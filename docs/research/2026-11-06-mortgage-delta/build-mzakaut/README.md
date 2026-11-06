# Two new tools for /mortgage-calculator/: "מחשבון זכאות משכנתא" (mzakaut) and "ריבית נומינלית וריבית אפקטיבית" (mnomeff)

HAD-675, mortgage delta rows A1, A2 and A8 (`../delta.md`). Built 6.11.2026, **local only**: nothing deployed, nothing committed,
no live write, no existing file edited (`inc/instruments.php` untouched). Every number of the eligibility tool comes from
`../eligibility.md` (gov.il pages S1 to S17, read 6.11.2026).

## Files

| File | What |
|---|---|
| `plugins/nadlan-config/assets/instruments/tools/mzakaut.js` | The eligibility tool (id `mzakaut`), Hebrew only, RTL. Pure logic in `window.NLZK`. Holds no amount of its own. |
| `plugins/nadlan-config/assets/instruments/data/zakaut.json` | Every table and amount, each block with its source id; `sources` S1 to S17 with URL, publish and update dates; `"checked": "2026-11-06"`; `unverified` lists what is kept off the page. |
| `plugins/nadlan-config/assets/instruments/tools/mnomeff.js` | The converter (id `mnomeff`), Hebrew only. Pure logic in `window.NLNE`. Reads `boi-mortgage.json` (by_bank). |
| `build-mzakaut/registry.php.txt` | The exact PHP: two entries for `nadlan_nli_tools()` and two branches for `nadlan_nli_summary()`, plus the switcher chips and panes. Linted (php -l, PHP 8.3). |
| `build-mzakaut/test_mzakaut.js` | Node test, 72 assertions, literals worked out by hand from the official tables. Last run: `test_mzakaut.out.txt`. |
| `build-mzakaut/preview.html` | Local mount exactly as the shortcode prints it, inside panes `#tool-zakaut` and `#tool-nomeff`. `?theme=1` adds the live theme stylesheets (read only). |
| `build-mzakaut/verify.py` | Playwright (Chrome, headless): starts `http.server` on 127.0.0.1:47986 itself and stops it in `finally`. 171 checks. Last run: `verify.out.txt`, `verify.json`, `shots/`. |

Run: `node docs/research/2026-11-06-mortgage-delta/build-mzakaut/test_mzakaut.js` and
`python docs/research/2026-11-06-mortgage-delta/build-mzakaut/verify.py` (from the repo root).

## Results (6.11.2026)

* Node: **72 of 72** passed.
* Browser: **171 of 171** passed at 390x844 (is_mobile) and 1280x900, plus a phone pass under the live theme: all eight profiles
  pressed, each headline equal to `NLZK` on the same values; zone א / ב, reserve, 10 פלוס, Negev, rate and term, marriage date,
  a bad value, the under-599 family; the converter both ways and a chip. No console error or warning, no horizontal scroll, every
  visible control at least 44 px, every input and select labelled, every group named. Under the live theme the only console
  errors were the theme's own Heebo fonts refusing a 127.0.0.1 origin (CORS), filtered by URL.
* Screenshots looked at (eyes): `shots/page-default-1280.png`, `mzakaut-family-390.png`, `mzakaut-olim_family-390.png`,
  `mnomeff-390.png`. Fixed after looking: the total row lost its padding (specificity), a "(" was left alone at a line end before
  source links, "+270" showed as "270+" in RTL, the two formulas shared one wrapped line, and on desktop the rules, process and
  links now fill the column under the result instead of leaving it empty.
* `registry.php.txt`: `php -l` clean; both summaries rendered against the real data files with WordPress stubs (below).

## Worked examples (by hand from the official tables; all in the test)

