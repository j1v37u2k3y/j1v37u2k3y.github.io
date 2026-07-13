---
layout: post
title: "Two Operators, Zero Tools: NeoSetup's Silent Gate"
category: tactics
tags: [ ansible, devenv, automation, tooling, open-source ]
published: true
author: j1v37u2k3y
show_sidebar: true
toc: true
searchable: true
---

Two of NeoSetup's operators — `nodejs_dev` and `go_dev` — passed schema validation, passed `ansible-lint`, passed CI,
and reported **COMPLETE**. They installed exactly zero tools. Had done for two releases.

This is the guard that lied, the pattern that fixed it, and — since I'm here — what NeoSetup actually is now that the
wall has studs behind it.

<!--cut-->

* TOC
{:toc}

# The green that meant nothing

NeoSetup is a dev-environment automation system: one command stands up a themed, batteries-included terminal — shell,
tmux, CLI tools, Docker — at whatever power level you want. You pick an **operator** (a config profile), it provisions
the box. `python_dev` installs the Python toolchain. `nodejs_dev` installs the Node toolchain. `go_dev` installs the Go
toolchain. That's the contract.

Except two of them didn't. `nodejs_dev` and `go_dev` applied their shell aliases, functions, and env vars — the visible
stuff — and installed **not one tool**. No `node`. No `nvm`. No `go`. Two profiles shipped labeled *complete* while
provisioning nothing.

And nothing complained. Schema validation: green. `ansible-lint` + `yamllint`: green. CI: green. Every check I had
agreed the operators were fine, because not one of those checks actually *installs a tool* and looks for it afterward.
Paint on a wall, and no studs behind it.

# The guard that lied

The install loop lives in `roles/tools/tasks/install_tools_unified.yml`, and its gate is one line of Ansible:

```yaml
- name: Install tool
  # ...resolve + install item...
  loop: "{{ operator_tools }}"
  when: item in tool_registry
```

Read that `when:` the way Ansible reads it. For each tool an operator asks for, check whether it's a key in
`tool_registry`. If it is, install it. If it *isn't* — skip. Not fail. **Skip.** No error, no warning, no non-zero exit.
The loop shrugs and moves to the next item.

The node and go tools were never registered in `roles/tools/vars/tool_registry.yml`. So the guard did exactly what it
was told: it found tools it had no entry for, and silently declined every one of them. The gate wasn't broken. It was
*obedient*. Nobody had told it about node or go, and its way of saying "I don't know that tool" was to say nothing at
all.

That's the whole trap. A `when: item in <registry>` filter turns an unregistered tool — a real bug, a broken contract —
into a no-op that looks identical to success. The operator is green because green is the *absence* of a raised error,
and a skip raises nothing.

# The fix: one installer per ecosystem

The instinct is to add rows to the registry — one per npm and go tool. Wrong joint. Node and Go tools aren't OS
packages; they're `npm install -g` and `go install` targets. Forcing them into the registry's per-tool `apt`/`brew`/
`pip` package model is jamming a finish nail where the frame needs a beam.

NeoSetup already had the right pattern sitting right there: `python_dev` doesn't register `pyenv`, `poetry`, and every
pip package separately — it has **one ecosystem installer** that owns the whole Python toolchain. So node and go get the
same treatment:

- `roles/tools/tasks/custom_installs/nvm_installer.yml` — installs `nvm`, then Node versions, then the global npm CLIs.
- `roles/tools/tasks/custom_installs/go_installer.yml` — installs the Go toolchain (Homebrew on macOS, the official
  tarball resolved from `go.dev/VERSION` on Linux), then `go install`s the tools.

Then register the *ecosystem*, not the leaves, in `tool_registry.yml`:

```yaml
operator_tool_sets:
  nodejs_dev: [ nvm ]
  go_dev: [ go ]
```

One installer per language, owning its whole world — mirroring pyenv/poetry exactly. Two smaller landmines fell out of
the same pass: a mangled command substitution in the `nodeinfo` shell function (`'Not found'kasync)` — a bad paste that
would've blown up at runtime), and a dead Go module path (`github.com/cosmtrek/air` → `github.com/air-verse/air`;
upstream moved the repo and the old path no longer resolves). Both were the kind of thing that only surfaces when
something finally *runs* the toolchain.

# Carve this one in: a silent skip is a lie about coverage

Here's the lesson, and it's bigger than one repo.

**If your contract is "listed means installed," then listed-but-unregistered must be loud, not skipped.** A guard that
silently drops the thing it can't handle isn't defensive — it's dishonest. It converts a broken promise into a passing
build. Every layer above it inherits the lie: the schema says complete, CI says green, the changelog says the operator
ships a toolchain, and the user gets an empty prompt.

