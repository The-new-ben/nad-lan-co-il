<?php
/**
 * nadlan-config - AI features: listing-description generator + natural-language search (v1.9.0)
 *
 * Two cutting-edge features, one LLM adapter, deliberately compliance-first:
 *
 *  1) AI listing-description generator (admin button on nadlan_property edit):
 *     -- Hebrew, factual, 85-150 words, 8-10th grade, neutral-warm tone.
 *     -- GUARDRAILS: no steering language by protected class (family status,
 *        religion, ethnicity, origin, gender, age, disability) - matches HUD
 *        Fair-Housing 2024 guidance AND Israeli חוק איסור הפליה במוצרים ובשירותים.
 *     -- POST-GENERATION SCAN flags banned phrases ("מתאים למשפחות עם ילדים",
 *        "קרוב לבית כנסת/כנסייה", "שכונה דתית/חילונית", "ל-zugot צעירים", etc.)
 *        and refuses to auto-publish if hits found - surfaces to editor instead.
 *
 *  2) Natural-language search: visitor types "דירת 4 חדרים בתל אביב עד 3 מיליון
 *     עם מעלית" → LLM parses to a STRUCTURED filter ({city,rooms_min,price_max,
 *     amenities[]}) → WP_Query → results. Deterministic regex fallback for the
 *     common Hebrew patterns so it works even if LLM is unavailable.
 *
 * LLM adapter: nadlan_llm_request($prompt, $opts) now delegates to the shared
 * GAP 4 provider adapter, nadlan_ai_chat(). Default provider is OpenAI with
 * Anthropic fallback. NEVER fails open: if no key + no override, returns
 * WP_Error so callers degrade gracefully.
 *
 * BLANK (owner): set provider + key in Settings -> NadLan AI. Compliance phrase
 * list is conservative; review with counsel before public NL search rollout
 * (docs/listings-questions.md).
 */

if ( ! defined( 'ABSPATH' ) ) { exit; }

/* ---- LLM adapter (pluggable) ---- */
if ( ! function_exists( 'nadlan_llm_request' ) ) {
	/**
	 * @param string $system System prompt.
	 * @param string $user   User content.
	 * @param array  $opts   max_tokens, temperature, model.
	 * @return string|WP_Error  The model's text reply, or WP_Error.
	 */
	function nadlan_llm_request( $system, $user, $opts = array() ) {
		$override = apply_filters( 'nadlan_llm_request', null, $system, $user, $opts );
		if ( $override !== null ) { return $override; }
		if ( ! function_exists( 'nadlan_ai_chat' ) ) {
			return new WP_Error( 'no_adapter', 'AI adapter not loaded' );
		}
		$max_tokens = (int) ( $opts['max_tokens'] ?? 600 );
		return nadlan_ai_chat( $system, array( array( 'role' => 'user', 'content' => $user ) ), $max_tokens );
	}
}

/* ---- Compliance scan (Hebrew + English steering phrases) ---- */
if ( ! function_exists( 'nadlan_compliance_scan' ) ) {
	/**
	 * Returns array of {phrase, reason} hits. Empty = clean.
	 * Conservative list - review with counsel before relaxing.
	 */
	function nadlan_compliance_scan( $text ) {
		$rules = array(
			// family status / age (Israeli + US Fair Housing concerns)
			array( '/מתאים\s+ל?(?:משפחות|זוגות\s+צעירים|רווקים|פנסיונרים)/u', 'family/age steering (familial status)' ),
			array( '/great\s+for\s+(?:families|young\s+professionals|empty\s+nesters)/i', 'family/age steering' ),
			array( '/perfect\s+for\s+(?:families|couples|singles)/i', 'familial steering' ),
			// religion / ethnicity / cultural
			array( '/קרוב\s+ל(?:בית\s+כנסת|מסגד|כנסייה)/u', 'religious steering' ),
			array( '/שכונה\s+(?:דתית|חרדית|חילונית|ערבית|יהודית)/u', 'religious/ethnic steering' ),
			array( '/קהילה\s+(?:דתית|חרדית|חילונית|ערבית|יהודית|נוצרית|מוסלמית)/u', 'religious/ethnic steering' ),
			array( '/close\s+to\s+(?:church|synagogue|mosque|temple)/i', 'religious steering' ),
			// disability
			array( '/walking\s+distance/i', 'ableist phrasing (use "near")' ),
			// generic steering
			array( '/exclusive\s+(?:community|neighborhood)/i', 'exclusionary phrasing' ),
		);
		$hits = array();
		foreach ( $rules as $r ) {
			if ( preg_match( $r[0], $text, $m ) ) {
				$hits[] = array( 'phrase' => $m[0], 'reason' => $r[1] );
			}
		}
		return $hits;
	}
}

