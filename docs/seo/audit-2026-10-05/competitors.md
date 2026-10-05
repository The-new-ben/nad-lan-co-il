# Competitors on our money words (HAD-435, 5.10.2026)

Evidence: 48 live Google SERPs pulled through DataForSEO (`/v3/serp/google/organic/live/advanced`, Israel, desktop,
depth 20, 5.10.2026 evening), DataForSEO Labs `competitors_domain` and `ranked_keywords` for nad-lan.co.il.
Raw: `data/dfs/serp-*.json`, `data/derived/serp-top10.csv`, `data/derived/serp-summary.json`,
`data/dfs/labs-competitors-nadlan.json`. Evidence class: **code** (API), not eyes. A desktop SERP from a data
centre is one sample; positions move by location, device and day.

## 1. The headline

**nad-lan.co.il does not appear in the desktop top 20 for any of the 48 money keywords checked**, including our
own strongest topics ("שדה דב", "duo תל אביב", "ריינבו תל אביב", "דמרי שדה דב", "הערכת שווי דירה",
"מגדלי כיכר המדינה"). GSC agrees: desktop average position 31.9, mobile 20.2; DataForSEO sees 692 ranked keywords,
4 in the top 10. Our clicks today come from names (professionals, project names) where competition is thin.

## 2. Who wins (top-10 appearances across the 48 SERPs)

