# G2 + G3 · /urban-renewal/pinui-binui/ and /urban-renewal/ · local build, 26.10.2026

Local only. Nothing was deployed, no REST write, no edit to a live file, `inc/instruments.php` was not edited, nothing committed.
Research and spec: `dna.md` (this folder). Proof: `proof-before-g2.md`, `proof-before-g3.md`, `proof-predicted-g2.md`,
`proof-predicted-g3.md`, `coverage-before-g2.md`, `coverage-predicted-g2.md`, `coverage-before-g3.md`, `coverage-predicted-g3.md`.

## Files
| File | What it is |
|---|---|
| `tools/urban/build_g2g3_data.py` | Builds `pinui.json` and `urcity.json` from the 2025 authority report (page by page, totals checked), the two laws, gov.il pages, renewal-stats.json and renewal-track.json. Rebuild is byte-identical. |
| `plugins/nadlan-config/assets/instruments/data/pinui.json` | 9 KB. The law (majorities, 1ד clocks, elderly, refusal grounds, abusive signing, what a deal must hold), the TAMA law rows, the tax and betterment annex, standard 21, the government calculator's assumptions, the report series (approval to permit 2015-2025, plans 2010-2025, tax-track declarations 2015-2025, districts), key 2025 numbers, sources. |
| `plugins/nadlan-config/assets/instruments/data/urcity.json` | 17 KB. Per city from the report: TAMA 38 replacement plans and status (+ self-promoted, + in force before), request-to-permit years, apartments sold 2025, tax-track declarations; the permits and requests split 2013-2025, building renewal 2025, the tracks comparison (annex A), districts, the law rows. |
| `plugins/nadlan-config/assets/instruments/tools/pinui.js` | Tool `pinui`: views maj / mine / time. Pure logic in `window.NLPB`. |
| `plugins/nadlan-config/assets/instruments/tools/urcity.js` | Tool `urcity`: views city / track / rank. Pure logic in `window.NLUC`. |
| `tools/instruments/test_g2g3.py` | 55 checks: rebuild identity, law numbers, 400 random clusters vs a Python reading of section 1, tax ceiling for 20-300 m², 1ד dates, city counts vs a Python recount and vs renewal-stats.json, report lines, track logic, strings (no long dash, banned words, zero counts), short line values, SVG ≥ 12 px. `python tools/instruments/test_g2g3.py` → PASS. |
| `write_g2_page.py`, `write_g3_page.py` | Page writers (exact anchored insertions + honesty fixes + Yoast title/description; backup, POST, read-back, live check). `--dry` reads the PUBLIC REST only. The real run is blocked by a `raise SystemExit` line until Ben's word. |
| `g2g3_common.py`, `infographics.py` | Shared helpers (tables, CSS, gates, link check) and the 7 SVGs (`svg/`). |
| `preview/g2-page-render.html`, `preview/g3-page-render.html` | Local renders of the new pages with the real tools: `http://localhost:8131/docs/research/2026-10-26-upgrades/g2g3-urban-renewal/preview/g2-page-render.html` (launch config `projects-hub-preview`). |
| `preview/shots/*` | 390 and 1280 px full-page screenshots (Edge headless), `shot.py` reports: no console errors, no sideways scroll, tools mounted. |
| `ds_g2g3.py` → DS components | `<scratchpad>/ds/project/components/PinuiBinuiPage/` and `UrbanRenewalHub/` (preview.html self-contained + README.md); copies in `preview/ds-*.html`. Not published. |
| `snippets/summaries.php`, `snippets/test_summaries.php` | The no-script summary branches for `nadlan_nli_summary()` (not applied); the test runs them on the real data (PASS). |
| `coverage-facts-g2.json`, `coverage-facts-g3.json`, `competitors-g2.txt`, `competitors-g3.txt` | Inputs of `tools/fact_coverage.py` and `tools/depth_proof.py` for the after-release proof. |
| `page-sources-g2.md`, `page-sources-g3.md` | Where every fact on each page comes from (internal, not printed). |