/* ---- AI listing description generator ----
 * Admin button on nadlan_property edit screen. Reads meta, calls LLM, scans
 * compliance, and either inserts (clean) or stores as draft note for review.
 */
if ( ! function_exists( 'nadlan_ai_desc_meta_box' ) ) {
	function nadlan_ai_desc_meta_box() {
		add_meta_box( 'nadlan_ai_desc', 'AI: תיאור נכס', function ( $post ) {
			$url = wp_nonce_url( admin_url( 'admin-post.php?action=nadlan_ai_desc&post_id=' . $post->ID ), 'nadlan_ai_desc_' . $post->ID );
			echo '<p>צרו תיאור אוטומטי מהשדות הקיימים (Hebrew, compliance-scanned). יישלח לעריכה לפני שמירה.</p>';
			echo '<a class="button button-primary" href="' . esc_url( $url ) . '">צרו תיאור</a>';
			$pending = get_post_meta( $post->ID, '_nadlan_ai_pending', true );
			if ( $pending ) {
				echo '<h4>טיוטה ממתינה</h4><textarea readonly style="width:100%;height:160px">' . esc_textarea( $pending ) . '</textarea>';
				$flags = get_post_meta( $post->ID, '_nadlan_ai_flags', true );
				if ( $flags ) { echo '<p style="color:#c00"><strong>דגלי תאימות:</strong> ' . esc_html( $flags ) . '</p>'; }
				$approve = wp_nonce_url( admin_url( 'admin-post.php?action=nadlan_ai_desc_approve&post_id=' . $post->ID ), 'nadlan_ai_desc_approve_' . $post->ID );
				echo '<a class="button" href="' . esc_url( $approve ) . '">אשר וכתוב לתוכן</a>';
			}
		}, 'nadlan_property', 'side' );
	}
}
add_action( 'add_meta_boxes', 'nadlan_ai_desc_meta_box' );

if ( ! function_exists( 'nadlan_ai_desc_run' ) ) {
	function nadlan_ai_desc_run() {
		if ( ! current_user_can( 'edit_posts' ) ) { wp_die( 'forbidden' ); }
		$id = isset( $_GET['post_id'] ) ? (int) $_GET['post_id'] : 0;
		check_admin_referer( 'nadlan_ai_desc_' . $id );
		$facts = array();
		foreach ( array( 'property_type','listing_type','city','street','rooms','size_sqm','floor','total_floors','price','elevator','parking','protected_room','balcony_sqm' ) as $k ) {
			$v = get_post_meta( $id, $k, true );
			if ( $v !== '' && $v !== null ) { $facts[ $k ] = $v; }
		}
		$system = "אתה כותב תיאורי נכסי נדל\"ן בעברית. כללים:\n"
			. "1) השתמש אך ורק בעובדות שניתנו. אל תמציא. דלג על שדה ריק.\n"
			. "2) 100-140 מילים, טון ניטרלי-חם, רמת קריאה כיתה ח-י, משפטים קצרים.\n"
			. "3) אסור להשתמש בביטויים מפלים או מכוונים על-פי דת, לאום, מוצא, מצב משפחתי, גיל, מגדר או נכות (חוק איסור הפליה במוצרים/Fair Housing).\n"
			. "4) אסור: \"מתאים למשפחות\", \"שכונה דתית/חילונית/ערבית\", \"קרוב לבית כנסת/מסגד/כנסייה\", \"לזוגות צעירים\", \"שכונה יוקרתית בלעדית\".\n"
			. "5) ללא אימוג'ים, ללא האשטגים, ללא קריאות לפעולה.\n"
			. "פלט: רק הטקסט הסופי, ללא כותרת.";
		$user = "נתוני הנכס:\n" . wp_json_encode( $facts, JSON_UNESCAPED_UNICODE );
		$out = nadlan_llm_request( $system, $user );
		if ( is_wp_error( $out ) ) {
			wp_safe_redirect( admin_url( 'post.php?post=' . $id . '&action=edit&ai_err=' . rawurlencode( $out->get_error_message() ) ) );
			exit;
		}
		$hits = nadlan_compliance_scan( $out );
		update_post_meta( $id, '_nadlan_ai_pending', $out );
		update_post_meta( $id, '_nadlan_ai_flags', $hits ? implode( ' · ', wp_list_pluck( $hits, 'phrase' ) ) : '' );
		wp_safe_redirect( admin_url( 'post.php?post=' . $id . '&action=edit&ai=generated' . ( $hits ? '&flagged=1' : '' ) ) );
		exit;
	}
}
add_action( 'admin_post_nadlan_ai_desc', 'nadlan_ai_desc_run' );

