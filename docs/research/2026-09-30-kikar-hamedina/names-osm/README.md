# Kikar Hamedina: place names in other languages, from OpenStreetMap only (HAD-375, 1.10.2026)

## Why

On the en/fr/ru/ar pages the area map and its list (`arealife/areamap.js`, `nameOf`: `names[LANG] || names.en ||` a name
without Hebrew letters `||` the kind) and the 3D world (`world.js`, `placeName`) show a place whose name exists only in
Hebrew by its kind ("School", "مدرسة", "Café"). This step gives such places their names in other languages. It uses only
OpenStreetMap tags. Nothing is translated, transliterated or invented.

## How to run it (it is step 4 of the registry chain)

```
python scripts/project-stage/build_places.py kikar             # 1. findplace + OSM + walk + sight
python docs/research/2026-09-30-kikar-hamedina/enrich_places_kikar.py   # 2-3. city layers, bus lines, rail, Yarkon
python docs/research/2026-09-30-kikar-hamedina/names_osm_kikar.py       # 4. THIS: names from OSM (writes both copies)
python scripts/project-stage/build_world_hamedina.py           # world.json; its copy of places.json is now a no-op
python docs/research/2026-09-30-kikar-hamedina/names-osm/diff_check.py  # proof: nothing but "names" changed
```

`names_osm_kikar.py` reuses the saved Overpass answer (`overpass.json`), so the output can be rebuilt offline to the same
bytes (two runs from the committed file both gave md5 `0b7da14298c37f1b4e4f37f90ebf8ce5`). `--fetch` asks Overpass again.
`--no-streets` is the stricter reading described under "Things to check" below. It is not used for the committed file.

## Method

1. **Overpass**, one query (`overpass-query.overpassql`), bbox = the places' lat/lng min/max ± 0.001°
   (32.072869, 34.773155 to 32.100415, 34.806300). It fetches every node, way and relation that has at least one of
   `name:en`/`name:ar`/`name:ru`/`name:fr` and also has a `name` or a `name:he`, using `out tags center`. The
   Hebrew-letter check on `name` runs in the script, not in Overpass. Endpoint: overpass-api.de, User-Agent
   `nadlan-config/2.0 (nad-lan.co.il)`, OSM base 2026-09-30T22:08:25Z. Fetch details are in `fetch-meta.json` (sha256
   of the raw answer). The answer has 3,017 elements. 2,892 of them have a Hebrew name plus another language.
2. **Targets**: every non-generic place whose name has Hebrew letters (the same range as `hasHe`, U+0590-U+05FF) and that
   has no `names.en`. There are 758 in the file, 316 of them within a 10-minute walk (`walk <= 10`).
3. **A match needs all of these**:
   - the Hebrew name is identical to the feature's `name` or `name:he` after normalising. Normalising means: NFC,
     removing direction marks, treating the geresh variants `׳ ' ’ ‘` as one, and the gershayim variants `״ " “ ”`
     and `''` as one, treating the hyphen variants `- – — ־` as one (with the spaces around them dropped), and
     collapsing whitespace;
   - the distance is ≤ 80 m (haversine, measured to the node or to the way's or relation's centre);
   - exactly one feature qualifies. With two or more, the place is skipped and listed below.
4. **Language check** for every value: `ar` needs Arabic letters, `ru` Cyrillic, `en`/`fr` Latin. A value must also
   have no Hebrew characters (the `hasHe` range) and no letters from the other scripts. A value that fails is dropped.
5. **Writing**: only the missing languages are added. Existing values are never overwritten. A new `names` object goes
   right before `sight`, which is where the builders' twin merge leaves it. Languages are written in the builders'
   order: en, ru, fr, ar. Both copies are written with the same bytes: `docs/research/2026-09-30-kikar-hamedina/places.json`
   and `plugins/nadlan-config/assets/project-stage/hamedina/places.json`. They are compact JSON (`ensure_ascii=False`,
   `separators=(",", ":")`) with one final LF, the same serialisation as the builders.

## Results

| | count |
|---|---|
| target places (Hebrew-only, no names.en) | 758 (316 within 10 min) |
| matched (one feature, same name, ≤ 80 m) | 51 |
| places given names | **50** (24 within 10 min) |
| values written | **63**: **en 50, ru 8, fr 1, ar 4** |
| matched but nothing new (the place already had that OSM value) | 1 (`osm:node/12946222126`, ru only) |
| ambiguous, skipped | 9 |
| no feature with the same name within 80 m | 698 |
| values dropped by the language check (among matched features) | 0 |
| existing values kept although OSM differs | 0 |
| Hebrew-only places left within 10 min (no names.en) | **292** (was 316) |
| shown by their kind on a language page, within 10 min | en 292, fr 292, ar 292, ru 291 |
| the same, whole file | en 708, fr 708, ar 708, ru 707 |

- 23 of the 50 matches are the place's own OSM element: the place id carries the same OSM id (`fp:osm-node-…` /
  `osm:…`), so this is the strongest evidence.
