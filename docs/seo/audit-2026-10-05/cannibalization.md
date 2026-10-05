# Cannibalization map and owner URL per word (HAD-435, 5.10.2026)

Evidence: GSC query x page, 28 days (6.9-3.10, post-purge reality) and 90 days (6.7-3.10). Files:
`data/derived/cannibalization-28d.csv` (458 queries with 2+ of our URLs, 96 of them with 20+ impressions) and
`cannibalization-90d.csv` (1,349 queries, 382 with 20+ impressions). Titles, H1s and canonicals come from the
5.10 crawl (`data/crawl/`). Volume and CPC: Google Ads via DataForSEO, Israel, monthly, USD.

Rules applied: the URL word law (one word = one owner URL; no new URL may reuse an owned head word; existing slugs are
not renamed), no noindex / nofollow / Disallow as a fix (owner law), additive changes only. **Every 301 below is a
proposal that needs Ben's explicit word, URL by URL.** Fix types, cheapest first: (1) internal links with the exact
anchor to the owner, (2) re-target the loser's title/H1/intro away from the word, (3) merge content into the owner,
(4) 301 the loser to the owner (owner's word).

## 0. What is already solved (no action)

- **The /city/ layer (410 since 25.8) and `?city=` filter URLs** caused most of the 90-day conflicts (192 groups in the
  August analysis). In the last 28 days they get no impressions: the `?city=` URLs carry a canonical to /projects/ and
  /city/ answers 410. The cost is that their demand now lands on /projects/ (see family B).
- **http vs https twins** (e.g. http://.../projects/duo-tel-aviv/ 391 impressions): the 308 is live; Google is folding
  them. No action.
- **"nadlan" across /, /en/, /ru/, /fr/**: hreflang doing its job (each language gets its own home). No action.

## 1. Families ranked by money at stake

### A. Sde Dov (our richest money cluster, split across 4-6 URLs) - FIX FIRST
| query | Ads vol | CPC $ | 28d: who gets it (impr, pos) |
|---|---:|---:|---|
| שדה דב | 4,400 | 4.92 | /sde-dov/ 115i p18; ashira-en, luxury-2026 1i each |
| שדה דב פרויקטים | 390 | 13.87 | /sde-dov/ 19i p42; /sde-dov-luxury-projects-2026/ 10i p85; /sde-dov/prices/ 6i p32; /premium/ 4i; /sde-dov/merkaz/ 1i |
| פרויקט שדה דב | 210 | 15.49 | (90d) /sde-dov/merkaz/ 81i p45 vs /sde-dov/ 71i p46 vs luxury-2026 14i |
| פרויקטים בשדה דב | 70 | 30.18 | /sde-dov/ 16i p39; /premium/ 9i; /sde-dov/prices/ 9i p27; merkaz 1i |
| שדה דב תל אביב | 320 | 8.64 | /sde-dov/ 29i p28; luxury-2026 4i p64; merkaz 1i |
| דירות למכירה בשדה דב | 40 | 11.73 | /sde-dov/ 52i **p36** vs /sde-dov/prices/ 35i **p18** |
| דירות בשדה דב / שדה דב דירות | 50 / 50 | 10.25 / 13.0 | /sde-dov/ p44-46 vs /sde-dov/prices/ **p12-18** vs home |
| שדה דב למכירה | 70 | 6.25 | /sde-dov/ p39 vs /sde-dov/prices/ **p18** vs home p51 |
| גינדי שדה דב | 480 | 13.72 | /sde-dov/ 15i p34 (the Hebrew Gindi Vogue project page is not shown at all) |

Diagnosis: the hub's title promises "כל הפרויקטים, המחירים והדירות למכירה", so it competes with its own prices page,
which Google already prefers for every "for sale / apartments" query. The project intent is split between the hub,
/sde-dov/merkaz/ and the thin /sde-dov-luxury-projects-2026/ (437 words). Project-name queries ("גינדי שדה דב") fall
on the hub because the project page's title leads with Latin "GINDI VOGUE" and the spelling "פרוייקט".

**Owner per word:**
- /sde-dov/ = "שדה דב", "רובע שדה דב", "שדה דב תל אביב", "שדה דב פרויקטים", "פרויקט(ים) (ב)שדה דב".
  Re-title away from prices: e.g. "רובע שדה דב: כל הפרויקטים, המפה והיזמים" (drop "המחירים והדירות למכירה").
- /sde-dov/prices/ = "מחירי דירות בשדה דב", "דירות למכירה בשדה דב", "דירות בשדה דב", "שדה דב למכירה", "שדה דב מחירים".
  Re-title to carry the for-sale word: e.g. "דירות למכירה בשדה דב: מחירים למ"ר ועסקאות".
- /sde-dov/merkaz/ = "מתחם המרכז שדה דב" only. Its first paragraph links to /sde-dov/ with the anchor "פרויקטים בשדה דב".
- each project page = its own name: /projects/gindi-vogue-sde-dov/ = "גינדי שדה דב", "גינדי ווג"; Dimri = "דמרי שדה דב";
  Ashira = "אשירה שדה דב"... The hub lists every project with the Hebrew name as the anchor.
- /sde-dov-luxury-projects-2026/ (437 words, competes on "projects"): **merge its unique lines into /sde-dov/ and 301 it
  to /sde-dov/ (owner's word)**. Until then: re-title it as a dated news item and link to the hub.
- /premium/ shows up on Sde Dov queries because it lists those projects; keep, no change.

### B. "New projects" generic + city intent (largest volume; no owner since the purge)
| query | Ads vol | CPC $ | 28d split |
|---|---:|---:|---|
| פרויקטים חדשים | 390 | 4.56 | /projects/ 234i p30; home 24i p79 |
| פרויקטים חדשים בתל אביב | 320 | 10.18 | /projects/ 151i p35; the TLV page /new-projects/new-projects-tel-aviv/ **absent** |
| דירות חדשות למכירה / דירות חדשות | 260 / 260 | 3.5-5.5 | /projects/ p42-45; home p63-85 |
| דירות מקבלן / דירות חדשות מקבלן | 210 / 170 | 3.7 / 5.4 | /projects/ p37-43; home p82-89 |
| פרויקטים חדשים למגורים / פרויקט נדלן חדש / פרויקטים חדשים מחירים / דירות חדשות בבניה | 10-20 each | | **/new-projects/new-projects-tel-aviv/ p13-17** beats /projects/ p24-52 |
| פרויקטים חדשים ב{city} (פתח תקווה 260, ירושלים 480, ראשון 210, רמת גן 170, חיפה 210, באר שבע 110...) | | 3.4-10.7 | /projects/ alone, p24-41 |
| איזה פרויקטים חדשים יש בהרצליה / פרויקטים חדשים בהרצליה | - / 110 | 5.0 | /herzliya-projects/ p38; /projects/ p64; /investment/herzliya-investment-apartment/ p6 |
| דירות חדשות בהרצליה | 40 | 4.42 | /herzliya-apartment-prices/ p28 (prices page answering a projects query) |

Diagnosis: /projects/ is the owner by URL law for "פרויקטים חדשים" and must stay so. The TLV page is a buying guide
("איך להשוות דירה מקבלן לפני חתימה"), not a list; Google likes it for generic phrases but will not rank it for the
TLV head term while /projects/ is the stronger page. City demand has no page at all except Herzliya.

**Owner per word:**
- /projects/ = "פרויקטים חדשים", "דירות חדשות (למכירה)", "דירות מקבלן", "פרויקטים חדשים בישראל/במרכז/על הנייר".
  Home keeps its owner-approved portal title; it links to /projects/ with the anchor "פרויקטים חדשים" (no change to its title).
- /new-projects/new-projects-tel-aviv/ = "פרויקטים חדשים בתל אביב", "דירות חדשות בתל אביב", "דירות מקבלן בתל אביב".
  Fix: add the live list of TLV projects (from the project DB) above the guide (additive), make the H1 the plain phrase,
  and on /projects/ point the TLV city filter link to this page with the anchor "פרויקטים חדשים בתל אביב".
- /new-projects/north-tel-aviv-new-projects/ = "פרויקטים חדשים בצפון תל אביב" (same treatment). /north-tel-aviv/old-north/
  = "הצפון הישן" area intent (it is orphaned today: no internal link reaches it).
- /herzliya-projects/ = "פרויקטים חדשים בהרצליה"; /herzliya-apartment-prices/ = "מחירי דירות בהרצליה";
  /investment/herzliya-investment-apartment/ = "דירה להשקעה בהרצליה". Cross-link with those exact anchors.
- Other cities: no owner exists. Creating one per city is a new-URL decision (strategy.md, item N1), not a
  cannibalization fix.

### C. Investment (highest CPC on the site)
| query | Ads vol | CPC $ | split |
|---|---:|---:|---|
| דירות להשקעה | 480 | 8.42 | /investment/ 48i p57; /properties/ 24i p53 (90d: also home) |
| השקעה נדלנית / השקעות נדלן / השקעה בנדלן | 390 / 390 / 170 | 22.8 / 22.8 / 30.2 | /investment/ p34-72; /investment/apartments-for-investment/ p81 |
| נכס להשקעה | 50 | 8.26 | /investment/ p54 |
| השקעות נדל"ן בתל אביב / במרכז / בדרום | 10-20 | | /investment/, home, /investment/apartments-for-investment/ |
| קניית דירה | 210 | 9.21 | /buying-apartment/ 42i p50; /investment/ 15i p78 |
| מכירת נכס / מכירת דירה | 20 / 140 | - / 1.67 | /selling-apartment/ p49-61; /investment/ p76-82 |

**Owner per word:** /investment/ = "נדל"ן להשקעה", "השקעה בנדל"ן", "השקעות נדל"ן", "נכס להשקעה", "דירות להשקעה".
/investment/apartments-for-investment/ is the same intent under a slug that repeats "investment": **merge into
/investment/ and 301 (owner's word; first proposed 25.8)**. /buying-apartment/ = "קניית דירה/נכס";
/selling-apartment/ = "מכירת דירה/נכס": remove buy/sell phrasing from /investment/ intro and link out with those anchors.
/properties/ must not carry "להשקעה" wording.

### D. Urban renewal
| query | Ads vol | CPC $ | split |
|---|---:|---:|---|
| פרויקט פינוי בינוי / פרויקטים פינוי בינוי | 210 / 210 | 4.03 | /projects/ 109i p33 vs /urban-renewal/map/ p48-55 |
| פרויקטים בהתחדשות עירונית / התחדשות עירונית פרויקטים | 10 / 70 | 3.81 | /projects/ p48-65 vs map p69-72 |
| מתחמי פינוי בינוי / מפת התחדשות עירונית | 70 / 260 | 1.9 / 2.8 | map p11-18 (owner, fine) |
| פרויקטי פינוי בינוי בתל אביב | - | | /urban-renewal/pinui-binui-tel-aviv/ p74, /projects/ p49 |
| תמא 38 תל אביב (+ variants) | | | /urban-renewal/tama-38-tel-aviv/ vs `/projects/?project_type=tama38` |

**Owner per word:** /urban-renewal/map/ = "מפת/מתחמי/פרויקטי פינוי בינוי", "פרויקטים בהתחדשות עירונית";
/urban-renewal/ = "התחדשות עירונית"; /urban-renewal/pinui-binui/ = "פינוי בינוי"; /urban-renewal/pinui-binui-tel-aviv/
= "פינוי בינוי בתל אביב"; /urban-renewal/tama-38-tel-aviv/ = "תמא 38 תל אביב". Fix: on /projects/ the urban-renewal
filter link goes to /urban-renewal/map/ with the anchor "פרויקטי פינוי בינוי"; the map page (703 words) gets a
server-rendered list of compounds per city so it can outrank the catalogue.

### E. Luxury Tel Aviv (four of our URLs, one word)
| query | Ads vol | CPC $ | split |
|---|---:|---:|---|
| דירות יוקרה בתל אביב | 140 | 2.18 | /property-value/luxury-apartments-tel-aviv/ 77i p42 (orphan page); /tel-aviv-luxury-apartment-prices/ p25 |
| פרויקטי יוקרה בתל אביב | - | | /luxury-tel-aviv/ 57i p74; (purged city pages) |
| מגדלי יוקרה | 40 | 2.48 | /projects/ 92i p38; /luxury-apartments-israel-guide-he/ p58; /projects/yoo-tel-aviv/ |

Pages: /luxury-tel-aviv/ ("דירות יוקרה בתל אביב - פארק בבלי...", depth 3), /tel-aviv-luxury-apartment-prices/ ("מחירי
דירות יוקרה בתל אביב"), /property-value/luxury-apartments-tel-aviv/ ("דירות יוקרה בתל אביב: בדיקות לפני רכישת
פנטהאוז", orphan), /luxury-apartments-israel-guide-he/ (Israel-wide).
**Owner per word:** /luxury-tel-aviv/ = "דירות יוקרה בתל אביב", "פרויקטי יוקרה בתל אביב", "מגדלי יוקרה בתל אביב";
/tel-aviv-luxury-apartment-prices/ = "מחירי דירות יוקרה בתל אביב"; /tel-aviv-penthouse-prices/ = "פנטהאוז בתל אביב";
/luxury-apartments-israel-guide-he/ = "דירות יוקרה בישראל". /property-value/luxury-apartments-tel-aviv/: re-target to
its real angle ("בדיקות לפני קניית דירת יוקרה") or **merge into /luxury-tel-aviv/ + 301 (owner's word)**.
This family is where Kikar Hamedina, DUO, Einstein and the Sde Dov towers must be linked from (strategy.md).

### F. Valuation tools
| query | Ads vol | CPC $ | split |
|---|---:|---:|---|
| הערכת שווי דירה / נכס / הערכת שווי | 590 / 260 / 170 | 1.3-8.8 | /property-value-estimator/ only (p20-30), fine |
| מחשבון מחיר דירה / מחירון דירות | 170 / 1,000 | 1.2 / 0.4 | estimator p17-23 vs /buy-or-rent/, /apartment-purchase-cost-calculator/, home, /selling-apartment/ |
| איך קובעים מחיר לנכס | - | | estimator p20 vs /property-value/ p74 |

**Owner:** /property-value-estimator/ = all valuation words ("הערכת שווי", "מחשבון שווי דירה", "שמאות דירה").
/property-value/ ("הערכת שווי דירה: איך בודקים...") repeats the head phrase in its title: re-title to its guide angle
and link to the estimator with the anchor "הערכת שווי דירה".

### G. Mortgage and purchase calculators
| query | Ads vol | CPC $ | split |
|---|---:|---:|---|
| "בדיקת משכנתא" | 170 | 5.08 | /mortgage-calculator/ 31i p17; /investment-property-mortgage/ 6i p28 |
| משכנתא לדירה | 50 | 5.56 | (90d) /investment-property-mortgage/ p47; /mortgage-calculator/ p74 |
| מחשבון קניית דירה | 40 | 0.90 | /apartment-purchase-cost-calculator/ p49; /buy-or-rent/ p82; /purchase-tax-calculator/ p72; /mortgage-calculator/ p95 |
| מחשבון לקנות או לשכור דירה | - | | /buy-or-rent/ p33; /buy-vs-rent/ p66; /apartment-purchase-cost-calculator/ p72 |

**Owner:** /mortgage-calculator/ = "מחשבון משכנתא", "בדיקת משכנתא", "משכנתא לדירה"; /investment-property-mortgage/ =
"משכנתא לדירה להשקעה"; /mortgage-calculator/reverse-mortgage/ = "משכנתא הפוכה" (25.8 rule stands);
/apartment-purchase-cost-calculator/ = "מחשבון קניית דירה", "עלויות רכישת דירה".
**Duplicate pair: /buy-or-rent/ (661 words) and /buy-vs-rent/ (253 words, orphan)** answer the same calculator
intent. Keep /buy-or-rent/ (it ranks better); **301 /buy-vs-rent/ -> /buy-or-rent/ (owner's word)**.

### H. English foreign-buyer guides (four URLs)
"buying property in israel", "comprar apartamento em israel sendo estrangeiro" (177 impressions), "israel mortgage for
foreigners": /en/buy-property-in-israel/ (pos 55-63), /buy-property-israel-foreign-buyers/ (pos 80),
/buying-real-estate-israel-foreign-investor/ (depth 4), /luxury-apartments-israel-guide/, /israel-mortgage-non-residents/.
**Owner:** /en/buy-property-in-israel/ = "buy property in Israel" (it sits in the /en/ hreflang tree);
/buying-real-estate-israel-foreign-investor/ = "invest in Israel real estate as a foreigner"; /israel-mortgage-non-residents/
= "Israel mortgage for non-residents". /buy-property-israel-foreign-buyers/ is the same intent as the owner:
**merge + 301 to /en/buy-property-in-israel/ (owner's word)**, or re-target it to a narrower angle (taxes and fees).

### I. Small, name-level and housekeeping
- **/site-map/ vs /sitemap/**: resolved. /sitemap/ now answers 301 to /site-map/ (checked 5.10). /site-map/ still
  takes stray impressions on "דירות", "פרויקטים להשקעה" (pos 75-94); harmless.
- **/catalog/ (orphan, 418 words) vs /projects/ vs /premium/**: three catalogue pages. /catalog/ took 710 impressions at
  p70 ("סוקולוב 14", "דירות מקבלן"). Re-target /catalog/ to "all listings, projects and pros" wording without
  "פרויקטים חדשים", or merge into /projects/ + 301 (owner's word).
- **/3-room-apartment-690k-israel-2026/ vs /affordable-apartments-israel-2026/**: the same story in Hebrew and English
  (the English one has an English title on the Hebrew site, no hreflang between them). Link them as language versions.
- **Einstein**: /projects/einstein-tower/, /projects/ashdar-einstein/, /projects/einstein-19/, /ramat-aviv/einstein/ are
  four different real things (verified titles). Not cannibalization; make sure each title carries its distinct name
  and /ramat-aviv/einstein/ links to all three projects.
- **Numeric-suffix professionals/projects (-2, -3)**: already handled 25.8 (most are different real entities).

## 2. Watch-list for the new Kikar Hamedina work (prevention)

- **Owner of "מגדלי כיכר המדינה", "כיכר המדינה דירות/מחירים/עסקאות/אכלוס"**: /projects/hamedina/ (and its 4
  language pages for their languages). No other URL may carry these words in title or H1.
- The URL word audit (5.10 sitemap snapshot): token `hamedina` is owned by the 5 Kikar pages; `kikar` is owned by
  /tel-aviv-plans/kikar-atarim/ (a different place). **Any new spoke URL carrying either token breaks the URL law**
  and would split the hub's 260/month head word. See strategy.md for the spoke design that avoids this.
- Luxury, Rova 4 and Old North pages link to the Kikar hub with the anchor "מגדלי כיכר המדינה"; they must not
  add Kikar Hamedina sections of their own beyond a short paragraph and the link.

## 3. Summary table: owner URL per money word

| word (Ads vol) | owner URL | competitors to fix |
|---|---|---|
| שדה דב (4,400), שדה דב פרויקטים (390), פרויקט שדה דב (210), שדה דב תל אביב (320) | /sde-dov/ | /sde-dov/merkaz/, /sde-dov-luxury-projects-2026/ |
| דירות למכירה בשדה דב, מחירי דירות בשדה דב | /sde-dov/prices/ | /sde-dov/ (title) |
| גינדי שדה דב (480) | /projects/gindi-vogue-sde-dov/ | /sde-dov/ |
| פרויקטים חדשים (390), דירות מקבלן (210), דירות חדשות (260) | /projects/ | home, /catalog/ |
| פרויקטים חדשים בתל אביב (320) | /new-projects/new-projects-tel-aviv/ | /projects/ |
| פרויקטים חדשים בהרצליה | /herzliya-projects/ | /projects/, prices page |
| נדל"ן להשקעה, השקעות נדל"ן (390), השקעה בנדל"ן (170), דירות להשקעה (480) | /investment/ | /investment/apartments-for-investment/, /properties/ |
| קניית דירה (210) | /buying-apartment/ | /investment/ |
| מכירת דירה (140) | /selling-apartment/ | /investment/ |
| פרויקטי פינוי בינוי (210), מפת התחדשות עירונית (260) | /urban-renewal/map/ | /projects/ |
| פינוי בינוי (9,900) | /urban-renewal/pinui-binui/ | - |
| התחדשות עירונית (8,100) | /urban-renewal/ | - |
| דירות יוקרה בתל אביב (140) | /luxury-tel-aviv/ | /property-value/luxury-apartments-tel-aviv/ |
| הערכת שווי דירה (590) | /property-value-estimator/ | /property-value/ |
| מחשבון משכנתא (40,500), בדיקת משכנתא (170) | /mortgage-calculator/ | /investment-property-mortgage/ |
| מחשבון קנייה או שכירות | /buy-or-rent/ | /buy-vs-rent/ |
| מגדלי כיכר המדינה (260) | /projects/hamedina/ | none yet: keep it that way |
