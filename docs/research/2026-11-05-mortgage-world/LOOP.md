# MORTGAGE LOOP: the best mortgage-calculator page in the world (HAD-675, Ben 5.11.2026)

**Ben, 5.11.2026 evening.** Upgrade the mortgage calculator page "without excuses, as if it were the best in the world".
- **Research:** look at the world's leading calculators, the Hebrew results and searches abroad, and the competitors' DNA.
- **Tools:** startup-grade practical tools (not more calculators), plus many numbers, calculations and proposals.
- **The page:** an image; a simple phone experience that is accessible, with no table-of-contents menus.
- **Search signals:** every signal says "מחשבון משכנתא" (title, breadcrumbs, synonyms, intent) without repetition.
- **Proof:** dozens of parameters showing we beat every page in the world.
- **English:** an English version that does not collide with the Hebrew page.
- **Process:** a loop with no self-granted discounts.

**Owner page:** https://nad-lan.co.il/mortgage-calculator/ (page 121, tool `mortgage`, data `boi-mortgage.json`).
**English owner today:** /israel-mortgage-non-residents/ (post 4962, foreigners).
**History:** October research is in `../2026-10-26-upgrades/u1-mortgage-calculator/` (dna.md, proof-after.md). Mortgage 2.0 went live in 1.72.523.

## Baseline (5.11.2026, Chrome pane at 375 x 812, code evidence)

| Measure | Value |
|---|---|
| Page height | 52,588 px, about 64.8 phone screens |
| First input | at 1,495 px, about 1.8 screens down |
| Mortgage 2.0 panel | from 491 to about 13,296 px (about 16 screens) |
| Content | 33 H2, 15 tables, 10 details, 20 SVG |
| Calculators | 3 on the page: Mortgage 2.0 plus 2 older ones |
| Weight | 325 KB HTML |
| Google | position 28 for the head term (DataForSEO), 9,141 impressions and 1 click in 3 months |
| Backlinks | none from Israeli sites |

## Board (status: todo / doing / done / waits-Ben)

