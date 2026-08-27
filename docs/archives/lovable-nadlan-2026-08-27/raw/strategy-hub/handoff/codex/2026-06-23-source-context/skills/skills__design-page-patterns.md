# Page Patterns — every page type, section by section

> **Notice to all agents:** When you build a NEW page type or restructure an existing one, **read the relevant section here, then open `docs/design/lovable-output-2026-05-28.md` §D-H for the full visual blueprint**. Don't improvise. Every page on nad-lan.co.il follows one of these patterns or extends one.

## Page-type registry

| Page type | Lovable section | Skill cross-refs | Live URLs (examples) |
|---|---|---|---|
| Homepage | §D (7 sections) | components, micro-interactions | `/` |
| Pillar / guide article | §E (3-col with TOC) | components §tables/accordion/quote | `/buying-apartment/`, `/real-estate-lawyer/`, etc. |
| Calculator / tool | §F (2-col, the signature) | components §inputs/charts | `/mortgage-calculator/`, `/purchase-tax-calculator/` |
| City page | §G (band+chart+grid+map) | charts, listing-card | `/tel-aviv-apartment-prices/` |
| Neighborhood page | §G inherits | — | `/neve-tzedek-apartment-prices/`, etc. |
| Professionals directory | §H listing | filter chips, profile card | `/professionals/` |
| Professional profile | §H profile | tabs, contact-form | (one per professional) |
| 404 | §I 404 | — | (any unknown URL) |
| Sitemap | (not in Lovable v1 — see `interactive-widgets.md`) | — | `/sitemap/` |
| Blog index / search results / lead-form variations | **GAP — second Lovable prompt** | — | TBD |

## Homepage — 7 sections (Lovable §D)

The hero replaces button chrome with **two text links + gold underline** — never primary/secondary buttons. The "five tools" row uses **restrained gold serif ordinals (01–05)** in Frank Ruhl Libre italic instead of icons — converts the section from "feature grid" to "table of contents." Each section, top to bottom:

1. **Hero** — `min(720px, 78vh)` desktop / 560px mobile. Composition: text right (RTL), 4:5 architectural photo left with hairline gold 1px frame inset 12px. Eyebrow + `display-1` headline + `body-lg` subline + two text-link CTAs + gold 64px rule + sources caption.
2. **The 5 signature tools** — 5 cards in a row desktop; stack on mobile. Each card: gold serif ordinal 01–05 in italic, `h4` title, 2-line `body-sm` description, bottom text link "פתיחת המחשבון ←". Card spec: paper-0 fill, 1px hairline border, 2px radius, 32px padding, 280px height desktop.
3. **Trust band** — full-width `cream-100` strip, 80px vertical padding. 4 stat tiles separated by 1px gold vertical hairlines 32px tall. Each: `display-2` numeric (tabular-nums) + `eyebrow` label. Below: caption with sources (`רשות המסים, הלמ״ס, בנק ישראל`).
4. **City intelligence** — 2-column. Right (60%): single elegant line chart 36mo ₪/m², 1.25px gold stroke. Left (40%): list of 6 cities with row hover (hairline gold edge + cream-100 bg).
5. **Guides / pillars** — asymmetric editorial 1+2: lead 50% + 2 stacked 50%. Hover: image desaturate 6%, title gold 1px underline from right.
6. **Professionals teaser** — 4 profile cards. Avatar 56px circle (only circular element on homepage). Bottom text link "כל אנשי המקצוע ←".
7. **Footer** — see `design-components.md` §footer.

**Mobile (≤640px)**: hero stacks (image below text); tools become vertical stack; trust 2×2; cities and guides stack.

## Pillar / guide article — 3-column reading (Lovable §E)

This is where most SEO traffic lands. It must feel like reading a **premium magazine**, not a CMS.

### Desktop layout
3 columns inside 1280px container, centered:
- **Right rail** 200px: sticky TOC (`top: 96px`). Eyebrow "בעמוד הזה" + list of H2s as `body-sm` ink-500. Active section: ink-900 + 1px gold right border (RTL).
- **Center** 680px: article column.
- **Left rail** 200px: author avatar 40px + name/role + share affordance + related-anchor.

