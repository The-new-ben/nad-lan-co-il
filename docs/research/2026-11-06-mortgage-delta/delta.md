# Delta: every component the government sites and the ranking competitors have, against /mortgage-calculator/

Research only, 6.11.2026. Our page read live today (release 1.72.595, raw HTML with a browser User-Agent and a cache-busting query,
plus the nine tool scripts). Sources and raw fields: `inventory.json` (80 records). Rules and numbers for the two new tools:
`eligibility.md` and `presign.md`. Today's manual SERP: `serp-manual.md`. Owner map of words: `../2026-11-05-mortgage-world/keywords.md`.

**Our page order today** (H2 sequence, live): H1 and answer paragraph, CTAs, "מחשבון משכנתא מהיר" (mquick), "מחשבון משכנתא לפי
מסלולים" (Mortgage 2.0), the switcher "ומה עוד בודקים: שבעה כלים למשכנתא" (mbudget, moffers, mdecision, mreplay, mexit, mready, mkeys),
then the article: "שוק המשכנתאות, ספטמבר 2026", "המספרים של היום", "ההצעה שלכם מול הממוצע של בנק ישראל", "הממוצע החודשי של בנק
ישראל לפי מסלול ותקופה", "כמה ההחזר על משכנתא של מיליון...", "שלושת הסלים האחידים", "מה בנק ישראל מתיר", "ארבע טעויות...", "לוח
סילוקין למשכנתא", "מדד, פריים...", "פירעון מוקדם ומחזור", the how-to chapters, "מקורות מידע שכדאי לבדוק", FAQ (38 in FAQPage).
"Where" below uses these names. The content-first order (H1, answer, CTAs, stage) is not touched by any row.

Legend: **yes** = present and at least as good; **partly** = present but weaker or not crawlable; **no** = absent. "Owner" = the
page of ours that owns the words, so the main page links instead of competing (keywords.md section 3).

## (a) Government tools and data

