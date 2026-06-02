<?php
/**
 * nadlan-config — Sponsored-spot CTA on directory (v1.40.0 / shark #9)
 *
 * Injects a "הופיעו כאן — קבלו לידים חמים" sponsored-spot card into the
 * professionals + projects directory results, every N cards. Clicks → /join-pro/
 * pricing page (or directly to the relevant cart product). Two purposes:
 *  1. Visible revenue surface to every visitor (people SEE the model exists).
 *  2. Visible to contractors viewing their own profile category — a constant
 *     reminder that they could be the next sponsored card.
 *
 * Filters into the existing `nldir-results` HTML via the directory's REST + the
 * server-rendered first page using a single output-buffer pass on the archive
 * pages we own. No double-render: only fires on pages with `class="nldir"`.
 */
if ( ! defined( 'ABSPATH' ) ) { exit; }

if ( ! function_exists( 'nadlan_ss_card' ) ) {
	function nadlan_ss_card( $mode = 'professional' ) {
		$pricing = home_url( '/join-pro/' );
		$cart    = $mode === 'project' ? home_url( '/?add-to-cart=489&ref=ss' ) : home_url( '/?add-to-cart=476&ref=ss' );
		$copy_h  = $mode === 'project' ? 'הציגו את הפרויקט שלכם כאן' : 'הכרטיס שלכם יכול להיות במקום זה';
		$copy_p  = $mode === 'project' ? 'חשיפה מועדפת ליזמים מולנו ולקוחות פוטנציאליים. ₪3,990 לקמפיין.' : 'הופיעו לפני 2,700 קבלנים אחרים. Pro מ-₪349/חודש.';
		ob_start(); ?>
<a class="nldc nldc-sponsored-spot" href="<?php echo esc_url( $cart ); ?>" style="--pc:#9C7A3C;--ps:#FBF6EE;background:linear-gradient(135deg,#FBF9F5,#F0E9DA);text-align:center;border:1.5px dashed rgba(156,122,60,.55)">
	<span class="nldc-sponsor" style="position:relative;inset:auto;align-self:center;margin-bottom:8px">מקודם · פנוי</span>
	<div style="display:flex;flex-direction:column;align-items:center;gap:6px;padding:14px 0">
		<span style="font-size:34px">📣</span>
		<h3 class="nldc-name" style="font-size:16px;margin:6px 0 2px;color:#1B1A17"><?php echo esc_html( $copy_h ); ?></h3>
		<p style="font-size:12.5px;color:#6b6b6b;margin:0;line-height:1.5"><?php echo esc_html( $copy_p ); ?></p>
		<span class="nldc-go" style="margin-top:8px;color:#9C7A3C;font-weight:700">בקשו מידע ←</span>
		<small style="font-size:11px;color:#9a9a9a">או <a href="<?php echo esc_url( $pricing ); ?>" style="color:#9C7A3C">השוואה מלאה</a></small>
	</div>
</a>
<?php
		return ob_get_clean();
	}
}

/* Inject after the 6th and the 18th card in the server-rendered directory.
 * We do this with a buffer filter scoped to the nldir results container. */
add_action( 'template_redirect', function () {
	if ( is_admin() || is_singular() ) { return; }
	if ( ! is_post_type_archive( array( 'nadlan_professional', 'nadlan_project' ) ) ) { return; }
	$mode = is_post_type_archive( 'nadlan_project' ) ? 'project' : 'professional';
	ob_start( function ( $html ) use ( $mode ) {
		if ( strpos( $html, 'nldir-results' ) === false ) { return $html; }
		// Find the results container and insert sponsored card after the 6th + 18th nldc card.
		return preg_replace_callback(
			'~(<div class="nldir-results"[^>]*>)(.*?)(</div>\s*<div class="nldir-more-wrap")~us',
			function ( $m ) use ( $mode ) {
				$open = $m[1]; $body = $m[2]; $tail = $m[3];
				// split body by closing </a> of each card
				$parts = preg_split( '~(?<=</a>)~', $body );
				$out = '';
				$count = 0;
				foreach ( $parts as $i => $part ) {
					$out .= $part;
					if ( strpos( $part, 'class="nldc' ) !== false ) {
						$count++;
						if ( $count === 6 || $count === 18 ) {
							$out .= nadlan_ss_card( $mode );
						}
					}
				}
				return $open . $out . $tail;
			},
			$html, 1
		) ?: $html;
	}, 0 );
}, 1 );

/* For AJAX load-more responses (REST), inject one sponsored card per page batch. */
add_filter( 'rest_post_dispatch', function ( $response, $server, $request ) {
	$route = $request->get_route();
	if ( $route !== '/nadlan/v1/directory' && $route !== '/nadlan/v1/projects' ) { return $response; }
	$data = $response->get_data();
	if ( empty( $data['html'] ) ) { return $response; }
	$mode = $route === '/nadlan/v1/projects' ? 'project' : 'professional';
	// inject one sponsored card after the first card in each AJAX batch
	$data['html'] = preg_replace( '~(</a>)~', '$1' . nadlan_ss_card( $mode ), $data['html'], 1 ) ?: $data['html'];
	$response->set_data( $data );
	return $response;
}, 10, 3 );
