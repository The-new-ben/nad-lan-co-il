<?php
/**
 * Broker placements: a broker's ad card on chosen pages, as a managed mechanism (owner order 24.9.2026:
 * "Meital's card is a good idea, do it, but with a mechanism. Not just a card: something I can control after").
 *
 * A placement (NadLan Ops > "שיבוץ מתווכים") says WHO appears (a professional's card), WHERE (page paths, a
 * trailing * matches a whole section), WHEN (start and end dates) and HOW (after which section, the headline).
 * The card is always labelled as the broker's advertisement with the name, "מתווך"/"מתווכת" and the licence
 * number (ethics regulation 19), because the site itself is a publisher and never the broker (Brokers Law 2(c)).
 * Views and clicks go to the private insights table (inc/insights.php): place_view, place_click.
 *
 * Nothing shows until a placement is published AND active. An admin can preview a draft on its page with
 * ?nlpl_preview=<placement id>.
 */
if ( ! defined( 'ABSPATH' ) ) { exit; }

add_action( 'init', function () {
	register_post_type( 'nadlan_placement', array(
		'labels'          => array( 'name' => 'שיבוץ מתווכים', 'singular_name' => 'שיבוץ', 'add_new_item' => 'שיבוץ חדש', 'edit_item' => 'עריכת שיבוץ' ),
		'public'          => false,
		'show_ui'         => true,
		'show_in_menu'    => 'nadlan-ops',
		'show_in_rest'    => false,
		'supports'        => array( 'title' ),
		'capability_type' => 'page',
		'map_meta_cap'    => true,
	) );
}, 20 );

if ( ! function_exists( 'nadlan_pl_fields' ) ) {
	function nadlan_pl_fields() {
		return array(
			'pl_pro'      => 'מזהה הכרטיס של המתווך',
			'pl_paths'    => 'עמודים (נתיב בכל שורה, למשל /property-value/ או /north-tel-aviv/*)',
			'pl_after_h2' => 'אחרי כמה פרקים (מספר; 0 = בסוף העמוד)',
			'pl_headline' => 'כותרת הכרטיס (לא חובה)',
			'pl_ask'      => 'הטקסט המוכן בוואטסאפ (לא חובה)',
			'pl_start'    => 'מתחיל בתאריך (YYYY-MM-DD, לא חובה)',
			'pl_end'      => 'נגמר בתאריך (YYYY-MM-DD, לא חובה)',
			'pl_active'   => 'פעיל (1 או 0)',
		);
	}
}

add_action( 'add_meta_boxes', function () {
	add_meta_box( 'nadlan_pl_box', 'הגדרות השיבוץ', function ( $post ) {
		wp_nonce_field( 'nadlan_pl_save', 'nadlan_pl_nonce' );
		echo '<table class="form-table" dir="rtl">';
		foreach ( nadlan_pl_fields() as $k => $label ) {
			$v = (string) get_post_meta( $post->ID, $k, true );
			echo '<tr><th><label for="' . esc_attr( $k ) . '">' . esc_html( $label ) . '</label></th><td>';
			if ( 'pl_paths' === $k ) {
				echo '<textarea id="pl_paths" name="pl_paths" rows="5" style="width:100%;direction:ltr">' . esc_textarea( $v ) . '</textarea>';
			} else {
				echo '<input type="text" id="' . esc_attr( $k ) . '" name="' . esc_attr( $k ) . '" value="' . esc_attr( $v ) . '" style="width:100%">';
			}
			echo '</td></tr>';
		}
		echo '</table><p>תצוגה מקדימה לפני פרסום: לפתוח את העמוד עם <code>?nlpl_preview=' . (int) $post->ID . '</code> (רק למנהל).</p>';
	}, 'nadlan_placement', 'normal', 'high' );
} );

add_action( 'save_post_nadlan_placement', function ( $post_id ) {
	if ( ! isset( $_POST['nadlan_pl_nonce'] ) || ! wp_verify_nonce( (string) $_POST['nadlan_pl_nonce'], 'nadlan_pl_save' ) ) { return; }
	if ( ! current_user_can( 'edit_post', $post_id ) || wp_is_post_revision( $post_id ) ) { return; }
	foreach ( array_keys( nadlan_pl_fields() ) as $k ) {
		if ( ! isset( $_POST[ $k ] ) ) { continue; }
		$v = wp_unslash( (string) $_POST[ $k ] );
		$v = 'pl_paths' === $k ? sanitize_textarea_field( $v ) : sanitize_text_field( $v );
		update_post_meta( $post_id, $k, $v );
	}
} );

if ( ! function_exists( 'nadlan_pl_path_matches' ) ) {
	function nadlan_pl_path_matches( $paths, $here ) {
		$here = '/' . trim( (string) $here, '/' ) . '/';
		foreach ( preg_split( '/\R/', (string) $paths ) as $p ) {
			$p = trim( $p );
			if ( '' === $p ) { continue; }
			$p = rawurldecode( $p );
			if ( '*' === substr( $p, -1 ) ) {
				$pre = '/' . trim( substr( $p, 0, -1 ), '/' );
				if ( 0 === strpos( rtrim( $here, '/' ), $pre ) ) { return true; }
			} elseif ( '/' . trim( $p, '/' ) . '/' === $here ) {
				return true;
			}
		}
		return false;
	}
}

