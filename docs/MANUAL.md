# nad-lan.co.il - THE MANUAL (auto-generated 2026-07-12)

One WordPress plugin (`nadlan-config`) carries every behavior on the site.
This manual is generated from the module doc-headers by
`scripts/build-manual.py` - regenerate after adding modules, never edit the
module sections by hand.

## The products (user-facing surfaces)

| Product | URL | What it is |
|---|---|---|
| Homepage v2 | / | Aerial hero, flagship 3D theater, light live map (city chips), renewal + rentals bands, tools, magazine |
| Projects catalog + 3D showroom | /projects/, project pages | Every project as a living 3D model: floors, apartments, sun, view, walk, offer flow |
| Listings | /properties/, listing pages | Sale/rent listings with facade selector, costs, map, wizard at /list-property/ |
| Professionals directory | /professionals/ | Vetted pros, profiles, reviews, RFP matching |
| Apartment Studio | /studio/ | Drag furniture, plan the apartment, notes to RFP |
| Urban renewal hub | /urban-renewal/ (+ sub-pillars, map, check) | SEO pillar, tools, AI wizard, TAMA-alternatives, English guide |
| Renewal project room | /my-renewal/ | Private building room: 3D consent map, 10-stage ladder, docs, updates (HE/EN/RU) |
| Rentals manager | /my-rentals/ | The digital lease file: portfolio map -> building 3D -> apartment panel; ledger, securities cap, CPI + tax calculators, statutory deadlines (HE/EN) |
| Calculators | /mortgage-calculator/ etc. | Mortgage, purchase tax, buy-vs-rent, value estimator |
| Glossary | /glossary/ | Real-estate encyclopedia terms, autolinked site-wide |
| Advertiser center | /advertise/, /pricing/ | B2B funnel: signup, placements, orders |

## Feature flags (wp option, '1' = on)

- `nadlan_feature_admin_control`
- `nadlan_feature_compound_map`
- `nadlan_feature_help`
- `nadlan_feature_lead_ai_qualify`
- `nadlan_feature_lead_drip`
- `nadlan_feature_lead_nurture`
- `nadlan_feature_offers`
- `nadlan_feature_renewal_map`
- `nadlan_feature_renewal_space`
- `nadlan_feature_renewal_wizard`
- `nadlan_feature_rentals`

## Modules (from each file's doc header)

### accessibility.php
```
nadlan-config - First-party accessibility widget + statement (owner 2026-07-07:
"the accessibility icon is not showing anywhere, bundled under the plus").
No third-party a11y plugin exists on the site, and Israeli regulation
(תקנות שוויון זכויות לאנשים עם מוגבלות, תקן 5568 / WCAG 2.0 AA) requires a
visible accessibility control and a statement page. This module ships both:
a standalone, always-visible button (NOT bundled in the floating CTA
cluster) opening a panel of real adjustments, each applied as an <html>
class and persisted in localStorage; plus a link to the statement page.
```

### admin-control.php
```
nadlan-config - Chunk E operator admin control plane (v1.55.0).
Ships dark behind nadlan_feature_admin_control. OFF means no menu, no REST
routes, no registered admin-control meta, and no custom operator capability.
```
REST: `nadlan/v1/admin-control/cards`, `nadlan/v1/admin-control/card/(?P<id>\d+)`, `nadlan/v1/admin-control/bulk`, `nadlan/v1/admin-control/impersonate/start`, `nadlan/v1/admin-control/impersonate/end`, `nadlan/v1/admin-control/impersonate/write-toggle`

### advertiser-center.php
```
nadlan-config - Advertiser Center (v1.41.2)
A customer-facing command center for claimed professionals, project advertisers,
and promoted property owners. It closes the post-payment gap by giving every
logged-in advertiser one place for owned cards, completion checks, views,
inquiries, reviews, recent orders, Studio edit links, and upgrade paths.
```
Shortcodes: `[nadlan_advertiser_center]`

### advertiser-orders.php
```
nadlan-config - Advertiser order bridge (v1.41.2)
Keeps paid advertising orders aligned with the existing directory contract:
`paid_tier` is the only ranking/gating source of truth. The only card-level
meta added here is campaign_end, paid_order_id, and paid_product_id.
```

### ai-brain.php
```
nadlan-config - THE AI BRAIN (2026-07-07, owner order: "make the AI brain
much, much smarter, prompted inside to get the best outputs").
A thin, research-backed pipeline layer on top of nadlan_ai_chat(). Each
primitive implements a published technique with measured gains:
 1. nadlan_brain_house_rules()  - a shared "constitution" appended to every
    system prompt: grounding-only answers (RAG discipline - Lewis et al.
    2020, arXiv:2005.11401), honesty laws, Hebrew register, dash law.
 2. nadlan_brain_judge()        - LLM-as-a-Judge rubric scoring (Zheng et
    al. 2023, MT-Bench, arXiv:2306.05685): score a draft 1-10 against an
    explicit rubric, return issues.
 3. nadlan_brain_refine()       - Self-Refine (Madaan et al. 2023,
    arXiv:2303.17651): feed the judge's critique back for one revision
    pass (~20% avg preference gain across tasks in the paper).
 4. nadlan_brain_vote()         - Self-Consistency (Wang et al. 2022,
    arXiv:2203.11171): sample N answers, majority-vote the label. Used
    SELECTIVELY (only when confidence is low) to stay cost-aware.
Everything is gated: option nadlan_brain_enabled (default on) and the
provider's own cost caps still apply to every e
... (truncated)
```

### ai-concierge.php
```
nadlan-config - AI Concierge grounding + handoff (v1.48.0).
The concierge answers only from local NadLan content, cites the source used,
and creates a private handoff ticket when the answer is not grounded or the
visitor asks for a human.
```
REST: `nadlan/v1/concierge`, `nadlan/v1/concierge-lead`

### ai-features.php
```
nadlan-config - AI features: listing-description generator + natural-language search (v1.9.0)
Two cutting-edge features, one LLM adapter, deliberately compliance-first:
 1) AI listing-description generator (admin button on nadlan_property edit):
    -- Hebrew, factual, 85-150 words, 8-10th grade, neutral-warm tone.
    -- GUARDRAILS: no steering language by protected class (family status,
       religion, ethnicity, origin, gender, age, disability) - matches HUD
       Fair-Housing 2024 guidance AND Israeli חוק איסור הפליה במוצרים ובשירותים.
    -- POST-GENERATION SCAN flags banned phrases ("מתאים למשפחות עם ילדים",
       "קרוב לבית כנסת/כנסייה", "שכונה דתית/חילונית", "ל-zugot צעירים", etc.)
       and refuses to auto-publish if hits found - surfaces to editor instead.
 2) Natural-language search: visitor types "דירת 4 חדרים בתל אביב עד 3 מיליון
    עם מעלית" → LLM parses to a STRUCTURED filter ({city,rooms_min,price_max,
    amenities[]}) → WP_Query → results. Deterministic regex fallback for the
    common Hebrew patterns so it works even if LLM is unavailable.
LLM adapter: nadlan_llm_request($prompt, $opts) now delegates to the shared
GAP 4 provider adapter, nadlan_ai_chat(). D
... (truncated)
```
REST: `nadlan/v1/nl-search`
Shortcodes: `[nadlan_nl_search]`

### ai-provider.php
```
nadlan-config - provider-agnostic AI adapter (GAP 4, v1.43.2).
Default provider is OpenAI. Anthropic stays available as a fallback so older
installs with an existing key keep working. Secrets are read only from server
constants or WordPress options, never from client-side code.
```

### archive-grid.php
```
nadlan-config - Branded archive grid for directory CPTs (v1.28.0)
The nadlan_professional / nadlan_project / nadlan_property archives are now linked
from the homepage, nav, footer and /catalog/ - but they were rendering through the
theme's default archive loop, which shows these data-only CPTs (no editor body) as
blank/plain rows. With 1500+ imported professionals that looked broken.
This module intercepts those archives (template_redirect, like city-hubs) and renders
a clean, branded, paginated CARD GRID built from the real meta - name, city,
classification, registry number, claim badge - matching the catalog skin. Facets bar
on top (reuses [nadlan_facets]). Keeps the theme header/footer so it stays on-brand.
Opt-out: define NADLAN_DISABLE_ARCHIVE_GRID to fall back to the theme template.
```

### autocomplete.php
```
nadlan-config - City / professional / project autocomplete (v1.15.0)
Powers the city input across facets, saved-search, AVM tool, and NL search
with a single fast REST endpoint backed by a daily-cached city index.
GET /nadlan/v1/suggest?q=&type=city|professional|project   → top 10 matches.
For 'city': aggregates the distinct city meta values across the 3 card CPTs
with their counts (so "תל אביב (1240)" appears).
Cache: full index in a 24h transient; query just filters in-PHP.
```
REST: `nadlan/v1/suggest`

### avm-deals.php
```
nadlan-config - Deal history + AVM + neighborhood data (v1.7.0)
The Madlan-parity data layer. Three parts:
 1) A cached deals table ({prefix}nadlan_deals) - populated by an ETL adapter
    (govmap/nadlan endpoints, verified by Cowork mission M10) OR by a direct REST
    ingest so we are not blocked on reverse-engineering. NEVER call upstream
    per-pageview - always read from the cache.
 2) A comparable-sales AVM (hedonic-lite): median ₪/sqm of nearby comps × subject
    sqm, with a confidence score derived from comp count + dispersion (a forecast
    standard deviation, FSD-style). Degrades to "insufficient_data" when the table
    is sparse, so nothing breaks before deals are seeded.
 3) Neighborhood stats panel + a "what's my home worth" seller lead funnel.
Method grounding (2025-26): AVMs combine comparable-sales + hedonic regression;
best practice exposes a confidence/FSD score and an explainable range. ML upgrade
(gradient boosting / SHAP explainability) is roadmap - see architecture skill.
BLANKS (owner/legal): storing nadlan.gov.il price data needs ToS/legal sign-off
(docs/listings-questions.md A.6). The estimate is informational, not an appraisal.
```
REST: `nadlan/v1/deals-ingest`, `nadlan/v1/avm`
Shortcodes: `[nadlan_home_value]`

