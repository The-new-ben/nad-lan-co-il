<?php
/**
 * nadlan-config - URBAN RENEWAL PROJECT SPACE (L4 2026-07-12, PRODUCT v2 2026-07-12).
 *
 * The building's project room: per-apartment consent tracked and painted on
 * the 3D standard model, the 10-stage bureaucratic ladder, an updates feed
 * (send-gated, deliverability-last), invite-by-token membership, and the
 * /my-renewal/ surface. Documents live in urban-docs.php.
 *
 * PRODUCT v2 (owner order): /my-renewal/ is no longer a login wall.
 * Anonymous visitors get a real, INDEXABLE product landing (HE + EN via
 * ?lang=en) with a live read-only demo of the finished demo project -
 * 3D model full width ON TOP, interactive progress stepper attached under
 * it, a live map, an auto to-do list and a documents rollup - plus
 * "start here" steps and Create/Estimate CTAs. Members get the same v2
 * layout with editing. The app JS lives in assets/urban/renewal-space.js.
 *
 * PRIVACY BY CONSTRUCTION: CPT nadlan_renewal is public=false, no rewrite,
 * no REST show - there is NO front-end URL to index. All access flows
 * through the dashboard route + membership-checked REST. The ONLY public
 * read is GET /renewal-demo, which serves exclusively the is_demo space.
 *
 * Feature gate: option nadlan_feature_renewal_space ('1' = on).
 */

if ( ! defined( 'ABSPATH' ) ) { exit; }

if ( ! function_exists( 'nadlan_ur_space_on' ) ) {
	function nadlan_ur_space_on() { return get_option( 'nadlan_feature_renewal_space', '1' ) === '1'; }
}

/* ---------- CPT ---------- */
add_action( 'init', function () {
	register_post_type( 'nadlan_renewal', array(
		'labels'              => array( 'name' => 'חדרי התחדשות', 'singular_name' => 'חדר התחדשות' ),
		'public'              => false,
		'show_ui'             => true,
		'show_in_rest'        => false,
		'exclude_from_search' => true,
		'publicly_queryable'  => false,
		'rewrite'             => false,
		'has_archive'         => false,
		'show_in_menu'        => 'edit.php?post_type=nadlan_project',
		'supports'            => array( 'title' ),
		'capability_type'     => 'post',
		'map_meta_cap'        => true,
	) );
} );

/* ---------- consent enum + sanitizers ---------- */
if ( ! function_exists( 'nadlan_ur_consent_statuses' ) ) {
	function nadlan_ur_consent_statuses() {
		return array(
			'consented'    => array( 'חתמו', '#517048' ),
			'in_process'   => array( 'בתהליך', '#9C7A3C' ),
			'missing_docs' => array( 'חסרים מסמכים', '#C2563A' ),
			'refused'      => array( 'סירבו', '#7A2E1D' ),
			'unreached'    => array( 'טרם הושג קשר', '#A79E8D' ),
		);
	}
}
if ( ! function_exists( 'nadlan_ur_doc_keys' ) ) {
	function nadlan_ur_doc_keys() {
		return array( 'id_copy' => 'צילום תעודת זהות', 'ownership_nesach' => 'נסח טאבו', 'signed_agreement' => 'הסכם חתום', 'poa' => 'ייפוי כוח' );
	}
}
if ( ! function_exists( 'nadlan_ur_clean_apartments' ) ) {
	function nadlan_ur_clean_apartments( $raw ) {
		$statuses = array_keys( nadlan_ur_consent_statuses() );
		$dirs = array( 'west', 'east', 'north', 'south' );
		$out = array();
		foreach ( (array) $raw as $u ) {
			if ( ! is_array( $u ) || empty( $u['id'] ) ) { continue; }
			$docs = array();
			foreach ( array_keys( nadlan_ur_doc_keys() ) as $dk ) { $docs[ $dk ] = ! empty( $u['docs'][ $dk ] ); }
			$out[] = array(
				'id'             => sanitize_key( $u['id'] ),
				'floor'          => max( 0, min( 60, (int) ( $u['floor'] ?? 0 ) ) ),
				'pos'            => max( 0, min( 20, (int) ( $u['pos'] ?? 0 ) ) ),
				'dir'            => in_array( $u['dir'] ?? '', $dirs, true ) ? $u['dir'] : 'west',
				'label'          => mb_substr( sanitize_text_field( (string) ( $u['label'] ?? '' ) ), 0, 60 ),
				'consent_status' => in_array( $u['consent_status'] ?? '', $statuses, true ) ? $u['consent_status'] : 'unreached',
				'docs'           => $docs,
				'contact_note'   => mb_substr( sanitize_text_field( (string) ( $u['contact_note'] ?? '' ) ), 0, 200 ),
				'note'           => mb_substr( sanitize_text_field( (string) ( $u['note'] ?? '' ) ), 0, 400 ),
				'updated'        => current_time( 'mysql' ),
			);
			if ( count( $out ) >= 400 ) { break; }
		}
		return $out;
	}
}
if ( ! function_exists( 'nadlan_ur_apartment_completion' ) ) {
	function nadlan_ur_apartment_completion( $unit ) {
		$done = array(); $missing = array();
		foreach ( nadlan_ur_doc_keys() as $k => $label ) {
			if ( ! empty( $unit['docs'][ $k ] ) ) { $done[] = $label; } else { $missing[] = $label; }
		}
		$n = count( $done ) + count( $missing );
		return array( 'score' => $n ? (int) round( count( $done ) / $n * 100 ) : 0, 'done' => $done, 'missing' => $missing );
	}
}

/* ---------- membership ---------- */
if ( ! function_exists( 'nadlan_ur_members' ) ) {
	function nadlan_ur_members( $space_id ) {
		$m = json_decode( (string) get_post_meta( $space_id, 'member_emails', true ), true );
		return is_array( $m ) ? $m : array();
	}
}
if ( ! function_exists( 'nadlan_ur_can_manage' ) ) {
	function nadlan_ur_can_manage( $space_id ) {
		if ( current_user_can( 'manage_options' ) ) { return true; }
		return (int) get_post_meta( $space_id, 'owner_user_id', true ) === get_current_user_id() && get_current_user_id() > 0;
	}
}
if ( ! function_exists( 'nadlan_ur_can_view' ) ) {
	function nadlan_ur_can_view( $space_id ) {
		if ( nadlan_ur_can_manage( $space_id ) ) { return true; }
		$u = wp_get_current_user();
		if ( ! $u || ! $u->exists() ) { return false; }
		foreach ( nadlan_ur_members( $space_id ) as $m ) {
			if ( isset( $m['email'] ) && strtolower( $m['email'] ) === strtolower( $u->user_email ) ) { return true; }
		}
		return false;
	}
}
if ( ! function_exists( 'nadlan_ur_space_ok' ) ) {
	function nadlan_ur_space_ok( $id ) {
		$p = get_post( $id );
		return $p && 'nadlan_renewal' === $p->post_type && 'trash' !== $p->post_status;
	}
}

/* ---------- language pack (HE canonical, EN for non-Hebrew-speaking neighbors) ---------- */
if ( ! function_exists( 'nadlan_ur_req_lang' ) ) {
	function nadlan_ur_req_lang( $raw = null ) {
		if ( null === $raw ) { $raw = isset( $_GET['lang'] ) ? sanitize_key( wp_unslash( $_GET['lang'] ) ) : ''; } // phpcs:ignore WordPress.Security.NonceVerification
		return 'en' === $raw ? 'en' : 'he';
	}
}
if ( ! function_exists( 'nadlan_ur_statuses_lang' ) ) {
	function nadlan_ur_statuses_lang( $lang ) {
		$s = nadlan_ur_consent_statuses();
		if ( 'en' === $lang ) {
			$en = array( 'consented' => 'Signed', 'in_process' => 'In progress', 'missing_docs' => 'Missing documents', 'refused' => 'Refused', 'unreached' => 'Not yet reached' );
			foreach ( $en as $k => $label ) { if ( isset( $s[ $k ] ) ) { $s[ $k ][0] = $label; } }
		}
		return $s;
	}
}
if ( ! function_exists( 'nadlan_ur_doc_keys_lang' ) ) {
	function nadlan_ur_doc_keys_lang( $lang ) {
		if ( 'en' === $lang ) {
			return array( 'id_copy' => 'ID copy', 'ownership_nesach' => 'Land registry extract (Tabu)', 'signed_agreement' => 'Signed agreement', 'poa' => 'Power of attorney' );
		}
		return nadlan_ur_doc_keys();
	}
}

/* Per-stage playbook: label + what happens + typical duration + next actions.
   HE labels mirror nadlan_ur_ladder_labels() (urban-tools.php) - keep in sync. */
