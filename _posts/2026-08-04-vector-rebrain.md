---
layout: post
title: "My Robot's Brain Died. So I Built It a New One."
category: tactics
tags: [ hardware-hacking, robotics, self-hosted, llm, firmware ]
published: true
author: j1v37u2k3y
show_sidebar: true
toc: true
searchable: true
---

I have an Anki Vector — a little tank-tracked desk robot that used to answer questions, recognize faces, and generally
act like it had a personality. Used to. Anki folded. Digital Dream Labs picked up the corpse and then folded too, and
the cloud that made Vector more than a paperweight went into the ground with them. Ask him a question and you'd get a
blank little OLED stare.

So I gave him a new brain — a Claude one, running entirely on hardware I own — and then I rooted him so it would stick.
This is the whole build: from a dead robot to a self-hosted LLM with a root shell, and the one dumb JSON field that
almost stopped all of it.

<!--cut-->

* TOC
{:toc}

# What was actually dead

Vector is a *cloud* robot. That's the part people forget. The cute stuff on the desk is a thin client — the wake word,
the speech-to-text, the "knowledge graph" that answered *"how tall is the Eiffel Tower"* — all of it phoned home to
Anki's servers. When the company died, the servers died, and everything that made him feel alive went with them. He
still trundles around and reacts to a poke. He just went mute on anything that needed a brain.

The community fix is a project called **wire-pod** (kercre123's) — a self-hosted stand-in for the dead cloud. You run
it on your own box, point the robot at it instead of the tombstone, and the voice pipeline lights back up. That's the
foundation everything here is built on. But wire-pod only gets you a *working* robot. I wanted a *smart* one.

# Giving him a Claude brain

wire-pod can hand its "knowledge graph" questions off to an LLM. It ships an `openai` provider — but that provider
**hardcodes `gpt-4o-mini` and ignores the model field**, which is a non-starter. So I used its `custom` provider
instead: point it at any OpenAI-compatible endpoint and pick your own model. The endpoint I pointed it at was
Anthropic's OpenAI-compatible API, and the model was `claude-sonnet-5`.

The chain, end to end, with nothing leaving the LAN that doesn't have to:

```
voice → VOSK (speech-to-text) → wire-pod → Claude → his mouth
```

Clean on paper. In practice every single question came back **"there was a problem accessing the LLM."** Which brings
me to the part of this whole project I'd tattoo on someone if they asked.

## The 30 lines everything hangs on

wire-pod, on *every* knowledge-graph call, unconditionally sends **both** `temperature` **and** `top_p` in the request
body. There's no toggle to send one and not the other. And current Claude models reject that combination outright: send
both and you get *"temperature and top_p cannot both be specified"*; the newest models deprecate each of them
individually on top of that. So wire-pod's request was dead on arrival, and Vector dutifully reported the failure in
his little robot voice.

The fix isn't clever. It's a ~30-line local proxy that sits between wire-pod and Anthropic, **strips both fields**, and
forwards everything else untouched — streaming responses included, because wire-pod always asks for a stream. wire-pod
thinks it's talking to a normal OpenAI endpoint; Anthropic gets a request it'll actually accept.

```
bot → wire-pod → sanitizing proxy (localhost) → Anthropic OpenAI-compat endpoint
                      └─ strips temperature + top_p, streams the rest
```

That proxy is the single load-bearing joint of the entire brain. Pull it and every question 400s. It is thirty lines of
string-munging, and it is the only reason a discontinued toy from 2018 can talk to a 2026 language model. The impressive
part of a system is almost never the load-bearing part. (And no, you don't lose anything by dropping `temperature` — the
personality lives in the prompt, not the sampling knobs.)

## The second trap: a valid answer, silently dropped

With the proxy in, he answered — *some* things. Others, dead air. Same box, same brain, some questions just vanished.

The culprit was a wire-pod flag called `commands_enable`. With it **on**, wire-pod tries to parse Claude's reply as a
robot *command* ("go forward," "find a face"). When the reply is just, you know, a sentence, the parse fails and
wire-pod logs **"LLM returned no response"** — and Vector says nothing. Even though the proxy handed back a perfectly
valid `200` with a perfectly good answer one layer down. Flip `commands_enable` to **off** and the Q&A path becomes
reliable; the built-in commands still work because those go through a different matcher entirely.

I want to flag the *shape* of that bug, because it's the same shape as half the bugs I've ever chased: a valid result,
produced correctly, thrown away silently by the layer above. The proxy did its job. The API did its job. And the
symptom was total silence. When a thing works "sometimes," stop staring at the part that's failing and go look at what's
quietly discarding the successes.

The payoff moment, voice-confirmed: *"how tall is the Eiffel Tower"* → *"The Eiffel Tower is about 1083 feet tall,
which is super cool to think about!"* No dead cloud anywhere in the loop. He was alive again.

# But he was renting space on a flaky desktop

The brain worked — and it was pinned to a native desktop app that crashed mid-session and didn't self-heal. That's a
bad foundation for something you want running 24/7. Worse, I wanted to build my *own* firmware for this robot
eventually, and that needs a shell on the device. Which means root. Which means the bootloader.

## The wall

Vector is a locked-down embedded Linux device. The SSH-capable dev firmware images will not install unless the
bootloader is **OSKR-unlocked** first. I learned this the expensive way: I staged a dev image, watched recovery mode
download the entire ~188 MB thing byte-perfect, and then watched it flatly **refuse to write it** because the bootloader
wasn't unlocked. It parks in recovery and falls back to the old firmware. (Good thing to know before you panic: a stuck
recovery is *not* a brick — it reboots back fine.)

