<?php
/**
 * nadlan-config - premium interactive project model and apartment picker.
 *
 * Tier 1 stays fast and practical: an architectural massing model from
 * project/unit metadata, routed into the existing /nadlan/v1/lead funnel.
 * Real developer drawings can replace demo units later without changing the
 * public journey.
 */

if ( ! defined( 'ABSPATH' ) ) {
	exit;
}

if ( ! function_exists( 'nadlan_p3d_enabled' ) ) {
	function nadlan_p3d_enabled() {
		return (bool) apply_filters( 'nadlan_p3d_enabled', get_option( 'nadlan_feature_project_3d', '0' ) === '1' );
	}
}

if ( ! function_exists( 'nadlan_p3d_status_label' ) ) {
	function nadlan_p3d_status_label( $status ) {
		$labels = array(
			'available' => 'זמינה לפנייה',
			'reserved'  => 'בתהליך בדיקה',
			'sold'      => 'לא זמינה',
		);
		return $labels[ $status ] ?? $labels['available'];
	}
}

if ( ! function_exists( 'nadlan_p3d_sanitize_decimal' ) ) {
	function nadlan_p3d_sanitize_decimal( $value ) {
		return is_numeric( $value ) ? (float) $value : 0.0;
	}
}

if ( ! function_exists( 'nadlan_p3d_units' ) ) {
	function nadlan_p3d_units( $post_id ) {
		$raw   = trim( (string) get_post_meta( (int) $post_id, 'project_3d_units', true ) );
		$units = $raw !== '' ? json_decode( $raw, true ) : array();
		if ( ! is_array( $units ) || ! $units ) {
			return array();
		}

		$out = array();
		foreach ( $units as $u ) {
			if ( ! is_array( $u ) || empty( $u['id'] ) ) {
				continue;
			}

			$status = sanitize_key( (string) ( $u['status'] ?? 'available' ) );
			if ( ! in_array( $status, array( 'available', 'reserved', 'sold' ), true ) ) {
				$status = 'available';
			}

			$out[] = array(
				'id'      => sanitize_key( (string) $u['id'] ),
				'title'   => sanitize_text_field( (string) ( $u['title'] ?? '' ) ),
				'points'  => preg_replace( '/[^0-9,. \-]/', '', (string) ( $u['points'] ?? '' ) ),
				'floor'   => max( 0, (int) ( $u['floor'] ?? 0 ) ),
				'rooms'   => nadlan_p3d_sanitize_decimal( $u['rooms'] ?? 0 ),
				'sqm'     => nadlan_p3d_sanitize_decimal( $u['sqm'] ?? 0 ),
				'balcony' => nadlan_p3d_sanitize_decimal( $u['balcony'] ?? 0 ),
				'dir'     => sanitize_text_field( (string) ( $u['dir'] ?? '' ) ),
				'line'    => sanitize_text_field( (string) ( $u['line'] ?? '' ) ),
				'view'    => sanitize_text_field( (string) ( $u['view'] ?? '' ) ),
				'building'      => sanitize_text_field( (string) ( $u['building'] ?? '' ) ),
				'availability'  => sanitize_text_field( (string) ( $u['availability'] ?? '' ) ),
				'note'          => sanitize_textarea_field( (string) ( $u['note'] ?? '' ) ),
				'market_note'   => sanitize_textarea_field( (string) ( $u['market_note'] ?? '' ) ),
				'source_note'   => sanitize_textarea_field( (string) ( $u['source_note'] ?? '' ) ),
				'price'   => nadlan_p3d_sanitize_decimal( $u['price'] ?? 0 ),
				'status'  => $status,
				'plan'    => esc_url_raw( (string) ( $u['plan'] ?? '' ) ),
			);
		}

		return $out;
	}
}

if ( ! function_exists( 'nadlan_p3d_demo_units' ) ) {
	function nadlan_p3d_demo_units() {
		return array(
			array(
				'id'      => 'demo-12-a',
				'title'   => 'קו A',
				'floor'   => 12,
				'rooms'   => 4,
				'sqm'     => 105,
				'balcony' => 12,
				'dir'     => 'צפון מערב',
				'line'    => 'A',
				'view'    => 'ים ושדרה ירוקה',
				'building'      => 'מגדל Rainbow',
				'availability'  => 'להמחשה, זמינות ומחיר לפי אישור יזם',
				'note'          => 'טיפוס דירה מערבי נמוך יחסית, מתאים להשוואת כיוון אוויר, מרפסת ונגישות למתחם הפנימי.',
				'market_note'   => 'אין מחיר רשמי במערכת. כאשר יוזן מקור מאושר, השדה יכול לשאת מחיר, עסקה אחרונה או טווח שיווק.',
				'source_note'   => 'הדגמה מקורית על בסיס נתוני פרויקט ציבוריים: מגדל גבוה, בנייני בוטיק, חצר פנימית וקרבה לים.',
				'price'   => 0,
				'status'  => 'available',
				'plan'    => '',
				'points'  => '408,578 486,578 486,594 408,594',
			),
			array(
				'id'      => 'demo-18-b',
				'title'   => 'קו B',
				'floor'   => 18,
				'rooms'   => 5,
				'sqm'     => 132,
				'balcony' => 16,
				'dir'     => 'מערב',
				'line'    => 'B',
				'view'    => 'חזית לים',
				'building'      => 'מגדל Rainbow',
				'availability'  => 'להמחשה, נדרש אימות מלאי',
				'note'          => 'דירת חמישה חדרים בקו מערבי, מוצגת כטיפוס משפחתי עם מרפסת ונוף פתוח יותר מהקומות הנמוכות.',
				'market_note'   => 'מחיר לפי פנייה בלבד. ניתן לקשור כאן עסקאות מדלן או נתוני יזם לאחר הרשאה ואימות.',
				'source_note'   => 'הקומות והכיוונים הם הדגמה תכנונית, לא תכנית מכר.',
				'price'   => 0,
				'status'  => 'available',
				'plan'    => '',
				'points'  => '492,479 570,479 570,495 492,495',
			),
			array(
				'id'      => 'demo-24-c',
				'title'   => 'קו C',
				'floor'   => 24,
				'rooms'   => 4,
				'sqm'     => 118,
				'balcony' => 14,
				'dir'     => 'דרום מערב',
				'line'    => 'C',
				'view'    => 'קו החוף והמרינה',
				'building'      => 'מגדל Rainbow',
				'availability'  => 'בתהליך בדיקה',
				'note'          => 'קו דרום מערבי להמחשה, מתאים לבדיקת נוף, חשיפה לשמש ומיקום ביחס לקו החוף.',
				'market_note'   => 'אפשר להציג כאן עסקה דומה, מחיר למ"ר או הערת זמינות כאשר מקור מאושר מוזן למערכת.',
				'source_note'   => 'הדגמה בלבד, ללא מחיר רשמי.',
				'price'   => 0,
				'status'  => 'reserved',
				'plan'    => '',
				'points'  => '576,380 654,380 654,396 576,396',
			),
			array(
				'id'      => 'demo-30-d',
				'title'   => 'קו D',
				'floor'   => 30,
				'rooms'   => 5,
				'sqm'     => 146,
				'balcony' => 20,
				'dir'     => 'מערב',
				'line'    => 'D',
				'view'    => 'ים פתוח וקו רקיע',
				'building'      => 'מגדל Rainbow',
				'availability'  => 'זמינות לפי פנייה',
				'note'          => 'קומה גבוהה יותר, מיועדת להמחיש את שכבת הנוף ואת מעבר המשתמש מהחזית אל מבט מהדירה.',
				'market_note'   => 'שדה מחיר נשאר ריק עד קבלת מלאי מאומת.',
				'source_note'   => 'לא תכנית מכר ולא הבטחת זמינות.',
				'price'   => 0,
				'status'  => 'available',
				'plan'    => '',
				'points'  => '492,281 570,281 570,297 492,297',
			),
			array(
				'id'      => 'demo-34-e',
				'title'   => 'קו E',
				'floor'   => 34,
				'rooms'   => 5,
				'sqm'     => 158,
				'balcony' => 22,
				'dir'     => 'צפון מערב',
				'line'    => 'E',
				'view'    => 'ים, פארק ושדה דב',
				'building'      => 'מגדל Rainbow',
				'availability'  => 'זמינות לפי פנייה',
				'note'          => 'קומה גבוהה בקו צפוני מערבי, להמחשת חיבור בין הים, הפארק והמתחם החדש.',
				'market_note'   => 'נתוני שוק יוצגו רק לאחר הזנת מקור מורשה.',
				'source_note'   => 'המחשה תכנונית לממשק בלבד.',
				'price'   => 0,
				'status'  => 'available',
				'plan'    => '',
				'points'  => '408,215 486,215 486,231 408,231',
			),
			array(
				'id'      => 'demo-38-p',
				'title'   => 'פנטהאוז הדגמה',
				'floor'   => 38,
				'rooms'   => 6,
				'sqm'     => 214,
				'balcony' => 44,
				'dir'     => 'מערב וצפון',
				'line'    => 'P',
				'view'    => 'קו ראשון לים',
				'building'      => 'מגדל Rainbow',
				'availability'  => 'להמחשה בלבד',
				'note'          => 'קומת פרימיום להמחשת תרחיש רכישה מתקדם, בדיקת ליווי מקצועי ואיסוף עניין ממוקד.',
				'market_note'   => 'מחיר וזמינות אינם מוצגים ללא אישור מקור.',
				'source_note'   => 'לא מלאי רשמי.',
				'price'   => 0,
				'status'  => 'available',
				'plan'    => '',
				'points'  => '408,149 654,149 654,179 408,179',
			),
			array(
				'id'      => 'demo-07-g',
				'title'   => 'בניין בוטיק · קו G',
				'floor'   => 7,
				'rooms'   => 3,
				'sqm'     => 86,
				'balcony' => 10,
				'dir'     => 'מזרח',
				'line'    => 'G',
				'view'    => 'חצר פנימית ומרחבי המתחם',
				'building'      => 'בניין בוטיק',
				'availability'  => 'זמינות לפי פנייה',
				'note'          => 'דירת בוטיק נמוכה יותר להמחשת ששת המבנים המרקמיים והחצר הפנימית של המתחם.',
				'market_note'   => 'אפשר לשייך כאן מכירה דומה או טווח מחיר כאשר מקור מאומת זמין.',
				'source_note'   => 'הדגמה שמטרתה להראות שהפרויקט כולל גם בנייני בוטיק, לא רק מגדל.',
				'price'   => 0,
				'status'  => 'available',
				'plan'    => '',
				'points'  => '705,705 790,705 790,730 705,730',
			),
		);
	}
}