## Registry entries for `inc/instruments.php` (inside `nadlan_nli_tools()`, after `'invest'`; NOT applied)
```php
			/* G2 (HAD-601 round 2): "הבניין שלכם בפינוי בינוי"; pinui.json from the Pinui Binui law, the 2025 authority report and gov.il (tools/urban/build_g2g3_data.py, 26.10.2026) + the tracker */
			'pinui' => array(
				'name' => 'הבניין שלכם בפינוי בינוי: הרוב לפי החוק, מה מגיע לכם וכמה זמן', 'cat' => 'ReferenceApplication', 'kicker' => 'מחשבון · פינוי בינוי',
				'desc' => 'לפי חוק פינוי ובינוי בנוסחו היום: הרוב המיוחס בניין אחר בניין (שני שלישים במקבץ, שלוש חמישיות בכל בניין), מה חסר, מתי אפשר לבקש שמאי של הרשות בחינם, תקרת השטח לפטור ממס לדירה שלכם, החלופות לבני 70 ו-75, המועדים שהחוק נותן ליזם מהעסקה הראשונה, והשלב של המתחם אצל הרשות עם השנים מאז אישור התכנית מול הממוצע של הרשות.',
				'data' => array( 'pinui.json', 'renewal-track.json' ),
				'related' => array( '/urban-renewal/' => 'התחדשות עירונית', '/urban-renewal/map/' => 'מפת התחדשות עירונית', '/urban-renewal/check/' => 'בדיקת בניין חינמית', '/glossary/dayar-sarvan/' => 'דייר סרבן', '/glossary/shamai-pinui-binui/' => 'שמאי פינוי בינוי', '/my-renewal/' => 'חדר פרויקט לנציגות' ),
			),
			/* G3: "התחדשות עירונית בעיר שלכם"; urcity.json from the 2025 authority report (annex A, TAMA 38 by city) + the tracker */
			'urcity' => array(
				'name' => 'התחדשות עירונית בעיר שלכם: מתחמים, מסלולים ותמ"א 38', 'cat' => 'ReferenceApplication', 'kicker' => 'מפה · התחדשות עירונית',
				'desc' => 'לכל עיר: המתחמים במפת הרשות הממשלתית להתחדשות עירונית לפי שלב ומסלול, הדירות היום ואחרי הבנייה והמכפיל, מה זז מאז הבדיקה הקודמת, ומה דוח הרשות לשנת 2025 אומר על תמ"א 38 בעיר (התכנית המחליפה, ההארכה, הזמן מבקשה להיתר, הדירות שנמכרו). לבניין: איזה מסלול נשאר פתוח, פינוי בינוי, תמ"א 38 או תכנית לרישוי מהיר, וכמה חתימות צריך. והשוואת כל הערים.',
				'data' => array( 'urcity.json', 'renewal-track.json' ),
				'related' => array( '/urban-renewal/pinui-binui/' => 'פינוי בינוי', '/urban-renewal/tama-38/' => 'תמ"א 38', '/urban-renewal/tama-38-alternatives/' => 'מה במקום תמ"א 38', '/urban-renewal/map/' => 'מפת התחדשות עירונית', '/urban-renewal/check/' => 'בדיקת בניין חינמית' ),
			),
```
Run the keyword guard on the two `name` strings and the `related` anchors before applying (the bare anchors above each link to their owner: פינוי בינוי → /urban-renewal/pinui-binui/, התחדשות עירונית → /urban-renewal/, תמ"א 38 → /urban-renewal/tama-38/, מפת התחדשות עירונית → /urban-renewal/map/).

## No-script summaries
`snippets/summaries.php`: two branches for `nadlan_nli_summary()` next to `'urtrack'`. `php snippets/test_summaries.php` → PASS (pinui: the majorities table for 8 building sizes and the key line; urcity: the top 20 cities with complexes, approved, units after, multiplier and the TAMA 38 line).

## Release order (when Ben says go; by the hunk rules, one runner at a time)
1. Release: the two tools + two data files + the registry + the summaries (plugin files; `inc/instruments.php` read from LIVE first, per the repo-not-live lesson).
2. `write_g2_page.py` and `write_g3_page.py` (remove the `raise SystemExit` line), each: backup, POST, read-back, live checks (one h1, tool mounted, FAQPage with 29 / 25 questions, SoftwareApplication, title).
3. `tools/source_audit.py` before and after on both pages + rainbow and h-infinity; `tools/content_first_check.py` (H1 → answer → CTAs → tool on 412 px).
4. `tools/depth_proof.py` and `tools/fact_coverage.py` with `competitors-g*.txt` and `coverage-facts-g*.json` → proof-after; the honesty statement from it.
5. Weekly: `build_renewal_track.py` refresh flows into both tools automatically; `build_g2g3_data.py` only when the authority publishes a new report.
