# Showroom live refresh check - 1.69.33

Date: 2026-06-24

## Scope

This check verifies whether the 1.69.33 showroom poster-flash fix can be proven on the public Rainbow page.

## Package result

The repository package for 1.69.33 is structurally valid:

- `plugin-dist/nadlan-config-1.69.33.zip` exists.
- Guarded verifier passed for version `1.69.33`.
- ZIP has 132 entries, 0 backslash paths, no absolute paths, no traversal, CRC OK.
- `project-3d.php` inside the ZIP contains `reveal="manual"`.
- `project-3d.php` inside the ZIP no longer contains `reveal="auto"`.
- The ZIP contains `dismissPoster()` reveal-after-load logic.
- Showroom style and script cache-busters are `1.69.33`.

## Live result

The public site could not prove the showroom fix because the tested Rainbow URLs return a 404 page:

- `https://nad-lan.co.il/projects/rainbow-tel-aviv/` returned the WordPress "Page not found" screen.
- `https://nad-lan.co.il/project/rainbow-tel-aviv/` also returned 404.
- `https://nad-lan.co.il/rainbow-sde-dov/` also returned 404.

The live REST root at `https://nad-lan.co.il/wp-json/` is reachable, but it does not list the `nadlan/v1` namespace. `https://nad-lan.co.il/wp-json/nadlan/v1/` returns `rest_no_route`.

## Honest conclusion

The code package is ready, but the public site is not currently exposing the NadLan Config plugin routes or the Rainbow showroom page. This means the visual refresh-flash fix is not live-proven yet.

Do not claim the 1.69.33 buyer experience is verified until:

1. The NadLan Config plugin is active and updated on WordPress.
2. Permalinks are refreshed if needed.
3. The Rainbow showroom URL returns the actual `.nlp3d` showroom.
4. A new timed screenshot run proves: poster visible at load, no blank cream stage at 400ms, GLB visible after load, and apartment selection still works.

## Files

- `error-viewport.png` - mobile screenshot of the public 404 page.
- `report.json` - Playwright run report for the failed public showroom check.
