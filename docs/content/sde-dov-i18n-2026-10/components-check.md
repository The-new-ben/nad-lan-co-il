# Sde Dov components in four languages: check (7.10.2026, HAD-460)

## What was made

Local only. Nothing was deployed, committed or pushed, and no WordPress call was made. The only network calls were public
GETs to check links.

| component | Hebrew source (unchanged) | new files |
|---|---|---|
| PriceGuide | `scripts/project-stage/price_guide/sde-dov-prices.json` (39 rows, 27 sources, `"open_groups": 2`) | `sde-dov-prices.en.json`, `.fr.json`, `.ru.json`, `.ar.json` (same folder) |
| AreaMap v1.1 | `scripts/project-stage/area_map/sde-dov.json` (9 projects, 25 places, no renewal) | `sde-dov.en.json`, `.fr.json`, `.ru.json`, `.ar.json` (same folder) |

No code was changed: `render.py`, `rooms.py`, `pg_helper.py` and `render_map.py` are untouched.

**Method.** This is the Rova 4 method (`docs/content/rova-4-2026-10/i18n-components-check.md`). Each file is a deep copy of
the Hebrew file.
- **Kept exactly:** every key, number, date, range, `src`, `sources`, `note`, `open_groups`, id, coordinate and order.
- **Replaced:** the visible text only, plus `updated_shown` and a full `ui` object.

**PriceGuide `ui`.**
- Base: the `ui` of `rova-4.<lang>.json`, which is itself the settled `ui` of `hamedina.<lang>.json` (interface words, units,
  separators, WhatsApp wording, the two English links in EN).
- Sde Dov strings added on top, from the Hebrew `ui`: `more_t`, `chart`, `js.avg`, `js.tw`, `js.aria_a` and `js.wa`.
- `kinds`: word for word from `rova-4.<lang>.json` (the Hebrew is the same).

**AreaMap `ui`.**
- Base: the `ui` of `rova-4.<lang>.json`.
- Added for every language: `js.lrt` (Green Line) and plurals for the three new place types (beach, promenade, future Green
  Line station).
- English only: `js.key` and `js.edge` say "quarter", the site's English word for Sde Dov ("Sde Dov quarter" in the
  `NAMES` table). Rova 4 uses "district".

## Names

| | EN | FR | RU | AR |
|---|---|---|---|---|
| `lang` / `dir` / `loc` | en / ltr / en-GB | fr / ltr / fr-FR | ru / ltr / ru-RU | ar / rtl / en-US |
| Sde Dov (in text) | the Sde Dov quarter | le quartier de Sde Dov | район Сде-Дов | حي سديه دوف |
| Thousands / decimal | `,` / `.` | U+202F / `,` | U+00A0 / `,` | `,` / `.` |
| Millions | ₪9.45 million | 9,45 M₪ | 9,45 млн ₪ | 9.45 مليون ₪ |
| `updated_shown` | 7 October 2026 | 7 octobre 2026 | 07.10.2026 | 7.10.2026 |

**Project and developer names.**
- **Project names** are the brands as the site already prints them on the language pages and in the comparison table:
  Rainbow Tel Aviv, DIMRI YAMA, ASHIRA, ZOHI (Tel Aviv), VOGUE / GINDI VOGUE, UTOPIA, FIRST.
- **Map pins** carry the same Latin label in all four languages, the Arabic included (owner's rule of 28.9: Arabic titles
  in English). The labels are: Rainbow, DIMRI YAMA, ASHIRA, UTOPIA, ZOHI, Shikun & Binui, GINDI VOGUE, FIRST, Mediterranean
  Towers.
- **Developer names** are the forms on the live language pages: Israel Canada, Y.H. Dimri, Avisror Moshe & Sons, Nahmias
  Group, Gindi Holdings and Hagag Group. "לוינשטין, מבנה ואלייד" becomes "Levinstein, Mivne and Allied", with the joining word
  translated.

