# /sde-dov/ (page 4730): number audit and alignment edits (HAD-439 Stage A, 7.10.2026)

Companion to align-edits.json in this folder. Data only: nothing was applied, nothing published, nothing committed.
The hub had never been audited. Every number in its body was checked against the repo's facts and public sources.
The prices page (/sde-dov/prices/, page 4758) is NOT in this audit: it was aligned today (78 edits,
docs/content/sde-dov-prices-2026-10/) and is live with them (re-read below); its claims are in claims.json as live.

## 1. Method

- Content: public `GET https://nad-lan.co.il/wp-json/wp/v2/pages/4730?_fields=id,link,title,content,yoast_head_json,modified_gmt`
  (content.rendered), retrieved 2026-10-07 20:08:23 UTC (page modified_gmt 2026-10-07 11:35:15, the AreaMap shortcode added
  by another session). Saved: `source/hub-4730-rest.json`. The prices page the same way (20:08:24 UTC, modified_gmt
  10:31:34, the 83,000 average and no 81,000: the 78 edits are live): `source/prices-4758-rest.json`.
- Live H1 (in the content, `nlseo-h1-v1`): "רובע שדה דב: פרויקטים ודירות למכירה"; 17 article H2s plus the AreaMap's own H2.
- Every number token in the visible article (the AreaMap component cut out) was extracted by script: 92 tokens before the
  edits, grouped into 22 distinct number claims (audit ids below, plus two non-number findings that sit in the same
  sentences). Each claim was checked against the repo (scripts/project-stage/price_guide/sde-dov-prices.json and its
  sources, docs/qa/had-460/sde-dov-prices-audit.md, docs/design/area-map-3d/sde-dov-sources.json) and public sources opened
  today (section 3, with retrieval times).
- 33 edits. A script applied them in order to the saved content.rendered: each "old" matches exactly once and still once
  after the earlier edits; all 33 also match exactly once in the raw post content backed up at 14:35 Israel time
  (`docs/qa/had-460/city-backup/page-4730-20261007T143514.json`, the state just before the AreaMap shortcode was added).
  No new text has an em dash, an en dash, "!" or an HTML entity. Result: `source/hub-4730-after-edits.html`.
- Not edited: the title, the H1, the URL, the Yoast title and description, the AreaMap shortcode, every H2/H3 except ONE
  (the H2 "הקרקע והמיקום: כ-1,500 דונם על חוף צפון תל אביב" carries a wrong number: edit 2).
- After the edits the translation gate (`check_translation.py --selftest`, live and --offline) finds **148 number tokens, 0
  unmatched** on the hub's translation source and **317 tokens, 0 unmatched** on the prices page; H1 1, banned 0, dashes 0,
  external links 0, heading duplicates 0, marker in place. Before the edits the same gate finds 14 tokens no claim supports
  (section 5).

## 2. Counts and the area decision

| | distinct claims | |
|---|---:|---|
| number claims in the hub body before the edits | 22 | 92 number tokens |
| CONSISTENT (kept as is) | 9 | A-02, A-03, A-04, A-07, A-08, A-11, A-13, A-15, A-24 |
| CONSISTENT, date or precision added | 4 | A-09, A-12, A-17, A-20 |
| CONFLICT with a dated source | 4 | A-05, A-10, A-14, A-22 (and A-06, boundaries, not a number) |
| STALE | 3 | A-01, A-19, A-23 |
| UNSOURCED | 2 | A-16, A-18 |
| **unsourced or conflicting numbers after the edits** | **0** | |

Edits by verdict: 10 CONFLICT, 5 UNSOURCED, 1 STALE, 3 CONSISTENT+DATE, 2 DATE, 5 STYLE (em dashes only), 1 TEXT (optional,
a broken FAQ sentence), 6 ADDED (optional: project facts the AreaMap cards on the same page already show).

**The area: about 1,300 dunam, not 1,500.** Three independent official readings agree: the municipality's Sde Dov page
("התוכנית כוללת כ-1,300 דונם", read 20:12 UTC), the district committee's approval for validity (12.3.2020: "שטחה הכולל
הוא כ-1,300 דונם") and the city GIS polygon of plan 4444 (Shape_Area 1,304,428 m², read 20:15 UTC; it holds all three
compounds: Eshkol 341, Centre 570, North 394 dunam). The 1,490 / 1,500 / 1,600 figures come from a 2022 press article, a
marketing site and Google's AI overview quoting that site: none is official, and the municipal neighbourhood polygon is
1,342 dunam (it leaves out Eshkol and adds the beach). Decision: about 1,300 (H2, text, FAQ).

