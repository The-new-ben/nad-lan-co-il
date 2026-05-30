# Article Publishing Protocol — ChatGPT output → live page

> **For Cowork:** This is the second half of `google-blueprint-workflow.md`. The Blueprint produces a Hebrew HTML article from ChatGPT. This protocol turns that raw HTML into a live page that ranks, monetizes, and matches the Lovable luxury design. **Every article goes through every step.** No shortcuts. The 2026-05-29 country spokes skipped these steps and 6 of 7 shipped broken.

> **Cross-references (do not duplicate here, follow the link):**
> - Voice rules + forbidden phrases + em-dash ban → `copywriting-skill.md`
> - Cluster map + which sibling/parent to link → `internal-linking-hub-spoke.md`
> - Yoast meta requirements + Person schema → `yoast-config.md`
> - Lawyer-byline + disclaimer wording for tax/legal → `copywriting-skill.md` §8
> - Lovable design tokens (the styling that the Gutenberg blocks unlock) → `luxury-design-system.md`
> - The pillar's existing prompts for the 7 short-rent countries → `spoke-prompts-short-rent-abroad.md`

## Pre-flight: what you have in hand

The output from `google-blueprint-workflow.md` step 6: a Hebrew HTML blob from ChatGPT, with `<h2>`, `<h3>`, `<p>`, `<ul>`, `<li>`, `<strong>` tags, all `dir="rtl"`. Length 1,800-2,500 words for a spoke or 2,500-4,000 for a pillar.

You also have, from the Blueprint:
- The target query
- The intent
- The mandatory backbone outline
- The sources list with dates

## Step 1 — Sanity-check the ChatGPT output (BEFORE touching WordPress)

Save the ChatGPT output to a temp file. Then scan it with the checks below. Anything that fails gets fixed in the source — never publish broken HTML hoping to fix it in WP.

### 1a. Strip ChatGPT preamble

ChatGPT often opens with one of:
- `להלן מאמר HTML נקי להדבקה`
- `הנה המאמר המבוקש`
- `להלן הטיוטה`
- `הערת שקיפות: ...`

**Delete these lines entirely.** They are meta-commentary about the writing task. They have no place on a public page.

### 1b. Strip citation tokens

Perplexity-style or ChatGPT-search-style output sometimes ends paragraphs with citation tokens like:
- `Government of Israel+9נדלן מאסטר+9Portukey+9`
- `[1][2][3]`
- `(Source: ...)+12`

**Delete every one of these.** Convert real source attributions to clean Hebrew inline form: `(מקור: בנק ישראל, מרץ 2026)`.

### 1c. Em-dash sweep

```bash
grep -c '—' /tmp/article.html
# must be 0
```

If non-zero, replace every ` — ` with ` - ` (regular hyphen with surrounding spaces) or with a comma. Owner-explicit ban (2026-05-29). See `copywriting-skill.md` §"Em-dash ban".

### 1d. Forbidden-phrase sweep

```bash
for p in 'חשוב להבין' 'ראוי לציין' 'במילים אחרות' 'עולם הנדלן' 'בעידן' 'ללא ספק' 'בעולם שבו' 'אינסוף' 'באופן כללי' 'בסופו של דבר' 'לסיכום' 'כפי שראינו' 'במאמר'; do
  c=$(grep -c "$p" /tmp/article.html)
  [ "$c" != "0" ] && echo "FORBIDDEN: $p ($c)"
done
```

Any hit → send back to ChatGPT with: "החלף את כל המופעים של '[phrase]' בנוסח ענייני שונה. אל תשתמש בביטוי הזה כלל." Do not try to fix in place — ChatGPT will rewrite cleaner than you can patch.

### 1e. Internal-leak word sweep

```bash
for w in 'ליד' 'leads' 'CRM' 'פילר' 'spoke' 'hub' 'cluster' 'intent' 'money page' 'UTM' 'SEO'; do
  c=$(grep -c "$w" /tmp/article.html)
  [ "$c" != "0" ] && echo "INTERNAL LEAK: $w ($c)"
done
```

`ליד` only triggers a manual check (it is a real Hebrew word meaning "next to"). Confirm context. If it means a sales lead, rephrase. The rest are forbidden in public copy — see `copywriting-skill.md` §4.

### 1f. HTML well-formedness

