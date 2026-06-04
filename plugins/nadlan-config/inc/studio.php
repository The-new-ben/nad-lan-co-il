<?php
/**
 * nadlan-config — Advertiser STUDIO frontend (v1.41.0)
 *
 * One self-serve URL — /studio/?id=<post_id> — that an advertiser opens to
 * fully manage their published card with NO admin/wp-login knowledge:
 *   • drag-and-drop image upload (or click), gallery reorder/delete
 *   • inline edit: title, description (with AI "improve this" assist),
 *     city/address, phone/email/website, social links (FB/IG/TT/YT),
 *     video URL embed (YouTube/Vimeo)
 *   • Leaflet + OpenStreetMap map picker (zero cost, no Google key)
 *   • Type-specific fields (project: units/status/יזם; pro: classification;
 *     property: price/rooms/sqm)
 *   • One-click "preview live page"
 *   • Tooltips on every field — explanations so a non-techie understands
 *
 * The page is intercepted at `/studio/` via template_redirect. Auth is mandatory:
 * caller must be logged in AND own the card (or be admin) — enforced by REST.
 *
 * 4-year-old friendly: empty-states say what to do; success toasts on every
 * action; nothing is hidden behind jargon; every input has a "?" tooltip.
 */
if ( ! defined( 'ABSPATH' ) ) { exit; }

/* Rewrite — /studio/ serves the editor */
add_action( 'init', function () {
	add_rewrite_rule( '^studio/?$', 'index.php?nadlan_studio=1', 'top' );
} );
add_filter( 'query_vars', function ( $v ) { $v[] = 'nadlan_studio'; return $v; } );

/* Flush rewrite once on update */
add_action( 'init', function () {
	if ( get_option( 'nadlan_studio_rewrite_v1' ) !== '1' ) {
		flush_rewrite_rules( false );
		update_option( 'nadlan_studio_rewrite_v1', '1' );
	}
}, 99 );

add_action( 'template_redirect', function () {
	if ( ! get_query_var( 'nadlan_studio' ) ) { return; }
	$id = isset( $_GET['id'] ) ? (int) $_GET['id'] : 0;

	if ( ! is_user_logged_in() ) {
		wp_safe_redirect( wp_login_url( add_query_arg( 'id', $id, home_url( '/studio/' ) ) ) );
		exit;
	}
	if ( $id <= 0 ) {
		nadlan_studio_render_picker();
		exit;
	}
	if ( ! function_exists( 'nadlan_studio_can_edit' ) || ! nadlan_studio_can_edit( $id ) ) {
		status_header( 403 );
		nadlan_studio_render_denied();
		exit;
	}
	nadlan_studio_render_editor( $id );
	exit;
}, 5 );

