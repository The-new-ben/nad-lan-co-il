# Rainbow apartment selection owner rerun - 2026-06-24

Owner asked for a serious manual QA pass on selecting apartments on the live Rainbow model and explicitly said not to fake a working result.

## Live target

- URL: `https://nad-lan.co.il/projects/rainbow-tel-aviv/`
- Live healthcheck version: `nadlan-config` 1.69.27
- Health marker verified: `model_surface_horizontal_bias_v16927: true`
- No code was changed in this rerun because the live release passed the selection checks below.

## Code path inspected

- Surface mesh pick: `plugins/nadlan-config/inc/project-3d.php`
- `selectUnitFromModelSurfacePoint()` calls `modelViewer.positionAndNormalFromPoint()`, then maps the real surface hit to the closest authored unit point from the unit map.
- `syncModelViewerCamera()` sets both `camera-orbit` and `camera-target`, then calls `jumpCameraToGoal()`.
- The current behavior is nearest authored-unit selection from the real model surface. It is not exact click-any-window BIM selection.

## Browser QA

### Strict model-surface pick

Path: `docs/qa/screenshots/showroom-surface-mesh-pick-live-user-rerun-2026-06-24/`

Result:

- Desktop 1440: pass.
- Mobile 390: pass.
- Raw model-viewer tap selected `unit-08-sw`.
- Mesh-pick log exists.
- Selected card opened.
- Camera orbit moved to `45deg 66deg 38m` on desktop and `45deg 66deg auto` on mobile.
- Camera target moved to `0m 31m 6m`.

Screenshots:

- `desktop-1440-after-surface-mesh-pick.png`
- `mobile-390-after-surface-mesh-pick.png`

### Visible apartment marker selection

Path: `docs/qa/screenshots/showroom-marker-hit-live-user-rerun-2026-06-24/`

Result:

- Desktop 1440: all 6 visible apartment targets passed.
- Mobile 390: all 6 visible apartment targets passed.
- Failed markers: none.

Units tested:

- `unit-08-sw`
- `unit-16-w`
- `unit-24-nw`
- `unit-31-se`
- `unit-38-penthouse`
- `unit-boutique-07`

Screenshots:

- `desktop-1440-after-marker-taps.png`
- `mobile-390-after-marker-taps.png`

### Mobile free-tap grid

Path: `docs/qa/screenshots/showroom-model-free-tap-grid-live-user-rerun-2026-06-24/`

Result:

- 9 mobile 390 model-area tap points tested.
- Dead model-surface points: none.
- Model-surface taps selected a unit and moved camera where the tap landed on model-viewer.
- Two points landed directly on visible markers, which is acceptable because the marker is the buyer-facing authored target.

## Public-language check

Live 390px showroom text scan:

- Forbidden internal terms found: none.
- Em dash found: no.
- Terms checked: Lovable, Codex, Claude, prompt, token, Tailwind, shadcn, money page, KD, CRM, pipeline, schema, Featured, Sponsored, Promoted, GLB, SVG.

Minor wording note for a later polish slice:

- Some buyer-visible text still says `מודל פעיל` and `סובב מודל`.
- This is not a selection blocker, but `תצוגה פעילה` and `סיבוב 360` would be cleaner buyer language.

## Honest limitation

This proves reliable selection for the six authored Rainbow unit targets and nearest authored-unit selection from real model-viewer surface hits.

It does not prove exact apartment picking for every visible window in the GLB. Exact click-any-window selection requires official apartment-level geometry, BIM or IFC mapping, or a GLB exported with per-unit pickable mesh IDs.
