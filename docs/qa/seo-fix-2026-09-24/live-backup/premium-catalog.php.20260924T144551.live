<?php
/**
 * nadlan-config - Premium project catalog (v1.71.6)
 *
 * [nadlan_premium_catalog]: the curated tier. Only projects that pass the full
 * experience gate for every approved publication language appear here: a complete
 * article, truthful interactive model, context and verified facts. Booking-style filters (facilities, rooms, delivery,
 * near sea) + recent-deals line per card + language links. This is both the
 * flagship UX and a monetization product (developers pay to be in the premium
 * tier). The big /projects/ catalog (900+) stays as the wide SEO net.
 *
 * JS prints in wp_footer (content filters corrupt inline scripts). No long dashes.
 */

if ( ! defined( 'ABSPATH' ) ) { exit; }

if ( ! function_exists( 'nadlan_pc_icons' ) ) {
	/** Tiny inline SVG icon set, gold-line DNA (stroke currentColor). */
	function nadlan_pc_icons() {
		$s = 'width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"';
		return array(
			'בריכה'   => '<svg '.$s.'><path d="M2 15c2-1.5 4-1.5 6 0s4 1.5 6 0 4-1.5 6 0"/><path d="M2 19c2-1.5 4-1.5 6 0s4 1.5 6 0 4-1.5 6 0"/><path d="M8 13V6a2 2 0 0 1 4 0"/><path d="M14 13V6a2 2 0 0 1 4 0"/></svg>',
			'לגונה'   => '<svg '.$s.'><circle cx="12" cy="12" r="8"/><path d="M6 12c2-1.2 4-1.2 6 0s4 1.2 6 0"/></svg>',
			'ספא'     => '<svg '.$s.'><path d="M8 4c0 2-2 2-2 4s2 2 2 4"/><path d="M13 4c0 2-2 2-2 4s2 2 2 4"/><path d="M18 4c0 2-2 2-2 4s2 2 2 4"/><path d="M4 17h16v2a2 2 0 0 1-2 2H6a2 2 0 0 1-2-2z"/></svg>',
			'חדר כושר'=> '<svg '.$s.'><path d="M6.5 6.5v11M17.5 6.5v11M3 9v6M21 9v6M6.5 12h11"/></svg>',
			'קולנוע'  => '<svg '.$s.'><rect x="3" y="6" width="18" height="13" rx="2"/><path d="m3 10 18-4"/><circle cx="8" cy="15" r="1.4"/><circle cx="16" cy="15" r="1.4"/></svg>',
			"קונסיירז'" => '<svg '.$s.'><path d="M4 18h16"/><path d="M12 6a7 7 0 0 1 7 7H5a7 7 0 0 1 7-7z"/><path d="M12 3v3"/></svg>',
			'לובי'    => '<svg '.$s.'><path d="M5 11V8a3 3 0 0 1 3-3h8a3 3 0 0 1 3 3v3"/><path d="M3 18v-4a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2v4"/><path d="M6 18v2M18 18v2"/></svg>',
			"לאונג'"  => '<svg '.$s.'><path d="M5 11V8a3 3 0 0 1 3-3h8a3 3 0 0 1 3 3v3"/><path d="M3 18v-4a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2v4"/><path d="M6 18v2M18 18v2"/></svg>',
			'ילדים'   => '<svg '.$s.'><circle cx="12" cy="6" r="2.5"/><path d="M12 9v5"/><path d="m9 21 3-7 3 7"/><path d="M8 12h8"/></svg>',
			'מסחר'    => '<svg '.$s.'><path d="M6 7h12l1 13H5z"/><path d="M9 10V6a3 3 0 0 1 6 0v4"/></svg>',
			'חניון'   => '<svg '.$s.'><rect x="4" y="4" width="16" height="16" rx="3"/><path d="M9 17V7h4a3 3 0 0 1 0 6H9"/></svg>',
			'ממ"ד'    => '<svg '.$s.'><path d="M12 3 4 6v6c0 5 3.5 7.5 8 9 4.5-1.5 8-4 8-9V6z"/></svg>',
			'Kelly'   => '<svg '.$s.'><path d="M12 3v18M5 8l7-5 7 5"/><path d="M7 21V11h10v10"/></svg>',
			'ים'      => '<svg '.$s.'><circle cx="12" cy="7" r="3"/><path d="M2 17c2-1.5 4-1.5 6 0s4 1.5 6 0 4-1.5 6 0"/><path d="M2 21c2-1.5 4-1.5 6 0s4 1.5 6 0 4-1.5 6 0"/></svg>',
			'פארק'    => '<svg '.$s.'><path d="M12 3a5 5 0 0 1 5 5c0 3-2.5 5-5 5s-5-2-5-5a5 5 0 0 1 5-5z"/><path d="M12 13v8M9 21h6"/></svg>',
			'מרינה'   => '<svg '.$s.'><path d="M12 3v13"/><path d="M12 6c3 0 6 2 7 5-2 0-4 1-7 5-3-4-5-5-7-5 1-3 4-5 7-5z"/><path d="M4 21c2-1.5 4-1.5 6 0s4 1.5 6 0"/></svg>',
		);
	}
}

