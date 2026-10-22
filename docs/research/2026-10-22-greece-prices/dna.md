# Greece price list: competitor DNA, inventions and the no-cannibalization plan

Prepared 22.10.2026 for nad-lan.co.il (owner order: "the most comprehensive Greece property price list page there is, prove it; research all the competitors; Greek sites too; extract their DNA; infographics, tools, something new; complex but one-tap UX; no cannibalization; a link to jus-tice.co.il").

Read-only research. Nothing was written to any website. The data agent's files (prices.json, prices.md) are not touched by this work.

| What | When (UTC, 22.10.2026) | How |
|---|---|---|
| Keyword volumes (Google Ads, Israel 2376, language "iw", 12 months Oct-2025 to Sep-2026) | 17:49 to 17:50 | DataForSEO search_volume (66 keywords) + keywords_for_keywords (8 seeds) |
| SERPs: 10 Hebrew (Israel) + 2 Greek (Greece) + 2 English (Greece) + 1 English (US), depth 20, AI Overview, PAA | 17:50:40 to 17:52:53 | DataForSEO organic live advanced |
| Competitor pages, raw HTML | 17:54 to 17:56:36 and 18:04:26 to 18:04:38 | python urllib, browser User-Agent; files in `C:\Users\777\nad-lan\_private-research\2026-10-22-greece-prices\pages\` (private, not in the repo) |
| Pages that refuse scripts (GPG, Indomio, Tranio, GREI) | 17:58 to 18:02 | read as text in the built-in browser (no raw HTML saved for these 5) |
| Search Console, both sites, 22.7 to 20.10.2026 | 18:06 to 18:12 | `gsc_api.py query` (read-only) |

Files in this folder: `dna.md` (this), `matrix.csv` (38 features x 28 pages), `keywords.csv` (92 keywords, clustered, with Search Console evidence), `serps.json` (15 SERPs, compact, AI Overview gist and cited domains), `dna-raw/` (full API responses, Search Console CSVs).

Evidence class: everything here is **code** evidence (API data, raw HTML counted by a script, page text read in full). No page was judged from a screenshot. The earlier research of today (`../2026-10-22-greece/serp-dna.md`) is reused, not redone.

---

## 0. Read this first (the 12 findings that decide the page)

1. **The demand is ten times bigger than Google Ads says.** Ads gives every Greece price phrase 10 to 30 a month (about 170 a month for the whole price cluster). Search Console shows the truth: jus-tice.co.il/greece-price-list/ got **22,843 impressions and 92 clicks in 13 weeks** (page level, 22.7 to 20.10.2026), about 1,700 impressions a week, steady, average position 7.9. The top query alone, "כמה עולה דירה ביוון", gave it 2,230 impressions at position 6.9.
2. **Position 7 under an AI Overview earns almost nothing: CTR 0.4%.** Google shows an AI Overview on **15 of 15 SERPs** checked (all 10 Hebrew, all 5 Greek and English). To get clicks the page must either be the AI Overview's source or be in the top 3. Both need dated, sourced numbers, which no Hebrew page has.
3. **The Hebrew AI Overview is stale and undated.** Its stock answer on 4 SERPs is "1,200 to 3,500 euro per m², a typical flat 100 to 250 thousand, Athens 1,800 to 5,000". It cites beta-estate, palmo, thisisgreece, nadlanmaster, green-acres, wise, geoln, greecestate and jus-tice, with no date and no official source. Where Hebrew pages are missing, Google fills the Hebrew AI Overview from English pages (Indomio, GPG, investropa, realting): on "בית ביוון מחיר" it quotes a national €2,769/m² from those English sources. **A Hebrew page with a dated official number becomes the obvious source.**
4. **The field is weak.** A 2021 page (nadlanco) is #3 for the head term "כמה עולה דירה ביוון". A listing page labelled "updated 2024" (nadlanexpert) is #1 on 3 SERPs. Facebook groups hold top-10 slots on 9 of 10 Hebrew SERPs. GREI listing pages hold **15 top-10 slots across the 10 Hebrew SERPs**, only because every card prints "€X, €Y/מ"ר, area".
5. **Every Hebrew price page is a wall of text with one or two tables.** Of the 26 Hebrew pages read, **none has a price map, none has a price tool, none separates asking prices from prices paid, none dates its rows, none has Dataset schema.** Only one Greek-cluster site in Hebrew (nadlan.org.il) has region tabs and calculators, and it has no national price list.
6. **Golden-visa tiers are wrong on every Hebrew price page except nadlan.org.il**: jus-tice says €500K "since 2023" and €250K in the Peloponnese and Zakynthos; gogreece says €250K; palmo says the visa "grants citizenship"; oasis calls it a "golden passport". The law in force for new investments since September 2024 (Law 5100/2024, art. 64, as published by GPG): €800K in Attica, Thessaloniki, Mykonos, Santorini and islands over 3,100 residents; €400K elsewhere; €250K only for conversions and listed-building restorations; 120 m² minimum; short lets banned.
7. **The best price pages in the world are Greek and English, and their DNA is copyable:** BuyGreece (a "source and period" column on every number), GPG (real vs nominal, "next update Nov 2026"), Indomio (monthly national number, September 2026, plus a clickable region map), Greca House (median plus the middle half, a minimum-sample rule, "read this before quoting it"), DKG (13,193 **recorded sale prices** from the official transfer registry vs asking prices), xe.gr (price by flat-size band, 100+ areas, Q3 2025 vs Q3 2026), yourhomesold.gr (price calculator, median vs mean), Spitogatos (demand map, gross yield, new-build column).
8. **Asking and paid prices differ by about a third, and no Hebrew page says so.** Asking: Spitogatos national about €2,561/m² (Q3 2026, as quoted by BuyGreece), Indomio €2,790/m² (September 2026). Paid: DKG's registry analysis gives Athens €1,838 and Thessaloniki €1,509/m² (January to May 2026); the English AI Overview quotes a national recorded median near €1,479/m². This gap is the single most useful fact for an Israeli buyer, and it is a trust moat.
9. **The owner's other site already owns this SERP.** jus-tice.co.il/greece-price-list/ (H1 "מחירי דירות ביוון 2026: כמה עולה דירה ביוון לפי אזור") is #5 and #6 in today's snapshot and position 6.8 to 7.7 in Search Console for every head term. The nad-lan page must take a different angle (data instrument vs legal narrative) and link to jus-tice only where the intents differ (section 7.4).
10. **nad-lan already has two pages Google uses for Greece prices:** the hub /global/greece/ is #3 for "מחיר למטר ביוון" and #4 for "מחירי נדל"ן ביוון", and the AI Overview cites it on both. The new page must take that intent over by internal links and anchors, not by deleting anything in the hub (section 7.2).
11. **A price-list precedent exists on nad-lan:** /price-list-dubai/ (H1 "מחירי דירות דובאי 2026", 33 tables). Its first word "price" is taken, and city pages start "מחירי דירות ב...", so the Greece page needs a different slug word and a different title start (section 7.1).
12. **The data agent already holds the granularity to price 100+ places** (Spitogatos Q3 2026 by region and Attica/Thessaloniki areas, Q2 2026 for 40+ islands, 40 holiday towns, xe.gr Q3 2026). Nobody in Hebrew prices more than about 25. Breadth with dates is the proof Ben asked for.

---

## 1. Keywords and clusters

92 keywords in `keywords.csv`. Ads volumes are Google's rounded buckets; the Search Console columns (jus-tice price list, 13 weeks) show real demand.

### 1.1 The price cluster (the new page owns it)

| Keyword | Ads vol/mo | 12-mo trend (Oct-25 to Sep-26) | jus-tice GSC impressions (13 wk) | jus-tice avg pos |
|---|---|---|---|---|
| כמה עולה דירה ביוון | 30 | 30,30,30,20,30,40,30,40,50,30,30,30 (up, peak Jun-26) | 2,230 | 6.9 |
| מחירי דירות ביוון / מחיר דירה ביוון (one Ads group) | 30 | 40,20,10,30,30,20,20,30,40,30,30,20 (flat) | 1,189 + 938 | 6.8 / 6.7 |
| מחיר דירות ביוון | (in the group) | | 915 | 4.6 |
| דירה ביוון מחיר / דירות ביוון מחירים | 20 | down | 949 | 7.2 |
| בית ביוון מחיר | 30 | up (20 to 40-50 in summer 2026) | 598 | 7.7 |
| כמה עולה בית ביוון | 30 | up (10-20 to 40) | 573 | 6.8 |
| מחיר בית ביוון | n/a | | 157 | 7.5 |
| דירות ביוון / בית ביוון / בתים ביוון (broad, price page ranks for them) | (hub terms) | | 404 / 394 / 74 | 17.2 / 10.9 / 12.1 |
| מחירי נדל"ן ביוון / מחירי נדלן ביוון | 10 | flat | small | |
| מחירי בתים ביוון | 10 | down | | |
| greece property prices / greece house prices / greece real estate prices | 10 each | flat | | |
| מחירון דירות ביוון, מחיר למטר ביוון, מחיר למ"ר ביוון, מחירי דירות ביוון 2026 | no Ads volume | | | AIO and organic still appear (see section 2) |

**Region and island price phrases have no Ads volume** (מחירי דירות בסלוניקי / בכרתים / ברודוס / בקורפו / בחלקידיקי / במיקונוס / בזקינתוס / בלפקדה / בפלופונס, כמה עולה דירה ב...). The only one with volume is "כמה עולה בית בכרתים" (10). In Search Console the jus-tice page still collects them: קניית דירה בכרתים 156, נדל"ן בכרתים 46, דירות נופש ביוון למכירה 130 (position 3.4), בתים לשיפוץ בכרתים 8. These are **rows on the price list**, not pages.

### 1.2 Intents that belong to other pages (do not take them)

| Intent | Example (evidence) | Owner page | What the price list does |
|---|---|---|---|
| Athens prices | מחירי דירות באתונה 20/mo, כמה עולה דירה באתונה 20, דירה באתונה מחיר 10; jus-tice gets מחיר דירות באתונה 408 impressions | /athens-apartments/ (H1 "דירה באתונה: אזור אחרי אזור, מחיר למ״ר...") | one Athens summary row (and Piraeus) with a link "מחירי אתונה לפי אזור"; no Athens neighbourhood table |
| Buying costs | כמה עולה לקנות בית ביוון 10/mo (168 impressions at jus-tice) | /acquisition-greece/ (its cost calculator) | the budget tool applies one "about 10% buying costs" line and links to the calculator; no fee table |
| Tax | ENFIA, rental tax, treaty | /taxation-greece-israel/ | one line per tool where tax changes the answer, with a link |
| Investing in Greece (broad) | נדל"ן ביוון 210, השקעה ביוון 70 | /global/greece/ (hub) | breadcrumb parent, one link back |
| Short lets | airbnb יוון | /short-term-rentals-abroad/short-term-rentals-greece/ | the short-let layer on the map links there |
| Listings | בתים למכירה ביוון 140, דירות למכירה ביוון 90 | hub / future seaside page | none |
| Other countries | **כמה עולה דירה בקפריסין 70/mo (more than any Greece price phrase)**, מחירי דירות בקפריסין 50, מחירי דירות בפורטוגל 40 | none on nad-lan yet (jus-tice has /cyprus-prices/) | not here. Finding: a Cyprus price list is the next page of this kind (owner decision) |

### 1.3 Vocabulary the searchers use (for headings and copy)

- Question form leads: "כמה עולה דירה/בית ביוון", "מה מחירו של דירה באתונה" (PAA).
- "מחיר" and "מחירי" more than "מחירון"; "מחירון" is the word competitors use in H1s (thisisgreece, palmo's table heading, nadlanmaster) and in titles "(ראו מחירון)".
- "למ"ר" / "למטר" / "מטר רבוע" all appear; AI Overviews write "למ"ר" and "למטר רבוע".
- Islands and sea: "ליד הים", "על הים", "בית נופש", "בתים לשיפוץ", "בתים כפריים", "יד 2" (related searches).
- Investor words: "תשואה", "להשקעה", "האם כדאי".

---

## 2. SERPs (Google Israel, Hebrew, desktop; plus Greece and the US)

Full lists in `serps.json`. Retrieved 17:50:40 to 17:52:53 UTC.

### 2.1 Top 10 of the main Hebrew price SERPs

| # | כמה עולה דירה ביוון | מחירי דירות ביוון | כמה עולה בית ביוון | בית ביוון מחיר | דירה ביוון מחיר | מחירון דירות ביוון | מחירי נדל"ן ביוון | מחיר למטר ביוון |
|---|---|---|---|---|---|---|---|---|
| 1 | nadlanexpert /city/athens/ | nadlan-greece projects | nadlanistka | he.airbnb (monthly stays) | **gogreece /property-prices-greece/** | **palmo /greece-prices/** | grei /listings/greece | nadlanexpert /city/athens/ |
| 2 | Facebook group | grei Athens listings | nadlanexpert | oasisnadlan | palmo /greece-prices/ | beta /greece-property-prices-and-returns/ | green-acres Athens | thisisgreece /athens-real-estate/ |
| 3 | nadlanco (2021) | Facebook group | nadlanmaster Athens | green-acres Athens | beta prices-returns | thisisgreece /property-prices/ | geoln | **nad-lan /global/greece/** |
| 4 | greece-properties.eu | greece-israel | green-acres Athens | nadlanco (2021) | green-acres /he | green-acres /he | **nad-lan /global/greece/** | home-li listings |
| 5 | grei Athens | nadlanexpert | greece-islands | thisisgreece home | Facebook group | **jus-tice /greece-price-list/** | il.investing (stocks) | grei Athens |
| 6 | grei investor guide | grei news | grei Athens | greece-israel | **jus-tice /greece-price-list/** | Facebook group | oasisnadlan | grei home |
| 7 | grei home | grei news | Facebook post | nadlanexpert cost of living | nadlanistka guide | nadlanmaster Greece | grei home | nadlanco (2021) |
| 8 | gogreece buy-apartment | he.airbnb | greece-realestate | grei home | greecestate | beta Athens prices | nadlan-greece | Facebook post |
| 9 | greecestate | homegreece compare | nadlanco (2021) | grei Athens | thisisgreece /property-prices/ | wise | grei Athens | jus-tice /investing-in-greece-real-estate/ |
| 10 | realestate-greece | greece-realestate | new-greece Athens | Facebook post | nadlanmaster Greece | greecerealestate | greece-realestate | greece-realestate |

Also pulled: "מחירי דירות בכרתים" (greece-islands, realestate-greece Crete, metzger-cy, Facebook, nadlan.org.il Crete) and "מחירי דירות בסלוניקי" (nadlanexpert, nadlan-greece project, a Greek agency in Hebrew, Facebook, greece-israel).

**Snapshot vs Search Console:** in this single snapshot jus-tice's price list is in the top 10 on only 2 of 10 Hebrew SERPs, while Search Console gives it a steady 6.8 to 7.7 average on all the head terms for 13 weeks. One live sample from one location moves a lot on these low-volume SERPs; Search Console is the bible here.

**Domain frequency across the 10 Hebrew SERPs (top-10 slots / top-20 appearances / AI Overview citations):** grei 15/29/4, Facebook 9/10/0, green-acres 6/17/5, nadlanexpert 6/8/1, greece-realestate 4/9/1, nadlanco 4/6/1, thisisgreece 4/5/6, beta-estate 3/7/6, nadlanmaster 3/5/6, jus-tice 3/3/6, palmo 2/4/5, wise 2/3/5, nad-lan 2/2/2, gogreece 2/2/1.

### 2.2 AI Overview (present on 10 of 10 Hebrew SERPs)

| SERP | Gist | Cited domains |
|---|---|---|
| כמה עולה דירה ביוון, מחירי דירות ביוון, כמה עולה בית ביוון, דירה ביוון מחיר (same text) | €1,200 to 3,500/m²; a typical flat €100 to 250K; Athens 1,800 to 5,000 (centre or new 3,800 to 7,000); Thessaloniki 1,400 to 3,500; Crete 1,500 to 2,500, villas from €450K; Mykonos/Santorini/Corfu houses €400 to 900K+; costs 8 to 12%. No date, no official source. | beta-estate, geoln, jus-tice, palmo, thisisgreece, wise, greecestate, green-acres, nadlanmaster |
| בית ביוון מחיר | "national average for 2026 about €2,769/m²"; Athens centre 2,400 to 4,000; south and north suburbs 3,500 to 4,200 | **English sources:** indomio, globalpropertyguide, investropa, realting, vonpollgreece, istasyaproperty, plus beta, nadlanexpert |
| מחירון דירות ביוון | Athens 1,800 to 5,000 (Vouliagmeni over 7,700); Thessaloniki 1,500 to 3,500; Mykonos ~6,750 and Santorini ~4,190 (these are jus-tice's figures); VAT 24% | beta, jus-tice, palmo, thisisgreece, wise, nadlanmaster |
| מחירי נדל"ן ביוון | Attica 1,800 to 4,500, Athens average ~2,978; Thessaloniki 1,200 to 2,500 | **nad-lan.co.il**, oasisnadlan, athens.co.il, green-acres, grei, realestate-greece |
| מחיר למטר ביוון | "1,200 to 2,500 euro per m² in most of the country"; Kolonaki 8,000 to 12,000 | jus-tice (/investing-in-greece-real-estate/), greece-realestate, home-li, thisisgreece, **nad-lan /global/greece/**, grei, nadlanco |
| מחירי דירות בכרתים | Heraklion ~€1,999, Apokoronas 1,800 to 2,500, Chania ~2,997 | grece-crete, greecerealestate, metzger-cy, greecestate, grei, nadlan.org.il, realestate-greece |
| מחירי דירות בסלוניקי | 2,384 to 3,090/m²; resale ~2,425, new ~3,060 | gogreece, greecement, greecerealestate, nadlan-greece, grei, **indomio**, nadlan.org.il, nadlanmaster, progreecegroup |

### 2.3 People also ask and related searches (Hebrew)

PAA appeared on only 3 Hebrew SERPs: "מה מחירו של דירה באתונה?", "כמה עולה לחיות ביוון?", "איפה אפשר לקנות דירה ביוון כדי להשקיע?", "איפה אפשר למצוא בית נופש ביוון למכירה?", "איפה אפשר למצוא בית ליד הים ביוון?", "איפה אפשר למצוא בתים להשכרה ביוון?", "איפה אפשר למצוא וילה ביוון לנופש?", "האם יש בית למכירה ביוון?", "מהי שכונת גיזי באתונה?", "איפה אפשר למצוא בתי מלון למכירה ביוון?". No answer sources were returned for them.

Related searches: בתים למכירה ביוון ליד הים, בתים לשיפוץ ביוון, דירות למכירה ביוון יד 2, דירות למכירה ביוון סלוניקי, בתים כפריים ביוון, האם כדאי לקנות דירה ביוון, נדלן בחאניה כרתים, וילות למכירה ביוון על הים, בית ביוון על הים, פודקאסט נדלן ביוון, קניית בית נופש ביוון, פרויקטים להשקעה ביוון.

### 2.4 Greece and English SERPs

| SERP | Top 3 | AI Overview | PAA / related |
|---|---|---|---|
| τιμές ακινήτων (Greece, Greek) | Spitogatos SPI, xe.gr price page, Indomio Athens centre | national sale €2,790/m² (+4.73%), rent €10.68 (+3.79%), **September 2026**; Attica €3,218; Kolonaki €5,516; Patisia €1,777 (Indomio) | πρόβλεψη 2026, 2027, φούσκα, ανά περιοχή |
| τιμή ανά τετραγωνικό (Greece, Greek) | Indomio Thessaloniki, Spitogatos SPI, xe.gr; #5 the official **maps.gsis.gr valuemaps** (objective values) | Attica south €4,231; Athens centre €3,420 (Plateia Vathis €2,041 to Syntagma €6,067) | ανά περιοχή Αθήνα / Θεσσαλονίκη, για χτίσιμο, ενοικίου |
| greece property prices 2026 (Greece, English) | GPG, Indomio EN, TradingEconomics | BoG +5.5 to 5.7% y/y in H1 2026, above the 2008 peak; **recorded median ~€1,479/m², 68 m² ≈ €95K**; asking higher | "Are property prices falling in Greece?", "Which Greek island is the cheapest to buy property?", "What are the current real estate prices in Greece?" |
| athens price per square meter (Greece, English) | Spitogatos listings, xe listings, pmrealestate 2024 | €2,500 to 3,500 typical; "size pricing paradox": flats under 80 m² cost more per m² | "Athens price per square meter calculator" |
| greece property prices (US, English) | listing sites, Properstar | national asking €2,561/m², "+94% since 2017" | "cheap houses in Greece under 100k by the sea" |

The Greek and English SERPs reward **dated data portals and tools** (index, map, calculator, valuation), not articles. That is the format gap in Hebrew.

---

## 3. Competitors read in full: 47 pages (26 Hebrew, 21 Greek/English) + 3 of ours

Counts are from the raw HTML by script (words in the main content, tables, schema, dates). The main Hebrew price pages (jus-tice, gogreece, palmo, beta-estate, oasisnadlan) and GPG and Indomio were read word by word; the other pages were read through their outline, every table and the passages that carry numbers. Full per-page metrics: `_private-research\...\pages\_analysis.json`. Feature matrix: `matrix.csv`.

**Could not be read (blocked, not bypassed):** spitogatos.gr/deiktis-timon (bot wall; the English index page was read instead), properstar.com (Azure WAF), ellika.gr (Cloudflare challenge), bmnow.co.il (DNS failure), indomio Athens-centre page (403; the national page was read in the browser). Reused from this morning's research and not re-read: nadlanmaster Greece/Athens/Crete guides, beta-estate Athens prices, yad2 blog, new-greece Athens.

### 3.1 jus-tice.co.il/greece-price-list/ (the owner's other site; the one to beat and to complement)

- Title "מחירי דירות ביוון 2026: כמה עולה דירה? מ-1,500 אירו למ"ר". H1 "מחירי דירות ביוון 2026: כמה עולה דירה ביוון לפי אזור". Meta: Thessaloniki and Crete from €1,500/m², a 3-room flat in central Athens €140 to 280K.
- Breadcrumb schema with 11 items from two trails mixed (ראשי > Articles > מקרקעין | נדל"ן > ... > עורך דין בחו״ל > עורך דין ביוון > ...). Article schema, author "Jus-Tice.co.il" (no person). Published 6.7.2025, modified 25.7.2026, "57 דקות קריאה".
- **12,631 words**, 637 numbers, **1 table** (16 rows: area, €/m², an 80 m² flat, who it suits), 4 images, no chart, no map, no tool, no FAQ, no FAQ schema.
- Structure: answer paragraph (1,200 to 2,500/m², 80 m² = €100 to 200K) → table → an "AI judge" courtroom-simulation widget → one long H2 per region: Athens, Thessaloniki, Crete, Rhodes, Lefkada, Corfu, Cyclades (Mykonos, Santorini, Paros, Naxos, Milos, Serifos, Andros), Peloponnese (Corinthia, Argolida with Nafplio and Porto Heli, Messinia with Kalamata, Mani/Laconia), Halkidiki (Kassandra, Sithonia), Agrinio/Patras/Zakynthos → short vs long let ROI → buying process for foreigners → lawyer CTA, a 23-country lawyer list, related guides.
- Each region has the same 11-parameter grid: price per m², yield, value trend, tourism, regulation, tax, infrastructure, demand and supply, foreign ownership rules, distance to services, maintenance. Greek names in brackets (Αθήνα, Κρήτη...). Prices also in ₪ (at a fixed, undated 4.0 rate).
- **Strengths:** the broadest Hebrew coverage (about 25 places); the AI Overview reuses its Mykonos €6,750 and Santorini €4,190; steady position 7 to 8 on every head term for 13 weeks; the investing page beside it is cited by the AI Overview for "מחיר למטר ביוון".
- **Wrong or stale (findings for the owner; fixing jus-tice needs his word and the justice-page-dna skill):**
  - golden visa: "€500,000, and €800,000 in parts of Athens, since 2023"; Rhodes €500K "like Athens"; Peloponnese and Zakynthos still €250K; Paros €400K. All wrong for investments since September 2024.
  - VAT 24% on new builds without the suspension to 31.12.2026; ENFIA "0.1 to 0.5% of value"; rental tax "15% to €12K, then 35%, 45%" (the 2026 scale is 15/25/35/45); "an Israeli investor will not pay double tax in Israel" (oversimplified: the Israeli side still applies); the financing section repeats "golden visa €500K central, €250K periphery".
  - Useful detail it does have: a 20-profession list with costs, a notary scale (about 1% to €120K, 0.7% above, plus VAT), the transfer tax paid before signing on the higher of price and objective value, and a link from the price page to its own /greece-lawyers/ page for the legal side (the same page this plan links to).
  - figures with no date or source on almost every row ("in the past year +9.3%"); the only sources named are the Bank of Greece (once) and GREI.
  - Lefkada €3,500 to 6,500/m² (Spitogatos Q2 2026: €3,302); Mykonos €6,750 (Spitogatos Q2 2026: €7,059).
  - an AI courtroom widget in the middle of a price page; a 57-minute read for a numbers question; CTR 0.4%.

### 3.2 The other Hebrew price pages, ranked by how much they matter

| Page | Where it ranks | DNA in one paragraph | Wrong / stale |
|---|---|---|---|
| **gogreece.co.il/property-prices-greece/** | #1 "דירה ביוון מחיר" | Title "מחירי דירות ביוון 2026 כמה עולה דירה ביוון באמת?", H1 "מחירי דירות ביוון". 2,120 words. The winning element is one table: **12 submarkets, "2026 vs 2025 €/m², % change"** (Athens centre/north/south/west/east, Piraeus, Piraeus suburbs, rest of Attica, Thessaloniki city/suburbs/rest, Argolida), the Spitogatos submarket structure. A Europe table (England, Paris, Tel Aviv, Spain, Greece). Short city blurbs (Corfu, Crete, Thessaloniki, Santorini). FAQ 4 with FAQPage schema. 4 forms, 4 WhatsApp links, no author, no breadcrumb. | body written 2021-2022 ("post-COVID", "prices peaked in 2022"); "7% flat rental tax"; golden visa €250K; Tel Aviv €5,701/m²; the table has no source |
| **palmo-group.com/greece-prices/** | #1 "מחירון דירות ביוון", #2 "דירה ביוון מחיר" | H1 "מחירי דירות ביוון - אז כמה עולה דירה ביוון?". 2,907 words. A 12-row table: Athens general/centre/north/south/west and **by flat size (studio to 5 rooms)**, Thessaloniki, Piraeus; a 6-city Europe table (London, Lisbon, Berlin, Tel Aviv €17,000, Paris); new vs resale premium 30 to 50%; 6 FAQ visible (no schema); disclaimer; podcast. Published 29.12.2024, modified 16.6.2026. | data "as of 2024"; Athens centre €3,800 to 7,000 (inflated); ">80% of deals by foreigners"; golden visa "grants citizenship"; no source |
| **beta-estate.com/greece-property-prices-and-returns/** | #2 "מחירון", #3 "דירה ביוון מחיר" | H1 "מחירי דירות ותשואות על דירה ביוון 2026". 2,728 words. **Key takeaways sourced to the Bank of Greece** (2025 +6.8%; new +8.0% vs old +6.0%; Athens +5.5%, Thessaloniki +10%, periphery +8%), forecast 3.2% a year to 2029 (Knight Frank, JLL), a 5-tier price table (70 m² flat), a yield table (gross and net), long vs short let table, BoG index image, a named co-founder, ~10 FAQ headings (no schema). Modified 26.1.2026. | rental tax "7 to 15%"; Airbnb limits "being considered" (the Athens freeze is in force); only 5 tiers |
| **thisisgreece.co.il/property-prices/** | #3 "מחירון", #5 "בית ביוון מחיר" | H1 "מחירון דירות ביוון". 1,845 words. Two 8-row tables: Greece / Athens / Thessaloniki / Piraeus / Lefkada / Crete with €/m², a studio-2-room price, a 3-room price and **rent next to price**. Source link to the Bank of Greece. | modified 13.3.2025 (19 months old); Lefkada €3,500 to 6,500 (copied by jus-tice) |
| **oasisnadlan.com/כמה-עולה-דירה-ביוון/** | #2 "בית ביוון מחיר" | H1 = the question + "מדריך מחירים, שכונות ותשואות למשקיעים ב־2025". 2,439 words. 5-row table (€/m² and a 70-100 m² flat), Athens neighbourhood groups, **a worked buying-cost example (€150K → €163,750)**, **Israel comparison in ₪ per m²** (Tel Aviv 35 to 45 thousand vs Athens under 15 thousand), author first name. | 2025, not updated since 2.10.2025; VAT 24% generic; Petralona called "periphery"; "golden passport" |
| **nadlanexpert.co.il/city/athens/** | #1 on 3 SERPs | A listing page (38 cards) with title "[לוח מעודכן 2024]", H1 "City: אתונה". No price table. Ranks on brand and exact title words. | label "2024"; 37 of 38 images without alt |
| **grei.co.il (listings + newsfeed)** | 15 top-10 slots | 4,808 Greek listings in Hebrew; **every card heading is "€price, €/m², type · area"**, which Google and the AI Overview quote; filters (type, price, rooms), gallery/map toggle, region counts, an FAQ; short news items (~150 words) on price moves. | the FAQ says Israelis "pay tax once, in Greece, maybe with a full exemption in Israel" |
| **green-acres.gr/he** | AIO-cited 5, #2-4 on several | Listing portal in Hebrew; each search shows **average €/m², median €/m², median size, price range** computed from its own listings (Athens: 483 listings, average €4,284/m²). Mapbox map. | listing averages of one agency network, not the market |
| **nadlan.org.il/country/greece (+ /crete, /thessaloniki)** | AIO-cited; #5 "מחירי דירות בכרתים" | The most modern Hebrew competitor: "מעודכן לנתוני 2026", **area tabs ("מפת האזורים, בחרו אזור")**, **net-yield and mortgage calculators** (number inputs), Airbnb occupancy by town, golden-visa tiers right (800/400), Thessaloniki short-let freeze, BoG/Indomio/GPG named. 1,240 to 1,450 words each. No national price list, no dates in schema, no author. | "0% מס שבח (עד סוף 2026)" is right; few places per page |
| nadlanmaster.co.il/מחירי-דירות-באתונה/ | #19 Crete, AIO-cited Thessaloniki | 501 words, 2 tables (flat types, 5 zones with rent). Title ends "(ראו מחירון)". | Athens centre €1,700 to 2,000 (below every asking index) |
| homegreece.co.il compare | #9 "מחירי דירות ביוון" | "השוואת מחירי נדל"ן בערי יוון המרכזיות: מפת ההשקעות המשתלמת ביותר": a 5-city table (€/m², yield), lead-form selects. Two H1s. | 2024 |
| greece-realestate.co.il/מחירי-דירות-ביוון/ | #10 several, AIO-cited | 1,377 words, no table. | 2022-2024 |
| nadlanco.co.il 2021 page | **#3 "כמה עולה דירה ביוון"** | 5-city table "early 2021", Tranio as source. | 5 years old; proves how weak the field is |
| wise.com/il/blog/real-estate-in-greece | #9 "מחירון" | 2,281 words, average by city (Spitogatos, TE), mortgage, building data; money-transfer CTA. | 27.12.2023 |
| globes.co.il (2023 article) | #15 "מחירון" | News: "prices jump, yields fall". | December 2023 |
| new-greece average-cost (2018), nadlanistka (2023), nadlanexpert Thessaloniki, thisisgreece Athens, home-li (JS shell), jus-tice /greece-lawyers/ (read for the link plan) | various | thin or old | |

### 3.3 The best non-Hebrew price pages (what to copy and beat)

| Page | DNA worth copying |
|---|---|
| **Global Property Guide, Greece price history** (read in browser) | KPI tiles (house prices y/y +5.63% Q1 2026, real +1.66%, Athens €2,500/m², mortgage 3.23%); **interactive chart with nominal/real and 1Y/5Y/10Y/All**; 11-submarket sale and rent tables (Spitogatos Q1 2026, € and USD, y/y); BoG regional split (Thessaloniki +6.4%, other cities +5.4%, Athens +5.2%); new vs old (+6.0% vs +5.5%); a 20-year nominal/real table; foreign inflows; golden-visa law and counts; permits by region; **"LAST UPDATE Jul 2026 · NEXT UPDATE Nov 2026"**; named author. |
| **Indomio.gr market page** (read in browser) | One national number per month (**€2,790/m² sale, €10.68 rent, September 2026**, y/y) with the range from the cheapest to the dearest region; a map of 13 regions with sale/rent and y/y; drill-down to prefecture, municipality, neighbourhood; trend charts. Google's Greek AI Overview quotes it verbatim. |
| **Spitogatos price index (EN)** | Quarter vs previous quarter table per area with a **new-build column**; sale/rent toggle; **demand map** (Leaflet); gross rental yield; Datawrapper charts; FAQ schema; a journalist sign-up. |
| **xe.gr price page** | 100+ areas, each a small table: listings available, **€/m² by size band (up to 80 m², 81-120, 121+)**, Q3 2025 vs Q3 2026, change; sale and rent; 11,169 words of tables. |
| **BuyGreece statistics 2026** | A 14-row "Statistic / Figure / **Source and period**" table; a 22-area asking-price table (Antiparos €7,600, Vouliagmeni €7,364, Mykonos €7,059...); BoG segments; a yield table with a "basis" column; golden-visa numbers from the ministry; FAQ 10 with schema; **Dataset schema**; modified 16.10.2026. The model for being quoted by AI. |
| **Greca House, Athens asking prices by neighbourhood** | Median €/m² and the **middle half (25th-75th percentile)** for 14 neighbourhoods, listing counts, "a neighbourhood is shown only with at least six flats of 20 m² or more", "These are asking prices on our own listings, not prices paid", "Read this before quoting it", Dataset schema, snapshot date. |
| **DKG Development, 13,000 sales** | 13,193 recorded transfers (January to May 2026) from the official **Property Transfer Values Registry**: median paid €/m², **59% of flats sold above the objective (tax) value**, new builds +69% over 1980s-90s flats, Athens €1,838 vs Thessaloniki €1,509/m² paid, Athens municipalities (Agia Varvara €971). Author with a PhD, method section. |
| **yourhomesold.gr** | "Τιμές Ακινήτων Οκτώβριος 2026" (the month in the title), an Attica **price calculator** (choose sub-region, area, m²), cheapest/dearest/mean per sub-region, median vs mean explained, method in steps, 14 FAQ with schema, Dataset/Table schema, 11 charts. |
| Engel & Völkers, property prices Greece | 15-region table, listings; Athens €4,500 to 8,000 (luxury skew). |
| Numbeo | Price-to-income 12.13, mortgage as % of income, rent by flat type, a city-vs-city compare tool. |
| Investropa, Greek islands | 12 island areas with a market label, typical price, €/m² and $/sq ft; an extra-costs table; **"what you can buy with each budget"**; a sources table with "how we used it". |
| TradingEconomics | BoG index 114.2 in Q2 2026 (record high, low 58.9 in Q3 2017), Dataset schema, forecast. |
| maps.gsis.gr valuemaps; thehomli zone price; ektimiseto | The official objective-value map, a zone-price calculator, a free AI valuation. These are the Greek "tools" format; none exists in Hebrew. |
| beta-globe (EN twin of beta-estate), euro2day map article (2024), ecopress tables (2019), Tranio Athens (listings, "golden visa from €250,000" banner), cityvalue (listing map) | secondary |

### 3.4 Our own pages read for the overlap check

- /athens-apartments/: H1 "דירה באתונה: אזור אחרי אזור, מחיר למ״ר ומה בודקים לפני שקונים", SEO title "אתונה: דירות למכירה ב־2026, מחיר למ״ר לפי אזור", 3,587 words, 8 tables, 2 calculators (buying cost, net yield), BoG index chart, "סולם המחירים של אתונה", "אתונה, סלוניקי, כרתים או חלקידיקי", 12 FAQ with schema. **It already holds an Athens price ladder and a 4-place comparison**; the price list must not repeat the Athens neighbourhood ladder and should link to this page for it.
- /global/greece/ (hub): 832 words, ranks #3/#4 for price-per-m² phrases and is AIO-cited for them.
- /price-list-dubai/: H1 "מחירי דירות דובאי 2026", 8,720 words, 33 tables, no tools. The house precedent for a country price list.

---

## 4. The matrix in one paragraph (details in matrix.csv)

Across 38 features and 28 pages: only the Greek and English data portals have a map, a tool, a dated period per number, real-vs-nominal, asking-vs-paid, Dataset schema and an update cadence. In Hebrew, the average price page has one to four tables, about 2,000 words, no date per figure, no named source per figure, no chart, no map, no tool, and a wrong golden-visa line. nad-lan's Athens page is already ahead of all Hebrew competitors on tools and freshness; the price list should be ahead of the Greek portals on the Israeli lens (₪, Israeli city comparison, flight, tax pointer) and equal to them on data discipline.

---

## 5. DNA synthesis: what the winning Hebrew Greece price page must contain

### 5.1 Must-haves (parity with the best, without which the page does not compete)

1. **An answer in the first 3 lines:** one national asking €/m² with its quarter and source, one paid €/m² with its period, the price of an 80 m² flat at the cheapest and the dearest place, and the y/y change. This is the AI Overview's sentence.
2. **A sortable table of 100+ places** (13 regions, 40+ islands, holiday towns near Athens, Peloponnese and Halkidiki, the big cities as summary rows): €/m² asking, y/y, rent €/m², gross yield where computable, an 80 m² price, golden-visa tier, a short-let flag, and a small per-row stamp "Spitogatos, רבעון 3 2026". Owner research law: no citation clutter on the page; the stamp is a label, the full source list stays in the repo and one short "על הנתונים" block.
3. **Asking vs paid, said plainly**, with the registry/BoG numbers next to the portal numbers.
4. **Real vs nominal** for the 10-year trend (BoG index, ELSTAT CPI), like GPG.
5. **Freshness signals that are true:** "נכון לרבעון 3 2026", the retrieval date, and "העדכון הבא: ינואר 2027". No fake freshness (gogreece's 2026 title on 2021 text is the anti-pattern).
6. **Golden-visa and short-let facts correct per row** (800/400/250-conversion; Athens districts 1-3 freeze; Thessaloniki centre added).
7. **Schema:** BreadcrumbList, FAQPage (10 to 14 questions), Dataset (name, temporalCoverage, spatialCoverage Greece, variableMeasured €/m², creator, isBasedOn the sources), Article with a named analyst. Exactly one H1.
8. **Owner laws on layout:** H1 → answer paragraph → CTAs → the stage (map) → facts → article, on every width, phones first (`tools/content_first_check.py`); the site's wide "ייעוץ חינם" WhatsApp bar; no scroll capture by the map (`tools/scroll_check.py`).

### 5.2 Vocabulary and patterns

- Use: "כמה עולה דירה ביוון", "מחיר למ״ר", "מחירון", "לפי אזור ואי", "דירת 80 מ״ר", "מחיר מבוקש" (asking) vs "מחיר בעסקאות בפועל" (paid), "תשואה ברוטו", "ליד הים", "בית נופש", "יד שנייה" vs "חדש מקבלן", Greek names in brackets on first mention (Χανιά), the island groups by name (הקיקלאדים, האיים היוניים, הדודקאנס, הספורדים, צפון הים האגאי).
- Avoid: "גולדן פספורט", "אזרחות דרך השקעה", "פטור ממס בישראל", "אטלס" (banned word on nad-lan), slogan copy, tech/demo talk (language-dna skill).
- Title pattern that wins here: the exact question or the price word first, then 2026, then the scope ("לפי אזור", "בכל אזור ואי"). Brand last.

---

## 6. Ten inventions nobody has (ranked by value x buildability; all plain JS + inline SVG, no libraries, data from prices.json)

| # | Invention | What the user does (one tap) | What it shows | Data it needs | Value / build (1-5) |
|---|---|---|---|---|---|
| 1 | **Greece price-heat map with one-tap region cards** | taps a region or island group on an SVG map of Greece (13 regions; island groups as tappable clusters) | the region fills by €/m² (sequential ramp, legend in €); a card slides up: asking €/m², y/y arrow, rent €/m², gross yield, 80 m² price, golden-visa tier, short-let flag, "→ האזור המלא" link (Athens → /athens-apartments/) | region polygons simplified to ~30 KB (Natural Earth admin-1, public domain; or Eurostat GISCO NUTS-2, free with attribution), prices.json per region | 5 / 4 |
| 2 | **"What does €X buy" budget slider** | drags one slider (€100K to €800K) or taps a preset | for 30+ places: m² you get after ~10% buying costs, as horizontal bars sorted by size; a line where 80 m² falls; a link to the acquisition calculator for the exact costs | €/m² per place, one cost factor | 5 / 5 |
| 3 | **"My Israeli flat in Greece" translator** | picks an Israeli city and room count | the flat's median value from nad-lan's own city price pages in ₪ → € at the Bank of Israel rate of the day → how many m² it buys in 30 Greek places ("your 4-room in Petah Tikva = 210 m² in Chania") | nad-lan's own Israeli medians (moat: no Greek site and no Hebrew competitor can link the two datasets) | 5 / 4 |
| 4 | **Island ladder** | scrolls one vertical ladder; taps a sea chip (Cyclades, Ionian, Dodecanese, Sporades, North Aegean, Crete) | 40+ islands from Antiparos €7,600 to Samos €1,059 (Spitogatos Q2 2026, as collected), each rung a tap target opening the same card as the map | island rows (already collected by the data agent) | 4 / 5 |
| 5 | **Asking vs paid gap meter** | taps a region | two bars: what sellers ask (portal) and what buyers paid (registry/BoG), the gap in %, one honest sentence ("המחיר במודעה גבוה בכ־X% ממה שנרשם בעסקאות") | asking per region + DKG/registry paid medians where they exist; otherwise the meter is hidden for that row (honesty law) | 4 / 4 |
| 6 | **Compare 3 places side by side** | taps up to 3 chips | a 3-column card: €/m², y/y, rent, yield, 80 m² price, golden-visa tier, short-let rule, direct flight time from Tel Aviv | per-place fields + a flight-time field | 4 / 5 |
| 7 | **Golden-visa lens** | toggles "גולדן ויזה" | each row gets its tier badge (800K / 400K / 250K conversion) and a computed line: **is the € threshold or the 120 m² minimum the binding rule here?** (120 m² x local €/m² vs the tier) | tier per place (law 5100/2024) + €/m² | 4 / 5 |
| 8 | **Short-let legality layer** | toggles "השכרה קצרה" on the map | hatching where new short-let registrations are frozen (Athens districts 1-3, central Thessaloniki) and a note that golden-visa property may not be short-let; link to the STR page | a list of frozen zones (official decisions) | 4 / 4 |
| 9 | **Price vs yield scatter** | taps a dot | each region/island as a dot (x = €/m², y = gross yield), quadrants "יקר ומניב / זול ומניב..."; the tapped dot opens the card | €/m² + rent €/m² per place | 3 / 4 |
| 10 | **Greece vs Israel, 10-year race** | taps "בשקלים / ביורו" | a slope or race chart: BoG dwelling index (Athens, Thessaloniki, rest) against the Israeli CBS dwelling index, rebased to 2016 = 100, in € and in ₪ | BoG index series + CBS series + yearly EUR/ILS | 3 / 4 |

Rules for all ten: one tap, no hover-only information, every number keeps its stamp (source + quarter), no tool shows a number the data does not have (unknown = omitted), mobile first, no wheel or touch capture.

Design line (owner law 13.10.2026, to be built through Claude Design): palette from a Greek hydrographic chart, not the AI default: chart white #F6F9FB background, land #E4E8E2, a sea-depth ramp #DCEBF4 → #0D3B66 for the price heat, one port-buoy red #C8102E for the user's selection only; figures in IBM Plex Mono (tabular, like survey sheets), Hebrew in the site's skin-A text face. Why not default: no cream, no terracotta or gold, no purple gradient; the colours come from the sea charts that sailors use for these same islands.

---

## 7. No-cannibalization plan

### 7.1 Slug, title, H1, breadcrumb (checked with the owner's tools)

| Item | Proposal | Check |
|---|---|---|
| Slug | **/prices-greece/** | No nad-lan URL starts with "prices" (first-word scan of 4,579 sitemap URLs + the 3 new Greece pages). No word repeats inside it. It follows the Greece-children pattern (acquisition-greece, taxation-greece-israel). "price" (singular) is taken as a first word by /price-list-dubai/, so "price-list-greece" is out. The token "greece" is already shared by 4 URLs (url_word_audit --token greece: /short-term-rentals-...-greece/, /acquisition-greece/, /taxation-greece-israel/, /global/greece/). Zero-overlap fallback if Ben wants no shared token at all: **/sqm-greece/** ("sqm" is in no URL). |
| SEO title (45 chars) | **כמה עולה דירה ביוון? מחירון 2026 לפי אזור ואי** | title_start_audit --check: OK. Starts with the top query (2,230 impressions at jus-tice); does not start "מחירי דירות" (city pages, Dubai) and differs from jus-tice's start "מחירי דירות ביוון 2026". |
| H1 (47 chars) | **מחירון נדל״ן ביוון 2026: מחיר למ״ר בכל אזור ואי** | OK. "מחירון נדלן" is not a 2- or 3-word start of any live title ("מחירון הדירות של ישראל", "מחירון חנויות", "מחירון רמת גן", "מחירון דקל" are different). |
| Breadcrumb label | **מחירון יוון** (נדל״ן > השקעות בחו״ל > יוון > מחירון יוון) | OK; --trio: title / H1 / breadcrumb are three different strings. |

Note: the title cache used by title_start_audit was built at 16:01 UTC, before today's Greece pages went live; their live titles were fetched separately (acquisition: "דירה ביוון לישראלים..." / "לקנות דירה ביוון 2026..."; taxation: "מיסוי דירה ביוון לישראלים..." / "מס על דירה ביוון..."; Athens: "דירה באתונה..." / "אתונה: דירות למכירה...") and none clashes. The cache was not refreshed because this task may not write outside this folder.

### 7.2 Who owns what on nad-lan (and the links that make it stick)

| Page | Keeps | Gets from the price list | Gives to the price list |
|---|---|---|---|
| /prices-greece/ (new) | national and regional/island price intent, rent level, the tools in section 6 | — | — |
| /global/greece/ (hub, ranks #3/#4 for price-per-m² today) | invest-in-Greece intent | a link back "יוון" (breadcrumb parent) | its 3-number price box stays short and gains the link **"מחירון נדל״ן ביוון לפי אזור ואי"** so the price intent moves by anchor, nothing deleted |
| /athens-apartments/ | all Athens price intent (neighbourhood ladder) | the Athens and Piraeus rows link "מחירי אתונה לפי אזור" | a link "מחירי יוון מחוץ לאתונה" from its "אתונה, סלוניקי, כרתים או חלקידיקי" section |
| /acquisition-greece/ | buying costs, steps | the budget tool's "~10% costs" line links "מחשבון עלות הקנייה" | a link "כמה עולה דירה בכל אזור ביוון" |
| /taxation-greece-israel/ | tax | one link from the translator and the yield column | none needed |
| STR Greece page | short lets | the short-let layer links there | none needed |
| /price-list-dubai/ | Dubai | optional sibling link "מחירון יוון" | optional sibling link "מחירי דירות דובאי" |

### 7.3 How the nad-lan page and jus-tice's page differ

| | jus-tice /greece-price-list/ | nad-lan /prices-greece/ |
|---|---|---|
| Angle | legal publisher: what each region costs and what the law and ownership look like there | data instrument for buyers: dated numbers, maps, tools, the Israeli lens |
| Format | one 12,600-word article, one table | an interactive stage + a 100-row table + short explanatory article |
| Title lead | "מחירי דירות ביוון 2026" | "כמה עולה דירה ביוון?" / "מחירון נדל״ן ביוון" |
| Numbers | ranges, undated | per row: source + quarter |
| CTA | a lawyer | WhatsApp advice, projects; and the one link to a jus-tice lawyer |

Both domains can rank on the same SERP (two results for the owner). The risk is not cannibalization across domains but duplicate text: the nad-lan page must be written fresh, not adapted from jus-tice.

### 7.4 Where nad-lan links to jus-tice (one link)

- **URL:** https://jus-tice.co.il/greece-lawyers/ (H1 "עורך דין ביוון", modified 19.9.2026; it carries the official foreign-buyer requirements, the law 5100/2024 amounts and a list of lawyers).
- **Anchor:** **"עורך דין ביוון לבדיקת זכויות בנכס"**.
- **Place:** the short block right after the full table, "לפני שמתחייבים על נכס" (one sentence: price is the start; title, debts, illegal building and the border-zone permit are checked by a lawyer in Greece). One normal follow link, editorial, not in the footer, not sitewide.
- **Why this URL and not the others:**
  - it is a **different intent** (a lawyer), the natural next step after reading prices, so nad-lan sends a lead-ready reader to the owner's other business without competing with itself;
  - the page is weak today (Search Console: 71 impressions in 13 weeks, average position 32; "עורך דין נדלן יוון" position 18), so a topical link from a strong price page helps it most;
  - linking to /greece-price-list/ would hand the price reader to the rival page for the same query and tell Google both pages answer the same thing;
  - linking to /buying-property-in-greece/ would compete with nad-lan's own /acquisition-greece/.
- **The other direction (owner's word only, jus-tice side, a finding):** jus-tice's price page could cite the nad-lan list once as its quarterly data source, and its golden-visa, VAT, ENFIA, treaty and Lefkada/Mykonos lines need correcting (section 3.1). Any jus-tice edit goes through the justice-page-dna skill.

---

## 8. Search Console (read-only), 22.7 to 20.10.2026

- **jus-tice.co.il, pages containing "greece"** (`dna-raw/gsc-justice-greece.csv`, 695 query-page rows): /greece-price-list/ 11,035 impressions in the query table (156 queries; the page-level total is 22,843 impressions and 92 clicks, `dna-raw/gsc-justice-pricelist-daily.csv`, weekly 1,550 to 2,240 impressions, position 7.2 to 8.5, no decline); /investing-in-greece-real-estate/ 1,753 at 42.2; /buying-property-in-greece/ 1,638 at 34.1; /real-estate-market-greece-cyprus/ 167 at 20.7; /greece-lawyers/ 71 at 32.3; /greece-financing/ 46; the treaty page 33; a 2021 lawyers PDF 182.
- **nad-lan.co.il, pages containing "greece" or "athens"** (`dna-raw/gsc-nadlan-greece.csv`, `gsc-nadlan-athens.csv`): only the hub has data (20 queries, all at 0 clicks): "כמה עולה דירה ביוון" position 14 (3 impressions), "יוון נדלן" 7, "ויזת זהב יוון" 2, "עורך דין נדלן יוון" 1, "נדלן ביוון" 51.5 (12 impressions). The three pages published today have no data yet.

---

## 9. Data cautions for whoever builds the page

- Spitogatos Q2 2026 holiday-homes blog text and table disagree on 4 places (Porto Rafti, Palaia Fokaia, Poros, Spetses); the data agent flagged it. Show the table value and say "לפי הטבלה".
- Asking-price averages from one agency (Greca, green-acres, GREI) are not market numbers; label them or leave them out.
- Island averages from small samples (Antiparos: 104 of 149 listed flats are new builds) need a sample note or a minimum-sample rule like Greca's.
- Bank of Greece revisions: 2025 growth appears as +7.8% (GPG) and +8.3% "revised September 2026" (BuyGreece). Use the latest BoG release the data agent has, with its date.
- The € to ₪ rate must be the Bank of Israel representative rate with its date (jus-tice's fixed 4.0 is the anti-pattern).
- Unknown = omitted on the page (owner honesty law): a row with no rent data shows no yield, not "n/a".

---

## 10. DataForSEO spend

| Call | Count | Cost reported by the API |
|---|---|---|
| Google Ads search volume (live) | 1 task, 66 keywords | $0.09 |
| Google Ads keywords for keywords (live) | 1 task, 8 seeds → 18 ideas | $0.09 |
| SERP Google organic live advanced, depth 20, async AI Overview, PAA | 15 tasks | $0.0814 |
| User data (balance) | 1 | free |
| **Total for this research** | | **≈ $0.26** (account balance before: $25.72; the account is shared with other sessions) |

## Appendix: reproduce

- SERP parse: `scratchpad\gp\serp_parse.py` (reads the saved API responses, writes `dna-raw\serp-NN.json` and `_compact.json`).
- Page fetch and metrics: `scratchpad\gp\fetch_analyze.py urls.tsv <private pages folder>` (stdlib only; run with `python -I`).
- Matrix: `scratchpad\gp\matrix.py`.
- Search Console: `python C:\Users\777\Documents\GSC-Data\tools\gsc_api.py query --site https://jus-tice.co.il/ --start 2026-07-22 --end 2026-10-20 --dimensions query,page --filter-page contains:greece --out ...` and the same for `sc-domain:nad-lan.co.il` (also `contains:athens`, and `--dimensions date --filter-page contains:greece-price-list` for the weekly series).
- Slug and titles: `python tools/gsc/url_word_audit.py --token greece|prices|price|greek`, `python tools/title_start_audit.py --check "..."` and `--trio "..." "..." "..."`.
