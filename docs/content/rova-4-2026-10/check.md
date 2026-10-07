# Self-check: article-he.md (7.10.2026, 08:00 UTC)

## 1. Front matter

| field | value | rule | result |
|---|---|---|---|
| seo_title | רובע 4 תל אביב: גבולות, רחובות, תוכנית ומחירי דירות | max 60 chars, contains "רובע 4 תל אביב" | 51 chars, PASS |
| meta_description | רובע 4 תל אביב הוא הצפון החדש: ... ופרויקטי התחדשות עירונית. | 140-155 chars | 144 chars, PASS |
| h1 | רובע 4 בתל אביב: הצפון החדש, הגבולות, התוכנית ומחירי הדירות | contains "רובע 4", exactly one h1 | PASS (body has no "# " line) |

## 2. Word count (script: scratchpad check.py; tables, front matter and link URLs excluded)

| measure | words |
|---|---|
| net prose including H2/H3 headings | 2,615 |
| net prose excluding headings | 2,457 |
| words inside tables (not counted) | 1,132 |

Target 2,200-3,200: PASS on both counting methods.

## 3. Forbidden words scan (body + front matter, substring count)

| word | count |
|---|---|
| אטלס | 0 |
| חשוב לציין | 0 |
| הזדמנות | 0 |
| חלום | 0 |
| מושלם | 0 |
| מדהים | 0 |
| חוויה / חוויית | 0 / 0 |
| ממשק | 0 |
| אינטראקטיבי | 0 |
| המערכת | 0 |
| הפלטפורמה | 0 |
| טכנולוגיה | 0 |
| סימולציה | 0 |
| בקרוב | 0 |
| אנחנו מתווכים / מתווכים | 0 / 0 |
| exclamation mark "!" | 0 |

