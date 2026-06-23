# Rainbow 3D Product Direction

Date: 2026-06-11
Status: saved decision record for Rainbow / Sde Dov 3D upgrade

## What We Have Now

Live site is on NadLan Config 1.59.0. The current Rainbow 3D module is a reusable skeleton, not the finished vision.

What is already valuable:

- Project-level unit picker exists.
- Unit selection state and lead payload are wired into the existing lead funnel.
- The copy is mostly honest: prices and views are framed as illustrative or by inquiry.
- Mobile breakpoints and basic accessibility paths exist.
- The CMS contract can support better data later: floors, units, plans, facade image, viewbox, unit polygons, and source metadata.

What is still not enough:

- The 3D module is too low on the page because it is appended after long project content.
- The building itself is not yet the main interface.
- The current tower is generic massing, not a faithful Rainbow model.
- The current "view from apartment" is a placeholder, not a real camera view.
- There are no real drawings or verified per-unit plans yet.
- The purchase journey is still a lead request, not a real non-binding reservation flow.
- Professionals are not yet attached to the buyer journey.

## Direction Locked

The product should become a buy-like-a-store experience for new-build projects, starting with Rainbow and then Sde Dov.

The flagship flow:

1. Buyer lands on the project page and sees the 3D selector near the top.
2. Buyer rotates or inspects the building.
3. Buyer clicks a floor or apartment directly on the facade.
4. Buyer opens a premium unit drawer with facts, drawing, view, availability language, and next steps.
5. Buyer chooses a path: ask details, request a callback, attach an advisor, or start a non-binding purchase check.
6. The system routes the request to the project owner and optionally to professionals.
7. Later, the buyer gets a deal room with status, documents, advisors, and next steps.

## Immediate v1.59.1 Scope

v1.59.1 should stay a hotfix and demo upgrade, not the full commerce system.

Implement now:

- Move the 3D selector directly after the project identity/profile header.
- Contain the layout so it does not break the page or mobile width.
- Make tower plates clickable so the building becomes an interface, not decoration.
- Render a clickable facade layer when `project_3d_image`, `project_3d_viewbox`, and unit `points` exist.
- Use the original lightweight demo facade SVG only for demo mode when no developer image exists.
- Add a more complete unit drawer path: details, drawing placeholder, advisors, timeline.
- Add a buyer journey strip so the module feels like a purchase path.
- Send unit, floor, timeline, advisor, and purchase intent into the lead payload.
- Add dataLayer / GA4 events for floor select, unit select, orbit, angle, view, tool panel, and submit.
- Persist unit-level intent into the lead record, not only into the free-text message.
- When the offers feature is enabled, mirror the soft purchase check into `nadlan_offer` as `non_binding_inquiry` with amount 0.
- Keep the CTA as non-binding.

CTA for v1.59.1:

`התחל בדיקת רכישה — לא מחייב`

Do not use "שריון לא מחייב 72 שעות" until the reservation and hold system exists.

## v1.60.0 Product Scope

v1.60.0 should be a deliberate product release, not a hotfix.

Build next:

- Purchase Screen behind `nadlan_feature_purchase_screen`.
- Non-binding reservation request state using the existing offers engine.
- WhatsApp OTP gate.
- Optional KYC seam.
- Optional refundable hold only through the developer/yazam payment processor.
- E-signed non-binding reservation summary.
- Buyer status / deal room start.
- Professionals panel: lawyer, mortgage advisor, inspection engineer, interior designer.

The legal frame must stay explicit:

- NadLan does not collect seriousness money or advance fees as a broker.
- Any refundable hold belongs on the developer/yazam merchant processor.
- The reservation summary must clearly say it is not a binding memorandum.
- No final price, payment schedule, delivery date, or binding commitment should be invented.

Recommended future reservation copy:

`בקשת שריון ל-72 שעות — בכפוף לאישור היזם`

## View From Apartment Decision

Mapbox is good for the compound locator and overview map.

For a credible high-floor Tel Aviv view, use CesiumJS with Google Photorealistic 3D Tiles. Tel Aviv OpenStreetMap building-height coverage is not strong enough for a convincing high-floor skyline view by itself.

Implementation direction:

- New module: `inc/view-from-unit.php`.
- Feature flag: `nadlan_feature_view_from_unit`.
- Cesium + Google Photorealistic 3D Tiles for the real surrounding city mesh.
- Mapbox remains available for locator maps and fallback.
- Camera altitude formula:

```text
ground_elevation_m + base_offset + (floor - 1) * floor_height_m + eye_height_m
```

- Default floor height: 3.05m, configurable per project.
- Unit bearing comes from unit direction.
- Add a sun slider later with local sun math and no external API.

Key sources checked:

- Google 3D Tiles documentation: https://developers.google.com/maps/documentation/tile/3d-tiles
- Google pricing for Photorealistic 3D Tiles: https://developers.google.com/maps/billing-and-pricing/pricing
- Cesium Photorealistic 3D Tiles guide: https://cesium.com/learn/photorealistic-3d-tiles-learn/
- CesiumJS + Google 3D Tiles quickstart: https://cesium.com/learn/cesiumjs-learn/cesiumjs-photorealistic-3d-tiles/

## Hold Amount Decision

For Rainbow / Sde Dov luxury inventory, NIS 5,000 is a good pilot amount for a refundable authorization, but only after the v1.60.0 legal/payment architecture exists.

Make it configurable:

- Demo or no developer merchant connected: NIS 0.
- Standard projects: NIS 2,000 to NIS 5,000.
- Sde Dov luxury projects: NIS 5,000 default.
- Ultra luxury: project-specific amount.

## Sequence After v1.60.0

Build Buying Copilot before Bidding Round.

Reason:

- Buying Copilot creates the strongest buyer-facing wow for project managers.
- It makes the page feel like a living system, not a form.
- Bidding Round is a strong revenue engine, but it needs enough buyer flow and enough professionals to feel real.

Preferred sequence:

1. v1.59.1: placement, clickable plates, unit drawer, analytics, non-binding lead path.
2. v1.60.0: Purchase Screen, non-binding reservation flow, deal room start, professional attach.
3. v1.61.0: Cesium / Google Photorealistic 3D Tiles view-from-unit and sun slider.
4. v1.62.0: Buying Copilot.
5. v1.63.0: Bidding Round for professionals.
6. Countrywide: Sde Dov project seeding, project inventory import, reusable unit/facade data pipeline.

## Supplier / Project Manager Journey

The supplier value proposition must be visible in the product:

- More serious buyer leads.
- Unit-level intent, not generic contact forms.
- Analytics by floor, unit, view, and advisor request.
- A premium project showcase that can justify paid exposure.
- Optional purchase screen as SaaS add-on.
- Optional deal-room dashboard for project managers.

The manager should eventually see:

- Units viewed.
- Units selected.
- Hot buyers.
- Purchase-check starts.
- Advisor requests.
- Conversion from view to inquiry.
- Follow-up status.

## Implementation Rule

Do not fake final reality. It is acceptable to ship a beautiful concept model and illustrative drawings if they are clearly labeled. It is not acceptable to publish invented prices, legal commitments, official plans, or availability as facts.

The product should become more real in layers:

1. Concept massing.
2. Clickable facade.
3. Illustrative plans.
4. Verified developer inventory.
5. Cesium real surroundings.
6. Official drawings and BIM/glTF where available.
7. Purchase screen and deal room.