if ( ! function_exists( 'nadlan_premium_catalog_data' ) ) {
	function nadlan_premium_catalog_data() {
		/* Curated tier, verified figures from the canonical DB (data/projects/).
		   Filterable so future projects join without a code release. */
		return apply_filters( 'nadlan_premium_catalog_projects', array(
			array(
				'slug' => 'rainbow-tel-aviv', 'name' => 'Rainbow תל אביב', 'dev' => 'ישראל קנדה',
				'area' => 'רובע שדה דב, קו ראשון לחוף', 'floors' => 39, 'units' => 459, 'delivery' => '2027',
				'price_note' => 'ממוצע נמכרות: 80,300 ₪ למ"ר כולל מע"מ (דוח שנתי 2025)',
				'rooms' => array( 3, 4, 5 ), 'sea' => true, 'park' => true, 'marina' => true,
				'fac' => array( 'לגונה ובריכות', 'ספא', 'חדר כושר', 'קולנוע', "קונסיירז'", 'מסחר', 'חניון', 'ממ"ד' ),
				'deal' => 'נמכרו 270 מתוך 459 (59%) עד סוף 2025, לפי דיווח רשמי',
			),
			array(
				'slug' => 'ashira-sde-dov', 'name' => 'ASHIRA שדה דב', 'dev' => 'אביסרור',
				'area' => 'רובע שדה דב, מול הים', 'floors' => 35, 'units' => 406, 'delivery' => '2028',
				'price_note' => 'אומדן אזור: כ-75,000 ₪ למ"ר (מדלן, לאימות מול היזם)',
				'rooms' => array( 2, 3, 4, 5 ), 'sea' => true, 'park' => true, 'marina' => true,
				'fac' => array( 'בריכה', 'ספא', 'חדר כושר', 'קולנוע', "לאונג'", 'אזורי ילדים', 'חניון', 'ממ"ד' ),
				'deal' => '4 בניינים במדרוג 8/8/16/35 קומות, תכנון אבנר ישר',
			),
			array(
				'slug' => 'dimri-yama-sde-dov', 'name' => 'Dimri Yama שדה דב', 'dev' => 'י.ח דמרי',
				'area' => 'רובע שדה דב', 'floors' => 39, 'units' => 458, 'delivery' => '2028',
				'price_note' => 'טרם פורסם מחירון; עוגן אזורי: 80,300 ₪ למ"ר (Rainbow, דיווח רשמי)',
				'rooms' => array( 3, 4, 5 ), 'sea' => true, 'park' => true, 'marina' => true,
				'fac' => array( 'בריכה', 'חדר כושר', 'לובי Kelly Hoppen', 'אזורי ילדים', 'חניון', 'ממ"ד' ),
				'deal' => 'עיצוב פנים בחתימת Kelly Hoppen CBE',
			),
			array(
				'slug' => 'einstein-tower', 'name' => 'EINSTEIN TOWER תל אביב', 'dev' => 'קבוצת חג׳ג׳',
				'catalog_state' => 'private_stage', 'catalog_gate_meta' => '_nl_flagship_v3_ready',
				'area' => 'פינת איינשטיין–לוי אשכול, צפון תל אביב', 'floors' => 28, 'units' => 215, 'delivery' => '2030',
				'delivery_label' => 'הערכת החברה: רבעון 3, 2030 (נכון ל-31.12.2025)',
				'price_note' => '215 יחידות בפרויקט 33א׳ (דוח שנתי 2025); נתוני מלאי ומחיר מוצגים רק לאחר אימות',
				'rooms' => array(), 'sea' => false, 'park' => false, 'marina' => false,
				'fac' => array( 'מסחר' ),
				'deal' => 'מגדל בן 28 קומות ושני בנייני בוטיק בני 13 קומות מעל בסיס מסחרי',
				'experience_label' => 'מודל החלטה תלת-ממדי',
				'link_label' => 'לעמוד המלא: מודל, סביבת קנייה ומפה ←',
			),
		) );
	}
}