| domain | top-10 slots | top-3 slots | page types that win |
|---|---:|---:|---|
| yad2.co.il (+ yadata, blog) | 39 + 4 + 1 | 18 + 2 | city and area listing search pages (`/realestate/forsale/{area}?city=`), the new-projects directory **Yad1** (`/yad1/newprojects/{area}?city=`), the valuation tool (yadata) |
| madlan.co.il | 34 | 16 | `/projects-for-sale/{city or neighbourhood}`, `/for-sale/{city}`, `/street-info/{street}`, `/propertyevaluation/`, `/projects/{project}` (DUO), `/commercial/offices-for-rent/{area}`, `/penthouses-for-sale/` |
| facebook.com / instagram.com / youtube.com | 27 / 7 / 7 | 7 / 3 / - | groups and developer videos on project-name queries (Rainbow, Dimri, Kikar) |
| calcalist / globes / bizportal / ynet / themarker | 9 / 7 / 8 / 4 / 3 | - | tag pages and news on Sde Dov, Kikar, DUO, market prices |
| gov.il, nadlan.gov.il, tel-aviv.gov.il, wikipedia | 7 / 4 / 2 / 3 | 2 / 2 / 2 / 2 | "נדלן", "עסקאות נדלן", "שדה דב", "מחיר למשתכן", "שמאי מקרקעין" |
| israelsir.co.il (Sotheby's) | 7 | 3 | luxury tag pages ("פנטהאוז למכירה", "דירות יוקרה בתל אביב", "דירות להשקעה בתל אביב") |
| sdedov.co.il | 4 | 1 | a single-topic Sde Dov information site, cited 3 times in Google's AI answers on Sde Dov |
| project-tlv.info | 2 | - | `/places/sde-dov/...` lot-by-lot project pages |
| law firms (realaw, hahn-law, barlaw, ma-law...) | 34 law-firm slots | | own "מס רכישה", "מס שבח", "נסח טאבו", "עורך דין מקרקעין", "פינוי בינוי" |
| developers (tidhar, dimri, aura, ashtrom, gindi) | 9 | 3 | own "פרויקטים חדשים", "דירות מקבלן", city project lists |
| nadlancenter, nadlan.com, nadlanmaster, onmap, hadashim, newkey, homeless, komo | 2-5 each | | category and city pages |

Labs `competitors_domain` (keyword overlap with us, Israel/Hebrew): facebook 603, youtube 519, **madlan 459** (avg
pos 10.0), instagram 429, **nadlancenter 412** (pos 21.6), **yad2 380** (pos 10.7), ynet 303, gov.il 243, zhg 237,
nadlanmaster 232, globes 231, nadlan.com 230, themarker 218, calcalist 216, magdilim 196, project-tlv.info 119.
Our average position on the shared set: 42.8.

SERP features on the 48 queries: **AI overview on 41 (85%)**, related searches 22, images 21, people-also-ask 11,
local pack 7 (lawyers, appraisers, offices, luxury), knowledge graph 7, video 6, ads on only 2 (DUO, Sde Dov project).

## 3. Money word by money word

| money word (Ads vol, CPC $) | who holds 1-3 | winning page type | what we have | gap |
|---|---|---|---|---|
| פרויקטים חדשים (390, 4.56) | tidhar, yad2 Yad1, dimri | developer catalogue, portal directory | /projects/ (pos 35-41) | our catalogue is not seen as a directory: no city facets as pages, thin snippet |
| פרויקטים חדשים בתל אביב (320, 10.18) | yad2 Yad1 x5, madlan neighbourhood | filtered directory pages | /projects/ ranks; the TLV page /new-projects/new-projects-tel-aviv/ does not | no strong TLV owner |
| פרויקטים חדשים ב{city} (Jerusalem 480, Rishon 210, Ramat Gan 170, Petah Tikva 260, Haifa 210...) | yad2 Yad1, madlan, onmap, hadashim, developers | one URL per city with a list of projects | nothing since the 25.8 purge (queries fall on /projects/ at 24-41) | **the largest generic gap** |
| דירות מקבלן / דירות חדשות מקבלן (210 / 170) | yad2 Yad1, madlan, dimri | directory | /projects/ (pos 37-43) | same |
| דירות למכירה (5,400, 2.29) + in TLV (880) / Jerusalem (1,300) | yad2, madlan, homeless, komo | listing search | /properties/ (7 demo listings) | **cannot win without real inventory**; not a content problem |
| נדלן (8,100, 7.55) | nadlan.gov.il, yad2, nadlancenter, madlan | portal home pages | home (pos 54-63) | brand-scale authority game; long term |
| הערכת שווי דירה (590, 1.26) / שמאות דירה (170, 11.36) | yadata, madlan, dirobot, appraiseit | data-driven calculators | /property-value-estimator/ (pos 19-21, our #1 click page) | a result based on real deal data by address; the AI answer cites 6 tools, not us |
| מחשבון משכנתא (40,500, 1.22) / משכנתא (9,900, 4.98) | banks, mortgage advisers, wobi | bank calculators | /mortgage-calculator/ (pos 50-56) | bank authority; low odds; keep as support tool |
| מס רכישה (6,600, 4.27) / מחשבון מס רכישה | law firms, midrag, small calculators (biz4biz, nuza) | calculator + legal guide | /purchase-tax-calculator/ (pos 57-59) | calculators that rank are simple single-purpose pages with 2026 brackets in the title |
| שדה דב (4,400, 4.92) | wikipedia, sdedov.co.il, tel-aviv.gov.il, calcalist | encyclopedic + a dedicated info site | /sde-dov/ (GSC 15-18, not in desktop top 20) | sdedov.co.il wins with a map, lots, news tags; we have more product (projects, 3D) but less "information hub" signal |
| שדה דב פרויקטים (390, 13.87) / פרויקט שדה דב (210, 15.49) / פרויקטים בשדה דב (70, 30.18) | madlan neighbourhood, rapac, olizki, newkey, project-tlv.info | lot-by-lot project lists | /sde-dov/, /sde-dov/merkaz/, /sde-dov-luxury-projects-2026/ split the intent | **we split our own strongest money intent across 4 URLs** (cannibalization.md) |
| דמרי שדה דב (210, 17.51) / dimri yama (70, 24.53) | dimri.co.il, FB, zirat-nadlan, sdedov | developer page + news | /projects/dimri-yama-sde-dov/ (GSC 8.5 for "dimri yama", 32 for Hebrew) | Hebrew title must carry "דמרי" (the searched spelling) |
| duo תל אביב (210) / duo (1,000, 9.34) | duo-tlv.com, ynet, globes, barnes, madlan project page | official + news + portal project page | /projects/duo-tel-aviv/ (GSC 17-25; our #2 click page) | prices and progress: PAA asks "address", "average price", "what is DUO" |
| ריינבו תל אביב (480, 5.34) | Israel Canada FB videos, yad2 blog, wxg | developer social + portal blog | /projects/rainbow-tel-aviv/ (GSC 13-17) | |
| מגדלי כיכר המדינה (260, 3.52) | FB groups, Instagram, globes 2015, ynet 2012, tlvonline | **no portal, no project page in the top 10** | /projects/hamedina/ (new, 6 impressions) | **open field**: the weakest top 10 of all 48. The AI answer cites ashtrom, wikipedia, globes, electra, tel-aviv.gov.il and states "two towers of 40 floors and one of 37": a fact-complete page can become the cited source |
| כיכר המדינה (5,400, 0.29) | easy.co.il, Instagram, Waze, yad2 neighbourhood projects, walla | place intent (shopping, the square) | - | low money; only the "towers" sub-intent matters |
| דירות יוקרה בתל אביב (140) / פנטהאוז למכירה | israelsir.co.il tag pages, yad2, madlan /penthouses-for-sale/, domestictlv | luxury listing tags | /property-value/luxury-apartments-tel-aviv/, /luxury-tel-aviv/, /tel-aviv-luxury-apartment-prices/, /luxury-apartments-israel-guide-he/ | four of our URLs split "luxury TLV"; no inventory |
| דירות להשקעה (480, 8.42) / השקעה בנדלן (170, 30.21) / השקעות נדלן (390, 22.79) | menivim, givat-alonim, yad2, okam, psagot, gindi, banks | guides + investment-product sites | /investment/ (pos 47-58), /investment/apartments-for-investment/ | highest CPC on the list; our root and child split the word |
| עורך דין מקרקעין (1,600, 12.98) / עורך דין נדלן (590, 13.82) | law firms + local pack + lawreviews directory | firm pages, directories | /real-estate-lawyer/ (pos 41), 2,847 professionals pages | a directory hub ("lawyers by city") is what pro.co.il / lawreviews do; matches our pros-network revenue |
| שמאי מקרקעין (2,400, 8.62) | landvalue.org.il, iritvan, wikipedia, gov, midrag, pro.co.il | association, firms, directories | /real-estate-appraiser/ | same directory play |
| בדק בית (3,600, 13.99) | (not pulled) | | /home-inspection/ (pos 60-68) | handover inspections are the Kikar 2027 wave (250 owners) |
| משרדים להשכרה (1,000, 15.24) / משרדים למכירה (390, 13.16) | yad2 commercial, madlan commercial, nmrk, top-land | listing search | /commercial-real-estate/office-for-rent/ and 20 office pages | no inventory; our commercial guides win only long-tail price questions |
| התחדשות עירונית (8,100) / פינוי בינוי (9,900) / תמא 38 (1,000) | ura.co.il (gov), law firms, developers, nadlancenter | guides + authority | /urban-renewal/ cluster, /urban-renewal/map/ (pos 11-16 for "מפת התחדשות עירונית") | the map is the asset; the head words are law-firm territory |
| מחיר למשתכן (90,500) / דירה בהנחה (74,000) | israhc.org, gov.il, news | government | none (check /affordable-apartments-israel-2026/) | huge volume, government-owned; only a lottery-results / project-list angle could earn |
| English "israel real estate" (US 720, 5.57), "tel aviv real estate" | realtor.com intl, immoisrael, israelpropertyhub, onmap/en, jpost, immobilier.co.il | portals for foreign buyers | /en/, /en/buy-property-in-israel/ (pos 55) | small, but foreign buyers are the Kikar/Sde Dov luxury audience |
| French "immobilier israel" | immobilier.co.il, immoisrael, jewishagency, immoneuf | French-language portals | /fr/, /acheter-appartement-israel-2026/ | |
| Russian "недвижимость в израиле" | vadimentor, kf.expert, geoln, ipotekaisrael, rbc, tranio | | /ru/ | |

## 4. What they have that we lack (ordered by money)

1. **One URL per city for new projects** (Yad1, Madlan projects-for-sale, Onmap, Hadashim, plus developer city lists).
   We removed ours on 25.8; demand did not go away, it now lands on /projects/ at positions 24-41.
2. **A real directory feel on the catalogue**: filters exposed as crawlable pages with their own titles and counts
   ("פרויקטים חדשים בתל אביב: 143 פרויקטים בשיווק"). Ours is one URL with `?city=` parameters canonicalised to /projects/.
3. **Inventory** for "דירות למכירה", "פנטהאוז למכירה", "משרדים להשכרה": competitors are listing engines. Content alone
   will not win these; the broker minisite / listings track (HAD-394, HAD-256) is the only way in.
4. **Data-backed valuation**: yadata and Madlan answer by address from deal data. Our estimator ranks 20 on brand-neutral
   value; adding address-level deal context would be the step change.
5. **Single-topic authority on Sde Dov**: sdedov.co.il has a map, lot pages and news tags and is cited by Google's AI
   answer three times. We have the stronger product (projects, 3D, prices) but not one clear hub that owns "projects in
   Sde Dov" (four of our URLs split it).
6. **Fresh news and progress signals** on project names (news tags, FB videos, "התקדמות בנייה"): related searches ask
   for prices, progress and address on DUO; we answer with static pages.
7. **Directory pages for pros by service and city** (pro.co.il, lawreviews, midrag): our 2,847 professional pages win
   names but no service-category page ranks for "עורך דין מקרקעין" or "שמאי מקרקעין".

## 5. What we have that they do not (the moat to lead with)

- 3D stages, view from every floor, the apartment basket and example apartments on the flagship project pages
  (Rainbow, DUO, Dimri Yama, Ashira, H Infinity, Einstein, Kikar Hamedina). No competitor page in these SERPs offers this.
- Five languages on the flagship projects; the English project pages already rank 4-8.
- Verified deal facts with claim discipline (the V7 rule) on Kikar Hamedina; the Kikar top 10 is social media and
  10-year-old news.
- The urban-renewal map (already 11-16 on its own query).
