# Dimri Yama geometry containment gate — v1.68.3

Date: 2026-06-20  
Branch: `codex/dimri-geometry-fix-1684`  
Target base: `codex/facade-engine-standard-1683`

## Why this exists

The live Dimri showroom previously failed the rectangle gate:

- the fixed facade plane overflowed the stage on 390px mobile and Edge-mobile;
- one showroom tap target measured below the 44px mobile target;
- the external floating action rail could overlap the selected-apartment card.

This release does not add a new facade concept. It adds a final geometry containment layer and a repeatable screenshot method for proving overflow/non-overlap.

## Implementation

- Added `nadlan_p3d_geometry_gate_v1683_css()` as the final project-showroom CSS layer after the 1.68.1 facade containment layer.
- Mobile dual-showroom facade plane is constrained inside the stage with `left:10px`, `right:10px`, `width:auto`, and `transform:none`.
- Showroom controls and unit cells keep a minimum 44px interaction target.
- External floating rails are hidden while a project showroom is active so they do not cover the selected-apartment card.
- Health flags added:
  - `geometry_gate_v1683`
  - `mobile_facade_containment_v1683`
  - `floating_rail_collision_guard_v1683`

## Screenshot proof

The geometry harness supports `--inject-css` so we can test an unreleased containment layer against the live DOM before deploy.

Command:

```powershell
node scripts/qa-showroom-geometry.mjs --slug dimri-yama-sde-dov --out docs/qa/screenshots/v1683-geometry-preview-dimri --strict --inject-css docs/qa/fixtures/showroom-geometry-1683-preview.css
```

Result: `passed: 4`, `failed: 0`.

Screenshots:

- `docs/qa/screenshots/v1683-geometry-preview-dimri/desktop-1440.png`
- `docs/qa/screenshots/v1683-geometry-preview-dimri/tablet-768.png`
- `docs/qa/screenshots/v1683-geometry-preview-dimri/mobile-390.png`
- `docs/qa/screenshots/v1683-geometry-preview-dimri/edge-mobile-390.png`
- `docs/qa/screenshots/v1683-geometry-preview-dimri/geometry-report.json`

Key measured facts from the report:

- all four viewports have `overflowX: 0`;
- mobile and Edge-mobile facade plane sits inside the stage;
- only one facade surface is visible;
- floating rail is not visible/overlapping while the showroom is active;
- minimum tap target is `44px`.

## Executable checks

```powershell
php -l plugins/nadlan-config/inc/project-3d.php
php -l plugins/nadlan-config/nadlan-config.php
php -l plugins/nadlan-config/inc/health.php
node --check scripts/qa-showroom-geometry.mjs
node -e "const fs=require('fs'); const s=fs.readFileSync('plugins/nadlan-config/inc/project-3d.php','utf8'); const m=s.match(/\$js = <<<'JS'\r?\n([\s\S]*?)\r?\nJS;/); if(!m) throw new Error('inline JS not found'); new Function(m[1]); console.log('inline JS ok', m[1].length);"
python scripts/build-plugin-zip.py 1.68.3
python scripts/verify-plugin-release.py 1.68.3
```

Results:

- PHP lint clean for all three PHP files.
- `scripts/qa-showroom-geometry.mjs` syntax clean.
- Inline project-showroom JS parses: `inline JS ok 69004`.
- ZIP clean: `entries=132`, `backslash=0`, `rooted=True`, `crc=ok`.
- Release verifier clean across plugin header, healthcheck, manifest, download URL, and ZIP.

## External reference basis

- Playwright screenshots: used for deterministic viewport capture.
- MDN `getBoundingClientRect()`: used for viewport/stage/facade rectangle checks.
- Lighthouse: kept in the standard toolchain for later performance/SEO gates.
- axe-core Playwright: kept in the standard toolchain for accessibility gates.
