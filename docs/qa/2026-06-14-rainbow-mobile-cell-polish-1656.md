# v1.65.6 Rainbow mobile apartment-cell polish

## Reason

v1.65.5 correctly moved the showroom away from abstract dots and toward apartment-shaped cells, but
live visual QA still showed two defects:

- mobile cells were 78px x 42px, below the 44px tap-target gate;
- selecting an apartment on mobile could collapse the model scene and place the selected card far
  outside the visible flow.

The owner also clarified the product direction again: buyers should choose apartments on the
building itself. Dots are not acceptable as the primary UI.

## Research basis

- DIGBY apartment selector: active perspective areas on a rendered property image.
- Render Vision 3D apartment viewer: click an apartment on the facade to open floor, area,
  orientation and availability.
- Zillow / Engrain interactive apartment maps: buyers need exact unit location and view.
- model-viewer hotspots: custom hotspot children can render the apartment-cell control.
- Parallel Select: facade and floor selectors should show availability status directly.

Full spec: `docs/2026-06-14-rainbow-apartment-cell-product-spec.md`.

## Changes

- Adds a late mobile CSS override to keep apartment cells at `86px x 48px`.
- Keeps selected-apartment actions at 44px+.
- Converts the selected-apartment card into a controlled mobile sheet so it stays in viewport and
  does not collapse the model scene.
- Adds health marker `project_3d.mobile_cell_polish_v1656`.
- Bumps NadLan Config to `1.65.6`, including manifest and cache-busters.

## Local proof

```powershell
git diff --check
node -e "extract inline project-3d JS and new Function(...)"
```

Result:

- `git diff --check`: clean except normal Windows CRLF warnings.
- inline project-3D JS parses: 60,735 bytes.
- ZIP: `plugin-dist/nadlan-config-1.65.6.zip`, 130 entries, root `nadlan-config/`, zero backslash
  paths.

## Remaining deployment gate

After merge/deploy, run:

```powershell
node scripts/qa-project-showroom-visual.mjs --site https://nad-lan.co.il --slug rainbow-tel-aviv --out docs/qa/screenshots/rainbow-showroom-visual-1656-live
```

Expected:

- mobile tap target no longer below 44px;
- no mobile/tablet showroom crop;
- selected card remains visible after clicking an apartment;
- healthcheck reports version `1.65.6` and `mobile_cell_polish_v1656`.

PHP lint was not run locally because this Windows shell has no `php` binary.

