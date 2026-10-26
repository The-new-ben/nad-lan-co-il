# /my-renewal/ today, and what it takes to ship the organizer room

Read-only audit, 26.10.2026. Sources: the live public page and the public demo endpoint (live version 1.72.529 per /wp-json/nadlan/v1/health), and the repo code. Screenshots of the live page: `live-audit/live-my-renewal-390.png` and `live-audit/live-my-renewal-1280.png`. The redesign: `preview.html` here (a copy of the design-system component `RenewalRoomPro`), screenshots in `shots/`.

## Where the code lives

- `plugins/nadlan-config/inc/urban-space.php`: the route, the private post type `nadlan_renewal`, the REST routes, the public landing and the member dashboard.
- `plugins/nadlan-config/assets/urban/renewal-space.js`: the room itself (renders the payload).
- `plugins/nadlan-config/inc/urban-wizard.php`: the free building check and its AI first analysis. `inc/urban-tools.php`: the ten stage labels and the consent calculator shortcode.
- Correction to the brief: `inc/renewals.php` is **not** this app. It is the billing renewal of paid advertising tiers (it creates a WooCommerce renewal invoice three days before a tier ends). The code comment names `urban-docs.php` for documents; **that file is not in the repo** and is not loaded.
- **The repo is behind the live site here.** The live landing says the files themselves are not stored in the room, and labels the example "חדר לדוגמה · נתוני דוגמה"; the repo copy still says documents are stored privately and says "הדגמה חיה". Any code change must start from the live file, never from the repo copy.

## What it does today

- **Anonymous visitors** get an indexable product landing in Hebrew and English (`?lang=en`) with canonical and hreflang: what the room is, three start steps, the live example room, before/after lists, six features, the consent calculator, FAQ (with FAQ schema) and a privacy note. "Free for residents and committees" is a promise on the page.
- **The example room** comes from the public route `/wp-json/nadlan/v1/renewal-demo` (checked live): "בניין לדוגמה: רחוב הדוגמה 1, גבעתיים", 4 floors × 3, 12 apartments all signed, stage 10 of 10, 12 updates.
- **A logged-in user** opens a room for one building (city, street, floors up to 40, apartments per floor up to 12; at most 5 rooms a day). Every apartment starts as "טרם הושג קשר".
- **In the room:** five consent statuses per apartment, four documents per apartment as checkboxes (ID, Tabu extract, signed agreement, power of attorney), the ten-stage ladder with typical durations and next actions, an updates feed, a stage history, an automatic consent note every 28 days, an invite link (anyone who opens it while logged in joins read-only, by email), a Mapbox city map, and a generic 3D building (`standard-residential.glb` through model-viewer) with one dot per apartment. Hebrew, English and Russian inside the room.
- **Email notices** to members exist but are off by default (deliverability first). The member dashboard sends `X-Robots-Tag: noindex, nofollow`; the room has no public URL.
- **Public demand evidence:** none. Search Console (26.7 to 24.10.2026, pages containing "renewal") shows one impression for /my-renewal/ in 90 days, and the public site shows no count of real rooms. So "people will want to manage their renewal through us" cannot be written as a fact; the pitch says what the room offers.

## Why it cannot be shown to an organizer as it is

1. **One room is one building.** No complex with several buildings, no portfolio view of all complexes; the dashboard only lists owned rooms as pills (up to 20). A pinui-binui complex is usually several buildings, and an organizer runs several complexes.
2. **One manager per room.** Only `owner_user_id` (or an admin) can edit; members are read-only. No organizer staff, no committee editor.
3. **Privacy finding (members see everything):** `nadlan_ur_space_payload()` returns the full apartment list, including every apartment's `contact_note` and `note`, to any logged-in member who joined by the link. For a committee room among neighbours this is tolerable; once an organizer keeps owner notes there ("ירושה", "ביקשו פגישה"), every neighbour can read every other apartment's notes. Must be fixed before any organizer uses it.
4. **Last save wins.** Saving one apartment posts the whole apartment array. Two staff members editing at once overwrite each other, and there is no per-apartment history of who changed what and when, which an organizer needs as signature evidence.
5. **Owners:** only a label and a contact note per apartment; no list of owners or heirs.
6. **No report** an organizer can hand a committee or a developer.
7. **Thresholds:** the task list mentions 66%, 67% and 80% rules; the live calculator words it more carefully (two thirds of the apartments in the cluster, one of three conditions). The room should use the calculator's wording, and a lawyer should check it.
8. **Design and words:** Frank Ruhl and Heebo, gold `#9C7A3C`, terracotta `#C2563A`, cream `#FAF7F1`/`#F3EEE3` (the banned palette), status colours in gold and terracotta, and the 3D building is a generic model, not their building. Visible words include "AI" and "מודל תלת-ממדי" (language-dna blacklist).
9. **Limits:** 400 apartments per room, 40 floors, 12 apartments per floor, 5 new rooms a day per user.

## What has to change in code to ship RenewalRoomPro (in order)

1. **Organizer account (M):** a private post type or user meta `nadlan_renewal_org` (name, logo, staff user ids, plan, `paid_until`); rooms get `org_id`, `complex_id` and `building_label`. `nadlan_ur_can_manage()` accepts org staff. Raise the daily room limit for org staff.
2. **Role-filtered payload (M, before anything else):** neighbours get the building totals, the stage, the updates and **their own apartment only**; they claim "I live in apartment X" when they join and the organizer approves it. Notes, contact notes and owner names go only to managers.
3. **One apartment per save (S):** `POST /renewal-space/{id}/apartment/{apt}` with a version number, plus an append-only change log per apartment (who, when, from, to).
4. **Owners per apartment (S):** `owners[]` (initials or name, share, heirs flag).
5. **Portfolio route (S):** `GET /renewal-org/{id}/portfolio` returning per complex: counts, stage, apartments missing a document, last update and the attention reasons the design shows.
6. **Report (S):** the report screen with print CSS (as in the design); a server PDF can come later.
7. **The UI (M):** render the four RenewalRoomPro screens from the payload. **Additive law:** the 3D building and the map are not removed; the facade elevation becomes the default view for organizer rooms and the 3D building stays one tap away.
8. **Tokens and words (S):** swap `nadlan_ur_space_css()` and the status colours in `nadlan_ur_consent_statuses()` to the Instruments tokens on the landing and in the room; remove "AI" and "מודל" from visible text.
9. **Billing (S):** a WooCommerce product "חדר ניהול לחברה מארגנת" priced per active complex per month, on the same pattern as the advertising tiers (payment sets `paid_until`, a daily check lapses it, renewal invoice three days before). A lapsed organizer room turns read-only; tenants' data is never deleted. Rooms stay free for residents and committees, as the landing promises.
10. **Legal (before the first organizer):** the organizer is the data controller and the site processes on its behalf, so a short data-processing agreement is needed under the amended Privacy Protection Law (unverified here, lawyer to confirm). Keep the live rule that ID copies and other files are not stored in the room.
11. **No URL, index or robots change:** the product stays at /my-renewal/; the dashboard keeps its existing noindex header.

S = a release or less, M = two or three releases. Nothing here was applied.
