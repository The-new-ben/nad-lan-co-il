# nad-lan.co.il — Full Implementation Spec for Codex
**Date:** 2026-06-04 · **Author:** Claude · **Status:** build-ready (do NOT skip the rules section)

> This is the exact build guide for the 6 gaps in `docs/2026-06-04-system-readiness-gap-map.html`.
> Every gap has: the problem (cited), the file/path, the real code to write, and the QA that proves it.
> **One gap = one PR = one version bump.** Never bundle.

---

## 0. GROUND RULES (violating these = rejected PR)

- **Branch:** off fresh `origin/main` per gap, named `codex/gap-N-<slug>`.
- **Lane:** PLUGIN only (`plugins/nadlan-config/`). Do NOT touch the theme
  (`functions.php`, `assets/css/*`, `patterns/*`) — that is Claude's lane.
- **Lint:** `php -l` clean on every changed file. If no PHP CLI on your box,
  say so and Claude lints before merge — do not claim a lint you didn't run.
- **ZIP:** rebuild with `zip -r` (forward slashes). NEVER `tar.exe`
  (Windows backslashes broke extraction in 1.41.2).
- **Version:** bump BOTH `plugins/nadlan-config/nadlan-config.php` header
  `Version:` AND the `'version'` string in the healthcheck response, AND
  `plugin-dist/nadlan-config.json`, AND build `plugin-dist/nadlan-config-X.Y.Z.zip`.
- **Copy:** any Hebrew user-facing string must pass `skills/copywriting-skill.md`
  §3 (no AI-tells) and §4 (no internal words: ליד/CRM/hub/spoke/intent/…).
  No em-dash (—) in public copy. CTAs from the §6 allowed list only.
- **PR:** open as DRAFT, tag Claude, list the exact curl/JS that proves it works.
- **Idempotence/guards:** every meta write that money depends on must be safe to
  run twice (renewals fire repeatedly).

Current live baseline: plugin **1.42.7**, Woo coming-soon OFF, 4 SKUs
(476 Pro/₪349, 477 Premier/₪749, 489 project/₪3990, 490 property/₪299), Morning
gateway (card/Bit/GPay/Apple) enabled. Ownership model: `owner_user_id` meta +
`current_user_can('manage_options')`. Tier source of truth: `paid_tier` meta
∈ {free,pro,premier}.

---

## GAP 1 — Paid placement boost  ·  v1.42.8  ·  ~1 hr  ·  REVENUE-CRITICAL

### Problem (cited)
`inc/directory.php:83` and `:568` — the `featured` sort orders by
`menu_order ASC, date DESC` and **never reads `paid_tier`**.
`inc/advertiser-orders.php` writes **0** `menu_order`. So paying for Pro/Premier
gives a badge but the SAME position. The thing the advertiser pays for is dead.

### The fix
Add a `posts_clauses` filter that ranks premier > pro > free, then by date,
and apply it on BOTH the professionals query and the projects query when
`sort=featured` (the default).

**File:** `plugins/nadlan-config/inc/directory.php`

```php
/* ---- paid-tier ranking (GAP 1) -------------------------------------------
 * Premier floats above Pro above free, then newest. Wired into the 'featured'
 * sort (the default) for both the professionals and projects directories.
 * Uses a transient-safe LEFT JOIN so cards with no paid_tier meta still appear.
 * ------------------------------------------------------------------------- */
if ( ! function_exists( 'nadlan_dir_tier_rank_clauses' ) ) {
	function nadlan_dir_tier_rank_clauses( $clauses ) {
		global $wpdb;
		// join the paid_tier meta (aliased so we never collide with meta_query joins)
		$clauses['join'] .= " LEFT JOIN {$wpdb->postmeta} nlt
			ON nlt.post_id = {$wpdb->posts}.ID AND nlt.meta_key = 'paid_tier' ";
		// FIELD() returns 0 for non-matches; DESC puts premier(2)>pro(1)>free/null(0)
		$rank = "FIELD(nlt.meta_value,'premier','pro')";
		$clauses['orderby'] = " {$rank} DESC, {$wpdb->posts}.menu_order ASC, {$wpdb->posts}.post_date DESC ";
		// LEFT JOIN can duplicate rows; force distinct
		$clauses['groupby'] = "{$wpdb->posts}.ID";
		return $clauses;
	}
}
```

Then in `nadlan_dir_query()` (around line 79-85) replace the `featured` branch:

