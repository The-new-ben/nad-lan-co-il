# Kikar HaMedina tools cluster: plan (21.10.2026)

Research and planning only. Nothing on the live site was changed, nothing was created, committed or pushed.
Owner order: Ben 15.10.2026 (tools for the whole buyer journey around Kikar HaMedina, one search intent per page,
everything linked to /projects/hamedina/, English too). Engine and rules: docs/loop/TOOLS-LOOP.md.

**Inputs used:** live sitemap index fetched 21.10.2026 (4,571 URLs); Search Console sc-domain:nad-lan.co.il,
21.7-19.10.2026, query+page (9,545 rows, 93,397 impressions); DataForSEO Google Ads volumes 21.10 (Hebrew/Israel 131
phrases; English 63 phrases in Israel, US, UK, France) + the 14.10 catalog keywords.csv where it already covered a phrase;
13 fresh SERPs (google mobile, 21.10 16:29-16:30 UTC: 10 Hebrew Israel, 2 English Israel, 1 English US) + 5 SERPs reused
from the 14.10 catalog; url_word_audit.py (live run for "arnona", then the same 21.10 sitemap list via --csv for 58 tokens).
**DataForSEO spend: USD 0.57** (balance 34.07 → 33.50). One Hebrew volume call was paid twice because the AI-mode
answer was cut to 10 rows.

**Rules kept:** "no data" (NA) is not zero; volumes are Google Ads 12-month averages; Google groups close variants (for
example מחשבון משכנתא / מחשבון משכנתאות, both 33,100), so cluster sums are UPPER bounds. No 301, no noindex, no new
URL on an owned head word.

---

## 1. Ranked table

Kikar link rule for every row: the tool carries one worked example "an apartment in a new tower at Kikar HaMedina"
(the published deal range on the live Kikar page: ₪9.58-10.63M, ~₪71,000/m², labelled "מידע גלוי") with one contextual
link to /projects/hamedina/ (varied anchor, never in the title); the Kikar page links down to the tool from the section
that owns that question. "כיכר המדינה" stays out of every tool title.