### breadcrumbs.php
```
nadlan-config - Breadcrumbs (visible + BreadcrumbList JSON-LD) (v1.14.0)
Output a Hebrew breadcrumb trail on every NadLan CPT single and on archives,
and emit BreadcrumbList JSON-LD for Google rich results (eligible site-wide
link sitelinks improvement). Skips if Yoast already prints its own
BreadcrumbList to avoid duplicate schema.
```

### brochure.php
```
nadlan-config - THE PER-APARTMENT BROCHURE (world-competitor gap #2,
owner-approved sequence 2026-07-07).
A buyer picks apartment N in the 3D building and gets a branded, print-ready
one-pager of THAT apartment: floor, direction, size, price estimate with the
mortgage line, project facts, honest disclaimers, and a deep link straight
back to the same unit selected in the 3D model. Browsers print it to PDF -
zero server dependencies, works on shared hosting.
GET /nadlan/v1/brochure?p=<project_id>&u=<unit_id>[&lang=he|en]
MONETIZATION: meta `project_brochure_logo` (URL) puts the developer's logo
on the sheet - a paid placement; absent, the brand mark carries it.
Every render increments `nadlan_brochure_views` on the project - fuel for
the developer analytics story.
```
REST: `nadlan/v1/brochure`

### bulk-project-seo.php
```
Bulk SEO fix for the long-tail nadlan_project catalog (966 pages per the live
sitemap, checked 2026-07-01 -- see docs/marketing/2026-07-01-marketing-seo-revenue-strategy.md).
Most of these were imported with just an address as the post title and no
SEO meta, so WordPress/Yoast falls back to "{title} - {site name}" -- no
buyer intent, no "for sale", nothing a search engine or a buyer's eye
catches. A handful of flagship projects (Rainbow, Ashira) already have
hand-written, richer titles set via their own higher-priority filters
(see project-page-assembly.php) -- this file runs at LOWER priority so it
never overrides those; it only fills in the gap for everything else.
Honesty rule: only real data is used (the post's own title, and its
nadlan_city term IF one is actually set). Never invents a city, price,
room count, or floor count that isn't already in the post.
```

### business-metrics.php
```
nadlan-config - business metrics + autopilot snapshot (v1.49.0).
Computes a daily, cached owner snapshot without requiring the draft billing,
lead-routing, auction, or AI branches to be present. When those branches land,
this module reads their logs/options automatically.
```

### buy-rent-calc.php
```
nadlan-config - Buy-vs-Rent decision engine + apartment deal analyzer (v1.71.4)
Two traffic-magnet tools, NYT-methodology with the Israeli layer no one else has:
  [nadlan_buy_vs_rent]   year-by-year simulation: buying (mortgage, purchase tax
                         from the dated brackets in calculators.php, upkeep,
                         appreciation, selling costs) vs renting AND investing the
                         equity + monthly difference. Net-worth curves on canvas,
                         break-even year, verdict, sensitivity chips.
  [nadlan_deal_check]    "is this apartment a good buy" analyzer: price/sqm vs the
                         user's area benchmark, yield vs alternatives, leverage
                         stress, total acquisition cost. Letter-grade verdict +
                         what-to-check list + AI deep-analysis lead funnel.
YMYL discipline: every figure is an estimate with visible assumptions the user
controls; purchase tax carries its effective date + verify link; no result is
presented as advice. No long dashes anywhere (owner law).
```
Shortcodes: `[nadlan_buy_vs_rent]`, `[nadlan_deal_check]`

### calculators.php
```
nadlan-config - Lead-magnet calculators (v1.19.0)
Rulebook §9.3 calculator suite (mortgage + home-value already exist in
listings-ux/avm-deals). This adds the rest as client-side shortcodes, each a
lead funnel:
  [nadlan_calc_purchase_tax]   מס רכישה   (brackets, filterable + dated)
  [nadlan_calc_capital_gains]  מס שבח     (ESTIMATE only - heavy disclaimer)
  [nadlan_calc_yield]          תשואת שכירות (ברוטו/נטו)
  [nadlan_calc_equity]         הון עצמי נדרש (LTV per Bank of Israel)
  [nadlan_calc_total_cost]     עלות רכישה כוללת
YMYL discipline: tax figures are FINANCIAL. Brackets live in a filterable PHP
array with an effective-date label + a visible "verify with רשות המסים" line +
authority link. Capital-gains is genuinely complex (linear calc + exemptions),
so that one is an explicit ESTIMATE with a lawyer/tax-advisor CTA, never a
definitive number.
BLANK (owner/Cowork): the surrounding pillar-page Hebrew copy (H1, explainer,
FAQ, spokes) is written via the ChatGPT→Cowork batch; this module is the WIDGET.
Update brackets each January via the nadlan_purchase_tax_brackets filter.
```
Shortcodes: `[nadlan_calc_purchase_tax]`, `[nadlan_calc_capital_gains]`, `[nadlan_calc_yield]`, `[nadlan_calc_equity]`, `[nadlan_calc_total_cost]`

### cards-render.php
```
nadlan-config - Card front-end render (v1.5.0)
Appends to single card views (project / professional / property):
  - a facts/stats table built from meta (the "Wikipedia-style" data block),
  - a media gallery from photos_csv,
  - a CLAIM CTA (if unclaimed) that posts to /nadlan/v1/claim,
  - a provenance line (source + last updated).
Also registers a [nadlan_card] shortcode and a [nadlan_directory] index list.
Theme-safe: appends via the_content (does not fight block templates) and ships
scoped inline CSS/JS only on card views.
```
Shortcodes: `[nadlan_card]`

### catalog-meta.php
```
nadlan-config - Catalog meta (v1.5.0)
Registers REST-exposed post meta for the directory "cards":
  - nadlan_project       (real-estate projects / developments)
  - nadlan_professional  (contractors + service givers: kablan, shamai, bedek-bait, etc.)
plus the SHARED claim/ownership meta on all three card CPTs (property/project/professional)
that powers the free-card → claim → upgrade funnel.
Design: parallels nadlan_config_register_property_meta(). Public read meta is
show_in_rest true; writable listing meta requires edit_post on that listing EXCEPT claim_status/owner which
are managed server-side via the claim flow (inc/claim.php), so they are read-only
over REST (auth_callback false for writes).
```

### catalog-shine.php
```
nadlan-config - Catalog / WooCommerce premium skin (v1.22.0)
The owner's catalog is a WooCommerce store (/catalog/, /shop, product archives).
Default Woo styling looks generic ("lame"). This module ships a SCOPED, brand-
matched skin (gold #9C7A3C, ink #1B1A17, cream #FAF7F1, Heebo) that only loads on
Woo surfaces - no global CSS bleed, no theme edit, no extra HTTP request (inline).
What it restyles, modern-store grade:
  - product grid cards: white, rounded, soft shadow, hover lift + image zoom
  - price in brand gold, sale badge as a gold pill, rating stars
  - add-to-cart / buttons: ink → gold hover, full-width on cards
  - single product: cleaner gallery, sticky-feel summary, polished tabs
  - store notices / messages on-brand
  - RTL-correct throughout (Hebrew store)
Guarded: does nothing if WooCommerce is not active.
```
Shortcodes: `[nadlan_featured_pros]`

### city-hubs.php
```
nadlan-config - Programmatic SEO city hubs (v1.10.0)
Auto-generates city/neighborhood hub pages that target GENERIC keyword intent
("קבלנים רשומים ב<עיר>", "פרויקטים ב<עיר>", "דירות למכירה ב<עיר>") and link DOWN
to the branded cards. Cannibalization-safe: hub keyword ≠ branded card keyword.
2026 best practice (research): ≥25-30% UNIQUE data per hub, quality > volume.
10 strong city hubs beat 100 thin ones. Doorway/scaled-content abuse is a real
Google penalty now. Therefore:
  - Floor: each hub must have ≥ NADLAN_HUB_CARD_FLOOR cards (default 5) of the
    relevant type, else 404 (no thin pages enter the index).
  - Per-hub unique data = card count + neighborhood AVG ₪/sqm (from wp_nadlan_deals)
    + deal volume + top 8 cards rendered inline. Not "nice place to live".
  - JSON-LD CollectionPage + ItemList for rich results.
Three rewrite endpoints (front-end only, no DB pages - clean and cache-friendly):
  /city/<city>/contractors/   → contractors hub
  /city/<city>/projects/      → projects hub
  /city/<city>/properties/    → properties hub (listings)
Cross-link: each hub links UP to the relevant pillar (e.g. /real-estate-lawyer/
for property hubs; the encyclopedia/glossary hubs o
... (truncated)
```

### claim-prompt.php
```
nadlan-config - Claim prompt on directory + profile (v1.40.0 / shark #11)
Adds a contextual "this is my card?" prompt on every unclaimed professional
profile page. Contractors searching their own name (a common behavior - they
Google themselves) hit the profile and see a clear claim-this-card path
→ claim → 30-day Pro trial → recurring revenue.
The claim funnel itself already exists in inc/claim.php (created in v1.5.0).
This module just makes it impossible to miss.
```

### claim.php
```
nadlan-config - Card claim & ownership funnel (v1.5.0)
Flow: free auto-created card (unclaimed) → owner submits a CLAIM via the public
REST endpoint → stored as a private nadlan_claim, card flips to "pending", admin
is emailed → admin APPROVES (assigns a WP user as owner) → card flips to
"verified" and that user may edit ONLY their own card (upload photos, edit text).
SECURITY NOTE (flagged for the Cowork review pass - see docs/listings-questions.md):
 - The identity-verification METHOD (proving the claimant truly owns the entity)
   is intentionally left to admin judgement + a token here; a stronger automated
   check (email-domain match, phone OTP, registry cross-check) is a TODO.
 - Owner editing is scoped to the owner's own single card via map_meta_cap.
```
REST: `nadlan/v1/claim`

### compare.php
```
nadlan-config - Compare listings (v1.11.0)
Zillow/Redfin-grade side-by-side comparison. Pure client-side state (localStorage
= no auth required) + a server-rendered comparison view via shortcode and a
dedicated /compare/ rewrite. JSON-LD for the comparison page is intentionally
omitted (low-value for search; this is a UX/conversion feature, not an SEO page).
UX: a "Compare" button is added to property singles via inline JS that toggles
the listing into the tray; tray floats bottom-right with current selections.
Capped at 4 items.
```
REST: `nadlan/v1/compare`

