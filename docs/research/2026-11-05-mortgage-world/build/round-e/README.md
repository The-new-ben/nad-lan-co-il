# Round E (HAD-675): refinance break-even in `mexit`, a city default in `mquick`

Staging only, built 6.11.2026. Nothing deployed, nothing committed, nothing under `plugins/` edited. The three JS files here start
from the repo files, which equal the live files of 1.72.590 byte for byte (MD5 checked against nad-lan.co.il on 6.11.2026:
mexit `cecae653…`, mquick `f80dff3a…`, mrates-common `07a88462…`, mortgage.js, core.js and core.css also equal).
Closes two LOSE rows of `proof/proof.md`: row 13 (refinance tool, world) and row 23 (local defaults by city, world).

| File | MD5 | What it is |
|---|---|---|
| `mexit.js` | e3dc6204d21df2fc2fd2b14a66fbed82 | "כמה תעלה היציאה" + the "האם למחזר?" section in "משכנתא שכבר יש לי" |
| `mrates-common.js` | 2925adec76f5bc03bc64650173690073 | added only: `refiAvg`, `refiExisting`, two style rules (mdecision and mreplay unchanged) |
| `mquick.js` | 1b24bf3ca4b1e889b2bca401d3c0a293 | v4: the city select in "לפי מחיר והון עצמי" (CRLF line ends, like the original) |
| `test_mrates.js` | 9c7f40a4d87f8c28d9979c42eaa133e2 | the 50 original checks unchanged + 28 new: **78 of 78 pass** |
| `preview.html` | f3eadb13966eff0a879daec96a521bdb | both tools mounted like the shortcode; `?lang=en` (mquick on the /en/ mount), `?theme=1` (the live theme CSS) |
| `verify_round_e.py`, `verify.json` | | the Playwright run (headless Chrome, 390x844 and 1280x800) and its report: **104 of 104 pass** |
| `screens/` | | 18 screenshots (list at the end) |

## 1. "האם למחזר?" in mexit

Where: mode "משכנתא שכבר יש לי", a new section under the fee result (before the "later" table). The fee answer, its lines and
everything in mode "משכנתא שאני לוקח" are unchanged.

What it shows: the balance refinanced today for the months left, in the same track, at the Bank of Israel average; the new
payment; the monthly saving (or "תוספת בחודש"); the one-off costs; the months until the saving covers them; "לא משתלם כרגע" when
there is no saving (under half a shekel) or when the months exceed the months left. Costs and months only: no "מומלץ", the lead
ends with "עלויות וחודשים, לא המלצה".

