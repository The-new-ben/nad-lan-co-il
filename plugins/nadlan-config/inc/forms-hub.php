<?php
/**
 * nadlan-config - THE LIFE OF A BUILDING: real-estate forms and building approvals on /forms/ (HAD-768, 1.72.694).
 * Claude Design canvas https://claude.ai/artifact/8DYH5mbbkKYmSY2vvcKiEW (v2 "מחזור החיים של בניין", NadLan Instruments system).
 * Ben, 17.11.2026: "not a page with five forms: map the whole life of a residential building, from city planning to demolition,
 * every approval, form, report and fee, with what only a 40-year expert knows next to each item, and a fairness declaration".
 *
 * [nadlan_forms] prints everything in the page HTML (crawlable, whole without JS):
 *  - the spine: one tile per stage (11 stages, a small line drawing of the building at that stage), each an anchor (#s-<stage>);
 *  - search + role chips (developer, buyer, owner, house committee) + kind chips (approval, form, report, fee, deadline ...);
 *  - the "what do I need now" instrument (forms.js: role + stage -> the checklist, the deadlines, copy / WhatsApp / print);
 *  - per stage: its items, each a card with its own anchor (#i-<id>): kind, authority, what it is, the expert note, the official
 *    form (the state's file, byte-identical, under its original file name in the Media Library) and the official page; details
 *    hold who, when, cost, the legal basis, the pitfall, the sources and the "link to this item" code;
 *  - the fairness declaration, with the counts computed from the data.
 * Data: assets/forms/forms.json (docs/research/2026-11-17-gov-forms/build_forms_data.py, from the gov.il inventory and the four
 * research bands; every fact carries its source). Schema: CollectionPage + ItemList of the official documents (DigitalDocument,
 * publisher = the government body, isBasedOn = the official page) + the page's FAQPage. Loaded by inc/directory.php (if present).
 */
if ( ! defined( 'ABSPATH' ) ) { exit; }

