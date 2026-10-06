---
name: sorted-cash-and-collections
description: Cash position and collections - who owes the business money, what is overdue, what the business owes, and draft polite chase messages. Use when the user asks about cash, receivables, overdue invoices, debtors, or who to chase.
---

# Cash and collections

1. Call `get_overview` for the headline cash, receivable and payable numbers.
2. Call `get_section` with the company's books (e.g. query "books") and read the customer and supplier tables.
3. Answer:
   - **Cash today** - book cash and money in limbo, with the snapshot time.
   - **Top 5 who owe us** - name, amount, overdue part if shown.
   - **Top 5 we owe** - supplier, amount.
   - **Chase list** - for the top overdue customers, a short, polite reminder message in the user's language (Arabic or English, match the user), ready to send.
4. Never invent balances. If a table is missing, say so.
