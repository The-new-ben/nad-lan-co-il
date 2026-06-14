# Rainbow showroom product slice v1.64.1

## Scope

This slice moves Rainbow from a working 3D demo toward a buyer apartment-selector product.

Implemented in code:

- Shorter, project-relevant intro above the model.
- Compact model stage height so the block does not dominate the whole page.
- Surroundings caption: `הדמיית סביבת שדה דב, להמחשה.`
- Unit JSON keeps `label` and `recommended`.
- Stage apartment markers become color-coded availability dots with 44px+ hit areas.
- Recommended units can pulse.
- Hover/focus marker tooltip shows rooms, sqm, floor/view and price estimate when present.
- Selected-unit card uses buyer actions: `פרטים מלאים`, `מבט מהדירה`, `דברו עם היזם`.
- View-from-apartment scrolls the stage into view and has a capture fallback for the return button.
- Healthcheck exposes `product_selector_v1641`, `status_colored_unit_picks`,
  `recommended_unit_pulse`, `stage_intro_above_model`, and `stage_return_capture_fix`.

## Owner-only inputs still needed

These are not blockers for the prototype, but they are required for the full commercial product:

1. Official BIM/GLB, approved elevation drawings or approved floor plans from the developer.
2. Real price sheet, inventory and availability.
3. Per-project contractor/developer WhatsApp and sales phone.
4. Durable media storage or CDN for GLB/poster/drawings if traffic grows.
5. Payment or reservation provider for any real reservation/payment journey.

Until these are supplied, the page must keep demo/estimate wording and avoid official-sales claims.

## Research basis

- Render Vision apartment selector: apartment selection must combine building navigation,
  availability, filters and buyer comparison, not only a static 3D view.
- Renderzen apartment selector: floor plans, pricing, availability and features belong in one
  selector surface.
- L-TOUCH: developer sales tools need availability states such as sold, reserved and available.
- model-viewer hotspot guidance: model hotspots should be real controls that trigger the same
  product state as the rest of the UI.
- Progressive disclosure: advanced tools should appear after intent, not all at once.

## QA gate to run in Chrome

Run against the live page after deploy:

1. 1440 desktop screenshot: intro above model, compact stage, visible unit markers.
2. 768 tablet screenshot: no horizontal overflow, selected card readable.
3. 390 mobile screenshot: flow is intro, model, selected unit, CTA.
4. Edge mobile UA screenshot: same as mobile Chrome.
5. Click at least one available marker and one reserved marker.
6. Confirm selected card updates title, status, view and price.
7. Confirm `מבט מהדירה` opens the big map stage and `חזרה למודל` closes it.
8. Confirm stage drag still rotates/spins the fallback/model.
9. Confirm lead form still sends selected unit, floor, rooms and estimate fields.
10. Confirm console has no page errors, one H1, no visible raw code, no horizontal overflow.

## Local package checks

- Inline JavaScript extracted from `inc/project-3d.php`: `node --check` passed.
- Manifest JSON parsed and points to `nadlan-config-1.64.1.zip`.
- ZIP rebuilt at `plugin-dist/nadlan-config-1.64.1.zip`.
- ZIP structure: root folder is `nadlan-config/`, no backslash paths, and `inc/project-3d.php`
  plus `inc/health.php` are present.
- PHP lint was not run locally because this Windows shell does not expose a `php` binary.

## Deployment reminder

After merge:

1. Pull/sync UPress server Git.
2. Update NadLan Config in WordPress to 1.64.1.
3. Clear UPress cache.
4. Hard refresh `/projects/rainbow-tel-aviv/`.
5. Verify `/wp-json/nadlan/v1/healthcheck` reports `version: 1.64.1` and
   `project_3d.product_selector_v1641: true`.