```php
case 'featured':
default:
	add_filter( 'posts_clauses', 'nadlan_dir_tier_rank_clauses' );
	$wq = new WP_Query( $args );          // run WITH the filter
	remove_filter( 'posts_clauses', 'nadlan_dir_tier_rank_clauses' );
	return $wq;
```
> NOTE: because the filter must wrap only THIS query, add+remove around the
> `new WP_Query`. Do the identical change in the PROJECTS query
> (`nadlan_dir_project_query`, ~line 560-570).

### QA (prove it)
```bash
# premier project must rank before a newer free project
curl -s -k "https://nad-lan.co.il/wp-json/nadlan/v1/projects?sort=featured&per_page=12" \
 | python3 -c "import sys,json;d=json.load(sys.stdin);print(d['html'][:600])"
```
- ✅ The known premier card (Rainbow, id 4464) appears in the first row.
- ✅ A free card with a newer date does NOT outrank it.
- ✅ `/professionals/` same: set one pro card, confirm it floats to top-6.
- 🛑 No SQL error in PHP log; card count unchanged (groupby prevents dupes).

---

## GAP 2 — Lead reaches the advertiser  ·  v1.42.9  ·  ~2 hr  ·  VALUE

### Problem (cited)
`inc/conversion-cta.php:109` stores `lead_card_id` but only `wp_mail()`s the
site admin (`:110-115`). A paying Pro/Premier advertiser never receives the
lead from their own card → they pay and see nothing.

### The fix
**File:** `plugins/nadlan-config/inc/conversion-cta.php` — right AFTER the
`if ( $card_id ) { update_post_meta( $lid, 'lead_card_id', $card_id ); }` line
and the existing admin email:

```php
/* GAP 2: route the lead to the paying card owner (pro/premier only). */
if ( $card_id ) {
	$owner_id = (int) get_post_meta( $card_id, 'owner_user_id', true );
	$tier     = (string) get_post_meta( $card_id, 'paid_tier', true );
	$requester = get_current_user_id();
	if ( $owner_id > 0
		&& $owner_id !== $requester                     // don't email yourself
		&& in_array( $tier, array( 'pro', 'premier' ), true ) ) {
		$owner = get_userdata( $owner_id );
		if ( $owner && is_email( $owner->user_email ) ) {
			$card_title = get_the_title( $card_id );
			$body  = "התקבלה פנייה חדשה לכרטיס שלך: {$card_title}\n\n";
			$body .= "שם: {$name}\n";
			$body .= $phone ? "טלפון: {$phone}\n" : '';
			$body .= $email ? "אימייל: {$email}\n" : '';
			$body .= $msg   ? "הודעה: {$msg}\n"   : '';
			$body .= "\nאפשר לחזור ללקוח ישירות. בהצלחה!";
			wp_mail( $owner->user_email, 'פנייה חדשה לכרטיס שלך · נדל״ן חכם', $body );
			update_post_meta( $lid, 'lead_routed_to_owner', 1 );
		}
	}
}
```
> Copy check: no "ליד"/"lead" word in the email (uses "פנייה"), no em-dash,
> Hebrew only. Passes copywriting-skill §4.

### QA
```bash
# as a logged-out visitor, submit a lead against a pro card you control
curl -s -k -X POST "https://nad-lan.co.il/wp-json/nadlan/v1/lead" \
 -H "Content-Type: application/json" \
 -d '{"name":"בודק","phone":"0500000000","card_id":<PRO_CARD_ID>,"goal":"בדיקה"}'
```
- ✅ The card's owner (a test user, tier=pro) receives the email within 60s.
- ✅ `lead_routed_to_owner=1` meta set on the lead.
- ✅ A lead on a FREE card → owner gets NOTHING (only admin). 
- 🛑 No email to owner if requester == owner (self-test guard).

---

## GAP 3 — True auto-renew subscriptions  ·  v1.43.0  ·  1-2 d  ·  REVENUE-CRITICAL
### ⚠️ BLOCKED until owner installs the official **WooCommerce Subscriptions** (~$199/yr). Do not start before it's active.

### Problem (cited)
`inc/advertiser-orders.php:103` activates on the one-time
`woocommerce_payment_complete`, sets `campaign_end`, and a daily cron
(`:154 nadlan_ao_daily_downgrade`) downgrades. No recurring charge → revenue
leaks every cycle. Owner decision: **Option B, true auto-renew**
(see `docs/2026-06-04-gap3-recurring-decision.md`). Morning gateway supports
WC Subscriptions + token renewal (changelog v1.6.0/2.3.5/2.3.6).

### The fix (3 parts)

