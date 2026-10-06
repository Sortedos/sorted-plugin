# Use Sorted in ChatGPT

ChatGPT does not install plugins from this repository. It connects to Sorted directly, as an **app** (OpenAI's name for a connection to an outside service through the Model Context Protocol, the standard plug that lets an assistant use another service's tools). This guide sets that up and explains how ChatGPT can use the know-how skills in this repository.

The ChatGPT steps below were checked on **7 October 2026** against OpenAI's own pages, listed under "Sources" at the end. OpenAI changes these screens often, and it is changing them now: on 1 October 2026 OpenAI staff said that the separate **developer mode** switch (a switch that let you add an app that is not in OpenAI's own list) is gone, and that custom servers are now added from ChatGPT's Plugins page. OpenAI's help article "Developer mode and MCP apps in ChatGPT" still describes the older screens, although it said "Updated: 21 hours ago" when it was read. So this page gives the new way first and the older screens as a fallback. **Not tested in a real ChatGPT workspace:** every screen name below comes from those OpenAI pages, and what could not be confirmed is marked **not verified**. If a screen differs from this page, follow OpenAI's current page, not this one.

## What you need

| | |
|---|---|
| ChatGPT plan | **Business** or **Enterprise / Edu**: everything, including sending numbers into Sorted. **Pro**: OpenAI's article says Pro users can connect a custom server "with read/fetch permissions" only, so asking questions can work but sending numbers (the feed tools) does not. **Free, Plus or any other plan**: OpenAI's article lists no support for these plans, so this guide does not promise it works for you. A staff post of 1 October 2026 says "all eligible users" can connect custom servers but not which plans are eligible (**not verified**). If the **Add custom MCP server** choice in the steps below is missing on your account, stop here. |
| Where | ChatGPT on the web. OpenAI's article says these apps are not available on mobile ("No - web only"). |
| Who in ChatGPT | A **ChatGPT workspace owner or admin**: the people who run your company's ChatGPT workspace (OpenAI's article says Workspace settings, then Members, lists them). On Business only they can add the app. On Enterprise / Edu an admin can also give chosen members the permission **Create custom MCP servers** (OpenAI staff say it was renamed from "Developer mode" on 1 October 2026). Not an admin? See [If you are not an admin](#if-you-are-not-an-admin). |
| A Sorted account | You sign in to Sorted during setup. Only a **Sorted company owner** (the owner role of your company inside Sorted, which is not the same thing as a ChatGPT workspace owner) can create, send to or end a feed; any member can list feeds. Where Sorted shows your role is **not verified**: if you are unsure, ask the person who set up your company in Sorted. |

## Connect ChatGPT to Sorted

Do this as the ChatGPT workspace owner or admin, or as a member who has been given the **Create custom MCP servers** permission. There is no separate developer mode switch to turn on first (OpenAI staff, 1 October 2026: "We have removed the need to enter an explicit 'developer mode' to connect custom MCP servers in ChatGPT").

1. In ChatGPT on the web, open **Plugins**: in the sidebar, or go to chatgpt.com/plugins.
2. Select the plus button, then **Add custom MCP server**. OpenAI's own pages name this choice differently: OpenAI's developer page says **Add custom MCP server**, and a staff post says **Add**, then **Create MCP App**, to be renamed **Create custom MCP server**. Pick whichever of these your screen shows.
3. Fill in:
   - Name: `Sorted`, and a short description of your own (the developer page asks for a name and a description).
   - Connection: a public address. Server address: `https://sortedos.com/api/mcp` (the whole address, including the `/mcp` part at the end).
   - Authentication: **OAuth**, the sign-in method where you approve access in Sorted's own window and share no password. You never paste a key into ChatGPT for this. The exact name of this choice on the new screen is **not verified**.
4. Read the risk warning. OpenAI says custom servers are not verified by OpenAI and should be added only if you know and trust the service; this address is Sorted's own. Select **I understand and want to continue**, then select **Create as a plugin**.
5. At some point in these steps ChatGPT opens Sorted's sign-in (OpenAI's new page does not say exactly when: **not verified**): **Sign in with Sorted** using your own Sorted account and approve the access. Then review the tools ChatGPT found on the server.
6. If ChatGPT offers to install the resulting plugin, install it, then start a new conversation.

### If your screens look older

If you do not see **Plugins** with an **Add** choice, but your account shows the screens that OpenAI's help article still describes (as read on 7 October 2026), use these. Which accounts still see them is **not verified**.

