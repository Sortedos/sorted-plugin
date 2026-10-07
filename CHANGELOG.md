# Changelog

## Unreleased

- New skill `sorted-onboard`, the starting point: it asks "Which software does your company run on?" (spreadsheets included, per company), researches every system, shows one plan (system, route, who checks the numbers), then connects them one by one and chooses the numbers. 14 skills now.
- Seven routes to a system, in order: Sorted reads it itself, a connector built into the assistant app, the vendor's own connector, the vendor's API, a connector someone else built (only after checks and the owner's yes), a file on the owner's computer, a report the owner exports.
- The assistant looks facts up in each system (plan, version, database name, companies, address) instead of asking the owner, and asks only for the kind of Odoo (Online, Odoo.sh or self-hosted) because that decides where to sign in.
- Fewer confirmations: a yes only for steps that cost money, delete something, change data the owner did not ask for, or make a key. Once the owner has signed in, the assistant presses on.
- Companies: the assistant reads the system's own list after sign-in, flags a mismatch with what the owner said, and lets the owner pick. It checks `list_connections` first and connects only what is missing.
- Keys: no new Odoo user (it may cost a paid seat). With the owner's explicit approval the assistant makes an API key on the owner's own user and carries it straight into Sorted's form, never through the chat. This replaces "the owner makes and pastes every key". Odoo keys expire, so the date is recorded and renewed before it. The lint allows only that wording (new rule 3b).
- The six feed skills and `sorted-connect-systems` no longer ask the owner for facts the system can show, and the assistant now does the clicks after sign-in.

## 1.2.0

- Six new skills teach an assistant to send numbers into Sorted through a feed, one per system: Odoo, Shopify, Google Ads, Google Analytics, Meta ads, and any other system.
- The same 13 skills now ship as a Claude Code plugin as well as a Codex plugin, and a guide explains how to connect ChatGPT.
- The connect skill for systems Sorted reads itself is shorter and clearer, and names the feed skills as the route for systems Sorted does not read.
- Skills no longer state a price: the assistant asks Sorted for the current price instead.
- New checks: a leak scan, a skill lint, a drift check between the two plugins, and an offline checker for example feed calls.

## 1.1.0

- Seven skills for Codex: what Sorted is, a business review, cash and collections, connecting a system, fixing numbers that disagree, organising the dashboard, and the subscription.