**Part A — products → subscriptions (in wp-admin, document it):**
Convert 476/477 to `subscription` products, billing period = month, with a
1-month free trial on 476 (preserves the "חודש ראשון חינם"). 489/490 keep their
term or become 6-month/2-month renewing per owner. Record the resulting product
IDs (they may stay the same).

**Part B — activation via subscription lifecycle, not one-time payment:**
**File:** `plugins/nadlan-config/inc/advertiser-orders.php`

```php
/* GAP 3: subscription lifecycle is the source of truth for paid_tier.
 * Keep woocommerce_payment_complete for NON-subscription products (489/490 if
 * left as one-time), but for subscription products the status hooks drive it. */
add_action( 'woocommerce_subscription_status_active',    'nadlan_sub_activate', 20 );
add_action( 'woocommerce_subscription_status_pending-cancel', 'nadlan_sub_keep', 20 ); // grace
add_action( 'woocommerce_subscription_status_expired',   'nadlan_sub_downgrade', 20 );
add_action( 'woocommerce_subscription_status_cancelled', 'nadlan_sub_downgrade', 20 );
add_action( 'woocommerce_subscription_status_on-hold',   'nadlan_sub_downgrade', 20 ); // failed renewal

if ( ! function_exists( 'nadlan_sub_activate' ) ) {
	function nadlan_sub_activate( $subscription ) {
		foreach ( $subscription->get_items() as $item ) {
			$pid = $item->get_product_id();
			$map = nadlan_ao_product_map();              // existing 476=>pro etc.
			if ( empty( $map[ $pid ] ) ) { continue; }
			$card_id = (int) $subscription->get_meta( 'card_id' );  // carried from cart
			if ( ! $card_id ) { continue; }
			update_post_meta( $card_id, 'paid_tier', $map[ $pid ]['tier'] );
			// next-payment date becomes campaign_end (safety-net cron still honors it)
			$next = $subscription->get_date( 'next_payment' ) ?: $subscription->get_date( 'end' );
			update_post_meta( $card_id, 'campaign_end', $next ? strtotime( $next ) : 0 );
			update_post_meta( $card_id, 'subscription_id', $subscription->get_id() );
			do_action( 'nadlan_advertiser_paid_tier_activated', $card_id, $subscription, $item, $next );
		}
	}
}
if ( ! function_exists( 'nadlan_sub_downgrade' ) ) {
	function nadlan_sub_downgrade( $subscription ) {
		foreach ( $subscription->get_items() as $item ) {
			$card_id = (int) $subscription->get_meta( 'card_id' );
			if ( $card_id ) {
				update_post_meta( $card_id, 'paid_tier', 'free' );
				do_action( 'nadlan_advertiser_paid_tier_expired', $card_id );
			}
		}
	}
}
if ( ! function_exists( 'nadlan_sub_keep' ) ) { function nadlan_sub_keep( $s ) {} }
```

**Part C — idempotence + safety net:**
- Renewals call `nadlan_sub_activate` again each cycle → fine (it just re-sets
  the same tier + new campaign_end). No double-charge logic needed; Subscriptions
  handles charging.
- KEEP the existing `nadlan_ao_daily_downgrade` cron as a backstop for any
  missed webhook, but it already only downgrades when `campaign_end < now`.
- Carry `card_id` from the add-to-cart link onto the subscription:
  in the existing cart-item → order-meta code, also copy to the subscription via
  `woocommerce_checkout_subscription_created` ($subscription->update_meta_data('card_id',...)).

**Part D — Advertiser Center:** add subscription status + next-billing date +
a "ניהול המנוי" link to `/my-account/subscriptions/` in
`inc/advertiser-center.php`.

### QA (full recurring cycle — must pass before outreach)
- Buy 476 as subscription → `paid_tier=pro`, subscription active, next_payment set.
- Force a renewal: `wp wcs_renewal_create <sub_id>` or admin "Process renewal" →
  tier STAYS pro, a new renewal order appears, no downgrade.
- Cancel → at period end `paid_tier` flips to free.
- Failed renewal (on-hold) → downgrade fires.
- `docs/2026-06-04-e2e-revenue-qa-script.md` Part 2 extended with these.

---

## GAP 4 — OpenAI adapter for AI concierge  ·  v1.43.1  ·  ~½ d

### Problem (cited)
`inc/ai-concierge.php:184` posts to `api.anthropic.com`, model
`claude-haiku-4-5`, key option `nadlan_ai_anthropic_key`. `inc/ai-features.php:58`
same. **0 OpenAI references.** Owner has OpenAI, not Anthropic → the concierge +
AI copy assist are dead.

### The fix
**File:** `plugins/nadlan-config/inc/ai-concierge.php` — abstract the request.

