# Lovable Prompt #2 — Gap fill for the design system

> **Notice to all agents:** Paste this prompt into Lovable AFTER the first round (which produced `docs/design/lovable-output-2026-05-28.md`). This second prompt fills five specific gaps identified by the design-system review and tells Lovable to **output framework-agnostic CSS + theme.json + Gutenberg block-pattern markup** ready for the WordPress port. Owner approval to send this: granted 2026-05-28.

---

## THE PROMPT (paste into Lovable as a follow-up to your first design)

```
ROUND 2 — Gap fill + WordPress-port artifacts.
This is a continuation of the נדל״ן חכם design system you produced earlier
(saved as nadlanchachamdesignsystem.md). Keep ALL tokens, colors, typography,
spacing, radii, shadows, motion, and components from round 1 — do NOT redesign
them. This round produces five additions plus the artifacts I need to port your
system into a WordPress block theme.

SCOPE GUARD
Do not invent new pages or features. Stay strictly inside the gaps named below.
If something is ambiguous, choose the option most consistent with round 1's
honesty statement, "Would Sotheby's ship this?" bar.

================================================================
GAP 1 — Page types you did not cover
================================================================

Design each of these as a finished screen (desktop + mobile) with the same
caliber and tokens as round 1. Use real Hebrew RTL copy placeholders.

A. Blog index / "מדריכים" archive page
   - Top: eyebrow "מדריכים" + serif H1 "מדריכים לקנייה, מכירה והשקעה."
     + a body-lg dek.
   - Filter row (hairline pill chips): כל הנושאים | קנייה | מכירה | השקעה |
     מימון | מיסוי | התחדשות עירונית | אנשי מקצוע.
   - Editorial grid: lead article + 2 secondary (your asymmetric §D pattern),
     then a uniform 3-up grid of remaining articles.
   - Pagination at bottom per your §I pagination component.

B. Search results page
   - Search field at top (the same expanded sheet you specced for the header,
     but inline).
   - Result row: serif h4 title (the page title) + caption breadcrumb path +
     2-line dek excerpt + eyebrow tag (e.g. "מדריך", "כלי", "עיר") + a small
     gold "match" indicator.
   - Empty state: serif quote-style line "אין תוצאות לחיפוש הזה. נסו ניסוח אחר."
     + 3 suggested popular searches as text links.

C. Lead-form variations
   Three contexts for the lead/contact form you already specced in §I:
   c1. Inline footer of a pillar article — quiet, single column, eyebrow
       "שאלה לעורך?" + h3 + 3 fields (שם, טלפון/אימייל, שאלה) + primary button.
   c2. Modal — opened from a text link "קביעת ייעוץ". Modal width 560px,
       paper-0, --shadow-3, 2px radius, 40px padding. Same form as §I.
   c3. Dedicated page "/contact/" — split layout: left column the form, right
       column an editorial block with eyebrow "צוות נדל״ן חכם" + a serif h2 +
       contact details (no phone if not yet committed — gold rule placeholder).

D. Neighborhood page (currently inherits the city page §G — make the differences
   explicit):
   - Header: breadcrumb includes city → neighborhood, H1 is neighborhood name.
   - Stat band reduced to 3 tiles (smaller sample size honesty).
   - Trend chart same as city.
   - Sub-area breakdown REPLACED by a "streets in this neighborhood" table.
   - Listings grid 2 columns instead of 3 (smaller inventory).
   - The honesty caption near the stat band: "המדגם ב{שכונה} קטן יותר —
     המגמה אמינה, ערכים בודדים פחות."

================================================================
GAP 2 — Map widget — full UI spec
================================================================

You sketched the monochrome cream basemap in §G. Now design the full widget:
- Zoom controls: hairline pill with + and − icons (1.25px stroke), bottom-left
  desktop, top-right mobile, ink-700 icons, 40px tap targets, focus rings.
- Layer toggle (small pill row, top-right desktop): מחירים | פרויקטים | עסקאות
  אחרונות. Active layer: ink fill, cream text.
- Pin variants:
  - Property pin: 8px gold-600 dot + 1px ink-900 ring (you already specced this).
  - Project pin: 10px hollow gold-600 ring + 2px center.
  - Recent-transaction pin: 6px ink-900 dot, no ring.
- Cluster bubble: cream-100 fill, ink-900 number, 1px hairline border, 32px
  circle, count tabular-nums.
- Hover popover from a pin: paper-0 card, 1px hairline, --shadow-2, 2px radius,
  220px wide, contains: 4:3 thumbnail (where applicable), h4 title, address
  caption, price tabular-nums, text-link "לפרופיל ←".
- Legend (bottom-right desktop): 3 rows × (pin sample + label caption).
- Fullscreen affordance: ⤢ icon top-left desktop, opens map into a modal at
  100vw × 100vh with a close × top-right.
- Empty / loading / "אזור לא נמכר ב-12 חודשים" empty states with serif notes.

================================================================
GAP 3 — Listing card — full state spec
================================================================

You sketched it in §G (3 columns, 4:5 image, eyebrow + h4 + caption + price).
Now spec every state and the saved/favorited affordance:
- Default, hover, focus, active states (the matrix from §K).
- "Saved" toggle: 24px outline-heart icon in top-left corner over the image,
  ink-700 stroke 1.25px on a paper-0 6×6 square no-radius badge, hairline
  border. Active state: filled gold-600 heart. Animation: 220ms scale 0.92→1.0.
- "New" or "Price drop" badge: micro style hairline + gold dot prefix, top-right
  corner over image (RTL: actually top-left visually because card content is
  right-aligned).
- Mobile spec: full-width card, 4:5 image, same content stack, tap-anywhere
  to the profile, save-heart 44px tap target.
- Skeleton/loading: 4:5 cream-100 image placeholder, 3 stacked hairline bars
  (60% / 80% / 40% width) for title/dek/price; subtle 1.5s shimmer using
  linear-gradient cream-50→paper-0→cream-50, respecting prefers-reduced-motion.
- Empty state for the listings GRID (no results): serif h3 "לא נמצאו דירות
  בקריטריונים שבחרתם." + body-sm line + text-link "ניקוי סינון ←".

================================================================
GAP 4 — Hand me the CSS bundle (the real artifact I need)
================================================================

Now extract round 1 + round 2 into copy-paste-ready CSS I can drop into a
WordPress block theme's style.css. Specifically:

1. A single :root { } block with ALL design tokens as CSS custom properties:
   - Every color from your palette (--ink-900, --ink-700, --ink-500,
     --stone-400, --stone-200, --cream-50, --cream-100, --paper-0, --gold-600,
     --gold-500, --gold-200, --hairline, --hairline-strong, --positive-700,
     --negative-700, --focus-ring, --overlay-ink).
   - Every spacing step (--space-1 .. --space-14).
   - Every font size from your scale (--fs-display-1, --fs-display-2,
     --fs-h1, --fs-h2, --fs-h3, --fs-h4, --fs-body-lg, --fs-body,
     --fs-body-sm, --fs-caption, --fs-eyebrow, --fs-micro, --fs-quote)
     with matching --lh-* (line-height) and --tr-* (letter-spacing) siblings.
   - Radii, shadows, durations, easings, z-indexes.

2. @font-face declarations for Frank Ruhl Libre (weights 400/500/700/900) and
   Heebo (weights 300/400/500), referencing local WOFF2 files at:
     /wp-content/themes/nadlan-revenue/assets/fonts/frank-ruhl-libre/frl-<w>.woff2
     /wp-content/themes/nadlan-revenue/assets/fonts/heebo/heebo-<w>.woff2
   Include both Hebrew and Latin subsets where applicable, with appropriate
   unicode-range. font-display: swap.

3. Base element styles for html[dir="rtl"], body, h1-h6, p, a, ul, ol, blockquote,
   table, th, td, hr, ::selection (cream on gold). Headings serif weight 500.
   Body 17/1.7 ink-700. Use logical properties (margin-inline, padding-inline,
   text-align: start) so the same CSS works in both RTL and LTR.

4. Component class CSS for every component from §I + the round-2 additions:
   .eyebrow, .tabular, .btn, .btn-secondary, .btn-text, .btn-icon-quiet,
   .input-underline (with label, helper, error), .slider, .toggle,
   .checkbox, .radio, .card, .card-interactive, .table-hairline, .tabs (with
   .tab-underline that animates), .accordion, .breadcrumb, .pagination,
   .badge, .badge-status, .tooltip, .lead-form, .toast, .header-luxury (with
   --header-scrolled state), .footer-luxury, .listing-card, .profile-card,
   .map-widget, .pull-quote, .article-section-opener, .gold-rule.

5. All micro-interactions from §K wired up: .link-luxury (animated gold
   underline from the right, RTL-correct), card lift, tab underline slide,
   accordion ±/×, drawer entrance + 80ms row stagger.

6. The two signature calculator visualizations:
   - .stack-bar (mortgage track allocation + payment contribution) — segments,
     hairline border, label legend.
   - .bracket-bar (purchase-tax) — log-scaled segments with graduated tints,
     vertical position marker with gold serif triangle, paid/unreached states.

7. Global @media (prefers-reduced-motion: reduce) override.

Make the CSS production-ready: clean, semantic class names, generous comments,
RTL-correct via logical properties. NO Tailwind utility soup — real CSS classes.

================================================================
GAP 5 — Hand me the theme.json fragment
================================================================

Now express the tokens as a WordPress block-theme theme.json v3 fragment:

- "settings.color.palette" — every color from your palette with slugs that
  match the CSS variable names (e.g. slug "ink-900", color "#1B1A17", name
  "Ink 900"). defaultPalette: false.
- "settings.typography.fontFamilies" — Frank Ruhl Libre (slug "frank-ruhl-libre")
  with fontFace entries pointing at the local WOFF2 paths (same paths as the
  @font-face block above), each fontFace specifying fontWeight, fontStyle,
  fontFamily, and src. Same for Heebo. Latin fallbacks in the fontFamily
  shorthand.
- "settings.typography.fontSizes" — every named scale step with fluid: false
  (we control fluidity via media query CSS).
- "settings.spacing.spacingSizes" — the full 14-step scale, defaultSpacingSizes:
  false.
- "settings.shadow.presets" — your shadow scale.
- "styles.elements.h1..h6, button, link" — apply your heading + button + link
  defaults via theme.json so the Block Editor inherits them.
- "styles.color.background" → cream-50; "styles.color.text" → ink-700.
- "styles.typography.fontFamily" → heebo; "styles.typography.fontSize" →
  body; "styles.typography.lineHeight" → 1.7.

Output as a single JSON code block I can paste into theme.json.

================================================================
GAP 6 — Gutenberg block-pattern markup
================================================================

For each of these homepage sections from your §D, output WordPress block
markup (the <!-- wp:* --> format) using the CSS classes you just produced
in GAP 4. Use real Hebrew RTL copy. The patterns will be registered as
block patterns in /wp-content/themes/nadlan-revenue/patterns/ so editors
can insert them with one click.

P1. Hero (§D.1) — full markup including the eyebrow, display-1 H1, dek,
    two text-link CTAs, 64px gold rule, sources caption, and the 4:5 image
    placeholder (use a <figure> with class "image-luxury" and a comment
    "Photographer-only architectural shot, warm-graded, landscape").
P2. Five-tools row (§D.2) — the row with the gold serif italic ordinals
    01-05.
P3. Trust band (§D.3) — the cream-100 strip with 4 stat tiles + gold
    vertical hairlines + sources caption.
P4. City intelligence (§D.4) — 2-column with chart placeholder + city
    list.
P5. Guides editorial 1+2 (§D.5).
P6. Professionals teaser (§D.6).
P7. Footer (§J) — full markup of the 4-column dark ink-900 footer with
    gold hairline rule and bottom row.
P8. Article section-opener (§E) — the 32px gold rule + H2 pattern.
P9. Pull-quote (§E) — the Frank Ruhl Libre 28px italic with the gold
    right-side rule (RTL).
P10. FAQ accordion (§E) — opening rows.

For each pattern, prefix with the standard WordPress pattern PHP header:
    <?php
    /**
     * Title: <Hebrew name>
     * Slug: nadlan-revenue/<slug>
     * Categories: nadlan-hero, nadlan-row, etc.
     * Description: <one-line Hebrew description>
     */
    ?>

================================================================
GAP 7 — Monetization surfaces (design-in, never bolt-on)
================================================================

The site will need to host paid surfaces over time without ever feeling like
ad inventory. Design ALL of these so they live inside the luxury system and
read as editorial sponsorship, not banner ads. NO IAB display-ad sizes, no
animated GIFs, no auto-play, no flashing, no full-bleed takeovers. Every
monetization surface gets a discreet eyebrow gold disclosure label per Israeli
disclosure norms ("שותפות בתשלום" or "מודעה ממומנת").

A. Sponsored guide / article — looks like editorial, marked as sponsored
   - Same article template as §E, with an eyebrow "תוכן שותפים · [partner]"
     in gold above the H1 in place of the category eyebrow.
   - At the top of the article body: a hairline 1px gold band 32px tall with
     caption "תוכן זה נתמך על־ידי [partner name]. הביקורת המערכתית של
     נדל״ן חכם נשמרת."
   - The partner's logo (their wordmark, monochrome ink-700, max 24px tall)
     appears in the author/trust strip in place of the avatar.
   - Otherwise identical to a normal pillar/guide. NEVER colored backgrounds,
     NEVER an embedded CTA banner inside the article.

B. Sponsored listing — premium placement in a listings grid
   - Card identical to §G listing card with one differential: a 1px gold-600
     hairline frame around the WHOLE card (not the image), and the eyebrow at
     the top of the card content reads "ממומן · [partner]" in gold.
   - Optional: a tiny gold ribbon ◆ 8px in the top-right of the image (RTL:
     visually top-left). One ribbon only. Never multiple flags.
   - Listings grid: sponsored cards may appear at positions 1, 5, 9 — never
     more than 1 in every 4 cards. Insert a discreet caption row at the
     bottom of the grid: "מודעות ממומנות מסומנות. סדר הצגה אינו דירוג איכותי."

C. Sponsored map pin variant
   - Pin design: a 1px gold-600 ring around the gold-600 dot (slightly larger:
     10px instead of 8px, 1.5px ring).
   - Popover identical to §Map but with an eyebrow "ממומן" at the top.

D. Sidebar / inline ad slot for the article reading column
   - Slot 1: between sections, full article-column width (680px), 1px hairline
     card, 24px padding, eyebrow "שותפות בתשלום" gold, h4 partner headline,
     body-sm 2-line dek, single text-link CTA. NEVER an image — pure type.
     This is the "sponsored capsule."
   - Slot 2 (mobile only — desktop has the rails): bottom-of-article sticky
     bar, 56px tall, paper-0, hairline top, eyebrow + h4 + arrow text link.
     Dismissible × on the right (RTL).
   - At most ONE sponsored capsule per article body, ONE bottom sticky on
     mobile. Never both at once.

E. Partner / sponsor strip (homepage band)
   - A new optional section between §D.6 (Professionals teaser) and the footer.
   - Eyebrow centered "בשיתוף עם" in gold + ink. Below: a row of 5-7 partner
     wordmarks, all rendered monochrome ink-700 at 24px height, separated by
     8px gold dots. Spacing 64px horizontal.
   - NO partner logos in color. NO graphics. NO "see all partners" CTA.
   - Hairline 1px ink at 12% above and below the strip.

F. Professional directory — paid tier visual differentials
   The §H profile card already exists. Define three tiers:
   - Free: card as specced in §H.
   - Pro: card gains a 1px gold-600 hairline frame (same as sponsored listing)
     and an eyebrow tag "pro" gold next to the specialty.
   - Premier: card surface becomes cream-100 (instead of paper-0), portrait
     gains a 1px gold inset frame, eyebrow tag "פרימייר" gold. Appears at the
     top of any filter result.
   - The differential is restrained — never a colored fill, never a "star" or
     "verified checkmark" icon. The frame and the small eyebrow tag carry the
     whole signal.
   - Filter sidebar gains a hairline pill "פרימייר בלבד" toggle.

G. Sponsored professional placement (the directory's revenue-equivalent of
   sponsored listings)
   - On the professional listing page, slot 1 of every page of results is a
     "מומלץ" card identical to a Premier card but with an additional eyebrow
     "מודעה" gold below the city/languages line.
   - Caption row at the bottom: "אנשי מקצוע ממומנים מסומנים."

H. Tracking-free analytics disclosure (legal/UX surface, design it nicely)
   - Bottom-of-page cookie/analytics notice: a cream-100 strip 48px tall,
     ink-700 body-sm caption "באתר זה משתמשים במדידה מצטברת בלבד, ללא קוקיז
     צד שלישי." with a small text link "פרטיות" left-aligned (RTL: visually
     left = end). Dismiss × on the right. Persistent until dismissed.

I. Ad-slot placeholders for the future (declare positions even if unused now)
   - Define and label these positions in your final blueprints, with each
     marked "RESERVED — no live ad" and styled as a 1px hairline empty box
     with eyebrow "מיועד לשותפות עתידית":
     · Homepage section between §D.5 (Guides) and §D.6 (Professionals) — a
       sponsored capsule slot.
     · City page below the trend chart, above the sub-neighborhood table.
     · Calculator page in the right rail beneath the inputs.
     · Article page in the left rail (where the author block lives) — a
       single sponsored capsule below the author/share strip.
   These reserved positions ensure the CMS schema, CSS classes, and template
   slots all exist from day one. Adding revenue later becomes a content
   decision, not a redesign.

J. CSS classes you MUST add to the bundle for monetization surfaces
   (these go into GAP 4):
   .sponsored-frame    — the 1px gold-600 frame applied to cards/articles.
   .sponsored-eyebrow  — eyebrow style in gold-600 for "ממומן" / "שותפות בתשלום".
   .sponsored-capsule  — the typography-only inline article ad.
   .sponsor-strip      — the homepage partner row.
   .pro-card, .premier-card — the directory tier differentials.
   .ad-slot-reserved   — the 1px hairline empty placeholder for future inventory.

K. WHAT WE WILL NEVER DO (so you reject it if it comes up):
   - Display ads (IAB 300×250, 728×90, sticky bottom bars with images, etc.).
   - Pop-ups, interstitials, exit-intent modals.
   - Auto-play video, animated banners, "skip in 5 seconds" anything.
   - Colored backgrounds on sponsored content to differentiate it.
   - "Featured" or "verified" badges as gold checkmarks or stars.
   - Multiple monetization surfaces visible on screen at once (max 1 capsule
     + map sponsored pins is the highest density allowed).
   - Affiliate-link disclosure done badly (always: eyebrow gold disclosure,
     never a small-print paragraph at the bottom).

================================================================
SELF-CRITIQUE (apply, then output)
================================================================

Before finalizing, audit the CSS bundle against round 1's bar: every class
name must be obvious to a developer who has never seen this codebase. Every
selector must be specific without !important. Every transition must respect
prefers-reduced-motion. RTL-correct via logical properties. No Tailwind, no
utility soup. List the 2 weakest spots in the bundle and fix them.

================================================================
HONESTY STATEMENT
================================================================

At the end, state explicitly:
- What is DONE in this bundle (CSS, theme.json, patterns).
- What is ASSUMED (e.g., that the woff2 fonts are at the specified paths,
  that the listing-card is bound to a custom post type the developer will
  register, that the map widget will be powered by MapLibre).
- What still needs real inputs (photography, real listing data, real map
  tiles, a copy editor pass on the Hebrew strings).
```

