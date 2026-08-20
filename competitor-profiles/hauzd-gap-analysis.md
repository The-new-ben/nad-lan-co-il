# Hauzd — FULL user-facing gap analysis (hands-on, 2026-08-20)

**Method:** real browser session on their LIVE showroom `palmanovacenter.hauzd.app` (Asunción,
Paraguay project) — entered (EN), accepted their entry gate, clicked: filters, List, a unit
(Dept 029), Floorplan, Views, Info. DOM read at every step. **Caveat:** their 3D renders in a
WebGL canvas; canvas VISUALS could not be screenshot-verified on this machine (in-app pane does
not composite) — canvas features are marked [canvas]. Everything else = clicked+read (eyes-DOM).
Owner order: "map everything they give that we don't — hands-on, click things."

## 1. What a buyer gets in a Hauzd showroom (verified click-by-click)

1. **Entrance**: language pick (EN/ES) + terms gate → straight into full-screen 3D. No page chrome, no scrolling — the experience IS the viewport.
2. **Persistent top nav**: Exterior · Amenities · Views · List · Location · Gallery · Info · Back.
3. **Filters**: Status + 1/2/3 BedR — instant; honest empty-state ("no units match filters") with one-tap "Remove filters".
4. **Tower selector** (Tower 1 / Tower 2).
5. **List = FULL sortable inventory table**: EVERY unit (Dept 001…250+) with bedrooms, bathrooms, m², orientation, tower, type. Sort arrows. This is the whole program, not 6 demo units.
6. **Unit page**: clickable breadcrumb inside the experience (Project \ Tower 1 \ Level 08 \ Dept 029), unit facts (3BR · 3.5 bath · 214m² · South · Type D), **Keyplan + Floorplan** buttons [canvas render], floor-level buttons (0-8) for level jumps, and a **"similar units" carousel** with 20+ alternative units (cross-sell engine).
7. **Views**: per-height/orientation panoramas [canvas].
8. **Amenities**: dedicated amenity walk [canvas].
9. **Location**: map scene [canvas]. **Gallery**: renders [canvas].
10. **Info**: full marketing story page inside the app (positioning, LEED, sustainability).
11. **WhatsApp** contact present in the app (wa reference in DOM).
12. Platform (marketing-verified, not in this demo): live price/status sync from CRM, online reservation+payment, favorites, developer analytics, iOS/Android + touchscreen apps.

## 2. THE GAP TABLE — what they give vs what we give (per user-facing feature)

