---
name: sorted-subscription
description: What to do when Sorted says billing_required or the free trial is ending - explain simply and give the payment link. Use when a Sorted tool returns billing_required, or the user asks about their Sorted subscription, trial or payment.
---

# Subscription

- If any Sorted tool returns `billing_required`: tell the user plainly that their Sorted subscription (or free trial) has ended, that their data is safe and paused, and, if the tool result has a `pay_here` link, give it to them (only an owner of the company gets one). If the result has a `billing_note` instead, this person is not an owner: say that an owner of their company manages billing, and give no link. Once paid, Sorted works again within a minute.
- If `get_overview` mentions a free trial with days left: mention it once, briefly, at the end of your answer. For the payment link (owners only), call `get_subscription`.
- Sorted is billed per user per month (each person who can sign in counts, the owner included), after a free trial that needs no card. For this company's exact price, call get_subscription; never quote a price from memory. Never promise discounts or refunds.
