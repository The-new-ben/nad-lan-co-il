<?php
/**
 * Plain PHP CLI test of the forum's "הדירה שמדברים עליה" layer (no WordPress): php tests-local/pro-forum-home-test.php
 * Loads the forum's pure part (NLF_PURE_ONLY) and then part 1 of inc/pro-forum-home.php (NLFH_PURE_ONLY), plus static checks
 * on the module's files and on the one-line hooks it needs in the forum's own files. Exit code 0 = all passed.
 */
define( 'ABSPATH', __DIR__ . '/' );
define( 'NLF_PURE_ONLY', true );
define( 'NLFH_PURE_ONLY', true );
require __DIR__ . '/../inc/pro-forum.php';
require __DIR__ . '/../inc/pro-forum-home.php';

$pass = 0; $fail = 0;
function t( $name, $cond ) {
	global $pass, $fail;
	if ( $cond ) { $pass++; echo "ok   $name\n"; } else { $fail++; echo "FAIL $name\n"; }
}

/* the 24 cities and their settlement codes (prices-hub.json) */
$hub = json_decode( (string) file_get_contents( __DIR__ . '/../assets/instruments/data/prices-hub.json' ), true );
$hubmap = array();
foreach ( (array) ( $hub['city'] ?? array() ) as $c ) { $hubmap[ $c['n'] ] = (int) $c['code']; }
ksort( $hubmap ); $mine = nlfh_cities(); ksort( $mine );
t( 'cities: the same 24 names and codes as prices-hub.json', 24 === count( $mine ) && $hubmap === $mine );
t( 'city code: רמת גן = 8600, אשדוד = 70', 8600 === nlfh_city_code( 'רמת גן' ) && 70 === nlfh_city_code( 'אשדוד' ) );
t( 'city code: a city outside the list = 0', 0 === nlfh_city_code( 'קריית שמונה' ) && 0 === nlfh_city_code( '' ) );
t( 'code ok: only the 24', nlfh_code_ok( 5000 ) && ! nlfh_code_ok( 1234 ) && ! nlfh_code_ok( 0 ) );

/* the street: no house number at the end, no phone, no link */
t( 'street: a name alone is fine', '' === nlfh_street_error( "ז'בוטינסקי" ) && '' === nlfh_street_error( 'דרך מנחם בגין' ) );
t( 'street: empty is fine (optional)', '' === nlfh_street_error( '' ) && '' === nlfh_street_error( '   ' ) );
t( 'street: a number inside the name is fine', '' === nlfh_street_error( 'ה-14 במאי' ) && '' === nlfh_street_error( '26 בנובמבר' ) );
foreach ( array( 'הרצל 12', 'הרצל 12א', 'הרצל12', 'הרצל 12 א', 'הרצל 12/3', "הרצל מס' 5", 'הרצל 12 דירה 4', '7', 'הרצל, 9' ) as $s ) {
	t( 'street: house number refused: ' . $s, 'בלי מספר בית, רק שם הרחוב.' === nlfh_street_error( $s ) );
}
t( 'street: a phone is refused', false !== strpos( nlfh_street_error( 'הרצל 050-1234567 ' . 'רחוב' ), 'טלפון' ) && '' !== nlfh_street_error( 'הרצל 0501234567' ) );
t( 'street: a link is refused', false !== strpos( nlfh_street_error( 'הרצל www.example.com' ), 'קישור' ) );
t( 'street: too long', '' !== nlfh_street_error( str_repeat( 'א', 41 ) ) && '' === nlfh_street_error( str_repeat( 'א', 40 ) ) );

