# Changelog

## Unreleased

- Install steps corrected (10 October 2026). Codex and Claude Code now add the plugin straight from GitHub (`codex plugin marketplace add Sortedos/sorted-plugin`, `claude plugin marketplace add Sortedos/sorted-plugin`), so no download is needed; the old `.` and `./` forms only work inside a copy of this repository and stay as a note for people who work from a copy. Claude on the web or the desktop app now has a plugin route (Customize, Plugins, Add marketplace, Add from a repository) next to the connector route. The ChatGPT guide says to install the plugin from your personal plugins, because Sorted is not in ChatGPT's own directory.
- New skill `sorted-onboard`, the starting point: it asks "Which software does your company run on?" (spreadsheets included, per company), researches every system, shows one plan (system, route, who checks the numbers), then connects them one by one and chooses the numbers. 14 skills now.
- Seven routes to a system, in order: Sorted reads it itself, a connector built into the assistant app, the vendor's own connector, the vendor's API, a connector someone else built (only after checks and the owner's yes), a file on the owner's computer, a report the owner exports.
- The assistant looks facts up in each system (plan, version, database name, companies, address) instead of asking the owner, and asks only for the kind of Odoo (Online, Odoo.sh or self-hosted) because that decides where to sign in.
- Fewer confirmations: a yes only for steps that cost money, delete something, change data the owner did not ask for, or make a key. Once the owner has signed in, the assistant presses on.
- Companies: the assistant reads the system's own list after sign-in, flags a mismatch with what the owner said, and lets the owner pick. It checks `list_connections` first and connects only what is missing.
- Keys: no new Odoo user (it may cost a paid seat). With the owner's explicit approval the assistant makes an API key on the owner's own user and carries it straight into Sorted's form, never through the chat. This replaces "the owner makes and pastes every key". Odoo keys expire, so the date is recorded and renewed before it. The lint allows only that wording (new rule 3b).
- The six feed skills and `sorted-connect-systems` no longer ask the owner for facts the system can show, and the assistant now does the clicks after sign-in.
- Key box rule: while a system shows a newly made key, the assistant reads only the box's title and field names (never the page or box text), takes no picture, never prints the key and never uses the clipboard, and moves the key from the system's one-time box into Sorted's key field in ONE action that returns only a length or "done". A page-text read once printed a fresh key into a session record; the lint (rules 3c and the required key box lines) now blocks this wording.
- Odoo steps, from a live trial on Odoo 17: open the key screen through the avatar menu (My Profile or Preferences, Account Security, New API Key), never by typing the action into the address bar (that opened an empty new-user form), and check the profile shows the owner's own name first. New API Key asks for the owner's password, then a description, then shows the key once.
- Adding a company: Sorted keeps one connection per Odoo address and database, and connecting again replaces it. To add a company, connect again with a new key (the owner approves it) and tick EVERY company Sorted should read, the ones already connected plus the new one. Compare the ticked list with `list_connections` before pressing Connect, and confirm with it afterwards that every company is still there. Sorted labels each company's cards by its exact Odoo name, so a renamed or differently capitalised company can lose its brand label: if a brand looks wrong after reconnecting, the assistant tells the owner. The lint rejects any skill text that claims one Odoo address and database can hold two connections.
- Sorted's test step: "This is an administrator's key..." and "already connected to <another company>" are information, not errors; continue to the company list (Step 3 of 3), tick only the companies the owner picked, press Connect, confirm with `list_connections`.
- The feed skills now say the owner puts a key into the assistant app's connector settings, and the assistant reads nothing off the key box.

## 1.2.0

- Six new skills teach an assistant to send numbers into Sorted through a feed, one per system: Odoo, Shopify, Google Ads, Google Analytics, Meta ads, and any other system.
- The same 13 skills now ship as a Claude Code plugin as well as a Codex plugin, and a guide explains how to connect ChatGPT.
- The connect skill for systems Sorted reads itself is shorter and clearer, and names the feed skills as the route for systems Sorted does not read.
- Skills no longer state a price: the assistant asks Sorted for the current price instead.
- New checks: a leak scan, a skill lint, a drift check between the two plugins, and an offline checker for example feed calls.

## 1.1.0

- Seven skills for Codex: what Sorted is, a business review, cash and collections, connecting a system, fixing numbers that disagree, organising the dashboard, and the subscription.
