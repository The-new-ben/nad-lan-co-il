# Ashira Showroom V2 Factory Bridge QA

Date: 2026-06-26
Branch: `codex/ashira-showroom-v2-clean`

## Scope

This slice makes the clean Ashira v2 preview usable by the project factory scripts. It does not
publish a page, does not deploy a plugin ZIP, and does not import anything into the live site.

## What Changed

- `scripts/build-project-showroom-draft.mjs` now accepts either `data-nlps-showroom` or
  `data-nlv2-showroom` as a supported showroom root marker.
- `scripts/apply-wp-draft-payload.mjs` now dry-runs v2 draft payloads without rejecting the clean
  `data-nlv2-showroom` marker.
- `scripts/build-project-showroom-draft.mjs` accepts project-specific Yoast title, meta
  description and focus keyword arguments instead of hardcoding Dimri copy.
- `assets/projects/ashira-sde-dov/showroom-payload.json` now validates against the current
  WordPress import schema while preserving Ashira v2 model, facade, environment and unit data.
- `docs/wp-drafts/ashira-sde-dov-v2-draft.json` was generated as a draft-only REST payload.

## ZIP Intake Boundary

`C:\Users\pro\Downloads\NadLan Ashira Factory Run.zip` was inspected. It helps as visual reference,
especially for the premium hero, apartment detail panel and floor-plan tab pattern, but it is not
Ashira production source material. It contains Rainbow-specific assets and a generated `dc` runtime,
so the implementation must not import its inline HTML or `support.js`.

## Verification

```powershell
node scripts\validate-project-showroom-payload.mjs --payload assets\projects\ashira-sde-dov\showroom-payload.json
node scripts\build-project-showroom-draft.mjs --pattern patterns\project-showroom-ashira-v2.php --slug ashira-sde-dov --title "Ashira Sde Dov" --yoast-title "Ashira Sde Dov - בחירת דירה ומודל תלת ממד" --yoast-description "Ashira Sde Dov בשדה דב: בחירת דירה על חזית הפרויקט, מודל תלת ממד, נתוני דירה ואומדן לא מחייב עד אימות מול היזם." --focus-keyword "Ashira Sde Dov" --out docs\wp-drafts\ashira-sde-dov-v2-draft.json
node scripts\apply-wp-draft-payload.mjs --payload docs\wp-drafts\ashira-sde-dov-v2-draft.json --dry-run
node --check scripts\build-project-showroom-draft.mjs
node --check scripts\apply-wp-draft-payload.mjs
node --check scripts\validate-project-showroom-payload.mjs
```

## Result

All checks passed locally. The live site was not changed.

## Honest Limits

- The draft payload is still draft-only until official Ashira material and owner approval exist.
- The `showroom-payload.json` uses the current import schema version (`v1`) because the live
  plugin-side payload schema has not yet been changed for v2-only naming.
- The v2 page root is clean (`data-nlv2-showroom`), but the data rail remains compatible with the
  existing WordPress import path so the factory can move forward safely.
