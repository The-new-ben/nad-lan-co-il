# Aurelia showroom: hand-over step 3 (HAD-810, 24.11.2026, Opus 5.5 build agent)

Read HANDOVER-STEP2e.md first (1.72.762 in full: clearRest/settle, floors 6..47, building 47/320, "5 חדרים ומעלה").

## LIVE
- 1.72.762 (showroom.js + showroom.css + flats.json): RELEASE DONE, 1761 rows OK, 0 failed. Frames `showroom/live4/`, recording
  `live4/live-phone-flow-762.mp4`.
- 1.72.763 (showroom.js + showroom.css), coordinator's review of the live 762 frames: state at the bottom of this file.
  1. Tower: when the flat's label ("דירה 2 · קומה 20") would touch the video-call pill, the label hangs under the balcony instead
     (`.nlas-mark.below`, measured in redraw). Both visible, the tower never hidden.
  2. Phones, plan opened large: the picture comes first, right under the site header (`reveal(m, cutbox)` + `settle(cutbox, 6)`:
     the picture may not slide more than 6 px under the header); the illustration note and "הקטנת התוכנית" sit in their own row
     UNDER the picture, then the room list. If no scroll leaves every request button clear of the bars, OUR picture narrows 3 % a
     step down to 70 % (`fitRest`, `--nlas-planw`); short phones (<= 760 px high) start at 94 % with a tighter list.
  3. The small plan (cut tab, not large): note, floor key ("תוכנית הקומה") and "התוכנית בגדול, עם המידות" in a row of their own
     above the picture; "גוררים את הספה" under it. Nothing of ours lies on our picture or text.
  4. The penthouse plan (wide picture, ar 2.67) on phones, opened large: the picture at min(68vw,300px) high in its own strip that
     the finger moves sideways (the browser's own overflow scroll, no touch capture), cue "גררו לצדדים לכל הדירה"; numbers + list stay.
  5. Floor 47 on the tower picture: NOT done, deliberately. The pick layer has no honest element for it: the model's crown is
     `TOWER_crown_plant_floor` ("קומת מערכות בכתר", a plant floor) and `TOWER_slab_roof` is the roof; floor 47 does not exist in the
     Blender model v2 (N_FLOORS = 46). Making the crown open a flat would be inventing. Floor 47 opens from the arrows (and the deep
     link #dira=47-1). To make it tappable honestly: add a 47th residential floor to scripts/aurelia/aurelia_v2.py, re-render the
     plates and id passes (all four views), rebuild data.json; that is a model change for the coordinator to order.
  6. Phones: the walking-time column (ours) gets lower buttons (32 -> 24 px, `rangeFit`, `--nlas-rgh`) so it ends above the
     Mapbox logo; the logo and attribution are untouched.

## Answers the coordinator asked for
- Floor 47: opens ONLY by the arrows (and the link #dira=47-1). It is not tappable on the tower, deliberately (reason in item 5 above).
- The faded "וואטסאפ" text on the site's green bottom button is REAL, not a capture artefact: on the live page (390x844, wacolor.py)
  the computed colour of #nl-sticky's "וואטסאפ" link is rgb(47,111,134) (teal) on background rgb(31,138,76) (green), about 1.2:1
  contrast; "מעניין אותי" next to it is white on rgb(194,86,58). It is the site's bar and Ben's wording: nothing was changed.

## NOT done
- (g) phone view tags crowding, (d) tower from the sea + aligned tap layer, (f) board update + PNG export: see the bottom.
- 267 sample flats vs the declared 320 (the model's floor layouts not redrawn: a design decision).
- No board frame for 762/763's fixes. Not checked: a real phone, iOS Safari, the call room itself.

## 1.72.763 RELEASED (showroom.js + showroom.css): 1768 rows OK, 0 failed, RELEASE DONE written
Live press (live5/): press3 360/390/1440/1920 0 BAD; 1280x720 2 BAD (the small plan's own rows pushed the short-desktop panel's
deals line under the WhatsApp pill and the call sheet below the screen); press_plan 360/390/1440 0 BAD; floors 390 0 BAD.
Recording live5/live-phone-flow-763.mp4. Source audit after byte-only; content_first_check 0 failed.

## 1.72.764 (showroom.js + showroom.css), coordinator's review of the live 763 frames
1+2. Short desktops (.nlas-tight, about 720-770 px high): the small plan keeps its note and "large" button only (the floor key is
   in "התוכנית", the designer link in the large plan) and the picture row gives the height back (--nlas-cuth); the panel ends
   above the bars again (1280x720: last line 572, bar 574) and the call sheet opens inside the screen (262-437).
3. One rule for every view tag box (phones and desktop): tags never lie on each other (4 px apart); on a small view at most three
   (the first in the list win), the rest wait for the large view (`placeIn`). This also answers (g) on phones.
4. The full-width plan's note and "smaller" keep a 16 px gutter.
Local press (local14/): press3 1280x720, 1366x768, 390x844, 360x740 0 BAD. Live: see live6/ and the lock file.

## 1.72.764 history (honest)
- Run 1 rolled itself back after its checks: 3544 rows OK, 6 BAD = one row asking showroom.css for the text "1.72.764 (HAD-810"
  (make_deploy764 inherited it by renaming 763 -> 764; the file had no such header). Code was right. Log `_deploy764-run1.log`.
- An attempt as 1.72.765 aborted before any write (the runner bumps live + 1 only). Lock lines written for both.
- Run 2 (same number 1.72.764, header added, plus the 360 penthouse fit: our picture may narrow to 60 %): see the lock file and
  the bottom of this file. The .bak764 files on the server are 1.72.763's (made once, before run 1's writes): a correct rollback target.
- The 06:48 live press at 1280x720 (call sheet 699..874) was taken while the files were being swapped; the coordinator's 06:55 re-press
  (live6/coord-check/) showed 304..479, 0 BAD.

## ROUND 765 for the next agent (coordinator's order, 24.11; showroom.js / showroom.css only, /projects/aurelia/ only, frames live7)
Do not claim before RELEASE DONE 1.72.764 is in the lock file.
1. PREPARED LOCALLY (bottom of showroom.css, "765 (prepared, not released)"): the site's green "וואטסאפ" text is white again on
   Aurelia by restoring the colour the bar's own stylesheet states (.nl-sticky__wa { color: #fff } in showroom-engine/showroom.css loses
   to body.nl-skin-a .entry-content a). Not pressed yet: measure before/after with wacolor.py (live: teal rgb(47,111,134) on
   rgb(31,138,76), about 1.2:1), keep a phone frame, and LIST read-only which other pages render #nl-sticky with teal text
   (einstein-tower and the engine pages); do not fix them.
2. NOT STARTED: low desktops 1280x720 / 1366x768 at rest BEFORE any tap: the facility cards at the foot of the side column
   ("הבריכה האולימפית · 50 × 25 מ'") rest half under the WhatsApp pill. Make the intro column end above the pill (smaller cards or one
   row less) and add a stage-rest check to press3 (every showroom control fully above the bars or off screen before the tap).
3. NOT STARTED: low desktop, flat open: the small furnished plan reads as a ~100 px thumbnail on a white band (since 764 the
   .nlas-tight cut row is --nlas-cuth: max(56px, pmh - 56px) on #f1f0ec). Let the picture fill its row by height on the panel's dark
   ground (drop the light background of .pn-cut in the small cut tab), keep the note and the "large" button.
4. Floor 47 on the tower picture: decide by eye on the four plates (img/street|pitch|pool|aerial-1600.webp, the top level under the
   roof). If it reads as a glazed, lived-in level, give that level's pick area to floor 47 (new card bal:47:1/2 -> flat key
   AUR-SAMPLE_47_u in data.json, from the id pass groups of TOWER_slab_roof's level / the crown); if it reads as a systems screen,
   leave 47 on the arrows and fold "a 47th residential floor in aurelia_v2.py + re-render all views" into the sea-side render job.
5. Check that no visible text or count shows 267 (or any building size other than 320 / 47): press_floors.py already checks 265 and
   "46 קומות"; add 267.
6. Then (d) the tower from the sea with an aligned tap layer (Chrome "gmktec" was connected at 02:00 UTC), (f) the board brought up
   to date and PNG exports of the CURRENT live frames into showroom\board-png (the files there are from 23.11 22:44).

## 1.72.764 RELEASED (second run): 1775 rows OK, 0 failed, RELEASE DONE written, lock released
Live (live6/): press3 0 BAD at 360x740, 390x844, 1280x720 (re-pressed after the checks; the first press caught the swap), 1366x768,
1440x900, 1920x1080; press_plan 360/390/1280 0 BAD; floors 390 0 BAD. Source audit after byte-only; content_first_check 0 failed.
Round 765 is NOT claimed: the brief is above (item 1 prepared locally in showroom.css, uncommitted to the site).
