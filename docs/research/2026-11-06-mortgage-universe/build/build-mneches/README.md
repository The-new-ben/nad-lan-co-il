# New tool for /mortgage-calculator/: "כמה אפשר לקבל על דירה קיימת" (mneches)

HAD-675. Built 6.11.2026, **local only**: nothing deployed, nothing committed, no existing file edited (`inc/instruments.php`
untouched). The loan a bank may give against a home the reader already owns (Google: משכנתא על נכס קיים, משכנתא כנגד נכס קיים,
כמה משכנתא אפשר לקחת על נכס קיים, הגדלת משכנתא, משכנתא נוספת לדירה קיימת). The title does not compete with the guide page that
owns "משכנתא לכל מטרה": the tool links to it with that exact anchor.

## Files

| File | What |
|---|---|
| `plugins/nadlan-config/assets/instruments/tools/mneches.js` | The tool (id `mneches`), Hebrew only, RTL. Pure logic in `window.NLNC`. Id-scoped CSS (`#nlnc`) over the instruments classes (`nli__panel`, `nli__title`, `nli__strip`, `nli__f`, `nli__in`, `nli__share`, `nli__eg`). |
| `plugins/nadlan-config/assets/instruments/data/mneches.json` | The rule texts with section numbers, the 120,000 exemption and the 18-month rule, the directive and Q&A files (URL, date, SHA-256, fetched 6.11.2026), the any-purpose loan figures of SDMX BIR_MRTG_99 for 8.2026 with series ids, and `unverified`. `"checked": "2026-11-06"`. |
| `build-mneches/registry.php.txt` | The entry for `nadlan_nli_tools()` and the branch for `nadlan_nli_summary()`, plus the chip and pane. `php -l` clean (PHP 8.3); summary rendered with stubs from the real data (below). |
| `build-mneches/test_mneches.js` | Node test, **62 assertions**, literals worked by hand or by an independent 40-digit Decimal annuity calculation. Last run: `test_mneches.out.txt`. |
| `build-mneches/preview.html` | Local mount exactly like the shortcode, inside switcher pane `#tool-neches` next to a second pane, with the switcher of `tools/mquick.js`; the host holds the PHP-rendered summary. `?theme=1` adds the live theme stylesheets (read only). |
| `build-mneches/verify.py` | Playwright (Chrome, headless) with its own `http.server` on a free 127.0.0.1 port, stopped in `finally`. **144 checks**. Last run: `verify.out.txt`, `verify.json`, `shots/`. |
| `build-mneches/sources/boi-sdmx-BIR_MRTG_99-2026-08_09.csv` | The SDMX file as fetched 6.11.2026 (SHA-256 332f89b0...), the evidence of every any-purpose figure. |

Run (from the repo root): `node docs/research/2026-11-06-mortgage-universe/build/build-mneches/test_mneches.js` and
`python docs/research/2026-11-06-mortgage-universe/build/build-mneches/verify.py`.

## The rules used, and where they were read

All from Bank of Israel files opened 6.11.2026. `https://boi.org.il/media/hjrlkrse/h2852.pdf` (circular ח-06-2852, 30.6.2026, carrying
the full text of directive 329 **version 13**; its version table: 2840 = v12, 8.2.2026; 2852 = v13, 30.6.2026) and
`https://www.boi.org.il/media/emunmobp/202601.pdf` (Q&A file of 8.2.2026). Both fetched by this session; their SHA-256 equal the copies
in `../../gov/raw/` (the test checks it), whose text was read.

