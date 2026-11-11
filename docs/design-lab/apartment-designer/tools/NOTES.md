# Apartment-design tools (HAD-707), 11.11.2026

17 Instruments tools for the three design pages. Nothing is live; nothing was committed. The releaser applies the hunk below on the **live** text of `inc/instruments.php` (the repo copy may differ from live).

## Files

| File | What |
|---|---|
| `plugins/nadlan-config/assets/instruments/tools/design.js` | the 17 tools (registry `'file' => 'design'`); pure math in `window.NLDS`; to-scale drawings built inside the file as SVG in `r.figure` (the engine has the slot, not a drawing kit); scoped CSS injected once (`#nlds-css`, selectors `[data-nli^="dsg"]`) |
| `plugins/nadlan-config/assets/instruments/data/design.json` | built, do not edit by hand |
| `tools/instruments/build_design_data.py` | builds design.json from `docs/research/2026-11-10-apartment-designer/prices-items/price-ranges.json` + `designer-fees.json` + the RULES and STEPS tables in the script; fails the build if a URL, a site name or a blacklisted word would reach the public file; four display-name and three note overrides (3D wording, "אריח") |
| `plugins/nadlan-config/inc/design-tools.php` | registry entries through the existing `nadlan_nli_tools` filter (same pattern as garden-tools.php) and `nadlan_dsg_summary( $id )`, the no-JavaScript summary of each tool (a sentence with a worked number and a table of the published ranges or rules). `php -l` clean |
| `docs/design-lab/apartment-designer/tools/harness.html` | all tools in the shortcode's markup with a hostile stand-in theme; `?only=dsgsofa` for one |
| `.../tools/test-design.mjs` | 406 unit checks: every formula, edge cases (zero, very large, missing price rows), and every tool's page compute on its defaults and every preset with the copy gate |
| `.../tools/test-summary.php` | 70 checks of the registry filter and the 17 summaries; writes `summaries.html` |
| `.../tools/check-tools.mjs` | headless Chrome, 390 px, touch: 199 checks; screenshots in `evidence/` + `receipt.json` |

Run: `python tools/instruments/build_design_data.py` · `node docs/design-lab/apartment-designer/tools/test-design.mjs` · `php docs/design-lab/apartment-designer/tools/test-summary.php` · serve the repo root `python -m http.server 47961 --bind 127.0.0.1` then `node docs/design-lab/apartment-designer/tools/check-tools.mjs`.

## The registry hunk (apply on the live `inc/instruments.php`)

1. Inside `nadlan_nli_summary( $id, $lang = 'he' )`, right after the `nlbudget` line (repo line 732):

```php
		if ( 0 === strpos( $id, 'dsg' ) ) { return function_exists( 'nadlan_dsg_summary' ) ? nadlan_dsg_summary( $id ) : ''; }  // 11.11.2026 (HAD-707): inc/design-tools.php
```

2. At the end of the file, after the `hazards-tools.php` line (repo line 1730):

```php
/* 11.11.2026 (HAD-707): the apartment-design tools (dsgfee ... dsgcurtain, tools/design.js on data/design.json); loaded only if present */
if ( file_exists( __DIR__ . '/design-tools.php' ) ) { require_once __DIR__ . '/design-tools.php'; }
```

No other line changes. Ship together: `inc/design-tools.php`, `assets/instruments/tools/design.js`, `assets/instruments/data/design.json`; add `design-tools.php` to the release's PHP list (the rollback-hunk lesson). The tools are Hebrew only (no `'en'` block), so `nadlan_nli_summary_en` needs nothing.

`related` links point only to pages that exist today (`/buying-apartment/`, `/guides/new-apartment-buyer-changes/`, `/home-inspection/`, `/apartment-purchase-cost-calculator/`). When the design pages go live, add them to `$rel` in `design-tools.php`.

## Which tool goes on which page

Shortcode: `[nadlan_tool id="dsgfee"]`; a page can open on a ready case: `[nadlan_tool id="dsgfee" preset="new"]`.

| Tool | Hebrew name (search phrase) | Hub `/design-studio/` | Price page `/design-studio/designer-cost/` | Designers page `/profession/מעצב-פנים/` |
|---|---|---|---|---|
| dsgfee | כמה עולה מעצב פנים לדירה (מחשבון עיצוב פנים) | teaser, `preset="r4"` | **first tool** | `preset="new"` |
| dsgquote | בדיקת הצעת מחיר של מעצבת פנים (דוגמא להצעת מחיר) | | **second** (the quote reader of C4) | yes |
| dsgwho | מעצב פנים, הום סטיילינג או אדריכל | yes | yes (saving options, C3) | **first** (the chooser) |
| dsgbudget | תקציב לעיצוב דירה | yes | **third** | |
| dsgfurnish | כמה עולה לרהט דירה | yes | yes | |
| dsgtime | לוח זמנים לדירה חדשה | yes (contractor flat) | yes (C2 contractor-flat section) | yes |
| dsgkitchen | כמה עולה מטבח (למטר) | yes | | |
| dsgfloor | מחשבון פרקט / כמה עולה פרקט למטר כולל התקנה | yes | | |
| dsgpaint | מחשבון צביעת דירה | yes | | |
| dsgsofa | מידות ספה לסלון | yes | | |
| dsgrug | גודל שטיח לסלון | yes | | |
| dsgdining | פינת אוכל: מידות | yes | | |
| dsgbed | עיצוב חדר שינה קטן | yes (small-flat section, E) | | |
| dsglight | תכנון תאורה לבית | yes (F) | | |
| dsgpoints | נקודות חשמל | yes | | |
| dsgstyle | סגנונות עיצוב פנים | yes | | yes (style filter) |
| dsgcurtain | וילונות ותריסים | yes | | |

