# Aurelia showroom: hand-over step 2c (HAD-810, 24.11.2026, Opus 5.5 build agent)

Coordinator's review of the live 1.72.758 frames -> PART A fixes (one release, 1.72.760), then PART B (b..e), each its own release.

## PART A: what changed (assets/aurelia-viewer/showroom.js + showroom.css only; PHP untouched)
1. Phones: `.nlas-band` between the stage and the map (`bandFlat`): the cut-away picture ("תוכנית הדירה", tap = the plan in the
   panel, `reveal()` above the bars), rooms · m² / floor · direction / "שלב: קונספט" · "דירה לדוגמה", and "הדירה מעניינת אותי"
   (lead form prefilled). `fitPhone()`: the stage height (`--nlas-stageh`, 36svh, lower on short phones) and the compact map height
   (`--nlas-maph`) are set so the map ends where the site's bars begin. The panel's facts grid is hidden on phones (the band has them).
2. The site's floating bars (#nlcta WhatsApp, #nl-sticky lead row, #nla11y) are measured at runtime (`bars()`, `barTop()`), never
   moved or restyled. Phone: the map ends at the bar line; `--nlas-barh` = bottom margin and scroll-margin; the call sheet is
   brought above the bars (`reveal`). Desktop: the panel's requests moved under the facts (2 rows), media 232 px, a shorter
   declaration line: at 1440x900 the panel ends at 745 px, the bar starts at 754 px.
3. "דילוג" sits in the landing spot (phone: the band's left end; desktop: the panel media's corner).
4. Compact map (`mapTidy`/`tidy`/`plansLayer`, from outside areamap.js and the map section): the page's nameless plan dots hide in
   the compact map and the same plans are drawn as a named Mapbox symbol layer `nlas-plans` (below `nlam-pin`, collision on, the
   language twins -en/-ar/-ru/-fr collapse; a project known only by a foreign page is not drawn); price pills: nearest wins, an
   overlapping one (or one under the chips / range / full-map button) waits. Full map = unchanged.
5. Pull-out rewritten, 1.2 s: the facade slice of that balcony (the same photo) leaves the tower (perspective at the balcony, a dark
   socket stays), turns into the glass volume, flies to the panel / the band, opens into the furnished cut-away (phones: then
   shrinks into the band's picture). Reduced motion = no flight. No wheel/touch capture.
6. Cues: "בחרו דירה על המגדל" (tower, before the tap), "האלומה מראה לאן הדירה פונה" (above the beam's tip, fades on the first touch of
   the map or after 12 s), "לחצו על מקום בנוף" (view, fades after the first tag).
Test kit: `press3.py WxH [OUT]` (LIVE=1 for the live page; otherwise the live page with the module served from disk). Local result
`local7/`: 360x740 22/22, 390x844 22/22, 1440x900 17/17, 0 console errors. Design frames for A on the board (section "ROUND 2C").

## Release
- make_deploy760.py (built on deploy759.py) swaps showroom.js + showroom.css. Source audit BEFORE done 24.11 ~01:30 IL (byte-only).
- Status: see the bottom of this file.
