#!/usr/bin/env python3
"""Leak scan for this repository: run it before every commit and before the repository is ever made public.

What it looks for, in every file and in the whole git history (commit authors, messages, and every change ever committed,
including lines deleted later):
  1. Things shaped like secrets: API keys, webhook secrets, access tokens, "Bearer" tokens.
  2. Absolute paths into someone's personal folder on their computer (Windows, Linux or Mac user folders).
  3. Private hostnames: database, hosting, store and accounting addresses other than the public examples.
  4. Email addresses other than the example and no-reply ones.
  5. Every term in a PRIVATE deny-list (real customer, person and company names). The deny-list is passed in with
     --denylist and must live OUTSIDE this repository: a list of real names inside a public repository would itself be a leak.

It prints one line per hit (file, line, which rule) and never prints the matched text itself, so running the scan
cannot leak a secret into a log (a part of a file path that itself matches is printed as "<hidden part>"). It ends with
"hits: N" and exits 1 when N > 0. It exits 2, and an incomplete scan never passes, when the git history cannot be read, when
the folder has no .git of its own (so its history cannot be read), or when the deny-list cannot be read or holds no terms.

Usage:
  python scripts/scan_public.py --denylist <private list> [folder]   # folder defaults to the repository root
  python scripts/scan_public.py --denylist <private list> --no-history <folder>   # scan the files alone, on purpose
  python scripts/scan_public.py --selftest                           # proves the scan can fail (a planted fake secret must be found)

The deny-list is UTF-8 text, one term per line (a byte-order mark at the start is fine; a UTF-16 file is refused).
"""
import argparse
import contextlib
import io
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
    ("wsl-user-path", re.compile(r"(?<![\w.])/mnt/[a-z]/Users/(?!<)[A-Za-z0-9._-]+/", re.I)),  # a Windows profile seen from WSL
    ("root-home-path", re.compile(r"(?<![\w.])/root/(?!<)[A-Za-z0-9._-]+")),
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
ALLOWED_EMAILS = {"noreply@sortedos.com", "noreply@anthropic.com", "info@sortedos.com"}  # the last one is the public contact
ALLOWED_EMAIL_DOMAINS = {"example.com", "example.org", "example.net"}
ALLOWED_IPS = {"127.0.0.1", "0.0.0.0"}


def load_denylist(path):
    """The private list: one term per line, lines starting with # are comments. Returns the lower-cased terms."""
    terms = []
    # utf-8-sig drops the byte-order mark that Windows Notepad and PowerShell put at the start of a file; with plain utf-8 the
    # first term would start with an invisible character and could never match anything.
    with open(path, encoding="utf-8-sig") as fh:
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
        public = low
        for addr in ALLOWED_EMAILS:  # a published address is not a leak, even when a private term is part of it
            public = public.replace(addr, " ")
        for i, term in enumerate(terms):
            if term in public:
                hits.append((name, n, "denylist-term-%d" % (i + 1)))
    return hits


def iter_files(root):
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS]
        for fn in filenames:
            if fn == ".git":  # in a git worktree .git is a FILE that only points at the real folder; git never publishes a path named .git
                continue
            if os.path.splitext(fn)[1].lower() in SKIP_EXT:
                continue
            yield os.path.join(dirpath, fn)


def git_history(root):
    """Everything a public repository publishes besides its current files: commit authors, committers and messages, and
    the content of every commit (a secret committed once and deleted later is still in the history).
    Returns (text, status); text is None when the history could not be read. That includes a folder with no .git of its own
    (a subfolder, or a copy exported without .git): the history that gets published is then unknown, so the scan is incomplete."""
    if not os.path.exists(os.path.join(root, ".git")):  # .git is a folder, or a file in a git worktree
        return None, "not scanned (this folder has no .git of its own, so its history cannot be read; use --no-history to scan the files alone on purpose)"
    git = ["git", "-c", "core.quotePath=false", "-C", root]
    texts = []
    try:
        # -m: git log shows NO change for a merge commit unless told to, and a secret that exists only in a merge (a conflict
        # resolution) would otherwise never be read.
        for args in (["log", "--all", "--format=%an <%ae>%n%cn <%ce>%n%B"],
                     ["log", "--all", "-m", "-p", "--format=", "--no-color", "--no-ext-diff", "--no-textconv"],
                     ["rev-list", "--all", "--count"]):
            out = subprocess.run(git + args, capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=300)
            if out.returncode != 0:
                return None, "could not be read (git %s ended with code %d)" % (args[0], out.returncode)
            texts.append(out.stdout)
    except (OSError, subprocess.SubprocessError) as e:
        return None, "could not be read (%s)" % e.__class__.__name__
    return texts[0] + "\n" + texts[1], "scanned (%s commits, with every file change)" % texts[2].strip()


