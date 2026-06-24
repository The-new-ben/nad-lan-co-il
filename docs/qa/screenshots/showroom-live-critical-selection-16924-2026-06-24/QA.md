# Rainbow showroom apartment selection live pass

- Date: 2026-06-24
- Live URL: https://nad-lan.co.il/projects/rainbow-tel-aviv/
- Live plugin version: 1.69.24
- Viewports: desktop 1440px and mobile 390px
- Result: pass

## What was tested

The same critical browser tap grid used for the failing 1.69.23 rerun was run again after activating 1.69.24 in WordPress admin.

- 9 desktop tap points across the model.
- 9 mobile 390px tap points across the model.
- Visible authored apartment targets.
- Bare model-surface taps near authored targets.
- Selected unit id, selected card, camera orbit, and camera target.

## Result

- Desktop failures: 0.
- Mobile failures: 0.
- Raw model-surface failures: 0.
- Live healthcheck confirmed `1.69.24`.

## Visual notes

- The model remains visible after selection.
- The selected apartment card opens with buyer-facing text.
- Camera orbit and camera target match the selected authored unit.
- The tested mobile frame stays inside 390px.
- No Lovable, Codex, Claude, prompt, token, war-room, GLB-status, or other internal workflow language appeared in the tested buyer frame.

## Honesty note

This proves reliable selection for the authored apartment targets and nearby model taps. It does not prove true click-any-window picking inside the GLB. Exact window-level selection still requires apartment-level geometry, BIM or IFC mapping, or a GLB exported with per-unit pickable mesh ids.
