---
name: nadlan-editorial-bright-tokens
description: Cream-luxury design tokens (cream, ink, gold, terracotta), Hebrew-first typography (Frank Ruhl Libre + Heebo), hairline borders, and watermark utility for Nadlan3D. Filename kept per owner spec; visual direction is cream luxury (locked direction in luxury-design-system.md), with terracotta as the only bright accent.
type: design
---

# Nadlan3D — cream-luxury tokens (a.k.a. editorial-bright)

The visual system shared by every Nadlan3D surface. Defined once in
`src/styles.css`, consumed everywhere through Tailwind v4 utilities and
shadcn semantic tokens.

## Colour tokens (oklch)

| Role        | Token (`--…`)  | Value                          | Hex (≈)   | Use                              |
|-------------|----------------|--------------------------------|-----------|----------------------------------|
| Base/bg     | `--cream`      | `oklch(0.972 0.012 85)`        | `#FAF7F1` | page background                  |
| Text/ink    | `--ink`        | `oklch(0.215 0.012 60)`        | `#1B1A17` | foreground, primary CTA          |
| Gold        | `--gold`       | `oklch(0.595 0.085 75)`        | `#9C7A3C` | accents in mark, focus ring      |
| Terracotta  | `--terracotta` | `oklch(0.585 0.145 35)`        | `#C2563A` | "Featured", hot CTAs only        |
| Sage        | `--sage`       | `oklch(0.625 0.045 130)`       | `#7A8F6A` | success/status (reserved)        |

These map to `--background`, `--foreground`, `--primary`, `--accent`, `--ring`
through the `@theme inline` block, so `bg-background`, `text-foreground`,
`bg-accent`, `ring-ring` all work without further config. Never write
hardcoded colour utilities (`text-white`, `bg-black`, `bg-[#…]`).

## Typography

| Surface              | HE (default)            | EN (LTR brand)       |
|----------------------|-------------------------|----------------------|
| Display / headings   | **Frank Ruhl Libre 500**| **Fraunces 500/600** |
| Body / UI            | **Heebo 400/500/700**   | **Inter Tight 400/500** |

Loaded via `@fontsource` packages (no Google Fonts CDN, no remote
`@import` in CSS — would break Lightning CSS). The font stack swaps via the
`html[lang]` selector in `src/styles.css` — `Frank Ruhl Libre + Heebo` for
HE and `Fraunces + Inter Tight` for EN. The HE stack is mandatory because
Fraunces and Inter Tight don't include Hebrew glyphs.

## Hairlines & shape

- 1 px borders on every container (`@utility hairline` / `hairline-b` / `hairline-t`)
- Radii small (`--radius: 0.25rem`, so `rounded-sm` is the default)
- Generous whitespace (`py-12 sm:py-20` on hero, `py-10` on listings)
- One shadow only — `shadow-[0_8px_24px_-12px_rgba(27,26,23,0.18)]` on card hover

## RTL behaviour

- Root `<html dir="rtl" lang="he">` is the default
- `LangProvider` (`src/lib/lang-context.tsx`) toggles `dir` and `lang` on `<html>`
- Use logical properties (`ms-*`, `me-*`, `start-*`, `end-*`) — never `ml-*`/`mr-*`
- Number formatting via `Intl.NumberFormat(lang === "he" ? "he-IL" : "en-IL")`

## Watermark utility (mandatory for AI-generated content)

```html
<div class="watermark-ai relative aspect-[4/3] bg-card">
  <!-- AI image / SVG -->
  <div class="watermark-ai-overlay">להמחשה בלבד · נוצר ב-AI</div>
</div>
```

The overlay is `pointer-events: none`, 45° repeating gradient + centred
uppercase label, and is mandatory on every AI-generated plan render. See
report 05.

## Skill consumers

- WordPress (Codex) — mirror the same hex values into the theme tokens
- Future Lovable runs — never re-introduce purple/indigo gradients, never
  drop the HE font stack

