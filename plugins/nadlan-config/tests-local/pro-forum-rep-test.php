<?php
/**
 * Plain PHP CLI test of the forum's reputation layer (no WordPress): php tests-local/pro-forum-rep-test.php
 * Loads the forum's pure part (NLF_PURE_ONLY) and then part 1 of inc/pro-forum-rep.php (NLFR_PURE_ONLY), plus static checks
 * on the module's files. Exit code 0 = all passed.
 */
define( 'ABSPATH', __DIR__ . '/' );
define( 'NLF_PURE_ONLY', true );
define( 'NLFR_PURE_ONLY', true );
require __DIR__ . '/../inc/pro-forum.php';
require __DIR__ . '/../inc/pro-forum-rep.php';

$pass = 0; $fail = 0;
function t( $name, $cond ) {
	global $pass, $fail;
	if ( $cond ) { $pass++; echo "ok   $name\n"; } else { $fail++; echo "FAIL $name\n"; }
}

/* the weights printed to the public (board 20, part ד) */
t( 'weights', array( 'helped' => 15, 'kudos' => 10, 'together' => 10, 'skills' => 3, 'reacts' => 2, 'posts' => 1 ) === nlfr_weights() );
t( 'post cap 5 a day', 5 === nlfr_post_cap() );
t( 'gate: 5 askers, 90 days', array( 'askers' => 5, 'days' => 90 ) === nlfr_gate() );
$L = nlfr_levels();
t( 'six level rows, stars 0 to 5', array( 0, 1, 2, 3, 4, 5 ) === array_column( $L, 'n' ) );
t( 'level names as on the board', array( 'חדש בזירה', 'יסודות', 'שלד', 'גמר', 'מסירה', 'מפתח' ) === array_column( $L, 'name' ) );
t( 'level thresholds', array( 0, 10, 50, 150, 400, 1000 ) === array_column( $L, 'min' ) );
t( 'max stars 5', 5 === nlfr_max_stars() );

/* points */
t( 'points of nothing = 0', 0 === nlfr_points( array() ) );
t( 'points: each weight', 15 === nlfr_points( array( 'helped' => 1 ) ) && 10 === nlfr_points( array( 'kudos' => 1 ) ) && 10 === nlfr_points( array( 'together' => 1 ) )
	&& 3 === nlfr_points( array( 'skills' => 1 ) ) && 2 === nlfr_points( array( 'reacts' => 1 ) ) && 1 === nlfr_points( array( 'posts' => 1 ) ) );
t( 'points: the board example (6, 31, 3, 1, 20 = 212)', 212 === nlfr_points( array( 'helped' => 6, 'reacts' => 31, 'kudos' => 3, 'together' => 1, 'posts' => 20 ) ) );
t( 'points never negative', 0 === nlfr_points( array( 'helped' => -5, 'posts' => -100 ) ) && 15 === nlfr_points( array( 'helped' => 1, 'posts' => -3 ) ) );
t( 'unknown counts ignored', 1 === nlfr_points( array( 'posts' => 1, 'bribe' => 999 ) ) );

/* levels at every threshold (the gates open: 5 askers, 90 days) */
$lvn = function ( $p ) { return nlfr_level( $p, 5, 90 )['n']; };
t( '9 = no stars', 0 === $lvn( 9 ) && 'חדש בזירה' === nlfr_level( 9, 5, 90 )['name'] );
t( '0 = no stars', 0 === $lvn( 0 ) );
t( '10 = 1', 1 === $lvn( 10 ) );
t( '49 = 1', 1 === $lvn( 49 ) );
t( '50 = 2', 2 === $lvn( 50 ) );
t( '149 = 2', 2 === $lvn( 149 ) );
t( '150 = 3', 3 === $lvn( 150 ) && 'גמר' === nlfr_level( 150, 0, 0 )['name'] );
t( '399 = 3', 3 === $lvn( 399 ) );
t( '400 = 4', 4 === $lvn( 400 ) );
t( '999 = 4', 4 === $lvn( 999 ) );
t( '1000 = 5', 5 === $lvn( 1000 ) && 'מפתח' === nlfr_level( 1000, 5, 90 )['name'] );
t( 'huge = 5', 5 === $lvn( 99999 ) );

