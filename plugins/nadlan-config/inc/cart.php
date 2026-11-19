<?php
/**
 * nadlan-config - "הסל שלי": one basket for every project and every language, the order summary, the request for proposal
 * (RFP) and the apartment reservation behind a lawyer gate (HAD-796, package 4 of HAD-788; board
 * https://claude.ai/artifact/CWRiuCvoeyxqS1ymeJAhkg; research docs/research/2026-11-19-buying-journey/).
 *
 * The buyer's basket lives in the browser (assets/cart/cart.js, localStorage 'nl-cart:v1'); the server keeps only what the
 * buyer sends: an order (private post type nadlan_cart_order, JSON in post_content, an unguessable token).
 *
 *  - POST /nadlan/v1/cart/order                    the request for proposal from the basket (after POST /nadlan/v1/lead)
 *  - GET  /nadlan/v1/cart/order/<token>            the order's state, as JSON, for the basket
 *  - GET  /nadlan/v1/cart/doc/<token>              the order document (he/en/fr/ru/ar), printable, with the reservation
 *  - POST /nadlan/v1/cart/order/<token>/reserve    the buyer accepts the draft conditions and asks to reserve
 *  - POST /nadlan/v1/cart/order/<token>/approve    a lawyer user (role nadlan_lawyer) approves or returns it
 *  - POST /nadlan/v1/cart/order/<token>/deposit    the deposit, SIMULATION ONLY: no money moves, no provider is called
 *  - wp-admin "בדיקת עורך דין": the lawyer's desk (the queue, the conditions the buyer read, "אני עורך דין ומאשר")
 *
 * The gate: option nadlan_cart_gate = '1' (default). The reservation stops at "waiting for a lawyer" until a user with the
 * capability nadlan_cart_approve (only the role nadlan_lawyer has it; administrators see the queue but cannot approve) ticks
 * the box. With '0' the journey runs to the end as if a lawyer had approved (Ben's simulation, 19.11.2026), and the order
 * records that the gate was off.
 * Money: there is no live charging code. The deposit is recorded as a simulation; option nadlan_cart_deposit_ils (empty by
 * default) only prints the amount the terms will name. A real deposit goes to the developer's escrow and needs Ben's provider,
 * terms and a lawyer; until then nothing here can take money.
 * Honesty: the unit is what the buyer picked on the page (an example apartment: floor, tower, direction) unless the project's
 * own unit list names it, then rooms and area are re-read here; prices are only what the buyer typed, and the purchase tax is
 * recomputed here from the brackets in force; the timeline claims only what happened. The site publishes and passes the
 * request on; it is not a party to the sale and never charges the buyer.
 */
if ( ! defined( 'ABSPATH' ) ) { exit; }

if ( ! function_exists( 'nadlan_cart_on' ) ) {
	function nadlan_cart_on() { return '0' !== (string) get_option( 'nadlan_cart', '1' ); }
}
if ( ! function_exists( 'nadlan_cart_gate_on' ) ) {
	function nadlan_cart_gate_on() { return '0' !== (string) get_option( 'nadlan_cart_gate', '1' ); }
}
if ( ! function_exists( 'nadlan_cart_terms_version' ) ) {
	function nadlan_cart_terms_version() { return 'draft-1 (19.11.2026)'; }
}

/* the project page this request is on: base slug (without -en/-fr/-ru/-ar), its language, and the post */
if ( ! function_exists( 'nadlan_cart_page_project' ) ) {
	function nadlan_cart_page_project() {
		static $memo = false;
		if ( false !== $memo ) { return $memo; }
		$memo = null;
		if ( is_admin() || ! is_singular( 'nadlan_project' ) ) { return $memo; }
		$id = (int) get_queried_object_id();
		if ( ! $id || post_password_required( $id ) || get_post_meta( $id, '_nadlan_private_unit_journey', true ) ) { return $memo; }
		if ( function_exists( 'nadlan_unit_journey_is_private_lab' ) && nadlan_unit_journey_is_private_lab( $id ) ) { return $memo; }
		$slug = (string) get_post_field( 'post_name', $id );
		$lang = 'he';
		$base = $slug;
		if ( preg_match( '/^(.+)-(en|fr|ru|ar)$/', $slug, $m ) ) { $base = $m[1]; $lang = $m[2]; }
		$memo = array( 'id' => $id, 'slug' => $base, 'page_slug' => $slug, 'lang' => $lang );
		return $memo;
	}
}

if ( ! function_exists( 'nadlan_cart_lang' ) ) {
	function nadlan_cart_lang( $l ) {
		$l = substr( strtolower( (string) $l ), 0, 2 );
		return in_array( $l, array( 'he', 'en', 'fr', 'ru', 'ar' ), true ) ? $l : 'he';
	}
}

