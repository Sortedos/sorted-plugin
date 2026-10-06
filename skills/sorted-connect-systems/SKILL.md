---
name: sorted-connect-systems
description: Connect the company's own systems (Odoo, Shopify, Google Ads, Google Analytics 4) so Sorted reads them itself. You prepare read-only access and the form fields that are not secret, in the owner's browser, and the owner pastes every key into Sorted's Connections page himself. Use when the owner asks to connect, add or reconnect a system.
---

# Connect a system to Sorted

Sorted reads numbers from the company's systems with read-only access. Only the **company owner** can connect or remove a system, on the Sorted website; you do the clicking in his browser. The connector tools cannot connect a system, so do not look for one. To see what is already connected, call `list_connections`.

## Before you start (always)

1. Confirm the person is the owner and signed in at https://sortedos.com. If the Connections page (https://sortedos.com/connections) offers no "connect", he is not the owner: say so and stop.
2. Say in two plain sentences what you are about to create in HIS system (a read-only user, an app, a reader permission) and wait for his yes, system by system.
3. You need a browser tool (a browser extension of your assistant app, or computer use). Without one, give the owner the steps below to follow by hand.

## Hard rules

- **Read-only, always.** Never give Sorted the right to change anything. Never create an administrator-level user or access yourself. The one exception is described under Odoo, and only the owner can choose it.
- **The owner handles every secret; you never do.** Never enter, copy, read out, transcribe, repeat or look at a secret (API key, client secret, password, token), and never extract one from a screen picture. You prepare the rest: open the right screens, create the read-only user, app or permission (after his yes), fill in the plain fields (address, database name, login, shop address, account name, account or property number), and open the provider's screen where the owner makes his key. Then tell the owner that he now makes the key himself and pastes it into Sorted's highlighted field, then presses Test. He presses Connect, or you may once he says it is done. If he pastes a secret into the chat by mistake, do not repeat it; tell him to revoke it and make a new one.
- **Hand over for people-only steps.** At a password prompt, a 2-step prompt, a passkey, a captcha, a payment screen or a page of terms, stop and ask the owner to act. Wait, then continue. Never guess a password.
- **One system at a time.** Finish and check one before starting the next.
- **Never invent a number or say a connection worked** until Sorted shows it (see "Check it worked").

## Odoo

1. Sorted's form needs the Odoo address (like https://yourcompany.odoo.com), the database name (not always the company name), a login, and an API key that the owner pastes himself.
2. Two choices, and the OWNER picks. Say both in plain words and ask which:
   - (A) RECOMMENDED: a dedicated read-only user for Sorted. First look in Settings, Users for an existing user with read-only Accounting (a new API key on it needs no extra paid seat). If there is none and the owner agrees, create one: Settings, Users, New, named for Sorted, **read access to Accounting only**, nothing else (this may cost a paid seat).
   - (B) A key on the owner's own administrator account, which Sorted accepts because most owners are administrators. Explain the trade-off first: Sorted only reads, but an Odoo API key carries exactly its user's rights, so if Sorted were ever breached an administrator's key could change the books, while a read-only user's key could change nothing. Only if the owner clearly agrees.
3. Open the chosen user's profile, Account Security, New API Key, with the name Sorted. Stop there: the owner makes the key and pastes it into Sorted himself.
4. On Sorted's Connections page choose Odoo. Step 1: fill in the address and database name. Step 2: fill in the user's login; the owner pastes the key into the highlighted field himself, then presses the test button. If the key belongs to an administrator, Sorted shows a plain warning; the owner reads it and decides. Then connect.
5. If the test fails, say plainly what Sorted answered and what to change. Never retry with a more powerful user without the owner's yes.
6. If his Odoo plan gives no programming access, say so; `sorted-connect-odoo` then lets his own assistant send the numbers instead.

## Shopify

1. Shopify gives app access only through its Dev Dashboard (https://dev.shopify.com). The owner signs in there as the **owner of the store**. The app must be made in the same Shopify account as the store, or Shopify refuses it.
2. Create an app. Under Admin API access scopes add **read_orders** and **read_products** (nothing that writes). Release the version.
3. Install the app on the store.
4. In Sorted's Shopify form, fill in the store address (yourstore.myshopify.com) and an account name, and open the app's settings page in Shopify. The owner pastes the Client ID and the Client secret into Sorted's form himself, then presses the test button. When Sorted shows "Shopify store found", he (or you, once he says so) presses Connect.
5. Sorted reads sales numbers only, never customers.

## Google Ads

1. On Sorted's Connections page choose Google Ads. Enter the account number (like 123-456-7890) and an account name, then press the sign-in button.
2. Google opens its own sign-in. The **owner** signs in with the Google account that can open that Ads account, including any 2-step prompt. Hand over here.
3. Google may show an "unverified app" screen; the owner chooses Advanced, then continues. Explain first that Google's only ads permission technically allows changes, and that Sorted only ever reads.
4. Back on the Connections page, check the account shows as connected. If an agency's manager account blocks it, `sorted-connect-google-ads` lets his own assistant send the numbers instead.

## Google Analytics 4

1. On Sorted's Connections page choose Google Analytics, and read the reader's email address written on that page.
2. In Google Analytics: Admin, Property access management, then Add users. Add that exact email as a **Viewer** (read-only). No higher role.
3. Find the Property ID (Admin, Property details, a number like 123456789) and enter it on Sorted's form.
4. Sorted checks each property by hand first, so "Waiting for Sorted to confirm" for a while is normal. Tell the owner.

## Meta ads and other systems

Sorted does not read Meta ads itself. The owner's own assistant can read them with his own Meta access and send the numbers to Sorted: follow `sorted-connect-meta-ads`. For any other system Sorted does not read: `sorted-connect-any-system`.

## Check it worked

1. Open the Connections page and read each system's status as the page shows it.
2. After the next hourly refresh, call `get_overview` and report only the numbers it returns, with their units and snapshot time. If a system has no numbers yet, say so. Do not guess.
3. The connection status is the proof. Never ask for a key, and never judge one by how it looks.
4. Tell the owner exactly what you created in each of his systems (user, app, permission), so he can remove it later: disconnecting in Sorted deletes only Sorted's copy of the access.

## If something goes wrong

Report the exact message, what you tried, and the one thing the owner could do next. Do not loop, do not work around a refusal, and never use broader access to make a test pass.

Reply in the owner's language. In Arabic, use natural short phrasing and keep numbers in Latin digits with their units.