| # | Component | Who has it | Do we have it | What to add, where, owner |
|---|---|---|---|---|
| A1 | State eligibility points calculator (ניקוד וגובה ההלוואה) | gov.il S1 links calcurate.co.il (server-side, undated); zakaut.com (siblings summed wrongly, 2018 amounts); Planner (page timed out) | **no** (Mortgage 2.0 has a "הלוואת זכאות" track where the user types amount and rate) | New tool chip "הלוואת זכאות: ניקוד וסכום" in the switcher after mready; runs in the browser; feeds the zakaut track. Spec: eligibility.md section 10. Owner: none today (keywords.md: no owner for eligibility; "מחשבון משכנתא משרד האוצר" sits in the head intent). A separate page needs Ben's word; token "eligibility" is free (url_word_audit 6.11) |
| A2 | Official points tables (marriage, children, siblings per applicant, singles by age) | gov.il S3, S4, S6 (updated 30.03.2026) | **no** (0 crawlable "ניקוד") | Dated tables in a new chapter after "מה בנק ישראל מתיר"; each table with its gov.il link and update date |
| A3 | Basic loan by points band (54,240 to 161,665 ₪, 11 bands) | gov.il S3 | **no** | Same chapter, one table; singles and olim marked "unverified mapping" (eligibility.md section 4) |
| A4 | Supplements: service 1% a month (542 to 1,617 ₪ per month by band), reserve, priority zones (100,000 / 70,000 ₪ at 4.5%), 10 פלוס (132,000 ₪ and income ceilings), Negev (48,000 to 84,000), confrontation line grant (10,400 / 9,100), olim (730 points, floors, 19,630 / 28,370 / 43,630, 10,895) | gov.il S7 to S14 | **no** | Inside the A1 tool and a compact table in the A2 chapter |
| A5 | Eligible-loan terms: rate = BoI average CPI-linked minus 0.5%, max 3%; up to 30 years shortenable to 5 ... 25; CPI-linked; no early repayment fee | gov.il S2; צו הבנקאות s.2 | **partly** (no-fee rule yes in FAQ and mexit; rate rule and terms no) | Two sentences in the A2 chapter; the current rate stays unverified until the BoI series is read (its page met a CAPTCHA today) |
| A6 | Eligibility process: registration at a mortgage bank (60 ₪), certificate valid one year from the request, extendable, any bank can lend, apply before the purchase contract, appeal committees, 36 months / 1 year from contract | gov.il S2 (25.09.2024) | **partly** (mready lists "תעודת זכאות ממשרד הבינוי והשיכון" for olim) | 5 lines in the A2 chapter + 2 FAQ: "יש מחשבון משכנתא של משרד האוצר?", "כמה זמן תעודת זכאות בתוקף?" |
| A7 | BoI "קו המשווה" (IRR and mix per bank, monthly, Excel TamInt010.xls, updated 11/08/2026, data 2026-09) | boi.org.il; Supermarker and YC link it | **partly**: we publish the same IRR per bank ("ריבית כוללת חזויה" column) and moffers uses it, but the name "קו המשווה" and its link are not in the HTML | Name and link it in "שוק המשכנתאות" under the bank table, with BoI's own disclaimer (bank-reported data, s.16יא) |
| A8 | Nominal to effective converter | boi.org.il (two fields, monthly-payment assumption) | **partly** (we convert inside the tools and explain "נומינלית" 8 times) | A two-field converter or a link in "הממוצע החודשי של בנק ישראל" |
| A9 | Indexation calculator (CBS, linked from BoI tools) | cbs.gov.il | **yes** (/cpi-calculator/ linked) | none |
| A10 | Directive 451 approval format (תוספת 6: header, 4 baskets x 12 rows, מידע נוסף) | boi.org.il | **partly**: moffers takes 4 numbers x 3 baskets; the page links version 20 (1/22, file 451-1-1.pdf) while the current is **version 22 (7/23, updated 19/07/23)** | Update the link to https://boi.org.il/media/utld2tgp/451.pdf; the presign tool reads the whole format (presign.md) |
| A11 | Directive 329 current version | boi.org.il circular 2852 (30.6.2026): version 13, the 2840 amendment in force from 1.10.2026 | **partly**: page text cites "גרסה 12, 8.2.2026" (the data file already notes version 13) | Update the visible citation to version 13 (30.6.2026) |
| A12 | Capital Market Authority calculators: life insurance for a mortgage (premium type, insured count, birth date, sex, smoker, tracks) and structure insurance (building type and floor, age, sum, water-damage plumber, claims, "האם הביטוח נרכש לצורך משכנתה?") | life.cma.gov.il, dira.cma.gov.il; Supermarker cross-links insurance | **partly**: named only inside mquick's JavaScript, not in crawlable HTML | Crawlable links in the full-cost lines and in presign check 21; owner /mortgage-home-insurance/ |
| A13 | Kol Zchut rights pages (מגבלות, אישור עקרוני, פתיחת תיק, שמאי, ביטוח, פירעון מוקדם, מיחזור, זכאות) | kolzchut.org.il | **no** link | Add 3 to 4 links to "מקורות מידע שכדאי לבדוק" |
| A14 | The 451 forecasts banks must use (from bond prices, every two weeks) | stated in 451 תוספת 6; Mizrahi repeats it | **no** (we use the BoI Research forecast of 21.10.2026) | Find and add the series; until then the presign recompute shows both (presign check 12). Location **unverified** |
| A15 | Rate change arrows per track vs last month | Supermarker ("▲ עלה", "▼ ירד") | **partly** (three-month table June to August) | Arrow and the change in points in "המספרים של היום" |
| A16 | gov.il life-events "taking a mortgage" steps | gov.il | not readable (403; the app rendered nothing; API 404) | Snippet only: survey the insurance market, do not sign with the bank's agency at once. Covered by presign check 21 |

## (b) Keywords, topics and headings

