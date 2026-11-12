<?php
/**
 * nadlan-config: the professionals' forum, wp-admin screen "פורום" (loaded by inc/pro-forum.php in wp-admin only).
 * Under "NadLan Ops" when that menu exists, else a top-level item. Lists items waiting for review, reported items, hidden
 * items and card requests, with approve / hide / restore / block buttons (POST + nonce). No long dashes in this file.
 */
if ( ! defined( 'ABSPATH' ) ) { exit; }

function nlf_admin_pending_count() {
	if ( ! nlf_db_ready() ) { return 0; }
	global $wpdb;
	return (int) $wpdb->get_var( 'SELECT COUNT(*) FROM ' . nlf_t( 'topics' ) . " WHERE status IN ('pending','hidden')" )
		+ (int) $wpdb->get_var( 'SELECT COUNT(*) FROM ' . nlf_t( 'replies' ) . " WHERE status IN ('pending','hidden')" )
		+ (int) $wpdb->get_var( 'SELECT COUNT(*) FROM ' . nlf_t( 'requests' ) . " WHERE status = 'pending'" );
}

add_action( 'admin_menu', function () {
	$n     = nlf_admin_pending_count();
	$label = 'פורום' . ( $n > 0 ? ' <span class="awaiting-mod">' . (int) $n . '</span>' : '' );
	if ( function_exists( 'nadlan_ops_render' ) ) {
		add_submenu_page( 'nadlan-ops', 'פורום', $label, 'manage_options', 'nadlan-forum', 'nlf_admin_screen' );
	} else {
		add_menu_page( 'פורום', $label, 'manage_options', 'nadlan-forum', 'nlf_admin_screen', 'dashicons-format-chat', 27 );
	}
}, 20 );

/** the actions of the screen, before any output */
add_action( 'admin_init', function () {
	if ( empty( $_POST['nlf_do'] ) || ! current_user_can( 'manage_options' ) ) { return; }
	check_admin_referer( 'nlf_mod' );
	$do   = sanitize_key( wp_unslash( $_POST['nlf_do'] ) );
	$type = sanitize_key( wp_unslash( $_POST['nlf_type'] ?? '' ) );
	$id   = (int) ( $_POST['nlf_id'] ?? 0 );
	$msg  = '';
	if ( in_array( $type, array( 'topic', 'reply' ), true ) && $id > 0 ) {
		if ( 'approve' === $do || 'restore' === $do ) { nlf_moderate( $type, $id, 'live' ); $msg = 'approve' === $do ? 'אושר.' : 'הוחזר.'; }
		if ( 'hide' === $do ) { nlf_moderate( $type, $id, 'hidden' ); $msg = 'הוסתר.'; }
		if ( 'remove' === $do ) { nlf_moderate( $type, $id, 'removed' ); $msg = 'נדחה.'; }
		if ( in_array( $do, array( 'block', 'silence', 'unblock' ), true ) ) {
			$row = 'topic' === $type ? nlf_topic( $id ) : nlf_reply( $id );
			if ( $row ) { nlf_member_set_status( (int) $row['member_id'], 'unblock' === $do ? 'ok' : ( 'block' === $do ? 'blocked' : 'silenced' ) ); $msg = 'מצב המשתתף עודכן.'; }
		}
		if ( 'clearflags' === $do ) {
			global $wpdb;
			$wpdb->delete( nlf_t( 'flags' ), array( 'target_type' => $type, 'target_id' => $id ) );
			$msg = 'הדיווחים נמחקו.';
		}
	}
	if ( 'request' === $type && $id > 0 && in_array( $do, array( 'done', 'reopen' ), true ) ) {
		global $wpdb;
		$wpdb->update( nlf_t( 'requests' ), array( 'status' => 'done' === $do ? 'done' : 'pending' ), array( 'id' => $id ) );
		$msg = 'הבקשה עודכנה.';
	}
	set_transient( 'nlf_admin_msg_' . get_current_user_id(), $msg, 60 );
} );

function nlf_admin_btn( $do, $type, $id, $label, $primary = false ) {
	return '<form method="post" style="display:inline-block;margin:0 0 4px 4px">' . wp_nonce_field( 'nlf_mod', '_wpnonce', true, false )
		. '<input type="hidden" name="nlf_do" value="' . esc_attr( $do ) . '"><input type="hidden" name="nlf_type" value="' . esc_attr( $type ) . '">'
		. '<input type="hidden" name="nlf_id" value="' . (int) $id . '"><button class="button' . ( $primary ? ' button-primary' : '' ) . '">' . esc_html( $label ) . '</button></form>';
}