/* level 5 gates */
t( 'level 5 needs 5 askers', 4 === nlfr_level( 1500, 4, 400 )['n'] );
t( 'level 5 needs 90 days', 4 === nlfr_level( 1500, 9, 89 )['n'] );
t( 'level 5 with both gates', 5 === nlfr_level( 1000, 5, 90 )['n'] );
t( 'gates do not touch lower levels', 4 === nlfr_level( 400, 0, 0 )['n'] && 1 === nlfr_level( 10, 0, 0 )['n'] );

/* progress */
$p = nlfr_progress( 212, 2, 30 );
t( 'progress: next level and missing (board: 188 to מסירה)', 'מסירה' === $p['next'] && 188 === $p['missing'] && 4 === $p['next_n'] );
t( 'progress: percent inside the level (board: 25)', 25 === $p['pct'] );
t( 'progress text (board)', 'עוד 188 נקודות לדרגת מסירה' === nlfr_progress_text( $p ) );
t( 'progress short (board: 62 = עוד 88 לגמר)', 'עוד 88 לגמר' === nlfr_progress_short( nlfr_progress( 62, 0, 0 ) ) );
t( 'progress at 0: 10 to יסודות, 0%', 10 === nlfr_progress( 0, 0, 0 )['missing'] && 0 === nlfr_progress( 0, 0, 0 )['pct'] && 'יסודות' === nlfr_progress( 0, 0, 0 )['next'] );
t( 'progress one below the next level: 98% (39 of 40, rounded)', 98 === nlfr_progress( 49, 0, 0 )['pct'] && 1 === nlfr_progress( 49, 0, 0 )['missing'] );
t( 'progress at a threshold: 0% of the new level', 0 === nlfr_progress( 50, 0, 0 )['pct'] && 100 === nlfr_progress( 50, 0, 0 )['missing'] );
t( 'one point words', 'עוד נקודה אחת לדרגת שלד' === nlfr_progress_text( nlfr_progress( 49, 0, 0 ) ) );
$top = nlfr_progress( 1200, 5, 90 );
t( 'progress at the top: no next, 100%', '' === $top['next'] && 0 === $top['missing'] && 100 === $top['pct'] && 'הדרגה הגבוהה בפורום' === nlfr_progress_text( $top ) && '' === nlfr_progress_short( $top ) );
$g1 = nlfr_progress( 1200, 3, 200 );
t( 'gated by askers: next מפתח, missing 0, need 2', 'מפתח' === $g1['next'] && 0 === $g1['missing'] && 2 === $g1['need_askers'] && 0 === $g1['need_days'] && 100 === $g1['pct'] );
t( 'gated text by askers', false !== strpos( nlfr_progress_text( $g1 ), 'שואלים שונים' ) && false !== strpos( nlfr_progress_text( $g1 ), '2 תשובות' ) );
$g2 = nlfr_progress( 1200, 7, 60 );
t( 'gated by days: need 30', 30 === $g2['need_days'] && 0 === $g2['need_askers'] && 'דרגת מפתח בעוד 30 ימים בפורום' === nlfr_progress_text( $g2 ) );

