<?php
/**
 * nadlan-config - URBAN RENEWAL PROJECT SPACE (L4 2026-07-12, PRODUCT v2 2026-07-12).
 *
 * The building's project room: per-apartment consent tracked and painted on
 * the 3D standard model, the 10-stage bureaucratic ladder, an updates feed
 * (send-gated, deliverability-last), invite-by-token membership, and the
 * /my-renewal/ surface. Documents are tracked per apartment as four checkboxes; no file is stored in a room (urban-docs.php
 * does not exist, HAD-396).
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
 *
 * RENEWAL ROOM PRO (26.10.2026, local build on top of live 1.72.534): an organizing company's management room on the
 * same route. A room can hold several buildings (one complex); the payload is filtered by role before it leaves the
 * server (renewal-room.php); one apartment is saved per request with a version and an append-only change log; owners
 * per apartment; the statutory majority per building; deadlines; an organizer account with a portfolio route
 * (renewal-org.php). The UI is assets/urban/renewal-space.js (facade, ladder, updates, report; the 3D building and the
 * map stay one tap away) with assets/urban/renewal-room.css (NadLan Instruments tokens). No URL, index or robots change.
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
		// NadLan Instruments (26.10.2026): deep, sea, a light sea tint, ink2 and the line grey. The facade adds patterns
		// (hatch, stipple, cross) so no status depends on colour alone; survey red stays for warnings only.
		return array(
			'consented'    => array( 'חתמו', '#1F4B5C' ),
			'in_process'   => array( 'בתהליך', '#2F6F86' ),
			'missing_docs' => array( 'חסרים מסמכים', '#8DB4C4' ),
			'refused'      => array( 'סירבו', '#3E4C58' ),
			'unreached'    => array( 'טרם הושג קשר', '#D3DCE2' ),
		);
	}
}
if ( ! function_exists( 'nadlan_ur_doc_keys' ) ) {
	function nadlan_ur_doc_keys() {
		return array( 'id_copy' => 'צילום תעודת זהות', 'ownership_nesach' => 'נסח טאבו', 'signed_agreement' => 'הסכם חתום', 'poa' => 'ייפוי כוח' );
	}
}
if ( ! function_exists( 'nadlan_ur_clean_apartments' ) ) {
	function nadlan_ur_clean_apartments( $raw, $max = 400 ) {
		$statuses = array_keys( nadlan_ur_consent_statuses() );
		$dirs = array( 'west', 'east', 'north', 'south' );
		$out = array();
		foreach ( (array) $raw as $u ) {
			if ( ! is_array( $u ) || empty( $u['id'] ) ) { continue; }
			$docs = array();
			foreach ( array_keys( nadlan_ur_doc_keys() ) as $dk ) { $docs[ $dk ] = ! empty( $u['docs'][ $dk ] ); }
			$row = array(
				'id'             => sanitize_key( $u['id'] ),
				'floor'          => max( 0, min( 60, (int) ( $u['floor'] ?? 0 ) ) ),
				'pos'            => max( 0, min( 20, (int) ( $u['pos'] ?? 0 ) ) ),
				'dir'            => in_array( $u['dir'] ?? '', $dirs, true ) ? $u['dir'] : 'west',
				'label'          => mb_substr( sanitize_text_field( (string) ( $u['label'] ?? '' ) ), 0, 60 ),
				'consent_status' => in_array( $u['consent_status'] ?? '', $statuses, true ) ? $u['consent_status'] : 'unreached',
				'docs'           => $docs,
				'contact_note'   => mb_substr( sanitize_text_field( (string) ( $u['contact_note'] ?? '' ) ), 0, 200 ),
				'note'           => mb_substr( sanitize_text_field( (string) ( $u['note'] ?? '' ) ), 0, 400 ),
				'updated'        => ! empty( $u['updated'] ) ? substr( sanitize_text_field( (string) $u['updated'] ), 0, 19 ) : current_time( 'mysql' ),
			);
			// Pro fields (renewal-room.php): kept when present, never invented for a legacy row
			if ( ! empty( $u['building'] ) ) { $row['building'] = sanitize_key( $u['building'] ); }
			if ( ! empty( $u['num'] ) ) { $row['num'] = max( 1, min( 9999, (int) $u['num'] ) ); }
			if ( isset( $u['owners'] ) && function_exists( 'nadlan_rr_clean_owners' ) ) { $row['owners'] = nadlan_rr_clean_owners( $u['owners'] ); }
			if ( isset( $u['common_share'] ) ) { $row['common_share'] = mb_substr( preg_replace( '/[^0-9\/\.%]/', '', (string) $u['common_share'] ), 0, 16 ); }
			if ( isset( $u['v'] ) ) { $row['v'] = max( 0, (int) $u['v'] ); }
			if ( isset( $u['updated_by'] ) ) { $row['updated_by'] = (int) $u['updated_by']; }
			$out[] = $row;
			if ( count( $out ) >= $max ) { break; }
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
	/** Pro: the site admin, the user who opened the room, or the staff of the organizing company that owns it (while
	 *  its account is active; billing is off by default, so always). */
	function nadlan_ur_can_manage( $space_id ) {
		if ( current_user_can( 'manage_options' ) ) { return true; }
		if ( function_exists( 'nadlan_rr_role' ) ) {
			$r = nadlan_rr_role( $space_id );
			return nadlan_rr_is_manager( $r ) && ( 'org' !== $r || nadlan_rr_room_active( $space_id ) );
		}
		return (int) get_post_meta( $space_id, 'owner_user_id', true ) === get_current_user_id() && get_current_user_id() > 0;
	}
}
if ( ! function_exists( 'nadlan_ur_can_view' ) ) {
	function nadlan_ur_can_view( $space_id ) {
		if ( nadlan_ur_can_manage( $space_id ) ) { return true; }
		if ( function_exists( 'nadlan_rr_role' ) && '' !== nadlan_rr_role( $space_id ) ) { return true; } // incl. a lapsed account's staff, read-only
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
		return in_array( $raw, array( 'en', 'ru' ), true ) ? $raw : 'he';
	}
}
if ( ! function_exists( 'nadlan_ur_statuses_lang' ) ) {
	function nadlan_ur_statuses_lang( $lang ) {
		$s = nadlan_ur_consent_statuses();
		$map = array(
			'en' => array( 'consented' => 'Signed', 'in_process' => 'In progress', 'missing_docs' => 'Missing documents', 'refused' => 'Refused', 'unreached' => 'Not yet reached' ),
			'ru' => array( 'consented' => 'Подписали', 'in_process' => 'В процессе', 'missing_docs' => 'Не хватает документов', 'refused' => 'Отказались', 'unreached' => 'Ещё не связались' ),
		);
		if ( isset( $map[ $lang ] ) ) {
			foreach ( $map[ $lang ] as $k => $label ) { if ( isset( $s[ $k ] ) ) { $s[ $k ][0] = $label; } }
		}
		return $s;
	}
}
if ( ! function_exists( 'nadlan_ur_doc_keys_lang' ) ) {
	function nadlan_ur_doc_keys_lang( $lang ) {
		if ( 'en' === $lang ) {
			return array( 'id_copy' => 'ID copy', 'ownership_nesach' => 'Land registry extract (Tabu)', 'signed_agreement' => 'Signed agreement', 'poa' => 'Power of attorney' );
		}
		if ( 'ru' === $lang ) {
			return array( 'id_copy' => 'Копия удостоверения личности', 'ownership_nesach' => 'Выписка из реестра (Табу)', 'signed_agreement' => 'Подписанный договор', 'poa' => 'Доверенность' );
		}
		return nadlan_ur_doc_keys();
	}
}

/* Per-stage playbook: label + what happens + duration + next actions. A duration shows only with a source: today only
   "היתר בנייה" (the authority's 2025 report, p. 87: 4.0 years on average from plan approval to the first permit, HAD-396).
   HE labels mirror nadlan_ur_ladder_labels() (urban-tools.php) - keep in sync. */
if ( ! function_exists( 'nadlan_ur_stage_meta' ) ) {
	function nadlan_ur_stage_meta( $lang = 'he' ) {
		if ( 'ru' === $lang ) {
			return array(
				array( 'label' => 'Первая организация', 'desc' => 'Первое собрание жильцов, письменный протокол и полный список собственников квартир.', 'duration' => '', 'actions' => array( 'Провести первое собрание жильцов', 'Собрать контакты всех собственников', 'Проверить дом в официальном реестре комплексов обновления' ) ),
				array( 'label' => 'Выбор комитета', 'desc' => 'От 3 до 5 соседей с письменным мандатом вести процесс от имени дома.', 'duration' => '', 'actions' => array( 'Проголосовать за комитет жильцов', 'Подписать письмо о назначении', 'Открыть единый канал обновлений для всех соседей' ) ),
				array( 'label' => 'Сбор подписей', 'desc' => 'Подписание собственниками принципиального согласия, с полной прозрачностью для всего дома.', 'duration' => '', 'actions' => array( 'Обновлять статус каждой квартиры на фасаде дома', 'Решать вопросы наследства и недостающих документов', 'Следить за особым большинством: две трети квартир в комплексе, три пятых в каждом доме и более половины общего имущества' ) ),
				array( 'label' => 'Выбор специалистов', 'desc' => 'Адвокат и оценщик, работающие на жильцов: оплачивает застройщик, выбираете вы.', 'duration' => '', 'actions' => array( 'Собрать предложения опытных адвокатов стороны жильцов', 'Выбрать оценщика от имени жильцов', 'Подписать соглашения о гонораре' ) ),
				array( 'label' => 'Выбор застройщика', 'desc' => 'Тендер застройщиков: опыт, финансовая устойчивость и гарантии.', 'duration' => '', 'actions' => array( 'Подготовить документ требований жильцов', 'Сравнить предложения застройщиков', 'Проверить банковские гарантии по закону о продаже' ) ),
				array( 'label' => 'Утверждение плана', 'desc' => 'План проходит комиссии по планированию: самая большая переменная во всём графике.', 'duration' => '', 'actions' => array( 'Сопровождать процесс планирования в комиссии', 'Информировать соседей о каждом решении', 'Поддерживать связь с городской администрацией обновления' ) ),
				array( 'label' => 'Разрешение на строительство', 'desc' => 'Финальная техническая спецификация и процесс выбора квартир.', 'duration' => '4 года в среднем от утверждения плана (пинуй-бинуй, 2025)', 'actions' => array( 'Подписать финальное приложение спецификации', 'Провести выбор квартир по согласованной формуле', 'Подготовить договоры аренды для переезда' ) ),
				array( 'label' => 'Переезд', 'desc' => 'Дом освобождается, аренду оплачивает застройщик до передачи ключей.', 'duration' => '', 'actions' => array( 'Подписать договоры аренды', 'Согласовать переезды', 'Передать ключи застройщику' ) ),
				array( 'label' => 'Строительство', 'desc' => 'Само строительство: надзорный инженер стороны жильцов отчитывается комитету.', 'duration' => '', 'actions' => array( 'Изучать периодические отчёты надзора', 'Согласованные визиты жильцов на площадку', 'Следить за графиком по договору' ) ),
				array( 'label' => 'Передача и регистрация', 'desc' => 'Разрешение на заселение, передача квартир, гарантийный год и регистрация в Табу.', 'duration' => '', 'actions' => array( 'Протокол передачи для каждой квартиры', 'Отслеживать исправления гарантийного года', 'Зарегистрировать кондоминиум в земельном реестре' ) ),
			);
		}
		if ( 'en' === $lang ) {
			return array(
				array( 'label' => 'First organizing', 'desc' => 'A first residents assembly, a written protocol and a full map of the apartment owners.', 'duration' => '', 'actions' => array( 'Hold a first residents assembly', 'Collect contact details for every apartment owner', 'Check the building against the official renewal-compounds registry' ) ),
				array( 'label' => 'Electing a committee', 'desc' => 'Three to five neighbors elected with a written mandate to run the process on behalf of the building.', 'duration' => '', 'actions' => array( 'Vote on a residents committee', 'Sign a written appointment letter', 'Open a single updates channel for all neighbors' ) ),
				array( 'label' => 'Collecting signatures', 'desc' => 'Signing the owners on an agreement in principle, with full transparency to the whole building.', 'duration' => '', 'actions' => array( 'Update the status of every apartment on the building face', 'Handle apartments with inheritance or missing papers', 'Track the special majority: two thirds of the apartments in the cluster, three fifths in each building and over half of the common property' ) ),
				array( 'label' => 'Hiring professionals', 'desc' => 'A lawyer and an appraiser who work for the residents: paid by the developer, chosen by you.', 'duration' => '', 'actions' => array( 'Collect offers from experienced tenants-side lawyers', 'Choose an appraiser on behalf of the residents', 'Sign fee agreements' ) ),
				array( 'label' => 'Choosing a developer', 'desc' => 'A developer tender: track record, financial strength and guarantees.', 'duration' => '', 'actions' => array( 'Prepare the residents requirements document', 'Compare developer offers side by side', 'Verify sale-law guarantees and securities' ) ),
				array( 'label' => 'Planning approval', 'desc' => 'The plan moves through the planning committees: the biggest variable in the whole timeline.', 'duration' => '', 'actions' => array( 'Follow the planning process with the committee', 'Update neighbors on every decision', 'Stay in touch with the municipal renewal administration' ) ),
				array( 'label' => 'Building permit', 'desc' => 'Final technical specification and the apartment-selection process.', 'duration' => '4 years on average from plan approval (pinui-binui, 2025)', 'actions' => array( 'Sign the final specification annex', 'Run the apartment selection by the agreed formula', 'Prepare rental agreements for the move-out' ) ),
				array( 'label' => 'Moving out', 'desc' => 'The building is vacated, and the developer pays the rent until delivery.', 'duration' => '', 'actions' => array( 'Sign rental agreements', 'Coordinate the moves', 'Hand keys to the developer' ) ),
				array( 'label' => 'Construction', 'desc' => 'The construction itself: the residents-side supervisor reports to the committee.', 'duration' => '', 'actions' => array( 'Review periodic supervision reports', 'Coordinate resident site visits', 'Track the schedule against the agreement' ) ),
				array( 'label' => 'Delivery and registration', 'desc' => 'Occupancy permit, apartment handover, the warranty year and Tabu registration.', 'duration' => '', 'actions' => array( 'Run a handover protocol for every apartment', 'Track warranty-year fixes', 'Register the shared building in the land registry' ) ),
			);
		}
		return array(
			array( 'label' => 'התארגנות ראשונית', 'desc' => 'אסיפת דיירים ראשונה, פרוטוקול כתוב ומיפוי מלא של בעלי הדירות.', 'duration' => '', 'actions' => array( 'כינוס אסיפת דיירים ראשונה', 'איסוף פרטי קשר של כל בעלי הדירות', 'בדיקת הבניין מול מאגר מתחמי ההתחדשות' ) ),
			array( 'label' => 'בחירת נציגות', 'desc' => 'בחירת 3 עד 5 שכנים עם מנדט כתוב לנהל את התהליך בשם הבניין.', 'duration' => '', 'actions' => array( 'הצבעה על נציגות דיירים', 'חתימה על כתב מינוי', 'פתיחת ערוץ עדכונים אחד לכל השכנים' ) ),
			array( 'label' => 'החתמות', 'desc' => 'החתמת בעלי הדירות על הסכמה עקרונית, בשקיפות מלאה לכל הבניין.', 'duration' => '', 'actions' => array( 'עדכון סטטוס לכל דירה על חזית הבניין', 'טיפול בדירות עם ירושה או מסמכים חסרים', 'מעקב אחרי הרוב המיוחס: שני שלישים מהדירות במקבץ, שלוש חמישיות בכל בניין ויותר ממחצית הרכוש המשותף' ) ),
			array( 'label' => 'בחירת אנשי מקצוע', 'desc' => 'עורך דין ושמאי שעובדים בשביל הדיירים, בשכר היזם ולפי בחירתכם.', 'duration' => '', 'actions' => array( 'קבלת הצעות מעורכי דין מלווים מנוסים', 'בחירת שמאי מטעם הדיירים', 'חתימה על הסכמי שכר טרחה' ) ),
			array( 'label' => 'בחירת יזם', 'desc' => 'מכרז יזמים: ניסיון מוכח, איתנות פיננסית ובטוחות.', 'duration' => '', 'actions' => array( 'הכנת מסמך דרישות הדיירים', 'השוואת הצעות יזמים זו מול זו', 'בדיקת ערבויות חוק מכר ובטוחות' ) ),
			array( 'label' => 'תב"ע ותכנון', 'desc' => 'התוכנית עוברת בוועדות התכנון: המשתנה הגדול ביותר בלוח הזמנים.', 'duration' => '', 'actions' => array( 'ליווי הליך התכנון מול הוועדה', 'עדכון השכנים בכל החלטה', 'קשר שוטף עם מנהלת ההתחדשות העירונית' ) ),
			array( 'label' => 'היתר בנייה', 'desc' => 'מפרט טכני סופי והליך בחירת דירות התמורה.', 'duration' => '4 שנים בממוצע מאישור התוכנית (פינוי בינוי, 2025)', 'actions' => array( 'חתימה על נספח המפרט הסופי', 'הליך בחירת דירות לפי הנוסחה שנקבעה', 'היערכות להסכמי שכירות לפינוי' ) ),
			array( 'label' => 'פינוי', 'desc' => 'פינוי הבניין, ושכר הדירה במימון היזם עד המסירה.', 'duration' => '', 'actions' => array( 'חתימה על הסכמי שכירות', 'תיאום הובלות', 'מסירת מפתחות ליזם' ) ),
			array( 'label' => 'בנייה', 'desc' => 'הבנייה עצמה, והמפקח מטעם הדיירים מדווח לנציגות.', 'duration' => '', 'actions' => array( 'מעבר על דוחות פיקוח תקופתיים', 'ביקורי דיירים מתואמים באתר', 'מעקב לוח הזמנים מול ההסכם' ) ),
			array( 'label' => 'מסירה ורישום', 'desc' => 'טופס 4, מסירת הדירות, שנת הבדק ורישום בטאבו.', 'duration' => '', 'actions' => array( 'פרוטוקול מסירה לכל דירה', 'מעקב תיקוני שנת בדק', 'רישום הבית המשותף בטאבו' ) ),
		);
	}
}

