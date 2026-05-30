# Article Guide Design Pattern (`nadlan-guide`)

> **What this is:** the self-contained, framework-agnostic HTML+CSS article layout the owner approved on 2026-05-30 ("I want this kind of design, it looks premium, professional"). It is the pattern currently live on the older Codex-era pillars (`/real-estate-lawyer/` id 11, `/investment-apartment/` id 10, `/buying-apartment/` id 9, etc.). Every new pillar and spoke should be built with this pattern so the whole site looks consistent and designed, not like raw HTML.

> **Why it works:** the layout is injected as a single `<!-- wp:html -->` Gutenberg block containing one `<div class="nadlan-guide">` wrapper plus a scoped `<style>` block. Because the CSS is scoped to `.nadlan-guide`, it renders identically regardless of theme, with no dependency on theme.json block-wrapping. This is the opposite of the 2026-05-29 Cowork spokes, which were bare `<h2>`/`<p>` tags that picked up no styling at all.

## The structure (what every article gets)

```html
<!-- wp:html -->
<div class="nadlan-guide">

  <!-- HERO: eyebrow + H2 + lede paragraphs + CTA + image -->
  <section class="hero wrap" aria-label="...">
    <div>
      <span class="eyebrow">בדיקה משפטית לפני חתימה</span>
      <h2>כותרת ראשית של המדריך</h2>
      <p>פסקת פתיחה ראשונה.</p>
      <p>פסקת פתיחה שנייה.</p>
      <div class="cta">
        <a class="btn" href="/target/">פעולה ראשית</a>
        <a class="btn secondary" href="/target2/">פעולה משנית</a>
      </div>
    </div>
    <figure>
      <img src="..." alt="תיאור בעברית" loading="lazy">
      <figcaption>כיתוב קצר.</figcaption>
    </figure>
  </section>

  <!-- BODY: all H2/H3/P/UL/TABLE inside .wrap -->
  <div class="wrap">
    <section>
      <h2>כותרת סעיף</h2>
      <p>...</p>

      <!-- 3-card row for "what to check / who it suits" -->
      <div class="cards">
        <div class="card"><b>כותרת כרטיס</b><p>תוכן.</p></div>
        <div class="card"><b>כותרת כרטיס</b><p>תוכן.</p></div>
        <div class="card"><b>כותרת כרטיס</b><p>תוכן.</p></div>
      </div>

      <!-- comparison table -->
      <table>
        <thead><tr><th>עמודה</th><th>עמודה</th></tr></thead>
        <tbody><tr><td>...</td><td>...</td></tr></tbody>
      </table>

      <!-- highlight note (gold box) for the key takeaway / warning -->
      <div class="note">נקודה קריטית שאסור לפספס.</div>

      <!-- CTA again near the bottom -->
      <div class="cta"><a class="btn" href="/real-estate-lawyer/">קבעו ייעוץ</a></div>
    </section>
  </div>

</div>
<!-- /wp:html -->
```

## The CSS contract (component vocabulary)

The full stylesheet lives inline. The component classes a writer uses:

| Class | Purpose |
|---|---|
| `.nadlan-guide` | Root wrapper. Sets RTL, font, base color. Scopes everything. |
| `.wrap` | Centered column, `min(1040px, 100% - 32px)`. |
| `.hero` | 2-column grid (text + image), rounded card with soft gradient + shadow. Collapses to 1 column under 800px. |
| `.eyebrow` | Pill tag above the H2. Establishes context / category. |
| `.cards` | 3-column responsive grid of `.card`. |
| `.card` | White rounded card with border + shadow. `.card b` is the bold card title. |
| `table` / `th` / `td` | Styled comparison table (header tint, row borders, rounded). |
| `.note` | Highlight box (warm tint, bold) for the one critical takeaway or warning per section. |
| `.cta` | Flex row of buttons. |
| `.btn` / `.btn.secondary` | Primary (filled pill) + secondary (outline) call-to-action buttons. |

### Current palette (green Codex era) - as live on id 9/10/11

```
text:            #14211c / #2f433b
headings:        #08382d (h2), #0f5a43 (h3)
hero gradient:   #fff → #f2faf5
borders:         #dce8e1
eyebrow:         bg #fff7de, border #efd890, text #65470f
note box:        bg #fff8e8, border #efd890, text #513d16
button primary:  bg #0f5a43, text #fff
table header:    bg #edf8f3
font:            Heebo, "Noto Sans Hebrew"
```

