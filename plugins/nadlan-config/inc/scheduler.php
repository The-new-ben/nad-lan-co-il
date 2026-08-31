<?php
/**
 * scheduler.php - appointment/viewing scheduler (owner order 2026-07-12).
 *
 * "Appointment scheduler to show projects, listings, professionals etc.
 *  Connect it to me by default but make it CMS changeable to paying customers."
 *
 * The law of this module:
 * - EVERY booking defaults to the site owner's single calendar (host id 0).
 *   A per-entity meta (nadlan_sched_host) reassigns a project/listing/
 *   professional to a paying customer's user id; that user then manages
 *   their own hours + WhatsApp number from /my-appointments/.
 * - Availability is data, resolved card meta -> host user meta -> site
 *   default -> hard Israeli default (Sun-Thu 09:00-19:00, Fri 09:00-13:00,
 *   Sat closed). Slot grid step = slot minutes + buffer minutes, so a
 *   buffer between consecutive visits is guaranteed by construction.
 * - Double-booking prevention: transient lock + post-insert first-wins
 *   dedupe (earliest post id keeps the slot, later one is cancelled).
 * - Confirmation channel is a WhatsApp deep link (deliverability-last law:
 *   email sending stays OFF behind nadlan_scheduler_notify_enabled,
 *   default 0; every notice is ALWAYS logged to nadlan_sched_notify_log).
 * - Every booking also mirrors into the existing nadlan_lead machinery so
 *   routing/inbox/AI-qualify see it with zero extra wiring.
 * - Flag nadlan_feature_scheduler, default ON (rentals-manager precedent).
 * - One-of-everything law: NO new floating element. The booking band is an
 *   inline section (#nlsch) appended to single card pages; a small anchor
 *   button is added into the EXISTING CTA rows by the widget JS.
 */
if ( ! defined( 'ABSPATH' ) ) {
	exit;
}

if ( ! function_exists( 'nadlan_sched_on' ) ) {
	function nadlan_sched_on() {
		return get_option( 'nadlan_feature_scheduler', '1' ) === '1';
	}
}

/* ---------- CPT ---------- */
add_action( 'init', function () {
	register_post_type( 'nadlan_appt', array(
		'labels'       => array( 'name' => 'NadLan Appointments', 'singular_name' => 'Appointment' ),
		'public'       => false,
		'show_ui'      => true,
		'show_in_menu' => true,
		'menu_icon'    => 'dashicons-calendar-alt',
		'supports'     => array( 'title', 'custom-fields' ),
	) );
} );

/* ---------- availability model ---------- */
if ( ! function_exists( 'nadlan_sched_default_avail' ) ) {
	function nadlan_sched_default_avail() {
		return array(
			// 0 = Sunday ... 6 = Saturday. Empty string = closed.
			'week'       => array( 0 => '09:00-19:00', 1 => '09:00-19:00', 2 => '09:00-19:00', 3 => '09:00-19:00', 4 => '09:00-19:00', 5 => '09:00-13:00', 6 => '' ),
			'slot_min'   => 30,
			'buffer_min' => 15,
			'lead_hours' => 3,
			'horizon'    => 14,
			'blackout'   => array(),
		);
	}
}

if ( ! function_exists( 'nadlan_sched_clean_avail' ) ) {
	function nadlan_sched_clean_avail( $raw ) {
		if ( is_string( $raw ) ) { $raw = json_decode( $raw, true ); }
		if ( ! is_array( $raw ) ) { return array(); }
		$out = array();
		if ( isset( $raw['week'] ) && is_array( $raw['week'] ) ) {
			$week = array();
			for ( $d = 0; $d <= 6; $d++ ) {
				$v = isset( $raw['week'][ $d ] ) ? trim( (string) $raw['week'][ $d ] ) : '';
				$week[ $d ] = preg_match( '/^([01]\d|2[0-3]):[0-5]\d-([01]\d|2[0-3]):[0-5]\d$/', $v ) ? $v : '';
			}
			$out['week'] = $week;
		}
		foreach ( array( 'slot_min' => array( 10, 180 ), 'buffer_min' => array( 0, 120 ), 'lead_hours' => array( 0, 168 ), 'horizon' => array( 3, 60 ) ) as $k => $lim ) {
			if ( isset( $raw[ $k ] ) && '' !== $raw[ $k ] ) {
				$out[ $k ] = max( $lim[0], min( $lim[1], (int) $raw[ $k ] ) );
			}
		}
		if ( isset( $raw['blackout'] ) && is_array( $raw['blackout'] ) ) {
			$bl = array();
			foreach ( array_slice( $raw['blackout'], 0, 60 ) as $b ) {
				$b = trim( (string) $b );
				if ( preg_match( '/^\d{4}-\d{2}-\d{2}$/', $b ) ) { $bl[] = $b; }
			}
			$out['blackout'] = $bl;
		}
		return $out;
	}
}

if ( ! function_exists( 'nadlan_sched_host_for' ) ) {
	// 0 = the site owner (default for every entity). CMS metabox reassigns.
	function nadlan_sched_host_for( $card_id ) {
		$h = (int) get_post_meta( $card_id, 'nadlan_sched_host', true );
		if ( $h > 0 && get_userdata( $h ) ) { return $h; }
		return 0;
	}
}

if ( ! function_exists( 'nadlan_sched_availability_for' ) ) {
	function nadlan_sched_availability_for( $card_id ) {
		$av = nadlan_sched_default_avail();
		$site = nadlan_sched_clean_avail( get_option( 'nadlan_sched_default_avail', '' ) );
		$av = array_merge( $av, $site );
		$host = nadlan_sched_host_for( $card_id );
		if ( $host > 0 ) {
			$user = nadlan_sched_clean_avail( get_user_meta( $host, 'nadlan_sched_avail', true ) );
			$av = array_merge( $av, $user );
		}
		$card = nadlan_sched_clean_avail( get_post_meta( $card_id, 'nadlan_sched_avail', true ) );
		$av = array_merge( $av, $card );
		if ( empty( $av['blackout'] ) ) { $av['blackout'] = array(); }
		return $av;
	}
}

/* ---------- slot engine ---------- */
if ( ! function_exists( 'nadlan_sched_booked_starts' ) ) {
	function nadlan_sched_booked_starts( $host, $from, $to ) {
		$q = new WP_Query( array(
			'post_type'      => 'nadlan_appt',
			'post_status'    => 'private',
			'posts_per_page' => 500,
			'fields'         => 'ids',
			'no_found_rows'  => true,
			'meta_query'     => array(
				array( 'key' => 'appt_host', 'value' => (string) $host ),
				array( 'key' => 'appt_status', 'value' => 'confirmed' ),
				array( 'key' => 'appt_start', 'value' => array( $from, $to ), 'compare' => 'BETWEEN' ),
			),
		) );
		$out = array();
		foreach ( $q->posts as $pid ) {
			$out[ (string) get_post_meta( $pid, 'appt_start', true ) ] = true;
		}
		return $out;
	}
}

if ( ! function_exists( 'nadlan_sched_slots_for' ) ) {
	function nadlan_sched_slots_for( $card_id ) {
		$av   = nadlan_sched_availability_for( $card_id );
		$host = nadlan_sched_host_for( $card_id );
		$tz   = wp_timezone();
		$now  = new DateTimeImmutable( 'now', $tz );
		$lead = $now->add( new DateInterval( 'PT' . max( 0, (int) $av['lead_hours'] ) . 'H' ) );
		$step = max( 10, (int) $av['slot_min'] ) + max( 0, (int) $av['buffer_min'] );
		$days = max( 3, min( 60, (int) $av['horizon'] ) );
		$booked = nadlan_sched_booked_starts( $host, $now->format( 'Y-m-d 00:00' ), $now->add( new DateInterval( 'P' . ( $days + 1 ) . 'D' ) )->format( 'Y-m-d 23:59' ) );
		$out = array();
		for ( $d = 0; $d < $days; $d++ ) {
			$day  = $now->add( new DateInterval( 'P' . $d . 'D' ) );
			$dow  = (int) $day->format( 'w' );
			$date = $day->format( 'Y-m-d' );
			$hours = isset( $av['week'][ $dow ] ) ? $av['week'][ $dow ] : '';
			$slots = array();
			if ( '' !== $hours && ! in_array( $date, $av['blackout'], true ) ) {
				list( $from, $to ) = array_pad( explode( '-', $hours ), 2, '' );
				$cur = new DateTimeImmutable( $date . ' ' . $from, $tz );
				$end = new DateTimeImmutable( $date . ' ' . $to, $tz );
				$fit = new DateInterval( 'PT' . max( 10, (int) $av['slot_min'] ) . 'M' );
				while ( $cur->add( $fit ) <= $end ) {
					$key = $cur->format( 'Y-m-d H:i' );
					if ( $cur >= $lead && ! isset( $booked[ $key ] ) ) {
						$slots[] = $cur->format( 'H:i' );
					}
					$cur = $cur->add( new DateInterval( 'PT' . $step . 'M' ) );
				}
			}
			$out[] = array( 'date' => $date, 'dow' => $dow, 'slots' => $slots );
		}
		return array( 'days' => $out, 'slot_min' => (int) $av['slot_min'], 'host' => $host );
	}
}

