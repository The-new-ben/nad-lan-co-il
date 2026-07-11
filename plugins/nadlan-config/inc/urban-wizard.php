<?php
/**
 * nadlan-config - URBAN RENEWAL WIZARD "בדיקת התחדשות לבניין שלי" (L3, 2026-07-11).
 *
 * Flow: address/city -> declared-compound lookup (urban-hub endpoint) ->
 * building details -> optional PRIVATE doc upload + paste-text ->
 * AI first advisory (server-appended disclaimer, cost-guarded) ->
 * instant 3D of THEIR building (standard model, one badge per floor) ->
 * CTAs. Logged-out visitors get the funnel quick-register gate.
 *
 * PDF LAW (decision 2026-07-11): v1 analysis reads PASTED TEXT only - most
 * consent-stage docs are phone scans a text parser cannot read, and honest
 * labels beat a fake "we read your file". Files are still stored (private,
 * random names) for the future project space.
 *
 * Feature gate: option nadlan_feature_renewal_wizard ('1' = on). The AI
 * endpoint is additionally guarded by provider availability + cost caps.
 */

if ( ! defined( 'ABSPATH' ) ) { exit; }

if ( ! function_exists( 'nadlan_ur_wizard_on' ) ) {
	function nadlan_ur_wizard_on() { return get_option( 'nadlan_feature_renewal_wizard', '1' ) === '1'; }
}

if ( ! function_exists( 'nadlan_ur_rate_limited' ) ) {
	function nadlan_ur_rate_limited( $bucket, $cap, $window ) {
		$key = 'nadlan_ur_' . $bucket . '_' . get_current_user_id();
		$n   = (int) get_transient( $key );
		if ( $n >= $cap ) { return true; }
		set_transient( $key, $n + 1, $window );
		return false;
	}
}

/* ---------- private document upload (files stored, never parsed in v1) ---------- */
add_action( 'rest_api_init', function () {
	register_rest_route( 'nadlan/v1', '/renewal-doc', array(
		'methods'             => 'POST',
		'permission_callback' => function () { return is_user_logged_in() && nadlan_ur_wizard_on(); },
		'callback'            => function ( WP_REST_Request $req ) {
			if ( nadlan_ur_rate_limited( 'doc', 40, HOUR_IN_SECONDS ) ) {
				return new WP_Error( 'rate_limited', 'חרגתם ממכסת ההעלאות לשעה.', array( 'status' => 429 ) );
			}
			$files = $req->get_file_params();
			if ( empty( $files['doc'] ) ) { return new WP_Error( 'no_file', 'לא התקבל קובץ.', array( 'status' => 400 ) ); }
			$f = $files['doc'];
			if ( (int) $f['size'] > 10 * 1024 * 1024 ) { return new WP_Error( 'too_big', 'קובץ עד 10MB.', array( 'status' => 400 ) ); }
			$check = wp_check_filetype_and_ext( $f['tmp_name'], $f['name'] );
			$allowed = array( 'jpg', 'jpeg', 'png', 'webp', 'pdf' );
			if ( empty( $check['ext'] ) || ! in_array( strtolower( $check['ext'] ), $allowed, true ) ) {
				return new WP_Error( 'bad_type', 'מותר להעלות תמונות או PDF בלבד.', array( 'status' => 400 ) );
			}
			// privacy: unguessable name + dedicated dir + private attachment
			$f['name'] = wp_generate_password( 24, false, false ) . '-' . sanitize_file_name( $f['name'] );
			$dirfilter = function ( $dirs ) {
				$dirs['subdir'] = '/nadlan-renewal' . $dirs['subdir'];
				$dirs['path']   = $dirs['basedir'] . $dirs['subdir'];
				$dirs['url']    = $dirs['baseurl'] . $dirs['subdir'];
				return $dirs;
			};
			add_filter( 'upload_dir', $dirfilter );
			$moved = wp_handle_upload( $f, array( 'test_form' => false, 'mimes' => array(
				'jpg|jpeg' => 'image/jpeg', 'png' => 'image/png', 'webp' => 'image/webp', 'pdf' => 'application/pdf',
			) ) );
			remove_filter( 'upload_dir', $dirfilter );
			if ( ! is_array( $moved ) || empty( $moved['file'] ) ) {
				return new WP_Error( 'upload_failed', 'ההעלאה נכשלה, נסו שוב.', array( 'status' => 500 ) );
			}
			$att = wp_insert_attachment( array(
				'post_mime_type' => $moved['type'],
				'post_title'     => 'renewal-doc',
				'post_status'    => 'private',
				'post_author'    => get_current_user_id(),
			), $moved['file'] );
			if ( is_wp_error( $att ) || ! $att ) { return new WP_Error( 'attach_failed', 'שמירה נכשלה.', array( 'status' => 500 ) ); }
			update_post_meta( $att, 'nadlan_renewal_doc', '1' );
			// PRIVACY: never return the raw URL - only the id
			return array( 'attachment_id' => (int) $att, 'stored' => true );
		},
	) );
} );

