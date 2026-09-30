# Kikar Hamedina: place names in other languages, from OpenStreetMap only (HAD-375, 1.10.2026)

## Why

On the en/fr/ru/ar pages the area map and its list (`arealife/areamap.js`, `nameOf`: `names[LANG] || names.en ||` a name
without Hebrew letters `||` the kind) and the 3D world (`world.js`, `placeName`) show a place whose name exists only in
Hebrew by its kind ("School", "مدرسة", "Café"). This step gives such places their names in other languages. It uses only
OpenStreetMap tags, and only the tags of the place's **own** feature (the owner's law: no invented facts). Nothing is
translated, transliterated or invented.

## How to run it (it is step 4 of the registry chain)

```
python scripts/project-stage/build_places.py kikar             # 1. findplace + OSM + walk + sight
python docs/research/2026-09-30-kikar-hamedina/enrich_places_kikar.py   # 2-3. city layers, bus lines, rail, Yarkon
python docs/research/2026-09-30-kikar-hamedina/names_osm_kikar.py       # 4. THIS: names from OSM (writes both copies)
python scripts/project-stage/build_world_hamedina.py           # world.json; its copy of places.json is now a no-op
python docs/research/2026-09-30-kikar-hamedina/names-osm/diff_check.py  # proof against e6861c65: nothing but "names" changed
```

`names_osm_kikar.py` reuses the saved Overpass answer (`overpass.json`), so the output can be rebuilt offline to the same
bytes. A clean rebuild from `e6861c65` gives md5 `56c271272cb8a080df9b347807f1a2c1`, and running the step again on its
own output changes nothing. `--fetch` asks Overpass again.

## Method

1. **Overpass**, one query (`overpass-query.overpassql`), bbox = the places' lat/lng min/max ± 0.001°
   (32.072869, 34.773155 to 32.100415, 34.806300). It fetches every node, way and relation that has at least one of
   `name:en`/`name:ar`/`name:ru`/`name:fr` and also has a `name` or a `name:he`, using `out tags center`. The
   Hebrew-letter check on `name` runs in the script, not in Overpass. Endpoint: overpass-api.de, User-Agent
   `nadlan-config/2.0 (nad-lan.co.il)`, OSM base 2026-09-30T22:08:25Z. Fetch details are in `fetch-meta.json` (sha256
   of the raw answer). The answer has 3,017 elements. 2,892 of them have a Hebrew name plus another language.
2. **Targets**: every non-generic place whose name has Hebrew letters (the same range as `hasHe`, U+0590-U+05FF) and that
   has no `names.en`. There are 758 in the file, 316 of them within a 10-minute walk (`walk <= 10`).
3. **Same name, near, unique.** A feature is a candidate when all of these hold:
   - the Hebrew name is identical to the feature's `name` or `name:he` after normalising. Normalising means: NFC,
     removing direction marks, treating the geresh variants `׳ ' ’ ‘` as one, and the gershayim variants `״ " “ ”`
     and `''` as one, treating the hyphen variants `- – — ־` as one (with the spaces around them dropped), and
     collapsing whitespace;
   - the distance is ≤ 80 m (haversine, measured to the node or to the way's or relation's centre).

   Exactly one candidate is required. With two or more, the place is skipped as ambiguous. The count covers **all**
   same-name features, before the strict rule, so a street next to a shop of the same name still makes the place
   ambiguous.
4. **The strict rule** is then applied to that one feature:
   - **NEVER** take a name from `highway=*` (a bus stop excepted), `amenity=parking`, `place=*`, `landuse=*`,
     `boundary=*`, or a building with no POI tags. This is checked first and wins even over (a).
   - **(a)** the place id carries the element's OSM id (`osm:node/N`, `fp:osm-node-N`, `fp:osm-way-N` ...), **or**
   - **(b)** the feature is a POI (`amenity`, `shop`, `leisure`, `tourism`, `office`, `healthcare`, a railway station, a
     `public_transport` platform or a bus stop) whose kind fits the place's group (`COMPAT` in the script):
     - education: school, college, university, kindergarten, childcare, library;
     - food: cafe, restaurant, fast_food, bar, pub, ice_cream, and bakery-type shops;
     - transport: bus_stop, platform, station, railway station/halt/tram_stop;
     - health: clinic, doctors, hospital, pharmacy, dentist, `healthcare=*`;
     - essentials: any shop, plus pharmacy, bank, atm, post_office;
     - outdoors: park, playground, garden, pitch, sports and fitness centres, pool, dog_park, stadium;
     - community: community_centre, place_of_worship, theatre, arts_centre, cinema, library, museum, gallery, NGO offices.

   Otherwise the match is rejected and listed below.
