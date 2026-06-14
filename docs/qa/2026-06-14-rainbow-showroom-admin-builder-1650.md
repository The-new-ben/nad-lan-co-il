# Rainbow Showroom Admin Builder v1.65.0 QA

## Scope

This slice improves the project editor experience for the Rainbow-style showroom.

The public showroom fields were already present, but the owner path still relied too much on raw
`project_3d_units` JSON. v1.65.0 adds a structured Hebrew metabox with grouped sections and a
simple unit-builder form that writes back to the same JSON field.

## What Changed

- Plugin version moves to `1.65.0`.
- `project-3d.php` renders a clearer `בחירת דירות אינטראקטיבית` metabox.
- The metabox now has sections for model/media, price/view data, apartment inventory, and project
  materials.
- Owners can add or update one apartment at a time through fields for id, title, floor, rooms, sqm,
  view, estimate, status, plan URL and model hotspot vectors.
- Raw `project_3d_units` JSON remains available for imports and debugging.
- Healthcheck reports `project_3d.admin_unit_builder_v1650`.

## Local Gates

- Inline frontend JS parse: required before package.
- ZIP must include `nadlan-config/` root and no backslash paths.
- Manifest must point to `nadlan-config-1.65.0.zip`.
- PHP lint was not run locally because this Windows shell has no PHP binary.

## Live Gate

After the owner updates NadLan Config in WordPress:

1. `/wp-json/nadlan/v1/healthcheck` must show `version: 1.65.0`.
2. `project_3d.admin_unit_builder_v1650` must be true.
3. In WordPress project edit for Rainbow, the metabox should show grouped Hebrew panels.
4. Adding a test unit through the builder should update the JSON textarea before saving.
5. Public page proof still requires the buyer page to render the selected apartment marker and card.

