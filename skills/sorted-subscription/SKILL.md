---
name: sorted-subscription
description: What to do when Sorted says billing_required or the free trial is ending - explain simply and give the payment link. Use when a Sorted tool returns billing_required, or the user asks about their Sorted subscription, trial or payment.
---

# Subscription

No Sorted tools in this chat? Sorted is not connected yet: follow `sorted-not-connected`.

- If any Sorted tool returns `billing_required`: tell the user plainly that their Sorted subscription (or free trial) has ended and their dashboard is paused, and that Sorted deletes the company's data 30 days after the trial or subscription ended unless they subscribe (if the result gives a deletion date, say exactly that; a payment that is only failing deletes nothing yet), and, if the tool result has a `pay_here` link, give it to them (only an owner of the company gets one). If the result has a `billing_note` instead, this person is not an owner: say that an owner of their company manages billing, and give no link. Once paid, Sorted works again within a minute.
- If `get_overview` mentions a free trial with days left: mention it once, briefly, at the end of your answer. For the payment link (owners only), call `get_subscription`.
- Sorted costs $5 per user per month (each person who can sign in counts, the owner included), after a free trial that needs no card. For this company's exact price, call get_subscription and quote what it returns. Never promise discounts or refunds.

Answer in the language the owner writes in. For Egyptian Arabic, answer in natural Egyptian Arabic, right-to-left, and keep numbers in Latin digits with their units.

Talk in plain words: never quote raw tool output, JSON, tool names or error codes to the person you are helping; say what happened in one plain sentence. Explain a technical term in a few words the first time you use it.
