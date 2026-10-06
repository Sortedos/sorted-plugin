#!/usr/bin/env python3
"""Leak scan for this repository: run it before every commit and before the repository is ever made public.

What it looks for, in every file and in the git history (commit authors and messages):
  1. Things shaped like secrets: API keys, webhook secrets, access tokens, "Bearer" tokens.
  2. Absolute paths into someone's personal folder on their computer (Windows, Linux or Mac user folders).
  3. Private hostnames: database, hosting, store and accounting addresses other than the public examples.
  4. Email addresses other than the example and no-reply ones.
  5. Every term in a PRIVATE deny-list (real customer, person and company names). The deny-list is passed in with
     --denylist and must live OUTSIDE this repository: a list of real names inside a public repository would itself be a leak.

It prints one line per hit (file, line, which rule) and never prints the matched text itself, so running the scan
cannot leak a secret into a log. It ends with "hits: N" and exits 1 when N > 0.

Usage:
  python scripts/scan_public.py --denylist <private list> [folder]   # folder defaults to the repository root
  python scripts/scan_public.py --selftest                           # proves the scan can fail (a planted fake secret must be found)
"""
import argparse
import os
import re
import subprocess
import sys
import tempfile

SKIP_DIRS = {".git", "node_modules", "dist", "__pycache__"}
SKIP_EXT = {".png", ".jpg", ".jpeg", ".gif", ".ico", ".zip", ".pdf", ".woff", ".woff2", ".ttf"}
MAX_BYTES = 2_000_000

# Rule name -> pattern. Each pattern needs a real token after a prefix, so a sentence that explains
# "your key starts with srt_" is not a hit, but a pasted key is.
TOKEN = r"[A-Za-z0-9]{16,}"
RULES = [
    ("secret-key", re.compile(r"\b(?:sk|rk)_(?:live|test)_" + TOKEN)),
    ("publishable-key", re.compile(r"\bpk_(?:live|test)_" + TOKEN)),
    ("webhook-secret", re.compile(r"\bwhsec_" + TOKEN)),
    ("sorted-key", re.compile(r"\bsr[tf]_[A-Za-z0-9_-]{16,}")),
    ("bearer-token", re.compile(r"\bBearer\s+[A-Za-z0-9._~+/=-]{20,}")),
    ("github-token", re.compile(r"\b(?:gh[pousr]_[A-Za-z0-9]{20,}|github_pat_[A-Za-z0-9_]{20,})")),
    ("google-key", re.compile(r"\bAIza[0-9A-Za-z_-]{30,}")),
    ("slack-or-meta-token", re.compile(r"\b(?:xox[abpr]-[A-Za-z0-9-]{10,}|EAA[A-Za-z0-9]{30,})")),
    ("aws-key", re.compile(r"\bAKIA[0-9A-Z]{16}\b")),
    ("private-key-block", re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----")),
    ("jwt", re.compile(r"\beyJ[A-Za-z0-9_-]{10,}\.eyJ[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}")),
    ("windows-user-path", re.compile(r"[A-Za-z]:[\\/]+Users[\\/]+", re.I)),
    ("unix-home-path", re.compile(r"(?<![\w.])/(?:home|Users)/(?!<)[A-Za-z0-9._-]+/")),
    ("database-host", re.compile(r"\b[a-z0-9-]+\.(?:supabase\.co|pooler\.supabase\.com|neon\.tech|rds\.amazonaws\.com)\b", re.I)),
    ("hosting-host", re.compile(r"\b[a-z0-9-]+\.(?:vercel\.app|netlify\.app|herokuapp\.com|onrender\.com|fly\.dev)\b", re.I)),
    ("ip-address", re.compile(r"\b(?:\d{1,3}\.){3}\d{1,3}\b")),
]
# Hostnames that are only examples (allowed) for the store and accounting systems the skills explain.
EXAMPLE_SUBDOMAINS = {"example", "yourcompany", "yourstore", "your-store", "acme", "mycompany", "mystore", "company", "store"}
SUBDOMAIN_RULES = [
    ("odoo-host", re.compile(r"\b([a-z0-9-]+)\.odoo\.com\b", re.I)),
    ("shopify-host", re.compile(r"\b([a-z0-9-]+)\.myshopify\.com\b", re.I)),
]
EMAIL = re.compile(r"\b[A-Za-z0-9._%+-]+@([A-Za-z0-9-]+\.)+[A-Za-z]{2,}\b")
ALLOWED_EMAILS = {"noreply@sortedos.com", "noreply@anthropic.com"}
ALLOWED_EMAIL_DOMAINS = {"example.com", "example.org", "example.net"}
ALLOWED_IPS = {"127.0.0.1", "0.0.0.0"}


def load_denylist(path):
    terms = []
    with open(path, encoding="utf-8") as fh:
        for raw in fh:
            line = raw.strip()
            if line and not line.startswith("#"):
                terms.append(line.lower())
    return terms


def scan_text(name, text, terms):
    hits = []
    for n, line in enumerate(text.splitlines(), 1):
        low = line.lower()
        for rule, pat in RULES:
            for m in pat.finditer(line):
                if rule == "ip-address" and m.group(0) in ALLOWED_IPS:
                    continue
                if rule == "ip-address" and not all(0 <= int(p) <= 255 for p in m.group(0).split(".")):
                    continue
                hits.append((name, n, rule))
        for rule, pat in SUBDOMAIN_RULES:
            for m in pat.finditer(line):
                if m.group(1).lower() not in EXAMPLE_SUBDOMAINS:
                    hits.append((name, n, rule))
        for m in EMAIL.finditer(line):
            addr = m.group(0).lower()
            if addr in ALLOWED_EMAILS or addr.split("@", 1)[1] in ALLOWED_EMAIL_DOMAINS:
                continue
            hits.append((name, n, "email-address"))
        for i, term in enumerate(terms):
            if term in low:
                hits.append((name, n, "denylist-term-%d" % (i + 1)))
    return hits


def iter_files(root):
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS]
        for fn in filenames:
            if os.path.splitext(fn)[1].lower() in SKIP_EXT:
                continue
            yield os.path.join(dirpath, fn)


