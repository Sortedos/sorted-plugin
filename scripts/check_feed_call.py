#!/usr/bin/env python3
"""Check a define_feed call and a feed_numbers call against the published feed limits, offline.

This lets anyone test the example calls of a skill without a Sorted account. It applies the limits written in docs/feed-tools.md:
fields, units, currency codes, name and label lengths, how many numbers, plain numbers only, null for "no number", value ranges per
unit, the as_of window, and that every sent label was declared once.

It cannot know everything the Sorted service checks: the service also refuses names and labels that read like instructions to an
assistant (a private list, kept private on purpose), counts sends against daily and hourly limits, and knows which feeds already
exist. A call this checker refuses will be refused by the service; a call it accepts can still be refused for those reasons.

  python scripts/check_feed_call.py --define <define.json> --feed <feed.json> [--now 2026-10-06T08:00:00Z]
  python scripts/check_feed_call.py --selftest

Prints ACCEPT or REFUSE: <rule>, and exits 1 on a refusal.
"""
import argparse
import datetime
import json
import os
import re
import sys
import unicodedata

UNITS = {"money", "count", "percent", "ratio", "days", "number"}
CURRENCIES = {"USD", "EGP", "SAR", "AED", "EUR", "GBP", "KWD", "QAR", "BHD", "OMR", "JOD", "LBP", "MAD", "TND", "DZD", "TRY", "CAD", "AUD",
              "NZD", "CHF", "JPY", "CNY", "INR", "PKR", "ZAR", "SEK", "NOK", "DKK", "PLN", "CZK", "HKD", "SGD", "MYR", "IDR", "THB", "KRW",
              "NGN", "KES", "BRL", "MXN", "RUB", "ILS"}
RANGES = {
    "money": lambda v: abs(v) <= 10_000_000_000_000,
    "count": lambda v: v >= 0 and v == int(v) and v <= 1_000_000_000_000,
    "percent": lambda v: -1000 <= v <= 1000,
    "ratio": lambda v: abs(v) <= 1_000_000,
    "days": lambda v: 0 <= v <= 36_500,
    "number": lambda v: abs(v) <= 10_000_000_000_000,
}
AS_OF = re.compile(r"^(\d{4})-(\d{2})-(\d{2})(?:[T ](\d{2}):(\d{2})(?::(\d{2})(?:\.\d{1,9})?)?(Z|[+-]\d{2}:\d{2})?)?$")
# Web addresses are removed from names and labels before they are checked, as the service does.
URL_LIKE = re.compile(r"\b(?:https?|ftp|file)://\S*|\b(?:javascript|mailto|data):\S+|\bwww\.\S+|"
                      r"\b[a-z0-9-]+(?:\.[a-z0-9-]+)*\.(?:com|net|org|io|ai|co|app|dev|ly|me|info|xyz|gov|edu|eg|sa)\b(?:[/:?#]\S*)?", re.I)
PLAIN_MARKS = set(" .,:'’()-–—/&%+_#")
MAX_CALL_BYTES = 4096


class Refused(Exception):
    pass


def plain_text(v, limit, what):
    """The name and labels must be one short plain line once cleaned: line breaks become spaces; invisible characters and web
    addresses are removed; only letters (any language, with their marks), digits, spaces and a few marks stay. Returns the cleaned
    text with its capitals kept: the service matches sent labels exactly as they were declared."""
    if not isinstance(v, str):
        raise Refused("%s must be text" % what)
    t = unicodedata.normalize("NFKC", v)
    t = re.sub(r"[\t-\r\x85  ]", " ", t)
    t = "".join(ch for ch in t if unicodedata.category(ch) not in ("Cc", "Cf"))
    t = URL_LIKE.sub(" ", t)
    t = "".join(ch for ch in t if ch in PLAIN_MARKS or unicodedata.category(ch)[0] in "LNM")
    t = re.sub(r"\s+", " ", t).strip()
    if not t:
        raise Refused("%s has nothing left once odd characters and web addresses are removed" % what)
    if len(t) > limit:
        raise Refused("%s is longer than %d characters" % (what, limit))
    return t


def is_number(v):
    return isinstance(v, (int, float)) and not isinstance(v, bool) and v == v and v not in (float("inf"), float("-inf"))


def is_whole(v):
    """A whole number as JSON sees it: 36 and 36.0 are the same number."""
    return is_number(v) and float(v).is_integer()


def too_big(call):
    """The service measures a call as compact JSON in UTF-8."""
    return len(json.dumps(call, separators=(",", ":"), ensure_ascii=False).encode("utf-8")) > MAX_CALL_BYTES