/* rooms, numbers, amounts */
t( 'rooms: 1 to 12, halves allowed', 4.0 === nlfh_rooms_norm( '4' ) && 3.5 === nlfh_rooms_norm( '3.5' ) && 3.5 === nlfh_rooms_norm( '3,5' ) && 12.0 === nlfh_rooms_norm( '12' ) && 1.0 === nlfh_rooms_norm( '1' ) );
t( 'rooms: refused outside or not a half', 0.0 === nlfh_rooms_norm( '0' ) && 0.0 === nlfh_rooms_norm( '12.5' ) && 0.0 === nlfh_rooms_norm( '3.3' ) && 0.0 === nlfh_rooms_norm( 'ארבעה' ) && 0.0 === nlfh_rooms_norm( '' ) );
t( 'rooms text: 4 / 3.5', '4' === nlfh_rooms_text( 4 ) && '3.5' === nlfh_rooms_text( 3.5 ) && '12' === nlfh_rooms_text( 12.0 ) );
t( 'int field: empty = null, bad = false, range', null === nlfh_int_field( '', 1, 9 ) && false === nlfh_int_field( 'x', 1, 9 ) && false === nlfh_int_field( '10', 1, 9 ) && 0 === nlfh_int_field( '0', -3, 99 ) && -1 === nlfh_int_field( '-1', -3, 99 ) );
t( 'amount: what people type', 3450000 === nlfh_amount_parse( '3,450,000' ) && 3450000 === nlfh_amount_parse( '₪ 3450000' ) && 3450000 === nlfh_amount_parse( '3 450 000 ש"ח' ) );
t( 'amount: out of 100,000..200,000,000 or agorot = 0', 0 === nlfh_amount_parse( '3.45' ) && 0 === nlfh_amount_parse( '99999' ) && 0 === nlfh_amount_parse( '250000000' ) && 0 === nlfh_amount_parse( '' ) && 0 === nlfh_amount_parse( '3450000.50' ) );
t( 'money: ₪3,250,000', '₪3,250,000' === nlfh_money( 3250000 ) );
t( 'money short: millions and thousands', "₪3.21 מ'" === nlfh_money_short( 3210000 ) && "₪3.45 מ'" === nlfh_money_short( 3450000 ) && "₪3 מ'" === nlfh_money_short( 3000000 ) && "₪3.2 מ'" === nlfh_money_short( 3200000 ) && '₪850 אלף' === nlfh_money_short( 850000 ) );

/* the title, built on the server */
$f = array( 'rooms' => 4, 'sqm' => 98, 'floor' => 6, 'floors' => 9, 'street' => "ז'בוטינסקי", 'city' => 'רמת גן' );
t( 'title: every part', '4 חדרים, 98 מ"ר, קומה 6 מתוך 9 · ז\'בוטינסקי, רמת גן: כמה היא שווה?' === nlfh_title( $f ) );
t( 'title: no m², no floors', '3.5 חדרים, קומה 2 · הרצל, חולון: כמה היא שווה?' === nlfh_title( array( 'rooms' => 3.5, 'sqm' => null, 'floor' => 2, 'floors' => null, 'street' => 'הרצל', 'city' => 'חולון' ) ) );
t( 'title: no street, ground floor', '5 חדרים, 120 מ"ר, קומת קרקע מתוך 4 · רעננה: כמה היא שווה?' === nlfh_title( array( 'rooms' => 5, 'sqm' => 120, 'floor' => 0, 'floors' => 4, 'street' => '', 'city' => 'רעננה' ) ) );
t( 'title: one room', 'חדר אחד · אילת: כמה היא שווה?' === nlfh_title( array( 'rooms' => 1, 'city' => 'אילת' ) ) );
t( 'title: floors without a floor are left out', '4 חדרים · בת ים: כמה היא שווה?' === nlfh_title( array( 'rooms' => 4, 'floor' => null, 'floors' => 9, 'city' => 'בת ים' ) ) );
t( 'title: within the forum title rules', '' === nlf_title_error( nlfh_title( $f ) ) && nlf_len( nlfh_title( array( 'rooms' => 12, 'sqm' => 1000, 'floor' => 99, 'floors' => 99, 'street' => str_repeat( 'א', 40 ), 'city' => str_repeat( 'ב', 40 ) ) ) ) <= 140 );
t( 'headline and place of the card', '4 חדרים, 98 מ"ר, קומה 6 מתוך 9' === nlfh_headline( $f ) && "רחוב ז'בוטינסקי, רמת גן" === nlfh_place( $f ) );