function nlf_admin_screen() {
	if ( ! current_user_can( 'manage_options' ) ) { return; }
	nlf_install();
	global $wpdb;
	$tab  = isset( $_GET['tab'] ) ? sanitize_key( wp_unslash( $_GET['tab'] ) ) : 'pending'; // phpcs:ignore -- a view switch
	$tabs = array( 'pending' => 'ממתינות לבדיקה', 'reported' => 'דווחו', 'hidden' => 'מוסתרות', 'requests' => 'בקשות על כרטיסים' );
	$tab  = isset( $tabs[ $tab ] ) ? $tab : 'pending';
	$msg  = get_transient( 'nlf_admin_msg_' . get_current_user_id() );
	if ( $msg ) { delete_transient( 'nlf_admin_msg_' . get_current_user_id() ); }
	echo '<div class="wrap" dir="rtl"><h1>פורום</h1>';
	if ( $msg ) { echo '<div class="notice notice-success"><p>' . esc_html( $msg ) . '</p></div>'; }
	echo '<p>הפורום ' . ( nlf_public() ? '<b>פתוח לכולם</b>' : '<b>מוסתר</b>. רואים אותו רק מנהלים ומי שפתח דף עם <code>?forum=on</code>' ) . '. כתובת: <a href="' . esc_url( add_query_arg( 'forum', 'on', home_url( '/forum/' ) ) ) . '" target="_blank">' . esc_html( home_url( '/forum/' ) ) . '</a>';
	$rst = nlf_rules_state();
	if ( ! empty( $rst['clash'] ) ) {
		echo ' · <b>הכתובת /forum/ שייכת לעמוד קיים באתר, ולכן הפורום לא נרשם עליה.</b>';
	} elseif ( function_exists( 'nadlan_forum_flush_needed' ) && nadlan_forum_flush_needed() ) {
		echo ' · <b>הכתובות עדיין לא נרשמו.</b>';
	}
	echo '</p><nav class="nav-tab-wrapper">';
	foreach ( $tabs as $k => $l ) { echo '<a class="nav-tab' . ( $k === $tab ? ' nav-tab-active' : '' ) . '" href="' . esc_url( admin_url( 'admin.php?page=nadlan-forum&tab=' . $k ) ) . '">' . esc_html( $l ) . '</a>'; }
	echo '</nav>';

	if ( 'requests' === $tab ) {
		$rows = $wpdb->get_results( 'SELECT * FROM ' . nlf_t( 'requests' ) . " ORDER BY (status = 'pending') DESC, id DESC LIMIT 100", ARRAY_A );
		echo '<table class="widefat striped"><thead><tr><th>סוג</th><th>כרטיס</th><th>מאת</th><th>הבקשה</th><th>מתי</th><th>מצב</th><th></th></tr></thead><tbody>';
		if ( ! $rows ) { echo '<tr><td colspan="7">אין בקשות.</td></tr>'; }
		foreach ( (array) $rows as $r ) {
			echo '<tr><td>' . ( 'removal' === $r['kind'] ? 'הסרה' : 'בעלות' ) . '</td><td><a href="' . esc_url( admin_url( 'post.php?post=' . (int) $r['pro_id'] . '&action=edit' ) ) . '">' . esc_html( get_the_title( (int) $r['pro_id'] ) ) . '</a></td>'
				. '<td>' . esc_html( $r['contact'] ) . ( '' !== $r['phone'] ? '<br>' . esc_html( $r['phone'] ) : '' ) . '</td><td>' . nlf_body_html( $r['body'] ) . '</td>' // phpcs:ignore -- escaped
				. '<td>' . esc_html( wp_date( 'j.n.Y H:i', nlf_ts( $r['created_at'] ) ) ) . '</td><td>' . ( 'pending' === $r['status'] ? 'ממתינה' : 'טופלה' ) . '</td><td>'
				. ( 'pending' === $r['status'] ? nlf_admin_btn( 'done', 'request', $r['id'], 'טופלה', true ) : nlf_admin_btn( 'reopen', 'request', $r['id'], 'פתיחה מחדש' ) ) . '</td></tr>'; // phpcs:ignore
		}
		echo '</tbody></table></div>';
		return;
	}

	$items = array();
	foreach ( array( 'topic' => nlf_t( 'topics' ), 'reply' => nlf_t( 'replies' ) ) as $type => $tb ) {
		if ( 'reported' === $tab ) {
			$sql = "SELECT x.*, COUNT(DISTINCT f.member_id) AS flags, GROUP_CONCAT(DISTINCT f.reason) AS reasons FROM $tb x JOIN " . nlf_t( 'flags' ) . " f ON f.target_type = '$type' AND f.target_id = x.id
				WHERE x.status IN ('live','hidden') GROUP BY x.id ORDER BY flags DESC, x.id DESC LIMIT 100";
		} else {
			$st  = 'pending' === $tab ? 'pending' : 'hidden';
			$sql = "SELECT x.*, 0 AS flags, '' AS reasons FROM $tb x WHERE x.status = '$st' ORDER BY x.id DESC LIMIT 100";
		}
		foreach ( (array) $wpdb->get_results( $sql, ARRAY_A ) as $r ) { $r['_type'] = $type; $items[] = $r; } // phpcs:ignore -- fixed strings only
	}
	$mem = array();
	foreach ( $items as $r ) { $mem[] = (int) $r['member_id']; }
	$mem     = nlf_members( $mem );
	$reasons = nlf_report_reasons();
	echo '<table class="widefat striped"><thead><tr><th>סוג</th><th>תוכן</th><th>מאת</th><th>מתי</th><th>דיווחים</th><th>פעולות</th></tr></thead><tbody>';
	if ( ! $items ) { echo '<tr><td colspan="6">אין כאן כלום כרגע.</td></tr>'; }
	foreach ( $items as $r ) {
		$m    = $mem[ (int) $r['member_id'] ] ?? null;
		$tid  = 'topic' === $r['_type'] ? (int) $r['id'] : (int) $r['topic_id'];
		$text = 'topic' === $r['_type'] ? '<b>' . esc_html( $r['title'] ) . '</b><br>' . nlf_body_html( nlf_excerpt( $r['body'], 400 ) ) : nlf_body_html( nlf_excerpt( $r['body'], 400 ) );
		$why  = array();
		foreach ( array_filter( explode( ',', (string) $r['reasons'] ) ) as $k ) { $why[] = $reasons[ $k ] ?? $k; }
		$btns = '';
		if ( 'pending' === $r['status'] ) { $btns .= nlf_admin_btn( 'approve', $r['_type'], $r['id'], 'אישור', true ) . nlf_admin_btn( 'remove', $r['_type'], $r['id'], 'דחייה' ); }
		if ( 'live' === $r['status'] ) { $btns .= nlf_admin_btn( 'hide', $r['_type'], $r['id'], 'הסתרה' ); }
		if ( 'hidden' === $r['status'] ) { $btns .= nlf_admin_btn( 'restore', $r['_type'], $r['id'], 'החזרה', true ) . nlf_admin_btn( 'remove', $r['_type'], $r['id'], 'מחיקה מהפורום' ); }
		if ( (int) $r['flags'] > 0 ) { $btns .= nlf_admin_btn( 'clearflags', $r['_type'], $r['id'], 'ניקוי הדיווחים' ); }
		if ( $m && 'ok' === $m['status'] ) { $btns .= nlf_admin_btn( 'silence', $r['_type'], $r['id'], 'השתקת המשתתף' ) . nlf_admin_btn( 'block', $r['_type'], $r['id'], 'חסימת המשתתף' ); }
		if ( $m && 'ok' !== $m['status'] ) { $btns .= nlf_admin_btn( 'unblock', $r['_type'], $r['id'], 'ביטול חסימה' ); }
		echo '<tr><td>' . ( 'topic' === $r['_type'] ? 'דיון' : 'תשובה' ) . '<br><a href="' . esc_url( add_query_arg( 'forum', 'on', home_url( '/forum/' . $tid . '/' ) ) ) . '" target="_blank">לדיון</a></td>'
			. '<td style="max-width:520px">' . $text . '</td>' // phpcs:ignore -- escaped
			. '<td>' . ( $m ? esc_html( $m['display_name'] ) . '<br><small>' . esc_html( $m['contact'] ) . '</small><br>'
				. ( '' !== (string) ( $m['trade_other'] ?? '' ) ? '<small>' . esc_html( 'תחום שכתב בעצמו (לבדיקה): ' . $m['trade_other'] ) . '</small><br>' : '' )
				. ( nlf_trade( (string) ( $m['trade'] ?? '' ) ) ? '<small>' . esc_html( 'תחום: ' . nlf_trade( (string) $m['trade'] )['label'] ) . '</small><br>' : '' )
				. '<small>' . esc_html( (string) (int) $m['approved_posts'] . ' הודעות שאושרו · ' . $m['status'] ) . '</small>' : '' ) . '</td>'
			. '<td>' . esc_html( wp_date( 'j.n.Y H:i', nlf_ts( $r['created_at'] ) ) ) . '</td>'
			. '<td>' . ( (int) $r['flags'] > 0 ? (int) $r['flags'] . '<br><small>' . esc_html( implode( ', ', $why ) ) . '</small>' : '' ) . '</td><td>' . $btns . '</td></tr>'; // phpcs:ignore
	}
	echo '</tbody></table></div>';
}
