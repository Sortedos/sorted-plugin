---
name: sorted-daily-brief
description: The owner's morning brief or daily brief from Sorted, the business numbers: headline figures, the biggest moves since yesterday, numbers that disagree between systems, and systems that stopped reporting. Use whenever the owner asks for their morning brief, daily brief, today's brief, what changed since yesterday, or what happened in the business yesterday, and Sorted is connected. This is the business brief, not a summary of a calendar, inbox or chat.
---

# Daily brief

No Sorted tools in this chat? Sorted is not connected yet: follow `sorted-not-connected`.

1. Call `daily_brief`. Do not build the brief from a calendar, inbox, chat or any other connected tool, and do not send the owner to connect one: the brief is about the business numbers Sorted holds.
2. Write it for a business owner, not an accountant, short, in this order:
   - **Headline numbers** - sales, cash and what owners watch first, each with its unit.
   - **Biggest moves since yesterday** - what went up or down, and by how much.
   - **Numbers that disagree** - each in one line: which two systems and how far apart. For the records behind one, use `sorted-fix-conflicts`.
   - **Systems that stopped reporting** - which, and since when.
3. Quote every figure with its currency or unit and the snapshot time. Never invent a number that `daily_brief` did not return; say "not available" instead.
4. If it says there is no data yet, say so plainly: either nothing is connected yet (offer `sorted-onboard`) or the first numbers have not arrived (they come within the hour of connecting). Do not fill the gap with anything else.
5. If a tool returns `billing_required`, follow `sorted-subscription`.
6. End with at most one next step, tied to a number above.

Reply in the owner's language. In Arabic, use natural short phrasing and keep numbers in Latin digits with their units.

Talk in plain words: never show the owner raw tool output, JSON, tool names or error codes; say what happened in one plain sentence. Explain a technical term in a few words the first time you use it.
