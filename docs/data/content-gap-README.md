# Content-Gap Audit 2026-07 - README

Audit date: 2026-07-29. Source: https://nad-lan.co.il/nadlan_project-sitemap.xml (94 URLs; the /projects/ archive root excluded). Read-only GET crawl, sequential, ~0.4 req/s, UA NadLan-InternalContentAudit/1.0. Feeds the writing agents of the SEO war plan (docs/2026-07-29-seo-war-plan.md): every thin project page gets one mega article via docs/prompts/mega-article-master-prompt-he.md.

## Method (how each column was measured)

- words: whitespace tokens of the rendered `<main>` element after stripping script/style/noscript/template/svg and tags. This is the article + on-page module text a crawler reads, so it is the honest SEO word count. DUO = ~5,000 by this measure; the owner floor is 3,000 article words.
- has_3d: yes when the page references a project-specific .glb (anything other than the sitewide fallback standard-residential.glb) or carries an nl-mv / `<model-viewer>` marker in the HTML. The engine loader script alone does not count.
- hotspots: max(count of slot="hotspot", count of "hotspot_position" keys in the engine config JSON). Hotspots are injected client-side from that config, so the JSON key count is the real unit count.
- langs_present/missing: hreflang alternates (en/fr/ru/ar) declared on the page. Language variants also exist as separate -en/-fr/-ru/-ar URLs; those rows are tagged lang-variant in notes and are NOT article targets.
- branded_title: yes when the title core (before the site suffix) contains a Latin brand token or a quoted brand. no = generic Hebrew title, the W1 retitle target.
- city: JSON-LD breadcrumb (4-item trail) or ApartmentComplex addressLocality, else city-name match in title/H1. Blank means the page exposes no city anywhere - itself a fixable gap.
- notes: dev= developer if visible, glb= custom model, lang-variant, dup-of, junk?, wave-1, fetch_failed.

## Totals

- Project pages crawled OK: 92 (of 93 sitemap URLs; 1 fetch failures listed at the bottom of the CSV)
- Hebrew project pages (excluding 16 language-variant pages): 76
- Average words: 1270 | median: 263 | min: 114 | max: 4959
- Under 500 words: 56 (74%) | under 1,000: 56 (74%) | under 3,000 (owner floor): 56 (74%)
- With real 3D (custom glb/engine markup): 4 | with hotspot configs: 10
- Language coverage: all four (en+fr+ru+ar): 4 | partial: 0 | Hebrew only: 72
- Branded titles: 11 of 76 (14%) - the rest are W1 retitle targets
- Junk/test records flagged junk?: 0 | duplicate records flagged dup-of: 0 (skip both when assigning articles)
- Top cities by project count: תל אביב-יפו (18), רמת גן (9), בת ים (7), קרית אונו (7), תל אביב יפו (4), אשדוד (4), נהריה (3), גבעתים (3), ראשון לציון (3), רעננה (3)

## Wave 1 - the first 50 articles (rows tagged wave-1 in the CSV)

Selection rule: real, non-duplicate, non-variant projects under 3,000 words, ranked by: has 3D (+100), Sde Dov cluster (+60, war-plan W4), top-8 city hub (+40), very thin <500 (+30), hotspot config (+20), unbranded title (+10); ties broken thinnest-first. 3D pages come first because the article multiplies an experience that already converts; Sde Dov pages feed the authority cluster.

