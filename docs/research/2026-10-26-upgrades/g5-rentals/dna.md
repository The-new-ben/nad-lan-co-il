# G5 · "דירות להשכרה" / "דירה להשכרה": the owner page (research, spec, build; LOCAL ONLY, 26.10.2026)

Ben, 26.10.2026: for every keyword where we do not appear, a winning page at our level (tools, text, English, competitor DNA, SERP
and People also ask, a moat, tables, prices, data, visuals, the right title that harms no other page, an honesty statement).
Nothing here was deployed, posted or committed. Evidence classes: **code** (API, raw HTML, scripts), **eyes** (screenshots looked
at), **unverified** (said so).

## 0. Decision (short)
- **Owner page: a NEW page at `/דירות-להשכרה/`** (option c), a rentals hub: our real rental listings (live count and cards),
  official rent data by city, size and neighbourhood, the moat tool "כמה שכר דירה הוגן לדירה הזאת", the law and the tax.
- **Why not (a)/(b) on an existing URL:** no page owns the intent today. `/properties/?listing_type=rent` already prints H1
  "דירות להשכרה" but its canonical is `/properties/` (the owner of "דירות למכירה"), so it is not an indexable URL of its own and
  re-targeting `/properties/` would split the sale owner. `/my-rentals/` is a landlord's management tool (title "ניהול השכרות
  חינם לבעלי דירות"), `/buy-vs-rent/` + `/buy-or-rent/` are a decision calculator, `/glossary/דמי-שכירות-ראויים/` is an
  appraisal term (it gets "אומדן דמי שכירות" 53 impressions @30). None matches "I want a flat to rent / what does renting cost".
- **Slug passes the URL word law:** `url_word_audit.py --token` (live sitemap, 4,598 URLs): "דירות" 0 owners, "להשכרה" 0 owners
  (`url-audit.txt`). English candidates fail: "rent" 44 owners (`/buy-vs-rent/`, 12 commercial, 31 listings), "rental" 0 but
  "rentals" 8 (`/short-term-rentals-abroad/*`, same head word), "apartments" 8, "dirot" 1 (`/michraz-dirot/`). The site already
  serves Hebrew slugs (`/glossary/...`, `/projects/הדר-דירה-להשכיר/`). `/דירות-להשכרה/` answers 404 today (free).
- **Keyword guard:** with today's list it BLOCKS (no owner yet, rule 7: Ben names the owner). With the proposed owner set in a
  scratch copy, title / H1 / slug / meta are all OK; every outgoing anchor OK (`kw-guard.txt`).
- **Honest odds:** the head terms are an inventory SERP. With 11 listings we will not reach the top 10 for "דירות להשכרה" /
  "דירה להשכרה" in the coming months (my estimate: under 5%). The page is built to win the tail on the same URL (rent prices,
  rent calculator, guarantees, rental tax) and to be the deepest information page on the head-term SERP; section 10.

## 1. Keywords (DataForSEO keyword_overview, Israel 2376, 26.10.2026) and Search Console
Head: דירות להשכרה 27,100 (KD 27, CPC $0.37, commercial) · דירה להשכרה 27,100 (KD 19, transactional) · יד 2 דירות להשכרה 110,000
(navigational). Cities: פתח תקווה 8,100 · ירושלים 6,600 · אשדוד 5,400 · ראשון לציון / חיפה / חולון 4,400 · רמת גן / נתניה 3,600 ·
תל אביב 2,900 · באר שבע 1,900 · בת ים 1,600. Intents on the same page: חוזה שכירות 2,900 (owned de facto by
`/real-estate-lawyer/residential-lease-agreement/`) · שכירות לטווח ארוך 1,600 (KD 9) · השכרת דירה 1,000 · חוזה שכירות להורדה 720 ·
דמי מפתח 480 (KD 4) · דירות להשכרה ללא תיווך 480 · כתב ערבות לשכירות 320 · חוק שכירות הוגנת 320 · מס על שכר דירה 260 · מחשבון שכר
דירה 260 · מחשבון מדד שכר דירה 260 (cpi page) · מדד שכר דירה 140 · מחשבון שכירות 110 · מס הכנסה על שכר דירה 110 · מחירי שכירות 90
(CPC $18) · ערבות לשכירות 70 (CPC $19.65). English (Israel): apartments for rent tel aviv 590 · rent apartment israel 170 ·
apartments for rent in israel 170 · rent in israel 90. Raw: `_private-research/2026-10-26-upgrades/raw/g5/serp/kw-overview.json`.

