# HAD-823 before: where the map sits on Rainbow, Ashira, DUO (live 1.72.767/768, 24.11.2026 ~12:30-13:30 Israel time)

Read-only visitor loads in headless Chrome (real GPU), one page at a time. Scripts: `measure.py` (layout), `press.py` (tap, "הנוף והמפה", beam).
Raw numbers: `before/measure.json`, `before/press.json`; frames `before/<page>-<size>-*.png`.

## Stage end vs map top (document y, px)

| page | size | stage ends | map starts | gap | what sits between |
|---|---|---|---|---|---|
| Rainbow | 360x740 | 1,833 | 4,039 | 2,206 | price block `#nlpg` (1,892) + view (264) |
| Rainbow | 390x844 | 1,824 | 4,002 | 2,178 | `#nlpg` (1,847) + view (281) |
| Rainbow | 1280x720 | 1,014 | 3,377 | 2,363 | `#nlpg` (2,325); view beside the map |
| Rainbow | 1440x900 | 1,100 | 3,311 | 2,211 | `#nlpg` (2,173) |
| Ashira | 360x740 | 2,518 | 4,595 | 2,077 | `#nlpg` (1,763) + view (264) |
| Ashira | 390x844 | 2,597 | 4,664 | 2,068 | `#nlpg` (1,737) + view (281) |
| Ashira | 1280x720 | 1,033 | 2,948 | 1,916 | `#nlpg` (1,878) |
| Ashira | 1440x900 | 1,119 | 2,909 | 1,790 | `#nlpg` (1,752) |
| DUO | 360x740 | 1,745 | 3,936 | 2,192 | `#nlpg` (1,877) + view (264) |
| DUO | 390x844 | 1,764 | 3,899 | 2,135 | `#nlpg` (1,804) + view (281) |
| DUO | 1280x720 | 981 | 2,659 | 1,679 | `#nlpg` (1,641) |
| DUO | 1440x900 | 1,119 | 2,728 | 1,609 | `#nlpg` (1,571) |

The block in the way is the price section `#nlpg` ("כמה עולה דירה ב...", the price calculator, the 3D-tour heading), placed by the
page grid in the "prices" row between the stage row and the "below" row (view + map). Source: `inc/project-stage.php`
grid-template-areas (`... "prices" "below" ...`). In the raw HTML the map is already inside `.nlps-below`, right after the view.

## The beam today
`bridge.js showBeam` (the engine's wedge, #C2563A, drawn from outside engine.js) on `nl:facing`: the map turns so the flat's way is
up, 450 m ahead. Pressed: desktop 1440 Rainbow 270°/270°, Ashira 281°/281°, DUO correct after a second side (90/101/100). On phones,
after "הנוף והמפה" the page lands on the view; the map is ~2,000 px lower and has not started (it starts only when a visitor stops on
it), so at that moment there is no beam on screen (beam1 = none on all three phones); it draws when the visitor scrolls down to it.
Under the site's bars at rest: no control of the card half under a bar in these presses. Console: only the two blocked analytics
requests (the press blocks them).
