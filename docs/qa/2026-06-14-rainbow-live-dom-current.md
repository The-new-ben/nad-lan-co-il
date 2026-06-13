# Rainbow Live DOM QA Current State

Command:

```powershell
node scripts\check-rainbow-live-dom.mjs --out docs\qa\screenshots-rainbow-live-dom-current
```

Live URL:

`https://nad-lan.co.il/projects/rainbow-tel-aviv/`

## Desktop 1440

Screenshot:

`docs/qa/screenshots-rainbow-live-dom-current/desktop-1440.png`

Pass:

- One H1.
- `.nlp3d` showroom present.
- No horizontal overflow.
- No raw code leak.
- No visible PHP/JS error text.
- Static featured image suppressed.
- Fallback tower visible.

Warnings:

- `<model-viewer>` is not visible yet because `project_model_glb` is not wired.
- Some visible floor plate targets are below the ideal 44px height, for example 41-43px.

## Mobile 390

Screenshot:

`docs/qa/screenshots-rainbow-live-dom-current/mobile-390.png`

Pass:

- One H1.
- `.nlp3d` showroom present.
- No horizontal overflow.
- No raw code leak.
- No visible PHP/JS error text.
- Static featured image suppressed.
- Fallback tower visible.

Warnings:

- `<model-viewer>` is not visible yet because `project_model_glb` is not wired.
- Several floor plate targets shrink below 44px on mobile. This should become a plugin/CSS follow-up
  before the showroom is considered accessibility-polished.

## Interpretation

The live 1.63.0 rail is structurally stable, but the full goal is not complete because:

1. The GLB is not yet wired into CMS, so the live page still uses the fallback model.
2. Some showroom controls are slightly below the 44px tap-target standard.

After PR #163 is merged and the CMS fields are populated, rerun:

```powershell
node scripts\check-rainbow-live-dom.mjs --expect-glb --out docs\qa\screenshots-rainbow-live-dom-after-glb
python scripts\check-rainbow-showroom-readiness.py --expect-live-glb
```
