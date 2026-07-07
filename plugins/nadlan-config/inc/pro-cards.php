<?php
/**
 * nadlan-config - PRO CARDS on content (owner 2026-07-07: "this is the business
 * behind all this").
 *
 * Every practice-area content page (encyclopedia term, guide, article) floats
 * the professionals who own that niche: a rich card woven INTO the reading
 * flow (after the second heading - the point where a reader who kept going is
 * genuinely interested), plus an experts row at the end when more than one
 * matches. Mobile-first: the card is a full-width native block, never a
 * floating element fighting the WhatsApp cluster.
 *
 * MATCHING (three layers, most specific wins):
 *  1) PINNED: `procard_pros` meta on the content (comma-separated professional
 *     IDs) - full manual control per page.
 *  2) DOMAIN MAP: content signals (glossary enc_domain / nadlan_term_cat slugs /
 *     post category slugs + names) -> profession keys, via the editable option
 *     `nadlan_procard_map` merged over honest defaults.
 *  3) Nothing matches -> nothing renders. No filler.
 *
 * ORDERING = THE MONETIZATION: premier > pro > free (then rating, then newer).
 * Paid cards carry an honest "ממומן" chip; seeded ratings keep the
 * "נתוני דוגמה" badge law from the directory. Caps: nadlan_procard_max (2
 * inline; the end row shows up to 6). Kill switch: nadlan_procard_enabled.
 */

if ( ! defined( 'ABSPATH' ) ) { exit; }

if ( ! function_exists( 'nadlan_procard_default_map' ) ) {
	function nadlan_procard_default_map() {
		return array(
			// token (matched inside domain/category slug+name) => profession keys
			'משפט'     => array( 'lawyer' ), 'מיסוי' => array( 'lawyer', 'accountant' ), 'מס' => array( 'lawyer', 'accountant' ),
			'legal'    => array( 'lawyer' ), 'tax' => array( 'lawyer', 'accountant' ),
			'משכנתא'   => array( 'mashkanta' ), 'מימון' => array( 'mashkanta' ), 'finance' => array( 'mashkanta' ), 'mortgage' => array( 'mashkanta' ),
			'שמאות'    => array( 'shamai' ), 'שמאי' => array( 'shamai' ), 'appraisal' => array( 'shamai' ),
			'בדק'      => array( 'bedek_bait', 'engineer' ), 'ליקויי' => array( 'bedek_bait', 'engineer' ),
			'הנדסה'    => array( 'engineer' ), 'קונסטרוקציה' => array( 'engineer' ), 'engineering' => array( 'engineer' ),
			'תכנון'    => array( 'urban_planner', 'architect' ), 'planning' => array( 'urban_planner', 'architect' ),
			'אדריכל'   => array( 'architect' ), 'architecture' => array( 'architect' ),
			'עיצוב'    => array( 'interior_designer' ), 'design' => array( 'interior_designer' ),
			'בנייה'    => array( 'kablan', 'engineer' ), 'קבלן' => array( 'kablan' ), 'construction' => array( 'kablan', 'engineer' ),
			'התחדשות'  => array( 'kablan', 'lawyer' ), 'תמ"א' => array( 'kablan', 'lawyer' ),
			'תיווך'    => array( 'metavech' ), 'brokerage' => array( 'metavech' ),
			'ניהול'    => array( 'property_manager' ), 'management' => array( 'property_manager' ),
			'מדידה'    => array( 'surveyor' ), 'טאבו' => array( 'lawyer', 'surveyor' ), 'רישום' => array( 'lawyer' ),
			'חשבונאות' => array( 'accountant' ),
		);
	}
}