| # | Item | Status | Evidence |
|---|---|---|---|
| R1 | World benchmark + ranked startup-tool ideas (world.md, world-matrix.csv) | done 5.11 | 36 pages, 33 products. The top tools: budget to real homes (100), rate decision and your payment (100), three offers in one table (80), your offer vs that bank's own average (80), "if 2022 returns" (80), exit cost by horizon (80). The BoI publishes "קו המשווה" by bank, so our moat is the PERSONAL comparison. On a phone the leaders' first input sits at 497-553 px, ours at 1,496; their pages are 11.8k-24k px, ours 52.7k. |
| R2 | Keywords HE + EN, live SERP desktop/mobile, PAA, AI answer, intent and owner map (keywords.md) | done 5.11 | keywords.md, serp-2026-11-05.json (the GSC CSVs and keywords.csv moved out of the public repo to Documents/GSC-Data/nad-lan.co.il/mortgage-2026-11-05/). Not in the top 20 for the head term (desktop or mobile). Title: מחשבון משכנתא 2026: חישוב החזר חודשי, תמהיל ולוח סילוקין. H1: מחשבון משכנתא: חישוב החזר חודשי ועלות כוללת לפי מסלולים. 0 crawlable mentions of לוח סילוקין. About 1,900 child-topic impressions land on the main page. The AI answers are wrong on the one-third prime cap, the 40% PTI, the 40-year term and the 60% foreigner LTV. English: /en/mortgage-calculator/ (hreflang twin). |
| R3 | Data v2: freshness, by-bank rates, borrower distribution, headline numbers (data/) | done 5.11 | data/data.md, build_mortgage_v2.py, boi-mortgage-v2.json (115 KB, 0 fails). New: rates by bank for 7 banks + total, per track, monthly 2024-09 to 2026-09 (TamInt010.xls, 20.10); new loans by LTV/PTI bands, investment and refinance, 25 months; track shares; debt stock and arrears; the early-repayment fee formula and rates; payment per city median (HPI + Tax Authority); 20 headlines with formulas. No official insurance price table. |
| B0 | Baseline UX audit | done | the table above |
| D1 | Design board (Artifact): phone-first page, tool switcher (no table of contents), hero instrument, new tools, data block, image | done v1 5.11 | https://claude.ai/artifact/VzwKJdV9HgRxRXDaAuLV7M : Main (phone, a working quick calculator on the BoI by-bank data), Tools (6 phone panels), Market (by bank, by city, KPIs), PageMap (order, signals, GEO, what is not touched). DS NadLan Instruments installed. |
| T1 | Hero quick answer: 3 inputs to the payment, sticky result on phone; Mortgage 2.0 as the full mode | done 5.11 (1.72.587 + 588) | mquick: by amount / price and equity / payment, 15-30 years, all banks or one bank; first input at 663 px on the phone (was 1,495). The full tool is folded on phones. |
| T2 | Bank-offer X-ray (moffers) | done 5.11 (1.72.588) | Three offers in one table, each against its own bank's BoI average, with a negotiation text. |
| T3 | Exit cost and early-repayment fee (mexit) | done 5.11 (1.72.588) | Cost by horizon plus the fee; 15,908 ILS worked example. The refinance monitor belongs to /mortgage-refinance/ (later). |
| T4 | Contract-to-keys timeline: contractor payment schedule, construction-input-index exposure, when to draw | done 6.11 (1.72.593 + page) | mkeys, the 7th chip "מהחוזה למפתח": the Sale Law linkage of indexation.js per payment, equity first then mortgage draws, interest until delivery (partial / full / immediate), the full payment after the keys at the BoI all-banks mix (mquick payPer1). Built by a sub-agent (node 54/54, browser 120/120), pressed live: 2,000,000 / 600,000 / stages / partial / 25 years gives 7,898 ILS, linkage 55,040, interest 57,809. |
| T8 | The full monthly cost in the quick calculator (benchmark row "taxes, insurance or HOA inside the monthly figure": NerdWallet, Rocket and Calculator.net have it, no Israeli page does) | done 6.11 (1.72.592) | mquick v5: two optional fields, "ביטוח חיים ומבנה" and "ארנונה וועד בית", empty by default (no official insurance price table, so no invented default); "העלות החודשית של הדירה" = payment + typed costs in all three modes; links to the Capital Market Authority calculators life.cma.gov.il and dira.cma.gov.il (both opened 6.11). Pressed live: 5,428 + 250 + 600 = 6,278. Benchmark: IL TIE -> LEAD, world LOSE -> TIE. |
| T5 | Readiness for approval in principle (mready) | done 5.11 (1.72.588) | 43 documents, each with its sources and date. |
| T6 | Budget to real homes (mbudget) | done 5.11 (1.72.588) | The listings load lazily. |
| T7 | Stress test: the 2022 replay (mreplay) + the rate decision (mdecision) | done 5.11 (1.72.588) | Peak 6,201 ILS (+772). Each quarter point is 54 ILS. |
| D2 | Market this month | done 5.11 (1.72.587) | [nadlan_mortgage_market]: six KPIs, by bank, by city, Dataset JSON-LD. |
| C1 | Content: answer first; intents with synonyms; FAQ in the searchers' words. Ben, 5.11: REMOVE NOTHING. Restructure and add only; child-page topics stay, each with a link to its owner. | done 6.11 (answer-first lines) | Ten old-guide chapters had no number, date or source in their opening; each got a 37-43 word answer-first paragraph with a dated figure, its official source and a link to the owner page (כושר החזר, אחוז מימון, משכנתא להשקעה) or the tool. Benchmark: dated and sourced 10 -> 15, worked examples 28 -> 34. FAQ wording in the searchers' words stays for a later pass. |
| G1 | AI engines (GEO/AIO), Ben 5.11: be the page ChatGPT, Perplexity, Gemini, Claude and Google AI Overviews quote. Dated numbers in plain HTML; one-sentence definitions; methodology and sources; JSON-LD BreadcrumbList (missing today) + WebApplication + FAQPage + Dataset + author/reviewer + dateModified; llms.txt entry refreshed; a visible breadcrumb (missing today). Checked 5.11: Googlebot, GPTBot, OAI-SearchBot, ChatGPT-User, ClaudeBot, PerplexityBot, Bingbot and CCBot all get 200; robots.txt allows all; llms.txt lists the page. | todo | |
| G1b | GEO method (skill ai-seo; Princeton GEO study, KDD 2024): measured gains are +40% from citing sources, +37% from statistics, +30% from expert quotes (only real, attributed quotes from official texts, never invented), +25% from an authoritative tone and +20% from clarity; keyword stuffing costs about 10%. Practice: a direct 40-60 word answer at the top of every section; headings phrased like the queries; comparison tables; dated statistics; an "updated" date; methodology; cover the fan-out queries (rates, LTV, PTI, baskets, refinance, prepayment fee, insurance, documents, timeline). Google: no AI-only markup needed and no chunking; write for people. | todo | |
| G2 | Titles: compare the SERP title Google shows with the HTML title for the top 10; pick the title and first paragraph from that; protect the sibling pages' keywords | done (research 5.11, title live 5.11); recheck | Live SERP 6.11 night (DataForSEO, google.co.il, mobile, he): we are #29 for "מחשבון משכנתא" and Google still shows the OLD title and the old hero paragraph, so the page was not recrawled since 5.11; GSC: sitemap_index downloaded 5.11 23:40, no resubmit needed, no indexing request (owner law). Recheck the displayed title and the GSC averages after 10.11. |
| C2 | Title, meta, breadcrumb, schema | done 5.11 | Title (56 chars), meta (157), H1, crumbs + BreadcrumbList, Dataset, 38 FAQ. |
| I1 | Hero image and share image | done 5.11 | gpt-image, the Israeli variant chosen of three; media 8777; og:image; captioned as an illustration. |
| E1 | English twin (hreflang pair) without overlap with /israel-mortgage-non-residents/ | doing (agent: build/english) | |
| P1 | Counted benchmark of dozens of parameters vs Israel and world pages | doing (agent: proof/) | |
| L1 | Internal links with the anchor "מחשבון משכנתא", about 10 pages a day | waits-Ben (pace) | |
| O1 | Outreach with the monthly figure | waits-Ben | |