### compound-map.php
```
nadlan-config - compound 3D fly-over map.
Renders a Mapbox GL JS district map for project compounds such as Sde Dov.
Ships dark behind nadlan_feature_compound_map.
```
Shortcodes: `[nadlan_compound_map]`

### compounds.php
```
nadlan-config - compounds (מתחמים): group projects under a development
compound (e.g., Sde Dov) with one archive page + filter facets by
developer / contractor / initiator. Always on (taxonomy registration is
harmless); front-end facets respect existing directory behavior.
```
Shortcodes: `[nadlan_compound_filter]`

### contextual-help.php
```
nadlan-config - Chunk F contextual help framework (v1.56.0).
Ships dark behind nadlan_feature_help. OFF means no scripts, no styles,
no pointers, no tooltip markup, and existing admin screens keep their
current behavior.
```

### conversion-cta.php
```
nadlan-config - Conversion CTA layer (v1.40.3)
STRIPPED 2026-06-03 per owner: the sticky bottom bar AND the exit-intent modal
are KILLED everywhere (mobile + desktop). They were too intrusive on mobile
(mouseout-based exit detection fired on scroll, sticky bar jumped the layout).
What remains:
  - Floating WhatsApp click-to-chat button (owner-controlled via Settings → NadLan CTA)
  - window.nadlanGA() dataLayer helper (other plugin scripts depend on it)
  - /nadlan/v1/lead REST endpoint (still used by claim-prompt, AI concierge handoff, etc.)
  - Settings page for the WhatsApp number
If we ever want the popup/sticky back, restore from git history of this file
(last good version: v1.40.2). Don't re-introduce them without a UX plan.
```
REST: `nadlan/v1/lead`

### cotour.php
```
nadlan-config - LIVE CO-TOURING (enhancement #3, the crown jewel - Realsee's
killer feature, unseen in the off-plan world).
An agent and a buyer navigate the SAME 3D building together: the agent's
camera, selected apartment, lighting and filter broadcast every ~1.5s; the
buyer's screen follows. Transport is plain REST + transients - no sockets,
no external service, works on shared hosting. A room lives 5 minutes past
its last broadcast; the room code is the only secret (share the join link
only with your buyer).
 POST /nadlan/v1/cotour   {room, state}   - the host broadcasts
 GET  /nadlan/v1/cotour?room=...          - the viewer follows
The engine drives it via ?cotour=host|join&room=<code> on any project page,
with a one-click "share live tour" button in the theater.
```
REST: `nadlan/v1/cotour`

### directory-assets.php
```
nadlan-config - Premium directory CSS + JS (v1.31.0)
Split out of directory.php for readability. Vanilla JS, no dependencies.
```

### directory.php
```
nadlan-config  -  Premium professionals directory (v1.31.0)
A state-of-the-art, Midrag/Houzz/Thumbtack-class directory for /professionals/:
 - hero search (free text + city) with profession quick-pills (colour-coded + icons)
 - live AJAX filtering / sorting (no page reload) backed by a REST endpoint
 - sidebar facets with live counts (profession, city, verified-only)
 - premium colour-accented cards: avatar, profession pill, official-registry trust
   badge, rating stars (review-ready), location, classification, CTA
 - server-rendered first page (SEO + no-JS fallback) using the SAME card renderer
   that the REST endpoint returns, so AJAX and server output are identical
 - sponsored/featured slot wiring (paid_tier) for the advertising model
Unique moat: every record is verified against the official רשם הקבלנים (gov.il),
surfaced as a trust badge competitors can't match.
```
REST: `nadlan/v1/directory`, `nadlan/v1/projects`

### drone-map.php
```
nadlan-config - Drone map on the projects catalog (owner ask 2026-07-06).
A cinematic satellite + 3D-buildings Mapbox view of every GEOCODED project,
injected as a collapsible band on the /projects/ archive. Pins are gold
NadLan markers; clicking flies in low over the site (drone feel) and opens
a popup linking to the project page.
HONESTY: only projects with real lat/lng meta appear (language siblings
excluded). Today that is the flagship set; the map grows automatically as
the geocode pass covers the wide catalog. The band says so, plainly.
Lazy: Mapbox GL loads only when the band is opened. No token -> no band.
```
REST: `nadlan/v1/project-map`

### en-hub.php
```
nadlan-config - English hub for foreign buyers (v1.69.97)
[nadlan_en_hub] renders the /en/ landing hub: hero, English project pages
(language siblings with the -en slug suffix), English guides (category
"english"), how-it-works trust points and a lead CTA. Everything is
CMS-driven; empty sections collapse. LTR by design.
```
Shortcodes: `[nadlan_en_hub]`

### facets.php
```
nadlan-config - Archive facets / filters (v1.14.0)
Yad2/Madlan-grade filtering on /properties/, /projects/, /professionals/.
Server-side `pre_get_posts` translates URL query params (?city=&rooms_min=&
price_max=&listing_type=&profession=&project_type=) into the appropriate
meta_query so filtered URLs are CRAWLABLE + LINKABLE (great for SEO + share).
Client side: a thin filter UI is injected via shortcode [nadlan_facets type=]
AND auto-prepended on the archive (just before the loop). Submits as a GET form
so URLs stay clean.
Cannibalization safety: only certain facet COMBINATIONS are valuable
(city alone, city+rooms, city+price-band). Everything else (single price-band
across all cities, deep combinations) emits noindex,follow to avoid the
scaled-content abuse penalty.
```
Shortcodes: `[nadlan_facets]`

### feature-flags.php
```
nadlan-config - master feature switchboard. Always visible to admins so dark
features can be turned on without hunting per-module pages.
```

### featured-upsell.php
```
nadlan-config - Featured upsell on claimed profiles (v1.40.0 / shark #8)
When a contractor is logged in viewing their OWN claimed profile (or any
verified-claimed profile), show a "your card is in position #X - upgrade to
land in top-5 in your city" banner with one-click checkout. The position is
computed live from the same featured-sort the directory uses. Conversion
driver for the existing Pro/Premier products (476/477) - turns the abstract
"upgrade" into a concrete, ego-tickling pitch.
Also appended to ALL claimed-but-free profiles (not just the owner's) as a
sponsored-pitch - the contractor sees it any time they visit their own page.
```

### final-hardening.php
```
nadlan-config - close-out seams, privacy, and endpoint hardening (v1.51.0).
```

### funnel.php
```
nadlan-config - B2B funnel de-friction (owner god-mission 2026-07-06).
1) QUICK REGISTER: one small form on the listing-wizard gate creates the
   account and signs the visitor in on the spot - no email round-trip, no
   WP admin screens. Email verification can follow; the listing cannot be
   lost to a password email. Rate-limited + honeypot.
2) /pricing/ belongs to the commercial offer: 301 to /join-pro/ (WordPress
   was slug-guessing it onto an article about apartment pricing).
3) ADVERTISER APPLICATION: a native lead form appended to the /advertise/
   page so a developer who will not open WhatsApp still converts.
```
REST: `nadlan/v1/quick-register`

### ga4-events.php
```
nadlan-config - GA4 / dataLayer event bridge (v1.40.0 / shark #12)
Pushes funnel events to window.dataLayer so Site Kit / GA4 / GTM can see
the whole conversion flow:
  page_view (auto)
  directory_filter_used
  directory_card_click
  profile_view
  quote_request (click)
  quote_submitted (success)
  claim_request
  review_submitted
  upgrade_click
  subscription_paid (WooCommerce hook → ₪ event)
The data layer is the standard channel; if Site Kit is active it'll surface
them. If GA4 is not installed, the pushes are silent.
```

### geo-search.php
```
nadlan-config - GAP 5 geo search.
Adds radius and bounding-box queries over the existing postmeta lat/lng model.
Paid placement still wins first; distance is the secondary ordering signal.
```
REST: `nadlan/v1/near`

### glossary-autolink.php
```
nadlan-config - Glossary in-text auto-linker + discoverability (v1.22.0)
Two jobs that compound the glossary's SEO value with zero per-term work:
 1) AUTO-LINK: on any singular post/page/pillar/term, the FIRST occurrence of a
    published glossary term's title (whole-word, Hebrew-aware) becomes a link to
    /glossary/<slug>/. Builds internal links INTO the glossary from the whole
    site, automatically, as new terms are published. Caps at 4 links/page so it
    never looks spammy, skips headings/existing links/the term's own page.
 2) DISCOVERABILITY: the glossary archive (/glossary/) is live but is not linked
    from the site, so visitors (and the owner) can't find it. We append a glossary
    link to the primary nav menu and a footer credit, so it's reachable.
The term map is cached (transient, 6h) and rebuilt when a term is saved.
```

### glossary-intake.php
```
nadlan-config - Encyclopedia intake + drip scheduler (owner mega-project
2026-07-06: the professional real-estate encyclopedia, "better than the UK
one").
Extends the existing glossary engine (inc/glossary.php, CPT nadlan_term)
with what the full-world encyclopedia needs:
 1) ENTITY FIELDS: name_en (the attached English term - doubles the search
    surface and serves professional olim) and entity_type (term / material /
    tool / method / role / regulation / standard / person / organization /
    publication / formula / software).
 2) INTAKE ENDPOINT: POST /nadlan/v1/glossary-intake (admin app-password)
    accepts a JSON array of entries. Entries WITH content are scheduled as
    FUTURE posts on a drip (default 12/day spread across working hours -
    steady human cadence, never a bulk dump); entries without content are
    created as drafts awaiting their article. Duplicate titles are skipped.
 3) EN-TERM CHIP: term pages render the English term under the title.
The drip is the anti-"scaled content abuse" discipline: quality-gated
batches at a believable cadence, with the existing thin-content guard and
autolinker doing their jobs on each published term.
```
REST: `nadlan/v1/glossary-intake`

