# Greece property cluster: SERP DNA research (Hebrew market, Israel)

Prepared 22.10.2026 for nad-lan.co.il. Read-only research: nothing was changed on any website.

- Market: Google Israel (location 2376), Hebrew, desktop. Keyword data from Google Ads through DataForSEO (12 months, Oct 2025 to Sep 2026). SERPs pulled live through DataForSEO on 22.10.2026, 16:01 to 16:03 UTC (time per SERP below).
- Competitor pages were downloaded as raw HTML on 22.10.2026, 16:05 to 16:15 UTC. The raw files and the extracted text are in `raw/pages/`. Every competitor number below was counted by a script on that raw HTML. The opening paraphrases and the "gets wrong" notes come from reading the full extracted text.
- Search Console (read-only) for both of the owner's sites, 20.7 to 19.10.2026: `raw/gsc-nadlan-greece-pages.csv` and `raw/gsc-justice-greece-pages.csv`.
- Files: `keywords-greece.csv` (371 keywords, clustered), `serps-greece.json` (14 SERPs, compact), `raw/serp-XX.json` (full DataForSEO responses), `raw/sv-batch1.json`, `raw/sv-batch2.json`, `raw/ideas.json`, `raw/pages/*.html|.txt`, `raw/pages/_analysis.json`.
- Evidence class: everything in this file is **code** evidence (API data and raw HTML parsing), not eyes. No page was viewed rendered.

---

## 0. Five things to know before planning (read first)

1. **We already own a Greece hub URL.** `https://nad-lan.co.il/global/greece/` exists (H1 "השקעות נדל"ן ביוון: העולם המלא למשקיע", FAQPage, BreadcrumbList נדלן > השקעות בחו"ל > יוון). In the last 3 months it got 57 impressions for "נדלן ביוון", "פרויקטים ביוון", "השקעה ביוון" and similar, at positions 30 to 60. The owner's rule is to reuse and expand the owning page, so the cluster hub is this URL. Do not mint a new hub. Defects found on it (code evidence):
   - it is **not in the sitemap list** (`sitemap-urls.txt`, 4,579 URLs, has no `/global/<country>/` page at all);
   - it has **two `<h1>` tags**: the logo `<h1><a>נדלן</a></h1>` plus the page H1, which breaks the "exactly one h1" law;
   - it is thin, with about 450 words of body text;
   - its rental-tax line says "15% עד 12 אלף אירו, ואז 35%/45%", while our own STR Greece page (sourced to the Greek finance ministry) gives the 2026 scale 15/25/35/45. Our two pages contradict each other.
2. **The owner's other site already competes here.** jus-tice.co.il has three Greece pages:
   - `/greece-price-list/` got 4,486 impressions in 3 months and ranks at **positions 3 to 5** for "כמה עולה דירה ביוון", "מחירי דירות ביוון", "מחיר דירה ביוון" and "דירה ביוון מחיר". It also ranks **#2 for "נדלן בכרתים"** today.
   - `/buying-property-in-greece/` sits at positions 31 to 37 for "רכישת/קניית בית ביוון".
   - `/investing-in-greece-real-estate/` sits at positions 42 to 58 for "השקעה/השקעות ביוון".

   A nad-lan price page would compete with the owner's best Greece ranking. Which domain owns which intent is the owner's decision (section 6.3).
3. **Google shows an AI Overview on 13 of 14 SERPs.** The only one without it is "השקעות נדלן ביוון". AIO cites gogreece.co.il (7 SERPs), nadlanmaster.co.il (6), green-acres.gr (6), palmo-group.com (4), greece-islands.co.il (4) and grei.co.il (4). **nad-lan.co.il and jus-tice.co.il are cited nowhere.**
4. **Most of the market's facts are stale or wrong**, so being right is a moat:
   - Golden visa at "€250K" still appears on yad2, Maariv, palmo, gogreece, nadlanexpert and in **our own STR page's meta description**.
   - "With the treaty you pay tax only in Greece, not in Israel" appears on nadlanmaster (Greece and Athens pages), gogreece, Maariv and thisisgreece.
   - thisisgreece says the seller pays transfer tax, that capital-gains tax is 15% if you sell within 5 years, and that rental tax runs 9 to 44%.
   - beta-estate and palmo show the same copied Athens table with "+45.2% in 2022".
5. **Several high-volume terms are travel intent, not purchase intent:**
   - "וילה/וילות ביוון" (260): the SERP is Airbnb, Booking and villa-rental agencies.
   - "וילה בכרתים" (210, peaks Jul to Aug).
   - "דירה ברודוס" (90): the SERP is hotels.
   - "ויזת זהב" (170): the AIO answers about the **Visa Gold credit card**.
   - "חלקידיקי" (8,100) and "גליפדה" (480) are destination terms.

   These are recorded as secondary or out of scope in the CSV, not as page targets.

---

## 1. Keyword universe

371 keywords: 228 seeds plus 183 Google Ads ideas, minus duplicates. Google Ads merges close variants and returns the same number for each, for example נדלן / נדל"ן / נדל ן and דירה / דירות. In the CSV these share a `variant_group`, and only one row per group has `count_in_total=yes`. Volumes are Google's rounded buckets (10, 20, 30, 40, 50, 70, 90, 110, 140, 170, 210, 260, ...). Treat them as orders of magnitude.

### 1.1 Head terms (purchase or investment intent)

| Keyword (variants) | Vol/mo | CPC $ | Comp. | 12-mo trend (Oct-25 to Sep-26) | Note |
|---|---|---|---|---|---|
| נדל"ן ביוון / נדלן ביוון | 210 | 5.94 | MED | 210,210,170,170,170,210,260,260,260,260,260,210 (up) | hub head term |
| דירה באתונה / דירות באתונה | 170 | 1.36 | MED | flat 110 to 210 | SERP mixes purchase and holiday flats |
| בתים למכירה ביוון ליד הים | 170 | 1.54 | MED | up | from Google ideas |
| דירה ביוון / דירות ביוון | 140 | 2.61 | MED | flat | broad; SERP = FB groups + buying guides |
| בתים למכירה ביוון | 140 | 0.97 | MED | up | |
| greece real estate | 110 | 0.77 | MED | flat | English-language Israeli searches |
| golden visa greece | 110 | 4.69 | MED | flat | |
| גולדן ויזה יוון | 90 | 1.39 | MED | 50 to 140, up | |
| דירות למכירה באתונה / דירה למכירה באתונה | 90 | 1.79 | MED | flat | |
| דירות למכירה ביוון / דירה למכירה ביוון | 90 | 1.78 | MED | up | |
| בתים ביוון | 90 | 1.72 | MED | up | |
| השקעה ביוון / השקעות ביוון | 70 | **13.16** | MED | down | highest CPC in the set: commercial value |
| השקעות נדל"ן ביוון / השקעות נדלן ביוון | 70 | 4.26 | MED | down | **no AIO** on this SERP |
| דירה/דירות להשקעה ביוון | 70 | 4.37 | MED | flat | |
| ויזת זהב יוון / ויזה זהב יוון | 70 | 1.33 | MED | up | |
| בית ביוון | 70 | 1.79 | MED | up | |
| דירה ביוון למכירה | 70 | 1.82 | MED | up | |
| קניית בית ביוון | 50 | 2.00 | MED | up (110 in Aug and Sep 2026) | |
| נדל"ן באתונה | 50 | 5.60 | MED | down | |
| אמנת מס ישראל יוון | 50 | n/a | LOW | flat | tax |
| דירה/דירות בסלוניקי | 40 | 1.28 | MED | flat | Israelis say סלוניקי; "תסלוניקי" has no volume |
| נכס/נכסים ביוון | 40 | 1.57 | HIGH | flat | |
| קניית דירה ביוון | 30 | 2.03 | MED | flat | |
| מיסוי ביוון | 30 | n/a | LOW | flat | |
| נדלן בכרתים / דירה בכרתים | 30 each | 1.3 to 1.5 | MED | up | |
| כמה עולה דירה ביוון / מחירי דירות ביוון | 30 each | 1.6 to 2.4 | MED/LOW | flat | jus-tice ranks 3 to 5 |
| השקעות נדלן באתונה | 30 | 10.84 | MED | down | |
| ENFIA | 20 | n/a | LOW | flat | |
| משכנתא ביוון | 20 | 0.67 | MED | down | |
| פתיחת חשבון בנק ביוון | 20 | 0.52 | LOW | down | |
| מס רכישה ביוון | 10 | 0.62 | LOW | 70 in Sep 2026 (spike) | |

Out of scope or other intent (kept in the CSV as OUT): יוון 27,100 and אתונה 18,100 (travel); חלקידיקי 8,100 (travel, summer peaks); נדלן בקפריסין 260 and השקעה בקפריסין 110 (Cyprus hub); השקעות נדלן בחול 210 (generic abroad); דרכון יווני 70 and אזרחות יוונית 50 (citizenship by descent, not property); רילוקיישן ליוון 70 (relocation, CPC $9; a possible future page); airbnb אתונה 70 (mostly travellers).

No measurable volume (Google Ads null) for: מיסוי נדל"ן ביוון, נדלן בתסלוניקי, airbnb ביוון, תשואה ביוון, קרקע ביוון, מגרש ביוון, עורך דין ביוון, מתווך ביוון, דירה בגליפדה, ניהול נכסים ביוון, every "מס על דירה בחו"ל" phrasing, השקעה ביוון 2026, יוון או פורטוגל. These are still worth covering as page sections, because AIO and PAA pick them up, but they are not page owners.

### 1.2 Clusters and the page each one belongs to

Totals are the sum of distinct variant groups (`count_in_total=yes`). "Clean" excludes rows marked mixed or secondary (travel-dominated SERPs).

| Cluster (page) | Deduped volume | Clean purchase-intent volume | Top owned terms |
|---|---|---|---|
| HUB: invest in Greece, broad | ~700 | ~700 | נדל"ן ביוון 210, greece real estate 110, השקעה ביוון 70, השקעות נדל"ן ביוון 70, דירות להשקעה ביוון 70, נכס ביוון 40, נדלן יוון 30, פרויקטים ביוון 20, יוון או קפריסין 20 |
| ATH: Athens apartments | ~1,220 | ~740 | דירה/דירות באתונה 170, דירות למכירה באתונה 90, נדל"ן באתונה 50, דירות באתונה למכירה 40, קוקאקי 40, קיפסלי 30, השקעות נדלן באתונה 30, כמה עולה דירה באתונה 20 (+ גליפדה 480, travel-mixed) |
| SEA: seaside houses and islands | ~1,520 | ~920 | בתים למכירה ביוון ליד הים 170, בתים למכירה ביוון 140, בתים ביוון 90, בית ביוון 70, וילה למכירה ביוון 30, Evia/Corfu/Rhodes/Lefkada/Paros "בתים למכירה ב..." long tail (+ וילה ביוון 260 mixed, דירה ברודוס 90 mixed) |
| ACQ: how to buy, costs, financing | ~620 | ~620 | דירה/דירות ביוון 140, דירות למכירה ביוון 90, דירה ביוון למכירה 70, קניית בית ביוון 50, קניית דירה ביוון 30, משכנתא ביוון 20, פתיחת חשבון בנק ביוון 20, רכישת דירה ביוון 20, מס רכישה ביוון 10 |
| GV: golden visa / residency | ~540 | ~370 | golden visa greece 110, גולדן ויזה יוון 90, ויזת זהב יוון 70, גולדן ויזה 40, ויזת זהב ביוון 20, תושבות ביוון 20 (+ ויזת זהב 170, credit-card mixed) |
| CRE: Crete | ~500 | ~150 | נדלן בכרתים 30, דירה בכרתים 30, בתים לשיפוץ בכרתים 20, דירות למכירה בכרתים 10, וילות למכירה בכרתים 10 (+ וילה בכרתים 210 holiday-mixed) |
| THE: Thessaloniki and Halkidiki | ~170 | ~170 | דירה בסלוניקי 40, דירות למכירה בסלוניקי 20, נדלן בסלוניקי 20, בתים למכירה בחלקידיקי 20 + related searches "פרויקטים בסלוניקי" and "דירות חדשות בסלוניקי" |
| TAX: Greek + Israeli tax | ~130 | ~130 | אמנת מס ישראל יוון 50, מיסוי ביוון 30, ENFIA 20, מס שבח/ירושה/הכנסה ביוון 10 each |
| PRICE: national price questions | ~130 | ~130 | כמה עולה דירה ביוון 30, מחירי דירות ביוון 30, בית ביוון מחיר 30, דירה ביוון מחיר 20. **Owner decision** (jus-tice ranks 3 to 5) |
| STR (existing page) | ~30 | n/a | airbnb יוון 30. The STR intent is already owned by `/short-term-rentals-abroad/short-term-rentals-greece/` |

**How many pages:** the hub (the existing `/global/greece/`, expanded) plus **7 children**: Athens, acquisition, seaside, golden visa, Thessaloniki-Halkidiki, tax, Crete. Each child owns one intent with no overlap. Prices stay a hub section until the owner decides about jus-tice. STR stays on the existing STR page. A Greece vs Cyprus comparison is a hub section for now (about 20/mo). Section 6 has the details.

Seasonality: houses, villas and islands rise from April and peak July to September. Athens apartments, the golden visa and the hub are flat or slightly up. Publish the seaside and Crete pages before spring 2027.

---

## 2. Our existing Greece pages (so the cluster does not cannibalise them)

### 2.1 `/short-term-rentals-abroad/short-term-rentals-greece/` (the STR page: keep the STR intent here)

- Title "השכרה לטווח קצר ביוון | נדלן חכם". H1 "השכרה לטווח קצר ביוון למשקיע ישראלי: רגולציה, מסים, מחירים ותהליך רכישה". About 2,200 words, Article schema, published 29.5.2026, modified 15.6.2026.
- **What it covers well, with sources:**
  - the STR definition (up to 59 days per contract, from 1.1.2024);
  - AADE registration and the AMA number, plus short-stay declarations;
  - the safety and operating rules from 1.10.2025, with the €5,000 fine;
  - the Athens freeze on new STR registrations in municipal districts 1 to 3 (Law 5162/2024), extended through 2026;
  - VAT on STR: up to 2 properties exempt; 3+ properties or a company pay 13%;
  - the climate resilience fee;
  - the 2026 rental-income scale 15/25/35/45;
  - the Israeli side: worldwide taxation, the 15% track without foreign-tax credit, which payments can be credited;
  - Bank of Greece price data (Q4-2025: +7.6% nationally, Athens +5.9%, Thessaloniki +8.0%; 2025 average +7.8%);
  - GPG gross yield 4.38%, flagged as unverified;
  - five common mistakes and a FAQ.
- **Overlap risk:** it also has short sections on "תהליך רכישה לזר" (AFM, 3% transfer tax, VAT suspension to 31.12.2026), prices and regions. The new pages own those intents. The STR page should keep only short summaries and link out (purchase, tax and Athens to the new children; the hub as "parent").
- **Defects, all visible in the public HTML:**
  - leftover editor text "מאמר מוכן להדבקה";
  - two different "עודכן ונבדק" lines (2026-05-30 and 28.5.2026);
  - a visible "## תגיות מוצעות" block listing tags;
  - several cut-off sentences ("סטטוס נכס ספציפי:", "...ולפי חדר או דירה... מעל 80", "בודקים דיווח, זיכוי מס זר, מסלול 15%", "אוטומטית של");
  - the meta description promises "ויזת זהב מ-250 אלף יורו", which is outdated and not in the body;
  - no breadcrumb, no images, and a FAQ without FAQPage schema.

  These go on the release checklist as no-silent-gap items.

### 2.2 `/global/greece/` (the hub: expand it)

- Covers, in about 450 words:
  - a numbers box (Athens €2,500 to 4,500/m², gross yield 4 to 6%, golden visa 800/400, transfer tax 3.09%, ENFIA, rental tax, free ownership for foreigners except border areas, top areas);
  - two sample projects (Koukaki, Glyfada);
  - a map;
  - purchase in 3 actors (lawyer, notary, accountant for the AFM), 6 to 10 weeks, power of attorney;
  - golden visa facts (800/400/250-special, family, not citizenship, no right to work as an employee);
  - risks (pre-1985 seismic code, debts that stay with the property, the Athens STR freeze);
  - a 3-question FAQ;
  - a lead CTA.
- Facts are mostly current. The rental-tax line is outdated (see section 0). It is thin and missing from the sitemap, and it has two H1s.

### 2.3 Sample projects `/global/project/koukaki-athens-residence/` and `/global/project/glyfada-coast-suites-athens/`

- About 175 words each, labelled "פרויקט להמחשה על בסיס נתוני שוק אמיתיים - אינו פרויקט ספציפי בשיווק", with an interactive building, a meeting-request form and "More posts" (which shows unrelated Dubai and Israel posts).
- These are the hub's "stage" assets. Link to them from the Athens child, Koukaki and Glyfada neighbourhood rows. Do **not** use them as ranking targets. Honesty law: they must stay labelled as illustrative.

### 2.4 jus-tice.co.il Greece pages (owner's other site)

| URL | H1 | Words | GSC 3-mo impressions | Ranking today |
|---|---|---|---|---|
| /greece-price-list/ | מחירי דירות ביוון 2026: כמה עולה דירה ביוון לפי אזור | ~12,300 (very long) | 4,486 (+ fragment URLs) | 3 to 5 for price queries; #2 "נדלן בכרתים" |
| /buying-property-in-greece/ | קניית דירה ביוון: מחירים, מיסים והליך הרכישה לישראלים | ~29,500 extracted (very long, many legal sub-topics) | 1,663 | 31 to 37 |
| /investing-in-greece-real-estate/ | תשואות נדל"ן ביוון לפי אזור: מה מניב ומה מסוכן | ~3,200 | 1,761 | 42 to 58 |

These pages are in the "מקרקעין | נדל"ן" legal-articles section, with Article schema and the author "Jus-Tice.co.il".

---

## 3. SERP snapshots (14 keywords, Google Israel, Hebrew, desktop)

Retrieved 22.10.2026 between 16:01:37 and 16:03:41 UTC through DataForSEO live advanced (depth 30, PAA click depth 2, async AIO loading on). The top 10 organic results are listed; positions 11 to 30 are in `serps-greece.json`.

### 3.0 Summary across SERPs

- **AI Overview present on 13/14 SERPs. Absent only on "השקעות נדלן ביוון".** Gist of the AIO answers:
  - "נדל"ן ביוון" / "השקעה ביוון": yields 5 to 10% (STR 7 to 10%); entry prices from €75 to 90K for small Athens flats; hot spots Athens, Piraeus, Thessaloniki, Crete, Halkidiki; transfer tax ~3.09%; golden visa €400K/€800K by area; a dubious line "0% capital gains for up to 3 apartments"; a reminder to use an independent local lawyer, engineer and notary; extra costs; then a pointer to Green-Acres and to Israeli brokers G.R.E and Palmo.
  - "דירה ביוון" / "דירה באתונה" / "דירות למכירה באתונה": €/m² figures by neighbourhood (Kolonaki from €5,800, Plaka €5,500, Glyfada €3,200 to 3,600, Piraeus €2,500; Athens average ~€2,978 to 3,168; Patisia ~€1,617), a 70 m² flat at €125 to 320K, and named neighbourhoods (Koukaki, Pagrati, Kypseli, Kolonaki, Exarchia). The AIO cites listing pages (green-acres, gogreece/properties).
  - "קניית דירה ביוון": steps (find, legal check in the cadastre, AFM, bank account, contract), ancillary costs **10 to 15%** of the price including 3.09%.
  - "גולדן ויזה יוון": a 5-year renewable permit; €800K in Athens, Thessaloniki, Mykonos, Santorini and Piraeus; €400K elsewhere; €250K for conversions and listed buildings.
  - "אמנת מס ישראל יוון": signed October 1995, in force 1.1.1999, English text prevails; links the gov.il PDF.
  - "נדלן בכרתים": flats €100 to 250K, ~9% annual rise, Rethymno median ~€3,548/m², yields 5 to 10%, golden visa "from €250K" (misleading).
  - "וילה ביוון" / "דירה ברודוס": holiday-rental answers. "ויזת זהב": a credit-card answer.
