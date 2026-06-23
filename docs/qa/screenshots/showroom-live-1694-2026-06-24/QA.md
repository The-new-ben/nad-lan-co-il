# Showroom Live QA 1.69.4

Date: 2026-06-24
Target: https://nad-lan.co.il/projects/rainbow-tel-aviv/
Release: NadLan Config 1.69.4
Selected unit tested: `unit-38-penthouse`

## What was broken

Manual Chrome inspection before the fix showed the internal `model-viewer` hotspot buttons existed but were not real buyer tap targets. Their centers were outside the visible browser viewport, so using them as proof would have been false.

## What changed

The duplicate internal model-viewer hotspot layer is now hidden from the buyer surface and from keyboard focus. The visible apartment pins on the model stage are the selection layer.

## Live proof

- WordPress admin showed NadLan Config updated from 1.69.3 to 1.69.4.
- Live health endpoint returns `version: 1.69.4`.
- Desktop 1440 live test selected `unit-38-penthouse`.
- Mobile 390 live test selected `unit-38-penthouse`.
- Active unit after click: `unit-38-penthouse`.
- Camera orbit after click: `32deg 58deg auto`.
- Camera target after click: `0 124 7`.
- Visible apartment pins after load: 6.
- Visible internal model-viewer hotspots after release: 0.
- Mobile global floating CTA visible over the showroom after selection: false.
- Public-language leak sample: null.
- Small tap targets: none.

## Evidence files

- `desktop-1440-before-click.png`
- `desktop-1440-after-click-unit-38-penthouse.png`
- `mobile-390-before-click.png`
- `mobile-390-after-click-unit-38-penthouse.png`
- `showroom-live-qa-report.json`
- `desktop-1440-report.json`
- `mobile-390-report.json`

## Honest note

The QA script still reports a few mobile rectangles ending at x=395 on a 390 viewport in page sections around the showroom. The document scroll width remains 390 and the mobile screenshot does not show horizontal scrolling. I am not treating that as proof of a selection failure, but it should stay on the mobile layout cleanup list for the full project page pass.
