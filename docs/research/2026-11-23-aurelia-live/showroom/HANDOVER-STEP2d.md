# Aurelia showroom: hand-over step 2d (HAD-810, 24.11.2026, Opus 5.5 build agent)

## 1.72.760 closed
deploy760.py ended "RELEASE 1.72.760 LIVE", no bridge left, exit=0, 0 failed rows. The RELEASE DONE 1.72.760 line was written (by
another hand at the same minute; my duplicate was removed).

## 1.72.761 RELEASED (swap showroom.js + showroom.css; commits 3aa453a7, 5c954102)
- (b) desktop: the view from the floor opens large under the tower + panel (viewBig, from c371fe63).
- Phones: `fitPhone` makes the compact map run on under the site's bars to the screen bottom (`--nlas-mapcov`, map padding
  bottom = cover, `showBeam` zooms from the visible height); the strip "מה יש לכיוון" is wholly below the screen at the flat rest.
  `.nlas-mapbig` and the Mapbox bottom controls sit at `bottom: var(--nlas-mapcov)`.
- `tidy`: price pills avoid areamap's symbol layer `nlam-pin` (stations, places), `nlam-home`, `nlas-plans`, the DOM markers, the
  site's bars and the map's logo/attribution/buttons: they are offset with CSS `translate` (12/22/32 px tries), else hidden;
  re-run after the page rests from a scroll (passive listener, no capture).
- Every block has `scroll-margin-top` (64 phone / 124 desktop) and `scroll-margin-bottom: var(--nlas-barh)`; `.nlas` has bottom
  margin = bars height on every width; `setBarVar` on boot and resize.
- `fitDesk` (desktop): the panel picture height `--nlas-pmh` (232 -> min 110) and, if still too tall, `.nlas-tight` (the floor's
  flat chips fold, tighter facts) so the requests, the deals line and the note end above the bars (1280x720: note bottom 567, bar 574).
  Re-run after the deals line loads. Desktop walking range moved to the map's top-left (away from the a11y button).
- press3.py gained: pills vs markers + under bars, strip rest at the flat state, every block can rest clear (both directions),
  the call press scrolls like a visitor. LIVE press: 360x740 25/25, 390x844 25/25, 1440x900 / 1280x720 / 1920x1080 19/19,
  press_viewbig live (8 tags, card, closes on the plan tab), 0 console errors. Frames `live3/`, `live3/live-phone-flow-761.mp4`.
- source_audit after: byte-only on aurelia, rainbow, ashira, h-infinity (h-infinity YELLOW = its old 168-char description).
  content_first_check 0 failed. Linear comment, Notion row, LOOP.md line, D:\00 מוכן להצגה\ number 30 replaced + read-me line.
- The run's check rows (deploy761.py, ~1,750 rows, ~2 h) and the RELEASE DONE 1.72.761 line: see the bottom of this file.

## Step (c) BUILT LOCALLY, NOT RELEASED (commit e1f42472): furnished plans with room names and sizes, opening large
- `planRooms(f)` = the same split planSvg draws (name, kind, m², sample data); `CUTLAB` = label anchors (percent) per picture
  (cut-r3/r5/r6, measured by eye; the pictures were drawn from D:/Media/Aurelia/v4/cut/plan-*.png); `cutLabels`, `planBig(on)`.
- Desktop: the button "התוכנית בגדול, עם המידות" (or a tap on the picture) widens the panel column to min(780px, 58%) beside the
  tower; names + m² on every room, "מרפסת לים"/"מרפסת" on the balcony. Phones: the band's "תוכנית הדירה" opens it large at once:
  full width, numbered rooms, the list under the picture. Other tabs close it.
- Pressed locally: `press_plan.py` 0 BAD at 360x740, 390x844, 1280x720, 1440x900 (labels on the picture, none overlapping, tower
  on screen on desktop, list on phones); press3 regression 390 25/25, 1440 19/19. Frames `local10/`. Board section ROUND 762 is up.
- To release: after RELEASE DONE 1.72.761, read the lock tail + health in a separate command, CLAIM 1.72.762, source audit
  before, `python scripts/project-stage/make_deploy762.py` (ready, built on deploy761.py), run deploy762.py in the background
  (log `_deploy762.log`), then `LIVE=1 press3.py` at the 5 sizes + `LIVE=1 press_plan.py` at 390 and 1440 into `live4/`.

## Not done / below the standard (honest)
- No 4-room sample exists in flats.json (rooms 3, 5, 6 only): no 4-room plan was invented. The 6-room cut-away already existed.
- Desktop plan-large: the panel then runs below the fold; the lower requests rest partly behind the WhatsApp bar until scrolled.
- Phones: the Mapbox logo sits behind the walking-range column (older than 761).
- The deals line says "5 חדרים" for the 6-room flat (the data bucket is r5); not changed.
- The view tags in the small panel view still crowd on phones.
- Floors with sample flats in flats.json: 6 to 46 (41 floors, none missing); floor 47 and floors 1-5 carry no sample flat, so
  they cannot be chosen as a flat (nothing invented). Whether 47 should be choosable is a data question for the coordinator.
- (d) tower from the sea + aligned tap layer, (e) floors to 47 check (press3 found every tested floor choosable; a full
  47-floor sweep was not run), (f) board PNG export to board-png/: NOT started.
- Not checked: a real phone, iOS Safari, the call room itself (answered "not now").

## RELEASE DONE 1.72.761
deploy761.py ended RELEASE 1.72.761 LIVE, no bridge left, exit=0, 0 failed rows; RELEASE DONE line written, lock released. 1.72.762 is NOT claimed.