/* the daily cap of answers and discussions */
t( 'posts: 3 on one day = 3', 3 === nlfr_count_posts( array( array( 'day' => '2026-11-18', 'n' => 3 ) ) ) );
t( 'posts: 9 on one day = 5', 5 === nlfr_count_posts( array( array( 'day' => '2026-11-18', 'n' => 9 ) ) ) );
t( 'posts: answers and discussions of the same day share the cap', 5 === nlfr_count_posts( array( array( 'day' => '2026-11-18', 'n' => 4 ), array( 'day' => '2026-11-18', 'n' => 3 ) ) ) );
t( 'posts: separate days each capped', 5 + 2 + 5 === nlfr_count_posts( array( array( 'day' => 'a', 'n' => 7 ), array( 'day' => 'b', 'n' => 2 ), array( 'day' => 'c', 'n' => 5 ) ) ) );
t( 'posts: rows of one event each (n defaults to 1)', 5 === nlfr_count_posts( array_fill( 0, 8, array( 'day' => 'x' ) ) ) );
t( 'posts: nothing / no day', 0 === nlfr_count_posts( array() ) && 0 === nlfr_count_posts( array( array( 'n' => 3 ) ) ) );

/* one reaction per giver per day */
$rx = array(
	array( 'giver' => 7, 'day' => '2026-11-18' ), array( 'giver' => 7, 'day' => '2026-11-18' ), // a reaction and a thanks of the same giver, same day
	array( 'giver' => 7, 'day' => '2026-11-17' ),
	array( 'giver' => 8, 'day' => '2026-11-18' ),
	array( 'giver' => 3, 'day' => '2026-11-18' ), // the member himself
	array( 'giver' => 0, 'day' => '2026-11-18' ), array( 'giver' => 9, 'day' => '' ),
);
t( 'reacts: one per giver per day, self and broken rows out', 3 === nlfr_count_reacts( $rx, 3 ) );
t( 'reacts: without a member id only broken rows go', 4 === nlfr_count_reacts( $rx ) );
t( 'reacts: none', 0 === nlfr_count_reacts( array(), 1 ) );

/* exclusion */
t( 'fixture contact', nlfr_is_fixture( 'test1@example.invalid' ) && nlfr_is_fixture( ' Sample@EXAMPLE.INVALID ' ) );
t( 'not a fixture', ! nlfr_is_fixture( 'a@example.com' ) && ! nlfr_is_fixture( 'example.invalid@gmail.com' ) && ! nlfr_is_fixture( '' ) );
t( 'excluded: status not ok', nlfr_excluded( array( 'status' => 'blocked', 'contact' => 'a@b.co' ) ) && nlfr_excluded( array( 'status' => 'pending', 'contact' => 'a@b.co' ) ) );
t( 'excluded: fixture', nlfr_excluded( array( 'status' => 'ok', 'contact' => 'x@example.invalid' ) ) );
t( 'excluded: no row', nlfr_excluded( null ) && nlfr_excluded( array() ) );
t( 'a real member counts', ! nlfr_excluded( array( 'status' => 'ok', 'contact' => 'yossi@gmail.com' ) ) );

/* stars and words */
t( 'stars text', '' === nlfr_stars_text( 0 ) && '★' === nlfr_stars_text( 1 ) && '★★★' === nlfr_stars_text( 3 ) && '★★★★★' === nlfr_stars_text( 5 ) );
t( 'stars text clamps', '★★★★★' === nlfr_stars_text( 9 ) && '' === nlfr_stars_text( -2 ) );
t( 'chip label (the brief)', 'דרגת גמר, 3 מתוך 5 כוכבים, 212 נקודות' === nlfr_chip_label( nlfr_level( 212, 0, 0 ), 212 ) );
t( 'star words for the notice', 'שני כוכבים' === nlfr_star_words( 2 ) && 'כוכב אחד' === nlfr_star_words( 1 ) );
t( 'month in Hebrew', 'נובמבר 2026' === nlfr_month_he( gmmktime( 12, 0, 0, 11, 18, 2026 ) ) && '' === nlfr_month_he( 0 ) );

