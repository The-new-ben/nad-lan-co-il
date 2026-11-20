<?php
/**
 * nadlan-config - rentals in five languages + "we will rent it out meanwhile" (HAD-795, package 6, 19.11.2026).
 *
 * 1. /my-rentals/ for visitors in he, en, fr, ru, ar (?lang=xx): the statistician's-ledger design (board
 *    https://claude.ai/artifact/E2zn8Z1Vw7qKwbuJG2nVRg), the right <html lang> (the 3D hint followed the theme's he-IL),
 *    a readable main button (it was teal text on terracotta), the 3D box on blueprint paper instead of black.
 *    Logged-in landlords keep the existing app untouched (inc/rentals-manager.php).
 * 2. The live demo speaks the page language: the demo portfolio is stored in Hebrew, so the /rental-demo response is
 *    translated on the way out (addresses, apartment names, example tenants, repairs, statuses, document names).
 * 3. The earnings estimate (assets/rentals/earn/): range from the CBS Table 4.9 (Price Statistics Monthly 10/2026,
 *    quarter VII-IX 2026, average +- 2 sampling errors), the visitor's own numbers, the 2026 rent tax routes, then
 *    "manage it yourself, free" or a request for management options (POST /nadlan/v1/lead, source rent_earn).
 * 4. Project pages: an inline opener under the 3D stage (#nlps), never floating; the apartment picked on the stage
 *    (event nl:facing) is carried into the sheet. Not on Ashira (owner order 19.10: the Ashira page is not changed).
 * No invented numbers; unknown = omitted. The site never presents itself as a broker. No long dashes.
 */

if ( ! defined( 'ABSPATH' ) ) { exit; }

if ( ! function_exists( 'nadlan_re_lang' ) ) {
	function nadlan_re_lang( $raw = null ) {
		if ( null === $raw ) { $raw = isset( $_GET['lang'] ) ? sanitize_key( wp_unslash( $_GET['lang'] ) ) : ''; } // phpcs:ignore WordPress.Security.NonceVerification
		return in_array( $raw, array( 'en', 'fr', 'ru', 'ar' ), true ) ? $raw : 'he';
	}
}
if ( ! function_exists( 'nadlan_re_url' ) ) {
	function nadlan_re_url( $lang ) { return home_url( '/my-rentals/' . ( 'he' === $lang ? '' : '?lang=' . $lang ) ); }
}
if ( ! function_exists( 'nadlan_re_ver' ) ) {
	function nadlan_re_ver() { return rawurlencode( defined( 'NADLAN_CONFIG_VERSION' ) ? NADLAN_CONFIG_VERSION : '1' ); }
}
if ( ! function_exists( 'nadlan_re_asset' ) ) {
	function nadlan_re_asset( $f ) { return plugins_url( 'assets/rentals/earn/' . $f, dirname( __FILE__ ) ) . '?v=' . nadlan_re_ver(); }
}

/* a project's city (meta 'city', Hebrew or English) -> a key of the CBS file; cities under 100,000 residents -> their district */
if ( ! function_exists( 'nadlan_re_city_key' ) ) {
	function nadlan_re_city_key( $city ) {
		$c = trim( preg_replace( '/[\s\-־]+/u', ' ', (string) $city ) );
		if ( '' === $c ) { return array( '', false ); }
		$big = array(
			'tel-aviv' => array( 'תל אביב', 'תל אביב יפו', 'תל-אביב', 'tel aviv', 'tel aviv yafo', 'tel aviv jaffa' ),
			'jerusalem' => array( 'ירושלים', 'jerusalem' ), 'haifa' => array( 'חיפה', 'haifa' ),
			'ramat-gan' => array( 'רמת גן', 'ramat gan' ), 'herzliya' => array( 'הרצליה', 'herzliya' ),
			'holon' => array( 'חולון', 'holon' ), 'bat-yam' => array( 'בת ים', 'bat yam' ), 'bnei-brak' => array( 'בני ברק', 'bnei brak' ),
			'petah-tikva' => array( 'פתח תקווה', 'פתח תקוה', 'petah tikva', 'petach tikva' ), 'rishon-lezion' => array( 'ראשון לציון', 'rishon lezion', 'rishon le zion' ),
			'rehovot' => array( 'רחובות', 'rehovot' ), 'netanya' => array( 'נתניה', 'netanya' ), 'kfar-saba' => array( 'כפר סבא', 'kfar saba' ),
			'ashdod' => array( 'אשדוד', 'ashdod' ), 'ashkelon' => array( 'אשקלון', 'ashkelon' ), 'beer-sheva' => array( 'באר שבע', 'beer sheva', "be'er sheva" ),
			'bet-shemesh' => array( 'בית שמש', 'beit shemesh', 'bet shemesh' ), 'hadera' => array( 'חדרה', 'hadera' ),
		);
		$district = array(
			'd-telaviv' => array( 'גבעתיים', 'קרית אונו', 'קריית אונו', 'אור יהודה', 'רמת השרון', 'אזור', 'givatayim', 'kiryat ono', 'ramat hasharon', 'or yehuda' ),
			'd-center' => array( 'רעננה', 'הוד השרון', 'מודיעין', 'מודיעין מכבים רעות', 'ראש העין', 'יבנה', 'נס ציונה', 'לוד', 'רמלה', 'יהוד', 'שוהם', 'אלעד', 'גני תקווה', 'כפר יונה', 'אבן יהודה', 'raanana', "ra'anana", 'hod hasharon', 'modiin', "modi'in", 'rosh haayin', 'yavne', 'ness ziona', 'lod', 'ramla', 'yehud', 'shoham' ),
			'd-haifa' => array( 'קרית ים', 'קריית ים', 'קרית ביאליק', 'קריית ביאליק', 'קרית מוצקין', 'קריית מוצקין', 'קרית אתא', 'קריית אתא', 'נשר', 'טירת כרמל', 'זכרון יעקב', 'פרדס חנה כרכור', 'אור עקיבא', 'קיסריה', 'nesher', 'caesarea' ),
			'd-north' => array( 'נהריה', 'עכו', 'כרמיאל', 'טבריה', 'עפולה', 'נצרת', 'נוף הגליל', 'צפת', 'קרית שמונה', 'יקנעם', 'יקנעם עילית', 'nahariya', 'akko', 'acre', 'karmiel', 'tiberias', 'afula', 'nazareth', 'safed', 'yokneam' ),
			'd-south' => array( 'אילת', 'קרית גת', 'קריית גת', 'דימונה', 'נתיבות', 'שדרות', 'אופקים', 'ערד', 'קרית מלאכי', 'eilat', 'kiryat gat', 'dimona', 'netivot', 'sderot', 'ofakim', 'arad' ),
			'd-jerusalem' => array( 'מבשרת ציון', 'מבשרת', 'mevaseret zion' ),
		);
		$lc = function_exists( 'mb_strtolower' ) ? mb_strtolower( $c, 'UTF-8' ) : strtolower( $c );
		foreach ( $big as $k => $names ) { foreach ( $names as $n ) { if ( $lc === $n || 0 === strpos( $lc, $n . ' ' ) ) { return array( $k, false ); } } }
		foreach ( $district as $k => $names ) { foreach ( $names as $n ) { if ( $lc === $n ) { return array( $k, true ); } } }
		return array( 'israel', true );
	}
}