if ( ! function_exists( 'nadlan_ur_stage_meta' ) ) {
	function nadlan_ur_stage_meta( $lang = 'he' ) {
		if ( 'en' === $lang ) {
			return array(
				array( 'label' => 'First organizing', 'desc' => 'A first residents assembly, a written protocol and a full map of the apartment owners.', 'duration' => '1-3 months', 'actions' => array( 'Hold a first residents assembly', 'Collect contact details for every apartment owner', 'Check the building against the official declared-compounds registry' ) ),
				array( 'label' => 'Electing a committee', 'desc' => '3-5 neighbors elected with a written mandate to run the process on behalf of the building.', 'duration' => '1-2 months', 'actions' => array( 'Vote on a residents committee', 'Sign a written appointment letter', 'Open a single updates channel for all neighbors' ) ),
				array( 'label' => 'Collecting signatures', 'desc' => 'Signing the owners on an agreement in principle, with full transparency to the whole building.', 'duration' => '6-18 months', 'actions' => array( 'Update the status of every apartment on the model', 'Handle apartments with inheritance or missing papers', 'Track the legal thresholds: 66% / 67% / 80%' ) ),
				array( 'label' => 'Hiring professionals', 'desc' => 'A lawyer and an appraiser who work for the RESIDENTS - paid by the developer, chosen by you.', 'duration' => '2-4 months', 'actions' => array( 'Collect offers from experienced tenants-side lawyers', 'Choose an appraiser on behalf of the residents', 'Sign fee agreements' ) ),
				array( 'label' => 'Choosing a developer', 'desc' => 'A developer tender: track record, financial strength and guarantees.', 'duration' => '4-8 months', 'actions' => array( 'Prepare the residents requirements document', 'Compare developer offers side by side', 'Verify sale-law guarantees and securities' ) ),
				array( 'label' => 'Planning approval', 'desc' => 'The plan moves through the planning committees - the biggest variable in the whole timeline.', 'duration' => '2-5 years', 'actions' => array( 'Follow the planning process with the committee', 'Update neighbors on every decision', 'Stay in touch with the municipal renewal administration' ) ),
				array( 'label' => 'Building permit', 'desc' => 'Final technical specification and the apartment-selection process.', 'duration' => '1-2 years', 'actions' => array( 'Sign the final specification annex', 'Run the apartment selection by the agreed formula', 'Prepare rental agreements for the move-out' ) ),
				array( 'label' => 'Moving out', 'desc' => 'The building is vacated - rent is paid by the developer until delivery.', 'duration' => '1-3 months', 'actions' => array( 'Sign rental agreements', 'Coordinate the moves', 'Hand keys to the developer' ) ),
				array( 'label' => 'Construction', 'desc' => 'The construction itself - the residents-side supervisor reports to the committee.', 'duration' => '2-4 years', 'actions' => array( 'Review periodic supervision reports', 'Coordinate resident site visits', 'Track the schedule against the agreement' ) ),
				array( 'label' => 'Delivery and registration', 'desc' => 'Occupancy permit, apartment handover, the warranty year and Tabu registration.', 'duration' => '6-18 months', 'actions' => array( 'Run a handover protocol for every apartment', 'Track warranty-year fixes', 'Register the shared building in the land registry' ) ),
			);
		}
		return array(
			array( 'label' => 'התארגנות ראשונית', 'desc' => 'אסיפת דיירים ראשונה, פרוטוקול כתוב ומיפוי מלא של בעלי הדירות.', 'duration' => '1-3 חודשים', 'actions' => array( 'כינוס אסיפת דיירים ראשונה', 'איסוף פרטי קשר של כל בעלי הדירות', 'בדיקת הבניין מול מאגר המתחמים המוכרזים' ) ),
			array( 'label' => 'בחירת נציגות', 'desc' => 'בחירת 3-5 שכנים עם מנדט כתוב לנהל את התהליך בשם הבניין.', 'duration' => 'חודש-חודשיים', 'actions' => array( 'הצבעה על נציגות דיירים', 'חתימה על כתב מינוי', 'פתיחת ערוץ עדכונים אחד לכל השכנים' ) ),
			array( 'label' => 'החתמות', 'desc' => 'החתמת בעלי הדירות על הסכמה עקרונית, בשקיפות מלאה לכל הבניין.', 'duration' => '6-18 חודשים', 'actions' => array( 'עדכון סטטוס לכל דירה על המודל', 'טיפול בדירות עם ירושה או מסמכים חסרים', 'מעקב אחרי הרפים בחוק: 66% / 67% / 80%' ) ),
			array( 'label' => 'בחירת אנשי מקצוע', 'desc' => 'עורך דין ושמאי שעובדים בשביל הדיירים - בשכר היזם, לפי בחירתכם.', 'duration' => '2-4 חודשים', 'actions' => array( 'קבלת הצעות מעורכי דין מלווים מנוסים', 'בחירת שמאי מטעם הדיירים', 'חתימה על הסכמי שכר טרחה' ) ),
			array( 'label' => 'בחירת יזם', 'desc' => 'מכרז יזמים: ניסיון מוכח, איתנות פיננסית ובטוחות.', 'duration' => '4-8 חודשים', 'actions' => array( 'הכנת מסמך דרישות הדיירים', 'השוואת הצעות יזמים זו מול זו', 'בדיקת ערבויות חוק מכר ובטוחות' ) ),
			array( 'label' => 'תב"ע ותכנון', 'desc' => 'התוכנית עוברת בוועדות התכנון - המשתנה הגדול ביותר בלוח הזמנים.', 'duration' => '2-5 שנים', 'actions' => array( 'ליווי הליך התכנון מול הוועדה', 'עדכון השכנים בכל החלטה', 'קשר שוטף עם מנהלת ההתחדשות העירונית' ) ),
			array( 'label' => 'היתר בנייה', 'desc' => 'מפרט טכני סופי והליך בחירת דירות התמורה.', 'duration' => 'שנה-שנתיים', 'actions' => array( 'חתימה על נספח המפרט הסופי', 'הליך בחירת דירות לפי הנוסחה שנקבעה', 'היערכות להסכמי שכירות לפינוי' ) ),
			array( 'label' => 'פינוי', 'desc' => 'פינוי הבניין - שכר הדירה במימון היזם עד המסירה.', 'duration' => '1-3 חודשים', 'actions' => array( 'חתימה על הסכמי שכירות', 'תיאום הובלות', 'מסירת מפתחות ליזם' ) ),
			array( 'label' => 'בנייה', 'desc' => 'הבנייה עצמה - המפקח מטעם הדיירים מדווח לנציגות.', 'duration' => '2-4 שנים', 'actions' => array( 'מעבר על דוחות פיקוח תקופתיים', 'ביקורי דיירים מתואמים באתר', 'מעקב לוח הזמנים מול ההסכם' ) ),
			array( 'label' => 'מסירה ורישום', 'desc' => 'טופס 4, מסירת הדירות, שנת הבדק ורישום בטאבו.', 'duration' => '6-18 חודשים', 'actions' => array( 'פרוטוקול מסירה לכל דירה', 'מעקב תיקוני שנת בדק', 'רישום הבית המשותף בטאבו' ) ),
		);
	}
}

/* UI strings for the app JS (data-i18n) */
if ( ! function_exists( 'nadlan_ur_space_strings' ) ) {
	function nadlan_ur_space_strings( $lang = 'he' ) {
		if ( 'en' === $lang ) {
			return array(
				'load_fail' => 'Could not load the project room.', 'consent_mix' => 'Consent mix', 'gauge' => 'signed',
				'hint_3d' => 'Tap an apartment on the model for its status and documents', 'apt_title' => 'Selected apartment',
				'apt_hint' => 'Tap an apartment on the 3D model to see and update its consent status and documents.',
				'map_title' => 'On the map', 'updates' => 'Updates for the neighbors', 'upd_ph' => 'What is new in the project?',
				'upd_send' => 'Post update', 'upd_none' => 'No updates yet.', 'inv_title' => 'Invite the neighbors',
				'inv_note' => 'Anyone opening the link joins the room in read-only mode. Share it in the building WhatsApp group.',
				'inv_btn' => 'Create invite link', 'history' => 'Stage history', 'typical' => 'Typical duration',
				'avg_note' => 'national averages, not a promise', 'next_actions' => 'Next actions', 'reached_at' => 'Reached on',
				'set_stage' => 'Set as current stage', 'td_map' => 'Map every apartment (no "not yet reached")',
				'td_66' => '66% signed - advancing a pinui-binui compound', 'td_67' => '67% signed - suing a refusing owner is possible',
				'td_80' => '80% signed - special majority for a single building', 'td_docs' => 'Full document file for every apartment',
				'td_pros' => 'Residents-side lawyer and appraiser chosen', 'td_dev' => 'Developer chosen in a tender',
				'todo_title' => 'Building to-do list', 'now_actions' => 'Now, at the current stage',
				'todo_note' => 'Derived automatically from the room data. Not legal advice.',
				'docs_title' => 'Documents rollup', 'docs_hint' => 'Update documents per apartment by tapping it on the model.',
				'docs_of' => 'Documents', 'floor' => 'Floor', 'save' => 'Save', 'compounds' => 'Declared compounds in the city',
				'map_approx' => 'Approximate city location', 'demo_badge' => 'Sample data',
				'track_pinui_binui' => 'Pinui-Binui', 'track_tama38_1' => 'Reinforcement (TAMA 38/1)', 'track_tama38_2' => 'Demolish and rebuild', 'track_unclear' => 'Track not decided yet',
			);
		}
		return array(
			'load_fail' => 'לא הצלחנו לטעון את חדר הפרויקט.', 'consent_mix' => 'תמהיל הסכמות', 'gauge' => 'חתמו',
			'hint_3d' => 'הקישו על דירה במודל לסטטוס ולמסמכים שלה', 'apt_title' => 'הדירה שנבחרה',
			'apt_hint' => 'הקישו על דירה במודל התלת-ממדי כדי לראות ולעדכן את סטטוס ההסכמה והמסמכים שלה.',
			'map_title' => 'על המפה', 'updates' => 'עדכונים לשכנים', 'upd_ph' => 'מה חדש בפרויקט?',
			'upd_send' => 'פרסום עדכון', 'upd_none' => 'אין עדכונים עדיין.', 'inv_title' => 'הזמנת השכנים',
			'inv_note' => 'כל מי שנכנס עם הקישור מצטרף לחדר לקריאה בלבד. שתפו אותו בקבוצת הוואטסאפ של הבניין.',
			'inv_btn' => 'יצירת קישור הזמנה', 'history' => 'היסטוריית שלבים', 'typical' => 'משך אופייני',
			'avg_note' => 'ממוצעים ארציים, לא הבטחה', 'next_actions' => 'הצעדים הבאים', 'reached_at' => 'הושג בתאריך',
			'set_stage' => 'קביעה כשלב הנוכחי', 'td_map' => 'מיפוי כל הדירות (אפס "טרם הושג קשר")',
			'td_66' => '66% חתימות - קידום מתחם פינוי בינוי', 'td_67' => '67% חתימות - אפשר לתבוע דייר סרבן',
			'td_80' => '80% חתימות - רוב מיוחס לבניין בודד', 'td_docs' => 'תיק מסמכים מלא לכל דירה',
			'td_pros' => 'נבחרו עורך דין ושמאי מטעם הדיירים', 'td_dev' => 'נבחר יזם במכרז',
			'todo_title' => 'רשימת המשימות של הבניין', 'now_actions' => 'עכשיו, בשלב הנוכחי',
			'todo_note' => 'נגזר אוטומטית מנתוני החדר. אין לראות בכך ייעוץ משפטי.',
			'docs_title' => 'תמונת המסמכים', 'docs_hint' => 'מעדכנים מסמכים לכל דירה בהקשה עליה במודל.',
			'docs_of' => 'מסמכים', 'floor' => 'קומה', 'save' => 'שמירה', 'compounds' => 'מתחמים מוכרזים בעיר',
			'map_approx' => 'מיקום משוער ברמת העיר', 'demo_badge' => 'נתוני דוגמה',
			'track_pinui_binui' => 'פינוי בינוי', 'track_tama38_1' => 'חיזוק (תמ"א 38/1)', 'track_tama38_2' => 'הריסה ובנייה', 'track_unclear' => 'המסלול טרם הוכרע',
		);
	}
}

