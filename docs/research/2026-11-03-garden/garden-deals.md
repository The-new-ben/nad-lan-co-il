# Garden apartments (דירת גן) in Tel Aviv-Yafo: Tax Authority deals

Computed 2026-11-03 by `scratchpad/garden/garden_deals.py` from the file below. Every number in this file comes from that file; nothing is estimated.

- **Source file:** `C:\Users\777\Documents\Codex\2026-08-27\https-www-nadlan-gov-il-https\platform\data\raw\tlv-citywide\tlv-deals.csv`
- **Origin:** Tax Authority deals, big-cities export from odata.org.il (see bigcities.url in the same folder); file saved 2026-09-06
- **Filter:** `DEALNATUREDESCRIPTION == 'דירת גן'` (the property-type column; the value is exactly `דירת גן`)
- **Area:** DEALNATURE (holds the area in m2 in this export; checked against rooms). **Price:** DEALAMOUNT (NIS, nominal, not inflation-adjusted). **New:** `NEWPROJECTTEXT == '1'`
- **Whole file:** 100,780 rows, 1998-01-01 .. 2024-09 (dense to 2024-08, thin in 2024-09); 3 stray later rows, one future-dated (2026-11-30)
- **Garden deals period:** 2001-10-15 .. 2024-08-28 (no garden deal after August 2024 is in the file)
- **Neighbourhood placement:** deal block-parcel (POLYGON_ID) matched to `addresses.geojson` (ms_gush, ms_chelka), centroid tested against `neighborhoods.geojson` (71 polygons): {'gush-helka match': 246, 'street+number match': 2}
- **Median rule:** median shown only when >=5 deals; price per m2 only where area >=20 m2
- **Outlier rule:** rows whose price per m2 is under 30% or over 3x the same-year citywide median for ordinary flats are listed in flagged_rows and left out of every aggregate. Rows kept: 227 of 248.
- Prices are nominal shekels (not inflation adjusted). The file has no garden size, no ממ"ד flag and no partial-share flag.

## Headline

| Set | Deals | Median price ₪ | Median ₪/m² | Median built m² |
|---|---|---|---|---|
| All garden rows, 2001-2024 (unscreened) | 248 | 3,095,000 | 29,924 | 106 |
| All years, screened | 227 | 3,200,000 | 31,352 | 107 |
| 1998-2009 | 61 | 1,789,000 | 16,337 | 103 |
| 2010-2014 | 38 | 3,095,000 | 31,017 | 113 |
| 2015-2019 | 47 | 3,600,000 | 35,614 | 103 |
| 2020-2024 | 81 | 5,400,000 | 44,422 | 115 |
| 2022-2024 | 28 | 5,546,000 | 48,377 | 115 |

## By year (screened)

| Year | Deals | Median price ₪ | Median ₪/m² | Median m² |
|---|---|---|---|---|
| 2001 | 1 | not published (<5 deals) | not published (<5 deals) | not published (<5 deals) |
| 2002 | 1 | not published (<5 deals) | not published (<5 deals) | not published (<5 deals) |
| 2003 | 8 | 1,627,000 | 14,633 | 103 |
| 2004 | 17 | 1,809,000 | 16,026 | 120 |
| 2005 | 7 | 1,573,000 | 15,889 | 87 |
| 2006 | 3 | not published (<5 deals) | not published (<5 deals) | not published (<5 deals) |
| 2007 | 12 | 1,868,000 | 18,779 | 94 |
| 2008 | 5 | 2,940,000 | 31,281 | 103 |
| 2009 | 7 | 3,120,000 | 22,286 | 129 |
| 2010 | 5 | 3,435,000 | 32,109 | 114 |
| 2011 | 6 | 3,300,000 | 25,057 | 119 |
| 2012 | 8 | 2,995,000 | 27,751 | 148 |
| 2013 | 8 | 1,602,500 | 25,726 | 74 |
| 2014 | 11 | 3,675,000 | 34,271 | 103 |
| 2015 | 11 | 2,450,000 | 23,333 | 100 |
| 2016 | 15 | 2,774,000 | 34,675 | 94 |
| 2017 | 5 | 3,100,000 | 50,664 | 106 |
| 2018 | 3 | not published (<5 deals) | not published (<5 deals) | not published (<5 deals) |
| 2019 | 13 | 4,670,000 | 43,750 | 104 |
| 2020 | 14 | 5,750,000 | 31,850 | 186 |
| 2021 | 39 | 4,918,000 | 46,410 | 104 |
| 2022 | 12 | 5,935,000 | 39,522 | 118 |
| 2023 | 11 | 5,442,000 | 68,033 | 98 |
| 2024 | 5 | 5,650,000 | 55,511 | 115 |

