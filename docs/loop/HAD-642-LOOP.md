# HAD-642 LOOP: tools and content on every project (Ben, 31.10.2026 night)

**Ben's order:** "תכנס ללופ ותשלים הכל, תשתמש ב-Claude Design, תוודא שאנחנו עם הכלים והתוכן הכי טובים. תתעדף את המרכז ויוקרה בשלב ראשון וגם אילת. פרויקטים של יזמים גדולים. שים לב לביטויי מפתח, בידול והימנעות מקניבליזציה."

**The loop:** a session cron fires every ~20 minutes. Each tick:
- reads this board;
- takes the FIRST unchecked item;
- does it end to end: design, build, release, verify on a phone;
- ticks it here with its evidence;
- sends Ben links at the end of every wave.

## Rules (every tick)

- **Additive law.** Never remove a strip, a tool or a 3D element from a page; add on top. On 31.10 Ben corrected me after I removed the Gefen strips.
- **Ashira:** never touch the page and never turn the slip on there.
- **3D and stage pages** (Rainbow, Dimri Yama, DUO, H Infinity, Einstein, Kikar Hamedina): add below the stage only. The engine and the cone are frozen.
- **Claude Design first** (DS artifact L9Nqz7Viv7K3MYeZrBc9s8), then code.
- **Releases:**
  - Use the chain `scripts/project-stage/make_deployNNN.py` (copy the latest, shift the numbers).
  - Read the lock line in `docs/coordination/claude-codex.md` and the live health in a SEPARATE command first.
  - Run the runner in the BACKGROUND, never under `timeout`.
  - On a "files written" record with a cut run, use the `verify538.py` pattern.
- **Inherited checks** that name counts (for example "פרויקטים בקטלוג: 942") must follow the live numbers after the registry refresh.
- **Honesty:** registry numbers and sourced lines only; no invented prices, dates or ranges.
- **Words:** language-dna blacklist; no long dashes; "תלת ממד" only in "סיור וירטואלי".
- **Keywords:**
  - One owner per head keyword (`tools/seo/kw_guard.py`, `tools/gsc/url_word_audit.py`).
  - A compound title is "<address>, <city>: פינוי בינוי". It never contains "פרויקטים חדשים" (the city hubs own that).
- **Campaign line in every report:** what is new in `C:\Users\777\Documents\grok-bot\nadlan-campaign\outbox`.

## Queue

- [x] **L0 Registry refresh** (31.10, 23:30). Result: 34 new compound pages; 18 statuses, 20 unit counts and 10 years updated; 0 hidden posts republished; 2 names renamed by the registry; `docs/qa/registry-2026-10-31/diff.json`. The catalog now counts 975. Original item: Finish `registry_refresh_20261031.py --continue`, then `--after`, then read `docs/qa/registry-2026-10-31/diff.json` (new pages, restored statuses, changed fields, changed titles).
- [x] **L0b Release 1.72.545** (released and verified). The viewing link was proven for a holdout visitor. Original item: The slip's viewing link fix (`?nudge=show`). Update the /projects/ and home count checks to the live numbers. Send Ben: https://nad-lan.co.il/projects/rainbow-tel-aviv/?nudge=show
- [x] **L1 Compound tool, wave 1: center + Eilat** (1.11, 00:30).
  - 345 written, 0 failed, Gefen already had it. 6 random pages checked at 390 px: title, visible H1, answer paragraph, stage strip, tools bar, tool.
  - 9 names with plan codes were re-cleaned by hand; the rule is now in `compound_wave.py`.
  - A compound whose registry row has no unit numbers shows no tool (nothing is invented).
  - Backup: `docs/qa/compound-wave/wave1-backup.json`.
  - Original item:
  - Code: a compound counts as upgraded when its content holds `[nadlan_compound_tool]` (no option list).
  - Cities: תל אביב-יפו, רמת גן, גבעתים, בני ברק, חולון, בת ים, הרצליה, פתח תקוה, רמת השרון, קרית אונו, אור יהודה, ראשון לציון, אילת.
  - Each compound gets, by REST:
    - an answer paragraph built from its own row (status-specific; the 4-year line on approved plans only);
    - the tool;
    - a clean title "<name>, <city>: פינוי בינוי" (strip ר"ג/ת"א/פ"ת style tails);
    - `data_quality=enriched`.
  - Backup and `--undo` like `cms538.py`.
  - Verify 5 random pages on a phone.
- [ ] **L1b Compound tool, wave 2:** every other city. RUNNING since 1.11 ~00:55 (634 compounds; dry plan clean: 0 odd names, 0 duplicate titles; rules for end-of-name plan codes, quotes and קרית to קריית added).
- [x] **L2 Big developers' projects** (1.11, 00:50).
  - Release 1.72.546 adds `inc/project-kit.php`; Claude Design v105.3 ProjectToolkit.
  - `[nadlan_project_kit]` was appended to 18 projects (`kit_cms.py`, backup `kit-backup.json`).
  - Checked on Rainbow, Park Bavli and DUO at 390 px: 4 instruments live, tabs work, the stage intact, Ashira without a kit.
  - Eilat has no developer project on the site yet. Einstein Tower is skipped because its article is pinned (iron law 6).
  - Original item:
  - Inventory the developer projects (not the registry), their developer, city and published price.
  - Claude Design `ProjectToolkit`: the site's instruments (data-nli: pcost, mortgage, cpi linkage, afford) prefilled with the project's own published numbers, plus "what else the apartment needs" (designer, engineer and handover inspection, kitchen, AC, closets) with sourced ranges.
  - Under the article, never inside the stage. Not on Ashira.
- [ ] **L2b Price slip on (WAITS for Ben's look, his rule of 31.10: "when I say it looks good, clone it to all"):** the big developers' projects in the center, luxury and Eilat (box = on). Never Ashira.
- [ ] **L3 Keyword map: center + luxury + Eilat.** A helper agent is researching (read-only); output goes to `docs/research/2026-11-01-keyword-map/`.
  - Sources: GSC 90 days plus DataForSEO volumes.
  - Map: owner URL per head term, gaps, cannibal pairs.
  - Fix titles and H1s so each page leads with its own words. No new URL without `url_word_audit`. Never a 301.
- [x] **L4 Home news band** (1.11, 01:20). Three real news items were published in the nadlan-news category (ids 8728, 8729, 8730):
  - /compounds-update-2026/: the registry in numbers;
  - /boi-decision-october-2026/: Bank of Israel, 3.25% on 21.10.2026, from the BOI briefing PDF;
  - /cbs-dwelling-july-august-2026/: CBS release 325/2026, -0.6% for Jul-Aug, -1.8% on the year.
  - Unverified dates were removed before publishing.
  - `url_word_audit` was run for every slug token: each token is owned only by its own new URL.
  - The home band is back (`nlhp-magazine` present).
  - Drafts and sources: `docs/content/news-2026-11/`.
  - Original item: three real, dated news items in the nadlan-news category (the registry refresh in numbers, plus two current market facts with sources), so the band returns.
- [ ] **L5 Report to Ben:** links, phone shots, what is left.

## Done

- 31.10: 1.72.538-544 live.
  - The tool on Gefen 8-10 (strips kept).
  - The price slip on Rainbow.
  - The glossary title quote fix.
  - The accessibility lift.
  - Commits f0c9e417 and e3983d33.
