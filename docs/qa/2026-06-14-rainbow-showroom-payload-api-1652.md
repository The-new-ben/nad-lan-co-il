# Rainbow Showroom Payload API v1.65.2 QA

## Scope

v1.65.2 adds a secure one-payload route for the future project factory:

- `GET /wp-json/nadlan/v1/project-showroom/<project_id>`
- `POST /wp-json/nadlan/v1/project-showroom/<project_id>`

The route exports/imports the same showroom fields that are visible in the WordPress metabox and
registered as REST meta.

## Security Contract

- Requires the target post to be a `nadlan_project`.
- Requires the current user to have `edit_post` for that project.
- No public or anonymous writes.
- Reuses the same sanitizers as the metabox/meta contract.
- Accepts either flat field names or `{ "meta": { ... } }`.

## Local Gate

- Frontend inline JS parses.
- Admin metabox script parses.
- `node scripts/build-project-showroom-payload.mjs rainbow-tel-aviv --write` creates
  `assets/projects/rainbow-tel-aviv/showroom-payload.json`.
- The payload contains 17 allowed `meta` fields, 6 unit records, 6 drawing records, GLB URL,
  poster URL, surroundings JSON and no unknown showroom fields.
- ZIP root is `nadlan-config/`.
- ZIP has zero backslash paths.
- Package contains:
  - `showroom_payload_api_v1652`
  - `nadlan_p3d_export_showroom_payload`
  - `nadlan_p3d_apply_showroom_payload`
  - `/project-showroom/(?P<id>\d+)`

PHP lint was not run locally because this shell has no PHP binary.

## Live Gate

After the plugin update:

1. Healthcheck reports `version: 1.65.2`.
2. `project_3d.showroom_payload_api_v1652` is true.
3. Authenticated GET for Rainbow returns meta and `units_count`.
4. Authenticated POST with a harmless test field updates that field and returns `updated_n`.
5. Public Rainbow page still renders and uses the saved fields.