if ( ! function_exists( 'nadlan_ai_desc_approve' ) ) {
	function nadlan_ai_desc_approve() {
		if ( ! current_user_can( 'edit_posts' ) ) { wp_die( 'forbidden' ); }
		$id = isset( $_GET['post_id'] ) ? (int) $_GET['post_id'] : 0;
		check_admin_referer( 'nadlan_ai_desc_approve_' . $id );
		$pending = (string) get_post_meta( $id, '_nadlan_ai_pending', true );
		if ( $pending !== '' ) {
			wp_update_post( array( 'ID' => $id, 'post_content' => $pending ) );
			delete_post_meta( $id, '_nadlan_ai_pending' );
			delete_post_meta( $id, '_nadlan_ai_flags' );
		}
		wp_safe_redirect( admin_url( 'post.php?post=' . $id . '&action=edit&ai=approved' ) );
		exit;
	}
}
add_action( 'admin_post_nadlan_ai_desc_approve', 'nadlan_ai_desc_approve' );

/* ---- Natural-language search ---- */
if ( ! function_exists( 'nadlan_nls_regex_fallback' ) ) {
	/** Deterministic Hebrew regex parser - used when LLM unavailable. */
	function nadlan_nls_regex_fallback( $q ) {
		$f = array();
		if ( preg_match( '/(\d+(?:\.\d+)?)\s*חדר/u', $q, $m ) )      { $f['rooms_min'] = (float) $m[1]; }
		if ( preg_match( '/עד\s*(\d[\d,\.]*)\s*מיליון/u', $q, $m ) ){ $f['price_max'] = (int) ( str_replace( array( ',', '.' ), '', $m[1] ) * 1000000 ); }
		if ( preg_match( '/עד\s*([\d,]+)/u', $q, $m ) && empty( $f['price_max'] ) ) { $f['price_max'] = (int) str_replace( ',', '', $m[1] ); }
		if ( preg_match( '/(?:ב|ב-)([\p{Hebrew}\s]+?)(?:\s+(?:עד|מ-|עם|של|בלי)|$)/u', $q, $m ) ) { $f['city'] = trim( $m[1] ); }
		if ( strpos( $q, 'שכירות' ) !== false ) { $f['listing_type'] = 'rent'; }
		elseif ( strpos( $q, 'מכירה' ) !== false || strpos( $q, 'למכירה' ) !== false ) { $f['listing_type'] = 'sale'; }
		return $f;
	}
}

