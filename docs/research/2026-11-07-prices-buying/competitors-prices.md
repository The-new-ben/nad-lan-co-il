# Competitor teardown: "מחירי דירות" (read 7.11.2026, desktop Chrome)

Each page was read in the browser through its DOM: headings, paragraphs, tables, inputs, JSON-LD and visible numbers. "Words" means the visible page text, chrome included. Numbers are copied as shown, with the date and source the page itself gives.

---

## 1. nadlan.gov.il: the government real-estate site (top 3 on all four head queries)
- **Title:** אתר הנדל"ן הממשלתי – נתוני עסקאות נדל"ן רשמיים
- **Meta:** "נתוני עסקאות נדל"ן רשמיים בישראל: מחירי דירות שנמכרו, שכירות ומידע על הסביבה, לפי יישוב, שכונה, רחוב או כתובת."
- **Headings:**
  - H1 אתר הנדל"ן הממשלתי
  - H2 נסח טאבו מהמפה · הבית לנתוני הנדל"ן הממשלתיים · כל המידע שצריך - במקום אחד!
  - H3 צפו · חקרו · השוו · עסקאות חדשות לידי? יש פרויקט חדש בשכונה?
- **Opening:** "באתר נתונים אודות נכסים ועסקאות שעברו טיוב, תקנון וסינון, מתוך מסדי הנתונים השונים של משרדי הממשלה… על גבי מפה… חיפוש חופשי, גוש/חלקה, שכונה וכתובת."
- **Tone:** official and terse. 134 words on the landing page.
- **Tools:**
  - address / street / settlement search, plus "search by my current location";
  - a map of deals;
  - search by gush/helka;
  - "הזמינו נסח טאבו" (order an official land-registry extract from the map);
  - "הירשמו לקבלת עדכונים" (alerts for new deals or projects nearby).
  - A reCAPTCHA sits on a form.
- **Numbers:** none on the landing page; they appear after a search.
- **Structured data:** none.
- **Why it wins:** it is the official source, the AI overviews cite it as the place to verify, and its brand is the query ("רשות המסים מחירי דירות").

## 2. madlan.co.il/area-info/תל-אביב-יפו-ישראל (top 3 on "מחירי דירות" and "מחירי הדירות")
- **Title:** תל אביב יפו - מידע ומחירי דירות שנמכרו בעיר | מדלן
- **Meta:** sold prices, new projects, neighbour reviews, map, population, schools, kindergartens, "אנטנות סלולריות, מפגעים".
- **Headings:**
  - H1 תל אביב יפו · H2 עיר
  - H3: סקירה כללית על העיר · מחירי דירות בתל אביב יפו · עסקאות בתל אביב יפו (1000) · בתי ספר · נתונים נוספים
  - H2 יעניין אותך לדעת… (about 30 H3 blog and podcast teasers)
  - H3 בתים למכירה בעיר · H2 פרויקטים למכירה בעיר
- **Opening:** none. The page opens straight into data cards. Tone: a dashboard, almost no prose. About 1,600 words.
- **Data shown:**
  - Overview: average purchase price ₪4,768,095 · average rent ₪9,500 · 6,150 listings · "the popular party".
  - Price by rooms, with three columns (new / second-hand / rent):
    | Rooms | New | Second-hand | Rent |
    |---|---|---|---|
    | 1 | ₪2.55M | ₪1.48M | ₪3,765 |
    | 2 | ₪2.87M | ₪2.72M | ₪6,900 |
    | 3 | ₪4.45M | ₪3.37M | ₪9,000 |
    | 4 | ₪5.65M | ₪4.17M | ₪11,200 |
    | 5 | ₪7.01M | ₪5.56M | ₪13,500 |
    | 6 | ₪13.51M | ₪6.4M | ₪18,750 |

    Rent is also shown for duplex, penthouse, mini-penthouse, house and garden flat.
  - "מגמות מחירים" chart with filters (rooms, deal type); "תאריך עדכון אחרון: 15.9.2026".
  - Deals table: address, date, price, m², ₪/m², rooms, a brokerage flag; filters for rooms and deal year; 125 pages. Latest rows are dated 29.10.2026.
  - Census block ("ממצאי מפקד האוכלוסין של הלמ״ס שפורסם ב-2024… סוף 2022"): 27% with a bachelor's degree, 17% hi-tech, 34% aged 20 to 39, 72% secular, 55% renting, 34% three-room flats, 2022 elections.
  - Schools table (grades, supervision, average pupils per grade); map.
  - About 15 chart or map nodes.
