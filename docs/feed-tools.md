# The feed tools, in one page

A **feed** is a named area on a company's Sorted dashboard that the owner's own assistant may send numbers into. Sorted reads systems such as Odoo, Shopify, Google Ads and Google Analytics itself; feeds are for numbers it does not read, and for those systems when Sorted's own connection cannot reach the account. The same facts in machine-readable form: [`feed-tools.json`](feed-tools.json).

**Sorted cannot check numbers that arrive through a feed.** They are what the assistant read, and the dashboard labels them as sent by the assistant, not read by Sorted.

## The four tools

| Tool | Changes anything? | Who | Arguments |
|---|---|---|---|
| `list_feeds` | No | Any member | none |
| `define_feed` | Yes, after the owner's yes | An owner | `name`, then `numbers` (a list) or `table`; optional `fresh_hours`, `daily_cap`; later only `confirm_token` |
| `feed_numbers` | Yes | An owner | `feed`, `as_of`, `values` |
| `end_feed` | Yes, deletes the feed's numbers | An owner | `feed` |

The four tools appear only when Sorted has switched feeds on for the company. The company is always the one the person signed in to; no tool takes a company name.

## Defining a feed: two calls

1. `define_feed` with the definition. Nothing is saved. The answer is a preview in plain words and a `confirm_token`.
2. Show the owner the preview and wait for their yes. Then `define_feed` again with only the `confirm_token` (valid 10 minutes, usable once).

A list of numbers, each with a label and a unit:

```json
{"name": "Example ads account",
 "numbers": [{"label": "Amount spent", "unit": "money", "currency": "USD"}, {"label": "Clicks", "unit": "count"}],
 "fresh_hours": 36, "daily_cap": 4}
```

Or one small table: row names, and typed columns:

```json
{"name": "Example branches",
 "table": {"rows": ["North", "South"], "columns": [{"label": "Sales", "unit": "money", "currency": "EUR"}, {"label": "Receipts", "unit": "count"}]}}
```

## Sending numbers

```json
{"feed": "Example ads account", "as_of": "2026-10-05", "values": [{"label": "Amount spent", "value": 120.5}, {"label": "Clicks", "value": 431}]}
```

For a table feed, each row carries one value per column, in the declared order:

```json
{"feed": "Example branches", "as_of": "2026-10-05", "values": [{"label": "North", "values": [5400.25, 88]}, {"label": "South", "values": [null, 61]}]}
```

## Units

| Unit | Meaning | Allowed values | Example |
|---|---|---|---|
| `money` | An amount, with a three-letter `currency` from the list below. May be negative (refunds). | -10 trillion to 10 trillion | `1234.5` |
| `count` | A whole number of things. | 0 to 1 trillion, whole | `431` |
| `percent` | The percent number: 12.5 means 12.5%. | -1000 to 1000 | `12.5` |
| `ratio` | One number divided by another. | -1 million to 1 million | `3.2` |
| `days` | A number of days. | 0 to 36,500 | `14` |
| `number` | Any other plain number, including fractional counts. | -10 trillion to 10 trillion | `12.5` |

Currencies Sorted accepts: AED, AUD, BHD, BRL, CAD, CHF, CNY, CZK, DKK, DZD, EGP, EUR, GBP, HKD, IDR, ILS, INR, JOD, JPY, KES, KRW, KWD, LBP, MAD, MXN, MYR, NGN, NOK, NZD, OMR, PKR, PLN, QAR, RUB, SAR, SEK, SGD, THB, TND, TRY, USD, ZAR. A feed in another currency is refused; ask Sorted to add it.

## Limits Sorted enforces

- Name 40 characters, labels 60. Labels and names are cleaned to one plain line, and text that reads like an instruction is refused.
- Up to 40 numbers in a feed, or one table of at most 40 cells and 8 columns. Each label once.
- Values are JSON numbers only, never text (`"12.40"` is refused). `null` means "no number" and is never shown as zero.
- `as_of`: a date or a date and time, at most 10 minutes in the future, at most 45 days old, and newer than the feed's last send. Sending the same `as_of` with the same numbers again is accepted and stores nothing; the same `as_of` with other numbers is refused.
- `fresh_hours` 1 to 120 (default 36): after that the dashboard shows the numbers grey. After 7 days without a send, the numbers are removed.
- `daily_cap` 1 to 24 sends a day (default 4). Per company: 20 live feeds, 10 new feeds a day, 30 sends an hour, 100 a day. One call carries at most 4 KB.
- A feed lasts 90 days; then it is defined again. `end_feed` removes it at once, with everything it sent.