/* ---------- helpers ---------- */
if ( ! function_exists( 'nadlan_sched_private_card' ) ) {
	/** Opaque boundary shared by slot discovery and booking mutation. */
	function nadlan_sched_private_card( $card_id ) {
		$card_id = absint( $card_id );
		return $card_id > 0 && 'nadlan_project' === get_post_type( $card_id ) && (
			( function_exists( 'nadlan_unit_journey_is_private_lab' )
				&& nadlan_unit_journey_is_private_lab( $card_id ) )
			|| 'private-unit-journey-v2' === (string) get_post_meta( $card_id, '_nadlan_private_unit_journey', true )
		);
	}
}

if ( ! function_exists( 'nadlan_sched_valid_card' ) ) {
	// the scheduler serves international projects too (owner 2026-07-12)
	function nadlan_sched_valid_card( $card_id ) {
		$card_id = absint( $card_id );
		if ( ! $card_id ) { return 0; }
		if ( nadlan_sched_private_card( $card_id ) ) { return 0; }
		$post = get_post( $card_id );
		return ( $post && in_array( $post->post_type, array( 'nadlan_professional', 'nadlan_project', 'nadlan_property', 'nadlan_intl' ), true ) ) ? $card_id : 0;
	}
}

if ( ! function_exists( 'nadlan_sched_kind_for' ) ) {
	function nadlan_sched_kind_for( $card_id ) {
		$t = get_post_type( $card_id );
		if ( 'nadlan_professional' === $t ) { return 'meeting'; }
		if ( 'nadlan_property' === $t ) { return 'visit'; }
		if ( 'nadlan_intl' === $t ) { return 'meeting'; }
		return 'tour';
	}
}

if ( ! function_exists( 'nadlan_sched_wa_number' ) ) {
	function nadlan_sched_wa_number( $host ) {
		if ( $host > 0 ) {
			$n = preg_replace( '/[^0-9]/', '', (string) get_user_meta( $host, 'nadlan_sched_wa', true ) );
			if ( strlen( $n ) >= 10 ) { return $n; }
		}
		if ( function_exists( 'nadlan_cta_whatsapp_number' ) ) {
			$n = preg_replace( '/[^0-9]/', '', (string) nadlan_cta_whatsapp_number() );
			if ( strlen( $n ) >= 10 ) { return $n; }
		}
		return preg_replace( '/[^0-9]/', '', (string) get_option( 'nadlan_whatsapp_e164', '' ) );
	}
}

if ( ! function_exists( 'nadlan_sched_utc' ) ) {
	function nadlan_sched_utc( $local ) {
		$dt = new DateTimeImmutable( $local, wp_timezone() );
		return $dt->setTimezone( new DateTimeZone( 'UTC' ) )->format( 'Ymd\THis\Z' );
	}
}

if ( ! function_exists( 'nadlan_sched_queue_notice' ) ) {
	// ALWAYS logs; sends only when nadlan_scheduler_notify_enabled = 1 (default OFF).
	function nadlan_sched_queue_notice( $to, $subject, $body ) {
		$log = get_option( 'nadlan_sched_notify_log', array() );
		if ( ! is_array( $log ) ) { $log = array(); }
		$sent = get_option( 'nadlan_scheduler_notify_enabled', '0' ) === '1';
		array_unshift( $log, array( 'at' => current_time( 'Y-m-d H:i' ), 'to' => $to, 'subject' => $subject, 'sent' => $sent ) );
		update_option( 'nadlan_sched_notify_log', array_slice( $log, 0, 40 ), false );
		if ( $sent && $to ) { wp_mail( $to, $subject, $body ); }
	}
}

if ( ! function_exists( 'nadlan_sched_host_email' ) ) {
	function nadlan_sched_host_email( $host ) {
		if ( $host > 0 ) {
			$u = get_userdata( $host );
			if ( $u && $u->user_email ) { return $u->user_email; }
		}
		return get_option( 'admin_email' );
	}
}