/* level-up notice */
t( 'levelup: nothing stored = store silently', array( 'show' => false, 'store' => 3 ) === nlfr_levelup( null, 3 ) );
t( 'levelup: up = show and store', array( 'show' => true, 'store' => 2 ) === nlfr_levelup( 1, 2 ) );
t( 'levelup: from 0 to 1 shows', true === nlfr_levelup( 0, 1 )['show'] );
t( 'levelup: same = nothing', array( 'show' => false, 'store' => null ) === nlfr_levelup( 2, 2 ) );
t( 'levelup: down = store quietly', array( 'show' => false, 'store' => 1 ) === nlfr_levelup( 3, 1 ) );

/* the sheet rows and the public rules come from the same weights */
$b = nlfr_breakdown( array( 'helped' => 6, 'reacts' => 31, 'kudos' => 3, 'together' => 1, 'posts' => 20 ) );
t( 'breakdown: board order, five rows without skills', array( 'helped', 'reacts', 'kudos', 'together', 'posts' ) === array_column( $b, 'key' ) );
t( 'breakdown: board numbers', array( 90, 62, 30, 10, 20 ) === array_column( $b, 'pts' ) && array( 6, 31, 3, 1, 20 ) === array_column( $b, 'n' ) );
$b2 = nlfr_breakdown( array( 'skills' => 2, 'posts' => 1 ) );
t( 'breakdown: the skills row when it counts, rows add up', 'skills' === end( $b2 )['key'] && nlfr_points( array( 'skills' => 2, 'posts' => 1 ) ) === array_sum( array_column( $b2, 'pts' ) ) );
$rr = nlfr_rule_rows();
t( 'rules: five rows, highest first', 5 === count( $rr ) && array( 15, 10, 3, 2, 1 ) === array_column( $rr, 1 ) );
t( 'rules: board wording', 'פרגון מחבר אחר, או "עבדו יחד" שאושר' === $rr[1][0] && 'תשובה שכתבתם, או דיון שפתחתם וקיבל תשובה (עד 5 ביום)' === $rr[4][0] && 'תגובה חיובית על הודעה שלכם (אחת ביום מכל חבר)' === $rr[3][0] );
t( 'rules fine line (board)', 'לדרגת מפתח צריך גם 5 תשובות שסומנו "עזרה לי" מחמישה שואלים שונים, ו-90 יום בפורום. תגובה של אדם על עצמו לא נספרת.' === nlfr_rules_fine() );

/* leaders order */
$ls = nlfr_leader_sort( array( array( 'id' => 1, 'points' => 30, 'helped' => 0 ), array( 'id' => 2, 'points' => 84, 'helped' => 1 ), array( 'id' => 3, 'points' => 30, 'helped' => 2 ), array( 'id' => 4, 'points' => 30, 'helped' => 2 ) ) );
t( 'leaders: points, then helped, then the older member', array( 2, 3, 4, 1 ) === array_column( $ls, 'id' ) );

