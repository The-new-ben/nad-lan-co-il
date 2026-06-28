# NadLan Content Showroom Bridge

This is a WordPress plugin, not a theme. It is designed to preserve the existing NadLan site, theme, calculators, guides, professionals, listings, lead infrastructure and monetization surfaces while adding a premium project showroom layer.

## Install

1. WordPress Admin → Plugins → Add New → Upload Plugin.
2. Upload `nadlan-content-showroom-bridge.zip`.
3. Activate.
4. Open an existing `nadlan_project` page, for example `/projects/ashira-sde-dov/`.

## What it does automatically

- On single `nadlan_project` pages, it removes the legacy static `<main class="nlv2-showroom">...</main>` block at render time.
- It prepends one clean showroom to the project page and wraps the existing article body in styled SEO article classes.
- It does not delete or rewrite `wp_posts.post_content`.
- It emits sibling-page hreflang links using the current slug and the `-en`, `-fr`, `-ru`, `-ar` convention.
- It sets `lang` and `dir` for `nadlan_project` pages by slug suffix.
- It stores leads through `/wp-json/nadlan-bridge/v1/lead`; if a `nadlan_lead` CPT exists it uses it, otherwise it stores a private fallback post.

## Shortcodes

Use these anywhere in WordPress content:

```text
[nadlan_project_showroom project="ashira-sde-dov"]
[nadlan_showroom_engine project="ashira-sde-dov"]
[nadlan_listing_3d project="ashira-sde-dov"]
[nadlan_project_gallery]
[nadlan_home_project_gallery]
[nadlan_seo_booster project="ashira-sde-dov"]
```

## Live data mapping

The plugin reads common project meta fields if they exist:

- `project_model_glb`, `project_3d_model_glb`, `model_glb`, `_nadlan_model_glb`
- `project_model_poster`, `project_3d_model_poster`, `model_poster`, `_nadlan_model_poster`
- `project_3d_facade_image`, `project_facade_image`, `facade_image`
- `project_floors`, `project_3d_floors`, `floors`
- `project_3d_avg_price_per_sqm`, `avg_price_per_sqm`
- `project_3d_units`, `project_units`, `units_json`, `_nadlan_units`

If a project is missing fields, it falls back to bundled Ashira, Rainbow and Dimri sample data instead of rendering a broken empty widget.

## Safe switches for developers

```php
add_filter( 'nlcb_auto_single_project_showroom', '__return_false' );
add_filter( 'nlcb_auto_home_gallery', '__return_true' );
```

The homepage gallery is not auto-injected by default. Use `[nadlan_home_project_gallery]` in the existing homepage or enable the filter above in a controlled release.

## QA included

The `qa` zip contains Chromium screenshots for:

- desktop Hebrew project preview
- desktop English project preview
- mobile Hebrew project preview
- mobile English project preview
- desktop Hebrew project gallery preview

This QA is static sandbox QA, not live WordPress QA.
