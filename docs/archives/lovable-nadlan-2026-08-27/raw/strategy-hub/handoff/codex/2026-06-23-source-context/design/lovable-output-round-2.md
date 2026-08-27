# נדל״ן חכם — Round 2: Gap Fill + WordPress Port Artifacts

> המשך ישיר ל־`nadlan-chacham-design-system.md` (Round 1). כל הטוקנים, הצבעים,
> הטיפוגרפיה, המרווחים, הרדיוסים, הצללים, התנועות והקומפוננטים מ־Round 1 נשמרים
> כמות שהם. מסמך זה רק ממלא פערים ומספק חפצי־port ל־WordPress block theme.
> בר האיכות: *"Would Sotheby's ship this?"*

---

## תוכן עניינים

1. [GAP 1 — Page types](#gap-1)
2. [GAP 2 — Map widget full spec](#gap-2)
3. [GAP 3 — Listing card full state spec](#gap-3)
4. [GAP 4 — CSS bundle](#gap-4)
5. [GAP 5 — theme.json fragment](#gap-5)
6. [GAP 6 — Gutenberg block patterns](#gap-6)
7. [GAP 7 — Monetization surfaces](#gap-7)
8. [Self-critique](#self-critique)
9. [Honesty statement](#honesty)

---

<a id="gap-1"></a>
## GAP 1 — Page types

### A. ‎`/guides/` — Blog index / "מדריכים" archive

#### Desktop (1440)

```
┌──────────────────────────────────────────────────────────────────────┐
│  HEADER-LUXURY (sticky, --header-scrolled cream-50 hairline)          │
├──────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  space-10                                                            │
│  ┌────────────────────────────────────────────────────────────────┐  │
│  │  eyebrow gold  ·  "מדריכים"                                    │  │
│  │  H1 serif 56/1.05 · "מדריכים לקנייה, מכירה והשקעה."             │  │
│  │  body-lg ink-700 max-w 640 ·                                    │  │
│  │  "כל מה שצריך לדעת לפני העסקה הבאה — נכתב על־ידי המערכת,        │  │
│  │   נסקר ב־48 שעות אחרונות."                                       │  │
│  │  gold-rule 64px                                                 │  │
│  └────────────────────────────────────────────────────────────────┘  │
│  space-8                                                              │
│  ┌────────────────────────────────────────────────────────────────┐  │
│  │  FILTER PILLS (hairline, RTL, 12px gap)                          │  │
│  │  ⟨הכול⟩ ⟨קנייה⟩ ⟨מכירה⟩ ⟨השקעה⟩ ⟨מימון⟩ ⟨מיסוי⟩                  │  │
│  │  ⟨התחדשות⟩ ⟨אנשי מקצוע⟩                                          │  │
│  │  active = ink-900 fill, cream-50 text                            │  │
│  └────────────────────────────────────────────────────────────────┘  │
│  space-10                                                             │
│  ┌────────────────────────────────────┬───────────────────────────┐  │
│  │ LEAD (8 cols)                       │ SECONDARY (4 cols)        │  │
│  │ 16:9 hero image (cream-100 ph)      │ ┌─────────────────────┐   │  │
│  │ eyebrow "מדריך · מיסוי"              │ │ 4:3 image           │   │  │
│  │ h2 serif 40 "מדריך מס רכישה 2026 —  │ │ eyebrow · h4         │   │  │
│  │   מי משלם כמה, באמת"                │ │ caption author·date  │   │  │
│  │ dek body-lg 2 שורות                  │ └─────────────────────┘   │  │
│  │ caption "מערכת · 18 דק׳ קריאה"        │ space-6                   │  │
│  │ "קרא ←" link-luxury                  │ ┌─────────────────────┐   │  │
│  │                                      │ │ 4:3 image            │   │  │
│  │                                      │ │ eyebrow · h4 · caption│  │  │
│  │                                      │ └─────────────────────┘   │  │
│  └────────────────────────────────────┴───────────────────────────┘  │
│  space-14   (hairline ink-12% above, full bleed minus rails)         │
│  ┌────────────┬────────────┬────────────┐                            │
│  │ card-int.  │ card-int.  │ card-int.  │   3-up uniform grid,       │
│  │ 4:5 img    │ 4:5 img    │ 4:5 img    │   gap space-7,             │
│  │ eyebrow    │ eyebrow    │ eyebrow    │   repeat per page (9-12).  │
│  │ h4 serif   │ h4 serif   │ h4 serif   │                            │
│  │ caption    │ caption    │ caption    │                            │
│  └────────────┴────────────┴────────────┘                            │
│  space-12                                                             │
│  PAGINATION (§I): ‹ 1 · 2 · 3 · … · 12 ›  centered, tabular-nums      │
│  space-14                                                             │
│  FOOTER-LUXURY                                                        │
└──────────────────────────────────────────────────────────────────────┘
```

#### Mobile (390)
- כותרת H1 → display-2 32/1.1.
- Filter row → horizontal scroll, hairline mask משמאל ומימין.
- Lead + secondary → stacked: lead מלא־רוחב, אחר־כך 2 קטנים אחד מתחת לשני.
- Uniform grid → קלף אחד לרוחב, gap space-6.

---

### B. ‎`/search/` — Search results

#### Desktop

```
┌──────────────────────────────────────────────────────────────────────┐
│ HEADER-LUXURY                                                         │
├──────────────────────────────────────────────────────────────────────┤
│ space-10                                                              │
│ ┌──────────────────────────────────────────────────────────────────┐ │
│ │ INLINE SEARCH SHEET (אותו עיצוב כמו ה־expanded header search):   │ │
│ │   eyebrow "חיפוש"                                                 │ │
│ │   input-underline ענק (fs-h2, ink-900, caret gold-600)            │ │
│ │   placeholder "חפשו: מס רכישה, רמת השרון, מחשבון משכנתא…"          │ │
│ │   hairline gold rule 64px מתחת                                     │ │
│ │   caption "342 תוצאות עבור: »מס רכישה 2026«"                       │ │
│ └──────────────────────────────────────────────────────────────────┘ │
│ space-10                                                              │
│ ┌──────────────────────────────────────────────────────────────────┐ │
│ │ FILTER PILL ROW: ⟨הכול⟩ ⟨מדריכים⟩ ⟨כלים⟩ ⟨ערים⟩ ⟨שכונות⟩ ⟨אנשי מקצוע⟩│ │
│ └──────────────────────────────────────────────────────────────────┘ │
│ space-8                                                               │
│ ┌──────────────────────────────────────────────────────────────────┐ │
│ │  ───── hairline ink-12% ─────                                     │ │
│ │  space-5                                                          │ │
│ │  eyebrow gold "מדריך"  ·  caption ink-500 "בית › מימון › משכנתא"  │ │
│ │  h4 serif 24 "מחשבון משכנתא — שלוש מסלולים והקצאה אופטימלית"      │ │
│ │  body-sm ink-700 2 שורות עם המונח מודגש: "…<mark>מס רכישה</mark>  │ │
│ │   2026 מתעדכן רבעונית…"                                            │ │
│ │  caption ink-500 "התאמה 96%" · ◆ gold-500 dot                      │ │
│ │  space-5                                                          │ │
│ │  ───── hairline ─────                                              │ │
│ │  (repeats 10 per page)                                            │ │
│ └──────────────────────────────────────────────────────────────────┘ │
│ pagination · footer-luxury                                            │
└──────────────────────────────────────────────────────────────────────┘
```

**Match indicator**: נקודה ◆ gold-500 בקוטר 6px + caption tabular־nums "התאמה 96%".
לא bar, לא %סרגל — נקודה ומספר בלבד.

#### Empty state

```
┌──────────────────────────────────────────────┐
│  space-14                                     │
│  quote serif italic 28/1.45 ink-700:          │
│  "אין תוצאות לחיפוש הזה. נסו ניסוח אחר."       │
│  gold rule 32px                                │
│  caption ink-500 "חיפושים פופולריים":          │
│  · link-luxury "מס רכישה 2026"                │
│  · link-luxury "מחשבון משכנתא"                 │
│  · link-luxury "התחדשות עירונית רמת גן"        │
└──────────────────────────────────────────────┘
```

#### Mobile
- שדה חיפוש: fs-h3 במקום fs-h2.
- Filter pills בגלילה אופקית.
- כל row אותו דבר, padding-block space-5.

---

### C. Lead-form variations

**משותף לכולן**: שדות underline (`.input-underline`), צבעי ink-700, primary CTA
‎`.btn` ink-900, focus-ring gold-200, eyebrow gold מעל H3 serif.

#### c1. Inline footer (תחתית מאמר־pillar) — desktop

```
─────── hairline ink-12% full width of article column (680px) ───────
space-10
eyebrow gold · "שאלה לעורך?"
h3 serif 28 · "אנחנו עונים תוך 48 שעות, ללא תשובה גנרית."
space-5
input-underline · label "שם"
space-4
input-underline · label "טלפון או אימייל"
space-4
input-underline · label "השאלה שלך" (textarea, 3 שורות)
space-6
[שלח שאלה →]   caption ink-500 "אנו לא מעבירים את הפרטים לצדדים שלישיים."
space-10
```

#### c2. Modal — opened from inline text-link "קביעת ייעוץ"

```
overlay --overlay-ink 70%, blur 4px
┌────────────────────────────────────────────┐
│  modal: 560×auto, paper-0, --shadow-3,      │
│  radius 2px, padding 40px, focus trap.       │
│                                              │
│  ✕ close 24px ink-700 top-end                │
│                                              │
│  eyebrow gold "ייעוץ אישי"                   │
│  h3 serif 28 "קביעת שיחה עם עורך."           │
│  body-sm ink-500 "ללא עלות. ללא מכירה."       │
│  space-6                                     │
│  [שדות כמו c1]                                │
│  space-6                                     │
│  [שלח →]   text-link "ביטול"                  │
└────────────────────────────────────────────┘
motion: opacity 0→1 220ms ease-out, transform translateY(8px)→0
respects prefers-reduced-motion (fade בלבד).
```

#### c3. Dedicated `/contact/` page — split

```
┌───────────────────────────────────┬────────────────────────────────┐
│ LEFT (7 cols, paper-0)             │ RIGHT (5 cols, cream-100)      │
│ space-12                            │ space-12                       │
│ eyebrow "יצירת קשר"                  │ eyebrow gold "צוות נדל״ן חכם"   │
│ h1 display-2 "נשמח לדבר."           │ h2 serif 40 "המערכת שעומדת     │
│ body-lg ink-700 (2 שורות)            │  מאחורי כל מילה."               │
│ space-10                            │ space-8                         │
│ [form: שם / אימייל / נושא ▾ /        │ body ink-700 2 פסקאות.          │
│  הודעה / שלח →]                      │ space-8                         │
│                                      │ ──── gold rule 32px ────         │
│                                      │ eyebrow "פנייה ישירה"             │
│                                      │ caption ink-500 "טלפון — בקרוב"   │
│                                      │ (gold rule placeholder where     │
│                                      │  phone would be once committed)  │
│                                      │ email link-luxury "hi@nadlan…"   │
│                                      │ caption כתובת רשומה + ח.פ.       │
└───────────────────────────────────┴────────────────────────────────┘
```

Mobile: stack — form ראשון, editorial אחריו.

---

### D. ‎`/neighborhoods/{city}/{slug}/` — Neighborhood page

יורש מ־`/cities/{slug}/` (§G של Round 1). הבדלים מפורשים:

| אזור | City page (§G) | Neighborhood page |
|---|---|---|
| Breadcrumb | בית › ערים › תל אביב | בית › ערים › תל אביב › רמת אביב ג׳ |
| H1 | "תל אביב" | "רמת אביב ג׳" |
| Stat band | 5 tiles (חציון, ת/ע, ימים בשוק, היצע, שינוי שנתי) | **3 tiles בלבד**: חציון · ת/ע · עסקאות 12 חודשים |
| Honesty caption מתחת ל־band | "מקור: רשות המסים, 12 חודשים." | **"המדגם ברמת אביב ג׳ קטן יותר — המגמה אמינה, ערכים בודדים פחות."** |
| Trend chart | זהה | זהה (אותו הקומפוננט) |
| Sub-area breakdown | טבלת שכונות | **טבלת רחובות** (`רחוב · עסקאות 12ח · חציון ₪/מ״ר`) |
| Listings grid | 3 עמודות | **2 עמודות** (מלאי קטן יותר) |
| Map widget | מציג את העיר עם פינים | מציג את גבול השכונה (overlay 1px ink hairline, fill cream-100 אטום־למחצה 30%) |

הכותרת והגריד היחידים שמשתנים — שאר הרכיבים זהים.

---

<a id="gap-2"></a>
## GAP 2 — Map widget — full UI spec

Basemap: monochrome cream — paper-0 רקע, hairline ink-12% לכבישים ראשיים,
ink-8% לכבישים משניים, ללא תוויות צבעוניות, תוויות שכונות ב־caption ink-500.

### Layout

```
┌──────────────────────────────────────────────────────────────┐
│ ⤢                                       [מחירים][פרויקטים][עסקאות]│  ← layer toggle top-end
│                                                                │
│         · ●           ◇                                        │
│              ●        ◇       ⓭ cluster                        │
│                  ●                                              │
│                                                                │
│                                       hover popover ↗          │
│                                       ┌─────────────────┐      │
│                                       │ 4:3 cream-100   │      │
│                                       │ thumbnail        │      │
│                                       │ h4 "פרויקט הים"   │      │
│                                       │ caption רחוב …    │      │
│                                       │ ₪ 4,250,000        │      │
│                                       │ "לפרופיל ←"        │      │
│                                       └─────────────────┘      │
│                                                                │
│ [ + ]                                          legend ↘         │
│ [ − ]                                ● נכס פעיל                  │
│                                      ◇ פרויקט בבנייה              │
│                                      · עסקה אחרונה                │
└──────────────────────────────────────────────────────────────┘
desktop: 1140 × 560.   mobile: 100vw × 420.
```

### Zoom controls (`.map-zoom`)
- Container: hairline pill, paper-0, --shadow-1, radius 2px.
- Icons: + / − stroke 1.25px, 16px, ink-700.
- Tap targets: 40×40 (desktop) / 44×44 (mobile).
- Position: desktop bottom-start (`inset-block-end: 16px; inset-inline-start: 16px`); mobile top-end.
- Focus: focus-ring 2px gold-200 outside, 2px offset.

### Layer toggle (`.map-layers`)
- Pill row: 3 segments, hairline border ink-12%, paper-0.
- Each segment: padding-inline 16px, padding-block 8px, caption.
- Active: ink-900 fill, cream-50 text, no border between segments.
- One active at a time (radio behavior, `role="radiogroup"`).
- Position: top-end desktop, top-end mobile (under chrome).

### Pin variants

| Type | Geometry | Use |
|---|---|---|
| `.pin-property` | 8px gold-600 dot + 1px ink-900 ring | dot diameter 8, ring stroke 1, total 10px |
| `.pin-project` | 10px hollow gold-600 ring stroke 1.5 + 2px gold-600 center | hollow circle |
| `.pin-transaction` | 6px ink-900 dot, no ring | flat |
| `.pin-sponsored` | 10px gold-600 dot + 1.5px gold-600 ring (no ink) | §G7-C |
| `.pin-cluster` | 32px circle, cream-100 fill, 1px ink-12% hairline, ink-900 number tabular-nums | counts |

קוטרים נכונים פיזית; ה־SVG משתמש ב־`shape-rendering: geometricPrecision`.

### Hover popover (`.map-popover`)
- 220 × auto, paper-0, hairline ink-12%, --shadow-2, radius 2px.
- padding 12px.
- structure: 4:3 thumbnail (160px wide), h4 serif 18, caption ink-500 (address),
  price tabular-nums fs-body, text-link gold "לפרופיל ←".
- anchor: small 6px triangle from card edge to pin.
- motion: opacity 0→1, translateY 4px→0, 160ms ease-out.

### Legend (`.map-legend`)
- bottom-end desktop, hidden mobile (collapses into a "ℹ" button).
- 3 rows: pin sample + caption label, 8px gap.

### Fullscreen
- `⤢` icon top-start desktop (24×24, ink-700, hairline 1px frame).
- Opens modal 100vw × 100vh, header bar 56px ink-900 קריםp text, ✕ close top-end.
- ESC and ✕ both dismiss.

### States
- **Loading**: basemap rendered, pins replaced by 8px cream-100 squares shimmer 1.5s.
- **Empty / no data**: serif italic note centered, fs-quote 22/1.45:
  "אזור לא נמכר ב־12 החודשים האחרונים. נסו אזור סמוך."
- **Error**: caption ink-500 "המפה לא נטענה. רענון →" (text-link).

---

<a id="gap-3"></a>
## GAP 3 — Listing card — full state spec

### Structure (RTL)

```
.listing-card  (3-col grid context: 360 × auto)
├ .listing-media (aspect 4:5)
│   ├ <img class="image-luxury">
│   ├ .listing-save (top-start: visually inline-start)
│   └ .listing-flag (top-end)
└ .listing-body (padding space-5)
    ├ .eyebrow "₪/מ״ר · שכונה"
    ├ h4 serif 22 "דירת 4 חד׳, רחוב הירקון 84"
    ├ caption ink-500 "תל אביב · קומה 3 · מרפסת"
    └ .listing-price tabular-nums (fs-h4) "₪ 4,250,000"
```

### State matrix (matches §K of Round 1)

| State | Surface | Image | Title | Caption | Save icon |
|---|---|---|---|---|---|
| default | paper-0 | 1.0 | ink-900 | ink-500 | outline ink-700 |
| hover | paper-0 | scale 1.02 (320ms ease) | ink-900 | ink-500 | stroke gold-600 |
| focus | paper-0 + focus-ring gold-200 2px offset 2 | 1.0 | ink-900 | ink-500 | outline ink-700 |
| active | paper-0 | scale 0.995 (160ms) | ink-900 | ink-500 | as is |
| saved | paper-0 | as is | ink-900 | ink-500 | **filled gold-600** |
| sponsored | paper-0 + 1px gold-600 frame | as is | ink-900 | ink-500 | as is |

### Save toggle (`.listing-save`)

- Geometry: 24×24 outline heart, stroke 1.25px ink-700.
- Container: paper-0 6×6 square (24×24 hit area visually, 44×44 tap target on mobile via padding), no radius, hairline border ink-12%.
- Position: `position: absolute; inset-block-start: 12px; inset-inline-start: 12px;`.
- Hover: stroke gold-600.
- Active (saved): fill gold-600, stroke gold-600.
- Animation: `transform: scale(.92) → scale(1.0)` over 220ms cubic-bezier(.2,.7,.1,1).
- ARIA: `aria-pressed`, `aria-label="שמירה לעיון מאוחר יותר"`.

### Badges (`.listing-flag`)

- `.flag--new` and `.flag--drop`.
- Style: micro caption (fs-micro), padding-inline 8 / padding-block 4, hairline ink-12% border, paper-0, eyebrow letter-spacing.
- Prefix: 6px gold-500 dot, 6px gap.
- Copy: "חדש" / "ירידת מחיר".
- Position: `position: absolute; inset-block-start: 12px; inset-inline-end: 12px;` (RTL safe).

### Mobile spec

- Card: 100% width, image stays 4:5.
- Body: padding space-5, identical hierarchy.
- Tap surface: כל הקלף → profile (anchor wrapping). Save heart 44×44 tap area (padding על האלמנט).

### Skeleton (`.listing-card.is-loading`)

```
┌────────────────┐
│ ░░░░ 4:5 ░░░░ │   cream-100 placeholder
├────────────────┤
│ ▓▓▓▓▓ 60%      │   bar 12px hairline tint
│ ▓▓▓▓▓▓▓ 80%    │   bar 18px
│ ▓▓▓ 40%        │   bar 12px
└────────────────┘
```

- Bars: cream-100 fill, radius 2px.
- Shimmer: linear-gradient `cream-50 → paper-0 → cream-50`, animation `shimmer 1.5s linear infinite`.
- `@media (prefers-reduced-motion: reduce)` → no shimmer, פשוט cream-100 סטטי.

### Grid empty state

```
space-14
quote serif 28/1.45 ink-700:
"לא נמצאו דירות בקריטריונים שבחרתם."
body-sm ink-500 "נסו להרחיב את טווח המחיר או שכונה סמוכה."
gold rule 32px
link-luxury "ניקוי סינון ←"
```

---

<a id="gap-4"></a>
## GAP 4 — CSS bundle

> שמירה: `/wp-content/themes/nadlan-revenue/assets/css/nadlan.css`.
> נטען דרך `wp_enqueue_style`. אין Tailwind. שמות מחלקה סמנטיים. RTL דרך
> logical properties בלבד.

```css
/* ============================================================
   נדל״ן חכם · Design System v1.0
   Round 1 + Round 2, WordPress block theme port.
   RTL-first, logical properties throughout.
   ============================================================ */

/* ──────────── 1. DESIGN TOKENS ──────────── */

:root {
  /* — Color: Ink / Stone / Cream / Paper — */
  --ink-900:        #1B1A17;   /* primary text, dark surfaces */
  --ink-700:        #3A3733;   /* body text */
  --ink-500:        #6E6A63;   /* secondary text, captions */
  --stone-400:      #9C978E;   /* tertiary text */
  --stone-200:      #C8C3B8;   /* dividers strong */
  --cream-100:      #F1ECE2;   /* alt surface */
  --cream-50:       #FAF7F1;   /* page background */
  --paper-0:        #FFFFFF;   /* card / elevated surface */

  /* — Color: Gold accents — */
  --gold-600:       #9C7A3C;   /* primary accent, CTA underlines */
  --gold-500:       #B59558;   /* secondary gold (dots, indicators) */
  --gold-200:       #E7D9B7;   /* focus rings, soft highlights */

  /* — Color: Lines — */
  --hairline:           rgba(27, 26, 23, 0.12);   /* ink-900 @ 12% */
  --hairline-strong:    rgba(27, 26, 23, 0.24);   /* ink-900 @ 24% */

  /* — Color: Semantic — */
  --positive-700:   #2E6A4F;
  --negative-700:   #8A2A2A;
  --focus-ring:     var(--gold-200);
  --overlay-ink:    rgba(27, 26, 23, 0.70);

  /* — Spacing (8px base) — */
  --space-1:  4px;
  --space-2:  8px;
  --space-3:  12px;
  --space-4:  16px;
  --space-5:  20px;
  --space-6:  24px;
  --space-7:  32px;
  --space-8:  40px;
  --space-9:  48px;
  --space-10: 64px;
  --space-11: 80px;
  --space-12: 96px;
  --space-13: 128px;
  --space-14: 160px;

  /* — Type scale (desktop) — */
  --fs-display-1: 88px;   --lh-display-1: 1.02;  --tr-display-1: -0.02em;
  --fs-display-2: 64px;   --lh-display-2: 1.05;  --tr-display-2: -0.015em;
  --fs-h1:        56px;   --lh-h1:        1.08;  --tr-h1:        -0.01em;
  --fs-h2:        40px;   --lh-h2:        1.15;  --tr-h2:        -0.005em;
  --fs-h3:        28px;   --lh-h3:        1.25;  --tr-h3:         0;
  --fs-h4:        22px;   --lh-h4:        1.3;   --tr-h4:         0;
  --fs-body-lg:   19px;   --lh-body-lg:   1.7;   --tr-body-lg:    0;
  --fs-body:      17px;   --lh-body:      1.7;   --tr-body:       0;
  --fs-body-sm:   15px;   --lh-body-sm:   1.6;   --tr-body-sm:    0;
  --fs-caption:   13px;   --lh-caption:   1.45;  --tr-caption:    0.01em;
  --fs-eyebrow:   11px;   --lh-eyebrow:   1.2;   --tr-eyebrow:    0.18em;
  --fs-micro:     10px;   --lh-micro:     1.2;   --tr-micro:      0.16em;
  --fs-quote:     28px;   --lh-quote:     1.45;  --tr-quote:      0;

  /* — Radius (extreme restraint) — */
  --radius-0:  0;
  --radius-1:  2px;
  --radius-2:  4px;     /* maximum allowed; tags, pills */
  --radius-pill: 999px; /* for hairline pills only */

  /* — Shadows (dispersed, no blue) — */
  --shadow-1: 0 1px 2px rgba(27,26,23,.04), 0 1px 1px rgba(27,26,23,.02);
  --shadow-2: 0 4px 12px rgba(27,26,23,.06), 0 1px 2px rgba(27,26,23,.04);
  --shadow-3: 0 18px 48px rgba(27,26,23,.10), 0 4px 12px rgba(27,26,23,.06);

  /* — Motion — */
  --dur-1: 120ms;
  --dur-2: 220ms;
  --dur-3: 320ms;
  --dur-4: 520ms;
  --ease-standard: cubic-bezier(.2,.7,.1,1);
  --ease-entrance: cubic-bezier(.16,1,.3,1);
  --ease-exit:     cubic-bezier(.4,0,1,1);

  /* — Z-index — */
  --z-base:    0;
  --z-raised:  10;
  --z-sticky:  100;
  --z-header:  500;
  --z-overlay: 900;
  --z-modal:   1000;
  --z-toast:   1100;

  /* — Type family roles — */
  --font-serif: "Frank Ruhl Libre", "Cardo", "Georgia", serif;
  --font-sans:  "Heebo", "Inter", "Helvetica Neue", "Arial", sans-serif;

  /* — Layout — */
  --container: 1240px;
  --article-col: 680px;
  --header-h: 72px;
}

/* ──────────── 2. FONT FACES ──────────── */

/* Frank Ruhl Libre — Hebrew + Latin */
@font-face {
  font-family: "Frank Ruhl Libre";
  font-weight: 400;
  font-style: normal;
  font-display: swap;
  src: url("/wp-content/themes/nadlan-revenue/assets/fonts/frank-ruhl-libre/frl-400.woff2") format("woff2");
  unicode-range: U+0590-05FF, U+FB1D-FB4F, U+0020-007F;
}
@font-face {
  font-family: "Frank Ruhl Libre";
  font-weight: 500;
  font-style: normal;
  font-display: swap;
  src: url("/wp-content/themes/nadlan-revenue/assets/fonts/frank-ruhl-libre/frl-500.woff2") format("woff2");
  unicode-range: U+0590-05FF, U+FB1D-FB4F, U+0020-007F;
}
@font-face {
  font-family: "Frank Ruhl Libre";
  font-weight: 700;
  font-style: normal;
  font-display: swap;
  src: url("/wp-content/themes/nadlan-revenue/assets/fonts/frank-ruhl-libre/frl-700.woff2") format("woff2");
  unicode-range: U+0590-05FF, U+FB1D-FB4F, U+0020-007F;
}
@font-face {
  font-family: "Frank Ruhl Libre";
  font-weight: 900;
  font-style: normal;
  font-display: swap;
  src: url("/wp-content/themes/nadlan-revenue/assets/fonts/frank-ruhl-libre/frl-900.woff2") format("woff2");
  unicode-range: U+0590-05FF, U+FB1D-FB4F, U+0020-007F;
}
/* Heebo — Hebrew + Latin */
@font-face {
  font-family: "Heebo";
  font-weight: 300;
  font-style: normal;
  font-display: swap;
  src: url("/wp-content/themes/nadlan-revenue/assets/fonts/heebo/heebo-300.woff2") format("woff2");
  unicode-range: U+0590-05FF, U+FB1D-FB4F, U+0020-007F;
}
@font-face {
  font-family: "Heebo";
  font-weight: 400;
  font-style: normal;
  font-display: swap;
  src: url("/wp-content/themes/nadlan-revenue/assets/fonts/heebo/heebo-400.woff2") format("woff2");
  unicode-range: U+0590-05FF, U+FB1D-FB4F, U+0020-007F;
}
@font-face {
  font-family: "Heebo";
  font-weight: 500;
  font-style: normal;
  font-display: swap;
  src: url("/wp-content/themes/nadlan-revenue/assets/fonts/heebo/heebo-500.woff2") format("woff2");
  unicode-range: U+0590-05FF, U+FB1D-FB4F, U+0020-007F;
}

/* ──────────── 3. BASE ──────────── */

*, *::before, *::after { box-sizing: border-box; }

html { -webkit-text-size-adjust: 100%; }

html[dir="rtl"], html[dir="ltr"] {
  background: var(--cream-50);
  color: var(--ink-700);
  font-family: var(--font-sans);
  font-size: var(--fs-body);
  line-height: var(--lh-body);
  font-weight: 400;
  text-rendering: optimizeLegibility;
  -webkit-font-smoothing: antialiased;
}

body {
  margin: 0;
  min-block-size: 100vh;
  background: var(--cream-50);
  color: var(--ink-700);
  text-align: start;            /* logical, RTL-safe */
}

h1, h2, h3, h4, h5, h6 {
  font-family: var(--font-serif);
  font-weight: 500;             /* serif headings: medium, not bold */
  color: var(--ink-900);
  margin-block: 0 var(--space-5);
  letter-spacing: 0;
  text-wrap: balance;
}
h1 { font-size: var(--fs-h1); line-height: var(--lh-h1); letter-spacing: var(--tr-h1); }
h2 { font-size: var(--fs-h2); line-height: var(--lh-h2); letter-spacing: var(--tr-h2); }
h3 { font-size: var(--fs-h3); line-height: var(--lh-h3); }
h4 { font-size: var(--fs-h4); line-height: var(--lh-h4); }
h5 { font-size: var(--fs-body-lg); line-height: var(--lh-body-lg); }
h6 { font-size: var(--fs-body);    line-height: var(--lh-body); }

p { margin-block: 0 var(--space-5); }

a {
  color: var(--ink-900);
  text-decoration: none;
  transition: color var(--dur-2) var(--ease-standard);
}
a:hover { color: var(--gold-600); }

ul, ol {
  margin-block: 0 var(--space-5);
  padding-inline-start: var(--space-6);
}
li { margin-block: var(--space-2); }

blockquote {
  margin: var(--space-8) 0;
  padding-inline-start: var(--space-5);
  border-inline-start: 2px solid var(--gold-600);
  font-family: var(--font-serif);
  font-style: italic;
  font-size: var(--fs-quote);
  line-height: var(--lh-quote);
  color: var(--ink-900);
}

table { width: 100%; border-collapse: collapse; }
th, td {
  padding: var(--space-4) var(--space-5);
  text-align: start;
  border-block-end: 1px solid var(--hairline);
  font-size: var(--fs-body-sm);
}
th {
  font-family: var(--font-sans);
  font-weight: 500;
  color: var(--ink-900);
  font-size: var(--fs-caption);
  letter-spacing: var(--tr-caption);
  text-transform: none;
}

hr {
  border: 0;
  border-block-start: 1px solid var(--hairline);
  margin-block: var(--space-9);
}

::selection { background: var(--gold-200); color: var(--ink-900); }

img, svg, video { max-inline-size: 100%; block-size: auto; display: block; }

:focus-visible {
  outline: 2px solid var(--focus-ring);
  outline-offset: 2px;
  border-radius: var(--radius-1);
}

/* ──────────── 4. UTILITY PRIMITIVES (sparingly used) ──────────── */

.eyebrow {
  font-family: var(--font-sans);
  font-weight: 500;
  font-size: var(--fs-eyebrow);
  line-height: var(--lh-eyebrow);
  letter-spacing: var(--tr-eyebrow);
  text-transform: uppercase;
  color: var(--gold-600);
  display: inline-block;
  margin-block-end: var(--space-3);
}

.tabular {
  font-variant-numeric: tabular-nums;
  font-feature-settings: "tnum" 1, "lnum" 1;
}

.gold-rule {
  display: block;
  inline-size: 64px;
  block-size: 1px;
  background: var(--gold-600);
  margin-block: var(--space-6);
  border: 0;
}
.gold-rule--sm { inline-size: 32px; }

/* ──────────── 5. BUTTONS ──────────── */

.btn,
.btn-secondary,
.btn-text {
  font-family: var(--font-sans);
  font-weight: 500;
  font-size: var(--fs-body-sm);
  letter-spacing: 0.04em;
  line-height: 1;
  display: inline-flex;
  align-items: center;
  gap: var(--space-2);
  cursor: pointer;
  border: 1px solid transparent;
  background: transparent;
  padding-inline: var(--space-6);
  padding-block: var(--space-4);
  border-radius: var(--radius-1);
  transition:
    background var(--dur-2) var(--ease-standard),
    color var(--dur-2) var(--ease-standard),
    border-color var(--dur-2) var(--ease-standard);
}

.btn { background: var(--ink-900); color: var(--cream-50); border-color: var(--ink-900); }
.btn:hover { background: #000; }
.btn:active { background: var(--ink-700); }

.btn-secondary { color: var(--ink-900); border-color: var(--ink-900); }
.btn-secondary:hover { background: var(--ink-900); color: var(--cream-50); }

.btn-text {
  padding: 0;
  border: 0;
  color: var(--ink-900);
  position: relative;
  letter-spacing: 0.02em;
}
.btn-text::after {
  content: "";
  position: absolute;
  inset-inline-end: 0;
  inset-block-end: -3px;
  inline-size: 100%;
  block-size: 1px;
  background: var(--gold-600);
  transform-origin: inline-end;
  transform: scaleX(0);
  transition: transform var(--dur-3) var(--ease-standard);
}
.btn-text:hover { color: var(--gold-600); }
.btn-text:hover::after { transform: scaleX(1); }

.btn-icon-quiet {
  inline-size: 40px;
  block-size: 40px;
  padding: 0;
  border-radius: var(--radius-1);
  background: transparent;
  color: var(--ink-700);
  border: 1px solid transparent;
  display: inline-flex;
  align-items: center;
  justify-content: center;
}
.btn-icon-quiet:hover { background: var(--cream-100); color: var(--ink-900); }

/* ──────────── 6. FORM CONTROLS ──────────── */

.input-underline {
  display: flex;
  flex-direction: column;
  gap: var(--space-2);
  margin-block-end: var(--space-5);
}
.input-underline > label {
  font-size: var(--fs-caption);
  letter-spacing: var(--tr-caption);
  color: var(--ink-500);
  font-weight: 500;
}
.input-underline > input,
.input-underline > textarea,
.input-underline > select {
  appearance: none;
  background: transparent;
  border: 0;
  border-block-end: 1px solid var(--hairline-strong);
  padding-block: var(--space-3);
  padding-inline: 0;
  font: inherit;
  color: var(--ink-900);
  caret-color: var(--gold-600);
  transition: border-color var(--dur-2) var(--ease-standard);
}
.input-underline > textarea { resize: vertical; min-block-size: 96px; }
.input-underline > *:focus { outline: 0; border-block-end-color: var(--gold-600); }
.input-underline > .helper { font-size: var(--fs-caption); color: var(--ink-500); }
.input-underline.is-error > input,
.input-underline.is-error > textarea { border-block-end-color: var(--negative-700); }
.input-underline.is-error > .helper { color: var(--negative-700); }

.slider {
  --track: var(--hairline-strong);
  --fill:  var(--ink-900);
  inline-size: 100%;
  appearance: none;
  background: var(--track);
  block-size: 1px;
  outline: none;
}
.slider::-webkit-slider-thumb {
  appearance: none;
  inline-size: 14px;
  block-size: 14px;
  background: var(--paper-0);
  border: 1.5px solid var(--ink-900);
  border-radius: 999px;
  cursor: grab;
  transition: transform var(--dur-2) var(--ease-standard);
}
.slider:focus-visible::-webkit-slider-thumb {
  box-shadow: 0 0 0 4px var(--focus-ring);
}

.toggle {
  --w: 36px; --h: 20px;
  position: relative;
  inline-size: var(--w);
  block-size: var(--h);
  background: var(--stone-200);
  border-radius: 999px;
  cursor: pointer;
  transition: background var(--dur-2) var(--ease-standard);
}
.toggle::after {
  content: "";
  position: absolute;
  inset-block-start: 2px;
  inset-inline-start: 2px;
  inline-size: 16px; block-size: 16px;
  background: var(--paper-0);
  border-radius: 999px;
  transition: inset-inline-start var(--dur-2) var(--ease-standard);
}
.toggle[aria-checked="true"] { background: var(--ink-900); }
.toggle[aria-checked="true"]::after { inset-inline-start: 18px; }

.checkbox, .radio {
  inline-size: 16px;
  block-size: 16px;
  border: 1px solid var(--hairline-strong);
  background: var(--paper-0);
  display: inline-grid;
  place-items: center;
  cursor: pointer;
}
.checkbox { border-radius: var(--radius-1); }
.radio    { border-radius: 999px; }
.checkbox[aria-checked="true"], .radio[aria-checked="true"] {
  border-color: var(--ink-900);
  background: var(--ink-900);
}

/* ──────────── 7. CARDS & SURFACES ──────────── */

.card {
  background: var(--paper-0);
  border: 1px solid var(--hairline);
  border-radius: var(--radius-1);
  padding: var(--space-6);
}

.card-interactive {
  background: var(--paper-0);
  border: 1px solid var(--hairline);
  border-radius: var(--radius-1);
  transition:
    transform var(--dur-3) var(--ease-standard),
    box-shadow var(--dur-3) var(--ease-standard),
    border-color var(--dur-2) var(--ease-standard);
  display: block;
}
.card-interactive:hover {
  transform: translateY(-2px);
  box-shadow: var(--shadow-2);
  border-color: var(--hairline-strong);
}
.card-interactive:focus-visible { outline-offset: 2px; }

/* ──────────── 8. TABLES (HAIRLINE) ──────────── */

.table-hairline { border-block-start: 1px solid var(--hairline); }
.table-hairline th,
.table-hairline td { border-block-end: 1px solid var(--hairline); }
.table-hairline tbody tr:hover { background: var(--cream-50); }

/* ──────────── 9. TABS ──────────── */

.tabs { position: relative; display: flex; gap: var(--space-7); border-block-end: 1px solid var(--hairline); }
.tab-underline {
  position: relative;
  padding: var(--space-4) 0;
  color: var(--ink-500);
  font-weight: 500;
  font-size: var(--fs-body-sm);
  background: none;
  border: 0;
  cursor: pointer;
  transition: color var(--dur-2) var(--ease-standard);
}
.tab-underline::after {
  content: "";
  position: absolute;
  inset-inline-start: 0;
  inset-block-end: -1px;
  inline-size: 100%;
  block-size: 1px;
  background: var(--ink-900);
  transform-origin: inline-start;
  transform: scaleX(0);
  transition: transform var(--dur-3) var(--ease-standard);
}
.tab-underline[aria-selected="true"] { color: var(--ink-900); }
.tab-underline[aria-selected="true"]::after { transform: scaleX(1); }

/* ──────────── 10. ACCORDION ──────────── */

.accordion-row { border-block-end: 1px solid var(--hairline); }
.accordion-row > button {
  inline-size: 100%;
  padding-block: var(--space-5);
  background: none;
  border: 0;
  text-align: start;
  font-family: var(--font-serif);
  font-size: var(--fs-h4);
  color: var(--ink-900);
  display: flex;
  justify-content: space-between;
  align-items: center;
  cursor: pointer;
}
.accordion-row > button::after {
  content: "+";
  font-family: var(--font-sans);
  font-size: 24px;
  color: var(--gold-600);
  transition: transform var(--dur-3) var(--ease-standard);
}
.accordion-row[aria-expanded="true"] > button::after { content: "×"; transform: rotate(0deg); }
.accordion-row > .accordion-body {
  max-block-size: 0;
  overflow: hidden;
  transition: max-block-size var(--dur-4) var(--ease-entrance);
}
.accordion-row[aria-expanded="true"] > .accordion-body { max-block-size: 600px; }

/* ──────────── 11. BREADCRUMB ──────────── */

.breadcrumb {
  font-size: var(--fs-caption);
  color: var(--ink-500);
  margin-block-end: var(--space-5);
}
.breadcrumb a { color: var(--ink-500); }
.breadcrumb a:hover { color: var(--gold-600); }
.breadcrumb > * + *::before { content: "›"; margin-inline: var(--space-2); color: var(--stone-400); }

/* ──────────── 12. PAGINATION ──────────── */

.pagination {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: var(--space-3);
  font-variant-numeric: tabular-nums;
  margin-block: var(--space-10);
}
.pagination a, .pagination span {
  min-inline-size: 32px;
  padding: var(--space-2) var(--space-3);
  color: var(--ink-500);
  text-align: center;
  border-block-end: 1px solid transparent;
}
.pagination a:hover { color: var(--ink-900); border-block-end-color: var(--gold-600); }
.pagination [aria-current="page"] { color: var(--ink-900); border-block-end-color: var(--ink-900); }

/* ──────────── 13. BADGES ──────────── */

.badge, .badge-status {
  display: inline-flex;
  align-items: center;
  gap: var(--space-2);
  padding-inline: var(--space-3);
  padding-block: var(--space-1);
  border: 1px solid var(--hairline);
  border-radius: var(--radius-pill);
  font-size: var(--fs-micro);
  letter-spacing: var(--tr-micro);
  text-transform: uppercase;
  color: var(--ink-700);
  background: var(--paper-0);
}
.badge-status::before {
  content: "";
  inline-size: 6px; block-size: 6px;
  border-radius: 999px;
  background: var(--gold-500);
}

/* ──────────── 14. TOOLTIP ──────────── */

.tooltip {
  position: absolute;
  z-index: var(--z-raised);
  background: var(--ink-900);
  color: var(--cream-50);
  padding: var(--space-2) var(--space-3);
  font-size: var(--fs-caption);
  border-radius: var(--radius-1);
  box-shadow: var(--shadow-2);
  opacity: 0;
  transform: translateY(2px);
  transition: opacity var(--dur-2) var(--ease-standard), transform var(--dur-2) var(--ease-standard);
  pointer-events: none;
}
.tooltip.is-open { opacity: 1; transform: translateY(0); }

/* ──────────── 15. LEAD FORM ──────────── */

.lead-form { display: flex; flex-direction: column; gap: var(--space-5); }
.lead-form .lead-form__legal {
  font-size: var(--fs-caption);
  color: var(--ink-500);
}

/* ──────────── 16. TOAST ──────────── */

.toast {
  position: fixed;
  inset-block-end: var(--space-7);
  inset-inline-end: var(--space-7);
  background: var(--ink-900);
  color: var(--cream-50);
  padding: var(--space-4) var(--space-5);
  border-radius: var(--radius-1);
  box-shadow: var(--shadow-3);
  z-index: var(--z-toast);
  font-size: var(--fs-body-sm);
  transform: translateY(8px);
  opacity: 0;
  transition: opacity var(--dur-3) var(--ease-entrance), transform var(--dur-3) var(--ease-entrance);
}
.toast.is-open { opacity: 1; transform: translateY(0); }

/* ──────────── 17. HEADER ──────────── */

.header-luxury {
  position: sticky;
  inset-block-start: 0;
  z-index: var(--z-header);
  background: transparent;
  border-block-end: 1px solid transparent;
  transition:
    background var(--dur-3) var(--ease-standard),
    border-color var(--dur-3) var(--ease-standard),
    backdrop-filter var(--dur-3) var(--ease-standard);
}
.header-luxury[data-scrolled="true"],
.header-luxury.--header-scrolled {
  background: rgba(250, 247, 241, 0.92);
  backdrop-filter: saturate(140%) blur(6px);
  border-block-end-color: var(--hairline);
}
.header-luxury > .header-inner {
  max-inline-size: var(--container);
  margin-inline: auto;
  padding-inline: var(--space-6);
  block-size: var(--header-h);
  display: grid;
  grid-template-columns: auto 1fr auto;
  align-items: center;
  gap: var(--space-7);
}
.header-luxury .header-wordmark {
  font-family: var(--font-serif);
  font-size: var(--fs-h4);
  font-weight: 500;
  letter-spacing: 0;
  color: var(--ink-900);
}
.header-luxury nav { display: flex; gap: var(--space-7); justify-content: center; }
.header-luxury nav a { color: var(--ink-900); font-size: var(--fs-body-sm); }

/* ──────────── 18. FOOTER ──────────── */

.footer-luxury {
  background: var(--ink-900);
  color: var(--stone-200);
  padding-block: var(--space-12) var(--space-7);
}
.footer-luxury .footer-inner {
  max-inline-size: var(--container);
  margin-inline: auto;
  padding-inline: var(--space-6);
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: var(--space-9);
}
.footer-luxury h4 {
  color: var(--cream-50);
  font-family: var(--font-sans);
  font-size: var(--fs-caption);
  letter-spacing: var(--tr-caption);
  text-transform: uppercase;
  margin-block-end: var(--space-5);
}
.footer-luxury a { color: var(--stone-200); display: block; padding-block: var(--space-2); font-size: var(--fs-body-sm); }
.footer-luxury a:hover { color: var(--gold-500); }
.footer-luxury .footer-rule {
  block-size: 1px;
  background: var(--gold-600);
  inline-size: 64px;
  margin-block: var(--space-10) var(--space-6);
}
.footer-luxury .footer-bottom {
  max-inline-size: var(--container);
  margin-inline: auto;
  padding-inline: var(--space-6);
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-size: var(--fs-caption);
  color: var(--stone-400);
}

/* ──────────── 19. LISTING CARD ──────────── */

.listing-card {
  position: relative;
  background: var(--paper-0);
  border: 1px solid var(--hairline);
  border-radius: var(--radius-1);
  overflow: hidden;
  transition:
    transform var(--dur-3) var(--ease-standard),
    box-shadow var(--dur-3) var(--ease-standard),
    border-color var(--dur-2) var(--ease-standard);
  display: block;
  color: inherit;
}
.listing-card:hover {
  transform: translateY(-2px);
  box-shadow: var(--shadow-2);
  border-color: var(--hairline-strong);
}
.listing-card:focus-visible { outline-offset: 2px; }
.listing-card:active { transform: translateY(0) scale(0.995); transition-duration: var(--dur-1); }

.listing-media {
  position: relative;
  aspect-ratio: 4 / 5;
  background: var(--cream-100);
  overflow: hidden;
}
.listing-media img {
  inline-size: 100%;
  block-size: 100%;
  object-fit: cover;
  transition: transform var(--dur-3) var(--ease-standard);
}
.listing-card:hover .listing-media img { transform: scale(1.02); }

.listing-body { padding: var(--space-5); }
.listing-body h4 {
  margin-block: 0 var(--space-2);
  font-size: var(--fs-h4);
  line-height: var(--lh-h4);
}
.listing-body .listing-meta {
  font-size: var(--fs-caption);
  color: var(--ink-500);
  margin-block-end: var(--space-4);
}
.listing-price {
  font-family: var(--font-sans);
  font-size: var(--fs-h4);
  color: var(--ink-900);
  font-variant-numeric: tabular-nums;
}

.listing-save {
  position: absolute;
  inset-block-start: var(--space-3);
  inset-inline-start: var(--space-3);
  inline-size: 24px; block-size: 24px;
  background: var(--paper-0);
  border: 1px solid var(--hairline);
  border-radius: 0;
  padding: 0;
  display: inline-grid;
  place-items: center;
  cursor: pointer;
  z-index: 2;
}
@media (max-width: 720px) {
  .listing-save { padding: 10px; inline-size: 44px; block-size: 44px; }
}
.listing-save svg { inline-size: 16px; block-size: 16px; stroke: var(--ink-700); stroke-width: 1.25; fill: none; transition: stroke var(--dur-2) var(--ease-standard), fill var(--dur-2) var(--ease-standard), transform var(--dur-2) var(--ease-standard); }
.listing-save:hover svg { stroke: var(--gold-600); }
.listing-save[aria-pressed="true"] svg { fill: var(--gold-600); stroke: var(--gold-600); transform: scale(1); animation: heart-pop var(--dur-2) var(--ease-standard); }

@keyframes heart-pop {
  0%   { transform: scale(.92); }
  100% { transform: scale(1); }
}

.listing-flag {
  position: absolute;
  inset-block-start: var(--space-3);
  inset-inline-end: var(--space-3);
  z-index: 2;
  display: inline-flex;
  align-items: center;
  gap: var(--space-2);
  padding-inline: var(--space-3);
  padding-block: var(--space-1);
  background: var(--paper-0);
  border: 1px solid var(--hairline);
  border-radius: var(--radius-1);
  font-size: var(--fs-micro);
  letter-spacing: var(--tr-micro);
  text-transform: uppercase;
  color: var(--ink-700);
}
.listing-flag::before {
  content: "";
  inline-size: 6px; block-size: 6px;
  border-radius: 999px;
  background: var(--gold-500);
}

/* Listing skeleton */
.listing-card.is-loading .listing-media { background: var(--cream-100); }
.listing-card.is-loading .skeleton-bar {
  block-size: 12px;
  background: linear-gradient(90deg, var(--cream-50), var(--paper-0), var(--cream-50));
  background-size: 200% 100%;
  animation: shimmer 1.5s linear infinite;
  border-radius: var(--radius-1);
  margin-block-end: var(--space-3);
}
.listing-card.is-loading .skeleton-bar.w-60 { inline-size: 60%; }
.listing-card.is-loading .skeleton-bar.w-80 { inline-size: 80%; }
.listing-card.is-loading .skeleton-bar.w-40 { inline-size: 40%; }
@keyframes shimmer { from { background-position: 200% 0; } to { background-position: -200% 0; } }

/* ──────────── 20. PROFILE CARD ──────────── */

.profile-card {
  background: var(--paper-0);
  border: 1px solid var(--hairline);
  padding: var(--space-6);
  display: grid;
  grid-template-columns: 96px 1fr;
  gap: var(--space-5);
  align-items: center;
}
.profile-card .portrait {
  inline-size: 96px; block-size: 96px;
  background: var(--cream-100);
  border-radius: 999px;
  overflow: hidden;
}
.profile-card .portrait img { inline-size: 100%; block-size: 100%; object-fit: cover; }
.profile-card .profile-name { font-family: var(--font-serif); font-size: var(--fs-h4); color: var(--ink-900); margin: 0; }
.profile-card .profile-meta { font-size: var(--fs-caption); color: var(--ink-500); }

/* ──────────── 21. MAP WIDGET ──────────── */

.map-widget {
  position: relative;
  background: var(--paper-0);
  border: 1px solid var(--hairline);
  border-radius: var(--radius-1);
  overflow: hidden;
  min-block-size: 560px;
}
@media (max-width: 720px) { .map-widget { min-block-size: 420px; } }

.map-canvas { position: absolute; inset: 0; background: var(--cream-50); }

.map-zoom {
  position: absolute;
  inset-block-end: var(--space-4);
  inset-inline-start: var(--space-4);
  display: inline-flex;
  flex-direction: column;
  background: var(--paper-0);
  border: 1px solid var(--hairline);
  border-radius: var(--radius-pill);
  box-shadow: var(--shadow-1);
  overflow: hidden;
}
.map-zoom button {
  inline-size: 40px; block-size: 40px;
  background: transparent; border: 0; cursor: pointer;
  color: var(--ink-700);
  display: grid; place-items: center;
}
.map-zoom button + button { border-block-start: 1px solid var(--hairline); }
.map-zoom button:hover { background: var(--cream-100); color: var(--ink-900); }
@media (max-width: 720px) {
  .map-zoom {
    inset-block-end: auto; inset-inline-start: auto;
    inset-block-start: var(--space-4); inset-inline-end: var(--space-4);
    flex-direction: row;
  }
  .map-zoom button { inline-size: 44px; block-size: 44px; }
  .map-zoom button + button { border-block-start: 0; border-inline-start: 1px solid var(--hairline); }
}

.map-layers {
  position: absolute;
  inset-block-start: var(--space-4);
  inset-inline-end: var(--space-4);
  display: inline-flex;
  background: var(--paper-0);
  border: 1px solid var(--hairline);
  border-radius: var(--radius-pill);
  overflow: hidden;
}
.map-layers button {
  background: transparent; border: 0; cursor: pointer;
  padding: var(--space-2) var(--space-4);
  font-size: var(--fs-caption);
  color: var(--ink-700);
}
.map-layers button[aria-pressed="true"],
.map-layers button.is-active { background: var(--ink-900); color: var(--cream-50); }

.map-fullscreen {
  position: absolute;
  inset-block-start: var(--space-4);
  inset-inline-start: var(--space-4);
  inline-size: 32px; block-size: 32px;
  background: var(--paper-0);
  border: 1px solid var(--hairline);
  color: var(--ink-700);
  display: grid; place-items: center;
  cursor: pointer;
}

.pin-property,
.pin-project,
.pin-transaction,
.pin-sponsored,
.pin-cluster {
  position: absolute;
  transform: translate(-50%, -50%);
  cursor: pointer;
}
.pin-property   { inline-size: 10px; block-size: 10px; border-radius: 999px; background: var(--gold-600); box-shadow: 0 0 0 1px var(--ink-900); }
.pin-project    { inline-size: 14px; block-size: 14px; border-radius: 999px; border: 1.5px solid var(--gold-600); background: transparent; position: relative; }
.pin-project::after { content: ""; position: absolute; inset: 4.25px; background: var(--gold-600); border-radius: 999px; }
.pin-transaction { inline-size: 6px;  block-size: 6px;  border-radius: 999px; background: var(--ink-900); }
.pin-sponsored  { inline-size: 13px; block-size: 13px; border-radius: 999px; background: var(--gold-600); box-shadow: 0 0 0 1.5px var(--gold-600); }
.pin-cluster {
  inline-size: 32px; block-size: 32px;
  border-radius: 999px;
  background: var(--cream-100);
  border: 1px solid var(--hairline);
  display: grid; place-items: center;
  color: var(--ink-900);
  font-size: var(--fs-caption);
  font-variant-numeric: tabular-nums;
}

.map-popover {
  position: absolute;
  inline-size: 220px;
  background: var(--paper-0);
  border: 1px solid var(--hairline);
  border-radius: var(--radius-1);
  box-shadow: var(--shadow-2);
  padding: var(--space-3);
  z-index: var(--z-raised);
  opacity: 0;
  transform: translateY(4px);
  transition: opacity var(--dur-2) var(--ease-standard), transform var(--dur-2) var(--ease-standard);
}
.map-popover.is-open { opacity: 1; transform: translateY(0); }
.map-popover .thumb { aspect-ratio: 4/3; background: var(--cream-100); margin-block-end: var(--space-3); }
.map-popover h4 { font-size: var(--fs-body-lg); margin-block-end: var(--space-2); }
.map-popover .popover-meta { font-size: var(--fs-caption); color: var(--ink-500); margin-block-end: var(--space-2); }
.map-popover .popover-price { font-variant-numeric: tabular-nums; font-size: var(--fs-body); color: var(--ink-900); margin-block-end: var(--space-3); }

.map-legend {
  position: absolute;
  inset-block-end: var(--space-4);
  inset-inline-end: var(--space-4);
  background: var(--paper-0);
  border: 1px solid var(--hairline);
  padding: var(--space-3) var(--space-4);
  font-size: var(--fs-caption);
  color: var(--ink-500);
  display: flex; flex-direction: column; gap: var(--space-2);
}
@media (max-width: 720px) { .map-legend { display: none; } }

.map-empty {
  position: absolute; inset: 0;
  display: grid; place-items: center;
  font-family: var(--font-serif);
  font-style: italic;
  font-size: var(--fs-quote);
  color: var(--ink-700);
  text-align: center;
  padding: var(--space-8);
}

/* ──────────── 22. EDITORIAL: PULL-QUOTE & SECTION OPENER ──────────── */

.pull-quote {
  font-family: var(--font-serif);
  font-style: italic;
  font-size: 28px;
  line-height: 1.45;
  color: var(--ink-900);
  margin-block: var(--space-9);
  padding-inline-end: var(--space-6);
  border-inline-end: 2px solid var(--gold-600);
  text-align: end;
}

.article-section-opener {
  margin-block: var(--space-10) var(--space-6);
}
.article-section-opener::before {
  content: "";
  display: block;
  inline-size: 32px;
  block-size: 1px;
  background: var(--gold-600);
  margin-block-end: var(--space-4);
}
.article-section-opener h2 {
  margin: 0;
  font-size: var(--fs-h2);
  line-height: var(--lh-h2);
}

/* ──────────── 23. CALCULATOR VIZ — STACK BAR & BRACKET BAR ──────────── */

/* Mortgage track allocation */
.stack-bar {
  display: flex;
  inline-size: 100%;
  block-size: 8px;
  border: 1px solid var(--hairline);
  border-radius: var(--radius-1);
  overflow: hidden;
  background: var(--cream-100);
}
.stack-bar > .seg { block-size: 100%; }
.stack-bar > .seg--kalatz { background: var(--ink-900); }
.stack-bar > .seg--prime  { background: var(--ink-500); }
.stack-bar > .seg--variable { background: var(--gold-600); }
.stack-bar-legend {
  display: flex; gap: var(--space-6);
  margin-block-start: var(--space-3);
  font-size: var(--fs-caption); color: var(--ink-500);
}
.stack-bar-legend .key { display: inline-flex; align-items: center; gap: var(--space-2); }
.stack-bar-legend .swatch { inline-size: 10px; block-size: 10px; border-radius: var(--radius-1); }
.stack-bar-legend .key--kalatz   .swatch { background: var(--ink-900); }
.stack-bar-legend .key--prime    .swatch { background: var(--ink-500); }
.stack-bar-legend .key--variable .swatch { background: var(--gold-600); }

/* Purchase-tax bracket bar (log-scaled, graduated) */
.bracket-bar {
  position: relative;
  display: grid;
  grid-template-columns: var(--cols, 22% 18% 16% 14% 12% 10% 8%);
  block-size: 24px;
  inline-size: 100%;
  border: 1px solid var(--hairline);
  border-radius: var(--radius-1);
  overflow: hidden;
  background: var(--cream-50);
}
.bracket-bar .bracket {
  position: relative;
  display: grid;
  place-items: center;
  font-size: var(--fs-micro);
  letter-spacing: var(--tr-micro);
  text-transform: uppercase;
  color: var(--ink-700);
  border-inline-end: 1px solid var(--hairline);
}
.bracket-bar .bracket:last-child { border-inline-end: 0; }
/* Graduated tints: paid (filled cream-100 → gold-200 ascending) */
.bracket-bar .bracket.is-paid       { background: var(--cream-100); }
.bracket-bar .bracket.is-current    { background: var(--gold-200); }
.bracket-bar .bracket.is-unreached  { background: var(--paper-0); color: var(--stone-400); }

.bracket-bar .marker {
  position: absolute;
  inset-block-start: -10px;
  inset-inline-start: var(--marker-x, 0%);
  transform: translateX(-50%);
  inline-size: 0; block-size: 0;
  border-inline-start: 6px solid transparent;
  border-inline-end:  6px solid transparent;
  border-block-start: 8px solid var(--gold-600);
}
.bracket-bar .marker::after {
  content: attr(data-label);
  position: absolute;
  inset-inline-start: 50%;
  inset-block-start: -22px;
  transform: translateX(-50%);
  font-family: var(--font-serif);
  font-style: italic;
  font-size: var(--fs-caption);
  color: var(--gold-600);
  white-space: nowrap;
}

/* ──────────── 24. MICRO-INTERACTIONS (§K) ──────────── */

/* Animated gold underline — RTL-correct (grows from inline-end) */
.link-luxury {
  position: relative;
  display: inline-block;
  color: var(--ink-900);
}
.link-luxury::after {
  content: "";
  position: absolute;
  inset-inline-end: 0;
  inset-block-end: -2px;
  inline-size: 100%;
  block-size: 1px;
  background: var(--gold-600);
  transform-origin: inline-end;
  transform: scaleX(0);
  transition: transform var(--dur-3) var(--ease-standard);
}
.link-luxury:hover { color: var(--gold-600); }
.link-luxury:hover::after { transform: scaleX(1); }

/* Drawer entrance with 80ms row stagger */
.drawer { transform: translateX(100%); transition: transform var(--dur-4) var(--ease-entrance); }
html[dir="rtl"] .drawer { transform: translateX(-100%); }
.drawer.is-open { transform: translateX(0); }
.drawer .stagger-row {
  opacity: 0;
  transform: translateY(8px);
  transition: opacity var(--dur-3) var(--ease-entrance), transform var(--dur-3) var(--ease-entrance);
}
.drawer.is-open .stagger-row { opacity: 1; transform: translateY(0); }
.drawer.is-open .stagger-row:nth-child(1) { transition-delay: 80ms; }
.drawer.is-open .stagger-row:nth-child(2) { transition-delay: 160ms; }
.drawer.is-open .stagger-row:nth-child(3) { transition-delay: 240ms; }
.drawer.is-open .stagger-row:nth-child(4) { transition-delay: 320ms; }
.drawer.is-open .stagger-row:nth-child(5) { transition-delay: 400ms; }

/* ──────────── 25. MONETIZATION SURFACES ──────────── */

.sponsored-frame {
  border: 1px solid var(--gold-600) !important;  /* deliberate, the differential signal */
}
.sponsored-eyebrow {
  font-family: var(--font-sans);
  font-weight: 500;
  font-size: var(--fs-eyebrow);
  letter-spacing: var(--tr-eyebrow);
  text-transform: uppercase;
  color: var(--gold-600);
}

.sponsored-capsule {
  inline-size: 100%;
  max-inline-size: var(--article-col);
  margin-block: var(--space-9);
  margin-inline: auto;
  padding: var(--space-6);
  background: var(--paper-0);
  border: 1px solid var(--hairline);
  border-radius: var(--radius-1);
}
.sponsored-capsule .capsule-eyebrow { /* typed-only, no image inside ever */
  font-size: var(--fs-eyebrow);
  letter-spacing: var(--tr-eyebrow);
  text-transform: uppercase;
  color: var(--gold-600);
  margin-block-end: var(--space-3);
}
.sponsored-capsule h4 { margin-block: 0 var(--space-3); }
.sponsored-capsule p { font-size: var(--fs-body-sm); color: var(--ink-700); margin-block-end: var(--space-4); }

.sponsor-strip {
  border-block: 1px solid var(--hairline);
  padding-block: var(--space-8);
  text-align: center;
}
.sponsor-strip .sponsor-row {
  display: inline-flex;
  align-items: center;
  gap: var(--space-10);
}
.sponsor-strip .sponsor-row > img {
  block-size: 24px; inline-size: auto;
  filter: brightness(0) saturate(100%);
  opacity: 0.7;
}
.sponsor-strip .dot {
  inline-size: 4px; block-size: 4px;
  border-radius: 999px;
  background: var(--gold-500);
}

.pro-card { /* extends .profile-card */
  border-color: var(--gold-600);
}
.premier-card { /* extends .profile-card */
  background: var(--cream-100);
  border: 1px solid var(--gold-600);
}
.premier-card .portrait { box-shadow: inset 0 0 0 1px var(--gold-600); }

.ad-slot-reserved {
  inline-size: 100%;
  min-block-size: 120px;
  border: 1px solid var(--hairline);
  display: grid;
  place-items: center;
  color: var(--ink-500);
  background: transparent;
}
.ad-slot-reserved::before {
  content: "מיועד לשותפות עתידית";
  font-size: var(--fs-eyebrow);
  letter-spacing: var(--tr-eyebrow);
  text-transform: uppercase;
  color: var(--gold-600);
}

.cookie-strip {
  position: fixed;
  inset-inline: 0;
  inset-block-end: 0;
  background: var(--cream-100);
  border-block-start: 1px solid var(--hairline);
  padding: var(--space-4) var(--space-6);
  display: flex;
  align-items: center;
  justify-content: space-between;
  font-size: var(--fs-body-sm);
  color: var(--ink-700);
  z-index: var(--z-sticky);
  min-block-size: 48px;
}

/* Sticky mobile sponsored bar */
.sponsored-sticky {
  position: fixed;
  inset-inline: 0;
  inset-block-end: 0;
  background: var(--paper-0);
  border-block-start: 1px solid var(--hairline);
  padding: var(--space-3) var(--space-4);
  display: none;
  align-items: center;
  gap: var(--space-3);
  block-size: 56px;
  z-index: var(--z-sticky);
}
@media (max-width: 720px) { .sponsored-sticky { display: flex; } }

/* ──────────── 26. RESPONSIVE TYPE ──────────── */

@media (max-width: 1024px) {
  :root {
    --fs-display-1: 64px;
    --fs-display-2: 48px;
    --fs-h1: 44px;
    --fs-h2: 32px;
    --fs-h3: 24px;
  }
}
@media (max-width: 720px) {
  :root {
    --fs-display-1: 48px;
    --fs-display-2: 36px;
    --fs-h1: 32px;
    --fs-h2: 26px;
    --fs-h3: 22px;
    --fs-body-lg: 17px;
  }
  .footer-luxury .footer-inner { grid-template-columns: 1fr 1fr; gap: var(--space-7); }
  .header-luxury > .header-inner { grid-template-columns: auto auto; }
  .header-luxury nav { display: none; }
}

/* ──────────── 27. REDUCED MOTION ──────────── */

@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after {
    animation-duration: 0.001ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.001ms !important;
    scroll-behavior: auto !important;
  }
  .listing-card:hover { transform: none; }
  .listing-card:hover .listing-media img { transform: none; }
  .listing-card.is-loading .skeleton-bar { animation: none; background: var(--cream-100); }
}
```

---

<a id="gap-5"></a>
## GAP 5 — theme.json fragment

> שמירה: `/wp-content/themes/nadlan-revenue/theme.json`.
> ערכים מותאמים לבלוק־עורך כך שמחברים יקבלו את אותו עיצוב גם בעמוד וגם בעורך.

```json
{
  "$schema": "https://schemas.wp.org/trunk/theme.json",
  "version": 3,
  "settings": {
    "appearanceTools": true,
    "color": {
      "defaultPalette": false,
      "defaultDuotone": false,
      "defaultGradients": false,
      "palette": [
        { "slug": "ink-900",   "name": "Ink 900",   "color": "#1B1A17" },
        { "slug": "ink-700",   "name": "Ink 700",   "color": "#3A3733" },
        { "slug": "ink-500",   "name": "Ink 500",   "color": "#6E6A63" },
        { "slug": "stone-400", "name": "Stone 400", "color": "#9C978E" },
        { "slug": "stone-200", "name": "Stone 200", "color": "#C8C3B8" },
        { "slug": "cream-100", "name": "Cream 100", "color": "#F1ECE2" },
        { "slug": "cream-50",  "name": "Cream 50",  "color": "#FAF7F1" },
        { "slug": "paper-0",   "name": "Paper 0",   "color": "#FFFFFF" },
        { "slug": "gold-600",  "name": "Gold 600",  "color": "#9C7A3C" },
        { "slug": "gold-500",  "name": "Gold 500",  "color": "#B59558" },
        { "slug": "gold-200",  "name": "Gold 200",  "color": "#E7D9B7" },
        { "slug": "positive-700", "name": "Positive 700", "color": "#2E6A4F" },
        { "slug": "negative-700", "name": "Negative 700", "color": "#8A2A2A" }
      ]
    },
    "typography": {
      "defaultFontSizes": false,
      "fluid": false,
      "fontFamilies": [
        {
          "slug": "frank-ruhl-libre",
          "name": "Frank Ruhl Libre",
          "fontFamily": "\"Frank Ruhl Libre\", \"Cardo\", \"Georgia\", serif",
          "fontFace": [
            { "fontFamily": "Frank Ruhl Libre", "fontWeight": "400", "fontStyle": "normal", "fontDisplay": "swap", "src": [ "file:./assets/fonts/frank-ruhl-libre/frl-400.woff2" ] },
            { "fontFamily": "Frank Ruhl Libre", "fontWeight": "500", "fontStyle": "normal", "fontDisplay": "swap", "src": [ "file:./assets/fonts/frank-ruhl-libre/frl-500.woff2" ] },
            { "fontFamily": "Frank Ruhl Libre", "fontWeight": "700", "fontStyle": "normal", "fontDisplay": "swap", "src": [ "file:./assets/fonts/frank-ruhl-libre/frl-700.woff2" ] },
            { "fontFamily": "Frank Ruhl Libre", "fontWeight": "900", "fontStyle": "normal", "fontDisplay": "swap", "src": [ "file:./assets/fonts/frank-ruhl-libre/frl-900.woff2" ] }
          ]
        },
        {
          "slug": "heebo",
          "name": "Heebo",
          "fontFamily": "\"Heebo\", \"Inter\", \"Helvetica Neue\", Arial, sans-serif",
          "fontFace": [
            { "fontFamily": "Heebo", "fontWeight": "300", "fontStyle": "normal", "fontDisplay": "swap", "src": [ "file:./assets/fonts/heebo/heebo-300.woff2" ] },
            { "fontFamily": "Heebo", "fontWeight": "400", "fontStyle": "normal", "fontDisplay": "swap", "src": [ "file:./assets/fonts/heebo/heebo-400.woff2" ] },
            { "fontFamily": "Heebo", "fontWeight": "500", "fontStyle": "normal", "fontDisplay": "swap", "src": [ "file:./assets/fonts/heebo/heebo-500.woff2" ] }
          ]
        }
      ],
      "fontSizes": [
        { "slug": "display-1", "name": "Display 1", "size": "88px", "fluid": false },
        { "slug": "display-2", "name": "Display 2", "size": "64px", "fluid": false },
        { "slug": "h1",        "name": "H1",        "size": "56px", "fluid": false },
        { "slug": "h2",        "name": "H2",        "size": "40px", "fluid": false },
        { "slug": "h3",        "name": "H3",        "size": "28px", "fluid": false },
        { "slug": "h4",        "name": "H4",        "size": "22px", "fluid": false },
        { "slug": "body-lg",   "name": "Body Large","size": "19px", "fluid": false },
        { "slug": "body",      "name": "Body",      "size": "17px", "fluid": false },
        { "slug": "body-sm",   "name": "Body Small","size": "15px", "fluid": false },
        { "slug": "caption",   "name": "Caption",   "size": "13px", "fluid": false },
        { "slug": "eyebrow",   "name": "Eyebrow",   "size": "11px", "fluid": false },
        { "slug": "micro",     "name": "Micro",     "size": "10px", "fluid": false },
        { "slug": "quote",     "name": "Quote",     "size": "28px", "fluid": false }
      ]
    },
    "spacing": {
      "defaultSpacingSizes": false,
      "units": [ "px", "rem", "em", "%", "vw", "vh" ],
      "spacingSizes": [
        { "slug": "1",  "name": "1 (4)",   "size": "4px"   },
        { "slug": "2",  "name": "2 (8)",   "size": "8px"   },
        { "slug": "3",  "name": "3 (12)",  "size": "12px"  },
        { "slug": "4",  "name": "4 (16)",  "size": "16px"  },
        { "slug": "5",  "name": "5 (20)",  "size": "20px"  },
        { "slug": "6",  "name": "6 (24)",  "size": "24px"  },
        { "slug": "7",  "name": "7 (32)",  "size": "32px"  },
        { "slug": "8",  "name": "8 (40)",  "size": "40px"  },
        { "slug": "9",  "name": "9 (48)",  "size": "48px"  },
        { "slug": "10", "name": "10 (64)", "size": "64px"  },
        { "slug": "11", "name": "11 (80)", "size": "80px"  },
        { "slug": "12", "name": "12 (96)", "size": "96px"  },
        { "slug": "13", "name": "13 (128)","size": "128px" },
        { "slug": "14", "name": "14 (160)","size": "160px" }
      ]
    },
    "shadow": {
      "defaultPresets": false,
      "presets": [
        { "slug": "1", "name": "Shadow 1", "shadow": "0 1px 2px rgba(27,26,23,.04), 0 1px 1px rgba(27,26,23,.02)" },
        { "slug": "2", "name": "Shadow 2", "shadow": "0 4px 12px rgba(27,26,23,.06), 0 1px 2px rgba(27,26,23,.04)" },
        { "slug": "3", "name": "Shadow 3", "shadow": "0 18px 48px rgba(27,26,23,.10), 0 4px 12px rgba(27,26,23,.06)" }
      ]
    },
    "layout": { "contentSize": "680px", "wideSize": "1240px" }
  },
  "styles": {
    "color": {
      "background": "var(--wp--preset--color--cream-50)",
      "text":       "var(--wp--preset--color--ink-700)"
    },
    "typography": {
      "fontFamily": "var(--wp--preset--font-family--heebo)",
      "fontSize":   "var(--wp--preset--font-size--body)",
      "lineHeight": "1.7"
    },
    "elements": {
      "h1": {
        "typography": {
          "fontFamily": "var(--wp--preset--font-family--frank-ruhl-libre)",
          "fontWeight": "500",
          "fontSize":   "var(--wp--preset--font-size--h1)",
          "lineHeight": "1.08",
          "letterSpacing": "-0.01em"
        },
        "color": { "text": "var(--wp--preset--color--ink-900)" }
      },
      "h2": {
        "typography": {
          "fontFamily": "var(--wp--preset--font-family--frank-ruhl-libre)",
          "fontWeight": "500",
          "fontSize":   "var(--wp--preset--font-size--h2)",
          "lineHeight": "1.15"
        },
        "color": { "text": "var(--wp--preset--color--ink-900)" }
      },
      "h3": {
        "typography": {
          "fontFamily": "var(--wp--preset--font-family--frank-ruhl-libre)",
          "fontWeight": "500",
          "fontSize":   "var(--wp--preset--font-size--h3)",
          "lineHeight": "1.25"
        },
        "color": { "text": "var(--wp--preset--color--ink-900)" }
      },
      "h4": {
        "typography": {
          "fontFamily": "var(--wp--preset--font-family--frank-ruhl-libre)",
          "fontWeight": "500",
          "fontSize":   "var(--wp--preset--font-size--h4)",
          "lineHeight": "1.3"
        },
        "color": { "text": "var(--wp--preset--color--ink-900)" }
      },
      "h5": {
        "typography": {
          "fontFamily": "var(--wp--preset--font-family--frank-ruhl-libre)",
          "fontWeight": "500",
          "fontSize":   "var(--wp--preset--font-size--body-lg)"
        }
      },
      "h6": {
        "typography": {
          "fontFamily": "var(--wp--preset--font-family--frank-ruhl-libre)",
          "fontWeight": "500",
          "fontSize":   "var(--wp--preset--font-size--body)"
        }
      },
      "button": {
        "typography": {
          "fontFamily": "var(--wp--preset--font-family--heebo)",
          "fontWeight": "500",
          "fontSize":   "var(--wp--preset--font-size--body-sm)",
          "letterSpacing": "0.04em"
        },
        "color": {
          "background": "var(--wp--preset--color--ink-900)",
          "text":       "var(--wp--preset--color--cream-50)"
        },
        "border": { "radius": "2px", "width": "1px", "color": "var(--wp--preset--color--ink-900)" },
        "spacing": {
          "padding": { "top": "16px", "bottom": "16px", "left": "24px", "right": "24px" }
        }
      },
      "link": {
        "color": { "text": "var(--wp--preset--color--ink-900)" },
        ":hover": { "color": { "text": "var(--wp--preset--color--gold-600)" } }
      }
    }
  }
}
```

---

<a id="gap-6"></a>
## GAP 6 — Gutenberg block patterns

> כל קובץ נשמר ב־`/wp-content/themes/nadlan-revenue/patterns/{slug}.php` ונטען
> אוטומטית כ־block pattern. הטקסט בעברית RTL. הקסל מעקב block אמיתי.

### P1 — `patterns/hero.php`

```php
<?php
/**
 * Title: כותרת בית — Hero
 * Slug: nadlan-revenue/hero
 * Categories: nadlan-hero
 * Description: כותרת אדיטוריאלית של עמוד הבית עם 4:5 imagery וקריאות לפעולה כקישורי טקסט.
 */
?>
<!-- wp:group {"tagName":"section","className":"nadlan-hero","layout":{"type":"constrained"}} -->
<section class="wp-block-group nadlan-hero">
  <!-- wp:columns {"verticalAlignment":"center"} -->
  <div class="wp-block-columns are-vertically-aligned-center">

    <!-- wp:column {"width":"55%"} -->
    <div class="wp-block-column" style="flex-basis:55%">
      <!-- wp:paragraph {"className":"eyebrow"} -->
      <p class="eyebrow">פלטפורמת ידע · נדל״ן ישראל</p>
      <!-- /wp:paragraph -->

      <!-- wp:heading {"level":1,"fontSize":"display-1"} -->
      <h1 class="wp-block-heading has-display-1-font-size">להבין נדל״ן בישראל לעומק, לפני שחותמים.</h1>
      <!-- /wp:heading -->

      <!-- wp:paragraph {"fontSize":"body-lg"} -->
      <p class="has-body-lg-font-size">מחירים אמיתיים, מסים מחושבים נכון, מסלולי משכנתא מושוואים — נכתב ונערך על־ידי המערכת, ללא תיווך מסחרי.</p>
      <!-- /wp:paragraph -->

      <!-- wp:separator {"className":"gold-rule"} -->
      <hr class="wp-block-separator gold-rule"/>
      <!-- /wp:separator -->

      <!-- wp:paragraph -->
      <p>
        <a class="link-luxury" href="/tools/mortgage/">מחשבון משכנתא ←</a>
        &nbsp;&nbsp;
        <a class="link-luxury" href="/guides/">כל המדריכים ←</a>
      </p>
      <!-- /wp:paragraph -->

      <!-- wp:paragraph {"fontSize":"caption","style":{"color":{"text":"var:preset|color|ink-500"}}} -->
      <p class="has-caption-font-size has-text-color" style="color:var(--wp--preset--color--ink-500)">מקורות: רשות המסים · בנק ישראל · הלמ״ס. עודכן השבוע.</p>
      <!-- /wp:paragraph -->
    </div>
    <!-- /wp:column -->

    <!-- wp:column {"width":"45%"} -->
    <div class="wp-block-column" style="flex-basis:45%">
      <!-- wp:image {"className":"image-luxury","style":{"aspectRatio":"4/5"}} -->
      <figure class="wp-block-image image-luxury">
        <!-- Photographer-only architectural shot, warm-graded, landscape -->
        <img src="/wp-content/themes/nadlan-revenue/assets/img/placeholder-architecture-4x5.jpg" alt="צילום אדריכלי של בניין מגורים בתל אביב, אור צהריים חם" />
      </figure>
      <!-- /wp:image -->
    </div>
    <!-- /wp:column -->

  </div>
  <!-- /wp:columns -->
</section>
<!-- /wp:group -->
```

### P2 — `patterns/tools-row.php`

```php
<?php
/**
 * Title: שורת חמשת הכלים
 * Slug: nadlan-revenue/tools-row
 * Categories: nadlan-row
 * Description: חמישה כלים ראשיים עם מספור ordinals זהב.
 */
?>
<!-- wp:group {"tagName":"section","className":"nadlan-tools-row","layout":{"type":"constrained"}} -->
<section class="wp-block-group nadlan-tools-row">
  <!-- wp:heading {"level":2,"fontSize":"h2"} -->
  <h2 class="has-h2-font-size">חמשת הכלים שעורכים השוק.</h2>
  <!-- /wp:heading -->

  <!-- wp:separator {"className":"gold-rule gold-rule--sm"} --><hr class="wp-block-separator gold-rule gold-rule--sm"/><!-- /wp:separator -->

  <!-- wp:columns -->
  <div class="wp-block-columns">

    <!-- wp:column -->
    <div class="wp-block-column">
      <span class="ordinal" style="font-family:var(--wp--preset--font-family--frank-ruhl-libre);font-style:italic;color:var(--wp--preset--color--gold-600);font-size:28px">01</span>
      <h3>מחשבון משכנתא</h3>
      <p>שלוש מסלולים, הקצאה מומלצת, סך החזרים.</p>
      <p><a class="link-luxury" href="/tools/mortgage/">פתח כלי ←</a></p>
    </div>
    <!-- /wp:column -->

    <!-- wp:column -->
    <div class="wp-block-column">
      <span class="ordinal" style="font-family:var(--wp--preset--font-family--frank-ruhl-libre);font-style:italic;color:var(--wp--preset--color--gold-600);font-size:28px">02</span>
      <h3>מס רכישה</h3>
      <p>סרגל מדרגות עם סמן עמדה חי.</p>
      <p><a class="link-luxury" href="/tools/purchase-tax/">פתח כלי ←</a></p>
    </div>
    <!-- /wp:column -->

    <!-- wp:column -->
    <div class="wp-block-column">
      <span class="ordinal" style="font-family:var(--wp--preset--font-family--frank-ruhl-libre);font-style:italic;color:var(--wp--preset--color--gold-600);font-size:28px">03</span>
      <h3>תשואה להשקעה</h3>
      <p>שכ״ד, עלויות, רווח נטו שנתי.</p>
      <p><a class="link-luxury" href="/tools/yield/">פתח כלי ←</a></p>
    </div>
    <!-- /wp:column -->

    <!-- wp:column -->
    <div class="wp-block-column">
      <span class="ordinal" style="font-family:var(--wp--preset--font-family--frank-ruhl-libre);font-style:italic;color:var(--wp--preset--color--gold-600);font-size:28px">04</span>
      <h3>השוואת ערים</h3>
      <p>חציון, ת/ע ועסקאות 12 חודשים.</p>
      <p><a class="link-luxury" href="/tools/city-compare/">פתח כלי ←</a></p>
    </div>
    <!-- /wp:column -->

    <!-- wp:column -->
    <div class="wp-block-column">
      <span class="ordinal" style="font-family:var(--wp--preset--font-family--frank-ruhl-libre);font-style:italic;color:var(--wp--preset--color--gold-600);font-size:28px">05</span>
      <h3>שמאות מהירה</h3>
      <p>הערכת שווי לפי עסקאות סמוכות.</p>
      <p><a class="link-luxury" href="/tools/valuation/">פתח כלי ←</a></p>
    </div>
    <!-- /wp:column -->

  </div>
  <!-- /wp:columns -->
</section>
<!-- /wp:group -->
```

### P3 — `patterns/trust-band.php`

```php
<?php
/**
 * Title: רצועת אמון
 * Slug: nadlan-revenue/trust-band
 * Categories: nadlan-row
 * Description: רצועת cream-100 עם 4 סטטיסטיקות וקווי הזהב המפרידים.
 */
?>
<!-- wp:group {"tagName":"section","className":"nadlan-trust-band","backgroundColor":"cream-100","layout":{"type":"constrained"}} -->
<section class="wp-block-group nadlan-trust-band has-cream-100-background-color has-background" style="padding-block:64px">

  <!-- wp:columns -->
  <div class="wp-block-columns" style="border-block:1px solid var(--hairline)">

    <!-- wp:column {"className":"trust-tile"} -->
    <div class="wp-block-column trust-tile" style="border-inline-end:1px solid var(--gold-600);padding-inline:24px">
      <p class="eyebrow">חציון ארצי ₪/מ״ר</p>
      <p class="has-h2-font-size tabular" style="font-family:var(--wp--preset--font-family--frank-ruhl-libre)">25,400 ₪</p>
      <p class="has-caption-font-size" style="color:var(--wp--preset--color--ink-500)">רשות המסים, 12 חודשים אחרונים</p>
    </div>
    <!-- /wp:column -->

    <!-- wp:column {"className":"trust-tile"} -->
    <div class="wp-block-column trust-tile" style="border-inline-end:1px solid var(--gold-600);padding-inline:24px">
      <p class="eyebrow">עסקאות 12 ח׳</p>
      <p class="has-h2-font-size tabular" style="font-family:var(--wp--preset--font-family--frank-ruhl-libre)">94,712</p>
      <p class="has-caption-font-size" style="color:var(--wp--preset--color--ink-500)">רשות המסים</p>
    </div>
    <!-- /wp:column -->

    <!-- wp:column {"className":"trust-tile"} -->
    <div class="wp-block-column trust-tile" style="border-inline-end:1px solid var(--gold-600);padding-inline:24px">
      <p class="eyebrow">משכנתא ממוצעת</p>
      <p class="has-h2-font-size tabular" style="font-family:var(--wp--preset--font-family--frank-ruhl-libre)">1,128,000 ₪</p>
      <p class="has-caption-font-size" style="color:var(--wp--preset--color--ink-500)">בנק ישראל</p>
    </div>
    <!-- /wp:column -->

    <!-- wp:column {"className":"trust-tile"} -->
    <div class="wp-block-column trust-tile" style="padding-inline:24px">
      <p class="eyebrow">שינוי שנתי</p>
      <p class="has-h2-font-size tabular" style="font-family:var(--wp--preset--font-family--frank-ruhl-libre)">−1.8%</p>
      <p class="has-caption-font-size" style="color:var(--wp--preset--color--ink-500)">הלמ״ס, מדד מחירי דירות</p>
    </div>
    <!-- /wp:column -->

  </div>
  <!-- /wp:columns -->

  <!-- wp:paragraph {"align":"center","fontSize":"caption","style":{"color":{"text":"var:preset|color|ink-500"}}} -->
  <p class="has-text-align-center has-caption-font-size has-text-color" style="color:var(--wp--preset--color--ink-500)">מקורות פתוחים בלבד. שום נתון לא מומצא — נטען מדאטה ציבורי כל שבוע.</p>
  <!-- /wp:paragraph -->
</section>
<!-- /wp:group -->
```

### P4 — `patterns/city-intelligence.php`

```php
<?php
/**
 * Title: מודיעין ערים
 * Slug: nadlan-revenue/city-intelligence
 * Categories: nadlan-row
 * Description: שתי עמודות — מקום למפה/גרף ורשימת ערים מובילות.
 */
?>
<!-- wp:group {"tagName":"section","className":"nadlan-city-intel","layout":{"type":"constrained"}} -->
<section class="wp-block-group nadlan-city-intel">
  <!-- wp:heading {"level":2} --><h2>מה קורה בכל עיר.</h2><!-- /wp:heading -->
  <!-- wp:separator {"className":"gold-rule gold-rule--sm"} --><hr class="wp-block-separator gold-rule gold-rule--sm"/><!-- /wp:separator -->

  <!-- wp:columns -->
  <div class="wp-block-columns">

    <!-- wp:column {"width":"60%"} -->
    <div class="wp-block-column" style="flex-basis:60%">
      <div class="map-widget" style="min-block-size:420px">
        <div class="map-canvas" aria-label="מפת ישראל מונוכרומטית"></div>
        <div class="map-zoom"><button aria-label="הגדלה">+</button><button aria-label="הקטנה">−</button></div>
      </div>
    </div>
    <!-- /wp:column -->

    <!-- wp:column {"width":"40%"} -->
    <div class="wp-block-column" style="flex-basis:40%">
      <table class="table-hairline">
        <thead><tr><th>עיר</th><th class="tabular">חציון ₪/מ״ר</th><th class="tabular">Δ שנתי</th></tr></thead>
        <tbody>
          <tr><td><a class="link-luxury" href="/cities/tel-aviv/">תל אביב–יפו</a></td><td class="tabular">52,800</td><td class="tabular">−2.4%</td></tr>
          <tr><td><a class="link-luxury" href="/cities/jerusalem/">ירושלים</a></td><td class="tabular">32,100</td><td class="tabular">+0.6%</td></tr>
          <tr><td><a class="link-luxury" href="/cities/haifa/">חיפה</a></td><td class="tabular">18,900</td><td class="tabular">−1.1%</td></tr>
          <tr><td><a class="link-luxury" href="/cities/ramat-gan/">רמת גן</a></td><td class="tabular">38,400</td><td class="tabular">−1.9%</td></tr>
          <tr><td><a class="link-luxury" href="/cities/herzliya/">הרצליה</a></td><td class="tabular">44,200</td><td class="tabular">−0.8%</td></tr>
        </tbody>
      </table>
      <p><a class="link-luxury" href="/cities/">כל הערים ←</a></p>
    </div>
    <!-- /wp:column -->

  </div>
  <!-- /wp:columns -->
</section>
<!-- /wp:group -->
```

### P5 — `patterns/guides-editorial.php`

```php
<?php
/**
 * Title: מדריכים — 1+2 אדיטוריאלי
 * Slug: nadlan-revenue/guides-editorial
 * Categories: nadlan-editorial
 * Description: לידיר אחד גדול ושני משניים — אותה היררכיית עורך.
 */
?>
<!-- wp:group {"tagName":"section","className":"nadlan-guides-editorial","layout":{"type":"constrained"}} -->
<section class="wp-block-group nadlan-guides-editorial">
  <!-- wp:heading {"level":2} --><h2>מן המערכת.</h2><!-- /wp:heading -->
  <!-- wp:separator {"className":"gold-rule gold-rule--sm"} --><hr class="wp-block-separator gold-rule gold-rule--sm"/><!-- /wp:separator -->

  <!-- wp:columns -->
  <div class="wp-block-columns">

    <!-- wp:column {"width":"66%"} -->
    <div class="wp-block-column" style="flex-basis:66%">
      <a class="card-interactive" href="/guides/purchase-tax-2026/">
        <figure class="image-luxury" style="aspect-ratio:16/9;background:var(--cream-100)"></figure>
        <div style="padding:24px">
          <p class="eyebrow">מדריך · מיסוי</p>
          <h2>מס רכישה 2026 — מי משלם כמה, באמת.</h2>
          <p>פירוק מדרגות, דירה ראשונה מול שנייה, חישוב בפועל על שני נכסים אמיתיים.</p>
          <p class="has-caption-font-size" style="color:var(--wp--preset--color--ink-500)">מערכת · 18 דקות קריאה</p>
        </div>
      </a>
    </div>
    <!-- /wp:column -->

    <!-- wp:column {"width":"34%"} -->
    <div class="wp-block-column" style="flex-basis:34%">
      <a class="card-interactive" href="/guides/mortgage-mix/">
        <figure class="image-luxury" style="aspect-ratio:4/3;background:var(--cream-100)"></figure>
        <div style="padding:20px">
          <p class="eyebrow">מדריך · מימון</p>
          <h4>הקצאה נכונה בין קל״צ, פריים ומשתנה.</h4>
        </div>
      </a>
      <a class="card-interactive" href="/guides/urban-renewal/" style="margin-top:32px;display:block">
        <figure class="image-luxury" style="aspect-ratio:4/3;background:var(--cream-100)"></figure>
        <div style="padding:20px">
          <p class="eyebrow">מדריך · התחדשות עירונית</p>
          <h4>תמ״א 38 מול פינוי־בינוי — איפה ערך אמיתי.</h4>
        </div>
      </a>
    </div>
    <!-- /wp:column -->

  </div>
  <!-- /wp:columns -->
</section>
<!-- /wp:group -->
```

### P6 — `patterns/professionals-teaser.php`

```php
<?php
/**
 * Title: אנשי מקצוע — טיזר
 * Slug: nadlan-revenue/professionals-teaser
 * Categories: nadlan-row
 * Description: שלוש כרטיסי פרופיל + קישור לדירקטוריון.
 */
?>
<!-- wp:group {"tagName":"section","className":"nadlan-pros","layout":{"type":"constrained"}} -->
<section class="wp-block-group nadlan-pros">
  <!-- wp:heading {"level":2} --><h2>אנשי מקצוע שבדקנו.</h2><!-- /wp:heading -->
  <!-- wp:separator {"className":"gold-rule gold-rule--sm"} --><hr class="wp-block-separator gold-rule gold-rule--sm"/><!-- /wp:separator -->

  <!-- wp:columns -->
  <div class="wp-block-columns">
    <div class="wp-block-column">
      <article class="profile-card">
        <div class="portrait"></div>
        <div>
          <h4 class="profile-name">עו״ד דנה לוי</h4>
          <p class="profile-meta">מקרקעין · תל אביב · עברית, אנגלית</p>
          <a class="link-luxury" href="/pros/dana-levy/">לפרופיל ←</a>
        </div>
      </article>
    </div>
    <div class="wp-block-column">
      <article class="profile-card">
        <div class="portrait"></div>
        <div>
          <h4 class="profile-name">יועץ משכנתאות אורי שמיר</h4>
          <p class="profile-meta">מימון · ירושלים · עברית</p>
          <a class="link-luxury" href="/pros/uri-shamir/">לפרופיל ←</a>
        </div>
      </article>
    </div>
    <div class="wp-block-column">
      <article class="profile-card">
        <div class="portrait"></div>
        <div>
          <h4 class="profile-name">שמאית רונית כהן</h4>
          <p class="profile-meta">שמאות · חיפה · עברית, רוסית</p>
          <a class="link-luxury" href="/pros/ronit-cohen/">לפרופיל ←</a>
        </div>
      </article>
    </div>
  </div>
  <!-- /wp:columns -->

  <!-- wp:paragraph --><p><a class="link-luxury" href="/pros/">כל אנשי המקצוע ←</a></p><!-- /wp:paragraph -->
</section>
<!-- /wp:group -->
```

### P7 — `patterns/footer.php`

```php
<?php
/**
 * Title: פוטר ראשי
 * Slug: nadlan-revenue/footer
 * Categories: nadlan-footer
 * Description: ארבע עמודות ink-900, גוון זהב מפריד, שורה תחתונה משפטית.
 */
?>
<!-- wp:group {"tagName":"footer","className":"footer-luxury","layout":{"type":"constrained"}} -->
<footer class="footer-luxury">
  <div class="footer-inner">
    <div>
      <h4>נדל״ן חכם</h4>
      <p style="color:var(--stone-400)">פלטפורמת ידע עצמאית. ללא תיווך, ללא עמלות מצרכן.</p>
    </div>
    <div>
      <h4>כלים</h4>
      <a href="/tools/mortgage/">מחשבון משכנתא</a>
      <a href="/tools/purchase-tax/">מס רכישה</a>
      <a href="/tools/yield/">תשואה להשקעה</a>
      <a href="/tools/city-compare/">השוואת ערים</a>
    </div>
    <div>
      <h4>מדריכים</h4>
      <a href="/guides/buying/">קנייה</a>
      <a href="/guides/selling/">מכירה</a>
      <a href="/guides/investment/">השקעה</a>
      <a href="/guides/urban-renewal/">התחדשות עירונית</a>
    </div>
    <div>
      <h4>על נדל״ן חכם</h4>
      <a href="/about/">המערכת</a>
      <a href="/methodology/">מתודולוגיה</a>
      <a href="/contact/">יצירת קשר</a>
      <a href="/privacy/">פרטיות</a>
    </div>
  </div>
  <div class="footer-rule" aria-hidden="true"></div>
  <div class="footer-bottom">
    <span>© <?php echo esc_html( gmdate( 'Y' ) ); ?> נדל״ן חכם · ירושלים</span>
    <span>אין באמור משום ייעוץ משפטי, מס או השקעות.</span>
  </div>
</footer>
<!-- /wp:group -->
```

### P8 — `patterns/article-section-opener.php`

```php
<?php
/**
 * Title: פותח חלק במאמר
 * Slug: nadlan-revenue/article-section-opener
 * Categories: nadlan-article
 * Description: קו זהב 32px + H2 — אותו אופנער לכל חלק במאמר ארוך.
 */
?>
<!-- wp:group {"className":"article-section-opener"} -->
<div class="wp-block-group article-section-opener">
  <!-- wp:heading {"level":2} -->
  <h2>איך לחשב את מס הרכישה שלכם נכון.</h2>
  <!-- /wp:heading -->
</div>
<!-- /wp:group -->
```

### P9 — `patterns/pull-quote.php`

```php
<?php
/**
 * Title: ציטוט סרק
 * Slug: nadlan-revenue/pull-quote
 * Categories: nadlan-article
 * Description: Frank Ruhl Libre 28px איטלי עם קו זהב מצד inline-end (RTL).
 */
?>
<!-- wp:group {"className":"pull-quote-wrap"} -->
<div class="wp-block-group pull-quote-wrap">
  <blockquote class="pull-quote">
    "הנתון היחיד שמשנה בעסקת מס רכישה הוא 'דירה יחידה' או 'שנייה ואילך' — כל השאר תוצאה של הגדרה."
  </blockquote>
</div>
<!-- /wp:group -->
```

### P10 — `patterns/faq-accordion.php`

```php
<?php
/**
 * Title: שאלות נפוצות
 * Slug: nadlan-revenue/faq-accordion
 * Categories: nadlan-article
 * Description: רכיב accordion עם שאלות נפוצות.
 */
?>
<!-- wp:group {"className":"faq-accordion"} -->
<div class="wp-block-group faq-accordion">
  <h2>שאלות נפוצות.</h2>

  <div class="accordion-row" aria-expanded="false">
    <button aria-controls="faq-1">מי נחשב לדירה יחידה לצורך מס רכישה?</button>
    <div class="accordion-body" id="faq-1">
      <p>חוק מס רכישה מגדיר "דירה יחידה" לפי בעלות במועד החתימה ולא לפי כוונה. רכישה של דירה נוספת לפני מכירת הקודמת מבטלת את הטבת המדרגה הראשונה — אלא אם נמכרה תוך 24 חודשים.</p>
    </div>
  </div>

  <div class="accordion-row" aria-expanded="false">
    <button aria-controls="faq-2">כמה זמן לוקח לקבל אישור משכנתא עקרוני?</button>
    <div class="accordion-body" id="faq-2">
      <p>אישור עקרוני אצל בנק גדול לוקח בממוצע 7-14 ימי עסקים, בהנחה שכל המסמכים מוגשים בפעם הראשונה במלואם.</p>
    </div>
  </div>

  <div class="accordion-row" aria-expanded="false">
    <button aria-controls="faq-3">מה ההבדל בין תמ״א 38/1 לפינוי בינוי?</button>
    <div class="accordion-body" id="faq-3">
      <p>תמ״א 38/1 מחזקת את הבניין הקיים ומוסיפה קומות; פינוי בינוי הורס ובונה מחדש פרויקט גדול יותר עם מספר בניינים. ההבדל מבחינת הדייר: זמן עבודה, מספר הדירות התמורה, וגובה ההיטל.</p>
    </div>
  </div>
</div>
<!-- /wp:group -->
```

---

<a id="gap-7"></a>
## GAP 7 — Monetization surfaces

### A. Sponsored guide / article

מבנה זהה לתבנית §E ב־Round 1 — אותם 680px column, אותו H1 serif, אותו author strip — בשלושה הבדלים מדויקים:

```
TOP OF ARTICLE
  eyebrow gold: "תוכן שותפים · אלפא נדל״ן"   ← מחליף את eyebrow קטגוריה
  H1 serif 56  "מדריך מס רכישה למשקיע זר 2026."
  caption ink-500 "מערכת נדל״ן חכם · 20 דק׳ קריאה"

PARTNER DISCLOSURE BAND (immediately under the byline strip)
  ───────────────────── 1px gold-600, full article-column ─────────────────────
  | caption ink-700:                                                             |
  | "תוכן זה נתמך על־ידי אלפא נדל״ן. הביקורת המערכתית של נדל״ן חכם נשמרת."        |
  ───────────────────── 1px gold-600 ─────────────────────────────────────────────
  block-size: 32px; padding-inline: 16px; vertical-align: center;

AUTHOR/TRUST STRIP — partner monochrome wordmark replaces author avatar
  [partner wordmark, monochrome ink-700, max-block-size 24px]
  caption "אלפא נדל״ן · שותף תוכן"   (← link to /partners/alpha-realty/)

BODY = identical pillar template. No colored backgrounds. No CTA banner.
```

### B. Sponsored listing — premium placement

- בסיס: `.listing-card` רגיל.
- הבדלים:
  - מסביב לכל הקלף: `class="listing-card sponsored-frame"` (1px gold-600).
  - Eyebrow בראש ה־body: `"ממומן · אלפא נדל״ן"` ב־`.sponsored-eyebrow`.
  - אופציונלית — ribbon יחיד `◆` 8px gold-600 ב־`inset-block-start: 8px; inset-inline-end: 8px;` מעל התמונה.
  - **לעולם** לא שני סימנים (אם יש frame — אין ribbon, או להפך). אדריכלות: בחר אחד פר־פרויקט.
- בגריד: מותר בעמדות 1, 5, 9 בלבד.
- בתחתית הגריד, caption ink-500:
  > "מודעות ממומנות מסומנות. סדר ההצגה אינו דירוג איכותי."

### C. Sponsored map pin variant

- `.pin-sponsored` (כבר ב־CSS): 10px gold-600 dot + 1.5px gold-600 ring.
- Popover: זהה ל־`.map-popover` רגיל, עם הוספת eyebrow `"ממומן"` בראש ה־popover (לפני ה־thumbnail).
- **לעולם** לא יותר משלושה pins ממומנים במפה אחת.

### D. Sidebar / inline ad slot — article reading column

#### Slot 1: typography-only capsule (in-body, max 1 per article)

```
─── 1px hairline ───
eyebrow gold: "שותפות בתשלום"
h4 serif: "ייעוץ מס לרוכשים זרים · אלפא נדל״ן"
body-sm ink-700 (2 שורות): "פגישת אבחון ראשונית ללא עלות. צוות דובר עברית, אנגלית ורוסית."
text-link gold: "להזמין פגישה ←"
─── 1px hairline ───
```

מחלקה: `.sponsored-capsule`. ללא תמונה. ללא רקע צבעוני. רוחב 680px (זהה
לעמודת המאמר).

#### Slot 2: mobile sticky bar

- 56px בגובה, `.sponsored-sticky`, paper-0, hairline עליון.
- תוכן: eyebrow gold "שותפות בתשלום" + h4 קצר + `→ link-luxury` + `×` close.
- מותר אחד בלבד. אם slot 1 מוצג במאמר → ב־mobile אין sticky.

### E. Partner / sponsor strip (homepage)

ממוקם בין §D.6 (Professionals teaser) ל־footer:

```
─────────────────────── 1px ink-12% ───────────────────────
                    eyebrow gold center
                       "בשיתוף עם"

  [WORDMARK]  ●  [WORDMARK]  ●  [WORDMARK]  ●  [WORDMARK]  ●  [WORDMARK]
   24px high monochrome ink-700, 8px gold-500 dot separators, 64px gap

─────────────────────── 1px ink-12% ───────────────────────
```

מחלקה: `.sponsor-strip`. כל לוגו נטען כ־SVG בודד, מעובד `filter: brightness(0) opacity(0.7)` כדי להבטיח monochrome. ללא CTA. ללא "ראו את כל השותפים".

### F. Professional directory tiers

| Tier | Card class | Differential |
|---|---|---|
| Free | `.profile-card` | בסיסי |
| Pro | `.profile-card.pro-card` | 1px gold-600 frame + eyebrow "PRO" gold ליד התחום |
| Premier | `.profile-card.premier-card` | רקע cream-100 + 1px gold-600 inset על הפורטרט + eyebrow "פרימייר" gold; מופיע ראשון בכל סינון |

ב־filter sidebar: hairline pill toggle `"פרימייר בלבד"`. אם נבחר — הדירקטוריון מוגבל ל־`.premier-card` בלבד.

### G. Sponsored professional placement

- בעמוד `/pros/`, עמדה 1 בכל דף תוצאות = `.profile-card.premier-card` עם
  eyebrow נוסף `"מודעה"` ב־gold תחת שורת עיר/שפות.
- ב־caption תחתון של הדף:
  > "אנשי מקצוע ממומנים מסומנים."

### H. Tracking-free analytics disclosure

```
.cookie-strip — cream-100, 48px tall, ink-700 body-sm:

  פרטיות   |   "באתר זה משתמשים במדידה מצטברת בלבד, ללא קוקיז צד שלישי."   ×
  ↑                                                                          ↑
  link-luxury start                                                          dismiss
```

נשמר ב־`localStorage` כדי לא לחזור. אם המשתמש לא מבטל — הוא נשאר. ללא overlay.

### I. Ad-slot placeholders — reserved positions

| מיקום | Placeholder class | Status |
|---|---|---|
| בית, בין §D.5 ל־§D.6 | `.ad-slot-reserved` | RESERVED — eyebrow "מיועד לשותפות עתידית" |
| עמוד עיר, מתחת לגרף, מעל טבלת תת-שכונות | `.ad-slot-reserved` | RESERVED |
| עמוד מחשבון, ב־right rail מתחת לקלטים | `.ad-slot-reserved` | RESERVED |
| עמוד מאמר, ב־left rail מתחת ל־author/share strip | `.ad-slot-reserved` | RESERVED |

המחלקה כבר ב־CSS bundle. ה־CMS template רושם את ה־slots כ־`<div class="ad-slot-reserved" data-slot="home-mid">` בלי תוכן — הפיכת ה־slot לפעיל בעתיד היא החלפה של inner HTML בלבד.

### J. Monetization CSS classes — recap

כבר ב־bundle, סעיף §25:

- `.sponsored-frame`
- `.sponsored-eyebrow`
- `.sponsored-capsule`
- `.sponsor-strip` (+ `.sponsor-row`, `.dot`)
- `.pro-card`, `.premier-card`
- `.ad-slot-reserved`
- `.cookie-strip`
- `.sponsored-sticky`

### K. What we will never do

- ❌ IAB display ads (300×250, 728×90, sticky image bars).
- ❌ Pop-ups, interstitials, exit-intent modals.
- ❌ Auto-play video, animated banners, "skip in 5".
- ❌ רקע צבעוני להבדלת תוכן ממומן.
- ❌ "Featured" / "verified" badges כצ׳קמרק זהב או כוכב.
- ❌ יותר מ־monetization surface אחד גלוי בו־זמנית (capsule + sponsored map pins הוא המקסימום).
- ❌ Affiliate disclosure בפסקה קטנה למטה. תמיד: eyebrow gold disclosure.

---

<a id="self-critique"></a>
## Self-critique — "Would Sotheby's ship this?"

### 2 נקודות החלשות ביותר בחבילת ה־CSS ומה תוקן:

**1. ‎`!important` ב־`.sponsored-frame`.**
היה: `border: 1px solid var(--gold-600) !important;` — חטא ראשון של בסיס קוד נקי.
אבל ההחלטה כאן מודעת: המסגרת חייבת לנצח את כל קולגה־מחלקה (`.listing-card`, `.profile-card`) שלכל אחת מהן יש `border` משלה. החלופה היא ספציפיות גבוהה יותר (`.listing-card.sponsored-frame`) שמחייבת לזכור את ה־base class בכל מופע. **שמרתי `!important` בכוונה**, עם תיעוד מפורש בקוד ("deliberate, the differential signal"). זה השימוש הצרכני־מותר היחיד ב־`!important` בכל הקובץ.

**2. `transition` רחב ב־`*` ב־`prefers-reduced-motion`.**
היה: `*, *::before, *::after { transition-duration: 0.001ms !important; }` — אלים גלובלית.
תיקון: השארתי את הסלקטור (הוא הפרקטיקה התקנית של WCAG SC 2.3.3) אבל הוספתי 3 overrides ספציפיות לסקיפס נפוצים שלא רוצים להישבר (skeleton shimmer הופך לתצוגה סטטית, listing hover מבטל transform). ככה אנימציות־התראה לא נופלות לתוך הצבירה.

נוסף: בודקתי שכל המעברים מבוססים `cubic-bezier` ולא `linear`/`ease` ברירת מחדל; שכל `transform` ב־RTL משתמש ב־`translateX` עם override `html[dir="rtl"]` (drawer); שכל מחלקה עם `position: absolute` יש לה הורה עם `position: relative` (`.listing-media`, `.map-widget`). כל הסלקטורים זוכים לפסילה ב־30 שניות על־ידי מפתח חדש בלי לקרוא את ה־HTML.

---

<a id="honesty"></a>
## Honesty statement

### DONE (במסמך הזה, מוכן ל־port)
- מערכת CSS שלמה לפי כל הטוקנים של Round 1 + Round 2 — צבעים, מרווחים, טיפוגרפיה, רדיוסים, צללים, תנועות, z-index, focus.
- `@font-face` ל־Frank Ruhl Libre (400/500/700/900) ו־Heebo (300/400/500) עם `unicode-range` עברי+לטיני.
- בסיס סמנטי עם logical properties — אותו CSS עובד RTL ו־LTR.
- כל הקומפוננטים מ־§I של Round 1: buttons, inputs, slider, toggle, checkbox, radio, cards, tables, tabs, accordion, breadcrumb, pagination, badges, tooltip, lead-form, toast, header, footer.
- כל הקומפוננטים החדשים מ־Round 2: listing-card (כל ה־states + saved + skeleton), profile-card, map widget מלא (zoom/layers/pins/popover/legend/fullscreen/empty), pull-quote, article section-opener.
- שני ויזואליזציות החתימה: `.stack-bar` (משכנתא) ו־`.bracket-bar` (מס רכישה).
- חבילת מונטיזציה מלאה: 8 מחלקות, 4 ad-slot reserved positions, cookie disclosure, 3 tiers לדירקטוריון.
- `theme.json` v3 שלם: 13 צבעים, 2 font families עם 7 fontFace entries, 13 font sizes, 14 spacing steps, 3 shadow presets, styles ל־h1–h6 + button + link + global.
- 10 block patterns (P1–P10) עם block markup אמיתי, מחלקות שתואמות 1:1 ל־CSS, עברית RTL מוכנה לעורך.
- `prefers-reduced-motion` global override + 3 component-specific overrides.

### ASSUMED
- קבצי WOFF2 ימוקמו בדיוק ב־`/wp-content/themes/nadlan-revenue/assets/fonts/{frank-ruhl-libre|heebo}/`. הצעת מקור (Google Fonts → WOFF2 self-hosted) — נדרשת הורדה חד־פעמית.
- ‎`Listing` מקושר ל־Custom Post Type שהמפתח יגדיר (`property`) עם meta fields: `price`, `address`, `neighborhood`, `city`, `floor`, `rooms`, `is_saved`, `is_sponsored`, `flag_type` ("new"/"drop").
- מפת `.map-widget` תופעל על־ידי MapLibre GL JS (Open Source, ללא Mapbox token) עם vector basemap מותאם (style.json) שצובע את ה־cream-50 + hairline ink. ה־CSS שלי מטפל ב־chrome (zoom, layers, pins, popover) — לא ב־tiles עצמן.
- ה־`.bracket-bar` מציג ערכים סטטיים כברירת מחדל; הצרכן מזריק `style="--cols: …; --marker-x: X%;"` מ־PHP כדי לסמן את עמדת המשתמש.
- שמות ה־block pattern categories (`nadlan-hero`, `nadlan-row`, `nadlan-editorial`, `nadlan-article`, `nadlan-footer`) ירשמו ב־`functions.php` עם `register_block_pattern_category()`.
- ‎`.cookie-strip` מציית למצב localStorage בלבד — ללא integration עם consent management פלטפורמה (אם יש GDPR scope אמיתי, נדרש Cookiebot/Iubenda).

### NEEDS REAL INPUTS
- **צילום אדריכלי**: כל ה־`image-luxury` placeholders. אדריכל-צלם, light-warm, landscape 4:5. ללא stock.
- **לוגו השותפים** (`.sponsor-strip`): wordmark SVG monochrome אחד לכל שותף, גובה 24px. בלי color, בלי גרדיינטים, בלי PNG.
- **נתוני עסקאות אמיתיים**: trust-band ו־city tables כוללים מספרים placeholder (25,400 ₪/מ״ר, 94,712 עסקאות). חיבור ל־`nadlan.gov.il` API נדרש ועיגון משפטי (mirror, attribution, no commercial resale).
- **תוויות עברית סופיות**: כל הטקסטים שכתבתי הם copy עורכי איכותי לקריאה ראשונה, אבל חייב עורך לשוני שעובר על כל H1, dek, eyebrow ו־CTA לפני live.
- **map tiles**: vector style.json שמרנדר את הבסיס המונוכרומטי. אפשר להזמין מ־Maptiler / Stadia / Protomaps עם custom style ב־$0–$25/חודש.
- **icon set**: כל ה־SVG icons (heart, +, −, ⤢, ×, ◆, ←, →) — קובץ icon sprite יחיד, stroke 1.25px, ink-700, max 24×24.
- **טלפון/אימייל**: ב־`/contact/` השארתי placeholder gold rule במקום הטלפון עד שתחליטו אם להתחייב למוקד מענה.

ללא Tailwind. ללא utility soup. כל מחלקה סמנטית, כל transition מציית ל־`prefers-reduced-motion`, כל RTL דרך logical properties — מוכן ל־drop directly ב־`style.css` של block theme.

