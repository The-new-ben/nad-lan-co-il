# The page loop: content gaps → the deepest page on each topic (started 22.10.2026 evening)

**Ben's order, 22.10.2026 (voice, verbatim gist):**
- Keep looping and don't stop until he says so. Opus 5.5 is fine.
- Research the gaps against the competitors that lead on Google. Find the content we lack and build pages on it: supporting content on high-volume keywords.
- Abroad is in scope: Cyprus, Italy, Thailand, Dubai, and more, for example Greece.
- Be very careful with cannibalization:
  - URLs don't start with the same keywords;
  - titles don't start with the same keywords;
  - check that we don't already have these titles;
  - title, breadcrumb and H1 are never the same string.
- Pages full of information, numbers and tools. Give an honesty statement and prove we are above every other page in the depth of information. Then deepen with more pages and link them.
- Tools: ultra complex, with UX where one tap with a finger gives everything. Price lists, generators, legal, accounting, valuation and engineering.
- Prove it's better. Languages too.
- Upload without waiting for permission.
- Never without Claude Design. Infographics and animation.
- Index on Google, every search engine and AI bots.
- Learn the competitors' DNA (language, keyword density, titles, headings), replicate it, and make it much better.

Linear: **HAD-592**. Tracking: Notion row per wave.

## Every loop turn
1. Read this board, the memory handoff top section, and live health (`/wp-json/nadlan/v1/health`).
2. Take the first item below that is not done and not blocked. Do it end to end:
   - **Research:**
     - keyword volumes, from DataForSEO for Israel and Hebrew (location 2376, language he);
     - the SERP and its People Also Ask, with the AI Overview written as "absent" when none is shown;
     - the top 5 competitors read in full: their DNA, density and structure;
     - Search Console for our own coverage.
   - **Cannibalization gates:**
     - `python tools/gsc/url_word_audit.py --token <word>`: the URL never starts with a word an existing URL starts with, and no word repeats inside it;
     - `python tools/title_start_audit.py --check "<H1>" --check "<SEO title>" --trio "<SEO title>" "<H1>" "<breadcrumb>"`: no 2-word start clash, three different strings;
     - Search Console query/page for the intent;
     - sister sites (cy-prus, thai-land, dubai-team, tra-vel): never target a query a sister site ranks for; take another angle and link to it.
   - **Claude Design first:** the page pattern in DS artifact https://claude.ai/artifact/L9Nqz7Viv7K3MYeZrBc9s8. The tools follow the NadLan Instruments system (Karantina, IBM Plex Sans Hebrew, IBM Plex Mono).
   - **Build:**
     - the page HTML in `docs/research/<date>-<topic>/pages/`;
     - tools in `plugins/nadlan-config/assets/instruments/tools/*.js`;
     - data in `assets/instruments/data/*.json`, every number with a source and an as_of date.
   - **Release:** tools go through the runner chain (`scripts/project-stage/make_deployNNN.py`, a lock line in `docs/coordination/claude-codex.md`, one runner at a time).
   - **Publish:** REST with a guard (slug free), read-back, then the live checks:
     - one H1;
     - title ≠ H1 ≠ breadcrumb;
     - the answer paragraph before the tool;
     - FAQPage and BreadcrumbList;
     - `tools/source_audit.py` GREEN;
     - phone at 390 px: no horizontal scroll, cards full width.
   - **Proof:** a depth table, ours vs each competitor: words, figures, tables, tools, FAQ answers, sources, freshness. Plus an honesty statement listing what we did NOT beat.
   - **Links:** in from 2-3 relevant pages (names already written become links) and out to the cluster.
   - **Indexing:** the URL is in the Yoast sitemap. On Ben's 22.10 word ("make sure they index"), resubmit the sitemap through the Search Console API once per wave. IndexNow and llms.txt come per the board.
   - **Log:** a Linear HAD-592 comment, a Notion row, this board, the memory handoff.
   - **Report:** send Ben the links in short Hebrew.
3. Never stop for a question. A question goes under "Waiting for Ben" and the loop moves on.

## On-page rules (what every page passes)
- **Three different strings.**
  - The H1 is the WordPress title. It owns the full intent.
  - The SEO title is ≤ 60 characters and opens with the head keyword in a different phrasing from the H1.
  - The breadcrumb label is 1-3 words.
  - All three are checked with `--trio`.
- **The opening.** The answer paragraph opens the page: it answers the query with the key numbers in its first 2 sentences.
  - Then the tool, opened on the page's own case.
  - Then the deep sections: tables, an infographic, the cost or tax breakdown, risks, the process.
  - The FAQ (h3 questions) closes the page.
- **Keyword placement.** The head keyword goes in the SEO title, the H1, the first 100 words, at least two H2s, and one image alt or caption. Density follows the competitors' range (from the DNA file) and is never stuffed.
- **Honesty.**
  - Every number has a source and a date, kept in the repo (the page carries no citation clutter, by the research law of 3.10).
  - Unknown values are omitted.
  - No legal or tax advice tone. Facts, and when to ask a professional (with a link to our pros).
