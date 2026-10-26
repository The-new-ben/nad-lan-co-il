# G5 · what the release adds (NOT applied)

The research session built everything locally and did not touch `inc/instruments.php` or any live file (owner order 26.10.2026:
local only). The releaser reads the LIVE copy of each PHP file first (memory: the repo is not live for every file; target = live +
these additions), lints with `php -l`, and ships these files together, after Ben's yes on the new URL:

| File | State |
|---|---|
| `plugins/nadlan-config/assets/instruments/tools/rentfair.js` | new |
| `plugins/nadlan-config/assets/instruments/data/rent.json` | new, built by `tools/instruments/build_rent_data.py` (116 KB) |
| `plugins/nadlan-config/inc/instruments.php` | live copy + block 1 + block 2 |
| `plugins/nadlan-config/inc/rent-listings.php` | new (block 3), required from the plugin's main file next to `archive-grid.php` |
| `tools/instruments/build_rent_data.py`, `tools/instruments/test_rentfair.js` | repo only (`node tools/instruments/test_rentfair.js` must print ALL OK) |

## Block 1: the registry (inside `nadlan_nli_tools()`, after the `'invest'` entry)

```php
			/* G5 (26.10.2026): the owner page /דירות-להשכרה/ ("דירות להשכרה" / "דירה להשכרה"); data rent.json (data.nadlan.gov.il rent files
			   20-08-2026, CBS table 4.9 Q2 2026, CBS rent index 120460, the Rental and Loan Law sign 6, Kol Zchut tax pages 22.2.2026) */
			'rentfair' => array(
				'name' => 'כמה שכר דירה הוגן לדירה הזאת', 'cat' => 'FinanceApplication', 'kicker' => 'בדיקה · שכר דירה',
				'desc' => 'שכר הדירה שמבקשים מכם או שאתם מבקשים, מול שכר הדירה החציוני הרשמי בעיר לפי מספר החדרים (72 ערים), מול השכונה (945 שכונות), מול הממוצע של הלמ״ס עם טעות הדגימה ומול החציון הארצי; הערובה המרבית שמותר לבקש לפי חוק השכירות והשאילה, מועדי התיקון וההודעות, ושלושת מסלולי המס של המשכיר ל־2026.',
				'data' => array( 'rent.json' ),
				'related' => array( '/real-estate-lawyer/residential-lease-agreement/' => 'חוזה שכירות דירה', '/cpi-calculator/' => 'מחשבון הצמדה למדד', '/buy-vs-rent/' => 'מחשבון קנייה מול שכירות', '/my-rentals/' => 'ניהול נכסים מושכרים' ),
			),
```

## Block 2: the plain summary (inside `nadlan_nli_summary()`, next to the `'invest'` branch)

For readers without scripts and for search engines; the script replaces it with the tool. Numbers come from rent.json, nothing is typed twice.

```php
		if ( 'rentfair' === $id ) {  // G5: national medians by size, the CBS average of the 18 cities, the guarantee cap and the tax ceiling, from rent.json
			$path = dirname( __DIR__ ) . '/assets/instruments/data/rent.json';
			$x = is_readable( $path ) ? json_decode( (string) file_get_contents( $path ), true ) : null;
			if ( ! is_array( $x ) || empty( $x['cities'] ) ) { return ''; }
			$f = function ( $n ) { return esc_html( number_format( (float) $n ) ); };
			$n = $x['nat']['r']; $q = $n['4']['q']; $qm = array( '03' => 'ינואר עד מרץ', '06' => 'אפריל עד יוני', '09' => 'יולי עד ספטמבר', '12' => 'אוקטובר עד דצמבר' );
			$ql = $qm[ substr( $q, 5, 2 ) ] . ' ' . substr( $q, 0, 4 );
			$h = '<p>שכר הדירה החציוני בישראל, ' . esc_html( $ql ) . ' (אתר הנדל״ן הממשלתי): ' . $f( $n['3']['v'] ) . ' ₪ לדירת 3 חדרים, ' . $f( $n['4']['v'] ) . ' ₪ ל־4 חדרים, ' . $f( $n['5']['v'] ) . ' ₪ ל־5 חדרים. '
				. 'הערובה שמותר לבקש כשהיא עולה לשוכר כסף: הנמוך מבין 3 חודשי שכירות ושליש משכר הדירה לכל התקופה. פטור ממס למשכיר ב־' . (int) $x['tax']['year'] . ': עד ' . $f( $x['tax']['ceiling'] ) . ' ₪ בחודש.</p>'
				. '<table><thead><tr><th>עיר</th><th>3 חדרים</th><th>4 חדרים</th><th>5 חדרים</th><th>ממוצע הלמ״ס, כל הגדלים</th></tr></thead><tbody>';
			foreach ( $x['cities'] as $c ) {
				if ( empty( $c['cbs']['total'] ) ) { continue; }  // the 18 cities the CBS measures; the full 72 are in the page's own table
				$cell = function ( $k ) use ( $c, $f ) { return isset( $c['r'][ $k ] ) ? $f( $c['r'][ $k ]['v'] ) . ' ₪' : ''; };
				$h .= '<tr><td>' . esc_html( $c['n'] ) . '</td><td>' . $cell( '3' ) . '</td><td>' . $cell( '4' ) . '</td><td>' . $cell( '5' ) . '</td><td>' . $f( $c['cbs']['total']['a'] ) . ' ₪</td></tr>';
			}
			return $h . '</tbody></table>';
		}
```

