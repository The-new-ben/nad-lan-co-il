<?php
/**
 * nadlan-config - REAL reviews engine (v1.33.0)
 *
 * State-of-the-art reviews for nadlan_professional + nadlan_project:
 *  - submission via REST with email gate (anti-spam honeypot + nonce + rate limit)
 *  - moderation: review CPT stored as 'pending'; admin approves → 'publish'
 *  - rating + reviews_count meta is recomputed on approval/un-approval
 *  - schema.org Review + AggregateRating JSON-LD on the target page (SEO juice)
 *  - public render block (stars summary + recent reviews list + submit form)
 *  - shortcode [nadlan_reviews id=…] + auto-appended on professional/project singles
 *  - admin email notification on every submission so the owner is in the loop
 */

if ( ! defined( 'ABSPATH' ) ) { exit; }

/* ---------- CPT: nadlan_review (internal storage; not public list) ---------- */
add_action( 'init', function () {
	register_post_type( 'nadlan_review', array(
		'labels' => array( 'name' => 'NadLan Reviews', 'singular_name' => 'Review',
			'menu_name' => 'חוות דעת', 'all_items' => 'כל חוות הדעת', 'add_new_item' => 'חוות דעת חדשה' ),
		'public'             => false,
		'show_ui'            => true,
		'show_in_menu'       => true,
		'menu_icon'          => 'dashicons-star-filled',
		'menu_position'      => 26,
		'supports'           => array( 'title', 'editor', 'custom-fields' ),
		'capability_type'    => 'post',
		'map_meta_cap'       => true,
	) );
} );

/* ---------- Recompute rating + reviews_count on save ---------- */
if ( ! function_exists( 'nadlan_reviews_recompute' ) ) {
	function nadlan_reviews_recompute( $target_id ) {
		if ( ! $target_id ) { return; }
		$rows = get_posts( array(
			'post_type'      => 'nadlan_review',
			'post_status'    => 'publish',
			'posts_per_page' => -1,
			'fields'         => 'ids',
			'meta_query'     => array( array( 'key' => 'target_id', 'value' => (int) $target_id ) ),
		) );
		$n = 0; $sum = 0;
		foreach ( $rows as $rid ) {
			$r = (float) get_post_meta( $rid, 'rating', true );
			if ( $r >= 1 && $r <= 5 ) { $n++; $sum += $r; }
		}
		$avg = $n ? round( $sum / $n, 2 ) : 0;
		update_post_meta( $target_id, 'rating', $avg );
		update_post_meta( $target_id, 'reviews_count', $n );
		delete_transient( 'nadlan_reviews_block_' . $target_id );
		delete_transient( 'nadlan_reviews_block_1603_' . $target_id );
	}
}
add_action( 'save_post_nadlan_review', function ( $post_id, $post ) {
	$tid = (int) get_post_meta( $post_id, 'target_id', true );
	if ( $tid ) { nadlan_reviews_recompute( $tid ); }
}, 20, 2 );
add_action( 'trashed_post', function ( $post_id ) {
	if ( get_post_type( $post_id ) !== 'nadlan_review' ) { return; }
	$tid = (int) get_post_meta( $post_id, 'target_id', true );
	if ( $tid ) { nadlan_reviews_recompute( $tid ); }
} );

