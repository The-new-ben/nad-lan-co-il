# Design Implementation — how the luxury system is wired into the theme

> **Notice to all agents:** the Lovable luxury design system (rounds 1+2) is **ported into the live theme** as of 2026-05-28. This skill is the operational map: where each artifact lives, how WordPress loads it, how to update it, and how to verify it after a sync. Read this before touching any theme styling, theme.json, or pattern.

## Source of truth → theme file mapping

| Design source | Lives in theme as | How WP loads it |
|---|---|---|
| `docs/design/lovable-output-round-2.md` §GAP4 CSS bundle | appended to `style.css` AND `style.min.css` behind marker `/* === NADLAN LUXURY DESIGN SYSTEM (Lovable round 1+2 port) === */` | theme enqueues `style.min.css` in production (`SCRIPT_DEBUG` off) via `nadlan_revenue_enqueue_styles()`; `style.css` only when SCRIPT_DEBUG on. The bundle is in BOTH so it loads either way. |
| §GAP5 theme.json fragment | merged into `theme.json` (`settings.color.palette`, `settings.typography.fontFamilies`+`fontSizes`, `settings.spacing.spacingSizes`, `settings.shadow`, `settings.layout`, `styles`) | WordPress auto-generates global-styles CSS from theme.json on every page — no enqueue needed. This is what makes the palette + fonts + element defaults apply site-wide and appear in the Block Editor. |
| §GAP6 patterns P1–P10 | `patterns/nadlan-*.php` (10 files) | WordPress auto-registers any `.php` in `patterns/` with a valid header. Slugs are `nadlan-revenue/<name>`. Insertable from the Block Editor inserter under their categories. |
| Fonts | `assets/fonts/frank-ruhl-libre/frl-{400,500,700,900}.woff2` + `assets/fonts/heebo/heebo-{300,400,500}.woff2` | Referenced two ways: (a) `@font-face` in the CSS bundle with absolute `/wp-content/themes/nadlan-revenue/...` URLs; (b) theme.json `fontFace` with theme-relative `file:./assets/fonts/...`. Both resolve to the same files. |

## Why the CSS is in both style.css and style.min.css

`functions.php` → `nadlan_revenue_enqueue_styles()` does:
```php
$suffix = SCRIPT_DEBUG ? '' : '.min';
wp_enqueue_style('nadlan-revenue-style', get_parent_theme_file_uri('style'.$suffix.'.css'), ...);
```
Production has `SCRIPT_DEBUG` off → loads `style.min.css`. So the bundle MUST be in `style.min.css` or it won't show. We put it in both (style.css for editor/debug parity, style.min.css for production). **When updating the bundle, update BOTH files** — or change the enqueue to always load one file.

> Future cleanup option: extract the bundle to `assets/css/luxury.css` and enqueue it explicitly. Deferred — the dual-file approach is robust and avoids depending on functions.php additions loading (which had gremlins; see `nadlan-config-plugin.md`).

## theme.json merge rules (do NOT blind-overwrite)

The fragment was **deep-merged** into the existing theme.json, preserving `templateParts` and `customTemplates` (which the block theme needs for header/footer/page templates). When you next update theme.json from a new Lovable round:
1. Load both JSONs.
2. Deep-merge fragment INTO base (fragment wins on leaf keys).
3. Re-apply `templateParts` + `customTemplates` from base.
4. Keep `version: 3` and the `$schema`.
5. Validate with `python3 -c "import json; json.load(open('theme.json'))"`.

There's a reusable merge snippet in the 2026-05-28 commit `25acbc4`.

## Pattern files

10 patterns, all php-lint clean, slugs `nadlan-revenue/*`:
- `nadlan-hero` — homepage hero (editorial, 4:5 image, text-link CTAs)
- `nadlan-tools-row` — 5 signature tools with gold serif ordinals 01–05
- `nadlan-trust-band` — cream strip, 4 stat tiles, gold vertical hairlines
- `nadlan-city-intelligence` — 2-col chart + city list
- `nadlan-guides-editorial` — asymmetric 1+2 magazine grid
- `nadlan-professionals-teaser` — 4 profile cards
- `nadlan-footer` — 4-col dark ink footer + gold rule
- `nadlan-article-section-opener` — 32px gold rule + H2
- `nadlan-pull-quote` — Frank Ruhl Libre 28px italic + gold side rule (RTL)
- `nadlan-faq-accordion` — FAQ rows

