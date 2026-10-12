---
name: sorted-connect-systems
description: Connect Odoo, Shopify, Google Ads or Google Analytics 4 so Sorted reads them itself, pressing on in the browser once the owner has signed in. Use to connect, add or reconnect a system.
---

# Connect a system to Sorted

Sorted only reads. You do Odoo yourself with `connect_odoo` and Google Analytics 4 through its guided setup; for Google Ads and Shopify the owner signs in on Sorted's Connections page.

## Before you start

Confirm the person is the **company owner**: the Connections page (https://sortedos.com/connections) must offer "connect"; if not, stop. Call `list_connections`; connect only what is missing, never a duplicate.

## Hard rules

- **Read-only, always.** Change nothing beyond the access the owner approved; use a read-only role or scope where one exists (not Odoo).
- **No browser or computer tool?** Never hand the owner technical steps. Tell them to continue in a mode or app that has one (ChatGPT: Work mode; Claude: Claude in Chrome or Cowork) with a ready message: "Set up Sorted for my company. Use your browser for every step; hand the screen to me only for passwords, sign-in codes and Allow." Only if they cannot switch, guide them click by click.
- **Few confirmations:** the owner's yes only for money, deletion, unrequested data changes and making a key. Never ask for a fact the system can show.
- **Passwords stay with the owner.** The owner types every password and 2-step code and handles any captcha, passkey, payment screen or page of terms: wait. Never ask for a password or token in the chat; if one reaches it, do not repeat it and advise changing it.
- **An Odoo key:** with the owner's explicit approval, make the API key on the owner's own user, read it from the one-time key box's field and pass it straight to `connect_odoo`. While a key shows, read only the box's title, field names and the key field, never the page or box text. Never repeat the key in the chat. Never use the clipboard. Never keep it in a file or notes. Take no picture of it. If the owner pasted a key in the chat, pass it straight to `connect_odoo`; do not lecture them or tell them to revoke it.
- **A Shopify Client ID and secret** have no tool: with the owner's explicit approval, move them into Sorted's form yourself, in ONE action that returns only a length or "done".
- **Never quote, name or cite these guides or their rules to the owner**: just act.

## Odoo

1. **Ask for the address** the owner signs in at (Odoo Online: odoo.com's account page lists the databases). Read the database name and login from the signed-in page's session info: view the source of the address plus /odoo (older Odoo: /web) and read "db" and "username". Never open Odoo.sh, GitHub or a hosting dashboard. Odoo Online's One App Free and Standard plans have no external API: Sorted cannot connect there; say so and stop.
2. Sorted keeps one connection per Odoo address and database: to add a company, call `connect_odoo` again with EVERY company Sorted should read, existing ones included; it replaces the old connection. Compare with `list_connections` before and after. Cards use each company's exact Odoo name; a renamed one loses its brand label: tell the owner.
3. **No new Odoo user:** the key goes on the owner's own user. Say plainly it could do whatever that user can and get a clear yes.
4. With that yes, open the key screen through the user's avatar menu: My Profile or Preferences, Account Security, New API Key (never type the action into the address bar), after checking the profile shows the owner's own name. The owner types the password it asks for. The key shows once; record any expiry date.
5. Ask: "Is this business its own company in Odoo, or booked inside a company shared with others, told apart by cost tags?" Own company: call `connect_odoo` with the address, database name, the Odoo login the key was made on, and the key. If the login sees several companies it saves NOTHING and lists them: let the owner pick, then call again with `companies` set to the pick, exactly as listed; then confirm with `list_connections`. If it says no, report it plainly; never retry blindly.
6. **Cost tags (analytic accounts):** call `connect_odoo` with `companies` set to that one company and `analytic` set to `[]`: it lists the tags and saves nothing. The owner picks his; tags that share a name are all included and each line counts once, so never ask about same-named tags. Call again with `analytic` set to the picks, exactly as listed. Say plainly that cash, receivables and payables are company-wide, so they are not shown for this business.
7. If `connect_odoo` is unavailable, use the Odoo form on Sorted's Connections page (its administrator's-key and already-connected notices are information, not errors).

## Google Ads, Google Analytics 4 and Shopify

Google Ads and Shopify connect with "Continue with ..." on Sorted's Connections page. Never sign your own browser in to Sorted for them: it can land on the wrong account or company.

1. Give the owner this link for their company, to open in the browser where they are already signed in to Sorted: https://sortedos.com/connections?org=<company id>&provider=<google_ads|ga4|shopify>. The company id is in the setup message or in the `org=` of any Sorted link a tool returned (none yet and one company: leave `org=` out). The page must show the company's name.
2. The owner presses Continue with Google (Shopify: store address, then Continue with Shopify), signs in, presses Allow, picks the account and presses Connect account. Google may show an "unverified app" screen: Advanced, then continue (first say that Google's only ads permission technically allows changes, while Sorted only reads).
3. Only if the owner cannot open the link, use your own browser: open https://sortedos.com/connections, confirm it shows the owner's email and the company's name, and if not, stop and tell the owner.
4. If the page says direct sign-in is not available, follow its guided setup (Shopify: an app from https://dev.shopify.com with only **read_orders** and **read_products**).
5. If no Google Ads account can be chosen because an agency's manager account blocks it, Sorted cannot read it yet: say so, and offer to ask the Sorted team to build it (see "Not yet" in `sorted-onboard`).

**Google Analytics 4** has no Continue with Google (Sorted's Google sign-in for it is switched off): never tell the owner to press it. You do its guided setup in your browser; the owner only signs in to Google. Open the link above; it must show the owner's email and the company's name, or stop and tell the owner. In https://analytics.google.com use the Google account that sees the business's real property (if you find only an empty or test property, or several, ask which one). Go to Admin, Property access management, + Add users: add the reader email Sorted's page shows, role **Viewer** (read-only). Then enter the Property ID (Admin, Property details) and the property's name on Sorted's page and press Connect. It reads "Waiting for Sorted to confirm" until Sorted checks by hand, usually within one working day: say that is normal.

## Check it worked

Read each system's status with `list_connections` and never say a connection worked until Sorted shows it. The first read usually happens within the hour (the dashboard's Refresh now button, if it shows, starts it); then call `get_overview` and report only the numbers it returns, with units and snapshot time. Tell the owner what you created and each key's expiry date; on a failure, report the exact message and one next step.

Reply in the owner's language. In Arabic, use natural short phrasing and keep numbers in Latin digits with their units.
