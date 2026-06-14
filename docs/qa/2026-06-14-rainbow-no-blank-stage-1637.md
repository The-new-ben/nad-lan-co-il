# QA: Rainbow No-Blank-Stage Guard 1.63.7

## Reason

Live 1.63.6 installed, but Chrome still showed the showroom as a dark frame with the model-viewer interaction prompt. The module script, GLB attributes, canvas, and healthcheck were present, but the buyer-visible result was still not acceptable.

## Fix

- Keep the procedural architectural tower/facade visible above the model-viewer rail as a no-blank fallback.
- Remove `.nlp3d-model-viewer` from the stage drag bail-list so drag gestures can rotate the visible tower even when model-viewer covers the stage.
- Keep `.nlp3d-mv-hotspot` in the bail-list so apartment hotspot selection remains protected.
- Bump package/cache surfaces to `1.63.7`.

## Gate

| Check | Result |
| --- | --- |
| Inline JS syntax | PASS, `node --check` |
| ZIP rootless | PASS |
| Header/version/cache-busters | PASS, `1.63.7` |

Live pass must show a visible building in Chrome. If the GLB canvas is still dark, the fallback tower must be visible and draggable.