if ( ! function_exists( 'nadlan_p3d_meta' ) ) {
	function nadlan_p3d_meta( $post_id, $demo ) {
		$title     = wp_strip_all_tags( get_the_title( $post_id ) );
		$developer = sanitize_text_field( (string) get_post_meta( $post_id, 'developer_name', true ) );
		$status    = sanitize_text_field( (string) get_post_meta( $post_id, 'project_status', true ) );
		$units     = sanitize_text_field( (string) get_post_meta( $post_id, 'num_units', true ) );
		$city      = sanitize_text_field( (string) get_post_meta( $post_id, 'city', true ) );
		$address   = sanitize_text_field( (string) get_post_meta( $post_id, 'address', true ) );
		$lat       = nadlan_p3d_sanitize_decimal( get_post_meta( $post_id, 'lat', true ) );
		$lng       = nadlan_p3d_sanitize_decimal( get_post_meta( $post_id, 'lng', true ) );
		$floor_h   = nadlan_p3d_sanitize_decimal( get_post_meta( $post_id, 'project_3d_floor_height_m', true ) );
		if ( $floor_h <= 0 ) {
			$floor_h = 3.05;
		}
		$ground_m = nadlan_p3d_sanitize_decimal( get_post_meta( $post_id, 'project_3d_ground_elevation_m', true ) );

		return array(
			'title'     => $title ?: 'הפרויקט',
			'developer' => $developer,
			'status'    => $status,
			'units'     => $units,
			'city'      => $city,
			'address'   => $address,
			'lat'       => $lat,
			'lng'       => $lng,
			'floor_height_m'     => $floor_h,
			'ground_elevation_m' => $ground_m,
			'url'       => get_permalink( $post_id ),
			'demo'      => (bool) $demo,
		);
	}
}

if ( ! function_exists( 'nadlan_p3d_json' ) ) {
	function nadlan_p3d_json( $value, $fallback ) {
		$json = wp_json_encode( $value, JSON_UNESCAPED_UNICODE | JSON_HEX_TAG | JSON_HEX_AMP | JSON_HEX_APOS | JSON_HEX_QUOT );
		return is_string( $json ) && $json !== '' ? $json : $fallback;
	}
}

if ( ! function_exists( 'nadlan_p3d_has_data' ) ) {
	function nadlan_p3d_has_data( $post_id ) {
		$post_id = (int) $post_id;
		return get_post_meta( $post_id, 'project_3d_image', true ) !== ''
			|| get_post_meta( $post_id, 'project_3d_units', true ) !== ''
			|| get_post_meta( $post_id, 'project_3d_demo', true ) === '1';
	}
}

if ( ! function_exists( 'nadlan_p3d_insert_after_project_header' ) ) {
	function nadlan_p3d_insert_after_project_header( $content, $block ) {
		if ( strpos( $content, 'nlp3d-premium' ) !== false ) {
			return $content;
		}

		$header_pos = strpos( $content, 'class="nlpf"' );
		if ( $header_pos === false ) {
			return $block . $content;
		}

		$script_end = strpos( $content, '</script>', $header_pos );
		if ( $script_end !== false && $script_end < $header_pos + 12000 ) {
			$insert_at = $script_end + strlen( '</script>' );
			return substr( $content, 0, $insert_at ) . $block . substr( $content, $insert_at );
		}

		$header_end = strpos( $content, '</div>', $header_pos );
		if ( $header_end !== false ) {
			$insert_at = $header_end + strlen( '</div>' );
			return substr( $content, 0, $insert_at ) . $block . substr( $content, $insert_at );
		}

		return $block . $content;
	}
}

