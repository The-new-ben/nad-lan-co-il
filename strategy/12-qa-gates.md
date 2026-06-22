# QA Gates

Purpose: define what "done" means for strategy, SEO, visual, showroom, and release work.

## Universal Gate

Every PR:
- `git status` clean except intended files.
- `git diff --check`.
- no secrets or local junk.
- scope matches branch purpose.
- deploy path declared: PLUGIN, THEME, CONTENT, NONE.

## Visual Gate

Required screenshots:
- desktop 1440 width.
- tablet 768 width.
- mobile 390 width.
- Edge/mobile UA if the bug is mobile-browser-specific.

Checks:
- no horizontal overflow.
- no overlapping important elements.
- headings above their paragraphs, not sideways/offset.
- CTAs readable and reachable.
- no public internal copy.
- floating buttons do not stack.

## Showroom Gate

Checks:
- asset state: official/concept/missing visible.
- no fake facade.
- no silent fallback.
- GLB/model errors visible.
- facade/picker contained on mobile.
- selected unit card dismissible.
- click/tap at least 3 units.
- Mapbox/view/tour buttons work or show missing state.
- lead payload includes project/unit.

## SEO Gate

Checks:
- one H1.
- title/meta unique.
- canonical correct.
- primary keyword matches registry.
- content answers search intent.
- numeric claims have source/date.
- legal/tax pages marked reviewed.
- schema only when visible content supports it.

## Public Trust Gate

Checks:
- no Woo cart/checkout/notices on non-commerce pages.
- no debug/class/code leakage.
- no unfinished placeholder copy.
- no "More posts" pattern on premium pages.
- no fake inventory or fake urgency.

## Release Gate

Plugin:
- version surfaces aligned.
- PHP lint.
- JS syntax.
- ZIP built by canonical builder.
- 0 backslash ZIP paths.
- healthcheck after deploy.

Theme:
- server Git pull required after merge.
- cache clear.
- live screenshot after pull.

Content:
- page preview.
- no escaped HTML.
- Yoast/title/meta/schema checks.

## Proof Locations

- Screenshots: `docs/qa/screenshots/<run>/`
- Healthcheck: `docs/qa/healthcheck-<version>-live.json`
- QA reports: `docs/qa/<date>-<topic>.md`
- Strategy decisions: `strategy/`

## External Tools To Use

- Chrome DevTools device toolbar.
- Playwright screenshots.
- Lighthouse/PageSpeed Insights for performance snapshots.
- Rich Results Test / Schema validator when schema changes.
- Search Console/GSC when available.
- Semrush/Ahrefs/Screaming Frog only when data is exported and source-labeled.

Do not claim external-tool verification unless the output or screenshot is committed or summarized with date/tool/query.