5. **Language check** for every value: `ar` needs Arabic letters, `ru` Cyrillic, `en`/`fr` Latin. A value must also
   have no Hebrew characters (the `hasHe` range) and no letters from the other scripts. A value that fails is dropped.
6. **Writing**: only the missing languages are added. Existing values are never overwritten. A new `names` object goes
   right before `sight`, which is where the builders' twin merge leaves it. Languages are written in the builders'
   order: en, ru, fr, ar. Both copies are written with the same bytes: `docs/research/2026-09-30-kikar-hamedina/places.json`
   and `plugins/nadlan-config/assets/project-stage/hamedina/places.json`. They are compact JSON (`ensure_ascii=False`,
   `separators=(",", ":")`) with one final LF, the same serialisation as the builders.

## Results (strict rule)

| | count |
|---|---|
| target places (Hebrew-only, no names.en) | 758 (316 within 10 min) |
| one same-name feature within 80 m | 51 |
| rejected by the strict rule | 20 (list below) |
| kept | 31: 23 by (a) own OSM element, 8 by (b) compatible POI |
| places given names | **30** (**12 within 10 min**) |
| values written | **36**: **en 30, ru 3, fr 0, ar 3** |
| kept but nothing new (the place already had that OSM value) | 1 (`osm:node/12946222126`, ru only) |
| ambiguous, skipped | 9 |
| no feature with the same name within 80 m | 698 |
| values dropped by the language check (among kept features) | 0 |
| existing values kept although OSM differs | 0 |
| Hebrew-only places left within 10 min (no names.en) | **304** (was 316) |
| shown by their kind on a language page, within 10 min | en 304, fr 304, ar 304, ru 303 |
| the same, whole file | en 728, fr 728, ar 728, ru 727 |

- 22 of the 30 named places are the place's own OSM element (rule a). The other 8 are compatible POIs (rule b): three
  bus platforms at 0.0 m, דידי דג (shop, 1.7 m), סופר בבלי (supermarket, 2.6 m), ארומה (cafe, 21.1 m), בית אריאלה
  (library, 16.3 m) and מכללת שנקר (college, 40.6 m).
- The language check is active. Over the whole Overpass answer it rejects 8 of 4,739 values, none of which belonged to
  a kept feature: `name:en` "1235" (4 ways), Arabic platform names with the Latin letters A/B/C (3 nodes), and
  "Tel Aviv Magistrate׳s Court", which contains a Hebrew geresh.
- `diff_check.py` (against `e6861c65`): 1,245 places compared, 30 places with names added, 36 values added,
  **0 differences outside `names`**. All top-level fields are byte-identical, and so is the key order.

### 20 sample matches (sorted by walking minutes)

| walk | place id | Hebrew name | OSM feature | kind | rule | m | written |
|---|---|---|---|---|---|---|---|
| 1 | fp:osm-node-11176806151 | אנטילופ | node/11176806151 | shop=clothes | a | 0.3 | en: Antelope |
| 1 | fp:osm-node-11176829810 | לוטו | node/11176829810 | shop=kiosk | a | 0.6 | en: Lotto |
| 1 | fp:osm-node-11176831454 | עודד קאשי | node/11176831454 | shop=jewelry | a | 0.4 | en: Oded Kashi |
| 2 | fp:osm-node-11361510170 | גולדה | node/11361510170 | amenity=ice_cream | a | 0.2 | en: Golda; ru: Голда |
| 3 | fp:osm-node-6815510153 | תיאטרון תל אביב | node/6815510153 | amenity=theatre | a | 0.5 | en: Tel-Aviv Theater |
| 5 | gtfs:20348 | דרך נמיר/ז'בוטינסקי | node/1803011220 | public_transport=platform | b | 0.0 | en: Namir Road/Jabotinsky; ar: طريق نمير/جابوتينسكي |
| 7 | fp:osm-way-219292804 | בית הכנסת היכל יהודה | way/219292804 | amenity=place_of_worship | a | 0.2 | en: Hechal Yehuda Synagogue |
| 7 | fp:21635 | דידי דג | node/11364155969 | shop=fishing | b | 1.7 | en: Didi Dag |
| 8 | gtfs:24068 | ת. רכבת תל אביב - סבידור/דרך נמיר | node/1803055865 | public_transport=platform | b | 0.0 | en: Tel Aviv Train Station Savidor/Namir Road; ar: محطة قطار تل أبيب سفيدور/طريق نمير |
| 8 | gtfs:21534 | תיכון חדש רבין/דרך נמיר | node/1803094010 | public_transport=platform | b | 0.0 | en: Hadash Rabin High School/Namir Road; ar: ثانوية حداش رابين/طريق نَمير |
| 9 | fp:osm-way-1183060379 | עירוני י"א | way/1183060379 | amenity=school | a | 0.5 | en: Ironi Yud Alef |
| 9 | fp:osm-node-1717768353 | זוריק | node/1717768353 | amenity=cafe | a | 0.4 | en: Zorik |
| 11 | fp:osm-node-1309308450 | לגבר | node/1309308450 | shop=gift | a | 0.5 | en: LaGever |
| 11 | fp:osm-node-1309308429 | צומת ספרים | node/1309308429 | shop=books | a | 0.5 | en: Tzomet Sfarim |
| 11 | fp:osm-node-10923421862 | גוד פארם | node/10923421862 | amenity=pharmacy | a | 0.2 | en: GOOD PHARM |
| 11 | fp:osm-way-149276659 | עטרת צבי | way/149276659 | amenity=place_of_worship | a | 0.5 | en: Ateret Tsvi |
| 11 | fp:osm-way-104701145 | שבט החורש | way/104701145 | amenity=community_centre | a | 0.1 | en: HaHoresh Scouts |
| 12 | fp:osm-way-98573563 | בני עקיבא | way/98573563 | amenity=community_centre | a | 0.5 | en: Bnei Akiva |
| 13 | fp:osm-node-2488604193 | שופרסל | node/2488604193 | shop=supermarket | a | 0.5 | en: Shufersal; ru: Шуферсаль |
| 13 | fp:osm-way-30781000 | גן מלץ | way/30781000 | leisure=park | a | 0.1 | en: The Maltz Park |

