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
