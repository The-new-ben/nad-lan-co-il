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

## The site's green "וואטסאפ" button text (owner's question; no change made)
See the bottom of this file (checked on the live page with the computed colours).

## NOT done
- (g) phone view tags crowding, (d) tower from the sea + aligned tap layer, (f) board update + PNG export: see the bottom.
- 267 sample flats vs the declared 320 (the model's floor layouts not redrawn: a design decision).
- No board frame for 762/763's fixes. Not checked: a real phone, iOS Safari, the call room itself.
