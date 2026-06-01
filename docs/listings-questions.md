# Banked questions & blanks — listings / directory / auction (for owner + Cowork review)

> Per owner's "leave the questions for later, don't stop coding" directive. These are decisions and hardening items deliberately left open while the infrastructure (nadlan-config v1.5.0) was built. Nothing here blocks the code from being merged/tested; they shape the next pass.

## A. Business / product decisions (owner)
1. **Card monetization tiers** — what does "claiming" unlock and at what price? (Free claim + edit? Paid "pro" with photos/leads/analytics? Per-lead? Subscription?) Affects the claim UI + upgrade flow.
2. **Service-provider scope** — which professions to seed first? (שמאים / בדק בית / יועצי משכנתא / אדריכלים / עו"ד). Each needs its own registry source; יועצי משכנתא have NO statutory registry (self-reported only).
3. **Auction model** — are these real property auctions (legal/regulatory weight, earnest deposit, contract on win) or lead-gen "expression of interest"? This determines whether we wire deposits/e-sign/Bar-style compliance or keep it soft.
4. **Buyer's premium %, default reserve policy, auction duration** — defaults shipped: 5%-ish premium field, 120s soft-close window/extend, increment ₪1,000. Confirm real numbers.
5. **Pricing/positioning vs Yad2/Madlan** — free directory as a funnel into the lawyer-marketplace + listings? Confirm how the pieces connect commercially.
6. **nadlan.gov.il price scraping** — needs legal sign-off (no official API, ToS). Approve before building price enrichment.

## B. Security / correctness — REVIEW WITH COWORK (hands-on testing)
1. **Claim verification METHOD** — current build: admin manually approves + a token is generated, and on approve a subscriber account is created/linked by email. The strong anti-hijack step (OTP to the *registry-listed* phone/email, not a typed one) is NOT yet enforced. Implement before opening claims publicly. (See architecture skill §6.)
2. **Owner edit scope** — `map_meta_cap` grants a verified owner edit of their own card + `upload_files`. Verify they cannot escalate (edit other cards, access admin). Consider restricting editable fields rather than full post edit.
3. **Auto-created subscriber accounts** — approving a claim calls `wp_insert_user` + `wp_new_user_notification`. Confirm this matches desired onboarding and doesn't spam.
4. **Auction concurrency** — bid path uses MySQL `GET_LOCK`; load-test concurrent bids. WP-Cron closes hourly (not second-precise) — for live auctions add a real system cron / Action Scheduler.
5. **Auction payments** — deposit hold + winner capture (Grow/Meshulam) + e-sign on win are NOT built (stubs/hooks only). Required before real auctions.
6. **Importer rate/ToS** — CKAN is public/keyless; batches of 500 are polite. Confirm no rate issues at ~14k. Re-pull to get exact current counts.
7. **Thin-content noindex** — verify the `wp_robots`/`wpseo_robots` guard actually emits noindex on stub cards on the live site (Yoast interaction).

## C. Data / content blanks
1. **Card body enrichment** — cards import as `data_quality=stub` (noindexed). The ChatGPT original-prose generation (via `/nadlan/v1/import-enrich`) is the next batch job — hand to Cowork using the prompt template in the architecture skill §5.
2. **New-build projects** (beyond urban-renewal) — no single open dataset; needs scrape/integration of Yad2/Madlan/municipal feeds. Deferred.
3. **govmap/nadlan endpoints** — reverse-engineered; re-verify paths before building the deals/AVM layer.
4. **First lawyer + contract-audit inputs still pending** — bio, headshot, sample opinion (separate workstream).

## D. Listings "Zillow" features NOT yet built (roadmap, see architecture skill §3)
AVM + deal-history, neighborhood panel, saved-search alerts, seller "what's it worth" funnel, schedule-viewing, school/planning overlays, compare/favorites, משכנתא calculator, AI descriptions, 3D tours, virtual staging, NL search, e-sign. Prioritized list in the skill.

## E. Deploy state
- All built on branch `claude/charming-meitner-mwVEW` → PR #4. Plugin v1.5.0 ships via PUC: merge to main → WP Admin → Update. Bids table auto-installs on admin_init/activation. GA4 v1.4.0 tag also in this PR.
- Nothing affects the live site until merge + Update click.
