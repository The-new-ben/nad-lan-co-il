<?php
/**
 * nadlan-config - English hub for foreign buyers (v1.69.97)
 *
 * [nadlan_en_hub] renders the /en/ landing hub: hero, English project pages
 * (language siblings with the -en slug suffix), English guides (category
 * "english"), how-it-works trust points and a lead CTA. Everything is
 * CMS-driven; empty sections collapse. LTR by design.
 */

if ( ! defined( 'ABSPATH' ) ) { exit; }

if ( ! function_exists( 'nadlan_enhub_projects' ) ) {
	function nadlan_enhub_projects( $limit = 6 ) {
		$hit = get_transient( 'nadlan_enhub_projects' );
		if ( is_array( $hit ) ) { return array_slice( $hit, 0, $limit ); }
		$pool = get_posts( array( 'post_type' => 'nadlan_project', 'post_status' => 'publish', 'posts_per_page' => 50, 'no_found_rows' => true ) );
		$out = array();
		foreach ( $pool as $p ) {
			if ( ! preg_match( '/-en$/', $p->post_name ) ) { continue; }
			$out[] = array(
				'id'    => $p->ID,
				'title' => get_the_title( $p ),
				'url'   => get_permalink( $p ),
				'img'   => function_exists( 'nadlan_hv2_img' ) ? nadlan_hv2_img( $p->ID ) : '',
				'city'  => (string) get_post_meta( $p->ID, 'city', true ),
				'ppsqm' => (int) get_post_meta( $p->ID, 'project_3d_avg_price_per_sqm', true ),
			);
		}
		set_transient( 'nadlan_enhub_projects', $out, 6 * HOUR_IN_SECONDS );
		return array_slice( $out, 0, $limit );
	}
}

