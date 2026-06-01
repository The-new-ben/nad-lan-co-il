# Article Guide Design Pattern (`nadlan-guide`) — green canonical

> **Owner decision 2026-05-30: green palette is canonical.** This is the framework-agnostic HTML+CSS article layout for every new pillar and spoke on nad-lan.co.il. The previous luxury (ink/cream/gold) variant in earlier revisions of this file is deprecated; references to it elsewhere should be updated.

> **Why this exists:** the layout is injected as a single `<!-- wp:html -->` Gutenberg block containing one `<div class="nadlan-guide">` wrapper plus a scoped `<style>` block. Because the CSS is scoped to `.nadlan-guide`, it renders identically regardless of theme, with no dependency on theme.json block-wrapping. This is the opposite of the 2026-05-29 Cowork spokes (bare `<h2>`/`<p>` tags that picked up no styling at all).

> **Reference page (live):** open `https://nad-lan.co.il/design-demo-green/` to see the full pattern rendered. Open `https://nad-lan.co.il/real-estate-lawyer/` for an in-the-wild example. The 11 pages that were retro-wrapped on 2026-05-30 are also live examples: `/investment/`, `/short-term-rentals-abroad/short-term-rentals-thailand/`, etc.

## Structure (every article gets this shape)

```html
<!-- nadlan-guide-wrap-v1 -->
<!-- wp:html -->
<script type="application/ld+json">{...Person + Article JSON-LD...}</script>
<style>{...the CSS contract below, inlined...}</style>
<div class="nadlan-guide"><div class="wrap">

  <!-- byline (author bar with avatar) -->
  <div class="byline">
    <div class="avatar" aria-hidden="true">בב</div>
    <div class="who"><b>מאת בן בטש, עורך דין</b><span>חבר לשכת עורכי הדין בישראל · רישיון 29020 · נבדק לאחרונה: YYYY-MM-DD</span></div>
  </div>

  <!-- HERO: eyebrow + H2 + lede + CTA + image -->
  <section class="hero" aria-label="פתיחה">
    <div>
      <span class="eyebrow">קטגוריה / קונטקסט</span>
      <h2>כותרת ראשית</h2>
      <p>פסקת לידע ראשונה.</p>
      <p>פסקת לידע שנייה.</p>
      <div class="cta">
        <a class="btn" href="/target/">פעולה ראשית</a>
        <a class="btn secondary" href="/target2/">פעולה משנית</a>
      </div>
    </div>
    <figure><img src="..." alt="תיאור בעברית" loading="lazy"><figcaption>כיתוב.</figcaption></figure>
  </section>

  <!-- BODY: sections with h2/h3/p; punctuated by cards/table/note -->
  <section>
    <h2>סעיף ראשון</h2>
    <p>...</p>
    <div class="cards">
      <div class="card"><b>כותרת כרטיס</b><p>תוכן.</p></div>
      <div class="card"><b>כותרת כרטיס</b><p>תוכן.</p></div>
      <div class="card"><b>כותרת כרטיס</b><p>תוכן.</p></div>
    </div>
    <table>
      <thead><tr><th>עמודה</th><th>עמודה</th></tr></thead>
      <tbody><tr><td>...</td><td>...</td></tr></tbody>
    </table>
    <div class="note">נקודת המפתח של הסעיף - אחת לכל סעיף, לא יותר.</div>
    <div class="cta"><a class="btn" href="/real-estate-lawyer/">קבעו ייעוץ עם עו"ד בן בטש</a></div>
  </section>

  <!-- DISCLAIMER (mandatory on tax/legal/contract/regulation content) -->
  <div class="disclaimer">אין לראות במאמר זה ייעוץ משפטי. כל מקרה דורש בדיקה פרטנית. ליצירת קשר: <a href="/real-estate-lawyer/">/real-estate-lawyer/</a>.</div>

</div></div>
<!-- /wp:html -->
<!-- /nadlan-guide-wrap-v1 -->
```

## CSS contract (component vocabulary)

| Class | Purpose |
|---|---|
| `.nadlan-guide` | Root wrapper. Sets RTL, Heebo font, base color #14211c. Scopes everything. |
| `.wrap` | Centered column, `min(1040px, 100% - 32px)`. |
| `.byline` | Author bar with circular green avatar + name + license + last-reviewed date. |
| `.hero` | 2-column grid (text + image), rounded card with soft green gradient + shadow. Collapses to 1 column under 800px. |
| `.eyebrow` | Pill tag above the H2. Gold-ish (`#fff7de` bg). |
| `.cards` | 3-column responsive grid of `.card`. |
| `.card` | White rounded card with green border + shadow. `.card b` is bold green card title. |
| `table` / `th` / `td` | Comparison table with green header tint (`#edf8f3`), row borders, rounded. |
| `.note` | Highlight box (warm `#fff8e8`, bold) for the **one** critical takeaway per section. |
| `.cta` | Flex row of buttons. |
| `.btn` / `.btn.secondary` | Primary green pill / outlined secondary. |
| `.disclaimer` | Dashed border, smaller text, for the legal disclaimer at the bottom. |

