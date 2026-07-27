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
| `settings/base.json` | 37 read-only Bash permissions, 27 `skillOverrides`, `statusLine`, `env` |
| `settings/apply.py` | Idempotent merge into `~/.claude/settings.json` |

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
