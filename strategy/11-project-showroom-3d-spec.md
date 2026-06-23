# Project Showroom 3D Spec

Core rule:
No silent fallback. No fake facade. No dead buttons. No stacking. If there is no real asset, show a clear missing state. If there is a concept asset, label it concept. If there is official material, label it official. Do not invent apartments, prices, availability, or facades.

Buyer journey:
1. Arrive on project page.
2. See project name, location, developer, and non-binding availability/price rule.
3. Open the model/facade selector.
4. Select a unit/floor with large touch targets.
5. See unit card: floor, rooms, area, view, status, estimate/source note, and next actions.
6. Open map/view/tour only when real data exists.
7. Submit lead with project and unit context.

Required states:
- Official facade/elevation.
- Concept facade/elevation.
- Missing facade/elevation.
- GLB loaded.
- GLB missing/broken.
- Mapbox ready.
- Mapbox unavailable/error.
- Tour URL present.
- Tour missing.

Developer/admin fields:
- Project identity.
- Developer.
- Official site/source URL.
- Model URL and model type.
- Facade/elevation images.
- Facade polygon/unit mapping.
- Unit JSON: id, floor, rooms, sqm, direction, view, status, price estimate, source note.
- Drawing/floor plan URLs.
- Tour/video URLs.
- Surroundings/environment data.

Mobile rules:
- Model first, facade second, selected card below.
- No fixed card covering content.
- No horizontal overflow at 390px.
- 44px minimum tap target.

Dependencies:
- Official media and unit data. `REQUIRES_OFFICIAL_ASSET`
- Legal/product language around estimates. `LEGAL_REVIEW`
- Mapbox/token status. `NEEDS_VERIFICATION`