---

## After Lovable returns, the porting checklist

1. **CSS bundle** → paste into `style.css` (and `style.min.css` — production enqueue) inside the theme. Verify RTL by spot-checking the live calculator pages, sitemap, and pillar pages.
2. **theme.json fragment** → merge into `theme.json` (NOT overwrite — preserve any settings outside the design-system scope). Commit.
3. **Gutenberg block patterns** → save each as `patterns/nadlan-<slug>.php` in the theme, with the standard WP pattern header. The pattern slugs (`nadlan-revenue/<slug>`) become available in the Block Editor inserter.
4. **Page-type screens** (blog index, search results, lead-form variations, neighborhood) → translate Lovable's screen layouts into Gutenberg page templates or block patterns and store under `templates/` or `patterns/`.
5. **Map widget** + **listing card** specs → wait until we register the `nadlan_property` CPT (Phase 1 of `agent-tooling-strategy.md`) before building. Save the spec to `skills/design-components.md` for reference.
6. After porting: bump the theme version to **v1.1.0** (luxury system landed); update `skills/site-state.md` with a verification block (Lighthouse score, RTL spot-check, font loading audit).

## Notes for Lovable's output

- The CSS bundle will be ~500–1500 lines. Save it under `docs/design/lovable-css-2026-05-XX.md` (whatever date Lovable returns it) for traceability.
- The theme.json fragment will be ~150–300 lines.
- The block patterns will be ~10 small files, ~30–80 lines each.
- Total artifact volume: ~2500 lines of authoritative CSS + JSON + markup. **This is what unblocks the full luxury site-wide.**

---
_Created 2026-05-28 by Claude Code (claude-opus-4-8). Use when ready; no expiry._

