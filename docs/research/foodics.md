# Foodics: research note for a future Sorted feed skill

**Foodics** is a point-of-sale system (the till and back-office software of a restaurant or shop) used widely in the Middle East. Sorted's feed documentation names Odoo, Shopify, Google Ads and Google Analytics as the systems Sorted reads itself; Foodics is not among them. Its numbers would therefore reach the dashboard through a **feed** (a named area that the owner's own assistant may send numbers into; see [feed-tools.md](../feed-tools.md)). A future skill must still check Sorted's Connections page first, as the general skill says.

This is a research note, not a skill. It records what Foodics's own public documentation says, checked on **6 October 2026**, so a skill can be written later without guessing. Every statement the documentation did not confirm carries the tag **UNVERIFIED**. A summary of those is at the end.

## 1. Sources (all official Foodics pages, all checked 6 October 2026)

| # | Page and address | Checked | What it was used for |
|---|---|---|---|
| S1 | Foodics MCP Server, https://apidocs.foodics.com/core/mcp_server.html (page footer: "Last Updated: 9/1/2026") | checked 6 October 2026 | The read-only connector for assistants: who can connect, what it covers |
| S2 | Scopes, https://apidocs.foodics.com/core/scopes.html | checked 6 October 2026 | The exact permission names |
| S3 | Introduction, https://apidocs.foodics.com/core/introduction.html | checked 6 October 2026 | Rate limit, blocking rules, UTC time |
| S4 | Orders, https://apidocs.foodics.com/core/resources/orders.html | checked 6 October 2026 | Order fields, statuses, filters, order paging |
| S5 | Pagination, https://apidocs.foodics.com/core/pagination.html | checked 6 October 2026 | 50 per page, the 10-page limit on orders |
| S6 | Accounting/ERP Integration guide, https://developers.foodics.com/guides/Accounting/Accounting-ERP-Integration.html | checked 6 October 2026 | Recommended scopes, how to total sales |
| S7 | Get Started guide, https://developers.foodics.com/guides/get-started.html | checked 6 October 2026 | How access is created, token facts, a second rate limit |
| S8 | Fetching General Data guide, https://developers.foodics.com/guides/fetching-general-data.html | checked 6 October 2026 | Business settings: currency, time zone, tax mode |
| S9 | Order Calculation Formulas guide, https://developers.foodics.com/guides/order-calculation-formulas.html | checked 6 October 2026 | What an order's total contains |
| S10 | API Changelog, https://developers.foodics.com/guides/api-changelog.html | checked 6 October 2026 | The 2021 change in how voided orders appear |
| S11 | Branch Business Days, https://apidocs.foodics.com/core/resources/branch_business_days.html | checked 6 October 2026 | A business day can span two calendar dates |
| S12 | Foodics MCP landing page, https://mcp.foodics.com/ (its page description says "read-only, using your own Foodics account") | checked 6 October 2026 | The vendor's own statement of read-only |

**Pages that could not be read.** Foodics's help-center articles (for example the one defining user roles, on help.foodics.com) refused the fetch with an access-denied answer on 6 October 2026, and an older help site answered "payment required". Nothing from them is used here. A search-engine snippet mentioned a "Read-Only" user role in the Foodics console; that is **UNVERIFIED**.

## 2. How read-only access is made

Two routes exist in the official pages. A third (a report exported by the owner) is the fallback the general skill already describes.

**Route A, the Foodics MCP server (best fit).** MCP is the standard plug that lets an assistant use another service's tools. Foodics runs one: S1 says it "gives AI assistants read-only access to your Foodics account through a set of search and report tools" and "can only read your Foodics data — it cannot create, edit, or delete anything in your account". S12 repeats "read-only". Sign-in is OAuth (the owner approves the connection in a browser window, and no password or key is shared with the assistant). **Who can grant it:** S1 says "You must sign in with a Foodics owner account. Foodics rejects non-owner sign-ins at the OAuth step." It can be added to Claude, to Cursor-style clients that read a config file, and to ChatGPT through a developer-mode app (S1 gives the steps; ChatGPT screens are covered by [chatgpt-connector.md](../chatgpt-connector.md)). The names of the individual tools are **not published** on the pages read: UNVERIFIED. How Foodics enforces read-only is not described: the promise is Foodics's, a skill can only rely on it and still use reading tools only.

