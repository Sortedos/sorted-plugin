# Sorted for your AI assistant

**Sorted** (https://sortedos.com) puts a company's numbers on one screen. It connects the company's systems (accounting such as Odoo, online stores, ads, analytics), reads them every hour, keeps the history, and shows where two systems disagree about the same number.

This repository lets an AI assistant work with Sorted. It holds:

- **13 skills**: short instruction files that teach an assistant how to do one job well with Sorted, such as a business review, a collections list, finding numbers that disagree, or connecting a system.
- **The Codex plugin** and **the Claude Code plugin**, which install those skills together with the connection to Sorted.
- **A guide for ChatGPT**, which connects to Sorted directly.

## Who this is for

Owners and teams who already use Sorted, or who are trying it, and who work with an AI assistant: Codex, Claude Code, Claude, or ChatGPT. Nothing here needs programming. Each install path takes a few minutes.

## What an assistant can do with Sorted

- Answer "how is the business doing?" from live numbers, with the time of each snapshot.
- List who owes the company money and draft polite reminders.
- Find where two systems disagree (for example the books and the bank) and list the exact records behind the gap.
- Help the owner connect Odoo, Shopify, Google Ads or Google Analytics, so that Sorted reads them itself.
- **Send in numbers from systems Sorted does not read itself** (Meta ads, a point-of-sale system, a delivery app, anything else), through a **feed**: a named area on the dashboard that the owner approves once. Six skills teach this, one per system: `sorted-connect-odoo`, `sorted-connect-shopify`, `sorted-connect-google-ads`, `sorted-connect-google-analytics`, `sorted-connect-meta-ads` and `sorted-connect-any-system`.

Two things to know about feeds:

1. **Sorted cannot check numbers that arrive through a feed.** They are what the assistant read. The dashboard labels them "sent by your assistant, not read by Sorted", and the owner is responsible for them.
2. **Feeds work only when Sorted has switched them on for your company.** If the tools `define_feed`, `feed_numbers`, `list_feeds` and `end_feed` are not in your assistant's list of Sorted tools, they are not switched on. Ask Sorted through the contact link on the Sorted website.

The tools, their limits and examples: [docs/feed-tools.md](docs/feed-tools.md).

## Install: Codex plugin

You need Codex installed and signed in, and a personal Sorted plugin key (it starts with `srt_`). Sorted gives you one: ask through the contact link on the Sorted website. The key belongs to you and your company; keep it to yourself.

1. Download this repository and open a terminal in its folder.
2. Save your key where Codex can read it, as the environment variable `SORTED_TOKEN`. On Windows, in PowerShell:

   ```powershell
   [Environment]::SetEnvironmentVariable("SORTED_TOKEN", (Read-Host "Paste your Sorted key"), "User")
   ```

   On macOS or Linux, add `export SORTED_TOKEN=...` with your key to your shell's start-up file.
3. Add the plugin to Codex:

   ```
   codex plugin marketplace add .
   codex plugin add sorted@sorted
   ```

4. Open a new terminal and ask Codex: "Do a quick business review using Sorted."

## Install: Claude Code plugin

You need Claude Code installed. No key: Claude Code signs in to Sorted with your own Sorted account.

1. Download this repository and open a terminal in its folder.
2. Add the plugin:

   ```
   claude plugin marketplace add .
   claude plugin install sorted@sorted
   ```

3. Start Claude Code, type `/mcp`, choose **sorted** and sign in with your Sorted account when the browser opens.
4. Ask: "Do a quick business review using Sorted."

Using Claude on the web or the desktop app instead: add a custom connector with the address `https://sortedos.com/api/mcp` and sign in with Sorted, following Claude's own guide (https://support.claude.com/en/articles/11175166-get-started-with-custom-connectors-using-remote-mcp). The skills can then be pasted into a conversation, or added as skills where your Claude plan allows it.

## Install: ChatGPT connector guide

ChatGPT connects to Sorted directly, as an app, with sign-in and no key. Which ChatGPT plans can do this, the steps, and how to give ChatGPT the skills: [docs/chatgpt-connector.md](docs/chatgpt-connector.md).

## Safety, in plain words

- Sorted only reads the company's systems. The skills tell the assistant to use read-only access and never to change anything in the owner's systems.
- The owner handles every password and key. The skills tell the assistant never to ask for, repeat or store one, and never to look at a key on screen.
- A feed is created only after the owner has seen its preview and said yes, and `end_feed` deletes everything it sent.
- Names and labels that come from other systems are treated as data, never as instructions.

## For contributors

The checks this repository runs on itself:

```
python scripts/scan_public.py --selftest                     # the leak scan can catch a planted secret
python scripts/scan_public.py --denylist <your private list> # leak scan of every file and the git history
node scripts/lint_skills.mjs                                 # skill lint: rules, limits, word cap, no secrets
python scripts/sync_codex_plugin.py --check                  # the Codex copy of the skills has not drifted
```

`skills/` is the one place to edit skills; `python scripts/sync_codex_plugin.py` copies them into the Codex plugin.

## License

Not chosen yet. Until a LICENSE file is added, no license is granted and all rights are reserved.