Order on the hub follows the build order of `seo/manual-2026-11-11/tools-from-intent.md`. Owner laws still apply before release: Claude Design board first, keyword-guard and SERP headings for the page titles, no mass release in one day.

## Every number that is not a published price, and its basis

Kinds: **standard** = a published guideline or official figure; **thumb** = a common rule of thumb, said so on the page; **assumption** = our modelling choice. All live in `design.json` `rules` with the same text.

| Rule | Value | Kind | Basis | Needs a source? |
|---|---|---|---|---|
| main walkway | 90 cm | thumb | Neufert, Architects' Data (main circulation ~90 cm) | an Israeli guide would be better |
| narrow walkway | 60 cm | thumb | common planning rule | yes |
| sofa to coffee table | 45 cm | thumb | 40 to 50 cm rule | yes |
| margin at a side wall / in a door | 5 cm / 2 cm | assumption | play to push in / carry through | no |
| corridor turn | geometry | exact | longest flat rectangle of thickness w through a right-angle corner: min over θ of (a·sinθ + b·cosθ − w)/(sinθ·cosθ); w = 0 gives (a^⅔+b^⅔)^{3/2} (tested) | no; "maybe" when it fails flat but the ceiling is higher than the sofa (carried on its end) |
| stretcher lift | 110 × 210 cm | thumb | common cabin of the stretcher lift Israeli high-rises must have; example only | yes (the standard's exact cabin) |
| rug overhang / under sofa / wall margin | 15 / 20 / 30 cm | thumb | styling rules; search answers showed 15 to 50 cm to the wall | yes |
| ready rug sizes | 120×170 … 300×400 | thumb | sizes sold in Israel | no |
| seat width (rectangular) | 60 cm | standard | Neufert | no |
| seat on a round table | 65 cm of edge | thumb | our rounding up for a curved edge | yes |
| table depth | 90 cm | thumb | 80 to 100 cm usual | no |
| chair clearance | 81 / 91 / 112 cm | standard | NKBA Kitchen & Bath Planning Guidelines, seating clearance (32 / 36 / 44 in) | no |
| table end | 60 cm | thumb | | yes |
| bed sizes | 90, 120, 140, 160, 180 | thumb | mattress sizes sold in Israel | no |
| bed side / foot | 60 / 70 cm | thumb | planning rule (50 minimum; 60 to 90 at the foot) | yes |
| wardrobe depth / front | 60; 90 hinged, 60 sliding | thumb | | yes |
| lux by room | living 150, dining 200, kitchen 300, bedroom 150, kids/study 300, bath 250, hall 100 | thumb | inside the IES Lighting Handbook residential ranges | an Israeli standard (ת"י 8995 is for workplaces) |
| lumen loss factor | ×1.25 | thumb | light lost on walls and shades | yes |
| lumens per fitting | spot 600, ceiling 2000, pendant 1200, LED profile 1000/m | thumb | catalogue outputs of LED fittings | per product |
| each fitting = one lighting point (profile = one) | | assumption | electricians may group spots on one point (said on the page) | ask an electrician |
| Kelvin by room | 2700 to 4000 | thumb | the search answer for תכנון תאורה לבית (11.11.2026) | no |
| paint coverage | 10 m² per litre per coat | thumb | interior acrylic data sheets: 8 to 12 | per brand |
| door opening | 1.7 m² | thumb | 0.80 × 2.10 | no |
| cans | 18, 5, 1 l; greedy, a 5 when over 3 l left, an 18 when over 14 l left | thumb / assumption | sizes in Israeli shops | no |
| quick-mode walls | rooms + 2 spaces, each square | assumption | said on the page; "room by room" mode is exact | no |
| flooring waste | straight 8%, diagonal 15%, herringbone 15% | thumb | installer rule (5 to 10%; 15%+) | yes |
| pack sizes | 60×60 1.44, 80×80 1.28, 120×120 1.44, laminate 2.2, engineered 2.0, SPC 2.2 m² | thumb | usual packs; field is editable | per product |
| reserve | 10% | thumb | 10 to 15% budgeting rule | **yes, an Israeli source** |
| VAT | 18% | standard | Israeli VAT since 1.1.2025 | no |
| flat size by rooms | 2: 60, 3: 80, 4: 100, 5: 130, 6: 150 m² | assumption | the bands the search answers use with fee tables (architecture.md); 2 and 6 ours | yes |
| kitchen run by rooms | 3 to 6.5 m | assumption | opening example only | no |
| level split | thirds of the usual band (or of the full range) | assumption | said on every page that uses it | ideally per-level prices |
| service split | planning only = lower half, full supervision = upper half of the fee band | assumption | the sources describe the band "from planning only to full supervision" | yes |
| painting in the budget | the published 4-room price × area / 100 m² | assumption, rough | the per-m² wall price and the whole-flat price disagree (2 to 3×); the paint tool shows both and says so | **yes** |
| AC in the budget | the 4-room all-in range for any size | rough | sources contradict | yes |
| furnishing basket per room | fixed list (living: sofa, armchair, coffee table, TV unit, 200×290 rug, floor lamp; ...) | assumption | in `BASKET` in design.js | could follow the engine's furniture list |
| timeline offsets | from 20 months before handover (choose a designer) to 1 month after (painting, moving) | assumption, labelled "typical, not a rule" | the order of `market/journey-and-trades.md`, which itself calls the timing an assumption; only the CBS build time (32.3 / 37.8 months, release 089/2026) is sourced | **yes, every offset**; the developer's change deadline has no public source |
| style quiz scoring and palettes | 5 questions, 7 styles, 5 colours each | assumption (design advice, not a fact) | | Ben or a designer to review |
| electrical points example | living 4→7, kitchen 5→7, bedrooms 3→4 or 5 | example only, labelled | our invented 4-room example plan, not a project's specification | a real sale specification |

Prices: every price comes from design.json (two research files, read November 2026). The usual band is used where the research found one, else the full range. A range with confidence "low", fewer than 2 sources, or no usual band is marked **גס**. VAT is stated per item ("לא צוין" for most). Fee rows go back to 2021 and the fee tool says so. Rounding for display: the low end down, the high end up (never shrinks a published range).

## What would make each tool better with real data

- **dsgfee / dsgquote / dsgwho**: real quotes from the directory's designers (with consent) by service level, so the halves become measured; an architect's apartment fee (no published range found, the tool shows none).
- **dsgbudget / dsgfurnish / dsgstyle**: per-level prices (basic, mid, high) instead of thirds; washing machine and dryer prices (missing); the furniture list read from the designer engine's plan instead of a fixed basket.
- **dsgkitchen**: what "price per metre" includes (uppers or not), the cause of the 1,200 to 8,500 spread; appliance usual bands (only full ranges today).
- **dsgfloor**: labour surcharge for diagonal and herringbone; real pack sizes per product.
- **dsgpaint**: a paint price per litre (no published paint price, so do-it-yourself needs the reader's price); the painters' measuring basis (floor m² vs wall m²) to reconcile the two published prices.
- **dsgsofa / dsgrug / dsgdining / dsgbed**: read the room sizes, door widths and furniture straight from the plan in the designer engine; an Israeli source for the clearances; real lift cabin sizes by building.
- **dsglight**: an Israeli residential lux guide; fittings catalogue with lumens.
- **dsgpoints**: the project's real sale specification (points per room) from the developer; the developer's change price list.
- **dsgtime**: the developer's real deadlines from the contract; a sourced lead time for kitchens and furniture.
- **dsgcurtain**: whether the per-m² curtain price includes fabric, sewing and fitting; the shutter minimum per window.

## What the engine could not do, and how it was done here

- To-scale drawings that follow every keystroke: built inside design.js as SVG strings returned in `r.figure` (the engine's existing slot) and recomputed on each change. No engine change.
- A text column in `rows` wider than the numbers, and 44 px short segmented buttons: scoped CSS in design.js (`[data-nli="dsgpoints"] .nli__row`, `[data-nli^="dsg"] .nli__seg button{min-width:48px}`). Worth moving the min-width into core.css for every tool (core's segmented buttons with one-digit labels are 38 px wide).
- Hebrew verdicts in the answer and in the value column: the engine sets them in the mono face, left to right, which spaces Hebrew letters and can flip mixed text. The design tools override this for their own blocks (sans, `direction:rtl`, `unicode-bidi:isolate`).

## Checks run (11.11.2026)

- `test-design.mjs`: 406 passed, 0 failed.
- `test-summary.php`: 70 passed, 0 failed; `php -l inc/design-tools.php` clean.
- `check-tools.mjs`: 199 passed, 0 failed at 390 px with touch (every ready case pressed, a typed change, the drawing present, no horizontal scroll with the table open, every control at least 44 × 44, no page errors). Screenshots in `evidence/`, read one by one; fixed after looking: mono Hebrew verdicts, cramped tables, flipped dimension labels, a 12-field sofa form (the way in is now one yes/no), a bedroom model that wrongly failed a normal kids' room (wardrobe position added).