/* ---------- helpers ---------- */
if ( ! function_exists( 'nadlan_studio_label' ) ) {
	function nadlan_studio_label( $k ) {
		$m = array(
			'title' => 'שם',
			'tagline' => 'משפט מפתח',
			'description' => 'תיאור',
			'city' => 'עיר', 'address' => 'כתובת',
			'phone' => 'טלפון', 'email' => 'אימייל', 'website' => 'אתר',
			'lat' => 'קו רוחב', 'lng' => 'קו אורך',
			'social_facebook' => 'Facebook', 'social_instagram' => 'Instagram',
			'social_tiktok' => 'TikTok', 'social_youtube' => 'YouTube', 'video_url' => 'וידאו',
			'classification' => 'התמחות',
			'years_active' => 'שנות ותק',
			'service_area' => 'אזורי שירות',
			'project_type' => 'סוג פרויקט', 'project_status' => 'שלב',
			'developer_name' => 'יזם', 'num_units' => 'יחידות דיור',
			'start_year' => 'שנת התחלה',
			'listing_type' => 'סוג עסקה', 'property_type' => 'סוג נכס',
			'price' => 'מחיר (₪)', 'rooms' => 'חדרים', 'floor' => 'קומה',
			'size_sqm' => 'גודל (מ״ר)', 'parking' => 'חניה', 'elevator' => 'מעלית',
		);
		return $m[ $k ] ?? $k;
	}
}
if ( ! function_exists( 'nadlan_studio_hint' ) ) {
	function nadlan_studio_hint( $k ) {
		$m = array(
			'tagline' => 'משפט אחד שיכול להופיע כותרת בכרטיס. למשל "הקבלן של בעלי הבית".',
			'description' => 'הסיפור שלכם. למה כדאי לפנות אליכם? מה מיוחד? אפשר לבקש מהעוזר החכם לשפר.',
			'city' => 'בה אתם פועלים. משפיע על דירוג בחיפושים מקומיים.',
			'address' => 'אופציונלי. לקוחות פוטנציאליים אוהבים להבין איפה אתם.',
			'phone' => 'הטלפון שיופיע ככפתור התקשרות לציבור.',
			'email' => 'אימייל פנייה. לא יופיע כברירת מחדל; רק אם תאשרו.',
			'website' => 'הקישור לאתר שלכם, אם יש.',
			'social_facebook' => 'הקישור המלא לדף הפייסבוק.',
			'social_instagram' => 'הקישור המלא לפרופיל אינסטגרם.',
			'social_tiktok' => 'הקישור המלא ל-TikTok.',
			'social_youtube' => 'קישור לערוץ או לסרטון.',
			'video_url' => 'קישור YouTube או Vimeo. נשתבץ אצלכם כסרטון.',
			'classification' => 'תחום ההתמחות הראשי. למשל "בנייה רוויה, סיווג 1".',
			'service_area' => 'באילו ערים/אזורים אתם נותנים שירות.',
			'project_type' => 'תמ״א 38, פינוי בינוי, בנייה חדשה...',
			'project_status' => 'באיזה שלב הפרויקט (תכנון, היתר, ביצוע, אכלוס).',
			'developer_name' => 'מי היזם של הפרויקט.',
			'num_units' => 'כמה יחידות דיור בפרויקט.',
			'price' => 'המחיר המבוקש. ירשם בכל הפורמטים.',
			'rooms' => 'מספר חדרים. אפשר 3.5, 4.5 וכו׳.',
			'lat' => 'נקודת המפה. הזזת הסיכה במפה תעדכן אוטומטית.',
		);
		return $m[ $k ] ?? '';
	}
}

/* ---------- denied / picker pages ---------- */
if ( ! function_exists( 'nadlan_studio_render_denied' ) ) {
	function nadlan_studio_render_denied() {
		get_header();
		?>
		<div class="nlst" dir="rtl" style="max-width:640px;margin:60px auto;padding:0 20px;text-align:center;font-family:var(--font-sans,Heebo,sans-serif)">
			<div style="font-size:48px;margin-bottom:14px">🔒</div>
			<h1 style="font-family:var(--font-serif,'Frank Ruhl Libre',serif)">אין הרשאה</h1>
			<p>הכרטיס הזה אינו שייך לך. כדי לערוך כרטיס, יש לבקש בעלות עליו תחילה.</p>
			<p><a class="nlst-link" href="<?php echo esc_url( home_url( '/professionals/' ) ); ?>">חיפוש הכרטיס שלך במאגר ←</a></p>
		</div>
		<?php
		get_footer();
	}
}

