# Screenshot QA

**Date:** 2026-07-21
**Tool:** headless Chromium via Playwright 1.61.1
**Scope:** static review artifacts only; not the public WordPress site
**Viewports:** desktop 1440×1000 and mobile 390×900; full-page capture

## Automated results

| Page | Viewport | Full height | Client / scroll width | Direction | Missing images | Browser errors | Result |
| --- | ---: | ---: | --- | --- | ---: | ---: | --- |
| Homepage | 1440 | 6091 | 1440 / 1440 | RTL | 0 | 0 | Pass |
| Homepage | 390 | 12884 | 390 / 390 | RTL | 0 | 0 | Pass |
| Projects + map | 1440 | 2142 | 1440 / 1440 | RTL | 0 | 0 | Pass |
| Projects + map | 390 | 3938 | 390 / 390 | RTL | 0 | 0 | Pass |
| Project detail | 1440 | 5403 | 1440 / 1440 | RTL | 0 | 0 | Pass |
| Project detail | 390 | 8567 | 390 / 390 | RTL | 0 | 0 | Pass |
| Foreign investor | 1440 | 5062 | 1440 / 1440 | LTR | 0 | 0 | Pass |
| Foreign investor | 390 | 9006 | 390 / 390 | LTR | 0 | 0 | Pass |
| Developer Studio | 1440 | 2715 | 1440 / 1440 | RTL | 0 | 0 | Pass |
| Developer Studio | 390 | 5918 | 390 / 390 | RTL | 0 | 0 | Pass after fix |

Fonts loaded as intended: Heebo for body/UI and Frank Ruhl Libre for Hebrew headings; the English page uses Georgia for display in this self-contained review.

## Visual inspection

### Homepage

- Search and real-estate imagery dominate the first viewport.
- The page visibly contains many project, area, data, tool and editorial doors without losing the cream/ink/gold identity.
- Featured project media is strong enough to communicate the target, and every concept image is visibly labelled.
- Mobile becomes one column, keeps search first and has no horizontal overflow.

### Projects + map

- Desktop establishes the familiar filter/list/map grammar.
- Card facts and evidence hierarchy remain scannable.
- Mobile removes the fixed filter/map columns and presents filter chips plus cards; a production implementation still needs a working map/list toggle and filter drawer.

### Project detail

- Gallery, identity, facts and contact appear before deep tools.
- 3D, unit table, media, facilities, map, costs and foreign-buyer layers read as one project mini-site.
- Mobile preserves the evidence order and uses poster/list alternatives; no WebGL is required for the review.
- Long English project names wrap; the current Rainbow title remains legible at 390px.

### Foreign investor

- Correct LTR behavior at both widths.
- Image-led discovery, English project cards, process, costs, 3D boundary and named follow-up form are visible.
- Currency/unit controls are framed as indicative display, not settlement promises.

### Developer Studio

- Desktop shows a credible WordPress-owned completion workflow and separates uploaded media from rights approval.
- Initial 390px run exposed a 485px scroll width from dense table/grid content. The review CSS was corrected by reflowing the top actions, forcing mobile amenity columns, wrapping field values and simplifying the unit table. The rerun is exactly 390px with no overflow.

## Truth/asset QA

- All project-like images are repository concept/prototype assets.
- Every HTML page has a global review notice.
- Project media carries a visible illustrative/prototype label.
- No exact price is presented; the standard wording is current price on request.
- Unit examples explicitly say they are not live inventory.
- 3D copy states that exact per-window selection requires official segmented geometry/unit IDs.

## Not proven by these screenshots

- Live WordPress rendering or content queries.
- Search, map, save, compare, form or Studio write behavior.
- Production performance/Core Web Vitals.
- Current public project facts, prices, availability or developer approval.
- Real media rights.
- Real HE/EN content parity.
- Exact 3D unit selection.

Those remain implementation and content-readiness gates after explicit owner approval.
