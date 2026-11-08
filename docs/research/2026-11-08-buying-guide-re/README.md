# /buying-apartment/ (page 9): full reverse engineering and the proof (HAD-686, from 8.11.2026)

Ben's order, 8.11.2026, by voice: make the guide for "קניית דירה" the best and biggest in the world, prove it scientifically, and prove that every piece of information on Amit Vered's guide is on ours.

## Method (what makes it a proof, not a claim)
1. **SERP pass.** 37 searches of the family, Google Israel (location 2376, Hebrew), desktop, through DataForSEO live advanced, with AI answer and people-also-ask. Raw JSON is kept private (`_private-research/2026-11-08-buying-guide-re/serp/`). The family list and the earlier manual Chrome passes (7.11) are in `../2026-11-07-prices-buying/`.
2. **Extraction.** Each competitor page is fetched once as a normal browser (no crawler user agent) and parsed into ordered blocks (headings, paragraphs, list items, table cells), plus title, meta, schema types, tables, lists, numbers and official links. Raw HTML and blocks stay private (copyright); only counts and our own paraphrase are in this public folder.
3. **Unit map (Amit Vered).** Every distinct information unit on his page (fact, rule, step, warning, number, document, authority, deadline) gets a row: where it is on our page, YES / PARTIAL / NO, and what is missing. `amit-vered-map.md`, `amit-vered-gaps.md`.
4. **n-gram delta.** Document frequency of 1 to 3 word terms across the top pages; the terms that 3 or more competitors use and our page lacks (`delta-ngrams.md`). The same measure is run again after the release.
5. **Counted proof.** Words, headings, units covered, tools, tables, dated official sources, FAQ, schema: our page against each competitor, before and after (`proof-table.md`).

## Stages
- **Stage 1 (8.11 night): research.** SERP, extraction, unit map, delta, coverage before.
- **Stage 2: design, sources, writing.** Claude Design version first (DS artifact). An official-source ledger with a reading date for every legal or numeric claim. Original writing of every missing unit, in the hub's own chapters.
- **Stage 3: tools and release.** New tools where a competitor has prose and we can give a working instrument (payment schedule, signing-day kit, handover protocol, registration tracker, memorandum risk check). Release through the runner chain, source audit before and after.
- **Stage 4: proof.** Chrome at 390 and 1366, every tool pressed; the coverage measure re-run; the counted table.

## Rules kept
No 301, no noindex, no request for indexing. No competitor sentence copied. No number without an official source and a reading date. Every live link on page 9 is kept; "קניית דירה" stays with page 9; children keep their heads (see `../2026-11-07-prices-buying/keyword-family.md`). `inc/price-nudge.php` and `assets/nudge/` are not touched (HAD-684).