- **Language.** The language-DNA skill and the forbidden-words list apply. No visible em/en dashes, so the source audit stays GREEN.
- **Abroad pages.** Prices in € with ₪ at the Bank of Israel rate (data/boi-fx.json). The Israeli tax side is always included, since that is what the competitors miss.

## The board

| # | Item | State | Evidence / notes |
|---|---|---|---|
| G0 | Gap map across countries and Israel topics (keyword volumes, SERPs, our and sister coverage) | **done 22.10** | docs/research/2026-10-22-content-gaps/gap-map.md (21 candidates, ranked) |
| E1 | Engine: one-tap presets, € formatting, opt-in page trail [nadlan_crumbs], /llms.txt, IndexNow, Hebrew profession headings | **done 22.10 (1.72.498)** | IndexNow 202 for 8 URLs |
| N1 | Yad Eliyahu price section | **done 22.10** | page 7103, all checks OK |
| G1 | GREECE wave 1: /athens-apartments/ (8572), /acquisition-greece/ (8573), /taxation-greece-israel/ (8574) + tools grbuy/grgv/gryield + hub fixes (one H1, 2026 facts, guides list, sitemap) | **done 22.10 (1.72.499)**: proof 22/19/13 of 25 facts vs best competitor 7 (PROOF.md); still behind on words and photos: deepen in a later turn | facts.md/facts.json (sources), serp-dna.md, build_pages.py, publish_pages.py, DS v227 AbroadGuide; then fix_str_page.py (page 398 leftovers) |
| G2 | Greece wave 2: seaside houses, Thessaloniki + Halkidiki, Crete (seasonal: before March 2027), Russian versions of wave 1 | todo | serp-dna.md section 6 |
| C14 | Purchase tax calculator upgrade (31,160/mo, we were at position 56) | **done 22.10 (1.72.500)** | live errors fixed (temporary order 31.12.2026, 24 months, oleh cap, disabled); ptax v2 with upgrader date + presets; page 6 rebuilt (4,422 words, 23 FAQ); guides 529/532 fixed; proof 24/25 vs 16 (PROOF.md) |
| GP | GREECE PRICE LIST (Ben 22.10 evening: the most comprehensive anywhere, all competitors incl. Greek sites, map/infographics/new tools, link to jus-tice) | **done 22.10 (1.72.501-503)**: /prices-greece/ (page 8585), 253 places on a map + budget + Israel tools; proof 31/35 facts vs jus-tice 21 and 4-11 for the 7 other ranking pages (PROOF.md); phone fixes measured live (labels, 10 px dots, 15 px names); jus-tice linked at /greece-lawyers/ only | docs/research/2026-10-22-greece-prices/ (dna.md, prices.json, PROOF.md); gaps named: price by flat size, Europe comparison, forecast |
| N2 | Contractor register: /pinkas-hakablanim/ with a server search over 17,874 contractors (14,400/mo, no competitor search) | **done 22.10 (1.72.504-505)**: page 8591 live, search route + tools pinkas/sivug, proof 31/32 facts vs best competitor 13 (PROOF.md), links in from /renovation-contractor/, /buying-apartment/, /construction-supervisor/; TODO: a link from /profession/קבלן/ (term description, not in REST: needs code) and from the /professionals/ directory | docs/research/2026-10-22-contractor-register/brief.md; mass pages for the 15,184 missing contractors need Ben's word on pace |
| K1 | Kit: nlag.bars as HTML rows (the SVG made 6 px names on phones and cut Hebrew labels, measured live on /prices-greece/) | **done in code 22.10**; republish /prices-greece/ + the 3 wave-1 pages after 1.72.504 | tools/guides/nlag.py |
| C12 | Condo documents (tsav, takanon, tashrit), 12,530/mo | todo | gap-map ★2 |
| C15 | Home inspection upgrade, 10,500/mo, position 63 | todo | gap-map ★3 |
| C13 | Capital gains tax guide + calculator, 23,280/mo, 2 impressions | todo | gap-map ★5; first find why the tax family is invisible |
| C01 | Georgia (Batumi, Tbilisi), Hebrew + Russian, 1,520/mo | todo | gap-map ★4, no sister site covers it |
| C17/C11/C02/C16/C03 | Deciding appraiser, landlords' tax, USA, appraiser, Israeli tax on property abroad | todo | gap-map ★6-★10 |

## Waiting for Ben (the loop goes on meanwhile)
- findplace vs nad-lan split for neighbourhood place pages.
- jus-tice.co.il vs nad-lan for abroad: jus-tice's /greece-price-list/ ranks 3-5 for Greece prices, so nad-lan has no Greece price page. The working split, until Ben says otherwise: nad-lan = market, buying, costs, tax tools; jus-tice = the legal angle.
- Pace for contractor pages: 15,184 register contractors have no page with us; mass creation needs his word.
- Our own defects logged: /global/project/koukaki-athens-residence/ claims golden visa "with another property" (wrong under the 2024 single-property rule) and pitches Airbnb in Koukaki (Athens district 1 freeze); nad-lan /price-list-dubai/ duplicates dubai-team's list; ?lang=en on /global/ declares he-IL.