### glossary-writer.php
```
nadlan-config - The encyclopedia WRITER (owner 2026-07-07: "something much
more sophisticated" than hand-feeding ChatGPT).
A self-running editorial desk: every hour it picks staged skeleton drafts
(nadlan_term entries created by the intake), writes each one a full tiered
article through the site's own OpenAI key, validates it (word floor per
tier, dash law, clean HTML), and hands it to the publishing drip. The owner
feeds ontology batches; the site writes and publishes itself.
Models routinely undershoot long-form word targets (measured 2026-07-06:
gpt-4o-mini returned 422 words against an 800-1300 brief, finish_reason
stop), so a draft below its tier floor gets ONE expand pass - the draft is
sent back with the measured count and the target, and the longer result
wins. After the expand pass a 10% tolerance applies (a 668-word article
against a 700 floor is a near-miss, not thin content); a real failure is
recorded, counted per entry, and an entry that failed 5 times is parked
(surfaced as "stuck" in the status endpoint) so it cannot block the queue
front and burn the API every tick.
WP core gotcha (bit us 2026-07-06): wp_update_post on a draft whose
post_date_gmt is 0000-00-00 sile
... (truncated)
```
REST: `nadlan/v1/enc-writer-status`

### glossary.php
```
nadlan-config - Glossary / encyclopedia engine ("מילון נדל"ן") (v1.17.0)
The home for the Wikipedia-orphan term project (skills/content-encyclopedia-
glossary-plan.md). Each term = a definitional micro-spoke that ranks for a
low-competition "מהו X" query and passes link equity UP to a money pillar.
 - CPT `nadlan_term` (/glossary/<slug>/) + taxonomy nadlan_term_cat
   (construction/planning/law/finance/appraisal/professions/deal-types).
 - Per-term render: definition + "מה זה אומר בפועל" practical block + source
   line + cross-link UP to the pillar it feeds (the silo rule, rulebook §6).
 - DefinedTerm + DefinedTermSet JSON-LD (GEO/AI-citation bait).
 - A-Z + category glossary index at /glossary/.
 - Thin-content noindex until enriched (same anti-thin discipline as cards).
 - REST enrich endpoint reuse: import-enrich already accepts nadlan_term? No -
   extend it; here we add the term to the allowed types for enrichment.
Cannibalization (rulebook §3.6 + skills/content-encyclopedia-glossary-plan.md §2):
a term gets an indexable page ONLY if its intent differs from every existing
pillar/spoke focus keyword. Definitional intent ("מהו X") ≠ transactional. The
`related_pillar` meta enfo
... (truncated)
```
REST: `nadlan/v1/glossary-publish`
Shortcodes: `[nadlan_glossary_index]`

### greeninvoice-recurring.php
```
nadlan-config - Green Invoice recurring IPN bridge (GAP 3).
```
REST: `nadlan/v1/gi-ipn`

### guide-schema.php
```
nadlan-config - Guide schema + hreflang for cornerstone SEO guides.
Flagship guide articles (e.g. the "elevated apartment living" guide) are
ordinary WordPress posts, but they need three things Yoast does not add on
its own for a hand-authored bilingual guide:
  1. FAQPage JSON-LD (AEO / Google "People also ask" + AI answer surfaces),
     printed in wp_head so content filters cannot mangle an inline <script>.
  2. Reciprocal hreflang between the HE and EN siblings (no Polylang/WPML on
     this site), so Google serves the right language and never treats the two
     as duplicate content.
  3. A crawlable, visible language switch is the theme's job; here we only
     emit the machine signals.
Data lives in post meta so this is reusable for every future guide:
  guide_faq_json   JSON array of {q, a}
  guide_hreflang   JSON object { he: url, en: url, x-default: url }
  guide_cornerstone "1" marks it (also used to widen the internal-link net)
```

### health.php
```
nadlan-config - reliability health endpoint + bounded event log (v1.56.0).
```
REST: `nadlan/v1/health`

### home-v2.php
```
nadlan-config - Homepage v2: the 12-band rich homepage (v1.69.87)
Implements handoff/claude-design/2026-07-02-homepage/homepage-spec.md and the
standalone mockup (factory-run drop). The homepage's jobs: convert brand
traffic, distribute link equity into ranking surfaces, look like an
institution. Everything renders from CMS data; a band with missing data
collapses cleanly. Band order/on-off via option `nadlan_home_bands`.
Bands: ticker · browse (mega-menu links) · hero · market · projects(dark) ·
listings · areas · magazine · tools · pros · intl(dark) · megafooter.
Honesty rules: every figure prints value + source + date; catalog-derived
stats are labeled as such; sponsored slots carry a visible label; no "3D"
in headings (badge on cards only); no em-dash in copy.
```
Shortcodes: `[nadlan_home_v2]`

### i18n.php
```
i18n engine (2026-07-03) - systematic 5-language chrome for nad-lan.co.il.
LAW (see handoff/research/2026-07-03-multilingual-architecture.md):
- CHROME (nav, hero, footer, labels, switcher) is systematic: one string
  table per language, resolved via nadlan_i18n('key'). Change once, every
  surface reflects it. 'he' values equal the exact current Hebrew, so the
  Hebrew page renders byte-identical.
- CONTENT (article/news/project bodies) is NOT here - it must be real
  translated CMS text (generation run), never machine-faked. Until then it
  falls back to Hebrew with correct hreflang (no SEO penalty).
- SEO: distinct URL per language (/ , /en/, /fr/, /ru/, /ar/), self-canonical
  + bidirectional hreflang + x-default on every language page.
Missing keys fall back to the 'he' value (never blank, never broken).
```
REST: `nadlan/v1/i18n/(?P<lang>[a-z]{2})`

### import.php
```
nadlan-config - Directory importer (v1.5.0)
Seeds the free directory cards from AUTHORITATIVE PUBLIC data (no API key):
  - Contractors  ← רשם הקבלנים open dataset on data.gov.il CKAN (~14k rows)
                   resource_id 4eb61bd6-18cf-4e7c-9f9c-e166dfa0a2d8
  - Urban-renewal projects ← מתחמי התחדשות עירונית (~938 compounds)
                   resource_id f65a0daf-f737-49c5-9424-d378d52104f5
Idempotent: each card stores source_id (MISPAR_KABLAN / MisparMitham); re-running
updates rather than duplicates. Cards are created as data_quality=stub and get
noindexed until enriched (see inc/schema.php) so thin stubs never hit the index
or cannibalize keyword pages. A separate REST endpoint lets Cowork push the
ChatGPT-enriched original prose that flips a card to data_quality=enriched.
Triggers: WP-CLI (`wp nadlan import contractors`), an admin batch button, and a
REST endpoint for enriched-content push. Runs in batches to avoid timeouts.
```
REST: `nadlan/v1/import-enrich`, `nadlan/v1/import-run`

### interior-fp.php
```
nadlan-config - First-person interior view (v1.69.84)
The owner's repeated ask, delivered practically: a walk-inside view of an
apartment generated ENTIRELY from real unit data (rooms, sqm, mamad, balcony,
direction) - no GLB, no materials required, works for every listing/unit.
Pure CSS-3D (perspective + transformed wall planes) + vanilla JS:
  - eye-height camera inside the room, drag / touch-drag to look around
  - door hotspots walk between rooms (salon → kitchen → bedrooms → mamad → balcony)
  - window light placed on the compass wall matching the unit's direction meta
  - honest "הדמיה סכמטית" label; upgraded automatically when a contractor feeds
    real assets later (tour_url via media.php takes precedence upstream)
Shared surface: [nadlan_interior_fp] shortcode + nadlan_interior_fp_html()
used by listings (property-showroom plan view) and projects (unit selector).
```
Shortcodes: `[nadlan_interior_fp]`

### keys-hub.php
```
nadlan-config - Keys & Connections Hub (v1.69.94)
ONE admin page for every external key and switch (owner request 2026-07-02:
"I'm sick and tired of looking for places to put keys"). Stores into the
SAME option names every module already reads, so nothing else changes:
  AI:      nadlan_ai_provider, nadlan_ai_openai_key, nadlan_ai_anthropic_key,
           nadlan_ai_enabled (master), nadlan_ai_widget_enabled (chat bubble)
  Mapbox:  nadlan_mapbox_token
  Media:   nadlan_home_video_url
  Contact: nadlan_whatsapp_e164, nadlan_phone
  Billing: nadlan_gi_api_key, nadlan_gi_ipn_secret (morning/greeninvoice)
Secrets are keep-if-blank (an empty field never wipes a stored key) and are
never echoed back. Toggles + non-secret fields are also registered on the
REST settings endpoint so the agent can manage them; secret keys are NOT
REST-exposed and can only be set from this page.
```
REST: `nadlan/v1/keys`

### lead-ai-qualify.php
```
nadlan-config - Chunk C lead AI qualification (v1.53.0).
Ships dark behind nadlan_feature_lead_ai_qualify. When disabled, or when
OpenAI is not configured, Chunk B lead E2E remains the complete behavior and
no AI call is made.
```

### lead-drip.php
```
nadlan-config - Lead nurture drip engine (v1.12.0)
2026 best-practice (research): segmented state machine -
  new → active (0-14d) → mid (15d-6mo) → long (6-18mo); auto-respond < 2 min;
  5-8 emails over 30-60d for standard drip; demote if no engagement; opt-out
  on every email; SMS is higher-OR but defer (provider TODO).
Wires onto nadlan_lead post creation: stamps drip_state=new + nudges into
'active'. Cron checks daily, sends due steps (Hebrew, RTL-aware mailto-style),
advances state, demotes silent leads.
BLANKS: SMS/WhatsApp channel (Twilio/local), engagement tracking pixel (privacy
decision - IL Privacy Protection Law), branded HTML template, A leads escalation
to phone. Default = email only, opt-out link mandatory.
```
REST: `nadlan/v1/drip-optout`

### lead-e2e.php
```
nadlan-config - lead end-to-end flow (v1.53.0).
Ships dark behind nadlan_feature_lead_e2e. When the flag is off, existing
conversion-cta/admin-post lead behavior remains untouched.
```
REST: `nadlan/v1/lead/status`

### lead-inbox.php
```
nadlan-config - Unified Lead Inbox + Owner Daily Digest (v1.40.0 / shark #3, #4)
ONE admin page for every money signal:
  - new nadlan_lead (general lead capture, CTA bar, exit-intent, concierge)
  - new nadlan_referral (Lead Ledger, status=new = captured but not routed)
  - new nadlan_review (pending moderation)
  - new nadlan_claim (pending owner approval)
  - new Pro/Premier upgrades (WooCommerce paid orders for products 476/477/489)
Plus a daily CRON email digest to the owner summarising the last 24h.
The owner stops checking 5 places - everything is in ONE inbox under
the menu "💰 Lead Inbox", count badge shows pending items.
```