| # | Component | Who has it | Do we have it | What to add, where, owner |
|---|---|---|---|---|
| B1 | "מחשבון זכאות משכנתא", "מחשבון משכנתא משרד האוצר" (260/mo), "הלוואת זכאות", "ניקוד", "תעודת זכאות" | gov.il #1, zakaut, Planner, Mashcantaman (ריבית זכאות) | **no** (ניקוד 0, תעודת זכאות 1) | H2 for the A2 chapter, for example "מחשבון זכאות למשכנתא: ניקוד, סכום ותנאים"; FAQ entry keywords.md had kept out as unverified is now verified (S1). Run kw_guard before the title words |
| B2 | "בדיקת משכנתא לפני חתימה", "מה לבדוק באישור עקרוני" | YC, arielmash, Planner, gov.il life-events, Hapoalim | **partly** (H2 "איך בודקים עלות כוללת לפני חתימה?", "איך להשוות בין שתי הצעות בנק?") | H2 for the presign tool, for example "בדיקת משכנתא לפני חתימה: מה בודקים באישור העקרוני". The main page is Google's pick for "בדיקת משכנתא" (104 @17); /mortgage-advisor/ keeps its title and links to the tool; /mortgage-calculator/mortgage-pre-approval/ owns "אישור עקרוני למשכנתא" (link with that anchor) |
| B3 | One-sentence definition of IRR, "ריבית כוללת חזויה" | BoI, Hapoalim and Leumi tooltips | **partly** (term used twice) | Answer-first sentence with BoI's wording in "שלושת הסלים האחידים" |
| B4 | "סל מוצע" | 451, Hapoalim, Mizrahi, Leumi | **no** (0) | Use the term in "שלושת הסלים האחידים" and in the presign tool |
| B5 | "החזר לשקל" / "עבור כל שקל תשלם" | FIBI, Clal, servicebank, Planner, Mashcantaman | **partly** (the tool shows it; crawlable text 0) | One sentence with the system-average figure in "כמה ההחזר על משכנתא של מיליון..." |
| B6 | Glossary block (מונחון) | Harel (11 H2 article), Discount menu | **yes** (/glossary/ linked) | none; link the glossary terms used by the presign tool |
| B7 | Insurance on the mortgage: "האם ניתן לקבל משכנתא ללא ביטוח חיים?" (PAA) | Kol Zchut, Harel, 451 s.11 | **partly** (kept out in keywords.md as unverified) | Now verifiable (451 s.11(ד)(3): no insurance required up to 30,000 ₪; external insurance right): one FAQ answer + link to /mortgage-home-insurance/ (owner of "ביטוח משכנתא") |
| B8 | Mortgage registration, lien removal, "מכתב כוונות", registration fee exemptions | Kol Zchut, 451 s.15ב (7/23) | **partly** (רישום משכנתא in the documents list only) | Two lines + gov.il service link; "רישום משכנתא" (1,000/mo) has no owner page (keywords.md): separate decision for Ben |
| B9 | Olim eligibility (730 points, floors, supplements) | gov.il S11, S12 | **partly** (1 mention of עולים) | Lines in the A2 chapter; /en/mortgage-calculator/ and /israel-mortgage-non-residents/ keep the English intents |
| B10 | War relief on mortgage payments (Kol Zchut "הקלות בבנקים בעקבות המלחמה מול איראן", 28.4.2026) | Kol Zchut | **no** | Out of the calculator's scope; logged as a finding for Ben (no owner page) |
| B11 | "מטרת המשכנתא" first question (first home / investment / replacement) | Mizrahi, Supermarker | **yes** (buyer type in mquick, Mortgage 2.0, mbudget, mready) | none |
| B12 | Russian and Ukrainian information PDFs; Arabic calculator | Mizrahi, calcurate | **no** | Owner decision (language plan), not a calculator item |

## (c) Tool features

| # | Component | Who has it | Do we have it | What to add, where, owner |
|---|---|---|---|---|
| C1 | Rate band per track and term under each rate field | Mashcantaman (12 tracks x 6 periods, undated) | **partly** (BoI averages per term and per bank, dated) | Under each rate field in Mortgage 2.0: the lowest and highest of the 7 banks for that track (by_bank), with the month |
| C2 | More tracks and change frequencies (משתנה כל 1, 2, 2.5, 10; עוגן מק"מ; מט"ח) | Mashcantaman, FIBI ("תדירות שינוי בשנים"), Kol Zchut | **partly** (prime, var5 linked and not linked) | Change frequency selector on variable tracks; FX skipped (0.1% of new loans, 8.2026) |
| C3 | Term in months | Mashcantaman, Hapoalim (סל מוצע), servicebank (10 to 480 months) | **partly** (years 4 to 30) | Months input in Mortgage 2.0 and the presign tool (refinance and approvals print months) |
| C4 | Schedule menu incl. interest-only, balloon plus Spitzer, grace plus Spitzer | servicebank (widest), FIBI, Clal | **partly** (Spitzer, equal, balloon, bullet, grace partial or full) | Name "גרייס ושפיצר" in the UI and the schedule chapter |
| C5 | Export: Excel schedule (servicebank), PDF comparison (FIBI, Mashcantaman print document) | as listed | **partly** (print and copy in mbudget, mready; case link) | Print/PDF and CSV of the schedule and the mix comparison in Mortgage 2.0 |
| C6 | Live rule check (1/3 fixed, 2/3 variable, LTV, PTI) | Supermarker, Hapoalim (66.66%) | **yes** | none |
| C7 | Prime shock over 3 years and CPI slider | Supermarker | **yes** (scenarios, custom shock, mdecision ladder, mreplay) | none |
| C8 | Price from equity and payment | Mizrahi tab 2, Mojo | **yes** (mquick by payment, mbudget) | none |
| C9 | Three scenarios side by side (today / BoI forecast / stress) | arielmash | **partly** (one scenario at a time) | Three columns in the Mortgage 2.0 summary |
| C10 | Balance after 5 years; payment to income per mix | arielmash | **yes** | none |
| C11 | Highest payment with the year it happens | FIBI ("בשנה ה-"), 451 row 9 (month) | **partly** (highest payment shown; its month not confirmed in this read) | Show the month next to the highest payment |
| C12 | Construction input index per contractor schedule | arielmash | **yes** (mkeys) | none |
| C13 | Refinance break-even | Supermarker Refinance.aspx | **yes** (mexit "האם למחזר") | Owner /mortgage-refinance/ for the full refinance intent |
| C14 | The three uniform baskets for the user's own amount and term, beside the user's mix | Hapoalim, Leumi, Supermarker, Mizrahi modal | **partly** (chapter table for fixed amounts; baskets inside mexit and moffers) | One tap "הסלים האחידים לסכום שלי" in Mortgage 2.0 |
| C15 | Eligible-loan track filled from the points result | none (gap everywhere) | **partly** (track exists, rate typed) | After A1: amount and the rate rule filled, no-fee label kept |
| C16 | Deep links with query parameters | Leumi (mortgageSum, period), Supermarker (mode, amount, years) | **partly** (hash state) | Optional; hash is enough (no new indexable URLs wanted) |
| C17 | Lead form carrying the user's mix | Supermarker, Mashcantaman, zakaut (data in the URL) | **no, by design** | Keep no lead form in tools (owner rules; lead privacy memory) |
| C18 | Reader comments (2,461) | Mashcantaman | **no** | Owner decision; never fake |

