---
layout: post
title: "sudo Isn't Broken. It's Configured by Someone in a Hurry."
category: tactics
tags: [ privilege-escalation, linux, sudo, ctf, gtfobins ]
published: true
author: j1v37u2k3y
show_sidebar: true
toc: true
searchable: true
---

Every `sudo` privilege escalation you'll ever read online ends the same way: run `sudo -l`, spot a binary, look it up on
GTFOBins, get a root shell. That's one shape. I've rooted a lot of boxes through sudo over the years, and when I went
back through my own notes to see how many were actually that shape, the answer was: fewer than half.

sudo is not a vulnerability. It's a delegation tool — a way for an admin to say "this user may run *this* thing as
*that* user." Every line in a `sudoers` file was written by a real person solving a real problem, usually under time
pressure. The misconfiguration is never "sudo is broken." It's the **gap between what someone needed and what they
actually granted** — and that gap shows up in five recognizable shapes. Only one of them is the GTFOBins one.

This is a walk through all five, each with a retired box that shows it in the wild.

<!--cut-->

* TOC
{:toc}

# Read the whole line, not just the binary

`sudo -l` prints something like this:

```
User www-data may run the following commands on bashed:
    (scriptmanager : scriptmanager) NOPASSWD: ALL
```

Most writeups skip straight to the command and ask "can I escape it?" But a sudoers entry has three parts, and the
interesting information is usually in the two everybody ignores:

- **the runas field** — `(scriptmanager : scriptmanager)` — *who* you get to become
- **the tag** — `NOPASSWD:` — whether you even need a password
- **the command** — `ALL` — *what* you're allowed to run

Read left to right, that line does not say "root." It says "www-data may become scriptmanager and run anything."
That distinction is the first shape.

# Shape 1: the shell escape (the one you already know)

I'll get this out of the way fast, because it's the one that's been written to death.

Sometimes the granted command is a program that will hand you a shell if you ask it nicely. Pagers, editors, and
interpreters all qualify: `less` runs `!/bin/sh`, `vim` has `:!`, `nano` can spawn a command, `awk` and `find` and
`python` will all execute for you. GTFOBins is just the catalog of which ones and how.

