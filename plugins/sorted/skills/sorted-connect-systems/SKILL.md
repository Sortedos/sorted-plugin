---
name: sorted-connect-systems
description: Connect Odoo, Shopify, Google Ads or Google Analytics 4 so Sorted reads them itself, pressing on in the browser once the owner has signed in. An API key is made only with the owner's explicit approval and never shown in the chat. Use when the owner asks to connect, add or reconnect a system.
---

# Connect a system to Sorted

Sorted reads the company's systems with read-only access. Only the **company owner** can connect or remove a system, on the Sorted website; you click in a browser the owner signs in to. A new owner starts with `sorted-onboard`; this skill covers the four systems Sorted reads itself.

## Before you start

1. Confirm the person is the owner, signed in at https://sortedos.com. If the Connections page (https://sortedos.com/connections) offers no "connect", they are not: say so and stop.
2. Call `list_connections`. Connect only what is missing, never a duplicate.

## Hard rules

- **Read-only, always.** Sorted only reads, and you change nothing in the owner's systems beyond the access they approved; use a read-only role or scope where one exists (Odoo is the exception).
- **Look it up, do not ask.** Never ask the owner for a fact the system can show (plan, version, database name, companies, address): open it, let the owner sign in, read it.
- **Few confirmations.** Pause for the owner's yes only for money, deletion, data changes they did not ask for, and making a key. Once signed in, press on, system after system, however long it takes; finish and check one before the next.
- **Passwords stay with the owner.** The owner types every password and 2-step code and handles any captcha, passkey, payment screen or page of terms: stop, ask them to act, wait. Never ask for a key, password or token in the chat, and never repeat, store or screenshot one. If a secret ever reaches the chat, by paste or slip, do not repeat it; tell the owner and advise revoking it and making a new one.
- **The one approved exception, an API key.** With the owner's explicit approval, you may create an API key on the owner's own user and move it from the system's one-time key box into Sorted's key field yourself, in ONE action that returns only a length or "done" (read the box's field into a variable and set Sorted's field from it), without ever showing it in the chat.
- **While a key shows**, read only the box's title and field names, never the page or box text. Take no picture of it, never print it, and never use the clipboard, whose history would hold a copy. Afterwards it exists nowhere else: keep it in no file or notes.

## Odoo

1. **Ask the kind first**, because it decides where to sign in: Odoo Online (sign in at odoo.com; the account page lists the databases and plans), Odoo.sh (sign in to the Odoo.sh dashboard, which shows the production address), or self-hosted Community or Enterprise (the company's own address). Then read the rest there yourself. Odoo says its Online One App Free and Standard plans have no external API: there use `sorted-connect-odoo`.
2. Read the companies (Settings, Users & Companies, Companies), flag any difference from what the owner said, and let the owner pick. Sorted's Connections page cannot change the companies of an existing Odoo connection (only Disconnect): to add one, make a new key and add a SECOND Odoo connection with only the missing companies, the owner approving the key. Sorted allows two Odoo connections on one database.
3. **No new Odoo user** (it may cost a paid seat). Sorted's code only reads, so a key with the full rights of the owner's own user is acceptable. Say plainly what that means (the key could do whatever the user can) and get a clear yes.
4. With that yes, open the key screen through the user's avatar menu: My Profile or Preferences, then Account Security, then New API Key. Never type the action into the address bar: on Odoo 17 that opened an empty new-user form, and New API Key then tried to create a record ("Contacts require a name"). Before pressing anything, check the profile shows the owner's own name.
5. New API Key opens a "Security Control" box ("confirm you own this account") that asks for the owner's password: the owner types it. Next a description (suggest "Sorted - Acme Trading", the company's own name), then "API Key Ready" shows the key once. Existing keys are listed by description and date only. Keys expire: record any date Odoo shows and tell the owner to renew before it.
6. On Sorted's Connections page choose Odoo; fill in the address, database name, login and the key (rules above), then press "Test the connection". Sorted may say "This is an administrator's key..." and "This system is already connected to" another company. Both are information, not errors: tell the owner in one line, continue to the company list (Step 3 of 3), tick only the companies the owner picked, press Connect, then confirm with `list_connections`.

## Shopify

1. Shopify gives app access only through its Dev Dashboard (https://dev.shopify.com); the owner signs in as the **owner of the store**, and the app must be made in the same Shopify account as the store. Read the store address from the store's admin.
2. Create an app with only the Admin API access scopes **read_orders** and **read_products**, release the version and install it on the store.
3. In Sorted's Shopify form fill in the store address and an account name. The key exception covers the app's Client ID and Client secret too, under the same box rules: with the owner's explicit yes, move them from the app's settings page into Sorted's form, never through the chat. Press the test button; at "Shopify store found", press Connect.
## Google Ads

1. Once the owner has signed in to Google Ads, read the account number and name (with several accounts, the owner picks). On Sorted's Connections page choose Google Ads, fill in both and press the sign-in button. The **owner** signs in with the Google account that can open that Ads account, 2-step prompt included.
2. At an "unverified app" screen the owner chooses Advanced, then continues; explain first that Google's only ads permission technically allows changes, and Sorted only ever reads.
3. Check the account shows as connected. If an agency's manager account blocks it, `sorted-connect-google-ads` lets their own assistant send the numbers instead.

## Google Analytics 4

1. On Sorted's Connections page choose Google Analytics and read the reader's email address written there.
2. In Google Analytics: Admin, Property access management, Add users. Add that exact email as a **Viewer** (read-only), no higher role.
3. Read the Property ID (Admin, Property details) and enter it on Sorted's form; with several properties, let the owner pick. Sorted checks each by hand, so a wait on "Waiting for Sorted to confirm" is normal: tell the owner.

## Check it worked

1. Read each system's status on the Connections page; never say a connection worked until Sorted shows it.
2. After the next hourly refresh call `get_overview` and report only the numbers it returns, with units and snapshot time (say so if a system has none yet).
3. List what you created in each system (user, app, permission, key) and each key's expiry date, so the owner can remove or renew it: disconnecting in Sorted deletes only Sorted's copy of the access.
4. On a failure, report the exact message and one next step; never loop or use broader access to make a test pass.

Reply in the owner's language. In Arabic, use natural short phrasing and keep numbers in Latin digits with their units.
