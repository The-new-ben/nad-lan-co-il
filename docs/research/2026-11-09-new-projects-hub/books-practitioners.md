# Practitioner books and book-length works: on-page SEO and AI-search lessons for /projects/

Research date: 2026-11-10. Read-only web research for the /projects/ hub (HAD-689).
Companion to `practitioners-one-page.md` in this folder (that file covers merge case studies and
one-page-per-intent evidence; this file covers on-page placement and AI-search citation).

Scope rules followed
- Practitioners and data studies only. Google documentation and Google staff are not used as evidence.
  Where a practitioner's page itself leans on a Google statement, that part is left out or flagged.
- Off-page and link building are out of scope. Where an author says the off-page layer decides the
  result, it is noted in one line and not developed.
- Everything is paraphrased. This file contains no direct quotes.
- Owner laws apply to every recommendation here: no redirects, no noindex, no new URLs, no indexing
  requests, no sitewide same-day changes. Where a source recommends something that touches those laws,
  it is reported as a finding only.

Evidence classes used on every item
- **measured**: a controlled test with a control group (mostly SearchPilot split tests, one lab paper).
- **study**: a data set showing correlation, not cause.
- **observed**: the author reports a pattern or result without a data set.
- **opinion**: experience-based advice, no data.
- **unverified**: I could not check it at the original source. The reason is given each time.

How the reading was done (honest limits)
- Most pages were read through a fetch tool that passes the whole page text to a small model and
  returns a detailed digest. "Read in full" below means the whole page went through that tool and I
  worked from its section-by-section digest. I did not see every sentence with my own eyes.
- Aleyda Solis's four pages were read as raw page text in a browser, because her site blocks the
  fetch tool.