```bash
python3 -c "from html.parser import HTMLParser; \
class P(HTMLParser):\
    def __init__(s): super().__init__(); s.ok=True
    def error(s,m): s.ok=False
p=P(); p.feed(open('/tmp/article.html').read()); print('OK' if p.ok else 'BROKEN')"
```

Also check tag balance with a quick `grep`:
```bash
grep -o '<h2' /tmp/article.html | wc -l   # should equal
grep -o '</h2>' /tmp/article.html | wc -l
```

### 1g. Length

```bash
wc -w /tmp/article.html   # Hebrew words: rough; aim for 1800-2500 spoke, 2500-4000 pillar
```

## Step 2 — Wrap in proper structure for publishing

The article body starts with the FIRST `<h2>`, not `<h1>` (WordPress wraps the page title in `<h1>` automatically; do not duplicate). If ChatGPT gave an `<h1>`, downgrade it to `<h2>` or delete it (use the page title instead).

Prepend the **date+author block**:

```html
<p dir="rtl"><em>עודכן ונבדק: 2026-MM-DD.</em></p>
```

For any article touching tax, legal, contract, or regulation (which is most of our content), also prepend the author byline AFTER the date line:

```html
<p dir="rtl"><strong>מאת [שם הבעלים המלא], עורך דין · נבדק לאחרונה: 2026-MM-DD</strong></p>
```

(See `copywriting-skill.md` §8 for the exact wording and the legal-disclaimer paragraph required at the bottom.)

Append the **legal disclaimer** at the very bottom for any tax/legal article:

```html
<hr/>
<p dir="rtl"><em>אין לראות במאמר זה ייעוץ משפטי. כל מקרה דורש בדיקה פרטנית של נסיבותיו. ליצירת קשר לייעוץ ראשוני: <a href="/contact/">/contact/</a>.</em></p>
```

## Step 3 — Apply Lovable design tokens (Gutenberg block wrapping)

This is where Cowork's pages broke. WordPress + the `nadlan-revenue` theme uses Full Site Editing (FSE) and applies styles per block. A bare `<p>` paragraph gets default styling. A `<!-- wp:paragraph -->` block gets the Lovable token styling (Frank Ruhl Libre serif on h2/h3, gold accent rules, proper RTL spacing).

**Wrap every top-level element in its Gutenberg block comment.** Pattern:

```html
<!-- wp:heading {"level":2} --><h2 dir="rtl">title</h2><!-- /wp:heading -->
<!-- wp:paragraph --><p dir="rtl">body...</p><!-- /wp:paragraph -->
<!-- wp:heading {"level":3} --><h3 dir="rtl">subtitle</h3><!-- /wp:heading -->
<!-- wp:list {"ordered":false} --><ul><li>item</li></ul><!-- /wp:list -->
```

Use this Python helper (Cowork: run it; do not retype it):

```python
import re
def wrap_blocks(html):
    # h1-h6
    html = re.sub(r'<h([1-6])([^>]*)>(.*?)</h\1>',
                  lambda m: f'<!-- wp:heading {{"level":{m.group(1)}}} --><h{m.group(1)}{m.group(2)}>{m.group(3)}</h{m.group(1)}><!-- /wp:heading -->',
                  html, flags=re.S)
    # paragraphs
    html = re.sub(r'<p([^>]*)>(.*?)</p>',
                  lambda m: f'<!-- wp:paragraph --><p{m.group(1)}>{m.group(2)}</p><!-- /wp:paragraph -->',
                  html, flags=re.S)
    # unordered lists
    html = re.sub(r'<ul([^>]*)>(.*?)</ul>',
                  lambda m: f'<!-- wp:list --><ul{m.group(1)}>{m.group(2)}</ul><!-- /wp:list -->',
                  html, flags=re.S)
    # ordered lists
    html = re.sub(r'<ol([^>]*)>(.*?)</ol>',
                  lambda m: f'<!-- wp:list {{"ordered":true}} --><ol{m.group(1)}>{m.group(2)}</ol><!-- /wp:list -->',
                  html, flags=re.S)
    return html
```

After wrapping, eyeball one h2 and one paragraph in the source — confirm the block comments are present.

## Step 4 — Internal-link wiring (the anti-cannibalization map)

A spoke that links only back to its pillar is an orphan. Every spoke needs **3 directions of linking**:

