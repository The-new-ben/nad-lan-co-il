# v1.60.2 Rainbow Flagship Page QA

Branch: `codex/rainbow-flagship-page-1602`

## Goal

Upgrade the Rainbow Tel Aviv project page from a buried 3D widget into a premium flagship
project experience that can be cloned for Sde Dov and future countrywide project pages.

## What Changed

- The project 3D module now has a final flagship CSS layer loaded after the older v1.59/v1.60
  layout rules.
- The live Mapbox view panel no longer stays hidden when token and coordinates are present.
  The map container removes `hidden`, forces `display:block`, and resizes after render.
- Non-fatal Mapbox style/source warnings no longer hide the map container.
- A compact premium capability band was added below the model:
  clickable facade, view from apartment, sun insight, and purchase-progress flow.
- A project-owner request form was added through the existing `/nadlan/v1/lead` route with
  `source=project_3d_showcase`. No new public route was added.
- A selected-unit dock was added, inspired by premium ecommerce product pages: current unit,
  status, 360 spin, and next-step action remain visible as the buyer explores.
- Scoped SEO title/meta description now apply to project pages that have 3D data.
- Healthcheck reports `premium_tower_picker_v5`, `mapbox_canvas_fix`, `flagship_showcase`,
  `owner_request_form`, and `selection_dock`.
- The clone standard was added to `skills/project-3d-sales-experience.md`.

## Source Research Used

- NAR virtual tour guide: virtual tours are valuable because they let buyers understand layout
  and spatial relationships, not just view static photos.
  https://www.nar.realtor/magazine/real-estate-news/technology/create-a-virtual-tour-real-estate
- ShowingTime virtual-tour guide: interactive floor plans add value by letting viewers navigate
  from plan areas into the visual experience.
  https://showingtime.com/resources/blog/what-are-the-differences-between-real-estate-virtual-tours
- Official Sde Dov district site: the district is planned around approximately 16,000 housing
  units with residential, commerce, employment, public buildings, parks, and transit.
  https://sdedov.co.il/about-sde-dov-district/
- Sde Dov FAQ: the district is divided into south, central, and north planning areas.
  https://sdedov.co.il/faq-en/
- Globes on Rainbow: the project includes a high-rise tower and lower buildings, and public
  reporting noted strong early sales as of May 2024.
  https://en.globes.co.il/en/article-eyal-waldman-buys-sde-dov-apartments-for-nis-50m-1001483936
- Official Rainbow/Israel Canada presence: positions the page around filtering needs and
  choosing an apartment, which supports an interactive selection experience.
  https://rainbow-telaviv.com/
- Israel Canada Rainbow page: confirms premium shoreline positioning and wellness facilities.
  https://www.israel-canada.co.il/en/projects/tel-aviv/rainbow
- BLK Architects Rainbow page: describes resort-style amenities, pools, spa, fitness and
  co-working areas.
  https://www.blk.co.il/rainbow
- Nike By You: guided product customization keeps the selected product as the center of the
  experience and uses a clear customization path, which maps to unit selection and advisor
  package selection for real estate.
  https://www.nike.com/nike-by-you
- Apple shop flows: purchase pages guide people through a sequence of choices rather than
  dropping them into a generic cart immediately, which supports a non-binding progression flow
  before any legal purchase rail exists.
  https://www.apple.com/shop/buy-iphone
- WebRotate 360: commercial product viewers use 360 inspection and hotspots to help buyers
  explore details; for project pages this maps to facade polygons, selected units, and 360 spin.
  https://www.webrotate360.com/products/webrotate-360-product-viewer.aspx
- Zakeke on 360 product viewers: 360 product views improve confidence by showing dimensions and
  detail. For Rainbow this supports keeping spin/inspection first and deferring fake checkout.
  https://www.zakeke.com/blog/benefits-of-360-product-viewer-for-ecommerce/

## Ecommerce Pattern Decision

The last design sweep looked at Amazon-style 360 product inspection, Nike-style customization,
Apple-style guided purchase, and commercial configurator/hotspot tools. The safe v1.60.2 pattern
is: selected-unit dock, 360 spin, compare, and advisor/package selection through the existing
inquiry flow. A real shopping cart for interior design, legal, mortgage, or other services should
wait for verified providers, prices, terms, invoices, cancellation language, and routing.

## Manual QA Checklist

1. Update the plugin to `1.60.2`.
2. Open `/wp-json/nadlan/v1/healthcheck` and confirm:
   - `version` is `1.60.2`
   - `project_3d.renderer` is `premium_tower_picker_v5`
   - `project_3d.mapbox_canvas_fix` is `true`
   - `project_3d.flagship_showcase` is `true`
   - `project_3d.owner_request_form` is `true`
3. Open `/projects/rainbow-tel-aviv/?cb=1602`.
4. Confirm the 3D module appears before the long article body.
5. Confirm the map panel is open when a Mapbox token and coordinates are configured.
6. Confirm the map is visible, draggable, and has controls.
7. Select another unit and confirm selected facts, camera text, compare tray, and lead payload
   update.
8. Submit the buyer form with test details and confirm a lead is created with unit fields.
9. Submit the project-owner request form and confirm the existing lead route receives
   `source=project_3d_showcase`.
10. At 390px viewport, confirm there is no horizontal overflow and all controls remain tappable.

## Boundaries

- This does not publish real prices or official availability. Demo/unverified data remains
  non-binding and price-by-inquiry.
- This does not add a new purchase endpoint, a new public route, or a separate inventory store.
- The future compound map must read the same `nadlan_project` card and the same unit JSON.