- **Structured data:** Place, BreadcrumbList.
- **Why it wins:** a city answer to a national query. Google maps "מחירי דירות" to the largest city, and Madlan has the deepest per-city data, real deal rows that Google lifts into the snippet ("₪46,250 למ״ר"), and freshness.

## 3. yadata.yad2.co.il: Yad2's data product (positions 1 to 8 across the cluster, several URLs)
### 3a. /market/sale, Tel Aviv-Yafo city view
- **Title:** תל אביב יפו: מחירי דירות, עסקאות אחרונות ומידע על האזור | ידאטה
- **Headings:**
  - H1 "תל אביב יפו מחירי דירות, עסקאות אחרונות וכל המידע העדכני של החודש האחרון על האזור"
  - KPI H3s: נכסים חדשים שמוצעים למכירה · נכסים יד שניה שמוצעים למכירה · מספר הימים הממוצע למודעה · מספר הקונים שפתחו מודעה · מדד השוק · מדד ההתפשרות
  - H2 מחירים ועסקאות (H3 התפלגות מחירים, מגמת מחירים) · H2 מחירי דירות שנמכרו… לפי כתובת · H2 אוכלוסייה · H2 מוסדות חינוך · H2 מפה · H2 דירות למכירה · H2 דירות ופרויקטים חדשים
- **Data shown (city, "last month"):**
  - 5,345 new properties for sale (+4% y/y) · 7,110 second-hand (+2%) · 38 average days per listing (−5%) · 80,223 buyers who opened a listing (+30%).
  - Market gauge: sellers' / balanced / buyers' market; Tel Aviv currently reads buyer-friendly.
  - **"מדד ההתפשרות": "הפער בין המחיר המבוקש למחיר סגירה בעיר הוא 5.3% בממוצע".**
  - Price-distribution table (rooms → average price, average ₪/m², share of supply):
    | Rooms | Average price | Average ₪/m² | Share of supply |
    |---|---|---|---|
    | 2 | ₪3,070,000 | ₪55,250 | 17% |
    | 3 | ₪4,070,000 | ₪50,900 | 34% |
    | 4 | ₪5,130,000 | ₪47,350 | 32% |
    | 5 | ₪6,810,000 | ₪48,450 | 15% |
    | 6 | ₪9,180,000 | ₪42,300 | 2% |
  - 12-month price-trend chart (11/25 to 10/26), apartments versus houses.
  - Sold-by-address table: address, type, date, rooms, m², **floor, year built**, price; filters for rooms, from 2024, type, price; 1,021 pages.
  - Population: lifestyle, marital status, 53% academic, transport to work, age histogram, 210,390 households, 2.2 persons per household.
  - Schools rated by Meitzav and social climate.
  - Map, listings, new projects.
  - **Yadata AI chatbot** with sample questions: "איפה אוכל לקנות דירה ב-2,000,000 ש״ח באזור המרכז?", "מה מחיר הדירות הממוצע בתל אביב?", "כמה תעלה לי שכירות של דירת 3 חדרים בשכונת הבורסה?"
  - About 118 chart nodes.
- **Structured data:** none. About 1,130 words.
### 3b. /market/sale without a city
A thin chooser: 298 words, H1 "מחירי דירות שנמכרו, עסקאות אחרונות ומידע על האזור", 12 city links. The national view has no national numbers.
### 3c. /property-valuation (number 1 for "מחיר דירה" and "מחירון דירות")
An address-based valuation that uses "המרחק ממוקדי עניין, נתיבי תחבורה ועוד" and takes about 5 minutes. (Our equivalent is /property-value-estimator/, which also ranks on page 1 for both queries.)

## 4. kantahome.com/forecasts-and-indexes/housing-index (the main number source for the AI overviews)
- **Title:** מדד מחירי הדירות בישראל | תחזית מחירי הדירות לשנת 2026
- **Meta:** "…טבלאות שינוי לפי חודשים ושנים, גרף היסטורי, מחירי דירות לפי ערים ותחזית… מתעדכן עם כל פרסום."
- **Headings:**
  - H1 מדד מחירי הדירות בישראל - תחזית מחירי הדירות לשנת 2026
  - H2: מדד מחירי הדיור 2026 טבלה לפי חודשים · 2025 טבלה לפי חודשים · היסטורי לפי שנים · גרף מחירי הדיור בישראל · מגמת מחירי הדיור בשנים האחרונות (H3 per month and year) · **מחירי הדיור לפי ערים וכמה משכורות נדרשות לרכישת דירה** · תחזית מחירי הדיור 2026 (H3 היקף הבניה בארץ · גובה הריבית במשק · יציבות המדינה) · למה מחירי הדירות עולים? · עליית מחירי הדיור בעשור האחרון · האם יש סיכוי לירידת מחירי הדיור? · איך נמדדים מחירי הדיור בארץ? · השפעת הריבית על מחירי הדיור · מחשבון מדד מחירי הדיור · podcast · lead forms