## Canonical palette (green)

```
text body:       #14211c → #2f433b
headings:        #08382d (h2, font-weight 900), #0f5a43 (h3, font-weight 800)
hero gradient:   #fff → #f2faf5
borders:         #dce8e1 / #bfd7cc / #e7f0eb
eyebrow:         bg #fff7de, border #efd890, text #65470f
note (warm):     bg #fff8e8, border #efd890, text #513d16
button primary:  bg #0f5a43, text #fff
button avatar:   bg #08382d, text #fff7de (initials)
table header:    bg #edf8f3
body font:       Heebo, "Noto Sans Hebrew", Arial, sans-serif
heading font:    Heebo (weight 900 for h2, 800 for h3) - dominant, distinctive
```

**Owner-explicit 2026-05-30:** the headline weight + green color is the dominant brand signal. Do not swap fonts or palette without owner approval.

## Font best practices (per owner request 2026-05-30)

- Use Heebo (Google Fonts) for both body and headings, with explicit weights: 400 body, 600 strong, 800 h3, 900 h2 + buttons + card titles + eyebrow.
- Preload Heebo 400 + 900 in the theme `<head>` for LCP. Other weights `font-display: swap`.
- Self-host the woff2 files in the theme (`/assets/fonts/`) to avoid Google Fonts privacy/GDPR complications and to remove a third-party dependency.
- Hebrew fallback chain: `Heebo, "Noto Sans Hebrew", Arial, sans-serif`. Never start with a Latin-only font (avoids Hebrew rendering bugs on Windows).
- No serif anywhere in the article body. Headings are Heebo 900, not a separate serif - the "dominant" feel comes from weight + green color + letter-spacing, not from a typeface change.

## How a writer/agent produces a page with this pattern

1. ChatGPT writes the prose per `strategy-master.md` §13 (Google Blueprint) and the SYSTEM block in `runbook-cowork-article-batch.md`. The SYSTEM block is hardened to make ChatGPT produce the `.nadlan-guide` structure directly: hero (eyebrow + h2 + 2 lede paragraphs + CTA), body sections with h2/h3/p, at least one `.cards` row, at least one `table`, **one** `.note` per section maximum, CTA near the bottom. Output is the **inner HTML only** (no `<style>`, no `<div class="nadlan-guide">` wrapper, no `<!-- wp:html -->`, no `<h1>`).
2. The publishing agent runs the sanity-check (no `{index=N}`, no `[N]`, no `word+N`, no em-dash, no preamble, no AI-tells), then wraps the cleaned inner HTML in: `<!-- nadlan-guide-wrap-v1 -->` + `<!-- wp:html -->` + JSON-LD `<script>` + `<style>` + `.nadlan-guide` + `.wrap` + byline + content + disclaimer + closing tags.
3. The `<style>` block is identical on every page. The browser caches it after the first hit; the duplicate cost is ~2.5KB minified. Acceptable price for self-contained robustness.
4. The `<script type="application/ld+json">` block contains a Person node for the author and an Article node referencing it. WordPress preserves the script tag in `wp:html` blocks for users with `unfiltered_html` capability (admin). Yoast adds its own Organization + WebSite + Breadcrumb graph separately; entity disambiguation via `@id` keeps the graphs consistent.
5. Wire internal links + lawyer CTA + Yoast meta + author user assignment per `internal-linking-hub-spoke.md` §"Article publishing protocol" and `runbook-cowork-article-batch.md`.

## Hard rules

- **Never publish bare `<h2>`/`<p>` without the `.nadlan-guide` wrapper.** That was the 2026-05-29 failure.
- **One `.note` per section maximum** - it loses impact if overused.
- **Hero image must have a real Hebrew alt + figcaption.** No decorative-only images.
- **CTA in the hero AND near the bottom**, both pointing to a money path (`/real-estate-lawyer/`, `/purchase-tax-calculator/`, `/join-pro/`).
- **Tables for any comparison** (yields, tax brackets, country-vs-country). Never inline comparisons in prose.
- **Em-dash ban + forbidden phrases** still apply inside this pattern (see `copywriting-skill.md` §3-4).
- **Author byline + Article JSON-LD on every page touching tax, legal, contract, regulation, investment, mortgage.** Owner is the author of record as of 2026-05-30 (בן בטש, רישיון 29020, info@nad-lan.co.il).

## Idempotency

The wrap is wrapped between `<!-- nadlan-guide-wrap-v1 -->` and `<!-- /nadlan-guide-wrap-v1 -->`. A re-publishing script can strip from the open marker to the close marker, leaving the body intact, then re-wrap with a fresh version. **Never** use a non-bounded "strip from marker to end" regex (that was the 2026-05-30 bug that wiped all 11 pages; restored from revisions).

---
_Created 2026-05-30 by Claude Code (claude-opus-4-7). Pattern reverse-engineered from live pages id 9/10/11 (Codex era), which the owner approved as the target look. Green canonical per owner 2026-05-30. Earlier luxury (ink/cream/gold) variant deprecated._
