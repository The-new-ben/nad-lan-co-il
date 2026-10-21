# Sde Dov district: environment research (Mission B)

Research for the "environment" section of https://nad-lan.co.il/sde-dov/contamination/. Compiled 21.10.2026. Every number, its source URL and retrieval date are in `facts.json` (ids W, A, S, G below). Nothing on the site was changed and nothing was committed. No project or company names appear here.

## Summary (English)

- **Wind (W1-W11).** Two data sets. The airport's own weather reports at Sde Dov (NOAA ISD 401762, 2009-2018, daytime only, about 05:00-22:00) and the IMS station "Tel Aviv Coast" (2410, 6.5 km SSW, 2016-2025, day and night, 3-hourly). Over the year about 61% of observations are wind from the sea side (SSW through N). In summer this rises to 75% (airport, daytime) and 80% (IMS). The summer cycle is a textbook sea breeze. A weak south-east land breeze blows at dawn (about 2 m/s). It turns onshore by 09:00 and peaks at 4.8-5.25 m/s (17-19 km/h) from the west around 14:00-15:00. It then veers to the north-west and eases in the evening. In winter 53% of observations are from the land side (ESE/SE), mostly at night and in the morning. Winds of 8 m/s or more make up 6.9% of winter observations, and 89% of them come from SW to WNW. Wind-rose data ready to draw: `windrose.csv` (IMS, speed bins), `windrose_sectors.csv` (both stations, 16 sectors per season), `wind_diurnal_*.csv`.
- **Air (A1-A7).** The nearest monitoring station is Shikun L (Israel Electric Corp., 0.8 km ESE, PM10 only): 39.0 ug/m3 annual in 2023 against the Israeli 50 (data availability 78%). At HaTzafon HaHadash (3.0 km S) in 2023: NO2 19.7 against 40, PM2.5 17.8 against 25 (8 daily exceedances), ozone with no 8-hour exceedance. All of these are below the Israeli environmental values. They are above the stricter WHO 2021 guidelines (PM2.5 5, NO2 10, PM10 15), as is the air of 97% of EU city dwellers for PM2.5. Tel Aviv municipality reports 3-15 daily PM2.5 exceedances per station in 2024 (18 allowed). The Reading power station, about 1 km SSW, stopped generating in 2020. The two nearest Ministry stations (University 2.1 km, Yehuda Maccabi 2.2 km) have no annual figures here: **not found** (see `not_found`).
- **Sun and sea (S1-S5).** The shoreline runs about 17.6 deg (NNE-SSW). A facade facing about 288 deg faces the sea square-on, and the nearest shore is about 440 m from mid-district. Sunset falls between azimuth 242 and 299 deg over the year, so it is over the sea in every season. Sunrise is always over land. 21 June: 05:35-19:50, 14 h 15 min, noon sun 81 deg. 21 December: 06:37-16:40, 10 h 03 min, noon sun 34 deg (computed, matches timeanddate within 1 minute). On tower shade we give general guidance only. The Ministry's 2015 planning guide calls for a shade study above 8 floors (facades 135-225 deg, sun hours 09:00-15:00) and a pedestrian wind study from 11 floors. No district-specific shade study was found.
- **Groundwater (G1-G3).** The district sits on the coastal aquifer. Ground is 4-10 m above sea level and the water table about +0.5 m (Water Authority map 2016), so groundwater lies 3.5-9.5 m deep. The upper part is sand and sandy clay over kurkar. No drinking water is pumped here, and none is expected (Water Authority, 2023). Newer 2023 level rasters exist on data.gov.il but the download was blocked (403): **not found**.

## Caveats

- The airport record has almost no night hours. Use the IMS station for 24-hour shares and the airport record for "on-site, daytime".
- IMS times are read as UTC (WMO synoptic hours). The IMS explanation file needs a sign-in, so it was not opened. The match with the UTC-stamped airport record supports the reading.
- Air figures are for 2023, the latest annual report found. Ministry-run stations: not found.
- Distances and bearings are from one mid-district point (32.1125N, 34.7841E). The district is about 2 km long north to south.

## Files

| File | What |
|---|---|
| `facts.json` | every value with source URL, date, method; `not_found` list with where we looked |
| `windrose.csv` | IMS Tel Aviv Coast 2016-2025: season x 16 sectors x 5 speed bins (% of observations) + calm |
| `windrose_sde_dov_metar.csv` | Sde Dov airport 2009-2018 daytime: same layout + variable + calm |
| `windrose_sectors.csv` | both stations, season x 16 sectors (% total), easiest to draw |
| `wind_diurnal_ims.csv`, `wind_diurnal_sde_dov_metar.csv` | mean direction, speed and sea/land shares by hour and season (sea-breeze cycle) |
| `air_stations.csv` | stations within 6.5 km: distance, bearing, operator, pollutants, 2023 values found |
| `sun_tel_aviv_2026.csv` | sunrise/sunset, azimuths, noon altitude, day length, 21st of each month + equinoxes/solstices |
| `raw/` | IMS and NOAA wind extracts, OSM coastline points, JSON summaries |
| `scripts/` | the four scripts that produced the tables (inputs were downloaded to the session scratchpad) |