- **Opening:** "אחרי עליות חדות בשנים האחרונות (14.7% ב-2022 ו-7.7% ב-2024), מחירי הדיור בישראל התמתנו: ב-2025 ירד מדד מחירי הדירות ב-0.1%, ומתחילת 2026 נרשמה ירידה מצטברת של 1.7% (נכון למדד יולי 2026, לפי הלמ"ס)…"
- **Tone:** explanatory, the voice of a mortgage-advice lead generator. About 2,090 words.
- **Numbers:**
  - Monthly change chips (−1.7%, −0.6%, 0.1%…).
  - **City table of average price for 3.5 to 4 rooms, and "salaries needed"** (CBS; average wage ₪11,730 per the National Insurance Institute):
    | Area | Average price | Salaries needed |
    |---|---|---|
    | Israel | ₪1,974,000 | 168 |
    | Jerusalem | ₪2,870,000 | 245 |
    | Tel Aviv | ₪4,885,000 | 416 |
    | Haifa | ₪1,807,000 | 154 |
    | Rishon LeZion | ₪2,387,000 | 204 |
    | Petah Tikva | ₪2,422,000 | 207 |
    | Netanya | ₪2,434,000 | 208 |
    | Ashdod | ₪1,963,000 | 168 |
    | Bnei Brak | ₪2,451,900 | 209 |
    | Be'er Sheva | ₪1,210,000 | 103 |
    | Holon | ₪2,251,000 | 199 |
    | Ramat Gan | ₪3,178,900 | 272 |
    | Ashkelon | ₪1,454,000 | 124 |
    | Rehovot | ₪2,258,000 | 193 |
    | Beit Shemesh | ₪1,938,000 | 166 |
    | Bat Yam | ₪2,979,000 | 254 |
    | Kfar Saba | ₪3,000,000 | 256 |
  - Construction of about 50K units a year in 2017 to 2022; a "shortage of 228 thousand apartments" (per the Builders Association report).
- **Tools:** the "מחשבון" is only instructions to use the CBS linkage calculator (index code 40010). No live widget; three name and phone lead forms.
- **Structured data:** none.
- **Why the AI overview cites it:** every number sits in a sentence with a date and "לפי הלמ"ס"; city averages come in one list; it has a forecast section.

## 5. mashcantaman.co.il/מדד-מחירי-הדירות/ (an AI-overview source)
- **Title:** מדד מחירי הדירות | משכנתאמן. H1 only. About 1,080 words.
- **Opening:** the market is in the headlines; since 2016 "הגוף היחיד שמוסמך לפרסם נתונים בנוגע למחירי הדיור הינו הלשכה המרכזית לסטטיסטיקה"; published on the 15th, based on two months of Tax Authority deals.
- **Table** (from 1994 to today): publication date · index · monthly % · annual %. For example:
  | Published | Index | Monthly % | Annual % |
  |---|---|---|---|
  | 15/06/2026 | 599.6 | −0.3 | −1.3 |
  | 15/05/2026 | 601.4 | +0.3 | −1.2 |
  | 15/04/2026 | 599.6 | −0.1 | −1.7 |
  | 15/03/2026 | 600.2 | −0.1 | −1.0 |
  | 15/02/2026 | 600.8 | +0.8 | +0.3 |
  | 15/01/2026 | 596 | +0.6 | −0.1 |
  | 15/12/2025 | 593 | −0.7 | −0.1 |
  | 15/11/2025 | 597.2 | −0.6 | +0.8 |
- **Tools:** a lead form with a city select.
- **Structured data:** WebPage, ImageObject, BreadcrumbList, WebSite, Organization.

## 6. hon.co.il/מחירי-דירות-לפי-עיר/ (page 1 for "מחיר דירה")
- H1 מחירי דירות לפי עיר. 424 words. Article schema with a Person author.
- **Tool:** choose a city and get a current price range.
- **Teaching paragraph (good DNA):** "מודעות מציגות מחיר מבוקש, לא מחיר שנסגר… המדד הנכון להשוואה… הוא מחיר למטר רבוע". Worked example: 100 m² at ₪30,000 versus ₪22,000 per m² is an ₪800K gap; at 70% financing that is ₪560K more loan.
- Sister page /מחשבון-מחירי-הדירות/ (2016) links a past price to the CBS index ("average about ₪2.4M").

