#!/usr/bin/env python3
"""Run every check of this repository in one go, and print one line per check plus a total.

  python scripts/check_all.py

Checks, in order:
  1. leak scan            scripts/scan_public.py with the private deny-list named in the SORTED_DENYLIST environment
                          variable (the list stays outside the repository); without it, only the scan's self-test runs
  2. skill lint           scripts/lint_skills.mjs
  3. Codex copy           scripts/sync_codex_plugin.py --check (no drift, same version in every manifest)
  4. tool names           every feed tool named in the docs and skills is one of the four in docs/feed-tools.json
  5. byte-order marks     no JSON file starts with one (Claude Code then loads no servers from .mcp.json)
  6. plugin validation    claude plugin validate . --strict (skipped, with a notice, when Claude Code is not installed)
Exit code 1 if any check failed.
"""
import glob
import json
import os
import re
import shutil
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def run(cmd):
    p = subprocess.run(cmd, cwd=ROOT, capture_output=True, text=True, encoding="utf-8", errors="replace", shell=False)
    out = (p.stdout + p.stderr).strip().splitlines()
    return p.returncode, (out[-1] if out else "")


def check_leaks():
    deny = os.environ.get("SORTED_DENYLIST")
    if deny:
        code, last = run([sys.executable, "scripts/scan_public.py", "--denylist", deny, ROOT])
        return code == 0, last
    code, last = run([sys.executable, "scripts/scan_public.py", "--selftest"])
    return code == 0, "self-test only (set SORTED_DENYLIST to scan for real names): " + last


def check_lint():
    node = shutil.which("node")
    if not node:
        return None, "skipped: Node.js is not installed"
    code, last = run([node, "scripts/lint_skills.mjs"])
    return code == 0, last


def check_codex_copy():
    code, last = run([sys.executable, "scripts/sync_codex_plugin.py", "--check"])
    return code == 0, last


def check_tool_names():
    with open(os.path.join(ROOT, "docs", "feed-tools.json"), encoding="utf-8") as fh:
        feed = {t["name"] for t in json.load(fh)["tools"]}
    files = glob.glob(os.path.join(ROOT, "skills", "*", "SKILL.md")) + glob.glob(os.path.join(ROOT, "docs", "*.md")) + [os.path.join(ROOT, "README.md")]
    bad = set()
    for f in files:
        text = open(f, encoding="utf-8").read()
        for name in re.findall(r"`((?:define|feed|list|end)_feeds?|feed_[a-z]+|[a-z]+_feeds?)`", text):
            if name not in feed:
                bad.add(name)
    return not bad, "feed tool names checked in %d files; unknown: %s" % (len(files), ", ".join(sorted(bad)) or "none")


def check_bom():
    files = []
    for dirpath, dirnames, filenames in os.walk(ROOT):  # os.walk also enters hidden folders (.claude-plugin, .agents), glob does not
        dirnames[:] = [d for d in dirnames if d not in (".git", "node_modules")]
        files += [os.path.join(dirpath, f) for f in filenames if f.endswith(".json")]
    files = sorted(files)
    with_bom = [os.path.relpath(f, ROOT) for f in files if open(f, "rb").read(3) == b"\xef\xbb\xbf"]
    return not with_bom, "JSON files without a byte-order mark: %d of %d%s" % (len(files) - len(with_bom), len(files), (" (" + ", ".join(with_bom) + ")") if with_bom else "")


def check_validate():
    claude = shutil.which("claude")
    if not claude:
        return None, "skipped: Claude Code is not installed"
    code, last = run([claude, "plugin", "validate", ".", "--strict"])
    return code == 0, last


def main():
    checks = [("leak scan", check_leaks), ("skill lint", check_lint), ("Codex copy", check_codex_copy),
              ("tool names", check_tool_names), ("byte-order marks", check_bom), ("plugin validation", check_validate)]
    passed = failed = skipped = 0
    for name, fn in checks:
        try:
            ok, detail = fn()
        except Exception as e:  # a check that crashes is a failed check, never a silent pass
            ok, detail = False, "crashed: %s" % e
        if ok is None:
            skipped += 1
            print("SKIP  %-18s %s" % (name, detail))
        elif ok:
            passed += 1
            print("PASS  %-18s %s" % (name, detail))
        else:
            failed += 1
            print("FAIL  %-18s %s" % (name, detail))
    print("checks: %d passed, %d failed, %d skipped" % (passed, failed, skipped))
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
