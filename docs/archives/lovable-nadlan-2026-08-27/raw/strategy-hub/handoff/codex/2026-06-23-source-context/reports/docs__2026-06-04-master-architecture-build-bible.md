# nad-lan.co.il — Master Architecture & Build Bible (for Codex)
**Date:** 2026-06-04 · **Author:** Claude · **Audience:** Codex (implementer)
**Status:** authoritative. This supersedes the gap-level sketch in
`docs/2026-06-04-codex-implementation-spec.md` for GAP 3 (free path) and adds
full architecture/PLD for every remaining gap.

> Read this once end to end before writing any code. Then re-read the relevant
> gap section before each PR. Every section answers **WHAT / WHY / WHERE / HOW**
> and gives real code, the failure modes, and the QA that proves it.

---

## 0. PRINCIPLES (the operating system of this build)

1. **`paid_tier` is the single source of truth** for ranking + gating. Never
   invent a parallel state. Everything (sort, badge, contact unlock, expiry)
   reads `paid_tier` ∈ {free, pro, premier}.
2. **Idempotence everywhere money flows.** Webhooks and crons fire repeatedly.
   Every handler must produce the same result run 1× or 50×.
3. **Guard re-entry.** Wrap new functions in `if ( ! function_exists() )`.
   Hook callbacks check a flag/cap before doing work.
4. **Degrade, never die.** A missing meta / failed API / deleted card returns a
   clean Hebrew message or a no-op, never a fatal or blank page.
5. **The owner sees, the owner does nothing.** Every automated action writes a
   trace (meta flag / option / ops-dashboard row) so the owner can VERIFY
   without touching code, and intervenes in nothing for daily ops.
6. **Plugin lane only.** All of this lives in `plugins/nadlan-config/`. The
   theme (functions.php, assets/css, patterns) is Claude's lane — do not touch.
7. **One gap = one branch = one version bump = one DRAFT PR.** You never merge.
   Claude reviews, takes the branch, deploys.

### The existing data model you build on (do not break it)
Per-card post meta (CPTs: `nadlan_professional` / `nadlan_project` / `nadlan_property`):
| meta key | meaning | written by |
|---|---|---|
| `paid_tier` | free/pro/premier — ranking + gating truth | tiers.php, advertiser-orders.php |
| `owner_user_id` | the WP user who owns the card | claim.php, studio-rest.php |
| `claim_status` | verified/pending/'' | claim.php |
| `data_quality` | stub/enriched — drives noindex guard | studio, schema.php |
| `campaign_end` | unix ts when paid window ends | advertiser-orders.php |
| `paid_order_id` / `paid_product_id` | the Woo order/product that paid | advertiser-orders.php |
| `lat` / `lng` | geo pin | studio.php |
| `city` / `address` / `classification` / `registry_number` | facts | import/studio |

REST surface (namespace `nadlan/v1`): `/lead`, `/directory`, `/projects`,
`/studio/*`, `/concierge`, `/referral/*`, `/healthcheck`, `/owner/*`.
Cron: `nadlan_ao_daily_downgrade` (daily, safety-net downgrade).

---

## 1. GAP 2 — Lead Inbox & Notification System  ·  v1.42.9
### The shallow version (email the owner) is NOT enough. Build the real thing.

### WHAT
A paying advertiser must (a) get notified the instant a lead lands on their
card, (b) see ALL their leads in one place inside the Advertiser Center, and
(c) the system must record delivery so the advertiser trusts it works.

### WHY
The whole value of Pro/Premier is "get customers." Today
`conversion-cta.php:109` stores `lead_card_id` but only emails the site admin.
The advertiser pays and sees nothing → churn. This closes the VALUE journey.

### WHERE
- `plugins/nadlan-config/inc/conversion-cta.php` (the /lead REST handler)
- `plugins/nadlan-config/inc/advertiser-center.php` (the "my leads" panel)
- new helper file `plugins/nadlan-config/inc/lead-routing.php` (clean boundary)

