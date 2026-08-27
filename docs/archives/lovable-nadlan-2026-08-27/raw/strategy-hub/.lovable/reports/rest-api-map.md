# NadLan REST API map

Namespaces exposed by `nad-lan.co.il`: `nadlan/v1` (custom), `auctions/v1` (custom), plus stock `wp/v2`, `wc/*`, `yoast/v1`, `jetpack/v4`, `google-site-kit/v1`, `wc-admin*`, `wp-abilities/v1`, `wp-site-health/v1`, `wp-block-editor/v1`.

This map covers the **custom** routes only. Source paths are relative to `plugins/nadlan-config/`.

## Format

`METHOD /route` — handler file:line — auth — live-probe result.
Live probes were unauthenticated `GET`s.

## Discovery / catalog

| Route | Handler | Notes |
| --- | --- | --- |
| `GET /nadlan/v1/projects` | `inc/directory.php:746` | Public. Returns `{ok, html}` — server-rendered project cards markup. Probe: HTTP 200, ~19 KB HTML. |
| `GET /nadlan/v1/directory` | `inc/directory.php:224` | Public. Same shape (HTML cards) for professionals. Probe: HTTP 200, ~10 KB. |
| `GET /nadlan/v1/suggest` | `inc/autocomplete.php:38` | Public. Top cities/terms with counts. Probe: HTTP 200, JSON `{ok, items:[{name,count}]}`. |
| `GET /nadlan/v1/map` | `inc/map.php:17` | Public. Listings for map (lat/lng). Probe: HTTP 200, `{ok, count:0, items:[]}` — no live listings currently. |
| `GET /nadlan/v1/near` | `inc/geo-search.php:222` | Public. Geo radius search. |
| `POST /nadlan/v1/nl-search` | `inc/ai-features.php:172` | Natural-language search (OpenAI). |
| `POST /nadlan/v1/compare` | `inc/compare.php:25` | Side-by-side compare. |
| `GET\|POST /nadlan/v1/saved-search` | `inc/saved-search.php:45` | Saved searches. |
| `GET /nadlan/v1/saved-search/confirm` | `inc/saved-search.php:49` | Email-confirmation handoff. |

## Project showroom

| Route | Handler | Notes |
| --- | --- | --- |
| `GET /nadlan/v1/project-showroom/<id>` | `inc/project-3d.php:683` | **Auth-gated** — probe returned 401 `rest_forbidden`. Confirm whether intent is admin-only or `nonce`-checked; the spec docs imply public read. |

## AI concierge & leads

| Route | Handler | Notes |
| --- | --- | --- |
| `POST /nadlan/v1/concierge` | `inc/ai-concierge.php:346` | Conversational concierge. |
| `POST /nadlan/v1/concierge-lead` | `inc/ai-concierge.php:459` | Concierge → lead conversion. |
| `POST /nadlan/v1/lead` | `inc/conversion-cta.php:69` | Primary CTA lead intake. |
| `POST /nadlan/v1/wa-lead` | `inc/whatsapp-lead-ingestion.php:159` | WhatsApp webhook → lead. |
| `GET /nadlan/v1/lead/status` | `inc/lead-e2e.php:381` | Lead pipeline status. |
| `POST /nadlan/v1/drip-optout` | `inc/lead-drip.php:85` | Drip opt-out. |
| `GET /nadlan/v1/nurture/unsubscribe` | `inc/lead-nurture.php:603` | Nurture unsub. |
| `GET /nadlan/v1/referral/route` | `inc/lead-ledger.php:107` | Referral routing. |
| `POST /nadlan/v1/referral/<token>/accept` | `inc/lead-ledger.php:201` | Referral accept. |
| `GET /nadlan/v1/referral/<token>/status` | `inc/lead-ledger.php:216` | Referral status. |

## Monetization / advertisers