Search Console (all-qp.csv, 90 days): not seen for either head term. Rent queries scatter over unrelated pages at low positions:
מחשבון שכר דירה (/buy-or-rent/ 5 @52, /buy-vs-rent/ 5 @77), בכמה להשכיר את הדירה שלי (/buy-or-rent/ 5 @80, /property-value-estimator/
2 @27), מחשבון שכירות (/property-value-estimator/ 2 @26), השכרת נכס (/investment/ 68 @74), אומדן דמי שכירות (glossary 53 @30).
No URL of ours competes for the head terms: the new page cannibalises nothing that has clicks.

## 2. What we have (code: live GETs 26.10.2026)
- **Real rent listings: 11** (`/properties/?listing_type=rent` lead: "11 מודעות"): 10 by Meital Katzir (licence 3131540) in Tel Aviv
  (Nofei Yam ×6, BSR Sarona ×2, Tzukei Aviv, Ramat Aviv), 1 owner listing in Kiryat Ata (3,400 ₪). Prices shown on 6 of 11. Two
  demo rent listings exist (`carmel-haifa-4r-rent-demo`, `florentin-tlv-2r-rent-demo`), labelled as demos on the archive.
- `/properties/` archive: title "דירות למכירה ולהשכרה בישראל - לוח נדל"ן", canonical `/properties/` also for `?listing_type=rent`.
- `/my-rentals/` (indexable, self canonical, NOT in the sitemap), `/post-listing/` ("פרסום דירה בחינם, למכירה או להשכרה"),
  `/real-estate-lawyer/residential-lease-agreement/` (lease guide, 2,573 words), `/cpi-calculator/`, `/buy-vs-rent/`, `/investment/`
  (rental-tax tracks table, U2), `/tabu-extract-check/`.
- Data already in the repo: the U2 fetch of all 74 government city files (rent + buy, version 20-08-2026) and the CBS 4.9 parse with
  Q2 2026; the rent files also carry **945 neighbourhood medians in 65 cities** that no page of ours used yet.

