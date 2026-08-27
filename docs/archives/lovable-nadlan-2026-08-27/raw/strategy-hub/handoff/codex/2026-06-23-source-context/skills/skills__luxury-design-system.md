# Luxury Design System — Master skill

> **Notice to all agents:** This is the **canonical visual system** for nad-lan.co.il. It is derived from Lovable's design output (`docs/design/lovable-output-2026-05-28.md`), which is the **source of truth**. This skill summarises rules and operational decisions; when in doubt, open the source doc. This file **supersedes** the earlier `visual-design-skill.md` palette/type AND the provisional `luxury-design-language.md`. They are deprecated.

## Read order for a designer/dev agent

1. This file (master rules + tokens)
2. `docs/design/lovable-output-2026-05-28.md` (the full design system from Lovable: competitor DNA, all tokens, all screens, all components, honesty statement)
3. `skills/design-page-patterns.md` (how each page type is built)
4. `skills/design-components.md` (every component, every state)
5. `skills/design-micro-interactions.md` (motion matrix)
6. `skills/design-logo-mark.md` (logo lockups)
7. `skills/design-rtl-hebrew.md` (RTL-specific rules pulled out for emphasis)

## What this system IS

A calm, serif-led, warm-cream RTL Hebrew platform where tools and knowledge are presented with the dignity of a **private bank's research desk** — never as a marketplace, never as a SaaS dashboard, never as a listings board. Synthesis of Sotheby's typographic restraint, Christie's Parisian silence + warm cream palette, The Agency's confidence to leave a hero alone, Compass's utility-as-hero clarity, Luxury Presence's asymmetric editorial grid for guides.

## Hard rules — never break these

