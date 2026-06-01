# Two ready-to-paste prompts: Lovable (competitor intel) + Cowork (glossary kickoff)

> Built 2026-06-01. The Lovable prompt is modeled on the Codex research prompt that produced the strong rulebook (skills/original-prompt-2026-05-28.md) — same 8-point deliverable rigor — but repointed at Lovable's own crawler (Semrush has no data on our new site yet) and instructed to also scan OUR site. The Cowork prompt follows the proven operator-brief structure (skills/cowork-prompt-business-readiness.md): from-scratch reminder of rules + skills + iron rules + obstacle handling.

---

## PROMPT A — LOVABLE (competitor architecture + content hierarchy + gap analysis)

```
ROLE
You are a senior SEO + content-architecture analyst. Use your OWN web crawling and
analysis. Do NOT assume Semrush has data on nad-lan.co.il — it is a brand-new site
with little history. Where Semrush HAS data on the COMPETITORS, use it and label it
[Semrush]; otherwise crawl directly and label it [crawled] or [estimated]. Never
invent numbers.

MARKET: Israeli residential + investment real estate. Hebrew, RTL. The goal is to
win the HARDEST, highest-commercial-intent keywords (not easy long-tail) and to map
the full "world" of real estate so Google and AI engines treat the site as the
one-stop authority. Long-tail/definitional content exists only as spokes that pass
link equity UP to the money pillars.

SITES TO ANALYZE
- OUR site (scan it, find what is thin/missing): https://nad-lan.co.il
- Primary competitor (WordPress, beat this one): https://www.nadlanmaster.co.il
- Intelligence leader: https://www.madlan.co.il
- Volume leader: https://www.yad2.co.il/realestate
- Global architecture benchmark (patterns only): https://www.zillow.com

DELIVERABLE — a single Markdown report with these 8 sections:

1. COMPETITOR DNA TABLE: per site — business model, traffic/authority signals
   [Semrush where available], strongest pages (URLs), design DNA, copy style,
   trust signals, lead-capture mechanism, monetization paths (with on-page
   evidence). Include OUR site's current state honestly (likely thin).

2. CONTENT CONSTRUCTION TEMPLATES (highest priority — this is what I most need):
   Take the 5 top-ranking pages of nadlanmaster + madlan and dissect HOW each is
   built, section by section: H1 pattern, intro structure, block order (data
   table / calculator / FAQ / map / lead form), word count, media used
   (photos/renders/video/floorplan/3D), schema types, internal-link pattern
   (what they link UP and DOWN to), exact CTA placement. Distill into a REUSABLE
   page template for each of: (a) money pillar, (b) city hub, (c) project landing
   page, (d) guide/spoke. I will hand these templates to my content team.

3. KEYWORD CLUSTERS BY MONEY PRIORITY: the hardest commercial Israeli RE keywords,
   grouped by intent (commercial / commercial-investigative / informational) and
   funnel stage (TOFU/MOFU/BOFU). For each: volume, KD, CPC, intent [Semrush where
   available, else estimated + labeled]. Rank by ROI = (commercial value × volume) /
   difficulty. We WANT the hard ones; flag which are realistic for a new site in
   6 vs 12 months.

4. CONTENT GAPS + WIKIPEDIA VOID: Hebrew RE topics with real search interest but
   weak/no authoritative page. CROSS-CHECK he.wikipedia.org for each — flag topics
   that have an English Wikipedia article but NO Hebrew one (these are our highest
   priority: near-zero competition, fast #1). Give at least 25 such terms.

5. HOMEPAGE STRUCTURE: based on what works for the leaders, the exact sections,
   order, CTA logic, search/filter module, trust/data sections, and mobile layout
   for a "quiet authority" Israeli RE homepage. (We will redesign our homepage; it
   currently looks weak.)

6. PILLAR ARCHITECTURE + INTERNAL-LINK MODEL: the silo map (buying / selling /
   investment / city / neighborhood / project / price / mortgage / tax-legal /
   urban-renewal / commercial) and how spokes link up to pillars. Note max internal
   links per page the leaders use.

7. MONETIZATION MAP: how each competitor makes money, with evidence (sponsored tags,
   tracking params, developer landing pages, directory tiers, lead forms).

8. HONEST VERDICT + "BUILD-NOW" LIST: where each competitor is strong/weak, and the
   8 highest-leverage moves for a NEW low-authority site to climb fastest. Be
   blunt; do not flatter.

EXCLUDE from any "build this" recommendation — we ALREADY OWN these pages, do not
tell us to build them:
  /real-estate-lawyer/ , /contract-audit/ , and any
  /city/<city>/{contractors|projects|properties}/ hub.

CONSTRAINTS
- Israeli SERP context (IL search volumes), never global numbers.
- Quote Hebrew verbatim; do not translate competitor copy.
- Label every metric [Semrush] / [crawled] / [estimated]. No invented figures.
- Foreign-market keywords (Portugal/Cyprus/Greece/Dubai/etc.): put them in a
  SEPARATE block at the end — do not mix into the main IL recommendations.
```

---

## PROMPT B — COWORK (glossary kickoff: Wikipedia-orphan Hebrew terms)

