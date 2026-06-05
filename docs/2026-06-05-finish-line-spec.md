# nad-lan.co.il — Finish-Line Build Spec (full PLD + code + cited best practices)

**Status:** authoritative for the remaining build. Supersedes nothing; it *completes* `docs/2026-06-04-master-architecture-build-bible.md`. Where this doc and the bible disagree on a remaining gap, this doc wins, because it is grounded in the cited research in the Sources appendix.

**Audience:** Codex (coding lane). Claude reviews and deploys. Codex never merges, opens DRAFT PRs only.

**Why this doc exists:** the owner asked for the finish line with no quality compromise, backed by real expert research (39 distinct authoritative sources below, all with URLs and several hard statistics). Every implementation rule here is traceable to a cited source. Do not invent behavior that contradicts a citation.

---

## Part 0 — How to use this doc

1. One gap = one branch = one DRAFT PR, rebased on current `main`. Branch names: `codex/gap5-geo-search`, `codex/gap6-roles`, `codex/gap3-recurring`, then the hardening tracks `codex/ai-support-hardening`, `codex/business-metrics`, `codex/reliability`.
2. Run all 10 cycles per gap (C1 foundation … C10 hardening) and show the per-cycle checklist in the PR body with a one-line note each + a manual QA/curl proof.
3. **Plugin lane only** (`plugins/nadlan-config/**` + `docs/**`). Never touch theme files (`assets/css` premium, `functions.php` homepage, `patterns/`). Leave documented hooks/filters for Claude to wire in the theme.
4. **Never commit secrets** — public repo. Keys/secrets live in `get_option()`; only the option *name* appears in code.
5. Bump the plugin version header + healthcheck + manifest on every functional PR.
6. Hebrew, RTL, copywriting-skill rules (no em-dash, no internal/dev words, CTA allow-list) on every user-facing string.

---

## Part 1 — The complete "real marketplace needs" map

This is the full catalogue of what a real multi-sided property marketplace needs, with current status. Items marked **MISSING** or **PARTIAL** are the finish-line scope.