/* ---------- strings (he/en app table; other langs coerce to en) ---------- */
if ( ! function_exists( 'nadlan_sched_strings' ) ) {
	function nadlan_sched_strings( $lang = 'he' ) {
		$he = array(
			'kicker'     => 'תיאום מועד',
			'title_tour' => 'בקשה לתיאום סיור בפרויקט', 'title_visit' => 'תיאום ביקור בנכס', 'title_meeting' => 'קביעת פגישת ייעוץ',
			'sub'        => 'בוחרים יום ושעה נוחים ושולחים בקשה. המועד כפוף לאישור הגורם המוסמך בפרויקט. ללא תשלום וללא התחייבות.',
			'pick_day'   => 'בחירת יום', 'pick_time' => 'בחירת שעה', 'details' => 'פרטים לאישור',
			'no_slots'   => 'אין מועדים פנויים בימים הקרובים. אפשר לפנות אלינו ישירות בוואטסאפ.',
			'day_names'  => array( 'יום א', 'יום ב', 'יום ג', 'יום ד', 'יום ה', 'יום ו', 'שבת' ),
			'today'      => 'היום', 'tomorrow' => 'מחר', 'closed' => 'סגור',
			'f_name'     => 'שם מלא', 'f_phone' => 'טלפון נייד', 'f_email' => 'אימייל (לא חובה)', 'f_note' => 'הערה (לא חובה)',
			'selected'   => 'המועד שנבחר', 'minutes' => 'דקות',
			'submit'     => 'שליחת הבקשה', 'sending' => 'שולחים את הבקשה...',
			'ok_title'   => 'הבקשה נקלטה', 'ok_sub' => 'המועד המבוקש נרשם אצלנו. קיום הסיור כפוף לאישור היזם או המשווק. אסמכתא:',
			'wa_btn'     => 'שליחת הבקשה בוואטסאפ', 'ics_btn' => 'הוספה ליומן (ICS)', 'gcal_btn' => 'יומן Google',
			'cancel_btn' => 'ביטול המועד', 'cancelled' => 'המועד בוטל.',
			'err_taken'  => 'המועד הזה נתפס הרגע. בחרו מועד אחר.',
			'err_generic'=> 'משהו השתבש. נסו שוב או פנו אלינו בוואטסאפ.',
			'err_fields' => 'צריך שם וטלפון כדי לקבוע.',
			'book_anchor'=> 'תיאום מועד ביומן',
			'wa_text'    => 'שלום, ביקשתי לתאם {kind} - {card} בתאריך {date} בשעה {time}. שם: {name}. אסמכתא: {ref}',
			'kind_tour'  => 'סיור בפרויקט', 'kind_visit' => 'ביקור בנכס', 'kind_meeting' => 'פגישת ייעוץ',
			'honest'     => 'נדלן אינה קובעת ביקורים בשם היזם. הבקשה מועברת לגורם המוסמך בפרויקט ואישור סופי יגיע בוואטסאפ. שינוי או ביטול - בכפתור הביטול או בוואטסאפ.',
		);
		$en = array(
			'kicker'     => 'Book a time',
			'title_tour' => 'Request a project tour', 'title_visit' => 'Schedule a property visit', 'title_meeting' => 'Book a consultation',
			'sub'        => 'Pick a convenient day and time and send a request. The slot is subject to confirmation by the project team. Free, no commitment.',
			'pick_day'   => 'Pick a day', 'pick_time' => 'Pick a time', 'details' => 'Your details',
			'no_slots'   => 'No open times in the coming days. You can reach us directly on WhatsApp.',
			'day_names'  => array( 'Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat' ),
			'today'      => 'Today', 'tomorrow' => 'Tomorrow', 'closed' => 'Closed',
			'f_name'     => 'Full name', 'f_phone' => 'Mobile phone', 'f_email' => 'Email (optional)', 'f_note' => 'Note (optional)',
			'selected'   => 'Selected time', 'minutes' => 'minutes',
			'submit'     => 'Confirm this time', 'sending' => 'Booking...',
			'ok_title'   => 'Request received', 'ok_sub' => 'Your requested time is recorded. The tour itself is subject to developer or marketer confirmation. Reference:',
			'wa_btn'     => 'Send the request on WhatsApp', 'ics_btn' => 'Add to calendar (ICS)', 'gcal_btn' => 'Google Calendar',
			'cancel_btn' => 'Cancel this appointment', 'cancelled' => 'The appointment was cancelled.',
			'err_taken'  => 'That time was just taken. Please pick another.',
			'err_generic'=> 'Something went wrong. Try again or reach us on WhatsApp.',
			'err_fields' => 'Name and phone are required.',
			'book_anchor'=> 'Book a time',
			'wa_text'    => 'Hello, I requested a {kind} - {card} on {date} at {time}. Name: {name}. Ref: {ref}',
			'kind_tour'  => 'project tour', 'kind_visit' => 'property visit', 'kind_meeting' => 'consultation',
			'honest'     => 'Nadlan does not schedule visits on behalf of the developer. Your request is forwarded to the authorized project team and final confirmation arrives on WhatsApp.',
		);
		$fr = array(
			'kicker'     => 'Prise de rendez-vous',
			'title_tour' => 'Demander une visite du projet', 'title_visit' => 'Planifier une visite du bien', 'title_meeting' => 'Réserver une consultation',
			'sub'        => 'Choisissez un jour et une heure et envoyez une demande. Le créneau est soumis à la confirmation de l’équipe du projet. Gratuit et sans engagement.',
			'pick_day'   => 'Choisir un jour', 'pick_time' => 'Choisir une heure', 'details' => 'Vos coordonnées',
			'no_slots'   => 'Aucun créneau disponible ces prochains jours. Contactez-nous directement sur WhatsApp.',
			'day_names'  => array( 'Dim', 'Lun', 'Mar', 'Mer', 'Jeu', 'Ven', 'Sam' ),
			'today'      => 'Aujourd’hui', 'tomorrow' => 'Demain', 'closed' => 'Fermé',
			'f_name'     => 'Nom complet', 'f_phone' => 'Téléphone portable', 'f_email' => 'Email (facultatif)', 'f_note' => 'Remarque (facultatif)',
			'selected'   => 'Créneau choisi', 'minutes' => 'minutes',
			'submit'     => 'Confirmer le créneau', 'sending' => 'Réservation...',
			'ok_title'   => 'Demande reçue', 'ok_sub' => 'Votre créneau est enregistré. La visite reste soumise à la confirmation du promoteur. Référence:',
			'wa_btn'     => 'Envoyer la confirmation WhatsApp', 'ics_btn' => 'Ajouter au calendrier (ICS)', 'gcal_btn' => 'Google Agenda',
			'cancel_btn' => 'Annuler le rendez-vous', 'cancelled' => 'Le rendez-vous a été annulé.',
			'err_taken'  => 'Ce créneau vient d’être pris. Choisissez-en un autre.',
			'err_generic'=> 'Une erreur est survenue. Réessayez ou contactez-nous sur WhatsApp.',
			'err_fields' => 'Le nom et le téléphone sont requis.',
			'book_anchor'=> 'Prendre rendez-vous',
			'wa_text'    => 'Bonjour, j’ai demandé {kind} - {card} le {date} à {time}. Nom: {name}. Réf: {ref}',
			'kind_tour'  => 'une visite du projet', 'kind_visit' => 'une visite du bien', 'kind_meeting' => 'une consultation',
			'honest'     => 'Nadlan ne fixe pas de visites au nom du promoteur. La demande est transmise à l’équipe autorisée et la confirmation finale arrive par WhatsApp.',
		);
		$ru = array(
			'kicker'     => 'Запись на встречу',
			'title_tour' => 'Запросить экскурсию по проекту', 'title_visit' => 'Записаться на просмотр квартиры', 'title_meeting' => 'Записаться на консультацию',
			'sub'        => 'Выберите удобные день и время и отправьте запрос. Время подлежит подтверждению командой проекта. Бесплатно и без обязательств.',
			'pick_day'   => 'Выберите день', 'pick_time' => 'Выберите время', 'details' => 'Ваши данные',
			'no_slots'   => 'Нет свободного времени в ближайшие дни. Свяжитесь с нами напрямую в WhatsApp.',
			'day_names'  => array( 'Вс', 'Пн', 'Вт', 'Ср', 'Чт', 'Пт', 'Сб' ),
			'today'      => 'Сегодня', 'tomorrow' => 'Завтра', 'closed' => 'Закрыто',
			'f_name'     => 'Полное имя', 'f_phone' => 'Мобильный телефон', 'f_email' => 'Email (необязательно)', 'f_note' => 'Комментарий (необязательно)',
			'selected'   => 'Выбранное время', 'minutes' => 'минут',
			'submit'     => 'Подтвердить время', 'sending' => 'Бронируем...',
			'ok_title'   => 'Запрос получен', 'ok_sub' => 'Запрошенное время записано. Проведение экскурсии подлежит подтверждению застройщика. Номер:',
			'wa_btn'     => 'Отправить подтверждение в WhatsApp', 'ics_btn' => 'Добавить в календарь (ICS)', 'gcal_btn' => 'Google Календарь',
			'cancel_btn' => 'Отменить встречу', 'cancelled' => 'Встреча отменена.',
			'err_taken'  => 'Это время только что заняли. Выберите другое.',
			'err_generic'=> 'Что-то пошло не так. Попробуйте снова или напишите нам в WhatsApp.',
			'err_fields' => 'Нужны имя и телефон.',
			'book_anchor'=> 'Записаться на встречу',
			'wa_text'    => 'Здравствуйте, я запросил {kind} - {card} {date} в {time}. Имя: {name}. Номер: {ref}',
			'kind_tour'  => 'экскурсию по проекту', 'kind_visit' => 'просмотр квартиры', 'kind_meeting' => 'консультацию',
			'honest'     => 'Nadlan не назначает визиты от имени застройщика. Запрос передается уполномоченной команде, финальное подтверждение придет в WhatsApp.',
		);
		$ar = array(
			'kicker'     => 'حجز موعد',
			'title_tour' => 'طلب جولة في المشروع', 'title_visit' => 'حجز زيارة للعقار', 'title_meeting' => 'حجز استشارة',
			'sub'        => 'اختاروا يوماً وساعة مناسبين وأرسلوا طلباً. الموعد خاضع لتأكيد فريق المشروع. مجاناً وبدون التزام.',
			'pick_day'   => 'اختيار اليوم', 'pick_time' => 'اختيار الساعة', 'details' => 'تفاصيلكم',
			'no_slots'   => 'لا توجد مواعيد متاحة في الأيام القريبة. تواصلوا معنا مباشرة عبر واتساب.',
			'day_names'  => array( 'الأحد', 'الاثنين', 'الثلاثاء', 'الأربعاء', 'الخميس', 'الجمعة', 'السبت' ),
			'today'      => 'اليوم', 'tomorrow' => 'غداً', 'closed' => 'مغلق',
			'f_name'     => 'الاسم الكامل', 'f_phone' => 'الهاتف المحمول', 'f_email' => 'البريد الإلكتروني (اختياري)', 'f_note' => 'ملاحظة (اختياري)',
			'selected'   => 'الموعد المختار', 'minutes' => 'دقيقة',
			'submit'     => 'تأكيد الموعد', 'sending' => 'جارٍ الحجز...',
			'ok_title'   => 'تم استلام الطلب', 'ok_sub' => 'تم تسجيل الموعد المطلوب. إجراء الجولة خاضع لتأكيد المطور أو المسوق. رقم المرجع:',
			'wa_btn'     => 'إرسال التأكيد عبر واتساب', 'ics_btn' => 'إضافة إلى التقويم (ICS)', 'gcal_btn' => 'تقويم Google',
			'cancel_btn' => 'إلغاء الموعد', 'cancelled' => 'تم إلغاء الموعد.',
			'err_taken'  => 'تم حجز هذا الموعد للتو. اختاروا موعداً آخر.',
			'err_generic'=> 'حدث خطأ ما. حاولوا مجدداً أو تواصلوا معنا عبر واتساب.',
			'err_fields' => 'الاسم والهاتف مطلوبان.',
			'book_anchor'=> 'حجز موعد',
			'wa_text'    => 'مرحباً، طلبت تنسيق {kind} - {card} بتاريخ {date} الساعة {time}. الاسم: {name}. المرجع: {ref}',
			'kind_tour'  => 'جولة في المشروع', 'kind_visit' => 'زيارة للعقار', 'kind_meeting' => 'استشارة',
			'honest'     => 'ندلان لا تحدد زيارات باسم المطور. يُحال الطلب إلى الجهة المخولة ويصل التأكيد النهائي عبر واتساب.',
		);
		$all = array( 'he' => $he, 'en' => $en, 'fr' => $fr, 'ru' => $ru, 'ar' => $ar );
		return isset( $all[ $lang ] ) ? $all[ $lang ] : $en;
	}
}