/* ---------- AI first advisory (paste-text based, disclaimer server-side) ---------- */
if ( ! function_exists( 'nadlan_ur_advice_disclaimer' ) ) {
	function nadlan_ur_advice_disclaimer() {
		return 'זהו כלי מידע ראשוני בלבד. הניתוח אינו ייעוץ משפטי, אינו חוות דעת שמאית ואינו מחייב. כל הערכה כאן היא אומדן לא מחייב. לפני כל חתימה התייעצו עם עורך דין מטעם הדיירים.';
	}
}

add_action( 'rest_api_init', function () {
	register_rest_route( 'nadlan/v1', '/renewal-advise', array(
		'methods'             => 'POST',
		'permission_callback' => function () { return is_user_logged_in() && nadlan_ur_wizard_on(); },
		'callback'            => function ( WP_REST_Request $req ) {
			if ( nadlan_ur_rate_limited( 'adv', 8, HOUR_IN_SECONDS ) ) {
				return new WP_Error( 'rate_limited', 'חרגתם ממכסת הבדיקות לשעה.', array( 'status' => 429 ) );
			}
			if ( ! function_exists( 'nadlan_ai_chat' ) ) {
				return new WP_Error( 'no_ai', 'שירות הניתוח אינו זמין כרגע.', array( 'status' => 503 ) );
			}
			// cost preflight runs later with the REAL prompt (see below)
			$city    = mb_substr( sanitize_text_field( (string) $req->get_param( 'city' ) ), 0, 60 );
			$floors  = max( 1, min( 40, (int) $req->get_param( 'floors' ) ) );
			$units   = max( 2, min( 400, (int) $req->get_param( 'units' ) ) );
			$year    = max( 1900, min( 2020, (int) $req->get_param( 'year' ) ?: 1970 ) );
			$consents = max( 0, min( $units, (int) $req->get_param( 'consents' ) ) );
			$compound = mb_substr( sanitize_textarea_field( (string) $req->get_param( 'compound_facts' ) ), 0, 800 );
			$pasted   = mb_substr( sanitize_textarea_field( (string) $req->get_param( 'text' ) ), 0, 6000 );

			$facts = "עיר: {$city}. קומות: {$floors}. דירות: {$units}. שנת בנייה משוערת: {$year}. הסכמות שנאספו: {$consents} מתוך {$units}.";
			if ( $compound ) { $facts .= "\nנתוני מתחם מוכרז מהמאגר הרשמי: " . $compound; }
			if ( $pasted ) { $facts .= "\nטקסט שהבעלים הדביקו ממסמכים (מקור: המשתמש, לא אומת):\n" . $pasted; }
			$ctx = 'רפים חוקיים (2024): 66% מבעלי הדירות לקידום מתחם פינוי בינוי; 67% לתביעת דייר סרבן; בבניין בודד רוב מיוחס של 80% מהדירות ו-75% מהרכוש המשותף. ' .
				'מסלולים: פינוי בינוי (מתחם, הריסה); תמא 38/1 (חיזוק ללא פינוי); תמא 38/2 (הריסת בניין בודד); מסגרות עירוניות מחליפות את התמא בהדרגה. ' .
				'ממוצע משך פרויקט: קרוב לעשור. בעלי מקצוע לדיירים: עורך דין, שמאי, מפקח, מארגן.';

			$system = 'אתה יועץ ראשוני להתחדשות עירונית באתר נדלן. ענה אך ורק על סמך ההקשר והעובדות שסופקו. ' .
				'אסור להמציא רפים, סכומים או לוחות זמנים. אסור מקף ארוך - רק מקף רגיל. ' .
				'החזר JSON בלבד: {"track_fit":"pinui_binui|tama38_1|tama38_2|unclear","track_reason":"<עד 300 תווים>","consent_needed":"<עד 200 תווים>","next_steps":["<עד 120>","<עד 120>","<עד 120>"],"professionals":["lawyer","shamai","mefakeach","organizer" מתוך אלה בלבד],"confidence":0.0-1.0}' .
				( function_exists( 'nadlan_brain_house_rules' ) ? nadlan_brain_house_rules() : '' );
			$messages = array( array( 'role' => 'user', 'content' => "הקשר:\n" . $ctx . "\n\nעובדות הבניין:\n" . $facts ) );
			if ( function_exists( 'nadlan_lead_ai_preflight_cost' ) ) {
				$pre = nadlan_lead_ai_preflight_cost( $system, $messages, 900 );
				if ( is_wp_error( $pre ) ) { return new WP_Error( 'budget', 'מכסת הניתוח היומית מוצתה, נסו מחר.', array( 'status' => 503 ) ); }
			}
			$out = nadlan_ai_chat( $system, $messages, 900 );
			if ( is_wp_error( $out ) ) { return new WP_Error( 'ai_failed', 'הניתוח נכשל, נסו שוב.', array( 'status' => 502 ) ); }
			$txt = is_array( $out ) ? (string) ( $out['text'] ?? $out['content'] ?? '' ) : (string) $out;
			if ( ! preg_match( '/\{.*\}/s', $txt, $m ) ) { return new WP_Error( 'ai_badjson', 'תשובה לא תקינה, נסו שוב.', array( 'status' => 502 ) ); }
			$j = json_decode( $m[0], true );
			if ( ! is_array( $j ) ) { return new WP_Error( 'ai_badjson', 'תשובה לא תקינה, נסו שוב.', array( 'status' => 502 ) ); }
			// enum-clean
			$tracks = array( 'pinui_binui', 'tama38_1', 'tama38_2', 'unclear' );
			$pros   = array( 'lawyer', 'shamai', 'mefakeach', 'organizer' );
			$clean  = array(
				'track_fit'      => in_array( $j['track_fit'] ?? '', $tracks, true ) ? $j['track_fit'] : 'unclear',
				'track_reason'   => mb_substr( sanitize_text_field( (string) ( $j['track_reason'] ?? '' ) ), 0, 300 ),
				'consent_needed' => mb_substr( sanitize_text_field( (string) ( $j['consent_needed'] ?? '' ) ), 0, 200 ),
				'next_steps'     => array_slice( array_map( function ( $s ) { return mb_substr( sanitize_text_field( (string) $s ), 0, 120 ); }, (array) ( $j['next_steps'] ?? array() ) ), 0, 3 ),
				'professionals'  => array_values( array_intersect( (array) ( $j['professionals'] ?? array() ), $pros ) ),
				'confidence'     => max( 0, min( 1, (float) ( $j['confidence'] ?? 0.4 ) ) ),
				'in_declared_compound' => '' !== $compound,
				// THE DISCLAIMER IS APPENDED HERE, IN PHP - a prompt failure can never drop it
				'disclaimer'     => nadlan_ur_advice_disclaimer(),
			);
			return $clean;
		},
	) );
} );

