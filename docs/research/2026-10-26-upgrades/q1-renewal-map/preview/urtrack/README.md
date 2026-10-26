# urtrack: "יומן המתחמים", the complex tracker with history (local build, 26.10.2026)

The moat of https://nad-lan.co.il/urban-renewal/map/ from `dna.md` section 7.8. For every urban renewal complex: the stage and
track at the authority today, the stage in the data.gov.il file and in our own import, units today and after building with the
multiplier, the plan number with its approval and deposit dates, "מופיע במאגר מאז", and every change seen between dated snapshots,
each with its check date. A second view, "מה זז במאגר", gives the count line and the table of all changes (T8).

**Local only.** Nothing deployed, nothing committed, no `deploy*.py` run. No `inc/*.php`, `core.js` or `core.css` touched. Nothing
written to the live site: every request was a read-only GET. The 947 imported project pages were not changed or refreshed. No Linear
or Notion item was created.

## Files

| file | status | what |
|---|---|---|
| `tools/urban/build_renewal_track.py` | new | fetches the sources (read only), keeps dated raw snapshots, builds the JSON |
| `plugins/nadlan-config/assets/instruments/data/renewal-track.json` | new | key `urtrack`, 1,015 complexes, 134 changes, 228 KB (minified) |
| `plugins/nadlan-config/assets/instruments/tools/urtrack.js` | new | the engine tool; pure logic in `window.NLUR` |
| `tools/instruments/test_urtrack.py` | new | 100 checks: totals against `renewal-stats.json`, an independent recomputation of the changes, the tool in node |
| `docs/research/2026-10-26-upgrades/ds_tools.py` | changed | an `UrbanTracker` entry, plus two small backwards-compatible options (`outdir`/`outfile`; every case may now be a preset name or a whole page case as a dict) |
| `preview/urtrack/index.html` | new | the real engine, the tool and the data inline, 9 cases |
| `preview/urtrack/render_preview.py` | new | Chrome at 390 and 1280 px, presses every control, writes `render-report.json` and `shot-{p,d}-*.png` |
| `preview/urtrack/urtrack-summary.php` | new | the summary branch for `nadlan_nli_summary('urtrack')`, NOT applied (linted and run, see below) |
| `C:\Users\777\nad-lan\_private-research\2026-10-26-upgrades\raw\q1-track\` | new, private | the history: `site_2026-07-13.json`, `file_2026-08-15.json`, `map_2026-10-20.json`, `map_2026-10-25.json`, `xplan_2026-10-26.json` |

## Sources and snapshots

Each snapshot is named by the date of the data in its source (that is "תאריך הבדיקה" in the tool), and it records when we read it.

| snapshot | source | rows | complexes | read |
|---|---|---|---|---|
| 13.7.2026, our import | `https://nad-lan.co.il/wp-json/wp/v2/nadlan_project` (public REST, `source=urban_renewal`; 892 of the 947 posts were last modified on 13.7.2026, the import run) | 947 | 947 | 26.10.2026 |
| 15.8.2026, data.gov.il file | resource `f65a0daf-f737-49c5-9424-d378d52104f5`, `last_modified` 15.8.2026 22:00 UTC | 970 | 970 | 26.10.2026 |
| 20.10.2026, authority map | ArcGIS `GIS_UrbanRenewal/FeatureServer/1`, `dataLastEditDate` 20.10.2026 22:23 UTC (the research pull of 25.10.2026, imported with `--import-map`) | 999 | 992 | 25.10.2026 |
| 25.10.2026, authority map | same layer, edited again 25.10.2026 23:23 UTC | 1,000 | 993 | 26.10.2026 |
| XPLAN | `ags.iplan.gov.il/.../PlanningPublic/Xplan/MapServer/1`, by plan number | 780 plans found | 787 complexes with dates | 26.10.2026 |

- `/wp-json/nadlan/v1/renewal-map-data` gives city totals only (947 in 76 cities), with no stage per complex, so the per-complex
  stage of our import comes from the project REST above. Its `source_id` is not exposed, so our rows are joined to the authority id
  by city plus a folded name (936), then by the planning-site plan id in `source_url` (2). The other 9 are in our import only
  (none of them in the 15.8 file or on the map).
- **Stable key:** the authority's complex number (`MisparProject` = `MisparMitham`). A complex drawn as several polygons is one
  row per polygon on the map (999 rows, 992 complexes on 20.10.2026), and the duplicates are identical, so they are merged. A
  complex that leaves under one number and enters under another in the same snapshot, with the same city and name, is merged as
  **renumbered**, and its history moves with it. There was one: פנמה 4, Jerusalem, 8003241 became 8003958 on 20.10.2026.
