# /mortgage-calculator/ : keyword universe, live SERPs, intent map and on-page signal plan (5.11.2026)

Research only. Nothing on the site was changed. Prepared 5.11.2026 (evening, Israel time) by the keyword and SERP researcher (Claude Opus 5.5).

Evidence classes: **code** = raw HTML or an API response read by script; **SERP** = DataForSEO `serp/google/organic/live/advanced`,
depth 20, async AI overview, PAA click depth 1, pulled 5.11.2026 19:47 to 19:53 UTC; **GSC** = Search Console API, property
sc-domain:nad-lan.co.il, 4.8 to 3.11.2026; **Ads** = DataForSEO Google Ads `search_volume` (12-month average, Israel 2376, Hebrew
`iw`), 5.11.2026; **KD** = DataForSEO Labs `bulk_keyword_difficulty` and `keyword_ideas` (Israel, he). Anything not proven is marked
**unverified**. Google Ads reports close spelling variants as one group with one number (מחשבון משכנתא, מחשבון משכנתאות, מחשבון משכנתה,
מחשב משכנתא all show 33,100), so volumes inside one intent are **not additive**.

Files in this folder (written by this task): `keywords.csv` (1,410 rows: 1,305 Hebrew, 105 English/French), `serp-2026-11-05.json`
(29 SERPs: 12 Hebrew queries x desktop and mobile, plus 5 English), `gsc-mortgage.csv` (431 rows, pages containing `/mortgage`),
`gsc-mortgage-sitewide.csv` (474 mortgage-word rows from the unfiltered site pull). Other files in this folder (`LOOP.md`, `data/`,
`world-matrix.csv`) belong to a parallel task and were not touched. The repo is public: the two GSC CSVs carry our query data.

Method notes. The owner's DataForSEO CLI (`dfs.cjs`) answered "fetch failed" inside this sandbox, so every call went through the
DataForSEO MCP tool. Google returned organic and AI-overview links as `google.com/goto?url=...`; all 457 of them were resolved to the real
URL by their HTTP 302 target (code). HTML `<title>` and H1 were then fetched for the 198 unique top-10 URLs (183 returned a title; bank
sites behind bot walls are marked unknown). DataForSEO spend for this task: about 1.2 USD (sum of reported call costs, approximate).

---

## 1. The short answer

- The head term is one intent with two alternating result sets. On 5.11 desktop "מחשבון משכנתא" shows the **bank set** (Hapoalim,
  Mashcantaman, Mizrahi-Tefahot, Leumi, Discount, Clal, Leumi Mortgages, Supermarker, Taxo, FIBI) while mobile shows the **independent
  set** (heshevavoda, Taxo, Harel servicebank, mydira, family-economy, Mercantile, gemel, sbc-il, Discount, goola). On 25.10 it was the
  other way round, and "חישוב משכנתא" swapped the opposite way. Earlier today (gap.md) our desktop rank was 28; in this pull we are not in
  the top 20 for the head term on either device. We appear once: **#16 mobile for "מחשבון החזר משכנתא"**. We lost the #6 desktop slot
  we had on 25.10 for "מחשבון משכנתא לפי החזר חודשי".
- Search Console shows Google already treats the page as the face of the whole cluster: 8,710 mortgage impressions on /mortgage-calculator/
  in 90 days, 1 click, and about **1,900 of those impressions belong to intents our child pages own** (reverse 593, capacity 513, LTV 273,
  rates 172, refinance 156, any-purpose 151). The fix is to make the children win those queries (exact-anchor links, child page upgrades),
  never to pull those intents into the main page and never a redirect.
- Weekly trend for the main page (GSC): impressions 322 (week of 14.9) to 892 (week of 19.10) and 884 (26.10); average position 50 to 54
  in mid-September, about 41 from the week of 28.9, then 36.5 (week of 19.10) and 37.4 (week of 26.10). Clicks stay at 0 to 1.
- Title advice: drop "ריבית" (owned by the rates child) and the "| nad-lan" tail (Google already appends "nad-lan - נדלן" to our title, SERP
  5.11), add "חישוב" and "לוח סילוקין". Details in section 8.