def printable_path(rel, terms):
    """A path as it may be printed. A part of a path (a folder or file name) can hold the very text a rule found, such as a
    customer name or a key, and the scan never prints matched text, so a part that matches on its own is replaced."""
    shown = "/".join("<hidden part>" if scan_text("", part, terms) else part for part in rel.split("/"))
    return "<hidden path>" if scan_text("", shown, terms) else shown  # the second test catches a match that spans two parts


def scan(root, terms, use_history=True):
    """Returns (files scanned, hits, history status, history readable)."""
    hits = []
    files = 0
    for path in iter_files(root):
        rel = os.path.relpath(path, root).replace("\\", "/")
        try:
            if os.path.getsize(path) > MAX_BYTES:
                hits.append((printable_path(rel, terms), 0, "file-too-large-to-scan"))
                continue
            with open(path, encoding="utf-8", errors="replace") as fh:
                text = fh.read()
        except OSError:
            hits.append((printable_path(rel, terms), 0, "unreadable-file"))
            continue
        files += 1
        in_file, in_name = scan_text("", text, terms), scan_text("", rel, terms)  # the file NAME is published too
        if in_file or in_name:
            shown = printable_path(rel, terms)
            hits.extend((shown, n, rule) for _, n, rule in in_file)
            hits.extend(("(file name) " + shown, n, rule) for _, n, rule in in_name)
    if use_history:
        history, status = git_history(root)
    else:
        history, status = "", "not scanned (--no-history was given, so only the files were read)"
    if history:
        hits.extend(scan_text("(git history)", history, terms))
    return files, hits, status, history is not None


def report(files, hits, status):
    for name, line, rule in hits:
        print("HIT  %s:%d  %s" % (name, line, rule))
    print("files scanned: %d" % files)
    print("git history: %s" % status)
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
        files, hits, status, _ = scan(tmp, terms, use_history=False)
        report(files, hits, status)
        rules = {r for _, _, r in hits}
        planted_ok = "secret-key" in rules and "denylist-term-1" in rules
        clean_ok = not any(n == "clean.md" for n, _, _ in hits)
    history_ok = history_selftest(fake)
    print("selftest: planted secret found=%s, planted name found=%s, clean file clean=%s, deleted secret found in history=%s"
          % ("secret-key" in rules, "denylist-term-1" in rules, clean_ok, history_ok))
    # None means the check needs git and git is not installed.
    more = [
        ("a secret that exists only in a merge commit is found in the history", merge_selftest(fake)),
        ("a worktree's .git file (a pointer into a user folder) is not reported", worktree_selftest()),
        ("a matching file or folder name is never printed", printing_selftest(fake)),
        ("WSL, root and home paths are flagged, look-alikes are not", rules_selftest()),
        ("deny-list: byte-order mark read, first term found; empty, UTF-16 and missing lists refused", denylist_selftest()),
        ("a folder with no .git of its own is an incomplete scan unless --no-history", nohistory_selftest()),
    ]
    for label, ok in more:
        print("selftest: %s: %s" % (label, "not run (git is not installed)" if ok is None else "ok" if ok else "FAILED"))
    failed = [label for label, ok in more if ok is False]
    print("selftest: %d of %d further checks passed" % (sum(ok is True for _, ok in more), len(more)))
    return 0 if planted_ok and clean_ok and history_ok is not False and not failed else 1


def quiet(fn, *args):
    """Runs fn with its printing captured. Returns (result, what it printed)."""
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        result = fn(*args)
    return result, buf.getvalue()


def write_file(folder, name, data):
    path = os.path.join(folder, name)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "wb") as fh:
        fh.write(data if isinstance(data, bytes) else data.encode("utf-8"))
    return path


def git_runner(folder):
    """Returns a function that runs git in folder with a fixed author and no signing; it raises when git fails or is missing."""
    base = ["git", "-c", "user.name=Selftest", "-c", "user.email=selftest@example.com", "-c", "commit.gpgsign=false", "-C", folder]
    return lambda *args: subprocess.run(base + list(args), check=True, capture_output=True, timeout=60)


