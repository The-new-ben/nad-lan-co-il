# Money-first content strategy, nad-lan.co.il (HAD-435, 5.10.2026)

Built on: gsc-baseline.md, money-words.md, cannibalization.md, technical.md, competitors.md (same folder).
Status: **a plan, read-only work**. Nothing here was changed on the live site. Every item that changes a page goes
through the owner's normal path (design first, Maya QA where she coordinates, a new word from Ben before a release).
**Every 301 and every new URL needs Ben's explicit word.** No noindex / nofollow / Disallow anywhere in this plan.

## 0. The three sentences

1. The site earns from **names** (professionals and project names, 67% of clicks) and almost none of its **money
   category words** is on page 1 (desktop top 20: zero of 48 checked).
2. The fastest money is in clusters we already half-own: **Sde Dov** (14 core words, ~5,900 searches/month, CPC up to $30, positions 7-18
   split across our own URLs), **project names** (DUO, Rainbow, Dimri, Gindi, Ashira at 8-34) and **Kikar Hamedina** (the
   weakest SERP of all 48: social posts and 10-year-old news).
3. The biggest generic gap, **"new projects in {city}"** (60 words, 6,000 searches/month, CPC up to $10.65), has had
   no owner since the 25.8 purge and needs Ben's decision.

## 1. Rules this plan obeys

- **One word = one owner URL** (cannibalization.md section 3 is the owner table). New URLs only where the URL word
  audit (5.10 sitemap snapshot, `tools/gsc/url_word_audit.py --token`) shows no owner, or where Ben accepts the conflict.
- **Additive only**: enrich, retitle, relink. Merges keep every unique line of the loser.
- **The page research law of 3.10** applies to every new or rewritten page before a brief goes to ChatGPT: 1-5 owned
  intents, ownership check, a manual read of the top 4-5 competitor pages in full (URLs + times), what Google shows
  (PAA, AI answer or "absent"), original prose, research kept in the repo. This audit did steps 1-2 and a machine SERP
  sample (competitors.md); **the manual reads (step 3-4) are still to do per page.**
- Content-first rendered order, honesty law (unknown = omitted), language DNA blacklist, no source names on pages.

## 2. Hubs and spokes

### Hub 1 - Kikar Hamedina (start here; HAD-433)
**Hub:** /projects/hamedina/ (he) with /projects/hamedina-en|fr|ru|ar/ as hreflang twins. Indexed: he, fr, ar.
**Not indexed: en ("unknown to Google"), ru ("discovered, not indexed")**; each language page has 5 internal links.

**Owned words:** "מגדלי כיכר המדינה" (260/mo, $3.52), "פרויקט כיכר המדינה", "מגדלי כיכר המדינה מחירים / למכירה / אכלוס";
English "kikar hamedina towers" (320/mo in Israel, $2.42) belongs to /projects/hamedina-en/; "kikar hamedina" (260).
"כיכר המדינה" alone (5,400) is the square (shopping/place intent): do not chase it.

**Why it can win fast:** Google's top 10 for "מגדלי כיכר המדינה" has no portal and no project page (Facebook groups,
Instagram, Globes 2015, Ynet 2012, tlvonline). Google's AI answer cites Ashtrom, Wikipedia, Globes, Electra and the
city, and states "two towers of 40 floors and one of 37"; a fact-complete page with clear answers can become the cited
source.

