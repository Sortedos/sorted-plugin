# Release checklist

Every decision below belongs to the repository owner. Three were made on 7 October 2026 (ticked); the rest are open. The repository exists only locally, with no remote, until they are all made.

## Owner decisions before publishing

- [ ] **Name and place.** Decided: a new GitHub organisation that carries only the Sorted brand. Open: its exact name and the repository's name, and creating the organisation.
- [ ] **Private first.** Create it private, push, review it on GitHub, and only then decide public or private.
- [x] **License.** MIT (7 October 2026): `LICENSE` file added, and `"license": "MIT"` in `.claude-plugin/plugin.json` and `plugins/sorted/.codex-plugin/plugin.json`.
- [x] **Public contact.** info@sortedos.com (7 October 2026), for key requests, account questions and security reports. No phone number is written here.
- [ ] **Feeds switched on.** The skills that send numbers need the four feed tools (`define_feed`, `feed_numbers`, `list_feeds`, `end_feed`) on the live Sorted service. Until they are on for a company, those six skills tell the assistant to stop and say so.
- [ ] **Which skills ship.** All 13 in `skills/`, or a subset.
- [x] **Internal files.** Decided (7 October 2026): at publish, this checklist, `docs/video-scripts/` and `docs/research/` move to the Sorted team's private folder, then every check below runs again.
- [ ] **Any announcement.** Posts, emails, directory listings or messages to anyone outside the team.

## Checks to run on the exact commit being published

- [ ] `python scripts/scan_public.py --denylist <private list>` prints `hits: 0` (it scans every file and every change in the git history).
- [ ] `python scripts/scan_public.py --selftest` passes (the scan can still catch a planted secret).
- [ ] `node scripts/lint_skills.mjs` ends with `ok - all skill checks passed`.
- [ ] `python scripts/sync_codex_plugin.py --check` prints `drift: 0`.
- [ ] `claude plugin validate . --strict` passes.
- [ ] The commit authors are a neutral identity, not a person (the leak scan checks this too).
- [ ] The README's three install paths were each followed once, from a clean machine or a clean assistant home.
