# MASTER RESET — homepage, projects template, design language (owner directive 2026-07-02)

> **Status: THE next major mission.** Owner is NOT satisfied with the homepage and project
> pages. No more incremental patches on these two surfaces — this is a researched rebuild.
> Read this whole file before writing any code. Execute phases IN ORDER.

## Owner verdict (verbatim intent, 2026-07-02)
- Homepage: "not professional", signals ONLY projects; must signal ALL of real estate
  (listings, professionals, guides, calculators); used to have a MEGA MENU (not found in
  this repo's git history — check the live server's other theme folders / pre-fork theme,
  and the Lovable SiteHeader.tsx); wants sponsored professionals floating in listings and
  project pages (Madlan-style monetized placements); rich + multilingual + switchable.
- Projects: do a literal ONE-ON-ONE teardown vs Zillow / Compass / Homes.com (render
  logic, sales logic, SEO); first paragraph must answer the Google query; progressive
  clickable info journey (click → deeper info → deal); financing/advisory/interior-design
  embedded at decision points; **FIRST-PERSON INTERIOR TOUR is a repeated owner demand
  and is still not delivered — top priority**; every project should rank #1 (low
  competition on project names); pages must SELL (softly) and route the deal through the
  owner (share on every deal, without exposing the mechanism).
- Fix: "Speak with Us" element that reveals the accessibility button (needs screenshot/DOM).
- Design: one language across everything; premium ≠ gold; Lovable tokens
  (`handoff/lovable/2026-06-23-war-room-sync/prototype-source/src/styles.css`, oklch
  cream/ink/terracotta + Frank Ruhl Libre/Heebo); fix remaining contrast issues.

## Phase 0 — RESEARCH FIRST (no code until this exists as a doc)
1. In Chrome: screenshot + teardown Zillow home, Compass home, Homes.com home, Madlan home
   (desktop+mobile). For each: section order, what's above the fold, search placement,
   how professionals/agents are monetized on surfaces, nav/mega-menu structure, language
   switching. Produce `docs/research/homepage-teardown.md` with a section-by-section
   comparison table vs ours.
2. Same for ONE Zillow listing page + ONE Compass listing + Madlan project page vs our
   Ashira: hero, first-viewport info density, CTA placement rhythm, progressive disclosure
   pattern, schema/SEO (view-source titles/H1/first paragraph/JSON-LD).
3. Dig the "previous mega menu": live server theme folders (File Manager), pre-fork theme
   in git history (`git log --all -- parts/header.html`), Lovable `SiteHeader.tsx`.

## Phase 1 — Homepage rebuild (one release, design-reviewed via preview HTML BEFORE shipping)
Sections (Madlan/Zillow-informed, all CMS-driven, zero hardcode):
hero with ONE search box (tabs: לקנייה/להשכרה/פרויקטים/בעלי מקצוע, autocomplete module
exists) → trust strip (2,711 מאומתים · 965 פרויקטים · מחשבונים · ליווי עו"ד) → featured
projects carousel (unified imagery treatment: one aspect, one overlay style — fix the
"three projects three styles" complaint; paid_tier drives order = monetization) → listings
band (magazine cards, latest+featured) → **sponsored professionals band** (premium profiles
carousel with monogram cards; "הצטרפו" tile → /advertise/) → tools band (calculators) →
guides band (pillars) → market-numbers band (real counts) → foreign-investor EN gateway
block → full mega-menu header + rich footer. Multilingual: nav/hero/bands translated
(he/en at minimum) with a real switcher; EN homepage variant at /en/ once EN pillar
content publishes. Preview-first: build docs/previews/homepage-v2-preview.html, owner
approves look, THEN implement as pattern/plugin.
## Phase 2 — Project template v2 ("render like Zillow")
Order: H1 + SEO-first-paragraph (query-answering, meta-driven) → gallery/3D hero with
unified imagery → key facts strip → sticky section nav → apartment selector →
**FIRST-PERSON INTERIOR (see Phase 3 — ship together)** → price/financing block (mortgage
calc inline + "צריכים מימון?" advisor CTA) → interior-design CTA block (floor-plan sketch +
"עצבו את הדירה" → designer professionals carousel = sponsored placement) → live map →
future plans → contractor block → article → FAQ (schema) → similar projects. Every block
CMS-driven; sponsored professional slots wired to paid_tier (the Madlan-style monetization
the owner asked for). SEO: Article+FAQPage+Product JSON-LD, first paragraph from meta.
## Phase 3 — First-person interior tour (THE debt; ship with Phase 2)
Practical path (no Unreal): three.js/<model-viewer> walkthrough INSIDE a parametric
apartment shell generated from rooms/sqm meta (rooms as lit boxes, openings, balcony,
window light by direction) — camera at eye height, tap-to-move hotspots (pano-style),
mobile gyro look. Cloud Design's clickable "drawer" model: search handoff/ + git history
for the animated GLB (owner remembers it; likely in an unmerged branch or external zip).
If found, wire it as the flagship. GLB regeneration pipeline for contractors = /studio/
upload → validated → replaces parametric shell. Label all generated interiors הדמיה.
## Phase 4 — Design-language unification release
One tokens.css (Lovable oklch set) consumed by ALL modules (nlps/nlpjx/nlpp/nldir/engine);
kill remaining gold-overload; AA contrast pass; owner screenshots reviewed before merge.

## Owner wish list (the "million-dollar" menu — owner picks, agent builds)
1. **Price/comps engine** (nadlan.gov.il ETL → live comps on every listing/project +
   monthly auto-report page) — the Madlan moat, ~₪150k agency work.
2. **First-person apartment tours** (Phase 3) — no IL portal has it, ~₪200k+ custom.
3. **City hub pages** /buy/tel-aviv etc. wired to live supply — Yad2's head-keyword moat.
4. **Lead marketplace**: routed leads with owner share on every deal (lead-ledger exists;
   add routing rules + contractor dashboards + monthly statements) — the actual business.
5. **AI everywhere**: search-by-description ("דירה עם מרפסת לים עד 2.5M"), AI buyer
   concierge per project, auto-valuation chat — engine exists, surfaces don't.
6. **Foreign-investor funnel**: EN cluster (Cowork writing now) + EN homepage + currency
   toggle + "buy from abroad" service page with the lawyer angle = highest-margin leads.
7. **Auto video reels** per project (slides+TTS from CMS data) for social/YouTube SEO.
8. **Contractor SaaS tier**: white-label showroom embed on THEIR site (iframe of our
   engine, our branding+leads) — recurring B2B revenue.
9. **Market data PR engine**: quarterly Hebrew press-release-grade reports from public
   data — backlinks + brand.
10. **WhatsApp bot** on the existing ingestion: buyers query inventory conversationally.

## Standing rules
Preview-first for all visual work (owner approves HTML preview before live). Deploy via
skills/agent-direct-wordpress-access.md. Verify inside the ZIP. No mocks; CMS-driven only.
The Cowork content mission runs in parallel and must not be blocked.
