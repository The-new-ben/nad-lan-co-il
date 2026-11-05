# Which page to strengthen: gap analysis, 5.11.2026

Ben asked for a keyword with high search volume and high value, where we rank poorly and the owner page already exists with no
cannibalization, and where the searcher is on the way to buying or selling. He wants that page strengthened hard.

## Pick: /mortgage-calculator/ ("מחשבון משכנתא")

| Fact | Number | Source |
|---|---|---|
| Monthly volume, head term | 33,100 (27,100-40,500 over 12 months) | DataForSEO Google Ads, 5.11 |
| Close variants | חישוב משכנתא 1,600 · משכנתא מחשבון 1,600 · מחשבון החזר משכנתא 590 · לפי החזר חודשי 590 · חישוב החזר משכנתא 480 | same |
| Difficulty | KD 11 (low) | keyword_opportunities_2026-11-04.csv |
| Our live rank for the head term | 28 (page 3) | DataForSEO SERP, google.co.il desktop, 5.11 |
| Impressions in 3 months | 9,141 · 1 click · 367 different queries | GSC 4.8-3.11 |
| Weekly average position | 52 (July) → 37 (since the 2.0 release of 26.10) | GSC by date |
| Cannibalization | none on the head term; the reverse-mortgage queries (468 + 109 impressions) land on the parent instead of /mortgage-calculator/reverse-mortgage/ | GSC query × page |

## Content is not the gap

| Page | Rank | Words | Tool |
|---|---|---|---|
| taxo.co.il | 1 | 424 | payment, max loan, period |
| heshevavoda.co.il (loan schedule) | 2 | 348 | schedule |
| topnetglobal.co.il | 3 | 354 | basic + lead form |
| mydira.co.il | 4 | 419 | by payment / by amount |
| family-economy.co.il | 5 | 72 | multi-track |
| gemel.net | 9 | 1,288 | tracks, schedule, FAQ |
| **nad-lan.co.il** | **28** | **7,705** | 3 tracks, up to 4 mixes side by side, Bank of Israel directive 329, 3 charts, yearly or monthly schedule, max loan, shareable link |

## The real gaps

1. **Authority.** We have 36 backlinks from 29 domains: all .com, none from an Israeli site, spam score 51, first seen 3.7.2026.
   mydira.co.il has 5,066 backlinks from 105 domains (3,717 of them from .co.il), first seen 2019 (DataForSEO backlinks summary, 5.11).
   The same pattern shows on the other money pages: /dira-behanacha/ has 17,563 words and 62 impressions in 3 months;
   /purchase-tax-calculator/ has 8,664 words and an average position of 55.
2. **Page weight.** Our page is 325 KB of HTML with 49 scripts and 95 KB of inline CSS. The rivals' pages are 10-90 KB. PageSpeed was
   not measured (the API answered 429 without a key).
3. **Overlap with our own child pages.** The parent repeats the rates section (owner /mortgage-calculator/mortgage-interest-rates/)
   and the reverse-mortgage content (owner /mortgage-calculator/reverse-mortgage/).
4. **What the results page asks for.** The related searches are לוח שפיצר, לוח סילוקין, מחשבון הלוואה פריים. Our tool has the
   schedule, but the title does not say it.
5. **Money path.** "יועץ משכנתאות" has a CPC of 14.77 USD against 1.35 for the calculator. /mortgage-advisor/ had 2 impressions in
   3 months, and no path leads from a calculator result to an advisor check.

## Plan (each step needs Claude Design first; steps 1 and 2 need Ben's word on outreach and pace)

1. **The writing topic that earns links:** a monthly figure no rival publishes, "how much a mortgage of one million shekels costs this
   month", by track, from the Bank of Israel series we already pull (HAD-531). It sits on the calculator page as a short dated block
   with a citable chart. Journalist and forum outreach happens only on Ben's word.
2. **Internal links:** project and listing pages link to the calculator with the anchor "מחשבון משכנתא", about 10 pages a day,
   never sitewide in one day.
3. **A lighter page:** the long rates and reverse-mortgage sections are replaced by a short summary and a link to the child page that
   already owns each topic. No new URL and no redirect.
4. **Title:** add "לוח סילוקין".
5. **Value:** a quiet "בדיקת משכנתא עם יועץ" step after the result, leading to /mortgage-advisor/.

## Why not the bigger keywords

- **דירה בהנחה + מחיר למשתכן** (60,500 + 90,500 a month). Google's top results are gov.il, the registration companies and news sites,
  and our 17,563-word page is not in the top 30. Same authority wall, a longer road.
- **מס רכישה.** The Tax Authority's own simulator holds places 1, 2 and 7.

## Finding for the log

DataForSEO counts 85 broken pages on nad-lan.co.il (backlinks summary, 5.11). The list was not pulled.