/* median, band, outliers */
t( 'median: odd, even, none', 3.0 === (float) nlfh_median( array( 5, 1, 3 ) ) && 2.5 === (float) nlfh_median( array( 4, 1, 3, 2 ) ) && 0 == nlfh_median( array() ) );
t( 'percentile: linear (PERCENTILE.INC)', 1.75 === (float) nlfh_pct( array( 1, 2, 3, 4 ), 25 ) && 3.25 === (float) nlfh_pct( array( 4, 3, 2, 1 ), 75 ) && 7.0 === (float) nlfh_pct( array( 7 ), 25 ) );
t( 'outliers: 0.3x..3x of the median of the others', array( false, false, false, true ) === nlfh_outliers( array( 3000000, 3200000, 3400000, 12000000 ) ) );
t( 'outliers: a far low one too', array( true, false, false, false ) === nlfh_outliers( array( 500000, 3000000, 3200000, 3400000 ) ) );
t( 'outliers: a lone estimate is not one', array( false ) === nlfh_outliers( array( 3000000 ) ) );
$s = nlfh_est_summary( array( 3000000, 3200000, 3400000, 3300000, 12000000 ) );
t( 'summary: count keeps the outlier, the band leaves it out', 5 === $s['count'] && 4 === $s['kept'] && 3250000 === $s['median'] && 3150000 === $s['p25'] && 3325000 === $s['p75'] );
t( 'summary waits below 3', 3 === nlfh_est_missing( 0 ) && 1 === nlfh_est_missing( 2 ) && 0 === nlfh_est_missing( 3 ) && 0 === nlfh_est_missing( 11 ) );
$tr = nlfh_track( 3000000, 3400000, 3210000, 3450000 );
t( 'track: right to left, the band inside, the asking price further left', $tr['band_r'] > 0 && $tr['band_r'] + $tr['band_w'] < 100 && $tr['med'] > $tr['band_r'] && $tr['ask'] > $tr['med'] && $tr['ask'] < 100 );
t( 'track: no asking price, no marker', null === nlfh_track( 1, 2, 1.5 )['ask'] && null === nlfh_track( 0, 0, 0 ) );

/* the vote */
t( 'split: whole percents adding to 100', array( 1 => 14, 2 => 38, 3 => 48 ) === nlfh_vote_split( array( 1 => 14, 2 => 38, 3 => 48 ) ) && 100 === array_sum( nlfh_vote_split( array( 1 => 1, 2 => 1, 3 => 1 ) ) ) );
t( 'split: largest remainder', array( 1 => 34, 2 => 33, 3 => 33 ) === nlfh_vote_split( array( 1 => 1, 2 => 1, 3 => 1 ) ) && array( 1 => 0, 2 => 0, 3 => 0 ) === nlfh_vote_split( array() ) );
$k = str_repeat( 'k', 64 );
t( 'voter key: a member, stable and 64 hex', nlfh_voter_key( 7, '', $k ) === nlfh_voter_key( 7, 'ab', $k ) && (bool) preg_match( '/^[a-f0-9]{64}$/', nlfh_voter_key( 7, '', $k ) ) );
t( 'voter key: a guest browser by its cookie', (bool) preg_match( '/^[a-f0-9]{64}$/', nlfh_voter_key( 0, str_repeat( 'a', 32 ), $k ) ) && nlfh_voter_key( 0, str_repeat( 'a', 32 ), $k ) !== nlfh_voter_key( 0, str_repeat( 'b', 32 ), $k ) );
t( 'voter key: member and guest never collide; a bad cookie = none', nlfh_voter_key( 1, '', $k ) !== nlfh_voter_key( 0, str_repeat( '1', 32 ), $k ) && '' === nlfh_voter_key( 0, 'x', $k ) && '' === nlfh_voter_key( 0, '', $k ) );
t( 'stats line: zero parts left out', '212 הצביעו · 31 תגובות · 4 אנשי מקצוע' === nlfh_stats_line( 212, 31, 4 ) && '31 תגובות' === nlfh_stats_line( 0, 31, 0 ) && '' === nlfh_stats_line( 0, 0, 0 ) && 'הצבעה אחת · תגובה אחת · איש מקצוע אחד' === nlfh_stats_line( 1, 1, 1 ) );
t( 'share text of part ה', 'כמה הייתם נותנים על הדירה הזו? T https://x/forum/1/' === nlfh_share_text( 'T', 'https://x/forum/1/' ) );
t( 'hot pick: most score, the newest on a tie, none', 2 === nlfh_hot_pick( array( array( 'id' => 1, 'score' => 3, 'created' => '2026-11-01' ), array( 'id' => 2, 'score' => 9, 'created' => '2026-10-01' ) ) )
	&& 3 === nlfh_hot_pick( array( array( 'id' => 1, 'score' => 0, 'created' => '2026-11-01' ), array( 'id' => 3, 'score' => 0, 'created' => '2026-11-02' ) ) ) && 0 === nlfh_hot_pick( array() ) );

