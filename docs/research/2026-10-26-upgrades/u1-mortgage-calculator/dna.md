# U1 · /mortgage-calculator/ · competitor DNA, facts and build spec

Research only (owner order, Ben 25.10.2026). Nothing on the live site was changed; no Linear or Notion item was created.
Prepared 25.10.2026 (evening, Israel time) by the U1 research lead (Claude Opus 5.5).

Evidence classes used below: **code** = raw HTML / official data file read by script; **SERP** = DataForSEO Google organic live
advanced (Israel 2376, Hebrew), task ids 10251925-*, 10251926-*, 10251938-* = 25.10.2026 19:25 to 19:38 UTC; **GSC** = Search
Console API, property sc-domain:nad-lan.co.il, 25.7 to 23.10.2026; **eyes** = page read in the owner's Chrome (BoI site sits behind
a bot wall, so it was read there). Anything not proven is marked **unverified** and kept out of the spec.

Raw files: `C:\Users\777\nad-lan\_private-research\2026-10-26-upgrades\raw\u1\` (our pages `ours-*.html`, competitors `c-*.html`,
GSC rows `gsc-mortgage-pages.csv`, URL audits `urlaudit-*.txt`, BoI files in `boi\`: directive 329 v12 `329_12.pdf`, circular 2852
`h2852.pdf`, Q&A `111598.pdf`, directive 451 circular 2694 `h2694.pdf`, early-repayment order `order-116.pdf`, average mortgage rates
`mashfix.xls` + `pribmash.xls` (both updated 18.10.2026), SDMX extract `boi-sdmx-BIR_MRTG_99-2025-2026.csv`).
Baseline depth proof: `proof-before.md` (this folder).

---

## 1. Intents and keyword set

GSC 90 days for /mortgage-calculator/: 8,259 impressions, 1 click, average position 47.0. Volumes = DataForSEO monthly (IL, he),
from `docs/research/2026-10-21-kikar-tools/keywords.csv` (14.10.2026).

| # | Intent (what the searcher wants) | Owned keywords on THIS page | GSC impr @ pos | Volume |
|---|---|---|---|---|
| 1 | Compute the monthly payment and total cost of a mortgage | מחשבון משכנתא · מחשבון משכנתאות · משכנתא מחשבון · חישוב משכנתא · מחשבון משכנתא פשוט · סימולטור משכנתא · עלות משכנתא | 573@45 · 99@37 · 216@45 · 338@44 · 44@37 · 52@48 · 166@40 | 33,100 (group) · 1,600 · 1,600 · 1,600 · 590 · 20 |
| 2 | Payment-first: from a payment I can carry to the loan, and the reverse | מחשבון משכנתא לפי החזר חודשי · מחשבון החזר משכנתא · מחשבון משכנתא החזר חודשי · חישוב החזר משכנתא · חישוב משכנתא לפי החזר חודשי · החזר משכנתא · משכנתא 1000000 כמה החזר | 298@38 · 296@41 · 181@41 · 157@40 · 98@40 · 81@34 · 71@57 | 590 · 590 · 30 · 480 · 110 · NA · 10 |
| 3 | Build and check a track mix (tracks, prime, CPI, uniform baskets) | מחשבון משכנתא מסלולים · חישוב משכנתא לפי מסלולים · מחשבון משכנתא עם מסלולים · בדיקת תמהיל משכנתא · "בדיקת משכנתא" · איך מחשבים ריבית משכנתא | 86@40 · 83@41 · 81@41 · 97@42 · 117@17 · 86@56 | 30 · 10 · 10 · NA · NA · NA |
| 4 | Repayment methods and special structures | מחשבון משכנתא בלון · משכנתא בלון מחשבון · חישוב משכנתא בלון · מחשבון משכנתא גרייס חלקי · (SERP: מחשבון שפיצר, לוח סילוקין) | 68@70 · 69@70 · 74@75 · 33@60 | 20 · 10 · 10 · 10 |
| 5 | Is my bank's offer fair, and what do Bank of Israel rules allow | מחשבון משכנתא בנק ישראל · (AIO: הגבלות בנק ישראל על התמהיל) | 27@31 | 20 |

Synonyms to use in copy: החזר חודשי, החזר ראשון, החזר מרבי צפוי, לוח סילוקין, שפיצר, קרן שווה, בלון, בוליט, גרייס, תמהיל, מסלול,
קל"צ, ק"צ, פריים, משתנה כל 5 שנים, צמוד למדד, סל אחיד, עלות כוללת, החזר לכל שקל, יחס החזר מהכנסה, שיעור מימון.

### Ownership map (one word = one owner URL; no new URL is needed)

`url_word_audit.py --token mortgage` = 18 URLs; `--token משכנתא` = 0; `--token reverse` = 1; `--token calculator` = 14
(files `urlaudit-*.txt`). GSC per page over 90 days: /mortgage-calculator/ 8,259 · /investment-property-mortgage/ 595 ·
/israel-mortgage-non-residents/ 314 · /mortgage-calculator/mortgage-ltv-ratio/ 63 · bridge-loan 16 · interest-rates 8 · refinance 6 ·
any-purpose 4 · pre-approval 1 · **reverse-mortgage 1** · repayment-capacity 0. Google treats the main calculator as the cluster's
face and sends it the sub-intents.

| Query family | Owner URL (keep) | Main calculator's role |
|---|---|---|
| מחשבון משכנתא, חישוב, החזר חודשי, מסלולים, בלון, גרייס, בדיקת תמהיל | **/mortgage-calculator/** | owns |
| מחשבון משכנתא הפוכה (434@54), משכנתא הפוכה מחשבון (98@55), טבלה משכנתא הפוכה (16+11) | **/mortgage-calculator/reverse-mortgage/** (indexed, crawled 16.10.2026, title already "מחשבון משכנתא הפוכה 2026: ...", has a working calculator) | short section + exact-anchor link only |
| כמה משכנתא אפשר לקחת (310@64) | **/mortgage-calculator/mortgage-repayment-capacity/** (H1 owns it; tool `afford` live since 21.10.2026) | short section + exact-anchor link; the main tool keeps a payment-to-loan mode (intent 2), not an income-and-equity affordability solver |
| ריבית משכנתא, ריבית משכנתא היום, ריבית הפריים | /mortgage-calculator/mortgage-interest-rates/ (tool `prime`) | shows today's numbers strip, links |
| מחשבון מחזור משכנתא (125@37), מחזור משכנתא מחשבון (40@49) | /mortgage-refinance/ | short section + link |
| מחשבון משכנתא לכל מטרה (131@43) | /mortgage-calculator/mortgage-for-any-purpose/ | link |
| אחוז מימון, מחשבון משכנתא לבניה עצמית (153@49) | /mortgage-calculator/mortgage-ltv-ratio/ | rule table + link |
| משכנתא לדירה להשקעה | /investment-property-mortgage/ | link (keep existing section) |

**Decision on "מחשבון משכנתא הפוכה":** the existing /mortgage-calculator/reverse-mortgage/ owns it. Reasons from the data:
(1) every top-10 result for that query is a dedicated reverse-mortgage page (moti.org.il calculator, itra-plus, mashkanta-hafuha,
insurers Harel/Clal/Phoenix/Ayalon, Bank Jerusalem), never a general calculator; (2) the dedicated page is indexed and already carries
the exact title; (3) it is starved of internal links: three sibling pages and the main calculator link to **/reverse-mortgage/, which
returns 404** (see 9.2). The URL repeats "mortgage" but existing slugs are never renamed (no-redirect law), and no new URL is minted.
Main calculator: one short section "משכנתא הפוכה לבני 60 ומעלה" with a button whose anchor is exactly "מחשבון משכנתא הפוכה" to
/mortgage-calculator/reverse-mortgage/; no reverse calculator on the main page (that would build a rival). The reverse page needs its
own upgrade (H1 starting "מחשבון משכנתא הפוכה", three repayment modes, provider terms table; see section 10) as a separate task.

---

## 2. SERP snapshot (25.10.2026, 19:25 to 19:38 UTC, DataForSEO, Google IL Hebrew)

SERPs are volatile: the head term shows a different top 10 on desktop and mobile. Banks win the AI overview everywhere.

### מחשבון משכנתא (desktop, depth 20)
1 lemon.co.il/mortgage-calculator/ "מה זה מחשבון משכנתא" · AIO · 2 nitzanm.co.il/mortgagecalculator/ · 3 mercantile.co.il loan calculator ·
4 topnetglobal.co.il · 5 bestie.co.il (repayment article) · 6 cmfs.co.il · 7 bizportal.co.il calculator · 8 machshevon.net · 9 c14.co.il
(2023 article) · 10 lahav-f.org.il · 11 mym.co.il · 12 משכנתא.org.il · 13 mashkanta.org.il/calc · 14 ram-finances.com · 15 gemel.net ·
16 arielmash.com · 17 calculatzia.com · 18 shelifinance.co.il · 19 ykinadlan.co.il. nad-lan not in top 20.
**Mobile top 10:** nitzanm · AIO · mercantile · servicebank.cav.co.il (Harel calculator) · moti.org.il balloon calculator · mym · gemel ·
omega-f · elhayyad · lahav-f.
**AIO** (sources Hapoalim, Mizrahi-Tefahot, Leumi ufapi, Mashcantaman): lists the bank calculators and Mashcantaman; describes uniform
basket simulation, first payment at forecast rate, BoI forecasts, "up to 4 mixes in parallel", Spitzer vs equal principal, BoI mix
limits. PAA: absent. Related: מחשבון שפיצר משכנתא · מחשבון הלוואה מרכנתיל · מחשבון לוח שפיצר עם לוח סילוקין · מחשבון משכנתא מסד ·
מחשבון הלוואה שפיצר · מחשבון משכנתא גרייס · מחשבון הלוואה פריים · מחשבון משכנתא גולינגו · לימון משכנתאות · יועץ משכנתא. Mobile
"people also search": מחשבון הלוואת בלון מזרחי טפחות · מחשבון משכנתא בלון · מחשבון שפיצר משכנתא · מחשבון הלוואת בלון בנק הפועלים /
לאומי · מחשבון הלוואה.

### חישוב משכנתא (desktop)
1 bankhapoalim.co.il/mortgage/mortgage-calculator · 2 mizrahi-tefahot.co.il/mortgages/calculator/ · AIO (same 4 sources) ·
3 mashcantaman.co.il/מחשבון-משכנתא/ · 4 ufapi.bankleumi.co.il/mortgageCalculator/Calc · 5 mortgage.discountbank.co.il/calculator ·
6 clalbit.co.il/calculatormashcanta/ · 7 mortgage.leumi.co.il calculator page · 8 taxo.co.il · 9 supermarker.themarker.com. PAA absent.
Related: מחשבון משכנתא פשוט · מזרחי · לאומי · פועלים · דיסקונט · הבינלאומי · חישוב משכנתא לפי החזר חודשי · מחשבון משכנתא משרד האוצר.

### כמה משכנתא אפשר לקחת (desktop)
AIO first (sources: kolzchut "מגבלות על לקיחת משכנתא", shelifinance, Bank Jerusalem, evensapir, Discount, Leumi, Mashcantaman):
LTV 75/70/50, any-purpose 50%, PTI up to 50% "but banks 30-35%", term up to 30 years, "at least 33% fixed, up to 66% variable".
Organic: 1 clalbit · 2 supermarker guide · 3 mashcantaman any-purpose · 4 shelifinance (term) · 5 mashcantaman max-mortgage calculator ·
6 meyda.org.il · 7 lsmashkanta · 8 kolzchut · 9 muhni.co.il.
**PAA:** מהו מחשבון מחזור משכנתא? · האם ניתן לקבל משכנתא על נכס קיים? · האם ניתן לקבל משכנתא ללא ביטוח חיים? · כמה הון עצמי נדרש
כדי לקבל משכנתא? · כמה כסף צריך להרוויח כדי לקבל משכנתא? · האם ניתן לקבל החזר משכנתא של 1.2 מיליון שקל?

### מחשבון משכנתא לפי החזר חודשי (desktop)
AIO (Hapoalim, Leumi, Mizrahi, Mashcantaman, FIBI apps, Taxo): "set the payment you can carry, pick term and rate"; Spitzer, equal
principal, grace/bullet. Organic: 1 mortgage.mercantile.co.il · 2 gadi-leichter.co.il · 3 c14 · 4 evensapir.co.il/calc ·
5 myhouse.org.il · **6 nad-lan.co.il/mortgage-calculator/** (live position 7 absolute) · 7 hon.co.il (2022) · 8 family-economy.co.il
(up to 5 tracks) · 9 optimai.co.il. PAA absent.

### מחשבון החזר משכנתא (mobile)
1 mym.co.il · AIO (Hapoalim, Mizrahi, Mashcantaman; Spitzer, equal principal, balloon/bullet) · 2 gemel.net · 3 berki.co.il (price minus
equity) · 4 family-economy · 5 realfix.co.il · 6 mako N12 "בכמה ירד החזר המשכנתה שלכם" (9.10.2026, prime 5.5% to 4.75% since May) ·
7 myhouse · 8 fullness.co.il (accelerated repayment) · 9 tefahot.co.il legacy calculator. PAA absent.

### מחשבון משכנתא הפוכה (desktop)
AIO (moti.org.il, Harel, Phoenix, Bank Jerusalem, Ayalon, Clal): audience 55 to 60+, no compulsory monthly payment or interest-only,
loan "20% to 60% of value by age", repaid on sale, move to assisted living or death. Organic: 1 itra-plus.com guide · 2 mashkanta-hafuha.co.il ·
3 primeinv.co.il · 4 meyda.org.il · 5 icf.co.il/mortgage-calculator/ · 6 mortgagebpoint.co.il (1.10.2026) · 7 taxo · 8 eytanim.net ·
9 midrag.co.il. **PAA:** מהי משכנתא הפוכה? · האם ניתן לקבל משכנתא על נכס קיים? · כמה כסף צריך להרוויח כדי לקבל משכנתא? · האם ניתן
לקבל החזר משכנתא של 1.2 מיליון שקל? · כמה החזר משכנתא חודשי אקבל על משכנתא של 2 מיליון ש"ח? · האם ניתן לקבל משכנתא ללא ביטוח חיים?

---

## 3. Competitor DNA (raw HTML read by script; counts from `dna.py` and `depth_proof.py`)

| Competitor | Keyword placement | Calculator: inputs · outputs | Data / visuals / schema / freshness | Why it ranks |
|---|---|---|---|---|
| **Mashcantaman** `/מחשבון-משכנתא/` (AIO source on every head query; #3 for חישוב משכנתא) | Title "מחשבון משכנתא עם ריביות מומלצות - חישוב משכנתא כולל מדד"; H1 "מחשבון משכנתא"; head term 9×; 2,519 words | Up to **4 mixes in parallel**; per track: amount, 12 track types (פריים, ק"צ, קל"צ, מ"צ, מל"צ, זכאות, יורו, דולר, עוגן מק"מ, משתנה כל 1/2/10), method (שפיצר / קרן שווה / בוליט), term **in months**, rate with a "recommended min-max range" per track and term, CPI with 5-year average hint; advanced: grace up to 60 months, one future rate change (month + %), future prepayment (partial/full, shorten term or lower payment). Mix summary: total loan, first payment, **max payment**, total interest, **total CPI linkage**, total repaid, **cost per shekel**. Full monthly schedule (print), mix comparison with yearly table and **payment-over-years chart** | Calculator is JS-rendered (not in raw HTML); 0 tables in HTML; **2,461 comments**; schema WebPage only; dateModified 29.1.2025 (stale); states an outdated rule ("up to 33% in tracks changing under 5 years") that Google's AIO repeats | Deepest calculator in the market + brand query volume (משכנתאמן מחשבון 880/mo) + years of links and UGC |
| **Bank Hapoalim** `/mortgage/mortgage-calculator` (#1 חישוב משכנתא, AIO) | Title "מחשבון משכנתא – חישוב ההחזר ותכנון המשכנתא"; H1 + H2 "מחשבון משכנתא"; 166 words | iframe app: **3 uniform baskets of BoI + a proposed basket**; first payment incl. forecast rate, **highest payment by BoI forecasts**, total expected repayment, total expected interest | 0 numbers, BreadcrumbList only | Bank brand authority + exact-match title; Google wants the banks' own calculators |
| **Mizrahi-Tefahot** `/mortgages/calculator/` (#2 חישוב משכנתא, AIO) | Title "מחשבון החזר משכנתא"; H1 "מחשבון משכנתא"; 1,646 words; FAQ 5 | 3 modes: price + equity + term → payment and loan; equity + term → max price; mix builder (add track: track, amount, term, rate, payment) → **first payment, max expected payment, total interest, total at end**; text on uniform baskets, forecasts (BoI, updated every two weeks), Spitzer, equal principal, partial/full grace, partial/full balloon | 39 figures; schema Organization only | Brand + the most complete explanation of baskets and forecasts among banks |
| **Leumi** ufapi + `mortgage.leumi.co.il` page (#4/#7) | "מחשבון משכנתא - חישוב משכנתא והחזר חודשי צפוי"; 507 words | Tabs **"סכום המשכנתא" (payment → loan)** and "ההחזר החודשי הראשון"; CPI forecast effect on payment and balance; combine loans with different terms and methods (שפיצר, קרן שווה, בוליט); repayment schedule (principal vs interest) | no schema, no tables | Brand; answers the payment-first intent explicitly (AIO cites it for that) |
| **lemon.co.il** `/mortgage-calculator/` (#1 desktop head term) | Title "מה זה מחשבון משכנתא"; H1 twice; 1,370 words; Article + Person + VideoObject + CommentAction | Thin definitional article; lead forms; no real calculator in HTML | 65 images (logos, team), video, map embed, author box, dateModified 16.9.2026 | Definitional "מה זה" angle + E-E-A-T signals (author, video, reviews) + freshness; partner badge with Madlan |
| **nitzanm.co.il** `/mortgagecalculator/` (#2 desktop, #1 mobile) | Title + H2 "מחשבון משכנתא"; 216 words | Per track: schedule type, track, amount, years, rate → **first payment, peak payment under CPI and rate forecast, total cost, payback per shekel**, interest and principal share of first payment, life-of-loan chart | Thin, fast, tool-first | Pure tool above the fold, exact-match title, low bounce |
| **mym.co.il** (#1 mobile החזר) | 64 words | Amount, down payment, rate, years | Thin | Tool-first, exact title |
| **gemel.net** (#2 mobile, #15 desktop) | Title "מחשבון משכנתא - חישוב החזר חודשי, ריבית ולוח סילוקין"; 1,109 words | Quick single track + **full mix with BoI baskets 1/2/3 and an automatic check of the one-third fixed rule**; weighted average rate | Worked example (1M, 25y, 5% = 5,846), FAQPage + WebApplication; rates "market averages example (June 2026)" | Finance hub authority, clean schema |
| **arielmash.com** (#16; the most advanced model found) | Title "מחשבון משכנתא מתקדם"; FAQPage + WebApplication | Scenario switch **today / BoI forecast / stress**; price, equity, net income; basket quick-starts; per track method and indexation; outputs first payment, max payment in scenario, total, interest + linkage cost, first-payment PTI, **balance in 5 years**, payment chart; **construction input index forecast per contractor payment schedule**; share link + Excel export. Strip: prime 4.75%, prime forecast Q2/2027 4.5%, inflation 1.5%, forecast 1.8% | Data as of 4.9.2026 / **July 2026 forecast (now stale: October forecast published 21.10.2026)**; updated 9.10.2026 | Depth, but low authority (page 2) |
| **machshevon.net**, **bizportal**, **icf.co.il** | exact titles | Spitzer single track; bizportal and machshevon add **payment tables by rate and term** (bizportal 6 tables, 129 cells; machshevon 113 figures); icf 10 FAQs | numbers-rich text | Number density and FAQ |

Reverse-mortgage SERP DNA (for the reverse page task, not this page): moti.org.il calculator (H1 "מחשבון משכנתא הפוכה", two schedules:
full deferral vs principal-only deferral, video), Harel 60+ (from 250,000 ₪, three repayment tracks: no payment / interest only /
Spitzer, no guarantors, no income check, no life insurance), itra-plus guide (55+).

---

## 4. Union checklist (every topic, table and calculator feature any competitor has) and gaps nobody covers

**Calculator features (union):** amount → payment · payment → max loan (Leumi, Clal, Supermarker) · price + equity → loan (Mizrahi,
berki, mym) · equity → max price (Mizrahi) · multi-track mix, up to 5 tracks (family-economy) · up to 4 mixes compared (Mashcantaman) ·
BoI uniform baskets 1/2/3 (Hapoalim, Mizrahi, gemel, arielmash) · one-third fixed check (gemel) · 12 track types incl. eligibility and FX ·
Spitzer / equal principal / bullet / balloon · partial and full grace · term in months · CPI assumption · forecast scenario (BoI) ·
stress scenario · one future rate change · future prepayment (shorten term / lower payment) · first payment · max payment · total paid ·
total interest · total CPI linkage · cost per shekel · interest vs principal share of first payment · balance after 5 years · full
monthly schedule · yearly schedule · payment-over-time chart · life-of-loan chart · first-payment PTI · recommended rate range per
track and term · share link · Excel export · print · construction input index exposure on a contractor payment schedule.

**Content (union):** what a calculator is · how to use · formula (Spitzer) · worked example · payment tables by rate and term · tracks
explained · uniform baskets · forecasts and where they come from · BoI rules (LTV, PTI, mix, term) · equity needed · PTI guidance ·
term choice 20/25/30 · prepayment · refinance · advisor or not · "hidden details" story · FAQs (up to 10).

**Gaps none covers (our openings):**
1. **Your offer vs the Bank of Israel average**, track by track and term by term, with the difference in shekels over the life of the
   loan. Nobody uses the official monthly averages (`mashfix.xls`, `pribmash.xls`, SDMX BIR_MRTG_99); Mashcantaman shows its own range.
2. **Where you stand among last month's borrowers**: your PTI, LTV, loan size and term against the official distribution of new
   mortgages (10,272 loans in August 2026). Nobody shows it.
3. **Correct, current BoI mix rule**: directive 329 v12/v13 says the variable part may not exceed 66.66% (no separate one-third prime
   cap). Mashcantaman and the AIO still state the old under-5-years 33% cap.
4. **Early repayment fee estimate per the Banking Order formula** using the same BoI average rates (fees that apply: operational up to
   60 ₪, notice 0.1%, capitalization with 20%/30% reductions, half the CPI average). Mashcantaman says its prepayment ignores fees.
5. **October 2026 BoI Research forecast** (rate 3.0% average in Q3 2027; inflation 2.0% over four quarters) and the next decision date
   (23.11.2026) wired into the scenarios; the best competitor still runs the July forecast.
6. **Dated, sourced numbers in the HTML itself** (tables Google can read without scripts), not only inside a JS app.

---

## 5. What Google wants to show

- A **working calculator first** (pure tool pages with 64 to 216 words hold positions 1 to 2), exact-match "מחשבון משכנתא" in title
  and H1, and a short definition ("מה זה מחשבון משכנתא" wins desktop #1).
- In the AIO: **bank calculators + one deep independent calculator**, and the features it names are exactly baskets, first payment at
  forecast, highest payment by BoI forecast, multi-mix comparison, Spitzer vs equal principal, BoI mix limits. To be cited we need those
  features stated in crawlable text with numbers and the rule source.
- For "כמה משכנתא אפשר לקחת" Google wants the two BoI limits (LTV, PTI) and the mix rule in numbers: that answer belongs to the
  capacity page; the main page should state the rules table and link.
- For payment-first queries Google explicitly describes "set the payment you can carry → loan amount": we must expose that mode.
- Balloon / grace / Spitzer schedule searches cluster on calculators that print a schedule.

---

## 6. Verified facts (primary sources, retrieved 25.10.2026 unless stated)

| Fact | Value | Source (date) |
|---|---|---|
| Bank of Israel rate | **3.25%**, in force since 3.9.2026; left unchanged on 21.10.2026 | BoI SDMX `BR/MNT_RIB_BOI_D` daily to 25.10.2026 (code); BoI press release 21.10.2026 (eyes) |
| Next rate decision | **23.11.2026** | boi.org.il press-releases page header (eyes) |
| Prime | **4.75%** (BoI rate + 1.5, bank convention) | derived; corroborated by arielmash strip and Mako N12 9.10.2026. BoI publishes the average prime monthly as a chart only |
| 2026 rate path | 8.1 → 4.00%; 28.5 → 3.75%; 9.7 → 3.50%; 3.9 → 3.25% | BoI SDMX via `data/boi-rate.json` (21.10.2026) and SDMX re-read today |
| CPI, 12 months to September 2026 | **1.6%** | CBS series 120010 (`data/cbs-120010.json`, fetched 21.10.2026; 105.3 vs 103.6) and BoI site header "1.6%" (eyes) |
| BoI Research forecast, October 2026 | BoI rate **3.0%** average in Q3 2027; inflation **2.0%** over the next four quarters, 1.5% in 2026, 2.1% in 2027; markets 3.1% / 1.8%; private forecasters 3.1% (2.8 to 3.5) / 2.1% (1.7 to 2.4) | BoI press release 21-10-26a (eyes) |
| Average rate, new housing loans, fixed not linked (קל"צ) | Jun 4.73% · Jul 4.63% · **Aug 2026 4.62%** | BoI SDMX BIR_MRTG_99, series BNK_99034_LR_BIR_MRTG_467 (code) |
| Average rate, fixed CPI-linked (ק"צ) | Jun 3.27% · Jul 3.22% · **Aug 3.29%** | same, series _1492 |
| Average rate, variable CPI-linked | Aug: benchmark **1.64%** + margin **1.55%** = 3.19% | same, series _1489 + _1488 |
| Prime-track average | **not published as its own series** in this dataflow | (gap, see unverified) |
| Average mortgage rate by term, not linked (fixed + variable, effective annual), reporting month 9/2026, in force from **19.10.2026** | average 4.55% · up to 1 year (incl. loans whose rate-change date is unknown) 4.35% · 1-5y 4.51% · 5-10y 4.59% · 10-15y 4.61% · 15-20y 4.74% · 20-25y 4.79% · over 25y 4.89% | BoI `mashfix.xls` (updated 18.10.2026); these are the rates used for early-repayment fees |
| Average mortgage rate by term, CPI-linked, same month | average 3.49% · up to 5y 3.50% · 5-10 3.49% · 10-15 3.24% · 15-20 3.46% · 20-25 3.37% · over 25y 3.53% | BoI `pribmash.xls` (updated 18.10.2026); history back to 1996 in the same file |
| New mortgages, August 2026 | **10,272 loans**, **10.90 billion ₪** (average ≈ **1.06 million ₪**); September first release 8.67 billion ₪ | SDMX series _63 and _897 (code; unit = ₪ thousands) |
| Track shares of August volume | variable not linked (incl. prime) 54.3% · fixed not linked 35.8% · fixed CPI 6.6% · variable CPI 3.2% · FX 0.1% | SDMX _70, _71, _69, _68, _66 (code) |
| LTV shares of August volume | up to 30% 8.4% · 30-45% 14.8% · 45-60% 27.9% · 60-75% 48.8% · above 75% ≈ 0.04% | SDMX _887 to _842 (code) |
| PTI shares of August volume | up to 10% 2.6% · 10-20% 12.5% · 20-30% 31.8% · 30-40% 52.6% · 40-50% 0.4% · above 50% 0 | SDMX PTI buckets (code) |
| Average payment-to-income, new housing loans | **29.23%** (Aug 2026) | SDMX _155 (code) |
| Average term, not linked | **23.8 years** (Aug 2026) | SDMX _461 (code) |
| Investment-home loans, August | 694 loans, 0.89 billion ₪ (≈1.28 million ₪ each) | SDMX _62, _776 (code) |
| LTV caps | single home **75%** · replacement home **70%** · investment home **50%** (a non-citizen cannot have a "single home", so 50%) | Directive 329 v12 (8.2.2026) s.2 and definitions; v13 (30.6.2026) only adds "in Israel" to the loan definition |
| Reduced-price homes (מחיר למשתכן, מחיר מטרה) | value may rest on an appraisal, capped at 2.1M ₪ or the purchase price if higher; buyer pays at least **100,000 ₪** own money (**60,000 ₪** where the new "מחיר למשתכן" grant applies) | Directive 329 s.4A |
| Payment-to-income | not above **50%**; above **40%** the loan carries a 100% risk weight; PTI = payment ÷ disposable income (net minus fixed commitments over 18 months, alimony, rent if not moving in); half of a first-degree guarantor's income may count, a spouse living with the borrower in full | Directive 329 s.5, s.6, Annex A |
| Variable-rate share | variable part ≤ **66.66%** of the loan (so at least one third fixed) | Directive 329 s.7 |
| Maximum term | **30 years** | Directive 329 s.8 |
| Any-purpose loan on a home | total LTV 50%, up to 70% if the part above 50% is at most **200,000 ₪** | Directive 329 s.10A, s.4 |
| PTI exemptions | bridge loans up to 3 years; any-purpose loans up to 120,000 ₪ | Directive 329 s.11-12 |
| Refinance | may not create or enlarge a breach of these limits | Directive 329 s.9 |
| Self-build / buying group LTV value | lower of appraisal and expected cost; no developer profit or expected appreciation | Directive 329 Q&A 2.18 |
| Uniform baskets in every approval in principle | Basket 1: 100% fixed not linked · Basket 2: 1/3 fixed not linked + 1/3 prime + 1/3 variable every 5 years CPI-linked on government bonds · Basket 3: 1/2 fixed not linked + 1/2 prime; terms offered 10/15/20/25/30; Spitzer; the approval must show the predicted overall interest, total predicted repayment and the highest predicted monthly payment | Directive 451, circular 2694 (31.1.2022, in force 31.8.2022), addendum 5 |
| Early repayment (Banking Order 2002, amended 2014) | operational fee up to **60 ₪**; **0.1%** of the amount if notice is under 10 days (not charged if the bank refinances it or the borrower died); capitalization fee on fixed tracks when the average rate is below the loan rate (lower of two formulas); none on loans whose rate changes at least yearly or at unknown dates (prime) and none on a rate-change day; CPI-linked loans repaid between the 1st and 15th: half the average monthly CPI change of the last 12 indices; reductions on the capitalization fee: **20% after 3 years, 30% after 5 years** (complementary loans: 10/20/30/40% after 1/2/3/4 years); directed (state) loans: no fee; notice up to 45 days ahead | צו הבנקאות (פירעון מוקדם של הלוואה לדיור), התשס"ב-2002, ss.2-8, 10 (`order-116.pdf`) |
| State eligibility loan (משכנתא בזכאות) | a CPI-linked fixed-rate loan; amount and terms set by the government by points (years of marriage or immigration, children, siblings, service) plus a "place loan" in priority areas; can be repaid early with no fee and no notice | Mizrahi-Tefahot eligibility page (bank disclosure, read 25.10.2026) + the Order s.2 |
| Reverse mortgage (provider terms) | Harel 60+: age 60+, loan from 250,000 ₪, three repayment tracks (none / interest only / Spitzer), no guarantors, no income check, no life insurance | harel-group.co.il (read 25.10.2026) |

**Unverified (kept out of the spec until checked):** the average prime-track margin; eligibility loan amounts and rate for 2026;
"up to 90% financing" for מחיר למשתכן (the directive sets minimum own money, not 90%); a BoI or Capital Market Authority rule set for
reverse mortgages; whether a bank must accept outside life and property insurance (PAA question, needs the law text); the exact
appraisal and file-opening fee ranges; grace length limits (Mashcantaman says up to 60 months).

---

## 7. Our page as Google gets it (raw HTML, `?x=` cache-buster, 25.10.2026) and its gaps

- Title "מחשבון משכנתא 2026: החזר חודשי, ריבית ותמהיל | nad-lan" (54 chars). H1 "מחשבון משכנתא 2026: החזר חודשי ועלות כוללת".
  Canonical self, no robots meta, indexed (URL Inspection: crawled 18.10.2026). dateModified 22.10.2026. Schema: **WebPage only**.
- Two inline calculators, no instruments-engine mount (no `data-nli`, so `depth_proof` counts tools = 0):
  (a) `nlc-mortgage` "תמהיל 3 מסלולים": per track amount / rate / years for קל"צ, פריים, משתנה; totals (loan, payment, interest,
  cost), a bar of the payment split by track, a "+2%" checkbox; defaults **5.2% / 6.0% / 5.5%, stale** against the official 4.62%
  fixed, prime 4.75% and 3.19% variable CPI; label "סימולציית עליית ריבית" and "נוסחת PMT", "נדלן חכם" break the language law.
  (b) `nmc` simple: loan, rate (default 4.8%), years, net income, stress (+1), fixed expenses → payment, total, interest, ratio,
  stressed payment, status text at 30% / 40%.
  Missing against the best competitor: payment → loan, price + equity → loan, equal principal, bullet/balloon, grace, CPI linkage,
  forecast scenarios, future prepayment, max payment, total linkage, cost per shekel, schedule, charts, mix comparison, uniform
  basket presets, rule checks (LTV, 66.66% variable, 30 years, PTI 50%), official rate defaults with dates, share link, print.
- Content: 2,143 words, 29 headings, but only **13 figures**, **1 table (21 cells)**, **1 image** (a Wikimedia hotlink of the Diamond
  Exchange), **2 official links**, 5 FAQs without FAQPage schema. No dated numbers anywhere in the text.
- **Broken internal links (404):** /reverse-mortgage/, /mortgage-ltv-ratio/, /mortgage-interest-rates/, /mortgage-repayment-capacity/
  on this page; the same block repeats on the interest-rates, LTV, repayment-capacity and reverse pages (17 broken links in the cluster).
  Fix = point each href at the real /mortgage-calculator/... URL (an href edit, not a redirect).
- Related cluster debt seen in passing: interest-rates page meta still says "ריבית בנק ישראל סביב 4% והפריים סביב 5.5%"; the
  non-resident page meta says "prime at 5.25%"; the reverse page H2 "ריבית, מנגנון צבירה ופירעון" uses a banned word and its FAQ heading
  reads "שאלות נפוצות חוזה".

Baseline depth (`proof-before.md`): ours words 2,143 · figures 13 · tables 1 · cells 21 · tools 0 · faq 5 · headings 29 · visuals 1 ·
sources 2. Competitor maxima: words 1,464 (Mizrahi; Mashcantaman's body text is larger but not detected as main) · figures 115
(bizportal) · tables 6 · cells 129 (bizportal) · tools 1 · faq 10 (icf) · headings 17 (lemon) · visuals 65 (lemon, mostly logos) ·
sources 2 (icf). Competitor sums: figures 416 · tables 7 · cells 145 · faq 35 · headings 86 · visuals 125.

---

## 8. BUILD SPEC

### 8.1 Title, H1, meta (keep what owns the head term)
- **Title: keep** "מחשבון משכנתא 2026: החזר חודשי, ריבית ותמהיל | nad-lan" (54 chars). It starts with the head term and holds intents 1
  to 3; position 45 is a depth and authority problem, not a title problem. Re-test only after six weeks with no movement.
- **H1: keep** "מחשבון משכנתא 2026: החזר חודשי ועלות כוללת". Exactly one H1; the calculator's own heading stays H2/H3.
- Meta description (proposal): "מחשבון משכנתא לפי מסלולים: החזר חודשי, ההחזר הגבוה הצפוי ולוח סילוקין, שלושת הסלים של בנק ישראל ובדיקה
  אם הריבית בהצעה שלכם גבוהה מהממוצע החודשי של בנק ישראל."

### 8.2 Answer paragraph (50 words, head term first)
"מחשבון משכנתא מחשב את ההחזר החודשי, הריבית וסך התשלומים לפי סכום, מסלולים ותקופה. הכניסו את הסכום, בחרו תמהיל או אחד משלושת
הסלים האחידים של בנק ישראל, וראו את ההחזר הראשון, ההחזר הגבוה הצפוי, ואם הריבית שהבנק הציע לכם גבוהה מהממוצע שבנק ישראל פרסם החודש.
כל הנתונים מבנק ישראל, עם תאריך."

### 8.3 Section order (content-first law: H1 → answer → CTAs → the calculator → facts → article; phones first)
1. H1 · 2. answer paragraph · 3. CTA row: "לחישוב ההחזר" (anchor to the tool) · "בדיקת הצעה מהבנק" (anchor to the offer check);
   the site-wide WhatsApp bar stays as is.
4. **The calculator (Mortgage 2.0)**, open with an example (8.5).
5. "המספרים של היום" strip + table T1 (dated).
6. "ההצעה שלכם מול הממוצע של בנק ישראל" (the moat output, 8.6).
7. "המשכנתא שלכם מול כל המשכנתאות של החודש" (infographics V1, V2, V3).
8. "ריבית משכנתא ממוצעת לפי מסלול ולפי תקופה" (T2, T3, chart V4).
9. "כמה ההחזר על משכנתא של מיליון, מיליון וחצי ושני מיליון" (T6).
10. "שלושת הסלים האחידים של בנק ישראל" (T5).
11. "מה בנק ישראל מתיר: מימון, החזר מהכנסה, תמהיל ותקופה" (T4; states the current 66.66% rule plainly).
12. "שפיצר, קרן שווה, בלון וגרייס" (T8).
13. "מדד, פריים ומה צפוי בריבית" (October forecast, next decision date, CPI 1.6%).
14. "פירעון מוקדם ומחזור" (T7) + link "מחזור משכנתא" → /mortgage-refinance/.
15. All existing sections, unchanged in substance (how to use, PTI, total cost, "מה לא רואים במחשבון פשוט" table, sensitivity, price,
    investment, equity, first vs future payment, comparing two offers, mistakes, advisor, sources) with dated numbers added where they
    now say "סביר" or "גבוה".
16. "מחשבונים קרובים": מחשבון משכנתא הפוכה → /mortgage-calculator/reverse-mortgage/ · כמה משכנתא אפשר לקחת →
    /mortgage-calculator/mortgage-repayment-capacity/ · אחוז מימון → /mortgage-calculator/mortgage-ltv-ratio/ · ריבית משכנתא היום →
    /mortgage-calculator/mortgage-interest-rates/ · משכנתא לכל מטרה · הלוואת גישור · מס רכישה · עלות רכישה כוללת (all real URLs).
17. FAQ (30, 8.8) · 18. honesty statement, method and sources, "עודכן ב" date.

### 8.4 Tables (each with its real source printed under it)
| # | Table | Data source | Refresh |
|---|---|---|---|
| T1 | המספרים של היום: ריבית בנק ישראל 3.25% · פריים 4.75% · ההחלטה הבאה 23.11.2026 · מדד 12 חודשים 1.6% · תחזית בנק ישראל לריבית ברבע השלישי 2027: 3.0% · ריבית ממוצעת קל"צ 4.62% (אוגוסט) | SDMX MNT_RIB_BOI_D; BoI press page; CBS 120010; BoI Research 21.10.2026; SDMX BIR_MRTG_99 | daily / monthly |
| T2 | ריבית ממוצעת במשכנתאות חדשות לפי מסלול, שלושה חודשים אחרונים (קל"צ, ק"צ, משתנה צמודה = עוגן + מרווח), עם ממוצע תקופה | SDMX BIR_MRTG_99 (_467, _1492, _1488/_1489, _461, _1491, _1487) | monthly |
| T3 | ריבית ממוצעת לפי תקופה לפירעון, לא צמודה וצמודה, בתוקף מ-19.10.2026 (8 + 7 buckets) with an effective-to-nominal note | BoI `mashfix.xls`, `pribmash.xls` | monthly (~mid month) |
| T4 | כללי בנק ישראל: 75/70/50, דירה במחיר מופחת (2.1M, 100,000 / 60,000), החזר מהכנסה 50% (40%), חלק משתנה עד 66.66%, 30 שנה, לכל מטרה 50%/70% עם 200,000, מחזור | Directive 329 v13 | on circular |
| T5 | שלושת הסלים: הרכב + החזר ראשון למיליון ₪ ב-20/25/30 שנה לפי הממוצעים העדכניים (preview at today's data: 20y 6,391 / 6,079 / 6,297 ₪; 25y 5,627 / 5,299 / 5,528 ₪; 30y 5,138 / 4,796 / 5,035 ₪, with the prime part at the BoI "up to 1 year" not-linked average converted to nominal 4.27% and the CPI part before indexation; the label must say so) | Directive 451 addendum 5 + T2/T3 | monthly |
| T6 | החזר חודשי למיליון ₪ לפי ריבית 3% עד 6% ותקופה 15/20/25/30 (preview: 4.5% 25y 5,558 ₪; 5% 25y 5,846 ₪; cross-checked with bizportal and gemel) + rows for 1.5M and 2M | formula | static, rates band moves with T2 |
| T7 | עמלות פירעון מוקדם לפי מסלול: תפעולית ≤ 60 ₪ · הודעה פחות מ-10 ימים 0.1% · היוון במסלול קבוע עם הפחתה 20% אחרי 3 שנים ו-30% אחרי 5 · פריים ומשתנה שנתי: ללא היוון · צמוד: חצי שינוי מדד ממוצע ב-1 עד 15 בחודש · הלוואת זכאות: ללא עמלה | Banking Order 2002 | on amendment |
| T8 | שפיצר מול קרן שווה מול בלון על הסכום שלכם: החזר ראשון, אחרון, סך ריבית (preview 1M, 25y, 4.62%: Spitzer 5,627 flat, interest 687,997 ₪; equal principal 7,183 → 3,346, interest 579,425 ₪) | formula | live |
| T9 | התפלגות המשכנתאות החדשות לפי החזר מהכנסה ולפי שיעור מימון (אוגוסט 2026) | SDMX | monthly |
| T10 | keep "מה לא רואים במחשבון פשוט" (existing) | existing | |

### 8.5 Infographics (SVG in the HTML, not images; one chart system, the site's own palette, no cream or gold)
- **V1 "איך לקחו משכנתא באוגוסט 2026"**: one stacked bar of the 10.9 billion ₪ by track (54.3 / 35.8 / 6.6 / 3.2 / 0.1%) with three
  numbers beside it: 10,272 משכנתאות · ממוצע 1.06 מיליון ₪ · 23.8 שנים. Source SDMX.
- **V2 "ההחזר מההכנסה שלכם מול כולם"**: histogram of the six PTI buckets with a marker at the visitor's PTI from the tool, the
  average 29.23% and the 40% and 50% lines of directive 329.
- **V3 "כמה מימון לקחו"**: LTV bucket bars (48.8% at 60-75%) with the visitor's LTV marker and the 75/70/50 caps.
- **V4 "ריבית המשכנתא לאורך השנים"**: monthly lines since March 2013 for the not-linked average and since 2011 for the CPI-linked
  average (BoI xls), with the BoI rate as a step line (SDMX) and the October 2026 forecast point (3.0%, Q3 2027).
- Inside the tool: payment-over-time stacked by track, balance curve, principal vs interest by year (see 8.5.3).

### 8.5.1 The calculator (tool id `mortgage`, instruments engine, mounted with [nadlan_tool], data `data/boi-mortgage.json`)
**Modes (segmented):** "לפי סכום" (amount → payment) · "לפי החזר חודשי" (payment → max loan, per track mix) · "לפי מחיר והון עצמי"
(price, equity, buyer type → loan, LTV check, equity needed).
**Inputs:**
- Buyer type: דירה יחידה / דירה חליפית / דירה להשקעה / דירה במחיר מופחת (drives the LTV cap and the reduced-price rules).
- Tracks as rows (engine type `rows`, up to 6): track (קל"צ · ק"צ · פריים · משתנה כל 5 צמודה · משתנה כל 5 לא צמודה · הלוואת זכאות),
  amount or share, rate (pre-filled with the official average for that track and term, editable, the date shown under it), years 4 to 30,
  method (שפיצר · קרן שווה · בלון · בוליט), grace months with partial / full.
- Presets ("מקרים מוכנים"): סל אחיד 1, 2, 3 at today's averages; the current 3-track default; "דירה ראשונה 2 מיליון עם 25% הון עצמי".
- CPI per year: options "תחזית בנק ישראל 2.0%", "ציפיות השוק 1.8%", custom.
- Prime path: "ללא שינוי" · "תחזית בנק ישראל: 3.0% ברבע השלישי 2027" · "ציפיות השוק: 3.1%" · "עלייה של 2%" (keeps the old +2% box)
  · custom shock with the month it starts (Mashcantaman's single future change).
- Net household income, existing loans and fixed expenses (keeps the old simple calculator's fields).
- Future prepayment: month, amount, "קיצור תקופה" or "הקטנת החזר", with the fee estimate (T7 rules + T3 average rates).
**Outputs:** first payment total and per track · highest payment in the chosen scenario and when · total paid · total interest · total
CPI linkage · החזר לכל שקל · balance after 5 and 10 years · PTI with the existing 30% / 40% status texts plus the 50% cap · LTV and equity
needed · rule checks with plain sentences (variable over 66.66%, term over 30, LTV over cap, PTI over 50%) · yearly schedule table
(monthly on expand) · three charts (payment over time by track, balance, principal vs interest) · compare up to 4 mixes side by side,
baskets included · share (copy, WhatsApp, print exist in the engine) + a link that reopens the same numbers.
**Engine gaps to build:** a small SVG chart helper in core.js; a payment-to-loan solver; schedule generator with CPI, grace, balloon,
prime path; `tools/instruments/build_boi_mortgage_data.py` reading SDMX BIR_MRTG_99 (rates, volumes, PTI and LTV buckets, term) and the
two BoI xls files (needs `xlrd`) into `data/boi-mortgage.json`, monthly, with the as-of dates.
**Feature parity (additive law):** every field and output of both current calculators survives inside Mortgage 2.0 (three default
tracks, totals, split bar, +2% stress, loan/rate/years/income/stress/expenses, ratio and its three status texts). The two old widgets stay
on the page until the new tool is pressed and seen working, then retire only on Ben's word.
**Defaults fix:** open with the official averages and their date, never hard-coded 5.2 / 6.0 / 5.5 / 4.8.
**Copy fixes inside the tool:** "סימולציית עליית ריבית" → "בדיקת עליית ריבית"; "נוסחת PMT" → "לוח שפיצר"; drop "נדלן חכם" and "Nadlan".

### 8.6 THE MOAT: "ההצעה שלכם מול בנק ישראל"
One practical check nobody offers, built only from public Bank of Israel data and tied to the keyword and the moment of intent
(the visitor has a bank offer and runs the calculator):
1. The visitor types the offer track by track (or picks "use my mix above").
2. For each track the page shows the official average for the same indexation and fixed or variable type (SDMX, monthly) and for the same
   term bucket (BoI average-rate files, in force from 19.10.2026), converted from effective to nominal, and the gap in percentage points.
3. It turns the gap into shekels: "בריבית הממוצעת של בנק ישראל הייתם משלמים X ₪ פחות לאורך ההלוואה" (or more), and per month.
4. It places the whole loan among last month's 10,272 mortgages: PTI bucket, LTV bucket, loan size against the 1.06 million ₪ average,
   term against 23.8 years.
5. It lists the honest limits in one line: averages mix all borrowers and LTV levels; a strong profile can beat them; this is not an
   offer and not advice.
Why it holds: it needs the monthly official feeds, the effective-to-nominal conversion and the Banking Order fee formula, refreshed
every month with dates. Mashcantaman's "recommended range" is its own number; banks will never show their offer against the average.

### 8.7 Schema
WebApplication (applicationCategory FinanceApplication, offers price 0, inLanguage he) · FAQPage (30) · BreadcrumbList · Dataset for
T2/T3/T9 (creator Bank of Israel, temporalCoverage, dateModified) · dateModified on every data refresh.

### 8.8 FAQ (30, in searchers' words; every answer must use only the verified facts in 6)
1. מה זה מחשבון משכנתא ואיך משתמשים בו?
2. איך מחשבים החזר חודשי של משכנתא?
3. כמה החזר חודשי על משכנתא של מיליון שקל?
4. כמה החזר חודשי על משכנתא של 1.2 מיליון שקל?
5. כמה החזר חודשי אקבל על משכנתא של 2 מיליון ש"ח?
6. איך מחשבים משכנתא לפי החזר חודשי שאני יכול לשלם?
7. כמה משכנתא אפשר לקחת? (short answer + link to the capacity page)
8. כמה כסף צריך להרוויח כדי לקבל משכנתא?
9. כמה הון עצמי נדרש כדי לקבל משכנתא?
10. האם אפשר לקחת משכנתא בלי הון עצמי?
11. כמה אחוז מהמשכורת יכול לצאת על משכנתא?
12. מה ההבדל בין מסלולי משכנתא?
13. מה ההבדל בין קל"צ לפריים?
14. מה זה תמהיל משכנתא ואיך בודקים אותו?
15. מה הם שלושת הסלים האחידים של בנק ישראל?
16. כמה מהמשכנתא מותר לקחת בריבית משתנה?
17. מה ריבית הפריים היום ומתי ההחלטה הבאה?
18. מה הריבית הממוצעת על משכנתא החודש?
19. איך אדע אם הריבית שהבנק הציע לי טובה?
20. מה זה לוח שפיצר ומה ההבדל מקרן שווה?
21. למה ההחזר בשפיצר קבוע אבל הריבית בו יורדת?
22. מה זה משכנתא בלון ובוליט ומתי משתמשים בהן?
23. מה זה גרייס במשכנתא וכמה הוא עולה?
24. איך המדד משפיע על המשכנתא שלי?
25. האם כדאי משכנתא ל-25 או ל-30 שנה?
26. האם ההחזר במחשבון הוא ההחזר הסופי שאקבל מהבנק? (existing)
27. האם כדאי להכניס הכנסה נטו או ברוטו? (existing)
28. כמה עולה פירעון מוקדם של משכנתא?
29. מהו מחשבון מחזור משכנתא? (short + link to /mortgage-refinance/)
30. האם ניתן לקבל משכנתא על נכס קיים? (any-purpose rule + link); plus a reverse-mortgage pointer inside 30 or in section 16.
Kept out until verified: "האם ניתן לקבל משכנתא ללא ביטוח חיים?" (needs the law text).

### 8.9 Honesty target (beat every competitor maximum, and the competitors' sum where it is meaningful)
Measured with `python tools/depth_proof.py --ours https://nad-lan.co.il/mortgage-calculator/ --them <the 12 URLs in proof-before.md>`:
| Metric | Ours now | Max competitor | Sum of competitors | Target after |
|---|---|---|---|---|
| words | 2,143 | 1,464 | ~10,300 | ≥ 3,500 (quality over count) |
| figures | 13 | 115 | 416 | **≥ 450** (dated tables T1 to T9) |
| tables | 1 | 6 | 7 | **≥ 9** |
| cells | 21 | 129 | 145 | **≥ 300** |
| tools | 0 | 1 | 2 | **≥ 1 mounted `data-nli`** (Mortgage 2.0) + the two legacy widgets until parity |
| faq | 5 | 10 | 35 | **30 unique** (covers the union; 36 if the owner wants the sum beaten) |
| headings | 29 | 17 | 86 | ≥ 35 |
| visuals | 1 | 65 (logos) | 125 | **≥ 7 real charts** (4 on page + 3 in tool); no stock photos counted |
| sources | 2 | 2 | 2 | **≥ 10 official links** (boi.org.il circulars and data files, cbs.gov.il, gov.il) |
| schema | WebPage | FAQPage, WebApplication | | WebApplication + FAQPage + Dataset + BreadcrumbList |
Facts the page must carry, dated: every row of section 6 except the reverse-mortgage provider row (that belongs to the reverse page).