```php
/* GAP 4: provider-agnostic AI call. Default OpenAI (owner's key). */
if ( ! function_exists( 'nadlan_ai_provider' ) ) {
	function nadlan_ai_provider() {
		return (string) get_option( 'nadlan_ai_provider', 'openai' ); // openai|anthropic
	}
}
if ( ! function_exists( 'nadlan_ai_chat' ) ) {
	/** @param array $messages [{role,content},...]  @return string|WP_Error */
	function nadlan_ai_chat( $system, $messages, $max_tokens = 600 ) {
		if ( nadlan_ai_provider() === 'openai' ) {
			$key = (string) get_option( 'nadlan_ai_openai_key', '' );
			if ( ! $key ) { return new WP_Error( 'nokey', 'OpenAI key missing' ); }
			$payload = array(
				'model'      => apply_filters( 'nadlan_ai_openai_model', 'gpt-4o-mini' ),
				'max_tokens' => $max_tokens,
				'messages'   => array_merge(
					array( array( 'role' => 'system', 'content' => $system ) ),
					$messages
				),
			);
			$resp = wp_remote_post( 'https://api.openai.com/v1/chat/completions', array(
				'timeout' => 30,
				'headers' => array(
					'Authorization' => 'Bearer ' . $key,
					'Content-Type'  => 'application/json',
				),
				'body' => wp_json_encode( $payload ),
			) );
			if ( is_wp_error( $resp ) ) { return $resp; }
			$j = json_decode( wp_remote_retrieve_body( $resp ), true );
			return $j['choices'][0]['message']['content'] ?? new WP_Error( 'bad', 'no content' );
		}
		// anthropic fallback (existing path) — keep working for completeness
		return nadlan_ai_chat_anthropic( $system, $messages, $max_tokens );
	}
}
```
Then refactor the existing concierge handler + `ai-features.php` to call
`nadlan_ai_chat()` instead of the hard-coded Anthropic POST. Add to the settings
page (`ai-concierge.php:244-265`): a provider radio + an `nadlan_ai_openai_key`
field next to the existing Anthropic field. Default new installs to `openai`.

### QA
```bash
# set provider=openai + key in wp-admin, then:
curl -s -k -X POST "https://nad-lan.co.il/wp-json/nadlan/v1/concierge" \
 -H "Content-Type: application/json" -d '{"message":"מתי כדאי לקחת עו״ד מקרקעין?"}'
```
- ✅ Returns a Hebrew answer. PHP log shows request to `api.openai.com`.
- ✅ With provider=anthropic + that key, still works (no regression).
- 🛑 Missing key → graceful "השירות אינו זמין כרגע", not a fatal.

---

## GAP 5 — Geo-radius "near me" search  ·  v1.43.2  ·  ~1 d

### Problem (cited)
0 haversine/distance queries in 11k LOC. lat/lng ARE stored
(`studio.php:485`, catalog-meta) and shown on a map, but no "within X km" search.

### The fix
**New file:** `plugins/nadlan-config/inc/geo-search.php` (add to the module
loader array in `nadlan-config.php`). Haversine via `posts_clauses`, gated on
`lat`,`lng`,`radius_km` request params so default behavior is unchanged.

```php
if ( ! defined( 'ABSPATH' ) ) { exit; }
/* GAP 5: opt-in geo-radius filter for the directory/projects REST queries.
 * Pattern adapted from github.com/birgire/geo-query (MIT). Uses existing
 * post meta keys 'lat' and 'lng'. */
if ( ! function_exists( 'nadlan_geo_clauses' ) ) {
	function nadlan_geo_clauses( $clauses, $lat, $lng, $km ) {
		global $wpdb;
		$lat = (float) $lat; $lng = (float) $lng; $km = max( 0.1, (float) $km );
		$clauses['join'] .=
			" INNER JOIN {$wpdb->postmeta} glat ON glat.post_id={$wpdb->posts}.ID AND glat.meta_key='lat'
			  INNER JOIN {$wpdb->postmeta} glng ON glng.post_id={$wpdb->posts}.ID AND glng.meta_key='lng' ";
		// 6371 = earth radius km; distance in km
		$dist = $wpdb->prepare(
			"( 6371 * acos( cos(radians(%f)) * cos(radians(glat.meta_value))
			 * cos(radians(glng.meta_value) - radians(%f))
			 + sin(radians(%f)) * sin(radians(glat.meta_value)) ) )",
			$lat, $lng, $lat
		);
		$clauses['fields']  .= ", {$dist} AS nl_distance ";
		$clauses['where']   .= $wpdb->prepare( " AND glat.meta_value <> '' " );
		$clauses['groupby']  = "{$wpdb->posts}.ID";
		$clauses['having']   = $wpdb->prepare( " {$dist} <= %f ", $km );
		$clauses['orderby']  = " nl_distance ASC ";
		return $clauses;
	}
}
```
Then in `inc/directory.php`'s REST callbacks (the `/directory` and `/projects`
endpoints), read `lat`,`lng`,`radius_km` from the request; if present, wrap the
WP_Query with `add_filter('posts_clauses', fn($c)=>nadlan_geo_clauses($c,$lat,$lng,$km))`
and remove after. Default radius 5 km. Add a "קרוב אליי" button in the directory
hero that calls `navigator.geolocation` and re-queries with the coords.

