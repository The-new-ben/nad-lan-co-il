# Monetization Surfaces — designed-in, never bolt-on

> **Notice to all agents:** every paid surface on nad-lan.co.il MUST live inside the luxury system and read as editorial sponsorship — not banner advertising. This skill defines what's allowed, what's forbidden, and how to wire reserved slots into the CMS NOW so revenue can be turned on later without redesign. The full Lovable spec lands in `docs/design/lovable-output-round-2.md` after the second prompt; this skill is the operational summary + the rules that bind every agent.

## The principle

A premium real-estate research desk doesn't sell banner ads — it hosts **editorial partnerships, premium professional placements, and discreet sponsored capsules**. Every monetization surface follows these rules:

- ❌ **Never** IAB display sizes (300×250, 728×90, etc.).
- ❌ **Never** colored backgrounds to differentiate sponsored content.
- ❌ **Never** auto-play, animated, or flashing elements.
- ❌ **Never** pop-ups, interstitials, exit-intent modals, sticky-bottom image bars.
- ❌ **Never** "verified" gold-star badges or checkmark icons.
- ❌ **Never** more than ONE sponsored capsule + sponsored pins visible at once.
- ✅ **Always** discreet gold eyebrow disclosure: `שותפות בתשלום` / `מודעה ממומנת` / `ממומן`.
- ✅ **Always** a 1px gold-600 hairline frame as the visual differentiator (not a fill).
- ✅ **Always** typography-only for inline article capsules (no images).

## Sponsored surfaces — per format

### Sponsored guide / article
Identical to a normal pillar article. Differentials:
- Category eyebrow replaced by `תוכן שותפים · [partner]` in gold.
- 32px hairline gold band at top of article body with caption: `תוכן זה נתמך על־ידי [partner name]. הביקורת המערכתית של נדל״ן חכם נשמרת.`
- Partner wordmark (monochrome ink-700, max 24px tall) in the author/trust strip replaces the avatar.

### Sponsored listing (in the listings grid)
- Identical to the §G listing card.
- Adds 1px `--gold-600` hairline frame around the card.
- Eyebrow at top of card content reads `ממומן · [partner]` in gold.
- Optional 8px gold ◆ ribbon top-right of image. **One** ribbon only.
- In a listings grid: sponsored cards may appear at positions **1, 5, 9** — max 1 in 4. Caption at bottom of grid: `מודעות ממומנות מסומנות. סדר הצגה אינו דירוג איכותי.`

### Sponsored map pin
- 10px gold dot + 1.5px gold ring (slightly larger than default 8px pin).
- Popover identical to §G map popover with eyebrow `ממומן` at top.

### Sponsored capsule (in-article)
- Typography only — NEVER an image.
- Full article-column width (680px), 1px hairline card, 24px padding.
- Layout: eyebrow `שותפות בתשלום` gold → h4 partner headline → body-sm 2-line dek → single text-link CTA.
- **Max ONE per article body.**

### Mobile bottom sticky (article)
- 56px tall, paper-0, hairline top.
- Eyebrow + h4 + arrow text link.
- Dismissible × on the right (RTL).
- **Mobile only.** Desktop has the rails for sponsored capsules instead.

### Partner / sponsor strip (homepage)
- Optional section between Professionals teaser and footer.
- Eyebrow `בשיתוף עם` centered, gold.
- Row of 5–7 partner wordmarks, all monochrome ink-700 at **24px height**, separated by 8px gold dots, 64px horizontal spacing.
- Hairline 1px ink at 12% above and below the strip.
- **No color logos. No graphics. No "see all partners" CTA.**

### Cookie/analytics disclosure (legal, designed-in)
- Cream-100 strip 48px tall.
- ink-700 body-sm caption: `באתר זה משתמשים במדידה מצטברת בלבד, ללא קוקיז צד שלישי.`
- Text link `פרטיות` (RTL: visually left).
- Dismiss × on the right. Persistent until dismissed (cookie/localStorage flag).

## Professional directory — tier visual differentials

Designed-in even before paid tiers go live:

