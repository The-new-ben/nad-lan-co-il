# U2 · /investment/ · competitor DNA, facts and build spec

Research only (owner order, Ben 25.10.2026). Nothing on the live site was changed; no Linear or Notion item was created.
Prepared 25.10.2026 (evening, Israel time) by the U2 research lead (Claude Opus 5.5). GSC API: live, full scope (read only here).

Evidence classes: **code** = raw HTML or an official data file read by script; **SERP** = DataForSEO Google organic live advanced
(Israel 2376, Hebrew, depth 20, AI overview loaded), tasks 10252007-* and 10252008-*, 25.10.2026 20:07:48 to 20:08:56 UTC;
**GSC** = Search Console API, sc-domain:nad-lan.co.il, 90 days to 23.10.2026 (`qp90.csv`); **eyes** = page read in the owner's Chrome
("gmktec"), used where gov.il, Kol Zchut and Madlan block scripts. Anything not proven is marked **unverified** and kept out of the spec.

Raw files (outside the repo): `C:\Users\777\nad-lan\_private-research\2026-10-26-upgrades\raw\u2\`
- `serp\` 10 SERP JSON files + `serp-organic.txt`, `serp-aio.txt`, `serp-log.json`; keyword volumes `kw_u2.json`
- `c-*.html` / `c-*.txt` 22 competitor pages (fetched 20:10 to 20:12 UTC), `ours*.html` our 16 cluster pages (`?x=` cache-buster), `fetch-log.json`
- `data\nadlan-gov\` 148 official files `rent_<code>.json` + `buy_<code>.json` for 74 cities (data.nadlan.gov.il, fetched 20:16 to 20:19 UTC,
  every file Last-Modified 20.8.2026, version 20-08-2026), CBS API series `cbs_120460/120490/40010/70000/120010.json`
- `gov\` Tax Authority 2026 buyer guide (70 pp.), instruction 1/2026, form 135 notes for tax year 2025, Knesset research paper on rental tax,
  MoF chief economist review for August 2026, CBS price bulletin table 4.9 (`cbs_a4_9_2026_09.pdf`), Tax Authority notice 12.10.2026 (eyes)
- `urlaudit-*.txt` URL word audits
Derived data for the build (in this folder): `data\yield-by-city.csv/.json` (via `build_yield.py`), `data\cashflow-by-city.csv`,
`data\breakeven-ltv-4rooms.csv`, `data\yield-two-rent-sources.csv`, `data\cbs-rent-table-4-9-2026q2.json`; fetch script `fetch_nadlan_gov.py`.
Baseline depth proof: `proof-before.md` (this folder).

---

## 1. Intents, keyword set and ownership

GSC 90 days for /investment/: **7,026 impressions, 1 click, 494 queries**, every head query between position 36 and 84.
Volumes: DataForSEO Labs keyword overview, IL/he, 25.10.2026 (`kw_u2.json`, cost $0.016).

| # | Intent | Queries this page owns (GSC impr@pos · monthly volume) | Owner URL |
|---|---|---|---|
| 1 | Is investing in property worth it, and how (head, "decide") | נדלן להשקעה 345@36 (90) · נדל"ן להשקעה 122@50 · השקעות נדלן 333@75 (320) · השקעות נדל"ן 119@76 + נדל״ן 61@75 + נדל״ן בישראל 140@78 · השקעה בנדלן 173@59 (140) · השקעות בנדלן 78@74 · השקעות נדלן בישראל 152@72 (40) · השקעות נדלן בארץ 135@60 (10) · השקעה נדלנית 23@34 · השקעת נדלן 24@41 | **/investment/** |
| 2 | What to buy and where: investment apartments, assets (head, "choose") | דירות להשקעה 231@55 (480) · דירה להשקעה 81@61 (480) · דירות להשקעה בארץ 114@64 · נכסים להשקעה בישראל 151@45 · נכסים להשקעה 105@49 (50) · נכס להשקעה 70@54 (50) · דירות להשקעה בישראל 61@50 · דירות למשקיעים 13@38 · בתים להשקעה 18@53 | **/investment/** (hub). Children keep their sub-intents: /investment/apartments-for-investment/ ("איך בוחרים"), /investment/where-to-buy-investment-apartment/ ("איפה כדאי לקנות", 50/mo) |
| 3 | What it yields and what is left each month (yield, cash flow) | תשואה דירה להשקעה · חישוב תשואה נדלן · אחוז תשואה · תשואה על דירה בישראל · סקירת שיעורי תשואה · איך בודקים תשואה של דירה (all 1-2 impr on this page) | **/investment/** for the city-by-city yield and cash-flow map (the moat). /investment/real-estate-yield/ keeps "how to calculate" (0 impr today); /investment-property-cashflow-calculator/ keeps "מחשבון תשואה/תזרים" (320/mo for מחשבון תשואה נדלן, 1 impr today) |
| 4 | Beginners | נדלן למתחילים 56@53 (30) · השקעות נדלן למתחילים 5@57 (20) · השקעות נדלן קטנות · מה לעשות עם 400 אלף שקל 10@64 · איפה להשקיע 200 אלף שקל | **/investment/** (one section, not a new page) |
| 5 | Taxes an investor pays | מס הכנסה דירות 24@70 · מס על נדלן 12@59 · מס הכנסה נדלן 12@40 · מיסוי נדלן 14@81 · מס רכישה למשקיעים 1@68 (related, 260/mo "מס על שכר דירה", 110/mo "מס הכנסה על שכר דירה") | **/investment/** carries the investor tax overview and the three rental-tax tracks. Deep owners: /real-estate-tax-advisor/purchase-tax-investor/ (purchase tax), /purchase-tax-calculator/, /real-estate-tax-advisor/capital-gains-tax-guide/ (betterment). **No page owns "מס על שכר דירה"** (/rental-income-tax/ returns 404): a dedicated page is the owner's call, no new URL now |
| 6 | Commercial property | נדלן מסחרי להשקעה 136@58 (30) · נכס מסחרי להשקעה 75@68 · רכישת נכס מסחרי 46@67 · נדל"ן מסחרי להשקעה 32@67 · השקעה במשרדים 15@84 | **/commercial-real-estate/** (+ /commercial-real-estate/commercial-real-estate-yield/). /investment/ keeps a short section and links |
| 7 | Financing an investment | הלוואה להשקעה בנדלן 74@62 · משכנתא למשקיעים 12@82 · מימון רכישות 46@72 | **/investment-property-mortgage/** (owns משכנתא לדירה להשקעה 390@40). /investment/ keeps the 50% rule and links |
| 8 | Developer and project finance | מימון נדלן 273@83 (90) · מימון נדל ן 60@88 · מימון נדל"ן 29@90 · מזנין · מימון עסקאות נדלן | **No owner on the site.** The SERP is developer credit (Harel fund, mezzanine, g-mortgage for developers). /investment/ cannot satisfy it; do not chase it here. Owner's call |
| 9 | Not ours | מכירת נכס 112@87, מכירת דירה, מכירת חנות → /selling-apartment/ · קניית דירה 92@84, קניית נכס → /buying-apartment/ · השכרת נכס 66@74 → /my-rentals/ · סוכן נדלן, תיווך → broker pages · מה זה noi / cap rate / פארי פאסו / סקשן 8 / מושע → /glossary/ entries | as listed |
| 10 | Foreign-language searchers landing here | investire in immobili in israele 277@62 · investimento immobiliare israele 49@63 · acquistare casa in israele 19@53 · investir em imóveis em israel 212@84 · investimento imobiliário israel 45@84 · invertir en inmuebles en israel 112@83 · inversión inmobiliaria israel 66@84 · financement immobilier israël 35@86 · English 4 to 10 each | **Separate decision for the owner.** There are no Italian, Portuguese or Spanish hubs; English, French, Russian hubs exist. Google already tests /investment/ for these: Italian ≈345, Portuguese ≈257, Spanish ≈178, French ≈42 impressions in 90 days. Not part of this Hebrew build |

**URL audits** (`url_word_audit.py`, 25.10.2026, 4,598 URLs): `--token investment` = 42 URLs (the hub, 20 city pages
/investment/&lt;city&gt;-investment-apartment/, real-estate-yield, real-estate-leverage, investment-via-company, bank-guarantee-purchase,
where-to-buy-investment-apartment, apartments-for-investment, residential-building/land-investment, airbnb-israel-regulation,
/investment-apartment/ and its Tel Aviv neighbourhoods child, /investment-property-mortgage/, /investment-property-cashflow-calculator/,
6 commercial pages, a glossary category) · `--token השקעה` = 0 · `investor` = 2 · `yield` = 2 · `rent` = 44 (/buy-or-rent/ and
/buy-vs-rent/ both live, see 9) · `rental` = 0 · `tax` = 11. **No new URL is needed for anything in this spec.**

**Synonyms to use in copy:** נדל״ן להשקעה, השקעות נדל״ן, השקעה בנדל״ן, דירה להשקעה, דירות להשקעה, נכס להשקעה, נכס מניב, תשואה ברוטו,
תשואה נטו, תשואה על ההון, תזרים חודשי, החזר משכנתא, שיעור מימון, הון עצמי, מס רכישה דירה נוספת, מס שבח, פטור משכר דירה, מסלול 10%,
מדד שכר דירה, מחיר חציוני, שכר דירה חציוני, פריפריה, מרכז.

---

## 2. SERP snapshot (25.10.2026, 20:07 to 20:09 UTC, DataForSEO, Google Israel, Hebrew)

nad-lan.co.il does not appear in the top 20 of any of the 10 SERPs. **People also ask: absent on all 10.** AI overview: present on 9
desktop SERPs, absent on mobile "נדלן להשקעה".

### נדלן להשקעה (desktop) · task 10252007-2646-0139-0000-5d906ff8318b
Top 10: 1 gemel.huji.ac.il "נדל"ן או שוק ההון? כך תבחרו באיזו אפשרות להשקיע" (2022) · 2 meitav.co.il "השקעה בנדל"ן דרך מסלול ממוקד נדל"ן במיטב מנג'ר" ·
3 finwiz.co.il "דירה להשקעה - יתרונות וחסרונות" · 4 YouTube "נדל"ן להשקעה - מדידה לראשונה" (accounting, IAS 40) · 5 genesis100.co.il (US property) ·
local pack (rs-nadlan Haifa, indigos, climaxgrp) · 6 mynumberz.co.il "איפה הכי כדאי לקנות דירה להשקעה? המצפן למשקיע המתלבט" · 7 Facebook group "דירות להשקעה" ·
8 wecheck.co.il "דירה להשקעה - היכן להשקיע ולגייס הון?" · 9 afikil.co.il "איך להשקיע בנדל"ן – המדריך המלא למתחילים" · 10 genesis100 again.
Related: eight Meitav fund searches (מיטב קרן נאמנות, מיטב מנג'ר תשואה ...). Mobile top 4: gemel.huji, meitav, nadlanmaster.co.il/israel/, finwiz.
**AI overview** (same text on נדלן להשקעה, השקעות נדלן, השקעה בנדלן): two profit sources (rent and appreciation); residential 3% to 4%,
commercial 7% to 9%; LTV 75% single, 50% second home; purchase tax exemption to about 1.9M for a single home, 8% to 10% for a second;
betterment 25% on real gain; betterment levy 50%; rental exemption 5,654 ₪ a month; channels: buy to let, abroad (from 100,000 ₪), indirect
(funds, TASE property shares, Meitav). Sources: lazyinvestor.co.il, bdo-academy.co.il (course), nadlancenter.co.il/article/3724.

### השקעות נדלן (desktop) · task 10252007-2646-0139-0000-9fc030e988f3
1 lazyinvestor.co.il/real-estate/ "נדל"ן למתחילים | השקעות לעצלנים" · 2 nadlancenter.co.il/article/3724 "השקעות נדל"ן - המדריך השלם לשנת 2026" ·
3 globes.co.il tag page · 4 isratop.co.il (service) · 5 openu.ac.il tafnit "השקעות בנדל"ן – מה זה ואיך מתחילים?" · 6 gindi.com/article/realestate-investment/ ·
7 genesis100 · 8 meitav · 9 YouTube "להשקיע בנדל"ן ללא הון עצמי" · 10 meitav. People also search: קניית קרקע להשקעה · קורס נדלן אונליין · קורס נדלן מומלץ ·
דירות להשקעה · יועץ השקעות מומלץ · איך להשקיע כסף. Related: השקעות נדלן למתחילים · השקעות נדלן בישראל ספר · השקעות נדלן בחול · חברות השקעות נדלן
בישראל · נדלן למתחילים ספר · השקעות לעצלנים נדלן · נכסים להשקעה · קורס השקעות נדלן.

### השקעה בנדלן (desktop) · task 10252008-2646-0139-0000-c46ddefb03fd
1 lazyinvestor · 2 openu tafnit · 3 meitav "איך להשקיע בנדל"ן בישראל גם בלי הון עצמי של מאות אלפי שקלים?" · 4 nadlan-nadlan.co.il "נדל"ן להשקעה - קרקעות, דירות ונכסים
מסחריים במרכז" · 5 globes "עם תשואה של 25% בשנה: כך תוכלו להשקיע בנדל"ן בלי לקנות דירה" · 6 YouTube (Guy Paran) · 7 nadlanmaster "איפה כדאי לקנות דירה להשקעה ב-2026?" ·
8 isratop · 9 climaxgrp "השקעות נדל"ן 2026 – המדריך המלא" · 10 fingrow. Related adds "השקעה בנדלן דרך שוק ההון", "חברות השקעה בנדלן".

### דירות להשקעה (desktop) · task 10252008-2646-0139-0000-294667268b94
1 israelsir.co.il (Sotheby's Tel Aviv listing tag) · 2 nadlan.com (new-project board) · 3 Facebook group · 4 nadlanisraeli.co "דירה להשקעה 2026: איפה כדאי לקנות +
תשואה צפויה" · 5 brokerli.com · 6 shtiglitz.co.il "דירות זולות להשקעה" · 7 YouTube "דירה להשקעה זה חרטא" · 8 nadlanmaster projects · 9 ynet "השכונות שעשו אקזיט" ·
10 nadlan-nadlan. Also 12 madlan.co.il/for-sale (north), 13 **madlan.co.il/investors** ("נתונים וכלים לבחירת נדל"ן להשקעה"), 14 yad2.
**AI overview:** gross 2.5% to 4.5% in 2026, typical 2% to 5%; neighbourhoods with past appreciation (Afula Rova Yizrael, Beit Shemesh Ramat Ezra,
Tirat Carmel, Or Akiva); ends by asking equity, centre or periphery, first or additional home. Sources: ynet, nadlanisraeli.co.
Related: איפה כדאי לקנות דירה להשקעה בארץ · דירות להשקעה פייסבוק · ... בחול · דירות להשקעה בצפון · לוח דירות למכירה · נדלן קום · ביזפורטל נדלן · נדלן עסקאות.

### דירה להשקעה (desktop) · task 10252008-2646-0139-0000-d0fd275f90e9
1 Facebook "דירות להשקעה בכל הארץ עד 1200000" · 2 broker-t.co.il · 3 gindi "דירה להשקעה בתל אביב" · 4 nadlan-nadlan · 5 Facebook · 6 tvuah.co.il "העלויות הנסתרות" ·
7 liberkey.co.il · 8 mashkantaguru.co.il "מה זה דירה להשקעה?" · 9 brookwood.co.il · 10 nadlanmaster "invest-100-200k".
**AI overview (the one Google builds from a city table):** "2.4% עד 4.1% בשנה", then a city list taken from nadlanmaster's table (Tiberias 4.06,
Beer Sheva 3.38, Eilat 3.54, Haifa 3.03, Ashkelon 3.18, Lod 3.14, Tel Aviv 2.55, Jerusalem 2.41); purchase tax 8% to 6,055,070 then 10%;
leverage "50% to 60%"; exemption 5,654 ₪; cash-flow warning (payment often above rent); compare with bonds and funds. Cited: nadlanmaster,
fingrow, lazyinvestor, globes, moneyplan. Related: by city (Jerusalem, Tel Aviv) and by budget (עד מיליון, עד 800 אלף, עד 1.5 מיליון, מקבלן עד מיליון).

### נכסים להשקעה בישראל (desktop) · task 10252008-2646-0139-0000-0ec61b550c86
1 efgad.co.il (2018/2021) · 2 nadlanhaaretz.co.il · 3 Facebook · 4 spectra-nadlan.co.il "המדריך למשקיע נדל״ן מתחיל" · 5 financetv.co.il (TASE property indices) ·
6 Facebook · 7 tivour.com "איפה להשקיע בישראל? השוואה בין הערים (2026)" · 8 karkaotisrael.co.il (land) · 9 brokerli · ad: Ashtrom. AIO: tracks (apartments,
land, indices, urban renewal), taxes, financing; sources spectra, karkaotisrael, tivour.

### מימון נדלן (desktop) · task 10252008-2646-0139-0000-45b5521fee73
1 harel-group (credit fund for real-estate finance) · 2 g-mortgage "מימון נדל"ן ליזמים" · 3 mikumi · 4 gmfgroup "מימון ליזמי נדל"ן" · 5 topinv · video pack · 6 credit360 ·
7 osimnadlan · local pack (mortgage and finance advisers) · gov.il "הטבות והקלות במימון הדירה" at 11. AIO: closed financial accompaniment, mezzanine 15% to 30%,
senior credit, leveraging an existing asset; players (Leumi, Phoenix, Mikhlol, Bareket, Peninsula, Top Capital). **Developer intent, not ours.**

### נדלן מסחרי להשקעה (desktop) · task 10252008-2646-0139-0000-94c970b70b13
Yad2 magazine (two articles), Facebook groups, isratowers listings, yad2 and madlan listings. AIO: commercial 6% to 9% vs residential 3% to 4%,
offices / shops / logistics, VAT, vacancy. Owner: /commercial-real-estate/.

### תשואה על דירה להשקעה (desktop, tool intent) · task 10252008-2646-0139-0000-f9f3b7b7aedc
1 okam.co.il · 2 broker-re.co.il "מחשבון תשואה" · 3 hasolidit forum · 4 ethica.finance calculator · 5 moti.org.il calculator · 6 calcalon · 7 bpgroup calculators ·
8 isratop · 9 nadlanitor.com · then nadlancenter calculator, realto.co.il/tools/rental-yield, danandlan. AIO: gross and net formulas table, costs, vacancy, leverage
effect on return on equity; sources diffe-rent, nadlanitor, ethica. Related: מחשבון תשואה נדלן · חישוב תשואה על דירה עם משכנתא · מחשבון כדאיות רכישת דירה.

---

## 3. Competitor DNA and why each ranks
Read in full from raw HTML (`c-*.txt`). Counts: `depth_proof.py` (proof-before.md) plus the DNA script. depth_proof undercounts pages
whose article sits outside `<main>`/`<article>`: fair article counts are given in brackets.

| Competitor (rank) | Title / H1 / keyword placement | Size and structure | Tables, tools, data | Freshness, schema | Why it ranks |
|---|---|---|---|---|---|
| **lazyinvestor.co.il/real-estate/** (1 השקעות נדלן, 1 השקעה בנדלן, AIO source) | Title "נדל"ן למתחילים | השקעות לעצלנים"; H1 "נדל"ן למתחילים". Head term not in title or H1; "השקעות" sits in the brand | 324 by tool (fair ≈1,350 words, 61 figures). Personal voice: "data for a single home 2024", why property (leverage example 4% rise on 250k = 16% on equity), strategy, how to start (rule of thumb 500 to 550 ₪ per 100k of mortgage, 40% of disposable income, cost list broker 2%+VAT = 23,400, lawyer 0.5%+VAT = 5,850, appraisal 3,000, adviser 6,000), viewing checklist, mortgage tips, opinion, 8 FAQ | No table, no tool | Updated 20.4.2026; FAQPage, Article, Person, Product, AggregateRating | Brand authority of a top personal-finance site, named financial-planner author, beginner intent matches Google's reading of "השקעות נדלן", concrete numbers, FAQ rich data. Weak: single-home case only, 2024 data, no city data |
| **nadlancenter.co.il/article/3724** (2 השקעות נדלן, AIO source) | Exact H1 "השקעות נדל"ן - המדריך השלם לשנת 2026"; head term ~50 times | 216 by tool (fair ≈2,000 words). Sections: characteristics, types (income, speculative land, flipping, refinancing, TASE, funds), residential vs commercial, Israel, abroad, USA multifamily, taxes (purchase, betterment 25%, levy 50%), summary | No table, no tool, no sources. Content is 2020-21 (purchase tax "back to 5%", low rates) relabelled 2026 | Date 10.5.2026; NewsArticle | Domain authority of a real-estate news site, exact-match H1 and density, "2026" in title, constant news links. Weak: factually stale |
| **gemel.huji.ac.il** (1 נדלן להשקעה desktop and mobile) | "נדל"ן או שוק ההון? כך תבחרו באיזו אפשרות להשקיע" | 990 words: numbers (decade of CBS price index vs S&P 500), pros of property (leverage 50% to 75%, stability, tax: rent exempt "about 5,200"), cons (maintenance, cash flow, cost of error, liquidity), rates changing, hedging via property stocks, the fund's own property book | None | 30.11.2022; Article | Google reads "נדלן להשקעה" as "should I invest in property or in the market": a comparison answer from a regulated provident fund. Stale numbers |
| **finwiz.co.il investment-property** (3 נדלן להשקעה) | Title "דירה להשקעה - יתרונות וחסרונות"; two H1s | 1,279 words: ten decision parameters (yield, risk, tradability, liquidity, entry cost, effort, tax, capital vs cash flow, knowledge, leverage), a 10 × 6 comparison table (property in Israel / abroad / stocks / bonds / provident fund), a 1-5 score chart, six-step fit guide with a situation table, CTA to their mortgage calculator | 2 tables (87 cells), 1 SVG score chart | FAQPage, Article | The best structured "decision" page; table + chart; matches comparison intent |
| **nadlanmaster.co.il איפה כדאי לקנות דירה להשקעה** (AIO source for דירה להשקעה; 7 השקעה בנדלן) | Title "איפה כדאי לקנות דירה להשקעה ב-2026? (מדריך, דירות ונתונים)"; "דירה להשקעה" 54 times | 3,571 words, 298 figures: what is an investment flat, vs other channels, banks lend 60%+ (wrong for an additional home), project ads (30+ cards), four location factors, **a 63-city table** (average price, average monthly rent, gross yield), gross yield formula, purchase-tax history and 2026 brackets, lead form by budget, 4 FAQ | 1 table, 252 cells; data "from the government real-estate site", "updated September 2026" | 28.9.2026; FAQPage | The only page with numbers by city, refreshed, which Google lifts into the AI overview. Weak: "average" prices with no room count or quarter, rent source unclear, gross only, no tax, no mortgage, no cash flow, sales-led |
| **gindi.com realestate-investment** (6 השקעות נדלן, 11 השקעה בנדלן) | "השקעות נדל״ן בישראל - מה צריך לדעת לשנת 2025?" | 2,551 words, 40 headings: why now, strategy, considerations, cities to consider, location checklist (schools, beach, transport), 6 FAQ, many related links | No table or data; 86 images and icons | 2.3.2025; no Article schema | Developer brand authority, wide topical coverage, exact phrase 31 times |
| **climaxgrp.co.il השקעות נדלן** (9 השקעה בנדלן; local pack) | "השקעות נדל"ן בישראל - המדריך המלא לשנת 2026" | 7,326 words (largest), 1 comparison table, many sub-articles (centre vs periphery, VAT 18%, market vs property) | 1 table, 20 cells | 26.9.2026; FAQPage, Review, LocalBusiness | Length, freshness, local business signals. Sales page for land |
| **nadlanisraeli.co דירה להשקעה** (4 דירות להשקעה, AIO source) | "דירה להשקעה 2026: איפה כדאי לקנות + תשואה צפויה" | 1,705 words, 3 tables (investment types, 5 areas with price/rent/gross yield, consumer vs entrepreneur), "market April 2026", risks, 4 FAQ | 3 tables, 70 cells | 21.6.2026; FAQPage | Exact intent wording, yield table, recent |
| madlan.co.il/investors (13 דירות להשקעה; 403 to scripts, read in Chrome) | "מדלן למשקיעים - נתונים וכלים לבחירת נדל"ן להשקעה" | BETA tool hub: August 2026 counters (7,532 residential deals, investors bought 1,077, sold 1,171), featured neighbourhoods, "find my neighbourhood by budget", head-to-head neighbourhood compare, 7 FAQ | Tools behind JS; raw HTML thin | | Brand and tools; thin indexable text. The real long-term rival for the tool intent |
| openu tafnit, mynumberz, wecheck, afikil, meitav, isratop, efgad, okam, ethica, nadlanitor, broker-re | Read; general guides, a fund product (meitav), a service (isratop), calculators (ethica, broker-re, moti) | wecheck: Tax Authority counts of multi-home owners (March 2024: about 290,000 own two homes, 86,000 three) with a CBS link; calculators: gross/net/ROE | | | Topical breadth or tool intent |

Our page (`ours-investment.html`, live 1.72.519, dateModified 21.10.2026): 4,235 words, 53 figures, 1 table (18 cells), 0 tools,
10 FAQ (h3, no FAQPage), 29 headings, 0 visuals, 0 official links, schema WebPage + Article + Person. Head term in title, H1 and the first
sentence; "השקעות נדל״ן" 0 times; "דירה/דירות להשקעה" 17; "תשואה" 49.

---

## 4. Union checklist (everything any competitor covers) and what nobody covers

Covered by at least one competitor (and so required on our page, each with a dated number where one exists):
1. What property investment is; two profit sources (rent, appreciation) · 2. Who it suits; property vs capital market, with a parameter
comparison table (finwiz, gemel) · 3. Channels: buy to let, commercial, land, flipping, urban renewal, funds and REITs, TASE property shares,
abroad (nadlancenter, nadlanisraeli, AIO) · 4. Leverage example and return on equity (lazyinvestor) · 5. LTV 75/70/50 (AIO) · 6. Equity and
side costs with shekel examples (lazyinvestor, tvuah) · 7. Rule of thumb payment per 100k (lazyinvestor) · 8. Payment-to-income limit
(lazyinvestor says 40%, the cap is 50%) · 9. Gross and net yield formulas and an example (nadlanmaster, AIO) · 10. Yields by city table
(nadlanmaster, nadlanisraeli) · 11. Purchase-tax brackets for an additional home and history (nadlanmaster) · 12. Betterment tax 25% and
levy 50% (nadlancenter, AIO) · 13. Rental exemption 5,654 ₪ and the tracks (lazyinvestor, AIO) · 14. Location checklist (gindi, nadlanmaster)
· 15. Tenant profile and management (lazyinvestor) · 16. Risks and mistakes · 17. Abroad vs Israel · 18. Commercial yields (AIO) ·
19. Investor counts (wecheck, madlan) · 20. FAQ.

**Gaps no competitor covers (our edge):**
- Yields by city **and room count**, same quarter, from official medians, with the quarter printed. nadlanmaster's "average price" has no rooms and no quarter.
- **Two official rent sources side by side** (government median vs CBS average with sampling error) and the honest range they give.
- **Cash flow after a 50% investor mortgage**, city by city, and the **break-even share**: how much of the price the rent alone can carry as a mortgage.
- **Purchase tax in months of rent** (national 4 rooms: 162,304 ₪ = 34 months of the 4,825 ₪ median rent).
- **The three rental-tax tracks computed for that city's rent** (exempt, partial, 10%, marginal), with the 11,308 ₪ zero point.
- **Rent vs price trend** from CBS (rent index +3.2% in a year while the dwelling price index fell 1.8%).
- **Investor activity from the Ministry of Finance** (investors 14% of August deals, 1,077 bought, 1,171 sold, 8,707 dwellings out of investors' stock since October 2021).
- The government site's own "median rental yield" figure, explained, so a visitor can read it correctly.
- The 10.2.2027 end date of the 8% / 10% temporary order (every competitor still says 8% with no date or the old 31.12.2026).
- Official links: nadlanmaster has one link to nadlan.gov.il; nobody links the Tax Authority, Bank of Israel, CBS or the MoF.

---

## 5. What Google wants to show

- **For "נדלן להשקעה" Google reads a decision**, not a listing: should I put money into property or the market, and through which channel.
  It ranks a provident fund's comparison, a fund product, a pros-and-cons page with a comparison table, then "where to buy". Our answer
  paragraph and first table must decide with numbers: yield, leverage, tax, liquidity, against the alternatives.
- **For "השקעות נדלן" / "השקעה בנדלן" it wants a beginner's map**: how to start, channels, costs, rules of thumb (related searches: למתחילים, ספר,
  קורס, חברות השקעה, דרך שוק ההון, בחו"ל).
- **For "דירה/דירות להשקעה" it wants numbers by city and by budget**: the AI overview builds a city yield list from the one page that has a table,
  and the related searches are city and budget ("עד מיליון", "עד 800 אלף"). A dated, sourced city table with room counts and a budget filter
  is exactly what the AI overview is reaching for.
- **The AI overview repeats the same fact set** on all head queries (LTV 50%, purchase tax 8% to 10%, betterment 25%, levy 50%, exemption
  5,654 ₪, cash flow often negative). A page that states each with the official source and date is the natural citation.
- **Formats Google mixes in:** YouTube in the top 10 of 5 of the 9 desktop SERPs, Facebook groups in 5 of 9, local packs (2), a video pack
  (מימון נדלן). No PAA anywhere. "2026" appears in 6 of the 90 top-10 titles (nadlancenter, nadlanmaster, climaxgrp, nadlanisraeli, tivour),
  and the AI overviews lead with "2026" data: a dated page is what they quote.

---

## 6. Verified facts (primary sources; retrieved 25.10.2026 unless stated)

| Fact | Value | Source (date) · class |
|---|---|---|
| Purchase tax, additional home (and foreign residents, companies) | **8% on the part up to 6,055,070 ₪, 10% above**, temporary order s.9(ג1ו)(1) | Tax Authority notice "הארכת תחולת הוראת השעה לעניין מס רכישה דירה נוספת, לאור סעיף 38 לחוק יסוד הכנסת", **published 12.10.2026**, https://www.gov.il/he/pages/pa121026-2 (eyes) |
| Its end date | set to 31.12.2026; because the Knesset dissolved (Basic Law: The Knesset s.38) **extended to purchases up to and including 10.2.2027** | same notice (eyes). What applies from 11.2.2027: **unverified**, not published |
| Purchase tax, single home 2026 | 0% to 1,978,745 · 3.5% to 2,347,040 · 5% to 6,055,070 · 8% to 20,183,565 · 10% above, bands frozen 16.1.2024 to 15.1.2028 | Tax Authority buyer guide 2026 p.61-62 (`Guides_knowrightinland_2026.pdf`, code); instruction 1/2026 (code) |
| Filing and payment | buyer's declaration within 30 days (s.73(ג)); tax due on the legal date, never before 60 days (s.51) | Guide 2026 p.11 and p.28 (code) |
| Worked purchase tax | national 4-room median 2,028,800 ₪ as an additional home: **162,304 ₪**; as a single home: 1,752 ₪ (3.5% on the 50,055 ₪ above 1,978,745) | our calculation from the brackets above |
| Bank of Israel LTV | single home 75% · replacement 70% · **investment home 50%** ("דירה להשקעה" = a home that is not a single or replacement home) | Directive 329, s.2.1 to 2.3 and definitions (`raw\u1\boi\329_12.pdf`, code) |
| Payment to income | not above 50% of disposable income; above 40% a 100% risk weight | Directive 329 s.5-6 (verified in U1, code) |
| Variable share / term | variable part ≤ 66.66%; term ≤ 30 years | Directive 329 s.7-8 (U1, code) |
| Bank of Israel rate / prime | **3.25%** since 3.9.2026, unchanged 21.10.2026; prime **4.75%** (rate + 1.5); next decision 23.11.2026 | BoI SDMX MNT_RIB_BOI_D + press release (U1 25.10.2026, code + eyes) |
| Average new-mortgage rates, August 2026 | fixed not linked **4.62%** · fixed CPI-linked 3.29% · variable CPI-linked 3.19% | BoI SDMX BIR_MRTG_99 (U1, code) |
| Investment-home mortgages, August 2026 | **694 loans, 0.89 billion ₪** (≈1.28 million each) | BoI SDMX _62, _776 (U1, code) |
| Rental income: full exemption | monthly residential rent up to **5,654 ₪** fully exempt (2024, 2025 and 2026); above it the exempt amount falls shekel for shekel and is **zero at 11,308 ₪**; all the landlord's residential rents are added; monthly test | Law 1990 s.2; Knesset Research Center paper (April 2024) quoting 5,654 for 2024 (code); Tax Authority form-135 notes for tax year 2025: "התקרה המתואמת היא 5,654" (code); Kol Zchut, updated 22.2.2026: 5,654 "נכון ל-2026" (eyes). 2026 value rests on Kol Zchut plus the 2025-2027 freeze of indexation; the Tax Authority's own 2026 table was not opened (**primary for 2026: pending**) |
| Rental income: 10% track | 10% of the gross rent, no deductions or depreciation; paid once a year, **within 30 days after the tax year** (for 2026: by 30.1.2027); cannot combine with partial exemption on the same flat; on a later taxable sale the depreciation that could have been claimed is added | Income Tax Ordinance s.122; Tax Authority payment page secapp.taxes.gov.il (search result); Kol Zchut 15.3.2026 (eyes); guide 2026 p.35 on depreciation in the purchase cost (code) |
| Rental income: marginal track | taxed as non-personal-exertion income: from 31% (under 60) or from 10% (60+); expenses and depreciation deductible; 2025-2027 brackets 84,120 / 120,720 / 193,800 / 269,280 / 560,280 / 721,560 ₪ a year | Kol Zchut 15.3.2026 (eyes); Ordinance s.121 |
| Business threshold | Tax Authority position: 10 or more flats = a business; 6 to 10 examined; up to 5 may use the tracks | Kol Zchut citing the Supreme Court and the 2018 Tax Authority draft circular (eyes; secondary) |
| Betterment tax (individual) | real gain taxed by period: 47% up to 6.11.2001, 20% to 31.12.2011, **25% from 1.1.2012**; company 23%; inflationary amount 10% only for the period to 31.12.1993 | Tax Authority guide 2026 p.34-37 (code) |
| Betterment, "new linear" for a qualifying residential flat that is not exempt | real gain up to 1.1.2014 exempt, after it 25% | guide 2026 p.34 (code) |
| Deductions against betterment | purchase tax paid, lawyer, appraiser, broker, improvements, real interest | guide 2026 p.35 (code) |
| Single-home exemption ceiling (s.49ב(2)) | 5,008,000 ₪, 1.1.2024 to 31.12.2027 | guide 2026 p.61 (code) |
| VAT | 18% from 1.1.2025 | `cost.json` (Tax Authority decision page) |
| CBS rent index (series 120460, private and public rent) | September 2026 **107.5** (2024 = 100): **+3.2% in 12 months**, +0.4% in the month | CBS API, fetched 25.10.2026 (code) |
| CBS dwelling price index (40010) | 590.0, **−1.8% year on year**, −0.6% on the period (two-month window July to August 2026, published 15.10.2026; API labels it July) | CBS API (code); window label from facts.md 5c |
| CBS new dwellings price index (70000) | −0.4% year on year | CBS API (code) |
| CPI | +1.6% in 12 months to September 2026 | CBS API 120010 (code) |
| CBS average free-market rent, Q2 2026 (table 4.9) | Israel 5,085.5 ₪ (±15); 3.5 to 4 rooms 5,453.8 (±27); Tel Aviv 3.5 to 4 rooms 8,871.6 (±119); Haifa 4,060.6; Beer Sheva 3,500.8; Jerusalem 6,179.6; 20 cities and 6 districts, 2024 to 2026, with sampling errors. Quarterly means include contracts not observed that quarter (estimated); annual means include all contracts signed that year; from 2026 a "4.5+" group covers all sizes | CBS price bulletin 7/2026, table 4.9 (`a4_9_h.pdf`, code) |
| Official median rents and deal prices by city and rooms | per city and quarter: median rent 3/4/5/all rooms (to April to June 2026) and median deal price 3/4/5/all rooms (cities to January to March 2026, Israel to April to June 2026). National 4 rooms: rent **4,825 ₪**, price **2,028,800 ₪** (April to June 2026) | data.nadlan.gov.il settlement rent/buy files, version 20-08-2026, Last-Modified 20.8.2026 (code); nadlan.gov.il labels "מחיר חציוני", "הנתונים מבוססים על ניתוחי מאגרי מידע שונים, ייתכנו אי דיוקים" (eyes) |
| The government site's own "yield" | nadlan.gov.il shows per city "**תשואת שכירות חציונית שנתית**" (Tel Aviv 2.72%), a price-change figure (Tel Aviv −1.45% last year) and a cost score (10/10). For Tel Aviv the figure equals the all-rooms median rent × 12 ÷ the all-rooms annual median price the site shows (8,000 × 12 ÷ 3.53M = 2.72%); the site does not publish the formula, so treat this as our reading, checked on one city | eyes on nadlan.gov.il/?view=settlement&id=5000&page=rent + code (`trends.indexes`) |
| Investors, August 2026 (MoF chief economist) | investors bought **1,077** dwellings (−2% y/y, −6% m/m), **14%** of all deals; sold 1,171; investors' stock −94 in August and **−8,707 since October 2021** (to July 2026); 46% of investor purchases were new; about 60 bought by REIT funds; Haifa area only 139 (9%) | MoF review for August 2026 (`mof-review-082026.pdf`, code) |
| All deals, August 2026 | 7,532 incl. subsidised (−1% y/y) | same (code; facts.md 5b) |
| Multi-home owners | about 290,000 Israelis own two homes, 86,000 three (March 2024) | wecheck citing Tax Authority (**secondary**, keep out until the Tax Authority file is opened) |

**Computed (label every one "החישוב שלנו", with formula, quarter and source):**
- Gross yield = median rent × 12 ÷ median deal price, same city, same room count, same quarter (January to March 2026). 65 cities have
  4-room data for that quarter: **median 3.0%**, range 2.16% (Givatayim) to 5.36% (Nazareth; small sample, flag). National 4 rooms 2.85%
  (April to June 2026). With the CBS average rent instead: national 3.5 to 4 rooms 3.15% (CBS Q1 2026 rent ÷ national 4-room median Q1 2026).
- Investor cash flow at the cap: loan 50% of the median price, 25 years Spitzer at 4.62% (BoI August average, fixed not linked):
  **563 ₪ a month per 100,000 ₪**. Rent minus payment, before any expense: positive in **13 of 65 cities**; national −883 ₪; Tel Aviv −4,713 ₪.
- Break-even share = rent × annuity factor (177.73 at 4.62%, 300 months) ÷ price: the part of the price the rent alone carries as a
  mortgage. National 42.3%; Tel Aviv 34.0%; Haifa 49.0%; Beer Sheva 53.2%; Ashkelon 55.6%; above 50% in 13 cities.
- Equity needed = price − loan + purchase tax + lawyer 0.5% + VAT (broker, appraisal, renovation excluded unless entered).

**Unverified, kept out:** a 2026 Tax Authority table for the rental ceiling (Kol Zchut only), rates after 10.2.2027, average prime-track
margin, the multi-home owner counts (wecheck), commercial yields "6% to 9%" (AIO, no source), the definition and sample size behind
nadlan.gov.il rent medians, maintenance and vacancy "norms" (no official source: the tool takes them from the visitor), the investor
"surtax" (מס יסף) effect on rent.

---

## 7. Our page as Google gets it (raw HTML, `?x=10050`, 25.10.2026 20:10 UTC) and its gaps

What exists (keep all of it, additive law): H1, a long intro, 13 H2 sections (what it is and for whom · four channels with H3s · equity,
leverage, mortgage · gross vs net · purchase tax 8% · betterment · rental tax · where to invest in 2026 · management · risks · mistakes ·
FAQ 9 · sources), the 5-row facts table, two cluster link blocks, the lawyer box with "קבעו ייעוץ עם עורך דין" and two purchase-tax
calculator links, the site-wide WhatsApp bar ("ייעוץ חינם" twice, wa.me 3), the disclaimer and "מצאתם טעות" line.

Gaps and defects:
1. **No tool, no chart, no city data.** The only numbers by place are "המרכז והדרום הם מוקדי פעילות".
2. **A false claim**: "אין מקור ממשלתי שמפרסם תשואה" (table row and sources note). The government site publishes a median rental yield per city.
3. **Vague or stale numbers**: "בדצמבר 2025 עד פברואר 2026 נמכרו דירות בהיקף משמעותי"; the 8% order has no end date ("בתקופת ההוראה הרלוונטית").
4. **Rental tax**: states 5,654 ₪ but not the 11,308 ₪ zero point, the monthly test, the 10% payment date, or the depreciation effect on a later sale.
5. **Content-first order broken**: three long paragraphs before any CTA; the only CTA is at the bottom; a meta paragraph about "תוצאות החיפוש" and IAS 40.
6. **"טעון אימות" 10 times**: reads as hedging. Replace with the dated fact or "בודקים מול רשות המסים".
7. **0 official links** (the sources list is plain text), 0 FAQPage, no BreadcrumbList, Person schema "מערכת נדל״ן חכם" with jobTitle "עורך דין מקרקעין".
8. **Brand drift**: footer "מערכת נדל״ן חכם" and "עודכן יוני 2026" while dateModified is 21.10.2026; /investment/real-estate-yield/ title ends "| נדלן חכם".
9. **Internal links missing**: none of the 20 city investment pages, /investment-property-mortgage/, /investment-property-cashflow-calculator/,
   /real-estate-tax-advisor/purchase-tax-investor/, /real-estate-tax-advisor/capital-gains-tax-guide/, /commercial-real-estate/,
   /investment/where-to-buy-investment-apartment/, glossary (cap-rate, net-operating-income, return-on-equity, loan-to-value).
10. "השקעות נדל״ן" (the second head term, 320/mo, 333 impressions) never appears.

---

## 8. BUILD SPEC

### 8.1 Title, H1, meta
- **Title: keep the head-first structure.** Today "נדל״ן להשקעה בישראל: דירות להשקעה, תשואה ומימון | נדלן" (54) gives the page its best
  position (36) on the head term. **Switch only when the city map is live** to "נדל״ן להשקעה: דירות להשקעה ותשואה לפי עיר 2026 | נדלן"
  (53): head term first, adds the 480/mo intent "דירות להשקעה" in the same order, names the moat Google's AI overview reaches for, drops
  "מימון" whose SERP is developer credit. Re-test after six weeks.
- **H1:** "נדל״ן להשקעה בישראל: תשואה, תזרים ומס של דירה להשקעה בכל עיר"
- **Meta description:** "נדל״ן להשקעה לפי הנתונים הרשמיים: תשואה ברוטו ותזרים חודשי ב־65 ערים, משכנתא עד 50%, מס רכישה 8% עד 10.2.2027
  ושלושת מסלולי המס על שכר דירה. בודקים כל עיר במחשבון."
- First H2 carries the second head term: "השקעות נדל״ן ב־2026: מה המספרים אומרים".

### 8.2 Answer paragraph (56 words, head term first)
"נדל״ן להשקעה בישראל מכניס היום תשואה ברוטו של כ־2.9% בשנה על דירת 4 חדרים בחציון הארצי, מ־2.3% בתל אביב ועד יותר מ־4% בחלק מערי
הפריפריה (החישוב שלנו, לפי חציוני אתר הנדל״ן הממשלתי). משקיע מקבל משכנתא של עד 50% ומשלם מס רכישה של 8% מהשקל הראשון, ולכן ברוב
הערים שכר הדירה לא מכסה את ההחזר החודשי."

### 8.3 Section order (content-first, phones first: H1 → answer → CTAs → the tool → facts → article)
1. H1 · 2. answer paragraph · 3. CTA row: "לבדיקת התשואה בעיר שלכם" (anchor to the tool) · "לקבלת פרטים נוספים בוואטסאפ" (in-page wording per the
   owner's 1.10 decision; the floating "ייעוץ חינם" bar stays as is) · "פגישה עם עורך דין מקרקעין" → /real-estate-lawyer/ (existing).
4. **The tool: "מפת התשואה והתזרים"** (8.5), opened on the national 4-room example.
5. Facts strip "המספרים של היום", 8 dated numbers: 8% ו־10% עד 10.2.2027 · מימון עד 50% · ריבית בנק ישראל 3.25%, פריים 4.75% · ריבית ממוצעת
   קל"צ 4.62% (אוגוסט) · פטור 5,654 ₪ בחודש · שכר הדירה עלה ב־3.2% בשנה · מחירי הדירות ירדו ב־1.8% בשנה · משקיעים 14% מהעסקאות (אוגוסט).
   Each links its source. On the page, write ups and downs in words, not with a minus sign, and quarters as "ינואר עד מרץ 2026", not "1-3.2026".
6. "השקעות נדל״ן ב־2026: מה המספרים אומרים" with V1 (rent vs prices) and T1.
7. "תשואה לפי עיר ולפי מספר חדרים" T2 (65 cities, sortable, filter by budget "עד מיליון / עד 1.5 מיליון / עד 2 מיליון / מעל") + V2; each city row links
   its /investment/&lt;city&gt;-investment-apartment/ page where one exists.
8. "כמה מהדירה שכר הדירה מחזיק" (the break-even line, V3, T3).
9. "כמה כסף צריך באמת: הון עצמי, מס רכישה ומשכנתא של 50%" V4 + T4, link /investment-property-mortgage/ and [nadlan_tool id="pcost"] (existing tool, mounted collapsed).
10. "נדל״ן או שוק ההון" T5 (parameter comparison: yield, leverage, tax, liquidity, entry cost, effort), with our numbers, no invented returns.
11. Existing sections, kept and rewritten with dated facts: what it is and for whom · channels (apartment, commercial → /commercial-real-estate/,
    income property via fund or company → /investment/investment-via-company/, abroad → /global/) · equity, leverage → /investment/real-estate-leverage/
    · gross vs net → /investment/real-estate-yield/ · purchase tax (T6, [nadlan_tool id="ptax"] collapsed) · betterment (T7) → capital-gains guide ·
    rental tax (T8, the three tracks) · where to invest (now driven by T2) · management → /property-management/ · risks · mistakes.
12. "מי קונה היום" (MoF investor data, V5 optional).
13. "נדל״ן למתחילים: חמשת הצעדים הראשונים" (intent 4, short, links the tool presets "200 אלף", "400 אלף").
14. FAQ (30, 8.8) · 15. sources with live links + method + honesty statement + "עודכן ב" (real date) · 16. the lawyer box, cluster links and disclaimer (existing).

### 8.4 Tables (each with its source line and quarter under it)
| # | Table | Data | Refresh |
|---|---|---|---|
| T1 | המספרים של היום (the strip as a table for screen readers) | Tax Authority 12.10.2026; Directive 329; BoI SDMX; Kol Zchut / Tax Authority; CBS 120460, 40010; MoF review | monthly |
| T2 | 65 cities × {rooms 3, 4, 5}: median rent, median price, gross yield (government medians), CBS average rent and the yield on it (20 cities), the government site's own yield (all rooms), quarter. Preview rows below | data.nadlan.gov.il rent/buy; CBS 4.9 | quarterly (gov files) / monthly (CBS) |
| T3 | Break-even share and rent minus payment per city at 50% / 4.62% / 25 years, with the rate and term in the header | T2 + BoI SDMX | monthly |
| T4 | "כמה כסף צריך" for the national median and five cities: price, loan 50%, purchase tax, lawyer + VAT, equity needed, payment, purchase tax in months of rent | T2 + ptax.json + cost.json | quarterly |
| T5 | Property vs capital market vs bonds vs provident fund: leverage (50% cap), tax on income (exempt to 5,654 / 10% / marginal vs 25% capital gains), liquidity, entry cost, effort | Directive 329, Tax Authority | yearly |
| T6 | Purchase tax: additional home 8% / 10% to 10.2.2027 vs single-home brackets; worked rows at 1M, 1.5M, 2M, 3M, 6M | guide 2026, notice 12.10.2026 | on change |
| T7 | Betterment rates by period, new linear, allowed deductions | guide 2026 p.34-37 | yearly |
| T8 | Rental tax at four rents (4,000 / 5,654 / 8,000 / 11,308 ₪): exempt part, 10% track tax, note on marginal | Law 1990, s.122, Kol Zchut | yearly |
| T9 | keep the existing 5-row table, corrected (rows 4 and 5 rewritten with the gov yield and the dated deals) | existing | |

**T2 preview (4 rooms, January to March 2026 unless marked; "החישוב שלנו")**

| עיר | עמוד שלנו | רבעון | שכ"ד חציוני (אתר הנדל"ן) | שכ"ד ממוצע 3.5-4 ח' (למ"ס Q1) | מחיר חציוני | תשואה ברוטו (חציון) | תשואה ברוטו (למ"ס) | "תשואה" באתר הממשלתי | החזר על 50% | שכ"ד פחות החזר | חלק המחיר ששכ"ד מחזיק | הון עצמי נדרש |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| ישראל (ארצי) | /apartment-prices/ | 4-6.2026 | 4,825 | 5,443 ±27 | 2,028,800 | 2.85% | 3.15%* | | 5,708 | -883 | 42.3% | 1,188,674 |
| תל אביב-יפו | /investment-apartment/tel-aviv-investment-neighborhoods/ | 1-3.2026 | 10,000 | 8,843 ±118 | 5,229,800 | 2.29% | 2.03% | 2.72% | 14,713 | -4,713 | 34.0% | 3,064,140 |
| ירושלים | /investment/jerusalem-investment-apartment/ | 1-3.2026 | 7,200 | 6,139 ±77 | 2,882,400 | 3.00% | 2.56% | 2.42% | 8,109 | -909 | 44.4% | 1,688,798 |
| חיפה | /investment/haifa-investment-apartment/ | 1-3.2026 | 4,400 | 4,052 ±54 | 1,597,500 | 3.31% | 3.04% | 2.71% | 4,494 | -94 | 49.0% | 935,975 |
| באר שבע | /investment/beer-sheva-investment-apartment/ | 1-3.2026 | 3,600 | 3,467 ±58 | 1,203,200 | 3.59% | 3.46% | 3.08% | 3,385 | 215 | 53.2% | 704,955 |
| אשקלון | /investment/ashkelon-investment-apartment/ | 1-3.2026 | 4,400 | 4,000 ±48 | 1,405,800 | 3.76% | 3.41% | 3.00% | 3,955 | 445 | 55.6% | 823,658 |
| אשדוד | /investment/ashdod-investment-apartment/ | 1-3.2026 | 5,500 | 4,834 ±63 | 2,130,200 | 3.10% | 2.72% | 2.94% | 5,993 | -493 | 45.9% | 1,248,084 |
| בת ים | /investment/bat-yam-investment-apartment/ | 1-3.2026 | 6,450 | 5,297 ±101 | 2,692,600 | 2.87% | 2.36% | 2.92% | 7,575 | -1,125 | 42.6% | 1,577,594 |
| חולון | /investment/holon-investment-apartment/ | 1-3.2026 | 6,300 | 5,382 ±65 | 2,428,500 | 3.11% | 2.66% | 2.93% | 6,832 | -532 | 46.1% | 1,422,858 |
| ראשון לציון | /investment/rishon-lezion-investment-apartment/ | 1-3.2026 | 6,000 | 5,513 ±71 | 2,392,600 | 3.01% | 2.76% | 3.22% | 6,731 | -731 | 44.6% | 1,401,824 |
| רחובות | /investment/rehovot-investment-apartment/ | 1-3.2026 | 5,600 | 5,073 ±73 | 2,345,500 | 2.87% | 2.60% | 2.45% | 6,599 | -999 | 42.4% | 1,374,228 |
| פתח תקווה | /investment/petah-tikva-investment-apartment/ | 1-3.2026 | 5,900 | 5,276 ±63 | 2,444,100 | 2.90% | 2.59% | 2.46% | 6,876 | -976 | 42.9% | 1,431,998 |
| רמת גן | /investment/ramat-gan-investment-apartment/ | 1-3.2026 | 7,500 | 6,796 ±99 | 3,330,400 | 2.70% | 2.45% | 2.44% | 9,370 | -1,870 | 40.0% | 1,951,281 |
| גבעתיים | /investment/givatayim-investment-apartment/ | 1-3.2026 | 7,500 | | 4,158,900 | 2.16% | | 2.21% | 11,700 | -4,200 | 32.1% | 2,436,700 |
| נתניה | /investment/netanya-investment-apartment/ | 1-3.2026 | 6,500 | 5,252 ±90 | 2,676,100 | 2.91% | 2.36% | 2.91% | 7,529 | -1,029 | 43.2% | 1,567,927 |
| הרצליה | /investment/herzliya-investment-apartment/ | 1-3.2026 | 8,000 | 6,990 ±134 | 3,272,800 | 2.93% | 2.56% | 2.94% | 9,207 | -1,207 | 43.4% | 1,917,534 |
| רעננה | /investment/raanana-investment-apartment/ | 1-3.2026 | 6,800 | | 3,289,900 | 2.48% | | 2.51% | 9,256 | -2,456 | 36.7% | 1,927,552 |
| כפר סבא | /investment/kfar-saba-investment-apartment/ | 10-12.2025 | 6,700 | 5,989 ±110 | 2,817,000 | 2.85% (Q4 2025) | | 3.27% | | | | |
| הוד השרון | /investment/hod-hasharon-investment-apartment/ | 1-3.2026 | 6,500 | | 3,264,800 | 2.39% | | 2.73% | 9,185 | -2,685 | 35.4% | 1,912,846 |
| רמת השרון | /investment/ramat-hasharon-investment-apartment/ | 1-3.2026 | 8,500 | | 3,809,600 | 2.68% | | 2.98% | 10,718 | -2,218 | 39.7% | 2,232,045 |
| קריית אונו | /investment/kiryat-ono-investment-apartment/ | 1-3.2026 | 7,350 | | 3,197,900 | 2.76% | | 2.74% | 8,997 | -1,647 | 40.8% | 1,873,650 |
| מודיעין-מכבים-רעות | /investment/modiin-investment-apartment/ | 1-3.2026 | 6,500 | | 2,559,800 | 3.05% | | 2.96% | 7,202 | -702 | 45.1% | 1,499,787 |
| שדרות | | 1-3.2026 | 3,500 | | 954,500 | 4.40% | | 3.81% | 2,685 | 815 | 65.2% | 559,242 |
| קריית שמונה | | 1-3.2026 | 2,500 | | 690,800 | 4.34% | | 3.77% | 1,943 | 557 | 64.3% | 404,740 |
| דימונה | | 1-3.2026 | 2,600 | | 740,700 | 4.21% | | 4.23% | 2,084 | 516 | 62.4% | 433,976 |

*Israel CBS-based yield uses CBS Q1 2026 (5,442.9) over the national 4-room median of Q1 2026 (2,072,000). Full 65-city data: `data\`.
Rules: show a cell only when rent and price share the quarter; print older quarters with their label; flag cities whose 3-room or 4-room
series has gaps (Nazareth, Ariel, Kadima-Tzoran, Kfar Yona); never fill a gap. Payment = 50% loan, 25 years, 4.62%. Equity = price − loan +
purchase tax + lawyer 0.5% + VAT.

### 8.5 Infographics (inline SVG, one chart system; dataviz rules; numbers in the HTML so Google reads them)
- **V1 "שכר הדירה עולה, המחירים יורדים"**: two lines, 24 months, rebased to 100: CBS rent index 120460 (+3.2% y/y) and dwelling price index 40010
  (−1.8% y/y), CPI as a thin reference. The direct label on each line end. Source line under it.
- **V2 "התשואה לפי עיר"**: ranked horizontal bars, 4 rooms, 65 cities (top 15 and bottom 5 visible, "הצג הכול"), the national 2.85% as a reference line,
  the government-site figure as a small tick on each bar.
- **V3 "קו האיזון"**: dot plot of the break-even share per city against the 50% cap line; dots right of the line = rent carries a full investor
  mortgage (13 cities). Label: rate 4.62%, 25 years, August 2026.
- **V4 "לאן הולך הכסף"**: one stacked bar for the national median 4-room flat: loan 1,014,400 · own money 1,014,400 · purchase tax 162,304 ·
  lawyer + VAT 11,970; beside it the monthly pair rent 4,825 vs payment 5,708.
- **V5 (optional) "מי קונה"**: MoF August 2026: investors 1,077 bought vs 1,171 sold, 14% of deals.
- **Design statement (law 13.10.2026):** palette from the world of the subject: ledger and tax-form ink. Ink navy #12304F for text and axes,
  form-grid blue #3E6FA3 for the sequential yield scale (light to dark), a diverging pair for cash flow: verdigris #1F7A5A (positive) and
  signal red #B8322A (negative), cool paper #F6F8FA (not cream) behind tables. Faces: the site's NLDS Hebrew face for text, **IBM Plex Sans Hebrew**
  with tabular figures for every number (it reads like a bank statement, not like a template). Why not the default: no cream, no gold, no purple
  gradient, no soft-shadow card grid; the look is a tax table and a bank ledger, the two documents an investor actually signs. Build through
  Claude Design first (design-first law), on the site's existing tokens.

### 8.5.1 The tool: "מפת התשואה והתזרים" (new instruments tool id `invest`, mounted with [nadlan_tool id="invest"], data `data/invest.json`)
**Data build:** `tools/instruments/build_invest_data.py` = `fetch_nadlan_gov.py` + `build_yield.py` from this folder (74 cities, rent + buy files,
1 request a second) + the CBS 4.9 parse + CBS 120460/40010 series; writes per city × rooms the medians with quarters, the CBS average with
error, the government yield index, and the as-of dates. Reuses `ptax.json` (tracks + 10.2.2027 end date), `cost.json` (VAT, lawyer range,
LTV caps), `boi-rate.json`. Rates: take the BoI SDMX averages (the planned `boi-mortgage.json` of U1); `nrm.json` today cites a press source.
**Inputs (example-first, every field opens filled):** city (search box, 65 + "ישראל") · rooms 3/4/5 · price (prefilled with the median, editable) ·
rent (prefilled with the government median; switch "ממוצע הלמ"ס" where available) · buyer track: דירה נוספת (default) / דירה יחידה / תושב חוץ ·
signing date (warns after 10.2.2027) · loan share (slider to the 50% cap; shows the cap rule) · rate (4.62% with the date; chips: ממוצע קל"צ,
פריים 4.75%, צמוד 3.29%) · term (to 30 years) · lawyer % · broker % (0 by default, chip 2% + מע"מ) · renovation and furniture ₪ · monthly costs ₪
(ועד בית, ביטוח, תחזוקה; 0 by default, the visitor enters) · empty months a year (0, chips 1 / 2) · rental tax track: פטור / 10% / מס שולי with
age 60+ and other monthly income · presets "מקרים מוכנים": "דירת 4 חדרים בחציון הארצי", "עד מיליון", "200 אלף הון עצמי", "400 אלף הון עצמי",
"תל אביב 3 חדרים".
**Outputs:** own money needed (with purchase tax and costs) · purchase tax and "שווה X חודשי שכירות" · monthly payment · rent minus payment ·
monthly cash flow after costs and tax · tax under each track side by side with the cheapest marked · gross yield on price · net yield on total
cost · return on own money (cash on cash) · break-even rent · break-even loan share · scenarios: rate +1%, rent −10%, one empty month ·
the city's place on V2 and V3 · "מה הרוויחה הדירה בשנה" from the official medians (price change and rent change, both quarters printed) ·
share bar (copy, WhatsApp, print, existing engine) and a link that reopens the same numbers.
**Budget mode:** enter own money (for example 400,000 ₪) → the cities where a median 3- or 4-room flat fits at the 50% cap after purchase tax,
sorted by cash flow. This answers "מה לעשות עם 400 אלף שקל" and the "עד מיליון" related searches with official data.
**Copy rules inside the tool:** no "סימולציה", "מערכת", "ממשק", "פלטפורמה"; "החישוב שלנו" under every computed number; quarter and source on hover and in print.
**Additive:** the page's existing calculators links (/purchase-tax-calculator/) stay; [nadlan_tool id="ptax"] and [nadlan_tool id="pcost"] mount
collapsed in their sections. The separate /investment-property-cashflow-calculator/ widget is not removed (follow-up: move it to the engine).

### 8.6 THE MOAT: "כמה מהדירה שכר הדירה קונה", the yield and cash-flow map of Israel
One practical thing nobody has, built only from public official data and tied to the keyword at the moment of intent (a person deciding
whether and where to buy an investment flat):
1. For 65 cities and each room count, the gross yield from **two official rent sources** (government median and CBS average with its sampling error),
   on the **same quarter's** median deal price, with the government site's own figure beside it and explained.
2. The same flat run through the **rules an investor actually lives under**: Bank of Israel 50% cap, the official average rate of the month,
   purchase tax 8% to 10.2.2027, the three rental-tax tracks.
3. One number per city that no one publishes: **the share of the price the rent alone can carry as a mortgage** (13 of 65 cities above 50% today;
   Tel Aviv 34%). It tells the visitor in one glance whether the city is a cash-flow buy or an appreciation bet that needs money from the pocket every month.
4. A budget mode that turns "I have 400,000 ₪" into a list of cities that work, by cash flow.
5. Refreshed on a fixed rhythm (government files quarterly, CBS monthly, BoI monthly), every cell with its quarter, every computed figure labelled.
Why it holds: it needs four official feeds joined city by city and room by room, the tax rules coded, and a monthly refresh. nadlanmaster has one
undated average per city with no rooms, no tax and no mortgage; Madlan keeps its numbers behind its own models; Google's AI overview is already
looking for exactly this table. Phase 2 (same data source): neighbourhood level for the large cities (the rent files carry neighbourhood medians,
neighbourhood buy files exist).

### 8.7 Schema
Article (dateModified on every data refresh, author an identified person, not "מערכת") · FAQPage (30) · BreadcrumbList · **Dataset** for T2
(creator: Israel Tax Authority deals via data.nadlan.gov.il and CBS; temporalCoverage 2026-01/2026-06; variableMeasured rent, price, yield;
license note; our calculation stated) · WebApplication for the tool (FinanceApplication, free).

### 8.8 FAQ (30, searchers' words; answers only from section 6; no em or en dashes)
1. **מה זה נדל״ן להשקעה?** נכס שקונים כדי להשכיר או למכור ברווח, לא כדי לגור בו. הרווח מגיע משני מקורות: שכר דירה ועליית ערך.
2. **האם השקעה בנדל״ן עדיין משתלמת ב־2026?** זה תלוי בעיר ובמימון. התשואה ברוטו החציונית על דירת 4 חדרים היא כ־2.9% בארץ, ובמשכנתא של 50% שכר הדירה מכסה את ההחזר רק ב־13 מתוך 65 ערים (החישוב שלנו, ריבית 4.62%).
3. **כמה תשואה נותנת דירה להשקעה בישראל?** לפי החציונים הרשמיים של ינואר עד מרץ 2026, ב־54 מתוך 65 ערים בין 2.3% ל־3.6% בשנה על דירת 4 חדרים, עם חציון של 3.0% (החישוב שלנו).
4. **איפה התשואה הכי גבוהה על דירה להשקעה?** בערי פריפריה כמו שדרות, קריית שמונה ודימונה (יותר מ־4%), אשקלון ובאר שבע (כ־3.6% עד 3.8%). במרכז היא נמוכה יותר: תל אביב כ־2.3%.
5. **איך מחשבים תשואה על דירה להשקעה?** ברוטו: שכר דירה שנתי חלקי מחיר הדירה. נטו: שכר הדירה אחרי הוצאות, מס וחודשים ריקים, חלקי העלות הכוללת כולל מס רכישה ועורך דין.
6. **מה ההבדל בין תשואה ברוטו לתשואה נטו?** ברוטו לא מוריד כלום. נטו מוריד מס רכישה, עלויות קנייה, תחזוקה, חודשים בלי שוכר ומס על שכר הדירה. ההבדל יכול להיות חצי אחוז ויותר.
7. **כמה הון עצמי צריך לדירה להשקעה?** לפחות חצי מהמחיר, ועוד מס רכישה ועלויות. על דירת 4 חדרים בחציון הארצי (2,028,800 ₪) זה כ־1.19 מיליון ₪ (החישוב שלנו).
8. **כמה משכנתא אפשר לקבל על דירה להשקעה?** עד 50% משווי הדירה, לפי הוראה 329 של בנק ישראל. ההחזר לא יעלה על 50% מההכנסה הפנויה.
9. **האם שכר הדירה יכסה את המשכנתא?** ברוב הערים לא. בריבית 4.62% ל־25 שנה כל 100,000 ₪ משכנתא עולים כ־563 ₪ בחודש. בחציון הארצי ההחזר 5,708 ₪ מול שכר דירה של 4,825 ₪.
10. **כמה מס רכישה משלמים על דירה להשקעה?** 8% על החלק עד 6,055,070 ₪ ו־10% מעל, מהשקל הראשון. על דירה של 2 מיליון ₪ זה 160,000 ₪.
11. **עד מתי חל מס הרכישה של 8% על דירה נוספת?** הוראת השעה הוארכה לרכישות עד 10.2.2027 כולל (הודעת רשות המסים, 12.10.2026). מה יחול אחר כך עוד לא פורסם.
12. **האם משלמים מס על שכר דירה?** על דירת מגורים אפשר לבחור: פטור עד תקרה, מסלול 10%, או מס שולי עם ניכוי הוצאות.
13. **מה תקרת הפטור ממס על שכר דירה ב־2026?** 5,654 ₪ בחודש מכל הדירות יחד. מעל זה הפטור קטן שקל מול שקל ונעלם ב־11,308 ₪.
14. **מה עדיף, מסלול 10% או פטור?** עד 5,654 ₪ בחודש הפטור משתלם. מעל 11,308 ₪ אין פטור, ולרוב 10% זול מהמס השולי. בין שני הסכומים בודקים את שני המסלולים במחשבון.
15. **מתי משלמים את המס במסלול 10%?** פעם בשנה, עד 30 יום מתום שנת המס. על 2026 משלמים עד 30.1.2027.
16. **כמה מס שבח משלמים במכירת דירה להשקעה?** 25% על השבח הריאלי מ־1.1.2012 אצל יחיד. בדירת מגורים מזכה שאינה פטורה, השבח עד 1.1.2014 פטור בחישוב לינארי מוטב.
17. **מה מורידים מהשבח?** מס רכישה ששולם, עורך דין, שמאי, תיווך, שיפורים בנכס וריבית ריאלית, לפי מדריך רשות המסים.
18. **נדל״ן או שוק ההון, מה עדיף?** נדל״ן נותן מינוף עד 50% ופטור על שכר דירה עד התקרה, אבל הוא לא נזיל ודורש הון גדול. שוק ההון נזיל וזול להיכנס אליו.
19. **איך משקיעים בנדל״ן בלי הון עצמי גדול?** דרך קרנות ומניות של חברות נדל״ן, או דירה זולה בפריפריה. במשכנתא של 50% גם דירה של מיליון ₪ דורשת יותר מחצי מיליון ₪ שלכם.
20. **מה אפשר לעשות עם 400 אלף שקל בנדל״ן?** במשכנתא של 50%, אחרי מס רכישה ועורך דין, מחיר הדירה המרבי הוא כ־683 אלף ₪ (החישוב שלנו), ולכן דירה בחציון מתאימה רק בחלק מערי הפריפריה. במחשבון, בחרו "400 אלף הון עצמי" ותראו את הערים.
21. **דירה בפריפריה או דירה במרכז?** בפריפריה התשואה ברוטו גבוהה יותר ושכר הדירה מכסה יותר מההחזר. במרכז התשואה נמוכה, ובוחרים בעיקר עליית ערך ונזילות.
22. **שכר הדירה עולה?** כן. מדד שכר הדירה של הלמ"ס עלה ב־3.2% בשנה עד ספטמבר 2026.
23. **מחירי הדירות יורדים?** מדד מחירי הדירות של הלמ"ס ירד ב־1.8% בשנה (יולי עד אוגוסט 2026). מדד הדירות החדשות ירד ב־0.4%.
24. **כמה משקיעים קונים היום?** באוגוסט 2026 קנו משקיעים 1,077 דירות, 14% מכל העסקאות, ומכרו 1,171, לפי הכלכלן הראשי באוצר.
25. **מה זה התשואה שמופיעה באתר הנדל״ן הממשלתי?** "תשואת שכירות חציונית שנתית" לכל החדרים יחד. בתל אביב 2.72%, וזה בדיוק שכר הדירה החציוני (8,000 ₪) כפול 12 חלקי המחיר החציוני השנתי שהאתר מציג (3.53 מיליון ₪). במפה שלנו התשואה מחושבת לפי מספר חדרים ולפי אותו רבעון, ולכן היא יכולה להיות שונה.
26. **האם כדאי להשקיע בנדל״ן מסחרי?** זה מסלול אחר: שוכר עסקי, מע"מ וחודשים ריקים ארוכים יותר. פירוט במדריך הנדל״ן המסחרי.
27. **השקעה בנדל״ן בחו״ל או בישראל?** בחו״ל מחיר כניסה נמוך יותר, אבל מס זר, מטבע וניהול מרחוק. בישראל יש מינוף של 50% ופטור על שכר דירה עד התקרה.
28. **מה זה cap rate ו־NOI?** NOI הוא ההכנסה מהנכס אחרי הוצאות התפעול. cap rate הוא NOI חלקי מחיר הנכס. הסבר מלא במילון.
29. **כמה דירות אפשר להשכיר לפני שזה נחשב עסק?** לפי עמדת רשות המסים, 10 דירות ומעלה נחשבות עסק, ובין 6 ל־10 בודקים לפי קריטריונים.
30. **האם צריך עורך דין ושמאי בעסקה להשקעה?** כן. עורך דין בודק זכויות, שעבודים, חוזה ומס, ושמאי בודק שווי ותכנון. מס הרכישה לבדו גדול מכל שכר הטרחה.

(FAQ 20 arithmetic: own money 400,000 = 0.5P + 0.08P + 0.0059P → P ≈ 683,000 ₪. FAQ 9: 1,014,400 ₪ loan.)

### 8.9 Honesty target (depth_proof metrics; competitors = the 8 in proof-before.md)
| Metric | Ours now | Competitor max (who) | Competitors' sum | Target | Note |
|---|---|---|---|---|---|
| words | 4,235 | 7,326 (climax) | 17,936 by tool; ≈20,750 with the two undercounts corrected | ≥ 7,500 | beat the max; the sum is not a goal (no padding) |
| figures | 53 | 298 (nadlanmaster) | 615 | **≥ 1,000** | T2 alone carries 65 × 12 |
| tables | 1 | 3 (nadlanisraeli) | 8 | **≥ 9** | T1 to T9 |
| table cells | 18 | 252 (nadlanmaster) | 429 | **≥ 1,000** | |
| tools | 0 | 0 | 0 | **3** (invest + ptax + pcost) | nobody in the head SERPs has a tool |
| FAQ | 10 | 13 (gindi) | 34 | 30 + FAQPage | beat the max |
| headings | 29 | 40 (gindi) | 141 | ≥ 45 | |
| visuals | 0 | 86 (gindi, decorative images and icons) | 222 | 5 data charts | honesty statement names it: gindi has more pictures; only finwiz has a data chart (one 1-5 score chart) |
| official sources | 0 | 1 (nadlanmaster) | 1 | **≥ 15** live links | Tax Authority ×5, BoI ×3, CBS ×4, data.nadlan.gov.il, MoF, Knesset research |
| schema | Article | FAQPage on 5 of 8 | | Article + FAQPage + BreadcrumbList + Dataset + WebApplication | |
| updated | 21.10.2026 | 28.9.2026 (nadlanmaster) | | shown on page, real date | |

**Honesty statement (draft for Ben to sign, Hebrew, after the release is measured):** "בדקנו את שמונת העמודים שגוגל מדרג גבוה על נדל״ן להשקעה
ב־25.10.2026. העמוד שלנו מציג יותר נתונים, יותר טבלאות ויותר מקורות רשמיים מכל אחד מהם ומכולם יחד, והוא היחיד עם מחשבון ועם תשואה ותזרים לכל
עיר לפי מספר חדרים. בעמוד אחד יש יותר תמונות משלנו. כל מספר בעמוד מופיע עם המקור והתאריך שלו, וכל חישוב שלנו מסומן." Replace the counts with
the after-proof numbers before publishing.

**Facts list the page must carry (section 6, each with link and date):** 8%/10% to 10.2.2027 · single-home brackets · 30/60 days · 50% LTV and its
definition · 50% payment-to-income · 3.25% / 4.75% · 4.62% / 3.29% / 3.19% (August) · 694 investment-home loans · 5,654 / 11,308 · 10% track by
30.1.2027 · marginal 31% / 10% at 60+ · business threshold (secondary, labelled) · betterment periods and 25% · new linear to 1.1.2014 · deductions ·
CBS rent +3.2% · CBS prices −1.8% · CBS new −0.4% · CPI 1.6% · CBS average rents (4.9) · official medians (Q1/Q2 2026) · the government yield
definition · MoF investors 1,077 / 14% / 1,171 / −8,707.

---

## 9. Findings to report (no redirects, no noindex, no new URLs; owner decisions where marked)
1. **/investment-apartment/** ("דירה להשקעה בודקים במספרים, מסמכים ותזרים", 0 impressions in 90 days) and **/investment/apartments-for-investment/**
   both hold the "investment apartment" intent next to the hub. Re-target their content to their sub-intents (checks and documents; how to choose);
   show the three side by side to Ben.
2. **/buy-or-rent/** and **/buy-vs-rent/** are two live "קנייה או שכירות" calculators (205 vs 43 impressions). Duplicate pair: owner's call.
3. **"מס על שכר דירה"** (260/mo) has no owner page; /rental-income-tax/ is 404. /investment/ carries the topic for now. A dedicated page is the owner's call.
4. **"מימון נדלן"** (developer credit) has no owner; not winnable from /investment/. Owner's call.
5. **Foreign-language demand** (Italian ≈345, Portuguese ≈257, Spanish ≈178 impressions in 90 days) lands on a Hebrew page. Owner's call on language hubs.
6. The page's claim that no government source publishes yield is wrong (fix in this release).
7. "עודכן יוני 2026" vs dateModified 21.10.2026; Person "מערכת נדל״ן חכם" as a lawyer; "| נדלן חכם" on /investment/real-estate-yield/.
8. /investment-property-cashflow-calculator/ runs a hand-made widget with hard-coded example values (1,800,000 / 160,000 / 950,000 / 5,200 / 3,900),
   outside the instruments engine. Follow-up: rebuild on `invest` data, keep every field.
9. `nrm.json` cites a press article for BoI averages; switch to the SDMX source when U1's `boi-mortgage.json` exists.

## 10. Follow-ups outside this page (for the coordinator)
- Neighbourhood-level yield for Tel Aviv, Jerusalem, Haifa, Beer Sheva (phase 2 of the moat, same data source).
- Each /investment/&lt;city&gt;-investment-apartment/ page mounts [nadlan_tool id="invest" city="…"] with its own city pre-selected (20 pages, paced, not one day).
- Quarterly refresh job for `invest.json` (government files were last updated 20.8.2026; the next file should carry April to June 2026 city prices).
- Open the Tax Authority 2026 rental-ceiling source (to move 5,654 for 2026 from Kol Zchut to primary).
