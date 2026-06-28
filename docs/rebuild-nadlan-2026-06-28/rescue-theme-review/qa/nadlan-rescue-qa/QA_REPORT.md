# NadLan Rescue Showroom Theme — QA Report

Generated in the sandbox from the uploaded handoff assets and engine bundle.

## Static checks
- PHP lint: passed for every PHP file.
- JavaScript syntax: passed for `engine.js`, `data.js`, `i18n.js`.
- Theme ZIP integrity: tested after packaging.

## Browser screenshots
Screenshots were taken with Playwright/Chromium from the generated static previews.

| Screenshot | Width | Result |
|---|---:|---|
| `desktop-he-1440.png` | 1440 | `#nl-root` = 1, `.nlv2-showroom` = 0, no horizontal overflow, lang `he`, dir `rtl`, no visible banned terms |
| `desktop-en-1440.png` | 1440 | `#nl-root` = 1, `.nlv2-showroom` = 0, no horizontal overflow, lang `en`, dir `ltr`, no visible banned terms |
| `mobile-he-390.png` | 390 | `#nl-root` = 1, `.nlv2-showroom` = 0, no horizontal overflow, lang `he`, dir `rtl`, no visible banned terms |
| `home-1440.png` | 1440 | `#nl-root` = 1, `.nlv2-showroom` = 0, no horizontal overflow, lang `he`, dir `rtl`, no visible banned terms |

Visible banned term scan covered: `GLB`, `BIM`, `hotspot`, `mesh`, `Lovable`, `Codex`, `Featured`, `Sponsored`, and placeholder marker `⟦`.

## Honest caveats
- This package was not deployed to the live NadLan site.
- The model assets are concept/showroom assets from the uploaded bundle, not official developer inventory.
- The FR/RU/AR UI has meaningful key labels and page scaffolding, but it is not a human legal/SEO translation pass.
- The theme uses a standalone emergency lead endpoint so it does not interfere with an existing production lead pipeline.
