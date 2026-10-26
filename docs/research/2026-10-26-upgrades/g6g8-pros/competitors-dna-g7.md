# G7 competitor DNA: "שמאי מקרקעין" + price intents

Target page: https://nad-lan.co.il/real-estate-appraiser/
Queries: "שמאי מקרקעין" (desktop + mobile), "כמה עולה שמאי" (desktop). Google Israel, retrieved 26.10.2026 11:32 UTC. Competitor pages fetched 26.10.2026 11:36-11:37 UTC.
Sources read: `serp/g6g8/g7_summary.txt`, the three raw SERP JSONs (only to get the AI overview reference list, local pack and related searches), `raw/g6g8/index-urls_g7.json`, and every `g7-*` / `g7p-*` .txt file, plus the .reader.md files for landvalue, gov-decisive and w-b. g7-mikied could not be fetched (HTTP 301, then 422) and is skipped.
Method notes:
- Word counts come from the index (`words_raw`). For landvalue, gov and w-b they come from `words_reader`. These counts include menus and other page furniture.
- H2/H3 counts were taken from the `## [hN]` markers in the .txt files and checked against the raw HTML. They include sidebars, widgets and repeated carousels; the "notes" column says where that inflates them.
- "Phrase" means the exact string "שמאי מקרקעין". Occurrence counts are for the whole visible text, navigation included.
- No People also ask box appeared on any of the 3 SERPs. The SERPs did show related searches, "people also search" and AI overviews.

Short names used below: LV = landvalue, JC = j-cohen, TD = teddy, SH = shovi (main article), AV = avrahams, MR = mrea, DZ = d.co.il directory, AF = afikil (main article), PRO = pro.co.il, GOV = gov.il decisive appraisal, WIKI = he.wikipedia, IV = iritvan, MP = midrag price 8151, EC = ec-shamaut, AFH = afikil "how appraiser works", DZP = d.co.il price list, RA = re-ap, SHP = shovi price, CAL = calliber, WB = w-b.co.il, MT = midrag tip 186, BN = banai.

---

## 1. Competitor table

### 1a. Identity, position, structure

| # | Name | SERP position (query, device) | URL | Title | H1 | Words | H2 / H3 | Tables | Images | FAQ (schema?) | Schema types | dateModified / visible date |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | LV g7-landvalue | #1 "שמאי מקרקעין" desktop + mobile (another LV page, id=578 "אתר הלשכה", is mobile #10). It is also an AIO reference (the LV homepage) | https://landvalue.org.il/index2.php?id=6&lang=HEB | שירותי הלשכה - לשכת שמאי מקרקעין בישראל (ע"ר) | שירותי הלשכה (twice) | 317 raw / 948 reader | 0 / 0 (bold subheads only) | 0 | 5 | 0 (no) | none | none. Privacy-policy file is named 2026 |
| 2 | JC g7-jcohen | #2 desktop + mobile | https://www.j-cohen.co.il/ | משרד יוסף כהן שמאות מקרקעין בתל אביב \| המומחים שלך לחיסכון בשומה! | none (no H1) | 1,947 | 3 / 37 (service cards repeated about 3 times by a carousel) | 0 | 38 | 0 (no) | BreadcrumbList, WebPage, WebSite, SearchAction, ImageObject… | modified 2025-03-13 (published 2019-09-03) |
| 3 | TD g7-teddy | #3 desktop + mobile (TD article "קווים לדמותו…" is #16 desktop / #15 mobile; TD 404 page is mobile #19) | https://www.teddy.co.il/ | טדי שמאות וניהול \| שמאי מקרקעין מומחים | ברוכים הבאים לטדי שמאות וניהול | 1,549 | 9 / 1 (one H2 and one H3 are empty, one H2 is repeated) | 0 | 36 | 0 (no) | none | none |
| 4 | SH g7-shovi | #4 desktop + mobile | https://www.shovi.co.il/שמאי-מקרקעין/ | שמאי מקרקעין \| יניב רפאל - שמאי מקרקעין מעל 15 שנות ניסיון | שמאי מקרקעין | 1,714 | 8 / 0 | 0 | 7 | 9 visible Q&A (no FAQ schema) | Article, Organization, Person, BreadcrumbList, WebPage… | visible 05/25/25; modified 2025-07-13 |
| 5 | AV g7-avrahams | #6 desktop + mobile | https://avrahams.org.il/ | שי אברהם - שמאי מקרקעין | אברהם שי - נדל"ן ושות' | 719 | 1 / 6 | 0 | 7 | 0 | none | none |
| 6 | MR g7-mrea | #8 desktop + mobile | https://www.mrea.co.il/ | שמאי מקרקעין - עמית מהלל ושות' משרד שמאות מקרקעין \| 052-6522734 | עמית מהלל ושות׳ שמאי מקרקעין | 1,051 | 17 / 10 (numbered service H2s, empty H3s) | 0 | 4 | 0 | Article, Person, WebPage, WebSite, ImageObject, SearchAction | modified 2026-09-14 (published 2021-01-01) |
| 7 | DZ g7-dcoil | #9 desktop + mobile | https://www.d.co.il/h-c49080-e0-p0-l0/ | שמאי מקרקעין - כ-1325 שמאים מורשים בכל הארץ - דפי זהב | שמאי מקרקעין מורשים בכל הארץ | 3,716 | 6 / 43 (H3 = listing cards) | 0 | 61 | 3 (FAQPage schema) | FAQPage, Question, Answer | none. Visible text says "הדאטה מעודכן לספטמבר 2026"; editorial guides dated 16/07/2012 and 26/01/2022 |
| 8 | AF g7-afikil | #11 desktop / #12 mobile | https://afikil.co.il/שמאות-מקרקעין/מה-זה-שמאי-מקרקעין-ואיך-הוא-תורם-לשוק-הנ/ | מה זה שמאי מקרקעין? תפקיד, הכשרה ומתי צריך \| אפיק NEWS | מה זה שמאי מקרקעין ואיך הוא תורם לשוק הנדל"ן? | 2,769 | 13 / 54 (H3 mostly sidebar and related posts; about 11 article H2s) | 0 | 155 | 4 visible Q&A. The FAQPage schema has 3 different Qs taken from the H2s (mismatch) | BlogPosting, FAQPage, BreadcrumbList, Organization, Person… | published 2026-02-04; modified 2026-06-28 |
| 9 | PRO g7-pro | #13 desktop + mobile. The PRO category page is an AIO link | https://www.pro.co.il/real-estate-appraisers/guide/information-about-a-real-estate-appraiser | כל מה שצריך לדעת על שמאי מקרקעין • המקצוענים | כל מה שצריך לדעת על שמאי מקרקעין | 1,486 | 9 / 6 | 0 | 63 | 0 | none | visible "עודכן לאחרונה: 11.07.2023" |
| 10 | GOV g7-gov-decisive | #14 desktop only | https://www.gov.il/he/departments/units/decisive_appraisal | (403 on fetch; reader title) שמאות מכריעה | שמאות מכריעה | 1,112 reader | 4 / 1 | 0 | 0 | 0 | none captured | visible "עודכן לאחרונה 18.03.2026" |
| 11 | WIKI g7-wiki | Not in organic top 19. It is an AIO reference on "שמאי מקרקעין" | https://he.wikipedia.org/wiki/שמאות_מקרקעין | שמאות מקרקעין – ויקיפדיה | שמאות מקרקעין | 2,149 | 9 / 6 | 1 | 7 | 0 | Article, Organization, ImageObject | modified 2026-08-02 |
| 12 | IV g7-iritvan | Not in organic top 19. It is an AIO reference (cited twice) | https://www.iritvan.co.il/ | שירותי שמאי מקרקעין בתל אביב והסביבה - אירית ונונו - שמאות מקרקעין | שמאי מקרקעין \| שמאות מקרקעין - אירית ונונו | 526 | 2 / 4 (2 empty H3s) | 0 | 1 | 0 | Organization, WebPage, BreadcrumbList… | modified 2024-10-22 (published 2018-03-18) |
| 13 | MP g7p-midrag-price8151 | Not in organic top 19 for "כמה עולה שמאי". It is the first AIO reference and is named in the AIO text ("לפי מחירון מידרג") | https://www.midrag.co.il/Content/Price/8151 | שמאי מקרקעין - מחיר \| כל הפרטים על מחירי שמאי מקרקעין - במידרג | שמאי מקרקעין - מחיר | 2,276 | 12 / 18 | 0 | 114 | 3 (FAQPage schema) | Article, FAQPage, Organization… | published 2022-08-15; modified 2024-07-03 |
| 14 | EC g7p-ecshamaut | AIO reference only (price query) | https://ec-shamaut.co.il/כמה-עולה-שמאות-דירה/ | שמאות דירה – כמה זה עולה באמת? מדריך לשנת 2025 - EC שמאות מקרקעין | none | 477 | 6 / 5 | 1 (price table) | 8 | 4 (FAQPage schema) | Article, FAQPage, Person, Organization… | 2025-08-24 |
| 15 | AFH g7p-afikil-how | #3 "כמה עולה שמאי" | https://afikil.co.il/real-estate-appraisal/howappraiserworks/ | איך שמאי מעריך דירה, מה המחיר ואיך מחשבים הערכת שווי דירה יד 2 - אפיק NEWS | same as title | 2,644 | 13 / 50 (H3 mostly sidebar) | 0 | 157 | 9 (FAQPage schema built from H2s, no visible FAQ block) | BlogPosting, FAQPage… | published 2021-04-14 (visible 14/04/21); modified 2026-04-20 |
| 16 | DZP g7p-dcoil-price | #4 "כמה עולה שמאי" | https://www.d.co.il/priceList-49080/ | שמאי מקרקעין מחירון - דפי זהב | מחירון שמאי מקרקעין - מחירי שמאות מקרקעין | 943 | 5 / 2 | 0 (the price list is not an HTML table) | 17 | 2 Q&A in intro (no schema) | none | none |
| 17 | RA g7p-reap | #7 "כמה עולה שמאי" | https://re-ap.co.il/2020/11/22/עלות-שמאי-מקרקעין/ | עלות שמאי מקרקעין - פריידנברג-סופר שמאי מקרקעין | עלות שמאי מקרקעין | 538 | 1 / 0 | 0 | 2 | 0 | Article, Person, Organization… | published 2020-11-22; modified 2026-01-18 |
| 18 | SHP g7p-shovi-price | #9 "כמה עולה שמאי" | https://www.shovi.co.il/מחירון-לשומת-מקרקעין/ | שמאי מקרקעין מחיר - מחירון לשומת מקרקעין \| יניב רפאל… | שמאי מקרקעין מחיר – מחירון לשומת מקרקעין | 473 | 0 / 0 | 0 | 7 | 0 | Article, Person, Organization… | visible 02/15/23; modified 2024-03-26 |
| 19 | CAL g7p-calliber | #8 "כמה עולה שמאי" (other CAL URLs at #6 and #12 are car appraiser pages, not fetched) | https://calliber.co.il/prices-list/apartment-valuation-price/ | מחיר הערכת שווי דירה \| קליבר | מחיר הערכת שווי דירה | 946 | 4 / 7 | 0 | 11 | 0 | Organization, ContactPoint, BreadcrumbList | none |
| 20 | WB g7p-wb | #1 "כמה עולה שמאי" (sister URL _id=40014 at #5, not fetched) | https://www.w-b.co.il/html5/arclookup.taf?&_id=39975&did=10322&g=10014 | כמה עולה שמאי מהבנק \| שמאי מקרקעין \| שמאות מקרקעין - בועז וכולדר (windows-1255) | כמה עולה שמאי מהבנק | 1,510 reader | 0 / 0 (bold subheads) | 10 (layout tables) | 9 | 0 | none | none |
| 21 | MT g7p-midrag-tip186 | #13 "כמה עולה שמאי". It is also an AIO reference on "שמאי מקרקעין" | https://www.midrag.co.il/Content/Tip/186 | שמאי מקרקעין \| כל מה שצריך לדעת על שמאות מקרקעין - במידרג | שמאי מקרקעין | 2,473 | 14 / 0 | 0 | 120 | 0 | Article, Organization, ImageObject | published 2022-08-14; modified 2024-09-05 |
| 22 | BN g7p-banai | #16 "כמה עולה שמאי" | https://www.banai.co.il/what-affects-the-price-of-a-real-estate-appraiser/ | מה משפיע על מחיר שמאי מקרקעין? \| בנאי - שמאות מקרקעין | מה משפיע על מחיר שמאי מקרקעין? + יש שאלות? (2 H1s) | 473 | 5 / 4 | 0 | 23 | 0 | Article, Person, Organization… | published 2021-09-14; modified 2021-10-20 |

