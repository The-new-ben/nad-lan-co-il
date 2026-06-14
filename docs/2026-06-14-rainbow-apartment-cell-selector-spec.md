# Rainbow Apartment Cell Selector Spec

Date: 2026-06-14

## Owner Problem

The live selector used abstract round markers. That is not enough for a buyer. A buyer needs to
recognize the clickable target as an apartment on the building, understand whether it is available,
then get apartment details and a next step.

## Research Signals

- Zillow's interactive floor-plan material frames floor plans and 3D tours as a way to move a
  listing from static media into a stronger digital shopping experience.
- Zillow Rentals' interactive property-map launch describes a buyer/renter pattern where users
  click an available unit and understand its floor, orientation and context before taking action.
- DIGBY's apartment-selector case study describes marking active areas on a 3D rendered development
  so buyers can choose an apartment and then see floor plans, images and sales data.
- Parallel Select describes a facade selector where the visitor rotates around the building and
  units change color by sales status.
- model-viewer supports HTML hotspot children with `slot="hotspot-..."`, so the same CMS unit data
  can render apartment-shaped controls on a real GLB model.

Sources:

- https://www.zillow.com/3d-home/floor-plans/
- https://zillow.mediaroom.com/2023-03-15-Room-with-a-view-Renters-can-now-use-interactive-property-maps-to-choose-their-apartment-on-Zillow
- https://digby.hu/apartment-selector
- https://select.parallel.nl/
- https://modelviewer.dev/examples/annotations

## Product Decision

The default visible control is no longer a dot. It is an apartment cell:

- rectangular, like a small facade bay;
- status stripe: available, reserved, sold;
- window rhythm inside the rectangle so it reads as a unit/floor cell;
- label inside the cell on desktop;
- large touch target on mobile;
- recommended units pulse only when available;
- the selected unit still opens the existing selected-apartment card, comparison and inquiry flow.

## What This Patch Does

Version 1.65.5 keeps the existing unit-selection state machine and changes the visual language:

- `.nlp3d-stage-pick` renders as a facade-like apartment cell instead of a circular dot.
- `.nlp3d-mv-hotspot` renders the same cell treatment for model-viewer hotspots.
- Sold cells are muted; reserved cells are amber; available cells are green.
- Tooltips remain for desktop hover/focus, while the selected-apartment card remains the primary
  detail surface on mobile.
- Healthcheck exposes `project_3d.apartment_cell_selector_v1655`.

## What Is Still Approximate

The rectangles are still driven from the current CMS unit coordinates and hotspot positions. They
are not official architectural apartment footprints. For exact apartment geometry, the owner or
developer must provide official BIM, elevation drawings or a licensed unit map. Until then, public
copy should remain illustrative and non-binding.

## QA Gate

- Desktop: apartment cells visible on the showroom, not dots.
- Mobile: cells remain at least 44px target area and do not cover the entire model.
- Click/tap on an available cell updates the selected apartment card.
- Sold cell does not route as an available unit.
- Recommended available cell pulses.
- No horizontal overflow.
- Healthcheck version is 1.65.5 and `apartment_cell_selector_v1655` is true.
