#!/usr/bin/env python3
"""Keep the Codex plugin's skills (plugins/sorted/skills/) identical to skills/, the one place to edit.

  python scripts/sync_codex_plugin.py           # copy skills/ into the Codex plugin
  python scripts/sync_codex_plugin.py --check   # change nothing; print "drift: N" and exit 1 when N > 0

It also checks that the three manifests (Claude Code plugin, Claude Code marketplace entry, Codex plugin) carry the same version.
A manifest with no version, or one that cannot be read, counts as drift, and every file and folder is compared (also names
such as tags or __pycache__, and a name that is a file on one side and a folder on the other).
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
PLUGIN_NAME = "sorted"


def marketplace_entry(d):
    """The marketplace's entry for this plugin, found by name (never by position)."""
    entries = [p for p in d["plugins"] if isinstance(p, dict) and p.get("name") == PLUGIN_NAME]
    if len(entries) != 1:
        raise ValueError("the marketplace must list exactly one plugin named %s, it lists %d" % (PLUGIN_NAME, len(entries)))
    return entries[0]


MANIFESTS = {
    "claude plugin": (os.path.join(ROOT, ".claude-plugin", "plugin.json"), lambda d: d.get("version")),
    "claude marketplace entry": (os.path.join(ROOT, ".claude-plugin", "marketplace.json"), lambda d: marketplace_entry(d).get("version")),
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
        # ignore=[] and hide=[]: by default dircmp skips names such as tags, RCS, CVS, .git and __pycache__, which the copy still carries.
        cmp = filecmp.dircmp(os.path.join(SRC, n), os.path.join(DST, n), ignore=[], hide=[])
        stack = [(cmp, n)]
        while stack:
            c, rel = stack.pop()
            problems += ["only in skills/%s: %s" % (rel, f) for f in c.left_only]
            problems += ["only in the Codex copy of %s: %s" % (rel, f) for f in c.right_only]
            # common_funny: the same name is a file on one side and a folder on the other, or cannot be read.
            problems += ["not the same kind in %s: %s (a file on one side, a folder on the other, or unreadable)" % (rel, f) for f in c.common_funny]
            _, mismatch, errors = filecmp.cmpfiles(c.left, c.right, c.common_files, shallow=False)
            problems += ["changed: %s/%s" % (rel, f) for f in mismatch + errors]
            stack += [(sub, rel + "/" + name) for name, sub in c.subdirs.items()]
    return problems


def versions():
    """Returns ({manifest: version}, problems). A manifest with no version, or one that cannot be read, is a problem: it is never
    counted as 'the same version everywhere'."""
    out, problems = {}, []
    for label, (path, get) in MANIFESTS.items():
        try:
            with open(path, encoding="utf-8") as fh:
                out[label] = get(json.load(fh))
        except (OSError, ValueError, KeyError, IndexError, TypeError) as e:
            out[label] = None
            problems.append("cannot read the version of the %s (%s: %s)" % (label, e.__class__.__name__, e))
            continue
        if not isinstance(out[label], str) or not out[label]:
            problems.append("the %s has no version" % label)
    return out, problems


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
    v, version_problems = versions()
    same = not version_problems and len(set(v.values())) == 1
    for p in version_problems:
        print("DRIFT  " + p)
    print("skills: %d in skills/, %d in the Codex plugin" % (len(skill_names(SRC)), len(skill_names(DST))))
    print("versions: %s (%s)" % (", ".join("%s %s" % kv for kv in v.items()), "same" if same else "INCOMPLETE" if version_problems else "DIFFERENT"))
    found = len(problems) + (len(version_problems) or (0 if same else 1))
    print("drift: %d" % found)
    return 1 if found else 0


if __name__ == "__main__":
    sys.exit(main())
