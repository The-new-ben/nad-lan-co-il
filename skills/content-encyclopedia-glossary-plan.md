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

**A glossary term gets its own page ONLY if no existing pillar/spoke already targets it.** If a term already has a page (see the do-not-duplicate list below), the glossary does NOT create a competing page — it either (a) skips it, or (b) creates a 1-paragraph stub that `rel=canonical`/links straight to the existing page. The glossary captures the *definition intent* of terms that currently have NO home.

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
