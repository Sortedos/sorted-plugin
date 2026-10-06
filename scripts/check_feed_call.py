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
NOT_PLAIN = re.compile(r"[^\w\s.,:'’()\-–—/&%+#]", re.UNICODE)
AS_OF = re.compile(r"^(\d{4})-(\d{2})-(\d{2})(?:[T ](\d{2}):(\d{2})(?::(\d{2})(?:\.\d{1,9})?)?(Z|[+-]\d{2}:\d{2})?)?$")


class Refused(Exception):
    pass


def plain_text(v, limit, what):
    """The name and labels must be one short plain line once cleaned (the service also removes web addresses and odd marks)."""
    if not isinstance(v, str):
        raise Refused("%s must be text" % what)
    t = unicodedata.normalize("NFKC", v)
    t = re.sub(r"\s+", " ", NOT_PLAIN.sub("", t)).strip()
    if not t:
        raise Refused("%s has nothing left once odd characters are removed" % what)
    if len(t) > limit:
        raise Refused("%s is longer than %d characters" % (what, limit))
    return t.lower()


def is_number(v):
    return isinstance(v, (int, float)) and not isinstance(v, bool) and v == v and v not in (float("inf"), float("-inf"))


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
        raise Refused("money needs a three-letter currency code from the supported list")
    if unit != "money" and "currency" in item:
        raise Refused("only money has a currency")
    return label, unit


def check_define(d):
    if not isinstance(d, dict):
        raise Refused("define_feed takes an object")
    extra = set(d) - {"name", "numbers", "table", "fresh_hours", "daily_cap", "confirm_token"}
    if extra:
        raise Refused("unknown field %s (the company always comes from the sign-in)" % sorted(extra)[0])
    name = plain_text(d.get("name"), 40, "the name")
    if ("numbers" in d) == ("table" in d):
        raise Refused("send either numbers or table, not both and not neither")
    seen = set()
    if "numbers" in d:
        items = d["numbers"]
        if not isinstance(items, list) or not 1 <= len(items) <= 40:
            raise Refused("numbers must be a list of 1 to 40 items")
        spec = []
        for it in items:
            label, unit = check_item(it, "number")
            if label in seen:
                raise Refused("the label %r appears twice" % label)
            seen.add(label)
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
            if n in seen:
                raise Refused("the row name %r appears twice" % n)
            seen.add(n)
            row_names.append(n)
        seen = set()
        spec = []
        for c in cols:
            label, unit = check_item(c, "column")
            if label in seen:
                raise Refused("the column label %r appears twice" % label)
            seen.add(label)
            spec.append((label, unit))
        shape = ("table", spec, row_names)
    for key, lo, hi in (("fresh_hours", 1, 120), ("daily_cap", 1, 24)):
        if key in d and not (isinstance(d[key], int) and not isinstance(d[key], bool) and lo <= d[key] <= hi):
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
    if not isinstance(f.get("feed"), str) or plain_text(f["feed"], 60, "the feed") != name:
        raise Refused("feed must be the name of the feed that was defined")
    t = parse_as_of(f.get("as_of"))
    if t is None:
        raise Refused("as_of must be a date or a date and time, such as 2026-10-06 or 2026-10-06T07:00:00Z")
    if t > now + datetime.timedelta(minutes=10):
        raise Refused("as_of is in the future")
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
        if label in sent:
            raise Refused("the label %r is sent twice" % label)
        sent.add(label)
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
    if len(json.dumps(f, ensure_ascii=False).encode("utf-8")) > 4096:
        raise Refused("the call is larger than 4 KB")


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
    ]
    ok = 0
    for name, de, fe, expect in cases:
        got = judge(de, fe, now)
        right = got.startswith("ACCEPT") == expect
        ok += right
        if not right:
            print("selftest WRONG: %s -> %s" % (name, got))
    print("selftest: %d of %d cases decided as expected (%d accept, %d refuse)" % (ok, len(cases), sum(c[3] for c in cases), sum(not c[3] for c in cases)))
    return 0 if ok == len(cases) else 1


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
    with open(a.define, encoding="utf-8") as fh:
        define = json.load(fh)
    with open(a.feed, encoding="utf-8") as fh:
        feed = json.load(fh)
    verdict = judge(define, feed, now)
    print(verdict)
    return 0 if verdict == "ACCEPT" else 1


if __name__ == "__main__":
    sys.exit(main())