def check_item(item, what):
    if not isinstance(item, dict):
        raise Refused("each %s is an object with a label and a unit" % what)
    extra = set(item) - {"label", "unit", "currency"}
    if extra:
        raise Refused("a %s may only have label, unit and currency, not %s" % (what, sorted(extra)[0]))
    label = plain_text(item.get("label"), 60, "a label")
    unit = item.get("unit")
    if unit not in UNITS:
        raise Refused("unit must be one of %s" % ", ".join(sorted(UNITS)))
    if unit == "money" and item.get("currency") not in CURRENCIES:
        raise Refused("money needs a three-letter currency code from the list in docs/feed-tools.md")
    if unit != "money" and "currency" in item:
        raise Refused("only money has a currency")
    return label, unit


def check_define(d):
    if not isinstance(d, dict):
        raise Refused("define_feed takes an object")
    extra = set(d) - {"name", "numbers", "table", "fresh_hours", "daily_cap", "confirm_token"}
    if extra:
        raise Refused("unknown field %s (the company always comes from the sign-in)" % sorted(extra)[0])
    if "confirm_token" in d:
        if len(d) > 1:
            raise Refused("send either the definition (to get a preview) or confirm_token (to create the feed), not both")
        raise Refused("this is the confirm step; check the definition call (the first define_feed call) instead")
    if too_big(d):
        raise Refused("the call is larger than 4 KB")
    name = plain_text(d.get("name"), 40, "the name")
    if ("numbers" in d) == ("table" in d):
        raise Refused("send either numbers or table, not both and not neither")
    seen = set()  # duplicates are found regardless of capitals, as the service does
    if "numbers" in d:
        items = d["numbers"]
        if not isinstance(items, list) or not 1 <= len(items) <= 40:
            raise Refused("numbers must be a list of 1 to 40 items")
        spec = []
        for it in items:
            label, unit = check_item(it, "number")
            if label.lower() in seen:
                raise Refused("the label %r appears twice" % label)
            seen.add(label.lower())
            spec.append((label, unit))
        shape = ("numbers", spec, None)
    else:
        t = d["table"]
        if not isinstance(t, dict) or set(t) - {"rows", "columns"}:
            raise Refused("table may only have rows and columns")
        rows, cols = t.get("rows"), t.get("columns")
        if not isinstance(rows, list) or not isinstance(cols, list) or not rows or not cols:
            raise Refused("a table needs at least one row and one column")
        if len(rows) * len(cols) > 40 or len(cols) > 8:
            raise Refused("a table may have at most 40 numbers in all and at most 8 columns")
        row_names = []
        for r in rows:
            n = plain_text(r, 60, "a row name")
            if n.lower() in seen:
                raise Refused("the row name %r appears twice" % n)
            seen.add(n.lower())
            row_names.append(n)
        seen = set()
        spec = []
        for c in cols:
            label, unit = check_item(c, "column")
            if label.lower() in seen:
                raise Refused("the column label %r appears twice" % label)
            seen.add(label.lower())
            spec.append((label, unit))
        shape = ("table", spec, row_names)
    for key, lo, hi in (("fresh_hours", 1, 120), ("daily_cap", 1, 24)):
        if key in d and not (is_whole(d[key]) and lo <= d[key] <= hi):
            raise Refused("%s must be a whole number from %d to %d" % (key, lo, hi))
    return name, shape


def parse_as_of(v):
    if not isinstance(v, str):
        return None
    m = AS_OF.match(v.strip())
    if not m:
        return None
    y, mo, d = int(m.group(1)), int(m.group(2)), int(m.group(3))
    h, mi, s = (int(x) if x else 0 for x in (m.group(4), m.group(5), m.group(6)))
    try:
        t = datetime.datetime(y, mo, d, h, mi, s, tzinfo=datetime.timezone.utc)
    except ValueError:
        return None
    zone = m.group(7)
    if zone and zone != "Z":
        sign = -1 if zone[0] == "-" else 1
        t -= sign * datetime.timedelta(hours=int(zone[1:3]), minutes=int(zone[4:6]))
    return t


