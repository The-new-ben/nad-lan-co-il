# Repo Knowledge Map

This map lists the existing knowledge that should guide the rebuild.

## Primary Source Of Truth

`handoff/claude-design/2026-06-28-nadlan-master-spec.md`

Use for:

- anti-stacking rules,
- language/hreflang architecture,
- showroom engine acceptance gates,
- project page section order,
- price/comps honesty rules,
- browser screenshot QA requirements.

Important correction for the rebuild: the spec says not to rebuild the working homepage blindly.
The owner has now decided to rebuild the theme/design line. That does not mean deleting safety. The
safe interpretation is: create a new theme/design system side by side, keep the current theme as a
backup, and switch only after QA.

## Visual Design Direction

`handoff/lovable/2026-06-24-premium-pattern/`

Use for:

- cream editorial luxury direction,
- typography and spacing,
- the showroom reference HTML/CSS,
- mobile/desktop screenshot target,
- WordPress implementation map.

Keep:

- NADLAN name,
- quiet premium real-estate tone,
- cream/ink/gold/terracotta palette family,
- large editorial type,
- restrained cards and strong information hierarchy.

Avoid:

- dark dashboard as the whole site language,
- random AI-looking hero images,
- technical labels on buyer pages,
- adding more CSS layers over the old output.

## Growth And SEO Strategy

`strategy/lovable/2026-06-21-report-0-strategy-intake.md`
`strategy/lovable/2026-06-21-report-1-public-trust-technical-seo.md`
`strategy/lovable/2026-06-21-report-2-keyword-master-universe.md`

Use for:

- NADLAN as a premium Israeli real-estate authority,
- hubs over random posts,
- Hebrew first, English/international investor layer second,
- city/area/project/urban-renewal/professional/calculator hubs,
- sourced, dated, authored YMYL content.

The rebuild must support content depth: project pages and hubs should be rich enough to compete,
not thin showroom pages.

## Showroom Product Rules

`skills/project-page-premium-showroom-runbook.md`
`handoff/shared-knowledge/skills/nadlan-showroom-design-rules.md`
`skills/lovable-competitor-blueprint-2026-06.md`

Use for:

- 3D model plus facade selector architecture,
- apartment cells instead of meaningless dots,
- price estimate labels,
- view/map/media/tour panels,
- CMS fields for contractor-supplied assets,
- mobile no-overflow gate,
- one project equals one data file plus one model/facade/media package.

Product truth:

- If the GLB is not apartment-level BIM, the GLB is a rotating context model.
- Apartment selection should happen through a static facade/elevation selector or unit-cell layer.
- A true click-any-apartment-on-a-spinning-building experience requires real per-unit geometry or
  segmented BIM/GLB data. The rebuild should preserve that upgrade path without pretending it
  already exists.

## Current Code Boundaries

Theme/root files:

- `theme.json`
- `style.css`
- `functions.php`
- `templates/`
- `parts/`
- `patterns/`

Plugin/showroom:

- `plugins/nadlan-config/inc/showroom-engine.php`
- `plugins/nadlan-config/assets/showroom-engine/engine.js`
- `plugins/nadlan-config/assets/showroom-engine/showroom.css`
- `plugins/nadlan-config/assets/showroom-engine/editorial.css`
- `plugins/nadlan-config/assets/showroom-engine/tokens.css`
- `plugins/nadlan-config/assets/showroom-engine/models/`

The next build should separate responsibilities:

- Theme owns site chrome, layout, editorial templates, homepage, archive pages, typography,
  spacing, heading alignment and public presentation.
- Plugin owns CPTs, data contracts, REST endpoints, healthcheck, lead capture, showroom payloads,
  model-viewer loading, and importer/validator logic.

## External Research Anchors

- Google Search Central localized versions/hreflang:
  https://developers.google.com/search/docs/specialty/international/localized-versions
- Google Search Central multilingual and multi-regional sites:
  https://developers.google.com/search/docs/specialty/international/managing-multi-regional-sites
- WordPress Theme Handbook for `theme.json`:
  https://developer.wordpress.org/themes/global-settings-and-styles/
- WordPress Block Themes overview:
  https://developer.wordpress.org/block-editor/how-to-guides/themes/
- model-viewer hotspot annotations:
  https://modelviewer.dev/examples/annotations
- Matterport on Homes.com:
  https://www.homes.com/solutions/matterport

These sources support the rebuild decisions: separate crawlable language URLs, theme-level global
styles, model hotspots when real 3D geometry supports them, and buyer-facing virtual tour/floor-plan
experiences as the product benchmark.
