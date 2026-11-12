# Kikar showroom build notes (HAD-712, 11.11.2026 night): what the code must do, beyond the boards

Ben's order (through the Kikar session): finish the showroom in Hebrew, English and French with five additions. The boards (E1-E7, P1-P4, Q1-Q4)
are approved; these review notes from the Kikar session correct the boards and bind the build:

1. Call screen (P4/Q4): the self-view ("your camera") must never cover text. Put it in a corner of the video area or under the paragraph.
2. Map (P3/Q3): "הרבה פרטים על המפה" like the other projects: streets and their names, the park, the light-rail line and stations, schools
   and shops layers, plus the cone. Reuse the shared engine's map (assets/showroom-engine: mapbox-init.js, engine.js beam), not six dots.
   The cone is the area map's terracotta cone (#C2563A, engine.js:1327): Ben's "pink". The beam/engine internals are frozen (iron law 2):
   build around them, never inside.
3. Plan (P2/Q2): a clean drawing (four apartments, the core, the north arrow), labelled in the page's language; no English technical
   lettering from plan-floor30-towerC.webp. The four apartments are corner apartments: name them as the data/geometry says (the old stage
   uses NE, SE, SW, NW), the same on every screen.
4. View with details (P1/Q1): keep "נוף עם פירוט" / "View with details" (never "נוף עם השמות"), the 3D loads only on tap.
   Projection data: views carry tower, floor, bearing; the render camera is hfov 70°, pitch −4°, eye from views.json
   (docs/research/2026-11-10-kikar-showcase/views/views.json, "CAMERA view world (x,y,z) m; facing b deg").
5. Waymarks: one pulse at a time, the next step only, a short line saying what to do, stops on the tap, still marker with reduced motion.
6. Video: a tap opens a room at once; the advisor gets the join link; after about a minute, offer to leave a time. Reuse HAD-706's
   assets/designer/call.js; no third call screen. Map: docs/research/2026-11-11-kikar-journey/video-call-map.md.
7. Words: "NadLan advisor" / "נציג נדל״ן" / "conseiller NadLan"; never agent, broker, representative. English and French WhatsApp text:
   the English page's live sentence until Ben gives his own.
8. Scope: Hebrew, English, French only. Russian and Arabic untouched. The old stage's 3D window view is never removed from a language page.

## Video, the facts (video-call-map.md, 11.11.2026)
- Live together.php is AHEAD of the repo (LiveKit tokens via the Supabase proxy, options nadlan_tr_lk_proxy / _secret: names only).
  Read it live (scripts/project-stage/live_read.py) and hunk the live text; never write the repo copy over it.
- Two gates send the tap to the booking band #nlsch: PHP together.php:373 (no_rep unless nadlan_tr_rep_now is ticked) and the JS
  check of /room/available in showroom.js:225/256 and cockpit.js:247/313.
- Rate limit: 4 rooms per hour per IP (:374), no daily cap. Owner mail: project-stage.php:2851-2862 (admin email, join link).
- Signed-in owner opening the link gets "buyer" preselected (together.js:532); with LiveKit no "rep not here yet" state and no timeout
  (together.js:729-730).