| Rule | Wording (shortened from the source) | Where |
|---|---|---|
| Any purpose LTV | a loan secured by a home that is not for buying, leasing, building, expanding or renovating one: LTV against the pledged home, **maximum 50%** | Q&A 2.2 (4.12.2012), 8.2 (6.10.2021) |
| Earlier loans count | total LTV of the loan together with the balance of earlier loans secured by the same home may not exceed the rates | section 4 |
| Relief | a bank **may** skip section 4 for a loan not for buying real estate up to **70%**, provided the excess above 50% is at most **200,000 ₪**, cumulative over all loans on the home | section 10a; Q&A 2.31 (8.2.2026) |
| PTI | payment to disposable income at most **50%**; above 40% risk weight 100% | sections 5, 6 |
| Same home, from 1.10.2026 | the monthly payment includes earlier loans secured by the same home, at any lender, with more than **18 months** left | Annex A 1.1; start moved to 1.10.2026 by circular 2852 s.2 |
| Disposable income | net income minus fixed costs of more than 18 months (loan payments, alimony) | Annex A 1.2 |
| Exemption | PTI limits do not apply to any-purpose loans up to **120,000 ₪**, cumulative | sections 11, 12.2; Q&A 8.3 (8.2.2026) |
| Variable share, same home | new credit at the same bank on the same home: the 66.66% variable cap is tested on all credit on the home (from 1.10.2026) | Q&A 5.1; circular 2852 s.3 |
| Buying another home on this one | LTV by the purchased home (75 / 70 / 50, section 2), and in any case at most 50% of the pledged home | Q&A 2.1 |
| Parents helping a child | a first-degree relative's loan on his own home for the child's equity is an any-purpose loan, 50% of the pledged home | Q&A 2.7 |
| A relative's income | at most half of a non-buying relative's disposable income, even if he signs as a borrower | Annex A 1.3 |
| Refinancing | classified by the original loan's purpose | Q&A 7.7 |
| Term | at most 30 years | section 8 |
| Who it binds | the directive addresses banking corporations | sections 2 to 9 |

The LTV / PTI / term numbers the tool computes with are read from `boi-mortgage.json` `rules` (`any_purpose` 0.5 / 0.7 / 200000,
`pti_max`, `term_max`); `mneches.json` holds the same numbers from the directive text and the test asserts they agree.

**The news of October / November 2026** (Calcalist): the Calcalist articles were not opened. What the official files confirm: the
"same home" PTI rule (Annex A 1.1) and the Q&A 5.1 variable rule start on **1.10.2026** (circular 2852 moved them from 1.7.2026); the
tool says so ("מה השתנה ב־1.10.2026"). Parents' help: the official rule in force is Annex A 1.3 (half of a relative's income), quoted
in the kids purpose; a draft Q&A 4.11 of 10.5.2026 on the same subject is not used.

## Rates

* **Any-purpose average** (default for any purpose, children, closing loans): Bank of Israel SDMX BIR_MRTG_99, "Consumer loans other
  than overdrafts, with housing collateral", new business, **8.2026**: not linked **6.53%** (421.6 million), CPI linked **5.33%**
  (110.7 million), weighted by volume; rate / 12 as published, CPI unchanged. Same file: fixed not linked 6.61% vs **4.62%** on housing
  loans, fixed CPI 5.28% vs 3.29%; 1,386 loans, 532.5 million ₪, average PTI 23.97%; LTV bands (up to 30%: 23.1%, 30 to 45: 25.6%,
  45 to 60: 42.7%, 60 to 75: 8.6%). This is the source that any-purpose loans are priced higher, so the tool says it with numbers.
* **Housing mix average** (default when buying another home): `boi-mortgage.json` by_bank, all banks, **9.2026**, effective rates
  turned monthly, the same per-shekel payment as mquick (1,000,000 over 25 years = 5,428.30; the data headline says 5,428). When it is
  used for an any-purpose case, the help line says that any-purpose loans averaged 6.61% vs 4.62%.
* **Own rate**: typed annual rate / 12; opens at the fixed not linked average of the purpose's kind (6.61% or 4.62%), labelled.

## Worked examples (all in the test)

