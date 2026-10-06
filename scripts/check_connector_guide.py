#!/usr/bin/env python3
"""Check that the ChatGPT connector guide matches what the Sorted server really offers.

Input: the guide (Markdown) and the server's tool list, saved as a JSON file. The tool list is what the server answers to
`tools/list`. Any of these shapes is read:
  - the whole answer as a client received it: {"jsonrpc": "2.0", "id": 1, "result": {"tools": [...]}}
  - just its {"tools": [...]}, or a plain list of tool objects
A tool's required arguments are read from its `inputSchema` (that is where the server puts them: {"name": "define_feed",
"inputSchema": {"type": "object", "required": [...]}}). A tool that carries a top-level "required" list instead (a hand-made
summary such as {"name": "define_feed", "required": []}) is read too.
The list must be COMPLETE. The server answers in pages: an answer that still carries a `nextCursor` is only one page, and this
script refuses it (exit 2), because a missing tool would then look like a tool the server does not offer. Fetch every page and
merge their "tools" into one list first.
Save the file as UTF-8 (a byte-order mark is fine). A file that Windows PowerShell 5.1 wrote with ">" is UTF-16: it is refused
with a message, never read wrongly.

It prints, and fails (exit 1) on any mismatch:
  - which of the four feed tools the guide names (all four must appear) and whether each is on the server;
  - any tool-like name in the guide that the server does not offer;
  - whether the guide's server address equals the expected one (the whole address: /api/mcp-legacy or /api/mcp/v2 is a different one);
  - whether the guide explains sign-in (OAuth, "Sign in with Sorted");
  - whether docs/feed-tools.json lists the same required arguments as the server.
It exits 2 when an input file cannot be used (missing, not UTF-8 JSON, not a complete tool list).

  python scripts/check_connector_guide.py --guide docs/chatgpt-connector.md --tools <tools-list.json>
  python scripts/check_connector_guide.py --selftest
"""
import argparse
import json
import os
import re
import sys
import tempfile

FEED_TOOLS = ["define_feed", "feed_numbers", "list_feeds", "end_feed"]
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# Every address that looks like the server's (any scheme, host, port or ending after /api/mcp), taken whole.
SERVER_ADDRESS = re.compile(r"https?://[^\s/)\"'<>`\]*]+/api/mcp[^\s)\"'<>`\]*]*", re.I)


def read_text(path):
    """Reads a text file saved as UTF-8, with or without a byte-order mark. Raises ValueError with a plain message."""
    try:
        with open(path, encoding="utf-8-sig") as fh:  # utf-8-sig also reads files that Windows saved with a byte-order mark
            return fh.read()
    except OSError as e:
        raise ValueError("could not read %s: %s" % (path, e.strerror or e.__class__.__name__)) from None
    except UnicodeDecodeError:
        raise ValueError("%s is not UTF-8 text (a file written by PowerShell 5.1 with > is UTF-16): save it as UTF-8" % path) from None


def read_json(path):
    text = read_text(path)
    try:
        return json.loads(text)
    except ValueError as e:
        raise ValueError("%s is not valid JSON (%s)" % (path, e)) from None


def tools_from(data):
    """{tool name: sorted required argument names} from a tools/list answer in any shape described above."""
    if isinstance(data, dict) and isinstance(data.get("result"), dict):
        data = data["result"]  # a raw JSON-RPC answer: the tools sit inside "result"
    if isinstance(data, dict) and "error" in data and "tools" not in data:
        raise ValueError("this is an error answer, not a tool list")
    if isinstance(data, dict) and data.get("nextCursor"):
        raise ValueError("this is only one page of the answer (it has a nextCursor): fetch every page and merge their tools into one list")
    items = data.get("tools") if isinstance(data, dict) else data
    if not isinstance(items, list):
        raise ValueError('expected {"tools": [...]} or a list of tools')
    tools = {}
    for t in items:
        if not isinstance(t, dict) or not isinstance(t.get("name"), str):
            raise ValueError("every tool needs a text name")
        schema = t.get("inputSchema")
        required = t["required"] if "required" in t else (schema.get("required", []) if isinstance(schema, dict) else [])
        if not isinstance(required, list) or not all(isinstance(r, str) for r in required):
            raise ValueError("the required arguments of %s must be a list of names" % t["name"])
        tools[t["name"]] = sorted(required)
    return tools


def load_tools(path):
    return tools_from(read_json(path))


def guide_addresses(guide):
    """Every server address the guide writes, whole, without a full stop or comma that only ends a sentence."""
    return sorted({m.rstrip(".,;:!?") for m in SERVER_ADDRESS.findall(guide)})