### lead-ledger.php
```
nadlan-config - LEAD LEDGER + revenue lock-in (v1.34.0)
Solves the owner's #1 pain: today leads go out to partners (lawyers, mortgage
advisors, brokers) and "the deal closes and nobody pays me back." This module
builds a real attribution + commission ledger:
  1. Every routed lead creates a nadlan_referral CPT record with a unique
     tracking token (rTOKEN), partner, customer-redacted contact, agreed %.
  2. Partner gets a one-click "accept terms" link - clicking it logs a
     timestamp + IP = a contract record we can show in a payment dispute.
  3. **The customer (not the partner) confirms status** via a tokenised public
     page /referral-status/<token>/ pinged automatically at 14/30/60 days. The
     partner has every reason to lie; the customer has no reason. That's the
     lock-in.
  4. A commission ledger logs amount owed and paid. The owner sees the total
     open balance in the admin dashboard.
Honest scope: software cannot FORCE a partner to pay. What this does:
  - creates a clean paper trail (proof of intro + customer-confirmed close)
  - makes non-payment visible and uncomfortable
  - makes the owner the indispensable middle (relationship + brand stays here)
  - a
... (truncated)
```
REST: `nadlan/v1/referral/route`, `nadlan/v1/referral/(?P<token>[a-z0-9]+)/accept`, `nadlan/v1/referral/(?P<token>[a-z0-9]+)/status`

### lead-nurture.php
```
nadlan-config - Chunk D automated lead nurture (v1.54.0).
Ships dark behind nadlan_feature_lead_nurture. The flow starts only after
Chunk B lead E2E capture and reuses Chunk C score/handoff data when present.
```
REST: `nadlan/v1/nurture/unsubscribe`

### lead-routing.php
```
nadlan-config - Lead routing to paid card owners (v1.42.9).
Routes a captured nadlan_lead to the owner of the exact card that received
the inquiry, only when that card is on a paid tier. Admin notification remains
the fallback path for free, unclaimed, invalid, or owner-unavailable cards.
```

### listings-ux.php
```
nadlan-config - Listings engagement & conversion UX (v1.6.0)
Best-in-class listing-page mechanics (Redfin/Zillow-grade), low-cost/no-API:
  - Similar listings (SQL on city + rooms±1 + price±15% + listing_type)
  - Favorites (REST for logged-in users; localStorage fallback handled client-side)
  - View counter + Days-on-Market badge (Redfin social-proof signal)
  - Mortgage / משכנתא calculator (client-side, ₪)  [nadlan_mortgage]
  - Schedule-viewing / WhatsApp contact CTA (reuses the /nadlan/v1/lead endpoint)
Roadmap (NOT here - see docs/listings-questions.md §D): AVM + deal-history,
neighborhood panel, saved-search email alerts, school/planning overlays.
```
REST: `nadlan/v1/favorite`
Shortcodes: `[nadlan_mortgage]`

### loi-form.php
```
NadLan Non-Binding Offer Letter (LOI) form.
The buyer-journey "buying moment": a buyer submits a non-binding purchase
offer on a project/unit. Origin: Codex's buyer-journey branch
(codex/buyer-journey-fixes-2026-07-01). This is the cleaned, review-passed
version -- Codex's original handler returned a fake success and saved NOTHING
("In a real implementation, this would save..."), which would silently drop
every real offer. This version actually persists the offer through the
existing lead pipeline (nadlan_lead_e2e_capture -> nadlan_lead CPT + routing),
with a direct-insert fallback so an offer is NEVER lost. Styling retokened to
the luxury design system (gold #9C7A3C, radius 2px, hairlines).
Shortcode: [nadlan_loi_form project_id="123" unit_id="unit-38"]
```
Shortcodes: `[nadlan_loi_form]`

### map.php
```
nadlan-config - Leaflet archive map with clustering (v1.12.0)
Madlan/Yad2-style map on the properties archive + city hubs. Uses Leaflet
(no API key, OSM tiles) + leaflet.markercluster (CDN). RTL-aware. Renders
via a [nadlan_map] shortcode AND auto-appends to /properties/ archive.
Data via REST GET /nadlan/v1/map?city=&listing_type= - returns only
lat/lng/title/price/url for the bounding-box. Limit 500 per request to
keep payload small. No PII.
```
REST: `nadlan/v1/map`
Shortcodes: `[nadlan_map]`

### media.php
```
nadlan-config - Rich media: 3D tour / video / floorplan (v1.10.0)
2026 reality (research): Matterport DROPPED by Zillow in Oct 2025 after the
CoStar acquisition; KUULA is the recommended free/affordable 3D tour platform
(Zillow-approved provider). We support Kuula iframe (JS-style for iOS+perf),
generic any-iframe (YouTube/Vimeo/CloudPano/Panoee), and a floorplan image/PDF.
Adds three meta fields to nadlan_property (REST-exposed) - they were declared
in catalog-meta's parent module sparsely; here we ensure tour_url, video_url,
floorplan_url are registered + render a tabbed media block on single views.
```

### milestone-notify.php
```
nadlan-config - MILESTONE CHANGE NOTIFICATIONS (2026-07-07).
The other half of the Lennar/Buildertrend retention pattern: when a
project's reported stage ADVANCES (project_status meta change that maps to
a later lifecycle stage), every buyer who inquired about that project gets
a short honest update with a link back to the project page.
OWNER LAW - emails/deliverability LAST: sending is OFF until
`nadlan_milestone_notify_enabled` is '1'. Until then the module only
RECORDS the pending notifications (option queue, capped) so nothing is
lost and the owner can flip the switch after SMTP work. Admin preview:
  GET /nadlan/v1/milestone-notify-queue   (manage_options)
```
REST: `nadlan/v1/milestone-notify-queue`

### milestones.php
```
nadlan-config - PROJECT MILESTONE TRACKER (2026-07-07, world-scan cycle).
The Amazon/Lennar/Buildertrend pattern Israeli buyers never get: where the
project stands on the road from planning to keys. Rendered ONLY from real
data - the project's own project_status meta (already curated in the CMS)
mapped onto the canonical Israeli lifecycle. No status = no band (collapse
law). Language siblings (slug-en/-fr/-ru/-ar) inherit the base project's
status so the ladder is never duplicated by hand.
 Stages: תכנון -> היתר בנייה -> שיווק ומכירות -> בנייה -> טופס 4 ומסירה
Token order matters: 'בהיתר בנייה' must match permit before construction.
```

### nearby-poi.php
```
nadlan-config - Nearby POI (schools/transit/amenities) via OpenStreetMap Overpass (v1.11.0)
Realtor.com/Rightmove-parity "what's nearby" tab. Free data (no API key) via
Overpass API; 10k req/day/IP rate limit so we aggressively cache (24h transient
per coords+radius bucket). Designed to fail silent - if Overpass is down or
times out, the panel just hides.
Categories shown: schools (amenity=school), kindergarten, supermarket,
pharmacy, transit (bus_stop+railway_station+subway). 1km radius.
```

### offers.php
```
nadlan-config - "הצעות מחיר" phase 1: non-binding offer collection on listings.
NOT a binding auction. Flat-fee monetization only (legal spec:
docs/2026-06-11-offers-feature-spec-cited.md). Dark behind nadlan_feature_offers.
```
REST: `nadlan/v1/offers`, `nadlan/v1/offers/leading/(?P<card>\d+)`

### og-image.php
```
nadlan-config - Dynamic OG image for social sharing (v1.40.0 / shark #16)
When someone shares a profile/term/article on WhatsApp/Twitter/FB, the
preview card shows an image. We don't have hand-made images for 2,700
contractors, so we generate SVG previews on the fly - branded cards that
look professional + carry the title.
Endpoint: GET /nadlan/v1/og/<post_id>.svg
Sets og:image / twitter:image to that URL on profile + term + project pages.
Why SVG (not PNG): zero dependencies (no Imagick/GD heavy work), browsers
render fine, social-card scrapers handle SVG. Lightning fast.
```
REST: `nadlan/v1/og/(?P<id>\d+)\.svg`

### ops-dashboard.php
```
nadlan-config - Operations dashboard (v1.13.0)
One admin page that surfaces ALL the moving parts at a glance:
leads (with drip-state breakdown), claims (pending/approved), auctions (live/
extended/sold), imports (cursor + counts), AVM cache size, deals count,
directory health, plugin version. Designed so the owner can manage the
whole system without hunting through 7 menus.
NEW capability flag: 'manage_options' required. No data is exposed publicly.
```

### owner-config-rest.php
```
nadlan-config - Owner-config REST + preferred-partners auto-route (v1.40.1)
Two things at once:
 A) Expose `nadlan_owner_whatsapp` and `nadlan_preferred_partners` for REST
    writes by authenticated admins (app password OK). Auth: manage_options.
    This lets any agent (Claude/Codex/Cowork) set/seed these without
    navigating WP-admin. The admin pages still own the UI; this is just
    the API surface.
 B) Close the v1.40.0 gap: actually USE the preferred-partners list when a
    lead is routed through the Lead Ledger without a partner_id, OR when
    the lead is generic (concierge / sticky CTA). The picker
    `nadlan_pp_pick()` already exists; this wires it in.
Safety: still NEVER cold-emails the 2,700 imported contractors. Only people
listed under `nadlan_preferred_partners` ever receive routed leads.
```
REST: `nadlan/v1/owner/whatsapp`, `nadlan/v1/owner/partners`

### placement-auction.php
```
nadlan-config - GAP 7 placement auction for scarce featured slots.
```
REST: `nadlan/v1/auction/bid`

### preferred-partners.php
```
nadlan-config - Preferred Partners (v1.40.0 / shark #7)
Safe auto-routing: the owner defines a small set of APPROVED partner emails
(the actual people you have a deal with), organised by profession + optional
city. The Lead Ledger consults this list when a routed lead is created with
a topic that doesn't match a partner_id (e.g. the AI concierge or sticky CTA
routes "מצא לי יועץ משכנתאות באזור גוש דן") and picks the right partner.
This is the FAT MONEY door: ₪3k-8k per closed mortgage / RE deal, captured
automatically once you've added even one real partner to the list. Without
this, every fat lead requires you to manually pick a partner.
Spam-safe: only emails on this list get routed. The 2,700 imported cold
contractors are NEVER contacted from here.
Stored as one option: nadlan_preferred_partners (JSON array). Admin page
under "💰 Lead Inbox" → "שותפים מועדפים".
```