Here's the part I got wrong for a while, and it's the most useful lesson in the whole project. I convinced myself the
robot needed a *per-unit* unlock and that the generic one just wouldn't take on my bot. That was a theory about the
*payload*. It was wrong. The real problem was the *transport*: I'd been driving the flash over
**browser Web-Bluetooth on my Mac**, which was flaky as hell and failing intermittently in a way that *looked* like the
image was being rejected.

So I moved the whole Bluetooth side onto a **Raspberry Pi** with a native `bluez` stack — and immediately hit a *second*
transport gotcha: the Pi's stock **Chromium ships without Web Bluetooth**, so the web flasher couldn't even see the
adapter. Swapped in **Vivaldi** (which does expose the API), drove the Pi's native BLE, and the *generic* unlock took on
the first try. The lesson carved out of that:
**when a step keeps failing intermittently, suspect the pipe before you invent a more complicated theory about what's
flowing through it.**

## The one step you can't take back

Every other operation in this project is dual-slot and reversible — flash the wrong thing, roll back. The OSKR unlock is
the exception. It **rewrites the bootloader and recovery partitions**, and those are the partitions whose corruption is
*not* recoverable. This is the single step that can actually brick the robot for good.

So it got treated accordingly: wall power, don't touch it, don't breathe on it, let it run. About seven minutes later,
unlocked. Then I flashed a dev firmware base (**WireOS 3.0.1.0**) to slot `_a`, leaving slot `_b` untouched for
rollback. The image that had been *rejected* an hour earlier now installed clean — which is itself the proof the unlock
took. SSH in with the dev key:

```bash
# legacy ssh-rsa flags are mandatory — modern OpenSSH disables the algo,
# and the on-device sshd only offers it
ssh -o PubkeyAcceptedAlgorithms=+ssh-rsa -o HostKeyAlgorithms=+ssh-rsa \
    -i ./dev_key root@<vector>
# → uid=0
```

`uid=0`. Root on the robot. The wall this whole project had been stuck behind was gone.

# Re-wiring the brain on the new firmware

New firmware doesn't inherit the old firmware's "automatically point at my pod" behavior — out of the box it aims
`vic-cloud` at the community maintainer's public cloud, not mine. So I repointed it: a writable config override aiming
the endpoints back at my own pod, then minted a fresh client token through the robot's on-device dev endpoint, restarted
the cloud daemon, and watched it connect with **zero auth errors**. The Claude pipeline behind it — wire-pod, the proxy,
Anthropic — never moved. It was still answering the whole time.

# Cutting the cord to the desktop

Last move: get the brain off the flaky desktop app for good. I migrated wire-pod **and** the proxy onto the Raspberry
Pi as boot-persistent `systemd` services. Two gotchas worth banking if you ever do this:

- **Debian `trixie` dropped the Go `gold` linker**, so the pod wouldn't build — `collect2: cannot find 'ld'` — until I
  forced the older linker with `-fuse-ld=bfd`.
