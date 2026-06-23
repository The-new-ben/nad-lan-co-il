> **DEPRECATED 2026-05-28** (palette + typography only).** The bright `#D89B3C` gold and `#0E3A8A` trust blue here were the corporate-blue direction. The luxury system (warm ink/cream/antique-gold) is authoritative — see `docs/design/lovable-output-2026-05-28.md` and `skills/luxury-design-system.md`. The non-design content here (e.g., performance constraints) remains valid.

---

# Visual Design Skill

> **Notice to all agents:** any visual change to the theme, Elementor template, or front-end component must respect this skill. If a competing design instruction lands from anywhere else, raise it with the owner — don't silently override.

## Goal

Premium real-estate brand feel — closer to Rightmove / Zillow / OnTheMarket than to Yad2 (gray-blue, cluttered) or Madlan (purple-cyan, data-dashboard). Premium = generous whitespace, restrained color, real-data prominence, calm typography. Not "modern stack" gradients, not glassmorphism, not animated hero loops.

## Palette

| Token | Hex | Use |
|---|---|---|
| `--bg-base` | `#FFFFFF` | page background |
| `--bg-soft` | `#FAF8F4` | cards, calculator boxes, soft strip backgrounds |
| `--text-body` | `#0F1B2D` | body text (not pure black) |
| `--text-strong` | `#0E3A8A` | H1/H2, primary nav (trust blue) |
| `--accent` | `#D89B3C` | primary CTA, key highlight (warm gold; NOT green "sale" energy) |
| `--positive` | `#0E7C57` | price up indicator |
| `--negative` | `#B3261E` | price down indicator |
| `--border` | `#E3E6EC` | dividers, map lines, card borders |

CSS custom properties go in `style.css` `:root`. Use them, don't hardcode hexes in components.

## Typography

- Headings: **Heebo Bold (700)**. Fallback: `Rubik`, `system-ui`. Avoid Rubik as primary — too "startup".
- Body: **Heebo Regular (400)**, base 17px mobile / 18px desktop, line-height 1.65.
- Numbers in tables: **Heebo Tabular Numbers** (tnum CSS feature) for column alignment.
- Avoid **Assistant** (too "government"), **Frank Ruhl Libre** (serif clashes with this premium-but-pragmatic feel), and any decorative display fonts.

Headings scale (mobile → desktop):
- H1: 32 → 52px, 1.15 leading.
- H2: 26 → 36px.
- H3: 21 → 26px.
- H4: 18 → 20px.

## Spacing system

- Base unit: 4px. Allowed multiples: 4, 8, 12, 16, 24, 32, 48, 64, 80, 120.
- Section vertical padding: 64px mobile, 80-120px desktop.
- Card padding: 16-24px.
- Form field height: 48px mobile, 52px desktop.

## Components

### Listing card

- Image 4:3 at top.
- Bottom block, white background:
  - Price in `--text-strong`, 22px bold, e.g. `2,450,000 ₪`.
  - One row: rooms · floor · sqm (separated by middle dot or `|`).
  - Address, truncated to 1 line.
- Top-right corner badge if applicable: "חדש" / "ירידת מחיר" / "מקבלן".
- Radius 12px. Box-shadow: `0 1px 3px rgba(15,27,45,0.06)`.
- Hover: lift 2px, shadow `0 6px 16px rgba(15,27,45,0.10)`.
- No gradients. No glass effects.

### Calculator box

- Background `--bg-soft`.
- Large inputs (52px height), labels above.
- Sliders for ranges (years, %).
- Result: 36px bold in `--text-strong`.
- Below result, expandable "הסבר על החישוב". Buttons: "ייצא ל-PDF", "שלח לעצמי במייל" (if mail capture allowed).

### Map / data UI

- Map library: **MapLibre GL JS** with OSM tiles via **Stadia** or **MapTiler** (paid free-tier OK). Do NOT use Google Maps (heavy, brand-incompatible).
- Pins in `--accent` (gold). Selected pin in `--text-strong` (blue).
- Charts: **Recharts** or **ECharts**. Single line, light fill area at 10% opacity. No 3D. No spinning animations. Axis labels in tabular numerals.

### Header

- 72px tall, background `--bg-base`, bottom border 1px `--border`.
- Logo right (RTL), primary nav center, search trigger + login left.
- Sticky on scroll up; hidden on scroll down past 200px.

### Footer

- 4 columns: Categories / Cities / Tools / Company.
- Below: copyright, privacy, terms, accessibility statement.
- Background `--bg-soft`.

### Mobile menu

- Hamburger → full-screen drawer from the right (RTL).
- Search field at top.
- Accordion items, 56px tall each.
- Sticky bottom CTA after 300px scroll: "ייעוץ ראשוני בחינם" (golden, full width).

## What the design is NOT

- Not gradient backgrounds (purple → blue, etc.).
- Not glassmorphism / frosted blur.
- Not "neumorphism" soft shadows.
- Not full-bleed hero video.
- Not animated number counters that count up on scroll.
- Not "scroll-triggered hijacks" that disable native scrolling.
- Not dark mode. Real estate is a daylight-confidence product. Defer dark mode to year 2+.

## Performance constraints (these inform design)

- LCP target ≤ 2.5s mobile. → Hero image must be optimized (WebP, ≤ 200KB), preloaded with `<link rel="preload">`.
- CLS target ≤ 0.1. → All images need explicit `width`/`height` attributes. No web fonts swapping that shift layout (use `font-display: swap` only with a matched fallback metric).
- INP target ≤ 200ms. → Avoid heavy JS on tap. Lazy-load the calculator JS only when scrolled into view.

## What about Elementor?

The strategy doc allows Elementor with constraints. **Current recommendation: keep the custom code theme `nadlan-revenue` and avoid Elementor for money pages** (homepage, pillars, calculators). Use Elementor only for marketing-flexible pages (campaign landings, About) if at all. Elementor's bloat fights the Lighthouse targets.

## Open TODOs for next agent

- [ ] Codex: generate or import a Hebrew brand logo conforming to the palette. SVG + PNG (512, 256, 192, 32). Store in `assets/branding/`.
- [ ] Codex: produce a Figma-equivalent component list in `docs/research/design-tokens.md` for downstream UI work.
- [ ] Owner: pick one of two body fonts (Heebo or Ploni) — currently both are credible.

---
_Created 2026-05-28 by Claude Code (claude-opus-4-7)._
