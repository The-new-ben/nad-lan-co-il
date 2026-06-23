# Lovable Design Prompt — nad-lan.co.il ("נדל״ן חכם")

> **How to use this:** paste the prompt block below into Lovable. After Lovable generates the design, ask it for the **exact design tokens and CSS** (there's a follow-up prompt at the bottom). Then hand the CSS/tokens back to Claude/Codex, who will port them into the WordPress block theme (`theme.json` + `style.css`). This file is committed so any agent can reuse/refine it.
>
> **Critical context for the porting agent:** the live site is **WordPress 7.0 (block theme `nadlan-revenue`, forked from Twenty Twenty-Five), RTL Hebrew, PHP 8.5**. Lovable outputs React/Tailwind — we do NOT ship Lovable's React. We extract its **visual design decisions** (tokens, type scale, spacing, components, CSS) and re-implement them in the block theme. So the prompt must make Lovable output explicit, portable CSS — not just a pretty React app.

---

## THE PROMPT (paste into Lovable)

```
SCOPE GUARD (read first)
This is a DESIGN-SYSTEM task. Produce: (1) designed screens, (2) a written
design-system document, (3) exact, framework-agnostic CSS + tokens (see OUTPUT).
Do NOT invent product features, pages, or copy beyond this spec. Do NOT use
stock-template patterns. If something is ambiguous, choose the most restrained,
luxury-correct option and note the assumption in the honesty statement at the end.

ROLE
You are a world-class luxury brand & web designer (think the studios behind
Sotheby's International Realty, Christie's International Real Estate, The Agency,
and Compass). You design $1M+ brand systems. I need you to design a complete,
museum-grade visual system for a Hebrew (RTL) real-estate decision platform.
Design like every pixel is judged. Restraint, warmth, and precision over flash.

STEP 0 — COMPETITOR DNA ANALYSIS (do this BEFORE designing, and show it)
Study these references and write a short DNA table. For EACH, list the URL and
3-5 concrete, specific observations about: typography (serif/sans, named feel),
color palette (actual tones), whitespace/grid, hero treatment, navigation,
button style, imagery, and the ONE move that makes it feel expensive.
References:
  - sothebysrealty.com  (serif, tradition, restraint)
  - christiesrealestate.com  (Parisian minimalism, exclusivity)
  - theagencyre.com  (full-bleed imagery, minimal)
  - compass.com  (clean modern, search-forward)
  - luxurypresence.com/best-real-estate-agent-websites  (agency design portfolio)
Then write ONE paragraph: "Design DNA we will borrow (not copy)" — the synthesis
that will guide our system. Do NOT reproduce any competitor's exact text, logo,
layout, or proprietary look. Original work only.

THE BRAND
- Name (Hebrew): נדל״ן חכם  (transliteration: "Nadlan Chacham" = "Smart Real Estate")
- Domain: nad-lan.co.il
- What it is: a premium Hebrew real-estate KNOWLEDGE + TOOLS platform. Not a
  listings board. It helps buyers, sellers, and investors make smart decisions
  BEFORE they sign — with interactive calculators (mortgage, purchase tax,
  valuation, yield), in-depth guides (buying, selling, investing, mortgage,
  tax & legal, urban renewal), city/neighborhood price intelligence, and a
  directory of vetted professionals.
- Audience: Israeli buyers/sellers/investors, including affluent and foreign
  (Anglo/French) investors. The tone is trustworthy, calm, sophisticated,
  data-grounded — NEVER salesy, NEVER cluttered.
- Positioning line (internal): "the calm, expert place you check before the
  biggest financial decision of your life."

NON-NEGOTIABLE CONSTRAINTS
1. RTL Hebrew first. The entire layout, navigation, alignment, and components
   must be designed right-to-left. Latin numerals stay LTR within RTL text.
2. Typography is the #1 luxury signal. Use a SERIF for headings and a clean
   light SANS for body. For Hebrew specifically:
     - Headings: "Frank Ruhl Libre" (the Hebrew equivalent of Playfair Display).
     - Body/UI: "Heebo", weights 300-500.
   Provide a full type scale (H1-H6, body, small, eyebrow/label, caption) with
   exact px/rem sizes, line-heights, letter-spacing, and weights for BOTH
   desktop and mobile. Big serif headings = tight tracking. Small labels =
   wide tracking (Hebrew has no uppercase; tracking carries the "label" feel).
3. Color: warm, minimal, expensive. Two neutrals + ONE metallic accent.
   Anchor it on: near-black ink (NOT pure #000), warm cream, antique muted gold
   (NOT bright gold), warm stone-gray for secondary text, warm hairline borders.
   Give exact hex values for: ink, base/white, cream, gold-accent, stone,
   hairline-line, muted-positive (price up), muted-negative (price down),
   and any tints/shades. Avoid corporate blue entirely. Avoid bright/neon.
4. Forced minimalism. Generous, confident whitespace. Hairline 1px borders
   preferred over heavy drop-shadows. When shadow is used, make it soft, warm,
   and subtle. Section padding should feel editorial and spacious.
5. Performance-minded: local fonts only (no runtime CDN), no heavy gradients,
   no glassmorphism, no parallax gimmicks, no auto-playing video. Elegance
   through type, space, and a single accent — not effects.
6. Accessibility: WCAG AA contrast, visible focus states, 44px+ tap targets.

DELIVERABLES (design ALL of these as polished screens, desktop + mobile)
A. Design tokens: the full color palette, the type scale, an 8px spacing scale,
   border-radius scale (luxury = small radii: 0-4px mostly), shadow scale,
   a motion/transition token set (durations + easing), and z-index scale.
B. Logo / wordmark: an elegant SERIF wordmark for "נדל״ן חכם" using Frank Ruhl
   Libre, with an optional refined monogram mark (the letter נ treated like a
   crest/seal — thin gold frame), a thin gold rule, and a wide-tracked tagline
   eyebrow. NO cartoon house icons. Provide horizontal + stacked + favicon
   (monogram) + dark-background (cream) variants.
C. Header / navigation: thin, sticky, "traveling" on scroll with a hairline and
   subtle backdrop. Right-aligned logo (RTL), restrained primary nav, ONE quiet
   CTA, a refined search affordance. Show the mobile hamburger → full-screen
   elegant drawer.
D. Homepage: a luxury editorial layout. Hero with a confident serif headline +
   calm subline + a single elegant search/CTA (no loud buttons). Then: a row of
   the 5 signature TOOLS as refined cards; a "why" trust band with restrained
   data points; a city/neighborhood price-intelligence section; guide/pillar
   highlights; a professionals teaser; and the footer. Editorial spacing
   throughout.
E. Pillar/guide article page: gorgeous long-form reading experience — serif
   headings, comfortable body measure (~680px), a sticky table-of-contents, an
   author/trust strip, pull-quotes, elegant tables, FAQ accordion, breadcrumb,
   and a tasteful related-articles block. This is where most SEO traffic lands;
   it must feel like reading a premium magazine.
F. Calculator / tool page: a beautiful interactive tool module. Show the
   MORTGAGE calculator (Israeli 3-track mix: קל״צ / פריים / משתנה, with a
   monthly-payment result, a stacked contribution bar, and a "+2% stress test"
   toggle) and the PURCHASE-TAX calculator (2026 brackets, a VISUAL bracket bar
   with a live position marker, single-apartment vs investor toggle, per-bracket
   breakdown). Design the inputs, sliders, result tiles, the bracket
   visualization, and the data-viz styling (charts: single elegant line, thin
   strokes, gold accent, tabular numerals). These tools are our competitive
   weapon — make them feel like a premium fintech product.
G. City / neighborhood page: price trend chart, average ₪/m², a stat band,
   a refined listings/projects grid, and a map placeholder styled elegantly.
H. Professionals directory: elegant profile cards (photo, name, specialty,
   city), filters, and a single profile page.
I. Components library: buttons (primary quiet ink, secondary outline, text
   link), form inputs (large, hairline, focus = gold ring), cards (hairline +
   hover lift), tables, tabs, accordion, breadcrumb, pagination, badges/tags,
   tooltips, the lead/contact form, toasts, and an elegant 404.
J. Footer: editorial multi-column (brand block + content pillars + tools +
   legal), thin gold rule, restrained.
K. Micro-interactions spec: hover/focus/active states for every interactive
   element, with exact timing and easing. RTL-aware (e.g., underline grows
   from the right).

GRANULARITY (break the system into 100+ concrete decisions, not vibes)
Be exhaustive and specific. Spell out exact values for: every color + its
tints/shades + which goes on which background; every type style (size,
line-height, weight, tracking, desktop + mobile); every spacing step; every
radius; every shadow; every border; every state (default/hover/focus/active/
disabled) for every interactive element; empty states; loading states; error
states; the exact RTL behavior of each component. If a real designer would
decide it, you decide it and write it down. No "use your judgment" hand-waving.

COPY RULES (for the Hebrew placeholder copy you write)
- Real, idiomatic Hebrew. Not translated-from-English.
- No long em-dashes. No AI giveaway phrases ("חשוב להבין", "ראוי לציין",
  "בעידן הנוכחי", "עולם הנדל\"ן", rhetorical-question stacks).
- No salesy hype ("הזול ביותר", "המתקדם בישראל"). Calm, factual, confident.
- Numbers with context; ₪ formatted as 2,500,000 ₪.
- Never expose internal/marketing jargon in visible copy.

STYLE REFERENCES (match this caliber, do not copy)
Sotheby's Intl Realty (serif, restraint, tradition), Christie's Intl RE
(Parisian minimalism, exclusivity), The Agency (full-bleed imagery, minimal),
Compass (clean modern). Aim for the intersection: classic-luxury serif
sophistication with modern clarity. Warm, editorial, expensive, calm.

OUTPUT FORMAT
1. STEP 0 competitor DNA table + the "design DNA we will borrow" paragraph.
2. The designed screens (desktop + mobile) for every deliverable A-K.
3. A written DESIGN SYSTEM doc with every token + component spec spelled out,
   precise enough that a developer rebuilds it in plain CSS without guessing.
4. Use real Hebrew RTL copy placeholders so I judge the true feel, not lorem.
5. SELF-CRITIQUE: before finishing, audit your own design against this bar —
   "Would Sotheby's ship this? What still looks templated or cheap?" — and fix
   it. List the 3 weakest spots and what you changed.
6. HONESTY STATEMENT (end): state explicitly what you DESIGNED vs what you
   ASSUMED, and what still requires real inputs to look $1M (e.g. professional
   architectural photography, final logo lockup, real transaction data,
   final Hebrew copy). Separate "done" from "needs real assets."
```

---

## FOLLOW-UP PROMPT (ask Lovable AFTER it designs — to extract portable CSS)

```
Now export the design system as framework-agnostic, copy-paste CSS so I can
implement it in a WordPress block theme (NOT React). Specifically give me:

1. A :root { } block with ALL design tokens as CSS custom properties:
   --color-ink, --color-base, --color-cream, --color-gold, --color-stone,
   --color-line, --color-positive, --color-negative, plus every spacing step
   (--space-1..--space-12 on an 8px scale), font sizes (--fs-h1..--fs-caption),
   line-heights, letter-spacings, radii, shadows (--shadow-sm/md/lg), and
   motion tokens (--ease, --dur).
2. @font-face declarations for Frank Ruhl Libre (headings) and Heebo (body),
   assuming local woff2 files (I will host them; just reference
   /wp-content/themes/nadlan-revenue/assets/fonts/...).
3. Base element styles: html/body, h1-h6, p, a (with RTL-aware animated
   underline), ul/ol, blockquote, table, hr, ::selection.
4. Component CSS classes for: buttons (.btn, .btn-secondary, .btn-text),
   inputs/forms, cards (.card with hover), the sticky header, the footer grid,
   eyebrow/label utility, breadcrumb, accordion, tags/badges, and the
   calculator UI (result tiles, bracket bar, stacked bar, sliders).
5. All CSS must be RTL-correct (use logical properties: margin-inline,
   padding-inline, inset-inline; text-align:start; etc.).
6. A short mapping note: which tokens should go into WordPress theme.json
   (palette + fontFamilies + fontSizes + spacingSizes) vs which belong in
   style.css (interactions, component classes).

Keep it clean, commented, and production-ready. No Tailwind utility soup —
real semantic CSS I can paste into a theme.
```

---

## Porting checklist (for Claude / Codex after Lovable returns)

When Lovable's CSS + tokens come back:

1. **theme.json** ← palette (`settings.color.palette`), font families (`settings.typography.fontFamilies` with the bundled woff2 `fontFace`), font sizes (`settings.typography.fontSizes`), spacing scale (`settings.spacing.spacingSizes`), and the global heading/button/link `styles`. Bump `$schema` to v3 (already v3).
2. **style.css + style.min.css** ← @font-face (already bundled fonts at `assets/fonts/frank-ruhl-libre/` + `assets/fonts/heebo/`), base element styles, component classes, micro-interactions, sticky-header polish, RTL logical properties. (Theme enqueues `style.min.css` in production — put the CSS in BOTH or update the enqueue in functions.php.)
3. **Header/footer template parts** ← rebuild via REST (`/wp/v2/template-parts/nadlan-revenue//header` and `//footer`) to match Lovable's header/footer, using the new classes.
4. **Calculator widgets** ← restyle `assets/widgets/*.html` to Lovable's tool UI (already deployed on the calculator pages; update the inline `<style>` to the new tokens).
5. **Logo / favicon / OG** ← if Lovable's wordmark differs from the current serif version, regenerate (PIL pipeline with Frank Ruhl Libre TTF is set up) or export Lovable's SVG, then upload + set `site_logo` / `site_icon` / Yoast OG via REST.
6. Verify live: fonts actually load (check `assets/fonts/...` 200s), palette applied, RTL correct on mobile, Lighthouse ≥ 90 desktop / ≥ 80 mobile.
7. Update `skills/luxury-design-language.md` with the final token values Lovable produced (replace the provisional hexes if Lovable refines them).

## Notes
- Fonts are already bundled locally (OFL): `assets/fonts/frank-ruhl-libre/` and `assets/fonts/heebo/`. Lovable's @font-face should point at those paths.
- Keep the owner's constraints: no new paid services, no runtime CDN fonts, no plugin sprawl. Lovable is a design source; implementation stays in the block theme + REST.
- The provisional palette in `skills/luxury-design-language.md` (ink #1A1A1C, cream #F7F4ED, gold #B08D57, stone #7A746C, line #E5E1D8) is a starting point — let Lovable refine it, then lock the final values into both this prompt's outcome and the skill.

---
_Created 2026-05-28 by Claude Code (claude-opus-4-8). Owner allocated a "$1M-quality" design bar and prefers Lovable for the visual design pass; Claude/Codex port the result into the WordPress block theme._
