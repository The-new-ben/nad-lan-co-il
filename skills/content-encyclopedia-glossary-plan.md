# Skill: Real-Estate Encyclopedia / Glossary ("מילון נדל"ן") — project map

> The plan for the "Wikipedia of Israeli real estate" content layer: hundreds-to-thousands of definitional term pages (micro-spokes) that SUPPORT the pillars/spokes and capture definitional + academic + AI-deep-research queries — WITHOUT cannibalizing a single existing ranking. Owner goal: become the Israeli Zillow/Yad2/Madlan-beater on depth + trust.
>
> **STATUS: THIS IS A MAP, NOT A BUILD.** Do not write encyclopedia entries here. The build is executed as a ChatGPT-via-Cowork batch project, exactly like the 22 articles (see runbook-cowork-FULL-OPERATOR-v3.2.md + the Drive inbox pipeline). This skill defines WHAT to build, the cannibalization guardrails, the per-term template (definition + practical "coursehood" + cross-links), and the discovery priorities (esp. the English-Wikipedia-gap goldmine). When the owner gives go, the term list + master prompt feed the same ChatGPT→Drive→Cowork→publish loop.

## 1. Why this wins (strategic rationale)

- **Topical authority**: Google's June 2025 core update + GEO research reward comprehensive, credible subject coverage. A dense glossary that interlinks to the money pages raises the WHOLE cluster's authority (every glossary page is an internal link with relevant anchor text pointing UP to a pillar/spoke).
- **GEO / AI-citation**: definitional, well-structured Q&A entries with named entities + cited sources are exactly what AI Overviews / ChatGPT / Perplexity pull (Princeton GEO: quotations +41%, stats +32%, citations +30%). A glossary is GEO gold.
- **Audience we don't have yet**: field professionals (appraisers, architects, lawyers, engineers, students) and deep-research users search exact terms ("מהו שמאי מכריע", "תקן 1045 בטון"). We capture them, then funnel to pillars + services.
- **Moat**: no Israeli portal has a serious, lawyer-reviewed, Hebrew real-estate encyclopedia. Madlan has data, Yad2 has listings — neither has the *knowledge layer*.

## 2. THE IRON RULE — zero cannibalization

> **Refined 2026-06-01 by cited research — see §11 for the authoritative decision flowchart + a correction on `noindex,follow`.** §2 here is the summary; §11 governs.

**A glossary term gets its own indexable page ONLY if its search intent differs from every existing pillar/spoke focus keyword.** If intent collides, the term does NOT get a competing page — it becomes an **anchor/H2 section inside the existing article** (physically cannot cannibalize, because no second URL exists). This is stronger than the noindex trick (see §11).

### Do-NOT-duplicate list (existing focus keywords — glossary must not target these as primary):
Pillars: נדל"ן להשקעה, מכירת דירה, קניית דירה, עורך דין מקרקעין, התחדשות עירונית, נדל"ן מסחרי, מחשבון משכנתא, יעוץ מס מקרקעין.
Spokes already owning a keyword: מס רכישה (דירה ראשונה/שנייה), מס שבח (+ פטור דירה יחידה, מס שבח מופחת), היטל השבחה, תמא 38 (זכויות/חוזה), פינוי בינוי, בחירת יזם, דמי תיווך, מכירה בלי מתווך, תמחור דירה, חוק המכר דירות, אופציה במקרקעין, טופס 4, היתר בנייה, חוזה מכר דירה, ייפוי כוח נוטריוני, חוזה שכירות, השכרת משרד/חנות, משכנתא הפוכה, יחס מימון, ריבית משכנתא, כושר החזר, מינוף, השקעה דרך חברה, Airbnb, תשואה, ערבות חוק מכר, דירות להשקעה, קניית דירה שלב אחר שלב, דירה חדשה מול יד שנייה, buy-vs-rent, short-term-rentals-abroad (+7 countries), all city price pages.

**Intent split that keeps us safe:** pillars/spokes target *commercial/transactional* intent ("how much", "calculator", "guide 2026", "what to check"). Glossary targets *pure definitional* intent ("מהו X", "X פירוש", "X הסבר", "ההבדל בין X ל-Y"). Same word, different SERP — but when in doubt, **skip and link, don't duplicate.**

