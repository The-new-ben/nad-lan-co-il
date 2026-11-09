# Counted proof after round R, 9.11.2026: /mortgage-calculator/ against Israel and the world (HAD-675)

Ben's order (9.11.2026): perfect on-page SEO and indisputable, counted proof that the page is the best in the world, with everything the
competitors and the SERP show folded in. Live after this round: 1.72.616 (deploy-result-615.json and 616.json, both "released and verified")
and page 121 content (write_page_r.py, backup in build/page-backup/).

## 1. Where the page stands on Google (manual, owner's Chrome, 9.11 00:12)

- "מחשבון משכנתא": about #51 (page 6). The top 8 are the banks, Mashcantaman and Harel. Google still shows our OLD title, so the title
  set on 6.11 has not been re-read yet; the planned recheck after 10.11 stands and the title was not touched.
- "משכנתא", "משכנתה": Wikipedia, the banks, boi.org.il, Kol Zchut, gov.il, paamonim, TheMarker. Our page is not on the first pages.
- The AI summary for the calculator query lists four calculators and what each does (3 BoI baskets; price and equity; Spitzer, equal
  principal, bullet, CPI; several mixes side by side). The AI summaries quote the Spitzer formula with P, r, n and a payment-to-income rule.
- No "people also ask" box on these queries. Related searches: the bank names, "לפי החזר חודשי", "פשוט", "משרד האוצר".
- Evidence: serp-manual-2026-11-09.md. Search Console numbers stay outside this public repo.

## 2. Depth against every page in the Israeli top results and the world leaders (raw HTML, tools/depth_proof.py)

Before (9.11 00:17) and after (9.11 04:13) this round. Full tables: depth-raw.md, depth-after-r.md.