if ( ! function_exists( 'nadlan_pl_for_request' ) ) {
	/** The placement for this page: an admin preview first, else the first active one whose paths match and whose dates cover today. */
	function nadlan_pl_for_request() {
		static $memo = null;
		if ( null !== $memo ) { return $memo; }
		$memo = 0;
		if ( is_admin() || ! is_singular() ) { return $memo; }
		$here = (string) wp_parse_url( (string) ( $_SERVER['REQUEST_URI'] ?? '' ), PHP_URL_PATH );
		$here = rawurldecode( $here );
		if ( isset( $_GET['nlpl_preview'] ) && current_user_can( 'edit_pages' ) ) {
			$pid = (int) $_GET['nlpl_preview'];
			if ( 'nadlan_placement' === get_post_type( $pid ) ) { $memo = $pid; return $memo; }
		}
		$ids = get_posts( array( 'post_type' => 'nadlan_placement', 'post_status' => 'publish', 'numberposts' => 50, 'fields' => 'ids',
			'meta_query' => array( array( 'key' => 'pl_active', 'value' => '1' ) ) ) );
		$today = current_time( 'Y-m-d' );
		foreach ( $ids as $pid ) {
			$s = (string) get_post_meta( $pid, 'pl_start', true );
			$e = (string) get_post_meta( $pid, 'pl_end', true );
			if ( ( '' !== $s && $today < $s ) || ( '' !== $e && $today > $e ) ) { continue; }
			if ( nadlan_pl_path_matches( get_post_meta( $pid, 'pl_paths', true ), $here ) ) { $memo = (int) $pid; break; }
		}
		return $memo;
	}
}

if ( ! function_exists( 'nadlan_pl_card' ) ) {
	function nadlan_pl_card( $pl ) {
		$pro = (int) get_post_meta( $pl, 'pl_pro', true );
		if ( $pro <= 0 || 'nadlan_professional' !== get_post_type( $pro ) || 'publish' !== get_post_status( $pro ) ) { return ''; }
		$name   = function_exists( 'nadlan_prof_person_name' ) ? (string) nadlan_prof_person_name( $pro ) : get_the_title( $pro );
		$label  = function_exists( 'nadlan_dir_prof_label' ) ? nadlan_dir_prof_label( (string) get_post_meta( $pro, 'profession', true ), $pro ) : '';
		$lic    = trim( (string) get_post_meta( $pro, 'license_number', true ) );
		$brand  = trim( (string) get_post_meta( $pro, 'company_name', true ) );
		$areas  = array_slice( array_filter( array_map( 'trim', explode( ',', (string) get_post_meta( $pro, 'areas_served', true ) ) ) ), 0, 5 );
		$phone  = (string) get_post_meta( $pro, 'phone', true );
		$wa     = function_exists( 'nadlan_prof_wa_digits' ) ? (string) nadlan_prof_wa_digits( $phone ) : preg_replace( '/\D/', '', $phone );
		$site   = (int) get_post_meta( $pro, 'nl_site_he', true );
		$href   = $site > 0 && 'publish' === get_post_status( $site ) ? get_permalink( $site ) : get_permalink( $pro );
		$head   = trim( (string) get_post_meta( $pl, 'pl_headline', true ) );
		$ask    = trim( (string) get_post_meta( $pl, 'pl_ask', true ) );
		$ask    = '' !== $ask ? $ask : 'שלום ' . $name . ', הגעתי מאתר נדלן ואשמח להתייעץ על הדירה שלי';
		$photo  = has_post_thumbnail( $pro ) ? get_the_post_thumbnail( $pro, 'thumbnail', array( 'class' => 'nlpl-ph', 'alt' => $name, 'loading' => 'lazy' ) ) : '';
		$slot   = 'pl-' . (int) $pl;
		$here   = (int) get_queried_object_id();
		ob_start(); ?>
<aside class="nlpl" dir="rtl" data-pl="<?php echo (int) $pl; ?>" data-pro="<?php echo (int) $pro; ?>" data-post="<?php echo $here; ?>" aria-label="<?php echo esc_attr( 'פרסומת: ' . $name ); ?>">
	<p class="nlpl-tag">פרסומת<?php echo '' !== $label ? ' · ' . esc_html( $label ) : ''; ?><?php echo '' !== $lic ? ' · רישיון ' . esc_html( $lic ) : ''; ?></p>
	<div class="nlpl-row">
		<?php echo $photo; // phpcs:ignore ?>
		<div class="nlpl-id">
			<p class="nlpl-name"><?php echo esc_html( $name ); ?><?php echo '' !== $brand && false === mb_strpos( $name, $brand ) ? '<span> · ' . esc_html( $brand ) . '</span>' : ''; ?></p>
			<?php if ( '' !== $head ) : ?><p class="nlpl-head"><?php echo esc_html( $head ); ?></p><?php endif; ?>
			<?php if ( $areas ) : ?><p class="nlpl-areas"><?php echo esc_html( implode( ', ', $areas ) ); ?></p><?php endif; ?>
		</div>
	</div>
	<div class="nlpl-cta">
		<a class="nlpl-btn nlpl-main" href="<?php echo esc_url( $href ); ?>" data-nl-ev="place_click" data-nl-slot="<?php echo esc_attr( $slot ); ?>">לנכסים של <?php echo esc_html( $name ); ?></a>
		<?php if ( '' !== $wa ) : ?><a class="nlpl-btn" target="_blank" rel="noopener" href="https://wa.me/<?php echo esc_attr( $wa ); ?>?text=<?php echo rawurlencode( $ask ); ?>" data-nl-ev="place_click" data-nl-slot="<?php echo esc_attr( $slot ); ?>">וואטסאפ</a><?php endif; ?>
	</div>
</aside>
		<?php
		return ob_get_clean();
	}
}

