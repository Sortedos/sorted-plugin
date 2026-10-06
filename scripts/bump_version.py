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
PLUGIN_NAME = "sorted"


def marketplace_entry(d):
    """The marketplace's entry for this plugin, found by name (never by position), the same way sync_codex_plugin.py finds it."""
    entries = [p for p in d["plugins"] if isinstance(p, dict) and p.get("name") == PLUGIN_NAME]
    if len(entries) != 1:
        raise ValueError("the marketplace must list exactly one plugin named %s, it lists %d" % (PLUGIN_NAME, len(entries)))
    return entries[0]


PLACES = [
    (os.path.join(".claude-plugin", "plugin.json"), lambda d, v: d.__setitem__("version", v), lambda d: d.get("version")),
    (os.path.join(".claude-plugin", "marketplace.json"), lambda d, v: marketplace_entry(d).__setitem__("version", v), lambda d: marketplace_entry(d).get("version")),
    (os.path.join("plugins", "sorted", ".codex-plugin", "plugin.json"), lambda d, v: d.__setitem__("version", v), lambda d: d.get("version")),
]


def new_text_for(text, setter, getter, version):
    """The file's text with the new version in it, worked out without touching the file. Raises when the file does not have the
    shape this script expects (no version place at all, a missing "plugins" list, text that is not JSON)."""
    data = json.loads(text)
    old = getter(data)
    # Change only the version text, so the rest of the file keeps its layout and the change stays one line.
    pattern = re.compile(r'("version"\s*:\s*")' + re.escape(str(old)) + r'"')
    new_text, n = pattern.subn(lambda m: m.group(1) + version + '"', text)
    if n != 1 or getter(json.loads(new_text)) != version:  # not exactly one place: rewrite the whole file instead
        setter(data, version)
        new_text = json.dumps(data, indent=2, ensure_ascii=False) + "\n"
    return old, new_text


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("version")
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()
    # [0-9], not \d: in Python \d also matches Arabic-Indic and other Unicode digits, and nothing downstream would catch them
    # (Claude Code treats a plugin version as plain text).
    if not re.fullmatch(r"[0-9]+\.[0-9]+\.[0-9]+", a.version):
        print("the version must look like 1.3.0 (digits 0 to 9 only)")
        return 2
    # Work out all three new texts first: a file that cannot be changed must be found before any file is written, or the three
    # manifests would end up disagreeing.
    changes = []
    for rel, setter, getter in PLACES:
        path = os.path.join(ROOT, rel)
        try:
            with open(path, encoding="utf-8", newline="") as fh:
                old, new_text = new_text_for(fh.read(), setter, getter, a.version)
        except (OSError, ValueError, KeyError, IndexError, TypeError) as e:
            print("%s cannot be changed (%s: %s). Nothing was written." % (rel.replace("\\", "/"), e.__class__.__name__, e))
            return 2
        print("%s: %s -> %s%s" % (rel.replace("\\", "/"), old, a.version, " (dry run, unchanged)" if a.dry_run else ""))
        changes.append((rel, path, new_text))
    if a.dry_run:
        return 0
    locked = [rel for rel, path, _ in changes if not os.access(path, os.W_OK)]
    if locked:
        print("%s cannot be written to. Nothing was written." % ", ".join(r.replace("\\", "/") for r in locked))
        return 2
    for done, (rel, path, new_text) in enumerate(changes):
        try:
            with open(path, "w", encoding="utf-8", newline="") as fh:  # no byte-order mark
                fh.write(new_text)
        except OSError as e:
            print("stopped at %s (%s): %d of %d files were already changed, so the manifests now disagree. Fix the cause and run this again."
                  % (rel.replace("\\", "/"), e.__class__.__name__, done, len(changes)))
            return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
