# Purchase-tax calculator: why position 56, and the upgrade plan

Page: https://nad-lan.co.il/purchase-tax-calculator/ (existing URL, no new URL, no redirect).
Research date: 22 October 2026. Read-only: nothing was changed on the live site.

Retrieval times (UTC, 22.10.2026)
- DataForSEO Google Ads volumes and keyword ideas (Israel 2376, language "iw"): 16:53.
- DataForSEO live SERPs (desktop, Hebrew, depth 20): 16:54:33 to 16:55:08.
- Our page raw HTML (curl, view-source): 16:56. Competitor raw HTML: 16:58. Madlan (403 to curl) via DataForSEO content parsing: 17:03.
- Tax Authority PDFs and the 2026 buyer guide: 17:00 to 17:10. gov.il guide page read in the owner's Chrome: about 17:06.
- Search Console (sc-domain:nad-lan.co.il, 22.7 to 20.10.2026): 16:53. URL Inspection API: about 17:09.

Files in this folder
- `keywords.csv`: 671 purchase-tax keywords with volume, 12-month average, CPC, cluster, intent and our GSC impressions.
- `serps.json`: the 8 SERPs (top 20 organic, People Also Ask, AI Overview text and cited domains, featured snippet, other features).
- `gsc-purchase-tax-pages.csv`: queries for every URL containing /purchase-tax (90 days).
- `gsc-mas-rechisha-queries-all-pages.csv`: every query with "מס" + "רכישה" (or "מס קני", "סימולטור מס", "מיסוי מקרקעין") on any of our URLs.
- `gsc-purchase-tax-calculator-daily-180d.csv`: daily impressions and position of the calculator.
- `gsc-url-inspection-cluster.csv`: index status of the six cluster URLs.

---

## 1. Keywords and intent

Volumes are Google Ads monthly averages (Israel, Hebrew). The whole cluster is 43,940 searches a month: 34,860 informational or tool searches, 7,390 payment or navigation searches that belong to gov.il, and 1,690 for the ambiguous "מס קנייה" (customs tax on goods, mostly not ours).

| Cluster | Volume | Leading terms |
|---|---|---|
| Calculator | 13,920 | מחשבון מס רכישה 4,400 · סימולטור מס רכישה 4,400 · חישוב מס רכישה 1,000 · מחשבון מס רכישה דירה ראשונה 590 · מס רכישה סימולטור 590 · מס רכישה מחשבון 480 |
| Head / general | 8,070 | מס רכישה 6,600 · מס רכישה דירה 90 |
| **Payment and navigation (gov.il)** | **7,390** | תשלום מס רכישה 2,900 · תשלום שובר מס רכישה 1,000 · תשלום מס רכישה מקוון 720 · תשלום מס רכישה באינטרנט 590 · אישור מס רכישה 210 |
| First home, single, upgraders | 3,200 | מס רכישה דירה ראשונה 2,400 · מס רכישה דירה יחידה 260 |
| Second home, investors | 2,350 | מס רכישה דירה שנייה 1,300 · מס רכישה על דירה שנייה/שניה 210+210 · דירה שלישית 90 |
| Brackets and rates | 1,630 | מדרגות מס רכישה 720 · מדרגות דירה יחידה 110 |
| Law and regulations | 1,220 | תקנות מס רכישה 720 · תקנה 11 140 |
| Exemptions and refunds | 1,150 | פטור ממס רכישה 210 · החזר מס רכישה 90 |
| Disabled buyers | 920 | מס רכישה לנכה דירה שנייה 70 · פטור ממס רכישה לנכה 70 · הנחה במס רכישה לנכה 70 |
| Land and commercial | 690 | מס רכישה על קרקע 110 |
| Timing and deadlines | 620 | מתי משלמים מס רכישה 140 · תוך כמה זמן צריך לשלם 110 |
| Gift, inheritance, family | 300 | מס רכישה דירה במתנה 20 · בהעברה ללא תמורה 20 |
| Foreign residents, olim, partial, contractor | 510 | שליש דירה מס רכישה 70 · תושב חוץ 40 · עולה חדש 40 |

Trend: "מס רכישה" peaks in February, July and November (9,900) on deal seasons; "מחשבון מס רכישה" slid from 5,400 (winter) to 2,400 in September 2026.

Payment intent (7,390): the SERP is gov.il, the Postal Bank and the Tax Authority payment system. We should not chase it with a page; one short "how to pay" block with the official link on the calculator page is enough.

---

## 2. What Google shows (8 SERPs, desktop, 16:54 to 16:55 UTC)

**nad-lan.co.il appears in none of the top 20 for any of the 8 terms.**

| Term | 1 | 2 | 3 | AI Overview | PAA |
|---|---|---|---|---|---|
| מחשבון מס רכישה | gov.il income-tax simulator (a mismatch) | maor-law.co.il | purenadlan.co.il | yes | none |
| מס רכישה | kolzchut (olim) | secapp.taxes.gov.il payment | yasmint-law.com | yes | none |
| סימולטור מס רכישה | zamirnadlan.co.il | youtube | shamanu.co.il | yes | none |
| מס רכישה דירה ראשונה | misim.gov.il simulator | gov.il simulator page | kolzchut | yes | none |
| מס רכישה דירה שנייה | misim.gov.il simulator | kolzchut | elkayamlaw.co.il | yes | 6 questions |
| חישוב מס רכישה | misim.gov.il simulator | gov.il simulator page | kolzchut | yes | 6 questions |
| מדרגות מס רכישה | nadlanmaster.co.il | bizportal.co.il | haimasher.com (2024 brackets) | yes | none |
| תשלום מס רכישה | Postal Bank | gov.il payments | kolzchut | yes | 6 questions |

