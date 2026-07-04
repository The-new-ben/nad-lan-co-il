<?php
/**
 * nadlan-config - Free listing wizard with AI assist (v1.69.70)
 *
 * Front-end, PRACTICAL (not a mock) listing-creation flow, Zillow-FSBO-style:
 *   [nadlan_listing_wizard] shortcode →
 *   Step 1  free-text description ("ספרו על הנכס") → AI (existing nadlan_llm_request
 *           adapter) extracts structured fields as strict JSON
 *   Step 2  review/edit every field (pre-filled by the AI)
 *   Step 3  photos (REAL upload via wp_handle_upload, logged-in only) + video URL
 *   Step 4  submit → pending nadlan_property owned by the user → moderation
 *
 * Free listings. Login required (spam + ownership). AI endpoint rate-limited.
 * All input sanitized against a strict whitelist. No caps bypass: submit inserts
 * as pending; publishing stays an editor action.
 */

if ( ! defined( 'ABSPATH' ) ) { exit; }

const NADLAN_PWIZ_MAX_PHOTO_BYTES = 8388608; // 8MB
const NADLAN_PWIZ_MAX_PHOTOS      = 12;

/* ---------------- field whitelist (shared by AI + submit) ---------------- */
if ( ! function_exists( 'nadlan_pwiz_fields' ) ) {
	function nadlan_pwiz_fields() {
		return array(
			// key => [type, label]
			'listing_type'       => array( 'enum:sale,rent', 'סוג עסקה' ),
			'property_type'      => array( 'enum:apartment,garden,penthouse,duplex,cottage,studio,other', 'סוג נכס' ),
			'price'              => array( 'int', 'מחיר (₪)' ),
			'rooms'              => array( 'float', 'חדרים' ),
			'floor'              => array( 'int', 'קומה' ),
			'total_floors'       => array( 'int', 'קומות בבניין' ),
			'size_sqm'           => array( 'int', 'שטח (מ״ר)' ),
			'balcony_sqm'        => array( 'int', 'מרפסת (מ״ר)' ),
			'city'               => array( 'text', 'עיר' ),
			'neighborhood'       => array( 'text', 'שכונה' ),
			'street'             => array( 'text', 'רחוב' ),
			'building_number'    => array( 'text', 'מספר בית' ),
			'parking'            => array( 'bool', 'חניה' ),
			'elevator'           => array( 'bool', 'מעלית' ),
			'ac'                 => array( 'bool', 'מיזוג' ),
			'protected_room'     => array( 'bool', 'ממ״ד' ),
			'storage'            => array( 'bool', 'מחסן' ),
			'arnona_monthly'     => array( 'int', 'ארנונה לחודש (₪)' ),
			'vaad_bayit_monthly' => array( 'int', 'ועד בית לחודש (₪)' ),
			'entry_date'         => array( 'text', 'תאריך כניסה' ),
			'condition'          => array( 'enum:new,renovated,good,needs_renovation', 'מצב הנכס' ),
			'direction'          => array( 'text', 'כיווני אוויר' ),
			'units_per_floor'    => array( 'int', 'דירות בקומה' ),
			'unit_position'      => array( 'int', 'מיקום הדירה בקומה (מימין)' ),
			'video_url'          => array( 'url', 'קישור לסרטון (יוטיוב)' ),
			'highlights_csv'     => array( 'text', 'נקודות בולטות (מופרד ב-|)' ),
		);
	}
}

if ( ! function_exists( 'nadlan_pwiz_sanitize' ) ) {
	function nadlan_pwiz_sanitize( $key, $val ) {
		$fields = nadlan_pwiz_fields();
		if ( ! isset( $fields[ $key ] ) ) { return null; }
		$type = $fields[ $key ][0];
		if ( strpos( $type, 'enum:' ) === 0 ) {
			$allowed = explode( ',', substr( $type, 5 ) );
			$v = sanitize_key( (string) $val );
			return in_array( $v, $allowed, true ) ? $v : null;
		}
		switch ( $type ) {
			case 'int':   $v = (int) $val;   return ( $v >= 0 && $v < 500000000 ) ? $v : null;
			case 'float': $v = (float) $val; return ( $v >= 0 && $v <= 30 ) ? $v : null;
			case 'bool':  return (bool) filter_var( $val, FILTER_VALIDATE_BOOLEAN );
			case 'url':   $v = esc_url_raw( trim( (string) $val ) ); return $v ?: null;
			default:      return sanitize_text_field( wp_unslash( (string) $val ) );
		}
	}
}

