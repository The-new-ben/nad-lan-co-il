# Display Integration Solution

Date: 2026-06-28

## Bottom Line

The right solution is **not** to activate the rescue theme and **not** to install the bridge plugin as a second live plugin.

The right solution is to fold the good parts of the bridge and mockups into the existing `nadlan-config` showroom engine, because that engine already lives inside the real site, already knows the `nadlan_project` CMS fields, already handles `#nl-root`, and already avoids the old `nlv2` / `nlp3d` stacking problem.

## Why

The live site already has real SEO pages, calculators, guides, listings, professionals, lead handling, and project content. Replacing the theme would throw away too much. Installing a second showroom plugin would create duplicate shortcodes, duplicate renderers, and lead-endpoint drift.

The display should become part of the existing product system, not another layer on top of it.

## How The Display Gets Onto The Website

1. Keep the current site, current theme, and `nadlan-config` as the active product base.
2. Use the design bundle and bridge plugin as source material only.
3. Port the visual showroom layout into `plugins/nadlan-config/assets/showroom-engine/showroom.css`.
4. Port only safe interaction improvements into `plugins/nadlan-config/assets/showroom-engine/engine.js`.
5. Keep one renderer only: `#nl-root`.
6. Keep old renderers disabled/stripped: `.nlv2-showroom = 0`, `.nlp3d = 0` on engine pages.
7. Keep the existing shortcode name `[nadlan_showroom_engine]`; do not register it again in another plugin.
8. Keep the existing lead funnel `/wp-json/nadlan/v1/lead`; do not introduce a parallel public lead endpoint.
9. Add a homepage/project-gallery band through the existing engine or a uniquely named shortcode inside `nadlan-config`.
10. Release one surgical version at a time, with browser screenshots before deploy and after deploy.

## What Not To Do

- Do not activate `nadlan-rescue-showroom-theme.zip` on the live site.
- Do not activate `nadlan-content-showroom-bridge.zip` as a second live plugin.
- Do not replace the homepage.
- Do not rewrite `wp_posts.post_content` destructively.
- Do not add another renderer above or below the old one.
- Do not duplicate `[nadlan_showroom_engine]`.
- Do not show internal words to buyers: GLB, BIM, mesh, hotspot, token, Lovable, Codex, Featured, Sponsored.

## First Safe Release

The first implementation PR should be a small visual integration release:

- Use the existing `nadlan-config` engine.
- Make the Ashira display match the approved mockup more closely.
- Add/repair the article styling.
- Add the homepage project-gallery band only if it can render without replacing the current homepage.
- Prove with screenshots:
  - home desktop
  - home mobile
  - Ashira Hebrew desktop
  - Ashira Hebrew mobile
  - Ashira English desktop
  - Ashira English mobile

## Acceptance Gate

Before any deploy:

- `#nl-root = 1`
- `.nlv2-showroom = 0`
- `.nlp3d = 0` on pages using the new engine
- no duplicate shortcode registration
- no horizontal overflow at 1440 and 390
- language pages use their own URL and direction
- buyer copy does not leak internal implementation words
- ZIP has forward-slash paths only
- version surfaces match

After deploy:

- healthcheck reports the shipped version
- screenshots prove the public site matches the target closely enough
- one issue fixed per release before the next release starts

## Honest Status

The bridge plugin is useful as a reference. It is not safe to upload as-is.

The rescue theme is useful as a visual prototype. It is not the right production architecture.

The production path is a controlled integration into the existing `nadlan-config` engine.
