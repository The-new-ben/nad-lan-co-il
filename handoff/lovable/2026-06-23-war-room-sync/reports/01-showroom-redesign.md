# 01 — Showroom redesign

The core deliverable. This is what contractors pay for and what foreign buyers come back to.

> Scope: the per-project page (`/project/<slug>/`). Three pilots: **Dimri Yama**, **Rainbow Tel Aviv**, **Urban-Renewal pilot** (TBD slug, תמא 38 / פינוי-בינוי).

---

## 1. Concept (one line)

> Pick a floor → pick a unit → step outside the window → step inside the apartment.
> One page. One thumb. Under 10 seconds. Phone-first.

Everything below serves that sentence.

---

## 2. Critique of what ships today

From live screenshots of `/project/dimri-yama/` and `/project/rainbow-tel-aviv/` + reading `assets/js/nadlan-project-showroom.js` and the per-project payloads:

| What works                                          | What's broken                                                                                                               |
|-----------------------------------------------------|------------------------------------------------------------------------------------------------------------------------------|
| Hero card is genuinely premium on desktop.          | On mobile the gold/dark glass card stacks awkwardly; primary CTA isn't visually dominant.                                    |
| Payload schema is rich — hotspots, orbits, drawings, environment, view-layer all already authored. | `nadlan-project-showroom.js` never reads `hotspot_position` / `camera_orbit` / `<model-viewer>` — the data exists, the JS doesn't drive it. |
| Lead payload from JS is excellent (unit + floor + dir + intent + market_note). | Lead has no price band, no calendar, no FX, no language toggle, no "save & share" — kills foreign-buyer intent. |
| Tabs (plan / tour / view / contact) are the right four. | Tabs only swap a paragraph of Hebrew placeholder copy. Nothing renders.                                                      |
| `Premier · פרופיל מאומת` badge on Rainbow is a strong trust primitive. | Not extended system-wide; Dimri Yama has no equivalent.                                                                       |
| Server has `/wp-json/nadlan/v1/project-showroom/<id>`. | Returns **401 unauth** in prod. Either intentional admin-gate or regression (see `advisor-notes.md`).                       |
| Offers placements coded in `inc/offers.php`.        | `GET /nadlan/v1/offers` returns **404 rest_no_route**. Sponsored slot on the showroom can't render.                          |

---

## 3. Proposed UX — four layers, mobile-first

All four layers live on one URL, no full-page reloads. Bottom-sheet pattern (Airbnb / Google Maps style).

### Layer 1 — Building

- Full-bleed `<model-viewer src="model.glb" reveal="interaction" poster="poster.webp">`.
- Auto-orbit on idle (subtle, ≤ 6°/s, pauses on touch).
- Right-rail icon pills (thumb-reachable on phone): **☀ סימולציית שמש**, **🌅 מבט מהדירה**, **🗺 מפת סביבה**, **🌐 שפה (HE/EN/FR/RU)**, **₪/$ FX**.
- Sticky bottom sheet, collapsed state: **"בחר דירה · 23 זמינות"** + a tiny availability bar.
- Header: project name, district chip, **verified badge** if `tier ≥ premium`.

### Layer 2 — Floor

- Tap the sheet → it expands to ~60vh.
- Left: vertical floor strip (1 → N). Each row shows availability dots by line: `N · S · E · W` colored green / amber / grey from `unit-map.json` `status`.
- Right: a small isometric facade hint of that floor, highlighting which lines exist.
- Selecting a floor smoothly orbits the model to that floor height using `camera_orbit` (compute from `project_3d_floor_height_m` + `project_3d_ground_elevation_m`, both already in `showroom-payload.json`).

### Layer 3 — Unit

- Tap a floor → grid of unit chips for that floor. Each chip:
  ```
  ┌─────────────────────────┐
  │ דירה 16W                │  rooms · sqm · dir
  │ 4 חד' · 112מ"ר · מערב  │
  │ 🟢 זמין                 │  status pill
  └─────────────────────────┘
  ```
- Tap a chip → camera orbits to that unit's `hotspot_position` + `camera_orbit` from `unit-map.json` (one of the missing wires). A pin appears on the facade.
- The chip-bar collapses to a horizontal scroller above the sheet so the user can flick between units while watching the model.

### Layer 4 — Inside the apartment