## Block 3: `inc/rent-listings.php` (new): the `[nadlan_rent_listings]` shortcode

The live count and cards of the real rent listings (demos excluded, as the archive counts them), with the archive's own card
(`nadlan_plist_card()`: price as published, rooms, size, floor, and per Brokers Ethics reg. 19 the broker's name, status and licence),
restyled in the Instruments tokens (the CSS is `docs/research/2026-10-26-upgrades/g5-rentals/listings.css`, inlined once). Never
"0 מודעות": with no listing the block says so in words and links to the archive. The page publishes; it does not intermediate
(Brokers Law s.2(c)): no form, no "we will find you a flat", contact only through each listing's own publisher.

```php
<?php
/* G5 (26.10.2026): [nadlan_rent_listings limit="12"] for /דירות-להשכרה/. Reads only; uses inc/archive-grid.php's card. */
if ( ! defined( 'ABSPATH' ) ) { exit; }
add_shortcode( 'nadlan_rent_listings', function ( $atts ) {
	if ( ! function_exists( 'nadlan_plist_card' ) || ! function_exists( 'nadlan_pl_nodemo' ) || ! function_exists( 'nadlan_pl_is_demo' ) ) { return ''; }
	$a   = shortcode_atts( array( 'limit' => 12 ), $atts );
	$ids = get_posts( array( 'post_type' => 'nadlan_property', 'post_status' => 'publish', 'posts_per_page' => -1, 'fields' => 'ids', 'no_found_rows' => true,
		'orderby' => 'date', 'order' => 'DESC', 'meta_query' => array( 'relation' => 'AND', nadlan_pl_nodemo(), array( 'key' => 'listing_type', 'value' => 'rent' ) ) ) );
	$ids = array_values( array_filter( $ids, function ( $id ) { return ! nadlan_pl_is_demo( $id ); } ) );
	$arch = add_query_arg( 'listing_type', 'rent', get_post_type_archive_link( 'nadlan_property' ) );
	$css  = '<style id="nlrh-list-css">' . file_get_contents( __DIR__ . '/../assets/rent-listings.css' ) . '</style>';  // listings.css shipped as assets/rent-listings.css
	if ( ! $ids ) { return $css . '<p class="nlrh-count">אין כרגע מודעות להשכרה באתר. <a href="' . esc_url( $arch ) . '">לכל המודעות</a></p>'; }
	$by = array();
	foreach ( $ids as $id ) { $c = trim( (string) get_post_meta( $id, 'city', true ) ); if ( '' !== $c ) { $by[ $c ] = ( $by[ $c ] ?? 0 ) + 1; } }
	arsort( $by );
	$parts = array(); foreach ( $by as $c => $k ) { $parts[] = ( 1 === $k ? 'אחת ב' : $k . ' ב' ) . $c; }
	$n = count( $ids );
	$h = $css . '<div class="nlrh-list"><p class="nlrh-count"><b>' . (int) $n . '</b> ' . ( 1 === $n ? 'מודעה להשכרה באתר' : 'מודעות להשכרה באתר' ) . ( $parts ? ': ' . esc_html( implode( ' ו־', $parts ) ) : '' ) . '.</p><div class="nlpl-grid">';
	$items = array(); $pos = 1;
	foreach ( array_slice( $ids, 0, max( 1, (int) $a['limit'] ) ) as $id ) {
		$h .= nadlan_plist_card( $id );
		$items[] = array( '@type' => 'ListItem', 'position' => $pos++, 'url' => get_permalink( $id ), 'name' => html_entity_decode( get_the_title( $id ), ENT_QUOTES, 'UTF-8' ) );
	}
	$h .= '</div><p class="nlrh-more"><a href="' . esc_url( $arch ) . '">לכל המודעות באתר, עם סינון לפי עיר, חדרים ומחיר</a></p></div>';
	$h .= '<script type="application/ld+json">' . wp_json_encode( array( '@context' => 'https://schema.org', '@type' => 'ItemList', 'name' => 'דירות להשכרה באתר', 'numberOfItems' => $n, 'itemListElement' => $items ), JSON_UNESCAPED_UNICODE | JSON_UNESCAPED_SLASHES ) . '</script>';
	return $h;
} );
```

Note: the page also needs `rentfair.js` enqueued; `nadlan_nli_page_ids()` finds `[nadlan_tool id="rentfair"]` in the content as for every tool.

## Checks after the release (before the page writer runs)
- `GET /wp-json/nadlan/v1/health` shows the new version; `tools/rentfair.js?x=…` answers 200 and contains `register('rentfair'`.
- A private test page with `[nadlan_tool id="rentfair"]` and `[nadlan_rent_listings]` prints the summary table in the raw HTML,
  the tool after the script, and the live count (11 on 26.10.2026) with the cards.
- Then, only after Ben's yes on the URL: `python docs/research/2026-10-26-upgrades/g5-rentals/write_g5_page.py --dry` (GET only),
  `--create` (draft), check the draft in his Chrome at 390 and 1280, then `--create --publish` is NOT re-run; publish the draft
  from wp-admin or by a REST status change, and run `proof_run.py --live`.
- After the page: rainbow + h-infinity spot check (law 7), `tools/source_audit.py` on the new URL, the sitemap check (the page must
  appear in the page sitemap), and a Search Console sitemap resubmit only (no indexing request: owner law 22.10.2026).