| Route | Handler | Notes |
| --- | --- | --- |
| `GET /nadlan/v1/offers` | `inc/offers.php:113` | Live probe: **HTTP 404 `rest_no_route`**. Discrepancy: route is registered in code but not reachable on prod — likely a `permission_callback` returning false unauth, or a missing include. See `docs-vs-reality.md`. |
| `GET /nadlan/v1/offers/leading/<card>` | `inc/offers.php:177` | Leading offer per card. |
| `POST /nadlan/v1/auction/bid` | `inc/placement-auction.php:285` | Placement-auction bid. |
| `GET /auctions/v1/<id>/state` | `inc/auction.php:131` | Auction state. |
| `GET /auctions/v1/<id>/bids` | `inc/auction.php:135` | Bids. |
| `POST /nadlan/v1/gi-ipn` | `inc/greeninvoice-recurring.php:322` | **GreenInvoice IPN webhook** — billing. Treat as untrusted input, must verify signature inside handler. |
| `GET /nadlan/v1/owner/whatsapp` | `inc/owner-config-rest.php:31` | Owner WhatsApp config. |
| `GET /nadlan/v1/owner/partners` | `inc/owner-config-rest.php:52` | Owner partners config. |

## Studio (owner media manager)

All under `nadlan/v1/studio/*` — `inc/studio-rest.php`. Authenticated.
- `POST /studio/<id>/save` (L55)
- `POST /studio/<id>/upload` (L138)
- `POST /studio/<id>/gallery/reorder` (L175)
- `POST /studio/<id>/gallery/delete` (L188)
- `POST /studio/<id>/ai-copy` (L204)
- `GET /studio/<id>` (L236)
- `GET /studio/mine` (L259)
- `POST /studio/create` (L300)

## Admin control

All under `nadlan/v1/admin-control/*` — `inc/admin-control.php`. Authenticated (admin).
- `GET /admin-control/cards` (L594)
- `GET\|POST /admin-control/card/<id>` (L599)
- `POST /admin-control/bulk` (L616)
- `POST /admin-control/impersonate/start` (L621)
- `POST /admin-control/impersonate/end` (L626)
- `POST /admin-control/impersonate/write-toggle` (L631)

## Ingest / import / valuation

| Route | Handler | Notes |
| --- | --- | --- |
| `POST /nadlan/v1/import-enrich` | `inc/import.php:211` | Enrich imported records. |
| `POST /nadlan/v1/import-run` | `inc/import.php:262` | Run import batch. |
| `POST /nadlan/v1/deals-ingest` | `inc/avm-deals.php:107` | Deals ingest. |
| `POST /nadlan/v1/avm` | `inc/avm-deals.php:168` | Auto valuation. |
| `POST /nadlan/v1/claim` | `inc/claim.php:41` | Claim a listing/professional. |
| `POST /nadlan/v1/favorite` | `inc/listings-ux.php:43` | Favorite a listing. |
| `POST /nadlan/v1/review-submit` | `inc/reviews.php:68` | Submit review. |
| `POST /nadlan/v1/glossary-publish` | `inc/glossary.php:233` | Publish glossary term. |

## Misc

| Route | Handler | Notes |
| --- | --- | --- |
| `GET /nadlan/v1/og/<id>.svg` | `inc/og-image.php:42` | Dynamic OG image as SVG. |
| `GET /nadlan/v1/health` | `inc/health.php:207` | Probe: HTTP 200. Returns plugin version, DB latency, GreenInvoice + OpenAI dependency status, lead E2E & AI usage counters. |
| `GET /nadlan/v1/healthcheck` | `nadlan-config.php:55` (root file) | Probe: HTTP 200. Catalog/CPT presence flags + AI provider + version. |

## Auth summary

Most write routes use `permission_callback` of either `is_user_logged_in` or a capability check; `lead`, `wa-lead`, `gi-ipn`, `concierge-lead` are public POSTs by design (forms/webhooks). The 401 on `/project-showroom/<id>` and 404 on `/offers` are the two anomalies worth confirming with you — both are listed as discrepancies in `docs-vs-reality.md`.