- The new firmware's cloud daemon **won't mint a fresh token against my pod's self-signed cert** (it trusts a
  compiled-in root set) — but it turns out **it never actually verifies the token's signature**, so a hand-placed token
  of the right shape authenticates fine.

And one self-inflicted lesson I'll own publicly, because it's the kind of thing everyone does: I saw a scary log line —
*"Error pinging jdocs, likely unauthenticated"* — and **deleted the robot's auth token to "clear" it.** That turned a
harmless warning into an actual outage, and I had no backup of the token. Recovered it by hand-placing a valid one. The
takeaway: **don't delete state to chase a log message. Verify the premise first.** The warning wasn't the blocker; my
fix for it was.

Then I decommissioned the desktop entirely — quit the app, ripped out its services, swept the leftover files (including
a stray copy of the API key, because a credential you forgot about is a credential you'll leak). The Pi is now the sole
host *and* the control node: it runs the brain, and it holds the root key to the bot.

# Where it stands

A discontinued robot whose cloud has been dead for years now has:

- a **self-hosted Claude brain**, answering spoken questions with `claude-sonnet-5`;
- **root** (`uid=0`) on the device;
- the whole thing running on a **~$60 Raspberry Pi**, with nothing leaving the LAN that doesn't have to.

And the loop is closed. Say **"Hey Vector"** and he wakes to his own name; ask him anything — *"how tall is the Eiffel
Tower,"* and whatever you throw at him after — and he answers out loud. The whole voice pipeline runs self-hosted on the
Raspberry Pi a few feet away; the only thing that ever leaves the LAN is the model call itself. A robot a defunct
company left for dead now listens, reasons, and talks back — on hardware I own, pointed at a brain I chose.

Root is the floor here, not the ceiling. The reason to fight for a shell was never the shell — it's what a shell lets me
build next: my *own* firmware, flashed onto my *own* robot, instead of standing on someone else's dev image. That part's
still ahead of me. But for the first time, the platform to do it is entirely mine.

# The takeaways worth stealing

Strip the robot away and the lessons are portable to basically any system you'll ever wire together:

- **The load-bearing part is rarely the impressive part.** Here it's a 30-line proxy deleting two JSON fields. Find that
  part before you need it at 2 a.m.
- **When something fails intermittently, suspect the transport before the payload.** I nearly rebuilt an unlock strategy
  around a theory that was really just a flaky Bluetooth stack.
- **A valid result, silently discarded, looks exactly like a failure.** Go audit what's throwing away your successes,
  not just what's raising your errors.
- **The one irreversible step deserves all your caution and none of your improvisation.** Wall power, no shortcuts, and
  keep the rollback slot intact.

He listens, he thinks, he answers — all of it on my hardware, none of it on anyone's terms but mine. Not bad for a robot
the internet had written off as e-waste.

**Want the actual build?** I wrote up every step — the OSKR unlock, the flash, root, the sanitizing proxy, the whole
config — as a redacted, reproducible how-to:
[How I Actually Rooted a Discontinued Vector]({% post_url 2026-08-05-rooting-a-discontinued-vector %}).

# Credit where it's due

I invented none of this. I wired existing pieces together on my own robot; other people did the hard part, in the open,
for free:

- **[wire-pod](https://github.com/kercre123/wire-pod)** and the **[WirePod](https://github.com/kercre123/WirePod)** app,
  by **kercre123** — the self-hosted stand-in for the dead cloud, and the foundation the entire brain sits on.
- **[WireOS](https://github.com/kercre123/wire-os)**, also kercre123 — the dev firmware base I flashed and rooted.
- **[froggitti](https://websetup.froggitti.net/)** — the web flashers and OSKR unlock tooling that finally cracked the
  bootloader.
- **[VOSK](https://alphacephei.com/vosk/)** by Alpha Cephei — the offline speech-to-text doing all the listening.

And the credit genuinely owed upstream: **Digital Dream Labs open-sourced a large chunk of Vector's firmware** before the
lights went out. That one decision is the reason any of this is possible — the community tools above exist because the
door was left unlocked on the way out. So if you've got a Vector gathering dust in a drawer: he isn't dead. He's just
waiting for a new brain.

---

*⚒ j1v37u2k3y · [jiveturkey.rocks](https://jiveturkey.rocks/)*