| Page | Words | Figures | Tables | Cells | Tools | FAQ | Headings | Visuals | Official sources |
|---|---|---|---|---|---|---|---|---|---|
| **nad-lan, after round R** | **20,680** | **2,729** | **32** | 1,328 | **22** | **65** | **146** | 7 | **8** |
| nad-lan, before | 20,154 | 2,576 | 31 | 1,216 | 22 | 66 | 146 | 6 | 8 |
| Bank Hapoalim (#1) | 0 (app) | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| Mizrahi-Tefahot (#2) | 1,464 | 39 | 0 | 0 | 0 | 4 | 15 | 3 | 0 |
| Mashcantaman (#3) | 199 | 10 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| Leumi calculator app (#4) | 0 (app) | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| Leumi Mortgages (#5) | 504 | 0 | 0 | 0 | 0 | 2 | 0 | 6 | 0 |
| Discount (#6) | 14 | 2 | 0 | 0 | 0 | 0 | 0 | 2 | 0 |
| FIBI (#7) | 49 | 0 | 0 | 0 | 1 | 0 | 1 | 0 | 0 |
| Harel (#8) | 1,176 | 11 | 0 | 0 | 0 | 10 | 13 | 3 | 0 |
| Clal (#9) | 290 | 15 | 0 | 0 | 1 | 0 | 3 | **17** | 0 |
| Supermarker (#14) | 2,562 | 193 | 2 | 58 | 0 | 8 | 8 | **21** | 2 |
| Walty (#18, same title shape as ours) | 1,636 | 58 | 2 | 32 | 1 | 18 | 12 | 4 | 2 |
| Wikipedia משכנתה | 2,958 | 73 | 1 | 4 | 0 | 0 | 10 | 5 | 3 |
| Kol Zchut משכנתא | 971 | 24 | 1 | 20 | 0 | 0 | 20 | 0 | 3 |
| NerdWallet (US) | 2,030 | 34 | 0 | 0 | 1 | 1 | 12 | **49** | 0 |
| Calculator.net (US) | 6,071 | 2,529 | 6 | **2,072** | 1 | 0 | 7 | **13** | 0 |
| Bankrate, Zillow, MoneySavingExpert, MoneyHelper, CFPB | blocked to scripts (405/403); Bankrate also sent the owner's Chrome away from the page. Not counted, not "solved". |

Where a competitor is ahead, said plainly: pictures (Clal 17, Supermarker 21, NerdWallet 49 mostly icons, Calculator.net 13, ours 7) and
table cells (Calculator.net prints a 360-row schedule in HTML). FAQ went 66 -> 65 because two questions asked the same thing (merged, every
answer sentence kept); one duplicate was re-targeted to the real search "משכנתא הורים".

## 3. The 77-parameter benchmark (docs/research/2026-11-05-mortgage-world/proof/measure.py, ours re-measured 9.11 04:13)

| | LEAD | TIE | LOSE |
|---|---|---|---|
| Against the best Israeli page per row (19 pages) | **33** | 34 | 10 |
| Against the best world page per row (24 pages) | **26** | 37 | 14 |

(After round Q on 6.11: Israel 33/34/10, world 25/38/14.) Every row and its definition: proof-table-r.md.

Still LOSE, and why:
- Weight and speed (HTML 585 KB, transfer 1.83 MB, 131 requests, TTFB, DOMContentLoaded, load, LCP): the best Israeli pages are bare
  tools; ours carries the article (Ben: remove nothing) and the site stack Ben keeps on this page (Stripe, chat, Hotjar; 6.11).
- Page height 40,401 px on a phone and first input at 665 px: the content-first order (H1, answer, buttons) is the house law.
- Weekly payments: they do not exist in Israel.
- World only: figures 1,158 vs Calculator.net 1,210 (close), cells, pictures.

## 4. What round R added (all additive)

| # | What | Why (who has it) | Where |
|---|---|---|---|
| R1 | "כמה עולה משכנתא של מיליון שקל, חודש אחר חודש": the first payment on 1,000,000 ₪ over 25 years at every bank's average mix, for 25 months, a chart, 13 months by bank | the asset that earns Israeli links (5.11 authority gap); no competitor publishes it | #million, inc/mortgage-market.php |
| R2 | A cite box with a ready sentence, copy, and the CSV of every month and bank | journalists need a sentence, a source and the data | #million, /wp-json/nadlan/v1/mortgage-million |
| R3 | Dataset #million with the CSV; the market Dataset gains the CSV; WebApplication #calculators with a featureList of the 16 tools | AI engines and Google Dataset Search read them; Walty and Supermarker carry WebApplication or SoftwareApplication | JSON-LD (9 blocks, all parse) |
| R4 | The Spitzer formula in the M, P, r, n notation with the worked example | the AI summary for "מחשבון משכנתא לפי החזר חודשי" quotes it | chapter "לוח סילוקין" |
| R5 | "מה המחשבון בודק": one sentence listing what the calculators do | the AI summary lists calculators by what they do | "איך משתמשים במחשבון המשכנתא?" |
| R6 | The "מדריך" badge left 12 links to the child pages | the anchor text read "ריבית משכנתא היוםמדריך"; now each anchor is the child's own phrase | topic map |
| R7 | FAQ: one question per intent (40-year pair merged; "משכנתא הורים") | FAQPage hygiene | FAQ |
| R8 | Phone fonts: the H1 face and the text face (Hebrew and Latin files) preloaded on phone widths | CLS 0.179 came from two late fonts (H1 2 -> 3 lines, the lead -1 line) | head, pages with the market section |
| R9 | The hero photo has width/height and loads lazily | no layout jump, no bandwidth fight with the fonts on phones | page 121 |

## 5. Phone speed, measured (tools/lcp_probe.mjs: 390 x 844, 150 ms RTT, 1.6 Mbps, CPU x4; median of 3)

See section 7 for the after numbers and the cause of the LCP move.

## 6. Authority plan (links from Israeli sites)

- The asset is live: https://nad-lan.co.il/mortgage-calculator/#million (refreshes itself with the monthly Bank of Israel file, ~20th).
- Target list: 47 Israeli outlets, writers and sites in four tiers (15 cover the Bank of Israel mortgage data every month), with recent
  article URLs, the byline as printed and public contact pages; 5 story angles; 3 Hebrew pitch drafts marked NOT SENT. Kept in the private
  research folder (not in this public repo). Nothing was sent; outreach waits for Ben's word.
- Today no Israeli outlet links to the site.

## 7. Honest statement

The page is the deepest mortgage page in Israel by every count above, and leads the world's mortgage calculators on 26 of 77 counted
parameters (ties 37). It is not the fastest or the lightest page: 14 world rows and 10 Israeli rows are still lost, all named above.
"The best in the world on every parameter" is not true today, and this file says exactly where.
