# City price pages: official median deal prices by rooms (7.10.2026)

Data for the rooms-mode PriceGuide on 24 nad-lan city price pages. Research and data files only: nothing was published, nothing on the live site was touched, nothing was committed.

## Source and method

- Official public summary files of data.nadlan.gov.il (the same files the government site loads), no token: `https://data.nadlan.gov.il/api/pages/settlement/buy/<CBS locality code>.json` and, for neighbourhoods, `https://data.nadlan.gov.il/api/pages/neighborhood/buy/<id>.json`. Same method as docs/research/2026-10-07-kikar-prices/README.md.
- Read on 7.10.2026 between 2026-10-07 08:43:16 and 2026-10-07 08:43:47 UTC, one request at a time with a 1 second pause, User-Agent `nad-lan.co.il price-guide research (official public summary files; polite 1 req/s)`. All 23 settlement files: HTTP 200, Last-Modified 20.8.2026 (10:31-10:32 GMT), `version` 20-08-2026.
- Each file holds `trends.rooms[]` for 3, 4, 5 rooms and all apartments; each `graphData` point is a quarter (`month` 3/6/9/12 = quarter ending March/June/September/December; labels here 1-3.2026 etc.) with `settlementPrice` (the city's median closed-deal price, full apartment price in ILS) and `countryPrice` (Israel). The government site labels this line "מחיר חציוני" (Tax Authority deals). Not per m2.
- The Israel series is identical in all 23 files (every quarter and room count compared by the build script).
- `null` in the files stays `null` here. Nothing was filled, interpolated or estimated.
- YoY = the newest published quarter of that room count against the same quarter one year earlier, computed from the two official medians. The files also carry a `summary` block (`lastYearAvgPrice`, `priceDifferencePercentage`) whose definition is not published; it was not used.
- Every settlement file's own `settlementID` and `settlementName` were checked against the expected code (table below).

## Code table

| page | city | code | name in the file | latest quarter | 4 rooms median, ₪ | 4 rooms quarter | 4 rooms YoY | 3 rooms YoY | 5 rooms YoY |
|---|---|---|---|---|---|---|---|---|---|
| /ashdod-apartment-prices/ | אשדוד | 70 | אשדוד | 1-3.2026 | 2,130,200 | 1-3.2026 | +6.2% | +0.3% | -5.8% |
| /ashkelon-apartment-prices/ | אשקלון | 7100 | אשקלון | 1-3.2026 | 1,405,800 | 1-3.2026 | -12.0% | -20.6% | -11.7% |
| /bat-yam-apartment-prices/ | בת ים | 6200 | בת ים | 1-3.2026 | 2,692,600 | 1-3.2026 | +4.3% | -1.1% | +13.0% |
| /beer-sheva-apartment-prices/ | באר שבע | 9000 | באר שבע | 1-3.2026 | 1,203,200 | 1-3.2026 | +1.8% | -0.6% | -4.3% |
| /bnei-brak-apartment-prices/ | בני ברק | 6100 | בני ברק | 1-3.2026 | 2,491,200 | 1-3.2026 | -2.5% | -0.2% | -4.3% |
| /eilat-apartment-prices/ | אילת | 2600 | אילת | 1-3.2026 | 1,719,300 | 1-3.2026 | -3.5% | +0.7% | +3.3% |
| /givatayim-apartment-prices/ | גבעתיים | 6300 | גבעתיים | 1-3.2026 | 4,158,900 | 1-3.2026 | -4.7% | -8.9% | -1.7% |
| /haifa-apartment-prices/ | חיפה | 4000 | חיפה | 1-3.2026 | 1,597,500 | 1-3.2026 | -10.7% | +0.5% | -8.8% |
| /herzliya-apartment-prices/ | הרצליה | 6400 | הרצלייה | 1-3.2026 | 3,272,800 | 1-3.2026 | -9.1% | +0.6% | -8.9% |
| /hod-hasharon-apartment-prices/ | הוד השרון | 9700 | הוד השרון | 1-3.2026 | 3,264,800 | 1-3.2026 | -2.2% | +0.5% | -3.7% |
| /holon-apartment-prices/ | חולון | 6600 | חולון | 1-3.2026 | 2,428,500 | 1-3.2026 | -5.8% | +1.0% | -5.6% |
| /jerusalem-apartment-prices/ | ירושלים | 3000 | ירושלים | 1-3.2026 | 2,882,400 | 1-3.2026 | -9.8% | +3.0% | -7.0% |
| /kfar-saba-apartment-prices/ | כפר סבא | 6900 | כפר סבא | 1-3.2026 | 2,817,000 | 10-12.2025 | -6.1% | -21.3% | -4.3% |
| /kiryat-ono-apartment-prices/ | קריית אונו | 2620 | קריית אונו | 1-3.2026 | 3,197,900 | 1-3.2026 | -3.1% | -4.7% | -6.0% |
| /modiin-apartment-prices/ | מודיעין מכבים רעות | 1200 | מודיעין-מכבים-רע | 1-3.2026 | 2,559,800 | 1-3.2026 | -15.9% | -15.5% | -4.8% |
| /netanya-apartment-prices/ | נתניה | 7400 | נתניה | 1-3.2026 | 2,676,100 | 1-3.2026 | +1.8% | -11.6% | -2.2% |
| /petah-tikva-apartment-prices/ | פתח תקווה | 7900 | פתח תקווה | 1-3.2026 | 2,444,100 | 1-3.2026 | -2.2% | +4.3% | -0.1% |
| /raanana-apartment-prices/ | רעננה | 8700 | רעננה | 1-3.2026 | 3,289,900 | 1-3.2026 | -0.8% | -0.8% | +0.2% |
| /ramat-gan-apartment-prices/ | רמת גן | 8600 | רמת גן | 1-3.2026 | 3,330,400 | 1-3.2026 | +3.5% | -2.8% | +4.8% |
| /ramat-hasharon-apartment-prices/ | רמת השרון | 2650 | רמת השרון | 1-3.2026 | 3,809,600 | 1-3.2026 | -10.7% | +16.4% | -2.4% |
| /rehovot-apartment-prices/ | רחובות | 8400 | רחובות | 1-3.2026 | 2,345,500 | 1-3.2026 | -6.9% | n/a | +3.6% |
| /rishon-lezion-apartment-prices/ | ראשון לציון | 8300 | ראשון לציון | 1-3.2026 | 2,392,600 | 1-3.2026 | +0.9% | -1.3% | +2.0% |
| /tel-aviv-apartment-prices/ | תל אביב יפו | 5000 | תל אביב -יפו | 1-3.2026 | 5,229,800 | 1-3.2026 | +10.7% | +14.1% | +6.5% |
| /apartment-prices/ | ישראל | (none) | Israel series (countryPrice) | 4-6.2026 | 2,028,800 | 4-6.2026 | -4.0% | +5.4% | -2.8% |

Israel medians in 1-3.2026 (the cities' quarter, used in every city answer): 3 rooms 1,647,500 ₪, 4 rooms 2,072,000 ₪, 5 rooms 2,920,600 ₪, all 2,058,800 ₪.

## Missing values and caveats

- **No city is without data.** All 23 cities have official medians for 1-3.2026 for at least one room count.
- **The Israel series runs one quarter further (4-6.2026) than every city (1-3.2026)** in the same 20.8.2026 files. The Israel page uses 4-6.2026 for Israel and 1-3.2026 for the cities range, and says so. City pages compare with Israel in the same quarter (`israel`), and also carry `israel_latest` (4-6.2026).
- Gaps by city (the JSON shows the newest published value with its own quarter; the answer text names that quarter):
  - באר שבע (9000): 5 rooms: not published for 1-3.2026, newest is 7-9.2025.
  - כפר סבא (6900): 3 rooms: not published for 1-3.2026, newest is 10-12.2025; 4 rooms: not published for 1-3.2026, newest is 10-12.2025; all apartments: not published for 1-3.2026, newest is 10-12.2025.
  - מודיעין מכבים רעות (1200): 3 rooms: not published for 1-3.2026, newest is 10-12.2025.
  - נתניה (7400): 3 rooms: not published for 1-3.2026, newest is 10-12.2025.
  - רחובות (8400): 3 rooms: no median for the same quarter a year earlier, so no YoY.
  - תל אביב יפו (5000): all apartments: not published for 1-3.2026, newest is 10-12.2025.
- Quarterly medians swing with the mix of deals in the quarter (new vs old, which neighbourhoods sold). One quarter's YoY is a data point, not a trend; the 8-quarter series is in each JSON for a chart.

## Biggest YoY moves (newest quarter vs the same quarter a year earlier)

Largest falls:
- כפר סבא, 3 rooms, 10-12.2025: 1,941,300 ₪ vs 2,466,800 ₪ (-21.3%)
- אשקלון, 3 rooms, 1-3.2026: 918,100 ₪ vs 1,156,700 ₪ (-20.6%)
- מודיעין מכבים רעות, 4 rooms, 1-3.2026: 2,559,800 ₪ vs 3,044,600 ₪ (-15.9%)
- מודיעין מכבים רעות, 3 rooms, 10-12.2025: 2,039,500 ₪ vs 2,414,500 ₪ (-15.5%)
- אשקלון, 4 rooms, 1-3.2026: 1,405,800 ₪ vs 1,597,300 ₪ (-12.0%)
- אשקלון, 5 rooms, 1-3.2026: 1,891,000 ₪ vs 2,142,600 ₪ (-11.7%)

Largest rises:
- רמת השרון, 3 rooms, 1-3.2026: 3,544,800 ₪ vs 3,044,100 ₪ (+16.4%)
- תל אביב יפו, 3 rooms, 1-3.2026: 4,225,800 ₪ vs 3,704,300 ₪ (+14.1%)
- בת ים, 5 rooms, 1-3.2026: 3,468,600 ₪ vs 3,069,800 ₪ (+13.0%)
- תל אביב יפו, 4 rooms, 1-3.2026: 5,229,800 ₪ vs 4,723,800 ₪ (+10.7%)
- תל אביב יפו, 5 rooms, 1-3.2026: 7,497,700 ₪ vs 7,042,600 ₪ (+6.5%)
- אשדוד, 4 rooms, 1-3.2026: 2,130,200 ₪ vs 2,006,000 ₪ (+6.2%)

4 rooms only (Kfar Saba compares 10-12.2025, the others 1-3.2026): 16 of 23 cities fell, 7 rose. Falls led by מודיעין מכבים רעות -15.9%, אשקלון -12.0%, חיפה -10.7%; rises led by תל אביב יפו +10.7%, אשדוד +6.2%, בת ים +4.3%.

## Neighbourhoods

- The settlement file lists the city's neighbourhoods (name and id) **without** medians and without deal counts. Each neighbourhood has its own official file with its own medians by rooms, so all 718 neighbourhood files of the 23 cities were read the same polite way (718 OK, 0 errors).
- The files give **no deal counts**, so "top by deal count" is not possible from official data. Neighbourhoods are ranked by `quarters_with_data`: how many of the 32 values (3/4/5/all rooms x the last 8 quarters) carry an official median (the government site leaves a median empty where there are too few deals, so this tracks activity). Kept: up to 8 per city, only those with at least one 3/4/5-room median in the city's data quarter, with that quarter's medians (null where not published).
- Neighbourhood names are exactly as written in the official files; the source cuts long names at about 20 characters (for example "הצפון החדש סביבת כי", "נווה אביבים וסביבת" in Tel Aviv-Yafo), and three Raanana neighbourhoods are named only by a number (2003, 2004, 2008; none of them is among the kept 7). Fix the display name by hand before showing it, never the number.
- Every neighbourhood row of every city (not only the kept ones) is in neighbourhoods-all.csv.

| city | neighbourhoods listed | kept |
|---|---|---|
| אשדוד | 26 | 8 |
| אשקלון | 36 | 8 |
| בת ים | 10 | 8 |
| באר שבע | 23 | 8 |
| בני ברק | 20 | 8 |
| אילת | 15 | 8 |
| גבעתיים | 12 | 3 |
| חיפה | 59 | 8 |
| הרצליה | 18 | 2 |
| הוד השרון | 11 | 5 |
| חולון | 26 | 8 |
| ירושלים | 110 | 8 |
| כפר סבא | 43 | 3 |
| קריית אונו | 11 | 3 |
| מודיעין מכבים רעות | 17 | 7 |
| נתניה | 38 | 8 |
| פתח תקווה | 40 | 8 |
| רעננה | 21 | 7 |
| רמת גן | 31 | 8 |
| רמת השרון | 11 | 2 |
| רחובות | 33 | 8 |
| ראשון לציון | 35 | 8 |
| תל אביב יפו | 72 | 8 |

## H2 titles against the live pages

Each page's live `<title>` and H1 were read on 7.10.2026 (2026-10-07 08:42 UTC); no JSON title repeats either. Default H2: "כמה עולה דירה ב<עיר> ב-2026". Herzliya's `<title>` already opens with "כמה עולה דירה בהרצליה?", so its H2 is "כמה משלמים על דירה בהרצליה ב-2026".

Near twins to decide on placement (the page already has an H2 that opens "כמה עולה דירה ב...", usually "... לפי הנתונים שנבדקו"): /givatayim-apartment-prices/, /haifa-apartment-prices/, /herzliya-apartment-prices/, /hod-hasharon-apartment-prices/, /jerusalem-apartment-prices/, /kfar-saba-apartment-prices/, /kiryat-ono-apartment-prices/, /netanya-apartment-prices/, /petah-tikva-apartment-prices/, /ramat-gan-apartment-prices/, /ramat-hasharon-apartment-prices/, /rishon-lezion-apartment-prices/. The new block can sit under that H2 or replace it.

Live `<title>` claims that disagree with the official medians (finding only, not touched):
- /modiin-apartment-prices/: title says 3 rooms around 2.65 million; official 3-room median 10-12.2025 = 2,039,500 ₪ (1-3.2026 not published), 4 rooms 1-3.2026 = 2,559,800 ₪.
- /ashkelon-apartment-prices/: title says 3 rooms from 1.0 million; official 3-room median 1-3.2026 = 918,100 ₪.
- /kfar-saba-apartment-prices/: title says 3 rooms between 2 and 3 million; official 3-room median 10-12.2025 = 1,941,300 ₪.
("From" claims on other titles are not contradicted by a median and were not judged.)

## Later, neighbourhood data

Not built now (neighbourhood-type pages). The official neighbourhood files exist for them:
- herzliya-pituach: "הרצליה פיתוח", id 65209714 (Herzliya 6400).
- neve-tzedek: "נווה צדק", id 65210041 (Tel Aviv-Yafo 5000).
- tel-aviv-luxury: no official "luxury" area; the Tel Aviv file has an `indexes.luxury` value with no published definition. Needs a choice of neighbourhoods.
- tel-aviv-seafront: no single official seafront area; candidates in the Tel Aviv list include "נמל תל-אביב" 65209988 and "כרם התימנים" 65210046. Needs a choice.

## Files

| file | what it holds |
|---|---|
| scripts/project-stage/price_guide/cities/<page-slug>.json | 24 files, one per page (23 cities + apartment-prices for Israel), mode "rooms" |
| all-cities.csv | one row per page: newest median, quarter, year-ago value and YoY for 3/4/5/all rooms, Israel same quarter, source URL, Last-Modified, retrieval time |
| all-cities-quarters.csv | the full official series 1-3.2021 to 4-6.2026 per city and room count, with Israel beside it |
| neighbourhoods-all.csv | every neighbourhood of the 23 cities: medians by rooms in the city's data quarter and quarters_with_data |
| nadlan-gov-settlements-raw.json | the 23 settlement files as served, minus the street lists |
| nadlan-gov-neighbourhoods-raw.json | the neighbourhood files kept in the JSONs, as served, minus their neighbour/street lists |

## For render.py (rooms mode)

- `rooms.<k>.latest` + `rooms.<k>.quarter` (can be older than `data_quarter`; show the quarter beside the number), `year_ago`, `change_pct`, `quarters` (8 points, oldest first, null = gap in a line chart, never a zero).
- `israel` = same quarter as `data_quarter`; `israel_latest` = newest Israel quarter. `answer` and `src_line` are ready Hebrew text (no em or en dash, no "!", thousands separators, ₪ after the number). The Israel page also has `cities` (every city's newest values) for a comparison table.
- Page text shows no source name except רשות המסים; URLs stay in `sources`.