if ( ! function_exists( 'nadlan_procard_signals' ) ) {
	function nadlan_procard_signals( $post_id ) {
		$sig = array();
		$pt  = get_post_type( $post_id );
		if ( 'nadlan_term' === $pt ) {
			$sig[] = (string) get_post_meta( $post_id, 'enc_domain', true );
			foreach ( (array) wp_get_object_terms( $post_id, 'nadlan_term_cat', array( 'fields' => 'all' ) ) as $t ) {
				if ( ! is_wp_error( $t ) && $t ) { $sig[] = $t->name; $sig[] = $t->slug; }
			}
			$sig[] = get_the_title( $post_id );
		} elseif ( 'post' === $pt ) {
			foreach ( (array) get_the_category( $post_id ) as $c ) { $sig[] = $c->name; $sig[] = $c->slug; }
			foreach ( (array) wp_get_post_tags( $post_id ) as $t ) { $sig[] = $t->name; }
		}
		return array_filter( array_map( 'strval', $sig ) );
	}
}

if ( ! function_exists( 'nadlan_procard_match' ) ) {
	function nadlan_procard_match( $post_id ) {
		// 1) pinned professionals - full manual control
		$pinned = array_filter( array_map( 'absint', explode( ',', (string) get_post_meta( $post_id, 'procard_pros', true ) ) ) );
		if ( $pinned ) {
			$out = array();
			foreach ( $pinned as $pid ) {
				$p = get_post( $pid );
				if ( $p && 'nadlan_professional' === $p->post_type && 'publish' === $p->post_status ) { $out[] = $p; }
			}
			if ( $out ) { return $out; }
		}
		// 2) domain map
		$map = array_merge( nadlan_procard_default_map(), (array) get_option( 'nadlan_procard_map', array() ) );
		$professions = array();
		$signals = nadlan_procard_signals( $post_id );
		foreach ( $signals as $s ) {
			foreach ( $map as $token => $keys ) {
				if ( '' !== $token && false !== mb_stripos( $s, (string) $token ) ) {
					$professions = array_merge( $professions, (array) $keys );
				}
			}
		}
		$professions = array_values( array_unique( $professions ) );
		if ( ! $professions ) { return array(); }
		$q = new WP_Query( array(
			'post_type' => 'nadlan_professional', 'post_status' => 'publish', 'posts_per_page' => 12,
			'no_found_rows' => true,
			'meta_query' => array( array( 'key' => 'profession', 'value' => $professions, 'compare' => 'IN' ) ),
		) );
		$posts = $q->posts;
		// the monetization order: ACTIVE DOMAIN SPONSORS first (the console
		// product), then premier > pro > free, then rating, then newer
		$sponsored = function ( $pid ) use ( $professions ) {
			if ( (int) get_post_meta( $pid, 'procard_sponsor_until', true ) < time() ) { return false; }
			$doms = array_filter( array_map( 'trim', explode( ',', (string) get_post_meta( $pid, 'procard_sponsor_domains', true ) ) ) );
			if ( ! $doms ) { return true; } // sponsor of everything they match
			foreach ( $doms as $d ) {
				if ( in_array( $d, $professions, true ) ) { return true; }
			}
			return false;
		};
		usort( $posts, function ( $a, $b ) use ( $sponsored ) {
			$sa = $sponsored( $a->ID ) ? 1 : 0; $sb = $sponsored( $b->ID ) ? 1 : 0;
			if ( $sa !== $sb ) { return $sb <=> $sa; }
			$w = array( 'premier' => 3, 'pro' => 2, 'free' => 1 );
			$ta = $w[ get_post_meta( $a->ID, 'paid_tier', true ) ] ?? 1;
			$tb = $w[ get_post_meta( $b->ID, 'paid_tier', true ) ] ?? 1;
			if ( $ta !== $tb ) { return $tb <=> $ta; }
			$ra = (float) get_post_meta( $a->ID, 'rating', true );
			$rb = (float) get_post_meta( $b->ID, 'rating', true );
			if ( $ra !== $rb ) { return $rb <=> $ra; }
			return strtotime( $b->post_date ) <=> strtotime( $a->post_date );
		} );
		return $posts;
	}
}