All 31 kept rows are in `matches.csv` (status `matched` or `matched-nothing-new`, column `rule`).

### Rejected by the strict rule (20): nothing written

| walk | place id (g/k) | Hebrew name | OSM feature | m | would have written | why rejected |
|---|---|---|---|---|---|---|
| 3 | fp:7710 (food/cafe) | בית החייל | way/102210229 | 25.3 | en: Bet HaHayal | never: building=yes with no POI tags |
| 4 | tlv:564/85 (essentials/pharmacy) | בארי | way/629173641 | 68.7 | en: Beeri; ru: Беэри; ar: بئيري | never: highway=residential |
| 5 | fp:696-390 (outdoors/park) | בילטמור | way/30879167 | 66.2 | en: Biltmore | never: highway=residential |
| 5 | fp:area-35 (outdoors/park) | אהבת ציון | way/31539798 | 78.4 | en: Ahavat Tsiyon; ru: Ахават Ционе | never: highway=residential |
| 5 | fp:961-26 (community/community) | אהבת ציון | way/31539798 | 68.4 | en: Ahavat Tsiyon; ru: Ахават Ционе | never: highway=residential |
| 6 | fp:961-45 (community/community) | גימנסיה הרצליה | way/405360284 | 8.9 | en: Herzliya Hebrew "Gymnasium"; ru: Еврейская Гимназия «Герцлия» | no POI kind that fits the group community (amenity=school) |
| 8 | fp:553-27 (community/community) | בית יד לבנים | way/370074343 | 14.1 | en: Yad Labanim | never: building=public with no POI tags |
| 8 | fp:745-9 (education/library) | בית יד לבנים | way/370074343 | 6.4 | en: Yad Labanim | never: building=public with no POI tags |
| 8 | fp:563-38 (health/health) | מגדל המאה | way/539793996 | 34.3 | en: Century Tower | never: building=yes with no POI tags |
| 9 | fp:30098 (education/school) | הר נבו | way/30615676 | 31.6 | en: Har Nevo | never: highway=residential |
| 9 | fp:961-40 (community/community) | אריסטובולוס | way/30827684 | 78.2 | en: Aristobulus | never: highway=living_street |
| 10 | tlv:745/95 (community/culture) | בית שלום עליכם | way/203814211 | 7.5 | en: Shalom Alaychem house | never: building=yes with no POI tags |
| 11 | fp:20236 (essentials/shopping) | רביבה וסיליה | node/5109147536 | 5.7 | en: Reviva and Celia | no POI kind that fits the group essentials (amenity=restaurant) |
| 12 | fp:624-28 (education/daycare) | בובליק | way/30754085 | 64.9 | en: Bublick | never: highway=residential |
| 17 | osm:way/1019796256 (outdoors/playground) | ככר מסריק | way/24893732 | 21.1 | en: Masaryk square | never: place=square |
| 19 | tlv:696/370 (outdoors/playground) | טירת צבי | way/641561465 | 20.7 | en: Tirat Zvi | never: highway=residential |
| 20 | fp:564-25 (health/health) | בבלי | way/803479640 | 65.5 | en: Bavli; ru: Бавли; fr: Bavli | never: place=suburb |
| 20 | fp:961-43 (community/community) | מלאכי | way/30773596 | 51.8 | en: Malachi | never: highway=residential |
| 21 | fp:696-242 (outdoors/park) | ירושלמי | way/469646954 | 65.5 | en: Yerushalmi | never: highway=residential |
| 22 | fp:osm-way-34333834 (outdoors/park) | ספורטק צפון | way/34333834 | 0.6 | en: Sportek North | never: landuse=recreation_ground (rule (a) holds: its own OSM element) |

