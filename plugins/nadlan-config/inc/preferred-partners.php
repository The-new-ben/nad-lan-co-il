<?php
/**
 * nadlan-config — Preferred Partners (v1.40.0 / shark #7)
 *
 * Safe auto-routing: the owner defines a small set of APPROVED partner emails
 * (the actual people you have a deal with), organised by profession + optional
 * city. The Lead Ledger consults this list when a routed lead is created with
 * a topic that doesn't match a partner_id (e.g. the AI concierge or sticky CTA
 * routes "מצא לי יועץ משכנתאות באזור גוש דן") and picks the right partner.
 *
 * This is the FAT MONEY door: ₪3k–8k per closed mortgage / RE deal, captured
 * automatically once you've added even one real partner to the list. Without
 * this, every fat lead requires you to manually pick a partner.
 *
 * Spam-safe: only emails on this list get routed. The 2,700 imported cold
 * contractors are NEVER contacted from here.
 *
 * Stored as one option: nadlan_preferred_partners (JSON array). Admin page
 * under "💰 Lead Inbox" → "שותפים מועדפים".
 */
if ( ! defined( 'ABSPATH' ) ) { exit; }

if ( ! function_exists( 'nadlan_pp_list' ) ) {
	function nadlan_pp_list() {
		$raw = get_option( 'nadlan_preferred_partners', '' );
		$data = is_string( $raw ) && $raw !== '' ? json_decode( $raw, true ) : array();
		return is_array( $data ) ? $data : array();
	}
}

if ( ! function_exists( 'nadlan_pp_pick' ) ) {
	/* Pick the best matching partner for (profession, city). Returns array(name,email,phone,pct) or null. */
	function nadlan_pp_pick( $profession, $city = '' ) {
		$profession = sanitize_key( $profession );
		$city = trim( (string) $city );
		$candidates = array();
		foreach ( nadlan_pp_list() as $p ) {
			$pp = sanitize_key( $p['profession'] ?? '' );
			if ( $profession && $pp !== $profession ) { continue; }
			$pc = trim( (string) ( $p['city'] ?? '' ) );
			$score = 0;
			if ( $city && $pc && mb_stripos( $city, $pc ) !== false ) { $score += 10; }
			if ( ! $pc ) { $score += 1; } // city-agnostic candidate
			$candidates[] = array( 'score' => $score, 'p' => $p );
		}
		if ( ! $candidates ) { return null; }
		usort( $candidates, function ( $a, $b ) { return $b['score'] - $a['score']; } );
		return $candidates[0]['p'];
	}
}

/* Admin page */
add_action( 'admin_menu', function () {
	add_submenu_page( 'nadlan-inbox', 'שותפים מועדפים', 'שותפים מועדפים', 'manage_options', 'nadlan-partners', 'nadlan_pp_admin_render' );
} );