### Luxury-palette variant (Lovable ink/cream/gold) - DROP-IN replacement

> **OPEN DECISION (owner, 2026-05-30):** keep the green palette as-is, OR re-tokenize the same structure to the Lovable warm palette. The structure stays identical; only the color values swap. Mapping below, using the theme.json tokens.

```
text:            #1B1A17 (ink-900) / #3A3733 (ink-700)
headings:        #1B1A17 (h2), #6E6A63 (ink-500) or gold-600 (h3)
hero gradient:   #FFFFFF → #FAF7F1 (cream-50)
borders:         #C8C3B8 (stone-200)
eyebrow:         bg #E7D9B7 (gold-200), border #B59558 (gold-500), text #9C7A3C (gold-600)
note box:        bg #FAF7F1 (cream-50), border #B59558 (gold-500), text #3A3733
button primary:  bg #9C7A3C (gold-600), text #FFFFFF  [or ink-900 bg for higher contrast]
table header:    bg #F1ECE2 (cream-100)
headings font:   "Frank Ruhl Libre" serif (per Lovable)
body font:       Heebo
```

A ready-to-paste luxury stylesheet template is at `/tmp/nadlan-guide-luxury.css` when the decision is made; the green template is recoverable from any of pages id 9/10/11.

## How a writer/agent produces a page with this pattern

1. ChatGPT writes the prose per `strategy-master.md` §13 (Google Blueprint) and the SYSTEM block in `spoke-prompts-short-rent-abroad.md`. **Update that SYSTEM block** so ChatGPT outputs the `.nadlan-guide` structure directly: hero (eyebrow + h2 + 2 lede paragraphs + CTA), body sections with h2/h3/p, at least one `.cards` row, at least one `table`, one `.note` per major section, CTA near the bottom. Output is the inner HTML only (no `<style>`, no `<div class="nadlan-guide">` wrapper, no `<!-- wp:html -->`).
2. The publishing agent (per `internal-linking-hub-spoke.md` §"Article publishing protocol") runs the sanity-check (no `{index=N}`, no `[N]`, no `word+N`, no em-dash, no preamble, no AI-tells), then wraps the cleaned inner HTML in: `<!-- wp:html -->` + `<div class="nadlan-guide">` + the scoped `<style>` block + content + closing tags.
3. The `<style>` block is identical on every page (the browser caches it; duplication across pages is acceptable for self-contained robustness). When the palette decision is made, store the canonical stylesheet in the repo at `assets/article-guide.css` and reference it, OR keep inlining it.
4. Wire internal links + lawyer CTA + Yoast meta + author (see the publishing protocol).

## Hard rules

- **Never publish bare `<h2>`/`<p>` without the `.nadlan-guide` wrapper.** That was the 2026-05-29 failure (unstyled raw HTML).
- **One `.note` per section maximum** - it loses impact if overused.
- **Hero image must have a real Hebrew alt + figcaption.** No decorative-only images.
- **CTA in the hero AND near the bottom**, both pointing to a money path (lawyer consult, calculator, or registration).
- **Tables for any comparison** (yields, tax brackets, country-vs-country). Never inline comparisons in prose.
- **Em-dash ban + forbidden phrases** still apply inside this pattern (see `copywriting-skill.md`).

## Relationship to the Lovable design system

The Lovable luxury system (`luxury-design-system.md` + sisters) defines the brand-level tokens, the header/footer, the homepage patterns, and the component vocabulary. The `nadlan-guide` pattern is the **article-body** layer. They are not in conflict: the brand chrome (header, footer, fonts, palette) comes from the theme; the article body uses `nadlan-guide` for its internal structure. The open decision is only whether `nadlan-guide`'s internal palette matches the green Codex era or the Lovable warm palette. Recommendation: re-tokenize to the Lovable palette so the article body and the brand chrome agree.

---
_Created 2026-05-30 by Claude Code (claude-opus-4-7). Pattern reverse-engineered from live pages id 9/10/11 (Codex era), which the owner approved as the target look. Palette-variant mapping added for the Lovable luxury system._
