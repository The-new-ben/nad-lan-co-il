# HAD-534 (d): the soil engine in English, left to right (patch plan, 21.10.2026)

Staged only. Nothing published, nothing committed, nothing written into `plugins/nadlan-config/`.
Base = the live files of release 1.72.475 (local plugin copies are byte-identical to live: core.js 24cc3837, core.css ffc57ec5,
soilmap.js a09461ae, pfas.js f7609932, soilask.js ecd75b65, data/sde-dov-soil.json af01fa53; instruments.php 2e285af4 local).
Full patched copies: `docs/tools/soil-en/patched/` (same tree as the plugin). Applying = copying the six files over the plugin.

## How it works (one paragraph)
`inc/page-lang.php` already prints `<html lang="en" dir="ltr">` on every page under the `/en/` root and pairs hreflang by path
(`/sde-dov/contamination/` <-> `/en/sde-dov/contamination/`). The engine reads that: core.js takes the language from
`<html lang>`, every tool picks its strings from a `{he, en}` table, and PHP prints each tool section with `dir="ltr" lang="en"`,
English summary, English related links and English JSON-LD, but only for a tool whose registry entry has an `en` block (today:
soilmap, pfas, soilask). Any other tool on an English page stays Hebrew and RTL, never half-translated. Hebrew pages: output
unchanged (proved below), with one deliberate fix in the Hebrew letter.

## inc/instruments.php (207 -> 257 lines)
| live line | change |
|---|---|
| after 47, 53, 59 | registry: an `'en' => array(name, kicker, desc, related)` block in `soilmap`, `pfas`, `soilask`. Related links point to live English pages only (all checked 200 on 21.10): `/en/sde-dov/`, `/en/sde-dov/prices/`, `/en/north-tel-aviv/`, `/en/buy-property-in-israel/`, `/en/guides/new-apartment-sale-specification/`. |
| after 72 | new `nadlan_nli_lang()` ('en' when `nadlan_pglang_lang()` says en), `nadlan_nli_tool_lang($t)` (en only if the tool has an `en` block), `nadlan_nli_t($t,$lang)` (merges the `en` block over the Hebrew). |
| 100 | fonts: on English pages enqueue `IBM Plex Sans 400/500/600 + IBM Plex Sans Condensed 600 + IBM Plex Sans Hebrew 400 + IBM Plex Mono 400/500`; Hebrew pages keep the exact current URL. |
| 111 | `nadlan_nli_summary( $id, $lang = 'he' )`, first line returns `nadlan_nli_summary_en( $id )` for en. |
| after 165 | new `nadlan_nli_summary_en()`: the same numbers from the same data file, in English (soilmap: paragraph + 7-row table; pfas: paragraph; soilask: the questions). Date with `gmdate('j M Y', strtotime($built . ' UTC'))`: `date_i18n` would print Hebrew month names, and without ' UTC' a non-UTC PHP zone printed "14 Oct". |
| 171-176 | shortcode: `$lang = nadlan_nli_tool_lang()`, `$t = nadlan_nli_t()`; section `dir="ltr|rtl" lang="en|he"`; default kicker Calculator/מחשבון; related nav "Related:" / aria "Related tools and guides" in English (Hebrew strings unchanged). |
| 198-200 | JSON-LD: `name`, `description` from `nadlan_nli_t()`, `'inLanguage' => $lang` (was hard-coded 'he'). The FAQPage regex (line 186) already accepts `<h2>Frequently asked questions</h2>`; the English page uses exactly that heading (6 Q parsed). |

