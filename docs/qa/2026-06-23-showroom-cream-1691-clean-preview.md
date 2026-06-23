# Showroom 1.69.1 Cream Preview QA

Date: 2026-06-23
Branch: `strategy/nadlan-seo-product-war-plan`
Target: Rainbow Tel Aviv project showroom

## Scope

This QA records branch preview evidence for the 1.69.1 cream showroom release. The live site still reports plugin `1.68.2`, so these screenshots are not live deployment proof.

The preview harness loaded the public Rainbow page, removed the live 1.68.2 showroom style blocks, injected the local 1.69.1 cream stylesheet, selected a unit, captured desktop, tablet, mobile, and focused stage screenshots, then wrote `report.json`.

## Files

- `docs/qa/screenshots/showroom-cream-1691-clean-preview/desktop-1440.png`
- `docs/qa/screenshots/showroom-cream-1691-clean-preview/tablet-768.png`
- `docs/qa/screenshots/showroom-cream-1691-clean-preview/mobile-390.png`
- `docs/qa/screenshots/showroom-cream-1691-clean-preview/edge-mobile-390.png`
- `docs/qa/screenshots/showroom-cream-1691-clean-preview/stage-desktop-1440.png`
- `docs/qa/screenshots/showroom-cream-1691-clean-preview/stage-tablet-768.png`
- `docs/qa/screenshots/showroom-cream-1691-clean-preview/stage-mobile-390.png`
- `docs/qa/screenshots/showroom-cream-1691-clean-preview/stage-edge-mobile-390.png`
- `docs/qa/screenshots/showroom-cream-1691-clean-preview/report.json`

## Automated Results

- Viewports passed: 4 of 4.
- Horizontal overflow: none detected.
- H1 count: one.
- Public leak scan: none detected.
- Minimum tap target: 44px.
- Preview CSS replacement: enabled.
- Removed live showroom style blocks per viewport: 3.
- Injected local 1.69.1 cream CSS: yes.

## Visual Review

Passed:

- The old dark showroom CSS functions were removed from `project-3d.php`; the file now has one active showroom CSS function.
- The visible showroom shell is cream, not dark teal.
- The model stage background is light.
- Loose environment names no longer appear as public text inside the model area.
- Mobile 390px no longer has instruction text overlapping the model.
- The selected-unit details column is contained and wraps inside the cream layout.

Known limitation:

- Rainbow still lacks an approved facade asset in this data state, so the right side truthfully shows the premium missing-facade state.
- This is preview evidence against live markup plus injected local CSS. After the owner deploys 1.69.1, capture live screenshots again without CSS injection.

## Release Checks

- `php -l plugins/nadlan-config/inc/project-3d.php`: passed.
- `php -l plugins/nadlan-config/nadlan-config.php`: passed.
- `php -l plugins/nadlan-config/inc/health.php`: passed.
- `node --check scripts/qa-project-showroom-visual.mjs`: passed.
- `python scripts/build-plugin-zip.py 1.69.1`: passed, 132 entries, zero backslash paths, rooted, CRC OK.
- `python scripts/verify-plugin-release.py 1.69.1`: passed.