| Tier | Card visual | Tag |
|---|---|---|
| **Free** | Standard §H profile card | — |
| **Pro** | Adds 1px `--gold-600` hairline frame | Gold eyebrow `pro` next to specialty |
| **Premier** | Surface becomes `--cream-100` (not paper-0); portrait gains 1px gold inset frame; appears at top of any filter result | Gold eyebrow `פרימייר` |

Filter sidebar adds a hairline pill toggle `פרימייר בלבד`.

### Sponsored professional placement
- Slot 1 of every page of results = a "מומלץ" card identical to a Premier card plus an additional eyebrow `מודעה` gold below city/languages.
- Caption row at bottom: `אנשי מקצוע ממומנים מסומנים.`

## Reserved slots — declare positions NOW even when unused

These slots are part of the CSS classes + Gutenberg block-pattern markup from day one, so adding revenue later is a content decision, never a redesign. Each renders as a 1px hairline empty box with eyebrow `מיועד לשותפות עתידית` until a sponsor activates it.

| Position | Page type | Slot |
|---|---|---|
| Between §D.5 (Guides) and §D.6 (Professionals) | Homepage | Sponsored capsule |
| Below the trend chart, above the sub-neighborhood table | City / neighborhood | Sponsored capsule |
| Right rail beneath the inputs | Calculator | Sponsored capsule |
| Left rail below author/share strip | Pillar / guide article | Sponsored capsule |

## CSS classes (must exist in the bundle from day one)

```
.sponsored-frame     — 1px gold-600 frame on cards/articles
.sponsored-eyebrow   — eyebrow gold-600 for "ממומן" / "שותפות בתשלום"
.sponsored-capsule   — typography-only inline article ad
.sponsor-strip       — homepage partner row
.pro-card            — directory Pro tier
.premier-card        — directory Premier tier
.ad-slot-reserved    — 1px hairline empty placeholder
```

These are part of GAP 4 (CSS bundle) and GAP 7 of `docs/lovable-prompt-2.md`.

## Schema / CMS readiness (so future monetization is content-not-rebuild)

When the `nadlan_property` and `nadlan_professional` CPTs are registered (Phase 1 of `agent-tooling-strategy.md`), include these fields from day one:

- `is_sponsored: bool` — boolean flag, surfaces the sponsored visual.
- `sponsor_name: string` — partner wordmark + eyebrow label text.
- `sponsor_logo: media_id` — wordmark file (monochrome ink-700, max 24px tall).
- `tier: enum('free','pro','premier')` — directory only.
- `sponsored_until: datetime` — auto-expiry of the sponsored visual.
- `sponsored_position_preference: int` — where in the grid (1/5/9 enforced server-side).

For articles, add a `sponsored_capsule_block` reusable block slot per article so editors can place ONE capsule without rebuilding the page each time.

Plugin `nadlan-config` will gain endpoints (v1.0.6+) to manage these flags via REST without WP-admin clicks: `POST /wp-json/nadlan/v1/sponsorship` etc. Defer until the CPTs exist.

## Israeli legal disclosure

The eyebrow gold disclosure (`שותפות בתשלום` / `מודעה ממומנת`) is the on-page legal disclosure under Israeli consumer protection norms for sponsored content. **Never** bury disclosure in fine print at the bottom. Always above-the-content, eyebrow gold, in plain Hebrew. When in doubt, default to `שותפות בתשלום` — it's the most defensible phrasing.

## Open TODOs

- [ ] Run Lovable round 2 (GAP 7 specs all the visuals).
- [ ] Port the CSS classes into the bundle.
- [ ] When `nadlan_property` + `nadlan_professional` CPTs are registered: add the sponsorship fields above.
- [ ] When the cookie/analytics disclosure goes live: confirm wording with the owner (lawyer).
- [ ] Define the partner-wordmark intake protocol (size, format, color requirements) — should belong in `image-pipeline.md`.

---
_Created 2026-05-28 by Claude Code (claude-opus-4-8). Owner explicitly raised monetization-readiness 2026-05-28; this skill documents how it's wired into the design system from day one._

