# QA - Showroom live 1.69.40 after update

Date: 2026-06-24
Live URL: https://nad-lan.co.il/projects/rainbow-tel-aviv/?codex_qa=live_16940_after
Plugin healthcheck: 1.69.40
Commit: 979e8ee

## What passed

- Live healthcheck reports `version = 1.69.40`.
- Live healthcheck reports `real_model_scene_truth_v16940 = true`.
- Live healthcheck reports `desktop_toolbar_touch_v16940 = true`.
- Desktop and mobile each render one `model-viewer`.
- Selecting `unit-16-w` sets the active unit.
- Camera orbit and camera target change after selection.
- Mobile 390 has no horizontal page overflow.
- Public-language scan found no banned internal terms in the tested viewport.
- Tap targets passed the QA script.

## Screenshot files

- `desktop-1440-before-click.png`
- `desktop-1440-after-click-unit-16-w.png`
- `mobile-390-before-click.png`
- `mobile-390-after-click-unit-16-w.png`
- `showroom-live-qa-report.json`

## Honest visual finding

This release is not the full Lovable premium target. It is a narrow source-truth fix.

The selected unit works and the scene no longer uses the CSS pseudo grid when a real model-viewer scene exists, but the page still reads as a picture-based stage and not as the canonical Lovable showroom. The selected panel is still below the stage on desktop instead of a persistent right column. Mobile still compresses the visual stage.

## Next required implementation

Implement Lovable PR 1 from `handoff/lovable/2026-06-24-premium-pattern/07-codex-build-plan.md`:

- Replace the active showroom shell.
- Build the 1240px premium grid.
- Stage is the visual center.
- Selected apartment panel is persistent at right on desktop and below the rail on mobile.
- Unit rail is explicit.
- Keep SEO real-estate public language.
- Do not stack another CSS layer over the current patch.