- **Business:** an owner or admin opens Workspace settings, Apps, **Create**, and turns on developer mode there, for themselves (each admin or owner has to do it for themselves).
- **Enterprise / Edu:** Settings, Apps, Advanced Settings, then the developer mode switch. An admin may first need to allow it under Workspace settings, Permissions & roles, Connected data (where OpenAI staff say the setting is now called **Create custom MCP servers**; the article calls it "Developer mode / Create custom MCP connectors"). Then Settings, Apps, **Create**, or Workspace settings, Apps, **Create**.
- Fill in the same name, server address and **OAuth**, press **Scan Tools**, sign in with Sorted, wait for the scan to finish, and press **Create**.
- The app appears as a draft under Workspace settings, Apps, Drafts, and for you under Settings, Apps, Enabled Apps, marked **Dev**. An admin or owner then publishes it for the workspace: Workspace settings, Apps, Drafts, **Publish**.
- Admins can also reach the older Apps page from the Admin console: select the ChatGPT workspace, open **Plugins**, then **Manage Legacy Apps**.

Whether an admin must also publish a connection made the new way from the Plugins page, so that colleagues can use it, is **not verified**: OpenAI's new page does not say.

## If you are not an admin

- **Business:** OpenAI's article says only admins and owners can enable developer mode and deploy an app. Send this page to your ChatGPT workspace admin and ask them to add Sorted with the steps above. Workspace settings, Members, shows who the admins are.
- **Enterprise / Edu:** an admin can give you the permission **Create custom MCP servers** (it was called Developer mode) under Workspace settings, Permissions & roles, Connected data. Ask for that, or ask them to add the app.
- **If an admin or owner is refused:** several people on OpenAI's community forum (3 and 5 October 2026), one of them a workspace owner, report the message "You need workspace admin permission to create a draft app", and OpenAI had not answered when it was read. This is a user report, not an OpenAI statement: the cause is **not verified**. Contact OpenAI support.

## Check it works

1. Open a new chat, choose **Sorted** from the tools menu (or type @ and pick it, as OpenAI's developer page describes), and ask: "Give me today's overview from Sorted."
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
- ChatGPT keeps a fixed copy of an app's tool list from the moment the app was created or published (OpenAI's article calls it a "frozen" snapshot). **When Sorted switches feeds on for you, the app must pick up the new tools.** Try these in order, then start a new conversation:
  1. **Refresh first.** In ChatGPT Plugins, open the Sorted connection and select **Refresh**. OpenAI's developer page says this is how a custom server connected directly in ChatGPT picks up changes.
  2. **Enterprise / Edu:** an admin refreshes the app's actions (Workspace settings, Apps, the three-dot menu next to the app, **Action control**, **Refresh**) and then switches the new actions on, because OpenAI says new actions are off by default.
  3. **Business:** OpenAI's help article says a published app cannot be updated and has to be created and published again. Do that only if **Refresh** is not offered or does not bring the new tools. Whether **Refresh** works on a published Business app is **not verified**.
- `define_feed`, `feed_numbers` and `end_feed` change something, so ChatGPT may ask you to confirm before it uses them. That is expected.
- Numbers sent this way are what the assistant read. **Sorted cannot check them**, and your dashboard labels them as sent by your assistant, not read by Sorted.

## Giving ChatGPT the know-how