### The top conflicts

1. **The area, "כ-1,500 דונם" in an H2 and "1,300 עד 1,500" in the text** (A-05): official about 1,300 (above).
2. **"כ-4,500 עד 6,900 יחידות דיור מיוחד"** (4 places, A-10): the approval of 12.3.2020 says 2,400 affordable + 4,500 special
   = 6,900 in all; 6,900 was misread as an upper bound. Now "כ-4,500", dated "לפי התוכנית שאושרה ב-2020".
3. **Eshkol "כ-70,000 עד 80,000 ₪ למ"ר" and "100 מ"ר = כ-8 מיליון"** (4 places each, A-16, A-18): no source. Replaced by the
   prices page's own sourced numbers: 2025 project averages in Eshkol 63,400-82,600 incl. VAT, most projects about 70,000 in
   2026, the survey average 83,000 (4.2026), and the PriceGuide calculator's 100 m² = 7 to 8.3 million (CALC).
4. **Rainbow "כ-480 יחידות דיור לפי שיווק וכ-459 לפי היתר"** (A-14): 480 is the 2021 land-tender figure; 459 is the
   developer's and the contractor's (1.1.2026). No source says "per permit". The "39 to 40 floors" range is kept (deal
   records 39, contractor 40).
5. **"מכרזי קרקע שיקפו מעל 3 מיליון ₪ קרקע ליחידה"** (A-19): true only for 2022 (3.3M average incl. development); the
   February 2025 for-sale tender reflected 1.7-2.2M per unit.
6. **"תכנית המתאר אושרה בשנת 2020, ומתחם אשכול בדרום קדם לה"** (A-22): Eshkol's detailed plan came into force 20.5.2021,
   after the master plan (9.8.2020); Centre 13.2.2025, North 8.6.2025 (city GIS). The municipal page still says the North
   is "in approval": the GIS layer says in force since 8.6.2025.
7. **Boundaries** (A-06, not a number): "from the port of Tel Aviv in the south ... to the continuation of Ibn Gabirol in the
   east" is wrong on both counts (the port is south of the Yarkon; Ibn Gabirol's continuation runs through the quarter).
   Replaced by the municipality's boundary description, in the same sentence as the area fix.

## 3. Source keys

Keys of the prices data (NC2604, ICE1904, ICE0305, ICE2105, ICE0606, BZ2606, ICE2510, NC2507, BZ2512, NC2604F, BZ2605,
GL2608, GL2410, GL2609, ICE2512, TA) are defined, with URL, what they say and when they were read, in
`scripts/project-stage/price_guide/sde-dov-prices.json` ("sources"); GL2311, BZ2608 and NC2503 in
`docs/content/sde-dov-prices-2026-10/align-check.md` section 3. Keys opened for this audit:

