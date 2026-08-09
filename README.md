# Claude Playground Repo

Doubles as a **Claude Code plugin marketplace** for personal config that should
follow me between machines (`~/.claude/` itself is machine-local and never syncs).

Two transports, because they carry different things:

- **Plugin marketplace** → output styles (and any future skills/commands/agents/hooks)
- **`install.sh`** → `settings.json` values, which plugins *cannot* ship

## Install on a new machine

```bash
git clone https://github.com/winsthuang/claude-playground && cd claude-playground
./install.sh --dry-run   # see what would change
./install.sh             # merge settings
```

Then inside Claude Code:

```
/plugin marketplace add winsthuang/claude-playground
/plugin install winston-output-styles@claude-playground
/plugin install winston-skills@claude-playground
```

Pick the style with `/config` → Output style, or `/output-style ELI5`.
Pull later changes with `/plugin marketplace update claude-playground`.

## What's here

| Component | Contents |
| --- | --- |
| `plugins/winston-output-styles` | `ELI5` — short sentences, no jargon, 2 options max when a decision is needed |
| `plugins/winston-skills` | `/ste100` — ASD-STE100 Simplified Technical English: session mode toggle or one-shot rewrite |
| `settings/base.json` | 26 read-only Bash permissions, `statusLine`, `outputStyle`, `env`, marketplaces + enabled plugins |
| `settings/apply.py` | Idempotent merge into `~/.claude/settings.json` |

`base.json` also registers the marketplaces and enables plugins, so a new machine
comes up with `ELI5`, `/ste100`, `de-ai-ify` and `slack-respond` without running
any `/plugin` commands by hand.

### What is deliberately *not* synced

**Commands that can execute arbitrary code.** `env`, `find` and `sqlite3` were
dropped from the allowlist — `env <cmd>`, `find -exec` and sqlite3's `.shell`
dot-command all run whatever you hand them, so an allowlist containing them is
not read-only. This matters more than it looks: an `allow` entry is a *hard*
pre-approval that short-circuits the `auto` mode classifier entirely. `sleep`
went too, since the harness blocks foreground `sleep` anyway.

**Commands the built-in tools already cover.** `cat`, `ls`, `head`, `tail`,
`locate`, `whereis` and `mdfind` duplicate Read/Glob/Grep, which Claude Code is
instructed to prefer — pre-approving them just smooths a path it shouldn't take.
`grep`, `rg` and `fd` are kept: they earn their place inside shell pipelines,
which the tools can't express.

**All `skillOverrides`.** The 27 entries suppressed skills that exist only as
local directories on one laptop, so there is nothing for them to suppress on a
new machine. The one real exception, `code-review`, was *intentionally dropped*
too — it is built into the CLI, so leaving the override in would have silently
disabled `/code-review` (and its multi-agent `ultra` variant) everywhere.

### External dependencies

- `statusLine` parses its JSON with **`python3`**, which `install.sh` already
  requires — so there is nothing extra to install. (It previously shelled out to
  `jq` four times and failed silently on machines without it.)
- `CLAUDE_CODE_TEAMMATE_MODE=tmux` needs **`tmux`** installed.
- `permissions.defaultMode: auto` is carried over by design. A bootstrapped
  machine starts in classifier-judged auto-approve from first launch.
- `slack-respond` reads its voice guide from an iCloud path under
  `~/Library/Mobile Documents/…/Claude Code/Slack/CLAUDE.md`. It degrades to
  generic defaults with a warning if that file is absent.

### Why settings need their own script

The plugin manifest has fields for `commands`, `agents`, `skills`, `hooks`,
`outputStyles`, `themes` — and nothing for `settings`. So the permission
allowlist and `skillOverrides` map can't ride along in the marketplace.

`apply.py` is **additive**: it unions the allowlist and the `skillOverrides`
map, and never deletes a key this repo doesn't define. Values that represent a
deliberate local choice (`permissions.defaultMode`, `statusLine`) are only
written when absent — it reports the conflict instead of clobbering. Pass
`--force` to override. Every write backs up the previous `settings.json` first.

Note: `permissions.allow` belongs in `settings.json`, not `settings.local.json`
— the latter is the machine-local variant that Claude Code now treats as legacy.

## Adding another output style

Drop a new `.md` into `plugins/winston-output-styles/output-styles/` with frontmatter:

```markdown
---
name: Style Name
description: shown in the /config picker
keep-coding-instructions: true
---

Prompt text that replaces Claude Code's default response style.
```

`keep-coding-instructions: true` keeps Claude Code's built-in software-engineering
instructions and layers the style on top. Omit it and the style replaces them
entirely — fine for a non-coding persona, bad for day-to-day work.