| # | Capability | Why it matters | Status |
|---|---|---|---|
| 1 | Listings catalog (projects/pros/properties) | core inventory | ✅ built |
| 2 | Paid placement / featured ranking | primary monetization | ✅ GAP 1 live (1.42.8) |
| 3 | Lead capture + routing to paid owners | converts traffic to value | ✅ GAP 2 (PR #71, pending deploy) |
| 4 | Payments + invoicing (WooCommerce + Morning) | take money legally in IL | ✅ built |
| 5 | **Recurring revenue (auto-renew)** | predictable MRR, zero-touch | 🟡 GAP 3 — free Green-Invoice IPN path, NOT built |
| 6 | **Geo / "near me" search** | the #1 property-search behavior | 🔴 GAP 5 — NOT built |
| 7 | **Roles & capabilities (buyer/advertiser/admin)** | security + self-serve management | 🔴 GAP 6 — NOT built |
| 8 | AI concierge | support deflection, engagement | 🟡 GAP 4 (PR #72) — needs support-grade hardening |
| 9 | **Business metrics + autopilot dashboard** | owner sees the business without touching code | 🔴 NOT built |
| 10 | **Reliability: health, errors, logging, alerting** | a zero-touch business cannot silently die | 🔴 NOT built |
| 11 | Reviews / ratings / trust signals | conversion + trust | 🔴 future (note hooks) |
| 12 | Notifications (email + future WhatsApp/SMS) | re-engagement, lead speed | 🟡 lead emails only; `nadlan_lead_deliver` filter ready |
| 13 | Saved searches / favorites / alerts | retention loop | 🔴 future (note hooks) |
| 14 | Privacy/GDPR + consent + data export/erase | legal, and WP has native hooks | 🔴 note + minimal |
| 15 | SEO (schema.org RealEstateListing, sitemaps, OG) | organic acquisition | 🟡 partial |
| 16 | Accessibility (WCAG) + RTL Hebrew correctness | legal in IL + UX | 🟡 partial |
| 17 | Anti-spam / rate limiting on public forms | cost + abuse | 🟡 lead form 8/hr/IP; extend |

Build order for this doc: **GAP 5 → GAP 6 → GAP 3 → AI support hardening → business metrics → reliability.** Items 11/13 stay future but you MUST leave documented `do_action`/`apply_filters` seams so they slot in later.

---

## Part 2 — GAP 5: Geo / "near me" search

### What / Why
Radius and map search is the dominant property-search behavior; major portals (Redfin, Zillow) refresh results on map pan with no search button and cluster dense markers (https://raw.studio/blog/using-maps-as-the-core-ux-in-real-estate-platforms/). We already store `lat`/`lng` card meta. The job is a fast, index-friendly nearest-search that **still respects paid placement (GAP 1)** within the result set.

### Where
New file `plugins/nadlan-config/inc/geo-search.php`. REST: extend the existing directory query / add `GET /nadlan/v1/near?lat=&lng=&radius_km=`. Loader entry in `nadlan-config.php`.

### The core engineering rule (cited)
A raw Haversine in a `WHERE` clause **cannot use a B-tree index** because the columns are buried in a calculation, forcing a full-table scan that computes the formula per row (a no-index distance scan estimated 4.67M rows / 10+ seconds) (https://aaronfrancis.com/2021/efficient-distance-querying-in-my-sql). The fix is a **bounding-box prefilter** that the optimizer can range-scan, then exact distance only on survivors.

Bounding box math (km; the `COS(lat)` term contracts longitude degrees toward the poles) (https://www.plumislandmedia.net/mysql/haversine-mysql-nearest-loc/):
- Latitude band: `lat ± (radius_km / 111.045)`
- Longitude band: `lng ± (radius_km / (111.045 * COS(RADIANS(lat))))`

Exact distance in SQL, with the `LEAST(1.0, …)` guard that prevents `ACOS` domain errors from float rounding (https://www.plumislandmedia.net/mysql/haversine-mysql-nearest-loc/):
```sql
111.045 * DEGREES(ACOS(LEAST(1.0,
  COS(RADIANS(:lat)) * COS(RADIANS(lat)) * COS(RADIANS(lng) - RADIANS(:lng))
  + SIN(RADIANS(:lat)) * SIN(RADIANS(lat))
)))
```

If/when we migrate to a native `POINT` column: store as **SRID 4326** (WGS84/GPS) and add a `SPATIAL INDEX` (R-tree), then use `ST_Distance_Sphere(g1,g2)` which returns **meters** with default sphere radius 6,370,986 m; both POINTs must share the SRS or you get `ER_GIS_DIFFERENT_SRIDS` (https://dev.mysql.com/doc/refman/8.0/en/spatial-convenience-functions.html). For now we stay on lat/lng meta + bounding box because that's what the data model has; **add a composite index** the optimizer can use.

### Implementation (PHP, posts_clauses approach to stay inside WP_Query)
```php
// inc/geo-search.php
if ( ! function_exists( 'nadlan_geo_search_args' ) ) {
    function nadlan_geo_search_args( $args, $lat, $lng, $radius_km ) {
        $args['nadlan_geo'] = array(
            'lat' => (float) $lat, 'lng' => (float) $lng,
            'radius_km' => max( 0.5, min( 100, (float) $radius_km ) ), // clamp
        );
        return $args;
    }
}
add_filter( 'posts_clauses', 'nadlan_geo_clauses', 30, 2 ); // after paid-placement (20)
function nadlan_geo_clauses( $clauses, $q ) {
    $geo = $q->get( 'nadlan_geo' );
    if ( empty( $geo ) ) { return $clauses; }
    global $wpdb;
    $lat = $geo['lat']; $lng = $geo['lng']; $r = $geo['radius_km'];
    $latDelta = $r / 111.045;
    $lngDelta = $r / ( 111.045 * max( 0.01, cos( deg2rad( $lat ) ) ) );
    // JOIN lat/lng meta
    $clauses['join'] .= " INNER JOIN {$wpdb->postmeta} glat ON glat.post_id={$wpdb->posts}.ID AND glat.meta_key='lat'";
    $clauses['join'] .= " INNER JOIN {$wpdb->postmeta} glng ON glng.post_id={$wpdb->posts}.ID AND glng.meta_key='lng'";
    // Bounding box prefilter (index-usable) — cheap, prunes the table first
    $clauses['where'] .= $wpdb->prepare(
        " AND CAST(glat.meta_value AS DECIMAL(10,6)) BETWEEN %f AND %f
          AND CAST(glng.meta_value AS DECIMAL(10,6)) BETWEEN %f AND %f",
        $lat - $latDelta, $lat + $latDelta, $lng - $lngDelta, $lng + $lngDelta
    );
    // Exact distance as a selected expression so we can order/having on it
    $dist = $wpdb->prepare(
        "111.045 * DEGREES(ACOS(LEAST(1.0,
            COS(RADIANS(%f)) * COS(RADIANS(CAST(glat.meta_value AS DECIMAL(10,6))))
            * COS(RADIANS(CAST(glng.meta_value AS DECIMAL(10,6))) - RADIANS(%f))
            + SIN(RADIANS(%f)) * SIN(RADIANS(CAST(glat.meta_value AS DECIMAL(10,6)))) )))",
        $lat, $lng, $lat
    );
    $clauses['fields']  .= ", ($dist) AS nadlan_distance_km";
    $clauses['where']   .= $wpdb->prepare( " AND ($dist) <= %f", $r );
    // Paid placement still wins, then distance. Keep GAP 1 ordering first.
    $clauses['orderby'] = "CASE pt.meta_value WHEN 'premier' THEN 2 WHEN 'pro' THEN 1 ELSE 0 END DESC, nadlan_distance_km ASC, {$wpdb->posts}.post_date DESC";
    return $clauses;
}
```
> Note for Claude: the `pt` alias is GAP 1's paid_tier join; on rebase ensure both `posts_clauses` filters compose (paid-placement priority 20, geo priority 30) and the orderby merges rather than overwrites. If composition is fragile, fold geo ordering into the GAP 1 clause builder.

### 10-cycle must-haves
- **C3 edge:** clamp radius (0.5–100 km); reject non-numeric lat/lng; cards with no lat/lng are excluded (INNER JOIN does this).
- **C8 performance:** add a composite index migration `(meta_key, meta_value)` is already there via WP; additionally document that at scale we move lat/lng to a dedicated indexed table or POINT column (cite Aaron Francis). Bounding box MUST come before exact distance.
- **C9 UX seam:** expose `nadlan_distance_km` to the card template; emit `do_action('nadlan_geo_results', $results)` so the theme can render "X km away" + a map. Default radius 25 km; allow 1/5/10/25/50.
- **C10:** "search this area" param for future map-pan (Redfin pattern) — accept a bounding box directly too.

---

## Part 3 — GAP 6: Roles & capabilities

### What / Why
A self-serve marketplace needs least-privilege roles: visitors/buyers read-only, advertisers manage only their own listings, admins manage all. Gate features by **capability, never by role name**, because a user can hold multiple roles (https://developer.wordpress.org/plugins/users/roles-and-capabilities/).

### Where
New file `plugins/nadlan-config/inc/roles.php`. Setup runs on activation + a versioned migration gate, NOT on `init` every load.

### Cited rules → concrete code
- `add_role()` "adds a role, if it does not exist"; after first call **sequential calls do nothing, including altering the capabilities list** — so running it every load silently fails to update caps and wastes a DB lookup (https://developer.wordpress.org/plugins/users/roles-and-capabilities/). ⇒ Version the setup; on cap changes, `remove_role()` then `add_role()`, or amend with `get_role()->add_cap()`.
- Register listings CPT with `'capability_type' => 'listing'` and `'map_meta_cap' => true`; without `map_meta_cap=>true` WP ignores authorship/status context (https://developer.wordpress.org/reference/functions/map_meta_cap/). `map_meta_cap()` maps `edit_post` → `edit_posts`/`edit_published_posts` for the author, else `edit_others_posts` — this is exactly how an advertiser edits only their own listing.
- Never assign meta caps (`edit_post`) directly to a role; they exist only for the `map_meta_cap` filter (https://justintadlock.com/archives/2010/07/10/meta-capabilities-for-custom-post-types).
- Per-object checks MUST pass the ID: `current_user_can('edit_post', $listing_id)` so `map_meta_cap` runs; calling without the ID checks only the primitive cap and **leaks cross-owner access** (https://developer.wordpress.org/reference/functions/map_meta_cap/).

```php
// inc/roles.php
const NADLAN_ROLES_VERSION = 1;

function nadlan_roles_setup() {
    if ( (int) get_option('nadlan_roles_version') >= NADLAN_ROLES_VERSION ) return; // idempotent gate

    // Advertiser: owner-scoped listing caps (primitives, NOT meta caps)
    remove_role('nadlan_advertiser'); // safe re-register on version bump
    add_role('nadlan_advertiser', 'מפרסם', array(
        'read' => true,
        'edit_listings' => true,
        'edit_published_listings' => true,
        'publish_listings' => true,
        'delete_listings' => true,
        'upload_files' => true,
        // deliberately NOT edit_others_listings -> least privilege
    ));

    // Buyer: read-only + saved searches (future)
    remove_role('nadlan_buyer');
    add_role('nadlan_buyer', 'קונה', array('read' => true));

    // Grant admins the management caps
    $admin = get_role('administrator');
    foreach (array('edit_listings','edit_others_listings','publish_listings',
                   'delete_listings','delete_others_listings','manage_advertisers') as $c) {
        if ($admin) $admin->add_cap($c);
    }

    // Migrate existing users by current meta (claim_status / owner_user_id / paid_tier)
    nadlan_roles_migrate_existing_users();

    update_option('nadlan_roles_version', NADLAN_ROLES_VERSION);
}
register_activation_hook( NADLAN_CONFIG_FILE, 'nadlan_roles_setup' );
add_action( 'admin_init', 'nadlan_roles_setup' ); // also catches plugin-update (gated, runs once)

// CPT registration must use map_meta_cap (where listings are registered):
//   'capability_type' => array('listing','listings'),
//   'map_meta_cap'    => true,
//   'capabilities'    => array('edit_posts'=>'edit_listings', ...)
```
- **Migration safety:** loop users under the version gate; use `$user->add_cap()` / role reassignment; idempotent because `add_cap`/`add_role` are safe to re-call (https://developer.wordpress.org/plugins/users/roles-and-capabilities/).
- **Uninstall:** `remove_role()` custom roles, `remove_cap()` custom caps from remaining roles to avoid orphaned DB entries.
- **C5 security gate:** replace any existing `in_array('advertiser',$user->roles)` checks with `current_user_can('edit_listings')`; the Advertiser Center inbox (GAP 2) ownership check stays `=== (int) get_current_user_id()`.

---

## Part 4 — GAP 3: Recurring revenue (FREE, Green-Invoice native + IPN)

### What / Why
~30% of subscription churn is **involuntary** (failed payments), and dunning recovers ~70% of initially-failed payments (GoCardless Success+ 70% vs 38% baseline) (https://gocardless.com/en-us/blog/farewell-to-failed-payments-with-success-plus/). Subscription businesses lose ~9% of MRR to failed payments; automated dunning recovers 45–70% (https://baremetrics.com/blog/recover-failed-payments-save-lost-revenue). So recurring billing without dunning + reconciliation leaks real money. We use Morning/Green-Invoice **native recurring standing orders (הוראת קבע)** + a secret-verified IPN webhook — cost ₪0, no $199 WooCommerce Subscriptions.

### Where
New file `plugins/nadlan-config/inc/greeninvoice-recurring.php`. REST: `POST /nadlan/v1/gi-ipn`. Cron: `nadlan_gi_reconcile` daily.

### Webhook security (cited, mandatory)
- **Verify signature before any business logic.** An unverified endpoint lets an attacker forge "payment succeeded" and grant access for free (https://docs.stripe.com/webhooks). Build `signed_payload = timestamp + "." + raw_body`, HMAC-SHA256 with the shared secret (from `get_option('nadlan_gi_ipn_secret')`, never in code), **constant-time compare** (`hash_equals`).
- **Timestamp tolerance 300 s (5 min)** to block replay; never 0 (https://docs.stripe.com/webhooks). Keep server clock NTP-synced.
- **Return 2xx fast, process async** to absorb renewal spikes (https://docs.stripe.com/webhooks).

### Idempotency (cited, mandatory)
- **Dedupe on the event/charge id**; if seen, return 200 immediately with no side effects (https://docs.stripe.com/webhooks).
- **TTL of the dedupe store must exceed the retry window** — providers retry up to 3 days, so persist processed ids ≥ 3 days or late retries slip through (https://hookdeck.com/webhooks/guides/implement-webhook-idempotency).
- **Tolerate out-of-order delivery**; fetch missing objects via API rather than assuming sequence (https://docs.stripe.com/webhooks).

```php
// inc/greeninvoice-recurring.php
add_action('rest_api_init', function () {
    register_rest_route('nadlan/v1', '/gi-ipn', array(
        'methods'  => 'POST',
        'callback' => 'nadlan_gi_ipn_handler',
        'permission_callback' => '__return_true', // auth is the signature, below
    ));
});

function nadlan_gi_ipn_handler( WP_REST_Request $req ) {
    $secret = get_option('nadlan_gi_ipn_secret');           // option name only
    if ( ! $secret ) return new WP_REST_Response(array('error'=>'not_configured'), 503);

    $raw = $req->get_body();
    $sig = $req->get_header('x-nadlan-signature');           // "t=...,v1=..."
    if ( ! nadlan_gi_verify( $raw, $sig, $secret, 300 ) ) {  // 5-min tolerance
        return new WP_REST_Response(array('error'=>'bad_signature'), 401);
    }

    $data = json_decode( $raw, true );
    $event_id = isset($data['id']) ? sanitize_text_field($data['id']) : '';
    if ( $event_id === '' ) return new WP_REST_Response(array('error'=>'no_id'), 400);

    // Idempotency: dedupe by event id, TTL > 3-day retry window
    $log = get_option('nadlan_gi_charge_log', array());
    if ( isset($log[$event_id]) ) return new WP_REST_Response(array('ok'=>true,'idempotent'=>true), 200);

    // ref pattern card_<id>_user_<uid>_tier_<tier>
    $ref = isset($data['ref']) ? sanitize_text_field($data['ref']) : '';
    $parsed = nadlan_gi_parse_ref( $ref );
    if ( ! $parsed ) return new WP_REST_Response(array('error'=>'bad_ref'), 422);

    $status = isset($data['status']) ? sanitize_text_field($data['status']) : '';
    if ( $status === 'paid' ) {
        nadlan_gi_extend_campaign( $parsed['card'], $parsed['tier'] ); // extend campaign_end, affirm paid_tier
        $log[$event_id] = array('t'=>time(),'ref'=>$ref,'status'=>'paid');
    } elseif ( $status === 'failed' ) {
        nadlan_gi_mark_dunning( $parsed['card'], $parsed['tier'] );    // start retry/grace window
        $log[$event_id] = array('t'=>time(),'ref'=>$ref,'status'=>'failed');
    }
    // bound + persist (keep >= 3 days; cap entries)
    $log = nadlan_gi_prune_log( $log, 4000 );
    update_option('nadlan_gi_charge_log', $log, false);
    return new WP_REST_Response(array('ok'=>true), 200);
}

function nadlan_gi_verify( $raw, $sig_header, $secret, $tolerance ) {
    if ( ! $sig_header ) return false;
    $parts = array(); foreach (explode(',', $sig_header) as $p) { $kv = explode('=', $p, 2); if (count($kv)===2) $parts[trim($kv[0])] = trim($kv[1]); }
    if ( empty($parts['t']) || empty($parts['v1']) ) return false;
    if ( abs( time() - (int) $parts['t'] ) > $tolerance ) return false;       // replay window
    $expected = hash_hmac('sha256', $parts['t'] . '.' . $raw, $secret);
    return hash_equals( $expected, $parts['v1'] );                             // constant-time
}
```

### Dunning / failed-payment retry (cited)
- Recurly default: **retry every 2 days, up to 5 attempts**; keep dunning **≤ 27–28 days** for monthly plans (longer wastes the billing window) (https://docs.recurly.com/docs/retry-logic , https://recurly.com/blog/dunning-process/).
- Smart/ML-timed retries beat fixed intervals (Stripe scores 500+ attributes per attempt; ~$9 recovered per $1 spent) (https://stripe.com/blog/how-we-built-it-smart-retries). We can't run ML, so use a fixed cadence: retry at days 2/4/7/14, **grace period until day 27** before downgrading.
- Implement `nadlan_gi_mark_dunning` to set `dunning_state` + `dunning_since`; the daily cron escalates and only after the grace window flips `paid_tier` down and fires `do_action('nadlan_subscription_lapsed', $card)`.

### Reconciliation (cited)
- **Webhooks are not guaranteed delivery** — run a daily reconciliation job that pulls charge/subscription state via the Green-Invoice API to catch missed IPNs; provider auto-retry only lasts ~3 days (https://docs.stripe.com/webhooks).
- **Apply a grace period before downgrading** — let the full dunning cycle (~27 days) complete before revoking access (https://recurly.com/blog/dunning-process/).

```php
// daily cron
add_action('nadlan_gi_reconcile', function () {
    // 1) pull recent charges from Green-Invoice API (key from get_option)
    // 2) for any 'paid' charge not in nadlan_gi_charge_log -> apply extend (missed IPN)
    // 3) advance dunning state machine; downgrade only past grace (day 27)
});
if ( ! wp_next_scheduled('nadlan_gi_reconcile') ) wp_schedule_event( time()+3600, 'daily', 'nadlan_gi_reconcile' );
```

### Owner prerequisites (surface as admin settings, do NOT block code)
1. Create the Morning recurring-charge links (one per tier/cycle).
2. Set `nadlan_gi_ipn_secret`.
3. Confirm per-tier cycle days (default 31).
PR body must include a **simulated-IPN curl** with a valid HMAC as proof.

---

## Part 5 — AI concierge → support-grade agent (hardening on GAP 4)

### What / Why
GAP 4 shipped the OpenAI provider switch. To be a real support agent (and to deflect tickets so the owner doesn't), it needs grounding, guardrails, handoff, cost control, and a deflection metric. Benchmark: Intercom Fin reached **50.8% resolution participating in 96% of conversations at Anthropic** (https://fin.ai/).

### Cited rules → requirements
- **RAG grounding:** answer only from approved knowledge (the site's guides/FAQ/listing data); cite a source per factual claim; refuse when no evidence ("sources or abstain") (https://www.clarityarc.com/insights/ai-hallucination-grounding-citation). For long context, extract verbatim quotes first, then answer from those quotes (https://docs.claude.com/en/docs/test-and-evaluate/strengthen-guardrails/reduce-hallucinations).
- **Permission to say "I don't know":** models over-answer because they're rewarded for answering; explicitly allow uncertainty (https://docs.claude.com/en/docs/test-and-evaluate/strengthen-guardrails/reduce-hallucinations).
- **Concise refusals (1–2 sentences), offer an alternative, restrict scope** so off-topic is declined not improvised (https://dzlab.github.io/ai/2025/05/12/peeking-under-the-hood-claude/).
- **Human handoff:** escalate when the agent can't resolve / low confidence / user asks for a human; on escalation, change conversation status so the bot stops owning it (no loop) and carry full context forward (https://support.zendesk.com/hc/en-us/articles/5352026794010-About-automated-resolutions-for-AI-agents).
- **Cost control:** prompt caching — put the static system prompt + reference material at the front; caching applies to prefixes ≥1,024 tokens, cutting input cost up to 90% / latency up to 80% (https://openai.com/index/api-prompt-caching/); cached input can drop $2.50→$0.25 per M tokens (https://openai.com/api/pricing/). Keep the cheap default model (gpt-4o-mini); only escalate hard tickets.
- **Metric:** distinguish **deflection** (1 − escalation rate, can mask bad answers) from **automated resolution** (verified the request was actually satisfied) (https://support.zendesk.com/hc/en-us/articles/8357756478106-Understanding-the-difference-between-deflection-AI-agent-handled-automated-resolution-and-custom-resolution-rates). Track Automation = Involvement × Resolution (https://www.intercom.com/help/en/articles/13533623-fin-ai-agent-automation-rate).

### Implementation deltas (on `nadlan_ai_chat`)
- Build a `nadlan_ai_kb()` retrieval over existing guides/FAQ (post content) → inject top-K chunks as the grounded context block at the **front** of the prompt (caching).
- System prompt: scope to nadlan topics; require citing the guide/listing it used; allow "איני בטוח" + offer to connect to a human.
- Add `nadlan_ai_should_escalate($answer,$confidence)` → on escalate, write a lead/ticket via the GAP 2 `nadlan_lead_route` path and return a Hebrew handoff message.
- Log per-conversation `escalated` bool + `grounded` bool to a `nadlan_ai_quality_log`; healthcheck exposes deflection + (later) resolution.
- Keep the global cost ceiling + `sslverify=>true` from my GAP 4 review.

---

## Part 6 — Business metrics + autopilot dashboard

### What / Why
A near-zero-touch business needs the owner to see the few numbers that matter daily without logging into code. NRR > 100% (net-negative churn) compounds growth from the existing base alone; ~40% of $15–30M ARR firms achieve it (https://chartmogul.com/saas-metrics/negative-churn/). LTV:CAC should be **> 3** (https://www.forentrepreneurs.com/ltv-cac/) and CAC payback **< 12 months** (https://www.forentrepreneurs.com/ltv-cac/).

### The daily numbers to surface (Ops "Autopilot" panel)
Push these in one view (Baremetrics-style real-time) (https://baremetrics.com/blog/saas-metrics-dashboards-examples-templates):
1. **MRR** — sum of active monthly recurring (https://baremetrics.com/blog/saas-metrics-checklist-kpis-founders-should-track).
2. **Active paid** (pro/premier counts), **new signups** today/7d.
3. **Churn** — logo vs revenue (https://chartmogul.com/saas-metrics/customer-churn/).
4. **NRR** = (Start + Expansion + Reactivation − Contraction − Churn) ÷ Start; target > 100% (https://chartmogul.com/saas-metrics/nrr/).
5. **MRR at risk / failed payments** — revenue tied to delinquent (dunning) cards + time-to-recovery; this involuntary churn is otherwise silent (https://baremetrics.com/blog/recover-failed-payments-save-lost-revenue).
6. **Lead volume + delivery rate** (from GAP 2 `nadlan_lead_log`).
7. **Activation** — % of new advertisers who publish a listing within 7 days (median activation 25%, SaaS 30%; "good"=60th pct) (https://www.lennysnewsletter.com/p/what-is-a-good-activation-rate).
8. **AI deflection** (from Part 5).

Net MRR churn formula to implement (negative is good): `(Churn + Contraction − Expansion − Reactivation) ÷ Start MRR` (https://chartmogul.com/saas-metrics/negative-churn/). Display ratios directionally — "LTV:CAC ratios are to be used, not believed" (https://www.forentrepreneurs.com/ltv-cac/).

### Where
Extend `inc/ops-dashboard.php` with a `nadlan_metrics_snapshot()` (cached daily transient) reading orders + `paid_tier` + `nadlan_gi_charge_log` + `nadlan_lead_log`. Healthcheck adds a `business` block. Optional: a daily email/Slack digest behind a filter `nadlan_metrics_digest`.

---

## Part 7 — Technical support / reliability

### What / Why
A zero-touch business cannot silently die. Alert on **symptoms users feel, not internal causes** (Google SRE) (https://sre.google/sre-book/practical-alerting/).

### Cited rules → requirements
- **Health endpoint:** expose `GET /wp-json/nadlan/v1/health` that actively pings each dependency (DB query, Morning/Green-Invoice API reachability, OpenAI reachability) and returns aggregate status; **alert on the end-to-end symptom**, not each probe (https://sre.google/sre-book/monitoring-distributed-systems/). External uptime checks run from outside the host so they catch full-server/DNS outages; check revenue endpoints every 30–60s (https://betterstack.com/docs/uptime/check-frequency/).
- **Cron heartbeats:** the daily reconcile/dunning crons "phone home" to an uptime heartbeat so a missed run alerts (https://betterstack.com/docs/uptime/uptime-monitor/).
- **Error monitoring:** capture PHP exceptions to a service/log; route only high-severity to the owner, alert only past a frequency threshold (N events / N users in a window), use anomaly thresholds for spiky data — avoid alert fatigue (https://docs.sentry.io/product/alerts/best-practices/ , https://docs.sentry.io/product/new-monitors-and-alerts/alerts/best-practices/).
- **Structured logging:** for billing/webhook/AI events log a stable event id + status + timestamp (reconcile + dedupe); **never log secrets/PII/card data** — scrub before send (https://docs.sentry.io/product/alerts/best-practices/). Bound retention: `WP_DEBUG_LOG` writes `wp-content/debug.log` unbounded → rotate/cap (https://developer.wordpress.org/advanced-administration/debug/debug-wordpress/).
- **WP cron reliability:** WP-Cron is traffic-dependent; for a business set `define('DISABLE_WP_CRON', true)` and a real server cron hitting `wp-cron.php` on a fixed clock so reconcile/dunning never silently stop (https://www.inmotionhosting.com/support/edu/wordpress/disable-the-wp-cron/). Surface failed loopback/WP-Cron via Site Health (https://wordpress.org/support/topic/cron-is-disabled-on-your-site/).
- **SLO basics:** pick one availability target (e.g., 99.9%); use multi-window multi-burn-rate alerts (page at burn rate 14.4 over 1h/5min; ticket at 1 over 3 days); for low-traffic sites aggregate to real user impact (https://sre.google/workbook/alerting-on-slos/).

### Where
New file `plugins/nadlan-config/inc/health.php` (health endpoint + dependency probes + structured event logger `nadlan_log_event($channel,$id,$status,$meta)` that scrubs secrets and bounds size). Document the owner steps: set `DISABLE_WP_CRON` + server cron, point an external uptime monitor at `/health` and at cron heartbeats.

---

## Part 8 — Future seams (must exist now, build later)
Leave these `do_action`/`apply_filters` hooks so the build is extensible without refactors:
- Reviews/ratings: `do_action('nadlan_after_lead_closed', $lead_id)` to prompt a review.
- Notifications: the GAP 2 `nadlan_lead_deliver` filter already abstracts the channel (email today, WhatsApp/SMS later).
- Saved searches/alerts: `do_action('nadlan_search_executed', $args, $user_id)`.
- Privacy/GDPR: register WP's native `wp_privacy_personal_data_exporters` / `_erasers` for lead + AI logs; honor data-erase.
- SEO: emit `schema.org/RealEstateListing` JSON-LD via a filter the theme can print.

---

## Sources (39 distinct authorities, grouped)

**Recurring billing / webhooks / dunning**
1. Stripe — Webhooks (signature/HMAC, 300s tolerance, 2xx-fast, dedupe, out-of-order, reconcile) https://docs.stripe.com/webhooks
2. Stripe — How we built Smart Retries (ML retries, ~$9 per $1) https://stripe.com/blog/how-we-built-it-smart-retries
3. GoCardless — Success+ (30% churn involuntary; 70% vs 38% recovery) https://gocardless.com/en-us/blog/farewell-to-failed-payments-with-success-plus/
4. Recurly — Retry logic (every 2 days, up to 5; caps) https://docs.recurly.com/docs/retry-logic
5. Recurly — Dunning process (≤27–28 days; A/R aging; grace before downgrade) https://recurly.com/blog/dunning-process/
6. Hookdeck — Webhook idempotency (TTL > retry window) https://hookdeck.com/webhooks/guides/implement-webhook-idempotency

**Geospatial search**
7. MySQL — Spatial convenience functions (ST_Distance_Sphere, SRID 4326, errors) https://dev.mysql.com/doc/refman/8.0/en/spatial-convenience-functions.html
8. Aaron Francis — Efficient distance querying in MySQL (index limits, bounding box, benchmarks) https://aaronfrancis.com/2021/efficient-distance-querying-in-my-sql
9. Plum Island Media — Haversine MySQL nearest-loc (box math, ACOS LEAST guard) https://www.plumislandmedia.net/mysql/haversine-mysql-nearest-loc/
10. Raw.studio — Maps as core UX in real estate (clustering, draw-on-map) https://raw.studio/blog/using-maps-as-the-core-ux-in-real-estate-platforms/
11. Redfin — Multiple area search (up to 5 areas, pan refresh) https://support.redfin.com/hc/en-us/articles/360025724771-Multiple-Area-Search

**WordPress roles & capabilities**
12. WordPress.org — Roles and Capabilities (add_role no-op, versioning, least privilege) https://developer.wordpress.org/plugins/users/roles-and-capabilities/
13. WordPress.org — map_meta_cap reference (per-object caps, pass ID) https://developer.wordpress.org/reference/functions/map_meta_cap/
14. Justin Tadlock — Meta capabilities for CPTs https://justintadlock.com/archives/2010/07/10/meta-capabilities-for-custom-post-types
15. Justin Tadlock — Users, roles, and capabilities https://justintadlock.com/archives/2009/08/30/users-roles-and-capabilities-in-wordpress

**AI support agent**
16. ClarityArc — Grounding & citation (sources-or-abstain) https://www.clarityarc.com/insights/ai-hallucination-grounding-citation
17. Anthropic — Reduce hallucinations (quote-first, permission to say "I don't know") https://docs.claude.com/en/docs/test-and-evaluate/strengthen-guardrails/reduce-hallucinations
18. dzlab — Claude guardrails (concise refusals, scope) https://dzlab.github.io/ai/2025/05/12/peeking-under-the-hood-claude/
19. Zendesk — Automated resolutions for AI agents (escalation status, no loop) https://support.zendesk.com/hc/en-us/articles/5352026794010-About-automated-resolutions-for-AI-agents
20. Zendesk — Deflection vs automated resolution https://support.zendesk.com/hc/en-us/articles/8357756478106-Understanding-the-difference-between-deflection-AI-agent-handled-automated-resolution-and-custom-resolution-rates
21. Intercom — Fin automation rate (Involvement × Resolution) https://www.intercom.com/help/en/articles/13533623-fin-ai-agent-automation-rate
22. Fin.ai — 50.8% resolution / 96% involvement at Anthropic https://fin.ai/
23. OpenAI — API prompt caching (≥1,024 tokens, up to 90% cost / 80% latency) https://openai.com/index/api-prompt-caching/
24. OpenAI — API pricing (cached input $2.50→$0.25 per M) https://openai.com/api/pricing/

**Business metrics & ops**
25. forEntrepreneurs (David Skok) — LTV:CAC (>3, payback <12mo, "used not believed") https://www.forentrepreneurs.com/ltv-cac/
26. ChartMogul — NRR (>100% target; ~106% median) https://chartmogul.com/saas-metrics/nrr/
27. ChartMogul — Negative churn (net MRR churn formula; ~40% achieve it) https://chartmogul.com/saas-metrics/negative-churn/
28. ChartMogul — Customer churn (logo vs revenue) https://chartmogul.com/saas-metrics/customer-churn/
29. Lenny's Newsletter — Activation rate (median 25%, SaaS 30%, 7-day window) https://www.lennysnewsletter.com/p/what-is-a-good-activation-rate
30. Baremetrics — SaaS metrics checklist (MRR foundation) https://baremetrics.com/blog/saas-metrics-checklist-kpis-founders-should-track
31. Baremetrics — Recover failed payments (~9% MRR lost; 45–70% recovered) https://baremetrics.com/blog/recover-failed-payments-save-lost-revenue
32. Baremetrics — Dashboards examples (real-time, Slack push) https://baremetrics.com/blog/saas-metrics-dashboards-examples-templates

**Reliability / observability**
33. Google SRE — Monitoring distributed systems (symptom = "what's broken") https://sre.google/sre-book/monitoring-distributed-systems/
34. Google SRE — Practical alerting (alert on symptoms not causes) https://sre.google/sre-book/practical-alerting/
35. Google SRE Workbook — Alerting on SLOs (multi-window multi-burn-rate) https://sre.google/workbook/alerting-on-slos/
36. Sentry — Alerts best practices (severity routing, scrub PII) https://docs.sentry.io/product/alerts/best-practices/
37. Sentry — New monitors & alerts best practices (thresholds, auto-resolve) https://docs.sentry.io/product/new-monitors-and-alerts/alerts/best-practices/
38. BetterStack — Check frequency (30–60s revenue endpoints; heartbeats) https://betterstack.com/docs/uptime/check-frequency/
39. WordPress.org — Debugging in WordPress (WP_DEBUG_LOG bounding) https://developer.wordpress.org/advanced-administration/debug/debug-wordpress/  ·  InMotion — Disable WP-Cron, use server cron https://www.inmotionhosting.com/support/edu/wordpress/disable-the-wp-cron/

*Researched 2026-06-05 via fan-out web search + adversarial verification. Every implementation rule above traces to one of these URLs.*