## Rules for every release

- **Release process:** lock line, `source_audit.py` before and after, a runner with hunks on the LIVE files.
- **Checks after release:** press the page on phone and desktop, then spot-check rainbow and h-infinity.
- **Language:** no long dashes; the language-dna blacklist applies.
- **Facts:** no invented numbers; every figure is dated and sourced.
- **Never:** a 301, a noindex, an indexing request, or a sitewide change in one day.
- **Additive law:** the two older calculators stay, folded and reachable, never deleted, unless Ben says otherwise.

## Build split (5.11 evening)
- Release A (me): data v2 as boi-mortgage.json, the `mquick` hero tool, the server-rendered market block + Dataset schema, page 121 content (title, H1, meta, [nadlan_crumbs], answer paragraph, the tool switcher, crawlable schedule sample, AI-correcting facts, child-protecting headings, new FAQ), English later.
- Agents (staging only, build/<id>/): mbudget, moffers, mrates (mdecision, mreplay, mexit), mready (with sourced document lists).

## Release A log (5.11.2026 night)
- 1.72.587 code release running: NEW inc/mortgage-market.php + tools/mquick.js, boi-mortgage.json v2, mquick registry + summary hunks on the live instruments.php, module 'mortgage-market'. Dry run clean; live health 1.72.587 while the page checks run.
- Page write prepared: build/release-a/write_page.py (dry OK: every original line kept, 5 edits (H1, the lead as a superset, three headings that protect child pages), crumbs, mquick, the full tool folded on phones after it draws, both old calculators folded, the market block, a 25-row yearly schedule, the four-rules section, FAQ 30 to 38, Yoast title 56 and description 157).
- For release 588: the inherited check ('/mortgage-calculator/?t587b=1', ['class="yoast-schema-graph"'], ['"breadcrumb":{"@id"']) expects NO breadcrumb pointer; after write_page.py adds [nadlan_crumbs] the page will have one. Flip that check in make_deploy588.
- Finding (not this release): /projects/h-infinity-somail-tel-aviv/ alternates between 336,709 and 356,937 bytes within minutes (source_audit 5.11 20:23 and 20:35). It looks like a rotating block; the cause has not been checked yet.

- Open: T4 (contract-to-keys timeline), C1 rest (the answer-first lines of the old sections), first input at most 600 px, the monthly data refresh (cron with the builder, then a release), the refinance monitor on /mortgage-refinance/, and breadcrumbs on the child pages (about 13 pages; pace with Ben).

## 5.11 night, round 3
- 1.72.589 (EN components) released and verified; /en/mortgage-calculator/ published (post 8780, under /en/ root 5011): 3,505 words, 15 FAQ, mquick in English, the market block + Dataset in English, hreflang he/en/x-default. It links to /israel-mortgage-non-residents/ with the exact anchor. The full Mortgage 2.0 is not mounted (Hebrew only). Phone: first input at 1,024 px (to improve), no Hebrew in the tool, no errors.
- REGRESSION found by pressing the English page: since 1.72.588 the switcher ran before the CSS text was defined and left an empty <style id="nlmq-css">, so the quick calculator was unstyled on both pages for about 45 minutes (it still computed). Fixed in 1.72.590 (ensureCss). Lesson: after every release press the TOP tool visually, not only the new parts.
- Open: an English breadcrumb ([nadlan_crumbs] is Hebrew only); the English first input; the foreigners page title loses "Calculator" (waits for Ben); E1 is otherwise done.

