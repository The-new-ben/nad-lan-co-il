# Rainbow Showroom Surface Pick QA - 1.69.16

Date: 2026-06-24  
Site: https://nad-lan.co.il/projects/rainbow-tel-aviv/  
Plugin version verified live: 1.69.16  
Result: PASS for desktop 1440 and mobile 390

## Goal

When a buyer taps the real 3D model surface, the showroom should select the closest authored apartment, set both `camera-orbit` and `camera-target`, and open the selected-apartment card.

## What Was Tested

The QA script rejected taps that landed on visible marker buttons. It chose a point where `document.elementFromPoint()` returned `MODEL-VIEWER`, then clicked that model surface.

The script also wrapped `modelViewer.positionAndNormalFromPoint()` during the test. That proves the production click path called the real model-viewer mesh-pick API, not only the overlay marker path.

Desktop result:

- Tap surface: `MODEL-VIEWER`
- Marker at tap point: none
- Mesh hit: yes
- Expected unit from mesh: `unit-16-w`
- Active unit after tap: `unit-16-w`
- Camera orbit after tap: `35deg 63deg auto`
- Camera target after tap: `-5 55 7`
- Unit card visible: yes

Mobile 390 result:

- Tap surface: `MODEL-VIEWER`
- Marker at tap point: none
- Mesh hit: yes
- Expected unit from mesh: `unit-16-w`
- Active unit after tap: `unit-16-w`
- Camera orbit after tap: `35deg 63deg auto`
- Camera target after tap: `-5 55 7`
- Unit card visible: yes

## Evidence Files

- `desktop-1440-before-surface-mesh-pick.png`
- `desktop-1440-after-surface-mesh-pick.png`
- `mobile-390-before-surface-mesh-pick.png`
- `mobile-390-after-surface-mesh-pick.png`
- `showroom-surface-mesh-pick-report.json`

## Honest Limitations

Native `<model-viewer>` hotspot buttons are still hidden. A separate prototype showed those native hotspots project poorly with the current Rainbow model and authored coordinates, so shipping them would make apartment selection worse.

This is not yet true per-window BIM picking. The shipped behavior is: tap real GLB surface, read the mesh point with `positionAndNormalFromPoint()`, then select the closest authored apartment point from `unit-map.json`.

That is a real model-surface interaction and a major improvement over marker-only selection, but the contractor-grade final version still needs either better authored facade/window geometry or a dedicated unit mesh layer.

## Source Basis

- Lovable showroom redesign §4: unit selection must set both camera orbit and camera target from `unit-map.json`.
- Official model-viewer API docs: `positionAndNormalFromPoint(clientX, clientY)` returns the mesh position under a screen point.  
  https://modelviewer.dev/docs/
