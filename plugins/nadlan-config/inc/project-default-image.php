<?php
/**
 * HAD-740 (Ben 14.11.2026): the approved default picture on every project card that has no picture of its own.
 * Not welded into code: the picture is a media-library item whose id sits in the option nadlan_pd_attachment, chosen under
 * Settings > Media ("תמונת ברירת מחדל לכרטיסי פרויקט"). A project's own featured picture (or a photo in photos_csv) always wins;
 * remove it and the default comes back. A language page (slug -en / -fr / -ru / -ar) first shows its Hebrew page's featured picture.
 * Option empty or the media deleted: null, and the card keeps its old behaviour exactly.
 * Gate: nothing changes for the public until option nadlan_pd_public = '1'; ?pics=next shows it for a check.
 * Loaded by one require line at the end of inc/directory.php (1.72.677).
 */
if ( ! defined( 'ABSPATH' ) ) { exit; }

if ( ! function_exists( 'nadlan_pd_on' ) ) {
	function nadlan_pd_on() {
		if ( '1' === (string) get_option( 'nadlan_pd_public', '' ) ) { return true; }
		return isset( $_GET['pics'] ) && 'next' === $_GET['pics']; // phpcs:ignore WordPress.Security.NonceVerification.Recommended
	}
}

if ( ! function_exists( 'nadlan_pd_lang_of_slug' ) ) {
	/** he / en / fr / ru / ar from a project slug (the language pages end in -en, -fr, -ru, -ar). */
	function nadlan_pd_lang_of_slug( $slug ) {
		return preg_match( '/-(en|fr|ru|ar)$/', (string) $slug, $m ) ? $m[1] : 'he';
	}
}

if ( ! function_exists( 'nadlan_pd_alt' ) ) {
	function nadlan_pd_alt( $lang ) {
		$alts = array(
			'he' => 'נדל״ן: בחרו את הדירה שלכם על הבניין. מגדל מגורים עם קומה מסומנת, תוכנית הדירה ומפת הסביבה',
			'en' => 'NadLan: choose your apartment on the building. A residential tower with one floor marked, the apartment plan and a map of the surroundings',
			'fr' => "NadLan : choisissez votre appartement sur l'immeuble. Tour résidentielle avec un étage sélectionné, le plan de l'appartement et la carte des environs",
			'ru' => 'NadLan: выберите квартиру прямо на здании. Жилая башня с выбранным этажом, план квартиры и карта окрестностей',
			'ar' => 'NadLan: اختاروا شقتكم على المبنى. برج سكني مع طابق محدد، مخطط الشقة وخريطة المحيط',
		);
		return $alts[ (string) $lang ] ?? $alts['he'];
	}
}

if ( ! function_exists( 'nadlan_pd_default' ) ) {
	/** The default picture as array( url, w, h, srcset, sizes, alt, id ), or null (no option, or the media is gone). */
	function nadlan_pd_default( $lang = 'he' ) {
		$aid = (int) get_option( 'nadlan_pd_attachment', 0 );
		if ( $aid < 1 || 'attachment' !== get_post_type( $aid ) || ! wp_attachment_is_image( $aid ) ) { return null; }
		$src = wp_get_attachment_image_src( $aid, 'large' );
		if ( ! is_array( $src ) || empty( $src[0] ) ) { return null; }
		$srcset = function_exists( 'wp_get_attachment_image_srcset' ) ? (string) wp_get_attachment_image_srcset( $aid, 'large' ) : '';
		return array(
			'url'    => (string) $src[0],
			'w'      => (int) $src[1],
			'h'      => (int) $src[2],
			'srcset' => $srcset,
			'sizes'  => '(max-width: 760px) 100vw, 420px',
			'alt'    => nadlan_pd_alt( $lang ),
			'id'     => $aid,
		);
	}
}

if ( ! function_exists( 'nadlan_pd_pick' ) ) {
	/** For a card of a project WITHOUT a picture of its own: the Hebrew twin's featured picture (language pages), else the default.
	 *  null = keep the card exactly as before (gate closed, or nothing to show). kind: 'twin' | 'default'. */
	function nadlan_pd_pick( $id ) {
		if ( ! nadlan_pd_on() ) { return null; }
		$slug = (string) get_post_field( 'post_name', (int) $id );
		$lang = nadlan_pd_lang_of_slug( $slug );
		if ( 'he' !== $lang ) {
			$he = get_page_by_path( (string) preg_replace( '/-(en|fr|ru|ar)$/', '', $slug ), OBJECT, 'nadlan_project' );
			if ( $he && has_post_thumbnail( $he->ID ) ) {
				$tid = (int) get_post_thumbnail_id( $he->ID );
				$src = wp_get_attachment_image_src( $tid, 'large' );
				if ( is_array( $src ) && ! empty( $src[0] ) ) {
					return array( 'url' => (string) $src[0], 'w' => (int) $src[1], 'h' => (int) $src[2], 'srcset' => (string) wp_get_attachment_image_srcset( $tid, 'large' ),
						'sizes' => '(max-width: 760px) 100vw, 420px', 'alt' => '', 'id' => $tid, 'kind' => 'twin' );
				}
			}
		}
		$d = nadlan_pd_default( $lang );
		if ( ! $d ) { return null; }
		$d['kind'] = 'default';
		return $d;
	}
}