**Other place names.**
- Where OpenStreetMap has an English name it is used: Tel Baruch Beach, Jilber Garden, Lamed HaYeruka, Reading Beach Park
  and Shufersal Express. "The Northen Dogs Beach" is fixed to "Northern Dog Beach".
- The established English names are used where they exist: Marc Chagall, Isaac Bashevis Singer, Reading, Levi Eshkol.
- Every other name is transliterated. "Kochav HaTzafon" and "Plan L" are the forms already on the live DIMRI YAMA and ASHIRA
  language pages.

## Links (GET-checked 7.10.2026, about 20:10 UTC)

| target | result | used for |
|---|---|---|
| `/projects/{rainbow-tel-aviv, dimri-yama-sde-dov, ashira-sde-dov, utopia-sde-dov, zohi-sde-dov, shikun-binui-sde-dov, gindi-vogue-sde-dov}-{en,fr,ru,ar}/` | 28 of 28 answer 200, with hreflang in all 5 languages | map project cards, in the same language |
| `/projects/first-sde-dov-{en,fr,ru,ar}/`, `/projects/migdalei-hayam-sde-dov-{en,fr,ru,ar}/` | 404 | the map cards keep the Hebrew page (200) |
| `/en/north-tel-aviv/rova-4/` | 200, `id="nlpg"` is the English PriceGuide (`lang="en"`) | EN "see" link `#nlpg` |
| `/fr/`, `/ru/`, `/ar/north-tel-aviv/rova-4/` | 404 | FR, RU and AR "see" links keep the Hebrew `/north-tel-aviv/rova-4/#nlpg` with translated text |
| `/{en,fr,ru,ar}/sde-dov/` and `/{en,fr,ru,ar}/sde-dov/prices/` | 404 | the `page` field stays Hebrew (metadata, like `note`) |

**The Rainbow, DIMRI YAMA and ASHIRA "see" links.**
- The language pages exist, but **none of them has a PriceGuide** (`id="nlpg"` is missing on all 12 pages). An `#nlpg` link
  would open the top of the page.
- So each link goes to the price section those pages do have: `#nlpjx-price` (`<section id="nlpjx-price">`, labelled
  "Prices and comparison").
- The text names what is there: "Rainbow Tel Aviv: prices and comparison →" and the equivalents in each language, not "the
  price guide".
- When those projects get language PriceGuides, change `#nlpjx-price` to `#nlpg` and the text back to "price guide": 3
  hrefs and 3 texts per file.

## The checks

Scripts, in `docs/qa/had-460/i18n-components/`:
- `check_i18n_sde_dov.py`, checks 1 to 4. It reuses `check_i18n.py`, which is not modified.
- `rawcheck_sde_dov.py`, check 5.
- `shoot_sde_dov.py`, the browser run.

How numbers are compared: as values, after normalising each language's separators.

**Month names.** A month written as a word is read as its number in every language, Hebrew included: "April 2026", "avril
2026", "в апреле 2026", "نيسان 2026" → 4.2026, and "במרץ 2026" → 3.2026. The Rova 4 script did this for October only. So a
month written as a word must still carry the same month and year as the Hebrew.

| check | PriceGuide EN | FR | RU | AR | AreaMap EN | FR | RU | AR |
|---|---|---|---|---|---|---|---|---|
| 1. non-text fields identical (missing / extra / changed) | 0/0/0 | 0/0/0 | 0/0/0 | 0/0/0 | 0/0/0 | 0/0/0 | 0/0/0 | 0/0/0 |
| 2. numbers per string (strings compared, mismatches) | 197, 0 | 197, 0 | 197, 0 | 197, 0 | 94, 0 | 94, 0 | 94, 0 | 94, 0 |
| 3. numbers per file, text and effective UI (Hebrew = language, multiset) | 216 = 216 | 216 = 216 | 216 = 216 | 216 = 216 | 37 = 37 | 37 = 37 | 37 = 37 | 37 = 37 |
| 4. scan: em/en dash, "!", source names, leftover Hebrew in the rendered HTML | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| 5. raw file: every distinct number in the whole Hebrew file is in the language file and back | 304 = 304 | 304 = 304 | 304 = 304 | 304 = 304 | 297 = 297 | 297 = 297 | 297 = 297 | 297 = 297 |