/* UI strings for the app JS (data-i18n). RenewalRoomPro 26.10.2026: one key set for HE, EN and RU. Hebrew passes the
   language-dna blacklist (no "model", "system", "demo", "AI", no long dash); the 3D building is called "סיור 360". */
if ( ! function_exists( 'nadlan_ur_space_strings' ) ) {
	function nadlan_ur_space_strings( $lang = 'he' ) {
		$he = array(
			'load_fail' => 'לא הצלחנו לטעון את החדר. נסו לרענן את העמוד.',
			'room_title' => 'חדר הניהול', 'room_building' => 'חדר הבניין', 'room_demo' => 'חדר לדוגמה', 'brand_mark' => 'נ', 'brand_sub' => 'התחדשות עירונית · נדלן',
			'demo_badge' => 'נתוני דוגמה', 'managed_by' => 'מנוהל על ידי {org}', 'org_line' => 'צוות: {s} · מתחמים: {c}', 'tabs_label' => 'מסכי החדר',
			'tab_portfolio' => 'תיק המתחמים', 'tab_complex' => 'מתחם', 'tab_updates' => 'עדכונים לדיירים', 'tab_report' => 'דוח לנציגות',
			'read_only' => 'תקופת החשבון של החברה המארגנת הסתיימה. החדר פתוח לקריאה בלבד, וכל הנתונים שמורים.',
			'stage_of' => 'שלב {n} מתוך 10', 'two_thirds' => 'שני שלישים',
			'attn_refused' => '{n} סירבו', 'attn_unreached' => '{n} בלי קשר', 'attn_idle' => 'לא עודכן {n} ימים', 'attn_deadline' => 'מועד בעוד {n} ימים: {label}', 'attn_deadline_passed' => 'עבר מועד לפני {n} ימים: {label}', 'attn_lead' => 'דורש טיפול:',
			'next_two_thirds' => 'עוד {n} חתימות עד שני שלישים מהדירות במתחם', 'next_reach' => 'ליצור קשר עם {n} בעלי דירות שטרם הושג איתם קשר', 'next_deadline' => '{label}: בעוד {n} ימים',
			'pf_sub' => 'כל המתחמים שאתם מלווים, במבט אחד: איפה כל מתחם עומד, כמה חתמו ומה הצעד הבא.', 'new_complex' => 'מתחם חדש',
			'kpi_cx' => 'מתחמים', 'kpi_bld' => 'בניינים', 'kpi_apt' => 'דירות', 'kpi_yes' => 'חתמו, בכל התיק', 'kpi_miss' => 'דירות שחסר להן מסמך', 'kpi_attn' => 'מתחמים שדורשים טיפול',
			'filter_label' => 'סינון המתחמים', 'f_all' => 'הכל', 'f_pinui_binui' => 'פינוי בינוי', 'f_tama' => 'תמ"א 38', 'f_attn' => 'דורש טיפול',
			'pf_empty' => 'עוד אין מתחמים בתיק. פתחו מתחם ראשון: שם, עיר, והבניינים עם הקומות והדירות.',
			'one_building' => 'בניין אחד', 'n_buildings' => '{n} בניינים', 'n_apts' => '{n} דירות', 'updated_on' => 'עודכן {d}',
			'col_cx' => 'מתחם', 'col_track' => 'מסלול', 'col_stage' => 'שלב', 'col_signed' => 'חתמו', 'col_miss' => 'חסר מסמך', 'col_next' => 'הצעד הבא',
			'pf_foot' => 'החדרים חינם לדיירים ולנציגות. שכן רואה את התמונה של הבניין ואת הדירה שלו בלבד.',
			'f_b_label' => 'שם הבניין', 'f_b_addr' => 'כתובת', 'f_floors' => 'קומות', 'f_upf' => 'דירות בקומה', 'f_cx_name' => 'שם המתחם', 'f_city' => 'עיר',
			'add_building' => 'הוספת בניין', 'create_cx' => 'פתיחת המתחם', 'new_cx_note' => 'כל הדירות מתחילות כ"טרם הושג קשר". את הבעלים, המסמכים והחתימות מעדכנים דירה אחר דירה.', 'opening' => 'פותחים את המתחם...',
			'pick_cx' => 'מתחם', 'signed_of_all' => 'נספרות כחתומות, מכל הדירות במתחם', 'yes_of' => '{y} מתוך {n} דירות',
			'gap_two_thirds' => 'עוד {n} חתימות עד שני שלישים מהדירות במתחם', 'gap_two_thirds_ok' => 'שני שלישים מהדירות במתחם חתמו. זה תנאי אחד מתוך שלושה.',
			'tama_note' => 'הרוב הנדרש בתמ"א 38 תלוי במסלול ובבניין, והחדר לא מחשב אותו. בדקו מול עורך הדין של הדיירים.',
			'mark_two_thirds' => 'שני שלישים · תנאי אחד מתוך שלושה', 'legend_label' => 'הדגשה לפי סטטוס', 'st_partial' => 'חתמו חלק מהבעלים',
			'law_t' => 'הרוב המיוחס לפי החוק', 'law_c1' => 'שני שלישים מהדירות במתחם', 'law_c1_d' => '{y} מתוך {n} חתמו. נדרשות {need}.',
			'law_c2' => 'שלוש חמישיות מהדירות בכל בניין', 'law_c2_d' => 'בבניין של 4 או 5 דירות: לפחות 3 דירות, ויותר משני בעלי דירות.',
			'law_c3' => 'יותר ממחצית הרכוש המשותף בכל בניין', 'law_c3_d' => 'לפי החלק של כל דירה ברכוש המשותף, כפי שהוא רשום בנסח הטאבו.',
			'law_need' => 'נדרשות {n}', 'law_need_small' => 'נדרשות 3, ויותר משני בעלים', 'law_not_computed' => 'פחות מ־4 דירות: לבדיקת עורך הדין',
			'law_owners_short' => 'לא מספיק בעלי דירות שונים', 'law_owners_unknown' => 'חסרים שמות בעלים', 'law_common_missing' => 'חסר החלק ברכוש המשותף ל־{n} דירות', 'law_common_short' => 'פחות ממחצית',
			'met' => 'מתקיים', 'short_n' => 'חסרות {n}', 'unknown' => 'חסר נתון',
			'law_note' => 'החדר בודק את הנתונים שהוזנו מול סעיף 1 לחוק פינוי ובינוי (עידוד מיזמי פינוי ובינוי). דירה נספרת כחתומה רק כשכל הבעלים הרשומים בה חתמו. אין בכך ייעוץ משפטי: את הרוב מאשר עורך הדין של הדיירים.',
			'facade_t' => 'חזית הבניינים', 'views_label' => 'תצוגה', 'view_facade' => 'חזית', 'view_3d' => 'סיור 360', 'view_map' => 'מפה',
			'hint_3d' => 'בניין סטנדרטי להמחשה בלבד, לא הבניין שלכם. סובבו והקישו על דירה.',
			'facade_hint' => 'כל משבצת היא דירה. הקישו על דירה כדי לעדכן בעלים, סטטוס ומסמכים.', 'facade_hint_ro' => 'כל משבצת היא דירה, לפי הסטטוס שלה. בלי שמות ובלי הערות.',
			'facade_hint_nb' => 'כך נראה הבניין: כל משבצת היא דירה, לפי הסטטוס שלה. בלי שמות.', 'grid_hidden' => 'בחדר הזה השכנים רואים את הסיכום של כל בניין, בלי הסטטוס של כל דירה.',
			'apt_aria' => '{b}, דירה {n}, קומה {f}: {s}', 'b_signed' => '{y}/{n} חתמו', 'b_35_ok' => 'שלוש חמישיות ✓', 'b_35_short' => 'חסרות {n} לשלוש חמישיות', 'building' => 'בניין',
			'ladder_t' => 'עשרת השלבים', 'ladder_note' => 'משך מוצג רק כשיש לו מקור', 'now' => 'עכשיו:',
			'avg_note' => 'דוח הרשות להתחדשות עירונית לשנת 2025, ממוצע ולא הבטחה', 'reached_at' => 'הושג בתאריך', 'next_actions' => 'הצעדים הבאים', 'set_stage' => 'קביעה כשלב הנוכחי',
			'dl_t' => 'מועדים', 'dl_empty' => 'אין עדיין מועדים. הוסיפו מועדים מההסכמים או מעורך הדין, והחדר יספור את הימים.',
			'dl_past' => 'עבר לפני {n} ימים', 'dl_today' => 'היום', 'dl_in' => 'בעוד {n} ימים', 'dl_label' => 'מה המועד', 'dl_ph' => 'לדוגמה: סוף תקופת ההחתמה לפי ההסכם', 'dl_date' => 'תאריך', 'dl_add' => 'הוספה',
			'dl_note' => 'החדר לא קובע מועדים לפי החוק. את המועדים מזינים מההסכמים ומעורך הדין, והחדר מתריע 30 ימים לפני.',
			'todo_title' => 'המשימות של המתחם', 'todo_note' => 'נגזר מהנתונים בחדר. אין לראות בכך ייעוץ משפטי.',
			'td_reach' => 'ליצור קשר עם {n} בעלי דירות שטרם הושג איתם קשר', 'td_reach_ok' => 'יש קשר עם כל בעלי הדירות',
			'td_23' => 'להגיע לשני שלישים מהדירות במתחם: חסרות {n}', 'td_23_ok' => 'שני שלישים מהדירות במתחם חתמו', 'td_35' => '{b}: חסרות {n} חתימות לשלוש חמישיות מהדירות',
			'td_common' => 'להזין מנסח הטאבו את החלק ברכוש המשותף ל־{n} דירות', 'td_partial' => '{n} דירות סומנו כחתומות, אבל חסרה בהן חתימה של בעלים נוסף',
			'td_docs' => '{n} דירות עם מסמך חסר', 'td_docs_ok' => 'אין דירות עם מסמך חסר', 'td_refused' => '{n} בעלי דירות סירבו: לתאם שיחה עם עורך הדין של הדיירים', 'td_refused_ok' => 'אין סירובים פתוחים',
			'td_deadline' => '{label}: בעוד {n} ימים', 'td_pros' => 'נבחרו עורך דין ושמאי מטעם הדיירים', 'td_dev' => 'נבחר יזם במכרז',
			'docs_title' => 'תמונת המסמכים', 'docs_hint' => 'בחדר מסמנים אילו מסמכים התקבלו. הקבצים עצמם, כולל צילומי תעודות זהות, נשמרים אצלכם ולא בחדר.', 'docs_of' => 'מסמכים',
			'mem_t' => 'שכנים בחדר', 'mem_count' => '{n} הצטרפו בקישור · {p} ממתינים לאישור דירה', 'claim_line' => '{who} ביקש/ה את דירה {n}, {b}', 'approve' => 'אישור', 'reject' => 'דחייה',
			'mem_role' => 'תפקיד', 'role_neighbor' => 'שכן', 'role_committee' => 'נציגות', 'grid_setting' => 'השכנים רואים בחזית את הסטטוס של כל דירה (בלי שמות, בלי הערות ובלי מסמכים)',
			'apt_n' => 'דירה {n}', 'apt_title' => 'הדירה שנבחרה', 'floor' => 'קומה',
			'apt_hint' => 'הקישו על דירה בחזית כדי לעדכן בעלים, סטטוס, מסמכים והערה. כל שינוי נרשם עם התאריך ומי עדכן.',
			'apt_hint_ro' => 'הקישו על דירה בחזית כדי לראות את הסטטוס שלה ואילו מסמכים התקבלו.', 'apt_hint_hidden' => 'בחדר הזה השכנים רואים סיכום לכל בניין.',
			'ro_note' => 'שמות, הערות ופרטי קשר נשארים אצל החברה המארגנת.', 'partial_warn' => 'הדירה סומנה כחתומה, אבל לא כל הבעלים חתמו. היא לא נספרת עד שכולם יחתמו.',
			'owners_t' => 'בעלי הדירה', 'own_add' => 'הוספת בעלים', 'owners_note' => 'דירה נספרת כחתומה רק כשכל הבעלים הרשומים בה חתמו. שמות הבעלים גלויים רק לצוות.',
			'own_ph' => 'שם או ראשי תיבות', 'own_name' => 'שם הבעלים', 'own_share' => 'חלק בדירה', 'own_heir' => 'יורש/ת', 'own_signed' => 'חתם/ה', 'remove' => 'הסרה',
			'status' => 'סטטוס', 'common_l' => 'החלק ברכוש המשותף (מנסח הטאבו)', 'contact_l' => 'פרטי קשר (פנימי)', 'note_l' => 'הערה (פנימית)', 'save' => 'שמירה', 'version_line' => 'גרסה {v}',
			'log_t' => 'היסטוריית הדירה', 'log_loading' => 'טוענים...', 'log_empty' => 'אין עדיין שינויים לדירה הזו.', 'someone' => 'איש צוות',
			'ev_status' => '{who}: הסטטוס שונה מ"{from}" ל"{to}"', 'ev_doc_on' => '{who}: סומן שהתקבל {doc}', 'ev_doc_off' => '{who}: הוסר הסימון של {doc}',
			'ev_owners' => '{who}: רשימת הבעלים עודכנה ({n} בעלים, חתמו {s})', 'ev_common' => '{who}: החלק ברכוש המשותף עודכן ל־{to}', 'ev_note' => '{who}: ההערה עודכנה', 'ev_contact' => '{who}: פרטי הקשר עודכנו',
			'ev_claim_ok' => '{who}: אושר שכן לדירה הזו', 'ev_claim_no' => '{who}: נדחתה בקשה של שכן לדירה הזו',
			'saving' => 'שומרים...', 'saved_v' => 'נשמר. גרסה {v}. הספירה עודכנה.', 'unchanged' => 'לא היה מה לשמור.',
			'conflict' => '{who} עדכן/ה את הדירה הזו לפני רגע ({at}). הנתונים רועננו: בדקו ושמרו שוב.', 'save_fail' => 'השמירה לא הצליחה. נסו שוב.',
			'up_sub' => '{name}. הנציגות והחברה המארגנת מפרסמות פעם אחת, וכל השכנים רואים.', 'up_new' => 'עדכון חדש לכל המתחם', 'upd_ph' => 'מה חדש בפרויקט?',
			'up_note' => 'העדכון מופיע אצל כל מי שהצטרף לחדר, ואפשר לשלוח אותו גם לקבוצת הוואטסאפ.', 'upd_send' => 'פרסום העדכון', 'up_done' => 'העדכון פורסם בחדר.',
			'wa_send' => 'שליחה לקבוצת הוואטסאפ', 'wa_tail' => 'כל הפרטים בחדר הבניין:', 'auto_badge' => 'עדכון תקופתי', 'upd_none' => 'אין עדכונים עדיין.',
			'inv_title' => 'הזמנת השכנים', 'inv_note' => 'קישור אחד לקבוצת הוואטסאפ של הבניין. מי שנכנס רואה את מצב הבניין, ואת הדירה שלו אחרי שתאשרו אותה.',
			'copy_link' => 'העתקת הקישור', 'copied' => 'הקישור הועתק', 'wa_share_link' => 'שליחת הקישור בוואטסאפ', 'wa_invite' => 'הצטרפו לחדר הבניין שלנו, כדי לראות את מצב ההתחדשות:',
			'inv_new' => 'קישור חדש', 'inv_new_note' => 'קישור חדש מבטל את הקודם. מי שכבר הצטרף נשאר בחדר.', 'inv_btn' => 'יצירת קישור הזמנה',
			'phone_caption' => 'כך שכן רואה את החדר בטלפון (דירה לדוגמה מתוך המתחם)', 'nb_room' => 'חדר הבניין · {name}', 'nb_signed' => 'כמה חתמו במתחם',
			'nb_short' => 'עוד {n} חתימות עד שני שלישים מהדירות במתחם.', 'nb_stage' => 'השלב', 'nb_mine' => 'הדירה שלכם', 'nb_owners' => '{n} בעלים רשומים, חתמו {s}',
			'nb_have' => 'התקבל:', 'nb_miss' => 'חסר:', 'nb_full' => 'כל המסמכים התקבלו', 'nb_claim_hint' => 'אחרי שהשכן בוחר את הדירה שלו והחברה מאשרת, הוא רואה כאן את המצב שלה.',
			'nb_pending' => 'הבקשה לדירה {n} נשלחה. אחרי שהחברה המארגנת תאשר, תראו כאן את מצב הדירה שלכם.', 'nb_rejected' => 'הבקשה הקודמת לא אושרה. בדקו את מספר הדירה ושלחו שוב, או פנו לנציגות.',
			'nb_claim_q' => 'באיזו דירה אתם גרים? אחרי אישור החברה המארגנת תראו כאן את מצב הדירה שלכם.', 'choose' => 'בחרו דירה', 'nb_claim_send' => 'שליחה לאישור',
			'nb_claim_note' => 'רק אתם והצוות רואים את הדירה שלכם. שכנים אחרים לא רואים אותה.', 'nb_last' => 'העדכון האחרון', 'nb_updates' => 'עדכונים',
			'nb_privacy' => 'השכנים רואים את התמונה הכללית ואת הדירה שלהם בלבד, בלי שמות של שכנים אחרים ובלי הערות.',
			'print' => 'הדפסה או שמירה כ־PDF', 'csv' => 'ייצוא לאקסל', 'rep_t' => 'דוח מצב · {name}', 'rep_by' => 'מוגש לנציגות הדיירים על ידי {org}', 'rep_by_room' => 'מוגש לנציגות הדיירים', 'as_of' => 'נכון ל־',
			'rep_consents' => 'ההסכמות', 'rep_consents_p' => '{y} מתוך {n} דירות נספרות כחתומות ({p}%).', 'rep_partial' => 'בעוד {n} דירות חתמו רק חלק מהבעלים.', 'rep_inproc' => 'בתהליך, כולל חסרי מסמכים', 'rep_35' => 'שלוש חמישיות', 'total' => 'סך הכל',
			'rep_month' => 'מה נעשה בחודש האחרון', 'rep_month_none' => 'לא פורסמו עדכונים בחודש האחרון.',
			'rep_foot' => 'הדוח מבוסס על הנתונים שעודכנו בחדר. אינו ייעוץ משפטי. הרוב הנדרש בכל מסלול נבדק מול עורך הדין של הדיירים.',
			'csv_counted' => 'נספרת כחתומה', 'csv_updated' => 'עודכן', 'gauge' => 'חתמו', 'compounds' => 'מתחמי התחדשות בעיר', 'map_approx' => 'מיקום משוער ברמת העיר',
			'track_pinui_binui' => 'פינוי בינוי', 'track_tama38_1' => 'חיזוק (תמ"א 38/1)', 'track_tama38_2' => 'הריסה ובנייה', 'track_unclear' => 'המסלול טרם הוכרע',
		);
		if ( 'en' === $lang ) {
			return array_merge( $he, array(
				'load_fail' => 'Could not load the room. Try refreshing the page.',
				'room_title' => 'Management room', 'room_building' => 'Building room', 'room_demo' => 'Sample room', 'brand_mark' => 'N', 'brand_sub' => 'Urban renewal · Nadlan',
				'demo_badge' => 'Sample data', 'managed_by' => 'Managed by {org}', 'org_line' => 'Staff: {s} · Complexes: {c}', 'tabs_label' => 'Room screens',
				'tab_portfolio' => 'Portfolio', 'tab_complex' => 'Complex', 'tab_updates' => 'Updates for residents', 'tab_report' => 'Committee report',
				'read_only' => 'The organizing company\'s account period ended. The room is read-only and all its data is kept.',
				'stage_of' => 'Stage {n} of 10', 'two_thirds' => 'Two thirds',
				'attn_refused' => '{n} refused', 'attn_unreached' => '{n} not reached', 'attn_idle' => 'no update for {n} days', 'attn_deadline' => 'deadline in {n} days: {label}', 'attn_deadline_passed' => 'deadline passed {n} days ago: {label}', 'attn_lead' => 'Needs attention:',
				'next_two_thirds' => '{n} more signatures to two thirds of the apartments in the complex', 'next_reach' => 'Reach {n} owners not contacted yet', 'next_deadline' => '{label}: in {n} days',
				'pf_sub' => 'Every complex you run, at a glance: where it stands, how many signed and what comes next.', 'new_complex' => 'New complex',
				'kpi_cx' => 'Complexes', 'kpi_bld' => 'Buildings', 'kpi_apt' => 'Apartments', 'kpi_yes' => 'Signed, whole portfolio', 'kpi_miss' => 'Apartments missing a document', 'kpi_attn' => 'Complexes needing attention',
				'filter_label' => 'Filter complexes', 'f_all' => 'All', 'f_pinui_binui' => 'Pinui-Binui', 'f_tama' => 'TAMA 38', 'f_attn' => 'Needs attention',
				'pf_empty' => 'No complexes yet. Open the first one: a name, a city, and the buildings with their floors and apartments.',
				'one_building' => 'one building', 'n_buildings' => '{n} buildings', 'n_apts' => '{n} apartments', 'updated_on' => 'updated {d}',
				'col_cx' => 'Complex', 'col_track' => 'Track', 'col_stage' => 'Stage', 'col_signed' => 'Signed', 'col_miss' => 'Missing a document', 'col_next' => 'Next step',
				'pf_foot' => 'Rooms are free for residents and committees. A neighbor sees the building picture and their own apartment only.',
				'f_b_label' => 'Building name', 'f_b_addr' => 'Address', 'f_floors' => 'Floors', 'f_upf' => 'Apartments per floor', 'f_cx_name' => 'Complex name', 'f_city' => 'City',
				'add_building' => 'Add a building', 'create_cx' => 'Open the complex', 'new_cx_note' => 'Every apartment starts as "not yet reached". Owners, documents and signatures are updated apartment by apartment.', 'opening' => 'Opening the complex...',
				'pick_cx' => 'Complex', 'signed_of_all' => 'counted as signed, of all apartments in the complex', 'yes_of' => '{y} of {n} apartments',
				'gap_two_thirds' => '{n} more signatures to two thirds of the apartments in the complex', 'gap_two_thirds_ok' => 'Two thirds of the apartments in the complex signed. That is one condition of three.',
				'tama_note' => 'The majority TAMA 38 needs depends on the track and the building; the room does not compute it. Check with the residents\' lawyer.',
				'mark_two_thirds' => 'Two thirds · one condition of three', 'legend_label' => 'Highlight by status', 'st_partial' => 'Some owners signed',
				'law_t' => 'The special majority under the law', 'law_c1' => 'Two thirds of the apartments in the complex', 'law_c1_d' => '{y} of {n} signed. {need} needed.',
				'law_c2' => 'Three fifths of the apartments in each building', 'law_c2_d' => 'A building of 4 or 5 apartments: at least 3 apartments, and more than two owners.',
				'law_c3' => 'More than half of the common property in each building', 'law_c3_d' => 'By each apartment\'s share of the common property, as registered in the Tabu extract.',
				'law_need' => '{n} needed', 'law_need_small' => '3 needed, and more than two owners', 'law_not_computed' => 'Fewer than 4 apartments: for the lawyer to check',
				'law_owners_short' => 'Not enough different owners', 'law_owners_unknown' => 'Owner names missing', 'law_common_missing' => 'Common-property share missing for {n} apartments', 'law_common_short' => 'Less than half',
				'met' => 'Met', 'short_n' => '{n} short', 'unknown' => 'Data missing',
				'law_note' => 'The room checks the data entered against section 1 of the Pinui-Binui Law (Encouraging Pinui-Binui Projects). An apartment counts as signed only when every registered owner signed. This is not legal advice: the residents\' lawyer confirms the majority.',
				'facade_t' => 'The building faces', 'views_label' => 'View', 'view_facade' => 'Facade', 'view_3d' => '360 tour', 'view_map' => 'Map',
				'hint_3d' => 'A standard building, for illustration only, not your building. Turn it and tap an apartment.',
				'facade_hint' => 'Every cell is an apartment. Tap one to update its owners, status and documents.', 'facade_hint_ro' => 'Every cell is an apartment, by its status. No names, no notes.',
				'facade_hint_nb' => 'This is the building: every cell is an apartment, by its status. No names.', 'grid_hidden' => 'In this room neighbors see a summary for each building, not each apartment\'s status.',
				'apt_aria' => '{b}, apartment {n}, floor {f}: {s}', 'b_signed' => '{y}/{n} signed', 'b_35_ok' => 'three fifths ✓', 'b_35_short' => '{n} short of three fifths', 'building' => 'Building',
				'ladder_t' => 'The ten stages', 'ladder_note' => 'A duration shows only when it has a source', 'now' => 'Now:',
				'avg_note' => 'the Urban Renewal Authority report for 2025, an average, not a promise', 'reached_at' => 'Reached on', 'next_actions' => 'Next actions', 'set_stage' => 'Set as current stage',
				'dl_t' => 'Deadlines', 'dl_empty' => 'No deadlines yet. Add dates from the agreements or from the lawyer, and the room counts the days.',
				'dl_past' => 'passed {n} days ago', 'dl_today' => 'today', 'dl_in' => 'in {n} days', 'dl_label' => 'What is due', 'dl_ph' => 'For example: end of the signing period under the agreement', 'dl_date' => 'Date', 'dl_add' => 'Add',
				'dl_note' => 'The room sets no legal deadline itself. Dates come from the agreements and the lawyer; the room warns 30 days ahead.',
				'todo_title' => 'Tasks for the complex', 'todo_note' => 'Derived from the room\'s data. Not legal advice.',
				'td_reach' => 'Reach {n} owners not contacted yet', 'td_reach_ok' => 'Every owner has been reached',
				'td_23' => 'Reach two thirds of the apartments in the complex: {n} short', 'td_23_ok' => 'Two thirds of the apartments in the complex signed', 'td_35' => '{b}: {n} signatures short of three fifths',
				'td_common' => 'Enter the common-property share from the Tabu extract for {n} apartments', 'td_partial' => '{n} apartments are marked signed but another owner has not signed',
				'td_docs' => '{n} apartments missing a document', 'td_docs_ok' => 'No apartment is missing a document', 'td_refused' => '{n} owners refused: set a call with the residents\' lawyer', 'td_refused_ok' => 'No open refusals',
				'td_deadline' => '{label}: in {n} days', 'td_pros' => 'Residents-side lawyer and appraiser chosen', 'td_dev' => 'Developer chosen in a tender',
				'docs_title' => 'Documents', 'docs_hint' => 'The room records which documents arrived. The files themselves, ID copies included, stay with you, never in the room.', 'docs_of' => 'Documents',
				'mem_t' => 'Neighbors in the room', 'mem_count' => '{n} joined by the link · {p} waiting for apartment approval', 'claim_line' => '{who} asked for apartment {n}, {b}', 'approve' => 'Approve', 'reject' => 'Reject',
				'mem_role' => 'Role', 'role_neighbor' => 'Neighbor', 'role_committee' => 'Committee', 'grid_setting' => 'Neighbors see every apartment\'s status on the facade (no names, no notes, no documents)',
				'apt_n' => 'Apartment {n}', 'apt_title' => 'Selected apartment', 'floor' => 'Floor',
				'apt_hint' => 'Tap an apartment on the facade to update its owners, status, documents and note. Every change is logged with the date and who made it.',
				'apt_hint_ro' => 'Tap an apartment on the facade to see its status and which documents arrived.', 'apt_hint_hidden' => 'In this room neighbors see a summary for each building.',
				'ro_note' => 'Names, notes and contact details stay with the organizing company.', 'partial_warn' => 'Marked signed, but not every owner signed. It does not count until all of them sign.',
				'owners_t' => 'Owners', 'own_add' => 'Add an owner', 'owners_note' => 'An apartment counts as signed only when every registered owner signed. Owner names are visible to staff only.',
				'own_ph' => 'Name or initials', 'own_name' => 'Owner name', 'own_share' => 'Share', 'own_heir' => 'Heir', 'own_signed' => 'Signed', 'remove' => 'Remove',
				'status' => 'Status', 'common_l' => 'Share of the common property (Tabu extract)', 'contact_l' => 'Contact details (internal)', 'note_l' => 'Note (internal)', 'save' => 'Save', 'version_line' => 'Version {v}',
				'log_t' => 'Apartment history', 'log_loading' => 'Loading...', 'log_empty' => 'No changes to this apartment yet.', 'someone' => 'A staff member',
				'ev_status' => '{who}: status changed from "{from}" to "{to}"', 'ev_doc_on' => '{who}: marked {doc} as received', 'ev_doc_off' => '{who}: unmarked {doc}',
				'ev_owners' => '{who}: owners list updated ({n} owners, {s} signed)', 'ev_common' => '{who}: common-property share set to {to}', 'ev_note' => '{who}: note updated', 'ev_contact' => '{who}: contact details updated',
				'ev_claim_ok' => '{who}: a neighbor was approved for this apartment', 'ev_claim_no' => '{who}: a neighbor\'s request for this apartment was rejected',
				'saving' => 'Saving...', 'saved_v' => 'Saved. Version {v}. The count is updated.', 'unchanged' => 'Nothing to save.',
				'conflict' => '{who} updated this apartment a moment ago ({at}). The data was refreshed: check it and save again.', 'save_fail' => 'Saving failed. Try again.',
				'up_sub' => '{name}. The committee and the organizing company post once, and every neighbor sees it.', 'up_new' => 'A new update for the whole complex', 'upd_ph' => 'What is new in the project?',
				'up_note' => 'The update shows for everyone who joined the room, and you can also send it to the WhatsApp group.', 'upd_send' => 'Post the update', 'up_done' => 'The update is posted in the room.',
				'wa_send' => 'Send to the WhatsApp group', 'wa_tail' => 'All the details in the building room:', 'auto_badge' => 'Periodic update', 'upd_none' => 'No updates yet.',
				'inv_title' => 'Invite the neighbors', 'inv_note' => 'One link for the building\'s WhatsApp group. Whoever opens it sees the building picture, and their own apartment once you approve it.',
				'copy_link' => 'Copy the link', 'copied' => 'Link copied', 'wa_share_link' => 'Send the link on WhatsApp', 'wa_invite' => 'Join our building room to follow the renewal:',
				'inv_new' => 'New link', 'inv_new_note' => 'A new link cancels the previous one. Whoever joined stays in the room.', 'inv_btn' => 'Create an invite link',
				'phone_caption' => 'What a neighbor sees on the phone (a sample apartment from the complex)', 'nb_room' => 'Building room · {name}', 'nb_signed' => 'How many signed in the complex',
				'nb_short' => '{n} more signatures to two thirds of the apartments in the complex.', 'nb_stage' => 'The stage', 'nb_mine' => 'Your apartment', 'nb_owners' => '{n} registered owners, {s} signed',
				'nb_have' => 'Received:', 'nb_miss' => 'Missing:', 'nb_full' => 'Every document arrived', 'nb_claim_hint' => 'Once the neighbor picks their apartment and the company approves it, they see its status here.',
				'nb_pending' => 'Your request for apartment {n} was sent. Once the organizing company approves it, you will see your apartment here.', 'nb_rejected' => 'The previous request was not approved. Check the apartment number and send again, or ask the committee.',
				'nb_claim_q' => 'Which apartment is yours? Once the organizing company approves it, you will see your apartment here.', 'choose' => 'Choose an apartment', 'nb_claim_send' => 'Send for approval',
				'nb_claim_note' => 'Only you and the staff see your apartment. Other neighbors do not.', 'nb_last' => 'Latest update', 'nb_updates' => 'Updates',
				'nb_privacy' => 'Neighbors see the overall picture and their own apartment only, with no other neighbor\'s name and no notes.',
				'print' => 'Print or save as PDF', 'csv' => 'Export to Excel', 'rep_t' => 'Status report · {name}', 'rep_by' => 'Submitted to the residents\' committee by {org}', 'rep_by_room' => 'Submitted to the residents\' committee', 'as_of' => 'As of',
				'rep_consents' => 'Consents', 'rep_consents_p' => '{y} of {n} apartments count as signed ({p}%).', 'rep_partial' => 'In {n} more apartments only some owners signed.', 'rep_inproc' => 'In progress, incl. missing documents', 'rep_35' => 'Three fifths', 'total' => 'Total',
				'rep_month' => 'Done in the last month', 'rep_month_none' => 'No updates were posted in the last month.',
				'rep_foot' => 'Based on the data updated in the room. Not legal advice. The majority each track needs is checked with the residents\' lawyer.',
				'csv_counted' => 'Counts as signed', 'csv_updated' => 'Updated', 'gauge' => 'signed', 'compounds' => 'Renewal compounds in the city', 'map_approx' => 'Approximate city location',
				'track_pinui_binui' => 'Pinui-Binui', 'track_tama38_1' => 'Reinforcement (TAMA 38/1)', 'track_tama38_2' => 'Demolish and rebuild', 'track_unclear' => 'Track not decided yet',
			) );
		}
		if ( 'ru' === $lang ) {
			return array_merge( $he, array(
				'load_fail' => 'Не удалось загрузить комнату. Обновите страницу.',
				'room_title' => 'Комната управления', 'room_building' => 'Комната дома', 'room_demo' => 'Пример комнаты', 'brand_mark' => 'N', 'brand_sub' => 'Городское обновление · Nadlan',
				'demo_badge' => 'Данные для примера', 'managed_by' => 'Ведёт {org}', 'org_line' => 'Сотрудники: {s} · Комплексы: {c}', 'tabs_label' => 'Экраны комнаты',
				'tab_portfolio' => 'Портфель комплексов', 'tab_complex' => 'Комплекс', 'tab_updates' => 'Обновления для жильцов', 'tab_report' => 'Отчёт для комитета',
				'read_only' => 'Срок счёта организующей компании истёк. Комната открыта только для чтения, все данные сохранены.',
				'stage_of' => 'Этап {n} из 10', 'two_thirds' => 'Две трети',
				'attn_refused' => 'отказались: {n}', 'attn_unreached' => 'нет связи: {n}', 'attn_idle' => 'нет обновлений {n} дн.', 'attn_deadline' => 'срок через {n} дн.: {label}', 'attn_deadline_passed' => 'срок прошёл {n} дн. назад: {label}', 'attn_lead' => 'Требует внимания:',
				'next_two_thirds' => 'Ещё {n} подписей до двух третей квартир комплекса', 'next_reach' => 'Связаться с {n} собственниками, с которыми ещё нет связи', 'next_deadline' => '{label}: через {n} дн.',
				'pf_sub' => 'Все комплексы, которые вы ведёте, одним взглядом: где каждый находится, сколько подписали и какой следующий шаг.', 'new_complex' => 'Новый комплекс',
				'kpi_cx' => 'Комплексы', 'kpi_bld' => 'Дома', 'kpi_apt' => 'Квартиры', 'kpi_yes' => 'Подписали, по всему портфелю', 'kpi_miss' => 'Квартиры без документа', 'kpi_attn' => 'Комплексы, требующие внимания',
				'filter_label' => 'Фильтр комплексов', 'f_all' => 'Все', 'f_pinui_binui' => 'Пинуй-бинуй', 'f_tama' => 'ТАМА 38', 'f_attn' => 'Требует внимания',
				'pf_empty' => 'Комплексов пока нет. Откройте первый: название, город и дома с этажами и квартирами.',
				'one_building' => 'один дом', 'n_buildings' => 'домов: {n}', 'n_apts' => 'квартир: {n}', 'updated_on' => 'обновлено {d}',
				'col_cx' => 'Комплекс', 'col_track' => 'Трек', 'col_stage' => 'Этап', 'col_signed' => 'Подписали', 'col_miss' => 'Нет документа', 'col_next' => 'Следующий шаг',
				'pf_foot' => 'Комнаты бесплатны для жильцов и комитета. Сосед видит картину дома и только свою квартиру.',
				'f_b_label' => 'Название дома', 'f_b_addr' => 'Адрес', 'f_floors' => 'Этажи', 'f_upf' => 'Квартир на этаже', 'f_cx_name' => 'Название комплекса', 'f_city' => 'Город',
				'add_building' => 'Добавить дом', 'create_cx' => 'Открыть комплекс', 'new_cx_note' => 'Все квартиры начинают со статуса «ещё не связались». Собственников, документы и подписи обновляют квартира за квартирой.', 'opening' => 'Открываем комплекс...',
				'pick_cx' => 'Комплекс', 'signed_of_all' => 'считаются подписанными, из всех квартир комплекса', 'yes_of' => '{y} из {n} квартир',
				'gap_two_thirds' => 'Ещё {n} подписей до двух третей квартир комплекса', 'gap_two_thirds_ok' => 'Две трети квартир комплекса подписали. Это одно условие из трёх.',
				'tama_note' => 'Нужное большинство в ТАМА 38 зависит от трека и дома; комната его не считает. Уточните у адвоката жильцов.',
				'mark_two_thirds' => 'Две трети · одно условие из трёх', 'legend_label' => 'Выделить по статусу', 'st_partial' => 'Подписали не все собственники',
				'law_t' => 'Особое большинство по закону', 'law_c1' => 'Две трети квартир комплекса', 'law_c1_d' => 'Подписали {y} из {n}. Нужно {need}.',
				'law_c2' => 'Три пятых квартир в каждом доме', 'law_c2_d' => 'Дом из 4 или 5 квартир: не менее 3 квартир и более двух собственников.',
				'law_c3' => 'Более половины общего имущества в каждом доме', 'law_c3_d' => 'По доле каждой квартиры в общем имуществе, как она записана в выписке из Табу.',
				'law_need' => 'нужно {n}', 'law_need_small' => 'нужно 3 и более двух собственников', 'law_not_computed' => 'Меньше 4 квартир: проверяет адвокат',
				'law_owners_short' => 'Недостаточно разных собственников', 'law_owners_unknown' => 'Не указаны собственники', 'law_common_missing' => 'Нет доли в общем имуществе у {n} квартир', 'law_common_short' => 'Меньше половины',
				'met' => 'Выполнено', 'short_n' => 'не хватает {n}', 'unknown' => 'Нет данных',
				'law_note' => 'Комната проверяет введённые данные по статье 1 Закона о пинуй-бинуй (поощрение проектов пинуй-бинуй). Квартира считается подписанной, только когда подписали все её зарегистрированные собственники. Это не юридическая консультация: большинство подтверждает адвокат жильцов.',
				'facade_t' => 'Фасады домов', 'views_label' => 'Вид', 'view_facade' => 'Фасад', 'view_3d' => 'Обзор 360', 'view_map' => 'Карта',
				'hint_3d' => 'Стандартный дом, только для наглядности, а не ваш дом. Поверните и нажмите на квартиру.',
				'facade_hint' => 'Каждая клетка обозначает квартиру. Нажмите, чтобы обновить собственников, статус и документы.', 'facade_hint_ro' => 'Каждая клетка обозначает квартиру и её статус. Без имён и заметок.',
				'facade_hint_nb' => 'Так выглядит дом: каждая клетка обозначает квартиру и её статус. Без имён.', 'grid_hidden' => 'В этой комнате соседи видят сводку по каждому дому, без статуса каждой квартиры.',
				'apt_aria' => '{b}, квартира {n}, этаж {f}: {s}', 'b_signed' => 'подписали {y}/{n}', 'b_35_ok' => 'три пятых ✓', 'b_35_short' => 'до трёх пятых не хватает {n}', 'building' => 'Дом',
				'ladder_t' => 'Десять этапов', 'ladder_note' => 'Срок показан, только если у него есть источник', 'now' => 'Сейчас:',
				'avg_note' => 'отчёт Управления по обновлению городов за 2025 год, среднее, не обещание', 'reached_at' => 'Достигнут', 'next_actions' => 'Следующие шаги', 'set_stage' => 'Отметить как текущий этап',
				'dl_t' => 'Сроки', 'dl_empty' => 'Сроков пока нет. Добавьте даты из договоров или от адвоката, и комната будет считать дни.',
				'dl_past' => 'прошёл {n} дн. назад', 'dl_today' => 'сегодня', 'dl_in' => 'через {n} дн.', 'dl_label' => 'Что за срок', 'dl_ph' => 'Например: конец срока сбора подписей по договору', 'dl_date' => 'Дата', 'dl_add' => 'Добавить',
				'dl_note' => 'Комната сама не устанавливает сроков по закону. Даты берут из договоров и у адвоката; комната предупреждает за 30 дней.',
				'todo_title' => 'Задачи комплекса', 'todo_note' => 'Формируется из данных комнаты. Не является юридической консультацией.',
				'td_reach' => 'Связаться с {n} собственниками, с которыми ещё нет связи', 'td_reach_ok' => 'Есть связь со всеми собственниками',
				'td_23' => 'Дойти до двух третей квартир комплекса: не хватает {n}', 'td_23_ok' => 'Две трети квартир комплекса подписали', 'td_35' => '{b}: до трёх пятых не хватает {n} подписей',
				'td_common' => 'Внести из выписки Табу долю в общем имуществе для {n} квартир', 'td_partial' => '{n} квартир отмечены как подписанные, но не подписал ещё один собственник',
				'td_docs' => 'Квартир без какого-либо документа: {n}', 'td_docs_ok' => 'Нет квартир без документов', 'td_refused' => 'Отказались {n} собственников: назначить разговор с адвокатом жильцов', 'td_refused_ok' => 'Открытых отказов нет',
				'td_deadline' => '{label}: через {n} дн.', 'td_pros' => 'Выбраны адвокат и оценщик стороны жильцов', 'td_dev' => 'Застройщик выбран на тендере',
				'docs_title' => 'Документы', 'docs_hint' => 'В комнате отмечают, какие документы получены. Сами файлы, включая копии удостоверений, остаются у вас, а не в комнате.', 'docs_of' => 'Документы',
				'mem_t' => 'Соседи в комнате', 'mem_count' => 'Присоединились по ссылке: {n} · ждут подтверждения квартиры: {p}', 'claim_line' => '{who} просит квартиру {n}, {b}', 'approve' => 'Подтвердить', 'reject' => 'Отклонить',
				'mem_role' => 'Роль', 'role_neighbor' => 'Сосед', 'role_committee' => 'Комитет', 'grid_setting' => 'Соседи видят на фасаде статус каждой квартиры (без имён, заметок и документов)',
				'apt_n' => 'Квартира {n}', 'apt_title' => 'Выбранная квартира', 'floor' => 'Этаж',
				'apt_hint' => 'Нажмите на квартиру на фасаде, чтобы обновить собственников, статус, документы и заметку. Каждое изменение записывается с датой и автором.',
				'apt_hint_ro' => 'Нажмите на квартиру на фасаде, чтобы увидеть её статус и полученные документы.', 'apt_hint_hidden' => 'В этой комнате соседи видят сводку по каждому дому.',
				'ro_note' => 'Имена, заметки и контакты остаются у организующей компании.', 'partial_warn' => 'Квартира отмечена как подписанная, но подписали не все собственники. Она не считается, пока не подпишут все.',
				'owners_t' => 'Собственники', 'own_add' => 'Добавить собственника', 'owners_note' => 'Квартира считается подписанной, только когда подписали все её зарегистрированные собственники. Имена видны только сотрудникам.',
				'own_ph' => 'Имя или инициалы', 'own_name' => 'Имя собственника', 'own_share' => 'Доля', 'own_heir' => 'Наследник', 'own_signed' => 'Подписал', 'remove' => 'Удалить',
				'status' => 'Статус', 'common_l' => 'Доля в общем имуществе (выписка Табу)', 'contact_l' => 'Контакты (внутреннее)', 'note_l' => 'Заметка (внутренняя)', 'save' => 'Сохранить', 'version_line' => 'Версия {v}',
				'log_t' => 'История квартиры', 'log_loading' => 'Загрузка...', 'log_empty' => 'Изменений по этой квартире пока нет.', 'someone' => 'Сотрудник',
				'ev_status' => '{who}: статус изменён с «{from}» на «{to}»', 'ev_doc_on' => '{who}: отмечено получение: {doc}', 'ev_doc_off' => '{who}: снята отметка: {doc}',
				'ev_owners' => '{who}: обновлён список собственников ({n}, подписали {s})', 'ev_common' => '{who}: доля в общем имуществе: {to}', 'ev_note' => '{who}: заметка обновлена', 'ev_contact' => '{who}: контакты обновлены',
				'ev_claim_ok' => '{who}: сосед подтверждён для этой квартиры', 'ev_claim_no' => '{who}: запрос соседа на эту квартиру отклонён',
				'saving' => 'Сохраняем...', 'saved_v' => 'Сохранено. Версия {v}. Подсчёт обновлён.', 'unchanged' => 'Нечего сохранять.',
				'conflict' => '{who} только что обновил(а) эту квартиру ({at}). Данные обновлены: проверьте и сохраните снова.', 'save_fail' => 'Не удалось сохранить. Попробуйте ещё раз.',
				'up_sub' => '{name}. Комитет и организующая компания публикуют один раз, и все соседи видят.', 'up_new' => 'Новое обновление для всего комплекса', 'upd_ph' => 'Что нового в проекте?',
				'up_note' => 'Обновление видят все, кто присоединился к комнате; его можно отправить и в группу WhatsApp.', 'upd_send' => 'Опубликовать', 'up_done' => 'Обновление опубликовано в комнате.',
				'wa_send' => 'Отправить в группу WhatsApp', 'wa_tail' => 'Все подробности в комнате дома:', 'auto_badge' => 'Периодическое обновление', 'upd_none' => 'Обновлений пока нет.',
				'inv_title' => 'Пригласить соседей', 'inv_note' => 'Одна ссылка для группы WhatsApp дома. Открывший видит картину дома, а свою квартиру после вашего подтверждения.',
				'copy_link' => 'Скопировать ссылку', 'copied' => 'Ссылка скопирована', 'wa_share_link' => 'Отправить ссылку в WhatsApp', 'wa_invite' => 'Присоединяйтесь к комнате нашего дома, чтобы следить за обновлением:',
				'inv_new' => 'Новая ссылка', 'inv_new_note' => 'Новая ссылка отменяет прежнюю. Кто уже присоединился, остаётся в комнате.', 'inv_btn' => 'Создать ссылку-приглашение',
				'phone_caption' => 'Так сосед видит комнату в телефоне (квартира для примера из комплекса)', 'nb_room' => 'Комната дома · {name}', 'nb_signed' => 'Сколько подписали в комплексе',
				'nb_short' => 'Ещё {n} подписей до двух третей квартир комплекса.', 'nb_stage' => 'Этап', 'nb_mine' => 'Ваша квартира', 'nb_owners' => 'Собственников: {n}, подписали: {s}',
				'nb_have' => 'Получено:', 'nb_miss' => 'Не хватает:', 'nb_full' => 'Все документы получены', 'nb_claim_hint' => 'Когда сосед выберет свою квартиру и компания подтвердит, он увидит здесь её статус.',
				'nb_pending' => 'Запрос на квартиру {n} отправлен. После подтверждения организующей компанией вы увидите здесь свою квартиру.', 'nb_rejected' => 'Прежний запрос не подтверждён. Проверьте номер квартиры и отправьте снова или обратитесь в комитет.',
				'nb_claim_q' => 'В какой квартире вы живёте? После подтверждения организующей компанией вы увидите здесь свою квартиру.', 'choose' => 'Выберите квартиру', 'nb_claim_send' => 'Отправить на подтверждение',
				'nb_claim_note' => 'Вашу квартиру видите только вы и сотрудники. Другие соседи её не видят.', 'nb_last' => 'Последнее обновление', 'nb_updates' => 'Обновления',
				'nb_privacy' => 'Соседи видят общую картину и только свою квартиру, без имён других соседей и без заметок.',
				'print' => 'Печать или сохранение в PDF', 'csv' => 'Экспорт в Excel', 'rep_t' => 'Отчёт о состоянии · {name}', 'rep_by' => 'Для комитета жильцов от {org}', 'rep_by_room' => 'Для комитета жильцов', 'as_of' => 'На',
				'rep_consents' => 'Согласия', 'rep_consents_p' => 'Подписанными считаются {y} из {n} квартир ({p}%).', 'rep_partial' => 'Ещё в {n} квартирах подписали не все собственники.', 'rep_inproc' => 'В процессе, вкл. без документов', 'rep_35' => 'Три пятых', 'total' => 'Итого',
				'rep_month' => 'Что сделано за последний месяц', 'rep_month_none' => 'За последний месяц обновлений не было.',
				'rep_foot' => 'Отчёт основан на данных, обновлённых в комнате. Не является юридической консультацией. Нужное большинство в каждом треке проверяет адвокат жильцов.',
				'csv_counted' => 'Считается подписанной', 'csv_updated' => 'Обновлено', 'gauge' => 'подписали', 'compounds' => 'Комплексы обновления в городе', 'map_approx' => 'Примерное положение на уровне города',
				'track_pinui_binui' => 'Пинуй-бинуй', 'track_tama38_1' => 'Укрепление (ТАМА 38/1)', 'track_tama38_2' => 'Снос и строительство', 'track_unclear' => 'Трек ещё не выбран',
			) );
		}
		return $he;
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
	/**
	 * Pro: $role null = the current user's role in this room (renewal-room.php); the demo route passes 'demo'.
	 * The payload is built in full and then FILTERED BY ROLE before it leaves the server: a neighbour never receives
	 * another apartment's note, contact note, owners, share or version, nor the members list or the change log.
	 */
	function nadlan_ur_space_payload( $id, $lang = 'he', $role = null ) {
		$apts = function_exists( 'nadlan_rr_apartments' ) ? nadlan_rr_apartments( $id ) : (array) json_decode( (string) get_post_meta( $id, 'renewal_apartments', true ), true );
		$buildings = function_exists( 'nadlan_rr_buildings' ) ? nadlan_rr_buildings( $id ) : array();
		$track = (string) get_post_meta( $id, 'track', true );
		$counts = function_exists( 'nadlan_rr_counts' ) ? nadlan_rr_counts( $apts ) : null;
		$total = count( $apts );
		$yes = $counts ? (int) $counts['yes'] : count( array_filter( $apts, function ( $a ) { return ( $a['consent_status'] ?? '' ) === 'consented'; } ) );
		$city = (string) get_post_meta( $id, 'city', true );
		$meta = nadlan_ur_stage_meta( $lang );
		$org = (int) get_post_meta( $id, 'org_id', true );
		$p = array(
			'id'        => (int) $id,
			// the raw title: get_the_title() prefixes a private post with "פרטי:", and the demo room is private (HAD-396)
			'title'     => html_entity_decode( (string) get_post_field( 'post_title', $id ), ENT_QUOTES, 'UTF-8' ),
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
		if ( ! function_exists( 'nadlan_rr_filter_payload' ) ) { return $p; }
		$p['complex_name'] = (string) get_post_meta( $id, 'complex_name', true );
		$p['street_line']  = (string) get_post_meta( $id, 'street_line', true );
		$p['buildings']    = $buildings;
		$p['counts']       = $counts;
		$p['law']          = nadlan_rr_law( $apts, $buildings, $track );
		$p['docs_rollup']  = nadlan_rr_docs_rollup( $apts );
		$p['deadlines']    = nadlan_rr_deadlines( $id );
		$p['org']          = ( $org && function_exists( 'nadlan_rr_org_public' ) ) ? nadlan_rr_org_public( $org ) : null;
		$p['is_sample']    = '1' === (string) get_post_meta( $id, 'is_sample', true );
		return nadlan_rr_filter_payload( $p, null === $role ? nadlan_rr_role( $id ) : (string) $role, $id );
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
			$key = 'nlur_demo_payload_v2_' . $lang; // v2 (1.72.537): the role-filtered payload, never the old cached one
			$p = get_transient( $key );
			if ( ! is_array( $p ) ) {
				$ids = get_posts( array( 'post_type' => 'nadlan_renewal', 'post_status' => 'any', 'posts_per_page' => 1,
					'fields' => 'ids', 'meta_query' => array( array( 'key' => 'is_demo', 'value' => '1' ) ) ) );
				if ( ! $ids ) { return new WP_Error( 'not_found', 'no demo space', array( 'status' => 404 ) ); }
				$p = nadlan_ur_space_payload( (int) $ids[0], $lang, 'demo' ); // Pro: the demo role (statuses and ticks, no names, no notes)
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
			// Pro: an organizer's staff opens complexes for its account (org_id), with several buildings
			$org = (int) $req->get_param( 'org_id' );
			if ( $org && ( ! function_exists( 'nadlan_rr_org_staff_role' ) || ( '' === nadlan_rr_org_staff_role( $org, get_current_user_id() ) && ! current_user_can( 'manage_options' ) ) ) ) {
				return new WP_Error( 'forbidden', 'not staff of this account', array( 'status' => 403 ) );
			}
			if ( $org && function_exists( 'nadlan_rr_org_active' ) && ! nadlan_rr_org_active( $org ) ) {
				return new WP_Error( 'lapsed', 'the account is read-only', array( 'status' => 402 ) );
			}
			if ( nadlan_ur_rate_limited( 'space', $org ? 40 : 5, DAY_IN_SECONDS ) ) {
				return new WP_Error( 'rate_limited', $org ? 'אפשר לפתוח עד 40 מתחמים ביום.' : 'אפשר לפתוח עד 5 חדרים ביום.', array( 'status' => 429 ) );
			}
			$city   = mb_substr( sanitize_text_field( (string) $req->get_param( 'city' ) ), 0, 60 );
			$addr   = mb_substr( sanitize_text_field( (string) $req->get_param( 'address' ) ), 0, 120 );
			$floors = max( 1, min( 40, (int) $req->get_param( 'floors' ) ) );
			$upf    = max( 1, min( 12, (int) $req->get_param( 'units_per_floor' ) ) );
			$name   = mb_substr( sanitize_text_field( (string) $req->get_param( 'name' ) ), 0, 80 );
			$blist  = array();
			foreach ( array_slice( (array) $req->get_param( 'buildings' ), 0, 12 ) as $b ) {
				if ( ! is_array( $b ) ) { continue; }
				$blist[] = array(
					'key' => 'b' . ( count( $blist ) + 1 ),
					'label' => mb_substr( sanitize_text_field( (string) ( $b['label'] ?? '' ) ), 0, 40 ),
					'address' => mb_substr( sanitize_text_field( (string) ( $b['address'] ?? '' ) ), 0, 120 ),
					'floors' => max( 1, min( 40, (int) ( $b['floors'] ?? 1 ) ) ),
					'upf' => max( 1, min( 12, (int) ( $b['upf'] ?? 1 ) ) ),
				);
			}
			if ( $blist && '' === $addr ) { $addr = $blist[0]['address']; }
			if ( '' === $city || ( '' === $addr && '' === $name ) ) { return new WP_Error( 'bad_request', 'נדרשות עיר וכתובת.', array( 'status' => 400 ) ); }
			if ( ! $blist ) { $blist = array( array( 'key' => 'b1', 'label' => '', 'address' => $addr, 'floors' => $floors, 'upf' => $upf ) ); }
			$max = $org ? 1200 : 400;
			$n = 0; foreach ( $blist as $b ) { $n += $b['floors'] * $b['upf']; }
			if ( $n > $max ) { return new WP_Error( 'too_big', 'עד ' . $max . ' דירות בחדר.', array( 'status' => 400 ) ); }
			$id = wp_insert_post( array(
				'post_type' => 'nadlan_renewal', 'post_status' => 'private',
				'post_title' => ( '' !== $name ? $name : $addr ) . ', ' . $city,
			), true );
			if ( is_wp_error( $id ) ) { return $id; }
			// seed the consent grid: every apartment starts unreached. A one-building room keeps the live ids (f1-1);
			// a complex prefixes the building key (b2-f1-1).
			$dirs = array( 'west', 'south', 'east', 'north' );
			$apts = array();
			$multi = count( $blist ) > 1;
			foreach ( $blist as $b ) {
				for ( $f = 1; $f <= $b['floors']; $f++ ) {
					for ( $p = 0; $p < $b['upf']; $p++ ) {
						$num = ( $f - 1 ) * $b['upf'] + $p + 1;
						$apts[] = array( 'id' => ( $multi ? $b['key'] . '-' : '' ) . 'f' . $f . '-' . ( $p + 1 ), 'floor' => $f, 'pos' => $p,
							'dir' => $dirs[ $p % 4 ], 'label' => 'דירה ' . $num, 'building' => $b['key'], 'num' => $num, 'v' => 0,
							'consent_status' => 'unreached', 'docs' => array(), 'contact_note' => '', 'note' => '' );
					}
				}
			}
			update_post_meta( $id, 'owner_user_id', get_current_user_id() );
			update_post_meta( $id, 'address', $addr );
			update_post_meta( $id, 'city', $city );
			update_post_meta( $id, 'floors', $blist[0]['floors'] );
			update_post_meta( $id, 'units_per_floor', $blist[0]['upf'] );
			update_post_meta( $id, 'track', sanitize_key( (string) $req->get_param( 'track' ) ) );
			update_post_meta( $id, 'renewal_stage', 0 );
			update_post_meta( $id, 'renewal_buildings', wp_slash( wp_json_encode( $blist, JSON_UNESCAPED_UNICODE ) ) );
			if ( '' !== $name ) { update_post_meta( $id, 'complex_name', $name ); }
			if ( $org ) { update_post_meta( $id, 'org_id', $org ); }
			update_post_meta( $id, 'renewal_apartments', wp_slash( wp_json_encode( nadlan_ur_clean_apartments( $apts, $max ), JSON_UNESCAPED_UNICODE ) ) );
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
			// the v2 bulk save, kept for a cached old script. Pro: the room's fields the old script does not know are kept,
			// every changed apartment gets its version bumped and its changes written to the change log. The Pro script
			// saves one apartment per request instead (renewal-room.php).
			$id = (int) $req['id'];
			$max = (int) get_post_meta( $id, 'org_id', true ) ? 1200 : 400;
			$clean = nadlan_ur_clean_apartments( (array) $req->get_param( 'apartments' ), $max );
			if ( function_exists( 'nadlan_rr_apartments' ) ) {
				$old = array();
				foreach ( nadlan_rr_apartments( $id ) as $a ) { $old[ $a['id'] ] = $a; }
				foreach ( $clean as $i => $a ) {
					if ( ! isset( $old[ $a['id'] ] ) ) { continue; }
					$o = $old[ $a['id'] ];
					foreach ( array( 'building', 'num', 'owners', 'common_share' ) as $k ) { if ( ! isset( $a[ $k ] ) && isset( $o[ $k ] ) ) { $clean[ $i ][ $k ] = $o[ $k ]; } }
					list( , $ch ) = nadlan_rr_apply_patch( $o, $clean[ $i ] );
					$clean[ $i ]['v'] = (int) $o['v'] + ( $ch ? 1 : 0 );
					if ( ! $ch ) { $clean[ $i ]['updated'] = $o['updated'] ?? $clean[ $i ]['updated']; continue; }
					$clean[ $i ]['updated_by'] = get_current_user_id();
					foreach ( $ch as $c ) { nadlan_rr_log_event( $id, $a['id'], $c[0], $c[1], $c[2], $clean[ $i ]['v'] ); }
				}
			}
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

	// Pro: the committee (a member a manager marked as committee) may post updates too
	$upd_perm = function ( $req ) use ( $mng_perm ) {
		if ( $mng_perm( $req ) ) { return true; }
		return is_user_logged_in() && nadlan_ur_space_on() && nadlan_ur_space_ok( (int) $req['id'] ) && function_exists( 'nadlan_rr_role' ) && 'committee' === nadlan_rr_role( (int) $req['id'] );
	};
	register_rest_route( 'nadlan/v1', '/renewal-space/(?P<id>\d+)/update', array(
		'methods' => 'POST', 'permission_callback' => $upd_perm,
		'callback' => function ( WP_REST_Request $req ) {
			$id = (int) $req['id'];
			$text = mb_substr( sanitize_textarea_field( (string) $req->get_param( 'text' ) ), 0, 1000 );
			if ( '' === $text ) { return new WP_Error( 'bad_request', 'עדכון ריק.', array( 'status' => 400 ) ); }
			$ups = (array) json_decode( (string) get_post_meta( $id, 'renewal_updates', true ), true );
			$me = wp_get_current_user();
			array_unshift( $ups, array( 'text' => $text, 'at' => current_time( 'mysql' ), 'by' => get_current_user_id(),
				'by_name' => $me && $me->exists() ? mb_substr( (string) $me->display_name, 0, 60 ) : '', 'from' => function_exists( 'nadlan_rr_role' ) ? nadlan_rr_role( $id ) : '' ) );
			update_post_meta( $id, 'renewal_last_activity', current_time( 'mysql' ) );
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
	foreach ( array( 'he', 'en', 'ru' ) as $l ) { delete_transient( 'nlur_demo_payload_v2_' . $l ); }
} );

/* ---------- the periodic consent notice (the Singapore ritual, feed-only) ----------
   Every ~28 days each active room gets an automatic feed post with the current
   consent percentage and stage - the whole building sees the same number without
   anyone having to ask. No email involved (deliverability-last law); pure feed. */
add_action( 'init', function () {
	if ( ! wp_next_scheduled( 'nadlan_ur_periodic_tick' ) ) {
		wp_schedule_event( time() + HOUR_IN_SECONDS, 'daily', 'nadlan_ur_periodic_tick' );
	}
} );
add_action( 'nadlan_ur_periodic_tick', function () {
	if ( get_option( 'nadlan_ur_monthly_note', '1' ) !== '1' || ! nadlan_ur_space_on() ) { return; }
	$ids = get_posts( array( 'post_type' => 'nadlan_renewal', 'post_status' => 'any', 'posts_per_page' => 100, 'fields' => 'ids' ) );
	foreach ( $ids as $id ) {
		if ( '1' === (string) get_post_meta( $id, 'is_demo', true ) ) { continue; }
		$last = (int) get_post_meta( $id, 'renewal_last_autonote', true );
		if ( $last && ( time() - $last ) < 28 * DAY_IN_SECONDS ) { continue; }
		$apts = json_decode( (string) get_post_meta( $id, 'renewal_apartments', true ), true );
		if ( ! is_array( $apts ) || ! count( $apts ) ) { continue; }
		// a room younger than 28 days is skipped too - let it fill up first
		$created = get_post_time( 'U', true, $id );
		if ( $created && ( time() - $created ) < 28 * DAY_IN_SECONDS ) { continue; }
		$total = count( $apts );
		// Pro: the careful count (status signed AND every listed owner signed), the same number the room shows
		$yes = count( array_filter( $apts, function ( $a ) { return function_exists( 'nadlan_rr_counted' ) ? nadlan_rr_counted( $a ) : ( $a['consent_status'] ?? '' ) === 'consented'; } ) );
		$pct = $total ? round( $yes / $total * 100 ) : 0;
		$stage = (int) get_post_meta( $id, 'renewal_stage', true );
		$labels = function_exists( 'nadlan_ur_ladder_labels' ) ? nadlan_ur_ladder_labels() : array();
		$text = 'עדכון תקופתי: ' . $yes . ' מתוך ' . $total . ' דירות חתמו (' . $pct . '%). השלב הנוכחי: ' . ( $labels[ $stage ] ?? $stage ) . '.';
		$ups = (array) json_decode( (string) get_post_meta( $id, 'renewal_updates', true ), true );
		array_unshift( $ups, array( 'text' => $text, 'at' => current_time( 'mysql' ), 'by' => 0, 'auto' => 1 ) );
		update_post_meta( $id, 'renewal_updates', wp_slash( wp_json_encode( array_slice( $ups, 0, 200 ), JSON_UNESCAPED_UNICODE ) ) );
		update_post_meta( $id, 'renewal_last_autonote', time() );
	}
} );

/* ---------- member notices (deliverability-last: OFF until flipped) ---------- */
if ( ! function_exists( 'nadlan_ur_queue_notice' ) ) {
	function nadlan_ur_queue_notice( $space_id, $text ) {
		$members = nadlan_ur_members( $space_id );
		$entry = array( 'space' => (int) $space_id, 'text' => mb_substr( $text, 0, 200 ),
			'recipients' => count( $members ), 'at' => current_time( 'mysql' ), 'sent' => false );
		if ( get_option( 'nadlan_renewal_notify_enabled', '0' ) === '1' && $members ) {
			$subject = 'עדכון מחדר ההתחדשות: ' . get_the_title( $space_id );
			$body = '<div dir="rtl" style="font-family:Arial,sans-serif;max-width:540px;margin:0 auto">' .
				'<p style="color:#12202A;line-height:1.7">' . esc_html( $text ) . '</p>' .
				'<p><a href="' . esc_url( home_url( '/my-renewal/?space=' . (int) $space_id ) ) . '" style="display:inline-block;background:#1F4B5C;color:#FFFFFF;font-weight:600;border-radius:6px;padding:12px 18px;text-decoration:none">לחדר הפרויקט</a></p>' .
				'<p style="font-size:11.5px;color:#5E6A75">קיבלתם עדכון זה כחברים בחדר ההתחדשות של הבניין באתר nad-lan.co.il.</p></div>';
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

if ( ! function_exists( 'nadlan_ur_page_header' ) ) {
	/** HAD-408: get_header() on this block theme prints only WP's theme-compat header (the site name as a bare second <h1>,
	 *  no logo, no menu). Same pattern as the directory, the archives and the 404: the compat site name becomes a hidden <p>,
	 *  then the theme's header template part (swapped for the site header by home-v3.php) is printed. */
	function nadlan_ur_page_header() {
		if ( function_exists( 'nadlan_dir_header_single_h1' ) ) { nadlan_dir_header_single_h1(); } else { get_header(); }
		if ( function_exists( 'block_template_part' ) ) { block_template_part( 'header' ); }
	}
}
if ( ! function_exists( 'nadlan_ur_page_footer' ) ) {
	/** HAD-408: get_footer() is a noop without footer.php; the theme's footer template part is printed first. */
	function nadlan_ur_page_footer() {
		if ( function_exists( 'block_template_part' ) ) { block_template_part( 'footer' ); }
		get_footer();
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

	// anonymous visitors and members-without-a-room get the PRODUCT LANDING, not a login wall.
	// The landing copy exists in HE + EN; RU rooms are fully supported, so ?lang=ru lands on EN
	// (never a half-translated page) while the room itself renders in Russian.
	$landing_lang = 'ru' === $lang ? 'en' : $lang;
	if ( ! is_user_logged_in() ) { nadlan_ur_render_landing( $landing_lang, false ); exit; }
	$uid = get_current_user_id();
	$u = wp_get_current_user();
	$owned = get_posts( array( 'post_type' => 'nadlan_renewal', 'post_status' => 'any', 'posts_per_page' => 20, 'fields' => 'ids',
		'meta_query' => array( array( 'key' => 'owner_user_id', 'value' => $uid ) ) ) );
	$member = get_posts( array( 'post_type' => 'nadlan_renewal', 'post_status' => 'any', 'posts_per_page' => 40, 'fields' => 'ids',
		'meta_query' => array( array( 'key' => 'member_emails', 'value' => $u->user_email, 'compare' => 'LIKE' ) ) ) );
	// Pro: the staff of an organizing company see every complex of its account, and land on the portfolio
	$orgs = function_exists( 'nadlan_rr_user_orgs' ) ? nadlan_rr_user_orgs( $uid ) : array();
	$org_rooms = array();
	foreach ( $orgs as $o ) { $org_rooms = array_merge( $org_rooms, nadlan_rr_org_rooms( $o ) ); }
	$spaces = array_values( array_unique( array_map( 'intval', array_merge( $org_rooms, $owned, $member ) ) ) );
	if ( ! $spaces && ! $orgs ) { nadlan_ur_render_landing( $landing_lang, true ); exit; }
	nadlan_ur_render_dashboard( $spaces, $lang, $orgs ? (int) $orgs[0] : 0 );
	exit;
} );

/* ---------- shared pieces ---------- */
if ( ! function_exists( 'nadlan_ur_space_app_mount' ) ) {
	/** Prints the app mount + the app script tag. */
	function nadlan_ur_space_app_mount( $mode, $space_id, $lang, $org = 0 ) {
		$glb = esc_url( function_exists( 'nadlan_showroom_engine_base_url' ) ? nadlan_showroom_engine_base_url() . 'models/standard-residential.glb' : '' );
		$token = function_exists( 'nadlan_mapbox_token' ) ? nadlan_mapbox_token() : '';
		$js = esc_url( plugins_url( 'assets/urban/renewal-space.js', dirname( __FILE__ ) ) . '?v=' . rawurlencode( NADLAN_CONFIG_VERSION ) );
		$css = esc_url( plugins_url( 'assets/urban/renewal-room.css', dirname( __FILE__ ) ) . '?v=' . rawurlencode( NADLAN_CONFIG_VERSION ) );
		// the site's own faces (Ben 26.10.2026: "like the site"): Assistant for words and numbers, Noto Serif Hebrew for headings
		$fonts = 'https://fonts.googleapis.com/css2?family=Assistant:wght@400;600;700;800&family=Noto+Serif+Hebrew:wght@600&display=swap';
		?>
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="<?php echo esc_url( $fonts ); ?>">
<link rel="stylesheet" href="<?php echo $css; // phpcs:ignore ?>">
<div id="nlurd-mount" class="nlurd-app" data-loading="1"
	data-mode="<?php echo esc_attr( $mode ); ?>"
	data-space="<?php echo (int) $space_id; ?>"
	data-org="<?php echo (int) $org ? (int) $org : ''; ?>"
	data-today="<?php echo esc_attr( substr( current_time( 'mysql' ), 0, 10 ) ); ?>"
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
		static $done = false;
		if ( $done ) { return; }
		$done = true;
		// NadLan Instruments (26.10.2026): ink #12202A, deep #1F4B5C for the main action, sea #2F6F86, line #D3DCE2, ground
		// #F6F8F9; the site's faces (Assistant, Noto Serif Hebrew for headings). Replaces Frank Ruhl, Heebo, gold, terracotta and cream.
		?>
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Assistant:wght@400;600;700;800&family=Noto+Serif+Hebrew:wght@600&display=swap">
<style>
.nlurd{--ink:#12202A;--ink2:#3E4C58;--mute:#5E6A75;--line:#D3DCE2;--line2:#B9C6CF;--g:#F6F8F9;--sea:#2F6F86;--deep:#1F4B5C;--tint:#E9F1F4;--sans:"Assistant","Segoe UI",Arial,sans-serif;--mono:"Assistant","Segoe UI",Arial,sans-serif;--serif:"Noto Serif Hebrew","David Libre",Georgia,serif;
  max-width:1120px;margin:0 auto;padding:24px 16px 60px;font-family:var(--sans);color:var(--ink2)}
.nlurd--room{max-width:1240px}
.nlurd *{box-sizing:border-box}
html body .nlurd h1,html body .nlurd h2{font-family:var(--serif)!important}
html body .nlurd h3{font-family:var(--sans)!important}
html body .nlurd h1,html body .nlurd h2,html body .nlurd h3{color:var(--ink)!important;font-weight:600!important;letter-spacing:0}
.nlurd-dhead{margin:0 0 14px}
.nlurd-dhead h1{margin:0 0 4px;font-size:clamp(1.5rem,3.2vw,2rem);line-height:1.25}
html body .nlurd a.nlurd-lang{color:var(--deep)!important;font-weight:600;margin-inline-start:8px}
.nlurd-app{min-height:220px}
.nlurd-note{font:400 12.5px/1.6 var(--sans);color:var(--mute)}
.nlurd-spaces{display:flex;gap:8px;flex-wrap:wrap;margin-bottom:14px}
html body .nlurd .nlurd-spaces a{border:1px solid var(--line);border-radius:3px;padding:9px 13px;font:600 13px/1.2 var(--sans);color:var(--ink2)!important;text-decoration:none;background:#fff}
html body .nlurd .nlurd-spaces a.is-on{background:var(--ink);color:#fff!important;border-color:var(--ink)}
/* landing */
.nlurl-hero{text-align:center;padding:34px 0 8px}
.nlurl-kicker{font:600 13px/1.2 var(--sans);color:var(--sea);margin:0 0 10px}
.nlurl-hero h1{font-size:clamp(1.7rem,4vw,2.5rem);margin:0 0 12px;line-height:1.25}
.nlurl-hero .sub{color:var(--ink2);font:400 16px/1.7 var(--sans);max-width:660px;margin:0 auto 20px}
.nlurl-ctas{display:flex;gap:12px;justify-content:center;flex-wrap:wrap}
.nlurl-cta{display:inline-flex;align-items:center;justify-content:center;min-height:48px;border-radius:6px;padding:0 24px;font:600 15px/1.2 var(--sans);text-decoration:none}
html body .nlurd a.nlurl-cta--go{background:var(--deep);border:1px solid var(--deep);color:#fff!important;text-decoration:none!important}
html body .nlurd a.nlurl-cta--go:hover{background:var(--ink);border-color:var(--ink)}
html body .nlurd a.nlurl-cta--alt{background:#fff;border:1px solid var(--ink);color:var(--ink)!important;text-decoration:none!important}
.nlurl-badges{color:var(--mute);font:400 12.5px/1.5 var(--sans);margin:14px 0 0}
.nlurl-badges b{color:var(--ink2)}
.nlurl-lang{text-align:center;margin:6px 0 0}
html body .nlurd .nlurl-lang a,html body .nlurd a.nlurl-guide{color:var(--deep)!important;font:600 14px/1.4 var(--sans)}
.nlurl-steps{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));margin:34px 0;border:1px solid var(--line);border-radius:6px;background:#fff}
.nlurl-step{padding:20px;border-inline-start:1px solid var(--line)}
.nlurl-step:first-child{border-inline-start:0}
@media(max-width:760px){.nlurl-steps{grid-template-columns:minmax(0,1fr)}.nlurl-step{border-inline-start:0;border-top:1px solid var(--line)}.nlurl-step:first-child{border-top:0}}
.nlurl-step i{display:grid;place-items:center;width:32px;height:32px;border:1.5px solid var(--deep);color:var(--deep);font:500 14px/1 var(--mono);font-style:normal;margin-bottom:12px}
.nlurl-step b{display:block;font:600 16px/1.3 var(--sans);color:var(--ink);margin-bottom:6px}
.nlurl-step p{font:400 14px/1.65 var(--sans);color:var(--ink2);margin:0}
.nlurl-demo{background:var(--ink);border-radius:6px;padding:20px 14px 22px;margin:10px 0 34px}
.nlurl-demo-head{display:flex;justify-content:space-between;align-items:center;gap:12px;flex-wrap:wrap;margin-bottom:14px;padding:0 4px}
html body .nlurd .nlurl-demo-head h2{color:#fff!important;margin:0;font-size:1.3rem}
.nlurl-demo-head .lbl{background:var(--tint);color:var(--ink);font:600 12px/1 var(--sans);border-radius:3px;padding:7px 10px}
.nlurl-demo-inner{background:var(--g);border-radius:4px;overflow:hidden}
.nlurl-2col{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:14px;margin:0 0 34px}
@media(max-width:760px){.nlurl-2col{grid-template-columns:minmax(0,1fr)}}
.nlurl-col{border-radius:6px;padding:20px 22px}
.nlurl-col--old{background:var(--g);border:1px solid var(--line)}
.nlurl-col--new{background:#fff;border:1.5px solid var(--deep)}
.nlurl-col h3{margin:0 0 10px;font-size:1.06rem}
.nlurl-col ul{margin:0;padding-inline-start:18px}
.nlurl-col li{font:400 14px/1.8 var(--sans);color:var(--ink2)}
.nlurl-feats{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:0 24px;margin:0 0 34px;border-top:1.5px solid var(--ink)}
@media(max-width:860px){.nlurl-feats{grid-template-columns:repeat(2,minmax(0,1fr))}}
@media(max-width:560px){.nlurl-feats{grid-template-columns:minmax(0,1fr)}}
.nlurl-feat{padding:16px 0;border-bottom:1px solid var(--line)}
.nlurl-feat b{display:block;font:600 15px/1.35 var(--sans);color:var(--ink);margin-bottom:4px}
.nlurl-feat p{font:400 13.5px/1.6 var(--sans);color:var(--mute);margin:0}
.nlurl-faq{margin:0 0 30px}
.nlurl-faq details{background:#fff;border:1px solid var(--line);border-radius:6px;padding:14px 18px;margin-bottom:8px}
.nlurl-faq summary{font:600 15px/1.4 var(--sans);cursor:pointer;color:var(--ink)}
.nlurl-faq p{font:400 14px/1.7 var(--sans);color:var(--ink2);margin:10px 0 0}
.nlurl-secttl{font-size:1.3rem;margin:0 0 14px}
.nlurl-privacy{background:var(--tint);border-inline-start:3px solid var(--deep);border-radius:4px;padding:16px 20px;font:400 13.5px/1.7 var(--sans);color:var(--ink2);margin-bottom:26px}
.nlurd-newform{background:#fff;border:1.5px solid var(--deep);border-radius:6px;padding:22px;margin:22px 0 30px}
.nlurd-newform h2{margin:0 0 12px;font-size:1.2rem}
.nlurd-f{display:grid;grid-template-columns:repeat(auto-fit,minmax(160px,1fr));gap:10px;margin:10px 0}
.nlurd-f label{display:flex;flex-direction:column;gap:5px;font:600 12.5px/1.4 var(--sans);color:var(--ink)}
.nlurd input[type=text],.nlurd input[type=number]{width:100%;border:1px solid var(--line2);border-radius:4px;padding:10px 11px;font:400 15px/1.3 var(--sans);background:#fff;color:var(--ink);min-height:44px}
html body .nlurd button.nlurd-btn{background:var(--deep)!important;color:#fff!important;border:0;border-radius:6px;padding:0 18px;min-height:44px;font:600 14px/1.2 var(--sans);cursor:pointer;margin-top:8px}
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
			: 'חדר פרויקט התחדשות עירונית לדיירים: הסכמה לכל דירה, שלבים ומסמכים | נדלן';
		$desc = $en
			? 'A free project room for buildings in pinui-binui and TAMA 38: track the consent of every apartment on the building face, check the majority the law requires, follow the 10 stages, track documents and updates in one private place. In Hebrew, English and Russian.'
			: 'חדר פרויקט חינמי לבניין בפינוי בינוי או תמ"א 38: מעקב הסכמה לכל דירה על חזית הבניין, הרוב לפי החוק, סרגל 10 השלבים, מסמכים ועדכונים במקום אחד פרטי. בעברית ובאנגלית.';
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
			'sub'    => 'One private place where the whole building sees the same truth: every apartment\'s consent marked on the face of the building, the 10 stages of the process, the documents and the updates. Free for residents and committees.',
			'cta_go' => $logged_in ? 'Open a room for your building' : 'Open a room for your building',
			'cta_alt' => 'Free compound check',
			'badges' => 'Free for residents and committees · Hebrew and English · Private, never shown in search',
			'steps_t' => 'Start here',
			'steps' => array(
				array( 'Check your building', 'Run the free wizard: address, floors, consent count. You get a first reading of the likely track and your next steps.' ),
				array( 'Open the project room', 'One click lays out the face of your building with every apartment on it. Mark who signed, who is in process, who is missing papers.' ),
				array( 'Invite the neighbors', 'Share one link in the building WhatsApp group. Everyone sees the same progress bar, the same documents, the same updates, and no more rumor management.' ),
			),
			'demo_t' => 'A live example: a project that reached the finish line',
			'demo_lbl' => 'Sample room · sample data',
			'old_t' => 'Today, without a project room',
			'old' => array( 'Consent counts living in one neighbor\'s Excel', 'Paper signatures nobody can audit', 'The same questions again and again in the WhatsApp group', 'Documents scattered across email inboxes' ),
			'new_t' => 'With the project room',
			'new' => array( 'Every apartment\'s status on the building face, one source of truth', 'A progress bar the whole building shares', 'A documents rollup that shows exactly what is missing', 'One updates feed, one invite link' ),
			'feats_t' => 'What is inside',
			'feats' => array(
				array( 'Consent on the building face', 'Every apartment is a cell on the building face, marked by status.' ),
				array( '10-stage progress bar', 'From first assembly to keys, with the next actions for every stage.' ),
				array( 'Auto to-do list', 'Derived live from your data: thresholds reached, documents missing, next moves.' ),
				array( 'Documents per apartment', 'ID, Tabu extract, signed agreement, power of attorney, tracked per apartment.' ),
				array( 'Updates feed', 'The committee posts once; every neighbor sees it.' ),
				array( 'First building check', 'The free check reads your building details and suggests the likely track, with every disclaimer it deserves.' ),
				array( 'The majority under the law', 'Two thirds in the complex, three fifths in each building and half of the common property: the room checks each condition against the data.' ),
				array( 'Committee report', 'A clean status report to print or save as PDF: per building, per condition, per document.' ),
				array( 'Privacy for every neighbor', 'A neighbor sees the overall picture and their own apartment only. Names and notes stay with the managers.' ),
			),
			'faq_t' => 'Questions owners ask',
			'faq' => array(
				array( 'Is it really free?', 'Yes. The project room is free for residents and committees. Nadlan makes its money from the professionals marketplace, not from homeowners.' ),
				array( 'Who can see our building\'s room?', 'Only people you invite with the link. Rooms are private and never listed in search engines. In the room you mark which documents each apartment has; the files themselves are not stored in the room.' ),
				array( 'We have neighbors who do not read Hebrew.', 'The whole room works in English and Russian too: switch with one link. Made for olim and owners abroad.' ),
				array( 'Is the first building check legal advice?', 'No. It is a first orientation only. Before signing anything, consult a lawyer who represents the residents: by law the developer pays for one you choose.' ),
			),
			'privacy' => 'Privacy: rooms are private, blocked from search engines and open only to the people you invite. In the room you mark which documents each apartment has; the files themselves are not stored in it. Nothing about your building appears in search.',
			'guide' => 'New to urban renewal? Read the full Hebrew guide',
			'lang_link' => '<a href="' . esc_url( $he_url ) . '">עברית</a>',
			'create_t' => 'Open the room for your building',
		) : array(
			'kicker' => 'התחדשות עירונית, מסודרת',
			'h1'     => 'חדר הפרויקט של הבניין שלכם',
			'sub'    => 'מקום פרטי אחד שבו כל הבניין רואה את אותה תמונה: ההסכמה של כל דירה מסומנת על חזית הבניין, עשרת שלבי התהליך, המסמכים והעדכונים. חינם לדיירים ולנציגות.',
			'cta_go' => 'פתיחת חדר לבניין שלכם',
			'cta_alt' => 'בדיקת מתחם חינם',
			'badges' => 'חינם לדיירים ולנציגות · עברית ואנגלית · פרטי ולא מופיע בחיפוש',
			'steps_t' => 'מתחילים כאן',
			'steps' => array(
				array( 'בודקים את הבניין', 'מריצים את האשף החינמי: כתובת, קומות, מצב הסכמות. מקבלים ניתוח ראשוני של המסלול המסתמן והצעדים הבאים.' ),
				array( 'פותחים חדר פרויקט', 'בלחיצה אחת נפרשת חזית הבניין עם כל הדירות עליה. מסמנים מי חתם, מי בתהליך, למי חסרים מסמכים.' ),
				array( 'מזמינים את השכנים', 'משתפים קישור אחד בקבוצת הוואטסאפ של הבניין. כולם רואים את אותו סרגל התקדמות, אותם מסמכים, אותם עדכונים, בלי ניהול שמועות.' ),
			),
			'demo_t' => 'דוגמה חיה: פרויקט שהגיע עד הסוף',
			'demo_lbl' => 'חדר לדוגמה · נתוני דוגמה',
			'old_t' => 'היום, בלי חדר פרויקט',
			'old' => array( 'ספירת ההסכמות חיה באקסל של שכן אחד', 'חתימות על נייר שאי אפשר לעקוב אחריהן', 'אותן שאלות שוב ושוב בקבוצת הוואטסאפ', 'מסמכים מפוזרים בין תיבות מייל' ),
			'new_t' => 'עם חדר הפרויקט',
			'new' => array( 'הסטטוס של כל דירה על חזית הבניין, מקור אמת אחד', 'סרגל התקדמות שכל הבניין רואה', 'תמונת מסמכים שמראה בדיוק מה חסר', 'ערוץ עדכונים אחד, קישור הזמנה אחד' ),
			'feats_t' => 'מה יש בפנים',
			'feats' => array(
				array( 'ההסכמות על חזית הבניין', 'כל דירה היא משבצת על חזית הבניין, לפי הסטטוס שלה.' ),
				array( 'סרגל 10 השלבים', 'מהאסיפה הראשונה עד המפתח, עם הצעדים הבאים לכל שלב.' ),
				array( 'רשימת משימות אוטומטית', 'נגזרת חיה מהנתונים שלכם: רפים שהושגו, מסמכים חסרים, המהלכים הבאים.' ),
				array( 'מסמכים לכל דירה', 'תעודת זהות, נסח טאבו, הסכם חתום וייפוי כוח, במעקב לכל דירה.' ),
				array( 'ערוץ עדכונים', 'הנציגות מפרסמת פעם אחת; כל שכן רואה.' ),
				array( 'בדיקת בניין ראשונה', 'הבדיקה החינמית קוראת את נתוני הבניין ומציעה את המסלול המסתמן, עם כל ההסתייגויות שמגיעות לה.' ),
				array( 'הרוב לפי החוק', 'שני שלישים במתחם, שלוש חמישיות בכל בניין ומחצית הרכוש המשותף: החדר בודק כל תנאי מול הנתונים.' ),
				array( 'דוח לנציגות', 'דוח מצב מסודר להדפסה או לשמירה כ־PDF: לכל בניין, לכל תנאי ולכל מסמך.' ),
				array( 'פרטיות לכל שכן', 'שכן רואה את התמונה הכללית ואת הדירה שלו בלבד. שמות והערות נשארים אצל המנהלים.' ),
			),
			'faq_t' => 'שאלות שבעלי דירות שואלים',
			'faq' => array(
				array( 'זה באמת חינם?', 'כן. חדר הפרויקט חינמי לדיירים ולנציגות. נדלן מרוויחה ממאגר אנשי המקצוע, לא מבעלי הדירות.' ),
				array( 'מי יכול לראות את החדר של הבניין שלנו?', 'רק מי שהזמנתם עם הקישור. החדרים פרטיים ולא מופיעים במנועי חיפוש. בחדר מסמנים אילו מסמכים יש לכל דירה; הקבצים עצמם לא נשמרים בחדר.' ),
				array( 'יש לנו שכנים שלא קוראים עברית.', 'כל החדר עובד גם באנגלית וברוסית: מחליפים בקישור אחד. מתאים לעולים ולבעלי דירות מחו"ל.' ),
				array( 'הבדיקה הראשונה היא ייעוץ משפטי?', 'לא. זו התמצאות ראשונית בלבד. לפני כל חתימה מתייעצים עם עורך דין מטעם הדיירים: על פי חוק היזם משלם על עורך דין שאתם בוחרים.' ),
			),
			'privacy' => 'פרטיות: החדרים פרטיים, חסומים למנועי חיפוש ופתוחים רק למי שהוזמן. בחדר מסמנים אילו מסמכים יש לכל דירה; הקבצים עצמם לא נשמרים בו. שום דבר על הבניין שלכם לא מופיע בחיפוש.',
			'guide' => 'חדשים בהתחדשות עירונית? התחילו מהמדריך המלא',
			'lang_link' => '<a href="' . esc_url( $en_url ) . '">English</a>',
			'create_t' => 'פתיחת החדר לבניין שלכם',
		);

		$cta_go_href = $logged_in ? '#nlurd-new' : wp_login_url( $self );
		$wizard = home_url( '/urban-renewal/check/' . ( $en ? '?lang=en' : '' ) );
		nadlan_ur_page_header(); // HAD-408: the site's real header, one h1
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
	<p style="text-align:center"><a href="<?php echo esc_url( home_url( $en ? '/urban-renewal/english-guide/' : '/urban-renewal/' ) ); ?>" class="nlurl-guide"><?php echo esc_html( $C['guide'] ); ?></a></p>
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
		nadlan_ur_page_footer();
	}
}

/* ---------- the member dashboard ---------- */
if ( ! function_exists( 'nadlan_ur_render_dashboard' ) ) {
	function nadlan_ur_render_dashboard( $spaces, $lang = 'he', $org = 0 ) {
		$he = ( 'he' === $lang );
		$sel = isset( $_GET['space'] ) ? (int) $_GET['space'] : 0; // phpcs:ignore WordPress.Security.NonceVerification
		if ( $sel && ( ! nadlan_ur_space_ok( $sel ) || ! nadlan_ur_can_view( $sel ) ) ) { $sel = 0; }
		if ( ! $sel && $spaces && ! $org ) { $sel = (int) $spaces[0]; } // Pro: an organizer lands on the portfolio unless ?space= is given
		$titles = array( 'he' => 'חדר ההתחדשות שלי', 'en' => 'My renewal room', 'ru' => 'Моя комната обновления' );
		$notes  = array(
			'he' => 'ניהול פנימי לבניין: הסכמות לכל דירה, שלבים, מסמכים ועדכונים. העמוד פרטי לחברי הבניין בלבד ואינו מופיע בחיפוש.',
			'en' => 'Internal building management: consent for every apartment, stages, documents and updates. Private to building members, never shown in search.',
			'ru' => 'Внутреннее управление домом: согласие каждой квартиры, этапы, документы и обновления. Страница приватная, только для жильцов дома, не отображается в поиске.',
		);
		if ( $org ) {
			$titles = array( 'he' => 'חדר הניהול של החברה', 'en' => 'The company management room', 'ru' => 'Комната управления компании' );
			$notes  = array(
				'he' => 'כל המתחמים שהחברה מלווה: הסכמות לכל דירה, הרוב לפי החוק, שלבים, מועדים, עדכונים לדיירים ודוח לנציגות. העמוד פרטי ואינו מופיע בחיפוש.',
				'en' => 'Every complex the company runs: consent per apartment, the legal majority, stages, deadlines, updates for residents and a committee report. Private, never shown in search.',
				'ru' => 'Все комплексы компании: согласие каждой квартиры, большинство по закону, этапы, сроки, обновления для жильцов и отчёт для комитета. Страница приватная, не отображается в поиске.',
			);
		}
		$lang_names = array( 'he' => 'עברית', 'en' => 'English', 'ru' => 'Русский' );
		nocache_headers();
		header( 'X-Robots-Tag: noindex, nofollow' );
		nadlan_ur_page_header(); // HAD-408
		nadlan_ur_space_css();
		?>
<div class="nlurd nlurd--room" dir="<?php echo $he ? 'rtl' : 'ltr'; ?>" lang="<?php echo esc_attr( $lang ); ?>">
	<header class="nlurd-dhead">
		<h1><?php echo esc_html( $titles[ $lang ] ); ?></h1>
		<p class="nlurd-note"><?php echo esc_html( $notes[ $lang ] ); ?>
			<?php foreach ( $lang_names as $lc => $ln ) : if ( $lc === $lang ) { continue; } ?>
			<a class="nlurd-lang" href="<?php echo esc_url( home_url( '/my-renewal/' . ( $sel || 'he' !== $lc ? '?' : '' ) . ( $sel ? 'space=' . (int) $sel : '' ) . ( 'he' === $lc ? '' : ( $sel ? '&' : '' ) . 'lang=' . $lc ) ) ); ?>"><?php echo esc_html( $ln ); ?></a>
			<?php endforeach; ?>
		</p>
	</header>
	<?php if ( ! $org && count( $spaces ) > 1 ) : ?>
	<nav class="nlurd-spaces">
		<?php foreach ( $spaces as $sid ) : ?>
		<a href="<?php echo esc_url( home_url( '/my-renewal/?space=' . (int) $sid . ( $he ? '' : '&lang=' . $lang ) ) ); ?>" class="<?php echo $sid === $sel ? 'is-on' : ''; ?>"><?php echo esc_html( get_the_title( $sid ) ); ?></a>
		<?php endforeach; ?>
	</nav>
	<?php endif; ?>
	<?php nadlan_ur_space_app_mount( $org ? 'org' : 'live', $sel, $lang, $org ); ?>
</div>
		<?php
		nadlan_ur_page_footer();
	}
}

/* healthcheck visibility */
add_filter( 'nadlan_config_healthcheck', function ( $out ) {
	if ( isset( $out['urban_renewal'] ) && is_array( $out['urban_renewal'] ) ) {
		$out['urban_renewal']['space'] = nadlan_ur_space_on();
	}
	return $out;
} );

/* RenewalRoomPro: roles, the role-filtered payload, one-apartment save, change log, the law, deadlines (renewal-room.php),
   which loads the organizer account, portfolio and billing (renewal-org.php). */
if ( file_exists( __DIR__ . '/renewal-room.php' ) ) { require_once __DIR__ . '/renewal-room.php'; }
