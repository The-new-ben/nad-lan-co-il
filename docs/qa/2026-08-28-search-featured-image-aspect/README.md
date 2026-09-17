# Search Results: keep project plates whole without touching other result types

Date: 2026-08-28 · Scope: Search Results, project cards only · Status: live, isolated branch, no merge

Final solution: the search template is untouched (byte-identical to the theme file) and a single
CSS rule scoped to `li.wp-block-post.type-nadlan_project` corrects project cards only.
A universal template override was tried first and deliberately reverted; see Solution history.

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

## Solution history

Three states. The middle one was applied, measured, and then deliberately reverted.

### 1. Before
`nadlan-platform-child//search`, `source: theme`, block attribute `{"isLink":true,"aspectRatio":"3/2"}`
with no `scale`, so the block defaults to `cover`. Plates lose 11.1% vertically. Legacy 16:9 loses
15.6% off the sides, legacy 3:2 fills exactly.

### 2. Intermediate, applied then reverted
The template was overridden with `aspectRatio 4/3 + scale contain` (override wp_id 7527).
Plates became whole, but the change applied to every result type: 16:9 article images gained a 25%
letterbox and 3:2 images an 11.1% letterbox. That tripped the agreed rollback trigger.

The override has been deleted. The live template is byte-identical to the theme file again:
`source: theme`, 4885 bytes, sha256 `bfbca079...0bce81f0`. Zero custom templates remain site wide.

### 3. Final, in place now
A narrow rule scoped by post type, added to the child theme's global styles (block-theme
Additional CSS, post id 4940, bound to `nadlan-platform-child`):

```css
body.search-results li.wp-block-post.type-nadlan_project .wp-block-post-featured-image img {
	aspect-ratio: 4 / 3 !important;
	object-fit: contain !important;
}
```

Three decisions behind that selector:

- **Post type, not filename.** `li.wp-block-post.type-nadlan_project` is WordPress's own stable
  card class, verified live on every project result.
- **`body.search-results`** keeps the rule strictly inside Search Results.
- **No figure rule, because it was measured and not assumed.** `.wp-block-post-featured-image`
  computes `aspect-ratio: auto`, `display: block`, `margin: 0`, `overflow: visible` and has no
  independent height, so its height follows the image. A wrapper rule would be dead weight.

`!important` is required because the query loop writes an inline style. Before saving anything, a
sentinel rule with the same selector was injected live: only the `type-nadlan_project` card changed
while two `type-page` cards kept their inline values, and the inline attribute stayed present. That
proves both the scoping and that the stylesheet beats the inline declaration.

The same rule is committed to `themes/nadlan-platform-child/assets/css/platform.css` on this branch
as its permanent home. When that file deploys, clear the global-styles copy so it is not defined twice.

| file | sha256 before | sha256 after |
|---|---|---|
| `themes/nadlan-platform-child/assets/css/platform.css` | `46a33219...e414f5b4` | `a378a2d5...8a0d33da` |

## QA

Screenshot capture in the operating Chrome window is non-functional (viewport 0x0, CDP clip error).
Evidence is live DOM and CSSOM receipts plus deterministic renders from the real image files.
See `before-intermediate-final.png`.

- **Five plates, single-project searches**: all compute `4 / 3` + `contain` while the inline style
  is back to `3/2 cover`. Exact fit, no bars, title and capsule row whole.
- **Mixed searches**: `H Infinity` returns one project card (4/3 contain, exact fit) beside two
  `type-page` cards at 1600x900 (3/2 cover, 15.6% side crop, original behaviour). `SIX-8` returns a
  project card beside a 1400x933 3:2 image that fills exactly with no crop and no bars.
  Worth noting: article results here are `type-page`, not only `type-post`. The rule ignores both.
- **General non-project search** (`משכנתא`, 14 results, 4 with images): every image is 1600x900 at
  `3 / 2 cover`, identical to the original state. No bars anywhere.
- **CLS**: 0.000 with zero shift entries on both the mixed search and the 14-result search.
- **Responsive**: 52 stylesheets scanned including every `@media` block; zero media-query rules
  touch object-fit, aspect-ratio, width, height or max-height on the image or figure. Desktop,
  tablet and mobile render identically by construction.
- **Console**: zero errors on search pages.
- **Distortion / overflow**: none. `contain` preserves the intrinsic ratio and cannot overflow.
- **Unchanged**: catalog `/projects/` still `.nldc-media` 4/3 contain with no inline style and zero
  `wp-block-post` cards; project pages have no featured-image block and their `og:image` is
  untouched; home and 404 have no project cards and no plate images.

## Known residual

Project cards whose featured image is not 4:3 now letterbox. Four UTOPIA language variants
(EN, FR, RU, AR) still carry `utopia-sde-dov-independent-concept-v1.webp` at 1536x1024 (3:2) and
show 11.1% cream bars where they previously filled exactly.

Option B trades bars on every 16:9 article result for bars on the few project cards that do not yet
have a 4:3 plate. The clean fix is giving those variants the series plate, which is queued work and
not a CSS matter.

Card alignment: in a mixed list, project cards are 4/3 and other cards 3/2, so image heights differ
by card type. The query loop is a single column list rather than a grid, so cards stack instead of
aligning side by side. This is inherent to option B.

## Rollback

```js
// CSS, restores the exact prior state (styles was an empty object)
await wp.apiFetch({path:'/wp/v2/global-styles/4940',method:'POST',data:{styles:{}}})
```
or Appearance > Editor > Styles > options > Additional CSS, clear the field.

The search template needs no rollback: it is already byte-identical to the theme file at repo HEAD
`623d5ba0eaebf5be8efbcce9a1fcb0d71c5c4ab1`, both source files copied verbatim into `receipts/`.

Triggers: the selector proves unstable, the CSS stops beating the inline style, or the mixed grid
is judged harmed.

## Not done, deliberately

- `og:image` still points at the full 1448x1086 plate. Social platforms crop to 1.91:1 or 2:1, which
  removes the title and the capsule row entirely. Dedicated 1200x630 OG images are the next step.
- No plates generated or uploaded, no existing image files modified, no other template touched, no
  broad CSS.
