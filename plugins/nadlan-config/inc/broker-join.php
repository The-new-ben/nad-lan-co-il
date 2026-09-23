<?php
/**
 * nadlan-config · Brokers join alone (x-broker-join) · v1.0.0 · 23.9.2026
 *
 * Owner order 23.9.2026: "every broker joins alone": a form on the brokers page opens the broker's record and a
 * basic site and hands over the personal upload link, with nobody in between. Free, the first step of the offer.
 *
 *   form (licence, name as on the licence, English name, office, mobile, email, areas, a few words, gender for Hebrew)
 *   -> the licence is checked against the Ministry of Justice brokers register (data.gov.il, public, free)
 *   -> one record per licence: a second sign-up for the same licence gets "you already have a site" and a way to
 *      receive the link again at the email that signed up, never the link itself
 *   -> nadlan_professional record (published), a Hebrew site at /brokers/<latin-name>/ built by x-broker-drop,
 *      a personal link /drop/<token>/, shown on the screen and sent to the email
 *   -> the English, Russian and French sites appear with the first listing (x-broker-drop 1.1)
 *
 * Protection: a hidden trap field, rate limits per address and per day, the register match, the declaration, and a
 * record of every sign-up (hashed address, time, what the register returned) on the broker's record, private.
 * The form sits wherever the page holds <div class="nljoin-mount" data-lang="he"></div>; with this module off the
 * mount stays an empty div.
 *
 * Needs x-broker-drop 1.1 (nl_drop_* functions). Installed as the persistent Code Snippet "x-broker-join" by
 * scripts/broker-drop/deploydrop.py. Rollback: deactivate the snippet (the sites already built stay).
 */

if ( ! defined( 'ABSPATH' ) ) { return; }
if ( defined( 'NL_JOIN_VERSION' ) ) { return; }
define( 'NL_JOIN_VERSION', '1.0.0' );
define( 'NL_JOIN_REGISTER', 'a0f56034-88db-4132-8803-854bcdb01ca1' );

/* =====================================================================================================
 * Words: Hebrew, English, Russian, French (Israeli brokers, olim among them)
 * ===================================================================================================== */