/* The setting: an attachment id (Settings > Media), and the public switch. Both visible to the REST settings route for admins only. */
add_action( 'init', function () {
	register_setting( 'media', 'nadlan_pd_attachment', array( 'type' => 'integer', 'default' => 0, 'show_in_rest' => true, 'sanitize_callback' => 'absint',
		'description' => 'HAD-740: the default picture of project cards (media id)' ) );
	register_setting( 'media', 'nadlan_pd_public', array( 'type' => 'string', 'default' => '', 'show_in_rest' => true,
		'sanitize_callback' => function ( $v ) { return '1' === (string) $v ? '1' : ''; }, 'description' => 'HAD-740: default card picture for everyone (1) or only with ?pics=next' ) );
} );

add_action( 'admin_init', function () {
	add_settings_field( 'nadlan_pd_attachment', 'תמונת ברירת מחדל לכרטיסי פרויקט', function () {
		if ( ! current_user_can( 'manage_options' ) ) { return; }
		$aid = (int) get_option( 'nadlan_pd_attachment', 0 );
		$src = $aid ? wp_get_attachment_image_src( $aid, 'medium_large' ) : false;
		echo '<div id="nlpd-field" dir="rtl">';
		echo '<input type="hidden" name="nadlan_pd_attachment" id="nlpd-id" value="' . esc_attr( (string) $aid ) . '">';
		echo '<div id="nlpd-prev" style="max-width:420px;aspect-ratio:8/5;background:#E3EEF2;border:1px solid #C9D3DA;border-radius:8px;overflow:hidden;margin:0 0 8px">'
			. ( $src ? '<img src="' . esc_url( $src[0] ) . '" alt="" style="width:100%;height:100%;object-fit:cover;display:block">' : '' ) . '</div>';
		echo '<button type="button" class="button" id="nlpd-pick">בחירת תמונה מספריית המדיה</button> ';
		echo '<button type="button" class="button-link" id="nlpd-clear"' . ( $aid ? '' : ' style="display:none"' ) . '>הסרה</button>';
		echo '<p class="description">מופיעה בכל כרטיס פרויקט שאין לו תמונה ראשית משלו. תמונה ראשית של פרויקט תמיד מנצחת. מומלץ יחס 8:5, לפחות 1600 על 1000. מזהה נוכחי: ' . ( $aid ? (int) $aid : 'אין' ) . '</p>';
		echo '</div>';
	}, 'media', 'default' );
} );

add_action( 'admin_enqueue_scripts', function ( $hook ) {
	if ( 'options-media.php' !== $hook || ! current_user_can( 'manage_options' ) ) { return; }
	wp_enqueue_media();
	wp_add_inline_script( 'media-editor', '(function(){document.addEventListener("DOMContentLoaded",function(){var pick=document.getElementById("nlpd-pick");if(!pick||!window.wp||!wp.media)return;'
		. 'var id=document.getElementById("nlpd-id"),prev=document.getElementById("nlpd-prev"),clr=document.getElementById("nlpd-clear"),fr=null;'
		. 'pick.addEventListener("click",function(e){e.preventDefault();if(!fr){fr=wp.media({title:"תמונת ברירת מחדל לכרטיסי פרויקט",library:{type:"image"},button:{text:"בחירה"},multiple:false});'
		. 'fr.on("select",function(){var a=fr.state().get("selection").first().toJSON();id.value=a.id;var u=(a.sizes&&(a.sizes.medium_large||a.sizes.large||a.sizes.full)||a).url;'
		. 'prev.innerHTML="";var im=document.createElement("img");im.src=u;im.alt="";im.style.cssText="width:100%;height:100%;object-fit:cover;display:block";prev.appendChild(im);clr.style.display="";});}fr.open();});'
		. 'clr.addEventListener("click",function(e){e.preventDefault();id.value="0";prev.innerHTML="";clr.style.display="none";});});})();' );
} );