/* ---------- the demo speaks the page language ---------- */
if ( ! function_exists( 'nadlan_re_demo_words' ) ) {
	function nadlan_re_demo_words( $lang ) {
		$w = array(
			'en' => array( 'ארלוזורוב 78' => '78 Arlozorov St', "ז'בוטינסקי 12" => '12 Jabotinsky St', 'תל אביב-יפו' => 'Tel Aviv-Yafo', 'תל אביב' => 'Tel Aviv', 'רמת גן' => 'Ramat Gan',
				'משפחת לוי (דוגמה)' => 'The Levi family (example)', 'ד. כהן (דוגמה)' => 'D. Cohen (example)', 'ר. מזרחי (דוגמה)' => 'R. Mizrahi (example)',
				'תוקן דוד שמש (דוגמה)' => 'Solar water heater fixed (example)', 'טפטוף בברז המטבח (דוגמה)' => 'Dripping kitchen tap (example)', 'צביעה לפני שוכר חדש (דוגמה)' => 'Repainting before a new tenant (example)',
				'פנויה - נתוני דוגמה' => 'Vacant, sample data', 'נתוני דוגמה' => 'Sample data', 'דוגמה' => 'Example', 'דירה' => 'Apartment' ),
			'fr' => array( 'ארלוזורוב 78' => '78 rue Arlozorov', "ז'בוטינסקי 12" => '12 rue Jabotinsky', 'תל אביב-יפו' => 'Tel Aviv-Jaffa', 'תל אביב' => 'Tel Aviv', 'רמת גן' => 'Ramat Gan',
				'משפחת לוי (דוגמה)' => 'Famille Levi (exemple)', 'ד. כהן (דוגמה)' => 'D. Cohen (exemple)', 'ר. מזרחי (דוגמה)' => 'R. Mizrahi (exemple)',
				'תוקן דוד שמש (דוגמה)' => 'Chauffe-eau solaire réparé (exemple)', 'טפטוף בברז המטבח (דוגמה)' => 'Robinet de cuisine qui goutte (exemple)', 'צביעה לפני שוכר חדש (דוגמה)' => 'Peinture avant un nouveau locataire (exemple)',
				'פנויה - נתוני דוגמה' => 'Vacant, données d’exemple', 'נתוני דוגמה' => 'Données d’exemple', 'דוגמה' => 'Exemple', 'דירה' => 'Appartement' ),
			'ru' => array( 'ארלוזורוב 78' => 'ул. Арлозоров, 78', "ז'בוטינסקי 12" => 'ул. Жаботинского, 12', 'תל אביב-יפו' => 'Тель-Авив-Яффо', 'תל אביב' => 'Тель-Авив', 'רמת גן' => 'Рамат-Ган',
				'משפחת לוי (דוגמה)' => 'Семья Леви (пример)', 'ד. כהן (דוגמה)' => 'Д. Коэн (пример)', 'ר. מזרחי (דוגמה)' => 'Р. Мизрахи (пример)',
				'תוקן דוד שמש (דוגמה)' => 'Отремонтирован солнечный бойлер (пример)', 'טפטוף בברז המטבח (דוגמה)' => 'Течёт кран на кухне (пример)', 'צביעה לפני שוכר חדש (דוגמה)' => 'Покраска перед новым жильцом (пример)',
				'פנויה - נתוני דוגמה' => 'Свободна, пример', 'נתוני דוגמה' => 'Пример данных', 'דוגמה' => 'Пример', 'דירה' => 'Квартира' ),
			'ar' => array( 'ארלוזורוב 78' => '78 شارع أرلوزوروف', "ז'בוטינסקי 12" => '12 شارع جابوتنسكي', 'תל אביב-יפו' => 'تل أبيب - يافا', 'תל אביב' => 'تل أبيب', 'רמת גן' => 'رمات غان',
				'משפחת לוי (דוגמה)' => 'عائلة ليفي (مثال)', 'ד. כהן (דוגמה)' => 'د. كوهين (مثال)', 'ר. מזרחי (דוגמה)' => 'ر. مزراحي (مثال)',
				'תוקן דוד שמש (דוגמה)' => 'تم إصلاح السخان الشمسي (مثال)', 'טפטוף בברז המטבח (דוגמה)' => 'تسريب في حنفية المطبخ (مثال)', 'צביעה לפני שוכר חדש (דוגמה)' => 'دهان قبل مستأجر جديد (مثال)',
				'פנויה - נתוני דוגמה' => 'شاغرة، بيانات مثال', 'נתוני דוגמה' => 'بيانات مثال', 'דוגמה' => 'مثال', 'דירה' => 'شقة' ),
		);
		return isset( $w[ $lang ] ) ? $w[ $lang ] : array();
	}
}
if ( ! function_exists( 'nadlan_re_tr' ) ) {
	function nadlan_re_tr( $s, $lang ) {
		$s = (string) $s; $w = nadlan_re_demo_words( $lang );
		if ( '' === $s || ! $w ) { return $s; }
		if ( isset( $w[ $s ] ) ) { return $w[ $s ]; }
		if ( preg_match( '/^דירה (\d+)$/u', $s, $m ) ) { return $w['דירה'] . ' ' . $m[1]; }
		if ( preg_match( '/^דוגמה: (.+), (.+)$/u', $s, $m ) ) { return $w['דוגמה'] . ': ' . nadlan_re_tr( $m[1], $lang ) . ', ' . nadlan_re_tr( $m[2], $lang ); }
		return $s;
	}
}
if ( ! function_exists( 'nadlan_re_statuses' ) ) {
	function nadlan_re_statuses( $lang ) {
		$c = array( 'ok' => '#1B7F6B', 'due' => '#1F4FD1', 'late' => '#C62828', 'vacant' => '#7C8B95', 'unowned' => '#C9D2D6' );
		$l = array(
			'he' => array( 'ok' => 'שולם', 'due' => 'החודש טרם סומן', 'late' => 'בפיגור', 'vacant' => 'פנויה', 'unowned' => 'לא שלי' ),
			'en' => array( 'ok' => 'Paid', 'due' => 'Month not marked yet', 'late' => 'Overdue', 'vacant' => 'Vacant', 'unowned' => 'Not mine' ),
			'fr' => array( 'ok' => 'Payé', 'due' => 'Mois pas encore marqué', 'late' => 'En retard', 'vacant' => 'Vacant', 'unowned' => 'Pas à moi' ),
			'ru' => array( 'ok' => 'Оплачено', 'due' => 'Месяц ещё не отмечен', 'late' => 'Просрочено', 'vacant' => 'Свободна', 'unowned' => 'Не моя' ),
			'ar' => array( 'ok' => 'مدفوع', 'due' => 'الشهر لم يُسجَّل بعد', 'late' => 'متأخر', 'vacant' => 'شاغرة', 'unowned' => 'ليست لي' ),
		);
		$out = array(); foreach ( $c as $k => $col ) { $out[ $k ] = array( $l[ $lang ][ $k ], $col ); }
		return $out;
	}
}
if ( ! function_exists( 'nadlan_re_doc_keys' ) ) {
	function nadlan_re_doc_keys( $lang ) {
		$d = array(
			'fr' => array( 'contract' => 'Bail signé', 'nesach' => 'Extrait du cadastre (Tabou)', 'protocol' => 'État des lieux + photos', 'securities' => 'Garanties (chèque de garantie / billet à ordre / garants)', 'insurance' => 'Assurance de l’immeuble' ),
			'ru' => array( 'contract' => 'Подписанный договор', 'nesach' => 'Выписка из реестра (Табу)', 'protocol' => 'Акт передачи + фото', 'securities' => 'Гарантии (чек / вексель / поручители)', 'insurance' => 'Страховка здания' ),
			'ar' => array( 'contract' => 'عقد إيجار موقّع', 'nesach' => 'مستخرج تسجيل الأراضي (طابو)', 'protocol' => 'محضر التسليم + صور', 'securities' => 'ضمانات (شيك ضمان / سند دين / كفلاء)', 'insurance' => 'تأمين المبنى' ),
		);
		if ( isset( $d[ $lang ] ) ) { return $d[ $lang ]; }
		return function_exists( 'nadlan_rm_doc_keys_lang' ) ? nadlan_rm_doc_keys_lang( $lang ) : array();
	}
}
add_filter( 'rest_post_dispatch', function ( $res, $server, $req ) {
	if ( ! ( $req instanceof WP_REST_Request ) || '/nadlan/v1/rental-demo' !== $req->get_route() || ! ( $res instanceof WP_REST_Response ) ) { return $res; }
	$lang = nadlan_re_lang( (string) $req->get_param( 'lang' ) );
	$data = $res->get_data();
	if ( ! is_array( $data ) || empty( $data['props'] ) || ! is_array( $data['props'] ) ) { return $res; }
	foreach ( $data['props'] as &$p ) {
		if ( empty( $p['is_demo'] ) ) { continue; }
		$p['statuses'] = nadlan_re_statuses( $lang );
		if ( 'he' !== $lang ) {
			foreach ( array( 'title', 'address', 'city' ) as $k ) { if ( isset( $p[ $k ] ) ) { $p[ $k ] = nadlan_re_tr( $p[ $k ], $lang ); } }
			$p['doc_keys'] = nadlan_re_doc_keys( $lang );
			if ( ! empty( $p['units'] ) && is_array( $p['units'] ) ) {
				foreach ( $p['units'] as &$u ) {
					foreach ( array( 'label', 'tenant_name', 'note' ) as $k ) { if ( isset( $u[ $k ] ) ) { $u[ $k ] = nadlan_re_tr( $u[ $k ], $lang ); } }
					if ( ! empty( $u['maintenance'] ) && is_array( $u['maintenance'] ) ) { foreach ( $u['maintenance'] as &$m ) { if ( isset( $m['text'] ) ) { $m['text'] = nadlan_re_tr( $m['text'], $lang ); } } unset( $m ); }
				}
				unset( $u );
			}
		}
	}
	unset( $p );
	$res->set_data( $data );
	return $res;
}, 10, 3 );