if ( ! function_exists( 'nadlan_pp_admin_render' ) ) {
	function nadlan_pp_admin_render() {
		if ( ! current_user_can( 'manage_options' ) ) { return; }
		if ( ! empty( $_POST['nadlan_pp_save'] ) && check_admin_referer( 'nadlan_pp_save' ) ) {
			$rows = isset( $_POST['p'] ) ? (array) $_POST['p'] : array();
			$clean = array();
			foreach ( $rows as $r ) {
				$name = sanitize_text_field( wp_unslash( $r['name'] ?? '' ) );
				$email = sanitize_email( wp_unslash( $r['email'] ?? '' ) );
				if ( ! $name || ! $email ) { continue; }
				$clean[] = array(
					'name'  => $name,
					'email' => $email,
					'phone' => preg_replace( '/[^0-9+]/', '', sanitize_text_field( wp_unslash( $r['phone'] ?? '' ) ) ),
					'profession' => sanitize_key( $r['profession'] ?? '' ),
					'city'  => sanitize_text_field( wp_unslash( $r['city'] ?? '' ) ),
					'pct'   => max( 0.0, min( 100.0, (float) ( $r['pct'] ?? 25 ) ) ),
				);
			}
			update_option( 'nadlan_preferred_partners', wp_json_encode( $clean, JSON_UNESCAPED_UNICODE ) );
			echo '<div class="notice notice-success"><p>נשמר. ' . count( $clean ) . ' שותפים.</p></div>';
		}
		$list = nadlan_pp_list();
		while ( count( $list ) < 3 ) { $list[] = array(); }
		?>
<div class="wrap" style="direction:rtl;font-family:Heebo,sans-serif">
<h1>שותפים מועדפים</h1>
<p>הוסיפו רק שותפים שיש לכם איתם הסכם פעיל. רק שותפים שמופיעים ברשימה הזו מקבלים לידים אוטומטית. 2,700 הקבלנים המיובאים <strong>לא יקבלו כלום</strong> מכאן.</p>
<form method="post">
	<?php wp_nonce_field( 'nadlan_pp_save' ); ?>
	<table class="widefat striped"><thead><tr><th>שם</th><th>אימייל</th><th>טלפון</th><th>מקצוע</th><th>עיר (אופציונלי)</th><th>עמלה %</th></tr></thead><tbody>
	<?php
	$profs = array(
		'kablan' => 'קבלן', 'shamai' => 'שמאי', 'bedek_bait' => 'בדק בית',
		'mashkanta' => 'יועץ משכנתאות', 'architect' => 'אדריכל',
		'lawyer' => 'עו״ד מקרקעין', 'mefakeach' => 'מפקח בנייה', 'metavech' => 'מתווך',
	);
	foreach ( $list as $i => $p ) :
	?>
		<tr>
			<td><input type="text" name="p[<?php echo $i; ?>][name]"  value="<?php echo esc_attr( $p['name'] ?? '' ); ?>" style="width:100%"></td>
			<td><input type="email" name="p[<?php echo $i; ?>][email]" value="<?php echo esc_attr( $p['email'] ?? '' ); ?>" style="width:100%"></td>
			<td><input type="text" name="p[<?php echo $i; ?>][phone]" value="<?php echo esc_attr( $p['phone'] ?? '' ); ?>" style="width:100%"></td>
			<td>
				<select name="p[<?php echo $i; ?>][profession]">
					<option value="">—</option>
					<?php foreach ( $profs as $k => $lbl ) : ?>
					<option value="<?php echo esc_attr( $k ); ?>" <?php selected( ( $p['profession'] ?? '' ), $k ); ?>><?php echo esc_html( $lbl ); ?></option>
					<?php endforeach; ?>
				</select>
			</td>
			<td><input type="text" name="p[<?php echo $i; ?>][city]" value="<?php echo esc_attr( $p['city'] ?? '' ); ?>" style="width:100%" placeholder="הכל"></td>
			<td><input type="number" name="p[<?php echo $i; ?>][pct]" value="<?php echo esc_attr( $p['pct'] ?? 25 ); ?>" step="0.1" min="0" max="100" style="width:80px">%</td>
		</tr>
	<?php endforeach; ?>
	<tr><td colspan="6" style="text-align:center"><button type="button" class="button" onclick="var t=this.closest('table'),tr=t.querySelector('tbody tr').cloneNode(true),i=t.querySelectorAll('tbody tr').length;tr.querySelectorAll('input,select').forEach(function(el){el.value='';el.name=el.name.replace(/p\[\d+\]/, 'p['+i+']');});t.querySelector('tbody').insertBefore(tr,this.parentNode.parentNode);">+ שורה נוספת</button></td></tr>
	</tbody></table>
	<p class="submit"><button type="submit" name="nadlan_pp_save" class="button-primary">שמור</button></p>
</form>
</div>
		<?php
	}
}

/* Hook: when a referral is created without partner_id but with a topic carrying
 * a profession hint, try auto-routing to a preferred partner. The Lead Ledger
 * still defaults to notify_partner=0 so this is opt-in per call. */
add_filter( 'nadlan_ll_auto_route', function ( $partner_id_or_zero, $params ) {
	if ( $partner_id_or_zero > 0 ) { return $partner_id_or_zero; }
	$prof = '';
	foreach ( array( 'kablan', 'shamai', 'bedek_bait', 'mashkanta', 'architect', 'lawyer', 'mefakeach', 'metavech' ) as $k ) {
		$lbl = array( 'kablan' => 'קבלן', 'shamai' => 'שמאי', 'mashkanta' => 'משכנתא', 'architect' => 'אדריכל', 'lawyer' => 'עורך דין', 'mefakeach' => 'מפקח', 'metavech' => 'מתווך', 'bedek_bait' => 'בדק בית' )[ $k ];
		if ( mb_stripos( (string) ( $params['topic'] ?? '' ), $lbl ) !== false ) { $prof = $k; break; }
	}
	$pick = nadlan_pp_pick( $prof, (string) ( $params['city'] ?? '' ) );
	if ( ! $pick ) { return 0; }
	// store the matched partner directly into the lead record metadata via filter chain.
	$GLOBALS['nadlan_ll_pp_match'] = $pick;
	return 0; // no nadlan_professional ID; flag for caller to use $pp_match instead.
}, 10, 2 );
