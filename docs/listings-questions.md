# Banked questions & blanks — full session inventory (for owner + Cowork)

> Per owner's "leave the questions for later, keep coding" directive. This is the single inventory of decisions, hardening items, integrations and content gaps left open while the infrastructure was built autonomously. Nothing here blocks merge/test — they shape the next pass.
>
> **Code state**: plugin v1.13.0 on `claude/charming-meitner-mwVEW` → PR #4. 17 modular includes under `inc/`. All PHP lints clean. Nothing live until PR #4 is merged to main and the WP "Update" is clicked.

---

## A. Business / product decisions (owner)
1. **Card monetization tiers** — what does claiming unlock and at what price? (Free claim + edit? Paid "pro" with photos/leads/analytics?)
2. **Service-provider scope** — which professions to seed first beyond contractors? (שמאים / בדק בית / יועצי משכנתא / אדריכלים / עו"ד) Each registry source separately (Cowork mission M8).
3. **Auction model** — real property auctions (legal weight, earnest deposit, contract) or lead-gen "expression of interest"? Determines whether we wire deposits + e-sign at full strength.
4. **Auction defaults** — buyer's premium %, default reserve policy, auction duration (current code defaults: 5%-ish premium field, 120s soft-close window/extend, ₪1,000 increment).
5. **Pricing/positioning** — how the free directory + lawyer-marketplace + auctions + listings tie together commercially.
6. **nadlan.gov.il price scraping** — needs legal sign-off (no official API, ToS-sensitive). Approve before deals ETL.
7. **LLM provider for AI features** (v1.9.0) — default Anthropic via `NADLAN_LLM_API_KEY`. Owner: choose provider + add the key to wp-config.php (or swap via `nadlan_llm_request` filter).
8. **e-Sign provider** (v1.11.0) — default = email-only (no provider). Pick BoldSign / Dropbox Sign / DocuSign / Israeli Comda etc. and wire via `nadlan_esign_create_request` filter. Document scope (offer letter only — see §B6).
9. **SMS/WhatsApp drip channel** (v1.12.0) — current drip is email-only. SMS has ~98% open rate; choose Twilio / local IL provider. Privacy/consent rules apply.
10. **Engagement tracking pixel** — open/click tracking in drip emails: IL Privacy Protection Law decision required. Off by default.
11. **Branded email template** — drip + transactional emails currently plain text. Approve HTML template + brand assets.

## B. Security / correctness — REVIEW WITH COWORK (hands-on testing in M5/M6)
1. **Claim verification METHOD** — current code stores a token + admin approves; the strong anti-hijack step (OTP to the *registry-listed* phone/email) is the planned hardening. Implement before opening claims publicly. Best-practice layered model in architecture skill §6.
2. **Owner edit scope** — `map_meta_cap` grants edit on owner's own card + `upload_files`. Verify no escalation (Cowork M5 step 3).
3. **Auto-created subscriber accounts** — claim-approve calls `wp_insert_user` + `wp_new_user_notification`. Confirm onboarding fit.
4. **Auction concurrency** — `GET_LOCK` per-auction; load-test concurrent bids. Hourly cron close (WP-Cron) is not second-precise — for tight finishes add a real system cron / Action Scheduler.
5. **Auction payments** — deposit hold + winner capture (Grow/Meshulam) NOT built (only stubs + hooks). Required before real auctions.
6. **e-Sign legal scope (IL)** — per **חוק חתימה אלקטרונית התשס"א-2001** (amended 2018), e-sign is **invalid** for property conveyances / land-registry / שטר מכר / POAs / bank-customer agreements. v1.11.0 adapter is intentionally scoped to the **offer/engagement letter** only, with a disclaimer baked into every document. **Counsel review required before go-live.**
7. **AI compliance scan (v1.9.0)** — list is conservative (HUD Fair-Housing + IL חוק איסור הפליה). Review with counsel before relaxing. Generator NEVER auto-publishes; flagged drafts wait for editor approval.
8. **Importer rate/ToS** — CKAN is public/keyless; 500/batch is polite. Confirm no rate issues at ~14k contractors.
9. **Thin-content noindex** — confirm `wp_robots`/`wpseo_robots` guard emits noindex on stub cards on the live site (Yoast interaction).
10. **REST endpoint hygiene** — public endpoints have honeypot + rate-limit (`/lead`, `/claim`, `/saved-search`); per-user rate-limit on `/auctions/v1/{id}/bids`. Logged-in REST (`/favorite`, `/import-enrich`) uses caps. Quick audit by Cowork during M5/M6.
11. **Overpass POI cache** (v1.11.0) — 24h transient per coord-bucket; fail-silent. Polite at default volumes (10k/day/IP limit).

## C. Data / content blanks
1. **Card body enrichment** — cards import as `data_quality=stub` (noindexed). Cowork M4 generates the original Hebrew prose and pushes via `/nadlan/v1/import-enrich`.
2. **New-build projects** beyond urban-renewal — no single open dataset; Cowork mission M9.
3. **govmap/nadlan deal endpoints** — reverse-engineered; verify (M10). AVM works off the cached `wp_nadlan_deals` table either way (slot in via `nadlan_deals_remote` filter or `POST /nadlan/v1/deals-ingest`).
4. **Service-provider registries** — Cowork mission M8.
5. **First lawyer + contract-audit inputs** still pending — bio, headshot, sample opinion.

## D. Roadmap NOT YET built (research-validated, prioritized)
- AVM upgrade: gradient-boosting model + SHAP explainability (v1.7.0 ships median-comps baseline).
- Repeat-sales index per neighborhood + price-trend chart.
- AI image alt-text / auto-tagging (vision API; adapter pattern).
- AI virtual staging (paid API; legally REQUIRED to disclose "virtually staged").
- WhatsApp Business chatbot.
- True realtime auction updates (Pusher/Ably) vs current `/state` polling.
- Property-tokenization / on-chain (skip — confirmed hype for IL local site in 2026).
- Tel Aviv opendata permit feed; CBS neighborhood demographics integration.

## E. Deploy state
- Branch `claude/charming-meitner-mwVEW` → **PR #4**. Plugin ships via PUC: merge to main → WP Admin → Update → click. Bids/deals tables auto-install on admin_init/activation. Healthcheck reports version + module readiness at `GET /wp-json/nadlan/v1/healthcheck`.
- **NadLan Ops** admin page (v1.13.0) surfaces every counter (leads/claims/cards/imports/auctions/data layer) in one screen.
- GA4 v1.4.0 fix is in this PR too.
- **Versions shipped this session**: 1.4.0 (GA4), 1.5.0 (directory+claim+importer+auction+schema+cards-render), 1.6.0 (listings-UX), 1.7.0 (AVM+deals+neighborhood), 1.8.0 (saved-search+alerts), 1.9.0 (AI desc generator + NL search), 1.10.0 (city hubs + media), 1.11.0 (compare + POI + e-sign), 1.12.0 (map + drip), 1.13.0 (ops dashboard).
