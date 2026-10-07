# Contributing

Thank you for helping. This repository holds instructions for AI assistants ("skills"), not application code, so most contributions are a new skill or a better sentence in an existing one.

## Proposing a skill for a new system

A skill teaches an assistant to read numbers from one outside system with read-only access and send them to Sorted through a feed. The entry point for a new owner is `skills/sorted-onboard/SKILL.md`, which researches every system the owner lists and points to the right skill; add your system to its routes only if it needs a route that is not already there. Copy the shape of an existing one, for example `skills/sorted-connect-any-system/SKILL.md`, and keep its parts in this order:

1. **What to ask the owner**: which numbers, which period, how often. Never ask for a fact the system can show (plan, version, address, list of accounts or companies): the assistant opens the system, the owner signs in, and the assistant reads it.
2. **Read-only access first**: the system's own connector with read-only rights, or a report the owner exports themselves.
3. **Make a read-only credential**: the exact screens, in the system's own words, for a read-only role or read-only scopes. Once the owner has signed in, the assistant does the clicks and the owner types every password; access details go into the assistant app's own settings, never in a chat. The one exception, an API key made on the owner's own user with the owner's explicit approval and carried straight into Sorted's own form, is written once in `skills/sorted-connect-systems/SKILL.md`; the lint (`scripts/lint_skills.mjs`, rules 3b and 3c) allows only that wording and never frees reading page text, the clipboard or a picture while a key shows.
4. **Numbers to read**: each with a plain label and one unit (`money` with a currency, `count`, `percent`, `ratio`, `days`, `number`), plus the traps of that system (numbers arriving as text, amounts in millionths, rates as fractions).
5. **The feed**: a worked `define_feed` call and a worked `feed_numbers` call, with fake data.
6. **Never**: never ask for a secret in a chat, never write to the owner's system, only send numbers actually read.

The limits every feed must respect are in [docs/feed-tools.md](docs/feed-tools.md).

## Before you open a pull request

- Run `python scripts/check_all.py` (on macOS or Linux, `python3`). Every check must pass, except the leak scan, which reports itself skipped: it needs the maintainers' private list of names, and the maintainers run it before merging.
- Save your skill's two example calls as JSON files and run `python scripts/check_feed_call.py --define <file> --feed <file>`. It must print `ACCEPT`. (It checks the published limits; the Sorted service also refuses labels that read like instructions to an assistant.)
- Run `python scripts/sync_codex_plugin.py` after editing anything under `skills/`, so the Codex plugin carries the same text.
- Keep each `SKILL.md` at 1,300 words or fewer.
- Use only fake examples: a company such as "Acme Trading", addresses ending in `example.com`.

## Never in a pull request

- Real names of customers, people or companies, real account numbers, hostnames or database names.
- Keys, tokens or passwords, even expired ones.
- Paths from your own computer.
- Prices: the product states its own price through the `get_subscription` tool.
- An instruction that asks an assistant to show or write out its reasoning.

## Security

If you find a security problem, do not open a public issue. Write to info@sortedos.com instead.
