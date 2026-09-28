# DUO Tel Aviv: sold apartments by floor, sales figures, facilities (evidence)

Research date: 28.9.2026. Web research (WebSearch, WebFetch, curl on public pages) plus the developer's own
quarterly and annual reports, downloaded from the developer's investor-relations page and text-extracted locally.
No site writes, no git. No buyer is named anywhere in this file, even where the source names them.

Evidence classes: **REPORT** = Africa Israel Residences' own filing; **PRESS** = news article; **DEV** = the
developer's marketing site, or content the developer paid for; **CALC** = my arithmetic on published numbers.

---

## 1. Deal rows tied to a floor

Five rows meet the bar (floor published, or "penthouse" as published; source article reachable; quote checked in
the page text). **None of them comes from the Tax Authority.** Three come from the company's report to the Israel
Securities Authority, as the press quoted it. Two come from one Israel Hayom item. No press item with Tax Authority
deal data for DUO was found (see section 7).

| # | Floor (as published) | Building | Apartment | Price | Per m² | Date | Source | Via |
|---|---|---|---|---|---|---|---|---|
| D1 | Penthouse (floor not published) | not stated | penthouse, size not published | not published | **106,545 ₪** (published) | 4.2021 | Israel Hayom 21.4.2021 | press |
| D2 | **43** | not stated | not published | not published | **76,679 ₪** (published) | 4.2021 | Israel Hayom 21.4.2021 | press; a *purchase request* (בקשת רכישה), not a binding contract |
| D3 | **17** | "הבניין השני" (which tower not said) | 4 rooms, ~102 m² net, ~17 m² balcony, underground parking | ~7.44M ₪ | ~72,900 ₪ (CALC: 7.44M / 102) | 9.2021 | Merkaz HaNadlan 13.9.2021; Globes 11.10.2021 | company report to the ISA, pre-sale |
| D4 | **16** | "הבניין השני" | 4 rooms, ~102 m² net, ~17 m² balcony, underground parking | ~7.33M ₪ | ~71,900 ₪ (CALC) | 9.2021 | same | same |
| D5 | **12** | "הבניין השני" | 4 rooms, ~102 m² net, ~17 m² balcony, underground parking | ~7.03M ₪ | ~68,900 ₪ (CALC) | 9.2021 | same | same |

### D1 and D2: Israel Hayom, 21.4.2021
- URL: https://www.israelhayom.co.il/article/872519 (canonical: https://www.israelhayom.co.il/business/real-estate/article/5880526)
- Author and date on the page: עופר פטרסבורג, 21/4/2021.
- D1 quote: "דירת פנטהאוז בפרויקט נמכרה השבוע ב-106,545 שקל למ"ר."
- D2 quote: "בקשת רכישה נוספת בפרויקט, לדירה בקומה ה-43, נחתמה השבוע בסכום של 76,679 שקל למ"ר."
- Caveats: the penthouse's floor is NOT published (the licensing decision puts penthouses on 48-50, but that is
  not evidence of which floor this one is, so `n` stays 0). D2 is a purchase request, the pre-sale's first step, and
  only the per-m² figure was published. The same item says "בגובה 55 קומות", which conflicts with the 54 of the
  company's report (section 4).
- WebFetch got HTTP 403; the text was read from the raw HTML via curl with a browser user agent.

### D3 to D5: the September 2021 pre-sale of the second building
- Primary: Merkaz HaNadlan (nadlancenter.co.il), 13.09.21: https://www.nadlancenter.co.il/article/4320
  - "עסקת מכירה של שלוש דירות בבניין השני של פרויקט DUO של החברה במתחם סומייל בתל אביב"
  - D3: "דירה בת ארבעה חדרים בקומה ה-17 בפרויקט, ששטחה כ-102 מ"ר נטו, עם כ-17 מ"ר מרפסת וחניה תת-קרקעית, בתמורה לסך של כ-7.44 מיליון שקל"
  - D4: "דירה בת ארבעה חדרים בקומה ה-16, ששטחה כ-102 מ"ר נטו, עם כ-17 מ"ר מרפסת וחניה תת-קרקעית, בתמורה לסך של כ-7.33 מיליון שקל"
  - D5: "דירה בת ארבעה חדרים בקומה ה-12, ששטחה כ-102 מ"ר נטו, עם כ-17 מ"ר מרפסת וחניה תת-קרקעית, תמורת כ-7.03 מיליון שקל"
  - Basis: "כך דיווחה החברה לרשות לניירות ערך"; prices "בהתאם למחירים שנקבעו לדירות אלה במחירון הבניין השני (לאחר שקלול שיעורי הנחת המכירה המוקדמת)".
