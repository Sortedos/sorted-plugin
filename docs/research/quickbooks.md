# QuickBooks Online: research note for a future Sorted feed skill

**QuickBooks Online** is Intuit's accounting software (the books of a small company: invoices, bills, bank accounts, reports). Sorted's feed documentation names Odoo, Shopify, Google Ads and Google Analytics as the systems Sorted reads itself; QuickBooks Online is not among them. Its numbers would therefore reach the dashboard through a **feed** (a named area that the owner's own assistant may send numbers into; see [feed-tools.md](../feed-tools.md)). A future skill must still check Sorted's Connections page first, as the general skill says.

This is a research note, not a skill. It records what Intuit's own public documentation says, checked on **6 October 2026**, from documentation only: no QuickBooks account, connector or sandbox company was touched. Every statement the documentation did not confirm carries the tag **UNVERIFIED**. A summary of those is at the end.

**Plain-words key.** *API*: the data service a program uses to read a system. *Scope*: a permission label an app asks for. *OAuth*: the sign-in flow where the owner approves access in the vendor's own window and shares no password. *Realm ID*: QuickBooks's number for one company file. *Endpoint*: one address of the data service.

## 1. Sources (all checked 6 October 2026)

| # | Page and address | Checked | What it was used for |
|---|---|---|---|
| Q1 | Learn about scopes, https://developer.intuit.com/app/developer/qbo/docs/learn/scopes | checked 6 October 2026 | The permission names, and the absence of a read-only accounting scope |
| Q2 | Set up OAuth 2.0, https://developer.intuit.com/app/developer/qbo/docs/develop/authentication-and-authorization/oauth-2.0 | checked 6 October 2026 | Sign-in flow, token lifetimes |
| Q3 | API call limits and throttles, https://developer.intuit.com/app/developer/qbo/docs/learn/limits-and-throttles | checked 6 October 2026 | Rate limits, 1000-row responses |
| Q4 | Basic schema and data formats for the Accounting REST API, https://developer.intuit.com/app/developer/qbo/docs/learn/rest-api-features | checked 6 October 2026 | Create/update calls on the same address, time format |
| Q5 | Query operations and syntax, https://developer.intuit.com/app/developer/qbo/docs/learn/explore-the-quickbooks-online-api/data-queries | checked 6 October 2026 | How rows are queried and paged |
| Q6 | ProfitAndLoss report, https://developer.intuit.com/app/developer/qbo/docs/api/accounting/report-entities/profitandloss | checked 6 October 2026 | Income, gross profit, net income |
| Q7 | BalanceSheet report, https://developer.intuit.com/app/developer/qbo/docs/api/accounting/report-entities/balancesheet | checked 6 October 2026 | Cash in the bank |
| Q8 | ARAgingSummary report, https://developer.intuit.com/app/developer/qbo/docs/api/accounting/report-entities/aragingsummary | checked 6 October 2026 | What customers owe |
| Q9 | APAgingSummary report, https://developer.intuit.com/app/developer/qbo/docs/api/accounting/report-entities/apagingsummary | checked 6 October 2026 | What is owed to suppliers |
| Q10 | Invoice entity, https://developer.intuit.com/app/developer/qbo/docs/api/accounting/all-entities/invoice | checked 6 October 2026 | Invoice dates, totals, multi-currency fields |
| Q11 | QuickBooks Online release notes, https://developer.intuit.com/app/developer/qbo/docs/release-notes/general-release-notes (whole page searched for "scope", "read-only" and "MCP"; entries run to September 2026) | checked 6 October 2026 | Whether anything recent changed access or scopes |
| Q12 | Intuit help article "User roles and access rights in QuickBooks Online", https://quickbooks.intuit.com/community/help-articles-128/user-roles-and-access-rights-in-quickbooks-online-284649 (on Intuit's community help site) | checked 6 October 2026 | Which user roles can only view reports |

Q1 to Q11 are script-built pages, so they were rendered in a browser with no sign-in and the parts used in this note were read. **Q12 could only be read as a short summary, not as the full page, so its quoted phrases are UNVERIFIED word for word.** The "Accounting API release notes" page lists nothing newer than December 2023, so Q11 is the page that carries recent changes. The API Explorer (Intuit's try-it tool) shows "Sign in to explore our APIs"; the reference pages above were readable without signing in.

## 2. How read-only access is made

**There is no read-only permission for the accounting data.** Q1 says "Scopes determine the types of data, and by extention API entities, your app can read and update in QuickBooks Online." The scope for accounting is a single one, `com.intuit.quickbooks.accounting`: "Grants access to the QuickBooks Online Accounting API, which focuses on accounting data." The others on that page are `com.intuit.quickbooks.payment` (the Payments API) and `openid` (the user's name, email, phone and address). The only scopes whose names end in `.read` are narrow ones for the GraphQL API (Intuit's second data service, listed separately on that page), for example `app-foundations.custom-field-definitions.read` and `payroll.compensation.read`; none covers invoices, reports or accounts. The release-notes page (Q11) has no entry about a read-only scope, and none that mentions an assistant connector; a changelog check cannot prove that none exists elsewhere, so that is **UNVERIFIED** outside the pages read.

**What that means in plain words.** The same access that reads a report can also create, change and delete: Q4 shows create and update calls on the same addresses (`POST baseURL/v3/company/realmId/resourceName`). **QuickBooks cannot promise read-only through an app's permission. The promise "only reads" would be the assistant's own rule, not QuickBooks's, and the owner must be told so before he says yes.** Also, a QuickBooks connector shown in one assistant app on 6 October 2026 listed, by tool name, actions that create, update, send and delete (for example creating and deleting invoices and changing employee records). That comes from the tool names the app displayed, not from an Intuit page, and the connector was not used: **UNVERIFIED** for any other connector. A skill must use only reading tools and reports, and refuse every other one.

**Ways to get closer to read-only, none confirmed end to end:**
1. **A user whose role only views reports.** Q12 (summary) names a "Reports Only User" role, available in the Plus plan, that "can view all reports except payroll or contact information", cannot open the audit log, and "can't view the actual transactions"; it adds that "Company administrators can add users and assign roles". The owner (or a company admin) would add a separate user for the assistant with that role and sign the connection in as that user. **UNVERIFIED:** whether an app connected by such a user can call the Accounting API at all, whether it can then still create or change anything, and whether the reports it returns are complete. This must be tried on a sandbox company (Intuit's test company) before any skill relies on it.
2. **Reports only, read through the API.** Section 3 uses only reports and one count query, so a future skill needs nothing else. This limits what the assistant does, not what the access could do.
3. **The owner runs and exports the reports himself** and shares the file. QuickBooks's export options are **UNVERIFIED** (no official page read).

**Who grants access.** The owner signs in through OAuth: Q2 says users are sent to an authorization page where they "give your app permission to access their QuickBooks Online company and its data", and tokens are "tied to your users' now authorized QuickBooks Online company (identified by the realmID)". Which QuickBooks role may press that button is **UNVERIFIED** (not on the pages read). Using the API directly needs an app registered with Intuit (keys held by whoever built the app); the steps and approval requirements for an app that serves only one's own company were not read: **UNVERIFIED**. A connector inside the assistant app hides all of this.

**Token life (Q2, Q11).** An access token lasts 3600 seconds (one hour). A refresh token (the long-lived pass that gets new access tokens) has a hard maximum of five years; Q11 (June 2026) says "the maximum refresh token lifetime is now limited to five years". If the refresh token expires, the owner signs in again. Changing the scopes also needs a new sign-in (Q1).

## 3. Numbers a feed could carry

Reports are requested with `GET /v3/company/<realmID>/reports/<ReportName>` and ask for dates as `start_date` and `end_date` in `YYYY-MM-DD` (Q6). **Report numbers arrive as text**: Intuit's own sample shows `"value": "325.00"`, so the assistant must turn each into a plain number before it goes into `feed_numbers` (the feed refuses text). The report's `Header` names the currency (the sample shows `"Currency": "USD"`) and the basis (`"ReportBasis": "Accrual"`). Always pass `accounting_method` (Q6: "Cash, Accrual") explicitly and write the basis into the feed's name or label. Which basis is the default when it is left out is **UNVERIFIED**.

| Label | Unit | How it is computed (names as Intuit writes them) | The trap |
|---|---|---|---|
| Income | `money` (the report's currency) | `ProfitAndLoss`, the section whose `group` is `Income` (its summary row is labelled "Total Income" in the sample), for an explicit `start_date` and `end_date`. | Text, not a number. A section can be missing when the company has no data (`NoReportData` appears in the header). Whether it counts income before or after sales tax depends on the company's setup: UNVERIFIED. |
| Gross profit | `money` | `ProfitAndLoss`, section `GrossProfit`. | The section exists in Intuit's sample; whether it exists for a company with no cost-of-goods accounts is UNVERIFIED. Send `null` if absent, never 0. |
| Net income | `money` | `ProfitAndLoss`, section `NetIncome`. | A loss is negative. Cash and Accrual give different answers for the same dates. |
| Net margin | `percent` (12.5 means 12.5%) | Net income divided by Income, times 100, worked out by the assistant. | `null` when Income is 0. |
| Cash in bank | `money` | `BalanceSheet` as of the report's end date, section `BankAccounts` (labelled "Total Bank Accounts" in the sample). | It is the balance in the books, not the bank's own figure: bank-feed lag and unreconciled items make them differ. Credit cards are a separate section (`CreditCards`). |
| Customers owe you | `money` | `ARAgingSummary` (the request path on that page is `.../reports/AgedReceivables`), the row whose `group` is `GrandTotal`, column "Total", as of `report_date`. | `aging_method` accepts "Report_Date" or "Current": say which. Foreign-currency invoices: UNVERIFIED whether the report converts them. |
| Overdue share of receivables | `percent` | From the same report: (Total minus the "Current" column) divided by Total, times 100. The sample's columns are "Current", "1 - 30", "31 - 60", "61 - 90", "91 and over", "Total". | Column titles are from the sample; whether every company sees the same ones is UNVERIFIED. `null` when Total is 0. |
| You owe suppliers | `money` | `APAgingSummary` (the request path is `.../reports/AgedPayables`), the grand-total row. | Same traps as the receivables line. |
| Invoices issued | `count` | One query: `select count(*) from Invoice where TxnDate >= '<first day>' and TxnDate <= '<last day>'` (Q5 shows `count(*)` in the select syntax; Q10 marks `TxnDate` "filterable"). | `TxnDate` is "the date entered by the user when this transaction occurred" (Q10), not the day it was saved. Whether voided invoices are counted is UNVERIFIED. A query is sent as a POST with a text body (Q5) even though it only reads, so a rule "never send a POST" would block it. |
| Days to collect | `days` | Customers owe you divided by Income for a full period, times the number of days in that period, worked out by the assistant. | A rough measure; only for a complete period. `null` when Income is 0. |

**Suggested feed shape.** A list of single numbers (about 10, well inside the 40-number limit): Income, Gross profit, Net income, Net margin, Cash in bank, Customers owe you, Overdue share, You owe suppliers, Invoices issued, Days to collect. `as_of` is the end date of the period. Use explicit dates, not Intuit's `date_macro` words such as "This Month" or "Last Fiscal Year": they follow the company's own calendar, and which time zone applies is **UNVERIFIED**.

## 4. Limits and known traps

- **Rate limits (Q3, production):** 500 requests per minute per realm ID, and 10 requests per second per realm ID and app. Batch calls: throttled at 40 per minute per realm ID and app. When throttled you get HTTP status 429 and Intuit says to "wait 60 seconds" before retrying. A request that runs over 120 seconds times out.
- **A monthly allowance exists for some apps (Q3):** apps in the Builder tier of Intuit's partner program have "an included limit of 500,000 CorePlus API calls per workspace per month", after which calls are throttled with 429. Whether a connector inside an assistant app counts against it is UNVERIFIED.
- **Paging (Q3, Q5):** a query returns at most 1000 entities per answer; use `STARTPOSITION` and `MAXRESULTS` to fetch the rest. Only one entity can be queried at a time. Whether the 1000 cap applies to a count query is UNVERIFIED.
- **Time (Q4):** timestamps are `<date>T<time><UTC offset>`, for example a time west of UTC by seven hours. Report dates are plain `YYYY-MM-DD` with no zone shown; which zone a report's day follows (the company's or UTC) is UNVERIFIED.
- **Currency (Q10):** invoices carry a `CurrencyRef` and, when the company uses several currencies, an `ExchangeRate` plus home-currency fields (`HomeTotalAmt`, `HomeBalance`). Reports show the currency in their header. A feed must carry one currency per number, so a multi-currency company needs the home-currency figures: whether every report is already in home currency is UNVERIFIED.
- **Amounts in entities are numbers** (`TotalAmt` is a "BigDecimal", read-only, and Intuit's own invoice sample shows `362.07`), **but amounts in reports are text.** Never copy a report cell into a feed unchanged.
- **Versions:** Q4 says the API supports "minor versions", so changes arrive in steps and an app can stay on one. A skill should name the minor version it was tested with. Whether report layouts change between versions is UNVERIFIED.
- **Test data:** Intuit offers sandbox companies and a separate sandbox address (shown on every report page above). A future skill is tested on invented data only.
- **Credentials:** never ask for a key or token in the chat. With a connector there is nothing to paste; the owner signs in through Intuit's own window.

## 5. UNVERIFIED, in one list

1. Whether a read-only accounting permission exists anywhere outside the pages read.
2. Whether a "Reports Only" user's connection can use the Accounting API, and what it can and cannot change. Also the quoted wording of Q12 (read through a summary).
3. Which QuickBooks role may authorize an app, and the steps for an app that serves one company only.
4. Whether other assistant connectors for QuickBooks are read-only (the one seen offered tools that change data).
5. The default accounting basis of a report, how reports treat multi-currency invoices, and whether income is before or after sales tax.
6. Which time zone Intuit's date macros use.
7. Whether a connector's calls count against the Builder-tier monthly allowance.
8. Export options of the QuickBooks screens.

No skill yet: this note prepares one.