- **One stage ladder:** תכנון ראשוני, תכנון סטטוטורי, תכנית מאושרת לפני מימוש, במימוש, אחרי רישוי. The map has no "after licensing"
  code and leaves the stage empty: the 177 complexes the file calls "after licensing" are exactly 177 of the map's 188 without a
  stage. So an empty map stage is shown as "the map gives no stage", next to the file's stage and its date, and is never counted as
  a step back. A move between in-implementation and after-licensing has no direction (labelled "השלב השתנה").
- **XPLAN (F12): included.** It was reliable by plan number: 1,096 plan strings in 28 batched queries, 3.3 seconds, no error, 780
  found (729 of the 804 national-format numbers; old local formats match less often). The approval publication date
  (`pl_date_8`) is present only at the approval station, so it is labelled "פרסום אישור ברשומות". `depositing_date` is the
  deposit *discussion* date and is labelled "דיון בהפקדה". The authority's own approval date (`taarichTokef`) is shown too. When it
  equals XPLAN's, one line says "(הרשות ו-XPLAN)". One caveat: XPLAN's server only completes TLS with an older cipher set, so the
  builder uses a relaxed SSL context for that host alone (`DEFAULT@SECLEVEL=1`; curl connects without it).

## Numbers (checked by the test)

- Totals match `plugins/nadlan-config/data/renewal-stats.json`: **970** in the 15.8.2026 file (and its stage counts 111 / 282 / 344
  / 55 / 177 / 1 malformed), **999** rows on the map on 20.10.2026 (and its stage counts, 79 localities), **947** in our import
  (equal to the research pull of `/renewal-map-data`).
- Research F10 holds exactly at 20.10.2026: **17** moved up between the file and the map, 36 added (35 new + 1 renumbered), 14 no
  longer listed (13 + 1 renumbered).
- Changes, 134 in all: 13.7 to 15.8: 32 added, 18 moved up, 9 left the list. 15.8 to 20.10: 35 added, 17 moved up, 13 left, 7 track
  changes, 1 renumbered. 20.10 to 25.10: 1 added (עליית הנוער, Haifa) and 1 moved up (הראשונים העצמאות תשי"ג, Migdal HaEmek, from
  preliminary to statutory). No complex moved down.
- **The count line** (file of 15.8.2026 against the map of 25.10.2026): "מאז 15.8.2026 נוספו 36 מתחמים, 18 עלו שלב, 13 לא מופיעים
  עוד ו-1 קיבל מספר מתחם חדש". Per city in `agg.cities` (Jerusalem: 4 added, 3 moved up, 2 left, 1 renumbered).

## The tool