- No featured snippet on any of the 8. Related searches on 7 of 8.
- The "מחשבון מס רכישה" SERP is unstable: at 16:08 UTC the gap-map run recorded nadlanmaster at 1. At 16:54 the gov.il income-tax (salary) simulator ranked 1 and nadlanmaster was out of the top 20.
- Domains that appear most across the 8 SERPs: gov.il (6 SERPs, best 1), kolzchut (6, best 1), nadlanmaster (4, best 1), nadlancenter (4), hon.co.il (4), misim.gov.il (3, rank 1 each time), bizportal (3, best 2), madlan blog (3, best 6), TheMarker supermarker (3).

**AI Overview** appears on all 8. It gives the five single-home brackets "בתוקף עד 15.1.2028", the 8%/10% additional-home brackets, 6% for land or commercial property, and "pay within 60 days". On the first-home SERP it also says the brackets run 16.1.2026 to 15.1.2027, which contradicts the freeze. Cited domains:
- Calculator, simulator and calculation SERPs: gov.il, misim.gov.il, kolzchut.org.il, nadlanmaster.co.il.
- Head term: gov.il, kolzchut, nadlancenter, yusim.
- First home: misim, gov.il, amitvered, lazyinvestor, kolzchut, nadlancenter, themarker.
- Second home: gov.il, elkayamlaw, nadlancenter, ishitrit-law, partouche-law, doron-aharoni.
- Brackets: gov.il, kolzchut.
- Payment: gov.il, kolzchut, elkayamlaw, dabullaw, avocat-en-israel, yusim, magdilim.

**People Also Ask** (found only on 3 SERPs):
- האם ניתן להיות פטור ממס רכישה על דירה שנייה?
- כיצד מחושב מס רכישה?
- האם דירה יחידה פטורה ממס רכישה?
- כמה מס רכישה משלמים על דירה ראשונה?
- מי זכאי לפטור ממס רכישה?
- איך לחשב מס רכישה?
- כיצד משלמים מס רכישה?
- מי חייב במס רכישה?
- איך מחשבים מס רכישה בהעברה ללא תמורה?
- מתי מועד תשלום מס רכישה?
- האם ניתן לבצע העברה ללא תמורה בין בני זוג?
- איך לשלם שובר מס רכישה?

---

## 3. Our Search Console data (22.7 to 20.10.2026)

- `/purchase-tax-calculator/`: 961 impressions, 0 clicks, average position 56.7, 110 queries.
  - Top queries: סימולטור מס רכישה 199 (pos 51) · מחשבון מס רכישה 180 (54.5) · מחשבון מס רכישה דירה ראשונה 96 (53) · מחשבון קניית דירה 68 (67) · חישוב מס רכישה בהעברה ללא תמורה 65 (74).
  - Monthly: June 8 impressions (pos 81) · July 297 (76) · August 452 (51) · September 364 (57) · 1 to 20 October 195 (55). It climbed from 76 to about 55 and has been flat since August.
  - **0 impressions for the head terms**: מס רכישה (6,600), מס רכישה דירה ראשונה (2,400), מס רכישה דירה שנייה (1,300), מדרגות מס רכישה (720), תשלום מס רכישה (2,900). Google treats the page only as a calculator, never as an answer about purchase tax.
- Our other purchase-tax pages get almost nothing. Of 811 impressions on purchase-tax queries across the whole site, 805 go to the calculator.
  - `/real-estate-tax-advisor/purchase-tax-first-home/`: 4 impressions.
  - `/real-estate-tax-advisor/purchase-tax-investor/`: 0.
  - `/real-estate-tax-advisor/`: 0.
  - `/israel-purchase-tax-foreign-residents/` (EN): 1.
  - `/real-estate-tax-advisor/gift-transfer-apartment/`: 18 (on gift queries, pos 77).
- **Index status (URL Inspection API):**

| URL | Status | Last crawl |
|---|---|---|
| /purchase-tax-calculator/ | indexed | **14.9.2026** (the 21.10 rebuild with the four-track tool has not been crawled yet) |
| /real-estate-tax-advisor/purchase-tax-first-home/ | indexed | 29.9.2026 |
| /real-estate-tax-advisor/purchase-tax-investor/ | **URL is unknown to Google** | never |
| /israel-purchase-tax-foreign-residents/ | **crawled, currently not indexed** | 30.8.2026 |
| /real-estate-tax-advisor/ | indexed | 10.10.2026 |
| /apartment-purchase-cost-calculator/ | indexed | 4.10.2026 |

### Our URLs about purchase tax (titles cache built 22.10 19:01, plus the sitemap)

| URL | H1 | SEO title |
|---|---|---|
| /purchase-tax-calculator/ (id 6) | מחשבון מס רכישה: הערכת עלות לפני קניית דירה | מחשבון מס רכישה 2026: דירה יחידה או משקיע |
| /real-estate-tax-advisor/purchase-tax-first-home/ (529) | מס רכישה דירה ראשונה 2026: מדרגות, פטור ודוגמת חישוב | מס רכישה דירה ראשונה 2026: מדרגות ופטור |
| /real-estate-tax-advisor/purchase-tax-investor/ (532) | מס רכישה דירה שנייה ומשקיעים 2026: מדרגות, חישוב והבדלים מדירה יחידה | מס רכישה דירה שנייה ומשקיעים 2026 |
| /real-estate-tax-advisor/ (92) | מיסוי מקרקעין: מס שבח, מס רכישה והיטל השבחה לפני עסקת נדל״ן | מיסוי מקרקעין 2026: מס רכישה, מס שבח והיטל השבחה |
| /israel-purchase-tax-foreign-residents/ (post 4961, EN) | Israel Purchase Tax (Mas Rechisha) for Foreign Residents: 2026 Brackets | — |
| /real-estate-tax-advisor/gift-transfer-apartment/ | (gift transfer) | — |
| /apartment-purchase-cost-calculator/ | מחשבון קניית דירה: כמה כסף צריך באמת כדי לקנות דירה? | — |