The 20 fall into four groups:
- 11 streets or areas: 10 streets, plus the Bavli suburb.
- 5 buildings with no POI tags: בית החייל, בית יד לבנים ×2, מגדל המאה, בית שלום עליכם.
- Masaryk square (`place=square`), and Sportek North (`landuse`, although it is the place's own element).
- 2 kinds that do not fit the group: the Gymnasium's school feature against a place filed under community, and the
  restaurant Reviva and Celia against a place filed under essentials.

"בזל" never reached this step. It stays ambiguous: street way/26149505 and parking node/331186813, both named בזל
within 80 m. So "Basel" is not written. Only the old `--no-streets` trial would have written it, from the parking lot.

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

These stay skipped, as ordered. Only the two bus stops have two candidates that are both platforms (the stop's two
sides). Every other place's candidates include a street, a path, a parking lot or a suburb, which the strict rule would
refuse anyway.

### Near misses (for the record, never written)

- 32 target places have a feature with the same name, but farther than 80 m. Some examples: כיכר המדינה
  (`fp:30020`, the square way at 104 m), בית יד לבנים (`fp:586-60`, 114 m), יהודה המכבי (94 m, 141 m),
  גן העיר (137 m, 251 m), ספורטק צפון (`fp:943-364`, 85 m).
- 64 have a feature within 80 m whose name contains ours or is contained in it. Identity is required, so these were not
  used. Column `near_miss` in `matches.csv` shows each one.

## Things to check

1. **One rejection keeps the place's own element out.** Sportek North (`fp:osm-way-34333834`) satisfies (a): OSM way
   34333834 is the place itself, a `leisure=park`. It also carries `landuse=recreation_ground`, and NEVER was applied
   literally, before (a). If NEVER should yield to (a), it is a one-line change and this one place (22 min) gets
   "Sportek North".
2. **Two rejections are the same business filed under another group in our data.** רביבה וסיליה (`fp:20236`, filed
   under essentials/shopping) is the restaurant "Reviva and Celia", 5.7 m away. גימנסיה הרצליה (`fp:961-45`) is filed
   under community (findplace layer 961, where the other entries are named after their streets), while the OSM feature is the school.
   The second one is probably right to reject: layer 961 may be a community facility at the school rather than the
   school itself.
3. **OSM itself carries some wrong pairs.** Two examples, both farther than 80 m and so unused: the street way/31539799
   is named אהבת ציון in Hebrew and "HaShofet Nofech" in English, and "נקודת טבע" has the English name
   "Future Cosmetics Boutique". The rules cannot catch a wrong `name:en` on the one kept feature. All 36 written values
   were read by eye and each one is the same name as the Hebrew.
4. **The file does carry OSM ids.** 519 place ids name an OSM element: 229 `osm:node/…`, 113 `osm:way/…`, 3 `osm:relation/…`,
   135 `fp:osm-node-…` and 39 `fp:osm-way-…`. They are the basis of rule (a).
5. **Place ids are not unique** in this file. 21 ids appear more than once: 58 rows in all, one id up to 6 times, and
   for example `fp:27581` and `fp:13730` twice each. This was already true before this step. `diff_check.py` therefore
   compares places by position.
6. **Line endings:** this clone has `core.autocrlf=true` and no `.gitattributes`. A fresh checkout writes CRLF, which
   changes the md5. The committed blob and the working file are LF (md5 `56c27127…`). To get the exact bytes back, use
   `git cat-file blob HEAD:<path>`, not `git checkout`.
7. History: the first version of this step (commit e0cafa57) applied only same name + 80 m + unique. It gave 50 places
   (md5 `0b7da142…`). The strict rule replaced it the same day.

## Files

- `overpass.json`: the raw Overpass answer (1,345,962 bytes).
- `overpass-query.overpassql`: the query.
- `fetch-meta.json`: endpoint, time, User-Agent, bbox, sha256, OSM base.
- `matches.csv`: one row per target place (758). Status is `matched` / `matched-nothing-new` / `rejected-strict` /
  `ambiguous` / `no-match`. Each row has the OSM feature, its kind, the rule (a/b) or the rejection reason, the
  distance, whether it is the place's own OSM id, the four tags read, what was written, what was dropped, and the near
  miss.
- `stats.json`: the counts above, with the rejected list.
- `diff_check.py`: the proof that only `names` changed.

OSM data © OpenStreetMap contributors, ODbL.