/* the public files: BOM, fields, buckets */
$bom = "\xEF\xBB\xBF";
$sjs = $bom . json_encode( array( 'settlementID' => 8600, 'settlementName' => 'רמת גן', 'version' => '20-08-2026',
	'otherNeighborhoods' => array( array( 'title' => 'תל גנים', 'id' => 65210662 ), array( 'title' => '', 'id' => 5 ), array( 'id' => 6 ) ),
	'trends' => array( 'rooms' => array(
		array( 'numRooms' => 3, 'summary' => array( 'lastYearAvgPrice' => 2701700, 'priceDifferencePercentage' => 0.81 ) ),
		array( 'numRooms' => 4, 'summary' => array( 'lastYearAvgPrice' => 3314200, 'priceDifferencePercentage' => '0.82' ) ),
		array( 'numRooms' => 5, 'summary' => array( 'lastYearAvgPrice' => null, 'priceDifferencePercentage' => null ) ),
		array( 'numRooms' => 'all', 'summary' => array( 'lastYearAvgPrice' => 3073800 ) ),
	) ) ), JSON_UNESCAPED_UNICODE );
$sp = nlfh_settlement_parse( $sjs );
t( 'settlement file with a BOM is read', is_array( $sp ) && 'רמת גן' === $sp['name'] && '20-08-2026' === $sp['version'] );
t( 'settlement: neighbourhoods by id, empty ones dropped', array( 65210662 => 'תל גנים' ) === $sp['nbhds'] );
t( 'settlement: averages by bucket, a null one left out', array( '3' => 2701700, '4' => 3314200, 'all' => 3073800 ) === $sp['rooms'] );
t( 'settlement: not a settlement file = null', null === nlfh_settlement_parse( '{"x":1}' ) && null === nlfh_settlement_parse( 'not json' ) && null === nlfh_settlement_parse( '' ) );
$njs = $bom . json_encode( array( 'neighborhoodId' => 65210661, 'neighborhoodName' => 'יד לבנים', 'settlementID' => 8600, 'version' => '20-08-2026',
	'trends' => array( 'rooms' => array( array( 'numRooms' => 4, 'summary' => array( 'lastYearAvgPrice' => 3231300 ), 'graphData' => array( array( 'neighborhoodPrice' => 3231300, 'year' => 2026, 'month' => 3 ) ) ),
		array( 'numRooms' => 3, 'summary' => array( 'lastYearAvgPrice' => null ) ) ) ) ), JSON_UNESCAPED_UNICODE );
