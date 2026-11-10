# Mirror of page one: what the pages Google ranks for "פרויקטים חדשים" actually contain (10.11.2026)

Read-only research. Nothing was changed on any site, no form was sent, no sign-up, no cookie banner was clicked, no CAPTCHA was met.
Builds on `serp.md`, `competitors.md`, `autocomplete.md`, `related.md`, `keyword-map.md`, `our-pages.md`, `intent-overlap.md` (9.11.2026). Those are not repeated here.

**Method and evidence class**
- Browser: the owner's Chrome, one own tab, closed at the end. Google: `google.co.il/search?q=...&hl=iw&gl=il`. Browser location: Tel Aviv area (results lean to Tel Aviv).
- All times are UTC on 10.11.2026 (Israel time = UTC+2). Each fact below carries the page and the time it was read.
- Evidence class: **code** (page text, DOM, JSON-LD read through the browser tools). One low-resolution screenshot of the Google result page was looked at (it showed the AI box). Photo type (render or real photo) was **not judged**, because no screenshots of competitor pages were looked at; only image sizes and ratios were measured.
- "First phone screen": measured by loading each page inside a 375 x 812 px frame of the same origin and listing the text and images whose box falls inside that frame. The browser still reports a desktop user agent, so a site that serves different HTML to phones by user agent may differ. A true phone was not used (the Chrome window could not be narrowed to 375 px).
- Word count = all visible words in the rendered page, including menus, cookie dialogs and footers.
- The Google result pages show a private Search Console card for nad-lan to the signed-in owner. Its numbers were deliberately not recorded (public repo).
- No page blocked the reading. Yad2 and Madlan opened normally in the owner's Chrome.

---

## 0. Three findings to read first