SERP results in the top 19 that were not fetched as competitors (for context): midrag search results for Petah Tikva (#5 on both devices), mikied (#7, failed), shamaoot.com (#10 desktop / #11 mobile), shamaeim.org.il "איגוד השמאים בישראל" (#12 desktop), etkin (#15/#14), bizportal tag page (#17/#16), mpra (#18/#17) and ori-r (mobile #18). On "כמה עולה שמאי": tarya (#2, a P2P lender), w-b _id=40014 (#5), calliber car-appraiser pages (#6, #12), facebook groups (#10, #17), appra (#11), eliasaf test-calculator (#14), midrag PriceList/465083 (#15), harel-vered (#18) and a property-appraiser price list (#19).
nad-lan.co.il does not appear in the captured results for either query.

### 1b. Conversion tools, exact-phrase placement, why it ranks, weak spots

| Name | Tools / forms / CTAs | "שמאי מקרקעין": title / H1 / first paragraph / count | Why it ranks | Weak spots |
|---|---|---|---|---|
| LV | Member login; nav link "איתור שמאי/ת" (a find-an-appraiser directory); office phone; no quote form | title yes ("לשכת שמאי מקרקעין בישראל") / H1 no / first paragraph no ("שמאי המקרקעין" with ה) / 2 (6 in reader) | Official association: entity authority and IVSC member logo. The page itself is a member-services page | No consumer content, no prices, no explanation of what an appraiser does; H1 does not match the query; no dates; no schema |
| JC | Contact form (name, phone, email, subject), phone 03-6096900, "ייעוץ ראשוני" | no ("שמאות מקרקעין") / no H1 / no / 3 | Office homepage, Tel Aviv, since 1996, ex-ILA (רמ"י) official; wide service list (levy, RMI, 197, IFRS, zero report, expropriation) | No H1; teaser snippets truncated with "להמשך קריאה"; carousel text repeated about 3 times; ">97% success" claim unsourced; no prices, FAQ or dates for visitors |
| TD | 2 lead forms, phone 03-6093320, success ticker ("הפחתנו 82%…") | title yes / H1 no / no / 19 | Office homepage, since 1997, testimonials (רמ"י 2005-2017, Bezeq), long "why an appraiser before buying" text | Unsourced stat ("ממחקר שביצעה לשכת שמאי מקרקעין… עשירית מהבקשות למשכנתה מסורבות"); "תקן 22" listed but not explained; empty headings; no dates; typos |
| SH | WhatsApp, call, contact float; "הצעת מחיר מותאמת" CTA; list of questions to ask the appraiser | yes / yes / yes / 31 | Exact-match H1 and URL slug, broad guide (definition, when, methods, checks, licensing, choosing, cost, 9 FAQ) | Contradicts itself on internship length; price section vague; FAQ has no schema; levy sentence garbled ("ראשית רשות מקומית" means "רשאית"); divorce-law claim overstated |
| AV | "ליעוץ מקצועי חינם, חייגו", lead form, "בואו נדבר" popup, phone 050-7260228 | yes / no / yes / 2 | Office homepage with exact-match title; levy case stories | Thin (719 words); a leftover developer note is visible on the page ("במקום תיאור להוסיף אפשרות להעלאת מסמך"); the "testimonials" are levy stories in the appraiser's own first person, apparently shifted one card from the named client, with typos ("דירת התשלום"); arithmetic error ("150,000 → 50,000 … הפחתה של 70%" is actually 66.7%) |
| MR | Free-consultation form ("לייעוץ שמאות מקרקעין חינם"), phone in title and H3 | yes / yes / yes / 14 | Exact-match title and H1, 9 numbered services, licensing and choosing sections, fresh dateModified (2026-09-14) | Misreads WIKI's statistic ("בשנת 2021 היו בישראל כ2671 שמאי מקרקעין"); typo "ביעות"; no prices or FAQ |
| DZ | Directory of 1,325 listings with filters (popularity / rating / distance), virtual phone numbers, WhatsApp, ratings, price snippet, guides, "נצפו לאחרונה" | yes / yes / yes / 63 | Directory/aggregator; exact match; count in title; FAQPage schema; prices; local filters | Editorial is thin and old (guides from 2012); FAQ answers are self-promotion; the guide teaser says "את חוק שמאי מקרקעין כתבה מועצת שמאי המקרקעין" (wrong). "1325" is a listing count, not a register count |
| AF | Course-lead form (career funnel), "האזנה לכתבה" audio player, phone/WhatsApp | yes / yes / yes / 22 | "What is" informational match; fresh (2026); FAQPage schema; topical site (appraisal school) | Generic, AI-style text; no prices; a wrong tax claim (appraisal as the basis for municipal tax rates); schema FAQ ≠ visible FAQ; heavy sidebar noise; it is a sales funnel for courses |
| PRO | Directory widget (3 Tel Aviv appraisers with ratings and phones, a "לא שמאי בנק" tag), city selector, SMS login, link to price list | yes / yes / no ("שמאי המקרקעין") / 27 | Directory brand; "כל מה שצריך לדעת" guide; AIO points users to PRO | Stale (11.07.2023); near-duplicate of MT text; levy triggers wrong ("חריגת בנייה"); "מועצת שמאי המקרקעין של לשכת המשפטים" (sic); no prices on the page |
| GOV | Links to the online service "בקשה למינוי שמאי מכריע", list of decisive appraisers, decisions database, exceptional-fee decisions; AI chat | no / no / no / 3 | Official government source for שמאות מכריעה | Procedural stub: no fees, no deadlines, no step-by-step |
| WIKI | none | no / no / yes / 13 | Encyclopedic authority; AIO definition source | Theory-heavy; no prices; 2021 data; contradicts itself on IVSC (joined 2019 vs "ישראל אינה מיוצגת") |
| IV | Contact CTA, chat widget | yes / yes / no ("שמאית מקרקעין") / 8 | AIO reference for the role list; exact-match title and H1 | Thin (526 words); claim that the report "sets" the taxes is overstated; dateModified 2024 |
| MP | Rated appraiser list by city (ratings, review counts), call center 1-700-707-233, many related-topic links | yes / yes / yes / 73 | Price intent owner: per-service price sections; AIO's main price source; FAQPage | Dated (2024-07); internal levy-fee inconsistency; FAQ "כמה לוקח שמאי מקרקעין?" answered with a price, not a time; VAT not stated; says property value never affects price (a sibling midrag page says pre-purchase appraisal is priced by value) |
| EC | Lead form, WhatsApp (Joinchat), phone | no / no H1 / no / 4 | Clear price table; FAQPage; AIO source | Thin (477 words); "2025" in the title; VAT answer contradicts the AIO; no H1 |
| AFH | "קליק לקבלת הצעת מחיר" links, course form | no / no / no / 18 | Title matches "how/price" intent; FAQPage from H2s; old URL with fresh dateModified | Promises a price ("מה המחיר") but has no numbers; LTV fact "נכון ל-2023"; contradicts WB on who receives the bank report |
| DZP | Price list, "האם המחירון עזר לך?" feedback, recommended businesses with phones, city links | yes / yes / yes / 33 | Exact match "מחירון שמאי מקרקעין"; widest price table (20 rows) | No date; every figure is a round number × 1.08 (looks like a blanket uplift; VAT status unstated); contradicts itself (intro 2,000-5,000 vs table 2,160-5,400; "אין מחירון… לפי שעות" vs hourly rows) |
| RA | Chat widget | yes / yes / yes / 10 | Exact match "עלות שמאי מקרקעין" title and H1 | No numbers at all; "2021 record mortgage year" is stale; thin |
| SHP | Call / WhatsApp | yes / yes / yes / 15 | Exact match "שמאי מקרקעין מחיר" title and H1; 6-row price list | Thin (473 words), 2023, typos, no sources |
| CAL | Lead form ("השארת פניה"), phone connect, JS price widget | no / no / no / 3 | Price-list section of a directory; "מחיר הערכת שווי דירה" exact match for a sub-intent | Price widget renders "טוען מחירון..." without JS; low outlier prices (1,200-2,000); no date |
| WB | Phone buttons (TA/Haifa), WhatsApp | yes (per reader title) / no / no / 5 | Exact-match title "כמה עולה שמאי מהבנק" (bank sub-intent); old domain | No price at all despite the title; legacy windows-1255 page; unsourced "since 2018" claim |
| MT | Rated appraiser list by city, call center | yes / yes / yes / 71 | Directory guide; AIO reference for the licensing path | Same text as PRO (near-duplicate); 2024; levy triggers wrong; "לשכת המשפטים" |
| BN | Lead form, phone 050-3332523 | yes / yes / no / 16 | Exact question H1 "מה משפיע על מחיר שמאי מקרקעין?" | No numbers; 2021; 2 H1s; thin |

---

## 2. Published prices

All amounts are in NIS. "VAT" = what the page says about VAT; "n/s" = not stated. Page dates: visible or dateModified (see table 1a). All pages were retrieved 26.10.2026. Nothing has been averaged.

### 2a. Prices from competitor pages read in full

| Page (date) | Service / property type | Price | Unit / basis | VAT | Notes |
|---|---|---|---|---|---|
| MP (2024-07-03) | Apartment valuation, residential building | 2,500-4,000 | per job, "בממוצע" | n/s | Same figure in the opening, summary and FAQ |
| MP | Private house / צמוד קרקע | "יכול לטפס עד 7,000" | per job | n/s | Reason given: land checks and building deviations |
| MP | Rent assessment (הערכת דמי שכירות) | 2,500-3,500 | per job | n/s | "almost no difference" between house and apartment |
| MP | Nachala (נחלה), no tax check | 4,500-6,000 | per job, average | n/s | |
| MP | Nachala with tax check | up to 12,000 | per job | n/s | |
| MP | Betterment-levy reduction (הפחתת היטל השבחה) | 4,000-6,000 + 10% of the reduction | fee + success % | n/s | Summary box |
| MP | Same, body text | ~5,000 average fee + 10% of the reduction | for reductions of "מאות אלפי שקלים" | n/s | **Inconsistent** with the summary box (4,000-6,000). Some appraisers charge a fee only; "רבים מהשמאים גם לא יגבו… על הבדיקה" (initial check often free); the higher the reduction, the lower the % |
| MP | Court expert opinion (חוות דעת לבית משפט) | +1,500-2,000 on top of the regular opinion | surcharge | n/s | Example: house at 2,500 → 4,000-4,500 for court |
| MP | Price drivers stated | work time only; value, size and purpose do "not" affect price | — | — | Contradicted by midrag/28035 (AIO snippet: pre-purchase priced by apartment value) and by CAL (purpose affects price) |
| EC (2025-08-24, "2025") | Apartment, general | 2,000-3,500 | per job | FAQ: "האם המחיר כולל מע"מ? בדרך כלל כן" | **Contradicts** the AIO ("אינם כוללים מע"מ בדרך כלל") and shamaotil (AIO snippet "לא כולל מע"מ") |
| EC | Residential apartment up to 5 rooms | 2,000-3,000 | table, "טווח מחירים ממוצע" | as above | |
| EC | Large apartment / penthouse | 2,500-3,500 | table | as above | |
| EC | Investment / unique apartment | 3,000-4,000 | table | as above | The AIO copies this row |
| EC | Private house | 3,000-5,000 | table | as above | |
| EC | Small commercial | 3,500-6,000 | table | as above | The AIO copies this row |
| EC | Complex projects | "יכולים להגיע ל-6,000" | per job | as above | Urgency surcharge and multi-unit discount (tenants' appraiser, purchase group) mentioned, amount unclear |
| SH (2025) | Apartment valuation | from ~2,500, up to "סכום כפול" (~5,000) | per job | n/s | |
| SH | Private house | "מעט יקר יותר" | — | n/s | No number |
| SH | Opinion for legal proceedings | +1,000-2,000 | surcharge | n/s | |
| SH | Nachala with tax check | ~10,000 "ולפעמים גם יותר" | per job | n/s | |
| SH | Nachala without tax check | 4,000-6,000 | per job | n/s | |
| SH | Objection to a tax assessment (השגה על שומת מס) | fixed fee or % of the tax reduction | — | n/s | No number. States that property value is not a pricing factor |
| SHP (2023-02-15 / mod 2024-03-26) | Standard apartment, middle floors, ≤120 m² | 2,500-5,000 | per job | n/s | "המחירון… המלצה בלבד" |
| SHP | Garden or roof apartment ≤120 m² | 3,000-6,000 | per job | n/s | |
| SHP | Rent assessment, apartment ≤120 m² | 2,500-5,000 | per job | n/s | |
| SHP | Depreciation (ירידת ערך), apartment ≤120 m² | 4,000-10,000 | per job | n/s | |
| SHP | Standard shop ≤60 m² | 3,000-7,000 | per job | n/s | |
| SHP | Empty plot for private / semi-detached house | 2,500-4,000 | per job | n/s | |
| DZ (directory, data "ספטמבר 2026") | Apartment valuation | 2,160-5,400 | per job | n/s | Price snippet on the listing page |
| DZ | Apartment, partition (פירוק שיתוף) | 2,376-5,400 | per job | n/s | |
| DZ | Apartment, partition incl. court filing | 2,376-5,400 | per job | n/s | Same as without court (suspicious) |
| DZP (no date) | Intro answer: apartment valuation | 2,000-5,000 | per job | n/s | **Contradicts** the table below (2,160-5,400) |
| DZP | Intro answer: hourly? | "אין מחירון שמאי מקרקעין לפי שעות אלא לפי הפרוייקט" | — | — | **Contradicts** the hourly rows below |
| DZP | Apartment valuation | 2,160-5,400 | per job | n/s | Every DZP number = round number × 1.08 (2,000×1.08, 5,000×1.08 …); the reason is unclear |
| DZP | Apartment, partition | 2,376-5,400 | per job | n/s | |
| DZP | Apartment, partition incl. court submission | 2,376-5,400 | per job | n/s | |
| DZP | Apartment, inheritance / estate split | 2,160-5,400 | per job | n/s | |
| DZP | Apartment with key money (דמי מפתח) | 3,024-6,480 | per job | n/s | |
| DZP | Rent assessment, apartment | 1,944-4,320 | per job | n/s | |
| DZP | Consultation hour with an appraiser | 216-540 | per hour | n/s | |
| DZP | Depreciation from an environmental nuisance (antenna, radon), "low level" | 2,700-5,400 | per job | n/s | |
| DZP | Shop ≤50 m², before purchase/sale | 2,700-6,480 | per job | n/s | |
| DZP | Shop ≤50 m², partition | 2,700-6,480 | per job | n/s | |
| DZP | Shop ≤50 m² with key money | 3,024-5,400 | per job | n/s | |
| DZP | Fuel station | 8,640-21,600 | per job | n/s | |
| DZP | Empty plot for a private house | 2,160-5,400 | per job | n/s | |
| DZP | Agricultural land 1-3 dunam | 3,240-6,480 | per job ("מחיר לדונם" in the row name, unclear) | n/s | |
| DZP | Plot 400-500 m² for 8-10 units | 6,480-16,200 | per job | n/s | |
| DZP | Private house valuation | 2,700-6,480 | per job | n/s | |
| DZP | Private house, inheritance / estate | 2,700-6,480 | per job | n/s | |
| DZP | Private house with key money | 3,024-6,480 | per job | n/s | |
| DZP | Real-estate mediation (גישור נדל"ן) | 216-540 | per hour | n/s | |
| CAL (no date) | Standard apartment valuation | 1,200-2,000 | per job | n/s | **Low outlier** vs all others |
| CAL | Commercial property, or inherited apartment with many owners | up to 3,500 | per job | n/s | |
| CAL | Warning threshold | "800 ש"ח או פחות" = red flag | — | — | |
| CAL | Purpose as a price driver | bank report "נהלים… קשוחים יותר" costs more than a personal report | — | — | Contradicts MP |

### 2b. Prices in the SERP AI overview (query "כמה עולה שמאי", 26.10.2026)

| Service | Price | Attribution shown | Notes |
|---|---|---|---|
| General VAT note | "המחירים אינם כוללים מע"מ בדרך כלל" | none | Conflicts with EC |
| Apartment in residential building / mortgage appraiser (שמאי משכנתא) | 2,000-4,000 | "לפי מחירון מידרג" | MP itself says 2,500-4,000 and does not split mortgage appraisals |
| Pre-contract appraisal (שמאות מוקדמת) | 1,800-4,000 "תלוי בשווי הנכס" | unclear (likely midrag/28035) | |
| Private house / צמוד קרקע | 2,500-7,000 | unclear | |
| Investment or unique apartment | 3,000-4,000 | matches EC | |
| Commercial / shop | 3,500-6,000; complex assets 10,000-20,000 | 3,500-6,000 matches EC; 10,000-20,000 unclear | |
| Plot / land | 4,000-12,000 "לפי סוג הייעוד" | unclear | Higher than SHP (2,500-4,000) and DZP (2,160-5,400) |
| Court opinion | +500-1,000 on top of the regular appraisal | unclear | **Contradicts** MP (+1,500-2,000) and SH (+1,000-2,000) |
| Car valuation / car after accident / private property appraiser | 350-600 / 800-1,100 / 2,500-10,000 | midrag car pages, dagan4u | Off-topic: the AIO mixes appraiser types (query is ambiguous) |

### 2c. Prices visible only in AIO reference snippets (truncated, pages not read in full)

| Source (snippet) | Service | Price | VAT |
|---|---|---|---|
| midrag.co.il/Content/Price/20505 | Mortgage appraiser, apartment | 1,500-3,000 "לרוב" | n/s |
| midrag.co.il/Content/Price/28035 | Pre-purchase appraisal | "מתומחר לפי שווי הדירה… עד ..." (cut off) | n/s |
| koorsim.co.il | Standard apartment | 2,000-5,000 | n/s |
| moshka.co.il | Residential plot / commercial or complex plot | 2,400-6,000 / 6,000-15,000 | n/s |
| shamaotil.co.il | Pre-purchase appraisal | 3,000-5,000 | "לא כולל מע"מ"; "ברוב המקרים התשלום הוא הנמוך בטווח" |
| eliasaf.co.il | Average apartment / ground-floor apartment with extra checks / nachala | 2,000-3,500 / 3,500-4,500 / "7..." (cut off) | n/s |
| kolzchut.org.il (mortgage appraisal) | Bank appraiser fee | No number: "משולם ישירות על-ידי מבקש המשכנתא ונקבע על-פי תעריפי הבנק" | — |

### 2d. Price categories nobody states

- Decisive appraiser (שמאי מכריע) and advisory appraiser (שמאי מייעץ) fees or tariffs: none. GOV only names the fee regulation "תקנות התכנון והבניה (שכרו של שמאי מכריע ושמאי מייעץ), תשס"ט-2009" and mentions requests for "שכר חריג" / "שכר חלקי". No numbers anywhere.
- Counter-appraisal for the betterment levy as a flat fee (outside the MP fee + 10% model): none.
- Urban-renewal tenants' appraiser (שמאי דיירים): none. EC only mentions a discount.
- Divorce valuation: none specific. Inheritance: only DZP (2,160-5,400 apartment, 2,700-6,480 house) and CAL (up to 3,500).
- Section 197 claim appraisal: none specific. Depreciation in general: SHP 4,000-10,000; DZP 2,700-5,400 (low-level nuisance).
- Percentage of property value as a fee: none. MP and SH explicitly say value is not a factor; the AIO and midrag/28035 say pre-purchase pricing depends on value.
- Bank (mortgage) appraisal on the competitor pages read: WB gives no number ("תלויה בתעריפים של אותו הבנק ובשיקולי השמאי").
- Pages titled or worded about price but with no number: WB ("כמה עולה שמאי מהבנק"), RA ("עלות שמאי מקרקעין"), AFH ("מה המחיר"), BN.

---

## 3. Facts stated

Flag codes: **C** = contradiction between pages; **W** = looks wrong; **O** = outdated or dated data; **U** = unsourced or unclear; **verify** = check against a primary source before reuse.

### 3a. Law, regulator, register, association

| # | Claim (paraphrase + Hebrew keywords) | Pages | Flag |
|---|---|---|---|
| 1 | The profession is regulated by "חוק שמאי מקרקעין, תשס"א-2001", via מועצת שמאי המקרקעין in משרד המשפטים (and by the לשכה per WIKI) | WIKI; AIO snippet gov.il/land_assessor; AIO text; SH and MR say "מוסדר בחוק" without the name | Only WIKI and the gov snippet name the law and its year |
| 2 | The council supervises: exams, the register (פנקס), intern registration, complaints | WIKI, MR (paraphrases WIKI) | |
| 3 | Only an appraiser registered in the פנקס may prepare a real-estate appraisal | WIKI, MR | |
| 4 | "Council of the Ministry's bureau": "מועצת שמאי המקרקעין של לשכת המשפטים" | PRO, MT | **W** (wording: משרד המשפטים) |
| 5 | "The council wrote the appraisers' law" ("את חוק שמאי מקרקעין כתבה מועצת שמאי המקרקעין") | DZ guide teaser (2012) | **W**: a statute is enacted by the Knesset; the council was established by the law |
| 6 | PRO calls the standards body "תקן 21 של מועצת המקרקעין" | PRO | **W** (name) |
| 7 | The לשכה is an עמותה and the representative body; most active appraisers are members | WIKI, MR | |
| 8 | Lishka services: dispute-resolution institute (arbitration, mediation, expert appointment), ethics committee, legal advice, library, a professional committee responsible for "גילויי הדעת והקווים המנחים", a new מס שבח deal-data service, intern and job pools | LV | **C/unclear**: WIKI says "הקווים המנחים" are written by the Chief Government Appraiser (השמאי הממשלתי הראשי). It is unclear whether LV means its own guidelines |
| 9 | The lishka joined IVSC in early 2019 | WIKI (body); LV shows an IVSC member logo | **C**: WIKI's external links say "ישראל אינה מיוצגת" → outdated line |
| 10 | Register count: 2,671 appraisers registered from the founding of the state to the start of 2021, ~75% active | WIKI | **O** (2021) |
| 11 | "בשנת 2021 היו בישראל כ2671 שמאי מקרקעין… קצת יותר מ75% פעילים" | MR | **W**: misreads WIKI's cumulative figure as a 2021 headcount |
| 12 | "כ-1325 שמאים מורשים" / "נמצאו 1325 שמאות מקרקעין" | DZ title and H2 | **C/U**: a directory listing count, not the register; differs from 2,671 |
| 13 | Licence numbers appear in listings ("מספר רישוי 848", "רישיון מספר 1497") | DZ | Shows register numbers exist; no page explains how to look one up |
| 14 | "Check the council's site for the list of licensed appraisers" | PRO, MT, MR ("ניתן לראות באתר מועצת שמאי המקרקעין"); DZ ("בדיקת רישום בפנקס השמאים") | No page gives the URL or steps |
| 15 | Avrahams: "רישיון ממשרד המשפטים"; CAL: "רישיון מוכר מטעם משרד המשפטים" | AV, CAL | consistent |
| 16 | Choosing tip: check membership in the lishka | BN | Membership ≠ licence; no page states this |

### 3b. Licensing path (degree, studies, internship, exams)

| # | Claim | Pages | Flag |
|---|---|---|---|
| 17 | Minimum: 3 cumulative conditions: any academic degree, all council exams, a one-year internship | WIKI | |
| 18 | Degree: "תואר אקדמי רלוונטי בתחום הנדל"ן, הכלכלה, או תחום דומה" | AF | **C** with WIKI ("השכלה אקדמאית כלשהי") and MR ("תואר ראשון או השכלה אקדמאית כלשהי") |
| 19 | Appraisal studies: 600-800 hours, usually 2-3 years, only for degree holders; institutions: הטכניון, המכללה למנהל, אוניברסיטת אריאל | SH | |
| 20 | Appraisal studies: 3 years | MR, MT ("3 שנים מפרכות"); PRO ("תואר ראשון לאחר שלוש שנים של לימודי התחום", ambiguous) | **C** with SH (2-3 years) |
| 21 | Internship: 1 year at 40 h/week or 2 years at 20 h/week | SH body | **C** with SH's own FAQ ("שנה (40 שעות שבועיות)") |
| 22 | Internship: "שנה לפחות" | MR | |
| 23 | Internship: 1-2 years | PRO, MT (AIO quotes MT) | **C** with WIKI (1 year) |
| 24 | Internship "יכול להימשך מספר שנים" | AF | **C** |
| 25 | Order: exams → internship → register | SH (body and FAQ) | **C** with AF (internship → exams) and MR/PRO/MT (studies → internship → exams) |
| 26 | 2023 reform led by the council: from 13 external exams to 6; more supervision of trainers; concentrated practical training | WIKI only | Pages from before or without the reform (PRO 2023-07, MT 2024, MR, SH) describe the old path; **verify** the current exam count |
| 27 | AIO: "תואר ראשון, לימודי שמאות, סטאז' (התמחות) ומבחנים ממשלתיים" | AIO | |

### 3c. Standards (תקינה שמאית) and guidelines

| # | Claim | Pages | Flag |
|---|---|---|---|
| 28 | Since the end of 2006 the council's הוועדה לתקינה שמאית has approved 20 standards; their status is "נורמת עבודה מומלצת בלבד" (not mandatory) | WIKI | **O/verify** (count and binding status) |
| 29 | תקן 19 = appraisal for collateral for credit ("בטוחה לאשראי"), "for commercial credit", value "בשיטה השמרנית" | JC | **U**: JC limits it to commercial credit, while WB labels its bank opinions generally as "בטוחה תקן 19". Whether it covers housing mortgages is unclear |
| 30 | תקן 21 = פינוי בינוי: 3 kinds of appraisal (developer economics, owners' consideration, viability per specific apartments) | PRO | **verify** (current version and number) |
| 31 | תקן 17.1 = developer appraisals / feasibility, incl. דוח אפס | MR | Only MR; **verify** |
| 32 | "שמאות לפי תקן 22" offered | TD (menu only) | Not explained anywhere; midrag has a link "מה זה תקן 22?" with no content on these pages |
| 33 | Midrag link titles: תקן 2, 6, 9 ("שטח דירה"), 10, 19, 21, 22 | MP, MT sidebars | Titles only, no content |
| 34 | IVS 1 market-value definition: willing buyer and seller, at arm's length, proper marketing, prudently, without compulsion | WIKI | |
| 35 | "הקווים המנחים" are written by the Chief Government Appraiser; updated 2007; 29 published | WIKI | **O/verify** (count); see #8 |
| 36 | Report minimum contents (per regulations): property identification, description of property and surroundings, rights valued, planning status, purpose, visit date, valuation date (המועד הקובע), principles | WIKI (cites "תקנות שמאי מקרקעין (אתיקה מקצועית), תשכ"ו-1966") | **verify**: the regulation predates the 2001 law; check the current name |
| 37 | MR version: identification, description, planning "בהווה ובעתיד", rights, infrastructure and surroundings, purpose | MR | Slightly different list from WIKI |
| 38 | Bank report includes photos, maps, נסח טאבו and a market-value recommendation | CAL | |

### 3d. Bank / mortgage appraisal

| # | Claim | Pages | Flag |
|---|---|---|---|
| 39 | You choose the appraiser from a limited list supplied by the bank ("מתוך מאגר מוגבל שמספק הבנק") | AFH, MT ("הבנק מציג רשימת שמאים מטעמו"), WB (list given after approval in principle) | consistent |
| 40 | "Since 2018 banks don't use a separate list; they must accept an appraisal by an appraiser approved by another bank" | WB | **U/verify** (no source) |
| 41 | The bank appraiser is not a bank employee; he is approved by the bank | WB | |
| 42 | You cannot order the bank appraisal from your own appraiser ("לא ניתן להזמין שמאי מטעמכם") | WB | Tension with MT ("אפשר להזמין יחד עם שמאי הבנק גם שמאי פרטי מטעמנו… לשאת ולתת מול שמאי הבנק") and TD (a private appraisal does not bind the bank appraiser) |
| 43 | Who pays: the mortgage applicant pays the bank appraiser directly, per the bank's tariffs | AIO snippet kolzchut; WB ("תלויה בתעריפים של אותו הבנק") | Not stated on most pages |
| 44 | Who gets the report: "הוא שולח את השומה לבנק ולא אליכם" | AFH | **C** with WB ("הבנק… מחויב להעביר העתק גם לכם") |
| 45 | Bank appraisal validity: 90 days ("תופסת ל-90 יום בלבד") | WB only | **U/verify** |
| 46 | Appeal: accepted almost always; rare exceptions; if the bank allows, via an approved appraiser and paid again | WB | |
| 47 | The bank uses the lower of contract price and appraisal | AFH | |
| 48 | Max LTV "נכון ל-2023": 75% of value | AFH | **O/incomplete**: stated as a single number with no buyer category; applies to single-apartment buyers only. **verify** against Bank of Israel rules |
| 49 | The bank appraiser also weighs quick-sale value (מימוש מהיר) and reinstatement cost (for insurance) | AFH | |
| 50 | Bank appraisers are conservative and serve the bank's interest | TD, MT, PRO, RA | EC: "השמאי אובייקטיבי… הדוח מותאם לדרישות הבנק" |
| 51 | Pre-appraisal (שמאות מוקדמת) is done before the contract by your own appraiser and costs more than the bank one; it can later be accepted by the bank if the appraiser works with all banks | AFH, WB | |
| 52 | "מחיר למשתכן": the bank sometimes allows a single appraiser who sets a very low value | AFH | **U** |
| 53 | "עשירית מהבקשות למשכנתה מסורבות" (lishka research) | TD | **U** (no source or date) |
| 54 | "שנת 2021 נרשמה כשנת שיא… בהיקף המשכנתאות" | RA | **O** |
| 55 | An appraisal is mandatory for a mortgage ("אף בנק ואף חברה חוץ בנקאית לא יעניקו… בלי הערכת שווי") | SH, CAL, AIO | |

### 3e. Decisive / advisory appraiser, betterment levy, disputes

| # | Claim | Pages | Flag |
|---|---|---|---|
| 56 | A MoJ unit (האגף לאסדרת מקצועות) runs the decisive-appraiser system under חוק התכנון והבנייה, התשכ"ה-1965: receives requests to appoint a שמאי מכריע or שמאי מייעץ, monitors performance, publishes decisions, handles case-merger / replacement / exceptional or partial fee / redaction requests, recruits candidates | GOV (updated 18.03.2026) | Authoritative; no deadlines or fees |
| 57 | Fee regulation: "תקנות התכנון והבניה (שכרו של שמאי מכריע ושמאי מייעץ), תשס"ט-2009" (tariff numbers not quoted) | GOV | |
| 58 | The decisive appraiser is appointed by the Minister of Justice; decides between the local authority and the citizen on levy amount or depreciation compensation; may also set expropriation compensation; appeal to ועדת ערר | WIKI | |
| 59 | The decisive appraiser decides between two conflicting appraisals | AF FAQ | |
| 60 | The appraiser submits the opinion "לשמאי המכריע או לוועדת הערר" and represents until a ruling | MP | |
| 61 | Advisory appraiser (שמאי מייעץ): only named (GOV) | GOV | **Gap**: nobody explains when it applies |
| 62 | Deadlines (e.g. 45 days to appeal or to request a decisive appraiser) | — | **Nobody states any deadline** |
| 63 | Levy = about half of the value increase ("כמחצית", "כ-50%") | TD, PRO, MT | consistent |
| 64 | Levy legal basis "סעיף 196 א' בחוק התכנון והבנייה"; triggers: new plan (תב"ע), relief (הקלה), non-conforming use (שימוש חורג) | SH, AFH (same 3 triggers) | SH text has a typo ("ראשית" = "רשאית") |
| 65 | Levy triggers include "חריגת בנייה", "החלפת ייעוד", "שינוי סביבת הנכס" | PRO, MT ("לבקש חריגת בניה") | **W**: illegal construction is not a levy trigger; this contradicts SH/AFH |
| 66 | The levy is charged to the owner or long-term lessee (חוכר לדורות); a contract clause moving it to the buyer does not bind the committee | AFH | |
| 67 | The levy is "imposed on the seller" | TD | **U** (simplification; see #66) |
| 68 | The local committee sets the increase through its own appraiser | PRO, MT | |
| 69 | Success claims: ">97% success" (JC); "הפחתנו 82%… 55%" (TD); AV case stories 232,000 cancelled; 150,000 → 50,000 "הפחתה של 70%"; 650,000 demand | JC, TD, AV | **U**; AV arithmetic **W** (it is 66.7%) |
| 70 | RMI (רמ"י) appraisals: dispute track with 2 tiers: (1) objection heard by a government appraiser (אגף שומת מקרקעין); (2) ועדת השגות, 3 members (a civil servant qualified as a magistrate, the chief government appraiser or deputy, a decisive appraiser); then an administrative petition to the district court | WIKI | |
| 71 | Expropriation-compensation objections committee established 2010, 3 members (same composition); petition to the district court | WIKI | |
| 72 | RMI charges are often inflated and based on interpretations convenient to RMI | JC | **U** (marketing) |
| 73 | Lishka dispute-resolution institute: arbitrators trained under the Arbitration Law / as mediators | LV | |

### 3f. Depreciation (section 197), expropriation, tax

| # | Claim | Pages | Flag |
|---|---|---|---|
| 74 | Section 197 of the Planning & Building Law allows owners to claim compensation for loss of value caused by an approved plan | JC, MR, AV (article title), MP/MT (link title), WIKI (decisive appraiser decides it) | |
| 75 | 197 time limit (e.g. 3 years from plan approval) | — | **Nobody states it** |
| 76 | Compensation is sometimes available for properties bordering the plan ("נכסים הגובלים בתוכנית"); depreciation causes listed: structural damage, water damage, ground movement, new roads, public buildings | AFH | **U**: mixes 197 with physical damage claims |
| 77 | Expropriation is allowed by Mandate-era laws, with compensation | SH | |
| 78 | Local committee can take land for public needs (cemetery, railway) | PRO, MT | |
| 79 | Expropriation is "פעולה קניינית ולא תכנונית", but can be done under the Planning & Building Law | JC | |
| 80 | "זכות במקרקעין" (land tax law) = ownership, lease over 25 years, or a usage permit | JC | |
| 81 | IFRS adopted in Israel from 2008; public companies report real estate at market value | JC; WIKI (IFRS encourages periodic valuations) | |
| 82 | מס שבח: single-apartment owners get a partial or full exemption up to a certain amount; unused building rights are taxed | SH, TD | no amounts |
| 83 | The old 4-year exemption is gone; "today there are fewer exemptions" | AFH | Historical, correctly framed |
| 84 | מס רכישה by brackets updated yearly; higher for non-residential use and for additional apartments | AFH, PRO, MT | |
| 85 | "הערכת שווי נכס משמשת בסיס לקביעת שיעורי המס העירוניים" | AF | **W** for Israel (municipal arnona is not value-based); generic text |
| 86 | "בהתאם לדוח שמאי… נקבע גובהם של תשלומי המס כמו מס שבח… והיטל השבחה" | IV | **W/overstated** (a private report does not set the tax) |
| 87 | "חוק יחסי ממון… מחייב חלוקה שוויונית לחלוטין של כלל הרכוש" | SH | **W/overstated** (the law has exceptions) — **verify** |
| 88 | "לדו"ח הממצאים תוקף משפטי" / "בעל אופי משפטי" usable with the tax authority | PRO, MT | **U** (vague) |
| 89 | "רק שמאי מוסמך יכול לתת מסמך קביל בבית משפט" | CAL | **U** |
| 90 | An illegal 15 m² of 100 m² → 450,000 less on a 3,000,000 apartment | MT | Arithmetic consistent |
| 91 | An illegal 25 m² of 100 m² → true value more than 25% below price (4M+ apartment) | TD | **U** |

### 3g. Process, timing, validity, methods

| # | Claim | Pages | Flag |
|---|---|---|---|
| 92 | Report turnaround: 3-7 business days; express 24-48 h | EC | Only source |
| 93 | "כמה לוקח שמאי מקרקעין?" answered with a price, no time given | MP FAQ | **W** (mis-answer) |
| 94 | Report validity: 90 days (bank) | WB | Only source; **verify** |
| 95 | Methods: comparison (most common), cost (new and unique assets), income capitalisation (commercial) | SH | |
| 96 | 3 approaches (comparison, income, cost); comparison preferred; income not used for residential; British 5 methods incl. residual (שיטת היזמות/השווי השיורי), named but not explained | WIKI | Residual is not explained anywhere |
| 97 | Bank appraisal: "כמעט תמיד" by comparison with same street or neighbourhood deals from the last year; factors listed (floor, elevator, balcony, aspects, parking, garden, roof, view, main road) | WB | |
| 98 | Value factors: elevator, floor (high floor without an elevator lowers value), parking registered in טאבו, underground parking, green space, schools/roads (near = good, too near = bad), polluting plant, power lines, cellular antennas ("לא באופן מובהק") | AFH | |
| 99 | Appraiser vs lawyer: appraiser at the interest stage (value, checks); lawyer before signing (contract, guarantees, registration) | PRO, MT | |
| 100 | Appraiser vs בדק בית: the appraiser's physical check is partial; for defects use a home-inspection firm | MT; SH FAQ says many appraisers do building inspections | mild **C** |
| 101 | An appraiser (often with an engineer) checks physical condition (cracks, damp) | PRO, MT, SH, TD | |
| 102 | Decisive-appraisal decisions are public (GIS and legal databases) | WIKI, GOV | |

---

## 4. Topics union

Coverage key: ● = covered with substance, ○ = mentioned or thin.

| Subtopic | Covered by | Quality note |
|---|---|---|
| Definition (מה זה שמאי מקרקעין) | ● SH, AF, WIKI, PRO, MT; ○ IV, AIO | Good |
| What the appraiser checks (legal, permit, planning, engineering, environment, tax) | ● SH, PRO, MT, AFH; ○ TD, RA, SHP, DZP, WB | Good, but repetitive |
| Types of appraisals by purpose (market, bank collateral, tax, court, levy, RMI, IFRS, zero report, expropriation, 197, rent, urban renewal, balance tables, protected tenancy) | ● JC, MR, IV; ○ TD, SH, PRO, MT, WIKI, CAL, WB (nav) | Spread across office homepages as teasers |
| Bank appraiser vs private appraiser | ● AFH, WB, TD, MT; ○ RA, PRO, EC | Contradictions on report copy and private appraiser (see 3d) |
| Pre-purchase appraisal (שמאות מוקדמת) | ● AFH, WB, TD; ○ RA, MT, CAL, EC | No checklist, no price consensus |
| Costs | ● MP, EC, DZP, SHP, SH, CAL; ○ DZ, AIO | Inconsistent; old; VAT unclear |
| What drives the price | ● MP, CAL, EC, BN; ○ SH, DZP | Contradictory (value / purpose matter or not) |
| How to choose an appraiser | ● SH (question list), MR, MT, BN; ○ PRO, DZ, CAL | |
| How to verify a licence (register lookup) | ○ PRO, MT, MR, DZ | **Nobody gives the actual lookup steps or the URL** |
| Licensing path | ● SH, MR, WIKI; ○ PRO, MT, AF, AIO | Contradictory numbers |
| Council vs lishka | ● WIKI; ○ MR, LV, AIO | Thin elsewhere |
| Appraisal standards (by number) | ○ JC (19), WB (19), PRO (21), MR (17.1), TD (22), WIKI (general) | **Nobody explains the standards to a consumer** |
| What the report contains | ● WIKI; ○ MR, CAL, AFH | No sample report or section walk-through (PRO links to a separate 2025 guide "דו"ח שמאות מקרקעין: המדריך המלא לפענוח המספרים") |
| Documents to prepare | — (SH only lists "איזה מסמכים אתה צריך ממני?" as a question to ask; CAL names נסח טאבו and תשריטים as appraiser inputs) | **Gap** |
| Timelines (turnaround, validity) | ○ EC (3-7 days), WB (90 days) | **Gap** |
| Betterment levy (what, 50%, triggers, who pays) | ● SH, AFH, TD, PRO, MT; ○ JC, MR, IV, BN | Errors in PRO and MT |
| Levy dispute: counter-appraisal, decisive / advisory appraiser procedure | ● GOV (functions), WIKI (role, appeal); ○ AF, MP, MR, IV, AV, JC, TD | **No step-by-step, no deadlines, no fees** |
| Urban renewal / TAMA 38 / tenants' appraiser | ● PRO (תקן 21), MT; ○ SH, JC, TD, EC, IV | No numbers |
| Court, inheritance, divorce, partition | ● SH, MR, PRO, CAL; ○ JC, TD, MT, DZ (guide titles), DZP (prices), LV (mediation) | |
| Depreciation and section 197 | ○ JC, MR, AV, WIKI, AFH, PRO, MT | **Time limit and procedure: nobody** |
| Expropriation compensation | ● WIKI (objections committee); ○ JC, SH, PRO, MT, MR, CAL | |
| Valuation methods (comparison / cost / income / residual) | ● SH, WIKI; ○ PRO, MT, AF, WB | **Residual method: named only (WIKI)** |
| Value factors (floor, elevator, parking, nuisances) | ● AFH, WB; ○ SHP, TD | |
| Taxes (מס שבח, מס רכישה) | ● SH, AFH, PRO, MT; ○ TD, MR, JC, BN | |
| RMI payments (דמי היתר, הסכמה, היוון) | ○ JC, MR, IV, MT, WIKI | |
| Appraiser vs lawyer / vs home inspection | ● PRO, MT; ○ SH FAQ | |
| LTV / lower-of rule | ○ AFH | Dated |
| Complaints about an appraiser (תלונה) | ○ WIKI (council handles complaints), LV (ethics committee) | **Gap**, and it is a related search |
| Find an appraiser by region | ● DZ, MP, PRO, MT; ○ LV ("איתור שמאי/ת"); local pack | |
| Appraiser career, salary, internship | ○ AF (course funnel); related searches | Off-intent for buyers |
| IFRS / zero report / feasibility | ○ JC, MR, WIKI, WB | |
| Price calculator | — | **Nobody** (yet "מחשבון שמאות דירה" is a related search and eliasaf "test-calculator" ranks #14) |
| What to do if the bank appraisal is low | ○ WB (appeal rare); MP sidebar link only | **Gap** |
| VAT on appraisal fees | ○ EC (FAQ), AIO | **Contradictory** |

Subtopics nobody covers well (synthesis):
1. A consistent, dated, sourced price table by purpose and property type, with a clear VAT position (incl./excl.).
2. Decisive / advisory appraiser procedure: who may apply, steps, deadlines, fee regulation, ועדת ערר.
3. Section 197 claims: time limit, who pays, procedure.
4. Licence verification: how to search the register and what a licence number shows.
5. Documents to prepare before the appraiser visits; turnaround time; report validity.
6. The appraisal standards in plain language (19, 21, 22, 17.1 and others): what each means for the client.
7. Bank appraisal mechanics, from the current rules: who chooses, who pays, copy of the report, validity, low-appraisal options.
8. Residual / developer method (relevant to land and urban renewal).
9. Complaint and ethics route.
10. A calculator or estimator.

---

## 5. Questions harvested

Note: no People also ask box appeared on any of the 3 SERPs. Duplicates are merged; source tags in brackets.

### 5a. FAQ blocks (visible FAQ or FAQPage schema)

- מה תפקידו של שמאי מקרקעין? [AF visible FAQ]
- איזו הכשרה נדרשת כדי להיות שמאי מקרקעין? [AF visible FAQ]
- מהי ההכשרה הנדרשת כדי להפוך לשמאי מקרקעין? [AF schema/H2]
- מה הם תפקידיו המרכזיים של השמאי בתהליך הערכת הנכס? [AF schema/H2]
- כיצד שמאי מקרקעין מסייע בקביעת שווי שוק אמיתי לנכסים? [AF schema/H2]
- מתי צריך שמאי מקרקעין? [AF FAQ]
- מה ההבדל בין שמאי לשמאי מכריע? [AF FAQ]
- מה זה שמאי מקרקעין? [SH FAQ; MT TOC]
- אילו נכסים נכללים בהגדרה נדל"ן? [SH FAQ]
- כיצד הופך אדם לשמאי מקרקעין? [SH FAQ]
- כל מי שלומד שמאות מקרקעין יכול להיות שמאי מקרקעין? [SH FAQ]
- איפה עובד שמאי מקרקעין? [SH FAQ]
- מתי נדרשים שירותיו של שמאי מקרקעין? [SH FAQ]
- האם שמאי מקרקעין מבצע גם ביקורות מבנים? [SH FAQ]
- איך שמאי מקרקעין קשור להיטל השבחה? [SH FAQ]
- מה עושים במקרה של הפקעת מקרקעין? [SH FAQ]
- איך לבחור שמאי מקרקעין מומלץ ומקצועי שמתאים לצרכים שלי? [DZ schema]
- איך אני יכול להיות בטוח שהמידע על שמאיי המקרקעין באתר אמין ומעודכן? [DZ schema]
- למה כדאי לחפש שמאי מקרקעין דווקא בדפי זהב ואיך מערכת הסינונים עוזרת לקבל פתרון מהיר? [DZ schema]
- כמה לוקח שמאי מקרקעין? [MP schema]
- מה בודק שמאי מקרקעין? [MP schema]
- איך בוחרים שמאי מקרקעין? [MP schema]
- האם המחיר כולל מע"מ? [EC schema]
- תוך כמה זמן מקבלים דוח שמאות? [EC schema]
- האם השמאי מייצג אותי או את הבנק? [EC schema]
- האם יש הנחה לשמאות מרובה? [EC schema]
- אז איך שמאי מעריך דירה כשהוא מגיע דרך הבנק, באחוזים ? [AFH schema]
- מה ההתייחסות המשפטית של הערכת שווי של דירה יד שניה מבחינת שמאי המקרקעין? [AFH schema]
- איך קובעים? הערכת המשכנתא או מחיר החוזה? [AFH schema]
- איך שמאי מעריך דירה יד שניה (2) במקרה של תכנית למשתכן? [AFH schema]
- אחרי הערכת שווי הדירה על ידי שמאי מקרקעין, מה לגבי משכנתא? [AFH schema]
- מהי שמאות מוקדמת ואיך שמאי מעריך דירה באופן הזה? [AFH schema]
- איך שמאי מעריך דירה לפיצויים? [AFH schema]
- מה מעלה ומה מוריד את ערך הדירה ואיך שמאי מעריך את זה? [AFH schema]
- איך שמאי מקרקעין מעריך היבטי מיסוי ברכישת דירה יד 2? [AFH schema]
- כמה עולה הערכת שמאי לדירה? [DZP intro]
- מהו שכר הטרחה של שמאי מקרקעין? [DZP intro]

### 5b. Question-form headings, TOCs and on-page question lists

- הגדרת התפקיד – מה עושה שמאי מקרקעין? / מתי צריך לפנות לשמאי מקרקעין? / כיצד מתבצעת הערכת שווי נכס? השיטות המקובלות / מה בודק שמאי מקרקעין כדי להעריך שווי נכס? / מי יכול להיות שמאי מקרקעין? / איך לבחור שמאי מקרקעין מקצועי? [SH H2]
- Questions to ask the appraiser [SH]: באילו תחומים אתה מתמחה? / איך עובד התהליך? / איזה מסמכים אתה צריך ממני? / מה תבדוק לגבי הנכס? / האם תוכל להציג לי דוגמה לעבודה דומה לזו שתספק עבורי? / האם אתה נכלל ברשימה של הבנק (כשהמטרה היא חוות דעת למשכנתא)? / כמה זמן נמשך התהליך עד לקבלת חוות הדעת?
- Checks before choosing [BN]: מהי השכלתו של השמאי? / האם השמאי בו אתם מתעניינים חבר בלשכת השמאים? / אילו לקוחות גדולים משרת/שירת השמאי? / האם ישנה אפשרות לבניית סל שירותים בהתאמה אישית?
- מה משפיע על מחיר שמאי מקרקעין? [BN H1] / אז איך שמאי המקרקעין יוכל לסייע לכם? [BN] / האם מחיר שמאי מקרקעין ותיק ומנוסה יהיה יקר יותר ממחיר שיוצע על ידי שמאי בתחילת דרכו? [BN]
- מחיר שמאי מקרקעין - איך קובעים אותו? / מה כלול במחיר? / מה משפיע על מחיר שמאי מקרקעין להערכת שווי דירה? (and the same for דמי שכירות, נחלה, הפחתת היטל השבחה, חוות דעת מומחה) / מה המחיר הממוצע? [MP]
- כמה שירותיו של אותו שמאי מקרקעין עולים? [MP opening]
- למה צריך שמאי מקרקעין? / חברת בדק בית או שמאי מקרקעין? / מה ההבדל בין עורך דין מקרקעין לשמאי מקרקעין? / איך לבחור שמאי מקרקעין? [MT TOC]; איך נוכל לדעת מה המצב ושווי הדירה האמיתיים? [MT]
- מהי שמאות מקרקעין? / מה ההבדל בין שמאי מקרקעין לבין עורך דין? / איך תזהו שמאי מקרקעין מוסמך? [PRO TOC]; הערכת שווי דירה: מתי צריך ולמה זה מומלץ? [PRO related]
- איך נבחר שמאי מקרקעין נכון? / מה חשוב בשמאי מקרקעין? [MR H2]
- האם אתם בטוחים שהמוכר אכן הנו בעליו החוקיים של הנכס? / למה צריך שמאי מקרקעין לפני רכישת דירה? / למה חשוב להסתייע בשמאי מקרקעין לפני עסקת נדל"ן? [TD H2]; מתכננים למכור או לרכוש דירה? מתלבטים האם להסתייע לצורך זה בשירותיו של שמאי מקרקעין? [TD]
- מה זה שמאי מקרקעין ואיך הוא תורם לשוק הנדל"ן? [AF H1]; שומה נגדית – מה זה שומה נגדית ומתי היא הופכת לכלי קריטי בהגנה על שווי הנכס? [AF related]
- אז איך שמאי מעריך דירה, מה המחיר, ואיך מחשבים הערכת מחיר דירה יד 2 ? / כיצד בודק שמאי המקרקעין את ערך הדירה למשכנתא? מה קובע את הערך לפני קניית הדירה? איך מחשבים פיצויים? ומה לגבי המיסים? [AFH H2]
- מה לוקח בחשבון שמאי מקרקעין? / מיהו שמאי מקרקעין מקצועי? / חשבתם פעם איך קובעים את הערך של הדירה? מי קובע כמה בדיוק אתם צריכים לשלם על הנכס…? [SHP]
- באילו מקרים חובה להזמין שמאות? / ממה מורכב המחיר? / מתי חשוב להזמין שמאות לפני מכירה? / מתי חובה להזמין שמאות כזו? / צריכים שמאי מקרקעין מקצועי? [CAL]
- מה משפיע על המחיר? / מתי כדאי להזמין שמאות? / "כמה עולה שמאות לדירה?" [EC]
- כמה עולה שמאי מהבנק [WB H1]; מצויים בהליכי בקשה לקבלת משכנתא? מעוניינים להבין היכן נכנס לתמונה השמאי וכמה זה יעלה לכם? [WB]
- לוקחים משכנתא? כדאי לכם ללכת על הערכת שומה מוקדמת / מוכרים נכס? זו הסיבה שכדאי לכם להתייעץ עם שמאי / מה קרה למחירי הדירות מאז פרוץ משבר הקורונה? / רוצה לדעת יותר על שמאות מקרקעין ? [DZ guides]
- רוכשים נדל"ן וצריכים הערכת שמאי? [RA]

### 5c. Midrag related-topic question links (MP and MT sidebars; titles only)

מה זה היטל השבחה? · מה זה מיסוי מקרקעין? · מה ההבדל בין היטל השבחה ומס שבח? · מה זה מס שבח? · מה זה תמא? · שמאות למשכנתא - מה זה? · מה זה הפקעה? · מה זה מס רכישה? · מה זה תקן 22? · מה זה ערבות חוק מכר? · מה זה מס שבח מקרקעין? · מה זה אישור מס שבח? · הסכם השבה - מה זה? · מה עושים אם מקבלים הערכת שמאי מקרקעין נמוכה? · שמאי מכריע - מה זה? · מה ההבדל בין תמא 38/1 לתמא 38/2? · הפחתת מס שבח - מה זה? · תקן 21 - מה זה? · תקן 19 - מה זה? · מה זה תת חלקה? · מה זה תת חלקה בטאבו? · שטח הדירה בטאבו לעומת ארנונה מה ההבדל? · מה זה טאבו מקרקעין? · למי משלמים מס רכישה? · איך למצוא גוש חלקה לפי כתובת? · האם יש מס על דירה שניה? · שומה מקוצרת - מה זה? · תביעה לפי סעיף 197 - מה זה? · האם יש מס על מכירת דירה? · האם יש מס שבח על דירה יחידה? · מה מוריד את ערך הדירה? · שומת מקרקעין - מה זה? · ערך כינון שמאות - מה זה? · תקן 9 שטח דירה - מה זה · גודל דירה בטאבו - איך מודדים? · תקן 6 - מה זה? · תקן 10 - מה זה?
Topic (non-question) links in the same sidebar: עלות שמאי משכנתא · שמאות מוקדמת מחיר · שמאי משכנתא · שמאי דיירים בפינוי בינוי · הערכת שמאי במחיר למשתכן · קניית דירה לפני פינוי בינוי · שווי דירה לפי קומה · שמאי מכריע היטל השבחה · שמאי מקרקעין חוות דעת לבית משפט · תקן 2 שמאות מקרקעין · דוח אפס · שמאי חקלאות · פיצויי הפקעה · בדיקת שווי נכס · בדיקת היתרי בנייה · בדיקת תב"ע · בדיקת נסח טאבו · חישוב שטח דירה ארנונה.

### 5d. SERP: related searches, people also search, AI overview prompts, forum titles

- Related searches "שמאי מקרקעין" (desktop): מתמחה שמאי מקרקעין · מכרזים שמאי מקרקעין · שמאי מקרקעין מרכז · משרד שמאי מקרקעין · שמאי מקרקעין בצפון · שמאי מקרקעין אשקלון · תלונה על שמאי מקרקעין · שמאי מקרקעין חדרה
- People also search (mobile), in addition to the above: דרושים שמאי מקרקעין · דמי חבר לשכת שמאי מקרקעין · שמאי מקרקעין אשדוד · קווים מנחים שמאי מקרקעין
- Related searches "כמה עולה שמאי": הערכת שמאי לדירה מחיר · שמאי דירה מחיר · מחשבון שמאות דירה · רשימת שמאים בנק מזרחי טפחות · שמאי מקרקעין · שמאות תקן 19 עלות · שמאי מקרקעין שכר · טריא now on · טריא שאלות ותשובות · טריא חדשות
- AI overview follow-up prompts: באיזה צורך מדובר (משכנתא, קניית דירה, היטל השבחה, ירושה)? · באיזה אזור בארץ נמצא הנכס? · איזה סוג של שמאי אתה צריך (מקרקעין, רכב או רכוש)? · מהי מטרת השומה (משכנתא, תאונה, קניית דירה)?
- Organic forum titles (real user questions): שלום? מהו המחיר המקובל להערכת שמאי מטעם הבנקים · היי יש לי שאלה בערכה גסה כמובן כמה עולה להביא שמאי להעריך ...

---

## 6. Heading DNA

### Common H2 patterns

1. **Definition:** "מה זה / מהי שמאות מקרקעין / מה עושה שמאי מקרקעין" (SH, PRO, MT, AF).
2. **When you need one:** "מתי צריך (לפנות ל)שמאי מקרקעין" / "באילו מקרים חובה להזמין שמאות" / "מתי כדאי להזמין שמאות" (SH, CAL, EC, AF FAQ).
3. **Purpose ladder, "שמאי מקרקעין ל-X":** להערכת שווי נכס / לבדיקת מיסוי מקרקעין / בפרויקט תמ"א 38 / לחוות דעת משפטית / לקבלת היטל השבחה / שירותים נוספים (PRO and MT, almost identical). Office homepages do the same as numbered service cards (MR 01-09, JC H3 cards, IV bullet list, TD menu).
4. **Method and checks:** "כיצד מתבצעת הערכת שווי נכס? השיטות המקובלות" + "מה בודק שמאי מקרקעין" (SH); "שלוש גישות שומה" (WIKI); a sub-list of checks (סביבה, משפטית, היתר, תכנונית, הנדסית, מיסים) in PRO, MT, SH.
5. **Who can be one / licensing:** "מי יכול להיות שמאי מקרקעין" / "מסלול ההכשרה" / "איך תזהו שמאי מקרקעין מוסמך" (SH, MR, PRO, AF).
6. **Choosing:** "איך לבחור שמאי מקרקעין (מקצועי / נכון)" (SH, MR, MT, BN).
7. **Cost:** "עלות שירותי שמאות מקרקעין" / "טווח מחירים עדכני" / "מה משפיע על המחיר" / "ממה מורכב המחיר" (SH, EC, CAL, BN, MP).
8. **Versus:** "מה ההבדל בין שמאי מקרקעין לעורך דין" / "חברת בדק בית או שמאי מקרקעין" (PRO, MT).
9. **Price-page template (MP):** one H2 per service, each with H3 "מה כלול במחיר? → מה משפיע על המחיר? → מה המחיר הממוצע?", then "שמאי מקרקעין מומלצים" and an FAQ.
10. **Fear and story H2s on office pages:** "האם אתם בטוחים שהמוכר…", "דחיית בקשות למשכנתה מצד הבנקים", "טעויות בהערכת שווי הדירה" (TD); "השורות הקטנות שכדאי לבדוק" (BN).

### How the strongest pages open (first 2 sentences, paraphrased)

- **SH (#4, exact H1):** Appraisal matters more than ever as prices keep rising; at its core it means valuing every kind of property, apartments above all. A licensed appraiser gives reasoned opinions for buying, selling, mortgages, urban-renewal offers and moshav nachala upgrades. The profession is regulated and supervised by the council.
- **AF (#11):** An appraiser is a critical profession in real estate that gives accurate valuations. It then asks three questions: what training is needed, what is the role in valuing property, and how does it set a true market value?
- **PRO (#13):** You will hire an appraiser when you buy, or when projects happen around your home; this guide explains all the checks and roles. A box follows: "what is appraisal, why check value, what other checks, how is it different from a lawyer".
- **MT:** Prices are not the only problem when buying; taxes, transfer of ownership and defects can raise the cost or kill the deal. An appraiser warns you in advance and gives a true value. Then a case: a 3M apartment with 15 illegal m² = 450,000 less.
- **WIKI (AIO source):** Appraisal is the profession of estimating market value of real estate. It is needed because property is heterogeneous and location-driven, so there is no central exchange price.
- **MP (price owner):** You face the deal of your life and know an appraiser protects it, but how much does the appraiser cost? It depends on the service, e.g. an apartment valuation is 2,500-4,000 on average.
- **TD (#3):** Planning to buy or sell and wondering whether to use an appraiser? A home is the biggest economic deal of your life, so consult one first. Then a case: a 4M+ apartment with 25 illegal m².
- **JC (#2):** Office founded in 1996 by a former senior ILA official, with a list of expertise (feasibility, land tax, levy, collateral).
- **EC:** First person: "the question I'm asked in almost every call is how much an appraisal costs"; there is no single answer, just as no two apartments are alike.
- **CAL:** People call an appraiser only under time pressure (sale, bank demand); the valuation is not a form, it is a document that moves a deal of hundreds of thousands.
- **WB (#1 price query):** In the mortgage process and want to know where the appraiser comes in and what it costs? The bank appraiser is not a bank employee but an approved professional.

---

## 7. What Google wants

For "שמאי מקרקעין", Google returns mostly entities rather than guides. The association (LV) is #1 on both devices with a member-services page that has almost no consumer content. Positions #2 to #8 are Tel Aviv office homepages (JC, TD, SH, AV, mikied, MR), mixed with directories (midrag search results #5, d.co.il #9, pro #13) and a 3-pack of Tel Aviv offices with large review counts (4.9/434, 5/222, 5/100). So the main intent is "find a credible, licensed appraiser", and authority, office identity and reviews carry most of the weight.

The AI overview handles the informational layer. It draws on WIKI, IV, LV, kolzchut, gov.il (land_assessor), nadlancenter, colman, TheMarker, harel-vered, MT and PRO. It covers the definition, a role list (valuation, pre-deal checks, mortgage report, levy / tax / depreciation reductions, court and inheritance or divorce opinions), when you need one, and regulation (the law, the council in MoJ, degree + studies + internship + government exams). It then sends users to pro.co.il and the lishka. It closes by asking the purpose and region, which signals that Google expects purpose-specific and local follow-ups.

For "כמה עולה שמאי", the AI overview builds a price ladder by property type and purpose, mainly from midrag pages, ec-shamaut, shamaotil, moshka, eliasaf and koorsim. It mixes in car and property-damage appraisers. Meanwhile the organic top 10 is weak: WB #1 states no price at all; tarya (#2) is off-topic; AFH (#3) has no numbers; DZP, CAL, SHP and RA are thin, old or contradictory. No page in the set offers a calculator, even though "מחשבון שמאות דירה" is a related search.

The opening is a single page that does three things together:
- an exact-match, licence-first explainer (law, council vs lishka, how to verify the register);
- a dated, sourced price table by purpose and property type, with a clear VAT stance and court / levy / urban-renewal rows;
- the procedural gaps nobody covers: bank appraisal rules, decisive / advisory appraiser steps and deadlines, 197 time limits, documents, turnaround and validity.

FAQPage markup should match the visible FAQ.