### ARCHITECTURE (3 layers)
```
[ lead submitted ]  →  conversion-cta /lead REST
        │ stores nadlan_lead post + lead_card_id meta (EXISTS)
        ▼
[ Layer 1: routing ]  lead-routing.php::nadlan_lead_route($lead_id,$card_id)
        │ resolves owner_user_id + paid_tier of the card
        │ if tier∈(pro,premier) AND owner≠requester → deliver + log
        ▼
[ Layer 2: delivery ]  email now; (later) WhatsApp/SMS via filter hook
        │ wp_mail + update meta lead_routed_to_owner=1, lead_routed_at=ts
        ▼
[ Layer 3: surface ]  advertiser-center "הפניות שקיבלתי" panel
        │ WP_Query nadlan_lead where lead_card_id IN (my cards)
        │ shows name/phone/date + delivery status badge
```

### HOW — the code

**`inc/lead-routing.php`** (new; add to the module loader array in nadlan-config.php):
```php
<?php
if ( ! defined( 'ABSPATH' ) ) { exit; }
/* GAP 2 — route a captured lead to the paying card owner + log delivery. */
if ( ! function_exists( 'nadlan_lead_route' ) ) {
	function nadlan_lead_route( $lead_id, $card_id, $fields ) {
		$lead_id = (int) $lead_id; $card_id = (int) $card_id;
		if ( ! $lead_id || ! $card_id ) { return; }
		if ( get_post_meta( $lead_id, 'lead_routed_to_owner', true ) ) { return; } // idempotent

		$owner = (int) get_post_meta( $card_id, 'owner_user_id', true );
		$tier  = (string) get_post_meta( $card_id, 'paid_tier', true );
		if ( $owner < 1 || ! in_array( $tier, array( 'pro', 'premier' ), true ) ) { return; }
		if ( $owner === get_current_user_id() ) { return; }            // self-test guard

		$u = get_userdata( $owner );
		if ( ! $u || ! is_email( $u->user_email ) ) { return; }

		$title = get_the_title( $card_id );
		$body  = "התקבלה פנייה חדשה לכרטיס שלך: {$title}\n\n";
		$body .= 'שם: ' . ( $fields['name'] ?? '' ) . "\n";
		$body .= ! empty( $fields['phone'] ) ? 'טלפון: ' . $fields['phone'] . "\n" : '';
		$body .= ! empty( $fields['email'] ) ? 'אימייל: ' . $fields['email'] . "\n" : '';
		$body .= ! empty( $fields['message'] ) ? "הודעה: " . $fields['message'] . "\n" : '';
		$body .= "\nאפשר לחזור ללקוח ישירות. לצפייה בכל הפניות: " . home_url( '/advertiser-center/' );

		// allow future channels (WhatsApp/SMS) to also deliver
		$delivered = apply_filters( 'nadlan_lead_deliver', false, $owner, $lead_id, $card_id, $body );
		if ( ! $delivered ) {
			$delivered = wp_mail( $u->user_email, 'פנייה חדשה לכרטיס שלך · נדל״ן חכם', $body );
		}
		update_post_meta( $lead_id, 'lead_routed_to_owner', $delivered ? 1 : 0 );
		update_post_meta( $lead_id, 'lead_routed_at', time() );
	}
}
```
Call it from the END of the `/lead` REST callback in `conversion-cta.php`
(after `update_post_meta($lid,'lead_card_id',$card_id)`):
```php
if ( $card_id && function_exists( 'nadlan_lead_route' ) ) {
	nadlan_lead_route( $lid, $card_id, array(
		'name'=>$name,'phone'=>$phone,'email'=>$email,'message'=>$msg,
	) );
}
```

**Advertiser Center panel** (`inc/advertiser-center.php`, inside the render):
```php
// "הפניות שקיבלתי" — leads on cards this user owns
$my_cards = get_posts(array('post_type'=>array('nadlan_professional','nadlan_project','nadlan_property'),
  'meta_key'=>'owner_user_id','meta_value'=>get_current_user_id(),'fields'=>'ids','posts_per_page'=>100));
if ($my_cards) {
  $leads = get_posts(array('post_type'=>'nadlan_lead','post_status'=>'private','posts_per_page'=>50,
    'meta_query'=>array(array('key'=>'lead_card_id','value'=>$my_cards,'compare'=>'IN'))));
  // render name / phone / date / "נמסר" badge per lead
}
```

### CYCLES 1-10 (what "deep" means here)
- C1 happy path email · C2 idempotent (lead_routed flag) · C3 escape all output,
  no PII leak to non-owners · C4 deleted user / free card / self-lead all no-op
  · C5 lead_routed_at trace + ops-dashboard count · C6 fires automatically on
  every /lead · C7 Hebrew email per copywriting-skill (no "ליד", no em-dash) ·
  C8 walk advertiser journey: pay→lead lands→email→see in center · C9 curl
  proof below · C10 harden: rate-limit so a spammer can't blast the owner's
  inbox (reuse the existing /lead 8/hr limit).