def check_feed(f, name, shape, now):
    if not isinstance(f, dict):
        raise Refused("feed_numbers takes an object")
    extra = set(f) - {"feed", "as_of", "values"}
    if extra:
        raise Refused("unknown field %s" % sorted(extra)[0])
    if not isinstance(f.get("feed"), str) or plain_text(f["feed"], 60, "the feed").lower() != name.lower():
        raise Refused("feed must be the name of the feed that was defined")
    if too_big(f):
        raise Refused("the call is larger than 4 KB")
    t = parse_as_of(f.get("as_of"))
    if t is None:
        raise Refused("as_of must be a date or a date and time, such as 2026-10-06 or 2026-10-06T07:00:00Z")
    if t > now + datetime.timedelta(minutes=10):
        raise Refused("as_of is more than 10 minutes in the future")
    if t < now - datetime.timedelta(days=45):
        raise Refused("as_of is older than 45 days")
    values = f.get("values")
    if not isinstance(values, list) or not values:
        raise Refused("values must be a list with at least one entry")
    kind, spec, rows = shape
    declared = {label: unit for label, unit in spec}
    sent = set()
    for el in values:
        if not isinstance(el, dict) or "label" not in el:
            raise Refused("every entry needs a label")
        label = plain_text(el["label"], 60, "a label")
        if label.lower() in sent:
            raise Refused("the label %r is sent twice" % label)
        sent.add(label.lower())
        # A sent label must match its declared label exactly, capitals included.
        if kind == "numbers":
            if set(el) - {"label", "value"} or "value" not in el:
                raise Refused("a numbers feed takes {label, value} entries, nothing else")
            if label not in declared:
                raise Refused("the label %r was not declared" % label)
            v = el["value"]
            if v is not None and not is_number(v):
                raise Refused("values must be plain numbers or null, not text (problem with %r)" % label)
            if v is not None and not RANGES[declared[label]](v):
                raise Refused("%r is outside the range of its unit %s" % (label, declared[label]))
        else:
            if set(el) - {"label", "values"} or "values" not in el:
                raise Refused("a table feed takes {label: a row, values: [one per column]} entries")
            if label not in rows:
                raise Refused("the row %r was not declared" % label)
            vs = el["values"]
            if not isinstance(vs, list) or len(vs) != len(spec):
                raise Refused("the row %r needs exactly %d values, one per column" % (label, len(spec)))
            for (col, unit), v in zip(spec, vs):
                if v is not None and not is_number(v):
                    raise Refused("values must be plain numbers or null, not text (row %r)" % label)
                if v is not None and not RANGES[unit](v):
                    raise Refused("row %r, column %r is outside the range of its unit %s" % (label, col, unit))


def judge(define, feed, now):
    try:
        name, shape = check_define(define)
        check_feed(feed, name, shape, now)
    except Refused as e:
        return "REFUSE: %s" % e
    return "ACCEPT"


