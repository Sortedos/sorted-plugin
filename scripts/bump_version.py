#!/usr/bin/env python3
"""Set one version number in every place the plugin declares it, so the Claude Code plugin, its marketplace entry and the Codex
plugin never disagree.

  python scripts/bump_version.py 1.3.0 --dry-run   # show the files it would change
  python scripts/bump_version.py 1.3.0             # change them, then run: python scripts/sync_codex_plugin.py --check

Add a section for the new version to CHANGELOG.md by hand: what changed, in plain words.
"""
import argparse
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PLACES = [
    (os.path.join(".claude-plugin", "plugin.json"), lambda d, v: d.__setitem__("version", v), lambda d: d.get("version")),
    (os.path.join(".claude-plugin", "marketplace.json"), lambda d, v: d["plugins"][0].__setitem__("version", v), lambda d: d["plugins"][0].get("version")),
    (os.path.join("plugins", "sorted", ".codex-plugin", "plugin.json"), lambda d, v: d.__setitem__("version", v), lambda d: d.get("version")),
]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("version")
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()
    if not re.fullmatch(r"\d+\.\d+\.\d+", a.version):
        print("the version must look like 1.3.0")
        return 2
    for rel, setter, getter in PLACES:
        path = os.path.join(ROOT, rel)
        with open(path, encoding="utf-8") as fh:
            data = json.load(fh)
        old = getter(data)
        print("%s: %s -> %s%s" % (rel.replace("\\", "/"), old, a.version, " (dry run, unchanged)" if a.dry_run else ""))
        if not a.dry_run:
            setter(data, a.version)
            with open(path, "w", encoding="utf-8", newline="\n") as fh:  # no byte-order mark
                json.dump(data, fh, indent=2, ensure_ascii=False)
                fh.write("\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