They reference categories (`nadlan-hero`, etc.) not yet registered — patterns still work (fall into the inserter uncategorized). **Optional improvement:** register pattern categories in `functions.php` via `register_block_pattern_category('nadlan-hero', [...])` so the inserter groups them. Deferred.

## How it goes live

These are theme files → **a theme sync is required**. The CSS, theme.json, fonts, and patterns ALL land together in one sync. Steps for the owner:
1. Merge the PR to `main` on GitHub (one click).
2. UPress → ניהול GIT → branch `main` → pull/clone to `/wp-content/themes/nadlan-revenue/`.
3. (No theme re-activation needed — same theme, updated files. WordPress regenerates global-styles CSS automatically.)

**Why not live via REST?** The CSS alone could be injected via global-styles, but it references fonts declared in theme.json `fontFace` and uses patterns — none of which exist live until the theme syncs. A CSS-only live injection would render a half-applied, font-broken state. One sync = the complete, correct result.

## Post-sync verification checklist (run after the owner syncs)

```
# 1. Fonts reachable (was 404 before sync)
curl -sI https://nad-lan.co.il/wp-content/themes/nadlan-revenue/assets/fonts/heebo/heebo-300.woff2 | head -1   # expect 200
# 2. CSS bundle present in the enqueued stylesheet
curl -s https://nad-lan.co.il/wp-content/themes/nadlan-revenue/style.min.css | grep -c "NADLAN LUXURY"          # expect >=1
# 3. Palette in generated global styles (homepage HTML)
curl -s https://nad-lan.co.il/ | grep -o "#1B1A17\|#9C7A3C\|FAF7F1" | sort -u                                   # expect the luxury hexes
# 4. Frank Ruhl Libre referenced in head
curl -s https://nad-lan.co.il/ | grep -c "Frank Ruhl Libre\|frank-ruhl-libre"                                   # expect >=1
# 5. Patterns registered
#    (REST) GET /wp-json/wp/v2/block-patterns/patterns  → look for slug "nadlan-revenue/hero"
```
Then a visual pass: homepage, a pillar page, a calculator page, mobile (360/768/1440). Record results in `site-state.md`. Target Lighthouse ≥90 desktop / ≥80 mobile.

## Known follow-ups after this lands

- **Calculator widgets** (`assets/widgets/*.html`) still use the OLD corporate-blue inline `<style>`. They render on the calculator pages PREPENDED to content. Retoken their inline styles to the new tokens (or convert them to use the new `.bracket-bar` / `.stack-bar` classes now in the bundle). Bump their `data-nlc` marker to `-v2`.
- **Footer template part** (`docs/wp-state/template-part-footer.html`, deployed as `custom` override) predates this system. Replace it with the `nadlan-footer` pattern OR retoken it. The pattern is the cleaner path.
- **Homepage** (id=2) is Codex's old Gutenberg content. To get the designed homepage, rebuild it from the `nadlan-hero` + `nadlan-tools-row` + `nadlan-trust-band` + `nadlan-city-intelligence` + `nadlan-guides-editorial` + `nadlan-professionals-teaser` + `nadlan-footer` patterns. This is a content edit (via REST or editor) — do it after the sync confirms the patterns + CSS are live.
- **Logo/favicon/OG**: the rejected cartoon-house (media 338/340) is still set. Regenerate to the monogram-seal spec (`design-logo-mark.md`) and swap.
- **Pages 42 existing**: their content keeps rendering; the new typography/palette applies automatically via theme.json + bundle. The hub-spoke related blocks and calculator widgets need retokenizing for full consistency.

## Update workflow (future design changes)

1. Edit the design in Lovable → get new CSS/theme.json/patterns.
2. Re-run the extraction (`/tmp/extract.py` pattern) → validate (brace balance, JSON valid, php -l).
3. Update `style.css` + `style.min.css` (replace content after the marker), merge theme.json, overwrite patterns.
4. Bump theme `Version:` in `style.css` header.
5. Commit, push, owner merges to main + syncs.
6. Run the post-sync verification checklist.

---
_Created 2026-05-28 by Claude Code (claude-opus-4-8). Port commit: 25acbc4. Source: docs/design/lovable-output-round-2.md._

