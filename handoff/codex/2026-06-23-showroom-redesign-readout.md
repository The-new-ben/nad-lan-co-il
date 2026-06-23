# NadLan Showroom Redesign Readout

Date: 2026-06-23

## What We Have

Lovable synced a useful strategy foundation, but not the visual/product package needed for implementation.

Available from Lovable:

- `handoff/lovable/2026-06-23-war-room-sync/reports/00-strategy-brief.md`
- `handoff/lovable/2026-06-23-war-room-sync/reports/01-showroom-redesign.md`
- `handoff/lovable/2026-06-23-war-room-sync/reports/report-3a-real-semrush.md`
- `repo-inventory.md`, `rest-api-map.md`, `advisor-notes.md`, and `plan.md`

Still missing from Lovable:

- visual mockups
- mobile screenshots
- coded prototype
- design tokens
- favicon/icon system
- owner-facing HTML/PDF export from Lovable
- reports `02` through `07`

## Current Showroom Reality

The current showroom is not contractor-ready.

Key facts from the repo:

- `assets/projects/rainbow-tel-aviv/` has the strongest technical base: real `model.glb`, poster, plans, `unit-map.json`, sourced environment data, and camera/hotspot values.
- `assets/projects/dimri-yama/` has stronger sales/story material, but its real GLB is not available. It uses a concept facade/fallback state.
- `assets/js/nadlan-project-showroom.js` is still a small brochure-level script: it swaps selected-unit text and placeholder panel copy, but does not render the full floor/unit/view/interior flow.
- `plugins/nadlan-config/inc/project-3d.php` is the more serious renderer and already contains partial support for model-viewer hotspots, real-facade-only logic, Mapbox token handling, comparisons, floor strips, tools, lead forms, and no-fake-facade states.
- Mapbox depends on `nadlan_mapbox_token` and feature flags. If token is absent, the UI must show a useful not-ready state, not a fake map.
- Old QA evidence already flagged fake facade grids and missing facade assets. The new design must not bring back fake stacked facade boards.

## Design Brief Locked

The next product slice is:

Build a mobile-first, investor-ready, contractor-sellable project showroom that feels materially better than Israeli real-estate listing pages.

This is the first sellable wedge, not the full limit of the business.

Owner correction locked:

- NadLan is not going after leftovers.
- The SEO and business architecture must cover the whole Israeli real-estate money market.
- High-competition topics are phased, not excluded.
- The master universe must include projects, listings, professionals, guides, city/neighborhood hubs, foreign buyers into Israel, and Israeli investors buying abroad.
- Outbound destinations to include now: Cyprus, Dubai/UAE, Greece, Thailand, plus additional justified markets.
- A stakeholder input packet is required so the business, asset, and technical decisions can be validated with the right person before deep implementation.

The core experience:

Pick project -> pick floor -> pick unit -> see exterior/view/map context -> inspect plan/interior/tour -> compare/save/share/WhatsApp -> submit a qualified lead.

The showroom must support three asset modes:

1. Full GLB + hotspots: Rainbow reference mode.
2. Concept/official facade + mapped units: Dimri fallback mode, clearly labeled.
3. Urban-renewal low-asset mode: facade/photo/floor-plan first, no fake 3D.

## Next Lovable Run

The prompt is saved at:

`handoff/codex/lovable-prompts/2026-06-23-showroom-visual-redesign-prompt.md`

Lovable must push outputs into:

`handoff/lovable/2026-06-23-showroom-visual-redesign/`

Codex will fetch `https://github.com/The-new-ben/nadlan-strategy-hub`, import that folder into the WordPress repo, and then start implementation against the visual spec.