/* ---------- geo helpers (honest: centroid = city level, geocode happens client-side) ---------- */
if ( ! function_exists( 'nadlan_ur_space_centroid' ) ) {
	function nadlan_ur_space_centroid( $city ) {
		if ( ! function_exists( 'nadlan_ur_city_centroids' ) || '' === trim( (string) $city ) ) { return null; }
		$norm = function ( $s ) { return trim( str_replace( array( '-', '  ' ), ' ', (string) $s ) ); };
		$want = $norm( $city );
		foreach ( nadlan_ur_city_centroids() as $name => $ll ) {
			if ( $norm( $name ) === $want ) { return array( (float) $ll[0], (float) $ll[1] ); }
		}
		return null;
	}
}
if ( ! function_exists( 'nadlan_ur_city_compound_count' ) ) {
	function nadlan_ur_city_compound_count( $city ) {
		$city = trim( (string) $city );
		if ( '' === $city ) { return null; }
		$key = 'nlur_ccnt_' . md5( $city );
		$n = get_transient( $key );
		if ( false === $n ) {
			$ids = get_posts( array( 'post_type' => 'nadlan_project', 'post_status' => 'publish', 'posts_per_page' => -1,
				'fields' => 'ids', 'no_found_rows' => true, 'meta_query' => array(
					array( 'key' => 'source', 'value' => 'urban_renewal' ),
					array( 'key' => 'city', 'value' => $city, 'compare' => 'LIKE' ),
				) ) );
			$n = count( $ids );
			set_transient( $key, $n, 6 * HOUR_IN_SECONDS );
		}
		return (int) $n;
	}
}

/* ---------- space payload ---------- */
if ( ! function_exists( 'nadlan_ur_space_payload' ) ) {
	function nadlan_ur_space_payload( $id, $lang = 'he' ) {
		$apts = json_decode( (string) get_post_meta( $id, 'renewal_apartments', true ), true );
		$apts = is_array( $apts ) ? $apts : array();
		$total = count( $apts );
		$yes = count( array_filter( $apts, function ( $a ) { return ( $a['consent_status'] ?? '' ) === 'consented'; } ) );
		$city = (string) get_post_meta( $id, 'city', true );
		$meta = nadlan_ur_stage_meta( $lang );
		return array(
			'id'        => (int) $id,
			'title'     => get_the_title( $id ),
			'address'   => (string) get_post_meta( $id, 'address', true ),
			'city'      => $city,
			'floors'    => (int) get_post_meta( $id, 'floors', true ),
			'units_per_floor' => (int) get_post_meta( $id, 'units_per_floor', true ),
			'track'     => (string) get_post_meta( $id, 'track', true ),
			'stage'     => (int) get_post_meta( $id, 'renewal_stage', true ),
			'ladder'    => array_column( $meta, 'label' ),
			'stage_notes' => array_map( function ( $m ) { return array( 'desc' => $m['desc'], 'duration' => $m['duration'], 'actions' => $m['actions'] ); }, $meta ),
			'apartments' => $apts,
			'consents'  => array( 'yes' => $yes, 'total' => $total, 'pct' => $total ? round( $yes / $total * 100, 1 ) : 0 ),
			'updates'   => array_slice( (array) json_decode( (string) get_post_meta( $id, 'renewal_updates', true ), true ), 0, 30 ),
			'stage_log' => array_slice( array_reverse( (array) json_decode( (string) get_post_meta( $id, 'renewal_stage_log', true ), true ) ), 0, 12 ),
			'can_manage' => nadlan_ur_can_manage( $id ),
			'is_demo'   => '1' === (string) get_post_meta( $id, 'is_demo', true ),
			'statuses'  => nadlan_ur_statuses_lang( $lang ),
			'doc_keys'  => nadlan_ur_doc_keys_lang( $lang ),
			'centroid'  => nadlan_ur_space_centroid( $city ),
			'compounds_in_city' => nadlan_ur_city_compound_count( $city ),
		);
	}
}