if ( ! function_exists( 'nadlan_studio_render_picker' ) ) {
	function nadlan_studio_render_picker() {
		get_header();
		?>
		<div class="nlst" dir="rtl" style="max-width:880px;margin:40px auto;padding:0 20px;font-family:var(--font-sans,Heebo,sans-serif)">
			<div style="text-align:center;margin-bottom:30px">
				<div style="font-size:42px">🎨</div>
				<h1 style="font-family:var(--font-serif,serif)">סטודיו פרסום</h1>
				<p style="color:#5a5a5a">העריכה הכי קלה של כרטיס נדל״ן. בלי קוד, בלי כאב ראש.</p>
			</div>
			<div id="nlst-my-cards" data-rest="<?php echo esc_url( rest_url( 'nadlan/v1/studio/mine' ) ); ?>">טוען…</div>
			<script>
				(function(){
					var el=document.getElementById('nlst-my-cards');
					fetch(el.dataset.rest,{credentials:'include',headers:{'X-WP-Nonce':'<?php echo esc_js( wp_create_nonce( 'wp_rest' ) ); ?>'}})
						.then(function(r){return r.json();})
						.then(function(d){
							if(!d||!d.ok||!d.cards||d.cards.length===0){
								el.innerHTML='<div style="text-align:center;padding:40px;background:#FBF9F5;border-radius:14px"><p>עדיין אין כרטיס מזוהה עליך. <a href="<?php echo esc_js( home_url( '/professionals/' ) ); ?>">חפש את הכרטיס שלך</a> ובקש בעלות.</p></div>';
								return;
							}
							var html='<div style="display:grid;grid-template-columns:repeat(auto-fill,minmax(260px,1fr));gap:14px">';
							d.cards.forEach(function(c){
								var photoHint=c.photos_count===0?'<span style="color:#DC2626">⚠ אין תמונות</span>':'<span style="color:#059669">'+c.photos_count+' תמונות</span>';
								html+='<a href="/studio/?id='+c.id+'" style="background:#fff;border:1px solid #ddd;border-radius:12px;padding:18px;text-decoration:none;color:inherit;display:block;transition:transform .15s,box-shadow .15s">'
									+'<div style="font-family:var(--font-serif,serif);font-size:18px;font-weight:600;margin-bottom:6px">'+(c.title||'ללא שם')+'</div>'
									+'<div style="font-size:12.5px;color:#7a7a7a;margin-bottom:10px">'+c.post_type+' · '+c.tier+'</div>'
									+'<div style="font-size:13px;color:#5a5a5a">'+photoHint+' · '+c.views+' צפיות · '+c.reviews+' ביקורות</div>'
									+'<div style="margin-top:12px;color:#9C7A3C;font-weight:600;font-size:13.5px">ערוך כרטיס ←</div>'
									+'</a>';
							});
							html+='</div>';
							el.innerHTML=html;
						})
						.catch(function(){el.innerHTML='<p style="color:#B91C1C">שגיאה בטעינה.</p>';});
				})();
			</script>
		</div>
		<?php
		get_footer();
	}
}