### Article composition (top to bottom)
1. Breadcrumb (`caption`, ink-500, gold `/` separator). Pattern: `בית / מדריכים / רכישה / [page title]`.
2. Eyebrow (e.g. `מדריך · רכישה`).
3. H1 in Frank Ruhl Libre 44px / line-height 1.15 / weight 500 / tracking −0.015em.
4. Dek (`body-lg`, ink-500, max 620px) — a single restrained sentence describing what's inside.
5. Author/trust strip: 40px avatar + name + role + "עודכן [date]" + reading time. Hairline 1px full-width below.
6. Body 17/1.7 ink-700.
7. **H2 section opener**: 64px top margin, 32px gold rule 24px ABOVE the H2, 16px bottom margin. This is the signature article-rhythm move.
8. **Pull-quote**: full article-column width, Frank Ruhl Libre 28px italic ink-900, 1px gold 2px-wide right border (RTL), 32px padding-right.
9. Lists: bullet is a small `·` in gold, not a dot.
10. Tables: hairline grid, header `cream-100`, tabular-nums, body-sm. Numeric columns sit on the **left** edge of the table in RTL (mirror of finance convention).
11. **Inline data callouts**: thin gold-framed box, ink-900 numeric, eyebrow label above.
12. **FAQ accordion** at end: eyebrow + H2 + rows of `h4` question + ±gold icon, hairline below. Only one open at a time.
13. **Related articles** (3 cards in a row, smaller 16:9 image, eyebrow + h4 + caption reading time).

### Mobile
Single column 20px outer margin. TOC collapses to a top-of-article accordion **"בעמוד הזה ▾"**. Pull-quote becomes full-width with gold rule on top.

### What this replaces on the live site
Codex's existing pillar pages currently have a `nadlan-hub-related-v1` block appended at end (from `internal-linking-hub-spoke.md`). That block must be **restyled to match the related-articles card grid above** as part of the redesign. Keep the marker.

## Calculator / tool page — the signature (Lovable §F)

This is our **competitive weapon**. Israeli competitors are bank calculators (corporate) or email-gated tools (Semerenko). Ours must feel like a **premium fintech research desk** — calm, elegant, transparent.

### Page chrome
Eyebrow "כלים" + H1 (e.g. "מחשבון משכנתא") + `body-lg` subhead + 1px gold rule 64px wide.

### Layout — 2 columns desktop, stacked mobile (inputs first on mobile)
- Right column (RTL primary): **inputs** 420px wide.
- Left column: **results** flex.

### Mortgage calculator (Lovable §F mortgage)
**Inputs grouped in 3 blocks**, each block titled with eyebrow + 1px hairline below:

**Block 1: הנכס וההון העצמי** — שווי הנכס (numeric, `₪` suffix, formatted 2,500,000), הון עצמי, auto-derived caption "יחס מימון: 60%" (LTV).

**Block 2: התמהיל (3 tracks)** — **horizontal stacked allocation bar** 8px tall, hairline border. Three segments: קל״צ (ink-900), פריים (gold-600), משתנה צמודה (stone-400). Below the bar: three rows, each `h4` track name + % input + interest-rate input + term slider 4–30 years. If total ≠ 100%: gold inline note "סה״כ התמהיל: 95% — חסר 5%" (no red error).

**Block 3: תרחישים** — toggle "מבחן עמידות +2%" (rates +2pp; result tile gains a second line in negative-700). Toggle "החזרה חודשית מקסימלית" (red threshold line on the payment timeline).

**Results — 3 large hairline tiles**, each: 1px hairline, 32px padding, eyebrow label, `display-2` numeric (tabular-nums), caption qualifier:
- **החזר חודשי משוקלל** — e.g. `7,840 ₪` — "חודש 1, ממוצע משוקלל בין המסלולים."
- **סך תשלום ריבית לאורך חיי המשכנתא** — "בהנחת ריבית קבועה לתרחיש."
- **יחס החזר מההכנסה** — `34%` — "מומלץ עד 35% לפי בנק ישראל."

Below tiles: **contribution chart** — single horizontal stacked bar 12px tall (principal vs interest over time), 3 segments matching the mix colors. Axis years 1/5/10/15/20/25 in `tabular-nums caption`.

Beneath: caption disclaimer `ink-500` — "החישוב להמחשה בלבד. הריביות בפועל נקבעות על־ידי הבנק המלווה." **No CTA button.** Single text link "שמירת התרחיש להדפסה ←".

### Purchase-tax calculator — bracket bar (Lovable §F purchase-tax — the signature viz)

**Inputs**: שווי הדירה numeric + toggle group **דירה יחידה | דירה נוספת / משקיע** (hairline pill, gold underline active). Optional hairline checkboxes: עולה חדש / נכה / משפר דיור.