if ( ! function_exists( 'nadlan_procard_html' ) ) {
	function nadlan_procard_html( $p, $compact = false ) {
		$id    = $p->ID;
		$pm    = function_exists( 'nadlan_dir_prof_meta' ) ? nadlan_dir_prof_meta( (string) get_post_meta( $id, 'profession', true ) ) : array( 'label' => 'בעל/ת מקצוע', 'color' => '#9C7A3C' );
		$img   = get_the_post_thumbnail_url( $id, 'medium' );
		$city  = (string) get_post_meta( $id, 'city', true );
		$tier  = (string) get_post_meta( $id, 'paid_tier', true );
		$spon  = (int) get_post_meta( $id, 'procard_sponsor_until', true ) >= time();
		update_post_meta( $id, 'procard_impressions', (int) get_post_meta( $id, 'procard_impressions', true ) + 1 );
		$rate  = (float) get_post_meta( $id, 'rating', true );
		$rcnt  = (int) get_post_meta( $id, 'reviews_count', true );
		$phone = preg_replace( '/[^0-9+]/', '', (string) get_post_meta( $id, 'phone', true ) );
		$demo  = $rate && ! get_post_meta( $id, 'reviews_verified', true );
		$verified = get_post_meta( $id, 'claim_status', true ) === 'verified';
		ob_start(); ?>
<div class="nlprc<?php echo $compact ? ' nlprc--sm' : ''; ?>" dir="rtl">
	<?php if ( $spon || ( 'free' !== $tier && $tier ) ) : ?><span class="nlprc-spon">ממומן</span><?php endif; ?>
	<a class="nlprc-media" href="<?php echo esc_url( get_permalink( $id ) ); ?>"<?php echo $img ? ' style="background-image:url(' . esc_url( $img ) . ')"' : ''; ?>>
		<?php if ( ! $img ) : ?><span class="nlprc-mono"><?php echo esc_html( mb_substr( get_the_title( $id ), 0, 1 ) ); ?></span><?php endif; ?>
	</a>
	<div class="nlprc-bd">
		<span class="nlprc-prof" style="color:<?php echo esc_attr( $pm['color'] ?? '#9C7A3C' ); ?>"><?php echo esc_html( $pm['label'] ?? '' ); ?><?php echo $verified ? ' <i class="nlprc-ver">✓ מאומת</i>' : ''; ?></span>
		<a class="nlprc-name" href="<?php echo esc_url( get_permalink( $id ) ); ?>"><?php echo esc_html( get_the_title( $id ) ); ?></a>
		<span class="nlprc-meta"><?php echo esc_html( $city ); ?><?php if ( $rate ) : ?><?php echo $city ? ' · ' : ''; ?><b>★ <?php echo esc_html( number_format( $rate, 1 ) ); ?></b> (<?php echo (int) $rcnt; ?>)<?php echo $demo ? ' <i class="nlprc-demo">נתוני דוגמה</i>' : ''; ?><?php endif; ?></span>
		<?php if ( ! $compact ) : ?>
		<div class="nlprc-cta">
			<a class="nlprc-go" href="<?php echo esc_url( get_permalink( $id ) ); ?>">לכרטיס המלא ←</a>
			<?php if ( $phone ) : ?><a class="nlprc-call" href="tel:<?php echo esc_attr( $phone ); ?>">התקשרו עכשיו</a><?php endif; ?>
		</div>
		<?php endif; ?>
	</div>
</div>
		<?php
		return ob_get_clean();
	}
}

