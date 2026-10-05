# Money words: volume x CPC x reachable position (HAD-435, 5.10.2026)

## Method (so the numbers can be checked)

- **Keyword set:** 224 hand-built commercial seeds (Hebrew + 40 English/Russian/French/Arabic) plus every GSC query with
  20+ impressions in the property's life (855) = 1,072 keywords, Israel. English/French seeds also checked in the US and
  France. Source: DataForSEO Google Ads `search_volume/live` (12-month average to Aug 2026, CPC in **USD**).
  Raw: `data/dfs-search-volume.csv`, `data/dfs/sv-*.json`.
- **Our position:** GSC 28-day position first, then 90-day, then DataForSEO Labs ranked keywords, and the 5.10 live
  desktop SERP (48 keywords; if we are not in its top ~20, the position used is at least 21).
- **Score:** `opportunity $/month = volume x (CTR at position 3 - CTR at current position) x CPC x reach factor x SERP factor`.
  CTR curve: 1st 28%, 2nd 15%, 3rd 10%, 4th 7%, 5th 5%, 6-10 3%, 11-20 1%, 21+ 0.2%. Reach factor by current position:
  top 10 = 0.9, 11-20 = 0.75, 21-30 = 0.5, 31-50 = 0.3, 51+ = 0.15, not ranking = 0.1. SERP factor 0.5 when 2+ of the
  top 5 are government, bank or Wikipedia. It is a **ranking device, not a revenue forecast**: CPC is what advertisers
  pay Google per click, i.e. the commercial value of the click, not our income.
- Google Ads merges close variants (e.g. "שדה דב" = "שדה דוב"; "מחשבון משכנתא" = "מחשבון משכנתאות"); the tables show one.
- Full ranked list: `data/derived/money-words-ranked.csv` (549 money keywords); families: `data/derived/money-families.csv`.

## 1. Money families (where the value sits)