/* ---------------- rate limit ---------------- */
if ( ! function_exists( 'nadlan_pwiz_rate_limited' ) ) {
	function nadlan_pwiz_rate_limited( $bucket, $limit, $window ) {
		$key = 'nlpwiz_' . $bucket . '_' . get_current_user_id();
		$n   = (int) get_transient( $key );
		if ( $n >= $limit ) { return true; }
		set_transient( $key, $n + 1, $window );
		return false;
	}
}

/* ---------------- REST ---------------- */
add_action( 'rest_api_init', function () {

	// AI extraction: free text → structured fields
	register_rest_route( 'nadlan/v1', '/listing-ai-draft', array(
		'methods'  => 'POST',
		'permission_callback' => function () { return is_user_logged_in(); },
		'callback' => function ( WP_REST_Request $req ) {
			if ( nadlan_pwiz_rate_limited( 'ai', 10, HOUR_IN_SECONDS ) ) {
				return new WP_Error( 'rate_limited', 'חרגתם ממכסת נסיונות. נסו שוב בעוד שעה.', array( 'status' => 429 ) );
			}
			$text = sanitize_textarea_field( (string) $req->get_param( 'text' ) );
			if ( mb_strlen( $text ) < 30 ) {
				return new WP_Error( 'too_short', 'ספרו קצת יותר על הנכס (לפחות כמה משפטים).', array( 'status' => 400 ) );
			}
			$text = mb_substr( $text, 0, 4000 );
			if ( ! function_exists( 'nadlan_llm_request' ) ) {
				return new WP_Error( 'no_ai', 'שירות ה-AI אינו זמין כרגע.', array( 'status' => 503 ) );
			}
			$keys = implode( ', ', array_keys( nadlan_pwiz_fields() ) );
			$system = 'You extract Israeli real-estate listing data from Hebrew or English free text. '
				. 'Return ONLY a JSON object, no markdown, no commentary. Allowed keys: ' . $keys . ', title, description. '
				. 'listing_type: sale|rent. property_type: apartment|garden|penthouse|duplex|cottage|studio|other. '
				. 'condition: new|renovated|good|needs_renovation. Booleans true/false. Numbers as numbers. '
				. 'title: catchy Hebrew listing title (max 70 chars). highlights: array of 3-5 short factual Hebrew selling points (max 40 chars each). description: polished 2-3 paragraph Hebrew description, '
				. 'factual, no exaggerations, no discrimination, no "once in a lifetime" hype. Omit keys you cannot infer. '
				. 'NEVER invent a price or address that is not in the text.';
			$out = nadlan_llm_request( $system, $text, array( 'max_tokens' => 900, 'temperature' => 0.2 ) );
			if ( is_wp_error( $out ) ) { return new WP_Error( 'ai_failed', 'ה-AI לא הצליח לעבד את הטקסט. נסו שוב.', array( 'status' => 502 ) ); }
			// tolerate accidental fencing
			$out  = trim( preg_replace( '/^```(?:json)?|```$/m', '', trim( (string) $out ) ) );
			$data = json_decode( $out, true );
			if ( ! is_array( $data ) ) { return new WP_Error( 'ai_badjson', 'תשובת ה-AI לא היתה תקינה. נסו שוב.', array( 'status' => 502 ) ); }
			$clean = array();
			foreach ( $data as $k => $v ) {
				if ( $k === 'highlights' && is_array( $v ) ) {
					$hl = array_filter( array_map( function ( $x ) { return mb_substr( sanitize_text_field( (string) $x ), 0, 60 ); }, array_slice( $v, 0, 6 ) ) );
					if ( $hl ) { $clean['highlights_csv'] = implode( '|', $hl ); }
					continue;
				}
				if ( $k === 'title' ) { $clean['title'] = mb_substr( sanitize_text_field( (string) $v ), 0, 90 ); continue; }
				if ( $k === 'description' ) { $clean['description'] = mb_substr( sanitize_textarea_field( (string) $v ), 0, 4000 ); continue; }
				$s = nadlan_pwiz_sanitize( $k, $v );
				if ( $s !== null ) { $clean[ $k ] = $s; }
			}
			// compliance scan on the generated description
			if ( ! empty( $clean['description'] ) && function_exists( 'nadlan_compliance_scan' ) ) {
				$hits = nadlan_compliance_scan( $clean['description'] );
				if ( $hits ) { $clean['compliance_notes'] = wp_list_pluck( $hits, 'reason' ); }
			}
			return array( 'fields' => $clean );
		},
	) );

	// Real photo upload
	register_rest_route( 'nadlan/v1', '/listing-photo', array(
		'methods'  => 'POST',
		'permission_callback' => function () { return is_user_logged_in(); },
		'callback' => function ( WP_REST_Request $req ) {
			if ( nadlan_pwiz_rate_limited( 'photo', 40, HOUR_IN_SECONDS ) ) {
				return new WP_Error( 'rate_limited', 'חרגתם ממכסת ההעלאות לשעה.', array( 'status' => 429 ) );
			}
			$files = $req->get_file_params();
			if ( empty( $files['photo'] ) ) { return new WP_Error( 'no_file', 'לא נבחר קובץ.', array( 'status' => 400 ) ); }
			$f = $files['photo'];
			if ( (int) $f['size'] > NADLAN_PWIZ_MAX_PHOTO_BYTES ) { return new WP_Error( 'too_big', 'קובץ גדול מ-8MB.', array( 'status' => 400 ) ); }
			$check = wp_check_filetype_and_ext( $f['tmp_name'], $f['name'] );
			if ( empty( $check['type'] ) || strpos( $check['type'], 'image/' ) !== 0 || $check['type'] === 'image/svg+xml' ) {
				return new WP_Error( 'not_image', 'ניתן להעלות תמונות בלבד (JPG/PNG/WEBP).', array( 'status' => 400 ) );
			}
			require_once ABSPATH . 'wp-admin/includes/file.php';
			require_once ABSPATH . 'wp-admin/includes/image.php';
			require_once ABSPATH . 'wp-admin/includes/media.php';
			$moved = wp_handle_upload( $f, array( 'test_form' => false, 'mimes' => array( 'jpg|jpeg' => 'image/jpeg', 'png' => 'image/png', 'webp' => 'image/webp' ) ) );
			if ( isset( $moved['error'] ) ) { return new WP_Error( 'upload_failed', $moved['error'], array( 'status' => 500 ) ); }
			$att_id = wp_insert_attachment( array(
				'post_mime_type' => $moved['type'],
				'post_title'     => sanitize_file_name( pathinfo( $moved['file'], PATHINFO_FILENAME ) ),
				'post_status'    => 'inherit',
				'post_author'    => get_current_user_id(),
			), $moved['file'] );
			if ( ! is_wp_error( $att_id ) && $att_id ) {
				wp_update_attachment_metadata( $att_id, wp_generate_attachment_metadata( $att_id, $moved['file'] ) );
			}
			return array( 'url' => $moved['url'], 'attachment_id' => (int) $att_id );
		},
	) );

	// Submit → pending listing
	register_rest_route( 'nadlan/v1', '/listing-submit', array(
		'methods'  => 'POST',
		'permission_callback' => function () { return is_user_logged_in(); },
		'callback' => function ( WP_REST_Request $req ) {
			if ( nadlan_pwiz_rate_limited( 'submit', 6, DAY_IN_SECONDS ) ) {
				return new WP_Error( 'rate_limited', 'ניתן לפרסם עד 6 מודעות ביום.', array( 'status' => 429 ) );
			}
			$title = mb_substr( sanitize_text_field( (string) $req->get_param( 'title' ) ), 0, 90 );
			$desc  = mb_substr( sanitize_textarea_field( (string) $req->get_param( 'description' ) ), 0, 6000 );
			$meta_in = (array) $req->get_param( 'fields' );
			if ( mb_strlen( $title ) < 8 ) { return new WP_Error( 'no_title', 'כותרת קצרה מדי.', array( 'status' => 400 ) ); }
			if ( mb_strlen( $desc ) < 40 ) { return new WP_Error( 'no_desc', 'תיאור קצר מדי.', array( 'status' => 400 ) ); }
			$meta = array();
			foreach ( $meta_in as $k => $v ) {
				$s = nadlan_pwiz_sanitize( $k, $v );
				if ( $s !== null && $s !== '' ) { $meta[ $k ] = $s; }
			}
			if ( empty( $meta['listing_type'] ) || empty( $meta['city'] ) ) {
				return new WP_Error( 'missing', 'חסרים שדות חובה: סוג עסקה ועיר.', array( 'status' => 400 ) );
			}
			// photos: only accept media-library URLs from this site (uploaded via our endpoint)
			$photos = array();
			foreach ( (array) $req->get_param( 'photos' ) as $u ) {
				$u = esc_url_raw( (string) $u );
				if ( $u && strpos( $u, wp_upload_dir()['baseurl'] ) === 0 ) { $photos[] = $u; }
				if ( count( $photos ) >= NADLAN_PWIZ_MAX_PHOTOS ) { break; }
			}
			$pid = wp_insert_post( array(
				'post_type'    => 'nadlan_property',
				'post_status'  => 'pending',
				'post_title'   => $title,
				'post_content' => $desc,
				'post_author'  => get_current_user_id(),
			), true );
			if ( is_wp_error( $pid ) ) { return new WP_Error( 'insert_failed', 'שמירה נכשלה. נסו שוב.', array( 'status' => 500 ) ); }
			foreach ( $meta as $k => $v ) { update_post_meta( $pid, $k, $v ); }
			if ( $photos ) { update_post_meta( $pid, 'photos_csv', implode( ',', $photos ) ); }
			update_post_meta( $pid, 'source', 'owner_wizard' );
			update_post_meta( $pid, 'claim_status', 'verified' );
			update_post_meta( $pid, 'owner_user_id', get_current_user_id() );
			// notify admin
			wp_mail( get_option( 'admin_email' ), '[nad-lan] מודעה חדשה ממתינה לאישור: ' . $title,
				'מודעה חדשה נשלחה מהאשף: ' . $title . "\n" . admin_url( 'post.php?post=' . $pid . '&action=edit' ) );
			return array( 'id' => (int) $pid, 'status' => 'pending' );
		},
	) );
} );