function nl_join_t( $lang, $k ) {
	static $T = array(
		'he' => array(
			'h' => 'פותחים אתר, בחינם', 'lead' => 'שתי דקות. בודקים את הרישיון מול פנקס המתווכים של משרד המשפטים, ומיד מקבלים אתר משלכם וקישור אישי להעלאת נכסים מהטלפון.',
			'lic' => 'מספר רישיון תיווך', 'name' => 'השם המלא, כפי שהוא ברישיון', 'name_en' => 'השם באותיות לועזיות', 'name_en_h' => 'לכתובת האתר ולאתר באנגלית. לדוגמה: Meital Katzir',
			'brand' => 'שם המשרד או המותג', 'opt' => 'לא חובה', 'phone' => 'טלפון נייד לוואטסאפ', 'phone_h' => 'יופיע באתר, בכפתורי הוואטסאפ והחיוג.',
			'email' => 'מייל', 'email_h' => 'לא מתפרסם. לשם נשלח הקישור האישי.', 'areas' => 'שכונות וערים שבהן אתם עובדים', 'areas_h' => 'מופרדות בפסיק. לדוגמה: נווה צדק, פלורנטין, יפו',
			'bio' => 'כמה מילים עליכם', 'bio_h' => 'עד 300 תווים. יופיע באתר כמו שנכתב.', 'gender' => 'איך לכתוב עליכם בעברית', 'g_m' => 'מתווך', 'g_f' => 'מתווכת',
			'decl' => 'אני בעל או בעלת הרישיון, והפרטים נכונים. פתיחת אתר בשם של מתווך אחר אסורה.', 'agree' => 'קראתי את ההסבר על הפרטים, ואני מסכים או מסכימה שהשם, המשרד, הרישיון, הטלפון והאזורים יפורסמו באתר שלי.',
			'privacy_h' => 'מה קורה עם הפרטים',
			'privacy' => 'nad-lan.co.il משתמשת בפרטים כדי לפתוח את האתר שלכם ואת קישור השליחה. השם, שם המשרד, מספר הרישיון, הטלפון והאזורים מתפרסמים באתר שלכם ובעמודי הנכסים, כי תקנה 19 לתקנות המתווכים במקרקעין מחייבת אותם בכל פרסום. מספר הרישיון נבדק מול פנקס המתווכים הציבורי של משרד המשפטים. המייל לא מתפרסם ומשמש רק לשליחת הקישור ולהודעות שירות. אין חובה חוקית למסור את הפרטים, אבל בלעדיהם אי אפשר לפתוח אתר. לעיון בפרטים, לתיקון או למחיקת האתר: %s.',
			'send' => 'פתיחת האתר', 'sending' => 'בודקים את הרישיון…',
			'ok_h' => 'האתר שלכם באוויר', 'ok_site' => 'לאתר שלכם', 'ok_link' => 'הקישור האישי להעלאת נכסים', 'ok_copy' => 'העתקה', 'ok_copied' => 'הועתק',
			'ok_wa' => 'שליחה לעצמי בוואטסאפ', 'ok_wa_text' => 'הקישור שלי להעלאת נכסים לאתר ב-nad-lan: %s', 'ok_first' => 'העלאת הנכס הראשון',
			'ok_keep' => 'שמרו את הקישור לעצמכם: מי שמחזיק בו יכול להעלות נכסים לאתר שלכם. שלחנו אותו גם למייל.',
			'ok_how' => 'איך מעלים נכס: פותחים את הקישור בטלפון, בוחרים תמונות, כותבים או מכתיבים כמה שורות, ושולחים. העמוד עולה לאתר בתוך דקה, בעברית ובאנגלית.',
			'e_fields' => 'חסרים פרטים. כל השדות המסומנים הם חובה.', 'e_lic' => 'מספר רישיון הוא מספר בלבד.', 'e_phone' => 'צריך מספר נייד ישראלי, לדוגמה 052-3631582.',
			'e_email' => 'המייל לא נראה תקין.', 'e_name_en' => 'את השם באותיות לועזיות כותבים באנגלית בלבד.', 'e_decl' => 'צריך לסמן את שתי ההצהרות.',
			'e_notfound' => 'לא מצאנו את מספר הרישיון הזה בפנקס המתווכים של משרד המשפטים. בודקים את המספר ושולחים שוב.',
			'e_name' => 'השם לא תואם את השם שרשום לרישיון הזה בפנקס. כותבים את השם בדיוק כפי שהוא מופיע ברישיון.',
			'e_register' => 'הבדיקה מול פנקס המתווכים לא זמינה כרגע. נסו שוב בעוד כמה דקות.',
			'e_dup' => 'לרישיון הזה כבר יש אתר ב-nad-lan. אם זה אתם ואיבדתם את הקישור, אפשר לקבל אותו שוב למייל שנרשם.',
			'e_dup_btn' => 'שליחת הקישור שוב למייל', 'e_dup_sent' => 'אם המייל תואם את המייל שנרשם, הקישור נשלח אליו עכשיו.', 'e_dup_other' => 'לא אתם פתחתם את האתר? כתבו לנו: %s',
			'e_rate' => 'יותר מדי ניסיונות מהחיבור הזה. אפשר לנסות שוב בעוד שעה.', 'e_closed' => 'ההרשמה סגורה זמנית. אפשר לכתוב לנו: %s', 'e_net' => 'אין חיבור. בודקים את האינטרנט ושולחים שוב.',
			'e_fail' => 'פתיחת האתר נכשלה. נסו שוב בעוד רגע.',
			'mail_s' => 'האתר שלך ב-nad-lan והקישור האישי להעלאת נכסים',
			'mail_b' => "שלום %1\$s,\n\nהאתר שלך: %2\$s\n\nהקישור האישי להעלאת נכסים (שמרו אותו לעצמכם, מי שמחזיק בו יכול להעלות נכסים לאתר שלכם):\n%3\$s\n\nאיך מעלים נכס: פותחים את הקישור בטלפון, בוחרים תמונות, כותבים כמה שורות על הנכס ושולחים. העמוד עולה לאתר בתוך דקה.\n\nnad-lan.co.il",
		),
		'en' => array(
			'h' => 'Open your site, free', 'lead' => 'Two minutes. We check your licence against the Ministry of Justice brokers register, and you get your own site and a personal link for uploading listings from your phone.',
			'lic' => 'Broker licence number', 'name' => 'Your full name in Hebrew, as on the licence', 'name_en' => 'Your name in English', 'name_en_h' => 'For your site address and your English site. For example: Meital Katzir',
			'brand' => 'Agency or brand name', 'opt' => 'optional', 'phone' => 'Mobile number for WhatsApp', 'phone_h' => 'Shown on your site, on the WhatsApp and call buttons.',
			'email' => 'Email', 'email_h' => 'Never published. Your personal link is sent here.', 'areas' => 'Neighbourhoods and cities you work in', 'areas_h' => 'In Hebrew, separated by commas. For example: נווה צדק, פלורנטין, יפו',
			'bio' => 'A few words about you', 'bio_h' => 'Up to 300 characters, in Hebrew. Shown on your site as written.', 'gender' => 'Hebrew pages call you', 'g_m' => 'מתווך (m)', 'g_f' => 'מתווכת (f)',
			'decl' => 'I hold this licence and the details are correct. Opening a site in another broker’s name is forbidden.', 'agree' => 'I have read how the details are used, and I agree that my name, agency, licence, phone and areas are published on my site.',
			'privacy_h' => 'What happens with your details',
			'privacy' => 'nad-lan.co.il uses your details to open your site and your upload link. Your name, agency, licence number, phone and areas are published on your site and listing pages, because regulation 19 of the Israeli brokers regulations requires them on every publication. The licence number is checked against the public Ministry of Justice brokers register. Your email is never published and is used only to send the link and service messages. You are not legally required to give these details, but without them a site cannot be opened. To see, correct or delete your details or your site: %s.',
			'send' => 'Open my site', 'sending' => 'Checking the licence…',
			'ok_h' => 'Your site is live', 'ok_site' => 'Your site', 'ok_link' => 'Your personal upload link', 'ok_copy' => 'Copy', 'ok_copied' => 'Copied',
			'ok_wa' => 'Send it to myself on WhatsApp', 'ok_wa_text' => 'My link for uploading listings to my nad-lan site: %s', 'ok_first' => 'Upload the first listing',
			'ok_keep' => 'Keep this link to yourself: whoever holds it can upload listings to your site. It was also sent to your email.',
			'ok_how' => 'How to upload: open the link on your phone, pick photos, write or dictate a few lines, and send. The page is live within a minute, in Hebrew and English.',
			'e_fields' => 'Some details are missing. Every marked field is required.', 'e_lic' => 'The licence number is digits only.', 'e_phone' => 'An Israeli mobile number is needed, for example 052-3631582.',
			'e_email' => 'The email does not look right.', 'e_name_en' => 'The English name takes Latin letters only.', 'e_decl' => 'Both statements need to be ticked.',
			'e_notfound' => 'This licence number is not in the Ministry of Justice brokers register. Check the number and send again.',
			'e_name' => 'The name does not match the name registered for this licence. Write it in Hebrew exactly as on the licence.',
			'e_register' => 'The brokers register cannot be checked right now. Try again in a few minutes.',
			'e_dup' => 'This licence already has a site on nad-lan. If it is yours and you lost the link, it can be sent again to the email that signed up.',
			'e_dup_btn' => 'Send the link again', 'e_dup_sent' => 'If the email matches the one that signed up, the link has been sent to it.', 'e_dup_other' => 'Did someone else open this site? Write to us: %s',
			'e_rate' => 'Too many attempts from this connection. Try again in an hour.', 'e_closed' => 'Sign-up is closed for now. Write to us: %s', 'e_net' => 'No connection. Check the internet and send again.',
			'e_fail' => 'The site could not be opened. Try again in a moment.',
		),
		'ru' => array(
			'h' => 'Откройте свой сайт бесплатно', 'lead' => 'Две минуты. Мы проверяем лицензию по реестру риелторов Министерства юстиции, и вы сразу получаете свой сайт и личную ссылку для загрузки объектов с телефона.',
			'lic' => 'Номер лицензии риелтора', 'name' => 'Полное имя на иврите, как в лицензии', 'name_en' => 'Имя латинскими буквами', 'name_en_h' => 'Для адреса сайта и англоязычной версии. Например: Meital Katzir',
			'brand' => 'Название агентства или бренда', 'opt' => 'необязательно', 'phone' => 'Мобильный для WhatsApp', 'phone_h' => 'Будет на сайте, в кнопках WhatsApp и звонка.',
			'email' => 'Эл. почта', 'email_h' => 'Не публикуется. Сюда придёт личная ссылка.', 'areas' => 'Районы и города, где вы работаете', 'areas_h' => 'На иврите, через запятую. Например: נווה צדק, פלורנטין, יפו',
			'bio' => 'Несколько слов о вас', 'bio_h' => 'До 300 знаков, на иврите. Появится на сайте как написано.', 'gender' => 'Как писать о вас на иврите', 'g_m' => 'מתווך (м)', 'g_f' => 'מתווכת (ж)',
			'decl' => 'Лицензия принадлежит мне, данные верны. Открывать сайт от имени другого риелтора запрещено.', 'agree' => 'Я прочитал(а), как используются данные, и согласен(на) на публикацию имени, агентства, лицензии, телефона и районов на моём сайте.',
			'privacy_h' => 'Что происходит с данными',
			'privacy' => 'nad-lan.co.il использует данные, чтобы открыть ваш сайт и ссылку для загрузки. Имя, агентство, номер лицензии, телефон и районы публикуются на вашем сайте и страницах объектов: правило 19 израильских правил о риелторах требует их в каждой публикации. Номер лицензии проверяется по открытому реестру риелторов Министерства юстиции. Почта не публикуется и используется только для отправки ссылки и служебных сообщений. Закон не обязывает передавать данные, но без них сайт открыть нельзя. Просмотр, исправление или удаление данных и сайта: %s.',
			'send' => 'Открыть сайт', 'sending' => 'Проверяем лицензию…',
			'ok_h' => 'Ваш сайт работает', 'ok_site' => 'Ваш сайт', 'ok_link' => 'Личная ссылка для загрузки объектов', 'ok_copy' => 'Копировать', 'ok_copied' => 'Скопировано',
			'ok_wa' => 'Отправить себе в WhatsApp', 'ok_wa_text' => 'Моя ссылка для загрузки объектов на сайт в nad-lan: %s', 'ok_first' => 'Загрузить первый объект',
			'ok_keep' => 'Храните ссылку у себя: любой, у кого она есть, может загружать объекты на ваш сайт. Мы отправили её и на почту.',
			'ok_how' => 'Как загрузить объект: откройте ссылку в телефоне, выберите фото, напишите или надиктуйте несколько строк и отправьте. Страница появится на сайте через минуту.',
			'e_fields' => 'Не хватает данных. Все отмеченные поля обязательны.', 'e_lic' => 'Номер лицензии состоит только из цифр.', 'e_phone' => 'Нужен израильский мобильный номер, например 052-3631582.',
			'e_email' => 'Адрес почты выглядит неверно.', 'e_name_en' => 'Имя латиницей пишется только латинскими буквами.', 'e_decl' => 'Нужно отметить оба пункта.',
			'e_notfound' => 'Этого номера нет в реестре риелторов Министерства юстиции. Проверьте номер и отправьте снова.',
			'e_name' => 'Имя не совпадает с именем, записанным на эту лицензию. Напишите его на иврите точно как в лицензии.',
			'e_register' => 'Реестр риелторов сейчас недоступен. Попробуйте через несколько минут.',
			'e_dup' => 'У этой лицензии уже есть сайт на nad-lan. Если это вы и ссылка потерялась, её можно получить снова на почту, указанную при регистрации.',
			'e_dup_btn' => 'Отправить ссылку снова', 'e_dup_sent' => 'Если почта совпадает с указанной при регистрации, ссылка уже отправлена.', 'e_dup_other' => 'Сайт открыли не вы? Напишите нам: %s',
			'e_rate' => 'Слишком много попыток с этого подключения. Попробуйте через час.', 'e_closed' => 'Регистрация временно закрыта. Напишите нам: %s', 'e_net' => 'Нет соединения. Проверьте интернет и отправьте снова.',
			'e_fail' => 'Не удалось открыть сайт. Попробуйте ещё раз.',
		),
		'fr' => array(
			'h' => 'Ouvrez votre site, gratuitement', 'lead' => 'Deux minutes. Nous vérifions votre licence dans le registre des agents immobiliers du ministère de la Justice, et vous recevez votre propre site et un lien personnel pour publier vos biens depuis votre téléphone.',
			'lic' => 'Numéro de licence d’agent immobilier', 'name' => 'Nom complet en hébreu, comme sur la licence', 'name_en' => 'Nom en lettres latines', 'name_en_h' => 'Pour l’adresse du site et la version anglaise. Par exemple : Meital Katzir',
			'brand' => 'Nom de l’agence ou de la marque', 'opt' => 'facultatif', 'phone' => 'Portable pour WhatsApp', 'phone_h' => 'Affiché sur le site, sur les boutons WhatsApp et appel.',
			'email' => 'E-mail', 'email_h' => 'Jamais publié. Votre lien personnel y est envoyé.', 'areas' => 'Quartiers et villes où vous travaillez', 'areas_h' => 'En hébreu, séparés par des virgules. Par exemple : נווה צדק, פלורנטין, יפו',
			'bio' => 'Quelques mots sur vous', 'bio_h' => 'Jusqu’à 300 caractères, en hébreu. Affiché tel quel sur le site.', 'gender' => 'En hébreu, les pages vous appellent', 'g_m' => 'מתווך (m)', 'g_f' => 'מתווכת (f)',
			'decl' => 'Je suis titulaire de cette licence et les informations sont exactes. Ouvrir un site au nom d’un autre agent est interdit.', 'agree' => 'J’ai lu comment les informations sont utilisées et j’accepte la publication de mon nom, agence, licence, téléphone et quartiers sur mon site.',
			'privacy_h' => 'Ce que deviennent vos informations',
			'privacy' => 'nad-lan.co.il utilise vos informations pour ouvrir votre site et votre lien de publication. Votre nom, votre agence, votre numéro de licence, votre téléphone et vos quartiers sont publiés sur votre site et vos pages de biens, car l’article 19 du règlement israélien des agents immobiliers les exige dans chaque publication. Le numéro de licence est vérifié dans le registre public du ministère de la Justice. Votre e-mail n’est jamais publié et sert uniquement à envoyer le lien et des messages de service. La loi ne vous oblige pas à fournir ces informations, mais sans elles le site ne peut pas être ouvert. Pour consulter, corriger ou supprimer vos informations ou votre site : %s.',
			'send' => 'Ouvrir mon site', 'sending' => 'Vérification de la licence…',
			'ok_h' => 'Votre site est en ligne', 'ok_site' => 'Votre site', 'ok_link' => 'Votre lien personnel de publication', 'ok_copy' => 'Copier', 'ok_copied' => 'Copié',
			'ok_wa' => 'Me l’envoyer sur WhatsApp', 'ok_wa_text' => 'Mon lien pour publier des biens sur mon site nad-lan : %s', 'ok_first' => 'Publier le premier bien',
			'ok_keep' => 'Gardez ce lien pour vous : toute personne qui le détient peut publier sur votre site. Il vous a aussi été envoyé par e-mail.',
			'ok_how' => 'Pour publier : ouvrez le lien sur votre téléphone, choisissez des photos, écrivez ou dictez quelques lignes, et envoyez. La page est en ligne en une minute.',
			'e_fields' => 'Il manque des informations. Tous les champs marqués sont obligatoires.', 'e_lic' => 'Le numéro de licence ne contient que des chiffres.', 'e_phone' => 'Un numéro de portable israélien est nécessaire, par exemple 052-3631582.',
			'e_email' => 'L’e-mail ne semble pas valide.', 'e_name_en' => 'Le nom en lettres latines ne prend que des lettres latines.', 'e_decl' => 'Les deux déclarations doivent être cochées.',
			'e_notfound' => 'Ce numéro ne figure pas dans le registre des agents immobiliers du ministère de la Justice. Vérifiez le numéro et envoyez à nouveau.',
			'e_name' => 'Le nom ne correspond pas à celui enregistré pour cette licence. Écrivez-le en hébreu exactement comme sur la licence.',
			'e_register' => 'Le registre ne peut pas être consulté pour le moment. Réessayez dans quelques minutes.',
			'e_dup' => 'Cette licence a déjà un site sur nad-lan. Si c’est le vôtre et que vous avez perdu le lien, il peut être renvoyé à l’e-mail de l’inscription.',
			'e_dup_btn' => 'Renvoyer le lien', 'e_dup_sent' => 'Si l’e-mail correspond à celui de l’inscription, le lien vient d’y être envoyé.', 'e_dup_other' => 'Ce n’est pas vous qui avez ouvert ce site ? Écrivez-nous : %s',
			'e_rate' => 'Trop de tentatives depuis cette connexion. Réessayez dans une heure.', 'e_closed' => 'Les inscriptions sont fermées pour le moment. Écrivez-nous : %s', 'e_net' => 'Pas de connexion. Vérifiez internet et envoyez à nouveau.',
			'e_fail' => 'Le site n’a pas pu être ouvert. Réessayez dans un instant.',
		),
	);
	$lang = isset( $T[ $lang ] ) ? $lang : 'he';
	return $T[ $lang ][ $k ] ?? ( $T['he'][ $k ] ?? $k );
}