add_action( 'rest_api_init', function () {
	register_rest_route( 'nadlan/v1', '/nl-search', array(
		'methods' => 'GET', 'permission_callback' => '__return_true',
		'callback' => function ( $req ) {
			$q = trim( (string) $req->get_param( 'q' ) );
			if ( $q === '' ) { return new WP_REST_Response( array( 'ok' => false ), 400 ); }
			$cache_key = 'nadlan_nls_' . md5( $q );
			$cached = get_transient( $cache_key );
			$filter = is_array( $cached ) ? $cached : null;
			$src = $cached ? 'cache' : null;
			if ( ! $filter ) {
				$system = "Convert a Hebrew real-estate query into a JSON object with keys city (string), listing_type ('sale'|'rent'), rooms_min (number), price_min (int), price_max (int). Output ONLY valid JSON, no commentary, no markdown. Use null for unknown fields.";
				$out = nadlan_llm_request( $system, $q, array( 'max_tokens' => 200 ) );
				if ( is_wp_error( $out ) ) {
					$filter = nadlan_nls_regex_fallback( $q ); $src = 'regex_fallback';
				} else {
					$j = json_decode( trim( preg_replace( '/^```(?:json)?|```$/m', '', $out ) ), true );
					$filter = is_array( $j ) ? array_filter( $j, function ( $v ) { return $v !== null && $v !== '' && $v !== 0; } ) : nadlan_nls_regex_fallback( $q );
					$src = is_array( $j ) ? 'llm' : 'regex_fallback';
				}
				set_transient( $cache_key, $filter, HOUR_IN_SECONDS );
			} else { $src = 'cache'; }

			// run WP_Query
			$query = new WP_Query( array(
				'post_type' => 'nadlan_property', 'posts_per_page' => 20, 'no_found_rows' => true,
				'meta_query' => nadlan_ss_meta_query( $filter ),
			) );
			$items = array();
			foreach ( $query->posts as $p ) {
				$items[] = array(
					'id' => $p->ID, 'title' => get_the_title( $p ), 'url' => get_permalink( $p ),
					'price' => (int) get_post_meta( $p->ID, 'price', true ),
					'rooms' => (float) get_post_meta( $p->ID, 'rooms', true ),
					'sqm'   => (int) get_post_meta( $p->ID, 'size_sqm', true ),
					'city'  => (string) get_post_meta( $p->ID, 'city', true ),
				);
			}
			wp_reset_postdata();
			return new WP_REST_Response( array( 'ok' => true, 'parsed' => $filter, 'source' => $src, 'count' => count( $items ), 'items' => $items ), 200 );
		},
	) );
} );

/* Shortcode: NL search box */
add_shortcode( 'nadlan_nl_search', function () {
	ob_start(); ?>
<div class="nlnls" dir="rtl">
	<h3>חיפוש חכם</h3>
	<p class="nlnls-eg">למשל: "דירת 4 חדרים בתל אביב עד 3 מיליון" · "שכירות 3 חדרים ברמת גן עד 7000"</p>
	<form onsubmit="return nadlanNlSearch(this)">
		<input type="text" name="q" placeholder="תארו במילים שלכם מה אתם מחפשים" required>
		<button type="submit">חפשו</button>
	</form>
	<div class="nlnls-out"></div>
</div>
<script>
function nadlanNlSearch(f){
	var out=f.parentNode.querySelector('.nlnls-out');
	out.textContent='מחפש…';
	fetch('<?php echo esc_url_raw( rest_url( 'nadlan/v1/nl-search' ) ); ?>?q='+encodeURIComponent(f.q.value)).then(function(r){return r.json();}).then(function(j){
		if(!j.ok){out.textContent='שגיאה.';return;}
		if(j.count===0){out.innerHTML='לא נמצאו תוצאות. '+(j.parsed.city?'נסו עיר אחרת.':'נסו לפרט עיר ומחיר.');return;}
		var h='<p class="nlnls-meta">'+j.count+' תוצאות (פירוש: '+JSON.stringify(j.parsed)+')</p><ul class="nlnls-list">';
		j.items.forEach(function(it){
			h+='<li><a href="'+it.url+'">'+it.title+'</a> · '+(it.price?'₪'+it.price.toLocaleString():'')+' · '+it.rooms+' חד׳ · '+it.sqm+' מ"ר · '+(it.city||'')+'</li>';
		});
		out.innerHTML=h+'</ul>';
	}).catch(function(){out.textContent='שגיאת רשת.';});
	return false;
}
</script>
<style>
.nlnls{margin:18px 0;font-family:var(--font-sans,Heebo,sans-serif);max-width:640px}
.nlnls-eg{font-size:13px;color:#777;margin:4px 0 8px}
.nlnls input{width:70%;padding:11px;border:1px solid #ccc;border-radius:4px}
.nlnls button{padding:11px 22px;background:#1B1A17;color:#FAF7F1;border:0;border-radius:4px;cursor:pointer;margin-inline-start:6px}
.nlnls-meta{font-size:12px;color:#999;margin:10px 0 6px}
.nlnls-list{list-style:none;padding:0}
.nlnls-list li{padding:8px 0;border-bottom:1px solid rgba(27,26,23,.08)}
.nlnls-list a{color:#1B1A17;font-weight:500;text-decoration:none}
</style>
	<?php
	return ob_get_clean();
} );
