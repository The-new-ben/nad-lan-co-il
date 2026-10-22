# Contractor register check: research brief (page + tool)

Prepared 22.10.2026 by a research agent (Opus 5.5) for nad-lan.co.il. Read-only on the live site: nothing was written to WordPress.
All retrieval times are Israel time (UTC+3) on 22.10.2026 unless stated.

Intent: "בדיקת קבלן רשום" and its family (פנקס הקבלנים, רשם הקבלנים, קבלן רשום, סיווג קבלנים).

---

## 0. The short version

| Item | Value | Evidence |
|---|---|---|
| Official dataset | "פנקס הקבלנים הרשומים", Ministry of Construction and Housing, data.gov.il package `pinkashakablanim`, resource `4eb61bd6-18cf-4e7c-9f9c-e166dfa0a2d8` | CKAN `package_show`, 19:14 |
| Rows | **24,373** (one row = contractor x branch) | `datastore_search` total, full download 19:14 |
| Contractors | **17,874** unique contractor numbers; 8,861 companies (with a company number), 9,013 individuals | `raw/register.json` |
| Last update | resource `last_modified` **17.08.2026 00:01** (declared weekly, automatic, but nothing new for 9+ weeks); newest registration date in the file 15.08.2026 | CKAN |
| Licence | CKAN licence field is **empty** (`license_id` "", `isopen` false). data.gov.il site terms apply; no named licence | CKAN |
| Our contractor pages | 2,699 with profession `kablan`; **2,690** match a current register number; 8 carry numbers no longer in the register; 1 is a demo page | public REST, 19:20 |
| Register contractors with no page on nad-lan | **15,184** of 17,874 (85%) | match by contractor number |
| Proposed URL | **/pinkas-hakablanim/** (new page; head word "pinkas" is unowned) | `url_word_audit.py`, 19:31 |
| H1 | בדיקת קבלן רשום: חיפוש בכל הקבלנים בפנקס הרשמי | `title_start_audit.py` OK |
| SEO title (54 chars) | פנקס הקבלנים: בדיקת קבלן רשום לפי שם, מספר, עיר וסיווג | OK |
| Breadcrumb | רשם הקבלנים | OK; trio check OK |
| Tool data | compact JSON for all 17,874 contractors = **1.28 MB raw / 354 KB gzip**; recommended: server search endpoint returning about 5 KB per query | `raw/tool-data-prototype.json` |
| Demand | head five terms 11,360 searches a month; the whole measured family about 14,400 after removing Google's close-variant duplicates | `keywords.csv` |
| AI overview | present on all 5 SERPs checked | `serps.json` |
| DataForSEO spend | about $0.20 (two search-volume calls at $0.09 each, confirmed for one, plus five live SERP calls) | API responses |

---

## 1. Official data

### 1.1 The dataset (data.gov.il)

- Package page: https://data.gov.il/dataset/pinkashakablanim (organisation: משרד הבינוי והשיכון, contact datagov@moch.gov.il).
- Description in CKAN: the register of registered contractors and the classification of works they are allowed to do. It is meant for citizens, local authorities and government offices.
- API that works (file download often returns 403; the datastore API did not):
  `https://data.gov.il/api/3/action/datastore_search?resource_id=4eb61bd6-18cf-4e7c-9f9c-e166dfa0a2d8&limit=5000&offset=N`
  Five calls of 5,000 rows each fetched everything (19:14). File: `raw/register.json` (14.5 MB, all fields, with `retrieved_utc`).
- Declared update frequency: weekly, automatic. Real state: last modified 17.08.2026, so the open data is about 9 weeks behind the live register. The tool must show "נכון ל-17.8.2026" and send users to the live official record for current status.
- Related datasets searched: the ministry has 12 datasets on data.gov.il; the only other professional list is "רשימת מתכננים ומודדים" (`metachnenim`). There is **no** separate open dataset for "קבלנים מוכרים" or "קבלני שיפוצים". Recognised contractors are a column in this dataset (`KABLAN_MUKAR`), and renovation contractors are branch 131 in it. The Ministry of Finance keeps its own recognised-contractors list at https://asset.mof.gov.il/contractorRepository/s/ (ranks on page 1 for "פנקס הקבלנים" and "סיווג קבלנים").

### 1.2 Fields (Hebrew label from CKAN, then meaning)

| Field | Hebrew label | Meaning and notes |
|---|---|---|
| MISPAR_YESHUT | מספר ישות | Company number for companies (9 digits, mostly 51xxxxxxx). **Empty for all individuals** (11,414 rows): personal ID numbers are not published. |
| SHEM_YESHUT | שם הישות | Contractor name as registered; sometimes the licensed dealer's name. |
| MISPAR_KABLAN | מספר קבלן | Contractor licence number in the ministry systems. It is also the id in the official record URL: `https://www.gov.il/apps/moch/rasham/details/{MISPAR_KABLAN}` (checked live on 6866, 19:23). |
| SHEM_YISHUV | שם ישוב | City (945 distinct values; trailing spaces in the raw data). |
| SHEM_REHOV, MISPAR_BAIT | שם רחוב, מספר בית | Street and house number. |
| TAARICH_KABLAN | (no label) | First registration date (1977 to 15.08.2026). |
| MISPAR_TEL | מספר טלפון | Phone (filled in 23,821 rows). |
| EMAIL | כתובת דוא"ל | Email (filled in 23,497 rows). |
| KOD_ANAF | קוד ענף | Branch code (32 branches). |
| TEUR_ANAF | תיאור ענף + הערות | Branch name. A restriction is appended after " - " (see 1.4). |
| KVUTZA | קבוצה | Group א, ב or ג. Per CKAN: groups א and ב belong to secondary branches (renovation, sealing, plumbing, air conditioning); group ג to primary branches (building, infrastructure, roads, water and sewage). In the data each branch has exactly one group. |
| SIVUG | סיווג | Level ק or 1 to 5. Group plus level sets the money (or sqm) limit. |
| TARICH_SUG | תאריך הסיווג | Date of the last classification. |
| HEKEF | היקף (באלפי ש"ח) | Max work per one site in thousand NIS, per the law. **Outdated**: these are the amounts valid 1.4.2026 to 1.10.2026 (see 1.5). "ב.מ." = unlimited. |
| KABLAN_MUKAR | קבלן מוכר | "לא מוכר" or "מוכר בסיווג N" (recognised for government works). |
| OVDIM | עובדים בענף | The qualified people the licence rests on (names). |
| HEARA | הערה | Registration basis: "על סמך כישורי המנהל" (20,886 rows) or "על סמך העסקת עובדים מקצועיים" (3,487). |

### 1.3 Counts (full detail in `register-fields.json`)

- Groups (rows): ג 10,671 · א 9,357 · ב 4,345.
- Level (rows): 1 17,863 · ק 2,707 · 2 1,216 · 5 1,147 · 3 883 · 4 557.
- Group x level (rows): א-ק 2,707 · א1 6,052 · א2 251 · א3 134 · א4 74 · א5 139 · ב1 3,756 · ב2 217 · ב3 176 · ב4 76 · ב5 120 · ג1 8,055 · ג2 748 · ג3 573 · ג4 407 · ג5 888.
- Contractors per branch (top): 100 בניה 8,482 · 131 שיפוצים 4,913 · 200 כבישים תשתית ופיתוח 1,972 · 260 קווי מים ביוב וניקוז 1,851 · 160 חשמלאות ותקשורת במבנים 1,437 · 130 בטונים ובניית שלדים 721 · 111 פיתוח חצרות 620 · 190 תברואה, אינסטלציה וכיבוי אש 548 · 210 עפר וחציבה 492 · 270 קווי חשמל ותאורת רחובות 459 · 170 מיזוג אוויר וקירור 440 · 135 הרחבת מבנים 430 (32 branches in all).
- Recognised for government works (rows): 1,258 (level 1 340 · 2 245 · 3 166 · 4 127 · 5 380).
- New contractors by first registration year: 2022 1,227 · 2023 1,531 · 2024 1,306 · 2025 1,288 · 2026 (to 15.8) 778.
- Top cities (rows): ירושלים 1,597 · תל אביב-יפו 785 · באר שבע 699 · ראשון לציון 621 · פתח תקווה 584 · נצרת 541 · חיפה 517 · אשקלון 487 · אום אל-פחם 487 · חולון 413.

### 1.4 Restrictions inside the data

The dataset has no status column. Restrictions are text after " - " in `TEUR_ANAF`:
- "רישיון זה מותלה בפועל כמפורט בפנקס הקבלנים": 14 rows
- "אינה רשאית לבצע עבודות חדשות": 6 rows
- "הקפאת רישיון - מלחמת חרבות ברזל": 3 rows
- Scope limits (air conditioning only without cooling; works within the Electricity Law): 4 rows
- 7 rows end with an empty " - " (no text)

The live record page shows a status column ("רשום" for record 6866). The status meanings are on the official page (1.5). The tool shows a warning badge for the 23 restricted rows and always links to the live record.

### 1.5 Official rules (gov.il pages read in the owner's Chrome, 19:18 to 19:36; gov.il returns 403 to scripts)

| Source | Dates on page | What it says |
|---|---|---|
| https://www.gov.il/he/pages/general_information_for_registration_of_contractors (המדריך לרישום בפנקס הקבלנים) | published 26.11.2018, updated 24.02.2026 | Law: חוק רישום קבלנים לעבודות הנדסה בנאיות, התשכ"ט-1969. Works above the scope or nature set in the regulations must be done only by a registered, licensed contractor. **A main-branch job above 103,250 NIS, or a sub-branch job above 54,000 NIS, requires a registered contractor.** Recommends buyers, home builders, clients and contractors to check the register: registered?, which branches?, which money scopes? |
| https://www.gov.il/he/pages/sivug_kablanim (סיווג קבלנים) | published 13.10.2020, updated 06.10.2026 | Classification regulations of 1988 (תקנות רישום קבלנים לעבודות הנדסה בנאיות (סיווג קבלנים רשומים), התשמ"ח-1988). Five levels; each is the max a contractor may do in his branch **on one site**, excluding VAT, land costs, land taxes and building fees; residential building also in sqm. Amounts change on 1 April and 1 October by the residential construction input index. **Table valid 1.10.2026 to 1.4.2027 (thousand NIS):** ק 846 (branch 131 only, since 13.9.2018) · א 1,994 / 3,988 / 7,977 / 15,954 / unlimited · ב 3,267 / 6,533 / 13,066 / 26,131 / unlimited · ג 5,458 / 9,627 / 19,255 / 38,508 / unlimited · residential sqm 2,000 / 3,000 / 5,000 / 10,000 / unlimited. Upgrade (since 11.5.2017): one site at 70% or more of the current level's max, or two overlapping sites together 100% or more and each 40% or more. |
| https://www.gov.il/he/pages/construction_registry (פנקס הקבלנים) | published 20.05.2022, updated 24.09.2026 | Search by classification as well as number, name, city and branch. The printable certificate lists branches, classifications, qualified staff, first registration date, last classification date, print date and a QR code to the live record. **Statuses:** "מוקפא" = frozen at the contractor's request, may not do building works; "מוחרג" or "מותלה" = by the registrar's decision, may do only the projects listed in the registrar's decisions file and may not take new work. Decisions file dated 24.9.2026. |
| https://www.gov.il/apps/moch/rasham/home (official search) | live | Fields: city picker, branch picker, company number or contractor number, contractor name. reCAPTCHA loads. Results open the record page. |
| https://www.gov.il/apps/moch/rasham/details/6866 (official record) | live | Name, ID number ("לא רלוונטי" for an individual), contractor number, registration date, address, phone, status; then per branch: group, level, classification date, scope, note, registration basis. **It still shows ג1 = 5,332,000**, the April 2026 amount. |
| April 2026 table (registrar's letter signed by Amit Graidy, copy at https://kbh.org.il/wp-content/uploads/2026/04/טבלת-סיווג-קבלני-אפריל-2026.pdf) | valid 1.4.2026 to 1.10.2026 | ק 825 · א1 1,948 · ב1 3,192 · ג1 5,332 ... These equal the dataset's HEKEF values, which proves the HEKEF column is one period old. |
| https://www.gov.il/he/departments/units/contractors_registrar_and_head_of_sales_laws_moch (unit page) | live | The registrar acts under the 1969 law; also cancels registrations, changes classification, takes disciplinary steps, handles residents' complaints, and since amendment 4 of the Sale (Apartments) law (2008) monitors sale guarantees. Head: Amit Graidy. The staff phone shown is 02-5847887 (same as the April letterhead). Google's AI overview shows 02-5847847; **do not publish a phone number until it is read off the official "all contact routes" page.** |
| Law text (secondary): https://he.wikisource.org/wiki/חוק_רישום_קבלנים_לעבודות_הנדסה_בנאיות | 1969 | s.14(a) only a registered contractor licensed for the branch may do works above the regulation thresholds; s.16 offence. Regulations: branches and sub-branches (1993), classification (1988), money scope and professional nature (1984), registration procedures (1988), fees (1980). Classification regulations on Nevo: https://www.nevo.co.il/law_html/law00/74263.htm |

Not verified (do not publish without an official source): registration fees (Midrag quotes 3,780 / 1,890 / 1,789 / 895 NIS), the exact list of "main" versus "sub" branches (the data shows hundreds-codes 100, 200, 300, 400, 500, 700; check the 1993 branch regulations), the registrar's phone and email.

Privacy: the open data carries phones, emails and street addresses of individuals. The tool should show name, city, branches, levels and the official link only; no phone, email or street.

---

## 2. Our pages

Source: `https://nad-lan.co.il/wp-json/wp/v2/nadlan_professional` (meta is public), 29 pages of 100, 19:20. File: `raw/nadlan-professionals.json`.

- 2,847 professional profiles; **2,699** with profession `kablan` (2,698 from `source = pinkas_hakablanim`, 1 `demo_seed`).
- Fields filled on the 2,698 register pages: `registry_number` (= MISPAR_KABLAN), `classification` (text such as "בניה (סיווג 1) · שיפוצים"), `company_name` (= SHEM_YESHUT), `city`, `source_id`, `source_url`. Empty: company number, phone, website, photos, bio.
- `source_url` is the generic search home `https://www.gov.il/apps/moch/rasham/home`, **not** the contractor's own record. Every profile can link the exact record `https://www.gov.il/apps/moch/rasham/details/{registry_number}`.
- What a profile page shows (sample https://nad-lan.co.il/professionals/גבאי-עמרם/, 19:24): title "גבאי עמרם: קבלן בנייה בירושלים | נדלן"; H1 = name; line "רשום בפנקס הקבלנים מאז 2020, מספר 34647"; branches with group-level ("בניה ג-1 · בטונים בנית שלדים ב-1 · שיפוצים א-ק"); city; WhatsApp and quote buttons; "similar professionals"; claim-ownership box; source line "פנקס הקבלנים הרשומים, data.gov.il · עודכן 01/06/2026"; schema `GeneralContractor` with `PropertyValue`. About 344 words.
- Match to the register (17.8.2026): **2,690 pages match**, 0 by company number (we never stored it). **13 pages show branches or levels that differ from the current register** (for example 28016: we show בניה 2, register says 3; 35824: we show one branch, register has three). **8 pages carry numbers that are no longer in the register** (30027 לביא דרור, 25942 אבו סעדה יוסף, 25776 אביטל אבי, 27449 גבארין נביל, 39285 ערבה שלמה, 33624 כהן אמבלו רוברט, 3608 שמי חיים, 10405 גרוס יצחק), so they may describe contractors who left the register (or whose number changed); check each on the official site before any wording change. Reported only; nothing removed.
- Coverage by branch (contractors with a page / in register): 100 בניה 1,144 / 8,482 · 131 שיפוצים 996 / 4,913 · 200 210 / 1,972 · 260 178 / 1,851 · 160 179 / 1,437 · 130 209 / 721.
- **15,184 register contractors have no page with us.** Making pages for them is a mass change (hundreds of pages a day) and needs Ben's word on pace. The tool does not need those pages: it links them to the official record.
- Demo page: https://nad-lan.co.il/professionals/demo-harel-construction/ is titled "קבוצת הראל בנייה - קבלן רשום" and says "חברת בנייה רשומה (סיווג ג-5) ... 14 פרויקטים מאוכלסים". It is labelled "פרופיל לדוגמה" and is `noindex`, but it is counted in the directory's "2,699 בעלי מקצוע" and has no register number. Honesty-law finding: it should not be counted or listed as a registered contractor.
- The archive https://nad-lan.co.il/profession/קבלן/: title "קבלני בנייה וביצוע בפרויקטים באתר", body is one 4,600-word profile of Danya Cebus (the DUO builder). Different intent (contractors of our projects). 7 impressions in 90 days.
- Directory https://nad-lan.co.il/professionals/?profession=kablan: canonical points to /professionals/, so the filtered view cannot rank on its own.

Search Console (sc-domain:nad-lan.co.il, 22.7 to 20.10.2026, pulled 19:29):
- /professionals/ pages: **583 of 1,422 clicks (41%)**, 11,412 impressions, 410 pages with a click. The clicks come from people searching a contractor's name. This is the case for covering all 17,874 names through the tool.
- Zero impressions for פנקס הקבלנים / רשם הקבלנים / קבלן רשום / סיווג קבלנים / בדיקת קבלן רשום. We are absent from these SERPs.
- Filtered evidence: `raw/gsc-contractor-queries-...csv`, `raw/gsc-professionals-pages-...csv`.

---

## 3. Search demand, SERPs and competitors

### 3.1 Volumes (Google Ads, Israel, Hebrew; DataForSEO, 19:15; `keywords.csv` with 12 months)

| Keyword | Monthly | CPC USD | Note |
|---|---|---|---|
| פנקס הקבלנים | 6,600 | 3.73 | peak 8,100 (May 2026) |
| רשם הקבלנים | 2,900 | 4.24 | spike 8,100 in Aug 2026 |
| קבלן רשום / קבלנים רשומים | 880 | 9.46 | one cluster in Google Ads |
| קבלן מוכר / קבלנים מוכרים | 720 | 4.63 | one cluster |
| סיווג קבלנים / סיווג קבלן / סיווג קבלני | 590 | 4.91 | one cluster |
| בדיקת קבלן רשום | 390 | 2.23 | the named intent |
| פנקס קבלנים | 320 | 4.59 | |
| פנקס הקבלנים הרשומים | 260 | 3.86 | |
| רשם הקבלנים טלפון | 260 | 4.88 | |
| איתור קבלן רשום | 210 | 2.67 | |
| רישיון קבלן | 210 | 13.37 | |
| חוק רישום קבלנים | 170 | | |
| בדיקת סיווג קבלן | 140 | 1.57 | |
| קבלן שיפוצים רשום | 140 | 11.08 | |
| רשם הקבלנים סיווג | 110 | | |
| others (רשם קבלנים, קבלן רשום בדיקה, רשימת קבלנים רשומים, ג1, ג5...) | 10 to 90 each | | |

Total of the measured family after removing duplicate clusters: about 14,400 a month. Several long forms (איך לבדוק קבלן רשום, היקף כספי קבלן, רשם הקבלנים חיפוש) have no Google Ads volume.

### 3.2 SERPs (DataForSEO live advanced, desktop, Israel, Hebrew, 19:16; full lists in `serps.json`)

AI overview: **present on all five** (פנקס הקבלנים, רשם הקבלנים, קבלן רשום, סיווג קבלנים, בדיקת קבלן רשום). Every AI overview sends the user to `gov.il/apps/moch/rasham/home` first and repeats the 103,250 / 54,000 NIS thresholds. Other cited sources: greeninvoice, govil.ai, Wikipedia, kolzchut, oron-group, thebuilder, nevo, conwize, kbh, midrag, rishumkablan, oz-shiputsim, lawcase, acb.

Top results:
- **פנקס הקבלנים**: 1 michlal.com (training company) · 2 my.acb.org.il/Search.aspx (**dead: 404 "הדף לא נמצא" when opened 19:38**) · 3 and 6 single gov.il contractor records · 4 medicalmalpractice.co.il guide · 5 top-renovations · 7 Facebook (ministry) · 8 hatikva · 9 MoF recognised list. No PAA.
- **רשם הקבלנים**: gov.il topic page, gov.il search app, Wikipedia, greeninvoice, gam.org.il, gov.il unit page, Facebook video, hatikva, rkablanim. PAA: מהי כתובת רשם הקבלנים? · מהי טבלת הסיווגים של רשם הקבלנים? · מי הוא רשם הקבלנים? · מהן ההחלטות האחרונות של רשם הקבלנים? · מהי אגרת רשם הקבלנים? · איך מגישים בקשה להחלפת עובד ברשם הקבלנים?
- **קבלן רשום**: nadlancenter.co.il, renovations.org.il, yuvalsegal, hatikva, rkablanim (x2), rishum-kablanim, keeperforms; video pack. PAA: איך אני יכול לבדוק אם קבלן רשום ברשם הקבלנים? · מה תפקידו של קבלן בניין? · מהם התנאים להעלאת סיווג רשם הקבלנים? · מה זה קבלן ג2? · איך מוציאים תעודת קבלן רשום? · מהי טבלת הסיווגים של רשם הקבלנים?
- **סיווג קבלנים**: thebuilder, kablanist ("2019-2020" table), yuvalsegal, ramonltd, MoF list, kbh April 2026 PDF, rkablanim, yuvalsegal, rishum-kablanim. No PAA.
- **בדיקת קבלן רשום**: midrag (a registration guide, not a check), gam.org.il, rishumkablan, reporto glossary, a Facebook group post, broker-re, rishumkablan home, a 10-year-old YouTube video, michlal. No PAA.
- Related searches that matter for the tool: חיפוש קבלן רשום לפי שם · בדיקת קבלן רשום לפי ח"פ · בדיקת קבלן רשום לפי תעודת זהות · העתק תעודת קבלן רשום · פנקס הקבלנים סיווגים · פנקס הקבלנים להורדה · טבלת סיווג קבלנים · סיווג קבלנים 131 · קבלן רשום שיפוצים · רשם הקבלנים טלפון.

### 3.3 Competitor pages read in full (19:25 to 19:40; HTML in `raw/competitors/`, structure in `raw/competitors/structure.json`)

| Page | Rank | Words (body) | Own search? | Classification table? | FAQ | What it misses |
|---|---|---|---|---|---|---|
| gov.il search app /apps/moch/rasham/home | 2 for רשם הקבלנים; cited in every AI overview | form only | yes: city, branch, company or contractor number, name (+ reCAPTCHA) | no (amounts on records are one period old) | no | no explanation of what a level allows, no "is this job too big for him?", old amounts on records |
| michlal.com/רשם-הקבלנים-פנקס | 1 for פנקס הקבלנים | 500 to 600 | no (lead forms) | no; quotes 90,471 / 47,255 (old) | no | dated 2021, sells a licensing course |
| nadlancenter.co.il/article/6331 | 1 for קבלן רשום | 1,200 to 1,300 | no | no; quotes 83,999 / 43,583 (old) | no | says "about 14,000 contractors" (real: 17,874); no table, no links to records |
| biz.midrag.co.il/content/Article/14754 | 1 for בדיקת קבלן רשום | 1,500 to 1,800 | no | branch table without money; examples ג1 4,348,000 (old) | no | it is a "how to register" guide; does not answer the check intent |
| thebuilder.co.il/סיווג-קבלנים | 1 for סיווג קבלנים | about 700 to 800 | no | rounded, undated amounts; no ק level | no | no date, no source link |
| hatikva.org.il/פנקס-הקבלנים | 8 to 10 | about 2,000 | no | no; unfilled "איקס" placeholders | 5 questions (FAQPage schema) | "over 12,000 contractors", placeholders, sales copy |
| medicalmalpractice.co.il/6150 | 4 for פנקס הקבלנים | 555 | no | no | no | thin |
| renovations.org.il/רישום-קבלנים | 2 for קבלן רשום | 430 | no | no | no | thin |
| govil.ai dataset page | AI overview source | 662 | yes, a live data.gov.il explorer | yes (from the data, so April amounts) | no | analytics page, not a consumer check; data as of 8 to 10.8.2026; says unofficial |

Gaps none of them fill (our edge):
1. One search over all 17,874 contractors by name, contractor number, company number, city, branch and level, with no captcha, plus a direct link to each contractor's live official record.
2. The **current** money limit per level (1.10.2026 table) next to each result; the official records and the data still show the April amounts.
3. "Is this contractor allowed to do my job?": enter the job type and budget and get the needed branch and level and whether registration is required at all (103,250 / 54,000).
4. Plain explanation of statuses (מוקפא, מוחרג, מותלה) with the restricted records flagged.
5. A link to a fuller nad-lan profile where one exists (2,690 today).
6. True counts and dates (17,874 contractors, 32 branches, 945 cities, data of 17.8.2026), against "12,000" and "14,000" elsewhere.

---

## 4. Proposal

### 4.1 Where the page lives

- **New page at /pinkas-hakablanim/** (one segment, no repeated word).
  - `url_word_audit.py` (19:31, 4,580 live URLs): "pinkas", "hakablanim", "kablan", "kablanim" and "register" are held by no URL; "registry" appears only inside /glossary/land-registry-extract/; the Hebrew "פנקס" and "רשם" are unused and "קבלן" is held only by /profession/קבלן/. "contractor" is held by /renovation-contractor/ and /new-projects/contractor-delay-compensation/ (head word of that segment), so /contractor-register/ would break the one-word-one-owner rule. "check" is held by nine URLs.
  - The slug transliterates the biggest query (פנקס הקבלנים, 6,600).
- **Not at /profession/קבלן/.** It is a taxonomy archive whose content is the Danya Cebus profile (our project contractors). Turning it into the register tool would replace that content (additive law) and mix two intents. Keep it, and link to the new page from it.
- /professionals/?profession=kablan keeps its canonical to /professionals/; add a strong link from the directory to the new page.

### 4.2 Strings (all three checked with `tools/title_start_audit.py`, 19:31: each "OK", trio "three different strings")

- **H1:** בדיקת קבלן רשום: חיפוש בכל הקבלנים בפנקס הרשמי
- **SEO title (54 characters):** פנקס הקבלנים: בדיקת קבלן רשום לפי שם, מספר, עיר וסיווג
  (a shorter fallback of 49: פנקס הקבלנים: בדיקת קבלן רשום לפי שם, מספר וסיווג)
- **Breadcrumb:** רשם הקבלנים (2,900 searches; no live title starts with it)
- Meta description idea: בודקים קבלן לפני שחותמים? חפשו לפי שם, מספר קבלן, ח"פ, עיר או ענף ב-17,874 הקבלנים הרשומים, ראו מה הסיווג מתיר לו לבנות ועברו לרשומה הרשמית.

### 4.3 The answer paragraph (directly under the H1; facts only)

> קבלן רשום הוא קבלן שמופיע בפנקס הקבלנים של משרד הבינוי והשיכון, לפי חוק רישום קבלנים לעבודות הנדסה בנאיות, התשכ"ט-1969. עבודה בענף ראשי בהיקף של יותר מ-103,250 ₪, או בענף משנה (למשל שיפוצים) ביותר מ-54,000 ₪, מותרת רק לקבלן רשום. בחיפוש כאן תראו לכל קבלן באילו ענפים הוא רשום, מה הסיווג שלו ועד איזה סכום מותר לו לבצע באתר אחד לפי הטבלה שבתוקף מ-1.10.2026: למשל קבלן בניין ג1 עד 5,458 אלף ₪, ג5 ללא הגבלה. לפני חתימה פתחו את הרשומה הרשמית שלו ב-gov.il ובדקו שהוא לא מוקפא, מוחרג או מותלה.

Sources (kept in this file, not on the page): general_information_for_registration_of_contractors (24.02.2026) for the thresholds; sivug_kablanim (06.10.2026) for the table; construction_registry (24.09.2026) for statuses.

### 4.4 The tool

Search inputs (one line on phones, filters in a drawer):
- free text: name (normalised: ignore בע"מ, quotes, final letters, spaces) or digits (an exact contractor number of up to 5 digits, or a 9-digit company number);
- city (945 values, typing completes);
- branch (32, shown as "בניה (100)");
- level (א-ק, 1 to 5 within the branch's group);
- "קבלן מוכר לעבודות ממשלתיות" toggle;
- optional "היקף העבודה שלי" in NIS: filters to contractors whose level covers that budget in the chosen branch, and answers "the law requires a registered contractor: yes or no".

Each result card:
- name · city · "רשום מאז {year}" · contractor number · company number when present;
- each branch as "בניה · ג1 · עד 5,458 אלף ₪ באתר אחד" from the **current official table**, not the HEKEF column; residential branch also "עד 2,000 מ"ר";
- badge "מוכר לעבודות ממשלתיות בסיווג N" when present;
- warning badge for the 23 restricted rows, with the restriction text;
- button "לרשומה הרשמית ב-gov.il" → `https://www.gov.il/apps/moch/rasham/details/{n}` (always);
- button "לפרופיל בנדלן" when we have a page (2,690 today);
- footer line: "הנתונים מהמאגר הפתוח data.gov.il, נכונים ל-17.8.2026. הסטטוס העדכני ברשומה הרשמית."
- No phone, email or street (privacy; the official record has them).

How the data ships:
- Measured prototype (`raw/tool-data-prototype.json`): one row per contractor `[number, name, company number, city index, first year, branches string, our slug if any]` plus a city list and a branch list: **1,278,886 bytes raw, 353,826 bytes gzip** for 17,874 contractors (about 72 bytes per contractor raw).
- Recommended: **a server search endpoint** (for example `/wp-json/nadlan/v1/pinkas?q=&city=&anaf=&sivug=&mukar=&budget=`) that reads a prebuilt file, returns at most 30 results (about 5 KB), and is cached. The page itself stays light (phones first, no scroll stalls), the data refreshes without a release, and no one can pull all names in one request.
- Fallback if a server endpoint is not wanted: lazy-load the gzip JSON only after the first keystroke in the search box (354 KB once, then search in the browser).
- Refresh: a weekly job calls the CKAN `datastore_search` API (the same 5 calls), rebuilds the file, and records the resource `last_modified`; the visible "נכון ל-" date comes from it. The money table is a small constant updated on 1 April and 1 October from sivug_kablanim.

### 4.5 Page order (rendered, phones first)

1. H1 → answer paragraph → search box (the main call to action) → results.
2. "מה הסיווג מתיר לבנות": the 1.10.2026 table (groups א/ב/ג by levels ק, 1 to 5, plus residential sqm), with the date and the next update date (1.4.2027).
3. "מה בודקים לפני שחותמים": registered in the right branch; level covers the job on one site; status not frozen, excluded or suspended; name and number on the quote match the record; print the official certificate (with QR).
4. "מי חייב להיות קבלן רשום": thresholds 103,250 / 54,000, renovation (131) and its ק level up to 846 thousand.
5. "מה ההבדל בין מוקפא, מוחרג ומותלה": from construction_registry.
6. "ענפי הפנקס": the 32 branches with code, group and number of contractors (from the data).
7. "קבלן מוכר": what the column means and the MoF list link.
8. "הפנקס במספרים": 17,874 contractors, 8,861 companies, 945 cities, new contractors per year, top cities (each city can link to the directory filtered by city).
9. FAQ.
10. Links onward.

Language: Israeli real-estate voice, no technical words on screen (the language-DNA law). Long text is written through the owner's ChatGPT flow (content-split law); this file is the fact base. Design: Claude Design first (design-first law). A suggested direction for the brief to Claude Design: take the look of the official licence certificate: ministry blue ink on white, a stamp-like status badge, register numbers set in tabular figures; a Hebrew face with true tabular figures chosen on purpose in Claude Design (not the site's default face). Not the default cream, terracotta or gold look.

### 4.6 FAQ (from Google's PAA and related searches; answers only from the official sources above)

1. איך בודקים אם קבלן רשום ברשם הקבלנים? (PAA)
2. אפשר לבדוק קבלן לפי ח"פ או לפי תעודת זהות? (related searches) → by company number yes; personal ID numbers are not published, so search individuals by name or contractor number.
3. מהי טבלת הסיווגים של רשם הקבלנים? (PAA, twice)
4. מה זה קבלן ג1, ג2 ... ג5? (PAA "מה זה קבלן ג2?")
5. מהם התנאים להעלאת סיווג? (PAA) → the 70% / two-site rule.
6. איך מוציאים תעודת קבלן רשום? (PAA; related "העתק תעודת קבלן רשום") → the printable certificate with QR on the record page.
7. האם קבלן שיפוצים חייב להיות רשום? (related "קבלן רשום שיפוצים")
8. מה ההבדל בין קבלן רשום לקבלן מוכר? (720 searches a month)
9. מה המשמעות של מוקפא, מוחרג או מותלה?
10. איך יוצרים קשר עם רשם הקבלנים? (PAA address; "רשם הקבלנים טלפון" 260) → link to the official contact page only, until the number is read off it.
Hold until an official source is read: "מהי אגרת רשם הקבלנים?" (PAA).

### 4.7 Internal links

From the new page: /professionals/ (directory) · /renovation-contractor/ · /construction-supervisor/ · /home-inspection/ · /real-estate-lawyer/sale-of-apartments-law/ · /investment/bank-guarantee-purchase/ · /new-projects/contractor-delay-compensation/ · /real-estate-lawyer/construction-defects-lawsuit/ · /new-projects/construction-input-index/ (the same index moves the money table) · /buying-apartment/ · /architect-building-permit/ · /real-estate-lawyer/building-permit-citizen-guide/ · /urban-renewal/pinui-binui/.
To the new page: every contractor profile (one line "בדיקת קבלן רשום" next to the source line), /professionals/, /profession/קבלן/, /renovation-contractor/, /construction-supervisor/, /home-inspection/, /buying-apartment/.

### 4.8 Fixes for the existing profiles (reported; no change made)

- Link each profile to its own official record, not to the search home.
- Show the current money limit for each level, and "ק" as "סיווג ק (שיפוצים עד 846 אלף ₪)".
- Update the 13 profiles whose branches or levels changed, and decide what to do with the 8 profiles whose numbers left the register (owner's decision; no removal, no redirect).
- Take the demo profile out of the count and out of "registered contractor" lists.
- Store the company number (8,861 companies have one) so a search by ח"פ finds the profile.
- Pages for the other 15,184 contractors: only at a pace Ben approves.

---

## 5. Files in this folder

- `brief.md`: this file.
- `keywords.csv`: 48 keywords with average and 12 monthly volumes, competition, CPC.
- `serps.json`: five SERPs with top 10, AI overview (present, cited URLs, claims), PAA, related searches.
- `register-fields.json`: fields with Hebrew labels and notes, totals, group x level x amount, branches (contractors, with-page counts, groups, levels), restrictions, recognised counts, years, top cities, and the current official table.
- `raw/register.json`: the full register (24,373 rows, all fields) from the CKAN datastore API.
- `raw/nadlan-professionals.json`: all 2,847 nad-lan professional records with meta.
- `raw/tool-data-prototype.json`: the compact tool data used for the size measurement.
- `raw/gov-pages/`: text of the official pages read (with dates and retrieval times).
- `raw/competitors/`: HTML of the competitor pages and `structure.json` (headings, word counts, schema).
- `raw/gsc-contractor-queries-2026-07-22_2026-10-20.csv`, `raw/gsc-professionals-pages-2026-07-22_2026-10-20.csv`: filtered Search Console rows.

## 6. Cost

DataForSEO: two Google Ads search-volume calls (48 keywords; the second reported $0.09, the first is the same call type) and five live advanced SERP calls with AI overview and one PAA click level (a few tenths of a cent each). Total about **$0.20**. The account day total was $3.35 at 19:40, which includes other sessions.