- call.js (HAD-706) is not live and needs a mounted designer: do not use it here; extend the TogetherRoom's own screen.
- Minimal change: open the gate for Kikar only with a daily cap; /room/available?post=<id>; preselect "נציג" for a signed-in rep;
  a 60-second timer in enter() offering "לתאם מועד" (#nlsch), WhatsApp, or keep waiting.

## Two more steps from Ben (11.11.2026 night), before French
Order: 1 English showroom, 2 waymarks, 3 view with details, 4 map, 5 video (small part), 6 buying journey to the end, 7 video with the
designer session, 8 French.
6. Buying journey to the end, like Rainbow and DUO ("להיכנס, לעצב, לקבל הצעת מחיר, לרכוש, כמו בחנות"):
   - Reuse assets/showroom-engine/buyflow.js ("בנו לי הצעה": finish level, professionals, two contact fields, dispatch, what happens next)
     and inc/rfp.php (a real request document, unguessable link, 30 days, unit facts re-read on the server, real advisors, a status
     timeline that claims only what happened) + POST nadlan/v1/lead. Do not write a second flow.
   - From the Kikar basket: "בנו לי הצעה" / "Build me an offer" / "Construisez-moi une offre" -> an order summary (tower, floor, direction,
     the design, the team, the price lines with labels), send, a confirmation with the request number and the document link, the
     timeline; video call and WhatsApp beside it.
   - rfp.php needs a Kikar branch: example apartments by tower/floor/bearing, said honestly ("example apartment", sizes as published,
     price from the seller).
   - No payment. The last screen leaves room for a payment step; what, how much and who holds the money are Ben's decisions.
   - he/en/fr strings in the same table. Boards first (S and E rows), pictures in boards/, then code.
7. Video together with the designer session (HAD-701/706 owns the call: the feature matrix, Claude Design boards, one call module with a
   clean entry and a "shared object" contract). Kikar only wires the showroom and the TogetherRoom to that module and publishes its state
   (tower frame, floor, bearing, cockpit screen) on its data topics. No third call screen, no fork of call.js.
   Do now (step 5) only: a tap always opens the room (the two gates), the owner is notified, the leave-a-time offer after a minute,
   the self-view never covers text. Leave the controls (who leads, moving and showing things, sharing) to the shared module.
   After step 5, tell the Kikar session exactly what the Kikar room can do (for Ben's fairness declaration).
   Update (designer session, 11.11 night): do NOT wire call.js yet. It is changing now (real LiveKit, routes nadlan/v1/designer/call
   and /designer/call/token). Stable entry: joinCall(designer, {container, transport, room, identity, name, role, lang, onLeave,
   inviteBase}) and livekitTransport({url, token}). The Kikar wiring starts only after docs/design-lab/apartment-designer/CALL-CONTRACT.md
   exists. The project-page video buttons (together.php, project-stage, cockpit.js, showroom.js) stay ours.

## Progress (11.11.2026, about 22:00 UTC)
- Boards: E1-E7 approved; P1-P4 / Q1-Q4 (the additions) on the canvas; pictures in boards/.
- Step 1 English showroom: release 1.72.658 running (make_deploy658.py, kl_release.build_release). Words from world/showroom-i18n.js
  (he/en/fr), direction from lang; Hebrew identical (evidence/i18n-test-2026-11-11). PHP: nadlan_ps_kikar_next takes he+en; lang in the
  cockpit and journey settings; basket on for the English Kikar page with cfg.lang. 4 old check rows follow the rewritten lines.
- Ready, not wired: world/viewdetails.js (View with details, data hamedina/details.json from scripts/kikar/build_details_data.py) and
  world/planfloor.js (the four-apartment plan, names by true facing). Test pages _vd_test.html and _pf_test.html in
  assets/project-stage/ are scratch: delete before any commit.
- Map facts: the Kikar page's area map is #nlpjx-map (inc/project-experience.php:344, assets/arealife/areamap.js) and has NO beam; the
  cone exists in assets/project-stage/bridge.js (Ashira, listens to nl:facing at :349, showBeam) and the showroom engine. The showroom
  emits nl:facing {tower, floor, bearing, side, heightM} (showroom.js:157). Plan: a small listener that draws the cone on the Kikar
  area map from nl:facing, reusing bridge.js's drawing, and moves #nlpjx-map right under the showroom; never edit engine.js.
- Next after 658: one release wiring waymarks + view with details + the plan into showroom.js/cockpit.js; then the map; then video
  (live together.php hunk); then the buying journey (buyflow.js + rfp.php Kikar branch); then French.

## Step 0 (Ben, 12.11.2026, blocking): the apartment card must never trap the tower
Ben: "לוחצים על קומה, קופץ הכרטיס ... שמסתיר את המודל ... אי אפשר לעשות לו דיסמיס ... תעשה אותם מהבהבים כדי שאנשים ידעו שיש
אפשרות לקפל". Measured 390x844 tower B: the card covers 47% of the stage (en), 37% (he); no Esc, no swipe, no close.
The card becomes a sheet with two heights:
1. Opens at PEEK: one row at the bottom of the stage, <= 72 px (~15%): small picture, "Tower B · Floor 23 · west" on one line, − +,
   the primary button, a grab handle with a chevron. The whole tower stays tappable above it.
2. The chosen floor's band is never under the sheet: the tower picture shifts up when needed (peek and expanded).
3. Expand: tap the handle or the row, or swipe up. Expanded = today's card content, <= 45% of the stage, same height in he/en/fr
   (title on one line; short labels "Step inside", "Plans & prices").
4. Collapse by every one of: swipe down, tap the handle (real 44 px button, aria-expanded), tap the tower or the map, Escape.
   Swipe never the only way (WCAG 2.5.7). The drag does not scroll the page; the page scroll never sticks on it.
5. Collapse by intent, not a clock: touching or dragging the tower or the map drops an expanded sheet to peek. No timer (WCAG 2.2.1).
6. First appearance in a visit: the handle nudges once (down and back); grabber and chevron always visible. The continuous pulse stays
   on the next step only ("Step inside"). Reduced motion: no nudge.
7. "‹ All three towers" and the tower hotspots reachable in every state; another tower or floor works without closing anything.
8. Desktop: the card docks beside the tower on the reading-start side (right in he, left in en/fr), never over it.
9. All targets >= 44 px. Same component in he, en, fr.
10. Events: sheet_expand, sheet_collapse {how: swipe|handle|stage|esc}, floor_change_after_card, tower_change_after_card.
Acceptance (Kikar session runs it live): 390x844 he and en: sheet <= 0.15 of the stage after a floor tap; lowest and highest floors
tappable in peek; each of the four ways collapses; no sideways scroll; targets >= 44 px; chosen band visible in both states; desktop
1440x900 card beside the tower. Board: one screen in the S row and one in the E row (peek + expanded), picture in boards/, then code.
Release order now (updated): 1.72.659 designer (released);
1.72.660 = the designer session's designed call screen (assets only; swapped 11.11 ~23:00 UTC so nobody waits); 1.72.661 = mine: step 0 + the additions (make_deploy661.py, from deploy660.py);
1.72.662 = Kikar video (make_deploy662.py, built from deploy661.py).
