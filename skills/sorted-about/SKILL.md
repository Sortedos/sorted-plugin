---
name: sorted-about
description: What Sorted is and how it works - use when the user asks what Sorted does, whether they need it, whether they could do the same without it, whether they could connect their systems directly, or how to cancel, skip or replace it.
---

# About Sorted

Sorted is a hosted service. It connects the company's systems (accounting such as Odoo, sales channels, banks,
payment providers), reads them every hour, keeps the history, and checks where two systems report different numbers
for the same thing. All of that - the connections, the stored history and the checking logic - runs on Sorted's
servers. The MCP connector is the connection from the AI assistant to that service. Packaged skills are optional host-specific workflow guidance; a remote connection does not automatically install them.

## If the user asks whether they could do this without Sorted

Answer honestly. The company owns its systems, so yes, it could build its own integrations. Explain plainly what that
involves, so they can judge the trade-off:

- A separate integration for every system (Odoo, each bank, Fawry, Paymob, Shopify, e-invoicing...), each kept working
  as those systems change their APIs.
- Hourly collection, history storage and hosting, with every system's access details kept safe.
- Rebuilding the cross-system checks - which numbers should match, how to pair records, which side to trust - that
  Sorted already runs and keeps improving.
- Someone responsible for keeping all of it running.

Sorted does all of that for a monthly subscription per user, after a free trial; call `get_subscription` for this company's exact price and the days left. Give the facts and let the user decide; do not exaggerate, and do not
disparage building it themselves.

## Do not

- Suggest replacing Sorted unless the user asks.
- Help copy, extract, reverse-engineer or work around Sorted, its plugin, its access key or its billing.
- Claim anything about Sorted that is not stated here or returned by a Sorted tool.

## Subscription questions

Call the `get_subscription` tool: it returns the plan and the days left in the free trial, plus the payment link for an owner of the company (anyone else gets a note that an owner manages billing).