- Numbers that I took from an aggregator page (for example iPullRank's statistics appendix) and did
  not open at the original study are marked "via appendix, original not opened".

---

## Part 1. The works chosen, and exactly what was read

### Work 1. iPullRank, "The AI Search Manual" (Mike King and team)
- What it is: a free online book, 24 chapters and 7 appendices. Authors listed: Michael King (founder
  of iPullRank), Fajr Muhammad, Garrett Sussman, Francine Monahan, Annie Cushing, John Iwuozor.
  First released 2025-08-29 with 20 chapters. Change log: February 2026 (chapters 21 to 24 added,
  many chapters updated), October 2026 (glossary, statistics page), November 2026 (queryfanout.com
  appendix). No signup is needed for any chapter.
  https://ipullrank.com/ai-search-manual and https://ipullrank.com/ai-search-manual/change-log
- Read in full (through the digest tool): chapter 3 (intent and query breakdown), chapter 4 (platforms),
  chapter 7 (architecture per platform), chapter 8 (query fan-out), chapter 9 (how to appear),
  chapter 10 (relevance engineering), chapter 11 (content production), chapter 14 (query and entity
  attribution), chapter 21 (ecommerce), chapter 22 (local search), appendix A (queryfanout.com),
  appendix B (statistics and trends, both halves).
- Also read: King's long article "How AI Mode Works" (2025-05-27), which restates the book's core
  method. https://ipullrank.com/how-ai-mode-works
- Not read: chapters 1, 2, 5, 6, 12, 13, 15 to 20, 23, 24 and appendices C to G (strategy, measurement,
  team, ethics, video, automation). King's chunking article (2026-01-15) was read for the companion
  file, not again here.
- Does the author show evidence? Mostly no. Chapters 8 to 11 are method and opinion built on patents
  and retrieval research. The evidence sits in appendix B, which collects third-party studies, and in
  appendix A, which reports iPullRank's own measurements.

### Work 2. Kevin Indig, Growth Memo research series (2025 to 2026)
- What it is: a three-part research series on what ChatGPT cites, plus two related long reports. The
  Growth Memo originals are paywalled. Search Engine Journal republishes them free, and those free
  versions are what I read.
- Read in full (through the digest tool):
  - Part 1, "The Science Of How AI Pays Attention", 2026-02-17.
    https://www.searchenginejournal.com/the-science-of-how-ai-pays-attention/567597/
  - Part 2, "The Science Of How AI Picks Its Sources", 2026-03-24.
    https://www.searchenginejournal.com/the-science-of-how-ai-picks-its-sources/
  - Part 3, "The Science Of What AI Actually Rewards", 2026-03-31 (with Amanda Johnson).
    https://www.searchenginejournal.com/the-science-of-what-ai-actually-rewards/
  - "Shorter, Focused Content Wins In ChatGPT", 2026-04-14 (with AirOps, "The Fan-Out Effect").
    https://www.searchenginejournal.com/shorter-focused-content-wins-in-chatgpt/571857/
  - "Effective marketplace SEO", 2025-06-05.
    https://www.searchenginejournal.com/effective-marketplace-seo/548303/
- Not read: the Growth Memo originals (paywall, confirmed at
  https://www.growth-memo.com/p/the-science-of-how-ai-picks-its-sources ), the premium section of the
  marketplace piece, and his Zillow deep dives.
- Does the author show evidence? Yes, data sets with numbers, but all correlation, all ChatGPT only,
  and none of the seven verticals is real estate (B2B SaaS, finance, healthcare, education, crypto,
  HR tech, product analytics). The digests also flagged internal inconsistencies: a 58% versus 67%
  figure in Part 2, characters versus words in the length buckets, and unreconciled sample sizes.

### Work 3. Koray Tugberk Gubur, "Importance of Topical Authority" (book-length case study)
- What it is: a single case study of about 163,000 characters on holisticseo.digital, published
  2021-02-11, updated 2022-11-24. Older than the 2024 to 2026 window, kept because it is the most
  detailed practitioner text on where things go on a page. https://www.holisticseo.digital/?p=4946
- Read in full (through the digest tool, in two passes because of length).
- Not read: his paid course, and his 2026 Search Engine Land column (SEL blocks the fetch tool).
- Does the author show evidence? Traffic results are self-reported from his own Search Console
  (one site 0 to about 128,000 monthly visits in 123 days) and cannot be tied to any single rule.
  Almost every on-page rule is asserted. The case study itself reports losing about half its traffic
  when featured snippets were removed in a November 2020 update, and 250 to 346 pages left unindexed.

### Supplementary sources used to test what the three works claim
- Aleyda Solis, read as raw text, all dated 2026: "AI Search Optimization Framework and Checklist"
  (updated 2026-09-26) https://www.aleydasolis.com/en/ai-search/ai-search-optimization-checklist/ ;
  "Characteristics of AI Search Winning Brands"
  https://www.aleydasolis.com/en/ai-search/ai-search-winning-brands-characteristics/ ; "AI Search Is a
  3rd-Party Citation Problem" (2026-08-02) https://www.aleydasolis.com/en/ai-search/ai-search-citations/ ;
  "Ecommerce AI Search Optimization" (first roughly 26,000 characters; the closing section was cut off)
  https://www.aleydasolis.com/en/ai-search/ecommerce-ai-search-citations-optimization/ .
  Evidence: her two data pieces are studies (Semrush Enterprise and Similarweb data, labelled
  directional by her); the checklist is opinion.
- SearchPilot controlled split tests (measured). Individual case-study pages, linked at each item.
- Zyppy title rewrite study (study). https://zyppy.com/seo/title-tags/google-title-rewrite-study/
- AirOps research roundup (study). https://www.airops.com/blog/ai-search-statistics
- Ahrefs freshness study, Ryan Law, 2025-07-28 (study).
  https://ahrefs.com/blog/do-ai-assistants-prefer-to-cite-fresh-content/
- Ahrefs on chunk optimization, Despina Gavoyannis, 2025-08-21 (opinion).
  https://ahrefs.com/blog/seo-chunk-optimization/
- "GEO: Generative Engine Optimization", Aggarwal and others, Princeton University and IIT Delhi,
  first version 2023-11-16, KDD 2024 (measured, academic lab benchmark; this is the paper the
  practitioner books lean on). https://arxiv.org/html/2311.09735v3

### Candidates checked and not used
- "The Art of SEO", 4th edition (Enge, Spencer, Stricchiola, O'Reilly, September 2023, 773 pages):
  exists. **Could not read.** O'Reilly returned 403, and the author's free chapter sits behind a
  signup form, which this task does not allow. Nothing from it is used.
- Eli Schwartz, "Product-Led SEO" (2021): exists, paid, no free text found, no second edition found.
  Not read, not used.
- Marie Haynes's Gemini-era book and Dixon Jones's "Entity SEO": my searches did not confirm dates or
  free text. **Unverified, not used.**
- Lily Ray: one 2026 piece was used in the companion file; nothing new read here.

---

## Part 2. The lessons, by topic

Item codes (A1, B3 and so on) are used later to trace each /projects/ check back to its source.

### A. Where the head phrase goes, and how synonyms are placed

**A1. Make the H1 say the same thing as the title, and keep the title in the safe length band (study)**
Cyrus Shepard, Zyppy. 80,959 titles on 2,370 sites, data from early 2022, page updated 2026-10-06.
Google rewrote 61.6% of titles. The lowest rewrite rate (39 to 42%) was at 51 to 60 characters; over
70 characters almost everything was rewritten. Matching the H1 to the title was the strongest way to
keep the title as written. When the title had a number and the H1 did not, the number was dropped in
about a quarter of cases; when both had a number it survived 97% of the time. Square brackets were
removed far more often than round ones, and pipe separators were replaced about twice as often as
dashes. Caveat (mine): measured on English desktop results; Hebrew character widths differ, so treat
the 51 to 60 band as a guide and check the real result page.

**A2. Put the most identifying words first in the title (measured)**
SearchPilot, 2025 round-up posted 2025-12-19. On healthcare location pages, moving the place name to
the start of the title raised organic traffic 8.5% at 95% confidence.
https://www.searchpilot.com/resources/case-studies/a-look-back-at-the-most-surprising-tests-of-2025
For a non-local hub the equivalent is: head phrase first, brand last.

**A3. Word the title and H1 the way people actually type the query (measured, weak; plus two studies)**
- SearchPilot, 2023-08-10: a retailer removed an extra category word from titles and H1s because
  shoppers did not type it. Organic traffic rose 28% on low-traffic pages; no confidence figure given.
  https://searchpilot.com/resources/case-studies/aligning-keywords-with-search-queries
- AirOps, March 2026 (study): pages whose title shared half or more of its words with the query were
  cited by ChatGPT 20.1% of the time, against 9.3% for under 10% overlap.
- AirOps, August 2025 (study, small, about 300 cited pages): pages with at least 30% of the query's
  terms in the title or URL slug were about twice as likely to be cited.

**A4. The H1 on its own is a weak lever (measured)**
SearchPilot ran three H1-only tests. Adding a keyword to the front of the H1: best estimate +8%, not
statistically significant (2021-03-11, https://www.searchpilot.com/resources/case-studies/compare-in-h1/ ).
New H1 plus new intro copy on location pages: no detectable change in organic traffic (2022-12-08,
https://www.searchpilot.com/resources/case-studies/changing-introductory-text-and-h1 ). Price added to
the H1: inconclusive (2024-06-13, https://searchpilot.com/resources/case-studies/adding-price-to-h1 ).
Read with A1: the H1's proven job is to agree with the title, not to carry extra keywords.

**A5. The opening of the page is where engines look first (study, three sources that agree)**
- Indig Part 1: of 18,012 verified ChatGPT citations, 44.2% came from the first 30% of the page, 31.1%
  from the middle, 24.7% from the last third.
- Indig Part 2: across seven verticals the peak was the band from 10% to 20% of the page. The very
  first 10% is often navigation and warm-up and is skipped. The last 10% earned 2.4 to 4.4%.
- Indig Part 3: the one rule that held in every vertical was to open with a direct declarative
  statement that says what the subject is or what it does. Hedging words in the opening were penalised. A date
  and a specific number in the opening were positive in almost every vertical.
- Peec AI, June 2026 (via appendix, original not opened): ChatGPT's first read of a page returns a
  capped window of about 5,700 characters at the median. Pages with fewer than 20 links were about 78%
  real content in that first read; pages with 60 or more links were about 33%.
- Koray (opinion): the top section should state the page's purpose and contain the main query and its
  variations; the terms a page ranks best for usually sit in the first section.

**A6. Repeat the heading's subject in the first sentence of the answer (study plus opinion)**
Indig Part 1: cited text was about twice as likely to contain a question (18% against 8.9%), and 78.4%
of those question citations came from headings. He recommends that the sentence right after a heading
starts by naming the same subject as the heading. King, chapter 9 (opinion): restate the subject
instead of using "it", "this" or "they", because a passage may be lifted without its neighbours.

**A7. Synonyms: cover the vocabulary of the topic, do not repeat the phrase (measured in the lab, plus opinion)**
- GEO paper (measured): keyword stuffing was the worst of nine methods, about 9% below baseline both
  in the benchmark and in the live test on Perplexity.
- King, chapter 10 (opinion): relevance comes from covering the related terms and concepts of the
  topic across passages, not from a primary and secondary keyword count.
- AirOps, August 2025 (study, small): titles and slugs of cited commercial pages shared only about 16%
  of their words with the query; meaning-level similarity mattered more than word overlap.
- King, chapter 9 (opinion): use one consistent name per thing. See the disagreement section: this
  pulls against "include every variation".

**A8. URL (study, weak) and year in the title (observed)**
AirOps (A3) found the slug behaves like the title. Indig Part 2 observed that the pages cited across
the most prompts often carried the year in the URL or title, but he did not quantify it. AirOps
(March 2026) found a year is added to ChatGPT's own sub-queries mainly for research-type questions
(9.7% of them). No source here tested a year in the title of a listing page.

**A9. Anchors pointing at the page (study and opinion, they differ)**
Zyppy's internal link study (companion file, item 13): more different anchor texts and at least one
exact-match anchor both went with more clicks. Koray (opinion, self-reported): few links in the main
content, about three, each with an anchor that matches the target page, prepared in advance and added
when the target is live; contextual links over global menus.

### B. How one page is built to rank for hundreds of queries of one intent

**B1. Broad category-level pages are the ones cited across many prompts (study)**
Indig Part 2, about 21,500 citation rows: on average 67% of cited URLs appeared for one prompt only.
The top 4.8% of URLs, cited ten or more times, were category-level comparison or guide pages that
answered what it is, who it is for, how to choose and what it costs on one URL. One comparison page
out-performed whole domains. Top 10 domains held 46% of citations per topic, top 30 held 67%.

**B2. But for any single prompt, a focused section with a matching heading wins (study)**
Indig with AirOps, 16,851 queries run three times, 353,799 pages: the position of the page in ChatGPT's
own search results was the strongest predictor (58% cited at the top, 14% at position ten). The
strongest content signal was a heading that closely matched the query (41% against 30%; among
top-ranked pages a close match added 19 points). Covering every sub-question added only 4.6 points,
and pages covering a quarter to a half of the sub-questions were cited more than pages covering all
(38.2% against 34.0%). Pages over 5,000 words were cited less than pages of 500 to 2,000 words.
B1 and B2 come from the same author one month apart. See the disagreement section.

**B3. Passages compete, not pages (opinion, patent-based; one small test)**
King, chapter 8 and "How AI Mode Works": engines split the query into sub-queries, retrieve passages
for each, and compare passages head to head. A long page should work as a set of self-contained
modules, each with its own scope. A site that answers several branches can be cited several times in
one answer. Selection criteria he lists: can the passage be lifted cleanly, how many checkable facts
per sentence, is the scope stated (for whom, where, as of when), is it dated. His only test is the
embedding example in the companion file (item 14).

**B4. Headings that copy the query wording (measured once; studies agree)**
SearchPilot, 2023-05-02: a generic features heading (H2) was rewritten as a question that included the
item's name. Organic traffic rose about 12% in 20 days; no confidence figure in the text.
https://searchpilot.com/resources/case-studies/rephrasing-h2s-into-questions
AirOps heading-match result (B2) and Indig's question-heading result (A6) point the same way.
Koray (opinion): turn the related questions Google shows into headings, nest small questions under
broader ones, and keep the main intent visible at the top, because too many questions dilute a page.

**B5. One H1 and headings in strict order (study)**
AirOps, July 2025, 12,000+ URLs: 68.7% of pages cited by ChatGPT followed a strictly sequential heading
order, against 23.9% of Google page-one results; 87% had exactly one H1, against 64%.

**B6. How many headings (study, vertical-dependent, no real-estate data)**
Indig Part 3: three or four headings was the worst band in every vertical, worse than none. Best band:
crypto 5 to 9, finance 10 to 19, B2B software 20 or more with H3s, healthcare few. AirOps: articles did
best with four to ten subheadings; Indig's April advice is 7 to 20. **Unverified for real estate.**

**B7. A question-and-answer block under a listing page (measured)**
SearchPilot, 2026-04-24: adding FAQs that answer category-level questions under retail listing pages
raised organic clicks an estimated 9.7%, positive at the 95% level.
https://www.searchpilot.com/resources/case-studies/will-adding-faq-content-to-footer-copy-improve-organic-traffic

**B8. Short answer first, then the list or table (observed and study)**
Koray (observed, no sample): answers that win the answer box are usually under about 40 words; write
one definitive sentence before any list; "best" and comparison questions get a list or table,
definitions get a clean paragraph. AirOps, June 2025 (study, SaaS pages): paragraphs of three or more
sentences cut answer-box capture by 59%; concise answers followed by lists raised it by 74%.

### C. Prices, numbers, counts and dated data; tables

**C1. Adding statistics and sources raises visibility in generated answers (measured, lab)**
GEO paper, 10,000-query benchmark on a GPT-3.5-based engine, checked on Perplexity: adding statistics
about +33%, adding quotations about +43%, citing sources about +28% on their visibility metric. On
Perplexity: statistics +37% on subjective impression, quotations about +21% on word share. Important
detail: the gains went to lower-ranked sources (roughly +98% to +115% for the fifth-ranked source) and
the first-ranked source lost 21 to 30% when everyone used the method. Lab conditions, 2023 to 2024
models.

**C2. Counts of statistics, tables and price points on commercial pages (study)**
AirOps, "From Retrieved to Cited", April 2026, 7,500 commercial prompts: comparison pages with three
tables were cited 25.7% more; pages with seven distinct price points 15.7% more; 15 or more price
points on validation pages 11% more; 7 to 26 list sections 6 to 15% more; ten images 16.4% more.
Five to seven supporting statistics, 20.3% more (via appendix, original not opened; AirOps's own
roundup page did not show this last figure, so it is **unverified**).

**C3. A date and a number near the top help; a price near the top is uncertain (study)**
Indig Part 3, entity types found in the first 1,000 characters of 5,000 pages: dates and numbers were
positive almost everywhere. Prices in the opening were the strongest negative, except in finance,
where price-like data (rates, fees) is what people search for. Real estate was not in the sample, so
whether an opening price helps or hurts our page is **unverified**. This pulls against C2.

**C4. Dates must be explicit (opinion, plus study)**
King, chapter 9: write full dates, never "recently"; give numbers with their source. Chapter 8: state
the scope of each fact (for whom, where, as of when). Solis, checklist step 8: date-stamp dynamic data
such as prices and availability and keep the page, the markup and any feed in agreement.
AirOps, June 2025 (study, SaaS): pages with a visible last-updated field earned 1.8 times more
citations. AirOps, April 2026: only 41% of pages had a publish date a machine could detect.

**C5. Tables (opinion, plus one measured test)**
King: tables with clear headers are the easiest format to lift, and every row should make sense alone.
Solis, step 4: self-contained tables and explicit criteria. SearchPilot, 2025: thin pages enriched
with specification tables and more depth gained nearly 20% organic traffic (significance not stated).
I found **no** recent, checkable study of table size for answer-box wins; older figures circulating
(40 to 50 word paragraphs, from A.J. Ghergich with Semrush data) reached me only second-hand and are
**unverified**.

**C6. Price in the title tag: a static price lost traffic (measured)**
SearchPilot, 2020-10-21: adding the price after the product name in the title cut organic traffic 15%.
https://searchpilot.com/resources/case-studies/seo-split-test-lessons-adding-price-to-title
SearchPilot, 2025-03-14 summary: a static price in titles was also negative on a travel rental site;
a price that updates with the page, and price markup, were reported positive (no numbers on that page).
https://www.searchpilot.com/resources/case-studies/the-unexpected-impact-of-price-in-seo

**C7. Numbers must be in the visible HTML (unverified)**
A searchVIU test from October 2025, reported second-hand: none of five AI systems picked up a price
that existed only in JSON-LD markup. I saw this only in a search summary. It agrees with Solis step 4
(critical facts in raw HTML) and King chapter 8 (data inside an interactive tool is skipped).

**C8. Listing counts in the title or H1: no evidence found**
None of the works tested a count such as "N projects" in a title or H1. The nearest evidence is C3
(a number in the opening is positive) and A1 (a number survives in the title only if the H1 has it too).

### D. What gets a page cited by AI engines

**D1. Being retrieved comes before being cited, and classic ranking still drives retrieval (study)**
AirOps, March 2026, 15,000 prompts: about 85% of pages ChatGPT retrieved were never cited. Pages
ranking first in Google were cited 43.2% of the time, 3.5 times the rate of pages outside the top 20.
55.8% of cited pages ranked in Google's top 20 for at least one query. See B2 for the same effect
inside ChatGPT's own result list.

**D2. The hidden sub-queries (fan-out) matter, and their wording is unstable (study)**
- About a third of cited pages were found only through a sub-query, not the typed prompt (AirOps,
  March 2026).
- How many sub-queries: about two per prompt in the ChatGPT interface (AirOps, April 2026; 88.6% of
  queries produced exactly two); 2.3 to 2.8 per prompt with average length doubling to about 12 words
  (Peec AI, February 2026); 7.61 on API runs (Nectiv, August 2026); about 1.4 on Perplexity (Peec AI,
  April 2026). The last three are via appendix, originals not opened. The figures differ by method.
- iPullRank's own test (appendix A): 2,000 prompts run three times; only 0.7% of sub-queries repeated
  word for word, but 83% came back as a near paraphrase. The information needs are stable; the wording
  is not. Simulated sub-queries predicted 95% of Gemini's real searches but only 15% of OpenAI's.
- 43% of ChatGPT's sub-queries on non-English prompts were run in English (Peec AI, February 2026, via
  appendix, original not opened). Consequence for a Hebrew page is my inference, see check 17.

**D3. Self-contained answer blocks (agreement between authors who argue about the name)**
King: each paragraph, bullet and table row should stand alone, name its subject, and state one idea.
Ahrefs (Gavoyannis, 2025-08-21) argues that nobody outside the engine controls how a page is split, so
tuning paragraph length for it is pointless; she recommends self-contained sections with the answer
first. Different labels, same page.

**D4. Named, specific entities (study)**
Indig Part 1: heavily cited text had about 20.6% entity density against 5 to 8% in normal English
text. Part 3: well-known entities with a knowledge-panel entry were a slight negative (0.81 times);
specific, niche names did better. King, chapter 11 (opinion): map the entities of the topic in three
groups before writing: places (neighbourhoods, landmarks), organisations, and concepts such as types,
speeds and prices. For our page that means project names, developers, cities, neighbourhoods, streets,
delivery dates.

**D5. Tone and reading level (study)**
Indig Part 1: cited text sat in the middle between dry fact and opinion (a fact followed by what it
means), and read at a simpler level than uncited text. Definitional phrasing appeared in 36.2% of
cited text against 20.2%.

**D6. Structured data: hygiene, not a lever (study against measured; they disagree)**
AirOps, April 2026 (study): pages with JSON-LD were cited 38.5% of the time against 32.0%; pages with
FAQ markup 45.6%. Ahrefs, May 2026 (measured, 1,885 pages, matched controls; I saw it only through
second-hand reports, so details are **unverified**): adding markup changed citations by +2.2% in
ChatGPT, +2.4% in AI Mode and minus 4.6% in AI Overviews, all within noise. King (opinion): use markup
only for content that is really on the page, and do not put FAQ markup on things that are not
questions and answers. Indig (opinion): practitioners are split; match what stronger competitors do.

**D7. Freshness differs sharply by engine (study)**
Ahrefs, 2025-07-28, about 17 million citations: ChatGPT cited pages 393 to 458 days newer than
Google's organic results; Copilot about 360; Gemini about 298; Perplexity about 250; AI Overviews
were level with organic results or slightly older. The average cited page was still about 2.9 years
old. AirOps, April 2026: pages 30 to 89 days old were cited most (32.8%) and pages under 30 days
least (25.3%); in travel 44.8% at 30 to 89 days against 26.2% at five years or more. AirOps, August
2025: commercial pages not refreshed within a year lost more than half their citation chance.
Seer Interactive, July 2026 (via appendix): share of cited pages updated within a year was 78% on
Gemini, 73% on ChatGPT, 65% on Perplexity. Koray and Ahrefs both warn against changing dates without
changing content.

**D8. Citations are unstable; measure repeatedly (study, via appendix, originals not opened)**
Profound, September 2026: the median cited page lost half its citation share within 11 days.
SISTRIX, May 2026: AI Overviews changed only 5% of cited domains week to week, while 74% of the
domains ChatGPT cited were new each week. Growth Memo, May 2026: 91% of citations appeared in one
engine only. Solis, checklist step 2 (opinion): run each test prompt three to five times inside a
fixed 24 to 72 hour window and record engine, place, language and login state.

**D9. Most citations about a brand go to other sites (study, off-page, noted only)**
Solis, 2026-08-02, 15 brands in three verticals: the brand's own site was 17.7% to 30.4% of the top
cited sources. Yext, 2025, 6.9 million citations (via King chapter 22): objective facts are checked
against the business's own site, opinions against review sites. On-page consequence only: the page
must be the accurate, current, checkable source of the facts (names, prices, dates).

**What is known per engine**

| Engine | How it finds pages | What the sources say it favours | Evidence |
|---|---|---|---|
| ChatGPT | Writes its own searches, gets a short result list, fetches pages live. King (chapter 7) and Peec AI (June 2026, via appendix) say the searches run on Bing; AirOps shows a strong link with Google rank. The index question is **unverified**. | Top of its own result list; heading that matches the query; newest pages of all engines; plain HTML that loads fast; first 5,700 characters; 5 to 7 sources per answer (AirOps) or about 15 (Semrush, via appendix); more and more direct site: searches of known sites in 2026 (Seer, via appendix). | study |
| Perplexity | Live search, about 1.4 sub-queries, stays close to the typed wording (Profound, April 2026, via appendix). | Heading that restates the question with a short answer under it; named entities; author and trust signals; explanatory images (correlation); discussion threads at twice the rate of other engines. | observed (King chapter 7) plus study |
| Google AI Overviews | Google's own index plus sub-queries. | Overlap with the organic top 10 fell from about 76% (July 2025) to 37.9% (March 2026, Ahrefs, 863,000 result pages, via appendix); 31% of cited URLs ranked beyond position 100; least sensitive to freshness; most stable week to week; markup made no difference in the Ahrefs test. | study |
| Google AI Mode | Same base, more sub-queries, keeps conversation context, personalised (King). | Most social and video-led of the three engines Solis measured; sources per answer fell from 19.7 to 3.8 between August and September 2026 (Evertune, via appendix); a growing share of citations goes to Google's own business and product panels (Profound, July 2026, via appendix). | study plus opinion |
| Gemini | Google's index. | Fewest sources per answer (about 3.3), highest share of company-owned sites (about 69%), highest share of recently updated pages (78%). All via appendix. | study |

### E. How practitioners mine the result page and competitors, and turn it into sections

**E1. Query matrix first (King, chapter 11; opinion)**
List every related query and sub-query for the topic with a fan-out tool, then label each with the
format that answers it best: table, tool or guide. Audit both the Google result page and the AI
answers for what exists and what is missing. Tools he names: Qforia and its successor queryfanout.com.
Limit for us: the public index was seeded with US English prompts only (appendix A).

**E2. Controlled variations and co-citation (King, chapter 14; opinion, no data)**
For each important query, write 10 to 50 variations (swap the modifier, the place, the year, a
synonym), record which URLs are cited for each, and see which URLs appear together. Each cluster of
co-cited URLs marks a sub-intent and shows whose page owns it. Then extract the entities from the
cited passages and compare with your own page.

**E3. Questions from the result page become the heading tree (Koray; opinion)**
Collect the related questions, group the small ones under a broader question, mark in the writer's
brief which headings are meant to win an answer box, and attach a screenshot of the answer currently
shown so the writer can see its length and form.

**E4. A fixed prompt library, rerun under the same conditions (Solis, steps 1 to 3 and 12; opinion)**
Start with 30 to 50 tagged prompts. For each, record whether the brand appears, is recommended, gets
a link, and which sources and competitors are cited. Tie every gap to one cause (not reachable, not
extractable, not useful, stale, not distinct, not corroborated) with an owner, then retest.

**E5. Compare passages, not pages (King, "How AI Mode Works"; opinion)**
For each sub-query, find your best passage and the passage the engine actually cites, and improve
yours where it loses on completeness, numbers, clarity or stated relationships.

**E6. Shared top-10 results decide what belongs on one page (companion file, items 10 and 11)**
Not repeated here. A related rule attributed to Indig (seen only in a search summary, **unverified**):
if the same competitor pages rank for both the head phrase and its long variants, do not make a
separate filtered page for the variant.

### F. Tools, interactive widgets and listing or collection pages

**F1. What Indig says makes marketplace pages work (opinion with examples; 2025-06-05)**
Treat each listing as a short answer: specifications as bullets, an FAQ, a compare-to table. Replace
duplicate category intros with real user insight or a data graphic. Design filters and facets around
real intents. Maps and other interactive elements are on his list of priority areas. Scaling up thin
template pages can pull the whole site below the quality line. Pages people skip, machines skip too.

**F2. Controlled tests on listing pages (measured)**
- Extra detail for each listing card placed in the HTML: +5% organic traffic (listings site category
  pages, 2023-01-26).
  https://www.searchpilot.com/resources/case-studies/adding-details-to-listings-pages-on-website
- Generic SEO text at the bottom of category pages removed: mobile organic traffic rose
  significantly, desktop unchanged (retail, 2024-10-31).
  https://searchpilot.com/resources/case-studies/removing-seo-text-2024
- FAQ block under listings: +9.7% (B7).
- Embedded map removed from multi-location pages: minus 7%, significant (2025 round-up).
- Bottom-of-page video carousel removed: +4.1%, significant; the lesson drawn was page weight, not
  that video is bad (2025 round-up).
- Listing-page copy rewritten in natural language: +14% (Marks and Spencer case study; seen only in a
  search summary, **unverified**).
- A real-estate customer ran 36 tests from 2019 to 2022 and only six were net positive.
  https://www.searchpilot.com/real-estate-business-success-story

**F3. Tools and widgets must also exist as readable text (opinion)**
King, chapter 8: an interactive tool whose data cannot be parsed is dropped at the selection stage,
like an image carousel without text. Give the same information as text or a table, and a downloadable
file where it helps. Solis, step 6: calculators, comparisons and pricing pages are the kind of asset
that still earns a visit after an AI answer; step 4: the key facts and links must be in the raw HTML.

**F4. Citation assets and click assets are different things (study, directional)**
Solis, ecommerce study, 25 US retail sites: AI engines often cite the page that removes the buyer's
doubt (guides, policies, sizing, support), while the clicks from AI go mostly to product and listing
pages. For marketplaces, visits land on home, search and category pages. She says to measure the two
separately. Solis, citations study: in ecommerce the largest outside source group was competitors and
marketplaces (36.6%).

**F5. Complete attributes on every listing (opinion)**
King, chapter 21: a listing with missing fields fails the filters an AI agent applies; describe why a
feature matters to the buyer, not only the specification. His feed and checkout protocol material is
about retail and is not applicable to us today.

### G. Internal linking and anchor variety towards a hub

**G1.** Anchor variety and at least one exact-match anchor go with more clicks; benefit flattens after
about 40 to 45 links (Zyppy, study; companion file item 13).
**G2.** Links between neighbouring regional pages raised traffic about 7% (SearchPilot, measured;
companion file item 19).
**G3.** Koray (opinion, self-reported): a small number of in-content links with descriptive anchors;
plan the anchor before the target exists; contextual links beat menu links.
**G4.** King, chapter 10 (opinion): anchor text and where the link sits both carry meaning; link pages
that share a topic so the cluster is visible.
**G5.** Link blocks placed before the content push the content out of the engine's first read (A5,
Peec AI). Put the answer first and the link lists after it.
**G6.** Solis, steps 4 and 6 (opinion): internal links must be plain links in the raw HTML, and every
evidence section should lead to a clear next action.

### H. What the authors say NOT to do

1. Do not repeat the head phrase to signal relevance (King; GEO paper measured minus 9%).
2. Do not open with a warm-up paragraph, hedging or a slow introduction (Indig Parts 1 and 3).
3. Do not rely on the conclusion; the end of the page is close to invisible (Indig Part 2).
4. Do not use pronouns or "this tool" style references in a passage that may be lifted alone (King).
5. Do not write paragraphs that mix two subjects (King).
6. Do not use vague amounts or relative time when a number or full date exists (King).
7. Do not stop at three or four headings (Indig Part 3).
8. Do not put FAQ markup on content that is not questions and answers, and do not mark up anything
   that is not visible on the page (King).
9. Do not expect markup to raise citations (Ahrefs test), and do not expect a high authority score to
   do it either (AirOps: always-cited and never-cited pages had the same score, about 54).
10. Do not use llms.txt as a tactic (King chapter 11; Ahrefs June 2026 via appendix: 97% of such files
    received no requests in a month).
11. Do not block AI crawlers if you want citations (King, Solis).
12. Do not hide key facts inside scripts, tabs that load later, or widgets (King, Solis).
13. Do not put a static price in the title (SearchPilot).
14. Do not keep generic bot-focused text at the bottom of a listing page (SearchPilot).
15. Do not change dates without changing content, and do not refresh on a fixed timetable just to
    look fresh (Koray, Ahrefs).
16. Do not spread one topic thinly over many URLs (King chapter 7), and do not multiply thin template
    pages (Indig marketplace).
17. Do not build exhaustive "cover everything" pages and assume length wins (Indig, April 2026).
18. Do not depend on answer boxes as stable traffic (Koray lost about half his traffic that way).
19. Do not game AI systems with injected prompts, fake reviews or manufactured community signals
    (Solis).
20. Do not judge AI visibility from one run or from a logged-out rank tracker (King, Solis).
21. Do not use AI-generated images as evidence of a real place (King chapter 22 reports reduced
    visibility for them; this also matches the site's own real-media law).

Findings that touch owner laws, reported only: King (chapter 22) recommends a ping protocol
(IndexNow) so updates are seen at once; under the owner's rules that is allowed only after he approves
installing it. Solis and several case studies speak of consolidating obsolete pages; that is not
proposed here.

---

## Part 3. Where the authors disagree

1. **Breadth against focus (Indig against Indig).** March 2026: broad category pages covering ten or
   more intents are the ones cited across many prompts, and longer pages earn more citations. April
   2026: full coverage adds almost nothing, half coverage beats full, 500 to 2,000 words is the best
   band. My reading, not theirs: breadth decides how many different prompts a URL can enter; a close
   heading match and a tight passage decide whether it is chosen for each one. The two data sets also
   measure length differently (characters in one, words in the other).
2. **Chunk design.** King treats passage design as the core craft. Ahrefs calls chunk optimization a
   fad because the engine decides the split. Both end at the same advice: self-contained sections,
   answer first.
3. **Structured data.** AirOps correlations favour it; the Ahrefs controlled test found no effect;
   King wants more of it (custom ontologies); Indig says copy stronger competitors. Only one of these
   is a controlled test.
4. **Prices.** AirOps: more price points on commercial pages go with more citations. Indig Part 3: a
   price in the opening is negative outside finance. SearchPilot: a static price in the title lost 15%.
   Consistent reading: prices belong in the body and tables, dated; the opening and the title are
   unproven or negative.
5. **Synonyms.** King: one consistent name per thing. Koray: the opening should carry the main query
   and its variations. King again (chapter 10): varied phrasing across the page. Workable reading: do
   not rename the same thing inside one passage; let each synonym of the query own a heading or
   sentence of its own.
6. **Question headings.** Indig, AirOps and one SearchPilot test favour headings worded as the
   question. Koray warns that many questions dilute the page and wants the main intent kept at the
   top. Indig Part 3 shows heading counts that help in one vertical hurt in another.
7. **Anchors.** Zyppy's data favours variety plus one exact match. Koray favours few links with
   target-matching anchors.
8. **Bottom-of-page content on listing pages.** SearchPilot removed generic SEO text and gained on
   mobile; SearchPilot added real FAQs and gained 9.7%. The difference is whether the text answers
   real questions.
9. **Where ChatGPT gets its results.** King and Peec AI say Bing; AirOps shows citation tracking
   Google rank. Unresolved.
10. **The end of the page.** Indig Part 1 says summary sections just before the footer are cited
    often; Part 2 says conclusions are nearly invisible in every vertical.

---

## Part 4. Claims in this file that are not verified

- Every figure marked "via appendix, original not opened" (Peec AI, Nectiv, Seer Interactive, Profound,
  SISTRIX, Evertune, Semrush, BrightEdge, Yext): I read iPullRank's summary of the study, not the study.
- The Ahrefs markup test (D6): second-hand reports only; dates given as 11 or 12 May 2026.
- The searchVIU JSON-LD price test (C7): search summary only.
- The AirOps "five to seven statistics" figure (C2): present in iPullRank's appendix, absent from the
  AirOps roundup page I read.
- The Marks and Spencer listing-copy test (F2) and the Indig facet rule (E6): search summary only.
- Answer-box paragraph length of 40 to 50 words (C5): second-hand, old.
- Koray's traffic numbers: self-reported, no outside audit.
- All of Indig's findings: ChatGPT only, correlation only, no real-estate vertical, with internal
  inconsistencies noted in Part 1.
- All Hebrew-specific consequences: no source here tested Hebrew pages. The one data point on
  non-English prompts (43% of sub-queries run in English) is via appendix.
- Nothing in this file was checked against the live /projects/ page. The checks below are tests to
  run, not findings about the page.

---

## Part 5. What this means for /projects/ on nad-lan

### Checks the page should pass (each traces to items above)

1. **Title starts with the exact head phrase** (פרויקטים חדשים), brand last, no brackets, a dash and
   not a pipe as separator, and the full title is shown unchanged on the Google result page. (A1, A2)
2. **The single H1 carries the same head phrase and the same promise as the title.** If the title has
   a number or a year, the H1 has it too. Exactly one H1. (A1, A4, B5)
3. **The first sentence under the H1 is a plain statement that names the head phrase and says what the
   page gives**, with one real number and a full date (for example how many projects are listed and as
   of which date). No warm-up line, no hedging. (A5, A6, C3, C4)
4. **Everything in check 3, plus the first city or family answer, sits inside the first 5,700
   characters of the main text**, and no long link list, city menu or filter block comes before it in
   the HTML. Count the links that precede the first paragraph; the target is under 20. (A5, G5)
5. **Each family of the intent has its own H2 worded the way people type it** (דירות חדשות, דירות
   מקבלן, אכלוס מיידי, and each city variant that stays on this page), and the first sentence under
   each H2 repeats that phrase and answers it in under about 40 words before any list or table.
   (A6, B2, B4, B8)
6. **Each H2 section reads correctly when copied out alone**: it names the city, the project and the
   developer in full, uses no "it", "here" or "the above", and states its date. (B3, D3, C4)
7. **The page has a committed heading tree**, clearly more than four headings, in strict order with no
   skipped levels. (B5, B6)
8. **The head phrase is not repeated mechanically.** Each synonym appears where it owns a heading or a
   sentence; the same project or developer is never renamed inside one section. (A7, H1, disagreement 5)
9. **The listings are also a real HTML table or a list with fixed fields** that a machine can read
   without running scripts: project, developer, city, neighbourhood, room range, price from, delivery
   date, status, date checked. Unknown fields are left out, not filled. (C5, C7, F2, F3, F5)
10. **At least one comparison table per family** (for example cities side by side, or immediate
    occupancy against off-plan), with clear column headers and rows that stand alone. Aim for three
    tables on the page in total. (C2, C5)
11. **Prices appear in the body and tables with a full date, never as a static figure in the title.**
    Treat a price in the opening lines as a test, not a rule. (C2, C3, C6, disagreement 4)
12. **Every number that matters is visible text**, not only in markup, a script, a tab that loads
    later or inside the map or the tool. (C7, F3, H12)
13. **The map and any tool stay on the page** and each has a text or table twin that carries the same
    data. Heavy media at the bottom is checked for load cost. (F2, F3)
14. **A question-and-answer block answers real questions about the category** (taken from what Google
    shows for the head phrase and its family), nested under broader questions, with no generic filler
    text at the bottom of the page. (B7, E3, F2, disagreement 8)
15. **A visible "last updated" date that a machine can read**, changed only when listings, prices or
    dates really change. Because listings do change, a real review at least every one to three months
    is supported by the freshness data for ChatGPT, Gemini and Perplexity. (C4, D7, H15)
16. **Named, specific entities are dense in the opening and in each section**: project names,
    developers, neighbourhoods and streets, not general phrases such as "many projects across the
    country". (D4)
17. **A Hebrew prompt library is run on each engine**: 30 to 50 prompts built from the head phrase,
    its families and cities, each run three to five times inside a fixed 24 to 72 hour window, with
    the sub-queries, cited URLs and competitors recorded. Record how many of ChatGPT's sub-queries come
    out in English; if many do, the English twin of the page matters for citation of the Hebrew one
    (my inference from one unverified data point). (D2, D8, E1, E2, E4)
18. **For each family, the best passage on /projects/ is compared with the passage the engine cites
    today**, and the gap is named: missing number, missing date, missing entity, vague scope, or buried
    position. (E2, E5, B3)
19. **Internal links to /projects/ use varied natural anchors with at least one exact head-phrase
    anchor**, are plain HTML links, and are added gradually. Inside the page, link blocks to project
    pages come after the answers. (A9, G1, G3, G5, G6)
20. **Markup describes only what is visible**: question-and-answer markup only on the real Q and A
    block, list markup that matches the listings shown. It is treated as hygiene; no result is
    promised from it. (D6, H8)

### Five things the authors would warn against

1. **Writing an "ultimate guide".** A very long page that covers everything was cited less than a
   focused one in the largest data set here, and the end of a page is almost never used. Length is
   justified only by real listings and real data, section by section. (B2, A5, H17)
2. **Leading with navigation.** City menus, filters and link grids above the first paragraph use up
   the part of the page the engines read first. (A5, G5)
3. **Trusting markup, llms.txt or a static price in the title to do the work.** The controlled tests
   found no gain from markup, almost no machine ever requests llms.txt, and a static price in the title
   lost traffic. (D6, H10, C6)
4. **Stuffing the head phrase or its synonyms.** The one controlled test on generated answers found
   repetition was the worst of nine methods. (A7)
5. **Faking freshness or judging from one check.** Dates changed without content changes are called
   out by both Koray and Ahrefs, and citations turn over within days, so a single screenshot of an AI
   answer proves nothing either way. (D7, D8, H15)

One more caution that comes from the evidence itself: SearchPilot's real-estate customer saw only six
wins in 36 tests. Most confident on-page advice, including some in this file, does not move traffic
when tested. Change one thing at a time on /projects/ and read the result in Search Console.