| key | source | date | read (UTC, 7.10.2026) | says |
|---|---|---|---|---|
| TLVSD | Tel Aviv-Yafo municipality, https://www.tel-aviv.gov.il/Residents/Development/Pages/SdeDov.aspx | live page | 20:12:21 | boundaries (N Tzukei Aviv and Propes St; E Neve Yam, Tochnit Lamed, Levi Eshkol; S Kochav HaTzafon, Reading, Shai Agnon; W the beach and promenade); master plan approved August 2020, about 1,300 dunam; 16,000 apartments, about 40,000 residents; commerce about 126K m², employment about 330K m², about 2,000 hotel rooms; Eshkol (TAMAL/3001, May 2021) about 4,800 units, 45,000 m² commerce, 145,000 m² employment; Centre (approved 2025) about 7,100 units, 60,000 / 155,000 m², 800 hotel rooms; North about 4,000 units, 20,000 / 30,000 m², 1,150 hotel rooms |
| TLVSP | https://www.tel-aviv.gov.il/Residents/Development/Pages/SdeDovPublicParticipation.aspx | live page | 20:12:24 | five participation meetings for the master plan; four topic meetings for the detailed plans (traffic and transport; urban design, environment and sustainability; building and programme; housing) |
| GIS528 | city GIS layer 528, query oid_taba IN (4523, 4524, 4526, 4609), https://gisn.tel-aviv.gov.il/arcgis/rest/services/IView2/MapServer/528/query | live | 20:15:54 | plan 4444 in force 9.8.2020, 1,304,428 m²; TAMAL 3001 Eshkol 20.5.2021, 341,324 m²; 1/4444 Centre 13.2.2025, 569,679 m²; 2/4444 North 8.6.2025, 393,615 m² |
| NC2003 | https://www.nadlancenter.co.il/article/2402 | 12.3.2020 | 20:13:18 | district committee approval for validity: 16,000 units, about 500,000 m² public buildings, 125,000 m² commerce, 330,000 m² employment, 125,000 m² hotels, about 365 dunam of parks and public gardens; 2,400 affordable, 4,500 special-housing units; total about 1,300 dunam |
| NC2502 | https://www.nadlancenter.co.il/article/11492 | 3.2.2025 | 20:13:18 | appeals committee clears the Centre plan: 7,128 units; "more than 7,100 units", about 60,000 m² commerce, 155,000 m² employment, about 800 hotel rooms |
| ICE2502b | https://www.ice.co.il/realestate/news/article/1049923 | 4.2.2025 | 20:13:19 | the Israel Land Authority opens tenders for 6,084 units plus 650 assisted-living units, bids until 19.2 or 24.3 |
| NC2502T | https://www.nadlancenter.co.il/article/11602 | 19.2.2025 | 20:13:20 | tender results: land for 3,922 units signed; the regular tender's results reflect land value of 1.7 to 2.2 million per apartment; Hagag 350 units, Gindi two compounds for 708 units |
| BZ2502 | https://www.bizportal.co.il/realestates/news/article/20013735 | 19.2.2025 | 20:13:20 | average land price per unit about 1.9 million incl. development; earlier Eshkol tenders peaked at 3.3 million per unit |
| ICE2502 | https://www.ice.co.il/realestate/news/article/1052128 | 19.2.2025 | 20:13:19 | in the 2022 tenders the average land price per unit was about 3.3 million incl. development |
| BZ2503 | https://www.bizportal.co.il/realestates/news/article/20015126 | 26.3.2025 | 20:14:55 | four more tenders closed for 2,744 units; "the eight tenders closed in the quarter, including February's"; 3,922 units in February (3,922 + 2,744 = 6,666) |
| ICE2603 | https://www.ice.co.il/realestate/news/article/1104529 | 5.3.2026 | 20:14:54 | context only: two 2025 winners paid 3.0 and 3.1 million per unit (so "over 3 million" was true for single bids, not as a level) |
| NC2502P | https://www.nadlancenter.co.il/article/11538 | 10.2.2025 | 20:14:25 | the coastal park is 2 km long and covers 240 dunam (runway park 30, linear park 43) |
| NC2601R | https://www.nadlancenter.co.il/article/13606 | 1.1.2026 | 20:14:25 | Ashtrom main contractor for Rainbow: a 40-floor tower and 6 more buildings of 8 floors, about 459 units, about 1,600 m² commerce; delivery in stages, the last in about 4.5 years; works from January 2026 |
| ASHT | https://ashtromconstruction.co.il/en/projects/rainbow-tlv | live page | 20:14:26 | 8 residential buildings, 459 apartments, about 8 dunam, a 40-story tower; completion within five years |
| HEWSD | he.wikipedia "נמל התעופה דב הוז" (API parse, revid 42924440) | live | 20:14:03 | opened 23.9.1938 with the Tel Aviv - Haifa - Beirut line; stopped operating 1.7.2019; evacuation completed 10.2.2020 |
| AMS | docs/design/area-map-3d/sde-dov-sources.json (the AreaMap research: city GIS lot polygons, local committee documents, press; each with its URL and time) | 7.10.2026 | 10:04-10:22 (that session) | Rainbow 459 units (480 in the tender, Mako), tower floor 13 "of 39" (GL2311); DIMRI YAMA 458 (40 + 16 + 9 + 9 floors); ASHIRA 406 (35-floor tower, 4 buildings); UTOPIA 337 (4 buildings, courtyard); ZOHI 230; GINDI VOGUE 708 (lots 2255 and 2206); FIRST 350 (45 floors + three of 9) |
| CALC | this audit | | | 100 m² x 70,000-83,000 = 7.0-8.3 million (as the PriceGuide calculator, area_default 100) |
| THIS | this edit set | 7.10.2026 | | the page is updated by it |

DataForSEO (keywords, SERP) is recorded in serp.md, not here.

## 4. Every number claim in the hub, with its verdict (audit ids A-01 to A-24; not the claims.json ids)

