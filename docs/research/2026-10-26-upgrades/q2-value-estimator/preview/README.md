# pval v2: the home value tool with three official checks (local build, 26.10.2026)

The tool `pval` of https://nad-lan.co.il/property-value-estimator/ (and of the neighbourhood pages that mount it with a page case),
upgraded per `dna.md` sections 4, 5 (V1 to V13), 7.5 item 3, 7.7 (I1, I3) and 7.8 (the moat: "שווי היום לפי מחיר הקנייה שלכם,
בשלוש בדיקות רשמיות"). **Local only: nothing deployed, nothing committed, no inc/*.php, core.js or core.css touched.**

## Files

| file | status | what |
|---|---|---|
| `plugins/nadlan-config/assets/instruments/tools/pval.js` | changed | v2 (same id, every v1 field, same v1 numbers) |
| `plugins/nadlan-config/assets/instruments/data/value.json` | changed | the 23 cities byte-identical in content to git HEAD, plus יבנה (2660) with its 8 neighbourhoods (47 KB, 10 KB gzip) |
| `plugins/nadlan-config/assets/instruments/data/value-series.json` | new | key `vseries`: 22 quarters for every city and 529 neighbourhoods, Israel, CBS 40010 + 60000 to 60500, settlement to district (224 KB, 52 KB gzip) |
| `tools/instruments/build_value_series.py` | new | reproduces both data files from the official sources (cache, fetch log, checks) |
| `tools/instruments/test_pval_math.py` | new | 76 checks, the real pval.js in node against an independent Python port and git HEAD |
| `docs/research/2026-10-26-upgrades/ds_tools.py` | changed | a `ValueAnchors` entry; a case may now carry a whole page case (dict) as well as a preset name |
| `q2-value-estimator/data/` | new | `fetch-log.json` (741 requests, all HTTP 200, Last-Modified 20.8.2026), `series-cities.csv`, `cbs-dwelling-index.csv`, `build-report.json`, `value-json-gains.csv` |
| `q2-value-estimator/preview/index.html` | new | the real engine + tool + data inline, 7 cases |
| `q2-value-estimator/preview/render_preview.py` | new | Chrome at 390 and 1280 px, presses every control, `render-report.json`, `shot-*.png` |
| `q2-value-estimator/preview/pval-summary-v2.php` | new | OPTIONAL summary branch (not applied) |

Another session is writing the page itself in this folder at the same time (`write_q2_stage2.py`, `infographics.py`,
`fetch_q2_data.py`, `data/q2-*.json`, `preview/q2-stage2-*.html`); none of those files were touched.

## Data

- **Deal medians**: `data.nadlan.gov.il/api/pages/settlement/buy/<code>.json` (24 cities) and `/neighborhood/buy/<id>.json`
  (all 726 neighbourhoods the cities list, 0 missing), version 20-08-2026, read 26.10.2026 01:13 to 01:26 UTC at about 1 request a
  second. Every quarter key is checked equal across files; the Israel line is identical in all 24 files; each neighbourhood's
  own city line equals the settlement file. Nulls stay null (529 neighbourhoods have at least one value; series that are all
  null are dropped).
- **CBS dwelling price index**: `api.cbs.gov.il/index/data/price?id=…`, 40010 monthly from 1.1994 (base 1993 average), the six
  districts from 10.2017 (base October 2017), all to 7.2026, one base each (checked, no chaining needed).
- **District**: CBS localities list on data.gov.il (resource 5c78e9fa-c2e2-4771-93ff-7f400a12f7ba) gives the sub-district, the
  same sub-district to district map as `tools/urban/build_renewal_stats.py` gives the district. All 24 cities map (Yavne: רחובות →
  המרכז → 60300; Herzliya and Ramat HaSharon: תל אביב).
- **value.json check**: every city figure and every neighbourhood figure of HEAD was compared with the fresh files: 0 mismatches.
  By value.json's own documented rule (newest median within the last four quarters) 4 neighbourhood figures are missing from
  HEAD (`data/value-json-gains.csv`: Haifa גבעת דאונס 5 rooms, Netanya נאות שקד 3 rooms and עיר ימים 5 rooms, Tel Aviv הצפון הישן
  4 rooms, all 7-9.2025). **Not added**, so every existing case keeps its number; adding them is one line in the builder if wanted.
- Rebuild: `python tools/instruments/build_value_series.py [--cache DIR] [--offline] [--refresh]` (default cache in the temp
  folder; `--offline` rebuilds from the cache).

All dna.md facts reproduce from the files: V2, V3, V4, V5 (Yavne 2,473,700 ₪, +6.7%, 8 neighbourhoods), V7 (590.0, -1.8% on the
year, peak 609.8 in 1.2025), V8 (all twelve district numbers) and **V10 exactly**: 1,780,200 × 579.9 / 447.7 = 2,305,870 → 2,305,900 ₪
(+29.5%) by the Center district; × 590.0 / 448.5 = 2,341,846 → 2,341,800 ₪ (+31.5%) by the national index; Yavne 4 rooms
1-3.2026 = 2,473,700 ₪ (+39.0%).

## The tool, v2

- **New fields** (all optional, all in `defaults`, so a page case can set them): `kind` (דירה / דירת גן / פנטהאוז / בית פרטי),
  rooms 2 to 6 (2 uses the 3-room series, 6 the 5-room series, said in the label "(במקום 2)" and in the note), `buyY` and `buyM`
  (purchase year 1994 to 2026 and month), `bought` (purchase price). City, neighbourhood and rooms now show in both methods
  (they feed check 1, the drawings and checks 2 and 3).
- **Check 1** = v1's base (neighbourhood median within four quarters, else the city), with its quarter.
- **Check 2** = purchase price × index in the latest month ÷ index in the purchase month: the district series when it has the
  month, else 40010 (and the note says why: no district, or a month before the district series). Rounded to 100 ₪.
- **Check 3** = purchase price × median now ÷ median in the purchase quarter, same place and room series: the neighbourhood when it
  has both quarters, else the city (said). Rounded to 100 ₪.
- **The answer stays v1's adjusted estimate** (D). Lines add check 2 and 3 with their months or quarters and the change in percent,
  the lowest and highest check, the spread, and the asking price placed on the range (above the highest, below the lowest, or
  inside it). The range is between the official checks 1 to 3; D and the asking price are shown on the same scale.
- **Notes**: which check is missing and why (purchase after 7.2026, before 1.1994, before 1-3.2021, no median in that quarter,
  no price or month yet), a plain sentence when the checks are more than 10% apart (quarter mix, district against
  neighbourhood), the CBS provisional line once when check 2 shows, the property type line (garden and penthouse: the median does
  not separate types; house: the median is of apartments only, compare by m² and ask an appraiser), and always "הערכה ראשונית,
  לא חוות דעת שמאית". The word שומה is never used.
- **Drawings** (`figure`, raw SVG from escaped parts, text 12 to 14 px in a 420-wide box): I3, the checks numbered 1 to 3 in registry
  blue on one scale, the shaded range, the estimate as a graphite diamond, the asking price as the only stamp-red element (a pin),
  legend with every value and date; shown when there is more than one distinct value. I1, 22 quarters of the place (registry blue,
  dots on every published quarter, a faint dotted bridge over quarters with no median) against Israel (graphite dashes), the
  purchase quarter and price marked; shown whenever the series file is loaded.
- **Presets** (from the data, no typed numbers): `yavne21` (V10), `tlv22` (Tel Aviv, bought at the 4-6.2022 median, asking price
  5,900,000 ₪ labelled as an example), `bhk22` (Beit HaKerem, bought at the neighbourhood's 1-3.2022 median; the checks disagree by
  more than 10% and the note says why). A page can open on one: `[nadlan_tool id="pval" preset="yavne21"]`.
- **Strip**: adds "מדד מחירי הדירות, שנה עד 7.2026: −1.8%".
- **Without value-series.json** the tool runs as v1 (the purchase year list holds only "בלי בדיקה לפי הקנייה"); checked.
- Bidi: signed percentages inside Hebrew labels sit in LTR isolates (U+2066/2069) and quarter labels carry word joiners so
  "1-3.2026" never breaks at its hyphen; the visible text is unchanged.

### Decisions to confirm

1. **District index from 10.2017, not from 2018.** The CBS API serves the district series from October 2017 (their base month).
   The tool uses the district whenever the series has the purchase month, so October to December 2017 use the district, not
   40010 as dna.md 7.8 says ("before 2018"). A one-line condition in `idxCheck` changes it if the spec wording should win.
2. **The m² method shows one more line**, "להשוואה: חציון 4 חדרים, …", the official median beside the m² result (the only
   difference the backward check allows, and it checks it is exactly that line).
3. **The range is between the official checks**, not including the adjusted estimate; the estimate sits on the scale as a diamond.

## Registry change for `inc/instruments.php` (not applied)

```php
'pval' => array(
    'name' => 'מחשבון שווי דירה', 'cat' => 'FinanceApplication', 'kicker' => 'מחשבון · שווי דירה',
    'desc' => 'כמה שווה דירה לפי העסקאות שנסגרו: המחיר החציוני לפי מספר החדרים בשכונה או בעיר (נתוני רשות המסים), עם התאמות למצב, לקומה ולבניין, טווח זהירות ובדיקת מחיר מבוקש, או חישוב לפי מחיר למ״ר. מי שמזין מתי קנה ובכמה מקבל שלוש בדיקות רשמיות: החציון היום, מדד מחירי הדירות של הלמ״ס במחוז, והחציון מאז הקנייה.',
    'data' => array( 'value.json', 'value-series.json' ),
    // 'related' unchanged
),
```

Only the `data` line is required (the `desc` sentence is optional). `grisrael` keeps `value.json` and simply gains Yavne in its
city list. Upload set for a release: `tools/pval.js`, `data/value.json`, `data/value-series.json` (+ the PHP line).
Optional: to let a page case carry a purchase without a preset, add `buyY`, `buyM`, `bought` to the shortcode's key list
(`kind` is already passed).

## Optional summary branch for `nadlan_nli_summary( 'pval' )`

`pval-summary-v2.php` holds `nadlan_nli_pval_summary_v2( $dir )`: today's city table unchanged (Yavne row included), then one
paragraph computed from the data: the CBS index of the latest month with its yearly change and the provisional note, the three
checks in one sentence and the V10 example (2,305,900 ₪, Yavne 2,473,700 ₪ in 1-3.2026), ending with "הערכה ראשונית, לא חוות
דעת שמאית". `php -l` clean; `php preview/pval-summary-v2.php` prints it from the repo data. To apply, replace the body of the
`'pval'` branch with `return nadlan_nli_pval_summary_v2( dirname( __DIR__ ) . '/assets/instruments/data' );`. The existing branch
needs no change for Yavne to appear.

## Checks

- `python tools/instruments/test_pval_math.py`: **PASS, 76 checks, 0 bad**. The data (HEAD cities unchanged, V2 to V8), V10 from
  the evidence CSVs and through the real pval.js (also the national fallback 2,341,800 ₪), the Python port against
  `NLPV.anchors` on 267 cases (every miss reason seen), v1 at git HEAD against v2 on 2,232 cases (default, every city × rooms 3
  to 5 × whole city and every neighbourhood, the five neighbourhood page cases, m² method): same answer, range, lines,
  breakdown, scenarios, table, formula, share text, note prefix and first source; the v2 surface (presets, fallbacks, property
  type lines, misses, no long dashes or banned words in any output or in the file, figure text ≥ 12 px).
- `node tools/instruments/test_tools.js`: ALL CHECKS PASS (its pval checks run against v2).
- `python docs/research/2026-10-26-upgrades/ds_tools.py ValueAnchors` then `python …/preview/render_preview.py`: 390 and 1280
  px, every control of every case pressed (3 presets, 3 segmented groups, 4 selects, purchase month and price, 6 inputs, 3
  scenarios, the table, copy, WhatsApp link, print): no sideways scroll before or after, no console errors or warnings, no
  field errors. Screenshots: `shot-p-full.png`, `shot-d-full.png`, `shot-{p,d}-{v10,ask,house}.png`.

## Not verified

- Nothing on the live site: the real WordPress mount (two data files in `data-nli-data`, theme CSS around the SVG) is simulated
  by the preview, not seen.
- Safari and Firefox were not run (Chrome only); the LTR isolates and word joiners are standard but unseen there.
- "The official median is for apartments only" is the spec's wording (dna.md task brief); the files say rooms, not property type.
- CBS values of recent months are provisional and will be revised; the builder must be rerun when CBS publishes (monthly) and
  when the nadlan.gov.il files change (Last-Modified is in the fetch log).