Single-year medians rest on 5 to 39 deals and swing with the mix of large and small units; use the period rows for any public claim.

## By rooms (screened)

| Rooms | All years: deals | median ₪ | median ₪/m² | median m² | 2020-2024: deals | median ₪ | median ₪/m² | median m² |
|---|---|---|---|---|---|---|---|---|
| 1-2 | 31 | 1,700,000 | 35,860 | 48 | 14 | 2,720,000 | 53,879 | 46 |
| 3 | 34 | 2,592,500 | 42,631 | 74 | 14 | 4,100,000 | 66,645 | 70 |
| 4 | 70 | 3,045,000 | 30,018 | 104 | 15 | 4,600,000 | 42,778 | 102 |
| 5+ | 89 | 5,400,000 | 29,924 | 157 | 38 | 6,875,000 | 41,142 | 178 |
| not stated | 3 | not published (<5 deals) | not published (<5 deals) | not published (<5 deals) | 0 | not published (<5 deals) | not published (<5 deals) | not published (<5 deals) |

## New (from a developer) vs second hand (screened)

| Set | Deals | Median ₪ | Median ₪/m² | Median m² |
|---|---|---|---|---|
| new, all years | 29 | 3,900,000 | 45,333 | 95 |
| second hand, all years | 198 | 3,005,000 | 29,924 | 109 |
| new, 2020-2024 | 14 | 4,875,000 | 61,900 | 73 |
| second hand, 2020-2024 | 67 | 5,442,000 | 41,902 | 121 |

## By neighbourhood (screened; municipal neighbourhood names as in the GIS layer)

