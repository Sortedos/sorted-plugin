#!/usr/bin/env python3
"""Keep the Codex plugin's skills (plugins/sorted/skills/) identical to skills/, the one place to edit.

  python scripts/sync_codex_plugin.py           # copy skills/ into the Codex plugin
  python scripts/sync_codex_plugin.py --check   # change nothing; print "drift: N" and exit 1 when N > 0

It also checks that the three manifests (Claude Code plugin, Claude Code marketplace entry, Codex plugin) carry the same version.
"""
import argparse
import filecmp
import json
import os
import shutil
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, "skills")
DST = os.path.join(ROOT, "plugins", "sorted", "skills")
MANIFESTS = {
    "claude plugin": (os.path.join(ROOT, ".claude-plugin", "plugin.json"), lambda d: d.get("version")),
    "claude marketplace entry": (os.path.join(ROOT, ".claude-plugin", "marketplace.json"), lambda d: d["plugins"][0].get("version")),
    "codex plugin": (os.path.join(ROOT, "plugins", "sorted", ".codex-plugin", "plugin.json"), lambda d: d.get("version")),
}


def skill_names(folder):
    if not os.path.isdir(folder):
        return []
    return sorted(d for d in os.listdir(folder) if os.path.isdir(os.path.join(folder, d)))


def drift():
    """Every difference between skills/ and the Codex copy: missing, extra or changed files."""
    problems = []
    src, dst = skill_names(SRC), skill_names(DST)
    problems += ["missing in the Codex plugin: %s" % n for n in src if n not in dst]
    problems += ["extra in the Codex plugin: %s" % n for n in dst if n not in src]
    for n in (n for n in src if n in dst):
        cmp = filecmp.dircmp(os.path.join(SRC, n), os.path.join(DST, n))
        stack = [(cmp, n)]
        while stack:
            c, rel = stack.pop()
            problems += ["only in skills/%s: %s" % (rel, f) for f in c.left_only]
            problems += ["only in the Codex copy of %s: %s" % (rel, f) for f in c.right_only]
            _, mismatch, errors = filecmp.cmpfiles(c.left, c.right, c.common_files, shallow=False)
            problems += ["changed: %s/%s" % (rel, f) for f in mismatch + errors]
            stack += [(sub, rel + "/" + name) for name, sub in c.subdirs.items()]
    return problems


def versions():
    out = {}
    for label, (path, get) in MANIFESTS.items():
        with open(path, encoding="utf-8") as fh:
            out[label] = get(json.load(fh))
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true", help="change nothing, report drift")
    a = ap.parse_args()
    if not a.check:
        names = skill_names(SRC)
        os.makedirs(DST, exist_ok=True)
        for old in skill_names(DST):
            if old not in names:
                shutil.rmtree(os.path.join(DST, old))
        for n in names:
            if os.path.isdir(os.path.join(DST, n)):
                shutil.rmtree(os.path.join(DST, n))
            shutil.copytree(os.path.join(SRC, n), os.path.join(DST, n))
        print("copied %d skills into plugins/sorted/skills" % len(names))
    problems = drift()
    for p in problems:
        print("DRIFT  " + p)
    v = versions()
    same = len(set(v.values())) == 1
    print("skills: %d in skills/, %d in the Codex plugin" % (len(skill_names(SRC)), len(skill_names(DST))))
    print("versions: %s (%s)" % (", ".join("%s %s" % kv for kv in v.items()), "same" if same else "DIFFERENT"))
    print("drift: %d" % (len(problems) + (0 if same else 1)))
    return 1 if problems or not same else 0


if __name__ == "__main__":
    sys.exit(main())
