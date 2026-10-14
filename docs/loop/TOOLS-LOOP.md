# TOOLS + CONTENT LOOP (Ben, 14.10.2026) · Linear epic HAD-527

The resume point of the tools program. Every loop turn reads this file first, does ONE item to the end, then updates the
"State" block at the bottom (newest first) and the Linear epic.

## The order, in Ben's words, condensed
- Traffic. Hundreds of practical pages built around TOOLS: calculators, generators (contracts, letters, checklists),
  price lists, planners, across the whole real-estate life cycle (buy from a contractor / second hand, mortgage, insurance,
  rent as tenant or landlord, sell, taxes, urban renewal, new-build rights, renovation and engineering, design and
  architecture, materials, moving, managing, professionals), and adjacent legal / accounting topics that tie back.
- Every word Ben says is an EXAMPLE: from each, find ten more on your own.
- Every tool is PROVEN better than any competitor in Israel and worldwide, side by side (UX, depth, accuracy, sources,
  design). Ultra-complex logic, one-click UX, a practical answer. A lame tool does not ship.
- Content around every tool: the intent, the pain, data and numbers with source and date, FAQ, schema; written for Google
  and for AI answers (AIO/GEO). Start with text, lots of real numbers.
- Woven like an organ: every tool links to and from the price lists, guides, projects, listings and professionals it
  touches. No cannibalisation: existing pages first (upgrade on the same URL), url_word_audit before any new slug, no exact
  title twice, never a 301.
- Claude Design first, always, and NEVER the Claude look (global law 13.10): no cream/beige, brown, terracotta, gold.
  The tools system is "NadLan Instruments": https://claude.ai/artifact/ATybPAavyDEkAzH7cdg1bB (survey-and-planning
  palette: ground #F6F8F9, ink #12202A, sea #2F6F86, survey #C42550 for the one deciding number, land-use data colours;
  Karantina display, IBM Plex Sans Hebrew, IBM Plex Mono for figures). Every brief states palette + faces + why not default.

## One turn = one item, to the end
1. Pick the top open item from docs/research/2026-10-14-tools-program/catalog.md (ranked backlog) unless a live fault or
   Ben's word comes first.
2. Competitor proof: open the best 3 competitors (Israel + abroad), list exactly what they lack; write the side-by-side
   table into docs/tools/<slug>/proof.md (screenshots of theirs and ours after release).
3. Design in Claude Design (a Design board or a component in NadLan Instruments) before code.
4. Build on the Instruments engine (plugins/nadlan-config/inc/instruments.php + assets/instruments/): logic as a pure JS
   module with unit checks (node), official data as dated JSON, example-first UI, scenarios, copy/WhatsApp/print.
5. Page: H1 + a one-paragraph answer with a number, the tool, then the article (SERP + competitor DNA per the page research
   law), FAQ, sources kept internal, JSON-LD (SoftwareApplication + FAQPage), internal links both ways.
6. Release through the runner (lock lines, pretest, live checks), then real presses on phone and desktop, screenshots.
7. Document: Linear child of HAD-527, Notion row, this file's State, memory handoff line; a short report to Ben with links,
   the proof table, and the milestone line.

## Budget rule
Weekly usage was 58% on 14.10 with the reset on 19.10 01:00. Pace: at most one tool to the end per turn, background agents
only for research. At 80% weekly: stop building, report, wait for the reset (leads and live faults only).

## State (newest first)
- 15.10 ~00:25: LOOP PAUSED BY BEN ("finish what you are doing, then stop until I tell you to loop again", to save usage).
  Nothing in flight: 1.72.452 live and verified, lock released, all committed. Do NOT resume the loop, the CPI refresh or any
  release until Ben says so. When he does: start with the indexation + delay phone tables, then the September CPI refresh.
- 15.10 ~00:15: TURN 4 POLISH, LIVE 1.72.450-452 (HAD-533), found by looking at the live phone shot: (1) the answer figure was
  direction:ltr, so "1 מתוך 10" read backwards; now unicode-bidi:plaintext on .nli__fig / scenario / strip figures; (2) two theme
  rules with !important (inline nl-premium-ui <=600px: td padding 8px 0 + width 100%; skin-a font) stripped every Instruments
  cell on phones, and our own forced-table rule set nowrap; now core.css owns padding, fonts and borders with !important and text
  cells wrap; (3) engine option table.phoneHide (columns a phone does not need); the warranty status cell carries its end date and
  phones show two columns. Presses: docs/tools/press_warranty.py (phone + desktop, 0 errors, table 292/292). FOLLOW-UP for the next
  turn: indexation schedule now scrolls 482 in 306 and delay 323 in 306 on phones -> give both a phoneHide or a folded cell.
- 14.10 ~23:30 (machine clock; the "15.10" labels on the turn 2-4 lines below and on the 449 lock line were wrong, all of it
  happened on the evening of 14.10): TURN 4 DONE (HAD-533). LIVE 1.72.449: tool "warranty" (Sale Law bdek + warranty clock: 10 schedule items,
  bdek end, warranty end = bdek + 3 years, 20 years structural, 1-year notice for defects visible at handover) on the EXISTING
  page 4474 /real-estate-lawyer/construction-defects-lawsuit/ after its first paragraph (place_tools.py 4474=warranty, all
  checks OK). Presses phone + desktop: 7/10 -> 1/10 after the handover date moved to 2020-01-10, 11 table rows, 0 errors.
  Facts docs/tools/warranty/facts.md (from the law text). 5 tools live. NEXT, in order: (a) after 15.10 18:30 the September
  CPI: build_index_data.py + build_boi_data.py, release 450, rebuild docs/tools/cpi/page.html and update page 8403; (b) inbound
  links into the tools from /new-projects/, the glossary, the rent pages and /home-inspection/; (c) next catalogue tool (Tabu
  fees / cost of professionals / CPI-linked repayment schedule); (d) verify the next BoI decision date on boi.org.il.