1. **Up to its pillar** (mandatory, exactly one anchor in the opening 200 words).
2. **Across to 2-4 sibling spokes** under the same pillar (mandatory; phrased naturally in body text, not as a "related articles" list).
3. **Down/across to 1-2 tools** (calculator, comparison widget, catalog filter).
4. **Out to the monetization CTA** (lawyer consultation, professional directory) — minimum once near the bottom.

The map for each pillar is in `internal-linking-hub-spoke.md`. Read the relevant pillar's spoke list before publishing.

### Anti-cannibalization rules

- **Never link a spoke to another spoke that targets the same query.** Two pages competing for "השקעת נדל״ן בפורטוגל" is self-cannibalization.
- **Spoke→pillar anchor text must use the pillar's H1 phrasing**, not the query. Example: from a Portugal spoke, link to the abroad pillar as "השקעת Airbnb בחו״ל" (the pillar's H1), not as "השקעת נדל״ן בחו״ל".
- **Spoke→sibling anchor text must use the sibling's exact query**. Example: from Portugal, link to Spain as "השכרה לטווח קצר בספרד" (Spain's target query).
- **Pillar→spoke anchor text uses the spoke's target query**. The pillar is the hub that distributes ranking power to spokes.

### The lawyer CTA block (monetization)

Every article should include this block near the bottom, before the FAQ:

```html
<!-- wp:group {"className":"cta-lawyer"} -->
<div class="wp-block-group cta-lawyer">
  <!-- wp:heading {"level":3} --><h3 dir="rtl">צריכים ליווי משפטי לעסקה?</h3><!-- /wp:heading -->
  <!-- wp:paragraph --><p dir="rtl">[שם הבעלים], עורך דין מקרקעין, מציע ייעוץ ראשוני של 15 דקות ללא עלות לקוראי האתר. הייעוץ בוחן את העסקה הספציפית שלכם, סיכונים משפטיים, מס רכישה ומבנה החוזה.</p><!-- /wp:paragraph -->
  <!-- wp:buttons --><div class="wp-block-buttons">
    <!-- wp:button {"className":"is-style-fill"} --><div class="wp-block-button is-style-fill"><a class="wp-block-button__link" href="/contact/">קבעו ייעוץ ראשוני</a></div><!-- /wp:button -->
  </div><!-- /wp:buttons -->
</div><!-- /wp:group -->
```

(The `cta-lawyer` CSS class is styled in `style.css` with the gold accent + cream background.)

## Step 5 — Set Yoast meta (BEFORE saving)

Yoast meta is set via REST in the `meta` field. **Every article needs**:

```python
yoast_meta = {
    '_yoast_wpseo_title':        '<target query> | nadlan-revenue',  # ≤60 chars
    '_yoast_wpseo_metadesc':     '<one factual sentence + what reader gets + soft CTA>',  # 150-160 chars
    '_yoast_wpseo_focuskw':      '<target query>',
    '_yoast_wpseo_is_cornerstone': '1' if pillar else '',
    '_yoast_wpseo_canonical':    '',  # WP fills this from permalink; leave blank
}
```

Then in the REST PUT body:

```python
requests.post(f'{WP_BASE_URL}/wp-json/wp/v2/pages/{page_id}',
              auth=(WP_USER, WP_APP_PASSWORD),
              json={'content': html_with_blocks, 'meta': yoast_meta})
```

**Verify after save** by reading `yoast_head_json.description`. If it is `MISSING` or shows the first paragraph instead of your metadesc, the write was rejected — usually because Yoast meta needs `register_post_meta` permission or the field name is wrong. The `nadlan-config` plugin v1.0.5+ registered the right names; trust them.

The 2026-05-29 spokes shipped with 4 of 7 missing meta descriptions. Google fell back to "להלן מאמר HTML נקי להדבקה" — visible in the SERP. **Do not let this happen again.**

## Step 6 — Schema upgrade (Article schema, not just WebPage)

Yoast defaults to WebPage schema. For real articles, upgrade to Article schema with author and publication date. This is set in Yoast → Search Appearance → Content Types → Pages → Schema, but for per-page override:

```python
yoast_meta['_yoast_wpseo_schema_article_type'] = 'Article'
yoast_meta['_yoast_wpseo_schema_page_type'] = 'WebPage'
```

For tax/legal/contract articles, also ensure the Person schema for the author lawyer is set (one-time owner action in Yoast → Settings → Authors).