/* ---------- REST ---------- */
add_action( 'rest_api_init', function () {
	$view_perm = function ( $req ) { return is_user_logged_in() && nadlan_ur_space_on() && nadlan_ur_space_ok( (int) $req['id'] ) && nadlan_ur_can_view( (int) $req['id'] ); };
	$mng_perm  = function ( $req ) { return is_user_logged_in() && nadlan_ur_space_on() && nadlan_ur_space_ok( (int) $req['id'] ) && nadlan_ur_can_manage( (int) $req['id'] ); };

	/* PUBLIC read-only demo: serves ONLY the is_demo space (the product landing's live demo) */
	register_rest_route( 'nadlan/v1', '/renewal-demo', array(
		'methods' => 'GET',
		'permission_callback' => function () { return nadlan_ur_space_on(); },
		'callback' => function ( WP_REST_Request $req ) {
			$lang = nadlan_ur_req_lang( (string) $req->get_param( 'lang' ) );
			$key = 'nlur_demo_payload_' . $lang;
			$p = get_transient( $key );
			if ( ! is_array( $p ) ) {
				$ids = get_posts( array( 'post_type' => 'nadlan_renewal', 'post_status' => 'any', 'posts_per_page' => 1,
					'fields' => 'ids', 'meta_query' => array( array( 'key' => 'is_demo', 'value' => '1' ) ) ) );
				if ( ! $ids ) { return new WP_Error( 'not_found', 'no demo space', array( 'status' => 404 ) ); }
				$p = nadlan_ur_space_payload( (int) $ids[0], $lang );
				$p['can_manage'] = false;
				set_transient( $key, $p, 10 * MINUTE_IN_SECONDS );
			}
			$p['can_manage'] = false; // belt and braces: the demo is never editable over this route
			return $p;
		},
	) );

	register_rest_route( 'nadlan/v1', '/renewal-space', array(
		'methods' => 'POST',
		'permission_callback' => function () { return is_user_logged_in() && nadlan_ur_space_on(); },
		'callback' => function ( WP_REST_Request $req ) {
			if ( nadlan_ur_rate_limited( 'space', 5, DAY_IN_SECONDS ) ) {
				return new WP_Error( 'rate_limited', 'אפשר לפתוח עד 5 חדרים ביום.', array( 'status' => 429 ) );
			}
			$city   = mb_substr( sanitize_text_field( (string) $req->get_param( 'city' ) ), 0, 60 );
			$addr   = mb_substr( sanitize_text_field( (string) $req->get_param( 'address' ) ), 0, 120 );
			$floors = max( 1, min( 40, (int) $req->get_param( 'floors' ) ) );
			$upf    = max( 1, min( 12, (int) $req->get_param( 'units_per_floor' ) ) );
			if ( '' === $addr || '' === $city ) { return new WP_Error( 'bad_request', 'נדרשות עיר וכתובת.', array( 'status' => 400 ) ); }
			$id = wp_insert_post( array(
				'post_type' => 'nadlan_renewal', 'post_status' => 'private',
				'post_title' => $addr . ', ' . $city,
			), true );
			if ( is_wp_error( $id ) ) { return $id; }
			// seed the consent grid: every apartment starts unreached
			$dirs = array( 'west', 'south', 'east', 'north' );
			$apts = array();
			for ( $f = 1; $f <= $floors; $f++ ) {
				for ( $p = 0; $p < $upf; $p++ ) {
					$apts[] = array( 'id' => 'f' . $f . '-' . ( $p + 1 ), 'floor' => $f, 'pos' => $p,
						'dir' => $dirs[ $p % 4 ], 'label' => 'דירה ' . ( ( $f - 1 ) * $upf + $p + 1 ),
						'consent_status' => 'unreached', 'docs' => array(), 'contact_note' => '', 'note' => '' );
				}
			}
			update_post_meta( $id, 'owner_user_id', get_current_user_id() );
			update_post_meta( $id, 'address', $addr );
			update_post_meta( $id, 'city', $city );
			update_post_meta( $id, 'floors', $floors );
			update_post_meta( $id, 'units_per_floor', $upf );
			update_post_meta( $id, 'track', sanitize_key( (string) $req->get_param( 'track' ) ) );
			update_post_meta( $id, 'renewal_stage', 0 );
			update_post_meta( $id, 'renewal_apartments', wp_slash( wp_json_encode( nadlan_ur_clean_apartments( $apts ), JSON_UNESCAPED_UNICODE ) ) );
			update_post_meta( $id, 'member_emails', wp_slash( wp_json_encode( array(), JSON_UNESCAPED_UNICODE ) ) );
			update_post_meta( $id, 'invite_token', wp_generate_password( 24, false, false ) );
			return array( 'id' => (int) $id, 'url' => home_url( '/my-renewal/?space=' . (int) $id ) );
		},
	) );

	register_rest_route( 'nadlan/v1', '/renewal-space/(?P<id>\d+)', array(
		'methods' => 'GET', 'permission_callback' => $view_perm,
		'callback' => function ( $req ) { return nadlan_ur_space_payload( (int) $req['id'], nadlan_ur_req_lang( (string) $req->get_param( 'lang' ) ) ); },
	) );

	register_rest_route( 'nadlan/v1', '/renewal-space/(?P<id>\d+)/apartments', array(
		'methods' => 'POST', 'permission_callback' => $mng_perm,
		'callback' => function ( WP_REST_Request $req ) {
			$id = (int) $req['id'];
			$clean = nadlan_ur_clean_apartments( (array) $req->get_param( 'apartments' ) );
			update_post_meta( $id, 'renewal_apartments', wp_slash( wp_json_encode( $clean, JSON_UNESCAPED_UNICODE ) ) );
			return nadlan_ur_space_payload( $id, nadlan_ur_req_lang( (string) $req->get_param( 'lang' ) ) );
		},
	) );

	register_rest_route( 'nadlan/v1', '/renewal-space/(?P<id>\d+)/stage', array(
		'methods' => 'POST', 'permission_callback' => $mng_perm,
		'callback' => function ( WP_REST_Request $req ) {
			$id = (int) $req['id'];
			$st = max( 0, min( 9, (int) $req->get_param( 'stage' ) ) );
			update_post_meta( $id, 'renewal_stage', $st );
			$log = (array) json_decode( (string) get_post_meta( $id, 'renewal_stage_log', true ), true );
			$log[] = array( 'stage' => $st, 'at' => current_time( 'mysql' ), 'by' => get_current_user_id() );
			update_post_meta( $id, 'renewal_stage_log', wp_slash( wp_json_encode( array_slice( $log, -60 ), JSON_UNESCAPED_UNICODE ) ) );
			nadlan_ur_queue_notice( $id, 'הפרויקט התקדם לשלב: ' . ( nadlan_ur_ladder_labels()[ $st ] ?? $st ) );
			return nadlan_ur_space_payload( $id, nadlan_ur_req_lang( (string) $req->get_param( 'lang' ) ) );
		},
	) );

	register_rest_route( 'nadlan/v1', '/renewal-space/(?P<id>\d+)/update', array(
		'methods' => 'POST', 'permission_callback' => $mng_perm,
		'callback' => function ( WP_REST_Request $req ) {
			$id = (int) $req['id'];
			$text = mb_substr( sanitize_textarea_field( (string) $req->get_param( 'text' ) ), 0, 1000 );
			if ( '' === $text ) { return new WP_Error( 'bad_request', 'עדכון ריק.', array( 'status' => 400 ) ); }
			$ups = (array) json_decode( (string) get_post_meta( $id, 'renewal_updates', true ), true );
			array_unshift( $ups, array( 'text' => $text, 'at' => current_time( 'mysql' ), 'by' => get_current_user_id() ) );
			update_post_meta( $id, 'renewal_updates', wp_slash( wp_json_encode( array_slice( $ups, 0, 200 ), JSON_UNESCAPED_UNICODE ) ) );
			nadlan_ur_queue_notice( $id, $text );
			return nadlan_ur_space_payload( $id, nadlan_ur_req_lang( (string) $req->get_param( 'lang' ) ) );
		},
	) );

	register_rest_route( 'nadlan/v1', '/renewal-space/(?P<id>\d+)/invite', array(
		'methods' => 'POST', 'permission_callback' => $mng_perm,
		'callback' => function ( $req ) {
			$id = (int) $req['id'];
			$tok = wp_generate_password( 24, false, false );
			update_post_meta( $id, 'invite_token', $tok );
			return array( 'join_url' => home_url( '/my-renewal/?join=' . rawurlencode( $tok ) ) );
		},
	) );

	register_rest_route( 'nadlan/v1', '/renewal-join/(?P<token>[A-Za-z0-9]{24})', array(
		'methods' => 'POST',
		'permission_callback' => function () { return is_user_logged_in() && nadlan_ur_space_on(); },
		'callback' => function ( $req ) {
			$tok = (string) $req['token'];
			$q = get_posts( array( 'post_type' => 'nadlan_renewal', 'post_status' => 'any', 'posts_per_page' => 1, 'fields' => 'ids',
				'meta_query' => array( array( 'key' => 'invite_token', 'value' => $tok ) ) ) );
			if ( ! $q ) { return new WP_Error( 'bad_token', 'קישור ההזמנה אינו תקף.', array( 'status' => 404 ) ); }
			$id = (int) $q[0];
			$u = wp_get_current_user();
			$members = nadlan_ur_members( $id );
			foreach ( $members as $m ) { if ( strtolower( $m['email'] ?? '' ) === strtolower( $u->user_email ) ) { return array( 'id' => $id, 'joined' => true ); } }
			$members[] = array( 'email' => $u->user_email, 'joined' => current_time( 'mysql' ) );
			update_post_meta( $id, 'member_emails', wp_slash( wp_json_encode( array_slice( $members, 0, 400 ), JSON_UNESCAPED_UNICODE ) ) );
			return array( 'id' => $id, 'joined' => true );
		},
	) );

	register_rest_route( 'nadlan/v1', '/renewal-notify-queue', array(
		'methods' => 'GET',
		'permission_callback' => function () { return current_user_can( 'manage_options' ); },
		'callback' => function () {
			return array( 'enabled' => get_option( 'nadlan_renewal_notify_enabled', '0' ) === '1',
				'log' => (array) get_option( 'nadlan_ur_notify_log', array() ) );
		},
	) );
} );

/* clear the cached demo payload whenever any renewal space is saved */
add_action( 'save_post_nadlan_renewal', function () {
	delete_transient( 'nlur_demo_payload_he' );
	delete_transient( 'nlur_demo_payload_en' );
} );

/* ---------- member notices (deliverability-last: OFF until flipped) ---------- */
if ( ! function_exists( 'nadlan_ur_queue_notice' ) ) {
	function nadlan_ur_queue_notice( $space_id, $text ) {
		$members = nadlan_ur_members( $space_id );
		$entry = array( 'space' => (int) $space_id, 'text' => mb_substr( $text, 0, 200 ),
			'recipients' => count( $members ), 'at' => current_time( 'mysql' ), 'sent' => false );
		if ( get_option( 'nadlan_renewal_notify_enabled', '0' ) === '1' && $members ) {
			$subject = 'עדכון מחדר ההתחדשות: ' . get_the_title( $space_id );
			$body = '<div dir="rtl" style="font-family:Heebo,Arial,sans-serif;max-width:540px;margin:0 auto">' .
				'<p style="color:#1B1A17;line-height:1.7">' . esc_html( $text ) . '</p>' .
				'<p><a href="' . esc_url( home_url( '/my-renewal/?space=' . (int) $space_id ) ) . '" style="display:inline-block;background:#9C7A3C;color:#FAF7F1;font-weight:700;border-radius:10px;padding:12px 18px;text-decoration:none">לחדר הפרויקט</a></p>' .
				'<p style="font-size:11.5px;color:#6D665C">קיבלתם עדכון זה כחברים בחדר ההתחדשות של הבניין באתר nad-lan.co.il.</p></div>';
			foreach ( $members as $m ) {
				if ( ! empty( $m['email'] ) && is_email( $m['email'] ) ) {
					wp_mail( $m['email'], $subject, $body, array( 'Content-Type: text/html; charset=UTF-8' ) );
				}
			}
			$entry['sent'] = true;
		}
		$q = (array) get_option( 'nadlan_ur_notify_log', array() );
		array_unshift( $q, $entry );
		update_option( 'nadlan_ur_notify_log', array_slice( $q, 0, 40 ), false );
	}
}

/* ---------- /my-renewal/ route ---------- */
add_action( 'init', function () {
	add_rewrite_rule( '^my-renewal/?$', 'index.php?nadlan_my_renewal=1', 'top' );
	if ( get_option( 'nadlan_my_renewal_rewrite_v1' ) !== '1' ) {
		flush_rewrite_rules( false );
		update_option( 'nadlan_my_renewal_rewrite_v1', '1' );
	}
} );
add_filter( 'query_vars', function ( $v ) { $v[] = 'nadlan_my_renewal'; return $v; } );