On **[Openadmin](https://www.hackthebox.com/machines/OpenAdmin)**, `sudo -l` showed `nano` runnable as another user. That's a
[GTFOBins](https://gtfobins.github.io/gtfobins/nano/#sudo) one-liner — reset nano, execute a command, done. On
**[Warzone 2](https://www.vulnhub.com/entry/warzone-2,598/)** (VulnHub) it was `less`. Same idea, different binary.

The mechanism to internalize is not "nano is dangerous." It's: **the sudoers entry trusts the binary to stay in its
lane, and the binary was never designed to stay in its lane.** An editor's whole job is to run things for you. Granting
it via sudo grants everything it can reach.

That's shape one. The other four are where it gets interesting, because almost nobody writes about them.

# Shape 2: sudo sideways

Back to that [Bashed](https://www.hackthebox.com/machines/Bashed) line:

```
(scriptmanager : scriptmanager) NOPASSWD: ALL
```

`ALL` looks like the jackpot until you read the runas field. This doesn't make you root — it makes you **scriptmanager**.

```
sudo -H -u scriptmanager bash -c 'id'
```

That's not privilege *escalation* in the vertical sense. It's lateral movement wearing sudo's clothes. And it's easy to
dismiss as a dead end — until you look at what scriptmanager can do that www-data couldn't. On [Bashed](https://www.hackthebox.com/machines/Bashed), scriptmanager
owned a directory of scripts that **root** executed on a timer. So the chain was: www-data → (sudo) → scriptmanager →
(write a script root will run) → root.

The lesson: `NOPASSWD: ALL` to a low-value service account is still a foothold, because the next question is always
"what does *that* account touch that I couldn't reach before?" sudo gave you a sideways step. The privesc was waiting
one hop later.

# Shape 3: trusted binary, attacker-supplied code

Here the granted binary isn't a pager or an editor. It's something whose entire job is to **run code you give it** —
and that's exactly the problem.

On **[Canape](https://www.hackthebox.com/machines/Canape)**, the grant was effectively:

```
sudo /usr/bin/pip install .
```

`pip` is not a shell. It won't drop you to a prompt. But installing a package *runs that package's `setup.py`*, as root,
by design. So you don't need to escape pip — you just hand it a package whose `setup.py` is your payload. Point it at a
directory you control, and pip dutifully executes your code with root's privileges, exactly as it was built to.

Package managers are the classic case (`pip`, `gem`, `npm`, `make`), but the pattern is broader than that: any trusted
binary that consumes a file *you* wrote and treats it as instructions is this shape. The binary is behaving perfectly.
The misconfiguration is that the sudoers grant trusted the tool without noticing the tool trusts its input — and its
input is yours.

# Shape 4: trusted script, untrusted input

This is the one I see mislabeled most often, because at a glance it looks like shape 1.

```
sudo /usr/bin/python3 /opt/remote-manage.py
```

People see `python3` and reach for GTFOBins. But you weren't granted `python3` — you were granted `python3` **running one
specific script you can't edit**. The interpreter is a red herring. The attack surface is the *script*, and specifically
whatever the script reads that you can influence.

On **[Forge](https://www.hackthebox.com/machines/Forge)**, that script exposed an interactive path — feed it the wrong input and it dropped into a Python prompt of
its own, which is game over. On **[Busqueda](https://www.hackthebox.com/machines/Busqueda)**, a root-run maintenance script invoked other tools (`git`, `docker`) using
**relative** paths and configs sitting in a directory the lower-privileged user could touch. You never modify the
trusted script. You modify what it trusts: a config file, a `PATH` lookup, a file it parses.

The tell is in the entry itself: a sudoers line that grants an interpreter *plus a fixed script* is trying to be safe —
the admin thought "I'm only letting them run this one reviewed script." The hole is everything that script pulls in at
runtime, none of which is in the sudoers line.

# Shape 5: writing the misconfiguration yourself

The first four shapes are about *finding* a bad grant. This one inverts it: sometimes there's no bad sudoers entry at
all — so you write one.

This needs a different precondition: a way to make root (or a process running as root) write a file. On **[SickOS 1.2](https://www.vulnhub.com/entry/sickos-12,144/)**,
a root-owned task periodically executed a script from a world-writable location. So I didn't attack sudo — I made the
root task append to `sudoers` for me:

```
echo 'www-data ALL=NOPASSWD: ALL' >> /etc/sudoers
```

Drop that into the file root runs, wait for the timer, and now the misconfiguration exists because I put it there. On
**[Lightweight](https://www.hackthebox.com/machines/Lightweight)**, the write primitive was more direct — enough access to overwrite `/etc/sudoers` outright, so I built
the sudoers file I wanted locally and dropped it over the real one.

This reframes what "a sudo vuln" even means. The sudoers file is just a file. If anything root controls can be coerced
into writing it — a cron job, a backup script, a file-write primitive from some other bug — then the sudo
misconfiguration isn't something you *find*, it's something you *author*. Which is exactly why write access to
`/etc/sudoers`, and to anything root executes, matters as much as the grants already in it.

# Shape 6: sudo without a shell

The last one is my favorite, because it violates the unspoken assumption behind all sudo tutorials: that you're sitting
at an interactive shell when you run it.

On **[FluxCapacitor](https://www.hackthebox.com/machines/FluxCapacitor)**, I never got a shell before rooting the box. The whole privesc happened over HTTP. A web endpoint
passed a parameter into a command line without sanitizing it, and the web user had a sudo grant for a management binary:

```
GET /sync?opt=' sudo /home/themiddle/.monit cmd <base64-encoded-command>' HTTP/1.1
```

That `.monit cmd` grant let the web user run an arbitrary command as root — and I reached it not from a terminal but by
injecting into a query string. Command injection in the web layer, chained straight into a sudo grant held by the
service account, executed as root. No TTY anywhere in the chain.

The point is that a sudo grant is reachable by **anything that can make that account run a command** — a web bug, a
deserialization gadget, a cron misfire — not just a person at a prompt. When you audit a service account's sudo rights,
the threat model isn't "what if this user logs in." It's "what if *anything* that runs as this user gets to pick the
command."

# So what does secure sudo look like

Every shape above maps to a defensive mistake, so here's the inverse — read it as the checklist the hurried admin
skipped:

- **Read your own runas fields.** `NOPASSWD: ALL` to a service account is a lateral foothold even when it isn't root.
  Grant the narrowest user, not the most convenient one.
- **Never grant a shell in disguise.** Pagers, editors, and interpreters (`less`, `vi`, `nano`, `python`, `awk`, `find`)
  can all execute arbitrary commands by design. If GTFOBins has an entry, sudo shouldn't.
- **Never grant a tool that runs its input as code.** `pip`, `gem`, `npm`, `make` — the binary is on the allowlist, but
  its input isn't, and its input is the attacker's.
- **If you must grant a script, its inputs are in scope too.** Pin absolute paths, set `secure_path`, drop the
  environment, and treat every file and config the script reads as part of the grant — because it is.
- **Guard who can write the grant.** `/etc/sudoers` and everything root executes (cron scripts, `*.d` drop-in dirs,
  backup jobs) are attack surface. A file-write primitive that reaches any of them is a sudo misconfiguration waiting to
  be authored.
- **Model the account, not the shell.** A service account's sudo rights are reachable by anything that can make it run a
  command, including a web request. Audit the grant against the account's full attack surface.

# The one line worth remembering

Across nine boxes, the sudoers file was never the villain. It was an honest record of what somebody needed to get their
job done on a particular Tuesday — a deploy that had to work, a maintenance task that had to run unattended, a service
that needed *just* enough access. Every one of those was reasonable in the moment.

The attacker doesn't read what you needed. The attacker reads what you granted, and they read it forever.

---

*⚒ j1v37u2k3y · [jiveturkey.rocks](https://jiveturkey.rocks/)*
