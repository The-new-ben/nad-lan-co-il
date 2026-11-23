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

## RELEASED 1.72.760 (24.11.2026, swap showroom.js + showroom.css; commit ec5ed951)
- Files live and md5-verified at the start of the run; health 1.72.760. Pressed LIVE (`LIVE=1 press3.py`): 360x740 22/22,
  390x844 22/22, 1440x900 17/17, 0 console errors. Numbers: map above the bars 204 px (360) / 205 px (390); pull-out 10.1-10.4 s at
  12% speed = ~1.22 s; skip at the band's left end (phone) / the panel media corner (desktop), touching nothing; compact map 0 nameless
  plan dots, 0 overlapping pills (3-4 pills kept, 1-2 named plans); call sheet rests above the bars (390: 267-443 vs bar 646;
  1440: 253-428 vs 754). Frames `live2/live-*.png`, recording `live2/live-phone-flow-760.mp4`. Copies in D:\00 מוכן להצגה\ (30, 24.11).
- The release run's own checks (deploy760.py, ~1,740 rows, ~2 h) and the RELEASE DONE line: see `scripts/project-stage/_deploy760.log`
  and docs/coordination/claude-codex.md. If the run was cut, finish with `deploy760.py --finish` or roll back with `--rollback`.

## PART B state
- (b) DONE LOCALLY, NOT RELEASED (commit c371fe63): `viewBig(f)`: on desktop the view tab opens the view large in a grid row under the
  tower + panel (1240 x 714 at 1440), the same tags (tappable, card inside), the cue, "×" closes, another tab closes it; `reveal()`
  keeps it under the site header + section tabs. drawTags/placeTags/tagCard now work on every tag box. Pressed locally with
  `press_viewbig.py` (1440: 8 tags, card opens, closes on the plan tab; 390: no big row, panel view as before; 0 errors), frames
  `local8/`. Next: `make_deploy761.py` = copy of make_deploy760.py with PREV/NEW 760/761 and rows for `function viewBig(` and
  `.nlas-viewbig`; source audit before/after; LIVE=1 press3 + press_viewbig; board frame first (the board has no (b) frame yet).
- (c) Hauzd-level plans for 3/4/5/6 rooms (6-room cut-away missing): NOT started.
- (d) tower from the sea + aligned tap layer (Blender id pass): NOT started.
- (e) board YEQCKbPrDQmcXqH7TkFMuH: section "ROUND 2C" added with the LOCAL frames of A (before the release); still to do: replace
  with the live2 frames, add (b), retire the old cockpit sections, export every artboard as PNG to board-png/.

## Honest gaps after 1.72.760
- On a 360 phone the strip "מה יש לכיוון" starts right at the bar line: its first word shows to the right of the WhatsApp bar
  (the bar is 259 px wide). Not a button; the strip is reached by scrolling.
- The fixed bars always cover something while the visitor scrolls; the showroom guarantees its settled states only (after the tap,
  after "תוכנית הדירה", after the call sheet).
- Desktop panel fits above the bars at 1440x900 with the page settled at the showroom top; shorter desktop screens not measured.
- The view tags on the panel's small view still crowd each other (b answers this on desktop only).
- Not checked: a real phone, iOS Safari, 1280/1920 desktops, the call room itself (answered "not now" in every press).

## After-checks done while the 760 run was still in its row checks (24.11 ~01:55 IL)
- source_audit after: aurelia / rainbow / h-infinity / ashira byte-only diffs (version strings); h-infinity YELLOW = its old 168-char
  description, unchanged. content_first_check on Aurelia: 0 failed (phone + desktop).
- Linear HAD-810 comment posted, Notion row "אורליה ספורט" (next step + evidence) updated, LOOP.md line, D:\00 מוכן להצגה\ number 30
  replaced with the 24.11 live frames + recording, read-me line updated.
- OPEN when this agent stopped: deploy760.py was still in its ~1,740 check rows (about 300 done at 01:55 IL, background run, log
  `scripts/project-stage/_deploy760.log`, last line `exit=N` when it ends). Whoever picks up: when the log ends with
  "RELEASE 1.72.760 LIVE" + "no active temporary bridge left" + exit=0, append the RELEASE DONE 1.72.760 line to
  docs/coordination/claude-codex.md (lock released). If it died mid-way: `python scripts/project-stage/deploy760.py --finish`
  (lock still HAD-810's). Do not start 1.72.761 before that line.