add_action( 'template_redirect', function () {
	if ( ! get_query_var( 'nadlan_my_renewal' ) ) { return; }
	if ( ! nadlan_ur_space_on() ) { wp_safe_redirect( home_url( '/urban-renewal/' ) ); exit; }
	$lang = nadlan_ur_req_lang();

	// join flow: needs a login first, then lands back here with the token
	$join = isset( $_GET['join'] ) ? sanitize_text_field( wp_unslash( $_GET['join'] ) ) : ''; // phpcs:ignore WordPress.Security.NonceVerification
	if ( $join && preg_match( '/^[A-Za-z0-9]{24}$/', $join ) ) {
		if ( ! is_user_logged_in() ) { wp_safe_redirect( wp_login_url( home_url( '/my-renewal/?join=' . rawurlencode( $join ) ) ) ); exit; }
		$q = get_posts( array( 'post_type' => 'nadlan_renewal', 'post_status' => 'any', 'posts_per_page' => 1, 'fields' => 'ids',
			'meta_query' => array( array( 'key' => 'invite_token', 'value' => $join ) ) ) );
		if ( $q ) {
			$id = (int) $q[0]; $u = wp_get_current_user();
			$members = nadlan_ur_members( $id ); $have = false;
			foreach ( $members as $m ) { if ( strtolower( $m['email'] ?? '' ) === strtolower( $u->user_email ) ) { $have = true; break; } }
			if ( ! $have ) {
				$members[] = array( 'email' => $u->user_email, 'joined' => current_time( 'mysql' ) );
				update_post_meta( $id, 'member_emails', wp_slash( wp_json_encode( array_slice( $members, 0, 400 ), JSON_UNESCAPED_UNICODE ) ) );
			}
			wp_safe_redirect( home_url( '/my-renewal/?space=' . $id ) ); exit;
		}
	}

	// anonymous visitors and members-without-a-room get the PRODUCT LANDING, not a login wall
	if ( ! is_user_logged_in() ) { nadlan_ur_render_landing( $lang, false ); exit; }
	$uid = get_current_user_id();
	$u = wp_get_current_user();
	$owned = get_posts( array( 'post_type' => 'nadlan_renewal', 'post_status' => 'any', 'posts_per_page' => 20, 'fields' => 'ids',
		'meta_query' => array( array( 'key' => 'owner_user_id', 'value' => $uid ) ) ) );
	$member = get_posts( array( 'post_type' => 'nadlan_renewal', 'post_status' => 'any', 'posts_per_page' => 40, 'fields' => 'ids',
		'meta_query' => array( array( 'key' => 'member_emails', 'value' => $u->user_email, 'compare' => 'LIKE' ) ) ) );
	$spaces = array_values( array_unique( array_merge( $owned, $member ) ) );
	if ( ! $spaces ) { nadlan_ur_render_landing( $lang, true ); exit; }
	nadlan_ur_render_dashboard( $spaces, $lang );
	exit;
} );

/* ---------- shared pieces ---------- */
if ( ! function_exists( 'nadlan_ur_space_app_mount' ) ) {
	/** Prints the app mount + the app script tag. */
	function nadlan_ur_space_app_mount( $mode, $space_id, $lang ) {
		$glb = esc_url( function_exists( 'nadlan_showroom_engine_base_url' ) ? nadlan_showroom_engine_base_url() . 'models/standard-residential.glb' : '' );
		$token = function_exists( 'nadlan_mapbox_token' ) ? nadlan_mapbox_token() : '';
		$js = esc_url( plugins_url( 'assets/urban/renewal-space.js', dirname( __FILE__ ) ) . '?v=' . rawurlencode( NADLAN_CONFIG_VERSION ) );
		?>
<div id="nlurd-mount" class="nlurd-app" data-loading="1"
	data-mode="<?php echo esc_attr( $mode ); ?>"
	data-space="<?php echo (int) $space_id; ?>"
	data-lang="<?php echo esc_attr( $lang ); ?>"
	data-rest="<?php echo esc_url( rest_url( 'nadlan/v1' ) ); ?>"
	data-nonce="<?php echo esc_attr( is_user_logged_in() ? wp_create_nonce( 'wp_rest' ) : '' ); ?>"
	data-glb="<?php echo $glb; // phpcs:ignore ?>"
	data-mapbox="<?php echo esc_attr( $token ); ?>"
	data-maplink="<?php echo esc_url( home_url( '/urban-renewal/map/' ) ); ?>"
	data-i18n="<?php echo esc_attr( wp_json_encode( nadlan_ur_space_strings( $lang ), JSON_UNESCAPED_UNICODE ) ); ?>"><?php
		echo esc_html( 'he' === $lang ? 'טוענים את חדר הפרויקט...' : 'Loading the project room...' );
	?></div>
<script defer src="<?php echo $js; // phpcs:ignore ?>"></script>
		<?php
	}
}

