# Premium Concept Art Manifest

Branch: `codex/concept-art`

Scope: original SVG assets only. No `inc/*.php`, no plugin version bump, no routes, no stock photos, no raster generation, no people, no fake logos.

These assets replace the rejected real-photo fallback direction with an original branded architectural language: deep blueprint teal, ink/charcoal structure, champagne linework, coastal horizon, tower massing, and restrained drafting marks.

## Files

| File | Role | Intended replacement |
| --- | --- | --- |
| `assets/premium/concept/hero-coast-concept.svg` | Wide homepage hero concept, coastal skyline and sea horizon. | `--nl-real-hero` in `inc/premium-ui.php`; homepage `.nlh .nlh-hero`; archive `.nldir-hero`. |
| `assets/premium/concept/skyline-telaviv-line.svg` | 16:10 Tel Aviv-style skyline card/profile concept. | Project/profile hero fallback; `.nlpf-banner`; project cards where no owner media exists. |
| `assets/premium/concept/blueprint-texture.svg` | Tileable blueprint grid and drafting marks. | Overlay/background texture for `.nldc-media`, `.nldir-hero::before`, `.nlpf-banner::before`, `.nlst-bar`, `.nlst-dropzone`. |
| `assets/premium/concept/project-concept.svg` | Abstract residential tower massing. | `--nl-real-project` replacement; `nadlan_card_photo_url()` project fallback in `inc/directory.php`; `.nldc-media` project cards. |
| `assets/premium/concept/property-concept.svg` | Abstract floor-plan/interior motif. | `--nl-real-property` replacement; `nadlan_card_photo_url()` property fallback in `inc/directory.php`; property archive `.nlag-card > .nldc-media`. |
| `assets/premium/concept/contact-sheet.svg` | SVG-only review sheet showing the concept set together. | PR review aid only; not intended for runtime wiring. |

## Wiring Map For Claude

### `inc/premium-ui.php`

Replace the 1.42.2 real-photo variables with concept SVG variables:

| Current variable / surface | Concept asset |
| --- | --- |
| `--nl-real-hero` | `hero-coast-concept.svg` |
| `--nl-real-project` | `project-concept.svg` or `skyline-telaviv-line.svg` for a more skyline-led treatment |
| `--nl-real-property` | `property-concept.svg` |
| `--nl-real-professional` | `project-concept.svg` for architect/developer/project-adjacent professions, or `blueprint-texture.svg` plus existing monogram/profession mark for non-visual professional cards |
| `.nldir-hero` | `hero-coast-concept.svg` as the main background, with `blueprint-texture.svg` as a low-opacity overlay only if needed |
| `.nlh .nlh-hero` | `hero-coast-concept.svg` |
| `.nldc-media::before` | `blueprint-texture.svg` or keep CSS grid if lighter |
| `.nlpf-banner` | `skyline-telaviv-line.svg` for projects, `project-concept.svg` or `blueprint-texture.svg` for professional profiles |

### `inc/directory.php`

In the fallback branch of `nadlan_card_photo_url()` or its replacement, avoid stock/raster fallbacks:

| Post type / case | Concept asset |
| --- | --- |
| `nadlan_project` with no featured image / no legal `photos_csv` | `project-concept.svg`, alternating with `skyline-telaviv-line.svg` for visual variety |
| `nadlan_property` with no featured image / no legal `photos_csv` | `property-concept.svg` |
| `nadlan_professional` with no owner image | Prefer existing SVG profession marks / monogram. If a media background is required, use `blueprint-texture.svg` or `project-concept.svg` for architect/developer/contractor only. Do not show human stock faces. |

### Selectors Served

| Selector / variable | Asset |
| --- | --- |
| `.nldc-media` | `project-concept.svg`, `property-concept.svg`, `skyline-telaviv-line.svg` |
| `.nldir-results .nldc.has-media` | SVG concept card background through the image/fallback helper |
| `.nlag-card > .nldc-media` | `property-concept.svg` |
| `.nlpf-banner` | `skyline-telaviv-line.svg`, `project-concept.svg`, or `blueprint-texture.svg` by post type |
| `.nldir-hero` | `hero-coast-concept.svg` |
| `.nlh .nlh-hero` | `hero-coast-concept.svg` |
| `.nlac-card-media` | Same fallback map as directory cards; no human faces |
| `.nlst-bar`, `.nlst-dropzone` | `blueprint-texture.svg` or the relevant card concept when editing a specific project/property |

## Art Direction

- Original architectural concept art, not stock-photo copies.
- No identifiable people, no faces, no copied skylines, no fake developer logos.
- Deep blueprint teal field: `#071313`, `#0b1f1f`, `#113332`.
- Champagne/gold linework: `#d7c39a`, `#f4dfaa`.
- Strokes use round caps/joins and mostly 2-3.4px line weights at large viewBox sizes.
- The feeling should be an architect's presentation drawing for an Israeli coastal real-estate platform, not clip-art.

## QA Notes

- SVGs are standalone, hand-authored, and contain no external image references.
- `blueprint-texture.svg` is tileable at `240x240`.
- All assets include `<title>` and `<desc>`.
- Claude should run real browser QA after wiring at 390px and 1440px on `/`, `/projects/`, `/professionals/`, single project, single professional, `/studio/`, and `/advertiser-center/`.

## Needs Owner Art

No asset is blocked. Longer term, the owner may still commission a bespoke Nadlan brand illustration system with named Israeli landmark abstractions, but this set is ready for Claude to wire into 1.42.2 without stock photography.