- **AIO citations by domain (count of SERPs):** gogreece.co.il 7, nadlanmaster.co.il 6, green-acres.gr 6, palmo-group.com 4, greece-islands.co.il 4, grei.co.il 4, greecerealestate.co.il 3, greecestate.co.il 3, airbnb/booking 3 each, nadlan-greece.co.il 2, yamasre.com 2, geffen-global.co.il 2, y-tax.co.il 2, then single citations (beta-estate, nadlan1on1, nadlanistka, euro-pass, progreecegroup.gr, rofeh-law, itzikharel, new-greece, gov.il, oritax, cpa.co.il, ...).
- **People Also Ask** appeared on only 3 SERPs (נדל"ן ביוון, דירה ברודוס, נדלן בכרתים). Property PAA questions:
  - מה מחירו של דירה באתונה?
  - איפה אפשר למצוא בתי מלון למכירה ביוון?
  - איפה אפשר למצוא בתים למכירה ביוון ליד הים?
  - איפה אפשר למצוא בית ליד הים ביוון?
  - איזה עיר הכי יפה ביוון?
  - איפה אפשר לקנות דירה ביוון כדי להשקיע?
  - **האם ישראלים יכולים לקבל משכנתא ביוון?**
  - איפה אפשר למצוא בית נופש ביוון למכירה?
  - איזה אי ביוון הוא זול?
  - האם יש בית באתונה למכירה?
  - Brand questions: מי הבעלים של פאלמו נדלן?, האם ביתא נדל"ן מספקת תביעות?
- **Related searches worth owning:** האם כדאי לקנות דירה ביוון (3 SERPs, counting "people also search"), דירות למכירה ביוון יד 2 (6 SERPs), פרויקטים בסלוניקי, דירות חדשות בסלוניקי, קניית בית באתונה, דירות למכירה לוטראקי יוון, מפת שכונות באתונה, דירות באתונה להשקעה, דירות באתונה על הים, בית ביוון על הים, בתים למכירה בכרתים ליד הים, בתים לשיפוץ בכרתים, בתים למכירה בחאניה כרתים, שטחים למכירה ביוון / קרקע ביוון, וילה ביוון על הים למכירה, ויזת זהב 2025 / פורטוגל / קפריסין / מלטה / הונגריה / איטליה.
- **SERP shape:**
  - The head terms are fragmented: developer and broker homepages (shoval, palmo, beta, grei, new-greece), Facebook groups (11 slots across the SERPs), forum threads (hasolidit, from 2018), yad2's thin blog (534 words), listing portals (green-acres.gr in Hebrew, greecestate, gogreece, geoln, domaza) and a few long guides (nadlanmaster, thisisgreece, beta, palmo).
  - No independent, data-led Hebrew guide holds a top-3 spot. That is the gap.
  - A local pack (3 Israeli brokers) shows on "השקעות נדלן ביוון".
  - Ads appear on 3 SERPs (דירה באתונה, גולדן ויזה יוון, דירות למכירה באתונה): palmo-group, beta-estate, lp.nadlan1on1. **Brand-review searches** ("פאלמו נדלן תביעות", "ביתא נדלן חוות דעת", "חברת פאלמו חוות דעת") show buyers are checking the companies themselves, so an independent "how to check a Greek developer/broker" section wins trust.
  - YouTube shows in 2 SERPs (Nir Leibel/Yamas). A Maariv advertorial is #1 for "השקעות נדלן ביוון".

SERP-by-SERP detail follows.

### "נדל"ן ביוון" (volume 210/mo) - retrieved 2026-10-22 16:01:37 UTC

SERP features: ai_overview, organic, people_also_ask, related_searches.

| # | Domain | Title (as shown) | URL |
|---|---|---|---|
| 1 | shovalyazamoot.com | דירות להשקעה ביוון | shovalyazamoot.com/projects |
| 2 | nadlanmaster.co.il | השקעות נדל"ן באתונה ב-2026 - מדריך למשקיע (ודירות להשקעה) | nadlanmaster.co.il/נדלן-באתונה/ |
| 3 | facebook.com | פורום השקעות נדל"ן באתונה | facebook.com/groups/363764060414566/ |
| 4 | grei.co.il | GREI: תשקיעו חכם בנדל"ן בחו"ל | grei.co.il/ |
| 5 | blog.yad2.co.il | נדל"ן ביוון - | blog.yad2.co.il/נדלן-ביוון/ |
| 6 | beta-estate.com | מחירי דירות באתונה: סקירה 2026 / כמה עולה דירה ... | beta-estate.com/real-estate-prices-athens/ |
| 7 | hasolidit.com | נדלן ביוון | hasolidit.com/kehila/threads/נדלן-ביוון.7791/ |
| 8 | greecestate.co.il | - נדל"ן ביוון, קניית בית באיי יוון - נדלן ביוון | greecestate.co.il/country/12 |
| 9 | beta-estate.com | כמה הון עצמי צריך כדי לקנות דירה ביוון? המדריך המלא לשנת 2026 | beta-estate.com/how-much-equity-needed-to-buy-apartment-in-greece/ |
| 10 | facebook.com | השקעות נדל"ן ביוון - Greek Property Group - GPG | facebook.com/greekpropertygroup/?locale=el_GR |

People Also Ask: מה מחירו של דירה באתונה?; איפה אפשר למצוא בתי מלון למכירה ביוון?; איפה אפשר למצוא בתים למכירה ביוון ליד הים?; איפה אפשר למצוא בית ליד הים ביוון?; איזה עיר הכי יפה ביוון?; איפה אפשר לקנות דירה ביוון כדי להשקיע?; האם ישראלים יכולים לקבל משכנתא ביוון?; מי הבעלים של פאלמו נדלן?; האם ביתא נדל"ן מספקת תביעות?.

Related searches: האם כדאי לקנות דירה ביוון; דירות למכירה ביוון יד 2; גריי יוון; GREI; קניית בית באתונה; דירות למכירה לוטראקי יוון; פרויקטים בסלוניקי; דירות חדשות בסלוניקי.

AI Overview: YES. Cited domains: palmo-group.com, nadlanmaster.co.il, greece-islands.co.il, greecerealestate.co.il, nadlan-greece.co.il, yamasre.com, greecestate.co.il, green-acres.gr.

### "דירה ביוון" (volume 140/mo) - retrieved 2026-10-22 16:01:56 UTC

SERP features: ai_overview, organic.

| # | Domain | Title (as shown) | URL |
|---|---|---|---|
| 1 | facebook.com | נדל״ן ביוון | facebook.com/groups/2653556238122827/ |
| 2 | facebook.com | הי כולם, מחפשים לרכוש בית ביוון. מקום כזה שטוב לגור בו | facebook.com/groups/635562977312120/posts/2034039704131100/ |
| 3 | shovalyazamoot.com | דירות למכירה ביוון ליד הים | shovalyazamoot.com/blog/דירות-למכירה-ביוון-ליד-הים |
| 4 | new-greece.co.il | קניית דירה ביוון – איך זה עובד | new-greece.co.il/buying-an-apartment-in-greece/ |
| 5 | facebook.com | דירות ונכסים ביוון | facebook.com/groups/502177497529367/ |
| 6 | thisisgreece.co.il | בתים למכירה ביוון - איך קונים בית ביוון? (מדריך, דירות ונכסים) | thisisgreece.co.il/houses-for-sale-in-greece/ |
| 7 | facebook.com | Real Estate Boutique- נדל"ן יוון | facebook.com/groups/1428873757528099/ |
| 8 | thisisgreece.co.il | השקעות נדל"ן ביוון - מידע, מדריכים, פרויקטים ונכסים (יוון למשקיע) | thisisgreece.co.il/ |
| 9 | wise.com | נדל"ן ביוון: סקירת מחירי דיור | wise.com/il/blog/real-estate-in-greece |
| 10 | greecestate.co.il | דירות למכירה באתונה - נדל"ן ביוון, קניית בית באיי יוון | greecestate.co.il/country/11 |

People Also Ask: none shown.

Related searches: none shown.

AI Overview: YES. Cited domains: palmo-group.com, nadlanmaster.co.il, gogreece.co.il, grei.co.il, geffen-global.co.il, green-acres.gr, baitbeyavan.com.

### "דירה באתונה" (volume 170/mo) - retrieved 2026-10-22 16:02:07 UTC

SERP features: ai_overview, organic, paid, related_searches.

| # | Domain | Title (as shown) | URL |
|---|---|---|---|
| 1 | new-greece.co.il | דירות למכירה באתונה | new-greece.co.il/apartments-for-sale-in-athens/ |
| 2 | check-in-out.com | דירות מומלצות באתונה: איפה כדאי להזמין דירה לחופשה הבאה? | check-in-out.com/athens-recommended-apartments/ |
| 3 | nadlan-greece.co.il | דירה באתונה - ACHARNON | nadlan-greece.co.il/projects/דירה-באתונה-acharnon/ |
| 4 | urbanikos.co.il | אורבניקוס השקעות נדל"ן ביוון | urbanikos.co.il/ |
| 5 | palmo-group.com | קניית בית ביוון – דירות להשקעה ביוון | palmo-group.com/buying-a-real-estate-in-greece/ |
| 6 | beta-estate.com | ביתא נדל״ן | beta-estate.com/ |
| 7 | nadlanmaster.co.il | פרויקט REDESTOU באתונה - דירות להשקעה במרכז העיר | nadlanmaster.co.il/palmo-athens/ |
| 8 | lametayel.co.il | דירות אתונה (Athens Flats) באתונה | lametayel.co.il/pois/5g98g |
| 9 | he.airbnb.com | נכסים לנופש על החוף באזור מרכז אתונה | he.airbnb.com/central-athens-regional-unit-greece/stays/beachfront |
| 10 | urbanikos.co.il | לוח נדל"ן ביוון - אורבניקוס Archives | urbanikos.co.il/category/4/ |

Ads: palmo-group.com.

People Also Ask: none shown.

Related searches: כמה עולה דירה באתונה; ביתא נדלן חוות דעת; דירות באתונה להשקעה; דירה לקניה באתונה; דירות ביוון; דירות למכירה ביוון יד 2; דירות להשקעה ביוון; אורבניקוס; רכישת דירה להשקעה ביוון; דירה למכירה ביוון; מפת שכונות באתונה; שחר שבק; יוסי פרנק יוון; Airbnb אתונה; בוקינג אתונה.

AI Overview: YES. Cited domains: beta-estate.com, green-acres.gr, gogreece.co.il, nadlan1on1.co.il, palmo-group.com, he.airbnb.com, booking.com.

### "השקעה ביוון" (volume 70/mo) - retrieved 2026-10-22 16:02:15 UTC

SERP features: ai_overview, organic, related_searches.

| # | Domain | Title (as shown) | URL |
|---|---|---|---|
| 1 | palmo-group.com | פאלמו - השקעות נדל"ן ביוון | palmo-group.com/ |
| 2 | nadlanmaster.co.il | השקעות נדל"ן ביוון - מדריך למשקיע, נכסים למכירה (מעודכן 2026) | nadlanmaster.co.il/נדלן-ביוון/ |
| 3 | beta-estate.com | ביתא נדל״ן: השקעות נדל"ן ביוון - השקעות ביוון | beta-estate.com/ |
| 4 | bizportal.co.il | רעיונות השקעה גרועים – רכישת נדל"ן ביוון ובקפריסין ועוד טעויות | bizportal.co.il/globalmarkets/news/article/20016263 |
| 5 | nadlanistka.com | מדריך רכישת דירה ביוון | nadlanistka.com/buy-apartment-in-greece-guide/ |
| 6 | gogreece.co.il | תהליך קניית בית ביוון – מדריך ב-7 שלבים מפורטים | gogreece.co.il/the-investment-process/ |
| 7 | nadlan-greece.co.il | השקעות נדל"ן ביוון / עד 15% תשואה החל מ-50,000 € / נדל"ן יוון | nadlan-greece.co.il/ |
| 8 | facebook.com | השקעות נדל"ן ביוון | facebook.com/groups/635562977312120/?locale=he_IL |
| 9 | lefkadaisrael.com | השקעת נדלן ביוון / לפקדה ישראל יזמות וניהול פרויקטים נדל״ן ביוון | lefkadaisrael.com/השקעת-נדלן-ביוון/ |
| 10 | lefkadaisrael.com | השקעת נדלן ביוון / לפקדה ישראל יזמות וניהול פרויקטים נדל״ן ביוון | lefkadaisrael.com/השקעת-נדלן-ביוון/ |

People Also Ask: none shown.

Related searches: נדלן ביוון; פאלמו נדלן תביעות; פרויקטים להשקעה ביוון; פאלמו נדלן דרושים; דירות למכירה ביוון יד 2; חברת פאלמו חוות דעת; ביתא נדלן; פאלמו לוטראקי; ביתא נדלן חוות דעת.

AI Overview: YES. Cited domains: nadlanmaster.co.il, nadlan-greece.co.il, nadlan-nadlan.co.il, yamasre.com, rofeh-law.com, geffen-global.co.il, gogreece.co.il.

### "גולדן ויזה יוון" (volume 90/mo) - retrieved 2026-10-22 16:02:23 UTC

SERP features: ai_overview, organic, paid, related_searches.

| # | Domain | Title (as shown) | URL |
|---|---|---|---|
| 1 | yamasre.com | פריסייל מיוחד לחברי יאמאס – דירות לגולדן ויזה בהחל מ-250K€ ... | yamasre.com/golden-visa-starting-from-250k-in-thessaloniki/ |
| 2 | yadidlaw.com | השקעות ותושבות ביוון - גולדן ויזה / עו''ד ונוטריון ... | yadidlaw.com/השקעות-ותושבות-ביוון |
| 3 | greekpropertygroup.com | אשרה אירופאית למשקיעים ביוון - Golden Visa Program | greekpropertygroup.com/post/golden-visa |
| 4 | shovalyazamoot.com | השקעה ביוון והמרוץ אל הגולדן ויזה, המדריך המלא - חלק א | shovalyazamoot.com/blog/השקעה-ביוון-והמרוץ-אל-הגולדן-ויזה-המדריך-המלא… |
| 5 | youtube.com | Golden Visa to Greece 🇬🇷 גולדן ויזה יוון (ויזת זהב) | youtube.com/shorts/nO1J661SVNQ |
| 6 | eurobank.gr | Golden Visa השקעת | eurobank.gr/-/media/eurobank/international-customers/pdf-brochure/gol… |
| 7 | bizportal.co.il | מה זאת "ויזת זהב", איזה מדינות מעניקות אותה וכמה נדרש להשקיע? | bizportal.co.il/globalmarkets/news/article/828290 |
| 8 | migration.gov.gr | Golden Visa | migration.gov.gr/en/golden-visa/ |
| 9 | home-li.co.il | מדריך ויזת הזהב (Golden Visa) ביוון: כל מה שמשקיע ישראלי חייב ... | home-li.co.il/BlogPost?id=6ac10b87afe77ac620dff7e7 |
| 10 | golden-visa.gogeek.co.il | גולדן ויזה | golden-visa.gogeek.co.il/ |

Ads: beta-estate.com.

People Also Ask: none shown.

Related searches: ויזת זהב 2025; ויזת זהב איטליה; ויזת זהב הונגריה; ויזת זהב פורטוגל; ויזת זהב מלטה; ויזת זהב קפריסין; ויזת זהב ארהב.

AI Overview: YES. Cited domains: progreecegroup.gr, nadlanmaster.co.il, greece-islands.co.il, gogreece.co.il, y-tax.co.il, euro-pass.co.il.

### "בתים למכירה ביוון" (volume 140/mo) - retrieved 2026-10-22 16:02:31 UTC

SERP features: ai_overview, organic, related_searches, images.

| # | Domain | Title (as shown) | URL |
|---|---|---|---|
| 1 | shovalyazamoot.com | בתים ביוון למכירה: עיר או כפר? - חלק א | shovalyazamoot.com/blog/בתים-ביוון-למכירה-עיר-או-כפר---חלק-א |
| 2 | new-greece.co.il | דירות למכירה באתונה | new-greece.co.il/apartments-for-sale-in-athens/ |
| 3 | greecestate.co.il | - נדל"ן ביוון, קניית בית באיי יוון - נדלן ביוון | greecestate.co.il/country/12 |
| 4 | facebook.com | נכסים מדהימים ביותר למכירה במיקום מושלם ביוון על הים | facebook.com/groups/635562977312120/posts/1752518415616565/ |
| 5 | green-acres.gr | רכישת נדל"ן ב-אתונה: 608 דירות ובתים בבלעדיות למכירה | green-acres.gr/מקרקעין/אתונה |
| 6 | greece-properties.eu | שוק הנדל"ן ביוון: הזדמנויות למגורים והשקעות | greece-properties.eu/he/ |
| 7 | grei.co.il | השקעות נדל״ן מעבר לים - דירות חדשות ויד שניה - GREI | grei.co.il/listings |
| 8 | oasisdevelopment.gr | קרקעות למכירה ולהשכרה ב יוון | oasisdevelopment.gr/he/properties/land |
| 9 | globalnadlan.co.il | בתים למכירה ביוון - המדריך לקניית נכס ביוון / GlobalNadlan | globalnadlan.co.il/houses-for-sale-in-greece |
| 10 | thisisgreece.co.il | השקעות נדל"ן ביוון - מידע, מדריכים, פרויקטים ונכסים (יוון למשקיע) | thisisgreece.co.il/ |

People Also Ask: none shown.

Related searches: דירות ביוון אתונה; דירות למכירה בקולונקי אתונה; דירות למכירה באורופוס יוון; וילות למכירה בחול; שטחים למכירה ביוון; קרקע ביוון; בתים למכירה באנדרוס יוון; נכסים למכירה בכרתים; בתים למכירה בכרתים ליד הים; דירות באתונה למכירה; בתים לשיפוץ בכרתים; דירות באתונה להשקעה; דירות באתונה לנופש; דירות למכירה ביוון יד 2; בתים למכירה בחאניה כרתים; דירות למכירה באתונה יד 2.

AI Overview: YES. Cited domains: greece-islands.co.il, gogreece.co.il, green-acres.gr, geoln.com, grei.co.il.

### "דירות למכירה באתונה" (volume 90/mo) - retrieved 2026-10-22 16:02:41 UTC

SERP features: ai_overview, organic, paid, related_searches.

| # | Domain | Title (as shown) | URL |
|---|---|---|---|
| 1 | gogreece.co.il | דירות למכירה ביוון, דירות למכירה באתונה, לוח יד 2 | gogreece.co.il/properties/ |
| 2 | green-acres.gr | רכישת נדל"ן ב-אתונה: 608 דירות ובתים בבלעדיות למכירה | green-acres.gr/מקרקעין/אתונה |
| 3 | facebook.com | נדל"ן ביוון בין חברים | facebook.com/groups/546052536666316/ |
| 4 | grei.co.il | השקעות נדל״ן באתונה - דירות חדשות ויד שניה למכירה - GREI | grei.co.il/listings/greece/athens |
| 5 | domaza.co.il | דירות למכירה באתונה / domaza.co.il | domaza.co.il/דירות_למכירה_באתונה/ |
| 6 | palmo-group.com | השקעות נדל"ן באתונה דירות באתונה להשקעה | palmo-group.com/real-estate-in-athens/ |
| 7 | urbanikos.co.il | דירות למכירה ביוון - לוח נכסים / עסקאות 2019-2020 + מחירים ... | urbanikos.co.il/app-for-sale-index/ |
| 8 | nadlanmaster.co.il | השקעות נדל"ן באתונה ב-2026 - מדריך למשקיע (ודירות להשקעה) | nadlanmaster.co.il/נדלן-באתונה/ |
| 9 | greecerealestate.co.il | נדל"ן ביוון | greecerealestate.co.il/ |
| 10 | greecerealestate.co.il | נדל"ן ביוון | greecerealestate.co.il/ |

Ads: lp.nadlan1on1.co.il.

People Also Ask: none shown.

Related searches: דירות למכירה ביוון יד 2; דירות באתונה להשקעה; דירות למכירה ביוון סלוניקי; וילות למכירה ביוון; דירות באתונה לנופש; דירות באתונה על הים; האם כדאי לקנות דירה ביוון; בית ביוון על הים.

AI Overview: YES. Cited domains: green-acres.gr, gogreece.co.il, palmo-group.com, greecestate.co.il, grei.co.il.

### "השקעות נדלן ביוון" (volume 70/mo) - retrieved 2026-10-22 16:02:47 UTC

SERP features: organic, local_pack, related_searches.

| # | Domain | Title (as shown) | URL |
|---|---|---|---|
| 1 | maariv.co.il | המדריך למשקיע המתחיל: כך תקנו דירה ביוון ב-8 שלבים | maariv.co.il/business/realestate/article-1093013 |
| 2 | shovalyazamoot.com | דירות להשקעה ביוון | shovalyazamoot.com/projects |
| 3 | hasolidit.com | נדלן ביוון | hasolidit.com/kehila/threads/נדלן-ביוון.7791/ |
| 4 | greece-islands.co.il | השקעות ביוון Investments in Greece | greece-islands.co.il/pages/investments.html |
| 5 | beta-estate.com | פורטוגל או יוון - איפה כדאי להשקיע בנדל״ן בשנת 2026? | beta-estate.com/real-estate-investment-greece-vs-portugal/ |
| 6 | facebook.com | השקעות נדלן יוון קנייה ומכירה real estate in Greece Athens buy ... | facebook.com/migdalimnadlan/?locale=he_IL |
| 7 | green-acres.gr | נדל"ן למכירה יוון: 14838 נכסים בלעדיים | green-acres.gr/he |
| 8 | leibovitch.co.il | רכישת נכס ביוון - המדריך המשפטי המלא למשקיעים ישראלים | leibovitch.co.il/post/רכישת-נכס-ביוון-המדריך-המשפטי-המלא-למשקיעים-ישר… |
| 9 | thisisgreece.co.il | השקעות נדל"ן ביוון - מידע, מדריכים, פרויקטים ונכסים (יוון למשקיע) | thisisgreece.co.il/ |
| 10 | beta-estate.com | כמה הון עצמי צריך כדי לקנות דירה ביוון? המדריך המלא לשנת 2026 | beta-estate.com/how-much-equity-needed-to-buy-apartment-in-greece/ |

People Also Ask: none shown.

Related searches: דירות חדשות בסלוניקי; פרויקטים בסלוניקי; שובל שמי יזמות ובניה בע מ.

AI Overview: absent.

### "קניית דירה ביוון" (volume 30/mo) - retrieved 2026-10-22 16:02:54 UTC

SERP features: ai_overview, organic, people_also_search.

| # | Domain | Title (as shown) | URL |
|---|---|---|---|
| 1 | new-greece.co.il | Home page - יוון החדשה - דירות ובתים ביוון | new-greece.co.il/ |
| 2 | nadlan1on1.co.il | רכישת נכס ביוון – ההזדמנות להשקעה עם ליווי מקיף ואישי | nadlan1on1.co.il/רכישת-נכס-ביוון-ההזדמנות-להשקעה-עם-ליו/ |
| 3 | youtube.com | איך לרכוש נכס או דירה ביוון / יזמות והשקעות נדל״ן ביוון / עם ניר לייבל | youtube.com/watch?v=WJAgFBawwP8 |
| 4 | thisisgreece.co.il | בתים למכירה ביוון - איך קונים בית ביוון? (מדריך, דירות ונכסים) | thisisgreece.co.il/houses-for-sale-in-greece/ |
| 5 | nadlanmaster.co.il | השקעות נדל"ן באתונה ב-2026 - מדריך למשקיע (ודירות להשקעה) | nadlanmaster.co.il/נדלן-באתונה/ |
| 6 | beta-estate.com | משכנתא ביוון 2026: מדריך מקיף לקבלת מימון נדל"ן ביוון | beta-estate.com/mortgage-greece/ |
| 7 | wise.com | נדל"ן ביוון: סקירת מחירי דיור | wise.com/il/blog/real-estate-in-greece |
| 8 | green-acres.gr | רכישת נדל"ן ב-אתונה: 608 דירות ובתים בבלעדיות למכירה | green-acres.gr/מקרקעין/אתונה |
| 9 | thisisgreece.co.il | מחירי דירות ביוון - עלות נכס לפי עיר / אי (ראו מחירון מפורט) | thisisgreece.co.il/property-prices/ |
| 10 | thisisgreece.co.il | מחירי דירות ביוון - עלות נכס לפי עיר / אי (ראו מחירון מפורט) | thisisgreece.co.il/property-prices/ |

People Also Ask: none shown.

Related searches: none shown.

AI Overview: YES. Cited domains: nadlanistka.com, nadlanmaster.co.il, gogreece.co.il, greecerealestate.co.il.

### "וילה ביוון" (volume 260/mo) - retrieved 2026-10-22 16:03:06 UTC

SERP features: ai_overview, organic, hotels_pack, related_searches, images.

| # | Domain | Title (as shown) | URL |
|---|---|---|---|
| 1 | he.airbnb.com | וילות לנופש באזור יוון | he.airbnb.com/greece/stays/villas |
| 2 | greece-islands.co.il | וילות גדולות ביוון | greece-islands.co.il/pages/bigvillas.html |
| 3 | vacance.co.il | Vacance / וילות ביוון, השכרת וילות למשפחות ביוון | vacance.co.il/יוון |
| 4 | booking.com | וילות ביוון | booking.com/villas/country/gr.he.html |
| 5 | mspirit.co.il | וילות ביוון: חבילות נופש יוקרתיות ביוון | mspirit.co.il/וילות-פרטיות/וילות-ביוון/ |
| 6 | tripadvisor.co.il | 10 הכי טובים: וילות ביוון - Tripadvisor | tripadvisor.co.il/Hotels-g189398-c3-zff22-Greece-Hotels.html |
| 7 | greecerealestate.co.il | ארכיון על הים - Gre - נדל"ן ביוון | greecerealestate.co.il/property-tags/על-הים/ |
| 8 | lefkada.co.il | Villa Adam - lefkada greece | lefkada.co.il/product/villa-adam/ |
| 9 | my-greece.co.il | השכרת וילה ביוון – המדריך המלא לנופש | my-greece.co.il/greece-holiday-villas/ |
| 10 | geoln.com | קנה וילה ביוון - וילות ביוון: מחיר, ביקורות, תמונות | geoln.com/he/property/villas/greece |

People Also Ask: none shown.

Related searches: וילה ביוון למכירה; וילות להשכרה ביוון על הים; וילות ביוון למשפחות; וילה ביוון על הים למכירה; וילות ביוון עם בריכה פרטית; חופשה בוילה ביוון; וילות יוקרה ביוון; וילות של ישראלים ביוון; טיסות ליוון.

AI Overview: YES. Cited domains: my-greece.co.il, mspirit.co.il, greece-islands.co.il, vacance.co.il, greecerealestate.co.il, instagram.com, booking.com, he.airbnb.com.

### "אמנת מס ישראל יוון" (volume 50/mo) - retrieved 2026-10-22 16:03:14 UTC

SERP features: ai_overview, organic, related_searches.

| # | Domain | Title (as shown) | URL |
|---|---|---|---|
| 1 | cpa.co.il | אמנה בין ישראל לבין ארה"ב | cpa.co.il/service/accounting-services/international-taxes/tax-treatie… |
| 2 | cpa.co.il | אמנה בין ישראל לבין יפן | cpa.co.il/service/accounting-services/international-taxes/tax-treatie… |
| 3 | cpa.co.il | אמנה בין ישראל לבין מלטה | cpa.co.il/service/accounting-services/international-taxes/tax-treatie… |
| 4 | bshcpa.co.il | אמנת המס ישראל הולנד: מניעת כפל מס בפעילות בינלאומית / בן שושן | bshcpa.co.il/אמנת-מס-ישראל-הולנד/ |
| 5 | gov.il | אמנה מדינת ישראל ממשלת בין הפורטוגלית לבין הרפובליקה בדבר ... | gov.il/BlobFolder/dynamiccollectorresultitem/portugal_dtpa/he/interna… |
| 6 | cpa.co.il | אמנה בין ישראל לבין איטליה | cpa.co.il/service/accounting-services/international-taxes/tax-treatie… |
| 7 | zscpa.co.il | אמנות מס - איך למנוע כפל מס | zscpa.co.il/אמנות-מס/ |
| 8 | cpa.co.il | שימוש באמנה למניעת כפל מס / מיסוי אמריקאי | cpa.co.il/service/us-taxation/preventing-double-taxation/ |
| 9 | tktax.co.il | אמנות למניעת כפל מס - המדריך למיסוי בינלאומי - טינה קפלן | tktax.co.il/post/tax-treaties/ |
| 10 | gov.il | אמנה בין מדינת ישראל לבין המדינות המכסיקניות המאוחדות ... | gov.il/BlobFolder/dynamiccollectorresultitem/mexico_dtpa/he/internati… |

People Also Ask: none shown.

Related searches: אמנת מס ישראל אירלנד; אמנת מס ישראל גרמניה; מדינות אמנת מס עם ישראל; אמנת מס ישראל דנמרק; אמנת מס ישראל אוסטרליה; אמנת מס ישראל הונגריה; אמנת מס ישראל רומניה; אמנת מס ישראל אנגליה.

AI Overview: YES. Cited domains: y-tax.co.il, itzikharel.com, new-greece.co.il, gov.il, oritax.co.il, cpa.co.il.

### "דירה ברודוס" (volume 90/mo) - retrieved 2026-10-22 16:03:22 UTC

SERP features: ai_overview, organic, people_also_ask, related_searches.

| # | Domain | Title (as shown) | URL |
|---|---|---|---|
| 1 | grei.co.il | השקעות נדל״ן ברודוס - דירות חדשות ויד שניה למכירה - GREI | grei.co.il/listings/greece/rhodes |
| 2 | he.airbnb.com | דירות נופש ברודוס | he.airbnb.com/rhodes-greece/stays/apartments |
| 3 | booking.com | דירות באזור רודוס | booking.com/apartments/region/gr/rhodes.he.html |
| 4 | tripadvisor.co.il | 10 הכי טובים: מלונות דירות ברודוס - Tripadvisor | tripadvisor.co.il/HotelsList-Rhodes-Apartment-Hotels-zfp13055282.html |
| 5 | agoda.com | מתכננים שהות ארוכה בדירות שירות? הזמינו רודוס ברודוס | agoda.com/he-il/theme/apartments/city/rhodes-gr.html |
| 6 | greecerealestate.co.il | ארכיון רודוס - Gre - נדל"ן ביוון | greecerealestate.co.il/location/רודוס/ |
| 7 | hotelscombined.co.il | אתרי לינה ונופש להשכרה בתוך רודוס (עיר) | hotelscombined.co.il/Place/Rhodes-vacation-rentals.htm |
| 8 | facebook.com | נכסים למכירה ביוון / Tel Aviv | facebook.com/hy2345/ |
| 9 | greecestate.co.il | בתים למכירה ברודוס - נדל"ן ביוון, קניית בית באיי יוון | greecestate.co.il/country/20 |
| 10 | rhodeshotel24.com | דילים במלונות של רודוס | rhodeshotel24.com/he/type/apartments-3/49/ |

People Also Ask: מהו מלון מומלץ ברודוס לזוגות?; איפה כדאי לישון ברודוס?; מהם מלונות 5 כוכבים הטובים ביותר ברודוס?; מהם הריזורטים המומלצים ביותר ברודוס?; מהם מלונות היוקרה הטובים ביותר ברודוס?; איזה מלונות ברודוס מציעים מגלשות מים?; מהם מלונות הכל כלול המומלצים ביותר ברודוס?; מהם מלונות 5 כוכבים מומלצים בכרתים?; האם יש מלונות הכל כלול עם פארק מים?.

Related searches: דירות ברודוס למכירה; וילות ברודוס למכירה; מלונות ברודוס; טיסות לרודוס; נדלן רודוס; בית חבד רודוס.

AI Overview: YES. Cited domains: booking.com, agoda.com, he.airbnb.com, tripadvisor.co.il, hotelscombined.co.il.

### "ויזת זהב" (volume 170/mo) - retrieved 2026-10-22 16:03:31 UTC

SERP features: ai_overview, organic.

| # | Domain | Title (as shown) | URL |
|---|---|---|---|
| 1 | yadidlaw.com | תוכניות גולדן ויזה באירופה: שינויים בתוכניות בשנת 2025 - דוד ידיד | yadidlaw.com/תוכניות-גולדן-ויזה-באירופה-2025 |
| 2 | euro-pass.co.il | ויזת זהב יוון - המדריך המשפטי להבטחת ההשקעה - עו"ד פינקו אלפסי | euro-pass.co.il/greece-golden-visa-legal-guide/ |
| 3 | israelhayom.co.il | המדינה שמתכננת להציע "ויזת זהב": תושבות לחמש שנים תמורת ... | israelhayom.co.il/travel/tourism-news/article/19081761 |
| 4 | nadlanexpert.co.il | הדרך הקלה לתושבות באירופה: גולדן ויזה יוון 2025/ החל מ-€250K | nadlanexpert.co.il/golden-visa-greece/ |
| 5 | horizonskyline.co.il | ויזת משקיע בדובאי: מדריך מקיף לקבלת ויזת זהב דרך השקעה בנדל"ן | horizonskyline.co.il/ויזת-משקיע-בדובאי-מדריך-מקיף-לקבלת-ויז/ |
| 6 | portugal-passport.co.il | ויזת זהב פורטוגל: מה זה ומה התנאים לקבלתה? - Portugal Passport | portugal-passport.co.il/ויזת-זהב-פורטוגל/ |
| 7 | lefkadaisrael.com | ויזת זהב Golden visa | lefkadaisrael.com/ויזת-זהב-golden-visa/ |
| 8 | polaris.ae | Golden Visa - ויזת הזהב של איחוד האמירויות | polaris.ae/he/migration/golden-visa/ |
| 9 | glidaiproperties.com | ויזת זהב בדובאי: מדריך מלא למשקיעים ישראלים / גלידאי נכסים | glidaiproperties.com/he/golden-visa |
| 10 | horizonskyline.co.il | קבלת ויזת זהב (Golden Visa) דרך השקעות נדל"ן בדובאי: המדריך המלא | horizonskyline.co.il/קבלת-ויזת-זהב-golden-visa-דרך-השקעות-נדלן-בדובא/ |

People Also Ask: none shown.

Related searches: none shown.

AI Overview: YES. Cited domains: hon.co.il, fibi.co.il, cal-online.co.il, supermarker.themarker.com, leumi.co.il, bankhapoalim.co.il, bizportal.co.il.

### "נדלן בכרתים" (volume 30/mo) - retrieved 2026-10-22 16:03:41 UTC

SERP features: ai_overview, organic, people_also_ask, related_searches.

| # | Domain | Title (as shown) | URL |
|---|---|---|---|
| 1 | he.airbnb.com | מקומות אירוח באזור כרתים | he.airbnb.com/crete-greece/stays |
| 2 | jus-tice.co.il | מחירי דירות ביוון 2026: כמה עולה דירה ביוון לפי אזור | jus-tice.co.il/greece-price-list/ |
| 3 | grece-crete.com | נדל"ן בכרתים / סוכן הנדל"ן שלך ביוון | grece-crete.com/page/51/?ref=ort |
| 4 | greecestate.co.il | בתים למכירה ביוון | greecestate.co.il/properties/proptype/2 |
| 5 | grece-crete.com | סוכן הנדל"ן שלך ביוון - נדל"ן בכרתים | grece-crete.com/page/2/ |
| 6 | greeces.co.il | קניית נדל"ן ביוון | greeces.co.il/ |
| 7 | greekim.co.il | Greekim - לוח נדל׳׳ן ביוון | greekim.co.il/ |
| 8 | green-acres.gr | נדל"ן למכירה יוון: 14838 נכסים בלעדיים | green-acres.gr/he |
| 9 | thisisgreece.co.il | השקעות נדל"ן ביוון - מידע, מדריכים, פרויקטים ונכסים (יוון למשקיע) | thisisgreece.co.il/ |
| 10 | grece-crete.com | נדל"ן בכרתים / סוכן הנדל"ן שלך ביוון | grece-crete.com/עמוד/75/?ref=ort |

People Also Ask: איפה אפשר למצוא בית נופש ביוון למכירה?; איפה אפשר למצוא בית להשכרה בכרתים?; איפה אפשר למצוא בתים להשכרה ביוון?; איפה אפשר למצוא בית ליד הים ביוון?; איזה אי ביוון הוא זול?; איפה אפשר למצוא בתים למכירה ביוון ליד הים?; איפה אפשר לקנות דירה ביוון כדי להשקיע?; האם יש בית באתונה למכירה?.

Related searches: בית ביוון על הים; בתים למכירה ביוון כרתים; דירות למכירה ביוון יד 2; דירות למכירה ביוון סלוניקי; נדלן ביוון; בתים למכירה בכרתים ליד הים; בית ביוון מחיר; דירות ביוון להשקעה.

AI Overview: YES. Cited domains: nadlanmaster.co.il, grei.co.il, green-acres.gr, greecestate.co.il.

---

## 4. Competitor DNA: the 6 strongest Hebrew pages (each read in full)

Selection: the pages that rank or are AIO-cited across the most main keywords, counting only pages with real content. Homepages and listing pages are covered in 4.7. The raw metrics and the full H2/H3 outlines are in the appendix. Density = occurrences of the main keyword phrase ÷ main-content words, counted on the raw HTML.

### 4.1 nadlanmaster.co.il/נדלן-ביוון/ (the market's reference guide; AIO-cited on 6 SERPs; #2 "השקעה ביוון")

- Title: "השקעות נדל"ן ביוון - מדריך למשקיע, נכסים למכירה (מעודכן 2026)". H1: **"נדל"ן ביוון"**, a bare exact match. No breadcrumb (only "מאת: מערכת נדלן מאסטר"). Meta description: "נדל"ן ביוון - מידע מקיף..." ending with ">>".
- 4,368 words; 273 numeric tokens; 19 H2s.
- Outline: key facts → economic history 2008-2017 → project cards (15) → price-trend graphs → taxes and yields → where to invest (Athens / Thessaloniki / Lefkada / islands) with a city table → prices by property type → links to sub-guides → yearly price change 2018-2025 → bureaucratic purchase steps and costs → advantages → mortgage → resale vs new → Airbnb rules → video → projects → FAQ → map → sources.
- Opening (paraphrase): before the numbers it gives a soft intro to Greece as a dream holiday country, then turns to the crisis-hit economy as the investor's opportunity, and promises answers, data and a forecast.
- 5 tables: key-facts table (13 rows), two city comparison tables (population, €/m², rent, gross yield), price by property type with rents, and yearly % change.
- Tools: none (no calculator).
- Media: 65 images (alts carry the keyword 9 times), YouTube embed, Google Maps embed, tradingeconomics graphs.
- FAQ: 11 questions with FAQPage schema.
- Schema: WebPage, FAQPage, Organization (no Article, no Person).
- 100 internal links in content (371 on the page); 5 external (bankofgreece, globalpropertyguide, tradingeconomics, kpmg, wikipedia).
- CTA: lead form with a "target destination" dropdown (Lefkada / Athens / Crete / Thessaloniki), a phone number and 2 WhatsApp links.
- Dates: published 2016-12-01, modified 2026-07-07. "מעודכן 2026" sits in the title.
- Author: "מערכת" byline and an author box with no person.
- Tone: conversational marketing, ✔️ and ◄ bullets, "בואו נצא לדרך", heavy variant stuffing ("השקעות נדלן ביוון" / "נדלן יווני").
- Keyword "נדל"ן ביוון": 33× = **0.76%**. Placement: title, H1, 3× in the first 100 words, 6 of 19 H2s, 9 image alts.
- **Gets wrong or leaves out:**
  - The key-facts row says an Israeli resident pays tax "only in Greece". Its own tax paragraph says the opposite (credit plus a duty to report in Israel).
  - The table says capital-gains tax is 15% while the body says it is suspended.
  - "מס שבח through a company = 15% of the price": the tax is on the gain, not the price.
  - It promises "עליית ערך כמעט ודאית".
  - €/m² appears as 2,389, 2,400 and "2,000 to 2,500" in different places.
  - Ancillary costs are quoted as "2 to 6%" while its own list adds up to more.
  - A golden-visa project card is headlined "250 אלף אירו בלבד" (the conversion track) with no 120 m², single-property or STR-ban explanation.
  - It has nothing on the Israeli 15% track, Israeli capital-gains tax on sale, reporting, or ₪ figures.
  - The page has a commercial bias: 15 marketed projects sit inside the guide.

### 4.2 nadlanmaster.co.il/נדלן-באתונה/ (#2 "נדל"ן ביוון", ranks on 4 SERPs)

- Title: "השקעות נדל"ן באתונה ב-2026 - מדריך למשקיע (ודירות להשקעה)". H1: "השקעות נדל"ן באתונה". No breadcrumb.
- 3,478 words; 126 numeric tokens; 17 H2s.
- Outline: what to know → advantages → market data → subprime analogy → why now → properties → yield → taxes → neighbourhoods → prices → 5-year % table → 15-year graph → purchase steps → where to start → form → map.
- Opening (paraphrase): a growing trend of Israelis buying in Athens, pushed by Israeli conditions (high tax on investment flats, high prices, low yields); Athens prices are framed as not yet back at the 2008 peak.
- Tables: market-data (11 rows, including the 2026 rental scale 15/25/35/45 and €3,252/m²) and yearly % change.
- FAQ: 7 questions with FAQPage. Media: 44 images and a map.
- Dates: published 2017-12-06, modified 2026-09-10.
- Keyword "נדל"ן באתונה": 32× = 0.92%; in title, H1, first 100 words (4×) and 8 of 17 H2s.
- **Gets wrong or leaves out:**
  - "Israelis pay only in Greece, no extra tax in Israel".
  - "Full exemption from מס שבח", presented as permanent (it is a suspension to 31.12.2026).
  - Mixes capital-gains and rental-income tax ("average 15%").
  - Pitches Airbnb potential with **no mention of the districts 1 to 3 registration freeze**.
  - Yield is "5 to 10%" in the text and "5 to 8%" in the table.
  - No neighbourhood €/m² table (beta-estate has one).

### 4.3 thisisgreece.co.il/houses-for-sale-in-greece/ (#6 "דירה ביוון", #4 "קניית דירה ביוון")

- Title: "בתים למכירה ביוון - איך קונים בית ביוון? (מדריך, דירות ונכסים)". H1: "בתים למכירה ביוון". Breadcrumb: דף הבית › מדריכים › בתים למכירה ביוון (BreadcrumbList).
- 1,965 words; 56 numeric tokens; 7 H2s: houses guide → listings → is it worth it → how much → steps → ancillary costs → projects.
- Opening (paraphrase): addresses the reader thinking of buying a house in Greece ("you are not alone"), then lifestyle and relocation framing with expat communities.
- Tables: a facts table (population, tourism, average house ~€300K, yield 5 to 10%) and a price-by-type table. Several cells are empty: Crete flat, Lefkada house, Thessaloniki houses.
- Tools: none. Media: 36 images (project cards). FAQ: none.
- Schema: WebPage, BreadcrumbList.
- Dates: published 2024-08-12, modified **2025-08-31** (stale). No author.
- CTA: inline form plus a side form.
- Keyword "בתים למכירה ביוון": 4× = **0.20%**. It ranks on title, H1 and site topicality, not on density.
- **Gets wrong:**
  - Golden visa "500 to 800 thousand" (wrong tiers; misses €400K and the €250K track).
  - Capital-gains tax "15% if sold within ~5 years" (wrong: suspended for individuals).
  - Rental income tax "9% to 44%" (old general scale).
  - Notary "~3%" (out of line with other sources' 1 to 2% for lawyer plus notary; verify).
  - Says the transfer tax is paid by the seller (AADE: the buyer pays before signing).
  - ENFIA "0.1 to 0.5%".
  - No Israeli tax side beyond "the treaty removes double tax"; no sources.

### 4.4 beta-estate.com/real-estate-prices-athens/ (#6 "נדל"ן ביוון", AIO-cited for "דירה באתונה"): the best data page

- Title: "מחירי דירות באתונה: סקירה 2026 | כמה עולה דירה באתונה? ביתא נדל״ן". H1: "מחירי דירות באתונה: סקירה 2026". Breadcrumb: דף הבית » הבלוג שלנו » ... (BreadcrumbList).
- 2,984 words; **166 numeric tokens**; 29 H2/H3s.
- Outline: key takeaways → yearly price table 2018-2026 → average price → factors → prices by neighbourhood → challenges Greece vs Israel → trends → considerations → tips → summary → 11 FAQ → sources → about → author.
- Opening (paraphrase): Athens prices rising moderately to fast after the 2009-2018 crisis; the stated goal is transparency, followed by a company introduction (founded 2018).
- Tables:
  - yearly €/m² and % change;
  - **15 neighbourhoods** with €/m², y/y %, rent €/m² and a character note (Ilisia, Kolonaki-Lykavittos, Exarchia, Kypseli, Patisia, Gerakas, Marousi, Glyfada, Palaio Psychiko, Vouliagmeni, Neo Faliro, Sounio, Kifisia, Petralona, Neos Kosmos);
  - a 10-row "challenges Greece vs Israel" table.
- Media: a neighbourhood map image and an infographic iframe. 6 of 8 images have no alt.
- FAQ: 11 Q&A visible, **no FAQPage schema**.
- Schema: Article, BreadcrumbList, Person.
- Sources list: Bank of Greece Q3-2025, Spitogatos Q3-2025, Indomio, GPG, ELSTAT.
- **E-E-A-T:** a visible author box (co-founder, lives in Athens, short bio). It is the only one of the six with a named person.
- CTA: forms, WhatsApp and a webinar sign-up (a live tour of a new Athens property, 18.08.2026).
- Dates: published 2024-06-18, modified 2026-02-05.
- Keyword "מחירי דירות באתונה": 11× = 0.37%; in title, H1, first 100 words (3×) and 4 H2s.
- **Gets wrong:**
  - The average is €3,168/m² in the body and €3,268 in the FAQ.
  - 2022 shows "+45.2%" (€1,400 → €2,033), which looks like a series break and does not match the Bank of Greece index pace. palmo-group shows the **identical table**.
  - The golden visa is "€500,000 in central Athens" in one paragraph and "€800,000 (2026 update)" in another.
  - Metro line 4 "opens 2026" (unverified; check the Attiko Metro timetable).
  - "~40% of Athens deals are by foreigners" has no source.
  - No yield math (gross → net), no purchase-cost table, no Israeli tax.

### 4.5 palmo-group.com/buying-a-real-estate-in-greece/ (#5 "דירה באתונה", AIO-cited for "דירה ביוון"; palmo is #1 for "השקעה ביוון" with its homepage)

- Title: "קניית בית ביוון – דירות להשקעה ביוון | פאלמו – מצוינות בהשקעות נדל"ן". H1: "המדריך לקניית בית ביוון". Breadcrumb: דף הבית » קניית בית ביוון.
- 3,155 words; 133 numeric tokens; 19 H2s.
- Outline: why buy → Athens 2018-2024 price table → 2008-2024 index table → step by step (8 steps) → neighbourhood €/m² table → city/island €/m² table → location → transfer tax → STR vs long-term → buying via an investment house (pros and cons) → management company → project cards → FAQ.
- Opening (paraphrase): almost every Israeli has dreamt of a home in Greece, an Athens flat or an island house 1.5 hours away; the dream is achievable and the process is not that complicated.
- Tables: 7, including 13 Athens neighbourhoods (Kolonaki from €5,800, Plaka €5,500, Glyfada €3,200 to 3,600, Piraeus €1,500 to 2,000...) and Athens / Thessaloniki / Santorini / Mykonos €/m².
- Tools: none. Media: 24 images (6 with no alt) and a Trading Economics HPI graph (2006-2020).
- FAQ: 5 questions with FAQPage. Schema: WebPage, BreadcrumbList, FAQPage.
- Dates: published 2023-10-05, modified 2026-06-25. **No author.**
- Tone: playful and emotional ("יאסו, מתחילים!", plate-smashing jokes, a "security certificate" flat abroad given Israel's situation).
- CTA: a form and 2 WhatsApp links.
- Keyword "קניית/לקנות בית ביוון": 10× = 0.32%; in title, H1 and the first 100 words.
- **Gets wrong:**
  - Golden visa "250 אלף יורו ומעלה", and claims holders can "live in any Schengen country" (they get Greek residence; Schengen gives 90/180-day travel only).
  - Says the treaty "frees you from Israeli purchase tax, betterment tax and property tax". Those Israeli taxes never apply to Greek property, and the treaty does not remove Israeli income-tax reporting.
  - "Betterment-tax exemption for owners of up to 3 apartments" has no source. This is the likely origin of the AIO line "0% מס שבח עד 3 דירות".
  - STR yield "8 to 12%" with no mention of the Athens freeze.
  - Athens table is "as of 2024" and identical to beta's.
  - Useful detail it does have: the transfer tax is computed on the **objective value** if that is higher, and a document list (passport, Israeli population-registry extract, Greek bank account, AFM).

### 4.6 gogreece.co.il/the-investment-process/ (#6 "השקעה ביוון", AIO-cited on 2 SERPs; the gogreece domain is the most AIO-cited at 7 SERPs, mainly its /properties/ listing page)

- Title: "תהליך קניית בית ביוון – מדריך ב-7 שלבים מפורטים | Go Greece IL". H1: "תהליך קניית בית ביוון – 7 שלבים להשקעה מנצחת". Breadcrumb (HTML only): Go Greece IL » מאמרים » השקעות ביוון.
- 2,464 words; 84 numeric tokens; 16 H2/H3s: why → step 1 advice/documents → step 2 bank account → step 3 find the property (furnishing, heating, parking tips) → step 4 price → step 5 preliminary agreement and deposit → step 6 financing → step 7 signing → after the purchase → FAQ.
- Opening (paraphrase): assumes the reader already chose real estate as the next investment, then places Greece among Europe's affordable, high-demand markets.
- Tables: price index 2008-2020 (nominal / real), Athens median €/m² (€1,922 centre / €2,000 outside) and a rate table labelled "mortgage property tax" (it looks like ENFIA supplementary rates).
- FAQ: 4 questions with FAQPage (its only schema type). 22 images, all with alt. 4 forms, 4 WhatsApp links.
- Dates: published 2023-01-28, modified 2026-09-24, but the **data is 2019-2020** ("fake freshness"). No author.
- Keyword "קניית בית ביוון": 15× = 0.61%; in 9 of 16 headings.
- **Gets wrong:**
  - Golden visa "above €250,000".
  - Treaty: "no need to pay tax to Israeli income tax".
  - Garbled claim that foreigners may not own property unless they pay Greek taxes.
  - Mortgage "must be repaid by age 58" (verify), with the rate range 3.5 to 7.5%.
  - Mislabelled ENFIA table.
  - Distinctive and worth matching: **Greece-specific tenant tips** (Greek long-term tenants often prefer unfurnished flats; heating with a meter; parking) and a **seller-documents checklist** (no-debt certificates, tax clearance, ENFIA, utilities).

### 4.7 Other ranking pages (short DNA)

- **blog.yad2.co.il/נדלן-ביוון/** (#5 "נדל"ן ביוון", #11 "השקעות נדלן ביוון"): 534 words, no H2s in the body. The title tag is broken ("נדל"ן ביוון -") and the meta description is generic. It says the golden visa is "usually around €250,000" and citizenship comes after 7 years. **It ranks on domain authority alone**, which proves the bar for content is low.
- **shovalyazamoot.com/projects** (#1 "נדל"ן ביוון", #2 "השקעות נדלן ביוון"): a developer's project listing (Thessaloniki, Nikiti/Halkidiki). 321 words, H1 "דירות להשקעה ביוון", 12 H3 cards all starting "דירה להשקעה ביוון, ...". No schema, no meta description, 27 of 43 images without alt. Exact-match headings plus brand signals.
- **new-greece.co.il/buying-an-apartment-in-greece/** (#4 "דירה ביוון"): 428 words, written in 2018 and never updated. Its sister page /apartments-for-sale-in-athens/ (2,732 words) is **#1 for "דירה באתונה"** and #2 for "בתים למכירה ביוון".
- **maariv.co.il/business/realestate/article-1093013** (#1 "השקעות נדלן ביוון"): a developer advertorial, 518 words, "8 steps". It says the golden visa is "250/500K, about to rise" and "taxed only in Greece". News-domain authority.
- **Golden-visa SERP leaders:**
  - yamasre.com: a 250K Thessaloniki presale landing page, 374 words.
  - yadidlaw.com: 427 words plus VideoObject.
  - greekpropertygroup.com.
  - eurobank.gr: a **Hebrew golden-visa PDF brochure from a Greek bank**, which shows the bank is courting Israelis.
  - migration.gov.gr: the official English page lists documents only and still shows the €250,000 wording. It does not show the 2024 tiers, so cite the law text.
  - nadlanmaster GV page: 1,511 words, GV phrase density **3.1%**, tiers 400/800 but limited to "Athens, Thessaloniki, Santorini, Mykonos" (misses all of Attica and islands over 3,100 residents), no FAQ schema.
  - euro-pass.co.il (#2 "ויזת זהב"): 3,271 words with the richest schema seen (Article + FAQPage + HowTo + LegalService + Speakable). Published 21.8.2026, modified **21.10.2026**, written from a lawyer's angle.
- **Tax:** y-tax.co.il treaty page (AIO-cited): 1,941 words, links aade.gr, mfa.gr and gov.il, modified 18.10.2026. The rest of the "אמנת מס ישראל יוון" SERP is generic treaty pages for other countries (cpa.co.il USA/Japan/Malta/Italy). **There is no strong Greece-specific Israeli-tax page in the top 10**, so a correct one can take the slot.

---

## 5. Synthesis: the DNA of a winning page here

### 5.1 What the ranking pages share

- **Length:** the content-ranking guides run 1,965 to 4,368 words (median about 3,000). Thin pages (321 to 534 words) rank only on brand or domain authority (yad2, Maariv, the shoval listing, new-greece).
- **Title:** the exact keyword first, then "2026" and/or "מדריך" / "(מעודכן 2026)" / a question ("כמה עולה...?") / a count ("ב-7 שלבים"). The brand goes last.
- **H1:** short exact match ("נדל"ן ביוון", "בתים למכירה ביוון", "השקעות נדל"ן באתונה", "גולדן ויזה – יוון"), or keyword + ": סקירה 2026".
- **Breadcrumb:** Home › guides/blog › page, with BreadcrumbList on 4 of 6. nadlanmaster has none.
- **Sections present on most of the six:**

| Section | Present on |
|---|---|
| Why Greece | 6/6 |
| Purchase steps | 6/6 |
| Taxes | 6/6 |
| Golden visa | 6/6 |
| Areas | 6/6 |
| Lead form | 6/6 |
| Price tables | 5/6 |
| Ancillary costs | 5/6 |
| FAQ | 5/6 (4 with schema) |
| WhatsApp | 5/6 |
| STR vs long-term | 4/6 |
| Mortgage | 4/6 |
| Project cards | 4/6 |
| New vs resale | 2/6 |

- **Questions every page answers:**
  - כמה עולה דירה ביוון / באתונה (€/m², a 50 to 70 m² example)?
  - איפה כדאי להשקיע?
  - מה התשואה (5 to 10% claims)?
  - כמה מס רכישה (3.09%)?
  - כמה עולה גולדן ויזה?
  - אפשר לקנות מרחוק (power of attorney)?
  - מה זה AFM?
  - יש אמנת מס?
  - משכנתא לזרים?
  - כמה זמן לוקח (1 to 2 months)?
  - יד 2 או חדש?
  - Airbnb או טווח ארוך?
- **Vocabulary searchers and competitors use (put these in headings, alts and FAQ):**
  - **Core terms:** נדל"ן ביוון / נדלן ביוון (both spellings), השקעות נדל"ן ביוון, דירה להשקעה, דירות למכירה, יד 2, מקבלן / על הנייר.
  - **Residency:** גולדן ויזה / ויזת זהב / Golden Visa, תושבות (not אזרחות).
  - **Taxes:** מס רכישה / מס העברה (3.09%), ENFIA / מס רכוש שנתי, מע"מ 24% (מוקפא), מס רווחי הון (מוקפא), אמנה למניעת כפל מס, זיכוי מס זר.
  - **Process and registration:** AFM / מספר מס יווני, TAXIS, נוטריון, טאבו / רישום מקרקעין / Ktimatologio (קטימטולוגיו), ייפוי כוח, אפוסטיל, מקדמה, שווי אובייקטיבי.
  - **Returns and rentals:** תשואה ברוטו / נטו, השכרה לטווח קצר / Airbnb / AMA.
  - **Places:** Athens neighbourhoods: קוקאקי, פגרטי, קיפסלי, קולונאקי, אקסרכיה, פטיסיה, ניאוס קוסמוס, פריסטרי, ספוליה, גליפדה, פיראוס. **סלוניקי** (Israelis do not write תסלוניקי), לוטראקי, לפקדה, חלקידיקי (ניקיטי), כרתים (חאניה, הרקליון, רתימנו).
  - **Recurring phrases:** "שעה וחצי טיסה", "המשקיע הישראלי", "המחירים עוד לא חזרו לשיא של 2008", "יאסו".

### 5.2 How we beat them (the concrete list)

1. **Be right, and show the date.** Each page gets a short "נכון ל-[month 2026]" fact box: the rule, one plain source stamp (for example "בנק יוון, רבעון 2/2026" or "חוק 5100/2024"), and the last-checked date. The owner's research law keeps full citations in the repo, so there is no citation clutter on the page. Every competitor is wrong on at least 2 of these 6:
   - the golden visa tiers;
   - who pays transfer tax;
   - the capital-gains suspension;
   - the VAT suspension;
   - the 2026 rental-tax scale;
   - the Athens STR freeze.
2. **The Israeli side, done properly (nobody does this):**
   - worldwide income taxation;
   - the two Israeli tracks for foreign rent: regular with foreign-tax credit, or the 15% track with no credit and no expenses except depreciation;
   - Israeli capital-gains tax on a later sale, with foreign-tax credit;
   - annual reporting and הצהרת הון;
   - which Greek payments are not creditable (ENFIA, transfer tax, municipal fees);
   - whether a Greek flat affects Israeli "דירה יחידה" status (verify before publishing; section 7);
   - inheritance: Greek inheritance tax applies, Israel has none;
   - FX: buying in € with ₪ money.
3. **Tools: none of the 20+ pages read has one.**
   - (a) **Total cost-to-buy calculator**: price, objective value, new or resale, lawyer, notary, agent, AFM/POA → € and ₪ totals.
   - (b) **Net-yield calculator** for Greece: rent, vacancy, management 8 to 25%, ENFIA, building fees, insurance, 2026 Greek bracket, Israeli track → net € and %. Reuse `/investment-property-cashflow-calculator/` logic.
   - (c) **Golden-visa eligibility checker**: area tier, property type, m², price, single property, intended STR use → eligible or not, and why.
   - (d) **Athens neighbourhood map** with €/m² and rent €/m² stamped by quarter, linking the Koukaki and Glyfada sample projects.
4. **Fresh, quarter-stamped data** instead of copied tables. Use the Bank of Greece residential price index by area (Athens / Thessaloniki / other cities / rest), Spitogatos or Indomio asking prices, and ELSTAT. Do not reuse the "+45.2% in 2022" table that beta and palmo share.
5. **Greek due diligence nobody covers.** These are must-have sections for the seaside and Crete pages (verify each):
   - Ktimatologio (cadastre) status and the ΚΑΕΚ number;
   - illegal-build legalisation and the engineer's certificate;
   - the energy certificate (ΠΕΑ);
   - forest maps for rural or island plots;
   - the coastal-zone rule (αιγιαλός / παραλία);
   - building outside the town plan (εκτός σχεδίου);
   - seismic code (pre-1985 buildings);
   - the seller's tax and ENFIA clearance.
6. **Independence as the hook.** Every competitor in the top 10 sells its own projects. Searchers also check those sellers: "פאלמו תביעות", "ביתא נדלן חוות דעת", "חברת פאלמו חוות דעת" appear as related searches. Add a "how to check a Greek developer or Israeli broker before you sign" checklist. Never name names on negative topics (owner rule).
7. **Structure and schema:**
   - Follow the Intent-first order on every width: H1 → answer paragraph → CTAs → stage (map / 3D / tool) → facts table → article.
   - Exactly one H1 (fix the logo H1 on /global/).
   - Schema: BreadcrumbList, Article with a named Person author and a lawyer/CPA reviewer, FAQPage on the visible FAQ; HowTo on the acquisition page.
   - Answer-first paragraphs of 40 to 60 words for AIO extraction.
   - Use both spellings of נדל"ן naturally.
   - Target density of 0.5 to 1%. Above 3% (nadlanmaster GV) is spammy.
8. **Hebrew in the site's marketing voice** (language-dna skill): real-estate marketing language, not tech talk. Keep the soft-dream openings short; the winner opens with the answer.

### 5.3 Title / H1 / breadcrumb patterns to use

- Title: `[exact keyword] 2026: [2 to 3 concrete payoffs]`, ≤ 60 characters before " | נדלן".
- H1: the keyword plus a decision promise, worded differently from the title.
- Breadcrumb: 1 to 2 words, different from both (נדלן › השקעות בחו"ל › יוון › אתונה).

---

## 6. Proposed page set: hub + 7 children

**Slug rules applied** (checked against the 4,579 URLs in `sitemap-urls.txt`):
- English words only; no word twice in one URL;
- the first word of each new slug is a word **no** existing URL starts with: athens, acquisition, golden, taxation, seaside, crete and thessaloniki each start 0 existing URLs. For comparison, buying (5), purchase (1), mortgage (13), property (5) and investment (34) are already owned and were avoided;
- `global` and `greece` are the existing section and hub segments, so children do not repeat them.

**Technical check needed:** confirm the /global/greece/ template accepts child pages. If it does not, use the flat fallback slugs in the table; their head words are also unowned.

| Page | Intent it owns (one each) | Owned keywords and synonyms (vol/mo) | Proposed H1 | SEO title (≤60) | Breadcrumb | Slug |
|---|---|---|---|---|---|---|
| **HUB** (exists) | Invest in Greek real estate: whether, where and how much, plus the map to every child | נדל"ן ביוון / נדלן ביוון 210; greece real estate 110; השקעה ביוון / השקעות ביוון 70; השקעות נדל"ן ביוון 70; דירה/דירות להשקעה ביוון 70; נכס/נכסים ביוון 40; נדל"ן יוון 30; דירות ביוון להשקעה 30; פרויקטים ביוון 20; יוון או קפריסין 20 (comparison section). **~700** | נדל"ן ביוון למשקיע הישראלי: איפה, כמה ובאיזה מסלול | נדל"ן ביוון 2026: השקעה, מחירים ותשואות לישראלים (48) | יוון (existing) | `/global/greece/` (keep) |
| **ATH** | Buy or invest in an apartment in Athens: neighbourhoods and €/m² | דירה/דירות באתונה 170; דירות/דירה למכירה באתונה 90; נדל"ן באתונה 50; דירות באתונה למכירה 40; קוקאקי 40; קיפסלי 30; השקעות נדלן באתונה 30; השקעה באתונה 20; מחירי דירות באתונה 20; כמה עולה דירה באתונה 20; דירות להשקעה באתונה 20 (+ גליפדה 480 travel-mixed, as a section). **~740** | דירה באתונה: שכונה אחרי שכונה, מחיר למ"ר ומה בודקים לפני שקונים | דירות למכירה באתונה 2026: מחיר למ"ר לפי שכונה (45) | אתונה | `/global/greece/athens-apartments/` (flat: `/athens-apartments/`) |
| **ACQ** | How to buy an apartment or house in Greece: steps, documents, total costs, financing | דירה/דירות ביוון 140; דירות/דירה למכירה ביוון 90; דירה ביוון למכירה 70; קניית בית ביוון 50; קניית דירה ביוון 30; לקנות בית ביוון 20; רכישת דירה ביוון 20; משכנתא ביוון 20; פתיחת חשבון בנק ביוון 20; בתים לקניה ביוון 20; מס רכישה ביוון 10; עורך דין יווני 10. **~620** | קניית דירה ביוון: התהליך המלא, המסמכים וכל העלויות עד המפתח | קניית דירה ביוון: השלבים, העלויות ומס הרכישה (44) | תהליך הרכישה | `/global/greece/acquisition-process/` (flat: `/acquisition-greece/`) |
| **SEA** | A house or villa by the sea or on an island: where, how much, coastal checks | בתים למכירה ביוון ליד הים 170; בתים למכירה ביוון 140; בתים ביוון 90; בית ביוון 70; וילה למכירה ביוון 30; בתים למכירה באוויה 30; בית למכירה ביוון 20; בתים למכירה ביוון על הים 20; בתים למכירה בקורפו 20; Rhodes / Lefkada / Paros / Mykonos / Santorini / Lesbos "בתים למכירה ב..." 10 each (+ וילה/וילות ביוון 260 and דירה ברודוס 90 as secondary). **~920** | בית על הים ביוון: איפה קונים, כמה זה עולה ומה חייבים לבדוק | בתים למכירה ביוון ליד הים: מחירים לפי אי ואזור (46) | בתים על הים | `/global/greece/seaside-houses/` (flat: `/seaside-houses-greece/`) |
| **GV** | Greek golden visa through property: tiers, conditions, family, what it does not give | golden visa greece 110; גולדן ויזה יוון 90; ויזת/ויזה זהב יוון 70; גולדן ויזה 40; ויזת זהב ביוון 20; תושבות ביוון 20; גולדן ויזה ביוון 10; תושבות קבע ביוון 10; גולדן ויזה יוון 2026 10 (+ ויזת זהב 170, credit-card mixed). **~370** | גולדן ויזה ביוון: 800, 400 או 250 אלף אירו, ומה המשפחה מקבלת בפועל | גולדן ויזה יוון 2026: סכומי ההשקעה והתנאים החדשים (49) | ויזת זהב | `/global/greece/golden-visa/` (flat: `/golden-visa-greece/`) |
| **THE** | Thessaloniki apartments and Halkidiki holiday homes (north Greece) | דירה/דירות בסלוניקי 40; דירות למכירה בסלוניקי 20; דירות למכירה ביוון סלוניקי 20; נדלן בסלוניקי 20; בתים למכירה בחלקידיקי 20; נדלן סלוניקי 10; השקעות נדלן בסלוניקי 10; השקעה בסלוניקי 10; בתים למכירה בסלוניקי 10; רכישת דירה בסלוניקי 10; related: פרויקטים בסלוניקי, דירות חדשות בסלוניקי. **~170** | דירה בסלוניקי ובית בחלקידיקי: עיר סטודנטים, חופי הצפון ומחירי 2026 | דירות למכירה בסלוניקי וחלקידיקי: מחירים ותשואות (47) | סלוניקי וחלקידיקי | `/global/greece/thessaloniki-halkidiki/` (flat: `/thessaloniki-halkidiki/`) |
| **TAX** | Tax on a Greek property for an Israeli: Greek taxes plus the Israeli side | אמנת מס ישראל יוון 50; מיסוי ביוון 30; ENFIA 20; מס הכנסה ביוון 10; מס שבח יוון 10; מס ירושה ביוון 10; מיסוי נדלן יוון 10; plus no-volume long tail (מס על דירה בחו"ל, דיווח על דירה בחו"ל, מס שכירות בחו"ל). **~130** | מיסוי דירה ביוון לישראלים: מה משלמים ביוון ומה מדווחים בישראל | מס על דירה ביוון: ENFIA, שכירות ואמנת המס עם ישראל (50) | מיסים | `/global/greece/taxation/` (flat: `/taxation-greece-israel/`) |
| **CRE** | Buy property in Crete (Chania, Heraklion, Rethymno), including renovation houses | נדלן בכרתים 30; דירה/דירות בכרתים 30; בתים לשיפוץ בכרתים 20; בית בכרתים 10; נדלן כרתים 10; דירות למכירה בכרתים 10; וילות למכירה בכרתים 10 (+ וילה בכרתים 210 holiday-mixed, secondary). **~150** | נדל"ן בכרתים: חאניה, הרקליון ורתימנו, מחירים ובתים לשיפוץ | בית בכרתים למכירה: מחירים בחאניה ובהרקליון (42) | כרתים | `/global/greece/crete/` (flat: `/crete-property/`) |

Priority by owned clean volume, commercial value and how weak the SERP is: ATH → ACQ → GV → SEA → THE → TAX → CRE.
- TAX is low-volume, but it is where every competitor is wrong, and its AIO slot is winnable.
- SEA and CRE are seasonal; publish them by March 2027.
- Pace the releases, for example 1 to 2 pages per week. The owner's law forbids mass same-day changes; pace needs his OK.

### 6.1 What each page must contain that the others do not (no overlap)

- **HUB:** the 60-second answer (is Greece for me?); a regions map with a one-line verdict per region linking each child; a national price snapshot by region (Bank of Greece index plus a €/m² band); yields gross vs net (summary, linking the calculator); golden visa in 3 lines (link GV); taxes in 3 lines (link TAX); risks; Greece vs Cyprus vs Portugal comparison table; sample projects; "how to check a developer"; FAQ. **Prices stay here** (see 6.3).
- **ATH:** a 15+ neighbourhood table (€/m², rent €/m², y/y, tenant profile, STR-freeze district yes/no); the Athens STR freeze explained with a link to the STR page; metro and Ellinikon effects (verified); Piraeus / Glyfada / southern coast; the Koukaki and Glyfada sample projects; budget examples (€100K / €200K / €300K → what you get).
- **ACQ:** a HowTo of 8 to 9 steps (AFM → bank → search → due diligence → preliminary agreement and deposit → contract at the notary → transfer tax before signing → cadastre registration → utilities, ENFIA and management); a **total-cost calculator**; documents list (Israeli side: population-registry extract, apostille, translations); power of attorney and buying remotely; mortgage for non-residents (LTV, rates, documents; answers the PAA "האם ישראלים יכולים לקבל משכנתא ביוון?"); new vs resale; VAT suspension; the seller's documents checklist.
- **SEA:** islands and coasts matrix (Crete → link CRE; Halkidiki → link THE; Rhodes, Corfu, Lefkada, Evia, Peloponnese, Cyclades) with price bands and seasonality; coastal-zone, forest-map, out-of-plan and illegal-build checks; access (ferries, flights from Israel); winter occupancy reality; the honest villa section ("villa for sale" vs holiday rental).
- **GV:** the 2024 tiers (€800K in Attica, Thessaloniki, Mykonos, Santorini and islands over 3,100 residents; €400K elsewhere; €250K only for conversions and listed buildings), the 120 m² single-property rule, the STR ban and fines, family members, 5-year renewal, no work right, not citizenship (citizenship needs 7 years of real residence and language), the processing route, an **eligibility checker**; GV vs Cyprus / Portugal / Malta comparison (the related searches ask for these); a "דרכון יווני" disambiguation FAQ.
- **TAX:** Greek side (3.09% transfer tax on price or objective value, ENFIA, the 2026 rental scale, the STR VAT rules summary with a link to the STR page, capital gains suspended to 31.12.2026, inheritance and gift tax) plus the Israeli side (section 5.2, point 2), with a worked example in ₪. This is the "treaty" page, so it must answer "אמנת מס ישראל יוון" in the first paragraph.
- **THE:** Thessaloniki districts and the student market; Israeli developers' focus area (neutral, no names); the €250K conversion projects and how to verify eligibility; Halkidiki peninsulas (Kassandra / Sithonia / Nikiti) with seasonality.
- **CRE:** Chania / Heraklion / Rethymno / Agios Nikolaos price bands; renovation houses (stone houses, village plots, permits); the airports (HER/CHQ) and the Israeli flight season; the honest seasonal-yield picture.

### 6.2 STR boundary and internal links

- The STR page keeps: STR definition, AMA registration, safety rules, the Athens freeze detail, STR VAT, the climate fee, STR yields. New pages **summarise in one or two lines and link** to it ("השכרה לטווח קצר ביוון"). The STR page gets "parent" links to the hub and to ACQ, TAX and ATH, and its purchase, tax and price sections shrink to summaries plus links (to avoid cannibalisation). Fix its defects (section 8).
- The hub links to all 7 children in the first screen (region map) and again in the body. Each child links up to the hub (breadcrumb plus a contextual link) and to at most 2 or 3 siblings:
  - ATH ↔ ACQ, TAX
  - SEA ↔ CRE, THE
  - GV ↔ ATH, THE
  - TAX ↔ ACQ
  - all ↔ STR where relevant.
- Sample projects link to ATH (neighbourhood) and GV (only when the tier fits; most €295K Athens units do **not** qualify on their own under the €800K Attica tier, so the page must say so honestly).

### 6.3 Owner decisions needed (cross-site)

1. **Prices**: jus-tice.co.il/greece-price-list/ ranks 3 to 5 for "כמה עולה דירה ביוון" and "מחירי דירות ביוון" (570 + 315 + 260 impressions/3 months).
   - Recommendation: **do not create a separate nad-lan price page now**. The hub carries a compact price snapshot.
   - The owner decides whether prices should live long-term on nad-lan (real-estate portal) or stay on jus-tice.
2. **Buying and investing in Greece**: jus-tice's /buying-property-in-greece/ (positions 31 to 37) and /investing-in-greece-real-estate/ (positions 42 to 58) target the same intents as ACQ and HUB.
   - Recommendation: nad-lan owns market, buying and investing; jus-tice owns the legal angle ("עורך דין ביוון", due-diligence law, contracts).
   - This means re-targeting content on jus-tice's side if the owner agrees. It is not a URL change.

---

## 7. Facts to verify at writing time (status 22.10.2026)

Each item lists what competitors say, what the current rule appears to be (our STR page's sources or our hub), and what needs verifying. **"Verify" items must not go live until they are confirmed against the primary source.**

| # | Topic | What competitors say | Current rule as we understand it | Verify with |
|---|---|---|---|---|
| 1 | Golden visa tiers | "€250K" (yad2, Maariv, palmo, gogreece, nadlanexpert, **our STR meta**); "500 to 800K" (thisisgreece); "500K central Athens" (beta, one paragraph) | €800K in Attica, Thessaloniki, Mykonos, Santorini and islands over 3,100 residents; €400K elsewhere; €250K only for commercial-to-residential conversion or listed-building restoration; single property ≥120 m²; GV property may not be short-let; transitional rule for deposits made before 31.8.2024 (Law 5100/2024) | The Law 5100/2024 text, Enterprise Greece. **migration.gov.gr's English page does not show the tiers** |
| 2 | Transfer tax | 3.09% everywhere; thisisgreece says the seller pays | 3% plus a municipal surcharge = 3.09%, **paid by the buyer before signing** (AADE), on the higher of price and objective value | AADE |
| 3 | VAT on new builds | some say 24% applies | 24% suspended to 31.12.2026 (Law 5246/2025 per nadlanmaster; our STR page cites the MoF) | MoF; check the extension status for 2027 |
| 4 | Capital-gains tax (individuals) | "15% if sold within 5 years" (thisisgreece); "full exemption" (nadlanmaster Athens) | 15% statutory, **suspended to 31.12.2026** | AADE / MoF; extension status |
| 5 | Rental income tax | "9 to 44%" (thisisgreece); "15% then 35/45" (**our hub**) | 2026 scale 15% to €12K, 25% to €24K, 35% to €36K, 45% above (MoF guide cited on our STR page) | MoF |
| 6 | ENFIA | "0.1 to 1.15%", "0.1 to 0.5%", mislabelled table (gogreece) | Main tax per m² by zone value plus a supplementary tax for higher total values | AADE ENFIA rules |
| 7 | Athens STR freeze | ignored by nadlanmaster Athens, palmo, thisisgreece | No new first registrations in Athens municipal districts 1 to 3 in 2025, continued in 2026 (Law 5162/2024; MoF draft budget 2026) | Status for 2027 |
| 8 | Israeli tax on Greek rent | "only in Greece / nothing in Israel" (nadlanmaster x2, gogreece, Maariv, thisisgreece, palmo) | Israeli residents are taxed on worldwide income; regular track with foreign-tax credit **or** the 15% track (no expenses except depreciation, no foreign-tax credit) per the ITA guide (tax year 2025) | ITA guide plus a CPA review |
| 9 | Israeli tax on a later sale | nobody covers it | Capital-gains tax under the Israeli Income Tax Ordinance (not מס שבח), with credit for Greek tax if any | CPA |
| 10 | Does a Greek flat count for Israeli "דירה יחידה"? | nobody covers it | **Unverified.** It may affect the מס שבח exemption on a later Israeli sale, and may not affect Israeli purchase tax | ITA / CPA before publishing. Do not state it without a source |
| 11 | Mortgage for non-residents | LTV 60 to 75% (nadlanmaster), "up to 80%" and 3.5 to 7.5% (gogreece), 4 to 5% (beta) | varies by bank | Greek banks (Eurobank publishes a Hebrew GV brochure) |
| 12 | Prices | Athens €2,389 to 3,268/m²; "+45.2% in 2022" (beta, palmo) | Bank of Greece: Q4-2025 +7.6% y/y nationally, Athens +5.9%, Thessaloniki +8.0%; 2025 average +7.8% (per our STR page) | Latest Bank of Greece release (Q2 or Q3-2026) |
| 13 | Tourism | 38M visitors in 2025, €23.6bn (nadlanmaster) | n/a | Bank of Greece |
| 14 | Athens Metro line 4 | "opens 2026" (beta) | likely later | Attiko Metro |
| 15 | Seaside and island checks | absent everywhere | coastal zone, forest maps, out-of-plan building, illegal-build legalisation, cadastre (ΚΑΕΚ), ΠΕΑ energy certificate | Greek lawyer and engineer review |

---

## 8. Defects found on our own pages (no-silent-gaps: open Linear issues)

1. `/short-term-rentals-abroad/short-term-rentals-greece/`:
   - visible editor leftovers: "מאמר מוכן להדבקה" and a "## תגיות מוצעות" block;
   - duplicate "עודכן ונבדק" lines with two formats;
   - 5 cut-off sentences;
   - the meta description says "ויזת זהב מ-250 אלף יורו" (outdated, not in the body);
   - no breadcrumb, no images, and a FAQ without FAQPage schema.
2. `/global/greece/`:
   - two `<h1>` tags (the logo is an h1; probably site-wide on the /global/ template; check the other /global/ pages);
   - not in the sitemap index list we have;
   - the rental-tax line is outdated against our STR page;
   - thin (about 450 words).
3. `/global/project/koukaki-athens-residence/` and `glyfada-coast-suites-athens/`: "More posts" shows unrelated posts (Dubai prices, French and English Israel guides). The pages are thin; the illustrative labelling is fine. **Honesty check on Koukaki:**
   - The text says "מתאים גם למסלול ויזת זהב בצירוף נכס נוסף". Under the 2024 rules the €800K Attica threshold must be met with a **single** property of at least 120 m², so combining units most likely does not qualify. Verify (item 1 in section 7), then fix.
   - It pitches Koukaki as top for tourist rental. Verify whether Koukaki falls inside Athens municipal districts 1 to 3 (the new-STR-registration freeze). If it does, the page must say so.
4. Cross-site: jus-tice.co.il Greece pages compete with the planned cluster (section 6.3). This is a decision, not a defect.

---

## 9. DataForSEO spend

| Call | Count | Cost reported by the API |
|---|---|---|
| Google Ads search volume (live) | 2 tasks (148 + 80 keywords) | $0.18 |
| Google Ads keywords for keywords (live) | 1 task (20 seeds → 183 ideas) | $0.09 |
| SERP Google organic live advanced | 1 test at depth 10 ($0.002) + 14 at depth 30, with async AIO and PAA clicks ($0.0849) | $0.087 |
| **Total for this research** | | **≈ $0.357** |

The account balance moved from $28.33 to $26.77 during the session window. The extra ~$1.20 is not from these calls (other sessions share the account).

---

## Appendix A. Raw page metrics (script output on the raw HTML, 22.10.2026)

### A_nadlanmaster_greece

- URL: https://www.nadlanmaster.co.il/נדלן-ביוון/ (fetched 2026-10-22 16:05:04 UTC, 298145 bytes raw HTML)
- Title tag: השקעות נדל"ן ביוון - מדריך למשקיע, נכסים למכירה (מעודכן 2026)
- Meta description: נדל"ן ביוון - מידע מקיף בנושא השקעות נדלן ביוון למשקיעים ששוקלים להשקיע במדינה השכנה, כולל נתונים, תחזיות, נכסים, דירות להשקעה והזדמנויות >>
- H1: נדל"ן ביוון
- Breadcrumb: נדל"ן ביוון > מאת: מערכת נדלן מאסטר
- Dates: published 2016-12-01T15:53:29+00:00, modified 2026-07-07T08:17:23+00:00
- Author in schema: none
- Schema types: Answer, FAQPage, ImageObject, Organization, Question, WebPage, WebSite
- Main-content words: 4368; numeric tokens: 273; tables: 5; images in content: 65 (no alt: 2); iframes/video: https://www.youtube.com/embed/Ol2vMFcDC6k, https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d6422259.704289776!2d28.301397983801184!3d38.18971702944972!2m3!; forms: 3; FAQ-schema questions: 11
- Links in content: internal 100 (whole page 371), external 5 (bankofgreece.gr, globalpropertyguide.com, he.wikipedia.org, kpmg.com, tradingeconomics.com); WhatsApp links 2; tel/mail 2
- H2/H3 outline (19): השקעות נדלן ביוון – מדריך למשקיע בנדלן יווני בשנת 2026 | מספר נתוני מפתח על שוק הנדל"ן ביוון | סקירה כלכלית היסטורית ומצב נוכחי של שוק הנדל"ן ביוון | נכסים ביוון להשקעה – דירות למכירה | מגמת מחירי הנדל"ן ביוון על פני זמן | על מיסי נדלן ביוון, תשואות ומה שביניהם | אז איפה כדאי להשקיע ביוון בשנת 2026? | מחירי דירות ביוון, בתים ונכסים | עוד בנדלן מאסטר – מדריכי נדל"ן על ערים מובילות ביוון ונוספים | נתוני עליית מחירי הנדל"ן השנתית במדינה ב-7 השנים האחרונות | השלבים (הבירוקרטיים) של רכישת נכס ביוון | השקעה ביוון – היתרונות בשוק הנדל"ן המקומי | דירות למכירה ביוון יד 2 או דירה מקבלן בפרויקט חדש? | השכרה לטווח קצר (Airbnb) ביוון – למה לצפות, הרגולציה והמגבלות החדשות | השקעות נדלן ביוון – וידאו עם עיקרי הדברים | פרויקטים להשקעה ביוון | תשובות לשאלות נפוצות: | יוון – מפה:
- Tables: 13 rows: נתונים על שוק הנדל"ן ביוון, מידע על השקעות נדלן במדינה || 6 rows: אתונה, סלוניקי, לפקדה || 6 rows: כרתים, רודוס, מיקונוס || 9 rows: מחירי נכסים ביוון לפי סוג הנכס, טווח מחירים ממוצע (יורו), שכר דירה חודשי ממוצע || 10 rows: שנה, השינוי במחירי הנדל"ן ביוון (ב-%)
- FAQ schema questions: כמה עולה דירה ביוון? | איפה במדינה כדאי להשקיע? | האם צריך לשלם מס רכישה? | לאיזו תשואה שנתית אפשר לצפות? | מהו סכום ההשקעה הנדרש לקבלת גולדן ויזה? | כמה זמן לוקח להשלים את תהליך הרכישה? | איך משפיעה אמנת המס בין ישראל ויוון על המשקיע הישראלי? | אילו מסים יחולו על רווח ההון ביוון אם תרצו למכור את הנכס בעתיד? | מהו AFM ולמה הוא דרוש לתהליך הרכישה? | האם חייבים לטוס ליוון כדי לקנות נכס? | האם חובה לפתוח חשבון בנק ביוון?

### B_nadlanmaster_athens

- URL: https://www.nadlanmaster.co.il/נדלן-באתונה/ (fetched 2026-10-22 16:05:05 UTC, 275469 bytes raw HTML)
- Title tag: השקעות נדל"ן באתונה ב-2026 - מדריך למשקיע (ודירות להשקעה)
- Meta description: השקעות נדלן באתונה - מידע על השקעה בנדל"ן באתונה, מגמות השוק, יתרונות וחסרונות של השקעה באתונה, דירות, מיסוי והאם כדאי לקנות נכס בבירת יוון >>
- H1: השקעות נדל"ן באתונה
- Breadcrumb: השקעות נדל"ן באתונה > מאת: מערכת נדלן מאסטר
- Dates: published 2017-12-06T16:05:32+00:00, modified 2026-09-10T06:57:47+00:00
- Author in schema: none
- Schema types: Answer, FAQPage, ImageObject, Organization, Question, WebPage, WebSite
- Main-content words: 3478; numeric tokens: 126; tables: 2; images in content: 44 (no alt: 2); iframes/video: https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d50310.55760996028!2d23.77335884489847!3d37.99089965334265!2m3!1f0!; forms: 3; FAQ-schema questions: 7
- Links in content: internal 80 (whole page 367), external 3 (bankofgreece.gr, gov.il, he.wikipedia.org); WhatsApp links 2; tel/mail 2
- H2/H3 outline (17): השקעות נדל"ן באתונה בשנת 2026 – מדריך למשקיעים | מה חשוב לדעת לפני השקעה באתונה? | יתרונות השקעה בנדל"ן באתונה | אתונה – נתונים על השוק | הקשר בין משבר הסאב פריים לכדאיות רכישת נדל"ן באתונה | נדל"ן להשקעה באתונה – למה עכשיו? | נכסים להשקעה באתונה והסביבה | תשואה פוטנציאלית על השקעות נדל"ן באתונה | מיסוי נדלן באתונה – כמה מס תשלמו על נכס להשקעה באתונה? | שכונות להשקעה באתונה ואזורים מומלצים עם פוטנציאל בעיר | מחירי דירות באתונה – כמה עולה דירה בעיר? | בטבלה: השינוי במחירי הנדל"ן באתונה ב-5 השנים האחרונות | גרף מגמת מחירי הנדל"ן באתונה ב-15 השנים האחרונות | תהליך רכישת נכס באתונה – שלבים עיקריים: | השקעה בנדל"ן באתונה – איפה מתחילים? | מפה של אתונה:
- Tables: 11 rows: שוק הנדל"ן בעיר אתונה, נתונים || 10 rows: שנה, השינוי במחירי הנדל"ן (ב-%)
- FAQ schema questions: האם כדאי לרכוש דירות באתונה בתקופה הנוכחית? | כמה עולה דירה באתונה? | מהן השכונות המובילות והמבוקשות בעיר? | האם צריך להיות אזרח יווני כדי לקנות נכס באתונה? | איזה סכום צריך להשקיע כדי להיות זכאי לגולדן ויזה ביוון? | מהם המיסים שצריך משקיע זר לשלם על נכס באתונה? | האם קיימת אמנת מס בין ישראל ויוון?

### C_thisisgreece_houses

- URL: https://thisisgreece.co.il/houses-for-sale-in-greece/ (fetched 2026-10-22 16:05:05 UTC, 192775 bytes raw HTML)
- Title tag: בתים למכירה ביוון - איך קונים בית ביוון? (מדריך, דירות ונכסים)
- Meta description: בתים למכירה ביוון - חושבים לקנות בית ביוון? ריכזנו כל מה שחשוב לדעת על רכישת נכס או דירה ביוון והאיים. מידע מקיף על התהליך, דירות ונכסים >>
- H1: בתים למכירה ביוון
- Breadcrumb: דף הבית > מדריכים > בתים למכירה ביוון
- Dates: published 2024-08-12T09:02:06+00:00, modified 2025-08-31T08:28:04+00:00
- Author in schema: none
- Schema types: BreadcrumbList, ImageObject, Organization, WebPage, WebSite
- Main-content words: 1965; numeric tokens: 56; tables: 2; images in content: 36 (no alt: 2); iframes/video: none; forms: 2; FAQ-schema questions: 0
- Links in content: internal 40 (whole page 102), external 0 (-); WhatsApp links 0; tel/mail 4
- H2/H3 outline (7): בתים למכירה ביוון – המדריך השלם לקניית בית ביוון | דירות למכירה ביוון, בתים ונכסים | האם כדאי לקנות בית ביוון? | כמה עולה בית ביוון? | שלבי רכישת בית ביוון | הוצאות נלוות בעת קניית בית ביוון | פרויקטים מובילים
- Tables: 6 rows: כ-11 מיליון בני אדם, מעל 30 מיליון תיירים בשנה, כ-300,000 יורו, 10%-5%, אתונה, סלוניקי, כרתים, לפקדה, מיקונוס, ס || 13 rows: החל מ-250 אלף יורו, בין אם מעוניינים ברכישת בית נופש ביוון ו, החל מ-400 אלף יורו, ברחבי יוון ניתן למצוא בתי יוקרה עם נוף ל, החל מ-100 אלף יורו, לצד בתי הנופש ווילות היוקרה, יוון מציעה 

### D_beta_prices_athens

- URL: https://beta-estate.com/real-estate-prices-athens/ (fetched 2026-10-22 16:05:07 UTC, 229341 bytes raw HTML)
- Title tag: מחירי דירות באתונה: סקירה 2026 | כמה עולה דירה באתונה? ביתא נדל״ן
- Meta description: מחפשים לדעת כמה עולה דירה באתונה? במדריך הזה תגלו את מחירי הדירות, הגורמים המשפיעים על השוק, ואת האתגרים והשיקולים החשובים ביותר למשקיעים
- H1: מחירי דירות באתונה: סקירה 2026
- Breadcrumb: דף הבית > הבלוג שלנו > מחירי דירות באתונה: סקירה 2026
- Dates: published 2024-06-18T07:26:37+00:00, modified 2026-02-05T10:05:42+00:00
- Author in schema: info
- Schema types: Article, BreadcrumbList, ImageObject, Organization, Person, WebPage, WebSite
- Main-content words: 2984; numeric tokens: 166; tables: 3; images in content: 8 (no alt: 6); iframes/video: https://beta-estate.com/wp-content/uploads/2024/06/what_you_get_infographicnewnews.html; forms: 3; FAQ-schema questions: 0
- Links in content: internal 9 (whole page 41), external 1 (facebook.com); WhatsApp links 2; tel/mail 8
- H2/H3 outline (29): נקודות מפתח – מחירי דירות באתונה 2026 | מחירי דירות ממוצעים באתונה (2018-2026) | מהו המחיר הממוצע לדירה באתונה? | מחירי דירות באתונה לפי שכונות (2026): | אתגרים בהכרת השוק והבנת מחירי הדירות בין יוון לישראל | מגמות ותחזיות לשנים הבאות | שיקולים חשובים לרוכשים ולמשקיעים | טיפים שימושיים למשקיעים המחפשים מחירי דירות אטרקטיביים באתונה | סיכום והמלצות | שאלות ותשובות נפוצות | מהו המחיר הממוצע למ"ר באתונה בשנת 2026? | למה מחירי הדירות באתונה עולים בשנים האחרונות? | באילו שכונות באתונה המחירים הכי נמוכים ואיפה הכי יקר? | כמה עולה דירה ממוצעת באתונה? | מה ההבדל בין דירה חדשה לדירה יד שנייה באתונה מבחינת מחיר וכדאיות? | אילו גורמים הכי משפיעים על מחיר הדירה באתונה? | האם אתונה עדיין נחשבת “זולה” ביחס לערי בירה אחרות באירופה? | האם אפשר להשיג תשואה של 6%–8% מהשכרה באתונה? | האם צריך להיות נוכח פיזית באתונה כדי להבין את השוק? | האם הבנקים ביוון נותנים משכנתאות למשקיעים זרים? | איך ביתא נדל"ן יכולה לעזור למשקיע הישראלי במחירי הדירות באתונה? | אודות ביתא נדל"ן | מקורות | צרו איתנו קשר | ההזדמנויות הטובות ביותר באתונה נסגרות הרבה לפני שהן מגיעות לכותרות. השאירו פרטים ונקפוץ לכם למייל רק כשיש משהו שבאמת שווה את הזמן שלכם. | מה קורה ביום שאחרי קבלת מפתח? | 18.08.2026 | 19:00 | ההרשמה בחינם | לא תודה
- Tables: 10 rows: שנה, מחיר ממוצע למ"ר (€), שינוי שנתי (%) || 16 rows: אזור, מחיר ממוצע למ"ר (€), שינוי שנתי (%), מחיר שכירות ממוצע למ"ר (€), מאפיינים, 3,694 || 11 rows: השפה היוונית מהווה מחסום; רוב המסמכים, ה, עברית היא שפת האם של המשקיע הישראלי; המס, היעדר אתרים מקוונים מקיפים כמו "מדלן" או, קיימים אתרים וכלים מקוונים בעברית המספקי, קושי בגישה למסמכים רשמיים כמו נסח טאבו; , גישה מקוונת ופשוטה למסמכים רשמיים ולמידע

### F_palmo_buying

- URL: https://palmo-group.com/buying-a-real-estate-in-greece/ (fetched 2026-10-22 16:05:10 UTC, 653111 bytes raw HTML)
- Title tag: קניית בית ביוון – דירות להשקעה ביוון | פאלמו – מצוינות בהשקעות נדל"ן
- Meta description: מתעניין לקנות בית ביוון? היכנסו לקרוא את המדריך המקיף שלנו עבור המשקיע הישראל - מתהליך הרכישה, התקציב, האזורים הפופולריים ועוד
- H1: המדריך לקניית בית ביוון
- Breadcrumb: דף הבית > קניית בית ביוון
- Dates: published 2023-10-05T07:08:47+00:00, modified 2026-06-25T11:30:39+00:00
- Author in schema: none
- Schema types: Answer, BreadcrumbList, FAQPage, ImageObject, Organization, Question, WebPage, WebSite
- Main-content words: 3155; numeric tokens: 133; tables: 7; images in content: 24 (no alt: 6); iframes/video: none; forms: 1; FAQ-schema questions: 5
- Links in content: internal 41 (whole page 64), external 0 (-); WhatsApp links 2; tel/mail 3
- H2/H3 outline (19): למה לקנות בית ביוון? | התפתחות מחירי דירות (יד שניה) ממוצעים באתונה (2018-2024) | שיעור השינוי השנתי במדד מחירי הנדל"ן ביוון בין השנים 2008–2024 (נתונים נומינליים): | צעד אחר צעד: השלבים בקניית בית ביוון | מחירי דירות ממוצעים באתונה לפי שכונות, נכון ל-2024: | המחיר הממוצע למ"ר בדירות באתונה, סלוניקי, סנטוריני ומיקונוס (נכון ל-2024): | לוקיישן, לוקיישן, לוקיישן: היכן כדאי לקנות בית ביוון? | דירות למכירה ביוון | 12 Averof | דירה באתונה מול האקרופוליס | הזדמנות לדירה באתונה | בנייה חדשה בלב החוויה העירונית | המיקום: פריסטרי. המחיר: היסטרי! | עבר ועתיד נפגשים בלב אתונה: הכירו את המלכה החדשה בשכונה | ובין לבין - לנפוש בלב העניינים | דירה להשקעה בשכונת ספוליה | קרוב לים, צמוד למטרו, פסיעה ממרכז העיר | שאלות תשובות
- Tables: 8 rows:  || 17 rows:  || 17 rows:  || 14 rows:  || 14 rows:  || 4 rows:  || 4 rows: 
- FAQ schema questions: מדוע פלאקה נקראת "שכונת האלים"? | מה ההבדל בין השקעה בדירה לטווח ארוך לדירת נופש? | אילו מסמכים נדרשים לרכישת נכס ביוון? | מהן הטבות המס לרוכשי דירה ביוון? | היכן כדאי לקנות נכס ביוון?

### R_gogreece_process

- URL: https://gogreece.co.il/the-investment-process/ (fetched 2026-10-22 16:05:31 UTC, 249520 bytes raw HTML)
- Title tag: תהליך קניית בית ביוון – מדריך ב-7 שלבים מפורטים | Go Greece IL
- Meta description: תהליך קניית בית ביוון – בזמן שבישראל מחירי הדיור בשמיים והתשואות נמוכות, במרחק שעה וחצי טיסה בלבד, קניית בית ביוון תניב לכם תשואה גבוהה במחיר שווה. היכנסו.
- H1: תהליך קניית בית ביוון – 7 שלבים להשקעה מנצחת
- Breadcrumb: Go Greece IL > מאמרים > השקעות ביוון > תהליך קניית בית ביוון
- Dates: published 2023-01-28T12:29:15+00:00, modified 2026-09-24T14:27:28+00:00
- Author in schema: none
- Schema types: Answer, FAQPage, Question
- Main-content words: 2464; numeric tokens: 84; tables: 3; images in content: 22 (no alt: 0); iframes/video: none; forms: 4; FAQ-schema questions: 4
- Links in content: internal 42 (whole page 159), external 3 (facebook.com, he.wikipedia.org); WhatsApp links 4; tel/mail 5
- H2/H3 outline (16): מדוע כדאי להיכנס לתהליך קניית בית ביוון? | תהליך קניית בית ביוון: שלב 1 – לקנות בית ביוון עם קבלת ייעוץ מתאים | אילו מסמכים נדרשים לאורך תהליך קניית בית ביוון? | תהליך קניית בית ביוון: שלב 2 – פתיחת חשבון בנק | האם ניתן לרכוש בית ביוון מבלי לצאת מהארץ? | תהליך קניית בית ביוון: שלב 3 – לאתר את הנכס המתאים | דירה מרוהטת היא לא בהכרח יתרון | חימום הוא אלמנט קריטי | נגישות לחניה | תהליך קניית בית ביוון: שלב 4 – לסגור על מחיר הוגן | תהליך קניית בית ביוון: שלב 5 – הסכם ראשוני והפקדת פיקדון | תהליך קניית בית ביוון: שלב 6 – טיפול במימון ההשקעה | מסמכים נדרשים | תהליך קניית בית ביוון: שלב 7 – חתימה סופית, הנפקת שטר מכר וקבלת המפתח | תם – אך לא נשלם | תשובות לשאלות נפוצות
- Tables: 14 rows: 2008, 0.77-, 3.57-, 2009, -4.21, 6.04- || 3 rows: מיקום, מחיר חציוני באירו למ"ר, במרכז, 1,922, מחוץ למרכז, 2,000 || 7 rows: עד 200 אלף אירו, 0.10%, עד 300 אלף אירו, 0.15%, עד 400 אלף אירו, 0.25%
- FAQ schema questions: האם כדאי ללכת על רכישת נכס ביוון? | מהם תנאי ויזת הזהב למשקיעי נדל"ן ביוון? | האם ניתן לקבל משכנתא ביוון? | האם ניתן לרכוש נכס ביוון מישראל?

### E_yad2_blog_greece

- URL: https://blog.yad2.co.il/נדלן-ביוון/ (fetched 2026-10-22 16:05:09 UTC, 127737 bytes raw HTML)
- Title tag: נדל"ן ביוון -
- Meta description: נדל"ן ביוון לכל הפרטים היכנסו לבלוג יד 2 עכשיו >>
- H1: נדל"ן ביוון
- Breadcrumb: Home > נדל&#8221;ן ביוון
- Dates: published 2025-06-17T11:53:00+00:00, modified 2025-11-16T14:27:11+00:00
- Author in schema: none
- Schema types: BreadcrumbList, ImageObject, Person, WebPage, WebSite
- Main-content words: 534; numeric tokens: 5; tables: 0; images in content: 9 (no alt: 8); iframes/video: none; forms: 2; FAQ-schema questions: 0
- Links in content: internal 12 (whole page 88), external 1 (aramapp.com); WhatsApp links 0; tel/mail 0
- H2/H3 outline (7): דואט רמת אפעל: סיפור אהבה בין ירוק ליוקרה בלב השכונה הוותיקה | פרויקט שלמה המלך 8-10 בקריית אונו של שלום את נתן – חוויית מגורים חדשה בלב העיר | הזדמנות נדירה למגורים בפרויקט חדש: דירת 4 חדרים עם תנאי תשלום גמישים ומחיר PRE-SALE | GINOT ברחובות – חווית מגורים למשפחות מבית אפרידר | עזריאלי טאון תל אביב – פרויקט מגורים יוקרתי מבית עזריאלי מגורים בלב העיר | "מגדלי רחובות הצעירה": מהפכת ההתחדשות העירונית של רחובות מתחילה כאן

### G_shoval_projects

- URL: https://www.shovalyazamoot.com/projects (fetched 2026-10-22 16:05:11 UTC, 58512 bytes raw HTML)
- Title tag: שובל יזמות - פרוייקטים
- Meta description: none
- H1: דירות להשקעה ביוון
- Breadcrumb: ראשי > דירות להשקעה ביוון
- Dates: published n/a, modified n/a
- Author in schema: none
- Schema types: none
- Main-content words: 321; numeric tokens: 19; tables: 0; images in content: 43 (no alt: 27); iframes/video: none; forms: 1; FAQ-schema questions: 0
- Links in content: internal 47 (whole page 84), external 3 (droxit.com, waze.com); WhatsApp links 3; tel/mail 6
- H2/H3 outline (18): פרוייקטים | דירות | דירה להשקעה ביוון, מרכז סלוניקי, 1BR | וילה למכירה ביוון, ניקיטי, ITAMOS Villa | דירה להשקעה ביוון, ניקיטי, 1BR | דירה להשקעה ביוון, מרכז סלוניקי, STUDIO | וילה למכירה ביוון, ניקיטי, PINE Villa | דירה להשקעה ביוון, ניקיטי, STUDIO | וילה למכירה ביוון, ניקיטי, EVERGREEN OAK Villa | דירה להשקעה ביוון, ניקיטי, 1BR gallery | דירה להשקעה ביוון, ניקיטי, MAGNOLIA Garden Apartment | דירה להשקעה ביוון, ניקיטי 1BR big gallery | דירה להשקעה ביוון, ניקיטי, OLIVE Garden Apartment | דירה להשקעה ביוון, ניקיטי, WINE GRAPE Penthouse | דירות להשקעה ביוון בצל משבר הקורונה | דירות להשקעה ביוון – אתונה | דירות להשקעה ביוון – סלוניקי | דירות להשקעה ביוון – פיראוס

### H_newgreece_buying

- URL: https://new-greece.co.il/buying-an-apartment-in-greece/ (fetched 2026-10-22 16:05:12 UTC, 623602 bytes raw HTML)
- Title tag: ?קניית דירה ביוון – איך זה עובד - יוון החדשה - דירות ובתים ביוון
- Meta description: משקיעים רבים גילו את הפוטנציאל שבמדינות זרות, בדגש על יוון – הנמצאת במרחק של שעה בלבד. באתר תמצאו את המתווה הכללי שישקף בפניכם את תהליך קניית הדירה ביוון.
- H1: ?קניית דירה ביוון – איך זה עובד
- Breadcrumb: Home > ?קניית דירה ביוון – איך זה עובד
- Dates: published 2018-11-07T13:49:31+00:00, modified 2018-11-08T11:25:40+00:00
- Author in schema: יוון החדשה
- Schema types: Article, BreadcrumbList, ImageObject, Organization, Person, WebPage, WebSite
- Main-content words: 428; numeric tokens: 4; tables: 0; images in content: 2 (no alt: 1); iframes/video: none; forms: 1; FAQ-schema questions: 0
- Links in content: internal 2 (whole page 88), external 0 (-); WhatsApp links 0; tel/mail 1
- H2/H3 outline (4): הצעד הראשון: היכרות וסיור נכסים | הצעד השני: רכישת הנכס | ?הנכס שלכם: מה קורה כעת | ?משקיעים זרים ותשואה – מה כדאי לדעת

### I_maariv_8steps

- URL: https://www.maariv.co.il/business/realestate/article-1093013 (fetched 2026-10-22 16:05:13 UTC, 235068 bytes raw HTML)
- Title tag: המדריך למשקיע המתחיל: כך תקנו דירה ביוון ב-8 שלבים | מעריב
- Meta description: יוון מספקת שלל הזדמנויות לנכסים אטרקטיביים עם פוטנציאל תשואה גבוה. מה הצעדים שיש לעשות אם רוצים לקנות בה נכס? כך תעשו זאת נכון
- H1: המדריך למשקיע המתחיל: כך תקנו דירה ביוון ב-8 שלבים
- Breadcrumb: מעריב > > > כלכלה > > > נדל"ן
- Dates: published n/a, modified n/a
- Author in schema: none
- Schema types: none
- Main-content words: 518; numeric tokens: 14; tables: 0; images in content: 6 (no alt: 0); iframes/video: none; forms: 0; FAQ-schema questions: 0
- Links in content: internal 4 (whole page 102), external 4 (facebook.com, news.google.com, oref.org.il, twitter.com); WhatsApp links 1; tel/mail 0
- H2/H3 outline (1): יוון מספקת שלל הזדמנויות לנכסים אטרקטיביים עם פוטנציאל תשואה גבוה. מה הצעדים שיש לעשות אם רוצים לקנות בה נכס? כך תעשו זאת נכון

### J_nadlanmaster_goldenvisa

- URL: https://www.nadlanmaster.co.il/גולדן-ויזה-יוון/ (fetched 2026-10-22 16:05:14 UTC, 220014 bytes raw HTML)
- Title tag: גולדן ויזה יוון - איך לקבל ויזת זהב למשקיעים / תושבות (מדריך)
- Meta description: גולדן ויזה ליוון - מידע מקיף על האפשרות לקבל תושבות ביוון באמצעות ויזת זהב. תנאים לקבלת מעמד תושב קבע, יתרונות ומהו הסכום שצריך להשקיע?
- H1: גולדן ויזה – יוון
- Breadcrumb: גולדן ויזה – יוון > מאת: מערכת נדלן מאסטר
- Dates: published 2024-01-07T10:05:44+00:00, modified 2026-09-10T06:57:20+00:00
- Author in schema: none
- Schema types: ImageObject, Organization, WebPage, WebSite
- Main-content words: 1511; numeric tokens: 25; tables: 1; images in content: 21 (no alt: 2); iframes/video: none; forms: 3; FAQ-schema questions: 0
- Links in content: internal 36 (whole page 323), external 1 (he.wikipedia.org); WhatsApp links 2; tel/mail 1
- H2/H3 outline (11): ויזת זהב ליוון – איך מקבלים ויתרונות מרכזיים – מדריך למשקיעים | גולדן ויזה יוון – תקציר למשקיע: | למה כדאי להוציא גולדן ויזה יוון ולמי היא מיועדת? | יתרונות של ויזת זהב ביוון | משמעות גולדן ויזה ביוון באיחוד האירופי | מי זכאי לגולדן ויזה ביוון וכיצד ניתן להנפיק את האשרה | מהו סכום ההשקעה הנדרש ביוון עבור גולדן ויזה ומהם תנאי הסף להגשת הבקשה | אילו מסמכים צריך להגיש כדי לקבל גולדן ויזה ביוון | האם קיים תוקף לוויזת זהב ביוון? | סיבות נוספות להשקעה ביוון פרט לגולדן ויזה | פרויקטים להשקעה ביוון
- Tables: 6 rows: שאלה, תשובה

### K_yadidlaw_goldenvisa

- URL: https://yadidlaw.com/השקעות-ותושבות-ביוון (fetched 2026-10-22 16:05:14 UTC, 282038 bytes raw HTML)
- Title tag: השקעות ותושבות ביוון - גולדן ויזה | עו''ד ונוטריון דוד ידיד
- Meta description: מסלול משקיעים גולדן ויזה יוון מעניק מעמד תושב למשקיעים ולבני משפחתם ל10 שנים. למידע על השקעות ותושבות ביוון, היכנסו לאתר >>
- H1: השקעות ותושבות ביוון (Golden Visa)
- Breadcrumb: דף הבית > השקעות ותושבות ביוון
- Dates: published 2022-07-26T07:25:04+00:00, modified 2026-10-19T10:06:09+00:00
- Author in schema: none
- Schema types: BreadcrumbList, ImageObject, Organization, VideoObject, WebPage, WebSite
- Main-content words: 427; numeric tokens: 9; tables: 0; images in content: 2 (no alt: 0); iframes/video: none; forms: 3; FAQ-schema questions: 0
- Links in content: internal 3 (whole page 193), external 0 (-); WhatsApp links 1; tel/mail 11
- H2/H3 outline (2): השקעות נדל"ן ביוון - סיוע וליווי על ידי משרדנו | מסלול משקיעים ביוון

### S_euro_pass_gv

- URL: https://euro-pass.co.il/greece-golden-visa-legal-guide/ (fetched 2026-10-22 16:05:32 UTC, 251741 bytes raw HTML)
- Title tag: ויזת זהב יוון - המדריך המשפטי להבטחת ההשקעה | עו"ד פינקו
- Meta description: חושבים על ויזת זהב ליוון? גלו למה ליווי משפטי של עו"ד ונוטריון ישראלי הוא קריטי להבטחת ההשקעה, מניעת סיכונים והצלחת התהליך. מדריך מקיף לשנת 2026.
- H1: הליווי המשפטי מאחורי ויזת זהב יוון: תפקיד עורך הדין והנוטריון בהבטחת ההשקעה
- Breadcrumb: דרכון פורטוגלי > הליווי המשפטי מאחורי ויזת זהב יוון: תפקיד עורך הדין והנוטריון בהבטחת ההשקעה
- Dates: published 2026-08-21T08:43:57+00:00, modified 2026-10-21T05:45:12+00:00
- Author in schema: משרד עו"ד פינקו אלפסי
- Schema types: Answer, Article, BreadcrumbList, ContactPoint, Country, FAQPage, HowTo, HowToStep, ImageObject, LegalService, LocalBusiness, OpeningHoursSpecification, Organization, Person, PostalAddress, Question, SpeakableSpecification, WebPage, WebSite
- Main-content words: 3271; numeric tokens: 51; tables: 1; images in content: 30 (no alt: 1); iframes/video: https://maps.google.com/maps?q=%D7%90%D7%91%D7%90%20%D7%94%D7%9C%D7%9C%207%2C%20%D7%A8%E2%80%9D%D7%92&t=m&z=10&output=em; forms: 3; FAQ-schema questions: 7
- Links in content: internal 20 (whole page 84), external 0 (-); WhatsApp links 2; tel/mail 8
- H2/H3 outline (50): נקודות חשובות מהמאמר | למה הוצאת ויזת זהב יוון היא קודם כל תהליך משפטי? | השילוב המנצח: עורך דין ישראלי לצד עורך דין מקומי | בדיקת נאותות משפטית לנכס (Due Diligence) | האם הנכס נקי מחובות ועיקולים? | מבנה הסכם הרכישה והבטחת כספי המשקיע | חשבונות נאמנות והגנה על הכסף | תפקיד הנוטריון באימות וחתימת המסמכים | מה עושה הנוטריון הישראלי? | מה עושה הנוטריון היווני? | תהליך העברת הכספים וחובות הדיווח | פתיחת חשבון בנק ביוון ומספר מס (AFM) | ליווי בהגשת הבקשה לרשויות ההגירה | הכנת התיק ברמה הבינלאומית | ניהול סיכונים משפטיים: מלכודות נפוצות ואיך להימנע מהן | מחירים מנופחים והבטחות שווא | חוקי המשחק החדשים: עדכוני ספי ההשקעה ביוון לשנת 2026 | סכומי ההשקעה המעודכנים (נכון ל-2026) | סוגיות מיסוי הכרוכות ברכישה והחזקת הנכס | רכישה כאדם פרטי לעומת חברה בע"מ | עלויות משפטיות ונוטריוניות צפויות בתהליך | ביצוע העסקה מרחוק: תהליך קבלת ייפוי כוח נוטריוני | מתי בכל זאת תצטרכו לטוס? | ליווי משפטי לאחר קבלת הוויזה: חידוש וניהול שוטף | שמירה על תוקף הוויזה ל-5 השנים הבאות | הטיפ של עו"ד הילה פינקו: אל תחתמו על שום מסמך בלי תרגום משפטי מלא | שאלות נפוצות | מה תפקידו של עורך דין בתהליך קבלת ויזת זהב ליוון, והאם חובה לשכור אחד? | מה ההבדל בין תפקיד עורך הדין לתפקיד הנוטריון בעסקת רכישת נדל"ן ביוון? | מהן העלויות הנלוות לייעוץ משפטי ונוטריוני בתהליך ויזת הזהב? | כיצד עורך הדין מוודא שהנכס נקי מחובות, עיקולים ובעיות רישום בטאבו? | אילו מסמכים משפטיים יש להכין, לתרגם ולאשר נוטריונית לצורך הגשת הבקשה? | מהם השלבים המשפטיים המרכזיים מרגע איתור הנכס ועד לקבלת אישור התושבות? | כיצד הליווי המשפטי מסייע בהבטחת כספי ההשקעה ושמירה על תוקף הוויזה? | לסיכום: אל תשאירו את העתיד שלכם ליד המקרה | לבדיקת זכאות אונליין | באיזה דרכון/ויזה מדובר? | בדיקת זכאות ראשונית | השאר פרטים ונחזור אליך בהקדם | תודה, פנייתך התקבלה!
- Tables: 5 rows: פרמטר להשוואה, רכישה כאדם פרטי, רכישה דרך חברה (LLC)
- FAQ schema questions: מה תפקידו של עורך דין בתהליך קבלת ויזת זהב ליוון, והאם חובה לשכור אחד? | מה ההבדל בין תפקיד עורך הדין לתפקיד הנוטריון בעסקת רכישת נדל"ן ביוון? | מהן העלויות הנלוות לייעוץ משפטי ונוטריוני בתהליך ויזת הזהב? | כיצד עורך הדין מוודא שהנכס נקי מחובות, עיקולים ובעיות רישום בטאבו? | אילו מסמכים משפטיים יש להכין, לתרגם ולאשר נוטריונית לצורך הגשת הבקשה? | מהם השלבים המשפטיים המרכזיים מרגע איתור הנכס ועד לקבלת אישור התושבות? | כיצד הליווי המשפטי מסייע בהבטחת כספי ההשקעה ושמירה על תוקף הוויזה?

### P_yamas_gv250

- URL: https://yamasre.com/golden-visa-starting-from-250k-in-thessaloniki/ (fetched 2026-10-22 16:05:28 UTC, 107698 bytes raw HTML)
- Title tag: פריסייל מיוחד לחברי יאמאס – דירות לגולדן ויזה בהחל מ-250K€ בסלוניקי!
- Meta description: כל יוון שונתה לרף של 400 אלף יורו בפריפריה ו-800 אלף במרכזי הערים – אבל וזה אבל ענק, נכנס סוג עסקה חדש המאפשר ויזה במרכזי הערים ב-250 אלף יורו ומעלה, כמו פעם.
- H1: פריסייל מיוחד לחברי יאמאס – דירות לגולדן ויזה בהחל מ-250K€ בסלוניקי!
- Breadcrumb: none
- Dates: published n/a, modified n/a
- Author in schema: none
- Schema types: none
- Main-content words: 374; numeric tokens: 15; tables: 0; images in content: 4 (no alt: 2); iframes/video: none; forms: 0; FAQ-schema questions: 0
- Links in content: internal 2 (whole page 40), external 0 (-); WhatsApp links 0; tel/mail 0
- H2/H3 outline (1): תיאום שיחת ייעוץעם ירון בלום

### T_ytax_treaty

- URL: https://y-tax.co.il/country/אמנת-מס-ישראל-יוון/ (fetched 2026-10-22 16:05:33 UTC, 302159 bytes raw HTML)
- Title tag: אמנת מס יוון - ישראל | נמרוד ירון ושות׳
- Meta description: משרד נמרוד ירון ושות' מייעץ בנושא אמנת מס יוון ישראל והיבטי מס נוספים במיסוי בינלאומי. פנו אלינו למתן ייעוץ אישי בנושא מס ביוון.
- H1: אמנת מס יוון – ישראל
- Breadcrumb: דף הבית > אמנת מס יוון &#8211; ישראל
- Dates: published 2024-12-11T13:16:41+00:00, modified 2026-10-18T12:55:36+00:00
- Author in schema: none
- Schema types: BreadcrumbList, Country, ImageObject, LegalService, LocalBusiness, Organization, Person, QuantitativeValue, WebPage, WebSite
- Main-content words: 1941; numeric tokens: 122; tables: 2; images in content: 6 (no alt: 1); iframes/video: https://currencyrate.today/load-exchangerates?lg=en&tz=0&fm=ILS&to=USD%2CGBP%2CAUD%2CCNY%2CJPY%2CRUB&st=default&cd=0&am=; forms: 4; FAQ-schema questions: 0
- Links in content: internal 13 (whole page 209), external 8 (aade.gr, amitmoreno.com, gov.il, ils.currencyrate.today, mfa.gr, new.embassies.gov.il, sld.co.il); WhatsApp links 1; tel/mail 12
- H2/H3 outline (23): אמנה למניעת כפל מס בין ישראל ליוון | ידיעות עדכניות | יחסי ישראל-יוון | פעילות עסקית ביוון | הסכמים בילטרליים ומוליטרליים בין יוון לישראל | תחולת ה- MLI | תושבות לצורכי מס ביוון | מערכת המיסוי ביוון | ניכוי מס במקור | מס ירושה ומס עיזבון ביוון | רילוקיישן ליוון | מיסוי מקרקעין ביוון | העברת כספים מישראל ליוון | סוגי ישויות עסקיות ביוון | חוקי תמריצים ביוון | מדינות איתן ליוון יש אמנה למניעת כפל מס | ליצירת קשר | שערי מטבע | מאמרים פופולאריים | מס על ירושה מחו"ל | מס על שכירות נדל"ן בחו"ל | העברת כספים לחו"ל ומחו"ל | להתייעצות עם מומחה במסים
- Tables: 9 rows:  || 8 rows: 

### L_thisisgreece_prices

- URL: https://thisisgreece.co.il/property-prices/ (fetched 2026-10-22 16:05:15 UTC, 154397 bytes raw HTML)
- Title tag: מחירי דירות ביוון - עלות נכס לפי עיר / אי (ראו מחירון מפורט)
- Meta description: מחיר דירה ביוון משתנה בהתאם למיקום הנכס, סוג הנכס, ומאפיינים נוספים. גלו איך נקבעים מחירי נדל"ן ביוון וכמה עולה נכס (בתים / דירות) במחירון >>
- H1: מחירון דירות ביוון
- Breadcrumb: דף הבית > מחירון דירות ביוון
- Dates: published 2024-08-25T14:47:59+00:00, modified 2025-03-13T07:53:55+00:00
- Author in schema: none
- Schema types: BreadcrumbList, ImageObject, Organization, WebPage, WebSite
- Main-content words: 1697; numeric tokens: 144; tables: 2; images in content: 5 (no alt: 2); iframes/video: none; forms: 2; FAQ-schema questions: 0
- Links in content: internal 8 (whole page 69), external 3 (bankofgreece.gr, nadlanmaster.co.il); WhatsApp links 0; tel/mail 4
- H2/H3 outline (8): מחירון דירות ביוון 2025 – מחירים ועלויות | מחירי נכסים ביוון | מחירי הנדל"ן ביוון ומגמת הצמיחה הכלכלית – סקירה כללית | מחירי הנכסים במדינה בשנת 2025 | כמה עולה בית ביוון? | הבדלי מחירים בין דירה בפרויקט חדש ביוון לבין דירות יד שניה | מחירי שכירות ביוון – מהו שכר הדירה הממוצע במדינה? | מה משפיע על מחירי נכסים ביוון והאיים
- Tables: 8 rows: 1500-5000 יורו, 1800-5000 יורו, 1500-3500 יורו, 70,000-160,000 יורו, 90,000-160,000 יורו, 70,000-130,000 יורו || 8 rows: 1700-3500 יורו, 3500-6500 יורו, 1500-2500 יורו, 75,000-140,000 יורו, 150,000-250,000 יורו, 85,000-140,000 יורו

### M_beta_equity

- URL: https://beta-estate.com/how-much-equity-needed-to-buy-apartment-in-greece/ (fetched 2026-10-22 16:05:17 UTC, 200744 bytes raw HTML)
- Title tag: כמה הון עצמי צריך כדי לקנות דירה ביוון? המדריך המלא לשנת 2026 - ביתא נדל״ן
- Meta description: כמה הון עצמי צריך כדי לקנות דירה ביוון ב-2026? מדריך למשקיעים ישראלים עם פירוט על רכישה במזומן, משכנתא, עלויות נלוות וגולדן ויזה.
- H1: כמה הון עצמי צריך כדי לקנות דירה ביוון? המדריך המלא לשנת 2026 / נקודות מפתח
- Breadcrumb: דף הבית > הבלוג שלנו > כמה הון עצמי צריך כדי לקנות דירה ביוון? המדריך המלא לשנת 2026
- Dates: published 2026-06-15T11:23:56+00:00, modified 2026-06-15T11:27:28+00:00
- Author in schema: info
- Schema types: Article, BreadcrumbList, ImageObject, Organization, Person, WebPage, WebSite
- Main-content words: 2286; numeric tokens: 168; tables: 4; images in content: 6 (no alt: 3); iframes/video: https://beta-estate.com/wp-content/uploads/2026/06/טבלה-הון-עצמי-לפי-מסלול-רכישה-ביתא.html; forms: 3; FAQ-schema questions: 0
- Links in content: internal 7 (whole page 39), external 6 (beta.deebo.co.il, facebook.com); WhatsApp links 2; tel/mail 8
- H2/H3 outline (21): כמה הון עצמי צריך כדי לקנות דירה ביוון במזומן, בלי משכנתא? | כמה הון עצמי צריך כדי לקנות דירה ביוון בעזרת משכנתא? | מהן כל העלויות הנלוות לרכישת דירה ביוון, וכמה הן מוסיפות להון הנדרש? | כמה עולה דירה ביוון בשנת 2026, ואיך זה מתורגם להון עצמי? | כמה הון עצמי צריך כדי לקבל גולדן ויזה ביוון ב-2026? | אילו מסלולי מימון פתוחים בפני משקיע ישראלי, ומה ההבדל ביניהם? | סיכום: כמה הון עצמי באמת צריך, ומה השלב הבא | שאלות נפוצות | כמה הון עצמי מינימלי צריך כדי לקנות דירה ביוון ב-2026? | האם משקיע ישראלי יכול לקבל משכנתא בבנק יווני, ובאיזה שיעור מימון? | מהן העלויות הנלוות לרכישת דירה ביוון, ולמה הן כל כך חשובות? | האם משלמים מע״מ של 24% על דירה חדשה מקבלן ביוון? | כמה כסף צריך להשקיע כדי לקבל גולדן ויזה ביוון? | האם כדאי לקנות במזומן או עם משכנתא ביוון? | כמה שווה ההון העצמי הנדרש בשקלים, ואיך שער החליפין משפיע? | צרו איתנו קשר | ההזדמנויות הטובות ביותר באתונה נסגרות הרבה לפני שהן מגיעות לכותרות. השאירו פרטים ונקפוץ לכם למייל רק כשיש משהו שבאמת שווה את הזמן שלכם. | מה קורה ביום שאחרי קבלת מפתח? | 18.08.2026 | 19:00 | ההרשמה בחינם | לא תודה
- Tables: 4 rows: €150,000, €60,000, €13,500, €73,500, €250,000, €100,000 || 7 rows: מס רכישה (FMA), 3.09%, מהערך האובייקטיבי או מחיר הרכישה, הגבוה , מע״מ על נכס חדש, 24% / מושעה, מושעה עד 31.12.2026; הקבלן גובה 3.09% במ || 4 rows: מדרגה עליונה, €800,000, אטיקה (כולל אתונה), מחוז סלוניקי, מיקונו, מדרגה אזורית, €400,000, כל שאר אזורי יוון. נכס יחיד, מינימום 120 || 5 rows: שיעור מימון, 50% עד 65% משווי הנכס היווני, תלוי בשווי ובמשכון הנכס הישראלי, מטבע ההלוואה, יורו – תואם להכנסות מהנכס, שקל – נוצרת חשיפה למט״ח

### Q_nadlanacademy

- URL: https://nadlan-academy.co.il/השקעות-נדלן-ביוון-המדריך-המלא/ (fetched 2026-10-22 16:05:30 UTC, 144635 bytes raw HTML)
- Title tag: השקעות נדל"ן ביוון: המדריך המלא למשקיע הישראלי (2026)
- Meta description: המדריך המלא להשקעות נדל"ן ביוון למשקיע הישראלי - מחירים, תשואות, ויזת זהב, מיסוי ותהליך רכישה. כל מה שצריך לדעת לפני שמשקיעים ב-2026.
- H1: השקעות נדל"ן ביוון: המדריך המלא למשקיע הישראלי (2026)
- Breadcrumb: דף הבית > השקעות נדל&quot;ן ביוון: המדריך המלא למשקיע הישראלי (2026)
- Dates: published 2026-04-23T11:15:37+00:00, modified 2026-05-07T10:47:57+00:00
- Author in schema: Samuel
- Schema types: Article, BreadcrumbList, ImageObject, Organization, Person, WebPage, WebSite
- Main-content words: 1648; numeric tokens: 116; tables: 1; images in content: 23 (no alt: 2); iframes/video: none; forms: 1; FAQ-schema questions: 0
- Links in content: internal 46 (whole page 76), external 0 (-); WhatsApp links 0; tel/mail 0
- H2/H3 outline (61): למה דווקא יוון? | מחירים תחרותיים — אבל כבר לא "בשפל" | תשואות גבוהות לעומת ישראל | חברה באיחוד האירופי — יציבות משפטית ומטבעית | אמנת מס עם ישראל | קרבה גיאוגרפית ותרבותית | אזורים מומלצים להשקעה ב-2026 | אתונה – הבחירה הראשית | סלוניקי – הזדמנות שעדיין פחות מוכרת | האיים – פוטנציאל גבוה, ניהול מורכב | ויזת הזהב – המצב המעודכן ל-2026 | מה היא מעניקה? | סכומי ההשקעה הנדרשים (בתוקף מאוגוסט 2024): | תהליך הרכישה | שלב 1: מספר מס יווני (AFM) | שלב 2: פתיחת חשבון בנק ביוון | שלב 3: בדיקת נאותות ועורך דין | שלב 4: חתימת חוזה ותשלום | עלויות העסקה (מעבר למחיר הנכס): | מיסוי – מה משלמים? | מס הכנסה על שכירות ביוון: | מס רווחי הון: | אמנת המס עם ישראל: | שכירות קצרת מועד (Airbnb) – הרגולציה מתהדקת | ניהול הנכס מרחוק | הסיכונים שחייבים לדעת | 1. מחירים שכבר עלו – ציפיות ריאליות | 2. בירוקרטיה יוונית – מציאות ולא מיתוס | 3. נכסים עם בעיות בעלות | 4. עונתיות חדה באיים | 5. עיכובים בוויזת הזהב | 6. רגולציית Airbnb | כמה כסף צריך ב-2026? | שאלות חשובות לפני שמשקיעים | סיכום: האם יוון כדאית ב-2026? | אהבתם? שתפו | צוות נדל"ן אקדמי | צרו קשר | עוד באותו נושא | אתונה 2026: המדריך האנציקלופדי להשקעות נדל"ן בבירה היוונית (חלק ב')
- Tables: 7 rows: סוג נכס, אזור, מחיר משוער

### Y_nadlanmaster_crete

- URL: https://www.nadlanmaster.co.il/נדלן-בכרתים/ (fetched 2026-10-22 16:10:30 UTC, 207028 bytes raw HTML)
- Title tag: השקעות נדלן בכרתים ב-2026 (מדריך מקיף, נתונים ודירות להשקעה)
- Meta description: נדל"ן בכרתים - מדריך מקיף על השקעות נדלן באי כרתים שביוון. מידע, נתונים על שוק הנדל"ן באי, דירות להשקעה בכרתים, בתים למכירה והזדמנויות >>
- H1: השקעות נדל"ן בכרתים
- Breadcrumb: השקעות נדל"ן בכרתים > מאת: מערכת נדלן מאסטר
- Dates: published 2020-07-19T06:07:27+00:00, modified 2026-01-18T09:42:54+00:00
- Author in schema: none
- Schema types: ImageObject, Organization, WebPage, WebSite
- Main-content words: 1174; numeric tokens: 31; tables: 0; images in content: 21 (no alt: 2); iframes/video: https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d834131.7222285713!2d25.472526756682896!3d35.24811883059619!2m3!1f0; forms: 2; FAQ-schema questions: 0
- Links in content: internal 38 (whole page 325), external 1 (he.wikipedia.org); WhatsApp links 2; tel/mail 1
- H2/H3 outline (9): מדריך למשקיעי נדל"ן באי כרתים בשנת 2026 | קצת היסטוריה לפני שמתחילים | למה כדאי להשקיע בנדל"ן בכרתים דווקא עכשיו? | שיטת המיסוי בכרתים ושיעורי התשואה הצפויים | מחירי נדל"ן בכרתים בשנת 2026 | היכן כדאי להשקיע בנדל"ן באי כרתים? | איך קונים נדל"ן בכרתים? | למידע על הזדמנויות השקעה מומלצות בכרתים – השאירו פרטיכם בטופס | כרתים – מפה:

### Z_newgreece_athens

- URL: https://new-greece.co.il/apartments-for-sale-in-athens/ (fetched 2026-10-22 16:10:31 UTC, 670603 bytes raw HTML)
- Title tag: דירות למכירה באתונה - יוון החדשה - דירות ובתים ביוון
- Meta description: בעוד שאתונה ממשיכה למשוך מבקרים ומתפתחת, עכשיו זה רגע טוב לשקול השקעה ברכישת דירה. אז איך עושים זאת ומה חשוב לדעת. המומחים שלנו ישמחו לעזור. היכנסו>
- H1: דירות למכירה באתונה
- Breadcrumb: Home > דירות למכירה באתונה
- Dates: published 2023-05-09T06:37:44+00:00, modified 2023-05-09T07:28:07+00:00
- Author in schema: יוון החדשה
- Schema types: Article, BreadcrumbList, ImageObject, Organization, Person, WebPage, WebSite
- Main-content words: 2732; numeric tokens: 15; tables: 0; images in content: 20 (no alt: 1); iframes/video: none; forms: 1; FAQ-schema questions: 0
- Links in content: internal 0 (whole page 86), external 0 (-); WhatsApp links 0; tel/mail 1
- H2/H3 outline (13): המצב הנוכחי של שוק הנדל”ן באתונה, מגמות שוק, מדדי צמיחה ועניין בקרב משקיעים | השכונות המבוקשות ביותר באתונה להשקעה בנדל”ן, המאפיינים הייחודיים ובפוטנציאל ההשקעה שלהן | מדד מחירי הדירות בשכונה: 5/5 | מדד מחירי הדירות בשכונה: 4.5/5 | מדד מחירי הדירות בשכונה: 4/5 | מדד מחירי הדירות בשכונה: 3/5 | מדד מחירי הדירות בשכונה: 3.5/5 | הזדמנויות השקעה בדירות באתונה | ההיבטים המשפטיים והרגולטוריים | מיסים | השכרת נכס דרך AIRBNB – כל המידע | טיפים להשקעה נכונה בדירות להשכרה באתונה | לסיכום

### N_justice_pricelist

- URL: https://jus-tice.co.il/greece-price-list/ (fetched 2026-10-22 16:05:20 UTC, 212310 bytes raw HTML)
- Title tag: מחירי דירות ביוון 2026: כמה עולה דירה? מ-1,500 אירו למ"ר
- Meta description: מחירי דירות ביוון לפי אזור: בסלוניקי ובכרתים מ-1,500 אירו למ"ר, דירת 3 חדרים במרכז אתונה 140 עד 280 אלף אירו, עלויות נלוות לרכישה ומה בודקים לפני שקונים.
- H1: מחירי דירות ביוון 2026: כמה עולה דירה ביוון לפי אזור
- Breadcrumb: ראשי > Articles > מקרקעין | נדל"ן > מחירי דירות ביוון 2026: כמה עולה דירה ביוון לפי אזור > עמוד הבית > עורך דין בחו״ל > עורך דין ביוון > עמוד הבית
- Dates: published 2025-07-06T09:18:36+00:00, modified 2026-07-25T11:19:42+00:00
- Author in schema: Jus-Tice.co.il
- Schema types: Article, BreadcrumbList, ImageObject, Organization, WebPage, WebSite
- Main-content words: 12319; numeric tokens: 604; tables: 1; images in content: 2 (no alt: 0); iframes/video: none; forms: 0; FAQ-schema questions: 0
- Links in content: internal 43 (whole page 193), external 2 (jus-tice.com); WhatsApp links 1; tel/mail 4
- H2/H3 outline (19): כמה עולה דירה ביוון? | אתונה (Athens – Αθήνα) | סלוניקי (Thessaloniki – Θεσσαλονίκη) | כרתים (Crete – Κρήτη) | רודוס (Rhodes – Ρόδος) | לפקדה (Lefkada – Λευκάδα) | קורפו (Corfu – Κέρκυρα) | האיים הקיקלאדיים (Cyclades – Κυκλάδες) | פלופונס (Peloponnese – Πελοπόννησος) | חלקידיקי (Halkidiki – Χαλκιδική) | אגריניו / פטראס / זקינתוס (Agrinio / Patras / Zakynthos – Αγρίνιο / Πάτρα / Ζάκυνθος) | ניתוח תשואה (ROI) בהשקעות נדל"ן: השכרה קצרה מול ארוכה | רכישת נכס ביוון, תהליך, חוקים לזרים ועלויות | הערת מערכת | צריכים בדיקה אישית בתחום מקרקעין | נדל"ן? | מדריכים משפטיים קשורים | קניית נכס בחו"ל: המדריך לישראלים, שלב אחר שלב | מחירי דירות בקפריסין 2026: כמה עולה דירה לפי מחוז | השקעות נדל"ן בפורטו: המדריך לישראלים
- Tables: 17 rows: אזור, מחיר למ"ר (אירו), דירת 80 מ"ר (הערכה), למי זה מתאים

### N2_justice_buying

- URL: https://jus-tice.co.il/buying-property-in-greece/ (fetched 2026-10-22 16:05:22 UTC, 418391 bytes raw HTML)
- Title tag: הליך רכישת דירה ביוון: שלב אחר שלב מול הרשויות היווניות | Jus-Tice
- Meta description: קניית דירה או בית ביוון: כמה עולה דירה ביוון, מס רכישה והוצאות נלוות, שלבי העסקה, בדיקות משפטיות וליווי עורך דין מקומי לישראלים.
- H1: קניית דירה ביוון: מחירים, מיסים והליך הרכישה לישראלים
- Breadcrumb: ראשי > Articles > מקרקעין | נדל"ן > הליך רכישת דירה ביוון: שלב אחר שלב מול הרשויות היווניות > עמוד הבית > עורך דין בחו״ל > עורך דין ביוון > עמוד הבית
- Dates: published 2023-03-21T19:29:06+00:00, modified 2026-09-23T17:00:46+00:00
- Author in schema: Jus-Tice.co.il
- Schema types: Article, BreadcrumbList, ImageObject, Organization, WebPage, WebSite
- Main-content words: 29570; numeric tokens: 842; tables: 1; images in content: 1 (no alt: 0); iframes/video: none; forms: 0; FAQ-schema questions: 0
- Links in content: internal 47 (whole page 197), external 2 (jus-tice.com); WhatsApp links 1; tel/mail 4
- H2/H3 outline (50): תהליך רכישת נכס ביוון: מדריך מקיף לישראלים | מיקומים מרכזיים להשקעות נכסים ביוון | גורמים שיש לקחת בחשבון בעת ​​בחירת נכס | רכישת נכס ביוון: שיקולים חשובים | השקעה ביוון | בחירת המיקום הטוב ביותר להשקעה בנכס | צפייה והזמנת נכס | חוזים, תשלומים ורישום נכסים | התאוששות כלכלית | הזדמנויות נדל"ן | מגזר התיירות | תושבות באמצעות השקעות נכסים | קרבה גיאוגרפית ותרבותית | איתור נכסים | אַתוּנָה יתרונות: | חסרונות: | סלוניקי יתרונות: | איי יוון (למשל מיקונוס, סנטוריני, כרתים, רודוס, קורפו) יתרונות: | שירותים נוספים לישראלים | טיפים לרכישת דירה ביוון | חוקים בינלאומיים הרלוונטיים לנדל"ן ביוון | סוגי זכויות על קרקע | מערכת רישום מקרקעין יוון | זכויות במקרקעין שאינן חייבות ברישום ביוון | משרדי רישום מקרקעין הפועלים ביוון | הוכחת בעלות על מקרקעין רשומים ביוון | רישום אלקטרוני של זכות בעלות | המסמכים הדרושים לרישום זכויות הבעלות ביוון הם: | הגבלות גישה לציבור במרשם המקרקעין ביוון | שוק הנדל"ן | מס העברות | מס ערך מוסף | מיסים אחרים | שכירות של חצרים עסקיים | סוגי שכירות לעסקים | העלאת שכר הדירה ביוון | זכותו של השוכר למכור או להשכרת משנה | ביטוח נכס יוון | תיקונים בנכס יוון | מיסים שישולמו על שכר דירה על ידי בעל הבית או השוכר של חוזה שכירות עסקי ביוון
- Tables: 15 rows: שלב, פעולה, הערות/מיקום

### N3_justice_investing

- URL: https://jus-tice.co.il/investing-in-greece-real-estate/ (fetched 2026-10-22 16:05:25 UTC, 117905 bytes raw HTML)
- Title tag: נדל"ן ביוון להשקעה: תשואות 5%-10% לפי אזור וסיכונים | Jus-Tice
- Meta description: השקעה בנדל"ן ביוון לישראלים: תשואה נטו של 5% עד 10% לפי מיקום, אזורים מניבים ומסוכנים, מס רכישה ומס שבח מקומי, מלכודות בעסקה ומה בודק עורך דין לפני חתימה.
- H1: תשואות נדל"ן ביוון לפי אזור: מה מניב ומה מסוכן
- Breadcrumb: ראשי > Articles > מקרקעין | נדל"ן > תשואות נדל"ן ביוון לפי אזור: מה מניב ומה מסוכן > עמוד הבית > עורך דין בחו״ל > עורך דין ביוון > עמוד הבית
- Dates: published 2025-01-19T16:36:57+00:00, modified 2026-07-15T15:18:22+00:00
- Author in schema: Jus-Tice.co.il
- Schema types: Article, BreadcrumbList, ImageObject, Organization, WebPage, WebSite
- Main-content words: 3192; numeric tokens: 66; tables: 0; images in content: 1 (no alt: 0); iframes/video: none; forms: 0; FAQ-schema questions: 0
- Links in content: internal 43 (whole page 189), external 2 (jus-tice.com); WhatsApp links 1; tel/mail 4
- H2/H3 outline (46): סקירת רקע היסטורי וכלכלי | המשבר הכלכלי 2008-2017 | ההתאוששות מאז 2017 | השפעת מגפת הקורונה (COVID-19) והשלכותיה | נתוני ביקוש והיצע | עליות מחירים ותנודות צפויות | השפעת התיירות | המשבר הכלכלי כתשתית הזדמנות | חוקי "גולדן ויזה" והקלות למשקיעים זרים | מניעי ההשקעה והסיבות להתעניינות | מיסוי, רגולציה והסכמי אמנת מס | שוק המשכנתאות והיקף ההלוואות לזרים | חסמי שפה ותרבות | סוגיות רעידות אדמה והיבטים סביבתיים | תחרות בין משקיעים זרים ומקומיים | מיסוי על רכישה, השכרה ומכירה | הכנסה משכירות, פוטנציאל ותמחור | רווחי הון ורווחיות לטווח ארוך | השוואה לנדל"ן בישראל: פערי תשואה ועלויות | אזורים ואיים מרכזיים להשקעה | אתונה, עיר הבירה והלב הכלכלי | סלוניקי, מוקד צעירים וסטודנטים | אזורי “פריים” לעומת אזורים מתפתחים | איתור הנכס ובדיקת נאותות | ליווי עורך דין יווני והסכמי מכר | רישום בטאבו, מיסוי ודיווחים (TAXIS) | אפשרויות מימון ביוון ובישראל | התנאים לקבלת אשראי והבדלי ריבית | ניהול שוטף, השכרה לטווח ארוך | Airbnb והשכרות לטווח קצר | התמודדות עם נזקים ותקלות | שיפוץ והשבחה, כיצד למקסם את ערך הנכס | פרויקטים יזמיים לבנייה חדשה | רכישת מגרשים חקלאיים או נכסים מסחריים | מגמות כלכליות צפויות | תיירות, תשתיות והתחדשות עירונית | תחזיות מחירים ורמת תשואה | הזדמנויות נוספות בשוק המקומי והגלובלי | האם משתלם להשקיע ביוון? | הבהרה משפטית

### W_ours_global_greece

- URL: https://nad-lan.co.il/global/greece/ (fetched 2026-10-22 16:10:28 UTC, 179296 bytes raw HTML)
- Title tag: השקעות נדל"ן ביוון: אתונה, ויזת זהב, מחירים והמדריך המלא למשקיע הישראלי | נדלן
- Meta description: המדריך המלא להשקעה בדירה ביוון: מחירי אתונה, ויזת הזהב האירופית, מס רכישה 3.09%, תשואות שכירות, תהליך הרכישה ופרויקטים להמחשה בתלת ממד ועל המפה.
- H1: נדלן / השקעות נדל"ן ביוון: העולם המלא למשקיע
- Breadcrumb: נדלן > השקעות בחו"ל > יוון
- Dates: published n/a, modified n/a
- Author in schema: none
- Schema types: Answer, BreadcrumbList, FAQPage, GeoCoordinates, ImageObject, Organization, Place, PostalAddress, Question, WebSite
- Main-content words: 453; numeric tokens: 20; tables: 0; images in content: 0 (no alt: 0); iframes/video: none; forms: 1; FAQ-schema questions: 3
- Links in content: internal 8 (whole page 11), external 0 (-); WhatsApp links 1; tel/mail 1
- H2/H3 outline (9): המספרים של יוון | פרויקטים להמחשה: לחקור בתלת ממד ועל המפה | על המפה | תהליך הרכישה: עורך דין, נוטריון ומספר מס | ויזת הזהב: מה באמת מקבלים | הסיכונים שאסור להתעלם מהם | הכלים שלנו עובדים גם כאן | שאלות נפוצות | רוצים ליווי בהשקעה ביוון?
- FAQ schema questions: האם 250 אלף אירו עדיין מספיקים לוויזת זהב? | כמה עולה להחזיק דירה באתונה? | אתונה או האיים?

### O_ours_str_greece

- URL: https://nad-lan.co.il/short-term-rentals-abroad/short-term-rentals-greece/ (fetched 2026-10-22 16:05:26 UTC, 224665 bytes raw HTML)
- Title tag: השכרה לטווח קצר ביוון | נדלן חכם
- Meta description: מדריך 2026 למשקיע ישראלי ביוון: רגולציית STR, חוק 1 באוקטובר 2025, מסים, ויזת זהב מ-250 אלף יורו, מחירים באתונה וסלוניקי, תשואה נטו.
- H1: השכרה לטווח קצר ביוון למשקיע ישראלי: רגולציה, מסים, מחירים ותהליך רכישה
- Breadcrumb: none
- Dates: published 2026-05-29T14:58:39+00:00, modified 2026-06-15T15:13:39+00:00
- Author in schema: none
- Schema types: Article, ImageObject, Organization, Person, PostalAddress, WebPage, WebSite
- Main-content words: 2218; numeric tokens: 103; tables: 1; images in content: 0 (no alt: 0); iframes/video: none; forms: 0; FAQ-schema questions: 0
- Links in content: internal 12 (whole page 135), external 0 (-); WhatsApp links 1; tel/mail 2
- H2/H3 outline (19): פתיחה | רגולציית השכרה לטווח קצר ביוון | טבלת בדיקה מהירה למשקיע | תשואות ומחירים | מיסוי מקומי ביוון והקשר למס בישראל | תהליך רכישה לזר | אזורים מומלצים לבדיקה | טעויות נפוצות של משקיעים ישראלים | שאלות נפוצות | האם ישראלי יכול לקנות דירה ביוון? | האם כל דירה ביוון יכולה לשמש להשכרה לטווח קצר? | האם יש הקפאת רישום חדש באתונה? | כמה מס משלמים ביוון על השכרה קצרה? | האם צריך לשלם מס גם בישראל? | מהו הנתון הכי חשוב לפני רכישה להשכרה קצרה? | תגיות מוצעות | מקורות |  | צריכים ליווי משפטי לעסקת נדל"ן?
- Tables: 10 rows: נושא, כלל עדכני שנבדק, משמעות למשקיע ישראלי

### X_ours_str_hub

- URL: https://nad-lan.co.il/short-term-rentals-abroad/ (fetched 2026-10-22 16:10:29 UTC, 233132 bytes raw HTML)
- Title tag: השקעת Airbnb בחו״ל 2026: השוואת יעדים וסיכונים | nad-lan
- Meta description: השקעת Airbnb בחו״ל ב-2026: איך משווים יעד, רגולציה, תפוסה, מסים, ניהול וסיכון מטבע לפני רכישת דירה להשכרה לטווח קצר.
- H1: השקעת Airbnb בחו״ל - השוואת יעדים 2026
- Breadcrumb: none
- Dates: published 2026-05-28T21:27:25+00:00, modified 2026-06-03T05:28:30+00:00
- Author in schema: none
- Schema types: ImageObject, Organization, WebPage, WebSite
- Main-content words: 1905; numeric tokens: 131; tables: 1; images in content: 0 (no alt: 0); iframes/video: none; forms: 0; FAQ-schema questions: 0
- Links in content: internal 16 (whole page 139), external 0 (-); WhatsApp links 1; tel/mail 1
- H2/H3 outline (22): למה דווקא Airbnb והשכרה קצרת טווח? | הגל הרגולטורי של 2025-2026: למה זה רגע מכריע | שמונה מוקשים שמשקיעים ישראלים נתקלים בהם - בסדר תכיפות יורד | איך לבחור - מסגרת ההחלטה בארבעה צירים | המנוע לדירוג ראשוני | איזה יעד מתאים לכם? | השוואה אמיתית - שבעה יעדים, נתונים מאומתים 2026 | השקעת נדל״ן Airbnb בחו״ל - המדריך המלא ל-2026 | השוואה לצד-צד | שבע אזהרות שמשקיעים ישראלים מתחרטים שלא ידעו | מבנה עסקה טיפוסית בחו״ל - שמונה שלבים | מס בישראל על הכנסה מנדל״ן בחו״ל | מקורות ואימותים | שאלות נפוצות | מה היעד הזול ביותר להיכנס? | מה היעד הבטוח ביותר רגולטורית? | למה דובאי מבטיחה 9-12% תשואה ויש שנותנים פחות? | האם ויזת זהב יוון עדיין רלוונטית להשקעה? | מה עושים אם המדינה ישימה חוק חדש מחר? | מאמר מעמיק לכל ארץ | השכרה לטווח קצר בפורטוגל למשקיע הישראלי | מדריכי המדינות - השכרה לטווח קצר בחו"ל
- Tables: 1 rows: יעד, תשואה ברוטו, סף כניסה (€), רישיון STR, מס שכירות, שינוי רגולציה 2025-26

### U_ours_koukaki

- URL: https://nad-lan.co.il/global/project/koukaki-athens-residence/ (fetched 2026-10-22 16:05:35 UTC, 231210 bytes raw HTML)
- Title tag: רזידנס קוקאקי - אתונה - נדלן
- Meta description: בניין בוטיק בשכונת קוקאקי שלרגלי האקרופוליס - השכונה המבוקשת ביותר באתונה לשכירות תיירותית ולצעירים: דירות 1-3 חדרים עם מרפסות, גג משותף עם נוף
- H1: רזידנס קוקאקי - אתונה
- Breadcrumb: דף הבית > רזידנס קוקאקי - אתונה
- Dates: published 2026-07-12T17:17:28+00:00, modified n/a
- Author in schema: none
- Schema types: ImageObject, Organization, WebPage, WebSite
- Main-content words: 178; numeric tokens: 6; tables: 0; images in content: 0 (no alt: 0); iframes/video: none; forms: 1; FAQ-schema questions: 0
- Links in content: internal 11 (whole page 138), external 0 (-); WhatsApp links 2; tel/mail 1
- H2/H3 outline (10): בחרו דירה מתוך הבניין | מתקנים ומה שמסביב | מה מסביב | רוצים לשמוע עוד על השקעה כזו? | קביעת פגישת ייעוץ | More posts | מחירי דירות דובאי 2026 | Acheter un appartement en Israel en 2026 : le guide complet | דירות יוקרה בישראל: המדריך המלא 2026 לרוכשים ולמשקיעים | Luxury Apartments in Israel: The Complete 2026 Guide for Foreign Buyers and Investors

### V_ours_glyfada

- URL: https://nad-lan.co.il/global/project/glyfada-coast-suites-athens/ (fetched 2026-10-22 16:05:36 UTC, 231379 bytes raw HTML)
- Title tag: גליפדה קוסט סוויטס - אתונה - נדלן
- Meta description: פרויקט יוקרה בגליפדה שעל הריביירה האתונאית, 300 מטר מהחוף: דירות 2-4 חדרים עם מרפסות שמש עמוקות, בריכה משותפת וחניון. האזור המועדף על משפחות ישראליות
- H1: גליפדה קוסט סוויטס - אתונה
- Breadcrumb: דף הבית > גליפדה קוסט סוויטס - אתונה
- Dates: published 2026-07-12T17:17:28+00:00, modified n/a
- Author in schema: none
- Schema types: ImageObject, Organization, WebPage, WebSite
- Main-content words: 171; numeric tokens: 7; tables: 0; images in content: 0 (no alt: 0); iframes/video: none; forms: 1; FAQ-schema questions: 0
- Links in content: internal 11 (whole page 138), external 0 (-); WhatsApp links 2; tel/mail 1
- H2/H3 outline (10): בחרו דירה מתוך הבניין | מתקנים ומה שמסביב | מה מסביב | רוצים לשמוע עוד על השקעה כזו? | קביעת פגישת ייעוץ | More posts | מחירי דירות דובאי 2026 | Acheter un appartement en Israel en 2026 : le guide complet | דירות יוקרה בישראל: המדריך המלא 2026 לרוכשים ולמשקיעים | Luxury Apartments in Israel: The Complete 2026 Guide for Foreign Buyers and Investors

## Appendix B. Reproduce

Scripts used (scratchpad, not committed): fetch.py (raw HTML, browser UA), analyze.py (stdlib HTML parser: title, meta, H1-H3, breadcrumb, JSON-LD types, tables, images/alt, forms, links, keyword counts), build_kw.py (CSV clustering), gen_sections.py (this file sections). Data files are all under this folder.