1. **The Tel Aviv immediate-occupancy URL answers 301 today.** `https://nad-lan.co.il/new-projects/new-projects-tel-aviv/` returned `301 Moved Permanently`, `Location: https://nad-lan.co.il/projects/`, header `X-Redirect-By: nad-lan` (direct request, 10:25 UTC). At the same hour Google still ranked that URL **3rd** for "דירות חדשות לאכלוס מיידי" and cited it as a source in both the AI box and AI Mode for that query. Reported as a finding only.
2. **Google's page changed since yesterday.** For the head query "פרויקטים חדשים" the AI box ("תקציר מ-AI") and a "אנשים שאלו גם על" block were both **present** today (10:14 UTC); on 9.11 both were absent. The AI box was present on **all five** queries today. The order also moved: Madlan first, Yad2's `/yad1` second (yesterday Yad2's Tel Aviv list was first).
3. **The leaders are thin list pages.** Median page length of the 13 pages in the top 5 is about 950 words and 8 of the 13 are under 1,000; Dimri (3rd for the head query) has 313, Tidhar (4th) 282. Nine of the 13 put the project list directly under the H1 with no paragraph. Our page has 6,663 words and its first phone screen holds two paragraphs and no card.

---

## 1. Today's order (top organic results, 10.11.2026)

| Query | Read (UTC) | 1 | 2 | 3 | 4 | 5 | AI box | People also ask |
|---|---|---|---|---|---|---|---|---|
| פרויקטים חדשים | 10:14 | madlan `/projects-for-sale/ישראל` | yad2 `/yad1` | dimri `/projects` | tidhar `/residences/for-sale/` | socity `/city/פרויקטים-חדשים-בתל-אביב/` | present | present (15 questions) |
| דירות חדשות | 10:16 | madlan ישראל | yad2 `/yad1` | nadlan.com `/` | yad2 `/yad1/newprojects/tel-aviv-area` (with area and city parameters) | dimri `/projects` | present (news style) | absent |
| דירות מקבלן | 10:16 | madlan ישראל | yad2 `/yad1` | dimri `/projects` | yad2 tel-aviv-area | nadlan.com `/` | present (buyer guide) | absent |
| פרויקטים חדשים בתל אביב | 10:16 | yad2 tel-aviv-area | madlan `/projects-for-sale/תל-אביב-יפו-ישראל` | myplace `/פרויקטים-חדשים/` | socity | tidhar `/projects-in-tel-aviv/` | present | absent |
| דירות חדשות לאכלוס מיידי | 10:17 | yad2 tel-aviv-area with `immediateOccupancy` parameter | ashtromegurim `/projects/projects-past` | **nad-lan** `/new-projects/new-projects-tel-aviv/` | nadlan.com `/` | selabinui `/project/דירות-לדוגמה-למכירה-לאכלוס-מיידי/` | present | absent |

Positions 6 and below today: head query: nadlan.com, tel-aviv.gov.il. דירות חדשות: digg.co.il, maariv (news). דירות מקבלן: peretzbh, madlan Tel Aviv. Tel Aviv: tel-aviv.gov.il, etzhashaked, hagag. Immediate: madlan Tel Aviv, dimri, yad2 tel-aviv-area, diur-plus.
nad-lan `/projects/` is not in the top 10 of the first four queries.

**13 distinct competitor pages** make up the 25 top-5 places (plus one page of ours). They are the "page one" set used in the matrix:
M-IL (Madlan Israel) · Y1 (Yad2 `/yad1`) · DIM (Dimri) · TID (Tidhar for sale) · SOC (Socity Tel Aviv) · NCOM (nadlan.com home) · Y-TLV (Yad2 Tel Aviv area) · M-TLV (Madlan Tel Aviv) · MYP (MyPlace) · TID-TLV (Tidhar Tel Aviv) · Y-IMM (Yad2 immediate occupancy) · ASH (Ashtrom Megurim ready flats) · SELA (Sela Binui sample flats).

---

## 2. The 13 pages, element by element

### 2.1 Madlan Israel: `madlan.co.il/projects-for-sale/ישראל` (read 10:18, phone frame 10:27)
- **Title:** דירות ופרויקטים חדשים בישראל | מדלן
- **Meta description:** one sentence with a live count ("...ל-422 דירות למכירה...", "המתעדכן מידי יום").
- **H1:** דירות ופרויקטים חדשים למכירה בכל הארץ
- **H2, in order:** 422 דירות ופרויקטים חדשים למכירה · הכתבות הנצפות ביותר. Then 44 H3, all article titles. The nearby block "פרויקטים חדשים בסביבה" is not a heading.
- **First 150 words under the H1:** no prose. The count line, three tabs (פרויקט חדש / תיווך / פרטי), the sort label, then project cards straight away.
- **Words:** 1,791 (most of it article titles and cards).
- **Cards:** about 50 on the page (25 are in the schema). Fields: badge line (פרויקט במבצע! / פרויקט חדש), project name, "דירות 4-2 חד׳", "7 קומות", street + neighbourhood + city, "החל מ - 5,600,000 ₪" on some, one developer promo line (for example "3 חד' החל מ- 5,600,000 ₪", "שלמו 10% - היתרה באכלוס!", "1.99% ריבית קבועה-15 שנה", "משלמים בעוד שנה!"). Photo ratios measured: 3:2 and 1:1.
- **Filters and sort (exact labels):** מחיר · חדרים · סוג נכס · מסננים נוספים · יצירת התראה · search field "כתובת, שכונה, בי״ס..." · "מיון לפי: רלוונטיות".
- **Default list:** whole country, sort by relevance. In this browser 5 of the first 6 cards are in Tel Aviv and one in Herzliya.
- **Map:** no map in the desktop page text; a floating "מפה" button and a floating "התראה" button sit at the bottom of the first phone screen.
- **Nearby module:** "פרויקטים חדשים בסביבה": name, "החל מ-" price, buildings, rooms, floors, **number of flats**, address.
- **FAQ:** none.
- **Link blocks:** "דירות ופרויקטים בערים פופלריות" (תל אביב יפו, רמת גן, רעננה, חיפה, ירושלים, באר שבע, each as "דירות חדשות למכירה ב...") · "דירות ופרויקטים לפי אזור" (מרכז, גוש דן, צפון, שפלה, דרום) · "דירות מסוגים שונים" (דירות גן, בתים פרטיים וקוטג׳ים, דירות פנטהאוז, דופלקס, בית דו משפחתי) · יזמי נדל"ן בישראל · מתווכים.
- **Schema:** BreadcrumbList, ItemList, **ApartmentComplex x25**, PostalAddress x25. (Yesterday's note "no usable JSON-LD" is corrected by this read.)
- **First phone screen:** search field, H1 at 160 px, the three tabs, "422 תוצאות", sort, first card photo (293 x 170) at 344 px with name, rooms, floors, address and "3 חד' החל מ- 5,600,000 ₪"; floating התראה and מפה buttons.

### 2.2 Yad2 `/yad1` (read 10:19)
- **Title = H1:** המקום המוביל לחיפוש פרויקטים ודירות חדשות בישראל (| יד2 in the title)
- **Meta description:** repeats the title phrase twice and adds a call to enter the site.
- **H2, in order:** פרויקטים מומלצים · חברות בנייה ויזמות נדל"ן נבחרות · פרויקטים בתלת מימד · הצטרפו למיליוני מחפשי פרויקטים חדשים בישראל. H3: search facets (סוג עסקה, חיפוש, מחוז, אזור, עיר, שכונה, רחוב, פרויקט, חברה) and ten developer names.
- **First 150 words under the H1:** a tab הכל / נדל״ן בחו״ל, an abroad banner, then "יזם החודש" and cards. No prose.
- **Words:** 1,368.
- **Cards:** about 56 (41 show a price). Fields: "פרויקט חדש" label, one promo line (כניסה מיידית!, הבנייה בעיצומה, משלמים 20% והיתרה באכלוס, PRESALE, תנאי תשלום 20/80), name, address, "3-5 חדרים • 0-6 קומות • 78-350 מ״ר", "החל מ- 1,990,000 ₪", a "3D" badge in the 3D strip. Photo ratio about 1.88:1 (52 images).
- **Top navigation:** פרויקטים חדשים · נדל״ן חו״ל · חברות נדל"ן · פרויקטים במבצע · יזם החודש · מפה · פרסום פרויקט.
- **Filters:** one search field "חיפוש לפי חברה, פרויקט או מיקום". No sort.
- **Default list:** national and promoted: "יזם החודש", then a mix (נתניה, ראשון לציון, יפו, אילת, טירת כרמל, אשדוד, עכו, חדרה, רמלה, רחובות...). On a second visit at 10:27 the same URL opened the Tel Aviv area list, so the site seems to remember the last area.
- **Developer directory:** ten developers with counts ("קבוצת שבירו יזמות ובנייה 26 פרויקטים", "עמרם אברהם 22 פרויקטים"...). Google uses this block as the result snippet.
- **Link blocks:** six districts in this order: מרכז והשרון · דרום · תל אביב והסביבה · מישור החוף הצפוני · ירושלים והסביבה · צפון והעמקים; under each: דירות חדשות, דופלקסים, קרקעות, דירות גן, בתים על הים (and משרדים, מרכזים מסחריים in some).
- **Schema:** none. **FAQ:** none. **Map:** a nav link only.

### 2.3 Yad2 Tel Aviv area: `yad2.co.il/yad1/newprojects/tel-aviv-area` (read 10:19, phone frame 10:27 and 10:28)
- **Title:** פרויקטים ודירות חדשות בתל אביב והסביבה - מעודכן ל-2026 (Google shows the variant "...בתל אביב יפו - מעודכן ל-2026" for the URL with area and city parameters).
- **Meta description:** the title phrase plus "לעוד פרטים ומידע נוסף היכנסו עכשיו".
- **H1:** פרויקטים ודירות חדשות בתל אביב והסביבה
- **H2, in order:** מצאו את המקום שלכם בתל אביב והסביבה · פרויקטים נוספים באזור זה (12 H3 project names) · גלו הכל על הבית ואזור המגורים שלכם · דירות חדשות, פרויקטים חדשים, דירות מקבלן.
- **First 150 words under the H1:** cards only.
- **Words:** 996.
- **Cards:** 18 per page, 8 pages, plus 12 name-and-address rows under "פרויקטים נוספים באזור זה". Fields: badges **במבצע** and **אכלוס קרוב**, name, street + neighbourhood + city, "4.5-5 חדרים • 1-8 קומות • 112-131 מ״ר", "החל מ- 3,299,000 ₪", on one card "החל מ־39,000 ₪ למ"ר", one promo line (for example "5 חד' החל מ- 3,990,000 ₪", "משלמים 1M בלבד במעמד החוזה"). 14 of 18 cards show a price. Photos: 18 of 18 at exactly 3:2.
- **Filters (exact labels):** דירות חדשות / הכל · סוג הנכס · מחיר (₪ 0 to ₪ +20,000,000) · חדרים (1, 1.5 ... 5.5, +6) · אכלוס קרוב · סיורי 3D · search "אזור, עיר, שכונה או פרויקט" · buttons חיפוש, איפוס, אישור, מפה.
- **Sort:** no sort control. The first card differed on three loads within ten minutes (a Bat Yam project, then a Ramat Gan project, then a Tel Aviv project), so the default order rotates; cards badged "במבצע" lead.
- **Map:** yes (Mapbox on the page, a "מפה" button; on the phone frame a floating "מפה" button).
- **Link blocks:** דירות חדשות לפי מחוז (5) · דירות חדשות לפי אזור (תל אביב יפו, רמת גן וגבעתיים, חולון ובת ים) · **דירות חדשות לפי מספר חדרים** (5, 6, 4, 3, 7 חדרים בתל אביב והסביבה) · נכסים מסוגים שונים (קרקעות, דופלקסים, דירות גן, בתים על הים) · מידע נוסף (הערכת שווי נכס - מחשבון נדל״ן) · פרויקטים חדשים ב-7 districts · דירות למכירה ב-13 cities · דירות להשכרה ב-13 cities · **עמודים פופולריים** (דירות חדשות למכירה, דירות מקבלן, דירות חדשות להשכרה, נדל״ן מסחרי חדש, חברות נדל״ן, בתים חדשים, דופלקסים, בית ליד הים, קרקעות להשקעה, מבצעים).
- **Foot paragraph** under the H2 "דירות חדשות, פרויקטים חדשים, דירות מקבלן": about 70 words promising virtual tours, the real view from each window, data tools and project comparison.
- **Schema:** ItemList, **RealEstateListing x18**, **ApartmentComplex x18**; BreadcrumbList as microdata. **FAQ:** none.
- **First phone screen:** H1 at 139 px, first card photo (320 x 213) at 207 px, name, address, rooms, "החל מ- 4,550,000 ₪", promo line, start of the second card, floating "מפה".

### 2.4 Yad2 immediate occupancy: same path with the `immediateOccupancy` parameter (read 10:20)
- **Title:** פרויקטים ודירות חדשות בתל אביב והסביבה לאכלוס קרוב - מעודכן ל-2026
- **H1:** **14** פרויקטים ודירות חדשות בתל אביב והסביבה לאכלוס קרוב (the count is in the H1 and Google prints it in the result title).
- **Canonical:** points to itself **with** the parameter; robots "follow, index". The filtered view is an indexable page of its own.
- 14 cards, every one badged "אכלוס קרוב", 8 also "במבצע"; 13 of 14 with a price. Promo lines include "אכלוס מיידי!" and "דירה תל אביבית באכלוס מיידי". Same headings, filters, link blocks and schema (ItemList, RealEstateListing x14, ApartmentComplex x14) as 2.3. Words: 956.

### 2.5 Dimri: `dimri.co.il/projects` (read 10:20, phone frame 10:28)
- **Title:** פרויקטים חדשים בשיווק | י.ח דמרי
- **Meta description:** a range of new projects by the company, four city names, ends with "מגוון דירות חדשות מקבלן למכירה".
- **H1:** פרויקטים חדשים בשיווק. **H2:** 19 project names, nothing else.
- **First 150 words under the H1:** breadcrumb, region tabs, filters, then cards. No prose.
- **Words:** 313. No canonical tag, no robots tag. hreflang he-IL, en-IL.
- **Cards:** 19. Fields: status badge (בשיווק on 18, פריסייל on 1), name, city, "החל מ 2,175,000" on 13. No rooms, no address, no delivery date. Photos 4:3 (19 of 19).
- **Filters (exact labels):** region tabs שפלה · מרכז · דרום · צפון · "בחירת עיר" · "סוג נכס" (דירת 2 חדרים, 2.5, 3, 4 חדרים, 6, **דירת גן, מיני פנטהאוז, פנטהאוז**) · a price slider (₪ 1,340,000 to ₪ 17,990,000). No sort.
- **Default list:** all 19, three featured first (נתניה, אור יהודה, נתיבות), then alphabetical.
- **Link blocks (footer):** פרויקטים לפי אזור (בדרום, במרכז, בצפון) · פרויקטים חדשים באשקלון / בפתח תקווה / בנתניה / באשדוד · פרויקטים באופקים.
- **Schema:** none. **FAQ:** none. **Map:** none.
- **First phone screen:** H1 at 167 px, a hero image, the first card's photo and "בשיווק" badge; the lower third is a cookie notice.

### 2.6 Tidhar: `tidhar.co.il/residences/for-sale/` (read 10:20, phone frame 10:28)
- **Title:** פרוייקטים חדשים | פרוייקטים בשיווק למגורים | תדהר
- **H1:** פרויקטים בשיווק למגורים. No H2. **H3:** 14 tiles, each "project name ,city".
- **Words:** 282 (about 70 of them a cookie dialog).
- **Cards:** 14 tiles with name and city only. No price, rooms or status. Tall photos (about 2:3).
- **Filters (exact labels):** עיר ("בחרו עיר": אשדוד, בת ים, גבעת שמואל, הרצליה, לוד, תל אביב) · סוג הנכס (2, 3, 4, 4.5, 5, 6, 7 חדרים, **דופלקס, דירות גן, פנטהאוז**) · טווח מחיר (0 to 23 מיליון ₪) · נקה סננים · **להצגת המפה**.
- **Default list:** all cities, Tel Aviv projects first.
- **Schema:** WebPage, BreadcrumbList, WebSite, Organization. **FAQ:** none.
- **First phone screen:** a cookie dialog over a hero image; H1 at 515 px; the city filter starts at 771 px. No card.

### 2.7 Tidhar Tel Aviv: `tidhar.co.il/projects-in-tel-aviv/` (read 10:23)
- **Title:** פרויקטים בתל אביב - מגורים - תדהר. **Meta description:** none. **H1:** פרויקטים בתל אביב.
- 7 tiles (name and city). Same three filters as 2.6. 243 words. Same schema set. Ranks 5th for the Tel Aviv query.

### 2.8 Socity: `socity.co.il/city/פרויקטים-חדשים-בתל-אביב/` (read 10:21, phone frame 10:29)
- **Title:** פרויקטים חדשים בתל אביב | דירות למכירה בצפון הישן והחדש 2026
- **Meta description:** projects on sale in Tel Aviv "כולל מחירים אמיתיים לפי שכונה", where to buy, pros and cons, best deals.
- **H1: none.** The page opens with an **H2** "פרויקטים חדשים בתל אביב".
- **H2, in order:** פרויקטים חדשים בתל אביב · להורדת מפרט הדירות (twice, one per project) · איפה יש פרויקטים חדשים בתל אביב · יתרונות וחסרונות של פרויקטים חדשים בתל אביב · פרויקטים בשיווק בתל אביב - פרויקטים בולטים · מדוע לרכוש דירה חדשה בתל אביב · שאלות/תשובות · עוד מהבלוג שלנו · lead-form and footer headings. **H3:** יתרונות של..., אתגרים וחסרונות של..., **פרויקטים חדשים בתל אביב מחירים**.
- **Opening (paraphrased):** two own project cards, then about 300 words saying Tel Aviv has the most new projects each year, that the municipal quarters plan channels renewal into quarters 3 to 6 and that most new building is renewal in boutique buildings.
- **Words:** 1,855. One table.
- **Price sentence (pattern):** "מחירי פרויקטים בשיווק בתל אביב נעים בטווח שבין 35,000 ש"ח למ"ר ל- 100,000 ש"ח למ"ר". Google's AI Mode repeats this range for the Tel Aviv query.
- **Table columns:** רובע · אזורים עיקריים · % מאוכלוסיית העיר · מחיר ממוצע 4 חד׳ · שכירות חודשית 4 חד׳ (for example quarter 3: 6.0 to 8.0 מיליון ₪).
- **FAQ (10):** איפה יש כיום פרויקטים חדשים בתל אביב? · האם פרויקטים חדשים בתל אביב הם רק בהתחדשות עירונית? · כמה זמן לוקח לקדם פרויקט חדש בתל אביב? · האם כדאי לקנות דירה על הנייר בתל אביב? · מה חשוב לבדוק בפרויקטים בשיווק בתל אביב? · האם יש יתרון ברכישת דירה מחברה שהמיקוד שלה הוא פרויקטים בתל אביב? · מה היתרון של בנייני בוטיק בפרויקטים חדשים בתל אביב? · האם יש תשואה טובה על דירות חדשות בתל אביב? · מהן המגבלות שחלות על פרויקטים בתל אביב? · מהן ההטבות שנהוג להציע לרוכשי דירות בפרויקט בניה חדש בתל אביב?
- **Filters, sort, map:** none. Lead form (שם, מס' טלפון, אימייל), floating "השאירו פנייה" and "שלחו וואטסאפ".
- **Schema:** Place, Organization, WebSite, CollectionPage (no FAQPage). hreflang he, en.
- **First phone screen:** cookie dialog, the H2 at 121 px, first own project photo and "להורדת מפרט הדירות".

### 2.9 nadlan.com home (read 10:21, phone frame 10:29)
- **Title:** NADLAN.COM | לוח דירות חדשות, פרויקטים חדשים ודירות קבלן במחירים מיוחדים ומידע מקיף על הפרויקטים והסביבה
- **H1:** NADLAN.COM | נדל"ן.קום לוח נדל״ן: דירות חדשות, פרויקטים חדשים, קרקעות והשקעות נדלן
- **H2:** 8 card and article titles. No section headings.
- **First element:** a search box "מצאו את דירת החלומות שלכם בעזרת AI", then the H1, then cards labelled מבצעי נדל"ן / PRESALE / הטבות מיוחדות / פרויקט / השקעות בחו"ל.
- **Words:** 535. **Cards:** 7 (label, name, a marketing blurb, city, "עוד על הפרויקט"); price inside the blurb: "דירות 5 חדרים החל מ- 2,190,000 ש"ח", "החל מ- 4,980,000 ש"ח". Two dated news items (9.11.2026, 1.11.2026).
- **Foot paragraph:** about 80 words describing the portal (renders, plans, virtual tours, video, map layers, transactions data).
- **Footer links:** פרויקטים חדשים · חברות בנייה · מגזין נדל״ן · התחדשות עירונית · פרויקטים באזור המרכז / השפלה / השרון · פרויקטים במחיר השקה · מדריך לרכישת דירה. Newsletter form "הצטרפו למועדון הנדלניסטים".
- **Schema:** none. **Filters, sort, map, FAQ:** none.
- **First phone screen:** AI search box at 173 px, H1 at 379 px, then a cookie notice.

### 2.10 Madlan Tel Aviv: `madlan.co.il/projects-for-sale/תל-אביב-יפו-ישראל` (read 10:22)
- **Title:** דירות ופרויקטים חדשים בתל אביב יפו | מדלן. **Description:** live count ("ל-174 דירות למכירה... בתל אביב יפו").
- **H1:** דירות ופרויקטים חדשים למכירה בתל אביב יפו. **H2:** 174 דירות ופרויקטים חדשים למכירה · יעניין אותך לדעת... (31 article H3).
- Same card, filters, sort, alert button and schema as 2.1 (ApartmentComplex x25). Extra top link "הכירו את העיר". Words: 1,784.
- **Link blocks:** מידע חשוב (דירות להשכרה, בתי ספר, יזמי נדל"ן, מתווכים בתל אביב יפו) · **דירות לפי מספר חדרים** (דירות 2 / 3 / 4 / 5 חדרים למכירה בתל אביב יפו) · דירות מסוגים שונים (דירות גן, דירות פנטהאוז, דירות גג, קוטג', בית דו משפחתי, **דירות עם ממ״ד**, בית פרטי למכירה בתל אביב יפו) · חיפושים פופולריים נוספים (6 cities).

### 2.11 MyPlace: `myplace.co.il/פרויקטים-חדשים/` (read 10:22, phone frame 10:29)
- **Title:** פרויקטים חדשים בתל אביב | פרויקט מגורים ת״א נכסים שווים ← MyPlace
- **Meta description:** a question ("מחפשים דירה בפרויקטים חדשים בתל אביב?"), range, prices, a call to contact.
- **H1:** פרויקטים חדשים בתל אביב. **H2 (after the list):** פרויקטים חדשים בצפון תל אביב היוקרתי · אזור שוקק חיים ומלא בעושר במרכז תל אביב · דרום תל אביב - אורבניות גולמית לצד איכות חיים קפדנית. **H3:** 12 project slogans.
- **Opening (paraphrased):** about 230 words: buying in a project differs from second hand; four things to check (who the developer is, Sale Law guarantees, the specification, the timetable and permit stage) and how the agency helps.
- **Words:** 657. **Cards:** 12: **permit-stage badge** (התקבל היתר בניה / בהליך רישוי מתקדם / הפרויקט בביצוע / הבניה החלה), slogan, city, area, street, "צפה בפרוייקט". No price, no rooms. Photos about 1.44:1.
- **Filters (exact labels):** סנן תוצאות · טווח מחירים (0 to 20,000,000) · מספר חדרים (1 to 10) · קוד נכס · "מצא לי נכס!".
- **Schema:** WebPage, BreadcrumbList, WebSite. hreflang he, en, fr. A footer link labelled "Hey AI, learn about this page".
- **First phone screen:** "סנן תוצאות", breadcrumb, H1 at 256 px, then the prose. No card.

### 2.12 Ashtrom Megurim: `ashtromegurim.co.il/projects/projects-past` (read 10:23, phone frame 10:30)
- **Title:** דירות חדשות לאכלוס מיידי בפרויקטים מובילים | אשטרום מגורים
- **Meta description:** "מבחר דירות חדשות לאכלוס מיידי...", "דירות 2-5 חדרים, גן או פנטהאוז, עם ממ"ד ובמחירים שונים".
- **H1:** דירות חדשות לאכלוס מיידי: הדירה שלכם כבר מוכנה. **H2:** הפרויקטים שלנו. Breadcrumb label: פרויקטים לאכלוס מידי.
- **Opening (paraphrased, about 60 words):** asks whether you want 4 or 5 rooms, a garden flat or a penthouse; says the company offers flats "עם ממ"ד בנות 2-5 חדרים", all ready to move into.
- **Words:** 241. **Cards:** 8: badge **אכלוס מיידי**, name, developer, track (התחדשות עירונית / מגורים), city, **"23 יח׳ דיור"**. No price, no rooms. Tall photos (about 0.7:1).
- **Filters:** tabs כל הפרויקטים · מגורים · התחדשות עירונית · מסננים. **Order:** Tel Aviv first (5 of 8 are Tel Aviv).
- **Schema:** BreadcrumbList only. hreflang he, en.
- **First phone screen:** H1 at 144 px, the intro at 336 px, "מסננים", the first card photo with its "אכלוס מיידי" badge at 657 px.

### 2.13 Sela Binui: `selabinui.co.il/project/דירות-לדוגמה-למכירה-לאכלוס-מיידי/` (read 10:24, phone frame 10:30)
- **Title:** דירות לדוגמה למכירה | אכלוס מיידי | סלע בינוי. **Meta description:** a generic company line.
- **H1: none.** **H2:** דירות לדוגמה, למכירה לאכלוס מיידי · four project names · צרו קשר.
- **Opening (paraphrased, about 70 words):** a few upgraded sample flats offered for immediate occupancy, then the terms line "שלמו רק 5% עכשיו והיתרה באכלוס, ללא ריבית והצמדה".
- **Words:** 1,278 (most of it long project drop-down lists). Four project sections with slideshows. One price sentence: "דירות 3, 4, 5 חד' החל מ- 1,625,000 ₪". Repeated type wording: "פנטהאוז ומיני פנטהאוז לאכלוס מיידי".
- **Filters:** site project search (קטגוריה, אזור, פרויקט). Lead form. **Schema:** Organization, WebSite, WebPage, Article.
- **First phone screen:** slideshow image, the project search, a privacy notice. No heading.

---

## 3. Our page today: `https://nad-lan.co.il/projects/` (read 10:25, phone frame 10:26, signed in as admin)

- **Title:** פרויקטים חדשים ודירות חדשות למכירה בישראל - מעודכן ל-2026 | נדלן
- **Meta description:** unchanged from 9.11 ("כל הפרויקטים החדשים ודירות מקבלן בישראל בקטלוג אחד..."). It carries no count and no date.
- **H1:** פרויקטים חדשים ודירות חדשות בישראל (one H1).
- **Opening:** a count paragraph (564 on sale now: 57 לאכלוס מיידי, 24 באכלוס קרוב, 52 בבנייה, 392 בשיווק, 39 בפריסייל; "נבדק ב־9.11.2026"), a second paragraph listing what is on the page ("עודכן ב־10.11.2026"), nine jump links, language links.
- **H2 (23), first six:** דירות חדשות לאכלוס מיידי: 57 פרויקטים, ועוד 24 לאכלוס קרוב · פרויקטים חדשים בשיווק: מחירים, חדרים ותנאי תשלום · 1,019 פרויקטים בקטלוג · פרויקטים חדשים בתל אביב: איפה בונים, כמה זה עולה ומה בדרך · מחירי דירות חדשות לפי עיר · פרויקטים חדשים בישראל: מה יש בקטלוג. Then the timeline, payments, seven calculators, checks, market numbers, cities, guides, FAQ, sources. 124 H3.
- **Words:** 6,663 (includes the admin bar). 9 tables. 31 images, 24 of them at 4:3.
- **New section "דירות חדשות לאכלוס מיידי":** label "דירות מוכנות מקבלן · נבדק מול פרסומי היזמים ב־9.11.2026"; tabs הכל 81 · לאכלוס מיידי 57 · אכלוס קרוב 24; filters עיר (30 cities with counts), מחיר (עד 2 / 3 / 4 / 5 מיליון ₪), חדרים (3, 4, 5 ומעלה). **Card fields:** stage badge (מאוכלס / אכלוס מיידי / a delivery text), neighbourhood + city, name, developer, rooms range, "החל מ 1,790,000 ₪ ל־5 חדרים", "מחיר למ"ר ב<עיר> לפי עסקאות: 13,366 ₪", developer terms where published, "נבדק ב־9.11.2026 · פרסום היזם". **Default order:** cheapest first; the first card is in Beer Sheva.
- **Catalog filter (above that section):** tabs הכל · תמ״א 38 (6) · פינוי בינוי (975) · בנייה חדשה (28); עיר by project count (ירושלים 213, תל אביב יפו 87, רמת גן 78...); סטטוס; סוג (building track, not home type); גודל; מיון (מומלצים / הכי הרבה יח"ד / חדש בקטלוג / א׳ עד ת׳); קרוב אליי; map entry "מפת מחירים ופרויקטים" (opens on click).
- **Marketing table:** region buttons with counts (כל הארץ 564, תל אביב 141, גוש דן 135...), שלב, מחיר, sort by price; columns פרויקט · יזם · חדרים · החל מ · תנאי תשלום · שלב (with "מסירה: 01/2030" where known).
- **City price table:** עיר · 3 חדרים · 4 חדרים · 5 חדרים · פרויקט חדש החל מ · בקטלוג.
- **FAQ:** 24 questions (FAQPage schema).
- **Schema:** CollectionPage, WebSite, Organization, BreadcrumbList, ItemList, SoftwareApplication x7, FAQPage. **No ApartmentComplex or RealEstateListing items.**
- **hreflang:** he, en, fr, ru.
- **First phone screen (375 x 812):** logo, breadcrumb, H1 at 165 px, the count paragraph (237 to 396 px), the second paragraph (from 445 px), four jump links at 746 px, language links at 792 px, the floating WhatsApp bar. **No filter, no card, no photo, no price** in the first screen. The document is 58,730 px tall at this width (Madlan 20,062; Yad2 Tel Aviv 9,784; Dimri 9,292).

---

## 4. Price phrasings people search

Sources: (S) Google suggest, `client=chrome&hl=iw&gl=il`, 124 calls on 10.11.2026 at 10:35 UTC; (A) `autocomplete.md`, 9.11.2026; (R) `related.md`, 9.11.2026; (P) "אנשים שאלו גם על" on the head query, 10.11.2026 10:15 UTC.

### By room count
- **מחיר דירת 3 חדרים ב...** (S): תל אביב, רחובות, חריש, באר שבע, הרצליה, פתח תקווה, רמת גן, עפולה, ראשון לציון, מודיעין, אילת, בת ים, אשדוד, כפר סבא, אשקלון. Also "מחיר דירה 3 חדרים בתל אביב", "מחיר דירת 3 חדרים ברמת אביב".
- **מחיר דירת 4 חדרים ב...** (S): נתניה, פתח תקווה, חריש, כפר סבא, רחובות, נתיבות, אשקלון, באר יעקב, רמת גן, באר שבע, מודיעין, ראשון לציון, רעננה, שדרות, חולון. Also "מחיר ממוצע של דירת 4 חדרים בתל אביב", "מחיר ממוצע לדירת 4 חדרים".
- **מחיר דירת 5 חדרים ב...** (S): ראשון לציון, מודיעין, כפר סבא, באר יעקב, פתח תקווה, חריש, רעננה, הוד השרון, רחובות, כרמי גת, גני תקווה, אשקלון, חולון, נתניה, גבעת שמואל.
- **מחיר דירת 2 חדרים ב...** (S): תל אביב, רמת גן, פתח תקווה, בת ים, **שדה דב**, באר שבע, חיפה; "דירת 2 חדרים בירושלים מחיר".
- **כמה עולה דירת 3 / 4 / 5 חדרים ב...** (S): 15 cities each (4 rooms: תל אביב, מודיעין, כפר סבא, באר שבע, חריש, ראשון לציון, פתח תקווה, רמת גן, כרמי גת, ירושלים, רחובות, כרמיאל, רעננה, אשקלון, גבעתיים).
- **With "חדשה"** (S): כמה עולה דירת 4 חדרים חדשה ב (נתיבות, פתח תקווה, כפר סבא, גבעתיים, אופקים, באר שבע, ראשון לציון, אשקלון, חדרה) · כמה עולה דירת 3 חדרים חדשה ב (כפר סבא, פתח תקווה, רמת גן, תל אביב, ראשון לציון) · כמה עולה דירת 5 חדרים חדשה ב (נתיבות, רעננה) · מחיר דירת 4 חדרים חדשה ברעננה · דירת 4 חדרים חדשה ב (רחובות, ראשון לציון, פתח תקווה, באר שבע, חולון, רמת גן, בת ים, תל אביב, חדרה) · דירת 3 חדרים חדשה ב (12 cities) · דירת 3 חדרים חדשה מקבלן · דירת 5 חדרים חדשה מקבלן · דירת 4 חדרים על הנייר.
- **Plural list forms** (S, A, R): דירות חדשות 3 / 4 / 5 חדרים ב<עיר> · דירות חדשות למכירה ב<עיר> 4 חדרים · דירות 3 חדרים מקבלן ב (מודיעין, פתח תקווה, ראשון לציון) · פרויקטים חדשים ב (נתניה, פתח תקווה, ראשון לציון) 3 חדרים · דירות חדשות בתל אביב 3 חדרים / 2 חדרים.
- **Dead forms** (S, no suggestions): "דירת 3 חדרים חדשה מחיר", "דירת 5 חדרים חדשה מחיר", "דירה חדשה 4 חדרים מחיר". People put the price word **first** ("מחיר דירת...", "כמה עולה דירת...") or add only the city.

### By apartment type
- **פנטהאוז** (S): כמה עולה פנטהאוז ב (תל אביב, ראשון לציון, אשקלון, פתח תקווה, באר שבע, הרצליה, נתניה, ראש העין, רמת גן, באר יעקב, אופקים, רעננה, חיפה) · פנטהאוז בתל אביב מחיר · מחיר פנטהאוז ב (ראשון לציון, אשדוד, הרצליה, בת ים, רמת גן, חיפה) · פנטהאוז חדש מקבלן · פנטהאוז חדש למכירה (ברעננה, בפתח תקווה, בראשון לציון, במודיעין, ברחובות) · פנטהאוז מקבלן אשדוד · פנטהאוז מחיר למשתכן. "פנטהאוז חדש מחיר": no suggestions.
- **מיני פנטהאוז** (S): מיני פנטהאוז למכירה (ברחובות, ברעננה, בראשון לציון) · מיני פנטהאוז 4 חדרים / 3 חדרים · מיני פנטהאוז או פנטהאוז. "מיני פנטהאוז מחיר", "מיני פנטהאוז מקבלן", "כמה עולה מיני פנטהאוז": no suggestions.
- **דירת גן** (S, A): דירת גן מקבלן (אשקלון) · דירת גן חדשה מקבלן · דירת גן חדשה למכירה · דירות גן מקבלן (באילת, בראש העין) · דירת גן על הנייר · דירת גן מחיר · מחיר דירת גן 5 חדרים במודיעין · מחיר דירת גן בחריש · כמה עולה דירת גן במודיעין / בגבעתיים · דירות גן חדשות (בקרית אתא, באשקלון, בירושלים) · דירת גן מחיר למשתכן. "דירת גן מקבלן מחיר", "דירת גן חדשה מחיר": no suggestions.
- **דופלקס** (S): דופלקס למכירה ב (רמת גן, ראשון לציון, פתח תקווה, תל אביב, אשדוד and more) · דופלקס חדש · כמה עולה דופלקס. "דופלקס מחיר" is polluted by a medicine of the same name.
- **Other types** (A): דירות סטודיו חדשות · צמודי קרקע · וילות · דו משפחתי · קוטג'ים · בתים פרטיים.

### By city (new flat, price word)
- **כמה עולה דירה חדשה ב...** (S): אשקלון, באר שבע, אופקים, נתיבות, שדרות, דימונה, עפולה, אילת, קרית גת, נתניה, ירושלים, תל אביב, בת ים, עמנואל, ירוחם. The south and the periphery come before Tel Aviv.
- **מחיר דירה חדשה ב...** (S): אילת, קרית גת, נתיבות, חיפה, עפולה, אופקים, אשקלון, באר שבע, חדרה, רחובות, שדרות, עכו, פתח תקווה, כפר סבא, רעננה.
- **דירה חדשה ב<עיר> מחיר** (S): אילת, אופקים, דימונה, נתיבות, אשקלון, שדרות, חדרה, חיפה, חולון, באר שבע, בת ים, רמת גן; with "מחירים": נהריה, עפולה, נתניה.
- **מחירי דירות חדשות ב...** (S, A): נהריה, נתיבות, אשקלון, אופקים, בת ים, אילת, אשדוד, פתח תקווה, עפולה, נתניה, חדרה, קרית גת, ירושלים, עכו, שדרות.
- **דירות חדשות ב<עיר> מחירים** (S): שדרות, חיפה, דימונה, נתיבות, הרצליה, רעננה, אשדוד, מודיעין, טבריה, נתניה, קרית אונו, באר שבע, קרית אתא, באר יעקב, ראשון לציון.
- **פרויקטים חדשים ב<עיר> מחירים** (S): נתיבות, חיפה, אופקים, אשקלון, גדרה, מודיעין, חולון, תל אביב, מזכרת בתיה, גן יבנה, בני עייש, באר יעקב, קרית גת, באר שבע.
- **Tel Aviv** (S): מחיר דירה חדשה בתל אביב · כמה עולה דירה חדשה בתל אביב · מחיר למטר דירה חדשה בתל אביב · כמה עולה מטר דירה בתל אביב · כמה עולה דירה במגדל בתל אביב · כמה עולה דירה על הים בתל אביב · פרויקטים חדשים בתל אביב מחירים (R, 8 result pages).
- **Generic** (S): כמה עולה דירה חדשה מקבלן · כמה עולה דירה בפרויקט · כמה עולה דירה על הנייר · דירה מקבלן מחיר · דירה חדשה מקבלן מחיר · מחיר למטר דירה חדשה · מחירון דירות חדשות (בראשון לציון, באילת). Budget forms (A, R): עד 1.2 מיליון, עד 1.5, עד 2 מיליון, עד מיליון שקל, עד מיליון וחצי.

### By feature (ממ"ד, מרפסת, חניה, מעלית)
- (S) "דירה עם ממד" and "דירות עם ממד" exist, but their suggestions are rentals and short stays (להשכרה, לטווח קצר, airbnb, סאבלט) plus cities; sale form: "דירות למכירה בחיפה עם ממד".
- (S) **No suggestions at all** for: "דירה חדשה עם ממ"ד", "דירות חדשות עם ממד", "דירה חדשה ממד", "דירה חדשה עם מרפסת", "דירות חדשות עם מרפסת שמש", "דירה חדשה עם חניה", "דירות חדשות עם חניה", "דירה מקבלן עם חניה", "דירה חדשה עם מעלית". "דירה חדשה עם ממד מחיר" falls back to "דירה חדשה מקבלן מחיר", "דירה חדשה עד מיליון שקל".
- (S) מרפסת: "דירה 3 חדרים עם מרפסת", "דירות למכירה עם מרפסת", the rest are rentals. חניה: "דירה עם חניה בתל אביב". מעלית: only rentals.
- Where the feature words do appear on page one: Ashtrom's description and intro ("דירות עם ממ"ד בנות 2-5 חדרים"), Madlan's link "דירות עם ממ״ד למכירה בתל אביב יפו", Sela's text ("2 חניות מקורות צמודות", "מרפסת שירות"). They work as copy and as filters, not as searched headings in this family.

### Price questions Google itself shows (P)
מה המחיר של פריסייל? · מה המחיר של יחידות דיור מוכנות? · מהם המחירים של פרויקטים חדשים בתל אביב? · מה המחיר למטר רבוע של דירה? · איפה הכי זול לקנות דירה בישראל? · איפה אפשר למצוא דירות למכירה עד מיליון ש"ח? · איפה אפשר למצוא דירות חדשות במחיר עד 1.5 מיליון שקל? · איפה אפשר למצוא דירות להשקעה עד 800 אלף שקל בישראל? · מהו גרף מחירי הדירות בישראל? · מהו מחשבון שווי דירה?
The other five in the block: איפה אפשר למצוא דירות מוכנות למכירה? · אילו פרויקטים חדשים בישראל זמינים עד 2 מיליון שקל? · איפה אפשר למצוא דירות למכירה בישראל? · מהו פרויקט תדהר בתל אביב? · האם יש דירות גן למכירה ב-יד 2?
Sources Google attached to the first four (opened): ready flats: ashtromegurim, dimri, last-one.co.il · up to 2 million: tdn.co.il, dimri, madlan · presale price: globes, socity `/דירות-פריסייל/`, captaininvest.co.il · flats for sale: madlan, yad2, homeless. Two of the questions are near copies of questions in our FAQ ("איפה אפשר למצוא דירות מוכנות למכירה, באכלוס מיידי?", "אילו פרויקטים חדשים יש עד 2 מיליון שקל?"); nad-lan is not among the attached sources.

### Price sentence patterns on page one (exact wording)
| Pattern | Where |
|---|---|
| "החל מ- 3,299,000 ₪" | Yad2 cards |
| "5 חד' החל מ- 3,990,000 ₪" · "3 חד' החל מ- 5,600,000 ₪" · "4 חד' החל מ- 2,390,000 ₪" | promo line on Yad2 and Madlan cards |
| "החל מ - 3,300,000 ₪" after "דירות 3 חד׳12 קומות" | Madlan cards |
| "החל מ־39,000 ₪ למ"ר" | one Yad2 card |
| "החל מ 2,175,000" | Dimri cards |
| "דירות 5 חדרים החל מ- 2,190,000 ש"ח" | nadlan.com blurb |
| "דירות 3, 4, 5 חד' החל מ- 1,625,000 ₪" | Sela Binui |
| "...נעים בטווח שבין 35,000 ש"ח למ"ר ל- 100,000 ש"ח למ"ר" | Socity |
| "החל מ-365,000 ₪ בחתימה" · "350,000₪ עכשיו, השאר באכלוס" · "427 אלף ש"ח והיתרה באכלוס" | payment-at-signing lines, Madlan and Yad2 |
| Ours: "החל מ 1,790,000 ₪ ל־5 חדרים" | price first, rooms after; the leaders put the rooms first ("5 חד' החל מ-") |

---

## 5. What the AI engines answer (10.11.2026)

### Google AI box ("תקציר מ-AI") on the result page
| Query | Structure of the answer | Sources shown |
|---|---|---|
| פרויקטים חדשים (10:14) | One line: follow new projects through Yad2 and Madlan. Then "פרויקטים בולטים וחברות מובילות בשיווק": a bullet per developer (Aura, Tidhar, Dimri, Ashtrom Megurim, Gabay) with its cities and named projects, one bullet for the north via Yad2. Ends with two questions: which area or city; living, investment or renewal. No price. | tidhar for-sale · yad2 `/yad1` · madlan ישראל · auraisrael · dimri `/projects` · ashtromegurim marketing page · gabaygroup · yad2 north |
| דירות חדשות (10:16) | Market opening (renewal, financing deals such as 10/90, big plans), then "דוגמאות לפרויקטים חדשים ואזורי ביקוש בולטים (נובמבר 2026)" by region with dated news (2,500 flats in Givatayim, 138 flats in Jerusalem) and one price ("החל מ-3,215,000 ₪"). Points to Yad2 and nadlan.com. Asks area, budget and rooms, on paper or ready. | nadlan.com · yad2 Tel Aviv · dimri · ashtromegurim ready flats · ynet · maariv (two items) · digg.co.il · ice · bizportal · a Facebook video |
| דירות מקבלן (10:16) | A buyer guide, not a list: what buying from a developer means, legal checks (contractor registry, land rights, permit, own lawyer), guarantees under the Sale Law, payments and index (20% not indexed, 20/80), handover and defects period. Ends by pointing to the ministry guide, Yad2 and Dimri. | prlaw.co.il · nadlanmaster `/דירות-חדשות-למכירה/` · gov.il buyer guide · elkayamlaw · midrag · yad2 `/yad1` · dimri · drlawfirm · shpak-law |
| פרויקטים חדשים בתל אביב (10:16) | "פרויקטים בולטים בשיווק ובבנייה": Duo Tel Aviv, Sde Dov (Yama, First, VOGUE), YAPI, Gallipolis, TRUE TLV, boutique buildings; then "אזורי התחדשות עירונית מרכזיים בעיר" from the municipality; points to Madlan; asks budget, area of the city, living or investment. | socity · tel-aviv.gov.il · madlan Tel Aviv · yad2 Tel Aviv · hagag · tidhar Tel Aviv · three Facebook videos |
| דירות חדשות לאכלוס מיידי (10:17) | A list of platforms (Yad2 filter, Yad1 centre and Sharon, nadlan.com, Sela Binui, Last One), then "דוגמאות לפרויקטים ואזורים בולטים" by region with price floors ("החל מ-3.19 מיליון ש"ח", "החל מ-1.62 מיליון ש"ח", "החל מ-2 מיליון ש"ח"). Asks area, rooms, budget. | yad2 Tel Aviv · yad2 centre and Sharon · nadlan.com · selabinui · last-one.co.il · ashtromegurim · nadlanmaster `/דירות-לכניסה-מיידית/` · **nad-lan.co.il `/new-projects/new-projects-tel-aviv/`** · madlan Tel Aviv · dimri · diur-plus |

### Google AI Mode ("מצב AI"), reached from the same result page
| Query | Structure | Sources linked |
|---|---|---|
| פרויקטים חדשים (10:30) | Opening on hundreds of projects and renewal; "פרויקטים בולטים לפי אזורים (עדכון 2026)" (Tel Aviv with a price range of about 2.6 to over 6 million, centre and Sharon, south and Shfela "לרוב החל מכ-2 מיליון ש"ח"); "לוחות לחיפוש והשוואת פרויקטים" (Yad1, Madlan, nadlan.com); "חברות יזמיות מובילות בשיווק" (Tidhar, Dimri, Gabay); asks city, rooms, budget. | madlan ישראל · yad2 Tel Aviv · nadlan.com · dimri · yad2 `/yad1` · tidhar · gabaygroup · socity · yeshnadlan |
| דירות חדשות (10:31) | "תמונת מצב ומחירים לפי אזורים" (Tel Aviv 2.6 to 3.3 million in the south of the city, 5 to 8 million in the north; Petah Tikva 4 rooms from about 2.45 million; Jerusalem and Beit Shemesh tenders; south from 2 million); "איפה כדאי לחפש פרויקטים חדשים?" (portals, developer sites, government lotteries); asks area, budget, rooms, ready or on paper. | nadlan.com · yad2 Tel Aviv · ashtromegurim · ynet · dimri · emess.co.il · nadlanmaster Tel Aviv · maariv · news08.net |
| דירות מקבלן (10:31) | Why buy new; "איפה מחפשים פרויקטים חדשים?" (portals, Tel Aviv on Madlan, direct from developers); "דגשים חשובים לפני חתימה על חוזה" (guarantees, index, extra costs, own lawyer); asks city, rooms, budget and wanted occupancy date. | madlan ישראל · dimri · yad2 `/yad1` · nadlan.com · madlan Tel Aviv · tidhar home · peretzbh · yad2 Tel Aviv |
| פרויקטים חדשים בתל אביב (10:32) | Opening with the 35,000 to 100,000 ₪ per m² range and starting prices by part of the city; **a map** with two area chips (צפון העיר ושדה דב · דרום, מזרח ויפו); "פרויקטים בולטים לפי אזורים בעיר" in four areas with named projects and "החל מ" prices; "מאפיינים עיקריים של השוק ב-2026"; asks budget and rooms, area, living or investment. | socity · tel-aviv.gov.il · madlan Tel Aviv · yad2 Tel Aviv · tidhar Tel Aviv · ken-hator · etzhashaked · two Facebook videos |
| דירות חדשות לאכלוס מיידי (10:32) | "יתרונות ודגשים ברכישת דירה מוכנה" (saves rent and index, see the finished flat, flexible terms, check Form 4 and registration); "פרויקטים בולטים ולוחות חיפוש מובילים" (Yad1 filter and "מדריך הפרויקטים של אתר נדל"ן", Ashtrom, Sela, other cities); asks city, rooms or budget. | selabinui · ashtromegurim · yad2 Tel Aviv · **nad-lan.co.il `/new-projects/new-projects-tel-aviv/`** · nadlan.com · e-eyal.co.il |

### Perplexity (perplexity.ai, no sign-in)
- **"פרויקטים חדשים בתל אביב" (10:33):** a short opening, then a **table** "פרויקטים בולטים" with columns פרויקט · אזור · מה מתוכנן (seven rows built from news: permits, number of flats, floors), then "אזורים מרכזיים" (four areas), then "מה כדאי לבדוק" (tell a permitted project from a planned one), then follow-up questions (for example "מה המחירים הממוצעים בפרויקטים חדשים", "אילו פרויקטים יש ברובע 4"). No prices. **19 sources:** ynet (2) · mako (3) · tidhar project pages (2) · nadlancenter.co.il (2) · madlan Tel Aviv · hagag · project-tlv.info · immobilier.co.il · yad2 Tel Aviv · maariv · globes · inn.co.il · prtfl.co.il · magdilim.co.il. nad-lan is not among them.
- **"דירות חדשות לאכלוס מיידי" (10:34):** a definition, then a **table** "דוגמאות פעילות" with columns אזור · פרויקט · מה מוצע · **מחיר החל מ** (seven rows, six with a price, almost all taken from Yad2), then "מה לבדוק לפני רכישה" (exact delivery date and Form 4, state of the flat, extra costs, faster payment schedule, price per m² against similar deals), then "איפה לחפש". **10 sources:** yad2 `/yad1/projectsale` · yad2 Tel Aviv · ashtromegurim ready flats · mako · last-one.co.il · nadlanmaster `/דירות-לכניסה-מיידית/` · yad2 centre and Sharon · yad2 second-hand Tel Aviv · nadlan.com · yad2 second-hand centre. nad-lan is not among them. After this answer Perplexity showed a sign-up panel; nothing was signed.

### What the AI answers have in common
1. Every Google answer ends with questions back to the searcher. Across the ten answers (five boxes, five AI Mode): **area or city on 10, budget on 8, rooms on 7**, living or investment on 3, ready or on paper on 2. Both Perplexity answers end by offering to narrow by city, budget and rooms.
2. The unit of the answer is **project name + area + "החל מ" price**, or **developer + cities**. Pages that print those three things as plain text per row get quoted (Yad2 cards, Dimri cards, nadlan.com blurbs).
3. Both AI layers of Google cite our Tel Aviv immediate-occupancy URL; neither cites `/projects/` on any of the five queries. Perplexity cites nad-lan on neither query.

---

## 6. Gap matrix

Columns: how many of the 13 page-one pages have the element, and whether `https://nad-lan.co.il/projects/` has it today (read 10:25). "Template" marks a phone measure taken on one page of a site and counted for its sibling pages too (Madlan x2, Yad2 list x2, Tidhar x2).

### Title, H1, opening
| Element | Of 13 | Ours |
|---|---|---|
| Title carries "פרויקטים" | 12 | yes |
| Title carries "חדשים" or "חדשות" | 11 | yes |
| Title carries "דירות" | 9 | yes |
| Title carries both "פרויקטים" and "דירות חדשות / חדשים" | 8 | yes |
| Place in title (בישראל / בתל אביב / והסביבה) | 8 | yes (בישראל) |
| "2026" or "מעודכן ל-2026" in title | 3 | yes |
| "מקבלן" or "קבלן" in title | 1 (nadlan.com) | no (it is in our description and first paragraph) |
| A real H1 | 11 (Socity and Sela have none) | yes |
| Live count in the H1 or in the first H2 | 3 (Madlan x2, Yad2 immediate) | partly: count is in the first paragraph and in a section H2, not in the H1 |
| Live count in the meta description | 2 (Madlan x2) | **no** |
| Paragraph of 40+ words under the H1 | 2 (MyPlace, Ashtrom) | yes (two paragraphs) |
| List starts directly under the H1, nothing in between | 9 | **no** |
| Page under 1,000 words | 8 (median about 950) | no (6,663) |

### List and cards
| Element | Of 13 | Ours |
|---|---|---|
| Project cards are the main content | 12 | partly (cards, then long guide) |
| Photo on every card | 12 | yes |
| One fixed photo ratio across the list | 5 (Yad2 list 3:2, Dimri 4:3, MyPlace, Ashtrom, Tidhar tall) | yes (4:3) |
| Project name | 12 | yes |
| City | 12 | yes |
| Street-level address (street + neighbourhood + city) | 6 | **partly** (neighbourhood + city, no street) |
| Rooms range | 6 | yes |
| "החל מ" price on the card | 8 | yes |
| Room-specific price line ("5 חד' החל מ-...") | 4 (Madlan Israel, Yad2 Tel Aviv, nadlan.com, Sela) | yes, other word order |
| Floors | 5 | **not on the new cards** |
| Size range in m² | 3 (Yad2) | **no** |
| Price per m² on the card | 1 (one Yad2 card) | yes (city deals) |
| Developer's own terms line | 6 | yes |
| Status or deal badge | 9 | yes (stage); **no deal badge** |
| "אכלוס קרוב" / "אכלוס מיידי" badge | 3 (Yad2 list x2, Ashtrom) | yes |
| "במבצע" badge | 4 (Yad2 x2, Madlan x2) | **no** |
| "3D" badge | 3 (Yad2) | **no** |
| Permit-stage badge (התקבל היתר בניה...) | 1 (MyPlace) | no |
| Number of flats in the project | 3 (Ashtrom, Madlan nearby block x2) | on catalog cards only |
| Developer name as a field | 1 (Ashtrom) | yes |
| Delivery date as a field | 0 | yes where published |
| Check date per card | 0 | yes |

### Filters, sort, map
| Element (exact labels seen) | Of 13 | Ours |
|---|---|---|
| Any filter | 11 | yes |
| מחיר / טווח מחיר / טווח מחירים | 8 | yes |
| חדרים / מספר חדרים (or rooms inside "סוג נכס") | 8 | yes |
| **A "סוג נכס / סוג הנכס" filter** (options read on Dimri and Tidhar x2: דירת גן, פנטהאוז, מיני פנטהאוז, דופלקס beside room counts; the option lists of Madlan and Yad2 were not opened) | 7 by label, 3 with options verified | **no** (our "סוג" is the building track) |
| City or area picker | 9 | yes |
| Free search field (address, neighbourhood, project, company) | 5 | yes |
| "אכלוס קרוב" toggle or "אכלוס מיידי" filter | 3 | yes |
| "סיורי 3D" filter | 2 | **no** |
| "יצירת התראה" button | 2 (Madlan) | **no** |
| Seller tabs פרויקט חדש / תיווך / פרטי | 2 (Madlan) | no |
| Sort control | 2 (Madlan "מיון לפי: רלוונטיות") | yes |
| Map or map button | 6 (Madlan x2, Yad2 x3, Tidhar "להצגת המפה") | yes (opens on click) |
| Paging with page numbers | 4 | "הצגת עוד" buttons |

### Sections, tables, FAQ, links
| Element | Of 13 | Ours |
|---|---|---|
| Deals entry ("פרויקטים במבצע" in the nav, "מבצעי נדל"ן", "פרויקטים במחיר השקה") | 4 | **no** |
| Nearby or more-projects block ("פרויקטים נוספים באזור זה", "פרויקטים חדשים בסביבה") | 4 | partly ("קרוב אליי") |
| Articles block | 4 | yes |
| Developer directory with project counts | 1 (Yad2 `/yad1`); AI answers are built per developer on 2 of 5 queries | **no** |
| Foot paragraph of 70 to 300 words | 5 | yes (far more) |
| Price table | 1 (Socity, by quarter, with a rent column) | yes (city by rooms; no rent column) |
| Price range sentence per m² | 1 (Socity) | not as one sentence for the country or a city |
| FAQ | 1 (Socity, 10 questions) | yes (24) |
| On-page lead form or newsletter | 6 (Socity, nadlan.com, MyPlace, Sela, Tidhar x2) | no (WhatsApp bar) |
| Links by district or region | 6 | yes |
| Links by city | 5 | yes |
| **Links by room count** ("דירות חדשות 4 חדרים ב...", "דירות 4 חדרים למכירה ב...") | 3 (Yad2 x2, Madlan Tel Aviv) | **no** |
| **Links by home type** (דירות גן, פנטהאוז, דופלקס, בתים על הים, קרקעות) | 5 | **no** |
| "עמודים פופולריים" block | 2 (Yad2) | no |
| Link to a value calculator | 2 (Yad2) | yes (own calculators) |
| Abroad entry (נדל״ן חו״ל, השקעות בחו"ל) | 4 | no (parked by the owner) |
| More than one language | 4 | yes (4 languages) |

### Schema
| Type | Of 13 | Ours |
|---|---|---|
| BreadcrumbList | 8 | yes |
| ItemList | 4 | yes |
| **ApartmentComplex per card (with PostalAddress on Madlan)** | 4 (Madlan x2, Yad2 x2) | **no** |
| **RealEstateListing per card** | 2 (Yad2) | **no** |
| Organization or WebSite | 5 | yes |
| CollectionPage | 1 | yes |
| FAQPage | 0 | yes |
| No JSON-LD at all | 3 (Yad2 `/yad1`, Dimri, nadlan.com) | n/a |

### First phone screen (375 x 812)
| Element | Count | Ours |
|---|---|---|
| H1 inside the first screen | 7 of 9 measured (Socity and Sela have no H1) | yes (165 px) |
| H1 within the first 170 px | 4 of 9 measured (Madlan 160, Yad2 139, Dimri 167, Ashtrom 144) | yes |
| **A project card with its photo inside the first screen** | 7 of 13 by template (Madlan x2, Yad2 list x2, Dimri, Socity, Ashtrom) | **no** |
| **A price inside the first screen** | 4 of 13 by template (Madlan x2, Yad2 list x2) | **no** |
| A filter or search control inside the first screen | 6 of 13 by template (Madlan x2, Tidhar, MyPlace, nadlan.com, Sela) | **no** |
| Floating "מפה" button | 4 of 13 by template (Madlan x2, Yad2 list x2) | no (floating WhatsApp bar) |
| Result count inside the first screen | 2 (Madlan "422 תוצאות") | yes (in the paragraph) |
| Cookie notice covering part of the screen | 5 of 9 measured | no |

---

## 7. Closing lists

### (a) The 20 most common page-one elements we lack, by how many of the 13 have them
| # | Element | Of 13 |
|---|---|---|
| 1 | The list starts directly under the H1, with no paragraph before the first card | 9 |
| 2 | A page under 1,000 words (ours is 6,663) | 8 |
| 3 | A project card with its photo inside the first phone screen | 7 (template) |
| 4 | A "סוג נכס" filter (home types דירת גן, פנטהאוז, מיני פנטהאוז, דופלקס verified on 3) | 7 by label |
| 5 | Street-level address on the card | 6 |
| 6 | A filter or search control inside the first phone screen | 6 (template) |
| 7 | On-page lead form or newsletter box | 6 |
| 8 | Link block by home type (דירות גן, פנטהאוז, דופלקס, בתים על הים) | 5 |
| 9 | Floors on the card | 5 |
| 10 | A price inside the first phone screen | 4 (template) |
| 11 | Typed schema per card: ApartmentComplex (Yad2 adds RealEstateListing) | 4 |
| 12 | "במבצע" badge on cards | 4 |
| 13 | A deals entry point ("פרויקטים במבצע") | 4 |
| 14 | Floating "מפה" button on the phone | 4 (template) |
| 15 | Link block by room count ("דירות חדשות 3 / 4 / 5 חדרים ב...") | 3 |
| 16 | Size range in m² on the card | 3 |
| 17 | "3D" badge on cards and a "סיורי 3D" filter | 3 |
| 18 | Live count inside the H1 or the first H2 itself | 3 |
| 19 | Live count in the meta description; "יצירת התראה" button beside the filters | 2 each |
| 20 | Developer directory with project counts | 1 on page one, but it is how Google's AI box and AI Mode organise the head-query answer |

Not lacking, and rare on page one: FAQ (1 of 13) and FAQPage schema (0), an intro paragraph (2), a price table (1), calculators (0), a check date per card (0), deal prices beside the developer's price (0), four languages (0 with four).

### (b) Wordings that recur in titles and H1 across the 13 pages
For Socity and Sela (no H1) the opening H2 is counted in the H1 column.

| Word or phrase | In titles | In H1 |
|---|---|---|
| פרויקטים (also spelled פרוייקטים by Tidhar) | 12 | 11 |
| חדשים / חדשות | 11 | 10 |
| דירות | 9 | 8 |
| בתל אביב (+ יפו, + והסביבה) | 6 | 6 |
| "פרויקטים חדשים" as one phrase | 5 | 4 |
| "דירות חדשות" as one phrase (including "ודירות חדשות") | 5 | 5 |
| "פרויקטים ודירות חדשות" (Yad2's order) | 3 | 3 |
| "דירות ופרויקטים חדשים" (Madlan's order) | 2 | 2 |
| למכירה | 2 | 3 |
| לאכלוס מיידי / לאכלוס קרוב / אכלוס מיידי | 3 | 3 |
| מעודכן ל-2026 / 2026 | 3 | 0 |
| למגורים / מגורים | 3 | 1 |
| בשיווק | 2 | 2 |
| בישראל / בכל הארץ | 2 | 2 |
| מקבלן / קבלן | 1 | 0 |
| מחירים (במחירים מיוחדים) | 1 | 0 |
| a number (count) | 0 in the page title, 1 in Google's printed title | 1 |

Recurring H2 wordings: "N דירות ופרויקטים חדשים למכירה" (Madlan x2) · "פרויקטים נוספים באזור זה" (Yad2 x2) · "דירות חדשות, פרויקטים חדשים, דירות מקבלן" (Yad2 x2, the only place the three head phrases sit in one heading) · "מצאו את המקום שלכם ב<אזור>" (Yad2 x2) · "פרויקטים מומלצים" · "חברות בנייה ויזמות נדל"ן נבחרות" · "פרויקטים בתלת מימד" · "הפרויקטים שלנו" · "פרויקטים חדשים בסביבה" (Madlan block label) · Socity's question-shaped set ("איפה יש פרויקטים חדשים בתל אביב", "יתרונות וחסרונות של...", "פרויקטים בשיווק ב... - פרויקטים בולטים", "מדוע לרכוש דירה חדשה ב...") and its H3 "פרויקטים חדשים בתל אביב מחירים".
Observation: the two portals join the two head nouns with "ו" in one phrase and never write "מקבלן" in a title or H1. Our title and H1 already follow the joined form.

### (c) Which city or area the leaders open on, and how they order cities
| Page | Default list opens on | City or region order |
|---|---|---|
| Yad2 (the URL Google ranks for the generic queries דירות חדשות and דירות מקבלן, and first for Tel Aviv) | **Tel Aviv and surroundings** (תל אביב, רמת גן, גבעתיים, בת ים, חולון). No sort control; the order rotates between loads and "במבצע" cards lead | Districts: מרכז והשרון · דרום · תל אביב והסביבה · מישור החוף הצפוני · ירושלים והסביבה · צפון והעמקים. Areas: תל אביב יפו · רמת גן וגבעתיים · חולון ובת ים. City links: חיפה, תל אביב יפו, ראשון לציון, מודיעין, פתח תקוה, אשדוד, חולון, רמת גן, באר שבע, ירושלים, חדרה, הרצליה, אשקלון |
| Yad2 `/yad1` | The whole country, promoted: "יזם החודש", then a national mix; reopened on Tel Aviv on a later visit | same district order |
| Madlan Israel | The whole country, "מיון לפי: רלוונטיות"; in this browser 5 of the first 6 cards are Tel Aviv | Cities: תל אביב יפו · רמת גן · רעננה · חיפה · ירושלים · באר שבע. Regions: מרכז · גוש דן · צפון · שפלה · דרום |
| Dimri | All 19 projects; three featured (נתניה, אור יהודה, נתיבות), then alphabetical | Region tabs: שפלה · מרכז · דרום · צפון |
| Tidhar | All cities; Tel Aviv projects first | City list alphabetical: אשדוד, בת ים, גבעת שמואל, הרצליה, לוד, תל אביב |
| nadlan.com | Deals first, by advertiser: אשקלון, רחובות, רמת השרון, קרית אונו, אבן יהודה | Footer: המרכז · השפלה · השרון |
| Ashtrom | Tel Aviv first (5 of 8), then Herzliya and Netanya | none |
| Socity, MyPlace, Tidhar Tel Aviv, Madlan Tel Aviv, Yad2 immediate | Tel Aviv only | MyPlace text order: north, centre, south of the city |
| **Ours** | The catalog filter, then the immediate-occupancy cards sorted **cheapest first** (first card: Beer Sheva) | City picker by project count: ירושלים (213), תל אביב יפו (87), רמת גן (78), חיפה (47)... Region buttons: כל הארץ · תל אביב · גוש דן · מרכז ושפלה · השרון · דרום · חיפה והצפון · ירושלים והסביבה |

Summary of (c): 9 of the 13 pages show Tel Aviv projects first (six are Tel Aviv pages, among them the Yad2 URL that Google ranks for the generic queries; Tidhar and Ashtrom lead with their Tel Aviv projects; Madlan's relevance order puts Tel Aviv on top in this browser). The other four (Yad2 `/yad1`, Dimri, nadlan.com, Sela) open on promoted or featured projects from several cities. None of the 13 orders by price by default, and none leads with Jerusalem. Where a region list exists, the centre comes first on 3 of 4 (Madlan, Yad2, nadlan.com); Dimri starts with the Shfela.

---

## 8. Limits of this read
- One browser, one location (Tel Aviv area), one day. Google's order and its AI box changed between 9.11 and 10.11, so both should be treated as moving.
- Phone screens were measured in a 375 px frame with a desktop user agent, not on a phone.
- Card counts on Madlan and Yad2 `/yad1` are approximate (lazy loading); schema counts are exact.
- Photo type was not judged. AI answers are quoted by structure only; their facts were not checked.