/* static checks on the module's files */
$php  = file_get_contents( __DIR__ . '/../inc/pro-forum-rep.php' );
$js   = file_get_contents( __DIR__ . '/../assets/proforum/rep.js' );
$css  = file_get_contents( __DIR__ . '/../assets/proforum/rep.css' );
$core = file_get_contents( __DIR__ . '/../inc/pro-forum.php' );
$all  = $php . $js . $css;
t( 'no long dashes', false === strpos( $all, '—' ) && false === strpos( $all, '–' ) );
t( 'no banned words', ! preg_match( '/פלטפורמה|המערכת|אינטראקטיבי|אטלס|נחבר אתכם/u', $all ) );
t( 'no emoji', ! preg_match( '/[\x{1F300}-\x{1FAFF}\x{2600}-\x{2604}\x{2606}-\x{27BF}]/u', $all ) );
t( 'stars never gold or yellow', ! preg_match( '/gold|#FFD|#FFC|#F5C|#FACC|#EAB308|#FBBF24|#F59E0B|yellow/i', preg_replace( '~/\*.*?\*/~s', '', $css ) ) && false !== strpos( $css, '#B0144F' ) );
t( 'no innerHTML / eval in js', ! preg_match( '/innerHTML|outerHTML|insertAdjacentHTML|\beval\s*\(|new Function|document\.write/', $js ) );
t( 'js reads the numbers from NLFR, never its own table', false !== strpos( $js, 'window.NLFR' ) && ! preg_match( '/\b(1000|400|150)\b/', $js ) );
t( 'no 403 / 401, errors are 400', ! preg_match( "/'status' => 40[13]/", $php ) );
t( 'route hidden from the index, public read through nlf_guard view', false !== strpos( $php, "'show_in_index' => false" ) && false !== strpos( $php, "nlf_guard( \$q, 'view' )" ) && false !== strpos( $php, "'/forum/rep/member'" ) );
t( 'no write route', 1 === substr_count( $php, 'register_rest_route(' ) && false !== strpos( $php, "'methods' => 'GET'" ) );
t( 'no redirects, no robots changes', ! preg_match( '/wp_redirect\s*\(|wp_safe_redirect\s*\(|header\(\s*[\'"]Location|noindex|nofollow|\b30[12]\b/i', $all ) );
t( 'no new table', false === stripos( $php, 'CREATE TABLE' ) && false === strpos( $php, 'dbDelta' ) );
t( 'no contact in the public answer', ! preg_match( "/'contact'\s*=>/", $php ) );
t( 'every query prepared', substr_count( $php, '$wpdb->get_results( $wpdb->prepare(' ) + substr_count( $php, '$wpdb->get_col( $wpdb->prepare(' ) === substr_count( $php, '$wpdb->get_' ) );
t( 'cache keys carry the version', false !== strpos( $php, "'nlfr_s' . NLFR_VER" ) && false !== strpos( $php, "'nlfr_l' . NLFR_VER" ) );
t( 'hooks used', 1 === preg_match_all( "/add_filter\( 'nlf_name_extra'.*?\}, 15, 2 \);/s", $php ) && false !== strpos( $php, "add_filter( 'nlf_home_after_start'" ) && false !== strpos( $php, "}, 20, 1 );" )
	&& false !== strpos( $php, "add_filter( 'nlf_member_bar_extra'" ) && false !== strpos( $php, "add_filter( 'nlf_home_notices'" ) && false !== strpos( $php, "add_filter( 'nlf_card_member_block'" ) );
t( 'the rules are real HTML in a dialog', false !== strpos( $php, 'id="nlfr-rules"' ) && false !== strpos( $php, 'nlfr_rules_html()' ) );
t( 'chip a11y: stars aria-hidden', false !== strpos( $php, '<span class="nlfr-st" aria-hidden="true">' ) );
t( 'css: buttons and headings carry !important colours', preg_match( '/button\.nlfr-chip\{[^}]*color:#8A0F3D !important/', $css ) && preg_match( '/h2\.nlfr-h\{[^}]*color:#101820 !important/', $css ) );
t( 'css: chip 26px with a 44px hit area', false !== strpos( $css, 'height:26px' ) && false !== strpos( $css, 'button.nlfr-chip::after{content:"";position:absolute;inset:-9px -4px}' ) );
t( 'css: five tiles from 900px', false !== strpos( $css, '@media (min-width:900px)' ) );
t( 'every new function and class uses the nlfr prefix', ! preg_match( '/^function (?!nlfr_)/m', $php ) && ! preg_match( '/\.(?!nlfr-|nlf-|nlf\b|is-)[a-z]+-[a-z]+\{/', $css ) );
t( 'js under 16 KB', strlen( $js ) < 16384 );
t( 'core: the module loads by one line at the end, after the card module', 1 === substr_count( $core, "require_once __DIR__ . '/pro-forum-rep.php'" )
	&& strpos( $core, "'/pro-forum-rep.php'" ) > strpos( $core, "'/pro-forum-card.php'" ) );

echo "\n$pass passed, $fail failed\n";
exit( $fail ? 1 : 0 );