if ( ! function_exists( 'nadlan_p3d_render' ) ) {
	function nadlan_p3d_render( $post_id ) {
		if ( ! nadlan_p3d_enabled() ) {
			return '';
		}

		$post_id = (int) $post_id;
		$image   = esc_url( (string) get_post_meta( $post_id, 'project_3d_image', true ) );
		$viewbox = sanitize_text_field( (string) get_post_meta( $post_id, 'project_3d_viewbox', true ) );
		if ( $viewbox === '' ) {
			$viewbox = '0 0 1000 1000';
		}
		$units   = nadlan_p3d_units( $post_id );
		$demo    = false;
		if ( ! $units ) {
			$units = nadlan_p3d_demo_units();
			$demo  = true;
		}
		if ( $image === '' && $demo ) {
			$image = esc_url( plugins_url( '../assets/concept/rainbow-facade-demo.svg', __FILE__ ) );
		}
		$image_alt = $demo ? 'המחשת חזית מקורית של מגדל ובנייני בוטיק לבחירת דירה' : 'חומר מקור של הפרויקט';
		$image_cap = $demo ? 'המחשה מקורית, לא תכנית מכר רשמית' : 'חומר מקור';

		$meta      = nadlan_p3d_meta( $post_id, $demo );
		$uid       = 'nlp3d-' . $post_id;
		$unit_json = nadlan_p3d_json( $units, '[]' );
		$meta_json = nadlan_p3d_json( $meta, '{}' );

		ob_start();
		?>
<section class="nlp3d nlp3d-premium" dir="rtl" data-project="<?php echo esc_attr( $post_id ); ?>" aria-labelledby="<?php echo esc_attr( $uid ); ?>-title">
	<div class="nlp3d-grid" aria-hidden="true"></div>
	<div class="nlp3d-shell">
		<div class="nlp3d-copy">
			<p class="nlp3d-kicker">תצוגת פרויקט אינטראקטיבית</p>
			<h2 id="<?php echo esc_attr( $uid ); ?>-title"><?php echo esc_html( $meta['title'] ); ?> · בחירת דירה בתלת ממד</h2>
			<p class="nlp3d-lead-text">מודל עבודה אדריכלי שמאפשר להבין קומות, כיווני אוויר, שטחים וקו נוף, ואז לשלוח פנייה ממוקדת על הדירה שנבחרה.</p>
			<div class="nlp3d-shop-path" aria-label="תהליך בחירה">
				<span>1. מסובבים</span>
				<span>2. בוחרים דירה</span>
				<span>3. בודקים ליווי</span>
				<span>4. מבקשים התקדמות</span>
			</div>
			<div class="nlp3d-metrics" aria-label="פרטי פרויקט">
				<span><?php echo $meta['developer'] ? esc_html( $meta['developer'] ) : 'יזם יימסר בפנייה'; ?></span>
				<span><?php echo $meta['status'] ? esc_html( $meta['status'] ) : 'סטטוס בבדיקה'; ?></span>
				<span><?php echo $meta['units'] ? esc_html( $meta['units'] ) . ' יחידות' : 'מלאי לפי פנייה'; ?></span>
			</div>
			<?php if ( $demo ) : ?>
				<p class="nlp3d-demo-note">תצוגת הדגמה. הדירות, המחירים והזמינות אינם נתוני מכירה רשמיים. הנתונים האמיתיים יוזנו כאשר היזם או מנהל הפרויקט יאשרו מלאי ותוכניות.</p>
			<?php endif; ?>
		</div>

		<div class="nlp3d-stage-wrap">
			<div class="nlp3d-toolbar" aria-label="שליטה במודל">
				<button type="button" class="nlp3d-angle is-active" data-angle="-32" data-action="angle-facade">חזית</button>
				<button type="button" class="nlp3d-angle" data-angle="0" data-action="angle-sea">ים</button>
				<button type="button" class="nlp3d-angle" data-angle="32" data-action="angle-city">עיר</button>
				<button type="button" class="nlp3d-orbit" data-orbit="1" data-action="orbit-building">סיבוב</button>
				<span class="nlp3d-drag-note">אפשר לגרור את המודל</span>
			</div>
			<div class="nlp3d-scene" style="--angle:-32deg" role="group" aria-label="מודל תלת ממדי סכמטי של מגדל מגורים">
				<div class="nlp3d-horizon"></div>
				<div class="nlp3d-sea"></div>
				<div class="nlp3d-park"></div>
				<div class="nlp3d-runway"></div>
				<div class="nlp3d-tower" role="group" aria-label="בחירת קומה ישירות מהמגדל"></div>
				<div class="nlp3d-shadow" aria-hidden="true"></div>
				<?php if ( $image ) : ?>
					<figure class="nlp3d-facade" data-viewbox="<?php echo esc_attr( $viewbox ); ?>">
						<img src="<?php echo $image; ?>" alt="<?php echo esc_attr( $image_alt ); ?>" loading="lazy">
						<svg class="nlp3d-facade-hotspots" viewBox="<?php echo esc_attr( $viewbox ); ?>" preserveAspectRatio="none" aria-label="בחירת דירה על גבי החזית"></svg>
						<figcaption><?php echo esc_html( $image_cap ); ?></figcaption>
					</figure>
				<?php endif; ?>
			</div>
		</div>

		<aside class="nlp3d-console" aria-label="בחירת דירה">
			<div class="nlp3d-console-head">
				<p>בחרו קומה ודירה</p>
				<span class="nlp3d-status-chip">מודל פעיל</span>
			</div>
			<div class="nlp3d-floor-strip" aria-label="קומות זמינות"></div>
			<div class="nlp3d-units" aria-label="דירות בקומה"></div>
			<div class="nlp3d-detail" aria-live="polite">
				<h3 class="nlp3d-selected-title">בחרו דירה</h3>
				<dl class="nlp3d-facts"></dl>
				<a class="nlp3d-plan" href="#" target="_blank" rel="noopener" hidden>פתיחת תוכנית דירה</a>
				<button type="button" class="nlp3d-view-toggle" data-action="view-from-unit">מבט מהדירה</button>
				<div class="nlp3d-viewframe" hidden>
					<div class="nlp3d-view-sky"></div>
					<div class="nlp3d-view-lines"></div>
					<p class="nlp3d-view-copy"></p>
				</div>
				<div class="nlp3d-tools" aria-label="מידע נוסף על הדירה">
					<button type="button" class="nlp3d-tool is-active" data-tool="spec" data-action="unit-spec">מפרט</button>
					<button type="button" class="nlp3d-tool" data-tool="drawing" data-action="unit-drawing">תוכנית</button>
					<button type="button" class="nlp3d-tool" data-tool="advisors" data-action="unit-advisors">יועצים</button>
				</div>
				<div class="nlp3d-tool-panel" aria-live="polite"></div>
				<div class="nlp3d-deal-steps" aria-label="מסלול בדיקת רכישה">
					<span>בחירה</span>
					<span>אימות</span>
					<span>ליווי</span>
					<span>אישור יזם</span>
				</div>
			</div>
			<form class="nlp3d-lead-form">
				<p class="nlp3d-form-title">רוצים להתקדם עם הדירה הזו?</p>
				<input type="text" name="name" placeholder="שם מלא" autocomplete="name" required>
				<input type="tel" name="phone" placeholder="טלפון" autocomplete="tel" required>
				<input type="email" name="email" placeholder="אימייל" autocomplete="email">
				<input type="text" name="budget" placeholder="מסגרת תקציב, אם ידועה">
				<input type="text" name="timeline" placeholder="מתי רלוונטי להתקדם?">
				<select name="advisor" aria-label="ליווי מקצועי מבוקש">
					<option value="">איזה ליווי תרצו לצרף?</option>
					<option value="lawyer">עורך דין רכישה</option>
					<option value="mortgage">יועץ משכנתאות</option>
					<option value="designer">מעצב פנים</option>
					<option value="inspector">בדק בית</option>
				</select>
				<input type="text" name="company" class="nlp3d-hp" tabindex="-1" autocomplete="off" aria-hidden="true">
				<div class="nlp3d-actions">
					<button type="submit" class="nlp3d-send" data-intent="callback" data-action="lead-callback">דברו איתי על הדירה</button>
					<button type="submit" class="nlp3d-send nlp3d-send-alt" data-intent="purchase" data-action="nonbinding-purchase-check">התחל בדיקת רכישה - לא מחייב</button>
				</div>
				<p class="nlp3d-legal">הפנייה אינה עסקה מחייבת, אינה זכרון דברים ואינה שריון רשמי. נציג יאמת זמינות, מחיר ותנאים עם היזם לפני כל התקדמות.</p>
				<p class="nlp3d-ok" hidden></p>
			</form>
		</aside>
	</div>
	<script type="application/json" class="nlp3d-data"><?php echo $unit_json; ?></script>
	<script type="application/json" class="nlp3d-meta"><?php echo $meta_json; ?></script>
</section>
		<?php
		return ob_get_clean();
	}
}

add_shortcode(
	'nadlan_project_3d',
	function ( $atts ) {
		$atts = shortcode_atts( array( 'id' => get_the_ID() ), $atts );
		return nadlan_p3d_render( (int) $atts['id'] );
	}
);

