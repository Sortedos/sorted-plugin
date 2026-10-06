---
name: sorted-fix-conflicts
description: Find where two business systems report different numbers (e.g. books vs bank, sales team vs store) and list the exact records to fix, with links. Use when the user asks what doesn't match, what to reconcile, or why two reports differ.
---

# Fix what doesn't match

1. Call `list_conflicts` (worst first).
2. For every conflict marked `bad` or `warn`, call `get_conflict_records` with its id.
3. Answer as a checklist, worst first:
   - **Conflict** - title, the two numbers, the gap, which side to trust and why (use the `why` field).
   - **Records to fix** - each record's reference, date, amount and status, with its link so the user can open it.
   - **Next step** - who in the team should fix it and what exactly they do.
4. If a conflict has no records, say the gap is older than the recent history and link the `more` entry.
5. Keep it to what can be acted on today.