| Neighbourhood | Deals | Deals 2020-2024 | Median ₪ (all years) | Median ₪/m² (all years) | Median ₪/m² 2015-2024 | Median m² | Last deal |
|---|---|---|---|---|---|---|---|
| נופי ים | 18 | 6 | 3,787,500 | 31,075 | 38,033 | 116 | 2023-06-29 |
| רביבים | 17 | 4 | 3,435,000 | 32,109 | 47,697 | 122 | 2024-08-28 |
| לב תל-אביב | 14 | 10 | 6,121,000 | 60,887 | 64,073 | 108 | 2024-03-14 |
| גני צהלה, רמות צהלה | 13 | 3 | 3,800,000 | 25,705 | 28,757 | 175 | 2023-12-14 |
| המשתלה | 13 | 2 | 2,494,000 | 19,697 | not published (<5 deals) | 122 | 2022-08-08 |
| נוה צדק | 12 | 2 | 2,028,500 | 27,269 | not published (<5 deals) | 74 | 2022-11-16 |
| הדר-יוסף | 12 | 5 | 2,930,500 | 32,631 | 42,778 | 116 | 2024-01-17 |
| שפירא | 11 | 7 | 1,835,000 | 30,808 | 30,808 | 53 | 2024-06-10 |
| תל ברוך צפון | 9 | 1 | 4,670,000 | 44,356 | 45,649 | 114 | 2020-05-20 |
| הצפון החדש-החלק הדרומי | 8 | 5 | 3,337,000 | 49,944 | 50,935 | 100 | 2021-09-14 |
| נוה דן | 7 | 3 | 6,350,000 | 31,134 | not published (<5 deals) | 253 | 2022-04-03 |
| עג'מי וגבעת עליה | 6 | 2 | 3,750,000 | 32,992 | not published (<5 deals) | 110 | 2021-02-08 |
| הצפון החדש-סביבת ככר המדינה | 6 | 5 | 4,325,000 | 70,766 | 70,766 | 58 | 2024-04-18 |
| נוה שאנן | 6 | 2 | 1,740,000 | 22,652 | not published (<5 deals) | 52 | 2022-09-22 |
| צוקי אביב | 6 | 1 | 5,866,500 | 38,594 | not published (<5 deals) | 142 | 2020-07-05 |
| התקוה | 5 | 1 | 1,125,000 | 11,842 | not published (<5 deals) | 95 | 2022-01-05 |
| הצפון החדש - החלק הצפוני | 5 | 5 | 7,137,000 | 64,289 | 64,289 | 109 | 2021-09-05 |
| 'נאות אפקה ב | 5 | 1 | 1,699,000 | 15,492 | not published (<5 deals) | 98 | 2021-11-18 |
| כרם התימנים | 4 | 1 | not published (<5 deals) | not published (<5 deals) | not published (<5 deals) | not published (<5 deals) | 2023-01-23 |
| כוכב הצפון | 4 | 0 | not published (<5 deals) | not published (<5 deals) | not published (<5 deals) | not published (<5 deals) | 2014-11-24 |
| צהלון ושיכוני חסכון | 4 | 1 | not published (<5 deals) | not published (<5 deals) | not published (<5 deals) | not published (<5 deals) | 2021-03-14 |
| פלורנטין | 3 | 1 | not published (<5 deals) | not published (<5 deals) | not published (<5 deals) | not published (<5 deals) | 2022-07-03 |
| עזרא והארגזים | 3 | 2 | not published (<5 deals) | not published (<5 deals) | not published (<5 deals) | not published (<5 deals) | 2023-05-16 |
| יד אליהו | 3 | 0 | not published (<5 deals) | not published (<5 deals) | not published (<5 deals) | not published (<5 deals) | 2015-06-23 |
| 'תכנית ל | 3 | 2 | not published (<5 deals) | not published (<5 deals) | not published (<5 deals) | not published (<5 deals) | 2020-10-29 |
| צפון יפו | 3 | 0 | not published (<5 deals) | not published (<5 deals) | not published (<5 deals) | not published (<5 deals) | 2017-02-22 |
| רמת-אביב | 3 | 1 | not published (<5 deals) | not published (<5 deals) | not published (<5 deals) | not published (<5 deals) | 2020-11-15 |
| ביצרון ורמת ישראל | 3 | 1 | not published (<5 deals) | not published (<5 deals) | not published (<5 deals) | not published (<5 deals) | 2021-10-03 |
| הצפון הישן - החלק הצפוני | 3 | 0 | not published (<5 deals) | not published (<5 deals) | not published (<5 deals) | not published (<5 deals) | 2014-09-15 |
| 'נאות אפקה א | 3 | 0 | not published (<5 deals) | not published (<5 deals) | not published (<5 deals) | not published (<5 deals) | 2018-02-15 |
| 'רמת אביב ג | 2 | 0 | not published (<5 deals) | not published (<5 deals) | not published (<5 deals) | not published (<5 deals) | 2019-04-17 |
| הצפון הישן-החלק הדרומי | 2 | 0 | not published (<5 deals) | not published (<5 deals) | not published (<5 deals) | not published (<5 deals) | 2016-06-01 |
| רמת החייל | 2 | 1 | not published (<5 deals) | not published (<5 deals) | not published (<5 deals) | not published (<5 deals) | 2021-03-25 |
| תל ברוך | 2 | 2 | not published (<5 deals) | not published (<5 deals) | not published (<5 deals) | not published (<5 deals) | 2023-12-03 |
| גלילות | 2 | 2 | not published (<5 deals) | not published (<5 deals) | not published (<5 deals) | not published (<5 deals) | 2020-11-03 |
| גבעת הרצל, אזור המלאכה-יפו | 1 | 0 | not published (<5 deals) | not published (<5 deals) | not published (<5 deals) | not published (<5 deals) | 2016-04-14 |
| בבלי | 1 | 1 | not published (<5 deals) | not published (<5 deals) | not published (<5 deals) | not published (<5 deals) | 2021-06-30 |
| יפו העתיקה,נמל יפו | 1 | 0 | not published (<5 deals) | not published (<5 deals) | not published (<5 deals) | not published (<5 deals) | 2015-09-13 |
| (יפו ד' (גבעת התמרים | 1 | 1 | not published (<5 deals) | not published (<5 deals) | not published (<5 deals) | not published (<5 deals) | 2021-03-10 |
| יפו ג' ונוה גולן | 1 | 0 | not published (<5 deals) | not published (<5 deals) | not published (<5 deals) | not published (<5 deals) | 2013-07-11 |

## By street: top 40 of 166 streets (screened; street names as in the file, surname first)

Only two streets reach the 5-deal floor for a median. The rest are counts only.

| # | Street | Deals | New-project deals | Median ₪ | Median ₪/m² | Last deal | Neighbourhood |
|---|---|---|---|---|---|---|---|
| 1 | סשא ארגוב | 6 | 0 | 2,105,500 | 19,902 | 2020-10-26 | המשתלה |
| 2 | פן אלכסנדר | 6 | 0 | 4,775,000 | 44,787 | 2020-05-20 | תל ברוך צפון |
| 3 | בעל העקידה | 4 | 0 | not published (<5 deals) | not published (<5 deals) | 2021-11-07 | שפירא |
| 4 | גלבוע אמיר | 4 | 1 | not published (<5 deals) | not published (<5 deals) | 2019-05-27 | נופי ים |
| 5 | קהילת ורשה | 4 | 2 | not published (<5 deals) | not published (<5 deals) | 2021-11-21 | הדר-יוסף |
| 6 | שגאל מרק | 4 | 0 | not published (<5 deals) | not published (<5 deals) | 2023-06-29 | נופי ים |
| 7 | ארם משה | 3 | 0 | not published (<5 deals) | not published (<5 deals) | 2015-08-05 | רביבים |
| 8 | נס ציונה | 3 | 3 | not published (<5 deals) | not published (<5 deals) | 2021-08-05 | לב תל-אביב |
| 9 | פינס | 3 | 0 | not published (<5 deals) | not published (<5 deals) | 2010-05-09 | נוה צדק |
| 10 | צה"ל | 3 | 0 | not published (<5 deals) | not published (<5 deals) | 2021-01-31 | גני צהלה, רמות צהלה |
| 11 | רוממה | 3 | 0 | not published (<5 deals) | not published (<5 deals) | 2021-11-18 | 'נאות אפקה ב |
| 12 | רכטר זאב | 3 | 0 | not published (<5 deals) | not published (<5 deals) | 2024-08-28 | רביבים |
| 13 | שטרייכמן יחזקאל | 3 | 0 | not published (<5 deals) | not published (<5 deals) | 2020-11-08 | נופי ים |
| 14 | תמיר שמואל | 3 | 0 | not published (<5 deals) | not published (<5 deals) | 2020-10-08 | נופי ים |
| 15 | אחימאיר אבא | 2 | 2 | not published (<5 deals) | not published (<5 deals) | 2019-04-17 | 'רמת אביב ג |
| 16 | אשכול לוי | 2 | 1 | not published (<5 deals) | not published (<5 deals) | 2010-03-23 | 'תכנית ל |
| 17 | בנימין מטודלה | 2 | 0 | not published (<5 deals) | not published (<5 deals) | 2012-11-15 | נוה דן |
| 18 | בת מרים יוכבד | 2 | 0 | not published (<5 deals) | not published (<5 deals) | 2019-07-03 | תל ברוך צפון |
| 19 | דבורה הנביאה | 2 | 0 | not published (<5 deals) | not published (<5 deals) | 2015-05-14 | רביבים |
| 20 | דגניה | 2 | 0 | not published (<5 deals) | not published (<5 deals) | 2008-04-30 | נוה צדק |
| 21 | וולמן יהודה | 2 | 0 | not published (<5 deals) | not published (<5 deals) | 2011-12-14 | רביבים |
| 22 | זליגמן מקס | 2 | 0 | not published (<5 deals) | not published (<5 deals) | 2022-08-08 | המשתלה |
| 23 | יבנאל | 2 | 0 | not published (<5 deals) | not published (<5 deals) | 2019-12-06 | נוה צדק |
| 24 | מויאל אהרון | 2 | 0 | not published (<5 deals) | not published (<5 deals) | 2023-12-14 | גני צהלה, רמות צהלה |
| 25 | סגל שמוליק | 2 | 0 | not published (<5 deals) | not published (<5 deals) | 2019-11-06 | גני צהלה, רמות צהלה |
| 26 | סמאטס | 2 | 1 | not published (<5 deals) | not published (<5 deals) | 2021-09-05 | הצפון החדש - החלק הצפוני |
| 27 | קדושי השואה | 2 | 1 | not published (<5 deals) | not published (<5 deals) | 2020-07-05 | צוקי אביב |
| 28 | קהילת יאסי | 2 | 0 | not published (<5 deals) | not published (<5 deals) | 2005-05-17 | הדר-יוסף |
| 29 | קהילת קייב | 2 | 0 | not published (<5 deals) | not published (<5 deals) | 2017-03-26 | 'נאות אפקה א |
| 30 | קובנר אבא | 2 | 0 | not published (<5 deals) | not published (<5 deals) | 2012-03-04 | כוכב הצפון |
| 31 | רביבים | 2 | 0 | not published (<5 deals) | not published (<5 deals) | 2023-02-28 | רביבים |
| 32 | רובינשטיין ארתור | 2 | 0 | not published (<5 deals) | not published (<5 deals) | 2022-02-01 | נופי ים |
| 33 | רוזן פנחס | 2 | 0 | not published (<5 deals) | not published (<5 deals) | 2012-01-02 | הדר-יוסף |
| 34 | רוזנבלום הרצל | 2 | 0 | not published (<5 deals) | not published (<5 deals) | 2020-11-03 | גלילות |
| 35 | רוזנבלום יאיר | 2 | 0 | not published (<5 deals) | not published (<5 deals) | 2019-12-23 | צוקי אביב |
| 36 | רש"י | 2 | 1 | not published (<5 deals) | not published (<5 deals) | 2021-06-23 | לב תל-אביב |
| 37 | שרון אריה | 2 | 0 | not published (<5 deals) | not published (<5 deals) | 2004-02-11 | רביבים |
| 38 | אברבנאל | 1 | 0 | not published (<5 deals) | not published (<5 deals) | 2007-05-08 | פלורנטין |
| 39 | אגדתי ברוך | 1 | 0 | not published (<5 deals) | not published (<5 deals) | 2007-05-02 | גני צהלה, רמות צהלה |
| 40 | אדיל עאזר | 1 | 1 | not published (<5 deals) | not published (<5 deals) | 2016-05-28 | עג'מי וגבעת עליה |

## Latest 30 garden deals in the file (all rows, flags shown)

| Date | Address | Neighbourhood | Rooms | m² | Price ₪ | ₪/m² | New | Floor field | Flag |
|---|---|---|---|---|---|---|---|---|---|
| 2024-08 | רכטר זאב 8 | רביבים | 5 | 123.4 | 6,850,000 | 55,511 |  | קרקע |  |
| 2024-06 | מסילת ישרים 8 | שפירא | 1 | 25.0 | 675,000 | 27,000 |  | שניה |  |
| 2024-04 | בילטמור 8 | הצפון החדש-סביבת ככר המדינה | 2 | 40.0 | 2,940,000 | 73,500 |  | ראשונה |  |
| 2024-03 | בלפור 6 | לב תל-אביב | 4 | 115.0 | 10,650,000 | 92,609 |  | מרתף ‎-3‏, קומה ‎0‏ |  |
| 2024-01 | קהילת לבוב 7 | הדר-יוסף | 4 | 127.0 | 5,650,000 | 44,488 |  | ראשונה |  |
| 2023-12 | אברהם רוויגו 1 | שפירא | 1 | 25.0 | 625,000,000 | 25,000,000 |  | ראשונה | excluded: high |
| 2023-12 | אהרון מויאל 3 | גני צהלה, רמות צהלה | 5 | 203.0 | 8,000,000 | 39,409 |  | ראשונה |  |
| 2023-12 | חנה רובינא 6 | תל ברוך | 6 | 181.0 | 6,308,000 | 34,851 |  | ראשונה |  |
| 2023-10 | ציונה תג'ר 13 | צהלון ושיכוני חסכון | 3 | 86.0 | 656,948 | 7,639 |  | שניה | excluded: low |
| 2023-08 | קליי 10 | הצפון החדש-סביבת ככר המדינה | 3 | 61.0 | 4,150,000 | 68,033 |  | שניה |  |
| 2023-07 | חכמי אתונה 1 | שפירא | 3 | 53.0 | 2,600,000 | 49,057 |  | ראשונה |  |
| 2023-07 | חכמי אתונה 1 | שפירא | 3 | 53.0 | 260,000 | 4,906 |  | ראשונה | excluded: low |
| 2023-06 | פלטיאל 1 | התקוה | 3 | 48.0 | 292,000 | 6,083 |  | ראשונה | excluded: low |
| 2023-06 | מארק שאגאל 8 | נופי ים | 5 | 117.7 | 8,100,000 | 68,819 |  | קרקע |  |
| 2023-05 | אדר 17 | עזרא והארגזים | 3 | 70.0 | 1,210,000 | 17,286 |  | ראשונה |  |
| 2023-05 | יצחק כוכבי 15 | שפירא | 2 | 44.0 | 400,000 | 9,091 |  | ראשונה | excluded: low |
| 2023-04 | בר-אילן 17 | לב תל-אביב | 3 | 79.0 | 5,442,000 | 68,886 |  | ראשונה |  |
| 2023-03 | כרם חמד 12 | שפירא | 4 | 98.0 | 2,500,000 | 25,510 |  | קרקע |  |
| 2023-02 | רביבים 44 | רביבים | 4 | 115.0 | 8,000,000 | 69,565 |  | ראשונה |  |
| 2023-02 | רביבים 44 | רביבים | 7 | 122.0 | 9,050,000 | 74,180 |  | ראשונה |  |
| 2023-01 | קהילת עדן 1 | כרם התימנים | 3 | 53.5 | 4,050,000 | 75,701 |  | קרקע |  |
| 2022-11 | הונא 46 | התקוה | 3 | 50.0 | 252,000 | 5,040 |  | ראשונה | excluded: low |
| 2022-11 | אריה דיסנצ'יק 4 | רביבים | 6 | 152.0 | 7,250,000 | 47,697 |  | קרקע, ראשונה |  |
| 2022-11 | לפין 20 | נוה צדק | 4 | 101.0 | 7,300,000 | 72,277 |  | ראשונה |  |
| 2022-10 | עיר שמש 31 | גני צהלה, רמות צהלה | 6 | 196.0 | 794,000 | 4,051 |  | ראשונה | excluded: low |
| 2022-09 | באר שבע 18 | מכללת יפו תל אביב ודקר | 4 | 117.46 | 977,000 | 8,318 |  | קרקע | excluded: low |
| 2022-09 | נווה שאנן 13 | נוה שאנן | 4 | 127.0 | 4,000,000 | 31,496 |  | ראשונה |  |
| 2022-09 | מקור חיים 7 | שפירא | 2 | 40.0 | 1,700,000 | 42,500 |  | ראשונה |  |
| 2022-08 | חזקיהו המלך 29 | שפירא | 2 | 47.0 | 1,240,000 | 26,383 |  | ראשונה |  |
| 2022-08 | מקס זליגמן 1 | המשתלה | 5 | 136.0 | 4,970,000 | 36,544 |  | שניה |  |

## Rows left out of the aggregates (outlier rule)

| Date | Address | Rooms | m² | Price ₪ | Reason |
|---|---|---|---|---|---|
| 2010-02-15 | יהודה הלוי 10 | 2.0 | 59.0 | 5,767,000 | high: over 3x that year citywide flat median per m2 (likely data error or multi-unit) |
| 2012-03-05 | יצחק חילו 5 | 5.0 | 200.0 | 17,833,000 | high: over 3x that year citywide flat median per m2 (likely data error or multi-unit) |
| 2015-06-18 | תשבי 15 | 4.0 | 127.0 | 275,000 | low: under 30% of that year citywide flat median per m2 (likely partial share or non-market) |
| 2015-12-07 | יגאל אלון 50 | 5.0 | 90.0 | 128,000 | low: under 30% of that year citywide flat median per m2 (likely partial share or non-market) |
| 2016-01-21 | שמואל בן-עדיה 25 | 4.0 | 80.0 | 553,000 | low: under 30% of that year citywide flat median per m2 (likely partial share or non-market) |
| 2016-09-04 | נס לגויים 9 | 3.0 | 101.35 | 273,000 | low: under 30% of that year citywide flat median per m2 (likely partial share or non-market) |
| 2016-12-25 | ז'אן ראסין 13 | 2.0 | 32.9 | 303,000 | low: under 30% of that year citywide flat median per m2 (likely partial share or non-market) |
| 2017-02-16 | עבד אל-ג'ני 8 | 4.0 | 122.8 | 810,000 | low: under 30% of that year citywide flat median per m2 (likely partial share or non-market) |
| 2017-03-26 | הסבא משפולה 6 | 3.0 | 81.0 | 140,000 | low: under 30% of that year citywide flat median per m2 (likely partial share or non-market) |
| 2018-08-29 | יהושע ברטונוב 12 | 6.0 | 709.0 | 5,635,000 | low: under 30% of that year citywide flat median per m2 (likely partial share or non-market) |
| 2018-09-20 | דבורה הנביאה 2 | 5.0 | 1602.0 | 4,550,000 | low: under 30% of that year citywide flat median per m2 (likely partial share or non-market) |
| 2020-11-23 | עיר שמש 25 | 5.0 | 813.0 | 4,725,000 | low: under 30% of that year citywide flat median per m2 (likely partial share or non-market) |
| 2022-04-19 | יצחק כוכבי 15 | 2.0 | 44.0 | 400,000 | low: under 30% of that year citywide flat median per m2 (likely partial share or non-market) |
| 2022-09-22 | באר שבע 18 | 4.0 | 117.46 | 977,000 | low: under 30% of that year citywide flat median per m2 (likely partial share or non-market) |
| 2022-10-12 | עיר שמש 31 | 6.0 | 196.0 | 794,000 | low: under 30% of that year citywide flat median per m2 (likely partial share or non-market) |
| 2022-11-29 | הונא 46 | 3.0 | 50.0 | 252,000 | low: under 30% of that year citywide flat median per m2 (likely partial share or non-market) |
| 2023-05-09 | יצחק כוכבי 15 | 2.0 | 44.0 | 400,000 | low: under 30% of that year citywide flat median per m2 (likely partial share or non-market) |
| 2023-06-29 | פלטיאל 1 | 3.0 | 48.0 | 292,000 | low: under 30% of that year citywide flat median per m2 (likely partial share or non-market) |
| 2023-07-04 | חכמי אתונה 1 | 3.0 | 53.0 | 260,000 | low: under 30% of that year citywide flat median per m2 (likely partial share or non-market) |
| 2023-10-25 | ציונה תג'ר 13 | 3.0 | 86.0 | 656,948 | low: under 30% of that year citywide flat median per m2 (likely partial share or non-market) |
| 2023-12-31 | אברהם רוויגו 1 | 1.0 | 25.0 | 625,000,000 | high: over 3x that year citywide flat median per m2 (likely data error or multi-unit) |

## Context, 2020-2024 (unscreened, same file)

apartments = DEALNATUREDESCRIPTION in ('דירה בבית קומות','דירה'); ground floor = FLOORNO 'קרקע'. Ground floor is a PROXY, not the same as a garden apartment.

| Set | Deals | Median ₪ | Median ₪/m² | Median m² |
|---|---|---|---|---|
| all apartments | 16,889 | 3,450,000 | 47,266 | 74 |
| ground floor apartments | 680 | 2,800,000 | 49,989 | 60 |
| garden labelled | 81 | 5,400,000 | 44,422 | 115 |
| penthouse labelled | 86 | 7,714,000 | 56,006 | 135 |

Share: 227 garden-labelled deals out of 75,182 flat-type residential deals (flats, garden flats, roof flats) in the whole file; 3,391 ordinary flats are recorded on the ground floor (FLOORNO 'קרקע'). The garden label is set by whoever reported the deal, so the true number of garden flats sold is very likely larger than 248 (inference, not measured).

## Ground floor vs whole neighbourhood, 2020-2024 (PROXY, unscreened)

Ordinary flats only (not garden-labelled). Neighbourhoods with at least 5 ground-floor deals. A ground-floor flat is not necessarily a garden flat; low ratios such as Ajami may reflect partial-share deals.

| Neighbourhood | Flats | Median ₪/m² all floors | Ground-floor flats | Median ₪/m² ground floor | Ground vs all |
|---|---|---|---|---|---|
| הצפון הישן - החלק הצפוני | 1193 | 61,240 | 68 | 63,167 | +3.1% |
| לב תל-אביב | 1186 | 60,909 | 77 | 54,107 | -11.2% |
| הצפון הישן-החלק הדרומי | 999 | 58,160 | 83 | 57,054 | -1.9% |
| הצפון החדש-סביבת ככר המדינה | 895 | 59,680 | 37 | 74,198 | +24.3% |
| הצפון החדש - החלק הצפוני | 642 | 61,826 | 40 | 69,204 | +11.9% |
| הצפון החדש-החלק הדרומי | 587 | 62,470 | 30 | 68,468 | +9.6% |
| נוה אביבים וסביבתה | 519 | 46,715 | 5 | not published (<5 deals) |  |
| יד אליהו | 488 | 37,791 | 18 | 36,406 | -3.7% |
| פלורנטין | 427 | 52,362 | 6 | 55,128 | +5.3% |
| התקוה | 418 | 28,174 | 17 | 28,150 | -0.1% |
| (יפו ד' (גבעת התמרים | 386 | 29,199 | 17 | 33,157 | +13.6% |
| צהלון ושיכוני חסכון | 349 | 39,574 | 34 | 37,237 | -5.9% |
| נוה שאנן | 338 | 41,591 | 13 | 38,831 | -6.6% |
| מכללת יפו תל אביב ודקר | 324 | 34,713 | 25 | 31,646 | -8.8% |
| קרית שלום | 306 | 30,990 | 62 | 30,920 | -0.2% |
| צפון יפו | 297 | 51,543 | 27 | 47,048 | -8.7% |
| ביצרון ורמת ישראל | 260 | 42,857 | 8 | 55,867 | +30.4% |
| יפו ג' ונוה גולן | 245 | 30,286 | 5 | 28,286 | -6.6% |
| כרם התימנים | 203 | 65,980 | 11 | 72,045 | +9.2% |
| נוה צדק | 187 | 65,732 | 5 | 54,015 | -17.8% |
| שפירא | 165 | 34,524 | 13 | 31,185 | -9.7% |
| עג'מי וגבעת עליה | 131 | 31,507 | 13 | 11,846 | -62.4% |
| תל ברוך צפון | 118 | 41,721 | 12 | 50,667 | +21.4% |
| מעוז אביב | 47 | 55,224 | 7 | 59,875 | +8.4% |

## Floor field on garden deals (as recorded)

ראשונה: 82, (blank): 42, קרקע: 36, שניה: 13, שלישית: 6, מרתף: 3, קרקע,ראשונה: 3, מרתף, קרקע: 2, רביעית: 2, קרקע+ראשונה: 2, מרתף + קרקע: 2, מרתף קרקע ביניים: 2, קומה ‎1‏: 2, מרתף עליון, קרקע: 2, מרתף,קרקע: 1, -: 1, מרתף ‎-3‏, קומה ‎0‏: 1, תשיעית: 1, מרתף וראשונה: 1, מרתף שני, קרקע: 1, רביעית, חמישית: 1, קרקע וראשונה: 1, קרקע, ראשונה: 1, שמינית: 1, שניה ושלישית: 1, קומה ‎0‏, קומה ‎1‏: 1, שישית: 1, מרתף,קרקע,ראשנה: 1, מרתף +קרקע ראשונה+גג: 1, מרתף ‎-1‏, קומה ‎0‏: 1, קרקע וקרקע עליונה: 1, מרתף+קרקע+ראשונה: 1, מרתף, קרקע, ראשונה: 1, מרתף שני +קרקע: 1, שניה,שלישית: 1, מרתף קרקע: 1, קרקע + ראשונה: 1, שביעית: 1, ראה הערות רשם: 1, מרתף ‎-1‏, קומה ‎0‏, קומה ‎1‏: 1, חמישית ו-גג: 1, חמישית+שישית: 1