## (d) Forms and checklists

| # | Component | Who has it | Do we have it | What to add, where, owner |
|---|---|---|---|---|
| D1 | Eligibility documents (ID with appendix, service and reserve confirmations, siblings' IDs or affidavit, marriage, divorce, death certificates, common-law affidavit, oleh certificate, pregnancy) | gov.il S2 | **partly** (mready has some olim items) | Add the S2 list to mready.json under an "eligibility" stage, each item with source S2 and its date |
| D2 | Approval-in-principle checklist | YC (7), arielmash (5, paid), Planner, CFPB pattern | **partly** (two how-to chapters) | The presign tool, 28 checks (presign.md) |
| D3 | Final documents vs approval, before signing | CFPB Closing Disclosure explainer and checklist | **no** | Presign mode 2 |
| D4 | Bank documents for the approval by profile | Mizrahi, Discount, Hapoalim lists | **yes** (mready: 43 items, each sourced and dated) | none |
| D5 | External insurance submission steps (policy to the branch, answer in 14 days, renewal notice 30 days) | 451 s.11, Kol Zchut | **no** on the main page | Presign check 21; owner /mortgage-home-insurance/ |
| D6 | Appeal on eligibility (committees, through the bank) | gov.il S2, S14 | **no** | A1 tool result footer |
| D7 | Mortgage registration request (gov.il service) | Kol Zchut links it | **no** | Link in B8 lines |
| D8 | Two-offer comparison worksheet | arielmash | **yes** (moffers: three offers) | none |

## (e) Trust and authority

| # | Component | Who has it | Do we have it | What to add, where, owner |
|---|---|---|---|---|
| E1 | Named author and reviewer, Person schema | Planner (Person with jobTitle, alumniOf, memberOf), arielmash (Person), YC (byline + Person), NerdWallet, Harel (Organization as author) | **no**; and the related-guides block says "כתוב ונבדק על-ידי עורך דין מקרקעין" with no name | A named reviewer is Ben's decision (HAD-658). Until then the unnamed lawyer line is a risk: a claim with no person behind it |
| E2 | One visible date line | Supermarker "עודכן בתאריך: 01/11/2026 · ריביות השוק: ספטמבר 2026 (בנק ישראל)"; YC published / updated; gov.il pages | **partly** ("עודכן 5.11.2026" and "נכון ל-25.10.2026" in different places; JSON-LD 6.11) | One line under the answer paragraph: updated date + data month |
| E3 | Method and assumptions section | Supermarker "הנחות החישוב" + "איך אנחנו משווים"; arielmash "מקורות המודל"; Hapoalim and FIBI disclaimers | **partly** (sources chapter; formulas only in script headers) | H2 "איך המחשבון מחשב: הנחות ומקורות" before "מקורות מידע": Spitzer, effective to monthly rate, forecast path and date, CPI assumption, what is excluded |
| E4 | What is excluded (file fee, appraisal, insurance, prepayment fees) | Mashcantaman, Supermarker, Hapoalim | **partly** | A list inside E3 |
| E5 | Official sources with dates | YC "מקורות רשמיים לעיון", Supermarker | **yes** (stronger than all: SDMX, files, directives, CBS) | Fix the 451 and 329 versions (A10, A11); add קו המשווה, gov.il, Kol Zchut |
| E6 | Licence numbers | none of the 15 commercial sites shows one; Harel links "מידע בדבר תגמול לבעל רישיון" | n/a | Keep the site from presenting itself as a broker or adviser (Brokers Law note in memory) |
| E7 | Ratings and reviews | Planner AggregateRating 5/5 (86), Mashcantaman comments | **no** | Never invented; owner decision |
| E8 | Contact | banks' phones, advisers' WhatsApp | **yes** (WhatsApp bar, email) | none |
| E9 | Schema stack | Harel and Supermarker FAQPage; arielmash WebApplication; Planner FinancialService; ours SoftwareApplication, FAQPage (38), BreadcrumbList, Dataset, HowTo | **yes**, except Person | Person only after E1 |
| E10 | BoI disclaimer on bank-reported data | boi.org.il קו המשווה | **partly** ("אינו הצעה") | BoI's sentence under the by-bank table (A7) |

## (f) Pre-signing check features from abroad

| # | Component | Who has it | Do we have it | What to add, where, owner |
|---|---|---|---|---|
| F1 | Field-by-field explainer of the standard offer document with "Actions to take" | CFPB Loan Estimate explainer (3 pages, 28 items) | **no** | Presign full mode: each 451 row with "מה לבדוק" |
| F2 | Final document diffed against the offer | CFPB Closing Disclosure | **no** | Presign mode 2 (check 26) |
| F3 | Compare on total cost, not the rate | CFPB (APR, TIP), NerdWallet | **yes** (moffers on IRR and totals) | none |
| F4 | Rate vs a dated market average for the same product, with change and the money value of 25 bps | NerdWallet (national average, week and year change) | **yes** (BoI averages, 54 ₪ per quarter point in mdecision) | Add month-over-month change (A15) |
| F5 | Get three or more offers | NerdWallet, CFPB, Freddie Mac figure | **partly** (moffers takes 2 to 3) | none |
| F6 | Validity or rate-lock date | CFPB rate lock; ESIS validity date | **no** | Presign check 1 (24 / 12 days, 451 s.4ג) |
| F7 | Risk labels on prepayment penalty and balloon | CFPB | **partly** (mexit fee; balloon in Mortgage 2.0) | Presign checks 16, 17 as labels |
| F8 | Linked products and insurance choice | ESIS section 8; CFPB "services you can shop for" | **partly** | Presign check 21 |
| F9 | Worst-case payment illustration | ESIS sections 5 and 6 | **yes** (highest payment, 2022 replay) | none |
| F10 | Consequences of non-payment | ESIS section 13 | **no** | One line + Kol Zchut link in presign (optional) |
| F11 | Wire-fraud warning before paying | CFPB closing checklist | **no** | Presign check 27 |
| F12 | Permission to walk away, no pressure | CFPB checklist | **no** | One line in the presign summary |
| F13 | Reflection period | EU (7 days, unverified this session) | n/a in Israel (no statutory period found) | Do not claim one; the 24-day hold is the Israeli window |
| F14 | Complaint path | ESIS section 12 | **no** | Link to the BoI public enquiries unit in presign (URL **unverified**, check before use) |

## Blocked or unverified in this pass

- gov.il life-events "taking-a-mortgage": 403 to scripts and WebFetch; the app rendered no content in the built-in browser; its
  public API answered 404 for the slug.
- boi.org.il "הריבית הממוצעת על משכנתאות צמודות למדד": Radware CAPTCHA; not solved; the eligible-loan rate stays unverified.
- MoneyHelper (3 pages): 403. NerdWallet "what is a good mortgage rate": 404 (its rates page was read instead). EUR-Lex: WAF
  challenge (ESIS read on legislation.gov.uk). Planner eligibility calculator: timeouts. haotzarsheli.mof.gov.il: retired.
- life.cma.gov.il and dira.cma.gov.il: 202/403 to scripts; read in the built-in browser (inputs only; nothing submitted).
- calcurate.co.il computes on the server; no value was typed (no-submit rule), so its outputs were not tested.
