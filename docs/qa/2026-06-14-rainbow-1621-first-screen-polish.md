# Rainbow 1.62.1 First-Screen Showroom Polish QA

Branch: `codex/rainbow-showroom-1621-polish`

## Why This Patch Exists

Live `1.62.0` installed correctly, but visual QA showed the page still did not read as a premium
product showroom:

- A theme `wp-block-post-featured-image` render dominated the first viewport before the 3D module.
- The interactive model existed, but the buyer reached it only after the page felt like a normal
  WordPress article.
- The fixed WhatsApp / AI / accessibility stack sat over the showroom side of the page and competed
  with 3D controls.
- Article headings and body blocks needed a scoped layout guard so headings sit above their text
  instead of feeling pushed aside.
- The model rotation was still clamped to a narrow angle range, so drag could not feel like a real
  product spinner.

## Live Evidence Before Patch

Healthcheck after owner update:

```json
{
  "version": "1.62.0",
  "project_3d": {
    "renderer": "premium_showroom_v7_product_stage",
    "showroom_v2": true,
    "cms_material_fields": true,
    "cms_material_cards": true,
    "hit_targets": true,
    "model_zoom_tilt": true
  }
}
```

Browser DOM geometry at desktop width:

- `.wp-block-post-featured-image` was present above the module.
- `.nlp3d` existed and rendered, but started below the first viewport.
- No horizontal overflow was present on desktop.
- Stage card was hidden by default, which is correct.
- Map was user-open only, which is correct.
- Fixed `.nlfab`, `#nlai`, and `#nla-btn` were visible over the right side of the page.

## Patch Scope

- Hide the theme featured image on 3D project pages where the `nadlan-p3d` stylesheet is loaded.
- Force `.nlp3d-premium` into a stage-first grid: stage, short copy, console.
- Raise the stage height so the building is the first serious product surface.
- Move floating contact/accessibility widgets to the opposite corner on project showroom pages.
- Add scoped project article typography guards for bare `h2`, `h3`, paragraphs, lists and tables.
- Replace the `-68..68` degree rotation clamp with normalized full-circle `0..360` rotation.
- Add drag-release momentum for a more product-like spinner feel.
- Bump renderer marker to `premium_showroom_v8_first_screen`.

## Post-Install Gate

After merge, uPress/server Git sync, plugin update/upload and hard refresh:

```bash
curl -s "https://nad-lan.co.il/wp-json/nadlan/v1/healthcheck" | jq '.version,.project_3d'
```

Expected:

- `version = 1.62.1`
- `project_3d.renderer = premium_showroom_v8_first_screen`
- `project_3d.showroom_first_view = true`
- `project_3d.static_featured_image_suppressed = true`
- `project_3d.floating_actions_clear = true`
- `project_3d.model_full_360 = true`

Manual browser checks:

- 1440px: the first serious visual after the page title is the dark showroom stage, not the static
  featured image.
- 1440px: fixed action buttons do not overlap the 3D toolbar or selected-unit card.
- 1440px: dragging horizontally spins the model through a full circle, not a short side-to-side
  wiggle.
- 390px: no horizontal overflow, no text cut-off, and the floating stack stays away from the
  primary stage controls.
- Long article: headings are above their related text with a readable measure.

## Honest Boundary

This patch improves presentation and interaction of the existing showroom. It does not claim to
deliver official Rainbow BIM, official floorplans, real developer availability, or a binding
purchase flow. Those remain data/product workstreams that require owner/developer source material.
