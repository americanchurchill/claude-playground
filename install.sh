#!/usr/bin/env bash
# Bootstrap a new machine's Claude Code config from this repo.
#
#   git clone https://github.com/winsthuang/claude-playground && cd claude-playground
#   ./install.sh              # merge settings, then print the plugin commands
#   ./install.sh --dry-run    # show what would change, write nothing
#
set -euo pipefail
cd "$(dirname "$0")"

DRY=""
FORCE=""
for a in "$@"; do
  case "$a" in
    --dry-run) DRY="--dry-run" ;;
    --force)   FORCE="--force" ;;
    -h|--help) sed -n '2,8p' "$0"; exit 0 ;;
    *) echo "unknown option: $a" >&2; exit 2 ;;
  esac
done

echo "==> Merging settings into ${CLAUDE_CONFIG_DIR:-$HOME/.claude}/settings.json"
python3 settings/apply.py $DRY $FORCE

cat <<'EOF'

==> Output styles ship as a plugin. Run these inside Claude Code:

    /plugin marketplace add winsthuang/claude-playground
    /plugin install winston-output-styles@claude-playground

    Then: /config -> Output style, or /output-style ELI5
    Later updates: /plugin marketplace update claude-playground
EOF
