# KikarHamedinaPhoneFlow v104.3: one scroll on the phone, and places named with icons

**Design system version 104.3 (30.9.2026 evening, HAD-375).** It builds on v104 (KikarHamedinaWorld) and v104.1 (KikarHamedinaFirstScreen). The design is written jointly with Codex ("Maya", the owner's Codex session). She confirmed the diagnosis independently, read-only, in her own browser. It is published BEFORE any code ships.

## The owner's words (30.9 evening, on his phone)

- "Very, very not easy to use... scrolling inside scrolling."
- "On maps I don't want to see dots. I want labels, small labels, icons. If it's a school, it's a school icon. If it's a restaurant, it's a restaurant icon."

## Measured on the live page (1.72.372, Chrome, 390x844, real finger swipes over CDP)

Evidence: `docs/research/2026-09-30-kikar-hamedina/mobile-swipe/` (he-live.json, four shots, swipe_test.py).

| Place | What a vertical swipe does | Cause (code) |
|---|---|---|
| **The 3D world**, entered | The page moves **0 px**. The camera takes the finger. | `world.css` asks for `touch-action: pan-y`, but three.js OrbitControls writes `touch-action: none` inline on the canvas when it connects. The inline style wins. One finger = ROTATE. |
| **The floor panel** (bottom sheet over the canvas) | The panel scrolls to its end (scrollTop 165). **The page moves 0 px**, three swipes in a row. | `.nlw-panel`: 314 px box, 480 px of content, `overflow-y:auto` plus `overscroll-behavior: contain`. A scroller inside a scroller, on top of a canvas that takes touches. |
| **The area map** | The page moves 378 px (fine). | - |
| **The area map's places** | Tiny dark dots with no names. Names appear only from zoom 15.2. 233+ places in 10 minutes pile up. | `areamap.js` `icons()`: the regex strips the `<svg>` wrapper **together with** `fill="none" stroke="#fff"`, so the glyphs paint as black blobs (Codex found this). `icon-allow-overlap: true` = no collision. `text-field` only from 15.2. One icon per GROUP (7), not per kind. |
| **The world's place pins** | 9 px dots; a label that finds no room falls back to a bare dot. | `layoutLabels()` `is-dot` fallback; no icon at all. |

## The design

### 1. One finger scrolls the page. Always. (the world, inline)

- **One finger up or down** scrolls the page, even when it starts on the 3D world. The canvas gets `touch-action: pan-y` back: world.js removes OrbitControls' inline `none` right after it connects.
- **One finger sideways** turns the model: the browser hands horizontal moves to the camera.
- **Two fingers** zoom and move the camera.
- **A one-time hint** appears the first time a finger touches the world on a phone, at the bottom of the stage, for 3.5 s. Hebrew: "↔ סיבוב · שתי אצבעות לזום · ⤢ למסך מלא". It is shown once per visit (sessionStorage), with no text on screen afterwards.
- **Full screen stays the immersive mode.** There nothing else scrolls, so `touch-action: none` is right: one finger orbits. The exit button is always visible.
- **Walking on a phone opens full screen by itself.** The joystick and the look-around need every finger, so the walk never happens inside the page. The exit brings the visitor back to the same spot on the page.

### 2. No scroller inside a scroller: the panel docks BELOW the world (phones, inline)

- On a phone, and not in full screen, the floor, places and walk panel and the place card **leave the canvas**. They sit in the page flow, directly under the world, in a "dock".
- **The dock has no height limit and no inner scroll.** The page's own scroll is the only scroll. The floor slider and the facing buttons sit right under the picture they change.
- **The world keeps a fixed, calm height** on phones: `clamp(360px, 58svh, 540px)`. Below it, the dock grows with its content.
- **The panel is no longer auto-collapsed on phones.** It has room now. The collapse button is not drawn in the dock.
- **In full screen** the panel returns to the bottom sheet over the canvas, as today. There it is the only scroller on screen.
- **Nothing is removed.** It is the same panel, the same controls, the same words and the same example-apartment row (P9c). Only where it sits changes.

### 3. Places are named, with the icon of what they are (both maps)

- **One icon per kind of place, not per group.** 47 kinds are mapped to 38 glyphs, for example:
  - school = a school building;
  - kindergarten = a toy brick;
  - daycare = a baby;
  - café = a cup;
  - restaurant = a fork and knife;
  - fast food = a sandwich;
  - bar = a glass;
  - bakery = a croissant;
  - bus = a bus;
  - light rail = a tram;
  - train = a train;
  - park = trees;
  - playground = a slide;
  - dog park = a dog;
  - sport = a ball;
  - gym = a dumbbell;
  - pool = a pool ladder;
  - supermarket = a cart;
  - greengrocer = an apple;
  - pharmacy = a pill;
  - bank = a bank building;
  - ATM = a banknote;
  - clinic = a stethoscope;
  - hospital = a hospital;
  - dentist = a tooth;
  - synagogue = a Star of David;
  - culture = masks;
  - community = people.
- **The icon set** is Lucide 1.49 (ISC licence, thin ink lines, matching the house line icons in the chips and the list). The slide, the tooth and the Star of David are drawn in the same grid. It is one shared file, `assets/arealife/place-icons.js`, used by the area map, the list and the 3D world. The badge is a circle in the GROUP colour (the seven house colours stay), with a white glyph and a cream ring.
- **Every place on the map that has room gets its name.**
  - **Mapbox:** one symbol layer.
    - `icon-image` per kind, made on demand through `styleimagemissing`.
    - The badge is 26 px at street zoom and 20 px when zoomed out.
    - `icon-allow-overlap: false` plus `symbol-sort-key` = walking minutes, so the nearest place wins and the far ones step back instead of piling up.
    - `text-field` shows the name from zoom 14.
    - `text-optional: true`: when a name has no room, the icon still shows.
    - `text-variable-anchor` places the label on the side that is free, left first in Hebrew and Arabic, right first in LTR, with the RTL text plugin.
    - Cream halo, 12.5 px text, at most 9 ems per line.
  - **The 3D world:** every place pin carries the same badge (22 px). The name chip keeps its stem. When a name finds no room, the badge stays; a bare dot is never drawn.
  - **The selected place** keeps the popup / card it has today.
- **Honesty:** every icon is the kind as the source tags it (findplace.co.il / OpenStreetMap). A place with no kind gets its group's icon, never a guessed kind.

### 4. The WhatsApp bar in full screen (Codex's finding)

- The world's full screen sits at z-index 2147483000, above the site's WhatsApp bar.
- In full screen, the world's own consult button (P7, WhatsApp green, "ייעוץ חינם") stays visible in the top bar, so a visitor is never left without the one-tap consult.

## What does not change

- The beam and engine.js stay frozen.
- The panel's contents, the words, the example-apartment row and the floor, facing and time-of-day logic stay as they are.
- Desktop stays the same: the panel floats over the canvas, and the wheel zooms only after the visitor engages.
- The WhatsApp bar rules from v103 and v104.1 stay.
- Touch targets stay 44 px.
- No CSS fakes: nothing is hidden to pass a check.

## The acceptance test (both before and after, the same script)

- `swipe_test.py` on the phone emulation:
  - a vertical swipe on the world moves the page (> 150 px);
  - a swipe on the dock moves the page;
  - no element on the page has `overflow:auto` together with `overscroll-behavior: contain` inline (outside full screen).
- The area map at zoom 15 around the tower:
  - at least 12 places carry a visible name;
  - no two badges overlap;
  - every badge shows its glyph in white (pixel check: not a black blob).
- The world, aerial view on a phone: every tier-1 pin shows a badge, and none is a bare dot.
- Screenshots in he, en and ar (RTL, LTR, RTL) at 390x844, before and after.

## v104.4 (30.9 night): Codex's QA of the live 1.72.373

Codex (Maya) tested the live page, read-only, and found two things. Both are now measured and fixed in world.js.

1. **A vertical swipe scrolled the page but also tilted the camera.**
   - Measured: the camera's height went 564 → 388 after one swipe.
   - Why: OrbitControls got the first touch moves before the browser took the pan, and it applies them with damping even after the finger lifts.
   - The fix: in the page (docked), a one-finger move that is mostly vertical is stopped in the capture phase on the world. It never reaches the camera; the browser still scrolls the page. Sideways moves still turn the model, with the tilt held until the damping settles.
   - Measured after: tilt change 0.0; page moved 474 px; a sideways swipe turns the model and does not scroll.
2. **Place icons overlapped each other and covered names in the world.**
   - The fix: an icon that would sit on a higher-priority icon, name or control now steps back.
   - The aerial view shows fewer icons, each clear, and none on top of another.

## v104.5 (30.9 night): the rest of Codex's QA (docs/coordination/codex-qa-373-2026-09-30.md)

Measured locally against the live 1.72.374 (the same script, `v1045_check.py`).

| Check | Live 374 | v104.5 |
|---|---|---|
| **M15**, the area map at its opening zoom (14.4) | 61 icons, no name | 30-38 places, **each with its name** |
| **M17**, world: icons without a name | 4 | **0** |
| **M17**, world: tap areas overlapping | 2 | **0** |
| **M24**, desktop: wheel after a click on the stage | page 0 px, the camera zooms | **page 260 px, camera still** |
| Ctrl+wheel | - | zooms |
| The WhatsApp bar on the floor slider | 7 positions | **0** |

- **M15, the map.**
  - **Why the names were missing:** the right-to-left text plugin loads lazily. Tiles laid out before it arrives keep their Hebrew and Arabic labels empty; Latin text rendered, Hebrew did not.
  - **The fix:** once the plugin is loaded, the places and the basemap's name labels are laid out again.
  - The place name now shows at every zoom. The icon and its name are one unit: a place with no room steps back, and it stays in the list.
- **M17, the world** (Maya's option a):
  - A place is its name and its icon together. A place with no room steps back entirely, and it stays in the list and the cards. An icon never stands alone.
  - On touch screens the name chip is a 44 px tap area, and the collision keeps those areas apart.
  - The icon is aria-hidden; the button with the name is the control.
  - On a 320 px phone the aerial view shows fewer names, each readable.
- **M24, desktop:** in the page, the wheel scrolls the page. Zoom is Ctrl or ⌘ plus the wheel (a trackpad pinch sends the same), in full screen, or while walking. A one-time hint says so.
- **M19:** with enlarged text, the tabs wrap to two lines instead of clipping. The notes' fold is 44 px tall.
- **The card:** the focus returns to what opened it.
- **The WhatsApp bar** (a finding from the P9c agent): its list of controls now includes `#nlps input`, so the floor slider in the dock counts as a control.

## v104.6 (30.9, loop turn 14): the project is a REQUIRED mark on the area map

- **Why:**
  - Codex's QA: "the central dot stays without a visible name."
  - Google's collision model: a *required* marker always shows, and optional ones yield to it ([Google Maps collision behavior](https://developers.google.com/maps/documentation/android-sdk/advanced-markers/collision-behavior)).
- **The design:**
  - Under the page's own dot, the project's name appears as a label: ink text with a cream halo, 13.5 px, at every zoom.
  - The dot and its name are reserved space. The places' icons and names make room around them instead of covering them.
  - Implementation: a symbol layer placed above the places, and a transparent reserve for the 20 px HTML dot.
  - It is the same label on every project page with an area map (the fleet), in the page's language (the page title).
- **Unchanged:** the dot itself, its popup, the prices, the plans and the beam.

## v104.7 (1.10, loop turn 15): the long world card, organized (progressive disclosure)

- **Why:**
  - Codex's QA: the tower card ran 1,065-1,402 px on a phone.
  - [NN/G: bottom sheets](https://www.nngroup.com/articles/bottom-sheet/) and [IxDF: progressive disclosure](https://ixdf.org/literature/topics/progressive-disclosure): the key facts and the main action first, details on request.
- **The design:**
  - The card opens with the tower's own facts, "בחרו מגדל", and the WhatsApp consult.
  - The seven facts about all three towers, each with its source, sit in a fold "על שלושת המגדלים". It is closed in the phone's dock and open on wide screens.
  - The ring building's facts get the same fold, "על טבעת הבניינים".
  - Nothing is deleted; one tap opens the fold.
- **Measured (390, he):** the card is 1,077 → 489 px, with all 9 facts still in it.
- **Fixed on the way:** the green WhatsApp button in the dock showed the theme's dark, underlined link text. The dock sits outside `.nlw`, so the button's white text is restated there. This regressed in 1.72.373.

## v104.8 (1.10, loop turn 16): places named in the page's language, from OpenStreetMap only

- **Why:**
  - Codex's QA: on the en and ar pages, places showed as a generic "School" or "مدرسة".
  - OSM's own practice for localized maps is `name:<lang>`, then `name:en`, then `name` ([OSM Wiki: Names](https://wiki.openstreetmap.org/wiki/Names)).
- **The rule (strict, never translated or transliterated):**
  - A place takes `name:en/ar/ru/fr` only from its own OSM element, or from a POI of a compatible kind.
  - The Hebrew name must be identical, and the match must be within 80 m and unique.
  - A name is never taken from a street, a parking lot, a square or neighbourhood, land use, or a building with no POI tags.
- **The result:** 30 places now carry their real name in other languages: en 30, ru 3, ar 3. 12 of them are within a 10-minute walk.
- **Dropped and ambiguous:** 20 matches were dropped as a different object (streets, bare buildings), and 9 ambiguous ones were skipped.
- **What is unchanged:** all other place fields are byte-identical. Where there is no sourced name, the kind is still shown ("School"), as before.

## v104.9 (1.10, loop turn 17): the fold headings are controls too (WCAG 2.2 SC 2.4.11)

- **Why:** WCAG 2.2 SC 2.4.11, "Focus Not Obscured": a focused control must not be hidden by author content, and floating buttons are the usual offenders ([TabNav, SC 2.4.11](https://tabnav.com/academy/wcag/success-criterion-2.4.11), [Vispero, WCAG 2.2](https://vispero.com/resources/new-success-criteria-in-wcag22/)). On the live 378 the accessibility button could sit on the dock card's last fold.
- **The design:**
  - Both floating buttons count the world's fold headings (`<summary>`) as controls: the site's WhatsApp bar (conversion-cta.php) and the accessibility corner (project-stage.php).
  - They lift into the nearest free place, exactly as they already do for the world's buttons and sliders.
  - `#nlps summary` is appended at the end of each list, so every existing rule is unchanged.