/* ---------- editor ---------- */
if ( ! function_exists( 'nadlan_studio_render_editor' ) ) {
	function nadlan_studio_render_editor( $id ) {
		$post = get_post( $id );
		$nonce = wp_create_nonce( 'wp_rest' );
		$rest_root = esc_url( rest_url( 'nadlan/v1/studio/' . $id ) );
		get_header();
		echo nadlan_studio_css();
		?>
<div class="nlst" dir="rtl" data-id="<?php echo (int) $id; ?>" data-rest="<?php echo $rest_root; ?>" data-nonce="<?php echo esc_attr( $nonce ); ?>" data-pt="<?php echo esc_attr( $post->post_type ); ?>">
	<header class="nlst-bar">
		<h1>סטודיו פרסום: <?php echo esc_html( get_the_title( $post ) ); ?></h1>
		<div class="nlst-bar-actions">
			<a class="nlst-link" href="<?php echo esc_url( get_permalink( $post ) ); ?>" target="_blank" rel="noopener">תצוגה ציבורית ↗</a>
			<button type="button" class="nlst-save" id="nlst-save-btn">שמירה</button>
		</div>
	</header>

	<div class="nlst-status" id="nlst-status" hidden></div>

	<div class="nlst-grid">
		<!-- LEFT: photos + maps + content -->
		<section class="nlst-col">
			<div class="nlst-section">
				<h2>תמונות <span class="nlst-help" title="גררו תמונות לכאן או לחצו לבחור. התמונה הראשונה היא תמונת הקאבר.">?</span></h2>
				<div class="nlst-dropzone" id="nlst-drop">
					<input type="file" id="nlst-file" accept="image/*" multiple hidden>
					<div class="nlst-drop-empty">
						<div class="nlst-drop-icon">📸</div>
						<p><b>גררו תמונות לכאן</b><br>או <button type="button" class="nlst-pick">בחרו תמונות מהמחשב</button></p>
						<small>JPG / PNG / WEBP · עד 10MB לתמונה</small>
					</div>
					<div class="nlst-gallery" id="nlst-gallery"></div>
				</div>
			</div>

			<div class="nlst-section">
				<h2>סיפור העסק <span class="nlst-help" title="הטקסט שיופיע כתיאור הראשי. אפשר לבקש מהעוזר החכם לכתוב או לשפר.">?</span></h2>
				<label class="nlst-label">משפט מפתח (כותרת קצרה)</label>
				<input type="text" id="f-tagline" maxlength="120" placeholder="לדוגמה: 25 שנה של בנייה מדויקת בגוש דן">
				<label class="nlst-label">תיאור מלא</label>
				<textarea id="f-description" rows="6" placeholder="ספרו את הסיפור שלכם, מה מייחד אתכם, אילו פרויקטים סגרתם, מי הלקוחות שלכם."></textarea>
				<div class="nlst-ai-row">
					<button type="button" class="nlst-ai" data-mode="improve">✨ שפר טקסט</button>
					<button type="button" class="nlst-ai" data-mode="shorter">קצר</button>
					<button type="button" class="nlst-ai" data-mode="longer">הרחב</button>
					<button type="button" class="nlst-ai" data-mode="pro">רשמי</button>
					<button type="button" class="nlst-ai" data-mode="friendly">חם ואנושי</button>
				</div>
			</div>

			<div class="nlst-section">
				<h2>מפה <span class="nlst-help" title="הזיזו את הסיכה למיקום המדויק. נשמר אוטומטית.">?</span></h2>
				<div id="nlst-map" style="height:300px;border-radius:12px;background:#FBF9F5"></div>
				<small>גררו את הסיכה לעדכון מיקום מדויק</small>
			</div>

			<?php if ( $post->post_type === 'nadlan_project' ) : ?>
			<div class="nlst-section">
				<h2>פרטי הפרויקט</h2>
				<div class="nlst-row">
					<div><label class="nlst-label">סוג פרויקט</label>
						<select id="f-project_type">
							<option value="">בחרו…</option>
							<option value="tama38">תמ״א 38</option>
							<option value="pinui_binui">פינוי בינוי</option>
							<option value="new_build">בנייה חדשה</option>
							<option value="urban">התחדשות עירונית</option>
						</select></div>
					<div><label class="nlst-label">שלב</label>
						<input type="text" id="f-project_status" placeholder="לדוגמה: בהקמה"></div>
				</div>
				<div class="nlst-row">
					<div><label class="nlst-label">יזם</label><input type="text" id="f-developer_name"></div>
					<div><label class="nlst-label">יחידות דיור</label><input type="number" id="f-num_units" min="0"></div>
				</div>
			</div>
			<?php elseif ( $post->post_type === 'nadlan_professional' ) : ?>
			<div class="nlst-section">
				<h2>פרטי בעל המקצוע</h2>
				<label class="nlst-label">התמחות</label>
				<input type="text" id="f-classification" placeholder="לדוגמה: בנייה רוויה, סיווג 1">
				<div class="nlst-row">
					<div><label class="nlst-label">שנות ותק</label><input type="number" id="f-years_active" min="0"></div>
					<div><label class="nlst-label">אזורי שירות</label><input type="text" id="f-service_area" placeholder="גוש דן, השפלה…"></div>
				</div>
			</div>
			<?php elseif ( $post->post_type === 'nadlan_property' ) : ?>
			<div class="nlst-section">
				<h2>פרטי הנכס</h2>
				<div class="nlst-row">
					<div><label class="nlst-label">סוג עסקה</label>
						<select id="f-listing_type">
							<option value="">בחרו…</option>
							<option value="sale">למכירה</option>
							<option value="rent">להשכרה</option>
						</select></div>
					<div><label class="nlst-label">סוג נכס</label><input type="text" id="f-property_type"></div>
				</div>
				<div class="nlst-row">
					<div><label class="nlst-label">מחיר (₪)</label><input type="number" id="f-price" min="0"></div>
					<div><label class="nlst-label">חדרים</label><input type="number" id="f-rooms" step="0.5" min="0"></div>
				</div>
				<div class="nlst-row">
					<div><label class="nlst-label">גודל (מ״ר)</label><input type="number" id="f-size_sqm" min="0"></div>
					<div><label class="nlst-label">קומה</label><input type="number" id="f-floor"></div>
				</div>
				<div class="nlst-row">
					<div><label class="nlst-label"><input type="checkbox" id="f-parking"> חניה</label></div>
					<div><label class="nlst-label"><input type="checkbox" id="f-elevator"> מעלית</label></div>
				</div>
			</div>
			<?php endif; ?>
		</section>

		<!-- RIGHT: contact + social + video -->
		<aside class="nlst-col">
			<div class="nlst-section">
				<h2>מיקום ויצירת קשר</h2>
				<label class="nlst-label">עיר</label>
				<input type="text" id="f-city">
				<label class="nlst-label">כתובת</label>
				<input type="text" id="f-address" placeholder="רחוב, מספר">
				<label class="nlst-label">טלפון</label>
				<input type="tel" id="f-phone">
				<label class="nlst-label">אימייל</label>
				<input type="email" id="f-email">
				<label class="nlst-label">אתר</label>
				<input type="url" id="f-website" placeholder="https://">
			</div>

			<div class="nlst-section">
				<h2>רשתות חברתיות <span class="nlst-help" title="הקישורים האלה יופיעו כאייקונים בכרטיס הציבורי שלכם.">?</span></h2>
				<label class="nlst-label">📘 Facebook</label>
				<input type="url" id="f-social_facebook" placeholder="https://facebook.com/…">
				<label class="nlst-label">📸 Instagram</label>
				<input type="url" id="f-social_instagram" placeholder="https://instagram.com/…">
				<label class="nlst-label">🎵 TikTok</label>
				<input type="url" id="f-social_tiktok" placeholder="https://tiktok.com/@…">
				<label class="nlst-label">▶ YouTube</label>
				<input type="url" id="f-social_youtube" placeholder="https://youtube.com/@…">
			</div>

			<div class="nlst-section">
				<h2>וידאו <span class="nlst-help" title="הדבק קישור YouTube או Vimeo. נטמיע אצלכם בכרטיס.">?</span></h2>
				<input type="url" id="f-video_url" placeholder="https://youtube.com/watch?v=…">
			</div>

			<input type="hidden" id="f-lat">
			<input type="hidden" id="f-lng">

			<div class="nlst-section nlst-tips">
				<h3>💡 טיפים מהירים</h3>
				<ul>
					<li><b>3 תמונות לפחות.</b> כרטיסים עם 3+ תמונות מקבלים פי 3 פניות.</li>
					<li><b>תיאור של 80+ מילים.</b> נכנס לתוצאות חיפוש של גוגל.</li>
					<li><b>טלפון + אימייל.</b> מאפשר לקוחות לפנות איך שנוח להם.</li>
					<li><b>סרטון.</b> הצופים נשארים פי 2 בכרטיסים עם וידאו.</li>
				</ul>
			</div>
		</aside>
	</div>
</div>

<!-- Leaflet (free, OpenStreetMap) -->
<link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css" crossorigin="">
<script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js" crossorigin=""></script>
<?php echo nadlan_studio_js(); ?>
		<?php
		get_footer();
	}
}

