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
- `node scripts/import-project-showroom-payload.mjs --post-id 4464 --payload assets/projects/rainbow-tel-aviv/showroom-payload.json --dry-run`
  validates the payload and refuses live write attempts when the healthcheck is below `1.65.2`
  or the payload route marker is missing.
- `node scripts/qa-project-showroom-live.mjs --site https://nad-lan.co.il --slug rainbow-tel-aviv --post-id 4464`
  checks the public page and reports the precise blockers before `--strict` is used in the
  post-deploy gate.
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
4. Authenticated POST can be run through:
   `node scripts/import-project-showroom-payload.mjs --site https://nad-lan.co.il --post-id 4464 --payload assets/projects/rainbow-tel-aviv/showroom-payload.json --apply`.
   The script must return `updated_n`, `after_units: 6` and `after_has_glb: true`.
5. Public Rainbow page still renders and uses the saved fields.
6. `node scripts/qa-project-showroom-live.mjs --strict` passes after the payload import and cache
   clear.

## Current Live Baseline Before 1.65.2 Install

On 2026-06-14, the live-readiness script ran against production and correctly reported:

- live version: `1.64.6`
- passed: 14
- failed: 3
- blockers: live plugin version below `1.65.2`, missing `showroom_payload_api_v1652`, and one-H1
  public-page gate not yet green on production.