**More detail on the checks:**
- **Hebrew letters:** zero in the full rendered HTML (`data-cfg` included) and zero in every non-metadata string of all 8
  files. Hebrew appears only in `sources` and `note`, which are copied unchanged as in Rova 4.
- **PriceGuide completeness:**
  - every key of `render.UI_HE` and all 12 `js` keys are present;
  - each unit pattern holds `{n}` once;
  - every `js` template has the Hebrew placeholders;
  - there are 39 rows in 5 groups, `open_groups` is 2, and 27 sources.
- **AreaMap completeness:**
  - every `UI`, `js`, `cats` and `loc` key is present;
  - every place type has a plural;
  - ids, coordinates, `hero`, edge distances, boundary, view and order are identical (checked one by one);
  - `facts` stays `{}`.
- **Banned words:** none, except FR "Logement unique". That is the settled purchase-tax label from `hamedina.fr.json`, as in
  Rova 4.
- **"Developer" is allowed in this price guide.** The Hebrew itself says "דוחות היזמים", "לפי היזם" and "הערכת היזם". The
  visible text has 9 occurrences in Hebrew and 9 in each language. No developer company is named in the price guide; only
  project names are.
- **Render test:** `render.html(d, '972525101555')` and `render_map.html(d)` run without errors for all 8 files.
  - PriceGuide sizes: 30,297 / 30,409 / 29,668 / 28,862 bytes (EN / FR / RU / AR); Hebrew is 27,658.
  - AreaMap sizes: 16,172 / 16,687 / 15,892 / 15,549 bytes; Hebrew is 15,176.
- **Default calculator result** ("most projects in the quarter", 100 m², single home) gives the Hebrew values in every
  language: 7-8.3 million, 70,000-83,000 per m², tax 326,000, total 7.98.

## Browser check (headless Chrome, `channel="chrome"`, SwiftShader WebGL, 390x844 phone, 12 s map wait)

Shots in `docs/qa/had-460/i18n-components/`, for EN and AR:
- `sde-dov-<lang>-390-price.png`;
- `-price-sea.png` ("high floor or facing the sea" pressed);
- `-price-list.png` (the full list opened, 39 rows);
- `-map.png`;
- `-card.png` (the Rainbow card);
- `-map-list.png`.

FR and RU were run without shots for the same DOM checks. Report: `sde-dov-report.json`.

| | page overflow | elements past the section edge | Hebrew in component text | console / page errors | map |
|---|---|---|---|---|---|
| EN | 0 | price 0; map: only the filter chips, inside their own horizontal scroll strip (`overflow-x:auto`, by design) | 0 | 0 / 0 | ready, 9 pins, 22 base-map labels, none Hebrew |
| FR | 0 | same | 0 | 0 / 0 | same |
| RU | 0 | same | 0 | 0 / 0 | same |
| AR | 0 | same (strip runs right to left) | 0 | 0 / 0 | same; RTL page, controls mirrored as in Hebrew |

**The cards and the filters.**
- The Rainbow card opens inside the frame in every language. Its button goes to `rainbow-tel-aviv-<lang>/`.
- There is no renewal filter, as in Hebrew v1.1. The five filters are: projects 9, schools 9, parks 8, shops 2, transport 6.

**Calculator, sea mode, in every language.** 9-11 million, 90,000-110,000 per m², tax about 514,000, total about 10.51
million. The WhatsApp text is built in the page's language, for example: "Hello, I checked the Sde Dov price guide: High
floor or facing the sea, 100 m², estimate ₪9-11 million. I would like more details (nad-lan.co.il)".

**What the shots show.**
- **EN phone:** the order is the opening paragraph, 3 tiles, the calculator, the WhatsApp button, the fine print, "The full
  price guide (39)" and the 4 "see" links.