/* ------------------------------------------------------------------ the words of the order document */
if ( ! function_exists( 'nadlan_cart_words' ) ) {
	function nadlan_cart_words( $lang ) {
		$W = array(
			'he' => array(
				'doc' => 'בקשה להצעה ושריון', 'ref' => 'מספר', 'date' => 'נוצר', 'project' => 'פרויקט', 'developer' => 'יזם', 'unit' => 'הדירה',
				'example' => 'דירה לדוגמה, כפי שנבחרה בדף', 'floor' => 'קומה', 'tower' => 'מגדל', 'facing' => 'פונה ל', 'rooms' => 'חדרים', 'sqm' => 'מ״ר',
				'unit_open' => 'הדירה תיבחר עם היזם', 'design' => 'התכנון שלי', 'finishes' => 'גימורים', 'changes' => 'שינויים', 'notes' => 'הערות לקבלן',
				'design_link' => 'פתיחת התכנון', 'items' => 'ריהוט ופריטים', 'extras' => 'בקשות מהמעצב', 'budget' => 'תקציב לפי המעצב', 'services' => 'שירותים שביקשת', 'none' => 'לא נבחרו',
				'call' => 'שיחה', 'ch_phone' => 'טלפון', 'ch_video' => 'וידאו', 'ch_wa' => 'וואטסאפ', 'price' => 'המחיר שהזנת', 'tax' => 'מס רכישה משוער',
				'b_single' => 'דירה יחידה', 'b_additional' => 'דירה נוספת', 'b_foreign' => 'תושב/ת חוץ', 'rent' => 'השכרה בינתיים',
				'status' => 'מה קרה עד עכשיו', 'st_rfp' => 'הבקשה להצעה נקלטה', 'st_reserve' => 'בקשת השריון נקלטה', 'st_wait' => 'ממתין לבדיקת עורך דין',
				'st_ok' => 'עורך דין אישר', 'st_ok_off' => 'אושר ללא בדיקת עורך דין (שלב לדוגמה)', 'st_returned' => 'עורך הדין החזיר את הבקשה עם הערה',
				'st_dep' => 'פיקדון לדוגמה: לא חויב כסף', 'st_next' => 'היזם והצוות חוזרים אליך', 'reserve' => 'שריון הדירה', 'draft' => 'טיוטה לבדיקת עורך דין',
				'terms' => 'תנאי השריון', 'accept' => 'קראתי את תנאי הטיוטה', 'ask' => 'בקשת שריון', 'deposit' => 'פיקדון שריון', 'sim' => 'לדוגמה בלבד · לא יחויב כסף',
				'amount_tbd' => 'הסכום ייקבע בתנאי השריון של היזם', 'pay_sim' => 'לפיקדון לדוגמה', 'cert' => 'אישור שריון לדוגמה',
				'cert_note' => 'זהו שריון לדוגמה שמראה את הדרך. אין לו תוקף מול היזם ולא חויב כסף, עד שייפתח חיוב אמיתי עם תנאים חתומים.',
				'approved_by' => 'אישר', 'licence' => 'רישיון', 'lawyer_note' => 'הערת עורך הדין', 'wait_note' => 'ברגע שעורך הדין יאשר, הכפתור לפיקדון ייפתח כאן. אפשר לסגור את הדף ולחזור בקישור הזה.',
				'print' => 'הדפסה או שמירה כ-PDF', 'back' => 'חזרה לדף הפרויקט', 'valid' => 'הקישור פרטי, למי שמחזיק בו בלבד',
				'legal' => 'המחיר, המפרט והחוזה נקבעים מול היזם. נדל״ן מפרסמת את הפרויקט ומעבירה את הבקשה ליזם ולאנשי המקצוע שבחרת; היא אינה צד לעסקה ואינה גובה מהקונה דבר. כל תשלום על הדירה, כשיהיה, ישולם ליזם לחשבון הליווי של הפרויקט בלבד.',
				'err' => 'משהו לא עבר. נסו שוב בעוד רגע.', 'sending' => 'שולחים...',
				'svc_mortgage' => 'ייעוץ משכנתא', 'svc_lawyer' => 'עורך דין מקרקעין', 'svc_design' => 'עיצוב פנים', 'svc_inspection' => 'בדק בית ופיקוח', 'svc_moving' => 'הובלה', 'svc_rent' => 'ניהול השכרה',
				'win' => 'בין', 'and' => 'ל־',
			),
			'en' => array(
				'doc' => 'Request for proposal and reservation', 'ref' => 'Reference', 'date' => 'Created', 'project' => 'Project', 'developer' => 'Developer', 'unit' => 'The apartment',
				'example' => 'An example apartment, as picked on the page', 'floor' => 'Floor', 'tower' => 'Tower', 'facing' => 'Facing', 'rooms' => 'rooms', 'sqm' => 'sqm',
				'unit_open' => 'The apartment will be chosen with the developer', 'design' => 'My design', 'finishes' => 'Finishes', 'changes' => 'Changes', 'notes' => 'Notes to the builder',
				'design_link' => 'Open the design', 'items' => 'Furniture and items', 'extras' => 'Requests from the designer', 'budget' => 'Budget from the designer', 'services' => 'Services you asked for', 'none' => 'None chosen',
				'call' => 'Call', 'ch_phone' => 'Phone', 'ch_video' => 'Video', 'ch_wa' => 'WhatsApp', 'price' => 'The price you entered', 'tax' => 'Estimated purchase tax',
				'b_single' => 'Only home', 'b_additional' => 'Additional home', 'b_foreign' => 'Foreign resident', 'rent' => 'Rent it out meanwhile',
				'status' => 'What has happened so far', 'st_rfp' => 'Request for proposal received', 'st_reserve' => 'Reservation request received', 'st_wait' => 'Waiting for a lawyer to review',
				'st_ok' => 'A lawyer approved', 'st_ok_off' => 'Approved without a lawyer review (example run)', 'st_returned' => 'The lawyer returned the request with a note',
				'st_dep' => 'Example deposit: no money charged', 'st_next' => 'The developer and the team get back to you', 'reserve' => 'Reserve the apartment', 'draft' => 'Draft for a lawyer',
				'terms' => 'Reservation conditions', 'accept' => 'I have read the draft conditions', 'ask' => 'Request a reservation', 'deposit' => 'Reservation deposit', 'sim' => 'Example only · no money is charged',
				'amount_tbd' => 'The amount will be set in the developer\'s reservation terms', 'pay_sim' => 'Go to the example deposit', 'cert' => 'Example reservation confirmation',
				'cert_note' => 'This is an example reservation that shows the way. It binds no developer and no money was charged, until real charging opens with signed terms.',
				'approved_by' => 'Approved by', 'licence' => 'Licence', 'lawyer_note' => 'Lawyer\'s note', 'wait_note' => 'Once the lawyer approves, the deposit button opens here. You can close this page and come back with this link.',
				'print' => 'Print or save as PDF', 'back' => 'Back to the project page', 'valid' => 'This link is private, for whoever holds it',
				'legal' => 'Price, specification and contract are set with the developer. NadLan publishes the project and passes your request to the developer and the professionals you chose; it is not a party to the sale and charges the buyer nothing. Any payment for the apartment, when there is one, goes to the developer\'s project escrow account only.',
				'err' => 'Something did not go through. Please try again in a moment.', 'sending' => 'Sending...',
				'svc_mortgage' => 'Mortgage advice', 'svc_lawyer' => 'Real estate lawyer', 'svc_design' => 'Interior design', 'svc_inspection' => 'Inspection and supervision', 'svc_moving' => 'Moving', 'svc_rent' => 'Rental management',
				'win' => 'between', 'and' => 'and',
			),
			'fr' => array(
				'doc' => 'Demande de proposition et réservation', 'ref' => 'Référence', 'date' => 'Créée le', 'project' => 'Projet', 'developer' => 'Promoteur', 'unit' => 'L’appartement',
				'example' => 'Un appartement exemple, tel que choisi sur la page', 'floor' => 'Étage', 'tower' => 'Tour', 'facing' => 'Orienté', 'rooms' => 'pièces', 'sqm' => 'm²',
				'unit_open' => 'L’appartement sera choisi avec le promoteur', 'design' => 'Mon aménagement', 'finishes' => 'Finitions', 'changes' => 'Modifications', 'notes' => 'Notes pour le constructeur',
				'design_link' => 'Ouvrir l’aménagement', 'items' => 'Mobilier et éléments', 'extras' => 'Demandes de l’outil', 'budget' => 'Budget selon le designer', 'services' => 'Services demandés', 'none' => 'Aucun',
				'call' => 'Appel', 'ch_phone' => 'Téléphone', 'ch_video' => 'Vidéo', 'ch_wa' => 'WhatsApp', 'price' => 'Le prix que vous avez saisi', 'tax' => 'Droits d’achat estimés',
				'b_single' => 'Logement unique', 'b_additional' => 'Logement supplémentaire', 'b_foreign' => 'Non-résident', 'rent' => 'Louer en attendant',
				'status' => 'Ce qui s’est passé', 'st_rfp' => 'Demande de proposition reçue', 'st_reserve' => 'Demande de réservation reçue', 'st_wait' => 'En attente de l’avocat',
				'st_ok' => 'Un avocat a approuvé', 'st_ok_off' => 'Approuvé sans avocat (parcours exemple)', 'st_returned' => 'L’avocat a renvoyé la demande avec une note',
				'st_dep' => 'Dépôt exemple : aucun débit', 'st_next' => 'Le promoteur et l’équipe vous recontactent', 'reserve' => 'Réserver l’appartement', 'draft' => 'Projet pour avocat',
				'terms' => 'Conditions de réservation', 'accept' => 'J’ai lu les conditions provisoires', 'ask' => 'Demander la réservation', 'deposit' => 'Dépôt de réservation', 'sim' => 'Exemple uniquement · aucun débit',
				'amount_tbd' => 'Le montant sera fixé dans les conditions du promoteur', 'pay_sim' => 'Vers le dépôt exemple', 'cert' => 'Confirmation de réservation (exemple)',
				'cert_note' => 'Réservation exemple qui montre le parcours. Elle n’engage aucun promoteur et rien n’a été débité, tant qu’un vrai paiement n’est pas ouvert avec des conditions signées.',
				'approved_by' => 'Approuvé par', 'licence' => 'Numéro d’inscription', 'lawyer_note' => 'Note de l’avocat', 'wait_note' => 'Dès que l’avocat approuve, le bouton du dépôt s’ouvre ici. Vous pouvez revenir avec ce lien.',
				'print' => 'Imprimer ou enregistrer en PDF', 'back' => 'Retour à la page du projet', 'valid' => 'Lien privé, pour qui le détient',
				'legal' => 'Prix, descriptif et contrat sont fixés avec le promoteur. NadLan publie le projet et transmet votre demande au promoteur et aux professionnels choisis ; elle n’est pas partie à la vente et ne facture rien à l’acheteur. Tout paiement pour l’appartement ira uniquement sur le compte séquestre du projet.',
				'err' => 'Cela n’a pas abouti. Réessayez dans un instant.', 'sending' => 'Envoi...',
				'svc_mortgage' => 'Conseil en crédit', 'svc_lawyer' => 'Avocat immobilier', 'svc_design' => 'Architecture intérieure', 'svc_inspection' => 'Inspection et suivi', 'svc_moving' => 'Déménagement', 'svc_rent' => 'Gestion locative',
				'win' => 'entre', 'and' => 'et',
			),
			'ru' => array(
				'doc' => 'Запрос предложения и бронирование', 'ref' => 'Номер', 'date' => 'Создан', 'project' => 'Проект', 'developer' => 'Застройщик', 'unit' => 'Квартира',
				'example' => 'Пример квартиры, выбранный на странице', 'floor' => 'Этаж', 'tower' => 'Башня', 'facing' => 'Окна на', 'rooms' => 'комн.', 'sqm' => 'м²',
				'unit_open' => 'Квартира будет выбрана с застройщиком', 'design' => 'Мой проект', 'finishes' => 'Отделка', 'changes' => 'Изменения', 'notes' => 'Заметки для строителя',
				'design_link' => 'Открыть проект', 'items' => 'Мебель и предметы', 'extras' => 'Запросы из дизайнера', 'budget' => 'Бюджет по дизайнеру', 'services' => 'Выбранные услуги', 'none' => 'Не выбраны',
				'call' => 'Звонок', 'ch_phone' => 'Телефон', 'ch_video' => 'Видео', 'ch_wa' => 'WhatsApp', 'price' => 'Введённая вами цена', 'tax' => 'Налог на покупку (оценка)',
				'b_single' => 'Единственное жильё', 'b_additional' => 'Дополнительное жильё', 'b_foreign' => 'Нерезидент', 'rent' => 'Сдать пока в аренду',
				'status' => 'Что уже произошло', 'st_rfp' => 'Запрос предложения получен', 'st_reserve' => 'Запрос на бронь получен', 'st_wait' => 'Ожидает проверки юриста',
				'st_ok' => 'Юрист одобрил', 'st_ok_off' => 'Одобрено без юриста (пробный путь)', 'st_returned' => 'Юрист вернул запрос с замечанием',
				'st_dep' => 'Пробный депозит: деньги не списаны', 'st_next' => 'Застройщик и команда свяжутся с вами', 'reserve' => 'Бронирование квартиры', 'draft' => 'Черновик для юриста',
				'terms' => 'Условия бронирования', 'accept' => 'Я прочитал(а) черновик условий', 'ask' => 'Запросить бронь', 'deposit' => 'Депозит за бронь', 'sim' => 'Только пример · деньги не списываются',
				'amount_tbd' => 'Сумма будет указана в условиях застройщика', 'pay_sim' => 'К пробному депозиту', 'cert' => 'Подтверждение брони (пример)',
				'cert_note' => 'Это пример брони, показывающий путь. Он не обязывает застройщика, деньги не списаны, пока не откроется настоящая оплата с подписанными условиями.',
				'approved_by' => 'Одобрил', 'licence' => 'Лицензия', 'lawyer_note' => 'Замечание юриста', 'wait_note' => 'Как только юрист одобрит, кнопка депозита откроется здесь. Можно вернуться по этой ссылке.',
				'print' => 'Печать или PDF', 'back' => 'К странице проекта', 'valid' => 'Ссылка личная, только для её владельца',
				'legal' => 'Цена, спецификация и договор согласуются с застройщиком. NadLan публикует проект и передаёт ваш запрос застройщику и выбранным специалистам; сайт не является стороной сделки и ничего не берёт с покупателя. Любой платёж за квартиру поступает только на эскроу-счёт проекта.',
				'err' => 'Не получилось. Попробуйте ещё раз через минуту.', 'sending' => 'Отправляем...',
				'svc_mortgage' => 'Ипотечный консультант', 'svc_lawyer' => 'Юрист по недвижимости', 'svc_design' => 'Дизайн интерьера', 'svc_inspection' => 'Технический надзор', 'svc_moving' => 'Переезд', 'svc_rent' => 'Управление арендой',
				'win' => 'с', 'and' => 'до',
			),
			'ar' => array(
				'doc' => 'طلب عرض وحجز', 'ref' => 'الرقم', 'date' => 'أُنشئ', 'project' => 'المشروع', 'developer' => 'المطوّر', 'unit' => 'الشقة',
				'example' => 'شقة نموذجية كما اختيرت في الصفحة', 'floor' => 'الطابق', 'tower' => 'البرج', 'facing' => 'باتجاه', 'rooms' => 'غرف', 'sqm' => 'م²',
				'unit_open' => 'ستُختار الشقة مع المطوّر', 'design' => 'تصميمي', 'finishes' => 'التشطيبات', 'changes' => 'التغييرات', 'notes' => 'ملاحظات للمقاول',
				'design_link' => 'فتح التصميم', 'items' => 'الأثاث والقطع', 'extras' => 'طلبات من المصمم', 'budget' => 'الميزانية حسب المصمم', 'services' => 'الخدمات المطلوبة', 'none' => 'لم يُختر شيء',
				'call' => 'مكالمة', 'ch_phone' => 'هاتف', 'ch_video' => 'فيديو', 'ch_wa' => 'واتساب', 'price' => 'السعر الذي أدخلته', 'tax' => 'ضريبة الشراء التقديرية',
				'b_single' => 'شقة وحيدة', 'b_additional' => 'شقة إضافية', 'b_foreign' => 'مقيم في الخارج', 'rent' => 'تأجيرها مؤقتًا',
				'status' => 'ما حدث حتى الآن', 'st_rfp' => 'تم استلام طلب العرض', 'st_reserve' => 'تم استلام طلب الحجز', 'st_wait' => 'بانتظار مراجعة المحامي',
				'st_ok' => 'وافق محامٍ', 'st_ok_off' => 'تمت الموافقة دون محامٍ (مسار تجريبي)', 'st_returned' => 'أعاد المحامي الطلب مع ملاحظة',
				'st_dep' => 'عربون تجريبي: لم يُخصم أي مبلغ', 'st_next' => 'يتواصل معك المطوّر والفريق', 'reserve' => 'حجز الشقة', 'draft' => 'مسودة للمحامي',
				'terms' => 'شروط الحجز', 'accept' => 'قرأت مسودة الشروط', 'ask' => 'طلب الحجز', 'deposit' => 'عربون الحجز', 'sim' => 'مثال فقط · لن يُخصم أي مبلغ',
				'amount_tbd' => 'يُحدَّد المبلغ في شروط الحجز لدى المطوّر', 'pay_sim' => 'إلى العربون التجريبي', 'cert' => 'تأكيد حجز نموذجي',
				'cert_note' => 'هذا حجز نموذجي يوضح الطريق. لا يُلزم أي مطوّر ولم يُخصم أي مبلغ، إلى أن يُفتح دفع حقيقي بشروط موقّعة.',
				'approved_by' => 'وافق', 'licence' => 'رقم الترخيص', 'lawyer_note' => 'ملاحظة المحامي', 'wait_note' => 'حين يوافق المحامي يُفتح زر العربون هنا. يمكنك العودة عبر هذا الرابط.',
				'print' => 'طباعة أو حفظ PDF', 'back' => 'العودة إلى صفحة المشروع', 'valid' => 'الرابط خاص بمن يحمله فقط',
				'legal' => 'السعر والمواصفات والعقد تُحدَّد مع المطوّر. ينشر NadLan المشروع وينقل طلبك إلى المطوّر والمختصين الذين اخترتهم؛ وليس طرفًا في الصفقة ولا يتقاضى من المشتري شيئًا. أي دفعة عن الشقة، حين تكون، تُدفع لحساب الضمان الخاص بالمشروع فقط.',
				'err' => 'لم ينجح الأمر. حاول مجددًا بعد قليل.', 'sending' => 'جارٍ الإرسال...',
				'svc_mortgage' => 'استشارة رهن عقاري', 'svc_lawyer' => 'محامي عقارات', 'svc_design' => 'تصميم داخلي', 'svc_inspection' => 'فحص وإشراف', 'svc_moving' => 'نقل', 'svc_rent' => 'إدارة التأجير',
				'win' => 'بين', 'and' => 'و',
			),
		);
		return $W[ nadlan_cart_lang( $lang ) ];
	}
}