## Seen in the SERP, not read in full
- **cbs.gov.il:** the subject page did not render text in the automated tab (only an accessibility toggle came back); not pursued.
- **News that ranks:** tlvonline, Globes, Calcalist, TheMarker, Mako, Maariv, Bizportal (the dated sources the AI overview quotes for "did prices fall").
- **Other price tools:** count.co.il (₪/m² calculator with weighted area); madadirot.co.il (per-city average, ₪/m², asking rent); levi-itzhak (price list and "השוואת מחירי דירות"); dirobot.co.il.

---

## World benchmark (house-price pages of the global leaders)

### Zillow: Home Values / ZHVI (zillow.com/home-values/)
- H1 "United States Housing Market". The big number is the typical home value, **$366,157, +1.2% over 1 year**, "homes go to pending in around 27 days (Updated on 9/30/2026)".
- "Key Takeaways" and "Housing Market Overview", **each metric with its own date**:
  - 1-yr market forecast 1.1%
  - for-sale inventory 1,406,624
  - new listings 362,642
  - median sale-to-list ratio 0.997
  - median sale price $382,333
  - median list price $403,300
  - % of sales over list 29.3%
  - % under list 51.1%
  - median days to pending 27
- ZHVI chart with home-type tabs (All / Single family / Condo) and ranges (1-yr / 5-yr / Max). Rental market trends. Methodology link. **Downloadable data** ("Housing Data page").
- FAQ: current values · recent change · states with the highest values · fastest-growing metros.
- **JSON-LD:** WebPage, **FAQPage**, BreadcrumbList.
- CTAs: local agent, pre-qualify.

### Rightmove: House Price Index (rightmove.co.uk/news/house-price-index/)
- A monthly report dated 19 October 2026, "Download full report", a table of contents, a news-style H1 ("Signs that soaring mortgage rates are now biting harder"), and narrative H2s.
- "The numbers at a glance": national average asking price £371,015, +1.0% m/m, −0.1% y/y, broken down **by market sector** (first-time buyer / second-stepper / top of the ladder). Expert comment.
- Tables: monthly average asking price · % change · **stock per agent** · **time on market**. Five-year trend.
- **Regional map** and 11 regional H2 sections; London trends.
- **Affordability:** "Monthly rent and mortgage costs for a first-time buyer home"; "Asking prices and income-based borrowing capacity"; mortgage-rate context (2-year fixed 5.55%).
- Editors, a past-reports archive, "Check how much homes near you sold for", instant valuation.
- **JSON-LD:** CollectionPage, ImageObject, BreadcrumbList, WebSite.

### Global Property Guide: Israel (globalpropertyguide.com/middle-east/israel/price-history)
- About 6,200 words of analysis.
- H2s: Property Prices and Price Index · House Price Variations (district; new homes; "City-level averages tell a different story from the index") · Demand (transactions, war, investors versus foreign buyers) · Supply (record construction; three districts; planning pipeline) · Rental Market (rents up while prices fall; poor yields) · Mortgage Market (rate cuts not reaching borrowers; supervisory tightening; purchase tax on investors) · Historic Perspective (three decades; "deepest in real terms since 2018"; past shocks) · Economic and Social Factors.
- **Nominal and inflation-adjusted annual table, 2008 onward.**
- Key numbers: +0.1% in May to June 2026 against the prior period; −1.5% y/y; **−2.96% in real terms**; April to May 2026 −1%, "the largest two-month fall in eight years"; prices fell in 9 of 12 months.
- Paywall for the full dataset; "Compare cities".

### What the world leaders have that no Israeli page in the top 10 has
1. One national dashboard where **every metric carries its own date** (Zillow).
2. **Real (inflation-adjusted) versus nominal** price change (GPG). Israeli pages show nominal only.
3. **Sale-to-list ratio and % sold above or below asking** (Zillow). Yadata has a single "התפשרות" % per city only.
4. **Affordability against income and rent:** monthly mortgage versus rent for a first-buyer home, and borrowing capacity versus price (Rightmove). Kanta has only "salaries needed".
5. **A forecast with a stated number** (Zillow 1-year forecast). Kanta has qualitative drivers only.
6. **Downloadable data and a monthly report archive** (Zillow Housing Data; Rightmove PDFs and past reports).
7. **Market-sector split** (first-time / mover / top of the ladder) (Rightmove).
8. **A regional map with a section per region** (Rightmove). Madlan and Yadata do it per city only.
9. **History through past shocks** (GPG).
10. **FAQPage schema on the price hub** (Zillow). No Israeli price page in the top 10 has FAQ schema.
11. **Time on market and stock levels, nationally** (Rightmove, Zillow). Yadata has this per city, not nationally.

