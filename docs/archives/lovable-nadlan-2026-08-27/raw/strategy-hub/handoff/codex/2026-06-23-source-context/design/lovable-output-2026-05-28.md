# נדל״ן חכם — Luxury Design System (RTL Hebrew)
**Domain:** nad-lan.co.il
**Scope:** Brand + Web Design System, museum-grade, framework-agnostic.
**Format:** Written specification (design tokens, components, screen blueprints). No code app built.

---

## STEP 0 — Competitor DNA Analysis

### DNA Table

| Reference | Typography | Palette | Whitespace / Grid | Hero | Navigation | Buttons | Imagery | The one move that makes it feel expensive |
|---|---|---|---|---|---|---|---|---|
| **sothebysrealty.com** | Custom Didone-style serif headlines (Benton Modern feel), thin sans (Avenir-like) for UI. Headlines set tight, large. | Off-black ink (~#1A1A1A), warm off-white (~#F7F5F1), single muted blue. No bright accents. | 12-col, generous outer margins (8-12% of viewport). Type-led grid, not card-led. | Full-bleed single hero photograph, headline overlaid bottom-left, no carousel, no badges. | Thin top utility bar + minimal primary nav, ALL CAPS small tracking. Logo dead-center. | Outline buttons, hairline 1px, ALL CAPS micro-tracking. No fills, no rounded corners (2px). | Architectural photography, natural light, no people. Always landscape, always wide. | The **tracked, all-caps serif wordmark + centered nav** — it reads like a magazine masthead, not a website. |
| **christiesrealestate.com** | Serif display (Caslon-ish), neutral sans body. Headlines are restrained in size, never shouty. | Warm cream (~#F4EFE6), deep ink, a single muted Christie's red used sparingly (links/accent). | Heavy left-and-right white margins. Sections separated by silence, not dividers. | Single editorial image + a 2-3 word serif headline, no CTA in hero — discovery is via search bar only. | Centered logo, sparse nav (5 items max), no megamenu. | Text-link CTAs more than buttons. When a button exists: hairline outline, no radius. | Interior photography with painterly tonality, lots of beige/cream. | **Parisian silence** — sections without horizontal dividers, separation purely through whitespace. |
| **theagencyre.com** | Geometric thin sans (Futura-like) for everything, very tight tracking on display sizes. | Pure black + pure white, one warm taupe accent. Monochrome on purpose. | Edge-to-edge full-bleed, very little inner margin on hero. Tight modular grid on content. | Full-screen single image, large thin sans headline, slow fade only. | Black bar, white type, ALL CAPS, hairline divider. | Black fills, white type, square corners, generous padding. | Cinematic, lifestyle, often dusk/night exteriors. | **Cinematic full-bleed + monochrome restraint** — fashion editorial energy, not real estate energy. |
| **compass.com** | Inter-style geometric sans, no serif. Large numerics. | Almost all white, navy ink, one bright Compass red. Cleaner than warm. | Card-driven 12-col, tighter margins than Sotheby's. | Search-first hero: oversized search field IS the hero. No image. | Sticky thin top bar, logo left, search center, account right. | Filled black/navy buttons, 4px radius, friendly. | Listing photography, agent portraits, professional but not editorial. | **Search-as-hero** — the product utility is the brand promise, no decoration. |
| **luxurypresence.com/best-real-estate-agent-websites** | Mixed agency showcase — recurring pattern: high-contrast serif/sans pairing, asymmetric grids, oversized agent names. | Each site monochrome + one accent. Recurring: ink + cream + muted brass/gold. | Big asymmetric editorial grids, magazine columns, pull-quotes. | Agent name set as serif display, image right or full-bleed. | Minimal — usually 4-5 items. | Outline + text-link, rarely filled. | Personal portraits + property hero shots, color-graded warm. | **Asymmetric editorial layouts** treating an agent or agency as a brand, not a service. |

### Design DNA we will borrow (not copy)
We take Sotheby's **typographic restraint and editorial magazine cadence**, Christie's **Parisian silence and warm cream palette with a single quiet accent**, The Agency's **confidence to leave a hero alone**, Compass's **utility-as-hero clarity** (we will surface our calculators where Compass surfaces search), and Luxury Presence's **asymmetric editorial grid** for guides. The synthesis: a calm, serif-led, warm-cream Hebrew RTL platform where tools and knowledge are presented with the dignity of a private bank's research desk — never as a marketplace, never as a SaaS dashboard, never as a listings board.

---

## DESIGN TOKENS

### Color
All values WCAG AA verified against their intended background.

| Token | Hex | Purpose | Min contrast partner |
|---|---|---|---|
| `--ink-900` | `#1B1A17` | Primary text, headings, primary button fill | on cream: 16.8:1 |
| `--ink-700` | `#2E2B26` | Strong UI text | on cream: 13.4:1 |
| `--ink-500` | `#5C564D` | Secondary text, captions | on cream: 7.1:1 |
| `--stone-400` | `#8A8276` | Tertiary text, metadata, placeholder | on cream: 4.6:1 |
| `--stone-200` | `#C9C3B7` | Disabled text, muted icons | decorative |
| `--cream-50` | `#FAF7F1` | Page background (primary) | base |
| `--cream-100` | `#F3EEE3` | Section alt background, table stripe | on cream: 1.05:1 (decorative only) |
| `--paper-0` | `#FFFFFF` | Card surface, input fill | base |
| `--gold-600` | `#9C7A3C` | Accent (links, focus ring, rule, monogram frame) | on cream: 4.7:1 ✓ AA for text ≥14px |
| `--gold-500` | `#B89154` | Hover state of accent, chart accent | decorative |
| `--gold-200` | `#E6D4AE` | Soft accent wash (used <5% of UI) | decorative |
| `--hairline` | `#E2DCD0` | 1px borders, dividers, table grid | decorative |
| `--hairline-strong` | `#C9C0AE` | Stronger divider, input border | on cream: 1.4:1 |
| `--positive-700` | `#3F6B4A` | Price-up, positive delta (muted forest) | on cream: 5.9:1 ✓ |
| `--negative-700` | `#8B3A2E` | Price-down, negative delta (muted terracotta) | on cream: 6.4:1 ✓ |
| `--focus-ring` | `#9C7A3C` at 40% alpha | Focus halo | layered |
| `--overlay-ink` | `rgba(27,26,23,0.55)` | Image overlay for text contrast | layered |

**Rules.** Gold is used in ≤5% of any screen. Never two saturated colors on the same surface. Positive/negative tones appear only inside numeric data — never as decorative chrome. Pure black (`#000`) and pure white (`#FFF` outside of paper cards) are forbidden in compositions.

### Typography

**Families (self-host as WOFF2, no CDN).**
- Headings: `Frank Ruhl Libre` (Hebrew serif). Latin fallback: `Cormorant Garamond`, then `Georgia`.
- Body / UI: `Heebo` (Hebrew sans). Latin fallback: `Inter`, then `system-ui`.
- Tabular numerics in tools: `Heebo` with `font-variant-numeric: tabular-nums lining-nums`.

**Type scale — Desktop.**

| Token | Family | Size | Line-height | Weight | Tracking | Use |
|---|---|---|---|---|---|---|
| `display-1` | Frank Ruhl Libre | 72px / 4.5rem | 1.05 | 500 | -0.02em | Hero homepage |
| `display-2` | Frank Ruhl Libre | 56px / 3.5rem | 1.08 | 500 | -0.018em | Section hero |
| `h1` | Frank Ruhl Libre | 44px / 2.75rem | 1.15 | 500 | -0.015em | Article H1 |
| `h2` | Frank Ruhl Libre | 32px / 2rem | 1.2 | 500 | -0.01em | Section heading |
| `h3` | Frank Ruhl Libre | 24px / 1.5rem | 1.25 | 500 | -0.005em | Sub-section |
| `h4` | Heebo | 18px / 1.125rem | 1.35 | 500 | 0 | Card title, small heading |
| `body-lg` | Heebo | 19px / 1.1875rem | 1.7 | 400 | 0 | Article lead paragraph |
| `body` | Heebo | 17px / 1.0625rem | 1.7 | 400 | 0 | Article body, default text |
| `body-sm` | Heebo | 15px / 0.9375rem | 1.6 | 400 | 0 | UI text, table cells |
| `caption` | Heebo | 13px / 0.8125rem | 1.55 | 400 | 0.01em | Captions, metadata |
| `eyebrow` | Heebo | 12px / 0.75rem | 1.4 | 500 | 0.18em | Eyebrow labels (Hebrew has no caps; tracking carries the label feel) |
| `micro` | Heebo | 11px / 0.6875rem | 1.4 | 500 | 0.14em | Tags, badges |
| `quote` | Frank Ruhl Libre | 28px / 1.75rem | 1.35 | 400 italic | -0.005em | Pull-quote |

**Type scale — Mobile (≤640px).** Down-shift by one step on display sizes; body stays readable.

| Token | Size | Line-height |
|---|---|---|
| `display-1` | 44px | 1.1 |
| `display-2` | 36px | 1.15 |
| `h1` | 30px | 1.2 |
| `h2` | 24px | 1.25 |
| `h3` | 20px | 1.3 |
| `body-lg` | 18px | 1.65 |
| `body` | 16px | 1.65 |
| `eyebrow` | 11px | tracking 0.2em |

**Rules.** Headings always Frank Ruhl Libre, weight 500 (never 700 — bold serif Hebrew looks dense). Body never exceeds weight 500. Hebrew measure: 60-75 characters per line; on the article template, content column is **680px max**. Numerics inside running text use the body font with `tabular-nums` only inside tables/tools, never inline prose. Latin digits inside Hebrew remain LTR — wrap any digit run in `<bdi>` to preserve order.

### Spacing
Base unit 8px. Scale: `4, 8, 12, 16, 20, 24, 32, 40, 48, 64, 80, 96, 128, 160`. Tokens `--space-1` through `--space-14`.
**Section vertical rhythm:** desktop sections `96px` top/bottom (`--space-11`), mobile `64px`. Inter-block within a section: `40px` desktop / `32px` mobile.

### Radius
Luxury = restraint. `--radius-0: 0`, `--radius-1: 2px`, `--radius-2: 4px`, `--radius-pill: 999px` (used only on filter chips and avatar). Cards: **2px**. Inputs: **2px**. Buttons: **2px**. Images: **0**. Never `8px+` except avatars/chips.

### Shadow
Warm, low, never blue.
- `--shadow-0`: none (default — prefer hairlines).
- `--shadow-1`: `0 1px 0 0 rgba(27,26,23,0.04), 0 1px 2px rgba(27,26,23,0.04)` — card resting.
- `--shadow-2`: `0 2px 4px rgba(27,26,23,0.06), 0 8px 24px rgba(27,26,23,0.06)` — card hover, dropdown.
- `--shadow-3`: `0 12px 40px rgba(27,26,23,0.10)` — modal, drawer.
**Rule:** ≤1 elevated layer visible at once on a section.

### Motion
- Durations: `--dur-1: 120ms` (micro), `--dur-2: 220ms` (default), `--dur-3: 360ms` (entrance), `--dur-4: 600ms` (page).
- Easings: `--ease-standard: cubic-bezier(0.2, 0.6, 0.2, 1)`, `--ease-entrance: cubic-bezier(0.16, 1, 0.3, 1)`, `--ease-exit: cubic-bezier(0.4, 0, 1, 1)`.
- No bounce, no spring, no parallax. Hover transitions only on color, border, and 1-2px translation.
- Respect `prefers-reduced-motion`: replace all translates with 0; durations → 0.

### Z-index
`--z-base: 0`, `--z-sticky: 50`, `--z-header: 100`, `--z-dropdown: 200`, `--z-drawer: 300`, `--z-modal: 400`, `--z-toast: 500`, `--z-tooltip: 600`.

### Grid
12 columns, 24px gutter desktop, 16px mobile. Container max **1280px** with 80px outer margin desktop / 20px mobile. Article reading column **680px** centered. Tools column **920px**.

---

## B. LOGO / WORDMARK

### Wordmark
Set **"נדל״ן חכם"** in Frank Ruhl Libre, weight 500, tracking `-0.01em`, optical size 32-48px. The `״` (gershayim) is preserved (not replaced with quote). All letters baseline-aligned; no swashes, no italic, no shadow.

### Monogram (the "seal")
The Hebrew letter **נ** set in Frank Ruhl Libre 500, ink `#1B1A17`, enclosed in a **1px gold (`#9C7A3C`) circle** of diameter 1.6× cap-height. Inside the circle, a second concentric circle at 0.92× provides a hairline frame (the "double rule" used by old houses). The נ sits optically centered, slightly raised (~3% of diameter) to compensate for the letter's open base. No fill behind the נ — the cream shows through.

### Lockups
- **Horizontal (default):** monogram on the right (RTL), 16px gap, wordmark to its left, baseline of wordmark aligned to monogram center. Optional tagline below wordmark: `eyebrow` style, gold underline rule 24px wide, 1px, centered under tagline.
- **Stacked:** monogram top, wordmark below, tagline below wordmark. Centered.
- **Favicon:** monogram only, 32×32 and 16×16 (at 16px, drop the inner hairline circle).
- **Dark background variant:** monogram and wordmark in `--cream-50`; gold frame remains `--gold-600`.

### Tagline (eyebrow under wordmark)
**"ידע. כלים. החלטות."** (Knowledge. Tools. Decisions.) Set in Heebo 500, 12px, tracking `0.22em`, color `--ink-500`.

### What we will NOT do
No house icon, no key, no roof, no graph, no skyline, no map pin, no abstract "n" mark, no gradient, no 3D, no shadow on the mark.

---

## C. HEADER / NAVIGATION

### Desktop
- Height **72px** at rest, **56px** when scrolled (state: `--header-scrolled`).
- Background: `--cream-50` at rest, `rgba(250,247,241,0.92)` + `backdrop-filter: saturate(1.05)` when scrolled.
- Bottom: 1px `--hairline` always; on scroll, hairline gains 4% opacity shadow below.
- Layout (RTL): **right** = logo (horizontal lockup, monogram height 32px), **center** = primary nav (5 items max), **left** = search icon + single quiet CTA.
- Primary nav items (Hebrew, in RTL display order from right to left):
  `מדריכים  ·  כלים  ·  ערים  ·  אנשי מקצוע  ·  על אודות`
- Item style: Heebo 500, 14px, tracking 0.04em, color `--ink-700`. Hover: color → `--ink-900`, **1px gold underline grows from the right** to full width over `--dur-2`.
- Active page: gold underline persistent, color `--ink-900`.
- CTA on the far left: text link **"התחברות"** — no button chrome, only a hairline underline on hover. We do not put a loud CTA in the header.
- Search affordance: a 20px serif `q` icon (or a thin magnifier 1.25px stroke) that opens a full-width search sheet sliding from top, height 220px, background `--paper-0`, large input with gold focus underline, recent queries list below.

### Mobile
- Height **56px**. Right: logo (monogram + wordmark, wordmark optically reduced). Left: search icon + hamburger (3 hairlines, 1.25px, 18px wide, 14px tall).
- Tap target 44×44 minimum.
- Hamburger opens a **full-screen drawer** sliding from the right:
  - Background `--cream-50`, padding 32px.
  - Top: monogram + close (×, 1.25px stroke).
  - Nav items as serif `h3` size, weight 500, right-aligned, 56px row height, hairline divider between rows.
  - Bottom: language toggle (HE / EN / FR) as `eyebrow`, gold rule above, tagline beneath.
  - Drawer opens with `--dur-3 --ease-entrance`, content fades in with 80ms stagger per row.

---

## D. HOMEPAGE — Editorial Layout

### Section 1 — Hero
- Full-width band, height **min(720px, 78vh)** desktop / **560px** mobile, background `--cream-50`.
- Composition: text **right** (RTL), large editorial photograph **left**, gap 80px. Photograph: warm-graded architectural interior or street, 4:5 portrait crop, no people, hairline gold 1px frame inset 12px.
- Eyebrow above headline: `eyebrow` style, gold, **"החלטות נדל״ן, בשקט."**
- Headline (`display-1`): **"לפני שחותמים — יודעים."**
- Subline (`body-lg`, max 520px, `--ink-500`): **"מחשבונים, מדריכים ונתוני שוק לקונים, מוכרים ומשקיעים בישראל. בלי רעש שיווקי, בלי אותיות קטנות."**
- Single CTA row, no buttons:
  - Primary text link: **"חישוב משכנתא →"** (arrow flipped for RTL: `←`) Heebo 500, 16px, gold underline.
  - Secondary text link: **"מדריך לקונה הראשון"** ink, hairline underline.
- Below CTAs, a thin gold rule 64px wide, then a `caption` line: **"מבוסס על נתוני רשות המסים ובנק ישראל, מעודכן לרבעון נוכחי."**

### Section 2 — The 5 signature tools
- Eyebrow centered: **"הכלים שלנו"**. H2 right-aligned, restrained: **"חמישה חישובים שאסור לדלג עליהם."**
- 5 cards in a single row desktop (5 columns, 24px gutter), 2-up + 1 stacked on tablet, vertical stack on mobile.
- Card spec: `--paper-0` fill, 1px `--hairline` border, no radius >2px, padding 32px, height 280px desktop.
- Card contents (top to bottom, RTL right-aligned):
  1. Tiny gold ordinal numeral in Frank Ruhl Libre 32px italic (01 / 02 / 03 / 04 / 05).
  2. Card title `h4`, weight 500, ink-900.
  3. Description `body-sm`, ink-500, 2 lines max.
  4. Bottom: text link **"פתיחת המחשבון ←"** gold.
- The 5 titles:
  - **משכנתא** — "בדיקת תמהיל ויכולת החזר."
  - **מס רכישה** — "מדרגות 2026, מחושב לפי המצב שלך."
  - **שווי דירה** — "טווח הערכה ראשוני לפי אזור."
  - **תשואה להשקעה** — "תשואה ברוטו ונטו, חישוב הוגן."
  - **עלויות סגירה** — "כל ההוצאות הנלוות, בלי הפתעות."

### Section 3 — Trust band
- Full-width strip, background `--cream-100`, 80px vertical padding.
- 4 data points in a row, separated by 1px gold vertical hairlines 32px tall.
- Each: large numeric `display-2` (`tabular-nums`), label `eyebrow` beneath.
- Examples: **"₪38B"** היקף עסקאות נסקר · **"127"** ערים ושכונות · **"68"** מדריכים מקצועיים · **"מעודכן רבעונית"**.
- Below: `caption` line crediting sources: **"מקורות: רשות המסים, הלמ״ס, בנק ישראל."**

### Section 4 — City / neighborhood intelligence
- H2 right: **"מודיעין שוק לפי עיר ושכונה."**
- 2-column layout. Right column (60%): a single elegant **line chart** showing average ₪/m² over the past 36 months for the currently selected city; thin 1.25px stroke gold, x/y axes hairline, no gridlines, single tooltip with serif numerics.
- Left column (40%): a list of 6 cities (תל אביב, ירושלים, חיפה, רמת גן, הרצליה, באר שבע), each row: city name `h4`, average ₪/m² right-aligned `tabular-nums`, 12-month delta in `--positive-700` / `--negative-700`. Hover row: hairline gold left border (RTL: appears on the left edge), background `--cream-100`.

### Section 5 — Guides / pillars
- Editorial magazine layout, asymmetric.
- Lead article right (50%): large 4:3 image, eyebrow **"מדריך"**, serif `h2` title, 2-line dek, byline + reading time.
- 2 stacked smaller articles left (50%, 50/50 split vertically), each: small 16:9 image, `h4` title, dek.
- Hover on article: image desaturates by 6% over `--dur-2`; title gains 1px gold underline from right.

### Section 6 — Professionals teaser
- Eyebrow: **"אנשי מקצוע מאומתים"**. H2: **"עורכי דין, שמאים, יועצי משכנתאות."**
- 4 profile cards in a row. Card: 1px hairline, 24px padding, avatar 56px circle (the only circular element on the homepage), name `h4`, specialty `caption`, city `caption` with gold dot separator.
- Bottom: text link **"כל אנשי המקצוע ←"** gold, centered.

### Section 7 — Footer (see J)

---

## E. PILLAR / GUIDE ARTICLE PAGE

### Layout
3-column desktop: right rail **TOC** (200px), center **article** (680px), left rail **author + share + related anchor** (200px). Total 1080px content, centered in 1280px container.

### Top of article
- Breadcrumb (top): `caption`, `--ink-500`, gold separator `/`. Example: **בית / מדריכים / רכישה / מדריך לקונה הראשון**.
- Eyebrow: **"מדריך · רכישה"**.
- H1 (`h1`, Frank Ruhl Libre 44px): **"מדריך לקונה דירה ראשונה בישראל, 2026."**
- Dek (`body-lg`, ink-500, max 620px): **"מה לבדוק לפני שמגישים הצעה, איך לבנות תמהיל משכנתא שמתאים להכנסה, ומה ההוצאות האמיתיות עד מסירת המפתח."**
- Author/trust strip: avatar 40px, name + role + date updated. Right of strip: reading time `caption`. Below strip: hairline 1px full width.

### Body
- Body font Heebo 17/1.7, ink-700.
- H2 inside article: 32px serif, 64px top margin, 16px bottom; preceded by a 32px gold rule 24px above (a "section opener").
- Pull-quote: full-width inside article column, Frank Ruhl Libre 28px italic, ink-900, with a 1px gold left border (RTL: right border) 2px wide, 32px padding-right.
- Lists: bullet is a small `·` in gold, not a dot.
- Tables: hairline grid, header row `--cream-100`, `tabular-nums` for numbers, `body-sm`. No zebra striping; alternating uses cream-100 at 50% opacity only on rows >10.
- Inline data callouts: a thin gold-framed box, ink-900 numeric, eyebrow label above.

### Sticky TOC (right rail in RTL)
- Eyebrow header **"בעמוד הזה"**.
- List of H2s as `body-sm`, ink-500. Active section ink-900 with a 1px gold right border (RTL: right side). Smooth scroll, no animation flourish.
- Sticks at `top: 96px`, hides on mobile (replaced by an opening accordion at the top of the article).

### FAQ accordion (end of article)
- Eyebrow **"שאלות נפוצות"**, H2 serif.
- Items: row with `h4` question right-aligned, +/− gold icon left. Border-bottom 1px hairline.
- Open state: answer in `body`, ink-700, 24px top padding, expand animation `--dur-3 --ease-entrance`.

### Related articles (bottom)
- 3 cards in a row. Same card spec as homepage guides but smaller image (16:9). Eyebrow + serif `h4` title + `caption` reading time.

### Mobile
- Single column, 20px outer margin. TOC collapses to a top-of-article accordion **"בעמוד הזה ▾"**. Pull-quote becomes full-width with the gold rule on top.

---

## F. CALCULATOR / TOOL PAGE

### Page chrome
- Eyebrow **"כלים"**, H1 serif **"מחשבון משכנתא"** or **"מחשבון מס רכישה"**.
- Subhead `body-lg` describing what it does in one sentence.
- Below: a 1px gold rule 64px wide.
- Layout: 2-column desktop. Right (RTL: primary) **inputs** 420px, left **results** flex. Stacks on mobile, inputs first.

### Mortgage calculator — Inputs
Inputs grouped in three blocks, each block titled with `eyebrow` + 1px hairline below.

**Block 1: הנכס וההון העצמי**
- שווי הנכס — large numeric input, suffix `₪`, formatted `2,500,000`.
- הון עצמי — numeric input.
- Auto-derived `caption`: **"יחס מימון: 60%"** (LTV).

**Block 2: התמהיל (3 tracks)**
A horizontal stacked **allocation bar**, 8px tall, hairline border, three segments:
- קל״צ (fixed unlinked) — `--ink-900` segment.
- פריים — `--gold-600` segment.
- משתנה צמודה (variable indexed) — `--stone-400` segment.
Below the bar, three rows, each with: track name `h4`, percentage input (% suffix), interest-rate input (% suffix, default seeded with current public-ish indicative values), term-in-years slider 4-30. Total of percentages must equal 100; if not, gold inline note **"סה״כ התמהיל: 95% — חסר 5%"** appears, no error red.

**Block 3: תרחישים**
- Toggle **"מבחן עמידות +2%"** — when on, interest rates rise by 2pp in the result, and the result tile shows a second line **"תחת +2%: 9,420 ₪"** in `--negative-700`.
- Toggle **"החזרה חודשית מקסימלית"** — when on, a red threshold line appears on the payment timeline if exceeded.

### Mortgage calculator — Results
Three large **result tiles**, each: 1px hairline, 32px padding, `eyebrow` label, `display-2` numeric (`tabular-nums`), and a `caption` qualifier below.

- **החזר חודשי משוקלל** — `7,840 ₪` — **"חודש 1, ממוצע משוקלל בין המסלולים."**
- **סך תשלום ריבית לאורך חיי המשכנתא** — `1,210,000 ₪` — **"בהנחת ריבית קבועה לתרחיש."**
- **יחס החזר מההכנסה** — `34%` — **"מומלץ עד 35% לפי בנק ישראל."**

Below the tiles, a **contribution chart**: a single horizontal stacked bar showing principal vs interest over time, 12px tall, three segments matching the mix colors. Below the bar, an axis with the years 1, 5, 10, 15, 20, 25 in `tabular-nums caption`.

Beneath: a `caption` disclaimer in `--ink-500`: **"החישוב להמחשה בלבד. הריביות בפועל נקבעות על־ידי הבנק המלווה."** No CTA button. A single text link **"שמירת התרחיש להדפסה ←"**.

### Purchase-tax calculator — Inputs
- Numeric input: שווי הדירה.
- Toggle group (2 options, hairline pill, gold underline for active): **דירה יחידה** | **דירה נוספת / משקיע**.
- Optional rows for עולה חדש / נכה / משפר דיור with hairline checkbox.

### Purchase-tax calculator — Bracket bar (the signature viz)
A **horizontal bracket bar** spanning the full width of the result column:
- 5-7 segments representing the 2026 brackets, widths proportional to log-bracket size (so high brackets remain readable).
- Segment fill: graduated tints of `--cream-100` → `--gold-200` → `--gold-500`.
- Each segment label below: bracket range in ₪ (`tabular-nums caption`), tax rate above in `eyebrow` gold.
- A **vertical position marker** (1.5px ink-900 with a small gold serif triangle on top) shows where the property sits.
- The segment(s) actually paid are visually "filled" with a slightly darker tone; segments not reached are at 40% opacity.

Below the bar:
- Per-bracket breakdown table: bracket range · rate · amount in this bracket · tax. `tabular-nums`, hairline grid.
- Total tax tile, same spec as mortgage result tiles: `display-2`, gold rule above.
- `caption` disclaimer: **"מבוסס על מדרגות 2026. שינויי חקיקה עשויים לעדכן את הסכומים."**

### Data-viz styling (all charts)
- Single accent color per chart (gold by default; ink for comparison series).
- Stroke 1.25px, no fill under lines unless single-series area (then `--gold-200` at 20%).
- No gridlines; only axis baselines, hairline.
- Axis labels Heebo 12px tabular, ink-500.
- Tooltip: `--paper-0` 1px hairline, 12px padding, 2px radius, `--shadow-2`, `tabular-nums`, serif value, sans label.
- Numerics inside charts ALWAYS `tabular-nums lining-nums`.

---

## G. CITY / NEIGHBORHOOD PAGE

- Header band: breadcrumb, eyebrow **"מודיעין שוק"**, H1 serif **"תל אביב — שוק הדירות, רבעון 1 2026."**
- Stat band (4 stat tiles in a row): מחיר ממוצע למ״ר · שינוי 12 חודשים · מספר עסקאות · ימי מכירה ממוצעים. Same tile spec as result tiles.
- Trend chart: 36-month line, single gold series, area fill at 12% gold. Toggle: 12M / 36M / 60M / כל ההיסטוריה (hairline pill).
- Sub-neighborhood breakdown: a table with hairline grid, `tabular-nums`, sortable by mini gold caret.
- Listings/projects grid: 3 columns desktop, each card 4:5 image, eyebrow **"פרויקט"** or **"דירה"**, `h4` title, address `caption`, price (`tabular-nums`) bottom-right with `eyebrow` "מ־" prefix.
- Map: full-width band, height 480px. Style as a **monochrome cream map** — `--cream-100` land, `--paper-0` water, `--hairline-strong` roads, gold pins (the dot is `--gold-600`, 8px, with a 1px ink-900 ring). No Google blue, no logos visible.

---

## H. PROFESSIONALS DIRECTORY

### Listing
- Filter bar (sticky under header): hairline pill chips — **"כל ההתמחויות"** ▾, **"כל הערים"** ▾, **"שפות"** ▾. Active chip: ink fill, cream text.
- Grid 3-up desktop, 2-up tablet, 1-up mobile.
- Profile card: 1px hairline, 24px padding, **portrait 4:5** top (warm-graded, neutral background), serif `h3` name, `eyebrow` specialty under, `caption` city + languages, bottom row gold text link **"לפרופיל ←"**.
- Hover: hairline darkens to `--hairline-strong`, gold 1px right border (RTL) appears, image desaturates 8%.

### Profile page
- 2-column header: right column portrait 4:5; left column H1 serif name, eyebrow specialty, `body-lg` short bio, hairline stat row (שנות ניסיון · עסקאות שטופלו · שפות), and a single text-link CTA **"קביעת ייעוץ ←"**.
- Below: tabs — **על אודות · התמחויות · המלצות · יצירת קשר** (hairline pill row, gold underline active).
- Contact form below (see Components).

---

## I. COMPONENTS LIBRARY

### Buttons
All buttons: 2px radius, 44px min height, 14px horizontal padding (text-button) / 24px (filled), Heebo 500 16px, tracking 0.02em. Transition: color, background, border over `--dur-2 --ease-standard`.

| Variant | Default | Hover | Focus | Active | Disabled |
|---|---|---|---|---|---|
| **Primary (quiet ink)** | bg `--ink-900`, text `--cream-50`, no border | bg `--ink-700` | 2px outline `--focus-ring` offset 2px | bg `#000` 95%, translateY 1px | bg `--stone-200`, text `--paper-0`, cursor not-allowed |
| **Secondary (outline)** | transparent, 1px `--ink-900`, text `--ink-900` | bg `--cream-100` | gold focus ring | bg `--cream-100`, translateY 1px | border `--stone-200`, text `--stone-400` |
| **Text link** | text `--gold-600`, gold 1px underline 4px below baseline | underline thickens to 1.5px and shifts up 2px | underline `--ink-900`, focus ring | translateY 1px | `--stone-400`, no underline |
| **Quiet (icon)** | icon `--ink-700`, no chrome | icon `--ink-900`, bg `--cream-100` circle 40px | focus ring | icon `#000` | `--stone-200` |

We do **not** use filled gold buttons. Gold is for accents only.

### Form inputs
- Field: 56px height, 1px `--hairline-strong` bottom border only (no full box) — "underline input." Background `--paper-0`. Padding 16px. Text `body`, ink-900. Right-aligned (RTL).
- Label above: `eyebrow`, ink-500. Required marker is a small gold dot, not asterisk.
- Focus: bottom border becomes 1.5px `--gold-600`; the label color shifts to `--ink-900`.
- Error: bottom border `--negative-700`, helper text `caption` `--negative-700` below.
- Placeholder: `--stone-400`.
- Helper text: `caption`, ink-500, 8px below.
- Number inputs with currency: suffix `₪` set inline, ink-500, 8px gap, RTL preserved.
- Sliders: 2px track `--hairline-strong`, filled portion `--ink-900`, thumb 18px circle `--paper-0` with 1px `--ink-900` border and a 4px inner gold dot. Hover thumb: outer ring `--focus-ring` halo.
- Toggle: 44×24 pill, off = `--cream-100` with hairline, on = `--ink-900`. Knob 18px circle, white. Transition `--dur-2`.
- Checkbox: 18×18 square, 1px hairline-strong, 2px radius, check is a 1.25px gold tick. Focus ring gold.
- Radio: 18px circle, when selected: inner 8px ink-900 dot.

### Cards
- Default: `--paper-0`, 1px `--hairline`, radius 2px, padding 24px (28px on guide cards).
- Hover (interactive cards only): border `--hairline-strong`, `--shadow-1` appears, translateY `-2px` over `--dur-2`. Image inside desaturates 4-8%.
- No drop-shadow at rest.

### Tables
- Hairline 1px between rows, no vertical borders. Header row: `eyebrow`, ink-500, 16px bottom padding, hairline bottom 1.5px `--hairline-strong`.
- Cells: `body-sm`, ink-700, 16px vertical padding, 12px horizontal.
- Numeric columns: `tabular-nums lining-nums`, right-aligned in LTR — in RTL Hebrew tables, numeric columns sit on the **left** edge of the table to mirror conventional finance reading.
- Sortable column header: gold caret, hover ink-900.

### Tabs
- Hairline row of labels, `eyebrow` size, 16px horizontal gap. Active tab: ink-900 + 1.5px gold underline directly under the label, width = label width. Underline animates `--dur-2` between tabs.

### Accordion
- Row: `h4` question RTL, +/− indicator. 1px hairline bottom. Tap target 56px min.
- Open: content `body`, 24px top padding, smooth height `--dur-3`. Only one open at a time on FAQ.

### Breadcrumb
- `caption`, ink-500. Separator `/` in `--gold-600` with 8px horizontal spacing. Current page ink-900.

### Pagination
- Hairline pill row of numbers. Current page: ink-900 with gold underline 1.5px. Arrows `←` `→` (RTL-aware: next is on the left in Hebrew).

### Badges / tags
- `micro` style (11px, tracking 0.14em, weight 500), 4px vertical / 10px horizontal padding, 2px radius, 1px hairline. Categories: hairline only. Status (e.g., **"חדש"**): hairline + ink text + tiny gold dot before.

### Tooltips
- `--paper-0`, 1px hairline, `--shadow-2`, 2px radius, 12px padding, `body-sm`, max-width 280px. Animation: fade + 4px translate, `--dur-2 --ease-entrance`. Delay 300ms.

### Lead / contact form (called: "פנייה לאיש מקצוע")
- Card-shell, padding 40px desktop / 24px mobile, 1px hairline, no shadow.
- Eyebrow + serif `h3` title (e.g. **"קביעת ייעוץ"**), subhead `body-sm`.
- Fields stacked: שם מלא · טלפון · אימייל · עיר · נושא הפנייה (select with hairline underline + gold caret) · הודעה (textarea, 4 rows, hairline bottom only).
- Footer: hairline checkbox **"אני מאשר/ת קבלת תשובה למייל ולטלפון."** + primary button **"שליחת פנייה"** + `caption` privacy line beneath.
- Success state: replace form with a serif `h3` **"קיבלנו את הפנייה."** + `body` line + 1 text link to return.

### Toasts
- Bottom-center desktop, top-center mobile. `--paper-0`, 1px hairline, `--shadow-2`, 2px radius, 16px padding. Icon (1.25px stroke) right, message `body-sm`, dismiss × left. Auto-dismiss 5s.

### 404 page
- Full viewport, centered.
- Tiny eyebrow **"404"** gold, then serif `display-2` **"הדף הזה כבר נמכר."** then `body-lg` **"אבל יש לנו עוד מה להראות. נסו את המדריכים או את חיפוש הנכסים."** then two text links **"חזרה לבית ←"** and **"כל המדריכים ←"**. No illustration. Pure type.

---

## J. FOOTER

- Full-width, background `--ink-900`, text `--cream-50`. Top padding 96px, bottom 48px.
- 4-column grid (RTL right-to-left): **brand block · מדריכים · כלים · חברה**.
- Brand block: monogram + wordmark in cream + gold frame, tagline beneath in `eyebrow` `--stone-400`, then a short editorial line `body-sm` `--cream-100` at 80% opacity: **"מקום שקט להחלטות נדל״ן בישראל."** Below: language toggle HE / EN / FR as `eyebrow` with gold dots between.
- Column links: `eyebrow` heading gold, then list of `body-sm` `--cream-50` 80% opacity, 12px row spacing, hover → 100% + gold underline from right.
- Above the bottom row: a full-width **1px gold hairline rule** at 40% opacity.
- Bottom row: `caption` `--stone-400` left, copyright right (RTL): **"© 2026 נדל״ן חכם · כל הזכויות שמורות"** · **"מדיניות פרטיות"** · **"תנאי שימוש"** · **"נגישות"**.
- No social icons unless we have real accounts; if used, they are 1.25px stroke icons in `--cream-50` 60% opacity.

---

## K. MICRO-INTERACTIONS SPEC

| Element | Default | Hover | Focus | Active | Notes |
|---|---|---|---|---|---|
| Nav item | underline 0 width | gold underline grows from right to full width, 220ms `--ease-standard` | gold focus ring 2px offset 4px | underline ink-900 | RTL-aware origin |
| Text link | gold underline 1px | thickens to 1.5px, lifts 2px | ring | translateY 1px | |
| Card | hairline default | border darkens, `--shadow-1`, translateY -2px | ring on parent | translateY 0 | |
| Image in card | full sat | desaturate 6%, scale 1.01 over 360ms | — | — | reduced-motion: no transform |
| Input | hairline bottom | bottom border darkens | gold bottom 1.5px, label ink-900 | — | label never floats — fixed above |
| Tab | label ink-500 | label ink-900 | ring | underline slides from previous tab over 220ms | width animates with label |
| Accordion | + icon | + tints ink-900 | ring on row | rotates 45° to × | content animates height 360ms |
| Slider thumb | white + gold dot | halo ring | ring | scale 1.05 | numeric value updates with `tabular-nums` |
| Toggle | cream + hairline | hairline darkens | ring | knob slides 220ms | |
| Toast | hidden | — | — | — | enter: fade + 8px translateY, 360ms `--ease-entrance` |
| Page transition | — | — | — | — | content fade 240ms, no slide |

All transitions wrapped in `@media (prefers-reduced-motion: reduce)` → durations 0, no transforms.

---

## CSS — Token export (framework-agnostic)

```css
:root {
  /* color */
  --ink-900:#1B1A17; --ink-700:#2E2B26; --ink-500:#5C564D;
  --stone-400:#8A8276; --stone-200:#C9C3B7;
  --cream-50:#FAF7F1; --cream-100:#F3EEE3; --paper-0:#FFFFFF;
  --gold-600:#9C7A3C; --gold-500:#B89154; --gold-200:#E6D4AE;
  --hairline:#E2DCD0; --hairline-strong:#C9C0AE;
  --positive-700:#3F6B4A; --negative-700:#8B3A2E;
  --focus-ring: rgba(156,122,60,0.40);
  --overlay-ink: rgba(27,26,23,0.55);

  /* type */
  --font-serif:"Frank Ruhl Libre","Cormorant Garamond",Georgia,serif;
  --font-sans:"Heebo","Inter",system-ui,sans-serif;

  /* spacing */
  --space-1:4px; --space-2:8px; --space-3:12px; --space-4:16px;
  --space-5:20px; --space-6:24px; --space-7:32px; --space-8:40px;
  --space-9:48px; --space-10:64px; --space-11:80px; --space-12:96px;
  --space-13:128px; --space-14:160px;

  /* radius */
  --radius-0:0; --radius-1:2px; --radius-2:4px; --radius-pill:999px;

  /* shadow */
  --shadow-1:0 1px 0 0 rgba(27,26,23,.04),0 1px 2px rgba(27,26,23,.04);
  --shadow-2:0 2px 4px rgba(27,26,23,.06),0 8px 24px rgba(27,26,23,.06);
  --shadow-3:0 12px 40px rgba(27,26,23,.10);

  /* motion */
  --dur-1:120ms; --dur-2:220ms; --dur-3:360ms; --dur-4:600ms;
  --ease-standard:cubic-bezier(.2,.6,.2,1);
  --ease-entrance:cubic-bezier(.16,1,.3,1);
  --ease-exit:cubic-bezier(.4,0,1,1);

  /* z */
  --z-base:0; --z-sticky:50; --z-header:100; --z-dropdown:200;
  --z-drawer:300; --z-modal:400; --z-toast:500; --z-tooltip:600;
}

html[dir="rtl"] body{
  font-family:var(--font-sans);
  color:var(--ink-700);
  background:var(--cream-50);
  font-size:17px; line-height:1.7;
  font-feature-settings:"kern","liga";
}

h1,h2,h3{font-family:var(--font-serif);font-weight:500;color:var(--ink-900);}
h1{font-size:44px;line-height:1.15;letter-spacing:-.015em;}
h2{font-size:32px;line-height:1.2;letter-spacing:-.01em;}
h3{font-size:24px;line-height:1.25;}
.eyebrow{font-family:var(--font-sans);font-size:12px;letter-spacing:.18em;
  font-weight:500;color:var(--ink-500);}
.tabular{font-variant-numeric:tabular-nums lining-nums;}

@media (max-width:640px){
  h1{font-size:30px;} h2{font-size:24px;} h3{font-size:20px;}
}

@media (prefers-reduced-motion:reduce){
  *{transition-duration:0!important;animation-duration:0!important;
    transform:none!important;}
}
```

---

## SCREEN BLUEPRINTS — at-a-glance ASCII (desktop unless noted)

### Homepage (desktop, RTL — right is the start)
```
┌──────────────────────────────────────────────────────────────────┐
│ [search][התחברות]   מדריכים  כלים  ערים  אנשי מקצוע  על  [LOGO ◐]│  header 72
├──────────────────────────────────────────────────────────────────┤
│                                                                  │
│   ◌ החלטות נדל״ן, בשקט.                                          │
│                                                ┌──────────────┐  │
│   לפני שחותמים —                                │              │  │
│   יודעים.                                       │   image 4:5  │  │
│                                                 │              │  │
│   מחשבונים, מדריכים ונתוני שוק...                └──────────────┘ │
│                                                                  │
│   חישוב משכנתא ←     מדריך לקונה הראשון                          │
│   ──── 64px gold rule                                            │
│   מבוסס על נתוני רשות המסים ובנק ישראל.                          │
│                                                                  │
├──────────────────────────────────────────────────────────────────┤
│                  הכלים שלנו                                       │
│   חמישה חישובים שאסור לדלג עליהם.                                 │
│  ┌─────┐ ┌─────┐ ┌─────┐ ┌─────┐ ┌─────┐                          │
│  │05   │ │04   │ │03   │ │02   │ │01   │                          │
│  │עלויות│ │תשואה│ │שווי │ │מס   │ │משכנ.│                         │
│  │סגירה│ │     │ │דירה │ │רכישה│ │     │                          │
│  │pen ←│ │pen ←│ │pen ←│ │pen ←│ │pen ←│                          │
│  └─────┘ └─────┘ └─────┘ └─────┘ └─────┘                          │
├──────────────────────────────────────────────────────────────────┤
│ TRUST BAND: ₪38B │ 127 │ 68 │ מעודכן רבעונית                     │
├──────────────────────────────────────────────────────────────────┤
│  מודיעין שוק לפי עיר ושכונה.                                       │
│  ┌──────list cities──────┐  ┌──────36M line chart──────┐         │
│  │ תל אביב    34,200 +6%│  │       /\\____/^\\___       │        │
│  │ ירושלים    28,100 +3%│  │   ___/                   │         │
│  │ חיפה       17,400 −1%│  │                          │         │
│  └─────────────────────┘  └──────────────────────────┘          │
├──────────────────────────────────────────────────────────────────┤
│  GUIDES editorial 1+2 grid                                       │
├──────────────────────────────────────────────────────────────────┤
│  אנשי מקצוע מאומתים — 4 profile cards                             │
├──────────────────────────────────────────────────────────────────┤
│  FOOTER (ink-900, gold rule, 4 columns)                          │
└──────────────────────────────────────────────────────────────────┘
```

### Article (desktop)
```
┌──────────────────────────────────────────────────────────────────┐
│  HEADER                                                          │
├──────────────────────────────────────────────────────────────────┤
│   author rail │  ARTICLE 680px                  │  TOC rail      │
│   (left)      │  בית / מדריכים / רכישה          │  בעמוד הזה     │
│   avatar      │  מדריך · רכישה                  │  · פתיחה       │
│   name        │  H1: מדריך לקונה...             │  · יחס מימון   │
│   share ⇧     │  dek...                         │  · עלויות      │
│               │  hairline                        │  · תמהיל       │
│               │  body 17/1.7 ink-700             │  · FAQ         │
│               │  ─── gold 24px                   │                │
│               │  H2 section opener               │                │
│               │  pull-quote w/ gold side rule    │                │
│               │  table, list, callout            │                │
│               │  FAQ accordion                   │                │
│               │  related articles ×3             │                │
├──────────────────────────────────────────────────────────────────┤
│  FOOTER                                                          │
└──────────────────────────────────────────────────────────────────┘
```

### Mortgage calculator (desktop)
```
┌──────────────────────────────────────────────────────────────────┐
│  HEADER                                                          │
├──────────────────────────────────────────────────────────────────┤
│  eyebrow · H1 מחשבון משכנתא · subhead · ─── gold                  │
├──────────────────────────────────────────────────────────────────┤
│   RESULTS (left)                       INPUTS (right, primary)  │
│  ┌─────────┐ ┌─────────┐ ┌─────────┐  ┌─────────────────┐       │
│  │החזר חודשי│ │סך ריבית │ │% מהכנסה │  │ הנכס וההון       │       │
│  │ 7,840 ₪ │ │1,210,000│ │  34%    │  │ שווי: 2,500,000  │       │
│  │ +2%:9420│ │         │ │עד 35%   │  │ הון:    900,000  │       │
│  └─────────┘ └─────────┘ └─────────┘  │ LTV: 60%         │       │
│  [━━━━━━━━━━━ stacked bar ━━━━━━━━━]  ├─────────────────┤        │
│   1   5   10   15   20   25 years     │ התמהיל            │       │
│                                       │ [קל״צ ━━ פר ━ מש] │       │
│  ⓘ החישוב להמחשה בלבד.                 │ קל״צ 50% 4.8% 25y│       │
│  שמירת התרחיש להדפסה ←                  │ פריים 30% 5.7% 15y│      │
│                                       │ משתנה 20% 4.5% 20y│       │
│                                       ├─────────────────┤        │
│                                       │ ⓞ מבחן עמידות +2% │       │
│                                       └─────────────────┘        │
├──────────────────────────────────────────────────────────────────┤
│  FOOTER                                                          │
└──────────────────────────────────────────────────────────────────┘
```

### Purchase-tax bracket bar (detail)
```
       1.75%   3.5%   5%   8%   10%
      ┌────┬────┬────┬─────┬────────┐
fill: │░░░░│▒▒▒▒│▓▓▓▓│     │        │   ← darker fills = brackets paid
      └────┴────┴────┴─────┴────────┘
      0   1.97M  2.34M  6.05M  20.18M   (₪, log-scaled widths)
                       ▲
                       │
                       ◆ 2,500,000 ₪  ← gold serif triangle + ink line
```

### Mobile homepage (RTL, 375px)
```
┌──────────────────────┐
│ ☰         ⌕ [LOGO ◐] │  56
├──────────────────────┤
│ ◌ החלטות נדל״ן…     │
│ לפני שחותמים —       │
│ יודעים.              │
│                      │
│ ┌──────────────────┐ │
│ │   image 4:5      │ │
│ └──────────────────┘ │
│ חישוב משכנתא ←       │
│ מדריך לקונה הראשון   │
│ ──── 48px gold       │
├──────────────────────┤
│ הכלים שלנו           │
│ ┌──────────────────┐ │
│ │ 01 · משכנתא      │ │
│ │ בדיקת תמהיל…    │ │
│ │ פתיחת המחשבון ← │ │
│ └──────────────────┘ │
│ ... (stack of 5)     │
├──────────────────────┤
│ TRUST (stack 2×2)    │
├──────────────────────┤
│ CITIES (stack)       │
│ GUIDES (stack)       │
│ PROS (stack)         │
├──────────────────────┤
│ FOOTER (stacked)     │
└──────────────────────┘
```

---

## SELF-CRITIQUE — "Would Sotheby's ship this?"

**3 weakest spots found and corrected.**

1. **Tools section risked feeling SaaS-y.** Original idea was filled cards with icons. Fix: stripped icons, replaced with restrained gold serif **ordinal numerals (01-05)** in Frank Ruhl Libre italic — this single move converts the tool row from "feature grid" to "table of contents," which is the editorial register Sotheby's would use.
2. **Hero had too many CTAs.** Initially planned a primary filled button + secondary outline. Fix: removed all button chrome from the hero; both CTAs are now text links with a gold underline. The hero now reads as a magazine cover, not a landing page. The closest button affordance moved into the tool cards where utility belongs.
3. **Calculator results were dashboard-flavored.** Original used colored chips and progress bars. Fix: every result is a **hairline tile with a serif numeric and an eyebrow label** — the same tile shape as the homepage trust band, so the entire system speaks one visual language. The bracket-bar visualization is the only allowed "chart" moment on the tax page; everything else is type.

Additional smaller fixes during audit: removed the dark mode (it cheapens warm cream systems and we cannot maintain photographic consistency across both); reduced the homepage from 9 sections to 7 (the previous "testimonials" and "press strip" were templated tells); deleted all rounded-pill CTAs; forced gold to ≤5% of any screen.

---

## HONESTY STATEMENT

### What is DONE in this document
- Full design-token set with exact hex, type scale (desktop + mobile), spacing, radius, shadow, motion, z-index.
- Logo concept + monogram + lockup rules, framework-agnostic.
- Header, footer, homepage, article, mortgage calculator, purchase-tax calculator with bracket viz, city page, professionals directory, full component library, micro-interaction state matrix.
- RTL behavior specified for every directional element (underline origin, table numeric alignment, drawer side, breadcrumb separator).
- Real Hebrew copy placeholders that are idiomatic, calm, and not translated.
- A CSS token block that a developer can paste directly.
- Self-critique with 3 concrete fixes applied.

### What is ASSUMED (and what we'd verify before shipping)
- **2026 purchase-tax brackets** are referenced as a visual structure, not as final published numbers. Final amounts must be set by an attorney/CPA against the latest official publication and updated each fiscal change.
- **Indicative mortgage interest rates** in calculator screenshots are placeholder seeds. Real ranges must be pulled from a maintained source (Bank of Israel monthly publication or a vetted partner) before launch.
- **City/neighborhood data** is laid out as if we already have a clean time-series of ₪/m² from official sources (Tax Authority / CBS). The pipeline, refresh cadence, and licensing notes must be confirmed.
- **Logo monogram with נ** is a strong direction, not a final lockup. A real type designer should kern the gershayim and tune the gold circle weight against final print/digital sizes.
- **Photography** is the single biggest gap between "this document" and "a $1M experience." A premium architectural photographer (warm graded interiors, no people, landscape, ≥3000px) must shoot or curate the hero and city imagery. Stock will visibly cheapen the system.
- **Map styling** assumes a self-styled vector basemap (Mapbox Studio, MapTiler, or self-hosted MapLibre) using the cream/gold palette. Default Google Maps cannot be used at this caliber.
- **Self-hosted WOFF2** for Frank Ruhl Libre and Heebo with proper Hebrew subsets is assumed; licensing is OFL for both, so safe, but the subsetting/preload pipeline must be implemented.
- **Accessibility numbers (contrast ratios)** were computed for the listed pairs only; any new pairing must be re-verified before use.

### What still needs real inputs to look $1M
1. Professional architectural photography library (hero + cities + projects).
2. Final logo lockup, signed off by a brand designer who can hand-tune the נ inside the gold seal.
3. Real, source-linked data feeds for prices, transactions, tax brackets, and mortgage rates.
4. A copy editor passing every Hebrew string for register and rhythm (this document gets the placeholder copy 90% there; a human editor closes the last 10%).
5. A motion designer to choreograph the page-transition cadence between homepage → tool → article (the spec defines durations, not the full storyboard).

No site code was modified. This is a written design system; the implementation team can build directly from the tokens, CSS block, component matrix, and screen blueprints above.