## 3. The whitelist — term universe with NO existing page (safe to build)

These are the categories of NEW terms (none currently targeted). This is the encyclopedia's territory:

- **בנייה וקונסטרוקציה**: בטון מזוין, כלונסאות, יסודות, שלד, קורות, עמודים, איטום, טיח, גמר, ריצוף, קונסטרוקציה, ממ"ד, גג רעפים, גג שטוח, בלוקים, גבס, תקן ישראלי 1045, תקן 413 (עמידות רעידות אדמה).
- **חומרי בניין**: בטון, פלדה, אלומיניום, זכוכית, איטונג, בלוק תרמי, בידוד תרמי, בידוד אקוסטי, צמנט, חצץ.
- **אדריכלות וסגנונות**: באוהאוס, ברוטליזם, סגנון בינלאומי, מודרניזם, פנטהאוז, דופלקס, טריפלקס, גן (דירת גן), לופט, מרתף, עליית גג.
- **תכנון עירוני**: תב"ע, תמ"מ, תמ"א, קו בניין, אחוזי בנייה, מרווחי בנייה, ייעוד קרקע, מגרש, חלקה, גוש, מקרקעי ייעוד, הפקעה, איחוד וחלוקה, מתחם.
- **משפט מקרקעין**: הערת אזהרה, זיקת הנאה, זכות קדימה, ליס פנדנס (lis pendens), בית משותף, רכוש משותף, תקנון מוסכם, צו בית משותף, חכירה, חכירה לדורות, בעלות, נסח טאבו, רישום מקרקעין, מינהל מקרקעי ישראל / רמ"י, שטר מכר, משכון, שעבוד.
- **מימון ומשכנתא**: לוח שפיצר, לוח קרן שווה, גרייס, ריבית דריבית, מדד תשומות הבנייה, צמודה/לא צמודה, פריים, ריבית קבועה/משתנה, מחזור משכנתא (already have refinance? check), בולט, גרירת משכנתא, ביטוח חיים למשכנתא.
- **מיסוי (definitional sub-terms only)**: שומה עצמית, שומה מכרעת, שמאי מכריע, יום המכירה, שווי רכישה, פחת, מס יסף, חישוב לינארי, נכס מזכה (definitional, link to the tax spokes).
- **שמאות והערכה**: שמאי מקרקעין, חוות דעת שמאית, גישת ההשוואה, גישת העלות, גישת היוון ההכנסות, שווי שוק, שווי מימוש מהיר.
- **מקצועות**: קבלן רשום, קבלן מבצע, מפקח בנייה, מהנדס קונסטרוקטור, יועץ אינסטלציה, אדריכל רשוי (definitional, link to /professionals/ directory).
- **פרויקטים וסוגי עסקה**: קומבינציה, מחיר למשתכן, דירה על הנייר, פרי-סייל, קבוצת רכישה, נדל"ן מניב, REIT, סאבלט.

Each is a definitional micro-page that **links up** to the relevant pillar/spoke. Hundreds available; thousands if we add minor terms.

## 4. Architecture

