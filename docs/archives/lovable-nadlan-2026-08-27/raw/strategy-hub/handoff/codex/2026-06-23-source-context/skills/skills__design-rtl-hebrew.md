# RTL Hebrew Rules — the directional decisions every component must respect

> **Notice to all agents:** Hebrew is RTL. Every directional design decision has an RTL-aware answer below. When you build or restyle a component, **check this skill BEFORE writing CSS**, because LTR habits sneak in unless you actively flip them. This skill consolidates RTL rules scattered across Lovable's spec into a single operational reference.

## Use CSS logical properties, not physical

Always prefer:
- `margin-inline-start` / `margin-inline-end` (NOT `margin-left` / `margin-right`)
- `padding-inline-start` / `padding-inline-end`
- `inset-inline-start` / `inset-inline-end`
- `border-inline-start-width` / `border-inline-end-width`
- `text-align: start` (NOT `text-align: right`)

When CSS logical properties don't exist for a thing (e.g. `transform: translateX`), explicitly flip in RTL: `[dir="rtl"] .thing { transform: translateX(-Npx); }`.

## Per-component RTL behavior (from Lovable + this skill)

### Underline animations (the signature interaction)
Origin must be the RIGHT side in RTL. Used on nav items, footer links, hover-grow underlines.

```css
.link-luxury {
  background-image: linear-gradient(currentColor, currentColor);
  background-size: 0 1px;
  background-repeat: no-repeat;
  background-position: 100% 100%;   /* RTL: right edge */
  transition: background-size var(--dur-2) var(--ease-standard);
}
.link-luxury:hover { background-size: 100% 1px; }
```

LTR version uses `background-position: 0% 100%` (left edge).

### Breadcrumb
- Order reads right-to-left (the root "בית" sits on the **right**).
- Separator `/` is symmetric in glyph, so no flipping needed.
- Spacing 8px each side of the `/`.

### Pagination arrows
- "Next" arrow in Hebrew is `←` (points left, because RTL reading advances leftward).
- "Previous" is `→`.
- Don't auto-flip arrows with `transform: scaleX(-1)` — use the correct glyph from the start.

### Table numeric columns
- Numeric columns sit on the **LEFT edge** of the table in RTL (mirror of conventional finance reading where numbers are at the right edge in LTR).
- Cells with numbers: `text-align: end` would put them on the left in RTL — correct.
- The numbers themselves stay LTR (digits read left-to-right). Wrap in `<bdi>` if mixed with text.

### Mobile drawer
- Opens from the **RIGHT** in RTL (matches the hamburger-on-the-left, drawer-on-the-right pattern when reversed for RTL: hamburger left, drawer right). Lovable: "Hamburger opens a full-screen drawer sliding from the right."
- LTR sites: drawer slides from the left.

### Sticky article TOC
- TOC rail is on the **right** (start side in RTL). The article content is in the center; the author rail is on the **left** (end side).
- Active TOC item gets a 1px gold **right** border (the inline-start border, RTL).

### Pull-quote
- The accent rule is on the **RIGHT** edge (the start side, the side the eye lands on first in RTL).
- Lovable: "1px gold left border (RTL: right border) 2px wide, 32px padding-right."

### Card hover gold edge
- Profile-card and listing-card hover state shows a "gold 1px right border (RTL)".
- The right border in RTL = the start-inline edge.

### Footer column order (RTL right→left)
- Right column = **brand block**
- Then **מדריכים**
- Then **כלים**
- Then **חברה** on the left.

### Header layout (RTL)
- **Right** = logo (the start-inline edge, where the brand belongs).
- **Center** = primary nav.
- **Left** = search icon + single CTA (end-inline edge).
- Lovable: "Right = logo, Center = primary nav (5 items max), Left = search icon + single quiet CTA."

### Search sheet
- Search input is right-aligned (RTL).
- Recent-queries list appears below, RTL.

### Form input affordances
- Text in inputs is right-aligned.
- Label sits **above** the field (Lovable: "label NEVER floats — fixed above"), right-aligned.
- Currency suffix (₪) appears inline AFTER the number (Lovable: "suffix `₪` set inline, ink-500, 8px gap, RTL preserved").
- Required-marker gold dot sits at the **end** of the label text (the left side in RTL).

### Toast position (mobile vs desktop)
- Lovable: bottom-center on desktop, top-center on mobile. **Not** corner-pinned (corner-pinning forces an LTR or RTL decision; centering avoids the problem).

### Number formatting inside Hebrew prose
- **Latin digits remain LTR**: wrap any digit run in `<bdi>` to preserve correct order in mixed Hebrew/number text.
- Examples: `<bdi>2,500,000 ₪</bdi>`, `<bdi>+6%</bdi>`.
- Tables and tools always use `font-variant-numeric: tabular-nums lining-nums`.

### Date formatting
- Hebrew dates use day-month-year: `15 בינואר 2026`.
- Numeric dates: `2026-01-15` (ISO; LTR digits, safe in any direction).
- Avoid `15/1/26` — ambiguous and clashes with the gold-`/` breadcrumb separator visually.

### Currency
- Always **after** the amount with 8px gap inline: `2,500,000 ₪`.
- Never `₪2,500,000` (LTR habit).
- Always with thousand separators (comma in Hebrew financial convention).

## What Hebrew DOES NOT have that affects UX

- **No uppercase.** Tracking carries the "label" feel instead. That's why our `eyebrow` style uses `letter-spacing: 0.18em` — to create the visual signal that ALL CAPS gives in English.
- **No italics for emphasis** — Hebrew italics look broken and unprofessional. Use **weight** (400 → 500) or **the Heebo→Frank Ruhl Libre family switch** for emphasis. The pull-quote uses Frank Ruhl Libre **italic 400** because it's a SERIF italic which Hebrew can carry; in body Heebo, never italicize.

## When you write CSS that touches direction

Before committing, grep your CSS for these LTR-habit words and consider whether each should be flipped:
- `left:` → `inset-inline-start:`
- `right:` → `inset-inline-end:`
- `margin-left:` → `margin-inline-start:`
- `margin-right:` → `margin-inline-end:`
- `padding-left:` → `padding-inline-start:`
- `padding-right:` → `padding-inline-end:`
- `text-align: left` → `text-align: start`
- `text-align: right` → `text-align: end`
- `border-left:` → `border-inline-start:`
- `border-right:` → `border-inline-end:`
- `transform: translateX(N)` → manually flip in RTL OR use `translate(N, 0)` with `transform-origin: 100% 0%` and document why

## Open TODOs

- [ ] Audit the live calculator widgets' inline `<style>` for hard-coded `right:` / `left:` — replace with logical properties.
- [ ] Confirm the live footer's column order is RIGHT→LEFT (brand · מדריכים · כלים · חברה) and not the deployed LTR-style flow.
- [ ] Article template's TOC rail: ensure it's on the right (start-inline) when implemented.
- [ ] All future widgets and patterns: enforce these rules in code review.

---
_Created 2026-05-28 by Claude Code (claude-opus-4-8). Consolidated from RTL rules scattered through docs/design/lovable-output-2026-05-28.md + Hebrew-typography knowledge._