def git_history(root):
    """Commit authors, committers and messages: a public repository publishes all of them."""
    if not os.path.isdir(os.path.join(root, ".git")):
        return ""
    try:
        out = subprocess.run(["git", "-C", root, "log", "--all", "--format=%an <%ae>%n%cn <%ce>%n%B"],
                             capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=60)
        return out.stdout
    except (OSError, subprocess.SubprocessError):
        return ""


def scan(root, terms):
    hits = []
    files = 0
    for path in iter_files(root):
        try:
            if os.path.getsize(path) > MAX_BYTES:
                hits.append((os.path.relpath(path, root), 0, "file-too-large-to-scan"))
                continue
            with open(path, encoding="utf-8", errors="replace") as fh:
                text = fh.read()
        except OSError:
            hits.append((os.path.relpath(path, root), 0, "unreadable-file"))
            continue
        files += 1
        hits.extend(scan_text(os.path.relpath(path, root).replace("\\", "/"), text, terms))
        # The file NAME is published too.
        hits.extend(scan_text("(file name) " + os.path.relpath(path, root).replace("\\", "/"),
                              os.path.relpath(path, root), terms))
    hits.extend(scan_text("(git history)", git_history(root), terms))
    return files, hits


def report(files, hits):
    for name, line, rule in hits:
        print("HIT  %s:%d  %s" % (name, line, rule))
    print("files scanned: %d" % files)
    print("hits: %d" % len(hits))


def selftest():
    """Negative control: a folder holding a planted fake key and a planted deny-listed name MUST produce hits."""
    with tempfile.TemporaryDirectory() as tmp:
        fake = "sk_" + "live_" + "Z9" * 12  # built at run time so this file itself holds no key-shaped text
        with open(os.path.join(tmp, "planted.md"), "w", encoding="utf-8") as fh:
            fh.write("config = '%s'\nowner: Plantedcustomer Ltd\n" % fake)
        with open(os.path.join(tmp, "clean.md"), "w", encoding="utf-8") as fh:
            fh.write("Your key starts with srt_ and you paste it yourself.\nhttps://yourcompany.odoo.com\n")
        terms = ["plantedcustomer"]
        files, hits = scan(tmp, terms)
        report(files, hits)
        rules = {r for _, _, r in hits}
        planted_ok = "secret-key" in rules and "denylist-term-1" in rules
        clean_ok = not any(n == "clean.md" for n, _, _ in hits)
        print("selftest: planted secret found=%s, planted name found=%s, clean file clean=%s"
              % ("secret-key" in rules, "denylist-term-1" in rules, clean_ok))
        return 0 if planted_ok and clean_ok else 1


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("folder", nargs="?", default=os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    ap.add_argument("--denylist", help="path to the PRIVATE deny-list (one term per line), kept outside this repository")
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args()
    if a.selftest:
        return selftest()
    if not a.denylist:
        print("--denylist is required (the private list of real names, kept outside this repository)")
        return 2
    denylist = os.path.abspath(a.denylist)
    folder = os.path.abspath(a.folder)
    if denylist.lower().startswith(folder.lower() + os.sep):
        print("The deny-list must live OUTSIDE the folder being scanned.")
        return 2
    files, hits = scan(folder, load_denylist(denylist))
    report(files, hits)
    return 1 if hits else 0


if __name__ == "__main__":
    sys.exit(main())