1. **Two neutrals + one accent.** Two neutrals are cream + ink; the single accent is muted antique gold. Never two saturated colors on one surface. Never bright colors.
2. **Gold is for ≤5% of any screen.** Never two saturated colors on the same surface.
3. **Serif headings (Frank Ruhl Libre) + light sans body (Heebo).** Heading weight is **500**, never 700 (bold Hebrew serif looks dense). Body weight ≤500.
4. **Hairlines over shadows.** Default to 1px borders. When shadow is used: warm, low, never blue. ≤1 elevated layer visible at once on a section.
5. **Radii: 0–2px on everything.** Only avatars and filter chips get pill radius. Images get 0px.
6. **Pure black and pure white are forbidden** outside of paper cards (paper-0 = #FFF is allowed only on card surfaces).
7. **Positive/negative tones appear only inside numeric data**, never as decorative chrome.
8. **No dark mode.** Lovable's self-critique fix #4: dark mode cheapens warm-cream systems.
9. **All transitions respect `prefers-reduced-motion: reduce`** → durations 0, no transforms.
10. **RTL-first.** Every directional decision (underline origin, table numeric edge, drawer side, breadcrumb separator, next/prev arrows) is RTL-aware. See `design-rtl-hebrew.md`.

## Tokens (the values to paste into theme.json + style.css)

### Color (WCAG-AA verified against intended bg per Lovable)
```
--ink-900:       #1B1A17   text, headings, primary button fill
--ink-700:       #2E2B26   strong UI text
--ink-500:       #5C564D   secondary text, captions
--stone-400:     #8A8276   tertiary text, metadata, placeholders
--stone-200:     #C9C3B7   disabled, muted icons
--cream-50:      #FAF7F1   page background (primary)
--cream-100:    #F3EEE3   section alt background, table stripe
--paper-0:       #FFFFFF   card surface, input fill ONLY
--gold-600:      #9C7A3C   accent — links, focus ring, rule, monogram frame
--gold-500:      #B89154   accent hover, chart accent
--gold-200:     #E6D4AE   soft accent wash (used <5%)
--hairline:      #E2DCD0   1px borders, dividers, table grid
--hairline-strong:#C9C0AE  stronger divider, input border
--positive-700:  #3F6B4A   price-up (muted forest)
--negative-700:  #8B3A2E   price-down (muted terracotta)
--focus-ring:    rgba(156,122,60,.40)
--overlay-ink:   rgba(27,26,23,.55)
```

### Typography
- Heading family: `"Frank Ruhl Libre", "Cormorant Garamond", Georgia, serif` — self-hosted woff2 at `assets/fonts/frank-ruhl-libre/`
- Body family: `"Heebo", "Inter", system-ui, sans-serif` — self-hosted woff2 at `assets/fonts/heebo/`
- **Full type scale (desktop + mobile) lives in `docs/design/lovable-output-2026-05-28.md` §Typography.** Mandatory tokens: `display-1, display-2, h1, h2, h3, h4, body-lg, body, body-sm, caption, eyebrow, micro, quote`.
- Article reading column: **680px max** (60–75 Hebrew chars/line).
- Tabular numerics in tools/tables only: `font-variant-numeric: tabular-nums lining-nums`.
- Latin digits inside Hebrew remain LTR — wrap any digit run in `<bdi>` to preserve order.

### Spacing
Base unit **8px**. Scale `4, 8, 12, 16, 20, 24, 32, 40, 48, 64, 80, 96, 128, 160` → `--space-1`..`--space-14`. Section vertical rhythm: desktop **96px** top/bottom, mobile **64px**. Inter-block within a section: **40px** desktop / **32px** mobile.

### Radius / Shadow / Motion / Z-index
All values in source doc + `design-components.md`. Highlights: radius is 0/2/4/pill only; shadows are subtle warm `0 1px 2px / 0 2px 4px+8px 24px / 0 12px 40px` ink-tinted; motion uses 120/220/360/600ms with `cubic-bezier(.2,.6,.2,1)` standard.

### Grid
12 columns, **24px gutter** desktop, **16px** mobile. Container max **1280px** with **80px** outer margin desktop / **20px** mobile. Article reading column **680px**. Tools column **920px**.

## Implementation map (where each token lives)

| Token category | WordPress location |
|---|---|
| Color palette + slugs | `theme.json` → `settings.color.palette` |
| Font families + woff2 fontFace | `theme.json` → `settings.typography.fontFamilies` |
| Font sizes (display-1..micro) | `theme.json` → `settings.typography.fontSizes` |
| Spacing scale | `theme.json` → `settings.spacing.spacingSizes` |
| Shadows | `theme.json` → `settings.shadow.presets` |
| Heading element styles | `theme.json` → `styles.elements.h1..h6` |
| Button defaults | `theme.json` → `styles.elements.button` |
| Component class CSS (.card, .btn, .input-underline, etc.) | `style.css` + `style.min.css` |
| Micro-interactions / focus rings / animated underlines | `style.css` |
| Logo, favicon, OG | Media library; `site_logo`, `site_icon` via `wp/v2/settings`; Yoast Search Appearance for OG |

## Deprecations enacted by this skill

- **`skills/visual-design-skill.md` §6 palette + §6.2 typography**: deprecated. The bright `#D89B3C` gold and `#0E3A8A` trust blue are NOT the brand. Use the tokens above.
- **`skills/luxury-design-language.md` provisional palette**: superseded by Lovable's WCAG-verified palette above.
- **Live theme.json color slugs** (`accent-1`..`accent-6` from the Twenty Twenty-Five fork): **must be remapped** to the new scale on the next theme update. The current calculator widgets and footer use the deprecated palette (`#0E3A8A`, `#D89B3C`, `#0E7C57`) — they need a retoken pass.
- **Calculator widget styling** (`assets/widgets/mortgage-calculator.html`, `assets/widgets/purchase-tax-calculator.html`): inline `<style>` uses the deprecated palette + corporate blue gradient on the result tile. Retoken to the new system per `design-components.md` and per Lovable's calculator screen spec.
- **Premium footer** (`docs/wp-state/template-part-footer.html` deployed live as `custom` override): uses `contrast` (dark) bg with `accent-1` gold — gold is correct slug, but values must remap. Footer **structurally** matches Lovable's footer spec; only the palette+typography refresh remain.

## Open TODOs

- [ ] Owner runs the **second Lovable prompt** (committed at `docs/lovable-prompt-2.md`) to fill the 5 documented gaps.
- [ ] Port Lovable's tokens into `theme.json` (palette + fontFamilies with fontFace + fontSizes + spacingSizes + shadow presets + element styles).
- [ ] Port Lovable's components into `style.css` (and `style.min.css` — the theme enqueues `.min` in production).
- [ ] Rebuild the calculator widget `<style>` blocks to the new tokens + Lovable's calculator spec.
- [ ] Regenerate logo PNG/SVG to Lovable's monogram-in-double-circle spec (the cartoon-house logo currently set as `site_logo` is rejected; replace).
- [ ] Replace the OG image with Lovable's editorial spec.
- [ ] Translate Lovable's section blueprints to Gutenberg `<!-- wp:* -->` block patterns (after second prompt — Lovable's pattern markup will be in the gap fill).

---
_Created 2026-05-28 by Claude Code (claude-opus-4-8). Authoritative source: docs/design/lovable-output-2026-05-28.md._

