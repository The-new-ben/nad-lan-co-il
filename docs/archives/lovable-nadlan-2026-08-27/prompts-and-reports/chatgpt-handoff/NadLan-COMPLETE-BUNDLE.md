# NadLan — COMPLETE STRATEGY BUNDLE (everything in one file)
**Assembled 2026-06-22.** One file holds it all: the master prompt to run next (Part 1), the prompts we already ran in Lovable (Part 2), the full outputs they produced (Part 3), the gap analysis (Part 4), and where we go from here incl. what to prompt Lovable (Part 5).

> **How to use:** Copy **Part 1** (between the `■■■` markers) into a strong reasoning model *or* into Lovable's Plan mode to generate the gap-filling build spec + new prompt series. Keep Parts 2–5 as the supporting bundle / attachments. Visual assets that live in the repo are listed in Part 5.

---
---

# PART 1 — THE MASTER PROMPT (run this next)

■■■ COPY FROM HERE ■■■

## ROLE
You are a **principal proptech product architect + technical-SEO/SERP strategist + growth-automation engineer**, with shipped experience building Zillow/Compass/Redfin/Homes.com-class portals, Mapbox/3D real-estate experiences, programmatic SEO at 100k-URL scale, and fully-automated growth systems. You advise the **owner** of **NadLan (נדל"ן)**, an Israeli real-estate portal aiming to dominate Israeli real estate and then expand internationally.

Produce a **complete, execution-ready, end-to-end specification** that an autonomous AI agent (or fleet of agents) can run **indefinitely until the product is built and operating** — covering keywords/SERP, content/articles, projects, design + visual generation, 3D/maps, the application + tech stack, marketing/EEAT, monetization, international expansion, and operations. Where the plan is already covered by the attached reports, **extend and fill the gaps**; do not repeat them.

**Be brutally honest. Do not flatter the owner.** If something is not feasible on the current stack (WordPress), if it needs an external system (CRM, headless app, capture vendor), if "3D for every apartment" is unrealistic short-term, or if a budget/credit reality bites — **say so plainly and give the real alternative.** The owner has asked explicitly for truth over reassurance.

## CONTEXT — NadLan today
- **Live:** nad-lan.co.il — **WordPress**, self-built FSE block theme. ~962 new-project CPT records, content pillars/spokes (Sde Dov, Ramat Aviv, Bat Yam, Herzliya…), Hebrew glossary, developer/contractor profiles. Hebrew-first, RTL. **The content/SEO layer ranks — do not break it.**
- **Vision:** the **Zillow/Homes.com/Compass of Israel** — map-first search, **real 3D project showrooms** (3D city map → click building → details → view → interiors), **all property types** (new projects now; rent + second-hand later), a marketplace of professionals/contractors/suppliers, then **international** (Cyprus, Dubai, Greece, Thailand for Israeli + global investors). **Zero-friction & autonomous:** every user (buyer, seller, agent, developer, pro) self-serves end-to-end; support is an AI agent; lead-routing/monetization/ops run automatically. The owner does not want to manually talk to customers.
- **Near-term money = NEW PROJECTS.** Israeli developers/contractors are spending heavily to advertise projects in a hard market; selling them qualified buyers — including international investors who tour the 3D and buy — is the immediate revenue. The homepage must foreground this while still competing across every category.
- **Prior work:** a 7-part Plan-Mode strategy series was run in Lovable. Reports 4–7 are captured in full (in this bundle, Part 3); Reports 0–3 (foundation / on-page SEO / keyword universe / competitor+SERP) are summarized (Part 2) — treat their subject as known, exact data as TO-BE-PRODUCED.

## HONEST CONSTRAINTS TO RESOLVE (confirm / refute / refine each — with specifics)
1. **WordPress = content layer, not app layer.** Keep WP for the ranking content/EEAT surface (962 projects, articles, glossary, schema). The map/3D/auth/dashboard/lead-engine/multilingual portal is a **web application**. Likely end-state = **two integrated systems** sharing one design system + canonical/URL strategy. Decide: classic-WP + bolted-on app, vs **headless WP** feeding a Next/React app. Give the concrete architecture + data flow + how the 962 existing URLs are preserved (301 map).
2. **Avoid Lovable lock-in.** Lovable writes real React/Vite and can sync to **your own GitHub** → you are not locked in **only if** you (i) connect it to your repo, (ii) own the backend/DB (self-hosted Postgres/Supabase or your CRM/API as system-of-record), (iii) deploy to your own host (Vercel/Netlify/server). Lovable **cannot crawl the live site** — feed it screenshots, exported components, the design tokens, and the repo. Specify the exact lock-in-proof workflow.
3. **Universal interior 3D is NOT feasible day one — tier it.** New projects → developer-supplied models. Second-hand/rental → cannot all have real interiors without capture (Matterport ≈ cost/unit) or agent upload. Realistic tiers: **T1** Mapbox GL 3D city/buildings everywhere (click building → details) · **T2** project exterior model + view simulation · **T3** real interior walkthrough only where captured/uploaded · **T4** basic fallback (photos + floor plan + street view + view-from-floor render). Confirm tiers, ingest pipeline, per-tier cost, and exactly what "see the view / go inside" means at each.
4. **A CRM / lead engine is required** (capture → dedup → route → SLA → bill → dashboards). WordPress is not a CRM. Build vs integrate (HubSpot / Pipedrive / Twenty / self-host) — recommend with cost.
5. **"Fully autonomous" has legal edges in Israel.** Agent-only: content, publishing, SEO, social, GBP, image-gen, support triage, lead routing. Human-in-the-loop (legally/practically): **broker-license** verification (חוק המתווכים), **legal/consent** copy, payment/KYC, takedowns, "official 3D" provenance approval. State the split.
6. **Cost & credits honesty.** Lovable free build credit ≈ 1/day; a real build needs a paid plan **or** — cleaner — export and let an autonomous coding agent build on your own repo. Estimate $/credits/time per path.

## DELIVERABLES — produce ALL, in order, execution-ready
**1) Ruthless gap audit.** Re-derive every gap from the attached reports + this brief. Rank by impact on (a) near-term project revenue, (b) SEO equity, (c) build risk. Flag anything in the reports that is wrong, inconsistent, or not buildable.

**2) New prompt series (the main output).** A numbered series of **Plan-Mode prompts** (each self-contained, ending "READY FOR NEXT PROMPT") that fills the gaps and then **builds** — e.g. keyword-data extraction, JSON-LD pack, WordPress→new-grammar migration/redirect map, editorial calendar, EN/i18n spec, then the build prompts (component gallery, calculators, 3D shell, page templates). For each: goal, exact expected output, acceptance test, and whether it is Plan or Build.