- Detail drawer (slides up over the model). 3 tabs:
  - **תכנית** — render the `plan` SVG from `unit-map.json` (Rainbow already authors these per type).
  - **סיור פנים** — Matterport / Cupix iframe from `tour_url`. Lazy-loaded on tab click only.
  - **מבט מהדירה** — panorama or rendered still from `interior_url` / `view_url`. Placeholder labeled "להמחשה — להחלפה בחומר רשמי" while we wait on contractor assets.
- Persistent CTA strip at the bottom of the drawer:
  - **`אני מעוניין`** (primary, gold) → opens lead modal pre-filled with unit context.
  - **`WhatsApp`** (secondary) → `wa.me/?text=…` with unit context, owner number from `owner-config-rest.php`.
  - **`שמירה`** (icon) → saves to local + posts to `/favorite` if logged in.
  - **`שיתוף`** (icon) → native share with deep-link `?unit=<id>`.

### Deep links

- `…/project/<slug>/?unit=<id>` opens that unit's drawer on load.
- `…/project/<slug>/?floor=<n>` opens floor view.
- `…/project/<slug>/?lang=en` flips to EN locale (when foreign-buyer engine ships, report 05).

---

## 4. Wiring spec — exactly what `nadlan-project-showroom.js` must do

Today the JS handles unit-button click → text swap. It needs three additions:

```js
// 1. Hotspot orbit
unitBtn.addEventListener('click', () => {
  const u = unitMap[unitBtn.dataset.unitId];
  modelViewer.cameraOrbit = u.camera_orbit;          // e.g. "24deg 61deg auto"
  modelViewer.cameraTarget = u.hotspot_position;     // e.g. "-6m 80m 5m"
  modelViewer.jumpCameraToGoal();
  renderUnitChip(u);
});

// 2. Floor → camera height
floorBtn.addEventListener('click', () => {
  const f = parseInt(floorBtn.dataset.floor, 10);
  const y = payload.meta.project_3d_ground_elevation_m
          + (f - 1) * payload.meta.project_3d_floor_height_m;
  modelViewer.cameraTarget = `0m ${y}m 0m`;
  modelViewer.jumpCameraToGoal();
});

// 3. Lazy tour iframe
tourTabBtn.addEventListener('click', () => {
  if (!tourFrame.src) tourFrame.src = activeUnit.tour_url;
});
```

That's the missing 30 lines. Until they land, the showroom is a brochure, not an experience.

---

## 5. Performance budget

| Metric                          | Target            | How                                                                         |
|---------------------------------|-------------------|-----------------------------------------------------------------------------|
| LCP (4G, mid-range Android)     | ≤ 2.5s            | Poster image as LCP element; `model-viewer reveal="interaction"`            |
| GLB transfer                    | ≤ 20MB, ideally ≤ 8MB | Draco + meshopt compression at export. Rainbow's current `model.glb` = 832KB (already good). Dimri Yama's `model-prototype.glb` = 8KB (placeholder, replace). |
| INP                             | ≤ 200ms           | No JS work on scroll; bottom-sheet animations via CSS transforms only.       |
| Matterport iframe               | Loaded on tab click | Never in initial doc.                                                       |
| Total JS shipped on showroom    | ≤ 60KB gzip       | Avoid React on this page; native DOM + `<model-viewer>`.                    |

---

## 6. What the contractor feeds us (sellable kit)

A single ZIP per project. Schema already exists under `assets/projects/<slug>/` — formalize it as a contract:

| File                            | Required | Notes                                                                |
|---------------------------------|----------|----------------------------------------------------------------------|
| `model.glb`                     | ✅       | Draco-compressed, ≤ 20MB, Y-up, meters, origin at ground center.     |
| `poster.webp`                   | ✅       | 1664×1040, hero render, sunset light preferred.                      |
| `unit-map.json`                 | ✅       | Schema in `assets/projects/rainbow-tel-aviv/unit-map.json` — canonical. Required fields: `id, floor, line, rooms, sqm, dir, view, status, hotspot_position, camera_orbit, plan, tour_url`. |
| `drawings.json`                 | ✅       | Floor plans per unit type as SVG/PDF URLs.                           |
| `environment.json`              | ✅       | District context + neighbor projects (sourced + dated).              |
| `view-layer-config.json`        | ⚪       | Sun/time/season presets. Optional for v1.                            |
| `material-intake-template.json` | ⚪       | Checklist of what's still missing — we send back to contractor.      |
| `interior/<unit-id>/*.jpg`      | ⚪       | Optional renders or 360 panos per unit.                              |