| # | Tool | Intent (one line) | Target URL | Head phrase (vol/mo) | Cluster vol (HE IL; EN IL/US/UK/FR) | GSC 90d on target (impr / clicks / pos) | Best competitor and its gap | Effort | Link to /projects/hamedina/ and back |
|---|---|---|---|---|---|---|---|---|---|
| 1 | Home value from official medians | "What is my apartment worth" with the official neighbourhood median by rooms and quarter | UPGRADE /property-value-estimator/ | הערכת שווי דירה 590 | 3,270 (value phrases; +2,830 deal-lookup phrases owned by nadlan.gov.il) | 4,081 / 20 / 23.1 (the site's best tool page) | yadata (yad2), madlan, dirobot (top 3, 14.10). Our page today makes the visitor type the area price per m² (catalog). Gap to prove: official Tax Authority median by rooms per quarter for the street's neighbourhood, next to a new tower's published deals, with an honest range | M | Preset "new tower near the square" → Kikar; Kikar "המחירים סביב הפרויקט" → tool |
| 2 | Purchase tax 2.0 | Exact purchase tax: single home, additional home, new immigrant, foreign resident | UPGRADE /purchase-tax-calculator/ | מחשבון מס רכישה 4,400 | 22,380 (upper bound; מחשבון/סימולטור 4,400 likely one group); EN 60/30/30/20 | 953 / 0 / 56.9 | maor-law (non-apartment asset), homeway, yuvalim-finance ("2026 single + additional"), michale; AI overview cites gov.il + hon. Today our tool has 3 inputs. Gap to prove: all four tracks in one, effective rate, link to the full cost | S | Example "₪10M as an additional home / foreign resident" → Kikar; Kikar "כמה עולה לקנות... מס רכישה ומשכנתא" → tool |
| 3 | Total purchase cost | "How much cash do I really need": tax + lawyer + broker + appraiser + mortgage fees + VAT | UPGRADE /apartment-purchase-cost-calculator/ | מחשבון דירה 320 (מחשבון קניית דירה 40) | 660 | 259 / 0 / 55.6 ("מחשבון קניית דירה" 142 impr) | SERP not checked in this pass. Our tool asks for the tax by hand (catalog). Gap: auto tax from tool 2, sourced fee ranges with dates | S (after 2) | Same Kikar section → tool; example → Kikar |
| 4 | Tel Aviv arnona calculator | Yearly and bi-monthly arnona by zone, area and building class, from the official 2026 order | NEW /arnona/ (token free; passed audit) + /en/arnona/ later | ארנונה תל אביב 9,900 | 10,650 TLV + calculator phrases; 36,860 incl. ארנונה 14,800, other cities, discounts; EN 2,730/500/110/100 (arnona 2,400 IL) | none (no page owns it) | kolhabait.com (#2: area, building type, year, zone, bill check), calculatzia (#3: class + area + discount); municipality owns the navigational top. Gap: both need the visitor to KNOW his zone and class; no address or map lookup, no tower example, no monthly-cost view, no English | M | Kikar new "monthly cost" line (V5 build list item 9) → /arnona/; /arnona/ tower example → Kikar (only after the order confirms the towers' zone/class) |
| 5 | Non-resident mortgage + foreign buyer cost (EN) | Mortgage at 50% LTV, payments in USD/EUR at the Bank of Israel rate, total cost to buy from abroad | UPGRADE /israel-mortgage-non-residents/ (EN), then /en/buy-property-in-israel/ | israel mortgage calculator 260 (IL-en) | EN mortgage 330/70/20/20; EN buying-from-abroad 100/170/90/60 | 276 / 0 / 65.5 and 633 / 0 / 63.7 | firstisrael, bankhapoalim, israelpropertyhub, semerenkogroup ("payment + total cash to close"), sellingisrael; no AI overview. Listing portals (Properstar, thetelavivi) own "buy apartment in tel aviv". Gap to prove: 50% non-resident cap + foreign-resident tax + FX in one flow | M | /projects/hamedina-en/ "Buying from abroad" → tools; tools' example → /projects/hamedina-en/ |
| 6 | Mortgage 2.0 with area price presets (HE) | Monthly payment and stress test at the area's price level | UPGRADE /mortgage-calculator/ (catalog item 15) | מחשבון משכנתא 33,100 | ~45,600 counting the 33,100 group once | 7,976 / 1 / 48.5 | yeadim-bit (aggregator), nitzanm, lemon, mercantile (14.10). Gap per catalog: rate/CPI shock, BoI directive 329 rules | L | Kikar mortgage line opens the tool with the price filled; tool preset → Kikar |
| 7 | Affordability (Zillow, PropertyGuru) | "How much can I borrow / buy" from income, by BoI caps | UPGRADE /mortgage-calculator/mortgage-repayment-capacity/ (owns the H1, has no tool) | כמה משכנתא אפשר לקחת 210 (catalog) | 380 | 0 rows; the query lands on /mortgage-calculator/ (287 impr, pos 64) | not checked in this pass | S | Result "what this budget buys near the square" → Kikar; Kikar → tool |
| 8 | Rent and yield | Gross and net yield with owner costs (arnona, fees, vacancy) and official rent levels | UPGRADE /investment-property-cashflow-calculator/ (title already "מחשבון תשואה לדירה להשקעה") | מחשבון תשואה 2,400 | 3,400 tool phrases (+3,090 rental-listing phrases not targeted); EN rent phrases 680/770/200/90 are listing intent | 1 / 0 / 5 | Top 5 for מחשבון תשואה are generic finance calculators (houseofinance, financialstar, financialplanning...), none real-estate: a gap, but the head intent is mostly financial | M | Kikar "למכירה ולהשכרה" → tool; example → Kikar |
| 9 | Price history, scenarios and neighbourhood price map | Price trend 2021-2026 by rooms around the square, CBS index, scenario fan; map of medians by neighbourhood | UPGRADE /tel-aviv-apartment-prices/ (title already "...ומגמה") | מדד מחירי הדירות 880 | 950 (+ TLV price phrases ~100) | 72 / 0 / 16.8 | nadlancenter, facebook, diffe-rent, ynet, cbs.gov.il; AI overview yes; no tool in top 5 | M | /north-tel-aviv/rova-4/ and the TLV page → Kikar; Kikar price section → history |
| 10 | Tower management-fee estimator | Monthly fee range for a luxury tower by facilities (pool, spa, gym, lobby staff) | UPGRADE /guides/new-project-management-fees/ (he; en sibling) | דמי ניהול 480 | 870 (דמי ניהול + חברת ניהול בניין); EN vaad bayit 30 IL | none (guide); tower-fee queries land on the COMMERCIAL fees page | ועד בית SERP (14.10): tasalaw, shchenim, info.org.il, ivb, square-management: guides, no estimator | M (data) | Kikar facilities section → estimator; guide → Kikar |
| 11 | Building and contents insurance | How much cover to buy (reconstruction cost, not price) and what drives the premium | UPGRADE /mortgage-home-insurance/ | ביטוח דירה 3,600 | 7,730 (CPC $26-69: insurers bid) | 3 / 0 / 6.7 | Clal, Harel, bestie (live comparison), 555, AIG: real quote engines. We cannot quote; we can size the cover | M | Kikar monthly-cost line → tool; example → Kikar |
| 12 | Travel time from the apartment | Walk / bike / transit time to Azrieli, HaShalom, the sea, the planned Purple line | SECTION on /projects/hamedina/ + /north-tel-aviv/rova-4/ (no new URL) | (transit phrases are NTA/Moovit intent: רכבת קלה תל אביב 4,400, הקו הסגול 3,600) | not counted as tool traffic | n/a | mako, tel-aviv.gov.il, nta, moovit, tevelmetro; nobody answers "from this home" | M | Lives on the Kikar page itself |
| 13 | Buy vs rent presets | Break-even year for the area's price and rent | UPGRADE /buy-or-rent/ (duplicate with /buy-vs-rent/ waits for Ben) | האם כדאי לקנות דירה 20 | 50 | 211 / 0 / 77.7 | not checked | S | Preset → Kikar |

## 2. Build order (expected traffic x fit; ship-in-one-turn on a page with impressions first)

1. **Home value, /property-value-estimator/** (4,081 impr at pos 23: the closest page to page one). Data in hand: the official
   neighbourhood medians (docs/research/2026-10-07-city-prices/neighbourhoods-all.csv and the 5 neighbourhoods around the
   square in 2026-10-07-kikar-prices/nadlan-gov-medians.csv), street → neighbourhood from the same official summaries.
2. **Purchase tax 2.0, /purchase-tax-calculator/** (953 impr, cluster 22K). Brackets are official and frozen to 15.1.2028
   (costs.md). One check first: the additional-home 8%/10% temporary provision runs to the end of 2026; its extension is
   not verified (catalog). Foreign residents on the additional-home track: confirm on the Tax Authority site.
3. **Total cost, /apartment-purchase-cost-calculator/**: same engine as 2, one short turn after it.
4. **Arnona, NEW /arnona/** (Tel Aviv first; the biggest new-page opportunity, 9,900/mo head). Needs the 2026 order parsed
   to dated JSON before any number is shown.
5. **English non-resident mortgage + foreign cost, /israel-mortgage-non-residents/ then /en/buy-property-in-israel/**
   (909 impr together; reuses 2 and the BoI data already live).

Then: 6 Mortgage 2.0 (big, coordinate with catalog item 15) · 7 affordability · 8 yield · 9 history + map ·
10 management fees · 11 insurance · 12 travel-time section (Kikar loop, Claude Design first) · 13 buy-vs-rent presets.
The Kikar-page side of every link (new "monthly cost" line, section links) goes through the Kikar loop laws
(design version first, the Kikar runner, content-first check).

## 3. Data: what we may not have, and the official source to use

| Tool | Missing data | Official source / honest fallback |
|---|---|---|
| 1, 9 | Per-deal prices and ₪/m² by STREET | nadlan.gov.il per-deal API needs reCAPTCHA tokens: not bypassed (07.10 README). Use the official neighbourhood/city summaries (median by rooms per quarter, file 20.8.2026). Per-street ₪/m² needs a person's browser session or an official data request to the Tax Authority (Ben's choice). Coverage of our wp_nadlan_deals cache: unverified |
| 2, 3, 5 | Additional-home rate after 2026; foreign-resident track | Tax Authority instruction 1/2025 (costs.md); verify the temporary provision on gov.il before release. Lawyer, broker, appraiser = market ranges with dates (costs.md section 3), labelled as ranges |
| 4 | Zone by address; the towers' zone and class | Tel Aviv "ארנונה כללית לשנת 2026" order (tel-aviv.gov.il, rank 1 for מחשבון ארנונה תל אביב). Whether the city GIS publishes the zone layer: unverified. Until then the visitor picks the zone, and the tower example stays off |
| 5, 6, 7 | Non-resident LTV clause; FX series | Bank of Israel directive 329 (LTV 75/70/50, payment-to-income 50% per catalog); BoI SDMX exchange rates (same feed as data/boi-rate.json; series id to confirm) |
| 8 | Rent levels; any Kikar rent | CBS average rent by city and rooms (quarterly). The towers are not yet occupied: no tower rent is shown, never estimated as fact |
| 9 | Long history | CBS dwellings price index by district + the 2021-Q1 to 2026 medians already saved |
| 10 | Tower management fees | No official source. Developer sale specifications and dated press only; unknown = omitted |
| 11 | Premiums; reconstruction cost per m² | No official premium table found in this pass (a Capital Market Authority comparison: verify). Reconstruction cost needs a dated source (appraiser or paid price list) |
| 12 | Purple line times | NTA published route and stations; MOT GTFS for running lines; OSM for walk/bike. Purple line not running: show distance to the planned station, no time |

## 4. Dropped or merged, and why

| Idea | Decision | Why |
|---|---|---|
| 10 Renovation cost per m² by finish | DROP from this cluster | No official or open price data (Dekel is paid; others are crowd price lists); ~590/mo national with established calculators (midrag, top-renovations, shiplus); a new-tower buyer's real question is buyer changes (/guides/new-apartment-buyer-changes/, volumes NA). Stays in the main catalog |
| 12 Sun, view, shade by floor | DROP as a page | Already live on the Kikar page (tower → floor → direction picker, sun fold); phrases ~60/mo; a separate page would compete with the Kikar page |
| 13 Project vs project | DROP as a page | /compare/ exists (conversion feature, not indexed by design) and the neighbours' comparison table runs on project pages; השוואת דירות 10/mo |
| 15 Price heat map | MERGE into 9 | "map" is owned by /urban-renewal/map/; מפת מחירי דירות 10/mo; official data is by neighbourhood, so a choropleth of medians, not a street heat map |
| 11 Travel-time as a page | SECTION only | "line", "rail", "light" are owned by /jerusalem-green-line-light-rail-property-2026/; transit SERPs belong to NTA/Moovit |
| FX converter page (שער יציג דולר 33,100; shekel to dollar 74,000 IL-en) | DROP | Off-intent; BoI and finance sites own it. A USD/EUR toggle inside the English tools only |
| 14 Foreign-buyer package as a NEW page | UPGRADE instead | Three English pages already split this intent (finding below) |

## 5. Findings to report (no redirect proposed)

- "כמה משכנתא אפשר לקחת" (287 impr, pos 64) lands on /mortgage-calculator/, not on /mortgage-calculator/mortgage-repayment-capacity/ (0 rows), which owns that H1.
- Residential tower-fee queries ("דמי ניהול במגדלים", "מה דמי ניהול בפרויקטים יוקרתיים") land on /commercial-real-estate/commercial-property-management-fees/; the residential guide has 0 rows.
- Three English foreign-buyer pages split one intent: /en/buy-property-in-israel/ (633 impr), /buy-property-israel-foreign-buyers/ (98), /buying-real-estate-israel-foreign-investor/ (93). Owner's decision.
- /en/buy-property-in-israel/ gets at least 281 impressions from Portuguese and Spanish queries ("comprar apartamento em israel sendo estrangeiro" 201, pos 62): a pt/es demand signal.
- /projects/hamedina/ is the site's de facto page for generic tower queries: "מגדלים בתל אביב" 37 impr pos 35, "מגדלים תל אביב" 36 pos 27, "מגדלי מגורים בתל אביב" 24 pos 19; the project's own name gets 16 impr (pos 15).
- English demand for the project is real: kikar hamedina towers 320/mo and kikar hamedina 320/mo in Israel (English), US 30-70.
- /buy-or-rent/ vs /buy-vs-rent/ duplicate (catalog finding 1) is still open.

---

## Appendix A. Keyword clusters (head + variants, monthly, Google Ads; NA = no data)

| Tool | Head | Variants |
|---|---|---|
| 1 Home value | הערכת שווי דירה 590 | הערכת שווי דירה בחינם 590 · כמה שווה הדירה שלי 480 · הערכת שווי נכס 260 · שווי דירה 210 · מחשבון שווי דירה 210 · הערכת שווי 140 · בדיקת שווי דירה 110 · שווי דירה לפי כתובת 50 · (deal lookup: עסקאות נדלן 2,400, עסקאות נדלן לפי כתובת 260) |
| 2 Purchase tax | מחשבון מס רכישה 4,400 | מס רכישה 6,600 · סימולטור מס רכישה 4,400 · מס רכישה דירה ראשונה 2,400 · מס רכישה דירה שנייה 1,300 · מדרגות מס רכישה 720 · מדרגות מס רכישה 2026 320 · מס רכישה תושב חוץ 40 · מס רכישה לתושב חוץ 20 · EN israel purchase tax 20 IL |
| 3 Total cost | מחשבון דירה 320 | עורך דין לקניית דירה 90 · מחשבון קניית דירה 40 · כמה עולה שמאי 40 · כמה עולה עורך דין לקניית דירה 40 · עמלת תיווך קניית דירה 40 · שכר טרחת עורך דין קניית דירה 30 · עלויות קניית דירה 10 · עלויות נלוות לקניית דירה NA |
| 4 Arnona | ארנונה תל אביב 9,900 | ארנונה 14,800 · הנחה בארנונה 2,900 · מחשבון ארנונה 260 · מחשבון ארנונה תל אביב 170 · צו ארנונה תל אביב 110 · חישוב ארנונה 110 · תעריף ארנונה תל אביב 30 · אזורי ארנונה תל אביב 20 · EN arnona 2,400 IL / 480 US · arnona tel aviv 320 IL |
| 5 EN mortgage + foreign | israel mortgage calculator 260 IL | mortgage in israel 70 IL / 30 US · buying property in israel 30 IL / 50 US / 40 UK · can foreigners buy property in israel 10 / 30 US · how to buy property in israel 10 / 20 US · israel purchase tax 20 IL · open bank account in israel non resident 10 · משכנתא לתושבי חוץ 40 · mortgage israel non resident NA |
| 6 Mortgage 2.0 | מחשבון משכנתא 33,100 | מחשבון משכנתאות 33,100 (same group) · חישוב משכנתא 1,600 · משכנתא מחשבון 1,600 · מחשבון משכנתא פשוט 1,600 · מחשבון משכנתא לפי החזר חודשי 590 · סימולטור משכנתא 590 · החזר משכנתא על 2 מיליון 70 · משכנתא על 3/5 מיליון NA |
| 7 Affordability | כמה משכנתא אפשר לקחת 210 | מחשבון זכאות משכנתא 110 · יחס החזר משכנתא 30 · כושר החזר משכנתא 10 · כמה משכנתא מגיע לי 10 · מחשבון יכולת רכישה 10 · כמה דירה אני יכול לקנות NA |
| 8 Yield | מחשבון תשואה 2,400 | מחשבון תשואה נדלן 320 · מחשבון שכר דירה 260 · מחירי שכירות 90 · תשואה על ההון 40 · שכר דירה בתל אביב 30 · שכר דירה ממוצע בתל אביב 20 · תשואה נטו 10 · אומדן דמי שכירות 10 · (listing: דירות להשכרה בתל אביב 2,900, דירות להשכרה בצפון תל אביב 170, דירות להשכרה כיכר המדינה 90) |
| 9 History + map | מדד מחירי הדירות 880 | מחירי דירות בתל אביב 50 · מחיר דירה בתל אביב 50 · עליית מחירי דירות 10 · עליית ערך דירה 10 · מחשבון עליית ערך דירה 10 · מחירי דירות בתל אביב לאורך השנים 10 · מפת מחירי דירות 10 · EN israel housing prices 40 IL / 50 US / 40 UK |
| 10 Management fees | דמי ניהול 480 | חברת ניהול בניין 390 · ועד בית 720 (belongs to /property-management/) · דמי ועד בית 20 · כמה משלמים ועד בית 10 · ועד בית ממוצע 10 · דמי ניהול במגדל מגורים NA · EN vaad bayit 30 IL |
| 11 Insurance | ביטוח דירה 3,600 | ביטוח מבנה 880 · ביטוח דירה השוואת מחירים 720 · השוואת ביטוח דירה 590 · ביטוח תכולה 590 · ביטוח מבנה ותכולה 260 · כמה עולה ביטוח דירה 170 · מחשבון ביטוח דירה 140 · ביטוח דירת יוקרה NA |
| 12 Travel (section) | רכבת קלה תל אביב 4,400 | הקו הסגול 3,600 · הקו האדום תחנות 880 · תחנת השלום 260 · מפת רכבת קלה תל אביב 210 · מסלול הקו הסגול 170 · תחנות הקו הסגול 110 · EN tel aviv light rail 480 IL / 170 US |
| 13 Buy vs rent | האם כדאי לקנות דירה 20 | לקנות דירה או לשכור 10 · לשכור או לקנות דירה 10 · לקנות או לשכור דירה 10 · כדאי לקנות דירה עכשיו NA |
| Kikar (context) | כיכר המדינה תל אביב 480 | מגדלי כיכר המדינה 260 · פרויקט כיכר המדינה 170 · דירות להשכרה כיכר המדינה 90 · מגדלי כיכר המדינה למכירה 70 · דירות למכירה כיכר המדינה 20 · EN kikar hamedina towers 320 IL · kikar hamedina 320 IL / 70 US |

Full rows (614, with GSC impressions per query): keywords.csv in this folder.

## Appendix B. Search Console rows used (21.7-19.10.2026)

Page totals: in the ranked table. Full filtered rows by intent (1,181): gsc-intents.csv in this folder. Top rows per intent
(query: impressions / clicks / avg position → top page):

| Intent | Rows (impr / clicks / pos → page) |
|---|---|
| Kikar (11 queries, 51 impr) | kikar hamedina towers 23/0/23.9 → /projects/hamedina-en/ · מגדלי כיכר המדינה 16/0/14.8 → /projects/hamedina/ · מגדלי כיכר המדינה למכירה 2/0/15.0 · מגדלי כיכר המדינה מחיר 1/0/68 → / |
| Value (196 q, 3,521 impr) | הערכת שווי דירה 480/1/20.6 · הערכת שווי נכס 452/3/20.4 · הערכת שווי 297/0/30.3 · כמה שווה הדירה שלי 182/1/30.7 · בדיקת שווי נכס 171/0/20.5 (all → /property-value-estimator/) · מחיר דירה חדשה בתל אביב 116/0/29.9 → /projects/ (53 of them → /tel-aviv-apartment-prices/, pos 12) |
| Purchase tax (69 q, 779 impr) | סימולטור מס רכישה 195/0/51.1 · מחשבון מס רכישה 177/0/54.4 · מחשבון מס רכישה דירה ראשונה 95/0/53.2 · חישוב מס רכישה בהעברה ללא תמורה 65/0/74.5 (all → /purchase-tax-calculator/) |
| Total cost (75 q, 790 impr) | מחשבון קניית דירה 142/0/51 · עלויות רכישת דירה מקבלן 67/0/61 (→ /apartment-purchase-cost-calculator/) · דמי תיווך 174/0/40.9 → commercial brokerage page · הערכת שמאי לדירה 53/0/33.3 → /property-value-estimator/ |
| Mortgage (360 q, 8,591 impr) | מחשבון משכנתא 519/0/48.3 · משכנתא לדירה להשקעה 434/0/38.9 → /investment-property-mortgage/ · מחשבון משכנתא הפוכה 429/0/54.6 · חישוב משכנתא 311/0/47.2 · מחשבון משכנתא לפי החזר חודשי 289/0/40.4 · כמה משכנתא אפשר לקחת 287/0/64.4 (→ /mortgage-calculator/) |
| Foreign (31 q, 764 impr) | israel mortgage for foreigners 168/0/64.9 → /israel-mortgage-non-residents/ · buying apartment in israel from usa / uk / abroad 143/0/56 · how to buy an apartment in israel 127/0/78.5 → /en/buy-property-in-israel/ · israel investment property for americans 92/0/78.1 → /buying-real-estate-israel-foreign-investor/ · buying property in israel as a foreigner 35/0/69.5 → /buy-property-israel-foreign-buyers/ |
| Yield / rent (85 q, 263 impr) | אומדן דמי שכירות 54/0/34 → glossary דמי שכירות ראויים · מחשבון שכר דירה 11/0/67.1 → /buy-or-rent/ · מחשבון שכירות 7/0/54.4 |
| Arnona (7 q, 13 impr) | all ≤5 impr, none on a residential page (they land on commercial pages, /projects/ and /) |
| Management fees (8 q, 17 impr) | דמי ניהול משרדים 4/0/20.2 · דמי ניהול במגדלים 1/0/38 · מה דמי ניהול בפרויקטים יוקרתיים 1/0/20 (→ commercial fees page) |
| Insurance (5 q, 29 impr) | ביטוח משכנתא מחשבון 21/0/46.4 → /mortgage-calculator/ |
| Luxury / towers (233 q, 1,504 impr) | פרויקטי יוקרה בתל אביב 112/0/59.9 → /luxury-tel-aviv/ · מגדלים בתל אביב 37/0/34.9 · מגדלים תל אביב 36/0/26.9 (→ /projects/hamedina/) |
| Transit (16 q, 25 impr) | address queries only (דרך השלום 87...), nothing on transit intent |

## Appendix C. url_word_audit results (21.10.2026; "arnona" run live, the rest on the same day's sitemap list)

| Token | Owners | Use |
|---|---|---|
| arnona | 0 | /arnona/ PASSES (new) |
| municipal, purple, metro, transit, commute, travel, heatmap, appreciation, forecast, history, trend, vaad, committee, rental, compare, comparison, sun, orientation, shade, afford, affordability, monthly, currency, usd, finish, street, square | 0 | free (no page proposed on them in this plan) |
| line, rail, light | 1: /jerusalem-green-line-light-rail-property-2026/ | travel tool cannot take them → section |
| map | 1: /urban-renewal/map/ | price map → section of /tel-aviv-apartment-prices/ |
| index | 1: /new-projects/construction-input-index/ | price index → section |
| price | 1: /price-list-dubai/ · prices: 71 | no new price URL |
| cost | 2: /apartment-purchase-cost-calculator/, /commercial-real-estate/office-fit-out-cost-tel-aviv/ | total cost → upgrade |
| yield | 2: /investment/real-estate-yield/, /commercial-real-estate/commercial-real-estate-yield/ | yield → upgrade |
| insurance | 2: /mortgage-home-insurance/, /commercial-real-estate/commercial-property-insurance/ | upgrade |
| renovation | 1: /renovation-contractor/ | dropped |
| management · fees | 7 each (incl. /guides/new-project-management-fees/ + 4 language siblings, /property-management/, commercial fees) | upgrade |
| foreign | 3 (two EN posts + /israel-purchase-tax-foreign-residents/) · buyers 2 · abroad 8 | upgrade, no new foreign URL |
| estimator | 3 (he, fr, ru /property-value-estimator/) · value 8 · calculator 14 · tax 11 · property 46 · rent 44 · home 3 | upgrades only |
| hamedina | 5 (he, en, fr, ru, ar project pages) · kikar 1: /tel-aviv-plans/kikar-atarim/ | no tool slug may use them |
| tower 13 · towers 2 · luxury 8 · north 15 · deals 2 · view 2 | owned | not used |

## Appendix D. SERP top 5 (google, Israel; mobile)

Fresh 21.10.2026 16:29-16:30 UTC unless marked 14.10 (catalog serp-top10.tsv).

| Phrase | AI overview | 1-5 |
|---|---|---|
| ארנונה תל אביב | yes (cites only tel-aviv.gov.il) | tel-aviv.gov.il exemption · tel-aviv.gov.il appointments · project-tlv.info · holders.tel-aviv.gov.il · tel-aviv.gov.il online services (municipal-law.co.il "תעריפי ארנונה... 2025" further down) |
| מחשבון ארנונה תל אביב | yes (tel-aviv.gov.il, kolhabait, calculatzia, din, kalkalan) | tel-aviv.gov.il 2026 order PDF · kolhabait.com (calculator) · calculatzia.com (calculator) · tel-aviv.gov.il צו ארנונה · din.co.il forum |
| מחשבון מס רכישה | yes (gov.il, hon) | maor-law · gov.il income-tax simulator · homeway · yuvalim-finance · michale |
| מס רכישה לתושב חוץ | yes (8 law/tax sites + kolzchut + misim) | epsteinlaw · kolzchut (new immigrants) · bshcpa · barlaw · eshimony-law: guides, no calculator |
| עסקאות נדלן | yes (gov.il, nadlan.gov.il, bizportal) | nadlan.gov.il · gov.il · over.org.il · madlan · nadlan.taxes.gov.il |
| מחשבון תשואה | yes (hon, lazyinvestor, adamvainshtein, clalbit) | houseofinance · financialstar · financialplanning · cpa-dray · yeda-kesef (all generic finance) |
| מדד מחירי הדירות | yes | nadlancenter · facebook · diffe-rent · ynet · cbs.gov.il |
| דירות יוקרה בתל אביב | yes | israelsir (3 of 5) · homeland · chabad.info |
| מפת רכבת קלה תל אביב | yes (nta, tevelmetro, dankal, tel-aviv.gov.il) | mako · tel-aviv.gov.il · nta · moovit · tevelmetro |
| כיכר המדינה תל אביב | yes (wikipedia, ashtrom, tel-aviv.gov.il, visit-tlv) | ynet · batim-il · yad2 (project "מעבר לכיכר") · b144 · facebook; nad-lan not in top 5 |
| arnona tel aviv (EN, IL) | yes | jerusalem.muni.il · lod.muni.il · buyitinisrael · jerusalem.muni.il · isrealestate.co.il (no Tel Aviv page in top 5) |
| israel mortgage calculator (EN, IL) | absent | firstisrael · bankhapoalim · israelpropertyhub · semerenkogroup · sellingisrael |
| buy apartment in tel aviv (EN, US) | yes | properstar · yokra-estate · properstar.co.nz · thetelavivi · properstar.ca |
| הערכת שווי דירה (14.10) | catalog | yadata (yad2) · madlan · dirobot · appraiseit · barlev-nadlan |
| מחשבון משכנתא (14.10) | catalog | yeadim-bit · nitzanm · lemon · mercantile · topnetglobal |
| ועד בית (14.10) | catalog | tasalaw · shchenim · info.org.il · ivb · square-management |
| ביטוח דירה (14.10) | catalog | clalbit · harel · bestie · 555 · aig |
| מחשבון שיפוץ (14.10) | catalog | midrag · top-renovations · shiplus · zuznews · arcdb |

Competitor feature check done in this pass: kolhabait.com/arnona/tel-aviv (inputs: area, building type, year built, zone,
optional bill amount, order year 2026/2027) and calculatzia.com/arnona-tel-aviv.html (inputs: order classification, area,
discount %). Everything else in the gap column comes from titles and the 14.10 catalog and must be proven in each
tool's proof.md before release.