**Cannibalization verdict.** There is no live cannibalization: Google gives 99% of the impressions to one page. The real problem is the opposite: the supporting pages are not indexed or not ranking, so the cluster shows Google almost no depth.

The overlap is latent. The calculator's title ("דירה יחידה או משקיע") claims the first-home and investor intents that two dedicated pages own. Both of those pages still teach the old 18-month rule (see the fact list below).

---

## 4. Competitor DNA

Word counts are visible main text without header, footer, nav or aside, measured on the raw HTML. "Density" counts "מס רכישה" occurrences × 2 ÷ words.

### 4.1 gov.il and misim.gov.il, the official simulator (rank 1 or 2 on the first-home, second-home and calculation SERPs; cited by every AI Overview)
- Landing page: https://www.gov.il/he/service/real_eatate_taxsimulator.
  - Title "סימולטור - מחשבון לחישוב מס ברכישת מקרקעין | רשות המסים בישראל". H1 is the same. 306 words. Breadcrumb: gov.il > מסים ותשלומים > אגרות, החזרים ותשלומי מסים.
  - Lists the five single-home brackets "החל מיום 16.1.25 ועד ליום 15.1.28", says use is anonymous, and says the law prevails over the page.
- Tool: https://www.misim.gov.il/svsimurechisha/startPage.aspx (ASP.NET, no H1).
  - Inputs: transaction **date** (date picker, so it covers past bracket sets); property type (דירת מגורים / דירת מגורים יחידה / בנין / קרקע); calculation type (a list of entitlements); value in ₪, in **$**, or "no value, show brackets only"; ownership share as numerator/denominator.
  - A glossary of property types with the single-home definition (1/3 share, inherited 1/2, protected tenancy before 1.1.1997, the family unit, sale within 24 months or 18 months for 1/6/23 to 31/5/25). A video guide.
  - It is missing: no explanation, no deadlines, no comparison, no share or print, and a dated UI.

### 4.2 Kol Zchut, "חישוב מס רכישה (מושג)" (rank 2 or 3 on 4 SERPs; cited by nearly every AI Overview; updated 15.10.2026)
- Title "חישוב מס רכישה (מושג) – כל-זכות". 2,188 words. Density 2.4%. No schema. Arabic and Russian versions.
- H2/H3 outline:
  - מי נחשב רוכש
  - הגדרת דירה יחידה
  - משפרי דיור, with sub-sections for one apartment, for purchase groups, and for two apartments
  - חישוב המס למי שרכשו חלק מדירה
  - שיעורי המס לדירה יחידה, one H3 per bracket with a worked 2.4M example, and פטור והנחה לנכים
  - additional-home rates with history 2020 to 2023
  - agricultural farm
  - land and commercial 6% with the 1/6 refund
  - refund for overpayment
  - official sources
- Strengths: every rule has dates, including the 2024 to 2026 war extensions for upgraders and for new residents. Official PDFs are linked (Tax Authority instructions 1/2025, 2/25, 2/2026).
- Gaps:
  - No calculator.
  - No payment section on this page.
  - The additional-home rates are labelled "עד 10.02.2027" with no source given. The Tax Authority says 31.12.2026.

### 4.3 nadlanmaster.co.il, "מחשבון מס רכישה" (rank 1 for מדרגות, 4 for מס רכישה, 10 for חישוב; cited by AI Overview)
- Title "מחשבון מס רכישה מעודכן (2026) ✔️ ידידותי ונוח לשימוש". H1 "מחשבון מס רכישה".
- Meta: "מחשבון מס רכישה - איך מחושב גובה מס הרכישה ... מדרגות מס רכישה מעודכנות 2026 וכיצד לחשב >>".
- Published 16.12.2021, modified 27.12.2025. 1,685 words. **Density 8.7%** (73 times). 296 internal links. Schema: WebPage only, no FAQ, no breadcrumb.
- Tool: a JavaScript "calculated fields form" (also not in the raw HTML). Inputs are price and first or second-plus.
- Outline:
  - a table of contents
  - מה זה מס רכישה
  - מהו מחשבון
  - איך משתמשים
  - מדרגות 2026
  - חישוב דירה ראשונה / שנייה
  - דירה יחידה ומקבלן
  - בניין
  - נכס מסחרי
  - קרקע
  - מתנה / ללא תמורה
  - מי זכאי להנחה
  - after these, project promo blocks
- Opening: it defines the tax as a tax on buyers of any property, anchored in section 9(a), "paid within about 60 days".
- Errors:
  - Disabled threshold 1,744,505 and oleh threshold 1,842,155 (both 2020/2021 figures).
  - "Foreign residents get 0.5%" (false).
  - "Brackets update every year by the housing index", with no freeze.
  - "מעודכן עד 31.12.2026".
- It wins on age, the exact-match H1, heavy keyword use and site authority, not on accuracy.

### 4.4 bizportal.co.il, article 20035184 (rank 2 for מדרגות; published 6.7.2026, modified 9.7.2026)
- Title and H1 "מס רכישה: כמה תשלמו באמת על הדירה, ואיפה מסתתרות ההקלות". Meta mentions the calculator and "קפואות עד תחילת 2028". 1,725 words. Schema NewsArticle and BreadcrumbList.
- Embedded calculator:
  - Purchase type: single / additional / commercial-land.
  - A slider from 300K to 12M in 10K steps, plus a number field.
  - Outputs the tax, the effective rate and the total cost.
  - It documents its own fields in a table.
- Price-point tables for each track (1.5M to 10M+: tax, effective rate, total cost).
- An 18-question Q&A, including:
  - האם המדרגות מתעדכנות ב-2026
  - כמה על דירה נוספת ב-2 מיליון
  - עולה, נכה, משפר דיור
  - מתי משלמים
  - מה קורה אם השווי חוצה מדרגות
  - שנייה מול שלישית
  - קרקע
  - ערעור על שומה
  - מתנה וירושה
