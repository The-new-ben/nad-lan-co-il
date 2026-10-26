# G6 G7 G8: the professionals cluster, local build (26.10.2026)

Ben's order (26.10.2026): every keyword where we do not appear gets a winning page. This folder holds the research, the spec, the tools,
the page writers and the proofs for /home-inspection/ (בדק בית), /real-estate-appraiser/ (שמאי מקרקעין) and /real-estate-lawyer/
(עורך דין מקרקעין). **Nothing here is applied, deployed or committed.** Research and spec: `dna.md`.

## Files

| Path | What |
|---|---|
| `tools/instruments/build_pros_data.py` | builds the three data files from the official texts and the published price pages (125 checks; rebuild is byte-identical from `tools/instruments/pros-official-cache.json` without the private raw folder) |
| `plugins/nadlan-config/assets/instruments/data/bedek.json`, `shamai.json`, `orechdin.json` | the data (every value dated and sourced) |
| `plugins/nadlan-config/assets/instruments/tools/bedek.js` | tool `bedek` (G6): defect against the law, calendar, prices; logic `window.NLBD` |
| `plugins/nadlan-config/assets/instruments/tools/shamai.js` | tools `shamai` and `shamaireg` (G7); `shamaireg` searches the data.gov.il register live (CORS open), copies nothing |
| `plugins/nadlan-config/assets/instruments/tools/orechdin.js` | tool `orechdin` (G8); reads orechdin.json + ptax.json |
| `tools/instruments/test_g6g8.js` | `node tools/instruments/test_g6g8.js` → ALL 161 CHECKS PASS (test_tools.js still passes) |
| `snippets/registry.php` + `test_registry.php` | the 4 registry entries for `nadlan_nli_tools()` (NOT APPLIED); php -l clean, test PASS |
| `snippets/summaries.php` + `test_summaries.php` | the 4 no-script summary branches for `nadlan_nli_summary()` (NOT APPLIED); php -l clean, test PASS |
| `write_g6_page.py`, `write_g7_page.py`, `write_g8_page.py` | page writers (anchored insertions, backup, read-back, live check); `--dry` reads only the public REST. The real run is blocked by `raise SystemExit` |
| `g6g8_common.py` | shared tables, CSS (CTA `color:#fff!important`, `.nadlan-guide` overrides), gates, link check, renderer |
| `infographics.py` → `svg/*.svg`, `preview/svg.html` | the 9 drawings (3 per page) |
| `ds_pros.py` | Claude Design component ProsCluster in the scratchpad `ds/project/components/ProsCluster/` (preview.html + README.md, not published) and `preview/ds-ProsCluster.html` |
| `preview/` | `g6/g7/g8-page-content.html` (what the writer posts), `-page-render.html` (local render), `tools-harness.html`, `shots/` (390 and 1280 px) |
| `build_proof_inputs.py` → `competitors-g6/7/8.txt`, `coverage-facts-g6/7/8.json` | proof inputs |
| `proof-before-*.md`, `proof-predicted-*.md`, `coverage-before-*.md`, `coverage-predicted-*.md` | depth and fact proofs, live today vs local render |
| `competitors-dna-g6/7/8.md`, `serp/*.txt`, `page-sources-g6/7/8.md`, `kw-guard.txt` | competitor DNA, SERP summaries, internal source lists, guard log |
| `page-backup/` | the three live pages as rendered and their meta, 26.10.2026 |

## Title decisions (kw_guard on every one: OK)

| Page | Field | Live today | New |
|---|---|---|---|
| G6 | H1 (WP title) | בדק בית לפני קניית דירה: מה בודקים ואיך משתמשים בדוח | בדק בית: מה בודקים, כמה זה עולה ועד מתי הקבלן אחראי |
| G6 | Yoast title | בדק בית לפני קניית דירה: מה בודקים, מחיר וליקויים 2026 | בדק בית: מחירים 2026, מה בודקים ועד מתי הקבלן אחראי |
| G7 | H1 (hero h2) | שמאי מקרקעין עוזר להבין כמה הנכס באמת שווה, ומה עלול להשפיע על העסקה | שמאי מקרקעין: מתי צריך, כמה זה עולה ואיך בודקים שהוא מורשה |
| G7 | Yoast title | שמאי מקרקעין: מתי צריך הערכת שווי לעסקה \| nad-lan | שמאי מקרקעין: מחירים 2026, סוגי שומה ובדיקת רישיון |
| G8 | H1 (hero h2) | בעסקת דירה, עורך הדין הוא קו ההגנה לפני הכסף הגדול (no head term) | עורך דין מקרקעין: מה הוא בודק לפני החתימה, כמה זה עולה ואיך בוחרים |
| G8 | Yoast title | עורך דין מקרקעין: בדיקה משפטית לפני חתימת חוזה דירה - נדלן | עורך דין מקרקעין: שכר טרחה 2026 ובדיקות לפני חתימה |

Why: head term first, then the two intents the SERP and the AI overviews answer (price, and the check or the law), the year where the SERP
shows prices. Each page owns its head term in the guard; none takes a word another page owns. All three pages had 0 clicks in 90 days.
Meta descriptions are in the writers (all OK in `kw-guard.txt`).

## Release order (only on Ben's word; one runner at a time, lock line in docs/coordination/claude-codex.md)

1. **Release A (code):** `tools/bedek.js`, `tools/shamai.js`, `tools/orechdin.js`, `data/bedek.json`, `data/shamai.json`, `data/orechdin.json`,
   and in `inc/instruments.php` the 4 entries of `snippets/registry.php` (after 'pinui') and the 4 branches of `snippets/summaries.php`
   (next to the 'pinui' branch). Read the LIVE `inc/instruments.php` first (the repo is not always live); target = live + these additions.
   Version bump; check `/wp-json/nadlan/v1/health`; spot-check rainbow and h-infinity.
2. **Release B (content):** remove the `raise SystemExit` line in each writer, then `python write_g6_page.py`, `write_g7_page.py`,
   `write_g8_page.py` (each backs up, posts, reads back and checks the live page). `--style` (reform of the old gold and cream on G7 and G8)
   only on Ben's word. No sitewide change; three pages only.
3. **After:** `python tools/source_audit.py` on the three pages and the controls; `python tools/content_first_check.py`; depth and fact proofs
   on the live URLs with `competitors-g6/7/8.txt` and `coverage-facts-g6/7/8.json`; scroll check on phones; screenshots at 390 and 1280.
   Never Request indexing; a passive sitemap resubmit is the most allowed. Send Ben the three links.

## Local checks done (26.10.2026)

* `node tools/instruments/test_g6g8.js`: 161 PASS. `python tools/instruments/build_pros_data.py`: 125 checks.
* `php -l` + `test_registry.php` + `test_summaries.php`: PASS.
* `python write_g6/7/8_page.py --dry`: anchors found in the live content, internal links 200, gates passed (FAQ 25 / 24 / 28).
* `shot.py` on the three local renders at 390 and 1280: no sideways scroll, no console errors, every tool mounted with its answer.
* Proofs: 32 of 32 checked facts on each page (best competitor 15 / 14 / 21); see `dna.md` section 7.
