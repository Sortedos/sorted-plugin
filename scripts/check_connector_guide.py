#!/usr/bin/env python3
"""Check that the ChatGPT connector guide matches what the Sorted server really offers.

Input: the guide (Markdown) and a tool list captured from the server's `tools/list` answer, saved as JSON:
  {"tools": [{"name": "define_feed", "required": []}, ...]}   (a plain list of such objects is accepted too)

It prints, and fails (exit 1) on any mismatch:
  - which of the four feed tools the guide names (all four must appear) and whether each is on the server;
  - any tool-like name in the guide that the server does not offer;
  - whether the guide's server address equals the expected one;
  - whether the guide explains sign-in (OAuth, "Sign in with Sorted");
  - whether docs/feed-tools.json lists the same required arguments as the server.

  python scripts/check_connector_guide.py --guide docs/chatgpt-connector.md --tools <tools-list.json>
"""
import argparse
import json
import os
import re
import sys

FEED_TOOLS = ["define_feed", "feed_numbers", "list_feeds", "end_feed"]
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def load_tools(path):
    with open(path, encoding="utf-8") as fh:
        data = json.load(fh)
    items = data["tools"] if isinstance(data, dict) else data
    return {t["name"]: sorted(t.get("required", [])) for t in items}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--guide", default=os.path.join(ROOT, "docs", "chatgpt-connector.md"))
    ap.add_argument("--tools", required=True, help="JSON tool list captured from the server's tools/list answer")
    ap.add_argument("--address", default="https://sortedos.com/api/mcp")
    ap.add_argument("--feed-doc", default=os.path.join(ROOT, "docs", "feed-tools.json"))
    a = ap.parse_args()

    with open(a.guide, encoding="utf-8") as fh:
        guide = fh.read()
    server = load_tools(a.tools)
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

    addresses = sorted(set(re.findall(r"https://[A-Za-z0-9.-]+/api/mcp\b", guide)))
    address_ok = addresses == [a.address]
    print("server address in guide: %s (expected %s): %s" % (", ".join(addresses) or "none", a.address, "matches" if address_ok else "MISMATCH"))
    if not address_ok:
        problems.append("server address mismatch")

    sign_in_ok = "OAuth" in guide and "Sign in with Sorted" in guide
    print("sign-in words present (OAuth, Sign in with Sorted): %s" % ("yes" if sign_in_ok else "no"))
    if not sign_in_ok:
        problems.append("the guide does not explain the sign-in")

    with open(a.feed_doc, encoding="utf-8") as fh:
        doc = {t["name"]: sorted(t["required"]) for t in json.load(fh)["tools"]}
    same = [t for t in FEED_TOOLS if t in server and doc.get(t) == server[t]]
    print("required arguments in docs/feed-tools.json equal the server's: %d of 4" % len(same))
    problems += ["docs/feed-tools.json required arguments differ for %s: doc %s, server %s" % (t, doc.get(t), server.get(t))
                 for t in FEED_TOOLS if t in server and doc.get(t) != server[t]]

    for p in problems:
        print("PROBLEM  " + p)
    print("problems: %d" % len(problems))
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