- A sister article (Sept 2026, 20041446) covers the 2027 additional-home expiry.

### 4.5 purenadlan.co.il/purchase-tax-calculator/ (rank 3 and 5; BlogPosting, 27.8.2026)
- Title "מחשבון מס רכישה 2026 - כמה מס משלמים בקניית דירה?". 2,694 words. Density 4.5%.
- Server-rendered calculator:
  - Track cards: single / upgrader / additional.
  - Price field and **price chips** (1.5M, 2M, 2.5M, 3M, 5M).
  - Results for single and for additional side by side, and a per-bracket table.
- Tables: single brackets, additional brackets, a scenario table, a 6-price example table (single vs additional), and a costs table.
- Mistake sections: first vs single, forgetting the tax, assuming upgraders always qualify, third and fourth homes.
- 8 FAQs: does it replace advice, second/third/fourth, first vs single, upgraders, when to pay, is the tax in the mortgage, why before an offer, can 2026 brackets change.
- Mentions the 2028 freeze. Lead-form heavy.

### 4.6 maor-law.co.il (rank 2 and 6 and 12 on the calculator SERP: three URLs)
- `/calculators/purchase-tax`: H1 "מחשבון מס רכישה". 480 words. WebApplication + BreadcrumbList schema.
  - Server-rendered form: price, "do you own another apartment", "will you live in it", "Israeli resident".
  - Sections "ארבע שאלות, וזהו" and "מה המחשבון לא עושה" (honest limits).
- A hub of about 20 sub-calculators: first home, single, additional, second, gift transfer (העברה ללא תמורה), cooling-off period for gifts, payment schedule, equity, delivery-delay compensation.
- This is the model for "one tool, many entry points".

### 4.7 Also present
- nadlancenter.co.il/article/3824: 1,841 words, density 9.6%, NewsArticle, "המדריך השלם לשנת 2026". Old rules, no 2028 freeze.
- madlan.co.il blog: about 820 words parsed. It says the brackets change every 16 January (no freeze) and gives an outdated 18-month upgrader rule (since 1.6.2025 it is 24 months).

### What every competitor gets wrong or leaves out
- The **additional-home 8%/10% rate is a temporary order that ends 31.12.2026** (Tax Authority instruction 1/2026). Nobody's calculator says it. Bizportal covers it in a separate article.
- **Upgrader windows** are date-dependent and were extended twice by war laws. Madlan, nadlanmaster and our own first-home and investor pages still say 18 months.
- **Olim**: two regimes, plus a price cap. Regulation 12A applies to a single home up to 20,183,565 ₪. Regulation 12 applies to anyone who arrived before 15.8.2024 and covers any apartment. No commercial calculator has either.
- **Disabled buyers** (regulation 11, the 2.5M rule): missing from every calculator.
- Payment timeline, declaration, objection and refund: only Kol Zchut, spread over three pages.

---

## 5. Our page today (raw HTML, 16:56 UTC)

| Item | Ours |
|---|---|
| Title | מחשבון מס רכישה 2026: דירה יחידה או משקיע \| nad-lan |
| Meta | מחשבון מס רכישה 2026 לדירה יחידה, דירה נוספת או משפרי דיור: מדרגות עדכניות, חישוב לפי מחיר הדירה וקישורים למדריכי מס רכישה. |
| H1 | מחשבון מס רכישה: הערכת עלות לפני קניית דירה (one H1) |
| Breadcrumb | none in schema |
| Words | 2,272 main text (2,787 with chrome). Density 2.9% (33 times), the lowest of the commercial competitors |
| Schema | WebPage, SoftwareApplication (Offer), FAQPage (4 Q), Organization, WebSite. No BreadcrumbList |
| Dates | published 27.5.2026, modified 21.10.2026 17:28 |
| Tool in raw HTML | **none**: an empty `div.nli-host[data-nli=ptax]`, filled by `instruments/core.js` + `tools/ptax.js` + `data/ptax.json` |
| Tool (JS) | price, track (single / additional / oleh / foreign), share %. Outputs: tax, effective rate, last-shekel bracket, price of the share, difference against single, all 4 tracks side by side, per-bracket table, formula, source. Share bar (copy, WhatsApp, print) in the engine. The engine supports presets; ptax defines none |
| Page weight | HTML 220 KB. 20 external scripts (incl. Stripe, WooCommerce, paid-member-subscriptions, Hotjar, GTM) and 15 stylesheets on a tax calculator |
| Links in | sitewide nav + cluster: home (5 links), cost calculator (5), first-home (4), investor (4), hub (4), gift transfer (3), foreign EN (3). Anchors almost always "מחשבון מס רכישה" / "מס רכישה" |

Answer paragraph today (paraphrased): the single-home brackets, additional and foreign 8%/10%, an example at 3M (45,538 against 240,000), and "בתוקף מ־16.1.2025 ומוקפאות עד 15.1.2028". It is good and close to what AI Overview shows.

H2 outline today:
- מחשבון
- מס רכישה הוא חלק מהתקציב
- מהו מס רכישה
- מדרגות לדירה יחידה
- איך להבין את החישוב
- מה צריך להכין
- דירה יחידה, נוספת וחלופית
- מס רכישה בדירה מקבלן
- טעויות נפוצות
- משכנתא
- מתי צריך עורך דין
- FAQ (4 generic questions)
- בדיקה מהירה
- סיכום
- כלי המשך

### Point by point against the leaders

