# New residential projects in marketing: market table (read 25.10.2026)

Data file: `market.json` (same folder). One object per project. Facts are copied as published, with the source URL; nothing was estimated.
An empty field means the source did not publish it. Raw pages and the audit trail (verbatim evidence for every price, unit count and
delivery date) are kept outside the repo in `C:\Users\777\nad-lan\_private-research\2026-10-25-projects-hub\` (`market-raw\`, `market-evidence.json`).

## Counts

| | Count |
|---|---|
| Projects (total) | 566 |
| Tel Aviv-Yafo | 143 |
| Other cities | 423 (in 55 cities) |
| With a from-price (`price_from`) | 348 (Tel Aviv 46) |
| With a per-sqm price (`price_psqm`) | 6 |
| With a delivery / occupancy date | 115 |
| With payment terms (`deal`) | 64 |
| Main source: developer site / portal / news | 282 / 274 / 10 |
| Developer-sourced records whose price came from Yad2 (`extra_sources`) | 83 |

Status: marketing 390, immediate 67, construction 52, presale 39, near_occupancy 18.
Renewal type: none stated 456, new_neighbourhood 60, pinui_binui 27, tama38 23.

Tel Aviv neighbourhood spread (as published by the source; sample): - 29, הצפון הישן 19, רמת אביב ג' 4, רמת אביב 4, הצפון החדש - דרום 4, נאות אפקה ב' 4, הדר יוסף 4, יפו 3, בבלי 3, רובע שדה דב 3, נחלת יצחק 3, נווה אביבים 3, יד אליהו 3, הצפון החדש - כיכר המדינה 3, נאות אפקה א' 2, איזור שדה דב 2, נווה חן 2, ביצרון 2, נאות אפקה 2, אפקה 2, הצפון החדש - צפון 2, מרכז יפו 2, הצפון הישן (רובע 3) 2, כרם התימנים 1, רביבים 1.

### Projects per city

תל אביב-יפו 143 · רמת גן 37 · ירושלים 34 · פתח תקווה 32 · בת ים 29 · נתניה 29 · הרצליה 19 · לוד 16 · רחובות 16 · רמת השרון 16 · ראשון לציון 14 · חיפה 13 · חולון 12 · אשקלון 10 · רעננה 10 · קריית אונו 9 · גבעת שמואל 8 · הוד השרון 8 · אשדוד 7 · חדרה 7 · באר יעקב 6 · גבעתיים 6 · יבנה 6 · אור יהודה 5 · אילת 5 · באר שבע 5 · נהריה 5 · קריית אתא 5 · אופקים 4 · טירת כרמל 4 · נתיבות 4 · פרדס חנה-כרכור 4 · קריית גת 4 · יהוד-מונוסון 3 · ראש העין 3 · רמלה 3 · גני תקווה 2 · כפר יונה 2 · מודיעין-מכבים-רעות 2 · נס ציונה 2 · קדימה-צורן 2 · בית שמש 1 · בן שמן 1 · בני עי"ש 1 · ג'סר א זרקא 1 · גדרה 1 · גן יבנה 1 · כפר סבא 1 · כרכום 1 · מצפה גליל 1 · נשר 1 · עכו 1 · עתלית 1 · קיבוץ אלומות 1 · קריית ביאליק 1 · תל מונד 1

## From-prices per city (cheapest and most expensive `price_from`)

| City | Priced | Cheapest | Most expensive |
|---|---|---|---|
| תל אביב-יפו | 46 | מתחם יאפא (צברים) 1,990,000 [yad2] | Ensemble (גולדווסר מינצר) 9,490,000 [yad2] |
| פתח תקווה | 29 | Mega Verber (קבוצת אבנר אליהו) 1,990,000 [yad2] | מיתר בקריה האקדמית (ח. מיתר) 4,800,000 [nadlan.com] |
| ירושלים | 23 | מקסיקו (רוטשטיין) 2,070,000 [yad2] | הכתר (מידר) 10,150,000 [yad2] |
| רמת גן | 21 | הרכסים 32-34 רמת גן (רייך-שחר בע"מ, BLD) 2,250,000 [yad2] | נוף אפעל SUNSET SUNRISE (סלע בינוי) 4,790,000 [yad2] |
| נתניה | 18 | AURA THE STRIP נתניה (אאורה) 1,990,000 [yad2] | YAMA - עיר ימים (י.ח. דמרי) 8,700,000 [developer] |
| בת ים | 17 | MINUTE מינט, בת ים (גשם החזקות) 2,150,000 [yad2] | SOL בת ים (סופרין נכסים בע"מ) 4,250,000 [yad2] |
| רחובות | 12 | AMPA PARK (אמפא ישראל ונפתלי ניסן) 1,960,000 [yad2] | Private Collection (יסודות איתנים יזום ובניה) 4,980,000 [nadlan.com] |
| ראשון לציון | 11 | כסיף בשכונת רמז המבוקשת מניה שוחט 3-5 (א.כסיף יזמות והשקעות נדל"ן) 2,440,000 [yad2] | אלקטרה לייף סטייל מתחם ה-1000 (אלקטרה מגורים) 3,790,000 [yad2] |
| אשקלון | 10 | אפגד באגמים (אפגד) 1,585,000 [yad2] | YAMA מרינה אשקלון (י.ח. דמרי) 2,490,000 [yad2] |
| חולון | 10 | גולומב (שיכון ובינוי נדל"ן) 1,660,000 [yad2] | ביאליק חולון (אורון נדל"ן) 2,799,000 [yad2] |
| לוד | 10 | RAYK לוד החדשה (קבוצת רייק) 1,950,000 [yad2] | אאורה בן שמן (אאורה) 2,680,000 [yad2] |
| רמת השרון | 10 | החלוץ (רמות בעיר) 2,950,000 [yad2] | LIA ליה (חן ואיתי גינדי) 5,980,000 [yad2] |
| הרצליה | 8 | חיים בויצמן 43 (פורוורד תנופה) 2,750,000 [yad2] | אמפא גליל ים (אמפא ישראל) 5,390,000 [yad2] |
| חיפה | 8 | אידר 39 חיפה (קבוצת שובל) 2,280,000 [yad2] | שמורת אלמוגים (אלמוגים החזקות) 3,466,000 [yad2] |
| אשדוד | 7 | כוכב הצפון (תדהר ויובלים) 1,770,000 [yad2] | THE LUX (קבוצת גבאי) 2,990,000 [yad2] |
| חדרה | 7 | ERA – רובע העתיד של חדרה (רוטשטיין) 1,350,000 [yad2] | פנינת הטייסים (ED בנייה ויזמות נדל"ן) 2,990,000 [yad2] |
| הוד השרון | 6 | השחר 49, הוד השרון (יצחק עופר חברה לבניין ופיתוח בע"מ) 3,000,000 [yad2] | רובע המייסדים - שלב ב' (קבוצת גבאי) 4,500,000 [yad2] |
| קריית אונו | 6 | מיתר באונו (ח. מיתר) 1,990,000 [nadlan.com] | הרימון (מצלאוי חברה לבנין) 3,350,000 [nadlan.com] |
| רעננה | 6 | שברץ 23 רעננה (מבני שלהב 1987 בע"מ) 2,680,000 [yad2] | שוסטר ברעננה (נוה שוסטר) 3,700,000 [yad2] |
| אור יהודה | 5 | נווה אור (י.ח. דמרי) 2,380,000 [developer] | OLAM (שיכון ובינוי נדל"ן) 2,950,000 [yad2] |
| אילת | 5 | אייל פרץ בשירת ההר אילת (אייל פרץ יזמות ונדל"ן) 1,290,000 [yad2] | AQUA RESORT (עמרם אברהם) 2,490,000 [yad2] |
| באר שבע | 5 | פארק הנחל (י.ח. דמרי) 1,330,000 [developer] | צרפתי בפארק (צרפתי שמעון) 1,790,000 [yad2] |
| יבנה | 5 | Above יבנה (חג'ג' צים) 2,140,000 [yad2] | האורנים יבנה (קבוצת מזרחי ובניו) 2,690,000 [yad2] |
| באר יעקב | 4 | צרפתי בשקמה - באר יעקב (רמי צרפתי) 2,440,000 [yad2] | ANDA באר יעקב (אפרידר) 3,250,000 [yad2] |
| גבעתיים | 4 | Only גבעתיים (אאורה) 3,585,000 [yad2] | אאורה אימג'ן גבעתיים (אאורה) 4,580,000 [yad2] |
| נהריה | 4 | אפי אכזיב (אפי קפיטל) 1,650,000 [yad2] | שכונת הים אכזיב (אלקטרה מגורים וצמח המרמן) 2,290,000 [yad2] |
| פרדס חנה-כרכור | 4 | גרופית VIEW, פרדס חנה (גרופית) 1,700,000 [yad2] | גרופית בשמורה (גרופית) 3,900,000 [nadlan.com] |
| קריית אתא | 4 | כלניתא (מ.א.י אביבי ייזום ובניה) 1,899,000 [yad2] | ALONIM - דר נופרים בגבעת אלונים (דר נופרים) 2,775,000 [yad2] |
| קריית גת | 4 | HAKEREM כרמי גת צפון (אמפא ישראל, קבוצת גשם ונפתלי ניסן) 1,190,000 [yad2] | רייסדור כרמי גת (רייסדור) 2,023,000 [yad2] |
| אופקים | 3 | אפי באפיקי נחל, אופקים (אפי קפיטל) 1,390,000 [yad2] | סדרת המיני פנטהאוזים והפנטהאוזים בשכונת אפיקי נחל (מגידו י.ק.) 2,138,000 [yad2] |
| טירת כרמל | 3 | NEXT טירת הכרמל (עמרם את נידם התחדשות עירונית בעמ, עמרם אברהם) 1,690,000 [yad2] | סנטרל בוטיק (עמרם אברהם) 2,450,000 [yad2] |
| יהוד-מונוסון | 3 | ענב שדרת האומנות (ענב יזום ונדלן) 2,350,000 [yad2] | לינק מתחם אשכנזי יהוד מונסון (אאורה) 3,390,000 [yad2] |
| נתיבות | 3 | שיא הנחלה (ש.י.א רפאל פרויקטים בע"מ) 1,320,000 [yad2] | Reisdor Netivot (רייסדור) 2,088,000 [yad2] |
| ראש העין | 3 | רייסדור ראש העין (רייסדור) 3,216,700 [yad2] | premium collection – פרימיום קולקשן ראש העין (גיא - דורון לוי) 3,890,000 [yad2] |
| גבעת שמואל | 2 | VIDA (בית וגג ו-TOP במרחבי השרון) 2,800,000 [yad2] | רמת הדר החדשה (י.ח. דמרי) 3,790,000 [developer] |
| גני תקווה | 2 | המשי (קבוצת שבירו יזמות ובנייה) 3,060,000 [yad2] | שבירו בגני תקווה (קבוצת שבירו יזמות ובנייה) 3,390,000 [yad2] |
| מודיעין-מכבים-רעות | 2 | מורשת טל PREMIUM (מיטל הנדסה) 3,990,000 [yad2] | נתנאל בכרמים מודיעין (קבוצת נתנאל) 5,200,000 [yad2] |
| נס ציונה | 2 | רובע הנשיאים נס ציונה (קבוצת היזום והבנייה א.א רוטשטיין) 2,100,000 [yad2] | THE IRIS (גוהרי יוסי השקעות בע"מ) 2,990,000 [yad2] |
| קדימה-צורן | 2 | טופ השדות (TOP במרחבי השרון) 3,000,000 [yad2] | בן צבי קדימה (שפונדר-ריטוב) 3,300,000 [yad2] |
| רמלה | 2 | אבני חושן (אבני דרך וי.ד. ברזאני) 2,340,000 [news] | YOUNG PARK (עמרם אברהם) 2,390,000 [yad2] |
| בית שמש | 1 | רוטשטיין HEIGHTS (רוטשטיין) 2,580,000 [yad2] | - |
| בן שמן | 1 | חלומות בן שמן (שיכון ובינוי נדל"ן) 2,350,000 [yad2] | - |
| בני עי"ש | 1 | רייסדור בני עי"ש (רייסדור) 2,708,000 [yad2] | - |
| ג'סר א זרקא | 1 | טורקיז (גשם החזקות) 2,750,000 [yad2] | - |
| גדרה | 1 | ארבע אמהות גדרה (מיישבי הארץ) 4,390,000 [yad2] | - |
| גן יבנה | 1 | נופי השפלה (גבאי יזמות) 2,340,000 [yad2] | - |
| כפר יונה | 1 | מגדלי יפה נוף (קבוצת יצחקי בר) 2,350,000 [yad2] | - |
| כפר סבא | 1 | ענב 360 (ענב יזום ונדלן) 2,950,000 [yad2] | - |
| נשר | 1 | אגמי בראשית (אפריקה ישראל מגורים, שיכון ובינוי וכלל תעשיות) 1,690,000 [yad2] | - |
| עכו | 1 | AQUA PARK עכו (עמרם אברהם) 1,790,000 [yad2] | - |
| קריית ביאליק | 1 | אפקה בשמורה (י.ח. דמרי) 1,820,000 [developer] | - |
| תל מונד | 1 | Tel Mond Collection (בנימין זיגדון בע"מ) 5,290,000 [yad2] | - |

Source tags: [developer] = the developer's own page; [yad2] = the developer's Yad2 new-projects listing ("minPrice" = lowest listed unit);
[nadlan.com] = nadlan.com project page; [news] = dated article. Per-sqm prices: H-Infinity 65,000 (Hagag page), Zohi 70,000 presale
(news 30.1.2026), VOGUE 65,000 low end for the last penthouses (news 30.11.2025), Weizmann 49 55,000, Bnei Efraim 236-240 42,000,
Kitzis (Hagag Tzim) 39,000 (the last three from Yad2).

## How it was collected

1. Starting list: the SERP and AI overview of 25.10.2026 (`serp.md`) and the competitor notes in `competitors/`.
2. Developer sites (preferred source), fetched with curl and a browser user agent: Tidhar, Hagag, Acro, Bayit Vegag, Ken Hator, Socity,
   Y.H. Dimri, Israel Canada, Prashkovsky, Gindi (gindi.com), Gabay, Electra Residential, Aura (incl. Megido), Africa Israel Residences
   (+ Africa Urban Renewal), Shikun & Binui (shbn.co.il), Azorim, Levinstein, Rotshtein, Ampa, Ashtrom Residential, Briga, Almog,
   Almogim, Maoz Daniel, Kardan, BST, Avisror, Oron, Grofit, Bonim BaIr, Matzlawi and others. Every project page
   was opened, not only the hub.
3. Almost no developer publishes a price (see below), so prices were taken from the developer's own Yad2 new-projects listing.
   Yad2 blocks curl and WebFetch (Radware). It was read in the owner's Chrome ("gmktec"), from the page's embedded project data
   (`__NEXT_DATA__`, query `yad1-map`) for the regions Tel Aviv area (all 133 listings), Centre and Sharon (200 of 219 listings, priced rows),
   South, Jerusalem area and Northern coastal plain (priced rows). North and valleys was not read. Rental listings were dropped.
4. nadlan.com project pages (server-rendered) and dated news articles (nadlancenter.co.il, ice.co.il, bizportal, Israel Hayom) were used
   only where the developer page had nothing.
5. Agents merged duplicates (joint projects listed by two developers) and kept one record each.

Extra key: `extra_sources` (a list of `{url, type, fields}`) appears on every record. It names a second source and the exact fields taken
from it (for example a Yad2 price added to a record whose main source is the developer page). It is empty when every field came from
`source_url`. `read_at` is 2026-10-25 for every record.

Field notes:
- `price_from` from Yad2 is the lowest-priced unit listed in the project's Yad2 listing that day; `price_note` says "(יד2)".
- `status` for Yad2-only records: PRESALE / פריסייל wording -> presale; Yad2 immediate-occupancy flag -> immediate; occupancy date within
  12 months -> near_occupancy; "הבנייה בעיצומה / החלה הבנייה" -> construction; otherwise marketing.
- `delivery` from Yad2 is the listing's occupancy month (MM/YYYY). Developer dates are kept as written ("2028", "Q4/2027", "יוני 2030").
- `deal` is the payment-terms line as published (e.g. "תנאי תשלום 20/80", "10% בחוזה והיתרה באיכלוס"); slogans were not copied.
- `units` is sometimes the whole compound and sometimes the phase on sale; the private evidence file says which.
- `renewal` is filled only where the source names the track. Many renewal projects say only "התחדשות עירונית"; those are null.
- Neighbourhood names on Yad2-only records are Yad2's own (e.g. "הצפון החדש - כיכר המדינה").

## Developer sites that blocked, rendered only with JavaScript, or published no prices

Blocked or broken:
- yad2.co.il and madlan.co.il: bot check (Radware / puzzle) for curl and WebFetch. Yad2 was read in the owner's Chrome; Madlan was not used.
- calcalist.co.il: "Access Denied" to curl (two articles not read).
- gindi.co.il: expired TLS certificate and 404; the live site is gindi.com. Gindi's model pages render only with JavaScript.
- shikunbinui.co.il: TLS name mismatch; the residential sales site is shbn.co.il.
- Israel Canada (Wix): the project-list pages load by JavaScript; the homepage list and each project page were used.
- JavaScript-only (no text in HTML): rozio.com (Rozio, Ben Saruk 22-24 and Asaf 17), ydb.co.il (Y.D. Barazani), netanel.co.il,
  Yanuv project pages, rothschild10.com, miriam10-20.co.il.
- No working site found: Tzarfati Shimon (tzarfati.co.il does not resolve; its records come from news + Yad2), Shabiro (Yad2 only),
  Kidar, Erez-Tirosh, Av-Gad.
- wissotsky6.com (mini-site of Acro's Wissotsky 6) is hijacked and serves a gambling page: never link it. weizmann.co.il is parked for sale.

No prices on the developer's own site (price came from Yad2 where it lists the project, otherwise left empty):
Tidhar (Mivtza Sinai mini-site shows an empty "החל מ- ---- ₪" block), Hagag (only H-Infinity: 65,000 ₪/sqm), Acro, Bayit Vegag, Ken Hator,
Socity, Israel Canada, Gindi, Prashkovsky (only a quoted news headline), Gabay, Electra, Aura, Africa Israel, Shikun & Binui, Azorim,
Levinstein, Rotshtein, Ampa, Ashtrom Residential (empty price field in the page data), Briga, Almog, Almogim, Maoz Daniel, Kardan, BST,
Avisror, Oron, Grofit, Bonim BaIr, Matzlawi. Y.H. Dimri is the only developer that publishes from-prices (15 of its 18 apartment projects).

No records at all: Danya Cebus (its site shows only a Mechir Lamishtaken portfolio; it builds as a contractor), Oranim (SEA ONE is a 60+
deposit scheme, not a sale), "Zohi Sadeh" (not a developer: "זוהי" is the Sde Dov project of Levinstein, Metropolis and Mivne, recorded once).

## Conflicts between sources

Google AI overview (25.10.2026) against the sources read:
- "YAMA TLV from 8,700,000": wrong. 8,700,000 is Dimri's YAMA Ir Yamim in Netanya. The YAMA TLV page (Sde Dov) shows no price; news
  (nadlancenter 26.12.2025) gave 2 rooms from 3.75M and company reports an average of 82,600 ₪/sqm incl. VAT (15.4.2026). Not used.
- "Rova Nordau Netanya from 2,380,000": wrong. Dimri's page and Yad2 both say 2,155,000; 2,380,000 is Dimri's Neve Or in Or Yehuda.
- "HaSolelim 4-6 rooms from 4,983,000": Tidhar's page and the project site show no price; Yad2 shows from 4,990,000 today
  (rooms: Tidhar's plans 2-6, project site "4 or 5 rooms"). Recorded 4,990,000 from Yad2.
- "Shabiro Glil Yam from 3,450,000": Yad2 shows 3,300,000 today (3 rooms, immediate). Recorded 3,300,000.
- "Galipolis from 3,215,000 (presale)": matches Yad2; Almog's page has no price; news (nadlancenter 16.1.2026) gave 2 rooms from 2.92M at launch.
- "Herzliya Hayeruka from 4,100,000": identified on Yad2 as "הרצליה הירוקה" by Rinovo (Hanadiv 51), 4,100,000. Recorded from Yad2.
- "Ben Saruk 22-24 from 6,890,000": not in Yad2's data today and the developer site (Rozio) is JavaScript-only. Not recorded.
- Matching the AI overview / Yad2 cards exactly: Bloch 10 (6,150,000), Remez 36 (5,900,000), Nahalat Yitzhak 17-19 (3,680,000),
  PATIO Ben Shemen (2,390,000), Afikei Hanahal (1,400,000 on Dimri's page), Tel Aviva (2,481,600), HaRa'ah 277-279 (2,987,000),
  Bnei Efraim 236-240 (4,550,000; 42,000 ₪/sqm), Electra Life Style Park Afel (2,550,000), GINDI TLV (5,200,000), LA-MER (3,500,000),
  CENTRAL Bat Yam (2,380,000; developer A.A. Rotshtein, not Rotshtein Nadlan), Asaf 17 (3,700,000), SEA&PARK (3,190,000).
- "Ma'avar LaKikar, Jabotinsky 133-137" (Yad2, Bayit Vegag, from 3,930,000): Africa Urban Renewal lists Jabotinsky 135-137 (TAMA 38, with
  Bayit Vegag) as in marketing, and Bayit Vegag lists 133 and 135-137 as "coming soon". The Yad2 price, 10%-at-signing term and 02/2029
  date were attached to the 135-137 record.

Inside developer sites and news (fields left as noted):
- Dimri Harmony (Ashdod): floor counter "535" vs text 36 (36 used); units counter 750 vs text 684 (750 used). River Park: 8 vs 9 floors.
- Tidhar Tzameret Dan: header 2 buildings / 217 units vs body one tower / 117 units (header used). Sharet: Tidhar "Old North", Acro "New North".
- Weizmann 80-88: Acro says in marketing and under construction; Ken Hator says occupied and sold out. Left out.
- Ashtrom: Zichron Yaakov 7 units 13 (page) vs 29 (card); Lamedan 15 floors 8 vs 9; Borokhov 14 and 24 show identical stats (copy-paste on the site).
- Rotshtein: VALLEY Tirat Carmel and the Be'er Yaakov cottages are "in marketing" on the homepage but "occupied" on their pages.
- Gabay O-Live: 56 units (project page) vs 66 (renewal page). DUO: 50 floors (developer) vs 54 floors / 668 units (2024 news); 50 kept, units empty.
- Electra Park Afel phase A: label "in marketing", but construction began (Feb 2024 news on the same page); recorded as construction.
- VOGUE (Gindi, Sde Dov): launch price 49,000 ₪/sqm (6.2025) is out of date; by 30.11.2025 692 of 708 were sold and the last penthouses were
  at 65,000-80,000 ₪/sqm. No developer page was found for it (news source).
- nadlan.com: Groffit BaShmura structured price 4,150,000 vs text 3,900,000 (text used); Shamayim VaAretz 2,275,000 vs 2,295,000 in body;
  Brenda 11 price typo "2,490,00" (left empty); some nadlan.com pages are stale (e.g. Park Afel still "pre-permit").
- Lipsky 18 (Bayit Vegag): the only price found is "2 rooms from 3.7M" in a January 2024 article; too old, not used.

### Price differences found while merging (developer page or news vs Yad2, 25.10.2026)

- סנטרל פארק / CENTRAL PARK 17 (באר שבע): דמרי ואזורים מציגים את אותו מתחם כל אחד באתרו (דמרי: 270 יח"ד, 29 קומות; אזורים: "למעלה מ-540 משפחות כבר גרות"). יד2 מציג אותו כפרויקט משותף. נרשם פעם אחת.
- SEVEN SEAS (תל אביב-יפו): כ-80,000 ₪ למ"ר הוא ממוצע מכירות מדוחות אלקטרה (מרכז הנדל"ן 25.3.2026), לא מחיר החל-מ; הושמט מהשדה.
- ארז-תירוש, דוד אלעזר (רעננה): 32-36 אלף ₪ למ"ר הוא מחיר עסקה סיטונאית של 8 דירות (מרכז הנדל"ן 3.8.2025), לא מחירון; הושמט. מחיר יד2 נכנס במקומו.
- נווה פארק (פתח תקווה): מחיר החל-מ במקור (developer): 2,695,000 ; ביד2 היום: 2,750,000. נשאר מחיר המקור.
- הרימון (קריית אונו): מחיר החל-מ במקור (portal): 3,350,000 ; ביד2 היום: 3,900,000. נשאר מחיר המקור.
- נווה אור (אור יהודה): מחיר החל-מ במקור (developer): 2,380,000 ; ביד2 היום: 2,440,000. נשאר מחיר המקור.
- צרפתי בנאות הדרים (באר שבע): מחיר 1,620,000 (3 חד', שלב ג', מרכז הנדל"ן 24.1.2025) הוחלף במחיר יד2 הנוכחי
- הרמוני (אשדוד): מחיר החל-מ במקור (developer): 1,840,000 ; ביד2 היום: 2,820,000. נשאר מחיר המקור.
- מגדלי עיר היין (אשקלון): מחיר החל-מ במקור (developer): 1,860,000 ; ביד2 היום: 1,850,000. נשאר מחיר המקור.
- רמות אשקלון (אשקלון): מחיר החל-מ במקור (developer): 1,700,000 ; ביד2 היום: 1,940,000. נשאר מחיר המקור.
- סנטרל פארק (באר שבע): מחיר החל-מ במקור (developer): 1,700,000 ; ביד2 היום: 1,750,000. נשאר מחיר המקור.
- פרשקובסקי ברובע המיוחד, קרית פרס (אשדוד): עמוד היזם מצטט כותרת חדשות "דירות החל מ-1.9 מיליון"; יד2 (רישום היזם) מציג היום החל מ-2,912,000; נרשם מחיר יד2
- SEA&PARK (בת ים): מחיר 3,050,000 (3 חד', ice.co.il 1.7.2024) ותנאי 15/85 + הלוואה (2024) הוחלפו במחיר יד2 הנוכחי
- אפקה בשמורה (קריית ביאליק): מחיר החל-מ במקור (developer): 1,820,000 ; ביד2 היום: 2,190,000. נשאר מחיר המקור.