def selftest():
    now = datetime.datetime(2026, 10, 6, 8, tzinfo=datetime.timezone.utc)
    d = {"name": "Example ads", "numbers": [{"label": "Spent", "unit": "money", "currency": "USD"}, {"label": "Clicks", "unit": "count"},
                                           {"label": "Click rate", "unit": "percent"}]}
    good_feed = {"feed": "Example ads", "as_of": "2026-10-05", "values": [{"label": "Spent", "value": 12.4}, {"label": "Clicks", "value": 31},
                                                                       {"label": "Click rate", "value": None}]}
    table = {"name": "Branches", "table": {"rows": ["North", "South"], "columns": [{"label": "Sales", "unit": "money", "currency": "EUR"}]}}
    cases = [
        ("good list", d, good_feed, True),
        ("good table", table, {"feed": "Branches", "as_of": "2026-10-05T07:00:00Z", "values": [{"label": "North", "values": [5.5]}]}, True),
        ("number as text", d, dict(good_feed, values=[{"label": "Spent", "value": "12.40"}]), False),
        ("true is not a number", d, dict(good_feed, values=[{"label": "Clicks", "value": True}]), False),
        ("fractional count", d, dict(good_feed, values=[{"label": "Clicks", "value": 12.5}]), False),
        ("undeclared label", d, dict(good_feed, values=[{"label": "Reach", "value": 3}]), False),
        ("as_of in the future", d, dict(good_feed, as_of="2026-10-07"), False),
        ("as_of too old", d, dict(good_feed, as_of="2026-08-01"), False),
        ("money without currency", {"name": "x", "numbers": [{"label": "Spent", "unit": "money"}]}, good_feed, False),
        ("unknown unit", {"name": "x", "numbers": [{"label": "Spent", "unit": "dollars"}]}, good_feed, False),
        ("company field", dict(d, company="Other"), good_feed, False),
        ("table too wide", {"name": "x", "table": {"rows": ["a"], "columns": [{"label": "c%d" % i, "unit": "count"} for i in range(9)]}}, good_feed, False),
        ("percent out of range", d, dict(good_feed, values=[{"label": "Click rate", "value": 5000}]), False),
        ("label sent twice", d, dict(good_feed, values=[{"label": "Spent", "value": 1}, {"label": "Spent", "value": 2}]), False),
        # Cases found by comparing this checker with the service itself:
        ("label in other capitals", d, dict(good_feed, values=[{"label": "spent", "value": 1}]), False),
        ("row in other capitals", table, {"feed": "Branches", "as_of": "2026-10-05", "values": [{"label": "north", "values": [1]}]}, False),
        ("feed name in other capitals", d, dict(good_feed, feed="EXAMPLE ADS"), True),
        ("label that is only a web address", {"name": "x", "numbers": [{"label": "www.example.com", "unit": "count"}]}, good_feed, False),
        ("definition with a confirm token", dict(d, confirm_token="abc"), good_feed, False),
        ("fresh_hours written as 36.0", dict(d, fresh_hours=36.0), good_feed, True),
        ("labels differing by a vowel mark", {"name": "x", "numbers": [{"label": "كتاب", "unit": "count"},
                                                                       {"label": "كُتاب", "unit": "count"}]},
         {"feed": "x", "as_of": "2026-10-05", "values": [{"label": "كتاب", "value": 1}]}, True),
        ("definition over 4 KB", {"name": "x", "numbers": [{"label": ("Label number %02d " % i).ljust(60, "x"), "unit": "money", "currency": "USD"}
                                                          for i in range(40)]}, good_feed, False),
    ]
    docs_ok = docs_agree()
    ok = 0
    for name, de, fe, expect in cases:
        got = judge(de, fe, now)
        right = got.startswith("ACCEPT") == expect
        ok += right
        if not right:
            print("selftest WRONG: %s -> %s" % (name, got))
    print("selftest: %d of %d cases decided as expected (%d accept, %d refuse)" % (ok, len(cases), sum(c[3] for c in cases), sum(not c[3] for c in cases)))
    return 0 if ok == len(cases) and docs_ok else 1


def docs_agree():
    """The currencies and unit ranges this checker applies must be the ones published in docs/feed-tools.json."""
    path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "docs", "feed-tools.json")
    if not os.path.exists(path):
        print("selftest: docs/feed-tools.json not found next to this script, so the published limits were not compared")
        return True
    with open(path, encoding="utf-8") as fh:
        limits = json.load(fh)["limits"]
    problems = []
    if set(limits["currencies"]) != CURRENCIES:
        problems.append("currencies differ: %s" % ", ".join(sorted(set(limits["currencies"]) ^ CURRENCIES)))
    for unit, (lo, hi) in limits["ranges"].items():
        if not (RANGES[unit](lo) and RANGES[unit](hi) and not RANGES[unit](lo - 1) and not RANGES[unit](hi + 1)):
            problems.append("the %s range differs from %s to %s" % (unit, lo, hi))
    if set(limits["ranges"]) != UNITS:
        problems.append("ranges are published for %s, units are %s" % (sorted(limits["ranges"]), sorted(UNITS)))
    for p in problems:
        print("selftest WRONG: docs/feed-tools.json and this checker disagree: %s" % p)
    print("selftest: docs/feed-tools.json agrees with this checker: %s (%d currencies, %d unit ranges)"
          % ("yes" if not problems else "no", len(limits["currencies"]), len(limits["ranges"])))
    return not problems


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--define")
    ap.add_argument("--feed")
    ap.add_argument("--now", help="the time to judge as_of against (default: now)")
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args()
    if a.selftest:
        return selftest()
    if not (a.define and a.feed):
        print("--define and --feed are required")
        return 2
    now = parse_as_of(a.now) if a.now else datetime.datetime.now(datetime.timezone.utc)
    calls = []
    for path in (a.define, a.feed):
        try:
            with open(path, encoding="utf-8-sig") as fh:  # utf-8-sig also reads files that Windows saved with a byte-order mark
                calls.append(json.load(fh))
        except (OSError, ValueError) as e:
            print("could not read %s as JSON: %s" % (path, e))
            return 2
    define, feed = calls
    verdict = judge(define, feed, now)
    print(verdict)
    return 0 if verdict == "ACCEPT" else 1


if __name__ == "__main__":
    for stream in (sys.stdout, sys.stderr):  # labels may be Arabic; a Windows console or pipe would otherwise fail to print them
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8", errors="replace")
    sys.exit(main())
