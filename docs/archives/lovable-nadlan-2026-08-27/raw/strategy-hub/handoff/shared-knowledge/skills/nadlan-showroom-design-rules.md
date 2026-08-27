# NadLan Showroom Design Rules

Status: active

Use this when designing or implementing the NadLan project showroom.

## Product Goal

The showroom must be contractor-sellable, investor-ready, mobile-first, multilingual-ready, and visibly above Israeli listing-site standards.

## Hierarchy

1. Project visual stage.
2. Floor/unit selection.
3. View/map context.
4. Plan/interior/tour.
5. Comparison/save/share.
6. WhatsApp/call/concierge lead.
7. Contractor asset intake if material is missing.

## Asset Truth

- Real GLB exists: model-first with hotspot/unit controls.
- Official/concept facade exists: facade-first and visibly labeled.
- No real visual asset: premium missing-state, not a fake facade.
- No Mapbox token/data: designed not-ready map state, not a fake map.
- No Matterport/Cupix/interior tour: tour-missing state and contractor asset request.

## Mobile Rules

- No horizontal overflow at 390px.
- No nested page-level scroll traps.
- Use a bottom sheet for selected-unit details.
- Keep primary contact actions reachable but not visually cheap.
- Text must fit buttons, tabs, chips, and cards.

## Interaction Rules

- Unit selection must drive the visible state.
- If `model-viewer` is used, unit selection should drive `camera-orbit`, `camera-target`, and hotspot focus where data exists.
- Facade selection should use real traced polygons or floor bands on real renders, not a square grid.
- Compare/save/share/WhatsApp states must be functional in prototypes.
- AI assistant is a guided concierge and lead qualification layer, not legal, tax, mortgage, or investment advice.

## SEO Rules

- Public copy must use commercial search language, not internal strategy language.
- Project pages link up to city, neighborhood, guide, and professional hubs.
- Unit/listing pages support project and hub pages. They should not cannibalize hubs unless they have unique content and a deliberate canonical strategy.

## WordPress Implementation Targets

- `plugins/nadlan-config/inc/project-3d.php`
- `assets/css/nadlan-project-showroom.css`
- `assets/js/nadlan-project-showroom.js`
- `assets/projects/rainbow-tel-aviv/`
- `assets/projects/dimri-yama/`

## Acceptance

- Prototype/screenshots for mobile/tablet/desktop.
- Explicit missing-asset states.
- Design tokens and component contracts.
- Owner-readable HTML.
- Codex implementation backlog with file targets and QA gates.

