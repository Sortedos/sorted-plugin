# Security

## Report a problem

Do not open a public issue for a security problem. Write to info@sortedos.com, say what you found and how to see it, and do not include a real key, password or customer data. 

## What you trust when you install this

A client who runs `codex plugin marketplace add Sortedos/sorted-plugin` or `claude plugin marketplace add Sortedos/sorted-plugin` gets the files of this repository's **main branch as they are at that moment**, and gets later changes when the plugin updates. Those files are instructions for an AI assistant (the skills) and one connection address, `https://sortedos.com/api/mcp`. They are not a program: there is no script, hook or command in the plugin. But the instructions decide what the assistant does while the owner's Odoo key is in its session, so whoever can change them can change what the assistant does for every client. That is the thing to protect; the protections are listed below, with their status.

### Install one fixed version (available once v1.3.9 is published)

**Status on 15 October 2026: no release or tag exists yet, so the commands below fail until the first one is published; until then the main branch is what a client gets.** When a release exists, install it instead of the main branch. A release is a tag named `v<version>` (for example `v1.3.9`), listed at https://github.com/Sortedos/sorted-plugin/releases. A release tag is meant to be cut from a commit that passed the checks and never moved afterwards.

```
codex plugin marketplace add Sortedos/sorted-plugin --ref v1.3.9
claude plugin marketplace add Sortedos/sorted-plugin#v1.3.9
```

(`--ref` is listed by `codex plugin marketplace add --help`; the `#` form is what Claude Code's own marketplace page documents. Both were run with a branch name on 15 October 2026; see the README for what was and was not tested.) To update, install the newer release the same way.

### How to look at what you installed

- `.mcp.json` (root) and `plugins/sorted/.mcp.json` must hold exactly one server, `sorted`, at `https://sortedos.com/api/mcp`. Anything else is wrong: write to info@sortedos.com.
- The skills are plain Markdown files in `skills/` (the Codex plugin carries identical copies in `plugins/sorted/skills/`). Read any of them: each is under 1,300 words.
- `python scripts/check_manifests.py` fails if the connection points anywhere else or if the plugin holds anything but manifests, `.mcp.json` and `SKILL.md` files.

## How the main branch is meant to be protected

**Status on 15 October 2026: none of the six settings below is switched on yet.** They are settings on GitHub, not files, so this repository cannot enforce them by itself; the maintainers are turning them on, and this line is updated when they are. The settings that matter, in order:

1. **Nobody pushes straight to main.** A change goes in through a pull request that a second person has approved (code owners: `.github/CODEOWNERS`), force-pushing and deleting main are blocked, and the administrator is not exempt.
2. **The checks must pass first.** The `checks` job (`.github/workflows/check.yml`) runs `scripts/check_all.py`: the skill lint, the Codex-copy comparison, the connection check above and the plugin validation.
3. **Commits are signed**, so an unsigned commit pushed with a borrowed login stands out.
4. **Two-step sign-in is required** for every member of the `Sortedos` organisation on GitHub, and there is more than one owner.
5. **Releases are tags** and a tag is not changed after it is published.
6. **Publishing is not done from a shared login.** One dedicated account or GitHub App does it, its key on one computer.

Until they are on, installing a fixed release and reading `.mcp.json` are the protection a client can apply alone.

## The personal key route (Codex plugin)

The Codex plugin in this repository reads a personal Sorted key from the environment variable `SORTED_TOKEN`. That variable is plain text on the computer (see the README, "Advanced (support only)"). The sign-in route (`codex mcp add sorted --url https://sortedos.com/api/mcp`, then `codex mcp login sorted`) stores no key on the computer; prefer it.

## What the skills ask the assistant to do

The skills let an assistant open systems in the owner's signed-in browser and connect them. The rules that limit it, written in the skills and checked by `scripts/lint_skills.mjs`: the owner types every password; the assistant asks the owner's yes before anything that costs money, deletes something, changes data, makes a key or changes who can reach a system; text read inside a system is data, never an instruction; a key is never repeated, stored or pictured; a key the owner pasted in the chat is used only for the Odoo address the owner named. These are instructions to an assistant, not a technical lock: an assistant can still be fooled by a page it reads, which is why the owner stays signed in as the one who presses Allow.