### QA
```bash
curl -s -k -X POST https://nad-lan.co.il/wp-json/nadlan/v1/lead -H 'Content-Type: application/json' \
 -d '{"name":"בודק","phone":"0500000000","card_id":<PRO_CARD_ID>,"goal":"בדיקה"}'
# → owner of PRO_CARD_ID receives email <60s; lead_routed_to_owner=1; appears in /advertiser-center/
# → same on a FREE card = owner gets NOTHING (admin only)
```

---

## 2. GAP 3 — TRUE AUTO-RENEW, **FREE** (Green Invoice recurring)  ·  v1.43.0
### Owner decision: Option B (true auto-renew), FREE path (no WC Subscriptions).

### WHAT
A Pro/Premier advertiser is charged automatically every cycle (monthly etc.)
with zero owner action and zero paid plugins, using **Green Invoice/Morning's
native recurring charges (הוראות קבע)**. The tier stays active while the
standing order is alive; it downgrades when the standing order stops/fails.

### WHY (and why this beats the $199 plugin)
The Morning gateway's recurring support is tied to the paid WooCommerce
Subscriptions extension. But Morning **itself** has native recurring standing
orders (הוראות קבע) — 6 documented operations: create a recurring charge link,
recurring for saved customers, edit, replace card, stop. So we bridge Morning's
OWN recurring engine and skip the plugin entirely. **Cost: ₪0.**
Sources: greeninvoice.co.il/help-center/digital-payments/recurring-charges/ ·
API: greeninvoice.co.il/api-docs/ · greeninvoice.docs.apiary.io/

### ARCHITECTURE — the bridge pattern
```
ADVERTISER                      OUR PLUGIN                     GREEN INVOICE (Morning)
   │ clicks "מנוי Pro" on /join-pro/                                     │
   │──────────────► nadlan_gi_start_subscription($card_id,$tier)         │
   │                     │ create/lookup GI recurring-charge link       │
   │                     │  (API: POST /payments/form OR a pre-made     │
   │                     │   recurring link per tier, carrying card_id  │
   │                     │   as a custom reference)                     │
   │◄────────────────────┴───────────────────────────────────────────► │ hosted recurring page
   │ enters card once, approves standing order ──────────────────────► │ creates standing order
   │                                                                     │ auto-charges each cycle
   │                          ◄── IPN webhook on EVERY successful charge │
   │                  /nadlan/v1/gi-ipn  (verify signature)             │
   │                     │ extend campaign_end + keep paid_tier         │
   │                     │ log charge in ops-dashboard                  │
   │                          ◄── IPN on cancel / failure ───────────── │
   │                     │ set paid_tier=free (downgrade)               │
   ▼                                                                     ▼
[ reconciliation cron — safety net ] nadlan_gi_reconcile (daily)
   queries GI API for each active subscription_ref; corrects drift if an
   IPN was missed.
```

### Two implementation tiers (build A first, then B if owner wants tighter UX)
**Tier A — recurring-charge LINK + IPN (simplest, fully free, fastest):**
- Owner creates ONE recurring-charge link per tier in the Morning dashboard
  (Pro monthly ₪349, Premier ₪749, …), each with a webhook/IPN URL pointing at
  our endpoint. Store the link URLs in plugin options
  (`nadlan_gi_link_pro`, `nadlan_gi_link_premier`, …).
- "מנוי" button on /join-pro/ → our route appends `?ref=card_<id>_user_<uid>`
  → redirects to the GI link.
- GI manages the auto-renew. On each charge it POSTs our IPN.

**Tier B — API-created standing order (premium UX, stays on-site):**
- Use the GI API to create the standing order server-side with the saved token,
  so the advertiser never leaves the site. Requires GI API key (owner has the
  Morning account). Endpoints per their api-docs: account auth → create
  payment / recurring. Keep the same IPN + reconciliation.

### HOW — the code (Tier A core)