/* the draft conditions the buyer reads and the lawyer reviews (one version, five languages) */
if ( ! function_exists( 'nadlan_cart_terms' ) ) {
	function nadlan_cart_terms( $lang ) {
		$T = array(
			'he' => array(
				'השריון הוא בקשה ליזם לעכב את הדירה הזו בשבילך לזמן קצוב, לפי תנאי היזם.',
				'הפיקדון, כשיופעל, ישולם ליזם לחשבון הליווי של הפרויקט בלבד, ויוחזר במלואו אם לא ייחתם חוזה בתוך התקופה.',
				'השריון אינו חוזה מכר ואינו מחייב אותך לרכוש.',
				'המחיר והתנאים הסופיים נקבעים בחוזה מול היזם, בליווי עורך הדין שלך.',
				'נדל״ן מעבירה את הבקשה ואינה צד לעסקה; היא אינה מחזיקה בכסף ואינה גובה דבר מהקונה.',
			),
			'en' => array(
				'A reservation asks the developer to hold this apartment for you for a set period, under the developer\'s terms.',
				'The deposit, once it is enabled, is paid to the developer\'s project escrow account only, and is refunded in full if no contract is signed within the period.',
				'A reservation is not a sale contract and does not oblige you to buy.',
				'Final price and terms are set in the contract with the developer, with your own lawyer.',
				'NadLan passes the request on and is not a party to the sale; it holds no money and charges the buyer nothing.',
			),
			'fr' => array(
				'La réservation demande au promoteur de garder cet appartement pour vous pendant une durée fixée, selon ses conditions.',
				'Le dépôt, une fois activé, est versé uniquement sur le compte séquestre du projet, et remboursé en totalité si aucun contrat n’est signé dans le délai.',
				'La réservation n’est pas un contrat de vente et ne vous oblige pas à acheter.',
				'Le prix et les conditions définitifs sont fixés dans le contrat avec le promoteur, avec votre propre avocat.',
				'NadLan transmet la demande et n’est pas partie à la vente ; elle ne détient aucun fonds et ne facture rien à l’acheteur.',
			),
			'ru' => array(
				'Бронь означает просьбу к застройщику удержать эту квартиру для вас на оговорённый срок, по его условиям.',
				'Депозит, когда он будет включён, вносится только на эскроу-счёт проекта и возвращается полностью, если договор не подписан в срок.',
				'Бронь не является договором купли-продажи и не обязывает вас покупать.',
				'Окончательная цена и условия определяются в договоре с застройщиком, с вашим юристом.',
				'NadLan передаёт запрос и не является стороной сделки; сайт не держит деньги и ничего не берёт с покупателя.',
			),
			'ar' => array(
				'الحجز طلب من المطوّر أن يحتفظ بهذه الشقة لك لمدة محددة وفق شروطه.',
				'العربون، حين يُفعَّل، يُدفع لحساب الضمان الخاص بالمشروع فقط، ويُعاد كاملًا إن لم يُوقَّع عقد خلال المدة.',
				'الحجز ليس عقد بيع ولا يُلزمك بالشراء.',
				'السعر والشروط النهائية تُحدَّد في العقد مع المطوّر، بمرافقة محاميك.',
				'ينقل NadLan الطلب وليس طرفًا في الصفقة؛ لا يحتفظ بأي مال ولا يتقاضى من المشتري شيئًا.',
			),
		);
		return $T[ nadlan_cart_lang( $lang ) ];
	}
}

/* ------------------------------------------------------------------ storage */
add_action( 'init', function () {
	register_post_type( 'nadlan_cart_order', array(
		'labels'          => array( 'name' => 'הזמנות מהסל', 'singular_name' => 'הזמנה מהסל' ),
		'public'          => false, 'show_ui' => false, 'show_in_rest' => false, 'rewrite' => false, 'query_var' => false,
		'supports'        => array( 'title' ), 'capability_type' => 'post', 'map_meta_cap' => true,
	) );
	// the lawyer role: reads and approves reservation requests, nothing else (versioned so a later change re-applies)
	if ( '2' !== (string) get_option( 'nadlan_cart_roles_v', '' ) ) {
		remove_role( 'nadlan_lawyer' );
		add_role( 'nadlan_lawyer', 'עורך דין (בדיקת שריון)', array( 'read' => true, 'nadlan_cart_review' => true, 'nadlan_cart_approve' => true ) );
		$adm = get_role( 'administrator' );
		if ( $adm ) { $adm->add_cap( 'nadlan_cart_review' ); $adm->remove_cap( 'nadlan_cart_approve' ); } // administrators see, never approve
		update_option( 'nadlan_cart_roles_v', '2', false );
	}
} );

add_action( 'admin_init', function () {
	foreach ( array( 'nadlan_cart', 'nadlan_cart_gate', 'nadlan_cart_deposit_ils' ) as $o ) {
		register_setting( 'nadlan_cart', $o, array( 'type' => 'string', 'show_in_rest' => true, 'sanitize_callback' => 'sanitize_text_field' ) );
	}
} );
add_action( 'rest_api_init', function () { // the same three options through /wp/v2/settings for the owner's scripts (manage_options only)
	foreach ( array( 'nadlan_cart', 'nadlan_cart_gate', 'nadlan_cart_deposit_ils' ) as $o ) {
		register_setting( 'nadlan_cart', $o, array( 'type' => 'string', 'show_in_rest' => true, 'sanitize_callback' => 'sanitize_text_field' ) );
	}
}, 5 );

if ( ! function_exists( 'nadlan_cart_find' ) ) {
	function nadlan_cart_find( $token ) {
		$token = strtolower( preg_replace( '/[^a-z0-9]/i', '', (string) $token ) );
		if ( strlen( $token ) < 20 ) { return null; }
		$q = get_posts( array( 'post_type' => 'nadlan_cart_order', 'post_status' => 'private', 'numberposts' => 1, 'fields' => 'ids',
			'meta_key' => 'cart_token', 'meta_value' => $token, 'no_found_rows' => true, 'suppress_filters' => true ) );
		if ( ! $q ) { return null; }
		$doc = json_decode( (string) get_post_field( 'post_content', $q[0] ), true );
		return is_array( $doc ) ? array( 'id' => (int) $q[0], 'doc' => $doc ) : null;
	}
}
if ( ! function_exists( 'nadlan_cart_store' ) ) {
	function nadlan_cart_store( $id, $doc ) {
		wp_update_post( array( 'ID' => (int) $id, 'post_content' => wp_slash( wp_json_encode( $doc, JSON_UNESCAPED_UNICODE | JSON_UNESCAPED_SLASHES ) ) ) );
		update_post_meta( (int) $id, 'cart_status', (string) $doc['status'] );
	}
}
if ( ! function_exists( 'nadlan_cart_event' ) ) {
	function nadlan_cart_event( &$doc, $what, $by = 'buyer' ) { $doc['events'][] = array( 'at' => gmdate( 'c' ), 'what' => $what, 'by' => $by ); }
}

/* ------------------------------------------------------------------ cleaning what the browser sends */
if ( ! function_exists( 'nadlan_cart_s' ) ) {
	function nadlan_cart_s( $v, $max = 160 ) { return mb_substr( sanitize_text_field( (string) $v ), 0, $max ); }
}
if ( ! function_exists( 'nadlan_cart_clean_design' ) ) {
	function nadlan_cart_clean_design( $d ) {
		if ( ! is_array( $d ) || 'nadlan-cart-design' !== ( $d['schema'] ?? '' ) ) { return null; }
		$out = array( 'unit_id' => nadlan_cart_s( $d['unit_id'] ?? '', 60 ), 'rooms' => array(), 'finishes' => array(), 'changes' => array(), 'items' => array(), 'extras' => array(), 'notes' => array(), 'budget' => null, 'share_url' => '', 'updated_at' => nadlan_cart_s( $d['updated_at'] ?? '', 40 ) );
		foreach ( array_slice( (array) ( $d['rooms'] ?? array() ), 0, 20 ) as $r ) {
			if ( ! is_array( $r ) ) { continue; }
			$a = isset( $r['area_m2'] ) && is_numeric( $r['area_m2'] ) ? round( (float) $r['area_m2'], 1 ) : null;
			$out['rooms'][] = array( 'name' => nadlan_cart_s( $r['name'] ?? '', 60 ), 'area_m2' => ( $a && $a > 0 && $a < 500 ) ? $a : null );
		}
		foreach ( array_slice( (array) ( $d['extras'] ?? array() ), 0, 12 ) as $r ) { if ( is_string( $r ) && '' !== trim( $r ) ) { $out['extras'][] = nadlan_cart_s( $r, 100 ); } }
		foreach ( array( 'finishes', 'changes', 'items' ) as $k ) {
			foreach ( array_slice( (array) ( $d[ $k ] ?? array() ), 0, 40 ) as $r ) { if ( is_array( $r ) && '' !== trim( (string) ( $r['label'] ?? '' ) ) ) { $out[ $k ][] = nadlan_cart_s( $r['label'], 140 ); } }
		}
		foreach ( array_slice( (array) ( $d['notes'] ?? array() ), 0, 40 ) as $r ) {
			if ( is_array( $r ) && '' !== trim( (string) ( $r['text'] ?? '' ) ) ) { $out['notes'][] = mb_substr( sanitize_textarea_field( (string) $r['text'] ), 0, 500 ); }
		}
		if ( ! empty( $d['budget'] ) && is_array( $d['budget'] ) && isset( $d['budget']['total_ils'] ) && is_numeric( $d['budget']['total_ils'] ) && '' !== trim( (string) ( $d['budget']['source_label'] ?? '' ) ) ) {
			$out['budget'] = array( 'total_ils' => (int) $d['budget']['total_ils'], 'source_label' => nadlan_cart_s( $d['budget']['source_label'], 120 ) );
		} elseif ( ! empty( $d['budget'] ) && is_array( $d['budget'] ) && isset( $d['budget']['min'] ) && is_numeric( $d['budget']['min'] ) && (int) $d['budget']['min'] > 0 ) { // package 2's design order: a range from its catalogue
			$out['budget'] = array( 'min' => (int) $d['budget']['min'], 'max' => isset( $d['budget']['max'] ) && is_numeric( $d['budget']['max'] ) ? (int) $d['budget']['max'] : null );
		}
		$su = esc_url_raw( (string) ( $d['share_url'] ?? '' ) );
		if ( $su && 0 === strpos( $su, home_url( '/' ) ) ) { $out['share_url'] = $su; }
		return ( $out['rooms'] || $out['finishes'] || $out['changes'] || $out['items'] || $out['notes'] || $out['share_url'] ) ? $out : null;
	}
}
if ( ! function_exists( 'nadlan_cart_services' ) ) {
	function nadlan_cart_services() { return array( 'mortgage' => 'mashkanta', 'lawyer' => 'lawyer', 'design' => 'interior_designer', 'inspection' => 'engineer', 'moving' => '', 'rent' => '' ); }
}
if ( ! function_exists( 'nadlan_cart_tax' ) ) {
	function nadlan_cart_tax( $amount, $buyer ) {
		if ( ! function_exists( 'nadlan_purchase_tax_config' ) || $amount <= 0 ) { return null; }
		$cfg = nadlan_purchase_tax_config();
		$br  = (array) ( $cfg[ 'single' === $buyer ? 'single' : 'additional' ] ?? array() );
		$t = 0.0; $prev = 0.0;
		foreach ( $br as $b ) {
			$top = ( null === $b[0] || (float) $b[0] >= PHP_INT_MAX ) ? INF : (float) $b[0];
			if ( $amount > $prev ) { $t += ( min( $amount, $top ) - $prev ) * (float) $b[1]; }
			$prev = $top;
			if ( $amount <= $top ) { break; }
		}
		return (int) round( $t );
	}
}