if ( ! function_exists( 'nadlan_studio_css' ) ) {
	function nadlan_studio_css() {
		return <<<'CSS'
<style id="nlst-css">
.nlst{font-family:var(--font-sans,Heebo,system-ui,sans-serif);direction:rtl;max-width:1280px;margin:0 auto;padding:24px 20px 60px;color:#1B1A17}
.nlst-bar{display:flex;align-items:center;justify-content:space-between;gap:14px;flex-wrap:wrap;background:linear-gradient(135deg,#1B1A17,#3a3329);color:#fff;padding:18px 22px;border-radius:14px;margin-bottom:18px}
.nlst-bar h1{margin:0;font-family:var(--font-serif,'Frank Ruhl Libre',serif);font-size:22px;font-weight:600}
.nlst-bar-actions{display:flex;gap:10px;align-items:center}
.nlst-link{color:#F3D9A6;text-decoration:none;font-size:13.5px;font-weight:600}
.nlst-save{background:linear-gradient(135deg,#9C7A3C,#B89254);color:#fff;border:0;border-radius:9px;padding:11px 22px;font:inherit;font-weight:700;cursor:pointer;transition:filter .2s,transform .15s}
.nlst-save:hover{filter:brightness(1.08);transform:translateY(-2px)}
.nlst-save.is-saving{opacity:.6;cursor:wait}
.nlst-status{padding:12px 16px;border-radius:10px;margin-bottom:14px;font-weight:600}
.nlst-status.is-ok{background:#ECFDF5;color:#059669;border:1px solid #6EE7B7}
.nlst-status.is-err{background:#FEF2F2;color:#B91C1C;border:1px solid #FECACA}
.nlst-grid{display:grid;grid-template-columns:1.4fr 1fr;gap:18px}
@media(max-width:900px){.nlst-grid{grid-template-columns:1fr}}
.nlst-col{display:flex;flex-direction:column;gap:18px}
.nlst-section{background:#fff;border:1px solid rgba(27,26,23,.1);border-radius:14px;padding:20px}
.nlst-section h2{font-family:var(--font-serif,serif);font-size:17px;font-weight:600;margin:0 0 12px;color:#1B1A17;display:flex;align-items:center;gap:8px}
.nlst-section h3{font-size:14px;margin:0 0 8px}
.nlst-help{display:inline-grid;place-items:center;width:18px;height:18px;border-radius:50%;background:#FBF9F5;border:1px solid rgba(156,122,60,.4);color:#9C7A3C;font-size:11px;font-weight:700;cursor:help}
.nlst-label{display:block;font-size:12.5px;color:#7a7a7a;margin:10px 0 5px;font-weight:600}
.nlst-section input[type=text],.nlst-section input[type=tel],.nlst-section input[type=email],.nlst-section input[type=url],.nlst-section input[type=number],.nlst-section select,.nlst-section textarea{width:100%;padding:11px 13px;border:1px solid rgba(27,26,23,.16);border-radius:9px;font:inherit;font-size:14px;background:#fff;box-sizing:border-box}
.nlst-section textarea{resize:vertical;min-height:120px}
.nlst-row{display:grid;grid-template-columns:1fr 1fr;gap:12px}
.nlst-ai-row{display:flex;gap:6px;flex-wrap:wrap;margin-top:10px}
.nlst-ai{background:#FBF9F5;color:#9C7A3C;border:1px solid rgba(156,122,60,.35);border-radius:18px;padding:7px 14px;font:inherit;font-size:12.5px;font-weight:600;cursor:pointer;transition:background .15s,color .15s}
.nlst-ai:hover{background:#9C7A3C;color:#fff}
.nlst-ai:disabled{opacity:.55;cursor:wait}
/* drop zone */
.nlst-dropzone{border:2px dashed rgba(27,26,23,.2);border-radius:14px;padding:18px;text-align:center;background:#FBF9F5;transition:border-color .2s,background .2s}
.nlst-dropzone.is-dragover{border-color:#9C7A3C;background:#FFF6E2}
.nlst-drop-empty{padding:18px 10px}
.nlst-drop-icon{font-size:42px}
.nlst-pick{background:linear-gradient(135deg,#9C7A3C,#B89254);color:#fff;border:0;border-radius:9px;padding:10px 18px;font:inherit;font-weight:700;cursor:pointer;margin-top:8px}
.nlst-pick:hover{filter:brightness(1.08)}
.nlst-drop-empty small{display:block;margin-top:8px;color:#9a9a9a;font-size:11.5px}
.nlst-gallery{display:grid;grid-template-columns:repeat(auto-fill,minmax(120px,1fr));gap:10px;margin-top:14px}
.nlst-gallery:empty{display:none}
.nlst-thumb{position:relative;aspect-ratio:1;border-radius:10px;overflow:hidden;border:1px solid rgba(27,26,23,.1);background:#fff}
.nlst-thumb img{width:100%;height:100%;object-fit:cover;display:block}
.nlst-thumb-del{position:absolute;inset-block-start:6px;inset-inline-end:6px;width:26px;height:26px;border-radius:50%;background:rgba(0,0,0,.6);color:#fff;border:0;font-size:14px;cursor:pointer;line-height:1}
.nlst-thumb-cover{position:absolute;inset-block-end:6px;inset-inline-start:6px;background:#9C7A3C;color:#fff;font-size:10px;font-weight:700;padding:2px 8px;border-radius:10px}
.nlst-tips{background:linear-gradient(135deg,#FBF9F5,#F0E9DA);border:1px solid rgba(156,122,60,.3)}
.nlst-tips ul{margin:0;padding-inline-start:18px;font-size:13px;color:#5a5a5a;line-height:1.7}
.nlst-tips b{color:#1B1A17}
</style>
CSS;
	}
}

if ( ! function_exists( 'nadlan_studio_js' ) ) {
	function nadlan_studio_js() {
		return <<<'JS'
<script id="nlst-js">
(function(){
	var root=document.querySelector('.nlst[data-rest]');if(!root)return;
	var REST=root.dataset.rest, NONCE=root.dataset.nonce, ID=parseInt(root.dataset.id,10), PT=root.dataset.pt;
	var statusEl=document.getElementById('nlst-status');
	function toast(kind,msg){statusEl.hidden=false;statusEl.className='nlst-status is-'+kind;statusEl.textContent=msg;clearTimeout(toast._t);toast._t=setTimeout(function(){statusEl.hidden=true;},3200);}
	function api(path,opts){opts=opts||{};opts.credentials='include';opts.headers=Object.assign({'X-WP-Nonce':NONCE},opts.headers||{});return fetch(REST+path,opts).then(function(r){return r.json().then(function(j){return{ok:r.ok,data:j,status:r.status};});});}

	// ---- LOAD current state ----
	api('').then(function(r){
		if(!r.ok){toast('err','שגיאה בטעינת הכרטיס.');return;}
		var d=r.data, m=d.meta||{};
		var setVal=function(id,v){var el=document.getElementById(id);if(el){if(el.type==='checkbox')el.checked=!!v;else el.value=v==null?'':v;}};
		setVal('f-tagline',m.tagline);setVal('f-description',m.description);
		setVal('f-city',m.city);setVal('f-address',m.address);
		setVal('f-phone',m.phone);setVal('f-email',m.email);setVal('f-website',m.website);
		setVal('f-social_facebook',m.social_facebook);setVal('f-social_instagram',m.social_instagram);
		setVal('f-social_tiktok',m.social_tiktok);setVal('f-social_youtube',m.social_youtube);
		setVal('f-video_url',m.video_url);
		setVal('f-lat',m.lat||31.7683);setVal('f-lng',m.lng||35.2137);
		// type-specific
		setVal('f-project_type',m.project_type);setVal('f-project_status',m.project_status);
		setVal('f-developer_name',m.developer_name);setVal('f-num_units',m.num_units);
		setVal('f-classification',m.classification);setVal('f-years_active',m.years_active);
		setVal('f-service_area',m.service_area);
		setVal('f-listing_type',m.listing_type);setVal('f-property_type',m.property_type);
		setVal('f-price',m.price);setVal('f-rooms',m.rooms);
		setVal('f-size_sqm',m.size_sqm);setVal('f-floor',m.floor);
		setVal('f-parking',m.parking);setVal('f-elevator',m.elevator);
		renderGallery(d.photos||[]);
		initMap(parseFloat(m.lat)||31.7683,parseFloat(m.lng)||35.2137);
	});

	// ---- SAVE ----
	function collect(){
		var ids=['tagline','description','city','address','phone','email','website',
			'social_facebook','social_instagram','social_tiktok','social_youtube','video_url',
			'lat','lng','project_type','project_status','developer_name','num_units',
			'classification','years_active','service_area',
			'listing_type','property_type','price','rooms','size_sqm','floor'];
		var out={};
		ids.forEach(function(k){var el=document.getElementById('f-'+k);if(el)out[k]=el.value;});
		var pk=document.getElementById('f-parking');if(pk)out.parking=pk.checked?1:0;
		var ev=document.getElementById('f-elevator');if(ev)out.elevator=ev.checked?1:0;
		return out;
	}
	document.getElementById('nlst-save-btn').addEventListener('click',function(){
		var btn=this;btn.classList.add('is-saving');btn.disabled=true;
		api('/save',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(collect())}).then(function(r){
			btn.classList.remove('is-saving');btn.disabled=false;
			toast(r.ok?'ok':'err',r.ok?'✓ נשמר. כל השינויים חיים.':'שגיאה בשמירה.');
		});
	});

	// ---- IMAGE UPLOAD ----
	var dz=document.getElementById('nlst-drop'),fi=document.getElementById('nlst-file');
	dz.querySelectorAll('.nlst-pick').forEach(function(b){b.addEventListener('click',function(){fi.click();});});
	fi.addEventListener('change',function(){uploadFiles(fi.files);fi.value='';});
	['dragenter','dragover'].forEach(function(ev){dz.addEventListener(ev,function(e){e.preventDefault();dz.classList.add('is-dragover');});});
	['dragleave','drop'].forEach(function(ev){dz.addEventListener(ev,function(e){e.preventDefault();dz.classList.remove('is-dragover');});});
	dz.addEventListener('drop',function(e){if(e.dataTransfer&&e.dataTransfer.files)uploadFiles(e.dataTransfer.files);});
	function uploadFiles(list){
		if(!list||!list.length)return;
		var done=0;
		Array.prototype.forEach.call(list,function(f){
			if(!f.type.startsWith('image/')){toast('err','קובץ לא תמונה דולג.');return;}
			if(f.size>10*1024*1024){toast('err',f.name+' גדול מ-10MB');return;}
			var fd=new FormData();fd.append('file',f);
			fetch(REST+'/upload',{method:'POST',credentials:'include',headers:{'X-WP-Nonce':NONCE},body:fd})
				.then(function(r){return r.json();})
				.then(function(j){if(j&&j.url){addThumb(j.url);done++;toast('ok','עלתה תמונה ('+done+'/'+list.length+')');}else{toast('err','שגיאה בהעלאה.');}});
		});
	}
	function renderGallery(urls){var g=document.getElementById('nlst-gallery');g.innerHTML='';urls.forEach(addThumb);}
	function addThumb(url){
		var g=document.getElementById('nlst-gallery');
		var el=document.createElement('div');el.className='nlst-thumb';
		el.innerHTML='<img src="'+url+'" alt="" loading="lazy">'+(g.children.length===0?'<span class="nlst-thumb-cover">קאבר</span>':'')+'<button type="button" class="nlst-thumb-del" aria-label="מחק">×</button>';
		el.querySelector('.nlst-thumb-del').addEventListener('click',function(){
			if(!confirm('למחוק תמונה?'))return;
			api('/gallery/delete',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({url:url})}).then(function(r){
				if(r.ok){el.remove();toast('ok','תמונה נמחקה.');}else{toast('err','שגיאה במחיקה.');}
			});
		});
		g.appendChild(el);
	}

	// ---- AI COPY ----
	document.querySelectorAll('.nlst-ai').forEach(function(btn){
		btn.addEventListener('click',function(){
			var ta=document.getElementById('f-description');var src=(ta.value||'').trim();
			if(src.length<5){toast('err','כתבו טקסט קצר תחילה (אפילו 2-3 מילים).');return;}
			btn.disabled=true;
			api('/ai-copy',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({source:src,mode:btn.dataset.mode})})
				.then(function(r){
					btn.disabled=false;
					if(r.data&&r.data.ok){ta.value=r.data.text;toast('ok','✨ הטקסט עודכן ע"י העוזר.');}
					else{toast('err',(r.data&&r.data.message)||'העוזר החכם אינו פעיל. הזינו מפתח Anthropic ב-Settings → NadLan AI.');}
				});
		});
	});

	// ---- MAP (Leaflet + OSM) ----
	function initMap(lat,lng){
		if(!window.L){setTimeout(function(){initMap(lat,lng);},300);return;}
		var map=L.map('nlst-map').setView([lat,lng],13);
		L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png',{attribution:'© OpenStreetMap',maxZoom:19}).addTo(map);
		var marker=L.marker([lat,lng],{draggable:true}).addTo(map);
		marker.on('dragend',function(e){
			var p=e.target.getLatLng();
			document.getElementById('f-lat').value=p.lat.toFixed(6);
			document.getElementById('f-lng').value=p.lng.toFixed(6);
			toast('ok','מיקום עודכן (אל תשכחו לשמור)');
		});
		map.on('click',function(e){marker.setLatLng(e.latlng);marker.fire('dragend',{target:marker});});
	}
})();
</script>
JS;
	}
}
