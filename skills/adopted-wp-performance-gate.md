# Adopted WordPress Performance Gate Skill

> Prevents NadLan releases from making the public site slower through unnecessary assets, heavy queries, duplicate renderers, or uncached expensive work.

## When to use this

- Any frontend asset, Mapbox, model-viewer, listing query, REST endpoint, admin dashboard, or image-heavy page changes.
- Any change that adds scripts, styles, database queries, or API calls.

## Gate

1. Identify new assets and whether they load only on needed routes.
2. Confirm scripts/styles have cache-busting versions.
3. Avoid duplicate CSS stacks and duplicate JS initializers.
4. Check queries for:
   - unbounded post queries
   - meta queries without need
   - N+1 loops
   - expensive work during every page load
5. Lazy-load expensive visual assets when acceptable.
6. Use real browser timing and visual screenshots for UI changes.
7. Note any deferred performance debt explicitly.

## NadLan adaptation

3D, Mapbox, and investor media are revenue surfaces, but they must be route-scoped. Do not load showroom-only assets on normal articles, city pages, or directory screens.

## Source basis

- WordPress agent skills `wp-performance`: https://github.com/WordPress/agent-skills
- Jorge Rosal performance review skill: https://github.com/jorgerosal/wordpress-skills

## Revision log

- 2026-06-23 - Created by Codex from WordPress performance skill research.