Draft honesty statement for Ben to sign (Hebrew, to go under the FAQ):
"הצהרת אמת: כל מספר בעמוד הזה מגיע ממקור רשמי שמופיע לידו, עם תאריך: בנק ישראל, הלשכה המרכזית לסטטיסטיקה והוראות המפקח על הבנקים.
החישובים נעשים בנוסחאות שמוצגות בעמוד. העמוד אינו הצעה לאשראי ואינו ייעוץ. בדקנו את העמוד מול 12 העמודים שמופיעים בגוגל על מחשבון
משכנתא, והתוצאה מתפרסמת כאן. בן בטש, עורך דין."

---

## 9. Defects to fix in the same release (findings, no redirects)
1. Four 404 hrefs on this page and 13 more in the sibling pages (section 7): change the hrefs to /mortgage-calculator/reverse-mortgage/,
   /mortgage-calculator/mortgage-ltv-ratio/, /mortgage-calculator/mortgage-interest-rates/, /mortgage-calculator/mortgage-repayment-capacity/.
2. Stale default rates in both widgets.
3. Banned words: סימולציה (tool note), "PMT", "Nadlan", "נדלן חכם".
4. Hotlinked Wikimedia hero image with an off-topic subject.
5. No FAQPage although the "שאלות נפוצות על מחשבון משכנתא" heading exists.

## 10. Follow-ups outside this page (separate tasks, for the coordinator)
- Reverse page: H1 "מחשבון משכנתא הפוכה: ..." , three repayment modes, provider terms table with dates (Harel, Clal, Phoenix, Bank
  Jerusalem, Ayalon), fix H2 "מנגנון" and the "שאלות נפוצות חוזה" heading, and inbound links from the cluster (after fix 9.1).
- Refinance page: early repayment fee estimator with the Banking Order formula and the BoI average rates (owns "מחשבון מחזור משכנתא").
- Interest-rates and non-resident pages: meta descriptions with stale rates (4% / 5.5% and 5.25%).
