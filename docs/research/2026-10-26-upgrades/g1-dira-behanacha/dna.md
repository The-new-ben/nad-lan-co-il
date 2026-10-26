# G1 · /dira-behanacha/ (page 8541) · research, competitor DNA, facts and build spec

Upgrade loop gap page G1 (Ben, 26.10.2026): make the existing owner page win **"מחיר למשתכן"** (90,500 searches a month in Israel,
KD 19, CPC $3.78) and **"דירה בהנחה"** (74,000, KD 18). LOCAL ONLY: research, spec, design, build and preview. Nothing on the live
site was changed, no REST write, no deploy script, no live file edited, nothing committed, no Linear or Notion item created by this
session. Prepared 26.10.2026 (09:50 to 13:00 UTC) by the G1 research lead (Claude Opus 5.5). GSC API: live, full scope (reads only).

Evidence classes: **code** = raw HTML, an official data file or an API read by script; **chrome** = page rendered in a real Chrome
(playwright, channel chrome) because gov.il and madlan.co.il answer 403 to scripts; **SERP** = DataForSEO Google organic live advanced
(Israel 2376, Hebrew, depth 20, async AI overview, PAA click depth 2), 26.10.2026 09:57:39 to 09:58:19 UTC; **GSC** = Search Console
API, sc-domain:nad-lan.co.il; **eyes** = a screenshot I looked at. Anything not proven is marked **unverified** and kept off the page.

