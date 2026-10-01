# Kikar Hamedina: place names in other languages from Wikidata labels, via OSM `wikidata` tags (HAD-375, 1.10.2026)

## What and why

The area map (`arealife/areamap.js`, `nameOf`: `names[LANG] || names.en ||` a name without Hebrew letters `||` the kind)
and the 3D world show a Hebrew-only place by its kind ("School", "Café") on the en/fr/ru/ar pages. Step 4
(`names_osm_kikar.py`) took the names from OSM's own `name:xx` tags. This step 5 adds a second source: many OSM features have
no `name:xx` tag but carry `wikidata=Q…`, and the Wikidata item's **label** is the real name in English, Arabic, French and
Russian. Nothing is translated or transliterated. Descriptions and aliases are never used. A value is the item's label, or
nothing.

The same run also audits the script of every existing `names` value (the coordinator's order, 1.10.2026). See
"Script audit" below.

## How to run (step 5 of the registry chain)

```
python scripts/project-stage/build_places.py kikar                         # 1
python docs/research/2026-09-30-kikar-hamedina/enrich_places_kikar.py      # 2-3
python docs/research/2026-09-30-kikar-hamedina/names_osm_kikar.py          # 4  (then names-osm/diff_check.py, proof of step 4)
python docs/research/2026-09-30-kikar-hamedina/names_wikidata_kikar.py     # 5  THIS (writes both copies)
python docs/research/2026-09-30-kikar-hamedina/names-wikidata/diff_check.py   # proof of step 5 against 89673407 (step 4's output)
python scripts/project-stage/build_world_hamedina.py                       # copies places.json byte for byte (a no-op)
```

Without `--fetch` the step reuses the saved Overpass and Wikidata answers, so it rebuilds offline to the same bytes. From
`89673407` (md5 `56c27127…`) it gives md5 **`3ba624cda17774df4b0fafbbb806548d`** (369,443 bytes). `--dry` on its own
output gives the same md5 and writes nothing, so the step is idempotent. `--fetch` asks Overpass and Wikidata again.

**Note:** `names-osm/diff_check.py` proves step 4 alone. Run on step 5's output, it now reports two expected
differences: the new `names_src` field on `tlv:745/125`, and the removed `names.en` of `fp:osm-way-283357822`. Use
`names-wikidata/diff_check.py` for step 5.

## The rule (never relaxed)

0. **Script audit** of every existing `names` value with `names_osm.lang_ok()`. A value with Hebrew letters inside
   `names.en/ru/fr/ar` plainly fails and is **removed**. If that empties the `names` object, the object goes too. Any
   other failure is only listed. Both kinds are recorded in `script-audit.csv`.
1. **Overpass**, one query (`overpass-query.overpassql`), the same bbox as step 4 (32.072869, 34.773155 to
   32.100415, 34.806300). It fetches every node, way and relation with a `wikidata` tag **or** one of
   `name:en/ar/ru/fr`, **and** a `name` or a `name:he`, using `out tags center`. This is a superset of step 4's query, so
   candidates and ambiguity are counted over every feature either step can see. OSM base 2026-10-01T06:50:05Z,
   3,031 elements. 2,902 have a Hebrew key, and 327 of those carry `wikidata`.
2. **Targets**: every non-generic place whose `name` has Hebrew letters and that still lacks at least one of
   `names.en/ar/fr/ru`.
3. **The place's own feature**, under step 4's strict rule. `strict()`, `never()`, `own_osm_ref()`, `norm()`,
   `meters()`, `lang_ok()` and `with_names()` are imported from `names_osm_kikar.py`, not copied.
   - **(A)** The place id carries an OSM element (`osm:way/N`, `fp:osm-node-N` …) and that element is in the answer. It is
     the feature, and `strict()` must give rule (a). NEVER still wins over (a).
   - **(B)** Otherwise, exactly one feature with the same Hebrew name (`norm()`) within 80 m. The count covers all
     same-name features, before the strict rule. `strict()` must give (a) or (b).
4. The feature must carry a well-formed `wikidata=Q<digits>`. `wbgetentities` (`props=labels|sitelinks`,
   `languages=en|ar|fr|ru|he`, no language fallback, 50 ids per call) is asked once. The raw answers are in `wikidata/`.
5. **Identity guard**: the item's Hebrew label, or its hewiki sitelink title, must equal the place's name after `norm()`.
   If the item has neither, the OSM feature's own `name`/`name:he` must equal the place's name. Otherwise the place is
   skipped (`he-mismatch`).
6. **Script check** on each label: `ar` Arabic, `ru` Cyrillic, `en`/`fr` Latin, and no letters of the other scripts.
7. Only missing languages are written. An existing value is never overwritten; a differing one is kept and listed.
   Each added value gets `names_src[lang] = "wikidata:Q…"`. `names_src` sits right after `names`, and only added
   values have an entry.

## Counts

**Targets: 1,020** (401 within a 10-minute walk). 729 of them lack `en`, 984 lack `ru`, 1,019 lack `fr` and 988 lack `ar`.

| group | targets |
|---|---|
| essentials | 297 |
| food | 247 |
| outdoors | 170 |
| education | 152 |
| community | 82 |
| health | 41 |
| transport | 31 |

**Filled: 1 place, 1 value.** The group is community, with en 1, ru 0, fr 0, ar 0. The place is `tlv:745/125`
צוותא (walk 20 min), filled with `en` "Tzavta" from `wikidata:Q12410852`. Its source feature is node/12101869647
`amenity=theatre`, at 29.0 m, under rule (b). That node has no `name:en` tag, so step 4 could not see it.

**Skipped, by reason (1,019 rows; one row per target place):**

| reason | places | of which within 10 min |
|---|---|---|
| no same-name feature within 80 m (in the union answer) | 725 | 300 |
| the feature has no `wikidata` tag (208 of them are the place's own element) | 232 | 74 |
| rejected by the strict rule (6 of them carry `wikidata`) | 24 | 12 |
| identity guard: the item's Hebrew label/hewiki differs from the place's name | 17 | 5 |
| ambiguous (2+ same-name features within 80 m) | 11 | 5 |
| matched, but the item has no label in a missing language | 10 | 5 |
| values dropped by the script check | 0 | |
| existing values kept although Wikidata differs | 5 values | |

The ten `matched-nothing-new` items have only an `en` label, and these places already have `en`. For example, גן הגת is
"Gan HaGat" and בית הכנסת היכל יהודה is "Hechal Yehuda Synagogue". Wikidata has no ru/fr/ar label for any of them.

After the step, these places are still shown by their kind on a language page (no `names[lang]` and no `names.en`):

| | en | ru | fr | ar |
|---|---|---|---|---|
| within 10 min | 304 | 303 | 304 | 304 |
| whole file | 728 | 727 | 728 | 728 |

The whole-file count rises by one compared with step 4, because "צמרת G" lost its Hebrew `en` value. Before, every
language page showed it in Hebrew.

## 10 examples: 1 written, 9 refused by the identity guard (NOT written, listed for the record)

| | Hebrew name (place) | Wikidata item and its Hebrew label | en label | ar label | outcome |
|---|---|---|---|---|---|
| 1 | צוותא (`tlv:745/125`) | Q12410852 צוותא | Tzavta | (none) | **written: en** |
| 2 | הגימנסיה העברית הרצליה | Q1592883 הגימנסיה העברית "הרצליה" | Herzliya Hebrew Gymnasium | ثانوية هرتسليا العبرية | refused: quotation marks differ |
| 3 | מועדון השייטים תל-אביב | Q7695561 מועדון השייטים תל אביב | Tel Aviv Rowing Club | (none) | refused: hyphen vs space |
| 4 | הלונדון מיניסטורס | Q7214716 לונדון מיניסטורס | London Ministore Tower | (none) | refused: the article ה |
| 5 | בי"ח איכילוב | Q2561450 המרכז הרפואי תל אביב ע"ש סוראסקי | Tel Aviv Sourasky Medical Center | مركز تل أبيب سوراسكي الطبي | refused: other name |
| 6 | תל אביב סבידור מרכז | Q2915697 תחנת הרכבת תל אביב – סבידור מרכז | Tel Aviv – Savidor Central railway station | محطة قطار تل أبيب – سفيدور مركز | refused |
| 7 | אבא הלל (×2 places) | Q25494925 תחנת אבא הלל | Abba Hillel Light Rail Station | (none) | refused: "תחנת" prefix |
| 8 | ספריית שער ציון – בית אריאלה / בית אריאלה | Q4263244 ספריית בית אריאלה | Beit Ariela | مكتبة شعار تسيون- بيت اريئيلا | refused |
| 9 | גן הפסלים ע"ש לולה אבנר | Q139575 גן הפסלים ע"ש לולה בר-אבנר | Lola Beer Ebner Sculpture Garden | (none) | refused |
| 10 | זמנהוף (a pharmacy) | Q7027396 מרפאת זמנהוף | Zamenhof Clinic | (none) | refused, and rightly: the item is the clinic, not the pharmacy |

All 17 refusals are listed in `stats.json` (`he_mismatch_list`) and in `matches.csv`. They also include the light-rail
stations (Arlozorov, Shaul HaMelech), גן העיר, the Scouts tribe, עירוני ד', and a Yarkon edge point.

**Kept, not overwritten (5):** these existing `en` values differ from Wikidata's label, and only the existing value was
kept: גן סוטין "Soutine garden" (Wikidata "Park Soutine"), גן וולובלסקי קרני "Volovelski Karni" ("Volovelski-Karni
Garden"), כיכר היל "Kikar Hill" ("Abattoir Hill"), גינת דובנוב "Dubnov" ("Dubnow Park"), גן הבנים "Gan HaBanim" ("Gan
Habanim").

**Rejected by the strict rule although the feature has `wikidata` (6):**
- גימנסיה הרצליה `fp:961-45`: a school feature, but the place is filed under community;
- בית שלום עליכם (Q2906196) and המשכן לאמנויות הבמה (Q555356): both are `building=yes` with no POI tags;
- ככר מסריק ×2 (Q2776314): `place=square`;
- בבלי (Q2919369): `place=suburb`.

## Script audit of the existing names (all 442 values, before this step's additions)

| place id | name | group | lang | value | why | action |
|---|---|---|---|---|---|---|
| `fp:osm-way-283357822` | צמרת G | essentials | en | `צמרת G` (old value, kept here) | contains Hebrew letters | **removed** (it was the place's only `names` value, so the `names` object went too) |

No other value fails: 0 values were listed only. There is no `ar` value with Latin letters, no `ru` value without
Cyrillic, and so on.

**Cause:** `scripts/project-stage/build_places.py` lines 384-385 copy an OSM `name` into `names.en` when it contains any
Latin letter, and OSM way/283357822 is named "צמרת G". A rebuild of the chain brings the value back in step 1, and this
step removes it again. The builder is shared with the other projects and was not changed. The **DUO** registry
(`assets/project-stage/duo/places.json`) carries the same bad value. It was not touched, since it is outside this step.

## Second source: Tel Aviv-Yafo municipal GIS (`gisn.tel-aviv.gov.il`, IView2): no usable English field

`tlv-gis-check.json` holds the layer metadata and the counts. The education layers (769 schools, 768 kindergartens, 624
daycares), the community layer (553) and the synagogues layer (568) have **no** English name field. The culture layer
(745) has `NAME_ENG` (alias "שם באנגלית"), but it is **empty in all 136 records city-wide** (0 not null, 0 not empty).
Nothing was taken from the city's GIS. (`enrich_places_kikar.py` already reads `NAME_ENG` for layer 745, and it never
fired.)

## Not used: `brand:wikidata` (measured, outside the brief)

A scratch probe (not saved, nothing written) counted what `brand:wikidata` would add under the same rules: 61 matched
targets across 27 brands, 35 of which pass the Hebrew guard. They would give en 0, ru 5, fr 23 and ar 15. The labels are
chains' legal names, such as "Bank Hapoalim B.M.", "Shufersal Ltd." and "Mizrahi Tefahot Bank Ltd.", not the branch's
name. Using them is the owner's call.

## Things to check

1. The yield is small: 1 value. Wikidata has items for few local places, and those items seldom have ru/fr/ar labels.
2. Wikidata labels can be wrong even when the Hebrew label matches. כיכר היל has the `en` label "Abattoir Hill" (it was
   kept out only because the place already had `en`). The guard proves the item's identity, not the quality of its
   labels. "Tzavta" (the written value) was read by eye: it is the theatre's own name.
3. Path (A) trusts the id's OSM element. One id, `osm:relation/16022802#n` (a Yarkon edge point), resolves to the whole
   park relation 2.1 km away. The identity guard refused it.
4. The 17 refusals are near-identical names (quotes, hyphen, ה, a "תחנת" prefix). Accepting them would need the owner's
   word; the brief says never to relax the guard.

## Files

- `../names_wikidata_kikar.py`: the step.
- `overpass.json`: the raw Overpass answer (1,352,870 bytes, sha256 in `fetch-meta.json`).
- `overpass-query.overpassql` and `fetch-meta.json`: the query and its metadata.
- `wikidata/batch-01.json`: the raw `wbgetentities` answer (26 ids). `wikidata/fetch-meta.json` holds the URL, the ids,
  the sha256 and the time.
- `matches.csv`: one row per target (1,020). It shows the path (A/B), the status, the OSM feature, the rule, the
  distance, the Wikidata id, the Hebrew label and hewiki title, the guard result, the four labels, what was written,
  what was kept, and the ambiguous candidates.
- `script-audit.csv`: every existing names value that failed the script check, with its action.
- `stats.json`: the counts above, with the lists.
- `tlv-gis-check.json`: the municipal GIS field check.
- `diff_check.py`: the proof. It shows only the listed removal and the traced additions, and nothing else.

OSM data © OpenStreetMap contributors, ODbL. Wikidata labels: CC0.
