# Owner Assessment — Full Scan (2026-06-11)

Scanned: live site (healthcheck, sitemaps, 238 pages, 23 glossary terms, sample page contents),
repo state, deployment state. Codex is out of tokens; Claude solo until he's back.

## 1. SYSTEM STATE — the machine is BUILT but NOT RUNNING
Live = v1.56.0. All 6 new modules deployed and verified (73+ executed assertions) but ALL DARK:
lead_e2e OFF, lead_ai OFF, lead_nurture OFF, admin_control OFF, help OFF. No OpenAI key. No Morning
IPN secret/links. **Zero-intervention monetization = 0% operational today** because the ignition
keys are owner-side config, not missing code. E2E live QA was interrupted mid-run (Codex tokens).

## 2. CONTENT — real cannibalization risk + concentration
- 0 blog posts; strategy is 238 PAGES + 23 glossary terms.
- 38 "X-prices" pages = heavy concentration in one niche (owner is right).
- CONCRETE cannibalization pairs found:
  * /tel-aviv-luxury-apartment-prices/ vs /property-value/luxury-apartments-tel-aviv/ — same topic,
    two silos. Merge or canonical one to the other.
  * /tel-aviv-apartment-prices/ vs luxury vs penthouse vs seafront — 4 pages chasing adjacent
    queries; need explicit query differentiation + hub linking, or consolidation.
  * /commercial-real-estate/commercial-property-prices-tel-aviv/ vs /commercial-property-for-sale-tel-aviv/ — borderline; differentiate intent (prices=research, for-sale=transactional).
- Diversification gaps: buyer-journey guides, legal/tax processes, neighborhood-life content,
  developer/contractor-facing content are thin vs the price cluster. Glossary (bill of materials)
  at 23 terms — barely started vs the 100+ target.

## 3. PUBLIC-FACING LANGUAGE LEAKS — mostly clean, one real fix
- "placeholder" hits = HTML input attributes (innocent). "חשיפה לשמש" = legit Hebrew. No
  "לא נוכל להציג"-style anti-marketing found in sample.
- REAL issue = AUDIENCE MIXING, not tech leakage: advertiser-pitch language on consumer surfaces:
  * Homepage tile 04: "חשיפה לפרויקטים... מול קונים"
  * /projects/ archive sponsored tile: "הציגו את הפרויקט שלכם כאן — חשיפה מועדפת... ₪3,990"
  /join-pro/ uses "לידים חמים" — CORRECT there (B2B audience). Fix = consumer-safe rewording on
  consumer surfaces only; keep the CTAs.

## 4. EEAT — weak today; owner's plan is right with two adjustments
Current price page: no Person schema, no reviewedBy, no sameAs, no visible reviewer/updated line.
Owner plan (lawyer; second site = Justice legal portal; name as reviewer at END of article):
- VERDICT: end-of-article reviewer box is BEST PRACTICE, not a compromise. Top-of-article author
  flags are for news; review credentials belong at the end + in schema.
- Implementation (both sites, correlated):
  a. Visible: end box "נבדק על ידי עו״ד <name>" + 1-2 line credentials + link to author/about page.
  b. Schema: Article.reviewedBy → Person with a stable @id; Person.sameAs → [Justice-site author
     page, LinkedIn, bar registry if available]. SAME Person @id/sameAs on BOTH sites = entity
     reconciliation (the correct cross-site authority play; NOT mass cross-linking).
  c. Visible "עודכן בתאריך" near top on price pages (freshness), reviewer at bottom.
- HONEST LIMIT: reviewedBy must stay in-expertise. A lawyer credibly reviews legal/tax/transaction
  content — NOT renovation costs or architecture. Apply the reviewer box selectively or it cheapens
  the signal and risks looking manufactured.

## 5. BIG IDEAS — honest feasibility
- PRIVATE-HOME AUCTION: real feature class (cf. Openn Negotiation). Legal caution: facilitating
  deals for a fee touches חוק המתווכים (broker licensing) — owner-lawyer must clear the model.
  PHASE IT: start as "הצעות מחיר" (offer collection + connect parties), not binding auction —
  90% of the engagement, far less legal exposure. The auction plumbing (bids table, REST) already
  exists in the plugin.
- 3D FLY-THROUGH OF ALL PROJECTS IN ISRAEL: nobody has these models. Realistic path: (1) embed
  contractor-provided Matterport/3D per project NOW (seam in Mission 1), (2) map-based 3D massing
  via Mapbox/Cesium + GovMap coordinates (mid-term), (3) per-apartment pick+purchase only where the
  contractor supplies a live availability feed (long-term, partnership-dependent). Multi-quarter
  roadmap, not a chunk.
- AUTO-ADDING PAGES TO MENUS: fully automatic nav = UX/SEO risk. Recommended: auto-ADD inside hub
  pages + auto-SUGGEST for the main menu with one-click approve in admin-control. Curated nav wins.

## 6. ROADMAP (priority order — money first)
P1 ACTIVATE THE MACHINE (days): flags on one-by-one with live QA each — lead_e2e → OpenAI key +
   lead_ai → lead_nurture → Morning secret/links + recurring → admin_control + help. Finish the
   interrupted E2E QA with screenshots. Building more while the engine is off = waste.
P2 CONTENT INTEGRITY SPRINT: cannibalization fixes (merge/canonical the pairs above), page→pillar
   map, hub-and-spoke internal linking, consumer-surface language pass.
P3 EEAT ROLLOUT: reviewer system (end-of-article + reviewedBy/Person/sameAs schema) on both sites,
   correlated entity; visible updated-dates on price pages.
P4 CONTENT DIVERSIFICATION: glossary to 100+ terms, buyer-journey + legal/tax guides (reviewer
   shines here), neighborhood content; front-page correlation to silos + curated nav.
P5 LISTINGS LEVEL-UP: Mission 1 (listing upgrade + 3D/Matterport embed seam) → offers/"auction"
   MVP → contractor availability-feed pilot.