| Element | Ours | Kol Zchut | nadlanmaster | bizportal | purenadlan | gov simulator |
|---|---|---|---|---|---|---|
| Exact-match H1 | partial | no | yes | no | yes | yes (סימולטור) |
| Calculator visible in raw HTML | no | n/a | no | yes | yes | yes |
| Tracks | 4 | n/a | 2 | 3 (incl. land) | 3 (incl. upgrader) | all, by date |
| Disabled / gift / land in the tool | no / no / no | — | no | land only | no | yes |
| Transaction date / bracket history | no | history text | no | no | no | yes |
| Price chips or slider | no | — | no | slider | chips | no |
| Price-point example table | no | 1 example | no | yes | yes | no |
| 2028 freeze stated | yes | yes | no | yes | yes | yes |
| Additional-home expiry 31.12.2026 | **no, says frozen to 2028** | says 10.2.2027 | no | separate article | no | no |
| Upgrader windows correct (24/18/12 + war) | no ("18 months") | yes | partly wrong | vague | vague | 24/18 |
| Deadlines (30-day declaration, 60 days, s.51) | no | other page | 60 days only | when to pay | when to pay | no |
| Objection, refund, how to pay | no | other pages | no | objection | no | no |
| FAQ | 4 generic | — | none | 18 | 8 | — |
| Breadcrumb schema | no | — | no | yes | no | — |

---

## 6. Why we are at 56 (causes, strongest first)

1. **Google is ranking the old page.** The last crawl was 14.9.2026. The four-track tool and the current text went live on 21.10 and have not been seen. Whether to request indexing is Ben's decision; nothing was requested.
2. **The page does not answer the purchase-tax question, only the calculator one.** It has 0 impressions for מס רכישה, first home, second home, brackets and payment. The text is generic and hedging: "what to prepare", "when to call a lawyer", "this guide does not replace advice". The facts that the SERP and AI Overview quote are missing: deadlines, upgrader windows, disabled and olim rules, land, gifts, refund, objection, payment. Kol Zchut, bizportal and nadlanmaster each carry these facts.
3. **A young page on a domain with no tax depth in Google's eyes.** It is 5 months old against nadlanmaster (2021), gov.il and Kol Zchut. The supporting cluster is invisible: the investor page is unknown to Google, the foreign-residents page is crawled but not indexed, the first-home page has 4 impressions and the hub has 0.
4. **Accuracy defects that a careful reader, or a rater, sees:**
   - The extra and foreign tracks are labelled "frozen to 15.1.2028", but they are a temporary order to 31.12.2026.
   - The single-track note says 18 months for upgraders; it is 24 months for purchases since 1.6.2025, and war extensions apply.
   - The oleh track applies 12A above 20,183,565 ₪, where it does not apply.
   - No regulation-12 option for olim who arrived before 15.8.2024.
   - No disabled track.
   - The first-home and investor guides repeat the 18-month rule.
5. **The tool is invisible in raw HTML, and the page carries shop scripts.** Maor-law, purenadlan and bizportal serve the form and the tables in HTML. Ours is an empty div and 20 scripts. Google renders JavaScript, so this is a secondary factor, not the main one.
6. Smaller items: no BreadcrumbList; only 4 FAQ questions with no PAA overlap; the lowest keyword density among the commercial pages (2.9% against 4.5% to 9.6%). Do not stuff, but the headings should carry the real search phrases.

---

## 7. Official facts for the upgrade (every fact with its source)