## Step 7 — Permalink and parent

For spokes under a pillar, set the parent page ID and let WP build the URL:

```python
{
    'parent': PILLAR_PAGE_ID,
    'slug': 'short-term-rentals-portugal',
    # results in /investment/short-term-rentals-abroad/short-term-rentals-portugal/
}
```

For the abroad-pillar spokes specifically, the URL convention is:
`/short-term-rentals-{country}/` (flat under root), not under the pillar — because the pillar slug is itself `/short-term-rentals-abroad/` and we do not want the URL to stutter. This was the 2026-05-29 decision; do not change without checking the redirect map.

## Step 8 — Navigation and menus

After publishing a new pillar (rare), add it to the main menu. Spokes do not go in the main menu — they live only via internal links from the pillar and via the sitemap.

For navigation REST API on WP 7.0:

```python
requests.get(f'{BASE}/wp-json/wp/v2/navigation', auth=(USER,PWD))
# get the navigation post id, then PATCH the content with the new menu item
```

In practice: easier to ask the owner to add the menu item in wp-admin → Appearance → Menus.

## Step 9 — Sitemap and IndexNow

The `nadlan-config` plugin (v1.1.2+) auto-pings IndexNow on every `publish` event. You do not need to ping manually. To verify it fired, check the healthcheck after publishing:

```bash
curl -s "$WP_BASE_URL/wp-json/nadlan/v1/healthcheck"
# v1.2.1 adds an "indexnow_last" field
```

Yoast auto-generates the sitemap at `/sitemap_index.xml`. New pages appear within minutes. **Do not write a custom sitemap** — Yoast handles it.

## Step 10 — Update `site-state.md`

Append a block to `skills/site-state.md` recording what was published:

```markdown
## 2026-MM-DD — Published [pillar/spoke] [slug] (page id [id])
- Target query: ...
- Word count: ...
- Internal links wired: pillar [id] ✓, siblings [id, id] ✓, calculator [id] ✓, lawyer CTA ✓
- Yoast title + metadesc set ✓
- Author byline ✓ (if tax/legal)
- IndexNow ping fired ✓ (verified via healthcheck)
- Known gaps / TODOs: ...
```

This is how the next agent (or you, next session) knows what is live and what is not.

## Failure modes that have happened (DO NOT REPEAT)

| Date | What broke | Why | Detection |
|---|---|---|---|
| 2026-05-29 | 6 country spokes shipped with `&lt;h2&gt;` showing as visible text | ChatGPT output pasted into WP with HTML double-escaped | `&lt;` count in REST `content.raw` |
| 2026-05-29 | 4 country spokes missing Yoast metadesc | `meta` field not included in REST POST | `yoast_head_json.description = MISSING` |
| 2026-05-29 | All 7 spokes had only 1 internal link (to pillar) | Anti-cannibalization map skipped | Link count in body < 3 |
| 2026-05-29 | Several spokes opened with "להלן מאמר HTML נקי להדבקה" | Step 1a skipped | grep for "להלן" / "הנה המאמר" |
| 2026-05-29 | Citation footnotes "Source+9..." left in body | Step 1b skipped | regex `[A-Za-z]+\+\d+` |
| 2026-05-29 | No author byline on tax/regulation articles | Step 2 skipped | grep for "מאת" / "עורך דין" |
| 2026-05-29 | No CTA block, no monetization surface | Step 4 lawyer block skipped | grep for `cta-lawyer` class |

Every one of these would have been caught by running the checks in this protocol.

## TL;DR — the 10-second mental model

1. Sanity-check ChatGPT output (no preamble, no footnotes, no em-dashes, no AI-tells).
2. Add date + author byline + disclaimer.
3. Wrap every block in Gutenberg comments.
4. Wire 3 directions of internal links + lawyer CTA.
5. Set Yoast title + metadesc + focuskw.
6. Upgrade to Article schema if tax/legal.
7. Set parent + slug.
8. (Owner) add to menu if pillar.
9. Verify IndexNow pinged.
10. Append to `site-state.md`.

Skip any step → broken page like 2026-05-29. Run every step → live page that ranks.

---
_Created 2026-05-30 by Claude Code (claude-opus-4-7) after auditing the 7 country spokes Cowork published 2026-05-29 and finding 6 of 7 broken. This file exists so Cowork has a persistent checklist between sessions._