$np = nlfh_nbhd_parse( $njs );
t( 'neighbourhood file with a BOM is read', is_array( $np ) && 'יד לבנים' === $np['name'] && 8600 === $np['settlement'] && array( '4' => 3231300 ) === $np['rooms'] );
t( 'neighbourhood: not one = null', null === nlfh_nbhd_parse( $sjs ) );
t( 'json: BOM taken off, an array is not an object', is_array( nlfh_json( $bom . '{"a":1}' ) ) && null === nlfh_json( '"x"' ) );
t( 'version date', '20.8.2026' === nlfh_version_date( '20-08-2026' ) && '' === nlfh_version_date( '2026-08-20' ) );
t( 'room match: 3, 3.5 -> 3; 4 -> 4; 5.5 -> 5; 2 and 6 -> all', '3' === nlfh_room_bucket( 3 ) && '3' === nlfh_room_bucket( 3.5 ) && '4' === nlfh_room_bucket( 4 ) && '5' === nlfh_room_bucket( 5.5 ) && 'all' === nlfh_room_bucket( 2 ) && 'all' === nlfh_room_bucket( 6 ) );
t( 'bucket label', 'דירות 4 חדרים' === nlfh_bucket_label( '4' ) && 'כל הדירות' === nlfh_bucket_label( 'all' ) );
t( 'data address: settlement and neighbourhood only, never /street/', 'https://data.nadlan.gov.il/api/pages/settlement/buy/8600.json' === nlfh_data_url( 'settlement', 8600 )
	&& 'https://data.nadlan.gov.il/api/pages/neighborhood/buy/65210661.json' === nlfh_data_url( 'neighborhood', 65210661 ) && '' === nlfh_data_url( 'street', 86001529 ) && '' === nlfh_data_url( 'settlement', 0 ) );
t( 'chips: three states, three intents (board words)', array( 'יד שנייה', 'דירה מקבלן', 'צריכה שיפוץ' ) === array_column( nlfh_states(), 0 ) && array( 'אני מוכר', 'שוקל לקנות אותה', 'סתם סקרן' ) === array_column( nlfh_intents(), 0 ) );

/* static checks: the module, its assets, the one-line hooks in the forum's files */
$root = __DIR__ . '/..';
$php  = (string) file_get_contents( $root . '/inc/pro-forum-home.php' );
$core = (string) file_get_contents( $root . '/inc/pro-forum.php' );
$rnd  = (string) file_get_contents( $root . '/inc/pro-forum-render.php' );
$js   = (string) file_get_contents( $root . '/assets/proforum/home.js' );
$css  = (string) file_get_contents( $root . '/assets/proforum/home.css' );
$mjs  = (string) file_get_contents( $root . '/assets/proforum/media.js' );
$kit  = (string) file_get_contents( $root . '/../../scripts/project-stage/forum_testkit.py' );
t( 'core: loaded once, after the media module', 1 === substr_count( $core, "require_once __DIR__ . '/pro-forum-home.php';" ) && strpos( $core, "/pro-forum-home.php'" ) > strpos( $core, "/pro-forum-media.php'" ) );
t( 'core: kinds are filterable (HOOK line), five without WordPress', 1 === substr_count( $core, "apply_filters( 'nlf_kinds'" ) && 5 === count( nlf_kinds() ) && ! isset( nlf_kinds()['home'] ) );
t( 'module adds the kind דירה לדיון', false !== strpos( $php, "\$k['home'] = 'דירה לדיון';" ) );
t( 'render: the estimate chip hook before the body', false !== strpos( $rnd, "apply_filters( 'nlf_reply_before_body', '', \$r, \$t )" ) && strpos( $rnd, "'nlf_reply_before_body'" ) < strpos( $rnd, "<p class=\"nlf-body\"><?php echo nlf_body_html( \$r['body'] )" ) );
t( 'media.js gives the apartment sheet its composer', false !== strpos( $mjs, "form[data-nlfmd-compose]" ) && false !== strpos( $php, 'data-nlfmd-compose' ) );
t( 'the generic route refuses kind home; the home route says it is itself', false !== strpos( $php, "nlfh_creating( true );" ) && false !== strpos( $php, "'home' === sanitize_key( (string) \$q->get_param( 'kind' ) ) && ! nlfh_creating()" ) );
t( 'routes: home, home/nbhd, home/vote', false !== strpos( $php, "\$reg( 'home', 'POST'" ) && false !== strpos( $php, "\$reg( 'home/nbhd', 'GET'" ) && false !== strpos( $php, "\$reg( 'home/vote', 'POST'" ) );
t( 'vote limits: 200 a day per hashed IP, one new guest vote per discussion per IP a day', false !== strpos( $php, "nlf_rl( 'nlfh_v', 200, DAY_IN_SECONDS )" ) && false !== strpos( $php, "'nlfh_ip_' . md5(" ) );
t( 'the public files: 7 days, a failure 10 minutes, the site named in the user agent, the BOM, no /street/ fetch', false !== strpos( $php, '7 * DAY_IN_SECONDS' ) && false !== strpos( $php, "array( 'fail' => 1 ), 10 * MINUTE_IN_SECONDS" ) && false !== strpos( $php, "'user-agent' => 'NadLanForum/1.0" ) && false === strpos( $php, 'street/buy' ) && false === strpos( $js, 'data.nadlan.gov.il' ) );
t( 'tables: homes, votes, estimates with their unique keys', false !== strpos( $php, 'UNIQUE KEY one_vote (topic_id,voter_key)' ) && false !== strpos( $php, 'UNIQUE KEY one_estimate (topic_id,member_id)' ) && false !== strpos( $php, 'rooms DECIMAL(3,1)' ) && false !== strpos( $php, 'PRIMARY KEY  (topic_id)' ) );
t( 'board words: the vote, the waiting line, the disclaimer, the replaced box', false !== strpos( $php, 'המחיר הזה, לדעתכם:' ) && false !== strpos( $php, 'אחרי ההצבעה רואים מה כולם חשבו' ) && false !== strpos( $php, 'ונראה את התמונה' )
	&& false !== strpos( $php, 'דעות של חברי הפורום, לא שמאות.' ) && false !== strpos( $php, 'ממוצע העסקאות בשנה האחרונה (רשות המסים)' ) && 1 === substr_count( $php, 'נמכרו ברחוב' ) && strpos( $php, 'נמכרו ברחוב' ) < strpos( $php, 'function nlfh_cities' ) ); // named once, in the header, as NOT built