/* ------------------------------------------------------------------ REST */
if ( ! function_exists( 'nadlan_cart_public' ) ) {
	/** what the basket may see about its order (no lead id, no lawyer user id) */
	function nadlan_cart_public( $doc ) {
		$l = $doc['lawyer'] ?? null;
		return array(
			'ok' => true, 'ref' => $doc['ref'], 'status' => $doc['status'], 'gate' => ! empty( $doc['gate'] ), 'url' => rest_url( 'nadlan/v1/cart/doc/' . $doc['token'] ),
			'events' => $doc['events'], 'lawyer' => $l ? array( 'name' => $l['name'], 'licence' => $l['licence'], 'note' => $l['note'], 'decision' => $l['decision'], 'at' => $l['at'] ) : null,
			'deposit' => $doc['deposit'] ?? null,
		);
	}
}

if ( ! function_exists( 'nadlan_cart_create' ) ) {
	function nadlan_cart_create( WP_REST_Request $req ) {
		if ( ! nadlan_cart_on() ) { return new WP_Error( 'off', 'off', array( 'status' => 403 ) ); }
		$p = $req->get_json_params();
		if ( ! is_array( $p ) ) { return new WP_Error( 'bad_request', 'invalid payload', array( 'status' => 400 ) ); }
		$ip = (string) ( $_SERVER['REMOTE_ADDR'] ?? '0' );
		$rk = 'nadlan_cart_rl_' . md5( $ip );
		$n  = (int) get_transient( $rk );
		if ( $n >= 10 ) { return new WP_Error( 'rate', 'too many', array( 'status' => 429 ) ); }
		set_transient( $rk, $n + 1, HOUR_IN_SECONDS );
		$lang = nadlan_cart_lang( $p['lang'] ?? 'he' );
		$slug = sanitize_title( (string) ( $p['project'] ?? '' ) );
		$post = $slug ? get_page_by_path( $slug, OBJECT, 'nadlan_project' ) : null;
		if ( ! $post || 'publish' !== $post->post_status || '' !== (string) $post->post_password || get_post_meta( $post->ID, '_nadlan_private_unit_journey', true ) ) {
			return new WP_Error( 'not_found', 'project not found', array( 'status' => 404 ) );
		}
		$page = $post; // the language page names the project in the buyer's language
		if ( 'he' !== $lang ) { $lp = get_page_by_path( $slug . '-' . $lang, OBJECT, 'nadlan_project' ); if ( $lp && 'publish' === $lp->post_status ) { $page = $lp; } }
		// the lead this order belongs to: just created by the basket for this project, not linked to another order
		$lid = absint( $p['lead_id'] ?? 0 );
		if ( $lid ) {
			$lp = get_post( $lid );
			$ok = $lp && 'nadlan_lead' === $lp->post_type && 'cart-rfp-v1' === (string) get_post_meta( $lid, 'utm_source', true )
				&& rawurldecode( (string) get_post_meta( $lid, 'project_slug', true ) ) === $slug && ! get_post_meta( $lid, 'cart_order_id', true )
				&& ( time() - (int) get_post_time( 'U', true, $lid ) ) < 900;
			if ( ! $ok ) { $lid = 0; }
		}
		if ( ! $lid ) { return new WP_Error( 'lead_required', 'lead required', array( 'status' => 400 ) ); }
		// the apartment: the page's example apartment, or a unit from the project's own list (facts re-read here)
		$u = is_array( $p['unit'] ?? null ) ? $p['unit'] : array();
		$unit = array( 'floor' => null, 'tower' => '', 'bearing' => null, 'label' => '', 'id' => '', 'rooms' => null, 'sqm' => null, 'example' => true );
		if ( isset( $u['floor'] ) && is_numeric( $u['floor'] ) && (int) $u['floor'] >= 0 && (int) $u['floor'] <= 120 ) { $unit['floor'] = (int) $u['floor']; }
		if ( ! empty( $u['tower'] ) && preg_match( '/^[A-Za-z0-9]{1,4}$/', (string) $u['tower'] ) ) { $unit['tower'] = strtoupper( (string) $u['tower'] ); }
		if ( isset( $u['bearing'] ) && is_numeric( $u['bearing'] ) ) { $unit['bearing'] = ( (int) round( (float) $u['bearing'] ) % 360 + 360 ) % 360; }
		$uid = sanitize_key( (string) ( $u['id'] ?? '' ) );
		if ( $uid ) {
			foreach ( (array) json_decode( (string) get_post_meta( $post->ID, 'project_3d_units', true ), true ) as $x ) {
				if ( is_array( $x ) && isset( $x['id'] ) && sanitize_key( (string) $x['id'] ) === $uid ) {
					$unit['id'] = $uid; $unit['example'] = false;
					$unit['label'] = nadlan_cart_s( $x['label'] ?? '', 60 );
					if ( isset( $x['floor'] ) ) { $unit['floor'] = (int) $x['floor']; }
					$unit['rooms'] = ! empty( $x['rooms'] ) ? (float) $x['rooms'] : null;
					$unit['sqm']   = ! empty( $x['sqm'] ) ? (float) $x['sqm'] : null;
					break;
				}
			}
		}
		$services = array();
		$map = nadlan_cart_services();
		foreach ( (array) ( $p['services'] ?? array() ) as $k => $v ) {
			$k = sanitize_key( (string) $k );
			if ( ! isset( $map[ $k ] ) || empty( $v ) ) { continue; }
			$pro = null;
			$pid = is_array( $v ) ? absint( $v['pro'] ?? 0 ) : 0;
			if ( $pid && 'nadlan_professional' === get_post_type( $pid ) && 'publish' === get_post_status( $pid ) && '' !== $map[ $k ] ) {
				$pro = array( 'id' => $pid, 'name' => function_exists( 'nadlan_prof_person_name' ) ? (string) nadlan_prof_person_name( $pid ) : get_the_title( $pid ), 'url' => get_permalink( $pid ) );
			}
			$services[] = array( 'key' => $k, 'pro' => $pro );
		}
		$rent = null;
		if ( is_array( $p['rent'] ?? null ) && 'nadlan-rent-plan' === ( $p['rent']['schema'] ?? '' ) ) {
			$r = $p['rent'];
			$rent = array( 'service' => in_array( ( $r['service']['id'] ?? '' ), array( 'rent-self', 'rent-managed-quote' ), true ) ? $r['service']['id'] : '', 'label' => nadlan_cart_s( $r['service']['label'] ?? '', 120 ), 'estimate' => null );
			$e = $r['estimate'] ?? null;
			if ( is_array( $e ) && is_numeric( $e['mid'] ?? null ) && '' !== trim( (string) ( $e['source_label'] ?? '' ) ) ) {
				$rent['estimate'] = array( 'low' => (int) ( $e['low'] ?? 0 ), 'mid' => (int) $e['mid'], 'high' => (int) ( $e['high'] ?? 0 ), 'source' => nadlan_cart_s( $e['source_label'], 120 ), 'as_of' => nadlan_cart_s( $e['as_of'] ?? '', 20 ) );
			}
			if ( ! in_array( 'rent', array_column( $services, 'key' ), true ) ) { $services[] = array( 'key' => 'rent', 'pro' => null ); }
		}
		$call = null;
		$c = is_array( $p['call'] ?? null ) ? $p['call'] : array();
		if ( ! empty( $c['day'] ) && preg_match( '/^\d{4}-\d{2}-\d{2}$/', (string) $c['day'] ) && preg_match( '/^(09|12|15|18)$/', (string) ( $c['win'] ?? '' ) ) ) {
			$call = array( 'day' => (string) $c['day'], 'win' => (string) $c['win'], 'ch' => in_array( ( $c['ch'] ?? '' ), array( 'phone', 'video', 'wa' ), true ) ? $c['ch'] : 'phone' );
		}
		$price = null;
		$amt = (int) preg_replace( '/\D/', '', (string) ( $p['price']['amount'] ?? '' ) );
		if ( $amt >= 100000 && $amt <= 500000000 ) {
			$buyer = in_array( ( $p['price']['buyer'] ?? '' ), array( 'single', 'additional', 'foreign' ), true ) ? $p['price']['buyer'] : 'single';
			$price = array( 'amount' => $amt, 'buyer' => $buyer, 'tax' => nadlan_cart_tax( $amt, $buyer ) );
		}
		$token = strtolower( wp_generate_password( 28, false, false ) );
		$ref   = 'NL-' . strtoupper( substr( $token, 0, 4 ) . '-' . substr( $token, 4, 4 ) );
		$doc = array(
			'v' => 1, 'token' => $token, 'ref' => $ref, 'created' => gmdate( 'c' ), 'lang' => $lang, 'status' => 'rfp_sent', 'gate' => nadlan_cart_gate_on(),
			'project' => array( 'id' => $post->ID, 'slug' => $slug, 'name' => get_the_title( $page->ID ), 'city' => (string) get_post_meta( $post->ID, 'city', true ), 'developer' => (string) get_post_meta( $page->ID, 'developer_name', true ), 'url' => get_permalink( $page->ID ) ),
			'unit' => $unit, 'design' => nadlan_cart_clean_design( $p['design'] ?? null ), 'services' => $services, 'rent' => $rent, 'call' => $call, 'price' => $price,
			'buyer' => array( 'first' => nadlan_cart_s( $p['name'] ?? '', 40 ) ), 'lead_id' => $lid, 'events' => array(), 'reserve' => null, 'lawyer' => null, 'deposit' => null,
		);
		nadlan_cart_event( $doc, 'rfp' );
		$oid = wp_insert_post( array( 'post_type' => 'nadlan_cart_order', 'post_status' => 'private', 'post_title' => $ref . ' ' . $slug,
			'post_content' => wp_slash( wp_json_encode( $doc, JSON_UNESCAPED_UNICODE | JSON_UNESCAPED_SLASHES ) ) ), true );
		if ( is_wp_error( $oid ) ) { return $oid; }
		update_post_meta( $oid, 'cart_token', $token );
		update_post_meta( $oid, 'cart_status', 'rfp_sent' );
		update_post_meta( $oid, 'cart_lead_id', $lid );
		update_post_meta( $lid, 'cart_order_id', $oid );
		update_post_meta( $lid, 'cart_order_ref', $ref );
		$adm = get_option( 'admin_email' );
		if ( $adm ) {
			wp_mail( $adm, '[נדלן] בקשה להצעה מהסל ' . $ref . ' - ' . $doc['project']['name'],
				"בקשה להצעה נשלחה מהסל.\n\nמספר: $ref\nפרויקט: " . $doc['project']['name'] . "\nמסמך: " . rest_url( 'nadlan/v1/cart/doc/' . $token ) . "\nהליד: " . admin_url( 'post.php?post=' . $lid . '&action=edit' ) . "\n" );
		}
		return rest_ensure_response( nadlan_cart_public( $doc ) + array( 'token' => $token ) );
	}
}

