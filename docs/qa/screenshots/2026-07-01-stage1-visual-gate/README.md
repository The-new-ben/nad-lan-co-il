# Stage 1 Visual Gate Evidence

Generated: 2026-07-01

## Project Showroom Gate

Both project runs used the live page plus the local `1.69.66` preview CSS path from `scripts/qa-project-showroom-visual.mjs` so the screenshots represent this branch before the WordPress plugin update is installed.

| Project | Result | Report |
| --- | --- | --- |
| Rainbow Tel Aviv | PASS, 4/4 viewports | `rainbow-tel-aviv/report.json` |
| Dimri Yama | PASS, 4/4 viewports | `dimri-yama/report.json` |

Required screenshots:

- `rainbow-tel-aviv/desktop-1440.png`
- `rainbow-tel-aviv/tablet-768.png`
- `rainbow-tel-aviv/mobile-390.png`
- `dimri-yama/desktop-1440.png`
- `dimri-yama/tablet-768.png`
- `dimri-yama/mobile-390.png`

Gate checks passed in both reports:

- `scrollWidth - clientWidth <= 2`
- one visible H1
- apartment selection opens the selected card
- selected unit receives `aria-pressed="true"`
- no fake facade grid without a real facade image
- tap targets are at least 44px
- no internal public wording markers found
- no HTML/PHP leak markers found

## Public Trust Capture

`public-trust/report.json` contains the live production capture for homepage, `/join-pro/`, `/sitemap/`, `/professionals/`, and a project page across desktop, tablet, and mobile.

Current live production still reports legacy Woo/text leaks before the `1.69.66` package is installed. This branch contains the server-side removals in `functions.php`; the capture is retained as baseline evidence.