| # | Hauzd gives | We give today | Closeable how |
|---|---|---|---|
| 1 | Full-viewport 3D, zero page-scroll, no frame-in-frame | 3D theater squeezed mid-page; side panel needs inner scroll (owner's "1000 times" complaint) | **ENGINE-UX NOW**: full-height theater mode + overlay panels — lane 1 composition |
| 2 | FULL inventory table (every unit, sortable, specs) | 5-6 authored demo units on flagships | **DATA NOW**: build full unit-type table per project from public program data (honest: מפרט תוכניתי, not מלאי) — no developer files needed |
| 3 | Filters (rooms/status) w/ honest empty-state | none | **ENGINE NOW** (unit data structure exists) |
| 4 | Keyplan + floorplan per unit | plan tab with one tiny SVG (Rainbow), plans OFF on most | **GENERATE** (GPT Image 2 plan series per type) + engine tab |
| 5 | Similar-units carousel (cross-sell) | none | **ENGINE NOW** (small JS, big sales value) |
| 6 | Breadcrumb Tower\Level\Unit navigation | hotspot pills only | **ENGINE** (medium) |
| 7 | Per-height view panoramas | window tab activates but paints nothing (CEO report) | FIX Mapbox paint (P0 in queue) or generated direction-true balcony views |
| 8 | Amenity walk scene | feature-bar links; no amenity visuals | **GENERATE** facility boards + amenity images (image factory) |
| 9 | Interior free-walk [canvas, real-time engine] | schematic CSS interior | P2 (real asset needed — CEO report law) — meanwhile: generated interior stills per unit type |
| 10 | Live price/status from CRM | prices only in article text; no per-unit status | Phase 2 with a signed developer; UNTIL THEN: price-range chips per unit type from public data, labeled |
| 11 | Reservation + payment in-experience | Woo checkout broken (lane 9) | **LANE 9 = prerequisite for money** |
| 12 | Favorites | none | engine, later |
| 13 | Developer analytics panel | health metrics internal | developer-facing report = product feature (later, sells the ₪3,990) |
| 14 | Multi-language | 2 langs | **WE WIN: 5 languages** |
| 15 | In-app story page | full SEO article ON the page | **WE WIN** |
| 16 | — Google visibility: canvas app, near-zero indexable text, invisible to search/AI | indexable content pages + 3D | **WE WIN BIG — THE STRATEGIC WEDGE** (proof below) |

## 3. The proof our wedge works (eyes, owner's Chrome, GSC 12-18.8)

/projects/duo-tel-aviv/ last 7 days: **10 clicks · 361 impressions · CTR 2.8% · avg position 11.4**.
Top queries: "duo תל אביב" (27), "דואו" (25), "duo tel aviv" (24), "פרויקט duo תל אביב מחירים".
The real WhatsApp lead (chose apartment → asked details) came through THIS funnel: brand search →
our indexable page → 3D → WhatsApp. A Hauzd showroom CANNOT do this — no indexable page. Their
model needs the developer to BUY traffic; ours generates it. This goes in every developer pitch.

## 4. The strategic project: DUO (decision + rationale)

- Only project with a PROVEN buyer lead through the full funnel.
- Brand demand exists and climbs (pos 15→11.4; 76+ brand impressions/week) — page-1 push = lead multiplication.
- Developer = Africa Israel (the owner's target developer for the first paid campaign).
- Assets in place: 1.06MB GLB, 5 authored hotspots, EN sibling, article. Missing: everything in the gap table.
- Rainbow is frozen (owner law) — DUO is the sanctioned flagship candidate.

**DUO build = the Hauzd-parity demo for every future developer meeting.**

### Materials manifest (generation run — GPT Image 2, Thinking mode)
Research first (public sources: developer site, permits, press): tower specs, unit-type mix,
amenity list, direction views. Then generate per the image-factory contract (SEO filenames,
alt_he, caption "הדמיה להמחשה" — never printed on image):
1. Hero dusk exterior (real twin-tower form) 2400×1350
2. Unit-type floor plans: one per type (2ch/3ch/4ch/5ch/penthouse) 1600×1200 PNG
3. Interior stills per type: living + bedroom + kitchen (consistent style batch)
4. Balcony views: N/S/E/W direction-true (park/sea/city per geo)
5. Amenity set: lobby, pool, gym, spa, lounge (only VERIFIED amenities)
6. Facility icon-board 1:1 with icon-safe framing
### Engine work (one change at a time, before/after to owner)
Full-height theater · full unit-type table + filters · similar-units strip · plans+price-range
surfaced next to the 3D (no inner scroll) · breadcrumb · window-view fix.

## 5. Generation model decision (owner asked)

**Use GPT Image 2 ("ChatGPT Images 2.0", live since 4/2026) with Thinking mode (Plus/Pro)** —
reasons before drawing, consistent style across up to 8 images per prompt (exactly our batch
pattern), high-res, reliable at plans/UI. The "Ultra" text-reasoning model is the wrong tool for
image runs (over-disclaims, acts unasked). Anti-refusal prompt frame (legitimate + specific):
"original illustrative architectural visualization for a real-estate information page; generic
modern Israeli residential tower; no logos, no brand names, no text on image, no recognizable
persons" — disclaimers live on OUR page as captions, not in the image.

## 6. Kept honest

Not verified: canvas visual quality/FPS of their engine (no screenshots on this machine), their
pricing, their live CRM sync in production. Their demo hid prices (developer choice). Entry
required accepting their terms gate (owner-ordered hands-on session).