if ( ! function_exists( 'nadlan_cart_notify_reviewers' ) ) {
	function nadlan_cart_notify_reviewers( $doc ) {
		$to = array();
		foreach ( get_users( array( 'role' => 'nadlan_lawyer', 'fields' => array( 'user_email' ) ) ) as $u ) { if ( is_email( $u->user_email ) ) { $to[] = $u->user_email; } }
		$adm = get_option( 'admin_email' );
		if ( $adm ) { $to[] = $adm; }
		if ( ! $to ) { return; }
		wp_mail( array_unique( $to ), '[נדלן] בקשת שריון ממתינה לבדיקת עורך דין ' . $doc['ref'],
			"בקשת שריון ממתינה לבדיקה.\n\nמספר: " . $doc['ref'] . "\nפרויקט: " . $doc['project']['name'] . "\nשולחן הבדיקה: " . admin_url( 'admin.php?page=nadlan-cart-review&ref=' . rawurlencode( $doc['ref'] ) ) . "\n" );
	}
}

add_filter( 'nadlan_hardening_public_post_routes', function ( $r ) { // the site's generic public-POST limit (inc/final-hardening.php)
	$r[] = '#^/nadlan/v1/cart/order$#';
	$r[] = '#^/nadlan/v1/cart/order/[a-zA-Z0-9]+/(reserve|deposit)$#';
	return $r;
} );

add_action( 'rest_api_init', function () {
	$tok = '(?P<token>[a-zA-Z0-9]{20,40})';
	register_rest_route( 'nadlan/v1', '/cart/order', array( 'methods' => 'POST', 'permission_callback' => '__return_true', 'callback' => 'nadlan_cart_create' ) );
	register_rest_route( 'nadlan/v1', '/cart/order/' . $tok, array( 'methods' => 'GET', 'permission_callback' => '__return_true',
		'callback' => function ( $req ) {
			$o = nadlan_cart_find( $req['token'] );
			return $o ? rest_ensure_response( nadlan_cart_public( $o['doc'] ) ) : new WP_Error( 'not_found', 'not found', array( 'status' => 404 ) );
		},
	) );
	register_rest_route( 'nadlan/v1', '/cart/order/' . $tok . '/reserve', array( 'methods' => 'POST', 'permission_callback' => '__return_true',
		'callback' => function ( $req ) {
			$o = nadlan_cart_find( $req['token'] );
			if ( ! $o ) { return new WP_Error( 'not_found', 'not found', array( 'status' => 404 ) ); }
			$doc = $o['doc'];
			$p   = $req->get_json_params();
			if ( empty( $p['accept'] ) || nadlan_cart_terms_version() !== (string) ( $p['terms'] ?? '' ) ) { return new WP_Error( 'terms', 'accept the current draft conditions', array( 'status' => 400 ) ); }
			if ( ! in_array( $doc['status'], array( 'rfp_sent', 'reserve_returned' ), true ) ) { return rest_ensure_response( nadlan_cart_public( $doc ) ); }
			$doc['reserve'] = array( 'at' => gmdate( 'c' ), 'terms' => nadlan_cart_terms_version(), 'terms_text' => nadlan_cart_terms( $doc['lang'] ) );
			$doc['gate']    = nadlan_cart_gate_on();
			nadlan_cart_event( $doc, 'reserve' );
			if ( $doc['gate'] ) {
				$doc['status'] = 'reserve_review';
				nadlan_cart_store( $o['id'], $doc );
				nadlan_cart_notify_reviewers( $doc );
			} else { // Ben's simulation: the journey runs on as if a lawyer had approved, and says so
				$doc['status'] = 'reserve_approved';
				$doc['lawyer'] = array( 'user' => 0, 'name' => '', 'licence' => '', 'note' => '', 'decision' => 'gate_off', 'at' => gmdate( 'c' ) );
				nadlan_cart_event( $doc, 'approved_gate_off', 'system' );
				nadlan_cart_store( $o['id'], $doc );
			}
			return rest_ensure_response( nadlan_cart_public( $doc ) );
		},
	) );
	register_rest_route( 'nadlan/v1', '/cart/order/' . $tok . '/approve', array( 'methods' => 'POST',
		'permission_callback' => function () { return current_user_can( 'nadlan_cart_approve' ); },
		'callback' => function ( $req ) {
			$o = nadlan_cart_find( $req['token'] );
			if ( ! $o ) { return new WP_Error( 'not_found', 'not found', array( 'status' => 404 ) ); }
			$r = nadlan_cart_decide( $o, $req->get_json_params() ?: array() );
			return is_wp_error( $r ) ? $r : rest_ensure_response( nadlan_cart_public( $r ) );
		},
	) );
	register_rest_route( 'nadlan/v1', '/cart/order/' . $tok . '/deposit', array( 'methods' => 'POST', 'permission_callback' => '__return_true',
		'callback' => function ( $req ) {
			$o = nadlan_cart_find( $req['token'] );
			if ( ! $o ) { return new WP_Error( 'not_found', 'not found', array( 'status' => 404 ) ); }
			$doc = $o['doc'];
			if ( 'reserved_sim' === $doc['status'] ) { return rest_ensure_response( nadlan_cart_public( $doc ) ); }
			if ( 'reserve_approved' !== $doc['status'] ) { return new WP_Error( 'gate', 'waiting for a lawyer', array( 'status' => 409 ) ); }
			// SIMULATION ONLY. No payment provider is called and no live mode exists in this code.
			$amt = (int) preg_replace( '/\D/', '', (string) get_option( 'nadlan_cart_deposit_ils', '' ) );
			$doc['deposit'] = array( 'mode' => 'simulation', 'at' => gmdate( 'c' ), 'amount' => $amt > 0 ? $amt : null, 'charged' => false );
			$doc['status']  = 'reserved_sim';
			nadlan_cart_event( $doc, 'deposit_sim' );
			nadlan_cart_store( $o['id'], $doc );
			return rest_ensure_response( nadlan_cart_public( $doc ) );
		},
	) );
	register_rest_route( 'nadlan/v1', '/cart/doc/' . $tok, array( 'methods' => 'GET', 'permission_callback' => '__return_true', 'callback' => 'nadlan_cart_render' ) );
	// test clean-up for the owner's scripts: removes orders by reference and the leads they made (manage_options only)
	register_rest_route( 'nadlan/v1', '/cart/admin/purge', array( 'methods' => 'POST',
		'permission_callback' => function () { return current_user_can( 'manage_options' ); },
		'callback' => function ( $req ) {
			$out = array();
			foreach ( array_slice( (array) ( $req->get_json_params()['refs'] ?? array() ), 0, 50 ) as $ref ) {
				$ref = preg_replace( '/[^A-Z0-9-]/', '', strtoupper( (string) $ref ) );
				if ( ! preg_match( '/^NL-[A-Z0-9]{4}-[A-Z0-9]{4}$/', $ref ) ) { continue; }
				$q = get_posts( array( 'post_type' => 'nadlan_cart_order', 'post_status' => array( 'private', 'draft', 'publish' ), 'numberposts' => 3, 's' => $ref, 'fields' => 'ids', 'suppress_filters' => true ) );
				$q = array_filter( $q, function ( $oid ) use ( $ref ) { return 0 === strpos( (string) get_the_title( $oid ), $ref . ' ' ); } );
				foreach ( $q as $oid ) {
					$lid = (int) get_post_meta( $oid, 'cart_lead_id', true );
					if ( $lid && 'nadlan_lead' === get_post_type( $lid ) ) { wp_delete_post( $lid, true ); }
					wp_delete_post( $oid, true );
					$out[] = array( 'ref' => $ref, 'order' => $oid, 'lead' => $lid );
				}
			}
			return array( 'ok' => true, 'removed' => $out );
		},
	) );
} );

if ( ! function_exists( 'nadlan_cart_decide' ) ) {
	/** a lawyer's decision (REST or the wp-admin desk): approve, or return with a note */
	function nadlan_cart_decide( $o, $p ) {
		if ( ! current_user_can( 'nadlan_cart_approve' ) ) { return new WP_Error( 'forbidden', 'only a lawyer user can approve', array( 'status' => 403 ) ); }
		$doc = $o['doc'];
		if ( 'reserve_review' !== $doc['status'] ) { return new WP_Error( 'state', 'not waiting for review', array( 'status' => 409 ) ); }
		$approve = 'return' !== (string) ( $p['decision'] ?? 'approve' );
		$lic = nadlan_cart_s( $p['licence'] ?? '', 20 );
		if ( $approve && ( empty( $p['confirm'] ) || '' === $lic ) ) { return new WP_Error( 'confirm', 'tick "אני עורך דין ומאשר" and give a licence number', array( 'status' => 400 ) ); }
		$u = wp_get_current_user();
		$doc['lawyer'] = array( 'user' => (int) $u->ID, 'name' => (string) $u->display_name, 'licence' => $lic, 'note' => mb_substr( sanitize_textarea_field( (string) ( $p['note'] ?? '' ) ), 0, 600 ), 'decision' => $approve ? 'approve' : 'return', 'at' => gmdate( 'c' ) );
		$doc['status'] = $approve ? 'reserve_approved' : 'reserve_returned';
		nadlan_cart_event( $doc, $approve ? 'approved' : 'returned', 'lawyer' );
		nadlan_cart_store( $o['id'], $doc );
		$adm = get_option( 'admin_email' );
		if ( $adm ) { wp_mail( $adm, '[נדלן] ' . ( $approve ? 'עורך דין אישר את ' : 'עורך דין החזיר את ' ) . $doc['ref'], 'מסמך: ' . rest_url( 'nadlan/v1/cart/doc/' . $doc['token'] ) . "\n" ); }
		return $doc;
	}
}