---

## Our page versus the winners: nad-lan.co.il/apartment-prices/ (read 7.11.2026)
- **Title:** "מחירון הדירות של ישראל: כל הערים והמספרים במקום אחד". **H1:** מחירון הדירות של ישראל.
- **H2s:** מחירון דירות לפי עיר: חציון לפי חדרים · תל אביב והשכונות המבוקשות · גוש דן והמרכז · השרון · ירושלים ומודיעין · יישובי הבתים הפרטיים · חיפה והצפון · השפלה והדרום · נדל"ן מסחרי (H3 משרדים / חנויות / תעשייה ולוגיסטיקה) · הכלים שממשיכים מכאן.
- About 1,040 words in the main content.
- **Opening:** "כמה באמת עולה דירה בכל עיר?…". Second paragraph: Q2-2026 national medians of ₪1,677,400 (3 rooms) / ₪2,028,800 (4 rooms) / ₪2,822,700 (5 rooms), with y/y +5.4% / −4% / −2.8%; Q1-2026 4-room range from ₪1,203,200 (Be'er Sheva) to ₪5,229,800 (Tel Aviv-Yafo).
- **Table:** 25 rows (national plus 23 cities) × medians for 3, 4 and 5 rooms with y/y change and quarter; source data.nadlan.gov.il; definitions (median, quarter, a dot means not published).
- **Schema:** WebPage, WebSite, Organization. **No FAQPage, no Dataset.**
- **Charts 0, maps 0, calculators 0** (three search inputs only).
- **Links out:** 23 city price pages, luxury / penthouse / seafront / Neve Tzedek / Herzliya Pituach, house prices (Savyon, Kfar Shmaryahu, Rishpon, Arsuf), 15 office and commercial price pages, /property-value-estimator/, /apartment-purchase-cost-calculator/.

### Gap table
| Item | nadlan.gov | Madlan | Yadata | Kanta | Mashcantaman | World | **Us** |
|---|---|---|---|---|---|---|---|
| Medians by city × rooms in one national table | – | per city only | per city only | city average for 3.5 to 4 rooms only | – | Zillow by metro | **YES (unique)** |
| Source and quarter stated per number | official | update date | "last month" | "לפי הלמ"ס" | publication date | Zillow per metric | YES (quarter) |
| ₪ per m² by rooms | after search | in deal rows | **YES** | – | – | – | **NO** (claimed in the intro, missing from the table) |
| New vs second-hand split | – | **YES** | – | – | – | – | NO |
| Rent and yield next to price | rent | **YES** | chatbot | – | – | Zillow rentals | NO |
| Recent sold deals list | **YES** | **YES** | **YES** | – | – | Rightmove link | NO (we must route, not compete) |
| 12-month or historical chart | – | YES | YES | YES | – | all three | **NO** |
| CBS monthly index table (m/m, y/y) | – | – | – | YES | **YES** | – | NO |
| "Did prices fall" answer by district | – | – | – | partial | – | GPG | **NO** |
| Market temperature (supply, days on market, asking-vs-closing gap) | – | – | **YES** | – | – | Zillow, Rightmove | NO |
| Affordability (salaries, rent vs mortgage) | – | – | – | salaries | – | Rightmove | NO |
| Forecast and drivers | – | – | – | YES | – | Zillow, GPG | NO |
| Real vs nominal | – | – | – | – | – | GPG | NO |
| Map | YES | YES | YES | – | – | Rightmove | NO |
| FAQ block and FAQPage schema | – | – | – | – | – | Zillow | NO |
| Dataset or downloadable data | open data | – | – | – | – | Zillow | NO |
| Value estimator | – | YES | YES | – | – | YES | child page (link only) |
| Luxury / segment price pages | – | – | – | – | – | – | **YES (unique)** |
| Commercial price pages | – | – | – | – | – | – | **YES (unique)** |
| Regional grouping of cities | – | – | – | – | – | Rightmove | YES |
| Methodology and definitions | – | – | – | short | short | Zillow | YES |

**Bottom line.** We are the only page with a cross-city × rooms median table, segment pages and commercial pages; that is our moat. We lack every "living" layer the winners use: charts, the CBS index series, the district answer to "did prices fall", ₪/m², new versus second-hand, rent and yield, market temperature, affordability, a map and FAQ schema. We also lack the "sold prices" router, the biggest related-search family.
