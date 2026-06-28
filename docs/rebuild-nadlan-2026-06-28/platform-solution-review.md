# Platform Solution Review

Date: 2026-06-28

## Verdict

This package is a better direction than the previous rescue theme and bridge plugin.

The correct production architecture is:

1. Keep `nadlan-revenue` as the parent theme.
2. Use a child theme for presentation only.
3. Keep `nadlan-config` as the business/source-of-truth plugin.
4. Use the orchestrator plugin only as a glue layer that delegates to `nadlan-config`.
5. Do not register `nadlan_showroom_engine` again.
6. Do not create a second project/showroom renderer.

## What Was Reviewed

Copied and extracted into this folder:

- `nadlan-platform-orchestrator-plugin.zip`
- `nadlan-platform-child-theme.zip`
- `nadlan-complete-platform-solution.zip`

## Checks Run

- ZIP path scan: clean, no Windows backslash-path entries.
- ZIP integrity: clean for all three ZIP files.
- PHP lint: clean for 14 PHP files.
- JavaScript syntax: clean for 2 JS files.
- `theme.json`: valid JSON.
- Shortcode collision check: the package does **not** register `nadlan_showroom_engine`.
- The orchestrator delegates to `nadlan_showroom_engine_shortcode()` when available.
- Homepage auto insertion option defaults off in the plugin.

## Good Parts To Keep

- Child-theme direction is safer than replacing the parent theme.
- Orchestrator plugin does not duplicate `nadlan_showroom_engine`.
- Orchestrator uses unique shortcodes:
  - `[nadlan_platform_home_projects]`
  - `[nadlan_platform_project_catalog]`
  - `[nadlan_platform_showroom]`
  - `[nadlan_platform_interior]`
- REST endpoint is admin-only with `current_user_can( 'manage_options' )`.
- Admin setting save uses `check_admin_referer`.
- Homepage band can be controlled by option in the plugin.
- Interior-tour slot is useful and should connect later to approved tour/media fields.

## Issues Before Live

### 1. Public Copy Leak

The project catalog default subtitle says that content and leads remain in the existing system.

That is internal language. Buyers should never see "leads", "system", "CMS", "orchestrator", or similar implementation words.

Fix before live: rewrite this as buyer-facing copy.

### 2. Child Theme Homepage Inserts Band Automatically

The child theme `templates/home.html` includes:

`[nadlan_platform_home_projects limit="6"]`

That means activating the child theme changes the homepage immediately, even if the plugin option is off.

This is not automatically wrong, but it must be screenshot-gated. Safer production behavior is either:

- keep the child theme presentation-only and insert the band manually in the homepage content, or
- keep the template insertion but activate only on staging first and compare full-page screenshots.

### 3. Content Is Starter Depth, Not Final SEO Depth

The Ashira language drafts are useful starters but not final project pages:

- Hebrew: about 419 words
- English: about 496 words
- French: about 492 words
- Russian: about 360 words
- Arabic: about 350 words

That does not meet the 2,000-3,000 word competitive project-page target.

Use these drafts as structure, not as finished investor-grade pages.

### 4. Not Live-Verified

The package has not been tested inside the real WordPress stack with the active `nadlan-revenue` parent, active `nadlan-config`, Yoast, cache, and live project data.

It must go through staging/preview Chrome QA before production.

## Recommended Path

### Release A: Safe Platform Shell

Install on staging only:

1. Existing `nadlan-config` stays active.
2. Upload orchestrator plugin.
3. Keep homepage auto band off.
4. Upload child theme.
5. Activate child theme only after confirming `nadlan-revenue` exists.
6. Screenshot:
   - homepage desktop/mobile
   - `/projects/` desktop/mobile
   - Ashira HE desktop/mobile
   - Ashira EN desktop/mobile
   - one calculator
   - one professional page
   - one guide page
7. Confirm no duplicate render:
   - `#nl-root = 1`
   - `.nlv2-showroom = 0`
   - no second showroom under the first

### Release B: Copy Cleanup

Before any live activation:

- remove internal wording from public subtitle
- make the homepage band placement either manual or explicitly gated
- confirm no hidden duplicate project band

### Release C: Ashira Content Completion

Expand each language page from starter draft to full buyer/investor content after SERP research.

Do not publish these drafts as "final SEO" in their current length.

## Honest Recommendation

This package is worth keeping and pushing into the repo as a candidate platform layer.

It is not ready for blind live activation.

The safest way to get this display onto the website is to test the child theme plus orchestrator on staging, fix the public-copy leak, prove no stacking with screenshots, and then deploy one controlled release.
