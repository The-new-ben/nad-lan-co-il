# Rainbow 3D Runtime Hotfix QA - v1.60.6

## Scope

Live v1.60.5 failed during project-3D startup on the Rainbow page. The visible symptom was a frozen/jammed selector: floor plates did not render, stage buttons did not reliably work, and the building could not be used as the main interface.

## Root Cause

The stage details handler referenced `detail` inside `init()` but no local variable declared `.nlp3d-detail`. That produced:

```text
ReferenceError: detail is not defined
```

Because the exception happens during boot, the remaining selector setup does not complete.

## Fix

- Declare `var detail = root.querySelector('.nlp3d-detail');` before binding stage actions.
- Guard the optional Mapbox 3D-building extrusion layer behind `liveMap.getSource('composite')` and `!liveMap.getLayer('nlp3d-3d-buildings')`.

## Local Gate

- Browser reproduction on live v1.60.5 confirmed the `detail is not defined` startup exception.
- Expected post-fix gate:
  - no `detail is not defined` console error;
  - `.nlp3d-plate` elements render;
  - angle buttons update active state;
  - orbit button toggles spin state;
  - stage details/view/inquiry buttons do not throw;
  - Mapbox missing `composite` source does not throw a page error.

## Boundary

This is a runtime hotfix only. It does not add the deferred v1.61.0 content/SEO migrator, pricing inventory, Cesium/Google photogrammetry, or a real purchase room.
