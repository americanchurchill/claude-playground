# Claude Playground Repo

Doubles as a **Claude Code plugin marketplace** for personal config that should
follow me between machines (`~/.claude/` itself is machine-local and never syncs).

## Install on a new machine

```
/plugin marketplace add winsthuang/claude-playground
/plugin install winston-output-styles@claude-playground
```

Then pick the style with `/config` → Output style, or `/output-style ELI5`.

To pull later changes: `/plugin marketplace update claude-playground`

## What's here

| Plugin | Contents |
| --- | --- |
| `winston-output-styles` | `ELI5` — short sentences, no jargon, 2 options max when a decision is needed |

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
