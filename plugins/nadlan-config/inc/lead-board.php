<?php
/**
 * nadlan-config - Lead board panel (v1.72.195)
 *
 * Owner law 2026-08-13: "I need to SEE these things - what people get, the
 * ranking, in an easy way, without logging in." [nadlan_lead_board] renders a
 * live leads panel for the password-protected board page: summary counters +
 * the recent leads with score, ack state and status. Privacy: phones masked,
 * emails omitted - full detail stays behind wp-admin links.
 */

if ( ! defined( 'ABSPATH' ) ) { exit; }

add_shortcode( 'nadlan_lead_board', function () {
	if ( ! post_password_required() && ! is_user_logged_in() && ! is_page() ) { return ''; }
	$leads = get_posts( array( 'post_type' => 'nadlan_lead', 'post_status' => 'any', 'numberposts' => 15 ) );
	$week  = 0; $total_real = 0;
	$all   = get_posts( array( 'post_type' => 'nadlan_lead', 'post_status' => 'any', 'numberposts' => 200, 'fields' => 'ids' ) );
	foreach ( $all as $lid ) {
		$t = get_the_title( $lid );
		if ( false !== mb_strpos( $t, 'בדיק' ) || false !== strpos( $t, 'E2E' ) ) { continue; }
		$total_real++;
		if ( strtotime( get_post_field( 'post_date', $lid ) ) > time() - WEEK_IN_SECONDS ) { $week++; }
	}
	ob_start(); ?>
<div class="nl-leadboard" dir="rtl">
<style>
.nl-leadboard{font-family:var(--font-sans,Heebo,sans-serif);margin:18px 0}
.nl-leadboard .sum{display:flex;gap:12px;margin-bottom:12px;flex-wrap:wrap}
.nl-leadboard .sum b{background:#FAF7F1;border-radius:8px;padding:10px 16px;font-size:14px}
.nl-leadboard table{width:100%;border-collapse:collapse;font-size:13px}
.nl-leadboard th,.nl-leadboard td{padding:7px 9px;border-bottom:1px solid rgba(27,26,23,.08);text-align:right}
.nl-leadboard th{background:#FAF7F1;font-weight:600}
.nl-leadboard .tier-hot{color:#a33}.nl-leadboard .tier-warm{color:#a70}.nl-leadboard .tier-cold{color:#579}
.nl-leadboard .ok{color:#2c7a4b}.nl-leadboard .no{color:#a33}
</style>
	<div class="sum">
		<b>לידים אמיתיים סה״כ: <?php echo (int) $total_real; ?></b>
		<b>בשבוע האחרון: <?php echo (int) $week; ?></b>
	</div>
	<table>
		<tr><th>תאריך</th><th>שם</th><th>טלפון</th><th>פרויקט</th><th>ציון AI</th><th>אישור לפונה</th><th>סטטוס</th></tr>
		<?php foreach ( $leads as $l ) :
			$m = function ( $k ) use ( $l ) { return (string) get_post_meta( $l->ID, $k, true ); };
			$phone = $m( 'phone' );
			$masked = $phone ? mb_substr( $phone, 0, 3 ) . '***' . mb_substr( $phone, -3 ) : '';
			$card_id = (int) $m( 'project_wp_id' );
			$tier = $m( 'lead_ai_tier' );
			$is_test = ( false !== mb_strpos( $l->post_title, 'בדיק' ) || false !== strpos( $l->post_title, 'E2E' ) );
		?>
		<tr>
			<td><?php echo esc_html( mb_substr( $l->post_date, 0, 16 ) ); ?></td>
			<td><?php echo esc_html( $m( 'name' ) ?: '-' ); ?><?php echo $is_test ? ' <small>(בדיקה)</small>' : ''; ?></td>
			<td dir="ltr"><?php echo esc_html( $masked ); ?></td>
			<td><?php if ( $card_id ) : ?><a href="<?php echo esc_url( get_permalink( $card_id ) ); ?>"><?php echo esc_html( get_the_title( $card_id ) ); ?></a><?php else : ?><?php echo esc_html( $m( 'project_title' ) ?: '-' ); ?><?php endif; ?></td>
			<td class="tier-<?php echo esc_attr( $tier ?: 'cold' ); ?>"><?php echo esc_html( $m( 'lead_score' ) !== '' ? $m( 'lead_score' ) . ' · ' . $tier : '-' ); ?></td>
			<td class="<?php echo 'sent' === $m( 'lead_ack_status' ) ? 'ok' : 'no'; ?>"><?php echo 'sent' === $m( 'lead_ack_status' ) ? 'נשלח' : 'לא'; ?></td>
			<td><?php echo esc_html( $m( 'lead_status' ) ?: 'new' ); ?></td>
		</tr>
		<?php endforeach; ?>
	</table>
	<p style="font-size:12px;color:#777">הנתונים חיים ומתעדכנים בכל רענון. פרטים מלאים וניהול: מתוך ההתראות במייל או בפאנל הניהול.</p>
</div>
	<?php
	return ob_get_clean();
} );