/* ------------------------------------------------------------------ the order document */
if ( ! function_exists( 'nadlan_cart_unit_line' ) ) {
	function nadlan_cart_unit_line( $u, $W, $lang ) {
		$parts = array();
		if ( '' !== (string) ( $u['label'] ?? '' ) ) { $parts[] = $u['label']; }
		if ( null !== ( $u['floor'] ?? null ) ) { $parts[] = $W['floor'] . ' ' . (int) $u['floor']; }
		if ( '' !== (string) ( $u['tower'] ?? '' ) ) { $parts[] = $W['tower'] . ' ' . $u['tower']; }
		if ( null !== ( $u['bearing'] ?? null ) ) {
			$D = array( 'he' => array( 'צפון', 'צפון מזרח', 'מזרח', 'דרום מזרח', 'דרום', 'דרום מערב', 'מערב', 'צפון מערב' ), 'en' => array( 'north', 'north-east', 'east', 'south-east', 'south', 'south-west', 'west', 'north-west' ),
				'fr' => array( 'nord', 'nord-est', 'est', 'sud-est', 'sud', 'sud-ouest', 'ouest', 'nord-ouest' ), 'ru' => array( 'север', 'северо-восток', 'восток', 'юго-восток', 'юг', 'юго-запад', 'запад', 'северо-запад' ),
				'ar' => array( 'الشمال', 'الشمال الشرقي', 'الشرق', 'الجنوب الشرقي', 'الجنوب', 'الجنوب الغربي', 'الغرب', 'الشمال الغربي' ) );
			$parts[] = $W['facing'] . ( 'he' === $lang ? '' : ' ' ) . $D[ $lang ][ (int) round( (int) $u['bearing'] / 45 ) % 8 ];
		}
		if ( ! empty( $u['rooms'] ) ) { $parts[] = rtrim( rtrim( number_format( (float) $u['rooms'], 1 ), '0' ), '.' ) . ' ' . $W['rooms']; }
		if ( ! empty( $u['sqm'] ) ) { $parts[] = (int) $u['sqm'] . ' ' . $W['sqm']; }
		return $parts ? implode( ' · ', $parts ) : $W['unit_open'];
	}
}