```
COWORK ACTIVATION — NADLAN GLOSSARY (WIKIPEDIA-ORPHAN) BATCH
============================================================
You start with NO memory. Read this whole brief, then execute non-stop until §STOP.
The owner is offline; do not ask for approvals. "Continue" is the answer for any
in-scope item.

WHO YOU ARE: the OPERATOR. You orchestrate the content loop and push to WordPress.
You do NOT hand-write the Hebrew yourself — ChatGPT writes the prose (preserve
tokens). You create the term records, route writing to ChatGPT, verify, and publish.

ACCESS (verify; never claim you lack it):
- Repo: /home/user/nad-lan-co-il (branch claude/charming-meitner-mwVEW; main is now
  merged with plugin v1.18.0).
- WordPress REST admin via env WP_BASE_URL / WP_USER / WP_APP_PASSWORD (create an
  Application Password in WP Admin → Users → Profile if missing).
- ChatGPT via the owner's Project (for Hebrew prose).
- Drive MCP (mistabrajustice@gmail.com) for Doc handoffs if needed.

MANDATORY READING AT SESSION START (one pass, in order):
1. skills/nadlan-seo-content-design-monetization-rulebook.md  ← THE rulebook,
   especially §3.6 (cannibalization), §6 (silo linking), §8.3 (Hebrew copy rules).
2. skills/content-encyclopedia-glossary-plan.md  ← the glossary plan + term whitelist
   + the IRON RULE (zero cannibalization).
3. docs/master-plan-and-sequencing.md  ← "WAVE 1" has the 60-term starter batch.
4. skills/site-state.md (last 6 blocks) for current state.

IRON RULES (non-negotiable, from rulebook §8.3):
- 100% ORIGINAL Hebrew. Never copy a sentence from Wikipedia or any competitor.
- NO long dashes (—). Use comma, period, or parentheses.
- NO AI markers ("במאמר זה", "חשוב לציין", "לסיכום", "בעולם של היום", "צוללים פנימה").
- NO internal SEO language in visible text (never "מילת מפתח", "pillar").
- NO hype/superlatives. Numbers always cite a source (תקן / חוק / רשות).
- Correct Hebrew RTL (numbers, units, parentheses).

PER-TERM LOOP (do this for each term in the WAVE-1 list in master-plan §WAVE 1):
1. VERIFY WIKIPEDIA VOID: search "<term> site:he.wikipedia.org". If a comprehensive
   Hebrew Wikipedia article already exists → SKIP the term, log "HE-WIKI EXISTS,
   skipped" (we will not compete with Wikipedia). If absent/thin → proceed.
2. CREATE the nadlan_term record via WP REST (POST /wp-json/wp/v2/nadlan_term with
   title = the Hebrew term, status=draft). Note the post_id.
3. GENERATE the body with ChatGPT using this exact sub-prompt:
   ---
   כתוב ערך מילון נדל"ן מקורי בעברית (סגנון ויקיפדיה, עובדתי וניטרלי) למונח: "<TERM>".
   מבנה: (1) פסקת הגדרה: מה זה ובאיזה הקשר נדל"ני. (2) פסקת עומק: איך זה עובד / סוגים /
   נתון מספרי אם רלוונטי. (3) בלוק "מה זה אומר בפועל עבורכם": הסבר יישומי לקונה/מוכר/
   משקיע. אורך 150-280 מילים. ייחודי 100%, נסח מחדש. ללא מקפים ארוכים, ללא סמני AI,
   ללא הייפ. סיים בלי שורת מקור (המערכת מוסיפה). פלט: HTML פסקאות בלבד.
   ---
4. PUSH via POST /wp-json/nadlan/v1/import-enrich with body:
   { "post_id": <id>, "content": "<html>", "data_quality": "enriched",
     "meta": { "term_en": "<English equivalent>",
               "wikipedia_en": "<EN Wikipedia URL>",
               "related_pillar": "<money-pillar URL this term links UP to>",
               "related_anchor": "<natural Hebrew anchor text>",
               "source_url": "<gov/standard/authority URL>",
               "source_label": "<e.g. תקן ישראלי 940 / חוק המקרקעין>" } }
   related_pillar mapping: construction/architecture terms → the buyer/'מקבלן' guide;
   law terms → /real-estate-lawyer/; finance terms → the mortgage pillar; appraisal
   terms → the 'שווי דירה' page; deal-type terms → the investment pillar.
5. PUBLISH the term (status=publish). The plugin pings IndexNow automatically.
6. QUALITY GATE before publish (rulebook §12): single H1, original copy, no dashes/
   AI-markers, source cited, the upward link present. If it fails, regenerate.
7. NEAR-DUPLICATE CHECK: keep a running list of your generated intros; if two terms
   come out >70% similar, regenerate the second with more entity-specific framing.

BATCH SIZE: 60 terms this run (the WAVE-1 list). Keep a progress log (last term done)
in a Drive doc or repo note so the next run resumes cleanly. After WAVE-1, the full
~200-term whitelist is in skills/content-encyclopedia-glossary-plan.md §3.

§STOP — stop and report to the owner if:
- WP REST auth fails (need an Application Password).
- /nadlan/v1/import-enrich returns 400/401 (confirm plugin v1.18.0 is active:
  GET /wp-json/nadlan/v1/healthcheck should show "version":"1.18.0").
- You finish the 60-term batch (report: how many published, how many skipped as
  HE-WIKI-EXISTS, 3 sample URLs, confirm they are indexable = no noindex meta).

DELIVERABLE: a short report — published count, skipped count, 3 sample /glossary/
URLs, and the progress cursor.
```

---

## Notes
- **Pictures/media** (owner raised): we have no images; plan is to generate via Gemini / NanoBanana / ChatGPT image gen and have Cowork attach them at the Pro+ tier. This is a separate mission (not in the glossary batch — glossary uses diagrams/own assets only, no stock-scrape). Homepage redesign → likely Lovable, deferred.
- **GA4**: resolved in code (v1.18.0 default OFF) — no wp-config edit needed from owner.
- **Polish/color**: mockup approved as "ok for now"; polishing deferred until the site is built out.
