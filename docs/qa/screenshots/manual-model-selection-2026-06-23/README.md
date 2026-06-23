# Manual Rainbow Model Selection QA

Date: 2026-06-23

Scope: live Chrome check on `https://nad-lan.co.il/projects/rainbow-tel-aviv/` before the 1.69.2 fix.

Result before fix: failed. The page had six model hotspot buttons in the DOM, but the buyer click did not select an apartment. `activeUnit` stayed empty, the selected apartment card stayed hidden, and camera values did not change after the manual click attempt.

Root cause found in code: Rainbow has a real model but no official facade image, so the runtime did not create a separate buyer-visible apartment selector. It relied only on model-viewer hotspot projection, and the live projected hotspot centers were outside the visible clickable stage.

Fix in 1.69.2: create a model-aligned apartment selector for the real-model/no-facade state, using the existing unit data and the existing `selectUnit`, camera target, camera orbit, selected-card and lead-payload flow.

Key evidence:

- `04-desktop-before-manual-click.json`: hotspot centers were not clickable in the viewport.
- `05-desktop-after-manual-click.json`: manual click attempt left `activeUnit` empty and card hidden.
- `09-page-assets-list.json`: the model and model-viewer script were observed as page assets, so this is an interaction/layout problem, not a missing asset claim.