def merge_selftest(fake):
    """A secret that exists only in merge commits (typed while resolving one merge, taken out by another) must still be found.
    git log shows no change at all for a merge commit unless it is told to (-m)."""
    with tempfile.TemporaryDirectory() as tmp:
        git = git_runner(tmp)
        try:
            git("init", "-q")
            git("checkout", "-q", "-b", "trunk")
            write_file(tmp, "base.md", "base\n")
            git("add", "base.md")
            git("commit", "-q", "-m", "base")
            git("checkout", "-q", "-b", "side")
            write_file(tmp, "side.md", "work on the side branch\n")
            git("add", "side.md")
            git("commit", "-q", "-m", "side work")
            git("checkout", "-q", "trunk")
            write_file(tmp, "trunk.md", "work on the trunk\n")
            git("add", "trunk.md")
            git("commit", "-q", "-m", "trunk work")
            git("merge", "-q", "--no-ff", "--no-commit", "side")
            write_file(tmp, "resolved.md", "key = '%s'\n" % fake)  # exists only in the merge
            git("add", "resolved.md")
            git("commit", "-q", "-m", "merge side")
            # The secret is taken out again by a second merge, so no ordinary commit ever shows it, in either direction.
            git("checkout", "-q", "-b", "side2", "side")
            write_file(tmp, "side2.md", "more work on a second branch\n")
            git("add", "side2.md")
            git("commit", "-q", "-m", "side2 work")
            git("checkout", "-q", "trunk")
            git("merge", "-q", "--no-ff", "--no-commit", "side2")
            git("rm", "-q", "resolved.md")
            git("commit", "-q", "-m", "merge side2")
            merges = git("rev-list", "--merges", "--count", "HEAD").stdout.decode().strip()
        except (OSError, subprocess.SubprocessError):
            return None
        _, hits, _, readable = scan(tmp, [])
        return merges == "2" and readable and any(n == "(git history)" and r == "secret-key" for n, _, r in hits) \
            and not any(n == "resolved.md" for n, _, _ in hits)


def worktree_selftest():
    """In a git worktree .git is a FILE holding the path of the real repository, which sits in someone's user folder. It must not
    be reported, and the history must still be read through it. Returns None when git is not installed."""
    with tempfile.TemporaryDirectory() as tmp:
        write_file(tmp, ".git", "gitdir: C:/Us" + "ers/someone/repo/.git/worktrees/w\n")  # assembled: this file holds no user path
        write_file(tmp, "clean.md", "fine\n")
        pointer_ok = not scan(tmp, [], use_history=False)[1]
    with tempfile.TemporaryDirectory() as tmp:
        git = git_runner(os.path.join(tmp, "main"))
        try:
            os.makedirs(os.path.join(tmp, "main"))
            git("init", "-q")
            write_file(os.path.join(tmp, "main"), "a.md", "fine\n")
            git("add", "a.md")
            git("commit", "-q", "-m", "first")
            git("worktree", "add", "-q", os.path.join(tmp, "wt"), "-b", "other")
        except (OSError, subprocess.SubprocessError):
            return None if pointer_ok else False
        if not os.path.isfile(os.path.join(tmp, "wt", ".git")):
            return False
        _, hits, _, readable = scan(os.path.join(tmp, "wt"), [])
        return pointer_ok and readable and not hits


def printing_selftest(fake):
    """A file or folder name that matches a rule is reported, but the matching text must never reach the printed report."""
    with tempfile.TemporaryDirectory() as tmp:
        for rel in (fake + ".md", "plantedcustomer-notes.md", "plantedcustomer-folder/inside.md"):
            write_file(tmp, rel, "nothing here\n")
        write_file(tmp, "plain.md", "owner: Plantedcustomer Ltd\n")
        files, hits, status, _ = scan(tmp, ["plantedcustomer"], use_history=False)
        _, printed = quiet(report, files, hits, status)
        named = [n for n, _, _ in hits if n.startswith("(file name)")]
        return len(named) >= 3 and "plantedcustomer" not in printed.lower() and fake not in printed and "plain.md:1" in printed


def rules_selftest():
    """Paths that must be flagged by their own rule, and look-alikes that must not be. Assembled at run time: this file holds no path."""
    flagged = [
        ("wsl-user-path", "open /mnt" + "/c/Users/bob/notes/"),
        ("root-home-path", "cd /ro" + "ot/work"),
        ("unix-home-path", "cd /ho" + "me/bob/x/"),
        ("windows-user-path", "C:" + "\\Users\\bob\\x"),
    ]
    clean = ["https://example.com/api/root/page", "the root folder", "/mnt" + "/c/Users/<name>/x/"]
    return all(rule in {r for _, _, r in scan_text("x", text, [])} for rule, text in flagged) \
        and not any(scan_text("x", text, []) for text in clean)