- English: build **/en/mortgage-calculator/** as the hreflang twin of the Hebrew page (same pattern as /asbestos/ and /en/asbestos/). The
  Israeli-calculator query group has **260/month in Israel** plus about 60 abroad, the SERP is weak, and Google already sends 22 English
  calculator impressions to the Hebrew page. /israel-mortgage-non-residents/ keeps foreigners and non-residents. Section 9.

---

## 2. Intent map (Hebrew, Israel)

"Volume" = the intent's largest Ads group. "GSC" = impressions @ average position over 90 days, per landing page. KD 0 to 100.

| # | Intent | Owner URL | Evidence: head keywords (volume, KD) | GSC (90 days) | Who ranks today (SERP) | Main page role |
|---|---|---|---|---|---|---|
| 1 | Mortgage calculator, head | **/mortgage-calculator/** | מחשבון משכנתא 33,100 (KD 11, CPC 1.35) · חישוב משכנתא 1,600 (KD 11) · משכנתא מחשבון 1,600 · מחשבון משכנתא פשוט 1,600 · סימולטור משכנתא 590 · סימולציית משכנתא 590 · מחשבון משכנתא ai 320 · מחשבון משכנתא משרד האוצר 260 | main 2,204 @40 | bank set (Hapoalim, Mizrahi, Leumi x2, Discount, Clal, FIBI) + Mashcantaman + Supermarker + Taxo, or the independent set (Taxo, heshevavoda, mydira, family-economy, gemel, Mercantile, lahav-f, ynow, icf) | **own**: title, H1, first paragraph |
| 2 | Monthly payment and payment-first | **/mortgage-calculator/** | מחשבון החזר משכנתא 590 (KD 11) · מחשבון משכנתא לפי החזר חודשי 590 (KD 7) · חישוב החזר משכנתא 480 (KD 11) · החזר משכנתא מחשבון 390 · החזר משכנתא 320 (KD 13) · חישוב משכנתא לפי החזר חודשי (KD 7) | main 2,200 @38 | hoomy, heshevavoda, Taxo, primeinv, Mercantile, moti, gemel, family-economy, Leumi ufapi, gadi-leichter, myhouse, evensapir, c14; **nad-lan #16 mobile** | **own**: H2 for each mode (amount to payment, payment to loan) |
| 3 | Payment for a given amount (1M, 1.5M, 2M) | **/mortgage-calculator/** | החזר משכנתא 1.5 מיליון 260 (KD 0) · החזר משכנתא 1 מיליון 110 (KD 6) · 1.2 מיליון 110 (KD 0) · כמה החזר משכנתא על מיליון שקל 70 · 79 keywords in all | main 228 @53 | not pulled (unverified) | **own** as a section with a crawlable amount x term table (existing H2 "כמה ההחזר על משכנתא של מיליון...") |
| 4 | Track mix and Bank of Israel baskets | **/mortgage-calculator/** | תמהיל 320 · תמהיל משכנתא 260 (KD 0) · מסלולי משכנתא 210 (KD 10) · תמהיל משכנתא מומלץ 110 (KD 2) · מחשבון משכנתא לפי מסלולים (KD 52) · מחשבון תמהיל משכנתא (KD 26) | main 594 @41 | Mashcantaman x2, Mizrahi, Supermarker, kolzchut, mashkantaguru, my-mashkanta, Leumi, midrag, ogen1, pardes, lsmashkanta | **own**: section |
| 5 | Amortization schedule: Spitzer, equal principal, balloon, grace | **/mortgage-calculator/** (for the mortgage forms) | שפיצר 1,000 (KD 0) · מחשבון שפיצר 720 · לוח שפיצר 590 (KD 0) · לוח סילוקין 480 (KD 0) · לוח סילוקין שפיצר 480 · מחשבון לוח שפיצר עם לוח סילוקין 260 · לוח סילוקין משכנתא (KD 1) · מחשבון שפיצר משכנתא (KD 9) | main 296 @68 | generic loan and definition pages: nadlancenter, hon x3, max, financialplanning, houseofinance, Mercantile, wikipedia, heshevavoda | **own a section** titled for the mortgage form ("לוח סילוקין למשכנתא"); the generic loan forms are not ours |
| 6 | Compare a bank offer / check a mortgage | **/mortgage-calculator/** | השוואת משכנתאות 260 (KD 19) · השוואת משכנתא 260 · בדיקת משכנתא 170 (KD 19) · הצעות משכנתא 70 (KD 54) | main 228 @37; **"בדיקת משכנתא" 104 @17** is the page's best position | not pulled (unverified) | **own**: the "your offer vs the Bank of Israel average" section |
| 7 | Total cost of a mortgage | **/mortgage-calculator/** | עלות משכנתא (KD 58) · כמה עולה משכנתא (KD 25) · מחיר משכנתא 50 · עלויות משכנתא | main 384 @44 | not pulled (unverified) | **own**: answer in the first screen ("עלות כוללת") |
| 8 | What a mortgage is (head word) | **/mortgage-calculator/** (protected tier A) | משכנתא 12,100 (KD 54) · משכנתאות 12,100 · מה זה משכנתא 210 (KD 4) · משכנתא או משכנתה 260 | main 152 @61 | guide set: kantahome x2, Leumi Mortgages, ynet, moti x2, midrag, hon, bizportal, primeinv | short definition block + FAQ; do not build headings around it. Whether a calculator page can rank for the bare word is **unverified** |
| 9 | Olim (Hebrew query) | **/mortgage-calculator/** short section | מחשבון משכנתא לעולים (GSC 52 @54) · משכנתא לעולים חדשים 30 · משכנתא באנגלית 140 | main 52 @54 | not pulled | 2 to 3 lines + link to /en/mortgage-calculator/ (proposed) and /israel-mortgage-non-residents/ |

Intents owned by other pages (the main page summarises in 2 to 3 lines and links with the exact anchor; no H2 that leads with these words):

| # | Intent | Owner URL (answers 200, code) | Evidence | GSC: where the impressions land today |
|---|---|---|---|---|
| 10 | Rates and prime | /mortgage-calculator/mortgage-interest-rates/ | ריבית בנק ישראל 22,200 (KD 10) · ריבית פריים 12,100 (KD 1) · פריים 9,900 · ריבית פריים היום 4,400 · ריבית משכנתא 720 (KD 16) · ריביות משכנתא 720 | **main 172 @45**, owner 97 @47 |
| 11 | Reverse mortgage | /mortgage-calculator/reverse-mortgage/ | משכנתא הפוכה 2,900 (KD 10, CPC 8.88) · מחשבון משכנתא הפוכה 320 (KD 0) · משכנתא פנסיונית 140 | **main 593 @53**, owner about 0 |
| 12 | How much mortgage can I get | /mortgage-calculator/mortgage-repayment-capacity/ | כמה משכנתא אפשר לקחת 210 (KD 10) · כושר החזר משכנתא (KD 45) · תנאים לקבלת משכנתא 70 | **main 513 @58**, owner 0 |
| 13 | LTV, equity, buyer type, self-build | /mortgage-calculator/mortgage-ltv-ratio/ | הון עצמי 720 · כמה הון עצמי צריך למשכנתא 480 · משכנתא לדירה שניה 170 · משכנתא לדירה ראשונה 140 · מחשבון משכנתא לבניה עצמית (GSC 158 @49 on main) | **main 273 @49**, owner 61 @63 |
| 14 | Refinance and early repayment | /mortgage-refinance/ | מחזור משכנתא 1,300 (CPC 10.66) · מיחזור משכנתא 720 · מחשבון מחזור משכנתא 170 (KD 8) · עמלת פירעון מוקדם 70 | **main 156 @36**, owner 2 |
| 15 | Any-purpose loan | /mortgage-calculator/mortgage-for-any-purpose/ | משכנתא לכל מטרה 390 · מחשבון משכנתא לכל מטרה (KD 27) | **main 151 @41**, owner 2 |
| 16 | Mortgage advisor | /mortgage-advisor/ | יועץ משכנתא / יועץ משכנתאות 3,600 (KD 9, **CPC 14.77**) · ייעוץ משכנתאות 880 | about 0 anywhere |
| 17 | Pre-approval | /mortgage-calculator/mortgage-pre-approval/ | אישור עקרוני למשכנתא 1,300 (KD 18) | 1 |
| 18 | Mortgage insurance | /mortgage-home-insurance/ | ביטוח משכנתא 1,000 (CPC 57) | main 21 @46, owner 3 |
| 19 | Investment-property mortgage | /investment-property-mortgage/ | משכנתא לדירה להשקעה (GSC 342 @41) | owner 396 @42; /investment/ 539 @81 |
| 20 | Bridge, porting, refusal, purchase tax, CPI, purchase cost | bridge-loan-apartment, mortgage-porting, mortgage-refusal, /purchase-tax-calculator/, /cpi-calculator/, /apartment-purchase-cost-calculator/ | מחשבון הלוואת גישור 70 · גרירת משכנתא 170 · משכנתא חוץ בנקאית 390 · מחשבון קניית דירה 40 | small |

Not on the main page at all: bank and competitor brand queries (341 keywords, e.g. לאומי משכנתא 9,900, מזרחי טפחות משכנתאות 6,600,
משכנתאמן 4,400); generic loan calculators (מחשבון הלוואה 9,900 KD 1, מחשבון ריבית דריבית 40,500, מחשבון הלוואה שפיצר 1,300; the SERP is
loan sites and card companies). Gaps with no owner page (do not add to the main page; separate decision): state eligibility loans (סבסוד
משכנתאות 880, מחשבון זכאות משכנתא משרד השיכון 140) and process and law (חוק משכנתא 2,400, meaning **unverified**; רישום משכנתא 1,000;
אגרת רישום משכנתא 210).

Autocomplete (10 seeds, `autocomplete/live/advanced`): bank names dominate every seed (פועלים, לאומי, מזרחי, דיסקונט, הבינלאומי). Useful
non-brand completions: מחשבון משכנתא פשוט · לפי החזר חודשי · משרד האוצר · יד 2 · חישוב משכנתא לפי הון עצמי · מחיר למשתכן · סימולטור
החזר משכנתא · סימולטור תמהיל משכנתא · החזר משכנתא 1 / 1.1 / 1.2 / 1.3 / 1.5 / 1.6 / 2 / 2.5 מיליון, 600 / 700 / 800 אלף · לוח סילוקין
שפיצר / הלוואה / משכנתא / קרן שווה / באנגלית · לוח שפיצר מחשבון / נוסחה / דוגמא / אקסל / הסבר · תמהיל משכנתא מומלץ 2026 / לדוגמא /
אופטימלי / בנק ישראל / באנגלית · סכום משכנתא לפי החזר חודשי · חישוב גובה משכנתא לפי החזר חודשי · משכנתא לפי יכולת החזר.

---

## 3. Protect these: keywords our other pages own

The main page must not lead any title, H1, H2 or bare anchor with these. Where the main page mentions them, it is one qualified phrase
plus the exact-anchor link to the owner.

| Owner page | Words it owns |
|---|---|
| /mortgage-calculator/mortgage-interest-rates/ | ריבית משכנתא, ריביות משכנתא, ריבית משכנתא היום, ריבית פריים, פריים, ריבית בנק ישראל, השוואת ריביות משכנתא |
| /mortgage-calculator/reverse-mortgage/ | משכנתא הפוכה, מחשבון משכנתא הפוכה, משכנתא פנסיונית, משכנתא לבני 60 |
| /mortgage-calculator/mortgage-repayment-capacity/ | כמה משכנתא אפשר לקחת, כושר החזר משכנתא, יחס החזר, כמה משכנתא אפשר לקחת לפי משכורת |
| /mortgage-calculator/mortgage-ltv-ratio/ | אחוז מימון משכנתא, יחס מימון, הון עצמי למשכנתא, משכנתא לבניה עצמית, משכנתא לדירה ראשונה / שניה, משפרי דיור |
| /mortgage-refinance/ | מחזור משכנתא, מיחזור משכנתא, מחשבון מחזור משכנתא, עמלת פירעון מוקדם |
| /mortgage-calculator/mortgage-for-any-purpose/ | משכנתא לכל מטרה, משכנתא על נכס קיים, משכנתא שניה |
| /mortgage-advisor/ | יועץ משכנתאות, ייעוץ משכנתאות |
| /mortgage-calculator/mortgage-pre-approval/ | אישור עקרוני למשכנתא |
| /mortgage-home-insurance/ | ביטוח משכנתא |
| /investment-property-mortgage/ | משכנתא לדירה להשקעה, הלוואה לדירה להשקעה |
| /mortgage-calculator/bridge-loan-apartment/, /mortgage-porting/, /mortgage-refusal/ | הלוואת גישור, גרירת משכנתא, מסורבי משכנתא, משכנתא חוץ בנקאית |
| /purchase-tax-calculator/, /cpi-calculator/, /apartment-purchase-cost-calculator/ | מס רכישה, מדד המחירים לצרכן, מחשבון קניית דירה |
| /israel-mortgage-non-residents/ (English) | israel mortgage for foreigners, mortgage in israel for foreigners, non-resident mortgage |

Two current main-page H2s break this rule (code, raw HTML 5.11): **"ריבית משכנתא ממוצעת לפי מסלול ולפי תקופה"** (leads with the rates
child's head term) and **"משכנתא לדירה להשקעה"** (the investment page's head term; `kw_guard` returns WARN for "דירה להשקעה", owner
/investment/). Suggested renames are in section 8.

`docs/seo/protected-keywords.json` is out of step with this map (finding): it lists the owner of "מחשבון משכנתא הפוכה" as
/mortgage-calculator/ (the 25.10 decision gave it to /mortgage-calculator/reverse-mortgage/), and it has no entries for the child-page
terms above (ריבית משכנתא, כמה משכנתא אפשר לקחת, מחזור משכנתא, משכנתא לכל מטרה, אחוז מימון, יועץ משכנתאות), so `kw_guard` cannot warn
on them.

---

## 4. Cannibalization (two or more of our URLs with impressions on one query, GSC 90 days)

`tools/seo/cannibal_check.py gsc-mortgage-sitewide.csv --min 5`:

| Query | URLs (impressions @ position) | Note |
|---|---|---|
| "בדיקת משכנתא" | /mortgage-calculator/ 104 @17 · /investment-property-mortgage/ 18 @23 | and /mortgage-advisor/ uses it in its title ("יועץ משכנתאות: בדיקת משכנתא לפני חתימה") with no impressions. Three pages aim at it; the main page is clearly Google's pick |
| משכנתא לדירה | /mortgage-calculator/ 41 @71 · /investment-property-mortgage/ 30 @55 | the main page's H2 "משכנתא לדירה להשקעה" feeds this |
| הלוואה להשקעה בנדלן | /investment/ 71 @63 · /investment-property-mortgage/ 10 @81 | outside the calculator; logged for the investment owner |
| תמהיל מגורים | /site-map/ 7 · /projects/ 5 | not a mortgage query |

Below the 5-impression line: מחשבון אחוז מימון משכנתא (ltv 2 @41, main 1 @66), mortgage israel calculator (main 2 @43,
/purchase-tax-calculator/ 1 @76), הון עצמי (/investment/ 21, /glossary/return-on-equity/ 2).

**Misrouting (one URL, but the wrong one)**, bigger than the cannibalization itself: 593 reverse-mortgage impressions, 513 "how much can I
borrow", 273 LTV, 172 rates, 156 refinance and 151 any-purpose impressions land on /mortgage-calculator/ while the owner children get 0 to
97. The children are indexed and linked (the main page links each child with the exact anchor, code); they are simply weaker than the
parent for those queries.

---

## 5. What changed since 25.10.2026 (same queries, same tool)

| Query | 25.10 top 10 | 5.11 top 10 | Entered / left |
|---|---|---|---|
| מחשבון משכנתא (desktop) | lemon, nitzanm, Mercantile, topnetglobal, bestie, cmfs, bizportal, machshevon, c14, lahav-f | Hapoalim, Mashcantaman, Mizrahi, Leumi ufapi, Discount, Clal, Leumi Mortgages, Supermarker, Taxo, FIBI | all 10 changed: Google switched desktop to the bank set |
| מחשבון משכנתא (mobile) | nitzanm, Mercantile, Harel servicebank, moti, mym, gemel, omega-f, elhayyad, lahav-f | heshevavoda, Taxo, Harel servicebank, mydira, family-economy, Mercantile, gemel, sbc-il, Discount, goola | stayed: Harel, Mercantile, gemel. Left: nitzanm, moti, mym, omega-f, elhayyad. In: heshevavoda, Taxo, mydira, family-economy, sbc-il, Discount, goola |
| חישוב משכנתא (desktop) | Hapoalim, Mizrahi, Mashcantaman, Leumi ufapi, Discount, Clal, Leumi Mortgages, Taxo, Supermarker | Taxo, mashkanta-center, mydira, ynow, family-economy, gemel, icf, Mercantile, משכנתא.org.il, lahav-f | the reverse switch: this query went from the bank set to the independent set |
| מחשבון משכנתא לפי החזר חודשי (desktop) | Mercantile Mortgages, gadi-leichter, c14, evensapir, myhouse, **nad-lan #6**, hon, family-economy, optimai | moti, heshevavoda, gemel, muhni, i-mashkanta, gadi-leichter, myhouse, evensapir, c14, family-economy | **we left the top 20**; PAA appeared (6 questions) |
| מחשבון החזר משכנתא (mobile) | mym, gemel, berki, family-economy, realfix, mako, myhouse, fullness, tefahot | hoomy, primeinv x2, Mercantile x2, zolo, Leumi ufapi, family-economy, gemel, fullness | in: hoomy, primeinv, zolo, Leumi. Out: mym, berki, realfix, mako, myhouse. **nad-lan #16** |
| כמה משכנתא אפשר לקחת (desktop) | Clal, Supermarker, Mashcantaman x2, shelifinance, meyda, lsmashkanta, kolzchut, muhni | Clal, Discount, meyda, Mashcantaman, alpm, kolzchut, muhni, hon, alonbiran x2 | in: Discount, alpm, hon, alonbiran. Out: Supermarker, shelifinance, lsmashkanta. PAA moved from desktop to mobile |
| מחשבון משכנתא הפוכה (desktop) | itra-plus, mashkanta-hafuha, primeinv, meyda, icf, mortgagebpoint, Taxo, eytanim, midrag | Bank Jerusalem calculator, hon, gov.il, refi, nitzanm, meyda, mortgage-center, pensyoter, credit360, eytanim | 8 of 10 changed; our reverse page is not in the top 20 |

AI overview, head term: on 25.10 it cited Hapoalim, Mizrahi-Tefahot, Leumi ufapi and Mashcantaman; on 5.11 it also cites Harel, Clal,
Menora Mivtachim and Leumi Mortgages (8 sources; Mashcantaman is still the only independent). nad-lan is cited in no AI overview.

---

## 6. Titles Google chooses in Israel

Base: the 158 unique top-10 URLs over the 12 Hebrew queries (both devices), and the 58 unique URLs of the five calculator queries (מחשבון
משכנתא, חישוב משכנתא, סימולטור משכנתא, מחשבון החזר משכנתא, מחשבון משכנתא לפי החזר חודשי). Every result's displayed title, HTML `<title>`
and H1 are in `serp-2026-11-05.json` (`serp_title`, `html_title`, `h1`, `title_check`).

- **Google keeps the page's own title.** Of 158 URLs: 43 identical, 68 the same but truncated, 10 the same with the site name appended,
  4 with the site name dropped, **18 rewritten (11%)**, 15 unknown (bot wall or no title in raw HTML). In the calculator set only 5 of 58
  were rewritten. When Google rewrites, it most often shows the **H1** (hon.co.il, myhouse, finwiz, heshevavoda, fullness, pensyoter) or
  replaces an empty or brand-only title (houseofinance "הבית הפיננסי" became "לוח סילוקין: מה זה, איך בונים ואיך קוראים אותו"; Harel's English
  "Mortgage Calculator" became "מחשבון משכנתא - הראל"). Lesson: keep the H1 close to the title, never leave either generic.
- **Word order:** 32 of 58 calculator titles start with "מחשבון משכנתא" (37 contain it). The common shape is head term, separator, then
  the benefit: "מחשבון משכנתא - חישוב החזר חודשי, ריבית ולוח סילוקין - גמל.נט", "מחשבון משכנתא | חישוב החזר חודשי, ריבית ותקופה - Hoomy",
  "מחשבון משכנתא: החזר חודשי ולוח סילוקין | SBC" (dashes normalised here).
- **"חישוב"** appears in 18 of 58, **"החזר חודשי"** in 19 of 58: the two most common words after the head term.
- **"לוח סילוקין"** in 3 of 58 calculator titles (gemel, sbc-il and one more) but in 20 of all 158; it is the related-search and
  autocomplete term Google pushes for this cluster (מחשבון לוח שפיצר עם לוח סילוקין, לוח סילוקין שפיצר).
- **Year:** "2026" in only 2 of 58 calculator titles (family-economy "מחשבון משכנתא מרובה מסלולים 2026", mydira "מחשבון משכנתא 2026 -
  סימולטור..."), "2025" in 1; 9 of 158 overall. The year is not what wins here; it is optional.
- **Brand position:** at the end in about 27 of 58 ("| SBC", "- גמל.נט", "- Finwiz"); the banks often put the bank first or leave it to
  Google. For our page Google showed "מחשבון משכנתא 2026: החזר חודשי, ריבית ותמהיל | nad-lan - נדלן": Google adds our site name even though
  the title already ends with "| nad-lan", so the tail wastes 9 characters.
- **Length:** displayed titles median 43 characters (calculator set), range 13 to 65; HTML titles median 47.
- **Colon** after the head term in 9 of 58. "בנק ישראל" and "עלות" appear in none, which leaves those two angles open.

---

## 7. What the AI answers say and cite

Full AI-overview text (Hebrew as shown) and every cited URL, per query and device, are in `serp-2026-11-05.json` (`ai_overview.text`,
`ai_overview.cited_sources`). Desktop and mobile show the same overview for every Hebrew query except "משכנתא". AI overview present on all
12 Hebrew queries and all 5 English ones.

Most cited across the Hebrew overviews (desktop): Mashcantaman 7 queries, Mizrahi-Tefahot 6, Leumi Mortgages 5, Hapoalim 5, Leumi ufapi 4,
Clal 4, then YouTube, Discount, Bank Jerusalem, Supermarker, hon, Harel 3 each. nad-lan: 0.

What they say, and how it checks against the verified facts in `docs/research/2026-10-26-upgrades/u1-mortgage-calculator/dna.md` section
6 (primary sources, 25.10.2026; no rate decision has happened since, next one 23.11.2026):

| Statement in the AI answer | Query | Verdict |
|---|---|---|
| Bank of Israel rate 3.25%, prime 4.75% (prime = BoI rate + 1.5) | משכנתא | **correct** |
| LTV: single home 75%, replacement home 70%, investment 50%, any-purpose 50% | כמה משכנתא אפשר לקחת, משכנתא, mortgage in israel | **correct but incomplete**: any-purpose may reach 70% when the part above 50% is at most 200,000 ₪ (directive 329 s.10A) |
| Payment should not exceed 30% to 40% of net income; BoI allows up to 50% | כמה משכנתא אפשר לקחת, לפי החזר חודשי | **correct** (cap 50%; above 40% a 100% risk weight) |
| "Banks usually approve a payment of up to about 35% of disposable income" | חישוב משכנתא, מחשבון החזר משכנתא | **misleading**: in August 2026, 52.6% of new mortgage volume had a payment-to-income of 30% to 40%; the average was 29.23% (BoI) |
| "Monthly payments generally cannot exceed 40% of net income" | mortgage in israel (English) | **wrong**: the cap is 50% (directive 329 s.5) |
| Term "usually 10 to 30 years", "up to 30 years" | חישוב משכנתא, משכנתא (mobile) | **correct** (directive 329 s.8: 30 years) |
| Term "4 to 30 years, or up to 40 at some lenders"; "5 to 30 or 40 years" | מחשבון החזר משכנתא, מחשבון משכנתא | **conflicts** with the 30-year cap for bank housing loans; non-bank lenders **unverified**. PAA also asks "האם ניתן לקבל משכנתא ל-40 שנה?" |
| Prime: "you can put up to a third (sometimes more) in prime" | משכנתא (desktop) | **outdated**: there is no one-third prime cap; the rule is variable part at most 66.66%, so at least one third fixed (directive 329 s.7) |
| "the requirement, in the past, to put at least a third in prime or unlinked" | תמהיל משכנתא | **garbled**: same rule as above |
| Recommended mix "prime 35-36%, fixed unlinked 34-35%, variable unlinked 30%" (from Mashcantaman and Mashkanta Guru, "second half of 2026") | תמהיל משכנתא | **opinion, not a rule**; it does fit the 66.66% variable cap |
| Prime "with no early repayment fee" | תמהיל משכנתא | **mostly correct**: no capitalization fee on tracks whose rate changes at least yearly; the operational fee (up to 60 ₪) and the 0.1% short-notice fee can still apply (Banking Order 2002) |
| Hapoalim calculator: BoI uniform baskets, first and highest expected payment; Leumi: loan amount from a desired payment; Mashcantaman: up to 4 mixes in parallel | head and payment queries | **correct** product descriptions; the baskets and the "highest predicted payment" are required by directive 451 |
| Reverse mortgage: age 55 or 60+, home "usually worth 1 million ₪ or more", no compulsory payment, repaid on sale or death, "early repayment without penalties" | מחשבון משכנתא הפוכה | 60+ correct for Harel (loans from 250,000 ₪); "1 million and up" and "no penalties" **unverified** |
| Foreigners: LTV "50% to 60%" | israel mortgage for foreigners (US) | **wrong** above 50%: a non-resident cannot hold a "single home", so the cap is 50% (directive 329 definitions) |
| Foreigners pay "the same base rates as residents" | same | **unverified** |
| English rates: fixed unlinked 4.70% (15 years) to 4.85% (30), CPI-linked fixed from 3.15%, 5-year variable CPI 3.40% to 3.50%, prime track about 5.0% | israel mortgage rates (IL English) | a broker's snapshot (evensapir), not BoI. BoI official, reporting month 9/2026: unlinked 10 to 15 years 4.61%, over 25 years 4.89%; CPI-linked average 3.49%; fixed CPI August 3.29%. The prime-track average is not published by BoI (**unverified**) |
| Olim get special terms and state-subsidized loans | mortgage in israel (English) | eligibility loans exist (bank disclosure); amounts and 2026 terms **unverified** |

What the overviews reward, so our page must state it in crawlable text with numbers and dates: the list of parameters (amount, term, rate
type, repayment method, payment-to-income), the three BoI baskets, first payment versus highest expected payment, payment-to-loan mode,
Spitzer versus equal principal versus balloon and grace, CPI effect, and the LTV and payment limits. They cite banks plus one deep
independent calculator. Our edge is to state the **current** rules correctly where the AI repeats outdated ones (the one-third prime
myth, the 40% cap, 40-year terms, foreigner LTV 60%).

People also ask (5.11; absent on the head term):
- מחשבון משכנתא לפי החזר חודשי (desktop): איך מחשבים לוח שפיצר? · איך אני יכול לבדוק את יכולת ההחזר שלי למשכנתא? · איך מחשבים ריבית
  דריבית עבור השקעות לעצלנים? · מהו מחשבון הלוואת גרייס? · מהו מחשבון החזר משכנתא? · מה ההבדל העיקרי בין הלוואת גרייס להלוואת בלון?
- כמה משכנתא אפשר לקחת (mobile): כמה כסף צריך להרוויח כדי לקבל משכנתא? · האם ניתן לקבל החזר משכנתא של 1.2 מיליון שקל? · כמה משכנתא
  ניתן לקחת על דירה שנייה? · האם ניתן לקבל משכנתא ל-40 שנה? · באיזה בנק הכי כדאי לקחת משכנתא? · האם ניתן לקבל משכנתא ללא ביטוח חיים?
- תמהיל משכנתא (desktop): איזה תמהיל משכנתא מומלץ לי? · איך בונים תמהיל משכנתא? · plus four repeats of the above.

Related searches on the head term: מחשבון משכנתא פשוט · לאומי · דיסקונט · מזרחי · פועלים · מחשבון החזר משכנתא · מחשבון משכנתא ai ·
ריבית משכנתא. Mobile "people also search": מחשבון הלוואה שפיצר · מחשבון לוח שפיצר עם לוח סילוקין · מחשבון הלוואה פריים · מחשבון שפיצר
משכנתא · מחשבון הלוואת בלון (bank names).

---

## 8. On-page signal plan for /mortgage-calculator/

Current (code, 5.11): title "מחשבון משכנתא 2026: החזר חודשי, ריבית ותמהיל | nad-lan" (54) · H1 "מחשבון משכנתא 2026: החזר חודשי ועלות
כוללת" · 33 H2 · FAQPage with 30 questions · **no BreadcrumbList and no visible breadcrumb** · the crawlable HTML has **0** mentions of
"לוח סילוקין" and "סימולטור" and 1 of "חישוב משכנתא" (the schedule exists only inside the JS tool).

**Title** (recommended, 56 characters, `kw_guard` OK):
`מחשבון משכנתא 2026: חישוב החזר חודשי, תמהיל ולוח סילוקין`
Fallback without the year (51): `מחשבון משכנתא: חישוב החזר חודשי, תמהיל ולוח סילוקין`. Why: head term first (32 of 58 winners), "חישוב" and
"החזר חודשי" are the two words winners add, "לוח סילוקין" is what related searches and autocomplete push and the page does not say yet,
"ריבית" belongs to the rates child, and Google appends our site name by itself. The 25.10 spec said "keep the title, re-test after six
weeks"; the weekly average moved from about 50 in mid-September to about 37 in late October, so this change is a refinement, not a rescue, and the owner may prefer
to wait until early December.

**H1 options** (one H1; each leads with the head term and differs from the title):
1. `מחשבון משכנתא: חישוב החזר חודשי ועלות כוללת לפי מסלולים` (55) recommended
2. keep `מחשבון משכנתא 2026: החזר חודשי ועלות כוללת` (current)
3. `מחשבון משכנתא וסימולטור תמהיל: החזר חודשי, עלות כוללת ולוח סילוקין`

**Meta description** (157, `kw_guard` OK):
`מחשבון משכנתא לפי מסלולים: חישוב החזר חודשי, ההחזר הגבוה הצפוי ולוח סילוקין שפיצר, שלושת הסלים של בנק ישראל ובדיקה אם הריבית שהציעו לכם גבוהה מהממוצע החודשי.`

**Breadcrumb** (visible and BreadcrumbList): `נדל"ן > מחשבון משכנתא` on the main page; on every child `נדל"ן > מחשבון משכנתא > [child]` (the
children already live under /mortgage-calculator/, so the parent is the natural hub and each child gains one more exact anchor
"מחשבון משכנתא" to the main page). There is no calculators hub page; none is needed. Pace: about 13 child pages, not all on one day (owner
rule on sitewide changes).

**First paragraph keyword set** (the current 50-word lead already does most of this): מחשבון משכנתא (first two words) · חישוב · החזר
חודשי · לפי החזר חודשי (payment-first in one clause) · מסלולים / תמהיל · שלושת הסלים של בנק ישראל · ההחזר הראשון והגבוה הצפוי · עלות
כוללת · לוח סילוקין. Not in the lead: ריבית משכנתא, כמה משכנתא אפשר לקחת, משכנתא הפוכה, מחזור משכנתא.

**Synonyms and variants to spread over headings** (one per heading, no phrase twice):
- H2 tool block: `מחשבון משכנתא לפי מסלולים` (keep)
- H2: `מחשבון החזר משכנתא: כמה תשלמו בכל חודש`
- H2: `חישוב משכנתא לפי החזר חודשי: מההחזר שמתאים לכם לסכום ההלוואה`
- H2: `כמה ההחזר על משכנתא של מיליון, מיליון וחצי ושני מיליון` (keep; add 800 אלף and 1.2 מיליון rows)
- H2: `לוח סילוקין למשכנתא: שפיצר, קרן שווה, בלון וגרייס` (replaces "שפיצר, קרן שווה, בלון וגרייס"; add a 12-row crawlable sample)
- H2: `בניית תמהיל משכנתא ושלושת הסלים האחידים של בנק ישראל`
- H2: `השוואת הצעות משכנתא: ההצעה שלכם מול הממוצע של בנק ישראל` (merges the existing moat section; holds "בדיקת משכנתא" in its first line)
- H2: `עלות משכנתא כוללת: ריבית, הצמדה והחזר לכל שקל`
- H3 in body: סימולטור משכנתא · סימולציית משכנתא · מחשבון משכנתא פשוט · מחשבון משכנתאות · משכנתא מחשבון · מחשבון שפיצר משכנתא · מחשבון
  תמהיל משכנתא · החזר חודשי ראשון · ההחזר הגבוה הצפוי · קל"צ, ק"צ, פריים, משתנה כל 5 שנים · יחס החזר מהכנסה (as a phrase, linked)
- Rename to protect children: "ריבית משכנתא ממוצעת לפי מסלול ולפי תקופה" to `הממוצע החודשי של בנק ישראל לפי מסלול ותקופה` (link "ריבית
  משכנתא היום" to the rates child); "משכנתא לדירה להשקעה" to a 2-line note `גם למשקיעים: מה משתנה בחישוב` with the exact anchor
  "משכנתא לדירה להשקעה" to /investment-property-mortgage/; "פירעון מוקדם ומחזור" to 2 lines + link "מחזור משכנתא".

**The 30 questions, as people search them** (source in brackets; "link" = answer in one or two sentences and send to the owner page):
1. מה זה מחשבון משכנתא? (25.10 SERP #1 title; PAA "מהו מחשבון החזר משכנתא?")
2. איך מחשבים משכנתא? (GSC 72 @55, Ads 50)
3. איך מחשבים החזר משכנתא? (Ads 30, KD 21)
4. איך מחשבים לוח שפיצר? (PAA 5.11; autocomplete "לוח שפיצר נוסחה")
5. מה זה לוח סילוקין? (AI overview; autocomplete)
6. מה ההבדל בין שפיצר לקרן שווה? (related "קרן שווה או שפיצר", KD 38)
7. מה ההבדל בין הלוואת גרייס להלוואת בלון? (PAA 5.11)
8. מה זה גרייס במשכנתא? (PAA "מהו מחשבון הלוואת גרייס?"; GSC)
9. כמה החזר חודשי על משכנתא של מיליון שקל? (Ads 70 + 50 + 40 + 40 across phrasings)
10. כמה החזר משכנתא על מיליון וחצי? (Ads 260 "החזר משכנתא 1.5 מיליון"; autocomplete)
11. כמה החזר משכנתא על 2 מיליון? (GSC 54 @51; 25.10 PAA)
12. האם ניתן לקבל החזר משכנתא של 1.2 מיליון שקל? (PAA 5.11, as Google phrases it)
13. כמה משלמים משכנתא בחודש? (GSC 44 @37)
14. כמה עולה משכנתא? (GSC 31; "עלות משכנתא" 171 @40)
15. איך מחשבים משכנתא לפי החזר חודשי? (autocomplete "חישוב גובה משכנתא לפי החזר חודשי")
16. מה ההבדל בין ההחזר הראשון להחזר הגבוה הצפוי? (AI overview feature)
17. מה הם שלושת הסלים האחידים של בנק ישראל? (AI overview, Hapoalim)
18. איך בונים תמהיל משכנתא? (PAA 5.11)
19. איזה תמהיל משכנתא מומלץ לי? (PAA 5.11; autocomplete "תמהיל משכנתא מומלץ 2026")
20. כמה מהמשכנתא אפשר לקחת בריבית משתנה? (corrects the outdated AI "one third prime")
21. איך משווים בין הצעות משכנתא של שני בנקים? (related "השוואת משכנתאות" 260)
22. האם הריבית שהבנק הציע לי גבוהה מהממוצע? (the moat; "בדיקת משכנתא" 104 @17)
23. באיזה בנק הכי כדאי לקחת משכנתא? (PAA 5.11; answer with the BoI averages, no bank ranking)
24. מה יקרה להחזר אם הריבית תעלה באחוז? (existing stress section)
25. האם ניתן לקבל משכנתא ל-40 שנה? (PAA 5.11; answer: banks 30 years, directive 329 s.8)
26. איך אני יכול לבדוק את יכולת ההחזר שלי למשכנתא? (PAA 5.11; link to capacity)
27. כמה כסף צריך להרוויח כדי לקבל משכנתא? (PAA 5.11, 25.10; link to capacity)
28. כמה הון עצמי נדרש כדי לקבל משכנתא? (25.10 PAA; Ads 480; link to LTV)
29. איך עולים חדשים מחשבים משכנתא? (GSC "מחשבון משכנתא לעולים" 52 @54; link to the English pages)
30. איך כותבים, משכנתא או משכנתה? (Ads 260; one line)

Kept out on purpose: "האם ניתן לקבל משכנתא ללא ביטוח חיים?" (PAA; the outside-insurance rule is unverified, so link only to
/mortgage-home-insurance/), "יש מחשבון משכנתא של משרד האוצר?" (Ads 260; gov.il/he/pages/mashkanta-calculator exists in the reverse SERP but
its content was not readable, 403: **unverified**).

---

## 9. English: twin page or not

### Demand (Google Ads, monthly average; Google groups the three calculator spellings into one number)

| Keyword group | Israel (en) | US | UK | Canada | France (fr) |
|---|---|---|---|---|---|
| mortgage calculator israel = israel mortgage calculator = israeli mortgage calculator | **260** | 40 | 10 | 10 | 10 |
| israel mortgage rates = mortgage rates israel = israeli mortgage rates | 90 | 70 | 10 | 10 | 10 |
| mortgage in israel = mortgage israel = israel mortgage = israeli mortgage | 70 | 30 | 10 | 10 | 10 |
| israel prime rate = prime rate israel | 110 | 10 | 10 | 10 | 10 |
| bank of israel interest rate | 90 | 30 | 20 | 10 | 10 |
| mashkanta | 50 | 10 | 10 | 10 | 10 |
| mashkanta calculator · loan calculator israel | 20 · 20 | 10 · 10 | 10 · 0 | 0 · 10 | 0 · 0 |
| buying property in israel | 30 | 50 | 40 | 10 | 10 |
| mortgage calculator (generic, searched in the country) | 720 | 2,740,000 | 450,000 | 368,000 | 6,600 |
| immobilier israel · achat appartement israel · credit immobilier israel | 90 · 10 · 40 | | | | 320 · 70 · 10 |
| israel mortgage for foreigners · olim mortgage israel · mortgage israel calculator shekel · aliyah mortgage | no data (Ads null) | null | null | null | null |

Hebrew speakers also search the English words: "משכנתא באנגלית" 140/month; autocomplete offers "לוח סילוקין באנגלית", "לוח שפיצר
באנגלית", "תמהיל משכנתא באנגלית". KD for the English terms: not returned by DataForSEO Labs (**unverified**).

Search Console (90 days): English calculator queries already reach the **Hebrew** page: israel mortgage calculator 8 @72, mortgage
calculator israel 5 @46, mashkanta calculator 3 @42, israeli mortgage calculator 2 @50, mortgage israel calculator 2 @43, loan calculator
israel 2 @44 (22 impressions, 0 clicks). /israel-mortgage-non-residents/ gets the foreigner queries: israel mortgage for foreigners 203 @63,
mortgage in israel 14 @94, and long questions at positions 1 to 5 (best mortgage lenders for first time home buyers in israel 9 @3, how to get
approved for a mortgage with low down payment in israel 7 @1). Note: "israel mortgage for foreigners" has 203 impressions in 90 days while
Ads returns null, so Ads under-counts this niche.

### Who ranks

- "mortgage calculator israel", Israel English desktop: kamakama.gov.il (BoI rate comparison) · bayitisrael · anglomortgages · isrealestate ·
  icf · Harel servicebank · muhni (a Hebrew page) · **en.comparis.ch (a Swiss calculator)** · liffgroup · a Coldwell Banker listing site.
  AI overview cites Israel Property Hub, First Israel, icf, newkey, sellingisrael and the banks. No PAA.
- Same query, US: creditanalyzer · liffgroup · Harel servicebank · kamakama.app · **ribit.io ("Israel Mortgage Simulator in 5 Languages")** ·
  Google Play x3 · bravomortgage · jerusalemrecenter · Discount. AI overview cites ribit.io, liffgroup, irec.
- "israel mortgage rates" (IL English): BoI x2, evensapir, First Israel, Mizrahi (new immigrants), Nefesh B'Nefesh, Bank Jerusalem, Discount,
  malchimortgages, semerenkogroup ("Israel Mortgage Calculator: Monthly Payment, Tracks..."). PAA present.
- "mortgage in israel" (IL English): Nefesh B'Nefesh x2, Mizrahi, Discount, Hapoalim, BoI, First Israel, altshuler-law, mortgageisrael,
  buyitinisrael. Related searches include "Mortgage in israel calculator".
- "israel mortgage for foreigners" (US): Mizrahi, semerenkogroup, Nefesh B'Nefesh, welcome-israel, First Israel, israelstart, buyitinisrael,
  homeinisrael, aliyahnet. Our page is not in the top 20 (GSC average 63).

A Swiss site, app-store listings and small broker pages in the top 10 mean a weak SERP: a complete English calculator with the Bank of
Israel data has a realistic path to page one (estimate, **unverified** until measured).

### Recommendation

**Yes: an English twin of the main page at `/en/mortgage-calculator/`**, paired by hreflang with `/mortgage-calculator/`, in the site's
existing pattern (code: /asbestos/ and /sde-dov/prices/ carry `hreflang="he"`, `hreflang="en"` to the /en/ copy, and `x-default` to the
Hebrew page).

- URL checks: `url_word_audit.py --token mortgage` = 18 URLs, `--token calculator` = 14 URLs; a run with the live inventory plus both
  candidates found no repeated word inside either candidate. `/en/mortgage-calculator/` adds no new head word: it is the language copy of
  the URL that already owns "mortgage" and "calculator", like /en/asbestos/. The alternative `/en/israel-mortgage-calculator/` would
  re-use "israel" and "mortgage", which /israel-mortgage-non-residents/ already owns: **rejected**. `kw_guard` on the slug: OK (the
  protected list holds no English terms). Whether the URL word law exempts language twins is the owner's call; the /en/ precedents say it does.
- Split with /israel-mortgage-non-residents/:

| Audience and query | Owner |
|---|---|
| israel / israeli mortgage calculator, mortgage calculator israel, mashkanta calculator, shekel / NIS mortgage calculator, amortization in Israel, monthly payment by track | **/en/mortgage-calculator/** (head: title, H1) |
| Israel mortgage rates today, prime, BoI averages (no English rates page exists) | /en/mortgage-calculator/ section, mirroring the Hebrew "numbers of today" strip |
| Olim and English-speaking residents (LTV 75% / 70%, payment-to-income, tracks, the three baskets) | /en/mortgage-calculator/ section, link to the foreigners page |
| Foreigners, non-residents, Israelis abroad (LTV 50%, FX income, cash to close in $, € or £) | **/israel-mortgage-non-residents/** (keeps all foreigner queries) |
| Purchase tax for foreigners | /israel-purchase-tax-foreign-residents/ |

- To keep two English URLs off "israel mortgage calculator", the non-residents page title "Israel Mortgage for Foreigners 2026: Rates, LTV,
  Calculator" should lose the trailing "Calculator" once the twin is live (it gets no calculator impressions today), and its links "Mortgage
  calculator in Hebrew" should point to the twin. Owner's word needed; no URL change and no redirect.
- Twin signals: title `Israel Mortgage Calculator 2026: Payments, Tracks, Schedule` (59) · H1 `Israeli Mortgage Calculator: Monthly
  Payment in Shekels, by Track` · meta `Israeli mortgage calculator in English: monthly payment in NIS by track, Bank of Israel baskets,
  amortization schedule and 2026 rules for residents and olim.` (157). Hebrew track names shown next to the English ones (פריים, קל"צ, ק"צ)
  because English searchers use "mashkanta" and the Hebrew terms.
- French: no French mortgage page now. French-language demand is for buying, not borrowing (immobilier israel 320 in France); "credit
  immobilier israel" is 40 in Israel and 10 in France. The existing /acheter-appartement-israel-2026/ can link to the English twin. Any
  French copy is a ChatGPT prompt for the owner (project law 8).

---

## 10. Findings for the log

1. Child-owned intents land on the main page (about 1,900 impressions in 90 days, section 4). Fix with child-page upgrades and exact
   anchors, never redirects.
2. `docs/seo/protected-keywords.json`: wrong owner for "מחשבון משכנתא הפוכה" and no child-page terms (section 3).
3. Main page: no BreadcrumbList and no visible breadcrumb; none on the children either (code: rates child, non-residents page).
4. Main page: "לוח סילוקין" and "סימולטור" absent from the crawlable HTML; the schedule lives only in the JS tool.
5. Main page H2s "ריבית משכנתא ממוצעת לפי מסלול ולפי תקופה" and "משכנתא לדירה להשקעה" lead with other pages' head terms; the second
   feeds the "משכנתא לדירה" double impressions.
6. Google shows our title as "... | nad-lan - נדלן": the brand appears twice.
7. "בדיקת משכנתא": three of our pages aim at it (main, investment-property, advisor title).
8. /reverse-mortgage/ still answers 404 (code), but no page in the cluster links to it any more (the 25.10 defect is fixed in links).
9. We dropped out of the top 20 for "מחשבון משכנתא לפי החזר חודשי" on desktop (was #6 on 25.10); GSC average for that query over 90 days is
   35.8. One-day SERP snapshots on this cluster swing widely (the head term changed all 10 desktop results within ten days and differs from
   this morning's gap.md pull), so judge by GSC weekly averages, not by a single SERP.

## 11. Unverified

Who ranks for the amount, compare and cost intents (no SERP pulled); English KD; how Ads null relates to real foreigner demand; the
40-year term at non-bank lenders; reverse-mortgage "1 million and up" and "no early repayment penalties"; foreigners' rates equal to
residents'; the prime-track average rate; the content of the gov.il mortgage calculator page; the meaning behind "חוק משכנתא" (2,400);
whether a calculator page can rank for the bare word "משכנתא"; the realistic page-one path for the English twin.
