# /sde-dov/prices/ (page 4758): price-number audit against sourced data (HAD-460, 7.10.2026)

Read-only audit. Nothing on the live site was changed. The live page was fetched with a public GET
(`https://nad-lan.co.il/sde-dov/prices/?nlcb=1791366288`, HTTP 200, 234,807 bytes, 2026-10-07 09:44:48 UTC); the post's
`article:modified_time` is 2026-10-06T12:55:54Z, while the visible footer says "עודכן יוני 2026". No FAQ or other
structured data on the page carries a price (JSON-LD = WebPage, WebSite, Organization only).

The sourced data is the new data file `scripts/project-stage/price_guide/sde-dov-prices.json` (its `sources` block holds
every URL, what it says and when it was read). Source keys below refer to it.

## Summary

21 distinct price claims (most of them repeated across several sections; occurrence counts per claim in the table below):

| verdict | count |
|---|---|
| CONSISTENT | 4 |
| CONFLICTS | 8 |
| UNSOURCED | 9 |

Two non-price counts were also checked: "כ-16,000 דירות" CONSISTENT (NC2604, BZ2606); "כ-11,000 דירות בתהליכי הקמה" UNSOURCED.

The headline figure of the article, "about 81,000 ₪/m² at the start of 2026" (10 occurrences, including the FAQ answer),
is not what any source says: the developers' survey gives about 83,000 (and ice's headline "almost 82,000"). If the
PriceGuide goes on this page as built, its tile (83,000) and the article (81,000) will disagree on screen.

## Every price claim

Occurrences = how many times the number appears in the page body (live.txt extract).