if ( ! function_exists( 'nadlan_sched_page_lang' ) ) {
	// Sibling pages carry a -en/-fr/-ru/-ar slug suffix (project-experience convention).
	function nadlan_sched_page_lang( $post_id ) {
		if ( 'nadlan_intl' === get_post_type( $post_id ) && isset( $_GET['lang'] ) ) { // phpcs:ignore
			$q = sanitize_key( wp_unslash( $_GET['lang'] ) ); // phpcs:ignore
			if ( in_array( $q, array( 'en', 'ar' ), true ) ) { return $q; }
		}
		$slug = (string) get_post_field( 'post_name', $post_id );
		foreach ( array( 'en', 'fr', 'ru', 'ar' ) as $ml ) {
			if ( substr( $slug, -3 ) === '-' . $ml ) { return $ml; }
		}
		return function_exists( 'nadlan_current_lang' ) ? nadlan_current_lang() : 'he';
	}
}

/* ---------- REST ---------- */
add_action( 'rest_api_init', function () {
	if ( ! nadlan_sched_on() ) { return; }

	register_rest_route( 'nadlan/v1', '/appt-slots', array(
		'methods'             => 'GET',
		'permission_callback' => '__return_true',
		'callback'            => function ( WP_REST_Request $req ) {
			$requested_card = (int) $req->get_param( 'card' );
			if ( nadlan_sched_private_card( $requested_card ) ) {
				return new WP_Error( 'not_found', 'not found', array( 'status' => 404 ) );
			}
			$card = nadlan_sched_valid_card( $requested_card );
			if ( ! $card ) { return new WP_Error( 'invalid', 'invalid card', array( 'status' => 400 ) ); }
			$data = nadlan_sched_slots_for( $card );
			$data['kind'] = nadlan_sched_kind_for( $card );
			unset( $data['host'] );
			return $data;
		},
	) );

	register_rest_route( 'nadlan/v1', '/appt-book', array(
		'methods'             => 'POST',
		'permission_callback' => '__return_true',
		'callback'            => function ( WP_REST_Request $req ) {
			$p = $req->get_json_params() ?: array();
			$requested_card = (int) ( $p['card'] ?? 0 );
			if ( nadlan_sched_private_card( $requested_card ) ) {
				return new WP_Error( 'not_found', 'not found', array( 'status' => 404 ) );
			}
			if ( '' !== (string) ( $p['company'] ?? '' ) ) { return new WP_Error( 'spam', 'spam', array( 'status' => 400 ) ); }
			$card  = nadlan_sched_valid_card( $requested_card );
			$start = sanitize_text_field( (string) ( $p['start'] ?? '' ) );
			$name  = sanitize_text_field( (string) ( $p['name'] ?? '' ) );
			$phone = preg_replace( '/[^0-9+]/', '', (string) ( $p['phone'] ?? '' ) );
			$email = sanitize_email( (string) ( $p['email'] ?? '' ) );
			$note  = sanitize_textarea_field( (string) ( $p['note'] ?? '' ) );
			$lang  = in_array( (string) ( $p['lang'] ?? 'he' ), array( 'he', 'en', 'fr', 'ru', 'ar' ), true ) ? (string) $p['lang'] : 'he';
			if ( ! $card || ! preg_match( '/^\d{4}-\d{2}-\d{2} \d{2}:\d{2}$/', $start ) ) {
				return new WP_Error( 'invalid', 'invalid request', array( 'status' => 400 ) );
			}
			if ( '' === $name || strlen( $phone ) < 9 ) {
				return new WP_Error( 'fields', 'name and phone required', array( 'status' => 400 ) );
			}
			$ip = $_SERVER['REMOTE_ADDR'] ?? '0';
			$tk = 'nlsch_rl_' . md5( $ip );
			$ct = (int) get_transient( $tk );
			if ( $ct >= 5 ) { return new WP_Error( 'rate', 'too many requests', array( 'status' => 429 ) ); }
			set_transient( $tk, $ct + 1, HOUR_IN_SECONDS );

			// The requested start must be a currently-open slot.
			$data = nadlan_sched_slots_for( $card );
			$open = false;
			list( $req_date, $req_time ) = explode( ' ', $start );
			foreach ( $data['days'] as $d ) {
				if ( $d['date'] === $req_date && in_array( $req_time, $d['slots'], true ) ) { $open = true; break; }
			}
			$host = nadlan_sched_host_for( $card );
			$lock = 'nlsch_lock_' . md5( $host . '|' . $start );
			if ( ! $open || get_transient( $lock ) ) {
				return new WP_Error( 'slot_taken', 'slot taken', array( 'status' => 409 ) );
			}
			set_transient( $lock, 1, 30 );

			$card_post = get_post( $card );
			$card_title = $card_post ? $card_post->post_title : '';
			$tz  = wp_timezone();
			$end = ( new DateTimeImmutable( $start, $tz ) )->add( new DateInterval( 'PT' . (int) $data['slot_min'] . 'M' ) )->format( 'Y-m-d H:i' );
			$token = strtolower( wp_generate_password( 24, false, false ) );
			$aid = wp_insert_post( array(
				'post_type'   => 'nadlan_appt',
				'post_status' => 'private',
				'post_title'  => $name . ' - ' . $card_title . ' - ' . $start,
			), true );
			if ( is_wp_error( $aid ) ) { return $aid; }
			foreach ( array(
				'appt_card' => $card, 'appt_host' => $host, 'appt_start' => $start, 'appt_end' => $end,
				'appt_status' => 'confirmed', 'appt_token' => $token, 'appt_lang' => $lang,
				'name' => $name, 'phone' => $phone, 'email' => $email, 'note' => $note,
			) as $mk => $mv ) {
				if ( '' !== $mv || 'email' !== $mk ) { update_post_meta( $aid, $mk, $mv ); }
			}

			// First-wins dedupe: earliest post id keeps the slot.
			$dups = get_posts( array(
				'post_type' => 'nadlan_appt', 'post_status' => 'private', 'fields' => 'ids',
				'posts_per_page' => 5, 'orderby' => 'ID', 'order' => 'ASC', 'no_found_rows' => true,
				'meta_query' => array(
					array( 'key' => 'appt_host', 'value' => (string) $host ),
					array( 'key' => 'appt_start', 'value' => $start ),
					array( 'key' => 'appt_status', 'value' => 'confirmed' ),
				),
			) );
			if ( $dups && (int) $dups[0] !== (int) $aid ) {
				update_post_meta( $aid, 'appt_status', 'cancelled' );
				return new WP_Error( 'slot_taken', 'slot taken', array( 'status' => 409 ) );
			}

			// Mirror into the lead machinery (routing/inbox see every booking).
			$kind = nadlan_sched_kind_for( $card );
			$lid = wp_insert_post( array(
				'post_type'    => 'nadlan_lead',
				'post_status'  => 'private',
				'post_title'   => $name . ' - appointment - ' . current_time( 'Y-m-d H:i' ),
				'post_content' => 'appointment ' . $kind . ' ' . $start . ( $note ? "\n" . $note : '' ),
			), true );
			if ( ! is_wp_error( $lid ) ) {
				update_post_meta( $lid, 'name', $name );
				update_post_meta( $lid, 'phone', $phone );
				if ( $email ) { update_post_meta( $lid, 'email', $email ); }
				update_post_meta( $lid, 'goal', 'appointment' );
				update_post_meta( $lid, 'lead_card_id', $card );
				update_post_meta( $lid, 'appt_id', $aid );
				if ( function_exists( 'nadlan_lead_route' ) ) {
					nadlan_lead_route( $lid, $card, array( 'name' => $name, 'phone' => $phone, 'email' => $email, 'goal' => 'appointment' ), 'scheduler' );
				}
			}

			$ref = strtoupper( substr( md5( $aid . $token ), 0, 6 ) );
			update_post_meta( $aid, 'appt_ref', $ref );
			nadlan_sched_queue_notice(
				nadlan_sched_host_email( $host ),
				'[נדלן] פגישה חדשה - ' . $card_title . ' - ' . $start,
				"פגישה חדשה נקבעה\n\nנכס: $card_title\nמועד: $start\nשם: $name\nטלפון: $phone\nהערה: $note\nאסמכתא: $ref\n\nניהול: " . home_url( '/my-appointments/' )
			);

			$s = nadlan_sched_strings( $lang );
			$kind_lbl = $s[ 'kind_' . $kind ];
			$wa_num = nadlan_sched_wa_number( $host );
			$wa_txt = strtr( $s['wa_text'], array( '{kind}' => $kind_lbl, '{card}' => $card_title, '{date}' => $req_date, '{time}' => $req_time, '{name}' => $name, '{ref}' => $ref ) );
			return array(
				'ok'        => true,
				'id'        => $aid,
				'token'     => $token,
				'ref'       => $ref,
				'start'     => $start,
				'end'       => $end,
				'utc_start' => nadlan_sched_utc( $start ),
				'utc_end'   => nadlan_sched_utc( $end ),
				'card'      => $card_title,
				'url'       => get_permalink( $card ),
				'whatsapp'  => $wa_num ? 'https://wa.me/' . $wa_num . '?text=' . rawurlencode( $wa_txt ) : '',
				'ics'       => rest_url( 'nadlan/v1/appt-ics/' . $aid ) . '?t=' . $token,
			);
		},
	) );

	register_rest_route( 'nadlan/v1', '/appt-cancel', array(
		'methods'             => 'POST',
		'permission_callback' => '__return_true',
		'callback'            => function ( WP_REST_Request $req ) {
			$p = $req->get_json_params() ?: array();
			$id = (int) ( $p['id'] ?? 0 );
			$token = sanitize_text_field( (string) ( $p['token'] ?? '' ) );
			if ( ! $id || '' === $token || get_post_type( $id ) !== 'nadlan_appt' ) {
				return new WP_Error( 'invalid', 'invalid', array( 'status' => 400 ) );
			}
			if ( ! hash_equals( (string) get_post_meta( $id, 'appt_token', true ), $token ) ) {
				return new WP_Error( 'forbidden', 'forbidden', array( 'status' => 403 ) );
			}
			update_post_meta( $id, 'appt_status', 'cancelled' );
			return array( 'ok' => true );
		},
	) );

	register_rest_route( 'nadlan/v1', '/appt-ics/(?P<id>\d+)', array(
		'methods'             => 'GET',
		'permission_callback' => '__return_true',
		'callback'            => function ( WP_REST_Request $req ) {
			$id = (int) $req['id'];
			$t  = sanitize_text_field( (string) $req->get_param( 't' ) );
			if ( get_post_type( $id ) !== 'nadlan_appt' || '' === $t
				|| ! hash_equals( (string) get_post_meta( $id, 'appt_token', true ), $t ) ) {
				return new WP_Error( 'forbidden', 'forbidden', array( 'status' => 403 ) );
			}
			$card  = (int) get_post_meta( $id, 'appt_card', true );
			$card_post = $card ? get_post( $card ) : null;
			$title = $card_post ? $card_post->post_title : 'NadLan';
			$start = (string) get_post_meta( $id, 'appt_start', true );
			$end   = (string) get_post_meta( $id, 'appt_end', true );
			$esc   = function ( $v ) { return str_replace( array( '\\', ';', ',', "\n" ), array( '\\\\', '\;', '\,', '\n' ), (string) $v ); };
			$ics = "BEGIN:VCALENDAR\r\nVERSION:2.0\r\nPRODID:-//NadLan//Scheduler//HE\r\nBEGIN:VEVENT\r\n"
				. 'UID:appt-' . $id . "@nad-lan.co.il\r\n"
				. 'DTSTAMP:' . gmdate( 'Ymd\THis\Z' ) . "\r\n"
				. 'DTSTART:' . nadlan_sched_utc( $start ) . "\r\n"
				. 'DTEND:' . nadlan_sched_utc( $end ) . "\r\n"
				. 'SUMMARY:' . $esc( 'נדלן: ' . $title ) . "\r\n"
				. 'DESCRIPTION:' . $esc( 'אסמכתא ' . get_post_meta( $id, 'appt_ref', true ) . ' - ' . home_url( '/' ) ) . "\r\n"
				. ( $card ? 'URL:' . $esc( get_permalink( $card ) ) . "\r\n" : '' )
				. "END:VEVENT\r\nEND:VCALENDAR\r\n";
			nocache_headers();
			header( 'Content-Type: text/calendar; charset=utf-8' );
			header( 'Content-Disposition: attachment; filename="nadlan-appointment-' . $id . '.ics"' );
			header( 'X-Robots-Tag: noindex' );
			echo $ics; // phpcs:ignore
			exit;
		},
	) );

	register_rest_route( 'nadlan/v1', '/my-appts', array(
		'methods'             => 'GET',
		'permission_callback' => function () { return is_user_logged_in(); },
		'callback'            => function () {
			return array( 'items' => nadlan_sched_list_for_user( get_current_user_id() ) );
		},
	) );

	register_rest_route( 'nadlan/v1', '/appt-status', array(
		'methods'             => 'POST',
		'permission_callback' => function () { return is_user_logged_in(); },
		'callback'            => function ( WP_REST_Request $req ) {
			$p = $req->get_json_params() ?: array();
			$id = (int) ( $p['id'] ?? 0 );
			$status = sanitize_key( (string) ( $p['status'] ?? '' ) );
			if ( ! $id || get_post_type( $id ) !== 'nadlan_appt'
				|| ! in_array( $status, array( 'confirmed', 'done', 'noshow', 'cancelled' ), true ) ) {
				return new WP_Error( 'invalid', 'invalid', array( 'status' => 400 ) );
			}
			$host = (int) get_post_meta( $id, 'appt_host', true );
			$uid  = get_current_user_id();
			if ( ! current_user_can( 'manage_options' ) && $host !== $uid ) {
				return new WP_Error( 'forbidden', 'forbidden', array( 'status' => 403 ) );
			}
			update_post_meta( $id, 'appt_status', $status );
			return array( 'ok' => true, 'status' => $status );
		},
	) );

	register_rest_route( 'nadlan/v1', '/my-availability', array(
		'methods'             => 'POST',
		'permission_callback' => function () { return is_user_logged_in(); },
		'callback'            => function ( WP_REST_Request $req ) {
			$p = $req->get_json_params() ?: array();
			$clean = nadlan_sched_clean_avail( $p );
			$uid = get_current_user_id();
			if ( current_user_can( 'manage_options' ) ) {
				update_option( 'nadlan_sched_default_avail', wp_json_encode( $clean ), false );
			} else {
				update_user_meta( $uid, 'nadlan_sched_avail', wp_json_encode( $clean ) );
			}
			$wa = preg_replace( '/[^0-9]/', '', (string) ( $p['wa'] ?? '' ) );
			if ( '' !== $wa && ! current_user_can( 'manage_options' ) ) {
				update_user_meta( $uid, 'nadlan_sched_wa', $wa );
			}
			return array( 'ok' => true, 'saved' => $clean );
		},
	) );
} );