A **skill** is a short instruction file that teaches an assistant how to do one job well. This repository has 13 of them. For example, [sorted-connect-meta-ads](../skills/sorted-connect-meta-ads/SKILL.md) explains which Meta ads numbers to read, how to make read-only access, and the exact feed calls. The list of all 13, each with a plain description and a link to its file, is the table in [the README](../README.md#the-13-skills). To send numbers into Sorted, pick the skill named for your system. ChatGPT does not load these files by itself. There are two ways to give it one:

**A. Upload it, where Skills is offered.** OpenAI's article "Skills in ChatGPT" says skills are "available to eligible ChatGPT Business, Enterprise, Healthcare, and Edu users, subject to workspace settings and product availability". If it is offered to you: in the sidebar select **Plugins**, open the **Skills** tab, select **Create**, then **Upload from your computer**. To get the skill's file, download this repository's files first (on its GitHub page, the green **Code** button, then **Download ZIP**, then unzip). Whether the upload takes one SKILL.md file, a whole folder or a ZIP is **not verified**: follow what the upload window asks for. ChatGPT scans an uploaded skill before you can use it. A skill marked **Needs Review** asks you to read more first, and a skill marked **Blocked** cannot be used. On Enterprise / Edu an admin has to allow uploads first (the permission is called **Enable skill uploading**, under Permissions & roles). OpenAI's article lists no Skills support for other plans.

**B. Paste it, on any plan.** Open the skill's link in the README table, copy all of the file's text (use the copy button above the file's text, or open the file's **Raw** view, select all and copy), and paste it as your first message in a new chat before you ask.

**Not verified:** how closely ChatGPT follows an uploaded or a pasted skill. OpenAI's developer page says "The description determines when the model considers the skill", and every skill here starts with a name and a description. Check the first feed preview carefully before you say yes.

## Daily sending

OpenAI's article says ChatGPT's agent mode does not use custom apps, and that deep research can use them only for reading, never for writing, so do not rely on either to send numbers every day. Whether ChatGPT's scheduled tasks can use the Sorted app unattended is **not verified**. Until it is, send numbers during a chat, and check with "list my Sorted feeds" that they arrived.

## Never

- Never paste a Sorted key, a password, or any other system's key into a ChatGPT chat. Sorted's ChatGPT app uses sign-in only.
- **If you pasted one by mistake, act at once, before anything else:**
  1. A **Sorted key** (it starts with `srt_`): contact Sorted straight away through the contact link on the Sorted website, and ask for that key to be cancelled and a new one issued.
  2. A **key or password for any other system** (Odoo, Shopify, Meta, Google and so on): open that system's own settings page for keys or access and delete or regenerate the key now, or change the password.
  3. Then delete the chat in ChatGPT. Deleting the chat does not make the old key safe; replacing the key does.
- Never connect a server address other than `https://sortedos.com/api/mcp` for Sorted. OpenAI's article warns that untrusted servers increase the risk of prompt injection (text that tries to give the assistant orders).

## Staying signed in

**Known limit, as checked on 6 October 2026.** OpenAI's article says ChatGPT keeps a connection alive with a renewable sign-in only when the service's sign-in settings advertise it (the `offline_access` scope). Sorted's published sign-in settings (`https://sortedos.com/.well-known/oauth-authorization-server`) allow renewal (`refresh_token`) but do not list `offline_access`. If ChatGPT asks you to sign in to Sorted again after a while, sign in again: your data is unchanged.

## Not verified, as of 7 October 2026

- Whether ChatGPT's screens match this page: it was not tested in a real ChatGPT workspace, and OpenAI's help article and its staff disagree on the developer mode screens.
- Whether Free or Plus accounts can add a custom server, and where a Pro account is limited to reading (OpenAI's article does not say, and still says Pro users "must continue enabling developer mode").
- What the OAuth choice is called on the new screen, and when Sorted's sign-in window opens.
- Whether an admin must publish a connection made from the Plugins page for colleagues, and whether **Refresh** works on a published Business app.
- Whether the Skills upload takes one SKILL.md file, a folder or a ZIP, and how closely ChatGPT follows a skill.
- Whether ChatGPT's scheduled tasks can use the Sorted app unattended.
- Where Sorted shows your role in your company.

## Sources

All read on 7 October 2026.

- OpenAI staff posts on the OpenAI Developer Community, 1 October 2026: https://community.openai.com/t/developer-mode-missing-from-security-login-on-chatgpt-pro/1402157 and https://community.openai.com/t/developer-mode-missing-and-mcp-app-creation-unavailable-across-multiple-chatgpt-accounts/1402294
- OpenAI developer page "Connect and test your plugin": https://developers.openai.com/plugins/deploy/connect-chatgpt (the older address https://developers.openai.com/apps-sdk/deploy/connect-chatgpt leads to the same page), and "Build skills": https://developers.openai.com/plugins/build/skills
- OpenAI help article "Developer mode and MCP apps in ChatGPT": https://help.openai.com/en/articles/12584461-developer-mode-and-mcp-apps-in-chatgpt
- OpenAI help article "Skills in ChatGPT": https://help.openai.com/en/articles/20001066-skills-in-chatgpt
- OpenAI help article "Admin controls, security, and compliance for plugins and apps": https://help.openai.com/en/articles/11509118-admin-controls-security-and-compliance-for-plugins-and-apps