- Second source, Globes, 11.10.2021: https://www.globes.co.il/news/article.aspx?did=1001386775
  - "מדובר בדירות של ארבעה חדרים בשטח של קצת יותר מ-100 מ"ר כל אחת, בקומות 17-12, הממוקמות בבניין השני של הפרויקט."
  - It agrees on the floors (12 to 17), the building, the rooms and the size, and puts the three at ~22M ₪ together (the first source: ~21.8M).
- The underlying filing is the company's immediate report of 13.9.2021, reference 2021-01-078610 (listed in the 2025
  annual report's DUO section). I could not open it: Maya's report-search API returned a WAF block.
- **Sensitivity (for the owner):** these three were related-party sales, and both articles name the buyers. The
  proposal does not name or describe them. It only says the prices were pre-sale prices by the company's report,
  which is also what the company said. If the owner prefers only arm's-length deals, D3 to D5 go, and then fewer
  than 2 rows remain (D1 has no floor and D2 is a purchase request). In that case the section should not be printed.
- Per m² is **calculated**: the published price divided by the published net area, without the balcony and
  parking, which is the page's own rule ("המחיר למ״ר מחושב: המחיר שפורסם חלקי שטח הדירה, בלי המרפסת והחניה").
  Parking is included in the price, so the true per-m² for the apartment alone is a little lower.

### Floor numbering vs the stage
The stage (assets/project-stage/duo/stage.js) models residential floors 1-50 with penthouses on 48-50, following
the licensing decision's numbering. Published floors 12, 16, 17 and 43 are within 1-50 and are used as `n` as
published. Which tower "the second building" is (north lot 111 or south lot 112) is **not published**, so the floor
card notes say "באחד המגדלים" / "הבניין השני" and do not pick a tower.

---

## 2. Deals found but NOT tied to a floor (not in the proposal)

