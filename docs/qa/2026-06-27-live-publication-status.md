# 2026-06-27 Live Publication Status

## Summary

The prepared NadLan homepage and Ashira showroom content were written to the live WordPress database
and published. The live plugin healthcheck is stable at `nadlan-config` version `1.69.41`.

The Ashira project pages are live in Hebrew, English, French, Russian, and Arabic. Browser QA using
the installed Google Chrome channel produced desktop and mobile screenshots. The Ashira pages passed
the current no-overflow / no-console-error gate.

One homepage JavaScript asset-base issue was found after publication: the showroom engine requested
`/assets/engine/projects.json` from the site root. The correct fallback is the theme asset base. The
source fix is in `assets/js/nadlan-showroom-engine.js` and still needs to be deployed through the
normal Git/theme update path.

## Live Pages

- Homepage: https://nad-lan.co.il/
- Ashira Hebrew: https://nad-lan.co.il/projects/ashira-sde-dov/
- Ashira English: https://nad-lan.co.il/projects/ashira-sde-dov-en/
- Ashira French: https://nad-lan.co.il/projects/ashira-sde-dov-fr/
- Ashira Russian: https://nad-lan.co.il/projects/ashira-sde-dov-ru/
- Ashira Arabic: https://nad-lan.co.il/projects/ashira-sde-dov-ar/

## WordPress Records

- Homepage updated: page ID `2`, slug `home`, status `publish`
- Ashira Hebrew updated: post ID `4744`, slug `ashira-sde-dov`, status `publish`
- Ashira English created: post ID `4927`, slug `ashira-sde-dov-en`, status `publish`
- Ashira French created: post ID `4926`, slug `ashira-sde-dov-fr`, status `publish`
- Ashira Russian created: post ID `4924`, slug `ashira-sde-dov-ru`, status `publish`
- Ashira Arabic created: post ID `4925`, slug `ashira-sde-dov-ar`, status `publish`

## Proof Artifacts

HTML snapshots:

- `docs/qa/screenshots/live-publish-check/home-after-publish.html`
- `docs/qa/screenshots/live-publish-check/ashira-he-after-publish.html`
- `docs/qa/screenshots/live-publish-check/ashira-en-after-publish.html`
- `docs/qa/screenshots/live-publish-check/ashira-fr-after-publish.html`
- `docs/qa/screenshots/live-publish-check/ashira-ru-after-publish.html`
- `docs/qa/screenshots/live-publish-check/ashira-ar-after-publish.html`

Google Chrome screenshots:

- `docs/qa/screenshots/live-publish-check/browser/home-desktop-1440.png`
- `docs/qa/screenshots/live-publish-check/browser/home-mobile-390.png`
- `docs/qa/screenshots/live-publish-check/browser/ashira-he-desktop-1440.png`
- `docs/qa/screenshots/live-publish-check/browser/ashira-he-mobile-390.png`
- `docs/qa/screenshots/live-publish-check/browser/ashira-en-desktop-1440.png`
- `docs/qa/screenshots/live-publish-check/browser/ashira-en-mobile-390.png`
- `docs/qa/screenshots/live-publish-check/browser/ashira-fr-desktop-1440.png`
- `docs/qa/screenshots/live-publish-check/browser/ashira-fr-mobile-390.png`
- `docs/qa/screenshots/live-publish-check/browser/ashira-ru-desktop-1440.png`
- `docs/qa/screenshots/live-publish-check/browser/ashira-ru-mobile-390.png`
- `docs/qa/screenshots/live-publish-check/browser/ashira-ar-desktop-1440.png`
- `docs/qa/screenshots/live-publish-check/browser/ashira-ar-mobile-390.png`
- `docs/qa/screenshots/live-publish-check/browser/report.json`

## QA Result

- Ashira Hebrew/English/French/Russian/Arabic: live browser QA passed for desktop `1440px` and
  mobile `390px`.
- Ashira pages: `data-nlv2-showroom` present, no horizontal overflow, no console errors.
- Homepage: live content is published and screenshot captured, but the engine asset fallback bug
  caused a root-relative JSON request. This is fixed locally in source and must be deployed before
  the homepage gate is considered green.

## Remaining Deploy Step

Deploy the source fix in `assets/js/nadlan-showroom-engine.js`, then re-run the homepage browser QA.
The expected post-deploy proof is:

- No request to `https://nad-lan.co.il/assets/engine/projects.json`
- The engine loads projects from the theme asset path
- Homepage desktop/mobile screenshots render without console errors
- No horizontal overflow at `1440px` or `390px`
