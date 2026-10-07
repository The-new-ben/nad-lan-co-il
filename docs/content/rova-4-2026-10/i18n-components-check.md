# Rova 4 components in four languages: check (7.10.2026, HAD-460)

## What was made

Local only. Nothing was deployed, committed or pushed, and no WordPress call was made.

| component | Hebrew source (unchanged) | new files |
|---|---|---|
| PriceGuide | `scripts/project-stage/price_guide/rova-4.json` | `rova-4.en.json`, `rova-4.fr.json`, `rova-4.ru.json`, `rova-4.ar.json` (same folder) |
| AreaMap v1.1 | `scripts/project-stage/area_map/rova-4.json` | `rova-4.en.json`, `rova-4.fr.json`, `rova-4.ru.json`, `rova-4.ar.json` (same folder); code change in `render_map.py`, see `docs/design/area-map-3d/CHANGELOG-v1.1.md` |

**Method (the `hamedina.*.json` method).** Each file is a deep copy of the Hebrew file:
- **Kept as they are:** every key, number, date, range, `src`, `sources`, `note`, id and position.
- **Replaced:** only the visible text, plus `updated_shown` and a full `ui` object.

**PriceGuide `ui`:**
- It is the `ui` of `hamedina.<lang>.json`: the interface words, units, separators and WhatsApp wording already settled for
  that language.
- Rova 4 strings on top: `more_t`, `js.wa`, the comparison label `js.tw`, and the chart title `chart`.
- `kinds` and `calc.gap` are taken word for word from `hamedina.<lang>.json`. The Hebrew sentences are the same.

**AreaMap place names:**
- Where OpenStreetMap has a local name (`name:en`, `name:ru` or `name:ar`), that name is used. Source:
  `docs/design/area-map-3d/raw/overpass.json`.
- Otherwise the name is transliterated.
- Chain brands keep their Latin brand unless OSM has a local form (Супер-Фарм, سوبير فارم, Шуферсаль Шели, Виктори).
- Developer names stay in Latin in every language (the `NAMES` rule in `scripts/i18n/build_lang_pages.py`).

## Decisions per language

| | EN | FR | RU | AR |
|---|---|---|---|---|
| `lang` / `dir` | en / ltr | fr / ltr | ru / ltr | ar / rtl |
| Rova 4 | Rova 4 | Rova 4 | Рова 4 (in text: район Рова 4) | روفاع 4 |
| New North | New North | Nouveau Nord | Новый Север | الشمال الجديد |
| Kikar HaMedina Towers | Kikar HaMedina Towers | tours Kikar HaMedina | башни Кикар ха-Медина | أبراج كيكار همدينا (map pin in English, as the `NAMES` row) |
| Tel Aviv-Yafo | Tel Aviv-Yafo | Tel Aviv-Jaffa | Тель-Авив-Яффо | تل أبيب يافا |
| Millions | ₪6.04-6.91 million | 6,04-6,91 M₪ | 6,04-6,91 млн ₪ | 6.04-6.91 مليون ₪ |
| Thousands / decimal (`grp` / `dec`) | `,` / `.` | U+202F / `,` | U+00A0 / `,` | `,` / `.` |
| `loc` | en-GB | fr-FR | ru-RU | en-US |
| `updated_shown` | 7 October 2026 | 7 octobre 2026 | 07.10.2026 | 7.10.2026 |
| "see" link | The Kikar HaMedina Towers price guide → /projects/hamedina-en/#nlpg | Les repères de prix des tours Kikar HaMedina → /projects/hamedina-fr/#nlpg | Обзор цен по башням Кикар ха-Медина → /projects/hamedina-ru/#nlpg | دليل أسعار أبراج كيكار همدينا ← /projects/hamedina-ar/#nlpg |
| `ui.links` | 2 English pages (as hamedina.en) | none | none | none |

**Links:**
- **"See" links:** they go to the Kikar language twins, which exist. Each twin returned 200 with hreflang on 7.10.2026,
  and its PriceGuide section carries `id="nlpg"`.
- **Rova 4 pages:** neither data file links to `/north-tel-aviv/rova-4/` itself, so no Hebrew Rova 4 link had to be kept.
  `/en/north-tel-aviv/rova-4/` and `/fr/north-tel-aviv/rova-4/` return 404 today. Once those pages exist, nothing in
  these files needs to change.
- **Map project cards:**
  - Language twins for Kikar HaMedina, DUO, YOO and Park Bavli.
  - The Hebrew page for H Infinity and Akirov Towers (no twins).
  - The Hebrew pages of the two renewal compounds (Arlozorov, Dafna).
- **`page` field:** it stays the Hebrew URL in every file. It is metadata, copied unchanged like `note`.

## The checks

Scripts:
- `docs/qa/had-460/i18n-components/check_i18n.py` (checks 1 to 4);
- `rawcheck.py` (check 5).