**The bracket bar**:
- Horizontal bar spanning the result column.
- 5–7 segments, widths **log-scaled** (so high brackets remain readable).
- Segment fills: graduated tints `cream-100` → `gold-200` → `gold-500`.
- Each segment: bracket range in ₪ caption below + rate above in eyebrow gold.
- **Vertical position marker** = 1.5px ink-900 line + small gold serif triangle on top, positioned at the property value.
- Brackets **paid** are darker; brackets not reached drop to 40% opacity.

**Below the bar**: per-bracket breakdown table (range · rate · amount-in-bracket · tax, tabular-nums, hairline grid) + total-tax tile (same spec as mortgage result tiles, gold rule above) + disclaimer caption "מבוסס על מדרגות 2026. שינויי חקיקה עשויים לעדכן את הסכומים."

### Data-viz styling (all charts on every tool)
- Single accent color per chart (gold by default; ink for comparison series).
- Stroke **1.25px**, no fill under lines unless single-series area (then `gold-200` at 20%).
- No gridlines; only hairline axis baselines.
- Axis labels: Heebo 12px tabular ink-500.
- Tooltip: paper-0 + 1px hairline + 12px padding + 2px radius + `--shadow-2`, tabular-nums, serif value, sans label.

### Replacement of the live calculator widgets
The current widgets at `/mortgage-calculator/` and `/purchase-tax-calculator/` use the **deprecated** corporate-blue `#0E3A8A` and bright gold `#D89B3C`. Retoken to this spec. Per `interactive-widgets.md`, the markers `data-nlc="mortgage-v1"` and `data-nlc="ptx-v1"` are in place; new versions bump to `-v2` and the injection script must REMOVE v1 before prepending v2.

## City / neighborhood page (Lovable §G)

- **Header band**: breadcrumb + eyebrow "מודיעין שוק" + H1 (e.g. "תל אביב — שוק הדירות, רבעון 1 2026.").
- **Stat band**: 4 stat tiles in a row — מחיר ממוצע למ״ר · שינוי 12 חודשים · מספר עסקאות · ימי מכירה ממוצעים. Same hairline-tile spec as calculator results.
- **Trend chart**: 36-month line, single gold series, area fill 12% gold. Toggle pill: 12M / 36M / 60M / כל ההיסטוריה.
- **Sub-neighborhood table**: hairline grid + tabular-nums, sortable by mini gold caret.
- **Listings/projects grid**: 3 columns desktop, each card 4:5 image + eyebrow `פרויקט`/`דירה` + h4 title + address caption + price (tabular-nums) bottom-right with eyebrow "מ־" prefix.
- **Map**: full-width 480px band. **Monochrome cream map** — `cream-100` land, `paper-0` water, `hairline-strong` roads, gold pins (8px `gold-600` dot with 1px ink-900 ring). **Never** default Google Maps blue/logos visible. Implementation: MapLibre + a self-styled basemap.

**Neighborhood inherits** the city page pattern. Differences are scoped to data (smaller polygon, smaller listings count, narrower trend signal — but the visual chrome is identical).

## Professionals directory (Lovable §H)

### Listing page
- **Sticky filter bar** under the header: hairline pill chips — `כל ההתמחויות ▾`, `כל הערים ▾`, `שפות ▾`. Active chip: ink fill, cream text.
- Grid: 3-up desktop, 2-up tablet, 1-up mobile.
- **Profile card**: 1px hairline + 24px padding + portrait 4:5 top (warm-graded, neutral background) + serif `h3` name + eyebrow specialty + caption city+languages with gold-dot separator + bottom gold text link "לפרופיל ←".
- Hover: hairline darkens to `hairline-strong`, gold 1px right border (RTL) appears, image desaturates 8%.

### Profile page
- 2-column header: portrait 4:5 right; left column H1 serif name + eyebrow specialty + `body-lg` short bio + hairline stat row (שנות ניסיון · עסקאות שטופלו · שפות) + single text-link CTA "קביעת ייעוץ ←".
- Tabs below: **על אודות · התמחויות · המלצות · יצירת קשר** (hairline pill row, gold underline active).
- Contact form per `design-components.md` §lead-contact-form.

## Open TODOs

- [ ] Send second Lovable prompt (gaps: blog index, search results, lead-form variations, neighborhood explicit spec, map widget full UI).
- [ ] After porting tokens: rebuild the live calculator widgets to this calculator spec (kill the corporate-blue gradient result tile).
- [ ] Rebuild the live pillar pages' related-articles block (`nadlan-hub-related-v1` marker) to the card-grid spec in §E.
- [ ] Replace the auto sitemap widget's cluster cards with the §G/§E card spec when patterns lands.

---
_Created 2026-05-28 by Claude Code (claude-opus-4-8). Source: docs/design/lovable-output-2026-05-28.md §D-H._

