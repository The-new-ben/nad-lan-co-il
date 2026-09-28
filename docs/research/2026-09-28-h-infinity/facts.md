# H Infinity (Hagag Group, Ibn Gabirol 128, Somail) - the fact ledger

Research date: 28.9.2026. Read-only web research (WebSearch, WebFetch, curl on public pages, Google Suggest,
OpenStreetMap Nominatim) plus local files already in the repo and the session scratchpad (Hagag's 2025 annual
report and Q2 2026 report, text-extracted). Nothing was written to the site. No secrets were touched.

Evidence classes used below:
- **OFFICIAL** = Hagag's filings to the Tel Aviv Stock Exchange (MAYA), the Tel Aviv municipality's GIS/permit layers,
  government bodies (NTA, Tax Authority, Bank of Israel).
- **DEV** = the developer's own websites and marketing pages (Hagag Group, infinity-hagag.co.il, hagaggroup.com).
- **PRESS** = news articles (Globes, Calcalist, Merkaz HaNadlan, Israel Hayom, Ynet, TheMarker).
- **DATA** = transaction data as displayed by Madlan (based on Tax Authority deal reports).
- **CALC** = our own arithmetic on published numbers. Must be labelled "חישוב שלנו" / "our calculation" in any article.
- **LISTING** = broker/portal listings (asking prices, never deal prices).

Rule for the article: every number carries its source and date in the text. Unknown = "לא פורסם" / "not published".
Tax and legal rates are marked **[לאישור הבעלים]** until the owner (a lawyer) confirms them.

---

## 1. Identity: what the project is called, where it is

| Item | Value | Source |
|---|---|---|
| Developer's H1 | "H - INFINITY TOWER - מתחם סומייל" | DEV, https://www.hagag-group.co.il/projects/ResidentProjects/h_infinity (read 28.9.2026) |
| Developer's title tag | "מגדל היוקרה H INFINITY - מתחם סומייל • קבוצת חג'ג'" | DEV, same |
| English developer page | "H-Infinity Tower" (H1), "H-Infinity Residence" in the text | DEV, https://www.hagag-group.co.il/en/projects/residential_projects/h-infinity |
| Marketing landing page | "INFINITY TOWER", H1 "THE SYMBOL OF TEL AVIV" | DEV, https://infinity-hagag.co.il/ and /infinity-tower/ |
| English marketing site | "Infinity Tower", H1 "Invest In Tel-Aviv's Next Iconic TOWER" | DEV, https://hagaggroup.com/infinity-tower/ |
| Name in the TASE filings | "סומייל 124" (project section); "אינפיניטי - סומייל" (sales table) | OFFICIAL, 2025 annual report and Q2 2026 report |
| Name in the press | "מגדל אינפיניטי" (Globes 12.8.2026, Merkaz HaNadlan 10.8.2026), "מגדל INFINITY" (Calcalist 1.9.2025), "Infinity Tower" (Globes English 14.4.2025) | PRESS |
| Name on portals | "H Infinity Tower תל אביב יפו" (Madlan), "INFINITY TOWER" (Yad2 project 5793), "אינפיניטי" (nadlan.com), "שלמה אבן גבירול 128" (NewKey) | DATA / portals |
| Purchase-group name (2014-2021) | קבוצת הרכישה "אינפיניטי" | PRESS, Globes 30.11.2021 |
| Street address | אבן גבירול 128, תל אביב (permit 20210989, request 20190089) | OFFICIAL, Tel Aviv GIS permit layer (via docs/research/2026-09-28-stages/stage-geometry.md section 4) |
| Other addresses in circulation | "Ibn Gabirol 126-132" (CTBUH Skyscraper Center); "אבן גבירול פינת ז'בוטינסקי" (Hagag site, press); "אבן גבירול-דובנובסקי" (infinity-hagag.co.il/infinity-tower/, verbatim, **an error**: Dubnov St. is not at the site); "Ben Gurion 128" (geoln.com, **error**) | various |
| Block / parcel / lot | גוש 6213 חלקה 1493, lot 124 of plan 2988ב, **3,167 m²** | OFFICIAL, 2025 annual report footnote 138; GIS layer 837 |
| Lot area, conflicting | "3,100 square meter lot" | PRESS, Globes English 14.4.2025 |
| Neighbourhood (portal naming) | "הצפון החדש סביבת כיכר המדינה" | DATA, Madlan |
| Compound | Somail compound (מתחם סומייל, also "סמל"), bounded by Ibn Gabirol (west), Arlozorov (south), Jabotinsky (north), Ben Saruk (east). Split into a south and a north compound; "הפרויקט מוקם בחלקו הצפוני". Each compound plans 2 residential towers of about 50 floors and 3 textural buildings of up to 8 floors. | OFFICIAL, 2025 annual report section 6.8.3.3.3; street order also OFFICIAL (GIS) |
| Lot centroid | 32.087284, 34.782720 | OFFICIAL (computed from GIS 837), stage-geometry.md 4.1 |