| # | Fact | Official source |
|---|---|---|
| F1 | Single home (individual, Israeli resident), purchases 16.1.2025 to 15.1.2028: 0% up to 1,978,745 ₪; 3.5% up to 2,347,040; 5% up to 6,055,070; 8% up to 20,183,565; 10% above. The amounts were set 16.1.2024 and frozen for 2025 to 2027 by the Economic Efficiency Law 2025 | Tax Authority instruction 1/2026, 18.1.2026 https://www.gov.il/BlobFolder/policy/inst-01-2026/he/realestate_inst-01-2026.pdf · instruction 1/2025, 16.1.2025 https://www.gov.il/BlobFolder/policy/inst-01-2025-3/he/realestate_inst-01-2025-3.pdf · https://www.gov.il/he/service/real_eatate_taxsimulator |
| F2 | A home that is not a single home (an additional home; any buyer who is not an individual Israeli resident, so foreign residents and companies): **temporary order s.9(c1f)** for purchases 16.1.2025 to **31.12.2026**: 8% up to 6,055,070 ₪, 10% above | instruction 1/2026 section 2b; instruction 1/2025 section 1 |
| F2a | UNVERIFIED: the order runs on to about 10.2.2027 because of the Knesset elections (Basic Law: The Knesset), then the new government decides. If it lapses, lower investor brackets return (starting at 5%; exact amounts not found in an official text) | Kol Zchut "חישוב מס רכישה" (no source given); bizportal 20041446 (Sept 2026). Check the Tax Authority before publishing any 2027 number |
| F3 | Oleh, regulation 12A (single home; purchase from a year before aliyah to 7 years after): 0 up to 1,978,745; 0.5% up to 6,055,070; 8% up to 20,183,565. **Above 20,183,565 ₪ the relief does not apply** | instruction 1/2026 section 2c and footnote 1 |
| F3a | Oleh, regulation 12 (business; and an oleh who arrived before 15.8.2024 may choose it for any apartment, even a non-single one, with no price cap): 0.5% up to 1,988,090 ₪, 5% above | instruction 1/2026 section 2c; Kol Zchut "הנחה במס רכישה לעולים" for the before-15.8.2024 choice |
| F4 | Disabled, blind, hostile-action victims, families of fallen soldiers (regulation 11): 0.5% of the value, granted twice only. For a single home up to 2,500,000 ₪: exempt up to the first bracket, 0.5% on the rest. Spouses: if one is entitled, both are calculated under the regulation (also if married within 12 months). Form 2973 | Tax Authority buyer guide 2026, p.52 https://www.gov.il/BlobFolder/generalpage/guide-for-seller-right-in-land/he/Guides_knowrightinland_2026.pdf (page updated 06.08.2026) |
| F5 | Upgraders are treated as single-home buyers if they sell the previous home within **24 months** (**18 months** for purchases 1.6.2023 to 31.5.2025), or within 12 months of receiving a new home from a contractor, whichever is later. If not sold in time they pay the difference plus linkage and interest; if they paid as additional and sold in time, they get a refund | guide 2026 p.50-51; official simulator glossary https://www.misim.gov.il/svsimurechisha/startPage.aspx; Kol Zchut |
| F5a | War extension ("שאגת הארי", 28.2 to 31.5.2026): a deadline whose period touches that window by even one day moves to the later of 31.8.2026 or the original end plus 3 months. Examples in the instruction: bought 1.9.24, sell by 31.8.26; bought 30.4.25, sell by 31.1.27; bought 1.6.25, sell by 1.9.27; contractor home received 31.12.25, sell by 31.3.27. Same rule for "becomes a resident within 2 years" | instruction 2/2026, 30.3.2026 https://www.gov.il/BlobFolder/policy/inst-02-2026-1/he/realestate_inst-02-2026.pdf. Kol Zchut also lists earlier 2024-25 extensions (21/27/15 months); reconcile before coding |
| F6 | Single-home definition: the buyer, spouse or partner and children under 18 count as one buyer. Not counted: a share of 1/3 or less in another home; an inherited share of 1/2 or less; a home under protected tenancy before 1.1.1997. A buyer who becomes a resident or returning resident within 2 years counts as a resident | guide 2026 p.50; official simulator glossary |
| F7 | Partial purchase: the tax is calculated on the whole home's value and multiplied by the share bought | guide 2026 p.51 |
| F8 | Land and non-residential property: 6% (since 1.8.2013). Land with a plan for at least 1 home and a permit within 2 years is reassessed at 5% | guide 2026 p.50 |
| F9 | Gift to a relative (regulation 20): 1/3 of the regular tax. Relatives: spouse, parent, descendant, grandchild, great-grandchild, descendant's spouse, sibling. Gift of a home to a spouse living there with the giver (regulation 21): exempt | guide 2026 p.52 |
| F10 | Declaration: the buyer files within **30 days** of the purchase (s.73(c)), form 7000, online through a lawyer. Late filing: an administrative fine of 5% of the tax plus linkage and interest; plus 310 ₪ (declaration) or 250 ₪ (notice) per two weeks late, for 16.1.2026 to 15.1.2027 | guide 2026; instruction 1/2026 section 1b |
| F11 | Payment: by self-assessment. The legal date (s.51) is the earliest of possession, payment of over 50%, or a power of attorney to register, **and never before 60 days from the transaction**. Deferral carries linkage and interest. A balance under the director's assessment is due within 15 days; under objection, pay the undisputed part within 30 days | guide 2026 (s.51, s.91) |
| F12 | How to pay: the Tax Authority real-estate payment system https://www.misim.gov.il/svMSMKTashlumim/frmTashlumChovot.aspx?cur=1 (ID, internet number and assessment number from the voucher), or the Postal Bank with the voucher. Instalments carry linkage and interest. The Land Registry approval comes only after full payment. UNVERIFIED: a credit-card cap of 50,000 ₪ (from AI Overview) | Kol Zchut "תשלום מס רכישה" (links to the official system); gov.il payments page https://www.gov.il/he/pages/payments-services |
| F13 | Assessment: a self-assessment notice within 20 days; the director assesses within 8 months; objection within 30 days on form 7013; appeal committee within 30 days; amendment within 4 years (form 7085) | guide 2026 p.53-54 |
| F14 | Refund check for past over-payment: https://secapp.taxes.gov.il/svStatusShuma/frmHechzer.aspx | Kol Zchut (official app link); gov.il https://www.gov.il/he/Departments/publications/reports/pa-260818 |
| F15 | A new home from a contractor: the tax is on the price **including VAT** | Kol Zchut "חישוב מס רכישה" (a court ruling). Not found in the ITA documents read; mark as Kol Zchut |

Our current numbers check out: 3,000,000 ₪ gives 45,538 (single), 240,000 (additional) and 5,106 (oleh 12A). 10,000,000 ₪ gives 513,886 (single), 878,899 (additional) and 335,976 (oleh).

---

## 8. Recommendation: upgrade the existing URL

### 8.1 The three strings (checked 22.10 with `tools/title_start_audit.py --skip https://nad-lan.co.il/purchase-tax-calculator/`)

| | String | Length | Check |
|---|---|---|---|
| SEO title | **מחשבון מס רכישה 2026: סימולטור לכל קונה ומדרגות המס** | 51 | OK |
| (alternative title) | מחשבון מס רכישה 2026: דירה יחידה, נוספת, עולה ונכה | 50 | OK, once the disabled track exists |
| H1 | **חישוב מס רכישה על דירה: מדרגות 2026, מסלולים ומועד תשלום** | 56 | OK |
| Breadcrumb | **מחשבון מס רכישה** | 15 | OK; the trio check passes (three different strings) |

- Rejected: "מס רכישה" as the breadcrumb. It clashes on the 2-word start with the first-home and investor pages.
- The title takes the 4,400 "סימולטור" term (our top GSC query) and drops "או משקיע", so it stops claiming the investor page's intent.

### 8.2 Answer paragraph (directly under the H1; replaces the current one)
> מס רכישה על דירה יחידה ב־2026: אין מס עד 1,978,745 ₪, ומעל זה 3.5%, 5%, 8% ו־10%, כל שיעור רק על החלק של המחיר שנופל במדרגה שלו. על דירה נוספת, לתושב חוץ ולחברה: 8% מהשקל הראשון עד 6,055,070 ₪ ו־10% מעל. דירה ב־3,000,000 ₪: מס של 45,538 ₪ כדירה יחידה, 240,000 ₪ כדירה נוספת ו־5,106 ₪ לעולה חדש. מדרגות הדירה היחידה מוקפאות עד 15.1.2028; השיעור על דירה נוספת הוא הוראת שעה עד 31.12.2026. מדווחים לרשות המסים תוך 30 יום מהחתימה, ומשלמים בדרך כלל עד 60 יום מיום העסקה.