**3) KEYWORD + SERP MASTER SPEC (the owner's #1 priority — uncompromising).** Define and BEGIN to fill the master keyword table covering **every category** (resale, rent, new projects, urban renewal, professionals, contractors, suppliers, commercial, land, investment, foreign-investor) **× every priority city × every intent**, competing with **every** competitor (yad2, madlan, yad1, OnMap, WinWin, law-firms, banks, kolzchut, developer microsites). Columns (minimum):
`keyword (HE/EN) · category · geo · search intent (informational/commercial/transactional/navigational) · SERP type · SERP features present (featured snippet / PAA / local pack / map pack / image pack / VIDEO pack / shopping / sitelinks / knowledge panel) · dominant media (text/image/video/3D) · est. volume · KD · CPC · current top-3 SERP owners · winnable? (Y/N + why) · target page (per Report-4 URL grammar) · cannibalization-safe SoT? · content type to win (tool/article/listing/profile/3D) · priority P0–P3`.
Specify the method (SEMrush/Ahrefs + live SERP scrape), which **head money-terms surface on the homepage**, and the explicit **near-term new-projects money cluster**. Go for the hard, high-value terms — not just easy long-tail.

**4) ARTICLE PLAN — 25+ long articles to write NOW.** For each: working title, primary + secondary keywords, search intent, SERP type + features/media (is it a video SERP? image SERP? PAA-heavy?), target/parent money page, internal-link targets (cannibalization-safe), recommended length, full H2 outline, EEAT/author requirement, and why it wins its SERP. Sequence them; tie each to a money page; bias toward the new-projects revenue cluster.

**5) 3D / MAP TECHNICAL ARCHITECTURE (honest, tiered).** Resolve constraint #3 into a concrete build: Mapbox GL (3D buildings/terrain, clustered price pins, neighborhood boundaries, "click building → details"), the model viewer (model-viewer vs three.js/R3F), Matterport/interior path, **view-from-the-apartment** simulation, asset pipeline (formats, compression, CDN, manifest), and the **per-tier coverage plan for ALL property types**. State costs, data sources, and what is NOT feasible + the substitute.

**6) AUTONOMOUS-AGENT EXECUTION PLAN.** The end-to-end task graph an agent/fleet runs until the product is done and operating: repo + infra; design-system build; page templates; content generation + WordPress publishing; SEO monitoring + iteration; **Chrome-profile + social-account creation, Google Business Profile, EEAT/citations, favicons, OG images, AI image generation ("how it should look", reference-screenshot-driven — never guessed)**; ad-campaign drafting; lead-engine + support agent; QA gates **with screenshots** (build → screenshot → verify, not build-then-guess). Per task: tool, trigger, input, output, human-in-the-loop?, acceptance test.

**7) TECH-STACK DECISION & INTEGRATION MAP.** Resolve #1/#2/#4: WP-headless vs classic-WP-plus-app; the app stack; the lock-in-proof backend/system-of-record; CRM/lead-engine choice; auth/roles; how WP content + app share tokens, URLs, canonicals, data; deploy targets; the **Lovable → own-GitHub → own-host** workflow. One recommended architecture (described as a diagram) + a cheaper fallback.

**8) VISUAL / DESIGN GENERATION SPEC (no guessing).** For **every element, page, listing, project, professional card, and the homepage**: how it should look, with concrete **image-generation prompts** to produce reference mockups, and the **screenshot-reference workflow** (generate visual → build → screenshot → compare → iterate). Include favicon, logo lockups, OG/Twitter card templates, icon set, empty/loading/error visuals — all from the Report-5 tokens. The owner wants to SEE it before/while building, not after.

**9) INTERNATIONAL + i18n PLAN.** Expansion to Cyprus, Dubai, Greece, Thailand (and the global Israeli-investor diaspora): per-market demand + legal/ownership notes, the URL/hreflang architecture, the language set (HE/EN/RU/FR/AR + per-market), how international buyers discover and **tour the 3D and transact**, and why this is valuable enough that Israeli developers pay to list. Sequence after the IL core.

**10) MONETIZATION-OPS & ZERO-FRICTION SELF-SERVE.** How each actor self-onboards and transacts with **no human**: developer self-lists + uploads 3D + buys leads; pro self-verifies (within legal limits) + subscribes; buyer tours + books; the AI **support agent**; billing/subscriptions; sponsored-placement self-serve. Name the tools/stack.

**11) RISKS, BOUNDARIES, COST & TIME.** The brutal-honesty section: what will break, what is legally gated in Israel, realistic 3D coverage by phase, build cost/credits/time per path (Lovable-paid vs export-to-coding-agent), and the single biggest reason this could fail. End with a recommended **90-day sequence** and the **first 5 actions**.

## OUTPUT FORMAT
Markdown. Lead with a 1-page **executive answer** (recommended architecture + 3 highest-leverage moves + the honest "here's what's actually hard"). Then deliverables 1–11 as labeled sections. Tables for #3 and #4. Mark any number `NEEDS_VERIFICATION` unless grounded. **Do not soften the boundaries to please the owner.**

■■■ COPY TO HERE ■■■

---
---

# PART 2 — THE PROMPTS WE ALREADY RAN IN LOVABLE (Plan Mode)

