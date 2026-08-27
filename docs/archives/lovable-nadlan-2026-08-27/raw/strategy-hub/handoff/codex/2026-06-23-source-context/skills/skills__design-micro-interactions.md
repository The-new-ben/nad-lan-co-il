# Micro-Interactions — the motion state matrix

> **Notice to all agents:** every interactive element on the site uses **one of these motion patterns** — never bespoke. The pattern is a four-state matrix (default / hover / focus / active) + a global `prefers-reduced-motion` override that disables transforms and zeroes durations.

## Global motion tokens (must wire into theme.json/style.css)

```
--dur-1: 120ms   /* micro feedback */
--dur-2: 220ms   /* default */
--dur-3: 360ms   /* entrance / accordion / drawer */
--dur-4: 600ms   /* page-level */
--ease-standard: cubic-bezier(0.2, 0.6, 0.2, 1)
--ease-entrance: cubic-bezier(0.16, 1, 0.3, 1)
--ease-exit:     cubic-bezier(0.4, 0, 1, 1)
```

**Rules (hard):**
- No bounce, no spring, no parallax.
- Hover transitions only on color, border, and 1–2px translation.
- All transitions wrapped in `@media (prefers-reduced-motion: reduce)` → durations 0, no transforms.

## The matrix (Lovable §K)

| Element | Default | Hover | Focus | Active | Notes |
|---|---|---|---|---|---|
| Nav item | underline 0 width | gold underline grows from right to full width, 220ms `--ease-standard` | gold focus ring 2px offset 4px | underline ink-900 | RTL-aware origin (right) |
| Text link | gold underline 1px | thickens to 1.5px, lifts 2px | focus ring | translateY 1px | — |
| Card | hairline default | border darkens to `--hairline-strong`, `--shadow-1`, translateY −2px | focus ring on parent | translateY 0 | — |
| Image in card | full saturation | desaturate 6%, scale 1.01 over 360ms | — | — | reduced-motion: no transform |
| Input | hairline bottom | bottom border darkens | gold bottom 1.5px + label ink-900 | — | label NEVER floats — fixed above |
| Tab | label ink-500 | label ink-900 | focus ring | underline **slides** from previous tab over 220ms | underline width animates with label width |
| Accordion | + icon | + tints ink-900 | focus ring on row | rotates 45° to × | content animates height 360ms `--ease-entrance` |
| Slider thumb | white + gold dot | halo ring | focus ring | scale 1.05 | numeric value updates with tabular-nums |
| Toggle | cream + hairline | hairline darkens | focus ring | knob slides 220ms | — |
| Toast | hidden | — | — | — | enter: fade + 8px translateY, 360ms `--ease-entrance` |
| Page transition | — | — | — | — | content fade 240ms, **no slide** |

## Patterns explained (the ones that matter most)

### Animated underline from the right (RTL-correct)
Used on: nav items, footer links, article-title hover on guide cards, related-articles hover.

```
.link-luxury {
  background-image: linear-gradient(currentColor, currentColor);
  background-size: 0 1px;
  background-repeat: no-repeat;
  background-position: 100% 100%;   /* RTL: starts on the right */
  transition: background-size var(--dur-2) var(--ease-standard);
  color: var(--gold-600);
}
.link-luxury:hover { background-size: 100% 1px; }
```

LTR sites use `background-position: 0% 100%` (origin left). RTL flips it. **Never** use `text-decoration: underline` with `text-underline-offset` for the luxury underline — it doesn't animate cleanly.

### Card lift
2px translateY upward, hairline border darkens, `--shadow-1` appears. Image inside desaturates 4-8% AND scales 1.01 over 360ms. The combination of three subtle changes is what reads as "premium" — single changes look templated.

### Tab underline slide
The underline doesn't fade between tabs — it **slides** with width-animation between labels. This requires the underline to be a child element of the tabs container that absolutely positions itself based on the active tab's offset and width. JS toggles `left` + `width` with `transition: 220ms`.

### Accordion ±/×
The + icon rotates 45° to become × on open. Implementation: a single SVG glyph rotated via CSS transform.

### Drawer entrance with stagger
Mobile drawer opens with `--dur-3 --ease-entrance`. Nav items inside fade in with **80ms stagger per row**. Implementation: `transition-delay: calc(var(--row-index) * 80ms)`.

### Page transition
**Content fade 240ms, no slide.** No carousel, no horizontal slide between pages, no parallax. Luxury = silence + precision, not motion theater.

## Focus rings — universal accessibility

Every interactive element has a focus ring. Default: `2px solid var(--focus-ring)` offset 2-4px. The ring is `--gold-600` at 40% alpha so it reads as a brand-coordinated halo, not the default browser blue.

```
*:focus-visible {
  outline: 2px solid var(--focus-ring);
  outline-offset: 2px;
}
```

44px+ tap targets everywhere (per Lovable's accessibility constraint).

## Reduced motion — global override

```
@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after {
    animation-duration: 0ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0ms !important;
    transform: none !important;
    scroll-behavior: auto !important;
  }
}
```

## Open TODOs

- [ ] Implement all transitions in `style.css` once the second Lovable prompt returns the CSS bundle.
- [ ] Verify the tab-underline slide pattern in the (future) calculator and professional-profile pages — these are the two pages where tabs live.

---
_Created 2026-05-28 by Claude Code (claude-opus-4-8). Source: docs/design/lovable-output-2026-05-28.md §K + §Motion._

