<?php
if ( ! defined( 'ABSPATH' ) ) { exit; }

function nlpo_project_card( $post_id ) {
	$title = get_the_title( $post_id );
	$url   = get_permalink( $post_id );
	$img   = nlpo_project_image( $post_id );
	$area  = (string) get_post_meta( $post_id, 'project_area', true );
	$floors = (string) get_post_meta( $post_id, 'project_floors', true );
	$excerpt = nlpo_project_excerpt( $post_id );
	ob_start();
	?>
	<a class="nlp-project-card" href="<?php echo esc_url( $url ); ?>">
		<span class="nlp-project-media">
			<?php if ( $img ) : ?><img loading="lazy" decoding="async" src="<?php echo esc_url( $img ); ?>" alt="<?php echo esc_attr( $title ); ?>"><?php endif; ?>
			<span class="nlp-project-badge"><?php esc_html_e( 'הדמיה להמחשה', 'nadlan-platform-orchestrator' ); ?></span>
		</span>
		<span class="nlp-project-body">
			<span class="nlp-section-eyebrow"><?php echo esc_html( $area ?: __( 'פרויקט חדש', 'nadlan-platform-orchestrator' ) ); ?></span>
			<h2><?php echo esc_html( $title ); ?></h2>
			<span class="nlp-project-meta">
				<?php if ( $floors !== '' ) : ?><span><?php echo esc_html( $floors ); ?> <?php esc_html_e( 'קומות', 'nadlan-platform-orchestrator' ); ?></span><?php endif; ?>
				<span><?php esc_html_e( 'בחירת דירה', 'nadlan-platform-orchestrator' ); ?></span>
				<span><?php esc_html_e( 'מידע וסביבה', 'nadlan-platform-orchestrator' ); ?></span>
			</span>
			<?php if ( $excerpt ) : ?><p class="nlp-project-desc"><?php echo esc_html( $excerpt ); ?></p><?php endif; ?>
			<span class="nlp-project-cta"><?php esc_html_e( 'לצפייה בפרויקט', 'nadlan-platform-orchestrator' ); ?></span>
		</span>
	</a>
	<?php
	return ob_get_clean();
}

function nlpo_catalog_shortcode( $atts, $content = null, $tag = '' ) {
	$a = shortcode_atts( array( 'limit' => 12, 'title' => '', 'subtitle' => '' ), $atts, $tag );
	$q = nlpo_project_query( (int) $a['limit'] );
	$title = $a['title'] !== '' ? $a['title'] : __( 'פרויקטים חדשים', 'nadlan-platform-orchestrator' );
	$subtitle = $a['subtitle'] !== '' ? $a['subtitle'] : __( 'השוו פרויקטים חדשים לפי דירות, סביבה, אומדן ותוכן בדיקה לפני פנייה.', 'nadlan-platform-orchestrator' );
	ob_start();
	?>
	<section class="nlp-catalog-shell" data-nlpo-home-projects>
		<div class="nlp-catalog-head">
			<div>
				<span class="nlp-section-eyebrow"><?php esc_html_e( 'NADLAN', 'nadlan-platform-orchestrator' ); ?></span>
				<div class="nlp-rule"></div>
				<h1 class="nlp-catalog-title"><?php echo esc_html( $title ); ?></h1>
				<p class="nlp-catalog-sub"><?php echo esc_html( $subtitle ); ?></p>
			</div>
			<a class="nlp-btn" href="<?php echo esc_url( get_post_type_archive_link( 'nadlan_project' ) ?: home_url( '/projects/' ) ); ?>"><?php esc_html_e( 'כל הפרויקטים', 'nadlan-platform-orchestrator' ); ?></a>
		</div>
		<div class="nlp-project-grid">
			<?php if ( $q->have_posts() ) : while ( $q->have_posts() ) : $q->the_post(); echo nlpo_project_card( get_the_ID() ); endwhile; wp_reset_postdata(); else : ?>
				<p><?php esc_html_e( 'עדיין אין פרויקטים לפרסום.', 'nadlan-platform-orchestrator' ); ?></p>
			<?php endif; ?>
		</div>
	</section>
	<?php
	return ob_get_clean();
}
add_shortcode( 'nadlan_platform_home_projects', 'nlpo_catalog_shortcode' );
add_shortcode( 'nadlan_platform_project_catalog', 'nlpo_catalog_shortcode' );

