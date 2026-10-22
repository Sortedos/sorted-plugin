---
name: sorted-cash-and-collections
description: Shows the cash position and collections - who owes the business money, what is overdue, what the business owes, and draft polite chase messages. Use when the user asks about cash, receivables, overdue invoices, debtors, or who to chase.
---

# Cash and collections

Answer in the language the person writes in. If they write Egyptian Arabic, answer in Egyptian colloquial Arabic; for other Arabic, answer in the same kind of Arabic. Keep numbers in Latin digits with their units.

No Sorted tools in this chat? Sorted is not connected yet: follow `sorted-not-connected`.

1. Call `get_overview` for the headline cash, receivable and payable numbers.
2. Call `get_section` with the company's books (e.g. query "books") and read the customer and supplier tables.
3. Answer:
   - **Cash today** - book cash and money in limbo, with the snapshot time.
   - **Top 5 who owe us** - name, amount, overdue part if shown.
   - **Top 5 we owe** - supplier, amount.
   - **Chase list** - for the top overdue customers, a short, polite reminder message written in the CUSTOMER's language (their Odoo language when known), ready to send, plus a one-line translation in the owner's language for the owner to check before sending.
4. Never invent balances. If a table is missing, say so. If a guide says a number is missing, try `live_read` before saying it is not available (for example, a count of overdue invoices).

If the owner is stuck after these steps, ask once per conversation: "Shall I tell the Sorted team about this?" Only on a clear yes, send it as `sorted-about` says; never make two offers in one reply.

Talk in plain words: never quote raw tool output, JSON, tool names or error codes to the person you are helping; say what happened in one plain sentence. Explain a technical term in a few words the first time you use it.