- 11 of the 50 took the name of a **street or a neighbourhood** with the same name (see "Things to check").
- Two OSM features each name two places: way/370074343 (בית יד לבנים, `fp:553-27` and `fp:745-9`) and way/31539798
  (the street אהבת ציון, `fp:area-35` and `fp:961-26`).
- The language check is active. Over the whole Overpass answer it rejects 8 of 4,739 values, none of which belonged to
  a matched feature: `name:en` "1235" (4 ways), Arabic platform names with the Latin letters A/B/C (3 nodes), and
  "Tel Aviv Magistrate׳s Court", which contains a Hebrew geresh.
- `diff_check.py`: 1,245 places compared, 50 places with names added, 63 values added, **0 differences outside `names`**.
  All top-level fields are byte-identical, and so is the key order.

### 20 sample matches (sorted by walking minutes)

| walk | place id | Hebrew name | OSM feature | kind | m | written |
|---|---|---|---|---|---|---|
| 1 | fp:osm-node-11176806151 | אנטילופ | node/11176806151 | shop=clothes | 0.3 | en: Antelope |
| 1 | fp:osm-node-11176829810 | לוטו | node/11176829810 | shop=kiosk | 0.6 | en: Lotto |
| 1 | fp:osm-node-11176831454 | עודד קאשי | node/11176831454 | shop=jewelry | 0.4 | en: Oded Kashi |
| 2 | fp:osm-node-11361510170 | גולדה | node/11361510170 | amenity=ice_cream | 0.2 | en: Golda; ru: Голда |
| 3 | fp:7710 | בית החייל | way/102210229 | building=yes | 25.3 | en: Bet HaHayal |
| 3 | fp:osm-node-6815510153 | תיאטרון תל אביב | node/6815510153 | amenity=theatre | 0.5 | en: Tel-Aviv Theater |
| 4 | tlv:564/85 | בארי | way/629173641 | highway=residential (street) | 68.7 | en: Beeri; ru: Беэри; ar: بئيري |
| 5 | fp:696-390 | בילטמור | way/30879167 | highway=residential (street) | 66.2 | en: Biltmore |
| 5 | fp:area-35 | אהבת ציון | way/31539798 | highway=residential (street) | 78.4 | en: Ahavat Tsiyon; ru: Ахават Ционе |
| 5 | fp:961-26 | אהבת ציון | way/31539798 | highway=residential (street) | 68.4 | en: Ahavat Tsiyon; ru: Ахават Ционе |
| 5 | gtfs:20348 | דרך נמיר/ז'בוטינסקי | node/1803011220 | public_transport=platform | 0.0 | en: Namir Road/Jabotinsky; ar: طريق نمير/جابوتينسكي |
| 6 | fp:961-45 | גימנסיה הרצליה | way/405360284 | amenity=school | 8.9 | en: Herzliya Hebrew "Gymnasium"; ru: Еврейская Гимназия «Герцлия» |
| 7 | fp:osm-way-219292804 | בית הכנסת היכל יהודה | way/219292804 | amenity=place_of_worship | 0.2 | en: Hechal Yehuda Synagogue |
| 7 | fp:21635 | דידי דג | node/11364155969 | shop=fishing | 1.7 | en: Didi Dag |
| 8 | gtfs:24068 | ת. רכבת תל אביב - סבידור/דרך נמיר | node/1803055865 | public_transport=platform | 0.0 | en: Tel Aviv Train Station Savidor/Namir Road; ar: محطة قطار تل أبيب سفيدور/طريق نمير |
| 8 | fp:553-27 | בית יד לבנים | way/370074343 | building=public | 14.1 | en: Yad Labanim |
| 8 | fp:745-9 | בית יד לבנים | way/370074343 | building=public | 6.4 | en: Yad Labanim |
| 8 | gtfs:21534 | תיכון חדש רבין/דרך נמיר | node/1803094010 | public_transport=platform | 0.0 | en: Hadash Rabin High School/Namir Road; ar: ثانوية حداش رابين/طريق نَمير |
| 8 | fp:563-38 | מגדל המאה | way/539793996 | building=yes | 34.3 | en: Century Tower |
| 9 | fp:osm-way-1183060379 | עירוני י"א | way/1183060379 | amenity=school | 0.5 | en: Ironi Yud Alef |

All 51 matched rows are in `matches.csv` (status `matched`), with the tags read and the values written.

### Ambiguous (two features qualify), skipped

