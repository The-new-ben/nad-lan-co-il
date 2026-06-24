# Showroom Live QA - 1.69.41 Premium Grid

Date: 2026-06-24
Site: https://nad-lan.co.il/projects/rainbow-tel-aviv/
Release: NadLan Config 1.69.41
Commit: 6b67982

## What Was Verified

- WordPress admin plugin row updated from 1.69.40 to 1.69.41.
- Public healthcheck returns `version: 1.69.41`.
- Public healthcheck includes `project_3d.premium_showroom_grid_v16941: true`.
- Desktop selected state now uses the premium two-column showroom grid:
  - stage on the left
  - selected apartment panel on the right
- Mobile 390 selected state remains single-column with no horizontal overflow.
- Four live unit selections were tested:
  - `unit-08-sw`
  - `unit-16-w`
  - `unit-24-nw`
  - `unit-31-se`
- Each tested unit opened the selected apartment card and set a different `camera-orbit` and `camera-target`.
- Public leak scan in the QA script found no sample of: Lovable, Codex, prompt, token, Tailwind, React, Featured, Sponsored, Promoted.

## Screenshots

Main proof:

- `desktop-1440-before-click.png`
- `desktop-1440-after-click-unit-16-w.png`
- `mobile-390-before-click.png`
- `mobile-390-after-click-unit-16-w.png`

Additional multi-unit proof:

- `multi-unit-08-sw/`
- `multi-unit-24-nw/`
- `multi-unit-31-se/`

Each folder contains desktop and mobile before/after screenshots plus JSON runtime proof.

## Honest Visual Assessment

This is a real improvement toward Lovable's premium reference. The selected apartment panel is no longer pushed below the stage on desktop. It now sits beside the stage and the page reads more like a showroom surface.

This is not finished. The stage is 642px high as requested, but the current rendered building visual occupies only the upper part of that stage, leaving a large cream void below it. That is visible in the screenshots and should be the next visual refinement. The current selection system is still authored unit pins plus fallback behavior, not true BIM/window-level apartment picking.

## Runtime Proof Summary

`unit-08-sw`:

- desktop orbit: `45deg 66deg 38m`
- desktop target: `0m 31m 6m`
- mobile width: `390`, scrollWidth: `390`

`unit-16-w`:

- desktop orbit: `35deg 63deg 38m`
- desktop target: `-5m 55m 7m`
- mobile width: `390`, scrollWidth: `390`

`unit-24-nw`:

- desktop orbit: `24deg 61deg 38m`
- desktop target: `-6m 80m 5m`
- mobile width: `390`, scrollWidth: `390`

`unit-31-se`:

- desktop orbit: `310deg 64deg 38m`
- desktop target: `6m 101m -5m`
- mobile width: `390`, scrollWidth: `390`

## Next Fix

Fill the premium stage correctly without stacking old CSS:

1. Keep one active showroom stylesheet.
2. Make the visual/model area occupy the full premium stage intentionally.
3. Preserve the right-side selected panel on desktop.
4. Preserve 390px mobile with no overflow.
5. Re-run this same live QA.
