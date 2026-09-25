# HANDOFF 25.9.2026: Rainbow, "the floor answers" (live 1.72.278 + 1.72.279)

**For any agent picking this up.** Everything below was checked live (a real headless Chrome, desktop 1440 and phone
390, on https://nad-lan.co.il/projects/rainbow-tel-aviv/). The site loop (cron) is **stopped** on the owner's word
(usage running out); resume from "What is left" at the end of this file.

## Why

The owner tried floor 32 on the live Rainbow page (25.9.2026, midday) and said the product was not there. He wanted:
- a floor click that shows the direction with the beam, linking the building and the map;
- cards with information;
- a way to get inside the apartment, use the design studio and see the view;
- the map attached right under the 3D model.

He also said "people don't know it exists" and "watch the films". The two films show the product:
- the homepage film, `wp-content/uploads/2026/07/nadlan-promo-v2.mp4`;
- the developers' film on /developers/ and /film/.

The films' promise: tap a floor and it answers, see the view, walk in, design it, then contact.

**His rule for data (25.9):** the developer's marketing data goes on the page as published, with its source. That covers apartments left, estimated prices and the apartments per side: "you are not a judge". He is contacting the developer (ישראל קנדה) for that data.

## What was live before (1.72.277), diagnosed

- **The floor card:** a floor tap showed a small card with one button (WhatsApp).
- **The view and the map:** they sat 361 px under the stage, behind the facts. They waited for a second tap on the ring.
- **The way inside:** the "להיכנס לדירה · 360°" button sat at y=2284, for floor 25 only.
- **The designer** (/tour/designer/) was reachable only from the menus.

## What is live now

### Design first: Claude Design system v33

Published to https://claude.ai/artifact/L9Nqz7Viv7K3MYeZrBc9s8 (the artifact's version 36):
- **ProjectStage README and preview:** the floor answers, the card's four actions, the steps, the map attached.
- **HomePage README and preview, HomePagePhone preview:** the film band. It is designed only and **not built yet**.
- **bundle.css:** the `nlps-steps` / `nlps-step` rules, and the grid order: below the stage first, then the facts.

The local source is in the session scratchpad, `…/638c26e3-…/scratchpad/ds/project/`.

### Release 1.72.278

Made by scripts/project-stage/deploy278.py; result in docs/qa/project-stage-2026-09-24/deploy-result-278.json.

**The first run was rolled back by its own check.** The check still wanted the old hint text. The check was fixed and the second run went live.

| File (plugins/nadlan-config/…) | Added | Removed / changed |
|---|---|---|
| assets/project-stage/rainbow/stage.js | option `autoFacing` (a side id): the first tap on a floor also picks that side's example apartment, so the arrow, the view and the beam answer at once (`facing.auto`; `skipAuto` for `selectUnit`); option `actions` ([{id,label,kind}]): buttons in the floor card that emit `nl:floor-action` {action, floor, heightM, bearing, unit}; text `more` ("לצד אחר: הקישו על הטבעת", shown while the side was picked automatically) | nothing removed; the WhatsApp button (`nl:floor-cta`) stays last in the card |
| assets/project-stage/rainbow/stage.css | `.rbs-label-more`, `.rbs-label-acts`, `.rbs-act`, `.rbs-act--go` (sea), focus rings | the card 244 → 264 px; on narrow stages `min(380px, 100% - 24px)` (was `auto`) |
| assets/project-stage/bridge.js | `seaSide` (the `w` apartment first); `autoFacing`, `actions`, `text.more` passed to the stage; `openTourAt(floor, side, opener)`: the viewer takes the rendered floor nearest the pick (10, 25, 36) and its scenes only; `nl:floor-action` handler (inside → viewer, view → scroll to `.nlps-below` under the sticky header, design → /tour/designer/); the inside button says "להיכנס לדירה · מקומה 36" when the pictures are from another floor; the steps (`[data-nlps-step]`: floor / view / inside / design; `aria-current` moves to "view" on the first floor pick; "view" with nothing picked selects 25-w first); GA events `floor_action`, `stage_step` | the old inline `[data-nlps-tour]` handler became `openTourAt` (same behaviour: the picked side, else the sea; now also the picked floor) |
| inc/project-stage.php | the steps `<ol class="nlps-steps">` under the stage; the tour scenes for floors 25, 10 and 36 (each scene has `floor`); the tour section's title names the floors ("קומות 10, 25 ו־36, בארבעת הכיוונים") | the hint `<p id="nlps-hint">` ("בחרו קומה במגדל, ואחר כך דירה לדוגמה בטבעת הקומה.") on pages with example apartments (kept on pages without); grid order: the view and the map right after the stage on every width (desktop, 1100-1279, under 1100), before the facts |
| assets/nlds/nlds.css | the steps' rules (built with scripts/nlds/build_nlds_css.py from the DS v33 source; the build is byte-reproducible) | — |
| assets/project-stage/rainbow/tour/ (32 new files) | `living-` and `balcony-` × floors 10 and 36 × w/n/e/s, full size and `-2k`. Rendered with scripts/interior/render_floors.py (Blender 5.2, 3072 px, 40 samples; log in scripts/interior/render_floors.log) | — (the `-card.jpg` files for 10 and 36 are made but not deployed and not needed) |
| nadlan-config.php | version 1.72.278 | — |

### Release 1.72.279: the phone fix

Made by scripts/project-stage/deploy279.py.

**The bug, found in the live phone journey:** the tap that opens the floor card also pressed the button that appeared under the finger. The browser's click follows the touch, so a floor tap opened the designer.

**The fix:** stage.js now has `cardAt` / `fresh()`. The card's buttons, WhatsApp included, ignore clicks for 500 ms after the card opens.

The local nadlan-config.php was synced to the live text, and its md5 matches deploy-result-279.json.

## Checked live (evidence)

- **Desktop 1440, floor 32:**
  - selection `32-w`;
  - the card: "קומה 32 · דירה לדוגמה · בפרויקט דירות 2 עד 5 חדרים, לפי פרסומי השיווק · לכיוון הים · לצד אחר: הקישו על הטבעת · להיכנס לדירה · מקומה 36 · הנוף והמפה · לעצב את הדירה · לקבלת תוכניות ומחירים";
  - the view title "קומה 32 · לכיוון הים · דירה לדוגמה";
  - the beam drawn on the area map;
  - step 2 current;
  - "הנוף והמפה" scrolls to the view;
  - "להיכנס לדירה" opens the viewer at floor 36 toward the sea, labelled "דירה לדוגמה" and "הדמיית פנים להמחשה בלבד";
  - no page errors.

  Layout: the stage 204-864, the steps 874-938, the view and the map from 1076, the facts from 1837.
- **Phone 390:** the same results (on 1.72.279) and no page errors. Screens: session scratchpad `rbclick/LIVE_M_*.png`, `LIVE_D_*.png`; the journey script is `rbclick/v33.py <url> <tag> [--m]`.
- **Runner page checks and orders:** all OK. Rainbow's source order is unchanged; only the grid moved the view and the map up.
- **Public-source audit (tools/source_audit.py) before and after:** Rainbow is GREEN. It has one H1, the same title, and +20 KB, all explained: the scenes of three floors in the tour button's attribute, plus the steps.

## Not touched

- The homepage: 1.72.277's home is unchanged.
- The beam's engine (engine.js).
- Other project pages: they have no stage, and the steps render only where example apartments exist.
- The language pages.
- Anything of EcoCity.
- noindex, the sitemaps, and every URL.

## What is left (in order)

1. **Phone polish on Rainbow:**
   - the floating direction tag ("לכיוון הים", `.rbs-facing`) overlaps the card's buttons when the card docks: hide the tag while the card is on, on narrow stages;
   - the accessibility button (bottom corner) covers step 3's number: add bottom room or move the steps up;
   - on the phone the card covers the upper tower (fine, but check that the picked floor stays visible).
2. **The homepage film band (DS HomePage v33, designed):**
   - a new `nadlan_hp_band_film()` at the start of `nadlan_hp_body()` in inc/home-v3.php, with the film via `nadlan_hv2_video_embed()`, the steps, and buttons to /projects/rainbow-tel-aviv/#nlps-t and the Sde Dov tour;
   - the services' third card gets `nadlan_sdedov_tour_poster()` instead of the video;
   - re-measure the phone photo (the scratchpad's h1home/lcp_home.py): it must stay under 4 s.
3. **"The view answers questions"** (the film): labelled places with distances in the view, from quarter.json.
4. **The developer's marketing data, when the owner brings it:** apartments left, price lists, the plan per side. It goes onto the floor card as published, with its source.
5. **Findings for the owner:** /tour/designer/ ends in a demo checkout with a card form marked "(דמו)". It was left unchanged.
6. **The rest of the board:** docs/loop/SITE-LOOP.md (H1.3b; HAD-298, HAD-299, HAD-301; the fleet items).

## Tracking

- Linear HAD-221 (Rainbow): comments on 25.9.
- Notion: a row in "מרכז הבקרה של הפרויקטים".
- Memory: `nadlan-session-handoff` (the top section), `nadlan-marketing-data-as-published`.
