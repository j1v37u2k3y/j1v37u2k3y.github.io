---
layout: post
title: "Building Just the tIP: An IP Finder That Trusts Nobody"
category: tactics
tags: [ self-hosted, privacy, docker, tor, php, geoip ]
published: true
author: j1v37u2k3y
show_sidebar: true
toc: true
searchable: true
---

Every "what's my IP" site on the internet does the same quiet thing: it takes the one piece of data you came to look
up — your IP — and hands it to three or four third-party APIs to geolocate it, name it, and flag it. You ask a privacy
question and the page answers by leaking the answer.

**Just the tIP** is my attempt at the opposite. It's a single-page PHP app that tells you your public IP, your
reverse-DNS hostname, roughly where that IP lives, and whether it smells like a VPN or a Tor exit — and, once it's fully
configured, a request to it touches *no* third party to do any of that. It's live at
[ip.jiveturkey.rocks](https://ip.jiveturkey.rocks), it's also on a `.onion`, and this is the whole build: a dormant
PHP 7.4 app dragged onto Render, a client-IP bug that only existed in production, a month of deleting every external
dependency it had, and the discipline of only printing privacy claims I could back with code.

<!--cut-->

* TOC
{:toc}

# The job

The starting point was unglamorous: an old IP-finder repo (`welikechips/ip-finder`) that had been dormant since the
PHP 7.4 days. It worked, technically, on a laptop. The job was to drag it off the workbench and stand it up in public,
on a real domain, running real PHP — and to make it something I'd actually be willing to point people at.

That "willing to point people at" part is what turned a one-afternoon deploy into a months-long thread. Because the
moment you host a privacy tool publicly, every shortcut it takes becomes a promise you're making to strangers. And the
first version took a lot of shortcuts.

One thing up front, because it trips people reading the repo: there's a `tor_check.py` in there, a standalone Python
Tor-connection checker that rides along inside the Docker image. It is **not** part of the website — nothing on the
page calls it. Two tools, one image. Don't conflate them. Everything below is about the web app.

# Standing it up on Render

First decision, killed on contact: GitHub Pages. Pages is static-only; it will not execute a line of PHP. This app is
PHP to the bone, so Pages was out before I finished typing the thought.

I looked at the usual free-tier suspects. Fly.io no longer has a permanent free tier. Oracle Cloud's "Always Free" tier
sounds great until the signup wall eats your registration. I landed on **Render's free tier**: native Docker, free TLS,
free custom domains. It does want a card on file at signup — their docs imply otherwise, but in practice it asked — and
it never charged it. The tradeoff I signed up for is the free-tier cold start: after 15 minutes idle the service spins
down, and the next visitor waits ~30–60s for it to wake. For a "check my IP" toy, acceptable.

## Docker, and the one rule that matters

The image is `php:8.3-apache` — bumped up from the EOL 7.4 the repo shipped with. The `Dockerfile` strips Apache's
access logging (more on *why* later — it's load-bearing for a privacy claim), and bakes in the bits the app needs.

The interesting file is `deploy/docker-entrypoint.sh`, because it's the joint between "a container I built" and "a
platform I don't control." Render injects the port your app must listen on as `$PORT` at runtime — it's not fixed, and
it's not 80. So the entrypoint rewrites Apache's listen directive to `$PORT`, then does the part people skip:

```sh
# rewrite Apache to Render's injected port, then hand off as PID 1
exec apache2-foreground
```

That `exec` matters. Without it, your shell script stays PID 1 and Apache runs as its child — which means the platform's
stop signals hit the shell, not the server, and your health checks and graceful shutdowns quietly lie to you. `exec`
replaces the shell with Apache so **Apache is PID 1**: clean signals, honest lifecycle.

## The Blueprint

Render reads a `render.yaml` Blueprint so the whole service is defined in the repo, not clicked together in a dashboard:

```yaml
services:
  - type: web
    runtime: docker
    plan: free
    region: virginia
    autoDeploy: true        # deploy on push to the default branch
    envVars:
      - key: IPINFO_TOKEN
        sync: false          # set in the dashboard, never committed
```

`sync: false` is the important flag: it declares the variable exists but keeps its value out of the repo — you set it
in the dashboard. Secrets never touch git.

There's a small, genuinely useful trick hiding in Render's behavior here: **service env vars are also passed as Docker
build args.** That's what later lets me bake a licensed MaxMind database into the image at *build* time from a key I
never commit — but I'm getting ahead of myself.

## The front door

The domain `jiveturkey.rocks` is registered at Bluehost — domain only, no hosting plan. `ip.jiveturkey.rocks` is just a
**CNAME** in Bluehost's DNS pointing at the Render service. Render terminates TLS and issues the cert. There's no Caddy
of mine, no reverse proxy of mine — Render's edge is the entire front door. Which brings us to the first real bug.

# The bug that only exists in production

Locally, getting the client's IP is trivial: read `REMOTE_ADDR`. In production it was wrong for everybody, and it was
wrong in the most misleading way possible — it returned *my server's* IP, not the visitor's.

Here's why. Render fronts every service with Cloudflare. Your container never sees the visitor's TCP connection; it sees
Render's proxy. So `REMOTE_ADDR` is the proxy, and the real visitor IP arrives in headers the edge sets:
`True-Client-IP`, `CF-Connecting-IP`, or as the **leftmost** hop of `X-Forwarded-For`.

My first instinct was the textbook one: Apache's `mod_remoteip`. Configure the trusted proxies, let the module rewrite
`REMOTE_ADDR` for you, done. Except it broke — and it broke *on the live site*, not on a whiteboard. `mod_remoteip`'s
trust model assumes your proxy connects from a **private** range. Render's Cloudflare edge connects from **public** IPs.
So the module refused to trust the hop and surfaced Render's own egress IP as "your" IP. Everyone who visited saw the
same wrong address.

I ripped `mod_remoteip` back out and did it in application code instead. `getClientIP()` reads the edge headers in
priority order, then falls back to `REMOTE_ADDR` for direct or local access:

1. `True-Client-IP`
2. `CF-Connecting-IP`
3. leftmost `X-Forwarded-For`
4. `REMOTE_ADDR` (direct / local)

The anti-spoofing property is subtle but real: because the Cloudflare/Render edge is the *only* path to the container,
and that edge **overwrites** those `*-Client-IP` headers on every request, a visitor can't forge them. Whatever they
send gets stomped by the edge before my code sees it. (There's a regression test in the suite that specifically pins the
Cloudflare `172.71` range behavior, because this is exactly the kind of thing that silently rots.)

The lesson I keep relearning: **some bugs don't exist until there's an edge in front of you.** You cannot catch this one
on localhost, because on localhost there is no Cloudflare.

# v2: making it actually useful

With v1 live, the next batch (six features) turned it from "shows an IP" into something worth bookmarking:

- **Dark mode** with an Auto / Light / Dark switch, and copy-to-clipboard buttons on every value.
- **HSTS** and the rest of the security headers.
- **A curl-friendly API.** `curl ip.jiveturkey.rocks` returns the bare IP, `?format=json` returns JSON, `?format=text`
  echoes just the value. The page is for humans; the API is for scripts.
- **VPN / datacenter / Tor-exit flags** — badges on the page and a `flags[]` array in the JSON. Crucially, the Tor-exit
  match is done against a **local** list, so your IP is never shipped out to check it.
- **Client-side WebRTC leak detection** — the browser probe that catches the classic "my VPN is on but WebRTC is
  narrating my real IP" leak, entirely in-browser.

That last pair — local Tor matching, in-browser WebRTC — set the direction for everything after. If the *features* could
run without phoning home, why couldn't the *whole app*?

# Cutting every third party

This is the part I'm proudest of, and it took a four-step initiative to pull off. The goal was blunt: a deployed request
should hit **no** external service to resolve your IP, hostname, geolocation, or Tor status. Here's each dependency and
how it died.

## Geolocation → local MaxMind

The original geo lookup called out to ipinfo.io, with ipwho.is as a fallback. Both are third parties, and ipinfo
throttles token-less requests from datacenter egress (the tell is a response with a `"readme": ".../missingauth"` body
and no `city`) — which is exactly what a cloud-hosted app *is*.

So geo moved local. The app now reads **MaxMind's GeoLite2** City and ASN databases directly, on-box, via the
`maxminddb` PECL extension (`MaxMind\Db\Reader`) — no Composer, which keeps the repo dependency-free. The `.mmdb` files
bake **into the image at build time** — and this is where that earlier Render detail pays off: Render passes service env
vars as Docker build args, so setting `MAXMIND_LICENSE_KEY` in the dashboard lets the build download the licensed DBs
without the key ever touching git. Only if the local DB is absent does it fall back to the HTTP APIs, so a keyless build
still works out of the box. Local is faster, private, and doesn't get rate-limited.

## Reverse DNS → the system resolver

The hostname lookup had an ipinfo fallback too. I deleted it, because it was *redundant*: ipinfo's "hostname" is itself
just a PTR record lookup. So `resolveHostname()` is now system-resolver-only — `gethostbyaddr`, the PTR record, plus a
forward-confirm heuristic for EC2-style names. Same answer, zero third parties.

## Browser detection → our own echo

The client-side "here's what the browser sees" panel used to fetch `api.ipify.org`. Now it fetches *our own*
same-origin `?format=text` endpoint. Dropping that one external `fetch` let me tighten the Content-Security-Policy hard:
`connect-src 'self' stun:` and `frame-src 'none'`. The tradeoff is honest — the browser tab now mostly mirrors the
server's answer instead of getting a truly independent cross-origin read — but WebRTC remains the real, independent leak
detector, and the page no longer talks to anyone but itself.

## Tor detection → a build-baked list

Tor-exit detection reads a bulk exit list that's **baked into the image at build**. `isTorExit()` does zero runtime
fetches and works fully offline; the runtime download is demoted to a fallback. Staleness is bounded by how often I
rebuild — which I automated (next section).

## The one exception, on purpose

WebRTC leak detection needs a STUN server *by protocol* — that's just how the browser discovers its own candidate IPs.
So the page keeps Google's public STUN endpoint. It's the sole deliberate third-party exception, and it's a fair one:
the STUN server never sees the page or its data, only a NAT-traversal handshake the browser initiates. Self-hosting
coturn is the purist move, but that's real infrastructure for a free-tier toy. I documented the exception rather than
pretending it didn't exist.

## Proving it

Claims are cheap. I ran the container with `--network none` — no network at all — and the IP, hostname, geo, and Tor
checks all still resolved. That's the proof: with a MaxMind key set, a deployed request touches **no** third party for
any of the four. Only WebRTC's STUN handshake reaches out, by design.

# Saying true things

Cutting the third parties created a new problem: the page's old footer now *lied*. It said "your IP is only sent to
third-party services to perform the lookup, never kept here" — a sentence that was true in v1 and became false the moment
I deleted those services. So the privacy copy got the same treatment as the code.

The footer line became a visible **privacy card**: six claims, each one traceable to actual code or deploy config —

- no database,
- no access logs,
- no tracking beyond one CSRF cookie,
- rate-limiting keeps no raw IP,
- lookups run locally (with the honest fallback caveat),
- WebRTC stays in-browser.

Two of those deserve their war stories.

**"No access logs" had to be made true before it could be printed.** The Dockerfile strips the vhost `CustomLog` and
runs `a2disconf other-vhosts-access-log`, so no visitor IP is ever written to a log in normal operation. And there's an
integration test that boots the container, hits it, and asserts no visitor request appears in the logs — so the claim
can't silently regress into a lie on some future refactor. Make the claim true, *then* guard it, *then* print it.

**And even a true claim can overclaim.** My first draft of the card said "No access logs — your IP is never written to a
log file." That implies *end-to-end* no-logging, and it doesn't hold: the app sits behind Cloudflare and Render, which
terminate the connection and see your IP the way any host does — that's literally where `True-Client-IP` comes from. So
the claim got scoped to what I actually control: *this app* keeps no access logs, with an honest caveat that the CDN and
host in front of it can see your IP the way any edge does, and that layer is outside the app's control. The difference
between a privacy claim and a privacy lie is usually a caveat about the edge you don't own.

Even the rate limiter respects this. It's per-IP now (the old session-keyed version capped nothing for a cookieless
client), but it stores **no raw IP** — the client IP is SHA-1 hashed into the bucket's *filename*, and the file body
holds only a count and a first-seen timestamp. Stale buckets auto-delete. It rate-limits you without remembering you.

# Keeping the baked data fresh

Baking GeoLite2 and the Tor list into the image is fast and private, but it has an obvious failure mode: a plain redeploy
can reuse a warm build cache and ship *stale* data forever. So there's a weekly GitHub Actions cron
(`refresh-deploy.yml`) that hits the Render API with `clearCache: clear`, forcing a clean rebuild that actually
re-downloads the databases and the exit list. The `RENDER_API_KEY` and `RENDER_SERVICE_ID` live as repo secrets; the
first manual run came back `HTTP 201` with `trigger: api`, so it's proven, not hopeful. Fresh data, no third party at
request time — the freshness cost is paid on a timer, off the critical path.

# A little polish

Two small UI passes, because a privacy tool should *feel* right:

- **A loud Tor flag.** When you're coming from a Tor exit, the thin little pill became a filled, glowing, gently-pulsing
  `🧅 TOR EXIT NODE` badge, and the whole "Your External IP" card lights up onion-purple. The pulse is gated behind
  `prefers-reduced-motion`, so it calms down for anyone who's asked the OS to stop animating things.
- **Dark by default.** A fresh visitor now lands in dark mode — a tiny pre-paint script in the `<head>` sets the theme
  before first paint (no flash), and only if you've never expressed a preference. The toggle cycles Dark → Light → Auto
  and remembers whatever you pick.

# Onto a .onion

The last chapter, and my favorite: the app now serves itself over a **Tor v3 onion service**, co-located in the very
same Render container, at

```
jiveserzcd3zj6ptn3o3cr5l35pfibmw4vgzvkjjsvuwwuknnnptc6qd.onion
```

That `jive` prefix isn't luck — it's a vanity address ground out with `mkp224o`, brute-forcing keys until one produced
an address starting with the string I wanted. The private key stays in offline custody and never touches the repo; it's
handed to the running service as a base64 blob in an env var (`ONION_KEY_B64`), because Render's Secret Files UI turned
out to be hard to find and an env var was the pragmatic path.

Architecturally, the whole thing shipped *dormant* first, behind an `ENABLE_ONION` flag — a `tor` sidecar wired into the
entrypoint, an `isOnionHost()` check, an onion-mode panel, HSTS gated to clearnet only (HSTS over an onion is
meaningless), and an `Onion-Location` header advertising the onion to Tor Browser users on the clearnet site. Then the
flag flipped on.

And here's the detail I love, because it's *self-consistent*: **over the onion there's no exit node and no client IP to
show.** Tor's onion routing means the service genuinely cannot see where you are. So visiting the tool over its own
onion, the page correctly reports that there's nothing to display — *that's the point.* Meanwhile, if you route to the
*clearnet* site through Tor, the page shows the exit relay's IP and lights up that loud Tor badge. Same tool, two paths,
and both answers are honest.

The honest caveat, again: on Render's free tier this is a keep-warm hack. The service spins down when idle and can't wake
itself, so the onion is only reliably reachable with an external pinger keeping it warm. I'd rather say that out loud than
imply an always-on hidden service I'm not paying for.

# Tests, because otherwise it's vibes

The whole thing rides on a plain-PHP test suite — no Composer, no framework. As of the last pass it's **84 unit + 31
integration = 115 checks, all green** in CI on every push and PR. The unit tests cover the validators, `getClientIP()`
header priority (including the anti-spoof and the Cloudflare-range regression), the rate-limiter decision logic, and the
MaxMind record normalization. The integration tests build and boot the real container and `curl` the real endpoints —
including that "no visitor IP in the logs" assertion.

One rule I'm strict about: **no real IPs in tests.** Everything uses RFC 5737 TEST-NET ranges and RFC 5398
documentation ASNs. A test fixture is not the place to leak a real address.

# What it taught me

Strip away the specifics and this project is one idea repeated: **a privacy tool has to be true at the code level, not
the copy level.** Every claim on that page traces to something you can read in the repo or the deploy config, and where
it can't be fully true, it carries a caveat instead of a lie.

The rest is corollaries. Bake data locally and refresh it on a timer instead of phoning home per request. Assume the edge
in front of you will surprise you, because it will. Prove your "it touches nobody" claim with `--network none`, not with
confidence. Make the claim true *before* you print it, and guard it with a test so it stays true. And when you genuinely
can't control a layer — the CDN, the host, the STUN handshake — say so, plainly, on the page.

It's live at [ip.jiveturkey.rocks](https://ip.jiveturkey.rocks), the code is at
[github.com/welikechips/ip-finder](https://github.com/welikechips/ip-finder), and if you're on Tor Browser, the onion's
in the `Onion-Location` header — or right up there in the address I already gave you.

---

*⚒ j1v37u2k3y · jiveturkey.rocks*
