# Showroom 1.69.1 Cream Skin Preview QA

Date: 2026-06-23

Scope: Rainbow project showroom, branch preview of the 1.69.1 cream-luxury CSS on the live public page.

Important status: this is not live-deploy proof. The screenshots were captured from the live Rainbow page with the current branch CSS injected for preview. Final live proof still requires plugin activation on production and a second screenshot pass after cache clear.

## Proof files

- Desktop: `docs/qa/screenshots/showroom-cream-1691-no-stack/desktop-1440.png`
- Tablet: `docs/qa/screenshots/showroom-cream-1691-no-stack/tablet-768.png`
- Mobile 390: `docs/qa/screenshots/showroom-cream-1691-no-stack/mobile-390.png`
- Edge mobile 390: `docs/qa/screenshots/showroom-cream-1691-no-stack/edge-mobile-390.png`
- Machine report: `docs/qa/screenshots/showroom-cream-1691-no-stack/report.json`

## Automated result

- 4 of 4 viewports passed.
- Horizontal overflow: none.
- H1 count: one.
- Public internal-language terms: none detected by the harness.
- Facade truth: no fake apartment cells rendered while the real facade asset is missing.
- Tap targets: minimum 48px in the tested viewports.

## Visual assessment

What works:

- The public showroom shell is now cream, bright, and editorial instead of a dark page.
- Typography is closer to the intended premium Hebrew magazine direction.
- Cards, copy blocks, borders, and surfaces are quieter and more consistent.
- Mobile 390 is contained and does not crop the showroom root.
- The missing-facade state is truthful: it does not fake a facade or apartment grid.

What is still not ideal:

- The current real model-viewer canvas still renders as a dark green 3D viewport on mobile. The page skin around it is cream, but the actual model area remains darker because it comes from the 3D rendering/model-viewer surface, not from the surrounding WordPress chrome.
- This should not be faked with an unrelated image. The right follow-up is a real model/material/rendering pass or a contractor-supplied better GLB/facade package.
- The screenshot is a branch preview. After deploy, repeat the same screenshots without injection.

## No-stacking check

- Active `nadlan-p3d` style enqueue now points to one primary stylesheet function: `nadlan_p3d_lovable_showroom_v1690_css()`.
- Old dark CSS functions remain in source history but are not actively enqueued in the showroom path.
- Footer CSS repaint hooks for the old article/floating-action layers are not active for this release path.

## Release checks

- PHP lint passed for the changed plugin files.
- Guarded ZIP builder passed for `nadlan-config-1.69.1.zip`.
- Release verifier passed after sequential rebuild and verification.

## Verdict

Technically shippable as a cream-skin preview release, with one honest visual caveat: the real 3D canvas still has a dark viewport. Do not claim the 3D model itself has been redesigned. Claim only the public showroom shell, copy hygiene, containment, and release packaging.