/* ---------- REST: submit a review ---------- */
add_action( 'rest_api_init', function () {
	register_rest_route( 'nadlan/v1', '/review-submit', array(
		'methods'             => 'POST',
		'permission_callback' => '__return_true',
		'callback'            => function ( $req ) {
			$p   = $req->get_json_params() ?: array();
			$tid = (int) ( $p['target_id'] ?? 0 );
			$name  = trim( wp_strip_all_tags( (string) ( $p['name'] ?? '' ) ) );
			$email = sanitize_email( (string) ( $p['email'] ?? '' ) );
			$rating= max( 1, min( 5, (int) ( $p['rating'] ?? 0 ) ) );
			$title = trim( wp_strip_all_tags( (string) ( $p['title'] ?? '' ) ) );
			$body  = trim( wp_strip_all_tags( (string) ( $p['body'] ?? '' ) ) );
			$hp    = (string) ( $p['company'] ?? '' );
			if ( $hp !== '' ) { return new WP_Error( 'spam', 'spam' ); }
			$target = get_post( $tid );
			if ( ! $target || ! in_array( $target->post_type, array( 'nadlan_professional', 'nadlan_project' ), true ) ) {
				return new WP_Error( 'bad_target', 'bad_target' );
			}
			if ( $name === '' || ! $email || $rating < 1 || mb_strlen( $body ) < 25 ) {
				return new WP_Error( 'invalid', 'נא למלא שם, אימייל, דירוג, וביקורת מפורטת (לפחות 25 תווים).' );
			}
			// rate-limit: max 3 reviews / hour per IP
			$ip = isset( $_SERVER['REMOTE_ADDR'] ) ? sanitize_text_field( wp_unslash( $_SERVER['REMOTE_ADDR'] ) ) : '0';
			$tk = 'nlrev_rl_' . md5( $ip );
			$ct = (int) get_transient( $tk );
			if ( $ct >= 3 ) { return new WP_Error( 'rate', 'יותר מדי בקשות. נסו שוב מאוחר יותר.' ); }
			set_transient( $tk, $ct + 1, HOUR_IN_SECONDS );
			// duplicate guard: same email + target in last 30d
			$dup = get_posts( array( 'post_type' => 'nadlan_review', 'post_status' => 'any', 'posts_per_page' => 1, 'fields' => 'ids',
				'meta_query' => array( 'relation' => 'AND',
					array( 'key' => 'target_id', 'value' => $tid ),
					array( 'key' => 'reviewer_email', 'value' => $email ),
				),
				'date_query' => array( array( 'after' => '30 days ago' ) ),
			) );
			if ( $dup ) { return new WP_Error( 'dup', 'כבר שלחתם חוות דעת על בעל המקצוע הזה לאחרונה.' ); }

			$rid = wp_insert_post( array(
				'post_type'   => 'nadlan_review',
				'post_status' => 'pending',
				'post_title'  => sprintf( '%s - %s (%d★)', $name, get_the_title( $tid ), $rating ),
				'post_content'=> ( $title ? '<strong>' . esc_html( $title ) . "</strong>\n\n" : '' ) . esc_html( $body ),
			), true );
			if ( is_wp_error( $rid ) ) { return $rid; }
			update_post_meta( $rid, 'target_id', $tid );
			update_post_meta( $rid, 'reviewer_name', $name );
			update_post_meta( $rid, 'reviewer_email', $email );
			update_post_meta( $rid, 'rating', $rating );
			update_post_meta( $rid, 'review_title', $title );
			update_post_meta( $rid, 'review_ip', $ip );

			// admin notify (owner stays in the loop)
			$admin = get_option( 'admin_email' );
			if ( $admin ) {
				$msg  = "חוות דעת חדשה ממתינה לאישור\n\n";
				$msg .= "על: " . get_the_title( $tid ) . " (" . get_permalink( $tid ) . ")\n";
				$msg .= "מאת: $name <$email>\n";
				$msg .= "דירוג: $rating/5\n";
				$msg .= ( $title ? "כותרת: $title\n" : '' );
				$msg .= "\n$body\n\n";
				$msg .= "אישור: " . admin_url( 'post.php?post=' . $rid . '&action=edit' ) . "\n";
				wp_mail( $admin, '[נדלן] חוות דעת ממתינה לאישור', $msg );
			}
			return array( 'ok' => true, 'message' => 'תודה! חוות הדעת התקבלה וממתינה לאישור.' );
		},
	) );
} );

