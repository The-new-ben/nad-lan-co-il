# Penthouse SEO: every "penthouse" search in Israel, led by the Kochav HaTzafon mini penthouse

INTERNAL research and plan file. Nothing here is published, deployed, committed or posted.
Built 21.10.2026 by an Opus 5.5 sub-agent (claude-opus-5-5) for the owner's goal of 21.10.2026: nad-lan.co.il ranks first for every existing "penthouse" search in Israel, Hebrew first, then English.

Pages in scope (the only three that may carry the word "penthouse", per the URL word law):
- Listing (HE): https://nad-lan.co.il/properties/kochav-hatzafon-new-mini-penthouse-for-sale/
- Listing (EN twin): https://nad-lan.co.il/en/brokers/meital-katzir/kochav-hatzafon-new-mini-penthouse-for-sale/
- Definitions: https://nad-lan.co.il/glossary/penthouse/
- Prices: https://nad-lan.co.il/tel-aviv-penthouse-prices/

Sources used (all reads; no writes anywhere):
- DataForSEO, MCP tool `mcp__dataforseo__api_request` (Labs keyword_ideas, keyword_suggestions, related_keywords, keyword_overview; Google Ads keywords_for_keywords; Google organic SERP live advanced). Seven Hebrew SERPs, two Israel-English SERPs and one Madlan content-parsing call went through the same account with the registry's script client `agent-tools/dataforseo/dfs.cjs`, to keep raw JSON out of the chat. All pulls on 21.10.2026 between 10:55 and 11:07 UTC. Spend: estimate under USD 0.20 (script calls printed USD 0.002 to 0.004 each; MCP calls do not print a cost).
- Google Search Console API, `sc-domain:nad-lan.co.il`, 21.7 to 19.10.2026, dimensions query+page (9,476 rows) and page (read only; token files never opened).
- `tools/gsc/url_word_audit.py` (live sitemaps, 4,571 URLs).
- Raw HTML of our four pages and 14 competitor pages, fetched 21.10.2026 at about 11:01 UTC; Madlan blocks plain fetches (HTTP 403), read through DataForSEO content parsing at 11:06:32 UTC.
- Tax Authority deals for Tel Aviv-Yafo (owner download of nadlan.gov.il data, file `Codex/2026-08-27/.../tlv-citywide/tlv-deals.csv`, 100,780 rows, downloaded 6.9.2026) with the neighbourhood logic of `tools/deals/build_tlv_neighborhoods.py`.
- The team's files: `docs/sales/kochav-ph/value-pack.md` (20.10), `strategy.md`, `campaign/keywords.md` (21.10).

Evidence classes: **[src]** read on the page itself; **[snippet]** seen only in a search result or AI answer; **[calc]** our calculation, formula given; **[api]** DataForSEO or Search Console number; **[owner]** the owner's or broker's word. A number that could not be found is written "not found".

Owner laws applied: no redirect, noindex, robots or sitemap proposal anywhere; no sitewide or mass change (only the four pages above); no new URL (every tool below is a block inside an existing page); no developer or project names on negative topics; long articles are written by the owner's ChatGPT from the brief in section 9, never by an agent.

---

## 0. Read first: what stops or shapes the work

