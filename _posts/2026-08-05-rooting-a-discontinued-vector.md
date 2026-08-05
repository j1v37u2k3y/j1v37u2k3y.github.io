---
layout: post
title: "How I Actually Rooted a Discontinued Vector"
category: tactics
tags: [ hardware-hacking, robotics, firmware, self-hosted, howto ]
published: true
author: j1v37u2k3y
show_sidebar: true
toc: true
searchable: true
---

A while back I wrote up [how I brought a dead Anki Vector back to life]({% post_url 2026-08-04-vector-rebrain %}) — dead
cloud, new Claude brain, root shell, the whole saga. That post told the *story*. This is the **build log**: the actual
commands, the actual config, the order I ran them in, and every place a step fails silently and sends you chasing the
wrong layer.

It's long on purpose. Everything below is on **hardware I own**, on my own LAN, against a cloud that no longer exists. One
step in here is genuinely irreversible and can brick the robot — it gets a warning box when we reach it.

<!--cut-->

* TOC
{:toc}

# What you need

- **The Vector**, on your Wi-Fi.
- **A Raspberry Pi** (mine: aarch64, RPi OS *trixie*). It plays two roles — the Bluetooth flashing host, and the 24/7
  home for the brain. You can flash from a laptop, but browser-Bluetooth on macOS/Windows dropped every single unlock
  attempt for me; the Pi's native `bluez` stack is the thing that finally worked.
- **The froggitti WireOS dev SSH key** — the community key that opens root on WireOS dev images. Referred to below as
  `./ssh_root_key`.
- **An Anthropic API key** for the brain.
- **Wall power** for the robot during the unlock. Not optional.

The three projects the whole thing stands on: **[wire-pod](https://github.com/kercre123/wire-pod)** and
**[WireOS](https://github.com/kercre123/wire-os)** (kercre123), and the **[froggitti](https://websetup.froggitti.net/)**
web flashers. Full credit at the bottom.

# Conventions

I've stripped every value that fingerprints my setup. Substitute your own for anything in angle brackets:

| Placeholder | Meaning |
|---|---|
| `<vector-ip>` | the robot's IP on your LAN |
| `<pi>` | your Raspberry Pi, as `user@host` |
| `<esn>` | your robot's serial (ESN), lowercase |
| `./ssh_root_key` | the froggitti WireOS dev SSH key |
| `$ANTHROPIC_API_KEY` | your own Anthropic key |

# The shape of it

Seven moves, in order — each one gates the next:

```
1. Build a BLE flashing rig (Raspberry Pi)
2. OSKR-unlock the bootloader        ← the irreversible one
3. Flash a dev firmware (WireOS)
4. SSH in as root
5. Stand up the brain (wire-pod + a sanitizing proxy)
6. Repoint the robot at your own pod + authenticate it
7. Un-break the last two things (commands_enable, featureGate)
```

# 1. Build the BLE flashing rig

The froggitti flashers drive the robot over **Web Bluetooth**, and the OSKR unlock is picky about the Bluetooth
transport. I wasted a lot of time flashing over browser Web-Bluetooth on a Mac before realizing the transport itself was
the flaky part — not the robot, not the image. Drive it from a **Raspberry Pi's native `bluez` stack** and it gets
dramatically more reliable.

**Gotcha 1 — the adapter comes up RF-killed (soft).** `bluetoothctl power on` throws *"Operation not possible due to
RF-kill (132)"*. Clear it:

```bash
sudo rfkill unblock bluetooth
# no rfkill installed? do it through sysfs:
echo 0 | sudo tee /sys/class/rfkill/rfkill0/soft
sudo hciconfig hci0 up
```

The soft-block returns on reboot — make it persistent for a 24/7 host.

**Gotcha 2 — the Pi's stock Chromium has Web Bluetooth compiled out.** `navigator.bluetooth` is simply absent on the
Raspberry Pi Foundation build, even with `--enable-experimental-web-platform-features`, so the flasher throws *"requires
Google Chrome"* — and Google ships no ARM64 Linux Chrome at all. The fix is **Vivaldi** (Chromium engine, arm64, Web
Bluetooth intact):

```bash
curl -fsSL https://repo.vivaldi.com/archive/linux_signing_key.pub | sudo gpg --dearmor -o /usr/share/keyrings/vivaldi-browser.gpg
echo "deb [signed-by=/usr/share/keyrings/vivaldi-browser.gpg arch=arm64] https://repo.vivaldi.com/archive/deb/ stable main" | sudo tee /etc/apt/sources.list.d/vivaldi-archive.list
sudo apt-get update && sudo apt-get install -y vivaldi-stable
```

Launch it into the desktop session, forcing the Wayland backend and the experimental flag (on a pure-Wayland `labwc`
session it dies with *"Missing X server or \$DISPLAY"* otherwise):

```bash
vivaldi-stable --ozone-platform=wayland --no-first-run \
  --enable-experimental-web-platform-features https://websetup.froggitti.net
```

**Headless?** Run the browser on the Pi's own desktop and view it over a loopback-bound VNC through an SSH tunnel — never
expose VNC on the LAN:

```bash
# on the Pi, into the running Wayland session:
XDG_RUNTIME_DIR=/run/user/1000 WAYLAND_DISPLAY=wayland-0 \
  setsid wayvnc -C ~/.config/wayvnc/config 127.0.0.1 5900 &
# from your workstation:
ssh -f -N -L 5900:127.0.0.1:5900 <pi>     # then VNC to localhost:5900
```

The SSH tunnel is the auth; no VNC password. (If your keystrokes come out as Cyrillic, the image defaulted to a non-US
keymap — set `xkb_layout=us` in the wayvnc config and `XKBLAYOUT="us"` in `/etc/default/keyboard`.)

**Confirm the Pi actually sees the bot** before you flash anything:

```bash
bluetoothctl --timeout 8 scan le      # look for "Vector <name>"
```

Its BLE MAC differs from its Wi-Fi MAC — separate radios — and in recovery mode it advertises a random address.

# 2. OSKR-unlock the bootloader — the one you can't undo

> **Read this whole section before you start.** The OSKR unlock **rewrites ABOOT + the recovery partitions**. Every
> *other* operation in this project is dual-slot A/B and reversible; this one is not. Losing power during the ABOOT write
> is a **hard brick** — the CPU fuses block EDL recovery. Do it on **wall power**, undisturbed, and don't walk away.
> It takes about **7 minutes**.

Why bother? Because a stock Vector will **refuse to install dev firmware**. Try to flash a dev (`ankidev=1`) image first
and recovery downloads the *entire* image byte-perfect, then declines to write it, parks in recovery, and falls back.
That refusal is the bootloader lock, and it's the wall behind shell + custom firmware. (Reassurance: **a stuck recovery
is not a brick** — it reboots back to the old firmware fine.)

