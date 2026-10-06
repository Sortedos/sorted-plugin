# Release checklist

Every decision below belongs to the repository owner. None of them has been made. The repository exists only locally, with no remote, until they are.

## Owner decisions before publishing

- [ ] **Name and place.** The repository's name and the GitHub organisation it lives in. It should carry only the Sorted brand.
- [ ] **Private first.** Create it private, push, review it on GitHub, and only then decide public or private.
- [ ] **License.** Choose one, replace the license placeholder file with a real `LICENSE` file, and add the same license id to `.claude-plugin/plugin.json` and `plugins/sorted/.codex-plugin/plugin.json` (both carry no license field today).
- [ ] **Public contact.** Which address or page receives security reports and support questions. Until then every document says "use the contact link on the Sorted website"; no address or phone number is written here.
- [ ] **Feeds switched on.** The skills that send numbers need the four feed tools (`define_feed`, `feed_numbers`, `list_feeds`, `end_feed`) on the live Sorted service. Until they are on for a company, those six skills tell the assistant to stop and say so.
- [ ] **Which skills ship.** All 13 in `skills/`, or a subset.
- [ ] **Any announcement.** Posts, emails, directory listings or messages to anyone outside the team.

## Checks to run on the exact commit being published

- [ ] `python scripts/scan_public.py --denylist <private list>` prints `hits: 0` (it scans every file and the git history).
- [ ] `python scripts/scan_public.py --selftest` passes (the scan can still catch a planted secret).
- [ ] `node scripts/lint_skills.mjs` ends with `ok - all skill checks passed`.
- [ ] `python scripts/sync_codex_plugin.py --check` prints `drift: 0`.
- [ ] `claude plugin validate . --strict` passes.
- [ ] The commit authors are a neutral identity, not a person (the leak scan checks this too).
- [ ] The README's three install paths were each followed once, from a clean machine or a clean assistant home.