Source names on the page (ויקיפדיה, מרכז הנדל"ן, ביזפורטל, כלכליסט, גלובס, ynet, יד2, מדלן, הלמ"ס, gov.il, tabanow, isramap,
www., http://): 0. The only official body named is רשות המסים (as the origin of the deal medians), the same wording as
the hamedina price list. pricedata.json scanned with the same list: 0 hits.

## 4. Dashes

| check | count |
|---|---|
| em dash (U+2014) | 0 |
| en dash (U+2013) | 0 |
| minus sign (U+2212) | 0 |
| spaced hyphen " - " used as a dash | 0 |

Hyphens left are word joiners only (ב-2026, כ-51,500, ה-80, 4.5) and the plan number תא/3729/א. Official neighbourhood names
were rewritten with a comma ("הצפון החדש, החלק הצפוני") instead of the spaced dash they carry in the government files.
Ranges in prose and article tables are written with "עד". pricedata.json keeps the hyphen-minus range style of
hamedina.json in tiles and table cells ("63,000-68,000"); no em or en dash there.

## 5. Every number in article-he.md mapped to facts.md

206 distinct numeric tokens were extracted by script. Small integers that are room counts, floor counts in deal rows,
street numbers and list ordinals are covered by the row they sit in.

| number(s) as on the page | where | fact id |
|---|---|---|
| 51,500; 2022 | opening | R4 |
| 3729/א; 5.2018 (in force); 23.5.2018; 30.5.2018; 14.11.2012 | opening, plan, FAQ | R16, R17, R18 |
| 6,835,800; 5,229,800 | opening, prices, tax example | R53, R55 |
| 63,000-68,000; 70,000-75,000 | opening, ₪/m² table, למי מתאים, FAQ | R60 |
| 9 quarters ("תשעה"); 1, 2, 3, 6 (quarter numbers) | H2 1 | R2, R3, R11 |
| 1948; the 80s; 50% larger plots | H2 1, comparison | R9, R93 |
| 2,825 dunam | H2 1 | R19 |
| מסוף 2000 | H2 1 | R6 |
| 8 / 7 / 6 / 4 floors; 1 / 2 partial roofs; 10 floors (Arlozorov plan) | streets table, heights table, FAQ | R23, R29 |
| 40 floors (eastern strip) | neighbourhoods table | R10 |
| 6,042,800; 6,910,000; 6,835,800 | neighbourhoods, prices, למי מתאים, FAQ | R52, R53, R54 |
| 5,100; 50% realisation | plan, comparison, FAQ | R19 |
| 25 m; 750 m²; 50%; 90 m² | heights paragraph | R23 |
| 8 or 9 floors, almost double units | heights paragraph | R40, R90 |
| 230%; 3 floors; 165%; 2 floors; 40 m²; 65% | additions table | R22 |
| 38 (תמ"א 38) | plan, levy | R20, R25 |
| half of the betterment; 23.5.2018; 45 days | levy, FAQ | R25 |
| 2019; 4.5 m; 5 m | what changed | R26 |
| 2024; תא/4474; 10 floors; 600 apartments | what changed | R28, R29 |
| 4.12.2024; 20,000 m²; 18,000 apartments; 3 years | what changed | R30 |
| 18.5.2026; תא/3729ב | what changed | R27 |
| ten blocks ("עשרה גושים") | how to check | R24 |
| 3-room medians 4,434,900; 4,943,500; 4,562,000; 4,225,800 | medians table, FAQ | R52-R55 |
| 5-room medians 7,704,000; 8,455,800; 7,497,700; "לא פורסם חציון" | medians table | R52-R55 |
| 30.7%; 32.1%; 15.5%; 4.9%; 17.0% | medians paragraph | R56 (computed) |
| 4-room Q1 series 6,281,300 / 6,001,300 / 5,681,700; 6,573,800 / 6,698,300; 7,020,100 / 6,293,100 / 6,777,900; 4,638,500 / 4,697,600 / 4,723,800 | trend table | R57 |
| 3-room Q1 series 4,434,300 / 4,310,100 / 4,993,800; 5,100,300 / 5,120,300; 4,759,300 / 5,192,200 / 4,878,400; 3,293,800 / 3,672,700 / 3,704,300 | trend table | R58 |
| 12.7%; 3.8%; 4.0%; 28.3%; 3.1% | trend paragraph | R59 (computed) |
| 10%-15%; 11% | trend paragraph | R64 |
| 15.9.2026; 0.9% | trend paragraph | R67 |
| 63,000-66,000 (4.2026) | ₪/m² table | R61 |
| 59,200-76,400 (2026) | ₪/m² table | R72-R77 (min R74, max R72) |
| 80,000-110,000 | ₪/m² table, למי מתאים, FAQ | R63 |
| 2,500,000-3,700,000; 40-54 m² | ₪/m² table | R62 |
| 93,600; 156 m² roof | how to read ₪/m² | R68, R87 |
| 76,400; 70,300 (ground floor) | how to read ₪/m² | R72, R73 |
| חנקין 3: 5 rooms, 188, 26, 156, floor 7, 17,600,000, 93,600, 3.2026 | deals table | R68 |
| ז'בוטינסקי 133: 280, 113, 28, floor 8, 22,000,000, 78,600, 12.2025 | deals table | R69 |
| רמז 27: 277, 22,850,000, 82,500, 10.2026 | deals table | R70 |
| ז'בוטינסקי 105: 5 rooms, 156, 170, 11,000,000, 70,500, 8.2026 | deals table | R71 |
| דוד ילין 9: 4, 110, 8,400,000, 76,400, 4.2026 | deals table | R72 |
| מוסינזון 17: 4, 102, 7,170,000, 70,300, 4.2026 | deals table | R73 |
| שלומציון המלכה: 4, 103, floor 1 of 7, 6,100,000, 59,200, 5.2026 | deals table | R74 |
| אפשטיין 7: 3, 70, floor 6, 4,880,000, 69,700, 4.2026 | deals table | R75 |
| ויצמן 50: 3, 75, floor 2, 4,750,000, 63,300, 4.2026 | deals table | R76 |
| בן שפרוט 21: 2, 46, 3,180,000, 69,100, 4.2026 | deals table | R77 |
| 5%-10% ask-to-close | asking intro | R65 |
| ה' באייר 18: 5, 161, 12, 14,500,000, 90,000 | asking table | R78 |
| ה' באייר 2: 4, 142, 23, 11,250,000, 79,200 | asking table | R79 |
| משה שרת: 4, 125, 3, 6,500,000, 100,000, 52,000 | asking table | R81 |
| ה' באייר 16: 4, 107, 4, 4,590,000, 42,900 | asking table, paragraph | R80 |
| דוד ילין 10: 2.5, 84, 1, 4,400,000, 90,000, 52,400 | asking table | R82 |
| 500 listings; 10% at signing | asking paragraph | R66 |
| 260,750; 562,479 | tax example | R84 (brackets R83) |
| 78 dunam | Kikar | R37 |
| 40 / 40 / 37 floors; 453 apartments | Kikar | R34 |
| 40 dunam park; 18 + 6 classrooms | Kikar, למי מתאים | R35 |
| end 2026; Q1 2027 | Kikar | R36 |
| half a year to two years | Kikar | R38 |
| almost 40%; 33%; 2022 | renewal | R39 |
| 7 to 9 floors; 18 to 22 m² | renewal | R40, R41, R42, R43 |
| בארי 36-56: 11 buildings, 190, 500, 3.2026, 13 dunam | renewal table and paragraph | R44 |
| ז'בוטינסקי 135-137: 32 → 9 floors, 68; 8.2024 | renewal table | R45 |
| ז'בוטינסקי 152: 4 floors, 20 → 8 floors, 38; last quarter of 2028 | renewal table | R43 |
| ז'בוטינסקי 133: 16 → 9 floors, 33; 11.2025 | renewal table | R46 |
| זכרון יעקב 16: 3 floors, 12 → 7 floors, 26; 24.11.2024; second half of 2028 | renewal table | R50 |
| רמז 44: 7 floors, 25; 9.12.2025; 18-24 months | renewal table and paragraph | R47, R91 |
| רמז 22 / 25 / 42: 32 / 26 / 20 | renewal table | R47 |
| רמז 27: 4 floors, 14 → 9 floors, 24; 2.2026 | renewal table | R42 |
| זלוציסטי 4: 4 floors, 12 → 8 floors, 22; 2.2026 | renewal table | R41 |
| שרת 30: 4, 11 → 8, 24; 7.2026 | renewal table | R49 |
| ליסין 27: 4, 12 → 7, 21; 7.2026 | renewal table | R48 |
| חנקין 3: 3.2026 | renewal table | R68, R51 |
| until 2028 (works) | למי מתאים | R43, R50 |
| August 2023 (red line) | transport | R31 |
| June 2028 (purple line) | transport | R32 |
| 2030 (green line) | transport | R33 |
| 8,000 (Rova 3); 30s-40s | comparison, FAQ | R11, R12 |

Unmapped numbers: none.

## 6. Links (HTTP status checked with curl -L on 7.10.2026, 08:00 UTC)

| link | anchor | status |
|---|---|---|
| https://nad-lan.co.il/north-tel-aviv/bavli/ | שכונת בבלי | 200 |
| https://nad-lan.co.il/north-tel-aviv/ | צפון תל אביב | 200 |
| https://nad-lan.co.il/purchase-tax-calculator/ | מחשבון מס רכישה | 200 |
| https://nad-lan.co.il/apartment-purchase-cost-calculator/ | מחשבון עלויות רכישת דירה | 200 |
| https://nad-lan.co.il/tel-aviv-apartment-prices/ | מחירי דירות בתל אביב | 200 |
| https://nad-lan.co.il/projects/hamedina/ | מגדלי כיכר המדינה (exact anchor as required) | 200 |
| https://nad-lan.co.il/urban-renewal/ | התחדשות עירונית | 200 (checked before linking) |
| https://nad-lan.co.il/north-tel-aviv/old-north/ | הצפון הישן (once, in "רובע 4 או הצפון הישן?") | 200 |
| target https://nad-lan.co.il/north-tel-aviv/rova-4/ | (the page itself) | 404, free |

8 internal links, all absolute, all to the allowed list. No external links in the body.

## 7. Deals vs asking

Deals and asking prices sit in separate tables; no average mixes them. ₪/m² ranges are labelled by type (מחיר שיווק /
עסקאות). The calculator's "resale" range (59,000-70,000) uses deals only (R73-R77, R74); the 42,900 asking is text only.

## 8. Conflicts with existing nad-lan pages (to fix in a separate task; nothing was edited)

1. /north-tel-aviv/old-north/ (section "מהו הצפון הישן וגבולותיו") describes the Old North as reaching "צירים מרכזיים כמו אבן
   גבירול וסביבת כיכר המדינה". Kikar HaMedina is in Rova 4 (east of Ibn Gabirol), not the Old North (R1, R11, R13).
2. /north-tel-aviv/bavli/ (section "השוואה לשכונות סמוכות בצפון הישן") says Bavli "שייכת מבחינה תודעתית ותכנונית למרחב של
   הצפון הישן". Officially Bavli is in Rova 4, הצפון החדש (R5).
3. /north-tel-aviv/miriam-hahashmonait/ is titled "מרים החשמונאית, התחדשות עירונית בצפון הישן"; the official street list puts
   מרים החשמונאית in "הצפון החדש, החלק הצפוני" (R13).
4. /north-tel-aviv/ hub lists the area's neighbourhoods without the New North / Rova 4 and without Kikar HaMedina; it should
   link down to the new page once it is live.
5. /projects/hamedina/ is consistent (it says "הצפון החדש, סביבת כיכר המדינה"; transport table matches R31-R33).
6. Renderer: scripts/project-stage/price_guide/render.py assumes a tower floor mode in modes[0]; pricedata.json (area mode)
   needs an area branch before it can render.
