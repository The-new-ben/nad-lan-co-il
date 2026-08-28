# Search Results featured image: 3/2 cover -> 4/3 contain

Date: 2026-08-28 · Scope: `nadlan-platform-child//search` only · Status: applied to production, isolated branch, no merge

## Problem

Five project plates (1448x1086, 4:3) were being clipped on the site search surface.
The Post Featured Image block inside the search Query Loop emitted:

```
style="aspect-ratio:3/2;width:100%;object-fit:cover;"
```

Container 1.5 against image 1.3333 gives an 11.1% vertical crop, split evenly, i.e. 60 px
off the top and 60 px off the bottom of the 1086 px file.

Measured loss per plate (pixel analysis of the actual files):

| plate | title rows | title lost | capsule rows | capsules lost |
|---|---|---|---|---|
| aurelia | 41-67 | 19 px, 70% | 997-1085 | 60 px, 67% |
| einstein-tower | 42-70 | 18 px, 62% | 956-1051 | 26 px, 27% |
| h-infinity-somail-tel-aviv | 44-72 | 16 px, 55% | 955-1085 | 60 px, 46% |
| six-8-herbert-samuel-tel-aviv | 40-65 | 20 px, 77% | 955-1085 | 60 px, 46% |
| utopia-sde-dov | 44-73 | 16 px, 53% | 955-1085 | 60 px, 46% |

The projects catalog `/projects/` was never affected: it is a separate custom template
(`.nldc-media`, aspect-ratio 4/3, object-fit contain) and showed 0% crop throughout.

## Root cause

`patterns/template-query-loop.php` line 20 in the parent theme *NadLan Revenue*:

```php
<!-- wp:post-featured-image {"isLink":true,"aspectRatio":"3/2"} /-->
```

No `scale` attribute means the block defaults to `cover`. That pattern is shared by
`templates/index.html`, `templates/search.html` and `templates/archive.html`, so editing the
file would have changed all three. Editing through the Site Editor instead creates a database
override of the search template alone, which is why the fix is scoped.

## Change applied

One block attribute set, in one template:

```
- <!-- wp:post-featured-image {"isLink":true,"aspectRatio":"3/2"} /-->
+ <!-- wp:post-featured-image {"isLink":true,"aspectRatio":"4/3","scale":"contain"} /-->
```

| | before | after |
|---|---|---|
| template source | `theme` | `custom` (wp_id 7527) |
| content length | 4885 | 4903 |
| sha256 | `bfbca079...0bce81f0` | `ce1eda4f...b2628d1f` |
| rendered inline style | `aspect-ratio:3/2;width:100%;object-fit:cover;` | `aspect-ratio:4/3;width:100%;object-fit:contain;` |

A guard asserted exactly one occurrence of the old block string before writing. Observed: 1.

## Scope verification

After the change the entire site has exactly one custom template: `nadlan-platform-child//search`.

| template | source | aspectRatio | touched |
|---|---|---|---|
| search | custom | 4/3 + contain | yes |
| archive | theme | 3/2 | no |
| index | theme | 3/2 | no |
| single | theme | 3/2 | no |
| home, 404 | theme | no featured-image block | no |
| `/projects/` catalog | custom `nldc` template | 4/3 contain already | no |
| project pages | child theme `single-nadlan_project.html` | no featured-image block | no |

## QA

Screenshot capture in the operating Chrome window is broken (viewport reports 0x0, CDP clip
error), so visual proof is a deterministic render built from the real image files plus live
DOM and CSSOM receipts. See `before-after-plate-card.png` and `before-after-legacy-16x9.png`.

- All five plates on `/?s=`: `object-fit: contain`, `aspect-ratio: 4/3`, zero bars, title and
  capsule row complete.
- CLS: 0.000 with zero layout-shift entries on both a single-result search and a 14-result
  general search. The block emits `width=1448 height=1086` plus an inline aspect-ratio, so the
  box is reserved before load. Threshold 0.1, pass.
- Mobile and tablet: all 49 stylesheets were scanned including every `@media` block for rules
  matching the image or its figure that set object-fit, aspect-ratio, width, height or
  max-height. Media-query hits: 0. The ratio is therefore viewport independent and mobile
  renders exactly as desktop.
- Distortion: none. `contain` preserves the intrinsic ratio, and for the plates the box ratio
  equals the image ratio, so they render undistorted and unscaled in ratio terms.
- Overflow: `contain` cannot overflow its box by definition; the image is `width:100%` inside a
  constrained group. No horizontal overflow introduced.
- Grid uniformity: one block serves every card, so all image boxes are 4/3 on every device.
- Alt text: the block renders the post title as alt, e.g. `Aurelia Sde Dov - אורליה שדה דב`.
  That is pre-existing behaviour, descriptive, and unchanged by this edit.
- Letterbox background: figure and img backgrounds are transparent; the nearest painted
  ancestor is `rgb(250,247,241)` on `.wp-site-blocks`, the site's warm cream. Bars therefore
  land on paper tone that matches the plates. Verifier condition 2 is met with no CSS change.

## Known cost, non-plate results

| native | ratio | before (3/2 cover) | after (4/3 contain) |
|---|---|---|---|
| 1600x900 | 16:9 | 15.6% cropped off the sides | 25.0% cream bars, nothing lost |
| 1672x941 | 16:9 | 15.5% cropped off the sides | 25.0% cream bars |
| 1536x1024 | 3:2 | perfect fill, 0% crop | 11.1% cream bars |
| 1400x933 | 3:2 | perfect fill, 0% crop | 11.1% cream bars |

No legacy content is lost, but 3:2 photos move from edge to edge to an 11.1% letterbox and
16:9 photos to a 25% letterbox. This is the trade the authorised setting makes.

If that reads as material harm, the one-attribute alternative is `"scale":"cover"` with
`"aspectRatio":"4/3"`. For the plates it is identical (box ratio equals image ratio, so cover
and contain both crop nothing), and legacy photos stay edge to edge with a side crop instead of
bars. That variant is not applied; it is offered.

## Rollback

Delete the override; WordPress falls back to the theme file.

- UI: Appearance > Editor > Templates > Search Results > options > Reset / Clear customizations
- API, from any wp-admin console:
  ```js
  await wp.apiFetch({path:'/wp/v2/templates/'+encodeURIComponent('nadlan-platform-child//search'),method:'DELETE',data:{force:true}})
  ```
- Verify: GET the template and confirm `source === 'theme'` and the content contains
  `"aspectRatio":"3/2"` with no `"scale"`.
- Restores to `templates/search.html` + `patterns/template-query-loop.php` at repo HEAD
  `623d5ba0eaebf5be8efbcce9a1fcb0d71c5c4ab1`, both copied verbatim into `receipts/`.

Rollback triggers to watch: cards become non-uniform, CLS rises above 0.1, or legacy 16:9
results are judged materially harmed.

## Not done, deliberately

- `og:image` still points at the full 1448x1086 plate. Social platforms crop to 1.91:1 or 2:1,
  which removes the title and the capsule row entirely. Dedicated 1200x630 OG images are the
  agreed next step and were explicitly out of scope here.
- No plates generated or uploaded, no existing image files modified, no CSS added, no other
  template touched.
