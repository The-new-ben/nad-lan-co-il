# Dimri Yama Theme Pattern Slice

This slice moves the Dimri Yama showroom from a local preview toward a reusable theme-owned project page pattern.

## What Was Added

- `patterns/project-showroom-dimri-yama.php`
  - WordPress block pattern for a project showroom.
  - Uses the Dimri Yama prototype poster, GLB, and facade assets.
  - Keeps the 3D model as context and the fixed facade as the apartment selector.
- `assets/css/nadlan-project-showroom.css`
  - Theme-owned layout and responsive styling.
  - Avoids adding more plugin CSS debt.
- `assets/js/nadlan-project-showroom.js`
  - Small unit-selector behavior.
  - Reads unit facts from `data-*` attributes in the markup.
  - Sends the selected apartment context to the existing `/nadlan/v1/lead` path when the buyer form is submitted.
- `functions.php`
  - Enqueues the showroom CSS, selector JS, and `model-viewer` only when the page content contains `data-nlps-showroom`.
  - Adds the required `type="module"` script tag for `model-viewer`.

## Architecture Decision

The theme owns presentation. The plugin should remain responsible for reusable data contracts, import/export, REST endpoints, and lead routing.

This avoids turning `nadlan-config` into the entire website again.

## How This Becomes A Real Project Page

1. Insert the `Dimri Yama project showroom` pattern into the Dimri Yama project page or use the same markup from an importer.
2. Replace prototype assets with approved assets:
   - official BIM/GLB or approved model export
   - approved facade/elevation
   - approved floor plans
   - approved interior tour URL
   - approved price and inventory data
3. Keep the `data-nlps-unit` attributes updated for each apartment:
   - title
   - status
   - rooms
   - sqm
   - floor
   - view
   - note
4. Keep the root `data-nlps-endpoint` on the showroom wrapper. By default it points to `rest_url( 'nadlan/v1/lead' )`.
5. Publish this as a real `nadlan_project` post when owner routing is needed. The JS derives the card ID from WordPress body classes when no explicit `data-nlps-card-id` exists.
6. The selected-unit buyer form sends these fields to the existing lead funnel:
   - card ID
   - unit ID
   - building
   - floor
   - rooms
   - sqm
   - availability
   - budget
   - timeline
   - advisor preference
   - non-binding purchase intent
7. Verify desktop, tablet, and mobile screenshots before publishing.

## Buyer And Contractor Flow

- Buyer selects a facade cell, sees the apartment card, checks plan/tour/view placeholders, then sends a callback or non-binding purchase check.
- Contractor updates project materials by replacing the same assets and unit data, without new code.
- The public page never says "lead", "funnel", "CRM", or internal process language. It says "פנייה", "דברו איתנו", and "בדיקת רכישה לא מחייבת".
- The current Dimri data is prototype-only until the owner supplies official BIM, inventory, availability, prices, contact details, and approved media.

## Known Limits

This is still a prototype because the official project materials are not yet available. It must not be presented as official inventory or official pricing until the owner or developer supplies approved data.
