# Rainbow showroom product QA - v1.64.6

## Scope

v1.64.6 is a surgical follow-up to v1.64.5.

v1.64.5 removed `.nlp3d-hotspot-hit` from the drag exclusion list, but live mobile tracing proved the actual event target was inside `.nlp3d-stage-pick`, which is a `<button>`. The generic `button` exclusion still blocked the buyer's natural drag path.

## Fix

- If the event starts inside `.nlp3d-stage-pick`, `.nlp3d-hotspot`, or `.nlp3d-hotspot-hit`, it is allowed into the model drag path.
- Ordinary buttons, links, inputs, selected-apartment cards, Mapbox viewframes, and model-viewer hotspot buttons remain protected from drag.
- Healthcheck flag: `project_3d.stage_pick_drag_v1646`.

## Gate

- Mobile drag that starts on a visible apartment marker must change the showroom angle.
- A tap on the same marker must still select the apartment.
- No horizontal overflow, one H1, zero console errors.