**Original master frame (summary of the owner's Project Knowledge):** "War room to build the infrastructure to dominate ALL Israeli real estate long-term. Don't cede any category (listings, for-sale/for-rent, new projects, urban renewal, professionals incl. contractors/architects/engineers/inspectors/appraisers, materials/suppliers, commercial, plots). Map everything with any association to real estate. Go for the hardest, most-competitive, most-profitable money keywords (דירות למכירה, נדל"ן, יד2, פרויקטים חדשים, תמ"א 38…), not just easy long-tail. Premium international design (Zillow/Compass/Redfin-inspired, NOT gold/beige), mobile-first, perfect RTL. Real design tokens, not pictures. For every page: which keywords, which is the hub, which are spokes, cannibalization control, articles to write now."

**Prompt 0–1 (summary):** war-room framing; full on-page + technical SEO blueprint (titles, H-structure, meta, schema, internal-linking law, Core Web Vitals, EEAT).
**Prompt 2 (summary):** the **keyword universe** — every money keyword across all categories/cities, clustered, with KD/volume (SEMrush) + hub/spoke assignment. *(Real numbers still to be produced.)*
**Prompt 3 (summary):** competitor + **SERP reverse-engineering** (yad2, madlan, yad1, OnMap, law-firms, banks, kolzchut) — who owns what, SERP features, content gaps.

**Prompt 4 (reconstructed):** "Plan Mode only. Produce full Site Architecture + cannibalization map: URL grammar, per-page 18-field contract (URL/parent/breadcrumb/type/primary+secondary keyword/intent/title/H1/meta/modules/schema/index-noindex/canonical/internal-links/monetization/priority/competitor), programmatic rules, index/noindex + faceted-nav rules, cannibalization source-of-truth table. End READY FOR NEXT PROMPT."

**Prompt 5 (verbatim):**
> אנחנו לא בורחים לביטויי זנב קלים. לא מוותרים על אף קטגוריה. Plan Mode בלבד — אל תבנה, אל תשנה קוד, אל תעשה deploy. הפק עכשיו דוח UX/UI ומערכת עיצוב מלאה בלבד. המטרה: NadLan כפורטל נדל"ן פרימיום בינלאומי, לא תבנית וורדפרס ולא אתר מיושן. Premium = דאטה, מפה, מרווחים, טיפוגרפיה, היררכיה, מהירות, אמון, clean product, microinteractions, mobile-first, RTL מושלם. לא זהב/בז'. Benchmark: Zillow, Homes.com, Redfin, Realtor, Compass, StreetEasy, Matterport, מדלן, יד2, יד1, OnMap. תן: Design principles, brand feeling, color palette (ערכי hex מדויקים), typography tokens, spacing scale, radius, shadows, cards, buttons, badges, forms, tables, search module, map/list layout, listing card, project card, professional card, homepage, project showroom, listing detail page, city page, professional page, join-pro page, developer dashboard, mobile design, RTL rules, accessibility, error/empty/loading states, QA checklist. כתוב כאילו אתה מוסר למתכנת מתחיל. אל תקצר. בסוף READY FOR NEXT PROMPT.

**Prompt 6 (verbatim):**
> Plan Mode בלבד — אל תבנה. הפק מפרט מלא של "חדר תצוגה תלת-ממד לפרויקט" (3D Project Showroom). זה החפיר הייחודי: מודל תלת-ממד אינטראקטיבי אמיתי לכל פרויקט — לא תמונה יפה. בנצ'מרק: Matterport, Sketchfab, Zillow 3D Home, Compass. תן: State machine official/concept/missing; נתוני המודל (glTF, GLB, USDZ, Draco, LOD, lazy-load, CDN); Viewer (model-viewer מול three.js, בקרות, hotspots, יום/לילה, מסך מלא, AR); Provenance (מקור לכל אסט, אסמכתאות, סימון רעיוני מול רשמי); מודולים בעמוד; ביצועים + fallback + נגישות; RTL ונייד; SEO/Schema (Residence/Place/3DModel, sameAs); אינטגרציית Sketchfab דו-כיוונית; QA ודגלים. אל תקצר. בסוף READY FOR NEXT PROMPT.

**Prompt 7 (verbatim):**
> Plan Mode בלבד — אל תבנה. הפק דוח מודל הכנסות ו-Outreach (GTM) מלא. מונטיזציה לכל הקטגוריות. תן: זרמי הכנסה (לידים, B2B developer dashboard + רישוי דאטה + כלים לסוכנויות, קידום ממומן מסומן, freemium לפרופילי מקצוע, אירוח 3D); תמחור ושכבות; משפך לכידה→ניתוב→המרה→שימור; GTM (גיוס 100 מקצוענים/20 יזמים/5 סוכנויות, תסריט קר, רצף מיילים, שותפויות רמ"י/עיריות/דאטה ציבורית, PR); KPI ויחידת כלכלה (CAC/LTV/churn); ציות ישראלי (לשכת עוה"ד, חוק המתווכים, הגנת הצרכן, הגנת הפרטיות, תיקון 40); רצף השקה מסונכרן לתור הבנייה; סיכונים. בסוף READY FOR NEXT PROMPT.

---
---

# PART 3 — THE FULL OUTPUTS (the exact reports Lovable produced)

*Reports 4–7 are reproduced in full below. The same text also lives as individual files in `strategy/lovable-reports/` for attaching separately. Reports 0–3 are pending capture.*

## ════ REPORT 4 — Full Site Architecture + Cannibalization Map ════
Plan-only. Every numeric/ranking claim = `נדרש אימות ב-Semrush / GSC`. URL grammar uses `{}` for variables; final slugs decided at implementation (HE-transliterated, lowercase, hyphenated; project IDs stable for canonical safety).

### A. Top-level URL grammar (the contract)
```
/                                       home
/buy/                                   sale hub
/buy/{city}/                            city sale hub
/buy/{city}/{neighborhood}/             neighborhood sale hub
/buy/{city}/{neighborhood}/{listing-id} listing leaf
/rent/  ...                             rent hub (mirror of /buy)
/projects/                              new-projects hub
/projects/{city}/                       city projects hub
/projects/{project-slug}-{id}/          project page (showroom state-machine)
/developers/{developer-slug}/           developer profile
/renewal/  /renewal/tama-38/  /renewal/pinui-binui/  /renewal/{city}/   urban renewal pillar+spokes
/cities/{city}/  /cities/{city}/{neighborhood}/  /cities/{city}/prices/   city intelligence (Dataset)
/tools/{mortgage-calculator|purchase-tax-calculator|appreciation-tax-calculator|yield-calculator|affordability|estimator}/
/pros/{role}/  /pros/{role}/{city}/  /pros/{role}/{city}/{slug}-{id}/   professionals (lawyer/mortgage-advisor/appraiser/inspector/agent/architect/engineer/contractor/supervisor)
/contractors/{specialty}/{city}/        contractor vertical
/suppliers/{category}/{city}/           suppliers (מטבחים/אריחים/אלומיניום/מיזוג)
/commercial/{offices|retail|warehouses}/{city}/   CRE
/land/{city}/                           land/plots
/invest/  /invest/yield-map/  /invest/foreign-buyers/   investment + EN bridge
/guides/{slug}/  /glossary/{term}/  /aeo/{question-slug}/   editorial / glossary / AEO
/b2b/{developers|agencies|professionals|data}/   B2B
/en/...                                 English mirror tree (hreflang)
/about/ /trust/ /methodology/ /legal/ /contact/ /sitemap/   institutional (EEAT spine)
```
**Rules:** trailing slash on hubs, none on leaves with `-{id}`; canonical=self for every indexable page; primary facets (city/neighborhood/role) in **path**, secondary (rooms/price/sort) in **query** + always `noindex,follow` except whitelist.

### B. Per-page 18-field contract (every page)
URL · parent · breadcrumb · type · primary kw · secondary kw · intent · title · H1 · meta · content modules · data modules · UX modules · schema · index/noindex · canonical · internal links in/out · monetization · priority P0–P3 · competitor to beat. Programmatic children inherit unless overridden.

**Archetype priorities & schema (sample):** `/` home → kw נדל"ן, WebSite+Organization+SearchAction, P0, vs yad2/madlan · `/buy/` → דירות למכירה, CollectionPage+ItemList, P0 · `/rent/` → דירות להשכרה (+scam module), P0 · `/projects/` → פרויקטים חדשים (verified-only default), P0 · `/renewal/` → התחדשות עירונית (attorney reviewer), P0 · `/buy/{city}/` → דירות למכירה {city}, CollectionPage+ItemList+Place+Breadcrumb+FAQ, index only if supply ≥ threshold, P0 top-5 · `/projects/{slug}-{id}/` → פרויקט {brand}, Residence+Place+Organization+Event+FAQ, index only if status≠missing, canonical stable on {id}, P0 · `/tools/mortgage-calculator/` → מחשבון משכנתא, WebApplication+HowTo+FAQ, P0 · `/tools/estimator/` → כמה שווה הדירה שלי (+methodology+confidence range), P0 · `/pros/{role}/{city}/` → {role} {city}, LocalBusiness ItemList, index only if ≥N verified pros · `/invest/foreign-buyers/` → buying property in israel, P0 intl (LEGAL_REVIEW).

### C. Internal-linking graph
Hub→sub-hub→leaf spine; every leaf links up + to 2–5 siblings; **vertical cross-links required** (city sale ↔ rent ↔ projects ↔ renewal ↔ cities; project ↔ developer ↔ neighborhood; tool ↔ pillar guide; pro role×city ↔ local listings); editorial→money pages (never reverse as primary anchor); footer hub block ≤40 links; real breadcrumb below depth 1; **zero orphan pages** (build-time check).

### D. Index/noindex + faceted nav
Index when real content+data+threshold+canonical=self+no thin dup. Noindex,follow for: facets beyond whitelist, thin/empty hubs, sold/rented archives, concept-only projects, internal search, query-facets outside whitelist. Whitelist (index): city, neighborhood, rooms-bucket only when supply justifies. Strip utm_*/fbclid/gclid from canonical. Expired/sold → 301 to parent + archive `/sold/{id}` noindex,follow. Project status presale→under_construction→occupancy all index if official; missing=noindex honest empty-state; cancelled=410. City/neighborhood templates must differ ≥X% unique or doorway risk → noindex.

### E. CANNIBALIZATION MAP (source-of-truth — non-negotiable)
| Intent cluster | Money keyword | **SoT page** | Common cannibals | Rule |
|---|---|---|---|---|
| Sale, city | דירות למכירה {city} | `/buy/{city}/` | /cities/{city}/, /projects/{city}/, guides | SoT=commercial; /cities/=מחירי/שכונות; projects=פרויקטים חדשים; guides=long-tail only |
| Sale, neighborhood | דירות למכירה {n} {city} | `/buy/{city}/{n}/` | /cities/.../{n}/, /projects/.../{n}/ | commercial vs intelligence vs new-build |
| Rent, city | דירות להשכרה {city} | `/rent/{city}/` | scam/lease guides | guides link up |
| New projects, city | פרויקטים חדשים {city} | `/projects/{city}/` | /buy/{city}/, developer pages | dev pages=brand only; sale hub never targets this |
| Project brand | פרויקט {brand} | `/projects/{slug}-{id}/` | dev page, projects hub, blog | only project page targets brand |
| Renewal head | תמא 38 / פינוי בינוי | `/renewal/tama-38/`, `/pinui-binui/` | city overlays, projects, guides | head=pillars; overlays={term} {city}; guides=sub-Qs |
| City intelligence | מחירי דירות {city} | `/cities/{city}/` | /buy/{city}/, blog | quarterly report=/guides/market-report-{city}-{Q}/ |
| Calculator | מחשבון משכנתא… | `/tools/{tool}/` | guides | guides="איך מחשבים…"+link; never "מחשבון" in title |
| Valuation | כמה שווה הדירה שלי | `/tools/estimator/` | sold archive, neighborhood | archive=noindex; neighborhood=מחירי not שווי |
| Pro role+city | {role} {city} | `/pros/{role}/{city}/` | profiles, role hub, sale hub | hub=head; role×city=local; profile={name} |
| Investment | השקעה בנדל"ן | `/invest/` + `/invest/yield-map/` | guides | guides=sub-Qs |
| EN intl | buying property in israel | `/en/...` + `/invest/foreign-buyers/` | HE pages | hreflang pairs; EN never on HE URL |
| AEO | natural-language Q | `/aeo/{q}/` | guides, glossary, hub FAQ | AEO leaf owns money-Q, links to pillar |
| Glossary | {term} מה זה | `/glossary/{term}/` | guides | glossary=definitional; guides=explanatory |

**Canonical rules:** every indexable page self-canonical; sort/pagination identical → canonical→base; filtered noindex,follow → self-canonical (not cross-canonical); HE↔EN hreflang each self-canonical. **#1 risk:** `/cities/{city}/` and `/buy/{city}/` both targeting "דירות למכירה {city}" = auto-split. The SoT table is law.

### F. Programmatic guardrails
No page ships without real data · unique-content gate ≥40% unique tokens vs siblings · weekly quality monitor auto-noindexes sub-threshold hubs · sitemap split (pages/cities/neighborhoods/projects/pros/guides/en ≤50k each) · monthly crawl diff + cannibalization re-check on new templates.

### G. Priority queue
**P0:** /, /buy/, /rent/, /projects/, /renewal/+tama-38/pinui-binui, /tools/{mortgage,purchase-tax,appreciation-tax,estimator}, /cities/{top-5}, /projects/{top-5}, project pages w/ official assets only, /invest/foreign-buyers/+/en/ stub, /trust/ /methodology/ /legal/. **P1:** /cities/{city}/{n}/, /pros/{lawyer,mortgage-advisor}/{top-5}, /renewal/{top-5}, remaining tools, /guides/ seed, /invest/, /b2b/*. **P2:** remaining pro roles+cities, /contractors/, /suppliers/, /commercial/ scoped, /land/, /glossary/, /aeo/ scale. **P3:** full CRE, full EN tree, full glossary, investor dashboard.

### H. Flags
NEEDS_VERIFICATION (every KD/volume/position) · LEGAL_REVIEW (renewal/tax/mortgage/legal/lease/reviews) · REQUIRES_OFFICIAL_ASSET (every project/developer/pro) · OFFICIAL_SOURCE_REQUIRED (every price/yield/tax-bracket/planning/transaction). Strategic risk: programmatic hubs without thresholds = doorway/thin penalty delaying the whole money-keyword attack.

## ════ REPORT 5 — UX/UI + Design System ════
RTL-first, mobile-first, premium intelligence portal. Brand feeling: **"Bloomberg Terminal for Israeli real estate, with a Compass-grade product surface."** Adjectives: precise, calm, fast, civic, modern. Forbidden: luxurious/warm/cozy/playful.

### Principles (non-negotiable)
Data over decoration (no module without data) · Trust is the brand (source line on every claim, status badge on every project, verification badge on every pro) · Map is first-class · RTL is default not translation · Mobile-first thumb-first (44×44 targets) · Hierarchy by weight+space not color (one accent ≤10% of screen) · Micro-interactions functional only · Performance is design (LCP ≤2.0s, no CLS) · Empty/loading/error designed with every component. **Forbidden:** gold/beige/cream, stock "family with keys", purple SaaS gradients, neon glows, glassmorphism on data, Lottie on KPIs, emoji icons, fake "trusted by" logos.

### Color tokens (exact hex)
Neutrals: `--ink-900 #0B0F14` · `800 #111722` · `700 #1B2330` · `600 #2A3342` · `500 #4B5566` · `400 #7A8497` · `300 #B4BCC9` · `200 #D7DCE3` (borders) · `100 #EBEEF2` (dividers) · `50 #F5F7FA` (bg) · white #FFFFFF.
Brand (single): `--brand-700 #0E4FB3` (pressed) · `600 #1561D8` (primary/links) · `500 #2E7BF0` (hover) · `100 #E2ECFB` (fills). ≤10% of surface, never body text.
Data-viz (colorblind-safe): sequential `#0B3B82 #1561D8 #5B9BF2 #A8C7F7 #E2ECFB`; diverging below/at/above `#0E7C66 #E8E8E8 #B5311B`.
Semantic: success `#0E7C66`/`#DCEFE9` · warning `#B57700`/`#FBEDCC` · danger `#B5311B`/`#F6DAD3` · info `#1561D8`/`#E2ECFB`.
Dark: bg `#0B0F14`, surface `#111722`/`#1B2330`, text `#EBEEF2`/`#B4BCC9`, border `#2A3342`, brand boosted `#2E7BF0`. Body ≥4.5:1, controls ≥3:1.

### Typography
Hebrew **Heebo** 400/500/600/700; English **Inter**; tabular numerals **IBM Plex Mono** (price/area/yield/IDs/dates). Forbidden: Assistant, Rubik, Open Sans Hebrew; weight 300. Scale (px/lh): xs 12/16 · sm 14/20 · base 16/24 · md 18/28 · lg 20/28 (card title) · xl 24/32 (section) · 2xl 30/36 (page H1) · 3xl 36/44 (hero) · 4xl 48/56 (landing). One H1/page, no skipped levels, `tabular-nums` in data.

### Spacing/Radius/Shadow
Spacing 4px grid: 0·2·4·6·8·12·16·20·24·32·40·48·64·80·96·128. Card padding 16/20/24; section rhythm 48/64/96. Radius xs4 chips · sm6 inputs · md10 cards · lg14 hero/map · pill999 badges (no 24px+ blobs). Shadows: elev-1 `0 1px 2px rgba(11,15,20,.06)` cards · elev-2 `0 4px 12px rgba(11,15,20,.08)` hover · elev-3 `0 12px 32px rgba(11,15,20,.12)` modal · focus ring `0 0 0 3px rgba(46,123,240,.35)`. No colored glows.

### Components
**Buttons** sm32/md40/lg48: Primary brand-600 (hover 500, pressed 700, disabled ink-200/400), Secondary white+ink-200, Ghost transparent, Danger (destructive only), Link. States default/hover/active/focus/disabled/loading. Icon-only needs aria-label, 44×44 mobile. No gradients/all-caps/emoji.
**Badges** 24h pill: verified success+check · concept warning + "נכס לא רשמי" · missing danger + "אין מקור רשמי" · sold/rented ink + strikethrough price.
**Forms** input 44h/40h, label above (sm/500, 6px gap), required `*` danger, helper xs/ink-500, error danger+icon, validate on blur, RTL label/helper/error on start. No floating labels, no placeholder-as-label.
**Tables** row 48/40, header ink-600 xs/500 sticky, numeric columns start-aligned in RTL + tabular-nums, sortable chevron, hover ink-50, selected brand-100, empty=illustration+CTA.
**Search module (hero):** underline mode-tabs (מכירה·השכרה·פרויקטים חדשים·התחדשות·מסחרי·מגרשים·אנשי מקצוע) · location combobox typeahead (cities/neighborhoods/streets/projects, entity-typed) · facets (rooms chips, price slider from/to, type) → mobile bottom sheet · CTA חיפוש + ghost פתח מפה · below: result count + "עודכן לפני 12 דק'". No featured-cities carousel, no wizard, no "talk to rep".
**Map+list:** desktop 60/40 (list start, map end), sticky map, card↔pin highlight; tablet 50/50; mobile list-first + "מפה" pill → full-screen + bottom drawer carousel. Pins = price label in a pill (₪2.4M), not generic icon.
**Listing card:** 4:3 image (reserved, no CLS), status badge, save heart, price lg/700 tabular, ₪/sqm, rooms·sqm·floor, 2-line address, agent badge + "עודכן לפני Xד׳". Sold=strikethrough+grayscale. No 5-stars, no fake "trending", no auto-carousel.
**Project card:** 16:10, state-machine badge (Official ✓ / Concept ⚠ / No source ✕), developer logo chip, name lg/600, status label+date, price range מ-₪X.XM, apartment-type chips, occupancy ETA, "אסמכתאות (N)".
**Professional card:** 56×56 avatar (rounded-md), name, role+license number, city, "מאומת" badge, specialty/language/response-time chips, "פנייה" + "צפייה בפרופיל". No fake stars → "אין ביקורות עדיין".

### Page layouts
**Homepage:** sticky 64h top bar (logo·nav·search·HE/EN·auth) → compact hero ~520h (H1 "נדל"ן בישראל — דאטה, מקצועיים, אמת." + search front-center, no stock photo) → market-pulse strip (4 CBS KPI tiles w/ source+timestamp) → 8 hub tiles (icon+label+1-liner+count) → verified-projects rail (8 cards) → tools strip (3 calculators w/ preview) → editorial latest (3 guides, named author) → institutional footer + hub block + mandatory methodology link. No autoplay video, no testimonial carousel, no animated KPI counters.
**Project showroom:** hero band (name+status+breadcrumb, sticky lead form/bottom CTA) · tabs (סקירה·דירות ומחירים·גלריה·תכניות·מיקום·קבלן·סטטוס תכנוני·אסמכתאות·שאלות) · state-machine band visible if ≠official · gallery w/ per-image provenance · apartments table (tabular-nums) · map+POIs (1km, official) · developer card (Organization+sameAs) · planning timeline (dated+sourced) · lead form (invisible CAPTCHA, consent LEGAL_REVIEW). No fake "starting from X₪".
**Listing detail:** hero gallery ≥16:9, price+₪/sqm, specs, address+map, sticky contact bar. Sections: תיאור·מפרט·מיקום ושכונה·מחירי שכנים·מחשבון משכנתא inline·נכסים דומים. States active/sold/rented/off-market.
**City page:** header band (H1+stats) · neighborhood map · price heat table (sortable, tabular-nums) · new projects (verified) · top pros (verified) · methodology box (mandatory) · FAQs. LEGAL_REVIEW + OFFICIAL_SOURCE on every number.
**Professional page:** avatar+name+role+license+verification+city, sticky contact card · sections על אודות·התמחויות·שפות·אזורי שירות·עסקאות·ביקורות מאומתות·שאלות·קשר. No fake reviews.
**Join-pro:** two-column (value prop / application form: name·role·license·city·phone·email·website·license PDF·consent), progress, success "נחזור תוך 48 שעות". No dark patterns.
**Developer dashboard (B2B):** left rail (סקירה·פרויקטים·לידים·נכסים דיגיטליים·אנליטיקה·חשבונית·הגדרות), KPI row (לידים השבוע·CTR·עלות לליד·פרויקטים פעילים), tables-heavy, inline drawers, per-seat permissions, visible audit log.

### Mobile · RTL · A11y · States
**Mobile:** breakpoints xs<360/sm360–767/md768–1023/lg1024–1439/xl≥1440; bottom tab bar (בית·חיפוש·שמורים·התראות·פרופיל) 56h; sticky bottom CTA; bottom sheets for filters (snap 25/50/90%); `h-dvh`; lazy-load below fold.
**RTL (binding):** `<html dir=rtl lang=he>`, EN tree ltr/en · **logical CSS only** (margin-inline-start/end, padding-inline, inset-inline) never margin-left/right · logical flex/grid order (no flex-row-reverse hack) · mirror directional icons via scaleX(-1) only (never logos/numerals) · Latin digits 1,234,567, ₪ before number · DD.MM.YYYY · `<bdi>` for mixed strings · tables header+numeric start-aligned · map controls on end side.
**A11y (WCAG 2.2 AA):** contrast per pair · focus ring everywhere · keyboard (tab order=visual, skip-to-main) · fields↔labels+aria-describedby errors · icon-only aria-label Hebrew · live regions · modals focus-trapped (Radix/shadcn) · map list-alternative · alt incl provenance · prefers-reduced-motion · 44×44.
**States:** loading=skeletons matching layout (no CLS); empty=icon+specific copy+CTA; error=retry; success=toast top-end 4s; disabled=opacity.5+tooltip-why.
**Motion:** micro120/default200/deliberate320ms, easing cubic-bezier(.2,0,0,1); not for KPI counters/parallax/scroll-reveals; respect reduced-motion.
**Imagery:** no stock family/villa/blobs/Lottie; project photos only with provenance; concept labeled; city pages use map+data-viz not photos; OG = auto data-card (title+price+city+badge).
**QA gate (every page):** type/spacing scale · one H1 · tokens only · dark parity · logical RTL · responsive 360/390/768/1024/1440 · a11y · states present · every number sourced · no fake reviews · LEGAL_REVIEW gated · LCP≤2.0s · CLS≈0 · schema per Report 4 · breadcrumbs+hreflang. **Strategic risk:** any component shipped without loading/empty/error/disabled = trust regression at first failure.

## ════ REPORT 6 — 3D Project Showroom (Engineering Spec) ════
The defensible moat: a real interactive 3D model per project, tied to a verified apartment table, hotspot-linked, AR-capable, **provenance-honest**. A verifiable spatial index, not a pretty render. Benchmarks: Matterport, Sketchfab, Zillow 3D Home, Compass.

### 1. State machine (server-computed, non-overridable in CMS)
- **OFFICIAL** — trigger: provenance.type ∈ {developer/rmi/municipality_official} + document_url + LEGAL_REVIEW=approved. Green badge "מודל רשמי · {source}" links to provenance doc. Allowed: hotspots→verified apartments, floor switcher, day/night, AR, fullscreen, share. Forbidden: any decorative element not in source file.
- **CONCEPT** — trigger: provenance.type=concept. Amber badge "הדמיה רעיונית — לא מחייבת" + persistent ~8% diagonal watermark + non-removable bottom banner. Allowed: rotate/zoom/generic floors. Forbidden: hotspots to specific apartments, AR, "official" iconography, price overlays.
- **MISSING** — no asset. No canvas; axonometric line-drawing placeholder (SVG), badge "אין מודל זמין", CTAs "בקש מהיזם מודל רשמי" (lead tagged request_3d) + "קבל עדכון". Forbidden: stock 3D, AI building, "coming soon" renders.
- Transitions: Concept→Official only by re-upload w/ valid provenance; Official→Missing only by takedown + audit log; all logged (actor+timestamp).

### 2. Model pipeline
Formats: web `.glb` (glTF 2.0, embedded textures); iOS AR `.usdz` sibling; Android Scene Viewer reads `.glb`; private archive keeps original DCC. Rejected: fbx/obj/dae. Budget (targets, NEEDS_VERIFICATION): triangles ≤250k exterior / ≤500k +ground / ≤1.2M full interior (LOD); texture ≤4096² PBR KTX2+Basis; Draco (or meshopt, one project-wide); size exterior ≤6MB, full ≤18MB, usdz ≤25MB, **hard ceiling 35MB→rejected**; LOD ≥3. Delivery: CDN immutable 1yr + content-hash; lazy-load via IntersectionObserver (rootMargin 200px), poster in initial HTML; Range support; decoders pinned + same-origin. Manifest per project drives viewer (provenance, files, camera presets, hotspots, floors, lighting, bounds, legal).

### 3. Viewer
Default `<model-viewer>` (glTF+USDZ+AR built-in, ~80KB gz, accessible). Escalate to three.js/R3F only for custom shader/cutaways/multi-camera (written justification). Controls: orbit/pan/zoom (clamped), reset, camera presets (חזית/כניסה/גג/חתך), floor switcher (isolates apartments in table), day/night (localStorage), fullscreen, share deep-link (cam/floor/hotspot). Hotspots = real `<button>`+aria-label, model-anchored; CONCEPT = floor-only. AR mobile-only, disabled in CONCEPT (iOS USDZ Quick Look / Android Scene Viewer).

### 4–5. Provenance + page modules
Provenance = body-copy line **under the viewer in all states** (never tooltip/hover); OFFICIAL_SOURCE_REQUIRED enforced at upload. Fixed module order (hide, never reorder, when data missing): hero → showroom → provenance → floor tour → **apartment table (sole source of truth for apartment data, not the 3D)** → map+POI → planning timeline → developer card → lead form → gallery (each image labeled צילום/הדמיה).

### 8. SEO/Schema (crawler sees no WebGL)
`<section>` + real `<h2>` "סיור תלת-ממד בפרויקט {name}"; poster alt incl name+"מודל תלת-ממד"; table/floors/provenance server-rendered. Schema: Residence/RealEstateListing per apartment, Place (geo/address), ImageObject (creditText=source), **3DModel** (encodingFormat "model/gltf-binary", contentUrl, license, isBasedOn→provenance doc). CONCEPT 3DModel carries disambiguatingDescription "הדמיה רעיונית", NOT image of Residence. sameAs→developer/RMI/municipality. Sitemap: URLs only (no .glb); robots blocks CDN paths.

### 9. Sketchfab (bidirectional, not source of truth)
Inbound: verified-owned model embedded via Sketchfab Viewer API in same slot (state+badge+provenance apply, iframe sandboxed). Outbound: every OFFICIAL model mirrored to NadLan org account w/ back-link to canonical page (backlinks/discovery). Forbidden: embedding third-party model as the developer's → auto-flag CONCEPT.

### 10. Hard bans (REQUIRES_OFFICIAL_ASSET)
Concept render without watermark+disclaimer · concept labeled "official/מהיזם" · AI buildings as project models · stock 3D reused · CONCEPT hotspots to specific apartments · price overlays on 3D canvas · provenance behind hover · loading model on initial page load (must be intent-gated) · indexing .glb · embedding third-party Sketchfab as developer's · replacing apartment table with 3D-only. Performance/fallback: LCP poster ≤2.0s, JS+decoder ≤180KB gz lazy, CLS=0 (reserved aspect 16:10 desktop/4:5 mobile), no-WebGL still renders table+floors+POIs, keyboard controls, non-3D alternative link.

## ════ REPORT 7 — Revenue Model & Go-To-Market ════
Numbers directional `NEEDS_VERIFICATION`; legal `LEGAL_REVIEW`. Primary revenue yr 1–2 = **leads (PPL)**.

### Revenue streams
**A. Leads (₪/lead, directional):** יזם 180–450 · מתווך 60–180 · עו"ד 250–600 · יועץ משכנתא 120–280 · שמאי 80–200 · קבלן 40–150 · ספק 60–220 · מסחרי 300–900 · מגרשים 400–1,200 · משקיע זר 600–1,500(USD). Consent button per הגנת הפרטיות + תיקון 40.
**B. B2B SaaS:** Developer Dashboard · Agency Workspace · Data Licensing API (institutional) · 3D Hosting.
**C. Promoted listings:** mandatory "ממומן" label (הגנת הצרכן); CPM/CPC/Featured Slot; no mixing into organic.
**D. Pro freemium:** Free / Pro ₪249–449 / Premium ₪899–1,490 / Enterprise.
**E. 3D hosting/production:** ₪199–699/mo; official-source production ₪8K–45K one-time. No charging concept-as-official.
**F. Tertiary (yr2+):** mortgage marketplace (rev-share), insurance, moving, renewal-organizer toolkit.

**Pricing tiers:** מתווך Free/₪349+PPL/₪1,490 · עו"ד Free/₪449+PPL/quote · יועץ Free/₪299+PPL/quote · קבלן Free(≤3 leads)/₪399/quote · יזם listing/₪2,500/project+leads/₪15k++API · סוכנות —/₪1,490(≤10 agents)/₪4,900+ · Data API —/—/₪8k–40k.

### Funnel
Capture (converting pages): listing→form+WhatsApp · showroom→"תאם ביקור"/"הורד מפרט" · city→"3 מתווכים מאומתים" · renewal→wizard · profile→"בקש הצעת מחיר" · calculator→"השווה 3 יועצים". Route: engine by city/category/price/urgency, round-robin within tier, Premium priority, SLA 5-min, auto-reassign, anti-fraud (dedup phone+OTP). Convert: lead→contact ≥70% in 1h. Retain: monthly ROI dashboard, churn warning, reactivation 50%.

### GTM (first 100 pros / 20 devs / 5 agencies)
Phase 0 (wk0–2): 3 pilot cities (TA/Haifa/Beer Sheva), manual seed 200 projects/500 listings/2,000 pro records (public registries), compliance review. Phase 1 (wk2–8): 100 pros — 1 SDR + Report-3 dashboards; cold call public numbers + LinkedIn + WhatsApp (opt-in); hook "פרופיל מאומת חינם + 5 לידים חינם"; 8–12% of 1,000. Cold script (<45s) + 5-touch email (intro / case study / "X פניות בעירך" / founder note / break-up). Phase 2 (wk4–12): 20 devs — top-down 80 from data.gov.il permits, 3 months free + 3D hosting, 3 anchor logos. Phase 3 (wk8–16): 5 agencies — free Workspace 6 months + preferred rotation. Partnerships: רמ"י land tenders, pilot municipalities, public data (gov.il/טאבו/Lamas/בנק ישראל), academia ("מדד NadLan" quarterly → PR). PR angles: first IL portal w/ real 3D per project; quarterly tower-data study; transparency-of-sources → Globes/Calcalist/TheMarker/Ynet.

### KPIs / unit economics
CAC/Pro <₪400, CAC/dev <₪6,000, payback Pro<3mo/dev<6mo · cost/organic-lead <₪25, paid<₪70 · lead→sold 60–75% · Pro churn <6%/mo, dev <20%/yr · LTV(Pro)≈₪4,375 · **LTV:CAC ≥4:1** · time-to-first-lead <7d · contact rate ≥70%/1h · showroom session ≥45s · organic lead share ≥60% by M12.

### Israeli compliance (LEGAL_REVIEW — all before launch)
לשכת עוה"ד (no promised results, no "מומחה" w/o certification) · חוק המתווכים (license# verified vs registry) · הגנת הצרכן ("ממומן" label, VAT prices, 14-day cancel) · הגנת הפרטיות + תיקון 40 (opt-in, explicit lead-transfer consent w/ party name) · שוויון הזדמנויות (no discriminatory filters) · נגישות WCAG 2.2 AA · גילוי נאות "תוכן בשיתוף" · GDPR for foreign base.

### Launch sequence (synced to build queue)
Q1: city pages/listings v1/pro directory/basic projects → free profiles + PPL pilot (no charge). Q2: 3D Showroom v1 (10 projects)/renewal hub/lead-routing → start PPL billing + Pro launch. Q3: Developer Dashboard/agency workspace/schema depth → dev subscriptions (3 anchors)+agency contracts. Q4: Data API/mortgage marketplace/foreign-investor EN → data licensing + rev-share + sponsored GA. **Golden rule:** no monetization for a category before 3 months of sufficient organic traffic on its pages. **Top risk:** if developers don't supply official 3D → showroom stays CONCEPT → sign 3 anchor data-partnerships + in-house 3D for top 50.

---
---

# PART 4 — GAP ANALYSIS (plan + prompts vs. what was delivered)

The four captured reports are **specification-complete and high quality** — but every one is words and tokens. **Nothing is rendered, built, or verified.** That is the headline gap.

**A. Spec gaps (asked, thin/absent):**
- **A1 Verified keyword DATA** — every number is `NEEDS_VERIFICATION`; the real prioritized keyword universe with volume/KD/SERP-features (what Lovable's SEMrush could give) is not yet produced. *Owner's #1 priority.*
- **A2 JSON-LD templates** — schema types named, not written.
- **A3 Migration / redirect map** — greenfield grammar vs the live WP site (962 projects, existing pillars); no current-URL→new-URL 301 plan → equity-loss risk.
- **A4 Editorial calendar** — page list exists; the sequenced "25+ articles to write now" with per-article keyword+intent+SERP+links does not.
- **A5 EN / foreign-investor tree** — named P0, but no actual EN page set / hreflang map / translated targets.

**B. Realization gaps (only a builder closes):**
- **B1 Zero rendered UI** — design system has exact tokens but no pixels. *Owner-flagged.*
- **B2 No working tools** — calculators specified, none built.
- **B3 No working 3D viewer** — spec only, no shell.
- **B4 No page templates** — homepage/listing/showroom/city/pro — none built.

**C. Capture gap:** Reports 0–3 full text not folded in (repo-equivalent exists for 2–3).

**New owner asks (this round):** universal property coverage (rent + second-hand) with "go inside / see the view / 3D city map / click building"; full autonomy (Chrome profiles, social, campaigns, GBP, EEAT, favicons, image-gen — "don't guess, show how it looks"); international (Cyprus/Dubai/Greece/Thailand) + languages; homepage foregrounding the new-projects money; competing on every keyword.

---
---

# PART 5 — WHERE WE GO FROM HERE

**Step 1 — run the master prompt (Part 1).** Paste it into a strong reasoning model (attach this bundle). It returns: the ruthless gap audit, a new Plan→Build prompt series, the keyword+SERP master table, the 25+ article plan, the 3D/Mapbox architecture, the autonomy plan, the tech-stack decision, the international/i18n plan, and the honest cost/credits/risk section.

**Step 2 — also ask Lovable to self-audit (paste in Plan mode):**
> Plan Mode בלבד — אל תבנה. סקור את כל 7 הדוחות שהפקת ותן: (1) מה חסר כדי לבנות את המוצר המלא מקצה לקצה — דאטת מילות מפתח אמיתית עם volume/KD/SERP features, תבניות JSON-LD, מפת מיגרציה מ-WordPress קיים (962 פרויקטים), לוח 25+ מאמרים, עץ EN, ארכיטקטורת 3D/Mapbox לכל סוגי הנכסים (חדש/השכרה/יד שנייה), CRM/מנוע לידים, רב-לשוניות, בינלאומי (קפריסין/דובאי/יוון/תאילנד). (2) מה אפשר לבנות עם קרדיט בנייה אחד, וכמה קרדיטים צריך לכל המוצר. (3) גבולות טכניים — האם WordPress מספיק או צריך אפליקציה/CRM חיצוני — תהיה כן. (4) רשימת ה-build prompts המדויקת לבנייה אוטונומית. בסוף READY FOR NEXT PROMPT.

**Step 3 — spend the build credit** on the highest-value gap once the above returns (recommended: the `/styleguide` component gallery + key screens from the Report-5 tokens — turns the design into something you can see and click).

**Step 4 — own the code.** Sync Lovable → your GitHub, own the backend, deploy to your host (no lock-in).

## Honest bottom line (no flattery)
- **WordPress is the content layer, not the app layer.** The map/3D/auth/dashboard/lead portal is a separate web app. Plan for two integrated systems. Forcing it all into WP will fail.
- **"3D interior for every apartment" isn't realistic short-term.** Tier it: Mapbox 3D city everywhere → project exterior+view → real interior only where captured → photo/floor-plan fallback. Start with new projects (the real money now).
- **You'll need a CRM/lead engine** and **some human-in-the-loop** for Israeli broker-license/consent/KYC. Full autonomy elsewhere is fine.
- **One free build credit/day won't build this** — plan a paid build or export-and-build-on-your-own-repo with a coding agent.

## Asset manifest (visuals already in the repo — for reference & reuse)
- Current-site UI previews: `docs/qa/screenshots/premium-revenue/preview-1440.png`, `preview-full-1440.png`, `preview-mobile-500.png`, `before-live-current.png`, `before-commerce-blocker.png`.
- Rainbow gold-standard project media (design reference): `docs/rainbow-media/hero.png`, `amenities.png`, `location.png`.
- Strategy files (this bundle's sources): `strategy/lovable-reports/04…07.md`, `strategy/gap-analysis-and-build-plan.md`, `strategy/war-room-master-report.html`, `strategy/NADLAN-MASTER-PROMPT` (= Part 1 here).
- Repo research: `skills/keyword-to-page-map.md`, `link-building-playbook.md`, `cannibalization-detection.md`, `seo-audit-checklist.md`, `ready-to-paste-profiles.md`.
- *Note:* the 3D-design-direction screenshot shared earlier was not in this session's uploads (cleared between sessions) — re-attach it when you next need it referenced.

_End of bundle. Created 2026-06-22._