| slug | city | words | 3D | hotspots | why |
|---|---|---|---|---|---|
| רבי-עקיבא-2 | נהריה | 246 | no | 0 | city hub, very thin |
| שדרות-הגעתון | נהריה | 246 | no | 0 | city hub, very thin |
| אנצו-סירני-38-42 | גבעתים | 248 | no | 0 | city hub, very thin |
| גשם-אלי-כהן | נהריה | 253 | no | 0 | city hub, very thin |
| הרב-שאולי | אשדוד | 254 | no | 0 | city hub, very thin |
| לביא | גבעתים | 255 | no | 0 | city hub, very thin |
| מתחם-ארלוזורוב-המתמיד | רמת גן | 255 | no | 0 | city hub, very thin |
| המעפילים | אשדוד | 255 | no | 0 | city hub, very thin |
| ישעיהו | קרית אונו | 257 | no | 0 | city hub, very thin |
| הדקל | אשדוד | 258 | no | 0 | city hub, very thin |
| ערבי-נחל | גבעתים | 260 | no | 0 | city hub, very thin |
| שטרן | קרית אונו | 260 | no | 0 | city hub, very thin |
| רוטשילד | בת ים | 260 | no | 0 | city hub, very thin |
| שפירא-פעמוני-העיר | אשדוד | 262 | no | 0 | city hub, very thin |
| בלפור | בת ים | 263 | no | 0 | city hub, very thin |
| הזמיר | קרית אונו | 263 | no | 0 | city hub, very thin |
| כצנלסון | בת ים | 263 | no | 0 | city hub, very thin |
| הררי | רמת גן | 263 | no | 0 | city hub, very thin |
| המבדיל | רמת גן | 263 | no | 0 | city hub, very thin |
| ביאליק-בנימין | רמת גן | 264 | no | 0 | city hub, very thin |
| נווה-יהושע-מרכז | רמת גן | 264 | no | 0 | city hub, very thin |
| הרב-לוי-ניסנבוים | בת ים | 264 | no | 0 | city hub, very thin |
| שאול-המלך | קרית אונו | 265 | no | 0 | city hub, very thin |
| עמק-החולה | רמת גן | 265 | no | 0 | city hub, very thin |
| בר-יהודה | קרית אונו | 265 | no | 0 | city hub, very thin |
| יוספטל-מזרח | בת ים | 265 | no | 0 | city hub, very thin |
| מגדלי-הגפן-2 | רמת גן | 267 | no | 0 | city hub, very thin |
| לוי-אשכול-צפון | קרית אונו | 267 | no | 0 | city hub, very thin |
| הרוגי-מלכות-בבל-הכלנית | קרית אונו | 267 | no | 0 | city hub, very thin |
| עלית-המתמיד-ארלוזורוב | רמת גן | 267 | no | 0 | city hub, very thin |
| מגדל-הים-רוטשילד-2 | בת ים | 269 | no | 0 | city hub, very thin |
| רמת-השקמה-שקמה-על-הפארק | רמת גן | 271 | no | 0 | city hub, very thin |
| קהילת-ורשה-2 | תל אביב יפו | 369 | no | 0 | city hub, very thin |
| רקאנטי | תל אביב יפו | 371 | no | 0 | city hub, very thin |
| טאגור | תל אביב יפו | 371 | no | 0 | city hub, very thin |
| הדר-יוסף-לודג | תל אביב יפו | 371 | no | 0 | city hub, very thin |
| דניה | - | 114 | no | 0 | very thin |
| ויצמן-ז-בוטינסקי | - | 114 | no | 0 | very thin |
| בר-כוכבא-2 | - | 116 | no | 0 | very thin |
| שי-עגנון-ההסתדרות | אשקלון | 251 | no | 0 | very thin |
| כפר-גבירול | רחובות | 251 | no | 0 | very thin |
| מנדלבלט | הרצליה | 252 | no | 0 | very thin |
| סלע | ראשון לציון | 254 | no | 0 | very thin |
| הרומנים | נתניה | 255 | no | 0 | very thin |
| שוק-אשכנזי | יהוד | 257 | no | 0 | very thin |
| הקרן | מעלה אדומים | 257 | no | 0 | very thin |
| ברנדיס | רעננה | 258 | no | 0 | very thin |
| כנרת | רעננה | 258 | no | 0 | very thin |
| הנטקה | ירושלים | 258 | no | 0 | very thin |
| ויצמן | רעננה | 258 | no | 0 | very thin |

## Hand-off instruction for a writing agent (one row -> one article)

1. Take the next wave-1 row from content-gap-2026-07.csv not yet logged in AGENT-LOG.md.
2. Open docs/prompts/mega-article-master-prompt-he.md. Fill its header from the row: project name (title/H1), city, slug, dev= from notes if present, has_3d. One row per prompt run, zero placeholders left.
3. Run the prompt with a ChatGPT writing agent. Demand the QA self-check block answers at the end.
4. Verify yourself before publish: word count >= 5,000 (>= 3,000 for source-poor projects, note it), zero em/en dashes, zero banned phrases, every source URL opens, internal links present.
5. Publish into the existing project page under /projects/<slug>/ (replace the stub article body; never delete the 3D module or lead forms). Owner law: publish, do not hand off files.
6. Log slug + date + delivered word count in AGENT-LOG.md. Weekly GSC snapshot per the war plan measures the wave.

## Failures

- https://nad-lan.co.il/projects/%d7%a7%d7%a4%d7%9c%d7%9f/ (ReadTimeout: HTTPSConnectionPool(host='nad-lan.co.il', port=443): Read timed out. (read timeo)

PARTIAL RUN - regenerate after full crawl.