How numbers are compared: as values, after normalising each language's separators. "7 October 2026" and
"7 octobre 2026" are read as 7.10.2026, and a leading zero is ignored (07.10.2026).

| check | PriceGuide EN | FR | RU | AR | AreaMap EN | FR | RU | AR |
|---|---|---|---|---|---|---|---|---|
| 1. non-text fields identical (missing / extra / changed) | 0/0/0 | 0/0/0 | 0/0/0 | 0/0/0 | 0/0/0 | 0/0/0 | 0/0/0 | 0/0/0 |
| 2. numbers per string (strings compared, mismatches) | 137, 0 | 137, 0 | 137, 0 | 137, 0 | 269, 0 | 269, 0 | 269, 0 | 269, 0 |
| 3. numbers per file, text and effective UI (Hebrew = language, multiset) | 166 = 166 | 166 = 166 | 166 = 166 | 166 = 166 | 115 = 115 | 115 = 115 | 115 = 115 | 115 = 115 |
| 4. scan: em/en dash, "!", source names, leftover Hebrew in the rendered HTML | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| 5. raw file: every distinct number in the whole Hebrew file is in the language file and back (sources, src, coordinates included) | 167 = 167 | 167 = 167 | 167 = 167 | 167 = 167 | 452 = 452 | 452 = 452 | 452 = 452 | 452 = 452 |

**More detail on the checks:**
- **Check 5 and metadata:** `sources`, `src`, `note`, `tax_src`, `gap_src` and `research` are copied in English unchanged,
  so they are read with the Hebrew separators in every file.
- **Placeholders and completeness (PriceGuide):**
  - Every key of `render.UI_HE` and all 12 `js` keys are present.
  - `u_m2`, `u_floor`, `u_mil`, `u_ils`, `u_pm2` and `approx` each hold `{n}` once.
  - Every `js` template has the same placeholders as Hebrew.
- **Completeness (AreaMap):**
  - Every `UI` key, `js`, `cats` and `loc` key is present.
  - Every place type has a plural.
  - The light-rail fact ("The Red Line has been running here since August 2023" and its equivalents) is matched to its
    stop (Arlozorov) in every language.
- **Banned words:** the scan found nothing except FR "Logement unique". That is the settled label of the purchase-tax
  choice ("single home"), from `hamedina.fr.json`, not a superlative. The map's "Developer: / Promoteur : / Застройщик: /
  المطوّر:" before a renewal developer follows the site's own `NAMES` pattern ("היזם: (.+)").
- **Render test:** `render.html(d, '972525101555')` and `render_map.html(d)` work for every file.
  - PriceGuide sizes: 22,284 / 22,476 / 21,806 / 21,456 bytes (EN / FR / RU / AR).
  - AreaMap sizes: 29,962 / 30,613 / 29,414 / 28,646 bytes.
  - Default calculator result as served (new building, 100 m², single home), the same values as Hebrew:
    - Hebrew: 6.3-6.8 million, 63,000-68,000 per m², tax 238,000, total 6.79.
    - EN: ₪6.3-6.8 million.
    - FR: 6,3-6,8 M₪.
    - RU: 6,3-6,8 млн ₪.
    - AR: 6.3-6.8 مليون ₪.

## Browser check (headless Chrome, 1440x900 and 390x844)

Shots: `docs/qa/had-460/i18n-components/<lang>-<1440|390>-price.png`, `-price-premium.png` (penthouse mode pressed) and the
map shots. All 10 runs: zero page and console errors, no horizontal scroll (`scrollWidth - innerWidth = 0`).

The calculator after pressing "penthouse or garden apartment" gave the same values in every language:

| | price range | per m² | total |
|---|---|---|---|
| Hebrew | 8-11 מיליון ₪ | 80,000-110,000 | 9.97 |
| EN | ₪8-11 million | about ₪80,000-110,000 per m² | about ₪9.97 million |
| FR | 8-11 M₪ | environ 80 000-110 000 ₪/m² | environ 9,97 M₪ |
| RU | 8-11 млн ₪ | около 80 000-110 000 ₪ за м² | около 9,97 млн ₪ |
| AR | 8-11 مليون ₪ | نحو 80,000-110,000 ₪ للمتر | نحو 9.97 مليون ₪ |

The WhatsApp text is built in each language, for example: "Hello, I checked the Rova 4 Tel Aviv price guide: Penthouse or
garden apartment, 100 m², estimate ₪8-11 million. I would like more details (nad-lan.co.il)".

**Shortened after looking at the phone shots.** The comparison chart's middle label ran into the "68,000" price label on
390 px phones in EN, FR and RU (seen in `en-390-price.png`, first run). It was shortened to the Hebrew label's width
(125 units):

| | label | width (units) |
|---|---|---|
| EN | Kikar HaMedina average | 125 |
| FR | Moyenne Kikar HaMedina | 131 |
| RU | Кикар ха-Медина, ср. | 120 |
| AR | متوسط أبراج كيكار همدينا | 127 |

