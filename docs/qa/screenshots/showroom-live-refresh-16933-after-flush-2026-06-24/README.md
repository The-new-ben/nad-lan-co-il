# Showroom live refresh check after permalink recovery - 1.69.33

Date: 2026-06-24

## Recovery

WP Admin showed `NadLan Config` active at version `1.69.33`. The plugin was not deactivated.

The public project URLs and NadLan REST routes were returning 404 because WordPress rewrite rules were stale after the plugin update. I opened WordPress Admin, saved Settings > Permalinks, and WordPress confirmed that the permalink structure was updated.

## Live checks after recovery

- `/projects/rainbow-tel-aviv/` returned HTTP 200 anonymously.
- `/projects/` returned HTTP 200 anonymously.
- `/wp-json/nadlan/v1/healthcheck` returned HTTP 200 anonymously with `version: 1.69.33`, `cpt_present: true`, and `nadlan_project_cpt: true`.
- The Rainbow page root contained `.nlp3d`.
- The showroom `model-viewer` used `reveal="manual"`.

## Refresh flash check

Timed screenshots show the stage poster stayed visible after page load:

- `t00-domcontentloaded-stage.png`
- `t04-400ms-stage.png`
- `t20-2s-stage.png`
- `t70-7s-stage.png`

No blank cream stage was reproduced in this run after the route recovery.

## Apartment selection check

Manual-style browser automation clicked the visible floor 16 marker on the public Rainbow page.

Proof files:

- `selection-before-click-stage.png`
- `selection-after-click-floor-16-stage.png`
- `selection-report.json`

Captured result:

- `pickCount: 6`
- selected unit: `unit-16-w`
- `camera-orbit: 35deg 63deg auto`
- `camera-target: -5m 55m 7m`
- the selected card changed to the floor 16 apartment

## Honest limitation

This run proves route recovery, stable poster display, visible unit markers, marker selection, selected-card state, and camera attribute updates.

It does not prove that the GLB fully rendered in browser automation. The `has-model-viewer-loaded` state remained false in the captured runs. The next technical task is to verify and fix real model first-render/load behavior, separate from the route recovery and marker-selection behavior proven here.
