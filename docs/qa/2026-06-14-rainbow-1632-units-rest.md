# Rainbow v1.63.2 Unit REST CMS Wiring QA

Scope: `plugins/nadlan-config/inc/project-3d.php`, plugin version metadata, manifest and ZIP.

## What Changed

- `project_3d_units` is now registered with `show_in_rest => true` for `nadlan_project`.
- Writes use the same `edit_post` authorization callback as the GLB/poster/drawings/material
  fields.
- Unit JSON is canonicalized at write time by `nadlan_p3d_sanitize_units_json()`.
- The public render path and the admin metabox now share `nadlan_p3d_clean_unit_items()`, so REST,
  admin save and frontend output read the same sanitized unit schema.
- Healthcheck now reports `project_3d.unit_meta_rest = true`.

## Why This Matters

PR #163 can provide a prototype GLB and a unit payload, but a fully repeatable CMS handoff needs the
unit inventory to be API-writable. Without this patch, deployment still requires a manual paste into
the Rainbow 3D metabox for `project_3d_units`.

This is still safe:

- no public write endpoint was added,
- no secrets are stored,
- REST writes require an authenticated editor for the project,
- invalid JSON is dropped instead of stored,
- URLs are sanitized,
- model hotspot vectors keep the existing numeric-vector gate.

## Local Proof

```powershell
node -e "const fs=require('fs'); const s=fs.readFileSync('plugins/nadlan-config/inc/project-3d.php','utf8'); const m=s.match(/\$js = <<<'JS'\r?\n([\s\S]*?)\r?\nJS;/); if(!m) throw new Error('inline JS not found'); new Function(m[1]); console.log('inline JS ok', m[1].length);"
```

Expected: inline JS parses.

```powershell
rg -n "1\.63\.2|project_3d_units|nadlan_p3d_sanitize_units_json|nadlan_p3d_clean_unit_items|unit_meta_rest" plugins/nadlan-config/nadlan-config.php plugins/nadlan-config/inc/project-3d.php plugin-dist/nadlan-config.json
```

Expected markers:

- plugin header and healthcheck `1.63.2`,
- `project_3d_units` in the REST meta registration map,
- sanitizer/helper functions,
- `unit_meta_rest`.

## Manual REST Gate For Claude / Deploy

After deploy, with a WordPress Application Password for an editor/admin:

```powershell
$base='https://nad-lan.co.il'
$auth=[Convert]::ToBase64String([Text.Encoding]::UTF8.GetBytes("$env:WP_USER`:$env:WP_APP_PASSWORD"))
$payload = @{
  meta = @{
    project_3d_units = '[{"id":"qa-rest-unit","title":"QA unit","floor":9,"rooms":4,"sqm":110,"status":"available","hotspot_position":"0 25 4","hotspot_normal":"0 0 1","camera_orbit":"40deg 65deg auto","plan":"javascript:bad"}]'
  }
} | ConvertTo-Json -Depth 8
Invoke-RestMethod -Method Post -Uri "$base/wp-json/wp/v2/nadlan_project/4464?context=edit" -Headers @{Authorization="Basic $auth"} -ContentType 'application/json; charset=utf-8' -Body $payload
```

Expected:

- request succeeds only for a user who can `edit_post` on project `4464`,
- saved meta contains `id`, title/floor/sqm/status/hotspot/camera fields,
- bad `plan` URL is sanitized away,
- healthcheck reports `project_3d.unit_meta_rest: true`.

Unauthenticated request must fail with 401/403.

## Packaging Gate

- `php -l plugins/nadlan-config/nadlan-config.php`
- `php -l plugins/nadlan-config/inc/project-3d.php`
- ZIP root must start with `nadlan-config/`.
- ZIP must have zero backslash paths.
- ZIP must contain markers:
  - `nadlan_p3d_sanitize_units_json`
  - `project_3d_units`
  - `unit_meta_rest`
  - `Version: 1.63.2`

## Sequencing

Recommended deployment order:

1. Merge/deploy v1.63.1 tap-target polish if not already live.
2. Merge/deploy v1.63.2 unit REST wiring.
3. Merge PR #163 asset payload.
4. Pull/sync UPress Git.
5. Run the Rainbow CMS apply helper with `--apply`; after this patch, the helper can be updated to
   include `project_3d_units` once it detects `unit_meta_rest=true`.
6. Clear cache and verify `/wp-json/nadlan/v1/healthcheck`:
   - `version: 1.63.2` or newer,
   - `project_3d.unit_meta_rest: true`,
   - `project_3d.projects_with_glb >= 1` after the GLB meta write.

## Local Blocker

This Windows shell still has no `php` binary, so PHP lint must run in Claude/deploy gate.