| Case | Points | Amount |
|---|---|---|
| Family, married 3 years, 2 children, siblings 2 and 4, service 24 + 20 months (the opening example) | 350 + 500 + 100 + 400 = **1,350** | band 1,000 to 1,399: 62,400 + 44 x 624 = **89,856 ₪** |
| The same with siblings summed (zakaut.com's error) | would be 350 + 500 + 650 = 1,500 | would be 85,250: the test asserts we do NOT do this |
| The same in zone א | 1,350 | 1,500-point amount 85,250 + 44 x 852 = 37,488 + 100,000 at 4.5% / 20 years (first payment 633) = **222,738 ₪** |
| The same, reserve 90 full days for one spouse | 1,350 | + 3% of 62,400 = 1,872: **91,728 ₪** |
| Veteran single aged 35, no siblings | 300 + 3 x 50 = **450** | below the S3 table: points only, "אין שורה בטבלת הסכומים" |
| Veteran single aged 35, 4 siblings | 450 + 400 = **850** | 54,240 (labelled unverified) |
| Olim family, second year (1 full year), 2 children | 250 + 500 + 730 = 1,480, floor **1,800** | 117,985 (labelled) |
| Olim family, 7 years, 3 children | 550 + 650 + 730 = **1,930** | 128,930 + 28,370 at 3% / 28 years = 157,300 (labelled) |
| Family under 599: married 1 year, no children, 1 + 1 siblings | 250 + 50 + 50 = **350** | "אין הלוואה לפי הניקוד" (never "0 ₪"); in zone א only the 100,000 |
| Single parent | 2,200 (S5) | 161,665, equal to the S5 amount |
| Family 12 years, 3 children, 10 פלוס all yes | 800 + 650 = 1,450 | 74,350 + 132,000 = 206,350; in a priority zone 10 פלוס needs 4 children |
| Rate typed from a certificate, 2.5% for 30 years on 89,856 | | first payment 355.04 ₪ |
| S8 consistency | | 100,000 / 70,000 at 4.5% / 12 for 240 months = 632.65 / 442.85, matching S8's 633 / 443 |
| Converter | | 4.5% nominal = 4.5940% effective; 4.5% effective = 4.4098% nominal; all-banks fixed not linked 9.2026: 4.7162% effective = 4.6172% nominal |

## How mzakaut decides (and where it reads the official text one way)

* Points: S3 (veteran families, siblings per spouse), S11 (olim families: seniority, children, +730, floors 1,700 / 1,800),
  S5 (single parent 2,200), S4 (singles by age, cap 1,690), S12 (olim singles +600 / +400, cap 1,690), S10 (disability).
* **Our readings, each said on the page or in the code, to confirm with the ministry if a reader asks:**
  1. The 1,690 cap of singles is on the total (age + siblings), since the disability maximum is 1,690 + 200 = 1,890.
  2. Disability: +200 after the profile's own floor or cap, then the S10 floor (1,700 + 200 = 1,900 matches the olim degree א'
     floor, which supports the order). "נכה רתוק לכסא גלגלים" is the veteran-family case S10 names (2,200); singles go to
     "נכה רווק", olim families to "משפחת נכים" with "גם משפחת עולים".
  3. Service supplement = months x the S7 per-month amount of the band actually used; in zone א that is the 1,500-point band,
     since S7 says 1% of the basic loan. Each spouse at most 36 months (the S16 code), civic service 12 (S7).
  4. The 46% / 65% cap of S7 is applied to compulsory service and reserve together.
  5. A veteran family below the table in zone א: only the 100,000 locality supplement is added; S3 does not say whether its
     "1,500 points at least" rule applies below 599, so that amount is not added and the page says so.
  6. Singles in a priority zone: S8 prints only their first payment (317 / 222), so it is shown and no amount is added.
  7. Olim supplement from 5 full years (S11 "5 to 6 years", "more than five years").
  8. 10 פלוס: the three conditions are yes/no questions with the S9 income table; the children rule is checked from the
     children field (2, or 4 in a priority zone).
* Headline: shekels for veteran families and the single parent; **points** for singles and olim, with the shekel figure in the line
  under it labelled "לפי טבלת הסכומים למשפחות ותיקות (S3); לבדוק בתעודת הזכאות".
