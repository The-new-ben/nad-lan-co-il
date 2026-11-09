# Competitors, one by one (read 9.11.2026 in the owner's Chrome)

Evidence class: **code** (page text and DOM read through the browser tools; no screenshots taken, so photo quality is judged only from DOM data where stated).
Pages read: Madlan national projects, Yad2 Tel Aviv projects, Yad2 deals hub, the government "דירה בהנחה" site, Ashtrom Megurim (home and marketing page), nadlan.com, Socity Tel Aviv. Homeless: its new-projects URL is gone (404) and it appears on none of the 27 result pages.

---

## 1. Madlan: `madlan.co.il/projects-for-sale/ישראל`
Ranks top 3 on 24 of 27 result pages. Title "דירות ופרויקטים חדשים בישראל | מדלן".

- **Opening:** H1 "דירות ופרויקטים חדשים למכירה בכל הארץ", then H2 "427 דירות ופרויקטים חדשים למכירה". No text paragraph: the count is the answer.
- **Headings:** H1, one H2 with the count, "הכתבות הנצפות ביותר" (about 40 research articles, several sponsored by developers), "פרויקטים חדשים בסביבה".
- **Filters and sort:** מחיר · חדרים · סוג נכס · מסננים נוספים · tabs פרויקט חדש / תיווך / פרטי · "מיון לפי: רלוונטיות" · pagination of 9 pages.
- **Alerts:** "יצירת התראה" button right next to the filters.
- **Card fields:** promo line on top (the badge), project name, "דירות 6-3 חד׳", floors, street and neighbourhood and city, "החל מ ₪" (on about half), developer promo text.
- **Badges seen (verbatim types):** "פרויקט במבצע!", "שלמו 10% - היתרה באכלוס!", "1.99% ריבית קבועה-15 שנה", "פטור מהצמדה למדד", "PRESALE 85%|15%", "מחירי פריסייל מיוחדים!", "אכלוס דצמבר 2026 !", "הטבות לרגל האכלוס !", "משלמים בעוד שנה וחצי!", "150,000 ש"ח לעיצוב הבית*", "תנאי מימון 10/90 !", "דירות אחרונות!", "אירוע מכירות מיוחד 6/11". Deals are free text written by the developer; nothing is normalised or valued.
- **Nearby module:** "פרויקטים חדשים בסביבה": price from, number of buildings, rooms, floors, **number of units**, address.
- **Footer hub links:** new flats by city (תל אביב, רמת גן, רעננה, חיפה, ירושלים, באר שבע), by region (מרכז, גוש דן, צפון, שפלה, דרום), by type (דירות גן, בתים פרטיים, פנטהאוז, דופלקס, דו משפחתי), developers index.
- **Schema:** no usable JSON-LD type found in the DOM. **Languages:** Hebrew only.
- **No price per m² on cards, no occupancy filter, no map in the page text** (Madlan's map mode exists in its app; not checked here).
- **Best at:** the count-as-answer opening, the alert button beside the filters, and breadth (427 national listings plus brokers and private sellers in one place).

## 2. Yad2 (Yad1): `yad2.co.il/yad1/newprojects/tel-aviv-area`
Ranks on 25 of 27 result pages, often twice. Title "פרויקטים ודירות חדשות בתל אביב והסביבה - מעודכן ל-2026".

- **Top navigation:** פרויקטים חדשים · נדל״ן חו״ל · חברות נדל"ן · **פרויקטים במבצע** · יזם החודש · מפה · פרסום פרויקט.
- **Filters:** דירות חדשות / הכל · סוג הנכס · מחיר · חדרים · **אכלוס קרוב** (a toggle) · **סיורי 3D**.
- **Filtered URLs that rank with counts in the title:** "14 פרויקטים ודירות חדשות בתל אביב והסביבה לאכלוס קרוב", "39 פרויקטים … עד 2,000,000 ₪", "32 … עד 1,500,000 ₪", "פרויקטים ודירות חדשות ברמת גן עד 2500000 ₪".
- **Card fields:** badge row (**אכלוס קרוב**, **במבצע**), name, street + neighbourhood + city, "4-5 חדרים • 1-9 קומות • 101-169 מ״ר", **"החל מ- ₪"**, sometimes **"החל מ- 42,000 ₪ למ"ר"** (price per m²), one marketing line ("אכלוס מיידי!", "משלמים 1M בלבד במעמד החוזה", "תנאי תשלום בהתאמה אישית").
- **Below the grid:** "פרויקטים נוספים באזור זה" (12 more), then link blocks: by district, by area, **by rooms** (3/4/5/6/7 rooms in the area), by type (קרקעות, דופלקסים, דירות גן, בתים על הים), value estimate calculator ("הערכת שווי נכס").
- **SEO text at the foot:** one paragraph promising "סיור וירטואלי … הנוף האמיתי מכל חלון … כלי ניתוח דאטה … להשוות בין פרויקטים". Google quotes it as the snippet on most queries.
- **Schema:** ItemList. 97 images (project renders). Hebrew only.
- **Deals hub** `/yad1/projectsale` ("פרויקטים חדשים במבצע | יד2"): the same cards filtered to "במבצע", nationwide; it ranks first for "דירות מקבלן במבצע" and "מבצעים דירות מקבלן".
- **Best at:** filtered pages with live counts (occupancy, budget, rooms) that Google treats as answers; the occupancy toggle; price per m² on some cards; a dedicated deals hub.

## 3. Government: `dira.gov.il` → gov.il "דירה בהנחה"
Not in the family's top 10 (its own intent: מחיר למשתכן 90,500 and דירה בהנחה 74,000 a month).

- **Opening:** "דירה בהנחה" is the umbrella name for מחיר מטרה, מחיר מופחת, מחיר למשתכן and דירה להשכיר.
- **Entry points:** אתר ההרשמה להגרלות · **דירות למכירה ללא הגרלה** · **מפת הפרויקטים** · **הצטרפות לקבלת עדכונים** · אזור אישי.
- **News strip:** the 11th lottery (7,922 units in 19 towns; about 115,000 households registered; winners notified 2.8.2026).
- **Services:** eligibility request, extension, lottery registration, cancel participation, complaint against a seller.
- **Best at:** an official **project map** and an official list of **discounted flats sold without a lottery**, the only true below-market inventory in Israel. A hub that shows these next to private projects (clearly labelled) answers "מבצע" better than any portal.

## 4. Developer "available apartments": Ashtrom Megurim
Ranks top 3 on every immediate-occupancy query ("דירות חדשות לאכלוס מיידי בפרויקטים מובילים").

- **Home:** H1 "תהיו בטוחים, אשטרום מגורים", H2 "הבית הבא שלכם", then 8 project tiles, **each badged "אכלוס מיידי"** (i- Neot Afeka, REMEZ 36, העצמאות הרצליה, A- NEOT AFEKA, איינשטיין רמת אביב, גלי נתניה, Recanati Residence, אבן שפרוט הרצליה), then "פרויקטים בשיווק" and "פרויקטים שהושלמו".
- **Marketing page** `/projects/marketing-projects/`: short intro ("דירת 4 או 5 חדרים, דירת גן או פנטהאוז … 2-5 חדרים"), filter tabs כל הפרויקטים / מגורים / התחדשות עירונית / מסננים, cards with status (בשיווק), developer, type, city, **units count**.
- **Project page** for immediate occupancy (e.g. העצמאות הרצליה) carries "אכלוס מיידי" in the title.
- **Schema:** the JSON-LD on the home page does not parse. **Languages:** Hebrew and an EN switch.
- **Best at:** owning "אכלוס מיידי" with a plain badge on every tile and the phrase in each project title. Same pattern at Sela Binui ("דירות לדוגמה למכירה | אכלוס מיידי": "שלמו רק 5% עכשיו והיתרה באכלוס, ללא ריבית והצמדה").

## 5. nadlan.com (home)
On 16 of 27 result pages, always with its home page. Title "NADLAN.COM | לוח דירות חדשות, פרויקטים חדשים ודירות קבלן במחירים מיוחדים…".

- **Opening:** a search box "**מצאו את דירת החלומות שלכם בעזרת AI**", then H1 "NADLAN.COM | נדל"ן.קום לוח נדל״ן: דירות חדשות, פרויקטים חדשים, קרקעות והשקעות נדלן".
- **Blocks:** dated opinion and news articles (1.11.2026, 25.10.2026), "הטבות מיוחדות" project cards (ENZO, K עיר היין, Private Collection, מקסיקו, UP LIFE נתיבות), newsletter "מועדון הנדלניסטים".
- Google's snippet for it mentions "הדמיות, תוכניות דירה, סיורים וירטואליים, צילומי וידאו ושכבות מידע אינטראקטיביות על גבי מפה".
- **Schema:** none found. Hebrew only.
- **Best at:** an exact-match title carrying all three head phrases (דירות חדשות, פרויקטים חדשים, דירות קבלן) and an AI search box as the first element.

## 6. Socity: `socity.co.il/city/פרויקטים-חדשים-בתל-אביב/`
A developer's content page that ranks on 7 result pages (Tel Aviv, prices, centre, near-me).

- **Headings (H2):** פרויקטים חדשים בתל אביב · להורדת מפרט הדירות · איפה יש פרויקטים חדשים בתל אביב · יתרונות וחסרונות של פרויקטים חדשים · פרויקטים בשיווק בתל אביב · מדוע לרכוש דירה חדשה בתל אביב · שאלות/תשובות · lead form.
- **One table** by רובע: main areas, share of population, **average 4-room price**, **monthly rent for 4 rooms**. Snippet Google shows: "35,000 to 100,000 ₪ per m² by quarter".
- About 1,850 words. **Schema:** Place, Organization, WebSite, CollectionPage. Hebrew only.
- **Best at:** a single, quotable price-range sentence per m² and a quarter-by-quarter table. The AI box for "פרויקטים חדשים בתל אביב" cites it.

## Also ranking, not read in full
- **Dimri `/projects`** (19 of 27 result pages): a developer portfolio by city with starting prices (Google's AI box quotes "נתניה … החל מ-2,155,000 ₪").
- **Tidhar `/residences/for-sale/`**, **Hagag `/ResidentProjects`** (Google rating 4.1, 116 reviews in the snippet), **Peretz Bonei Hanegev `/projects-for-sale`**, **Aura**, **Gabay**, **Oron**: developer "in marketing" pages.
- **nadlanmaster.co.il**: city pages with **price ranges by room count** ("3 rooms 2.8-4.5M"), budget pages ("דירות חדשות עד מיליון וחצי").
- **yeshnadlan.co.il**, **myplace.co.il**, **project-tlv.info**, **digg.co.il**, **last-one.co.il** ("דירות אחרונות מהקבלן … אכלוס מיידי במחירי הרגע האחרון"), **nadlan-mekablan.co.il**, **hadashim.co.il** (new buyer guides, October 2026).
- **News for deals:** Calcalist (Gindi: 900,000 ₪ deferred for ten years after keys, no interest or indexation, about 300 flats), Bizportal (developers' cash flow from sales down 58% in August, "כמה שווים המבצעים").

## The gap nobody fills
| Need | Who does it today | Gap |
|---|---|---|
| Live count of projects by stage, with the date | Madlan (one number), Yad2 (one filter) | Nobody shows **all stages side by side** with counts and a check date |
| Immediate occupancy across developers | Yad2 toggle (Tel Aviv area), each developer for itself | No national, cross-developer list with delivery month |
| Deals in shekels | Free-text badges (Madlan, Yad2), news articles | **Nobody values a deal** (20/80, no indexation, 10-year deferral) in shekels against a normal schedule |
| Marketing price against real deal prices | Nobody | Our catalog already shows city and street ₪/m² from the Tax Authority on cards |
| Budget answer ("what can I get for 2M") | Yad2 filtered URLs, Facebook groups, news | No tool that combines budget, mortgage capacity and the real list |
| Near me | Google guesses from location | No ranking page has a location tool with walking minutes |
| Alerts | Madlan alert button, gov.il updates | No alert for "project moved to immediate occupancy" or "new deal in my city" |
| Languages | Hebrew only (all portals) | We have he, en, fr, ru on the hub |
