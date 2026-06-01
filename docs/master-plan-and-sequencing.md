# nad-lan — Master plan & sequencing (owner decision, 2026-06-01)

> Owner asked me to own the order and reduce overwhelm. This is the decided plan: what to build, in what order, who does each piece, and why. Honest SEO rationale, not flattery. The grand vision (owner's words): map the **entire "bill of materials" of real estate** — every term, every material, every professional (lawyer/accountant/advisor/bank), every project — so Google + AI engines see a one-stop-shop "world", and every piece passes link equity UP to the money pillars (the hard, competitive keywords). We go for the big keywords, not leftovers.

## The honest sequence (why this order)

Our domain is **new = low authority**. You cannot win "נדל"ן להשקעה" (top KD) cold. So we build authority from the bottom up while the conversion pages wait for link equity:

| # | Wave | Why now | Who | Status |
|---|---|---|---|---|
| **1** | **Glossary (Wikipedia-orphan terms)** | Lowest competition (no Hebrew article = fast #1), compounds topical authority, each term links UP to a money pillar. The cheapest kick. | Infra: **Claude Code (done, v1.17.0)**. Content: **Cowork + ChatGPT** batch (runbook v3.2). Discovery: **Claude Code + Lovable** verify Wikipedia void. | **KICKED OFF** |
| **2** | **Directory inventory** (contractors/projects/professionals) | Thousands of indexable entity pages = inventory Google rewards; tier-gated so no free advertising. | Infra: **done (v1.5.0/v1.16.0)**. Run import + enrich: **Cowork** (missions M2-M4). | Ready; needs PR #4 merged |
| **3** | **Calculator + money pillars** | The conversion/revenue pages. Built once #1-#2 feed link equity. | Calc infra: **Claude Code**. Long-form: **Cowork + ChatGPT** per skills. | Next |
| **4** | **Competitive intel** (nadlanmaster + Zillow architecture) | Informs WHICH pillars/keywords to prioritize in #3. Runs in parallel. | **Lovable** (own crawler) + **Cowork** synthesis. | Prompt ready (below) |
| **5** | **Foreign RE** | Last + careful (see rule below). | Cowork + ChatGPT, spoke-level. | Deferred |

**Bottom line:** #1 and #2 run NOW in parallel (different tools, no collision). #3 I build the shells now, content follows. #4 is intel that tunes #3. #5 waits.

---

## Who does what (tool assignment)

- **Claude Code (me):** all plugin/theme CODE, infrastructure, schema, page shells/templates, the importer, data models, sequencing, prompts, and reviewing Cowork/Lovable output for cannibalization + quality-gate compliance. I do NOT hand-write 200 Hebrew articles (that's the batch pipeline).
- **Cowork + ChatGPT (the proven batch loop, runbook v3.2 → Drive → publish):** all long-form Hebrew CONTENT at scale — glossary terms, card enrichment, pillar/spoke articles. This is the content factory. It already produced 22 articles successfully.
- **Lovable:** competitive intelligence via its **own web crawler** (not Semrush-on-us — our site is too new, Semrush has nothing yet). Crawl nadlanmaster + Zillow, extract architecture/content-construction patterns. Also can build front-end UX experiments.
- **Codex:** design/theme polish (green canonical palette) + block patterns when needed.
- **Owner:** the few things only you can do — merge PR #4 + WP "Update" click; paste the Lovable/Cowork prompts; approve prices (Pro/Premier); the lawyer-profile inputs; decide foreign-RE go/no-go per the rule below.

---

## WAVE 1 — Wikipedia-orphan glossary: KICKED OFF

**Infra shipped (v1.17.0, `inc/glossary.php`):** `nadlan_term` CPT at `/glossary/`, category taxonomy, per-term template (definition + "מה זה אומר בפועל" practical block + source + cross-link UP to the money pillar), `DefinedTerm`/`DefinedTermSet` JSON-LD (AI-citation bait), A-Z index shortcode, thin-content noindex until enriched, `import-enrich` accepts terms. See the live look in `docs/previews/nadlan-preview.html` (the "כלונסאות" example).

**The play (from skills/content-encyclopedia-glossary-plan.md):** prioritize terms with an **English Wikipedia article but NO Hebrew one** — content gap = fast #1 + zero cannibalization (pure definitional intent ≠ our transactional pillars).

**Starter term batch (≈60 — verify he.wikipedia void per term before publish):**

*בנייה וקונסטרוקציה:* כלונסאות, בטון מזוין, בטון דרוך, קורת מעבר, רפסודה (יסוד), כלונס קדוח, איטונג, בלוק תרמי, גשר תרמי, בידוד אקוסטי, תקן ישראלי 1045 (בידוד תרמי), תקן 413 (עמידות רעידות אדמה), תקן 940 (יסודות), קיר דיפון, אלמנט מתועש, בנייה טרומית.
*אדריכלות:* באוהאוס, ברוטליזם, סגנון בינלאומי, רציונליזם אדריכלי, פנטהאוז (מקור המונח), דופלקס, טריפלקס, מזנין, לופט.
*תכנון עירוני:* תב"ע, תמ"מ, תמ"א, קו בניין, אחוזי בנייה, מרווחי בנייה, ייעוד קרקע, איחוד וחלוקה, הפקעה, זכויות בנייה, מתחם, מגרש מינימלי.
*משפט מקרקעין:* זיקת הנאה, זכות קדימה, ליס פנדנס (Lis pendens), בית משותף, רכוש משותף, צו רישום בית משותף, חכירה לדורות, נסח טאבו, שטר מכר, משכון, שעבוד, זכות מעבר.
*מימון:* לוח שפיצר, לוח קרן שווה, גרייס (משכנתא), ריבית פריים, מדד תשומות הבנייה, אמורטיזציה, בלון (הלוואת בלון).
*שמאות:* גישת ההשוואה, גישת העלות, גישת היוון ההכנסות, שווי שוק, שווי מימוש מהיר, שמאי מכריע, פחת (שמאות).
*עסקאות/סוגים:* קומבינציה (עסקת קומבינציה), פרי-סייל, קבוצת רכישה, נדל"ן מניב, REIT (קרן ריט), סאבלט, אופציה במקרקעין.

> Many of these (כלונסאות, ליס פנדנס, גישת היוון, לוח שפיצר, איחוד וחלוקה, גרייס) have a robust EN concept but thin/absent HE Wikipedia — exactly the goldmine. **Verification step is in the prompt below.**

**Master prompt for the Cowork+ChatGPT batch (paste into the runbook v3.2 loop):**

```
ROLE: אתה כותב ערכי מילון נדל"ן מקוריים בעברית (סגנון ויקיפדיה, עובדתי וניטרלי)
עבור nad-lan.co.il. כל ערך הוא מונח הגדרתי שמדרג על "מהו X" ומקשר מעלה לעמוד כסף.

לכל מונח ברשימה:
1. ודא שאין ערך ויקיפדיה עברי קיים למונח (חפש "המונח site:he.wikipedia.org").
   אם קיים ערך עברי מקיף — דלג וסמן "HE-WIKI EXISTS, skip" (כדי לא להתחרות).
2. אם אין — כתוב ערך מקורי 150-280 מילים:
   - פסקת הגדרה (מה זה, באיזה הקשר נדל"ני).
   - פסקת עומק (איך זה עובד / סוגים / נתון מספרי אם רלוונטי).
   - בלוק "מה זה אומר בפועל עבורכם" (קונה/מוכר/משקיע — הסבר יישומי).
   - שורת מקור (תקן ישראלי / חוק / רשות מוסמכת — לא ויקיפדיה).
3. כללי קופי (חובה, מתוך הרולבוק §8.3): ללא מקפים ארוכים (—), ללא סמני AI
   ("במאמר זה", "לסיכום", "חשוב לציין"), ללא שפת SEO, ללא הייפ. עברית RTL נכונה.
4. ייחודי 100% — נסח מחדש, אל תעתיק מוויקיפדיה או ממתחרה.

לכל ערך החזר JSON: { title, term_en, wikipedia_en, related_pillar, related_anchor,
source_url, source_label, body_html }. related_pillar = עמוד הכסף הרלוונטי
(למשל מונחי בנייה → /real-estate-lawyer/ או מדריך רכישה מקבלן; מונחי מימון →
עמוד משכנתא; מונחי שמאות → עמוד שווי דירה). דחוף דרך POST /nadlan/v1/import-enrich
(post_id של ה-nadlan_term שניצור, או צור דרך REST).

הרשימה: [60 המונחים מהבאצ' למעלה]
```

**Assignment:** Claude Code creates the empty `nadlan_term` stubs (via REST/CLI) + the related_pillar mapping; Cowork+ChatGPT writes the bodies and pushes via `import-enrich`; Lovable/Cowork does the he.wikipedia void verification. Target first batch: 60 terms → expand to the full whitelist (~200) in skills/content-encyclopedia-glossary-plan.md §3.

---

## WAVE 4 — Improved Lovable mission (repointed, per owner feedback)

> Owner correctly noted: Semrush has **no data on our new site yet**, so don't rely on "our keyword gap." Use **Lovable's own crawler** on the competitors, and go deep on **how their content is built and architected** (owner's specific ask).

```
ROLE
You are a senior SEO + content-architecture analyst. Use your own web crawling/
analysis (do NOT depend on Semrush having data for nad-lan.co.il — it is a brand-
new site with no history). Where you DO have Semrush data on the COMPETITORS, use
it and cite it; otherwise crawl and analyze directly and say so.

TARGETS
1. nadlanmaster.co.il (our closest WordPress competitor)
2. madlan.co.il (the intelligence leader)
3. zillow.com (global gold standard, for architecture patterns only)

FOR EACH TARGET, produce a deep architecture + content-construction breakdown:
A. SITE ARCHITECTURE: silo/hub structure, URL patterns, how categories/pillars/
   spokes interlink, depth (clicks from home), how many internal links per page,
   breadcrumb structure, sitemap segmentation.
B. CONTENT CONSTRUCTION (owner's priority): take 5 of their top pages and dissect
   HOW each page is built — section by section: H1 pattern, intro structure, the
   order of blocks (data table? calculator? FAQ? map? lead form?), word count,
   media used (photos/renders/video/floorplan/3D), schema types, the internal-
   link pattern (what they link UP/DOWN to), and the exact CTA placement. I want a
   repeatable TEMPLATE I can hand to my content team.
C. KEYWORD FOOTPRINT (competitor only, Semrush where available): their top 30
   ranking keywords with position, volume, KD, intent, landing URL. For each, mark
   if it is a money/commercial keyword vs informational.
D. CONTENT-GAP / WIKIPEDIA-VOID: identify Hebrew real-estate topics where there is
   high search interest but weak/no authoritative page AND no Hebrew Wikipedia
   article (cross-check he.wikipedia.org). These are our priority targets.
E. MONETIZATION: how each target makes money (sponsored placements, developer
   landing pages, lead forms, directories, ads) — with the on-page evidence.

EXCLUDE from any "build this" recommendation (we already own these):
/real-estate-lawyer/, /contract-audit/, and any /city/<city>/{contractors|projects|
properties}/ hub.

DELIVERABLE (single Markdown report):
1. Per-target architecture map (diagram-as-text ok).
2. A reusable PAGE TEMPLATE for: (a) a money pillar, (b) a city hub, (c) a project
   landing page, (d) a guide/spoke — distilled from what actually ranks.
3. Top 30 cannibalization-safe target keywords ranked by ROI (commercial value vs
   difficulty), each with the page-type to build and the pillar it feeds.
4. Top 20 Wikipedia-void Hebrew terms (for our glossary).
5. Honest assessment: where each competitor is strong/weak, and the 5 highest-
   leverage moves for a NEW site to climb fastest.

CONSTRAINTS: don't invent metrics; mark [crawled] vs [Semrush] vs [estimated].
Hebrew SERP context (IL volumes), not global. Quote Hebrew verbatim.
```

---

## Foreign real-estate — the safe-integration rule (owner wants it, carefully)

Owner: we already have short-term-rent-abroad spokes (Thailand, Dubai, Italy, Spain, Cyprus, Greece — see skills/spoke-prompts-short-rent-abroad.md). We DO want investment-abroad and to be first, but must **not signal to Google that we're a non-Israeli site.** Rule:

1. **Establish Israeli authority FIRST** (Waves 1-3). Foreign content comes after the IL core is dense.
2. **Spoke-level only, never a top-nav pillar.** No "נדל"ן בחו"ל" in the main menu. Foreign pages live as spokes under an investment pillar, reachable but not emphasized.
3. **Cap internal links to foreign pages.** Monitor: foreign pages should receive a small minority of internal links vs Israeli pages (keep the site's internal-link "center of gravity" Israeli). Rule of thumb: < 10% of internal links point abroad until IL authority is proven.
4. **Frame as "השקעת ישראלים בחו"ל"** (Israeli-investor angle: tax, regulation, repatriation) — keeps topical relevance Israeli, not "we are a Cyprus brokerage."
5. **Separate the hreflang/geo signals**: keep `he-IL` primary; don't add foreign-language versions.
6. **Reuse the directory infra** (CPTs are generic) — a Cyprus project is just a `nadlan_project` with country meta; no new architecture.

> I will add a `country` meta to `nadlan_project` (default "IL") when Wave 5 starts, plus an internal-link-budget monitor in the ops dashboard, so we can SEE the IL-vs-abroad link ratio.

---

## Cards & media plan (the "how do they look" question)

- **Visual answer:** see `docs/previews/nadlan-preview.html` — basic/free-locked/Pro/Premier cards, a glossary term page, and a city hub, all in the design system.
- **Basic (free/stub):** registry facts only (name, city, classification), claim CTA. Indexable (SEO inventory) but no contact/photos.
- **Pro:** contact + photos + active lead form.
- **Premier:** Pro + "מאומת" badge + priority sort.
- **Media (the open question — plan):** owner-uploaded only at Pro+ (we never host unlicensed images on free cards). For projects, developer supplies renders/gallery/video/3D (Kuula) at the paid tier — the media module (v1.10.0) already supports tour_url/video_url/floorplan_url + photos_csv. For glossary/guides, use licensed/own diagrams only (no stock-scrape). **Research note (catalog sites):** freemium is standard (83% of top apps) — basic browse free, rich media + contact behind paywall; we match this with the tier module (v1.16.0).

---

## What's live in PR #4 after this turn
Plugin **v1.17.0**, 23 modules. New since last summary: tier paywall (v1.16.0) + glossary engine (v1.17.0). Preview mockup at `docs/previews/nadlan-preview.html`. Nothing live until PR #4 merges + WP Update. GA4 confirmed working (incognito) — disable my hardcode after merge.
