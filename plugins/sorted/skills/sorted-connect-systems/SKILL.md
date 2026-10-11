---
name: sorted-connect-systems
description: Connect Odoo, Shopify, Google Ads or Google Analytics 4 so Sorted reads them itself. For Odoo you make the API key (after the owner's explicit yes) and pass it to Sorted's connect_odoo tool. Use to connect, add or reconnect a system.
---

# Connect a system to Sorted

Sorted reads the company's systems, read-only. Only the **company owner** can connect or remove one. For Odoo you do every step yourself with `connect_odoo`; for the others you click in a browser the owner signs in to. A new owner starts with `sorted-onboard`.

## Before you start

1. Confirm the person is the owner, signed in at https://sortedos.com. If the Connections page (https://sortedos.com/connections) offers no "connect", they are not: stop and say so.
2. Call `list_connections`. Connect only what is missing, never a duplicate.

## Hard rules

- **Read-only, always.** Change nothing in the owner's systems beyond the access they approved; use a read-only role or scope where one exists (Odoo is the exception).
- **Look it up, do not ask.** Never ask the owner for a fact the system can show.
- **Few confirmations.** Pause for the owner's yes only for money, deletion, unrequested data changes and making a key. Once signed in, press on, system after system, checking each before the next.
- **Passwords stay with the owner.** The owner types every password and 2-step code and handles any captcha, passkey, payment screen or page of terms: stop, ask them to act, wait. Never ask for a password or token in the chat; if one reaches it (an Odoo key is the exception), do not repeat it and advise changing it.
- **An Odoo key:** with the owner's explicit approval, make the API key on the owner's own user, read it from the one-time key box's field and pass it straight to `connect_odoo` (the owner copies nothing). While a key shows, read only the box's title, field names and the key field, never the page or box text. Never repeat the key in the chat. Never use the clipboard (its history keeps a copy). Never keep it in a file or notes. Take no picture of it. If the owner pasted a key in the chat, pass it straight to `connect_odoo`; do not lecture them or tell them to revoke it.
- **A Shopify Client ID and secret** have no tool: with the owner's explicit approval, move them from the app's settings page into Sorted's form yourself, in ONE action that returns only a length or "done", never showing them in the chat.

## Odoo

1. **Ask the kind first**, because it decides where to sign in: Odoo Online (sign in at odoo.com; the account page lists the databases and plans), Odoo.sh (its dashboard shows the production address), or self-hosted (the company's own address). `connect_odoo` names the kind it detects: if the owner's answer differs, say so plainly. Odoo's Online One App Free and Standard plans have no external API: there use `sorted-connect-odoo`.
2. Read the companies (Settings, Users & Companies, Companies), flag any difference from what the owner said, and let them pick. Sorted keeps one connection per Odoo address and database: to add a company, call `connect_odoo` again with EVERY company Sorted should read, existing ones included (same key, or a new one with the owner's yes); the new connection replaces the old. Compare with `list_connections` before and after. Cards carry each company's exact Odoo name, so a renamed or recapitalised company can lose its brand label: if one looks wrong, tell the owner.
3. **No new Odoo user** (it may cost a paid seat). Sorted only reads, so a key with the owner's own full rights is acceptable: say plainly that it could do whatever the user can, and get a clear yes.
4. With that yes, open the key screen through the user's avatar menu: My Profile or Preferences, then Account Security, then New API Key. Never type the action into the address bar (on Odoo 17 it opened an empty new-user form and New API Key failed). Before pressing anything, check the profile shows the owner's own name.
5. New API Key opens a "Security Control" box that asks for the owner's password: the owner types it. Next a description (suggest "Sorted - Acme Trading"), then "API Key Ready" shows the key once. Keys expire: record any date Odoo shows and have the owner renew before it.
6. Call `connect_odoo` with the address, database name, the Odoo login the key was made on, and the key. It checks the login and saves the connection: nothing more to click. If the login sees several companies it saves NOTHING and lists them: let the owner pick, then call again with `companies` set to the pick, exactly as listed. Tell the owner its answer (companies connected, numbers within minutes, kind of Odoo, and for an administrator's key that it could do whatever that user can while Sorted only reads), then confirm with `list_connections`. If it says no, report it plainly; never switch to a user with more rights or retry blindly (10 tries an hour).
7. No browser tool for the key? The owner can make it (steps 4 and 5) and paste it in the chat. If `connect_odoo` is unavailable, or the owner prefers, use Sorted's Connections page: choose Odoo, fill in the form, press "Test the connection" (its administrator's-key and already-connected notices are information, not errors), tick the companies, press Connect.

## Shopify

1. App access is only through Shopify's Dev Dashboard (https://dev.shopify.com): the owner signs in as the **owner of the store**, and the app is made in the store's own Shopify account. Read the store address from its admin.
2. Create an app with only the Admin API access scopes **read_orders** and **read_products**, release the version and install it on the store.
3. In Sorted's Shopify form fill in the store address and an account name, press the test button and, at "Shopify store found", Connect. The Shopify rule above covers the Client ID and secret.

## Google Ads

1. Once signed in to Google Ads, read the account number and name (several accounts: the owner picks). On Sorted's Connections page choose Google Ads, fill in both and press the sign-in button; the **owner** signs in with the Google account that can open that Ads account, 2-step prompt included.
2. At an "unverified app" screen the owner chooses Advanced, then continues; first explain that Google's only ads permission technically allows changes, and Sorted only reads.
3. If an agency's manager account blocks it, `sorted-connect-google-ads` lets their assistant send the numbers.

## Google Analytics 4

1. On Sorted's Connections page choose Google Analytics and read the reader's email address shown.
2. In Google Analytics: Admin, Property access management, Add users. Add that exact email as a **Viewer** (read-only), no higher role.
3. Read the Property ID (Admin, Property details) and enter it on Sorted's form (several properties: the owner picks). Sorted checks each by hand, so "Waiting for Sorted to confirm" is normal: tell the owner.

## Check it worked

1. Read each system's status on the Connections page; never say a connection worked until Sorted shows it.
2. After the next hourly refresh call `get_overview` and report only the numbers it returns, with units and snapshot time (say so if a system has none yet).
3. List what you created in each system and each key's expiry date, so the owner can remove or renew it: disconnecting in Sorted deletes only Sorted's copy of the access.
4. On a failure, report the exact message and one next step; never loop or use broader access to make a test pass.

Reply in the owner's language. In Arabic, use natural short phrasing and keep numbers in Latin digits with their units.