if ( ! function_exists( 'nadlan_en_hub_shortcode' ) ) {
	function nadlan_en_hub_shortcode() {
		$projects = nadlan_enhub_projects();
		$guides = get_posts( array( 'post_type' => 'post', 'posts_per_page' => 6, 'no_found_rows' => true, 'category_name' => 'english' ) );
		$counts = array(
			'projects' => (int) wp_count_posts( 'nadlan_project' )->publish,
			'pros'     => (int) wp_count_posts( 'nadlan_professional' )->publish,
		);
		ob_start(); ?>
<div class="nlen" dir="ltr">

	<section class="nlen-hero">
		<p class="nlen-kicker">For international buyers</p>
		<h1>Buying property in Israel, with the full picture first</h1>
		<p class="nlen-sub">Walk through new-build projects in 3D, choose an apartment from inside the building, see honest price estimates and the real neighborhood - before you talk to anyone. Then get verified legal, tax and mortgage guidance in English.</p>
		<div class="nlen-trust">
			<span><b><?php echo number_format( $counts['projects'] ); ?></b> projects tracked from official registries</span>
			<span><b><?php echo number_format( $counts['pros'] ); ?></b> verified professionals (gov.il)</span>
			<span><b>English</b> speaking guidance end to end</span>
		</div>
	</section>

	<?php if ( $projects ) : ?>
	<section class="nlen-band">
		<h2>Explore projects in English</h2>
		<div class="nlen-grid">
			<?php foreach ( $projects as $p ) : ?>
			<a class="nlen-card" href="<?php echo esc_url( $p['url'] ); ?>">
				<span class="nlen-card-media"<?php echo $p['img'] ? ' style="background-image:url(' . esc_url( $p['img'] ) . ')"' : ''; ?>><em>Choose your apartment inside the building</em></span>
				<b><?php echo esc_html( $p['title'] ); ?></b>
				<span class="nlen-card-cap"><?php echo esc_html( $p['city'] ); ?><?php echo $p['ppsqm'] ? ' · ~' . number_format( $p['ppsqm'] ) . ' ILS/sqm (non-binding estimate)' : ''; ?></span>
			</a>
			<?php endforeach; ?>
		</div>
	</section>
	<?php endif; ?>

	<?php if ( count( $guides ) >= 2 ) : ?>
	<section class="nlen-band">
		<h2>Guides that answer the hard questions</h2>
		<div class="nlen-guides">
			<?php foreach ( $guides as $g ) : ?>
			<a href="<?php echo esc_url( get_permalink( $g ) ); ?>"><b><?php echo esc_html( get_the_title( $g ) ); ?></b><span>Read the guide →</span></a>
			<?php endforeach; ?>
		</div>
	</section>
	<?php endif; ?>

	<section class="nlen-band nlen-how">
		<h2>How buying from abroad works with us</h2>
		<div class="nlen-steps">
			<div><b>1 · See everything remotely</b><span>3D building tours, floor and view per apartment, live neighborhood maps with schools and transit, price estimates in context.</span></div>
			<div><b>2 · Verify with professionals</b><span>Real-estate lawyers, licensed appraisers and mortgage advisors from a registry-verified directory, working in English.</span></div>
			<div><b>3 · Decide with clear numbers</b><span>Purchase tax for non-residents, financing terms, full transaction costs - calculated before you commit to anything.</span></div>
		</div>
	</section>

	<section class="nlen-cta">
		<div>
			<h2>Tell us what you are looking for</h2>
			<p>A short note is enough. We reply in English, usually within one business day. No obligation.</p>
		</div>
		<form class="nlen-form" onsubmit="return nlenLead(this)">
			<input type="text" name="name" placeholder="Full name" required>
			<input type="email" name="email" placeholder="Email" required>
			<input type="text" name="message" placeholder="What are you looking for? (city, budget, timeline)">
			<input type="text" name="company" class="nlen-hp" tabindex="-1" autocomplete="off" aria-hidden="true">
			<button type="submit">Send</button>
			<span class="nlen-msg" aria-live="polite"></span>
		</form>
	</section>

	<p class="nlen-legal">Information on this page is general and not legal, tax or investment advice. Price figures are non-binding estimates based on publicly available data; verify with the developer.</p>
</div>
<script>
function nlenLead(f){
	var m=f.querySelector('.nlen-msg');m.textContent='Sending...';
	fetch('<?php echo esc_url_raw( rest_url( 'nadlan/v1/lead' ) ); ?>',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({name:f.name.value,email:f.email.value,message:f.message.value,company:f.company.value,goal:'international buyer',source:'en-hub',lang:'en'})})
	.then(function(r){return r.json()}).then(function(d){
		if(d&&d.ok!==false){f.style.display='none';m.textContent='Thank you. We will get back to you in English shortly.'}
		else{m.textContent='Something went wrong, please try again.'}
	}).catch(function(){m.textContent='Network error, please try again.'});
	return false;
}
</script>
<?php
		return ob_get_clean();
	}
}
add_shortcode( 'nadlan_en_hub', 'nadlan_en_hub_shortcode' );