/* ---------------- the wizard UI ---------------- */
if ( ! function_exists( 'nadlan_pwiz_shortcode' ) ) {
	function nadlan_pwiz_shortcode() {
		if ( ! is_user_logged_in() ) {
			$login = wp_login_url( get_permalink() );
			$reg   = wp_registration_url();
			return '<div class="nlpw nlpw-gate" dir="rtl"><h3>פרסום מודעה - חינם</h3>'
				. '<p>כדי לפרסם נכס (בחינם, בלי כרטיס אשראי) צריך חשבון - כך נשמור על מודעות אמינות בלבד.</p>'
				. '<p><a class="nlpw-btn" href="' . esc_url( $login ) . '">התחברות</a> '
				. ( get_option( 'users_can_register' ) ? '<a class="nlpw-btn nlpw-btn-alt" href="' . esc_url( $reg ) . '">הרשמה מהירה</a>' : '' )
				. '</p></div>';
		}
		ob_start(); ?>
<div class="nlpw" id="nlpw" dir="rtl" data-rest="<?php echo esc_attr( rest_url( 'nadlan/v1' ) ); ?>" data-nonce="<?php echo esc_attr( wp_create_nonce( 'wp_rest' ) ); ?>">
	<ol class="nlpw-steps"><li class="is-on">תיאור</li><li>פרטים</li><li>תמונות</li><li>אישור</li></ol>

	<section class="nlpw-step nlpw-s1 is-on">
		<h3>ספרו לנו על הנכס - במילים שלכם</h3>
		<p class="nlpw-hint">כתבו חופשי: מה הנכס, איפה, כמה חדרים, קומה, מחיר, מה מיוחד בו. ה-AI שלנו יהפוך את זה למודעה מסודרת - ואתם מאשרים לפני פרסום.</p>
		<textarea id="nlpw-text" rows="7" placeholder="לדוגמה: דירת 4 חדרים ברחוב סוקולוב בחולון, קומה 3 מתוך 6, 95 מ״ר עם מרפסת, ממ״ד ומעלית. משופצת. 2.1 מיליון ש״ח..."></textarea>
		<button type="button" class="nlpw-btn" id="nlpw-ai">✨ בנו לי מודעה עם AI</button>
		<button type="button" class="nlpw-link" id="nlpw-skip">או מלאו ידנית ←</button>
		<p class="nlpw-err" id="nlpw-err1" hidden></p>
	</section>

	<section class="nlpw-step nlpw-s2">
		<h3>בדקו והשלימו את הפרטים</h3>
		<label class="nlpw-full">כותרת המודעה<input type="text" id="nlpw-title" maxlength="90"></label>
		<label class="nlpw-full">תיאור<textarea id="nlpw-desc" rows="6"></textarea></label>
		<div class="nlpw-grid" id="nlpw-fields"></div>
		<button type="button" class="nlpw-btn" data-go="3">המשך לתמונות ←</button>
	</section>

	<section class="nlpw-step nlpw-s3">
		<h3>תמונות וסרטון</h3>
		<p class="nlpw-hint">עד <?php echo (int) NADLAN_PWIZ_MAX_PHOTOS; ?> תמונות (JPG/PNG/WEBP, עד 8MB). מודעות עם 6+ תמונות מקבלות פי 2 פניות.</p>
		<input type="file" id="nlpw-photo" accept="image/jpeg,image/png,image/webp" multiple>
		<div class="nlpw-thumbs" id="nlpw-thumbs"></div>
		<label class="nlpw-full">קישור לסרטון (יוטיוב, לא חובה)<input type="url" id="nlpw-video" placeholder="https://youtu.be/..."></label>
		<p class="nlpw-err" id="nlpw-err3" hidden></p>
		<button type="button" class="nlpw-btn" data-go="4">לסיכום ←</button>
	</section>

	<section class="nlpw-step nlpw-s4">
		<h3>רגע לפני פרסום</h3>
		<div class="nlpw-review" id="nlpw-review"></div>
		<p class="nlpw-hint">המודעה תפורסם לאחר בדיקה קצרה של הצוות (בדרך כלל תוך יום עסקים). הפרסום חינם.</p>
		<button type="button" class="nlpw-btn nlpw-submit" id="nlpw-send">פרסמו את המודעה - חינם</button>
		<p class="nlpw-err" id="nlpw-err4" hidden></p>
	</section>

	<section class="nlpw-step nlpw-done">
		<h3>🎉 המודעה נשלחה!</h3>
		<p>קיבלנו את המודעה והיא ממתינה לאישור מהיר. נעדכן אתכם במייל כשהיא עולה לאוויר.</p>
		<p><a class="nlpw-btn" href="<?php echo esc_url( home_url( '/properties/' ) ); ?>">לכל הנכסים ←</a></p>
	</section>
</div>
<?php
		return ob_get_clean();
	}
}
add_shortcode( 'nadlan_listing_wizard', 'nadlan_pwiz_shortcode' );