**Spokes: sections on the hub, not new URLs.** URL word audit result: `hamedina` is owned by the 5 Kikar pages; `kikar`
by /tel-aviv-plans/kikar-atarim/ (another place); `handover` by 10 guide URLs; `occupancy` by
/real-estate-lawyer/form-4-occupancy-permit/; `deals` by /developer-deals/. **Every spoke slug HAD-433 would need
breaks the URL law**, and none of the spoke intents has measurable search volume (DataForSEO: "כיכר המדינה אכלוס /
מחירים / דירות" = no volume). So each spoke is a section with its own anchor id on all five pages, built from the
5.10 press facts (claim ids, no source names, "according to publications" kept where it applies):

| spoke (HAD-433) | where | facts | links out to the existing owner of the general word |
|---|---|---|---|
| Occupancy and handover | hub section `#occupancy` | P1 (permit expected end 2026, handover through Q1 2027), P6 (3 basements, 1,600+ spaces), P5 (community centre, school, kiosks) | /guides/common-property-handover/, /real-estate-lawyer/form-4-occupancy-permit/, /home-inspection/ |
| Deals tracker | hub section `#deals`, dated "updated on" | P10 (10-15 sold, ~₪65K/m² average, some above ₪80K/m², the 140 m² floor-38 deal), our V3 range | /tel-aviv-luxury-apartment-prices/, /tel-aviv-penthouse-prices/ |
| The builders and the build | hub section | P7 (Electra and Ashtrom, ~₪1.4B), P8 (earthworks, shoring, 7 floors/month), P9 (₪4.3B cost, credit line) | developer/contractor pages in the directory |
| Landowners' timeline and tax | hub section | P2 (about 250 landowners are the developers), P13 (many expected to wait 6-24 months before selling) | /real-estate-tax-advisor/capital-gains-tax-guide/ (owner of "מס שבח", 3,600/mo) gets a Kikar paragraph linking back |
| Renting at Kikar | hub section | P13 (owners who wait will live in or rent the apartment) | /my-rentals/ (rentals module), /property-management/ ("ניהול נכסים") |
| Rova 4 premium market | hub section | P12 (10-15% off the peak estimated; premium barely moved) | /north-tel-aviv/, /tel-aviv-apartment-prices/, optional new page N3 |
| Celebrity deals | **not on the sales pages** (HAD-433); a news item only after a legal check | P11, "according to publications" | - |

Plus an FAQ block (with FAQPage markup, already present on the page) answering what people and the AI answer ask:
how many towers/floors/apartments, who builds, when is occupancy, price per m², parking, who are the sellers.

**Links into the hub (the part that decides indexing and rank):**
- Sitewide link: change the anchor from "כיכר המדינה" to **"מגדלי כיכר המדינה"** (4,386 header/footer links today).
- Home (he): flagship card with that anchor. /en/, /ru/, /fr/, /ar/ homes: a card to their language twin
  (this is the fix for the unindexed en and ru pages).
- /projects/ (top of the Tel Aviv group), /new-projects/new-projects-tel-aviv/ (TLV list), /tel-aviv-apartment-prices/
  (Rova 4 paragraph), /tel-aviv-luxury-apartment-prices/, /luxury-tel-aviv/, /tel-aviv-penthouse-prices/,
  /north-tel-aviv/ and /north-tel-aviv/bavli/ (today an orphan with 212 impressions), the peer towers (DUO, Park
  Bavli, YOO, Einstein, H Infinity) in a "מגדלי יוקרה נוספים בתל אביב" block, and the English twins of those towers
  linking /projects/hamedina-en/.
- /home-inspection/: a short "בדק בית לדירה חדשה במגדל" paragraph naming the 2027 Kikar handover, linking the hub.

**The business behind it (HAD-433 item 3):** about 250 owners receive 453 apartments in 2027; many wait 6-24 months
before selling. The words that monetise that wave are already ours or the pros network's: בדק בית ($14/click),
ניהול נכסים, השכרה, עורך דין מקרקעין ($13), מתווך (broker minisites, HAD-394), listing (HAD-256).

### Hub 2 - Sde Dov (fix first: most money per hour of work)
**Hub:** /sde-dov/. **Spokes:** /sde-dov/prices/ (for-sale and price words), every project page (Rainbow, Dimri Yama,
Ashira, Gindi Vogue, First, Utopia, Zohi, Shikun Binui...), area pages (/sde-dov/merkaz/, /tzafon/, /eshkol/,
/marina/, /parks/, /transport/, /hotels/, /employment/, /institutions/), /tour/sde-dov/ (noindex by owner decision).
- Apply cannibalization.md family A: hub title without "מחירים ודירות למכירה"; prices page title with
  "דירות למכירה בשדה דב"; merkaz links the hub; /sde-dov-luxury-projects-2026/ merged (301 on Ben's word).
- Hub lists every project with its **Hebrew searched name as the anchor** ("גינדי ווג שדה דב", "דמרי ימה שדה דב",
  "אשירה שדה דב", "ריינבו תל אביב"); sitewide "Dimri Yama" anchor becomes Hebrew.
- **English twin of the hub (new page N2)**: "sde dov" 390/mo in Israel + 320/mo in the US at $26 CPC; today an
  English project page (ashira-en) ranks 17 for it. URL audit: `sde`/`dov` owned by the 45 /sde-dov/ URLs, so it is
  allowed **only as the hreflang twin of /sde-dov/** (same page, other language), slug on Ben's word.

### Hub 3 - New projects, Tel Aviv first
**Hub:** /projects/ (national: "פרויקטים חדשים", "דירות מקבלן", "דירות חדשות"). **City owner:**
/new-projects/new-projects-tel-aviv/ for "פרויקטים חדשים בתל אביב" (320/mo, $10.18); /new-projects/north-tel-aviv-new-projects/
for North TLV ($18/click). **Spokes:** every TLV project page.
- Add the live list of TLV projects (from the project DB) on top of the TLV guide (additive), plain H1, and point the
  TLV city filter on /projects/ to it with the exact anchor.
- /projects/ gets directory signals: counts per city as text, a server-rendered "all projects by city" index (fixes
  the 893 orphans, technical.md T1), a fixed sitewide anchor ("כל הפרויקטים976" today), and an FAQ answering the
  related searches (על הנייר, בשיווק, עד מיליון וחצי).

### Hub 4 - Pros services (highest CPCs; turns 2,847 directory pages into money pages)
| owner page (exists) | money words | the upgrade |
|---|---|---|
| /home-inspection/ (pos 60-68) | בדק בית 3,600 ($13.99), בדק בית מחיר 480 ($7.61) | guide + inspectors from the directory by city + "דירה חדשה מקבלן / מגדל" section (Kikar, Sde Dov handovers) |
| /real-estate-lawyer/ (pos 41-49) | עורך דין מקרקעין 1,600 ($12.98), עורך דין נדלן 590 ($13.82) | lawyers by city from the directory (the lawyer pool, no dual representation); sitewide anchor "עורך דין מקרקעין" instead of "בדיקה משפטית" |
| /real-estate-appraiser/ | שמאי מקרקעין 2,400 ($8.62) | appraisers by city; link the glossary "שמאי מכריע" (1,900) |
| /mortgage-calculator/ section | יועץ משכנתאות 3,600 ($12.77) | a section "יועצי משכנתאות" with directory links. A separate URL would carry `mortgage`, owned by 18 URLs: **conflict, not recommended** |
| /brokers/ | מתווך 720, מתווך נדלן 320, משרד תיווך 320 | broker platform (HAD-394) |

### Hub 5 - Investment
/investment/ owns all investment head words (השקעה נדלנית $22.79, השקעה בנדל"ן $30.21, דירות להשקעה $8.42).
Spokes: the 22 city investment pages, /investment-property-mortgage/, the yield calculator
(/investment-property-cashflow-calculator/, retitle to "מחשבון תשואה", 2,400/mo), /global/ for abroad.
Merge /investment/apartments-for-investment/ into the hub (301 on Ben's word, first proposed 25.8); fix the three
broken child links on the hub.

### Hub 6 - Urban renewal
/urban-renewal/ ("התחדשות עירונית" 8,100), /urban-renewal/pinui-binui/ ("פינוי בינוי" 9,900), /urban-renewal/map/
("מפת/מתחמי/פרויקטי פינוי בינוי"; already pos 11 with **one** internal link), TLV pages, /tel-aviv-plans/*, and the
urban-renewal project pages. Give the map sitewide-level links and a server-rendered compounds list per city.

### Hub 7 - Prices and valuation (already page 1, use it as the link engine)
The 29 city price pages rank 7-9 on average. /property-value-estimator/ is the #1 click page. Use the price pages
to push money pages: each gets a "פרויקטים חדשים ב{עיר}" block (links to the project pages = orphan fix + city
intent support), a link to the city investment page, and to the estimator with the anchor "הערכת שווי דירה".
Retitle the estimator (technical.md T5).

## 3. The top 10 pages to fix first (by money)

| # | page(s) | what to change | money words | evidence |
|---:|---|---|---|---|
| 1 | /sde-dov/ + /sde-dov/prices/ + /sde-dov/merkaz/ (+ merge /sde-dov-luxury-projects-2026/) | split the words (hub = projects, prices page = for sale), Hebrew project anchors, merkaz links hub | שדה דב 4,400; פרויקט(ים) שדה דב 670 at $14-30; for-sale 260 at $6-13 | cannibalization A |
| 2 | Sde Dov project pages: Gindi Vogue, Dimri Yama, Ashira, Rainbow (+ First, Utopia, Zohi) | Hebrew searched name first in title/H1, under ~60 chars; Dimri sitewide anchor in Hebrew | גינדי שדה דב 480 ($13.72), דמרי שדה דב 210 ($17.51), ריינבו תל אביב 480, אשירה 90 | money-words #20, #23-24, #29-30 |
| 3 | /projects/hamedina/ + 4 language twins | press facts as sections (P1-P13), FAQ, sitewide anchor "מגדלי כיכר המדינה", language homes link the twins (en/ru indexing) | מגדלי כיכר המדינה 260; kikar hamedina towers 320 | Hub 1; technical T3 |
| 4 | /property-value-estimator/ | title with "הערכת שווי דירה" (+ "בחינם" if true), answer-first lead, link from price pages | הערכת שווי דירה 590, בחינם 590, שמאות דירה 170 ($11.36) | #1 click page, title 23 chars |
| 5 | /new-projects/new-projects-tel-aviv/ (+ North TLV) | live TLV project list on top, plain H1, /projects/ TLV link points here | פרויקטים חדשים בתל אביב 320 ($10.18), פרויקט תל אביב 260 | cannibalization B |
| 6 | /projects/ | all-projects-by-city index (orphans), directory text, FAQ, fix "כל הפרויקטים976" | פרויקטים 1,600, פרויקטים חדשים 390, דירות מקבלן 210 | technical T1/T2 |
| 7 | /projects/duo-tel-aviv/ | answer the PAA (address, average price, what is DUO), progress block, Hebrew "מגדלי דואו" in title | duo 1,000 ($9.34), duo תל אביב 210 | #2 click page, pos 8-23 |
| 8 | /home-inspection/ | service hub with inspectors by city + new-tower handover section (Kikar/Sde Dov) | בדק בית 3,600 ($13.99) | pos 60-68 |
| 9 | /investment/ (+ merge apartments-for-investment) | one owner for all investment words, fix 3 broken links | 1,870/mo at $8-30 | cannibalization C |
| 10 | /real-estate-lawyer/ + /real-estate-appraiser/ | lawyers/appraisers by city from the directory; sitewide anchor "עורך דין מקרקעין" | 4,600/mo at $8.6-13.8 | Hub 4 |

Also in the first wave because they are free: the 83 broken hrefs (technical T4, incl. /mortgage-calculator/'s own
link to its reverse-mortgage child) and the money-page inlinks (/urban-renewal/map/ has one).

## 4. New pages to create (each needs Ben's word; research law steps 3-4 before any brief)

| id | page | owner word(s) and intent | volume / CPC | URL word audit (5.10 snapshot) | competes with an existing URL? |
|---|---|---|---|---|---|
| N1 | **City new-project pages** for the top cities (Jerusalem, Petah Tikva, Rishon LeZion, Ramat Gan, Haifa, Bat Yam, Netanya, Beer Sheva...) | "פרויקטים חדשים ב{עיר}": a list of the city's projects with status, developer, price where verified | 60 keywords, ~6,000/mo, CPC $3.4-10.65 | city tokens are already held (e.g. `jerusalem` 5 URLs: price page, investment page, commercial pages, light-rail article); `projects` is the /projects/ section; precedent /herzliya-projects/ | **YES**: /projects/ city filters, the city price pages; it also reverses part of the 25.8 purge. **Option A (no new URL, law-safe):** a server-rendered "פרויקטים חדשים ב{עיר}" section on each city price page (they rank 7-9). **Option B:** /{city}-projects/ like /herzliya-projects/, rich pages only, top 6 cities. Recommendation: A now, B only on Ben's word. |
| N2 | **English Sde Dov hub** (hreflang twin of /sde-dov/) | "sde dov", "sde dov tel aviv", "sde dov apartments for sale" | 390 IL + 320 US, CPC $6.84 / $25.97 | `sde`, `dov` owned by 45 /sde-dov/ URLs | **YES by token**, allowed only as the same page in English (hreflang pair). Slug on Ben's word. |
| N3 | Rova 4 / New North area page (optional) | "רובע 4 תל אביב", "הצפון החדש" (volume not measured yet: check first) | unknown | `rova` free; slug /north-tel-aviv/rova-4/ passes (no repeated word); `north` section owner is /north-tel-aviv/ | **Partly**: /north-tel-aviv/ (area hub), /tel-aviv-luxury-apartment-prices/. Only if the volume check shows demand. |
| N4 | Government-program guide ("דירה בהנחה / מחיר למשתכן: פרויקטים, הגרלות ומחירים") | "דירה בהנחה", "מחיר למשתכן" | 74,000 + 90,500, CPC $3.8 | `dira`, `behanacha`, `mechir`, `mishtaken` free; `affordable` held by /affordable-apartments-israel-2026/ | **YES (audience)**: /affordable-apartments-israel-2026/ and /3-room-apartment-690k-israel-2026/. Government and news own the SERP; honesty law: verified lottery data only. Long shot; owner's call. |
| N5 | Kikar spokes as URLs (occupancy, deals, landowners, renting) | - | no measurable volume | `hamedina`, `kikar`, `handover`, `occupancy`, `deals` all owned | **YES**: build as hub sections instead (Hub 1). Not recommended as URLs. |
| N6 | Mortgage-adviser page | "יועץ משכנתאות" | 3,600, $12.77 | `mortgage` owned by 18 URLs; `advisor` by 9 (tax-advisor cluster) | **YES**: build as a section of /mortgage-calculator/ instead. |

Not new pages but language twins worth adding: Hebrew/English pairing between /3-room-apartment-690k-israel-2026/
and /affordable-apartments-israel-2026/ (same story, no hreflang today).

## 5. Internal-link plan

**Sitewide (header/footer, ~4,400 pages):**
| link today | anchor today | change to |
|---|---|---|
| /projects/hamedina/ | כיכר המדינה | מגדלי כיכר המדינה |
| /real-estate-lawyer/ | בדיקה משפטית | עורך דין מקרקעין |
| /projects/dimri-yama-sde-dov/ | Dimri Yama | דמרי ימה שדה דב |
| /projects/ | כל הפרויקטים976 (glued) | פרויקטים חדשים (count as a separate element) |
| /projects/rainbow-tel-aviv/ | glued caption + title | ריינבו תל אביב |
| (add) /urban-renewal/map/ | - | מפת פינוי בינוי |

**Home (he):** keep the owner-approved title. Make sure the body links, with these exact anchors: פרויקטים חדשים ->
/projects/; פרויקטים חדשים בתל אביב -> TLV page; מגדלי כיכר המדינה -> Kikar; רובע שדה דב -> /sde-dov/; דירות למכירה
בשדה דב -> /sde-dov/prices/; הערכת שווי דירה -> estimator; נדל"ן להשקעה -> /investment/; בדק בית -> /home-inspection/.
**Language homes (/en/, /fr/, /ru/, /ar/):** a flagship block linking the language twins of Kikar, DUO, Rainbow,
Dimri Yama, Ashira, Gindi Vogue (fixes the unindexed Kikar en/ru pages).

**Neighbours (mesh):**
- Every project page: "more projects in {city}" (6 links, Hebrew names) and, for TLV luxury towers, "מגדלי יוקרה
  נוספים בתל אביב" (Kikar, DUO, Park Bavli, YOO, Einstein, H Infinity, Sde Dov flagships).
- Every city price page: "פרויקטים חדשים ב{עיר}" block, city investment page, estimator.
- Sde Dov area pages -> hub ("פרויקטים בשדה דב") and prices page ("דירות למכירה בשדה דב").
- Guides that own general words link to the hubs that apply them (handover guide -> Kikar #occupancy; capital-gains
  guide -> Kikar landowners section; /property-management/ -> rentals).
- Orphans: the all-projects-by-city index; /north-tel-aviv/bavli/, /north-tel-aviv/old-north/, /north-tel-aviv/shchunat-lamed/
  linked from /north-tel-aviv/; /construction-engineering-guide/ from the glossary hub; /property-value/luxury-apartments-tel-aviv/
  from /luxury-tel-aviv/ (or merged).

## 6. 30 / 60 / 90 days

Expected impact is an **estimate** from the CTR curve in money-words.md, assuming the change ships and Google
re-crawls; it is not a promise. Baseline: ~374 clicks per 28 days (6.9-3.10), ~90/week.

**Days 1-30: fix what we already half-own (no new URLs)**
- Sde Dov split (top-10 #1, #2), the project-name retitles, the sitewide anchor changes.
- Kikar: press-fact sections + FAQ on all five pages, language-home links (en/ru indexing), the Kikar anchor.
- The 83 broken hrefs; money-page inlinks (map, prices, TLV, North TLV, Herzliya, luxury).
- Estimator retitle.
- Expected: "שדה דב" from ~18 to ~8-12 (about +60-130 clicks/month at 4,400 searches), project names to page 1
  (+30-60/month), Kikar he/en to top 5 on 580 searches (+30-50/month). **Roughly +120-240 clicks/month by day 45-60**,
  and almost all of it on money words.

**Days 31-60: build the directory and the hubs**
- /projects/ all-projects-by-city index + "more projects in {city}" on project pages (orphans).
- TLV and North TLV pages with live project lists; city price pages get their "new projects" blocks (N1 option A).
- Pros hubs: /home-inspection/, /real-estate-lawyer/, /real-estate-appraiser/ with directory listings by city.
- Investment merge (on Ben's word) and the yield-calculator retitle.
- Ben decides: N1 option B (city project URLs), N2 (English Sde Dov twin), the 301 list.
- Expected: orphan project pages regain crawl and impressions (they already earned 6,500 impressions on sitemap
  discovery alone); pros words move from 40-68 toward 15-25 (clicks follow later at these CPCs).

**Days 61-90: expand where the data says**
- N2 English Sde Dov twin; N1 option B cities if approved (research law per page); N3 only if volume exists.
- Kikar deals tracker updated monthly; a handover-season content push in Hebrew and English (inspection, renting,
  management, selling timeline) linked to the hub and the pros network.
- Re-run this audit (same scripts; see below) and compare: money-word positions, clicks on money pages, orphans count.
- Expected by day 90: **600-800 clicks per 28 days** (from 374), with Sde Dov, project names, Kikar, the estimator and
  TLV projects carrying the increase; leads measured by the existing WhatsApp/lead events, not by clicks.

## 7. How to re-run (repo memory)

GSC: `python tools/gsc/gsc_api.py query --site sc-domain:nad-lan.co.il --start ... --end ... --dimensions query,page --out ...`.
Analysis scripts used for this audit are copied to `data/scripts/` (crawl.py = the polite crawler, gsc_analyze.py,
dfs_volume.py + dfs.py + serp_run.py = DataForSEO calls through the shared launcher, money.py, families.py,
serp_analyze.py, tech.py, plus the seed keyword lists). They read no secrets themselves; GSC and DataForSEO go
through `tools/gsc/gsc_api.py` and `agent-tools/dataforseo/run.cjs`. Paths inside them point at this folder and the
session scratchpad; adjust before re-use. DataForSEO spend: `data/dfs/dfs-costs.csv` (about $0.84 for this audit).
