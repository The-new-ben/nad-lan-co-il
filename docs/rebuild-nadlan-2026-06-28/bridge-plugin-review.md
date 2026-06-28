# NadLan Content Showroom Bridge Review

Date: 2026-06-28

Reviewed files:

- `bridge-plugin-review/nadlan-content-showroom-bridge.zip`
- `bridge-plugin-review/nadlan-content-showroom-bridge-qa.zip`
- extracted plugin under `bridge-plugin-review/plugin/nadlan-content-showroom-bridge/`
- extracted QA screenshots under `bridge-plugin-review/qa/qa/`

## Bottom Line

The plugin-bridge direction is better than the standalone rescue theme direction because it does not
replace the whole site. It tries to preserve the existing homepage, guides, calculators, listings,
professionals and project content, while adding a showroom layer.

However, it should not be installed live as a separate plugin beside `nadlan-config` without fixes.
The current repo already contains a CMS-wired showroom engine in
`plugins/nadlan-config/inc/showroom-engine.php`, and the bridge overlaps with it.

Best use: treat this bridge as a source of UI/CSS/shortcode ideas to merge surgically into
`nadlan-config`, not as a second live showroom plugin.

## Checks Run Locally

Passed:

- PHP lint on `nadlan-content-showroom-bridge.php`
- `node --check` on `assets/bridge.js`
- ZIP path scan: no Windows backslash-path poison found
- extracted QA screenshots are present
- static browser QA regenerated under `bridge-plugin-review/local-qa/`

Independent static browser QA found:

- `.nlv2-showroom = 0`
- `.nlp3d = 0`
- no horizontal overflow at 1440 or 390
- one H1 on project previews
- clicking a unit updates the hidden `unit` field to `ashira-10-corner`
- no JavaScript page errors in the static previews

## Critical Issues Before Live

### 1. Shortcode collision

The bridge registers:

- `[nadlan_showroom_engine]`
- `[nadlan_project_showroom]`
- `[nadlan_listing_3d]`
- `[nadlan_project_gallery]`
- `[nadlan_home_project_gallery]`
- `[nadlan_seo_booster]`

But the existing `nadlan-config` plugin already registers `[nadlan_showroom_engine]`.

If both plugins are active, whichever plugin loads last may own that shortcode. This is not
deterministic enough for production.

Fix: do not install this as a separate active plugin with the same shortcode names. Either rename
the bridge shortcode namespace or fold the useful parts into `nadlan-config`.

### 2. Duplicate showroom risk

The bridge auto-prepends its showroom on all singular `nadlan_project` pages by default:

`apply_filters( 'nlcb_auto_single_project_showroom', true )`

The current `nadlan-config/inc/showroom-engine.php` already auto-renders the current engine for
active project pages, disables the old `nlp3d` module, and strips legacy `.nlv2-showroom` content.

If both are active, the page can render two showroom systems.

Fix: bridge auto-render must default off, or it must explicitly detect the existing `nadlan-config`
engine and step aside.

### 3. model-viewer module loading

The bridge uses:

`wp_script_add_data( 'nlcb-model-viewer', 'type', 'module' );`

Earlier production failures showed this is not safe enough. The active theme already has a
`script_loader_tag` filter for `nadlan-model-viewer`, but not for the bridge handle
`nlcb-model-viewer`.

Fix: add a `script_loader_tag` filter for `nlcb-model-viewer`, or reuse the existing
`nadlan-model-viewer` handle.

### 4. Existing lead funnel is not fully reused

The bridge posts to `/wp-json/nadlan-bridge/v1/lead` and writes a `nadlan_lead` post if the CPT
exists. That is not the same as using the existing `/nadlan/v1/lead` endpoint and its delivery,
qualification and nurture seams.

Fix: route through the existing NadLan lead endpoint or fire the same established actions/filters
used by the current lead pipeline.

### 5. Public wording leak

Independent static QA found the English page visibly includes the word `lead` in article copy:

`so a general lead becomes a focused enquiry`

Public buyer pages should not use internal business words.

Fix: replace with buyer-facing wording, for example:

`so a general question becomes a focused apartment enquiry`

### 6. Static QA is not live WordPress QA

The package QA is useful but it was run against static previews. It does not prove behavior inside
the real WordPress site with `nadlan-config`, the active theme, real project posts, Yoast, existing
content filters and the current lead endpoint.

Fix: test on staging or a local WordPress copy with both the active theme and `nadlan-config`.

## What To Save From This Bridge

Good pieces:

- plugin-bridge direction, not replacement theme,
- non-destructive render-time de-stack idea,
- project/home shortcodes,
- simple project gallery shortcode,
- article wrapper styling concept,
- static QA discipline,
- no backslash ZIP poison,
- buyer-oriented visual layout in the screenshots.

Do not copy blindly:

- duplicate shortcode name,
- separate lead endpoint,
- auto-showroom default on,
- `nlcb-model-viewer` enqueue without module tag filter,
- hardcoded fallback comps/prices as if they were real,
- English public word `lead`.

## Recommendation

Do not upload this plugin live as-is.

Next safest implementation step:

1. Keep the ZIP and QA as evidence.
2. Open one surgical branch against `nadlan-config`.
3. Port only the useful bridge improvements into the existing CMS-wired showroom engine.
4. Do not create a second active showroom plugin.
5. Gate on real WordPress/staging:
   - one showroom renderer,
   - no `.nlv2-showroom`,
   - no `.nlp3d`,
   - one model-viewer script with `type="module"`,
   - no public internal words,
   - unit click updates existing lead payload,
   - Hebrew and English screenshots at desktop and mobile.

