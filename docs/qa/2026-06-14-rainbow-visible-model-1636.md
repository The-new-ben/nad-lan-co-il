# QA: Rainbow Visible Model Hotfix 1.63.6

## Reason

Live 1.63.5 fixed the `type="module"` runtime blocker and installed the GLB/poster/unit data, but Chrome QA still showed a buyer-visible blank/dark showroom stage. The model-viewer custom element was active, yet the model did not read visually against the dark stage.

## Fix

- Rebuilt `assets/projects/rainbow-tel-aviv/model.glb` from the existing prototype asset with brighter showroom materials.
- Converted all 12 index accessors from 32-bit to 16-bit indices for safer Chrome/mobile WebGL compatibility.
- Added explicit model-viewer lighting/readability attributes: `environment-image="neutral"`, `exposure="1.45"`, `camera-target="0m 68m 0m"`, and `shadow-softness=".7"`.
- Bumped plugin/package/cache surfaces to `1.63.6`.

## Local Gate

| Check | Result |
| --- | --- |
| GLB magic/version/length | PASS, `glTF` v2 and declared length matches |
| GLB size | PASS, 944 KB -> 852 KB |
| Index accessors | PASS, all scalar index accessors now `5123` |
| Inline JS syntax | PASS, `node --check` |
| ZIP paths | PASS, rootless and no backslashes |
| ZIP version/header | PASS, `1.63.6` |

## Live Gate

After install, verify:

1. Healthcheck reports `version: 1.63.6`.
2. Rainbow page has `script#nadlan-model-viewer-js[type="module"]`.
3. `<model-viewer>` has `environment-image="neutral"` and `exposure="1.45"`.
4. The showroom stage shows a visible tower, not an empty dark frame.
5. No horizontal overflow at desktop/mobile widths.