function nl_join_contact() {
	return 'info@nad-lan.co.il';
}

/* =====================================================================================================
 * The Ministry of Justice brokers register (data.gov.il datastore, public). Cached a day per licence.
 * ===================================================================================================== */
function nl_join_registry( $licence ) {
	$licence = preg_replace( '/\D+/', '', (string) $licence );
	if ( $licence === '' ) { return new WP_Error( 'nolic', 'no licence' ); }
	$key = 'nljoin_reg_' . $licence;
	$hit = get_transient( $key );
	if ( is_array( $hit ) ) { return $hit; }
	$url  = add_query_arg( array(
		'resource_id' => NL_JOIN_REGISTER,
		'filters'     => wp_json_encode( array( 'מס רשיון' => (int) $licence ), JSON_UNESCAPED_UNICODE ),
		'limit'       => 5,
	), 'https://data.gov.il/api/3/action/datastore_search' );
	$resp = wp_remote_get( $url, array(
		'timeout' => 20,
		'headers' => array( 'User-Agent' => 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128 Safari/537.36 nad-lan.co.il-licence-check', 'Accept' => 'application/json' ),
	) );
	if ( is_wp_error( $resp ) ) { return new WP_Error( 'register', $resp->get_error_message() ); }
	$code = (int) wp_remote_retrieve_response_code( $resp );
	$data = json_decode( wp_remote_retrieve_body( $resp ), true );
	if ( $code !== 200 || ! is_array( $data ) || empty( $data['success'] ) ) { return new WP_Error( 'register', 'http ' . $code ); }
	$out = array( 'found' => false, 'name' => '', 'city' => '' );
	foreach ( (array) ( $data['result']['records'] ?? array() ) as $r ) {
		if ( (string) (int) ( $r['מס רשיון'] ?? 0 ) === (string) (int) $licence ) {
			$out = array( 'found' => true, 'name' => trim( (string) ( $r['שם המתווך'] ?? '' ) ), 'city' => trim( (string) ( $r['עיר מגורים'] ?? '' ) ) );
			break;
		}
	}
	set_transient( $key, $out, $out['found'] ? DAY_IN_SECONDS : HOUR_IN_SECONDS );
	return $out;
}

/** Hebrew name words, spelled one way: no punctuation, final letters as plain letters. */
function nl_join_name_words( $s ) {
	$s = str_replace( array( 'ך', 'ם', 'ן', 'ף', 'ץ' ), array( 'כ', 'מ', 'נ', 'פ', 'צ' ), (string) $s );
	$s = preg_replace( '/[^\p{Hebrew}\p{L}\s]+/u', ' ', $s );
	$s = function_exists( 'mb_strtolower' ) ? mb_strtolower( $s ) : strtolower( $s );
	return array_values( array_filter( preg_split( '/\s+/u', trim( $s ) ) ) );
}

/** The register writes surname first ("קציר מיטל"); the broker may write it either way, with a middle name or without. */
function nl_join_name_match( $typed, $registered ) {
	$t = nl_join_name_words( $typed );
	$r = nl_join_name_words( $registered );
	if ( count( $t ) < 2 || count( $r ) < 1 ) { return false; }
	$common = count( array_intersect( $r, $t ) );
	return $common >= min( 2, count( $r ) ) && $common >= count( $r ) - 1;
}

/* =====================================================================================================
 * The form: printed where the page holds the mount, in the page's language
 * ===================================================================================================== */
add_filter( 'the_content', function ( $html ) {
	if ( strpos( $html, 'nljoin-mount' ) === false || is_admin() ) { return $html; }
	return preg_replace_callback( '#<div class="nljoin-mount"(?: data-lang="([a-z]{2})")?[^>]*>\s*</div>#', function ( $m ) {
		return nl_join_form( ! empty( $m[1] ) ? $m[1] : 'he' );
	}, $html, 1 );
}, 30 );

function nl_join_form( $lang ) {
	$lang = in_array( $lang, array( 'he', 'en', 'ru', 'fr' ), true ) ? $lang : 'he';
	$he   = $lang === 'he';
	$t    = function ( $k ) use ( $lang ) { return nl_join_t( $lang, $k ); };
	$req  = '<span class="nljoin-req" aria-hidden="true">*</span>';
	$f    = function ( $id, $label, $attrs, $hint = '', $required = true ) use ( $req, $t ) {
		return '<div class="nljoin-f"><label for="nlj-' . $id . '">' . esc_html( $label ) . ( $required ? $req : ' <span class="nljoin-opt">(' . esc_html( $t( 'opt' ) ) . ')</span>' ) . '</label>'
			. '<input id="nlj-' . $id . '" name="' . $id . '" ' . $attrs . ( $required ? ' required aria-required="true"' : '' ) . ( $hint !== '' ? ' aria-describedby="nlj-' . $id . '-h"' : '' ) . '>'
			. ( $hint !== '' ? '<p class="nljoin-hint" id="nlj-' . $id . '-h">' . esc_html( $hint ) . '</p>' : '' ) . '</div>';
	};
	$priv = get_privacy_policy_url();
	$who  = '<a href="mailto:' . esc_attr( nl_join_contact() ) . '">' . esc_html( nl_join_contact() ) . '</a>' . ( $priv ? ' · <a href="' . esc_url( $priv ) . '">' . ( $he ? 'מדיניות הפרטיות' : 'Privacy policy' ) . '</a>' : '' );
	$cfg  = array( 'api' => esc_url_raw( rest_url( 'nadlan/v1/brokers' ) ), 'lang' => $lang, 'copied' => $t( 'ok_copied' ), 'sending' => $t( 'sending' ), 'send' => $t( 'send' ), 'net' => $t( 'e_net' ) );
	$h  = '<section class="nljoin" id="join" lang="' . $lang . '" dir="' . ( $he ? 'rtl' : 'ltr' ) . '" aria-labelledby="nlj-h">';
	$h .= '<div class="nljoin-card">';
	$h .= '<h2 id="nlj-h">' . esc_html( $t( 'h' ) ) . '</h2><p class="nljoin-lead">' . esc_html( $t( 'lead' ) ) . '</p>';
	$h .= '<form class="nljoin-form" novalidate>';
	$h .= '<div class="nljoin-grid">';
	$h .= $f( 'licence', $t( 'lic' ), 'type="text" inputmode="numeric" autocomplete="off" maxlength="12" dir="ltr"' );
	$h .= $f( 'name_he', $t( 'name' ), 'type="text" autocomplete="name" maxlength="60" dir="rtl"' );
	$h .= $f( 'name_en', $t( 'name_en' ), 'type="text" autocomplete="off" maxlength="60" dir="ltr" lang="en"', $t( 'name_en_h' ) );
	$h .= $f( 'brand', $t( 'brand' ), 'type="text" autocomplete="organization" maxlength="60"', '', false );
	$h .= $f( 'phone', $t( 'phone' ), 'type="tel" inputmode="tel" autocomplete="tel" maxlength="20" dir="ltr"', $t( 'phone_h' ) );
	$h .= $f( 'email', $t( 'email' ), 'type="email" inputmode="email" autocomplete="email" maxlength="120" dir="ltr"', $t( 'email_h' ) );
	$h .= '</div>';
	$h .= $f( 'areas', $t( 'areas' ), 'type="text" autocomplete="off" maxlength="200" dir="rtl"', $t( 'areas_h' ) );
	$h .= '<div class="nljoin-f"><label for="nlj-bio">' . esc_html( $t( 'bio' ) ) . ' <span class="nljoin-opt">(' . esc_html( $t( 'opt' ) ) . ')</span></label><textarea id="nlj-bio" name="bio" rows="3" maxlength="300" dir="rtl" aria-describedby="nlj-bio-h"></textarea><p class="nljoin-hint" id="nlj-bio-h">' . esc_html( $t( 'bio_h' ) ) . '</p></div>';
	$h .= '<fieldset class="nljoin-g"><legend>' . esc_html( $t( 'gender' ) ) . $req . '</legend><label><input type="radio" name="gender" value="m" required> ' . esc_html( $t( 'g_m' ) ) . '</label><label><input type="radio" name="gender" value="f"> ' . esc_html( $t( 'g_f' ) ) . '</label></fieldset>';
	$h .= '<details class="nljoin-priv"><summary>' . esc_html( $t( 'privacy_h' ) ) . '</summary><p>' . sprintf( esc_html( $t( 'privacy' ) ), $who ) . '</p></details>';
	$h .= '<label class="nljoin-c"><input type="checkbox" name="decl" value="1" required> <span>' . esc_html( $t( 'decl' ) ) . '</span></label>';
	$h .= '<label class="nljoin-c"><input type="checkbox" name="agree" value="1" required> <span>' . esc_html( $t( 'agree' ) ) . '</span></label>';
	$h .= '<div class="nljoin-trap" aria-hidden="true"><label>Website<input type="text" name="website" tabindex="-1" autocomplete="off"></label></div>';
	$h .= '<button type="submit" class="nljoin-btn">' . esc_html( $t( 'send' ) ) . '</button>';
	$h .= '<div class="nljoin-msg" role="alert" aria-live="assertive" hidden></div>';
	$h .= '</form>';
	$h .= '<div class="nljoin-ok" hidden><h3>' . esc_html( $t( 'ok_h' ) ) . '</h3>';
	$h .= '<p><a class="nljoin-btn nljoin-site" href="#" target="_blank" rel="noopener">' . esc_html( $t( 'ok_site' ) ) . '</a></p>';
	$h .= '<p class="nljoin-lbl">' . esc_html( $t( 'ok_link' ) ) . '</p><div class="nljoin-link"><input type="text" readonly dir="ltr" aria-label="' . esc_attr( $t( 'ok_link' ) ) . '"><button type="button" class="nljoin-copy">' . esc_html( $t( 'ok_copy' ) ) . '</button></div>';
	$h .= '<p class="nljoin-row"><a class="nljoin-btn nljoin-btn--ghost nljoin-wa" href="#" target="_blank" rel="noopener" data-text="' . esc_attr( $t( 'ok_wa_text' ) ) . '">' . esc_html( $t( 'ok_wa' ) ) . '</a><a class="nljoin-btn nljoin-first" href="#" target="_blank" rel="noopener">' . esc_html( $t( 'ok_first' ) ) . '</a></p>';
	$h .= '<p class="nljoin-hint">' . esc_html( $t( 'ok_keep' ) ) . '</p><p class="nljoin-hint">' . esc_html( $t( 'ok_how' ) ) . '</p></div>';
	$h .= '</div></section>';
	$h .= '<style>' . nl_join_css() . '</style>';
	$h .= '<script>window.NLJOIN=' . wp_json_encode( $cfg, JSON_UNESCAPED_UNICODE | JSON_UNESCAPED_SLASHES ) . ';</script><script>' . nl_join_js() . '</script>';
	return $h;
}

function nl_join_css() {
	return <<<'NLJCSS'
.nljoin{--j-ink:#14212B;--j-ink2:#3B4753;--j-mute:#6B7680;--j-line:#E3E1DA;--j-sea:#2F6F86;--j-seah:#255C70;--j-sand:#EEE9DD;--j-surf:#FFFFFF;--j-bad:#B3261E;--j-ok:#2E7D5B;margin:32px 0;scroll-margin-top:96px}
.nljoin .nljoin-card{background:var(--j-surf);border:1px solid var(--j-line);border-radius:16px;padding:clamp(20px,4vw,36px);max-width:760px;margin-inline:auto;box-shadow:0 1px 2px rgba(20,33,43,.04)}
.nljoin h2{font-family:'Noto Serif Hebrew','Frank Ruhl Libre','Noto Serif',Georgia,serif!important;font-weight:600;font-size:clamp(24px,3vw,32px);line-height:1.25;margin:0 0 8px;color:var(--j-ink)!important;text-wrap:balance}
.nljoin h3{font-family:'Noto Serif Hebrew','Frank Ruhl Libre','Noto Serif',Georgia,serif!important;font-weight:600;font-size:24px;margin:0 0 12px;color:var(--j-ink)!important}
.nljoin .nljoin-lead{margin:0 0 20px;color:var(--j-ink2);font-size:16.5px;line-height:1.65}
.nljoin .nljoin-grid{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:0 18px}
@media (max-width:640px){.nljoin .nljoin-grid{grid-template-columns:minmax(0,1fr)}}
.nljoin .nljoin-f{margin:0 0 14px}
.nljoin label,.nljoin legend{display:block;font-weight:700;font-size:15px;color:var(--j-ink);margin:0 0 6px}
.nljoin .nljoin-req{color:var(--j-sea);margin-inline-start:3px}
.nljoin .nljoin-opt{font-weight:400;color:var(--j-mute);font-size:13.5px}
.nljoin input[type=text],.nljoin input[type=tel],.nljoin input[type=email],.nljoin textarea{width:100%;box-sizing:border-box;min-height:48px;border:1px solid var(--j-line);border-radius:10px;padding:10px 12px;font:inherit;font-size:16px;background:#FBFAF7;color:var(--j-ink)}
.nljoin textarea{min-height:84px;resize:vertical}
.nljoin input:focus,.nljoin textarea:focus{outline:3px solid var(--j-sea);outline-offset:1px;border-color:transparent}
.nljoin input[aria-invalid=true]{border-color:var(--j-bad)}
.nljoin .nljoin-hint{margin:6px 0 0;font-size:13.5px;color:var(--j-mute);line-height:1.5}
.nljoin fieldset.nljoin-g{border:0;padding:0;margin:4px 0 14px;display:flex;flex-wrap:wrap;gap:6px 18px;align-items:center}
.nljoin fieldset.nljoin-g legend{width:100%}
.nljoin fieldset.nljoin-g label{display:inline-flex;gap:6px;align-items:center;font-weight:500;margin:0}
.nljoin .nljoin-priv{margin:6px 0 14px;border:1px solid var(--j-line);border-radius:10px;padding:10px 14px;background:#FBFAF7}
.nljoin .nljoin-priv summary{cursor:pointer;font-weight:700;color:var(--j-sea)}
.nljoin .nljoin-priv p{margin:10px 0 0;font-size:14px;line-height:1.65;color:var(--j-ink2)}
.nljoin .nljoin-priv a{color:var(--j-sea)}
.nljoin .nljoin-c{display:flex;gap:10px;align-items:flex-start;font-weight:500;font-size:14.5px;line-height:1.55;margin:0 0 10px;color:var(--j-ink2)}
.nljoin .nljoin-c input{margin-top:4px;width:18px;height:18px;flex:0 0 auto}
.nljoin .nljoin-trap{position:absolute!important;width:1px;height:1px;overflow:hidden;clip:rect(0 0 0 0);white-space:nowrap}
.nljoin .nljoin-btn{display:inline-flex;align-items:center;justify-content:center;min-height:52px;padding:10px 26px;border-radius:999px;border:1px solid var(--j-sea);background:var(--j-sea);color:#fff!important;font:700 17px/1.2 inherit;cursor:pointer;text-decoration:none!important}
.nljoin .nljoin-btn:hover{background:var(--j-seah);border-color:var(--j-seah)}
.nljoin .nljoin-btn:disabled{opacity:.6;cursor:default}
.nljoin .nljoin-btn--ghost{background:transparent;color:var(--j-sea)!important}
.nljoin .nljoin-btn--ghost:hover{background:var(--j-sand)}
.nljoin form .nljoin-btn{width:100%;margin-top:6px}
.nljoin .nljoin-msg{margin-top:14px;padding:12px 14px;border-radius:10px;border:1px solid var(--j-bad);background:#FBEDEC;color:var(--j-ink);font-size:15px;line-height:1.6}
.nljoin .nljoin-msg[data-k=ok]{border-color:var(--j-ok);background:#EAF4EF}
.nljoin .nljoin-msg button{margin-top:10px;min-height:44px;padding:8px 18px;font-size:15px}
.nljoin .nljoin-ok .nljoin-lbl{font-weight:700;margin:18px 0 6px}
.nljoin .nljoin-link{display:flex;gap:8px}
.nljoin .nljoin-link input{flex:1;min-width:0;font-size:14.5px}
.nljoin .nljoin-copy{min-height:48px;padding:8px 16px;border-radius:10px;border:1px solid var(--j-sea);background:#fff;color:var(--j-sea);font:700 15px inherit;cursor:pointer}
.nljoin .nljoin-row{display:flex;flex-wrap:wrap;gap:10px;margin:16px 0 8px}
[hidden]{display:none!important}
NLJCSS;
}

function nl_join_js() {
	return <<<'NLJJS'
(function(){
'use strict';
var C=window.NLJOIN||{},root=document.getElementById('join');if(!root)return;
var form=root.querySelector('.nljoin-form'),msg=root.querySelector('.nljoin-msg'),btn=form.querySelector('.nljoin-btn'),ok=root.querySelector('.nljoin-ok');
function esc(s){return String(s==null?'':s).replace(/[&<>"']/g,function(c){return {'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c];});}
function show(html,kind){msg.hidden=false;msg.setAttribute('data-k',kind||'');msg.innerHTML=html;msg.scrollIntoView({block:'nearest',behavior:'smooth'});}
function post(path,body){return fetch(C.api+path,{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(body),credentials:'omit'}).then(function(r){return r.json().then(function(j){return {ok:r.ok,s:r.status,j:j};});});}
function val(n){var el=form.elements[n];if(!el)return '';if(el.type==='checkbox')return el.checked?'1':'';if(el.length&&!el.tagName){for(var i=0;i<el.length;i++){if(el[i].checked)return el[i].value;}return '';}return (el.value||'').trim();}
form.addEventListener('submit',function(e){
  e.preventDefault();
  var data={lang:C.lang};['licence','name_he','name_en','brand','phone','email','areas','bio','gender','decl','agree','website'].forEach(function(n){data[n]=val(n);});
  [].forEach.call(form.querySelectorAll('[aria-invalid]'),function(x){x.removeAttribute('aria-invalid');});
  btn.disabled=true;btn.textContent=C.sending;msg.hidden=true;
  post('/join',data).then(function(x){
    if(x.ok&&x.j&&x.j.drop){
      form.hidden=true;ok.hidden=false;
      ok.querySelector('.nljoin-site').href=x.j.site;
      var inp=ok.querySelector('.nljoin-link input');inp.value=x.j.drop;
      ok.querySelector('.nljoin-first').href=x.j.drop;
      var wa=ok.querySelector('.nljoin-wa');wa.href='https://wa.me/?text='+encodeURIComponent(wa.getAttribute('data-text').replace('%s',x.j.drop));
      ok.querySelector('.nljoin-copy').addEventListener('click',function(){var b=this;function done(){b.textContent=C.copied;}
        if(navigator.clipboard&&navigator.clipboard.writeText){navigator.clipboard.writeText(x.j.drop).then(done,function(){inp.select();});}else{inp.select();}});
      ok.scrollIntoView({block:'start',behavior:'smooth'});
      return;
    }
    var j=x.j||{},m=j.message||'';
    if(j.data&&j.data.field){var f=form.elements[j.data.field];if(f&&f.setAttribute){f.setAttribute('aria-invalid','true');f.focus();}}
    if(j.code==='nljoin_dup'){
      show(esc(m)+'<div><button type="button" class="nljoin-btn nljoin-btn--ghost" id="nlj-relink">'+esc(j.data.btn)+'</button></div><div class="nljoin-hint">'+j.data.other+'</div>');
      var rb=document.getElementById('nlj-relink');
      rb.addEventListener('click',function(){rb.disabled=true;post('/relink',{licence:data.licence,email:data.email,lang:C.lang}).then(function(y){show(esc((y.j&&y.j.message)||''),'ok');}).catch(function(){show(esc(C.net));});});
      return;
    }
    show(esc(m||C.net));
  }).catch(function(){show(esc(C.net));}).then(function(){btn.disabled=false;btn.textContent=C.send;});
});
})();
NLJJS;
}

/* =====================================================================================================
 * The doors: join, and the link again
 * ===================================================================================================== */
add_action( 'rest_api_init', function () {
	register_rest_route( 'nadlan/v1', '/brokers/join', array( 'methods' => 'POST', 'permission_callback' => '__return_true', 'callback' => 'nl_join_rest' ) );
	register_rest_route( 'nadlan/v1', '/brokers/relink', array( 'methods' => 'POST', 'permission_callback' => '__return_true', 'callback' => 'nl_join_rest_relink' ) );
} );

function nl_join_ip_key() {
	$ip = isset( $_SERVER['REMOTE_ADDR'] ) ? (string) $_SERVER['REMOTE_ADDR'] : '';
	return substr( hash_hmac( 'sha256', $ip, wp_salt( 'nonce' ) ), 0, 20 );
}

function nl_join_limited( $bucket, $limit, $window ) {
	$k = 'nljoin_' . $bucket . '_' . nl_join_ip_key();
	$n = (int) get_transient( $k );
	if ( $n >= $limit ) { return true; }
	set_transient( $k, $n + 1, $window );
	return false;
}

function nl_join_err( $code, $lang, $key, $status = 400, $extra = array() ) {
	$m = nl_join_t( $lang, $key );
	if ( strpos( $m, '%s' ) !== false ) { $m = sprintf( $m, nl_join_contact() ); }
	return new WP_Error( $code, $m, array_merge( array( 'status' => $status ), $extra ) );
}

function nl_join_by_licence( $licence ) {
	$ids = get_posts( array(
		'post_type'        => 'nadlan_professional',
		'post_status'      => array( 'publish', 'draft', 'pending', 'private' ),
		'numberposts'      => 1,
		'fields'           => 'ids',
		'suppress_filters' => true,
		'meta_query'       => array( array( 'key' => 'license_number', 'value' => (string) $licence ) ),
	) );
	return $ids ? (int) $ids[0] : 0;
}

/** Areas and the office name in English, Russian and French, once at sign-up (a short model call; empty on any doubt). */
function nl_join_translate_names( $areas, $brand ) {
	$out = array( 'en' => array(), 'ru' => array(), 'fr' => array(), 'brand_en' => '' );
	if ( ! $areas || ! function_exists( 'nl_drop_llm_json' ) ) { return $out; }
	$sys = 'You give the usual English, Russian and French names of Israeli neighbourhoods and cities, as locals and property sites write them. Return ONLY JSON {"en":[...],"ru":[...],"fr":[...]} with the names in the same order as given, one per item. Example: ["נווה צדק","יפו","הרצליה פיתוח"] -> {"en":["Neve Tzedek","Jaffa","Herzliya Pituach"],"ru":["Неве-Цедек","Яффо","Герцлия-Питуах"],"fr":["Neve Tsedek","Jaffa","Herzliya Pituah"]}. Never add, drop or merge an item.';
	$err = null;
	$j   = nl_drop_llm_json( $sys, wp_json_encode( array_values( $areas ), JSON_UNESCAPED_UNICODE ), 500, $err );
	if ( ! is_array( $j ) ) { return $out; }
	foreach ( array( 'en', 'ru', 'fr' ) as $l ) {
		$list = array_values( (array) ( $j[ $l ] ?? array() ) );
		if ( count( $list ) !== count( $areas ) ) { continue; }
		$ok = true;
		foreach ( $list as $x ) {
			if ( ! is_string( $x ) || $x === '' || mb_strlen( $x ) > 40 || preg_match( '/[\d{}<>@\/\\\\]|https?:/u', $x ) || preg_match( '/\p{Hebrew}/u', $x ) ) { $ok = false; break; }
		}
		if ( $ok ) { $out[ $l ] = array_map( 'sanitize_text_field', $list ); }
	}
	if ( $brand !== '' && ! preg_match( '/\p{Hebrew}/u', $brand ) ) { $out['brand_en'] = $brand; }
	return $out;
}

function nl_join_rest( WP_REST_Request $req ) {
	$lang = in_array( (string) $req->get_param( 'lang' ), array( 'he', 'en', 'ru', 'fr' ), true ) ? (string) $req->get_param( 'lang' ) : 'he';
	if ( ! function_exists( 'nl_drop_site_ensure' ) ) { return nl_join_err( 'nljoin_engine', $lang, 'e_fail', 503 ); }
	if ( get_option( 'nl_join_open', '1' ) !== '1' ) { return nl_join_err( 'nljoin_closed', $lang, 'e_closed', 403 ); }
	$p = function ( $k, $max ) use ( $req ) {
		$v = trim( sanitize_text_field( wp_unslash( (string) $req->get_param( $k ) ) ) );
		return function_exists( 'mb_substr' ) ? mb_substr( $v, 0, $max ) : substr( $v, 0, $max );
	};
	if ( $p( 'website', 50 ) !== '' ) { return array( 'ok' => true ); }   // the trap: a quiet no
	if ( nl_join_limited( 'try', 12, HOUR_IN_SECONDS ) ) { return nl_join_err( 'nljoin_rate', $lang, 'e_rate', 429 ); }
	$licence = preg_replace( '/\D+/', '', $p( 'licence', 20 ) );
	$name_he = preg_replace( '/\s+/u', ' ', $p( 'name_he', 60 ) );
	$name_en = preg_replace( '/\s+/u', ' ', $p( 'name_en', 60 ) );
	$brand   = $p( 'brand', 60 );
	$phone   = $p( 'phone', 20 );
	$email   = sanitize_email( $p( 'email', 120 ) );
	$areas   = array_slice( array_values( array_filter( array_map( 'trim', preg_split( '/[,،\n]+/u', $p( 'areas', 200 ) ) ) ) ), 0, 8 );
	$bio     = trim( sanitize_textarea_field( wp_unslash( (string) $req->get_param( 'bio' ) ) ) );
	$bio     = function_exists( 'mb_substr' ) ? mb_substr( $bio, 0, 300 ) : substr( $bio, 0, 300 );
	$gender  = $p( 'gender', 2 ) === 'f' ? 'f' : ( $p( 'gender', 2 ) === 'm' ? 'm' : '' );
	if ( $licence === '' || $name_he === '' || $name_en === '' || $phone === '' || $email === '' || ! $areas || $gender === '' ) {
		$field = $licence === '' ? 'licence' : ( $name_he === '' ? 'name_he' : ( $name_en === '' ? 'name_en' : ( $phone === '' ? 'phone' : ( $email === '' ? 'email' : ( ! $areas ? 'areas' : 'gender' ) ) ) ) );
		return nl_join_err( 'nljoin_fields', $lang, 'e_fields', 400, array( 'field' => $field ) );
	}
	if ( strlen( $licence ) < 4 || strlen( $licence ) > 9 ) { return nl_join_err( 'nljoin_lic', $lang, 'e_lic', 400, array( 'field' => 'licence' ) ); }
	if ( ! preg_match( "/^[A-Za-z][A-Za-z .'\-]{1,58}[A-Za-z.]$/", $name_en ) ) { return nl_join_err( 'nljoin_name_en', $lang, 'e_name_en', 400, array( 'field' => 'name_en' ) ); }
	$digits = preg_replace( '/\D+/', '', $phone );
	if ( strpos( $digits, '972' ) === 0 ) { $digits = '0' . substr( $digits, 3 ); }
	if ( ! preg_match( '/^05\d{8}$/', $digits ) ) { return nl_join_err( 'nljoin_phone', $lang, 'e_phone', 400, array( 'field' => 'phone' ) ); }
	$phone = substr( $digits, 0, 3 ) . '-' . substr( $digits, 3 );
	if ( ! is_email( $email ) ) { return nl_join_err( 'nljoin_email', $lang, 'e_email', 400, array( 'field' => 'email' ) ); }
	if ( $req->get_param( 'decl' ) !== '1' || $req->get_param( 'agree' ) !== '1' ) { return nl_join_err( 'nljoin_decl', $lang, 'e_decl', 400, array( 'field' => 'decl' ) ); }
	foreach ( array_merge( $areas, array( $bio, $brand ) ) as $txt ) {
		if ( preg_match( '/https?:|www\.|@|<|>/i', $txt ) ) { return nl_join_err( 'nljoin_fields', $lang, 'e_fields', 400, array( 'field' => 'areas' ) ); }
	}
	if ( $bio !== '' && function_exists( 'nl_drop_banned_hits' ) && nl_drop_banned_hits( $bio, 'he' ) ) { $bio = ''; }

	// one site per licence
	$dup = nl_join_by_licence( $licence );
	if ( $dup ) {
		return nl_join_err( 'nljoin_dup', $lang, 'e_dup', 409, array( 'btn' => nl_join_t( $lang, 'e_dup_btn' ), 'other' => sprintf( esc_html( nl_join_t( $lang, 'e_dup_other' ) ), '<a href="mailto:' . esc_attr( nl_join_contact() ) . '">' . esc_html( nl_join_contact() ) . '</a>' ) ) );
	}
	if ( nl_join_limited( 'reg', 8, HOUR_IN_SECONDS ) ) { return nl_join_err( 'nljoin_rate', $lang, 'e_rate', 429 ); }
	$reg = nl_join_registry( $licence );
	if ( is_wp_error( $reg ) ) { return nl_join_err( 'nljoin_register', $lang, 'e_register', 503 ); }
	if ( empty( $reg['found'] ) ) { return nl_join_err( 'nljoin_notfound', $lang, 'e_notfound', 404, array( 'field' => 'licence' ) ); }
	if ( ! nl_join_name_match( $name_he, $reg['name'] ) ) { return nl_join_err( 'nljoin_name', $lang, 'e_name', 400, array( 'field' => 'name_he' ) ); }

	// a quiet day has a ceiling; a flood waits for the owner
	$day = 'nljoin_day_' . gmdate( 'Ymd' );
	$n   = (int) get_option( $day, 0 );
	if ( $n >= (int) get_option( 'nl_join_daily_cap', 40 ) ) { return nl_join_err( 'nljoin_closed', $lang, 'e_closed', 429 ); }
	update_option( $day, $n + 1, false );

	$res = nl_join_create( array(
		'licence' => $licence, 'name_he' => $name_he, 'name_en' => $name_en, 'brand' => $brand, 'phone' => $phone, 'email' => $email,
		'areas' => $areas, 'bio' => $bio, 'gender' => $gender, 'register' => $reg, 'lang' => $lang,
	) );
	if ( is_wp_error( $res ) ) { return nl_join_err( 'nljoin_fail', $lang, 'e_fail', 500 ); }
	return $res;
}

/**
 * Opens the broker: the record, the link, the Hebrew site. Also used by the owner's test bridge with 'status' => 'draft'.
 * @param array $d licence, name_he, name_en, brand, phone, email, areas[], bio, gender, register{name,city}, lang, status
 */
function nl_join_create( $d, $status = 'publish' ) {
	$slug_base = sanitize_title( $d['name_en'] );
	if ( $slug_base === '' ) { return new WP_Error( 'slug', 'slug' ); }
	$parent = nl_drop_lang_parent( 'he' );
	if ( ! $parent ) { return new WP_Error( 'parent', 'no brokers page' ); }
	$slug = $slug_base;
	for ( $i = 2; $i < 30; $i++ ) {
		$taken = get_page_by_path( 'brokers/' . $slug, OBJECT, 'page' ) || get_page_by_path( $slug, OBJECT, 'nadlan_professional' );
		if ( ! $taken ) { break; }
		$slug = $slug_base . '-' . $i;
	}
	$names = nl_join_translate_names( $d['areas'], $d['brand'] );
	$pid   = wp_insert_post( array(
		'post_type'    => 'nadlan_professional',
		'post_status'  => $status,
		'post_title'   => $d['name_he'] . ( $d['brand'] !== '' ? ' · ' . $d['brand'] : '' ),
		'post_name'    => $slug,
		'post_content' => '',
		'post_author'  => nl_drop_author(),
	), true );
	if ( is_wp_error( $pid ) || ! $pid ) { return new WP_Error( 'insert', 'insert' ); }
	$token = nl_drop_new_token();
	$meta  = array(
		'profession'      => 'metavech',
		'license_number'  => $d['licence'],
		'company_name'    => $d['brand'],
		'phone'           => $d['phone'],
		'areas_served'    => implode( ',', $d['areas'] ),
		'city'            => $d['areas'][0] ?? '',
		'bio'             => $d['bio'],
		'source'          => 'broker_join',
		'claim_status'    => 'verified',
		'verified_at'     => time(),
		'languages_csv'   => 'עברית',
		'nl_drop_on'      => '1',
		'nl_name_he'      => $d['name_he'],
		'nl_name_en'      => $d['name_en'],
		'nl_brand_en'     => $names['brand_en'],
		'nl_gender'       => $d['gender'],
		'nl_auto_publish' => '1',
		'nl_langs'        => 'he,en',
		'nl_tier'         => 'free',
		'nl_slug'         => $slug,
		'nl_areas_en'     => implode( ',', $names['en'] ),
		'nl_areas_ru'     => implode( ',', $names['ru'] ),
		'nl_areas_fr'     => implode( ',', $names['fr'] ),
	);
	foreach ( $meta as $k => $v ) { update_post_meta( $pid, $k, is_string( $v ) ? wp_slash( $v ) : $v ); }
	update_post_meta( $pid, '_nl_drop_token', $token );
	update_post_meta( $pid, '_nl_email', $d['email'] );
	update_post_meta( $pid, '_nl_signup', wp_slash( wp_json_encode( array(
		'at'       => gmdate( 'c' ),
		'ip'       => nl_join_ip_key(),
		'ua'       => substr( (string) ( $_SERVER['HTTP_USER_AGENT'] ?? '' ), 0, 160 ),
		'lang'     => $d['lang'] ?? 'he',
		'register' => $d['register'],
		'declared' => true,
	), JSON_UNESCAPED_UNICODE ) ) );
	$b    = nl_drop_broker( $pid );
	$site = nl_drop_site_ensure( $b, 'he', $status );
	if ( ! $site ) { return new WP_Error( 'site', 'site' ); }
	$b = nl_drop_broker( $pid );
	nl_drop_site_sync( $b );
	$site_url = (string) get_permalink( $site );
	update_post_meta( $pid, 'website', $site_url );
	$drop = home_url( '/drop/' . $token . '/' );
	$first = trim( (string) preg_split( '/\s+/u', $d['name_he'] )[0] );
	@wp_mail( $d['email'], nl_join_t( 'he', 'mail_s' ), sprintf( nl_join_t( 'he', 'mail_b' ), $first, $site_url, $drop ) );
	@wp_mail( get_option( 'admin_email' ), '[nad-lan] מתווך חדש הצטרף: ' . $d['name_he'], 'רישיון ' . $d['licence'] . "\n" . $site_url . "\n" . admin_url( 'post.php?post=' . $pid . '&action=edit' ) );
	return array( 'ok' => true, 'broker' => (int) $pid, 'site' => $site_url, 'drop' => $drop );
}

/** The link again, only to the email that signed up. The answer never says whether it matched. */
function nl_join_rest_relink( WP_REST_Request $req ) {
	$lang = in_array( (string) $req->get_param( 'lang' ), array( 'he', 'en', 'ru', 'fr' ), true ) ? (string) $req->get_param( 'lang' ) : 'he';
	$ans  = array( 'ok' => true, 'message' => nl_join_t( $lang, 'e_dup_sent' ) );
	if ( nl_join_limited( 'relink', 4, HOUR_IN_SECONDS ) ) { return nl_join_err( 'nljoin_rate', $lang, 'e_rate', 429 ); }
	$licence = preg_replace( '/\D+/', '', (string) $req->get_param( 'licence' ) );
	$email   = sanitize_email( (string) $req->get_param( 'email' ) );
	$pid     = $licence !== '' ? nl_join_by_licence( $licence ) : 0;
	if ( ! $pid || ! is_email( $email ) ) { return $ans; }
	$saved = (string) get_post_meta( $pid, '_nl_email', true );
	if ( $saved === '' || strtolower( $saved ) !== strtolower( $email ) ) { return $ans; }
	$b = function_exists( 'nl_drop_broker' ) ? nl_drop_broker( $pid ) : null;
	if ( ! $b || ! $b['on'] || $b['token'] === '' ) { return $ans; }
	$first = trim( (string) preg_split( '/\s+/u', $b['name_he'] )[0] );
	@wp_mail( $saved, nl_join_t( 'he', 'mail_s' ), sprintf( nl_join_t( 'he', 'mail_b' ), $first, nl_drop_site_url( $b, 'he' ), home_url( '/drop/' . $b['token'] . '/' ) ) );
	return $ans;
}

/* =====================================================================================================
 * Admin: how the broker joined, on the broker's record
 * ===================================================================================================== */
add_action( 'add_meta_boxes_nadlan_professional', function ( $post ) {
	if ( (string) get_post_meta( $post->ID, '_nl_signup', true ) === '' ) { return; }
	add_meta_box( 'nl_join_box', 'הרשמה עצמית', function ( $post ) {
		$s = json_decode( (string) get_post_meta( $post->ID, '_nl_signup', true ), true );
		$e = (string) get_post_meta( $post->ID, '_nl_email', true );
		echo '<p>נרשם: ' . esc_html( $s['at'] ?? '' ) . '</p>';
		echo '<p>בפנקס המתווכים: ' . esc_html( ( $s['register']['name'] ?? '' ) . ( ! empty( $s['register']['city'] ) ? ', ' . $s['register']['city'] : '' ) ) . '</p>';
		echo '<p>מייל (לא מתפרסם): <span dir="ltr">' . esc_html( $e ) . '</span></p>';
		echo '<p class="description">לחסימת אתר: מבטלים את "פעילה" בתיבת הנכסים ומעבירים את עמודי האתר לטיוטה.</p>';
	}, 'nadlan_professional', 'side', 'default' );
} );

add_filter( 'nadlan_config_healthcheck', function ( $out ) {
	$out['broker_join'] = array(
		'version'    => NL_JOIN_VERSION,
		'open'       => get_option( 'nl_join_open', '1' ) === '1',
		'today'      => (int) get_option( 'nljoin_day_' . gmdate( 'Ymd' ), 0 ),
		'joined_all' => count( get_posts( array( 'post_type' => 'nadlan_professional', 'post_status' => 'any', 'fields' => 'ids', 'numberposts' => 1000, 'meta_query' => array( array( 'key' => 'source', 'value' => 'broker_join' ) ), 'suppress_filters' => true ) ) ),
	);
	return $out;
} );