The tell is always the same: *green is the absence of an error, not the presence of the result.* Validating that a
config is well-formed is not the same as validating that it does anything. Two operators can be perfectly well-formed
and install nothing, and no linter on earth will catch it — because "install nothing" is a completely valid thing for a
skipped task to do.

Measure twice. An operator being green in the schema doesn't mean it *does* anything. The only check that would have
caught this is the one that runs the install and then asks the box: is `node` actually here? (That end-to-end gap is now
[issue #77](https://github.com/j1v37u2k3y/NeoSetup/issues) — the `tools`/`docker` roles are `--skip-tags`'d in the
container CI, so the full toolchain install still isn't exercised in the pipeline. If it's not tested, it didn't happen.
I'm not going to pretend otherwise in a blog post.)

# So — what is NeoSetup?

Now that the wall stands up: NeoSetup is Matrix-themed development-environment automation, built **entirely on
Ansible**. No bespoke bash installer to drift out of sync — playbooks and roles are the load-bearing walls, and there's nothing
hand-rolled sitting beside them telling a different story.

The load-bearing idea is **operators**: config profiles that *extend each other*, so shared framing lives in one place
and specializations layer on top.

```
jiveturkey  →  matrix  →  base
```

`base` is the minimal essentials. `matrix` adds the cyberpunk theme. `jiveturkey` is the full power-user loadout on top
of that. Each operator declares `extends: <parent>` and inherits — then overrides — variables up the spine. Add
`python_dev` / `nodejs_dev` / `go_dev` / `macos` / `windows_wsl` for the specializations. Same inheritance model your
code uses, applied to your machine.

Which means the whole thing collapses to picking a pill:

| Pill      | Command                      | What you get                                   |
|-----------|------------------------------|------------------------------------------------|
| 🔴 Red    | `./setup install jiveturkey` | Full power-user setup, security tools included |
| 🔵 Blue   | `./setup install base`       | Minimal essentials only                        |
| 🟢 Matrix | `./setup install matrix`     | The cyberpunk theme, with style                |

# How it's framed

- **Ansible is the foundation.** Roles + playbooks do all the work — no separate installer to rot.
- **Roles are the studs:** `shell`, `tmux`, `tools`, `docker`, `common` — the framing every operator builds on.
- **Operators are the finish layer:** profile dirs with a `vars.yml` and an `extends:` line. Inherit up the spine,
  override what's specific to you.
- **`tool_registry.yml` is the single gate** every tool passes through — per-platform package mappings live there, so a
  tool is only offered where it genuinely installs. (Yes: *that* gate. The fix above didn't remove it — it made the
  ecosystem installers first-class citizens of it, so "listed" and "installed" mean the same thing again.)
- **Language toolchains** that don't map to apt/brew/pip each get one ecosystem installer that owns the whole toolchain,
  the way pyenv/poetry already did for Python.

It's tested across a **27-combination container matrix** — three operators (`base`, `matrix`, `jiveturkey`) against
Debian, Ubuntu, Kali, Parrot, Rocky, Alma, Fedora, and friends. With the honest caveat, above, about which roles that
matrix currently exercises.

# Honesty is the build policy, not a slogan

The same session that fixed the gate also pruned the issue board from **40 open to 8**. Not a mass-close — a triage. I
walked all 40 against the actual codebase and bucketed them DONE / PARTIAL / NOT-STARTED with file evidence, then closed
22 stale ones with tailored reasons. The four "cloud operator" tickets? The registry referenced
`kubectl_installer.yml` / `helm_installer.yml` / `azure_cli_installer.yml` that **don't exist on disk** — the exact same
silent-gate class of bug, but scaffolding over nothing. Closed as *broken*, not aspirational.

A board of untouched wishlist tickets is a lie about the roadmap, the same way a green-but-empty operator is a lie about
coverage. So the registry only claims a tool on platforms where it genuinely ships. Brew-only tools like `onefetch`,
`bottom`, `bandwhich`, and `git-sizer` got **deferred** rather than dressed up with fake apt names that silently no-op
on Linux — because I'd just spent the day paying for exactly that kind of quiet lie, and I wasn't about to introduce a
fresh one on the way out.

All of it shipped in **v2.1.0**.

# Take a pill

NeoSetup is open source. Clone it, pick your operator, and stand up a terminal that looks like it belongs to someone who
means it:

**→ [github.com/j1v37u2k3y/NeoSetup](https://github.com/j1v37u2k3y/NeoSetup)** · [v2.1.0
release](https://github.com/j1v37u2k3y/NeoSetup/releases/tag/v2.1.0)

```bash
git clone https://github.com/j1v37u2k3y/NeoSetup.git
cd NeoSetup
./setup
```

Red pill and the wall has studs now. I checked.

---

*⚒ j1v37u2k3y · [jiveturkey.rocks](https://jiveturkey.rocks/)*