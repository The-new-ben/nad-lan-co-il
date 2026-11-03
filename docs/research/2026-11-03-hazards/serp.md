# What Google shows in Israel for the 6 biggest hazard terms

Pulled 3.11.2026 at 19:53 UTC (21:53 Israel time).

**Setup.**
- Endpoint: DataForSEO `POST /v3/serp/google/organic/live/advanced`.
- Location 2376 (Israel), language "iw", desktop, depth 10, `load_async_ai_overview: true`.
- 6 calls in total.

**How the 6 terms were chosen.** They are the biggest on-topic terms in `keywords.md`, with one change. "מדד זיהום אוויר" (1,000) was swapped for "בדיקת אנטנה סלולרית" (390). The reason: three air-pollution SERPs would repeat one intent, and this term has the highest CPC in the set ($19.16).

**How to read this file.**
- **Rank.** Positions are DataForSEO `rank_absolute` and count every SERP block. Organic order is shown as O1, O2 and so on.
- **Redirect wrappers.** Many organic URLs came back as `google.com/goto?...` wrappers. For those we record the breadcrumb (site and path) Google showed, not an invented final URL.
- **People Also Ask (PAA).** "Absent" means no PAA block appeared within the returned first page (depth 10).

---

## 1. זיהום אוויר (6,600 a month)

**AI Overview: present** (position 1).
- **What it says.** You can follow real-time data and air-quality indices through the Ministry of Environmental Protection's monitoring site, or check the forecast portal. It defines air pollution and lists the main sources: industry, transport, power stations, and Sahara dust. On Israel it gives about 5,510 early deaths in 2023 and about 22.5 billion NIS of economic damage in 2023, figures from the ministries' report. It mentions health effects (asthma, heart disease, dementia research) and ends by offering to cover "specific pollution sources in your area" and the Clean Air Law.
- **Cites:** air.sviva.gov.il; gov.il/apps/sviva/airq (forecast); mdec.co.il (Daliyat al-Karmel council); he.wikipedia.org; pop.education.gov.il; i24news.tv; greenpeace.org/israel; volta.solar; makorrishon.co.il.

**Top organic results.**

| # | Title | Site and URL |
|---|---|---|
| O1 | זיהום אוויר | infospot.co.il › scp › זיהום_אוויר |
| O2 | כל מה שלא ידעתם על זיהום אוויר בעולם | volta.solar/knowledge-center/… (Volta Solar) |
| O3 | הלמ"ס פרסמה מדד איכות אוויר: חריגות מערכי היעד | http://infospot.co.il/n/Air_quality_index |
| O4 | זיהום אוויר בישראל (video) | YouTube · זווית |
| O5 | זיהום אוויר עירוני - אקולוגיה וסביבה | magazine.isees.org.il › הסביבה הבנויה |
| O6 | מדד איכות אוויר בירושלים, מחוז ירושלים, ישראל | accuweather.com › air-quality-index |
| O7 | מדידה והערכה של איכות האוויר (ניטור) (מושג) | kolzchut.org.il › מדידה_והערכה_של_איכות_האוויר_(ניטור) |
| O8 | זיהום אוויר \| פורטל איכות הסביבה | environmentindex.com › inquiry |
| O9 | זיהום אוויר גבוה נמדד ברחבי הארץ - כך תימנעו מהסכנות | israelhayom.co.il/news/environment/article/19765523 |

Only 9 organic results were returned in depth 10.

**People Also Ask: present** (position 11). The questions:
1. מהו דירוג זיהום האוויר?
2. איך יודעים שיש זיהום בגוף?
3. איך מדווחים על זיהום אוויר?
4. איפה אני יכול למצוא תחנות ניטור זיהום אוויר בישראל?

**Related searches:** זיהום אוויר בירושלים היום · זיהום אוויר עכשיו תלפיות ירושלים · זיהום אוויר תל אביב עכשיו · זיהום אוויר בישראל היום · זיהום אוויר בישראל לפי ערים · זיהום אוויר בישראל מפה · ישראל זיהום אוויר · זיהום אוויר מודיעין.

---

## 2. אנטנה סלולרית (2,400 a month)

**AI Overview: present** (position 1, with an image strip).
- **What it says.** As of August 2026 about 8,768 cellular antennas are registered in Israel, 8,368 active and 400 under construction. It lists the site types: ground masts, rooftop, small cells, "sting" antennas and wireless access points. Its radiation claim is "radiation levels are supervised under strict standards (measured values typically 78.4 to 98.4)". That number pair is quoted as shown; it is unexplained and looks garbled.
- **Tools it names:** the spectrum.fit address map, the ArcGIS "cellular antennas dashboard", and the mihachi.co.il coverage map.
- **Cites:** spectrum.fit (מפת אנטנות סלולריות לפי כתובת); arcgis.com/apps/dashboards/361fb3cf9857422b8bab4a908fb2ae2b; mihachi.co.il.