| # | family | Ads vol/mo (IL) | opp $/mo | best pos now | owner URL (cannibalization.md) | the move |
|---:|---|---:|---:|---:|---|---|
| 1 | Government housing programs: מחיר למשתכן 90.5K, דירה בהנחה 74K ($3.8) | 164,500 | 6,240 | none | none | long shot: government and news own it; only a "projects in the lottery, with prices" angle could earn (new page, owner's call) |
| 2 | Mortgage calculator: מחשבון משכנתא 40.5K ($1.22), משכנתא 9.9K ($4.98) + 29 variants | 59,920 | 2,570 | 22.6 (variants), head 37-61 | /mortgage-calculator/ | bank-dominated; improve, do not bet the quarter on it |
| 3 | **Sde Dov hub**: שדה דב 4,400 ($4.92), שדה דב תל אביב 320 ($8.64), רובע שדה דב 210 | 4,970 | 1,569 | 12-18 | /sde-dov/ | **fix the split (cannibalization A), title away from prices, hub links every project by its Hebrew name** |
| 4 | **New projects by city** (Jerusalem 480, Petah Tikva 260, Rishon 210 at $10.65, Ramat Gan 170, Haifa 210, Bat Yam 110 at $7.49...) 60 keywords | 6,000 | 1,179 | 8 (Bat Yam via `?city=`), else 24-50 | **none since the 25.8 purge** | the largest generic gap; needs the owner's decision on city pages (strategy.md N1) |
| 5 | Listings: דירות למכירה 5,400 + city variants | 25,950 | 1,077 | 24+ | /properties/ (7 demo listings) | needs inventory (brokers track), not content |
| 6 | Home head term: נדלן 8,100 ($7.55) | 8,100 | 899 | 54-63 | / | authority game; home is owner-canon copy; win through internal links and brand |
| 7 | **Home inspection**: בדק בית 3,600 ($13.99), בדק בית מחיר 480 ($7.61) | 4,580 | 841 | 43-68 | /home-inspection/ | pros-network money word and the Kikar 2027 handover wave; rebuild as a service hub with inspectors from the directory |
| 8 | **Sde Dov in English**: sde dov 390 IL ($6.84) + 320 US ($25.97) | 390 (+320 US) | 741 | 17 (via ashira-en) | none: an English twin of /sde-dov/ | add the English language version of the hub (hreflang twin, owner's word on the slug) |
| 9 | New projects generic: פרויקטים 1,600, פרויקטים חדשים 390, דירות חדשות 260, דירות מקבלן 210 | 4,220 | 636 | 26-54 | /projects/ | directory signals: counts, city sections, fresh "בשיווק עכשיו" block, FAQ |
| 10 | **Investment**: דירות להשקעה 480 ($8.42), השקעה נדלנית 390 ($22.79), השקעה בנדלן 170 ($30.21) | 1,870 | 565 | 23-72 | /investment/ | merge the child (cannibalization C), one strong hub, add the yield calculator link |
| 11 | **DUO**: duo 1,000 ($9.34), duo tel aviv 260, duo תל אביב 210 | 1,490 | 543 | 8-23 | /projects/duo-tel-aviv/ | already #2 click page; answer the PAA (address, average price, what is DUO), progress updates |
| 12 | Mortgage adviser: יועץ משכנתאות 3,600 ($12.77) | 3,600 | 460 | none | none (pros category page) | a pros category page if the directory has advisers (new URL, URL check) |
| 13 | **Rainbow**: ריינבו 1,300, ריינבו תל-אביב 480 ($5.34), rainbow tel aviv 170 | 2,400 | 436 | 10-17 | /projects/rainbow-tel-aviv/ | close to page 1; title spelling "ריינבו תל אביב" first |
| 14 | Urban renewal head: התחדשות עירונית 8,100 ($4.86) | 8,100 | 394 | not top 20 | /urban-renewal/ | law-firm and government SERP; the map is our edge |
| 15 | Pinui binui head: פינוי בינוי 9,900 ($3.61) | 10,070 | 383 | 34 | /urban-renewal/pinui-binui/ | same |
| 16 | Appraiser: שמאי מקרקעין 2,400 ($8.62), שמאי מכריע 1,900 ($7.05) | 5,400 | 378 | 30-58 | /real-estate-appraiser/ + glossary | pros-network money; appraisers by city from the directory |
| 17 | Valuation: הערכת שווי דירה 590, בחינם 590, כמה שווה הדירה שלי 480, שמאות דירה 170 ($11.36) | 2,940 | 365 | 15-21 | /property-value-estimator/ | our #1 click page; step change = address-level deal data |
| 18 | **New projects in Tel Aviv**: פרויקטים חדשים בתל אביב 320 ($10.18), פרויקט תל אביב 260, פרויקטים בתל אביב 140 | 1,100 | 351 | 20-42 | /new-projects/new-projects-tel-aviv/ | give the TLV page the live TLV project list (cannibalization B) |
| 19 | Reverse mortgage: משכנתא הפוכה 2,900 ($8.36) | 3,400 | 324 | 11 (variant) | /mortgage-calculator/reverse-mortgage/ | 25.8 parent/child rule |
| 20 | Purchase tax: מס רכישה 6,600 ($4.27), מחשבון מס רכישה 4,400 | 13,520 | 312 | 53-59 | /purchase-tax-calculator/ | 2026 brackets in title + first screen; the ranking calculators are single-purpose and simple |
| 21 | Tabu extract: נסח טאבו 49,500 ($0.33) | 55,980 | 312 | 23-58 | /tabu-extract-check/ | low CPC, huge volume; law-firm SERP |
| 22 | Real-estate lawyer: עורך דין מקרקעין 1,600 ($12.98), עורך דין נדלן 590 ($13.82) | 2,230 | 304 | 41-49 | /real-estate-lawyer/ | pros-network money (lawyer pool); "lawyers by city" from the directory |
| 23 | **Sde Dov projects**: שדה דב פרויקטים 390 ($13.87), פרויקט שדה דב 210 ($15.49), פרויקטים בשדה דב 70 ($30.18) | 710 | 266 | 35-48 | /sde-dov/ | the highest CPC cluster we touch; fix the split |
| 24 | **Dimri Yama**: דמרי שדה דב 210 ($17.51), dimri yama 70 ($24.53) | 280 | 216 | 8.5 (EN), 32 (HE) | /projects/dimri-yama-sde-dov/ | Hebrew title must start "דמרי" (the searched spelling) |
| 25 | Offices: משרדים להשכרה 1,000 ($15.24), משרדים למכירה 390 ($13.16) | 1,390 | 204 | none | /commercial-real-estate/office-for-rent/ | listing engines win; our office price guides win only long tail |
| 26 | **Gindi Vogue**: גינדי שדה דב 480 ($13.72) | 510 | 197 | 34 (hub, not the project page) | /projects/gindi-vogue-sde-dov/ | retitle the project page in Hebrew first; hub anchor "גינדי שדה דב" |
| 27 | Rentals: דירות להשכרה 27,100 ($0.65) | 30,000 | 197 | none | none | rentals product, not SEO, for now |
| 28 | Penthouses: פנטהאוזים 3,600, פנטהאוז למכירה בתל אביב 110 ($8.0) | 3,990 | 170 | 29 (glossary) | /tel-aviv-penthouse-prices/ | the glossary ranks instead of the prices page; link and retitle |
| 29 | Capital gains: מס שבח 3,600, מחשבון מס שבח 1,600 | 5,200 | 120 | none | /real-estate-tax-advisor/capital-gains-tax-guide/ | Kikar landowners (P13) are the hook |
| 30 | English portal terms (US): israel real estate 720 ($5.57), tel aviv real estate 480, apartments for sale in tel aviv 390 | (US) | 116 | none | /en/ | foreign luxury buyers; /en/ project pages already rank 4-8 |
| 31 | Sde Dov for sale/prices: שדה דב למכירה 70, דירות בשדה דב 50 ($10.25), שדה דב דירות 50 ($13.0) | 260 | 94 | 7-18 | /sde-dov/prices/ | already the page Google prefers; make it the owner |
| 32 | Urban renewal map/projects: מפת התחדשות עירונית 260, פרויקט פינוי בינוי 210 | 630 | 91 | 11 | /urban-renewal/map/ | strongest urban-renewal asset; add the compounds list |
| 33 | Ashira: אשירה שדה דב 90, אביסרור שדה דב 90 | 200 | 83 | 14 | /projects/ashira-sde-dov/ | |
| 34 | Brokers: מתווך 720, מתווך נדלן 320, משרד תיווך 320 ($5-6) | 1,360 | 82 | none | /brokers/ | broker platform (HAD-394) |
| 35 | Yield calculator: מחשבון תשואה 2,400 ($2.59) | 2,400 | 62 | none | /investment-property-cashflow-calculator/ | page exists; retitle to the searched words |
| 36 | TAMA 38: תמא 38 1,000 | 1,140 | 60 | 46 | /urban-renewal/tama-38/ | |
| 37 | **Kikar Hamedina**: מגדלי כיכר המדינה 260 ($3.52), kikar hamedina towers 320 ($2.42), kikar hamedina 260 | 6,410 (5,400 is the square) | 59 | 40 (new page) | /projects/hamedina/ + /projects/hamedina-en/ | low $ today, but the weakest SERP of all 48 and the 2027 owners wave; see strategy.md |
| 38 | Developers: חברות בנייה 720 ($6.88) | 800 | 52 | 83 | developers directory | |
| 39 | Lease contract: חוזה שכירות 3,600 | 4,080 | 48 | none | /residential-lease-agreement/ (missing from sitemap in Aug) | rentals module lead-in |
| 40 | Property management: ניהול נכסים 320, חברת ניהול נכסים 210 | 670 | 38 | 65 | /property-management/ | rentals business (HAD-383); the Kikar wait-to-sell owners |

Also on the list but below 40: luxury TLV (דירות יוקרה 320, מגדלי יוקרה בתל אביב 90; $23/mo), נדלן בחול 170 ($19.65),
ביטוח נכס 90 ($41.74), עסקת קומבינציה 260 ($15.54), קניית דירה 210 ($9.21).

## 2. Top 40 single keywords (Israel unless marked)

| # | keyword | vol | CPC $ | our pos | our page now | owner URL | opp $ |
|---:|---|---:|---:|---:|---|---|---:|
| 1 | מחיר למשתכן | 90,500 | 3.78 | - | - | none (new page idea) | 3,421 |
| 2 | דירה בהנחה | 74,000 | 3.81 | - | - | none (new page idea) | 2,819 |
| 3 | שדה דב | 4,400 | 4.92 | 18 (GSC 28d); not desktop top 20 | /sde-dov/ | /sde-dov/ | 1,461 |
| 4 | מחשבון משכנתא | 40,500 | 1.22 | 37-56 | /mortgage-calculator/ | same | 1,453 |
| 5 | נדלן | 8,100 | 7.55 | 54-63 | / | / | 899 |
| 6 | בדק בית | 3,600 | 13.99 | 60-68 | /home-inspection/ | same | 740 |
| 7 | משכנתא | 9,900 | 4.98 | 61 | /mortgage-calculator/ | same | 725 |
| 8 | דירות למכירה | 5,400 | 2.29 | 24+ | /properties/ | same (inventory) | 606 |
| 9 | sde dov (US) | 320 | 25.97 | 17 | /projects/ashira-sde-dov-en/ | English twin of /sde-dov/ | 561 |
| 10 | יועץ משכנתאות | 3,600 | 12.77 | - | - | pros category (new) | 460 |
| 11 | duo | 1,000 | 9.34 | 23 | /projects/duo-tel-aviv/ | same | 458 |
| 12 | התחדשות עירונית | 8,100 | 4.86 | - | - | /urban-renewal/ | 394 |
| 13 | פינוי בינוי | 9,900 | 3.61 | - | - | /urban-renewal/pinui-binui/ | 357 |
| 14 | מס רכישה | 6,600 | 4.27 | - | - | /purchase-tax-calculator/ | 282 |
| 15 | השקעה נדלנית / השקעות נדלן | 390 | 22.79 | 45-72 | /investment/ | /investment/ | 261 |
| 16 | משכנתא הפוכה | 2,900 | 8.36 | - | - | /mortgage-calculator/reverse-mortgage/ | 242 |
| 17 | נסח טאבו | 49,500 | 0.33 | 58 | /tabu-extract-check/ | same | 240 |
| 18 | עורך דין מקרקעין | 1,600 | 12.98 | - | - | /real-estate-lawyer/ | 208 |
| 19 | שמאי מכריע | 1,900 | 7.05 | 58 | /glossary/שמאי-מכריע/ | same | 197 |
| 20 | גינדי שדה דב | 480 | 13.72 | 34 | /sde-dov/ | /projects/gindi-vogue-sde-dov/ | 194 |
| 21 | sde dov (IL) | 390 | 6.84 | 17 | /projects/ashira-sde-dov-en/ | English twin of /sde-dov/ | 180 |
| 22 | דירות להשכרה | 27,100 | 0.65 | - | - | none | 176 |
| 23 | ריינבו תל אביב | 480 | 5.34 | 11-17 | /projects/rainbow-tel-aviv/ | same | 173 |
| 24 | פנטהאוזים | 3,600 | 0.87 | 29 | /glossary/penthouse/ | /tel-aviv-penthouse-prices/ | 154 |
| 25 | משרדים להשכרה | 1,000 | 15.24 | - | - | /commercial-real-estate/office-for-rent/ | 152 |
| 26 | השקעה בנדלן | 170 | 30.21 | 47 | /investment/ | same | 151 |
| 27 | שמאות דירה | 170 | 11.36 | 20 | /property-value-estimator/ | same | 130 |
| 28 | פרויקטים | 1,600 | 4.87 | 54 | /projects/ | same | 115 |
| 29 | dimri yama | 70 | 24.53 | 8.5 | /projects/dimri-yama-sde-dov/ | same | 108 |
| 30 | דמרי שדה דב | 210 | 17.51 | 32 | /projects/dimri-yama-sde-dov/ | same | 108 |
| 31 | שמאי מקרקעין | 2,400 | 8.62 | - | - | /real-estate-appraiser/ | 103 |
| 32 | מס שבח | 3,600 | 2.69 | - | - | capital-gains guide | 97 |
| 33 | פרויקטים חדשים בתל אביב | 320 | 10.18 | 35 | /projects/ | /new-projects/new-projects-tel-aviv/ | 96 |
| 34 | פרויקט שדה דב | 210 | 15.49 | 48 | /sde-dov/merkaz/ | /sde-dov/ | 96 |
| 35 | פרויקט תל אביב | 260 | 6.62 | 27 | /projects/ | TLV page | 84 |
| 36 | פרויקטים חדשים בירושלים | 480 | 5.91 | 36 | /projects/ | none (city page) | 83 |
| 37 | עורך דין נדלן | 590 | 13.82 | - | - | /real-estate-lawyer/ | 82 |
| 38 | שדה דב תל אביב | 320 | 8.64 | 32 | /sde-dov/ | same | 81 |
| 39 | שדה דב פרויקטים | 390 | 13.87 | 55 | /sde-dov/merkaz/ | /sde-dov/ | 80 |
| 40 | פרויקטים חדשים בפתח תקווה | 260 | 6.12 | 24 | /projects/ | none (city page) | 78 |

## 3. What the money map says

1. **The Sde Dov cluster is the best money-per-effort on the site**: 14 hub, project and for-sale keywords with about
   5,900 searches a month (6,300 with the English "sde dov", 9,700 with the project names), CPCs from $4.9 to $30,
   and we already rank 7-18 on half of them. Every fix there is a title, an H1 or an anchor
   (cannibalization A), not new content.
2. **Project-name words are the fastest wins** (DUO, Rainbow, Dimri, Gindi, Ashira): positions 8-34, CPCs $5-25, and
   the fix is mostly Hebrew-first titles with the searched spelling and hub anchors.
3. **City new-project demand is the biggest generic gap** (60 keywords, 6,000 searches, CPC up to $10.65) and has had no
   owner since the purge. Only the owner can decide whether to bring back city pages and in which form.
4. **Pros-network words carry the highest CPCs** (בדק בית $14, עורך דין מקרקעין $13, יועץ משכנתאות $12.8, שמאי מקרקעין
   $8.6). They match the paid Pro product: a service-by-city directory page per profession turns the 2,847 professional
   pages into money pages.
5. **Kikar Hamedina is small in dollars today** (260 + 320 English) but the SERP is open (no portal, no project page in
   the top 10) and the 2027 handover wave (about 250 owners, 453 apartments) is a supply event worth owning now.
6. Head tools (mortgage, purchase tax, tabu) are big but bank/government/law-firm territory; keep them healthy, do not
   put the first 90 days there.
