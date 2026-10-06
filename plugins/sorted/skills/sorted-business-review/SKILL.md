---
name: sorted-business-review
description: Monthly (or any-time) business review from Sorted's live numbers - sales, cash, who owes whom, what is overdue, and which systems disagree. Use when the user asks how the business is doing, for a review, a summary, or a board update.
---

# Business review

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
5. Quote every figure with its currency and the snapshot time. Never invent a number that no tool returned; say "not available" instead.
6. If a tool returns `billing_required`, follow the `sorted-subscription` skill instead.
