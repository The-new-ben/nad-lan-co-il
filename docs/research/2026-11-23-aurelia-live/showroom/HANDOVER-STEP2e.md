# Aurelia showroom: hand-over step 2e (HAD-810, 24.11.2026, Opus 5.5 build agent)

## 1.72.762 RELEASED (swap showroom.js + showroom.css + flats.json; commits 00369b4d, f1fae35b)
- Step (c) furnished plans with room names and sizes, opening large (built by the previous agent, see HANDOVER-STEP2d.md).
- Coordinator's three additions:
  1. `clearRest(anchor)` + `settle(anchor)` in showroom.js: after every showroom scroll (reveal, plan large, flat open) the page is
     nudged by the smallest step so no showroom button sits half under a site bar (bars measured by `bars()`, header by `siteTop()`,
     never moved). Candidates = every button edge against every bar/header/screen line; score = [half under a bar, anchor px under
     the header /20, half under the header, wholly hidden, |dy| (scrolling back costs double)]. Passes run again 4 x 900 ms (late
     pictures, scroll anchoring, bars that fade in) and stop the moment the visitor touches/wheels/types (passive listeners only).
     `NLAS.rest()` returns the live score; `window.__nlas.restLog` keeps the last 24 passes.
  2. Floors 6..47: `scripts/aurelia/build_flats.py` adds floor 47 (= floor 46's 6-room sample, id 47-1/47-2, flat key
     AUR-SAMPLE_47_u, z + 3.3 m) and a `building` block {floors 47, flats 320, res [6,47]}; asserts every floor 6..47 has a sample.
     The data holds 267 SAMPLE flats (model 265 + 2); the building's 320 is declared, not drawn. No visible text prints 265/267/46
     as a size (press_floors checks it). Floors 1-5 stand in the podium: the stepper simply starts at 6 (`aria-label "קומות 6 עד 47"`,
     arrows disabled at the ends). Floor 47 has no balcony on the tower picture: reached by the stepper only.
  3. Deals line: "5 חדרים ומעלה" for r >= 5 (the data's r5 bucket; same wording as inc/radius-prices.php).
  Plus: the floor key plan is drawn from each flat's model rectangle (`k` in flats.json); floors 41-45 showed the typical layout before.
- Live presses (live4/): press3 390x844 25/25, 1280x720 / 1440x900 / 1920x1080 19/19, 360x740 24/25 (see 763); press_plan 390/1440
  17/17 (incl. 47-1 and "no button half under a bar at rest"); press_floors 390/1440 7/7 (41 floors tapped on the picture, 6..47 by
  the stepper). Recording live4/live-phone-flow-762.mp4 (tap, pull-out, map, plan large, floor 46 -> 47). Source audit after byte-only;
  content_first_check 0 failed. Linear comment, Notion row, LOOP line, D:\00 מוכן להצגה\ (30, three frames + recording, read-me) done.

## 1.72.763 (showroom.js only): see the bottom of this file for its state
- Found live at 360x740: on a short phone the plan opened large was pushed DOWN (top 346) so the request rows could leave the screen.
  Fix: the anchor never drops more than 40 px; up to 110 px of it (caption + "הקטנת התוכנית") may rest under the site header.
  Local 360: buttons clear, picture top 44 (13 px of balcony sky under the header), press3 now checks the picture (.pn-cutbox) top
  >= 36 and measures 4.8 s after the tap (at rest). make_deploy763.py ready (built on deploy762.py).

## Not done / below the standard (honest)
- 267 sample flats vs the declared 320: the concept model's floor layouts were not re-drawn (a design decision for the coordinator).
- No board frame was made for 762's small visible fixes (disabled arrows, the label, the key plan) nor for (c)'s live state.
- Step 2 (d) tower from the sea + aligned tap layer: NOT started. Chrome "gmktec" was connected at 02:00 UTC (deviceId 3faca133...).
  Note: data.json already has an `aerial` view labelled "מהים" with an id pass; the showroom's VIEWS only use street/pitch/pool, and
  the old aerial tower reads as a plain box (HANDOVER.md "Known gaps"). (d) = a new plate from the same camera (or a new sea camera)
  through ChatGPT with the Blender first frame, id pass re-rendered, then a "מהים" chip in VIEWS.
- Step 2 (g) phone view tags crowding and (f) board update + PNG export: NOT started.
- Not checked: a real phone, iOS Safari, the call room itself.
