---
name: sorted-connect-systems
description: Connect the company's own systems (Odoo, Shopify, Google Ads, Google Analytics 4) so Sorted reads them itself, pressing on in the browser once the owner has signed in. An API key is made only with the owner's explicit approval and never shown in the chat. Use when the owner asks to connect, add or reconnect a system.
---

# Connect a system to Sorted

Sorted reads numbers from the company's systems with read-only access. Only the **company owner** can connect or remove a system, on the Sorted website; you do the clicking in a browser the owner signs in to (without a browser tool, give the owner the steps to follow by hand). The connector tools cannot connect a system. A new owner starts with `sorted-onboard`; this skill covers the four systems Sorted reads itself.

## Before you start (always)

1. Confirm the person is the owner and signed in at https://sortedos.com. If the Connections page (https://sortedos.com/connections) offers no "connect", they are not the owner: say so and stop.
2. Call `list_connections`. Connect only what is missing, such as a company not yet in an existing Odoo connection. Never create a duplicate.

## Hard rules

- **Read-only, always.** Sorted only reads, and you change nothing in the owner's systems beyond the access the owner approved. Where a system offers a read-only role or scope, use it. Odoo is the one exception, below.
- **Look it up, do not ask.** Never ask the owner for a fact the system can show: its plan, version, database name, list of companies or address. Open the system, let the owner sign in, and read it. If its list of companies differs from what the owner said, say so, then let the owner pick which to pull.
- **Few confirmations.** Pause for the owner's yes only at important steps: anything that costs money, deletes something, changes data they did not ask for, or makes an API key. Otherwise, once the owner has signed you in, press on: click Connect, create, fill in, and go to the next system, even if it takes long. One system at a time: finish and check one first.
- **Passwords stay with the owner.** The owner types every password and 2-step code, and handles any captcha, passkey, payment screen or page of terms: stop, ask them to act, wait, then continue. Never ask for a key, password or token in the chat, and never repeat, store or screenshot one. If the owner pastes a secret into the chat by mistake, do not repeat it; tell them to revoke it and make a new one.
- **The one approved exception, an API key.** With the owner's explicit approval, you may create an API key on the owner's own user and copy it from the system's one-time key box into Sorted's connection form yourself, without ever showing it in the chat. While a key or password shows, take no screenshot and describe nothing on the screen. Once the key is in Sorted's form it exists nowhere else: do not keep it in a file or in your notes.

## Odoo

1. **Ask the kind first**, because it decides where to sign in: Odoo Online (sign in at odoo.com; the account page lists the databases and plans), Odoo.sh (sign in to the Odoo.sh dashboard, which shows the production address), or self-hosted Community or Enterprise (the company's own address). Then read the rest there yourself. Odoo says its Online One App Free and Standard plans have no external API, so Sorted cannot connect there; use `sorted-connect-odoo` instead.
2. Read the list of companies (Settings, Users & Companies, Companies), flag any difference from what the owner said, and let the owner pick. Against `list_connections`, add only the companies not yet connected.
3. **No new Odoo user**: it may cost a paid seat. Sorted's code only reads, so a key with the full rights of the owner's own user is acceptable. Say plainly what that means (the key could do whatever the user can) and get a clear yes first.
4. With that yes, make the key in the owner's own Odoo session: the user's Preferences (or My Profile), Account Security, New API Key, named Sorted. Odoo asks the user's password to confirm: the owner types it. Odoo shows a key only once and keys expire: pick the longest duration offered (often about three months), record the date, and tell the owner to renew before it.
5. On Sorted's Connections page choose Odoo; fill in the address, database name, login and the key as the hard rules describe, and press the test button. If the key belongs to an administrator, Sorted shows a plain warning about rights; read it to the owner. Then connect.

## Shopify

1. Shopify gives app access only through its Dev Dashboard (https://dev.shopify.com). The owner signs in there as the **owner of the store**; the app must be made in the same Shopify account as the store, or Shopify refuses it. Read the store address (yourstore.myshopify.com) from the store's admin.
2. Create an app. Under Admin API access scopes add **read_orders** and **read_products** (nothing that writes). Release the version, then install it on the store.
3. In Sorted's Shopify form, fill in the store address and an account name. The approved exception covers the app's Client ID and Client secret too: with the owner's explicit yes, fill them from the app's settings page into Sorted's form, never through the chat. Press the test button; when Sorted shows "Shopify store found", press Connect. Sorted reads sales only, never customers.

## Google Ads

1. After the owner signs in to Google Ads, read the account number (like 123-456-7890) and name there; if there are several accounts, let the owner pick.
2. On Sorted's Connections page choose Google Ads, fill in both, and press the sign-in button. Google opens its own sign-in: the **owner** signs in with the Google account that can open that Ads account, including any 2-step prompt.
3. Google may show an "unverified app" screen; the owner chooses Advanced, then continues. Explain first that Google's only ads permission technically allows changes, and that Sorted only ever reads.
4. Check the account shows as connected. If an agency's manager account blocks it, `sorted-connect-google-ads` lets their own assistant send the numbers instead.

## Google Analytics 4

1. On Sorted's Connections page choose Google Analytics, and read the reader's email address written there.
2. In Google Analytics: Admin, Property access management, then Add users. Add that exact email as a **Viewer** (read-only). No higher role.
3. Read the Property ID (Admin, Property details, a number like 123456789) and enter it on Sorted's form; with several properties, let the owner pick.
4. Sorted checks each property by hand, so a wait on "Waiting for Sorted to confirm" is normal. Tell the owner.

Meta ads, and any other system or spreadsheet, go through a feed: `sorted-connect-meta-ads`, `sorted-connect-any-system`.

## Check it worked

1. Read each system's status on the Connections page. Never say a connection worked until Sorted shows it.
2. After the next hourly refresh, call `get_overview` and report only the numbers it returns, with their units and snapshot time. If a system has no numbers yet, say so.
3. List for the owner what you created in each system (user, app, permission, key) and when each key expires, so they can remove or renew it: disconnecting in Sorted deletes only Sorted's copy of the access.
4. If something goes wrong, report the exact message and the one thing the owner could do next. Do not loop, and never use broader access to make a test pass.

Reply in the owner's language. In Arabic, use natural short phrasing and keep numbers in Latin digits with their units.