/* ---------- the wizard page ---------- */
add_shortcode( 'nadlan_renewal_wizard', function () {
	if ( ! nadlan_ur_wizard_on() ) { return ''; }
	if ( ! is_user_logged_in() ) {
		// the proven quick-register gate (funnel.php endpoint)
		$reg = esc_url( rest_url( 'nadlan/v1/quick-register' ) );
		return '<div class="nlur-gate" dir="rtl"><h3>בדיקת התחדשות לבניין שלכם</h3><p>הבדיקה חינמית ושומרת את הנתונים שלכם לחדר הפרויקט. הרשמה בשדה אחד:</p>' .
			'<form onsubmit="return false" class="nlur-gate__f"><input type="text" id="nlurg-name" placeholder="שם"><input type="email" id="nlurg-email" placeholder="אימייל"><input type="tel" id="nlurg-phone" placeholder="טלפון"><input type="text" id="nlurg-web" style="display:none" tabindex="-1" autocomplete="off">' .
			'<button type="button" id="nlurg-go">מתחילים</button></form><div id="nlurg-msg" aria-live="polite"></div>' .
			'<style>.nlur-gate{background:#F3EEE3;border:1px solid #E2DCD0;border-radius:16px;padding:24px;max-width:560px;margin:20px auto}.nlur-gate h3{font-family:"Frank Ruhl Libre",serif;margin:0 0 6px}.nlur-gate p{font:400 14px Heebo;color:#51483A}.nlur-gate__f{display:flex;flex-direction:column;gap:8px;margin-top:10px}.nlur-gate__f input{border:1px solid #E2DCD0;border-radius:10px;padding:12px;font:400 14px Heebo}.nlur-gate__f button{background:#C2563A;color:#FAF7F1;border:0;border-radius:10px;padding:13px;font:700 15px Heebo;cursor:pointer}</style>' .
			'<script>document.getElementById("nlurg-go").addEventListener("click",function(){var m=document.getElementById("nlurg-msg");m.textContent="רושמים...";fetch("' . $reg . '",{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify({name:document.getElementById("nlurg-name").value,email:document.getElementById("nlurg-email").value,phone:document.getElementById("nlurg-phone").value,website:document.getElementById("nlurg-web").value})}).then(function(r){return r.json().then(function(j){return{ok:r.ok,j:j}})}).then(function(x){if(x.ok){location.reload()}else{m.textContent=(x.j&&x.j.message)||"שגיאה, נסו שוב"}}).catch(function(){m.textContent="שגיאה, נסו שוב"})});</script></div>';
	}
	$lookup = esc_url( rest_url( 'nadlan/v1/renewal-lookup' ) );
	$docurl = esc_url( rest_url( 'nadlan/v1/renewal-doc' ) );
	$advurl = esc_url( rest_url( 'nadlan/v1/renewal-advise' ) );
	$nonce  = wp_create_nonce( 'wp_rest' );
	$glb    = esc_url( function_exists( 'nadlan_showroom_engine_base_url' ) ? nadlan_showroom_engine_base_url() . 'models/standard-residential.glb' : '' );
	$js     = esc_url( plugins_url( 'assets/urban/renewal-3d.js', dirname( __FILE__ ) ) );
	$ver    = defined( 'NADLAN_CONFIG_VERSION' ) ? NADLAN_CONFIG_VERSION : '1';
	ob_start(); ?>
<div class="nlurw" dir="rtl" id="nlurw"
	data-lookup="<?php echo $lookup; // phpcs:ignore ?>" data-doc="<?php echo $docurl; // phpcs:ignore ?>"
	data-advise="<?php echo $advurl; // phpcs:ignore ?>" data-nonce="<?php echo esc_attr( $nonce ); ?>" data-glb="<?php echo $glb; // phpcs:ignore ?>">
	<ol class="nlurw-steps"><li class="is-on">כתובת</li><li>הבניין</li><li>מסמכים</li><li>ניתוח ראשוני</li><li>הבניין בתלת ממד</li></ol>

	<section class="nlurw-step" data-step="1">
		<h3>איפה הבניין?</h3>
		<div class="nlurw-f"><label>עיר<input type="text" id="nlurw-city" autocomplete="address-level2"></label>
		<label>רחוב ומספר<input type="text" id="nlurw-street"></label></div>
		<button type="button" class="nlurw-next" data-go="2">בדיקה מול מאגר המתחמים והמשך</button>
		<div id="nlurw-lookupres" class="nlurw-note" aria-live="polite"></div>
	</section>

	<section class="nlurw-step" data-step="2" hidden>
		<h3>קצת על הבניין</h3>
		<div class="nlurw-f">
			<label>קומות<input type="number" id="nlurw-floors" min="1" max="40" value="4"></label>
			<label>סך דירות<input type="number" id="nlurw-units" min="2" max="400" value="12"></label>
			<label>שנת בנייה משוערת<input type="number" id="nlurw-year" min="1900" max="2020" value="1970"></label>
			<label>כמה בעלי דירות כבר בעד?<input type="number" id="nlurw-consents" min="0" max="400" value="0"></label>
		</div>
		<button type="button" class="nlurw-next" data-go="3">המשך</button>
	</section>

	<section class="nlurw-step" data-step="3" hidden>
		<h3>מסמכים (לא חובה)</h3>
		<p class="nlurw-sub">אפשר להעלות נסח טאבו, פרוטוקול או מכתב יזם. הקבצים נשמרים לתיק הבניין בקישור חסוי שאינו מפורסם; הניתוח האוטומטי מתבסס על הטקסט שתדביקו למטה, לא על קריאת הקובץ. אל תעלו מידע רגיש שאינו נחוץ.</p>
		<input type="file" id="nlurw-file" accept=".pdf,.jpg,.jpeg,.png,.webp">
		<div id="nlurw-filemsg" class="nlurw-note" aria-live="polite"></div>
		<label class="nlurw-paste">הדביקו טקסט מהמסמכים (למשל סעיפים מהצעת היזם או מנסח הטאבו)<textarea id="nlurw-text" rows="5"></textarea></label>
		<button type="button" class="nlurw-next" data-go="4">קבלת ניתוח ראשוני</button>
	</section>

	<section class="nlurw-step" data-step="4" hidden>
		<h3>הניתוח הראשוני</h3>
		<div id="nlurw-adv" class="nlurw-adv" aria-live="polite">מנתחים את הנתונים...</div>
		<button type="button" class="nlurw-next" data-go="5">לצפייה בבניין בתלת ממד</button>
	</section>

	<section class="nlurw-step" data-step="5" hidden>
		<h3>ככה הבניין שלכם נראה בקומות</h3>
		<div id="nlurw-3d" class="nlurw-3d"></div>
		<p class="nlurw-note">הדמיה עקרונית לפי מספר הקומות שהזנתם - לא הבניין האמיתי.</p>
		<div class="nlurw-cta">
			<a class="nlurw-btn nlurw-btn--gold" href="/professionals/?context=renewal">מציאת עורך דין ושמאי לדיירים</a>
			<a class="nlurw-btn" href="/urban-renewal/">חזרה למדריך המלא</a>
		</div>
		<p class="nlurw-note">בקרוב: פתיחת חדר פרויקט לבניין, עם מפת הסכמות על המודל, מסמכים ועדכונים לשכנים.</p>
	</section>
</div>
<style>
.nlurw{max-width:720px;margin:0 auto;background:#fff;border:1px solid #E2DCD0;border-radius:18px;padding:24px}
.nlurw-steps{display:flex;gap:6px;list-style:none;padding:0;margin:0 0 18px;counter-reset:s}
.nlurw-steps li{flex:1;text-align:center;font:600 11.5px/1.3 Heebo;color:#8E877A;background:#F3EEE3;border-radius:8px;padding:8px 4px;counter-increment:s}
.nlurw-steps li.is-on{background:#1B1A17;color:#FAF7F1}
.nlurw h3{font-family:"Frank Ruhl Libre",serif;margin:0 0 10px}
.nlurw-f{display:grid;grid-template-columns:1fr 1fr;gap:10px;margin-bottom:14px}
@media(max-width:600px){.nlurw-f{grid-template-columns:1fr}}
.nlurw-f label,.nlurw-paste{display:flex;flex-direction:column;gap:5px;font:600 12.5px Heebo;color:#51483A}
.nlurw-f input,.nlurw-paste textarea{border:1px solid #E2DCD0;border-radius:10px;padding:12px;font:400 15px Heebo;background:#FAF7F1}
.nlurw-next{background:#C2563A;color:#FAF7F1;border:0;border-radius:10px;padding:13px 22px;font:700 14.5px Heebo;cursor:pointer;margin-top:10px}
.nlurw-note{font:400 12.5px/1.6 Heebo;color:#6D665C;margin-top:10px}
.nlurw-sub{font:400 13.5px/1.6 Heebo;color:#51483A}
.nlurw-adv{background:#F3EEE3;border-radius:12px;padding:16px;font:400 14.5px/1.7 Heebo;color:#1B1A17}
.nlurw-adv h4{font-family:"Frank Ruhl Libre",serif;margin:0 0 6px}
.nlurw-adv .d{font-size:11.5px;color:#8E877A;border-top:1px solid #E2DCD0;padding-top:8px;margin-top:10px}
.nlurw-3d{height:420px;border-radius:14px;overflow:hidden;background:#14130F}
.nlurw-cta{display:flex;gap:10px;flex-wrap:wrap;margin-top:12px}
.nlurw-btn{flex:1;text-align:center;border:1px solid #E2DCD0;border-radius:10px;padding:13px;font:700 14px Heebo;color:#1B1A17;text-decoration:none}
.nlurw-btn--gold{background:linear-gradient(180deg,#b9923f,#9C7A3C);color:#FAF7F1;border:0}
#nlurw-file{font:400 13px Heebo}
</style>
<script src="<?php echo $js; // phpcs:ignore ?>?ver=<?php echo esc_attr( $ver ); ?>" defer></script>
	<?php
	return ob_get_clean();
} );