**Top organic results.**

| # | Title | Site and URL |
|---|---|---|
| O1 | בדיקת קליטה סלולרית לפי כתובת - איזה חברה הכי טובה באזור שלך | zolsim.co.il/he/blog/cellular-network-coverage-check-israel |
| O2 | מפת הכיסוי הסלולרי: כמה אנטנות יש בעיר שלכם ואיפה הן ממוקמות? (11.4.2024) | ynet.co.il › economy › article (ynet.co.il/economy/article/by08kjsea) |
| O3 | תשתיות אנטנות הסלולר בישראל (7.1.2016) | knesset.gov.il › data › mada2016-01-11 |
| O4 | בדיקת קליטה סלולרית לפני שחותמים על חוזה: המדריך המלא | xphone.co.il/cellular-coverage-check |
| O5 | איזה אנטנות סלולריות יש ואיך לבדוק מה האנטנה הכי קרובה? (6.2.2021) | tiber.co.il › כל הכתבות |
| O6 | אנטנות סלולריות - תנודע Tnuda (31.1.2016) | tnuda.org.il/אנטנות-סלולריות |
| O7 | אנטנות סלולריות (municipal map page) | yavne.muni.il/אנטנות-סלולריות/ |
| O8 | אנטנה סלולרית 210282 - נס הרים - אנטנת פלאפון | easy.co.il › page |
| O9 | איך אנטנות סלולריות חכמות משפרות את כיסוי הרשת בערים צפופות (1.6.2025) | bell.co.il › smart-cellular-coverage |

**People Also Ask: absent.**

**Related searches:** אנטנות סלולריות לפי כתובת · מפת אנטנות סלולריות 5g · אנטנה סלולרית לבית · אנטנה סלולרית למקלט · מפת אנטנות סלולריות בישראל · בדיקת עוצמת קליטה סלולרית · מפת אנטנות סלולריות המשרד להגנת הסביבה · פלאפון.

---

## 3. מפת אנטנות סלולריות (1,300 a month)

**AI Overview: present**, at position 3, after two organic results.
- **What it says.** It opens: several interactive tools let you check antenna locations, radiation permits and network coverage in Israel by address. It then lists the tools below and offers to look up "your exact address".
- **Tools it names:**
  - the spectrum.fit address map (active and future sites, by operator and generation, including 5G);
  - the ArcGIS dashboard (operation data, site types, measured radiation values);
  - nPerf (crowd-sourced 2G to 5G coverage);
  - mihachi.co.il (coverage and prices);
  - the Ministry of Communications "transparency" page at gov.il/he/pages/10042024_1 (coverage per address).
- **Cites:** spectrum.fit; arcgis.com dashboard; nperf.com/he/map/IL/-/-/signal; mihachi.co.il; gov.il/he/pages/10042024_1.

**Top organic results.**

| # | Title | Site and URL |
|---|---|---|
| O1 | כיסוי תשתיות הסלולר בישראל: כלי נתונים מתעדכן | isoc.org.il/sts-data/cellula-communication-infrastructure-israel |
| O2 | כל מה שחשוב לדעת על אנטנות הסלולר בישראל - המדריך המלא (11.3.2025) | smartcut.co.il/cellular-antennas-in-israel/ |
| O3 | אנטנות סלולריות ביקום — 6 אתרים, מפה ורשימה - נתונים | netunim.co.il › ממשל וזכויות › אנטנות סלולריות (programmatic per-locality pages) |
| O4 | איזה אנטנות סלולריות יש ואיך לבדוק מה האנטנה הכי קרובה? | tiber.co.il › כל הכתבות |
| O5 | אתר חדש מציג את מפת הכיסוי הסלולרי בישראל (14.4.2024) | haboreret.co.il › תקשורת › סלולר |
| O6 | מפת כיסוי 3G / 4G / 5G Haifa… | nperf.com › map › 294801.Haifa › signal |
| O7 | Search (tags: אנטנות סלולריות) | arcgis.com › home › search |
| O8 | אנטנות סלולריות | easy.co.il/list/Cell-Tower-Location |

8 organic results; an Images block sits at position 7.

**Images block sources:**
- norad4u.co.il (antenna maps page);
- hof-hacarmel.co.il and ramat-hasharon.muni.il (council antenna pages);
- ynet "מפת הכיסוי הסלולרי";
- ynet "דור 5 בישראל: מדוע סלקום מסתירה את הפריסה שלה?";
- ynet "אתר חדש ימצא לכם מפגעים ליד הבית".