if ( ! function_exists( 'nadlan_sched_list_for_user' ) ) {
	function nadlan_sched_list_for_user( $uid ) {
		$admin = user_can( $uid, 'manage_options' );
		$meta = array( array( 'key' => 'appt_start', 'value' => gmdate( 'Y-m-d 00:00', time() - 7 * DAY_IN_SECONDS ), 'compare' => '>=' ) );
		if ( ! $admin ) {
			$meta[] = array( 'key' => 'appt_host', 'value' => (string) $uid );
		}
		$q = new WP_Query( array(
			'post_type' => 'nadlan_appt', 'post_status' => 'private', 'posts_per_page' => 120,
			'no_found_rows' => true, 'meta_key' => 'appt_start', 'orderby' => 'meta_value', 'order' => 'ASC',
			'meta_query' => $meta,
		) );
		$items = array();
		foreach ( $q->posts as $p ) {
			$card = (int) get_post_meta( $p->ID, 'appt_card', true );
			$card_post = $card ? get_post( $card ) : null;
			$phone = (string) get_post_meta( $p->ID, 'phone', true );
			$items[] = array(
				'id'     => $p->ID,
				'start'  => (string) get_post_meta( $p->ID, 'appt_start', true ),
				'status' => (string) get_post_meta( $p->ID, 'appt_status', true ),
				'name'   => (string) get_post_meta( $p->ID, 'name', true ),
				'phone'  => $phone,
				'wa'     => $phone ? 'https://wa.me/' . preg_replace( '/[^0-9]/', '', ( 0 === strpos( $phone, '0' ) ? '972' . substr( $phone, 1 ) : $phone ) ) : '',
				'note'   => (string) get_post_meta( $p->ID, 'note', true ),
				'ref'    => (string) get_post_meta( $p->ID, 'appt_ref', true ),
				'card'   => $card_post ? $card_post->post_title : '',
				'card_url' => $card_post ? get_permalink( $card_post ) : '',
			);
		}
		return $items;
	}
}