| What | Detail | Source | Why excluded |
|---|---|---|---|
| 5 apartments, one buyer, 4.2026 | four 5-room apartments of ~160 m² and one 4-room apartment of ~100 m², each with parking, "כולן דירות מערביות עם נוף לים"; "יותר מ־82 אלף שקל למ"ר, בממוצע"; ~65.2M ₪ in all (ICE) | Globes 19.04.2026 https://www.globes.co.il/news/article.aspx?did=1001540082 ; Globes English https://en.globes.co.il/en/article-businessman-buys-5-tel-aviv-apartments-in-dou-project-1001540437 ; ICE https://www.ice.co.il/realestate/news/article/1110041 | no floor published. Could be added with floor "לא פורסמה" if the owner wants it; the heading is "לפי קומה", so I left it out |
| 3 apartments, related parties, 1.2021 | 2 rooms ~59 m² + ~15 m² balcony, ~3.29M ₪; 4 rooms ~102 m² + ~17 m² balcony, ~5.28M ₪; 4 rooms ~102 m², ~5.11M ₪ | Merkaz HaNadlan 14.01.21 https://www.nadlancenter.co.il/article/3313 | no floor |
| 23 related-party apartments, 2021 | "טווח המחירים בעסקאות הללו עמד על 3-7.5 מיליון שקל לדירה" | Globes 11.10.2021 (above) | a range, no floors |
| Recent deals by other buyers, 2026 | "המחירים נעים בין 80-85 אלף שקל למ"ר. הרף הגבוה הוא בקומות הגבוהות" | ICE 22.4.2026 https://www.ice.co.il/realestate/news/article/1110182 | no floor or apartment |
| Broker **asking** price | 4 rooms, floor 18, 176 m², 12.5M ₪ (Ronkin listing, in the page's dossier) | data/projects/dossiers/duo-tel-aviv-2026-07-04.txt | an asking price, not a sale. Must never enter the deals table |

---

## 3. Sales figures (with sources)

All REPORT figures refer to the partners' marketable share (510 of 668 units).

| Figure | Value | As of | Source and quote |
|---|---|---|---|
| Units sold (signed contracts) | **372 of 510** | 30.6.2026 | REPORT, Q2 2026, board report section 1.3 (PDF p.23): "DUO TLV7 70% 668 510 372 1,338,612 87% 2027" (footnote 4: signed contracts only, not purchase requests). https://res.afi-g.com/about/Documents/2026/Q2-2026.pdf |
| Units not yet sold | **138** | 30.6.2026 | REPORT, Q2 2026, section 7.13.2 table (PDF p.6). The CEO gave the same 138 in Globes 19.4.2026: "לחברה נותרו עוד 138 דירות למכירה" |
| Engineering/financial completion | **87%** | 30.6.2026 | REPORT, Q2 2026 (PDF p.6 and p.23) |
| Sales in 1-6.2026 | **12 units**, 111,715K ₪ before VAT, **10,985K ₪ average per unit incl. VAT** | 30.6.2026 | REPORT, Q2 2026, section 3.5 "התפלגות מכירות 1-6/2026" (PDF p.31): "DUO TLV 12 111,715 10,985" |
| Avg price per m², contracts signed 1-6.2026 | **71K ₪ before VAT** (~83.8K incl. 18% VAT, CALC) | 30.6.2026 | REPORT, Q2 2026, section 7.13.2 (PDF p.6), column "מחיר מכירה ממוצע למ"ר בחוזים שנחתמו בפרויקט ללא מע"מ בתקופה 1-6/26" |
| Q1 2026 | 366 sold, 144 unsold, 9 units sold in the quarter, 64.8K ₪/m² before VAT, 10,508K ₪ average per unit incl. VAT, 82% completion | 31.3.2026 | REPORT, Q1 2026 (PDF pp.8, 29, 36) https://res.afi-g.com/about/Documents/2026/Q1-2026.pdf . Calcalist 20.5.2026 gives the same quarter as "76.5 אלף שקל" per m² and "10.5 מיליון שקל לדירה": https://www.calcalist.co.il/market/article/gq3hvod1j (76.5 = 64.8 × 1.18, CALC, so Calcalist's figure includes VAT) |
| 2025 | 13 units, 1,281 m², **69.9K ₪/m² before VAT**; cumulative 361 units, 33,885 m², 53.5K ₪/m² before VAT; 149 unsold; 5 more contracts after year-end at 65K ₪/m² | 31.12.2025 | REPORT, 2025 annual report, section 7.13.2 DUO (PDF p.45) https://res.afi-g.com/about/Documents/2025/12-2025.pdf (Maya reference 2026-01-026862, 25.3.2026) |
| 2025 incl. VAT | "ב־2025 מכרנו במחיר ממוצע של 82.5 אלף שקל למ"ר" | 4.2026 | PRESS, the CEO in Globes 19.4.2026 (82.5 = 69.9 × 1.18, CALC: the same number with VAT) |
| Sales by year | 2021-2022: 329; 2023: 10; 2024: 9; 2025: 13 | | PRESS, Globes 19.4.2026 and 12.3.2025 https://www.globes.co.il/news/article.aspx?did=1001504367 ; REPORT, 2025 (2023: 10, 2024: 9, 2025: 13) |
| Price the company assumes for unsold stock | residential 76K ₪/m² before VAT; **69K without penthouses** | 31.12.2025 | REPORT, 2025 (PDF p.46), footnote: "המחיר הממוצע למ"ר לדירות בנטרול דירות פנטהאוז הוא 69" |
| Price point from the developer | "דירות שני חדרים ב־4 מיליון שקל, וגם פנטהאוזים" | 4.2026 | PRESS, the CEO in Globes 19.4.2026 |
| Older press price points | "המחיר הממוצע למ״ר עומד על 76 אלף שקל למ״ר", "דירת 4 חדרים עולה כ-10 מיליון שקל" | 15.4.2024 | PRESS, Bizportal https://www.bizportal.co.il/realestates/news/article/826621 |
| Early sales | pre-sale to end-12.2020: 127 apartments; 277 of ~510 released; 150 units / ~700M ₪ by 8.2021; 250 sold, average 6.5M ₪ per apartment by 10.2021 | 2020-2021 | Merkaz HaNadlan 14.1.2021 (3313); Calcalist 17.8.2021 https://www.calcalist.co.il/market/article/hkt11tfkgt ; Calcalist 25.10.2021 https://www.calcalist.co.il/real-estate/article/s1j54r7it |

### Construction status and occupancy
- REPORT 2025: full permit December 2021; main contractor Electra Construction and Danya Cebus, signed 14.8.2022;
  "מסחר ומגורים מתוכניים לשנת 2027"; financial completion 76% at 31.12.2025. REPORT Q2 2026: 87%, completion 2027
  (footnote 5: the expected end of construction and start of occupancy).
- PRESS, the CEO in Globes 19.4.2026: "אנחנו רואים שריאלי ניתן יהיה להוציא טופס 4 ברבעון השני של 2027".
- PRESS, Bizportal 15.4.2024: "הפרויקט נמצא בשלב שלד, קומה 24, ושש קומות מרתף".
- Electra's project page (checked 28.9.2026) still says "דצמבר 2026":
  https://www.electra.co.il/%D7%90%D7%9C%D7%A7%D7%98%D7%A8%D7%94_%D7%91%D7%99%D7%9C%D7%93%D7%99%D7%A0%D7%92/%D7%A4%D7%A8%D7%95%D7%99%D7%A7%D7%98%D7%99%D7%9D/%D7%9E%D7%92%D7%93%D7%9C%D7%99_dou_%D7%A1%D7%9E%D7%9C_%D7%93%D7%A8%D7%95%D7%9D

---

## 4. Conflicts between sources

| Field | Versions | Reading |
|---|---|---|
| Price per m² | 69.9 vs 82.5 (2025); 64.8 vs 76.5 (Q1 2026); 71 vs ~83.8 (H1 2026) | the same numbers before and after 18% VAT (CALC). The page article puts "69.9 לפני מע״מ" next to Calcalist's 76.5 without saying that 76.5 includes VAT |
| Units sold at end-2025 | 361 (REPORT) vs "357 דירות - 70%" (ICE 22.4.2026) | follow the report |
| Price in Q1 2025 | "84.2 אלף שקל" (ICE) vs 2025 full-year 69.9 before VAT (REPORT) | ICE's number is not in the reports I read; not used |
| "Marketing rate" | 61% (REPORT 2025 table) vs 361/510 = 71% by units (CALC); "כ-70% מפרויקט DUO מכור" (Bizportal 18.8.2024) | the report's 61% is a different measure. Say "372 מתוך 510", never a percent |
| Floors | 54 with 50 residential (REPORT, Globes) vs 50 (developer site, Electra, Bizportal) vs 55 (Israel Hayom 2021 and 2023, which adds "200 מטר") | the page already uses 54 / 50 residential; keep it |
| Parking basements | 5 (Electra; the licensing decision as the page cites it) vs "שש קומות מרתף" (Bizportal 4.2024) vs up to 6 (city property record, in the dossier) | the page article already flags it |
| Commercial area | ~13,000 m² gross (REPORT 2025, Globes) vs ~12,000 (Israel Hayom) vs 9,620 m² main (REPORT "מצב תכנוני") vs ~10,000 m² main, of them ~7,300 for sale (REPORT Q2 2026 footnote 1) | gross vs main area; say "כ-13 אלף מ״ר ברוטו" with the report as source |
| Completion | 2027 (REPORT); Form 4 in Q2 2027 (CEO); "דצמבר 2026" (Electra); "תחילת האכלוס ב 2027" (developer-paid Ynet piece) | Electra's page is out of date |
| Company's share | 70% (report tables) vs "כ- 52%" (project page of the 2025 report) vs the partners' 74.26% | not used on the page |

---

## 5. Facilities: what the sources say vs facilities.json

Developer site, checked 28.9.2026: https://www.duo-tlv.com/residential-towers/
- Pool: "הבריכה ממוקמת על גג מבנה הלובי בין שני מגדלי המגורים". It also lists "בריכת 'אינסוף' (Infinity Pool) חיצונית, הכוללת בריכת פעוטות ומרחבי ישיבה ושיזוף". **Confirms** facilities.json.
- Lobby: "קומת הקרקע בגובה המרשים של כ-7 מטרים תשמש כלובי ראשי המחבר את שני מגדלי המגורים" and "בכל קומה תוכנן גם לובי קומתי מעוצב". **Confirms**.
- Wellness: "מתחם רווחת הדיירים מתוכנן כקומפלקס עצמאי בעל כניסה ישירה מהלובי ... מכיל חדר כושר יוצא דופן בגודלו. במתחם תמצאו גם את מרחב הבריכה". **Small correction:** the site places the pool area *inside* the wellness complex, and the gym is "יוצא דופן בגודלו" or "מועדון כושר מאובזר", not "מתקדם". The club line in facilities.json is still fair ("מועדון לרווחת הדיירים" is in the services list).
- Gym size: "חדר כושר מרווח ומצויד אשר מתפרש על פני 300 מ"ר" in Ynet 25.8.2025, content "מוגש מטעם אפריקה ישראל" (developer-paid): https://www.ynet.co.il/article/bjik0afyxg . It could be added to the club card as "לפי היזם".
- Globes 19.4.2026: "הפרויקט יכלול חדר כושר, לאונג' לדיירים, בריכה וספא" and "יש חיבור ישיר לקו הירוק בקומה במינוס אחת של הפרויקט" (the CEO). The light-rail link is not in facilities.json or the facts.
- Private pools on penthouse floors 49-50: **no developer or press source found**. Only the licensing decision
  (as cited in docs/research/2026-09-28-stages/stage-geometry.md, which I did not re-open) mentions them. The card
  already cites the decision. Nothing contradicts it.
- Retail: "מתחם מסחר בשלוש קומות בשטח של כ -13,000 מ"ר ברוטו (כולל מסחר במרתף-1)" (REPORT 2025). **Confirms** "מתחם מסחרי בן 3 קומות".

---

## 6. What on the page my sources contradict or leave out of date

1. **The deals section's fixed intro** (nadlan_ps_deals in inc/project-stage.php) says the rows are "לפי נתוני רשות המסים כפי שפורסמו בעיתונות". **None of DUO's rows comes from the Tax Authority.** Shown as is for DUO, that line would be false. The function needs a per-project intro (the proposal suggests a `deals_intro` key; the code change is not made). The footer "המחיר למ״ר מחושב" is also not true for D1 and D2, where the per-m² figure was published. Those rows say "כפי שפורסם".
2. **The article's sales section is out of date.** It uses Q1 2026 (144 unsold) and 2025. The current figure is 372 sold, 138 unsold, 87% complete (30.6.2026).
3. **VAT mixing** in the article's price line: "69.9 אלף לפני מע״מ" sits next to Calcalist's 76.5 and Globes' 82+, which include VAT. That is not a contradiction, but a reader will take it as a price gap.
4. **Electra's "דצמבר 2026"** in the article is superseded by the CEO's "טופס 4 ברבעון השני של 2027" (Globes 19.4.2026).
5. The facts row "מצב: בבנייה, השלמה מתוכננת ב-2027" is **confirmed**. So are "2 מגדלים של 54 קומות, 50 קומות מגורים", 668 units, the pool on the lobby roof, and permit 12.2021.
6. The broker asking price (floor 18, 12.5M ₪) in the article must stay labelled as an asking price. It is not a deal.

---

## 7. What I searched and did not find

- Queries run (Hebrew and English): "דואו תל אביב עסקה קומה", "DUO תל אביב נמכרה דירה", "מגדלי DUO אבן גבירול נמכרה", "אפריקה ישראל מגורים דואו מכירות", "DUO Tel Aviv apartment sold floor", "סמל דרום" + קומה, "ארלוזורוב 85/87", penthouse and private-pool deal searches, Globes English "Dou", Tax Authority phrasing ("רשות המסים" + DUO/סומייל), Ynet "בכמה נמכרה", ICE, Bizportal, Calcalist, TheMarker, Israel Hayom, Merkaz HaNadlan, project-tlv.info.
- **No Tax Authority deal (floor, size, price) for DUO was found in the press.** The weekly deal columns (Globes, Ynet/Madlan, TheMarker "עסקה בשבוע") did not surface a DUO row. Developer sales in a building under construction often reach those columns only after registration.
- **Not reachable:** Madlan's DUO project page (HTTP 403); TheMarker's premium article on the 127 pre-sale requests (paywall); Maya's report-search API (WAF block), so the 13.9.2021 immediate report itself was not opened; nadlan.gov.il was not attempted (a scripted app).
- **Not published anywhere I found:** the floor of the 2021 penthouse; the floors of the five apartments of 4.2026; which tower is "the second building"; any developer price list.

## 8. Files used
- Developer reports (downloaded to the session scratchpad, text-extracted with pdftotext/pypdf): Q2-2026.pdf, Q1-2026.pdf, 12-2025.pdf from https://res.afi-g.com/about/Pages/investorrelations.aspx
- Page config read: plugins/nadlan-config/inc/project-stage.php ('rainbow-tel-aviv' deals format, 'duo-tel-aviv'); plugins/nadlan-config/assets/project-stage/duo/facilities.json; data/projects/duo-tel-aviv.json; data/projects/dossiers/duo-tel-aviv-2026-07-04.txt
