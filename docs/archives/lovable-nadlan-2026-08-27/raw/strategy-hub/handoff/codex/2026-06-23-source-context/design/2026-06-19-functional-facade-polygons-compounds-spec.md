# Spec — Functional facade: real building, polygons not squares, compounds, click→views+info

> **Status:** implementation contract for Codex (slice after 1.67.6 camera/dismiss). Target **1.68.0** (feature, not patch).
> **Owner directives verbatim (2026-06-19):**
> - *"Make the facade much more functional. When you press on it, you can get views, you can get info — not just press like on a button, I want things."*
> - *"Make building look like building, and buildings have sometimes complexities and compounds. Don't do just a square."*
> - *"Research it, web search and give me proofs of searching it."*

## 0. Research — proof of search (cited)

I searched the live web; these are the patterns real estate developer tools actually ship:

1. **SVG polygons traced on a real building render — not squares.** The *Interactive Real Estate* plugin lets you "draw clickable SVG polygons directly on the image," each polygon connected to a specific unit. → [wordpress.org/plugins/interactive-real-estate](https://wordpress.org/plugins/interactive-real-estate/)
2. **Hierarchical navigation building → floor → unit.** "Buyers can click a building to select a floor, then click a floor to browse individual apartments… everything happens inline" (no reload). → [same](https://wordpress.org/plugins/interactive-real-estate/)
3. **Click reveals real info.** The modal shows "size, price, availability status, room count, and any custom fields you define," plus shareable unit links. → [same](https://wordpress.org/plugins/interactive-real-estate/)
4. **Status color-coding on the building map** — available / reserved / sold, "so buyers can see availability at a glance." → [same](https://wordpress.org/plugins/interactive-real-estate/)
5. **Compounds / multi-building.** "You can organize a project into multiple blocks, each with their own floors and units" (apartment complexes, cottage developments). → [same](https://wordpress.org/plugins/interactive-real-estate/)
6. **Views from the apartment + per-unit inspection.** Render Vision's apartment selector lets buyers inspect "the overall building and every apartment unit individually, with availability, living space in m² and other facts available with one click." → [render-vision.com/apartment-selector](https://render-vision.com/apartment-selector/)
7. **Interactive masterplan for compounds.** VisEngine: "break your project into easily digestible parts by creating separate maps for each floor or section of a building and link these maps for seamless navigation." → [visengine.com/what-is-an-interactive-master-plan-in-real-estate](https://visengine.com/what-is-an-interactive-master-plan-in-real-estate/) · [mapme.com — interactive site plans](https://mapme.com/blog/create-interactive-site-plans-for-real-estate-development-projects/)

**Conclusion the sources converge on:** the facade is a *navigable, data-driven, status-colored polygon map on a real building image*, with a click opening a rich panel (facts + views + interior), and a *compound/site-plan level* above it when there are multiple buildings. That's the target — not a grid of squares.

## 1. Where we are (honest)

The engine **already has the right primitive**: `renderFacade()` builds clickable SVG polygons from each unit's `points` field over a `.nlp3d-facade` image (`inc/project-3d.php`). What's missing:
- **Real polygon data.** Dimri/Rainbow units have placeholder/empty `points` → the fallback grid of rectangles renders instead (the "squares" the owner sees).
- **A real facade image.** Currently an SVG prototype, not a believable building render.
- **Compound level.** `building` field exists per unit but there's no building→floor→unit hierarchy UI when multiple buildings exist.
- **Rich click panel.** Click selects + shows facts, but doesn't surface the two branches the owner wants: **view from apartment** + **interior journey**.

## 2. Target architecture (4 layers)

```
LEVEL 0  Compound / site plan   →  shown only when units span ≥2 buildings
            click a building     →  drills into LEVEL 1
LEVEL 1  Building facade         →  SVG polygons traced on the building render,
            status-colored          one polygon per unit (or per floor band)
            click a unit polygon →  selects unit, opens LEVEL 2 panel
LEVEL 2  Unit panel (rich)       →  tabs:  [פרטים]  [נוף מהדירה]  [סיור פנימי]
            פרטים  = facts (floor, rooms, m², dir, price est, status)
            נוף    = view-from-apartment (Mapbox/360 keyed to orientation)
            סיור   = interior journey (interior_url / tour_url / plan)
LEVEL 3  3D context model        →  the model-viewer (camera-locked per 1.67.6),
                                     for orientation/sun/sea, NOT the picker
```

## 3. Data contract (CMS — extend, don't replace)

Per unit (already partly present):
| field | exists? | purpose |
|---|---|---|
| `points` | ✅ | SVG polygon tracing the apartment on the facade image |
| `building` | ✅ | which building/block in the compound |
| `floor` | ✅ | floor (for building→floor→unit) |
| `status` | ✅ | available/reserved/sold color |
| `interior_url` | ✅ | interior render |
| `tour_url` | ✅ | 360/Matterport |
| `plan` | ✅ | floor plan |
| `view_note` / `dir` | ✅ | view-from-apartment context |

Per project (new):
| field | type | purpose |
|---|---|---|
| `facade_images` | array of `{building, src, viewbox}` | one render per building in the compound |
| `site_plan_image` | url | the compound/masterplan image (LEVEL 0) |
| `site_plan_polygons` | array `{building, points}` | clickable building outlines on the site plan |

When `facade_images` has 1 entry and no `site_plan_image` → single-building mode (skip LEVEL 0). When ≥2 → compound mode.

## 4. Rendering rules (the "looks like a building, not a square")

- **Polygons follow the architecture.** Each unit polygon traced on the real render (irregular shapes, balconies, setbacks). The authoring tool = the dev shortcut below.
- **Floor slabs + vertical massing.** When no per-unit polygon exists, fall back to *floor bands* (horizontal strips) on the render, not isolated squares — a band reads as a real floor.
- **Status legend** stays (green/amber/grey).
- **Hover/focus** raises the polygon + shows a mini-tooltip (title · rooms · m² · price · status) — sourced from existing `unitPriceInfo`.
- **Compound:** LEVEL 0 site plan with building outlines; selecting a building swaps the facade image + filters units to that building.

## 5. Click → rich panel (the "I want things, not just a button")

On unit select, the stage card becomes a **3-tab panel** (reusing existing data):
- **פרטים (Facts):** floor, rooms, m², balcony, direction, view, price estimate (non-binding), status chips. *(exists — keep.)*
- **נוף מהדירה (View):** the Mapbox/live-view keyed to the unit's `dir`/orientation + computed camera altitude (the sun/view logic already exists in `renderToolPanel` 'view'/'sun'). Honest fallback text when no map layer.
- **סיור פנימי (Interior):** `interior_url` image, `tour_url` 360 embed, `plan` link — the interior-journey doc (`docs/design/2026-06-19-project-showroom-engine-interior-journey.md`) is the contract. Placeholder media for prototypes; official later.

Tabs use the existing `nlp3d-stage-tabs` pattern.

## 6. Dev shortcut — author polygons fast (no manual coordinate math)

Codex builds a tiny one-page tracer (committed under `scripts/facade-polygon-tracer.html`): load the facade image, click around each apartment, it emits the `points` string + `building`/`floor` to paste into the CMS. This is how the cited tools let non-engineers author polygons.

## 7. Acceptance gate (Codex provides; Claude re-runs)

| # | Check | Pass |
|---|---|---|
| 1 | Single-building project renders polygons from `points` (not the square grid) | screenshot shows traced shapes on a building render |
| 2 | Compound project (≥2 buildings) shows LEVEL 0 site plan; clicking a building drills in | screenshots of both levels |
| 3 | Click a unit → 3-tab panel with Facts / View / Interior | screenshot of each tab |
| 4 | Status colors correct; sold not selectable | screenshot |
| 5 | Mobile 390: facade legible, tabs usable, dismiss still works (1.67.6) | screenshots |
| 6 | Healthcheck flags `facade_polygons_v1680`, `compound_site_plan_v1680`, `unit_panel_tabs_v1680` | curl |
| 7 | Embedded selector + camera lock survive | markers present |
| 8 | php -l / JS check / ZIP guard | all pass |

Screenshots committed `docs/qa/screenshots/v1680-facade/` at 1440/768/390.

## 8. Honest boundaries

- **A real polygon facade needs a real building render + traced polygons.** For Rainbow/Dimri prototypes those are illustrative until the developer supplies official elevations. The *engine* will be correct; the *assets* are owner-input. Label prototypes as illustrative.
- **Mapbox must work first** for the "View" tab to be real — that's the separate runtime defect (console error needed). Until then "View" shows the computed sun/orientation text, which is honest.
- **Penthouse-on-top / floor ordering** is a data fix in the unit map (`floor` values), not this renderer — file alongside.

## 9. Sequence
1.67.6 (camera + dismiss, in flight) → **1.68.0 (this: polygons + compound + tabs)** → Mapbox fix → real assets per project.

