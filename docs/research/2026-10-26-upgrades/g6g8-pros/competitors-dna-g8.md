# G8 competitor DNA: "עורך דין מקרקעין" / "עורך דין קניית דירה" / "real estate lawyer israel"

Target page: https://nad-lan.co.il/real-estate-lawyer/
Sources (local only): `serp/g6g8/g8_summary.txt` (+ the raw `g8_d.json`, `g8_m.json`, `g8p_d.json`, `en_d.json` for the full AI overview text and references), `raw/g6g8/index-urls_g8.json`, and every `g8-*`, `g8p-*`, `g8en-*` .txt / .reader.md / .html. SERP retrieved 26.10.2026 at about 11:33 UTC, pages fetched 11:37 to 11:38 UTC.
Query codes: **Q1** = "עורך דין מקרקעין" (D = desktop, M = mobile), **Q2** = "עורך דין קניית דירה" (desktop), **EN** = "real estate lawyer israel" (desktop).

Capture caveats:
- **g8-carish**: both the .txt and the .html are a gzip stream that was saved as text, so the 0x8B bytes became U+FFFD and the file can't be recovered (I tried a byte-by-byte raw-deflate decode and it failed). Only its SERP title is known. The index entry of 1,208 words comes from the corrupted bytes and means nothing.
- **g8-lawfind** (DNS failure) and **g8-yonilevy** (HTTP 403): only the reader.md exists, so the schema and FAQ markup are unknown.
- **g8-dcoil**: the captured URL (Bnei Brak) returned a "no results" page. The SERP shows it with the title "עורך דין מקרקעין, בבני ברק". It's unclear whether this is a bot or geo difference.
- I counted word totals with Python. Hebrew word counts from Git-bash `wc` were wrong, so I didn't use them.

---

## 1. Competitor table

### 1a. Identity and structure (one row per competitor)