### premium-catalog.php
```
nadlan-config - Premium project catalog (v1.71.6)
[nadlan_premium_catalog]: the curated tier. Only projects that pass the full
experience gate appear here: complete article in 5 languages, selectable 3D,
facade, verified facts. Booking-style filters (facilities, rooms, delivery,
near sea) + recent-deals line per card + language links. This is both the
flagship UX and a monetization product (developers pay to be in the premium
tier). The big /projects/ catalog (900+) stays as the wide SEO net.
JS prints in wp_footer (content filters corrupt inline scripts). No long dashes.
```
Shortcodes: `[nadlan_premium_catalog]`

### premium-ui.php
```
nadlan-config - Site-wide premium UI overlay (v1.42.0)
One module that lifts the catalog/profile/micro-UI from "default WP directory" to
an editorial real-estate experience without rewriting directory.php / cards-render.php.
Ships:
  1. An inline SVG sprite (profession marks + small UI icons) injected once in
     wp_footer, so existing card markup can do <svg><use href="#profession-..."/></svg>.
  2. A high-priority CSS layer that:
       - retunes palette + typography to the ink/charcoal/champagne system
       - replaces the bright pill avatars with calm monogram-style marks
       - upgrades buttons, chips, sponsored slots, FAB, profile shell
       - fixes mobile data-tables (article tables forcing 400-677px layout at 390px)
       - enforces 44px tap targets for header/footer/glossary/nav
       - re-anchors the floating CTA to the visual viewport (safe-area)
Boundary: this module ONLY adds CSS + sprite + a small profile-shell decorator. It
does NOT touch routes, REST, lead pipes, billing, schema, or any business logic.
```

### pricing-schema.php
```
nadlan-config - Pricing page schema + meta (v1.40.0 / shark #10)
Adds Product + Offer JSON-LD on /join-pro/ so Google's rich results show
the price + "free trial" + ratings (once we have any). Also sets a clean
Yoast-friendly meta title/description. Pure SEO play: rich snippets get
+20-35% CTR vs. plain results.
```

### pro-cards.php
```
nadlan-config - PRO CARDS on content (owner 2026-07-07: "this is the business
behind all this").
Every practice-area content page (encyclopedia term, guide, article) floats
the professionals who own that niche: a rich card woven INTO the reading
flow (after the second heading - the point where a reader who kept going is
genuinely interested), plus an experts row at the end when more than one
matches. Mobile-first: the card is a full-width native block, never a
floating element fighting the WhatsApp cluster.
MATCHING (three layers, most specific wins):
 1) PINNED: `procard_pros` meta on the content (comma-separated professional
    IDs) - full manual control per page.
 2) DOMAIN MAP: content signals (glossary enc_domain / nadlan_term_cat slugs /
    post category slugs + names) -> profession keys, via the editable option
    `nadlan_procard_map` merged over honest defaults.
 3) Nothing matches -> nothing renders. No filler.
ORDERING = THE MONETIZATION: premier > pro > free (then rating, then newer).
Paid cards carry an honest "ממומן" chip; seeded ratings keep the
"נתוני דוגמה" badge law from the directory. Caps: nadlan_procard_max (2
inline; the end row shows up to 6). Kill switch: 
... (truncated)
```

### pro-stats-email.php
```
nadlan-config - MONTHLY PRO STATS EMAIL (retention moat, built 2026-07-07).
Advertisers who see their numbers renew. Once a month every claimed,
published professional card's owner gets a short honest report: profile
views, leads, content impressions (procard_impressions - renders inside
encyclopedia/guide pages), and sponsorship status with a renewal path.
OWNER LAW - emails/deliverability come LAST: sending is OFF until the
option `nadlan_pro_stats_email_enabled` is set to '1'. Until then the
module only exposes an admin-gated PREVIEW endpoint so the email can be
verified without a single message leaving the site:
  GET /nadlan/v1/pro-stats-preview?card=<id>   (manage_options)
```
REST: `nadlan/v1/pro-stats-preview`

### professional-profile.php
```
nadlan-config - World-class professional profile layer (v1.69.82)
Owner directive 2026-07-02: single professional pages were "very basic".
This module adds a Zillow-agent/Houzz-class rich profile on top of the
existing directory (2,711 gov.il-verified records, ratings, tiers, claim):
  1. Profile hero: brand monogram portrait (parametric SVG - elegant, honest,
     no fake photos), name, profession pill, city, gov.il verified badge,
     rating, years/projects stats, tier-aware contact CTAs.
  2. Expertise band: specialties + languages chips, service areas.
  3. WIRED TO EVERYTHING: their projects (developer/contractor name match),
     colleagues nearby (same profession/city), profession-matched guides,
     calculators - hub-spoke in both directions.
  4. Extends the profession taxonomy: designers, engineers, accountants,
     surveyors, property managers, urban planners (the "go for all" ask).
  5. Demo premium profiles supported: is_demo flag → visible "לדוגמה" tag +
     noindex (same honest pattern as demo listings).
```

### profile-extras.php
```
nadlan-config - Public profile extras (v1.41.0)
Renders the new studio fields (social icons + video embed) on single
professional/project/property pages, just below the body content.
Photos already render via cards-render.php's gallery (reads photos_csv).
```

### project-experience.php
```
nadlan-config - Project buying experience layer (v1.69.85)
Owner mobile-QA 2026-07-01: projects felt stacked, un-unified, apartment
selection didn't work, map wasn't clickable, article buried. This module
adds a REPLICABLE experience layer to EVERY nadlan_project page:
  1. Sticky section nav (סיור ובחירת דירה / סביבה / עוד מידע)
  2. Apartment selection lives in the showroom engine only (design audit
     2026-07-02, D1/D2): this module must never render a second picker or
     standalone interior widget next to the engine.
  3. Live clickable surroundings map: streets/satellite, real OSM POIs
     (schools/kindergartens/transit/shops/health) AND a FUTURE-PLANS layer -
     nearby urban-renewal projects from our own 965-project gov.il dataset,
     each marker clickable to its project page (spoke wiring).
  4. "The world around the project" grid: contractor, professionals, city,
     calculators, guides, glossary - hub-spoke links.
  5. Compact factual SEO intro from real meta (no invented content).
```
REST: `nadlan/v1/comps`

### project-preview.php
```
Project-page PREVIEW (2026-07-03) - proves the new modular project-page
design runs inside WordPress, not just as a standalone HTML file.
A REST route serves the complete self-contained design (from
assets/preview/<slug>.html) with the Mapbox token injected from the keys hub
and the 3D model pointed at the plugin asset. A shortcode embeds it in an
isolated iframe so no theme CSS can collide with it.
Usage: create a page and add  [nadlan_project_preview slug="duo"]
Preview URL (direct):  /wp-json/nadlan/v1/preview/duo
```
REST: `nadlan/v1/preview/(?P<slug>[a-z0-9\-]+)`
Shortcodes: `[nadlan_project_preview]`

### property-showroom.php
```
nadlan-config - Property showroom layer (v1.69.70)
The differentiator block on single nadlan_property pages, on top of the
existing stack (cards-render facts/gallery, listings-ux similar/favorites/
mortgage, nearby-poi real schools/transit via OSM, avm-deals, media tabs,
schema JSON-LD):
  1. Key-facts hero strip (price, rooms, floor, sqm, ₪/sqm, listing type)
  2. Sketch-first SELECTABLE FACADE - parametric SVG building generated from
     total_floors / floor / units_per_floor / unit_position meta; the listed
     apartment is highlighted; hover/click floors; toggle to a parametric
     schematic floor plan (rooms/mamad/balcony) - the "inside view".
  3. Monthly costs panel (arnona + vaad bayit + mortgage estimate).
  4. Single-listing Leaflet map (OSM tiles, no key) with the asset marker.
  5. Honest "לדוגמה" badge on is_demo listings.
Registers the extra Israeli listing meta Yad2/Madlan-parity requires:
arnona_monthly, vaad_bayit_monthly, entry_date, condition, storage,
renovated_year, direction, units_per_floor, unit_position.
```

### property-wizard.php
```
nadlan-config - Free listing wizard with AI assist (v1.69.70)
Front-end, PRACTICAL (not a mock) listing-creation flow, Zillow-FSBO-style:
  [nadlan_listing_wizard] shortcode →
  Step 1  free-text description ("ספרו על הנכס") → AI (existing nadlan_llm_request
          adapter) extracts structured fields as strict JSON
  Step 2  review/edit every field (pre-filled by the AI)
  Step 3  photos (REAL upload via wp_handle_upload, logged-in only) + video URL
  Step 4  submit → pending nadlan_property owned by the user → moderation
Free listings. Login required (spam + ownership). AI endpoint rate-limited.
All input sanitized against a strict whitelist. No caps bypass: submit inserts
as pending; publishing stays an editor action.
```
REST: `nadlan/v1/listing-ai-draft`, `nadlan/v1/listing-photo`, `nadlan/v1/listing-submit`
Shortcodes: `[nadlan_listing_wizard]`

### related-content.php
```
nadlan-config - RELATED CONTENT FLOATS + PRO DOSSIER (2026-07-11).
The anti-thin-content layer (owner order): float genuinely related site
content - glossary terms, guides/news, calculators - into the two thinnest
surfaces (listings, professional profiles), the way pro-cards.php floats
sponsored professionals into articles. One restrained band, token-matched,
cached, collapses when there is nothing honest to show.
Plus the real thin-fix for profiles: an AI-written DOSSIER (domain explainer
for the profession - what they do in a deal, how to choose one, FAQ). The
writer is an admin-gated REST batch (runs ONLY on owner trigger, uses the
ai-brain judge/refine pipeline); the renderer ships now and shows the meta
when present. Honesty law: general domain content only - the prompt forbids
inventing facts about the specific person.
Kill switch: option nadlan_relcontent_enabled ('1' default).
```
REST: `nadlan/v1/prof-dossier-generate`

