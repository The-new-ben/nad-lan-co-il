# Tel Aviv: ready and near-ready projects, hand check (9.11.2026)

Input: `plugins/nadlan-config/data/projects-market.json` (read 25.10.2026), the 27 rows with status `immediate` or `near_occupancy` and city תל אביב-יפו.
Full per-row results: `tel-aviv.json` in this folder.

## How it was checked

- Developer site first for every row (Ashtrom, Ken HaTor, Hagag, Levinstein "In The City", Africa Israel, Prashkovsky, Tidhar, Bait VeGag, Gindi, BST).
- Yad2 and Madlan block automated fetches (Yad2 shows a Radware "verifying your browser" page; Madlan returns 403). Those pages were read normally in the owner's Chrome. No CAPTCHA came up and none was solved. No forms, no sign-ups.
- Dated news (Bizportal, nadlancenter) used only to settle conflicts, and named in the row notes.
- No price was carried over from the input file. A price is filled only when it was seen today.

## Counts

| Result | Rows |
|---|---|
| Confirmed immediate occupancy | 20 (18 were already immediate, 2 moved up from near) |
| Confirmed near occupancy | 4 (HaGaDa 12/2026, בלוך 39-41 12/2026, ליפסקי 18 Q1/2027, שלומציון 42 03/2027) |
| Status changed vs input | 5 (list below) |
| Not found | 2 (Ensemble, הרביעייה בסמאטס) |
| Blocked, left unresolved | 0 (Yad2 and Madlan were blocked for automated fetch, read in the browser instead) |

## Status changes vs the input file

- **ז'בוטינסקי 152 (בית וגג):** near_occupancy to **marketing**. Bizportal, 16.4.2026: demolition of the old building had just started, occupancy Q4 2028. The Yad2 collection page "מעבר לכיכר" says February 2029. The developer page still shows Q2/2027, which is stale. Remove from the finder.
- **Ensemble (גולדווסר מינצר):** near_occupancy to **not_found**. No developer site, nothing on Yad2, Madlan or nadlan.com. Its price (9,490,000) and date (02/2027) cannot be confirmed. Remove.
- **הרביעייה בסמאטס:** immediate to **not_found**. The Yad2 page now shows only building facts (שדרות סמאטס 19, 4 buildings, 84 apartments) with no units for sale. An old unit listing is gone. Probably sold out, not provable today. Remove.
- **MOMA Tel Aviv (חג'ג'):** near_occupancy to **immediate**. The developer page still says "אכלוס מעבר לדלת", but nadlancenter (21.3.2025) reports Form 4 received and occupancy begun.
- **הסוללים (תדהר ומבנה):** near_occupancy to **immediate**. The Yad2 developer listing says "לאכלוס מיידי", and its expected date (July 2026) has passed. The Tidhar page shows only "בשיווק".

## Label mismatches (immediate label vs stated date)

1. **JAFFA COURTYARD | יהודה הימית:** the developer says "סטטוס: אוכלס", while the Yad2 text says "אכלוס בקרוב".
2. **MOMA Tel Aviv:** the developer says "אכלוס מעבר לדלת" (coming soon). Form 4 and occupancy were already reported in March 2025.
3. **זיכרון ויצמן:** the developer FAQ says "מתאכלס בימים אלה", but the same page body says "נבנה בימים אלה". Yad2 tags the project "אכלוס קרוב" with an expected date of October 2026, which has already passed.
4. **ז'בוטינסקי 152:** the developer page says Q2/2027, news says Q4 2028 and Yad2 says February 2029.

Minor wording issues that do not change the status:
- **Ashtrom (A- NEOT AFEKA, i- Neot Afeka, REMEZ 36):** the pages carry the "אכלוס מיידי" label next to "2026 מועד צפוי לאכלוס". Yad2 gives REMEZ 36 as November 2026.
- **הסוללים:** the Yad2 header still reads "צפי אכלוס - יולי 2026".
- **Port TLV:** the page still says construction "will be completed during 2024".

## Prices vs the input file

| Project | Input | Today | Note |
|---|---|---|---|
| שלומציון 42 | 5,650,000 | **5,200,000** (3 rooms, 82.3 sqm) | **Changed.** Deal: "הנחה ... של 590,000 ₪ לזמן מוגבל! במקום 5,790,000 ₪", no end date |
| Ensemble | 9,490,000 | none | Project not found |
| JAFFA COURTYARD | 3,700,000 | 3,700,000 (3-room garden, 92 sqm) | Same, from Yad2 |
| REMEZ 36 | 5,900,000 | 5,900,000 (4 rooms, 96 sqm) | Same, from Yad2 |
| הסוללים | 4,990,000 | 4,990,000 (4 rooms, 102 sqm) | Same, from Yad2 |
| וולפסון 52 | 3,150,000 | 3,150,000 (2 rooms, 50 sqm) | Same, from Yad2 |
| זיכרון ויצמן | 3,989,000 | 3,989,000 (2 rooms, 52.5 sqm) | Same, from Yad2 |
| מגדלי גינדי | 5,200,000 | 5,200,000 (4 rooms, 95 sqm) | Same, from Yad2 |

Port TLV publishes only a price per sqm (from 95,000 ₪/sqm), so it has no price_from.

## Other data errors in the input

- **מגדלי גינדי תל אביב:** the input names the developer as גינדי החזקות. The project belongs to מגדלי גינדי תל אביב בע"מ / גינדי השקעות, which is a different company. Today's Yad2 listing shows only 4-room units, not "2-5, פנטהאוז 6".
- **וולפסון 52:** the input neighbourhood is נווה שאנן. Yad2 files it under פלורנטין, and its address is וולפסון 52 פינת הקונגרס 13.
- **בלוך 39-41:** Yad2 also lists גורקן יזמות נדל"ן as co-developer.
- **Deals seen today** (as published, none with an end date):
  - MOMA: 300,000 ₪ furniture package.
  - הזוהר 5: full furniture package.
  - Port TLV: 25% now, the rest in 2027.
  - הסוללים: 50/50 with the second half a year after occupancy.
  - זיכרון ויצמן: up to 50% a year after occupancy, limited to 10 apartments.
  - גינדי: 50% now, the rest in two years.
  - שלומציון 42: the 590,000 ₪ discount.
