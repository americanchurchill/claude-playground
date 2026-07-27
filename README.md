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
```

Pick the style with `/config` → Output style, or `/output-style ELI5`.
Pull later changes with `/plugin marketplace update claude-playground`.

## What's here

| Component | Contents |
| --- | --- |
| `plugins/winston-output-styles` | `ELI5` — short sentences, no jargon, 2 options max when a decision is needed |
| `settings/base.json` | 33 read-only Bash permissions, `statusLine`, `env`, marketplaces + enabled plugins |
| `settings/apply.py` | Idempotent merge into `~/.claude/settings.json` |

`base.json` also registers the marketplaces and enables plugins, so a new machine
comes up with `ELI5`, `de-ai-ify` and `slack-respond` without running any
`/plugin` commands by hand.

### What is deliberately *not* synced

**Four permissions were dropped from the allowlist.** `env`, `find` and `sqlite3`
all execute arbitrary commands — `env <cmd>`, `find -exec`, and sqlite3's
`.shell` dot-command — so an allowlist containing them is not read-only, it is
silent arbitrary execution that never prompts again. `sleep` went too: the
harness blocks foreground `sleep` anyway. Add them back if you want them; the
principle here is that the allowlist holds only what cannot execute code.

**26 of the 27 `skillOverrides` were dropped.** They suppress skills that exist
only as local directories on one laptop, so on a fresh machine there is nothing
to suppress. `code-review` is the exception — it is built into the CLI, so that
override is load-bearing everywhere and is kept.

### External dependencies

- `statusLine` shells out to **`jq`**. Without it the status line silently breaks.
- `CLAUDE_CODE_TEAMMATE_MODE=tmux` needs **`tmux`** installed.
- `permissions.defaultMode: auto` is carried over. A fresh machine will start in
  auto-approve mode — deliberate, but worth knowing before running this on a
  machine you trust less than your laptop.
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