/* ---------------- wizard assets ---------------- */
if ( ! function_exists( 'nadlan_pwiz_assets' ) ) {
	function nadlan_pwiz_assets() {
		if ( ! is_singular() || ! has_shortcode( (string) get_post_field( 'post_content', get_queried_object_id() ), 'nadlan_listing_wizard' ) ) { return; }
		wp_register_style( 'nadlan-pwiz', false );
		wp_enqueue_style( 'nadlan-pwiz' );
		wp_add_inline_style( 'nadlan-pwiz', '
.nlpw{--ink:#1B1A17;--warm:#6D665C;--gold:#9C7A3C;--line:#E2DCD0;--band:#F3EEE3;max-width:720px;margin:0 auto 40px;font-family:var(--font-sans,Heebo,system-ui,sans-serif);color:var(--ink)}
.nlpw h3{font-family:var(--font-serif,"Frank Ruhl Libre",serif);font-size:1.4rem;margin:0 0 10px}
.nlpw-steps{display:flex;gap:6px;list-style:none;counter-reset:s;margin:0 0 22px;padding:0}
.nlpw-steps li{flex:1;text-align:center;font-size:12px;color:var(--warm);counter-increment:s;padding:8px 4px;border-bottom:3px solid var(--line)}
.nlpw-steps li::before{content:counter(s) ". ";font-weight:700}
.nlpw-steps li.is-on{color:var(--ink);border-color:var(--gold);font-weight:600}
.nlpw-step{display:none}.nlpw-step.is-on{display:block}
.nlpw-hint{font-size:13px;color:var(--warm)}
.nlpw textarea,.nlpw input[type=text],.nlpw input[type=url],.nlpw input[type=number],.nlpw select{width:100%;font:inherit;font-size:14px;border:1px solid var(--line);border-radius:8px;padding:10px 12px;background:#FFFDFC;box-sizing:border-box}
.nlpw label{display:block;font-size:12.5px;font-weight:600;margin:0 0 12px}
.nlpw label input,.nlpw label select,.nlpw label textarea{margin-top:5px;font-weight:400}
.nlpw-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(160px,1fr));gap:0 14px}
.nlpw-grid .nlpw-chk{display:flex;align-items:center;gap:8px;font-weight:400;font-size:13.5px}
.nlpw-grid .nlpw-chk input{width:auto}
.nlpw-btn{display:inline-block;font:inherit;font-size:14.5px;font-weight:700;background:var(--ink);color:#fff;border:0;border-radius:8px;padding:12px 26px;cursor:pointer;margin-top:14px;text-decoration:none}
.nlpw-btn:hover{background:#000}
.nlpw-btn-alt{background:var(--gold)}
.nlpw-link{background:none;border:0;font:inherit;font-size:13px;color:var(--warm);cursor:pointer;margin-inline-start:12px;text-decoration:underline}
.nlpw-err{color:#A93F2A;font-size:13px}
.nlpw-thumbs{display:flex;flex-wrap:wrap;gap:8px;margin:12px 0}
.nlpw-thumbs img{width:86px;height:64px;object-fit:cover;border-radius:6px;border:1px solid var(--line)}
.nlpw-review{border:1px solid var(--line);border-radius:10px;background:var(--band);padding:14px 18px;font-size:14px}
.nlpw-review dt{font-size:11px;color:var(--warm)}.nlpw-review dd{margin:0 0 8px;font-weight:600}
.nlpw-submit{background:var(--gold);font-size:16px}
.nlpw-gate{max-width:520px;margin:0 auto;text-align:center;border:1px solid var(--line);border-radius:12px;padding:28px;background:#FFFDFC}
' );
		wp_register_script( 'nadlan-pwiz-js', false, array(), '1.69.70', true );
		wp_enqueue_script( 'nadlan-pwiz-js' );
		$fields_js = array();
		foreach ( nadlan_pwiz_fields() as $k => $def ) { $fields_js[] = array( 'key' => $k, 'type' => $def[0], 'label' => $def[1] ); }
		wp_add_inline_script( 'nadlan-pwiz-js', 'var NLPW_FIELDS=' . wp_json_encode( $fields_js ) . ';
(function(){
document.addEventListener("DOMContentLoaded",function(){
	var root=document.getElementById("nlpw");if(!root){return}
	var rest=root.dataset.rest.replace(/\/$/,""),nonce=root.dataset.nonce;
	var state={fields:{},photos:[]};
	function go(n){
		root.querySelectorAll(".nlpw-step").forEach(function(s,i){s.classList.toggle("is-on",i===n-1)});
		root.querySelectorAll(".nlpw-steps li").forEach(function(li,i){li.classList.toggle("is-on",i===Math.min(n,4)-1)});
		window.scrollTo({top:root.offsetTop-40,behavior:"smooth"});
	}
	function api(path,opts){
		opts=opts||{};opts.headers=Object.assign({"X-WP-Nonce":nonce},opts.headers||{});
		return fetch(rest+path,opts).then(function(r){return r.json().then(function(j){if(!r.ok){throw new Error(j.message||"שגיאה")}return j})});
	}
	function buildFields(vals){
		var wrap=document.getElementById("nlpw-fields");wrap.innerHTML="";
		NLPW_FIELDS.forEach(function(f){
			var v=vals[f.key];
			var lab=document.createElement("label");
			if(f.type==="bool"){
				lab.className="nlpw-chk";
				lab.innerHTML="<input type=checkbox data-k=\""+f.key+"\""+(v?" checked":"")+"> "+f.label;
			}else if(f.type.indexOf("enum:")===0){
				var ops=f.type.slice(5).split(","),he={sale:"מכירה",rent:"השכרה",apartment:"דירה",garden:"דירת גן",penthouse:"פנטהאוז",duplex:"דופלקס",cottage:"קוטג/בית",studio:"סטודיו",other:"אחר",new:"חדש מקבלן",renovated:"משופץ",good:"טוב",needs_renovation:"דורש שיפוץ"};
				lab.innerHTML=f.label+"<select data-k=\""+f.key+"\"><option value=\"\">-</option>"+ops.map(function(o){return "<option value=\""+o+"\""+(v===o?" selected":"")+">"+(he[o]||o)+"</option>"}).join("")+"</select>";
			}else{
				var t=(f.type==="int"||f.type==="float")?"number":(f.type==="url"?"url":"text");
				lab.innerHTML=f.label+"<input type="+t+" data-k=\""+f.key+"\" value=\""+(v!==undefined?String(v).replace(/"/g,"&quot;"):"")+"\">";
			}
			wrap.appendChild(lab);
		});
	}
	function collect(){
		var out={};
		root.querySelectorAll("#nlpw-fields [data-k]").forEach(function(el){
			var k=el.dataset.k,v=el.type==="checkbox"?el.checked:el.value.trim();
			if(v!==""&&v!==false){out[k]=v}
		});
		var vid=document.getElementById("nlpw-video").value.trim();if(vid){out.video_url=vid}
		return out;
	}
	document.getElementById("nlpw-ai").addEventListener("click",function(){
		var btn=this,err=document.getElementById("nlpw-err1");err.hidden=true;
		btn.disabled=true;btn.textContent="ה-AI קורא את התיאור...";
		api("/listing-ai-draft",{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify({text:document.getElementById("nlpw-text").value})})
		.then(function(j){
			var f=j.fields||{};state.fields=f;
			document.getElementById("nlpw-title").value=f.title||"";
			document.getElementById("nlpw-desc").value=f.description||"";
			buildFields(f);go(2);
		}).catch(function(e){err.textContent=e.message;err.hidden=false})
		.finally(function(){btn.disabled=false;btn.textContent="✨ בנו לי מודעה עם AI"});
	});
	document.getElementById("nlpw-skip").addEventListener("click",function(){buildFields({});go(2)});
	root.querySelectorAll("[data-go]").forEach(function(b){b.addEventListener("click",function(){
		if(b.dataset.go==="4"){
			var f=collect(),t=document.getElementById("nlpw-title").value.trim();
			var he={sale:"מכירה",rent:"השכרה"};
			var rows=[["כותרת",t],["עסקה",he[f.listing_type]||f.listing_type||"-"],["עיר",f.city||"-"],["מחיר",f.price?Number(f.price).toLocaleString()+" ₪":"-"],["חדרים",f.rooms||"-"],["תמונות",state.photos.length]];
			document.getElementById("nlpw-review").innerHTML="<dl>"+rows.map(function(r){return "<dt>"+r[0]+"</dt><dd>"+r[1]+"</dd>"}).join("")+"</dl>";
		}
		go(parseInt(b.dataset.go,10));
	})});
	document.getElementById("nlpw-photo").addEventListener("change",function(){
		var err=document.getElementById("nlpw-err3");err.hidden=true;
		Array.prototype.slice.call(this.files,0,12).forEach(function(file){
			var fd=new FormData();fd.append("photo",file);
			api("/listing-photo",{method:"POST",body:fd}).then(function(j){
				state.photos.push(j.url);
				var img=document.createElement("img");img.src=j.url;document.getElementById("nlpw-thumbs").appendChild(img);
			}).catch(function(e){err.textContent=e.message;err.hidden=false});
		});
		this.value="";
	});
	document.getElementById("nlpw-send").addEventListener("click",function(){
		var btn=this,err=document.getElementById("nlpw-err4");err.hidden=true;btn.disabled=true;btn.textContent="שולחים...";
		api("/listing-submit",{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify({
			title:document.getElementById("nlpw-title").value,
			description:document.getElementById("nlpw-desc").value,
			fields:collect(),photos:state.photos
		})}).then(function(){go(5)})
		.catch(function(e){err.textContent=e.message;err.hidden=false;btn.disabled=false;btn.textContent="פרסמו את המודעה - חינם"});
	});
});
})();' );
	}
}
add_action( 'wp_enqueue_scripts', 'nadlan_pwiz_assets' );