def denylist_selftest():
    """A deny-list saved with a byte-order mark must still find its FIRST term, and a list that cannot work must stop the scan."""
    with tempfile.TemporaryDirectory() as tmp:
        bom = write_file(tmp, "bom.txt", b"\xef\xbb\xbfAcme\n# a comment\nBeta\n")
        utf16 = write_file(tmp, "utf16.txt", "Acme\nBeta\n".encode("utf-16"))
        empty = write_file(tmp, "empty.txt", b"")
        comments = write_file(tmp, "comments.txt", b"# only a comment\n\n")
        write_file(tmp, "scanned/clean.md", "nothing\n")
        scanned = os.path.join(tmp, "scanned")
        try:
            load_denylist(utf16)
            utf16_refused = False
        except ValueError:
            utf16_refused = True
        loaded = load_denylist(bom) == ["acme", "beta"]
        refused = [quiet(run_scan, scanned, p, False)[0] for p in (empty, comments, utf16, os.path.join(tmp, "missing.txt"))] == [2, 2, 2, 2]
        write_file(tmp, "scanned/planted.md", "owner: Acme Ltd\n")
        code, printed = quiet(run_scan, scanned, bom, False)
        return loaded and utf16_refused and refused and code == 1 and "denylist-term-1" in printed and "deny-list terms loaded: 2" in printed


def nohistory_selftest():
    """A folder with no .git of its own (a subfolder, or a copy exported without .git) has no readable history: that is exit 2."""
    with tempfile.TemporaryDirectory() as tmp:
        deny = write_file(tmp, "deny.txt", "never-matches-anything\n")
        write_file(tmp, "plain/clean.md", "nothing\n")
        plain = os.path.join(tmp, "plain")
        return quiet(run_scan, plain, deny, True)[0] == 2 and quiet(run_scan, plain, deny, False)[0] == 0


def history_selftest(fake):
    """A secret committed and then deleted must still be found in the history. Returns None when git is not installed."""
    with tempfile.TemporaryDirectory() as tmp:
        git = ["git", "-c", "user.name=Selftest", "-c", "user.email=selftest@example.com", "-c", "commit.gpgsign=false", "-C", tmp]
        try:
            subprocess.run(git + ["init", "-q"], check=True, capture_output=True, timeout=60)
            with open(os.path.join(tmp, "notes.md"), "w", encoding="utf-8") as fh:
                fh.write("key = '%s'\n" % fake)
            subprocess.run(git + ["add", "notes.md"], check=True, capture_output=True, timeout=60)
            subprocess.run(git + ["commit", "-q", "-m", "add notes"], check=True, capture_output=True, timeout=60)
            with open(os.path.join(tmp, "notes.md"), "w", encoding="utf-8") as fh:
                fh.write("no key here\n")
            subprocess.run(git + ["commit", "-q", "-am", "remove the key"], check=True, capture_output=True, timeout=60)
        except (OSError, subprocess.SubprocessError):
            return None
        _, hits, _, readable = scan(tmp, [])
        return readable and any(n == "(git history)" and r == "secret-key" for n, _, r in hits) \
            and not any(n == "notes.md" for n, _, _ in hits)


def run_scan(folder, denylist, use_history=True):
    """The real scan. Returns the exit code: 0 clean, 1 hits, 2 the scan could not be completed (and so never passes)."""
    folder = os.path.abspath(folder)
    denylist = os.path.abspath(denylist)
    if denylist.lower().startswith(folder.lower() + os.sep):
        print("The deny-list must live OUTSIDE the folder being scanned.")
        return 2
    try:
        terms = load_denylist(denylist)
    except (OSError, ValueError) as e:  # ValueError includes a file that is not UTF-8 text, such as one PowerShell saved as UTF-16
        print("The deny-list could not be read (%s; it must be a UTF-8 text file), so the scan cannot run." % e.__class__.__name__)
        return 2
    print("deny-list terms loaded: %d" % len(terms))
    if not terms:
        print("The deny-list holds no terms, so the scan would look for no names at all.")
        return 2
    files, hits, status, readable = scan(folder, terms, use_history)
    report(files, hits, status)
    if not readable:
        print("The git history could not be read, so the scan is incomplete.")
        return 2
    return 1 if hits else 0


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("folder", nargs="?", default=os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    ap.add_argument("--denylist", help="path to the PRIVATE deny-list (one term per line), kept outside this repository")
    ap.add_argument("--no-history", action="store_true",
                    help="scan the files only. Without this, a folder with no .git of its own is an incomplete scan (exit 2)")
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args()
    if a.selftest:
        return selftest()
    if not a.denylist:
        print("--denylist is required (the private list of real names, kept outside this repository)")
        return 2
    return run_scan(a.folder, a.denylist, not a.no_history)


if __name__ == "__main__":
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8", errors="replace")
    sys.exit(main())
