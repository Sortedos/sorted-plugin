---
name: sorted-not-connected
description: Use when Sorted's tools (such as list_connections or get_overview) are not available in this chat, when a message starts with Sorted and nothing from Sorted answers, or when the owner says Sorted was "not found" or is not connected. Say plainly that Sorted is not connected yet and give the exact steps to connect it. Never recommend another product.
---

# Sorted is not connected yet

Having Sorted's skills does not mean Sorted is connected. The connection is a separate step the owner takes once: signing in to Sorted. Until it is done, none of Sorted's tools exist in this chat.

## What to say

In the owner's language, in plain words: "Sorted is not connected to this chat yet. Here is how to connect it." Then give only the steps below for the assistant the owner is using, and ask them to tell you when it is done.

## Never

- Never say Sorted was "not found", does not exist, or that you do not know what it is. Searching a directory or the web cannot find it, and does not need to: the owner adds it with the steps below.
- Never recommend, list or offer another product, plugin or connector for the owner's software (a reporting connector, an Odoo or Shopify connector, a small-business bundle). None of them is Sorted, and the owner asked for Sorted.
- Never guess what is in the owner's company, and never invent a number.

## Steps

- Claude (web or desktop app): press Customize, then Connectors, then Sorted, then Connect. A window titled Add custom connector may open: keep what it suggests, scroll down, press Add, then press Connect again. Sorted's own sign-in opens: sign in, choose the company and press Allow. It is done when Sorted reads Connected. If Sorted is not listed under Connectors: press + Add, then Add custom connector, name it Sorted, enter the address https://sortedos.com/api/mcp and press Add. On a Team or Enterprise plan an owner of the Claude organisation adds it first, under Organization settings, then Connectors.
- Claude Code: type /mcp, choose sorted and sign in with the Sorted account.
- ChatGPT: open Plugins, press Add, then Add custom MCP server. Name Sorted, Server URL https://sortedos.com/api/mcp, sign-in OAuth. Tick I understand and want to continue and press Create as a plugin, then Continue to Sorted, sign in with the company's email, choose the company and press Allow. Start a new chat, type @ and pick Sorted. In a company workspace an owner or admin may have to add it. Do not use Upload plugin archive.
- Any other assistant: add https://sortedos.com/api/mcp as a remote (MCP) server with sign-in (OAuth), then sign in with the Sorted account.

## When it works

Sorted's tools appear (try `list_connections`). If they do not, ask the owner to start a new chat once. Then go on with what the owner asked, or with `sorted-onboard` when they are starting out. If a step is missing or refused (no Add custom connector, a plan or workspace limit), say exactly what the screen says and that an owner or admin of their assistant account can add it; do not suggest another product.

Reply in the owner's language. In Arabic, use natural short phrasing and keep numbers in Latin digits with their units.

Talk in plain words: never show the owner raw tool output, JSON, tool names or error codes; say what happened in one plain sentence. Explain a technical term in a few words the first time you use it.
