# NadLan Platform Child 0.1.4 Rollback

Scope: child-theme presentation slice only. No database content is rewritten.

## What This Release Changes

- Updates `themes/nadlan-platform-child`.
- Adds child header and footer template parts.
- Routes homepage, project archive, project single, and normal pages through the child chrome.
- Marks the existing homepage project showcase with `data-nlpo-home-projects` at render time only.
- Rebuilds `theme-dist/nadlan-platform-child-0.1.4.zip`.

## Rollback Steps

1. WordPress Admin -> Appearance -> Themes.
2. Activate the previous stable theme: `nadlan-revenue`.
3. Clear UPress/cache layers.
4. Hard-refresh `/`, `/projects/`, and one project page.
5. Confirm the public homepage returns to the previous chrome.

If keeping the child theme active but reverting this release:

1. Upload the previous `nadlan-platform-child` ZIP.
2. Clear UPress/cache layers.
3. Verify `/` and `/projects/`.

## Safety Notes

- No `wp_posts.post_content` rewrite is performed.
- No `nadlan-config` plugin module is edited.
- No calculators, professionals, billing, leads, or listings code is edited.
- The homepage project band marker is added by `the_content` filter only on the front page.
