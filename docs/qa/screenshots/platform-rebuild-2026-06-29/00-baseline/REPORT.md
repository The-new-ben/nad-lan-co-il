# Baseline Platform QA

Date: 2026-06-29
Browser: installed Google Chrome via Playwright `channel: chrome`

## Summary Table

| Page | Viewport | Status | lang | dir | H1 | #nl-root | .nlv2 | .nlp3d | Home band | Overflow | Console errors | 404s | Screenshot |
| --- | --- | ---: | --- | --- | ---: | ---: | ---: | ---: | ---: | --- | ---: | ---: | --- |
| home | desktop-1440 | 200 | he-IL | rtl | 1 | 0 | 0 | 0 | 0 | no | 0 | 0 | home-desktop-1440.png |
| home | mobile-390 | 200 | he-IL | rtl | 1 | 0 | 0 | 0 | 0 | no | 0 | 0 | home-mobile-390.png |
| home-preview | desktop-1440 | 200 | he-IL | rtl | 1 | 0 | 0 | 0 | 0 | no | 0 | 0 | home-preview-desktop-1440.png |
| home-preview | mobile-390 | 200 | he-IL | rtl | 1 | 0 | 0 | 0 | 0 | no | 0 | 0 | home-preview-mobile-390.png |
| projects | desktop-1440 | 200 | he-IL | rtl | 2 | 0 | 0 | 0 | 0 | no | 0 | 0 | projects-desktop-1440.png |
| projects | mobile-390 | 200 | he-IL | rtl | 2 | 0 | 0 | 0 | 0 | no | 0 | 0 | projects-mobile-390.png |
| ashira-he | desktop-1440 | 200 | he | rtl | 1 | 1 | 0 | 0 | 0 | no | 0 | 0 | ashira-he-desktop-1440.png |
| ashira-he | mobile-390 | 200 | he | rtl | 1 | 1 | 0 | 0 | 0 | no | 0 | 0 | ashira-he-mobile-390.png |
| ashira-en | desktop-1440 | 200 | en | ltr | 1 | 1 | 0 | 0 | 0 | no | 0 | 0 | ashira-en-desktop-1440.png |
| ashira-en | mobile-390 | 200 | en | ltr | 1 | 1 | 0 | 0 | 0 | no | 0 | 0 | ashira-en-mobile-390.png |
| rainbow | desktop-1440 | 200 | he-IL | rtl | 1 | 0 | 0 | 1 | 0 | no | 0 | 0 | rainbow-desktop-1440.png |
| rainbow | mobile-390 | 200 | he-IL | rtl | 1 | 0 | 0 | 1 | 0 | no | 0 | 0 | rainbow-mobile-390.png |
| dimri | desktop-1440 | 200 | he-IL | rtl | 1 | 0 | 0 | 1 | 0 | no | 0 | 0 | dimri-desktop-1440.png |
| dimri | mobile-390 | 200 | he-IL | rtl | 1 | 0 | 0 | 1 | 0 | no | 0 | 0 | dimri-mobile-390.png |
| calculator | desktop-1440 | 200 | he-IL | rtl | 1 | 0 | 0 | 0 | 0 | no | 0 | 0 | calculator-desktop-1440.png |
| calculator | mobile-390 | 200 | he-IL | rtl | 1 | 0 | 0 | 0 | 0 | no | 0 | 0 | calculator-mobile-390.png |
| professionals | desktop-1440 | 200 | he-IL | rtl | 2 | 0 | 0 | 0 | 0 | no | 0 | 0 | professionals-desktop-1440.png |
| professionals | mobile-390 | 200 | he-IL | rtl | 2 | 0 | 0 | 0 | 0 | no | 0 | 0 | professionals-mobile-390.png |
| guide | desktop-1440 | 200 | he-IL | rtl | 1 | 0 | 0 | 0 | 0 | no | 0 | 0 | guide-desktop-1440.png |
| guide | mobile-390 | 200 | he-IL | rtl | 1 | 0 | 0 | 0 | 0 | no | 0 | 0 | guide-mobile-390.png |
| healthcheck | desktop-1440 | 200 |  |  | 0 | 0 | 0 | 0 | 0 | no | 1 | 0 | healthcheck-desktop-1440.png |
| healthcheck | mobile-390 | 200 |  |  | 0 | 0 | 0 | 0 | 0 | no | 0 | 0 | healthcheck-mobile-390.png |
| content-gaps | desktop-1440 | 404 |  |  | 0 | 0 | 0 | 0 | 0 | no | 1 | 1 | content-gaps-desktop-1440.png |
| content-gaps | mobile-390 | 404 |  |  | 0 | 0 | 0 | 0 | 0 | no | 1 | 1 | content-gaps-mobile-390.png |

## Key Failures To Fix Before Platform V1
- Homepage project band is absent on live baseline.
- Mobile homepage header/nav has clipped offscreen controls at 390px.
- Some pages expose forbidden public terms. See report.json.

## Anti-Stack Baseline

- New factory project pages should ultimately show `#nl-root = 1` and `.nlv2-showroom = 0`.
- Legacy `.nlp3d` counts are recorded so we can avoid stacking old project-3D with the new factory.
- Homepage band should be exactly `1` only after a controlled insertion method is chosen.

## Raw Data

See `report.json` in this folder for console errors, network 404s, text leaks and offscreen nav geometry.