function nlpo_showroom_shortcode( $atts ) {
	$a = shortcode_atts( array( 'project' => '', 'id' => '', 'page' => 'project' ), $atts, 'nadlan_platform_showroom' );
	if ( function_exists( 'nadlan_showroom_engine_shortcode' ) ) {
		return nadlan_showroom_engine_shortcode( $a );
	}
	return '<div class="nlp-interior"><div class="nlp-interior-stage"><p class="nlp-interior-placeholder">' . esc_html__( 'תצוגת הפרויקט תעלה בקרוב.', 'nadlan-platform-orchestrator' ) . '</p></div></div>';
}
add_shortcode( 'nadlan_platform_showroom', 'nlpo_showroom_shortcode' );

function nlpo_interior_shortcode( $atts ) {
	$a = shortcode_atts( array( 'project' => '', 'id' => '' ), $atts, 'nadlan_platform_interior' );
	$post = null;
	if ( $a['id'] ) {
		$post = get_post( (int) $a['id'] );
	} elseif ( $a['project'] ) {
		$post = get_page_by_path( sanitize_title( $a['project'] ), OBJECT, 'nadlan_project' );
	} elseif ( is_singular( 'nadlan_project' ) ) {
		$post = get_post( get_queried_object_id() );
	}
	if ( ! $post ) { return ''; }
	$tour = esc_url( (string) get_post_meta( $post->ID, 'project_3d_tour_url', true ) );
	$panos = get_post_meta( $post->ID, 'project_interior_panoramas', true );
	if ( is_string( $panos ) && $panos !== '' ) { $panos = json_decode( $panos, true ); }
	if ( ! is_array( $panos ) ) { $panos = array(); }
	ob_start();
	?>
	<section class="nlp-interior" data-nlpo-interior>
		<div class="nlp-interior-head">
			<div>
				<span class="nlp-section-eyebrow"><?php esc_html_e( 'סיור פנים', 'nadlan-platform-orchestrator' ); ?></span>
				<h2 class="nlp-interior-title"><?php echo esc_html( get_the_title( $post ) ); ?></h2>
			</div>
		</div>
		<div class="nlp-interior-stage" data-nlpo-interior-stage>
			<?php if ( $tour ) : ?>
				<p class="nlp-interior-placeholder"><?php esc_html_e( 'סיור פנים זמין. לחצו כדי לפתוח את התצוגה.', 'nadlan-platform-orchestrator' ); ?></p>
			<?php elseif ( ! empty( $panos ) ) : ?>
				<p class="nlp-interior-placeholder"><?php esc_html_e( 'תמונות פנים פנורמיות זמינות לצפייה לפי חדר.', 'nadlan-platform-orchestrator' ); ?></p>
			<?php else : ?>
				<p class="nlp-interior-placeholder"><?php esc_html_e( 'סיור פנים יתווסף כאשר יתקבלו תמונות או קישור מאושר מהיזם. בינתיים מוצגות תכנית הדירה, הסביבה והמידע הרלוונטי לבחירה.', 'nadlan-platform-orchestrator' ); ?></p>
			<?php endif; ?>
		</div>
		<div class="nlp-interior-actions">
			<?php if ( $tour ) : ?><button class="nlp-btn" type="button" data-nlpo-tour-url="<?php echo esc_url( $tour ); ?>"><?php esc_html_e( 'פתח סיור פנים', 'nadlan-platform-orchestrator' ); ?></button><?php endif; ?>
			<a class="nlp-btn" href="#inquiry"><?php esc_html_e( 'דברו איתנו על הדירה', 'nadlan-platform-orchestrator' ); ?></a>
		</div>
	</section>
	<?php
	return ob_get_clean();
}
add_shortcode( 'nadlan_platform_interior', 'nlpo_interior_shortcode' );
