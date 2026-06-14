# Rainbow apartment-cell product spec

Date: 2026-06-14
Scope: Rainbow Tel Aviv showroom, then every future project showroom.

## What I understand

The buyer should not click abstract dots. A dot does not say floor, apartment, window bay, direction
or availability. The buyer should click apartment-shaped cells on the building itself. The cell must
feel like a unit in the facade: rectangular, aligned to the model, color-coded by availability, and
large enough to tap on mobile.

The buyer journey is:

1. See the project and immediately understand that apartments are selectable.
2. Rotate the building like a product in an online store.
3. Tap a visible apartment cell on the building, not a detached list.
4. See floor, rooms, sqm, view/direction, status and non-binding price estimate.
5. Open the apartment view, plan/tour when available, and contact the developer with the selected
   unit attached.

The contractor/developer journey is:

1. Upload or connect model, facade, poster, drawings, surroundings, video and unit inventory.
2. Edit status, estimate, view and recommended flag in the CMS.
3. Receive inquiries with unit context.
4. Later replace prototype assets with official BIM, official plans and real inventory without new
   plugin code.

## Research lessons

- DIGBY apartment selector: buyers browse apartments on a 3D rendered property image, with active
  areas marked in perspective and per-apartment floor plans, images and sales data.
  Source: https://digby.hu/apartment-selector
- Render Vision 3D apartment viewer: the facade itself is the selector; a click opens floor, area,
  orientation and availability. This is the exact interaction standard Rainbow should follow.
  Source: https://render-vision.com/services/3d-apartment-viewer-services/
- Zillow / Engrain interactive maps: buyers care about the exact location of the available unit and
  the view. Unit location is a product feature, not decoration.
  Source: https://www.prnewswire.com/news-releases/room-with-a-view-renters-can-now-use-interactive-property-maps-to-choose-their-apartment-on-zillow-301772138.html
- Zillow 3D Home floor plans: the strongest experience connects visual tour and floor plan so users
  understand where they are. Rainbow should connect building cell, plan, view and inquiry.
  Source: https://www.zillow.com/3d-home/floor-plans/
- model-viewer hotspots: the correct web rail for GLB hotspots is slotted children with
  `data-position` and `data-normal`; the visible child can be a custom apartment-cell control.
  Source: https://modelviewer.dev/examples/annotations
- Parallel Select: tower projects need facade and floor selectors with availability colors. The
  accepted real-estate pattern is available/reserved/sold directly on the visual building.
  Source: https://select.parallel.nl/

## Product rules

1. Dots are not the primary selector. They are allowed only as a last-resort fallback when the model
   is too dense or there is no facade geometry.
2. The primary selector is an apartment cell: rectangle, window rhythm, status stripe and short
   label.
3. Every cell is at least 44px in both directions on mobile. Current target: 86px x 48px on small
   screens.
4. Available = green stripe, reserved = amber stripe, sold = grey stripe. Recommended available
   apartments may pulse.
5. A tap selects. A drag beginning on the apartment area rotates the building. These two actions
   must coexist.
6. On mobile, the selected-apartment card is a controlled bottom sheet. It must not collapse the
   model stage or appear off-screen.
7. Public copy must say "פנייה", "התעניינות", "בדיקה", "יזם" or "מנהל הפרויקט". It must not say
   internal terms such as leads, funnel, CRM, paid placement or implementation prompts.

## CMS contract

The current implementation keeps the owner-editable source in `project_3d_units` JSON. Each unit
must support:

- `id`
- `label`
- `floor`
- `rooms`
- `sqm`
- `status`: `available`, `reserved`, `sold`
- `view` or `dir`
- `price_estimate` plus non-binding source note
- `recommended`
- `hotspot_position`
- `hotspot_normal`
- optional `plan_url`, `tour_url`, `interior_url`, `video_url`

Future UI should turn this JSON into a real repeater, but the public page must already behave as if
these are real inventory cells.

## QA gate

Run at 1440, 768, 390 and Edge mobile:

1. Cell markers render as rectangles, not dots.
2. Mobile cell target is at least 44px high and wide.
3. Tap a cell: selected card appears in view.
4. Drag from a cell: model rotates and accidental click is suppressed.
5. No horizontal overflow.
6. No visible internal wording.
7. One H1.
8. Healthcheck exposes the active feature marker.

