# Project 3D Placement And Sales Journey Skill

Use this with `skills/project-3d-sales-experience.md` when improving a project-level apartment picker.

## Placement Rule

- The 3D apartment selector must appear immediately after the single-project identity/profile header.
- It must come before long project copy, source notes, FAQ, reviews, or footer-like sections.
- Never append the selector with `$content . renderer` on a flagship project page. Long SEO copy can push the product experience thousands of pixels down.

## Buyer Journey Rule

- Treat the selector as a buying journey, not as decoration.
- Minimum visible path: rotate or inspect the model, choose floor, choose unit, inspect facts, inspect drawing/view state, choose professional help, request progress.
- A purchase-like CTA is allowed only as a non-binding request until official inventory, price, payment terms, and legal flow exist.

## Lead Payload Rule

Every unit-level request should include:

- `card_id`
- `unit`
- `floor`
- `rooms`
- `sqm`
- `timeline`
- optional `advisor`
- `purchase_intent`
- `reservation_state`
- `view_bearing`
- `view_altitude_m`
- `source=project_3d`

This lets the owner see which apartment and which professional path created the lead.

## Countrywide Rule

For Sde Dov and later countrywide rollout, keep one renderer contract. Every compound or project can improve data quality over time:

- concept massing
- clickable facade
- traced floor/unit polygons
- Mapbox/Cesium view
- verified inventory
- BIM/glTF/3D Tiles

Do not block useful concept-level interaction while waiting for official BIM, but never publish invented price, availability, or legal commitment.

## Rainbow Product Direction - 2026-06-11

The saved decision record is `docs/2026-06-11-rainbow-3d-product-direction.md`.

Locked direction:

- v1.59.1 is a hotfix/demo upgrade: move the 3D selector high on the page, contain mobile/desktop layout, make tower plates clickable, enrich the unit drawer, capture timeline/advisor/purchase intent, and emit GA4/dataLayer events.
- v1.59.1 also makes the facade clickable when `project_3d_image`, `project_3d_viewbox`, and unit `points` exist. Demo mode may use the original `assets/concept/rainbow-facade-demo.svg` with clearly illustrative coordinates.
- If the offers feature is enabled, a purchase-check lead may create a private `nadlan_offer` in `non_binding_inquiry` status with `offer_amount=0`; this is a tracking record, not a financial offer or reservation.
- v1.59.1 CTA is `התחל בדיקת רכישה — לא מחייב`.
- Do not use `שריון לא מחייב 72 שעות` until a real reservation engine, developer/yazam processor, and legal disclaimer exist.
- v1.60.0 is the first real commerce phase: Purchase Screen, non-binding reservation state through offers, WhatsApp OTP, optional KYC seam, optional developer-side refundable hold, e-sign summary, buyer status, and professionals panel.
- For real high-floor Tel Aviv views, use a future CesiumJS + Google Photorealistic 3D Tiles module. Mapbox remains good for locator/overview maps, but Tel Aviv OSM height coverage is not enough for a credible apartment-view demo by itself.
- After v1.60.0, build Buying Copilot before Bidding Round because the buyer-side magic is more important for project-manager demos than the professional-auction revenue mechanic.
