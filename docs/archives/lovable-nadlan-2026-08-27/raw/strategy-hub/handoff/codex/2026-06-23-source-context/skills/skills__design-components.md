# Components Library — every component, every state

> **Notice to all agents:** when implementing a component, find it here, follow the spec exactly, and cross-reference `docs/design/lovable-output-2026-05-28.md` §I for any detail this skill summarises. Every component has a default + hover + focus + active + (where applicable) disabled state. NO component is ad-hoc.

## Buttons (Lovable §I → Buttons)

**Universal:** radius `2px`, min-height `44px`, Heebo weight 500 16px, tracking 0.02em, transitions on color/background/border `--dur-2 --ease-standard`. **We do NOT use filled gold buttons.** Gold is for accents only.

| Variant | Default | Hover | Focus | Active | Disabled |
|---|---|---|---|---|---|
| **Primary (quiet ink)** | bg `--ink-900`, text `--cream-50`, no border, 24px horizontal padding | bg `--ink-700` | 2px outline `--focus-ring` offset 2px | bg #000 95%, translateY 1px | bg `--stone-200`, text `--paper-0`, cursor not-allowed |
| **Secondary (outline)** | transparent, 1px `--ink-900`, text `--ink-900` | bg `--cream-100` | gold focus ring | bg `--cream-100`, translateY 1px | border `--stone-200`, text `--stone-400` |
| **Text link** | text `--gold-600`, gold 1px underline 4px below baseline, 14px horizontal padding | underline thickens to 1.5px and shifts up 2px | underline `--ink-900` + focus ring | translateY 1px | `--stone-400`, no underline |
| **Quiet (icon)** | icon `--ink-700`, no chrome | icon `--ink-900` + bg `--cream-100` circle 40px | focus ring | icon #000 | `--stone-200` |

## Form inputs — "underline" style (Lovable §I → Form inputs)

Inputs use **only a bottom hairline**, NOT a full box. This is a signature luxury move.

- **Field**: 56px height, 1px `--hairline-strong` bottom only, bg `--paper-0`, padding 16px, text `body` ink-900, right-aligned (RTL).
- **Label** above: `eyebrow` style ink-500. Required marker is a small gold dot (not asterisk).
- **Focus**: bottom border becomes 1.5px `--gold-600`; label color shifts ink-500 → ink-900.
- **Error**: bottom border `--negative-700`, helper text caption `--negative-700` below.
- **Placeholder**: `--stone-400`.
- **Helper text**: caption ink-500, 8px below.
- **Currency suffix** (₪): inline ink-500 8px gap, RTL preserved.

### Sliders
2px track `--hairline-strong`. Filled portion `--ink-900`. Thumb 18px circle paper-0 + 1px ink-900 border + 4px inner gold dot. Hover: outer focus-ring halo.

### Toggle
44×24 pill. Off = `--cream-100` + hairline. On = `--ink-900`. Knob 18px circle white. Transition `--dur-2`.

### Checkbox
18×18 square + 1px `--hairline-strong` + 2px radius. Check = 1.25px gold tick. Focus ring gold.

### Radio
18px circle. Selected: inner 8px ink-900 dot.

## Cards (Lovable §I → Cards)

- **Default**: bg `--paper-0` + 1px `--hairline` + radius 2px + padding 24px (28px on guide cards).
- **Hover** (interactive cards only): border `--hairline-strong`, `--shadow-1` appears, translateY −2px over `--dur-2`. Image inside desaturates 4–8%.
- **No drop-shadow at rest.**

## Tables (Lovable §I → Tables)

- Hairline 1px between rows ONLY (no vertical borders).
- Header row: eyebrow + ink-500 + 16px bottom padding + 1.5px `--hairline-strong` bottom.
- Cells: `body-sm` ink-700, 16px vertical / 12px horizontal padding.
- Numeric columns: `tabular-nums lining-nums`, right-aligned in LTR. **In RTL Hebrew tables, numeric columns sit on the LEFT edge** (mirrors conventional finance reading).
- Sortable header: gold caret. Hover → ink-900.