- **Fields:** the view (one complex / מה זז במאגר); city (all 79 cities in the data, with counts; in the moves view also "all
  cities"); free-text search by complex name, street or plan number, with spelling folded both ways (גבעתיים/גבעתים, פתח
  תקווה/פתח תקוה, קריית/קרית, ו/וו, י/יי, no niqqud or punctuation); the complex (that city's complexes, or the search results across
  cities, with complexes on today's map first). City and complex always stay together. Choosing a city opens its newest move, and
  clearing a search with no result goes back to the complex shown before.
- **Presets** (built from the data, so they follow each refresh): כפר שלם, Tel Aviv (approved to in-implementation on 20.10.2026),
  the newest move up, the newest addition, a complex that left the map, the search "גבעתיים", and the moves view.
- **One complex:** the answer is the stage at the authority today with the track and the kind (for example עיבוי). When the
  complex is not on today's map, the answer is red and says the last stage, with its source and date. The lines show: the file's
  stage when it differs; units today and after building, with the source and date; the multiplier (labelled "חישוב שלנו"); the
  file's units when they differ; the plan number; the approval date (authority and XPLAN); the deposit discussion; the XPLAN
  station; the declaration date; permits; "מופיע במאגר מאז" ("13.7.2026 או לפני" for complexes already in the first snapshot); and
  every change with its check date.
- **The notes:** both sources with their dates when they disagree. The line "בממוצע עוברות 4.0 שנים מאישור התכנית עד היתר ראשון
  (הרשות, 2025)" plus "זה ממוצע של מתחמים שכבר קיבלו היתר, ולא תחזית למתחם הזה" appears only for an approved plan before
  implementation (stage 3); in-implementation and after-licensing plans already have permits. Also the renumbering, and links to
  the plan on mavat, our project page (`/projects/<slug>/`, from the import) and the authority's map.
- **The figure:** an SVG timeline in RTL, a lane per stage and a column per snapshot, oldest on the right; up to 8 columns (then
  the first plus the last 7). A move up is a thick deep-sea segment, a step back or a removal is red, a stage that one source does
  not give is grey dashed. Text is 14 to 17 px in a 420-wide viewBox.
- **The table:** every complex of the city with its stage at the authority (the file's stage in brackets when they differ), units
  and its last change.
- **Moves view:** the count line as the answer, totals per kind, an SVG of what moved at each of the last four checks, and T8, the
  table of all changes (complex, city, what changed, from and to, check date), for all cities or one.
- **Honesty (7.8):** no start or occupancy year anywhere. The check date is on every change, and both sources are shown when they
  disagree. The formula line says how the comparison works and that the sources publish no start or occupancy dates.
- **Language:** no long dashes, none of the banned words (XPLAN's station "בבדיקה תכנונית" is shown as "בדיקה תכנונית"), the arrow
  ← in Hebrew labels and → in the number values (LTR).
- **Look:** the map page's tokens: ink #12202A, sea #2F6F86 for a point, deep #1F4B5C for a move up, line #D3DCE2 for the stage
  lanes, red #C42550 only for a step back or a removed complex. IBM Plex Sans Hebrew and IBM Plex Mono through the engine. One
  engine-wide note: Plex Mono has no Hebrew, so Hebrew in the big answer figure falls back to a system face, as in every engine tool.

## Tests and rendering

- `python tools/instruments/test_urtrack.py` gives 100 OK, 0 problems (it needs node; it reads the raw snapshots when they are on
  this machine).
- `python docs/research/2026-10-26-upgrades/ds_tools.py UrbanTracker` rebuilds `index.html`, then
  `python .../preview/urtrack/render_preview.py` renders it. At **390 and 1280 px**, 9 tool instances: every preset of every
  instance pressed (54 per width), both views, city, search (פתח תקווה, then גבעתיים, then a search with no result, then clearing
  it), the complex select, the table, copy ("הועתק"), WhatsApp (opens api.whatsapp.com with the text), print (stubbed, called once).
  Result: **no console errors or warnings, no sideways scroll** (also with every table open), nothing past the viewport outside a
  table scroller. Screenshots: `shot-p-*.png` (phone, the output column) and `shot-d-*.png` (desktop, the whole panel) for the
  default, approved with XPLAN, two sources and the moves view.

## Registry entry for `inc/instruments.php` (not applied)

Add it to the `nadlan_nli_tools()` array next to `gwall` and `t466`. Every related link was checked on 26.10.2026 and answers 200
with no redirect.

```php
			/* Q1 moat (local build 26.10.2026): "יומן המתחמים", the complex tracker of /urban-renewal/map/; renewal-track.json from the authority's map, the data.gov.il file, our import and XPLAN (tools/urban/build_renewal_track.py) */
			'urtrack' => array(
				'name' => 'יומן המתחמים: מה השלב של המתחם שלכם, ומה השתנה בו', 'cat' => 'ReferenceApplication', 'kicker' => 'יומן · התחדשות עירונית',
				'desc' => 'לכל מתחם התחדשות עירונית: השלב והמסלול אצל הרשות הממשלתית להתחדשות עירונית היום, השלב בקובץ data.gov.il ובייבוא שלנו, כמה דירות יש היום וכמה יהיו אחרי הבנייה והמכפיל, מספר התכנית ותאריכי ההפקדה והאישור, ממתי המתחם מופיע במאגר וכל שינוי שראינו בין הבדיקות עם תאריך הבדיקה. חיפוש לפי עיר, שם מתחם, רחוב או מספר תכנית, וטבלה של כל מה שזז במאגר.',
				'data' => array( 'renewal-track.json' ),
				'related' => array( '/urban-renewal/' => 'המדריך להתחדשות עירונית', '/urban-renewal/check/' => 'בדיקת בניין חינמית', '/urban-renewal/pinui-binui/' => 'פינוי בינוי', '/urban-renewal/tama-38/' => 'תמ״א 38 והחלופות', '/my-renewal/' => 'חדר פרויקט לנציגות' ),
			),
```

On the page: `[nadlan_tool id="urtrack"]` (it opens on כפר שלם), `[nadlan_tool id="urtrack" preset="moves"]` (it opens on "מה זז
במאגר", the right fit for section 5 of the 7.5 order), or `[nadlan_tool id="urtrack" city="ירושלים"]` (it opens on the city's newest
move). The shortcode passes only whitelisted keys, so opening on one complex (for a "מה השתנה" line on each of the 947 project pages)
needs `'cx'` and `'view'` added to the key list in the `nadlan_tool` shortcode. That is one line in `inc/instruments.php`, not done
here.

## Summary branch for `nadlan_nli_summary('urtrack')` (not applied)

The code is in `urtrack-summary.php`; paste the `if ( 'urtrack' === $id ) { ... }` block into `nadlan_nli_summary()`. It reads the
same JSON and prints the count line, the snapshots, today's map total, the honesty sentence and the T8 table. Checked here: `php -l`
(PHP 8.3) reports no syntax errors, and it was run against the real JSON with a stub `esc_html`. Output: 15.7 KB, 134 rows, the
same count line as the tool, no long dash, no banned word. It opens:

> מאז 15.8.2026 נוספו 36 מתחמים, 18 עלו שלב, 13 לא מופיעים עוד ו-1 קיבל מספר מתחם חדש (קובץ data.gov.il מול מפת הרשות של
> 25.10.2026). במפת הרשות היום 993 מתחמים. הבדיקות: הייבוא שלנו 13.7.2026, קובץ data.gov.il 15.8.2026, מפת הרשות 20.10.2026, מפת
> הרשות 25.10.2026. כל שינוי מתוארך לבדיקה הראשונה שבה ראינו אותו. אין כאן שנת התחלת בנייה או אכלוס: המקורות לא מפרסמים אותן.

followed by the table "מה זז במאגר: כל השינויים בין הבדיקות (134)", with columns מתחם · עיר · מה השתנה · משלב ← לשלב · תאריך הבדיקה,
newest check first.

## Weekly refresh

1. `python tools/urban/build_renewal_track.py`. It reads the file, the map and XPLAN (read only). Our import is read once only,
   since it is not being refreshed; `--site` re-reads it. A new snapshot is written only when a source changed (a new
   `last_modified`, a new map edit date, a new XPLAN day). The same version is never rewritten: re-running today printed
   "unchanged, kept" for all three. Then the JSON is rebuilt from every snapshot in the folder, so the history only grows.
   `--offline` rebuilds from the saved snapshots only.
2. `python tools/instruments/test_urtrack.py` must say PASS. The checks pinned to 970 / 999 / 947 follow `renewal-stats.json`. If
   that file is rebuilt on a newer map or file, update those few lines; every other check follows the data.
3. Rebuild the preview (`ds_tools.py UrbanTracker`, then `render_preview.py`) and look at it.
4. Ship through the normal release pipeline, with the owner's word. The data URL is cache-busted by the plugin version
   (`?ver=NADLAN_CONFIG_VERSION`), so a new JSON reaches readers only with a version bump. A weekly scheduled run (for example
   Sunday night, after the authority's weekend edits) can be set up on the owner's word; none was created.

## Open items and what I could not verify

- The tool is not on any page, and nothing above is applied (registry, summary, shortcode keys). The page's own hard-coded line in
  `inc/urban-map-data.php` ("נוספו 36 מתחמים ו-17 עלו שלב", 15.8 against 20.10) is now one check old: against 25.10 it is 36 and 18.
  It could read `agg` from this JSON; that file was not touched.
- `renewal-stats.json` (the page's tiles) still counts the 20.10.2026 map (999). The map had 1,000 rows on 25.10.2026.
  `build_renewal_stats.py` was not re-run.
- The 13.7.2026 date of our import comes from the posts' modified dates and research F11. 5 of the 947 posts were last written by
  an import on 1.6.2026 and 49 were edited on 28.8.2026 (titles); their stage is taken as it stands on the site.
- "Added between 13.7 and 15.8" assumes the 13.7 import read the whole file. It created 10 new posts that day and updated the rest,
  which supports that, but it is not proven row by row.
- The map layer's licence field is empty (research F9). The JSON carries stages, counts, names and plan numbers, which is fact
  reporting, and no geometry.
- Renumbering is detected by same city, same name and same snapshot. A renamed and renumbered complex at once would still show as
  one removal and one addition.
- XPLAN found no record for 316 of the 1,096 plan strings (mostly old local formats). Those complexes show no XPLAN lines.
