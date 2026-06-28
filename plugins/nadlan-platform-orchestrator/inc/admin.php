<?php
if ( ! defined( 'ABSPATH' ) ) { exit; }

add_action( 'admin_notices', function () {
	if ( ! current_user_can( 'manage_options' ) ) { return; }
	if ( ! nlpo_has_nadlan_config() ) {
		echo '<div class="notice notice-warning"><p>' . esc_html__( 'NadLan Platform Orchestrator is active, but nadlan-config was not detected. The orchestrator will not replace business logic. Activate nadlan-config before using showroom features.', 'nadlan-platform-orchestrator' ) . '</p></div>';
	}
} );

add_action( 'admin_menu', function () {
	add_management_page(
		__( 'NadLan Platform', 'nadlan-platform-orchestrator' ),
		__( 'NadLan Platform', 'nadlan-platform-orchestrator' ),
		'manage_options',
		'nlpo-platform',
		'nlpo_admin_page'
	);
} );

function nlpo_admin_page() {
	if ( ! current_user_can( 'manage_options' ) ) { return; }
	if ( isset( $_POST['nlpo_save'] ) && check_admin_referer( 'nlpo_save_settings' ) ) {
		update_option( 'nlpo_auto_insert_home_band', isset( $_POST['nlpo_auto_insert_home_band'] ) ? '1' : '0', false );
		echo '<div class="notice notice-success"><p>' . esc_html__( 'Settings saved.', 'nadlan-platform-orchestrator' ) . '</p></div>';
	}
	$gaps = nlpo_scan_content_gaps( 80 );
	?>
	<div class="wrap">
		<h1><?php esc_html_e( 'NadLan Platform', 'nadlan-platform-orchestrator' ); ?></h1>
		<p><?php esc_html_e( 'This screen checks the platform wiring without replacing the existing site structure or showroom engine.', 'nadlan-platform-orchestrator' ); ?></p>
		<form method="post">
			<?php wp_nonce_field( 'nlpo_save_settings' ); ?>
			<table class="form-table" role="presentation">
				<tr>
					<th scope="row"><?php esc_html_e( 'Homepage project band', 'nadlan-platform-orchestrator' ); ?></th>
					<td><label><input type="checkbox" name="nlpo_auto_insert_home_band" value="1" <?php checked( get_option( 'nlpo_auto_insert_home_band', '0' ), '1' ); ?>> <?php esc_html_e( 'Append a project band to the homepage. Keep off until screenshot QA approves placement. Logged-in admins can preview with ?nlpo_preview=1.', 'nadlan-platform-orchestrator' ); ?></label></td>
				</tr>
			</table>
			<p><button class="button button-primary" type="submit" name="nlpo_save" value="1"><?php esc_html_e( 'Save', 'nadlan-platform-orchestrator' ); ?></button></p>
		</form>
		<h2><?php esc_html_e( 'Language and content gap scan', 'nadlan-platform-orchestrator' ); ?></h2>
		<table class="widefat striped">
			<thead><tr><th><?php esc_html_e( 'Project', 'nadlan-platform-orchestrator' ); ?></th><th><?php esc_html_e( 'Languages found', 'nadlan-platform-orchestrator' ); ?></th><th><?php esc_html_e( 'Missing', 'nadlan-platform-orchestrator' ); ?></th><th><?php esc_html_e( 'Thin content', 'nadlan-platform-orchestrator' ); ?></th></tr></thead>
			<tbody>
			<?php foreach ( $gaps as $row ) : ?>
				<tr>
					<td><strong><?php echo esc_html( $row['title'] ); ?></strong><br><code><?php echo esc_html( $row['base_slug'] ); ?></code></td>
					<td><?php echo esc_html( implode( ', ', $row['langs'] ) ); ?></td>
					<td><?php echo esc_html( $row['missing'] ? implode( ', ', $row['missing'] ) : 'OK' ); ?></td>
					<td><?php echo esc_html( $row['thin'] ? wp_json_encode( $row['thin'] ) : 'OK' ); ?></td>
				</tr>
			<?php endforeach; ?>
			</tbody>
		</table>
	</div>
	<?php
}