## Strings I could not translate with full confidence

1. **"רובע 4" in Arabic:** "روفاع 4", a transliteration that follows the brief's name "Rova 4". `hamedina.ar.json` wrote
   "المنطقة 4" for the same district. The Russian uses "Рова 4" or "район Рова 4" ("район 4" in `hamedina.ru.json`). One
   word for the whole site is needed once the ChatGPT article translations come back.
2. **"Kikar HaMedina" spelling:** the brief and this task say "Kikar HaMedina". The live Kikar pages, their H1s and
   `NAMES` say "Kikar Hamedina". These files follow the brief. One sed aligns them if the owner prefers the live spelling.
3. **Developer names** (Latin forms not found on the companies' own pages):
   - "אפריקה התחדשות" → Africa Renewal;
   - "יעז יזמות" → Yaaz Development;
   - "אדם שוסטר" → Adam Shuster;
   - "אנשי העיר" → Anshei HaIr;
   - "בית וגג" → Bayit VeGag;
   - "קבוצת תשובה ואלעד מגורים" → Tshuva Group and Elad Residences.
4. **Street names:**
   - Latin forms: "זלוציסטי" → Zlotisti, "בן שפרוט" → Ben Shaprut, "לסר אורי" → Lasser Uri,
     "גליצנשטיין" → Glitzenstein, "ליסין" → Lissin, "שלומציון המלכה" → Shlomtzion HaMalka.
   - The Arabic forms of every street were transliterated, not checked against Arabic street signs.
5. **Café and place names with no OSM English:**
   - "ג'ונו" → Juno;
   - "מיצלי" → Mitzli;
   - "לחם ארז" → Lechem Erez;
   - "בית לחם" (a café, OSM's English "Bethlehem" not used) → Beit Lechem;
   - "גן אורי" (a kindergarten; OSM's English "Gan Or" contradicts the Hebrew) → Gan Uri;
   - "עירוני ד' סניף" → Ironi Dalet, branch campus;
   - "צהרוני ניצני יובל" → Nitzanei Yuval after-school club;
   - "מסוף 2000" in Arabic → "محطة 2000".
6. **Arabic numerals with dual nouns:** digits were kept, so the numbers match: "2 أبراج", "2 غرف", "2.5 غرف".
   Classical Arabic would write برجان or غرفتان without the digit.
7. **"חדשה מקבלן"** → "brand-new apartment" and "appartement neuf", and **"בלי דירה בפרויקט של יזם"** → "without new-build
   projects". This avoids the word "developer", which the price guide's language scan bans.
8. **"מחיר שיווק"** (kind `mkt`) is inherited from the Kikar files. RU "Цена в проекте" was already marked unsure there.
9. **Russian park names** are in the nominative after "сад" / "сквер" ("Сад Гордон"), the Israeli-Russian usage. They are
   not declined.

## Seen in the components (not changed here)

1. **The price guide's area chart title (Hebrew):** `rova-4.json` has no `ui.chart`, so the Hebrew `<title>` reads "המחיר
   למ״ר לפי הקומה במגדלים, עם העסקאות שפורסמו", the floor chart's title, on an area chart. The four language files carry an
   area title ("Price per m² for your choice, against the Kikar HaMedina Towers average and Tel Aviv-Yafo" and equivalents).
   Proposed Hebrew override: `"chart": "המחיר למ״ר לבחירה שלכם, מול ממוצע מגדלי כיכר המדינה ותל אביב יפו"`.
2. **Chart labels collide in penthouse mode, Hebrew included.** The labels "80,000" and "110,000" sit on the next row's
   label (`he-390-price-premium.png`). This is the chart layout in `render.py`, not the data.
3. **The calculator's explanation line is set with `textContent`.** After the first script run it loses the number
   islands, so a range can break at its hyphen ("70,000-" / "75,000", seen in `ar-390-price.png`). This happens in Hebrew too.
4. **Units can wrap away from their numbers.** In EN a lone "₪" can end a line before its number, and a unit after a number
   island can start a line. This is the known `rich()` behaviour (`price_guide/i18n-check.md`, item 1 and item 4).
5. **The "Where is the apartment" field label** (Hebrew default "איפה הדירה") is kept in all languages. In the area mode its
   options are apartment types, so a Rova 4 override such as "סוג הדירה" may read better. That is a Hebrew decision first.
6. **Going live needs release work** in `pg_helper.py` (not edited, by instruction):
   - `[nadlan_price_guide key="rova-4"]` always renders `he`, so `/en/north-tel-aviv/rova-4/` needs a `lang` attribute
     or the page's language;
   - the files are already found by `payloads()` as (`rova-4`, `en`) and so on;
   - the AreaMap shortcode has the same gap (`CHANGELOG-v1.1.md`).
