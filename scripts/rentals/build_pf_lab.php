<?php
/* Builds the lab pages of the rentals opening stage from the REAL server file (inc/rentals/portfolio.php), with small stand-ins
   for the WordPress functions it calls, and a page around it that copies what the live page does to it:
   the live landing's own inline styles for the hero and the steps, the theme's forced heading face, link colour and button
   colours, the professionals' card rule on the bare class .nlpf, the page's side padding, and (with ?floats=1) the site's
   floating WhatsApp bar, basket and accessibility button at their measured places.
   The map key is never written: the lab page takes it from its address (?t=...).
   Usage: php scripts/rentals/build_pf_lab.php   -> docs/design-lab/rentals-portfolio/stage-he.html, stage-en.html */
define( 'ABSPATH', __DIR__ );
define( 'NADLAN_CONFIG_VERSION', 'lab' );
function plugins_url( $p, $f ) { return '../../../plugins/nadlan-config/' . $p; }
function esc_attr( $s ) { return htmlspecialchars( (string) $s, ENT_QUOTES, 'UTF-8' ); }
function esc_html( $s ) { return htmlspecialchars( (string) $s, ENT_QUOTES, 'UTF-8' ); }
function esc_url( $s ) { return htmlspecialchars( (string) $s, ENT_QUOTES, 'UTF-8' ); }
function wp_json_encode( $d, $f = 0 ) { return json_encode( $d, $f ); }
function nadlan_mapbox_token() { return ''; }
require dirname( __DIR__, 2 ) . '/plugins/nadlan-config/inc/rentals/portfolio.php';
$out = dirname( __DIR__, 2 ) . '/docs/design-lab/rentals-portfolio/';
$go  = '#signup?redirect=/my-rentals/';
foreach ( array( 'he', 'en' ) as $lang ) {
	$en = 'en' === $lang;
	ob_start();
	nadlan_rm_portfolio_stage( $lang, $go, '/my-rentals/?sample=1' . ( $en ? '&lang=en' : '' ) );
	$stage = str_replace( 'data-token=""', 'data-token="" data-lab="1"', ob_get_clean() );
	/* the key arrives in the address only: set it on the stage before pf.js (deferred) runs */
	$stage = str_replace( '<script defer src=', '<script>document.getElementById("nlpf").dataset.token=new URLSearchParams(location.search).get("t")||"";</script><script defer src=', $stage );
	$sub = $en ? 'Add a property, mark your apartments on a 3D model of the building, and manage everything per apartment: tenant, rent tracking, lease and tax reminders, documents and maintenance. No spreadsheets, no fees.' : 'מוסיפים נכס, מסמנים את הדירות שלכם על מודל תלת-ממדי של הבניין, ומנהלים הכל מדירה אחת: שוכר, שכר דירה, מעקב תשלומים, תזכורות חוזה ומס, מסמכים ותחזוקה. בלי אקסל ובלי עמלות.';
	$steps = $en
		? array( array( 'Add a property', 'City, address, floors - and we build a 3D model of your building on the map.' ), array( 'Mark your apartments', 'Tap the apartments you own on the model and fill in tenant, rent and lease dates.' ), array( 'One color says it all', 'The apartment color tells the story: paid, pending, overdue, vacant. Lease reminders, documents and maintenance - one place.' ) )
		: array( array( 'מוסיפים נכס', 'עיר, כתובת, קומות - ונבנה לכם מודל תלת-ממדי של הבניין על המפה.' ), array( 'מסמנים את הדירות שלכם', 'מקישים על הדירות שבבעלותכם על המודל וממלאים שוכר, שכר דירה ותאריכי חוזה.' ), array( 'הכל במעקב אחד', 'צבע הדירה אומר הכל: שולם, ממתין, בפיגור, פנויה. תזכורות חוזה, מסמכים ותחזוקה - במקום אחד.' ) );
	$html = '<!doctype html><html lang="' . $lang . '" dir="' . ( $en ? 'ltr' : 'rtl' ) . '"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">'
		. '<title>LAB: the rentals opening stage (' . $lang . ')</title>'
		. '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Heebo:wght@400;600;700&display=swap">'
		/* the theme stand-in */
		. '<style>body{margin:0;background:#f4f6f8}li{margin:8px 0}h1,h2{font-family:Georgia,serif!important;font-weight:600!important}h2{color:#7a1f1f!important}.nlrm a{color:rgb(47,111,134)!important}'
		. 'button{background:#c2563a!important;color:#fff!important;border-radius:4px!important;text-transform:uppercase!important}'
		. '.nlpf{width:min(1120px,calc(100vw - 28px))!important;margin:24px auto 44px!important;border:1px solid #999;border-radius:18px;direction:rtl}'
		. '.lab-head{height:64px;background:#fff;border-bottom:1px solid #dfe6ec}.lab-pad{padding:0 12px}.nlrm-demo{height:900px;background:#fff;border-radius:16px;margin-top:20px;padding:20px}'
		/* the live landing's own inline styles (inc/rentals-manager.php) */
		. '.nlrm{max-width:1120px;margin:0 auto;padding:24px 16px 60px;font-family:Heebo,sans-serif;color:#1B1A17}'
		. '.nlrm-hero{text-align:center;padding:30px 0 10px}.nlrm-kicker{font:700 12.5px Heebo;letter-spacing:.06em;color:#9C7A3C;text-transform:uppercase;margin:0 0 10px}'
		. '.nlrm-hero h1{font-size:clamp(1.6rem,3.8vw,2.4rem);margin:0 0 12px;line-height:1.3}.nlrm-hero .sub{color:#51483A;font:400 15px/1.7 Heebo;max-width:640px;margin:0 auto 20px}'
		. '.nlrm-ctas{display:flex;gap:12px;justify-content:center;flex-wrap:wrap}.nlrm-cta{display:inline-block;border-radius:12px;padding:15px 26px;font:700 15px Heebo;text-decoration:none}'
		. '.nlrm-cta--go{background:#C2563A;color:#FAF7F1}.nlrm-badges{color:#8E877A;font:600 12px Heebo;margin:14px 0 22px}'
		. '.nlrm-steps{display:grid;grid-template-columns:repeat(3,1fr);gap:14px;margin:10px 0 30px}@media(max-width:760px){.nlrm-steps{grid-template-columns:1fr}}'
		. '.nlrm-step{background:#fff;border:1px solid #E2DCD0;border-radius:16px;padding:18px;text-align:start}'
		. '.nlrm-step i{display:block;width:36px;height:36px;border-radius:50%;background:#9C7A3C;color:#FAF7F1;font:700 16px/36px "Frank Ruhl Libre",serif;font-style:normal;text-align:center;margin-bottom:10px}'
		. '.nlrm-step b{display:block;font-family:"Frank Ruhl Libre",serif;margin-bottom:4px}.nlrm-step p{font:400 13px/1.65 Heebo;color:#51483A;margin:0}</style></head><body>'
		. '<script>if(new URLSearchParams(location.search).get("floats")==="1"){document.write(\'<a class="lab-f" id="lab-wa" style="position:fixed;z-index:99980;left:12px;bottom:78px;width:280px;height:50px;border-radius:25px;background:#0f7a5a"></a><a class="lab-f" id="lab-cart" style="position:fixed;z-index:99990;right:12px;bottom:84px;width:129px;height:44px;border-radius:22px;background:#fff;border:1px solid #14212b"></a><a class="lab-f" id="lab-a11y" style="position:fixed;z-index:99998;right:14px;bottom:14px;width:52px;height:52px;border-radius:12px;background:#1f4b5c"></a>\');}</script>'
		. '<div class="lab-head"></div><div class="lab-pad"><div class="nlrm" dir="' . ( $en ? 'ltr' : 'rtl' ) . '" lang="' . $lang . '">'
		/* the landing as the release prints it */
		. '<header class="nlrm-hero">' . nadlan_rm_lockup( $lang )
		. '<p class="nlrm-kicker">' . ( $en ? 'Rental management · free for landlords' : 'ניהול השכרות · חינם לבעלי דירות' ) . '</p>'
		. '<h1>' . ( $en ? 'Every apartment you rent out: on the map, inside the building, fully in control' : 'כל הדירות המושכרות שלכם: על המפה, בתוך הבניין, בשליטה מלאה' ) . '</h1>'
		. '<p class="nlrm-one">' . esc_html( nadlan_rm_one_line( $lang ) ) . '</p></header>'
		. $stage
		. '<header class="nlrm-hero nlrm-hero--after"><p class="sub">' . $sub . '</p><div class="nlrm-ctas"><a class="nlrm-cta nlrm-cta--go" href="' . $go . '">' . ( $en ? 'Start managing, free' : 'מתחילים לנהל, חינם' ) . '</a></div>'
		. '<p class="nlrm-badges">' . ( $en ? 'Free for landlords' : 'חינם לבעלי דירות · מעקב ותזכורות, לא סליקה' ) . '</p></header>'
		. '<div class="nlrm-steps">' . implode( '', array_map( function ( $s, $i ) { return '<div class="nlrm-step"><i>' . ( $i + 1 ) . '</i><b>' . $s[0] . '</b><p>' . $s[1] . '</p></div>'; }, $steps, array_keys( $steps ) ) ) . '</div>'
		. '<section class="nlrm-demo"><h2>demo</h2></section></div></div></body></html>';
	file_put_contents( $out . 'stage-' . $lang . '.html', $html );
	echo "stage-$lang.html " . strlen( $html ) . "\n";
}
