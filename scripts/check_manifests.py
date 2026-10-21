#!/usr/bin/env python3
"""Check that nothing but plain text and the one expected connection can ship inside this plugin.

  python scripts/check_manifests.py

Why: a client who installs this repository gets whatever is on the main branch. The two worst changes a stranger (or a stolen login)
could make are (a) pointing the connection at another server, so that every client's sign-in or personal key goes there, and (b) adding
something that RUNS on the client's computer (a hook, a command, a script the plugin starts). This check fails on both. It is only a
real guard when it is a required check on main (see SECURITY.md); on its own it cannot stop anyone who can push without review.

It checks:
  1. both .mcp.json files declare exactly one server, named sorted, whose address is https://sortedos.com/api/mcp and which has no
     command, arguments, environment, headers or any other key (the Codex copy has no environment variable or personal key either: Codex signs in with OAuth)
  2. both marketplace files list only this folder as the source (no other repository, no download)
  3. the three plugin manifests carry no key that loads code (hooks, commands, agents, servers of their own, scripts)
  4. the plugin carries only the files in the allowlist below: manifests, .mcp.json and skills/<name>/SKILL.md (nothing that runs)
Exit code 1 if any check failed.
"""
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
URL = "https://sortedos.com/api/mcp"
MANIFEST_KEYS_OK = {"name", "version", "license", "description", "author", "homepage", "keywords", "skills", "interface", "owner", "plugins",
                    # directory listing fields: https addresses and one icon path, read by the plugin directory, never loaded as code
                    "displayName", "repository", "icon", "documentationUrl", "supportUrl", "privacyPolicyUrl", "termsOfServiceUrl"}
SERVER_KEYS_OK = {
    ".mcp.json": {"type", "url"},
    os.path.join("plugins", "sorted", ".mcp.json"): {"type", "url"},
}
# Everything a published plugin may hold. A hooks, commands, agents, bin, monitors or settings file is not on this list on purpose.
PLUGIN_FILES_OK = {os.path.join(".codex-plugin", "plugin.json"), ".mcp.json"}


def load(rel):
    with open(os.path.join(ROOT, rel), encoding="utf-8") as fh:
        return json.load(fh)


def check_servers(problems):
    for rel, allowed in SERVER_KEYS_OK.items():
        servers = load(rel).get("mcpServers", {})
        if list(servers) != ["sorted"]:
            problems.append("%s: must declare exactly one server named sorted, found %s" % (rel, list(servers)))
            continue
        s = servers["sorted"]
        extra = set(s) - allowed
        if extra:
            problems.append("%s: the sorted server has keys that are not allowed: %s" % (rel, ", ".join(sorted(extra))))
        if s.get("url") != URL:
            problems.append("%s: the server address must be exactly %s, found %r" % (rel, URL, s.get("url")))


def check_marketplaces(problems):
    entries = load(os.path.join(".claude-plugin", "marketplace.json")).get("plugins", [])
    for e in entries:
        if e.get("source") != "./":
            problems.append(".claude-plugin/marketplace.json: source must be \"./\", found %r" % (e.get("source"),))
    entries = load(os.path.join(".agents", "plugins", "marketplace.json")).get("plugins", [])
    for e in entries:
        src = e.get("source")
        if not (isinstance(src, dict) and src.get("source") == "local" and src.get("path") == "./plugins/sorted"):
            problems.append(".agents/plugins/marketplace.json: source must be the local folder ./plugins/sorted, found %r" % (src,))


def check_manifest_keys(problems):
    for rel in (os.path.join(".claude-plugin", "plugin.json"), os.path.join(".claude-plugin", "marketplace.json"),
                os.path.join("plugins", "sorted", ".codex-plugin", "plugin.json")):
        extra = set(load(rel)) - MANIFEST_KEYS_OK
        if extra:
            problems.append("%s: keys that could load code or servers are not allowed: %s" % (rel.replace("\\", "/"), ", ".join(sorted(extra))))


def check_files(problems):
    base = os.path.join(ROOT, "plugins", "sorted")
    for dirpath, dirnames, filenames in os.walk(base):
        for f in filenames:
            rel = os.path.relpath(os.path.join(dirpath, f), base)
            parts = rel.split(os.sep)
            if rel in PLUGIN_FILES_OK or (len(parts) == 3 and parts[0] == "skills" and parts[2] == "SKILL.md"):
                continue
            problems.append("plugins/sorted/%s is not an allowed plugin file (only manifests, .mcp.json and skills/<name>/SKILL.md)" % rel.replace("\\", "/"))
    # The Claude Code plugin is the repository root: no code-loading folders or files there either.
    for name in ("hooks", "commands", "agents", "bin", "monitors", "output-styles", "settings.json", "hooks.json"):
        if os.path.exists(os.path.join(ROOT, name)):
            problems.append("%s must not exist at the repository root: the Claude Code plugin is the root, so it would load" % name)
    for f in os.listdir(os.path.join(ROOT, "skills")):
        sub = os.listdir(os.path.join(ROOT, "skills", f))
        if sub != ["SKILL.md"]:
            problems.append("skills/%s must hold only SKILL.md, found %s" % (f, sorted(sub)))


def main():
    problems = []
    for fn in (check_servers, check_marketplaces, check_manifest_keys, check_files):
        try:
            fn(problems)
        except Exception as e:  # a check that crashes is a failed check, never a silent pass
            problems.append("%s crashed: %s" % (fn.__name__, e))
    if problems:
        print("FAIL - %d problem(s): %s" % (len(problems), "; ".join(problems)))
        return 1
    print("ok - 2 server files point only at %s; marketplaces are local; manifests load no code; plugin holds only manifests, .mcp.json and SKILL.md files" % URL)
    return 0


if __name__ == "__main__":
    sys.exit(main())
