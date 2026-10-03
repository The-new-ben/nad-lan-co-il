<?php
/**
 * auction.php - sale-by-offers product (owner order 2026-07-12).
 *
 * "Someone wants to present his apartment, put it on the net, and people
 *  give proposals... a separate mechanism of people proposing and the
 *  seller responding... end-to-end with the 3D models."
 *
 * EXTENDS the existing offers module (one-of-everything law - no second
 * offer engine): offers.php owns submission, dedupe, leading amount and
 * transparency modes; this module adds the missing product layer:
 * - the AUCTION BAND on single properties (leading offer, activity feed,
 *   the offer form, honest non-binding framing) - the 3D lives on the
 *   property page already (property-showroom).
 * - the SELLER RESPONSE mechanism: accept / counter / decline per offer
 *   (owner or admin), visible anonymized in the public activity feed.
 * - /sell-by-auction/ landing: SEO page + the conversational seller form.
 * - a labeled metabox on nadlan_property (offers_enabled, min,
 *   transparency, window) - no secret meta keys.
 * HONESTY LAW: every surface states this is NOT a legal auction; offers
 * are non-binding; the seller may pick any offer or none.
 */
if ( ! defined( 'ABSPATH' ) ) {
	exit;
}

if ( ! function_exists( 'nadlan_auction_active' ) ) {
	function nadlan_auction_active( $card_id ) {
		return function_exists( 'nadlan_offers_enabled' ) && nadlan_offers_enabled()
			&& get_post_meta( $card_id, 'offers_enabled', true ) === '1';
	}
}

