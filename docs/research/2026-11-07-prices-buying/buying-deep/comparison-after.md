# Comparison after the build: /buying-apartment/ (Phase 1 live in 1.72.607; Phase 2 local, 8.11.2026)

- **Our column is counted on the built page**, not a target: `docs/research/2026-11-07-prices-buying/page-9-new.html` rendered through the real shortcode (`tools/instruments/build_buying_harness.py`) and pressed in headless Chrome at 390 and 1366 (`tools/instruments/shot_buying.py`, all checks pass). Phase 1 (4 tools) is live since 1.72.607; Phase 2 (6 more tools, PDF) is local, prepared as 1.72.608 (dry run only).
- Competitor cells are copied from `comparison-grid.md` (observed 7.11.2026, desktop only); nothing about them was re-measured.
- Mobile here means a 390 px headless Chrome, not a real phone. Rankings and AI citations can only be filled two to four weeks after release.
- Counting rules: words = server-rendered text (head + tool summaries + article), before JS adds the tool surfaces; figures = numbers with % or ₪ in that text, each tied to a named, dated source.

## A. Against Israel's top 5
| Parameter | Us before (7.11) | **Us now (Phase 1 + 2, counted)** | Amit Vered | Yoni Levy | Elkayam | ygoldlaw | gov.il | Who wins |
|---|---|---|---|---|---|---|---|---|
| Depth (words) | ~2,650 | **7,053** | ~17,000 | ~2,000 | ~14,600 | ~3,000 | 270 + booklet | **Amit Vered, Elkayam** (we are third) |
| Interactive tools inside the guide | 0 | **10** (plan, equity sources + handover test, equity ladder, offer, compare 2 to 4 flats, buy before sell, deadline calendar, visit sheet, who pays what, benefits) | 0 | 0 | 1 link | 0 | 0 | **us** |
| Buyer statuses handled | none | **12**, each with its tax brackets, LTV and programmes | – | – | developer only | – | developer buyers | **us** |
| Personal memory | – | plan, compare list and visit sheets kept in the browser | – | – | – | – | – | **us** |
| Numbers with source and date | few | **213** figures | caps in text | unsourced | one example | some rates | – | **us** |
| Deadlines | – | 8-row table + **calendar file (.ics)** from the signing date; unverified deadlines left out and said | – | – | in prose | – | – | **us** |
| Who pays what (second-hand) | – | 8 rows, each with a law or official source; contract-only items named without a row | – | – | – | in prose | – | **us** |
| Benefits routing | – | 13 programmes by status and toggles, each with its gov.il page and date | – | – | – | – | **the source** | **gov.il** (we route to it) |
| Printable / downloads | – | **"הדפסה או שמירה כ־PDF"** on the plan, calendar, comparison, visit sheet and who-pays table (a real PDF of the visit sheet was produced in the test); .ics | – | ruling PDFs | a PDF | – | booklet + checklist PDF | **tie with gov.il** (they have an official booklet; we have personal printouts) |
| FAQ + schema | 5 Q, no FAQPage | **19 Q** in FAQPage + 10 SoftwareApplication | FAQPage | FAQPage, Person | FAQPage, Person | none | none | **us on volume** |
| Article / Person schema | WebPage | not added | Attorney | Article, Person | BlogPosting, Person | WebPage | – | **Yoni Levy, Elkayam** |
| Author / reviewer | unverified lawyer line | **no named reviewer** (the unverified line was removed) | named lawyer | named lawyer | named lawyer | law office | the Ministry | **all four law sites** |
| Every live link kept | – | **yes: 0 missing**; 72 unique internal links | – | – | – | – | – | – |
| Mobile (390) | n/m | pressed, no sideways scroll, CTAs inside 2 viewports | n/m | n/m | n/m | n/m | n/m | **us** (only one measured) |
| Video | – | – | – | – | – | – | – | nobody |
| Top 10 / AI citations | 0 / 0 | after release only | #1 on 5 / 10 | top 10 on 11 / 12 | #1 "מקבלן" / 7 | #1 "מה לבדוק" / 4 | top 10 on 10 / 10 | **all of them, today** |

## B. Against the top 4 abroad
| Parameter | **Us now** | Bankrate | Rightmove | Redfin | NerdWallet | Who wins |
|---|---|---|---|---|---|---|
| Affordability → places | 24 cities × rooms | budget step | MIP → search | calculator | calculator | **us** |
| Buy before sell | **planner: bridge, tax window, double months, 3 months late** | – | chains guide | guide + "will selling pay off" | – | **us** (Redfin close) |
| Offer strategy | offer helper with data | step 7 | guide | 6 tips | n/m | **us** |
| Compare candidate homes | **2 to 4 flats side by side** | – | saved properties | favourites | – | **us** on cost; **Rightmove** on listings |
| Viewing checklist | **visit sheet, saved, printable** | – | viewing guide | – | – | **us** |
| Help programmes | 13 programmes routed | first-time programmes | **every scheme its own guide** | – | n/m | **Rightmove** (depth per scheme) |
| Pre-approval | guide links only | personalised offers | **lender-backed MIP** | partner lender | lender comparison | **Rightmove** |
| Accounts across devices | browser only | building one | **My Rightmove** | account | **sign-in** | **Rightmove, NerdWallet** |
| Glossary / moving toolkit | – | – | **both** | 17 things | – | **Rightmove** |
| Freshness | dated blocks | **daily edits** | n/m | 28.4.2026 | n/m | **Bankrate** |

## C. Honest reading
**We beat every observed column on:** tools inside the guide (10 vs 0 to 1), the buyer's own case, equity turned into places, buy-before-sell math, a sourced deadline calendar, a sourced who-pays table, a visit sheet that remembers, dated numbers everywhere, and FAQ volume.

**We still lose on:** text depth (7,053 words against ~17,000 and ~14,600); a named professional author or reviewer and Person/Article schema (the law sites); lender-backed pre-approval and cross-device accounts (Rightmove, NerdWallet); scheme-by-scheme guides, a glossary and a moving toolkit (Rightmove); an official downloadable booklet (gov.il); daily freshness (Bankrate); and rankings and AI citations until release (everyone).

**Left out on purpose (no official dated source today):** the up-to-₪50,000 second-hand grant (the gov.il guide answered 403 on 8.11.2026, and nothing showed the lottery is open); National Insurance disability grants; IDF rehabilitation help; a legal deadline for the warning note; the eligibility-loan current rate; who pays registry fees, house committee and utilities until handover (contract only, named without a row).

**Still not built:** T5 payment caps (caps not verified), T7 tabu-status decoder, T8 deviation risk score, T9 ownership structure, T12 developer card, T13 address check, T15 registration-form check, T16 clause list, T17 signing-day kit, T18 handover protocol, T23 receiver guide, T25 inline glossary.