### renewals.php
```
nadlan-config - Tier renewals (month 2 and onward), owner core-business ask
2026-07-06.
The gap: paid tiers (advertiser-orders.php) activate for N days and then
silently drop to free - no renewal path, month-2 revenue was manual.
The machine (competitor-standard shape, sized to what we run today):
 - 3 days before a paid tier expires, a RENEWAL ORDER for the same product
   and the same card is created automatically and the customer receives the
   standard WooCommerce invoice email with a one-click pay link
   (order-pay page -> Morning credit card / Bit / Google Pay).
 - Payment flows through the existing woocommerce_payment_complete hook,
   which extends campaign_end from the current end (stacking is already
   built into nadlan_ao_apply_order_item) - zero double logic here.
 - Unpaid renewals: the existing downgrade cron drops the tier at expiry
   exactly as before; the pending order stays payable for 7 more days
   (late payment re-activates from the payment date), then auto-cancels.
Upgrade path (documented in AGENT-LOG): WooCommerce Subscriptions + the
Morning gateway's native token support makes month-2 charges automatic
with no email step. This module is forward-compatib
... (truncated)
```

### rentals-manager.php
```
nadlan-config - RENTAL MANAGEMENT for private landlords (v1, 2026-07-12).
The Israeli small-landlord product nobody offers free + self-serve:
every rented apartment managed FROM THE 3D BUILDING on a portfolio map.
Flow (owner order): /my-rentals/ dashboard opens with the PORTFOLIO MAP
on top; click a building pin -> its 3D model loads; click your apartment
on the model -> the management panel: tenancy, rent ledger, deadline
chips (contract end, option, the Jan-30 tax date), documents checklist,
maintenance log, real actions (WhatsApp reminder to the tenant, find a
professional, list the apartment).
HONEST SCOPE v1: tracking + reminders + documents. NO payment
processing, NO tenant screening (rent moves by checks/bank transfer in
Israel - we track it, we do not move it). Tax figures are reminders
only, always "verify with רשות המסים".
PRIVACY: CPT nadlan_rentalprop is public=false, no rewrite, no REST
show. Owner-only access (member invites = later). The ONLY public read
is GET /rental-demo serving the is_demo portfolio for the landing.
MONETIZATION INFRA: free now; each property carries rm_plan meta
(default 'free') so paid tiers can gate features later without schema
change. Featu
... (truncated)
```
REST: `nadlan/v1/rental-demo`, `nadlan/v1/rental-prop`, `nadlan/v1/rental-props`, `nadlan/v1/rental-prop/(?P<id>\d+)`, `nadlan/v1/rental-prop/(?P<id>\d+)/units`, `nadlan/v1/rental-demo-seed`

### reviews.php
```
nadlan-config - REAL reviews engine (v1.33.0)
State-of-the-art reviews for nadlan_professional + nadlan_project:
 - submission via REST with email gate (anti-spam honeypot + nonce + rate limit)
 - moderation: review CPT stored as 'pending'; admin approves → 'publish'
 - rating + reviews_count meta is recomputed on approval/un-approval
 - schema.org Review + AggregateRating JSON-LD on the target page (SEO juice)
 - public render block (stars summary + recent reviews list + submit form)
 - shortcode [nadlan_reviews id=…] + auto-appended on professional/project singles
 - admin email notification on every submission so the owner is in the loop
```
REST: `nadlan/v1/review-submit`
Shortcodes: `[nadlan_reviews]`

### rfp.php
```
nadlan-config - RFP document (buy-flow phase 2, research spec 2026-07-05)
The buy-flow posts a structured request; this module turns it into a real,
shareable, printable RFP document the buyer can open immediately and the
owner can forward to the developer and advisors.
 - POST /nadlan/v1/rfp        create the document (called by buyflow.js right
                              after the lead is accepted); returns {url}
 - GET  /nadlan/v1/rfp/<token> the rendered document (unguessable token)
HONESTY LAWS: unit facts are re-read SERVER-SIDE from the project post (the
client payload only points at project slug + unit id); every money-shaped
line is estimate-labeled; advisors listed are real directory entries matched
by profession; the status timeline claims only what actually happened.
```
REST: `nadlan/v1/rfp`, `nadlan/v1/rfp/(?P<token>[a-zA-Z0-9]{16,32})`

### roles.php
```
nadlan-config - GAP 6 roles and listing capabilities.
```

### saved-search.php
```
nadlan-config - Saved searches + email alerts (v1.8.0)
Zillow/Redfin-grade proactive alerts (no external API). A visitor saves a search
(city / rooms / price / type); we double-opt-in their email, then a daily cron
matches NEW listings against each confirmed search and emails the matches.
Store: private CPT nadlan_saved_search (meta: email, user_id, params JSON,
confirmed, token, last_run). Double opt-in = anti-spam + consent hygiene.
BLANK (owner): alert frequency default = daily; web-push + WhatsApp alerts are
roadmap (docs/listings-questions.md §D). Branded email template = TODO.
```
REST: `nadlan/v1/saved-search`, `nadlan/v1/saved-search/confirm`
Shortcodes: `[nadlan_save_search]`

### schema.php
```
nadlan-config - Card schema + SEO guards (v1.5.0)
1) JSON-LD per card type (LocalBusiness/GeneralContractor, Residence/
   ApartmentComplex, RealEstateListing) - stats-rich, machine-readable, which
   is what AI answer-engines and Google reward.
2) THIN-CONTENT NOINDEX guard: any card still at data_quality=stub (or with a
   body below the word floor) is noindex,follow. This is the anti-cannibalization
   + anti-thin-content safeguard from the research - stubs don't compete with
   keyword pages and don't dilute crawl budget. Once enriched (original ChatGPT
   prose pushed via import-enrich), the card becomes indexable.
```

### showroom-engine.php
```
nadlan-config - Showroom Engine bridge (Claude Design port).
Mounts the data-driven showroom engine (assets/showroom-engine/) via a
project-agnostic shortcode. The engine renders ANY project from a payload built
from that project's CMS meta - the factory. New project = new nadlan_project post
with its meta filled, zero code.
  [nadlan_showroom_engine]                     -> the current nadlan_project page,
                                                   or the newest project as fallback
  [nadlan_showroom_engine id="123"]            -> a specific project by post id
  [nadlan_showroom_engine project="rainbow"]   -> a specific project by slug
  [nadlan_showroom_engine page="home"]         -> gallery of all published projects
No stacking: renders the new engine only where the shortcode is placed; it never
touches the existing project-3d showroom.
```
Shortcodes: `[nadlan_showroom_engine]`

### showroom-metabox.php
```
Showroom control panel (meta box) for nadlan_project.
Solves the owner's #1 pain: to configure a project's showroom you previously
had to open "Custom Fields", remember secret meta keys (nlp3d_use_engine, lat,
lng, project_model_glb, project_model_poster) and type raw values. This adds a
normal, labelled settings panel on the Project edit screen -- a checkbox and a
few text fields, no code. It writes the SAME meta keys the engine already reads
(see showroom-engine.php), so it just makes the existing wiring editable.
Concept from Antigravity's buyer-journey work (2026-07-01); implemented cleanly
into the repo here with nonce + capability + sanitization.
```

### showroom-support.php
```
Showroom support - the living remains of project-3d.php (retired v1.70.1).
The OLD showroom renderer is gone (the new showroom-engine renders every
project). What survives here is everything the NEW engine and the authoring
flow still depend on:
 1. the script_loader_tag filter that loads model-viewer as an ES module;
 2. register_post_meta for all project_3d_* showroom fields (REST exposure
    engine.js relies on) with their sanitizers;
 3. the admin metabox - the only authoring UI for units/facade/environment/
    price meta - and its save handler;
 4. the /nadlan/v1/project-showroom/<id> payload API (agent tooling).
Also: no-op tombstones for shortcodes whose providers were deleted
(orchestrator plugin, legacy homepage module) so no raw shortcode text can
ever leak into a rendered page from stale templates or content.
```
REST: `nadlan/v1/project-showroom/(?P<id>\d+)`

### sitemap-ping.php
```
nadlan-config - Sitemap ping on content change (v1.40.0 / shark #13)
When meaningful content changes (a glossary term is enriched, a new
professional is verified, a new project is enriched), ping the Yoast sitemap
and warm the Google index. Free SEO speed-up - pages get crawled days faster
than they would by default.
Throttle: max 1 ping per hour total (Google rate-limits anyway).
```

### social-proof.php
```
nadlan-config - Social proof + "what's hot" widget (v1.40.0 / shark #14)
Three trust signals appended to the homepage that convert undecided visitors:
 1. Live counters: "X בעלי מקצוע · Y פרויקטים · Z מונחים" (already in DB).
 2. "Just claimed" feed: the last 3 contractors who claimed their card -
    creates urgency for other contractors viewing the site ("they're moving").
 3. "What's popular this week" - top-viewed professionals (uses a simple
    post_meta view counter the directory cards stamp on click).
Pure conversion psychology: numbers that grow + names that just acted are
the strongest social-proof on directory sites (Houzz, Thumbtack pattern).
Shortcode: [nadlan_social_proof] for placement anywhere.
```
Shortcodes: `[nadlan_social_proof]`

### sponsored-spot.php
```
nadlan-config - Sponsored-spot CTA on directory (v1.41.1 - REWRITTEN, ob-free)
⚠️ v1.40.0 BUG FIXED HERE: the old version used ob_start() on template_redirect
and called nadlan_ss_card() (which itself used ob_start/ob_get_clean) from
inside that output-buffer handler. PHP forbids nested output buffering inside
an ob handler → FATAL → blank page. This blanked BOTH /professionals/ and
/projects/ (everything rendered by directory.php) from v1.40.0 to v1.41.0.
New approach - zero output buffering:
  • nadlan_ss_card() builds a plain string (no ob_start).
  • Server-side injection via the `nadlan_dir_cards_html` filter that
    directory.php applies to its rendered cards (added v1.41.1). We insert a
    sponsored card after the 6th real card.
  • AJAX load-more injection via rest_post_dispatch (unchanged logic, now uses
    the ob-free card).
```