t( 'board words: the sheet and the privacy line', false !== strpos( $php, 'כמה הדירה שלכם שווה? תשאלו את הפורום' ) && false !== strpos( $php, 'רחוב, בלי מספר' ) && false !== strpos( $php, 'להציג לפורום' )
	&& false !== strpos( $php, 'המיקום יוסר מהתמונות. מי שרוצה לפנות אליכם כותב דרך הפורום, והטלפון שלכם לא מוצג.' ) );
t( 'no lead form, no contact of the seller', false === strpos( $php, 'nlf_pro_phone' ) && false === strpos( $php, "'contact'" ) && false === strpos( $js, 'tel:' ) );
t( 'nothing in the JSON-LD from this module', false === strpos( $php, "add_filter( 'nlf_jsonld'" ) );
t( 'og:image: Yoast presenter off only with a picture, own tag first', false !== strpos( $php, "'wpseo_frontend_presenters'" ) && false !== strpos( $php, '<meta property="og:image"' ) );
t( 'js: handle nlf-home after nlf-media; nlfExtra wrapped, not replaced', false !== strpos( $php, "wp_enqueue_script( 'nlf-home'" ) && false !== strpos( $js, 'var prev = rf.nlfExtra;' ) && false !== strpos( $js, 'prev.call(rf, path)' ) );
t( 'js: people\'s text only through textContent', false === strpos( $js, 'innerHTML' ) && false === strpos( $js, 'insertAdjacentHTML' ) );
t( 'css: every rule under .nlf with the nlfh- prefix', ! preg_match( '/^(?!\.nlf |@media|\/\*| |\t|\})[^\n]*\{/m', $css ) && false === strpos( $css, '.nlf .nlf-' ) );
t( 'board palette in the css', false !== strpos( $css, '#B0144F' ) && false !== strpos( $css, '#2F6F86' ) && false !== strpos( $css, '#2E7D5B' ) && false !== strpos( $css, '#101820' ) && false !== strpos( $css, '#D5DBDF' ) );
t( 'test kit clean removes homes, votes and estimates', false !== strpos( $kit, 'nlfh_purge_members( $ids, (array) $tids )' ) && false !== strpos( $php, 'function nlfh_purge_members(' ) );
t( 'no long dashes in the new files', ! preg_match( '/\x{2014}|\x{2013}/u', $php . $js . $css ) );

echo "\n$pass passed, $fail failed\n";
exit( $fail ? 1 : 0 );