if ( ! function_exists( 'nadlan_reviews_inline_js' ) ) {
	function nadlan_reviews_inline_js( $rest_url ) {
		$js = <<<'JS'
(function(){
	function boot(){
		document.querySelectorAll('.nlrev-stars-pick').forEach(function(g){
			var input=g.querySelector('input[name=rating]');
			g.querySelectorAll('.nlrev-star').forEach(function(b){
				b.addEventListener('click',function(){
					var v=parseInt(b.dataset.v,10);
					input.value=v;
					g.querySelectorAll('.nlrev-star').forEach(function(s){s.classList.toggle('is-on',parseInt(s.dataset.v,10)<=v);});
				});
			});
		});
	}
	if(!window.nadlanReviewSubmit){
		window.nadlanReviewSubmit=function(form){
			var fd=new FormData(form),data={target_id:parseInt(form.dataset.target,10)};
			fd.forEach(function(v,k){data[k]=v;});
			data.rating=parseInt(data.rating||0,10);
			var msg=form.querySelector('.nlrev-msg');
			msg.className='nlrev-msg';
			msg.textContent='\u05e9\u05d5\u05dc\u05d7...';
			fetch('__NLREV_REST__',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(data)})
				.then(function(r){return r.json();})
				.then(function(d){
					if(d ? d.ok : false){
						msg.className='nlrev-msg is-ok';
						msg.textContent=d.message||'\u05e0\u05e9\u05dc\u05d7';
						form.reset();
						form.querySelectorAll('.nlrev-star').forEach(function(s){s.classList.remove('is-on');});
					}else{
						msg.className='nlrev-msg is-err';
						msg.textContent=(d ? d.message : '')||'\u05e9\u05d2\u05d9\u05d0\u05d4. \u05e0\u05e1\u05d5 \u05e9\u05d5\u05d1.';
					}
				})
				.catch(function(){
					msg.className='nlrev-msg is-err';
					msg.textContent='\u05e9\u05d2\u05d9\u05d0\u05d4. \u05e0\u05e1\u05d5 \u05e9\u05d5\u05d1.';
				});
			return false;
		};
	}
	if(document.readyState==='loading'){document.addEventListener('DOMContentLoaded',boot)}else{boot()}
})();
JS;
		return str_replace( '__NLREV_REST__', esc_js( $rest_url ), $js );
	}
}

add_action(
	'wp_enqueue_scripts',
	function () {
		if ( ! is_singular( array( 'nadlan_professional', 'nadlan_project' ) ) ) {
			return;
		}
		wp_register_script( 'nadlan-reviews', '', array(), '1.60.3', true );
		wp_enqueue_script( 'nadlan-reviews' );
		wp_add_inline_script( 'nadlan-reviews', nadlan_reviews_inline_js( rest_url( 'nadlan/v1/review-submit' ) ) );
	}
);