## P1 benchmark (5.11 night, proof/proof.md; 77 parameters, 19 Israeli + 24 world pages, the live page after 1.72.588)
- vs the best Israeli page per row: 28 LEAD, 37 TIE, 12 LOSE. vs the best world page per row: 23 LEAD, 34 TIE, 20 LOSE.
- Leads: the six tools (none in Israel or the world: offers vs each bank's own average, readiness, decision in shekels, the 2022 replay, budget to homes), the fee on the page, BoI by bank + distribution + city payments + Dataset, dated figures 10 vs 3/2, worked examples 28, FAQ schema 38, words 9,157.
- LOSE, to close next (page-level, mine): page height 50,719 px (fold long sections into closed details that stay in the HTML, goal about 15,000); first input 665 (a shorter lead to about 430; lower would put the tool above the answer and break Ben's content-first law, so I keep the law); input labels 0.84 (label the 9 classic inputs); tap targets 0.75 (44 px on chips and table links); the old hero photo hotlinked from Wikimedia, 166 KB (self-host); a refinance break-even panel; a city default; the HowTo schema.
- LOSE, sitewide (needs Ben's word): Stripe 287 KB, the tawk.to chat 241 KB and Hotjar on every page (load after the first tap); 20 font files; about 176 KB of inline CSS and JS; the page cache header. Named author or reviewer (who signs).
- Accept: weekly payments (Israel is monthly), BoI data age (monthly by nature), a 360-row schedule (weight), the promo image count.

## Round D (5.11 night, content only, no release)
- Shorter lead; aria-label on the classic inputs; the Wikimedia photo self-hosted and credited (it carried no credit before, a CC BY-SA licence gap); phone folding (6 sections) and FAQ tap-to-open. Measured on the phone: first input 556 px (target 600 met), page height 33,472 px (was 50,323), labelled inputs 55/55.
- Next page items: page height toward 20,000 (the city table and the tools panels), the refinance break-even panel, a city default in mquick, HowTo schema, the English first input (1,024 px) and an English breadcrumb, the monthly data refresh after BoI publishes TamInt010 (around the 20th: run data/build_mortgage_v2.py, then a data-only release).

## Round E (6.11.2026, release 1.72.591 + English page 8780)
- Live 1.72.591 (deploy-result-591.json, released and verified): "האם למחזר?" in mexit (the existing balance refinanced today at the Bank of Israel average for the months left; new payment, monthly difference, exit costs, break-even months), a city select in mquick's price mode (24 cities + the national row, Tax Authority median 4 rooms, dated), language-aware page breadcrumbs (Hebrew output byte-identical). HowTo schema live on the Hebrew page (nlmx-howto).
- English page: [nadlan_crumbs label="Mortgage calculator"] at the top; trail Home › Mortgage calculator, BreadcrumbList, dir ltr, one h1.
- Pressed on a phone 390x844 (Playwright, system Chrome, eyes on screenshots): Hebrew crumbs dir rtl + aria "מיקום בעמוד" unchanged; refinance worked example 162 months, 105 ILS a month, costs 16,925 ILS; city select fills 2,028,800 and the payment 8,842 ILS on both pages; 0 console errors; 0 horizontal scroll on both pages.
- Next: page height toward 20,000 px (city table and tool panels), T4 contract-to-keys timeline, C1 answer-first lines of the old sections, rerun proof/measure.py, the monthly BoI refresh around the 20th, breadcrumbs on the child pages (about 13, paced with Ben).

## Round F (6.11.2026, content only, no code release): a shorter phone page, nothing removed
- Design: PhoneLength board on the canvas (https://claude.ai/artifact/VzwKJdV9HgRxRXDaAuLV7M, version 10).
- Hebrew page 121: the phone folding script v2. A chapter taller than 560 px (was 1,100) folds to its heading and first paragraph when the folded part is at least 200 px. The FAQ becomes a compact list (18 px, one rule per question). Not folded: the six tools, the market block, the four rules, the guide's opening block with the photo and child-page links. Measured live on a phone (390x844): page 33,472 -> 27,963 px, folded chapters 6 -> 14, FAQ 2,925 -> 2,199 px. Desktop 43,368 px, unchanged. Text in the HTML unchanged. 0 console errors, 0 horizontal scroll.
- English page 8780: the same block in English ("Read the full section") before the FAQ. Phone 21,637 -> 11,572 px, below NerdWallet (13,548). Desktop 15,670, unchanged. 6 chapters folded, 15 FAQ in a list.
- Source audit before and after: only explained diffs (the 1.72.591 version strings, the footer email's per-request spam encoding, today's English breadcrumbs, the fold block itself).
- Finding, not touched: on the English page the theme's heading face falls back to a serif for Latin text (H1, H2, FAQ questions). A typography fix for the English pages, sitewide, is a separate item.
- Finding, not ours: on desktop, headless Chrome logs a CORS error for the tawk.to chat script (embed.tawk.to), on the live page before and after this round.
- Next: the Hebrew page is still 27,963 px. The big blocks left: the open tool pane (budget to homes, 3,446 px), the market block (3,018 px, of which the city table is 1,109 px, sorted by price, so the first rows alone would hide Tel Aviv and Jerusalem), the four rules (1,241 px), the guide's opening block (1,055 px).
- Round F2, same night (content only): the benchmark re-run after round F showed CLS 0 -> 0.047 on the phone. Its cause was the quick calculator mounting 500 to 640 px taller than its server summary, which pushed the paragraph under it out of the first screen. Fix: a min-height per width on the mquick host, measured on the live pages (each value at most the mounted height: no gap, checked 0 px at 360/390/430). Live CLS now 0 at 360/390/412 on both pages; desktop 1280 0.047 -> 0.021 (Hebrew) and 0.006 (English), the rest is font swap on the lead.
- Round F2: the loan distribution (by income share and by financing share) sat inside a chapter that folds on phones, so the benchmark's "visible distribution" row fell from LEAD to TIE. One sentence with the two August 2026 figures already on the page now ends the chapter's visible first paragraph.
- Benchmark trade-off, stated plainly: "visible words after JavaScript" counts only unfolded text, so folding moves it from 8,414 to about 4,100 words and that row from LEAD to LOSE. The words in the HTML (what crawlers and AI engines read) stay 9,163, a LEAD. Keeping the fold: it is what makes the phone page usable, and the text is not removed.

## Round G (6.11.2026 night, release 1.72.592 + content): T8, the full monthly cost
- Design: TrueCost board on the canvas (version 12). Code: mquick v5 (round-g/patch_mquick_v5.py; the note shortened by hand after the first check; the two fields aligned at the bottom; the source sentence moved from the mono face, which fell back to a Courier-like font, to the text face).
- Released 1.72.592 (deploy-result-592.json, released and verified; the live mquick.js was the 1.72.591 file, md5 1b24bf3c, before the swap). Then the pages' nlmq-reserve min-heights followed the taller tool (round-g/write_reserve_g.py): phone CLS still 0 at 360/390/412 on both pages, no gap under the tool.
- Pressed live on a phone, both pages: fields empty at start, total hidden; 250 + 600 gives 6,278 with a three-part breakdown; emptying one field leaves two parts; "by monthly payment" adds the costs to the typed payment; 0 console errors, 0 horizontal scroll.
- Benchmark (our page re-measured; the old manual ruling "no insurance enters the monthly figure" replaced with the new evidence): vs Israel 31 LEAD, 35 TIE, 11 LOSE; vs world 23 LEAD, 38 TIE, 16 LOSE.
- Next: T4 (contract-to-keys timeline), C1 (answer-first lines), the BoI refresh around the 20th.

## Round H (6.11.2026 night, release 1.72.593 + page): T4, from contract to keys
- Design: Keys board on the canvas (version 14). Build: build/round-h/ (mkeys.js, test_mkeys.js 54/54, preview + verify_h.py 120/120, README with the worked example).
- Released 1.72.593 (deploy-result-593.json, released and verified): NEW tools/mkeys.js; two insert hunks on the live inc/instruments.php (the registry entry with deps indexation + mquick, and a server summary: the Sale Law rule and the latest construction index). Then page 121: the 7th chip and its pane, the switcher heading "שבעה כלים" (write_page_h.py).
- Pressed live (press_live_h.py, phone 390 and desktop 1280): all 9 tools mount; the default case 7,898 ILS; every plan, grace and term chip changes the result; #tool-keys opens the pane; 0 console errors; 0 horizontal scroll.
- Benchmark: no row measures this tool; the tally stays vs Israel 31/35/11, vs world 23/38/16.
- Next: C1 (answer-first lines in the old chapters, GEO), G2 (titles), the BoI refresh around the 20th.

## Round I (6.11.2026 night, content only): C1, answer first
- Design: AnswerFirst board on the canvas (version 16), generated from build/round-i/answers.json.
- Page 121 (write_page_i.py): ten paragraphs class nlx-ans right after their headings; the old first paragraphs unchanged. Figures recomputed from the live data files on 6.11: the all-banks payment on 1,000,000 ILS (15/20/25/30 years: 7,532 / 6,202 / 5,428 / 4,931), total interest 628,489 (25 y) and 775,170 (30 y), +1 point on every track 5,979, PTI 29.23% and 52.6% at 30-40% (8.2026), purchase tax on an additional home 8% to 6,055,070 and 10% above, the national 4-room median 2,028,800 (4-6.2026) and its 25% equity 507,200, the bank range 4.75% to 6.96% (5,281 vs 6,140), the 2022 replay 6,201 (+772).
- Pressed live: phone 10/10 visible as the kept paragraph of their chapters, 21 chapters folded, phone page 26,971 px (was 28,269: the longer chapters now fold), desktop all 10 visible and nothing folded; 0 errors; 0 horizontal scroll; the three owner links answer 200.
- Benchmark: dated_sourced 10 -> 15, worked_examples 28 -> 34, words_raw 9,696, page_height 27,022; tally unchanged (IL 31/35/11, world 23/38/16).
- Next: G2 (titles: compare the SERP title Google shows with ours), the FAQ in the searchers' words, the BoI refresh around the 20th.

## Round J (6.11.2026 night): G2 check, and the rows that cannot become a lead
- G2: Google has not recrawled the page since the 5.11 title change (old title and snippet in the live SERP; the sitemap was fetched 5.11 23:40). Nothing to change; recheck after 10.11.
- GSC cluster baseline (pages containing /mortgage-calculator/, 27.10 to 3.11): 114 to 195 impressions a day, average position 33 to 43, 0 clicks. The authority gap (memory nadlan-authority-gap) stays the main lever: Israeli links (L1, O1) wait for Ben.
- Benchmark rows still LOSE after rounds D to I, and why they stay:
  - Speed and weight (html_bytes, transfer 1.74 MB, 114 requests, TTFB, DCL, load, LCP): the best Israeli pages are bare tools (13 KB, 8 requests). Ours carries the site stack (Stripe, tawk.to, Hotjar, 20 font files, theme CSS). A page-only fix cannot reach them; a sitewide performance decision is Ben's (HAD-658).
  - page_height and words_rendered: the full article stays on the page (Ben: remove nothing); folding already took the phone page from 50,719 to 27,022 px, and folded text is not counted as visible.
  - first_input_y 556 vs Mashcantaman 410: the gap is the H1 (3 lines) and the answer paragraph; closing it breaks the content-first order (owner law 27.9) or cuts the H1.
  - payment_frequency: weekly or bi-weekly mortgage payments do not exist in Israel; adding them would be invented.
  - market_data_age_days (world): the Bank of Israel publishes mortgage averages monthly; there is no official daily rate to show.
  - author_reviewer (world): a named reviewer is Ben's decision (HAD-658).
  - figures_raw, cells_raw, visuals_rendered (world, Calculator.net and Meilleurtaux): we lead Israel; matching them means very large tables and images that would add weight to rows we already lose.
- Cadence: the loop now runs slow (hourly), for the time-gated items: the title recheck after 10.11, the BoI data refresh around 20.11 (build_mortgage_v2.py, then a data-only release), and anything Ben answers.
- Round I, English (6.11 early morning): the olim chapter of /en/mortgage-calculator/ was the one English chapter opening with no figure; it now opens with the oleh purchase-tax brackets (0% to ₪1,978,745, 0.5% to ₪6,055,070, ptax.json, in force since 16.1.2025) and the 75% single-home cap. Live, phone: visible as the kept paragraph of the folded chapter, 0 errors, 0 horizontal scroll, page 11,867 px. Both pages healthy at 1.72.593 (all 9 Hebrew tools in the HTML).

## Round K (6.11.2026 morning, release 1.72.594): no dead end in "כמה דירה זה קונה"
- The finding: on its own default example (budget 1,926,000) the tool showed only "no home on the site up to the budget", while a priced home was 74,000 above it.
- Design: BudgetAbove board on the canvas (version 18). Code: mbudget v2 (round-k/patch_mbudget_v2.py, then capped by hand at 15% above after the first live check listed Tel Aviv homes 2.7 and 3 million above): the note stays, then up to three of the closest priced homes at most 15% above the budget, each with its gap. NLMB.listings returns `above`. Tests: the original suite 148/148 (the trace check now knows the new prices and gaps; it can run on the plugin file with MBUDGET_TOOL) plus 3 new unit cases.
- Released 1.72.594 (deploy-result-594.json, released and verified; the live file was the 1.72.588 v1, md5 9b492aeb, before the swap). The 594 runner first carried the 593 cache-busting markers; fixed before the run (390 markers t594, none t593).
- Pressed live: phone shows the Ofakim home at 2,000,000 "₪74,000 מעל הסכום"; all 9 tools mount on phone and desktop; 0 errors; 0 horizontal scroll. Source audit: only the footer email encoding.

## Loop stopped (6.11.2026, Ben)
- Ben: keep Stripe, the chat and Hotjar on the mortgage page (no page-only removal), so the weight and speed rows stay as they are. Ben stopped the loop.
- Left for later, time-gated: the title Google shows after 10.11 (GSC + one live SERP), and the Bank of Israel monthly refresh around 20.11 (data/build_mortgage_v2.py, then a data-only release with the page numbers that quote September 2026).
- Still waiting for Ben: a named reviewer, the pace of Israeli links (L1, O1), breadcrumbs on the child pages.

## Round M, 6.11.2026 (Ben: manual Google pass, competitors and government sites, nothing they have and we lack): LIVE 1.72.596
mcheck (pre-signing, 451 format, 28 checks + final documents), mzakaut + zakaut.json (eligibility points, gov.il), mnomeff (nominal/effective), Mortgage 2.0 v2 (C1 C2 C3 C5 C9 C14); page 121: before-signing, eligibility-loan, calculator-method, קו המשווה, FAQ 41, byline צוות נדל״ן at the very end. Proof: ../2026-11-06-mortgage-delta/proof-after-m.md (78 rows, 66 yes). Benchmark IL 32/34/11, world 24/38/15. Commit 702edaef.

## Round N, 6.11.2026 evening (Ben: the whole mortgage universe on this one page; the bare word משכנתא / משכנתה is the head keyword; manual Google only; Kol Zchut and the state sites; Claude Design; a recursive loop): LIVE 1.72.597
- Research (docs/research/2026-11-06-mortgage-universe/): manual SERP in the owner's Chrome (משכנתא 1 to 80, nad-lan #76 with the old title; משכנתה 1 to 20: knowledge panel + local pack, no AI summary; 20 more queries), serp-dna-mashkanta.md (why each result sits where it sits); Kol Zchut 125 pages, 3,258 facts, quotes checked (kolzchut/); 100 official facts, 89 verified, the BoI fee files, bank lines (gov/); 108 competitor pages, delta and heading DNA (competitors/); gov.il service pages blocked to scripts were read by hand (mortgage_registration, fees-2026, guide-mortgage).
- Design: board "משכנתא מהאישור ועד הסילוק" (canvas v20).
- Tools (1.72.597, deploy-result-597.json, released and verified): mhivun (עמלת היוון, whole mortgage, partial prepayment, 24 months; equal to feeExisting on 400 cases), mneches (דירה קיימת; BoI any-purpose rate 6.61% vs 4.62%; 120,000 ₪ exemption), mrishum (רישום משכנתה ואגרות 2026, 33 paths, exemptions, ILA path read by hand), mkashe (הקפאה ואי תשלום: three deferral kinds, the timeline, rights, ended war programs).
- Page 121 (write_page_n.py): the map "כל נושאי המשכנתא, לפי השלב" (8 stages, 49 links, CTA, 24 back-links, never floating), chapters what-is-mortgage, mortgage-registration, registration-fees, capitalization-fee, mortgage-cancellation, payment-trouble, mortgage-rights (14 law + 16 Kol Zchut), existing-property, mortgage-banks, rules-2026; amount ladder (32 amounts); 13 chips; FAQ 41 -> 54; DefinedTerm; link to jus-tice for מחיקת משכנתא. Follow-ups the same evening: map links 40 -> 44 px (tap44 0.73 -> 0.87), the money sentence back before the definition in the lead (first_money_y 356 -> 302).
- Pressed live (content/press-live-n.json, shots/live-n-*): 13 chips, the four tools mount, map 8 groups (phone closed, desktop open), 0 broken links, 10 new chapters, FAQ 54, byline last, one h1, no horizontal scroll, 0 console errors. Source audit: the mortgage page +4 scripts, +1 JSON-LD, +1 style; rainbow and h-infinity byte noise only.
- Benchmark: Israel 32 lead / 35 tie / 10 lose (was 32/34/11), world 25 / 37 / 15 (was 24/38/15).
- Open: the title Google shows (recheck after 10.11); BoI refresh around 20.11; the housing-company commitment path; the current eligibility-loan rate (gov.il, by hand); a named reviewer (Ben).

## Round O (loop, 6.11.2026 evening): eligibility rate, the stopped relief law, the borrower's situations (content only)
- Read by hand in the owner's Chrome: gov.il mortgage_guide (updated 25.9.2024: 36 months new / 1 year second-hand, self-build 36 months from the permit, total up to 75%, the rate formula, any mortgage bank), mortgage_interest_decrease (28.2.2016: 599 points, 10 to 30 years), and the BoI page the guide links ("הריבית הממוצעת על משכנתאות", file updated 18.10.2026). Manual SERPs: משכנתא לשיפוץ, משכנתא ללא הון עצמי, עד איזה גיל, 90 אחוז, החזר משכנתא מהמדינה, סבסוד משכנתאות (Globes 20.5.2026: the government relief law stopped; ynet 31.3.2026: approved by the government).
- Page 121 (write_page_o.py): eligibility terms + the eligibility rate by term worked from the formula (2.74% / 2.96% / 2.87% / 3.00%, labelled our computation); rules-2026 rows 13.1, 31.3, 20.5; new chapter mortgage-situations (Q&A 2.2 renovation is not any-purpose; no equity: 329 s.2 and s.4א, Q&A 2.7, Annex A 1.3; no age limit in directive 329, text searched; self-employed; young couples; no general refund from the state); map link (stage 1 now 8); FAQ 54 -> 59.
- Pressed live: map 50 links, 0 broken; FAQ 59; 0 errors; no horizontal scroll. Audit: bytes only. Benchmark unchanged IL 32/35/10, world 25/37/15.

## Round P (loop, 6.11.2026 evening): mortgage tracks, the ILA commitment, and a style fix (content only)
- Manual: ILA procedure 90.02B (PDF, published 8.7.2025): the commitment is issued with no fee (s.1.10); ILA issues it when the home is not managed by a housing or contractor company (except Annex 2) and not registered; conditions; discharge with a signed letter from the lender. Manual SERPs: התחייבות לרישום משכנתא חברה משכנת, משכנתא לבנייה עצמית. Kol Zchut "מסלולי הלוואה למשכנתא" (2.3.2025) for track facts.
- Page 121 (write_page_p.py): chapter mortgage-tracks (six tracks with abbreviations, share and average rate from קו המשווה 9.2026, capitalization-fee rule); the ILA commitment paragraph in mortgage-registration; map link (stage 2 now 9); FAQ 59 -> 64 (40 years, self-build, porting, the ILA commitment, מ״צ vs מל״צ).
- Found and fixed live: what-is-mortgage and mortgage-tracks sat outside `.nadlan-guide .nlu1`, so their tables showed the theme default (cream header, against the design law); both now sit in the same two-level wrapper as the other chapters (fix_wrap_p.py, fix_wrap_p2.py), and the phone fold skips them so the definition stays open (fix_fold_p.py).
- Pressed live: 51 map links, 0 broken; FAQ 64; 0 errors; no horizontal scroll; tables white with steel rules on 390 and 1280 (eyes).
- Benchmark: Israel 33 lead / 34 tie / 10 lose (best so far; words_rendered LEAD), world 25 / 38 / 14.
- Waiting: the mrishum data update with the ILA fee 0 and discharge (agent), then a data release 1.72.598.
- 1.72.598 (deploy-result-598.json, released and verified): mrishum + rishum.json after ILA procedure 90.02B (commitment 0 ₪ per s.1.10, conditions, discharge by the rights holder with the lender's document; amendment and discharge fees "not stated in the procedure"); the mrishum summary hunk on the live instruments.php. Pressed live on the ILA path at 390 and 1280: 90.02B and 0 ₪ shown, the old "not on the service page" label gone, 0 errors, no horizontal scroll.

## Round Q (loop, 6.11.2026 evening): lenders' own terms, side by side (content only)
- Read by hand in the owner's Chrome: deferral pages of Mizrahi-Tefahot (full or interest-only, no term extension, 320 ₪ per loan, one request per borrower set), Leumi Mortgages (the law's 3 x 3 months, plus discretionary deferral, tariff fee), Discount (up to 6 months, with or without term extension, in the app, cancel within 60 days), Bank of Jerusalem (FAQ); Hapoalim's page rendered no text (left out). Insurers: Menora Mivtachim (any purpose up to 70%, investment up to 75%, "not bound by the BoI underwriting rules"), Clal (up to 60%); Harel refused access (left out, not bypassed).
- Page 121 (write_page_q.py): the deferral table in payment-trouble (with the law's baseline row), the bank vs insurers table in existing-property; FAQ 64 -> 66.
- Pressed live: 0 errors, no horizontal scroll, tables in the site style at 390 and 1280; phone numbers checked by glyph position (asterisk left of the digits). Benchmark unchanged IL 33/34/10, world 25/38/14.
