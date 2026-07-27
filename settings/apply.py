#!/usr/bin/env python3
"""Merge settings/base.json into a machine's ~/.claude/settings.json.

Additive by design: unions the permission allowlist and skillOverrides map,
and never removes a key this repo does not define. Values that would clobber
an existing local choice (permissions.defaultMode, statusLine) are only
written when absent, unless --force is passed.
"""
import argparse
import json
import shutil
import sys
from datetime import datetime
from pathlib import Path

HERE = Path(__file__).resolve().parent


def merge(base: dict, cur: dict, force: bool) -> tuple[dict, list[str], list[str]]:
    out = json.loads(json.dumps(cur))
    changes: list[str] = []
    skipped: list[str] = []

    for k, v in base.get("env", {}).items():
        if out.setdefault("env", {}).get(k) != v:
            out["env"][k] = v
            changes.append(f"env.{k} = {v}")

    perms = base.get("permissions", {})
    if "allow" in perms:
        cur_allow = out.setdefault("permissions", {}).get("allow", [])
        added = [a for a in perms["allow"] if a not in cur_allow]
        if added:
            out["permissions"]["allow"] = sorted(set(cur_allow) | set(perms["allow"]))
            changes.append(f"permissions.allow += {len(added)} entries")

    # Scalars that represent a deliberate local choice: do not clobber silently.
    for key, val in (("defaultMode", perms.get("defaultMode")),):
        if val is None:
            continue
        cur_val = out.setdefault("permissions", {}).get(key)
        if cur_val is None or force:
            if cur_val != val:
                out["permissions"][key] = val
                changes.append(f"permissions.{key} = {val}")
        elif cur_val != val:
            skipped.append(f"permissions.{key}: kept {cur_val!r} (repo has {val!r})")

    # Plain additive maps: repo wins per-key, local-only keys survive.
    for section, label in (("skillOverrides", "skillOverrides"),
                           ("extraKnownMarketplaces", "marketplaces"),
                           ("enabledPlugins", "plugins")):
        if not base.get(section):
            continue
        cur_map = out.setdefault(section, {})
        added = {k: v for k, v in base[section].items() if cur_map.get(k) != v}
        if added:
            cur_map.update(added)
            changes.append(f"{label}: {', '.join(sorted(added))}")

    # Top-level values that represent a deliberate local choice.
    for key in ("statusLine", "outputStyle"):
        if not base.get(key):
            continue
        if not out.get(key) or force:
            if out.get(key) != base[key]:
                out[key] = base[key]
                changes.append(f"{key} set")
        elif out[key] != base[key]:
            skipped.append(f"{key}: kept existing (use --force to replace)")

    return out, changes, skipped


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--config-dir", default=None,
                    help="defaults to $CLAUDE_CONFIG_DIR or ~/.claude")
    ap.add_argument("--force", action="store_true",
                    help="overwrite defaultMode/statusLine even if already set")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    import os
    cfg_dir = Path(args.config_dir or os.environ.get("CLAUDE_CONFIG_DIR")
                   or Path.home() / ".claude")
    target = cfg_dir / "settings.json"

    base = json.loads((HERE / "base.json").read_text())
    cur = json.loads(target.read_text()) if target.exists() else {}

    merged, changes, skipped = merge(base, cur, args.force)

    if not changes:
        print("Already up to date.")
    else:
        for c in changes:
            print(f"  + {c}")
    for s in skipped:
        print(f"  ~ {s}")

    if args.dry_run:
        print("\n(dry run, nothing written)")
        return 0
    if not changes:
        return 0

    cfg_dir.mkdir(parents=True, exist_ok=True)
    if target.exists():
        stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
        backup = target.with_suffix(f".json.bak-{stamp}")
        shutil.copy2(target, backup)
        print(f"\nBacked up {target} -> {backup.name}")

    target.write_text(json.dumps(merged, indent=2) + "\n")
    print(f"Wrote {target}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
