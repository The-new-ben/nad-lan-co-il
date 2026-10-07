# PriceGuide i18n check: Kikar Hamedina (hamedina.en/fr/ru/ar.json), 7.10.2026

**What was made:** four data files beside `hamedina.json`, one per language twin of `/projects/hamedina/`
(`/projects/hamedina-en/`, `-fr/`, `-ru/`, `-ar/`). Each file is a deep copy of the Hebrew file (every key, every number,
`sources`, `src`, dates and `note` kept as they are) with only the visible text replaced, plus `updated_shown` and a `ui` object
that overrides every key of `render.UI_HE` (including all 12 `js` keys). Nothing else in the repo was edited; nothing was committed
or deployed.

**The H2 titles:**

| Lang | H2 |
|---|---|
| EN | How much does an apartment cost at Kikar Hamedina Towers? |
| FR | Combien coûte un appartement dans les tours Kikar Hamedina ? |
| RU | Сколько стоит квартира в башнях Кикар ха-Медина? |
| AR | كم يبلغ سعر شقة في أبراج كيكار همدينا؟ |

**Inputs read:** `hamedina.json`, `render.py` (UI_HE, `ui()`, `html()`, the script's use of every `T.*` key), the four live pages
(fetched 7.10.2026, raw HTML: names, top WhatsApp button wording, number style, dates, live links), `sitemap_index.xml` with the
page, post, nadlan_intl and nadlan_term sitemaps (591 URLs), `docs/research/2026-09-30-kikar-hamedina/serp-dna.md`, `serp-fr.md`,
`serp-ru.md`, `serp-ar.md` (there is no serp file in `docs/research/2026-10-kikar-v7/`; its `packet-*.json` gave the names,
WhatsApp text, units, typography and banned-word lists per language).

## Decisions taken from the live pages

| | EN | FR | RU | AR |
|---|---|---|---|---|
| Project name | Kikar Hamedina Towers | les tours Kikar Hamedina | башни Кикар ха-Медина | أبراج كيكار همدينا |
| `wa` (exact top button text on the live page) | More details on WhatsApp | Plus de détails sur WhatsApp | Подробнее в WhatsApp | مزيد من التفاصيل عبر واتساب |
| Millions | ₪9.58-10.63 million | 9,58-10,63 M₪ (the page's own style) | 9,58-10,63 млн ₪ | 9.58-10.63 مليون ₪ |
| Per m² | ₪65,000 per m² | 65 000 ₪/m² | 65 000 ₪ за м² | 65,000 ₪ للمتر |
| Thousands / decimal (`grp` / `dec`) | `,` / `.` | U+202F / `,` | U+00A0 / `,` | `,` / `.` (live page: Latin digits only, 0 Eastern digits) |
| `loc` | en-GB | fr-FR | ru-RU | en-US |
| `updated_shown` (the page's own full-date style) | 7 October 2026 | 7 octobre 2026 | 07.10.2026 | 7.10.2026 |
| `links` | 2 English pages (below) | `[]` | `[]` | `[]` |

- **Links:** no language version of `/apartment-purchase-cost-calculator/` or `/mortgage-calculator/` exists (`/en|fr|ru|ar/mortgage-calculator/`
  and `/en/apartment-purchase-cost-calculator/` return 404; none in the sitemaps). English has two English pages on the same two needs,
  both already linked from the live EN twin: `/israel-purchase-tax-foreign-residents/` ("Israel purchase tax for foreign residents →")
  and `/israel-mortgage-non-residents/` ("Israeli mortgages for non-residents →"). FR, RU and AR have no equivalent (the only French
  buying guide, `/acheter-appartement-israel-2026/`, is a general guide written without accents; `/fr|ru/property-value-estimator/` is a
  seller's value estimator), so their `links` are `[]`. Set EN to `[]` too if only true calculator twins should be linked.
- **Dates inside the table and tiles** stay exactly as in Hebrew (`10.2026`, `4-12.2024`, `1-3.2026`), as instructed.
- **Spaces before units:** in FR and RU, thousands use the no-break space inside the number; between a number and its unit
  (₪, M₪, млн, m², м²) the files use a plain space. Reason, seen in the browser: `render.rich()` makes each number an
  inline-block island, and browsers always allow a wrap right after an inline-block, even before a no-break space; with a no-break
  space the wrapped line then starts with a visible space (" m²", " ₪/m²"). A plain space wraps cleanly. French no-break spaces are
  kept before ":" and "?" where a word precedes them, and "млн ₪" keeps a no-break space between the two words.
- **No letters glued to a number**, for the same reason (a wrap could split "5" from "-комнатную" or "12" from "e étage"):
  RU "квартира из 3 комнат", "на этаже 12"; FR "étage 12"; EN "a 140 m² apartment with 4 rooms"; AR ranges as
  "من ... إلى ..." and the conjunction on a word ("ولشقة من 4 غرف 6.84 مليون") instead of "و6.84".
- **Shortened to fit the phone layout** (checked at 390 px): the total row ("Total with tax", "Total avec la taxe", "Итого с налогом",
  "الإجمالي مع الضريبة"; the line above already names the purchase tax) and the chart's towers label ("Towers’ average",
  "Moyenne des tours", "Средняя по башням", "متوسط الأبراج") so it no longer runs into the price labels of the row above.

## The five checks, per language

Checked with a Python script against `hamedina.json` and `render.UI_HE` (numbers compared as values after normalising each
language's separators; the month words for October are read as 10 so the dates compare too).

## EN (`hamedina.en.json`)

1. **Numbers in `calc` and every non-text field identical to Hebrew:** PASS. 29 numeric calc values compared (modes lo/hi/band/lo_floor1/hi_floor39, deals_plot, avg_line, ta_median, tax_single, tax_more), plus slug, dates, kinds keys, `sources`, `src`, `note`; missing keys 0, extra keys 0, changed values 0.
2. **Every number inside text matches the Hebrew string it translates (same values, separators may differ):** PASS, 134 strings compared one to one (data text, kind labels, every UI string, the date).
   - thousands separator in text: expected U+002C; plain-space groups 0, other separators 0; `ui.grp` = U+002C, `ui.dec` = `.`.
3. **Placeholders:** PASS. Unit patterns u_m2, u_floor, u_mil, u_ils, u_pm2, approx each hold `{n}` exactly once; the 12 js templates hold the same placeholders as Hebrew ({n}, {lo}, {hi}, {f}, {avg}, {m}, {ta}, {a}, {r}); every UI_HE key and js key present (33 + 12).
   - `lang` en, `dir` ltr, `loc` en-GB, links: Israel purchase tax for foreign residents → https://nad-lan.co.il/israel-purchase-tax-foreign-residents/; Israeli mortgages for non-residents → https://nad-lan.co.il/israel-mortgage-non-residents/.
4. **Scan for `—`, `–`, `!`, source names (Globes, Bizportal, Calcalist, ice, ynet, Madlan, Yad2, nadlan.gov.il, Mako, TheMarker, Sotheby's, in Hebrew and Latin), banned words (interface, platform, simulation, demo, engine, developer, broker, superlatives, in all four languages) and leftover Hebrew in the rendered HTML:** PASS, nothing found.
5. **Render test** (`render.html(d,'972525101555')`): PASS, 15969 bytes of markup, no exception. Default calculator result as served: range `8.46-9.74`, per m² `60,400-69,600`, tax `442,000`, total `9.54`.

## FR (`hamedina.fr.json`)

1. **Numbers in `calc` and every non-text field identical to Hebrew:** PASS. 29 numeric calc values compared (modes lo/hi/band/lo_floor1/hi_floor39, deals_plot, avg_line, ta_median, tax_single, tax_more), plus slug, dates, kinds keys, `sources`, `src`, `note`; missing keys 0, extra keys 0, changed values 0.
2. **Every number inside text matches the Hebrew string it translates (same values, separators may differ):** PASS, 134 strings compared one to one (data text, kind labels, every UI string, the date).
   - thousands separator in text: expected U+202F; plain-space groups 0, other separators 0; `ui.grp` = U+202F, `ui.dec` = `,`.
3. **Placeholders:** PASS. Unit patterns u_m2, u_floor, u_mil, u_ils, u_pm2, approx each hold `{n}` exactly once; the 12 js templates hold the same placeholders as Hebrew ({n}, {lo}, {hi}, {f}, {avg}, {m}, {ta}, {a}, {r}); every UI_HE key and js key present (33 + 12).
   - `lang` fr, `dir` ltr, `loc` fr-FR, links: none (`[]`).
4. **Scan for `—`, `–`, `!`, source names (Globes, Bizportal, Calcalist, ice, ynet, Madlan, Yad2, nadlan.gov.il, Mako, TheMarker, Sotheby's, in Hebrew and Latin), banned words (interface, platform, simulation, demo, engine, developer, broker, superlatives, in all four languages) and leftover Hebrew in the rendered HTML:** PASS, nothing found.
5. **Render test** (`render.html(d,'972525101555')`): PASS, 15990 bytes of markup, no exception. Default calculator result as served: range `8,46-9,74`, per m² `60 400-69 600`, tax `442 000`, total `9,54`.

## RU (`hamedina.ru.json`)

1. **Numbers in `calc` and every non-text field identical to Hebrew:** PASS. 29 numeric calc values compared (modes lo/hi/band/lo_floor1/hi_floor39, deals_plot, avg_line, ta_median, tax_single, tax_more), plus slug, dates, kinds keys, `sources`, `src`, `note`; missing keys 0, extra keys 0, changed values 0.
2. **Every number inside text matches the Hebrew string it translates (same values, separators may differ):** PASS, 134 strings compared one to one (data text, kind labels, every UI string, the date).
   - thousands separator in text: expected U+00A0; plain-space groups 0, other separators 0; `ui.grp` = U+00A0, `ui.dec` = `,`.
3. **Placeholders:** PASS. Unit patterns u_m2, u_floor, u_mil, u_ils, u_pm2, approx each hold `{n}` exactly once; the 12 js templates hold the same placeholders as Hebrew ({n}, {lo}, {hi}, {f}, {avg}, {m}, {ta}, {a}, {r}); every UI_HE key and js key present (33 + 12).
   - `lang` ru, `dir` ltr, `loc` ru-RU, links: none (`[]`).
4. **Scan for `—`, `–`, `!`, source names (Globes, Bizportal, Calcalist, ice, ynet, Madlan, Yad2, nadlan.gov.il, Mako, TheMarker, Sotheby's, in Hebrew and Latin), banned words (interface, platform, simulation, demo, engine, developer, broker, superlatives, in all four languages) and leftover Hebrew in the rendered HTML:** PASS, nothing found.
5. **Render test** (`render.html(d,'972525101555')`): PASS, 15469 bytes of markup, no exception. Default calculator result as served: range `8,46-9,74`, per m² `60 400-69 600`, tax `442 000`, total `9,54`.

## AR (`hamedina.ar.json`)

1. **Numbers in `calc` and every non-text field identical to Hebrew:** PASS. 29 numeric calc values compared (modes lo/hi/band/lo_floor1/hi_floor39, deals_plot, avg_line, ta_median, tax_single, tax_more), plus slug, dates, kinds keys, `sources`, `src`, `note`; missing keys 0, extra keys 0, changed values 0.
2. **Every number inside text matches the Hebrew string it translates (same values, separators may differ):** PASS, 134 strings compared one to one (data text, kind labels, every UI string, the date).
   - thousands separator in text: expected U+002C; plain-space groups 0, other separators 0; `ui.grp` = U+002C, `ui.dec` = `.`.
3. **Placeholders:** PASS. Unit patterns u_m2, u_floor, u_mil, u_ils, u_pm2, approx each hold `{n}` exactly once; the 12 js templates hold the same placeholders as Hebrew ({n}, {lo}, {hi}, {f}, {avg}, {m}, {ta}, {a}, {r}); every UI_HE key and js key present (33 + 12).
   - `lang` ar, `dir` rtl, `loc` en-US, links: none (`[]`).
4. **Scan for `—`, `–`, `!`, source names (Globes, Bizportal, Calcalist, ice, ynet, Madlan, Yad2, nadlan.gov.il, Mako, TheMarker, Sotheby's, in Hebrew and Latin), banned words (interface, platform, simulation, demo, engine, developer, broker, superlatives, in all four languages) and leftover Hebrew in the rendered HTML:** PASS, nothing found.
5. **Render test** (`render.html(d,'972525101555')`): PASS, 15231 bytes of markup, no exception. Default calculator result as served: range `8.46-9.74`, per m² `60,400-69,600`, tax `442,000`, total `9.54`.

## Browser check (beyond the five)

Each section was rendered with `render.CSS` and `render.JS` in headless Edge at 1280 px and 390 px, the controls were pressed
(mode "new building nearby", tax "additional apartment", the phone "full list" button) and the script's output was read back and
screenshotted (screenshots looked at). All 8 runs: no script error, no horizontal scroll, floor slider hidden for the non-tower
modes, the script's first output identical to the server-rendered default.

| | Default (towers, 140 m², floor 20, single) | New building, additional apartment |
|---|---|---|
| EN | ₪8.46-9.74 million, about ₪60,400-69,600 per m², tax about ₪442,000, total about ₪9.54 million | ₪8.82-9.52 million, tax about ₪796,000, total about ₪9.97 million |
| FR | 8,46-9,74 M₪, environ 60 400-69 600 ₪/m², environ 442 000 ₪, environ 9,54 M₪ | 8,82-9,52 M₪, environ 796 000 ₪, environ 9,97 M₪ |
| RU | 8,46-9,74 млн ₪, около 60 400-69 600 ₪ за м², около 442 000 ₪, около 9,54 млн ₪ | 8,82-9,52 млн ₪, около 796 000 ₪, около 9,97 млн ₪ |
| AR | 8.46-9.74 مليون ₪، نحو 60,400-69,600 ₪ للمتر، نحو 442,000 ₪، نحو 9.54 مليون ₪ | 8.82-9.52 مليون ₪، نحو 796,000 ₪، نحو 9.97 مليون ₪ |

WhatsApp text sent (towers default), EN: "Hello, I checked the Kikar Hamedina Towers price guide: In the towers, 140 m², floor 20,
estimate ₪8.46-9.74 million. I would like more details (nad-lan.co.il)". FR, RU and AR send the same message in their language
with their own number format.

## (6) Terms I was not sure of

- **"רובע 4"**: EN "District 4", FR "district 4", RU "район 4", AR "المنطقة 4". None of the live twins names Tel Aviv's districts,
  so there is no site precedent; "New North" (the neighbourhood name the twins use) would be a different, smaller area.
- **"מחיר שיווק"** (kind `mkt`): EN "Marketed price", FR "Prix de commercialisation", RU "Цена в проекте", AR "سعر التسويق".
  The Russian is the least settled: the usual phrase names the developer, a word the RU page bans.
- **"חציון" in Arabic:** the live AR page writes "الوسيط", which is also the word for a broker; the files use "القيمة الوسيطة"
  everywhere, so a pill reading "median" can never read as "broker".
- **"מחירון"**: rendered as "price guide" / "repères de prix" / "обзор цен" / "دليل الأسعار", because each twin states that the
  project has no official price list ("official price list", "grille tarifaire officielle", "قائمة أسعار رسمية").
- **"דירה נוספת"** (purchase-tax choice): translated as "additional apartment" and equivalents. For EN, FR and RU readers abroad,
  a foreign resident pays this same schedule (the EN twin says so); a label such as "Additional apartment or foreign resident" would
  guide them better, but it says more than the Hebrew, so it is left for the owner's word.
- **"שמאים"**: EN "appraisers", FR "experts immobiliers", RU "оценщики", AR "مخمّنين عقاريين".
- **French "dans l'ancien"** for existing (resale) buildings and "rez-de-jardin" for a garden apartment: the usual French market words.

## Seen in the component itself (render.py, not changed here)

1. **A wrap is always possible right after a number island** (inline-block): a unit or "%" can start a new line, and a no-break
   space there shows as a leading space. The data files work around it; a structural fix would keep the unit inside the island.
2. **The caption wraps word by word on phones** once the list is opened ("Repères / de prix", "Обзор / цен", "دليل / الأسعار");
   the Hebrew caption is one word, so it never showed. Likely the caption of the block-displayed table shrinking to fit.
3. **On phones, the low and high price labels overlap** in the comparison chart when the range is narrow (63,000 and 68,000 print
   on top of each other for "new building nearby"). This depends only on the numbers, so the Hebrew section has it too.
4. **EN puts ₪ before the number** (the English page's style), so a line can end on a lone "₪" before the number island.
