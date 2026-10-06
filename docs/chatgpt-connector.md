# Use Sorted in ChatGPT

ChatGPT does not install plugins from this repository. It connects to Sorted directly, as an **app** (OpenAI's name for a connection to an outside service through the Model Context Protocol, the standard plug that lets an assistant use another service's tools). This guide sets that up and explains how ChatGPT can use the know-how skills in this repository.

The ChatGPT steps below were checked on **6 October 2026** against OpenAI's help article "Developer mode and MCP apps in ChatGPT" (https://help.openai.com/en/articles/12584461-developer-mode-and-mcp-apps-in-chatgpt). OpenAI changes these screens often. If a screen differs, follow OpenAI's article, not this page.

## What you need

| | |
|---|---|
| ChatGPT plan | **Business** or **Enterprise / Edu** for everything, including sending numbers into Sorted. **Pro** can connect in developer mode with read permissions only: asking questions works, sending numbers (the feed tools) does not. OpenAI's article names no other plan. |
| Where | ChatGPT on the web. OpenAI's article says these apps are not available on mobile. |
| Who | On Business, only a workspace admin or owner can turn on developer mode and create the app. On Enterprise / Edu, an admin can also allow chosen members. |
| A Sorted account | You sign in to Sorted during setup. Only an **owner** of a company in Sorted can create, send to or end a feed. |

## Connect ChatGPT to Sorted

1. **Turn on developer mode** (as of 6 October 2026):
   - Enterprise / Edu: Settings, Apps, Advanced Settings, then the developer mode switch (an admin may first need to allow it under Workspace Settings, Permissions & Roles, Connected Data).
   - Business: an admin or owner turns it on for themselves under Settings, Apps, Advanced settings, Developer mode, or while creating the app under Workspace settings, Apps, Create.
2. **Create the app.** In Settings (or Workspace settings), Apps, Create. Fill in:
   - Name: `Sorted`
   - Server address (the endpoint): `https://sortedos.com/api/mcp`
   - Authentication: **OAuth**. You never paste a key into ChatGPT for this.
3. Press **Scan Tools**. ChatGPT opens Sorted's sign-in: **Sign in with Sorted** using your own Sorted account and approve the access. Then wait for the tool scan to finish, and press **Create**.
4. The app appears under Settings, Apps, Enabled Apps, marked **Dev**. On a Business or Enterprise workspace an admin then publishes it for the workspace (Workspace settings, Apps, Drafts, Publish).

## Check it works

1. Open a new chat, choose **Sorted** from the tools menu (or mention it in your message), and ask: "Give me today's overview from Sorted."
2. A working connection answers with your company's numbers and the time of the snapshot they come from. If ChatGPT says it has no Sorted tools, the app is not selected for that message: select it again. OpenAI's article notes that choosing an app applies to one message, not the whole chat.

## Sending numbers into Sorted (feeds)

Sorted reads Odoo, Shopify, Google Ads and Google Analytics itself, from its Connections page. For numbers it does not read (Meta ads, a point-of-sale system, a delivery app, anything else), your assistant can send them in through four tools of the Sorted app:

| Tool | What it does |
|---|---|
| `list_feeds` | Lists your feeds and when each last received numbers. Never shows a number. |
| `define_feed` | Declares a feed: its name and exactly which numbers it may carry. The first call only returns a preview; nothing is saved until you say yes. |
| `feed_numbers` | Sends one set of numbers into a feed. |
| `end_feed` | Removes a feed and deletes every number it sent. |

- **If these four tools are not in the Sorted app's tool list, feeds are not switched on for your company.** Ask Sorted, through the contact link on the Sorted website.
- ChatGPT keeps a fixed copy of an app's tool list from the moment the app was created or published. **When Sorted switches feeds on for you, the app must pick up the new tools:** on Enterprise / Edu an admin refreshes the app's actions (Workspace settings, Apps, the app's menu, Action control, Refresh); on Business the app is created and published again.
- `define_feed`, `feed_numbers` and `end_feed` change something, so ChatGPT may ask you to confirm before it uses them. That is expected.
- Numbers sent this way are what the assistant read. **Sorted cannot check them**, and your dashboard labels them as sent by your assistant, not read by Sorted.

## Giving ChatGPT the know-how

The folders under `skills/` in this repository teach an assistant how to do a task well: for example `skills/sorted-connect-meta-ads/SKILL.md` explains which Meta ads numbers to read, how to make read-only access, and the exact feed calls. ChatGPT does not load these files by itself. To use one, copy the text of the skill you need into the chat (or into a ChatGPT project's instructions) before you ask. **Not verified:** how closely ChatGPT follows a pasted skill. Check its first feed preview carefully before you say yes.

## Daily sending

OpenAI's article says ChatGPT's agent mode does not use custom apps, so do not rely on agent mode to send numbers every day. Whether ChatGPT's scheduled tasks can use the Sorted app unattended is **not verified**. Until it is, send numbers during a chat, and check with "list my Sorted feeds" that they arrived.

## Never

- Never paste a Sorted key, a password, or any other system's key into a ChatGPT chat. Sorted's ChatGPT app uses sign-in only. If you pasted one by mistake, revoke it and make a new one.
- Never connect a server address other than `https://sortedos.com/api/mcp` for Sorted. OpenAI's article warns that untrusted servers increase the risk of prompt injection (text that tries to give the assistant orders).

## Staying signed in

**Known limit, as checked on 6 October 2026.** OpenAI's article says ChatGPT keeps a connection alive with a renewable sign-in only when the service's sign-in settings advertise it (the `offline_access` scope). Sorted's published sign-in settings (`https://sortedos.com/.well-known/oauth-authorization-server`) allow renewal (`refresh_token`) but do not list `offline_access`. If ChatGPT asks you to sign in to Sorted again after a while, sign in again: your data is unchanged.