### studio-rest.php
```
nadlan-config - Advertiser STUDIO REST (v1.41.0)
Backend for the self-serve advertiser studio. Five endpoints:
  POST   /nadlan/v1/studio/<id>/save           - update fields + meta (owned cards)
  POST   /nadlan/v1/studio/<id>/upload         - drag-drop image upload
  POST   /nadlan/v1/studio/<id>/gallery/reorder - reorder photos
  POST   /nadlan/v1/studio/<id>/gallery/delete  - remove a photo
  POST   /nadlan/v1/studio/<id>/ai-copy         - AI copy assist (uses concierge if configured)
Auth: caller must be logged-in (app password OK) and pass edit_post for the
card. Ownership still lives in owner_user_id + claim_status and is mapped by
map_meta_cap, so owners can edit only their own listings.
The 2,700 imported cold contractors are unaffected - only claimed cards have
an owner; only those can be edited.
```
REST: `nadlan/v1/studio/(?P<id>\d+)/save`, `nadlan/v1/studio/(?P<id>\d+)/upload`, `nadlan/v1/studio/(?P<id>\d+)/gallery/reorder`, `nadlan/v1/studio/(?P<id>\d+)/gallery/delete`, `nadlan/v1/studio/(?P<id>\d+)/ai-copy`, `nadlan/v1/studio/(?P<id>\d+)`, `nadlan/v1/studio/mine`, `nadlan/v1/studio/create`

### studio.php
```
nadlan-config - Advertiser STUDIO frontend (v1.41.0)
One self-serve URL - /studio/?id=<post_id> - that an advertiser opens to
fully manage their published card with NO admin/wp-login knowledge:
  • drag-and-drop image upload (or click), gallery reorder/delete
  • inline edit: title, description (with AI "improve this" assist),
    city/address, phone/email/website, social links (FB/IG/TT/YT),
    video URL embed (YouTube/Vimeo)
  • Leaflet + OpenStreetMap map picker (zero cost, no Google key)
  • Type-specific fields (project: units/status/יזם; pro: classification;
    property: price/rooms/sqm)
  • One-click "preview live page"
  • Tooltips on every field - explanations so a non-techie understands
The page is intercepted at `/studio/` via template_redirect. Auth is mandatory:
caller must be logged in AND own the card (or be admin) - enforced by REST.
4-year-old friendly: empty-states say what to do; success toasts on every
action; nothing is hidden behind jargon; every input has a "?" tooltip.
```

### term-faq-schema.php
```
nadlan-config - Auto FAQ schema + breadcrumbs on glossary terms (v1.40.0 / shark #15)
Each term page has 3 H2 sections (הגדרה / מה זה אומר בפועל / טעות נפוצה).
Emit FAQPage JSON-LD so Google can show the term as a rich result with the
Q&A expanders directly in SERP - massive CTR uplift, free.
Also emits BreadcrumbList schema (home → glossary → term).
```

### tiers.php
```
nadlan-config - Card tiers / paywall + free-trial gating (v1.16.0)
Closes the "free listings give away links + contacts" leak per owner brief
(2026-06-01). The rulebook §10 specifies Free/Pro/Premier tiers; v1.5.0 had no
tier - every verified claim got full edit + public contact. This module adds:
 1) `paid_tier` meta on every card: 'free' | 'pro' | 'premier' (default 'free').
 2) Free-trial timer: when admin approves a claim, `trial_started` stamps now;
    after NADLAN_FREE_TRIAL_DAYS (default 30) the card downgrades automatically.
 3) Visibility helpers strip PHONE, EMAIL, WEBSITE, PHOTOS, OUTBOUND LINKS from
    the public card render unless the card is `pro`/`premier` (or in trial).
 4) Free-tier card stays INDEXABLE (the SEO inventory we want) but the value
    surfaces (contact + photos + leads) are gated.
 5) Admin meta box per card to set tier + trial expiry. Healthcheck reports
    free/pro/premier counts.
Rulebook §10 alignment: matches the "Free/Pro/Premier (מיקום, בלעדיות אזור,
תג מאומת)" plan. Premier adds priority sort in hubs/archives (built here).
BLANK: actual checkout for upgrade is out of scope for this commit - the
upgrade button on the card opens a lead-captur
... (truncated)
```

### urban-hub.php
```
nadlan-config - URBAN RENEWAL HUB glue (L1, 2026-07-11).
The /urban-renewal/ pillar and its spokes are CMS pages (edited via REST,
like every guide). This module ships only what pages cannot:
 1. GET /nadlan/v1/renewal-lookup - public compound lookup over the ~938
    gov.il urban-renewal compounds already imported as nadlan_project stubs
    (source=urban_renewal meta, import.php). Rate limited 30/hr/IP.
 2. [nadlan_ur_lookup] - the "is my building in a declared compound?"
    teaser embedded on the pillar. Works logged-out, honest miss copy.
 3. nadlan_ur_interlinks() - the hub URL map used by the spoke grid.
Prefix law: inc/renewals.php is the BILLING module - everything urban
renewal uses urban-* files and nadlan_ur_/nlur prefixes.
```
REST: `nadlan/v1/renewal-lookup`
Shortcodes: `[nadlan_ur_lookup]`

### urban-map.php
```
nadlan-config - URBAN RENEWAL MAP + advisor wiring (L5, 2026-07-12).
1. Adds the renewal advisor kinds to the RFP matcher (filter added in
   rfp.php): shamai / mefakeach / organizer, so the wizard and the
   project space can request quotes from the real directory.
2. /urban-renewal/map/: city-cluster map over the ~938 imported gov.il
   compounds. HONEST V1: the import carries no lat/lng, so the map shows
   CITY AGGREGATES with counts by track (never fake per-building pins);
   per-compound pins arrive after a geocoding enrichment pass.
Feature gate: option nadlan_feature_renewal_map ('1' = on).
```
REST: `nadlan/v1/renewal-map-data`
Shortcodes: `[nadlan_ur_map]`

### urban-space.php
```
nadlan-config - URBAN RENEWAL PROJECT SPACE (L4 2026-07-12, PRODUCT v2 2026-07-12).
The building's project room: per-apartment consent tracked and painted on
the 3D standard model, the 10-stage bureaucratic ladder, an updates feed
(send-gated, deliverability-last), invite-by-token membership, and the
/my-renewal/ surface. Documents live in urban-docs.php.
PRODUCT v2 (owner order): /my-renewal/ is no longer a login wall.
Anonymous visitors get a real, INDEXABLE product landing (HE + EN via
?lang=en) with a live read-only demo of the finished demo project -
3D model full width ON TOP, interactive progress stepper attached under
it, a live map, an auto to-do list and a documents rollup - plus
"start here" steps and Create/Estimate CTAs. Members get the same v2
layout with editing. The app JS lives in assets/urban/renewal-space.js.
PRIVACY BY CONSTRUCTION: CPT nadlan_renewal is public=false, no rewrite,
no REST show - there is NO front-end URL to index. All access flows
through the dashboard route + membership-checked REST. The ONLY public
read is GET /renewal-demo, which serves exclusively the is_demo space.
Feature gate: option nadlan_feature_renewal_space ('1' = on).
```
REST: `nadlan/v1/renewal-demo`, `nadlan/v1/renewal-space`, `nadlan/v1/renewal-space/(?P<id>\d+)`, `nadlan/v1/renewal-space/(?P<id>\d+)/apartments`, `nadlan/v1/renewal-space/(?P<id>\d+)/stage`, `nadlan/v1/renewal-space/(?P<id>\d+)/update`, `nadlan/v1/renewal-space/(?P<id>\d+)/invite`, `nadlan/v1/renewal-join/(?P<token>[A-Za-z0-9]{24})`, `nadlan/v1/renewal-notify-queue`

### urban-tools.php
```
nadlan-config - URBAN RENEWAL TOOLS (L2, 2026-07-11).
Pillar-embedded decision tools, calculators.php discipline: client-side
widgets, filterable legal constants WITH effective dates + a gov.il verify
link, YMYL disclaimers on every output, no em/en dashes.
 [nadlan_ur_consent_calc]  apartments + consents -> live % vs the three
                           legal thresholds, what unlocks at each
 [nadlan_ur_expectations]  honest non-binding "what owners usually get"
 [nadlan_ur_timeline]      the 10-stage strip (labels shared with L4)
```
Shortcodes: `[nadlan_ur_consent_calc]`, `[nadlan_ur_expectations]`, `[nadlan_ur_timeline]`

### urban-wizard.php
```
nadlan-config - URBAN RENEWAL WIZARD "בדיקת התחדשות לבניין שלי" (L3, 2026-07-11).
Flow: address/city -> declared-compound lookup (urban-hub endpoint) ->
building details -> optional PRIVATE doc upload + paste-text ->
AI first advisory (server-appended disclaimer, cost-guarded) ->
instant 3D of THEIR building (standard model, one badge per floor) ->
CTAs. Logged-out visitors get the funnel quick-register gate.
PDF LAW (decision 2026-07-11): v1 analysis reads PASTED TEXT only - most
consent-stage docs are phone scans a text parser cannot read, and honest
labels beat a fake "we read your file". Files are still stored (private,
random names) for the future project space.
Feature gate: option nadlan_feature_renewal_wizard ('1' = on). The AI
endpoint is additionally guarded by provider availability + cost caps.
```
REST: `nadlan/v1/renewal-doc`, `nadlan/v1/renewal-advise`
Shortcodes: `[nadlan_renewal_wizard]`

### wa-source.php
```
nadlan-config - WHATSAPP SOURCE TRACKING (owner order 2026-07-12).
Problem: WhatsApp inquiries arrive with no clue which page the visitor
came from - the owner cannot read intent or see which pages convert.
The wa.me deep link carries context only through its `text` parameter,
so we stamp it there.
ONE site-wide interceptor (covers plugin CTAs, theme buttons, everything):
on click of any wa.me link that targets a PHONE NUMBER (wa.me/9725... =
a message to the business), append a source line with the page title +
URL to the prefilled text. Share-to-a-friend links (wa.me/?text=..., no
number) are left untouched - stamping those would spam users' friends.
The stamp is applied at click time so SPAs/tabs always carry the CURRENT
page, and it is idempotent (never doubles).
```

### whatsapp-lead-ingestion.php
```
nadlan-config - WhatsApp-to-lead ingestion bridge.
This does not scrape WhatsApp and does not require unofficial libraries. It
gives the owner a secure bridge for iOS/Android shortcuts, a future Cloud API
webhook relay, or a manual operator paste flow so WhatsApp messages enter the
same lead CPT, routing, ack, AI and nurture rails as site forms.
```
REST: `nadlan/v1/wa-lead`
