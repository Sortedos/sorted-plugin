# Sorted for your AI assistant

**Sorted** (https://sortedos.com) puts a company's numbers on one screen. It connects the company's systems (accounting such as Odoo, online stores, ads, analytics), reads them every hour, keeps the history, and shows where two systems disagree about the same number.

This repository lets an AI assistant work with Sorted. It holds:

- **14 skills**: short instruction files that teach an assistant how to do one job well with Sorted, such as getting a company started, a business review, a collections list, finding numbers that disagree, or connecting a system.
- **The Codex plugin** and **the Claude Code plugin**, which install those skills together with the connection to Sorted.
- **A guide for ChatGPT**, which connects to Sorted directly.

## Who this is for

Owners and teams who already use Sorted, or who are trying it, and who work with an AI assistant: Codex, Claude Code, Claude, or ChatGPT. Nothing here needs programming. Each install path takes a few minutes.

Pick the path for the assistant you use. A terminal is the text window where you type commands (PowerShell on Windows, Terminal on a Mac).

| You use | Terminal needed? | Follow |
|---|---|---|
| Codex | Yes | [Install: Codex plugin](#install-codex-plugin) |
| Claude Code | Yes | [Install: Claude Code plugin](#install-claude-code-plugin) |
| Claude on the web or the desktop app | No | [Claude on the web or the desktop app](#claude-on-the-web-or-the-desktop-app) |
| ChatGPT | No | [Install: ChatGPT connector guide](#install-chatgpt-connector-guide) |

## What an assistant can do with Sorted

- **Get a company started from its own software.** The assistant asks one question first, "Which software does your company run on?", spreadsheets included (Excel files on the computer, Google Sheets, Excel in OneDrive or SharePoint), and for every company the owner runs. It then researches how each system can be reached, shows ONE plan (system, route, who checks the numbers), and connects them one by one in its own browser. The owner signs in and types every password; the assistant looks facts up in each system instead of asking for them, and asks for a yes only at steps that cost money, delete something, change data the owner did not ask for, or make a key. The skill is `sorted-onboard`.
- Answer "how is the business doing?" from live numbers, with the time of each snapshot.
- List who owes the company money and draft polite reminders.
- Find where two systems disagree (for example the books and the bank) and list the exact records behind the gap.
- Help the owner connect Odoo, Shopify, Google Ads or Google Analytics, so that Sorted reads them itself.
- **Send in numbers from systems Sorted does not read itself** (Meta ads, a point-of-sale system, a delivery app, anything else), through a **feed**: a named area on the dashboard that the owner approves once. Six skills teach this, one per system: `sorted-connect-odoo`, `sorted-connect-shopify`, `sorted-connect-google-ads`, `sorted-connect-google-analytics`, `sorted-connect-meta-ads` and `sorted-connect-any-system`. Sorted reads Odoo, Shopify, Google Ads and Google Analytics itself, and each of those skills offers that first; the feed is for when Sorted's own connection cannot reach the account, or for a number Sorted does not show.

Two things to know about feeds:

1. **Sorted cannot check numbers that arrive through a feed.** They are what the assistant read. The dashboard labels them "sent by your assistant, not read by Sorted", and the owner is responsible for them.
2. **Feeds work only when Sorted has switched them on for your company.** If the tools `define_feed`, `feed_numbers`, `list_feeds` and `end_feed` are not in your assistant's list of Sorted tools, they are not switched on. Ask Sorted at info@sortedos.com.

The tools, their limits and examples: [docs/feed-tools.md](docs/feed-tools.md).

## The 14 skills

Each skill is one instruction file. The plugins install all of them; in an assistant without the plugin, open the file, copy all of its text and paste it as your first message.

| Skill | What it is for |
|---|---|
| [sorted-onboard](skills/sorted-onboard/SKILL.md) | **Start here.** Ask which software the company runs on, research how to reach each system, show one plan, then connect them one by one and choose the numbers |
| [sorted-about](skills/sorted-about/SKILL.md) | What Sorted is, what it does and what it does not do |
| [sorted-business-review](skills/sorted-business-review/SKILL.md) | A business review from the live numbers: sales, cash, who owes whom, what disagrees |
| [sorted-cash-and-collections](skills/sorted-cash-and-collections/SKILL.md) | Cash, who owes the business money, what is overdue, polite reminder drafts |
| [sorted-fix-conflicts](skills/sorted-fix-conflicts/SKILL.md) | Where two systems report different numbers, and the exact records behind the gap |
| [sorted-organise-dashboard](skills/sorted-organise-dashboard/SKILL.md) | Hide, show, move or add cards and pages on the dashboard |
| [sorted-subscription](skills/sorted-subscription/SKILL.md) | The trial, the plan and the payment link |
| [sorted-connect-systems](skills/sorted-connect-systems/SKILL.md) | Connect Odoo, Shopify, Google Ads or Google Analytics so Sorted reads them itself |
| [sorted-connect-odoo](skills/sorted-connect-odoo/SKILL.md) | Send Odoo numbers through a feed |
| [sorted-connect-shopify](skills/sorted-connect-shopify/SKILL.md) | Send Shopify store numbers through a feed |
| [sorted-connect-google-ads](skills/sorted-connect-google-ads/SKILL.md) | Send Google Ads numbers through a feed |
| [sorted-connect-google-analytics](skills/sorted-connect-google-analytics/SKILL.md) | Send Google Analytics numbers through a feed |
| [sorted-connect-meta-ads](skills/sorted-connect-meta-ads/SKILL.md) | Send Meta ads (Facebook and Instagram) numbers through a feed |
| [sorted-connect-any-system](skills/sorted-connect-any-system/SKILL.md) | Send numbers from any other system through a feed |

## Install: Codex plugin

You need Codex installed and signed in, and a personal Sorted plugin key (it starts with `srt_`). Sorted gives you one: ask at info@sortedos.com. The key belongs to you and your company; keep it to yourself.

1. Open a terminal: on Windows, press the Windows key, type `PowerShell` and press Enter; on a Mac, press Command and Space, type `Terminal` and press Enter. Any folder will do: Codex fetches the plugin from GitHub itself, so you do not download anything.
2. Save your key where Codex can read it, as the environment variable `SORTED_TOKEN` (a named setting your computer keeps for programs).

   On Windows, in PowerShell (the window's title or prompt says PowerShell, not Command Prompt), one line at a time:

   a. Paste this line and press Enter:

      ```powershell
      $key = Read-Host "Paste your Sorted key" -AsSecureString
      ```

   b. Paste your key when it asks, and press Enter. Nothing shows on screen while you paste: that is normal.
   c. Paste this line and press Enter:

      ```powershell
      [Environment]::SetEnvironmentVariable("SORTED_TOKEN", [Net.NetworkCredential]::new("", $key).Password, "User")
      ```

   On a Mac, type `touch ~/.zshrc; open -e ~/.zshrc` to open your terminal's start-up file in TextEdit; on Linux, type `nano ~/.bashrc`. Add a new last line: `export SORTED_TOKEN=` followed by your key, with no spaces. Save and close the file. Typing the key into the file, not into the terminal, keeps it out of the terminal's history.
3. Add the plugin to Codex, straight from GitHub. The first line tells Codex where the plugin lives (`Sortedos/sorted-plugin` is this repository's GitHub name), the second installs it:

   ```
   codex plugin marketplace add Sortedos/sorted-plugin
   codex plugin add sorted@sorted
   ```

4. Close every Codex window, including the Codex desktop app if it is open, so that Codex sees the new key. Open a new terminal, type `codex` and press Enter, then ask: "Do a quick business review using Sorted." A working answer quotes your company's numbers with the time they were read.

(Working from a copy of this repository on your computer instead, for example while changing it? Open a terminal in that folder and use `codex plugin marketplace add .` for the first line.)

Tested on: Windows 11 with Codex 0.155.1. On 10 October 2026 both commands above were run for real against this public repository in a clean Codex home: the marketplace was added from GitHub and `sorted@sorted` 1.2.0 installed and showed as "installed, enabled". The command form `owner/repo` is the one in OpenAI's own page "Build plugins" (https://developers.openai.com/codex/plugins/build). Signing in with a key and the business-review answer were last run on 6 October 2026, with the plugin as it was then (13 skills; the 14th, `sorted-onboard`, was added on 7 October). Not tested: macOS, Linux.

## Install: Claude Code plugin

You need Claude Code installed. No key: Claude Code signs in to Sorted with your own Sorted account.

1. Open a terminal, as in step 1 of the Codex section above. Any folder will do: Claude Code fetches the plugin from GitHub itself.
2. Add the plugin, straight from GitHub:

   ```
   claude plugin marketplace add Sortedos/sorted-plugin
   claude plugin install sorted@sorted
   ```

3. Start Claude Code, type `/mcp`, choose **sorted** and sign in with your Sorted account when the browser opens.
4. Ask: "Do a quick business review using Sorted."

(Working from a copy of this repository on your computer instead? Open a terminal in that folder and use `claude plugin marketplace add ./` for the first line.)

Tested on: Windows 11 with Claude Code 2.1.296. On 10 October 2026 both commands above were run for real against this public repository in a clean Claude Code configuration folder: the marketplace was added from GitHub and `sorted@sorted` installed. The sign-in step (step 3) was not run in that test, and neither was the answer in step 4. Earlier, on 6 October 2026 with Claude Code 2.1.291 and 2.1.292, the plugin from a local copy and the Sorted server entry were installed. Not tested: macOS, Linux.

### Claude on the web or the desktop app

No terminal. There are two routes. The plugin route brings the connection to Sorted and Sorted's skills together; the connector route brings the connection only and works on every plan. Sorted is not in Claude's own plugin directory, so you add it yourself in either case.

**Route A: the plugin (Pro, Max, Team and Enterprise plans).**

1. In Claude, open **Customize** in the left sidebar, then the **Plugins** tab.
2. Press **Add**, then **Add marketplace**, then **Add from a repository**.
3. Enter `Sortedos/sorted-plugin` (this repository's GitHub name).
4. Open the **Discover** tab, choose **Sorted** and press **Add**.
5. Sign in with your Sorted account when Claude asks (if it does not, press **Connect** next to Sorted under **Customize**, then **Connectors**), choose your company and press **Allow**.

On a Team or Enterprise plan, a Claude owner can limit which marketplaces are allowed; if **Add marketplace** is missing or refuses, ask your owner or use Route B. A plugin added this way is saved to your Claude account and also reaches Claude Code when you sign in there with the same account. Anthropic's page: https://support.claude.com/en/articles/13837440

**Route B: the connector only (every plan, Free included).**

1. In Claude, open **Customize**, then **Connectors**, click **+ Add**, then **Add custom connector**. Name it Sorted, enter the address `https://sortedos.com/api/mcp`, press **Continue**, keep the sign-in choices Claude suggests and press **Add**. On a Team or Enterprise plan, an owner of the Claude organisation adds it first under **Organization settings**, **Connectors**; members then find it under **Customize**, **Connectors** and click **Connect**. Anthropic's page shows each screen: https://support.claude.com/en/articles/11175166-get-started-with-custom-connectors-using-remote-mcp
2. Sign in with your Sorted account when Claude asks, choose your company and press **Allow**.
3. To use a skill, open its file from [the list of skills](#the-14-skills), copy all of its text and paste it as your first message.

Tested on: nothing yet in a real Claude account. The menu names of both routes were checked against Anthropic's two pages on 10 October 2026 ("Use plugins in Claude" and "Get started with custom connectors using remote MCP"), and `claude plugin marketplace add Sortedos/sorted-plugin` worked from a terminal (see the Claude Code section). Not tested: adding the marketplace in Claude on the web or the desktop app, or connecting it to Sorted. Anthropic changes these menus often: if a screen differs, follow Anthropic's page.

## Install: ChatGPT connector guide

ChatGPT connects to Sorted directly, as an app, with sign-in and no key. Which ChatGPT plans can do this, the steps, and how to give ChatGPT the skills: [docs/chatgpt-connector.md](docs/chatgpt-connector.md).

Tested on: the steps were checked against OpenAI's own pages on 7 October 2026 (OpenAI changed these screens on 1 October 2026; the guide gives the new way first and the older screens as a fallback), and Sorted's server answered with its four feed tools in a local test. Not tested: a real ChatGPT workspace connecting to Sorted.

## Safety, in plain words

- Sorted only reads the company's systems. The skills tell the assistant to use read-only access and never to change anything in the owner's systems.
- The owner types every password. An API key is made only with the owner's explicit approval, on the owner's own user (no new paid user), and goes straight from the system's own screen into Sorted's own form, never into the chat. While a key is on screen the assistant reads only the key box's title and field names, never the page or box text, takes no picture, never prints the key and never uses the clipboard (the computer's clipboard history would keep a copy); it moves the key in one action that returns nothing but a length or "done". The skills tell the assistant never to ask for, repeat or store a secret in the chat, and never to describe a screenshot of one. The key may still pass through the assistant's own session while it is carried between the two pages, which is why each key needs the owner's yes. Odoo keys expire, so the assistant records the date and renews before it.
- The assistant asks for the owner's yes only at important steps: anything that costs money, deletes something, changes data the owner did not ask for, or makes a key. Once the owner has signed it in, it presses on, system after system.
- A feed is created only after the owner has seen its preview and said yes, and `end_feed` deletes everything it sent.
- Names and labels that come from other systems are treated as data, never as instructions.

## For contributors

How to propose a new system skill or report a problem: [CONTRIBUTING.md](CONTRIBUTING.md). What changed in each version: [CHANGELOG.md](CHANGELOG.md). This page in Arabic: [docs/ar/README.md](docs/ar/README.md).

The checks this repository runs on itself (on macOS or Linux, type `python3` where it says `python`). One command runs them all (`python scripts/check_all.py`); one by one:

```
python scripts/scan_public.py --selftest                     # the leak scan can catch a planted secret
python scripts/scan_public.py --denylist <your private list> # leak scan of every file and every change in the git history
node scripts/lint_skills.mjs                                 # skill lint: rules, limits, word cap, no secrets
python scripts/sync_codex_plugin.py --check                  # the Codex copy of the skills has not drifted
```

`skills/` is the one place to edit skills; `python scripts/sync_codex_plugin.py` copies them into the Codex plugin.

## License

MIT: anyone may use, change and share this repository, keeping the copyright line. See [LICENSE](LICENSE).