**`inc/greeninvoice-recurring.php`** (new module):
```php
<?php
if ( ! defined( 'ABSPATH' ) ) { exit; }
/* GAP 3 — FREE auto-renew bridge to Morning/Green-Invoice standing orders. */

/* 1) tier → recurring-link option + product mapping */
if ( ! function_exists( 'nadlan_gi_tier_link' ) ) {
	function nadlan_gi_tier_link( $tier ) {
		return (string) get_option( 'nadlan_gi_link_' . $tier, '' ); // set in admin
	}
}

/* 2) start: /studio or /join-pro CTA → record intent + bounce to GI link */
add_action( 'init', function () {
	if ( empty( $_GET['nadlan_subscribe'] ) ) { return; }
	$tier = sanitize_key( $_GET['nadlan_subscribe'] );          // pro|premier
	$card = (int) ( $_GET['card_id'] ?? 0 );
	if ( ! is_user_logged_in() ) { wp_safe_redirect( wp_login_url( add_query_arg( $_GET, home_url() ) ) ); exit; }
	$link = nadlan_gi_tier_link( $tier );
	if ( ! $link || ! $card ) { wp_safe_redirect( home_url( '/join-pro/?err=1' ) ); exit; }
	// carry our reference so the IPN can map the charge back to the card+user
	$ref = 'card_' . $card . '_user_' . get_current_user_id() . '_tier_' . $tier;
	update_post_meta( $card, 'gi_pending_ref', $ref );
	wp_safe_redirect( add_query_arg( array( 'external_id' => $ref ), $link ) );
	exit;
}, 1 );

/* 3) IPN endpoint — Green Invoice calls this on every charge / cancel */
add_action( 'rest_api_init', function () {
	register_rest_route( 'nadlan/v1', '/gi-ipn', array(
		'methods'             => 'POST',
		'permission_callback' => '__return_true',     // verified by shared secret below
		'callback'            => 'nadlan_gi_ipn_handler',
	) );
} );

if ( ! function_exists( 'nadlan_gi_ipn_handler' ) ) {
	function nadlan_gi_ipn_handler( $req ) {
		// SECURITY: verify a shared secret OR GI signature header
		$secret = (string) get_option( 'nadlan_gi_ipn_secret', '' );
		$got    = (string) ( $req->get_header( 'x-nadlan-secret' ) ?: ( $req->get_param( 'secret' ) ?? '' ) );
		if ( ! $secret || ! hash_equals( $secret, $got ) ) {
			return new WP_Error( 'forbidden', 'forbidden', array( 'status' => 403 ) );
		}
		$p      = $req->get_json_params() ?: $req->get_params();
		$ref    = sanitize_text_field( (string) ( $p['external_id'] ?? $p['ref'] ?? '' ) );
		$event  = sanitize_key( (string) ( $p['event'] ?? $p['status'] ?? '' ) ); // paid|charged|failed|cancelled
		if ( ! preg_match( '/card_(\d+)_user_(\d+)_tier_(\w+)/', $ref, $m ) ) {
			return array( 'ok' => false, 'reason' => 'bad_ref' );
		}
		$card = (int) $m[1]; $tier = $m[3];
		$ok_events   = array( 'paid', 'charged', 'success', 'active' );
		$bad_events  = array( 'failed', 'cancelled', 'stopped', 'expired' );

		if ( in_array( $event, $ok_events, true ) ) {
			// IDEMPOTENT: extend the window; same charge twice = same end date band
			$cycle_days = (int) apply_filters( 'nadlan_gi_cycle_days', 31, $tier );
			$start = max( time(), (int) get_post_meta( $card, 'campaign_end', true ) );
			update_post_meta( $card, 'paid_tier', in_array( $tier, array('pro','premier'), true ) ? $tier : 'free' );
			update_post_meta( $card, 'campaign_end', $start + $cycle_days * DAY_IN_SECONDS );
			update_post_meta( $card, 'gi_subscription_active', 1 );
			nadlan_gi_log( $card, 'charge', $p );          // ops trace
		} elseif ( in_array( $event, $bad_events, true ) ) {
			update_post_meta( $card, 'gi_subscription_active', 0 );
			update_post_meta( $card, 'paid_tier', 'free' );
			nadlan_gi_log( $card, $event, $p );
		}
		return array( 'ok' => true );
	}
}

/* 4) ops trace so the owner can SEE every charge without code */
if ( ! function_exists( 'nadlan_gi_log' ) ) {
	function nadlan_gi_log( $card, $event, $payload ) {
		$log = get_option( 'nadlan_gi_charge_log', array() );
		array_unshift( $log, array( 't'=>time(), 'card'=>$card, 'event'=>$event,
			'amount'=>$payload['amount'] ?? '', 'ref'=>$payload['external_id'] ?? '' ) );
		update_option( 'nadlan_gi_charge_log', array_slice( $log, 0, 500 ) );
	}
}
```

