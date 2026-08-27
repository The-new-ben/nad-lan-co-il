# Skill: Compound 3D Map

Use this skill when adding or extending a district-level 3D map for `nadlan_compound` archives such as Sde Dov.

## Product Standard

A compound map is not a decorative map. It is a sales and due-diligence surface:

- district context first: coastline, roads, nearby neighborhoods, transit and project clusters
- project pins from real `nadlan_project` posts with `lat` and `lng`
- click-through to the project page, where unit selection, lead capture and offers already live
- generated or illustrative district visuals are allowed only when clearly marked as illustrative
- no copied stock photos, no copied developer imagery, no fake faces, no fake availability

## Implementation Pattern

1. Register a dark feature flag, default off.
2. Keep the token as an option name only. Never hardcode a Mapbox, MapTiler or Cesium token in the repo.
3. If token or data is missing, show a graceful RTL notice. Do not throw JavaScript errors.
4. Use a shortcode for controlled placement and auto-render on the compound taxonomy archive only when the feature flag is on.
5. Query pins from `nadlan_project` posts in the `nadlan_compound` term and require numeric `lat`/`lng`.
6. JSON-encode pin data with WordPress JSON helpers and `JSON_HEX_*` flags.
7. Lazy-init the map with `IntersectionObserver`.
8. Make markers keyboard reachable and popups usable in Hebrew/RTL.
9. Keep the map module separate from the listing/unit picker. The map moves users from district to project; the project picker moves users from project to unit lead.
10. Add healthcheck fields: enabled, token_present and pins_count.

## Stack Guidance

- Near-term: Mapbox GL JS for drone-like fly-over, 3D buildings and project pins.
- Tokenless fallback: friendly notice or an SVG/static district concept, not a broken map.
- Mid-term: MapLibre can reduce vendor dependence, but it needs a reliable vector style/building source.
- Long-term all-Israel digital twin: CesiumJS / 3D Tiles when real city-scale 3D assets exist.

## QA Checklist

- Feature flag off: no map markup, no Mapbox assets.
- Token missing: notice appears, no console error, no Mapbox assets.
- Token present: Mapbox assets load only on pages that render the shortcode/archive.
- Pins: no coordinates means no pin; invalid coordinates are skipped.
- Popup: project name, status, unit count and project-page CTA.
- Motion: initial fly-in and orbit, with pause on user interaction.
- Mobile: no horizontal overflow, map height usable at 390px.
- Accessibility: role/aria-label on the map container, focusable marker buttons, visible focus.

## Data Boundary

The compound map is infrastructure. Content agents or the owner must populate the actual project cards, coordinates, media and per-project facts. If the data is not sourced, show less. Never invent live prices, availability, permits or unit status.

## Seeding Pattern

When a flagship compound is dark-launched before all project content is imported, add a tiny idempotent seed instead of creating demo posts. The seed may ensure the real compound term exists and assign an already-existing, validated `nadlan_project` to it, but it must not create project posts, overwrite other taxonomy terms, or run when the feature flag is off.

For Sde Dov, the safe pattern is:

- gate on `nadlan_feature_compound_map === '1'`
- gate once with an integer seed option such as `nadlan_compound_seeded`
- ensure `{ slug: sde-dov, name: "רובע שדה דב" }` in `nadlan_compound`
- find Rainbow by existing title/meta markers such as `Rainbow`, `ריינבו` or `קשת`
- only fall back to a known post ID after checking the post exists and is `nadlan_project`
- assign with `wp_set_object_terms(..., true)` so existing terms stay untouched
- if the project is absent, do nothing and retry later rather than fabricating content