add_action( 'wp_enqueue_scripts', function () {
	if ( ! is_singular() || ! has_shortcode( (string) get_post_field( 'post_content', get_queried_object_id() ), 'nadlan_en_hub' ) ) { return; }
	wp_register_style( 'nadlan-enhub', false );
	wp_enqueue_style( 'nadlan-enhub' );
	wp_add_inline_style( 'nadlan-enhub', '
.nlen{--ink:#1B1A17;--warm:#6D665C;--gold:#9C7A3C;--terra:#C2563A;--line:#E2DCD0;--band:#F3EEE3;font-family:var(--font-sans,Heebo,system-ui,sans-serif);color:var(--ink);text-align:left}
.nlen h1{font-family:var(--font-serif,"Frank Ruhl Libre",serif);font-weight:500;font-size:clamp(1.9rem,4.6vw,3rem);line-height:1.12;margin:0 0 12px}
.nlen h2{font-family:var(--font-serif,"Frank Ruhl Libre",serif);font-weight:500;font-size:clamp(1.3rem,2.4vw,1.7rem);margin:0 0 16px}
.nlen-kicker{font-size:11.5px;font-weight:700;letter-spacing:.14em;color:var(--gold);text-transform:uppercase;margin:0 0 4px}
.nlen-hero{padding:34px 0 10px}
.nlen-sub{color:var(--warm);max-width:640px;font-size:15.5px;margin:0 0 18px}
.nlen-trust{display:flex;gap:24px;flex-wrap:wrap;font-size:12.5px;color:var(--warm)}
.nlen-trust b{color:var(--ink);font-size:15px;display:block}
.nlen-band{padding:28px 0;border-top:1px solid var(--line);margin-top:24px}
.nlen-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(240px,1fr));gap:16px}
.nlen-card{display:block;border:1px solid var(--line);border-radius:14px;overflow:hidden;background:#fff;text-decoration:none;color:var(--ink);transition:transform .2s,box-shadow .25s}
.nlen-card:hover{transform:translateY(-3px);box-shadow:0 14px 34px rgba(27,26,23,.1)}
.nlen-card-media{display:block;aspect-ratio:16/10;background:var(--band) center/cover no-repeat;position:relative}
.nlen-card-media em{position:absolute;bottom:10px;left:10px;font-style:normal;font-size:11px;font-weight:700;background:rgba(27,26,23,.85);color:#E6D4AE;border-radius:5px;padding:4px 9px}
.nlen-card>b{display:block;font-family:var(--font-serif,serif);font-size:1.1rem;padding:12px 14px 2px}
.nlen-card-cap{display:block;font-size:12px;color:var(--warm);padding:0 14px 12px}
.nlen-guides{display:grid;grid-template-columns:repeat(auto-fit,minmax(240px,1fr));gap:12px}
.nlen-guides a{display:block;border:1px solid var(--line);border-radius:10px;background:#fff;padding:16px 18px;text-decoration:none;color:var(--ink);transition:border-color .2s,transform .2s}
.nlen-guides a:hover{border-color:var(--gold);transform:translateY(-2px)}
.nlen-guides b{display:block;font-size:14.5px;line-height:1.4;margin-bottom:6px}
.nlen-guides span{font-size:12.5px;color:var(--gold);font-weight:700}
.nlen-steps{display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:14px}
.nlen-steps div{border:1px solid var(--line);border-radius:12px;background:#FAF8F3;padding:18px}
.nlen-steps b{display:block;font-size:14.5px;margin-bottom:6px}
.nlen-steps span{font-size:13px;color:var(--warm);line-height:1.55}
.nlen-cta{display:grid;grid-template-columns:1fr 1fr;gap:26px;align-items:center;background:linear-gradient(160deg,#211F19,#14130F);border-radius:16px;color:#FAF8F3;padding:28px;margin-top:28px}
@media(max-width:760px){.nlen-cta{grid-template-columns:1fr}}
.nlen-cta h2{color:#F4EEDE;margin:0 0 6px}
.nlen-cta p{margin:0;font-size:13.5px;color:#C9C2B2}
.nlen-form{display:grid;gap:8px}
.nlen-form input{border:1px solid rgba(244,238,222,.25);border-radius:9px;background:rgba(255,255,255,.06);color:#F4EEDE;font:inherit;font-size:14px;padding:12px 14px}
.nlen-form input::placeholder{color:#8D8676}
.nlen-form button{border:0;border-radius:9px;background:var(--terra);color:#fff;font:700 15px/1 inherit;font-family:inherit;padding:13px;cursor:pointer}
.nlen-form button:hover{background:#A7452E}
.nlen-hp{position:absolute;left:-9999px}
.nlen-msg{font-size:13px;color:#E6D4AE}
.nlen-legal{font-size:11.5px;color:var(--warm);border-top:1px solid var(--line);padding-top:14px;margin-top:26px}
' );
} );