**Reconciliation cron** (safety net — the existing `nadlan_ao_daily_downgrade`
already downgrades when `campaign_end < now`; KEEP it. Add a second daily job
that, for cards with `gi_subscription_active=1` whose `campaign_end` is within
2 days, optionally pings the GI API to confirm the standing order is alive.)

### EDGE CASES YOU MUST HANDLE (C4)
- Duplicate IPN for the same charge → idempotent extend (band by cycle).
- IPN arrives for a deleted card → no-op, log a warning.
- Advertiser changes card in GI → GI keeps charging, IPN keeps coming, tier stays.
- Charge fails once then succeeds (retry) → first IPN downgrades, second
  re-activates. Acceptable; or add a 24h grace before downgrade on first fail.
- Owner stops the standing order in GI → cancel IPN → downgrade.
- No IPN ever arrives (misconfig) → reconciliation cron + the existing
  campaign_end downgrade catch it. The system never charges silently with no
  tier, and never gives tier with no charge.

### SECURITY (C3)
- IPN verified by a shared secret (`nadlan_gi_ipn_secret`, set in admin, sent in
  header or query). Reject anything else with 403.
- Never trust the amount/tier from the IPN alone for what tier to grant — derive
  tier from OUR `external_id` ref (which we created), not from GI's free-text.

### ADMIN (C5) — `inc/greeninvoice-recurring.php` settings page
A settings page under NadLan: fields for the 3 recurring-link URLs + the IPN
secret + a read-only table of the last 50 charges from `nadlan_gi_charge_log`.
This is the owner's "money is flowing" window — zero code to read it.

### CYCLES 1-10 here
C1 link+redirect works · C2 IPN idempotent · C3 secret-verified IPN · C4 the 6
edge cases above · C5 charge-log admin table · C6 fully automatic (GI charges,
IPN extends, cron safety-net) · C7 premium /join-pro "מנוי" button + Hebrew
copy · C8 full MONEY journey: subscribe→charge→renew→fail→downgrade→resubscribe
· C9 simulated-IPN curl proof below · C10 harden: replay protection (store last
charge id, ignore dup), and a "test IPN" button in admin.

### QA (simulate an IPN without a real card)
```bash
SECRET=$(your admin secret)
curl -s -k -X POST https://nad-lan.co.il/wp-json/nadlan/v1/gi-ipn \
 -H "x-nadlan-secret: $SECRET" -H 'Content-Type: application/json' \
 -d '{"external_id":"card_4464_user_1_tier_premier","event":"paid","amount":749}'
# → card 4464 paid_tier=premier, campaign_end +31d, gi_subscription_active=1, log row
curl ... -d '{"external_id":"card_4464_user_1_tier_premier","event":"cancelled"}'
# → card 4464 paid_tier=free, active=0
# replay the "paid" IPN 5× → end date advances by ONE band, not five.
```

### ⚠️ OWNER PREREQUISITES (Codex: confirm before final wiring, but you CAN
### build + test the IPN/cron side now with simulated IPNs)
1. Owner creates the recurring-charge links in the Morning dashboard (one per
   tier) and sets the IPN/webhook URL to `/wp-json/nadlan/v1/gi-ipn`.
2. Owner sets the 3 link URLs + the IPN secret in the new admin page.
3. Confirm per-tier cycle (monthly Pro/Premier?). Default 31 days.

---

## 3. GAP 4 — OpenAI agent (provider-agnostic AI)  ·  v1.43.1
### WHAT/WHY: the concierge + AI copy are wired to Anthropic; owner has OpenAI.
Make AI provider-agnostic, default OpenAI, keep RAG + lead capture, add cost
guards + graceful failure. This is the foundation for the "talking avatar"
vision later (text agent first, voice/video later).