if ( ! function_exists( 'nadlan_cart_render' ) ) {
	function nadlan_cart_render( WP_REST_Request $req ) {
		$o = nadlan_cart_find( $req['token'] );
		nocache_headers();
		header( 'Content-Type: text/html; charset=utf-8' );
		header( 'Referrer-Policy: no-referrer' );
		if ( ! $o ) { status_header( 404 ); echo 'Not found'; exit; }
		$doc  = $o['doc'];
		$lang = nadlan_cart_lang( $doc['lang'] ?? 'he' );
		$W    = nadlan_cart_words( $lang );
		$rtl  = in_array( $lang, array( 'he', 'ar' ), true );
		$e    = function ( $s ) { return esc_html( (string) $s ); };
		$loc  = array( 'he' => 'he-IL', 'en' => 'en-GB', 'fr' => 'fr-FR', 'ru' => 'ru-RU', 'ar' => 'en-GB' )[ $lang ];
		$num  = function ( $n ) use ( $lang ) { $s = number_format( (float) $n, 0, '.', 'fr' === $lang || 'ru' === $lang ? ' ' : ',' ); return '<span class="n">₪ ' . $s . '</span>'; };
		$tz   = new DateTimeZone( 'Asia/Jerusalem' );
		$when = function ( $iso ) use ( $tz ) { try { $d = new DateTime( (string) $iso ); $d->setTimezone( $tz ); return $d->format( 'd.m.Y · H:i' ); } catch ( Exception $x ) { return ''; } };
		$st   = (string) $doc['status'];
		$tok  = (string) $doc['token'];
		$api  = esc_url_raw( rest_url( 'nadlan/v1/cart/order/' . $tok ) );
		$fonts = 'https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@500&family=IBM+Plex+Sans+Arabic:wght@400;600;700&family=IBM+Plex+Sans+Hebrew:wght@400;600;700&family=IBM+Plex+Sans:wght@400;600;700&display=swap';
		$rows = function ( $k, $v ) { return '<div class="ln"><span class="k">' . $k . '</span><span class="v">' . $v . '</span></div>'; };

		$html  = '<!doctype html><html lang="' . $lang . '" dir="' . ( $rtl ? 'rtl' : 'ltr' ) . '"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">';
		$html .= '<title>' . $e( $doc['ref'] . ' · ' . $W['doc'] ) . '</title><link rel="stylesheet" href="' . esc_url( $fonts ) . '">';
		$html .= '<style>:root{--paper:#fff;--table:#E9EDF2;--sheet:#F4F6F9;--ink:#0F2438;--ink2:#43566B;--rule:#C7D0DA;--ok:#0A7D5A;--okbg:#E3F3EC;--draft:#B3122E;--draftbg:#FBE8EB;--focus:#2B6FD8}'
			. '*{box-sizing:border-box}body{margin:0;background:var(--table);color:var(--ink);font:15px/1.55 "IBM Plex Sans Hebrew","IBM Plex Sans","IBM Plex Sans Arabic",Arial,sans-serif}'
			. '.w{max-width:760px;margin:0 auto;padding:20px max(16px,env(safe-area-inset-left)) 60px}.doc{background:var(--paper);border:1px solid var(--rule);border-radius:12px;overflow:hidden}'
			. '.hd{background:var(--ink);color:#fff;padding:18px 20px;display:flex;flex-wrap:wrap;justify-content:space-between;gap:10px;align-items:flex-end}.hd h1{margin:0;font-size:22px;line-height:1.25}.hd small{opacity:.8}'
			. '.ref{font-family:"IBM Plex Mono",monospace;font-size:20px;letter-spacing:.04em;direction:ltr;unicode-bidi:isolate}'
			. 'section{padding:16px 20px;border-top:1px solid var(--rule)}h2{margin:0 0 8px;font-size:16px}.ln{display:grid;grid-template-columns:130px 1fr;gap:10px;padding:6px 0;border-top:1px dashed var(--rule)}.ln:first-of-type{border-top:0}.k{color:var(--ink2);font-size:13px}.v{min-width:0}'
			. '@media(max-width:520px){.ln{grid-template-columns:1fr;gap:2px}}ul{margin:4px 0 0;padding-inline-start:20px}.n{font-variant-numeric:tabular-nums;direction:ltr;unicode-bidi:isolate}'
			. '.tl{display:grid;gap:8px}.tl div{display:flex;gap:10px;align-items:flex-start}.dot{flex:none;width:12px;height:12px;border-radius:50%;border:2px solid var(--rule);margin-top:5px}.dot.ok{background:var(--ok);border-color:var(--ok)}.dot.wait{border-color:var(--ink);box-shadow:0 0 0 4px var(--sheet)}'
			. '.stamp{display:inline-block;transform:rotate(-2deg);border:2px solid currentColor;border-radius:4px;padding:2px 9px;font-weight:700;font-size:13px}.stamp.dr{color:var(--draft);background:var(--draftbg)}.stamp.ok{color:var(--ok);background:var(--okbg)}'
			. 'ol{margin:6px 0 0;padding-inline-start:20px;display:grid;gap:6px;font-size:14px}.dep{border:1.5px dashed var(--ink);border-radius:10px;padding:12px;display:grid;gap:6px;margin-top:12px}'
			. '.ck{display:flex;gap:10px;align-items:flex-start;margin:12px 0;font-size:14px}.ck input{width:22px;height:22px;flex:none;margin:0;accent-color:#0F2438}'
			. 'button,.btn{display:inline-flex;justify-content:center;align-items:center;min-height:48px;padding:0 18px;border-radius:8px;font:700 15px/1 inherit;font-family:inherit;background:var(--ink);color:#fff;border:0;cursor:pointer;text-decoration:none;width:100%}'
			. 'button[disabled]{opacity:.35;cursor:not-allowed}.btn2{background:var(--paper);color:var(--ink);border:1.5px solid var(--ink)}button:focus-visible,a:focus-visible,input:focus-visible{outline:3px solid var(--focus);outline-offset:2px}'
			. '.note{background:var(--sheet);border-radius:8px;padding:10px 12px;font-size:13px;color:var(--ink2)}.acts{display:grid;gap:8px;grid-template-columns:1fr 1fr}@media(max-width:520px){.acts{grid-template-columns:1fr}}.err{color:var(--draft);font-size:13px;min-height:1em}'
			. 'a{color:var(--ink)}@media print{body{background:#fff}.w{padding:0}.noprint{display:none!important}.doc{border:0}}</style></head><body><div class="w"><article class="doc">';
		$html .= '<header class="hd"><div><small>' . $e( $W['doc'] ) . '</small><h1>' . $e( $doc['project']['name'] ) . '</h1><small>' . $e( trim( $doc['project']['city'] . ( $doc['project']['developer'] ? ' · ' . $W['developer'] . ': ' . $doc['project']['developer'] : '' ) ) ) . '</small></div>'
			. '<div><div class="ref">' . $e( $doc['ref'] ) . '</div><small>' . $e( $W['date'] ) . ' ' . $e( $when( $doc['created'] ) ) . '</small></div></header>';
		// the apartment
		$html .= '<section><h2>' . $e( $W['unit'] ) . '</h2><div>' . $e( nadlan_cart_unit_line( $doc['unit'], $W, $lang ) ) . '</div>' . ( ! empty( $doc['unit']['example'] ) && null !== $doc['unit']['floor'] ? '<div class="k">' . $e( $W['example'] ) . '</div>' : '' ) . '</section>';
		// the design
		if ( ! empty( $doc['design'] ) ) {
			$d = $doc['design'];
			$h = '';
			if ( $d['rooms'] ) { $h .= $rows( $e( $W['rooms'] ), $e( implode( ', ', array_map( function ( $r ) { return $r['name'] . ( $r['area_m2'] ? ' ' . $r['area_m2'] : '' ); }, $d['rooms'] ) ) ) ); }
			if ( $d['finishes'] ) { $h .= $rows( $e( $W['finishes'] ), $e( implode( ' · ', $d['finishes'] ) ) ); }
			if ( $d['changes'] ) { $h .= $rows( $e( $W['changes'] ), '<ul><li>' . implode( '</li><li>', array_map( 'esc_html', $d['changes'] ) ) . '</li></ul>' ); }
			if ( $d['notes'] ) { $h .= $rows( $e( $W['notes'] ), '<ul><li>' . implode( '</li><li>', array_map( 'esc_html', $d['notes'] ) ) . '</li></ul>' ); }
			if ( ! empty( $d['items'] ) ) { $h .= $rows( $e( $W['items'] ), $e( implode( ' · ', $d['items'] ) ) ); }
			if ( ! empty( $d['extras'] ) ) { $h .= $rows( $e( $W['extras'] ), $e( implode( ' · ', $d['extras'] ) ) ); }
			if ( $d['budget'] && isset( $d['budget']['total_ils'] ) ) { $h .= $rows( $e( $W['budget'] ), $num( $d['budget']['total_ils'] ) . ' <span class="k">(' . $e( $d['budget']['source_label'] ) . ')</span>' ); }
			elseif ( $d['budget'] && isset( $d['budget']['min'] ) ) { $h .= $rows( $e( $W['budget'] ), $num( $d['budget']['min'] ) . ( $d['budget']['max'] ? ' - ' . $num( $d['budget']['max'] ) : '+' ) ); }
			if ( $d['share_url'] ) { $h .= $rows( '', '<a href="' . esc_url( $d['share_url'] ) . '">' . $e( $W['design_link'] ) . '</a>' ); }
			$html .= '<section><h2>' . $e( $W['design'] ) . '</h2>' . $h . '</section>';
		}
		// services, rent, call, price
		$sv = array();
		foreach ( $doc['services'] as $s ) { $sv[] = $e( $W[ 'svc_' . $s['key'] ] ?? $s['key'] ) . ( $s['pro'] ? ' · <a href="' . esc_url( $s['pro']['url'] ) . '">' . $e( $s['pro']['name'] ) . '</a>' : '' ); }
		$html .= '<section><h2>' . $e( $W['services'] ) . '</h2>' . ( $sv ? '<ul><li>' . implode( '</li><li>', $sv ) . '</li></ul>' : '<div class="k">' . $e( $W['none'] ) . '</div>' );
		if ( ! empty( $doc['rent'] ) ) {
			$r = $doc['rent'];
			$html .= $rows( $e( $W['rent'] ), $e( $r['label'] ) . ( $r['estimate'] ? ' · ' . $num( $r['estimate']['low'] ) . ' - ' . $num( $r['estimate']['high'] ) . ' <span class="k">(' . $e( $r['estimate']['source'] . ' ' . $r['estimate']['as_of'] ) . ')</span>' : '' ) );
		}
		if ( ! empty( $doc['call'] ) ) {
			$c = $doc['call'];
			try { $dd = new DateTime( $c['day'] . ' 12:00', $tz ); $day = $dd->format( 'd.m.Y' ); } catch ( Exception $x ) { $day = $c['day']; }
			$html .= $rows( $e( $W['call'] ), $e( $day . ' · ' . $W['win'] . ' ' . $c['win'] . ':00 ' . $W['and'] . ( (int) $c['win'] + 3 ) . ':00 · ' . $W[ 'ch_' . $c['ch'] ] ) );
		}
		if ( ! empty( $doc['price'] ) ) {
			$pr = $doc['price'];
			$html .= $rows( $e( $W['price'] ), $num( $pr['amount'] ) . ' <span class="k">' . $e( $W[ 'b_' . $pr['buyer'] ] ) . '</span>' );
			if ( null !== $pr['tax'] ) { $html .= $rows( $e( $W['tax'] ), $num( $pr['tax'] ) ); }
		}
		$html .= '</section>';
		// the timeline: only what happened
		$tl = array();
		foreach ( $doc['events'] as $ev ) {
			$lab = array( 'rfp' => $W['st_rfp'], 'reserve' => $W['st_reserve'], 'approved' => $W['st_ok'], 'approved_gate_off' => $W['st_ok_off'], 'returned' => $W['st_returned'], 'deposit_sim' => $W['st_dep'] )[ $ev['what'] ] ?? '';
			if ( $lab ) { $tl[] = '<div><span class="dot ok"></span><span>' . $e( $lab ) . ' <span class="k">' . $e( $when( $ev['at'] ) ) . '</span></span></div>'; }
		}
		if ( 'reserve_review' === $st ) { $tl[] = '<div><span class="dot wait"></span><span><b>' . $e( $W['st_wait'] ) . '</b></span></div>'; }
		if ( 'rfp_sent' === $st ) { $tl[] = '<div><span class="dot wait"></span><span>' . $e( $W['st_next'] ) . '</span></div>'; }
		$html .= '<section><h2>' . $e( $W['status'] ) . '</h2><div class="tl">' . implode( '', $tl ) . '</div>';
		if ( ! empty( $doc['lawyer'] ) && 'gate_off' !== $doc['lawyer']['decision'] ) {
			$l = $doc['lawyer'];
			$html .= '<div class="note" style="margin-top:10px">' . $e( $W['approved_by'] ) . ': ' . $e( $l['name'] ) . ' · ' . $e( $W['licence'] ) . ' <span class="n">' . $e( $l['licence'] ) . '</span>' . ( $l['note'] ? '<br>' . $e( $W['lawyer_note'] ) . ': ' . $e( $l['note'] ) : '' ) . '</div>';
		}
		$html .= '</section>';
		// the reservation
		$html .= '<section id="reserve"><h2>' . $e( 'reserved_sim' === $st ? $W['cert'] : $W['reserve'] ) . '</h2>';
		if ( 'reserved_sim' === $st ) {
			$html .= '<p><span class="stamp ok">' . $e( ( $doc['lawyer']['decision'] ?? '' ) === 'gate_off' ? $W['st_ok_off'] : $W['st_ok'] ) . '</span> <span class="stamp dr">' . $e( $W['sim'] ) . '</span></p>';
			$html .= $rows( $e( $W['deposit'] ), $doc['deposit']['amount'] ? $num( $doc['deposit']['amount'] ) . ' · ' . $e( $W['sim'] ) : $e( $W['amount_tbd'] . ' · ' . $W['sim'] ) );
			$html .= '<p class="note">' . $e( $W['cert_note'] ) . '</p>';
		} else {
			$terms = ! empty( $doc['reserve']['terms_text'] ) ? $doc['reserve']['terms_text'] : nadlan_cart_terms( $lang );
			$html .= '<p><span class="stamp dr">' . $e( $W['draft'] ) . '</span> <span class="k">' . $e( $W['terms'] . ' · ' . nadlan_cart_terms_version() ) . '</span></p><ol>';
			foreach ( $terms as $t ) { $html .= '<li>' . $e( $t ) . '</li>'; }
			$html .= '</ol>';
			$amt = (int) preg_replace( '/\D/', '', (string) get_option( 'nadlan_cart_deposit_ils', '' ) );
			$html .= '<div class="dep"><span class="stamp dr" style="justify-self:start">' . $e( $W['sim'] ) . '</span><b>' . $e( $W['deposit'] ) . '</b><span>' . ( $amt > 0 ? $num( $amt ) : $e( $W['amount_tbd'] ) ) . '</span></div>';
			if ( in_array( $st, array( 'rfp_sent', 'reserve_returned' ), true ) ) {
				$html .= '<div class="noprint"><label class="ck"><input type="checkbox" id="nlc-accept"><span>' . $e( $W['accept'] ) . '</span></label><button type="button" id="nlc-reserve" disabled>' . $e( $W['ask'] ) . '</button></div>';
			} elseif ( 'reserve_review' === $st ) {
				$html .= '<p class="note">' . $e( $W['wait_note'] ) . '</p><button type="button" disabled class="noprint">' . $e( $W['pay_sim'] ) . '</button>';
			} elseif ( 'reserve_approved' === $st ) {
				$html .= '<div class="noprint" style="margin-top:12px"><button type="button" id="nlc-deposit">' . $e( $W['pay_sim'] ) . '</button></div>';
			}
		}
		$html .= '<p class="err noprint" id="nlc-err" role="status" aria-live="polite"></p></section>';
		$html .= '<section><p class="note">' . $e( $W['legal'] ) . '</p><p class="k">' . $e( $W['valid'] ) . '</p></section></article>';
		$html .= '<div class="acts noprint" style="margin-top:14px"><button type="button" class="btn2" onclick="window.print()">' . $e( $W['print'] ) . '</button><a class="btn btn2" href="' . esc_url( $doc['project']['url'] ) . '">' . $e( $W['back'] ) . '</a></div></div>';
		$cfg = array( 'api' => $api, 'terms' => nadlan_cart_terms_version(), 'err' => $W['err'], 'sending' => $W['sending'], 'project' => $doc['project']['slug'], 'status' => $st );
		$html .= '<script>(function(){var C=' . wp_json_encode( $cfg, JSON_UNESCAPED_UNICODE | JSON_UNESCAPED_SLASHES ) . ';'
			. 'var $=function(i){return document.getElementById(i)},er=$("nlc-err");'
			. 'function post(path,body,btn){var t=btn.textContent;btn.disabled=true;btn.textContent=C.sending;er.textContent="";'
			. 'fetch(C.api+path,{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify(body)}).then(function(r){if(!r.ok)throw r;return r.json()}).then(function(){location.reload()})'
			. '.catch(function(){btn.disabled=false;btn.textContent=t;er.textContent=C.err})}'
			. 'var a=$("nlc-accept"),r=$("nlc-reserve"),d=$("nlc-deposit");'
			. 'if(a&&r){a.addEventListener("change",function(){r.disabled=!a.checked});r.addEventListener("click",function(){if(window.nlTrack)try{nlTrack("reserve_request",{project:C.project})}catch(e){}post("/reserve",{accept:true,terms:C.terms},r)})}'
			. 'if(d){d.addEventListener("click",function(){post("/deposit",{simulate:true},d)})}'
			. 'if(C.status==="reserve_review"){setInterval(function(){fetch(C.api).then(function(r){return r.json()}).then(function(j){if(j&&j.status!==C.status)location.reload()}).catch(function(){})},20000)}'
			. 'if(location.hash==="#reserve"){var s=$("reserve");if(s)s.scrollIntoView()}})();</script></body></html>';
		echo $html; // phpcs:ignore WordPress.Security.EscapeOutput -- built from escaped parts above
		exit;
	}
}