if ( ! function_exists( 'nadlan_ur_space_css' ) ) {
	function nadlan_ur_space_css() {
		?>
<style>
.nlurd{max-width:1120px;margin:0 auto;padding:24px 16px 60px;font-family:Heebo,sans-serif;color:#1B1A17}
.nlurd h1,.nlurd h2,.nlurd h3{font-family:"Frank Ruhl Libre",Georgia,serif}
.nlurd-app{min-height:220px}
.nlurd-app[data-loading]{color:#8E877A;font:400 14px Heebo;padding:40px 0;text-align:center}
.nlurd-top{display:flex;justify-content:space-between;align-items:flex-end;gap:14px;flex-wrap:wrap;margin:0 0 10px}
.nlurd-title{font-family:"Frank Ruhl Libre",Georgia,serif;font-size:1.45rem;margin:0}
.nlurd-sub{color:#6D665C;font-size:13.5px;margin:4px 0 0}
.nlurd-chip{display:inline-block;background:#F3EEE3;border:1px solid #E2DCD0;border-radius:999px;padding:4px 11px;font:600 11.5px Heebo;color:#51483A;text-decoration:none;margin-inline-start:6px}
.nlurd-chip--demo{background:#1B1A17;color:#E9D9A8;border-color:#1B1A17}
.nlurd-gauge{font-family:"Frank Ruhl Libre",serif;font-size:1.1rem;color:#1B1A17}
.nlurd-gauge b{font-size:1.7rem;color:#517048}
.nlurd-break{display:flex;height:12px;border-radius:999px;overflow:hidden;margin:0 0 12px;background:#F3EEE3}
.nlurd-break i{display:block;min-width:4px}
.nlurd-3d{position:relative;height:56vh;min-height:420px;max-height:640px;border-radius:18px;overflow:hidden;background:radial-gradient(ellipse at 50% 30%,#26221733 0%,transparent 65%),#14130F;border:1px solid #2A251B}
@media(max-width:600px){.nlurd-3d{height:62vh;min-height:400px}}
.nlurd-3d model-viewer{width:100%;height:100%;direction:ltr;background:transparent}
.nlurd-3dhint{position:absolute;bottom:12px;inset-inline-start:50%;transform:translateX(50%);z-index:2;background:rgba(20,19,15,.82);color:#E9D9A8;font:600 12px/1 Heebo;padding:8px 14px;border-radius:999px;border:1px solid rgba(233,217,168,.35);pointer-events:none;white-space:nowrap;max-width:92%;overflow:hidden;text-overflow:ellipsis;transition:opacity .5s}
[dir="ltr"] .nlurd-3dhint{transform:translateX(-50%)}
.nlurd-3dhint.is-off{opacity:0}
.nlur-apt{width:30px;height:30px;border-radius:50%;border:2px solid #fff;color:#fff;font:700 10.5px Heebo;cursor:pointer;background:#A79E8D}
.nlur-apt:not([data-visible]){opacity:0;pointer-events:none}
.nlurd-legend{display:flex;gap:12px;flex-wrap:wrap;margin:10px 2px 4px;font:600 12px Heebo;color:#51483A}
.nlurd-legend i{display:inline-block;width:11px;height:11px;border-radius:50%;margin-inline-end:4px;vertical-align:-1px}
.nlurd-stepper{display:flex;gap:0;overflow-x:auto;margin:14px 0 0;padding-bottom:4px;counter-reset:st}
.nlurd-step{position:relative;flex:1;min-width:88px;border:0;background:none;padding:8px 4px 10px;cursor:pointer;text-align:center;font-family:inherit}
.nlurd-step i{display:block;width:30px;height:30px;line-height:26px;margin:0 auto 6px;border-radius:50%;border:2px solid #C9C2B4;background:#FAF7F1;color:#8E877A;font:700 12.5px/26px Heebo;font-style:normal;position:relative;z-index:1}
.nlurd-step:not(:last-child):after{content:"";position:absolute;top:22px;inset-inline-start:calc(50% + 16px);width:calc(100% - 32px);height:2px;background:#E2DCD0}
.nlurd-step.is-done i{background:#517048;border-color:#517048;color:#FAF7F1}
.nlurd-step.is-done:after{background:#517048}
.nlurd-step.is-now i{background:#C2563A;border-color:#C2563A;color:#FAF7F1;box-shadow:0 0 0 4px rgba(194,86,58,.18)}
.nlurd-step.is-open i{outline:2px solid #9C7A3C;outline-offset:2px}
.nlurd-step span{display:block;font:600 11px/1.3 Heebo;color:#51483A}
.nlurd-step.is-now span{color:#1B1A17;font-weight:700}
.nlurd-stepcard{margin-top:8px}
.nlurd-stepcard h4 i{display:inline-block;width:24px;height:24px;line-height:21px;border-radius:50%;border:2px solid #9C7A3C;color:#9C7A3C;font:700 11px/21px Heebo;font-style:normal;text-align:center;margin-inline-end:6px}
.nlurd-grid{display:grid;grid-template-columns:1fr 1fr;gap:14px;margin-top:14px}
@media(max-width:860px){.nlurd-grid{grid-template-columns:1fr}}
.nlurd-card{background:#fff;border:1px solid #E2DCD0;border-radius:16px;padding:18px 20px}
.nlurd-card h4{font-family:"Frank Ruhl Libre",serif;margin:0 0 10px;font-size:1.08rem}
.nlurd-card p{font:400 13.5px/1.65 Heebo;margin:0 0 8px}
.nlurd-note{font:400 12px/1.6 Heebo;color:#8E877A}
.nlurd-btn{background:#C2563A;color:#FAF7F1;border:0;border-radius:10px;padding:11px 18px;font:700 13.5px Heebo;cursor:pointer;margin-top:8px}
.nlurd-btn:hover{filter:brightness(1.06)}
.nlurd textarea,.nlurd select,.nlurd input[type=text],.nlurd input[type=number]{width:100%;border:1px solid #E2DCD0;border-radius:10px;padding:11px;font:400 14px Heebo;background:#FAF7F1;box-sizing:border-box}
.nlurd-map{height:280px;border-radius:12px;overflow:hidden;background:#F3EEE3}
.nlurd-mapchips{display:flex;gap:8px;flex-wrap:wrap;margin-top:10px}
.nlurd-pin{width:22px;height:22px;border-radius:50% 50% 50% 0;transform:rotate(-45deg);background:#C2563A;border:2px solid #FAF7F1;box-shadow:0 4px 10px rgba(27,26,23,.35)}
.nlurd-todos{list-style:none;margin:0;padding:0}
.nlurd-todos li{display:flex;align-items:center;gap:10px;font:400 13.5px/1.5 Heebo;padding:7px 0;border-bottom:1px solid #F3EEE3}
.nlurd-todos li i{flex:0 0 22px;width:22px;height:22px;border-radius:50%;border:2px solid #C9C2B4;font-style:normal;color:#FAF7F1;font:700 12px/20px Heebo;text-align:center}
.nlurd-todos li.is-done i{background:#517048;border-color:#517048}
.nlurd-todos li.is-done{color:#8E877A;text-decoration:line-through;text-decoration-color:#C9C2B4}
.nlurd-acts{margin:4px 0 8px;padding-inline-start:18px}
.nlurd-acts li{font:400 13px/1.7 Heebo}
.nlurd-docrow{display:flex;align-items:center;justify-content:space-between;gap:8px;font:400 13.5px Heebo;margin:5px 0}
.nlurd-docrow b{color:#51483A}
.nlurd-meter{height:8px;background:#F3EEE3;border-radius:999px;overflow:hidden;margin:8px 0}
.nlurd-meter i{display:block;height:100%;background:#517048}
.nlurd-updates{list-style:none;margin:0;padding:0}
.nlurd-updates li{font:400 13.5px/1.6 Heebo;border-bottom:1px solid #F3EEE3;padding:8px 0}
.nlurd-updates time{color:#8E877A;font-size:11.5px;display:block}
.nlurd-invite input{direction:ltr;text-align:left;margin-top:8px}
.nlurd-spaces{display:flex;gap:8px;flex-wrap:wrap;margin-bottom:14px}
.nlurd-spaces a{border:1px solid #E2DCD0;border-radius:999px;padding:9px 15px;font:600 13px Heebo;color:#51483A;text-decoration:none;background:#fff}
.nlurd-spaces a.is-on{background:#1B1A17;color:#FAF7F1;border-color:#1B1A17}
/* landing */
.nlurl-hero{text-align:center;padding:34px 0 8px}
.nlurl-kicker{font:700 12.5px Heebo;letter-spacing:.06em;color:#9C7A3C;text-transform:uppercase;margin:0 0 10px}
.nlurl-hero h1{font-size:clamp(1.7rem,4vw,2.5rem);margin:0 0 12px;line-height:1.25}
.nlurl-hero .sub{color:#51483A;font:400 15.5px/1.7 Heebo;max-width:640px;margin:0 auto 20px}
.nlurl-ctas{display:flex;gap:12px;justify-content:center;flex-wrap:wrap}
.nlurl-cta{display:inline-block;border-radius:12px;padding:15px 26px;font:700 15px Heebo;text-decoration:none}
.nlurl-cta--go{background:#C2563A;color:#FAF7F1;box-shadow:0 14px 30px -12px rgba(194,86,58,.55)}
.nlurl-cta--alt{background:#fff;color:#1B1A17;border:1.5px solid #9C7A3C}
.nlurl-cta:hover{filter:brightness(1.05)}
.nlurl-badges{color:#8E877A;font:600 12px Heebo;margin:14px 0 0}
.nlurl-badges b{color:#51483A}
.nlurl-steps{display:grid;grid-template-columns:repeat(3,1fr);gap:14px;margin:34px 0}
@media(max-width:760px){.nlurl-steps{grid-template-columns:1fr}}
.nlurl-step{background:#fff;border:1px solid #E2DCD0;border-radius:16px;padding:20px;position:relative}
.nlurl-step i{display:block;width:38px;height:38px;border-radius:50%;background:#9C7A3C;color:#FAF7F1;font:700 17px/38px "Frank Ruhl Libre",serif;font-style:normal;text-align:center;margin-bottom:12px}
.nlurl-step b{display:block;font-family:"Frank Ruhl Libre",serif;font-size:1.06rem;margin-bottom:6px}
.nlurl-step p{font:400 13.5px/1.65 Heebo;color:#51483A;margin:0}
.nlurl-demo{background:#14130F;border-radius:22px;padding:22px 20px 26px;margin:10px 0 34px}
.nlurl-demo-head{display:flex;justify-content:space-between;align-items:center;gap:12px;flex-wrap:wrap;margin-bottom:14px}
.nlurl-demo-head h2{color:#FAF7F1;margin:0;font-size:1.35rem}
.nlurl-demo-head .lbl{background:rgba(233,217,168,.14);border:1px solid rgba(233,217,168,.4);color:#E9D9A8;font:600 12px Heebo;border-radius:999px;padding:7px 13px}
.nlurl-demo-inner{background:#FAF7F1;border-radius:16px;padding:16px}
.nlurl-2col{display:grid;grid-template-columns:1fr 1fr;gap:14px;margin:0 0 34px}
@media(max-width:760px){.nlurl-2col{grid-template-columns:1fr}}
.nlurl-col{border-radius:16px;padding:20px 22px}
.nlurl-col--old{background:#F3EEE3;border:1px solid #E2DCD0}
.nlurl-col--new{background:#fff;border:1.5px solid #9C7A3C}
.nlurl-col h3{margin:0 0 10px;font-size:1.06rem}
.nlurl-col ul{margin:0;padding-inline-start:18px}
.nlurl-col li{font:400 13.5px/1.8 Heebo;color:#51483A}
.nlurl-feats{display:grid;grid-template-columns:repeat(3,1fr);gap:12px;margin:0 0 34px}
@media(max-width:860px){.nlurl-feats{grid-template-columns:repeat(2,1fr)}}
@media(max-width:560px){.nlurl-feats{grid-template-columns:1fr}}
.nlurl-feat{background:#fff;border:1px solid #E2DCD0;border-radius:14px;padding:16px 18px}
.nlurl-feat b{display:block;font-family:"Frank Ruhl Libre",serif;margin-bottom:4px}
.nlurl-feat p{font:400 12.5px/1.6 Heebo;color:#6D665C;margin:0}
.nlurl-faq{margin:0 0 30px}
.nlurl-faq details{background:#fff;border:1px solid #E2DCD0;border-radius:12px;padding:14px 18px;margin-bottom:8px}
.nlurl-faq summary{font:700 14px Heebo;cursor:pointer;color:#1B1A17}
.nlurl-faq p{font:400 13.5px/1.7 Heebo;color:#51483A;margin:10px 0 0}
.nlurl-secttl{font-size:1.3rem;margin:0 0 14px}
.nlurl-privacy{background:#F3EEE3;border-radius:14px;padding:16px 20px;font:400 13px/1.7 Heebo;color:#51483A;margin-bottom:26px}
.nlurl-lang{text-align:center;margin:6px 0 0}
.nlurl-lang a{color:#9C7A3C;font:600 13px Heebo;text-decoration:none}
.nlurd-newform{background:#fff;border:1.5px solid #9C7A3C;border-radius:16px;padding:22px;margin:22px 0 30px}
.nlurd-newform h2{margin:0 0 12px;font-size:1.2rem}
.nlurd-f{display:grid;grid-template-columns:repeat(auto-fit,minmax(160px,1fr));gap:10px;margin:10px 0}
.nlurd-f label{display:flex;flex-direction:column;gap:5px;font:600 12.5px Heebo}
/* the block theme prints empty post-title h1s on this virtual route - hide + remove */
h1:empty{display:none}
</style>
<script>document.addEventListener("DOMContentLoaded",function(){document.querySelectorAll("h1").forEach(function(h){if(!h.textContent.trim()&&!h.children.length){h.remove()}})});</script>
		<?php
	}
}

/* ---------- the PRODUCT LANDING (anonymous + members without a room) ---------- */
if ( ! function_exists( 'nadlan_ur_render_landing' ) ) {
	function nadlan_ur_render_landing( $lang, $logged_in ) {
		$en = ( 'en' === $lang );
		$he_url = home_url( '/my-renewal/' );
		$en_url = home_url( '/my-renewal/?lang=en' );
		$self   = $en ? $en_url : $he_url;
		$title  = $en
			? 'Building Renewal Project Room for Apartment Owners in Israel | Nadlan'
			: 'חדר פרויקט התחדשות עירונית לדיירים: הסכמות על מודל תלת-ממד, שלבים ומסמכים | נדלן';
		$desc = $en
			? 'A free project room for buildings in pinui-binui and TAMA 38: track every apartment consent on a 3D model, follow the 10 stages, keep documents and updates in one private place. In Hebrew and English.'
			: 'חדר פרויקט חינמי לבניין בפינוי בינוי או תמ"א 38: מעקב הסכמות לכל דירה על מודל תלת-ממדי, סרגל 10 השלבים, מסמכים ועדכונים במקום אחד פרטי. בעברית ובאנגלית.';
		add_filter( 'pre_get_document_title', function () use ( $title ) { return $title; }, 99 );
		add_action( 'wp_head', function () use ( $desc, $self, $he_url, $en_url ) {
			echo '<meta name="description" content="' . esc_attr( $desc ) . '">' . "\n";
			echo '<link rel="canonical" href="' . esc_url( $self ) . '">' . "\n";
			echo '<link rel="alternate" hreflang="he" href="' . esc_url( $he_url ) . '">' . "\n";
			echo '<link rel="alternate" hreflang="en" href="' . esc_url( $en_url ) . '">' . "\n";
			echo '<link rel="alternate" hreflang="x-default" href="' . esc_url( $he_url ) . '">' . "\n";
			echo '<meta property="og:title" content="' . esc_attr( $desc ? $desc : '' ) . '">' . "\n";
		}, 4 );

		$C = $en ? array(
			'kicker' => 'Urban renewal, organized',
			'h1'     => 'Your building\'s renewal project room',
			'sub'    => 'One private place where the whole building sees the same truth: every apartment\'s consent painted on a 3D model of the building, the 10 stages of the process, the documents and the updates. Free for residents and committees.',
			'cta_go' => $logged_in ? 'Open a room for your building' : 'Open a room for your building',
			'cta_alt' => 'Free feasibility check (5 minutes)',
			'badges' => 'Free for residents and committees · Hebrew and English · Private, never shown in search',
			'steps_t' => 'Start here',
			'steps' => array(
				array( 'Check your building', 'Run the free wizard: address, floors, consent count. You get a first AI analysis of the likely track and your next steps.' ),
				array( 'Open the project room', 'One click seeds a 3D model of your building with every apartment on it. Mark who signed, who is in process, who is missing papers.' ),
				array( 'Invite the neighbors', 'Share one link in the building WhatsApp group. Everyone sees the same progress bar, the same documents, the same updates - no more rumor management.' ),
			),
			'demo_t' => 'A live example - a project that reached the finish line',
			'demo_lbl' => 'Live demo · sample data',
			'old_t' => 'Today, without a system',
			'old' => array( 'Consent counts living in one neighbor\'s Excel', 'Paper signatures nobody can audit', 'The same questions again and again in the WhatsApp group', 'Documents scattered across email inboxes' ),
			'new_t' => 'With the project room',
			'new' => array( 'Every apartment\'s status on a 3D model, one source of truth', 'A progress bar the whole building shares', 'A documents rollup that shows exactly what is missing', 'One updates feed, one invite link' ),
			'feats_t' => 'What is inside',
			'feats' => array(
				array( '3D consent map', 'Every apartment is a dot on the building model, colored by status.' ),
				array( '10-stage progress bar', 'From first assembly to keys, with typical durations and next actions per stage.' ),
				array( 'Auto to-do list', 'Derived live from your data: thresholds reached, documents missing, next moves.' ),
				array( 'Documents per apartment', 'ID, Tabu extract, signed agreement, power of attorney - tracked per unit.' ),
				array( 'Updates feed', 'The committee posts once; every neighbor sees it.' ),
				array( 'AI first analysis', 'The wizard reads your building details and suggests the likely track - with every disclaimer it deserves.' ),
			),
			'faq_t' => 'Questions owners ask',
			'faq' => array(
				array( 'Is it really free?', 'Yes. The project room is free for residents and committees. Nadlan makes its money from the professionals marketplace, not from homeowners.' ),
				array( 'Who can see our building\'s room?', 'Only people you invite with the link. Rooms are private, never listed in search engines, and documents are stored privately with membership-checked access.' ),
				array( 'We have neighbors who do not read Hebrew.', 'The whole room works in English too - switch with one link. Perfect for olim and foreign owners.' ),
				array( 'Is the AI analysis legal advice?', 'No. It is a first orientation only. Before signing anything, consult a lawyer who represents the residents - by law the developer pays for one you choose.' ),
			),
			'privacy' => 'Privacy: rooms are private and carry a no-index header. Documents are stored with random names, private status and membership-checked download. Nothing about your building appears in search.',
			'guide' => 'New to urban renewal? Read the full Hebrew guide',
			'lang_link' => '<a href="' . esc_url( $he_url ) . '">עברית</a>',
			'create_t' => 'Open the room for your building',
		) : array(
			'kicker' => 'התחדשות עירונית, מסודרת',
			'h1'     => 'חדר הפרויקט של הבניין שלכם',
			'sub'    => 'מקום פרטי אחד שבו כל הבניין רואה את אותה תמונה: ההסכמה של כל דירה צבועה על מודל תלת-ממדי של הבניין, עשרת שלבי התהליך, המסמכים והעדכונים. חינם לדיירים ולנציגות.',
			'cta_go' => 'פתיחת חדר לבניין שלכם',
			'cta_alt' => 'בדיקת כדאיות חינם (5 דקות)',
			'badges' => 'חינם לדיירים ולנציגות · עברית ואנגלית · פרטי ולא מופיע בחיפוש',
			'steps_t' => 'מתחילים כאן',
			'steps' => array(
				array( 'בודקים את הבניין', 'מריצים את האשף החינמי: כתובת, קומות, מצב הסכמות. מקבלים ניתוח ראשוני של המסלול המסתמן והצעדים הבאים.' ),
				array( 'פותחים חדר פרויקט', 'בלחיצה אחת נבנה מודל תלת-ממדי של הבניין עם כל הדירות עליו. מסמנים מי חתם, מי בתהליך, למי חסרים מסמכים.' ),
				array( 'מזמינים את השכנים', 'משתפים קישור אחד בקבוצת הוואטסאפ של הבניין. כולם רואים את אותו סרגל התקדמות, אותם מסמכים, אותם עדכונים - בלי ניהול שמועות.' ),
			),
			'demo_t' => 'דוגמה חיה - פרויקט שהגיע עד הסוף',
			'demo_lbl' => 'הדגמה חיה · נתוני דוגמה',
			'old_t' => 'היום, בלי מערכת',
			'old' => array( 'ספירת ההסכמות חיה באקסל של שכן אחד', 'חתימות על נייר שאי אפשר לעקוב אחריהן', 'אותן שאלות שוב ושוב בקבוצת הוואטסאפ', 'מסמכים מפוזרים בין תיבות מייל' ),
			'new_t' => 'עם חדר הפרויקט',
			'new' => array( 'הסטטוס של כל דירה על מודל תלת-ממדי, מקור אמת אחד', 'סרגל התקדמות שכל הבניין רואה', 'תמונת מסמכים שמראה בדיוק מה חסר', 'ערוץ עדכונים אחד, קישור הזמנה אחד' ),
			'feats_t' => 'מה יש בפנים',
			'feats' => array(
				array( 'מפת הסכמות תלת-ממדית', 'כל דירה היא נקודה על מודל הבניין, צבועה לפי סטטוס.' ),
				array( 'סרגל 10 השלבים', 'מהאסיפה הראשונה עד המפתח, עם משכים אופייניים וצעדים באים לכל שלב.' ),
				array( 'רשימת משימות אוטומטית', 'נגזרת חיה מהנתונים שלכם: רפים שהושגו, מסמכים חסרים, המהלכים הבאים.' ),
				array( 'מסמכים לכל דירה', 'תעודת זהות, נסח טאבו, הסכם חתום וייפוי כוח - במעקב פר דירה.' ),
				array( 'ערוץ עדכונים', 'הנציגות מפרסמת פעם אחת; כל שכן רואה.' ),
				array( 'ניתוח AI ראשוני', 'האשף קורא את נתוני הבניין ומציע את המסלול המסתמן - עם כל ההסתייגויות שמגיעות לו.' ),
			),
			'faq_t' => 'שאלות שבעלי דירות שואלים',
			'faq' => array(
				array( 'זה באמת חינם?', 'כן. חדר הפרויקט חינמי לדיירים ולנציגות. נדלן מרוויחה ממאגר אנשי המקצוע, לא מבעלי הדירות.' ),
				array( 'מי יכול לראות את החדר של הבניין שלנו?', 'רק מי שהזמנתם עם הקישור. החדרים פרטיים, לא מופיעים במנועי חיפוש, והמסמכים נשמרים באחסון פרטי עם בדיקת חברות בכל גישה.' ),
				array( 'יש לנו שכנים שלא קוראים עברית.', 'כל החדר עובד גם באנגלית - מחליפים בקישור אחד. מתאים לעולים ולבעלי דירות מחו"ל.' ),
				array( 'הניתוח של ה-AI הוא ייעוץ משפטי?', 'לא. זו התמצאות ראשונית בלבד. לפני כל חתימה מתייעצים עם עורך דין מטעם הדיירים - על פי חוק היזם משלם על עורך דין שאתם בוחרים.' ),
			),
			'privacy' => 'פרטיות: החדרים פרטיים ונושאים כותרת no-index. מסמכים נשמרים בשמות אקראיים, בסטטוס פרטי ועם בדיקת חברות בכל הורדה. שום דבר על הבניין שלכם לא מופיע בחיפוש.',
			'guide' => 'חדשים בהתחדשות עירונית? התחילו מהמדריך המלא',
			'lang_link' => '<a href="' . esc_url( $en_url ) . '">English</a>',
			'create_t' => 'פתיחת החדר לבניין שלכם',
		);

		$cta_go_href = $logged_in ? '#nlurd-new' : wp_login_url( $self );
		$wizard = home_url( '/urban-renewal/check/' );
		get_header();
		nadlan_ur_space_css();
		?>
<div class="nlurd" dir="<?php echo $en ? 'ltr' : 'rtl'; ?>" lang="<?php echo esc_attr( $lang ); ?>">
	<header class="nlurl-hero">
		<p class="nlurl-kicker"><?php echo esc_html( $C['kicker'] ); ?></p>
		<h1><?php echo esc_html( $C['h1'] ); ?></h1>
		<p class="sub"><?php echo esc_html( $C['sub'] ); ?></p>
		<div class="nlurl-ctas">
			<a class="nlurl-cta nlurl-cta--go" href="<?php echo esc_url( $cta_go_href ); ?>"><?php echo esc_html( $C['cta_go'] ); ?></a>
			<a class="nlurl-cta nlurl-cta--alt" href="<?php echo esc_url( $wizard ); ?>"><?php echo esc_html( $C['cta_alt'] ); ?></a>
		</div>
		<p class="nlurl-badges"><?php echo esc_html( $C['badges'] ); ?></p>
		<p class="nlurl-lang"><?php echo wp_kses_post( $C['lang_link'] ); ?></p>
	</header>

	<?php if ( $logged_in ) : ?>
	<section class="nlurd-newform" id="nlurd-new">
		<h2><?php echo esc_html( $C['create_t'] ); ?></h2>
		<div class="nlurd-f">
			<label><?php echo $en ? 'City' : 'עיר'; ?><input type="text" id="nlurd-city"></label>
			<label><?php echo $en ? 'Street and number' : 'רחוב ומספר'; ?><input type="text" id="nlurd-addr"></label>
			<label><?php echo $en ? 'Floors' : 'קומות'; ?><input type="number" id="nlurd-floors" min="1" max="40" value="4"></label>
			<label><?php echo $en ? 'Apartments per floor' : 'דירות בקומה'; ?><input type="number" id="nlurd-upf" min="1" max="12" value="3"></label>
		</div>
		<button type="button" class="nlurd-btn" id="nlurd-create"><?php echo esc_html( $C['cta_go'] ); ?></button>
		<div id="nlurd-createmsg" aria-live="polite" class="nlurd-note"></div>
	</section>
	<?php endif; ?>

	<section>
		<h2 class="nlurl-secttl"><?php echo esc_html( $C['steps_t'] ); ?></h2>
		<div class="nlurl-steps">
			<?php foreach ( $C['steps'] as $i => $s ) : ?>
			<div class="nlurl-step"><i><?php echo (int) $i + 1; ?></i><b><?php echo esc_html( $s[0] ); ?></b><p><?php echo esc_html( $s[1] ); ?></p></div>
			<?php endforeach; ?>
		</div>
	</section>

	<section class="nlurl-demo">
		<div class="nlurl-demo-head">
			<h2><?php echo esc_html( $C['demo_t'] ); ?></h2>
			<span class="lbl"><?php echo esc_html( $C['demo_lbl'] ); ?></span>
		</div>
		<div class="nlurl-demo-inner">
			<?php nadlan_ur_space_app_mount( 'demo', 0, $lang ); ?>
		</div>
	</section>

	<section class="nlurl-2col">
		<div class="nlurl-col nlurl-col--old"><h3><?php echo esc_html( $C['old_t'] ); ?></h3><ul>
			<?php foreach ( $C['old'] as $li ) : ?><li><?php echo esc_html( $li ); ?></li><?php endforeach; ?>
		</ul></div>
		<div class="nlurl-col nlurl-col--new"><h3><?php echo esc_html( $C['new_t'] ); ?></h3><ul>
			<?php foreach ( $C['new'] as $li ) : ?><li><?php echo esc_html( $li ); ?></li><?php endforeach; ?>
		</ul></div>
	</section>

	<section>
		<h2 class="nlurl-secttl"><?php echo esc_html( $C['feats_t'] ); ?></h2>
		<div class="nlurl-feats">
			<?php foreach ( $C['feats'] as $f ) : ?>
			<div class="nlurl-feat"><b><?php echo esc_html( $f[0] ); ?></b><p><?php echo esc_html( $f[1] ); ?></p></div>
			<?php endforeach; ?>
		</div>
	</section>

	<?php if ( ! $en && shortcode_exists( 'nadlan_ur_consent_calc' ) ) : ?>
	<section><?php echo do_shortcode( '[nadlan_ur_consent_calc]' ); ?></section>
	<?php endif; ?>

	<section class="nlurl-faq">
		<h2 class="nlurl-secttl"><?php echo esc_html( $C['faq_t'] ); ?></h2>
		<?php foreach ( $C['faq'] as $qa ) : ?>
		<details><summary><?php echo esc_html( $qa[0] ); ?></summary><p><?php echo esc_html( $qa[1] ); ?></p></details>
		<?php endforeach; ?>
	</section>

	<div class="nlurl-privacy"><?php echo esc_html( $C['privacy'] ); ?></div>
	<p style="text-align:center"><a href="<?php echo esc_url( home_url( $en ? '/urban-renewal/english-guide/' : '/urban-renewal/' ) ); ?>" style="color:#9C7A3C;font:600 14px Heebo"><?php echo esc_html( $C['guide'] ); ?></a></p>
</div>
<script type="application/ld+json"><?php
	$faq_ld = array( '@context' => 'https://schema.org', '@type' => 'FAQPage', 'mainEntity' => array() );
	foreach ( $C['faq'] as $qa ) {
		$faq_ld['mainEntity'][] = array( '@type' => 'Question', 'name' => $qa[0],
			'acceptedAnswer' => array( '@type' => 'Answer', 'text' => $qa[1] ) );
	}
	echo wp_json_encode( $faq_ld, JSON_UNESCAPED_UNICODE );
?></script>
		<?php if ( $logged_in ) : ?>
<script>
(function(){
	var b=document.getElementById("nlurd-create");if(!b)return;
	b.addEventListener("click",function(){
		var m=document.getElementById("nlurd-createmsg");m.textContent="<?php echo $en ? 'Opening the room...' : 'פותחים חדר...'; ?>";
		fetch("<?php echo esc_url( rest_url( 'nadlan/v1/renewal-space' ) ); ?>",{method:"POST",
			headers:{"Content-Type":"application/json","X-WP-Nonce":"<?php echo esc_js( wp_create_nonce( 'wp_rest' ) ); ?>"},
			body:JSON.stringify({city:document.getElementById("nlurd-city").value,address:document.getElementById("nlurd-addr").value,floors:document.getElementById("nlurd-floors").value,units_per_floor:document.getElementById("nlurd-upf").value})})
		.then(function(r){return r.json().then(function(j){if(!r.ok)throw j;return j})})
		.then(function(d){location.href=d.url})
		.catch(function(e){m.textContent=(e&&e.message)||"<?php echo $en ? 'Error' : 'שגיאה'; ?>"});
	});
})();
</script>
		<?php endif; ?>
		<?php
		get_footer();
	}
}

/* ---------- the member dashboard ---------- */
if ( ! function_exists( 'nadlan_ur_render_dashboard' ) ) {
	function nadlan_ur_render_dashboard( $spaces, $lang = 'he' ) {
		$en = ( 'en' === $lang );
		$sel = isset( $_GET['space'] ) ? (int) $_GET['space'] : 0; // phpcs:ignore WordPress.Security.NonceVerification
		if ( $sel && ( ! nadlan_ur_space_ok( $sel ) || ! nadlan_ur_can_view( $sel ) ) ) { $sel = 0; }
		if ( ! $sel && $spaces ) { $sel = (int) $spaces[0]; }
		nocache_headers();
		header( 'X-Robots-Tag: noindex, nofollow' );
		get_header();
		nadlan_ur_space_css();
		?>
<div class="nlurd" dir="<?php echo $en ? 'ltr' : 'rtl'; ?>" lang="<?php echo esc_attr( $lang ); ?>">
	<header style="margin-bottom:14px">
		<h1 style="margin:0 0 4px"><?php echo $en ? 'My renewal room' : 'חדר ההתחדשות שלי'; ?></h1>
		<p class="nlurd-note"><?php echo $en
			? 'Internal building management: consents on the model, stages, documents and updates. Private to building members, never shown in search.'
			: 'ניהול פנימי לבניין: הסכמות על המודל, שלבים, מסמכים ועדכונים. העמוד פרטי לחברי הבניין בלבד ואינו מופיע בחיפוש.'; ?>
			<a href="<?php echo esc_url( home_url( '/my-renewal/?space=' . (int) $sel . ( $en ? '' : '&lang=en' ) ) ); ?>" style="color:#9C7A3C;font-weight:600"><?php echo $en ? 'עברית' : 'English'; ?></a>
		</p>
	</header>
	<?php if ( count( $spaces ) > 1 ) : ?>
	<nav class="nlurd-spaces">
		<?php foreach ( $spaces as $sid ) : ?>
		<a href="<?php echo esc_url( home_url( '/my-renewal/?space=' . (int) $sid . ( $en ? '&lang=en' : '' ) ) ); ?>" class="<?php echo $sid === $sel ? 'is-on' : ''; ?>"><?php echo esc_html( get_the_title( $sid ) ); ?></a>
		<?php endforeach; ?>
	</nav>
	<?php endif; ?>
	<?php nadlan_ur_space_app_mount( 'live', $sel, $lang ); ?>
</div>
		<?php
		get_footer();
	}
}

/* healthcheck visibility */
add_filter( 'nadlan_config_healthcheck', function ( $out ) {
	if ( isset( $out['urban_renewal'] ) && is_array( $out['urban_renewal'] ) ) {
		$out['urban_renewal']['space'] = nadlan_ur_space_on();
	}
	return $out;
} );