**Route B, an API app with read scopes.** A **scope** is a permission label an app asks for, and the access token it receives is limited to the scopes granted (S2). S6 recommends these for accounting-style reading: `general.read`, `orders.list`, `inventory.transactions.read`, `inventory.settings.read`, `menu.ingredients.read`, `customers.accounts.read`, plus `tokens.limited.revoke` (it only revokes the app's own tokens). For the numbers in section 3 only `general.read` and `orders.list` are needed (S4: listing orders needs "orders.list OR orders.limited.read"). `operations.read` is only needed for business-day records (S11).
- **Who creates the app:** S7 says developer applications "are created by Foodics team after obtaining some needed information from the developer", and that the integration scope given to Foodics "will define your Application API Scopes". So an owner cannot make a private read-only key himself from these pages; a partner app that Foodics already created is needed, and Foodics's team decides its scopes (S2: "Your app scopes will be defined by Foodics team").
- **Who grants it:** a Foodics user presses Authorize on a consent screen that lists the scopes (S2, S7). Which user role may do this is **UNVERIFIED** for the API route.
- **What cannot be made read-only:** the same scope list contains write scopes such as `customers.write`, `menu.write`, `operations.write`, `inventory.transactions.write`, `orders.limited.create`, `orders.limited.pay` and `orders.limited.deliver`. An app that Foodics created with any of them can change data. The owner must read the scope list on the consent screen and refuse anything that is not a reading scope. The word "limited" in `orders.limited.read` is not explained on the pages read (it may only show orders the app itself created): **UNVERIFIED**, so prefer `orders.list` for sales totals.
- **The token does not expire** (S7: "Token doesn't expire") until the owner revokes it in the Foodics console or the app revokes it. A reading token that is no longer needed must be revoked.

If neither route is possible, the owner exports a sales report from the Foodics console and shares the file. The export formats are **UNVERIFIED** (help pages not readable).

## 3. Numbers a feed could carry

Amounts in Foodics come as JSON numbers of type "double" (S4), not as text. Money is in the business's own currency, given by `business_currency` in the settings (S8). Orders are listed with `GET /orders` (S4); the filters used below are `business_date`, `status`, `branch_id`.

| Label | Unit | How it is computed (names as Foodics writes them) | The trap |
|---|---|---|---|
| Sales | `money` (the business's currency) | `GET /orders` for one `business_date`: sum `total_price` of orders with `status` 4 (Closed), minus `total_price` of orders with `status` 5 (Returned). This is the rule in S6. | `total_price` includes charges, taxes and rounding (S9: order sums = products + charges + taxes - discount, then rounding). Prices in the product list are before tax when `tax_inclusive_pricing` is false (S8). Say in the label whether it includes tax. Whether a returned order's `total_price` is stored positive is UNVERIFIED. |
| Receipts | `count` | Same call: number of orders with `status` 4, minus number with `status` 5 (S6 calls this the net count). | Orders with `status` 3 (Declined), 6 (Joined), 8 (Draft) are left out; that none of them carries sales is UNVERIFIED. Before 13 January 2021 a void appeared as a closed order whose products were all at `status` 5, and Foodics's 2021 note says some branches kept that behaviour until their cashier app was updated (S10), so an order whose products are all status 5 is void. Whether any branch still behaves that way today is UNVERIFIED. |
| Average receipt | `money` | Sales divided by Receipts, computed by the assistant after the two numbers above. | Send `null` when Receipts is 0, never 0. Round to the currency's usual decimals only at the end. |
| Refunds | `money` | Sum of `total_price` of orders with `status` 5 (Returned) for the day; send it as a negative number, as the feed docs allow for refunds. | A return is on its own order (`original_order`); which `business_date` it carries (the return day or the sale day) is UNVERIFIED. |
| Discounts | `money` | Order-level `discount_amount`, plus each product line's `discount_amount` (and combo `discount_amount`), as listed in the S6 attribute table. | Whether the order-level figure already includes the product-level ones is UNVERIFIED. Check one day against the Foodics console before sending. |
| Tips | `money` | Sum of `payments.tips` over the day's orders (S6 lists tips under `payments`). | A tip is a separate field, not part of `total_price` in the vendor's sample. That this is always so is UNVERIFIED. Payment `amount` is what the customer paid; `tendered` includes change (S4), so never use `tendered`. |
| Sales by payment method | `money` (table: one row per method) | Same orders with `include=payments.payment_method`; sum payment `amount` by the method's `name`. | A payment has its own `business_date` (S4) that can differ from the order's. Orders paid with two methods appear in two rows. |
| Sales by order type | `money` (table: Dine In, Pick Up, Delivery, Drive Thru) | Sum `total_price` of closed orders grouped by `type` 1 to 4 (S4). | Use the same status rule as Sales, or the table will not add up to it. |
| Returned orders | `percent` | Count of `status` 5 orders divided by count of `status` 4 orders, times 100 (12.5 means 12.5%). | `null` when there are no closed orders. |
| Voided orders | `count` | Orders with `status` 7 (Void), plus orders whose products are all `status` 5 (S10). | The two ways of recording a void (new and old cashier app) must both be counted once. |

**Through Route A** the vendor lists reports for "net sales, order counts, average order value, discounts, returns, and business days reports, groupable by date range, branch, or category" and breakdowns "by fulfillment type (dine-in, pickup, delivery, drive-thru) and payment method" (S1). These match Sales, Receipts, Average receipt, Discounts, Refunds, Sales by order type and Sales by payment method above. The tool names are UNVERIFIED, and what "net sales" means (before or after tax, charges, tips) is **UNVERIFIED**: compare one day with the Foodics console and write the meaning into the label.

**Suggested feed shape.** One table feed, rows are branches, columns Sales, Receipts, Average receipt, Refunds (the shape in the general skill). Sorted allows at most 40 cells and 8 columns, so 4 columns fit 10 branches; a larger chain needs the busiest branches in one feed and the rest in another, or totals only. `as_of` is the business date. Branch names are business data, not personal data.

## 4. Limits and known traps

- **Rate limit: the official pages disagree.** The API introduction (S3) says "90 requests per minute per access token per IP address". The Get Started guide (S7) says "30 requests per minute per access token per IP address". Both were read on 6 October 2026. Use the lower number until Foodics clears it up. Foodics sends `X-RateLimit-Limit` and `X-RateLimit-Remaining` headers, and on 429 ("Too Many Attempts") a `retry-after` header in seconds (S3).
- **Blocking.** More than 10 consecutive 429 answers inside 10 seconds blocks the address for 60 seconds. More than 60 invalid requests (401 or 403) inside 60 seconds blocks it for 1 hour. On 401 Foodics says to stop the integration at once; on 403 do not retry (S3).
- **Paging.** Lists return 50 objects per page (S5). `GET /orders` is different: paging with `page` stops after page 10 (500 orders). Foodics tells you to send `sort=reference` and `filter[reference_after]=<last reference you handled>` on every orders request (S4, S5, S6). A busy branch can exceed 500 orders in a day, so a skill must page this way.
- **Time zones.** All timestamp fields are in UTC (S3: "Foodics API timing is UTC"), written `YYYY-MM-DD HH:MM:SS`. The business's own offset is `business_timezone` in `GET /settings` (S8, shown there as "+03:00"). `business_date` is a plain date. A business day can run past midnight: Foodics's own sample opens at 07:48 on 9 December and closes at 10:23 on 10 December (S11). **Slice days by `business_date`, never by `closed_at`.**
- **Currency and money.** One business currency (`business_currency`, S8). The same settings also list `cashier_tendered_amount_currencies`, so cash may be taken in another currency; how that appears in order totals is UNVERIFIED. Tax amounts can have more than two decimals in Foodics's samples (for example 0.35217, S6), so add first and round last.
- **Tax mode.** `tax_inclusive_pricing` in `GET /settings` says whether product prices already contain tax (S8).
- **Deleted objects.** Foodics's own test list tells integrators to ignore or handle deleted objects and nullable fields (S6). Many list calls take an `is_deleted` filter (S8).
- **Statuses.** Orders: 1 Pending, 2 Active, 3 Declined, 4 Closed, 5 Returned, 6 Joined, 7 Void, 8 Draft (S4).
- **Sandbox.** Foodics gives developers a separate sandbox address and test account (S7). A future skill is tested on invented data only; no real business is needed.
- **Credentials.** Never ask for the access token or app secret in the chat. On Route A there is nothing to paste.

## 5. UNVERIFIED, in one list

1. Names of the Foodics MCP server's tools, and what its "net sales" report includes.
2. Which Foodics user role may authorize an API app (Route B).
3. What "limited" means in `orders.limited.read`.
4. Whether a Foodics "Read-Only" console role exists (only a search snippet mentioned it; the help pages refused the fetch).
5. Which rate limit is right, 30 or 90 per minute.
6. Sign and `business_date` of a returned order; whether order-level discount already includes product-level discounts; whether tips are ever inside `total_price`.
7. Export formats of the console's reports.
8. Whether any branch still records voids the pre-2021 way, and how cash taken in a second currency shows in totals.

No skill yet: this note prepares one.