| # | Name | SERP pos (query) | URL | Title | H1 | Words | H2/H3 | Tables | Imgs | FAQ (schema?) | Tools / forms | Schema types | dateModified |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | g8-lawfind | Q1 #1 D, #1 M | lawfind.co.il/landingpage.aspx?rama1=11 | "עורך דין נדל"ן, עורכי דין נדל"ן" (SERP: "עורכי דין נדל"ן") | עורכי דין נדל"ן | 10,550 (reader; mostly ~70 article teasers; legal-info block ≈271) | 0/0 (layout text) | 0 | ~120 (reader) | none | "fill details and send to all marked lawyers" multi-lawyer form; hotline 03-6958791; 3 lawyer cards | unknown (fetch failed) | none (content cites 2008–2013 rules) |
| 2 | g8-midrag-99 | Q1 #2 D, #2 M | midrag.co.il/Content/SecFeedbacksIndex/99 | עורך דין מקרקעין \| חוות דעת והמלצות - באתר מידרג | 5,451 חוות דעת על עורך דין מקרקעין | 196 raw / 1,723 reader (nav) | 1/2 | 0 | 24 | none | review index A–Z (2 sub-services shown); site counters 3,142,131 reviews / 12,509 pros / 149 sectors; app links | none | none |
| 3 | g8-dcoil | Q1 #3 D (Bnei Brak), #6 M (other d.co.il city URLs at D #7, #10, #15, #18, #19) | d.co.il/h-c9010118-e0-p0-l0-city6100-t1000000190.nb1/ | captured: "לא נמצאו תוצאות - דפי זהב No-Results" (SERP: "עורך דין מקרקעין, בבני ברק") | לא נמצאו תוצאות חיפוש עבור: עורכי דין - דיני מקרקעין בבני ברק | 74 raw / 1,430 reader (nav) | 2/1 (empty) | 0 | 4 | none | "AI Mode" search; link to "מחירון עורכי דין מקרקעין" (price list, not captured) | none | none |
| 4 | g8-carish | Q1 #4 D, #4 M | carish.org.il/עורך-דין-מקרקעין | SERP: "עורך דין מקרקעין - כל עורכי הדין כל המחירים!" | unclear | unclear (capture corrupted) | unclear | unclear | unclear | unclear | unclear (title promises "all prices") | unclear | unclear |
| 5 | g8-cohenlawyers | Q1 #5 D, #5 M | cohenlawyers.co.il/blank-2 | מקרקעין / נדל"ן \| boutique-law-firm | (template error) phone "03-5277032" + address line | 661 (body ≈629) | 2/0 | 0 | 3 | none ("FAQPage" string in Wix code only) | none (contact details) | none in JSON-LD | none |
| 6 | g8-irelaw | Q1 #8 D, #8 M | ire-law.com/he/ | עורך דין מקרקעין בישראל \| קנייה, מכירה ומיסוי | עורך הדין שלך למקרקעין בישראל. | 2,422 | 14/67 | 0 | 88 | 12 (FAQPage ✓) | book a call, free first consult, WhatsApp, Google 4.9 (127), "ask AI about Ella" widget, 48 guide links, llms.txt | AdministrativeArea, AggregateRating, Answer, ContactPoint, Country, FAQPage, GeoCoordinates, ImageObject, Offer, OfferCatalog, Organization, Person | 2026-07-29 (pub 2026-05) |
| 7 | g8-yonilevy (TA page) | Q1 #9 D, #10 M; homepage yonilevy.co.il cited in AIO (M) | yonilevy.co.il/עורך-דין-מקרקעין/עורכי-דין-מקרקעין-תל-אביב/ | עורכי דין מקרקעין תל אביב (SERP adds "- ניסיון של שנים בתחום הנדל"ן") | עורכי דין מקרקעין תל אביב | body ≈809 (reader 10,400 incl. nav/URLs) | 4/1 (+4 h4 FAQ) | 0 | many (reader) | 4 visible; schema unknown (403) | callback form, WhatsApp, Messenger, intro video, Google 5.0 (137) | unknown | "updated 18/10/2023" (published 2023-10-18) |
| 8 | g8-psakdin | Q1 #11 D, #11 M (a Givatayim variant at #13/#14) | psakdin.co.il/Lawyers?CatID=1100 | עורך דין נדל״ן - פסקדין | עורך דין ומשרדי עורכי דין נדל"ן | 3,835 (~56 lawyer cards; intro ≈230) | 3/1 | 0 | 142 | none | lawyer search by field / sub-field / area / city; "הלפי" legal bot; legal calculators link; newsletter | none | none |
| 9 | g8-hakoach | Q1 #17 D, #18 M | hakoach.co.il/עורך-דין-מקרקעין/ | עורך דין מקרקעין \| הכוח שבצדק | עורך דין מקרקעין | 3,988 | 0/58 (article cards) | 0 | 1 | none | none (category archive of 58 posts) | none | newest post 21.7.2026 |
| 10 | g8-lawreviews (real-estate) | Q1 AIO reference (D+M); not in HE organic top 19 (its EN twin is EN #4) | lawreviews.co.il/search/real-estate | עורך דין מקרקעין מומלץ (נדל"ן) \| לפי 1292 חוות דעת \| LawReviews | עורכי דין מקרקעין ונדל"ן מומלצים ע"י לקוחות | 4,234 (info + FAQ ≈1,941) | 8/38 | 0 | 28 | 10 visible (no FAQPage) | search by field/area; "רוצים לקבל כמה הצעות מחיר" quote form; 144 lawyers with stars/review counts; filters (language, gender, virtual consult); city links; "people also searched" | BreadcrumbList, CollectionPage, ImageObject, ItemList, LegalService, ListItem, Organization, PostalAddress, WebSite | none |
| 11 | g8-gelberg (home) | Q1 AIO reference (D+M) + local pack #2 ("נאור גלברג - עורך דין מקרקעין ונדל״ן"); not in organic top 19 | gelberglaw.co.il/ | עורך דין מקרקעין ושמאי מקרקעין \| עו״ד נאור גלברג | עו"ד נדל"ן ושמאי מקרקעין נאור גלברג | 7,431 | 13/16 (+25 H4 FAQ) | 0 | 116 | 25 visible (no FAQPage) | contact forms, WhatsApp, "full checklist" lead magnet, calculator menu (purchase tax, CGT, construction-input index, delay compensation, rent tax), podcasts, Google 5.0 (124), "traffic-light method" | BreadcrumbList, CollegeOrUniversity, Country, EducationalOccupationalCredential, EntryPoint, ImageObject, ListItem, Offer, OfferCatalog, OpeningHoursSpecification, Person, PostalAddress | 2026-09-22 (pub 2023-10-27) |
| 12 | g8p-addalaw | Q2 #1 | addalaw.co.il/lawyer-for-buying-an-apartment/ | עורך דין קניית דירה \| מדריך מקיף מבוסס על מאות עסקאות \| עו״ד מור עדה | עורך דין קניית דירה \| מדריך מקיף מבוסס על מאות עסקאות | 16,331 | 58/83 | 3 (LTV by buyer type; 2nd-hand vs developer; fee-quote comparison card) | 39 | 6 (FAQPage ✓) | contact forms; fee comparison card; "LawReviews 4.9 (90)"; footer link "Hey AI, learn about this page" | AggregateRating, Answer, Article, BreadcrumbList, CommentAction, ContactPoint, CreativeWork, EntryPoint, FAQPage, GeoCoordinates, ImageObject, ListItem | 2026-07-02 (pub 2025-09-14) |
| 13 | g8p-lawreviews-buy | Q2 #2 | lawreviews.co.il/search/service/buying-apartment | עורך דין קניית דירה מומלץ \| LawReviews | עורכי דין קניית דירה מומלצים ע"י לקוחות | 4,788 (info + FAQ ≈2,709) | 7/31 | 0 | 18 | 10 visible (no FAQPage) | quote form; 111 lawyers; filters | same as #10 | none |
| 14 | g8p-doron | Q2 #3 + AIO reference | doron-aharoni.com/שכר-טרחת-עורך-דין-במכירת-דירה-ברכישה/ | שכר טרחת עורך דין במכירת דירה וברכישת דירה 2026 | שכר טרחת עורך דין במכירת דירה / ברכישת דירה מעודכן לשנת 2026 | 1,816 | 0/7 (+H4) | 0 (lists) | 3 | 6 visible (no FAQPage) | form with deal-type select (sale / purchase / gift / inheritance / urban renewal); WhatsApp; Kfar Saba + TA phones | BlogPosting, BreadcrumbList, ImageObject, ListItem, Organization, Person, WebPage, WebSite | 2026-10-12 (pub 2026-03-26) |
| 15 | g8p-otmazgin | Q2 #4 | otmazgin-law.com/עורך-דין-קניית-דירה/עורך-דין-קניית-דירה-מקבלן-מהו-תפקידו/ | עורך דין קניית דירה מקבלן - מהו תפקידו? - עו"ד מיטל אוטמזגין | עורך דין קניית דירה מקבלן – מהו תפקידו? | 1,036 | 6/6 | 0 | 20 | none | contact forms | BreadcrumbList, EntryPoint, ImageObject, ListItem, Organization, PropertyValueSpecification, ReadAction, SearchAction, WebPage, WebSite | 2022-06-15 (pub 2022-04-01) |
| 16 | g8p-ericyanai | Q2 #5 | ericyanai.co.il/lawyer-buying-apartment/ | עורך דין קניית דירה - פועלו וחשיבותו לרכישת דירה בשנת 2023 \| משרד עורכי דין אריק ינאי | none (title text not tagged) | 3,395 | 3/27 | 0 | 9 | none | forms; audio narration (m4a) | BreadcrumbList, EntryPoint, ImageObject, ListItem, Organization, ReadAction, SearchAction, WebPage, WebSite | 2024-01-24 (pub 2022-10-31) |
| 17 | g8p-kolzchut-cap | Q2 AIO reference (not organic) | kolzchut.org.il/he/הגבלה_על_גובה_שכר_הטרחה_שמותר_לקבלן_... | הגבלה על גובה שכר הטרחה שמותר לקבלן לדרוש מהקונה לשלם לעורך דין מטעמו עבור רישום הזכויות בדירה (זכות) – כל-זכות | same | 876 | 7/4 | 1 (gov hotlines) | 0 | none | "did this help", suggest edit | none | text "updated 3.2.2026" |
| 18 | g8p-midrag-tip5795 | Q2 AIO reference (not organic; a midrag search URL is Q2 #19) | midrag.co.il/Content/Tip/5795 | עורך דין לקניית דירה \| המלצות על עורך דין לקניית דירה במידרג | עורך דין לקניית דירה | 2,009 (body ≈1,061) | 9/0 | 0 | 148 | 3 visible / 2 in FAQPage ✓ | rated lawyer list (e.g. 9.99 / 202 reviews), city selector, video answer, ~90 related article links | Answer, Article, FAQPage, ImageObject, Organization, Question | 2023-04-10 (pub 2022-11-17) |
| 19 | g8p-amitvered | Q2 #6 | amitvered.co.il/קניית-דירה/ | קניית דירה - המדריך המלא לרכישת דירה (2026) \| עמית ורד, עו"ד | קניית / רכישת דירה | 17,820 | 2/20 (+many H4/H5; 14-chapter TOC) | 0 | 11 | 5 (FAQPage ✓) | contact, newsletter, links to purchase-tax / CGT / payment-schedule guides | Answer, Attorney, FAQPage, GeoCoordinates, OpeningHoursSpecification, PostalAddress, Question | 2026-01-01 |
| 20 | g8p-yonilevy-buy | Q2 #12 | yonilevy.co.il/עורך-דין-נדלן/עורך-דין-קניית-דירה/ | עורך דין לקניית דירה \| 150 בדיקות לפני שחותמים \| יוני לוי | עורך דין קניית דירה | 4,184 | 13/18 | 0 | 134 | 8 visible / 1 in FAQPage | forms, WhatsApp group + deal-tracking system pitch, Trustindex Google reviews (111; footer 5.0/137), "150-check protocol", 7 case stories, media clips | Answer, Article, BreadcrumbList, EntryPoint, FAQPage, GeoCoordinates, ImageObject, LegalService, ListItem, Organization, Person, PostalAddress | 2026-09-06 (pub 2026-07-08) |
| 21 | g8en-strn | EN #2 + AIO reference + AIO firm card ("5.0 (21)") | strn.co.il/practice/real-estate-attorney-israel/ | Real Estate Lawyer in Israel \| Sternberg & Co. Advocates | Real Estate Lawyer in Israel for Property Matters and Strategic Representation | 2,342 | 19/13 | 1 (costs) | 15 | FAQPage ✓ but the only Q is a placeholder: "Why do we need? (test)" | inquiry form (reply in 24h) | Answer, BreadcrumbList, EntryPoint, FAQPage, ImageObject, ListItem, Organization, PropertyValueSpecification, QuantitativeValue, Question, ReadAction, SearchAction | 2026-09-27 (pub 2025-03-12) |
| 22 | g8en-gornitzky | EN #1 + AIO reference + AIO card ("4.6 (56)") | gornitzky.com/practices/real-estate-construction/ | Real Estate Law in Israel \| Gornitzky & Co | REAL ESTATE & CONSTRUCTION | 1,805 | 5/65 (news items) | 0 | 141 | none | newsletter | BreadcrumbList, EntryPoint, ImageObject, ListItem, Organization, PropertyValueSpecification, ReadAction, SearchAction, WebPage, WebSite | 2025-11-02 (pub 2018-04-17) |
| 23 | g8en-aharoni | EN #3; local pack ("Aharoni Law Firm - Israeli Lawyer") | aharonilaw.com/practice-area/israeli-real-estate-law/ | Israeli Real Estate Lawyer \| Real Estate Law in Israel | Israeli Real Estate Lawyer (+ stray H1 "connect") | 2,081 | 18/10 | 0 | 10 | none (3 FAQ links in footer) | contact form, "free consultation", US + IL phones | BreadcrumbList, ListItem, SiteNavigationElement | none |

### 1b. Exact-phrase placement, why each page ranks, weak spots

| Name | "עורך דין מקרקעין" (title / H1 / 1st paragraph / count) | "עורך דין קניית דירה" (title / H1 / count) | Why it ranks | Weak spots |
|---|---|---|---|---|
| g8-lawfind | no / no ("נדל"ן") / no / 6 (teasers) | 0 | old category directory; big internal article hub ("כיצד לבחור עורך דין מקרקעין", "שכר טירחה בחוזה נדל"ן"); directory intent | outdated (2008 eviction rules, the "until end of 2013" CGT cooling period, 2010 rulings); only 3 lawyers, one of them criminal/traffic; no fees; no dates; http only |
| g8-midrag-99 | yes (start) / yes / plural "עורכי דין מקרקעין" / 5 | 0 | review-platform brand; 5,451 reviews; exact title and H1 | almost empty: 2 sub-service links, no lawyers, no guidance, no fees |
| g8-dcoil | SERP title yes; captured no / H1 "דיני מקרקעין" / no / 2 (nav) | 0 | Zap / Golden Pages authority; city × category pages (5 d.co.il URLs in Q1 D top 19); local intent | captured page is a "no results" page with no content (unclear why) |
| g8-carish | SERP title yes (start) / unclear / unclear / unclear | unclear | exact-match slug and title; the "all lawyers, all prices" promise matches fee intent | unclear (not readable) |
| g8-cohenlawyers | no / no (H1 = phone) / no / 2 (body + tag) | 1 (tag) | unclear; covers 15 deal types (buy/sell, lease, receiver, developer, gift, divorce, registration, TAMA 38, opinions, management, condo order, co-ownership, combination, litigation) | Wix "blank-2" URL; H1 is a phone number; list numbering skips 13; typos; no date, fees or FAQ |
| g8-irelaw | yes (start) / no ("למקרקעין") / no / 1 (FAQ) | 0 | exact-match title; fresh; FAQ + AggregateRating schema; 48 internal guides; foreign-buyer / remote angle | translated feel (French origin: "4,9", "Ella", "Version texte pour IA"); claims "transparent fees" but gives no number; unverifiable "40 years / 1,000+ deals"; self-served AggregateRating |
| g8-yonilevy (TA) | plural in title and H1; singular in a body link (2nd section) / 5 | 0 | local modifier (Tel Aviv); brand entity (named in the AIO, and hakoach carries promo posts about him); strong Google reviews | thin "3 tips" page; dated 2023; outlier fee claim (1%–2% or more); self-promotion |
| g8-psakdin | no / no / no / 0 (uses "נדל"ן", "דיני מקרקעין") | 0 | legal-portal authority (case-law database); directory | no exact phrase; listed lawyers are mostly generalists (family, criminal, injury); thin intro; no fees |
| g8-hakoach | yes / yes / meta "עו"ד יוני לוי" / 79 (category labels) | 1 | exact-match category; freshness (posts through July 2026); keyword density | promotional posts for named lawyers (Yoni Levy, Oshar Elkayam, Haim Partouche, Yakir Dabul, Arbel, Shmuel Avraham) with no sponsor disclosure found in the HTML; off-topic posts (Cyprus, US, offices, mold); no original guidance |
| g8-lawreviews (RE) | yes (start, "מומלץ") / plural / no / 50 (card labels) | 0 | verified reviews + quote form + long SEO block; the AIO cites it as "the comparison platform" | no fee figures; FAQ not marked up; claims reporting and payment are both "within 60 days" (contradicts 30-day reporting); one "real-estate" card is an insolvency lawyer (Rafael Meir) |
| g8-gelberg | yes (start) / no / no / 9 | 2 (service H3) | entity: GBP + reviews + credential schema; lawyer and appraiser double license; 25-question FAQ incl. fees; fresh; the AIO uses it for "how to choose" | no FAQPage markup; reviews carousel repeated 3× in HTML; fee claims have no source; the full privacy-policy text sits in the page HTML (probably a modal) |
| g8p-addalaw | 4 (body only) | yes (title start) / yes (H1 start) / 1st paragraph no / 46 | exact match + extreme depth (16k words) + fresh + fee table + FAQ schema + statute citations (ss. 73(ג), 15(ב), 15(ד), s.324, s.7(א)) | structure, tips and anecdotes closely mirror amitvered (same TOC order, same kindergarten/antenna story, same 1,500–2,000 ₪ inspection, same 13–14 ₪ bank check), so it reads as derivative; its registry fees differ from amitvered (146/183 vs 150/188); bracket validity "until 15.01.2028" vs amitvered "until 15.01.2026"; delay-compensation tiers look wrong (see §3); broken FAQ sentence "נע בין 0.5% + מע"מ" |
| g8p-lawreviews-buy | 17 (labels) | yes (title start) / plural / 12 | directory + reviews + long step-by-step guide | generic; the 0.5%–1.5% fee has no source; the dual-representation answer is vague and cites no rule number; first card is labelled "עורך דין צוואה וירושה"; undated |
| g8p-doron | 3 | 0 (owns fee intent; year "2026" in title) | fee intent; freshness (mod 12.10.2026); 2026 registry fee list; the AIO cites it for the fee answer | link text gives developer-lawyer cap as "5,000 ₪" (outdated; Kol Zchut has 5,915 ₪ for 2026); several registry fees have no source (e.g. "רישום מכר/חכירה 43 ₪"); no table; no FAQPage |
| g8p-otmazgin | 0 | as part of "...מקבלן" in title and H1 / 6 | exact slug folder /עורך-דין-קניית-דירה/; developer subtopic | old (2022); thin; **wrong**: says the law requires a legal professional present at signing; unsourced "the developer's firm is legally required to state it doesn't represent buyers" |
| g8p-ericyanai | 2 | yes (title start) / no H1 / 5 | exact title; long checklist of checks; legacy page | "2023" in title; outdated purchase-tax brackets (1,805,545…); labels "8% up to 5,525,070 ₪" as "(פטור ממס רכישה)" (error); ILA lease "usually 49 years" is only partly right |
| g8p-kolzchut-cap | 0 | 0 | official-rights authority; exact cap numbers; the AIO cites it | the worked example uses the 2024 cap (5,575.06 ₪) on a page updated for 2026; no year given for the 4,642,750 ₪ price ceiling |
| g8p-midrag-tip5795 | 39 (labels/links) | "לקניית" (with ל) in title and H1 / exact 0 | brand + reviews + FAQ schema; the AIO uses it for "where to find recommendations" | thin; 2023; inaccurate tip (verify owner of unregistered flat via the Pledges Registrar); its only fee claim is "0.5%" |
| g8p-amitvered | 3 | not in title or H1 / 15 | deepest original guide (14 chapters, ~40 sub-steps); statute quotes (Land Law ss. 7(א), 8; Municipalities Ordinance s.324); year in title; Attorney schema | brackets "valid until 15.01.2026" (stale at crawl); uses "תקנות השוק" for warning-note protection (looks wrong, see §3); thin on fees; no tables |
| g8p-yonilevy-buy | 0 | title "לקניית" / H1 exact / 6 | exact H1; fresh; unique "150 checks" hook; reviews; brand entity | heavy self-promotion; same "check 14 / 150,000 ₪ off" story told once about a storeroom and once about parking; no fee figure (only disparages "0.2%" lawyers); FAQPage marks 1 of 8 questions; says it does no planning or engineering checks |
| g8en-strn | n/a ("real estate lawyer" ×20, "...in Israel" ×12) | n/a | EN exact match ×12; costs table; AIO cites it for fees and services; GBP card | placeholder FAQ in schema ("Why do we need? (test)"); "93% state-owned" with no source; registration fees "1,500–2,500 NIS + VAT" don't match official fee amounts |
| g8en-gornitzky | n/a (0 exact) | n/a | tier-1 firm brand; Chambers / Legal 500 quotes; deal news | no consumer content, fees or process; H1 not keyword-led |
| g8en-aharoni | n/a ("real estate lawyer" ×5) | n/a | EN title match; olim / North-America angle; local pack | outdated tax figures (exempt to 1.7M; 10% above 17.3M); **wrong** "purchase tax within 60 days of moving to the country"; poses fee questions but gives no fee numbers |

---

## 2. Published fees

### 2a. Lawyer fee figures (as stated; not averaged)

| # | Figure (exact) | Unit / basis | Party / deal type | Page | Page date |
|---|---|---|---|---|---|
| 1 | ~0.5% + VAT ("כ-0.5% + מע"מ משווי הנכס"); lower for expensive property, higher for very cheap property | % of property value, before VAT | buyer and seller; second-hand and from a developer ("בטווח דומה") | g8p-doron | mod 2026-10-12 ("נכון לשנת 2026") |
| 2 | fixed fee regardless of value (no amount given) | flat | gift between relatives (העברה ללא תמורה), inheritance registration incl. estate-distribution agreement | g8p-doron | 2026-10-12 |
| 3 | developer may charge its own lawyer's fee separately from your lawyer; article link text: "הגבלת שכ"ט עו"ד הקבלן ל-5,000 ₪" | ₪ cap (as quoted) | buyer from developer | g8p-doron | 2026-10-12. **Outdated vs Kol Zchut 5,915 ₪** |
| 4 | % is before VAT; VAT added ("בהצעות של משרדנו שכר הטרחה מצוין בתוספת מע"מ"); payment dates set in the fee offer/agreement; taxes and registry fees paid separately; excludes physical/engineering inspection and post-signing litigation | n/a | all | g8p-doron | 2026-10-12 |
| 5 | ~0.5% of deal price + VAT, **minimum ~5,000–6,000 ₪ + VAT** | % + min ₪ | buyer | g8p-addalaw | mod 2026-07-02 |
| 6 | second-hand up to 2,500,000 ₪: **5,000–12,500 ₪ + VAT** | ₪ range | buyer, 2nd-hand | g8p-addalaw | 2026-07-02 |
| 7 | second-hand 2,500,000–5,000,000 ₪: **12,500–25,000 ₪ + VAT** | ₪ range | buyer, 2nd-hand | g8p-addalaw | 2026-07-02 |
| 8 | from developer: **5,000–15,000 ₪ + VAT** ("לעיתים כולל מע"מ") | ₪ range | buyer, new from developer | g8p-addalaw | 2026-07-02 |
| 9 | complex deals (פינוי-בינוי, קבוצת רכישה, נכס מסחרי): "higher, set by complexity" | no number | urban renewal / group purchase / commercial | g8p-addalaw | 2026-07-02 |
| 10 | price drivers listed: not in Tabu (ILA/housing co.), building violations, liens, several sellers (inheritance/partnership), complex tax (foreign resident, several properties, CGT exemption), urgent timeline | qualitative | buyer | g8p-addalaw | 2026-07-02 |
| 11 | own-office FAQ: "נע בין 0.5% + מע"מ משווי העסקה, הכולל ליווי מלא עד רישום העסקה" (sentence is broken) | % | buyer | g8p-addalaw | 2026-07-02 |
| 12 | note: table upper bounds = exactly 0.5% of the bracket limits (12,500 = 0.5%×2.5M; 25,000 = 0.5%×5M); lower bound = the stated minimum | derived observation | n/a | g8p-addalaw | n/a |
| 13 | average ~0.5% + VAT; "ניתן למצוא עורך דין בסכום מוזל משמעותית" | % | buyer, 2nd-hand | g8p-amitvered | mod 2026-01-01 |
| 14 | 0.5%–1.5% of value + VAT; sometimes a global sum; "not fixed by law" | % range | buyer | g8p-lawreviews-buy | undated |
| 15 | one-time consultation ~500 ₪; with document review up to 1,000 ₪ and more | ₪ | consult | g8-gelberg | mod 2026-09-22 |
| 16 | buy or sell deal: between 0.5% and 1% of value | % range | buyer / seller | g8-gelberg | 2026-09-22 |
| 17 | sale: accepted range 0.25%–1%; "usually 0.5%"; plus expenses (Tabu fees, MoJ fees, document delivery, municipal fees) | % range | seller | g8-gelberg | 2026-09-22 |
| 18 | "בקנייה של דירה יד שנייה נהוג לקחת חצי אחוז" (recommendation only) | % | buyer, 2nd-hand | g8p-midrag-tip5795 | 2023-04-10 |
| 19 | ~0.5% for high-value deals, up to ~2% for low-value deals, + VAT; "paid at signing; amount and timing are up to the parties" | % range | buyer | g8p-ericyanai | 2024-01-24 (title says 2023) |
| 20 | Tel Aviv sale-deal accompaniment "starts at 1% and can reach 2% or more"; models: fixed, hourly, or mixed | % range | sale deal, Tel Aviv | g8-yonilevy (TA) | 2023-10-18 |
| 21 | "עורך דין ב-0.2% לרוב לא יבצע אפילו 10% מהבדיקות שלנו" (implies cheap market offers of ~0.2%) | % (implied low end) | buyer | g8p-yonilevy-buy | 2026-09-06 |
| 22 | "same rate for purchase and sale", "no minimum threshold, no hidden clauses", written quote after review; no number | none | buyer / seller | g8-irelaw | 2026-07-29 |
| 23 | fees "can reach tens of thousands of shekels"; "no uniform price or fixed %" (teaser) | qualitative | all | g8-lawfind | undated (old) |
| 24 | tenants' lawyer in TAMA 38 / pinui-binui is "usually paid by the developer" but owes loyalty to tenants only | who pays | urban renewal | g8-lawreviews (RE) | undated |
| 25 | developer's lawyer is paid by the buyer "within the legal expenses limited by law" (no figure) | n/a | developer purchase | g8-lawreviews (RE) | undated |
| 26 | AIO (Q2): second-hand "לרוב עומד על כ-0.5% משווי עסקת המקרקעין בתוספת מע"מ" | % | buyer, 2nd-hand | Google AIO (refs: doron, midrag tip, adicohen-law, kolzchut) | 2026-10-26 |
| 27 | AIO (EN): "often around 0.5% to 1.5% plus VAT, or a fixed flat fee" | % range | buyer | Google AIO (element ref: strn; **figure not on captured strn page**, same as lawreviews-buy HE wording) | 2026-10-26 |
| 28 | strn: "transparent pricing", no lawyer figure | none | all | g8en-strn | 2026-09-27 |
| 29 | aharoni: asks "What are the legal fees?" without answering | none | all | g8en-aharoni | undated |

### 2b. Developer's-lawyer cap (תקנות המכר (דירות) (הגבלת גובה ההוצאות המשפטיות); חוק המכר (דירות) s.6ג)

| Item | Figure | Source / date |
|---|---|---|
| Who it covers | developer's lawyer representing seller **and** buyer (buyer's consent, usually in the contract) for registration only: managing the rights list, registration at Land Registry incl. condo registration / amending the condo order, other registration expenses | kolzchut (updated 3.2.2026) |
| List management until registration | **300 ₪** max ("החל מ-2007, בהתאם לצו הפיקוח על מחירי מצרכים ושירותים") | kolzchut |
| Other registration legal expenses: lower of fixed sum or 0.5% | **5,915 ₪ (2026)**; **5,770.77 ₪ (2025)**; **5,575.06 ₪ (2024)**; or **0.5% of the contract price**; whichever is lower, **before VAT** | kolzchut |
| Price ceiling | cap applies if price ≤ **4,642,750 ₪**; above it "החוק לא מגביל" (no cap). Year of the ceiling not stated | kolzchut |
| Worked example | 4,000,000 ₪ → 0.5% = 20,000 > cap → max **5,575.06 ₪ + VAT** (uses the 2024 figure); 5M ₪ → no limit | kolzchut (example not updated) |
| Payment mechanics | pay the lawyer directly (not through the seller); lawyer must issue a tax invoice; buyer may hire a separate lawyer and pay them separately | kolzchut |
| AIO wording | "הסכום הנמוך מביניהם: כ-5,915 ש"ח + מע"מ או 0.5% ממחיר הדירה (נכון לשנת 2026; לא חל על דירות יוקרה מעל סכום מסוים)" | Google AIO Q2, 2026-10-26 (refs doron, midrag tip, adicohen-law, kolzchut; only kolzchut contains 5,915) |
| Stale figure in the wild | "5,000 ₪" | g8p-doron (link text) |
| Housing-company list fee (likely the same 300 ₪ cap) | "אגרה עבור מכר בחברה המשכנת – 300 ₪ + מע"מ" | g8p-doron (2026) |

### 2c. Other deal costs quoted next to lawyer fees (for the fee data file)

| Item | Figure | Page (date) |
|---|---|---|
| Home inspection (בדק בית) | ~1,500–2,000 ₪ | addalaw (2026-07-02); amitvered (2026-01-01) |
| Bank check for deposit | ~13–14 ₪ | addalaw; amitvered |
| Total side costs | "יכולות להגיע ל-15% ואף יותר ממחיר הדירה" | amitvered |
| Safety margin in budget | at least 5% | addalaw; amitvered |
| Agent fee | 1.5%–2% + VAT | strn (EN); AIO EN |
| Appraiser / engineer | 3,000–7,000 NIS + VAT | strn (EN); AIO EN |
| "Registration fees" | 1,500–2,500 NIS + VAT (doesn't match the official registry fees in §3; may include handling; unclear) | strn (EN); AIO EN |
| Municipal certificate fee | 100–200 ₪ | amitvered |

### 2d. Not found on any captured page
- **Bar Association recommended minimum tariff (התעריף המינימלי המומלץ)**: no page mentions it, so its status (in force or cancelled) isn't available from these files. Demand exists: the related search "תקנות שכר טרחה עורך דין".
- **Official tariff**: the only official limit cited is the developer's-lawyer cap above.
- **Fee figures for combination deals, land / agricultural land, urban renewal (owner side), group purchase**: none (addalaw only says "higher").
- **Inheritance / gift fee amounts**: none (doron only says "fixed").
- **When fees are paid**: ericyanai "at signing"; doron "per fee agreement"; addalaw links an article ("מתי משלמים לעורך דין בקניית דירה") but gives no rule. Related search "מתי משלמים לעורך דין קניית דירה" confirms demand.

---

## 3. Facts stated (claim, Hebrew key words, pages, flags)

### 3.1 Purchase steps (order as stated)
| Claim | Key words | Pages | Flags |
|---|---|---|---|
| Pre-contract stage covers 3 aspects: legal, engineering/planning, economic | השלב הטרום חוזי; היבטים משפטיים / הנדסיים ותכנוניים / כלכליים | amitvered, addalaw | addalaw mirrors amitvered |
| Steps: define needs → search → mortgage approval in principle → negotiate → sign → deposit → get apartment | הגדרת הצרכים; אישור עקרוני; מקדמה | gelberg (about block); gelberg FAQ adds "registration at Tabu or housing company" | – |
| Steps: locate and negotiate → (avoid memo) → negotiate and draft → sign + report within 30 days → mortgage → payments + warning note → seller obligations → possession (protocol) → registration | – | lawreviews-buy | – |
| Full chain: checks → memo (avoid) → payment schedule → signing (contract, ancillary docs, deposit) → warning note → tax report and purchase tax → CGT advance → mortgage → remove seller mortgage → municipal certificate → tax approvals → mortgage deeds → possession (physical vs legal) → registration | הערה על מכר; מקדמה על חשבון מס שבח; אישור עירייה; שטרי משכנתה; חזקה משפטית | amitvered, addalaw | – |
| Firm steps: negotiation, legal checks, contract, signing, tax reports, warning note, transfer at Tabu | – | cohenlawyers | – |
| 3-step office process: confidential call → checks and file opening (POA for remote) → signing and Tabu registration | – | irelaw | – |
| Seller-side: checks (Tabu, building rights, municipal debts, betterment levy) → find buyer → negotiate → contract → transfer (+ CGT) | – | gelberg | – |
| Developer purchase: contract review, "נספח שינויים" (amendments annex), delivery date, voucher-book payments, changes during construction | נספח שינויים; פנקס שוברים | otmazgin | – |
| Developer's order form (טופס הזמנה) is a binding document; consult before signing it | טופס הזמנה | addalaw | no source given |

### 3.2 Memorandum of understanding (זיכרון דברים)
| Claim | Pages | Flags |
|---|---|---|
| Binding if it contains essentials (parties, property, price, payment and delivery dates) and shows intent; content counts, not the title | gelberg, lawreviews RE, lawreviews-buy, addalaw, amitvered, irelaw, strn (EN "may carry binding effect") | consistent |
| Land Law s.8 requires writing; contract law requires גמירות דעת + מסוימות; a court may fill missing terms; an unsigned memo can bind through conduct | amitvered (cites s.8), addalaw (no section number) | – |
| Memo date may be the "determining date" for reporting (30 days) and purchase-tax payment (60 days) | amitvered, addalaw | – |
| If one must sign: make it conditional on a contract within a set time, auto-cancel without compensation; seller should bar warning-note registration under the memo | amitvered, addalaw | – |
| Cancelling a memo can cost liquidated damages "usually 10% of the deal value" | lawreviews RE | – |
| Recommendation: don't sign without a lawyer / at all | all guides; irelaw review anecdote | – |

### 3.3 Due diligence and documents
| Claim | Key words | Pages | Flags |
|---|---|---|---|
| Tabu extract online in minutes; fee **18 ₪ (2026)** | נסח טאבו | amitvered | **contradiction**: doron 17 ₪ (2026); addalaw "low fee" |
| Find גוש/חלקה via arnona bill, seller's contract, Mapi (המרכז למיפוי ישראל), Tax Authority real-estate info, free | – | amitvered, addalaw | – |
| What the extract shows: registered at Tabu or not; separate sub-parcel vs "מושע"; ownership vs lease; full owner; how acquired; mortgage; notes / liens / orders | מושע; בעלות / חכירה | amitvered, addalaw | – |
| Unregistered flat: get a rights approval from ILA / housing company / החטיבה להתיישבות | אישור זכויות | amitvered, addalaw, ericyanai, lawreviews-buy | – |
| Housing company rights approval fee "אינו מוסדר בחוק" | – | ericyanai | **contradiction**: addalaw / amitvered cite the price-control order (150–500 ₪); kolzchut 300 ₪ list cap |
| Check the seller's marital status; a spouse or common-law partner may claim rights; banks require spouse consent | ידוע/ה בציבור; כתב ויתור והסכמה | amitvered, addalaw | – |
| Seller-identity fraud (forged ID, POA, inheritance papers, elderly victims); ask for 2nd ID and purchase history | עוקץ נדל"ן | amitvered, addalaw | – |
| Occupants: tenant contract end and options; licensee (בר-רשות) without a contract | – | amitvered, addalaw | – |
| Condo file online (צו רישום, תקנון, תשריט) **39 ₪ (2026), ~24 h** | תיק בית משותף | amitvered | **contradiction**: addalaw "modest fee, ~4 hours" |
| The תשריט (condo plan) is the binding plan for attached parking, storage, roof; banks' appraisers require it | הצמדות | amitvered, addalaw, ericyanai, midrag tip, yonilevy-buy | – |
| Building file: permit + "גרמושקה"; check both physical fit and approved use (a "דירה" in Tabu may be a storeroom or shelter in the permit); Form 4 | היתר בנייה; ייעוד; טופס 4 | amitvered, addalaw, ericyanai, irelaw, lawreviews-buy | – |
| Risky types: very old buildings; ground / basement / pilotis; roof units; commercial frontage; garden flats over common yard; changed openings; light construction; split flats | – | amitvered, addalaw | – |
| Building violations are criminal offences under the Planning and Building Law 1965 (fines, even prison; demolition orders); can block a mortgage and the municipal certificate; can hurt purchase-tax relief and future CGT exemption | חריגות בנייה | amitvered, addalaw, lawreviews RE, lawreviews-buy, midrag tip | – |
| Duty to restore building violations "falls on the new owner, not the seller" | – | ericyanai | oversimplified, no source |
| Lawyer checks permit and use; physical fit needs an appraiser / engineer / surveyor | – | amitvered, addalaw, yonilevy-buy ("we don't do planning or engineering checks; get a pre-appraisal") | – |
| Lost permit files in old buildings: get a written municipal "not found" note for the bank appraiser | – | amitvered, addalaw | – |
| Check the Pledges Registry (רשם המשכונות) and Companies Registry for hidden liens | – | addalaw; ericyanai; yonilevy-buy (case 4) | – |
| "For apartments not registered in Tabu, check the owner via the Pledges Registrar" | – | midrag tip | **looks wrong / incomplete**: other pages say ownership comes from the ILA / housing-company rights approval; the Pledges Registry shows liens |
| Municipal debts are not necessarily on the Tabu extract; ask the municipality (needs seller POA) | – | ericyanai, lawreviews-buy, yonilevy-buy | – |
| Price check: Tax Authority public deals database | מאגר מידע נדל"ן | amitvered, addalaw | – |
| Inspection 1,500–2,000 ₪; thermal tools for hidden moisture | בדק בית | amitvered, addalaw | – |
| Known developers command a 5%–10% price premium in some cities | – | amitvered | no source |
| TABA check: designated uses nearby; future urban renewal | תב"ע | amitvered, addalaw, ericyanai | – |
| "150 checks" protocol (examples: #14 plan cross-check, #17 Pledges Registry, #22 ownership chain, #34 third-party rights, #39 municipal certificate, #142 house-committee debts) | נוהל 150 | yonilevy-buy | marketing; inconsistent anecdote |
| Lawfind definitions: lease over 5 years = חכירה; over 25 years = חכירה לדורות; the Land Registry is the only registration authority under the Land Law 1969 | – | lawfind | – |
| ILA lease "usually 49 years"; the ILA site issues rights approvals online | – | ericyanai | partly right (no other page confirms or contradicts) |
| Rights at ILA are usually leasehold, not full ownership; many properties are registered only at ILA | – | lawreviews RE | – |
| ILA consent fees (דמי הסכמה) are payable on lease transfer (no amount) | דמי ההסכמה | ericyanai | – |

### 3.4 Contract, payments, possession
| Claim | Pages | Flags |
|---|---|---|
| Signing usually at the seller's lawyer's office, 1–1.5 h; three parts: contract, ancillary documents, deposit | amitvered, addalaw | – |
| Deposit usually **10%–20%**, sometimes **30%–40%** | amitvered, addalaw | ericyanai: "around 20% at signing, or into the lawyer's trust" |
| Deposit check held in trust by seller's lawyer until the buyer's warning note is registered | amitvered, addalaw, ericyanai | – |
| Liquidated damages for fundamental breach **10%**; daily delay compensation; grace for late payment **7–14 days** | amitvered (10%, 7–14 d), addalaw ("~10%") | – |
| Recommended clauses: seller signs bank documents within ~5 business days; insurance until possession; force majeure (Tabu strikes, war); spouse consent; tax deposit in trust | amitvered, addalaw | – |
| Contract annexes: Tabu extract / rights approval; payoff letter / intent letter; plans; original developer contract; lease; inheritance order / probate | amitvered, addalaw, ericyanai | – |
| Ancillary docs: warning-note request (both); irrevocable POA for registration (sellers); POA to delete the note on buyer breach (buyers); sale deeds (שטרי מכר); transfer forms per registry | amitvered, addalaw, ericyanai, lawreviews-buy | – |
| Sale deed signed before a lawyer or the registrar for identification | ericyanai | – |
| Tax deposit (פיקדון מסים) in trust if CGT / municipal / property-tax approvals are missing at possession; should be sized to "maximum exposure" | amitvered, addalaw, yonilevy-buy, lawreviews-buy | – |
| Physical vs legal possession (rented flat: buyer steps into lease, receives checks and guarantees) | amitvered, addalaw | – |
| Possession protocol, meter readings (electricity via 103, water / arnona, gas deposit), house-committee no-debt letter | amitvered, addalaw, lawreviews-buy, ericyanai | – |

### 3.5 Warning note (הערת אזהרה) and registry fees (אגרות)
| Claim | Figures | Pages | Flags |
|---|---|---|---|
| Purpose: blocks a conflicting deal; two circles of protection (internal at the registry, external via public notice); banks require it | – | amitvered, addalaw, lawreviews RE, lawreviews-buy, ericyanai, lawfind, midrag tip | – |
| Interim protection called "תקנות השוק" | – | amitvered | **looks wrong**: lawfind ties "תקנת השוק" to Land Law s.10 (a different doctrine) |
| Online warning note through the MoJ representatives system, 1–2 working days | **146 ₪ (2026)** | addalaw; doron (146 ₪ online) | **contradiction**: amitvered **150 ₪ (2026)** |
| Manual warning note at the Tabu office, done on the spot | **183 ₪ (2026)** | addalaw | **contradiction**: amitvered **188 ₪ (2026)** |
| Warning note at ILA: usually free; at housing company: **150–500 ₪** (price-control order התש"ס-1999); some add **350 ₪** handling | – | amitvered, addalaw | – |
| ILA / housing company: **7–14 days** or more | – | amitvered, addalaw | – |
| Pledge (משכון) at the Pledges Registry for buyer protection when rights sit with a housing company | **38–190 ₪** by duration | amitvered, addalaw | **contradiction**: doron **215 ₪** (online, 5+ years) |
| Other 2026 fees | Tabu extract 17 ₪; sale/lease registration 43 ₪; mortgage registration 183 ₪; warning note for buyer's bank 146 ₪ online; co-ownership agreement 183 ₪; inheritance / will / estate agreement 183 ₪; delete warning note 99 ₪; housing-company sale fee 300 ₪ + VAT; municipal certificate per municipality | doron | figures have no source; "43 ₪ sale registration" looks low (unverified) |
| Online warning notes recently launched by the registry | – | ericyanai | dated phrasing |

### 3.6 Tax Authority reporting and taxes
| Claim | Figures | Pages | Flags |
|---|---|---|---|
| Buyer must report within **30 days** of signing (s.73(ג) Land Taxation Law) | 30 d | addalaw, amitvered, lawreviews-buy | **contradiction**: lawreviews RE says "report and pay within 60 days" |
| Purchase tax payment within **60 days** of the deal | 60 d | addalaw (body + FAQ), amitvered, lawreviews RE | aharoni EN: "within 60 days of moving to the country" (**wrong**) |
| Difference after the Tax Authority's assessment: pay within 30 days; late penalty **0.2% per week** + linkage + interest | 0.2%/wk | amitvered; addalaw (0.2%/wk) | – |
| Represented buyers can report online only (smart card, representatives system); "הצהרה על נכונות הפרטים" form; **Form 7000א** for several buyers not in the same family unit | – | amitvered, addalaw | – |
| Purchase-tax brackets, single apartment: 0% to **1,978,745**; 3.5% to **2,347,040**; 5% to **6,055,070**; 8% to **20,183,565**; 10% above | ₪ | amitvered ("valid until 15.01.2026"), addalaw ("as of Jan 2026 … valid until 15.01.2028") | **contradiction on validity**: same numbers, different validity date |
| Additional apartment: 8% to **6,055,070**; 10% above | ₪ | amitvered, addalaw | – |
| Old brackets: 0% to 1,805,545; 3.5% to 2,141,605; 5% to 5,525,070; 8% to 18,416,900; 10% above; additional 8% to 5,525,070 "(פטור ממס רכישה)" | ₪ | ericyanai | **outdated** + label error |
| "Exempt up to 1.7 million; 3.5–10%; above 17.3 million 10%"; "rates change every January" | ₪ | aharoni EN | **outdated** |
| Family unit: spouses + minor children = one buyer | התא המשפחתי | amitvered, addalaw | – |
| Partial rights up to 1/3 (or 1/2 of an inherited flat) don't count as "another apartment" | – | amitvered | addalaw words it as "less than one third"; minor wording difference |
| Reliefs: disabled categories, olim, bereaved families, terror victims' families | – | amitvered, lawreviews-buy | – |
| Purchase tax between relatives: 1/3 rate (regulation 20) | – | lawfind (teaser) | old source; unverified |
| CGT advance: buyer pays **7.5% or 15%** of consideration (by original purchase date) under s.15(ב); deemed paid by seller (s.15(ד)); stamped voucher = CGT approval for registration; not required for an exempt qualifying apartment or non-cash consideration | 7.5% / 15% | amitvered, addalaw | – |
| Trigger: "after the buyer paid **40%** of the price" | 40% | amitvered, addalaw (same lineage) | **needs verification** against the statute; I recall a "more than 50%" trigger, but that isn't confirmed in these files |
| CGT single-apartment exemption s.49ב(2): individual owner; residential use 4 years (or 4/5 of the period); only apartment; no exempt sale in the prior **18 months**; exceptions (new flat bought, old sold within 18 months; inheritance) | 18 months | gelberg | gelberg media headline "משפרי דיור חוזרים ל-24 חודשים" (about the purchase-tax window for upgraders) adds 18/24-month confusion; unclear |
| CGT routes: full exemption, linear relief, full tax | – | amitvered, addalaw, lawreviews RE | – |
| CGT "typically about 25% of the net gain" | 25% | aharoni EN | – |
| Old rule: 18-month cooling period until end of 2013, "no longer needed" | – | lawfind (teaser) | outdated framing |
| Betterment levy = **half** of the value increase from a planning decision (plan, הקלה, שימוש חורג); Third Schedule of the Planning and Building Law 1965; due on realization (sale or permit) | 50% | gelberg, amitvered, addalaw | – |
| Betterment exemptions: residential expansion up to **140 m²** (conditions); accessibility service areas; ממ"ד | 140 m² | amitvered, addalaw | – |
| Who pays betterment: custom is seller for plans approved before signing, buyer after | – | ericyanai, lawreviews-buy ("לרוב ... על המוכר עד למועד חתימת ההסכם"), amitvered ("כמעט תמיד על המוכרים"), lawfind ("ניתן לקבוע בחוזה על הקונה") | contract-dependent |
| Property-tax (מס רכוש) clearance needed if no voluntary transaction after **31.12.1999** | date | amitvered | – |

### 3.7 Municipal certificate, mortgage, registration
| Claim | Figures | Pages | Flags |
|---|---|---|---|
| Municipalities Ordinance **s.324**: no transfer is registered without a certificate that municipal debts are paid; covers arnona + betterment (+ development levies) | – | amitvered (quotes the text), addalaw | – |
| Certificate takes up to **30 days**; **3–4 months** where betterment is possible (roof units, villas); inspection possible; some small councils split it (council + planning committee) | 30 d / 3–4 mo | amitvered, addalaw | – |
| Mortgage LTV caps (Bank of Israel): first apartment **75%**; single apartment (upgraders) **70%**; additional apartment **50%** | % | amitvered, addalaw (table) | – |
| Contracts usually say "no mortgage approval ≠ ground to cancel", so get approval in principle first | – | amitvered, addalaw, lawreviews-buy, gelberg | – |
| Bank documents (IDs, 3–6 months' statements, payslips, Form 106, insurance, bank-list appraiser, notarial POA, single/additional affidavit, tax-report copy) | – | amitvered, addalaw | – |
| Seller signs "כתב התחייבות לרישום משכנתה" → warning note in favor of buyer's bank | – | amitvered, addalaw, lawreviews-buy, doron | – |
| Seller's mortgage removal: transfer to another property (גרירה), freeze (הקפאה) or payoff (פירעון), against a bank intent letter (מכתב כוונות); pay the loan account directly, not the current account | – | amitvered, addalaw | – |
| Mortgage deeds take **7–10 business days** | – | amitvered ("7–10"); addalaw ("a week to ten working days") | – |
| Land Regulations (Management and Registration) 2011, reg. 14(ב): lawyer verifies mortgage-deed signatures | – | amitvered | – |
| Land Law **s.7(א)**: a transaction is completed by registration, at the moment the registrar approves it | – | amitvered (quote), addalaw | – |
| Three registries: Land Registry (Tabu), ILA, housing companies; registration takes days to weeks | – | amitvered, addalaw, lawreviews-buy | – |
| Unregistered rights are only "quasi-proprietary" (מעין קניינית) | – | lawreviews RE | – |
| Timelines: second-hand from contract to final registration **2–4 months** | – | lawreviews-buy | – |
| Deal is usually signed within **1–3 months** | – | irelaw | – |
| Final Tabu registration takes weeks to months after possession | – | lawreviews RE | – |

### 3.8 Sale Law guarantees and developer purchases
| Claim | Pages | Flags |
|---|---|---|
| חוק המכר (דירות), תשל"ג-1973: bank guarantees, defect liability, spec, warranty | addalaw | – |
| Every payment to the developer must be backed by a bank guarantee | addalaw | – |
| Security is "a bank guarantee or an insurance policy, until registration" | lawreviews-buy | – |
| Payments go through a voucher book (פנקס שוברים) to the accompanying bank's project account | otmazgin | – |
| Delay compensation after a **60-day** grace: up to 4 months ×1.0 rent; beyond 4 months ×1.25; beyond 10 months ×1.5 | addalaw | **looks wrong**: my recollection of the statute is ×1 up to 8 months, ×1.25 for 8–10 months, ×1.5 above 10; verify against the law |
| Developer's lawyer represents the developer only (focus on registration), even though the buyer pays them | lawreviews RE, lawreviews-buy, addalaw, otmazgin, kolzchut, AIO Q2 | consistent |
| Construction-input index linkage until delivery; developer-lawyer fee; development costs | addalaw (table) | – |
| **Nobody** names חוק המכר (דירות) (הבטחת השקעות של רוכשי דירות), התשל"ה-1974, the guarantee release timing, or warranty / בדק periods | – | gap |

### 3.9 Dual representation (one lawyer for both sides)
| Claim | Pages | Flags |
|---|---|---|
| "On the Bar's ethics rules a lawyer usually may not represent both sides in the same real-estate deal (potential conflict); each side should have its own lawyer" | lawreviews-buy | no rule number; **contradiction** with the next rows |
| Buyer and seller may agree on one lawyer to save money; not recommended | amitvered | – |
| Someone representing both sides can't fully protect you; a broker-recommended lawyer is conflicted | addalaw, amitvered | – |
| A joint lawyer may not advise separately or prefer one party; own lawyer owes duty to buyer only | kolzchut (developer-registration context, with buyer consent) | – |
| Lawyer "representing both parties" in a gift transfer between relatives | doron | – |
| **No page cites the Bar Association (Professional Ethics) Rules or a rule number** | – | gap |

### 3.10 Bar Association, profession, market facts
| Claim | Pages | Flags |
|---|---|---|
| Number of registered lawyers in Israel: **not stated anywhere** (PAA asks "כמה עורכי דין רשומים בישראל?") | – | gap |
| Memberships claimed: Bar property & real-estate forum, urban-renewal committee, real-estate tax committee | gelberg | self-claimed |
| "Member of the Israel Bar"; lawyer + notary | irelaw | – |
| Manual Tabu filing by courier needs the lawyer's Bar card copy | amitvered, addalaw | – |
| 93% of property state-owned, 7% private | strn EN | AIO EN: "over 90% publicly owned" (refs lawreviews EN, Wikipedia, kahn) |
| Caveat emptor ("ייזהר הקונה") puts due diligence on the buyer | lawreviews RE; AIO EN | – |
| Contracts drafted in Hebrew with translations | strn EN | – |
| Group purchase: 15–30 members, ~15% discount (120k–200k ₪) | lawfind (old teaser) | outdated, no source |
| Agricultural land "to be rezoned": Standard 22 appraisal is a must ("תקן ממשלתי") | lawreviews RE | wording: Standard 22 is an appraisers'-council standard; unverified |

### 3.11 Urban renewal (stated by gelberg; others briefly)
| Claim | Pages | Flags |
|---|---|---|
| TAMA 38 approved 2005 for buildings permitted before 1.1.1980; expired; replaced by "חלופת שקד" (Planning and Building Law amendment 139) and local plans; transition rules for earlier permit requests | gelberg | – |
| 38/1 = strengthening + additions; 38/2 = demolish and rebuild | gelberg | – |
| Strengthening Law 2008: **two-thirds (67%)** majority; Superintendent of Land Registration may approve over objections | gelberg | – |
| Pinui-binui law 2006: two-thirds can sue an unreasonable refuser | gelberg | – |
| Standard 21 (2012, updated) for economic feasibility | gelberg | – |
| Tenants' lawyer secures guarantees (Sale Law guarantee + rent guarantee), timelines, equal consideration | lawreviews RE | – |

### 3.12 Contradictions and suspect numbers (summary)
1. Reporting deadline: 30 days (addalaw, amitvered, lawreviews-buy) vs "report and pay within 60 days" (lawreviews RE).
2. Tabu extract: 17 ₪ (doron) vs 18 ₪ (amitvered), both "2026".
3. Warning note online: 146 ₪ (addalaw, doron) vs 150 ₪ (amitvered); manual 183 ₪ (addalaw) vs 188 ₪ (amitvered).
4. Pledge: 38–190 ₪ (amitvered, addalaw) vs 215 ₪ (doron).
5. Condo file turnaround: ~4 h (addalaw) vs ~24 h (amitvered).
6. Bracket validity: "until 15.01.2026" (amitvered) vs "until 15.01.2028" (addalaw), same numbers. Ericyanai and aharoni use old brackets.
7. Developer-lawyer cap: 5,915 ₪ (kolzchut, AIO) vs "5,000 ₪" (doron link text). Kolzchut's own example uses 5,575.06 (2024).
8. Housing-company fees: "not regulated by law" (ericyanai) vs price-control order caps (addalaw / amitvered / kolzchut).
9. Dual representation: "usually not allowed" (lawreviews-buy) vs "allowed with agreement / consent" (amitvered, kolzchut, doron).
10. Fee level: 0.5% mainstream (doron, addalaw, amitvered, midrag, AIO) vs 0.5–1% (gelberg), 0.5–1.5% (lawreviews-buy, AIO EN), up to 2% for small deals (ericyanai), 1–2%+ in Tel Aviv (yonilevy TA), 0.25–1% seller (gelberg).
11. Suspect: delay-compensation tiers (addalaw); "40%" CGT advance trigger (amitvered / addalaw); "תקנות השוק" (amitvered); signing requires a legal professional (otmazgin, wrong); purchase tax "60 days of moving to the country" (aharoni, wrong); "8% … (פטור)" label (ericyanai); EN "registration fees 1,500–2,500 NIS" (strn) vs official fees in the tens or hundreds of ₪.
12. AIO attribution: the AIO's 5,915 ₪ cites doron and midrag, whose captured pages don't contain 5,915 (only kolzchut does). The AIO EN "0.5%–1.5%" cites strn, whose page has no lawyer-fee figure.

---

## 4. Topics union (who covers what)
Codes: LF lawfind · MD midrag-99 · CO cohen · IR irelaw · YL yonilevy-TA · PS psakdin · HK hakoach · LR lawreviews-RE · GB gelberg · AD addalaw · LB lawreviews-buy · DA doron · OT otmazgin · EY ericyanai · KZ kolzchut · MT midrag-tip · AV amitvered · YB yonilevy-buy · ST strn · GO gornitzky · AH aharoni

| Subtopic | Covered by (depth) | Gap? |
|---|---|---|
| What a real-estate lawyer does (role) | GB, LR, LB, AD, AV, PS, CO, IR, MT, AIO; ST/AH (EN) | covered |
| Range of deal types / services | CO (15 types), GB, IR, PS, LF, YL, ST | – |
| When to hire (timing: before memo / before listing) | AD, AV, GB (seller: before listing), LB, YB, IR | – |
| Before a memorandum: risks and safe wording | AV, AD (deep), GB, LR, LB, IR, YB, ST | – |
| Second-hand vs new from developer | AD (table), LR, LB, AV (FAQ), OT, IR | thin on the developer side except AD/OT |
| Land / plot purchase | LR (FAQ: ownership, TABA, expropriation, levy, co-ownership), YL (mentions), HK (titles only), GB (review) | **weak**: no process, fees or agricultural-land detail |
| Combination deals | CO (definition), GB (definition), LF (teaser), LR (tax note), ST (EN) | **weak**: no process / fees |
| Group purchase | LB (risks; each member needs own lawyer), LF (old numbers), AD (fees "higher") | weak |
| Urban renewal (TAMA 38, pinui-binui) | GB (deep FAQ), LR, CO, PS, ST, cohen | covered for owners; no fee data |
| Inheritance / gift transfers | DA (fixed fee, tax planning), IR, CO, LF, YB (heirs case) | no amounts |
| Receiver (כונס) purchase | CO, MT (link), YB (link), ST (EN) | weak |
| Documents list (annexes, ancillary, bank, tax) | AV, AD (deep), EY, LB | covered |
| Red flags / risky property types | AV, AD, YB (cases), EY, MT | covered |
| Building violations and permits | AV, AD, EY, LB, LR, MT, YB | covered |
| Seller fraud / identity | AV, AD | – |
| Fees: level | DA, AD (table), AV, LB, GB, MT, EY, YL, AIO | covered, but no deal-type × price matrix except AD |
| Fees: what's included / excluded | DA (both), AD (included; comparison card) | – |
| Fees: what drives price | AD, DA | – |
| Fees: VAT treatment | DA (explicit), KZ (before VAT), AD, LB | – |
| Fees: when paid | EY, DA (vague) | **gap** |
| Developer's-lawyer cap | KZ (only full source), DA (outdated), LR (no number), AIO | **gap among law-firm pages** |
| Seller-side fee | GB, DA | – |
| How to choose a lawyer | GB, YL (3 tips), AD, AV, MT, HK (titles), LF (teaser), AIO | covered generically |
| Questions to ask a lawyer | HK (titles only), AD (fee-quote card), YB (FAQ style) | **gap**: no real question list |
| Verify a lawyer (Bar registry, license, complaints, malpractice insurance) | none | **gap** (PAA asks about complaints, insurance, number of lawyers) |
| Dual representation rules | LB, AV, AD, KZ, DA | **weak**: no rule numbers |
| Mistakes to avoid | AV/AD tips, YB cases, GB "traffic light" | – |
| Taxes: purchase tax (brackets, family unit, 1/3 rule) | AV, AD, EY (old), LB, IR, AH (old) | – |
| Taxes: CGT, betterment, CGT advance, property-tax clearance | GB, AV, AD, EY, DA | – |
| Tax reporting deadlines and penalties | AV, AD, LB, LR (contradiction) | – |
| Mortgage coordination (AIP, LTV, seller mortgage removal, bank docs, deeds) | AV, AD (deep), LB, IR, YB | covered |
| Warning note mechanics and fees | AV, AD, DA, LB, EY, LF | covered (with contradictions) |
| Municipal certificate (s.324) | AV, AD, YB | – |
| Registration (Tabu / ILA / housing co.) | AV, AD, LB, EY, LR, CO | – |
| ILA specifics (lease, consent fees, online approval) | EY, LR, LB | weak |
| Sale Law guarantees (guarantee vs insurance, voucher book, release) | AD, LB, OT, IR, LR | **weak**: nobody names the 1974 Investments Law or release rules |
| Warranty / defects periods after delivery | none in detail (AD generic, ST EN "construction defects") | **gap** |
| Delivery delay compensation | AD (tiers suspect), GB (calculator link), YL (article links), IR | weak |
| Timelines (deal, registration) | LB, IR, LR, AV/AD per step | – |
| Foreign buyers / olim / remote via POA | IR, AV (link only), ST, AH, AIO EN | **weak in Hebrew**: no foreign-resident tax rates or bank / FX steps |
| Rental / landlord contracts | CO, IR, LF, HK, ST | off-core |
| Real-estate lawyer vs broker | HK (title), MT (link "האם עורך דין יכול להיות גם מתווך?"), AD / AV (broker conflict) | weak |
| Costs beyond the lawyer (registry, agent, appraiser, moving) | AV, AD, DA, ST, EY | – |
| Price research (Tax Authority deals) | AV, AD | – |

**Nobody covers well:** fee payment timing and milestones; a fee matrix by deal type (only addalaw); the Bar's tariff history; dual-representation ethics with rule citations; verifying a lawyer (license, complaints, insurance); land and combination deals; Sale (Investments) Law mechanics and warranty periods; foreign-resident purchase tax in Hebrew; a sourced, dated table of registry fees with no contradictions.

---

## 5. Questions harvested

### 5.1 Hebrew page FAQ / question headings (exact, deduplicated, grouped)
Source codes as in §4.

**Role and need**
- מה תפקידו של עורך דין מקרקעין? (GB)
- מה תפקידו של עורך דין רכישת דירה? (GB)
- מה תפקידו של עורך דין מכירת דירה? (GB)
- מדוע כדאי להיעזר בעורך דין מקרקעין ברכישת נכס בישראל? (IR)
- הנכס נראה לי פשוט. האם אני באמת זקוק לעורך דין? (IR)
- באילו נושאים כדאי לפנות לעורכי דין מקרקעין תל אביב? (YL)
- מהם סוגי העסקאות הנפוצים ביותר בתחום המקרקעין? (GB)
- האם אני מוכרח/ה לשכור עו"ד לרכישת דירה מקבלן? (OT, H2)
- לקבלן יש עורך דין מטעמו - האם לא די בכך? (OT, H2)
- האם חובה לשכור עורך דין ברכישת דירה מקבלן, אם יש לקבלן עורך דין? (LR)
- האם אפשר להסתפק בעורך הדין של הקבלן בקניית דירה חדשה? (AD)
- האם עורך הדין של הקבלן מייצג אותי? (AD)
- האם עורך דין אחד יכול לייצג גם אותי (הקונה) וגם את המוכר באותה עסקה? (LB)
- מתי השלב הנכון ביותר לפנות לעורך דין מקרקעין? (AD)
- באיזה שלב מומלץ להתייעץ עם עורך דין מכירת דירה? (GB)
- מה החשיבות של בחירת עורך דין המתמחה במקרקעין לייצוג משפטי במכירה של הדירה? (GB)
- אנו קונים דירה לראשונה בחיינו, האם נבין את כל הפרטים? (AV)
- לא מדובר סה"כ בייצוג משפטי ברכישת דירה? (YB, H3)

**Fees**
- מה עלויות שכר הטרחה של עורך דין מקרקעין? (GB)
- מהו שכר הטרחה של עורך דין מקרקעין בייצוג במכירת הדירה? (GB)
- כמה עולה עורך דין לקניית דירה? (AD, AV)
- כמה עולה עורך דין לקניית דירה – יד שנייה או מקבלן? (DA)
- כמה לוקח עורך דין על מכירת דירה? (DA)
- מהו שכר הטרחה המקובל של עורך דין ברכישת דירה? (LB)
- כמה כסף עורך דין צריך לדרוש בעסקת מקרקעין? (MT)
- מה מחיר ליווי בעסקת מכר מעורכי דין נדל"ן תל אביב? (YL)
- איך עובד התמחור לשירותי עורכי דין מקרקעין תל אביב? (YL)
- כיצד נקבע שכר הטרחה? (IR)
- מה כולל שכר הטרחה? (DA)
- האם שכר הטרחה כולל מע"מ? (DA)
- מתי משלמים את שכר הטרחה? (DA)
- אילו תשלומים יש מלבד שכר הטרחה? (DA)
- מהן העלויות בעת רכישת דירה? (AV)
- למה מומלץ לוודא מול עורכי דין מקרקעין תל אביב אם השירות כולל ליווי רצוף? (YL)
- כמה עולה עורך דין לקניית דירה – פירוט שכר טרחה / מה מצדיק תעריף גבוה יותר בליווי עו"ד רכישת דירה? / מה כלול בשכר הטרחה? (AD, headings)

**Choosing and working with the office**
- איך לבחור עו"ד מקרקעין ונדל"ן? (GB)
- איך לבחור עורך דין לקניית דירה? (AD, MT headings)
- כיצד מתנהל תהליך העבודה עם המשרד? (IR)
- למה אני צריך "נוהל 150"? עורך דין רגיל לא עושה את אותן בדיקות? בכנות? (YB)
- האם כל הבדיקות האלו לא יעכבו את החתימה? המוכר לחוץ. (YB)
- מה הכוונה ב"שליטה מלאה בכל שלב"? אני אדע מה קורה? (YB)
- איך הגישה הטכנולוגית שבה אתם עובדים באה לידי ביטוי? (YB, H3)

**Process and checks**
- מהם השלבים העיקריים בתהליך רכישת דירה? (GB)
- מהם הדברים החשובים שצריך לבדוק ביחס לדירה לפני החתימה על החוזה? (GB)
- מה חשוב לבדוק לפני קניית דירה? (MT) / מה חשוב לבדוק לפני קניית דירה? ואיך קונים נכון? (AV)
- אילו בדיקות מקדמיות חשוב לערוך לפני מכירת הדירה? (GB)
- מהן הנקודות המהותיות שעורך דין המייצג מוכר צריך להדגיש בהסכם המכר? (GB)
- מה זה נסח טאבו? (MT)
- מה ההבדל בין מנהל מקרקעי ישראל (רמ"י) לבין הטאבו? (LR)
- מהן חריגות בנייה וכיצד הן משפיעות על העסקה? (LR) / אתם בודקים גם חריגות בנייה? (YB) / האם אתם מבצעים בדיקות תכנוניות והנדסיות? (YB, H3)
- מה קורה אם יש למוכר חובות או עיקולים על הדירה? (LB) / מה קורה אם גיליתם בעיה בנכס? העסקה מתפוצצת? (YB)
- האם ניתן למכור דירה שיש עליה משכנתא? (LR)
- מה בודקים לפני שקונים מגרש לבנייה? (LR)
- מצאתי דירה מושלמת, אבל תחושת הבטן שלי אומרת שמשהו מוזר. מה לעשות? (YB)
- יש לי כבר טיוטת חוזה מהצד השני, מה עכשיו? (YB)
- מתי כדאי לקבל אישור עקרוני למשכנתא? (LB)
- האם אתם עובדים עם הבנקים הישראליים בנוגע למשכנתא? (IR)
- מה חשוב לבדוק בדירה במעמד קבלת החזקה? (LB)
- מה ההבדל בין קניית דירה יד שניה לבין קניית דירה מקבלן? (AV)
- מהם הסיכונים ברכישת דירה "על הנייר"? (LR) / מהם הסיכונים העיקריים ברכישת דירה "על הנייר" מקבלן? (LB)
- האם 150 בדיקות אומר שהתהליך ייקח הרבה זמן? (YB, H3)

**Memorandum and warning note**
- מדוע כדאי להימנע מלחתום על זיכרון דברים עם המוכר? (GB)
- האם "זיכרון דברים" מסוכן? (IR)
- האם אני חייב לחתום על זיכרון דברים לפני חוזה רכישה? (LB)
- מדוע אסור לחתום על זיכרון דברים ללא ייעוץ משפטי? (LR, H3) / למה מסוכן לחתום על זיכרון דברים? (AD, H2)
- מהי "הערת אזהרה" ולמה היא חשובה? (LR) / מהי "הערת אזהרה" ומדוע היא חשובה לי כקונה? (LB) / מהי "הערת אזהרה" ומתי רושמים אותה? (AD)

**Taxes**
- מהו מס רכישה ומתי משלמים אותו? (LR) / מהו "מס רכישה" וכיצד הוא מחושב? (LB) / מהו מס רכישה? (IR) / מי משלם את מס הרכישה ומתי? (AD)
- מהו מס שבח? (IR)
- מהם התנאים המסוימים של מוכר דירת מגורים לעמוד בהם כדי לקבל פטור ממס שבח? (GB)
- מהו היטל השבחה ואילו מקרים המוכר יידרש לשלמו? (GB)
- אילו סוגי מיסים ניתנים להפחתה בסיוע של עורך דין מיסוי מקרקעין? (GB)
- באיזה שלב של עסקת המקרקעין כדאי לפנות לעורך דין מיסוי מקרקעין? (GB)
- האם אתם עוזרים גם בתכנון מס? (YB)
- מתי צריך להעביר את המקדמה? (AD/AV heading, CGT advance)

**Time**
- כמה זמן לוקח להעביר בעלות על דירה? (LR)
- כמה זמן אורך בדרך כלל תהליך רכישת דירה בליווי עורך דין? (LB)
- מהו משך הזמן לעסקת מקרקעין בישראל? (IR)

**Remote / olim / disputes**
- האם חובה להיות נוכח בישראל כדי לרכוש נכס? (IR)
- האם אני יכול לרכוש נכס בישראל כעולה חדש? (IR)
- מה קורה במקרה של מחלוקת לאחר הרכישה? (IR)

**Urban renewal**
- מה תפקידו של עורך הדין בפרויקט תמ"א 38? (LR)
- מהי תוכנית תמ"א 38? / מהם ההבדלים בין תמ"א 38/1 לתמ"א 38/2? / איך אדע איזה סוג תמ"א 38 מתאים לבניין שלי? / מהו אחוז ההסכמה הנדרש של הדיירים כדי להוציא לפועל פרויקט תמ"א 38? (GB)
- באיזה אופן עורך דין פינוי בינוי יסייע לי בפרויקט? / מהו דייר סרבן? / מהו תקן 21? (GB)

**Question-shaped related links (not FAQ, useful as long-tail):** midrag tip: "מה זה הערת אזהרה?", "מה זה זכרון דברים?", "איך מבטלים הערת אזהרה בטאבו?", "מה זה תקנה 27?", "מה זה הערת אזהרה סעיף 126?", "מה זה חברה משכנת?", "אישור זכויות - מה זה?", "מה זה פרצלציה?", "מה זה מושע?", "מה זה עסקת קומבינציה?", "מה זה הסכם מכר?", "מה זה טופס 4?", "מה זה אישור מס רכוש?", "מה זה חכירה מהוונת?", "מה ההבדל בין חכירה להשכרה?", "האם עורך דין יכול להיות גם מתווך?", "מהי דירת מגורים מזכה?", "שכר טרחה של עורך דין מקרקעין". Hakoach article titles: "לא סומכים על כל אחד – כל השאלות שחשוב לשאול עו"ד מקרקעין לפני קניית דירה", "באילו מקרים נזדקק לשירותיו של עו"ד מקרקעין וכיצד בוחרים את המתאים ביותר?", "איך עוזר עורך דין מקרקעין בעסקה?", "איך בוחרים עורך דין מקרקעין?", "3 שאלות שיש לשאול עו"ד נדל"ן לפני ששוכרים את שירותיו", "עורכי דין נדל"ן לעומת סוכני נדל"ן". Lawfind teasers: "כיצד לבחור עורך דין מקרקעין", "שכר טירחה בחוזה נדל"ן", "זמן סביר לרישום דירה בטאבו".

### 5.2 Hebrew PAA (from SERP; no answers captured)
Q1 mobile: כמה עורכי דין רשומים בישראל? · איפה אני יכול למצוא עורך דין למשפחה? · איך מגישים תלונה על עורך דין? · איפה אפשר למצוא חוות דעת על עורכי דין? · איך אני יכול למצוא עורך דין? · מה כולל ביטוח אחריות מקצועית לעורכי דין? · האם מנורה מבטחים מציעה ביטוח אחריות מקצועית לעורכי דין? · מהו מספר הטלפון של שירות הלקוחות של איילון אחריות מקצועית לסוכני ביטוח? · מהו ביטוח Run Off?
Q2 desktop (dedup; "איפה אני יכול למצוא עורך דין למשפחה?" repeats): כמה עורך דין גובה על מכירת דירה? · מהם השלבים בתהליך קניית דירה? · מהן הבדיקות שיש לבצע לפני קניית דירה? · מה עליי לבדוק לפני שאני שוכר דירה? · מהם השלבים ברכישת דירה יד שניה? · מהן העלויות הנוספות ברכישת דירה? · איך לקנות דירה?

### 5.3 Related searches (Q2)
שכר טרחה עורך דין קניית דירה מקבלן · שכר טרחה עורך דין מכירת דירה יד שניה · מתי משלמים לעורך דין קניית דירה · איך מחשבים שכר טרחת עורך דין · עורך דין מקרקעין · שכר טרחת עורך דין קבלן · שכר טרחה עורך דין רישום בטאבו · תקנות שכר טרחה עורך דין

### 5.4 English PAA (EN query; no answers captured)
How much does a lawyer cost in Israel? · Who are the best lawyers in Israel? · How much is real estate in Israel? · Who owns the most property in Israel? · Who is the richest family in Israel? · Which city in Israel is the richest? · What is the nicest place to live in Israel? · Where do billionaires live in Israel? · What's the safest city in Israel?

### 5.5 English page FAQ / question headings
- strn: FAQPage contains only "Why do we need? (test)" ("This is why."), a placeholder.
- aharoni (in body): "How Are Real Estate Contracts Negotiated In Israel?" · "What are the specific taxes associated with buying a property in Israel?" · "What are the legal fees?" · "What are the commissions and contract negotiations?" · "What are some of the best neighborhoods and communities to establish yourself?"; footer FAQ links: "What Inheritance Laws Apply In Israel?" · "What Happens If Someone Dies Without A Will in Israel (Intestate)?" · "What Documents Are Needed To Transfer Property In Israel?"
- gornitzky: none.

---

## 6. Heading DNA

**Long guides (addalaw, amitvered, lawreviews-buy, ericyanai):** chronological H2 spine:
1. how to start / pre-contract stage → 2. checks part A (physical, property title / Tabu, occupants, seller identity, condo file, engineer, building file / permit, appraiser) → 3. checks part B (economics: budget, side costs, mortgage approval in principle, LTV, seller's mortgage) → 4. checks part C (taxes: purchase tax brackets, CGT, betterment levy) → 5. memorandum (what, why dangerous, if you must) → 6. payment schedule → 7. why a lawyer → 8. signing (contract chapters, annexes, ancillary documents, first payment) → 9. after signing (warning note, tax report, CGT advance, mortgage, seller-mortgage deletion, municipal certificate, tax approvals, mortgage deeds) → 10. possession (physical vs legal, protocol, meters, keys) → 11. registration → 12. our service / CTA → FAQ.
Add-ons that only addalaw has: "צ'ק-ליסט 5 בדיקות חובה" box near the top, a 2nd-hand vs developer comparison table, "חוק המכר" / delay-compensation / spec sections, a fee table with ranges, a fee-quote comparison card, "מדריכים להעמקה לפי השלב בעסקה".

**Law-firm service pages (gelberg, irelaw, cohen, yonilevy-buy, strn, aharoni):** hero promise + trust counters (deals, years, reviews) → services grid (buy / sell / developer / tax / urban renewal / TAMA / group purchase / foreign) → "why us" → method (gelberg "שיטת הרמזור", irelaw "3 steps", yonilevy "נוהל 150") → testimonials → FAQ by service tab → contact form repeated.

**Directories (lawreviews ×2, psakdin, lawfind, midrag, d.co.il):** H1 "עורכי דין … מומלצים" → "נמצאו N עורכי דין" → cards → quote CTA ("רוצים לקבל כמה הצעות מחיר") → articles → "people also searched" → by city → general-info SEO block (H3 essays: complexity, developer vs 2nd-hand, tax, urban renewal, commercial / land, memo, Tabu) → FAQ.

**Fee page (doron):** "בקצרה" summary box → "what the fee includes" per deal type (H4: sale 2nd-hand, purchase 2nd-hand, developer, gift, inheritance) → average % → other deals (fixed fee) → registry fees list (buyer / seller, 2026) → fee FAQ (6) → office offer.

**How the strongest pages open (first 2 sentences, paraphrased):**
- addalaw: the guide covers every stage of buying in Israel from first checks to registration, for first-time buyers, upgraders and investors; written by a real-estate lawyer active since 2016, then cites the government buyer's guide (Ministry of Construction and Housing) recommending a lawyer, engineer and architect.
- amitvered: the office has handled real-estate deals since 1998 and offers personal "maximum legal protection"; the guide intro says buying is among the biggest deals in life and promises a professional legal guide to the whole second-hand process.
- lawreviews-buy: buying an apartment is for most of us the most significant and exciting deal of our lives, but the Israeli process is legally and bureaucratically complex, so a lawyer is "a necessity, not a luxury".
- gelberg: "don't sign a real-estate deal without understanding the full picture", then the double license (lawyer + certified appraiser) and 1,000+ deals.
- yonilevy-buy: the buyer's lawyer is "the person between you and a fall in the deal of your life", someone who turns every stone through 150 deep checks.
- doron: opens with a "בקצרה" box: fee derives from value, deal type and complexity; around 0.5% + VAT in 2026; taxes and fees are separate.
- irelaw: "your real-estate lawyer in Israel", transparent fees without conditions, buy from Israel or abroad by POA.
- midrag tip: "about to buy? congratulations, but before planning the dream home, call a real-estate lawyer".
- psakdin: "you surely ask who a real-estate lawyer is": one who deals with immovable property, needed at least once in life.

---

## 7. What Google wants
For **Q1 "עורך דין מקרקעין"**, Google treats the query as a find-a-lawyer intent. The top three organic results, and most of the 19, are directories and review platforms (lawfind, midrag ×4 URLs, d.co.il ×6, psakdin ×2, carish, azarim). Only a few law-firm pages rank (cohen #5, ire-law #8, yonilevy-TA #9), and there are no long guides. A **local pack** (Oshar Elkayam, Naor Gelberg, Yigal Iliaich – Netanya) sits under #3.

The Hebrew **AI overview** answers with a short role list (due diligence at Tabu / ILA / housing company, contract, warning note and registration, purchase tax / CGT / levies, TAMA 38 / pinui-binui). It then gives "how to choose" advice (specialization; use LawReviews or Midrag reviews) and names offices (Oshar Elkayam, Yoni Levy, Limor Arbel). Its references are LawReviews, gelberglaw.co.il, yonilevy.co.il, limorarbel.com, Midrag, and Google Business Profiles. It ends by asking the user's region and deal type. The named firms overlap with the promo posts on hakoach (Elkayam, Arbel, Levy), which points to entity, review and mention signals rather than content.

For **Q2 "עורך דין קניית דירה"**, intent flips to informational plus commercial. The top 6 are long law-firm guides and fee pages (addalaw 16k words #1, lawreviews-buy #2, doron fee page #3, amitvered 17.8k #6), with one directory. The AI overview lists the lawyer's checks and contract role, then a fee block: second-hand "~0.5% + VAT", and the developer's-lawyer cap "the lower of ~5,915 ₪ + VAT or 0.5% of the price (2026; not for luxury flats above a certain sum)". It cites doron-aharoni, midrag tip 5795, adicohen-law and Kol Zchut (only Kol Zchut actually carries 5,915).

For **EN**, Google shows firm pages (Gornitzky, Sternberg, Aharoni, Givati) plus directories (LawReviews EN, Legal 500, Lawzana) and an AIO with firm cards (ratings) and a costs block taken from Sternberg's table. The opening for the nad-lan page is a page that combines a directory-grade "how to choose / verify" layer with a dated, sourced fee and cap table (the AIO is already pulling those numbers). It should own the exact H1/title "עורך דין מקרקעין" as an informational hub that links to the buy and sell intents.

---

## 8. English pages (g8en-*)

**g8en-strn (Sternberg & Co.)**: H1 "Real Estate Lawyer in Israel for Property Matters and Strategic Representation"; H2s: partners who handle your case; why you need a real-estate attorney (93% state / 7% private); representation in Tel Aviv / Jerusalem / nationwide (non-residents); services for buying (developer, receiver, second-hand, investment, commercial; memo "zichron dvarim" may bind); due diligence (ILA ownership verification, Taba review, engineers / appraisers); transaction process (agent fees, ownership types, negotiation, title / encumbrance checks, mortgage help); contract drafting (Hebrew with translations; in-house notary for POA); registration (tax declarations, cautionary notes, registration); renovations and rentals; **costs table** (purchase tax "according to brackets incl. foreign resident"; agent 1.5–2% + VAT; appraiser / engineer 3,000–7,000 NIS + VAT; registration fees 1,500–2,500 NIS + VAT); urban renewal (Pinoi Binoi, Tama 38); leases; litigation; combination agreements / JV; construction defects; lost / unclaimed property; contact. Foreign-buyer topics: non-residents, remote, translation, notarial POA, ILA. No lawyer-fee figure; FAQ placeholder.

**g8en-gornitzky**: H1 "REAL ESTATE & CONSTRUCTION", "Building the legal foundations"; large-project positioning (highways, tunnels, desalination, hotels); key contacts; 50+ deal / news H3s (incl. "New Purchase Tax regulations for Olim Chadashim", "Client update regarding taxation of apartments in Israel", "Key Questions: Gifting an Apartment to Children"); Chambers / Legal 500 quotes. No fees, no consumer process, no foreign-buyer guidance beyond "local and international clients".

**g8en-aharoni**: H1 "Israeli Real Estate Lawyer"; services (contracts, property rights search, due diligence, registry, litigation, mortgage incl. vacation houses, leases, taxation); "How are contracts negotiated in Israel" (lawyers negotiate drafts, unlike the US); purchasing for Aliya (taxes, legal fees, commissions, neighborhoods); location factors (schools, synagogues, English-speaking communities); costs; **taxes** (purchase tax "within 60 days of moving to the country" (wrong), exempt to 1.7M, 3.5–10%, 10% above 17.3M (outdated), "rates change every January"; capital gains ~25% of net gain; rental income tax; municipal tax). Foreign-buyer topics: US / Canada / UK / Europe clients, offices in TA / LA / NY / Miami, free consultation. No fee figures.

**EN AIO DNA (for reference):** "mandatory for a safe property transaction"; over 90% publicly owned land; caveat emptor; services (Taba / Tabu due diligence, contracts, purchase tax "Mas Rchisha" and capital-gains "Mas Shevach", Tama 38 / Pinoi Binoi, foreign-buyer remote transactions, escrow, banking compliance); firm cards with ratings; costs (legal 0.5–1.5% + VAT or flat; registration 1,500–2,500 NIS + VAT; appraiser 3,000–7,000 NIS + VAT; agent 1.5–2% + VAT); closing questions (residential or commercial? city or ILA land? resident or foreign?).