| Case | LTV rule | Income rule | Result |
|---|---|---|---|
| Opening example: value 2,800,000, balance 350,000, any purpose, income 25,000, other loans 1,500, existing payment 3,150, 20 years, any-purpose average | 50% = 1,400,000, minus 350,000 = **1,050,000**; relief min(1,960,000; 1,600,000) − 350,000 = 1,250,000 | 50% x 23,500 = 11,750, minus 3,150 = 8,600 a month; 8,600 / 7,329.83 per million = 1,173,288 | **1,050,000 ₪**, LTV binds by 123,288; first payment 7,696.32; total 1,847,116.74; PTI after 46.15% (the 40% note shows) |
| Income-bound: same home, income 18,000, other 2,000, own 5% | 1,050,000 | 50% x 16,000 − 3,150 = 4,850; 1,000,000 at 5% / 20 y = 6,599.5574, so 734,897 | **734,897 ₪**, income binds by 315,103; payment 4,850, PTI 50% |
| Zero balance: 2,000,000, income 40,000, own 5% (a typed existing payment is ignored) | 1,000,000; relief 1,200,000 | 20,000 a month = 3,030,506 | **1,000,000 ₪**; 6,599.56 a month, 1,583,893.77 in all, 583,893.77 interest |
| Balance above the cap: 900,000 on 1,500,000 (60%) | cap 750,000: **no room** | | "אין מקום להלוואה נוספת", never a negative; relief min(1,050,000; 950,000) − 900,000 = 50,000, said in the line |
| 800,000 on 1,000,000 | no room, also under the 70% relief | | said in the line |
| Exemption: 2,000,000, balance 0, income 3,000, other 2,000, own 5% | 1,000,000 | 500 a month = 75,762 | any purpose / closing loans: **120,000 ₪** (sections 11, 12.2); buying or children: 75,762 |
| Exemption capped: 300,000, balance 100,000 | 150,000 − 100,000 = 50,000 | | 50,000 (the exemption never lifts above the LTV room) |
| Existing 6,000 on income 10,000 | 1,000,000 − 300,000 | 5,000 − 6,000: no room | buying: "אין מקום לפי ההכנסה"; any purpose: 120,000 (exempt) |
| Term table, opening example | | 10 y 764,788 (income binds) · 15 y 1,000,808 · 20 y 1,173,288 · 25 y 1,299,338 · 30 y 1,391,471 | payments 8,600 · 8,600 · 7,696.32 · 6,949.69 · 6,489.53 |

## How the tool decides (our readings, each said on the page or in the code)

1. The headline is the base rule (50%). The 70% of section 10a is a bank's option: a second figure and a dashed zone on the bar, never
   the headline.
2. Relief and the 120,000 exemption apply to "לכל מטרה" and "סגירת הלוואות"; not to buying another home (a loan to buy real estate)
   and not to parents' help (Q&A 2.7 names 50%).
3. Buying another home: the existing balance counts inside the 50% of the pledged home (Q&A 2.1 read with section 4).
4. The exemption: when the income room carries less than min(120,000, LTV room), the result is that minimum and the line says the PTI
   limit of the directive does not apply and the decision stays with the bank. Cumulative use is said in the label.
5. The existing payment counts only when there is a balance; the help says it counts if more than 18 months are left.
6. Closing loans: the help asks not to include payments of loans being closed (our assumption, said on the page); closing a mortgage is
   refinancing (Q&A 7.7).

## Verified in the browser (verify.py, 144 of 144)

At 390x844 (is_mobile) and 1280x900: the chip opens the pane; opening values and presses; the headline against `NLNC` after every
press (4 purposes, 5 terms, 3 rate sources, own rate 6.61 / 5 / 25 (error), income-bound, balance 0 (field hides), balance above the
cap, the exemption, an empty value (error)); copy (clipboard read back), WhatsApp (href checked, navigation blocked), the case link
(read back, opened in a fresh page: the pane opens by pressing its chip, the case comes back); the guide link with the exact anchor;
fonts (Plex Sans Hebrew text, Plex Mono figures); one column on the phone, two on desktop; every amount shows the shekel sign on the
same side as the live tools; no console error or warning, no horizontal scroll, every visible control at least 44 px, inputs labelled,
groups named. Plus a phone pass under the live theme stylesheets (faces and 2 px radius hold).