## Tabs (Lovable §I → Tabs)

- Hairline row of labels, eyebrow size, 16px horizontal gap.
- Active tab: ink-900 + 1.5px gold underline directly under label, **width = label width**.
- Underline **animates** between tabs over `--dur-2`.

## Accordion (Lovable §I → Accordion)

- Row: `h4` question (RTL right-aligned), ± gold indicator on the left side. 1px hairline bottom. Tap target 56px min.
- Open: content `body`, 24px top padding, smooth height `--dur-3`.
- **Only one open at a time on FAQ.**

## Breadcrumb (Lovable §I → Breadcrumb)

- Caption size, ink-500.
- Separator: `/` in `--gold-600` with 8px horizontal spacing.
- Current page: ink-900.
- **RTL note**: breadcrumb reads right-to-left, but the `/` glyph is symmetric so it's safe.

## Pagination (Lovable §I → Pagination)

- Hairline pill row of numbers.
- Current page: ink-900 + gold underline 1.5px.
- Arrows `←` `→` are **RTL-aware**: next is on the **left** in Hebrew (← means next), previous on the right.

## Badges / tags (Lovable §I → Badges/tags)

- `micro` style (11px, tracking 0.14em, weight 500).
- 4px vertical / 10px horizontal padding, 2px radius, 1px hairline.
- **Categories**: hairline only.
- **Status** (e.g. `חדש`): hairline + ink text + tiny gold dot BEFORE.

## Tooltips (Lovable §I → Tooltips)

- `--paper-0` + 1px hairline + `--shadow-2` + 2px radius + 12px padding + `body-sm` + max-width 280px.
- Animation: fade + 4px translateY, `--dur-2 --ease-entrance`.
- Delay **300ms** before show.

## Lead / contact form (Lovable §I → "פנייה לאיש מקצוע")

- Card shell: 40px padding desktop / 24px mobile, 1px hairline, **no shadow**.
- Eyebrow + serif `h3` title (e.g. "קביעת ייעוץ") + subhead `body-sm`.
- Fields stacked: שם מלא · טלפון · אימייל · עיר · נושא הפנייה (select with hairline underline + gold caret) · הודעה (textarea, 4 rows, hairline bottom only).
- Footer: hairline checkbox "אני מאשר/ת קבלת תשובה למייל ולטלפון" + primary button "שליחת פנייה" + caption privacy line.
- **Success state**: replace form with serif `h3` "קיבלנו את הפנייה." + `body` line + 1 text link to return.

This form posts to `/wp-admin/admin-post.php?action=nadlan_lead` (per `nadlan-config-plugin.md` v1.0.3+). Needs `nadlan_nonce` hidden field — once the form is added to a page, add the `[nadlan_lead_nonce]` shortcode (deferred in plugin v1.0.4; will re-add when needed).

## Toasts (Lovable §I → Toasts)

- Position: bottom-center desktop, top-center mobile.
- `--paper-0` + 1px hairline + `--shadow-2` + 2px radius + 16px padding.
- Icon (1.25px stroke) RIGHT, message `body-sm`, dismiss × LEFT.
- Auto-dismiss 5s.

## Header (Lovable §C → Desktop)

- Height **72px** at rest, **56px** when scrolled (`--header-scrolled` state).
- Bg: `--cream-50` at rest; on scroll: `rgba(250,247,241,0.92) + backdrop-filter: saturate(1.05)`.
- Bottom: 1px `--hairline` always; on scroll, gains 4% opacity shadow below.
- Layout (RTL): right = logo, center = primary nav (5 items max), left = search icon + single quiet CTA.
- Nav items: Heebo 500 14px tracking 0.04em ink-700. Hover: ink-900 + **1px gold underline grows from the right** to full width over `--dur-2`.
- Active page: gold underline persistent + ink-900.
- CTA on far left: text link "התחברות" — no button chrome, only hairline underline on hover. **No loud CTA in header.**
- Search: 20px serif `q` icon → opens full-width search sheet from top, 220px height, paper-0 bg, large input with gold focus underline, recent queries below.

