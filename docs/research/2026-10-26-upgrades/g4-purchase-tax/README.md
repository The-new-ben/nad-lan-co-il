# G4 /purchase-tax-calculator/ (page 6): local build, 26.10.2026

LOCAL ONLY. Nothing deployed, no REST write, no deploy script run, nothing committed. Research and spec: `dna.md` (this folder).

## Files

| File | What it is |
|---|---|
| `plugins/nadlan-config/assets/instruments/tools/ptax.js` | **Changed locally.** ptax v3 (header comment lists every rule and source). Standard engine, no core.js change. |
| `plugins/nadlan-config/assets/instruments/data/ptax.json` | **Changed locally, additive only** (new keys `pay`, `oleh_window`, `resident_months`, `not_sale`, `farm`, `cancel_form`, `checked_v3`). pcost, afford, nrm, dirafit read only old keys. |
| `test/test_ptax_v3.js` | `node docs/research/2026-10-26-upgrades/g4-purchase-tax/test/test_ptax_v3.js`: part 1 runs 2,961 v2 cases against `test/ptax-v2-live.js` (the live file, md5 df1cac4b...) and requires the same answer, label, sub-line, table, scenarios, formula, every v2 line and note; part 2 checks the v3 rules by hand (official examples of instruction 2/2026, payment dates, fines, the oleh window, partners, the link). ALL CHECKS PASS. `node tools/instruments/test_tools.js` still passes. |
| `write_g4_page.py` | The page writer (NOT RUN against the site). `--local` builds from `page-backup/page-6-reconstructed-20261025.html`; `--dry` reads the live raw through the bridge; no flag = backup, POST, read-back, live check. `--title` also sets the Yoast title and description. |
| `page-backup/page-6-reconstructed-20261025.html` | The live raw as of 25.10.2026 13:01:56 (the 25.10 backup + `fix_ptax_extension.py`), matched word for word to the public REST content read 26.10 12:27 (modified 2026-10-25T13:01:56). |
| `preview/index.html`, `preview/g4-page-content.html` | The local page with the real tool; `preview/shoot.py` serves the repo and checks 390 and 1280 px. |
| `preview/*.png` | Screenshots: page top, tool (default, two buyers, oleh), the three figures, the city table, at 390 and 1280. |
| `ds_component.py` | Builds the Claude Design component `scratchpad/ds/project/components/PurchaseTax2/` (preview.html + README.md). Not published. |
| `coverage-facts-g4.json` | 34 facts for `tools/fact_coverage.py`. |
| `proof-*-before.md`, `proof-*-predicted.md` | Depth and fact proofs: the live page today, and the local preview, against the same 14 competitors. |

Raw research (not in the repo): `C:\Users\777\nad-lan\_private-research\2026-10-26-upgrades\raw\g4\` (29 competitor HTML files, index.txt, SERP JSON, keyword JSON, GSC daily CSV, official PDFs and their text, the competitor text extracts).

## Release order (coordinator)

1. `node .../test/test_ptax_v3.js` and `node tools/instruments/test_tools.js` (both ALL CHECKS PASS).
2. Release `tools/ptax.js` + `data/ptax.json` (+ the optional registry snippet below) with the usual runner. Keep the inherited checks: ptax.js has `NLPT`, `register('ptax'`, `sellBy`, `oleh12`; the page has `data-nli="ptax"` and `20,183,565`. Add `payDue` to the ptax.js check list.
3. `python .../write_g4_page.py --dry` (read only), then without `--dry` (with `--title` if the title change is approved).
4. Live: source audit before/after, `tools/content_first_check.py`, press on a phone and a desktop (preset "שני קונים", an oleh with an aliyah date, 6 weeks late, copy the result and open the copied link: it must reopen the same numbers), spot-check rainbow + h-infinity.
5. Proof on the live URL: `tools/depth_proof.py` and `tools/fact_coverage.py --facts coverage-facts-g4.json` against the 14 URLs in `proof-depth-before.md`.

## Registry and no-script summary (inc/instruments.php): snippet, NOT applied

`'ptax'` desc, replace:
```
'desc' => 'מחשב את מס הרכישה על דירה לפי המדרגות של רשות המסים בכל המסלולים: דירה יחידה, דירה נוספת, עולה חדש, תושב חוץ, נכה, קרקע ומתנה לקרוב, ועד מתי כל שיעור בתוקף; למשפרי דיור גם עד מתי למכור את הדירה הקודמת, כולל הארכת המלחמה.',
```
with:
```
'desc' => 'מחשב את מס הרכישה על דירה לפי המדרגות של רשות המסים בכל המסלולים: דירה יחידה, דירה נוספת, עולה חדש, תושב חוץ, נכה, קרקע ומתנה לקרוב, ועד מתי כל שיעור בתוקף; מתי מדווחים ומשלמים ומה עולה כל שבוע של איחור; שני קונים לפי המעמד של כל אחד; חלון ההטבה לעולה ותקנה 12 מול 12א; ולמשפרי דיור עד מתי למכור את הדירה הקודמת, כולל הארכת המלחמה.',
```
In the `'ptax' === $id` summary, replace the closing sentence:
```
המס מחושב על שווי הדירה כולה, וקונה של חלק משלם לפי החלק שלו.</p>';
```
with:
```
המס מחושב על שווי הדירה כולה, וקונה של חלק משלם לפי החלק שלו. מדווחים תוך 30 יום מהעסקה ומשלמים תוך 60 יום, או מאוחר יותר כשהחזקה ורוב התשלום נדחים (סעיף 51); איחור בתשלום: 0.2% מהמס לכל שבוע ועוד הצמדה וריבית.</p>';
```
(Check that the old sentence matches exactly once; the summary is printed inside the tool host for readers without scripts and for search engines.)

## Title (the writer's `--title`)

SEO title `מחשבון מס רכישה 2026: סימולטור, מדרגות ומתי משלמים` (50 characters), H1 and breadcrumb unchanged. Description: `מחשבון מס רכישה 2026 לפי רשות המסים: דירה יחידה, נוספת, עולה, נכה, תושב חוץ ושני קונים. מדרגות, מתי משלמים, מה עולה שבוע איחור ועד מתי למכור דירה קודמת.` (152). Guard and audit results: `dna.md` 8.1.