## assets/instruments/core.js (176 -> 203 lines)
| live line | change |
|---|---|
| 3 | header note. |
| 7-14 | `LANG` from `<html lang>` (`/^en\b/`), `LOC` = en-US / he-IL for every `Intl.NumberFormat` (lines 7, 10, 11), `MON` month names; `fmt.month` -> "Oct 2026", `fmt.date` -> "15 Oct 2026" on English pages (Hebrew "15.10.2026" unchanged). New table `TX` (14 strings, he/en), `langOf(node)` (the closest `[lang]`, i.e. the tool section), `pick(tx, lang)`. |
| 24-57 (field) | 'הסרת שורה ' / 'הוספת שורה' from `st.t`. |
| 88-89 (mount) | `lg = langOf(root)`, `T = pick(TX, lg)`; `root.setAttribute('dir', lg === 'en' ? 'ltr' : 'rtl')` (was always rtl). |
| 101, 110, 130, 141, 146 | example badge + note, calc error, scenarios aria, "full breakdown" summary, "Sources:" from T. |
| 137 | `r.docDir` / `r.docLang`: a generated letter can carry its own direction (a Hebrew letter inside an English page). |
| 149-156 | share bar: Copy the result / Copied / Send on WhatsApp / Print or save as PDF. Share text logic unchanged (the result text is the tool's, already English on English pages; `bare` letters still go out without our link). |
| 171 | "data did not load" in the root's language. |
| 174 | `NadLanInstruments.lang`, `.langOf`, `.pick`, `.TX` exported (the tools read `.lang`). |

## assets/instruments/core.css (136 -> 154 lines; lines 1-136 untouched)
Appended block (18 lines) scoped to `.nli[dir="ltr"]` / `.nli[lang="en"]`: direction ltr; Latin faces as tokens
(`--nli-sans: IBM Plex Sans`, `--nli-display: IBM Plex Sans Condensed`, title 600 36/40, phone 30/34); inputs and select
left-aligned; the big figure, scenario and strip figures left; `dl` values right; table headers left, numeric cells right;
the letter `pre` LTR, but `pre[dir="rtl"]` stays RTL in Plex Sans Hebrew; the map popup LTR.
Design line (owner law 13.10): palette unchanged, NadLan Instruments survey palette (ground #F6F8F9, ink #12202A, sea #2F6F86,
survey #C42550 for the one deciding number); faces IBM Plex Sans + Plex Sans Condensed + Plex Mono, the Latin side of the Plex
family the Hebrew already uses, so one survey-instrument voice in both scripts. Not Inter, not Space Grotesk, no serif, no cream.

## assets/instruments/tools/soilmap.js (194 -> 303 lines)
- 11-25: `BIN` labels, `ST`, `NOTE` move into tables: `TX` (70 strings, he/en, `{name}` placeholders), `NOTE` per plot {he,en},
  `DATA_EN` (Hebrew values of the data file -> English: 21 plot uses, 3 stages, 9 project facts, plan "תמ"ל3001", the threshold
  label, the sources line). `EN` from `NadLanInstruments.lang` (safe in node: no document access before line 145).
- 39-42: `xs()` = "598×" in English ("פי 598" in Hebrew); date range "5 May 2026 to 26 May 2026".
- 72-87: the whole surface from T (kicker, title, lede, strip "60 of 101", search label/placeholder, chips " · project in marketing",
  legend, note, table, sources line); stage and use cells through `tr()`.
- 90-119: plot card (Plot N, uses, m², badges, peak, "at a depth of 10 m", PFOA, Sampling/Report rows, approx note, developer
  statements, phase line with the English "Project in marketing" prefix stripped by `T.mktPrefix`, report link labelled
  "(Hebrew PDF)") and the WhatsApp "Ask for details" text in English (same number 972525101555, nothing collected).
- 134-136, 145: search hint / not found / map failed.
- 151: MapLibre cooperative-gesture texts in English; 152: navigation control top-right on English pages (top-left in Hebrew).
- 180-182: borehole popup in English (local var renamed from `f` to `p`; `f()` is now the template filler).
- The RTL text plugin stays loaded on English pages: the OpenFreeMap base map labels streets in Hebrew.

## assets/instruments/tools/pfas.js (44 -> 87 lines)
- 9-12: `TX` (33 strings), `LABEL_EN` (threshold label), `xs()` "598×" / "12% of the threshold".
- 15-40: kicker, title, lede, fields (units shown as ng/kg, µg/kg, mg/kg), error, answer, lines, note, formula, source label
  "(Hebrew PDF)", share text, comparison table; all from T. Logic unchanged (the soil and PFAS checks of test_tools.js pass on the patched copies).

## assets/instruments/tools/soilask.js (63 -> 153 lines)
- 11-36: the letter becomes `letter(rec, plot, stage, form, lang)` with `LX.he` / `LX.en` (same seven questions, same opening
  per status, WhatsApp keeps questions 1, 2, 4, 5). `lang` defaults to he, so `NLAX.letter` callers are unchanged.
- FIX (also on the Hebrew page): live line 15 printed `' ב־' + dmy(report)` whenever `report` was set, and `dmy()` returns ''
  for partial dates, so the live letter for plots 2206 (the default!), 2255, 2270, 2701 and 822 reads
  "...במאגר המשרד להגנת הסביבה ב־, נמצאה...". Now the date is left out when it is partial. 20 of 60 Hebrew letter variants
  change, each only by that fragment (node check below).
- 40-61: interface from `TX` (24 strings; the letter itself 32 in `LX`); on English pages a fourth field "Letter language: English / Hebrew (for the
  developer)"; a Hebrew letter on the English page returns `docDir: 'rtl'` (core prints it right to left). The note links
  `/en/buy-property-in-israel/` (there is no English lawyer page).

## Verification done (local, 21.10.2026)
- `php -l` on the patched instruments.php: clean. PHP render of the three shortcodes + JSON-LD with stubbed WordPress:
  Hebrew output byte-identical to the live module (9,239 bytes); English output has 0 Hebrew letters, `inLanguage: en`,
  FAQPage with 6 questions from page-en.html.
- node (scratchpad test): stats 7 reports / 101 holes / 60 over, x597.97, mg conversion, `bin()` equal to live; every TX
  entry has he+en; every Hebrew value in the data file has an English entry; English letters carry no Hebrew.
- Playwright, `python docs/tools/soil-en/press_soil_en.py`: Hebrew text of all three tools, live files vs patched files:
  identical (soilask only the date fix). English phone 390 and desktop 1366: map canvas drawn, all three sections LTR,
  title in Plex Sans Condensed, 0 px horizontal overflow, 0 console errors, 0 Hebrew letters in the tools; chip 2206, a
  project chip (plot 150), search 2227, search "abc", PFAS 0.127 mg/kg = 20×, letter switched to Hebrew = `dir="rtl"`.
  Screenshots: `docs/tools/soil-en/shots/en-*.png` (looked at: soilmap d+m, pfas m, soilask m, Hebrew letter d).

## Release steps for the main session
1. Copy the six files from `patched/` into `plugins/nadlan-config/` (same relative paths), bump the version, run
   `node tools/instruments/test_tools.js`, release through the runner. After it: the live Hebrew page 8406 must read the same
   (source_audit diff on `/sde-dov/contamination/`: only the version strings), and the default letter loses " ב־,".
2. Create the page: `copy docs\tools\soil-en\page-en.html docs\tools\soil-en\page.html`, then
   `python scripts/project-stage/create_tool_page.py soil-en --dry` and without `--dry`. meta.json: parent 8342 (`/en/sde-dov/`),
   slug `contamination` (free: `/en/sde-dov/contamination/` is 404 today), tools soilmap/pfas/soilask, Yoast title/description,
   an English forbid list (company and project names, "contaminat", "pollut", "toxic", ...) for update_tool_page.py.
3. Purge the cache of `/sde-dov/contamination/` so its hreflang cluster shows the English twin (page-lang.php clears its
   transient on save; the page cache does not know).
4. Optional, one line, one page: link `/en/sde-dov/` (8342) to the new page, as the Hebrew hub links 8406.

## Open points to state to the owner
- The data is as of 15.10.2026 (`built`); the English page says "Data as of 15 October 2026". If a report was added since,
  rebuild the data first and update both pages' numbers together.
- "Project in marketing" kept literally per the brief; "a project now selling" would read more naturally to a foreign buyer.
- The URL keeps the word "contamination" because the hreflang pairing in page-lang.php needs the same path as the Hebrew page;
  the visible English copy never uses it (gate in meta.json).

## Research record (page research law, 21.10.2026)
- URL: `python tools/gsc/url_word_audit.py` logic on the live sitemaps (4,571 URLs): `/en/sde-dov/contamination/` has no word
  twice; "contamination" is owned only by its Hebrew twin `/sde-dov/contamination/`; "soil", "pfas", "tests" are owned by no URL;
  language twins follow the existing pattern (`/en/sde-dov/`, `/en/sde-dov/prices/`, children of the en root 5011).
- English SERP (DataForSEO live, 21.10.2026 ~16:45 UTC): "sde dov pfas soil" (Israel, en) and "sde dov contamination" (US, en).
  Both show an AI overview (asynchronous, content not retrieved). Organic: gov.il Hebrew page `gov.il/he/pages/sde_dov`, the
  gov.il English news item "Preliminary Findings of PFAS Compound Contamination in the Soil and Groundwater at the Sde Dov
  Site", a Kan news video (Aug 2026), old airport-closure articles, generic PFAS research. No English page has a plot map,
  per-plot values, a calculator or a buyer letter. Volumes: keywords.csv (15.10) shows no data for the English phrases.