## Hebrew draft for the page (about 430 words)

Checked against the language-dna blacklist: no direction letters, no long dashes, no project or company names. Every number maps to `facts.json`.

## רוח, אוויר, שמש ומי תהום ברובע שדה דב

רובע שדה דב שוכן על קו החוף של צפון תל אביב, ומרכזו נמצא כ-440 מטר בלבד מקו המים. הקרבה לים קובעת כאן את הרוח, את האור ואת מה שמתחת לקרקע.

### הרוח: בריזה מהים בימי הקיץ

בתחנת "תל אביב חוף" של השירות המטאורולוגי, בשנים 2016 עד 2025, 61% מהתצפיות היו של רוח שמגיעה מכיוון הים, ובקיץ 80%. ברוב בקרי הקיץ נושבת רוח יבשתית חלשה מדרום-מזרח, כ-7 קמ"ש. עד 09:00 הרוח כבר מסתובבת אל הים. בצהריים היא נושבת ממערב, אחר הצהריים מגיעה לכ-17 קמ"ש, ולקראת הערב נעה לצפון-מערב ונחלשת. בחורף 53% מהתצפיות הן של רוח מזרחית ודרום-מזרחית מהיבשה, בעיקר בלילה ובבוקר. הרוחות החזקות, 29 קמ"ש ומעלה, נרשמו ב-7% מתצפיות החורף, ו-89% מהן הגיעו מהים, מדרום-מערב עד מערב-צפון-מערב. רשומות תחנת שדה התעופה עצמה מהשנים 2009 עד 2018 מראות את אותה תמונה בשעות היום: בקיץ 75% מהדיווחים הם של רוח מהים, בשיא של כ-19 קמ"ש בשעה 14:00.

### האוויר: מתחת לערכי הסביבה בישראל

תחנת הניטור הקרובה ביותר, בשכונת ל', נמצאת כ-800 מטר מזרחית לרובע ומודדת חלקיקים נשימים. ב-2023 נמדד בה ממוצע שנתי של 39 מיקרוגרם למ"ק, מול ערך סביבה של 50. בתחנת הצפון החדש, כ-3 ק"מ דרומה, נמדדו באותה שנה 19.7 מיקרוגרם למ"ק של חנקן דו-חמצני מול ערך של 40, ו-17.8 מיקרוגרם למ"ק של חלקיקים עדינים מול ערך של 25, ולא נרשמה שם חריגה מתקן האוזון. ההנחיות של ארגון הבריאות העולמי מ-2021 מחמירות יותר: 5 מיקרוגרם לחלקיקים עדינים ו-10 לחנקן דו-חמצני. ב-2021 היו 97% מתושבי הערים באיחוד האירופי חשופים לחלקיקים עדינים מעל ההנחיה הזו. תחנת הכוח רדינג, כקילומטר דרומית למרכז הרובע, עברה לגז ב-2006 והפסיקה לייצר חשמל ב-2020.

### שמש וים: השקיעה מעל הים בכל עונה

קו החוף נמתח מדרום לצפון בזווית קלה מזרחה, ולכן חזית הפונה מערבה, מעט צפונה, מביטה ישר אל הים. השמש שוקעת מעל הים בכל ימות השנה: ב-21 ביוני בשעה 19:50 בצד הצפון-מערבי, וב-21 בדצמבר בשעה 16:40 בצד הדרום-מערבי. הזריחה תמיד מעל היבשה: ב-21 ביוני בשעה 05:35 וב-21 בדצמבר בשעה 06:37. היום הארוך בשנה נמשך 14 שעות ורבע, והקצר כ-10 שעות. בצהרי יוני השמש עומדת 81 מעלות מעל האופק, ובדצמבר 34 מעלות בלבד, ולכן בחורף הצל של בניינים גבוהים ארוך יותר. לפי המדריך לתכנון סביבתי של המשרד להגנת הסביבה, תכנית לבניינים מעל 8 קומות מלווה בבחינת הצללה, ותכנית לבניינים של 11 קומות ומעלה גם בבחינת השפעת הרוח ברחובות ובשטחים הפתוחים.

### מי התהום: 3.5 עד 9.5 מטר מתחת לפני הקרקע

הרובע יושב מעל אקוויפר החוף. גובה הקרקע בשטח הוא 4 עד 10 מטר מעל פני הים, ומפלס מי התהום כחצי מטר מעל פני הים, כך שמי התהום נמצאים בעומק של 3.5 עד 9.5 מטר, לפי הטופוגרפיה. בחלק העליון חול וחרסית חולית לסירוגין, ומתחתם כורכר. בגלל הקרבה לים לא שואבים כאן מי שתייה, וגם בעתיד לא צפויה שאיבה כזו. חפירה מתחת למפלס מי התהום, למשל לחניון תת-קרקעי, נעשית לפי הנחיות המשרד להגנת הסביבה, הכוללות דיגום ואישור לפני פינוי הקרקע.