### ARCHITECTURE
```
[ widget / REST /concierge ] → nadlan_ai_chat($system,$messages)
   ├─ provider switch (option nadlan_ai_provider, default openai)
   ├─ RAG: retrieve top-k from glossary+directory (EXISTS in ai-concierge)
   ├─ cost guard: per-IP daily token cap (transient), refuse over cap
   ├─ openai → POST api.openai.com/v1/chat/completions (gpt-4o-mini)
   └─ degrade: missing key → "השירות אינו זמין כרגע", logged, never fatal
```
Full `nadlan_ai_chat()` adapter code is in
`docs/2026-06-04-codex-implementation-spec.md` §GAP 4. Extend it with:
- `nadlan_ai_guard($ip)` daily token cap (transient) before the call.
- streaming optional (later); for now a single response is fine.
- settings page: provider radio + `nadlan_ai_openai_key` + a usage/cost counter.
QA: curl `/nadlan/v1/concierge` returns Hebrew answer, request hits openai.com,
missing key degrades cleanly.

---

## 4. GAP 5 — Geo-radius search  ·  v1.43.2
### WHAT/WHY: lat/lng stored + mapped, but no "near me." Add Haversine geo_query.
### ARCHITECTURE
```
[ "קרוב אליי" button ] → navigator.geolocation → /nadlan/v1/directory?lat&lng&radius_km
   → directory.php REST reads params → wraps WP_Query with posts_clauses
     (Haversine INNER JOIN lat/lng, HAVING distance<=radius, ORDER BY distance)
   → default radius 5km; no params → identical to today
```
Full `inc/geo-search.php` Haversine code is in the spec §GAP 5
(adapted from github.com/birgire/geo-query, MIT). Deepen with:
- a `_geo_indexed` numeric copy of lat/lng if string-meta perf is poor (C2),
- distance returned per card + shown as "2.4 ק״מ ממך" (C7),
- exclude cards with empty lat/lng cleanly (C4).
QA: curl with TLV coords returns nearest-first; without coords unchanged.

---

## 5. GAP 6 — Roles & capabilities  ·  v1.43.3
### WHAT/WHY: only admin vs owner. Add real roles for zero-touch delegation.
### ARCHITECTURE — capability matrix
```
role               caps
nadlan_advertiser  read, nadlan_edit_own_card, nadlan_upload_own_media
nadlan_manager     read, + nadlan_moderate_reviews, nadlan_reassign_card,
                   nadlan_run_imports
administrator      gets all nadlan_* caps too (so nothing breaks)
```
Replace blunt `manage_options` gates with cap checks (keep owner-match for
non-admins). Full `inc/roles.php` code in the spec §GAP 6. Deepen with:
- a one-time migration that assigns `nadlan_advertiser` to existing users who
  own ≥1 card (C2/C6),
- deactivation cleanly removes the custom roles (C10),
- an admin "team" page to grant nadlan_manager to a user (C7).
QA: per-role matrix in the spec — advertiser 403s on foreign cards, manager
can't change billing, admin unchanged.

---

## 6. CROSS-CUTTING — the owner's autopilot dashboard
Add to `inc/ops-dashboard.php` a single "Autopilot" panel that surfaces, with
zero code, that the business is running:
- active subscriptions count + last 10 charges (from `nadlan_gi_charge_log`)
- leads routed in last 7d (count of `lead_routed_to_owner=1`)
- tier distribution (free/pro/premier counts)
- AI concierge usage + cost this month
- any reconciliation drift the cron corrected
This is the proof that "everything is automatic, owner does nothing."

---

## 7. THE 10-CYCLE METHOD (apply to every gap; write it in each QA doc)
C1 foundation · C2 idempotence · C3 security+authority · C4 edge cases ·
C5 observability/trace · C6 automation/zero-touch · C7 premium UX+Hebrew copy ·
C8 full-journey walk · C9 deterministic QA proof · C10 adversarial hardening.
A PR that didn't visibly do all 10 is not done.

## 8. DELIVERY discipline (unchanged, non-negotiable)
One gap → branch `codex/gapN-<slug>` off fresh origin/main → 10 cycles →
php -l clean → ZIP (forward slashes) + version bump (header + healthcheck +
manifest) → docs/qa/...gapN.md with all 10 cycles + the curl/WP-CLI proof →
DRAFT PR, tag Claude, STOP. Claude reviews vs the e2e QA script, takes the
branch, deploys. You never merge. You never touch the theme.

Build order: GAP 2 → GAP 4 → GAP 5 → GAP 6 → GAP 3 (GAP 3 IPN/cron can be built
+ simulated now; final wiring waits on the owner creating the Morning links).