/* ---------- seller response + public state ---------- */
add_action( 'rest_api_init', function () {
	register_rest_route( 'nadlan/v1', '/offer-respond', array(
		'methods'             => 'POST',
		'permission_callback' => function () { return is_user_logged_in(); },
		'callback'            => function ( WP_REST_Request $req ) {
			$p = $req->get_json_params() ?: array();
			$oid = absint( $p['offer'] ?? 0 );
			$act = sanitize_key( (string) ( $p['action'] ?? '' ) );
			if ( ! $oid || get_post_type( $oid ) !== 'nadlan_offer' || ! in_array( $act, array( 'accept', 'counter', 'decline' ), true ) ) {
				return new WP_Error( 'invalid', 'invalid', array( 'status' => 400 ) );
			}
			$card = (int) get_post_meta( $oid, 'offer_card_id', true );
			$owner = (int) get_post_meta( $card, 'owner_user_id', true );
			if ( ! current_user_can( 'manage_options' ) && get_current_user_id() !== $owner ) {
				return new WP_Error( 'forbidden', 'forbidden', array( 'status' => 401 ) );
			}
			$resp = array(
				'action' => $act,
				'amount' => 'counter' === $act ? max( 0, (float) ( $p['amount'] ?? 0 ) ) : 0,
				'note'   => sanitize_text_field( (string) ( $p['note'] ?? '' ) ),
				'at'     => time(),
			);
			update_post_meta( $oid, 'offer_response', wp_json_encode( $resp, JSON_UNESCAPED_UNICODE ) );
			if ( 'accept' === $act ) { update_post_meta( $oid, 'offer_status', 'accepted' ); }
			if ( 'decline' === $act ) { update_post_meta( $oid, 'offer_status', 'declined' ); }
			return array( 'ok' => true, 'response' => $resp );
		},
	) );

	register_rest_route( 'nadlan/v1', '/auction-state/(?P<card>\d+)', array(
		'methods'             => 'GET',
		'permission_callback' => '__return_true',
		'callback'            => function ( WP_REST_Request $req ) {
			$card = absint( $req['card'] );
			if ( ! nadlan_auction_active( $card ) ) { return new WP_Error( 'off', 'off', array( 'status' => 404 ) ); }
			$mode = get_post_meta( $card, 'offers_transparency', true ) ?: 'leading_amount';
			$ids = function_exists( 'nadlan_offers_for_card' ) ? nadlan_offers_for_card( $card, array( 'live', 'accepted', 'declined' ) ) : array();
			$feed = array();
			foreach ( $ids as $oid ) {
				$resp = json_decode( (string) get_post_meta( $oid, 'offer_response', true ), true );
				$feed[] = array(
					'handle'  => (string) get_post_meta( $oid, 'offer_handle', true ),
					'amount'  => 'sealed' === $mode ? 0 : (float) get_post_meta( $oid, 'offer_amount', true ),
					'status'  => (string) get_post_meta( $oid, 'offer_status', true ),
					'response'=> is_array( $resp ) ? array( 'action' => $resp['action'], 'amount' => 'sealed' === $mode ? 0 : (float) $resp['amount'] ) : null,
					'at'      => (int) get_post_meta( $oid, 'offer_created_at', true ),
				);
			}
			usort( $feed, function ( $a, $b ) { return $b['amount'] <=> $a['amount']; } );
			return array(
				'ok' => true, 'mode' => $mode,
				'leading' => 'sealed' === $mode ? 0 : ( function_exists( 'nadlan_offers_leading_amount' ) ? nadlan_offers_leading_amount( $card ) : 0 ),
				'count' => count( $ids ),
				'min' => (float) get_post_meta( $card, 'offers_min', true ),
				'window_end' => (int) get_post_meta( $card, 'offers_window_end', true ),
				'feed' => array_slice( $feed, 0, 12 ),
			);
		},
	) );

	// demo seeder: flips the offers flag on, arms the demo property, seeds 3 labeled offers
	register_rest_route( 'nadlan/v1', '/auction-demo-seed', array(
		'methods'             => 'POST',
		'permission_callback' => function () { return current_user_can( 'manage_options' ); },
		'callback'            => function () {
			update_option( 'nadlan_feature_offers', '1', false );
			$prop = get_page_by_path( 'baka-jlm-garden-4r-demo', OBJECT, 'nadlan_property' );
			if ( ! $prop ) { return new WP_Error( 'no_demo_property', 'no_demo_property', array( 'status' => 404 ) ); }
			$card = $prop->ID;
			update_post_meta( $card, 'offers_enabled', '1' );
			update_post_meta( $card, 'offers_min', 2800000 );
			update_post_meta( $card, 'offers_transparency', 'leading_amount' );
			update_post_meta( $card, 'offers_window_end', time() + 14 * DAY_IN_SECONDS );
			$existing = function_exists( 'nadlan_offers_for_card' ) ? nadlan_offers_for_card( $card, array( 'live', 'accepted', 'declined' ) ) : array();
			if ( count( $existing ) >= 3 ) { return array( 'ok' => true, 'card' => $card, 'existed' => true ); }
			$rows = array(
				array( 'amount' => 2850000, 'name' => 'קונה א (נתוני דוגמה)', 'fin' => 'preapproved', 'resp' => null ),
				array( 'amount' => 2920000, 'name' => 'קונה ב (נתוני דוגמה)', 'fin' => 'cash', 'resp' => array( 'action' => 'counter', 'amount' => 3050000, 'note' => 'נתוני דוגמה', 'at' => time() - DAY_IN_SECONDS ) ),
				array( 'amount' => 2760000, 'name' => 'קונה ג (נתוני דוגמה)', 'fin' => 'pending', 'resp' => array( 'action' => 'decline', 'amount' => 0, 'note' => 'נתוני דוגמה', 'at' => time() - 2 * DAY_IN_SECONDS ) ),
			);
			$n = count( $existing );
			foreach ( $rows as $r ) {
				$n++;
				$oid = wp_insert_post( array( 'post_type' => 'nadlan_offer', 'post_status' => 'private', 'post_title' => 'הצעה #' . $n . ' לנכס ' . $card . ' (דוגמה)' ) );
				if ( is_wp_error( $oid ) ) { continue; }
				update_post_meta( $oid, 'offer_card_id', $card );
				update_post_meta( $oid, 'offer_amount', $r['amount'] );
				update_post_meta( $oid, 'offer_name', $r['name'] );
				update_post_meta( $oid, 'offer_phone', '0500000000' );
				update_post_meta( $oid, 'offer_financing', $r['fin'] );
				update_post_meta( $oid, 'offer_handle', 'מציע #' . $n );
				update_post_meta( $oid, 'offer_status', $r['resp'] && 'decline' === $r['resp']['action'] ? 'declined' : 'live' );
				update_post_meta( $oid, 'offer_created_at', time() - $n * 3600 );
				if ( $r['resp'] ) { update_post_meta( $oid, 'offer_response', wp_json_encode( $r['resp'], JSON_UNESCAPED_UNICODE ) ); }
			}
			return array( 'ok' => true, 'card' => $card, 'url' => get_permalink( $card ) );
		},
	) );
} );