| # | claim (Hebrew as on the page) | where (occurrences) | verdict | source | edit |
|---|---|---|---|---|---|
| A-01 | נבדק ועודכן: יוני 2026 | date line (1) | STALE | THIS | 1 |
| A-02 | השדה נחנך ביום 23 בספטמבר 1938, קו תל אביב-חיפה-ביירות | history (1) | CONSISTENT | HEWSD | none |
| A-03 | השדה נסגר ביום 1 ביולי 2019 | history (1) | CONSISTENT (English sources say 30.6, the last day of flights) | HEWSD | none |
| A-04 | הפינוי הושלם בתחילת 2020 | history (1) | CONSISTENT (10.2.2020) | HEWSD | none |
| A-05 | כ-1,500 דונם / כ-1,300 עד 1,500 דונם | H2, text (2) | CONFLICT | TLVSD, NC2003, GIS528 | 2, 3, 17 |
| A-06 | מנמל תל אביב בדרום ... עד המשך אבן גבירול במזרח (not a number) | text, FAQ (2) | CONFLICT | TLVSD | 3, 17 |
| A-07 | חזית חוף של כ-2 ק"מ | text (1) | CONSISTENT (the coastal park is 2 km) | NC2502P | none |
| A-08 | 16,000 דירות ל-40,000 תושבים (also "16 אלף") | H2, plan, table, FAQ, summary, planning (11) | CONSISTENT | TLVSD, NC2003 | none |
| A-09 | 500,000 מ"ר מבני ציבור, 125,000 מ"ר מלונאות, 365 דונם פארקים, 2,400 דב"י | plan, table, transport, affordable, FAQ (12) | CONSISTENT, undated: "לפי התוכנית שאושרה ב-2020" added where rewritten | NC2003 | 4, 16, 19 |
| A-10 | 4,500 עד 6,900 יחידות דיור מיוחד | plan, table, affordable, FAQ (4) | CONFLICT (6,900 = 2,400 + 4,500) | NC2003 | 4, 5, 16, 19 |
| A-11 | Eshkol 4,800 / 45,000 / 145,000; Centre 7,100-7,128 / 60,000 / 155,000 / 800 rooms; North 4,000 / 20,000 / 30,000 / 1,150 rooms | compounds table, FAQ (15) | CONSISTENT | TLVSD, NC2502 | none |
| A-12 | בפברואר ומרץ שמונה מכרזים, 6,666 יחידות, יותר מ-40% | compounds (1) | CONSISTENT, undated: 2025 added | BZ2503, NC2502T | 6 |
| A-13 | Rainbow: מגדל בן 39 עד 40 קומות | table, H3 paragraph (2) | CONSISTENT (39 deal records, 40 contractor) | AMS, NC2601R | kept in 7, 8 |
| A-14 | Rainbow: כ-480 לפי שיווק, כ-459 לפי היתר | table, H3 paragraph (2) | CONFLICT (attributions) | NC2601R, AMS, GL2608 | 7, 8 |
| A-15 | Rainbow: קבלן אשטרום, אכלוס צפוי 2030 | table, paragraph, investment, FAQ (4) | CONSISTENT (last stage about 4.5 years from 1.2026) | NC2601R, ASHT | 7, 8 (wording) |
| A-16 | אשכול: כ-70,000 עד 80,000 ₪ למ"ר | prices, table, investment, FAQ (4) | UNSOURCED | replacement NC2604, ICE1904, ICE2105, ICE0606 | 9, 10, 15, 18 |
| A-17 | Rainbow: ממוצע סביב כ-82,000 ₪ למ"ר | prices, table, investment, FAQ (4) | CONSISTENT (81,782 to 3.2026): aligned to 81,800 with its date | BZ2605 | 9, 11, 15, 18 |
| A-18 | דירת 100 מ"ר כ-8 מיליון ₪ | prices, table, FAQ (3) | UNSOURCED (100 x the unsourced 80,000) | CALC | 9, 12, 18 |
| A-19 | מכרזי קרקע מעל 3 מיליון ₪ ליחידה | prices, table (2) | STALE (2022: 3.3M; 2.2025: 1.7-2.2M) | ICE2502, BZ2502, NC2502T | 9, 13 |
| A-20 | עסקאות יוקרה של 14 מיליון ₪ ומעלה | prices, table (2) | CONSISTENT (10.2024): the 12.2025 record deal added | GL2410, BZ2512, NC2604F | 9, 14 |
| A-21 | דמי הניהול: "., גובה דמי הניהול בכל פרויקט." (broken text, not a number) | FAQ (1) | TEXT | THIS | 20 (optional) |
| A-22 | תכנית המתאר אושרה בשנת 2020, ומתחם אשכול קדם לה | planning (1) | CONFLICT (dates) | GIS528, TLVSD | 21 |
| A-23 | הנתונים נבדקו מול המקורות ב-18.8.2026 | planning note (1) | STALE | THIS | 27 |
| A-24 | חמישה מפגשים; ארבעה מפגשי נושא (words) | planning (2) | CONSISTENT | TLVSP | none |