add_filter( 'the_content', function ( $content ) {
	if ( ! is_singular( array( 'nadlan_term', 'post' ) ) || ! in_the_loop() || ! is_main_query() ) { return $content; }
	if ( (int) get_option( 'nadlan_procard_enabled', 1 ) !== 1 ) { return $content; }
	$pros = nadlan_procard_match( get_the_ID() );
	if ( ! $pros ) { return $content; }
	$max  = max( 1, (int) get_option( 'nadlan_procard_max', 2 ) );
	$lead = array_slice( $pros, 0, 1 );
	$rest = array_slice( $pros, 1, 5 );

	$eyebrow = '<p class="nlprc-eyebrow">המומחים של התחום</p>';
	$card    = $eyebrow . nadlan_procard_html( $lead[0] );

	// weave AFTER the second heading: the reader who reached this point cares
	$parts = preg_split( '/(<h2[^>]*>)/i', $content, -1, PREG_SPLIT_DELIM_CAPTURE );
	if ( count( $parts ) >= 5 ) {
		// parts: [before, h2tag, seg, h2tag, seg, ...] - inject before the 2nd h2
		$parts[3] = '<aside class="nlprc-slot" aria-label="מומחים בתחום">' . $card . '</aside>' . $parts[3];
		$content  = implode( '', $parts );
	} else {
		$content .= '<aside class="nlprc-slot" aria-label="מומחים בתחום">' . $card . '</aside>';
	}
	// experts row at the end (compact cards)
	if ( $rest && $max > 1 ) {
		$row = '';
		foreach ( array_slice( $rest, 0, 5 ) as $p ) { $row .= nadlan_procard_html( $p, true ); }
		$content .= '<aside class="nlprc-row-wrap" aria-label="עוד מומחים בתחום"><p class="nlprc-eyebrow">עוד מומחים בתחום</p><div class="nlprc-row">' . $row . '</div></aside>';
	}
	$css = '<style>
.nlprc-slot{margin:26px 0}
.nlprc-eyebrow{font:700 11.5px/1 Heebo,sans-serif;letter-spacing:.12em;color:#9C7A3C;margin:0 0 8px}
.nlprc{position:relative;display:flex;gap:16px;align-items:stretch;background:linear-gradient(135deg,#fff,#FBF8F2);border:1px solid #D6C189;border-radius:16px;padding:14px;box-shadow:0 16px 38px -26px rgba(27,26,23,.4)}
.nlprc-spon{position:absolute;top:10px;inset-inline-end:12px;font:600 10.5px/1 Heebo,sans-serif;color:#6D665C;background:#F3EEE3;border:1px solid #E2DCD0;border-radius:6px;padding:4px 7px}
.nlprc-media{flex:0 0 92px;height:92px;border-radius:12px;background:#14130F center/cover no-repeat;display:flex;align-items:center;justify-content:center;text-decoration:none;align-self:center}
.nlprc-mono{font:700 2rem/1 "Frank Ruhl Libre",serif;color:#E9D9A8}
.nlprc-bd{display:flex;flex-direction:column;gap:3px;min-width:0;justify-content:center}
.nlprc-prof{font:700 11.5px/1.2 Heebo,sans-serif;letter-spacing:.06em}
.nlprc-ver{font-style:normal;color:#517048;font-weight:700}
.nlprc-name{font-family:"Frank Ruhl Libre",serif;font-size:1.25rem;color:#1B1A17;text-decoration:none;font-weight:700}
.nlprc-name:hover{color:#9C7A3C}
.nlprc-meta{font:400 12.5px/1.4 Heebo,sans-serif;color:#6D665C}
.nlprc-meta b{color:#9C7A3C}
.nlprc-demo{font-style:normal;font-size:10.5px;color:#6D665C;background:#F3EEE3;border-radius:5px;padding:2px 5px}
.nlprc-cta{display:flex;gap:8px;margin-top:8px;flex-wrap:wrap}
.nlprc-go{font:700 13px/1 Heebo,sans-serif;color:#FAF7F1;background:#1B1A17;border-radius:9px;padding:10px 14px;text-decoration:none}
.nlprc-go:hover{background:#9C7A3C;color:#FAF7F1}
.nlprc-call{font:700 13px/1 Heebo,sans-serif;color:#1B1A17;border:1.5px solid #9C7A3C;border-radius:9px;padding:9px 14px;text-decoration:none}
.nlprc-row-wrap{margin:30px 0 8px}
.nlprc-row{display:grid;grid-template-columns:repeat(auto-fill,minmax(240px,1fr));gap:10px}
.nlprc--sm{padding:10px;gap:10px}
.nlprc--sm .nlprc-media{flex-basis:56px;height:56px;border-radius:10px}
.nlprc--sm .nlprc-name{font-size:1rem}
.nlprc--sm .nlprc-mono{font-size:1.3rem}
@media(max-width:560px){.nlprc{padding:12px}.nlprc-media{flex-basis:76px;height:76px}.nlprc-name{font-size:1.12rem}.nlprc-cta a{flex:1;text-align:center}}
</style>';
	return $content . $css;
}, 14 );

/* meta for manual pinning, editable in the CMS */
add_action( 'init', function () {
	foreach ( array( 'nadlan_term', 'post', 'page' ) as $pt ) {
		register_post_meta( $pt, 'procard_pros', array(
			'show_in_rest' => true, 'single' => true, 'type' => 'string',
			'sanitize_callback' => 'sanitize_text_field',
			'auth_callback' => function () { return current_user_can( 'edit_posts' ); },
		) );
	}
}, 12 );


/* ---------------- THE SPONSORSHIP CONSOLE (enhancement #7) ----------------
 * Self-serve: a professional picks practice areas, pays through the existing
 * WooCommerce checkout (product id in option nadlan_procard_product), and the
 * boost activates itself on payment - 30 days, stacking like campaigns. */
add_filter( 'woocommerce_add_cart_item_data', function ( $data, $product_id ) {
	if ( (int) $product_id !== (int) get_option( 'nadlan_procard_product', 0 ) ) { return $data; }
	if ( isset( $_GET['sponsor_domains'] ) ) { $data['nadlan_sponsor_domains'] = sanitize_text_field( wp_unslash( $_GET['sponsor_domains'] ) ); } // phpcs:ignore
	if ( isset( $_GET['sponsor_card'] ) ) { $data['nadlan_sponsor_card'] = absint( $_GET['sponsor_card'] ); } // phpcs:ignore
	return $data;
}, 10, 2 );
add_action( 'woocommerce_checkout_create_order_line_item', function ( $item, $key, $values ) {
	if ( ! empty( $values['nadlan_sponsor_domains'] ) ) { $item->add_meta_data( '_nadlan_sponsor_domains', $values['nadlan_sponsor_domains'], true ); }
	if ( ! empty( $values['nadlan_sponsor_card'] ) ) { $item->add_meta_data( '_nadlan_card_id', (int) $values['nadlan_sponsor_card'], true ); }
}, 10, 3 );
add_action( 'woocommerce_payment_complete', function ( $order_id ) {
	if ( ! function_exists( 'wc_get_order' ) ) { return; }
	$pidopt = (int) get_option( 'nadlan_procard_product', 0 );
	if ( ! $pidopt ) { return; }
	$order = wc_get_order( $order_id );
	if ( ! $order ) { return; }
	foreach ( $order->get_items() as $item ) {
		if ( (int) $item->get_product_id() !== $pidopt ) { continue; }
		$card = (int) $item->get_meta( '_nadlan_card_id' );
		if ( ! $card || get_post_type( $card ) !== 'nadlan_professional' ) {
			// self-serve fallback: the customer's claimed card (owner_user_id)
			$cust = (int) $order->get_customer_id();
			$card = 0;
			if ( $cust ) {
				$own = get_posts( array( 'post_type' => 'nadlan_professional', 'posts_per_page' => 1, 'fields' => 'ids',
					'meta_query' => array( array( 'key' => 'owner_user_id', 'value' => $cust ) ) ) );
				$card = $own ? (int) $own[0] : 0;
			}
			if ( ! $card ) {
				$order->add_order_note( 'חסות תחום שולמה אך לא נמצא כרטיס מקצועי משויך ללקוח - יש לשייך ידנית (procard_sponsor_until על הכרטיס).' );
				continue;
			}
		}
		$doms = sanitize_text_field( (string) $item->get_meta( '_nadlan_sponsor_domains' ) );
		// stack from the later of now / current expiry (same law as campaigns)
		$base = max( time(), (int) get_post_meta( $card, 'procard_sponsor_until', true ) );
		update_post_meta( $card, 'procard_sponsor_until', $base + 30 * DAY_IN_SECONDS );
		if ( $doms !== '' ) { update_post_meta( $card, 'procard_sponsor_domains', $doms ); }
	}
}, 25 );

/* the picker rides the advertiser page next to the call-back form */
add_filter( 'the_content', function ( $content ) {
	if ( ! is_page( 'advertise' ) || is_admin() ) { return $content; }
	$product = (int) get_option( 'nadlan_procard_product', 0 );
	if ( ! $product || ! function_exists( 'wc_get_product' ) ) { return $content; }
	$prod = wc_get_product( $product );
	if ( ! $prod ) { return $content; }
	$price = wp_kses_post( $prod->get_price_html() );
	$cart  = esc_url( add_query_arg( array( 'add-to-cart' => $product ), wc_get_cart_url() ) );
	// values = profession KEYS (the same tokens the boost check intersects)
	$doms  = array( 'lawyer' => 'משפט ומיסוי', 'mashkanta' => 'משכנתאות ומימון', 'shamai' => 'שמאות', 'bedek_bait' => 'בדק בית', 'architect' => 'תכנון ואדריכלות', 'kablan' => 'בנייה והתחדשות', 'metavech' => 'תיווך', 'property_manager' => 'ניהול נכסים' );
	$chips = '';
	foreach ( $doms as $k => $d ) { $chips .= '<label class="nlspon-chip"><input type="checkbox" value="' . esc_attr( $k ) . '"><span>' . esc_html( $d ) . '</span></label>'; }
	$html = '<section class="nlspon" id="nlspon" dir="rtl" data-cart="' . $cart . '">
	<h2>חסות על תחום תוכן</h2>
	<p class="nlspon-sub">הכרטיס המקצועי שלכם מוצג ראשון בכל מונחי האנציקלופדיה והמדריכים של התחומים שתבחרו - עם סימון ממומן, הוגן וברור. ' . $price . ' ל-30 יום.</p>
	<div class="nlspon-chips">' . $chips . '</div>
	<a class="nlspon-btn" id="nlspon-go" href="' . $cart . '">להפעלת החסות ←</a>
	<p class="nlspon-note">לאחר התשלום החסות נדלקת אוטומטית על הכרטיס המקצועי שלכם. בלי חוזים ובלי טלפונים.</p>
</section>
<style>
.nlspon{max-width:640px;margin:22px auto;background:#fff;border:1px solid #D6C189;border-radius:18px;padding:26px 28px;font-family:Heebo,system-ui,sans-serif;box-shadow:0 18px 44px -24px rgba(27,26,23,.35)}
.nlspon h2{font-family:"Frank Ruhl Libre",serif;color:#1B1A17;margin:0 0 4px;font-size:1.5rem}
.nlspon-sub{color:#6D665C;font-size:14px;margin:0 0 14px}
.nlspon-chips{display:flex;flex-wrap:wrap;gap:8px;margin-bottom:16px}
.nlspon-chip input{position:absolute;opacity:0}
.nlspon-chip span{display:inline-block;font:600 13px/1 Heebo;color:#51483A;background:#F3EEE3;border:1.5px solid #E2DCD0;border-radius:999px;padding:9px 14px;cursor:pointer;transition:all .15s}
.nlspon-chip input:checked+span{background:#1B1A17;color:#FAF7F1;border-color:#1B1A17}
.nlspon-btn{display:block;text-align:center;background:#C2563A;color:#FAF7F1!important;font:700 15px/1 Heebo;border-radius:12px;padding:15px;text-decoration:none}
.nlspon-btn:hover{background:#a84730}
.nlspon-note{margin-top:10px;font-size:12px;color:#6D665C}
</style>
<script>
(function(){
	var box=document.getElementById("nlspon"),go=document.getElementById("nlspon-go");
	if(!box||!go)return;
	box.addEventListener("change",function(){
		var sel=[].map.call(box.querySelectorAll("input:checked"),function(i){return i.value}).join(",");
		var u=new URL(box.dataset.cart);
		if(sel)u.searchParams.set("sponsor_domains",sel);else u.searchParams.delete("sponsor_domains");
		go.href=u.toString();
	});
})();
</script>';
	return $content . $html;
}, 22 );