* The rate: the rule in words only ("0.5% מתחת לממוצע הצמודות של בנק ישראל, ולא יותר מ־3%", S2). An optional field takes the
  rate printed on the certificate and gives the first payment (Spitzer, rate / 12, index unchanged); empty by default.
* Every line carries its source chip ("S3 · עודכן 30.3.2026"), linked to the gov.il page. Below: terms (S2, S17), the process (S2),
  the official pages S1 to S14 with dates, the official calculator (S1), and our pages (#mortgage-tool, /dira-behanacha/,
  /mortgage-calculator/mortgage-interest-rates/, /mortgage-advisor/). The binding line (S1) and the copy button sit under the result.
* No form, no request of its own (the test greps for fetch, sendBeacon, XMLHttpRequest and form).

## Still unverified (kept off the page or labelled)

1. The current eligible-loan rate (the Bank of Israel page answered with a CAPTCHA): no number anywhere.
2. Whether singles and olim use the S3 amount table: their shekel figure is labelled.
3. The olim singles' seniority ladder (not on S12): S11's ladder, labelled on the line.
4. The Negev amount per locality: the 48,000 to 84,000 range in words, never in a total.
5. The "חסרי דירה" definition, the 75% financing cap, the registration fee (60 / 70): not shown.
6. The reserve unit (S2 "per 15 full days" vs S7 "0.5%"): S2's unit, the difference printed on the line.
7. S10 degree ב' singles: 2,000 used; the page's own 2,200 example is printed in the help line.
8. The priority-zone locality list (S15, not opened): the reader picks zone א, ב or none; the list is linked.
9. Our readings 1 to 8 above.

## Server summaries (rendered with stubs from the real data, 6.11.2026)

* mzakaut: "הלוואת זכאות של משרד הבינוי והשיכון: למשפחה ותיקה הניקוד נקבע לפי שנות הנישואין (30 נקודות בשנה הראשונה, 250 אחרי
  שנה, ועוד 50 לכל שנה), מספר הילדים (350 לילד אחד, 500 לשניים) ומספר האחים והאחיות של כל אחד מבני הזוג בנפרד (50 לאח אחד, 400
  לארבעה). המשכנתא הבסיסית לפי קבוצת הניקוד: מ־54,240 ₪ (599 עד 999 נקודות) ועד 161,665 ₪ (2,200 נקודות ומעלה) ..." (full text in
  the branch; every number read from zakaut.json at render time).
* mnomeff: "... למשל 4.50% נומינלית הן 4.59% אפקטיבית, ו־4.50% אפקטיבית הן 4.41% נומינלית. ... בקבועה לא צמודה ב־9.2026 הייתה
  4.72%, שהן 4.62% נומינלית ..." (numbers from boi-mortgage.json via `nadlan_nli_mrates()` and `nadlan_nli_mr_nom()`).

## Release steps (not done)

1. Paste `registry.php.txt` parts (1) and (2) into `inc/instruments.php`; ship the two tool files and `data/zakaut.json`.
2. Add the two chips and panes to the page switcher (`tool-zakaut`, `tool-nomeff`; markup in the snippet header). Where the chips
   go and their wording on the live page are the owner's call (delta.md row A2 suggests the switcher; a separate page needs his word
   and the URL word audit).
3. After release: source audit of the raw HTML, content_first_check, and the press-through in the owner's Chrome.

## Design

Palette of the instruments system: ink #12202A, ink-2 #3E4C58, mute #5E6A75, line #D3DCE2, sea #2F6F86, sea-deep #1F4B5C, ground
#F6F8F9, error #C42550; IBM Plex Sans Hebrew for text, IBM Plex Mono for numbers and the source chips. Why not the default look: the
surface is a government record read line by line (each line stamped with its gov.il page and date, a ruled ledger, a hard 2 px
rule above the result), no cream, no brass, no soft cards, no gradient. All CSS id-scoped (`#nlzk`, `#nlne`) with `!important`
on type, buttons, inputs, lists and tables, as the theme restyles plain elements.