/* ---------- the demo app's interface strings in fr, ru, ar (he and en stay in nadlan_rm_strings) ---------- */
if ( ! function_exists( 'nadlan_re_app_strings' ) ) {
	function nadlan_re_app_strings( $lang ) {
		if ( in_array( $lang, array( 'he', 'en' ), true ) ) {
			$s = function_exists( 'nadlan_rm_strings' ) ? nadlan_rm_strings( $lang ) : array();
			$s['days_sfx'] = 'en' === $lang ? 'd' : ' ימים';
			return $s;
		}
		$S = array(
			'fr' => array(
				'load_fail' => 'Impossible de charger vos biens.', 'none_yet' => 'Aucun bien pour l’instant : ajoutez le premier ci-dessous.', 'units' => 'appartements', 'sel_title' => 'Appartement choisi',
				'sel_hint_mgr' => 'Touchez un appartement sur la maquette. Un appartement en pointillés n’est pas encore marqué comme le vôtre : touchez-le pour l’ajouter.',
				'sel_hint_ro' => 'Touchez un appartement coloré sur la maquette pour voir sa gestion locative.',
				'portfolio' => 'Vue du portefeuille', 'buildings' => 'immeubles', 'monthly_rent' => 'Loyer mensuel', 'late_n' => 'en retard', 'due_n' => 'pas encore marqués ce mois', 'vacant_n' => 'vacants',
				'next_actions' => 'Mes prochaines actions', 'no_actions' => 'Rien d’urgent. Tout est en ordre.', 'derived_note' => 'Calculé automatiquement à partir de vos données. Des rappels, pas un conseil juridique ou fiscal.',
				'health' => array( 'contract' => 'Bail', 'rent' => 'Loyer', 'security' => 'Garanties', 'repairs' => 'Réparations', 'tax' => 'Impôt', 'renewal' => 'Renouvellement' ),
				'label' => 'Nom de l’appartement', 'tenant' => 'Locataire', 'phone' => 'Téléphone du locataire', 'rent' => 'Loyer mensuel (₪)', 'start' => 'Début du bail', 'end' => 'Fin du bail', 'opt' => 'Option jusqu’au',
				'linkage' => 'Indexation', 'link_none' => 'Aucune', 'link_madad' => 'Indexé sur l’IPC', 'ledger' => 'Suivi des loyers (12 mois)', 'docs' => 'Dossier de documents', 'maint' => 'Entretien', 'maint_new' => 'Nouvel incident', 'add' => 'Ajouter',
				'urgent' => 'Urgent (logement impossible)', 'standard' => 'Normal', 'fix_by' => 'Délai légal maximal', 'overdue_fix' => 'Délai légal dépassé', 'mark_done' => 'Traité', 'reopen' => 'Rouvrir', 'notes' => 'Notes',
				'save' => 'Enregistrer', 'saving' => 'Enregistrement...', 'saved' => 'Enregistré', 'save_fail' => 'Échec, réessayez',
				'wa_btn' => 'Rappel WhatsApp', 'wa_text' => 'Bonjour {name}, petit rappel pour le loyer de {month}. Merci !', 'pro_btn' => 'Trouver un professionnel', 'list_btn' => 'Publier l’appartement', 'studio_btn' => 'Aménager l’appartement (Studio)',
				'sec_title' => 'Garanties', 'sec_check' => 'Chèque de garantie', 'sec_shtar' => 'Billet à ordre', 'sec_arev' => 'Garants', 'sec_bank' => 'Garantie bancaire / dépôt',
				'sec_amount' => 'Montant du dépôt / de la garantie (₪)', 'sec_cap' => 'Plafond légal des garanties coûteuses', 'sec_cap_f' => 'le plus bas entre 3 mois de loyer et un tiers du loyer total du bail', 'sec_over' => 'Au-dessus du plafond légal : vérifiez avec un avocat',
				'cpi_title' => 'Calcul de l’indexation', 'cpi_base' => 'Indice de base (du bail)', 'cpi_cur' => 'Indice actuel (CBS)', 'cpi_pct' => 'Part indexée', 'cpi_floor' => 'Plancher au loyer de base (selon le bail)',
				'cpi_res' => 'Loyer indexé', 'cpi_note' => 'Saisissez les indices du Bureau central des statistiques. Formule : loyer x (actuel / base). Aide au calcul ; le texte du bail prévaut.',
				'tax_title' => 'Estimation de l’impôt sur les loyers ({year})', 'tax_total' => 'Total des loyers résidentiels mensuels (TOUS vos appartements, y compris ceux gérés ailleurs)',
				'tax_exempt' => 'Exonéré', 'tax_taxable' => 'Imposable (régime ordinaire)', 'tax_ten' => 'Régime 10 % (annuel)', 'tax_paid_rent' => 'Loyer que vous payez pour votre logement (annuel, si vous louez)',
				'tax_deadline' => 'Régime 10 % : déclaration et paiement après la fin de l’année fiscale. Vérifiez la dernière date exacte sur le site de l’Autorité fiscale.', 'tax_note' => 'Estimations, avec un plafond d’exonération de {ceiling} ₪ par mois (selon le guide de l’Autorité fiscale, c’est le plafond de 2025). Vérifiez le plafond en vigueur sur le site de l’Autorité fiscale. Vérifiez auprès de l’Autorité fiscale ou d’un comptable avant d’agir.',
				'notice_l' => 'Préavis du bailleur : {d} jours avant la fin', 'notice_t' => 'Préavis du locataire : {d} jours',
				'act_late' => '{label}, {city} : loyer en retard', 'act_due' => '{label} : mois pas encore marqué', 'act_end' => '{label} : le bail se termine dans {d} jours', 'act_ended' => '{label} : bail TERMINÉ, renouveler ou clore',
				'act_opt' => '{label} : la fenêtre d’option se ferme dans {d} jours', 'act_repair' => '{label} : réparation urgente, délai légal {d} jours', 'act_repair_std' => '{label} : incident ouvert proche du délai de 30 jours',
				'act_docs' => '{label} : dossier incomplet', 'act_tax' => 'Régime 10 % : après la fin de l’année, déclarer et payer. Vérifiez la dernière date sur le site de l’Autorité fiscale', 'act_sec' => '{label} : dépôt au-dessus du plafond légal',
				'export_btn' => 'Exporter le dossier de preuves', 'export_doc' => 'Dossier de preuves locatif', 'export_gen' => 'Généré le', 'export_note' => 'Résumé automatique des données enregistrées dans la gestion locative NadLan. Pas un document juridique.',
				'days_sfx' => ' j',
			),
			'ru' => array(
				'load_fail' => 'Не удалось загрузить объекты.', 'none_yet' => 'Пока нет объектов: добавьте первый ниже.', 'units' => 'квартир', 'sel_title' => 'Выбранная квартира',
				'sel_hint_mgr' => 'Нажмите на квартиру на модели. Пунктирная квартира ещё не отмечена как ваша: нажмите, чтобы добавить её.',
				'sel_hint_ro' => 'Нажмите на цветную квартиру на модели, чтобы увидеть управление арендой.',
				'portfolio' => 'Обзор портфеля', 'buildings' => 'зданий', 'monthly_rent' => 'Аренда в месяц', 'late_n' => 'просрочено', 'due_n' => 'не отмечено в этом месяце', 'vacant_n' => 'свободно',
				'next_actions' => 'Мои следующие шаги', 'no_actions' => 'Ничего срочного. Всё по плану.', 'derived_note' => 'Рассчитано автоматически из ваших данных. Это напоминания, не юридическая и не налоговая консультация.',
				'health' => array( 'contract' => 'Договор', 'rent' => 'Аренда', 'security' => 'Гарантии', 'repairs' => 'Ремонт', 'tax' => 'Налог', 'renewal' => 'Продление' ),
				'label' => 'Название квартиры', 'tenant' => 'Жилец', 'phone' => 'Телефон жильца', 'rent' => 'Аренда в месяц (₪)', 'start' => 'Начало договора', 'end' => 'Конец договора', 'opt' => 'Опцион до',
				'linkage' => 'Индексация', 'link_none' => 'Нет', 'link_madad' => 'По индексу цен', 'ledger' => 'Учёт платежей (12 месяцев)', 'docs' => 'Папка документов', 'maint' => 'Обслуживание', 'maint_new' => 'Новая неисправность', 'add' => 'Добавить',
				'urgent' => 'Срочно (жить нельзя)', 'standard' => 'Обычно', 'fix_by' => 'Предельный срок по закону', 'overdue_fix' => 'Срок по закону прошёл', 'mark_done' => 'Сделано', 'reopen' => 'Открыть снова', 'notes' => 'Заметки',
				'save' => 'Сохранить', 'saving' => 'Сохраняем...', 'saved' => 'Сохранено', 'save_fail' => 'Не сохранилось, попробуйте ещё раз',
				'wa_btn' => 'Напоминание в WhatsApp', 'wa_text' => 'Здравствуйте, {name}! Дружеское напоминание об аренде за {month}. Спасибо!', 'pro_btn' => 'Найти мастера', 'list_btn' => 'Опубликовать квартиру', 'studio_btn' => 'Спланировать квартиру (Студия)',
				'sec_title' => 'Гарантии', 'sec_check' => 'Гарантийный чек', 'sec_shtar' => 'Вексель', 'sec_arev' => 'Поручители', 'sec_bank' => 'Банковская гарантия / депозит',
				'sec_amount' => 'Сумма депозита / гарантии (₪)', 'sec_cap' => 'Законный предел затратных гарантий', 'sec_cap_f' => 'меньшее из 3 месяцев аренды и трети всей аренды за срок', 'sec_over' => 'Выше законного предела: уточните у юриста',
				'cpi_title' => 'Калькулятор индексации', 'cpi_base' => 'Базовый индекс (из договора)', 'cpi_cur' => 'Текущий индекс (ЦСБ)', 'cpi_pct' => 'Доля индексации', 'cpi_floor' => 'Не ниже базовой аренды (по договору)',
				'cpi_res' => 'Аренда после индексации', 'cpi_note' => 'Вводите индексы Центрального статистического бюро. Формула: аренда x (текущий / базовый). Только помощь в расчёте; решает текст договора.',
				'tax_title' => 'Оценка налога на аренду ({year})', 'tax_total' => 'Вся жилая аренда в месяц (ВСЕ ваши квартиры, включая те, что не ведутся здесь)',
				'tax_exempt' => 'Освобождено', 'tax_taxable' => 'Облагается (обычный режим)', 'tax_ten' => 'Режим 10% (в год)', 'tax_paid_rent' => 'Аренда, которую вы платите за своё жильё (в год, если снимаете)',
				'tax_deadline' => 'Режим 10%: отчитаться и заплатить нужно после окончания налогового года. Последний день проверьте на сайте Налогового управления.', 'tax_note' => 'Только оценки, с порогом освобождения {ceiling} ₪ в месяц (по руководству Налогового управления, это порог 2025 года). Актуальный порог проверьте на сайте Налогового управления. Перед действиями проверьте в Налоговом управлении или у бухгалтера.',
				'notice_l' => 'Уведомление арендодателя: за {d} дней до конца', 'notice_t' => 'Уведомление жильца: {d} дней',
				'act_late' => '{label}, {city}: аренда просрочена', 'act_due' => '{label}: месяц ещё не отмечен', 'act_end' => '{label}: договор заканчивается через {d} дн.', 'act_ended' => '{label}: договор ЗАКОНЧИЛСЯ, продлить или закрыть',
				'act_opt' => '{label}: окно опциона закрывается через {d} дн.', 'act_repair' => '{label}: срочный ремонт, срок по закону {d} дн.', 'act_repair_std' => '{label}: открытая неисправность близка к сроку 30 дней',
				'act_docs' => '{label}: папка документов неполная', 'act_tax' => 'Режим 10%: после окончания года подать отчёт и оплатить. Последний день проверьте на сайте Налогового управления', 'act_sec' => '{label}: депозит выше законного предела',
				'export_btn' => 'Выгрузить папку доказательств', 'export_doc' => 'Папка доказательств по аренде', 'export_gen' => 'Создано', 'export_note' => 'Автоматическая сводка данных из системы аренды NadLan. Не юридический документ.',
				'days_sfx' => ' дн.',
			),
			'ar' => array(
				'load_fail' => 'تعذّر تحميل عقاراتكم.', 'none_yet' => 'لا توجد عقارات بعد: أضيفوا الأول أدناه.', 'units' => 'شقق', 'sel_title' => 'الشقة المختارة',
				'sel_hint_mgr' => 'انقروا على شقة في المجسّم. الشقة المنقّطة لم تُسجَّل بعد كشقتكم: انقروا عليها لإضافتها.',
				'sel_hint_ro' => 'انقروا على شقة ملوّنة في المجسّم لرؤية إدارة إيجارها.',
				'portfolio' => 'صورة المحفظة', 'buildings' => 'مبانٍ', 'monthly_rent' => 'الإيجار الشهري', 'late_n' => 'متأخرة', 'due_n' => 'لم تُسجَّل هذا الشهر', 'vacant_n' => 'شاغرة',
				'next_actions' => 'خطواتي التالية', 'no_actions' => 'لا شيء عاجل. كل شيء على المسار.', 'derived_note' => 'محسوب تلقائيًا من بياناتكم. تذكيرات فقط، وليست استشارة قانونية أو ضريبية.',
				'health' => array( 'contract' => 'العقد', 'rent' => 'الإيجار', 'security' => 'الضمانات', 'repairs' => 'الإصلاحات', 'tax' => 'الضريبة', 'renewal' => 'التجديد' ),
				'label' => 'اسم الشقة', 'tenant' => 'المستأجر', 'phone' => 'هاتف المستأجر', 'rent' => 'الإيجار الشهري (₪)', 'start' => 'بداية العقد', 'end' => 'نهاية العقد', 'opt' => 'خيار حتى',
				'linkage' => 'الربط بالمؤشر', 'link_none' => 'بلا', 'link_madad' => 'مربوط بمؤشر الأسعار', 'ledger' => 'متابعة الدفعات (12 شهرًا)', 'docs' => 'ملف المستندات', 'maint' => 'الصيانة', 'maint_new' => 'عطل جديد', 'add' => 'إضافة',
				'urgent' => 'عاجل (يمنع السكن)', 'standard' => 'عادي', 'fix_by' => 'الموعد القانوني الأقصى', 'overdue_fix' => 'انقضى الموعد القانوني', 'mark_done' => 'تمّت المعالجة', 'reopen' => 'إعادة فتح', 'notes' => 'ملاحظات',
				'save' => 'حفظ', 'saving' => 'جارٍ الحفظ...', 'saved' => 'تم الحفظ', 'save_fail' => 'فشل الحفظ، حاولوا مرة أخرى',
				'wa_btn' => 'تذكير عبر واتساب', 'wa_text' => 'مرحبًا {name}، تذكير ودّي بإيجار شهر {month}. شكرًا!', 'pro_btn' => 'إيجاد مهني', 'list_btn' => 'نشر الشقة', 'studio_btn' => 'تخطيط الشقة (الاستوديو)',
				'sec_title' => 'الضمانات', 'sec_check' => 'شيك ضمان', 'sec_shtar' => 'سند دين', 'sec_arev' => 'كفلاء', 'sec_bank' => 'كفالة بنكية / وديعة',
				'sec_amount' => 'مبلغ الوديعة / الكفالة (₪)', 'sec_cap' => 'السقف القانوني للضمانات المكلفة', 'sec_cap_f' => 'الأقل بين إيجار 3 أشهر وثلث إيجار كامل المدة', 'sec_over' => 'فوق السقف القانوني: راجعوا محاميًا',
				'cpi_title' => 'حاسبة الربط بالمؤشر', 'cpi_base' => 'مؤشر الأساس (من العقد)', 'cpi_cur' => 'المؤشر الحالي (دائرة الإحصاء)', 'cpi_pct' => 'نسبة الربط', 'cpi_floor' => 'حدّ أدنى بقيمة الإيجار الأساسي (حسب العقد)',
				'cpi_res' => 'الإيجار المحدَّث', 'cpi_note' => 'أدخلوا قيم المؤشر من دائرة الإحصاء المركزية. المعادلة: الإيجار x (الحالي / الأساس). مساعدة في الحساب فقط؛ نص العقد هو الحاسم.',
				'tax_title' => 'تقدير ضريبة الإيجار ({year})', 'tax_total' => 'مجموع الإيجار السكني الشهري (كل شققكم، بما فيها غير المُدارة هنا)',
				'tax_exempt' => 'معفى', 'tax_taxable' => 'خاضع للضريبة (المسار العادي)', 'tax_ten' => 'مسار 10% (سنوي)', 'tax_paid_rent' => 'الإيجار الذي تدفعونه عن منزلكم (سنويًا، إن كنتم مستأجرين)',
				'tax_deadline' => 'مسار 10%: يُصرَّح عنه ويُدفع بعد انتهاء السنة الضريبية. تحقّقوا من اليوم الأخير على موقع سلطة الضرائب.', 'tax_note' => 'تقديرات فقط، بسقف إعفاء قدره {ceiling} ₪ شهريًا (حسب دليل سلطة الضرائب هذا هو سقف 2025). تحقّقوا من السقف الحالي على موقع سلطة الضرائب. تحقّقوا لدى سلطة الضرائب أو محاسب قبل أي إجراء.',
				'notice_l' => 'إشعار المؤجر: {d} يومًا قبل النهاية', 'notice_t' => 'إشعار المستأجر: {d} يومًا',
				'act_late' => '{label}، {city}: الإيجار متأخر', 'act_due' => '{label}: الشهر لم يُسجَّل بعد', 'act_end' => '{label}: ينتهي العقد بعد {d} يومًا', 'act_ended' => '{label}: انتهى العقد، جدّدوا أو أغلقوا',
				'act_opt' => '{label}: نافذة الخيار تُغلق بعد {d} يومًا', 'act_repair' => '{label}: إصلاح عاجل، الموعد القانوني {d} أيام', 'act_repair_std' => '{label}: عطل مفتوح يقترب من موعد 30 يومًا',
				'act_docs' => '{label}: ملف المستندات ناقص', 'act_tax' => 'مسار 10%: بعد انتهاء السنة، التصريح والدفع. تحقّقوا من اليوم الأخير على موقع سلطة الضرائب', 'act_sec' => '{label}: الوديعة فوق السقف القانوني',
				'export_btn' => 'تصدير ملف الأدلة', 'export_doc' => 'ملف أدلة الإيجار', 'export_gen' => 'أُنشئ في', 'export_note' => 'ملخص تلقائي للبيانات المسجّلة في نظام إدارة الإيجارات في NadLan. ليس مستندًا قانونيًا.',
				'days_sfx' => ' أيام',
			),
		);
		return isset( $S[ $lang ] ) ? $S[ $lang ] : array();
	}
}