Raw files (outside the repo): `C:\Users\777\nad-lan\_private-research\2026-10-26-upgrades\raw\g1\`
- `serp\` 6 head SERPs (`serp_mechir`, `serp_mechir_m`, `serp_dira`, `serp_dira_m`, `serp_hagralot`, `serp_matara`), 6 side searches,
  `serp-summary.txt`, `serp-log.json`; keyword volumes `kw_he.json` (102 asked, 80 with data), `kw_en_il.json`, `kw_en_us.json`
- `comp\` 33 pages as `c-*.html` + `c-*.txt` (`fetch-log.json` has status, size, UTC time and "real Chrome" for the 12 read rendered)
- `gov\` the ministry's releases of 23.6.2026 and 2.8.2026 (chrome); `data\` data.gov.il package + the full lottery datastore (2,352 rows),
  `data\moch\` the probe of dira.moch.gov.il (its project list needs a login: not used)
- `ours-dira.html` (our live page, 26.10.2026 09:51 UTC), `ours-en-developer-deals.html`, `urlaudit-tokens.txt`
- Earlier full reads (22.10.2026, 47 pages in Chrome, incl. the 8 chapters of the gov.il participation guide): `scratchpad\dira\pages\`
  and `docs/research/2026-10-22-dira-behanacha/serp-research.md` (this spec re-checks every fact it reuses).

---

## 1. Intents, keywords, ownership

**Where we stand (GSC + URL Inspection, code).** /dira-behanacha/ was published 22.10.2026 (HAD-583) and is **"Discovered - currently
not indexed"** (URL Inspection API, 26.10.2026). It has 0 impressions for any query (query+page 20.10 to 25.10.2026: 0 rows). It is
in `page-sitemap.xml` (lastmod 22.10.2026). In 90 days (27.7 to 25.10.2026) the whole site got only stray impressions on the cluster:
"מחשבון משכנתא מחיר למשתכן" 4@46 and "מחשבון מחיר למשתכן" 1@52 on /mortgage-calculator/, "מכרזי מחיר למשתכן" 2@81 on
/developer-deals/. No cannibalization exists. **We do not request indexing (owner law 22.10.2026).**

**Ownership (code).** `url_word_audit.py`, 26.10.2026, 4,598 URLs: `dira` and `behanacha` = only /dira-behanacha/; `mishtaken`,
`lottery`, `hagrala`, `discount`, `eligibility` = 0. `docs/seo/protected-keywords.md` names /dira-behanacha/ as owner of both head
terms (tier A). The titles cache (4,533 rows) shows no other page with מחיר למשתכן / דירה בהנחה / מחיר מטרה / הגרלה in title or H1.
English: /affordable-apartments-israel-2026/ (a 690,000-shekel buyer guide, no mention of the programme) and /en/developer-deals/
(foreign-buyer developer incentives, no mention). **No new URL is needed.**

**Keyword set (DataForSEO Labs keyword overview, IL/he, 26.10.2026, $0.034; monthly volumes, newest month first in the trend):**

| # | Intent | Queries (volume / month) | Owner |
|---|---|---|---|
| 1 | What the programme is (name, both names) | מחיר למשתכן 90,500 (trend 90.5k, 110k, 110k, 135k, 135k, 49.5k: peaks with lottery openings) · דירה בהנחה 74,000 · מחיר מטרה 3,600 · מה זה מחיר למשתכן 140 · מה זה דירה בהנחה 50 · מחיר מופחת 50 | /dira-behanacha/ |
| 2 | Lotteries: when, where, results | מחיר למשתכן הגרלות 6,600 · מחיר למשתכן הגרלה 6,600 · הגרלות מחיר למשתכן 5,400 · דירה בהנחה הגרלות 3,600 · דירה בהנחה הגרלה 3,600 · הגרלת/הגרלות דירה בהנחה 2,900 each · מחיר למשתכן ההגרלה הבאה 1,300 · דירה בהנחה תוצאות 880 · מחיר למשתכן תוצאות 390 · תוצאות הגרלה דירה בהנחה 390 · מתי ההגרלה הבאה של דירה בהנחה 320 · דירה בהנחה הגרלה הבאה 210 · סדר הגרלות דירה בהנחה 70 · רשימת ערים דירה בהנחה 50 | /dira-behanacha/ |
| 3 | Year | מחיר למשתכן 2026 3,600 · דירה בהנחה 2026 3,600 | /dira-behanacha/ (title carries 2026) |
| 4 | Eligibility and certificate | אישור זכאות מחיר למשתכן 1,000 · מחיר למשתכן זכאות 880 · דירה בהנחה זכאות 720 · אישור זכאות דירה בהנחה 320 · מי זכאי למחיר למשתכן 170 · חידוש זכאות דירה בהנחה 170 · מי זכאי לדירה בהנחה 140 · משפרי דיור 480 · דירה בהנחה מילואים 880 | /dira-behanacha/ |
| 5 | Registration, personal area, phones | מחיר למשתכן אזור אישי 2,400 (CPC 36.72) · מחיר למשתכן הרשמה 1,300 · דירה בהנחה אזור אישי 1,300 · דירה בהנחה הרשמה 590 · מילגם דירה בהנחה 720 · אלונים דירה בהנחה 590 · מחיר למשתכן טלפון 260 · מעוף דירה בהנחה 170 | navigational to the ministry and the registration companies; we answer how and link out (we cannot own a login) |
| 6 | Odds and tools | מחשבון מחיר למשתכן 70 · מחשבון דירה בהנחה 70 · מחיר למשתכן סיכויים, סיכויי זכייה (no volume returned) | /dira-behanacha/ (the tools) |
| 7 | Price and money | דירה בהנחה מחירים 90 · משכנתא מחיר למשתכן 90 · מחשבון משכנתא מחיר למשתכן 70 · הון עצמי מחיר למשתכן 70 · דירות ללא הגרלה 140 | /dira-behanacha/ for the programme's rules; the full mortgage calculation stays with /mortgage-calculator/ (linked, its anchor) |
| 8 | Not ours | דירה להשכיר 27,100 (generic "apartment for rent" and the name of the government rental company; the protected list has "דירה להשכרה" with no owner) · מכרזי מחיר למשתכן 110 (RAMI tenders, /developer-deals/ and /michraz-dirot/ territory) | not chased |

**English demand (DataForSEO, 26.10.2026).** Israel/English: no data for any of 20 terms. US/English: affordable housing israel 20,
mechir lamishtaken 10, israel housing lottery 10, israel apartment lottery 10; nothing else. **Decision: no English URL.** A short
English section inside the existing English page /en/developer-deals/ answers "can a foreign buyer use it" (draft: `en-section.html`).

**Title guard (code, `tools/seo/kw_guard.py`, Git Bash `MSYS_NO_PATHCONV=1`, with the 90-day query+page CSV):** title, H1 and meta all
**OK** (this page owns both terms). Anchors in the new copy: "מחשבון המשכנתא" → /mortgage-calculator/ OK, "פגישה עם עורך דין מקרקעין"
→ /real-estate-lawyer/ OK. One anchor was dropped after a WARN: "מחשבון כמה משכנתא אפשר לקחת" → the child page, because Search Console
gives "כמה משכנתא אפשר לקחת" only to /mortgage-calculator/ (314 impressions @63.8); the old paragraph keeps its existing link.
Full output: `kw-guard.txt`.

---

## 2. SERP snapshot (26.10.2026, 09:57 to 09:58 UTC, DataForSEO, Google Israel, Hebrew)

nad-lan.co.il appears in none of the six SERPs (top 20). **AI overview: present on all six.** **People also ask: only on "מחיר למשתכן
הגרלות"** (9 questions, answers load late and were not returned). Madlan's two guides sit at 13 and 17; Yad2 and TheMarker absent.

**"מחיר למשתכן" (desktop).** 1 dira.moch.gov.il/exception-file.html (an error file) · 2 dira.moch.gov.il/.../header.html ("סביבת בדיקות",
a test-environment partial) · 3 shikun-maof.co.il/online/ (registration form) · 4 gov.il spokesman-25052026 (round 11 opens) · 5
mashcantaman.co.il "רשימת כל המכרזים והפרויקטים בתכנית מחיר למשתכן" (a 4,488-cell tenders table, 28.11.2025) · 6 Facebook group
simplehouseil (35.3K) · 7 mgad.co.il/meshtakenn (a developer's page) · 8 gov.il mishtaken_contact · 9 midrag Q&A · 10 israhc.org
"מדד הגר" (an affordable-housing index) · then gov.il spokesman-12042026, dira.milgam.co.il, madlan blog (13), akc.co.il (14), kantahome,
meyda (2022), alonim form, pln.co.il calculator, Facebook page. **Mobile** 1 dira.moch exception file · 2 gov.il spokesman 25.5 · 3
mashcantaman · 4 dira.moch header · 5 midrag · 6 mgad · 7 gov.il 12.4 · 8 israhc · 9 Facebook · 10 res-nadlan.
**AI overview (same on both):** "מחיר למשתכן היא תוכנית ממשלתית ... כיום פועלת התוכנית תחת השם המרכזי דירה בהנחה" with the four tracks;
eligibility (homeless singles "מגיל 26" (stale), improvers, reserve, disabled); certificate 200 ₪, renewal 50 ₪, companies "מילגם,
אלונים ועמידר" (Amidar is stale: today Maof); up to 3 towns; discount "26% ל־40%" (Wikipedia's historic figure); grant towns; sale lock
5/7 years. Sources: dira.moch, gov.il topic, Kol Zchut, Wikipedia, Mizrahi, Bank Hapoalim, Maof.
Related: מתי נפתחות הגרלות מחיר למשתכן 2026 / 2027 · אישור זכאות · הרשמה 2026 · מעוף · ההגרלה הבאה · הגרלות פתוחות · 2026 ערים ·
רשימת הגרלות · סדר הגרלות 2026 · 2026 מחירים · הגרלה 12.
**Reading:** the head term's top 10 is weak: two broken government files, a form, a May release, a 2025 list, a Facebook group, two
small sites. No page answers name + eligibility + this round + odds + money in one place. This is the most winnable head term on
the site's list.

**"דירה בהנחה" (desktop).** 1 dira.moch.gov.il (home) · 2 gov.il topic page · AI overview · 3 shikun-maof/dira · 4 alonim · 5 Facebook
(ministry page, 72.9K) · 6 arcgis project map · 7 Kol Zchut · 8 dira.milgam · 9 miluim.idf.il · 10 Mizrahi "זכיתם בדירה בהנחה?" ·
then gov.il registration service, nadlancenter/5349, renten, Globes 25.5.2026, **better-dira.co.il (16)**, madlan (17), shikun.milgam.
**Mobile:** 1 **better-dira.co.il** · 2 nadlancenter/14284 · 3 renten · AI overview · 4 Facebook · 5 Calcalist · 6 dira.moch header ·
7 mako 25.5.2026 · 8 fnx · 9 ynet tag · 10 klikatnadlan. **AI overview:** register and get a certificate at dira.moch.gov.il; who is
eligible (homeless, improvers, reserve 60 days in order 8); 200 / 50 ₪; Alonim, Milgam, Maof; four tracks. Related: 2026 · הגרלות ·
אזור אישי · תוצאות · זכאות · הרשמה · מתי ההגרלה · מילואים.
**Reading:** navigational and authority-heavy (the ministry twice, three registration companies, Kol Zchut, IDF, a bank). Mobile is
volatile (better-dira first). Realistic for us: page 1 bottom or page 2 for the bare term, with a better shot at the AI overview's
"tool" citation (22.10 the overview named better-dira as the odds tool).

**"מחיר למשתכן הגרלות"** (PAA): מתי תתקיים הגרלת מחיר למשתכן 2026? · מתי תהיה הגרלת מחיר למשתכן? · איך נכנסים לאזור האישי באתר הגרלות
מחיר למשתכן? · איפה אני יכול למצוא את תוצאות הגרלת "דירה בהנחה"? · באיזה ערים תתקיים הגרלת "דירה בהנחה"? · איך נרשמים להגרלה של דירה
בהנחה? · מי זכאי לדירה בהנחה? · מהם סיכויי הזכייה בהגרלת מחיר למשתכן? · איך אני יכול לקבל אישור זכאות לרכישת דירה בתוכנית "דירה
בהנחה"? (all nine are answered in the new FAQ or the page). AI overview: certificates resumed "החל מ־5 באוקטובר 2026"; reserve up to 50%;
IDF draft condition; "ניתן לבדוק נתונים והסתברויות לפי יישובים באתרים כמו הגרלות דירה בהנחה" citing better-dira. Top 10: dira.moch,
gov.il registration, Facebook, arcgis map, milgam, maof, Kol Zchut, renten, gov.il topic, alonim.

**"מחיר מטרה"** (desktop): 1 gov.il guide · 2 nadlancenter/350 · 3 Facebook · images · 4 dira.moch · 5 Mizrahi · ... 12 Wikipedia ·
16 madlan "10 נקודות על מחיר למשתכן". AI overview: "הנחה של עד 20% או עד תקרה של 500,000 ש"ח" (mixes two eras; source a law firm).

Earlier SERPs (22.10.2026, `serp-research.md`): PAA on "דירה בהנחה הגרלה", "דירה בהנחה מי זכאי", "הגרלת דירה בהנחה תוצאות" (27 more
questions, among them: האם ידועים בציבור זכאים, כמה הון עצמי צריך, מי נחשב משפר דיור, האם רכישת שליש דירה פוגעת בזכאות, מי נחשב
מחוסר דיור); the odds intent ("מחיר למשתכן סיכויים לזכות") had no strong page: social posts, forum threads, 2016 to 2023 news.

---

## 3. Competitor DNA (read in full; counts by `tools/depth_proof.py` through `proof_run.py`, which percent-encodes Hebrew paths)

| Competitor (where it ranks) | Title / H1 / keyword placement | Size, structure | Tables, tools, data | Freshness, schema | Why it ranks / weakness |
|---|---|---|---|---|---|
| **gov.il topic + eligibility + guide + releases** (1-2 on both heads, AI overview source) | "דירה בהנחה"; the eligibility page "מי זכאי בתוכניות דירה בהנחה?" | topic 523 words (chrome), eligibility 1,480 (chrome), guide 8 chapters | release tables (round 11 towns, households) | eligibility updated 26.5.2026, registration and certificate 24.9.2026 | Authority. Spread over 10+ pages, a notice in future tense for 5.10.2026, no odds, no money comparison, the "מה זה דירה בהנחה" page is a broken link (22.10) |
| **dira.moch.gov.il** (1 and 2 on מחיר למשתכן, 1 on דירה בהנחה) | header still "מחיר למשתכן" | a login app; Google ranks an error file and a test-environment partial | the project list needs a login | | Navigational authority; nothing to read |
| **Kol Zchut** (7 דירה בהנחה; AI overview source) | "דירה בהנחה (מחיר למשתכן) (זכות)" | 1,863 words, 23 headings | 1 table (20 cells, call centres), 6 official domains linked | Google shows 17.9.2026 | Neutral, step by step, cancellation rules. No numbers, no odds, no prices |
| **shikun-maof.co.il/dira** (3 דירה בהנחה; AI overview) | "דירה בהנחה ◇ מעוף לדיור"; "דירה בהנחה" ×35 | 2,387 words, 4 headings, 14 FAQ | 0 tables; 15 images | 18.10.2026; FAQPage, BreadcrumbList | A registration company: authority + FAQ rich data. Sales page, no data |
| **alonim.co.il** (4 דירה בהנחה; AI overview) | "דירה בהנחה - הנפקת זכאויות ..." | 2,884 words, 34 headings (one per family status), 17 Q | an eligibility form (counted as a tool) | none | Same; scannable by status. No numbers |
| **mashcantaman.co.il** (5 מחיר למשתכן desktop, 3 mobile) | "רשימת כל המכרזים והפרויקטים בתכנית מחיר למשתכן"; the term ×567 | 9,932 words, 3 headings | **1 table, 4,488 cells** (every tender) | 28.11.2025; BreadcrumbList | Exact-match title + a giant list Google reads as the "list" intent. Stale (no 2026), no odds, no rules |
| **mgad.co.il** (7) | "תוכנית מחיר למשתכן", no H1 | 1,068 words, 26 headings | none | none | A developer's explainer; thin |
| **midrag** (9) | "מה זה מחיר למשתכן?" | 617 words, QAPage | none; 105 images (site chrome) | none | Exact "what is" question on a strong domain |
| **madlan blog ×2** (13 מחיר למשתכן, 17 דירה בהנחה) | "מחיר למשתכן: מי זכאי, כמה חוסכים ואיך נרשמים" / "דירה בהנחה 2026: הגרלות, זכאות ומה צריך לדעת" | 845 and 815 words (chrome), 17-19 headings | none | 13.10.2026 / 30.6.2026; Article, FAQPage | Brand. Thin and generic |
| **better-dira.co.il** (1 mobile דירה בהנחה; named by the AI overview as the odds tool) | "הגרלות דירה בהנחה" | a JS table, no text | round 11 per lottery: registrants, locals, reserve, odds external/local, price per m2, estimated flat cost | current round only | Fast and exact for one round; no history, no method, no rules, unofficial |
| **mishtaken-hacham.co.il** (12 to 15 on results) | "הגרלות דיור במקום אחד" | JS; 2,515 lotteries, odds per track, a 5-step calculator | the closest product | | Strong product, invisible on the heads, no schema |
| **wizbid.co.il/lotteries/N** (programmatic; seen on side searches) | "הגרלה 1544 בית שמש, 23 דירות, סיכוי זכייה 0.77%" | 738 words a page, 14 headings, FAQ | per lottery: odds, local odds, price per m2 "(ללא מע״מ)", the RAMI tender, "הנחה אמיתית" against Tax Authority deals per m2 | Dataset, Event, FAQPage schema | **The real long-tail rival** (one page per lottery, real-discount per m2). Not on the head terms today |
| nadlancenter 350 / 5349 / 14284 (2 mobile, 12-13) | "מחיר למשתכן - המדריך השלם לשנת 2026" | ~3,750 words in the article (the tool sees 220: the body is outside main) | none | dateModified 2025; content from 2016-2021 (6 years, Amidar, 187.20 ₪) | Domain + exact H1 + "2026" in the title. Stale facts |
| akc, nilikeren, meyda, mizrahi, bankhapoalim, israhc | read | 550 to 1,460 words | none | 2022 to 5.2026 | Topical breadth; none has data |

**Our page now** (`ours-dira.html`, 26.10.2026): 2,121 words, 476 figures, 1 table (the tool summary, 470 cells), 1 tool, 8 FAQ
(FAQPage), 17 headings, 0 visuals, 2 official domains; "מחיר למשתכן" ×3, "דירה בהנחה" ×13; title "דירה בהנחה: הסיכוי לזכות בהגרלה
בכל עיר, מהנתונים הרשמיים" (the 90,500 term is missing from the title and H1); not indexed. Fact coverage 29 of 38 (`coverage-before.md`).

---

## 4. Union checklist and what nobody covers

Covered by at least one competitor (all on the new page, each with source and date): the name and the four tracks · eligibility by
family status · homeless definition and the one-third rule · improvers only in continuation lotteries and the 12-month sale ·
not eligible (two homes, past buyers, kibbutz) · IDF draft-status condition · certificate 200 / 50 ₪, 10 working days, the three
companies and their phone codes · registration steps, personal area, results by SMS and file · up to 3 towns · locals (3 of the last
years or 4 of 10) and their quota · reserve definition and quota · wheelchair priority · 75% financing and the appraisal route · grant ·
state loan rate rule · 45 minutes to choose, 30 working days to sign · sale lock 5/7 years · flats without a lottery · round 11 towns
and flats · next lottery status · a list of lotteries/tenders · odds per lottery (better-dira, mishtaken-hacham, wizbid) · real
discount per lottery (wizbid).

**Gaps no competitor covers (our edge):**
1. **Round 11 by town from the ministry's own table** (households registered per town, 23.6.2026): flats per 100 registered households,
   ranked, beside each town's history in the official file (all registrants and locals). Nobody prints the per-town household numbers.
2. **The 2.73 towns per household** (313,415 town registrations / 114,848 households): why a town shows 2.5 flats per 100 while 6.9% of
   households won. Nobody explains the gap between "odds in a town" and "odds of a household".
3. **Reserve vs everyone else in round 11**: 18.6% (official) vs 3.6% (our calculation), five times.
4. **Every round since March 2022 in one table** (rounds 1 to 9 from the file, 10 and 11 from releases) and the fall of the typical
   lottery's odds from 1.14% to 0.29%; 69% of lotteries since 2022 below 1%.
5. **The price against the town's deal median**, honestly limited to towns whose last lottery price is from 2024-2025: 3.5% (Kiryat Gat)
   to 40.6% (Beit Shemesh) for a 100 m2 flat with VAT against the 4-room median; stale prices excluded and named.
6. **A personal eligibility + track + three-town check** built on the official definitions, and a **cost check** that applies the
   programme's own financing rules (75%, the appraisal route, the grant inside the financing).
7. **Freshness with dates**: the file's newest lottery (27.1.2025) printed, round 12 "no official announcement" stated, the 5.10.2026
   notice reported as what it says. Competitors repeat stale facts (Amidar, 6 years, 187.20 ₪, "מגיל 26").
8. **A full list of the 635 lotteries since 2022** (collapsed), the "רשימת הגרלות / טבלת דירות" intent, larger than mashcantaman's list.

---

## 5. What Google wants to show

- **"מחיר למשתכן" = definition + current state.** The AI overview leads with "today it runs under the name דירה בהנחה, four tracks",
  then eligibility, costs, 3 towns, discount, sale lock. Related searches are all "when does the next lottery open", "2026", "2027",
  "open lotteries", "list of lotteries", "order of lotteries", "prices". The answer paragraph must say both names and the state of the
  lottery today; the page must carry the lottery list and the order.
- **"דירה בהנחה" = navigational + eligibility.** Google ranks the places where you act (the ministry, the companies) and the rights
  explainer. We win the "decide before you act" part: eligibility in one table, which towns, what it costs.
- **Odds are the open intent**: Google's overview sends people to better-dira by name; a page with a transparent method and official
  numbers is the natural replacement citation.
- **Formats:** no video packs on the heads, Facebook groups in 3 of 6, an images block on מחיר מטרה. PAA only on the lottery query.
  "2026" in the related searches of every head query: the title carries 2026.

---

## 6. Verified facts (official unless marked; retrieved 26.10.2026 unless stated)

| Fact | Value | Source (date) · class |
|---|---|---|
| Name and tracks | "דירה בהנחה" is the umbrella of the ministry's and RAMI's programmes: מחיר מטרה, מחיר מופחת, מחיר למשתכן, דירה להשכיר | gov.il/he/departments/topics/dira · chrome |
| Round 11 | opened 25.5.2026, closed 22.6.2026; certificates to 7.6.2026; 7,922 flats, 19 towns, 82 lotteries; 50% to active reservists, about 25% (half of them) to combat; up to 3 towns and all their lotteries; registration time does not matter; IDF draft-status check after closing | spokesman-25052026 · chrome |
| Round 11 by town (order, lotteries, flats, households) | Rishon 2/148/23,425 · Ashdod 1/256/16,299 · Beit Shemesh 4/425/15,012 · Rehovot 1/30/7,623 · Hadera 4/268/22,711 · Kfar Saba 11/1,045/38,732 · Kiryat Gat 9/1,433/28,514 · Nahariya 2/218/12,522 · Eilat 1/99/8,875 · Maale Adumim 16/1,663/22,658 · Yehud 1/121/7,630 · Yokneam 1/89/5,717 · Kadima Tzoran 6/315/23,241 · Kafr Manda 2/131/1,652 · Mazkeret Batya 4/427/19,721 · Rechasim 5/405/12,404 · Beit Dagan 5/399/26,402 · Bnei Ayish 4/179/10,145 · Bat Hefer 3/271/10,132; total line 114,840 households (the town column sums to 313,415) | spokesman-23062026 (updated 6.8.2026) · chrome |
| Round 11 totals | 114,848 households, about 1.7 million registrations; drawn 26.7.2026; notices from 2.8.2026 | spokesman-23062026, spokesman-02082026, topic page · chrome |
| Reserve in round 11 | 25,394 registered, 4,734 won, "כמעט אחד מכל חמישה"; about 60% of all winners | spokesman-02082026 · chrome |
| Round 11 announcement | 12.4.2026, opening set for 15.4.2026 (it opened 25.5.2026) | spokesman-12042026 (SERP title, 22.10 read) |
| The official file | data.gov.il "נתונים תקופתיים - תכנית דירה בהנחה", resource 7c8255d0: 2,352 lotteries 29.2.2016 to **27.1.2025**; modified 16.8.2026; rounds 10 and 11 not in it; 2,340 rows labelled "מחיר למשתכן"; second resource "דירות למכירה ללא הגרלה" has 0 rows in the datastore | data.gov.il API · code |
| Rounds 1 to 9 (from the file) | 635 lotteries, 52,486 flats, 10,040,540 registrations; typical-lottery odds 1.14% (3.2022) to 0.29% (12.2024) | our calculation from the file · code |
| Round 10 | 7,479 flats, 21 towns, opened 10.8.2025, notices 23.11.2025 | ministry notice via rashuiot (6.8.2025), mako (23.11.2025) · **secondary** |
| Eligibility | homeless = no home or more than a third in 3 years (and at contract); family statuses as listed; improvers = one home, sell within 12 months of occupancy, renew themselves from 1.1.2025; not eligible: two homes for a year, past capped-price buyers, kibbutz; locals 3 years or 4 of 10, Population Authority, no appeal; reserve 60 days in order 8 from 7.10.2023, certificates issued to 5.8.2025 give no reserve priority, check at 1111 ext 4; target-price priorities: wheelchair 1 per 30 (at least 1), reserve 50% (25% combat) in periphery 1-4, 35% (15%) elsewhere, locals 20%, periphery cap 73% | gov.il/he/pages/tenaey_zkaut (updated 26.5.2026) · chrome |
| Certificate | 200 ₪, up to 10 working days (can be longer), improvers only in continuation lotteries; registration companies; notice: issuance stopped, "תיפתח מחדש ביום 5.10.2026" | gov.il request_for_eligibility_confirmation and register_for_discounted_housing_lottery (updated 24.9.2026) · chrome |
| Certificate validity, renewal, phones | one year, 50 ₪, Milgam *6078, Alonim *2850, Maof *9344 | spokesman-25052026 · chrome |
| Results | SMS, mail, voice call for kosher phones; personal area; anonymous file per lottery | register page · chrome |
| Financing | up to 75% of the price; with BoI approval by appraised value with at least 100,000 ₪ own money and value up to 2.1M (above it: 2.1M or the price, the higher); grant 40,000 / 60,000 (mishtaken, qualifying towns), 40,000 (mufchat, matara), released after own money; state loan for 10-year homeless: 0.5% below the BoI average linked rate, max 3.0%, 10 to 30 years | gov.il benefits_in_apartment_funding (updated 24.2.2026) · chrome |
| After winning | permit "זמן רב", 45 minutes to choose, contract within 30 working days, sale lock 5 years from Form 4 or 7 from the lottery | gov.il participation guide ch. 5, 7 (22.10.2026) · chrome |
| Flats without a lottery | projects with remaining flats, contact the developer in order, some by mail within 48 hours | gov.il mechirat_dirot_lelo_hagralah (updated 30.5.2024) · chrome |
| Deal medians | by rooms and quarter, data.nadlan.gov.il version 20.8.2026 (via invest.json) | code |
| Mortgage rate | BoI average fixed unlinked 4.62% (8.2026) | boi-mortgage.json · code |
| Purchase tax | only home exempt to 1,978,745 ₪ | ptax.json · code |
| Track mechanics | מחיר למשתכן: lowest bid per m2; מחיר מטרה: discount from the appraised market price | Wikipedia (secondary); RAMI decision 4.7 not opened |

**Unverified, kept off the page:** the discount percentage of מחיר מטרה (25% up to 500,000 since 6.2023 per a law firm and a RAMI text
seen only through prog.co.il; the AI overview says 20%); whether issuance actually reopened on 5.10.2026 (the notice is future tense);
the next lottery's date and towns (i24 20.10.2026: end of December, about 4,000, periphery only; ice 27.9: early 2027; mishtaken-hacham:
December, about 5,000); "75% to reserve from the next lottery" (ice); lottery 10's 132,000 registrants; the cancellation rule (Kol Zchut,
printed with attribution only in one FAQ answer); that the price per m2 is before VAT (two trackers say so; the tool has a switch);
round 11 prices per lottery (only better-dira, from the login-only site).

---

## 7. Gaps on our page today
1. **Not indexed** (Discovered, not indexed, 4 days old). Not something copy fixes; the release and a passive sitemap resubmit are the
   allowed steps. Requesting indexing needs Ben's yes for this page (owner law).
2. The 90,500 term is missing from the title, H1 and answer ("מחיר למשתכן" ×3 on the page).
3. No round-11-by-town numbers, no reserve figures, no money comparison, no eligibility table, no rounds history, 0 visuals.
4. A future-tense date that has passed (certificates "אמורה להיפתח מחדש ב־5.10.2026").
5. 8 FAQ; PAA and related searches unanswered (personal area, results, open now, towns, the reserve odds, grant, purchase tax).

---

## 8. BUILD SPEC (built locally; files in section 11)

### 8.1 Title, H1, meta (guard OK)
- **Yoast title (52 chars):** `מחיר למשתכן ודירה בהנחה 2026: זכאות, הגרלות וסיכויים`. The bigger and weaker-SERP term first, both names
  (the AI overview teaches the equivalence), "2026" for the 7,200 a month of year queries, the three intents Google's related searches show.
- **H1 (post title):** `דירה בהנחה (מחיר למשתכן): מי זכאי, ההגרלות והסיכוי לזכות בכל עיר` (the slug's term first, the old name in
  brackets as Kol Zchut does, the moat named).
- **Meta description:** `דירה בהנחה ומחיר למשתכן 2026: בדיקת זכאות, שלוש הערים עם הסיכוי הגבוה, ההגרלה ה־11 בכל עיר, מילואים 18.6%, המחיר מול העסקאות בעיר והצעדים עד המפתח.`
- The page has no clicks, so the change risks nothing; re-check in Search Console 4 weeks after indexing.

### 8.2 Answer paragraph (head terms first, 72 words)
"דירה בהנחה היא תוכנית הדיור של משרד הבינוי והשיכון ורשות מקרקעי ישראל, שמוכרת לזכאים חסרי דירה דירות חדשות מקבלן במחיר מופחת, בהגרלה.
מחיר למשתכן הוא השם הקודם שלה, והיום הוא אחד מארבעה מסלולים בתוכה, לצד מחיר מטרה, מחיר מופחת ודירה להשכיר. בהגרלה האחרונה, ה־11, נרשמו
114,848 משקי בית ל־7,922 דירות ב־19 יישובים, וזכו 6.9% מהם; משרתי מילואים זכו ב־18.6%. על ההגרלה ה־12 עוד אין הודעה רשמית."

### 8.3 Rendered order (content-first; measured in the local preview)
H1 → answer (390px: 192px from the top) → CTA row "לבדיקת הזכאות והערים שלכם" / "לקבלת פרטים נוספים בוואטסאפ" / "פגישה עם עורך דין
מקרקעין" (525px) → **dirafit** (970px, 1.15 phone screens) → "דירה בהנחה במספרים" + T1 → old answer paragraph + the existing **dira**
tool → old "מה זו דירה בהנחה" + T2 (tracks) → old method → **round 11 by town** (V1 + T3) and **every round since 2022** (V2 + T4 +
collapsed T10) → old locals/reserve → **priorities** (V3 + T5) → old three towns → **three towns in numbers** → old eligibility →
**eligibility matrix and certificate** (T6, T7) → old last/next lottery → **before round 12** checklist → old after winning →
**money** with **diracost**, T8, T9, V4 → FAQ (8 old + 22 new) → "שיטה ומקורות" with the date.

### 8.4 Tables (all generated from dira-round.json by `write_g1_page.py`)
T1 today's numbers (10 rows) · T2 the four tracks · T3 round 11 by town (19 rows × 8) · T4 every round since 2022 (11 rows) · T5
priorities and quotas · T6 eligibility matrix (11 statuses × homeless / improver) · T7 the certificate (3 companies) · T8 price vs deal
median (6 towns with 2024-2025 prices) · T9 financing rules with a worked Kiryat Gat example · T10 all 635 lotteries since 3.2022
(collapsed `<details>`, 5,724 cells; about 200 KB of the 240 KB new content, 32 KB gzipped: a known weight cost, accepted for the
"list" intent).

### 8.5 Infographics (inline SVG, viewBox 420 wide, rtl, text ≥ 12px, numbers also in the tables)
V1 "ההגרלה ה־11: דירות לכל 100 נרשמים בעיר" (ranked bars, the all-towns line 2.5) · V2 "הסיכוי בהגרלה טיפוסית, לפי סבב" (rounds 1-9) ·
V3 "מי זכה בהגרלה ה־11" (reserve 18.6 / all 6.9 / rest 3.6) · V4 "מהזכאות ועד המפתח" (8 steps, the sale lock in survey red). Files in `svg/`.
**Design statement (law 13.10.2026):** NadLan Instruments. Ink #12202A, sea #2F6F86, deep #1F4B5C, line #D3DCE2, survey red #C42550 only
for the warning step, green #4F9A5C only for the financing segment. IBM Plex Sans Hebrew for text, IBM Plex Mono for every figure,
Karantina for tool titles. **Why it is not the default AI look:** no cream, gold, terracotta or purple gradient, no soft-shadow card on
every block; the forms of a lottery protocol, an eligibility form and survey paper. The engine's yellow and purple are kept off the page
(the cost bar has two segments). Claude Design component: `scratchpad/ds/project/components/DiraBehanacha/` (preview.html + README.md).

### 8.6 The moat: two tools nobody has, on official numbers only (`tools/dirafit.js`, NEW)
**dirafit, "מי זכאי, באיזה מסלול, ואיפה הכי כדאי להירשם".** Inputs: family status (9 official statuses), home ownership (5), reserve
(no / 60 days / combat), town of residence (the 19 towns), sort (round 11 / the file / locals in the file); five ready cases.
Output: status (homeless: first and continuation lotteries / improver: continuation only / not eligible with the gov.il reason); the
first town of your list and the next two (local town first when the file has local results); reserve and local priorities; the group
figures of round 11 as scenario buttons; the 19-town table (flats, households, flats per 100, lotteries and median odds in the file,
local odds); notes with the certificate route, the reserve certificate date, the IDF condition.
**diracost, "כמה תעלה הדירה מההגרלה, ומה ההנחה מול מחירי העסקאות בעיר".** Inputs: town, price per m2 (opens on the town's last price
in the file), VAT switch, size, room count, own money, appraisal value, grant 0 / 40,000 / 60,000, rate (BoI 4.62%), term; four ready
cases. Output: price with VAT, the gap against the town's deal median (quarter printed), maximum financing (75% or the appraisal route),
own money needed and the shortfall, the monthly payment, purchase tax, scenarios (rate +1%, 10 m2 more), the all-town table.
**Data:** `data/dira-round.json` (69 KB) built by `tools/instruments/build_dira_round.py` from the official file (fetched live or
`--cache`), the three releases typed with their URLs and asserted (sums 7,922 / 82 / 313,415), the gov.il rules as structured data,
and invest.json medians. **Test:** `node tools/instruments/test_dirafit.js` = 40 checks, ALL OK (group odds, eligibility, ranking,
price, 75%, appraisal route incl. the 2.1M cap and the 100,000 floor, grant inside financing, payment against U2's 563 per 100,000,
purchase tax). **Why it holds:** it needs the ministry's per-town table (published once, in a release), the official file with the
local columns, the gov.il rules coded, and the deal medians joined town by town; better-dira and mishtaken-hacham have odds but no
rules and no money; wizbid has money per lottery but no eligibility and no round 11 by town.

### 8.7 Schema
Already printed by the site: FAQPage from the FAQ section (30 after the change), SoftwareApplication per tool (3 after the release).
Follow-up (not in this build, theme level): BreadcrumbList; a Dataset for T3/T10 (creator: Ministry of Construction and Housing via
data.gov.il; temporalCoverage 2016-02/2026-08).

### 8.8 FAQ: 8 old + 22 new (in `write_g1_page.py` QA_NEW), each answer from section 6; the 9 PAA questions of 26.10 and the 27 of 22.10 are covered.

### 8.9 English
No English URL (demand under 50 a month, section 1). Draft section for /en/developer-deals/: `en-section.html` (foreign buyers are not
eligible; the round 11 figures; link to the Hebrew page). Applying it is Ben's call (the page is a foreign-buyer page).

---

## 9. Proof plan and the predicted honesty statement
**Before** (`proof-before.md`, live page, 26.10.2026 12:09): ours 2,121 words / 476 figures / 1 table / 470 cells / 1 tool / 8 FAQ /
17 headings / 0 visuals / 2 official domains. Competitor max: words 9,932, figures 1,266, cells 4,488 (mashcantaman); FAQ 17, headings 34
(alonim); visuals 105 (midrag); official domains 6 (Kol Zchut). Sum of the 15 measured: words 24,613, figures 1,906, tables 4, cells 4,514,
tools 1, FAQ 48, headings 148, visuals 221, official domains 25. Fact coverage (`coverage-before.md`, 38 facts): ours 29, best 17
(nadlancenter/350), union of competitors 28.
**Predicted after** (`proof-predicted.md` and `coverage-predicted.md`, the local preview at 127.0.0.1, content as the writer builds it;
the live page will add the two tool summaries): **words 15,689** (prose about 5,360; the rest is the T10 list) · **figures 5,388** ·
**tables 10** · **cells 6,196** · **tools 3** · **FAQ 30** · **headings 51** · visuals 4 · official domains 5 (10 official pages) ·
**fact coverage 38 of 38** (union of competitors 28).
**Where we stay behind (named):** pictures (4 data figures against 15 Maof, 105 Midrag site images, 43 israhc); official domains 5 vs
Kol Zchut 6 by the tool's domain count; the competitors' sums on words (24,613, mostly mashcantaman's list), FAQ (48) and headings (148)
are not targets (no padding). Not measurable by script (403): the gov.il pages (authority we cannot match) and Madlan (845 and 815 words,
chrome). Out of scope of a single page: wizbid's one page per lottery.
**Draft for Ben to sign after the release is measured (Hebrew):** "בדקנו ב־26.10.2026 את העמודים שגוגל מדרג על מחיר למשתכן ועל דירה
בהנחה. העמוד שלנו מציג יותר נתונים, יותר טבלאות ויותר עובדות רשמיות מכל אחד מהם ומכולם יחד, והוא היחיד שמראה את ההגרלה ה־11 בכל עיר,
את הסיכוי של משרתי המילואים מול כל השאר ואת המחיר מול חציון העסקאות בעיר, עם בדיקת זכאות ומחשבון. במספר התמונות יש עמודים עם יותר.
כל מספר בעמוד מופיע עם המקור והתאריך שלו, וכל חישוב שלנו מסומן." Replace the numbers with the after-proof before publishing it.
Commands after the release: `python docs/research/2026-10-26-upgrades/g1-dira-behanacha/proof_run.py --out proof-after.md` and
`python .../coverage_run.py --out coverage-after.md`.

### Honest chance of ranking
- **Indexing first:** today the page is not indexed; until Google crawls it nothing ranks. By the owner's law we do not request it.
- **"מחיר למשתכן":** the top 10 is weak (broken government files, a form, a list from 2025, small sites). Once indexed, a top-10 place
  within two to four months is realistic, top 3 is possible but not likely soon: gov.il and the registration companies keep the
  navigational part, and nad-lan.co.il's head terms sit at 13 to 60 today.
- **"דירה בהנחה":** authority-led (gov.il twice, Maof, Alonim, Milgam, Kol Zchut, IDF, a bank). Page 1 bottom or page 2 is the
  realistic target; the AI overview's tool citation (today better-dira) is the better prize.
- **Long tail** (הגרלות by town, סיכויים, מילואים, אזור אישי how-to, ללא הגרלה, רשימת הגרלות): faster, and the year queries
  (7,200 a month) follow the title.
- **Timing:** demand peaks when a lottery opens (135,000 a month in May-June 2026). Being indexed before round 12 matters more than any
  copy change.

---

## 10. Findings for Ben (no action without his word)
1. /dira-behanacha/ is **not indexed** (Discovered, 26.10.2026). Owner law: no indexing request; if he wants an exception for this page,
   it needs his yes. A sitemap resubmit after the release is the passive step the law allows (GSC write: per his word).
2. /en/developer-deals/ prints most of its middle sections and its FAQ **twice** (two "Frequently Asked Questions" sections, repeated
   H2s: Prashkovsky auction, Gindi VOGUE, Azorim, LOV, rent support, Av-Gad, Aura, Mevaseret). Reported only.
3. The ministry's own "מה זה דירה בהנחה?" guide page is a broken link on gov.il (22.10); Google ranks two internal files of
   dira.moch.gov.il (an error file and a test-environment header) at 1 and 2 for "מחיר למשתכן". External, reported for context.
4. The official file stops at 27.1.2025 although it was modified 16.8.2026; rounds 10 and 11 are missing. The page says so.
5. English section on /en/developer-deals/ (draft ready) and the 200 KB lottery list (accepted for now): his call if he disagrees.
6. For the coordinator: the LIVE dira tool files (`tools/dira.js`, `data/dira.json`, `tools/instruments/build_dira_data.py`,
   `harness_dira.html`, release 1.72.496) and both earlier research folders (2026-10-21, 2026-10-22) are untracked in git.

## 11. Files (all local; nothing committed)
| File | What |
|---|---|
| `docs/research/2026-10-26-upgrades/g1-dira-behanacha/dna.md` | this file |
| `.../write_g1_page.py` | the page writer (anchored insertions, title + Yoast meta, gates, backup, read-back, live check). **NOT run live.** Offline run: `--dry --from ../../2026-10-22-dira-behanacha/page.html` |
| `.../preview/g1-page-content.html`, `g1-page-render.html`, `preview/shots/` | the new content, a local render shell, screenshots at 390 and 1280 |
| `.../svg/v1..v4*.svg` | the four infographics |
| `.../page-sources.md` | where every fact comes from (internal) |
| `.../instruments-snippet.md` | the registry and no-script blocks for inc/instruments.php (not applied; PHP linted and run on the data) |
| `.../en-section.html` | the English section draft |
| `.../proof_run.py`, `coverage_run.py`, `coverage-facts.json`, `proof-before.md`, `proof-predicted.md`, `coverage-before.md`, `coverage-predicted.md`, `kw-guard.txt` | proof plan and results |
| `.../build_ds_preview.py` | builds the Claude Design component |
| `plugins/nadlan-config/assets/instruments/tools/dirafit.js` | NEW tool file (dirafit + diracost) |
| `plugins/nadlan-config/assets/instruments/data/dira-round.json` | NEW data |
| `tools/instruments/build_dira_round.py`, `tools/instruments/test_dirafit.js` | NEW builder and test |
| `<scratchpad>/ds/project/components/DiraBehanacha/preview.html`, `README.md` | Claude Design component (not published) |

## 12. Release order (for the releaser, after Ben's go)
1. `python tools/instruments/build_dira_round.py` (fresh from data.gov.il) and `node tools/instruments/test_dirafit.js` = ALL OK.
2. Release: dirafit.js + dira-round.json + live inc/instruments.php with the two blocks of `instruments-snippet.md` (php -l; hunk rules).
3. Check the tools answer on a test mount; then `write_g1_page.py --dry` (REST GET), then without `--dry`.
4. source_audit.py before and after on /dira-behanacha/; rainbow + h-infinity spot check; send Ben the link.
5. proof-after / coverage-after; the honesty statement with the measured numbers; Linear + Notion.