### QA
```bash
curl -s -k "https://nad-lan.co.il/wp-json/nadlan/v1/directory?lat=32.0853&lng=34.7818&radius_km=3" \
 | python3 -c "import sys,json;d=json.load(sys.stdin);print(len(d.get('html','')))"
```
- ✅ Returns only pros within 3 km of TLV center, nearest first.
- ✅ Without lat/lng params → identical to today (no behavior change).
- 🛑 No SQL error; cards missing lat/lng are simply excluded from geo results.

---

## GAP 6 — Roles & authorities  ·  v1.43.3  ·  ~1 d

### Problem (cited)
0 `add_role()`. Access is admin (`manage_options`) vs card-owner
(`owner_user_id`, `studio-rest.php:28-30`) vs anon. No way to delegate
"advertiser manager" without giving full admin → blocks zero-touch ops.

### The fix
**New file:** `plugins/nadlan-config/inc/roles.php`

```php
if ( ! defined( 'ABSPATH' ) ) { exit; }
/* GAP 6: custom roles + capabilities for delegated, zero-touch operations. */
if ( ! function_exists( 'nadlan_register_roles' ) ) {
	function nadlan_register_roles() {
		add_role( 'nadlan_advertiser', 'מפרסם נדל״ן', array(
			'read' => true, 'nadlan_edit_own_card' => true,
			'nadlan_upload_own_media' => true,
		) );
		add_role( 'nadlan_manager', 'מנהל תוכן נדל״ן', array(
			'read' => true, 'nadlan_moderate_reviews' => true,
			'nadlan_reassign_card' => true, 'nadlan_run_imports' => true,
			'nadlan_edit_own_card' => true,
		) );
		// give admins the new caps too
		$admin = get_role( 'administrator' );
		if ( $admin ) {
			foreach ( array('nadlan_edit_own_card','nadlan_upload_own_media',
				'nadlan_moderate_reviews','nadlan_reassign_card','nadlan_run_imports',
				'nadlan_manage_tiers') as $cap ) { $admin->add_cap( $cap ); }
		}
	}
}
register_activation_hook( dirname( __DIR__ ) . '/nadlan-config.php', 'nadlan_register_roles' );
add_action( 'init', function () {
	if ( get_option( 'nadlan_roles_v' ) !== '1' ) {
		nadlan_register_roles(); update_option( 'nadlan_roles_v', '1' );
	}
} );
```
Then SOFTEN the blunt gates (keep admin working via the caps added above):
- `studio-rest.php:28` → `if ( current_user_can('manage_options') || current_user_can('nadlan_edit_own_card') ) ...` (still also require owner match for non-admins — keep the `$owner === $uid` line).
- `tiers.php:216` → `current_user_can('nadlan_manage_tiers')`.
- `lead-ledger.php` / `ops-dashboard.php` admin pages → gate on
  `nadlan_moderate_reviews` / `manage_options`.

### QA (per-role, from the gap-map matrix)
- A `nadlan_advertiser` user: CAN edit their own card, gets **403** on a card
  they don't own, CANNOT open the ops dashboard.
- A `nadlan_manager`: CAN moderate reviews + reassign, CANNOT change billing.
- Admin: unchanged (everything still works).

---

## Suggested order & dependencies
1. **GAP 1** (1hr) — ship first, unblocks the core paid promise.
2. **GAP 2** (2hr) — advertisers see value immediately.
3. **GAP 4** (½d) — turns AI on (independent, no blockers).
4. **GAP 5** (1d) — geo search (independent).
5. **GAP 6** (1d) — roles (independent; do before scaling staff).
6. **GAP 3** (1-2d) — LAST, and only after owner installs WC Subscriptions.

Each lands as its own draft PR. Claude reviews against
`docs/2026-06-04-e2e-revenue-qa-script.md`, merges, and asks the owner for the
one "Update Now" click.
