# Rainbow Showroom REST Field Contract v1.65.1 QA

## Scope

v1.65.1 hardens the owner/admin work from v1.65.0.

The metabox callback now points directly at `nadlan_p3d_render_admin_metabox()` instead of carrying
the old raw-field callback after an unreachable `return`.

The REST meta contract now includes the fields that the metabox exposes:

- `project_3d_image`
- `project_3d_viewbox`
- `project_3d_floor_height_m`
- `project_3d_ground_elevation_m`
- `project_3d_avg_price_per_sqm`
- `project_3d_price_source_note`
- `project_3d_model_type`
- `project_model_glb`
- `project_model_usdz`
- `project_model_poster`
- `project_3d_video_url`
- `project_3d_tour_url`
- `project_3d_cesium_tiles_url`
- `project_3d_drawings_json`
- `project_3d_environment_json`
- `project_3d_units`
- `project_3d_demo`

## Local Gate

- Frontend inline JS must parse.
- Admin metabox script block must parse.
- ZIP must be rooted at `nadlan-config/` with no backslash paths.
- Package must contain `admin_callback_clean_v1651` and `rest_showroom_fields_v1651`.
- PHP lint was not run locally because this shell has no PHP binary.

## Live Gate

After WordPress installs v1.65.1:

1. Healthcheck reports `version: 1.65.1`.
2. `project_3d.admin_callback_clean_v1651` is true.
3. `project_3d.rest_showroom_fields_v1651` is true.
4. Authenticated REST writes can set the same showroom fields that are visible in the metabox.

