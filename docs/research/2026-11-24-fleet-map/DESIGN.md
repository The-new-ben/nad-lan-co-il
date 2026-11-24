# HAD-823 design: before / after per width (local mock = the live page with the new bridge.js served in place)

No new visual language: the map keeps his look, his named places, his chips, his walking range and his beam. Only the grid row of the
view-and-map pair moves up. The page's raw HTML order (what Google reads without JavaScript) does not change.

| width | before (rendered order under the stage) | after |
|---|---|---|
| phones 360 / 390 (one column) | stage → price block `#nlpg` (~1,850 px) → view (~270) → map | stage → **map** (22 px under the stage) → view → price block |
| 768-1099 (one column) | as phones | as phones |
| 1100-1279 (two columns) | stage row → price block → view + map side by side | stage row → view + map side by side → price block |
| 1280+ (three columns) | stage row → price block (~2,200) → view + map side by side | stage row → **view + map side by side** (24 px under) → price block |

What moved down: the price block ("כמה עולה דירה ב...", the price calculator) now follows the view and the map. Nothing removed, no
wording touched. Above the stage nothing changes (H1, answer paragraph, buttons): the content-first order holds, and the new order
matches iron law 4 better (stage → view + map → facts) than before (stage → prices → view + map).

"הנוף והמפה" (the floor card button and step 2): on these pages it lands with the WHOLE map between the sticky header and the site's
bars (measured at the press, bars untouched), so the building and its beam (drawn low in the map, the flat's way up) never rest under
the WhatsApp pill. Phones pressed 5 times: 5/5 land the same.

Frames to compare (phone first): `before/rainbow-390x844-stage-end.png` vs `mock/rainbow-390x844-stage-end.png`;
`mock/rainbow-390x844-3-viewmap.png` (landing with the beam), `mock/rainbow-1440x900-3-viewmap.png` (desktop pair), and the same
names for ashira / duo.

Known and left as is (not in this order): the map section's own heading and chip rows sit above the map canvas on phones (~400 px),
the site's price-alert sheet can open over the map after a while on Rainbow (its own timing rules), and price pills sit close to the
building's dot in the beam view (areamap's own layout).