/* ------------------------------------------------------------------ the lawyer's desk in wp-admin */
add_action( 'admin_menu', function () {
	add_menu_page( 'בדיקת עורך דין', 'בדיקת עורך דין', 'nadlan_cart_review', 'nadlan-cart-review', 'nadlan_cart_desk', 'dashicons-yes-alt', 27 );
} );
add_action( 'admin_post_nadlan_cart_decide', function () {
	if ( ! current_user_can( 'nadlan_cart_approve' ) ) { wp_die( 'רק משתמש עורך דין יכול לאשר.', 403 ); }
	check_admin_referer( 'nadlan_cart_decide' );
	$tok = sanitize_text_field( wp_unslash( $_POST['token'] ?? '' ) );
	$o   = nadlan_cart_find( $tok );
	$r   = $o ? nadlan_cart_decide( $o, array( 'decision' => sanitize_key( wp_unslash( $_POST['decision'] ?? 'approve' ) ), 'confirm' => ! empty( $_POST['confirm'] ),
		'licence' => wp_unslash( $_POST['licence'] ?? '' ), 'note' => wp_unslash( $_POST['note'] ?? '' ) ) ) : new WP_Error( 'nf', 'not found' );
	$msg = is_wp_error( $r ) ? 'err' : 'ok';
	wp_safe_redirect( admin_url( 'admin.php?page=nadlan-cart-review&m=' . $msg ) );
	exit;
} );
if ( ! function_exists( 'nadlan_cart_desk' ) ) {
	function nadlan_cart_desk() {
		if ( ! current_user_can( 'nadlan_cart_review' ) ) { return; }
		$can = current_user_can( 'nadlan_cart_approve' );
		$ids = get_posts( array( 'post_type' => 'nadlan_cart_order', 'post_status' => 'private', 'numberposts' => 40, 'fields' => 'ids', 'meta_key' => 'cart_status',
			'meta_value' => array( 'reserve_review', 'reserve_approved', 'reserve_returned', 'reserved_sim' ), 'meta_compare' => 'IN', 'orderby' => 'date', 'order' => 'DESC', 'suppress_filters' => true ) );
		$sel = sanitize_text_field( wp_unslash( $_GET['ref'] ?? '' ) ); // phpcs:ignore WordPress.Security.NonceVerification
		echo '<div class="wrap" style="direction:rtl;font-family:\'IBM Plex Sans Hebrew\',Arial,sans-serif;max-width:980px"><h1>בדיקת עורך דין: בקשות שריון</h1>';
		$m = sanitize_key( wp_unslash( $_GET['m'] ?? '' ) ); // phpcs:ignore WordPress.Security.NonceVerification
		if ( 'ok' === $m ) { echo '<div class="notice notice-success"><p>ההחלטה נרשמה.</p></div>'; }
		if ( 'err' === $m ) { echo '<div class="notice notice-error"><p>לא נרשם: יש לסמן "אני עורך דין ומאשר" ולמלא מספר רישיון.</p></div>'; }
		echo '<p style="color:#43566B">' . ( $can ? 'אישור נרשם עם שם המשתמש שלך, מספר הרישיון והשעה. התנאים הם טיוטה (' . esc_html( nadlan_cart_terms_version() ) . ').' : 'מנהל האתר רואה את התור אבל אינו יכול לאשר. אישור נעשה רק על ידי משתמש בתפקיד עורך דין.' ) . '</p>';
		if ( ! $ids ) { echo '<p>אין בקשות שריון כרגע.</p></div>'; return; }
		$names = array( 'reserve_review' => 'ממתין לבדיקה', 'reserve_approved' => 'אושר', 'reserve_returned' => 'הוחזר לקונה', 'reserved_sim' => 'שריון לדוגמה הושלם' );
		foreach ( $ids as $oid ) {
			$doc = json_decode( (string) get_post_field( 'post_content', $oid ), true );
			if ( ! is_array( $doc ) ) { continue; }
			$W = nadlan_cart_words( 'he' );
			$open = 'reserve_review' === $doc['status'] || $sel === $doc['ref'];
			echo '<details style="background:#fff;border:1px solid #C7D0DA;border-radius:8px;margin:10px 0;padding:0"' . ( $open ? ' open' : '' ) . '><summary style="padding:12px 14px;cursor:pointer;font-size:14px"><b style="font-family:monospace">' . esc_html( $doc['ref'] ) . '</b> · ' . esc_html( $doc['project']['name'] ) . ' · ' . esc_html( nadlan_cart_unit_line( $doc['unit'], $W, 'he' ) ) . ' · <b>' . esc_html( $names[ $doc['status'] ] ?? $doc['status'] ) . '</b></summary><div style="padding:0 14px 14px">';
			echo '<p>קונה: ' . esc_html( $doc['buyer']['first'] ) . ' · שפת הבקשה: ' . esc_html( $doc['lang'] ) . ' · <a href="' . esc_url( rest_url( 'nadlan/v1/cart/doc/' . $doc['token'] ) ) . '" target="_blank" rel="noopener">המסמך המלא כפי שהקונה רואה</a> · <a href="' . esc_url( admin_url( 'post.php?post=' . (int) $doc['lead_id'] . '&action=edit' ) ) . '">הליד</a></p>';
			echo '<p><b>התנאים שהקונה קרא (' . esc_html( $doc['reserve']['terms'] ?? '' ) . '):</b></p><ol>';
			foreach ( (array) ( $doc['reserve']['terms_text'] ?? array() ) as $t ) { echo '<li>' . esc_html( $t ) . '</li>'; }
			echo '</ol>';
			if ( ! empty( $doc['lawyer'] ) ) { echo '<p>החלטה: ' . esc_html( $doc['lawyer']['decision'] ) . ' · ' . esc_html( $doc['lawyer']['name'] ) . ' · רישיון ' . esc_html( $doc['lawyer']['licence'] ) . '</p>'; }
			if ( $can && 'reserve_review' === $doc['status'] ) {
				echo '<form method="post" action="' . esc_url( admin_url( 'admin-post.php' ) ) . '" style="display:grid;gap:10px;max-width:520px">';
				wp_nonce_field( 'nadlan_cart_decide' );
				echo '<input type="hidden" name="action" value="nadlan_cart_decide"><input type="hidden" name="token" value="' . esc_attr( $doc['token'] ) . '">';
				echo '<label>מספר רישיון<br><input type="text" name="licence" inputmode="numeric" style="width:200px"></label>';
				echo '<label>הערה לקונה (לא חובה)<br><textarea name="note" rows="2" style="width:100%"></textarea></label>';
				echo '<label style="font-size:15px"><input type="checkbox" name="confirm" value="1"> <b>אני עורך דין ומאשר</b> את המשך התהליך לבקשה הזו</label>';
				echo '<p style="display:flex;gap:8px"><button class="button button-primary" name="decision" value="approve">אישור</button><button class="button" name="decision" value="return">החזרה לקונה עם הערה</button></p></form>';
			}
			echo '</div></details>';
		}
		echo '</div>';
	}
}

/* ------------------------------------------------------------------ the basket on the page */
add_action( 'wp_enqueue_scripts', function () {
	if ( ! nadlan_cart_on() || is_admin() ) { return; }
	$v = defined( 'NADLAN_CONFIG_VERSION' ) ? NADLAN_CONFIG_VERSION : '1';
	if ( nadlan_cart_page_project() ) {
		wp_enqueue_style( 'nadlan-cart', plugins_url( 'assets/cart/cart.css', dirname( __FILE__ ) ), array(), $v );
		wp_enqueue_script( 'nadlan-cart', plugins_url( 'assets/cart/cart.js', dirname( __FILE__ ) ), array(), $v, array( 'in_footer' => true, 'strategy' => 'defer' ) );
	}
}, 31 );

add_action( 'wp_footer', function () {
	if ( ! nadlan_cart_on() || is_admin() || is_feed() ) { return; }
	$pp = nadlan_cart_page_project();
	$v  = defined( 'NADLAN_CONFIG_VERSION' ) ? NADLAN_CONFIG_VERSION : '1';
	$lang = $pp ? $pp['lang'] : ( function_exists( 'nadlan_current_lang' ) ? nadlan_cart_lang( nadlan_current_lang() ) : 'he' );
	$tax = function_exists( 'nadlan_purchase_tax_config' ) ? nadlan_purchase_tax_config() : array();
	foreach ( array( 'single', 'additional' ) as $k ) {
		foreach ( (array) ( $tax[ $k ] ?? array() ) as $i => $b ) { if ( (float) $b[0] >= PHP_INT_MAX ) { $tax[ $k ][ $i ][0] = null; } }
	}
	$cfg = array(
		'v' => $v, 'lang' => $lang, 'rest' => esc_url_raw( rest_url( 'nadlan/v1/' ) ), 'gate' => nadlan_cart_gate_on(),
		'privacy' => esc_url_raw( get_permalink( 396 ) ?: home_url( '/' ) ), 'mortgage' => esc_url_raw( home_url( '/mortgage-calculator/' ) ),
		'rentals' => esc_url_raw( home_url( '/my-rentals/' ) ), 'pros' => esc_url_raw( home_url( '/professionals/' ) ),
		'designer' => esc_url_raw( home_url( '/tour/designer/' ) ),
		'wa' => function_exists( 'nadlan_cta_whatsapp_number' ) ? preg_replace( '/\D/', '', (string) nadlan_cta_whatsapp_number() ) : '',
		'tax' => array( 'single' => $tax['single'] ?? array(), 'additional' => $tax['additional'] ?? array() ),
		'deposit' => (int) preg_replace( '/\D/', '', (string) get_option( 'nadlan_cart_deposit_ils', '' ) ),
		'terms' => nadlan_cart_terms_version(),
	);
	if ( $pp ) {
		$id  = $pp['id'];
		$ps  = function_exists( 'nadlan_ps_current' ) ? nadlan_ps_current() : null;
		$sec = array();
		foreach ( (array) ( $ps['sectors'] ?? array() ) as $s ) { if ( 'he' === $pp['lang'] ) { $sec[] = array( (float) $s[0], (float) $s[1], (string) $s[2] ); } }
		$img = get_the_post_thumbnail_url( $id, 'medium' );
		if ( ! $img && 'he' !== $pp['lang'] ) { $hp = get_page_by_path( $pp['slug'], OBJECT, 'nadlan_project' ); if ( $hp ) { $img = get_the_post_thumbnail_url( $hp->ID, 'medium' ); } }
		$cfg['project'] = array(
			'slug' => $pp['slug'], 'id' => $id, 'name' => html_entity_decode( get_the_title( $id ), ENT_QUOTES, 'UTF-8' ), 'city' => (string) get_post_meta( $id, 'city', true ),
			'url' => get_permalink( $id ), 'img' => $img ? esc_url_raw( $img ) : '', 'sectors' => $sec,
			'hint' => 'he' === $pp['lang'] ? (string) ( $ps['basket_hint'] ?? '' ) : '',
			'engine' => function_exists( 'nadlan_project_mode' ) && 'showroom' === nadlan_project_mode( $id ),
		);
		$cfg['team'] = function_exists( 'nadlan_bk_team' ) ? array_map( function ( $t ) { return $t[0]; }, nadlan_bk_team() ) : array();
		echo '<script type="application/json" id="nadlan-cart-cfg">' . wp_json_encode( $cfg, JSON_UNESCAPED_UNICODE | JSON_UNESCAPED_SLASHES ) . '</script>' . "\n";
		return;
	}
	// every other page: the basket follows the buyer (a small chip), loaded only when this browser already holds a basket
	$js  = esc_url_raw( plugins_url( 'assets/cart/cart.js', dirname( __FILE__ ) ) . '?ver=' . $v );
	$css = esc_url_raw( plugins_url( 'assets/cart/cart.css', dirname( __FILE__ ) ) . '?ver=' . $v );
	echo '<script type="application/json" id="nadlan-cart-cfg">' . wp_json_encode( $cfg, JSON_UNESCAPED_UNICODE | JSON_UNESCAPED_SLASHES ) . '</script>'
		. '<script>(function(){try{var s=JSON.parse(localStorage.getItem("nl-cart:v1")||"null");if(!s||!s.projects||!Object.keys(s.projects).length)return}catch(e){return}'
		. 'var l=document.createElement("link");l.rel="stylesheet";l.href=' . wp_json_encode( $css ) . ';document.head.appendChild(l);'
		. 'var j=document.createElement("script");j.src=' . wp_json_encode( $js ) . ';j.defer=true;document.body.appendChild(j)})();</script>' . "\n";
}, 41 );