**People Also Ask: absent.**

**Related searches:** מפת אנטנות סלולריות 5g · אנטנות סלולריות לפי כתובת.

---

## 4. קרינה (1,300 a month, generic)

**AI Overview: present** (position 1).
- **What it says.** Radiation is energy emitted by matter that spreads as waves or particles. It explains ionizing radiation (X-ray, gamma, alpha, beta, part of UV) and non-ionizing radiation (visible light, infrared, microwave, radio, "found in home devices, antennas and cell phones"). Then three tracking topics: the UV index from the Israel Meteorological Service, car radiation (the ministry's periodic measurements of new cars), and phone radiation (SAR, signal strength). It ends by asking whether you mean "cellular or electrical radiation at home", sun radiation, or a test of a device or car.
- **Cites:** he.wikipedia.org (קרינה); kolzchut.org.il (חולים נפגעי קרינה); weizmann.ac.il; cancer.org.il/articles/6789; itlglobal.org; ims.gov.il/he/UVIHourly; mako.co.il (car-radiation table, Q4 2026).

**Top organic results.**

| # | Title | Site and URL |
|---|---|---|
| O1 | קרינה בלתי מייננת | he.wikipedia.org › wiki › קרינה_בלתי_מייננת |
| O2 | אינדקס קרינה UV - מתי באמת מסוכן (11.11.2025) | cancer.org.il › articles |
| O3 | בטיחות קרינה | gov.il › radiation-safety › govil-landing-page |
| O4 | סיכוני קרינה מייננת \| Safety Unit | weizmann.ac.il/safety/he/safety-subjects/radiation-safety/risks-ionizing-radiation |
| O5 | מדוע קרינה מסוכנת | galit.co.il/מדוע-קרינה-מסוכנת/ (גלית החברה לאיכות הסביבה) |
| O6 | מהי קרינה \| גלית החברה לאיכות הסביבה | galit.co.il › מאמרים › הכל על קרינה |
| O7 | סיכונים וניתוח קרינה אלקטרומגנטית | osh.org.il › uploadfiles › d_1719_krina (PDF) |
| O8 | סוגי קרינה מייננת \| Safety Unit | weizmann.ac.il/safety/he/safety-subjects/radiation-safety/types-ionizing-radiation |

8 organic results; an Images block sits at position 5. Its sources include radshield.co.il, radon.co.il and a ynet piece on a home radiation meter.

**People Also Ask: absent.**

**Related searches:** קרינה מייננת · אינדקס קרינה עכשיו · אינדקס קרינה שבועי · אינדקס קרינה לשיזוף · אינדקס קרינה מחר · אינדקס קרינה ירושלים · **האם קרינה בלתי מייננת מסוכנת** · אינדקס קרינה שבת.

---

## 5. זיהום אוויר בישראל לפי ערים (1,000 a month)

**AI Overview: absent.**

**Images block at position 1.** Sources:
- mako/N12 "דוח סודי: הערים המזוהמות בישראל";
- gov.il "אוויר בסביבה" app page (gov.il/he/pages/new_air_quality_app);
- sviva-sc.org.il 2022 summary;
- eco-wiki;
- gov.il ministry warning page;
- ynet;
- Instagram;
- isees.

**Top organic results.**

| # | Title | Site and URL |
|---|---|---|
| O1 | אתר חדש מציג נתוני איכות אוויר (2.2.2021) | infospot.co.il › A_new_site_that_displays_air_qu… |
| O2 | הכירו את אתר מערכת ניטור האוויר החדש שלנו! (video) | Facebook · המשרד להגנת הסביבה |
| O3 | איכות אויר - איגוד ערים לאיכות הסביבה שומרון | shomron.enviosh.org.il/201/ |
| O4 | זיהום אוויר עירוני - אקולוגיה וסביבה | magazine.isees.org.il › הסביבה הבנויה |
| O5 | חישוב מדד איכות האוויר (PDF) | air.sviva.gov.il/Pagesfiles/…AQI….pdf |
| O6 | מדד איכות הסביבה | idi.org.il › indexes › environment-index |
| O7 | מדדי זיהום אויר | k-8.co.il (Kiryat Shmona municipality, environmental unit) |
| O8 | מערך הניטור ומצב איכות האוויר בשנת 2022 | sviva-sc.org.il › מחלקת ניטור אוויר |
| O9 | מדד איכות אוויר בירושלים… | accuweather.com › air-quality-index |

**People Also Ask: absent.**

**Related searches:** זיהום אוויר עכשיו · זיהום אוויר בישראל היום · זיהום אוויר בישראל לפי ערים 2024 · זיהום אוויר בישראל לפי ערים 2023 · זיהום אוויר חיפה · איכות האוויר באר שבע · זיהום אוויר מודיעין · ישראל זיהום אוויר.

**Finding.** No page ranks with an actual table of cities. Google fills the SERP with old news items, council pages and a PDF. This is a clear content gap: a dated city table built from the ministry's monitoring data.

---

## 6. בדיקת אנטנה סלולרית (390 a month, CPC $19.16)

**AI Overview: present** (position 2, after a Facebook post).
- **What it says.** To check antennas, signal strength and coverage by address there are free official tools built on the Environmental Protection and Communications ministries' data. It then lists tools in three groups and names the three infrastructure groups: Pelephone, PHI (Partner and HOT), and Cellcom (with WeCom).
- **Tools it names:**
  - by address: tiber.co.il/Home/Antenna and kamazeole.co.il/cellular-reception-checker (number of active antennas, distance to the nearest, generations);
  - the official map: govmap.gov.il/sviva and the ArcGIS ministry dashboard;
  - crowd coverage: nPerf.
- **Cites:** spectrum.fit; kamazeole.co.il; tiber.co.il; govmap.gov.il/sviva; arcgis.com dashboard; nperf.com.

**Top organic results.**

| # | Title | Site and URL |
|---|---|---|
| O1 | יש קליטה סלולרית אצלכם בבית? לפני שבוחרים חבילת סלולר | facebook.com/tibercashback/posts/… |
| O2 | כיסוי 3G / 4G / 5G ב- Tel-Aviv… | nperf.com › 293397.Tel-Aviv › signal |
| O3 | מפת כיסוי סלולרי ישראל 2025 - בדקו את איכות הקליטה בכל אזור (29.5.2025) | zolzolzol.co.il › post |
| O4 | מפת אנטנות סלולריות לפי כתובת בישראל \| Watch My Health | cellular.wmh.co.il/ |
| O5 | אנטנות סלולריות - תנודע Tnuda | tnuda.org.il › אנטנות-סלולריות |
| O6 | רשת הסלולר המובילה באזור שלכם | binyamin.org.il › המועצה › שירות לתושב |
| O7 | בדיקת אנטנות סלולריות ליד בית: מה לבדוק? (7.5.2026) | afikil.co.il/real-estates/… (מכללת אפיק, real-estate section) |
| O8 | כל מה שחשוב לדעת על אנטנות הסלולר בישראל - המדריך המלא | smartcut.co.il › כתבות וסקירות › סלולר |

8 organic results.

**Images block** at position 10. Sources:
- bedikat-krina.co.il (אינג' ליאור ברסלר);
- a YouTube short on radiation testing;
- midrag.co.il/Content/Tip/5238 ("כל מה שרציתם לדעת על בדיקת קרינה סלולרית");
- spectrum.fit;
- afikil;
- tgspot.co.il;
- bizzness.net;
- norad4u.co.il.

**People Also Ask: absent.**

**Related searches:** אפליקציה לבדיקת קליטה סלולרית · רשת סלולרית 5g · רשת סלולר הכי טובה · אנטנה להגברת קליטה סלולרית · Tiber סלולר · בדיקת קליטה אינטרנט · מפת סלולר · תשתיות סלולר בישראל.

---

## Cross-SERP findings

1. **AI Overviews appear on 5 of the 6 terms.** The only one without is "זיהום אוויר בישראל לפי ערים".
2. **spectrum.fit owns the antenna AI answer.** It is cited in all 3 antenna AI Overviews and is the source of the "8,768 antennas, August 2026" fact. The AI picks dated, numbered facts plus an FAQ.
3. **Antenna SERPs are reception-shopping SERPs.** Zolsim, Xphone, Tiber, nPerf, mihachi and zolzolzol are all telecom deal or coverage sites. Health and home-buying intent is served only by tnuda (2016 to 2018 content), afikil (thin) and bedikat-krina and midrag (images only).
4. **No real-estate portal ranks for any of the 6 terms.** No page combines antennas with power lines, transformers, air, noise or industry. The one multi-hazard idea in the SERP is an old ynet image, "אתר חדש ימצא לכם מפגעים ליד הבית", about the "סביבתי" site of Adam Teva V'Din and Tel Aviv University.
5. **People Also Ask appears only on "זיהום אוויר".** It shows 4 questions, including "איך מדווחים על זיהום אוויר?" and "איפה … תחנות ניטור … בישראל?".
6. **Official tools are cited but never explained.** govmap/sviva, the ministry's ArcGIS dashboard, air.sviva.gov.il and the gov.il forecast all appear in AI Overviews, but no page teaches how to read them together for one address.