Not numbers, read on the way and kept: the developer list, DIMRI YAMA's architect and interior designer, the Green Line
through the quarter (TLVSD), FIRST as "a luxury tower" (its facts are in optional edit 28).

## 5. Before and after (the translation gate on the Hebrew)

- Before the edits: 92 number tokens, 14 with no supporting claim: 1,500 (x2), 6,900 (x4), 80,000 (x4), 82,000 (x4), and 6
  em dashes in the translated part. The gate cannot see a wrong attribution or a stale level written with small numbers (480
  "per marketing", "8 million", "over 3 million", "2020 ... Eshkol preceded it"): the audit above did.
- After the edits: 148 tokens, 0 unmatched; H1 1; banned 0; dashes 0; external links 0 (the official-sources list is not part
  of the translation source); heading duplicates 0 against /new-projects/, /guides/, /brokers/, /developer-deals/,
  /projects/hamedina/, /north-tel-aviv/, /north-tel-aviv/rova-4/ and the prices page. The prices page as live: 317 tokens, 0
  unmatched.
- Soft style words left in the Hebrew (warnings, not edited, outside this task): "יחסית", "כמעט", "מנגנון", "שכבה",
  "בבדיקה" (10 on the hub, 8 on the prices page).

## 6. Found but not edited (for the owner or a later edit)

- **Heading overlap on the Hebrew site:** the hub's H2 "בדיקות משפטיות לפני רכישה על הנייר בשדה דב" starts with the same four
  words as an H2 on /projects/dimri-yama-sde-dov/, /projects/zohi-sde-dov/ and /projects/gindi-vogue-sde-dov/. Headings are
  outside this task; the Hebrew self-test therefore compares the hub with the Hebrew hubs only (the translations ARE compared
  with the -en/-fr/-ru/-ar project pages, where this overlap does not exist).
- The prices page's Yoast title is 69 characters ("מחירי דירות בשדה דב - מחיר למ״ר, טבלאות השוואה וסקירת שוק | נדל"ן חכם"),
  over the 60 the gate asks of the translations, and it still ends with the old brand "נדל"ן חכם"; the prices page's footer
  box also says "נכתב ונערך בידי מערכת נדל״ן חכם".
- The hub keeps an external "מקורות תכנון רשמיים" list (6 links with em dashes) and a closing box with an em dash; both are
  left out of the translations, and the owner's research law keeps sources internal.
- The compounds table says Eshkol is "ממוקם על מסלול ההמראה לשעבר"; the municipality places the runway park in the North
  plan. Not a number; not verified further.
- The municipal Sde Dov page still says the North plan is "in approval" (the GIS says in force since 8.6.2025) and gives
  newer housing figures (about 7,000 units for households priced out of the market, about 2,100 of them municipal affordable
  rentals, about 900 assisted-living units on three lots) than the 2020 approval the hub quotes. The hub now dates its
  figures ("לפי התוכנית שאושרה ב-2020"); a later content pass could add the municipal figures.
- Google's US AI overview for "sde dov" leads with PFAS soil and groundwater contamination reports (2026). The Hebrew hub
  does not mention them; the translations must not add them. Worth a dated, sourced paragraph in the Hebrew first (the
  owner's call).
- The investment paragraph still says "אכלוס צפוי בשנת 2030 בפרויקט Rainbow Tel Aviv, לפי פרסומי היזם": consistent, but
  2030 is the last stage per the contractor; the table and the project paragraph now say so.

## 7. Apply notes

- Order: 1 to 33. Edits 20 and 28-33 are optional and independent of the others.
- Re-fetch the page and re-check every "old" against the raw content right before applying (other sessions edited this page
  today).
- After applying: re-fetch, run `python tools/source_audit.py` on /sde-dov/ (public-source law), run
  `python docs/content/sde-dov-i18n-2026-10/check_translation.py --selftest --live` (expect PASS), and confirm the H1, the 17
  H2s (one changed: "כ-1,300 דונם") and the AreaMap are in place.
- The language versions must be built from the Hebrew AFTER these edits (the packets already are: build_packets.py applies
  align-edits.json in memory through check_translation.hebrew_source()).