if ( ! function_exists( 'nadlan_fh_data' ) ) {

	function nadlan_fh_data() {
		static $d = null;
		if ( null !== $d ) { return $d; }
		$f = dirname( __DIR__ ) . '/assets/forms/forms.json';
		$j = is_readable( $f ) ? json_decode( (string) file_get_contents( $f ), true ) : null;
		$d = is_array( $j ) && ! empty( $j['items'] ) ? $j : array( 'items' => array(), 'stages' => array(), 'roles' => array(), 'kinds' => array() );
		return $d;
	}

	function nadlan_fh_on_page() {
		if ( ! is_singular( 'page' ) ) { return false; }
		$p = get_post();
		return $p && false !== strpos( (string) $p->post_content, '[nadlan_forms' );
	}

	function nadlan_fh_ver( $rel ) {
		$p = dirname( __DIR__ ) . '/assets/forms/' . $rel;
		return ( defined( 'NADLAN_CONFIG_VERSION' ) ? NADLAN_CONFIG_VERSION : '1' ) . '.' . ( is_readable( $p ) ? filemtime( $p ) : 0 );
	}

	function nadlan_fh_kb( $bytes ) {
		$b = (int) $bytes;
		if ( $b <= 0 ) { return ''; }
		return $b >= 1048576 ? number_format( $b / 1048576, 1 ) . ' MB' : max( 1, (int) round( $b / 1024 ) ) . ' KB';
	}

	/** the small drawing of the building at each stage (line drawing on the planning-map colours; decorative). */
	function nadlan_fh_pic( $stage ) {
		$k = '#12202A';
		$p = array(
			'plan'     => '<rect x="6" y="10" width="66" height="28" fill="#F2D15A" opacity=".55"/><rect x="6" y="10" width="66" height="28" fill="none" stroke="' . $k . '" stroke-dasharray="3 3"/><path d="M6 24h66M39 10v28" stroke="#4F9A5C" stroke-width="2"/>',
			'permit'   => '<rect x="16" y="6" width="46" height="32" fill="#fff" stroke="' . $k . '"/><path d="M22 14h28M22 20h34M22 26h20" stroke="#2F6F86" stroke-width="2"/><circle cx="53" cy="31" r="5" fill="none" stroke="#C42550" stroke-width="2"/>',
			'start'    => '<path d="M8 38h62" stroke="' . $k . '" stroke-width="2"/><path d="M22 38V8M23 8h34M50 8v10" stroke="' . $k . '" stroke-width="2"/><rect x="44" y="18" width="12" height="8" fill="none" stroke="' . $k . '"/><path d="M30 38v-6h14v6" fill="none" stroke="#C42550"/>',
			'sale'     => '<rect x="20" y="14" width="34" height="24" fill="none" stroke="' . $k . '" stroke-dasharray="3 2"/><path d="M8 38h62" stroke="' . $k . '" stroke-width="2"/><rect x="48" y="4" width="22" height="13" fill="#F2D15A" stroke="' . $k . '"/><path d="M52 10h14" stroke="' . $k . '"/>',
			'build'    => '<rect x="24" y="8" width="30" height="30" fill="#fff" stroke="' . $k . '"/><path d="M24 18h30M24 28h30M34 8v30M44 8v30" stroke="' . $k . '" stroke-width=".8"/><path d="M8 38h62" stroke="' . $k . '" stroke-width="2"/><path d="M18 38V12M60 38V12" stroke="#5E6A75" stroke-dasharray="2 2"/>',
			'finish'   => '<rect x="24" y="8" width="30" height="30" fill="#fff" stroke="' . $k . '"/><path d="M29 13h6v5h-6zM43 13h6v5h-6zM29 23h6v5h-6zM43 23h6v5h-6z" fill="#2F6F86"/><path d="M36 38v-7h6v7" fill="none" stroke="' . $k . '"/><path d="M8 38h62" stroke="' . $k . '" stroke-width="2"/>',
			'register' => '<rect x="12" y="6" width="38" height="32" fill="#fff" stroke="' . $k . '"/><path d="M18 14h26M18 20h26M18 26h16" stroke="' . $k . '"/><rect x="40" y="22" width="26" height="16" fill="#8E7CC3" opacity=".85"/><path d="M45 30h16" stroke="#fff" stroke-width="2"/>',
			'live'     => '<rect x="24" y="8" width="30" height="30" fill="#fff" stroke="' . $k . '"/><path d="M29 13h6v5h-6zM43 13h6v5h-6zM29 23h6v5h-6zM43 23h6v5h-6z" fill="#F2D15A"/><path d="M8 38h62" stroke="' . $k . '" stroke-width="2"/><circle cx="64" cy="18" r="6" fill="#4F9A5C"/>',
			'change'   => '<rect x="24" y="14" width="30" height="24" fill="#fff" stroke="' . $k . '"/><rect x="24" y="4" width="18" height="10" fill="none" stroke="#C42550" stroke-dasharray="2 2"/><path d="M8 38h62" stroke="' . $k . '" stroke-width="2"/>',
			'renewal'  => '<rect x="10" y="20" width="22" height="18" fill="#fff" stroke="' . $k . '"/><rect x="42" y="4" width="26" height="34" fill="#fff" stroke="#2F6F86" stroke-width="2"/><path d="M34 28h6M37 25l3 3-3 3" stroke="' . $k . '"/><path d="M6 38h66" stroke="' . $k . '" stroke-width="2"/>',
			'end'      => '<path d="M24 38V18l10-6 10 8 10-4v22" fill="none" stroke="' . $k . '" stroke-dasharray="3 2"/><path d="M8 38h62" stroke="' . $k . '" stroke-width="2"/><path d="M60 6l-8 12" stroke="#C42550" stroke-width="2"/><circle cx="62" cy="5" r="3" fill="#C42550"/>',
		);
		return '<svg width="78" height="44" viewBox="0 0 78 44" aria-hidden="true" focusable="false">' . ( isset( $p[ $stage ] ) ? $p[ $stage ] : $p['plan'] ) . '</svg>';
	}

	/** one item card */
	function nadlan_fh_card( $it, $d ) {
		$id    = sanitize_title( $it['id'] );
		$kinds = isset( $d['kinds'] ) ? $d['kinds'] : array();
		$kl    = isset( $kinds[ $it['kind'] ] ) ? $kinds[ $it['kind'] ] : $it['kind'];
		$roles = isset( $it['roles'] ) ? implode( ' ', array_map( 'sanitize_key', (array) $it['roles'] ) ) : '';
		$f     = isset( $it['form'] ) && is_array( $it['form'] ) ? $it['form'] : array();
		$kw    = trim( $it['title'] . ' ' . ( isset( $f['num'] ) ? $f['num'] . ' ' : '' ) . ( isset( $f['name'] ) ? $f['name'] . ' ' : '' ) . ( isset( $it['authority'] ) ? $it['authority'] . ' ' : '' ) . ( isset( $it['kw'] ) ? $it['kw'] . ' ' : '' ) . $kl );
		$url   = home_url( '/forms/#i-' . $id );
		$h  = '<article class="nlfm-card k-' . esc_attr( sanitize_key( $it['kind'] ) ) . '" id="i-' . esc_attr( $id ) . '" data-st="' . esc_attr( $it['stage'] ) . '" data-r="' . esc_attr( $roles ) . '" data-kd="' . esc_attr( $it['kind'] ) . '" data-k="' . esc_attr( $kw ) . '">';
		$h .= '<div class="nlfm-card__top"><span class="nlfm-tag">' . esc_html( $kl ) . '</span>' . ( ! empty( $it['authority'] ) ? '<span class="nlfm-auth">' . esc_html( $it['authority'] ) . '</span>' : '' ) . ( ! empty( $f['num'] ) ? '<span class="nlfm-num" dir="ltr">' . esc_html( $f['num'] ) . '</span>' : '' ) . ( ! empty( $it['partial'] ) ? '<span class="nlfm-part">אומת חלקית: ראו את המקורות</span>' : '' ) . '</div>';
		$h .= '<h3>' . esc_html( $it['title'] ) . '</h3>';
		if ( ! empty( $it['what'] ) ) { $h .= '<p class="nlfm-what">' . esc_html( $it['what'] ) . '</p>'; }
		if ( ! empty( $it['expert'] ) ) { $h .= '<div class="nlfm-expert"><span>הערת מומחה</span><p>' . esc_html( $it['expert'] ) . '</p></div>'; }
		$acts = '';
		if ( ! empty( $f['file'] ) ) {
			$ext = isset( $f['ext'] ) ? strtoupper( $f['ext'] ) : '';
			$acts .= '<a class="nlfm-btn is-main" href="' . esc_url( $f['file'] ) . '" download>' . esc_html( ! empty( $f['num'] ) ? 'הורדת טופס ' . $f['num'] : 'הורדת הטופס' ) . ( $ext ? ' <small dir="ltr">' . esc_html( trim( $ext . ' ' . nadlan_fh_kb( isset( $f['size'] ) ? $f['size'] : 0 ) ) ) . '</small>' : '' ) . '</a>';
		}
		if ( ! empty( $it['online'] ) ) { $acts .= '<a class="nlfm-btn" href="' . esc_url( $it['online'] ) . '" rel="noopener" target="_blank">הגשה מקוונת</a>'; }
		if ( ! empty( $it['official'] ) ) { $acts .= '<a class="nlfm-link" href="' . esc_url( $it['official'] ) . '" rel="noopener" target="_blank">בעמוד הרשמי</a>'; }
		if ( $acts ) { $h .= '<div class="nlfm-acts">' . $acts . '</div>'; }
		$h .= '<details class="nlfm-more"><summary>מי, מתי, כמה, הבסיס בחוק ואיפה נתקעים</summary><div class="nlfm-more__in">';
		foreach ( array( 'who' => 'מי', 'when' => 'מתי וכמה זמן', 'cost' => 'עלות או אגרה', 'basis' => 'הבסיס בחוק' ) as $k => $lab ) {
			if ( ! empty( $it[ $k ] ) ) { $h .= '<p><b>' . esc_html( $lab ) . ':</b> ' . esc_html( $it[ $k ] ) . '</p>'; }
		}
		if ( ! empty( $it['pitfall'] ) ) { $h .= '<div class="nlfm-pit"><span>איפה נתקעים</span><p>' . esc_html( $it['pitfall'] ) . '</p></div>'; }
		if ( ! empty( $it['related'] ) ) {
			$r = array();
			foreach ( (array) $it['related'] as $x ) { $r[] = '<a href="' . esc_url( home_url( $x[0] ) ) . '">' . esc_html( $x[1] ) . '</a>'; }
			$h .= '<p class="nlfm-rel"><b>באתר:</b> ' . implode( ' · ', $r ) . '</p>';
		}
		if ( ! empty( $it['sources'] ) ) {
			$h .= '<p class="nlfm-src"><b>מקורות</b>' . ( ! empty( $d['checked_he'] ) ? ' (נבדקו ' . esc_html( $d['checked_he'] ) . ')' : '' ) . ':</p><ol class="nlfm-srcs">';
			foreach ( (array) $it['sources'] as $s ) { $h .= '<li><a href="' . esc_url( $s['url'] ) . '" rel="noopener" target="_blank">' . esc_html( $s['title'] ) . '</a></li>'; }
			$h .= '</ol>';
		}
		$h .= '<div class="nlfm-share" data-fm-share></div>'; // forms.js fills it on open: copy link, WhatsApp and the link code for other sites
		return $h . '</div></details></article>';
	}

	function nadlan_fh_counts( $d ) {
		$src = array(); $forms = 0;
		foreach ( $d['items'] as $it ) {
			foreach ( (array) ( isset( $it['sources'] ) ? $it['sources'] : array() ) as $s ) { $src[ $s['url'] ] = 1; }
			if ( ! empty( $it['form']['file'] ) ) { $forms++; }
		}
		return array( 'items' => count( $d['items'] ), 'stages' => count( $d['stages'] ), 'forms' => $forms, 'sources' => count( $src ) );
	}

	add_shortcode( 'nadlan_forms', function () {
		$d = nadlan_fh_data();
		if ( empty( $d['items'] ) ) { return ''; }
		$c = nadlan_fh_counts( $d );
		$by = array();
		foreach ( $d['items'] as $it ) { $by[ $it['stage'] ][] = $it; }
		$h  = '<section class="nlfm" id="nlfm" dir="rtl" lang="he" aria-label="טפסים ואישורים לאורך חיי הבניין">';
		$h .= '<p class="nlfm-count"><bdi>' . (int) $c['stages'] . '</bdi> שלבים · <bdi>' . (int) $c['items'] . '</bdi> פריטים · <bdi>' . (int) $c['forms'] . '</bdi> טפסים רשמיים להורדה · <bdi>' . (int) $c['sources'] . '</bdi> מקורות · עודכן ' . esc_html( isset( $d['updated_he'] ) ? $d['updated_he'] : '' ) . '</p>';
		// the spine
		$h .= '<nav class="nlfm-spine" aria-label="ציר החיים של הבניין"><ol>';
		foreach ( $d['stages'] as $s ) {
			$n = isset( $by[ $s['id'] ] ) ? count( $by[ $s['id'] ] ) : 0;
			$h .= '<li><a href="#s-' . esc_attr( $s['id'] ) . '" data-fm-stage="' . esc_attr( $s['id'] ) . '">' . nadlan_fh_pic( $s['id'] ) . '<span class="n" dir="ltr">' . esc_html( $s['n'] ) . '</span><span class="t">' . esc_html( $s['name'] ) . '</span><span class="c"><bdi>' . $n . '</bdi> פריטים</span></a></li>';
		}
		$h .= '</ol></nav>';
		// find
		$h .= '<div class="nlfm-find"><label class="nlfm-q"><span>חיפוש</span><input id="nlfm-q" type="search" inputmode="search" autocomplete="off" placeholder="שם, מספר טופס או נושא: 7002, תעודת גמר, היטל השבחה"></label>';
		$h .= '<div class="nlfm-chips" role="group" aria-label="מי אתם"><button type="button" class="nlfm-chip" data-fm-r="" aria-pressed="true">כולם</button>';
		foreach ( $d['roles'] as $r ) { $h .= '<button type="button" class="nlfm-chip" data-fm-r="' . esc_attr( $r['id'] ) . '" aria-pressed="false">' . esc_html( $r['name'] ) . '</button>'; }
		$h .= '</div><div class="nlfm-chips is-k" role="group" aria-label="סוג"><button type="button" class="nlfm-chip" data-fm-kd="" aria-pressed="true">הכול</button>';
		$kc = array(); foreach ( $d['items'] as $it ) { $kc[ $it['kind'] ] = ( isset( $kc[ $it['kind'] ] ) ? $kc[ $it['kind'] ] : 0 ) + 1; }
		foreach ( $d['kinds'] as $k => $lab ) { if ( ! empty( $kc[ $k ] ) ) { $h .= '<button type="button" class="nlfm-chip" data-fm-kd="' . esc_attr( $k ) . '" aria-pressed="false">' . esc_html( $lab ) . ' <bdi>' . (int) $kc[ $k ] . '</bdi></button>'; } }
		$h .= '</div><p class="nlfm-none" id="nlfm-none" hidden>לא מצאנו. נסו מילה אחת, מספר טופס, או נקו את הסינון.</p></div>';
		// the instrument
		$h .= '<div class="nlfm-wiz" id="nlfm-wiz"><h2 class="nlfm-wiz__h">מה אני צריך עכשיו?</h2><p class="nlfm-wiz__lead">בחרו מי אתם ובאיזה שלב הבניין, ותקבלו את רשימת האישורים, הטפסים, הדיווחים והמועדים של השלב, לסימון, להעתקה, לוואטסאפ או להדפסה.</p><div id="nlfm-wiz-in"></div></div>';
		// the key numbers (a table: the format AI answers and featured snippets lift as is)
		if ( ! empty( $d['facts'] ) ) {
			$h .= '<div class="nlfm-facts" id="numbers"><h2>המספרים שחשוב לדעת</h2><p class="nlfm-facts__p">המועדים, הספים והרובים שקובעים את הלו"ז ואת הכסף בחיי הבניין, כל אחד עם הסעיף והמקור הרשמי.</p><div class="nlfm-facts__wrap"><table><thead><tr><th scope="col">המספר</th><th scope="col">מה הוא קובע</th><th scope="col">הבסיס</th></tr></thead><tbody>';
			foreach ( $d['facts'] as $f ) {
				$h .= '<tr><th scope="row"><bdi>' . esc_html( $f['n'] ) . '</bdi></th><td>' . esc_html( $f['t'] ) . ( ! empty( $f['go'] ) ? ' <a href="#s-' . esc_attr( $f['go'] ) . '">לשלב</a>' : '' ) . '</td><td><a href="' . esc_url( $f['src'] ) . '" rel="noopener" target="_blank">' . esc_html( $f['st'] ) . '</a></td></tr>';
			}
			$h .= '</tbody></table></div><p class="nlfm-src">נבדק ' . esc_html( isset( $d['checked_he'] ) ? $d['checked_he'] : '' ) . '. מספר שלא מצאנו לו מקור רשמי לא נכנס לטבלה.</p></div>';
		}
		// the stages
		foreach ( $d['stages'] as $s ) {
			if ( empty( $by[ $s['id'] ] ) ) { continue; }
			$h .= '<div class="nlfm-stage" id="s-' . esc_attr( $s['id'] ) . '" data-st="' . esc_attr( $s['id'] ) . '"><div class="nlfm-stage__h"><span class="n" dir="ltr">' . esc_html( $s['n'] ) . '</span><h2>' . esc_html( $s['name'] ) . '</h2></div>';
			if ( ! empty( $s['lead'] ) ) { $h .= '<p class="nlfm-stage__p">' . esc_html( $s['lead'] ) . '</p>'; }
			if ( ! empty( $s['related'] ) ) {
				$r = array(); foreach ( (array) $s['related'] as $x ) { $r[] = '<a href="' . esc_url( home_url( $x[0] ) ) . '">' . esc_html( $x[1] ) . '</a>'; }
				$h .= '<p class="nlfm-rel">המדריכים שלנו לשלב: ' . implode( ' · ', $r ) . '</p>';
			}
			$k = 0; $all = count( $by[ $s['id'] ] );
			foreach ( $by[ $s['id'] ] as $it ) { $card = nadlan_fh_card( $it, $d ); if ( $k++ >= 3 ) { $card = str_replace( '<article class="nlfm-card ', '<article class="nlfm-card is-more ', $card ); } $h .= $card; }
			if ( $all > 3 ) { $h .= '<button type="button" class="nlfm-morebtn" data-fm-more="' . esc_attr( $s['id'] ) . '">הצגת כל <bdi>' . (int) $all . '</bdi> הפריטים בשלב ' . esc_html( $s['name'] ) . '</button>'; }
			$h .= '</div>';
		}
		// fairness declaration
		$h .= '<div class="nlfm-fair" id="fairness"><h2>הצהרת הגינות</h2>';
		foreach ( (array) ( isset( $d['fairness'] ) ? $d['fairness'] : array() ) as $p ) { $h .= '<p>' . esc_html( $p ) . '</p>'; }
		$h .= '<p class="nlfm-fair__n"><bdi>' . (int) $c['items'] . '</bdi> פריטים · <bdi>' . (int) $c['sources'] . '</bdi> מקורות · <bdi>' . (int) $c['forms'] . '</bdi> טפסים רשמיים · נבדק ' . esc_html( isset( $d['checked_he'] ) ? $d['checked_he'] : '' ) . '</p></div>';
		$h .= '<script type="application/json" id="nlfm-data">' . wp_json_encode( array(
			'items' => array_map( function ( $it ) {
				return array( 'id' => sanitize_title( $it['id'] ), 'st' => $it['stage'], 'kd' => $it['kind'], 't' => $it['title'], 'r' => isset( $it['roles'] ) ? array_values( (array) $it['roles'] ) : array(), 'days' => isset( $it['days'] ) ? (int) $it['days'] : 0, 'from' => isset( $it['dayFrom'] ) ? $it['dayFrom'] : '', 'file' => isset( $it['form']['file'] ) ? $it['form']['file'] : '' );
			}, $d['items'] ), 'stages' => array_map( function ( $s ) { return array( 'id' => $s['id'], 'n' => $s['n'], 'name' => $s['name'] ); }, $d['stages'] ), 'roles' => $d['roles'], 'kinds' => $d['kinds'] ), JSON_UNESCAPED_UNICODE | JSON_UNESCAPED_SLASHES | JSON_HEX_TAG | JSON_HEX_AMP ) . '</script>';
		return $h . '</section>';
	} );

	add_action( 'wp_enqueue_scripts', function () {
		if ( ! nadlan_fh_on_page() ) { return; }
		$u = plugins_url( 'assets/forms/', dirname( __FILE__ ) );
		wp_enqueue_style( 'nadlan-forms-fonts', 'https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;500&family=IBM+Plex+Sans+Hebrew:wght@400;500;600;700&family=Karantina:wght@700&display=swap', array(), null );
		wp_enqueue_style( 'nadlan-forms', $u . 'forms.css', array(), nadlan_fh_ver( 'forms.css' ) );
		wp_enqueue_script( 'nadlan-forms', $u . 'forms.js', array(), nadlan_fh_ver( 'forms.js' ), true );
	}, 20 );

	add_action( 'wp_head', function () {
		if ( ! nadlan_fh_on_page() ) { return; }
		$d = nadlan_fh_data();
		$items = array(); $i = 0;
		foreach ( $d['items'] as $it ) {
			if ( empty( $it['form']['file'] ) ) { continue; }
			$f = $it['form'];
			$doc = array( '@type' => 'DigitalDocument', 'name' => $it['title'], 'url' => home_url( '/forms/#i-' . sanitize_title( $it['id'] ) ), 'contentUrl' => $f['file'],
				'encodingFormat' => isset( $f['mime'] ) ? $f['mime'] : 'application/pdf', 'inLanguage' => 'he' );
			if ( ! empty( $it['authority'] ) ) { $doc['publisher'] = array( '@type' => 'GovernmentOrganization', 'name' => $it['authority'] ); }
			if ( ! empty( $it['official'] ) ) { $doc['isBasedOn'] = $it['official']; }
			if ( ! empty( $it['what'] ) ) { $doc['description'] = $it['what']; }
			$items[] = array( '@type' => 'ListItem', 'position' => ++$i, 'item' => $doc );
		}
		$p = get_post();
		$graph = array( array( '@type' => 'CollectionPage', 'name' => get_the_title( $p ), 'url' => get_permalink( $p ), 'inLanguage' => 'he',
			'dateModified' => get_post_modified_time( 'c', true, $p ), 'mainEntity' => array( '@type' => 'ItemList', 'numberOfItems' => count( $items ), 'itemListElement' => $items ) ) );
		$url = get_permalink( $p );
		$org = array( '@type' => 'Organization', '@id' => home_url( '/#organization' ), 'name' => 'נדל"ן nad-lan.co.il', 'url' => home_url( '/' ) );
		// the page: what it is about (entities with their Wikipedia pages), who publishes it, what it cites, and how fresh it is
		$cite = array();
		foreach ( $d['items'] as $it ) { foreach ( (array) ( isset( $it['sources'] ) ? $it['sources'] : array() ) as $sc ) { if ( count( $cite ) < 60 && ! isset( $cite[ $sc['url'] ] ) && preg_match( '~gov\.il|wikisource|knesset|mevaker~', $sc['url'] ) ) { $cite[ $sc['url'] ] = array( '@type' => 'CreativeWork', 'name' => $sc['title'], 'url' => $sc['url'] ); } } }
		$about = array();
		foreach ( array( 'היתר בנייה' => 'היתר_בנייה', 'תעודת גמר' => 'טופס_4', 'לשכת רישום המקרקעין' => 'לשכת_רישום_המקרקעין', 'רשות מקרקעי ישראל' => 'רשות_מקרקעי_ישראל', 'בית משותף' => 'בית_משותף', 'מס שבח' => 'מס_שבח', 'מס רכישה' => 'מס_רכישה', 'פינוי בינוי' => 'פינוי_בינוי', 'תמ"א 38' => 'תמ%22א_38', 'היטל השבחה' => 'היטל_השבחה' ) as $n => $w ) {
			$about[] = array( '@type' => 'Thing', 'name' => $n, 'sameAs' => 'https://he.wikipedia.org/wiki/' . $w );
		}
		$graph[0]['@id'] = $url . '#page';
		$graph[0]['description'] = 'כל הטפסים, האישורים, הדיווחים, האגרות והמועדים בחיי בניין מגורים בישראל, מהתכנית ועד ההריסה, עם הטפסים הרשמיים להורדה והמקורות.';
		$graph[0]['publisher'] = $org;
		$graph[0]['about'] = $about;
		$graph[0]['citation'] = array_values( $cite );
		$graph[0]['isAccessibleForFree'] = true;
		$graph[0]['speakable'] = array( '@type' => 'SpeakableSpecification', 'cssSelector' => array( '.entry-content > p:first-of-type', '#numbers table' ) );
		// the eleven stages as an ordered process
		$steps = array(); $k = 0;
		foreach ( $d['stages'] as $st ) { $steps[] = array( '@type' => 'HowToStep', 'position' => ++$k, 'name' => $st['name'], 'text' => isset( $st['lead'] ) ? $st['lead'] : '', 'url' => $url . '#s-' . $st['id'] ); }
		$graph[] = array( '@type' => 'HowTo', '@id' => $url . '#lifecycle', 'name' => 'מחזור החיים של בניין מגורים בישראל: מהתכנית ועד ההריסה', 'inLanguage' => 'he', 'step' => $steps );
		// the data itself, open for reuse
		$graph[] = array( '@type' => 'Dataset', '@id' => $url . '#data', 'name' => 'טפסים ואישורים בחיי בניין מגורים בישראל', 'description' => count( $d['items'] ) . ' פריטים ב-11 שלבים: אישורים, טפסים רשמיים, דיווחים, אגרות ומועדים, לכל פריט הבסיס בחוק ומקורות רשמיים.',
			'inLanguage' => 'he', 'creator' => $org, 'dateModified' => isset( $d['updated'] ) ? $d['updated'] : '', 'isAccessibleForFree' => true, 'url' => $url,
			'distribution' => array( array( '@type' => 'DataDownload', 'encodingFormat' => 'application/json', 'contentUrl' => rest_url( 'nadlan/v1/forms' ) ) ) );
		if ( function_exists( 'nadlan_nli_faq' ) ) {
			$faq = nadlan_nli_faq( $p->post_content );
			if ( $faq ) { $graph[] = array( '@type' => 'FAQPage', 'url' => get_permalink( $p ), 'mainEntity' => $faq ); }
		}
		echo '<link rel="alternate" type="application/json" title="הנתונים של העמוד" href="' . esc_url( rest_url( 'nadlan/v1/forms' ) ) . '">' . "\n";
		echo '<script type="application/ld+json" id="nadlan-forms-ld">' . wp_json_encode( array( '@context' => 'https://schema.org', '@graph' => $graph ), JSON_UNESCAPED_UNICODE | JSON_UNESCAPED_SLASHES ) . '</script>' . "\n";
	}, 31 );

	/** GET /wp-json/nadlan/v1/forms: the same data as JSON, for AI assistants, agents and anyone who wants to reuse it. */
	add_action( 'rest_api_init', function () {
		register_rest_route( 'nadlan/v1', '/forms', array( 'methods' => 'GET', 'permission_callback' => '__return_true', 'callback' => function () {
			$d = nadlan_fh_data();
			$r = new WP_REST_Response( array( 'name' => 'טפסים ואישורים בחיי בניין מגורים בישראל', 'page' => home_url( '/forms/' ), 'updated' => isset( $d['updated'] ) ? $d['updated'] : '',
				'note' => 'Every item carries its legal basis and official sources. Form files are the state\'s copies from gov.il, byte-identical. Not legal advice; check the official page before acting.',
				'stages' => $d['stages'], 'facts' => isset( $d['facts'] ) ? $d['facts'] : array(), 'items' => $d['items'] ), 200 );
			$r->header( 'Cache-Control', 'public, max-age=3600' );
			return $r;
		} ) );
	} );

	/** /llms.txt: add the forms and approvals hub (the list itself is built in inc/instruments.php). */
	add_action( 'parse_request', function ( $wp ) {
		if ( 'llms.txt' !== ( isset( $wp->request ) ? (string) $wp->request : '' ) || ! function_exists( 'nadlan_llms_txt' ) ) { return; }
		$p = get_page_by_path( 'forms' );
		if ( ! $p || 'publish' !== $p->post_status ) { return; }
		$d = nadlan_fh_data(); $n = count( $d['items'] );
		$o = nadlan_llms_txt();
		$o .= "\n## Forms and building approvals\n";
		$o .= '- [' . html_entity_decode( get_the_title( $p ), ENT_QUOTES, 'UTF-8' ) . '](' . get_permalink( $p ) . '): ' . $n . ' items across the life of a residential building in Israel, from the plan and the land to demolition (11 stages): approvals, the state\'s official forms to download (Tabu, real-estate tax, Israel Land Authority, building licensing, condominium), reports, fees and statutory deadlines, each with its legal basis and official sources. Data as JSON: ' . rest_url( 'nadlan/v1/forms' ) . "\n";
		status_header( 200 ); header( 'Content-Type: text/plain; charset=utf-8' ); header( 'Cache-Control: public, max-age=3600' );
		echo $o; exit;
	}, -1 );
}