/* ---------- the visitor page in five languages ---------- */
if ( ! function_exists( 'nadlan_re_copy' ) ) {
	function nadlan_re_copy( $lang ) {
		$C = array(
			'he' => array(
				'title' => 'ניהול השכרות חינם לבעלי דירות: המפה, הבניין בתלת-ממד וכל דירה מושכרת במקום אחד | נדלן',
				'desc' => 'מערכת חינמית לניהול דירות מושכרות: כל הנכסים על מפה, כל בניין במודל תלת-ממדי, ולכל דירה: שוכר, שכר דירה, מעקב תשלומים, תזכורות חוזה ומס, מסמכים ותחזוקה. ובנוסף: כמה הדירה תכניס, לפי נתוני הלמ"ס.',
				'kicker' => 'ניהול השכרות · חינם לבעלי דירות', 'h1' => 'כל הדירות המושכרות שלכם: על המפה, בתוך הבניין, בשליטה מלאה',
				'sub' => 'מוסיפים נכס, מסמנים את הדירות שלכם על מודל תלת-ממדי של הבניין, ומנהלים הכל מדירה אחת: שוכר, שכר דירה, מעקב תשלומים, תזכורות חוזה ומס, מסמכים ותחזוקה. בלי אקסל ובלי עמלות.',
				'go' => 'מתחילים לנהל, חינם', 'earn_go' => 'כמה הדירה תכניס?', 'badges' => 'חינם לבעלי דירות · מעקב ותזכורות, לא סליקה · פרטי ולא מופיע בחיפוש',
				's1' => array( 'מוסיפים נכס', 'עיר, כתובת, קומות, ונבנה לכם מודל תלת-ממדי של הבניין על המפה.' ),
				's2' => array( 'מסמנים את הדירות שלכם', 'מקישים על הדירות שבבעלותכם על המודל וממלאים שוכר, שכר דירה ותאריכי חוזה.' ),
				's3' => array( 'הכל במעקב אחד', 'צבע הדירה אומר הכל: שולם, ממתין, בפיגור, פנויה. תזכורות חוזה, מסמכים ותחזוקה במקום אחד.' ),
				'earn_h' => 'קונים דירה ומשכירים בינתיים?', 'earn_p' => 'בחרו עיר וגודל וקבלו את טווח שכר הדירה מהלשכה המרכזית לסטטיסטיקה, את החשבון שלכם אחרי מס, ואת מי שינהל את הדירה.',
				'demo_h' => 'הדגמה חיה: תיק של משכיר עם ארבע דירות', 'demo_l' => 'נתוני דוגמה',
				'honest' => 'הגינות מלאה: המערכת עוקבת ומזכירה. היא לא גובה כסף ולא מבצעת סליקה. שכר הדירה ממשיך לעבור כרגיל, בהעברה בנקאית או בצ\'קים. תזכורות המס הן תזכורות בלבד, ואת המספרים המחייבים בודקים מול רשות המסים.',
				'guide_note' => '',
				'faq' => array(
					array( 'כמה זה עולה?', 'ניהול ההשכרות חינמי לבעלי דירות. אין עמלות ואין סליקה, ושכר הדירה ממשיך לעבור ישירות אליכם.' ),
					array( 'מי רואה את הנתונים שלי?', 'רק אתם. הנכסים פרטיים, לא מופיעים בחיפוש, והגישה מוגנת בחשבון שלכם.' ),
					array( 'כמה דירה מכניסה בשכירות?', 'לפי הלשכה המרכזית לסטטיסטיקה, שכר הדירה הממוצע בישראל ביולי עד ספטמבר 2026 היה 5,132 ₪ לחודש. המחשבון בעמוד מציג את הממוצע לפי עיר ומספר חדרים, עם טווח הטעות של הלשכה.' ),
					array( 'מה עם הצמדה למדד ומס?', 'מסמנים חוזה צמוד מדד ומקבלים תזכורת עדכון. המערכת מזכירה גם, אחרי סוף שנת המס, לדווח ולשלם במסלול 10 אחוזים; את היום האחרון המדויק בודקים באתר רשות המסים. המספרים המחייבים נבדקים תמיד מול רשות המסים.' ),
				),
			),
			'en' => array(
				'title' => 'Free Rental Management for Landlords in Israel: the Map, the 3D Building, Every Apartment in One File | Nadlan',
				'desc' => 'A free digital lease file for Israeli landlords: every property on a map, every building in 3D, and per apartment the tenant, rent tracking, CPI and tax reminders, documents and maintenance. Plus what the apartment will earn, from official CBS data.',
				'kicker' => 'Rental management · free for landlords', 'h1' => 'Every apartment you rent out: on the map, inside the building, fully in control',
				'sub' => 'Add a property, mark your apartments on a 3D model of the building, and manage everything per apartment: tenant, rent tracking, lease and tax reminders, documents and maintenance. No spreadsheets, no fees.',
				'go' => 'Start managing, free', 'earn_go' => 'How much will it earn?', 'badges' => 'Free for landlords · tracking and reminders, no payment processing · private, never in search',
				's1' => array( 'Add a property', 'City, address, floors, and we build a 3D model of your building on the map.' ),
				's2' => array( 'Mark your apartments', 'Tap the apartments you own on the model and fill in tenant, rent and lease dates.' ),
				's3' => array( 'One colour says it all', 'The apartment colour tells the story: paid, pending, overdue, vacant. Lease reminders, documents and maintenance in one place.' ),
				'earn_h' => 'Buying, and renting it out meanwhile?', 'earn_p' => 'Pick a city and a size: the rent range from the Central Bureau of Statistics, your own numbers after tax, and who will manage the apartment.',
				'demo_h' => 'Live demo: a landlord file with four apartments', 'demo_l' => 'Sample data',
				'honest' => 'Full honesty: the system tracks and reminds. It does not collect money or process payments. Rent keeps flowing as usual, by bank transfer or cheques. Tax reminders are reminders only; binding numbers are checked with the Israel Tax Authority.',
				'guide_note' => '',
				'faq' => array(
					array( 'How much does it cost?', 'Rental management is free for landlords. No fees, no payment processing: rent keeps flowing directly to you.' ),
					array( 'Who sees my data?', 'Only you. Properties are private, never listed in search, and access is protected by your account.' ),
					array( 'How much does an apartment earn when rented?', 'According to the Central Bureau of Statistics, the average rent in Israel in July to September 2026 was 5,132 shekels a month. The calculator on this page shows the average by city and number of rooms, with the Bureau\'s margin.' ),
					array( 'What about CPI linkage and tax?', 'Mark a CPI-linked lease and get an adjustment reminder; the system also reminds you, after the end of the tax year, to report and pay on the 10 percent route; the exact last day is checked on the Tax Authority site. Binding numbers are always checked with the Israel Tax Authority.' ),
				),
			),
			'fr' => array(
				'title' => 'Gestion locative gratuite pour propriétaires en Israël : la carte, l’immeuble en 3D, chaque appartement dans un seul dossier | Nadlan',
				'desc' => 'Un dossier locatif numérique et gratuit pour les propriétaires en Israël : chaque bien sur une carte, chaque immeuble en 3D, et par appartement le locataire, le suivi des loyers, les rappels d’indexation et d’impôt, les documents et l’entretien. Et ce que l’appartement rapportera, selon les données officielles.',
				'kicker' => 'Gestion locative · gratuite pour les propriétaires', 'h1' => 'Tous les appartements que vous louez : sur la carte, dans l’immeuble, sous contrôle',
				'sub' => 'Ajoutez un bien, marquez vos appartements sur une maquette 3D de l’immeuble et gérez tout appartement par appartement : locataire, suivi des loyers, rappels de bail et d’impôt, documents et entretien. Sans tableur, sans frais.',
				'go' => 'Commencer, gratuitement', 'earn_go' => 'Combien rapportera-t-il ?', 'badges' => 'Gratuit pour les propriétaires · suivi et rappels, sans encaissement · privé, jamais dans la recherche',
				's1' => array( 'Ajoutez un bien', 'Ville, adresse, étages : nous construisons une maquette 3D de votre immeuble sur la carte.' ),
				's2' => array( 'Marquez vos appartements', 'Touchez les appartements qui vous appartiennent et indiquez locataire, loyer et dates du bail.' ),
				's3' => array( 'Une couleur dit tout', 'La couleur de l’appartement raconte tout : payé, en attente, en retard, vacant. Rappels, documents et entretien au même endroit.' ),
				'earn_h' => 'Vous achetez et louez en attendant ?', 'earn_p' => 'Choisissez une ville et une taille : la fourchette de loyer du Bureau central des statistiques, vos propres chiffres après impôt, et qui gérera l’appartement.',
				'demo_h' => 'Démo en direct : le dossier d’un propriétaire avec quatre appartements', 'demo_l' => 'Données d’exemple',
				'honest' => 'En toute transparence : le système suit et rappelle. Il n’encaisse pas d’argent et ne traite aucun paiement. Le loyer continue d’arriver comme d’habitude, par virement ou par chèque. Les rappels fiscaux ne sont que des rappels ; les montants qui engagent se vérifient auprès de l’Autorité fiscale israélienne.',
				'guide_note' => 'Le guide complet, du premier jour à la dixième année, existe en anglais et en hébreu :',
				'faq' => array(
					array( 'Combien ça coûte ?', 'La gestion locative est gratuite pour les propriétaires. Sans frais, sans encaissement : le loyer arrive directement chez vous.' ),
					array( 'Qui voit mes données ?', 'Vous seul. Les biens sont privés, jamais dans la recherche, et l’accès est protégé par votre compte.' ),
					array( 'Combien rapporte un appartement en location ?', 'Selon le Bureau central des statistiques, le loyer moyen en Israël de juillet à septembre 2026 était de 5 132 shekels par mois. Le calculateur de cette page donne la moyenne par ville et par nombre de pièces, avec la marge du Bureau.' ),
				),
			),
			'ru' => array(
				'title' => 'Бесплатное управление арендой для владельцев квартир в Израиле: карта, здание в 3D, каждая квартира в одной папке | Nadlan',
				'desc' => 'Бесплатная цифровая папка аренды для владельцев в Израиле: все объекты на карте, каждое здание в 3D, по каждой квартире жилец, учёт платежей, напоминания об индексации и налоге, документы и обслуживание. И сколько квартира принесёт, по официальным данным.',
				'kicker' => 'Управление арендой · бесплатно для владельцев', 'h1' => 'Все квартиры, которые вы сдаёте: на карте, внутри здания, под полным контролем',
				'sub' => 'Добавьте объект, отметьте свои квартиры на 3D-модели здания и ведите всё по каждой квартире: жилец, учёт платежей, напоминания о договоре и налоге, документы и обслуживание. Без таблиц и без комиссий.',
				'go' => 'Начать бесплатно', 'earn_go' => 'Сколько она принесёт?', 'badges' => 'Бесплатно для владельцев · учёт и напоминания, без приёма платежей · приватно, не в поиске',
				's1' => array( 'Добавьте объект', 'Город, адрес, этажи, и мы построим 3D-модель вашего здания на карте.' ),
				's2' => array( 'Отметьте свои квартиры', 'Нажмите на свои квартиры на модели и укажите жильца, аренду и даты договора.' ),
				's3' => array( 'Всё видно по цвету', 'Цвет квартиры говорит всё: оплачено, ожидает, просрочено, свободна. Напоминания, документы и обслуживание в одном месте.' ),
				'earn_h' => 'Покупаете и пока сдаёте?', 'earn_p' => 'Выберите город и размер: диапазон аренды по данным Центрального статистического бюро, ваш расчёт после налога и кто будет управлять квартирой.',
				'demo_h' => 'Живая демонстрация: папка владельца с четырьмя квартирами', 'demo_l' => 'Пример данных',
				'honest' => 'Честно: система ведёт учёт и напоминает. Она не собирает деньги и не принимает платежи. Аренда поступает как обычно, переводом или чеками. Налоговые напоминания только напоминают; обязательные суммы проверяются в Налоговом управлении Израиля.',
				'guide_note' => 'Полное руководство, от первого дня до десятого года, есть на английском и иврите:',
				'faq' => array(
					array( 'Сколько это стоит?', 'Управление арендой бесплатно для владельцев. Без комиссий и без приёма платежей: аренда приходит прямо к вам.' ),
					array( 'Кто видит мои данные?', 'Только вы. Объекты приватны, не появляются в поиске, доступ защищён вашим аккаунтом.' ),
					array( 'Сколько приносит квартира при сдаче?', 'По данным Центрального статистического бюро, средняя аренда в Израиле в июле–сентябре 2026 года составила 5 132 шекеля в месяц. Калькулятор на этой странице показывает среднее по городу и числу комнат, с погрешностью Бюро.' ),
				),
			),
			'ar' => array(
				'title' => 'إدارة إيجارات مجانية لأصحاب الشقق في إسرائيل: الخريطة، المبنى بالأبعاد الثلاثية، كل شقة في ملف واحد | Nadlan',
				'desc' => 'ملف إيجار رقمي مجاني لأصحاب الشقق في إسرائيل: كل العقارات على خريطة، كل مبنى بالأبعاد الثلاثية، ولكل شقة المستأجر ومتابعة الدفعات وتذكيرات الربط بالمؤشر والضريبة والمستندات والصيانة. وكم ستدرّ الشقة، حسب البيانات الرسمية.',
				'kicker' => 'إدارة الإيجارات · مجانًا لأصحاب الشقق', 'h1' => 'كل الشقق التي تؤجّرونها: على الخريطة، داخل المبنى، تحت سيطرة كاملة',
				'sub' => 'أضيفوا عقارًا، وحدّدوا شققكم على مجسّم ثلاثي الأبعاد للمبنى، وأديروا كل شيء لكل شقة: المستأجر، متابعة الدفعات، تذكيرات العقد والضريبة، المستندات والصيانة. بلا جداول وبلا عمولات.',
				'go' => 'ابدأوا الإدارة مجانًا', 'earn_go' => 'كم ستدرّ الشقة؟', 'badges' => 'مجاني لأصحاب الشقق · متابعة وتذكيرات بلا تحصيل · خاص ولا يظهر في البحث',
				's1' => array( 'أضيفوا عقارًا', 'المدينة والعنوان والطوابق، ونبني لكم مجسّمًا ثلاثي الأبعاد للمبنى على الخريطة.' ),
				's2' => array( 'حدّدوا شققكم', 'انقروا على الشقق التي تملكونها في المجسّم واملأوا المستأجر والإيجار وتواريخ العقد.' ),
				's3' => array( 'اللون يقول كل شيء', 'لون الشقة يروي القصة: مدفوع، بانتظار، متأخر، شاغر. التذكيرات والمستندات والصيانة في مكان واحد.' ),
				'earn_h' => 'تشترون وتؤجّرون في الأثناء؟', 'earn_p' => 'اختاروا مدينة وحجمًا: نطاق الإيجار من دائرة الإحصاء المركزية، وحسابكم بعد الضريبة، ومن سيدير الشقة.',
				'demo_h' => 'عرض حيّ: ملف مؤجّر بأربع شقق', 'demo_l' => 'بيانات مثال',
				'honest' => 'بكل شفافية: النظام يتابع ويذكّر. لا يجمع أموالًا ولا ينفّذ دفعات. يستمر الإيجار بالوصول كالمعتاد، بتحويل بنكي أو بشيكات. تذكيرات الضريبة تذكيرات فقط، والمبالغ الملزمة تُفحص لدى سلطة الضرائب الإسرائيلية.',
				'guide_note' => 'الدليل الكامل، من اليوم الأول حتى السنة العاشرة، متاح بالإنجليزية والعبرية:',
				'faq' => array(
					array( 'كم يكلّف ذلك؟', 'إدارة الإيجارات مجانية لأصحاب الشقق. بلا عمولات وبلا تحصيل: يصل الإيجار إليكم مباشرة.' ),
					array( 'من يرى بياناتي؟', 'أنتم فقط. العقارات خاصة ولا تظهر في البحث، والدخول محمي بحسابكم.' ),
					array( 'كم تدرّ الشقة عند تأجيرها؟', 'حسب دائرة الإحصاء المركزية، بلغ متوسط الإيجار في إسرائيل بين يوليو وسبتمبر 2026 نحو 5,132 شيكل شهريًا. تعرض الحاسبة في هذه الصفحة المتوسط حسب المدينة وعدد الغرف، مع هامش الدائرة.' ),
				),
			),
		);
		return $C[ $lang ];
	}
}

