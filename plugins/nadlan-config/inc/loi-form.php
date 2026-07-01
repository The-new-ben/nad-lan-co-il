<?php
/**
 * NadLan Non-Binding Offer Letter (LOI) form.
 *
 * The buyer-journey "buying moment": a buyer submits a non-binding purchase
 * offer on a project/unit. Origin: Codex's buyer-journey branch
 * (codex/buyer-journey-fixes-2026-07-01). This is the cleaned, review-passed
 * version -- Codex's original handler returned a fake success and saved NOTHING
 * ("In a real implementation, this would save..."), which would silently drop
 * every real offer. This version actually persists the offer through the
 * existing lead pipeline (nadlan_lead_e2e_capture -> nadlan_lead CPT + routing),
 * with a direct-insert fallback so an offer is NEVER lost. Styling retokened to
 * the luxury design system (gold #9C7A3C, radius 2px, hairlines).
 *
 * Shortcode: [nadlan_loi_form project_id="123" unit_id="unit-38"]
 */
if ( ! defined( 'ABSPATH' ) ) {
	exit;
}

add_shortcode( 'nadlan_loi_form', 'nadlan_render_loi_form' );

function nadlan_render_loi_form( $atts ) {
	$atts = shortcode_atts(
		array(
			'project_id' => get_the_ID(),
			'unit_id'    => '',
		),
		$atts,
		'nadlan_loi_form'
	);

	ob_start();
	?>
	<div class="nl-loi-container" id="nl-loi-form-wrapper">
		<h3>הגשת הצעת רכישה לא מחייבת</h3>
		<p>השלב הראשון לרכישת הדירה. ההצעה אינה חוזה מחייב, ומותנית בחתימה על הסכם מכר סופי מול היזם. הפרטים יועברו לנציג הפרויקט לצורך המשך התהליך.</p>

		<form id="nl-loi-form" method="post">
			<input type="hidden" name="action" value="nadlan_submit_loi">
			<input type="hidden" name="nonce" value="<?php echo esc_attr( wp_create_nonce( 'nadlan_loi_nonce' ) ); ?>">
			<input type="hidden" name="project_id" value="<?php echo esc_attr( $atts['project_id'] ); ?>">
			<input type="hidden" name="unit_id" id="nl-loi-unit-id" value="<?php echo esc_attr( $atts['unit_id'] ); ?>">

			<div class="nl-form-row">
				<div class="nl-form-group">
					<label for="nl-loi-name">שם מלא (כפי שמופיע בתעודת זהות)</label>
					<input type="text" id="nl-loi-name" name="full_name" autocomplete="name" required>
				</div>
				<div class="nl-form-group">
					<label for="nl-loi-id">ת.ז / דרכון</label>
					<input type="text" id="nl-loi-id" name="id_number" inputmode="numeric" required>
				</div>
			</div>

			<div class="nl-form-row">
				<div class="nl-form-group">
					<label for="nl-loi-phone">טלפון נייד</label>
					<input type="tel" id="nl-loi-phone" name="phone" autocomplete="tel" required>
				</div>
				<div class="nl-form-group">
					<label for="nl-loi-email">דואר אלקטרוני</label>
					<input type="email" id="nl-loi-email" name="email" autocomplete="email" required>
				</div>
			</div>

			<div class="nl-form-row">
				<div class="nl-form-group">
					<label for="nl-loi-offer">הצעת מחיר (₪) — לא חובה</label>
					<input type="number" id="nl-loi-offer" name="offer_price" min="0" step="10000" inputmode="numeric">
				</div>
				<div class="nl-form-group">
					<label for="nl-loi-mortgage">אישור עקרוני למשכנתא?</label>
					<select id="nl-loi-mortgage" name="mortgage_status">
						<option value="yes">כן, יש ברשותי אישור עקרוני בתוקף</option>
						<option value="no">לא, טרם הוצאתי אישור / רוכש הון עצמי</option>
						<option value="process">בתהליך הוצאת אישור עקרוני</option>
					</select>
				</div>
			</div>

			<div class="nl-form-checkbox">
				<input type="checkbox" id="nl-loi-terms" name="terms_agreed" required>
				<label for="nl-loi-terms">אני מאשר/ת את <a href="/terms/" target="_blank" rel="noopener">תנאי השימוש</a> ואת העברת פרטיי ליזם/לקבלן לצורך המשך הליך הרכישה.</label>
			</div>

			<div class="nl-form-checkbox">
				<input type="checkbox" id="nl-loi-marketing" name="marketing_agreed">
				<label for="nl-loi-marketing">אני מאשר/ת קבלת עדכונים והצעות נדל״ן (לא חובה).</label>
			</div>

			<button type="submit" class="nl-loi-submit">הגשת הצעת רכישה ליזם</button>
			<p class="nl-loi-response" id="nl-loi-response" role="status" aria-live="polite"></p>
		</form>
	</div>

	<style>
		.nl-loi-container {
			background: #14130F;
			color: #FAF7F1;
			padding: clamp(20px, 3vw, 34px);
			border-radius: 2px;
			border: 1px solid #9C7A3C;
			max-width: 800px;
			margin: 2rem auto;
			font-family: "Heebo", Arial, sans-serif;
			direction: rtl;
		}
		.nl-loi-container h3 {
			color: #B89154;
			font-family: "Frank Ruhl Libre", Georgia, serif;
			font-weight: 500;
			margin: 0 0 10px;
			font-size: clamp(1.4rem, 2vw, 1.8rem);
		}
		.nl-loi-container > p {
			color: #C9C3B7;
			line-height: 1.7;
			margin: 0 0 20px;
			font-size: 0.95rem;
		}
		.nl-form-row {
			display: flex;
			gap: 1rem;
			margin-bottom: 1rem;
		}
		.nl-form-group {
			flex: 1;
			display: flex;
			flex-direction: column;
			min-width: 0;
		}
		.nl-form-group label {
			font-size: 0.9rem;
			margin-bottom: 0.5rem;
			color: #E0DCD3;
		}
		.nl-form-group input,
		.nl-form-group select {
			min-height: 46px;
			padding: 0.6rem 0.75rem;
			background: #211F19;
			border: 1px solid #3A362E;
			color: #fff;
			border-radius: 2px;
			font: inherit;
		}
		.nl-form-group input:focus,
		.nl-form-group select:focus {
			outline: 2px solid rgba(156, 122, 60, .4);
			outline-offset: 1px;
			border-color: #9C7A3C;
		}
		.nl-form-checkbox {
			margin-bottom: 1rem;
			display: flex;
			align-items: flex-start;
			gap: 0.5rem;
			font-size: 0.85rem;
			color: #C9C3B7;
		}
		.nl-form-checkbox a { color: #B89154; }
		.nl-loi-submit {
			background: #9C7A3C;
			color: #14130F;
			border: 0;
			min-height: 50px;
			padding: 0 2rem;
			font: inherit;
			font-weight: 700;
			cursor: pointer;
			border-radius: 2px;
			width: 100%;
		}
		.nl-loi-submit:hover { background: #B89154; }
		.nl-loi-submit[disabled] { opacity: .6; cursor: default; }
		.nl-loi-response {
			margin-top: 1rem;
			padding: 0.85rem 1rem;
			border-radius: 2px;
			display: none;
		}
		.nl-loi-response.is-success {
			display: block;
			background: rgba(63, 107, 74, .18);
			border: 1px solid #3F6B4A;
			color: #cfe6d3;
		}
		.nl-loi-response.is-error {
			display: block;
			background: rgba(139, 58, 46, .18);
			border: 1px solid #8B3A2E;
			color: #f2cfc8;
		}
		@media (max-width: 768px) {
			.nl-form-row { flex-direction: column; gap: 0; }
			.nl-form-row .nl-form-group { margin-bottom: 1rem; }
		}
	</style>

	<script>
		(function () {
			var form = document.getElementById("nl-loi-form");
			if (!form) return;
			form.addEventListener("submit", function (e) {
				e.preventDefault();
				var btn = form.querySelector(".nl-loi-submit");
				var resp = document.getElementById("nl-loi-response");
				if (btn) { btn.disabled = true; }
				fetch("<?php echo esc_url( admin_url( 'admin-ajax.php' ) ); ?>", {
					method: "POST",
					body: new FormData(form),
					credentials: "same-origin"
				})
				.then(function (r) { return r.json(); })
				.then(function (data) {
					if (data && data.success) {
						resp.className = "nl-loi-response is-success";
						resp.textContent = (data.data && data.data.message) || "ההצעה התקבלה.";
						form.reset();
					} else {
						resp.className = "nl-loi-response is-error";
						resp.textContent = (data && data.data && data.data.message) || "אירעה שגיאה. אנא נסו שוב.";
						if (btn) { btn.disabled = false; }
					}
				})
				.catch(function () {
					resp.className = "nl-loi-response is-error";
					resp.textContent = "אירעה שגיאה. אנא נסו שוב מאוחר יותר.";
					if (btn) { btn.disabled = false; }
				});
			});
		})();
	</script>
	<?php
	return ob_get_clean();
}

add_action( 'wp_ajax_nadlan_submit_loi', 'nadlan_handle_loi_submission' );
add_action( 'wp_ajax_nopriv_nadlan_submit_loi', 'nadlan_handle_loi_submission' );

function nadlan_handle_loi_submission() {
	if ( ! check_ajax_referer( 'nadlan_loi_nonce', 'nonce', false ) ) {
		wp_send_json_error( array( 'message' => 'פג תוקף הטופס. רעננו את הדף ונסו שוב.' ) );
	}

	$full_name  = sanitize_text_field( wp_unslash( $_POST['full_name'] ?? '' ) );
	$email      = sanitize_email( wp_unslash( $_POST['email'] ?? '' ) );
	$phone      = sanitize_text_field( wp_unslash( $_POST['phone'] ?? '' ) );
	$id_number  = sanitize_text_field( wp_unslash( $_POST['id_number'] ?? '' ) );
	$offer_raw  = isset( $_POST['offer_price'] ) ? preg_replace( '/[^0-9]/', '', (string) wp_unslash( $_POST['offer_price'] ) ) : '';
	$mortgage   = sanitize_text_field( wp_unslash( $_POST['mortgage_status'] ?? '' ) );
	$project_id = absint( wp_unslash( $_POST['project_id'] ?? 0 ) );
	$unit_id    = sanitize_text_field( wp_unslash( $_POST['unit_id'] ?? '' ) );
	$marketing  = ! empty( $_POST['marketing_agreed'] );

	if ( $full_name === '' || $phone === '' || $email === '' ) {
		wp_send_json_error( array( 'message' => 'אנא מלאו שם, טלפון ודוא״ל.' ) );
	}

	$mortgage_label = array(
		'yes'     => 'יש אישור עקרוני בתוקף',
		'no'      => 'אין אישור / רוכש הון עצמי',
		'process' => 'בתהליך הוצאת אישור',
	);
	$offer_display = $offer_raw !== '' ? number_format_i18n( (int) $offer_raw ) . ' ₪' : 'לא צוינה';

	$message_lines = array(
		'הצעת רכישה לא מחייבת (LOI).',
		'ת.ז / דרכון: ' . ( $id_number !== '' ? $id_number : '—' ),
		'הצעת מחיר: ' . $offer_display,
		'משכנתא: ' . ( $mortgage_label[ $mortgage ] ?? '—' ),
		'דירה: ' . ( $unit_id !== '' ? $unit_id : '—' ),
		'שיווק: ' . ( $marketing ? 'אישר עדכונים' : 'לא אישר' ),
	);

	$fields = array(
		'name'    => $full_name,
		'phone'   => $phone,
		'email'   => $email,
		'goal'    => 'LOI',
		'message' => implode( "\n", $message_lines ),
	);

	$saved = false;

	// Preferred path: the real end-to-end lead pipeline (dedupe + routing + audit).
	if ( function_exists( 'nadlan_lead_e2e_enabled' ) && nadlan_lead_e2e_enabled() && function_exists( 'nadlan_lead_e2e_capture' ) ) {
		$result = nadlan_lead_e2e_capture( $fields, $project_id, 'loi_form' );
		if ( ! is_wp_error( $result ) ) {
			$saved   = true;
			$lead_id = is_array( $result ) && ! empty( $result['lead_id'] ) ? (int) $result['lead_id'] : 0;
			nadlan_loi_attach_meta( $lead_id, compact( 'id_number', 'offer_raw', 'mortgage', 'unit_id', 'project_id', 'marketing' ) );
		}
	}

	// Fallback: never lose a real offer. Insert directly into the nadlan_lead CPT.
	if ( ! $saved ) {
		$lead_id = wp_insert_post(
			array(
				'post_type'   => 'nadlan_lead',
				'post_status' => 'private',
				'post_title'  => $full_name . ' - LOI - ' . current_time( 'Y-m-d H:i' ),
				'post_content'=> implode( "\n", $message_lines ),
			),
			true
		);
		if ( is_wp_error( $lead_id ) ) {
			wp_send_json_error( array( 'message' => 'אירעה שגיאה בשמירת ההצעה. אנא נסו שוב.' ) );
		}
		update_post_meta( $lead_id, 'name', $full_name );
		update_post_meta( $lead_id, 'phone', $phone );
		update_post_meta( $lead_id, 'email', $email );
		update_post_meta( $lead_id, 'goal', 'LOI' );
		nadlan_loi_attach_meta( (int) $lead_id, compact( 'id_number', 'offer_raw', 'mortgage', 'unit_id', 'project_id', 'marketing' ) );
	}

	wp_send_json_success( array( 'message' => 'הצעת הרכישה התקבלה. נציג הפרויקט יצור קשר בהקדם.' ) );
}

/**
 * Attach LOI-specific meta to a lead post (real offer data, so it's never lost).
 */
function nadlan_loi_attach_meta( $lead_id, $data ) {
	if ( ! $lead_id ) {
		return;
	}
	update_post_meta( $lead_id, 'lead_type', 'loi' );
	if ( ! empty( $data['id_number'] ) ) { update_post_meta( $lead_id, 'loi_id_number', $data['id_number'] ); }
	if ( ! empty( $data['offer_raw'] ) ) { update_post_meta( $lead_id, 'loi_offer_price', (int) $data['offer_raw'] ); }
	if ( ! empty( $data['mortgage'] ) ) { update_post_meta( $lead_id, 'loi_mortgage_status', $data['mortgage'] ); }
	if ( ! empty( $data['unit_id'] ) ) { update_post_meta( $lead_id, 'loi_unit_id', $data['unit_id'] ); }
	if ( ! empty( $data['project_id'] ) ) { update_post_meta( $lead_id, 'loi_project_id', (int) $data['project_id'] ); }
	update_post_meta( $lead_id, 'loi_marketing_opt_in', ! empty( $data['marketing'] ) ? '1' : '0' );
}