/* ---------- the booking band on single card pages ---------- */
add_filter( 'the_content', function ( $content ) {
	if ( ! nadlan_sched_on() || ! is_singular( array( 'nadlan_project', 'nadlan_property', 'nadlan_professional', 'nadlan_intl' ) ) || ! in_the_loop() || ! is_main_query() ) {
		return $content;
	}
	static $done = false;
	if ( $done ) { return $content; }
	$card = get_the_ID();
	if ( get_post_meta( $card, 'nadlan_sched_off', true ) === '1' ) { return $content; }
	/* Review mode (owner order 31.8.2026): no choose-a-date block on review
	 * project pages - it reads like the developer's own sales surface. */
	if ( 'nadlan_project' === get_post_type( $card ) && function_exists( 'nadlan_project_mode' ) && 'showroom' !== nadlan_project_mode( $card ) ) { return $content; }
	$done = true;
	$wlang = nadlan_sched_page_lang( $card );
	$s = nadlan_sched_strings( $wlang );
	$kind = nadlan_sched_kind_for( $card );
	$js = plugins_url( 'assets/scheduler/booking.js', dirname( __FILE__ ) ) . '?v=' . rawurlencode( defined( 'NADLAN_CONFIG_VERSION' ) ? NADLAN_CONFIG_VERSION : '1' );
	ob_start();
	?>
<section id="nlsch" class="nlsch" dir="<?php echo in_array( $wlang, array( 'he', 'ar' ), true ) ? 'rtl' : 'ltr'; ?>">
	<style>
	.nlsch{background:#F3EEE3;border:1px solid #E2DCD0;border-radius:22px;padding:26px 22px;margin:34px 0;font-family:Heebo,sans-serif;color:#1B1A17}
	.nlsch-kicker{font:700 12.5px Heebo;letter-spacing:.06em;color:#9C7A3C;text-transform:uppercase;margin:0 0 6px}
	.nlsch h2{font-family:"Frank Ruhl Libre",Georgia,serif;font-size:1.45rem;margin:0 0 6px}
	.nlsch-sub{font:400 14px/1.65 Heebo;color:#51483A;margin:0 0 18px;max-width:560px}
	.nlsch-lbl{font:700 13px Heebo;color:#51483A;margin:16px 0 8px}
	.nlsch-days{display:flex;gap:8px;overflow-x:auto;padding-bottom:6px;-webkit-overflow-scrolling:touch}
	.nlsch-day{flex:0 0 auto;min-width:64px;background:#fff;border:1px solid #E2DCD0;border-radius:14px;padding:10px 8px;text-align:center;cursor:pointer;font:600 12px Heebo;color:#51483A}
	.nlsch-day b{display:block;font:700 17px "Frank Ruhl Libre",serif;color:#1B1A17;margin-top:2px}
	.nlsch-day.is-on{background:#1B1A17;color:#E9D9A8;border-color:#1B1A17}
	.nlsch-day.is-on b{color:#FAF7F1}
	.nlsch-day.is-off{opacity:.42;cursor:default}
	.nlsch-times{display:flex;gap:8px;flex-wrap:wrap;margin-top:4px}
	.nlsch-time{background:#fff;border:1px solid #E2DCD0;border-radius:999px;padding:9px 16px;font:600 13.5px Heebo;color:#1B1A17;cursor:pointer}
	.nlsch-time.is-on{background:#9C7A3C;color:#FAF7F1;border-color:#9C7A3C}
	.nlsch-form{display:none;background:#fff;border:1px solid #E2DCD0;border-radius:16px;padding:18px;margin-top:16px;max-width:560px}
	.nlsch-form.is-open{display:block}
	.nlsch-sel{font:600 13px Heebo;color:#9C7A3C;margin:0 0 12px}
	.nlsch-form input,.nlsch-form textarea{width:100%;box-sizing:border-box;background:#FAF7F1;border:1px solid #E2DCD0;border-radius:10px;padding:11px;font:400 14px Heebo;color:#1B1A17;margin:0 0 10px}
	.nlsch-form textarea{min-height:60px;resize:vertical}
	.nlsch-go{display:inline-block;background:#C2563A;color:#FAF7F1;border:0;border-radius:12px;padding:13px 26px;font:700 15px Heebo;cursor:pointer;box-shadow:0 14px 30px -14px rgba(194,86,58,.55)}
	.nlsch-go[disabled]{opacity:.6;cursor:wait}
	.nlsch-err{display:none;color:#C2563A;font:600 13px Heebo;margin:8px 0 0}
	.nlsch-ok{display:none;background:#fff;border:1px solid #E2DCD0;border-radius:16px;padding:22px;margin-top:16px;max-width:560px}
	.nlsch-ok.is-open{display:block}
	.nlsch-ok h3{font-family:"Frank Ruhl Libre",serif;margin:0 0 6px;color:#517048}
	.nlsch-ok p{font:400 14px/1.6 Heebo;color:#51483A;margin:0 0 14px}
	.nlsch-ok .row{display:flex;gap:10px;flex-wrap:wrap}
	.nlsch-ok a.btn{display:inline-block;border-radius:12px;padding:11px 18px;font:700 13.5px Heebo;text-decoration:none}
	.nlsch-ok a.wa{background:#C2563A;color:#FAF7F1}
	.nlsch-ok a.lite{border:1.5px solid #9C7A3C;color:#9C7A3C;background:#fff}
	.nlsch-cancel{background:none;border:0;color:#A79E8D;font:600 12.5px Heebo;cursor:pointer;margin-top:12px;text-decoration:underline;padding:0}
	.nlsch-honest{font:400 12px/1.6 Heebo;color:#8E877A;margin:14px 0 0}
	.nlsch-empty{font:400 14px Heebo;color:#51483A;background:#fff;border:1px solid #E2DCD0;border-radius:14px;padding:16px}
	</style>
	<p class="nlsch-kicker"><?php echo esc_html( $s['kicker'] ); ?></p>
	<h2><?php echo esc_html( $s[ 'title_' . $kind ] ); ?></h2>
	<p class="nlsch-sub"><?php echo esc_html( $s['sub'] ); ?></p>
	<div id="nlsch-mount"
		data-card="<?php echo esc_attr( $card ); ?>"
		data-kind="<?php echo esc_attr( $kind ); ?>"
		data-lang="<?php echo esc_attr( $wlang ); ?>"
		data-rest="<?php echo esc_url( rest_url( 'nadlan/v1' ) ); ?>"
		data-i18n="<?php echo esc_attr( wp_json_encode( $s, JSON_UNESCAPED_UNICODE ) ); ?>"></div>
	<p class="nlsch-honest"><?php echo esc_html( $s['honest'] ); ?></p>
</section>
<script defer src="<?php echo esc_url( $js ); ?>"></script>
	<?php
	return $content . ob_get_clean();
}, 28 );

/* ---------- CMS metabox (owner assigns a paying customer per entity) ---------- */
add_action( 'add_meta_boxes', function () {
	foreach ( array( 'nadlan_project', 'nadlan_property', 'nadlan_professional' ) as $pt ) {
		add_meta_box( 'nadlan_sched_panel', 'תיאום פגישות (Scheduler)', 'nadlan_sched_metabox_render', $pt, 'normal', 'default' );
	}
} );

if ( ! function_exists( 'nadlan_sched_metabox_render' ) ) {
	function nadlan_sched_metabox_render( $post ) {
		wp_nonce_field( 'nadlan_sched_metabox', 'nadlan_sched_metabox_nonce' );
		$host = (int) get_post_meta( $post->ID, 'nadlan_sched_host', true );
		$off  = get_post_meta( $post->ID, 'nadlan_sched_off', true ) === '1';
		$av   = nadlan_sched_clean_avail( get_post_meta( $post->ID, 'nadlan_sched_avail', true ) );
		$week = isset( $av['week'] ) ? $av['week'] : array();
		$day_lbl = array( 'ראשון', 'שני', 'שלישי', 'רביעי', 'חמישי', 'שישי', 'שבת' );
		?>
		<div dir="rtl" style="max-width:680px">
			<p>
				<label style="font-weight:600"><input type="checkbox" name="nadlan_sched_off_field" value="1" <?php checked( $off ); ?>> כיבוי התיאום בעמוד הזה</label>
			</p>
			<p>
				<label for="nadlan_sched_host_field" style="font-weight:600;display:block;margin-bottom:4px">מי מקבל את הפגישות של הכרטיס הזה</label>
				<?php wp_dropdown_users( array( 'name' => 'nadlan_sched_host_field', 'selected' => $host, 'show_option_none' => 'ברירת מחדל: בעל האתר', 'option_none_value' => 0 ) ); ?>
				<span style="color:#666;font-size:12px;display:block;margin-top:3px">לקוחות בתשלום: בחרו כאן את המשתמש שלהם. הוא מנהל שעות פעילות ומספר וואטסאפ משלו בעמוד /my-appointments/.</span>
			</p>
			<p style="font-weight:600;margin-bottom:4px">שעות פעילות מיוחדות לכרטיס הזה (לא חובה)</p>
			<p style="color:#666;font-size:12px;margin-top:0">פורמט: 09:00-18:00. שדה ריק = היום סגור. אם הכל ריק - נופלים לשעות של המשתמש או של האתר.</p>
			<table style="border-collapse:collapse">
				<?php for ( $d = 0; $d <= 6; $d++ ) : ?>
				<tr>
					<td style="padding:2px 0 2px 10px;font-size:12px"><?php echo esc_html( $day_lbl[ $d ] ); ?></td>
					<td><input type="text" name="nadlan_sched_week_<?php echo (int) $d; ?>" value="<?php echo esc_attr( isset( $week[ $d ] ) ? $week[ $d ] : '' ); ?>" placeholder="<?php echo $d < 5 ? '09:00-19:00' : ( 5 === $d ? '09:00-13:00' : '' ); ?>" style="width:130px"></td>
				</tr>
				<?php endfor; ?>
			</table>
			<p>
				<label>אורך פגישה (דקות) <input type="number" name="nadlan_sched_slot" value="<?php echo esc_attr( isset( $av['slot_min'] ) ? $av['slot_min'] : '' ); ?>" placeholder="30" style="width:70px"></label>
				&nbsp; <label>מרווח בין פגישות <input type="number" name="nadlan_sched_buffer" value="<?php echo esc_attr( isset( $av['buffer_min'] ) ? $av['buffer_min'] : '' ); ?>" placeholder="15" style="width:70px"></label>
				&nbsp; <label>התראה מראש (שעות) <input type="number" name="nadlan_sched_lead" value="<?php echo esc_attr( isset( $av['lead_hours'] ) ? $av['lead_hours'] : '' ); ?>" placeholder="3" style="width:70px"></label>
			</p>
			<p>
				<label style="display:block;font-weight:600;margin-bottom:4px">תאריכים חסומים (מופרדים בפסיק, YYYY-MM-DD)</label>
				<input type="text" name="nadlan_sched_blackout" value="<?php echo esc_attr( isset( $av['blackout'] ) ? implode( ', ', $av['blackout'] ) : '' ); ?>" style="width:100%;max-width:560px" placeholder="2026-09-23, 2026-10-02">
			</p>
		</div>
		<?php
	}
}

add_action( 'save_post', function ( $post_id ) {
	if ( ! isset( $_POST['nadlan_sched_metabox_nonce'] )
		|| ! wp_verify_nonce( sanitize_text_field( wp_unslash( $_POST['nadlan_sched_metabox_nonce'] ) ), 'nadlan_sched_metabox' ) ) {
		return;
	}
	if ( defined( 'DOING_AUTOSAVE' ) && DOING_AUTOSAVE ) { return; }
	if ( ! current_user_can( 'edit_post', $post_id ) ) { return; }
	if ( ! in_array( get_post_type( $post_id ), array( 'nadlan_project', 'nadlan_property', 'nadlan_professional' ), true ) ) { return; }

	update_post_meta( $post_id, 'nadlan_sched_off', ! empty( $_POST['nadlan_sched_off_field'] ) ? '1' : '0' );
	$host = isset( $_POST['nadlan_sched_host_field'] ) ? absint( $_POST['nadlan_sched_host_field'] ) : 0;
	if ( $host > 0 ) { update_post_meta( $post_id, 'nadlan_sched_host', $host ); } else { delete_post_meta( $post_id, 'nadlan_sched_host' ); }

	$raw = array();
	$has = false;
	$week = array();
	$week_has = false;
	for ( $d = 0; $d <= 6; $d++ ) {
		$v = isset( $_POST[ 'nadlan_sched_week_' . $d ] ) ? trim( sanitize_text_field( wp_unslash( $_POST[ 'nadlan_sched_week_' . $d ] ) ) ) : '';
		$week[ $d ] = $v;
		if ( '' !== $v ) { $week_has = true; }
	}
	// An all-empty week means "inherit the host/site hours", NOT "all closed".
	if ( $week_has ) { $raw['week'] = $week; $has = true; }
	foreach ( array( 'slot_min' => 'nadlan_sched_slot', 'buffer_min' => 'nadlan_sched_buffer', 'lead_hours' => 'nadlan_sched_lead' ) as $k => $f ) {
		$v = isset( $_POST[ $f ] ) ? trim( sanitize_text_field( wp_unslash( $_POST[ $f ] ) ) ) : '';
		if ( '' !== $v ) { $raw[ $k ] = (int) $v; $has = true; }
	}
	$bl = isset( $_POST['nadlan_sched_blackout'] ) ? sanitize_text_field( wp_unslash( $_POST['nadlan_sched_blackout'] ) ) : '';
	if ( '' !== trim( $bl ) ) { $raw['blackout'] = array_map( 'trim', explode( ',', $bl ) ); $has = true; }
	if ( $has ) {
		update_post_meta( $post_id, 'nadlan_sched_avail', wp_json_encode( nadlan_sched_clean_avail( $raw ) ) );
	} else {
		delete_post_meta( $post_id, 'nadlan_sched_avail' );
	}
} );

/* ---------- /my-appointments/ (host + owner dashboard, noindex) ---------- */
add_action( 'init', function () {
	add_rewrite_rule( '^my-appointments/?$', 'index.php?nadlan_my_appts=1', 'top' );
	if ( get_option( 'nadlan_my_appts_rewrite_v1' ) !== '1' ) {
		flush_rewrite_rules( false );
		update_option( 'nadlan_my_appts_rewrite_v1', '1' );
	}
} );
add_filter( 'query_vars', function ( $v ) { $v[] = 'nadlan_my_appts'; return $v; } );

add_action( 'template_redirect', function () {
	if ( ! get_query_var( 'nadlan_my_appts' ) ) { return; }
	if ( ! nadlan_sched_on() ) { wp_safe_redirect( home_url( '/' ) ); exit; }
	if ( ! is_user_logged_in() ) { wp_safe_redirect( wp_login_url( home_url( '/my-appointments/' ) ) ); exit; }
	nocache_headers();
	header( 'X-Robots-Tag: noindex, nofollow' );
	$uid   = get_current_user_id();
	$items = nadlan_sched_list_for_user( $uid );
	$admin = current_user_can( 'manage_options' );
	$av    = $admin
		? array_merge( nadlan_sched_default_avail(), nadlan_sched_clean_avail( get_option( 'nadlan_sched_default_avail', '' ) ) )
		: array_merge( nadlan_sched_default_avail(), nadlan_sched_clean_avail( get_user_meta( $uid, 'nadlan_sched_avail', true ) ) );
	$wa = $admin ? '' : (string) get_user_meta( $uid, 'nadlan_sched_wa', true );
	$day_lbl = array( 'ראשון', 'שני', 'שלישי', 'רביעי', 'חמישי', 'שישי', 'שבת' );
	$status_lbl = array( 'confirmed' => 'מאושרת', 'done' => 'התקיימה', 'noshow' => 'לא הגיעו', 'cancelled' => 'בוטלה' );
	get_header();
	?>
<div class="nlsad" dir="rtl">
	<style>
	.nlsad{max-width:980px;margin:0 auto;padding:24px 16px 60px;font-family:Heebo,sans-serif;color:#1B1A17}
	.nlsad h1,.nlsad h2{font-family:"Frank Ruhl Libre",Georgia,serif}
	.nlsad h1{font-size:clamp(1.5rem,3.4vw,2.1rem);margin:12px 0 4px}
	.nlsad .lead{color:#51483A;font:400 14px/1.7 Heebo;margin:0 0 24px}
	.nlsad-card{background:#fff;border:1px solid #E2DCD0;border-radius:16px;padding:16px 18px;margin-bottom:12px;display:flex;gap:16px;flex-wrap:wrap;align-items:center;justify-content:space-between}
	.nlsad-card .when{font:700 15px "Frank Ruhl Libre",serif;min-width:130px}
	.nlsad-card .who{font:400 13.5px/1.5 Heebo;color:#51483A;flex:1;min-width:200px}
	.nlsad-card .who a{color:#9C7A3C}
	.nlsad-st{border-radius:999px;padding:5px 12px;font:600 12px Heebo}
	.nlsad-st.confirmed{background:#EFF3EA;color:#517048}.nlsad-st.done{background:#F3EEE3;color:#8E877A}
	.nlsad-st.noshow{background:#F7E8E3;color:#C2563A}.nlsad-st.cancelled{background:#F3EEE3;color:#A79E8D;text-decoration:line-through}
	.nlsad-acts button{border:1px solid #E2DCD0;background:#fff;border-radius:10px;padding:7px 12px;font:600 12px Heebo;color:#51483A;cursor:pointer;margin-inline-start:6px}
	.nlsad-empty{background:#F3EEE3;border:1px solid #E2DCD0;border-radius:16px;padding:22px;color:#51483A;font:400 14px Heebo}
	.nlsad-av{background:#F3EEE3;border:1px solid #E2DCD0;border-radius:22px;padding:22px;margin-top:34px}
	.nlsad-av h2{margin:0 0 8px;font-size:1.25rem}
	.nlsad-av p.hint{font:400 13px/1.6 Heebo;color:#51483A;margin:0 0 14px}
	.nlsad-av label{font:600 12.5px Heebo;color:#51483A}
	.nlsad-av input{background:#fff;border:1px solid #E2DCD0;border-radius:10px;padding:9px;font:400 13.5px Heebo;margin:3px 0 10px}
	.nlsad-av .grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(150px,1fr));gap:4px 14px}
	.nlsad-save{background:#C2563A;color:#FAF7F1;border:0;border-radius:12px;padding:12px 24px;font:700 14px Heebo;cursor:pointer}
	.nlsad-saved{display:none;color:#517048;font:600 13px Heebo;margin-inline-start:10px}
	</style>
	<h1>הפגישות שלי</h1>
	<p class="lead"><?php echo $admin ? 'כל הפגישות שנקבעו באתר (7 ימים אחורה והלאה). כל פגישה היא גם ליד במערכת הלידים.' : 'הפגישות שנקבעו אליכם דרך הכרטיסים שלכם באתר.'; ?></p>
	<?php if ( ! $items ) : ?>
		<div class="nlsad-empty">אין פגישות קרובות. כשמבקר יקבע מועד בעמוד פרויקט, נכס או בעל מקצוע - הוא יופיע כאן.</div>
	<?php else : foreach ( $items as $it ) : ?>
		<div class="nlsad-card" data-id="<?php echo (int) $it['id']; ?>">
			<span class="when"><?php echo esc_html( $it['start'] ); ?></span>
			<span class="who">
				<b><?php echo esc_html( $it['name'] ); ?></b>
				<?php if ( $it['phone'] ) : ?> · <a href="<?php echo esc_url( $it['wa'] ); ?>" target="_blank" rel="noopener"><?php echo esc_html( $it['phone'] ); ?></a><?php endif; ?>
				<?php if ( $it['card'] ) : ?><br><a href="<?php echo esc_url( $it['card_url'] ); ?>"><?php echo esc_html( $it['card'] ); ?></a><?php endif; ?>
				<?php if ( $it['note'] ) : ?><br><?php echo esc_html( $it['note'] ); ?><?php endif; ?>
			</span>
			<span class="nlsad-st <?php echo esc_attr( $it['status'] ); ?>"><?php echo esc_html( isset( $status_lbl[ $it['status'] ] ) ? $status_lbl[ $it['status'] ] : $it['status'] ); ?></span>
			<span class="nlsad-acts">
				<button data-s="done">התקיימה</button>
				<button data-s="noshow">לא הגיעו</button>
				<button data-s="cancelled">ביטול</button>
			</span>
		</div>
	<?php endforeach; endif; ?>

	<div class="nlsad-av">
		<h2><?php echo $admin ? 'שעות ברירת המחדל של האתר' : 'שעות הפעילות שלי'; ?></h2>
		<p class="hint">פורמט 09:00-19:00, שדה ריק = סגור. השינוי נכנס לתוקף מיד בכל העמודים <?php echo $admin ? 'שלא הוגדרו להם שעות מיוחדות.' : 'שמחוברים אליכם.'; ?></p>
		<form id="nlsad-form">
			<div class="grid">
				<?php for ( $d = 0; $d <= 6; $d++ ) : ?>
				<div><label><?php echo esc_html( $day_lbl[ $d ] ); ?></label><br>
				<input type="text" name="w<?php echo (int) $d; ?>" value="<?php echo esc_attr( isset( $av['week'][ $d ] ) ? $av['week'][ $d ] : '' ); ?>" placeholder="<?php echo 6 === $d ? 'סגור' : '09:00-19:00'; ?>" style="width:130px"></div>
				<?php endfor; ?>
			</div>
			<div class="grid" style="margin-top:8px">
				<div><label>אורך פגישה (דק)</label><br><input type="number" name="slot_min" value="<?php echo (int) $av['slot_min']; ?>" style="width:90px"></div>
				<div><label>מרווח (דק)</label><br><input type="number" name="buffer_min" value="<?php echo (int) $av['buffer_min']; ?>" style="width:90px"></div>
				<div><label>התראה מראש (שע)</label><br><input type="number" name="lead_hours" value="<?php echo (int) $av['lead_hours']; ?>" style="width:90px"></div>
				<?php if ( ! $admin ) : ?>
				<div><label>וואטסאפ (9725...)</label><br><input type="text" name="wa" value="<?php echo esc_attr( $wa ); ?>" style="width:150px" dir="ltr"></div>
				<?php endif; ?>
			</div>
			<p style="margin-top:14px"><button type="submit" class="nlsad-save">שמירת הזמינות</button><span class="nlsad-saved" id="nlsad-saved">נשמר</span></p>
		</form>
	</div>
	<script>
	(function(){
		var REST = <?php echo wp_json_encode( esc_url_raw( rest_url( 'nadlan/v1' ) ) ); ?>, NONCE = <?php echo wp_json_encode( wp_create_nonce( 'wp_rest' ) ); ?>;
		document.querySelectorAll('.nlsad-acts button').forEach(function(b){
			b.addEventListener('click', function(){
				var card = b.closest('.nlsad-card');
				fetch(REST + '/appt-status', { method:'POST', headers:{'Content-Type':'application/json','X-WP-Nonce':NONCE},
					body: JSON.stringify({ id: parseInt(card.dataset.id,10), status: b.dataset.s })
				}).then(function(r){ if(r.ok){ location.reload(); } });
			});
		});
		var f = document.getElementById('nlsad-form');
		f.addEventListener('submit', function(e){
			e.preventDefault();
			var fd = new FormData(f), week = {}, body = { week: week };
			for (var d = 0; d <= 6; d++) { week[d] = (fd.get('w'+d)||'').trim(); }
			['slot_min','buffer_min','lead_hours','wa'].forEach(function(k){ var v = fd.get(k); if (v !== null && v !== '') { body[k] = v; } });
			fetch(REST + '/my-availability', { method:'POST', headers:{'Content-Type':'application/json','X-WP-Nonce':NONCE}, body: JSON.stringify(body) })
				.then(function(r){ if(r.ok){ var s=document.getElementById('nlsad-saved'); s.style.display='inline'; setTimeout(function(){s.style.display='none';},2500); } });
		});
	})();
	</script>
</div>
	<?php
	get_footer();
	exit;
} );

/* ---------- daily reminder tick (log-first, sending behind the flag) ---------- */
add_action( 'init', function () {
	if ( ! wp_next_scheduled( 'nadlan_sched_tick' ) ) {
		wp_schedule_event( time() + HOUR_IN_SECONDS, 'daily', 'nadlan_sched_tick' );
	}
} );
add_action( 'nadlan_sched_tick', function () {
	if ( ! nadlan_sched_on() ) { return; }
	$tz = wp_timezone();
	$tomorrow = ( new DateTimeImmutable( 'now', $tz ) )->add( new DateInterval( 'P1D' ) )->format( 'Y-m-d' );
	$q = new WP_Query( array(
		'post_type' => 'nadlan_appt', 'post_status' => 'private', 'posts_per_page' => 100,
		'fields' => 'ids', 'no_found_rows' => true,
		'meta_query' => array(
			array( 'key' => 'appt_status', 'value' => 'confirmed' ),
			array( 'key' => 'appt_start', 'value' => array( $tomorrow . ' 00:00', $tomorrow . ' 23:59' ), 'compare' => 'BETWEEN' ),
		),
	) );
	foreach ( $q->posts as $aid ) {
		if ( get_post_meta( $aid, 'appt_reminded', true ) === '1' ) { continue; }
		update_post_meta( $aid, 'appt_reminded', '1' );
		$host = (int) get_post_meta( $aid, 'appt_host', true );
		$card = (int) get_post_meta( $aid, 'appt_card', true );
		$card_post = $card ? get_post( $card ) : null;
		nadlan_sched_queue_notice(
			nadlan_sched_host_email( $host ),
			'[נדלן] תזכורת: פגישה מחר - ' . get_post_meta( $aid, 'appt_start', true ),
			'פגישה מחר: ' . ( $card_post ? $card_post->post_title : '' ) . "\n" . get_post_meta( $aid, 'name', true ) . ' ' . get_post_meta( $aid, 'phone', true ) . "\nניהול: " . home_url( '/my-appointments/' )
		);
	}
} );

/* ---------- healthcheck ---------- */
add_filter( 'nadlan_config_healthcheck', function ( $out ) {
	$counts = wp_count_posts( 'nadlan_appt' );
	$out['scheduler'] = array(
		'on'           => nadlan_sched_on(),
		'appointments' => isset( $counts->private ) ? (int) $counts->private : 0,
		'notify'       => get_option( 'nadlan_scheduler_notify_enabled', '0' ) === '1',
	);
	return $out;
} );