- **Content type**: a dedicated `nadlan_term` CPT (or a WP category `/glossary/` under a single archive). Recommend CPT `nadlan_term` with taxonomy `term_category` (the categories in §3) — keeps it cleanly separated from articles/pages and lets us build a A-Z index + search.
- **URL**: `/glossary/<term-slug>/` (Hebrew slug or transliterated). Archive at `/glossary/` (= "מילון נדל"ן"). A-Z + category filters.
- **Page template** (definitional core + practical "coursehood", 400-800 words):
  1. H1 = the term.
  2. **One-sentence definition first** (GEO: definitional first sentence → AI citation).
  3. 2-4 short paragraphs: what it is, why it matters in an Israeli transaction, a number/example, the law/standard reference if any.
  4. **"מדריך מעשי" / coursehood block (REQUIRED — owner-mandated):** not just a dry definition. A short practical how-this-applies section: what the reader should DO with this term, step-by-step where relevant, what to check, common mistakes, who to ask. This is what makes a landing visitor stay and convert. Example for "הערת אזהרה": how to register one, where (לשכת רישום המקרקעין), cost, how to verify one exists before buying, what to do if it's missing.
  5. **"קשור ל:"** cross-link box → links UP to the relevant pillar/spoke + 2-3 sibling terms + any relevant tool (calculator) + a service CTA. Every term is a value hub that routes the visitor deeper into the site.
  6. Optional mini-FAQ (1-2 Q&A) for PAA capture.
  7. Staff byline + "נבדק ע"י עו"ד" where legal, + sources.
- **Internal linking model (the micro-spoke engine)**:
  - Every glossary term → links to its parent pillar + 1-2 sibling terms + the most relevant spoke.
  - Each pillar/spoke → on first mention of a glossary term in its body, link DOWN to the term page (contextual, varied anchor). Do this via an automated "term linker" (match known term → first occurrence → link), idempotent.
  - Result: a dense web where the glossary feeds link equity UP and the pillars distribute crawl depth DOWN. Classic hub-and-microspoke.

## 5. Sourcing — honest + legally safe

- **Term discovery** (the LIST): scan Hebrew + English Wikipedia category trees (real estate, construction, architecture, property law, mortgage), Quora/PAA real-estate questions, academic glossaries (Technion/HUJI real-estate & civil-engineering syllabi terms), professional bodies (לשכת שמאי המקרקעין, התאחדות הקבלנים). Use these ONLY to build the term list + understand scope.
- **PRIORITY discovery channel — the "English-gap" goldmine (owner-mandated):** find terms that have an **English Wikipedia article but NO Hebrew Wikipedia article** (or only a stub). These are content gaps where almost nobody writes in Hebrew, so a quality Hebrew page can rank #1 fast and get cited by AI with little competition. Method: walk the EN Wikipedia categories (Real estate, Construction, Architecture, Property law, Mortgage, Urban planning), and for each article check whether a HE interlanguage link exists. No HE link = candidate. Examples likely to have EN-but-not-HE coverage: specific construction methods, niche financing instruments, architectural movements, planning doctrines, valuation methodologies. Tag each candidate "EN-gap" — these go to the FRONT of the build queue. (We still write original Hebrew; we do not translate Wikipedia — we cover the topic.)
- **Writing**: every definition is **original Hebrew**, written by the ChatGPT pipeline (cost-efficient) following copywriting-skill.md rules (no em/en-dash, no AI-tells, definitional lead, sources cited). **Never copy Wikipedia/Quora text** — Wikipedia is CC-BY-SA (attribution + share-alike obligations + duplicate-content/quality risk) and Quora is copyrighted. We use them as a topic map, not a text source.
- **Accuracy**: legal/tax/standard terms get a lawyer-review pass (the owner's moat) before publish; mark "נבדק ע"י עו"ד".

## 6. Phasing + governance

- **Phase A (proof, 30-50 terms)**: pick the 30-50 highest-value definitional terms with clear pillar linkage and obvious search/AI-research demand (e.g., הערת אזהרה, נסח טאבו, קומבינציה, מחיר למשתכן, שמאי מכריע, תב"ע, אחוזי בנייה, בית משותף, חכירה לדורות, לוח שפיצר). Build, interlink, measure (once GA4/Site Kit is live).
- **Phase B (scale, 200-500)**: roll category by category once the model proves it lifts the cluster and isn't cannibalizing (verify in Search Console: glossary pages rank for definitional queries, pillars hold their commercial queries).
- **Phase C (depth, 1000+)**: long-tail materials/techniques/architecture terms; known contractors/developers as NEUTRAL factual entries (company, founded, notable projects — no superlatives, no "best", to stay clean of advertising/defamation risk).
- **Governance**: batch through the ChatGPT pipeline (Drive inbox → Cowork publishes as `nadlan_term`), each batch sanity-checked (copywriting rules + cannibalization check: confirm slug + focus keyword not in the do-not-duplicate list) before publish. Append progress to site-state.md.

## 7. Quality + cannibalization gate (run per term before publish)

```
For each candidate term:
  1. Is its primary keyword in the do-not-duplicate list (§2)?  → if yes: SKIP or stub+link, do not build.
  2. Does an existing page already rank for it (Search Console)? → if yes: link, don't duplicate.
  3. Is the intent purely definitional ("מהו/פירוש/הסבר")?       → required yes.
  4. Does it link UP to a pillar/spoke?                          → required yes.
  5. Copywriting rules pass (no dashes/AI-tells, sources)?       → required yes.
  6. Legal/tax term → lawyer-reviewed?                           → required for those.
```

## 8. The Lovable / build-tool note

- **Content** = ChatGPT pipeline (NOT Lovable — Lovable builds apps/UIs, not bulk SEO content, and burns budget).
- **Lovable's useful role** = design the **glossary front-end UX** (A-Z index, category filter, term-of-the-day, search, the "קשור ל:" box, related-terms graph) as a polished component we port into the theme. A master prompt for that is worth doing AFTER the CPT + data model exist.
- A **master prompt for ChatGPT** to generate a batch of glossary entries is drafted in §9.

## 9. ChatGPT master prompt (per-batch glossary generation) — template

```
פרויקט: מילון נדל"ן של nad-lan.co.il. כתוב N ערכי מילון קצרים (250-450 מילים כל אחד) למונחים הבאים: [רשימת מונחים מקטגוריה X].
לכל ערך:
- כותרת H2 = המונח.
- משפט הגדרה ראשון, חד וברור ("X הוא...").
- 2-3 פסקאות: מה זה, מתי זה רלוונטי בעסקת נדל"ן ישראלית, מספר/דוגמה, והפניה לחוק/תקן אם יש.
- בלוק "מדריך מעשי" (חובה): מה לעשות עם המונח הזה בפועל, צעד אחר צעד היכן שרלוונטי, מה לבדוק, טעויות נפוצות, ולמי לפנות. לא רק הגדרה יבשה: ערך מעשי שגורם לקורא להישאר.
- בלוק "קשור ל:" עם קישורים פנימיים אל [pillar/spoke הרלוונטי] + 2-3 מונחים אחים + מחשבון רלוונטי אם יש + CTA לשירות.
חוקי כתיבה: בלי קו מפריד ארוך, בלי en-dash, בלי "חשוב להבין/מהווה/בעידן/לסיכום", הגדרה עובדתית, מקורות ראשוניים (חוק, תקן, רשות). פלט HTML עם <h2>/<h3>/<p>/<ul>/<strong> ו-dir="rtl". שמור כל ערך כקובץ Google Doc בתיקיית inbox בשם glossary-<slug>.html.
הערה: עדיפות למונחים שיש עליהם ערך בוויקיפדיה האנגלית ואין בעברית (פער תוכן = דירוג ראשון מהיר). אל תתרגם מוויקיפדיה, כתוב מקור בעברית.
```

## 10. Integration with the proptech roadmap

The glossary is the **content moat** that complements the **tech moat** in proptech-adoption-roadmap.md. Together: tools (AVM, tax calc, contract-checker) + knowledge (encyclopedia) + listings (catalog) + trust (lawyer-reviewed) = the Israeli Zillow/Madlan-beater. The glossary is low-risk (no cannibalization), high-GEO-value, and buildable now via the existing ChatGPT pipeline while traffic grows.

_Created 2026-06-01 by Claude Code (claude-opus-4-8). Cannibalization guardrail = the 100-page keyword inventory captured in site-state. Build in governed batches via the ChatGPT pipeline; Lovable only for the front-end UX component._

---

## 11. Research-backed build spec (2026-06-01) — AUTHORITATIVE

Cited from a deep research pass (Wikipedia MOS, Google canonical/noindex docs, Mueller statements, schema.org, GEO sources). This section governs where it conflicts with earlier notes.

### 11a. Wikipedia/Wikimedia STYLE — the page template to replicate (RTL-adapted)
Per Wikipedia Manual of Style / Layout, top → bottom:
1. **Hatnote** ("ראו ערך מורחב: …" / "לא להתבלבל עם …") — disambiguation/cross-ref, first screen.
2. **Infobox** (תיבת מידע) — structured fact box. **Place on the LEFT for our Hebrew RTL site** (Wikipedia puts it right on LTR).
3. **Lead section** (פסקת פתיחה) — definition-first, term in bold in the first sentence, no bullets. This is the block AI engines extract/cite. Most important.
4. **Table of contents** (תוכן עניינים) — auto from H2/H3 when 4+ sections.
5. **Body** (H2/H3 hierarchy) + the practical "מדריך מעשי" coursehood block (owner-mandated, §4).
6. **ראו גם / See also** — bulleted internal related-term links only.
7. **מקורות / References** — citations (a minimal valid entry = lead + references).
8. **תבנית ניווט / navbox** — bottom grouped links (e.g., "מונחי משכנתא").
9. **קטגוריות / Categories** — classification for browse/discovery.
Plus **disambiguation pages** where one Hebrew term has several real-estate meanings (stub listing the meanings, each linking out).

### 11b. WordPress implementation — DECISION: CPT on the MAIN domain
- **Build a `nadlan_term` CPT with a wiki-style template + CSS on the main domain.** Reason: shares existing domain authority + internal-link graph; full per-term control of canonical/robots/schema (essential for the cannibalization defense); one stack for a solo operator.
- **Do NOT run MediaWiki on a subdomain.** Google treats a subdomain as a substantially separate site → splits authority → the topical-authority transfer to our pillars is lost. Confirmed (Pagely).
- Optional bootstrap: the **Encyclopedia/Glossary/Lexicon plugin by Daniel Stelter (Eickmeyer)** creates its own CPT with A-Z, autocomplete, SEO URLs. If used: **DISABLE its auto-"linkify" feature** — auto-linking carpet-bombs pillar/spoke articles with links to thin term pages and destroys anchor discipline (a real cannibalization vector). Keep canonical/robots control.

### 11c. Cannibalization defense — CORRECTED + ranked
1. **Intent separation (primary).** Google tolerates the same keyword on multiple pages when intent differs. Glossary = purely definitional ("מה זה X" — definition, formula, history). Pillar/spoke = transactional/advisory ("X — כמה, איך, מדריך 2026"). Different title, H1, angle. Safe when intent is genuinely distinct.
2. **ANCHOR-IN-EXISTING (safest).** If intent collides with an existing focus keyword, do NOT create a page — add the term as an H2 section with an `id` anchor inside the existing spoke, and point all "definition" internal links to that anchor. No second URL = cannot cannibalize. **Default choice when in doubt.**
3. **Canonical → pillar (near-duplicates only).** `rel=canonical` from term to pillar ONLY when the term page is essentially a thin duplicate. Google may ignore a canonical between genuinely different pages. **NEVER combine canonical with noindex** (Google rejects the contradiction).
4. **`noindex,follow` — CORRECTION to earlier advice.** It removes the page from the SERP (so it can't out-rank the pillar) — but it does **NOT durably preserve internal-link equity**. John Mueller confirmed long-term `noindex` decays to `noindex,nofollow`: Google stops recrawling, drops it, and stops following its links. So: use `noindex,follow` only for thin/navigational terms, and **never make a noindexed term the sole link path to another page** (any page it links to must also be reachable from indexable pages — pillars, navboxes, sitemap). Reassess noindexed terms in ~6 months: promote to index or fold into a parent term.
5. **Anchor/link discipline.** Glossary links UP to the canonical pillar with the **bare term** as anchor (not the money keyword). Pillars link DOWN to terms sparingly. Always link to the canonical URL.

### 11d. Per-term DECISION FLOWCHART (run on every candidate; first match wins)
```
Q1. Same search INTENT as an existing pillar/spoke focus keyword?
      YES → ANCHOR-IN-EXISTING (H2+id inside that article). No new URL.
      NO  → Q2
Q2. Purely definitional, intent clearly DIFFERENT from any pillar?
      YES → FULL INDEXABLE term page. Self-canonical. DefinedTerm schema. Link up to pillar.
      NO  → Q3
Q3. Overlaps a pillar keyword BUT has real encyclopedic value?
      YES → build + rel=canonical → pillar (no noindex). Ensure its links are also reachable elsewhere.
      NO  → Q4
Q4. Thin / near-zero volume, needed only for completeness or navigation?
      YES → noindex,follow (treat equity as temporary; never sole link path). Reassess in 6 months.
      NO  → Q5
Q5. No volume, no encyclopedic value, no nav need?
      → SKIP.
```
Default bias for a rankings-protective site: when torn between INDEX and ANCHOR-IN-EXISTING → choose ANCHOR.

### 11e. Schema
- Glossary index page → `DefinedTermSet` (name, url, hasPart → term @ids).
- Each term page → `DefinedTerm` (name, description, inDefinedTermSet), JSON-LD. Rich indexable terms can ALSO carry `Article`.
- **Honest flag:** `DefinedTerm`/`DefinedTermSet` produce **no dedicated Google rich result** and are **not a confirmed ranking boost**. The verified benefit is machine-readability / entity clarity / AI-citation grounding. Don't promise a SERP visual from it.

### 11f. The SEO/GEO upside (why it's worth it)
GEO research lists glossaries (definitions + disambiguation) alongside pillars/FAQs as content that wins AI citations — "definitional clarity strengthens semantic coverage and increases citation eligibility." Definition-first leads are exactly what AI Overviews / ChatGPT / Perplexity extract. A comprehensive Hebrew term set signals nad-lan.co.il is the authoritative entity hub for Israeli real estate, strengthening the pillars it links to. Priority = English-Wikipedia-gap terms (no HE competitor = fast #1 + AI citation with little competition).

### 11g. Build path (unchanged)
Map (this skill) → term list with per-term flowchart verdict → ChatGPT master prompt (§9) → Drive inbox → Cowork publishes as `nadlan_term` (or anchor-edits into existing spokes) → /glossary/ index with A-Z + DefinedTermSet. Lovable only for the front-end UX component (infobox, A-Z, related-terms graph), not content.

Sources: Wikipedia MOS/Layout, MOS/Lead, MOS/Infoboxes; Google consolidate-duplicate-URLs + canonicalization docs; Search Engine Roundtable (Mueller long-term noindex→nofollow); Sitebulb; Backlinko/Yoast/Semrush (cannibalization); schema.org DefinedTerm/DefinedTermSet; Search Engine Land GEO; Pagely (WP wiki / subdomain authority); Barn2/Bloggerpilot (glossary plugins).

---

## 12. Wikipedia/Wikimedia community-evidence integration patterns (2026-06-01)

> Research pass mining Wikipedia MoS, Wikipedia talk archives, WordPress.org plugin support threads, and SEO case studies (Investopedia). Honest evidence-strength flags. This is the patterns shortlist; per-term flowchart in §11 still governs.

### Ranked shortlist (use this when wiring a term into the site)

**1. ANCHOR-IN-SPOKE (term = H2 with `id` inside its owning spoke, no new URL).** Evidence: **STRONG**. Direct Wikipedia parallel: `{{R to section}}` / targeted redirects. Zero cannibalization vector because no second URL exists. *Use when:* the term's meaning is fully owned by one pillar/spoke and other pages only need to reference it. **This is our default.**

**2. PRIMARY-HOME + sibling section-links.** Evidence: STRONG (Wikipedia) / MEDIUM (SEO). When a term is relevant to several pillars, pick the single best-fit pillar as **owner**, place the term there as H2#id, and link `/owner-spoke/#term-id` from siblings. *Use when:* the term is multi-pillar but one is clearly primary. — This is the answer to the owner's worry "but the term is relevant to many pages": **pick one owner, link to its anchor from the others, never duplicate the definition across pages.**

**3. INLINE GLOSS (short concise definition embedded in body, no link, no separate entry).** Evidence: MEDIUM. Wikipedia MOS:UNDERLINK explicitly endorses "a concise definition instead of or in addition to a link." Zero risk because nothing exists outside the article. *Use when:* the term needs in-context clarity but a separate destination would add no value.

**4. HATNOTE-STYLE DISAMBIGUATION per pillar.** Evidence: MEDIUM. When one Hebrew term has multiple real-estate meanings, do NOT create a standalone disambiguation page (that's the thin-content trap that competes with both real homes). Each pillar that owns a sense puts a one-line hatnote at the top: "ערך זה עוסק ב-X. למשמעות Y ראו [pillar Z]." *Use when:* the same Hebrew word has distinct meanings owned by different pillars.

**5. THICK STANDALONE TERM PAGE with deliberately NARROWED practical block (Investopedia /terms/ model).** Evidence: MEDIUM (one strong case: Investopedia). The term page covers what/why/who/which-form + **outbound government link** + internal link UP to the pillar's how-to. Critically, the practical block must be **strictly thinner than the pillar's** — names the form/authority, doesn't reproduce the full how-to. *Use when:* the term genuinely needs a standalone URL (backlinks, AI-overview citations, English-Wikipedia-gap term with real search demand) **AND** you can hold the line that its action section stays narrower than the pillar's.

### Anti-patterns (do NOT do — research-backed)

- **DO NOT** create standalone glossary entries that duplicate a pillar's how-to content. (Direct practitioner warning: "the glossary can rank too well, causing Google to send traffic to the glossary instead of your blog post." — Content Powered.)
- **DO NOT** put a "ראו גם / See also" block that lists glossary links already present in the body. Wikipedia MoS/Layout explicitly prohibits this: "The 'See also' section should not repeat links that appear in the article's body." Signal dilution + redundant cues. The "See also" block is ONLY for related terms the article does NOT already mention inline.
- **DO NOT** enable plugin auto-tooltip "link every occurrence." WordPress.org support threads show practitioners actively backing off this. Apply Wikipedia MOS:DUPLINK: **link a term at most once per major section, first occurrence only.** Inside the glossary itself, repeat linking is acceptable; in spoke articles it is not.

### Anchor-text rule (Wikipedia MOS:DUPLINK + RTL note)
- Pillar/spoke → glossary anchor: **bare-term anchor only**, on **first occurrence per section**, not the money keyword. Disable plugin "linkify all" features.
- RTL caveat: Hebrew prefix letters (ה־, ב־, ל־, ש־, מ־) cause false-positive matches in naive auto-linkers. If we use Glossary by Codeat or similar, configure word-boundary detection carefully or rely on manual linking. Implementation issue, not SEO.

### "Coursehood" + government-link discipline (owner non-negotiable)
Per the owner's locked rule: every term page (and every spoke) pairs definition with a **practical action layer + direct government links**: לשכת רישום המקרקעין (Tabu), רשות המסים (Israel Tax Authority), רמ"י (Israel Land Authority), מינהל התכנון (Planning Administration), רשם הקבלנים (Contractor Registrar), משרד המשפטים (forms portal), בנק ישראל (mortgage rules). On a term page using Pattern #5, this block is **deliberately narrower** than the parent pillar's how-to — names the authority/form + outbound gov link + internal link to the pillar — so the term doesn't out-rank the pillar's transactional guide.

### Honest evidence flags
- Reddit (r/SEO, r/bigseo, r/TechSEO) and Moz were blocked to the research crawler — practitioner Search Console post-mortems specifically on glossary cannibalization are NOT publicly available in what we could reach. The cannibalization risk is real in principle (and well-documented for generic page-vs-page competition), but WordPress-glossary-specific forensic data is a gap.
- Investopedia is the one strong case for the thick-term-page pattern. Second independent case (nolo.com / gov.uk) not found at equivalent depth.
- Hebrew/RTL-specific cannibalization evidence: none found. RTL concerns are implementation (word boundaries), not SEO outcome.

### When we resume the glossary build (later, after Zillow stable)
Default to Pattern #1 (anchor-in-spoke). Use Pattern #2 for multi-pillar terms. Use Pattern #5 only for English-Wikipedia-gap terms with real demand. NEVER use noindex,follow as the primary defense (owner does not trust it; research confirms equity decay). The build still runs through ChatGPT→Drive→Cowork→publish, but Cowork's job is now mostly "anchor-edit into the right spoke" rather than "publish a new term page."

Sources: Wikipedia MoS/Layout, MoS/Linking (DUPLINK/OVERLINK/UNDERLINK), MoS/Glossaries, MoS/Disambiguation, Redirect (R to section); WordPress.org plugin support indices (CM Tooltip Glossary, Glossary by Codeat); Content Powered glossary cannibalization article; Investopedia SEO case study (spicymargarita.co); Search Engine Land cannibalization guide.