| walk | place id | Hebrew name | candidates |
|---|---|---|---|
| 6 | gtfs:25903 | ארלוזורוב/דרך נמיר | node/1802991844 0.0 m and node/1802991842 31.0 m: the two platforms of the stop, same en/ar |
| 6 | gtfs:21815 | ביה''ח איכילוב/ויצמן | node/1802994421 0.0 m and node/1802994419 27.1 m: the two platforms, same en/ar |
| 8 | fp:696-56 | אלעזר החורני | two ways of the street, 24.0 m and 78.7 m, same en |
| 11 | tlv:769/616 | הנרייטה סולד | two ways of the street, 37.8 m and 50.0 m, same en/ru |
| 12 | fp:564-121 | בזל | street way/26149505 32.4 m (en/ar/ru) and parking node/331186813 61.5 m (en only), en the same |
| 13 | fp:563-2 | השל"ה | two ways of the street, 39.9 m and 53.8 m, same en |
| 14 | fp:586-105 | גשר בר יהודה | path way/188963006 41.5 m (en) and bridge way/1232794551 41.9 m (en/ar/ru), en the same |
| 18 | fp:553-22 | בבלי | suburb way/803479640 54.6 m (en/ru/fr) and street way/30826559 74.4 m (en), en the same |
| 18 | fp:564-60 | ארלוזורוב | two ways of the street, 29.1 m and 61.5 m, same en/ar/ru |

None of the nine has conflicting values: the candidates are either one object split in OSM or share the same `en`.
If the rule "unique" were relaxed to "unique, or every candidate carries the same value", these nine would be filled.
That would include the two busy bus stops at a 6-minute walk. The rule was applied as written.

### Near misses (for the record, never written)

- 32 target places have a feature with the same name, but farther than 80 m. Some examples: כיכר המדינה
  (`fp:30020`, the square way at 104 m), בית יד לבנים (`fp:586-60`, 114 m), יהודה המכבי (94 m, 141 m),
  גן העיר (137 m, 251 m), ספורטק צפון (`fp:943-364`, 85 m).
- 64 have a feature within 80 m whose name contains ours or is contained in it. Identity is required, so these were not
  used. Column `near_miss` in `matches.csv` shows each one.

## Things to check

1. **11 places took the name of a street or a neighbourhood, not the place's own feature.** The city's layers sometimes
   name a place by its street: a pharmacy "בארי" at Be'eri 27, a playground "בילטמור", a daycare "בובליק", a Clalit
   clinic "בבלי". The matching street way, or the Bavli suburb, has the same Hebrew name within 80 m, and all the rules
   hold. The written value (for example "Beeri", "Biltmore", "Bavli") is the same label in the other language, but it
   comes from a different OSM object. 6 of the 11 are within 10 minutes: בארי, בילטמור, אהבת ציון ×2, הר נבו
   (a state elementary school at הר נבו 4), and אריסטובולוס. The full list is in `matches.csv` (column
   `street_or_area` = yes).
   `--no-streets` leaves streets and named areas out (a feature that is also an amenity, park, building etc. counts as
   the thing). It gives 41 places (18 within 10 min) and md5 `9f390d6e9bfcb94c331fa0465dfb6523`. In that mode two
   ambiguous places become single matches: בזל, a clinic, would take "Basel" from a **parking lot**, and
   גשר בר יהודה would take the bridge's en/ru/ar.
2. **OSM itself carries some wrong pairs.** Two examples, both farther than 80 m and so unused: the street way/31539799
   is named אהבת ציון in Hebrew and "HaShofet Nofech" in English, and "נקודת טבע" has the English name
   "Future Cosmetics Boutique". The rules cannot catch a wrong `name:en` on the one matched feature. All 63 written values
   were read by eye and each one is the same name as the Hebrew. Two look odd but come from OSM as they are: the English
   of the gymnasium has stray quotes (Herzliya Hebrew "Gymnasium"), and the Russian of Ahavat Zion reads "Ахават Ционе".
3. **The file does carry OSM ids.** 519 place ids name an OSM element: 229 `osm:node/…`, 113 `osm:way/…`, 3 `osm:relation/…`,
   135 `fp:osm-node-…` and 39 `fp:osm-way-…`. They are used here only as evidence (column `same_osm_id`), never as a
   match on their own.
4. **Place ids are not unique** in this file. 21 ids appear more than once: 58 rows in all, one id up to 6 times, and
   for example `fp:27581` and `fp:13730` twice each. This was already true before this step. `diff_check.py` therefore
   compares places by position.
5. **Line endings:** this clone has `core.autocrlf=true` and no `.gitattributes`. A fresh checkout writes CRLF, which
   changes the md5. The committed blob and the working file are LF (md5 `0b7da142…`). To get the exact bytes back, use
   `git cat-file blob HEAD:<path>`, not `git checkout`.

## Files

- `overpass.json`: the raw Overpass answer (1,345,962 bytes).
- `overpass-query.overpassql`: the query.
- `fetch-meta.json`: endpoint, time, User-Agent, bbox, sha256, OSM base.
- `matches.csv`: one row per target place (758). Status is `matched` / `matched-nothing-new` / `ambiguous` / `no-match`.
  Each row has the OSM feature, its kind, the distance, whether it is the place's own OSM id, the four tags read, what
  was written, what was dropped, and the near miss.
- `stats.json`: the counts above.
- `diff_check.py`: the proof that only `names` changed.

OSM data © OpenStreetMap contributors, ODbL.
