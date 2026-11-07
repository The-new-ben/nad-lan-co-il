# Comparison after the build: /buying-apartment/ Phase 1 (local, 8.11.2026)

- **Our column is counted on the built page**, not a target: `docs/research/2026-11-07-prices-buying/page-9-new.html` rendered through the real shortcode (`tools/instruments/build_buying_harness.py`), pressed in headless Chrome at 390 and 1366 (`tools/instruments/shot_buying.py`, all checks pass). Competitor cells are copied from `comparison-grid.md` (observed 7.11.2026, desktop only); nothing about them was re-measured.
- **Not live.** Rankings, AI citations and real-phone checks can only be filled after release. Mobile here = a 390 px headless Chrome, not a real phone.
- Counting rules: words = server-rendered text (head + tool summaries + article), before JS adds the tool surfaces; "sourced numbers" = figures with % or ₪ in that text, each tied to a named, dated source on the page.

## A. Against Israel's top 5
| Parameter | Us before (live 7.11) | **Us after (built, counted)** | Amit Vered | Yoni Levy | Elkayam | ygoldlaw | gov.il | Who wins |
|---|---|---|---|---|---|---|---|---|
| Depth (words) | ~2,650 | **5,477** (article 4,276 + summaries 910 + head) | ~17,000 | ~2,000 | ~14,600 | ~3,000 | 270 + booklet | **Amit Vered and Elkayam** (we are third) |
| Stage skeleton | topic H2s, 5-row table | 7 stages, 36 steps, each with the professional and an owner-page link (in the tool, filtered by status and type) | 13 H3 stages | 5 H2 | 49 headings | 10 checks | booklet | **us** (only one that adapts to the buyer) |
| Buyer statuses handled | none | **12**, each with its own purchase-tax brackets, LTV and eligibility items | – | – | developer only | – | developer buyers | **us** |
| Interactive tools inside the guide | 0 (lead form) | **4 tools, 5 functions** (plan, equity sources, handover stress test, equity ladder, offer helper) + links to 6 existing calculators | 0 | 0 | link to an index calculator | 0 | 0 | **us** |
| Personal plan that remembers | – | **yes** (browser only, nothing sent) | – | – | – | – | – | **us** |
| Numbers with source and date | few | **154** % or ₪ figures, each with source and date (Tax Authority, BoI, Ministry of Construction, CBS, regulations) | caps in text | unsourced | one worked example | some rates | – | **us** |
| Deadlines table | – | **8 rows, each at an official source**; the AI's 30 / 40 / 60 contradiction named; unverified deadlines left out | – | – | in prose | – | – | **us** |
| Eligibility-loan amounts | – | official table (54,240 to 161,665 ₪), service, reserve, disability, Negev | – | – | – | – | **the source** | **gov.il** (it is the source; we route to it) |
| Equity → places | – | 24 cities × 3/4/5 rooms against the max price | – | – | – | – | – | **us** |
| Offer basis | – | median, lowest of 4 quarters, neighbourhood share, district index; no invented discount | – | – | – | – | – | **us** |
| Freshness | "2026" in title | data date on every block; refresh from the instrument files | "(2026)" | 5.5.2026 | 16.8.2026 | 5.3.2025 | n/m | **us** |
| FAQ + schema | 5 Q, no FAQPage | **17 Q** from autocomplete language, FAQPage (module) + 4 SoftwareApplication | FAQPage | FAQPage, Person | FAQPage, Person | none | none | **us on volume; they have Person** |
| Article / HowTo / Breadcrumb schema | WebPage, Organization | not added in Phase 1 (Yoast's own graph unchanged) | Attorney | Article | BlogPosting | WebPage | – | **Yoni Levy, Elkayam** |
| Author / reviewer | site brand ("כתוב ונבדק על ידי עורך דין" line, unverified) | **no named reviewer**; the unverified lawyer line was taken out | named lawyer | named lawyer | named lawyer | law office | the Ministry | **all four law sites** |
| Printable / downloads | – | print my plan (browser print); no PDF, no calendar file, no spreadsheet | – | ruling PDFs | a PDF | – | booklet + checklist PDF | **gov.il, Elkayam** |
| Video | – | – | – | – | – | – | – | tie (nobody) |
| Human layer | "טעויות נפוצות" | 8 FAQ answers on fear, family, wedding, faith calendar, war, receiver, no broker | warnings | "טיפ זהב" | "כבדהו וחשדהו" | – | – | **us** |
| Official primary links | some | gov.il calculator + mortgage guide, Tax Authority, BoI series, CBS, regulations (in tool sources) | – | – | – | – | **the source** | **gov.il** |
| Every live link kept | – | **yes: 0 of the live page's links missing**; 68 unique internal links | – | – | – | – | – | – |
| Mobile (390) | n/m | pressed, no sideways scroll, CTAs at 836 px (inside 2 viewports) | n/m | n/m | n/m | n/m | n/m | **us** (only one measured) |
| Visible top 10 / AI citations | 0 / 0 | not measurable before release | #1 on 5 / 10 | top 10 on 11 / 12 | #1 "מקבלן" / 7 | #1 "מה לבדוק" / 4 | top 10 on 10 / 10 | **all of them, today** |

## B. Against the top 4 abroad
| Parameter | **Us after (built)** | Bankrate | Rightmove | Redfin | NerdWallet | Who wins |
|---|---|---|---|---|---|---|
| Opening move | head term + the equity answer with the median and the monthly payment, then 4 CTAs | why buy + takeaways | "what you could afford" | buying power box | n/m | **tie** with Rightmove/Redfin |
| Affordability → places | **24 cities × rooms** | budget step | MIP → search | calculator | calculator | **us** (places by budget) |
| Pre-approval | guide links only | personalised offers | **lender-backed MIP** | partner lender | lender comparison | **Rightmove** |
| Purchase costs | sourced cost table + links to our cost and purchase-tax calculators | calculators | Stamp Duty calculator | – | closing-costs calculator | tie |
| Buy before sell | FAQ + plan step + bridge-loan link (no planner yet) | – | chains guide | **guide + "will selling pay off"** | – | **Redfin** |
| Offer strategy | **offer helper with data** | step 7 | guide | 6 tips | n/m | **us** |
| Help programmes | eligibility-loan table and routing; grants without numbers (not verified) | first-time programmes | **every scheme its own guide** | – | n/m | **Rightmove** |
| Personal account / memory | plan remembered in the browser | building one | **My Rightmove** | account | **sign-in** | **Rightmove, NerdWallet** (cross-device) |
| Viewing checklist / glossary / moving | – (Phase 2: T21, T25, moving list) | – | **all three** | 17 things | – | **Rightmove** |
| Freshness | dated blocks | **daily edits** | n/m | 28.4.2026 | n/m | **Bankrate** |
| FAQ schema | yes (17) | yes | n/m | FAQ section | n/m | tie |

## C. Honest reading
**We now beat every observed column on:** tools inside the guide (4 vs 0), the buyer's own case (12 statuses, plan that remembers), equity turned into places, an offer basis from closed deals, the sourced deadlines table, and dated numbers in every block.

**We still lose on:** text depth (Amit Vered ~17,000 and Elkayam ~14,600 words against our 5,477); a named professional author or reviewer (all four law sites); Article/Person schema; downloads (PDF, calendar file, spreadsheet: gov.il and Elkayam have PDFs); lender-backed pre-approval (Rightmove); cross-device accounts (Rightmove, NerdWallet); scheme-by-scheme help guides, viewing checklist, glossary and moving toolkit (Rightmove); a buy-before-sell planner (Redfin); daily editorial freshness (Bankrate); and, until release, rankings and AI citations (everyone).

**Not yet covered from the bill of materials (Phase 2):** ownership structure as a tool (T9), receiver and execution-office guide (T23), Amidar, heirs and foreign-seller cases, developer registration form (T15), Sale Law payment caps (T5, caps not yet verified), developer card (T12), address check (T13), visit scorecard (T21), compare 2 to 4 flats (T22), deadline calendar file (T24), glossary inline (T25), benefits finder with the grant rules verified (T19), who-pays-what (T11), buy-before-sell planner (T10).