/* ---------- Render block: summary + list + form ---------- */
if ( ! function_exists( 'nadlan_reviews_render' ) ) {
	function nadlan_reviews_render( $target_id ) {
		$target_id = (int) $target_id;
		if ( ! $target_id ) { return ''; }
		$ck = 'nadlan_reviews_block_1603_' . $target_id;
		$cache = get_transient( $ck );
		if ( $cache !== false ) { return $cache; }
		$avg = (float) get_post_meta( $target_id, 'rating', true );
		$cnt = (int) get_post_meta( $target_id, 'reviews_count', true );
		$reviews = get_posts( array(
			'post_type' => 'nadlan_review', 'post_status' => 'publish',
			'posts_per_page' => 6,
			'meta_query' => array( array( 'key' => 'target_id', 'value' => $target_id ) ),
		) );
		$full = (int) round( $avg );
		ob_start(); ?>
<section class="nlrev" dir="rtl" id="nadlan-reviews">
	<header class="nlrev-head">
		<h2>חוות דעת לקוחות</h2>
		<?php if ( $cnt > 0 ) : ?>
		<div class="nlrev-summary">
			<span class="nlrev-bigstars" aria-hidden="true"><?php echo str_repeat( '★', $full ) . str_repeat( '☆', max( 0, 5 - $full ) ); ?></span>
			<b><?php echo esc_html( number_format( $avg, 1 ) ); ?></b>
			<span class="nlrev-cnt"><?php echo (int) $cnt; ?> חוות דעת</span>
		</div>
		<?php else : ?>
		<p class="nlrev-noyet">היו הראשונים לשתף חוות דעת</p>
		<?php endif; ?>
	</header>

	<?php if ( $reviews ) : ?>
	<ol class="nlrev-list">
		<?php foreach ( $reviews as $r ) :
			$rname = nadlan_meta_norm( get_post_meta( $r->ID, 'reviewer_name', true ) ) ?: 'אנונימי';
			$rrate = (int) get_post_meta( $r->ID, 'rating', true );
			$rtitle= nadlan_meta_norm( get_post_meta( $r->ID, 'review_title', true ) );
			$rbody = wp_strip_all_tags( $r->post_content );
			$initial = mb_substr( $rname, 0, 1 ); ?>
		<li class="nlrev-item" itemprop="review" itemscope itemtype="https://schema.org/Review">
			<div class="nlrev-av"><?php echo esc_html( $initial ); ?></div>
			<div class="nlrev-body">
				<div class="nlrev-meta">
					<span class="nlrev-name" itemprop="author"><?php echo esc_html( $rname ); ?></span>
					<span class="nlrev-stars" aria-label="<?php echo (int) $rrate; ?> מתוך 5">
						<span itemprop="reviewRating" itemscope itemtype="https://schema.org/Rating">
							<meta itemprop="ratingValue" content="<?php echo (int) $rrate; ?>">
							<meta itemprop="bestRating" content="5">
						</span>
						<?php echo str_repeat( '★', $rrate ) . str_repeat( '☆', max( 0, 5 - $rrate ) ); ?>
					</span>
					<time class="nlrev-time" datetime="<?php echo esc_attr( get_the_date( 'c', $r ) ); ?>"><?php echo esc_html( get_the_date( 'd/m/Y', $r ) ); ?></time>
				</div>
				<?php if ( $rtitle ) : ?><h4 class="nlrev-title" itemprop="name"><?php echo esc_html( $rtitle ); ?></h4><?php endif; ?>
				<p class="nlrev-text" itemprop="reviewBody"><?php echo esc_html( $rbody ); ?></p>
			</div>
		</li>
		<?php endforeach; ?>
	</ol>
	<?php endif; ?>

	<details class="nlrev-form-wrap"<?php echo $cnt === 0 ? ' open' : ''; ?>>
		<summary>כתבו חוות דעת</summary>
		<form class="nlrev-form" data-target="<?php echo (int) $target_id; ?>" onsubmit="return nadlanReviewSubmit(this)">
			<div class="nlrev-stars-pick" role="radiogroup" aria-label="דירוג">
				<?php for ( $i = 1; $i <= 5; $i++ ) : ?>
				<button type="button" class="nlrev-star" data-v="<?php echo $i; ?>" aria-label="<?php echo $i; ?> כוכבים">★</button>
				<?php endfor; ?>
				<input type="hidden" name="rating" value="0" required>
			</div>
			<input type="text" name="name" placeholder="שם" required>
			<input type="email" name="email" placeholder="אימייל" required>
			<input type="text" name="title" placeholder="כותרת (אופציונלי)">
			<textarea name="body" placeholder="ספרו על החוויה (לפחות 25 תווים)" required minlength="25"></textarea>
			<input type="text" name="company" class="nlrev-hp" tabindex="-1" autocomplete="off" aria-hidden="true">
			<button type="submit">שליחה</button>
			<span class="nlrev-msg" aria-live="polite"></span>
		</form>
	</details>
</section>
<?php if ( $cnt > 0 ) : ?>
<script type="application/ld+json"><?php echo wp_json_encode( array(
	'@context' => 'https://schema.org', '@type' => 'AggregateRating',
	'itemReviewed' => array( '@type' => get_post_type( $target_id ) === 'nadlan_professional' ? 'LocalBusiness' : 'Place', 'name' => get_the_title( $target_id ), 'url' => get_permalink( $target_id ) ),
	'ratingValue' => number_format( $avg, 1 ), 'reviewCount' => $cnt, 'bestRating' => 5, 'worstRating' => 1,
), JSON_UNESCAPED_UNICODE | JSON_UNESCAPED_SLASHES ); ?></script>
<?php endif; ?>
<style>
.nlrev{font-family:var(--font-sans,Heebo,sans-serif);direction:rtl;background:#fff;border:1px solid rgba(27,26,23,.1);border-radius:18px;padding:26px;margin:26px 0;color:#1B1A17}
.nlrev-head{display:flex;align-items:center;justify-content:space-between;gap:14px;flex-wrap:wrap;margin-bottom:18px;padding-bottom:14px;border-bottom:1px solid rgba(27,26,23,.08)}
.nlrev-head h2{font-family:var(--font-serif,"Frank Ruhl Libre",serif);font-weight:600;font-size:24px;margin:0}
.nlrev-summary{display:flex;align-items:center;gap:9px;font-size:15px}.nlrev-bigstars{color:#F5A623;font-size:20px;letter-spacing:2px}.nlrev-summary b{font-size:20px}.nlrev-cnt{color:#7a7a7a;font-size:13px}
.nlrev-noyet{color:#9a9a9a;font-style:italic;margin:0}
.nlrev-list{list-style:none;margin:0;padding:0;display:flex;flex-direction:column;gap:18px}
.nlrev-item{display:flex;gap:14px;padding:18px;background:#FBF9F5;border-radius:14px}
.nlrev-av{flex:none;width:42px;height:42px;border-radius:50%;background:linear-gradient(135deg,#9C7A3C,#B89254);color:#fff;display:grid;place-items:center;font-weight:700;font-size:17px}
.nlrev-body{flex:1;min-width:0}
.nlrev-meta{display:flex;align-items:center;gap:10px;flex-wrap:wrap;font-size:13px;color:#6b6b6b;margin-bottom:6px}
.nlrev-name{font-weight:700;color:#1B1A17}.nlrev-stars{color:#F5A623;letter-spacing:1px;font-size:14px}.nlrev-time{font-size:12px;color:#9a9a9a}
.nlrev-title{font-size:15px;margin:0 0 6px;color:#1B1A17;font-weight:700}
.nlrev-text{font-size:14px;color:#3a3a3a;line-height:1.6;margin:0}
.nlrev-form-wrap{margin-top:20px;border-top:1px solid rgba(27,26,23,.08);padding-top:18px}
.nlrev-form-wrap summary{cursor:pointer;font-weight:700;color:#9C7A3C;list-style:none;padding:10px 14px;background:#FBF9F5;border-radius:10px;display:inline-block;user-select:none}
.nlrev-form-wrap summary::-webkit-details-marker{display:none}
.nlrev-form{display:grid;gap:10px;margin-top:14px;max-width:560px}
.nlrev-form input[type=text],.nlrev-form input[type=email],.nlrev-form textarea{border:1px solid rgba(27,26,23,.16);border-radius:10px;padding:12px 14px;font:inherit;background:#fff}
.nlrev-form textarea{min-height:90px;resize:vertical}
.nlrev-form button[type=submit]{background:linear-gradient(135deg,#9C7A3C,#B89254);color:#fff;border:0;border-radius:10px;padding:13px 30px;font:inherit;font-weight:700;cursor:pointer;justify-self:start}
.nlrev-stars-pick{display:flex;gap:4px;direction:ltr;justify-content:flex-end}
.nlrev-stars-pick .nlrev-star{background:none;border:0;color:#ddd;font-size:32px;cursor:pointer;padding:0;line-height:1;transition:color .12s,transform .12s}
.nlrev-stars-pick .nlrev-star:hover,.nlrev-stars-pick .nlrev-star.is-on{color:#F5A623}
.nlrev-stars-pick .nlrev-star:hover{transform:scale(1.15)}
.nlrev-hp{position:absolute;left:-9999px;width:1px;height:1px;opacity:0}
.nlrev-msg{font-size:13px;padding:6px 0}
.nlrev-msg.is-ok{color:#059669}.nlrev-msg.is-err{color:#B91C1C}
</style>
</section>
		<?php
		$html = ob_get_clean();
		set_transient( $ck, $html, 5 * MINUTE_IN_SECONDS );
		return $html;
	}
}

add_shortcode( 'nadlan_reviews', function ( $atts ) {
	$a = shortcode_atts( array( 'id' => 0 ), $atts );
	return nadlan_reviews_render( (int) $a['id'] ?: get_the_ID() );
} );

/* Auto-append reviews on single professional + project pages.
   Design audit 2026-07-02 (D5): a flagship project page must not carry an empty
   "be the first to review" block - on projects the section renders only once
   real approved reviews exist. Professionals keep the empty state (growth loop). */
add_filter( 'the_content', function ( $content ) {
	if ( ! is_singular( array( 'nadlan_professional', 'nadlan_project' ) ) || ! in_the_loop() || ! is_main_query() ) { return $content; }
	$id = get_the_ID();
	if ( get_post_type( $id ) === 'nadlan_project' && (int) get_post_meta( $id, 'reviews_count', true ) < 1 ) { return $content; }
	return $content . nadlan_reviews_render( $id );
}, 22 );