Until they deliver real assets, every prototype field MUST carry its `source_note` + `availability` disclaimer. **No fake prices, ever.** The current payloads already enforce this — keep it.

---

## 7. Pilot-specific notes

### Dimri Yama (`/project/dimri-yama/`)
- Hero already strong. Replace `model-prototype.glb` (8KB stub) with real GLB before contractor pitch — current 3D layer is non-functional even when the JS wiring lands.
- Rich `journeys-and-monetization.md` + `multilingual-seo-plan.md` already in `assets/projects/dimri-yama/` — fold into report 04 + 05.
- Add the `Premier · פרופיל מאומת` badge once the contractor signs Premium.

### Rainbow Tel Aviv (`/project/rainbow-tel-aviv/`)
- The reference implementation. Real GLB (832KB), real environment.json with sourced citations, real unit-map with 5 unit types.
- The four icon pills (3D / units / sun sim / view) shown in the hero are mocked into the image. Make them real, interactive, mobile-thumb-reachable.
- Use this as the foreign-buyer EN proof page (report 05).

### Urban-renewal pilot (slug TBD)
- Pick from existing CPT inventory in WP — a תמא 38 / פינוי-בינוי project, ideally one with existing tenants (different buyer persona: existing owners + investors).
- Stripped-down kit: no GLB required for v1 if budget tight — facade SVG + floor SVGs + unit table is enough. The 4-layer UX must degrade gracefully from "no GLB" to "facade image".
- Demonstrates: same template, lower asset bar, different funnel (existing-owner authentication via claim flow uses existing `/claim` endpoint).

---

## 8. Sponsored / monetization slots on the showroom

Placed once per page, never interrupting the 3D experience:

| Slot                             | Filled from                                          | Owner control |
|----------------------------------|------------------------------------------------------|---------------|
| Hero badge "מומלץ · Lighthouse"   | `tiers` + `featured-upsell`                          | Admin tier change |
| Right-rail "פרויקטים בסביבה"     | `environment.json → layers.neighbor_projects` + `offers` (when 404 fixed) | `placement-auction` |
| Drawer footer "מקצוענים מאומתים" | `/directory` filtered by city + profession           | Round-robin / paid |
| Below-fold "השוו פרויקטים"       | `/compare`                                           | Auto                |

These do not break the UX promise — they ride on layers that already exist in the payload.

---

## 9. What blocks shipping (engineering checklist for the WP team)

1. **Wire hotspots + camera orbit** in `nadlan-project-showroom.js` (30 lines, spec in §4).
2. **Fix `/wp-json/nadlan/v1/project-showroom/<id>` 401** — confirm intent, expose public read.
3. **Fix `/wp-json/nadlan/v1/offers` 404** — likely missing `require_once` in `nadlan-config.php`.
4. **Replace Dimri Yama prototype GLB** with real model (or use facade-prototype.svg fallback).
5. **Add the right-rail icon pills component** (sun / view / map / lang / FX) — reusable across pilots.
6. **Build the bottom-sheet** — pure CSS + native dialog, no React.
7. **Author the unit-chip component** (data attrs already present, just needs HTML/CSS).
8. **Lazy-load Matterport** — gated on tab click.
9. **Deep-link router** for `?unit=`, `?floor=`, `?lang=`.
10. **Reconcile `plugin-dist/` vs `plugins/nadlan-config/`** so the deployed JS is the one we edit.

Until 1–3 land, the redesign is cosmetic. Sequence those first.

---

## 10. Open decisions for you

- **Urban-renewal pilot slug** — pick a project from the existing WP catalog so report 04 has a 3rd worked monetization example.
- **Default language on `/project/<slug>/`** — HE always, EN via toggle, or geo-detect for foreign IPs? (My recommendation: HE default, EN toggle persistent across session, `?lang=en` deep-link wins.)
- **Matterport vs Cupix vs in-house panos** — provider lock-in affects what we ask contractors to deliver. Recommendation: accept any iframe URL, document the 3 supported providers in the contractor kit.