Which average (the source and month are printed on the line and in the sources):
- **fixed tracks** (קבועה לא צמודה, קבועה צמודה): `prepay.nl` / `prepay.cpi` (BoI `mashfix.xls` / `pribmash.xls`), the row in force
  today, the column of the months left (the same column s.3(3) of the fee uses, so the new rate is exactly the fee's "today" average);
- **prime and the two variable tracks**: `by_bank.latest`, row `system`, the track's rate (BoI `TamInt010.xls`, month 9.2026), because
  their rate runs to the next change day, not to the end, and the term file mixes them with short fixed loans.
- Effective annual turned nominal for a monthly payment, `NLMG.ef2nom` (the page's conversion everywhere).
- The reader can type an offer in "הריבית במחזור" (it opens at the average; the line then says "כפי שהקלדתם"). A typed offer is
  dropped when the track changes, so another track opens at its own average.

Costs, only what the data verifies: the capitalization fee (`feeExisting`, unchanged), the operational fee up to 60 ILS
(`fees.operational_max`) and 0.1% for notice under 10 days (`fees.notice_rate`; a toggle "הודעה לבנק על הפירעון", counted by default,
"10 ימים ומעלה" removes it). Appraiser and file costs are not in any official file: the field "עלויות נוספות (שמאי, פתיחת תיק)" is
empty by default and adds only what the reader types. On a linked track the 1st-to-15th CPI fee is shown on its own line marked
"לא נכלל" (it is avoided by the repayment date). The fee and costs are paid up front, not added to the new loan.

Prime and variable, said on the screen: prime has no capitalization fee (Banking Order s.4, "ללא: פריים" + a note). Note for the
brief: a variable-every-5-years track is NOT fee-free by the Order; the tool keeps its existing logic (fee only up to the next change
day, none on the change day itself) and says exactly that, with the next change month (for example 11.2029).

Shared link: `#mexit=` now also carries `rf: [typed rate or null, extra, notice]`; an old link without `rf` opens as before.
Safety: if a cached old `mrates-common.js` meets the new `mexit.js`, the section is skipped and the fee works as before. Release
both files together.

### The worked example (every input and its source)

| Input | Value | Source |
|---|---|---|
| Loan | 1,000,000 ILS, fixed not linked, 25 years (300 payments), Spitzer | the tool's existing example (mexit, test section 2) |
| Loan month and rate | 11.2024, 4.88% | BoI new mortgages, BIR_MRTG_99, average fixed not-linked rate of 11.2024 (`flows`) |
| Repaid | 11.2026: 24 paid, 276 left | today |
| Balance today | 956,994 ILS (956,993.98) | Spitzer schedule at 4.88% |
| Payment today | 5,776 ILS (5,776.20) | `pmt(956,994; 4.88%/12; 276)` = the loan's own payment |
| Average for the new loan | 4.788% effective = 4.686% nominal | BoI `mashfix.xls`, column "מעל 20 ועד 25 שנים" (276 months = 23 years), in force from 19.10.2026, data 9.2026 |
| New payment | 5,671 ILS (5,671.39) | `pmt(956,994; 4.686%/12; 276)` |
| Monthly saving | 105 ILS (104.81) | 5,776.20 - 5,671.39 |
| Capitalization fee | 15,908 ILS (15,907.53) | Banking Order, lower of s.3(3) and s.3(4), no cut before 3 years (existing math) |
| Operational fee | 60 ILS | `fees.operational_max` |
| Notice under 10 days | 957 ILS (956.99) | 0.1% x 956,994, `fees.notice_rate` |
| Other costs | 0 (field empty) | not in the data |
| **Costs** | **16,925 ILS** (16,924.52) | |
| **Months** | **162** = ceil(16,924.52 / 104.81 = 161.48), of 276 left (about 13.5 years) | |

Variants (all in the tests): notice of 10 days or more: 15,968 ILS, 153 months; plus 3,000 ILS typed: 191 months (181 without the
notice fee); a typed offer of 4.20%: 47 months; a typed 4.83%: 625 months, more than the 276 left, "לא משתלם כרגע"; a 4.00% loan
from 11.2024: the average is higher, no saving, "לא משתלם כרגע"; prime at 4.50%: average 4.1477% effective (by_bank 9.2026), no
capitalization fee, costs 60 + 955 = 1,015 ILS, 5 months.

Why the fixed case takes long: s.3(3) of the Order prices the fee as the payment difference to the end of the loan discounted at
the same average, so a refinance at that average pays most of its own saving back as the fee. The tool says this in one factual
line; it does not advise.

## 2. The city select in mquick (v4)

- In "לפי מחיר והון עצמי" only, above the price and equity fields: a select "עיר (מחיר חציוני, 4 חדרים)", first option "בחרו עיר"
  (no city, the default), then "ישראל" (2,028,800 ILS, 4-6.2026), then the 24 cities of `homes.medians.city` by Hebrew name.
- Choosing one puts its median 4-room deal price in the price field and shows its quarter under the select, for example
  "חציון 1-3.2026, רשות המסים" (each city keeps its own quarter: Kfar Saba 10-12.2025). Equity stays as typed. Typing another
  price clears the city. The copy text adds the city line only when a city is chosen.
- Tel Aviv-Yafo: 5,229,800 - 400,000 = a 4,829,800 loan, 26,218 ILS a month at the 9.2026 system mix, LTV 92.4% (the existing
  "above 75%" line). With 25% equity the payment equals the page's own city table (`homes.payments`, 21,292): tested.
- English (`lang="en"`): "City (median price, 4 rooms)", "Choose a city", "All of Israel" first, cities by English name, the note
  "Median, Q1 2026, Israel Tax Authority". The data has no English names. I found no English locality names published by the Tax
  Authority (nadlan.gov.il is Hebrew; a web search on 6.11.2026 found only third-party tools), so the map is the one already live on
  the English page's market table (`inc/mortgage-market.php` `nadlan_mm_city_en`, 1.72.589): the same 25 names in the select and in
  the table. A name missing from the map would stay Hebrew with `lang="he"`.
- CSS: id-scoped `#nlmq …` rules with `!important` (select 16 px, 46 px inside a 48 px box, no own border, native arrow). Checked
  with the live theme and design-system stylesheets loaded (`?theme=1`): 16 px, 0 px border, 48 px box.
- No city = no change: in the browser, amount mode is identical to the live v3 file in text and in pixels, and price mode is
  identical in DOM once the new city block is removed (the live mquick.js was served in place of the copy for that comparison).

## 3. Verification

- `node --check`: mexit.js, mquick.js, mrates-common.js, test_mrates.js: OK.
- `node docs/research/2026-11-05-mortgage-world/build/round-e/test_mrates.js`: 78 of 78 (sections 1 to 5 = the 50 original checks,
  6 = refinance 20 checks, 7 = mquick cities 8 checks). The original `build/mrates/test_mrates.js` still passes 50 of 50.
- Browser (`python verify_round_e.py` with the repo root served by `python -m http.server 47962 --bind 127.0.0.1`): 104 of 104 at
  390x844 and 1280x800: no console errors (a favicon 404 of the test server was silenced in the preview), no horizontal scroll
  (also with the live theme CSS), the city select works in Hebrew and English, the refinance figures appear (162, then 153 with
  10 days notice, 181 with 3,000 typed, "לא משתלם כרגע" at 4.83%, prime and variable notes), focus stays in the field while typing,
  every control in both tools is at least 44 px, no long dashes, no "מומלץ", no Hebrew letters in the English tool. A shared
  `#mexit=` link with `rf` restores 181 months, 3,000 and "10 ימים ומעלה".

Screens: `mquick-he-price-nocity-{390,1280}`, `mquick-he-city-tlv-{390,1280}`, `mquick-en-city-tlv-{390,1280}`,
`mquick-he-city-haifa-theme-390`, `mexit-have-refi-{390,1280}`, `mexit-refi-section-{390,1280}`, `mexit-refi-not-worth-{390,1280}`,
`mexit-refi-prime-{390,1280}`, `mexit-refi-theme-390`, `page-he-{390,1280}` (full page).

## 4. For the release (not done here)

- Ship `mrates-common.js` and `mexit.js` in the same release (the `?ver=` of both changes together); `mquick.js` is independent.
- Not changed: `inc/instruments.php` (the mexit `desc` and server summary could mention the refinance example later), the page,
  the English page. Lock line, `source_audit.py` before and after, press both tools on the live page at phone and desktop width.