- Sources: F1, F2, F3, F10, F11.
- Move the Kikar HaMedina 10M example into the examples section; do not remove it (additive law).

### 8.3 Sections to add, in rendered order: H1, answer, CTAs, tool, then these
1. **טבלת מדרגות מס רכישה 2026 לכל המסלולים.** One table: single, additional/foreign/company, oleh 12A, oleh 12, disabled, land/commercial. Include an "in force until" column (15.1.2028 / **31.12.2026** / 15.1.2028 / 15.1.2028 / — / —) and a source line with the instruction 1/2026 link. Facts F1 to F4, F8. Server-render it.
2. **כמה מס רכישה משלמים: דוגמאות לפי מחיר.** Rows 1.5M, 2M, 2.5M, 3M, 4M, 6M, 10M. Columns single, additional, oleh, disabled (single up to 2.5M), with the effective rate. Generate it from `NLPT.tax` so it matches the tool. The Kikar example goes here.
3. **מה יקרה למס הרכישה על דירה נוספת ב־2027.** State the official 31.12.2026 end date (F2). Add one clearly labelled line: "דווח שההוראה תמשיך לחול עד אחרי הבחירות (בדיקה מול רשות המסים)" (F2a). No invented numbers. No competitor calculator has this; it is our freshness edge for the 2,350 second-home cluster.
4. **מי נחשב "דירה יחידה".** Family unit, 1/3 share, inherited 1/2, protected tenancy, becoming a resident within 2 years plus the war extension (F6, F5a).
5. **משפרי דיור: כמה זמן יש למכור את הדירה הקודמת.** 24 / 18 / 12-months-from-possession; the war extension with the four official examples; what happens if you miss it (difference plus interest) and the refund if you paid as additional (F5, F5a). Link to `/mortgage-calculator/bridge-loan-apartment/`.
6. **מס רכישה לעולה חדש.** 12A against 12, the window, the 20.18M cap, couples, form 2973 (F3, F3a, F4 spouses). Link to the EN foreign page.
7. **הנחה במס רכישה לנכה.** Regulation 11, the 2.5M rule, twice in a lifetime, spouses, form 2973 (F4). Covers the 920-search disabled cluster, which no calculator covers.
8. **תושב חוץ ותושב חוזר.** Additional rates; single only if the buyer becomes a resident within 2 years (F2, F6). Link to `/israel-purchase-tax-foreign-residents/` and `/israel-mortgage-non-residents/`.
9. **דירה מקבלן.** Price includes VAT (F15); payment is deferred to possession or over 50% paid (F11); the 12-months-from-possession upgrader window (F5). Link to `/buying-new-apartment-developer-2026-negotiation/`.
10. **מתנה, העברה ללא תמורה וירושה.** 1/3 for relatives, exemption for a spouse living there (F9). Link to `/real-estate-tax-advisor/gift-transfer-apartment/`. GSC shows "חישוב מס רכישה בהעברה ללא תמורה" landing on this page (65 impressions, pos 74).
    - UNVERIFIED: whether receiving an inheritance itself carries purchase tax. Check the law before writing it.
11. **קנייה של חלק מדירה או עם שותפים.** Whole value × share (F7), and the 1/3 rule.
12. **קרקע, מגרש ונכס מסחרי.** 6%, and 5% with a permit within 2 years (F8). Link to `/investment/residential-land-investment/`.
13. **מתי ואיך משלמים מס רכישה.** A dated timeline:
    - signing
    - declaration within 30 days (form 7000, through a lawyer)
    - self-assessment notice within 20 days
    - payment: s.51, never before 60 days
    - director's assessment within 8 months
    - objection within 30 days
    - Plus the official payment link (F12), linkage and interest, and the 5% and 310/250 ₪ fines (F10, F11, F13). Covers the 620-search timing cluster and catches part of the 7,390 payment searches without competing with gov.il.
14. **שומה, השגה והחזר מס רכישה.** F13, F14.
15. **היסטוריית מדרגות.** 2020 to 2026, a small table. Data to collect from Tax Authority instructions 1/2020 to 2/2024 (Kol Zchut has the additional-home and oleh thresholds for 2020 to 2024). Not collected in this run.

Keep the current "טעויות נפוצות" and "משכנתא" sections, rewritten with the facts above. Shorten the "מה צריך להכין" and "מתי צריך עורך דין" hedging.

### 8.4 FAQ (replace the 4 generic questions; FAQPage schema; questions in searchers' words)
1. איך מחשבים מס רכישה על דירה?
2. כמה מס רכישה משלמים על דירה ראשונה?
3. האם דירה יחידה פטורה ממס רכישה?
4. האם אפשר לקבל פטור ממס רכישה על דירה שנייה?
5. מי זכאי לפטור או להנחה במס רכישה?
6. מתי משלמים מס רכישה, ותוך כמה זמן?
7. איך משלמים את שובר מס הרכישה?
8. איך מחשבים מס רכישה בהעברה ללא תמורה?
9. האם העברה ללא תמורה בין בני זוג פטורה ממס רכישה?
10. מה יקרה למס הרכישה על דירה נוספת אחרי 31.12.2026?
11. קניתי דירה חדשה ועוד לא מכרתי את הישנה: כמה מס אשלם?
12. האם מס רכישה על דירה מקבלן מחושב כולל מע״מ?
13. כמה מס רכישה משלם עולה חדש?
14. האם נכה משלם מס רכישה על דירה שנייה?
15. קניתי חצי או שליש דירה: איך מחושב המס?
16. האם יש הבדל בין דירה שנייה לדירה שלישית?
17. כמה מס רכישה משלמים על קרקע או מגרש?
18. איך מקבלים החזר מס רכישה?
19. אפשר לערער על שומת מס רכישה?