Screenshots looked at (eyes): `mneches-default-390.png` (all of it, in crops), `mneches-default-1280.png`, `mneches-noroom-390.png`,
`mneches-buy-390.png`, `mneches-income-390.png`, `mneches-theme-390.png`. Fixed after looking: the source chips repeated "שו"ת" and
used the mono face for Hebrew (now "הוראה 329, שו"ת 2.2 ו־8.2" in the text face); one ledger value ("עד 1,250,000 ₪") put the sign on
the other side from every other amount (the word moved to the label; a browser check now guards it); Hebrew value cells ("אין מקום")
fell into the mono face (now the text face, explicit direction); "כ־384,000 ₪" put the sign against the prefix (now "כ־384 אלף ₪");
the 75 to 90% band printed "0.0%" for 60 thousand (now "<0.1%", left to right); the bar's relief label could overlap the 50% label
(now above the bar); the bar now shows a balance above the cap in survey red; "200,000 ₪" no longer breaks across lines.

## Server summary (rendered by PHP 8.3 with stubs from the real data files)

"כמה אפשר לקבל על דירה קיימת לפי בנק ישראל: בהלוואה לכל מטרה בשעבוד דירת מגורים המימון המרבי הוא 50% משווי הדירה, יחד עם יתרת
המשכנתא שכבר רשומה עליה. בשיקול דעת הבנק אפשר עד 70%, כשהחלק שמעל 50% עד 200,000 ₪ בכל ההלוואות על הדירה. ההחזר החודשי עד 50%
מההכנסה הפנויה, ומ־1.10.2026 הוא כולל גם הלוואות קודמות על אותה דירה שנותרו להן יותר מ־18 חודשים; הלוואה לכל מטרה של עד 120,000 ₪
פטורה ממגבלת ההחזר. למשל דירה בשווי 2,800,000 ₪ עם יתרת משכנתא של 350,000 ₪: 50% הם 1,400,000 ₪, פחות היתרה, כלומר עד 1,050,000 ₪,
ובהקלה עד 1,250,000 ₪. באוגוסט 2026 נתנו הבנקים 1,386 הלוואות חדשות לכל מטרה בשעבוד דירה, 532.5 מיליון ₪, וההחזר הממוצע היה 23.97%
מההכנסה; הריבית הממוצעת בקבועה לא צמודה 6.61%, מול 4.62% במשכנתאות לדיור באותו חודש. לפי הוראת ניהול בנקאי תקין 329, גרסה 13
(30.6.2026), וקובץ השאלות והתשובות (8.2.2026), נבדק ב־6.11.2026."

## Still unverified (labelled on the page or kept off it)

1. Whether the SDMX rates are nominal or effective (not stated in the file): used as published, / 12, and said so in the help line.
2. The final text of circular 2840 (8.2.2026) was not opened (no URL found); that its section 9 is the Annex A 1.1 change is read from
   the December 2025 draft and Q&A 5.1. Version 13 of the directive, which was opened, contains the Annex A 1.1 text.
3. Whether a bank applies the 70% relief to a parents' loan: not applied.
4. Reading 3 above (the existing balance inside the 50% when buying another home).
5. The Calcalist articles: not opened; only the official files are used.
6. Non-bank lenders: the line names no lender and no number (no lender page was opened).
7. The search phrases of the task were not checked in Google or DataForSEO by this session.

## Release steps (not done)

1. Paste `registry.php.txt` parts (1) and (2) into `inc/instruments.php`; ship `tools/mneches.js` and `data/mneches.json`.
2. Add the chip and pane `tool-neches` to the switcher of /mortgage-calculator/ (markup in the snippet header). Where the chip goes and
   its wording on the live page are the owner's call.
3. After release: source audit of the raw HTML, content_first_check, press-through in the owner's Chrome, and a link from the guide
   page /mortgage-calculator/mortgage-for-any-purpose/ to `#tool-neches` if the owner wants it.

## Design

Steel-blue ink on form-paper white, the instruments tokens (`--nli-*`): ink #12202A, sea-deep #1F4B5C, sea #2F6F86, survey red
#C42550 only for warnings (no room, the balance above the cap, PTI above 40%), open green #4F9A5C for spare room; IBM Plex Sans Hebrew
for text, IBM Plex Mono for figures. The signature element is a deed bar: the home's value as one ruled strip with the 50% mark (solid)
and the bank's 70% option (dashed), split into balance, the amount, the unused room (hatched) and the part above the cap (red); below
it a ledger where every line carries its section of directive 329. Why not the default look: it reads like a land-registry form filled
line by line, no cream, no brass, no gradient, no soft cards, no emoji.