if ( ! function_exists( 'nadlan_p3d_inline_css' ) ) {
	function nadlan_p3d_inline_css() {
		return <<<'CSS'
.nlp3d,.nlp3d *{box-sizing:border-box}.nlp3d{--ink:#f6efe2;--muted:#c9bd9f;--gold:#c4a15a;--gold2:#ead8a3;--deep:#071817;--teal:#103b3b;--panel:rgba(7,15,16,.72);width:100%;margin:42px auto;color:var(--ink);position:relative;overflow:hidden;background:radial-gradient(circle at 18% 8%,rgba(25,105,105,.55),transparent 31%),linear-gradient(135deg,#061313,#102d2d 54%,#17140e);box-shadow:0 28px 80px rgba(0,0,0,.24);isolation:isolate}.nlp3d-grid{position:absolute;inset:0;background-image:linear-gradient(rgba(234,216,163,.07) 1px,transparent 1px),linear-gradient(90deg,rgba(234,216,163,.07) 1px,transparent 1px);background-size:34px 34px;opacity:.8;pointer-events:none}.nlp3d-shell{position:relative;z-index:1;display:grid;grid-template-columns:minmax(260px,.86fr) minmax(360px,1.35fr) minmax(300px,.82fr);gap:22px;min-height:680px;padding:34px}.nlp3d-copy{align-self:end;padding-bottom:22px}.nlp3d-kicker{margin:0 0 12px;color:var(--gold2);font-size:13px}.nlp3d h2{font-size:clamp(30px,4.4vw,58px);line-height:1.02;margin:0 0 18px;font-family:Georgia,"Times New Roman",serif;font-weight:500;letter-spacing:0;max-width:11ch}.nlp3d-lead-text{color:rgba(246,239,226,.84);font-size:17px;line-height:1.75;max-width:34ch;margin:0 0 18px}.nlp3d-metrics{display:grid;gap:8px;margin:18px 0}.nlp3d-metrics span{display:inline-flex;width:max-content;max-width:100%;min-height:34px;align-items:center;border:1px solid rgba(234,216,163,.22);background:rgba(255,255,255,.055);padding:7px 12px;color:#fff7e6;font-size:13px}.nlp3d-demo-note{margin:16px 0 0;color:#f1dba0;font-size:13px;line-height:1.55;border-right:2px solid var(--gold);padding-right:12px}.nlp3d-stage-wrap{position:relative;min-height:620px}.nlp3d-toolbar{position:absolute;z-index:8;top:12px;right:12px;display:flex;gap:8px;flex-wrap:wrap}.nlp3d button{font:inherit;min-width:44px;min-height:44px}.nlp3d-angle,.nlp3d-orbit{border:1px solid rgba(234,216,163,.34);background:rgba(7,24,24,.72);color:var(--ink);padding:8px 14px;cursor:pointer}.nlp3d-angle.is-active,.nlp3d-orbit.is-active{background:linear-gradient(135deg,var(--gold),#7c5e27);color:#10100c;border-color:rgba(255,255,255,.42)}.nlp3d-scene{position:absolute;inset:0;border:1px solid rgba(234,216,163,.2);background:linear-gradient(180deg,rgba(15,48,50,.4),rgba(8,18,18,.86));overflow:hidden;perspective:1100px}.nlp3d-horizon{position:absolute;inset:14% -8% auto;height:1px;background:linear-gradient(90deg,transparent,rgba(234,216,163,.32),transparent)}.nlp3d-sea{position:absolute;left:-12%;right:52%;bottom:8%;height:44%;background:linear-gradient(135deg,rgba(43,119,139,.5),rgba(7,31,42,.08));transform:skewY(-10deg)}.nlp3d-park{position:absolute;right:-8%;bottom:20%;width:56%;height:24%;background:linear-gradient(135deg,rgba(93,127,83,.26),rgba(196,161,90,.08));transform:skewY(10deg)}.nlp3d-runway{position:absolute;right:8%;left:18%;bottom:24%;height:46px;border-top:1px solid rgba(234,216,163,.18);border-bottom:1px solid rgba(234,216,163,.18);transform:rotate(-7deg);opacity:.7}.nlp3d-shadow{position:absolute;right:27%;bottom:14%;width:44%;height:10%;background:radial-gradient(ellipse,rgba(0,0,0,.44),transparent 72%);filter:blur(9px)}.nlp3d-tower{position:absolute;right:50%;bottom:118px;width:min(230px,40%);height:420px;transform-style:preserve-3d;transform:translateX(50%) rotateX(62deg) rotateZ(var(--angle,-32deg));transition:transform .55s cubic-bezier(.2,.8,.2,1)}.nlp3d-scene.is-orbit .nlp3d-tower{animation:nlp3dOrbit 14s linear infinite}.nlp3d-plate{position:absolute;right:0;left:0;height:12px;border:1px solid rgba(234,216,163,.24);background:linear-gradient(135deg,rgba(255,255,255,.16),rgba(196,161,90,.12));box-shadow:0 3px 0 rgba(0,0,0,.16);transform:translateZ(calc(var(--i)*3px));transition:background .18s,border-color .18s,box-shadow .18s}.nlp3d-plate.has-units{background:linear-gradient(135deg,rgba(234,216,163,.34),rgba(255,255,255,.08))}.nlp3d-plate.is-active{border-color:#fff0b8;background:linear-gradient(135deg,#f4dd98,rgba(255,255,255,.2));box-shadow:0 0 0 2px rgba(234,216,163,.2),0 0 24px rgba(234,216,163,.22)}.nlp3d-plate.is-sold{opacity:.42}.nlp3d-reference{position:absolute;left:16px;bottom:16px;width:min(170px,28%);margin:0;border:1px solid rgba(234,216,163,.22);background:rgba(0,0,0,.35);padding:6px}.nlp3d-reference img{display:block;width:100%;height:auto}.nlp3d-reference figcaption{font-size:11px;color:var(--muted);margin-top:4px}.nlp3d-console{align-self:stretch;background:var(--panel);border:1px solid rgba(234,216,163,.24);backdrop-filter:blur(16px);padding:20px;display:flex;flex-direction:column;gap:16px;box-shadow:inset 0 1px 0 rgba(255,255,255,.08)}.nlp3d-console-head{display:flex;justify-content:space-between;align-items:center;gap:12px;border-bottom:1px solid rgba(234,216,163,.16);padding-bottom:12px}.nlp3d-console-head p{font-family:Georgia,"Times New Roman",serif;font-size:22px;margin:0}.nlp3d-status-chip{border:1px solid rgba(234,216,163,.3);color:#fff3c0;padding:5px 9px;font-size:12px}.nlp3d-floor-strip{display:flex;flex-wrap:wrap;gap:8px}.nlp3d-floor{border:1px solid rgba(234,216,163,.24);background:rgba(255,255,255,.055);color:var(--ink);padding:7px 11px;cursor:pointer}.nlp3d-floor.is-active,.nlp3d-floor:hover,.nlp3d-floor:focus-visible{background:#ead8a3;color:#16140f;outline:none}.nlp3d-units{display:grid;gap:9px}.nlp3d-unit-card{width:100%;min-height:58px;text-align:right;border:1px solid rgba(234,216,163,.2);background:rgba(255,255,255,.055);color:var(--ink);padding:11px 12px;cursor:pointer}.nlp3d-unit-card strong{display:block;font-size:15px}.nlp3d-unit-card span{display:block;color:var(--muted);font-size:12px;margin-top:4px}.nlp3d-unit-card.is-active,.nlp3d-unit-card:hover,.nlp3d-unit-card:focus-visible{outline:none;border-color:#ead8a3;background:rgba(234,216,163,.18)}.nlp3d-unit-card.is-sold{opacity:.55}.nlp3d-detail{background:rgba(255,255,255,.06);border:1px solid rgba(234,216,163,.16);padding:16px}.nlp3d-selected-title{margin:0 0 12px;font-size:21px;font-family:Georgia,"Times New Roman",serif;font-weight:500}.nlp3d-facts{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:8px;margin:0}.nlp3d-facts div{border-top:1px solid rgba(234,216,163,.18);padding-top:8px}.nlp3d-facts dt{font-size:12px;color:var(--muted)}.nlp3d-facts dd{margin:2px 0 0;color:#fff;font-weight:700}.nlp3d-plan{display:inline-flex;margin-top:12px;color:#ffe8a6;text-decoration:none;border-bottom:1px solid currentColor}.nlp3d-lead-form{display:grid;grid-template-columns:1fr 1fr;gap:10px;margin-top:auto}.nlp3d-form-title,.nlp3d-legal,.nlp3d-ok{grid-column:1/-1;margin:0}.nlp3d-form-title{font-weight:700;color:#fff}.nlp3d-lead-form input{min-height:46px;border:1px solid rgba(234,216,163,.26);background:rgba(255,255,255,.9);color:#16140f;padding:10px 12px;border-radius:0}.nlp3d-lead-form input:focus{outline:2px solid #ead8a3;outline-offset:2px}.nlp3d-actions{grid-column:1/-1;display:grid;grid-template-columns:1fr 1fr;gap:10px}.nlp3d-send{border:0;background:linear-gradient(135deg,#ead8a3,#b99043);color:#15120c;font-weight:800;padding:13px 14px;cursor:pointer;box-shadow:0 12px 28px rgba(0,0,0,.22)}.nlp3d-send-alt{background:transparent;color:#ffe8a6;border:1px solid rgba(234,216,163,.42);box-shadow:none}.nlp3d-send:hover,.nlp3d-send:focus-visible{filter:brightness(1.05);outline:2px solid rgba(255,255,255,.7);outline-offset:2px}.nlp3d-send:disabled{opacity:.55;cursor:not-allowed}.nlp3d-legal{font-size:12px;color:var(--muted);line-height:1.45}.nlp3d-ok{font-weight:700;color:#fff2b9}.nlp3d-hp{position:absolute!important;width:1px!important;height:1px!important;overflow:hidden!important;clip:rect(1px,1px,1px,1px)!important;clip-path:inset(50%)!important;white-space:nowrap!important}.nlp3d-status-available{color:#dff8dc}.nlp3d-status-reserved{color:#ffe2a7}.nlp3d-status-sold{color:#c6c6c6}@keyframes nlp3dOrbit{from{transform:translateX(50%) rotateX(62deg) rotateZ(-40deg)}to{transform:translateX(50%) rotateX(62deg) rotateZ(320deg)}}@media(max-width:1240px){.nlp3d-shell{grid-template-columns:1fr 1.2fr;min-height:auto}.nlp3d-console{grid-column:1/-1}.nlp3d-copy{align-self:start;padding-bottom:0}.nlp3d h2{max-width:16ch}.nlp3d-stage-wrap{min-height:560px}}@media(max-width:900px){.nlp3d{margin:28px 0}.nlp3d-shell{grid-template-columns:1fr;padding:22px}.nlp3d-stage-wrap{min-height:520px}.nlp3d-copy{order:1}.nlp3d-stage-wrap{order:2}.nlp3d-console{order:3}.nlp3d h2{max-width:none}.nlp3d-reference{display:none}}@media(max-width:600px){.nlp3d-shell{padding:16px;gap:16px}.nlp3d-stage-wrap{min-height:460px}.nlp3d-toolbar{position:relative;top:auto;right:auto;margin-bottom:10px}.nlp3d-scene{position:relative;height:430px}.nlp3d-tower{width:210px;height:360px;bottom:92px}.nlp3d-facts,.nlp3d-lead-form,.nlp3d-actions{grid-template-columns:1fr}.nlp3d h2{font-size:32px}.nlp3d-lead-text{font-size:15px}.nlp3d-console{padding:16px}.nlp3d-floor{padding:8px 10px}.nlp3d-actions .nlp3d-send{width:100%}}@media(max-width:390px){.nlp3d-shell{padding:14px}.nlp3d-scene{height:400px}.nlp3d-tower{width:190px;height:330px}.nlp3d-toolbar{gap:6px}.nlp3d-angle,.nlp3d-orbit{padding:7px 10px}}
CSS;
	}
}

if ( ! function_exists( 'nadlan_p3d_experience_css' ) ) {
	function nadlan_p3d_experience_css() {
		return <<<'CSS'
.entry-content>.nlp3d,.wp-block-post-content>.nlp3d{width:min(1180px,calc(100vw - 48px));max-width:none;margin-block:22px 38px;margin-inline:calc(50% - min(590px,calc(50vw - 24px)));border-radius:28px}.nlp3d{border:1px solid rgba(234,216,163,.2)}.nlp3d-shop-path{display:grid;grid-template-columns:1fr;gap:7px;margin:16px 0 0}.nlp3d-shop-path span{display:flex;align-items:center;min-height:34px;width:max-content;max-width:100%;padding:6px 11px;border:1px solid rgba(234,216,163,.2);background:rgba(255,255,255,.06);color:#fff3d0;font-size:12.5px}.nlp3d-tools{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:7px;margin-top:14px}.nlp3d-tool{border:1px solid rgba(234,216,163,.24);background:rgba(255,255,255,.06);color:#ffe8a6;padding:8px 10px;cursor:pointer}.nlp3d-tool.is-active,.nlp3d-tool:hover,.nlp3d-tool:focus-visible{background:rgba(234,216,163,.2);color:#fff;outline:2px solid rgba(234,216,163,.42);outline-offset:2px}.nlp3d-tool-panel{margin-top:10px;border:1px solid rgba(234,216,163,.16);background:rgba(0,0,0,.18);padding:12px 13px;color:#f7edd2;line-height:1.55}.nlp3d-tool-panel strong{display:block;color:#fff3bd;margin-bottom:4px}.nlp3d-tool-panel p{margin:0;font-size:13px}.nlp3d-lead-form select{min-height:46px;border:1px solid rgba(234,216,163,.26);background:rgba(255,255,255,.9);color:#16140f;padding:10px 12px;border-radius:0;font:inherit}.nlp3d-lead-form select:focus{outline:2px solid #ead8a3;outline-offset:2px}.nlp3d-send-alt{font-weight:800}@media(max-width:900px){.entry-content>.nlp3d,.wp-block-post-content>.nlp3d{width:min(100%,calc(100vw - 28px));margin-inline:calc(50% - min(50%,calc(50vw - 14px)));border-radius:22px}.nlp3d-shop-path{grid-template-columns:repeat(2,minmax(0,1fr))}.nlp3d-shop-path span{width:100%}}@media(max-width:600px){.entry-content>.nlp3d,.wp-block-post-content>.nlp3d{width:calc(100vw - 22px);margin-inline:calc(50% - 50vw + 11px);margin-block:18px 30px;border-radius:18px}.nlp3d-tools{grid-template-columns:1fr}.nlp3d-shop-path{grid-template-columns:1fr}.nlp3d-tool-panel{font-size:13px}.nlp3d-lead-form select{width:100%}}
CSS;
	}
}

if ( ! function_exists( 'nadlan_p3d_inline_js' ) ) {
	function nadlan_p3d_inline_js( $rest_url ) {
		$js = <<<'JS'
(function(){
	function readJson(node,fallback){try{return JSON.parse(node ? node.textContent : '')}catch(e){return fallback}}
	function fmt(n){return new Intl.NumberFormat('he-IL').format(n)}
	function statusLabel(status){return status==='sold'?'לא זמינה':(status==='reserved'?'בתהליך בדיקה':'זמינה לפנייה')}
	function firstAvailable(units){return units.find(function(u){return u.status!=='sold'}) || units[0] || null}
	function selectedTitle(u){if(!u){return 'בחרו דירה'}var base=u.title || ('קו '+(u.line||u.id));return base+' · קומה '+(u.floor||'-')}
	function unitText(u){var parts=[];if(u.rooms){parts.push(u.rooms+' חדרים')}if(u.sqm){parts.push(fmt(u.sqm)+' מ"ר')}if(u.view){parts.push(u.view)}return parts.join(' · ')}
	function detailRows(u,meta){
		var price=(meta.demo||!u.price)?'לפי פנייה':('₪'+fmt(u.price));
		var rows=[['סטטוס',statusLabel(u.status)],['בניין',u.building||'לפי פנייה'],['קו',u.line||'לפי פנייה'],['חדרים',u.rooms?u.rooms:'לפי פנייה'],['שטח',u.sqm?fmt(u.sqm)+' מ"ר':'לפי פנייה'],['מרפסת',u.balcony?fmt(u.balcony)+' מ"ר':'לפי פנייה'],['כיוון',u.dir||'לפי פנייה'],['נוף',u.view||'לפי פנייה'],['מחיר',price],['זמינות',u.availability||'לא מאומתת'],['יזם',meta.developer||'לפי פנייה']];
		if(u.market_note){rows.push(['נתוני שוק',u.market_note])}
		if(u.source_note){rows.push(['מקור',u.source_note])}
		return rows;
	}
	function bearingForDirection(dir){
		dir=(dir||'').toString();
		var north=dir.indexOf('צפון')>-1,south=dir.indexOf('דרום')>-1,east=dir.indexOf('מזרח')>-1,west=dir.indexOf('מערב')>-1;
		if(north&&west){return 315} if(south&&west){return 225} if(north&&east){return 45} if(south&&east){return 135}
		if(west){return 270} if(east){return 90} if(south){return 180} return 0;
	}
	function cameraParams(u,meta){
		var floor=Math.max(1,parseInt(u&&u.floor||1,10));
		var floorHeight=Number(meta.floor_height_m||3.05)||3.05;
		var ground=Number(meta.ground_elevation_m||0)||0;
		var altitude=ground+4+((floor-1)*floorHeight)+1.55;
		return {lat:Number(meta.lat||0)||0,lng:Number(meta.lng||0)||0,bearing:bearingForDirection(u&&u.dir),altitude_m:Math.round(altitude*10)/10,floor_height_m:floorHeight};
	}
	function init(root){
		var units=readJson(root.querySelector('.nlp3d-data'),[]);
		var meta=readJson(root.querySelector('.nlp3d-meta'),{});
		if(!Array.isArray(units)||!units.length){return}
		var scene=root.querySelector('.nlp3d-scene');
		var tower=root.querySelector('.nlp3d-tower');
		var facade=root.querySelector('.nlp3d-facade');
		var hotspots=root.querySelector('.nlp3d-facade-hotspots');
		var floors=[].slice.call(new Set(units.map(function(u){return parseInt(u.floor||0,10)}).filter(Boolean))).sort(function(a,b){return b-a});
		var maxFloor=Math.max.apply(null,floors.concat([39]));
		var minFloor=Math.max(1,Math.min.apply(null,floors.concat([1])));
		var activeUnit=firstAvailable(units);
		var activeFloor=activeUnit ? parseInt(activeUnit.floor||floors[0]||maxFloor,10) : maxFloor;
		var floorStrip=root.querySelector('.nlp3d-floor-strip');
		var unitList=root.querySelector('.nlp3d-units');
		var title=root.querySelector('.nlp3d-selected-title');
		var facts=root.querySelector('.nlp3d-facts');
		var plan=root.querySelector('.nlp3d-plan');
		var form=root.querySelector('.nlp3d-lead-form');
		var ok=root.querySelector('.nlp3d-ok');
		var viewToggle=root.querySelector('.nlp3d-view-toggle');
		var viewFrame=root.querySelector('.nlp3d-viewframe');
		var viewCopy=root.querySelector('.nlp3d-view-copy');
		var toolPanel=root.querySelector('.nlp3d-tool-panel');
		var toolButtons=[].slice.call(root.querySelectorAll('.nlp3d-tool'));
		var currentAngle=-32;
		var dragState=null;
		var activeTool='spec';
		function track(action,extra){
			window.dataLayer=window.dataLayer||[];
			var payload={event:'project_3d_interaction',action:action,card_id:parseInt(root.dataset.project,10)};
			if(extra){Object.keys(extra).forEach(function(k){payload[k]=extra[k]})}
			window.dataLayer.push(payload);
		}
		function floorHasUnits(f){return units.some(function(u){return parseInt(u.floor||0,10)===f})}
		function unitForFloor(f){return units.find(function(u){return parseInt(u.floor||0,10)===f&&u.status!=='sold'})||units.find(function(u){return parseInt(u.floor||0,10)===f})}
		function unitById(id){return units.find(function(u){return u.id===id})}
		function hasPoints(u){return u&&typeof u.points==='string'&&u.points.trim().split(/\s+/).length>=3}
		function renderTower(){
			tower.innerHTML='';
			var count=Math.max(22,Math.min(45,maxFloor));
			for(var i=1;i<=count;i++){
				var floor=Math.round(minFloor+((maxFloor-minFloor)*(i-1)/Math.max(1,count-1)));
				var b=document.createElement('div');
				b.className='nlp3d-plate'+(floorHasUnits(floor)?' has-units':'')+(floor===activeFloor?' is-active':'');
				var uf=unitForFloor(floor);
				if(uf&&uf.status==='sold'){b.className+=' is-sold'}
				b.style.setProperty('--i',i);
				b.style.bottom=(i*8)+'px';
				b.style.width=(72+Math.sin(i/3)*8)+'%';
				b.style.right=(14+Math.cos(i/4)*5)+'%';
				b.dataset.floor=floor;
				b.dataset.action='select-floor';
				b.title='קומה '+floor;
				b.setAttribute('role','button');
				b.setAttribute('tabindex','0');
				b.setAttribute('aria-label','בחרו קומה '+floor);
				b.addEventListener('click',function(e){e.stopPropagation();selectFloor(parseInt(this.dataset.floor,10))});
				b.addEventListener('keydown',function(e){if(e.key==='Enter'||e.key===' '){e.preventDefault();selectFloor(parseInt(this.dataset.floor,10))}});
				tower.appendChild(b);
			}
		}
		function renderFacade(){
			if(!hotspots){return}
			hotspots.innerHTML='';
			var any=false;
			units.filter(hasPoints).forEach(function(u){
				any=true;
				var poly=document.createElementNS('http://www.w3.org/2000/svg','polygon');
				poly.setAttribute('points',u.points);
				poly.setAttribute('class','nlp3d-hotspot nlp3d-status-'+u.status+(activeUnit&&u.id===activeUnit.id?' is-active':''));
				poly.setAttribute('tabindex','0');
				poly.setAttribute('role','button');
				poly.setAttribute('aria-label',selectedTitle(u)+' · '+statusLabel(u.status));
				poly.dataset.unit=u.id;
				poly.dataset.action='select-unit-facade';
				var t=document.createElementNS('http://www.w3.org/2000/svg','title');
				t.textContent=selectedTitle(u)+' · '+unitText(u);
				poly.appendChild(t);
				poly.addEventListener('click',function(e){e.stopPropagation();selectUnit(u.id,'facade')});
				poly.addEventListener('keydown',function(e){if(e.key==='Enter'||e.key===' '){e.preventDefault();selectUnit(u.id,'facade-keyboard')}});
				hotspots.appendChild(poly);
			});
			if(facade){facade.hidden=!any}
			scene.classList.toggle('has-facade',any);
		}
		function syncFacade(){
			root.querySelectorAll('.nlp3d-hotspot').forEach(function(p){p.classList.toggle('is-active',activeUnit&&p.dataset.unit===activeUnit.id)});
		}
		function renderFloors(){
			floorStrip.innerHTML='';
			floors.forEach(function(f){
				var b=document.createElement('button');
				b.type='button';
				b.className='nlp3d-floor'+(f===activeFloor?' is-active':'');
				b.textContent='קומה '+f;
				b.dataset.floor=f;
				b.dataset.action='select-floor';
				b.addEventListener('click',function(){selectFloor(parseInt(this.dataset.floor,10))});
				floorStrip.appendChild(b);
			});
		}
		function renderUnits(){
			unitList.innerHTML='';
			units.filter(function(u){return parseInt(u.floor||0,10)===activeFloor}).forEach(function(u){
				var b=document.createElement('button');
				b.type='button';
				b.className='nlp3d-unit-card nlp3d-status-'+u.status+(activeUnit&&u.id===activeUnit.id?' is-active':'')+(u.status==='sold'?' is-sold':'');
				b.innerHTML='<strong>'+selectedTitle(u)+'</strong><span>'+unitText(u)+' · '+statusLabel(u.status)+'</span>';
				b.dataset.unit=u.id;
				b.dataset.action='select-unit-card';
				b.addEventListener('click',function(){selectUnit(u.id,'card')});
				unitList.appendChild(b);
			});
		}
		function renderDetail(){
			if(!activeUnit){return}
			title.textContent=selectedTitle(activeUnit);
			facts.innerHTML='';
			detailRows(activeUnit,meta).forEach(function(row){
				var wrap=document.createElement('div');
				var dt=document.createElement('dt');
				var dd=document.createElement('dd');
				dt.textContent=row[0];
				dd.textContent=row[1];
				wrap.appendChild(dt);
				wrap.appendChild(dd);
				facts.appendChild(wrap);
			});
			if(activeUnit.plan){plan.href=activeUnit.plan;plan.hidden=false}else{plan.hidden=true}
			renderUnitView();
			renderToolPanel();
			ok.hidden=true;
			form.querySelectorAll('button[type="submit"]').forEach(function(b){b.disabled=false});
		}
		function renderToolPanel(){
			if(!toolPanel||!activeUnit){return}
			var headline='מפרט הדירה';
			var copy='הדירה שנבחרה מוצגת לפי נתוני ההמחשה: '+(activeUnit.rooms||'')+' חדרים, '+(activeUnit.sqm?fmt(activeUnit.sqm)+' מ"ר':'שטח לפי פנייה')+', קומה '+(activeUnit.floor||'לפי פנייה')+', '+(activeUnit.building||'בניין לפי פנייה')+'. '+(activeUnit.note||'מפרט רשמי יימסר לאחר בדיקת זמינות מול היזם.');
			if(activeTool==='drawing'){
				headline='תוכנית ומדידות';
				copy=activeUnit.plan?'ניתן לפתוח את תוכנית הדירה המקושרת ולבקש בדיקה של המידות, המרפסת והכיוונים.':'תוכנית רשמית עדיין לא נטענה לכרטיס. אפשר לשלוח בקשה ולקבל תוכנית, מדידות, כיווני אוויר וחומר מכירה כאשר הם זמינים ומאומתים. המערכת כבר שומרת את היחידה, הקומה והקו כדי לקשור אליהם תוכנית רשמית בהמשך.';
			}
			if(activeTool==='advisors'){
				headline='ליווי מקצועי';
				copy='אפשר לבקש לצרף עורך דין רכישה, יועץ משכנתאות, בדק בית או מעצב פנים. הבקשה תישלח עם הדירה שנבחרה, כולל קומה, שטח, כיוון ונוף, כדי לחזור אליכם עם ליווי מתאים לפני כל התחייבות.';
			}
			toolPanel.innerHTML='';
			var strong=document.createElement('strong');
			var p=document.createElement('p');
			strong.textContent=headline;
			p.textContent=copy;
			toolPanel.appendChild(strong);
			toolPanel.appendChild(p);
		}
		function renderUnitView(){
			if(!viewCopy||!activeUnit){return}
			var view=activeUnit.view||activeUnit.dir||'הסביבה הקרובה';
			var cam=cameraParams(activeUnit,meta);
			var cameraNote=(cam.lat&&cam.lng)?(' פרמטרי המבט נשמרים להכנת תצוגת תלת ממד: גובה '+cam.altitude_m+' מ׳, כיוון '+cam.bearing+'°.'):'';
			viewCopy.textContent='מבט המחשה מהיחידה: '+view+'. זהו מצב תצוגה תכנוני עד שיוזנו הדמיות ותוכניות מאושרות.'+cameraNote;
			if(viewFrame){viewFrame.dataset.view=(activeUnit.view||'city').toLowerCase()}
		}
		function setAngle(angle){
			currentAngle=Math.max(-68,Math.min(68,angle));
			scene.style.setProperty('--angle',currentAngle+'deg');
		}
		function selectFloor(f){
			activeFloor=f;
			var next=unitForFloor(f);
			if(next){activeUnit=next}
			renderAll(false);
			track('select_floor',{floor:f,unit:activeUnit&&activeUnit.id});
		}
		function selectUnit(id,source){
			var next=unitById(id);
			if(next){activeUnit=next;activeFloor=parseInt(next.floor||activeFloor,10)}
			renderAll(false);
			track('select_unit',{floor:activeFloor,unit:id,source:source||'unknown'});
		}
		function renderAll(includeTower){
			if(includeTower){renderTower();renderFacade()}else{root.querySelectorAll('.nlp3d-plate').forEach(function(p){p.classList.toggle('is-active',parseInt(p.dataset.floor,10)===activeFloor)});syncFacade()}
			renderFloors();
			renderUnits();
			renderDetail();
		}
		root.querySelectorAll('.nlp3d-angle').forEach(function(b){
			b.addEventListener('click',function(){
				root.querySelectorAll('.nlp3d-angle').forEach(function(x){x.classList.remove('is-active')});
				b.classList.add('is-active');
				setAngle(parseFloat(b.dataset.angle||'-32'));
				scene.classList.remove('is-orbit');
				var orbit=root.querySelector('.nlp3d-orbit');
				if(orbit){orbit.classList.remove('is-active')}
				track('angle',{angle:b.textContent});
			});
		});
		var orbit=root.querySelector('.nlp3d-orbit');
		if(orbit){orbit.addEventListener('click',function(){scene.classList.toggle('is-orbit');orbit.classList.toggle('is-active');track('orbit',{active:scene.classList.contains('is-orbit')})})}
		if(viewToggle&&viewFrame){
			viewToggle.addEventListener('click',function(){
				viewFrame.hidden=!viewFrame.hidden;
				viewToggle.classList.toggle('is-active',!viewFrame.hidden);
				renderUnitView();
				track('view_from_unit',{unit:activeUnit&&activeUnit.id,open:!viewFrame.hidden});
			});
		}
		toolButtons.forEach(function(b){
			b.addEventListener('click',function(){
				activeTool=b.dataset.tool||'spec';
				toolButtons.forEach(function(x){x.classList.toggle('is-active',x===b)});
				renderToolPanel();
				track('tool_panel',{tool:activeTool,unit:activeUnit&&activeUnit.id});
			});
		});
		scene.addEventListener('pointerdown',function(e){
			if(e.target.closest('button,a,input,.nlp3d-hotspot')){return}
			dragState={x:e.clientX,angle:currentAngle,id:e.pointerId};
			scene.classList.add('is-dragging');
			scene.classList.remove('is-orbit');
			if(orbit){orbit.classList.remove('is-active')}
			if(scene.setPointerCapture){scene.setPointerCapture(e.pointerId)}
		});
		scene.addEventListener('pointermove',function(e){
			if(!dragState){return}
			setAngle(dragState.angle+(e.clientX-dragState.x)*0.22);
		});
		function endDrag(e){
			if(!dragState){return}
			if(scene.releasePointerCapture){try{scene.releasePointerCapture(dragState.id)}catch(err){}}
			dragState=null;
			scene.classList.remove('is-dragging');
		}
		scene.addEventListener('pointerup',endDrag);
		scene.addEventListener('pointercancel',endDrag);
		form.addEventListener('submit',function(e){
			e.preventDefault();
			if(!activeUnit){return}
			var submitter=e.submitter || form.querySelector('.nlp3d-send');
			var intent=submitter&&submitter.dataset.intent==='purchase'?'purchase':'callback';
			var fd=new FormData(form);
			var intentText=intent==='purchase'?'בדיקת רכישה ושמירה':'בקשת שיחה';
			var advisor=fd.get('advisor')||'לא נבחר';
			var timeline=fd.get('timeline')||'לא נמסר';
			var cam=cameraParams(activeUnit,meta);
			var reservationState=intent==='purchase'?'non_binding_inquiry':'lead_request';
			var message=intentText+' מתוך מודל תלת ממדי של '+(meta.title||'הפרויקט')+'. יחידה: '+selectedTitle(activeUnit)+'. '+unitText(activeUnit)+'. בניין: '+(activeUnit.building||'לא נמסר')+'. זמינות: '+(activeUnit.availability||'לא מאומתת')+'. תקציב: '+(fd.get('budget')||'לא נמסר')+'. מועד התקדמות: '+timeline+'. ליווי מבוקש: '+advisor+'. נא לאמת זמינות, מחיר ותנאים מול היזם לפני כל התקדמות. סטטוס: '+reservationState+'.';
			var payload={card_id:parseInt(root.dataset.project,10),name:fd.get('name'),phone:fd.get('phone'),email:fd.get('email'),goal:intentText,message:message,company:fd.get('company'),source:'project_3d',budget:fd.get('budget'),unit:activeUnit.id,floor:activeUnit.floor,rooms:activeUnit.rooms,sqm:activeUnit.sqm,building:activeUnit.building||'',availability:activeUnit.availability||'',market_note:activeUnit.market_note||'',timeline:timeline,advisor:advisor,purchase_intent:intent==='purchase',reservation_state:reservationState,view_bearing:cam.bearing,view_altitude_m:cam.altitude_m};
			track('submit',{intent:intent,unit:activeUnit.id,floor:activeUnit.floor,advisor:advisor,reservation_state:reservationState,view_bearing:cam.bearing,view_altitude_m:cam.altitude_m});
			form.querySelectorAll('button[type="submit"]').forEach(function(b){b.disabled=true});
			ok.textContent='שולחים את הפנייה...';
			ok.hidden=false;
			fetch('__NLP3D_REST__',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(payload)})
				.then(function(r){if(!r.ok){throw new Error('lead failed')}return r.json()})
				.then(function(){ok.textContent='קיבלנו את הפנייה. נציג יחזור אליך בתוך 24 שעות עם בדיקת זמינות ונתונים מאומתים.'})
				.catch(function(){ok.textContent='השליחה נכשלה. אפשר לנסות שוב או לפנות דרך כפתור יצירת הקשר באתר.';form.querySelectorAll('button[type="submit"]').forEach(function(b){b.disabled=false})});
		});
		renderAll(true);
	}
	function boot(){document.querySelectorAll('.nlp3d-premium').forEach(init)}
	if(document.readyState==='loading'){document.addEventListener('DOMContentLoaded',boot)}else{boot()}
})();
JS;
		return str_replace( '__NLP3D_REST__', esc_js( $rest_url ), $js );
	}
}

add_action(
	'wp_enqueue_scripts',
	function () {
		if ( ! nadlan_p3d_enabled() ) {
			return;
		}

		wp_register_style( 'nadlan-p3d', '', array(), '1.59.2' );
		wp_enqueue_style( 'nadlan-p3d' );
		wp_add_inline_style( 'nadlan-p3d', nadlan_p3d_inline_css() );
		wp_add_inline_style( 'nadlan-p3d', '.nlp3d-drag-note{display:inline-flex;align-items:center;min-height:44px;color:rgba(246,239,226,.72);font-size:12px;padding:0 6px}.nlp3d-scene{touch-action:none;cursor:grab}.nlp3d-scene.is-dragging{cursor:grabbing}.nlp3d-actions{grid-template-columns:1fr}.nlp3d-view-toggle{margin-top:12px;border:1px solid rgba(234,216,163,.36);background:rgba(255,255,255,.06);color:#ffe8a6;padding:9px 12px;cursor:pointer}.nlp3d-view-toggle.is-active{background:rgba(234,216,163,.18);color:#fff}.nlp3d-viewframe{position:relative;margin-top:12px;min-height:150px;overflow:hidden;border:1px solid rgba(234,216,163,.18);background:linear-gradient(180deg,rgba(41,112,139,.58),rgba(8,25,25,.92));isolation:isolate}.nlp3d-view-sky{position:absolute;inset:0;background:radial-gradient(circle at 18% 22%,rgba(255,255,255,.24),transparent 18%),linear-gradient(135deg,rgba(39,107,130,.42),rgba(18,50,43,.1));opacity:.86}.nlp3d-view-lines{position:absolute;inset:auto -8% 18% -8%;height:46%;border-top:1px solid rgba(234,216,163,.28);background:linear-gradient(160deg,rgba(234,216,163,.1),transparent 54%);transform:skewY(-8deg)}.nlp3d-view-copy{position:absolute;right:14px;left:14px;bottom:12px;margin:0;color:#fff8dc;font-size:13px;line-height:1.5;text-shadow:0 1px 12px rgba(0,0,0,.55)}@media(max-width:600px){.nlp3d-drag-note{flex-basis:100%;min-height:24px}.nlp3d-viewframe{min-height:130px}}' );
		wp_add_inline_style( 'nadlan-p3d', nadlan_p3d_experience_css() );
		wp_add_inline_style( 'nadlan-p3d', '.nlp3d-facade{position:absolute;z-index:6;inset:58px 13% 54px;margin:0;display:block;border:1px solid rgba(234,216,163,.22);background:linear-gradient(135deg,rgba(4,16,18,.44),rgba(255,255,255,.04));box-shadow:0 24px 64px rgba(0,0,0,.34);overflow:hidden;pointer-events:none}.nlp3d-facade[hidden]{display:none}.nlp3d-facade img{display:block;width:100%;height:100%;object-fit:cover;filter:saturate(.82) contrast(1.08) sepia(.08);opacity:.86}.nlp3d-facade:after{content:"";position:absolute;inset:0;background:linear-gradient(180deg,rgba(234,216,163,.08),transparent 34%,rgba(0,0,0,.22));pointer-events:none}.nlp3d-facade figcaption{position:absolute;right:10px;bottom:9px;left:10px;z-index:3;color:#fff3c6;font-size:11px;line-height:1.4;text-shadow:0 1px 10px rgba(0,0,0,.72)}.nlp3d-facade-hotspots{position:absolute;z-index:2;inset:0;width:100%;height:100%;pointer-events:auto}.nlp3d-hotspot{fill:rgba(234,216,163,.08);stroke:rgba(234,216,163,.64);stroke-width:2;vector-effect:non-scaling-stroke;cursor:pointer;transition:fill .16s,stroke .16s,filter .16s}.nlp3d-hotspot:hover,.nlp3d-hotspot:focus-visible{fill:rgba(234,216,163,.24);stroke:#fff2ba;outline:none;filter:drop-shadow(0 0 8px rgba(234,216,163,.42))}.nlp3d-hotspot.is-active{fill:rgba(234,216,163,.34);stroke:#fff2ba;filter:drop-shadow(0 0 14px rgba(234,216,163,.5))}.nlp3d-scene.has-facade .nlp3d-tower{opacity:.34}.nlp3d-deal-steps{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:6px;margin-top:12px}.nlp3d-deal-steps span{min-height:32px;display:flex;align-items:center;justify-content:center;border:1px solid rgba(234,216,163,.18);background:rgba(255,255,255,.045);color:#fff3c8;font-size:12px}.nlp3d-deal-steps span:first-child{background:rgba(234,216,163,.16);border-color:rgba(234,216,163,.36)}@media(max-width:900px){.nlp3d-facade{inset:62px 8% 42px}}@media(max-width:600px){.nlp3d-facade{inset:70px 7% 34px}.nlp3d-deal-steps{grid-template-columns:repeat(2,minmax(0,1fr))}}' );
		wp_add_inline_style( 'nadlan-p3d', '.entry-content>.nlp3d,.wp-block-post-content>.nlp3d{width:min(1280px,calc(100vw - 36px));margin-inline:calc(50% - min(640px,calc(50vw - 18px)));overflow:clip}.nlp3d-shell{grid-template-columns:minmax(220px,.72fr) minmax(520px,1.45fr);grid-template-areas:"copy stage" "console stage";align-items:start;min-height:0;padding:28px}.nlp3d-copy{grid-area:copy;align-self:start;padding-bottom:0}.nlp3d-stage-wrap{grid-area:stage;min-height:760px}.nlp3d-console{grid-area:console;min-width:0}.nlp3d h2{max-width:15ch;font-size:clamp(28px,3vw,46px)}.nlp3d-lead-text{font-size:15px;line-height:1.65}.nlp3d-facade{inset:72px 5% 58px;display:flex;align-items:center;justify-content:center;background:radial-gradient(circle at 50% 32%,rgba(234,216,163,.08),transparent 42%),rgba(4,16,18,.55)}.nlp3d-facade img{object-fit:contain;object-position:center center;padding:12px;opacity:.97}.nlp3d-facade-hotspots{inset:12px;width:calc(100% - 24px);height:calc(100% - 24px)}.nlp3d-scene.has-facade .nlp3d-tower{opacity:.18}.nlp3d-detail{max-height:none}.nlp3d-facts{grid-template-columns:repeat(2,minmax(0,1fr));max-height:360px;overflow:auto;padding-inline-end:4px}.nlp3d-facts div:nth-last-child(-n+2){grid-column:1/-1}.nlp3d-facts dd{overflow-wrap:anywhere}.nlp3d-lead-form input,.nlp3d-lead-form select{min-width:0}.nlp3d-actions{gap:8px}.nlp3d-tool-panel{max-height:170px;overflow:auto}.nlp3d-tower:before{content:"";position:absolute;inset:-8px 6%;border:1px solid rgba(234,216,163,.22);background:linear-gradient(90deg,rgba(234,216,163,.05),transparent 45%,rgba(234,216,163,.08));transform:translateZ(-18px)}.nlp3d-plate{border-radius:2px}.nlp3d-plate:after{content:"";position:absolute;inset:3px 12%;background:repeating-linear-gradient(90deg,rgba(234,216,163,.45) 0 6px,transparent 6px 13px);opacity:.42}@media(max-width:1180px){.nlp3d-shell{grid-template-columns:1fr;grid-template-areas:"copy" "stage" "console"}.nlp3d-stage-wrap{min-height:680px}.nlp3d h2{max-width:100%}.nlp3d-lead-text{max-width:62ch}.nlp3d-console{display:grid;grid-template-columns:minmax(220px,.68fr) minmax(320px,1fr);align-items:start}.nlp3d-console-head,.nlp3d-floor-strip,.nlp3d-units{grid-column:1}.nlp3d-detail,.nlp3d-lead-form{grid-column:2}.nlp3d-detail{grid-row:1 / span 3}.nlp3d-lead-form{grid-row:4}}@media(max-width:760px){.entry-content>.nlp3d,.wp-block-post-content>.nlp3d{width:calc(100vw - 18px);margin-inline:calc(50% - 50vw + 9px)}.nlp3d-shell{padding:16px}.nlp3d-stage-wrap{min-height:560px}.nlp3d-scene{height:540px}.nlp3d-facade{inset:64px 3% 46px}.nlp3d-facade img{padding:6px}.nlp3d-facade-hotspots{inset:6px;width:calc(100% - 12px);height:calc(100% - 12px)}.nlp3d-console{display:flex}.nlp3d-facts{grid-template-columns:1fr;max-height:none}.nlp3d-facts div:nth-last-child(-n+2){grid-column:auto}.nlp3d-toolbar{position:relative;top:auto;right:auto;margin-bottom:10px}.nlp3d-scene{position:relative}.nlp3d-copy{padding-inline:2px}.nlp3d-shop-path span{font-size:12px}}@media(max-width:420px){.nlp3d-stage-wrap{min-height:500px}.nlp3d-scene{height:500px}.nlp3d h2{font-size:28px}.nlp3d-metrics span{width:100%}}' );

		wp_register_script( 'nadlan-p3d', '', array(), '1.59.2', true );
		wp_enqueue_script( 'nadlan-p3d' );
		wp_add_inline_script( 'nadlan-p3d', nadlan_p3d_inline_js( esc_url_raw( rest_url( 'nadlan/v1/lead' ) ) ) );
	}
);

add_filter(
	'the_content',
	function ( $content ) {
		if ( ! nadlan_p3d_enabled() || ! is_singular( 'nadlan_project' ) || ! in_the_loop() || ! is_main_query() ) {
			return $content;
		}

		$pid = get_the_ID();
		if ( ! nadlan_p3d_has_data( $pid ) ) {
			return $content;
		}

		return nadlan_p3d_insert_after_project_header( $content, nadlan_p3d_render( $pid ) );
	},
	6
);

add_action(
	'add_meta_boxes',
	function () {
		if ( ! nadlan_p3d_enabled() ) {
			return;
		}

		add_meta_box(
			'nadlan-p3d',
			'בחירת דירות אינטראקטיבית',
			function ( $post ) {
				wp_nonce_field( 'nadlan_p3d_save', 'nadlan_p3d_nonce' );
				$img = esc_attr( (string) get_post_meta( $post->ID, 'project_3d_image', true ) );
				$vb  = esc_attr( (string) get_post_meta( $post->ID, 'project_3d_viewbox', true ) );
				$fh  = esc_attr( (string) get_post_meta( $post->ID, 'project_3d_floor_height_m', true ) );
				$gm  = esc_attr( (string) get_post_meta( $post->ID, 'project_3d_ground_elevation_m', true ) );
				$js  = esc_textarea( (string) get_post_meta( $post->ID, 'project_3d_units', true ) );
				$dm  = get_post_meta( $post->ID, 'project_3d_demo', true ) === '1';
				echo '<p><label>כתובת תמונת מקור או הדמיה מאושרת<br><input type="url" name="project_3d_image" value="' . $img . '" class="widefat"></label></p>';
				echo '<p><label>viewBox למצב שכבת SVG ישנה, אם קיים<br><input type="text" name="project_3d_viewbox" value="' . $vb . '" class="widefat"></label></p>';
				echo '<p><label>גובה קומה במטרים לחישוב מבט מהדירה<br><input type="number" step="0.01" min="2.4" max="5" name="project_3d_floor_height_m" value="' . $fh . '" class="widefat" placeholder="3.05"></label></p>';
				echo '<p><label>גובה קרקע משוער במטרים, אם ידוע<br><input type="number" step="0.1" min="-50" max="400" name="project_3d_ground_elevation_m" value="' . $gm . '" class="widefat" placeholder="0"></label></p>';
				echo '<p><label>יחידות JSON: id, title, floor, rooms, sqm, balcony, dir, line, view, price, status, plan<br><textarea name="project_3d_units" rows="10" class="widefat code">' . $js . '</textarea></label></p>';
				echo '<p><label><input type="checkbox" name="project_3d_demo" value="1" ' . checked( $dm, true, false ) . '> הצג מודל הדגמה כאשר אין מלאי רשמי</label></p>';
				echo '<p class="description">במצב הדגמה המחיר מוצג "לפי פנייה" כדי לא להציג נתוני מכירה לא מאומתים.</p>';
			},
			'nadlan_project',
			'normal'
		);
	}
);

add_action(
	'save_post_nadlan_project',
	function ( $post_id ) {
		if ( ! isset( $_POST['nadlan_p3d_nonce'] ) || ! wp_verify_nonce( $_POST['nadlan_p3d_nonce'], 'nadlan_p3d_save' ) ) {
			return;
		}
		if ( defined( 'DOING_AUTOSAVE' ) && DOING_AUTOSAVE ) {
			return;
		}
		if ( ! current_user_can( 'edit_post', $post_id ) ) {
			return;
		}

		update_post_meta( $post_id, 'project_3d_image', esc_url_raw( wp_unslash( $_POST['project_3d_image'] ?? '' ) ) );
		update_post_meta( $post_id, 'project_3d_viewbox', sanitize_text_field( wp_unslash( $_POST['project_3d_viewbox'] ?? '' ) ) );
		update_post_meta( $post_id, 'project_3d_floor_height_m', nadlan_p3d_sanitize_decimal( wp_unslash( $_POST['project_3d_floor_height_m'] ?? '' ) ) );
		update_post_meta( $post_id, 'project_3d_ground_elevation_m', nadlan_p3d_sanitize_decimal( wp_unslash( $_POST['project_3d_ground_elevation_m'] ?? '' ) ) );
		$units = (string) wp_unslash( $_POST['project_3d_units'] ?? '' );
		update_post_meta( $post_id, 'project_3d_units', json_decode( $units ) !== null || $units === '' ? $units : '' );
		update_post_meta( $post_id, 'project_3d_demo', ! empty( $_POST['project_3d_demo'] ) ? '1' : '0' );
	}
);

add_filter(
	'nadlan_config_healthcheck',
	function ( $out ) {
		$q = new WP_Query(
			array(
				'post_type'      => 'nadlan_project',
				'post_status'    => 'any',
				'fields'         => 'ids',
				'posts_per_page' => 1,
				'meta_query'     => array(
					'relation' => 'OR',
					array( 'key' => 'project_3d_units', 'compare' => 'EXISTS' ),
					array( 'key' => 'project_3d_demo', 'value' => '1' ),
				),
			)
		);
		$out['project_3d'] = array(
			'enabled'          => nadlan_p3d_enabled(),
			'renderer'         => 'premium_tower_picker_v3',
			'lead_endpoint'    => '/nadlan/v1/lead',
			'facade_polygons'  => true,
			'lead_unit_payload' => true,
			'view_from_unit_seam' => 'cesium_ready',
			'reservation_state' => 'non_binding_inquiry',
			'projects_with_3d' => (int) $q->found_posts,
		);
		wp_reset_postdata();
		return $out;
	}
);