Questions 1, 3, 4, 5, 6, 7, 8 and 9 are verbatim or near-verbatim PAA. The others come from bizportal and purenadlan Q&A and from keyword ideas.

### 8.5 Tool (ptax) improvements
1. **Validity per track** in `ptax.json`: add `valid_until` per track (single 2028-01-15, extra and foreign **2026-12-31**, oleh 2028-01-15). Change the strip "המדרגות מוקפאות עד" so it does not apply to extra and foreign. Show a notice for extra and foreign: "הוראת שעה עד 31.12.2026".
2. **Fix oleh:** above 20,183,565 ₪, 12A does not apply, so calculate as single (F3). Add a sub-option "עליתי לפני 15.8.2024" for regulation 12: 0.5% up to 1,988,090, 5% above, also for an additional home (F3a).
3. **Add a disabled track** (regulation 11): single home up to 2.5M gives 0 up to 1,978,745 and 0.5% on the rest; otherwise 0.5% of the whole value (F4).
4. **Upgrader mode with a deadline date.** Input the purchase date and contractor yes/no plus the possession date. Output "sell by" under F5 and F5a and the cost of missing it (the difference between additional and single). No competitor has this. Fix the single-track note "18 חודשים" now (24 months from 1.6.2025).
5. **Add tracks**: land/commercial 6% (with "permit within 2 years gives 5%"), and gift to a relative at 1/3 (F8, F9). This covers the maor-law gift calculator and our 65 GSC impressions on that query.
6. **Transaction date** (like the official simulator): choose the bracket set by date. At minimum, warn when the date is 1.1.2027 or later for extra and foreign.
7. **One-tap presets** (the engine already supports `preset`):
   - דירה ראשונה 2.5 מ׳
   - משפרי דיור 3.5 מ׳
   - משקיע 2 מ׳
   - עולה חדש 4 מ׳
   - דירה מקבלן 3 מ׳ כולל מע״מ
   - חצי דירה 2 מ׳
   - נכה, דירה יחידה 2.4 מ׳
8. **Price chips and a slider** (1.5M, 2M, 2.5M, 3M, 4M, 6M, 10M), as purenadlan and bizportal have.
9. **The result as a decision line**: price + tax = total. Cash needed on top of the price. A link to `/apartment-purchase-cost-calculator/` with the price carried over. Keep the share and print bar, and make the shared link reopen the same inputs (check the engine).
10. **Server-render a static fallback** inside `.nli-host`: field labels, the brackets table and the example table, so the raw HTML carries the tool, like maor-law, purenadlan and bizportal.
11. **Page weight:** check whether Stripe, WooCommerce and the paid-member-subscriptions scripts are needed on tool pages; dequeue them if not (20 scripts and 15 stylesheets today).

Schema: add BreadcrumbList (בית > מיסוי מקרקעין > מחשבון מס רכישה). Keep SoftwareApplication and FAQPage. Keep dateModified honest.

### 8.6 Internal links
Pages that should link to the calculator, contextually, with varied anchors, one page per release (no sitewide mass change):

| Page | Anchor |
|---|---|
| /real-estate-tax-advisor/purchase-tax-first-home/ | סימולטור מס רכישה לדירה יחידה (single preset) |
| /real-estate-tax-advisor/purchase-tax-investor/ | חישוב מס רכישה לדירה נוספת (investor preset) |
| /real-estate-tax-advisor/gift-transfer-apartment/ | חישוב מס רכישה בהעברה ללא תמורה |
| /mortgage-calculator/bridge-loan-apartment/ | מס רכישה למשפרי דיור |
| /buying-new-apartment-developer-2026-negotiation/ | מס רכישה על דירה מקבלן |
| /investment-property-cashflow-calculator/ | מס רכישה על דירה להשקעה |
| /investment/investment-via-company/ | מס רכישה לחברה |
| /investment/residential-land-investment/ | מס רכישה על קרקע |
| /israel-mortgage-non-residents/ | מס רכישה לתושב חוץ |
| /apartment-purchase-cost-calculator/ | already links; vary to "מדרגות מס רכישה 2026" |

Pages the calculator should link out to: first-home, investor, gift transfer, foreign residents (EN), cost calculator, capital-gains guide, bridge loan, the hub.

### 8.7 Pages to re-target (never redirect)
- **First-home guide** owns "מס רכישה דירה ראשונה / יחידה" (2,660) and the upgrader detail.
  - Fix the 18-month rule (F5, F5a).
  - Point the "מחשבון מס רכישה" H2 to the calculator with the single preset; do not duplicate a full calculator.
- **Investor guide** owns "מס רכישה דירה שנייה / נוספת / שלישית" (2,350) and the 2027 expiry.
  - Fix the "כלל 18 החודשים" heading.
  - It is unknown to Google: check that the sitemap and internal links reach it. Requesting indexing is Ben's call.
- **The calculator** owns "מחשבון / סימולטור / חישוב מס רכישה" (13,920), the head "מס רכישה" (6,600), "מדרגות" (1,630) and timing (620).
- **The hub** `/real-estate-tax-advisor/` owns "מיסוי מקרקעין".

### 8.8 Release notes for whoever builds it
- Page loop law: one page per release. Run `tools/source_audit.py` before and after, and `tools/content_first_check.py`. Spot-check rainbow and h-infinity.
- Facts table F1 to F15: the source lines stay in the repo (this file); the page carries one short source line, not citation clutter.
- Before going live, re-check F2a (the 2027 status) against the Tax Authority.

---

## 9. DataForSEO spend
- About $0.31 in total:
  - search volume via MCP, about $0.09 (estimated)
  - search volume via script, $0.09
  - keyword ideas, $0.09
  - 8 live SERPs, $0.032
  - 3 content-parsing fetches, $0.0045
- Account balance after the run: $26.07 (includes other sessions' spend).