**Our live page's own errors to fix (not facts to publish):** the page meta `lat/lng` 32.086, 34.7821 is ~154 m off
lot 124; the address "אבן גבירול פינת ז'בוטינסקי" is the corner of lot 121 (Hagag's *other* lot, "Somail 121");
`num_floors 52`, `num_units 242` are out of date (see stage-geometry.md section 5).

### Name collisions (entities Google mixes with this project)
- "אינפיניטי" alone = Infinity investment house (pension/provident funds); autocomplete is dominated by it.
- "Infinity Park" Raanana (offices), "מגדל אינפיניטי רעננה" (El-Har), "INFINITY" office-tower brand (infinity8.co.il,
  including an "H Tower" page), all rank for "מגדל אינפיניטי".
- "מגדלי חג'ג'" / "Hagag Towers" = the HaArba'a office towers (Hagag's HQ, HaArba'a 30), not this project.
- English/Russian "H infinity" = a control-theory term (H∞ control). Arabic "برج انفينيتي" = Infinity Tower,
  New Administrative Capital, Egypt.
- Hagag's other Somail lot: **Somail 121** (parcel 1490, ~3,100 m², Ibn Gabirol/Jabotinsky corner), a future
  project, 80% Hagag via a partnership with Mor (20%). Current plan: two 8-floor residential buildings, ~38 homes,
  ~3,178 m² retail. OFFICIAL, 2025 annual report. Not H Infinity.

---

## 2. The buildings: floors, homes, height (conflicts side by side)

| Item | Value | Source |
|---|---|---|
| **Permit (OFFICIAL)** | Building permit 22.12.2021 + change permit 9.12.2024: "מגדל מגורים בן 53 קומות לצד מבנה מרקמי בן 6 קומות מגורים מעל קומת מסחר, ובהם סך כולל של כ-278 יחידות דיור וכ-267 מ"ר ברוטו שטח מסחרי" | OFFICIAL, Hagag 2025 annual report s.6.8.3.3.3, https://www.hagag-group.co.il/Uploads/2026/04/rln33jws7WiMM6.pdf |
| Planning table | 278 homes, 29,425 m² residential, 267 m² retail | OFFICIAL, same |
| 2021 permit as first issued | 49 residential floors + a commercial floor, 273 homes, 346 parking spaces, gym on the ground floor | OFFICIAL, GIS permit layer 772 (stage-geometry.md 4.3) |
| Developer site (Hebrew) | "מגדל יוקרה בן 52 קומות ובניין בוטיק בן 7 קומות" | DEV, hagag-group.co.il and infinity-hagag.co.il (read 28.9.2026) |
| Developer site (English) | "a 51-story tower and a 6-story boutique residential complex" | DEV, hagag-group.co.il/en |
| English marketing site | "a 51-story tower and a 7-story boutique building. With 273 apartments" | DEV, hagaggroup.com/infinity-tower (2025) |
| Marketing landing /infinity-tower/ | "מתנשא לגובה של 51 קומות" | DEV |
| Press 2021 | "מגדל בן 47 קומות ובניין נוסף בן 6 קומות ובסך הכול 237 יחידות דיור" (the original purchase-group plan); dispute over enlarging to 273 | PRESS, Globes 30.11.2021, https://www.globes.co.il/news/article.aspx?did=1001392692 |
| Press 2025 | "53 floors with 287 apartments on a 3,100 square meter lot" | PRESS, Globes English 14.4.2025 |
| Press 2026 | "מגדל מרכזי בן 52 קומות ובו 287 יחידות דיור" | PRESS, Merkaz HaNadlan 10.8.2026, https://www.nadlancenter.co.il/article/15151 |
| Press 2026 | "מגדל מגורים בן 52 קומות לצד בניין נוסף בן שבע קומות, ובסך-הכול 278 יחידות דיור" | PRESS, Globes 12.8.2026 (did=1001552079) |
| Early plan | "50 floors, ~200 apartments" (2012-2014 headlines); "47 floors, 200 units" (TheMarker 2014) | PRESS, project-tlv.info timeline; themarker.com/realestate/1.2500807 |
| Portals | Madlan "2 בניינים, 6-49 קומות, 273 דירות"; geoln "48 floors, 242 apartments, completion October 2020" (stale); nadlanmaster "48 floors" (stale) | DATA / portals |
| **How to explain the gap** | "53" counts the tower's floors in the amended 2024 permit; "52 + 7" and "51 + 6" are marketing counts of the tower and the low building with or without the retail floor; 237 → 273 → 278 homes follow the 2014 plan, the 2021 permit and the 2024 change permit. **287** appears only in press (2025-2026) and conflicts with the filing's 278. | our reading; cite each number with its source |
| **Height** | **No official height published.** CTBUH Skyscraper Center lists 180 m / 591 ft, 51 floors, status "Architecturally Topped Out", completion 2026, construction start 2017, location "126-132 Iben Gavirol Street". SkyscraperCity forum thread titles moved from "168m, 50fl+6fl, U/C" to "197 m, 52fl + 6fl, T/O". | https://www.skyscrapercenter.com/building/h-infinity-tower-i/17932 (database, not official); skyscrapercity.com threads (forum, unofficial) |
| Tower footprint | ~623 m² (25 × 25 m) and low building ~313 m² on Ibn Gabirol (west side) | OFFICIAL polygons, roles INFERRED (stage-geometry.md 4.3) |

---

## 3. Developer, architect, contractor, finance

| Item | Value | Source |
|---|---|---|
| Developer | קבוצת חג'ג' ייזום נדל"ן בע"מ (TASE: HGG), through the fully owned subsidiary קבוצת חג'ג' סומייל בע"מ | OFFICIAL, 2025 annual report |
| Founders | the brothers Tzahi (Yitzhak) and Ido Hagag; co-CEOs since 29.8.2024 | OFFICIAL, 2025 annual report; DEV |
| Developer's track record (as stated by the developer) | "אחראית על למעלה מ-45 פרויקטים יוקרתיים ופורצי דרך, ביניהם מגדלי הארבעה, מגדל מאייר ברוטשילד, FIRST בשדה דב" (Hebrew site); "Over 100 Successful Projects" (hagaggroup.com) | DEV (two different counts) |
| Meier on Rothschild | Hagag launched it in 2014, architect Richard Meier | PRESS, Calcalist 1.9.2025 |
| Early partner | "Hagag, Wardinon to build 50-story Tel Aviv tower" (2014); project-tlv lists "קבוצת חג'ג' וורדינון" | PRESS, https://en.globes.co.il/en/article-1000805704 ; project-tlv.info |
| Holding today | 100% via Hagag Somail, subject to the option holders' right to 24% of pre-tax profit ("הסכם סיחור"; one option holder has business ties with Mr. Yitzhak Hagag) | OFFICIAL, 2025 annual report |
| Architect | Prof. Moshe Tzur (משה צור אדריכלים ובוני ערים בע"מ) | DEV; Madlan; CTBUH |
| Main contractor | אלקטרה בנייה (Electra Construction), contract 2020 (press 12.11.2020) | OFFICIAL (annual report, contractor agreement s.6.8.3.1.7 of the 2023 report); PRESS Globes 12.8.2026; project-tlv timeline |
| Contractor note | "למעט בפרויקט סומייל, שם הקבלן הראשי אינו אחראי לטיב עבודות קבלני המשנה" | OFFICIAL, 2025 annual report (general contractors section) |
| Suppliers named on their own sites | Klein's (kitchens), DEBI Aluminum (facade aluminium) | kleins.co.il/en/project/h-infinity-tower-tel-aviv/ ; debi-al.co.il/en/h-infinity-tower-tel-aviv/ (supplier portfolio pages, not verified spec) |
| Accompanying bank | In 2020-2021 the purchase group's accompanying bank was **Bank Mizrahi** ("הבנק המלווה של הפרויקט, בנק מזרחי") | PRESS, Globes 30.11.2021. The 2025 report speaks of "הגופים המממנים / הבנק המלווה" without naming it in the part read. **Current bank: not confirmed.** |
| Financing addendum 18.5.2026 | the deadline to deposit the "new plan" (see section 7) was extended from 1.5.2026 to **31.10.2026** | OFFICIAL, Q2 2026 report s.1.5.2.3, https://www.hagag-group.co.il/Uploads/2026/09/OGy0Rl8MjoKHAq.pdf |
| Land purchase | 2015, about ₪187.5M, by exercising options | OFFICIAL, 2025 annual report |
| Betterment levy | disputed: first assessment ~₪78M, second ~₪14.3M; a decisive appraiser set ~₪46.5M on the first; appeals pending by both sides | OFFICIAL, 2025 annual report (company-side matter, not a buyer cost; mention only if relevant) |
| Litigation | the report mentions a claim by a purchase-group member about his rights (note 19ג(9)) | OFFICIAL, 2025 annual report (neutral mention at most) |

---

## 4. History timeline

| Date | Event | Source |
|---|---|---|
| until 1948 | Sumail (סומייל, Arabic السُّمَيل, also named al-Mas'udiyya / אל-מסעודייה), an Arab village founded in the 2nd half of the 19th century on a kurkar ridge; population 104 (1870), 449 (1922), 651 (1931), ~850 (1945). Residents left on 25.12.1947; Jewish residents then lived in the houses as an informal neighbourhood without municipal infrastructure or property rights. | he.wikipedia.org/wiki/סומייל (read 28.9.2026) |
| 2006 | the compound's plans approved (residential + commercial); proposal to rename it "סמל" | he.wikipedia (as above) |
| 12.2012-1.2013 | Hagag exercised an option on the lot; "50 קומות" headlines | PRESS, project-tlv.info timeline |
| Q3 2014 | marketing starts (purchase-group model) | OFFICIAL, 2025 annual report ("מועד התחלת שיווק") |
| 1.12.2014 | "קבוצת חג'ג': 90 דירות החל מ-2.2 מ' ש' נמכרו במגדל שיוקם במרכז ת"א" | PRESS, TheMarker 1.12.2014 |
| 2015 | lot bought (~₪187.5M) | OFFICIAL |
| Q4 2016 | "מועד התחלת עבודות הקמה" | OFFICIAL, 2025 annual report |
| 12.11.2020 | Electra Construction to build H INFINITY | PRESS, project-tlv timeline |
| 22.12.2021 | building permit | OFFICIAL |
| 25.11.2021 / 30.11.2021 | the group assembly approved turning the project into a developer project led by Hagag; members get Sale Law guarantees, a uniform spec and a final delivery date | OFFICIAL (report), PRESS (Globes 30.11.2021) |
| from 11.2021 | sales to non-members in the developer model | OFFICIAL, Q2 2026 report |
| 9.12.2024 | change permit (53 floors, ~278 homes) | OFFICIAL |
| 1.9.2025 | campaign: ~20 apartments, "15% במעמד חוזה", 2.5 rooms from ₪4.5M, 4 rooms ~120 m² + 14 m² balcony from ₪8.1M; "בעוד כשנתיים צפויה... לאכלס" | PRESS (sponsored, "בשיתוף Channel22"), Calcalist https://www.calcalist.co.il/article/b1p8qwzcee |
| 10.8.2026 / 12.8.2026 | new campaign: ₪1M at signing, guaranteed rent for 2 years (details in section 6) | PRESS, Merkaz HaNadlan 10.8.2026; Globes 12.8.2026 |
| Q4 2026 | planned end of construction works (company estimate) | OFFICIAL, 2025 annual report |
| Q2 2027 | planned end of marketing | OFFICIAL, 2025 annual report |
| Q4 2026 - H1 2027 | expected release of surplus to the company, "בכפוף למכירת כלל היחידות שנותרו לשיווק" | OFFICIAL, 2025 annual report |

---

## 5. Status and occupancy (as of 28.9.2026)

| Item | Value | Source |
|---|---|---|
| Construction | "בניית הפרויקט נמצאת בעיצומה" | OFFICIAL, 2025 annual report |
| Permit layer stage | permit 20210989 "בניה חדשה מגדל מגורים מעל 20 קומות", stage "בבניה", works-start field 11.11.2025 | OFFICIAL, GIS (stage-geometry.md 4.3) |
| Financial completion (excl. land) | **74%** (31.12.2025) → **83%** (31.3.2026) → **86.3%** (30.6.2026) | OFFICIAL, Q2 2026 report, "שיעור השלמה כספי (לא כולל קרקע)" (our reading of the extracted table; the column order was checked against the cost rows) |
| Costs | cumulative ₪622.4M, ₪108.6M left to complete (30.6.2026) | OFFICIAL, Q2 2026 report |
| End of construction | "רבעון 4 2026" (planned) | OFFICIAL, 2025 annual report |
| Occupancy in the press | "שצפוי להתאכלס במהלך השנה הקרובה" (12.8.2026); "ייכנסו לדירה בתוך כשנה" (10.8.2026); "Estimated occupancy is within approximately two years" (Barnes listing, undated); "December 2027" (selecsion.com listing) | PRESS; LISTING |
| Delivery under the 2021 group deal | Form 4 within 48 months of the "determining date", delivery within 52 months, +3 months allowed; the determining date itself is not published in the part read | OFFICIAL, 2025 annual report |
| Topped out? | CTBUH: "Architecturally Topped Out"; forum: "T/O" | database/forum only, not official |
| **Honest summary** | The company plans to finish construction in Q4 2026; the press (8.2026) speaks of occupancy within about a year. **A contractual delivery date for a given apartment is not published**; it is in each buyer's contract. | |

---

## 6. Prices, sales and the 2026 offer

### 6.1 Published "from" prices (marketing, not deals)
| Claim | Source and date |
|---|---|
| "החל מ-65,000 ₪ למ"ר בלבד. 15% בלבד במעמד החתימה והיתרה באכלוס. ללא הצמדה למדד" | DEV, hagag-group.co.il H INFINITY page (read 28.9.2026) |
| "החל מ-₪65,000 למ״ר בלבד", "10% בלבד במעמד החתימה והיתרה באכלוס", "ללא הצמדה למדד", "הטבה ייחודית ל-20 דירות בלבד" | DEV, infinity-hagag.co.il (read 28.9.2026). **Conflict: 10% vs 15% at signing.** |
| "דירות יוקרה 2-6 חד׳ עם מרפסות נוף החל מ-5.82 מיליון ₪", "הטבה מיוחדת ל-20 דירות בלבד" | DEV, infinity-hagag.co.il/infinity-tower/ |
| "1-3 bedroom apartments, starting from 70 sqm + 7 sqm balcony, from 5,868,000 NIS"; "3-4 bedroom apartments, starting from 129 sqm + 29 sqm balcony, from 10,215,000 NIS"; "5-6 bedroom penthouse, 287 sqm + 60 sqm balcony, from 31,620,000 NIS"; "Est. construction duration: 4 years" (undated) | DEV, hagag-group.co.il/en |
| "2 Bedrooms: Starting at ~$1,700,000; 3 Bedrooms ~$2,000,000; 4 Bedrooms ~$2,600,000", at the Feb 2025 USD/ILS rate | DEV, hagaggroup.com/infinity-tower |
| 1.9.2025: 2.5 rooms from ₪4.5M; 4 rooms ~120 m² + 14 m² balcony from ₪8.1M; "העסקאות האחרונות... כ-85,000 ש"ח למ"ר" | PRESS (sponsored), Calcalist 1.9.2025 |
| 12.8.2026: ~30 apartments of 2-5 rooms "במחיר התחלתי של 60 אלף שקל למ"ר", "הנחה של 10%-15%, תלוי בגודל הדירה" (estimate) | PRESS, Globes 12.8.2026 |
| Listings: "starting at 4,950,000 ILS" (selecsion, Vantage); "4,900,000 NIS" (Home in Israel); 4 rooms 94 m² + 14 m² terrace, floor 8, ₪4.5M (Evenis, "new project"); penthouse 5 rooms 310 m² + 54 m² terraces ₪27.6M, sea view (Barnes) | LISTING, asking prices only |
| Undated snippet: "2-5 חדרים החל מ-4,100,000 ₪... ₪1,000,000 בחתימה... היתרה שנתיים לאחר האכלוס" | a portal/broker snippet in the SERP; **not verified, do not use** |

### 6.2 The August 2026 offer (verbatim facts)
- Merkaz HaNadlan 10.8.2026 (דרור ניר קסטל): "רוכשי יותר מ-30 דירות במגדל אינפיניטי בתל אביב ישלמו מיליון שקל
  במעמד החתימה, ייכנסו לדירה בתוך כשנה, ואת יתרת התמורה ישלימו רק בעוד כשלוש שנים - ללא ריבית, הצמדה או צורך
  במשכנתה בתקופת הביניים".
- Same: "מתחייבת קבוצת חג'ג' לדאוג לכך שהנכס יושכר בשנתיים הראשונות לאכלוס בתשואה דו ספרתית על הסכום הראשוני
  ששולם (24%-52%)". Example 1: "דירת 2 חדרים בגודל 70 מ"ר יובטח שכר דירה של 10,000 ש"ח לחודש לפחות למשך השנתיים
  הראשונות, בסך כולל של 240,000 ש"ח". Example 2: "דירת 5 חדרים יובטח שכר דירה של 22,000 ש"ח בחודש... 528,000 ש"ח".
- Globes 12.8.2026: "את היתרה לשלם בעוד שלוש שנים **מרגע האכלוס** ללא ריבית והצמדה".
  **Conflict:** "בעוד כשלוש שנים" (Merkaz HaNadlan, reads as from signing) vs "שלוש שנים מרגע האכלוס" (Globes).
  The binding version is the sale contract.
- **CALC (must be labelled):** the "24%-52%" is rent over two years divided by the ₪1M paid, **not** a yield on the
  apartment's price. ₪10,000 × 12 = ₪120,000 a year. Against the lowest 2025 deal for a 70 m² two-room
  (₪5,843,010, 27.11.2025, section 6.3) that is **about 2.1% gross a year**. ₪22,000 × 12 = ₪264,000 a year; against
  2025 five-room deals of ₪10.9M-₪17.4M that is **about 1.5%-2.4% gross**. Madlan's Tel Aviv gross yield figure on
  the page: 2.46% (area), 2.55% (city). The deferred balance without interest or indexation is a real financial
  benefit whose value depends on interest rates.
- **Open questions for the buyer (not facts):** when is purchase tax paid on the full price in this model; what
  guarantees cover the ₪1M; who is the tenant-finder and what happens if the rent is not reached; what exactly
  "entry within a year" means in the contract. **[לאישור הבעלים]** for the tax-timing rule.

### 6.3 Recorded deals (Tax Authority data as shown by Madlan)
Source: https://www.madlan.co.il/projects/H-Infinit ("היסטוריית עסקאות", tab "בפרויקט (152)"), read 28.9.2026.
The page shows 152 deals in the project; the page data we could read holds 84 unique rows (2013-2026). Sizes and
prices are as reported by Madlan; rooms as reported. Floors are **not** in the data except as a unit code; only
two floors are confirmed by the press (Globes English 14.4.2025).

Summary by year (price per m² as reported):
| Year | Deals | Median ₪/m² | Range ₪/m² | Note |
|---|---|---|---|---|
| 2013 | 23 | 35,321 | 17,629-79,463 | purchase-group era: members' rights, not comparable to today |
| 2014-2017 | 15 | ~36,600 | 13,291-43,543 | same |
| 2021 | 13 | 65,309 | 34,817-72,832 | start of the developer model (11.2021) |
| 2022 | 7 | 59,456 | 55,264-70,107 | |
| 2023 | 1 | 75,086 | | |
| 2024 | 13 | 74,006 | 56,898-89,245 | |
| 2025 | 11 | 89,662 | 72,111-94,915 | |
| 2026 (to 28.9) | 1 | 95,714 | | |
| **2025-2026** | **12** | **~91,000** | **72,111-95,714** | CALC median |

Rows 2024-2026 (as shown; floor only where the press published it):
| Date | Rooms | m² | Price ₪ | ₪/m² | Floor |
|---|---|---|---|---|---|
| 31.1.2024 | 5 | 169 | 14,150,250 | 83,729 | not published |
| 30.6.2024 | 4 | 94 | 7,500,000 | 79,787 | not published |
| 30.6.2024 | 4 | 216 | 15,860,000 | 73,426 | not published |
| 31.7.2024 | 5 | 149 | 12,307,600 | 82,601 | not published |
| 1.8.2024 | 4 | 95 | 6,857,115 | 72,180 | not published |
| 15.9.2024 | 3 | 86 | 6,063,200 | 70,502 | not published |
| 15.9.2024 | 2 | 71 | 4,592,900 | 64,689 | not published |
| 30.10.2024 | 4 | 124 | 11,066,400 | 89,245 | not published |
| 5.11.2024 | 2 | 84 | 4,779,445 | 56,898 | not published |
| 19.11.2024 | 4 | 85 | 6,576,750 | 77,374 | not published |
| 11.12.2024 | 2 | 69 | 5,477,995 | 79,391 | not published |
| 20.12.2024 | 4 | 125 | 8,910,906 | 71,287 | not published |
| 24.12.2024 | 4 | 94 | 6,956,580 | 74,006 | not published |
| 23.1.2025 | 5 | 180 | 16,641,026 | 92,450 | **43** (Globes EN: "NIS 16.5 million, 43rd floor, 180 m² plus 22 m² balcony") |
| 23.1.2025 | 5 | 150 | 11,094,017 | 73,960 | **9** (Globes EN: "NIS 11 million, 9th floor, 150 m² plus 29 m² balcony") |
| 13.2.2025 | 5 | 151 | 10,888,800 | 72,111 | not published |
| 11.3.2025 | 5 | 169 | 16,040,650 | 94,915 | not published |
| 11.3.2025 | 3 | 119 | 10,669,750 | 89,662 | not published |
| 11.3.2025 | 3 | 167 | 15,840,900 | 94,856 | not published |
| 11.3.2025 | 3 | 119 | 10,592,400 | 89,012 | not published |
| 3.4.2025 | 6 | 182 | 17,226,840 | 94,653 | not published |
| 27.11.2025 | 2 | 70 | 5,843,010 | 83,472 | not published |
| 27.11.2025 | 5 | 312 | 29,373,960 | 94,147 | not published |
| 31.12.2025 | 1 (as reported) | 119 | 9,341,250 | 78,498 | not published |
| 19.2.2026 | 5 | 182 | 17,419,950 | 95,714 | not published |

Cross-checks: the two Globes English deals (14.4.2025, "French investors buy 2 Tel Aviv apartments for NIS 27.5m",
bought by "a real estate holding company owned by French investors") match the two 23.1.2025 rows. The 19.2.2026 row
(₪17.42M) matches the Q2 2026 report's single H1 2026 contract (₪17,420K incl. VAT). Rows with odd room counts
(e.g. "1 room, 119 m²") are shown as reported; do not interpret them.

### 6.4 Sales figures from the company's reports (OFFICIAL)
| Item | Value | Source |
|---|---|---|
| Developer-model contracts (to non-members, since 11.2021) | 2025: 14 contracts, 2,406 m², ₪67,337/m²; Q1 2026: 1 contract, 194 m², ₪76,271/m²; Q2 2026: none. Cumulative 30.6.2026: **50 contracts, 6,926 m², average ₪58,933/m²** | Q2 2026 report, section on Somail 124. The report warns: "מחירי המכירה הממוצעים החוזיים... לא מביאים לידי ביטוי רכיבים דוגמת פריסות תשלומים פטור מהצמדה למדד ועוד" |
| H1 2026 marketing table (incl. VAT) | to 30.6.2026: 1 unit, ₪17,420K; from 1.1.2026 to the report's publication incl. join requests and options: **12 units, ₪91,702K, average ₪7.6M** | Q2 2026 report, table ב' |
| Press on the same | "לא נמכרה אף דירה ברבעון השני... לאחר שברבעון הראשון נמכרה דירה אחת בלבד"; "278 יחידות דיור שרובן נמכרו, וכיום נותרו עוד **60 דירות** לשיווק"; "לאחר תום תקופת הדוח נחתמו 11 הסכמים נוספים" | PRESS, Globes 1.9.2026 (did=1001553998) |
| Company claim 8.2026 | "שווקו עד כה מעל 200 דירות" | PRESS, Globes 12.8.2026 |
| Earlier averages | "Since the company began marketing Infinity Tower in 2021, the average per square meter in apartments sold was NIS 53,600 while in 2024 the average was NIS 58,390"; "In the first quarter of 2024, the average was NIS 64,100" (as quoted by our fetch; it conflicts with the 2024 average in the same article and is probably Q1 2025: do not use without reading the article) | PRESS, Globes English 14.4.2025, https://en.globes.co.il/en/article-french-investors-buy-2-tel-aviv-apartments-for-nis-275m-1001507757 |
| Calcalist headline | "קבוצת חג'ג' מכרה מאות דירות במגדל INFINITY" | PRESS (sponsored), 1.9.2025 |
| Early sales | 2014: 90 apartments from ₪2.2M (3 rooms); "Nearly half of the 200 apartments... presale, 3 rooms from 2.2 million, 4 rooms from 3 million" | PRESS, TheMarker 1.12.2014; Globes 2013-2014 |

**Why deal ₪/m² (~₪72K-96K in 2025-26) is far above the "from ₪60K-65K/m²" marketing:** marketing states the
cheapest unit (low floor, small), the company's averages are contractual and may exclude VAT and payment-terms
effects (as the report says), and Madlan's figures are the reported consideration per reported area. Present all
three, with sources, and do not merge them.

### 6.5 Area benchmarks
| Item | Value | Source |
|---|---|---|
| Madlan page, neighbourhood | average ₪/m² "62 א' ₪", yield 2.46% | DATA, Madlan project page (28.9.2026) |
| Madlan, Tel Aviv city | ppa ~₪65,972/m² (all), new-build ppa ~₪72,039/m², yield 2.55% | DATA, Madlan page JSON |
| DUO (neighbour, south Somail) | 1-6.2026: 12 units, average ₪10,985K per unit incl. VAT, ~₪71K/m² before VAT (~₪83.8K incl. VAT, CALC); ICE 22.4.2026: "המחירים נעים בין 80-85 אלף שקל למ"ר" | OFFICIAL Africa Israel Residences Q2 2026 (via docs/research/2026-09-28-duo/duo-deals.md); PRESS ICE |
| Our own page's price box | Tel Aviv average ₪52,856/m² (2,432 deals), Ibn Gabirol ₪72,179/m² (9 deals) | the live page (source of that widget: our site's deals data; state its date if used) |

---

## 7. Buyer-protection facts specific to this project

- **Occupancy condition (OFFICIAL, footnote 137):** in its permit request, Hagag Somail undertook to prepare a plan
  adding **450 m² gross public space** on its Bavli 3 land; "תנאי לאכלוס פרויקט סומייל 124 הינו הפקדה בפועל של
  התוכנית החדשה עד למועד האכלוס". If not approved, the company undertook to find another planning solution.
  The financing addendum of 18.5.2026 extended the deposit deadline to **31.10.2026** (Q2 2026 report).
- **Purchase-group to developer switch (OFFICIAL + PRESS):** approved 25.11.2021; group members got Sale Law
  (הבטחת השקעות) guarantees against every payment, a uniform spec and a final delivery date; late delivery beyond
  18 months lets a member cancel (report). Ministry of Construction quote (Globes 30.11.2021): "בעולם קבוצות הרכישה
  אין חוק שמגן על החברים. בעולם היזמות הכספים מוגנים".
- **Payment terms differ by source** (15% vs 10% at signing vs ₪1M) → the contract governs.
- **"ללא הצמדה למדד"** is a developer claim (DEV). Check it in the contract.
- **Sale Law guarantee** = the standard protection on every payment to a developer (חוק המכר (דירות) (הבטחת השקעות של
  רוכשי דירות), תשל"ה-1974). Owner to confirm wording. **[לאישור הבעלים]**

---

## 8. Facilities and specification (DEV only, nothing verified in a spec)

| Facility | Hebrew developer site | English/other | Conflict |
|---|---|---|---|
| Pool | "בריכת אינפיניטי מרשימה המשקיפה אל קו החוף" (floor not stated) | hagaggroup.com: "Rooftop Half-Size Olympic Pool (25 meters)"; Calcalist 9.2025: rooftop INFINITY pool; selecsion: "Semi-Olympic pool", "Rooftop with panoramic views" | infinity pool vs half-Olympic 25 m: **both "on the roof" per two sources; size and type differ.** |
| Lobby | "לובי כניסה המתנשא לגובה של כ-10 מטרים" | "grand lobby" | |
| Residents' room | "חדר דיירים מפואר" | "residents' club" (EN) | |
| Park | "פארק לרווחת התושבים" | | place not stated |
| Fitness | "מתקני כושר מתקדמים"; 2021 permit: gym on the ground floor (OFFICIAL) | "State-Of-The-Art Fitness Center" | |
| Spa | not on the Hebrew site | "spa" (EN developer page); Calcalist 9.2025: spa, co-working | |
| Parking | 346 spaces (2021 permit, OFFICIAL) | "secure underground parking", "Private Parking With Electric Charging Stations" | number of basements not stated |
| Security | | "24/7 Security" (hagaggroup.com); "24/7 concierge service" (listing) | |
| Facade | "קירות מסך בשילוב חלונות מרצפה עד תקרה והצללות חשמליות", "חיפוי אלוקובונד" | | |
| Retail | ~267 m² gross (OFFICIAL); "Commercial On The Ground Floor" | | |
| Apartment mix | "2-6 חד׳ עם מרפסות נוף" (DEV); "2.5 - 5.5 rooms" (selecsion); "from 2 bedroom to 4 bedroom + penthouses" (hagaggroup.com) | | |
| Listings' claims | 4 elevators incl. a Shabbat elevator, storage, bicycle room (selecsion); 4-metre ceilings, VRF A/C, smart-home readiness, sauna (Barnes, penthouse) | LISTING, unverified |
| **Not published** | official height, floor-to-floor height, management fees, number of elevators (official), spec sheet, floor plans (behind a buyers' password on the developer site), pool dimensions (official), balcony directions per unit, number of basements |

---

## 9. Location: distances (CALC, straight line from the lot centroid; walking distance is longer)

Lot centroid 32.087284, 34.782720 (OFFICIAL GIS). POI coordinates from OpenStreetMap Nominatim (28.9.2026).
| Place | Straight line |
|---|---|
| Herzliya Hebrew Gymnasium (Jabotinsky 106) | ~245 m |
| Gan Ha'ir (Ibn Gabirol 71) | ~620 m |
| Tel Aviv City Hall (Ibn Gabirol 69) | ~640 m |
| Kikar HaMedina | ~670 m |
| Rabin Square | ~730 m |
| Tel Aviv Sourasky (Ichilov) Medical Center | ~1 km (our estimate from the hospital's known position; not geocoded) |
| Tel Aviv Museum of Art | ~1.1 km |
| Hilton Beach (nearest beach) | ~1.27 km |
| Dizengoff Square | ~1.3 km |
| Tel Aviv Port | ~1.4 km |
| Gordon Beach | ~1.5 km |
| Tel Aviv Savidor Center railway station | ~1.5 km |
| Dizengoff Center | ~1.5 km |
| Habima / Charles Bronfman Auditorium | ~1.6 km |
| Azrieli Center | ~1.65 km |
| Sarona Market | ~1.85 km |
| Tel Aviv University | ~3.5 km |
| Ben Gurion Airport | ~13.2 km |
Developer phrasing for comparison: "5 minute walk from Kikar Hamedina" (EN site), "15 Minute Walk To The Beach"
(hagaggroup.com). Views ("נוף אינסופי של קו החוף") are a developer claim; per-apartment views are not published.

### Transport (OFFICIAL / PRESS)
- **Green Line** light rail: tunnel of ~4.5 km under Ibn Gabirol, Carlebach and Begin with four underground stations;
  permits approved for the underground stations "קפלן, רבין, ארלוזורוב וקרליבך" (Israel Hayom 27.4.2026). Opening:
  partial (Rishon LeZion-Holon-Levinsky) end of 2028; the rest, from south Tel Aviv to Herzliya, **2030**
  (Calcalist 18.2.2025; Ynet 18.2.2025; Israel Hayom 27.4.2026). The developer says "גישה נוחה... כולל הקו הירוק של
  הרכבת הקלה" (DEV) - true in the future tense only.
- **Purple Line**: runs along Arlozorov (NTA works page "ארלוזורוב מאבן גבירול עד בן יהודה"); commercial opening
  planned **July 2028** (Calcalist 18.2.2025). Exact station positions: check the NTA map before citing.
- **Red Line**: operating; nearest link is via Savidor/Arlozorov (do not claim a station at the site).
- Israel Railways: Tel Aviv Savidor Center ~1.5 km (CALC).
- The claim "two light-rail stations inside the compound" (older internal dossier) is **not confirmed** by an official
  source in this research. Use: the Green Line's Arlozorov station is planned under Ibn Gabirol at Arlozorov, at the
  south edge of Somail, and the Purple Line runs along Arlozorov.

### Neighbours in the compound (OFFICIAL unless stated)
- **DUO Tel Aviv** (Africa Israel Residences), south Somail: two towers of 54 floors (50 residential), **668 homes**
  in the permit; completion expected 2027 (company). Our page: /projects/duo-tel-aviv/.
- **Lot 122** (Africa Israel, north tower east of H Infinity): permit 14.4.2024, 50 residential floors, 226 homes,
  a 1,500 m² public building; a 4/2026 request adds a roof pool at floor 50. **Lot 123**: an 8-floor textural building,
  31 homes. (GIS, stage-geometry.md 4.2)
- **Somail 121** (Hagag, north corner Ibn Gabirol/Jabotinsky): future, see section 1.
- **New municipal tower** south of the lot on plan 4067: 25 floors in the GIS buildings layer (footprint 1,928 m²);
  Time Out: "מגדל ציבורי חדש: כך ייראה בניין העירייה שנבנה על קרקעות סומייל" (municipal offices, kindergartens,
  public garden). Magdilim: "a new 24-story structure at the corner of Ibn Gabirol-Arlozorov".
- Compound scale in the press: "4 מגדלים בני 50 קומות ובניינים מרקמיים"; "~1,200 apartments in 50-story towers"
  (magdilim.co.il). Magdilim also: prices rose "מכ-55,000 שקל למ"ר לכ-70,000 שקל למ"ר" in one year (undated older
  article; use only with its date if found).

---

## 10. Taxes, mortgages, buying from abroad (general law; **[לאישור הבעלים]** on every rate)

| Item | Value | Source |
|---|---|---|
| Purchase tax 2026, single apartment (Israeli resident) | 0% to ₪1,978,745; 3.5% to ₪2,347,040; 5% to ₪6,055,070; 8% to ~₪20M; 10% above | PRESS, Bizportal 6.7.2026 (https://www.bizportal.co.il/realestates/news/article/20035184); brackets reported frozen until 1.2028 |
| Additional apartment / investor | 8% from the first shekel to ₪6,055,070; 10% above | same |
| Foreign resident (תושב חוץ) | no single-apartment brackets: 8% from the first shekel to ₪6,055,070, 10% above | same; immobilier.co.il FR 26.7.2026 |
| Olim (new immigrants) | reduced rates for one apartment, from one year before to seven years after aliyah. **Sources conflict:** "0.5% עד 1,988,090 ₪ ו-5% מעבר לכך" (an Israeli guide) vs "0% jusqu'à 1 978 745 NIS, puis 0,5 % jusqu'à 6 055 070 NIS" (immobilier.co.il, 26.7.2026, after a February 2026 reform) | must be checked on the Tax Authority simulator https://www.misim.gov.il/svsimurechisha/startPage.aspx |
| Mortgage LTV, non-residents | maximum 50% | Bank of Israel, Proper Conduct of Banking Business Directive 329 (https://boi.org.il/media/uckpqztg/329_et.pdf); broker/guide sites agree |
| Mortgage LTV, resident first home | up to 75% | Bank of Israel (as above) |
| Mortgage LTV, resident replacing a home (משפרי דיור) | up to 70% | Bank of Israel Directive 329 (general rule, **[לאישור הבעלים]**) |
| Mortgage LTV, investor / additional apartment | up to 50% | same |
| Remote purchase | power of attorney to an Israeli lawyer, non-resident bank account, virtual viewings (general practice) | immobilier.co.il RU/FR guide 19.4.2026 |
| Capital gains (mas shevach) | 25% on real gain is the general rate for non-residents | immobilier.co.il (press), **[לאישור הבעלים]** |
| No residency from buying | buying property gives no residency or citizenship ("Israel does not have a real-estate golden visa") | guide sites; general law |
| Foreign-resident share of deals | "In January 2025, purchases by foreign residents in Israel totaled 150 apartments, about 1.9% of all transactions" | PRESS, Globes English 14.4.2025 |

---

## 11. What is NOT published (the article must say "לא פורסם" / "not published")
- Official tower height; floor-to-floor height; number of elevators (official).
- A current price list; which apartments are available; per-floor prices.
- Floor plans (behind a buyers' password on hagag-group.co.il); technical specification (מפרט).
- Management fees (דמי ניהול) and the management company.
- Balcony directions and views per apartment.
- Pool dimensions and floor (sources conflict).
- A contractual delivery date for new buyers; Form 4 date.
- The current accompanying bank.
- Number of basement levels.
