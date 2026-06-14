# Rainbow 1.64.0 clickable showroom layer

## Reason

Live Chrome QA after 1.63.9 found that the buyer could rotate the showroom stage, but apartment selection was still not green:

- `model-viewer` hotspot buttons existed in the DOM but projected outside the viewport on the live page.
- The SVG/facade hotspot layer was empty on the GLB path.
- Console unit cards stretched too tall in Chrome, making the selector feel jammed.

## Change

- Adds a stage-level `.nlp3d-stage-picks` layer over the visible tower.
- Each pick is a real `button`, 50-54px, tied to the same `selectUnit()` function and `data-unit` IDs as the rest of the journey.
- Stage picks update the existing details card, floor state, stage card, compare state, live view camera, and inquiry payload.
- Unit-card rows are prevented from stretching into giant controls.

## Gate

- Buyer can drag the tower and see the transform change.
- Buyer can click a visible apartment pick on the stage.
- Active unit changes after click.
- Stage card and console details reflect the selected unit.
- Inquiry path remains reachable after selection.
- No horizontal overflow, no visible code leak, one H1, and no fatal console errors.
