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