- **Chart labels** ("Your choice / Sde Dov average / Tel Aviv-Yafo, median") do not collide in the default mode or in sea
  mode.
- **AR:** the Latin brands sit correctly at the start of RTL lines ("DIMRI YAMA، 32 شقة في 2025"). Ranges stay left to
  right ("2.4-2.7 مليون ₪").

**Changed after looking.** The fine print's "6%-8%" broke as "6%-" / "8%" on the EN phone. In AR it showed the range
reversed ("%8-%6"), because `rich()` makes "6" and "8" separate islands. EN and AR now say "6-8%", as RU already did (FR
says "6 à 8%"). It is one island, the same numbers and the same check result.

## Strings I could not translate with full confidence

1. **"Shikun & Binui"** is how the company writes its name in English. The live language pages say "Shikun Binui".
2. **"מגדלי הים התיכון" → "Mediterranean Towers"**, the company's English name, kept in Latin in all four languages. Its fact
   "דיור מוגן" is translated as:
   - Senior living;
   - Résidence seniors;
   - Резиденция для пожилых;
   - سكن محمي لكبار السن.
3. **"תכנית ל"** is "Plan L" in EN and FR, as on the live DIMRI YAMA pages. In RU it is "Тохнит Ламед" and in AR "تخنيت لامد",
   transliterated, with no live precedent on the site.
4. **Hebrew letter numerals were kept as letters,** so no digit was added: "עירוני כ"ד עמוס עוז" → "Ironi Kaf Dalet Amos
   Oz", and "גינה לזכר כ"ג יורדי הסירה" → "Kaf Gimel Yordei HaSira Memorial Garden". English readers may know them as "24"
   and "the 23".
5. **"כוכב הצפון" → "Kochav HaTzafon"** for the school and the garden. OSM's English name for the garden is "Northern Star
   Park". The transliteration matches the neighbourhood name on the live language pages.
6. **Station names follow the Hebrew labels.** The municipal GIS has English names for these stations, and two of them
   differ from the Hebrew: it calls "זהרה לביטוב" "Dov" and "נופי ים" "HaGush HaGadol". These files keep the Hebrew labels:
   Zohara Levitov and Nofei Yam. "פרופס" → Propes, as in the GIS.
7. **"מול הים" (facing the sea)** is RU "вид на море" (sea view) in the mode label and in the Rainbow row. That is the usual
   Russian marketing phrase, slightly wider than "facing".
8. **Arabic months** use the Levantine names (نيسان, آذار, حزيران, كانون الأول), as `rova-4.ar.json` used "آب". Arabic digits
   stay with dual and plural nouns ("2 غرف"), as in Rova 4.
9. **"VAT" in Russian is "НДС"**. Some Israeli Russian media write "маам".
10. **The English pills for the three projects** are the bare brands (Rainbow, DIMRI YAMA, ASHIRA), not "In Rainbow". They
    also feed the WhatsApp text ("…price guide: Rainbow, 100 m²…").

## Seen in the components (not changed here)

1. **Same `rich()` behaviour as in Rova 4.** A lone ₪ can end a line before its number. The EN default explanation breaks as
   "is ₪" / "75,000-85,000." on a 390 px phone. This is renderer behaviour, not the data.
2. **The Hebrew file has the same "6%-8%" split** in its fine print. By the same mechanism as the AR shot it should show as
   "%8-%6" in RTL, the low number on the left unlike every other range (Hebrew was not shot in this run). Proposed Hebrew data
   fix: "6-8%" (a Hebrew decision; not edited).
3. **Rainbow, DIMRI YAMA and ASHIRA language pages need their own PriceGuides.** Today only the Hebrew pages carry one. Once
   they exist, the "see" links switch to `#nlpg` (see Links above).
4. **Going live needs release work in `pg_helper.py` (not edited),** as for Rova 4:
   - the shortcode always renders `he`;
   - no `/en/` (or other) Sde Dov price page exists yet;
   - the map shortcode has the same gap.
