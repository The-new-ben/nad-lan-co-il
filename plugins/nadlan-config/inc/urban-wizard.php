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
	function nadlan_ur_advice_disclaimer( $lang = 'he' ) {
		if ( 'en' === $lang ) {
			return 'This is a first-orientation information tool only. The analysis is not legal advice, not an appraisal opinion and not binding. Every estimate here is a non-binding approximation. Before signing anything, consult a lawyer who represents the residents.';
		}
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
			$lang    = function_exists( 'nadlan_ur_req_lang' ) ? nadlan_ur_req_lang( (string) $req->get_param( 'lang' ) ) : 'he';
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
				( 'en' === $lang ? ' Write the VALUES of track_reason, consent_needed and next_steps in ENGLISH (the enum keys stay exactly as specified).' : '' ) .
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
				'disclaimer'     => nadlan_ur_advice_disclaimer( $lang ),
			);
			return $clean;
		},
	) );
} );

/* ---------- the wizard page (HE + EN via ?lang=en) ---------- */
if ( ! function_exists( 'nadlan_ur_wizard_strings' ) ) {
	function nadlan_ur_wizard_strings( $lang ) {
		if ( 'en' === $lang ) {
			return array(
				'gate_t' => 'A renewal check for your building', 'gate_p' => 'The check is free and saves your data for the project room. One-field signup:',
				'gate_name' => 'Name', 'gate_email' => 'Email', 'gate_phone' => 'Phone', 'gate_go' => 'Start', 'gate_busy' => 'Signing you up...', 'gate_err' => 'Error, try again',
				'steps' => array( 'Address', 'The building', 'Documents', 'First analysis', 'Your building in 3D' ),
				's1_t' => 'Where is the building?', 'city' => 'City', 'street' => 'Street and number', 's1_go' => 'Check the compounds registry and continue',
				's2_t' => 'About the building', 'floors' => 'Floors', 'units' => 'Total apartments', 'year' => 'Approximate build year', 'consents' => 'How many owners already agree?', 'cont' => 'Continue',
				's3_t' => 'Documents (optional)', 's3_p' => 'You can upload a Tabu extract, a protocol or a developer letter. Files are stored in the building file under a private link; the automatic analysis reads the TEXT you paste below, not the file. Do not upload sensitive information that is not needed.',
				'paste' => 'Paste text from the documents (for example clauses from the developer offer or the Tabu extract)', 's3_go' => 'Get the first analysis',
				's4_t' => 'The first analysis', 'analyzing' => 'Analyzing the data...', 's4_go' => 'See the building in 3D',
				's5_t' => 'This is how your building looks by floors', 's5_note' => 'A schematic visualization based on the floor count you entered - not the real building.',
				'cta_pros' => 'Find a residents-side lawyer and appraiser', 'cta_guide' => 'Back to the full guide',
				'cta_room' => 'Open a project room for the building - consent map on the model, documents and updates for the neighbors',
			);
		}
		return array(
			'gate_t' => 'בדיקת התחדשות לבניין שלכם', 'gate_p' => 'הבדיקה חינמית ושומרת את הנתונים שלכם לחדר הפרויקט. הרשמה בשדה אחד:',
			'gate_name' => 'שם', 'gate_email' => 'אימייל', 'gate_phone' => 'טלפון', 'gate_go' => 'מתחילים', 'gate_busy' => 'רושמים...', 'gate_err' => 'שגיאה, נסו שוב',
			'steps' => array( 'כתובת', 'הבניין', 'מסמכים', 'ניתוח ראשוני', 'הבניין בתלת ממד' ),
			's1_t' => 'איפה הבניין?', 'city' => 'עיר', 'street' => 'רחוב ומספר', 's1_go' => 'בדיקה מול מאגר המתחמים והמשך',
			's2_t' => 'קצת על הבניין', 'floors' => 'קומות', 'units' => 'סך דירות', 'year' => 'שנת בנייה משוערת', 'consents' => 'כמה בעלי דירות כבר בעד?', 'cont' => 'המשך',
			's3_t' => 'מסמכים (לא חובה)', 's3_p' => 'אפשר להעלות נסח טאבו, פרוטוקול או מכתב יזם. הקבצים נשמרים לתיק הבניין בקישור חסוי שאינו מפורסם; הניתוח האוטומטי מתבסס על הטקסט שתדביקו למטה, לא על קריאת הקובץ. אל תעלו מידע רגיש שאינו נחוץ.',
			'paste' => 'הדביקו טקסט מהמסמכים (למשל סעיפים מהצעת היזם או מנסח הטאבו)', 's3_go' => 'קבלת ניתוח ראשוני',
			's4_t' => 'הניתוח הראשוני', 'analyzing' => 'מנתחים את הנתונים...', 's4_go' => 'לצפייה בבניין בתלת ממד',
			's5_t' => 'ככה הבניין שלכם נראה בקומות', 's5_note' => 'הדמיה עקרונית לפי מספר הקומות שהזנתם - לא הבניין האמיתי.',
			'cta_pros' => 'מציאת עורך דין ושמאי לדיירים', 'cta_guide' => 'חזרה למדריך המלא',
			'cta_room' => 'פתיחת חדר פרויקט לבניין - מפת הסכמות על המודל, מסמכים ועדכונים לשכנים',
		);
	}
}
if ( ! function_exists( 'nadlan_ur_wizard_js_i18n' ) ) {
	function nadlan_ur_wizard_js_i18n( $lang ) {
		if ( 'en' === $lang ) {
			return array(
				'checking' => 'Checking the compounds registry...', 'found' => 'A declared compound was found nearby: ', 'found2' => '. Its data will be attached to the analysis.',
				'notfound' => 'No matching declared compound was found. That does not mean there is no potential - the single-building track does not appear in the registry.',
				'uploading' => 'Uploading...', 'uploaded' => 'The file was saved to the building file (private link). Remember: the analysis reads the text you paste below.', 'upfail' => 'The upload failed',
				'analyzing' => 'Analyzing the data...', 'unavailable' => 'The analysis is unavailable right now. The tools and the guide on the renewal page are always open.', 'failed' => 'The analysis failed, try again.',
				'track' => 'The likely track: ', 'consents' => 'Consents', 'steps' => 'Next steps', 'pros' => 'Relevant professionals',
				'tracks' => array( 'pinui_binui' => 'Pinui-Binui', 'tama38_1' => 'Reinforcement (TAMA 38/1)', 'tama38_2' => 'Demolish and rebuild (single building)', 'unclear' => 'Needs further checking' ),
				'prosmap' => array( 'lawyer' => 'Residents-side lawyer', 'shamai' => 'Real-estate appraiser', 'mefakeach' => 'Construction supervisor', 'organizer' => 'Organizer / administration' ),
			);
		}
		return array(
			'checking' => 'בודקים מול מאגר המתחמים...', 'found' => 'נמצא מתחם מוכרז קרוב: ', 'found2' => '. הנתונים יצורפו לניתוח.',
			'notfound' => 'לא נמצא מתחם מוכרז תואם. זה לא אומר שאין פוטנציאל - מסלול בניין בודד לא מופיע במאגר.',
			'uploading' => 'מעלים...', 'uploaded' => 'הקובץ נשמר לתיק הבניין (קישור חסוי). זכרו: הניתוח קורא את הטקסט שתדביקו למטה.', 'upfail' => 'ההעלאה נכשלה',
			'analyzing' => 'מנתחים את הנתונים...', 'unavailable' => 'הניתוח אינו זמין כרגע. הכלים והמדריך בעמוד ההתחדשות פתוחים תמיד.', 'failed' => 'הניתוח נכשל, נסו שוב.',
			'track' => 'המסלול המסתמן: ', 'consents' => 'הסכמות', 'steps' => 'הצעדים הבאים', 'pros' => 'אנשי מקצוע רלוונטיים',
			'tracks' => array( 'pinui_binui' => 'פינוי בינוי', 'tama38_1' => 'חיזוק (תמא 38/1)', 'tama38_2' => 'הריסה ובנייה לבניין בודד', 'unclear' => 'דרוש בירור נוסף' ),
			'prosmap' => array( 'lawyer' => 'עורך דין דיירים', 'shamai' => 'שמאי מקרקעין', 'mefakeach' => 'מפקח בנייה', 'organizer' => 'מארגן/מנהלת' ),
		);
	}
}
add_shortcode( 'nadlan_renewal_wizard', function () {
	if ( ! nadlan_ur_wizard_on() ) { return ''; }
	$lang = function_exists( 'nadlan_ur_req_lang' ) ? nadlan_ur_req_lang() : 'he';
	$en   = ( 'en' === $lang );
	$W    = nadlan_ur_wizard_strings( $lang );
	$dir  = $en ? 'ltr' : 'rtl';
	if ( ! is_user_logged_in() ) {
		// the proven quick-register gate (funnel.php endpoint)
		$reg = esc_url( rest_url( 'nadlan/v1/quick-register' ) );
		return '<div class="nlur-gate" dir="' . $dir . '"><h3>' . esc_html( $W['gate_t'] ) . '</h3><p>' . esc_html( $W['gate_p'] ) . '</p>' .
			'<form onsubmit="return false" class="nlur-gate__f"><input type="text" id="nlurg-name" placeholder="' . esc_attr( $W['gate_name'] ) . '"><input type="email" id="nlurg-email" placeholder="' . esc_attr( $W['gate_email'] ) . '"><input type="tel" id="nlurg-phone" placeholder="' . esc_attr( $W['gate_phone'] ) . '"><input type="text" id="nlurg-web" style="display:none" tabindex="-1" autocomplete="off">' .
			'<button type="button" id="nlurg-go">' . esc_html( $W['gate_go'] ) . '</button></form><div id="nlurg-msg" aria-live="polite"></div>' .
			'<style>.nlur-gate{background:#F3EEE3;border:1px solid #E2DCD0;border-radius:16px;padding:24px;max-width:560px;margin:20px auto}.nlur-gate h3{font-family:"Frank Ruhl Libre",serif;margin:0 0 6px}.nlur-gate p{font:400 14px Heebo;color:#51483A}.nlur-gate__f{display:flex;flex-direction:column;gap:8px;margin-top:10px}.nlur-gate__f input{border:1px solid #E2DCD0;border-radius:10px;padding:12px;font:400 14px Heebo}.nlur-gate__f button{background:#C2563A;color:#FAF7F1;border:0;border-radius:10px;padding:13px;font:700 15px Heebo;cursor:pointer}</style>' .
			'<script>document.getElementById("nlurg-go").addEventListener("click",function(){var m=document.getElementById("nlurg-msg");m.textContent="' . esc_js( $W['gate_busy'] ) . '";fetch("' . $reg . '",{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify({name:document.getElementById("nlurg-name").value,email:document.getElementById("nlurg-email").value,phone:document.getElementById("nlurg-phone").value,website:document.getElementById("nlurg-web").value})}).then(function(r){return r.json().then(function(j){return{ok:r.ok,j:j}})}).then(function(x){if(x.ok){location.reload()}else{m.textContent=(x.j&&x.j.message)||"' . esc_js( $W['gate_err'] ) . '"}}).catch(function(){m.textContent="' . esc_js( $W['gate_err'] ) . '"})});</script></div>';
	}
	$lookup = esc_url( rest_url( 'nadlan/v1/renewal-lookup' ) );
	$docurl = esc_url( rest_url( 'nadlan/v1/renewal-doc' ) );
	$advurl = esc_url( rest_url( 'nadlan/v1/renewal-advise' ) );
	$nonce  = wp_create_nonce( 'wp_rest' );
	$glb    = esc_url( function_exists( 'nadlan_showroom_engine_base_url' ) ? nadlan_showroom_engine_base_url() . 'models/standard-residential.glb' : '' );
	$js     = esc_url( plugins_url( 'assets/urban/renewal-3d.js', dirname( __FILE__ ) ) );
	$ver    = defined( 'NADLAN_CONFIG_VERSION' ) ? NADLAN_CONFIG_VERSION : '1';
	ob_start(); ?>
<div class="nlurw" dir="<?php echo esc_attr( $dir ); ?>" id="nlurw" data-lang="<?php echo esc_attr( $lang ); ?>"
	data-i18n="<?php echo esc_attr( wp_json_encode( nadlan_ur_wizard_js_i18n( $lang ), JSON_UNESCAPED_UNICODE ) ); ?>"
	data-lookup="<?php echo $lookup; // phpcs:ignore ?>" data-doc="<?php echo $docurl; // phpcs:ignore ?>"
	data-advise="<?php echo $advurl; // phpcs:ignore ?>" data-nonce="<?php echo esc_attr( $nonce ); ?>" data-glb="<?php echo $glb; // phpcs:ignore ?>">
	<ol class="nlurw-steps"><?php foreach ( $W['steps'] as $i => $st ) : ?><li<?php echo 0 === $i ? ' class="is-on"' : ''; ?>><?php echo esc_html( $st ); ?></li><?php endforeach; ?></ol>

	<section class="nlurw-step" data-step="1">
		<h3><?php echo esc_html( $W['s1_t'] ); ?></h3>
		<div class="nlurw-f"><label><?php echo esc_html( $W['city'] ); ?><input type="text" id="nlurw-city" autocomplete="address-level2"></label>
		<label><?php echo esc_html( $W['street'] ); ?><input type="text" id="nlurw-street"></label></div>
		<button type="button" class="nlurw-next" data-go="2"><?php echo esc_html( $W['s1_go'] ); ?></button>
		<div id="nlurw-lookupres" class="nlurw-note" aria-live="polite"></div>
	</section>

	<section class="nlurw-step" data-step="2" hidden>
		<h3><?php echo esc_html( $W['s2_t'] ); ?></h3>
		<div class="nlurw-f">
			<label><?php echo esc_html( $W['floors'] ); ?><input type="number" id="nlurw-floors" min="1" max="40" value="4"></label>
			<label><?php echo esc_html( $W['units'] ); ?><input type="number" id="nlurw-units" min="2" max="400" value="12"></label>
			<label><?php echo esc_html( $W['year'] ); ?><input type="number" id="nlurw-year" min="1900" max="2020" value="1970"></label>
			<label><?php echo esc_html( $W['consents'] ); ?><input type="number" id="nlurw-consents" min="0" max="400" value="0"></label>
		</div>
		<button type="button" class="nlurw-next" data-go="3"><?php echo esc_html( $W['cont'] ); ?></button>
	</section>

	<section class="nlurw-step" data-step="3" hidden>
		<h3><?php echo esc_html( $W['s3_t'] ); ?></h3>
		<p class="nlurw-sub"><?php echo esc_html( $W['s3_p'] ); ?></p>
		<input type="file" id="nlurw-file" accept=".pdf,.jpg,.jpeg,.png,.webp">
		<div id="nlurw-filemsg" class="nlurw-note" aria-live="polite"></div>
		<label class="nlurw-paste"><?php echo esc_html( $W['paste'] ); ?><textarea id="nlurw-text" rows="5"></textarea></label>
		<button type="button" class="nlurw-next" data-go="4"><?php echo esc_html( $W['s3_go'] ); ?></button>
	</section>

	<section class="nlurw-step" data-step="4" hidden>
		<h3><?php echo esc_html( $W['s4_t'] ); ?></h3>
		<div id="nlurw-adv" class="nlurw-adv" aria-live="polite"><?php echo esc_html( $W['analyzing'] ); ?></div>
		<button type="button" class="nlurw-next" data-go="5"><?php echo esc_html( $W['s4_go'] ); ?></button>
	</section>

	<section class="nlurw-step" data-step="5" hidden>
		<h3><?php echo esc_html( $W['s5_t'] ); ?></h3>
		<div id="nlurw-3d" class="nlurw-3d"></div>
		<p class="nlurw-note"><?php echo esc_html( $W['s5_note'] ); ?></p>
		<div class="nlurw-cta">
			<a class="nlurw-btn nlurw-btn--gold" href="<?php echo esc_url( home_url( '/my-renewal/' . ( $en ? '?lang=en' : '' ) ) ); ?>"><?php echo esc_html( $W['cta_room'] ); ?></a>
			<a class="nlurw-btn" href="<?php echo esc_url( home_url( '/professionals/?context=renewal' ) ); ?>"><?php echo esc_html( $W['cta_pros'] ); ?></a>
			<a class="nlurw-btn" href="<?php echo esc_url( home_url( $en ? '/urban-renewal/english-guide/' : '/urban-renewal/' ) ); ?>"><?php echo esc_html( $W['cta_guide'] ); ?></a>
		</div>
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
@media(max-width:600px){.nlurw-3d{height:60vh;min-height:380px}}
.nlurw-cta{display:flex;gap:10px;flex-wrap:wrap;margin-top:12px}
.nlurw-btn{flex:1;text-align:center;border:1px solid #E2DCD0;border-radius:10px;padding:13px;font:700 14px Heebo;color:#1B1A17;text-decoration:none}
.nlurw-btn--gold{background:linear-gradient(180deg,#b9923f,#9C7A3C);color:#FAF7F1;border:0}
#nlurw-file{font:400 13px Heebo}
</style>
<script src="<?php echo $js; // phpcs:ignore ?>?ver=<?php echo esc_attr( $ver ); ?>" defer></script>
	<?php
	return ob_get_clean();
} );