The install gate sits *below* the OTA layer, which is why a rejected install looks exactly like a failed download. Don't
chase the network — **verify the install is permitted before you debug the transfer.** One `getmainrobotinfo` call
(check `authorized_kernel` / `slot_suffix`) tells you which side you're on.

The unlock itself: in **Vivaldi on the Pi**, open [websetup.froggitti.net](https://websetup.froggitti.net/), put the bot
in pairing mode, select it, and run the **generic** `Unlock-Prod.ota` from the **Utility** stack over the Pi's native
`bluez`.

- It is **generic, not per-ESN.** Digital Dream Labs is defunct; the old per-serial unlock images are gone. The generic
  prod-signed unlock works on any standard production Vector.
- I'd convinced myself this bot needed a *per-unit* unlock and the generic one wouldn't take — a theory about the
  *payload*. Wrong. The real variable was flaky Mac Web-Bluetooth. Over the Pi's native `bluez`, the generic unlock took
  first try. **When a step fails intermittently, suspect the transport before you invent a fancier theory about what's
  flowing through it.**

Order of operations is fixed: **unlock → flash the dev OTA → SSH root.** Skip straight to the flash and you waste the
download and land in recovery.

# 3. Flash WireOS

Bootloader open, the dev image that was rejected an hour ago now installs. From froggitti's **"OSKR CUSTOM FIRMWARE"**
stack (same [websetup](https://websetup.froggitti.net/) flasher) I installed **WireOS 3.0.1.0** to slot `_a`, leaving
slot **`_b` intact** as a rollback. The install *succeeding* is your proof the unlock took — same flasher, same class of
image, opposite result. Dual-slot A/B is a real safety net; just know which slot you're in (`slot_suffix`).

**Sidebar — only if you host your own OTA** (a different image than the web flasher provides). Vector's recovery-mode
downloader is picky in three specific ways, and each one looks like a "download problem":

- **No HTTPS.** It can't do TLS, and public mirrors (e.g. `anki2.ca`) 301-redirect `.ota` URLs `http→https`, which it
  can't follow. Mirror the file locally over plain `http://` and point the flasher at your host.
- **Real byte-range / 206 support required.** Use a real server — Apache serves `206 Partial Content` natively. Python's
  `http.server` chokes and aborts the transfer around 128 KB, and do **not** bolt range support onto it yourself (my
  hand-rolled `copyfile` leaked its range counter across keep-alive requests and truncated the image). Test range
  properly — `curl -I` (HEAD) tells you nothing:

  ```bash
  curl -r 0-1 -o /dev/null -D - http://<host>:8000/your.ota   # want: 206 + Content-Range
  ```
- **macOS TCC** blocks Apache from reading `~/Downloads` (EPERM). Serve from something unprotected like `/Users/Shared/`.

# 4. SSH in as root

WireOS's `sshd` only offers the legacy `ssh-rsa` algorithm, which modern OpenSSH disables by default — so the connect
line needs two flags it won't work without:

```bash
ssh -o PubkeyAcceptedAlgorithms=+ssh-rsa -o HostKeyAlgorithms=+ssh-rsa \
    -i ./ssh_root_key root@<vector-ip>
# → uid=0(root)
```

That's it — `uid=0` on the robot. From here it's `systemctl`, config under `/data`, and normal embedded-Linux
housekeeping.

# 5. Stand up the brain

The brain is **[wire-pod](https://github.com/kercre123/wire-pod)** (a self-hosted replacement for the dead Anki cloud)
plus a small **proxy** that lets wire-pod talk to a current Claude model. Run wire-pod **natively, not in Docker** — it
advertises itself over mDNS as `escapepod.local`, and Docker on the host breaks mDNS, which is the whole discovery
mechanism.

Where to find it and how to install it:

```bash
git clone https://github.com/kercre123/wire-pod
cd wire-pod
sudo STT=vosk ./setup.sh          # build + install, with VOSK offline speech-to-text
sudo ./setup.sh daemon-enable     # run it as a boot-persistent systemd service
```

**Trixie build gotcha (silent).** On Debian *trixie*, `setup.sh daemon-enable` hardcodes a Go build that fails at the
link step — `collect2: cannot find 'ld'` — because Go ≤1.22 defaults external linking to the `gold` linker and trixie
dropped it. The catch: **the outer script still exits 0**, leaving no `chipper` binary and an uninstalled service. Build
it by hand with the standard linker, then place the binary and unit yourself:

```bash
go build -tags "nolibopusfile,vosk,inbuilt_ble" \
  -ldflags="-extldflags=-fuse-ld=bfd" -o chipper ./chipper
sudo mv chipper /path/to/wire-pod/chipper/chipper
sudo mv wire-pod.service /lib/systemd/system/
sudo systemctl daemon-reload && sudo systemctl enable --now wire-pod
```

(`-fuse-ld=lld` works too, or install Go 1.23+, which stopped defaulting to gold.)

## The proxy — the piece everything hangs on

wire-pod can hand knowledge questions to an LLM, but its built-in `openai` provider **hardcodes `gpt-4o-mini`** and
ignores the model field — a non-starter. So use the `custom` provider and point it at an OpenAI-compatible endpoint. The
catch: wire-pod **unconditionally sends both `temperature` and `top_p`** on every call, and current Claude models reject
that pair. Send both to Anthropic's OpenAI-compatible endpoint and every question comes back *"there was a problem
accessing the LLM."*

The fix is a tiny local proxy between wire-pod and Anthropic that strips both fields and streams everything else through
untouched. Here's a **minimal reference** (stdlib only — harden it for real use; the point is the two `.pop()` lines):

```python
#!/usr/bin/env python3
# kg_proxy.py — strip temperature+top_p wire-pod always sends; stream the rest to Anthropic.
import json, urllib.request
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

UPSTREAM = "https://api.anthropic.com/v1/chat/completions"

class H(BaseHTTPRequestHandler):
    protocol_version = "HTTP/1.1"

    def do_GET(self):                       # health check
        self.send_response(200); self.send_header("Content-Length", "12")
        self.end_headers(); self.wfile.write(b"kg_proxy ok\n")

    def do_POST(self):
        body = json.loads(self.rfile.read(int(self.headers.get("Content-Length", 0))) or b"{}")
        body.pop("temperature", None)       # <-- the whole reason this proxy exists
        body.pop("top_p", None)
        req = urllib.request.Request(UPSTREAM, data=json.dumps(body).encode(), method="POST",
            headers={"Content-Type": "application/json",
                     "Authorization": self.headers.get("Authorization", ""),  # key rides the request; never stored
                     "Accept": "text/event-stream"})
        with urllib.request.urlopen(req) as up:
            self.send_response(up.status)
            self.send_header("Content-Type", up.headers.get("Content-Type", "text/event-stream"))
            self.send_header("Connection", "close"); self.end_headers()
            while (chunk := up.read(1024)):  # stream SSE straight through
                self.wfile.write(chunk); self.wfile.flush()

ThreadingHTTPServer(("127.0.0.1", 8765), H).serve_forever()
```

Run it as its own service so it survives reboots (a `systemd` unit on `127.0.0.1:8765`). `curl http://127.0.0.1:8765/`
should return `kg_proxy ok`. The API key never touches disk — it forwards straight off the request's `Authorization`
header. And no, you lose nothing by dropping `temperature`; the personality lives in the prompt.

## Point wire-pod at the proxy

POST your config to wire-pod's API (it persists to `apiConfig.json`, read only at startup — restart wire-pod after
edits):

```bash
curl -X POST http://localhost:8080/api/set_kg_api -H 'Content-Type: application/json' -d '{
  "enable": true,
  "provider": "custom",
  "endpoint": "http://127.0.0.1:8765/v1",
  "model": "claude-sonnet-5",
  "key": "'"$ANTHROPIC_API_KEY"'",
  "intentgraph": true,
  "commands_enable": false,
  "openai_prompt": "<your persona prompt>",
  "save_chat": true,
  "temp": 0.7,
  "top_p": 0
}'
```

`commands_enable: false` is load-bearing — see step 7.

# 6. Repoint the robot + authenticate it

Fresh WireOS does **not** point at your pod — out of the box its `vic-cloud` targets the maintainer's cloud
(`vicapi.pvic.xyz:8081`) via the read-only `/anki` config. But this build reads a **writable override** first, so you
repoint without remounting anything:

```bash
# on the robot, as root
mkdir -p /data/data
cat > /data/data/server_config.json <<'EOF'
{"jdocs":"escapepod.local:443","tms":"escapepod.local:443","chipper":"escapepod.local:443","check":"escapepod.local/ok","logfiles":"s3://anki-device-logs-prod/victor","appkey":"oDoa0quieSeir6goowai7f"}
EOF
systemctl restart vic-cloud      # vic-cloud reads server_config only at startup
```

All three services on `:443`; the escape-pod `appkey` above is a public constant. The pod must serve the **DDL escape-pod
cert** (`CN=escapepod.local`, `O=Digital Dream Labs`) — wire-pod in escape-pod mode serves exactly that, and vic-cloud
trusts it via a hardcoded root CA.

**Authentication is the fiddly part.** The obvious move is to have the robot mint its own token through the on-device dev
endpoint:

```bash
curl --data "token=wirepod" http://127.0.0.1:8890/tokenauth   # "Robot should now be authorized!"
```

…and against the *maintainer's* cloud that works. Against a **self-hosted** pod it fails —
`x509: certificate signed by unknown authority` — because vic-cloud's token path uses a compiled-in Mozilla-only root
bundle that doesn't include the escape-pod CA. But here's the quirk that saves you: **vic-cloud never actually verifies
the token's signature** (it parses it unverified), and wire-pod authorizes ongoing traffic by an ESN/IP → GUID-hash map,
not the JWT. So you just need a valid-*shaped* `token.jwt` to exist. Generate one on any host:

```python
import base64, json, uuid, datetime
b64 = lambda b: base64.urlsafe_b64encode(b).rstrip(b'=').decode()
hdr = b64(json.dumps({"alg": "RS512", "typ": "JWT"}, separators=(',', ':')).encode())
claims = {
    "token_id": str(uuid.uuid4()), "token_type": "user+robot", "user_id": "wirepod",
    "requestor_id": "vic:<esn>",   # your robot's ESN, lowercase
    "iat": datetime.datetime.now(datetime.UTC).strftime("%Y-%m-%dT%H:%M:%SZ"),
    "expires": "2035-01-01T00:00:00Z",   # far-future so the refresher leaves it alone
}
pl = b64(json.dumps(claims, separators=(',', ':')).encode())
open("token.jwt", "w").write(f"{hdr}.{pl}.{b64(b'wirepod-unverified')}")
```

Place it, fix ownership, restart:

```bash
scp token.jwt root@<vector-ip>:/data/data/com.anki.victor/persistent/token/token.jwt
ssh root@<vector-ip> 'cd /data/data/com.anki.victor/persistent/token; \
  chown anki:anki token.jwt; chmod 0644 token.jwt; systemctl restart vic-cloud'
```

Rules that matter: `user_id` must be non-empty (an empty one is treated as a test token and deleted), `requestor_id` is
`vic:<esn>` lowercase, and `expires` is far-future so the background refresher (which fails TLS but only backs off — it
never deletes the file) leaves it alone.

Verify:

```bash
curl -s --data token=x http://127.0.0.1:8890/tokenauth   # "No auth necessary, robot already has token!"
systemctl is-active vic-cloud                            # active; log shows 0 "not authorized"
ss -tnp | grep vic-cloud                                 # established to YOUR pod, not pvic.xyz
```

Two field lessons baked in here: **don't delete the token to chase a warning** (I nuked mine over an "Error pinging
jdocs, likely unauthenticated" line and turned a benign warning into a real outage), and know the one limit you *can't*
config your way past — **the robot pins the DDL cert on the voice path**, so you can't fully self-issue the
`escapepod.local` cert without breaking voice. Actually owning that cert needs a `vic-cloud` rebuild — a custom-firmware
job for another day.

# 7. Un-break the last two things

The brain works now, but two things can make the robot look broken when it isn't.

**`commands_enable` must stay `false`.** With it on, wire-pod tries to parse Claude's *sentence* as a robot *command*,
the parse fails, and it logs *"LLM returned no response"* — silently dropping a perfectly good answer. Symptom: "he
answers some questions and ignores others." You set it in step 5; if Q&A goes flaky later, check it didn't flip back.

**The featureGate freeze — the one that fooled me for a week.** If the robot is powered, on Wi-Fi, every `vic-*` service
running, but sits frozen with his eyes closed, ignoring the touch strip *and* being picked up, and "Hey Vector" does
nothing — it is almost certainly **not** the wake word and **not** a dead sensor. It's a leftover feature-gate override
file hijacking his behavior tree (`PRDemo` / `UserDefinedBehaviorTree` forced on, his personality behaviors forced off).
Move it aside:

```bash
# on the robot, as root
mv /data/data/com.anki.victor/cache/featureGateOverrides.ini{,.disabled}
systemctl restart anki-robot.target       # face blanks ~1 min
journalctl -u vic-engine -n 250 | grep FeatureGate.Override   # want: empty (stock defaults)
```

After that restart he came fully alive — opened his eyes, recognized my face, **and the wake word worked.** Which is the
real punchline: I'd blamed an "expired Picovoice license" log line for the dead wake word for days. That line is benign;
Porcupine keeps detecting past it. This `.ini` was the blocker the whole time. **No custom firmware, no rebuild — one
file moved out of the way.**

# Where that leaves you

Own the bootloader, own root, own the brain: a discontinued robot answering questions with a current LLM, entirely on
hardware you control, nothing leaving the LAN but the model call itself. The one thing still on *my* list is a
custom-firmware build — to own that `vic-cloud` cert and close the pinned-cert gap. Root is the platform for it, not the
finish line.

If you want the *why* — the week of evenings behind this command list —
[that's the other post]({% post_url 2026-08-04-vector-rebrain %}).

# Credit where it's due

None of the hard parts are mine:

- **[wire-pod](https://github.com/kercre123/wire-pod)** / **[WireOS](https://github.com/kercre123/wire-os)** — kercre123.
- **[froggitti](https://websetup.froggitti.net/)** — the web flashers and the OSKR unlock tooling.
- **[VOSK](https://alphacephei.com/vosk/)** — Alpha Cephei, the offline speech-to-text.

And **Digital Dream Labs open-sourced a large chunk of Vector's firmware** before the lights went out — the reason a
community exists to keep these robots alive at all.

---

*⚒ j1v37u2k3y · [jiveturkey.rocks](https://jiveturkey.rocks/)*