### Mobile header
- Height 56px. Right: logo. Left: search icon + hamburger (3 hairlines, 1.25px, 18px wide, 14px tall). Tap targets 44×44 min.
- Hamburger opens **full-screen drawer** sliding from right: cream-50 bg, 32px padding, monogram + × top, nav items as `h3` 500 right-aligned 56px row with hairline dividers, language toggle bottom (HE/EN/FR as eyebrow with gold dots between).
- Drawer opens `--dur-3 --ease-entrance`; content fades in with **80ms stagger per row**.

## Footer (Lovable §J)

- Full-width bg `--ink-900`, text `--cream-50`. Top padding 96px, bottom 48px.
- 4-column grid (RTL right→left): **brand block · מדריכים · כלים · חברה**.
- **Brand block**: monogram + wordmark in cream + gold frame, tagline in `eyebrow` `--stone-400`, short editorial line `body-sm cream-100` 80% opacity: "מקום שקט להחלטות נדל״ן בישראל." Language toggle HE/EN/FR as eyebrow with gold dots between.
- **Column links**: eyebrow heading gold + list of `body-sm cream-50` 80% opacity, 12px row spacing. Hover → 100% + **gold underline from right**.
- Above the bottom row: **full-width 1px gold hairline rule at 40% opacity**.
- Bottom row: `caption stone-400` left + (RTL right): "© 2026 נדל״ן חכם · כל הזכויות שמורות" · "מדיניות פרטיות" · "תנאי שימוש" · "נגישות".
- Social icons ONLY if real accounts exist. If used: 1.25px stroke icons cream-50 60% opacity.

The currently-deployed footer (`docs/wp-state/template-part-footer.html`) **already matches this structure**. The palette/typography refresh is the remaining work.

## 404 (Lovable §I → 404)

- Full viewport, centered.
- Tiny eyebrow "404" gold → serif `display-2` "**הדף הזה כבר נמכר.**" → `body-lg` "אבל יש לנו עוד מה להראות. נסו את המדריכים או את חיפוש הנכסים." → two text links "חזרה לבית ←" and "כל המדריכים ←".
- **No illustration. Pure type.**

## Listing card (referenced in §G, full spec needed in second prompt)

What we know from Lovable §G:
- 3 columns desktop.
- 4:5 image top.
- Eyebrow "פרויקט" or "דירה" + `h4` title + address caption + price tabular-nums bottom-right with eyebrow "מ־" prefix.

Full hover/state spec, mobile spec, "saved/favorited" affordance: **gap → second Lovable prompt**.

## Map widget (referenced in §G, full UI spec needed in second prompt)

What we know from Lovable §G:
- Monochrome cream basemap (cream-100 land, paper-0 water, hairline-strong roads).
- Pins: 8px gold-600 dot with 1px ink-900 ring.
- 480px band height.

Full spec needed: zoom controls, legend, clustering, hover card, fullscreen, popover styling. **Gap → second Lovable prompt.**

## Open TODOs

- [ ] Translate every component spec to actual CSS classes (`.btn`, `.btn-secondary`, `.btn-text`, `.input-underline`, `.card`, `.card-interactive`, `.table-hairline`, etc.) — this is what the **second Lovable prompt** must produce.
- [ ] Build `[nadlan_lead_nonce]` shortcode back into the plugin when the lead form lands on a page (deferred from v1.0.4 since shortcodes were suspected fatal cause; might have been function collision instead — see plugin skill).
- [ ] Listing-card + map widget full specs after second prompt.

---
_Created 2026-05-28 by Claude Code (claude-opus-4-8). Source: docs/design/lovable-output-2026-05-28.md §I + §C + §J._

