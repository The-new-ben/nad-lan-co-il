# Theme Fork Decision

> **Notice to all agents:** The repository root IS the `nadlan-revenue` WordPress theme. It is a **full fork** of Twenty Twenty-Five (WordPress core, GPL-2.0+), not a child theme. Read this before editing any theme file or proposing a theme change.

## What happened (2026-05-28)

The owner uploaded the actual Twenty Twenty-Five (`/wp-content/themes/twentytwentyfive/`) from the live UPress server. Claude Code (claude-opus-4-7) copied all of Twenty Twenty-Five's files into the repo root, bulk-renamed every identifier (`twentytwentyfive_` → `nadlan_revenue_`, `'twentytwentyfive'` → `'nadlan-revenue'`, package and slug references), then customized:

- `style.css` — theme header replaced with NadLan Revenue metadata.
- `theme.json` — color palette swapped for nad-lan brand (gold `#D89B3C`, trust blue `#0E3A8A`, cream `#FAF8F4`, positive green, negative red, etc.). Heebo added as first fontFamily for Hebrew. Body typography switched to `var:preset|font-family|heebo`, weight 400, line-height 1.65.
- `functions.php` — Twenty Twenty-Five setup retained (post formats, editor styles, stylesheet enqueue, checkmark list block style, pattern categories, format block binding) all renamed; **appended**: `nadlan_lead` CPT, lead-form admin-post handler with sanitization+nonce, and four WordPress 7.0 Abilities API registrations under `nadlan/*` (see `abilities-api.md`).
- All 98 pattern PHP files: text-domain swept clean.

## Why a fork and not a child theme

The owner specified: full ownership, simple mental model for the next agent, one folder = the whole theme. Child theme would inherit Twenty Twenty-Five updates automatically (a real advantage) but introduces parent/child confusion that the owner wanted to avoid for multi-agent coordination. Fork wins on simplicity; we lose upstream security fixes from Twenty Twenty-Five unless we periodically diff and merge.

**Maintenance protocol:** roughly every 3-6 months, an agent should `git diff` the current upstream Twenty Twenty-Five against our base fork (commit `[fork-point: T25 v1.5, 2026-05-25 upstream snapshot]`) and selectively cherry-pick fixes that don't conflict with our customizations.

## What's in the theme

```
/                              ← repo root = theme root
├── style.css                  ← NadLan Revenue theme header
├── style.min.css              ← T25 minified base CSS (kept as-is)
├── functions.php              ← T25 setup (renamed) + nad-lan additions
├── theme.json                 ← brand palette + Heebo typography + T25 structure
├── readme.txt                 ← theme readme (partially renamed; cosmetic)
├── screenshot.png             ← T25 screenshot (TODO: replace with nad-lan branded)
├── assets/                    ← T25 fonts (manrope, fira-code, ysabeau-office, vollkorn,
│                                 fira-sans, beiruti, platypi, roboto-slab, literata)
│                                 + editor-style.css + 36 webp pattern images
├── parts/                     ← block parts (header, footer, vertical-header,
│                                 sidebar, header-large-title, footer-columns,
│                                 footer-newsletter) — 7 .html files
├── patterns/                  ← 98 block patterns (book/podcast/portfolio/news themes;
│                                 most are unused for nad-lan but harmless)
├── styles/                    ← 32 style variation .json files (sections, blocks,
│                                 colors, typography)
├── templates/                 ← 8 block templates (index, page, single, archive,
│                                 home, 404, search, page-no-title)
├── package.json / package-lock.json / contributing.txt   ← T25 dev files,
│                                 harmless at runtime
├── AGENTS.md                  ← coordination contract (lives at theme root because
│                                 the whole repo is the theme — when UPress clones,
│                                 AGENTS.md lands inside /wp-content/themes/nadlan-revenue/)
├── README.md                  ← project readme
├── skills/                    ← shared brain (this file's family)
└── docs/                      ← research, SERP snapshots, future content backlog
```

## What is INTENTIONALLY not in functions.php

Documented to stop future agents from re-adding by accident:

- `register_nav_menus()` — block theme uses the block-based Navigation block. Classic nav menus would duplicate.
- Hand-rolled `WebSite` JSON-LD — Yoast SEO already outputs it. Two `WebSite` schemas on a page is a problem. See `yoast-config.md`.
- `wp_enqueue_style` for a separate "main.css" — block themes load styles via `theme.json` + WordPress core. The kept `nadlan_revenue_enqueue_styles` is enough.
- Theme support for `nav-menus`, `widgets` — unused in block themes.

## Patterns that we keep but don't use

Twenty Twenty-Five ships ~98 patterns aimed at book / podcast / event / portfolio / news sites. Most are irrelevant for nad-lan (`banner-about-book.php`, `event-rsvp.php`, `grid-videos.php`, `format-audio.php`, ...). They are harmless — they only render when explicitly inserted by an editor. Leaving them in keeps the fork clean and identical to upstream structure. We will ADD nad-lan-specific patterns later (lawyer-trust-strip, calculator-card, listing-card, lead-form, neighborhood-stat) as new files in `patterns/`.

## What still needs to happen

- [ ] **Owner: upload via UPress Git** (see `site-state.md` for the exact path).
- [ ] **Owner: activate `NadLan Revenue` in WP Admin → Appearance → Themes.**
- [ ] **Visual check**: homepage and 42 existing pages should render. Block content is theme-agnostic; expect the look to shift to our palette+Heebo, but structure intact.
- [ ] If anything breaks, switch back to Twenty Twenty-Five in WP Admin (still installed) — zero data loss.
- [ ] Next agent: add nad-lan-branded patterns under `patterns/` (lawyer-trust-strip, calculator-card, etc.). Each pattern file starts with the standard pattern header comment: `Title:`, `Slug: nadlan-revenue/<slug>`, `Categories:`.
- [ ] Next agent: replace `screenshot.png` with a 1200×900 brand-aligned image once we have one.
- [ ] Periodically: diff against upstream Twenty Twenty-Five and cherry-pick relevant fixes.

## Function naming convention going forward

- Public PHP functions in this theme: `nadlan_revenue_<thing>()`.
- Text domain in `__()`, `_e()`, `_x()`: `'nadlan-revenue'`.
- Pattern slugs: `nadlan-revenue/<slug>`.
- Pattern category slugs: `nadlan_revenue_<category>` (matches T25's underscore convention).
- Abilities API names: `nadlan/<ability>` (see `abilities-api.md`).
- Custom post types: prefix `nadlan_` (e.g. `nadlan_lead`, future `nadlan_property`).
- Action / filter hooks: prefix `nadlan_revenue_<hook>`.

---
_Created 2026-05-28 by Claude Code (claude-opus-4-7)._