- 15.10 ~01:40: TURN 4 STARTED: warranty clock (שעון האחריות). Law facts extracted to docs/tools/warranty/facts.md (schedule of
  10 bdek periods 1-7 years, structural 20 years, warranty 3 years after bdek, notice rules s.4א). NEXT STEPS: url_word_audit
  (warranty, bedek, defects) and the existing defects/bedek pages (e.g. /real-estate-lawyer/construction-defects-lawsuit/) to
  decide upgrade vs new page; tool 'warranty' (input delivery date -> per item: bdek end, warranty end, days left, status
  colour; notice deadline for visible defects = delivery + 1 year); release 449; place; presses; document.
  DECIDED: no URL owns 'warranty'; place the tool on the EXISTING /real-estate-lawyer/construction-defects-lawsuit/ (owns 'bedek'
  intent) after its first paragraph, and add /home-inspection/ to the tool's related links (no new page, no cannibalisation).
- 15.10 ~00:55: TURN 3 DONE (HAD-531). LIVE 1.72.448: tool "prime" on the EXISTING page 514
  /mortgage-calculator/mortgage-interest-rates/ (BoI official SDMX series MNT_RIB_BOI_D via tools/instruments/build_boi_data.py
  -> data/boi-rate.json: 3.25%, prime 4.75%, effective 3.9.2026); related links woven between all four tools. Runner pattern:
  write make_deployNNN.py by hand from the last released deployNNN.py (never sed-derive a maker: it regenerated 447 by
  mistake, restored from git). NEXT: (a) after 15.10 18:30 the September CPI: rebuild cbs JSON + boi JSON, release, rebuild
  docs/tools/cpi/page.html and update page 8403; (b) next tool: warranty clock of the Sale Law (verify the periods on the
  law's schedule first) or Tabu fees; (c) verify the next BoI decision date on boi.org.il before writing it anywhere.
- 15.10 ~00:10: TURN 2 DONE (HAD-529). LIVE 1.72.447 + NEW PAGE https://nad-lan.co.il/cpi-calculator/ (page 8403, tool "cpi":
  sum by known/for index, CPI-linked rent with update rules and floor, interest + linkage). Data now aligned to the CBS
  calculator at every base boundary (build_index_data.py asks the CBS calculator with value 1,000,000): ₪120,573.65 vs CBS
  ₪120,573.75. Engine fixes shipped ([hidden] really hides, tables stay tables on phones, zero legend items drop). Page
  builder docs/tools/cpi/build_page.py (all numbers from the data); publisher scripts/project-stage/create_tool_page.py
  (slug free + same-title gate + live checks, draft on failure). Research landed: docs/research/2026-10-14-tools-program/
  catalog.md (ranked backlog, 10 surprises, keyword volumes keywords.csv). NEXT, in order: (a) MONTHLY DATA: after the 15th
  (next 15.10, the September index) rebuild the JSON + release, and rebuild docs/tools/cpi/page.html via build_page.py then
  update page 8403 content; (b) links: add /cpi-calculator/ to the related lists of indexation and delay, link from the CPI
  glossary entry and rent pages; (c) next tool from the catalogue: #1 warranty clock of the Sale Law (verify periods on the
  primary source first), #2 Bank of Israel rate + prime impact (on the existing mortgage-rates page), #4 Tabu fees.
- 14.10 ~22:40: TURN 1 DONE (HAD-528). LIVE 1.72.445-446: the Instruments engine (inc/instruments.php, assets/instruments/
  core.js + core.css, data/cbs-200010.json + cbs-120010.json chained to the latest base by tools/instruments/build_index_data.py,
  checked against the CBS calculator) + tools "indexation" (page 4436 /new-projects/construction-input-index/) and "delay"
  (page 4439 /new-projects/contractor-delay-compensation/), placed after the first paragraph by
  scripts/project-stage/place_tools.py. Unit checks tools/instruments/test_tools.js (11 pass); local render
  tools/instruments/shot_harness.py; live presses docs/tools/press_live.py (phone + desktop, 0 errors). Proof tables
  docs/tools/<tool>/proof.md. DS v3 has the live Instrument component (bundle = core + tools). Lesson: plugins_url() from
  inc/ needs dirname(__DIR__) (1.72.446 fixed a 404). NEXT polish (ship with the next tool): the theme turns the detail
  table into cards on phones (force table display inside .nli), hide zero-value breakdown legend items. NEXT links: project
  pages and /new-projects/ -> both tools. NEXT tool: from catalog.md when the research agent lands.
- 14.10 ~20:45: program opened. HAD-527 epic. NadLan Instruments design system v2 published. Research agents running:
  docs/research/2026-10-14-tools-program/catalog.md (backlog, competitors, keyword volumes) and
  docs/coordination/open-threads-2026-10-14.md (everything started and not finished). Existing calculators found in
  inc/calculators.php (purchase tax, capital gains estimate, yield, equity, total cost), inc/buy-rent-calc.php,
  inc/urban-tools.php: these are UPGRADE targets on their own URLs, not new pages. Next: the Instruments engine, then the
  first tool from the ranked backlog.
