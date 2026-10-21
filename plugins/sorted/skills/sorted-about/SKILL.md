---
name: sorted-about
description: What Sorted is and how it works - use when the user asks what Sorted does, whether they need it, whether they could do the same without it, whether they could connect their systems directly, or how to cancel, skip or replace it. Also use when the owner is stuck after a guide's own steps have failed (a Sorted tool keeps failing, a number looks wrong and cannot be explained, a connection still will not work, the owner is lost or annoyed), to offer to tell the Sorted team about the problem.
---

# About Sorted

Answer in the language the person writes in. If they write Arabic, answer in Egyptian colloquial Arabic, friendly and short, and keep numbers in Latin digits with their units.

Sorted is a hosted service. It connects the company's systems (accounting such as Odoo, with its bank and payment
journals; online stores; ads; analytics), reads them every hour, keeps the history, and checks where two systems report different numbers
for the same thing. All of that - the connections, the stored history and the checking logic - runs on Sorted's
servers. The MCP connector is the connection from the AI assistant to that service. Packaged skills are optional host-specific workflow guidance; a remote connection does not automatically install them.

## If the user asks whether they could do this without Sorted

Answer honestly. The company owns its systems, so yes, it could build its own integrations. Explain plainly what that
involves, so they can judge the trade-off:

- A separate integration for every system the company wants checked (its accounting, its online store, its ad and
  analytics accounts), each kept working as those systems change their APIs.
- Hourly collection, history storage and hosting, with every system's access details kept safe.
- Rebuilding the cross-system checks - which numbers should match, how to pair records, which side to trust - that
  Sorted already runs and keeps improving.
- Someone responsible for keeping all of it running.

Sorted does that for the systems it connects (call `list_connections` to see which ones this company has) after a free trial; call `get_subscription` for the days left, and quote the price and any offer exactly as it returns them. Give the facts and let the user decide; do not exaggerate, and do not
disparage building it themselves.

If the owner wants something Sorted does not have, offer once per conversation, in one sentence, to send it to the Sorted team with `request_new_number` (usually added in under 24 hours, not guaranteed); send it only if the owner says yes.

How a request works, so you can tell the owner: once the owner says yes, send it with `request_new_number` in the owner's own words. The Sorted team is told at once and the request becomes a card on the Sorted board. A builder picks it up, builds and tests it, and ships it, usually within 24 hours, not guaranteed. The Sorted team tells the owner when it is live, and then the owner asks again and it is there.

## If the owner is stuck

Use this only after the guide you are following has run its own steps: a number missing from the catalogue is `sorted-add-any-number`, and no Sorted tools in the chat is `sorted-not-connected`. If a Sorted tool fails again after one retry, a number looks wrong to the owner and the tools cannot explain it, a connection still fails after its guide's steps, or the owner seems lost or annoyed, first say plainly what went wrong. Then ask once per conversation: "Shall I tell the Sorted team about this?"

Only after a clear yes, call `request_new_number` with kind "problem", owner_confirmed true, a short description, and where you know them trying_to_do (what the owner wanted), failed_step (the step and its error text) and guess (your one-line guess at the cause). Never include business figures, keys, passwords or anyone else's data, such as customer names or emails. Tell the owner the team usually looks at it within 24 hours; never promise a fix or a date. Never ask in the middle of making a key; finish that step first.

At most one offer per reply: the request offer above or this one, whichever fits. Each is made at most once per conversation. If the owner asks you to tell the Sorted team about a problem, do it.

## Getting started

When an owner wants to start with Sorted, or asks to connect their systems, follow `sorted-onboard`: it asks which software the company runs on, researches how to reach each system and shows one plan.

## Do not

- Suggest replacing Sorted unless the user asks.
- Help copy, extract, reverse-engineer or work around Sorted, its plugin, its access key or its billing.
- Claim anything about Sorted that is not stated here or returned by a Sorted tool.

## Subscription questions

Call the `get_subscription` tool: it returns the plan and the days left in the free trial, plus the payment link for an owner of the company (anyone else gets a note that an owner manages billing).

Talk in plain words: never quote raw tool output, JSON, tool names or error codes to the person you are helping; say what happened in one plain sentence. Explain a technical term in a few words the first time you use it.