1. **The listing's facts still disagree, now also inside its own code.** The Hebrew page's visible copy, title and meta say 197 m² built and an 80 m² terrace. Its JSON-LD carries two `floorSize` values, **197 and 190** [src, raw HTML 21.10]. Madlan's listing says 190 m² and 74 + 4 = 78 m² of balconies (value-pack.md). One number must be settled (Tabu extract, permit plan or the broker in writing) before any title or schema change below. Until then this file writes "[confirmed built m²]" and "[confirmed terrace m²]".
2. **Rent and yield on the listing: the owner must say which reading of his order applies.** His order of 20.10 forbids mentioning this home's tenancy and its rent. The Hebrew listing does not do that, but it carries an H3 "עלויות שוטפות, תשואה ומטבע", a line "שכר דירה ממוצע ותשואה (7.2026) כ-13,900 ש״ח לחודש; תשואה ברוטו של כ-3%" (neighbourhood averages) and a "שכירות להשוואה" table of other homes [src]. `campaign/keywords.md` reads the order as "the tenancy, the rent and the yield are never mentioned". Reported as a finding; nothing here changes it.
3. **The prices page has no prices.** /tel-aviv-penthouse-prices/ (1,827 words, one table) is a checklist of what to inspect. It never gives a price, a price per m² or a deal [src]. Google's AI answer for "פנטהאוז למכירה בתל אביב" already gives a number (prices "start at about 3.95 million ILS in the northern and southern neighbourhoods") [snippet]. Our page cannot win a price search without numbers.
4. **The definitions page is thin and stale.** /glossary/penthouse/ has about 982 words, no table, no FAQ markup, the title "פנטהאוז - נדלן", "עודכן יוני 2026", and it links to none of the other two pages [src]. Competitors that Google's AI answers cite are no better on facts (most are 2013 to 2017 articles), so the gap is open.
5. **nad-lan.co.il appears in none of the 12 SERPs pulled** (top 10, 21.10.2026) [api].
6. **What "first for every penthouse search" can and cannot mean.** About 9,000 of the roughly 17,700 monthly searches in the universe are "for sale in <city>" (5,710) and "for rent" (3,280) feed searches. Google answers them with Yad2, Madlan, Komo and broker category pages that show tens to thousands of homes (Madlan: 1,083 penthouses for sale in Tel Aviv-Yafo at 11:06 UTC). We have one penthouse-type home for sale and two for rent, and the URL law forbids new city pages with the word. Content alone will not put us first there. What is winnable: the head term "פנטהאוז" (3,600, difficulty 9, informational), definitions (about 600), mini penthouse (about 600), Tel Aviv prices and Tel Aviv penthouse searches (about 1,200), and every Kochav HaTzafon and north Tel Aviv mini-penthouse search. Winning the feed clusters needs inventory (brokers' penthouses listed on the site), which is a business decision, not a page change.
7. **Language versions of the glossary or prices page are blocked by the URL law.** `/en/glossary/penthouse/` or any other new path would re-use "penthouse", which /glossary/penthouse/ and /tel-aviv-penthouse-prices/ own. English demand is served by the English listing only, unless the owner rules otherwise.
8. **A small build gap in our own deals code.** `tools/deals/build_tlv_neighborhoods.py` keeps the property types "דירת גג", "פנטהאוז" and "מיני פנטהאוז" but not "דירת גג (פנטהאוז)", the label the Tax Authority actually uses on 50 Tel Aviv rows [src, CSV]. Our local copy of the deals also stops in early 2024 for roof types (the 2025-2026 rows are nearly absent: 1 and 2 deals). A fresh pull is needed before any public price table.

---

## 1. Intents (research law, step 1)

| # | Intent (owned) | Synonyms and variants seen in data | Owner page |
|---|---|---|---|
| 1 | What is a penthouse, a mini penthouse, a roof apartment; the differences | מה זה פנטהאוז, פנטהאוז הגדרה, מה זה מיני פנטהאוז, מיני פנטהאוז הגדרה, דירת גג, מה ההבדל בין פנטהאוז לדופלקס / לדירת גג / למיני פנטהאוז, פנטהאוז או דירת גן, יתרונות וחסרונות | /glossary/penthouse/ |
| 2 | The head term "פנטהאוז" (and "פנטהאוזים", "דירת פנטהאוז", "דירות פנטהאוז") in its informational sense | Google files "פנטהאוזים" under the same cluster as "פנטהאוז" (core keyword) | /glossary/penthouse/ |
| 3 | How much a penthouse costs in Tel Aviv; price per m²; how terraces are priced | מחירי פנטהאוזים, כמה עולה פנטהאוז (בתל אביב), מחיר פנטהאוז, מחיר למטר מרפסת, פנטהאוז תל אביב, פנטהאוזים בתל אביב, פנטהאוז למכירה בתל אביב | /tel-aviv-penthouse-prices/ |
| 4 | A mini penthouse for sale in north Tel Aviv / Kochav HaTzafon | מיני פנטהאוז למכירה, מיני פנטהאוז למכירה בתל אביב, פנטהאוז למכירה בצפון תל אביב, כוכב הצפון, פנטהאוז רמת אביב | listing (HE) |
| 5 | English: penthouse / mini penthouse in Tel Aviv | penthouse tel aviv, penthouse in tel aviv, tel aviv penthouses for sale, mini penthouse, penthouse israel | listing (EN) |

---

## 2. Ownership and cannibalisation (research law, step 2)

`python tools/gsc/url_word_audit.py --token penthouse` (21.10.2026, 4,571 URLs): 8 URLs hold "penthouse":
`/tel-aviv-penthouse-prices/`, `/glossary/penthouse/`, the three Meital Katzir listings in Hebrew (`/properties/kochav-hatzafon-new-mini-penthouse-for-sale/`, `/properties/tzukei-aviv-double-height-mini-penthouse-for-rent/`, `/properties/nofei-yam-mini-penthouse-5-rooms-for-rent/`) and their three English twins under `/en/brokers/meital-katzir/`.

Related head words checked the same day:
- "mini": only the six Meital Katzir listings. The two rental mini penthouses are the natural owners of "מיני פנטהאוז להשכרה" searches.
- "balcony": `/guides/new-apartment-balcony/` and its en/fr/ru/ar versions own it. A terrace guide must not become a rival page; the terrace content below lives inside the three penthouse pages, and any link from the balcony guide needs the owner's yes.
- "luxury": 8 URLs (`/luxury-tel-aviv/`, `/tel-aviv-luxury-apartment-prices/`, `/property-value/luxury-apartments-tel-aviv/` and others). "דירות יוקרה בתל אביב" (140) belongs to them, not to the penthouse pages.
- "tax" and "calculator": `/purchase-tax-calculator/`, `/apartment-purchase-cost-calculator/` and 12 more. The penthouse calculator below re-uses their logic inside the prices page; it is not a new calculator URL.
- "terrace", "duplex": no URL holds them.

Search Console overlaps (90 days):
- "מיני פנטהאוז הגדרה" was shown on `/glossary/` (the index: 3 impressions, position 77) and on `/glossary/penthouse/` (1 impression, position 33). A light split; the fix is a clear "מיני פנטהאוז" section on /glossary/penthouse/ with its own anchor, nothing on the index.
- "ניהול משא ומתן משפטי בקניית פנטהאוז יוקרה מקבלן" landed on `/buying-apartment/` (8 impressions, position 62). Not a conflict worth acting on.
- No penthouse query landed on the luxury pages.

---

## 3. The keyword universe (task 1)

Method:
- Hebrew, Israel (2376, he): Labs keyword_ideas (seeds פנטהאוז, פנטהאוז למכירה, מיני פנטהאוז, דירת גג; 2,691 ideas, first 700 by volume read), keyword_suggestions (פנטהאוז; מיני פנטהאוז; דירת גג), related_keywords (פנטהאוז למכירה, depth 2), keyword_overview (50 hand-picked terms: spellings, prices, neighbourhoods, duplex, garden). 731 unique Hebrew terms collected; 619 contain the topic and reach 10 searches a month; 118 more are furniture shops, design, holiday rentals and named buildings ("noise", listed in cluster K).
- English: Google Ads keywords_for_keywords for Israel-en and US-en (Labs does not cover Israel-en), Labs keyword_overview for US-en. Labs related_keywords for "penthouse tel aviv" (US) returned nothing.
- Volume = Google's monthly average over the last 12 months, rounded. CPC in USD. KD = DataForSEO keyword difficulty 0-100 (blank when DataForSEO has none). YoY = change in volume over 12 months, %. Pulled 21.10.2026, 10:55 to 11:05 UTC.
- Spellings "פנטהאוס", "פנטאוז", "פנטהוז" returned no volume of their own (Google folds them into "פנטהאוז"); Search Console shows each with 1 impression on /glossary/penthouse/.
- "פנטהאוזים" (3,600) is the same Google cluster as "פנטהאוז" (core keyword פנטהאוז, identical monthly series). Count it once. "פנטהאוז בתל אביב" and "פנטהאוזים בתל אביב" (110 each, identical CPC 3.02) are very likely one cluster too.
- The 12-month totals per cluster below exclude the noise cluster K. Universe total, Hebrew, excluding K: about 17,700 searches a month (the 3,600 of "פנטהאוזים" not counted twice).

### 3.1 Hebrew clusters at a glance

| Cluster | Terms ≥10 | Searches / month | What Google shows on page 1 | Owner page | Winnable now? |
|---|---|---|---|---|---|
| A. Head term (פנטהאוז, דירת/דירות פנטהאוז) | 71 (3 real, 68 named buildings/brands at 10) | 4,480 (3,800 in the 3 real terms) | furniture shops, Wikipedia, Sotheby's tag page, Madlan, mako tag, Booking, hon.co.il | glossary | yes, informational, KD 9 |
| B. Penthouse for sale, no city | 8 | 530 | Yad2, Komo, Madlan feeds, Indik, Sotheby's; AI answer lists the portals | prices page (TLV section) + listing | partly; feeds dominate |
| C. For sale / in a named city (not Tel Aviv) | 276 | 5,710 | Yad2, Madlan city feeds, local brokers | none (no URL may be created) | no, needs inventory |
| D. Tel Aviv | 34 | 1,070 | Madlan neighbourhood feeds, Sotheby's, Indik, Domestic, Zemour; AI answers (one is about a holiday rental) | prices page; listing for north TLV | yes for prices and north TLV |
| E. Mini penthouse | 32 | 600 | AI answer calling it a marketing term; unadlan, Bizportal, givat-alonim, broker-re, ynet, Sotheby's tag | glossary (definition); listing (for sale TLV) | yes |
| F. Definitions and differences | 11 | 600 (320 of it "מה זה דופלקס") | AI answer; law-firm, design and developer pages, dictionaries | glossary | yes |
| G. Prices | 12 | 130 | (no SERP pulled; see D) | prices page | yes |
| H. Roof apartment, duplex, garden | 25 | 520 | isratowers, Facebook groups, Yad2, walla, Madlan | glossary (definitions); city sale terms not winnable | definitions yes |
| I. Luxury, pool, sea, terraces | 31 | 800 | (not pulled) | glossary (terrace section), prices page | partly |
| J. For rent, by night, events | 119 | 3,280 | Yad2, Madlan, holiday-rental sites | the two rental mini-penthouse listings for "מיני פנטהאוז להשכרה"; rest not ours | small part |
| K. Noise (furniture shop "פנטהאוז", design, named buildings, holiday units) | 118 | 6,330 | the furniture shops | not ours | not a target |

### 3.2 Hebrew clusters in full (every term with volume ≥ 10)

#### A. Head term: 71 terms, 4480 searches/month
| Keyword | Vol | CPC $ | KD | Intent | YoY % |
|---|---|---|---|---|---|
| פנטהאוז | 3600 | 1.1 | 9 | informational | -47 |
| דירות פנטהאוז | 110 | 3.39 |  | transactional | -36 |
| דירת פנטהאוז | 90 | 2.62 |  | transactional | -36 |

#### B. Penthouse for sale, no city: 8 terms, 530 searches/month
| Keyword | Vol | CPC $ | KD | Intent | YoY % |
|---|---|---|---|---|---|
| פנטהאוז למכירה | 170 | 2.76 |  | transactional | 129 |
| פנטהאוזים למכירה | 170 | 2.91 |  | transactional | 24 |
| יד 2 פנטהאוז | 50 | 1.7 |  | transactional |  |
| פנטהאוז יד 2 | 40 | 9.2 |  | transactional |  |
| דירות פנטהאוז למכירה | 30 | 4.01 | 41 | transactional | 33 |
| למכירה פנטהאוז | 30 | 2.5 |  | transactional |  |
| פנטהאוז למכירה יד 2 | 30 | 1.92 |  | transactional | 100 |
| פנטהאוז מקבלן | 10 |  |  | transactional | -100 |

#### C. For sale or named, by city (outside Tel Aviv): 276 terms, 5710 searches/month
| Keyword | Vol | CPC $ | KD | Intent | YoY % |
|---|---|---|---|---|---|
| פנטהאוז למכירה בראשון לציון | 210 | 3.61 |  | transactional | -48 |
| פנטהאוז למכירה באשקלון | 210 | 2.66 |  | transactional | 53 |
| פנטהאוז אילת | 140 | 1.17 |  | informational | 29 |
| פנטהאוז הרצליה | 140 | 2.45 |  | informational | 91 |
| פנטהאוז למכירה ביבנה | 90 | 3.58 |  | transactional | -29 |
| פנטהאוז למכירה בנהריה | 90 | 3.1 |  | transactional | 57 |
| פנטהאוז באילת | 90 | 1.49 |  | informational | -20 |
| פנטהאוז למכירה באשדוד | 90 | 1.44 |  | transactional | 22 |
| פנטהאוז למכירה ברמת גן | 70 | 11 |  | transactional | 75 |
| פנטהאוז למכירה ברחובות | 70 | 1.57 |  | transactional | -43 |
| פנטהאוז למכירה בחולון | 70 | 2.31 |  | transactional | 29 |
| פנטהאוז למכירה בחיפה | 70 | 1.93 |  | transactional | -22 |
| פנטהאוז למכירה בבאר יעקב | 70 | 3.15 |  | transactional | 67 |
| פנטהאוז למכירה בהוד השרון | 70 | 2.48 |  | transactional | -20 |
| פנטהאוז למכירה בהרצליה | 70 | 2.47 |  | transactional | 100 |
| פנטהאוז למכירה בפתח תקווה | 50 | 1.96 |  | transactional |  |
| פנטהאוז פתח תקווה | 50 | 3.41 |  | informational |  |
| פנטהאוז בנתניה | 50 | 1.93 |  | informational | -25 |
| פנטהאוז אשדוד | 50 | 1.57 |  | navigational | -25 |
| פנטהאוז למכירה בחריש | 50 | 2.38 |  | transactional |  |
| פנטהאוז למכירה באשקלון יד 2 | 50 | 0.97 |  | transactional | 80 |
| פנטהאוז למכירה בנתניה | 50 | 2.91 |  | transactional | -50 |
| פנטהאוז בת ים | 50 | 1.83 |  | informational |  |
| פנטהאוז ראשון לציון | 50 | 3.73 |  | navigational | -29 |
| פנטהאוז למכירה בבת ים | 50 | 3.61 |  | transactional | -71 |
| פנטהאוז באשקלון | 40 | 2.34 |  | informational | -25 |
| פנטהאוז למכירה ברעננה | 40 | 3.12 |  | transactional | -67 |
| פנטהאוז למכירה בנתיבות | 40 | 2.75 |  | transactional | 33 |
| פנטהאוז למכירה באילת | 40 | 2.5 |  | transactional |  |
| פנטהאוז למכירה באשדוד יד 2 | 40 | 1.34 |  | transactional | 100 |
| פנטהאוז למכירה בראש העין | 40 | 1.44 |  | transactional | 67 |
| פנטהאוז בירושלים | 40 | 3.14 | 42 | navigational | 50 |
| פנטהאוז למכירה בנס ציונה | 40 | 2.5 | 13 | transactional | 100 |
| פנטהאוז למכירה בעפולה | 40 | 2.62 |  | transactional | -20 |
| פנטהאוז באר יעקב | 40 | 3.97 |  | informational |  |
| פנטהאוז למכירה בראשון לציון יד 2 | 40 | 3.32 | 45 | transactional | 25 |
| פנטהאוז חיפה | 40 | 2.14 | 13 | informational | 33 |
| פנטהאוז בראשון לציון | 30 | 1.15 | 40 | informational | -50 |
| פנטהאוז למכירה בקרית מלאכי | 30 | 1.5 |  | transactional |  |
| פנטהאוז למכירה בקרית השרון | 30 | 4.36 | 41 | transactional | -75 |

Also in this cluster (keyword · vol): פנטהאוז למכירה בקרית מוצקין 30 · פנטהאוז חולון 30 · פנטהאוז קרית אונו 30 · פנטהאוז למכירה בחולון ח 300 מדלן יד 2 30 · פנטהאוז למכירה בקרית ביאליק 30 · פנטהאוז רמת השרון 30 · פנטהאוז גני תקווה 30 · פנטהאוז למכירה בכפר סבא 30 · פנטהאוז רמת גן 30 · פנטהאוז באשדוד 30 · פנטהאוז למכירה ברמת השרון 30 · פנטהאוז למכירה במודיעין 30 · פנטהאוז למכירה בגבעתיים 30 · פנטהאוז 5 חדרים למכירה באשקלון 30 · פנטהאוז למכירה בחולון ח-300 מדלן יד 2 30 · פנטהאוז למכירה בבאר שבע 30 · פנטהאוז למכירה בקריות 30 · פנטהאוז למכירה בשדרות 20 · פנטהאוז למכירה בקרית אונו 20 · פנטהאוז חריש 20 · פנטהאוז למכירה בפסגות אפק ראש העין 20 · פנטהאוז בבת ים 20 · פנטהאוז למכירה בפתח תקווה כפר גנים ג 20 · פנטהאוז שדרות 20 · פנטהאוז גבעת שמואל 20 · פנטהאוז למכירה בחדרה 20 · פנטהאוז בחריש 20 · פנטהאוז למכירה ברחובות יד 2 20 · פנטהאוז ירושלים 20 · פנטהאוז למכירה נס ציונה 20 · פנטהאוז הרצליה פיתוח 20 · פנטהאוז למכירה בירושלים 20 · פנטהאוז כפר גנים ג 20 · פנטהאוז נהריה 20 · פנטהאוז גבעתיים 20 · פנטהאוז למכירה בגני תקווה 20 · פנטהאוז בחיפה 20 · פנטהאוז גליל ים 20 · פנטהאוז בראש העין 20 · פנטהאוז חדרה 20 · פנטהאוז רעננה 20 · פנטהאוז באשדוד למכירה 20 · פנטהאוז נס ציונה 20 · פנטהאוז בפתח תקווה 20 · פנטהאוז באר שבע 20 · פנטהאוז למכירה בטירת הכרמל 20 · פנטהאוז ברעננה למכירה 20 · פנטהאוז ביתר עילית 20 · פנטהאוז בהרצליה 20 · פנטהאוז למכירה בפתח תקווה אם המושבות 20 · פנטהאוז בבאר יעקב 20 · פנטהאוז למכירה באופקים 20 · פנטהאוז למכירה בחולון יד 2 20 · פנטהאוז ברמת גן 20 · פנטהאוז ברחובות 20 · פנטהאוז באשקלון למכירה 20 · פנטהאוז למכירה בכפר גנים ג 10 · פנטהאוז נירוונה נתניה 10 · פנטהאוז ערוץ 10 · פנטהאוז אמדר 10 · פנטהאוז למכירה בצור יצחק 10 · פנטהאוז בראשון לציון מערב 10 · פנטהאוז חדש למכירה בהרצליה 10 · פנטהאוז למכירה גבעת הרקפות קרית ביאליק 10 · פנטהאוז שמים נתניה 10 · פנטהאוז נוף גן עדן אילת 10 · פנטהאוז דובאי 10 · פנטהאוז מול כנרת 10 · פנטהאוז למסיבות במרכז 10 · פנטהאוז ויקיפדיה 10 · גג/פנטהאוז למכירה בבת ים יד2 10 · פנטהאוז הצוקים חדרה 10 · פנטהאוז ברמת השרון 10 · פנטהאוז כנרת 10 · פנטהאוז עין הים חדרה 10 · פנטהאוז גני תקווה יד 2 10 · פנטהאוז בראש העין למכירה 10 · פנטהאוז למסיבות 10 · פנטהאוז בבאר יעקב שכונת צמרות 10 · פנטהאוז למכירה בעכו 10 · דירות פנטהאוז למכירה בחיפה 10 · פנטהאוז למכירה בנווה גן פתח תקווה 10 · יד 2 פנטהאוז למכירה באשקלון 10 · פנטהאוז במודיעין 10 · פנטהאוז נשיאותי אילת 10 · פנטהאוז עיר ימים נתניה 10 · פנטהאוז מודיעין 10 · פנטהאוז רמדה 10 · פנטהאוז למכירה בנאות אשלים ראשון לציון 10 · פנטהאוז בנתניה למכירה יד 2 10 · פנטהאוז אמדר אילת 10 · פנטהאוז משכנות האומנים קרית מוצקין 10 · פנטהאוז בגבעתיים למכירה 10 · פנטהאוז במגדלי יו 10 · פנטהאוז נווה גן רמת השרון 10 · פנטהאוז עם נוף לים 10 · פנטהאוז 5 חדרים למכירה באשדוד 10 · דירות פנטהאוז למכירה בראשון לציון 10 · פנטהאוז במגדלי אקירוב 10 · פנטהאוז בכפר סבא 10 · פנטהאוז מורשת מודיעין 10 · פנטהאוז נורת 10 · פנטהאוז נוף לים 10 · פנטהאוז בהרצליה פיתוח 10 · פנטהאוז אופק אילת 10 · פנטהאוז פינות אוכל 10 · פנטהאוז למכירה ביפו 10 · יד 2 פנטהאוז למכירה בראשון לציון 10 · פנטהאוז חדש למכירה בראשון לציון 10 · פנטהאוז באגמים אשקלון 10 · פנטהאוז בטירת הכרמל יד 2 10 · פנטהאוז נווה גן פתח תקווה 10 · פנטהאוז למכירה בהרצליה פיתוח 10 · פנטהאוז בראשית אילת 10 · פנטהאוז למכירה בחדרה ללא תיווך 10 · פנטהאוז למכירה במערב ראשון לציון 10 · דירות פנטהאוז למכירה בחולון 10 · פנטהאוז נוף יובל 10 · פנטהאוז נכסים גדרה 10 · פנטהאוז כפר גנים ג פתח תקווה 10 · פנטהאוז למכירה בחולון ח 300 יד 2 10 · פנטהאוז בכפר יונה 10 · פנטהאוז למכירה בחריש יד 2 10 · פנטהאוז למכירה בבאר שבע יד 2 10 · פנטהאוז חדש למכירה באשקלון 10 · פנטהאוז למכירה בעיר ימים 10 · פנטהאוז רמדה חדרה 10 · פנטהאוז באילת למכירה 10 · פנטהאוז מהחלומות אילת 10 · פנטהאוז אתר 10 · פנטהאוז למכירה ברעננה יד 2 10 · פנטהאוז למכירה בכפר סבא הירוקה 10 · פנטהאוז שטיחים 10 · פנטהאוז נופש 10 · פנטהאוז לומינה 10 · יד 2 פנטהאוז למכירה באשדוד 10 · פנטהאוז יחיד בקומה באשקלון 10 · פנטהאוז בפתח תקווה יד 2 10 · פנטהאוז ביבנה 10 · פנטהאוז סרטים 10 · פנטהאוז בקריית השרון 10 · פנטהאוז חדש ברמת גן 10 · פנטהאוז רמת אפעל 10 · פנטהאוז למכירה באור יהודה 10 · פנטהאוז חדש בראשון לציון 10 · פנטהאוז ברחובות למכירה 10 · פנטהאוז בעיר ימים 10 · פנטהאוז נווה זמר רעננה 10 · פנטהאוז למכירה בבני ברק 10 · פנטהאוז בארגמן נס ציונה 10 · פנטהאוז ללא תיווך בבאר שבע 10 · פנטהאוז למכירה ברחובות המדע 10 · פנטהאוז דרמה 10 · פנטהאוז למכירה בקרית חיים מזרחית 10 · פנטהאוז למסיבות באשדוד 10 · פנטהאוז הים האדום 10 · פנטהאוז בראשון לציון למכירה 10 · פנטהאוז הכי יקר בישראל 10 · פנטהאוז אשקלון יד 2 10 · פנטהאוז חדש ברחובות 10 · פנטהאוז נופש באילת 10 · פנטהאוז ראם 10 · פנטהאוז מול הכותל 10 · פנטהאוז בהרצליה הירוקה 10 · פנטהאוז בגני תקווה 10 · פנטהאוז אבן ישראל 10 · פנטהאוז פארק צמרת 10 · פנטהאוז מגדלי יו 10 · פנטהאוז באכזיב 10 · פנטהאוז נאות פרס 10 · פנטהאוז למכירה במזכרת בתיה 10 · פנטהאוז הבשמים 10 · פנטהאוז אם המושבות 10 · פנטהאוז בנתניה 30 מיליון 10 · פנטהאוז בגבעתיים 10 · פנטהאוז למכירה בקרית גת 10 · פנטהאוז עודפים 10 · פנטהאוז בחולון 10 · פנטהאוז ממילא 10 · פנטהאוז בקרית אתא 10 · פנטהאוז בצל ההר 10 · פנטהאוז למכירה בשוהם 10 · פנטהאוז אור ים 10 · פנטהאוז קינג אילת 10 · פנטהאוז חנות 10 · פנטהאוז בגליל ים 10 · פנטהאוז מול הכנרת 10 · פנטהאוז מקבלן בעפולה 10 · פנטהאוז למסיבה 10 · פנטהאוז חדש למכירה בכפר סבא 10 · פנטהאוז למכירה ברחובות ההולנדית 10 · פנטהאוז חדש למכירה 10 · פנטהאוז בחדרה 10 · פנטהאוז בראש העין החדשה 10 · פנטהאוז למכירה בחולון ח 300 10 · פנטהאוז במגדל בראשית 10 · פנטהאוז בוטיק רחובות 10 · פנטהאוז למכירה בבאר יעקב יד 2 10 · פנטהאוז לימי הולדת 10 · פנטהאוז לאירועים 10 · פנטהאוז מריו 10 · פנטהאוז למכירה בח 370 חולון 10 · פנטהאוז סוויט טאוור 10 · פנטהאוז סי וויו 10 · פנטהאוז בנתניה למכירה 10 · פנטהאוז חיפה מועדון 10 · פנטהאוז ברעננה 10 · פנטהאוז למכירה בשוהם יד 2 10 · פנטהאוז נירוונה 10 · פנטהאוז בראשית 10 · פנטהאוז בוטיק כנרת 10 · פנטהאוז עיר ימים 10 · פנטהאוז כרמי הנדיב 10 · פנטהאוז למכירה בנחלת יהודה 10 · פנטהאוז סיטי טאוור 10 · פנטהאוז בהרצליה למכירה 10 · פנטהאוז למכירה בברנע 10 · פנטהאוז למכירה ביבנה הירוקה 10 · פנטהאוז למכירה בחולון ח-300 יד 2 10 · פנטהאוז ראש העין החדשה 10 · פנטהאוז כלבו שלום 10 · פנטהאוז למכירה ראשון לציון 10 · פנטהאוז למכירה בהרצליה ללא תיווך 10 · פנטהאוז ראם חדרה 10 · פנטהאוז בוטיק צל הרים 10 · פנטהאוז כפר סבא הירוקה 10 · פנטהאוז למכירה פתח תקווה 10 · פנטהאוז פלמורה 10 · יד 2 פנטהאוז למכירה בהרצליה 10 · פנטהאוז ארלוזורוב 17 10 · פנטהאוז משכנות אומנים 10 · פנטהאוז למכירה בת ים 10 · פנטהאוז בנופים מודיעין 10 · פנטהאוז למכירה במערב ראשון 10 · פנטהאוז ביבנה הירוקה 10 · פנטהאוז באשדוד ללא תיווך 10

#### D. Tel Aviv and its neighbourhoods: 34 terms, 1070 searches/month
| Keyword | Vol | CPC $ | KD | Intent | YoY % |
|---|---|---|---|---|---|
| פנטהאוז תל אביב | 210 | 3.39 |  | informational | -19 |
| דירות יוקרה בתל אביב | 140 | 2.94 |  | informational | -18 |
| פנטהאוז בתל אביב | 110 | 3.02 |  | informational | -18 |
| פנטהאוזים בתל אביב | 110 | 3.02 |  | informational | -18 |
| פנטהאוז למכירה בתל אביב | 90 | 4.24 |  | transactional | -50 |
| דירות יוקרה למכירה בתל אביב | 70 | 5.9 |  | transactional | -29 |
| פנטהאוז למכירה תל אביב | 30 | 2.73 | 13 | transactional |  |
| פנטהאוז עם בריכה תל אביב | 20 | 4.68 | 40 | transactional |  |
| פנטהאוז עם בריכה בתל אביב | 20 | 2.05 |  | informational | -33 |
| פנטהאוז למכירה בתל אביב יד 2 | 20 | 2.28 | 13 | transactional |  |
| פנטהאוז תל אביב למכירה | 20 | 4.66 | 13 | transactional |  |
| פנטהאוז רמת אביב | 10 | 8.86 |  | informational | 50 |
| פנטהאוז למכירה בצפון תל אביב | 10 | 2.24 | 13 | transactional |  |
| פארק בבלי פנטהאוז | 10 |  | 46 | navigational |  |
| פנטהאוז יוקרה תל אביב | 10 |  |  | informational |  |
| פנטהאוז למכירה ברמת אביב | 10 | 6.64 |  | transactional |  |
| פנטהאוז תל אביב מסיבה | 10 |  |  | informational |  |
| פנטהאוז תל אביב למסיבות | 10 |  |  | navigational |  |
| ארלוזורוב 17 תל אביב פנטהאוז | 10 |  | 46 | navigational | -100 |
| פנטהאוז למסיבה בתל אביב | 10 | 2.2 | 38 | transactional |  |
| פנטהאוז ברמת אביב החדשה | 10 |  |  | transactional |  |
| פנטהאוז תל אביב כלות | 10 |  |  | informational |  |
| פנטהאוז עם בריכה תל אביב למכירה | 10 | 1.38 | 43 | transactional |  |
| פנטהאוז בתל אביב למסיבה | 10 |  | 38 | transactional | -100 |
| פנטהאוז לימי הולדת תל אביב | 10 |  | 40 | transactional | -100 |
| פנטהאוז בתל אביב למכירה | 10 | 3.12 |  | transactional |  |
| פנטהאוז גינדי tlv | 10 |  | 40 | informational |  |
| פנטהאוז יוקרתי בתל אביב | 10 | 4.25 |  | transactional | 100 |
| לופט פנטהאוז תל אביב | 10 | 0.59 |  | navigational |  |
| פנטהאוז למכירה ברמת אביב ג | 10 |  | 9 | transactional |  |
| פנטהאוז יוקרה בתל אביב | 10 | 4.25 |  | informational | 100 |
| גינדי tlv פנטהאוז | 10 | 1.34 | 40 | informational |  |
| פנטהאוז למסיבות בתל אביב | 10 | 2.2 | 38 | transactional |  |
| פנטהאוז תל אביב התארגנות לכלה | 10 | 2.27 |  | transactional |  |

#### E. Mini penthouse: 32 terms, 600 searches/month
| Keyword | Vol | CPC $ | KD | Intent | YoY % |
|---|---|---|---|---|---|
| מיני פנטהאוז | 170 | 6.19 |  | transactional | 55 |
| מה זה מיני פנטהאוז | 50 |  |  | informational | -20 |
| מיני פנטהאוז למכירה | 40 | 2.38 |  | transactional | -25 |
| מיני פנטהאוז למכירה בראשון לציון | 30 | 4.23 |  | transactional | -60 |
| מיני פנטהאוז הגדרה | 30 |  |  | informational | -86 |
| מה ההבדל בין פנטהאוז למיני פנטהאוז | 20 |  |  | informational |  |
| מיני פנטהאוז באשקלון | 10 | 0.69 |  | informational |  |
| מיני פנטהאוז חריש | 10 | 0.29 | 38 | informational |  |
| מיני פנטהאוז בחולון | 10 |  |  | informational |  |
| מיני פנטהאוז למכירה נס ציונה | 10 |  | 38 | transactional |  |
| מיני פנטהאוז למכירה ברחובות | 10 | 1.71 | 42 | transactional | 200 |
| מיני פנטהאוז למכירה בתל אביב | 10 |  |  | transactional |  |
| מיני פנטהאוז עם בריכה פרטית למכירה | 10 | 1.95 |  | transactional |  |
| מיני פנטהאוז למכירה בנתניה | 10 |  |  | transactional |  |
| מיני פנטהאוז למכירה בהרצליה הירוקה | 10 |  |  | transactional |  |
| מיני פנטהאוז בהוד השרון | 10 | 3.41 |  | transactional |  |
| מיני פנטהאוז ברמת גן | 10 |  | 42 | informational |  |
| מיני פנטהאוז למכירה בהרצליה | 10 | 4.5 | 37 | transactional |  |
| מיני פנטהאוז בגני תקווה | 10 |  | 42 | informational |  |
| מיני פנטהאוז נחלת יהודה | 10 | 3.31 | 41 | informational |  |
| מיני פנטהאוז למכירה בהוד השרון | 10 |  | 5 | transactional |  |
| מיני פנטהאוז למכירה בגני תקווה | 10 | 4.65 | 9 | transactional |  |
| מיני פנטהאוז למכירה בפתח תקווה | 10 | 1.54 |  | transactional |  |
| מיני פנטהאוז למכירה ביבנה | 10 |  | 41 | transactional | -100 |
| מיני פנטהאוז למכירה בראש העין | 10 | 1.83 |  | transactional | -50 |
| מיני פנטהאוז למכירה בחולון | 10 |  |  | transactional |  |
| מיני פנטהאוז למכירה באשדוד | 10 | 2.18 | 9 | transactional |  |
| מיני פנטהאוז למכירה ברמת השרון | 10 | 6.38 |  | transactional |  |
| מיני פנטהאוז למכירה באשקלון | 10 |  | 40 | transactional |  |
| מיני פנטהאוז כפר גנים ג | 10 |  | 13 | informational |  |
| מיני פנטהאוז בבאר יעקב | 10 | 3.47 | 12 | informational |  |
| דירות מיני פנטהאוז למכירה בפתח תקווה | 10 |  |  | transactional | -100 |

#### F. Definitions and differences: 11 terms, 600 searches/month
| Keyword | Vol | CPC $ | KD | Intent | YoY % |
|---|---|---|---|---|---|
| מה זה דופלקס | 320 |  |  | informational | -18 |
| מה זה פנטהאוז | 110 |  |  | informational | 29 |
| מה זה דירת גן | 70 |  |  | informational | 40 |
| פנטהאוז הגדרה | 30 |  |  | informational | -60 |
| הגדרה של פנטהאוז | 10 |  |  | informational |  |
| יתרונות וחסרונות של פנטהאוז | 10 |  | 42 | commercial | -100 |
| פנטהאוז מה זה | 10 |  |  | informational |  |
| מה מותר לבנות במרפסת פנטהאוז | 10 |  |  | informational |  |
| מה ההבדל בין פנטהאוז לדופלקס | 10 |  |  | informational | 100 |
| דירת גג חסרונות | 10 |  | 40 | informational | -100 |
| מה ההבדל בין דירת גג לפנטהאוז | 10 |  |  | informational |  |

#### G. Prices: 12 terms, 130 searches/month
| Keyword | Vol | CPC $ | KD | Intent | YoY % |
|---|---|---|---|---|---|
| בריכה על גג פנטהאוז מחיר | 20 |  |  | commercial | -50 |
| כמה עולה פנטהאוז בתל אביב | 10 | 2.54 |  | commercial | -33 |
| מחיר פנטהאוז | 10 |  |  | informational |  |
| מחיר פנטהאוז בתל אביב | 10 |  |  | commercial | -100 |
| מגדלי יו פנטהאוז מחיר | 10 |  |  | informational |  |
| כמה עולה פנטהאוז | 10 | 2.79 |  | commercial | 100 |
| פנטהאוז tlv מחיר | 10 |  |  | informational |  |
| כמה עולה פנטהאוז במגדלי יו | 10 |  |  | commercial |  |
| מחיר פנטהאוז בחריש | 10 |  |  | informational |  |
| פנטהאוז במגדלי יו מחיר | 10 |  |  | informational | -100 |
| מחירי פנטהאוזים | 10 |  |  | informational |  |
| מחיר למטר מרפסת | 10 |  |  | informational |  |

#### H. Roof apartment, duplex, garden: 25 terms, 520 searches/month
| Keyword | Vol | CPC $ | KD | Intent | YoY % |
|---|---|---|---|---|---|
| דירת גג | 90 | 1.26 |  | informational | -22 |
| בריכה על גג פנטהאוז | 70 | 3.94 |  | informational | -55 |
| מרפסת גג | 70 | 0.85 |  | informational | -43 |
| דירת גג למכירה בחולון | 40 | 1.52 |  | transactional | 25 |
| דירת גג למכירה בפתח תקווה | 30 | 2.08 |  | transactional | -57 |
| פנטהאוז דופלקס | 20 | 3.42 | 36 | informational | -50 |
| פנטהאוז על הגג נתניה | 20 | 0.11 |  | transactional | 75 |
| דירת גן או פנטהאוז | 10 |  | 38 | informational |  |
| גג פנטהאוז למכירה בבת ים יד2 | 10 |  | 43 | transactional | -100 |
| דופלקס פנטהאוז | 10 |  | 36 | informational |  |
| דירת גג עם בריכה | 10 |  |  | informational |  |
| למכירה דירת גג אבן יהודה | 10 |  |  | transactional |  |
| דירת גג למכירה בהרצליה | 10 | 0.89 | 37 | transactional |  |
| שיפוץ דירת גג | 10 | 5.92 | 43 | informational |  |
| דירת גג למכירה | 10 |  | 13 | transactional |  |
| פינוי בינוי דירת גג תמורה | 10 |  |  | commercial |  |
| דירת גג פתח תקווה | 10 | 1.75 |  | informational | -80 |
| פיצול דירת גג | 10 |  | 41 | informational | -100 |
| דירת גג תל אביב | 10 | 2.24 | 42 | informational | -67 |
| דירת גג בתל אביב | 10 | 1.36 | 42 | transactional |  |
| דירת גג למכירה בראשון לציון | 10 | 0.65 | 10 | transactional | 100 |
| פינוי בינוי דירת גג | 10 |  | 8 | transactional | -100 |
| דירת גג למכירה ברעננה | 10 |  | 42 | transactional |  |
| דירת גג למכירה תל אביב | 10 | 1.41 | 42 | transactional |  |
| דירות גג למכירה | 10 |  | 9 | transactional |  |

#### I. Luxury, pool, sea, terraces: 31 terms, 800 searches/month
| Keyword | Vol | CPC $ | KD | Intent | YoY % |
|---|---|---|---|---|---|
| פנטהאוז עם בריכה | 170 | 1.81 |  | transactional | -19 |
| פנטהאוז עם בריכה למכירה | 90 | 2.89 |  | transactional |  |
| בריכה במרפסת פנטהאוז | 50 | 0.01 |  | transactional | -25 |
| מרפסת פנטהאוז | 50 |  |  | informational | -20 |
| פנטהאוז יוקרה | 40 | 2.5 | 42 | informational | -57 |
| פנטהאוז באילת עם בריכה | 40 | 1.29 | 41 | informational | 67 |
| פנטהאוז יוקרתי | 40 | 2.5 | 40 | informational | -57 |
| פנטהאוז על הים נתניה | 30 | 3.37 |  | informational | 100 |
| פנטהאוז מול הים ראשון לציון | 20 | 2.64 |  | informational | -50 |
| פנטהאוז על הים | 20 | 2.01 | 42 | informational | -50 |
| פנטהאוז עם בריכה באילת | 20 | 1.94 | 41 | transactional | -33 |
| פנטהאוז מרפסת | 20 |  | 4 | transactional | -80 |
| פנטהאוז עם בריכה בראשון לציון | 20 | 1.63 |  | informational |  |
| פנטהאוז מול הים | 20 |  | 42 | informational | -67 |
| פנטהאוז היוקרה בבית השעון | 10 |  | 42 | informational |  |
| פנטהאוז עם בריכה פרטית באילת | 10 | 0.93 | 41 | transactional |  |
| האם משלמים ארנונה על מרפסת פנטהאוז | 10 |  | 41 | commercial |  |
| תאורה למרפסת פנטהאוז | 10 | 0.46 | 42 | informational | 100 |
| פנטהאוז עם בריכה יבנה | 10 |  |  | informational |  |
| פנטהאוז קיסריה מול הים | 10 | 1.15 |  | informational | -80 |
| גינה במרפסת פנטהאוז | 10 | 2.41 |  | informational | -33 |
| פנטהאוז בריכה | 10 |  |  | informational |  |
| פנטהאוז על הגג | 10 | 0.19 |  | informational |  |
| פנטהאוז עם בריכה גני תקווה | 10 |  |  | informational |  |
| פנטהאוז עם בריכה בחיפה | 10 | 1.27 |  | commercial |  |
| פנטהאוז עם בריכה במודיעין | 10 | 1.34 | 40 | transactional |  |
| פנטהאוז בנתניה עם בריכה | 10 | 1.5 |  | informational |  |
| פנטהאוז על הים נהריה | 10 | 2.07 |  | transactional |  |
| פנטהאוז עם בריכה חדרה | 10 | 0.25 |  | transactional |  |
| פנטהאוז על הים אילת | 10 |  |  | informational |  |
| פנטהאוז מול הים אילת | 10 |  |  | informational | -75 |

#### J. For rent, by night, events: 119 terms, 3280 searches/month
| Keyword | Vol | CPC $ | KD | Intent | YoY % |
|---|---|---|---|---|---|
| פנטהאוז להשכרה | 210 | 1.53 |  | informational | 24 |
| פנטהאוז להשכרה באשקלון | 170 | 1.71 |  | transactional | 55 |
| פנטהאוז להשכרה ברמת גן | 90 | 13.09 |  | transactional | 200 |
| פנטהאוז להשכרה בתל אביב | 90 | 1.59 |  | transactional | -36 |
| פנטהאוז להשכרה בראשון לציון | 90 | 1.45 |  | transactional | 29 |
| פנטהאוז להשכרה באשדוד | 70 | 0.12 |  | transactional | -71 |
| פנטהאוז להשכרה בחולון | 70 | 1.2 |  | transactional | -55 |
| פנטהאוז להשכרה בחיפה | 70 | 0.51 |  | transactional | -29 |
| פנטהאוז להשכרה ללילה | 70 | 0.98 |  | transactional | -29 |
| פנטהאוז להשכרה בנהריה | 70 |  |  | transactional | 25 |
| פנטהאוז להשכרה בפתח תקווה | 70 | 1.37 |  | transactional | -29 |
| פנטהאוז להשכרה בחריש | 70 | 2.2 |  | transactional | -20 |
| דירת גג להשכרה בחולון | 70 |  |  | transactional | -33 |
| פנטהאוז להשכרה בבת ים | 50 | 0.68 |  | transactional | -43 |
| פנטהאוז להשכרה בנתיבות | 50 |  |  | transactional | 33 |
| פנטהאוז להשכרה בהוד השרון | 50 | 0.02 |  | transactional | -57 |
| יד 2 פנטהאוז להשכרה | 50 |  |  | transactional | -33 |
| פנטהאוז להשכרה בקריות | 50 |  |  | informational | -50 |
| פנטהאוז תל אביב להשכרה | 50 | 1.44 |  | transactional | -20 |
| פנטהאוז להשכרה באילת | 40 | 0.93 |  | transactional | -56 |
| פנטהאוז להשכרה בהרצליה | 40 | 1.53 |  | transactional | 33 |
| פנטהאוז להשכרה בבאר שבע | 40 |  | 13 | transactional | -33 |
| פנטהאוז להשכרה ברעננה | 40 |  |  | transactional | -50 |
| פנטהאוז להשכרה בראש העין | 40 | 1.31 |  | transactional | 33 |
| פנטהאוז להשכרה ברחובות | 40 |  |  | commercial | -50 |
| פנטהאוז להשכרה בקרית אונו | 40 | 2.05 |  | transactional | 100 |
| פנטהאוז להשכרה בנתניה | 40 | 0.36 |  | transactional |  |
| פנטהאוז להשכרה תל אביב | 40 | 1.53 |  | transactional |  |
| פנטהאוז להשכרה בכפר גנים ג | 30 |  |  | commercial | -89 |
| פנטהאוז להשכרה ברמת השרון | 30 | 1.57 | 42 | transactional | -60 |
| פנטהאוז להשכרה בבאר יעקב | 30 | 1.88 | 9 | transactional | 50 |
| פנטהאוז בת ים להשכרה | 30 | 0.82 |  | transactional |  |
| פנטהאוז בתל אביב ללילה | 30 | 1.34 | 40 | transactional | -33 |
| פנטהאוז להשכרה בגני תקווה | 30 |  | 42 | transactional | 100 |
| פנטהאוז באשדוד להשכרה | 30 | 0.35 |  | transactional | 100 |
| פנטהאוז להשכרה בשדרות | 30 | 2.93 |  | transactional | 50 |
| פנטהאוז להשכרה בחדרה | 30 | 2.94 | 9 | transactional | -33 |
| פנטהאוז להשכרה בירושלים | 30 | 2.65 | 42 | transactional | 50 |
| פנטהאוז להשכרה בעפולה | 30 |  | 40 | transactional | -25 |
| פנטהאוז עם בריכה להשכרה ללילה | 30 | 0.77 |  | transactional |  |

Also in this cluster (keyword · vol): פנטהאוז עם בריכה להשכרה 30 · פנטהאוז להשכרה בכפר סבא 30 · דירת גג להשכרה בפתח תקווה 30 · דירת גג להשכרה ברמת גן 30 · פנטהאוז להשכרה ללילה בתל אביב 20 · פנטהאוז תל אביב להשכרה ליום 20 · פנטהאוז בתל אביב להשכרה 20 · פנטהאוז בראשון לציון להשכרה 20 · פנטהאוז להשכרה במודיעין 20 · פנטהאוז להשכרה בגבעת שמואל 20 · דירות מיני פנטהאוז להשכרה בראשון לציון 20 · פנטהאוז להשכרה במרכז 20 · פנטהאוז להשכרה בגבעתיים 20 · פנטהאוז להשכרה ביבנה 20 · פנטהאוז בנתניה להשכרה 20 · פנטהאוז להשכרה בראשון לציון יד 2 20 · פנטהאוז להשכרה ללילה במרכז 20 · להשכרה פנטהאוז 20 · פנטהאוז באילת לנופש 20 · דירת גג להשכרה 20 · דירת גג להשכרה תל אביב 20 · דירת גג להשכרה בתל אביב 20 · פנטהאוז חריש להשכרה 10 · פנטהאוז להשכרה ללילה תל אביב 10 · מיני פנטהאוז להשכרה בראש העין 10 · פנטהאוז להשכרה בנס ציונה 10 · פנטהאוז להשכרה בכפר יונה 10 · פנטהאוז להשכרה בקרית קריניצי 10 · פנטהאוז להשכרה בקרית מלאכי 10 · פנטהאוז להשכרה בגני תקווה יד 2 10 · פנטהאוז להשכרה אם המושבות 10 · מיני פנטהאוז להשכרה 10 · פנטהאוז להשכרה בקרית גת 10 · מיני פנטהאוז להשכרה ברמת גן 10 · פנטהאוז להשכרה בפרדס חנה 10 · פנטהאוז להשכרה ללילה בנתניה 10 · פנטהאוז להשכרה ללילה באילת 10 · פנטהאוז להשכרה למסיבה בתל אביב 10 · פנטהאוז להשכרה בגבעת אולגה 10 · פנטהאוז להשכרה בקרית השרון 10 · פנטהאוז בתל אביב להשכרה ללילה 10 · פנטהאוז באילת להשכרה יומית 10 · פנטהאוז להשכרה בתל אביב ללילה 10 · פנטהאוז להשכרה ביבנה הירוקה 10 · פנטהאוז להשכרה בקרית ים 10 · פנטהאוז להשכרה בצור יצחק 10 · יד 2 פנטהאוז להשכרה בטירת כרמל 10 · דירות פנטהאוז להשכרה בחולון 10 · פנטהאוז בחדרה לנופש 10 · פנטהאוז להשכרה בטירת הכרמל 10 · פנטהאוז להשכרה הר חומה 10 · פנטהאוז ללילה בתל אביב 10 · פנטהאוז בחריש להשכרה 10 · פנטהאוז להשכרה באילת יד 2 10 · פנטהאוז להשכרה ברמת אביב החדשה 10 · דירות פנטהאוז להשכרה באילת 10 · פנטהאוז להשכרה בעיר ימים 10 · פנטהאוז להשכרה בעין הים 10 · מיני פנטהאוז להשכרה בחולון 10 · להשכרה מיני פנטהאוז 10 · פנטהאוז להשכרה יומית באילת 10 · פנטהאוז ברחובות להשכרה 10 · פנטהאוז להשכרה בתל אביב למסיבה 10 · פנטהאוז להשכרה בחולון ח 300 10 · פנטהאוז להשכרה ללילה בחדרה 10 · פנטהאוז להשכרה גליל ים 10 · פנטהאוז להשכרה ביהוד 10 · פנטהאוז עם בריכה להשכרה תל אביב 10 · פנטהאוז להשכרה בכפר סבא הירוקה 10 · פנטהאוז להשכרה יומית 10 · פנטהאוז באילת להשכרה 10 · פנטהאוז בחדרה להשכרה 10 · פנטהאוז בטבריה לנופש 10 · פנטהאוז עם בריכה להשכרה באילת 10 · פנטהאוז להשכרה למסיבה 10 · פנטהאוז עם בריכה ללילה 10 · פנטהאוז באשקלון להשכרה 10 · פנטהאוז ללילה 10 · דירת גג להשכרה בהרצליה 10

#### K. Noise: furniture shops, design, named buildings, holiday units (not a target): 118 terms, 6330 searches/month
| Keyword | Vol | CPC $ | KD | Intent | YoY % |
|---|---|---|---|---|---|
| פנטהאוז בייסיק | 1600 | 1.37 | 4 | transactional | 30 |
| פנטהאוז רהיטים | 720 | 0.6 |  | transactional | 22 |
| פנטהאוז שמיים נתניה | 260 | 0.5 |  | informational |  |
| תמיר מנדובסקי פנטהאוז | 210 |  |  | informational |  |
| עיצוב מרפסות פנטהאוז | 170 | 2.38 |  | informational | -72 |
| פנטהאוז עיצוב הבית | 170 | 0.88 | 13 | informational |  |
| עיצוב פנטהאוז | 170 | 1.45 |  | informational | -81 |
| עיצוב מרפסת פנטהאוז | 170 | 1.36 |  | informational | -35 |
| עיצוב פנטהאוז יוקרתי | 140 | 2.21 |  | informational | -44 |
| פנטהאוז שמיים | 140 | 0.58 |  | informational | 55 |
| בוטיק פנטהאוז רחובות | 110 | 0.63 |  | informational | 27 |
| עיצוב פנטהאוז מודרני | 90 | 1.29 |  | informational | -57 |
| עיצוב גגות פנטהאוז | 90 | 2.44 |  | informational | -64 |
| פנטהאוז ריהוט גן | 90 | 0.65 |  | informational | 29 |
| פנטהאוז 42 אילת | 70 | 1.76 |  | navigational | 450 |

Also in this cluster (keyword · vol): מגזין פנטהאוז 30 · ריהוט גן יוקרתי פנטהאוז 30 · פנטהאוז אור עקיבא 30 · עיצוב דירת גג 30 · פנטהאוז אאוטלט 20 · פנטהאוז סייז אור עקיבא 20 · פנטהאוז נופים בהר 20 · פנטהאוז בריגה נתניה 20 · בריגה נתניה פנטהאוז 20 · פנטהאוז להשכרה ליום הולדת 20 · פנטהאוז להשכרה בכרמי גת 20 · פנטהאוז גפן אילת 20 · חצר המלכה פנטהאוז 20 · פנטהאוז חלום על הים 20 · פנטהאוז למסיבת רווקים 20 · פנטהאוז למסיבת רווקות 20 · פנטהאוז הרברט סמואל 20 · פנטהאוז ריהוט חוץ 20 · פנטהאוז מיטות 20 · פנטהאוז באנגלית 20 · פנטהאוז מפואר 20 · פנטהאוז בריגה 20 · פנטהאוז נוף כנרת 20 · פנטהאוז מרינה 20 · מגדל שלום מאיר פנטהאוז 20 · פנטהאוז מעוצב תמונות 10 · בריגה פנטהאוז 10 · פנטהאוז בייסיק שטיחים 10 · עיצוב פנטהאוז תמונות 10 · פנטהאוז ריהוט גינה 10 · פנטהאוז בייסיק תל אביב יפו 10 · פנטהאוז ליום הולדת 10 · פנטהאוז בייסיק ריהוט גן 10 · פנטהאוז רהיטים קטלוג 10 · פנטהאוז בייסיק הרצליה 10 · פנטהאוז רהיטים יפו 10 · פנטהאוז להשכרה באור עקיבא 10 · פנטהאוז למסיבת רווקים בתל אביב 10 · פנטהאוז תל אביב מסיבת רווקים 10 · מגדלי בריגה פנטהאוז 10 · לויקיישן מיני פנטהאוז 10 · פנטהאוז רהיטים סניפים 10 · פנטהאוז רהיטי גן 10 · דירות פנטהאוז מעוצבות 10 · פנטהאוז למכירה באור עקיבא 10 · פנטהאוז בריגה טאוורס 10 · פנטהאוז בייסיק קטלוג 10 · פנטהאוז רהיטים בהרצליה כתובת 10 · פנטהאוז רהיטים אאוטלט 10 · בריגה טאוורס פנטהאוז 10 · מתחם 42 אילת פנטהאוז 10 · פנטהאוז מפואר במודיעין 10 · פנטהאוז רהיטי גן הרצליה 10 · פנטהאוז ריהוט גן הרצליה 10 · פנטהאוז אאוטלט אודים שעות פתיחה 10 · פנטהאוז רהיטים בהרצליה 10 · בוטיק פנטהאוז ברחובות 10 · פנטהאוז חנות רהיטים 10 · מגדל שלום פנטהאוז 10 · פנטהאוז רויאל ביץ 10 · פנטהאוז בייסיק ספות 10 · פנטהאוז עם בריכה למסיבת רווקות 10 · עיצוב דירת פנטהאוז 10 · פנטהאוז רהיטים ספות 10 · פנטהאוז רהיטי גן עודפים 10 · פנטהאוז רהיטים לגינה 10 · ביקורות על פנטהאוז בייסיק 10 · פנטהאוז להשכרה באשדוד ליום הולדת 10 · מרפסת פנטהאוז עיצוב 10 · תמונות של פנטהאוז בייסיק 10 · פנטהאוז בייסיק ריהוט חוץ 10 · פנטהאוז עיצוב 10 · עיצוב גינות פנטהאוז 10 · פנטהאוז רהיטים אינסטגרם 10 · פנטהאוז למכירה במרינה אשדוד 10 · פנטהאוז רהיטים אודים 10 · פנטהאוז בריגה עיר ימים 10 · דירת גג בכפר בלום 10

### 3.3 English

| Keyword | Market | Volume | CPC $ | Competition | Notes |
|---|---|---|---|---|---|
| penthouse tel aviv | Israel en | 50 | 3.46 | MEDIUM (46) | Google Ads |
| penthouse tel aviv / penthouse in tel aviv | US en | 50 (one cluster) | 5.70 | LOW (18) | Google Ads; peak 140 in 2.2026 |
| tel aviv luxury apartments | Israel en | 50 | 4.62 | MEDIUM (63) | owned by the luxury pages |
| luxury apartments tel aviv | US en | 50 | 4.28 | LOW | Labs, commercial |
| tel aviv luxury real estate | US en | 30 | 3.29 | MEDIUM | Labs |
| penthouse israel | Israel en / US en | 10 / 10 | 1.98 / 5.37 | MEDIUM | |
| mini penthouse | Israel en | 10 | n/a | LOW (4) | US: no data |
| tel aviv penthouses for sale | US en | 10 | 5.80 | LOW (24) | |
| jerusalem penthouse / penthouse jerusalem | US en / Israel en | 10 / 10 | 15.28 / n/a | LOW | not ours |
| penthouse raanana | US en | 10 | n/a | | not ours |
| luxury apartments for sale tel aviv, tel aviv luxury apartments for sale, luxury rentals tel aviv, luxury apartments for rent in tel aviv, tel aviv luxury apartments for rent | Israel en | 10 each | 0.80 to 3.18 | MEDIUM-HIGH | luxury pages own these |
| what is a penthouse | US en | 6,600 | n/a | LOW, KD 7 | global definition, not an Israel buyer; no URL may serve it |
| penthouse meaning | US en | 4,400 | n/a | KD 7 | same |
| penthouse apartment | US en | 8,100 | 3.52 | KD 7, navigational | US rental feeds; not ours |
| luxury penthouse | US en | 2,400 | 3.71 | KD 4 | global; not ours |
| penthouse vs duplex | US en | 10 | n/a | | |
| tel aviv penthouse for sale, penthouse for sale in israel, israel penthouse for sale, what is a mini penthouse | US en | no data | | | |

For the wider English, French and Russian buyer universe (tel aviv real estate 480, israel real estate 720, immobilier israel 320 and others), see `campaign/keywords.md` section 2; not repeated here.

---

## 4. Our standing in Search Console (task 2)

Window 21.7 to 19.10.2026, `sc-domain:nad-lan.co.il`. Filter: queries containing פנטהאוז and its spellings, penthouse, גג, mini, דופלקס, יוקרה.

### 4.1 Page totals (all queries, including the ones Google hides)

| Page | Clicks | Impressions | Avg position |
|---|---|---|---|
| /glossary/penthouse/ | 1 | 117 | 11.1 |
| /tel-aviv-penthouse-prices/ | 0 | 84 | 7.3 |
| /properties/kochav-hatzafon-new-mini-penthouse-for-sale/ | 0 | 9 | 7.3 |
| /en/brokers/meital-katzir/kochav-hatzafon-new-mini-penthouse-for-sale/ | 0 | 1 | 9.0 |
| /properties/nofei-yam-mini-penthouse-5-rooms-for-rent/ | 0 | 21 | 7.0 |
| /properties/tzukei-aviv-double-height-mini-penthouse-for-rent/ | 0 | 3 | 8.7 |
| /en/.../nofei-yam-5-room-mini-penthouse-for-rent/ | 0 | 2 | 3.5 |
| /en/.../tzukei-aviv-double-height-mini-penthouse-for-rent/ | 0 | 1 | 10.0 |

Most impressions on these pages come from queries Google does not report (anonymised long tail). The good average positions belong to those rare long queries, not to the head terms.

### 4.2 Penthouse queries Google does report (query × page)

| Query | Page | Impr. | Clicks | Position |
|---|---|---|---|---|
| פנטהאוז | /glossary/penthouse/ | 2 | 0 | 75.0 |
| מיני פנטהאוז הגדרה | /glossary/ | 3 | 0 | 77.3 |
| מיני פנטהאוז הגדרה | /glossary/penthouse/ | 1 | 0 | 33.0 |
| מה ההבדל בין פנטהאוז לדירת יוקרה רגילה | /glossary/penthouse/ | 1 | 0 | 17.0 |
| מה ההבדל בין פנטהאוז לדופלקס | /glossary/penthouse/ | 1 | 0 | 47.0 |
| פנטהאוזים | /glossary/penthouse/ | 1 | 0 | 32.0 |
| פנטאוז | /glossary/penthouse/ | 1 | 0 | 43.0 |
| פנטהאוס | /glossary/penthouse/ | 1 | 0 | 44.0 |
| ניהול משא ומתן משפטי בקניית פנטהאוז יוקרה מקבלן | /buying-apartment/ | 8 | 0 | 62.5 |
| מחיר? / כן | /tel-aviv-penthouse-prices/ | 1 / 1 | 0 | 5.0 / 9.0 |
| מה זה בית דופלקס | /glossary/ | 1 | 0 | 76.0 |
| הערכת שווי גג משותף | /property-value-estimator/ | 3 | 0 | 25.0 |
| תקנות התכנון והבניה טופס 4 גישה לגג | /real-estate-lawyer/form-4-occupancy-permit/ | 1 | 0 | 50.0 |

Neighbouring luxury queries for context: פרויקט יוקרה התחדשות עירונית → /projects/ (128 impressions, position 40.9); מגדלי יוקרה → /projects/ (92, 38.1); פרויקטי יוקרה בתל אביב → /luxury-tel-aviv/ (64, 72.5). Zero clicks on all.

Reading: the head term "פנטהאוז" reaches us at position 75 on the glossary page. No reported query reaches the listing. Cannibalisation is minor (one definition query split between /glossary/ and /glossary/penthouse/).

---

## 5. SERPs (task 3, research law step 4)

Google Israel, Hebrew, desktop, depth 10, DataForSEO organic live advanced with AI Overview loading on. Times are UTC, 21.10.2026. "AI answer absent" means DataForSEO returned no AI Overview block at that moment. Page types: feed = a listings search page; tag = a broker's category page of listings; guide = an article.

### 5.1 The ten Hebrew SERPs

**1. פנטהאוז** (3,600) at 10:58:47
- Organic: penthouse-furniture.co.il (furniture shop) · he.wikipedia.org/wiki/פנטהאוז (encyclopedia) · instagram.com/penthouse__ (furniture shop) · [local pack: furniture shops and a holiday unit] · [images] · israelsir.co.il tag "פנטהאוז יוקרתי למכירה בתל אביב" (tag) · madlan.co.il/penthouses-for-rent/ישראל (feed, "233 דירות") · penthousebasic.co.il (furniture shop) · mako.co.il/Tagit/פנטהאוז (news tag) · booking.com (holiday) · hon.co.il "פנטהאוז – יתרונות וחסרונות" (guide, 2016, modified 1.10.2026).
- AI answer: absent. People also ask: absent.
- Related searches: פנטהאוז בייסיק, פנטהאוז רהיטים, פנטהאוז הרצליה, פנטהאוז רהיטים עודפים, פנטהאוז הגדרה, פנטהאוז תל אביב, פנטהאוז רהיטים יפו, פנטהאוז ספות.
- Reading: four of ten slots go to a furniture brand. Only two real-estate guides rank (Wikipedia at 309 words, hon.co.il at 1,465). A definitive Hebrew guide has room at the top.

**2. פנטהאוז למכירה** (170; 320 in 9.2026, +129% a year) at about 10:58:50
- Organic: indik.net "פנטהאוז למכירה בתל אביב" (broker tag) · [images] · yad2 "גגות/פנטהאוזים למכירה" (feed) · [AI answer] · komo.co.il (feed) · yad2 Jerusalem (feed) · israelsir tag (tag) · remax1.co.il Hadera (broker tag) · yad2 Afula (feed) · madlan Petah Tikva (feed, "43 דירות").
- AI answer: present. It sends buyers to portals and luxury brokers. Sources: madlan.co.il (Petah Tikva, central moshavim), yad2.co.il, indik.net, israelsir.co.il. It ends by asking city, budget, terrace size.
- People also ask: absent. Related: פנטהאוז למכירה ירושלים, פנטהאוז למכירה תל אביב-יפו, מיני פנטהאוז למכירה, פנטהאוז למכירה בפתח תקווה אם המושבות, ... כפר גנים ג, מיני פנטהאוז למכירה בראשון לציון, ... בחולון, פנטהאוז למכירה באשקלון.

**3. מיני פנטהאוז** (170, +55% a year) at 10:58:59
- AI answer (first): "a marketing term in Israeli real estate" for a large home one or two floors below the top; "true penthouse" has roof rights "in the bylaws"; typical terrace "25–30 m² and up"; appraisers call many cases a marketing trick. Sources: unadlan.co.il (2017), bizportal.co.il 819031 (4.10.2023), givat-alonim.co.il (7.8.2024), he.wikipedia.org, broker-re.co.il (29.12.2022), ynet L-4384714 (29.5.2013), a Facebook post of "מחאת דיור".
- Organic: unadlan (guide 2017) · bizportal (news 2023) · madlan Tel Aviv "פנטהאוז / מיני למכירה ... 1085 דירות" (feed) · [images] · [PAA] · givat-alonim (developer magazine) · broker-re (broker glossary) · israelsir mini tag (tag) · hon.co.il (guide) · ynet (news 2013).
- People also ask: מה ההבדל בין מיני פנטהאוז לפנטהאוז? · כמה עולה פנטהאוז בתל אביב? · איפה הכי זול לקנות דירה בישראל? · מהי ההגדרה של פנטהאוז? · מה ההבדל העיקרי בין דופלקס לפנטהאוז? · מהי ההגדרה של דופלקס?
- Related: מיני פנטהאוז למכירה, מיני פנטהאוז להשכרה, מיני פנטהאוז חולון, פנטהאוז למכירה בתל אביב יד 2, פנטהאוז תל אביב להשכרה, פנטהאוז תל אביב למכירה, פנטהאוז פתח תקווה, מה זה פנטהאוז.
- Reading: this is the listing's biggest opportunity. Google's answer tells buyers the term is often a trick. A home with a terrace about three times the 25 m² norm that the appraisers' chair named for Kochav HaTzafon (ynet 2013, quote below) answers that doubt with numbers.

**4. פנטהאוז תל אביב** (210) at 10:59:19
- AI answer: present, but about a holiday unit called "הפנטהאוז של תל אביב" (Aza street). Sources: vila4u, booking.com, aaa.co.il, ttt.co.il, rrr.co.il, penthousetlv.com, instagram.
- Organic: tlv2go.com (holiday) · indik.net rent tag · habait-halavan.co.il "פנטהאוז למכירה בתל אביב" (broker page, 22.4.2025) · resort.co.il (holiday) · madlan "במגדל" (feed, 3) · Facebook video (a WE tower penthouse) · nyg.co.il Tel Aviv (broker) · [images] · domestictlv.co.il listing. Paid ads present.
- PAA: absent.

**5. פנטהאוזים בתל אביב** (110) at 10:59:26
- AI answer: present, same holiday unit and same sources as above.
- Organic: myplace.co.il "דירות יוקרה" (broker) · domestictlv penthouse tag · madlan "במגדל" · society4u.co.il sale search · nyg.co.il · madlan נגה (106) · society4u rent · indik rent · madlan מעוז אביב ב' (104).
- Related: דירות יוקרה בתל אביב להשכרה, דירות יוקרה למכירה בתל אביב, פנטהאוז למכירה בתל אביב, דירות בתל אביב למכירה, וילה למכירה בתל אביב, פנטהאוז עם בריכה בתל אביב, דירות לשימור למכירה בתל אביב, פנטהאוז עם בריכה למכירה.

**6. פנטהאוז למכירה בתל אביב** (90) at 10:59:35
- Organic: madlan נגה (feed) · israelsir "פנטהאוז יוקרתי למכירה במרכז תל אביב" (tag) · [AI answer] · myplace (broker) · domestictlv listing "פנטהאוז נדיר ... נוף עד הים" · madlan אבן גבירול (375) · zemour-realty.com "פנטהאוז למכירה בצפון תל אביב" (broker guide, 16.8.2021) · yad2 Tel Aviv (feed) · ariel-home.co.il ("201 פנטהאוס למכירה") · madlan בני אפרים 227 (10).
- AI answer: present. Says prices "start at about 3.95 million ILS in the northern and southern neighbourhoods and can reach tens of millions in the centre and on the waterfront" [snippet]. Sources: zemour-realty.com, madlan.co.il ×4 (נגה, בני אפרים 227, ריינס 1, אבן גבירול), israelsir.co.il, domestictlv.co.il.
- PAA: איפה אפשר למצוא דירות יוקרה בתל אביב? · איפה אפשר למצוא פנטהאוז בתל אביב? · (an unrelated Yad2 question).
- Related: בתי יוקרה למכירה בתל אביב, דירות בתל אביב למכירה, וילה למכירה בתל אביב, פנטהאוז עם בריכה למכירה, דירות לשימור למכירה בתל אביב, פנטהאוז עם בריכה בתל אביב, למכירה דירה אקירוב.

**7. מה זה פנטהאוז** (110, +29%) at 10:59:42
- AI answer: present. Penthouse = "a luxury home on the top floor of a residential building or tower", big terrace, no neighbours above, open view, priced well above the rest. Sources: rossetto.co.il (design), israelsir.co.il (design tips), hamichlol.org.il, ynet L-5430191 (21.12.2018), urban-tower.co.il (developer), novet.co.il (design), 5nadlan.co.il.
- Organic: ravit-law.co.il "מנפצים את מיתוס הפנטהאוז" (law firm, TAMA 38; 31.12.2023) · novet.co.il (design) · urban-tower.co.il "פנטהאוז ומיני פנטהאוז: ההבדלים" (developer) · [images] · ynet 2018 · gil-ron.co.il "פנטהאוז, דירת גג או דירת גן, מה עדיף?" · hamichlol (disambiguation, 2.11.2025) · rossetto.co.il (design) · kfirhy-law.com "למה בית המשפט חייב יזם לרשום בתקנון כי דירת הגג נמצאת בקומה האחרונה?" (law firm, 1.12.2019).
- PAA: absent.

**8. דירות פנטהאוז** (110) at 10:59:53
- Organic: madlan "בכל הארץ - 3152 דירות" (feed) · [AI answer] · yad2 (feed) · he.wikipedia · israelsir tag · hon.co.il · madlan Tel Aviv (1085) · levi-itzhak.co.il "מה שווה יותר דירת גן או פנטהאוז?" · nadlanmaster.co.il (feed) · isratowers.co.il (rent). Knowledge panel present.
- AI answer: present. Sources: he.wikipedia, hon.co.il, levi-itzhak.co.il, tivnadlan.co.il/glossary/דירת-פנטהאוז (a competitor glossary), nadlanmaster.co.il, broker-re.co.il.

**9. מה זה מיני פנטהאוז** (50) at 10:59:59
- AI answer: present. A single-level, relatively large home one or two floors below the true penthouse, larger terrace, no roof rights. Sources: unadlan, givat-alonim, eldargroup.com "מדריך לדירות מיוחדות", ynet 2013, hon.co.il, a Facebook group post, bizportal.
- Organic: madlan national (feed) · themarker.com (14.5.2015) · [PAA] · instagram post · milog.co.il (dictionary) · gil-ron.co.il · novet.co.il · Facebook group · milononline.net (dictionary) · mishpati.co.il forum (29.3.2018, property tax).
- PAA: מה מקור המילה "פנטהאוז"? · (three unrelated on half-rooms and cottages) · מה ההבדל בין פנטהאוז למיני פנטהאוז?

**10. דירת גג** (90) at 11:00:09
- AI answer: present. A top-floor home with a private roof terrace usually reached by an inner staircase; differs from a penthouse built as one luxury level. Sources: eldargroup.com, isratowers.co.il, a Facebook group, walla 3458114 (4.9.2021), madlan (Bnei Brak), yad2 rent.
- Organic: isratowers.co.il (rent) · Facebook group · yad2 לב תל אביב (feed) · walla (news) · Facebook group · madlan (feed) · yad2 rent · Facebook group.

### 5.2 English SERPs (Google Israel, English)

**penthouse tel aviv** at 11:06:02: israelsir.com listing · [local pack: three holiday penthouses] · israelpropertyhub.com listing · plumguide.com (holiday) · **video pack** (YouTube: Israel Sotheby's; Montefiore twice) · Facebook (Airbnb) · a hotel-booking site · YouTube tour · israelsir.com listing · properstar.co.za ("54 Penthouses for Sale in Tel Aviv-Yafo") · Facebook. AI answer absent; PAA absent.

**mini penthouse** at 11:06:08: AI answer present ("a high-floor luxury apartment that mimics the layout and large outdoor terrace of a full penthouse, usually spanning 120 to 300 square meters"; sources luxury-propertyinisrael.com, nyg.co.il ×2, myplace.co.il, janglo.net ×2, israelsir.com, booking.com ×2). Organic: luxury-propertyinisrael.com (Netanya agency tag) · booking.com · habitat.co.il (furniture) · pinterest · a Dimri PDF · janglo.net · onmap.co.il rent · ronkin-list.com.

The US English SERP for "penthouse tel aviv" was recorded on 21.10 in `campaign/keywords.md` (video pack of three YouTube listing tours there too).

---

## 6. Competitor pages read in full (task 3 and research law step 3)

All fetched 21.10.2026 at about 11:01 UTC (raw HTML, then the visible text read end to end). Word counts are of the visible text after navigation is removed, so they include sidebars and comments; treat them as rough.

### 6.1 "פנטהאוז" (head term): the three real-estate results

| Rank | URL | Type | Words | Structure | Dates | Schema |
|---|---|---|---|---|---|---|
| 2 | https://he.wikipedia.org/wiki/פנטהאוז | encyclopedia | ~309 | one definition paragraph, "בישראל" section with the penthouse vs roof apartment split, two external links | created 2.10.2006, modified 27.4.2026 | Article |
| 4 | https://www.israelsir.co.il/property_tags/פנטהאוז-יוקרתי-למכירה-בתל-אביב/ | broker tag | ~610 | H1 + about 15 listing cards (title, built m², asking price), no prose | none | CollectionPage, BreadcrumbList |
| 9 | https://www.hon.co.il/פנטהאוז-יתרונות-וחסרונות/ | guide | ~1,465 | H1, definition, penthouse vs roof apartment, mini penthouse, "how much it costs", pros (privacy, view, light, outdoor space), cons (neighbours, lift, parking distance, limited design), quotes a developer's marketing VP | published 12.9.2016, modified 1.10.2026 | Article, BreadcrumbList |

What makes them rank:
- Wikipedia: the only clean definition plus a domain Google trusts; it is tiny. It gives the Israeli split (penthouse = one level with a roof terrace next to the living room; roof apartment = same size as the floor below, with the roof above reached by stairs).
- Sotheby's tag: exact-match H1 and real inventory with prices (16.75M ILS for 248 m² up to 100M ILS for 900 m² on floor 47) [src, asking prices]. No text at all.
- hon.co.il: the only Hebrew article that covers pros, cons and price on one page, and it is kept "fresh" with a box of current numbers at the top (purchase-tax brackets frozen to 15.1.2028, VAT 18%, Bank of Israel rate). Its price claims are thin: "about 30% and up" over a similar home, examples of 9M vs 3.2M ILS "in a report", 100M ILS for 500 m² towers [src]. No table, no tool, no sources.

### 6.2 "פנטהאוז למכירה": the top three

| Rank | URL | Type | Words | What is on it |
|---|---|---|---|---|
| 1 | https://www.indik.net/דירת-פנטהאוז | broker tag | ~891 | H1 "פנטהאוז למכירה בתל אביב", 24 listing cards as H3 (Old North, centre, promenade, Givatayim; sale and rent mixed), a short marketing paragraph, sidebar of articles; RealEstateAgent schema; no dates, no prices in the text body (prices in the cards per the AI answer: 160 m² for 10.5M ILS, 152 m² for 13.5M ILS [snippet]) |
| 2 | https://www.yad2.co.il/realestate/forsale?propertyGroup=apartments&property=6 | feed | not readable (bot wall "Radware Page") | per the SERP: "thousands of new ads every day", filters by budget and size [snippet] |
| 3 | https://www.komo.co.il/code/nadlan/apartments-for-sale.asp?nehes=3 | feed | ~687 | H1 "גג/פנטהאוז/מיני פנטהאוז למכירה", 26 listings as H2 (city, neighbourhood, street, price), one SEO line at the end; no schema |

What makes them rank: inventory. Exact-match H1, many fresh homes with prices, national reach. Komo even merges "גג/פנטהאוז/מיני פנטהאוז" into one category, which is how Israeli portals classify (Yad2 property=6 is "גגות/פנטהאוזים"). Not one of them explains anything.

### 6.3 "מיני פנטהאוז": the top three (plus two the AI answer leans on)

| Rank | URL | Type | Words | What is on it |
|---|---|---|---|---|
| 1 | https://unadlan.co.il/מיני-פנטהאוז/ | guide | ~1,210 (about 800 of article) | H1 question; "definition": upper floors (stepped), a sun terrace of **30 m² and up**, privacy like a penthouse; developers' version: a regular home with a bigger terrace, one floor below the top, higher finish; split of the market at 2005 (buildings before 2005 have only penthouses); roof rights exist only if the bylaws attach them; advice: decide by the attached rights, not the name. Published 29.5.2017, modified 25.5.2023. BlogPosting schema. No numbers beyond 25-30 m². |
| 2 | https://www.bizportal.co.il/realestates/news/article/819031 | news | ~2,173 (about 1,100 of article, the rest 31 comments) | "the fake of real estate": a regular home with 21 m² terrace instead of 14 m², premium 120,000-150,000 ILS (6%-7%) in a Hadera project, 200,000-250,000 ILS in the centre; appraiser Omid Soleimani: the term is an invention; **balcony utility coefficient 0.2 to 0.5** depending on size, neighbourhood and use. 4.10.2023. NewsArticle schema. |
| 3 | madlan.co.il/penthouses-for-sale/תל-אביב-יפו-ישראל | feed | ~1,783 (cards + blog links) | H1 "פנטהאוזים למכירה בתל אביב יפו", "1083 פנטהאוזים למכירה" at 11:06 UTC, cards mixing "פנטהאוז" and "מיני פנטהאוז", 25 blog links, no SEO prose [src via DataForSEO content parsing] |
| (AI source) | https://www.ynet.co.il/articles/0,7340,L-4384714,00.html | news | ~698 | "the difference is 3 m²": a mini penthouse on floor 7 in a north Tel Aviv project, 122 m² + 14 m² terrace vs 120 m² + 13 m² below it, 150,000 ILS more. The then chair of the Real Estate Appraisers Association, Ohad Danos: there is no professional definition, but homes called so "usually enjoy a terrace of at least 25 m²", "as is customary in north Tel Aviv projects such as the Kochav HaTzafon neighbourhood". His breakdown: about 50,000 ILS for the floor, about 50,000 ILS for the extra metres (20,000 ILS per m² inside, 10,000 ILS per m² of balcony), about 50,000 ILS "for the name". 29.5.2013. |
| (AI source) | https://givat-alonim.co.il/news/דירה-או-מיני-פנטהאוז-... | developer magazine | ~614 | mini penthouses on floors 16-17, 5.5 rooms vs 5, a terrace "twice" the average. 7.8.2024. |

What makes them rank: they answer the doubt ("is it a trick?") in plain words. None has a table, a calculator, a checklist of documents or a dated price. The freshest is 2024; the main facts date from 2013 to 2017.

### 6.4 Legal pages the definition SERPs show (used in the brief)

- https://www.kfirhy-law.com/post/דירת-פנטהאוז (1.12.2019, ~1,500 words): the Jerusalem District Court ruling in ה"פ 49407-05-12 ג'ולי ביטן נ' מצפה בית שמש בע"מ (5.3.2018): the developer must register in the condominium bylaws that the penthouses are on the top floor and that no floors may be added; the bylaws override the sale contract unless the buyer registered a protest; Land Law 1969 sections 61, 64 (standard vs agreed bylaws), 125 (a deal ends with registration); building on the roof needs the consent of all owners. [src; verify the ruling's citation in Nevo before quoting it on a page]
- https://ravit-law.co.il/.../המדריך-לתמא-38-מנפצים-את-מיתוס-הפנטהאוז/ (31.12.2023): in TAMA 38, check the land registry documents to see whether future roof rights belong to the penthouse owners or to all owners. [src]

### 6.5 The DNA in one table

| Trait | Wikipedia | hon | unadlan | Bizportal | ynet | Sotheby's tag | Indik | Komo/Yad2/Madlan |
|---|---|---|---|---|---|---|---|---|
| Clear definition | yes | yes | yes | partial | partial | no | no | no |
| Penthouse vs mini vs roof apartment | partial | yes | yes | partial | no | no | no | merged categories |
| Numbers on terraces | no | no | 25-30 m² | 0.2-0.5 coefficient | 25 m² norm, 10,000/m² balcony | built m² only | no | m² per card |
| Prices | no | anecdotes | no | premiums in ILS | 150,000 gap | asking prices | in cards | asking prices |
| Legal checks (bylaws, permit, roof rights) | no | no | one line | one line | no | no | no | no |
| Table / tool | no | no | no | no | no | no | no | filters |
| Freshness | 4.2026 | 10.2026 (box only) | 2017 | 2023 | 2013 | live | live | live |
| Length | ~300 | ~1,500 | ~800 | ~1,100 | ~700 | cards | cards | cards |

The page that combines a sourced definition, the mini-penthouse test, the legal checks, dated price tables and two working tools does not exist in Hebrew.

---

## 7. The plan (task 4)

### 7.1 Who owns what

| Cluster | Owner page | Supporting page | Not ours |
|---|---|---|---|
| A head "פנטהאוז", "דירת/דירות פנטהאוז" | /glossary/penthouse/ | prices page | furniture shops |
| F definitions, H roof apartment / duplex / garden definitions, I terraces and pools (how-to) | /glossary/penthouse/ | | |
| E mini penthouse, definition | /glossary/penthouse/ (section "מיני פנטהאוז", own anchor) | listing | |
| E mini penthouse for sale, Tel Aviv / north / Kochav HaTzafon | listing (HE) | prices page | the rest of Israel's cities |
| G prices, D "פנטהאוז תל אביב", "פנטהאוזים בתל אביב", "פנטהאוז למכירה בתל אביב", "כמה עולה פנטהאוז" | /tel-aviv-penthouse-prices/ | listing | |
| B "פנטהאוז למכירה" (no city) | prices page (section with what is for sale on the site now) | listing | Yad2/Madlan feeds will stay above |
| C city sale, J rent (except mini penthouse rent) | none | | needs inventory; no new URLs |
| "מיני פנטהאוז להשכרה" | the two rental mini-penthouse listings (Tzukei Aviv, Nofei Yam) | | |
| English "penthouse tel aviv", "mini penthouse" (Israel) | listing (EN) | | global "what is a penthouse" |

### 7.2 Title, H1 and meta proposals

Rules used: one H1 per page; the answer paragraph right under the H1 (intent-first law); Israeli developer-site language, no tech words, no slogans; unknown facts omitted; numbers only once settled. Character counts are approximate.

**Listing (HE)** — owns "מיני פנטהאוז למכירה בתל אביב / בצפון / בכוכב הצפון"
- Now: title "מיני פנטהאוז 5 חדרים למכירה בכוכב הצפון תל אביב"; H1 "מיני פנטהאוז 5 חדרים עם מרפסת של 80 מ״ר, כוכב הצפון".
- Title: `מיני פנטהאוז למכירה בכוכב הצפון, תל אביב | 5 חדרים, מרפסת [confirmed terrace m²] מ״ר` (about 60)
- H1: `מיני פנטהאוז 5 חדרים למכירה בכוכב הצפון, עם מרפסת של [confirmed terrace m²] מ״ר`
- Meta: `מיני פנטהאוז חדש בקומה 11 מתוך 12 בכוכב הצפון: 5 חדרים, [confirmed built m²] מ״ר בנוי ומרפסת של [confirmed terrace m²] מ״ר, פי שלושה מהמקובל במיני פנטהאוז. 2 חניות, מחסן, ממ״ד. 18,000,000 ש״ח.` (about 155)
- The "three times" line rests on ynet 29.5.2013 (appraisers' chair: at least 25 m², "customary in Kochav HaTzafon"): 78 / 25 = 3.1 or 80 / 25 = 3.2 [calc]. The source stays in this file, not on the page.
- First paragraph under the H1 answers Google's doubt directly: what makes this a real mini penthouse (floor 11 of 12, the terrace size, the built area against a typical 5-room home in the building if the broker can give it, otherwise omitted).

**Listing (EN)** — owns "penthouse tel aviv", "mini penthouse tel aviv"
- Title: `Mini Penthouse for Sale in North Tel Aviv, Kochav HaTzafon | 5 Rooms` (about 65)
- H1: `Mini penthouse for sale in Kochav HaTzafon, north Tel Aviv, with a [confirmed terrace m²] m² terrace`
- Meta: `A new five-room mini penthouse on floor 11 of 12 in Kochav HaTzafon, north Tel Aviv: [confirmed built m²] m² built and a [confirmed terrace m²] m² terrace, about three times the usual size. Two parking spaces, storage, safe room. NIS 18,000,000.`
- English SERPs show a video pack; see action 5 for the film.

**/glossary/penthouse/** — owns the head term and all definitions
- Now: title "פנטהאוז - נדלן"; H1 "פנטהאוז".
- Title: `פנטהאוז: מה זה, מיני פנטהאוז, דירת גג ודופלקס, ומה בודקים לפני שקונים` (about 70; Google may cut after about 60, the head word is first)
- H1: `פנטהאוז: מה זה, ומה ההבדל ממיני פנטהאוז, דירת גג ודופלקס`
- Meta: `פנטהאוז הוא הדירה בקומה העליונה עם מרפסת גג צמודה. ההבדל ממיני פנטהאוז, דירת גג ודופלקס, כמה מרפסת נחשבת "מיני", איך בודקים את הגג בתקנון ובהיתר, ומחירים לפי עסקאות.` (about 160)

**/tel-aviv-penthouse-prices/** — owns prices and Tel Aviv penthouse searches
- Now: title "פנטהאוז בתל אביב — מחירי הצמרת האמיתיים"; H1 "מחירי פנטהאוזים בתל אביב".
- Title (only after the deal table is live): `מחירי פנטהאוזים בתל אביב: עסקאות, מחיר למ״ר לפי שכונה ומחשבון` (about 60)
- H1: `מחירי פנטהאוזים בתל אביב: כמה עולה פנטהאוז בכל שכונה`
- Meta: `כמה עולה פנטהאוז בתל אביב? מחיר למ״ר לפי שכונה מעסקאות רשות המסים, מחשבון ששוקל מרפסות בשליש או בחצי ומחשב מס רכישה לפי סוג הרוכש, ומה בודקים בגג לפני עסקה.`
- If the table is not ready, keep the current title; do not promise deals the page does not show.

### 7.3 Internal links (only among these pages, per the owner)

| From | To | Anchor (Hebrew) | Status |
|---|---|---|---|
| glossary | prices page | מחירי פנטהאוזים בתל אביב | new |
| glossary (mini penthouse section) | listing (HE) | מיני פנטהאוז למכירה בכוכב הצפון | new; as the worked example of a mini penthouse that passes the test |
| prices page | glossary | מה זה פנטהאוז ומה ההבדל ממיני פנטהאוז | exists (check the anchor) |
| prices page (north Tel Aviv section) | listing (HE) | מיני פנטהאוז למכירה בצפון תל אביב | new |
| listing (HE) | glossary | exists (1 link) | keep |
| listing (HE) | prices page | מחירי פנטהאוזים בתל אביב | new |
| listing (EN) ↔ listing (HE) | | | exists (language switch) |

Ask the owner before any of these: from /guides/new-apartment-balcony/ (owns "balcony"), from /purchase-tax-calculator/ and /apartment-purchase-cost-calculator/, from the luxury pages, from /glossary/ (the index), from the two rental mini-penthouse listings, from any strong page to the listing (his order: not yet).

### 7.4 The tools (blocks inside the existing pages; no new URL)

Design note for every tool (owner law of 13.10.2026): palette and type taken from Israeli permit drawings and Tabu extracts: blueprint ink navy `#13294B` on drafting white `#F7F8F6`, with surveyor red `#C8102E` only for warnings and a thin grid line `#C9D3DE`; Hebrew face "Heebo" is the safe default, so use "Assistant" for text and "Frank Ruhl Libre" only for large figures, Latin "IBM Plex Sans". Not cream, not brass, not a purple gradient, no emoji. Each tool goes through Claude Design before any build (owner law of 27.9).

**T1. Penthouse price-per-m² and total-cost calculator** (prices page; a compact read-only version already exists on the listing as "מחיר למ״ר: הדירה מול השוק")
- Inputs: asking price; built m² (from the Tabu or permit); terrace m² (sun terraces); roof m² (a separate attached roof, if any); weighting for outdoor area: 1/3, 1/2 or custom between 0.2 and 0.5; buyer type: single home, additional home, foreign resident, new immigrant; lawyer % (default 0.5%) and broker % (default 2%), both + VAT 18%.
- Outputs: price per built m²; weighted area and price per weighted m² at the chosen weight, and side by side at 1/3 and 1/2; purchase tax by bracket with the working shown; total cost and % over price; a line against the neighbourhood median from T3 when there are 5 or more deals.
- Sources to wire: brackets frozen 16.1.2025 to 15.1.2028 (single home 0% to 1,978,745; 3.5% to 2,347,040; 5% to 6,055,070; 8% to 20,183,565; 10% above; additional home 8% to 6,055,070 then 10%; immigrant track 0% to 1,978,745 then 0.5% to 6,055,070) from value-pack.md section 4.1 (Bizportal 6.8.2026), to be checked against the Tax Authority simulator https://www.gov.il/he/service/real_eatate_taxsimulator before going live; the foreign-resident rule must be confirmed there or with a tax adviser. The weight range 0.2 to 0.5 is the appraiser's range quoted by Bizportal on 4.10.2023; no official coefficient was found (value-pack.md section 9). Re-use the engine of /purchase-tax-calculator/ so the two never disagree.
- Worked example for QA (listing, built 190 m², terraces 78 m², 18,000,000 ILS): 94,737 per built m²; 84,349 at 0.3; 78,603 at 0.5; single-home tax 1,153,886; additional-home or foreign 1,678,899 [calc, value-pack.md 2.5 and 4.2]. At 1/3: 190 + 26 = 216 m², 83,333 per weighted m² [calc].
- Structured data: `WebApplication` (name, applicationCategory "FinanceApplication", operatingSystem "Any", offers price 0 ILS, inLanguage he) nested in the page's `WebPage`; no rating markup.

**T2. "Penthouse, mini penthouse, roof apartment, duplex, garden apartment" comparison** (glossary)
- A table with one column per type and rows: where in the building; what is attached in the bylaws (roof, yard, terrace); typical outdoor area (with the source of each number); rights to build on the roof; typical premium over a regular home (only sourced numbers: hon.co.il "about 30% and up" is weak, show it as "estimates in articles" or omit); typical upkeep (sealing, shading, pool load); who it suits; what to check. Five quick questions ("do you want one level?", "do you need a garden at ground level?", "will you host on the roof?", ...) highlight the matching column.
- Sources: Wikipedia (Israeli split), unadlan 2017 (30 m²), ynet 2013 (25 m² per the appraisers' chair), Bizportal 2023 (coefficient 0.2-0.5), broker-re 2022 (definitions of loft, duplex, triplex, garden duplex, roof apartment), kfirhy-law (bylaws).
- Structured data: `DefinedTermSet` "סוגי דירות מיוחדות" with one `DefinedTerm` per type (name, description, inDefinedTermSet), plus `FAQPage` for the PAA questions (מה ההבדל בין מיני פנטהאוז לפנטהאוז? / מהי ההגדרה של פנטהאוז? / מה ההבדל העיקרי בין דופלקס לפנטהאוז? / מה מקור המילה "פנטהאוז"? / כמה עולה פנטהאוז בתל אביב?). The page already carries `DefinedTerm` and `DefinedTermSet` [src]; extend them.

**T3. North Tel Aviv penthouse price table from public deals** (prices page; one row reused on the listing)
- Source: Israel Tax Authority deals (nadlan.gov.il), Tel Aviv-Yafo. Types "דירת גג", "דירת גג (פנטהאוז)", "פנטהאוז", "מיני פנטהאוז". Many penthouses are registered as "דירה בבית קומות"; a second, clearly labelled column may add "top-floor deals" (FLOORNO equal to BUILDINGFLOORS, text normalised), never mixed into the first.
- Method: geocode to the municipal address layer and drop into the city's neighbourhood polygons (the logic of `tools/deals/build_tlv_neighborhoods.py`, with "דירת גג (פנטהאוז)" added); show deals count, median price, median m², median ILS per m², range, latest deal date; hide a median under 5 deals ("not enough deals"); the m² is the registered area, which usually excludes terraces, and the table says so.
- Freshness: our local copy (downloaded 6.9.2026) has roof-type deals only up to 25.2.2024. A fresh pull is required; the table shows "updated <date>" and the date range.
- What the current copy shows (illustration only, not for publishing; 72 roof-type deals in Tel Aviv-Yafo, 21.1.2021 to 25.2.2024):

| Neighbourhood | Deals | Median price ₪ | Median m² | Median ₪/m² | Range ₪/m² |
|---|---|---|---|---|---|
| לב תל-אביב | 13 | 9,150,000 | 112 | 71,835 | 6,284-313,159 |
| 'רמת אביב ג | 9 | 8,700,000 | 203 | 52,473 | 40,573-71,698 |
| (not geocoded) | 8 | 9,000,000 | 148 | 60,601 | 34,764-87,792 |
| הצפון הישן-החלק הדרומי | 6 | 8,650,000 | 130 | 58,879 | 42,623-94,145 |
| בבלי | 6 | 6,373,000 | 98 | 72,305 | 54,298-100,730 |
| הצפון החדש - החלק הצפוני | 6 | 8,332,500 | 122 | 72,816 | 67,080-76,442 |
| הצפון הישן - החלק הצפוני | 5 | 14,000,000 | 198 | 87,436 | 70,707-136,842 |
| נוה אביבים וסביבתה | 3 | 8,100,000 | 152 | 49,908 | 40,211-59,762 |
| גני צהלה, רמות צהלה | 3 | 4,125,000 | 98 | 38,410 | 26,108-45,797 |
| נופי ים | 2 | 11,830,000 | 234 | 48,364 | 42,909-53,818 |
| כוכב הצפון | 2 | 8,700,000 | 153 | 56,606 | 55,721-57,491 |
| נחלת יצחק | 2 | 6,264,500 | 120 | 51,267 | 48,120-54,413 |
| הצפון החדש-סביבת ככר המדינה | 2 | 8,225,000 | 126 | 72,363 | 55,000-89,726 |
| 'תכנית ל | 1 | 5,500,000 | 120 | 45,757 | 45,757-45,757 |
| הצפון החדש-החלק הדרומי | 1 | 15,350,000 | 230 | 66,739 | 66,739-66,739 |
| שפירא | 1 | 3,500,000 | 99 | 35,504 | 35,504-35,504 |
| רמת-אביב | 1 | 5,900,000 | 43 | 137,529 | 137,529-137,529 |
| נוה דן | 1 | 3,050,000 | 206 | 14,806 | 14,806-14,806 |

All 72 deals: median 63,684 ILS per registered m² [calc]. Source: Tax Authority deals, owner download 6.9.2026; types דירת גג, דירת גג (פנטהאוז), מיני פנטהאוז; 8 deals could not be placed on the address layer.

- Kochav HaTzafon itself: two roof-type deals in that window, Galili Israel 12 (22.3.2022, 9,900,000 ILS, 172 m², 57,491 per m², floors 7-8 of 8) and Bonei HaIr 3 (2.1.2022, 7,500,000 ILS, 135 m², 55,721 per m², floors 8-9 of 8) [src, CSV]. Street names only, no developer names.
- Data quality seen: some rows look mislabelled (one building shows "דירת גג (פנטהאוז)" on floor 1 of 7); outliers from 6,284 to 313,159 ILS per m² in לב תל-אביב. Median, not mean, and a manual check of the top and bottom rows before every refresh.
- Structured data: `Dataset` (name, description, temporalCoverage "2021-01/2024-02" or the fresh range, spatialCoverage Tel Aviv-Yafo, creator nad-lan.co.il, isBasedOn https://www.nadlan.gov.il, variableMeasured "median price per m²"), with the visible HTML table.

**T4. Terrace and exposure guide with a permit checklist** (glossary; one short block on the listing)
- Part 1, usability: inputs orientation (N, S, E, W and the corners), floor, terrace depth in metres, shade (pergola allowed?), wind. Outputs plain notes: hours of sun, summer heat, winter wind, whether a 2.5 m deep strip fits a dining table. No invented numbers; where no source exists, the note is qualitative.
- Part 2, the permit and the bylaws: what to request and where: the building permit and plans (תיק בניין, in Tel Aviv through the municipality's engineering archive), the Tabu extract and the condominium order with the bylaws and the plan (תשריט) showing what is attached to the home, whether roof rights are attached or common, any warning notes, form 4 / completion certificate, open enforcement files; for TAMA 38 or urban-renewal buildings, who owns future roof rights. The legal rules as stated by kfirhy-law and ravit-law (section 6.4), each to be checked by the site's lawyer before publishing.
- Structured data: `HowTo` for the checklist (Google no longer shows HowTo rich results, but the markup still helps AI answers read the steps) and `FAQPage` lines.

**T5. "Is it a real mini penthouse?" test** (glossary; the listing shows its own result)
- Inputs: the home's floor and the building's top floor; terrace m²; built m²; the built m² of a regular home with the same rooms in the building (optional); ceiling height (optional); roof rights attached (yes/no/unknown).
- Score and plain verdict against sourced thresholds: terrace at least 25 m² (ynet 2013, appraisers' chair) and 30 m² (unadlan 2017); on one of the two top floors; larger built area than the typical unit; the price per weighted m² from T1 against the neighbourhood median from T3.
- The listing's own result, once the facts are settled: floor 11 of 12, terrace [confirmed] m², about three times the 25 m² threshold.
- This answers the AI Overview's "marketing trick" line with a test, which no ranking page offers.
- Structured data: part of the page's `WebApplication` or a second `WebApplication` block; no fake reviews or ratings.

### 7.5 Structured data per page (summary)

| Page | Keep | Add | Fix |
|---|---|---|---|
| Listing (HE) | Apartment, Offer, FAQPage, BreadcrumbList, RealEstateListing | VideoObject if the film is published | two `floorSize` values (197 and 190) in one page; one settled number everywhere |
| Listing (EN) | RealEstateListing, Apartment, Offer, FAQPage | BreadcrumbList; VideoObject | same numbers as HE |
| Glossary | Article, DefinedTerm, DefinedTermSet, BreadcrumbList | FAQPage, more DefinedTerm, HowTo (T4), WebApplication (T5) | dateModified to the rewrite date |
| Prices page | WebPage | Article, FAQPage (its five questions are already on the page), Dataset (T3), WebApplication (T1), BreadcrumbList | |

### 7.6 Measurement

Search Console per page, 28 days before and after each change, with the reported queries above as the baseline: "פנטהאוז" at position 75, "מיני פנטהאוז הגדרה" at 33 and 77, no reported query on the listing. Re-pull the 10 SERPs 6 weeks after the glossary goes live.

---
## 8. Not found (and where we looked)

- A penthouse sale inside Kochav HaTzafon after 2.2024: our deals copy stops there; value-pack.md also found none in Bizportal, Globes, Madlan, nadlancenter.
- Tax Authority deals for 2025-2026 (any type, Tel Aviv): not in the local copy (1 and 2 rows); nadlan.gov.il sits behind a bot check and was not bypassed.
- An official Israeli coefficient for weighting balconies or roofs in price per m²: not found. Ranges seen: 0.2 to 0.5 (appraiser Omid Soleimani, Bizportal 4.10.2023); ynet 2013's breakdown implies 0.5 (10,000 ILS per m² of balcony vs 20,000 per m² inside).
- A legal definition of "פנטהאוז" or "מיני פנטהאוז" in Israeli law or appraisal standards: not found. Wikipedia and ynet both say there is no binding professional definition.
- Penthouse prices by city outside Tel Aviv from deal data: not pulled (no local data). The brief marks them "not found" unless the owner supplies a fresh pull.
- Search volume for the spellings "פנטהאוס", "פנטאוז", "פנטהוז": no data (folded into "פנטהאוז").
- Yad2's penthouse category content: blocked by a bot wall (Radware). Seen only in SERP snippets.
- Madlan pages by plain fetch: HTTP 403. The Tel Aviv page was read through DataForSEO content parsing; the national and neighbourhood pages only in snippets.
- People also ask on "פנטהאוז", "פנטהאוז למכירה", "פנטהאוז תל אביב", "מה זה פנטהאוז", "דירות פנטהאוז", "דירת גג": absent in the pulls.
- AI Overview on "פנטהאוז" and on the English "penthouse tel aviv": absent in the pulls.

---

## 9. The brief for the owner's ChatGPT: the Hebrew penthouse encyclopedia (task 5)

Copy everything inside the block into ChatGPT Pro as is. It rewrites the existing page in place (same URL); it does not create a page.

```text
אתה כותב תוכן נדל"ן בכיר בעברית. המשימה: לכתוב מחדש את הדף הקיים
https://nad-lan.co.il/glossary/penthouse/
כך שיהיה המדריך המלא והמדויק ביותר בעברית על פנטהאוז, מיני פנטהאוז ודירת גג.
הכתובת לא משתנה. לא פותחים דף חדש.

מי קורא
קונה ישראלי שמתלבט אם לקנות פנטהאוז, מיני פנטהאוז או דירת גג, ורוצה להבין מה הוא באמת מקבל.
גם מי שרק שאל בגוגל "מה זה פנטהאוז" צריך לקבל תשובה ברורה בשורה הראשונה.

מה הדף צריך לענות עליו (לפי מה שאנשים מחפשים בגוגל)
- פנטהאוז, 3,600 חיפושים בחודש
- מה זה פנטהאוז, 110
- מיני פנטהאוז, 170. מה זה מיני פנטהאוז, 50. מיני פנטהאוז הגדרה, 30
- דירת גג, 90. מה ההבדל בין דירת גג לפנטהאוז
- דירת פנטהאוז, 90. דירות פנטהאוז, 110
- מה זה דופלקס, 320. מה ההבדל בין פנטהאוז לדופלקס
- מה זה דירת גן, 70. פנטהאוז או דירת גן
- יתרונות וחסרונות של פנטהאוז. מה מותר לבנות במרפסת פנטהאוז
- כמה עולה פנטהאוז, כמה עולה פנטהאוז בתל אביב, מחיר למטר מרפסת
השאלות שגוגל מציג בתיבת "אנשים שואלים גם":
- מה ההבדל בין מיני פנטהאוז לפנטהאוז?
- מהי ההגדרה של פנטהאוז?
- מה ההבדל העיקרי בין דופלקס לפנטהאוז?
- מהי ההגדרה של דופלקס?
- מה מקור המילה "פנטהאוז"?
- כמה עולה פנטהאוז בתל אביב?

מה גוגל עונה היום (התשובה האוטומטית שלו), כדי שתעשה טוב ממנה
- על "מיני פנטהאוז": זה מונח שיווקי, דירה גדולה קומה או שתיים מתחת לפנטהאוז,
  מרפסת של 25 עד 30 מ"ר ומעלה, ושמאים רבים אומרים שלעיתים זה תעלול שיווקי.
- על "מה זה פנטהאוז": דירת יוקרה בקומה העליונה, מרפסת גדולה, אין שכנים מעל, נוף פתוח,
  ובדרך כלל הדירה היקרה בבניין.
- על "דירת גג": דירה בקומה העליונה עם גג פרטי שעולים אליו במדרגות פנימיות, שונה מפנטהאוז שהוא מפלס אחד.
הדף שלנו צריך לתת את אותן תשובות בשורה הראשונה של כל פרק, ואז ללכת הרבה יותר עמוק: מספרים, טבלאות, מסמכים, בדיקות.

מה יש אצל המתחרים (מחקר פנימי בלבד, לא לצטט אותם בדף ולא לקשר אליהם)
- ויקיפדיה: הגדרה קצרה מאוד. פנטהאוז הוא דירה בקומה העליונה עם מרפסת גג צמודה.
  בישראל מבחינים בין פנטהאוז, מפלס אחד עם מרפסת גג ליד הסלון וגדול מהדירות שמתחתיו,
  לבין דירת גג, דירה בגודל של הדירות שמתחת עם הגג מעליה ומדרגות פנימיות אליו. אין הגדרה מקצועית מחייבת.
- hon.co.il: מאמר מ-2016 על יתרונות וחסרונות: פרטיות, נוף, אור, שטח חוץ; מול שכנים, תלות במעלית,
  מרחק לחניה ותכנון מוגבל. אומר שפנטהאוז יקר "בכ-30% ומעלה" מדירה דומה, בלי מקור.
- unadlan.co.il (2017): מיני פנטהאוז הוא מונח שיווקי. כדי שיהיה ראוי לשם: קומות עליונות,
  מרפסת שמש של 30 מ"ר ומעלה ופרטיות. זכויות בגג קיימות רק אם התקנון מצמיד אותן.
- ynet (2013): בדיקה שמצאה הפרש של 3 מ"ר בלבד בין "מיני פנטהאוז" לדירה רגילה,
  ופער של 150 אלף ש"ח. יו"ר לשכת שמאי המקרקעין דאז אמר שאין הגדרה מקצועית,
  אבל מקובל שמיני פנטהאוז נהנה ממרפסת של 25 מ"ר לפחות, וזה הנוהג בפרויקטים בצפון תל אביב.
- ביזפורטל (2023): שמאי מקרקעין אמר שמקדם השווי של מרפסת נע בין 0.2 ל-0.5 משווי מטר בנוי,
  לפי גודל, שכונה ותועלת.
- אתר עורכי דין (2019): פסק דין של בית המשפט המחוזי בירושלים חייב יזם לרשום בתקנון הבית המשותף
  שהפנטהאוזים בקומה האחרונה ושאסור להוסיף קומות. התקנון גובר על הסכם המכר אם הקונה לא רשם מחאה.
  לבנות על הגג צריך הסכמה של כל בעלי הדירות.
- אתר עורכי דין (2023): בתמ"א 38 בודקים במסמכי הרישום למי שייכות זכויות הבנייה העתידיות בגג.
מה חסר לכולם: אין טבלת השוואה, אין רשימת מסמכים מסודרת, אין מספרים עם תאריך,
אין בדיקה פשוטה "האם זה באמת מיני פנטהאוז". שם אנחנו מנצחים.

מבנה הדף
1. פסקת פתיחה של 3 עד 4 משפטים: מה זה פנטהאוז, במילים פשוטות, מיד אחרי הכותרת.
   אחריה שורה קצרה אחת למה הדף הזה שונה (מספרים, מסמכים, בדיקות).
2. מה זה פנטהאוז: ההגדרה, מקור המילה (penthouse, מבנה צמוד לבניין), ומה מקובל בישראל.
3. מיני פנטהאוז: מה זה, ממה הוא שונה מפנטהאוז ומדירה רגילה, ולמה גוגל ושמאים אומרים
   שלפעמים זה רק שם. כאן הבדיקה בחמישה צעדים: באיזו קומה ביחס לקומה העליונה, כמה מטר מרפסת
   (25 מ"ר לפחות לפי יו"ר לשכת השמאים ב-2013, 30 מ"ר לפי מדריך מ-2017), האם השטח הבנוי גדול
   מדירה רגילה עם אותו מספר חדרים, תקרה גבוהה יותר אם יש, ומה רשום בתקנון.
   לא לנקוב בשמות של חברות או פרויקטים כשמתארים תעלולי שיווק.
4. דירת גג: מה זה, ההבדל מפנטהאוז, ומתי מותר לבנות חדר על הגג (רק בהיתר ולפי התכנית החלה).
5. דופלקס, טריפלקס, דופלקס גן ודירת גן: הגדרה קצרה לכל אחד וקישור רעיוני לפנטהאוז.
6. טבלת השוואה אחת גדולה: פנטהאוז, מיני פנטהאוז, דירת גג, דופלקס, דירת גן.
   שורות: איפה בבניין, מה מוצמד בתקנון, שטח חוץ טיפוסי (רק עם מקור), זכויות בנייה בגג,
   פרמיה במחיר (רק אם יש מקור; אם אין, כתוב "אין נתון מבוסס"), תחזוקה, למי זה מתאים, מה בודקים.
7. גדלים: כמה מטר זה פנטהאוז. מטר בנוי, מרפסת שמש, גג מוצמד, מחסן וחניה, ואיך כל אחד נרשם.
   הסבר שהמטרים ברשות המסים הם השטח הרשום, שבדרך כלל לא כולל מרפסות.
8. מחיר: איך מחשבים מחיר למ"ר בפנטהאוז. שקלול מרפסות בשליש או בחצי משטחן (מקובל בדיווחים),
   הטווח 0.2 עד 0.5 שהזכיר שמאי, ודוגמה מספרית אחת:
   18,000,000 ש"ח, 190 מ"ר בנוי, 78 מ"ר מרפסות:
   94,737 ש"ח למ"ר בנוי; בשקלול שליש 216 מ"ר ו-83,333 ש"ח למ"ר; בשקלול חצי 229 מ"ר ו-78,603 ש"ח למ"ר.
   הדף יכלול מחשבון שהאתר בונה; אתה רק כותב את ההסבר שמסביבו.
9. מחירים לפי עיר, עם מקור ותאריך בלבד. מה שיש לנו:
   תל אביב, עסקאות של דירות גג ופנטהאוזים ברשות המסים, ינואר 2021 עד פברואר 2024, 72 עסקאות,
   חציון של כ-63,700 ש"ח למ"ר רשום. לפי שכונה (רק שכונות עם 5 עסקאות ומעלה):
   לב תל אביב 13 עסקאות, כ-71,800 ש"ח למ"ר; רמת אביב ג' 9, כ-52,500; הצפון הישן החלק הדרומי 6, כ-58,900;
   בבלי 6, כ-72,300; הצפון החדש החלק הצפוני 6, כ-72,800; הצפון הישן החלק הצפוני 5, כ-87,400.
   מחירים מבוקשים (לא עסקאות): 12 מודעות של פנטהאוזים בתל אביב מאוקטובר 2026, חציון של כ-102,500 ש"ח
   למ"ר בנוי, מ-56,900 עד 186,100.
   כתוב תמיד "עסקאות" או "מחיר מבוקש" ואת התאריך. האתר יחליף את נתוני העסקאות בנתונים מעודכנים לפני הפרסום.
   לכל עיר אחרת (ירושלים, הרצליה, רמת גן, נתניה, ראשון לציון, אשקלון, אשדוד, חיפה, באר שבע, אילת):
   אין לנו נתון. השאר מקום מסומן "[נתוני עסקאות יתווספו]" ואל תמציא מספר.
10. מס רכישה בקנייה של פנטהאוז: המדרגות הקפואות עד 15.1.2028.
    דירה יחידה: 0% עד 1,978,745 ש"ח; 3.5% עד 2,347,040; 5% עד 6,055,070; 8% עד 20,183,565; 10% מעל.
    דירה נוספת: 8% עד 6,055,070 ו-10% מעל. עולה חדש (דירה יחידה): 0% עד 1,978,745, 0.5% עד 6,055,070.
    הוסף משפט שהמדרגות נבדקות מול הסימולטור של רשות המסים לפני כל עסקה.
    על תושב חוץ כתוב רק שהוא משלם בדרך כלל לפי מדרגות דירה נוספת ושצריך לבדוק עם יועץ מס.
11. איך בודקים את הגג והמרפסות בהיתר ובטאבו: רשימת מסמכים מסודרת.
    נסח טאבו, צו בית משותף, תקנון ותשריט (מה מוצמד לדירה), היתר הבנייה והתוכניות בתיק הבניין בעירייה,
    טופס 4 או תעודת גמר, הערות אזהרה, תיקי פיקוח על בנייה, ובבניין בתמ"א 38 או בפינוי בינוי:
    למי שייכות זכויות הבנייה בגג. הסבר בפשטות מה זה תקנון מצוי ותקנון מוסכם ולמה התקנון גובר על הסכם המכר.
    את פסק הדין תאר בלי שם התיק ובלי שמות הצדדים: "בית המשפט המחוזי בירושלים קבע ב-2018".
12. כיווני אוויר ומרפסת: מה זה אומר צפון, דרום, מזרח ומערב לשימוש במרפסת, רוח בקומות גבוהות,
    הצללה ופרגולה (רק בהיתר), בריכה על הגג (בדיקת עומסים ואיטום). בלי מספרים בלי מקור.
13. רשימת בדיקות לפני קנייה: 15 עד 20 סעיפים קצרים, מהשאלה הראשונה למתווך ועד החתימה.
14. יתרונות וחסרונות, בכנות.
15. שאלות ותשובות: כל שאלות "אנשים שואלים גם" שלמעלה, תשובה של 2 עד 4 משפטים לכל אחת.
16. סיום: שורת הנעה אחת: "לקבלת פרטים נוספים בוואטסאפ". לא לכתוב "ייעוץ חינם" בגוף הדף.

כללי כתיבה
- עברית ישראלית חיה, כמו באתר של יזם טוב: חמה, ברורה, בלי מילים טכניות ובלי סיסמאות.
  לא להשתמש במילים "אטלס" או "Atlas", ולא בסיסמאות כמו "אפס טפסים".
- כל מספר חייב לבוא מהרשימה למעלה, עם התאריך שלו. אם אין מספר, לכתוב "אין נתון" או להשמיט.
  לא להמציא מחירים, גדלים, פרמיות, תאריכים או שמות.
- לא לנקוב בשמות של חברות, יזמים או פרויקטים בהקשר שלילי.
- בלי ציטוטים ובלי קישורים למתחרים. המקורות נשמרים אצלנו.
- כל פרק פותח במשפט שעונה על השאלה, ואז מרחיב.
- כותרות משנה ברורות שכוללות את הביטוי שמחפשים (למשל "מה זה מיני פנטהאוז").
- טבלאות במקום שזה עוזר להשוות.
- אורך: 5,000 מילה נטו לפחות, בלי מילוי.
- שורת אחריות אחת קטנה בסוף: מידע כללי, לא ייעוץ משפטי, מיסויי או שמאי.

מה להחזיר
1. כותרת לדף (עד 60 תווים) שמתחילה במילה "פנטהאוז".
2. כותרת ראשית אחת לדף.
3. תיאור לגוגל של 150 עד 160 תווים.
4. גוף הדף המלא עם כותרות משנה, טבלאות ושאלות ותשובות.
5. בסוף, רשימה נפרדת של כל מספר שהשתמשת בו, ולידו המקור והתאריך מהרשימה למעלה.
```

Notes for the owner, outside the prompt:
- The brief is Hebrew only. Other languages would need new URLs with the word "penthouse", which the URL law forbids. If the owner wants them, that is his ruling first.
- Before publishing: the site's lawyer reads sections 10 and 11; the deal numbers in section 9 are replaced by a fresh Tax Authority pull (T3); the tools T2, T4, T5 are built through Claude Design.
- The listing numbers in the brief's example (190 and 78) are Madlan's; if the settled numbers differ, change the example.

---

## 10. Top 5 actions, in order

1. **Settle the listing's facts and the owner's reading of the rent order, then fix the listing.** One built area and one terrace figure everywhere (visible text, title, meta, both JSON-LD `floorSize` values, the EN twin). Owner's word on the neighbourhood rent and yield blocks. Then apply the listing title, H1, meta and first paragraph from 7.2. One page, two languages.
2. **Give /tel-aviv-penthouse-prices/ real numbers.** Fresh Tax Authority pull (add "דירת גג (פנטהאוז)" to the type list), the north Tel Aviv penthouse table (T3) and the price-per-m² and total-cost calculator with terrace weighting and purchase tax (T1), each designed first in Claude Design. Then the new title, H1 and meta, plus Article, FAQPage, Dataset and WebApplication markup.
3. **Send the brief in section 9 to the owner's ChatGPT and rebuild /glossary/penthouse/ in place** with the comparison tool (T2), the terrace and permit guide (T4) and the mini-penthouse test (T5). New title, H1 and meta from 7.2; FAQPage and extended DefinedTermSet.
4. **Link the three pages to each other** (table 7.3) once 2 and 3 are live, and ask the owner about links from the balcony guide, the purchase-tax calculator and the luxury pages.
5. **English and video.** Apply the EN listing title and meta; publish the listing film as a YouTube video with VideoObject markup on both listings, since the English and US SERPs for "penthouse tel aviv" show a video pack of listing tours. Measure every step in Search Console 28 days later against the baseline in 4.2.