/* ---------- the auction band on single properties ---------- */
add_filter( 'the_content', function ( $content ) {
	if ( ! is_singular( 'nadlan_property' ) || ! in_the_loop() || ! is_main_query() ) { return $content; }
	$card = get_the_ID();
	if ( ! nadlan_auction_active( $card ) ) { return $content; }
	static $done = false;
	if ( $done ) { return $content; }
	$done = true;
	$is_seller = is_user_logged_in() && ( current_user_can( 'manage_options' ) || get_current_user_id() === (int) get_post_meta( $card, 'owner_user_id', true ) );
	ob_start();
	?>
<section id="nlauc" class="nlauc" dir="rtl"
	data-card="<?php echo esc_attr( $card ); ?>"
	data-rest="<?php echo esc_url( rest_url( 'nadlan/v1' ) ); ?>"
	data-seller="<?php echo $is_seller ? '1' : '0'; ?>"
	data-nonce="<?php echo esc_attr( is_user_logged_in() ? wp_create_nonce( 'wp_rest' ) : '' ); ?>">
	<style>
	.nlauc{background:#14130F;border-radius:22px;padding:30px 26px;margin:34px 0;font-family:Heebo,sans-serif;color:#FAF7F1}
	.nlauc-kicker{font:700 12.5px Heebo;letter-spacing:.08em;color:#E9D9A8;text-transform:uppercase;margin:0 0 8px}
	.nlauc h2{font-family:"Frank Ruhl Libre",Georgia,serif;color:#FAF7F1;font-size:1.45rem;margin:0 0 4px}
	.nlauc-sub{font:400 13.5px/1.65 Heebo;color:#CDC5B4;margin:0 0 18px;max-width:560px}
	.nlauc-top{display:flex;gap:14px;flex-wrap:wrap;margin:0 0 18px}
	.nlauc-stat{background:#1E1C15;border:1px solid #3A342A;border-radius:14px;padding:14px 20px;min-width:140px}
	.nlauc-stat i{display:block;font:600 11.5px Heebo;color:#A79E8D;font-style:normal;margin-bottom:4px}
	.nlauc-stat b{font:800 20px "Frank Ruhl Libre",serif;color:#E9D9A8}
	.nlauc-feed{margin:0 0 18px}
	.nlauc-feed h3{font:700 13px Heebo;color:#CDC5B4;margin:0 0 8px}
	.nlauc-row{display:flex;gap:12px;align-items:center;background:#1E1C15;border:1px solid #2A251B;border-radius:10px;padding:10px 14px;margin-bottom:6px;font:400 13px Heebo;color:#E9E2D2}
	.nlauc-row b{color:#E9D9A8}
	.nlauc-tag{border-radius:999px;padding:4px 10px;font:700 10.5px Heebo;margin-inline-start:auto}
	.nlauc-tag.accept{background:#517048;color:#FAF7F1}.nlauc-tag.counter{background:#9C7A3C;color:#14130F}
	.nlauc-tag.decline{background:#3A342A;color:#A79E8D}.nlauc-tag.live{background:#2A251B;color:#CDC5B4}
	.nlauc-form{background:#FAF7F1;border-radius:16px;padding:20px;color:#1B1A17;max-width:560px}
	.nlauc-form h3{font-family:"Frank Ruhl Libre",serif;margin:0 0 12px;font-size:1.1rem}
	.nlauc-form input{width:100%;box-sizing:border-box;background:#fff;border:1px solid #E2DCD0;border-radius:10px;padding:12px;font:400 14.5px Heebo;margin:0 0 10px}
	.nlauc-fin{display:flex;gap:8px;flex-wrap:wrap;margin:0 0 10px}
	.nlauc-fin button{border:1px solid #E2DCD0;background:#fff;border-radius:999px;padding:8px 14px;font:600 12.5px Heebo;color:#51483A;cursor:pointer}
	.nlauc-fin button.is-on{background:#1B1A17;color:#FAF7F1;border-color:#1B1A17}
	.nlauc-ack{font:400 12.5px/1.5 Heebo;color:#51483A;display:flex;gap:8px;align-items:flex-start;margin:0 0 12px}
	.nlauc-go{background:#C2563A;color:#FAF7F1;border:0;border-radius:12px;padding:13px 28px;font:700 15px Heebo;cursor:pointer;box-shadow:0 14px 30px -14px rgba(194,86,58,.55)}
	.nlauc-go[disabled]{opacity:.6}
	.nlauc-msg{font:600 13px Heebo;margin:10px 0 0;display:none}
	.nlauc-honest{font:400 11.5px/1.7 Heebo;color:#A79E8D;margin:16px 0 0;max-width:640px}
	.nlauc-sell{background:#1E1C15;border:1px solid #3A342A;border-radius:14px;padding:16px;margin-top:16px}
	.nlauc-sell h3{font:700 13px Heebo;color:#E9D9A8;margin:0 0 10px}
	.nlauc-sell .act{border:1px solid #3A342A;background:#14130F;color:#CDC5B4;border-radius:8px;padding:6px 12px;font:600 12px Heebo;cursor:pointer;margin-inline-start:6px}
	</style>
	<p class="nlauc-kicker">מכירה בהצעות · לא מחייב</p>
	<h2>הנכס פתוח להצעות מחיר</h2>
	<p class="nlauc-sub">מגישים הצעה, המוכר רואה ומגיב - מקבל, מציע נגדי או מסרב. שקוף, פשוט, ובלי שום התחייבות משפטית משני הצדדים.</p>
	<div class="nlauc-top" id="nlauc-stats"></div>
	<div class="nlauc-feed" id="nlauc-feed"></div>
	<div class="nlauc-form" id="nlauc-form">
		<h3>הגשת הצעה</h3>
		<input type="number" name="amount" placeholder="סכום ההצעה בשקלים" min="0">
		<input type="text" name="name" placeholder="שם מלא">
		<input type="tel" name="phone" placeholder="טלפון">
		<input type="text" name="company" tabindex="-1" autocomplete="off" style="position:absolute;left:-9999px;width:1px;height:1px;opacity:0">
		<div class="nlauc-fin" data-v="pending">
			<button type="button" data-f="cash">מזומן</button>
			<button type="button" data-f="preapproved">אישור עקרוני למשכנתא</button>
			<button type="button" data-f="pending">עוד לא בדקתי מימון</button>
		</div>
		<label class="nlauc-ack"><input type="checkbox" id="nlauc-ack"> אני מבין/ה שההצעה אינה מחייבת, אינה מכרז על פי דין, והמוכר רשאי לבחור כל הצעה או לא לבחור כלל.</label>
		<button type="button" class="nlauc-go" id="nlauc-go">הגשת הצעה</button>
		<p class="nlauc-msg" id="nlauc-msg"></p>
	</div>
	<div class="nlauc-sell" id="nlauc-sell" hidden></div>
	<p class="nlauc-honest">ההצעות נאספות ככלי היכרות בין מוכר לקונים ואינן מהוות התחייבות, מכרז או הזמנה להציע הצעות במובן המשפטי. פרטי המציעים מוצגים למוכר בלבד; בעמוד מוצג כינוי אנונימי.</p>
</section>
<script>
(function(){
	var el=document.getElementById("nlauc");if(!el)return;
	var REST=el.dataset.rest,CARD=el.dataset.card,SELLER=el.dataset.seller==="1",NONCE=el.dataset.nonce;
	var fmt=function(n){return "₪"+Number(n).toLocaleString()};
	function load(){
		fetch(REST+"/auction-state/"+CARD).then(function(r){return r.json()}).then(function(d){
			if(!d||!d.ok)return;
			var st=document.getElementById("nlauc-stats");
			var days=d.window_end?Math.max(0,Math.ceil((d.window_end*1000-Date.now())/86400000)):0;
			st.innerHTML='<div class="nlauc-stat"><i>ההצעה המובילה</i><b>'+(d.leading?fmt(d.leading):(d.mode==="sealed"?"חסוי":"אין עדיין"))+"</b></div>"
				+'<div class="nlauc-stat"><i>הצעות עד כה</i><b>'+d.count+"</b></div>"
				+(d.min?'<div class="nlauc-stat"><i>סף מינימום</i><b>'+fmt(d.min)+"</b></div>":"")
				+(days?'<div class="nlauc-stat"><i>נותרו</i><b>'+days+" ימים</b></div>":"");
			var fd=document.getElementById("nlauc-feed");
			if(d.feed&&d.feed.length){
				fd.innerHTML="<h3>תנועת ההצעות</h3>"+d.feed.map(function(f){
					var t=f.response?f.response.action:(f.status==="accepted"?"accept":"live");
					var lbl={accept:"התקבלה",counter:"הצעה נגדית"+(f.response&&f.response.amount?" "+fmt(f.response.amount):""),decline:"נדחתה",live:"ממתינה"}[t]||"ממתינה";
					return '<div class="nlauc-row"><span>'+f.handle+"</span>"+(f.amount?"<b>"+fmt(f.amount)+"</b>":"")+'<span class="nlauc-tag '+t+'">'+lbl+"</span></div>";
				}).join("");
			}else{fd.innerHTML="";}
			if(SELLER){loadSeller();}
		});
	}
	function loadSeller(){
		var box=document.getElementById("nlauc-sell");box.hidden=false;
		box.innerHTML="<h3>אזור המוכר: תגובה להצעות</h3><p style='font:400 12px Heebo;color:#A79E8D;margin:0 0 8px'>הפרטים המלאים של המציעים מופיעים בניהול ההצעות. כאן מגיבים בקליק.</p>";
		fetch(REST+"/auction-state/"+CARD).then(function(r){return r.json()}).then(function(d){
			(d.feed||[]).forEach(function(f,i){
				var row=document.createElement("div");row.className="nlauc-row";
				row.innerHTML="<span>"+f.handle+"</span><b>"+(f.amount?fmt(f.amount):"")+"</b>"
					+'<span style="margin-inline-start:auto"><button class="act" data-a="accept">קבלה</button><button class="act" data-a="counter">נגדית</button><button class="act" data-a="decline">דחייה</button></span>';
				row.dataset.handle=f.handle;
				box.appendChild(row);
			});
			box.addEventListener("click",function(e){
				var b=e.target.closest(".act");if(!b)return;
				var handle=b.closest(".nlauc-row").dataset.handle;
				var body={action:b.dataset.a,handle:handle,card:parseInt(CARD,10)};
				if(b.dataset.a==="counter"){var amt=prompt("סכום ההצעה הנגדית בשקלים:");if(!amt)return;body.amount=parseFloat(amt);}
				fetch(REST+"/offer-respond-by-handle",{method:"POST",headers:{"Content-Type":"application/json","X-WP-Nonce":NONCE},body:JSON.stringify(body)})
					.then(function(r){if(r.ok){load();}else{alert("לא הצליח - נסו מהניהול");}});
			},{once:true});
		});
	}
	var fin=el.querySelector(".nlauc-fin");
	fin.querySelectorAll("button").forEach(function(b){b.addEventListener("click",function(){
		fin.querySelectorAll("button").forEach(function(x){x.classList.remove("is-on")});b.classList.add("is-on");fin.dataset.v=b.dataset.f;})});
	document.getElementById("nlauc-go").addEventListener("click",function(){
		var go=this,msg=document.getElementById("nlauc-msg");
		var f=document.getElementById("nlauc-form");
		var amount=parseFloat(f.querySelector("[name=amount]").value||"0");
		var name=f.querySelector("[name=name]").value.trim();
		var phone=f.querySelector("[name=phone]").value.trim();
		if(!document.getElementById("nlauc-ack").checked){msg.textContent="יש לאשר שההצעה אינה מחייבת.";msg.style.color="#C2563A";msg.style.display="block";return}
		go.disabled=true;msg.style.display="none";
		fetch(REST+"/offers",{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify({
			card_id:parseInt(CARD,10),amount:amount,name:name,phone:phone,financing:fin.dataset.v,nonbinding_ack:1,company:f.querySelector("[name=company]").value})})
		.then(function(r){return r.json().then(function(j){return{ok:r.ok,j:j}})})
		.then(function(res){
			go.disabled=false;
			if(res.ok&&res.j.ok){msg.textContent="ההצעה נקלטה! המוכר יראה אותה ויגיב כאן.";msg.style.color="#517048";msg.style.display="block";load();}
			else{msg.textContent=(res.j&&res.j.message)||"משהו השתבש.";msg.style.color="#C2563A";msg.style.display="block";}
		});
	});
	load();
})();
</script>
	<?php
	return ob_get_clean() . $content;
}, 24 );

/* seller respond by handle (the front panel cannot know offer post ids) */
add_action( 'rest_api_init', function () {
	register_rest_route( 'nadlan/v1', '/offer-respond-by-handle', array(
		'methods'             => 'POST',
		'permission_callback' => function () { return is_user_logged_in(); },
		'callback'            => function ( WP_REST_Request $req ) {
			$p = $req->get_json_params() ?: array();
			$card = absint( $p['card'] ?? 0 );
			$handle = sanitize_text_field( (string) ( $p['handle'] ?? '' ) );
			$owner = (int) get_post_meta( $card, 'owner_user_id', true );
			if ( ! current_user_can( 'manage_options' ) && get_current_user_id() !== $owner ) {
				return new WP_Error( 'forbidden', 'forbidden', array( 'status' => 401 ) );
			}
			$ids = function_exists( 'nadlan_offers_for_card' ) ? nadlan_offers_for_card( $card, array( 'live', 'accepted', 'declined' ) ) : array();
			foreach ( $ids as $oid ) {
				if ( (string) get_post_meta( $oid, 'offer_handle', true ) === $handle ) {
					$inner = new WP_REST_Request( 'POST', '/nadlan/v1/offer-respond' );
					$inner->set_body( wp_json_encode( array( 'offer' => $oid, 'action' => $p['action'] ?? '', 'amount' => $p['amount'] ?? 0 ) ) );
					$inner->set_header( 'Content-Type', 'application/json' );
					return rest_do_request( $inner );
				}
			}
			return new WP_Error( 'not_found', 'not_found', array( 'status' => 404 ) );
		},
	) );
} );

/* ---------- metabox on nadlan_property ---------- */
add_action( 'add_meta_boxes', function () {
	add_meta_box( 'nadlan_auction_panel', 'מכירה בהצעות (Auction)', function ( $post ) {
		wp_nonce_field( 'nadlan_auction_mb', 'nadlan_auction_mb_nonce' );
		$on = get_post_meta( $post->ID, 'offers_enabled', true ) === '1';
		$min = (string) get_post_meta( $post->ID, 'offers_min', true );
		$tr = (string) get_post_meta( $post->ID, 'offers_transparency', true );
		?>
		<div dir="rtl">
			<p><label><input type="checkbox" name="nl_auc_on" value="1" <?php checked( $on ); ?>> <b>הנכס פתוח להצעות מחיר</b></label></p>
			<p><label>סף מינימום (₪) <input type="number" name="nl_auc_min" value="<?php echo esc_attr( $min ); ?>" style="width:140px"></label></p>
			<p><label>שקיפות <select name="nl_auc_tr">
				<option value="leading_amount" <?php selected( $tr, 'leading_amount' ); ?>>מציגים את ההצעה המובילה</option>
				<option value="sealed" <?php selected( $tr, 'sealed' ); ?>>חסוי (רק שיש הצעות)</option>
			</select></label></p>
			<p style="color:#666;font-size:12px">חלון ההצעות מתארך אוטומטית עם כל הצעה חדשה. תגובות (קבלה/נגדית/דחייה) - מעמוד הנכס כשאתם מחוברים, או מרשימת ההצעות.</p>
		</div>
		<?php
	}, 'nadlan_property', 'side' );
} );
add_action( 'save_post_nadlan_property', function ( $post_id ) {
	if ( ! isset( $_POST['nadlan_auction_mb_nonce'] )
		|| ! wp_verify_nonce( sanitize_text_field( wp_unslash( $_POST['nadlan_auction_mb_nonce'] ) ), 'nadlan_auction_mb' ) ) { return; }
	if ( defined( 'DOING_AUTOSAVE' ) && DOING_AUTOSAVE ) { return; }
	if ( ! current_user_can( 'edit_post', $post_id ) ) { return; }
	update_post_meta( $post_id, 'offers_enabled', ! empty( $_POST['nl_auc_on'] ) ? '1' : '0' );
	update_post_meta( $post_id, 'offers_min', isset( $_POST['nl_auc_min'] ) ? absint( $_POST['nl_auc_min'] ) : 0 );
	$tr = isset( $_POST['nl_auc_tr'] ) ? sanitize_key( wp_unslash( $_POST['nl_auc_tr'] ) ) : 'leading_amount';
	update_post_meta( $post_id, 'offers_transparency', in_array( $tr, array( 'leading_amount', 'sealed' ), true ) ? $tr : 'leading_amount' );
} );

/* ---------- /sell-by-auction/ landing ---------- */
add_action( 'init', function () {
	add_rewrite_rule( '^sell-by-auction/?$', 'index.php?nadlan_sell_auction=1', 'top' );
	if ( get_option( 'nadlan_sell_auction_rewrite_v1' ) !== '1' ) {
		flush_rewrite_rules( false );
		update_option( 'nadlan_sell_auction_rewrite_v1', '1' );
	}
} );
add_filter( 'query_vars', function ( $v ) { $v[] = 'nadlan_sell_auction'; return $v; } );

add_action( 'template_redirect', function () {
	if ( ! get_query_var( 'nadlan_sell_auction' ) ) { return; }
	$title = 'מכירת דירה בשיטת ההצעות: הקונים מציעים, אתם בוחרים | נדלן';
	$desc  = 'שמים את הדירה על הבמה עם מודל תלת ממדי, קונים מגישים הצעות מחיר לא מחייבות, ואתם רואים בזמן אמת מה השוק באמת מוכן לשלם - ומגיבים. חינם, שקוף, בלי בלעדיות.';
	add_filter( 'pre_get_document_title', function () use ( $title ) { return $title; }, 99 );
	add_action( 'wp_head', function () use ( $desc ) {
		$self = home_url( '/sell-by-auction/' );
		echo '<meta name="description" content="' . esc_attr( $desc ) . '">' . "\n";
		echo '<link rel="canonical" href="' . esc_url( $self ) . '">' . "\n";
	}, 4 );
	$demo = get_page_by_path( 'baka-jlm-garden-4r-demo', OBJECT, 'nadlan_property' );
	get_header();
	?>
<div class="nlsba" dir="rtl">
	<style>
	.nlsba{max-width:980px;margin:0 auto;padding:26px 16px 70px;font-family:Heebo,sans-serif;color:#1B1A17}
	.nlsba h1,.nlsba h2{font-family:"Frank Ruhl Libre",Georgia,serif}
	.nlsba-hero{text-align:center;padding:26px 0 10px}
	.nlsba-kicker{font:700 12.5px Heebo;letter-spacing:.06em;color:#9C7A3C;text-transform:uppercase;margin:0 0 10px}
	.nlsba-hero h1{font-size:clamp(1.6rem,3.6vw,2.35rem);margin:0 0 12px;line-height:1.3}
	.nlsba-hero .sub{color:#51483A;font:400 15px/1.75 Heebo;max-width:640px;margin:0 auto 8px}
	.nlsba-steps{display:grid;grid-template-columns:repeat(3,1fr);gap:14px;margin:26px 0}
	@media(max-width:760px){.nlsba-steps{grid-template-columns:1fr}}
	.nlsba-step{background:#fff;border:1px solid #E2DCD0;border-radius:16px;padding:20px;text-align:start}
	.nlsba-step i{display:block;width:36px;height:36px;border-radius:50%;background:#9C7A3C;color:#FAF7F1;font:700 16px/36px "Frank Ruhl Libre",serif;font-style:normal;text-align:center;margin-bottom:10px}
	.nlsba-step b{display:block;font-family:"Frank Ruhl Libre",serif;margin-bottom:5px;font-size:1.05rem}
	.nlsba-step p{font:400 13px/1.65 Heebo;color:#51483A;margin:0}
	.nlsba-demo{text-align:center;background:#F3EEE3;border:1px solid #E2DCD0;border-radius:18px;padding:20px;margin:0 0 10px}
	.nlsba-demo a{display:inline-block;border:1.5px solid #9C7A3C;color:#9C7A3C;border-radius:12px;padding:12px 24px;font:700 14px Heebo;text-decoration:none;margin-top:8px}
	.nlsba-honest{font:400 12.5px/1.75 Heebo;color:#8E877A;max-width:680px;margin:26px auto 0;text-align:center}
	</style>
	<header class="nlsba-hero">
		<p class="nlsba-kicker">מכירה בהצעות · חינם</p>
		<h1>הדירה שלכם על הבמה. הקונים מציעים. אתם בוחרים.</h1>
		<p class="sub">השוק קשה ודירות מחכות חודשים? במקום לנחש מחיר, תנו לקונים להגיד כמה הם באמת מוכנים לשלם: הדירה מוצגת עם מודל תלת ממדי, סביבה ונתונים, ההצעות נאספות בשקיפות, ואתם מגיבים - מקבלים, מציעים נגדית או מסרבים.</p>
	</header>
	<div class="nlsba-steps">
		<div class="nlsba-step"><i>1</i><b>מספרים לנו על הדירה</b><p>הטופס הקצר למטה - שמונה שאלות. אנחנו בונים לדירה עמוד עם תלת ממד, מפה וכל הנתונים.</p></div>
		<div class="nlsba-step"><i>2</i><b>קונים מגישים הצעות</b><p>כל קונה רואה את הדירה מבפנים, את הסביבה ואת ההצעה המובילה - ומגיש הצעה לא מחייבת עם פרטי המימון שלו.</p></div>
		<div class="nlsba-step"><i>3</i><b>אתם מגיבים ובוחרים</b><p>קבלה, הצעה נגדית או דחייה - בקליק. בלי בלעדיות, בלי עמלה, ובלי שום מחויבות משפטית עד שתחליטו.</p></div>
	</div>
	<?php if ( $demo && nadlan_auction_active( $demo->ID ) ) : ?>
	<div class="nlsba-demo">
		<b style="font-family:'Frank Ruhl Libre',serif;font-size:1.1rem">רוצים לראות איך זה נראה לקונים?</b><br>
		<span style="font:400 13px Heebo;color:#51483A">דירת הדוגמה שלנו פתוחה להצעות עכשיו (נתוני דוגמה)</span><br>
		<a href="<?php echo esc_url( get_permalink( $demo ) ); ?>">לצפייה בדירה החיה עם ההצעות ←</a>
	</div>
	<?php endif; ?>
	<?php echo nadlan_sf_render( 'auction' ); // phpcs:ignore ?>
	<p class="nlsba-honest">איסוף ההצעות הוא כלי היכרות בין מוכר לקונים: ההצעות אינן מחייבות, התהליך אינו מכרז על פי דין, ואין באמור ייעוץ משפטי. פרטי המציעים מוצגים למוכר בלבד. במקרים המחייבים הליך מכר מוסדר (כינוס נכסים, הוצאה לפועל) יש לפעול לפי הוראות הדין ובליווי עורך דין.</p>
</div>
	<?php
	get_footer();
	exit;
} );

/* ---------- healthcheck ---------- */
add_filter( 'nadlan_config_healthcheck', function ( $out ) {
	$out['auction'] = array(
		'offers_flag' => get_option( 'nadlan_feature_offers', '0' ) === '1',
		'landing'     => home_url( '/sell-by-auction/' ),
	);
	return $out;
} );