## 3. Google (DataForSEO SERP live advanced, google.co.il, Hebrew, 26.10.2026 11:30 to 11:52 UTC; raw `raw/g5/serp/`)
- **דירות להשכרה** (desktop and mobile): AI overview (loaded asynchronously): "search the listing boards ... Yad2", two local agencies
  (Rental Israel, Jerusalem; ג'י פי נכסים, Petah Tikva), then asks city, budget, rooms. Organic 2 to 20: **19 of 19 are
  yad2.co.il/rent/... filter URLs**. No People also ask.
- **דירה להשכרה**: Yad2 /realestate/rent · Madlan /for-rent/ישראל ("5349 דירות מחכות לך") · Homeless /rent/ · Yad2 Jerusalem ·
  Facebook group · isratowers (short let) · OnMap TA · Komo Jerusalem · renten.co.il (the government company "דירה להשכיר") · Madlan
  Petah Tikva; local pack; then Facebook groups, OnMap, kolhayechidot, subletisrael; **mako "האפליקציות שיעזרו לכם לשכור דירה" at
  #19 is the only article**. Related: city + "ללא תיווך" + Yad2/Madlan/Homeless brand searches, "פרסום דירה להשכרה". No PAA.
- Tail, same day: **מחירי שכירות** AIO = CBS H1-2026 figures via ynet (5,069; TA 7,398 ...) + Scoutr; organic Madlan, WeCheck (index
  calculator), Dirobot, CBS, yadata, hon, Scoutr, Yad2, renten. **שכר דירה ממוצע** AIO ynet + Scoutr; organic ynet, calcalist, CBS,
  Madlan, seenker (rent calculator), a Knesset PDF, Instagram, hon, nadlancenter. **כמה עולה לשכור דירה** AIO mako + flamingo +
  Scoutr + dironet; organic Yad2, Madlan, mako, renten, dirobot, WeCheck, seenker. **מחשבון שכר דירה**: hon, yadata, seenker, WeCheck,
  dirobot, qtax, finka, diffe-rent, taxo (all tools/guides, winnable). **חוק שכירות הוגנת** AIO sources nevo, gov.il, nadlancenter;
  organic insurance-israel, hon, Madlan blog, broker-re, **jus-tice.co.il #6 (Ben's other site)**, menivim, kolzchut, Knesset, a law
  firm. **ערבות לשכירות**: diffe-rent, WeCheck, Tel Aviv municipality form, kolzchut, law firms. **מס על שכר דירה**: kolzchut, gov.il,
  calcalist, meitav, law firms, wikipedia; **the only PAA found**: האם שכר דירה פטור ממס? · מהו גובה הפטור ממס על השכרת דירה בשנת
  2026? · האם ניתן לשלם מס הכנסה על שכר דירה באינטרנט? · מהו טופס בקשה לתשלום מס על הכנסה מהשכרת דירה? · איך משלמים מס הכנסה בגובה
  10% על שכר דירה? (+4 generic tax-file questions). **שכירות לטווח ארוך**: hon, ynet, renten, developers' rental sites. **השכרת דירה**:
  Yad2 ×8, sabras. **דירות להשכרה בתל אביב**: tlv2go, Madlan (Ramat Aviv), luxury-realestate-israel, Yad2, Facebook ×3, dorin, homeland
  (small brokers rank here).

## 4. Competitors read (raw HTML in `raw/g5/comp/`, DNA in `raw/g5/dna-extract.json`)
| Page | How the keyword sits | Depth | Tools, data | Why it ranks |
|---|---|---|---|---|
| Yad2 /realestate/rent | title "נדל״ן להשכרה \| אלפי מודעות חדשות בכל יום" | not readable: Radware page to scripts, **CAPTCHA in Ben's Chrome (not solved, not measured)** | inventory | inventory, brand, 19 filter URLs indexed |
| Madlan /for-rent/ישראל (Chrome read) | title "דירות להשכרה בישראל - 5,352 דירות מחכות לך", H1 "דירות להשכרה בכל הארץ" | ~1,366 words, all cards; 0 tables, 0 FAQ | filters, 108 pages, city/area/type link grid, blog teasers | live count + inventory + internal grid |
| Homeless /rent/ | title/H1 "דירות להשכרה", 55 repeats | 2,064 words, 2 tables, 155 images | huge filter form | inventory, exact-match repetition, SEO text block |
| OnMap /search/homes/rent | title "דירות להשכרה על המפה", H1 | 602 words, ItemList | map | inventory (951), map |
| Komo | H1 "דירות להשכרה" | 81 words | form | domain age |
| isratowers /rent/ | H1 "דירות להשכרה בישראל" | 553 words, RealEstateListing schema | listings | schema + listings |
| mako apps article (#19) | H1 about apps | 98 words in main | none | news domain |
| ynet 14892044 | rent-price story | 1,310 words, CBS H1-2026 for 18 cities | none | freshness, AIO source |
| Scoutr rent report | "דוח שכירות ישראל 2026" | 684 words, 1 table (18 cities, asking prices of 46,752 ads, daily) | Dataset schema, CSV | data freshness, AIO source |
| seenker rent calculator | "מחשבון שכירות" | 250 words, FAQPage 8 | JS calculator by neighbourhood | tool |
| dirobot | "מחשבון שווי נכס, שכירות" | 315 words, FAQ 20 | JS estimator | tool |
| hon מדד שכר דירה | index + calculator | 796 words, FAQ 9 | index calculator | tool, age |
| kolzchut guarantee | "הגבלת סכום הערובה..." | 1,116 words, FAQ 8, 1 table | none | authority |
| WeCheck fair-rental law | "חוק שכירות הוגנת" | 2,733 words | none | depth, brand |
| diffe-rent guarantees | "ערבויות לשכירות דירה" | 1,621 words, FAQ 3 | none | depth |
| jus-tice.co.il fair-rental-law-2017 | "חוק שכירות הוגנת: מה מותר ומה אסור" | 418 words | none | (Ben's site) |
No page in either SERP combines listings with official rent data, a fair-rent check, the law and the tax.

## 5. What Google wants
For the head terms: inventory (thousands of current listings), filters by city, rooms and price, a live count in the title, city
and type link grids. For the tail on the same intent: current official rent numbers by city and size (the AIO quotes CBS figures via
ynet), a calculator, and plain answers on guarantees, repairs, notices and tax.

## 6. Verified facts (official, with dates; every figure in rent.json carries its source)
| Fact | Source |
|---|---|
| Median rent by city and rooms 3/4/5/all, 22 quarters to April to June 2026 (TA 3 rooms 8,250; Israel 4 rooms 4,825); 945 neighbourhood medians (all sizes, last-year basis: TA 8,000 = the file's settlementPrice = all.ly) | data.nadlan.gov.il rent files, version 20-08-2026 (code, read 25.10.2026); "מחיר חציוני" on nadlan.gov.il (eyes, U2) |
| CBS average free-market rent, Q2 2026, 18 cities + 6 districts + Israel, groups 1-2 / 2.5-3 / 3.5-4 / 4.5+, sampling errors (Israel 5,085.5 ±15; TA 3.5-4 8,871.6 ±119) | CBS price bulletin table 4.9 (U2 parse); matches ynet 8.9.2026 (5,086 in Q2) |
| Rent index 120460: +3.2% over 12 months to 9.2026, +0.4% in 9.2026; 4.0% to 8.2024 | CBS API (code) |
| Fair-rental chapter 25א to 25טו: written lease; habitable flat (first schedule, 6 items); repairs 30 days / urgent 3 days (25ח); tenant pays rent, arnona, utilities, building upkeep; not fixed systems, building insurance, the landlord's broker (25ט); guarantee cap lower of a third of the term's rent and 3 months, use cases, notice, return in 60 days with fruits (25י); "other guarantor" = licensed credit, deposit-and-credit, stable-payment providers and insurers (**amendment 5786**, ס"ח תשפ"ו 362); notice of sale (25יא); options 90 / 60 days (25יב); cancellation clause only if mutual, 90 / 60 days (25יג); no contracting out (25יד); exclusions incl. ≤3 months, >10 years, rent above 20,000 ₪ updated each 1 January by CPI (25טו) | Nevo law00/5149 (current to 30.9.2026) and Wikisource (edited 30.9.2026), code |
| Personal guarantors not in the cap; relatives excluded; bank guarantee above the cap still valid at the bank | Kol Zchut (code) |
| Rental tax 2026: exemption 5,654 ₪ a month (same 2024 to 2026; 5,471 in 2023; 5,196 in 2022), partial to 11,308 (exempt = 11,308 − rent), monthly, on all flats; 10% track, no expenses, due 30.1.2027 for 2026; offset of rent paid up to 7,500 for a single-home owner (from 2023); regular track first bracket 31% (10% from 60); payment online with a tax file, else at the post bank with the voucher "בקשה לתשלום מס על הכנסה מהשכרת דירה" | Kol Zchut pages updated 22.2.2026 (code); gov.il guide 403 to scripts, its AIO summary agrees |
| "דירה להשכיר" is the government company for long-term rental tenders | renten.co.il (code) |
Our calculations (labelled "החישוב שלנו" on the page): CBS change vs Q2 2025, the tax table, the 10%-vs-exemption break-even
(about 6,740 ₪ a month under 60), neighbourhood × rooms estimates, the median carried to 9.2026 by the index.

## 7. Gaps we fill (nobody in the set has them together)
Official signed-contract numbers for 72 cities and 945 neighbourhoods (Scoutr: asking prices, 18 cities; ynet/CBS: 18 cities);
sampling errors; median vs average explained; the 5786 guarantee amendment; a fair-rent check that also checks the guarantee against
the law and the landlord's tax; real listings with licence lines on the same page; English.

## 8. Build spec (built locally)
**8.1 Title, H1, meta, slug** (kw-guard OK with the proposed owner):
- slug `/דירות-להשכרה/`
- SEO title (56): `דירות להשכרה 2026: מחירי שכירות בכל עיר ומחשבון שכר דירה`
- H1 (theme prints it from the page title): `דירות להשכרה: שכר הדירה בכל עיר ושכונה, הדירות באתר והחוק`
- meta (148): `מחפשים דירה להשכרה? שכר הדירה החציוני ב־72 ערים ו־945 שכונות, ממוצעי הלמ״ס, בדיקת שכר דירה הוגן, הערובה המותרת בחוק והמס למשכיר. נתונים רשמיים 2026.`

**8.2 Answer paragraph** (portal DNA, both head terms, the numbers): "מחפשים דירה להשכרה? שכר הדירה החציוני לדירת 4 חדרים בישראל עמד
על 4,825 ₪ באפריל עד יוני 2026, ובתל אביב-יפו על 10,500 ₪. כאן תמצאו ..." (preview/g5-page-content.html).

**8.3 Rendered order** (checked at 390 and 1280 px): H1 → answer → CTA row (בדקו את שכר הדירה · לדירות להשכרה באתר · פרסום מודעה
בחינם · הזכויות בחוק; 2×2 on phones) → the tool → the listings → today's numbers → 18 cities (V1) → 72 cities → neighbourhoods →
Tel Aviv → the index (V2) → the law (V3) → tax → checklists → long-term rental and key money → FAQ 24 → English → sources.
No WhatsApp CTA on this page on purpose (Brokers Law s.2(c): a "we'll find you a flat" line would be intermediation; contact is per
listing, by its publisher). The sitewide floating bar is unchanged.

**8.4 Tables (13, all from rent.json):** T1 today by size (gov median, CBS average ± error, change vs Q2 2025); T2 18 cities × 4
groups + total + yearly change; T3 6 districts; T4 72 cities × 3/4/5/all + the file's yearly change; T5 the dearest and cheapest 3
neighbourhoods in 8 cities; T6 Tel Aviv, all 61 neighbourhoods with our 3-room estimate; T7 the index, 12 months; T8 guarantee cap
by rent and lease length; T9 who pays what; T10 deadlines with sections; T11 tax tracks at 6 rents; T12 exemption ceiling 2022 to 2026;
plus the English table (18 cities). 1,144 cells.

**8.5 Infographics (3 SVG, Instruments, 420 wide, rtl, ≥12 px):** V1 average rent 3.5 to 4 rooms, 18 cities, sampling-error
whiskers and the national line; V2 the rent index's 12-month change every month since 8.2024 (4.0% → 3.2%); V3 the lease on a time
line by section. Plus the tool's own ruler + 12-quarter line.

**8.6 The moat: `rentfair`** (`plugins/nadlan-config/assets/instruments/tools/rentfair.js`, data `rent.json`, test
`tools/instruments/test_rentfair.js` ALL OK, 50+ checks incl. Kol Zchut's worked examples and the engine compute on every case).
See the component README for inputs and outputs. What it does that no competitor does: the asked rent against the *official*
median of the city, the neighbourhood and the size, with the CBS average and its error, AND the lease checked against the law
(guarantee cap, 60-day return, 3/30-day repairs, 90/60 notices, broker) AND the landlord's three tax tracks, in one screen.

**8.7 FAQ (24, FAQPage via the existing `nadlan_nli_faq()`):** the 5 rental PAA questions of "מס על שכר דירה" (the only PAA found),
the AIO questions of the price queries (כמה עולה לשכור דירה, ממוצע בתל אביב, העיר הזולה), related searches (ללא תיווך, מדד שכר דירה,
סיום חוזה), Kol Zchut's question set on guarantees, GSC queries (דמי תיווך שכירות), and the long-term / key-money intents.

**8.8 Listings:** `[nadlan_rent_listings limit="12"]` (instruments-snippet.md block 3): live count by city, the archive's cards with
the broker licence line, ItemList schema, "לכל המודעות באתר" to the filtered archive. Never typed into the page.

**8.9 English:** no English URL (no free English head word: rent 44, rentals 8, apartment 106 owners; demand 590 + 170 + 170 + 90 a
month). An English section inside the page (`lang="en" dir="ltr"`, `en-section.html`): what the two official numbers are, 18 cities
in NIS, the law in six lines, the landlord's tax. Later, if Ben wants: an `/en/` page once a free head word is chosen.

**8.10 Internal links out (10, all 200 without redirect):** /post-listing/, /my-rentals/, /cpi-calculator/, /real-estate-lawyer/
residential-lease-agreement/, /tabu-extract-check/, /investment/, /buy-vs-rent/ and the filtered archive. **In (proposal, Ben's word):**
the bare "דירות להשכרה" menu and grid links in `inc/home-v3.php` (lines 157, 215, 227, 749) and `inc/skin-a.php` (90) point to
`/properties/?listing_type=rent`; under the owner rule they should point to `/דירות-להשכרה/` (the guard blocks them otherwise). That is a
sitewide link change (pace law: his OK), not done.

## 9. Proof plan and the predicted honesty statement
Run `proof_run.py` (depth_proof + fact_coverage, unchanged shared tools) now on the local preview (`proof-predicted.md`,
`coverage-predicted.md`) and `proof_run.py --live` after publishing (`proof-after.md`). Predicted (local preview, raw HTML, 26.10.2026
14:07, 15 competitors measured; Yad2 not readable, Madlan by Chrome read):
- words **6,056** vs best 2,733 (WeCheck) · figures **1,365** vs 516 (Homeless) · tables **13** vs 2 · cells **1,144** vs 593 ·
  FAQ **24** vs 20 (Dirobot) · headings **45** vs 20 · official sources **4** vs 1 · fact coverage **38/38** vs best 12 (ynet).
- tools: the counter shows 1 vs 0, but seenker, Dirobot and hon have script calculators it cannot see: call it **a tie on tools**.
- **Behind:** pictures 24 vs 155 (Homeless) and 61 (OnMap), and above all **inventory: 11 listings vs 5,352 (Madlan), 951 (OnMap),
  thousands (Homeless, Yad2)**. That is what the head-term SERP ranks on.
- Caveats: the fact list was written by us from our own research, so 38/38 is expected; the live page adds the tool's no-script
  summary (one more table) and the theme's chrome.

## 10. Honest odds
- "דירות להשכרה" / "דירה להשכרה" top 10: under 5% in 6 months (my estimate). The SERP is an inventory SERP (Yad2 holds 19 of 20 on
  the plural); the only non-listing result is a 481-word mako article at #19. A position on page 2 to 3 is possible on the singular,
  not more, until we carry hundreds of listings.
- The tail on the same URL is winnable: "מחשבון שכר דירה" 260 (a tools SERP), "מחירי שכירות" 90 (CPC $18), "שכר דירה ממוצע", "כמה
  עולה לשכור דירה" (AIO quotes the same CBS numbers we print, for more cities), "מחשבון שכירות" 110; partly "שכירות לטווח ארוך" 1,600,
  "ערבות לשכירות", "מס על שכר דירה" (strong kolzchut/gov.il pages). Expect hundreds of impressions a month, not thousands, in the first
  quarter.
- The lever for the head term is inventory: more rent listings from brokers (the self-serve broker platform) and owners (`/post-listing/`).

## 11. What needs Ben
1. Yes or no on the new URL `/דירות-להשכרה/` as the owner of "דירות להשכרה" + "דירה להשכרה" (and whether it also holds "דירות להשכרה
   בתל אביב" 2,900 until a city page exists, HAD-602; the page has an H2 for it).
2. Yes or no on re-pointing the sitewide "דירות להשכרה" menu, grid and footer links (home-v3.php, skin-a.php) from the filtered archive to the new page (a sitewide change).
3. Findings, his call: (a) 4 Nofei Yam 5-room rent listings (base, -2, -3, -4) look like duplicates: two share the same title,
   cover photos repeat, two have no price; ask Meital. (b) two demo rent listings are in the live sitemap (indexing is his decision).
   (c) `/my-rentals/` is indexable but not in the sitemap. (d) jus-tice.co.il ranks #6 for "חוק שכירות הוגנת": a link from this page
   to it is a portfolio decision. (e) "דמי מפתח" (480, KD 4) has no owner: a candidate page.
4. Release slot through the coordinator (rentfair.js, rent.json, inc/rent-listings.php, instruments.php blocks).

## 12. Not verified
Yad2 (CAPTCHA), calcalist and the Madlan blog (403), the Tax Authority page (403; Kol Zchut used, the AIO summary agrees); the
CPI-updated value of the 20,000 ₪ ceiling (no Reshumot notice found: the page states the rule, not a 2026 number); the exact meaning
of the government file's yearly-change field (printed as "השינוי השנתי בקובץ"); the neighbourhood figures' period (matched to the
city's last-year figure on Tel Aviv and Haifa); how the theme renders the page (preview has no theme header/footer).

## 13. Files
In this folder: `dna.md` · `url-audit.txt` · `kw-guard.txt` + `kw_guard_run.py` · `write_g5_page.py` (dry run writes `preview/`,
`svg/`, `page-sources.md`, `en-section.html`; `--create` NOT run) · `build_listings_snapshot.py` + `listings.css` ·
`instruments-snippet.md` (release blocks, not applied) · `coverage-facts.json` + `proof_run.py` + `proof-predicted.md` +
`coverage-predicted.md` · `shot_preview.py` + `preview/shots/` (390 and 1280, report.json) · `build_ds_preview.py`.
Engine: `plugins/nadlan-config/assets/instruments/tools/rentfair.js`, `.../data/rent.json`, `tools/instruments/build_rent_data.py`,
`tools/instruments/test_rentfair.js`. Claude Design: `<scratchpad>/ds/project/components/RentalsHub/` (preview.html + README.md).
Raw: `C:\Users\777\nad-lan\_private-research\2026-10-26-upgrades\raw\g5\` (serp, comp, gov, index.txt, dna-extract.json).
