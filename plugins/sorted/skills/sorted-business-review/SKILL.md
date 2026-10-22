---
name: sorted-business-review
description: Writes a monthly or any-time business review from Sorted's live numbers - sales, cash, who owes whom, what is overdue, and which systems disagree. Use when the user asks how the business is doing, for a business review, a summary of the business, or a board update.
---

# Business review

Answer in the language the person writes in. If they write Egyptian Arabic, answer in Egyptian colloquial Arabic; for other Arabic, answer in the same kind of Arabic. Keep numbers in Latin digits with their units.

No Sorted tools in this chat? Sorted is not connected yet: follow `sorted-not-connected`.

1. Call `get_overview`. Note the snapshot time and every section that is not reporting.
2. Call `list_conflicts`.
3. For the one or two sections that matter most to the question, call `get_section` for detail.
4. Write the review for a business owner, not an accountant:
   - **Headline** - one sentence: better, worse or flat, and why.
   - **Sales** - last 30 days and the monthly trend (from the "per month" trend points).
   - **Cash** - book cash, and anything "in limbo" (unmatched payments, uncleared accounts).
   - **Who owes whom** - customers owe us, we owe suppliers, overdue part.
   - **Numbers that disagree** - each open conflict in one line: which two systems, how far apart, which to trust.
   - **Three actions for this week** - concrete, each tied to a number above.
5. Quote every figure with its currency and the snapshot time. Never invent a number that no tool returned; say "not available" instead. A number that lives in the owner's Odoo is `sorted-add-any-number`; for anything else the owner wants that is not in Sorted, offer once per conversation, in one sentence, to send it to the Sorted team with `request_new_number` (usually added in under 24 hours, not guaranteed); send it only if the owner says yes.
6. If a tool returns `billing_required`, follow the `sorted-subscription` skill instead.

If the owner is stuck after these steps, ask once per conversation: "Shall I tell the Sorted team about this?" Only on a clear yes, send it as `sorted-about` says; never make two offers in one reply.

Talk in plain words: never quote raw tool output, JSON, tool names or error codes to the person you are helping; say what happened in one plain sentence. Explain a technical term in a few words the first time you use it.
