# Sorted for your AI assistant

**Sorted** (https://sortedos.com) puts a company's numbers on one screen. It connects the company's systems (accounting such as Odoo, online stores, ads, analytics), reads them every hour, keeps the history, and shows where two systems disagree about the same number.

This repository lets an AI assistant work with Sorted. It holds:

- **13 skills**: short instruction files that teach an assistant how to do one job well with Sorted, such as a business review, a collections list, finding numbers that disagree, or connecting a system.
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

- Answer "how is the business doing?" from live numbers, with the time of each snapshot.
- List who owes the company money and draft polite reminders.
- Find where two systems disagree (for example the books and the bank) and list the exact records behind the gap.
- Help the owner connect Odoo, Shopify, Google Ads or Google Analytics, so that Sorted reads them itself.
- **Send in numbers from systems Sorted does not read itself** (Meta ads, a point-of-sale system, a delivery app, anything else), through a **feed**: a named area on the dashboard that the owner approves once. Six skills teach this, one per system: `sorted-connect-odoo`, `sorted-connect-shopify`, `sorted-connect-google-ads`, `sorted-connect-google-analytics`, `sorted-connect-meta-ads` and `sorted-connect-any-system`. Sorted reads Odoo, Shopify, Google Ads and Google Analytics itself, and each of those skills offers that first; the feed is for when Sorted's own connection cannot reach the account, or for a number Sorted does not show.

Two things to know about feeds:

1. **Sorted cannot check numbers that arrive through a feed.** They are what the assistant read. The dashboard labels them "sent by your assistant, not read by Sorted", and the owner is responsible for them.
2. **Feeds work only when Sorted has switched them on for your company.** If the tools `define_feed`, `feed_numbers`, `list_feeds` and `end_feed` are not in your assistant's list of Sorted tools, they are not switched on. Ask Sorted at info@sortedos.com.

The tools, their limits and examples: [docs/feed-tools.md](docs/feed-tools.md).

## The 13 skills

Each skill is one instruction file. The plugins install all of them; in an assistant without the plugin, open the file, copy all of its text and paste it as your first message.

| Skill | What it is for |
|---|---|
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

1. Get this repository's files onto your computer: on its GitHub page, click the green **Code** button, then **Download ZIP**, and unzip the file. Then open a terminal in the unzipped folder: on Windows, right-click inside the folder in File Explorer and choose **Open in Terminal**; on a Mac, right-click the folder and choose **Services**, then **New Terminal at Folder**.
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
3. Add the plugin to Codex:

   ```
   codex plugin marketplace add .
   codex plugin add sorted@sorted
   ```

4. Close every Codex window, including the Codex desktop app if it is open, so that Codex sees the new key. Open a new terminal, type `codex` and press Enter, then ask: "Do a quick business review using Sorted." A working answer quotes your company's numbers with the time they were read.

Tested on: Windows 11 with Codex 0.155.1, 6 October 2026 (the plugin and its 13 skills installed). Not tested: macOS, Linux.

## Install: Claude Code plugin

You need Claude Code installed. No key: Claude Code signs in to Sorted with your own Sorted account.

1. Get this repository's files and open a terminal in their folder, as in step 1 of the Codex section above.
2. Add the plugin:

   ```
   claude plugin marketplace add ./
   claude plugin install sorted@sorted
   ```

3. Start Claude Code, type `/mcp`, choose **sorted** and sign in with your Sorted account when the browser opens.
4. Ask: "Do a quick business review using Sorted."

Tested on: Windows 11 with Claude Code 2.1.291 and 2.1.292, 6 October 2026 (the plugin, its 13 skills and the Sorted server entry installed; the sign-in step was not run in that test). Not tested: macOS, Linux.

### Claude on the web or the desktop app

No terminal and no key: Claude connects to Sorted directly, with your Sorted account.

1. In Claude, open **Customize**, then **Connectors**, click **+ Add**, then **Add custom connector**. Name it Sorted and enter the address `https://sortedos.com/api/mcp`. On a Team or Enterprise plan, an owner of the Claude organisation adds it first under **Organization settings**, **Connectors**; members then find it under **Customize**, **Connectors** and click **Connect**. Claude's own guide shows each screen: https://support.claude.com/en/articles/11175166-get-started-with-custom-connectors-using-remote-mcp
2. Sign in with your Sorted account when Claude asks.
3. To use a skill, open its file from [the list of skills](#the-13-skills), copy all of its text and paste it as your first message, or add it as a skill where your Claude plan allows it.

Tested on: nothing yet; only the menu names were checked, against Claude's guide on 7 October 2026. Not tested: connecting Claude on the web or the desktop app to Sorted.

## Install: ChatGPT connector guide

ChatGPT connects to Sorted directly, as an app, with sign-in and no key. Which ChatGPT plans can do this, the steps, and how to give ChatGPT the skills: [docs/chatgpt-connector.md](docs/chatgpt-connector.md).

Tested on: the steps were checked against OpenAI's own pages on 7 October 2026 (OpenAI changed these screens on 1 October 2026; the guide gives the new way first and the older screens as a fallback), and Sorted's server answered with its four feed tools in a local test. Not tested: a real ChatGPT workspace connecting to Sorted.

## Safety, in plain words

- Sorted only reads the company's systems. The skills tell the assistant to use read-only access and never to change anything in the owner's systems.
- The owner handles every password and key. The skills tell the assistant never to ask for, repeat or store one, and never to look at a key on screen.
- A feed is created only after the owner has seen its preview and said yes, and `end_feed` deletes everything it sent.
- Names and labels that come from other systems are treated as data, never as instructions.

## For contributors

How to propose a new system skill or report a problem: [CONTRIBUTING.md](CONTRIBUTING.md). What changed in each version: [CHANGELOG.md](CHANGELOG.md). Notes that prepare future system skills: [docs/research/](docs/research/). This page in Arabic: [docs/ar/README.md](docs/ar/README.md).

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