| # | claim on the page (short quote) | sections | occ. | verdict | evidence (source key, date) |
|---|---|---|---|---|---|
| 1 | "המחיר הממוצע למ״ר ... סביב 81,000 ש״ח" (start of 2026) | opening, מחיר למ״ר (text + table), פרמיית קו ראשון, השוואה (text + table), תחזית, איך לקרוא, FAQ x2 | 10 | **CONFLICTS** | NC2604 (15.4.2026) and ICE1904 (19.4.2026): Sde Dov average about 83,000 ₪/m², about 1,280 units; ICE1904 headline "almost 82K"; ICE0305 (3.5.2026): "about 83K". 81,700 is Rainbow's own average (NC2604), not the quarter's |
| 2 | "טווחי הפריסייל נעים בדרך כלל בין 70,000 ל-100,000" | opening, מחיר למ״ר (text + table), פרמיית קו ראשון (table), השוואה (text + table), פריסייל, FAQ | 8 | **CONFLICTS** | 2026: most projects about 70K, some at 60K (ICE2105, 21.5.2026); two 5-room deals at 54,200-57,300 (ICE0305, 3.2026); one Eshkol project's recent deals 60-62K (ICE2105); survey range 60,200-138,000 (NC2604, 4.2026); official prices 75-85K (BZ2606, 6.6.2026). The lower bound is too high and the upper bound too low |
| 3 | "דירות עם נוף לים משווקות סביב 90,000 ש״ח למ״ר" | opening, table x2, פרמיית קו ראשון, איך לקרוא, FAQ | 7 (the other 2 are Park Tzameret, #21) | **CONFLICTS** | BZ2512 (18.12.2025): units facing the sea or in the central buildings sell at 75-80K "and more". 90K appears only as a developer's announced price or aim (ice 28.5.2025; ICE2510, 26.10.2025); that seafront project sold presale at 71K (ICE2510) and averaged 75,520 in 2025 (NC2604) |
| 4 | "ולעיתים עד 100,000 ש״ח למ״ר" (sea view, the ceiling) | opening, tables, FAQ | 6 (plus 8 inside the #2 range) | **CONFLICTS** | Published deals above 100K: tower floors 38/39/43 at about 107,700-119,200 on the built area (BZ2512, 12.2025, CALC); Ashira penthouse about 103,000 (BZ2408, 8.2024); survey maximum 138,000 (NC2604). A developer's "90-100K for select units" (ICE2512, 12.2025) supports 100K only as a typical upper end, not as the ceiling |
| 5 | "המחיר הממוצע הצפוי לעסקה ... סביב 7 מיליון ש״ח" | opening, table x2, עסקאות שיא table, מימון x2, מס, FAQ | 7 | **UNSOURCED** | No source. Published averages per unit: Rainbow 8.67M (ice 27.8.2025), FIRST 8.36M (NC2507, 7.2025) and about 7.7M on its linear track (ice 12.4.2026); 4 rooms 9.45M (NC2604) |
| 6 | "כ-75,000 ש״ח למ״ר" (the expected average behind the 7M) | table, עסקאות שיא table, FAQ | 3 of 5 | **UNSOURCED** | No source for a quarter-wide expected 75K. Nearest: FIRST's 2025 average 75,520 (one project, NC2604); a journalist's "70-75K this year" for large companies (ICE2510, 10.2025) |
| 7 | "הממוצע עלה מכ-64,700 ... לכ-81,600 ש״ח למ״ר לאחר גל מכירות" | מחיר למ״ר, פריסייל | 2 | **CONSISTENT** | BZ2606 (6.6.2026): a joint project (taken as 'זוהי תל אביב'), Q1 2026 about 64.7K incl. VAT, 8 units after the quarter about 81.6K. The page omits that the sample is 8 units and that net of the financing component the figures are 60.9K and 76.8K |
| 8 | "הערכות של חברות בנייה ... 64,000 עד 75,000" | מחיר למ״ר (text + table) | 2 | **UNSOURCED** | No source. Nearest: Dimri's value for its unsold stock, 73.2K incl. VAT (BZ2606) or 62K before VAT (GL2609); the survey's 63.4K-82.6K are sales averages, not estimates |
| 9 | "בניין בוטיק מסוים ... החל מכ-53,500" | מחיר למ״ר table, פרמיית קו ראשון table | 2 | **UNSOURCED** | No Sde Dov source. Nearest: the cheapest listed VOGUE unit about 54,500 (ICE2510, 10.2025, a 20-floor building, not boutique); two 3.2026 deals 54,200-57,300 (ICE0305). The only 53,500 in the repo's research is DUO's cumulative before-VAT average (docs/content/wave1/duo-tel-aviv-content-package-2026-08-04, outside Sde Dov) |
| 10 | "דירות 2 חדרים ... כ-46.8 מ״ר ... כ-3.81 מיליון" | לפי גודל (text + table), עסקאות שיא table, משקיעים | 6 (3.81) | **UNSOURCED** | No Sde Dov source. The only "3.81M" found is Israel Canada's Midtown Jerusalem average per unit (ice 28.5.2025 and 27.8.2025). Sourced Sde Dov 2-room prices: 2.8-3.1M ('זוהי תל אביב', ICE2105, 5.2026), 54 m² at 3.665M (ICE0305), VOGUE list 2.979-3.501M (ICE2510), Dimri from 3.75M (NC2512 in dimri json), Ashira from 3.9M (3.2024) |
| 11 | "מחיר גלום של כ-81,410 ש״ח למ״ר" (2 rooms) | לפי גודל (text + table) | 2 | **UNSOURCED** | Derived from #10 |
| 12 | "דירת 3 חדרים סביב 6.86 מיליון" | לפי גודל table, FAQ | 2 | **UNSOURCED** | No source. Sourced 3-room figures: 4.6-4.8M for 82-83 m² ('זוהי תל אביב', ICE2105, 5.2026); Ashira launch from 5.4M (3.2024); Rainbow 98 m² over 8M (9.2023) |
| 13 | "דירת 4 חדרים סביב 9.45 מיליון" | לפי גודל (text + table), מס, תחזית, FAQ | 5 | **CONSISTENT** | NC2604 (15.4.2026), ICE1904, ICE0305: 4 rooms average about 9.45M. Undated on the page |
| 14 | "דירת 5 חדרים סביב 11.61 מיליון" | לפי גודל (text + table), מס, תחזית, FAQ, משקיעים | 6 | **UNSOURCED** | No source. Sourced 5-room figures: VOGUE list 139.7 m², floor 18, 11.954M (ICE2510, 10.2025); two 132 m² deals 7.16-7.57M (ICE0305, 3.2026); 126 m² 7.727M (ICE0305); Ashira from 9M (3.2024) |
| 15 | "העסקה הזולה ביותר ... 2.3 מיליון ש״ח לדירת 32 מ״ר" | לפי גודל, מתחם (text + table), עסקאות שיא (text + table), משקיעים | 6 | **CONFLICTS** | The only published 32 m² deal: Rainbow tower, floor 4, 1 room, 3.1M, 7.2023 (Tax Authority data in Globes 29.11.2023, GL2311 in rainbow json). The survey's cheapest per m² is 60.2K for a 40 m² 2-room (NC2604; CALC about 2.41M) |
| 16 | "עסקת שיא של כ-43.75 מיליון ש״ח לדירת 508 מ״ר במתחם אשכול" | לפי גודל, מתחם (text + table), עסקאות שיא (text x2 + table) | 6 | **CONFLICTS** | BZ2512 (18.12.2025) and NC2604F (13.4.2026) both call the FIRST floor-38 sale (more than 42M, about 390 m² + 200 m² balcony, 12.2025) the largest or most expensive deal so far in the quarter. No source found for 43.75M / 508 m². (Rainbow's 2024 purchase of several apartments for about 50M, about 550 m² to be merged, GL2407 in rainbow json, is a multi-unit purchase) |
| 17 | "FIRST ... כ-94 ועוד 8 דירות בכ-853 מיליון ... כ-8.4 מיליון ש״ח לדירה" | מתחם, איך לקרוא | 2 | **CONSISTENT** | BZ2512 (18.12.2025) and NC2507 (17.7.2025): 102 units (incl. join requests and options) for 853M, 8.36M each. Dated 7.2025, undated on the page; the paragraph reads as if FIRST were in Eshkol, while ICE1904 lists Hagag among the Central-compound projects |
| 18 | "יגאל דמרי ... 150,000 ש״ח למ״ר" | תחזית, FAQ (h3 + answer) | 4 | **CONSISTENT** | https://www.nadlancenter.co.il/article/11668 (3.3.2025, read 7.10.2026 09:48 UTC): said at a conference, "in a decade or two". The page omits the date and the 10-20 year horizon |
| 19 | "ממוצע מחיר למ״ר בתל אביב ... כ-55,000 עד 60,000" | השוואה (text + table) | 2 | **CONFLICTS** | The site's own Tel Aviv-Yafo figure, shown on every Tel Aviv project page and in the new PriceGuide's comparison row: median 52,856 ₪/m² (Tax Authority deals 10.2023-10.2025, TA). No source for an average of 55-60K was found (median vs average differ, so the conflict is one of alignment) |
| 20 | "ברמת אביב ... 55,000 עד 70,000 ש״ח למ״ר" | השוואה (text + table), FAQ | 3 | **CONFLICTS** | ICE0606 (6.6.2026): Ramat Aviv recent deals average around 55K, older Ramat Aviv Gimmel buildings 40-43K; https://www.bizportal.co.il/realestates/news/article/20036053 (2.8.2026, read about 09:50 UTC): Ramat Aviv Gimmel average 51-53K. 70K appears only in single new-project deals nearby |
| 21 | "פארק צמרת ... 90,000 עד 120,000 ש״ח למ״ר" | השוואה (text + table) | 2 | **UNSOURCED** | No reputable dated source found (search returned listing pages only) |

## Top conflicts, in order of visibility

1. **The average (#1), 10 times:** page "סביב 81,000"; sources about 83,000 (NC2604 15.4.2026, ICE1904 19.4.2026, ICE0305 3.5.2026).
2. **The range (#2), 8 times:** page "בדרך כלל בין 70,000 ל-100,000"; 2026 sources about 70K for most projects, deals at 54-62K, survey range 60,200-138,000.
3. **The record deal (#16), 6 times:** page "43.75 מיליון ... 508 מ״ר במתחם אשכול"; two sources call the 42M+ FIRST floor-38 deal (12.2025) the largest so far.
4. **The cheapest deal (#15), 6 times:** page "2.3 מיליון ש״ח לדירת 32 מ״ר"; the only published 32 m² deal was 3.1M (7.2023).
5. **Sea-view pricing (#3, #4):** page "סביב 90,000 ... עד 100,000"; BZ2512 says sea-facing units sell at 75-80K and more, and published top-floor deals reached about 107,700-119,200 ₪/m² (12.2025).

Also: the rooms table (#10-#12, #14: 3.81M / 6.86M / 11.61M and 46.8 m²) has no source; the 3.81M matches a Jerusalem
project's average, which suggests a mix-up in the article's preparation.

## Alignment with the new PriceGuide (if placed on this page)

| the article says | the PriceGuide (sde-dov-prices.json) shows |
|---|---|
| about 81,000 average | about 83,000 (tile 1, avg_line, the chart's "שדה דב, ממוצע" dot) |
| presale 70,000-100,000 | about 70,000 for most projects in 2026; 60,200-138,000 range; 54,200-57,300 deals |
| expected 7M per deal | 4 rooms about 9.45M; calculator default 100 m² = 7-8.3M |
| Tel Aviv 55,000-60,000 | Tel Aviv 52,856 (median) |
| updated "יוני 2026" | updated 7.10.2026 |

## Findings outside this page (not edited)

- **rainbow-tel-aviv.json, dimri-yama-sde-dov.json, ashira-sde-dov.json:** the row "פרויקט חדש בתכנית ל" shows
  70,000-72,000 with "בקומות הנמוכות: 52,000-57,000". In the source (ice 21.5.2026, ICE2105) the 52-57K low floors
  belong to a new project in Program L, while "most recent sales 70-72K" belong to a project in "הגוש הגדול" (not Sde
  Dov, not Program L). The same three files' mode "פרויקט אחר ברובע" (60,000-72,000) uses that 72K as its upper bound.
  Worth a correction pass on all three (live since 1.72.43x).
- The page lists source names at the bottom ("מקורות לעיון: ...") while the research law keeps sources internal; not a
  number, noted only.

## Method and what could not be verified

- Page text: raw HTML, scripts and styles removed, from the H1 to the end of the article. Every number with ₪, ש״ח,
  מיליון or אלף was listed; repeated numbers were grouped per claim.
- Sources opened on 7.10.2026 (UTC): ice 1111582, 1109996, 1112481 and Bizportal 20033505, Merkaz HaNadlan 14303
  (09:46); Merkaz HaNadlan 12512, 14291, 11668, Bizportal 20025106, ice 1109135 (09:48); ice 1088395, 1081367, 1066851
  (about 09:49); ice 1114418, Bizportal 20036053 (about 09:50); data.nadlan.gov.il neighbourhood files 65210724,
  65210022, 65210017 and settlement 5000 (09:50, all Last-Modified 20.8.2026); Merkaz HaNadlan 12196 (09:54).
- The official neighbourhood that holds the quarter, "אזור שדה דב" (65210724), has no median in any quarter, so no
  official per-room median exists for Sde Dov itself; the per-deal government API is reCAPTCHA-protected and was not
  used.
- Not found anywhere: 43.75M / 508 m², 2.3M / 32 m², 46.8 m² / 3.81M, 6.86M, 11.61M, 53,500, 64,000-75,000 company
  estimates, 7M / 75K expected average, Park Tzameret 90-120K, 11,000 units under construction. They may come from a
  paid data source (for example a Madlan area report) that was not opened (bot checks are not bypassed); if the
  article's author has that source, it should be recorded before these numbers stay on the page.