if ( ! function_exists( 'nadlan_pc_row_public_ready' ) ) {
	/** A staged catalog record is registered in the hierarchy but cannot surface before read-back promotion. */
	function nadlan_pc_row_public_ready( $row, $post ) {
		if ( ! is_array( $row ) || ! is_object( $post ) ) { return false; }
		if ( ! isset( $row['catalog_state'] ) || 'private_stage' !== $row['catalog_state'] ) { return true; }
		$gate = isset( $row['catalog_gate_meta'] ) ? (string) $row['catalog_gate_meta'] : '';
		return '' !== $gate && '1' === (string) get_post_meta( (int) $post->ID, $gate, true );
	}
}

add_shortcode( 'nadlan_premium_catalog', function () {
	nadlan_bvr_mark_pc();
	$rows = nadlan_premium_catalog_data();
	// single source of truth with the facility-chips module (chips deep-link here)
	$fkeys = function_exists( 'nadlan_fc_keys' ) ? nadlan_fc_keys()
		: array( 'בריכה', 'ספא', 'חדר כושר', 'קולנוע', "קונסיירז'", 'לגונה', "לאונג'", 'אזורי ילדים', 'מסחר', 'חניון', 'ממ"ד' );
	ob_start(); ?>
<style>
.nlpc{max-width:1060px;margin:10px auto;font-family:var(--font-sans,Heebo,sans-serif);direction:rtl;color:#1B1A17}
.nlpc .bar{display:flex;flex-wrap:wrap;gap:8px;margin:14px 0 6px;align-items:center}
.nlpc .lbl{font-size:11.5px;letter-spacing:.12em;color:#9C7A3C;font-weight:700;margin-inline-end:4px}
.nlpc .f,.nlpc .fr{background:#fff;border:1px solid #E2DCD0;border-radius:999px;padding:7px 15px;font:inherit;font-size:13.5px;cursor:pointer}
.nlpc .f.on,.nlpc .fr.on{background:#1B1A17;color:#fff;border-color:#1B1A17}
.nlpc .f,.nlpc .fr{display:inline-flex;align-items:center;gap:6px;transition:all .15s}
.nlpc .f:hover,.nlpc .fr:hover{border-color:#9C7A3C;color:#9C7A3C}
.nlpc .f.on:hover,.nlpc .fr.on:hover{color:#E6D4AE}
.nlpc .ic{display:inline-flex;color:#9C7A3C}
.nlpc .f.on .ic,.nlpc .fr.on .ic{color:#E6D4AE}
.nlpc-fac .ic{margin-inline-end:4px;vertical-align:-2px}
.nlpc-card{transition:transform .2s,box-shadow .2s}
.nlpc-card:hover{transform:translateY(-2px);box-shadow:0 22px 48px rgba(27,26,23,.12)}
.nlpc-none{background:#F3EEE3;border:1px solid #E2DCD0;border-radius:12px;padding:16px 20px;font-size:14px;margin-bottom:14px}
#nlpc_active .pill{background:#9C7A3C;color:#fff;border-radius:999px;padding:4px 12px;font-size:12px;cursor:pointer}
#nlpc_active .pill:after{content:" ×";opacity:.8}
.nlpc .count{font-size:13px;color:#5C564D;margin:6px 0 14px}
.nlpc-card{display:grid;grid-template-columns:260px 1fr;background:#fff;border:1px solid #E2DCD0;border-radius:16px;overflow:hidden;margin-bottom:16px;box-shadow:0 14px 34px rgba(27,26,23,.06)}
.nlpc-card.hide{display:none}
.nlpc-media{background:#14130F center/cover no-repeat;min-height:210px;position:relative}
.nlpc-media em{position:absolute;bottom:10px;inset-inline-start:10px;font-style:normal;font-size:11px;background:rgba(20,19,15,.82);color:#E6D4AE;border-radius:6px;padding:4px 10px}
.nlpc-3d{position:absolute;top:10px;inset-inline-end:10px;width:64px;height:64px;border-radius:12px;background:#14130F center/cover no-repeat;border:1.5px solid #9C7A3C;box-shadow:0 3px 12px rgba(0,0,0,.35)}
.nlpc-3d b{position:absolute;bottom:-1px;inset-inline-end:-1px;font-size:9.5px;font-weight:800;letter-spacing:.4px;background:#9C7A3C;color:#14130F;border-radius:8px 0 10px 0;padding:2px 6px}
.nlpc-body{padding:18px 22px}
.nlpc-body h3{font-family:var(--font-serif,"Frank Ruhl Libre",serif);font-size:1.35rem;margin:0}
.nlpc-meta{font-size:13.5px;color:#5C564D;margin:3px 0 8px}
.nlpc-price{font-size:13px;color:#1B1A17;background:#F3EEE3;border-radius:8px;padding:6px 10px;display:inline-block}
.nlpc-fac{display:flex;flex-wrap:wrap;gap:6px;margin:10px 0}
.nlpc-fac span,.nlpc-fac a{font-size:12px;background:#FAF7F1;border:1px solid #E2DCD0;border-radius:999px;padding:4px 10px;color:inherit;text-decoration:none}
.nlpc-fac a{cursor:pointer;transition:border-color .15s,color .15s}
.nlpc-fac a:hover{border-color:#9C7A3C;color:#9C7A3C}
.nlpc-deal{font-size:12.5px;color:#5C564D;border-top:1px dashed #E2DCD0;padding-top:8px}
.nlpc-foot{display:flex;justify-content:space-between;align-items:center;margin-top:10px;flex-wrap:wrap;gap:8px}
.nlpc-langs{display:flex;gap:4px}
.nlpc-langs a{font-size:11px;border:1px solid #E2DCD0;border-radius:6px;padding:3px 7px;text-decoration:none;color:#5C564D}
.nlpc-go{color:#C2563A;font-weight:700;text-decoration:none;font-size:14.5px}
.nlpc-join{background:#14130F;color:#FAF7F1;border-radius:16px;padding:22px 26px;margin-top:8px}
.nlpc-join b{font-family:var(--font-serif,serif);font-size:1.2rem;color:#E6D4AE}
.nlpc-join p{font-size:13.5px;color:#CFC6B4;margin:6px 0 0}
@media(max-width:700px){.nlpc-card{grid-template-columns:1fr}}
.nlpc-media.is-poster{background-size:contain;background-color:#14130F;background-repeat:no-repeat;background-position:center}
</style>
<div class="nlpc" id="nlpc">
  <?php $icons = nadlan_pc_icons(); ?>
  <div class="bar"><span class="lbl">מתקנים ושירותים</span>
  <?php foreach ( $fkeys as $i => $k ) : ?><button class="f" data-fi="<?php echo (int) $i; ?>"><i class="ic"><?php echo isset( $icons[ $k ] ) ? $icons[ $k ] : ''; ?></i><?php echo esc_html( $k ); ?></button><?php endforeach; ?>
  </div>
  <div class="bar"><span class="lbl">חדרים</span>
    <button class="fr" data-r="2">2</button><button class="fr" data-r="3">3</button><button class="fr" data-r="4">4</button><button class="fr" data-r="5">5</button>
    <span class="lbl" style="margin-inline-start:12px">אכלוס</span>
		<button class="fr" data-d="2027">2027</button><button class="fr" data-d="2028">2028</button><button class="fr" data-d="2030">2030</button>
    <span class="lbl" style="margin-inline-start:12px">יזם</span>
		<button class="fr" data-dev="ישראל קנדה">ישראל קנדה</button><button class="fr" data-dev="אביסרור">אביסרור</button><button class="fr" data-dev="י.ח דמרי">י.ח דמרי</button><button class="fr" data-dev="קבוצת חג׳ג׳">קבוצת חג׳ג׳</button>
  </div>
  <div class="bar"><span class="lbl">בסביבה</span>
    <button class="fr" data-sea="1"><i class="ic"><?php echo $icons['ים']; ?></i>חוף הים במרחק הליכה</button>
    <button class="fr" data-park="1"><i class="ic"><?php echo $icons['פארק']; ?></i>פארק הירקון</button>
    <button class="fr" data-marina="1"><i class="ic"><?php echo $icons['מרינה']; ?></i>מרינה ונמל תל אביב</button>
    <span class="lbl" style="margin-inline-start:12px">מיון</span>
    <select id="nlpc_sort" class="fr" style="cursor:pointer">
      <option value="">מומלץ</option><option value="delivery">אכלוס מוקדם</option>
      <option value="floors">הכי גבוה</option><option value="units">הכי גדול</option>
    </select>
  </div>
  <div class="bar" id="nlpc_active" style="min-height:10px"></div>
  <div class="count" id="nlpc_count"></div>
  <div class="nlpc-none" id="nlpc_none" style="display:none">אין פרויקט בקטלוג הפרימיום שעונה על כל הסינונים. נסו להסיר סינון, או עברו ל<a href="/projects/">קטלוג המלא</a>.</div>
  <?php foreach ( $rows as $p ) :
    $post = get_page_by_path( $p['slug'], OBJECT, 'nadlan_project' );
    if ( ! $post ) { continue; }
	if ( ! nadlan_pc_row_public_ready( $p, $post ) ) { continue; }
    $link   = get_permalink( $post );
    // IMAGERY PIVOT (owner decision 1, 2026-07-07): the REAL model render
    // leads the card; the sketch plate is the secondary chip, not the face.
    // small badge so the buyer knows a live 3D selection experience waits inside.
    $poster = esc_url( (string) get_post_meta( $post->ID, 'project_model_poster', true ) );
    $plate  = esc_url( (string) get_post_meta( $post->ID, 'project_3d_image', true ) );
		$hero   = $poster !== '' ? $poster : $plate;
		$experience_label = isset( $p['experience_label'] ) ? $p['experience_label'] : 'בחירת דירה בתלת ממד';
		$link_label = isset( $p['link_label'] ) ? $p['link_label'] : 'לעמוד המלא: מודל, חזית, מאמר ומפה ←';
    $fattrs = '';
    foreach ( $fkeys as $i => $k ) { foreach ( $p['fac'] as $f ) { if ( strpos( $f, $k ) !== false ) { $fattrs .= ' data-f' . $i . '="1"'; break; } } }
    $langs = array();
    foreach ( array( 'HE' => '', 'EN' => '-en', 'FR' => '-fr', 'RU' => '-ru', 'AR' => '-ar' ) as $ll => $suf ) {
      $sib = get_page_by_path( $p['slug'] . $suf, OBJECT, 'nadlan_project' );
      if ( $sib && 'publish' === get_post_status( $sib ) ) { $langs[ $ll ] = get_permalink( $sib ); }
    }
  ?>
  <article class="nlpc-card" data-rooms="<?php echo esc_attr( implode( ',', $p['rooms'] ) ); ?>" data-delivery="<?php echo esc_attr( $p['delivery'] ); ?>" data-sea="<?php echo ! empty( $p['sea'] ) ? 1 : 0; ?>" data-park="<?php echo ! empty( $p['park'] ) ? 1 : 0; ?>" data-marina="<?php echo ! empty( $p['marina'] ) ? 1 : 0; ?>" data-dev="<?php echo esc_attr( $p['dev'] ); ?>" data-floors="<?php echo (int) $p['floors']; ?>" data-units="<?php echo (int) $p['units']; ?>"<?php echo $fattrs; ?>>
    <div class="nlpc-media<?php echo ( $hero && $hero === $poster ) ? ' is-poster' : ''; ?>" style="background-image:url('<?php echo $hero; ?>')"><em><?php echo esc_html( $experience_label ); ?></em><?php if ( $plate && $plate !== $hero ) : ?><span class="nlpc-3d" style="background-image:url('<?php echo $plate; ?>')" aria-hidden="true"><b>◆</b></span><?php endif; ?></div>
    <div class="nlpc-body">
      <h3><?php echo esc_html( $p['name'] ); ?></h3>
      <?php $delivery_label = isset( $p['delivery_label'] ) ? $p['delivery_label'] : 'אכלוס ' . $p['delivery']; ?>
      <div class="nlpc-meta"><?php echo esc_html( $p['dev'] . ' · ' . $p['area'] . ' · ' . $p['floors'] . ' קומות · ' . $p['units'] . ' דירות · ' . $delivery_label ); ?></div>
      <span class="nlpc-price"><?php echo esc_html( $p['price_note'] ); ?></span>
      <div class="nlpc-fac"><?php foreach ( $p['fac'] as $f ) { $ic=''; foreach ( $icons as $k2 => $svg ) { if ( strpos( $f, $k2 ) !== false ) { $ic='<i class="ic">'.$svg.'</i>'; break; } }
        // facility chips are CLICKABLE (owner, 2026-07-29): a chip filters the catalog by
        // that facility. Labels with no canonical filter key stay plain spans.
        $ck = function_exists( 'nadlan_fc_canonical' ) ? nadlan_fc_canonical( array( $f ) ) : array();
        if ( $ck && function_exists( 'nadlan_fc_premium_url' ) ) {
          echo '<a href="' . esc_url( nadlan_fc_premium_url( $ck[0] ) ) . '" title="' . esc_attr( 'סינון הקטלוג: ' . $ck[0] ) . '">' . $ic . esc_html( $f ) . '</a>';
        } else { echo '<span>' . $ic . esc_html( $f ) . '</span>'; } } ?></div>
      <div class="nlpc-deal"><?php echo esc_html( $p['deal'] ); ?></div>
      <div class="nlpc-foot">
        <a class="nlpc-go" href="<?php echo esc_url( $link ); ?>"><?php echo esc_html( $link_label ); ?></a>
        <?php if ( function_exists( 'nadlan_sdedov_card_tour_btn' ) ) { echo nadlan_sdedov_card_tour_btn( $post ); } // phpcs:ignore ?>
        <div class="nlpc-langs"><?php foreach ( $langs as $ll => $lu ) { echo '<a href="' . esc_url( $lu ) . '">' . esc_html( $ll ) . '</a>'; } ?></div>
      </div>
    </div>
  </article>
  <?php endforeach; ?>
  <div class="nlpc-join"><b>הפרויקט שלכם שייך לכאן?</b>
    <p>הקטלוג הפרימיום כולל רק פרויקטים עם חוויית בחירה מלאה: מודל תלת ממדי אינטראקטיבי, מאמר מקיף בחמש שפות, נתונים מאומתים ומפה חכמה. יזמים ומשווקים מוזמנים לפנות דרך <a href="/advertise/" style="color:#E6D4AE">עמוד הפרסום ליזמים</a>.</p>
  </div>
</div>
<?php
// the live drone map under the premium grid (owner 2026-07-06)
if ( function_exists( 'nadlan_drone_map_band' ) ) { echo nadlan_drone_map_band( 'showcase', 'he' ); } // phpcs:ignore WordPress.Security.EscapeOutput
return ob_get_clean();
} );

if ( ! function_exists( 'nadlan_bvr_mark_pc' ) ) {
	function nadlan_bvr_mark_pc() { static $on = false; $prev = $on; $on = true; return $prev; }
	function nadlan_pc_needed() { return nadlan_bvr_mark_pc() || false; }
}
add_action( 'wp_footer', function () {
	static $checked = false; if ( $checked ) { return; } $checked = true;
	/* only print if the shortcode ran on this request */
	if ( ! nadlan_bvr_mark_pc() ) { return; }
	?>
<script>
(function(){
var st={f:new Set(),r:new Set(),d:new Set(),dev:new Set(),sea:false,park:false,marina:false};
function pills(){var host=document.getElementById('nlpc_active');if(!host)return;host.innerHTML='';
 document.querySelectorAll('#nlpc .f.on,#nlpc .fr.on').forEach(function(b){
  var p=document.createElement('span');p.className='pill';p.textContent=b.textContent.trim();
  p.onclick=function(){b.click()};host.appendChild(p);});}
function apply(){var n=0;
 document.querySelectorAll('.nlpc-card').forEach(function(c){var ok=true;
  st.f.forEach(function(i){if(!c.hasAttribute('data-f'+i))ok=false});
  if(st.r.size){var rs=c.dataset.rooms.split(',');var hit=false;st.r.forEach(function(r){if(rs.indexOf(r)>=0)hit=true});if(!hit)ok=false}
  if(st.d.size&&!st.d.has(c.dataset.delivery))ok=false;
  if(st.dev.size&&!st.dev.has(c.dataset.dev))ok=false;
  if(st.sea&&c.dataset.sea!=='1')ok=false;
  if(st.park&&c.dataset.park!=='1')ok=false;
  if(st.marina&&c.dataset.marina!=='1')ok=false;
  c.classList.toggle('hide',!ok);if(ok)n++;});
 var el=document.getElementById('nlpc_count');if(el)el.textContent=n+' פרויקטים מתאימים';
 var none=document.getElementById('nlpc_none');if(none)none.style.display=n?'none':'block';
 pills();}
function sortCards(){var by=document.getElementById('nlpc_sort').value;if(!by)return;
 var wrap=document.querySelector('#nlpc .nlpc-card').parentNode;
 var cards=[].slice.call(document.querySelectorAll('.nlpc-card'));
 cards.sort(function(a,b2){
  if(by==='delivery')return (+a.dataset.delivery)-(+b2.dataset.delivery);
  if(by==='floors')return (+b2.dataset.floors)-(+a.dataset.floors);
  return (+b2.dataset.units)-(+a.dataset.units);});
 cards.forEach(function(c){wrap.insertBefore(c,document.querySelector('.nlpc-join'))});}
document.querySelectorAll('#nlpc .f').forEach(function(b){b.onclick=function(){var i=b.dataset.fi;b.classList.toggle('on');b.classList.contains('on')?st.f.add(i):st.f['delete'](i);apply();};});
document.querySelectorAll('#nlpc .fr[data-r]').forEach(function(b){b.onclick=function(){b.classList.toggle('on');b.classList.contains('on')?st.r.add(b.dataset.r):st.r['delete'](b.dataset.r);apply();};});
document.querySelectorAll('#nlpc .fr[data-d]').forEach(function(b){b.onclick=function(){b.classList.toggle('on');b.classList.contains('on')?st.d.add(b.dataset.d):st.d['delete'](b.dataset.d);apply();};});
document.querySelectorAll('#nlpc .fr[data-dev]').forEach(function(b){b.onclick=function(){b.classList.toggle('on');b.classList.contains('on')?st.dev.add(b.dataset.dev):st.dev['delete'](b.dataset.dev);apply();};});
[['data-sea','sea'],['data-park','park'],['data-marina','marina']].forEach(function(t){
 var b=document.querySelector('#nlpc .fr['+t[0]+']');if(b)b.onclick=function(){b.classList.toggle('on');st[t[1]]=b.classList.contains('on');apply();};});
var so=document.getElementById('nlpc_sort');if(so)so.onchange=sortCards;
/* DEEP LINK (facility chips, 2026-07-29): /premium/?fac=NAME[,NAME] pre-applies
   the matching facility filter buttons - chips anywhere on the site land here
   with the filter already on. Match by button TEXT, not index (reorder-proof). */
try{
 (new URLSearchParams(location.search).get('fac')||'').split(',').forEach(function(n){
  n=n.trim();if(!n)return;
  document.querySelectorAll('#nlpc .f').forEach(function(b){
   if(b.textContent.trim()===n&&!b.classList.contains('on'))b.click();});});
}catch(e){}
/* card facility chips: on this page a chip toggles the filter IN PLACE
   (no reload); anywhere else the chip's real href navigates here. */
document.addEventListener('click',function(e){
 var a=e.target.closest('.nlpc-fac a');if(!a)return;e.preventDefault();
 var n=null;try{n=new URL(a.href).searchParams.get('fac')}catch(err){}
 if(!n){return}
 var hit=null;document.querySelectorAll('#nlpc .f').forEach(function(b){if(b.textContent.trim()===n)hit=b});
 if(hit){if(!hit.classList.contains('on'))hit.click();hit.scrollIntoView({behavior:'smooth',block:'center'})}
 else{window.location=a.href}});
apply();
})();
</script>
<?php }, 61 );