add_filter( 'the_content', function ( $content ) {
	if ( ! in_the_loop() || ! is_main_query() ) { return $content; }
	$pl = nadlan_pl_for_request();
	if ( ! $pl ) { return $content; }
	$card = nadlan_pl_card( $pl );
	if ( '' === $card ) { return $content; }
	$n = (int) get_post_meta( $pl, 'pl_after_h2', true );
	if ( $n > 0 ) {
		// before the (n+1)th section heading, so the card closes the n-th section
		$pos = -1;
		$off = 0;
		for ( $i = 0; $i <= $n; $i++ ) {
			$pos = strpos( $content, '<h2', $off );
			if ( false === $pos ) { break; }
			$off = $pos + 3;
		}
		if ( false !== $pos && $pos > 0 ) { return substr( $content, 0, $pos ) . $card . substr( $content, $pos ); }
	}
	return $content . $card;
}, 40 );

add_action( 'wp_footer', function () {
	if ( ! nadlan_pl_for_request() ) { return; }
	$url = esc_url_raw( rest_url( 'nadlan/v1/ev' ) );
	echo "\n<style id=\"nadlan-placement-css\">.nlpl{margin:28px 0;padding:18px 20px;border:1px solid var(--sa-line,#E3E1DA);border-radius:14px;background:var(--sa-surf,#fff);font-family:var(--sa-sans,Assistant,Arial,sans-serif);color:var(--sa-ink,#14212B)}.nlpl p{margin:0}.nlpl-tag{font-size:12px;letter-spacing:.02em;color:var(--sa-mute,#6B7680);margin-bottom:10px!important}.nlpl-row{display:flex;gap:14px;align-items:center}.nlpl-ph{width:64px;height:64px;border-radius:50%;object-fit:cover;object-position:50% 22%;flex:none}.nlpl-name{font-family:var(--sa-serif,'Noto Serif Hebrew',Georgia,serif);font-size:20px;font-weight:600;line-height:1.25}.nlpl-name span{font-family:var(--sa-sans,Assistant,Arial,sans-serif);font-size:15px;font-weight:400;color:var(--sa-ink2,#3B4753)}.nlpl-head{font-size:15px;color:var(--sa-ink2,#3B4753);margin-top:2px!important}.nlpl-areas{font-size:14px;color:var(--sa-mute,#6B7680);margin-top:4px!important}.nlpl-cta{display:flex;gap:10px;flex-wrap:wrap;margin-top:14px}.nlpl-btn{display:inline-flex;align-items:center;justify-content:center;min-height:44px;padding:0 18px;border-radius:999px;border:1px solid var(--sa-sea,#2F6F86);color:var(--sa-sea,#2F6F86);text-decoration:none;font-weight:600;font-size:15px}.nlpl-main{background:var(--sa-sea,#2F6F86);color:#fff}.nlpl-btn:focus-visible{outline:3px solid var(--sa-deep,#1F4B5C);outline-offset:2px}@media(max-width:520px){.nlpl-btn{flex:1}}</style>\n";
	echo "<script id=\"nadlan-placement-ev\">(function(){if(!navigator.sendBeacon)return;var u=" . wp_json_encode( $url ) . ";function s(c,e){try{navigator.sendBeacon(u,new Blob([JSON.stringify({e:e,pro:+c.dataset.pro,post:+c.dataset.post,slot:'pl-'+c.dataset.pl})],{type:'application/json'}))}catch(_){}}document.querySelectorAll('.nlpl').forEach(function(c){if('IntersectionObserver' in window){var o=new IntersectionObserver(function(x){if(x[0].isIntersecting){s(c,'place_view');o.disconnect()}},{threshold:.5});o.observe(c)}else{s(c,'place_view')}c.addEventListener('click',function(v){if(v.target.closest('[data-nl-ev]'))s(c,'place_click')})})})();</script>\n";
}, 41 );
