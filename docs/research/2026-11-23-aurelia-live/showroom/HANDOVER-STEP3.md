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