if ( ! function_exists( 'nadlan_re_earn_opts' ) ) {
	function nadlan_re_earn_opts( $lang, $extra = array() ) {
		return array_merge( array(
			'lang' => $lang,
			'data' => nadlan_re_asset( 'cbs-rent-2026q3.json' ),
			'lead' => rest_url( 'nadlan/v1/lead' ),
			'my'   => nadlan_re_url( $lang ) . '#nlre-start',
		), $extra );
	}
}

if ( ! function_exists( 'nadlan_re_landing' ) ) {
	function nadlan_re_landing( $lang ) {
		$c = nadlan_re_copy( $lang );
		$rtl = in_array( $lang, array( 'he', 'ar' ), true );
		$self = nadlan_re_url( $lang );
		/* the area from a deep link (?earn=tel-aviv.r4, the basket's "link") */
		$area = 'tel-aviv'; $rooms = 'r4';
		if ( isset( $_GET['earn'] ) && preg_match( '/^([a-z\-]{2,20})\.(r[1345])$/', sanitize_text_field( wp_unslash( $_GET['earn'] ) ), $m ) ) { $area = $m[1]; $rooms = $m[2]; } // phpcs:ignore WordPress.Security.NonceVerification
		$locale = array( 'he' => 'he-IL', 'en' => 'en-US', 'fr' => 'fr-FR', 'ru' => 'ru-RU', 'ar' => 'ar' );
		add_filter( 'pre_get_document_title', function () use ( $c ) { return $c['title']; }, 99 );
		add_filter( 'language_attributes', function () use ( $lang, $rtl, $locale ) { return 'lang="' . esc_attr( $locale[ $lang ] ) . '" dir="' . ( $rtl ? 'rtl' : 'ltr' ) . '"'; }, 99 );
		add_action( 'wp_head', function () use ( $c, $self ) {
			echo '<meta name="description" content="' . esc_attr( $c['desc'] ) . '">' . "\n";
			echo '<link rel="canonical" href="' . esc_url( $self ) . '">' . "\n";
			foreach ( array( 'he', 'en', 'fr', 'ru', 'ar' ) as $l ) { echo '<link rel="alternate" hreflang="' . $l . '" href="' . esc_url( nadlan_re_url( $l ) ) . '">' . "\n"; } // phpcs:ignore
			echo '<link rel="alternate" hreflang="x-default" href="' . esc_url( nadlan_re_url( 'he' ) ) . '">' . "\n";
			echo '<link rel="stylesheet" href="' . esc_url( nadlan_re_asset( 'earn.css' ) ) . '">' . "\n";
		}, 4 );
		if ( function_exists( 'nadlan_dir_header_single_h1' ) ) { nadlan_dir_header_single_h1(); } else { get_header(); }
		$names = array( 'he' => 'עברית', 'en' => 'English', 'fr' => 'Français', 'ru' => 'Русский', 'ar' => 'العربية' );
		$login = wp_login_url( $self );
		$glb = esc_url( function_exists( 'nadlan_showroom_engine_base_url' ) ? nadlan_showroom_engine_base_url() . 'models/standard-residential.glb' : '' );
		$token = function_exists( 'nadlan_mapbox_token' ) ? nadlan_mapbox_token() : '';
		$js = esc_url( plugins_url( 'assets/rentals/rental-manager.js', dirname( __FILE__ ) ) . '?v=' . nadlan_re_ver() );
		$app_lang = $lang; // rental-manager.js reads data-lang; its strings come from data-i18n in this language
		?>
<div class="nlrx" dir="<?php echo $rtl ? 'rtl' : 'ltr'; ?>" lang="<?php echo esc_attr( $lang ); ?>">
	<style>
	.nlrx{--ink:#0E1B24;--ink2:#2B3B46;--mute:#41535F;--line:#C9D2D6;--ground:#F3F5F4;--blue:#1F4FD1;--blue2:#163A9E;--stage:#E3EAEE;
		max-width:1120px;margin:0 auto;padding:20px 16px 64px;color:var(--ink);font-family:"IBM Plex Sans","IBM Plex Sans Hebrew","IBM Plex Sans Arabic",system-ui,sans-serif;line-height:1.6}
	.nlrx[lang=he]{font-family:"IBM Plex Sans Hebrew","IBM Plex Sans",system-ui,sans-serif}.nlrx[lang=ar]{font-family:"IBM Plex Sans Arabic","IBM Plex Sans",system-ui,sans-serif}
	body:has(.nlrx){background:#F3F5F4}
	.nlrx h1,.nlrx h2,.nlrx h3{font-family:inherit!important;color:var(--ink)!important;letter-spacing:0}
	.nlrx-langs{display:flex;flex-wrap:wrap;gap:6px;justify-content:center;margin:0 0 14px;padding:0;list-style:none}
	.nlrx-langs a{display:inline-flex;align-items:center;min-height:36px;padding:0 12px;border:1px solid var(--line);border-radius:999px;font-size:13px;font-weight:600;color:var(--ink)!important;text-decoration:none!important;background:#fff}
	.nlrx-langs a[aria-current]{background:var(--ink);color:#fff!important;border-color:var(--ink)}
	.nlrx-hero{text-align:center;padding:12px 0 6px}
	.nlrx-kicker{margin:0 0 10px;font:600 12px/1.4 "IBM Plex Mono",monospace;letter-spacing:.1em;color:var(--mute);text-transform:uppercase}
	.nlrx-hero h1{font-size:clamp(1.65rem,4.6vw,2.6rem);line-height:1.2;margin:0 auto 12px;max-width:860px;font-weight:700}
	.nlrx-hero .sub{max-width:720px;margin:0 auto 18px;font-size:16px;color:var(--ink2)}
	.nlrx-ctas{display:flex;flex-wrap:wrap;gap:10px;justify-content:center}
	.nlrx a.nlrx-cta{display:inline-flex;align-items:center;justify-content:center;min-height:52px;padding:0 24px;border-radius:6px;font-weight:700;font-size:16px;text-decoration:none!important}
	.nlrx a.nlrx-cta--go{background:var(--blue)!important;color:#fff!important}
	.nlrx a.nlrx-cta--go:hover{background:var(--blue2)!important}
	.nlrx a.nlrx-cta--line{background:#fff!important;color:var(--ink)!important;border:2px solid var(--ink)}
	.nlrx-badges{margin:14px 0 22px;font-size:13px;color:var(--mute);text-align:center}
	.nlrx-steps{display:grid;gap:12px;margin:0 0 30px}
	@media(min-width:760px){.nlrx-steps{grid-template-columns:repeat(3,minmax(0,1fr))}}
	.nlrx-step{background:#fff;border:1px solid var(--line);border-radius:10px;padding:16px}
	.nlrx-step i{display:inline-flex;width:30px;height:30px;align-items:center;justify-content:center;border:2px solid var(--ink);border-radius:50%;font:600 14px "IBM Plex Mono",monospace;font-style:normal;margin-bottom:8px}
	.nlrx-step b{display:block;font-size:16px;margin-bottom:2px}
	.nlrx-step p{margin:0;font-size:14px;color:var(--ink2)}
	.nlrx-sec{margin:0 0 32px;scroll-margin-top:90px}
	.nlrx-sec>h2{font-size:clamp(1.3rem,3.4vw,1.75rem);margin:0 0 6px;font-weight:700}
	.nlrx-sec>p{margin:0 0 14px;color:var(--ink2);max-width:760px}
	.nlrx-demo{background:#fff;border:1px solid var(--line);border-radius:12px;padding:14px}
	.nlrx-demo-head{display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:8px;margin:0 0 10px}
	.nlrx-demo-head h2{margin:0;font-size:1.2rem;font-weight:700}
	.nlrx-demo-head .lbl{background:var(--ink);color:#fff;font:600 12px "IBM Plex Mono",monospace;border-radius:999px;padding:6px 12px}
	.nlrx-honest{background:#fff;border:1px solid var(--line);border-inline-start:4px solid var(--ink);border-radius:8px;padding:14px 16px;font-size:14px;color:var(--ink2);margin:0 0 30px}
	.nlrx-gnote{background:#fff;border:1px solid var(--line);border-radius:8px;padding:14px 16px;font-size:14.5px}
	.nlrx-gnote a{color:var(--blue)!important;font-weight:700;margin-inline-start:10px}
	/* the existing demo app (rental-manager.js), restyled to the board: blueprint stage, readable buttons */
	.nlrx .nlrm-app{min-height:200px;font-family:inherit}
	.nlrx .nlrm-app[data-loading]{color:var(--mute);text-align:center;padding:30px 0}
	.nlrx .nlrm-map{height:300px;border-radius:10px;overflow:hidden;background:var(--stage);border:1px solid var(--line)}
	.nlrx .nlrm-props{display:flex;gap:8px;flex-wrap:wrap;margin:12px 0}
	.nlrx .nlrm-props button{min-height:44px;border:1px solid var(--line)!important;border-radius:999px;padding:0 15px;font-weight:600;font-size:13.5px;color:var(--ink)!important;background:#fff!important;cursor:pointer}
	.nlrx .nlrm-props button.is-on{background:var(--ink)!important;color:#fff!important;border-color:var(--ink)!important}
	.nlrx .nlrm-3d{position:relative;height:52vh;min-height:380px;max-height:600px;border-radius:12px;overflow:hidden;background:linear-gradient(var(--stage),var(--stage)),repeating-linear-gradient(0deg,transparent 0 23px,#d3dce1 23px 24px);background-blend-mode:multiply;border:1px solid var(--line);margin-top:8px}
	@media(max-width:600px){.nlrx .nlrm-3d{height:56vh}}
	.nlrx .nlrm-3d model-viewer{width:100%;height:100%;direction:ltr;background:transparent;--poster-color:transparent}
	.nlrx .nlrm-hot{width:30px;height:30px;border-radius:50%;border:2px solid #fff;color:#fff;font-weight:700;font-size:10.5px;cursor:pointer;background:#7C8B95;box-shadow:0 0 0 1px rgba(14,27,36,.35)}
	.nlrx .nlrm-hot:not([data-visible]){opacity:0;pointer-events:none}
	.nlrx .nlrm-hot.is-ghost{background:rgba(124,139,149,.35);border-style:dashed;color:var(--ink)}
	.nlrx .nlrm-legend{display:flex;gap:12px;flex-wrap:wrap;margin:10px 2px;font-weight:600;font-size:12.5px;color:var(--ink2)}
	.nlrx .nlrm-legend i{display:inline-block;width:11px;height:11px;border-radius:50%;margin-inline-end:4px;vertical-align:-1px}
	.nlrx .nlrm-grid{display:grid;grid-template-columns:1fr;gap:12px;margin-top:12px}
	@media(min-width:860px){.nlrx .nlrm-grid{grid-template-columns:1fr 1fr}}
	.nlrx .nlrm-card{background:#fff;border:1px solid var(--line);border-radius:10px;padding:16px 18px}
	.nlrx .nlrm-card h4{font-family:inherit!important;margin:0 0 10px;font-size:1.04rem;color:var(--ink)!important}
	.nlrx .nlrm-note{font-size:12.5px;color:var(--mute)}
	.nlrx .nlrm-btn{min-height:44px;background:var(--blue)!important;color:#fff!important;border:0;border-radius:6px;padding:0 18px;font-weight:700;font-size:14px;cursor:pointer;margin-top:8px}
	.nlrx .nlrm-btn--ghost{background:#fff!important;color:var(--ink)!important;border:2px solid var(--ink)}
	.nlrx .nlrm-app input,.nlrx .nlrm-app select,.nlrx .nlrm-app textarea{width:100%;min-height:42px;border:1px solid var(--line);border-radius:6px;padding:8px 10px;font-size:14px;background:#fff;box-sizing:border-box;color:var(--ink)}
	.nlrx .nlrm-f{display:grid;grid-template-columns:1fr 1fr;gap:10px;margin:8px 0}
	.nlrx .nlrm-f label{display:flex;flex-direction:column;gap:4px;font-weight:600;font-size:12px;color:var(--ink2)}
	.nlrx .nlrm-chips{display:flex;gap:8px;flex-wrap:wrap;margin:8px 0}
	.nlrx .nlrm-chip{display:inline-block;border-radius:999px;padding:6px 12px;font-weight:600;font-size:12px;background:var(--ground);border:1px solid var(--line);color:var(--ink2)}
	.nlrx .nlrm-chip--warn{background:#FDECEC;border-color:#C62828;color:#7F1D1D}
	.nlrx .nlrm-chip--gold{background:#EAF0FF;border-color:var(--blue);color:#163A9E}
	.nlrx .nlrm-ledger{display:grid;grid-template-columns:repeat(6,1fr);gap:6px;margin:8px 0}
	@media(max-width:520px){.nlrx .nlrm-ledger{grid-template-columns:repeat(4,1fr)}}
	.nlrx .nlrm-ledger button{min-height:40px;border:1px solid var(--line)!important;border-radius:6px;padding:4px 2px;font-weight:600;font-size:11.5px;background:#fff!important;cursor:pointer;color:var(--ink2)!important}
	.nlrx .nlrm-ledger button.is-paid{background:#1B7F6B!important;border-color:#1B7F6B!important;color:#fff!important}
	.nlrx .nlrm-docrow{display:flex;align-items:center;gap:8px;font-size:13.5px;margin:5px 0}
	.nlrx .nlrm-docrow input{width:auto;min-height:0}
	.nlrx .nlrm-maint li{font-size:13px;border-bottom:1px solid #DDE3E6;padding:6px 0;list-style:none;display:flex;justify-content:space-between;gap:8px}
	.nlrx .nlrm-maint li.is-done{color:var(--mute);text-decoration:line-through}
	.nlrx .nlrm-actions{display:flex;gap:8px;flex-wrap:wrap;margin-top:10px}
	.nlrx .nlrm-actions a{display:inline-flex;align-items:center;min-height:44px;border:1px solid var(--line);border-radius:6px;padding:0 14px;font-weight:700;font-size:12.5px;color:var(--ink)!important;text-decoration:none!important;background:#fff}
	.nlrx .nlrm-actions a:hover{border-color:var(--ink)}
	.nlrx .nlrm-guide{--g-paper:#fff}
	h1:empty{display:none}
	</style>
	<nav aria-label="Language"><ul class="nlrx-langs"><?php foreach ( $names as $l => $n ) { echo '<li><a href="' . esc_url( nadlan_re_url( $l ) ) . '" hreflang="' . esc_attr( $l ) . '" lang="' . esc_attr( $l ) . '"' . ( $l === $lang ? ' aria-current="page"' : '' ) . '>' . esc_html( $n ) . '</a></li>'; } ?></ul></nav>
	<header class="nlrx-hero" id="nlre-start">
		<p class="nlrx-kicker"><?php echo esc_html( $c['kicker'] ); ?></p>
		<h1><?php echo esc_html( $c['h1'] ); ?></h1>
		<p class="sub"><?php echo esc_html( $c['sub'] ); ?></p>
		<div class="nlrx-ctas">
			<a class="nlrx-cta nlrx-cta--go" href="<?php echo esc_url( $login ); ?>"><?php echo esc_html( $c['go'] ); ?></a>
			<a class="nlrx-cta nlrx-cta--line" href="#earn"><?php echo esc_html( $c['earn_go'] ); ?></a>
		</div>
		<p class="nlrx-badges"><?php echo esc_html( $c['badges'] ); ?></p>
	</header>
	<div class="nlrx-steps">
		<?php foreach ( array( 's1', 's2', 's3' ) as $i => $k ) { echo '<div class="nlrx-step"><i>' . ( $i + 1 ) . '</i><b>' . esc_html( $c[ $k ][0] ) . '</b><p>' . esc_html( $c[ $k ][1] ) . '</p></div>'; } ?>
	</div>
	<section class="nlrx-sec" id="earn" aria-labelledby="nlrx-earn-h">
		<h2 id="nlrx-earn-h"><?php echo esc_html( $c['earn_h'] ); ?></h2>
		<p><?php echo esc_html( $c['earn_p'] ); ?></p>
		<div data-nadlan-earn="<?php echo esc_attr( wp_json_encode( nadlan_re_earn_opts( $lang, array( 'area' => $area, 'rooms' => $rooms ) ), JSON_UNESCAPED_UNICODE | JSON_UNESCAPED_SLASHES ) ); ?>"></div>
	</section>
	<section class="nlrx-sec nlrx-demo">
		<div class="nlrx-demo-head"><h2><?php echo esc_html( $c['demo_h'] ); ?></h2><span class="lbl"><?php echo esc_html( $c['demo_l'] ); ?></span></div>
		<div id="nlrm-mount" class="nlrm-app" data-loading="1"
			data-mode="demo" data-lang="<?php echo esc_attr( $app_lang ); ?>"
			data-i18n="<?php echo esc_attr( wp_json_encode( nadlan_re_app_strings( $lang ), JSON_UNESCAPED_UNICODE ) ); ?>"
			data-rest="<?php echo esc_url( rest_url( 'nadlan/v1' ) ); ?>" data-nonce=""
			data-glb="<?php echo $glb; // phpcs:ignore ?>" data-mapbox="<?php echo esc_attr( $token ); ?>"
			data-pros="<?php echo esc_url( home_url( '/professionals/' ) ); ?>" data-wizard="<?php echo esc_url( home_url( '/list-property/' ) ); ?>"
			data-studio="<?php echo esc_url( home_url( '/studio/' ) ); ?>" data-glossary="<?php echo esc_url( home_url( '/glossary/' ) ); ?>">…</div>
		<script defer src="<?php echo $js; // phpcs:ignore ?>"></script>
	</section>
	<div class="nlrx-honest"><?php echo esc_html( $c['honest'] ); ?></div>
	<?php
	if ( in_array( $lang, array( 'he', 'en' ), true ) ) {
		$gf = ( defined( 'NLRM_DIR_ASSETS' ) ? NLRM_DIR_ASSETS : plugin_dir_path( dirname( __FILE__ ) ) . 'assets/rentals/' ) . 'guide/' . $lang . '.html';
		if ( is_readable( $gf ) ) {
			echo '<link rel="stylesheet" href="' . esc_url( ( defined( 'NLRM_URL_ASSETS' ) ? NLRM_URL_ASSETS : plugins_url( 'assets/rentals/', dirname( __FILE__ ) ) ) . 'guide/guide.css?ver=' . nadlan_re_ver() ) . '">' . "\n";
			echo wp_kses_post( (string) file_get_contents( $gf ) ); // phpcs:ignore
		}
	} else {
		echo '<p class="nlrx-gnote">' . esc_html( $c['guide_note'] ) . '<a href="' . esc_url( nadlan_re_url( 'en' ) ) . '#nlrm-guide" hreflang="en" lang="en">English</a><a href="' . esc_url( nadlan_re_url( 'he' ) ) . '#nlrm-guide" hreflang="he" lang="he">עברית</a></p>';
	}
	?>
	<script type="application/ld+json"><?php
	echo wp_json_encode( array( '@context' => 'https://schema.org', '@type' => 'FAQPage', 'inLanguage' => $lang, 'mainEntity' => array_map( function ( $qa ) {
		return array( '@type' => 'Question', 'name' => $qa[0], 'acceptedAnswer' => array( '@type' => 'Answer', 'text' => $qa[1] ) );
	}, $c['faq'] ) ), JSON_UNESCAPED_UNICODE | JSON_UNESCAPED_SLASHES ); ?></script>
	<script defer src="<?php echo esc_url( nadlan_re_asset( 'earn.js' ) ); ?>"></script>
</div>
		<?php
		get_footer();
	}
}

/* ---------- project pages: the inline opener under the 3D stage ---------- */
add_action( 'wp_footer', function () {
	if ( ! is_singular( 'nadlan_project' ) ) { return; }
	$id = get_queried_object_id(); $p = get_post( $id );
	if ( ! $p || false !== strpos( (string) $p->post_name, 'ashira' ) || false !== strpos( (string) $p->post_name, 'אשירה' ) ) { return; } // owner order 19.10: the Ashira page is not changed
	if ( post_password_required( $id ) ) { return; }
	list( $area, $fallback ) = nadlan_re_city_key( (string) get_post_meta( $id, 'city', true ) );
	$opts = nadlan_re_earn_opts( '', array(
		'area' => $area ? $area : 'israel', 'areaFallback' => (bool) $fallback, 'cityLabel' => (string) get_post_meta( $id, 'city', true ),
		'project' => array( 'slug' => (string) $p->post_name, 'title' => html_entity_decode( get_the_title( $id ), ENT_QUOTES, 'UTF-8' ), 'id' => (int) $id ),
	) );
	unset( $opts['lang'] ); // the sheet follows the page's own <html lang>
	$opts['my'] = home_url( '/my-rentals/' );
	?>
<link rel="stylesheet" href="<?php echo esc_url( nadlan_re_asset( 'earn.css' ) ); ?>" media="print" onload="this.media='all'">
<script>
(function(){
	var O=<?php echo wp_json_encode( $opts, JSON_UNESCAPED_UNICODE | JSON_UNESCAPED_SLASHES ); ?>;
	function go(){
		var stage=document.getElementById('nlps'); if(!stage||document.querySelector('.nlre-open'))return;
		var L=(document.documentElement.lang||'he').slice(0,2).toLowerCase(); if(['he','en','fr','ru','ar'].indexOf(L)<0)L='he';
		O.lang=L; if(L!=='he'){O.my='<?php echo esc_js( home_url( '/my-rentals/' ) ); ?>?lang='+L;}
		function draw(){
			var S=(window.NadlanEarn&&window.NadlanEarn.strings[L])||null; if(!S)return;
			var w=document.createElement('div'); w.className='nlre-open'; w.setAttribute('dir',(L==='he'||L==='ar')?'rtl':'ltr');
			var a=document.createElement('a'); a.href='#'; a.setAttribute('data-nadlan-earn-open',JSON.stringify(O)); a.setAttribute('aria-haspopup','dialog'); a.setAttribute('data-nlre-wired','1');
			a.innerHTML='<span><b></b><small></small><span class="nlre-pickline" hidden></span></span><i>₪</i>';
			a.querySelector('b').textContent=S.open; a.querySelector('small').textContent=S.opensub;
			if(window.__nlpsPick&&(window.__nlpsPick.floor||window.__nlpsPick.unit)){var p=window.__nlpsPick;a.__nlrePick={id:p.unit||'',label:'',floor:p.floorNum!=null?p.floorNum:(p.floor||'')};}
			w.appendChild(a); stage.parentNode.insertBefore(w,stage.nextSibling);
			a.addEventListener('click',function(e){e.preventDefault();var o=JSON.parse(a.getAttribute('data-nadlan-earn-open'));if(a.__nlrePick)o.unit=a.__nlrePick;window.NadlanEarn.open(o);});
			window.addEventListener('nl:facing',function(e){var d=e.detail||{};a.__nlrePick={id:d.unit||'',label:d.label||'',floor:d.floor!=null?d.floor:''};var s=a.querySelector('.nlre-pickline');s.textContent=(d.label||d.unit||'')+(d.floor!=null?' · '+d.floor:'');s.hidden=false;});
		}
		if(window.NadlanEarn){draw();return;}
		var s=document.createElement('script'); s.src='<?php echo esc_js( nadlan_re_asset( 'earn.js' ) ); ?>'; s.defer=true; s.onload=draw; document.body.appendChild(s);
	}
	if(document.readyState==='loading'){document.addEventListener('DOMContentLoaded',go);}else{go();}
})();
</script>
	<?php
}, 60 );
