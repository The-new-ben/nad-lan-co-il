# Full module audit - nadlan-config, orchestrator plugin, child theme
Date: 2026-07-02 · Method: 7 parallel read-only audit agents over every module,
cross-referenced against hooks, shortcode placements, REST routes, crons and the
live design law (page = engine, price, world, article, inquiry, disclaimer).

## A. FIXED IMMEDIATELY (shipped v1.69.96 - clear bugs, no approval needed)

| # | File | Bug | Fix |
|---|---|---|---|
| 1 | city-hubs.php | Banned brand "נדל\"ן חכם" in every city-hub page title | Title now "נדלן" |
| 2 | lead-drip.php | Banned brand in the auto welcome email + duplicate email sequences (drip fired on every lead alongside e2e ack/nurture) | Brand fixed; drip now OFF by default behind `nadlan_feature_lead_drip` |
| 3 | esign.php | Banned brand in winner email (dormant) | Fixed |
| 4 | city-hubs.php | /sitemap-nadlan-hubs.xml ran up to ~15,000 uncached queries per anonymous hit (DoS surface) | Output cached 12h |
| 5 | health.php | /nadlan/v1/health fired live outbound probes (greeninvoice+OpenAI, 4s timeouts) on every anonymous hit | Report cached 2 min |
| 6 | project-page-assembly.php | v1635 seeder re-ran up to 3 blocking 8s remote fetches on EVERY request until success | Done-flag set first |
| 7 | owner-config-rest.php | Lead auto-route hooked save_post, which fires BEFORE lead meta exists → blank leads emailed to an arbitrary partner + routing permanently marked done | Moved to wp_after_insert_post |
| 8 | tiers.php | "שדרגו לפרו" B2B box + Premier badge rendered on buyer-facing flagship projects (design law D4) | Engine-active projects exempt |
| 9 | featured-upsell.php | "You're at position #X, upgrade" pitch + coupon shown to every visitor, heavy rank query per view | Owner-only |
| 10 | directory.php | Raw machine enums (marketing/construction) printed as project status to visitors | Hebrew label map, unknown slugs hidden |
| 11 | social-proof.php | Legacy trust block still appended below the v2 homepage; per-view meta write on project pages | Front-page hook removed; counter now professionals-only |
| 12 | glossary-autolink.php | Pillar block + footer link strip stacked with the v2 homepage | Front-page block removed; strip skips front page |

## B. KILL LIST - awaiting owner approval (safe removals, nothing breaks)

1. **nadlan-platform-orchestrator (whole plugin)** - inert: home band permanently
   off, its only shortcode placement never renders (directory.php exits first),
   zero references from nadlan-config. Sole live effect: 2 wasted asset requests
   on every page. Deactivate + delete; also remove the dead shortcode from the
   child archive template and the no-op mark_home_showcase filters in child
   functions.php.
2. **auction.php + esign.php** - full auction engine with zero renderer, zero
   auctions, an empty public /auctions/ archive (SEO hole). Well-written, unused.
3. **homepage.php** - legacy home sections, superseded by home-v2; auto-inject
   already disabled. Verify shortcodes unplaced, then remove.
4. **project-page-assembly.php** - one-time Rainbow seeder whose data already
   persists in the DB; runtime filters redundant. Remove after extracting the
   two sanitize functions it borrows from project-3d (see 5).
5. **project-3d.php (the OLD showroom)** - zombie, but retirement requires 4
   extractions FIRST: (a) the script_loader_tag filter that makes model-viewer
   load as a module - THE NEW ENGINE DEPENDS ON IT; (b) sanitize functions used
   by project-page-assembly; (c) register_post_meta for project_3d_* keys the
   engine reads; (d) the admin metabox is still the ONLY authoring UI for
   units/facade/environment/price meta - needs a replacement before removal.
6. **lead-drip.php** - now off by default; retire fully in favor of
   lead-e2e ack + lead-nurture after one clean week.

## C. FIX QUEUE (real issues, need small builds - next releases)

- saved-search.php: POST endpoint abusable for opt-in email spam (720/day/IP to
  arbitrary addresses), unconfirmed rows never purged, no real unsubscribe.
- lead-ledger.php: /referral/<token>/accept mutates contract state on GET -
  email scanners auto-"accept terms". Must become POST behind a confirm page.
- claim.php: unauthenticated POST flips any card to claim_status=pending before
  verification - defer the flip to admin approval.
- compare.php: client JS injects listing titles unescaped (stored-XSS once
  public submissions grow).
- listings-ux.php: "similar listings" city filter is dead code (ignores
  location); WhatsApp CTA hardcodes the phone number instead of the option.
- studio-rest.php: /studio/create lets any logged-in user publish 10 live
  listings/day instantly while the wizard enforces pending moderation - align.
- loi-form.php: stores national ID as plain post meta (PII) - stop collecting
  or encrypt; then wire the form into project pages (it is placed nowhere).
- reviews.php: literal \n stored in review body when a title is given.
- offers.php: dedupe guard never expires (unbounded wp_options growth).
- breadcrumbs(5) + directory hero(5) + cards-render(20) + profile-extras(23)
  still render on flagship project pages beyond the six lawful blocks - decide
  which move inside the engine/article and which go.
- Floating #nlcta WhatsApp bubble renders on project pages (law: one compact bar).
- sponsored-spot.php: nested <a> inside card <a> (invalid HTML).
- preferred-partners.php: dead auto-route block (never-applied filter) - delete.
- autocomplete.php: footer JS runs on every page even without a city input.
- lead-e2e/whatsapp-ingestion/offers: idempotency guard options never GC'd.
- "popular this week" sorts by all-time views (mislabeled timeframe).
- studio.php picker prints raw post_type/tier values to advertisers.

## D. NOTABLE KEEPERS (well-built, leave alone)
greeninvoice-recurring (HMAC-verified IPN, idempotent), final-hardening (global
REST write rate-limiter), lead-e2e, import (gov.il, idempotent), geo-search,
placement-auction (properly guarded), whatsapp-lead-ingestion (fail-closed),
lead-nurture (HMAC unsubscribe), roles, studio (active advertiser editor),
premium-ui (design-law enforcer), child theme (cooperates with home-v2).

## E. Cross-cutting facts
- Banned brand: fully purged from the codebase as of v1.69.96.
- No fabricated social proof anywhere (counters are real; caveat: crawler-
  inflated views, weekly label on all-time data).
- All REST write routes with `__return_true` were individually examined: the
  acceptable ones self-protect (honeypot+rate limits+moderation); the two real
  problems (saved-search, referral-accept) are in the fix queue.
- The three "new surfaces" are the_content filters, not templates - every
  legacy the_content module stacks unless explicitly gated. That is the
  architectural root of the recurring stacking bugs.