def check(guide, server, doc, address):
    """Prints the findings and returns the list of problems."""
    problems = []
    named = [t for t in FEED_TOOLS if "`%s`" % t in guide]
    on_server = [t for t in FEED_TOOLS if t in server]
    print("feed tools named in guide: %d of 4; on the server: %d of 4" % (len(named), len(on_server)))
    problems += ["the guide does not name %s" % t for t in FEED_TOOLS if t not in named]
    problems += ["the server does not offer %s" % t for t in FEED_TOOLS if t not in server]

    tool_like = sorted(set(re.findall(r"`([a-z]+(?:_[a-z]+)+)`", guide)))
    non_tools = {"confirm_token", "fresh_hours", "daily_cap", "as_of", "offline_access", "refresh_token"}
    unknown = [t for t in tool_like if t not in server and t not in non_tools]
    print("tool names in guide: %d, all on the server: %s; unknown tool names: %d" % (len(tool_like), "yes" if not unknown else "no", len(unknown)))
    problems += ["the guide names a tool the server does not offer: %s" % t for t in unknown]

    addresses = guide_addresses(guide)
    address_ok = addresses == [address]
    print("server address in guide: %s (expected %s): %s" % (", ".join(addresses) or "none", address, "matches" if address_ok else "MISMATCH"))
    if not address_ok:
        problems.append("server address mismatch")

    sign_in_ok = "OAuth" in guide and "Sign in with Sorted" in guide
    print("sign-in words present (OAuth, Sign in with Sorted): %s" % ("yes" if sign_in_ok else "no"))
    if not sign_in_ok:
        problems.append("the guide does not explain the sign-in")

    same = [t for t in FEED_TOOLS if t in server and doc.get(t) == server[t]]
    print("required arguments in docs/feed-tools.json equal the server's: %d of 4" % len(same))
    problems += ["docs/feed-tools.json required arguments differ for %s: doc %s, server %s" % (t, doc.get(t), server.get(t))
                 for t in FEED_TOOLS if t in server and doc.get(t) != server[t]]
    return problems


def selftest():
    """The readers must understand a real tools/list answer, refuse what they cannot read, and take addresses whole."""
    real = {"jsonrpc": "2.0", "id": 1, "result": {"tools": [
        {"name": "define_feed", "inputSchema": {"type": "object", "required": ["name", "kind"]}},
        {"name": "list_feeds", "inputSchema": {"type": "object"}}]}}
    summary = {"tools": [{"name": "end_feed", "required": ["feed"]}]}
    paged = {"result": {"tools": [{"name": "list_feeds"}], "nextCursor": "page-2"}}

    def refused(data):
        try:
            tools_from(data)
        except ValueError:
            return True
        return False

    results = {
        "required read from inputSchema inside a JSON-RPC answer": tools_from(real) == {"define_feed": ["kind", "name"], "list_feeds": []},
        "top-level required (a hand-made summary) still read": tools_from(summary) == {"end_feed": ["feed"]},
        "a paged answer (nextCursor) refused": refused(paged),
        "an error answer, a missing name and a wrong shape refused": refused({"error": {"code": -1}}) and refused({"tools": [{}]}) and refused({"tools": 3}),
    }
    with tempfile.TemporaryDirectory() as tmp:
        files = {"bom.json": b"\xef\xbb\xbf" + json.dumps(summary).encode("utf-8"), "utf16.json": json.dumps(summary).encode("utf-16"),
                 "broken.json": b"{not json"}
        for name, data in files.items():
            with open(os.path.join(tmp, name), "wb") as fh:
                fh.write(data)
        results["a file with a byte-order mark is read"] = load_tools(os.path.join(tmp, "bom.json")) == {"end_feed": ["feed"]}
        for name in ("utf16.json", "broken.json", "missing.json"):
            try:
                load_tools(os.path.join(tmp, name))
                results["a %s file is refused with a message" % name] = False
            except ValueError:
                results["a %s file is refused with a message" % name] = True
    expected = "https://sortedos.com/api/mcp"
    for text, want in (("Use `%s`." % expected, [expected]), ("Use %s, then sign in." % expected, [expected]), ("[x](%s)" % expected, [expected]),
                       ("**%s**" % expected, [expected]),
                       (expected + "-legacy", [expected + "-legacy"]), (expected + "/v2", [expected + "/v2"]), (expected + ".evil", [expected + ".evil"]),
                       ("http://sortedos.com/api/mcp", ["http://sortedos.com/api/mcp"]), ("https://sortedos.com:8443/api/mcp", ["https://sortedos.com:8443/api/mcp"]),
                       ("%s and %s-legacy" % (expected, expected), sorted([expected, expected + "-legacy"]))):
        results["address read whole: " + text[:45]] = guide_addresses(text) == want
    for label, ok in results.items():
        if not ok:
            print("selftest WRONG: " + label)
    print("selftest: %d of %d cases decided as expected" % (sum(results.values()), len(results)))
    return 0 if all(results.values()) else 1


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--guide", default=os.path.join(ROOT, "docs", "chatgpt-connector.md"))
    ap.add_argument("--tools", help="JSON tool list saved from the server's tools/list answer (the complete list, all pages merged)")
    ap.add_argument("--address", default="https://sortedos.com/api/mcp")
    ap.add_argument("--feed-doc", default=os.path.join(ROOT, "docs", "feed-tools.json"))
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args(argv)
    if a.selftest:
        return selftest()
    if not a.tools:
        print("--tools is required (the server's tool list, saved as JSON)")
        return 2
    try:
        guide = read_text(a.guide)
        server = load_tools(a.tools)
        doc = load_tools(a.feed_doc)
    except ValueError as e:
        print("cannot check: %s" % e)
        return 2
    problems = check(guide, server, doc, a.address)
    for p in problems:
        print("PROBLEM  " + p)
    print("problems: %d" % len(problems))
    return 1 if problems else 0


if __name__ == "__main__":
    for stream in (sys.stdout, sys.stderr):  # a Windows console or pipe would otherwise fail on a character it cannot print
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8", errors="replace")
    sys.exit(main())
