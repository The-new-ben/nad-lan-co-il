<?php
/**
 * nadlan-config: the professionals' forum, HTML (loaded by inc/pro-forum.php). Server-side pages that read with JavaScript off,
 * inside the theme (get_header / get_footer). Every rule is scoped under .nlf (assets/proforum/forum.css).
 * Owner correction 12.11.2026: the forum window, contact buttons and owner controls print only on the profile of a professional
 * who joined himself (a linked member); every other card gets a small neutral box and "זה הכרטיס שלכם?". No long dashes here.
 */
if ( ! defined( 'ABSPATH' ) ) { exit; }

/* ---------------------------------------------------------------- small parts */

function nlf_svg( $name ) {
	$p = array(
		'chat'  => '<path d="M4 5h16v11H9l-5 4z"/>',
		'back'  => '<path d="M9 5l7 7-7 7"/>',
		'share' => '<circle cx="6" cy="12" r="2.5"/><circle cx="18" cy="6" r="2.5"/><circle cx="18" cy="18" r="2.5"/><path d="M8.2 10.8l7.6-3.6M8.2 13.2l7.6 3.6"/>',
		'close' => '<path d="M6 6l12 12M18 6L6 18"/>',
		'check' => '<path d="M4 12l5 5L20 6"/>',
		'heart' => '<path d="M12 20s-7-4.4-7-9.6A4 4 0 0112 8a4 4 0 017 2.4C19 15.6 12 20 12 20z"/>',
	);
	return '<svg aria-hidden="true" focusable="false" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">' . ( $p[ $name ] ?? '' ) . '</svg>';
}

function nlf_tint_style( $pair ) { return '--nlf-bg:' . esc_attr( $pair[0] ) . ';--nlf-fg:' . esc_attr( $pair[1] ); }

function nlf_cat_tag( $cat ) {
	$c = nlf_categories();
	$x = isset( $c[ $cat ] ) ? $c[ $cat ] : $c['general'];
	return '<span class="nlf-tag" style="' . nlf_tint_style( array( $x[1], $x[2] ) ) . '">' . esc_html( $x[0] ) . '</span>';
}

function nlf_kind_tag( $kind ) {
	if ( 'question' === $kind ) { return ''; }
	$k = nlf_kinds();
	return isset( $k[ $kind ] ) ? '<span class="nlf-tag nlf-tag-plain">' . esc_html( $k[ $kind ] ) . '</span>' : '';
}

function nlf_avatar( $a, $big = false ) {
	$cls = 'nlf-av' . ( $a['pro'] ? ' nlf-av-sq' : '' ) . ( $big ? ' nlf-av-lg' : '' );
	return '<span class="' . $cls . '" style="' . nlf_tint_style( $a['tint'] ) . '" aria-hidden="true">' . esc_html( nlf_initials( $a['name'] ) ) . '</span>';
}

/** the author's name line: name · label (a link to the profile only for a joined professional with a public card) */
function nlf_author_line( $a ) {
	$txt = esc_html( $a['name'] ) . ( '' !== $a['label'] ? ' · ' . esc_html( $a['label'] ) : '' );
	$out = '' !== $a['url'] ? '<a class="nlf-who" href="' . esc_url( $a['url'] ) . '">' . $txt . '</a>' : '<span class="nlf-who">' . $txt . '</span>';
	if ( '' !== $a['verified'] ) { $out .= '<span class="nlf-ver">' . nlf_svg( 'check' ) . esc_html( $a['verified'] ) . '</span>'; }
	return $out;
}

function nlf_when( $sql ) {
	$ts  = nlf_ts( $sql );
	$ago = nlf_ago( $ts, time() );
	return '<time datetime="' . esc_attr( gmdate( 'c', $ts ) ) . '">' . esc_html( '' !== $ago ? $ago : wp_date( 'j.n.Y', $ts ) ) . '</time>';
}

/** direct contact to a JOINED professional who switched his phone on himself; no prefilled text */
function nlf_phone_block( $a, $intro = true ) {
	if ( empty( $a['phone'] ) ) { return ''; }
	$p = $a['phone'];
	$h = '<div class="nlf-direct">';
	if ( $intro ) { $h .= '<span class="nlf-direct-t">' . esc_html( 'פנייה ישירה אל ' . $a['name'] . ':' ) . '</span>'; }
	$h .= '<div class="nlf-two">';
	if ( '' !== $p['wa'] ) { $h .= '<a class="nlf-btn nlf-btn-fill" href="' . esc_url( 'https://wa.me/' . $p['wa'] ) . '" target="_blank" rel="noopener">וואטסאפ</a>'; }
	if ( '' !== $p['tel'] ) { $h .= '<a class="nlf-btn nlf-btn-line" href="' . esc_url( 'tel:' . $p['tel'] ) . '">חיוג</a>'; }
	return $h . '</div></div>';
}

function nlf_trap() {
	return '<div class="nlf-trap" aria-hidden="true"><label>אתר<input type="text" name="website" tabindex="-1" autocomplete="off" value=""></label></div>';
}

/** the consent sentence; a link whose option is empty is left out (never a dead link) */
function nlf_consent_html() {
	$rules = esc_url( (string) get_option( 'nadlan_forum_rules_url', '' ) );
	$priv  = esc_url( (string) get_option( 'nadlan_forum_privacy_url', '' ) );
	$r = '' !== $rules ? '<a href="' . $rules . '" target="_blank" rel="noopener">כללי הפורום</a>' : 'כללי הפורום';
	$p = '' !== $priv ? '<a href="' . $priv . '" target="_blank" rel="noopener">מדיניות הפרטיות</a>' : 'מדיניות הפרטיות';
	return 'קראתי את ' . $r . ' ואת ' . $p . '. המייל לא מוצג לאף אחד.';
}

function nlf_member_bar( $me ) {
	if ( ! $me ) { return ''; }
	$a = nlf_author( $me );
	return '<div class="nlf-mebar"><span>נכנסתם בתור <b>' . esc_html( $a['name'] ) . '</b></span><button type="button" class="nlf-link" data-nlf-leave>יציאה</button></div>';
}

/* ---------------------------------------------------------------- the forum home */

function nlf_q( $sql, $args ) { global $wpdb; return $args ? $wpdb->prepare( $sql, $args ) : $sql; } // phpcs:ignore

function nlf_render_home() {
	global $wpdb;
	$a  = nlf_filter_args();
	$me = nlf_me();
	$tt = nlf_t( 'topics' );
	$where = array(); $args = array();
	if ( 'mine' === $a['v'] ) {
		$where[] = 'member_id = %d'; $args[] = $me ? (int) $me['id'] : 0;
		$where[] = "status IN ('live','pending','hidden')";
	} else {
		$where[] = "status = 'live'";
	}
	if ( '' !== $a['c'] ) { $where[] = 'cat = %s'; $args[] = $a['c']; }
	if ( 'open' === $a['v'] ) { $where[] = 'reply_count = 0'; }
	if ( 'requests' === $a['v'] ) { $where[] = "kind = 'seek'"; $where[] = "status_seek = 'open'"; } // the open-requests board
	if ( 'hot' === $a['v'] ) { $where[] = 'last_at >= %s'; $args[] = gmdate( 'Y-m-d H:i:s', time() - 7 * DAY_IN_SECONDS ); }
	$w     = implode( ' AND ', $where );
	$order = 'hot' === $a['v'] ? '(reply_count * 3 + thanks_count * 2 + view_count / 20) DESC, last_at DESC' : ( 'open' === $a['v'] ? 'created_at DESC' : 'last_at DESC' );
	$per   = 20;
	$total = ( 'mine' === $a['v'] && ! $me ) ? 0 : (int) $wpdb->get_var( nlf_q( "SELECT COUNT(*) FROM $tt WHERE $w", $args ) );
	$rows  = $total ? $wpdb->get_results( nlf_q( "SELECT * FROM $tt WHERE $w ORDER BY $order LIMIT " . (int) $per . ' OFFSET ' . (int) ( ( $a['pg'] - 1 ) * $per ), $args ), ARRAY_A ) : array();
	$open_args = array(); $open_w = "status = 'live' AND reply_count = 0";
	if ( '' !== $a['c'] ) { $open_w .= ' AND cat = %s'; $open_args[] = $a['c']; }
	$open_n = (int) $wpdb->get_var( nlf_q( "SELECT COUNT(*) FROM $tt WHERE $open_w", $open_args ) );

	// how many joined professionals offered themselves on each "seek" request in the list (real counts only)
	$seek = array();
	$ids  = array();
	foreach ( (array) $rows as $r ) { if ( 'seek' === $r['kind'] ) { $ids[] = (int) $r['id']; } }
	if ( $ids ) {
		foreach ( (array) $wpdb->get_results( 'SELECT r.topic_id, COUNT(DISTINCT m.pro_id) AS n FROM ' . nlf_t( 'replies' ) . ' r JOIN ' . nlf_t( 'members' ) . " m ON m.id = r.member_id
			WHERE r.status = 'live' AND m.pro_id IS NOT NULL AND r.topic_id IN (" . implode( ',', $ids ) . ') GROUP BY r.topic_id', ARRAY_A ) as $s ) {
			$seek[ (int) $s['topic_id'] ] = (int) $s['n'];
		}
	}

	$sort = array( '' => 'חדש', 'requests' => 'בקשות פתוחות', 'hot' => 'חם השבוע', 'open' => 'בלי תשובה', 'mine' => 'שלי' );
	ob_start();
	?>
<div class="nlf nlf-page" dir="rtl">
	<header class="nlf-top">
		<span class="nlf-kicker">נדל"ן · בעלי מקצוע</span>
		<h1 class="nlf-h1"><?php echo esc_html( nlf_home_h1() ); ?></h1>
		<p class="nlf-lead">שואלים, עונים ופונים ישר לבעלי המקצוע שהצטרפו: קבלנים, עורכי דין, שמאים ויועצי משכנתאות.</p>
		<?php echo nlf_member_bar( $me ); // phpcs:ignore -- escaped inside ?>
	</header>
	<section class="nlf-start" aria-label="כתיבת הודעה">
		<button type="button" class="nlf-askbtn" data-nlf-compose><span class="nlf-plus" aria-hidden="true">+</span><span>מה אתם צריכים? כתבו שאלה או בקשה</span></button>
		<div class="nlf-quick">
			<button type="button" class="nlf-chip" style="<?php echo nlf_tint_style( array( '#DCE6F2', '#1D3B66' ) ); // phpcs:ignore ?>" data-nlf-compose data-kind="seek" data-cat="build">מחפש קבלן שיפוצים</button>
			<button type="button" class="nlf-chip" style="<?php echo nlf_tint_style( array( '#EBDDF0', '#4A1D5E' ) ); // phpcs:ignore ?>" data-nlf-compose data-kind="question" data-cat="law">שאלה לעורך דין</button>
			<button type="button" class="nlf-chip" style="<?php echo nlf_tint_style( array( '#DCEFE3', '#1B4D33' ) ); // phpcs:ignore ?>" data-nlf-compose data-kind="seek" data-cat="value">צריך שמאי</button>
		</div>
	</section>
	<nav class="nlf-sort" aria-label="מיון">
		<?php foreach ( $sort as $k => $label ) :
			$on  = $k === $a['v'] || ( '' === $k && 'new' === $a['v'] );
			$url = nlf_home_url( array( 'c' => $a['c'], 'v' => $k ) ); ?>
			<a class="nlf-pill<?php echo $on ? ' is-on' : ''; ?>" href="<?php echo esc_url( $url ); ?>"<?php echo $on ? ' aria-current="page"' : ''; ?>><?php echo esc_html( $label ); ?><?php if ( 'open' === $k && $open_n > 0 ) : ?> <span class="nlf-hot"><?php echo (int) $open_n; ?></span><?php endif; ?></a>
		<?php endforeach; ?>
	</nav>
	<nav class="nlf-cats" aria-label="נושאים">
		<a class="nlf-cat<?php echo '' === $a['c'] ? ' is-on' : ''; ?>" href="<?php echo esc_url( nlf_home_url( array( 'v' => $a['v'] ) ) ); ?>"<?php echo '' === $a['c'] ? ' aria-current="page"' : ''; ?>>כל הנושאים</a>
		<?php foreach ( nlf_categories() as $k => $c ) : ?>
			<a class="nlf-cat<?php echo $k === $a['c'] ? ' is-on' : ''; ?>" style="<?php echo nlf_tint_style( array( $c[1], $c[2] ) ); // phpcs:ignore ?>" href="<?php echo esc_url( nlf_home_url( array( 'c' => $k, 'v' => $a['v'] ) ) ); ?>"<?php echo $k === $a['c'] ? ' aria-current="page"' : ''; ?>><?php echo esc_html( $c[0] ); ?></a>
		<?php endforeach; ?>
	</nav>
	<p class="nlf-live" id="nlf-live" role="status" aria-live="polite"></p>
	<div class="nlf-list">
	<?php if ( 'mine' === $a['v'] && ! $me ) : ?>
		<div class="nlf-empty"><p>כדי לראות את ההודעות שלכם, היכנסו. זה צעד אחד.</p><button type="button" class="nlf-btn nlf-btn-fill" data-nlf-enter>כניסה</button></div>
	<?php elseif ( ! $rows ) : ?>
		<div class="nlf-empty"><p><?php echo ( '' === $a['c'] && '' === $a['v'] ) ? 'עוד אין דיונים. כתבו את הראשון.' : 'אין כאן דיונים עדיין. כתבו את הראשון.'; ?></p><button type="button" class="nlf-btn nlf-btn-hot" data-nlf-compose<?php echo '' !== $a['c'] ? ' data-cat="' . esc_attr( $a['c'] ) . '"' : ''; ?>>כתבו הודעה</button></div>
	<?php else : foreach ( $rows as $t ) :
		$fresh = time() - nlf_ts( $t['last_at'] ) < HOUR_IN_SECONDS; ?>
		<article class="nlf-card">
			<div class="nlf-meta"><?php echo nlf_cat_tag( $t['cat'] ) . nlf_kind_tag( $t['kind'] ); // phpcs:ignore ?>
				<?php if ( '' !== $t['city'] ) : ?><span><?php echo esc_html( $t['city'] ); ?></span><?php endif; ?>
				<span class="nlf-when<?php echo $fresh ? ' is-new' : ''; ?>"><?php if ( $fresh ) : ?><span class="nlf-dot" aria-hidden="true"></span><?php endif; ?><?php echo nlf_when( $t['last_at'] ); // phpcs:ignore ?></span>
			</div>
			<h2 class="nlf-ttl"><a href="<?php echo esc_url( home_url( '/forum/' . (int) $t['id'] . '/' ) ); ?>"><?php echo esc_html( $t['title'] ); ?></a></h2>
			<div class="nlf-foot">
				<?php if ( 'live' !== $t['status'] ) : ?><span class="nlf-chip-s nlf-wait">ממתינה לבדיקה</span><?php endif; ?>
				<?php if ( (int) $t['solved_reply_id'] > 0 ) : ?><span class="nlf-chip-s nlf-ok"><?php echo nlf_svg( 'check' ); // phpcs:ignore ?>יש תשובה שעזרה</span><?php endif; ?>
				<?php if ( ! empty( $seek[ (int) $t['id'] ] ) ) : $n = $seek[ (int) $t['id'] ]; ?><span><?php echo esc_html( 1 === $n ? 'בעל מקצוע אחד הציע את עצמו' : $n . ' בעלי מקצוע הציעו את עצמם' ); ?></span><?php endif; ?>
				<?php if ( 'live' === $t['status'] && 0 === (int) $t['reply_count'] ) : ?><span class="nlf-chip-s nlf-new">מחכה לתשובה ראשונה</span><?php endif; ?>
				<span class="nlf-push"><?php echo esc_html( nlf_count_words( $t['reply_count'], 'תשובה אחת', 'תשובות' ) ); ?></span>
				<?php if ( (int) $t['view_count'] > 0 ) : ?><span><?php echo esc_html( nlf_count_words( $t['view_count'], 'צפייה אחת', 'צפיות' ) ); ?></span><?php endif; ?>
			</div>
		</article>
	<?php endforeach; endif; ?>
	</div>
	<?php
	$pages = (int) ceil( $total / $per );
	$GLOBALS['nlf_pages'] = $pages; // the canonical of a page past the last one is /forum/
	if ( $pages > 1 ) :
		$base = array( 'c' => $a['c'], 'v' => $a['v'] ); ?>
	<nav class="nlf-pages" aria-label="עמודים">
		<?php if ( $a['pg'] > 1 ) : ?><a class="nlf-btn nlf-btn-line" href="<?php echo esc_url( nlf_home_url( $base + array( 'pg' => $a['pg'] > 2 ? $a['pg'] - 1 : '' ) ) ); ?>">הקודמים</a><?php endif; ?>
		<span>עמוד <?php echo (int) $a['pg']; ?> מתוך <?php echo (int) $pages; ?></span>
		<?php if ( $a['pg'] < $pages ) : ?><a class="nlf-btn nlf-btn-line" href="<?php echo esc_url( nlf_home_url( $base + array( 'pg' => $a['pg'] + 1 ) ) ); ?>">הבאים</a><?php endif; ?>
	</nav>
	<?php endif; ?>
	<?php if ( $me && (int) $me['pro_id'] > 0 ) { echo nlf_owner_box( (int) $me['pro_id'] ); } // phpcs:ignore -- his switches stay reachable even when his profile is hidden ?>
	<?php echo nlf_directory_band(); // phpcs:ignore -- escaped inside ?>
</div>
	<?php
	return ob_get_clean();
}

/* ---------------------------------------------------------------- one discussion */

function nlf_render_topic( $t ) {
	global $wpdb;
	$me      = nlf_me();
	$admin   = nlf_is_admin();
	$own_w   = $me ? $wpdb->prepare( ' OR member_id = %d', (int) $me['id'] ) : '';
	$replies = $wpdb->get_results( $wpdb->prepare( 'SELECT * FROM ' . nlf_t( 'replies' ) . " WHERE topic_id = %d AND (status = 'live'" . ( $admin ? " OR status IN ('pending','hidden')" : $own_w ) . ") AND status <> 'removed' ORDER BY id ASC LIMIT 300", (int) $t['id'] ), ARRAY_A );
	$replies = (array) $replies;
	$ids     = array( (int) $t['member_id'] );
	$byid    = array();
	foreach ( $replies as $r ) { $ids[] = (int) $r['member_id']; $byid[ (int) $r['id'] ] = $r; }
	$mem     = nlf_members( $ids );
	$solved  = (int) $t['solved_reply_id'];
	if ( $solved && isset( $byid[ $solved ] ) && 'live' === $byid[ $solved ]['status'] ) {
		usort( $replies, function ( $x, $y ) use ( $solved ) { return ( (int) $y['id'] === $solved ) <=> ( (int) $x['id'] === $solved ) ?: (int) $x['id'] <=> (int) $y['id']; } );
	} else { $solved = 0; }
	$mine_thanks = array();
	if ( $me ) {
		foreach ( (array) $wpdb->get_results( $wpdb->prepare( 'SELECT target_type, target_id FROM ' . nlf_t( 'thanks' ) . ' WHERE member_id = %d', (int) $me['id'] ), ARRAY_A ) as $x ) {
			$mine_thanks[ $x['target_type'] . (int) $x['target_id'] ] = 1;
		}
	}
	$is_author = $me && (int) $me['id'] === (int) $t['member_id'];
	$following = $me && nlf_follows( (int) $me['id'], (int) $t['id'] );
	$op        = nlf_author( $mem[ (int) $t['member_id'] ] ?? null );
	$cats      = nlf_categories();
	$catl      = isset( $cats[ $t['cat'] ] ) ? $cats[ $t['cat'] ][0] : $cats['general'][0];
	$url       = home_url( '/forum/' . (int) $t['id'] . '/' );
	$wa        = 'https://wa.me/?text=' . rawurlencode( $t['title'] . ' ' . $url );
	$live_n    = 0;
	foreach ( $replies as $r ) { if ( 'live' === $r['status'] ) { $live_n++; } }
	$topic_thanks_label = 'question' === $t['kind'] ? 'גם אני במצב הזה' : 'תודה';
	ob_start();
	?>
<div class="nlf nlf-page nlf-thread" dir="rtl" data-topic="<?php echo (int) $t['id']; ?>" data-live="<?php echo 'live' === $t['status'] ? '1' : '0'; ?>">
	<div class="nlf-bar">
		<a class="nlf-ico" href="<?php echo esc_url( home_url( '/forum/' ) ); ?>" aria-label="חזרה לפורום"><?php echo nlf_svg( 'back' ); // phpcs:ignore ?></a>
		<span class="nlf-crumb"><a href="<?php echo esc_url( home_url( '/forum/' ) ); ?>">פורום נדל"ן</a> › <a href="<?php echo esc_url( nlf_home_url( array( 'c' => $t['cat'] ) ) ); ?>"><?php echo esc_html( $catl ); ?></a></span>
		<button type="button" class="nlf-pill nlf-follow<?php echo $following ? ' is-on' : ''; ?>" data-nlf-follow aria-pressed="<?php echo $following ? 'true' : 'false'; ?>"><?php echo $following ? 'במעקב' : 'מעקב'; ?></button>
		<a class="nlf-ico nlf-ico-box" href="<?php echo esc_url( $wa ); ?>" target="_blank" rel="noopener" aria-label="שיתוף בוואטסאפ"><?php echo nlf_svg( 'share' ); // phpcs:ignore ?></a>
	</div>
	<section class="nlf-op" aria-labelledby="nlf-title">
		<div class="nlf-meta"><?php echo nlf_cat_tag( $t['cat'] ) . nlf_kind_tag( $t['kind'] ); // phpcs:ignore ?></div>
		<h1 class="nlf-h1 nlf-h1-t" id="nlf-title"><?php echo esc_html( $t['title'] ); ?></h1>
		<div class="nlf-arow"><?php echo nlf_avatar( $op ); // phpcs:ignore ?>
			<div class="nlf-acol"><?php echo nlf_author_line( $op ); // phpcs:ignore ?>
				<span class="nlf-sub"><?php echo esc_html( implode( ' · ', array_filter( array( $t['city'], wp_date( 'j.n.Y H:i', nlf_ts( $t['created_at'] ) ), nlf_count_words( $t['view_count'], 'צפייה אחת', 'צפיות' ) ) ) ) ); ?></span>
			</div>
		</div>
		<?php if ( (int) $t['pro_id'] > 0 && 'nadlan_professional' === get_post_type( (int) $t['pro_id'] ) && ! nlf_pro_removed( (int) $t['pro_id'] ) ) : $pid = (int) $t['pro_id']; ?>
			<p class="nlf-to-line">השאלה הופנתה אל <?php echo 'publish' === get_post_status( $pid ) ? '<a href="' . esc_url( get_permalink( $pid ) ) . '">' . esc_html( get_the_title( $pid ) ) . '</a>' : esc_html( get_the_title( $pid ) ); ?></p>
		<?php endif; ?>
		<?php if ( 'pending' === $t['status'] ) : ?><p class="nlf-note">ההודעה תעלה אחרי בדיקה קצרה</p><?php elseif ( 'live' !== $t['status'] ) : ?><p class="nlf-note">ההודעה מוסתרת עד בדיקה</p><?php endif; ?>
		<?php if ( '' !== trim( $t['body'] ) ) : ?><p class="nlf-body nlf-body-op"><?php echo nlf_body_html( $t['body'] ); // phpcs:ignore -- escaped ?></p><?php endif; ?>
		<?php if ( 'live' === $t['status'] ) : $on = isset( $mine_thanks[ 'topic' . (int) $t['id'] ] ); ?>
		<div class="nlf-acts">
			<button type="button" class="nlf-pill nlf-thank<?php echo $on ? ' is-on' : ''; ?>" data-nlf-thank="topic" data-id="<?php echo (int) $t['id']; ?>" data-label="<?php echo esc_attr( $topic_thanks_label ); ?>" aria-pressed="<?php echo $on ? 'true' : 'false'; ?>"><?php echo nlf_svg( 'heart' ); // phpcs:ignore ?><span><?php echo esc_html( $topic_thanks_label . ( (int) $t['thanks_count'] > 0 ? ' · ' . (int) $t['thanks_count'] : '' ) ); ?></span></button>
			<button type="button" class="nlf-pill nlf-mute nlf-push" data-nlf-report="topic" data-id="<?php echo (int) $t['id']; ?>">דיווח</button>
		</div>
		<?php endif; ?>
	</section>
	<div class="nlf-rhead"><h2 class="nlf-h2"><?php echo esc_html( $live_n > 0 ? nlf_count_words( $live_n, 'תשובה אחת', 'תשובות' ) : 'תשובות' ); ?></h2></div>
	<p class="nlf-live" id="nlf-live" role="status" aria-live="polite"></p>
	<div class="nlf-replies" id="nlf-replies">
		<?php if ( ! $replies ) : ?><p class="nlf-empty-s" data-nlf-noreplies>עוד אין תשובות. כתבו את הראשונה.</p><?php endif; ?>
		<?php foreach ( $replies as $r ) :
			$a  = nlf_author( $mem[ (int) $r['member_id'] ] ?? null );
			$is_solved = (int) $r['id'] === $solved;
			$on = isset( $mine_thanks[ 'reply' . (int) $r['id'] ] ); ?>
		<article class="nlf-reply<?php echo $is_solved ? ' is-solved' : ''; ?>" id="r<?php echo (int) $r['id']; ?>" data-id="<?php echo (int) $r['id']; ?>" data-name="<?php echo esc_attr( $a['name'] ); ?>" data-text="<?php echo esc_attr( nlf_excerpt( $r['body'], 120 ) ); ?>">
			<?php if ( $is_solved ) : ?><span class="nlf-chip-s nlf-ok nlf-solved-chip"><?php echo nlf_svg( 'check' ); // phpcs:ignore ?>התשובה שעזרה</span><?php endif; ?>
			<div class="nlf-arow"><?php echo nlf_avatar( $a, true ); // phpcs:ignore ?><div class="nlf-acol"><?php echo nlf_author_line( $a ); // phpcs:ignore ?></div><?php echo nlf_when( $r['created_at'] ); // phpcs:ignore ?></div>
			<?php if ( (int) $r['quote_id'] > 0 && isset( $byid[ (int) $r['quote_id'] ] ) && 'live' === $byid[ (int) $r['quote_id'] ]['status'] ) :
				$qr = $byid[ (int) $r['quote_id'] ]; $qa = nlf_author( $mem[ (int) $qr['member_id'] ] ?? null ); ?>
				<blockquote class="nlf-quote"><a href="#r<?php echo (int) $qr['id']; ?>"><?php echo esc_html( $qa['name'] . ' כתב/ה:' ); ?></a> "<?php echo esc_html( nlf_excerpt( $qr['body'], 140 ) ); ?>"</blockquote>
			<?php endif; ?>
			<p class="nlf-body"><?php echo nlf_body_html( $r['body'] ); // phpcs:ignore -- escaped ?></p>
			<?php if ( 'pending' === $r['status'] ) : ?><p class="nlf-note">ההודעה תעלה אחרי בדיקה קצרה</p><?php elseif ( 'hidden' === $r['status'] ) : ?><p class="nlf-note">ההודעה מוסתרת עד בדיקה</p><?php endif; ?>
			<?php if ( 'live' === $r['status'] ) : ?>
			<div class="nlf-acts">
				<button type="button" class="nlf-pill nlf-thank<?php echo $on ? ' is-on' : ''; ?>" data-nlf-thank="reply" data-id="<?php echo (int) $r['id']; ?>" data-label="תודה" aria-pressed="<?php echo $on ? 'true' : 'false'; ?>"><span><?php echo esc_html( 'תודה' . ( (int) $r['thanks_count'] > 0 ? ' · ' . (int) $r['thanks_count'] : '' ) ); ?></span></button>
				<button type="button" class="nlf-pill" data-nlf-quote>ציטוט</button>
				<?php if ( $is_author && (int) $r['member_id'] !== (int) $me['id'] ) : ?><button type="button" class="nlf-pill nlf-solve" data-nlf-solve="<?php echo (int) $r['id']; ?>" aria-pressed="<?php echo $is_solved ? 'true' : 'false'; ?>"><?php echo $is_solved ? 'ביטול הסימון' : 'זו התשובה שעזרה'; ?></button><?php endif; ?>
				<button type="button" class="nlf-pill nlf-mute nlf-push" data-nlf-report="reply" data-id="<?php echo (int) $r['id']; ?>">דיווח</button>
			</div>
			<?php echo nlf_phone_block( $a ); // phpcs:ignore ?>
			<?php endif; ?>
		</article>
		<?php endforeach; ?>
	</div>
	<?php if ( 'live' === $t['status'] ) : ?>
	<form class="nlf-replyform" data-nlf-replyform novalidate>
		<label for="nlf-reply-body" class="nlf-label">כתבו תשובה</label>
		<div class="nlf-quoting" hidden><span></span><button type="button" class="nlf-link" data-nlf-unquote>ביטול הציטוט</button></div>
		<div class="nlf-replyrow">
			<textarea id="nlf-reply-body" name="body" rows="2" maxlength="4000" placeholder="כתבו תשובה"></textarea>
			<button type="submit" class="nlf-btn nlf-btn-hot">שליחה</button>
		</div>
		<input type="hidden" name="quote_id" value="">
		<?php echo nlf_trap(); // phpcs:ignore ?>
		<?php echo nlf_member_bar( $me ); // phpcs:ignore ?>
	</form>
	<?php endif; ?>
</div>
	<?php
	return ob_get_clean();
}

/* ---------------------------------------------------------------- the professional's profile */

/**
 * The black-framed "בפורום" window (Card board). Printed ONLY for a professional who joined (a linked member); '' otherwise.
 */
function nadlan_forum_card_window( $pro_post_id ) {
	$pro    = (int) $pro_post_id;
	if ( ! nlf_gate_open() ) { return ''; } // public helper: nothing while the forum is hidden, wherever it is called from
	$linked = nlf_pro_member( $pro );
	if ( ! $linked || nlf_pro_removed( $pro ) ) { return ''; }
	global $wpdb;
	$rt = nlf_t( 'replies' ); $tt = nlf_t( 'topics' ); $mt = nlf_t( 'members' );
	$ans_n = (int) $wpdb->get_var( $wpdb->prepare( "SELECT COUNT(*) FROM $rt r JOIN $mt m ON m.id = r.member_id JOIN $tt t ON t.id = r.topic_id
		WHERE m.pro_id = %d AND r.status = 'live' AND t.status = 'live'", $pro ) );
	$ans = $ans_n ? $wpdb->get_results( $wpdb->prepare( "SELECT r.id, r.body, r.thanks_count, r.created_at, t.id AS tid, t.title, t.reply_count FROM $rt r JOIN $mt m ON m.id = r.member_id JOIN $tt t ON t.id = r.topic_id
		WHERE m.pro_id = %d AND r.status = 'live' AND t.status = 'live' ORDER BY r.id DESC LIMIT 3", $pro ), ARRAY_A ) : array();
	$ask_n = (int) $wpdb->get_var( $wpdb->prepare( "SELECT COUNT(*) FROM $tt WHERE pro_id = %d AND status = 'live'", $pro ) );
	$ask = $ask_n ? $wpdb->get_results( $wpdb->prepare( "SELECT id, title, reply_count, created_at FROM $tt WHERE pro_id = %d AND status = 'live' ORDER BY id DESC LIMIT 3", $pro ), ARRAY_A ) : array();
	$today = $ans && nlf_ts( $ans[0]['created_at'] ) > time() - DAY_IN_SECONDS;
	$f     = nlf_pro_female( $pro );
	$him   = $f ? 'אותה' : 'אותו';
	$only  = $f ? 'רק אליה' : 'רק אליו';
	$a     = nlf_author( $linked );
	$uid   = 'nlfw' . $pro;
	ob_start();
	?>
<section class="nlf nlf-win" dir="rtl" aria-label="הפורום של בעל המקצוע" data-pro="<?php echo $pro; // phpcs:ignore ?>" data-pro-name="<?php echo esc_attr( get_the_title( $pro ) ); ?>" data-cat="<?php echo esc_attr( nlf_cat_for_profession( nlf_pro_profession( $pro ) ) ); ?>">
	<div class="nlf-win-h"><?php echo nlf_svg( 'chat' ); // phpcs:ignore ?><h2 class="nlf-h2">בפורום</h2><?php if ( $today ) : ?><span class="nlf-today"><span class="nlf-dot" aria-hidden="true"></span>פעיל היום</span><?php endif; ?></div>
	<?php if ( $ans_n || $ask_n ) : ?>
	<div class="nlf-tabs" role="tablist" aria-label="הפעילות בפורום">
		<?php $first = true; foreach ( array( 'a' => array( 'תשובות', $ans_n ), 'q' => array( 'שאלו ' . $him, $ask_n ) ) as $k => $tab ) : if ( $tab[1] < 1 ) { continue; } ?>
		<button type="button" role="tab" id="<?php echo esc_attr( $uid . $k ); ?>-t" aria-controls="<?php echo esc_attr( $uid . $k ); ?>" aria-selected="<?php echo $first ? 'true' : 'false'; ?>" tabindex="<?php echo $first ? '0' : '-1'; ?>"><?php echo esc_html( $tab[0] . ' ' . number_format( $tab[1] ) ); ?></button>
		<?php $first = false; endforeach; ?>
	</div>
	<?php $first = true; if ( $ans_n ) : ?>
	<div class="nlf-panel" role="tabpanel" id="<?php echo esc_attr( $uid ); ?>a" aria-labelledby="<?php echo esc_attr( $uid ); ?>a-t">
		<?php foreach ( $ans as $x ) : ?>
		<article class="nlf-mini"><a class="nlf-mini-t" href="<?php echo esc_url( home_url( '/forum/' . (int) $x['tid'] . '/#r' . (int) $x['id'] ) ); ?>"><?php echo esc_html( $x['title'] ); ?></a>
			<p>"<?php echo esc_html( nlf_excerpt( $x['body'], 160 ) ); ?>"</p>
			<span class="nlf-sub"><?php echo nlf_when( $x['created_at'] ); // phpcs:ignore ?><?php echo (int) $x['thanks_count'] > 0 ? esc_html( ' · ' . nlf_count_words( $x['thanks_count'], 'תודה אחת', 'תודות' ) ) : ''; ?></span></article>
		<?php endforeach; ?>
	</div>
	<?php $first = false; endif; if ( $ask_n ) : ?>
	<div class="nlf-panel" role="tabpanel" id="<?php echo esc_attr( $uid ); ?>q" aria-labelledby="<?php echo esc_attr( $uid ); ?>q-t"<?php echo $first ? '' : ' hidden'; ?>>
		<?php foreach ( $ask as $x ) : ?>
		<article class="nlf-mini"><a class="nlf-mini-t" href="<?php echo esc_url( home_url( '/forum/' . (int) $x['id'] . '/' ) ); ?>"><?php echo esc_html( $x['title'] ); ?></a>
			<span class="nlf-sub"><?php echo nlf_when( $x['created_at'] ); // phpcs:ignore ?><?php echo (int) $x['reply_count'] > 0 ? esc_html( ' · ' . nlf_count_words( $x['reply_count'], 'תשובה אחת', 'תשובות' ) ) : ''; ?></span></article>
		<?php endforeach; ?>
	</div>
	<?php endif; endif; ?>
	<form class="nlf-win-ask" data-nlf-ask novalidate>
		<label for="<?php echo esc_attr( $uid ); ?>-ask" class="nlf-label"><?php echo esc_html( 'שאלו ' . $him . ', או את ' . nlf_pro_plural_phrase( $pro ) . ' בפורום' ); ?></label>
		<div class="nlf-replyrow"><input id="<?php echo esc_attr( $uid ); ?>-ask" type="text" name="q" maxlength="140" placeholder="היי, אני מחפש..."><button type="submit" class="nlf-btn nlf-btn-hot">שליחה</button></div>
		<div class="nlf-radios">
			<label><input type="radio" name="to" value="pro" checked> <?php echo esc_html( $only ); ?></label>
			<label><input type="radio" name="to" value="all"> לכל הפורום</label>
		</div>
	</form>
	<?php if ( ! $ans_n && ! $ask_n ) : ?><a class="nlf-more" href="<?php echo esc_url( home_url( '/forum/' ) ); ?>">לפורום נדל"ן ←</a><?php endif; ?>
	<?php echo nlf_phone_block( $a ); // phpcs:ignore ?>
</section>
	<?php
	return ob_get_clean();
}

/** a card whose person did not join: never implies taking part (owner correction 12.11.2026) */
function nlf_neutral_box( $pro ) {
	$cat = nlf_cat_for_profession( nlf_pro_profession( $pro ) );
	return '<section class="nlf nlf-neutral" dir="rtl" aria-labelledby="nlf-nb-' . (int) $pro . '"><h2 class="nlf-h2" id="nlf-nb-' . (int) $pro . '">מחפשים בעל מקצוע?</h2>'
		. '<p>פרסמו בקשה בפורום ובעלי מקצוע שהצטרפו יענו לכם.</p>'
		. '<button type="button" class="nlf-btn nlf-btn-fill" data-nlf-compose data-kind="seek" data-cat="' . esc_attr( $cat ) . '">פרסמו בקשה</button></section>';
}

function nlf_claim_box( $pro ) {
	return '<section class="nlf nlf-claim" dir="rtl" aria-label="זה הכרטיס שלכם?" data-pro="' . (int) $pro . '"><div class="nlf-claim-t"><span class="nlf-claim-h">זה הכרטיס שלכם?</span>'
		. '<span>הצטרפות לפורום או הסרת הכרטיס. הכול בלחיצה, אחרי קוד למייל.</span></div><div class="nlf-claim-b">'
		. '<button type="button" class="nlf-pill nlf-pill-ink" data-nlf-join="' . (int) $pro . '">הצטרפות</button>'
		. '<button type="button" class="nlf-pill nlf-pill-ink" data-nlf-removal="' . (int) $pro . '">הסרת הכרטיס</button></div></section>';
}

/** "הפרופיל שלי" (Profile board): the linked professional's own switches; no redirect after any of them */
function nlf_owner_box( $pro ) {
	$me = nlf_me();
	if ( ! $me || (int) $me['pro_id'] !== (int) $pro || 'nadlan_professional' !== get_post_type( (int) $pro ) ) { return ''; }
	$s = nlf_owner_state( $pro );
	ob_start();
	?>
<section class="nlf nlf-owner" dir="rtl" data-nlf-owner data-pro="<?php echo (int) $pro; ?>" aria-labelledby="nlf-own-h">
	<div class="nlf-own-head"><h2 class="nlf-h2" id="nlf-own-h">הפרופיל שלי</h2><span class="nlf-own-only">רק אתם רואים את החלק הזה</span></div>
	<div class="nlf-removed" data-nlf-removed<?php echo $s['removed'] ? '' : ' hidden'; ?>><p>הפרופיל הוסר. <button type="button" class="nlf-link" data-nlf-restore>להחזרה לחצו כאן</button></p></div>
	<div data-nlf-owner-live<?php echo $s['removed'] ? ' hidden' : ''; ?>>
		<label class="nlf-switch"><span class="nlf-sw-t"><b>הפרופיל מוצג באתר</b><span>כיבוי מסתיר אותו מיד. אפשר להחזיר בכל רגע.</span></span><input type="checkbox" data-nlf-own="visible"<?php checked( $s['visible'] ); ?>></label>
		<label class="nlf-switch"><span class="nlf-sw-t"><b>הטלפון שלי מוצג</b><span>כבוי: פונים אליכם רק בהודעה דרך הפורום.</span></span><input type="checkbox" data-nlf-own="phone"<?php checked( $s['phone'] ); ?>></label>
		<div class="nlf-danger-zone">
			<button type="button" class="nlf-btn nlf-btn-danger" data-nlf-remove>הסרת הפרופיל מהאתר</button>
			<span class="nlf-sub">לחיצה אחת ואישור. הפרופיל יורד מיד, בלי לפנות לאף אחד ובלי לחכות לתשובה.</span>
			<div class="nlf-confirm" data-nlf-confirm hidden>
				<p>בטוחים? הפרופיל יורד מהאתר עכשיו. ההודעות שלכם בפורום נשארות, עם השם בלבד.</p>
				<div class="nlf-two"><button type="button" class="nlf-btn nlf-btn-danger-fill" data-nlf-remove-yes>כן, להסיר</button><button type="button" class="nlf-btn nlf-btn-line" data-nlf-remove-no>ביטול</button></div>
			</div>
		</div>
	</div>
	<p class="nlf-live" role="status" aria-live="polite"></p>
	<button type="button" class="nlf-link" data-nlf-leave>יציאה</button>
</section>
	<?php
	return ob_get_clean();
}

/* placement on a professional's page: through the_content, late (priority 40, after the profile at 6 and its wpautop shield at 11),
   so inc/professional-profile.php is not edited */
add_filter( 'the_content', function ( $content ) {
	if ( ! is_singular( 'nadlan_professional' ) || ! in_the_loop() || ! is_main_query() || ! nlf_gate_open() ) { return $content; }
	nlf_install();
	$pro = (int) get_the_ID();
	if ( $pro <= 0 || nlf_pro_removed( $pro ) ) { return $content; }
	$me  = nlf_me();
	if ( $me && (int) $me['pro_id'] === $pro ) {
		$html = nadlan_forum_card_window( $pro ) . nlf_owner_box( $pro );
	} elseif ( nlf_pro_member( $pro ) ) {
		$html = nadlan_forum_card_window( $pro ) . nlf_claim_box( $pro );
	} else {
		$html = nlf_neutral_box( $pro ) . nlf_claim_box( $pro );
	}
	$GLOBALS['nlf_card_printed'] = true;
	nlf_nocache();
	return $content . '<div class="nlf-card-zone" id="nlf-card-zone">' . $html . '</div>';
}, 40 );

/* ---------------------------------------------------------------- the sheets (once per forum surface) */

add_action( 'wp_footer', function () {
	if ( '' === nlf_rendering() && empty( $GLOBALS['nlf_card_printed'] ) ) { return; }
	$roles = nlf_roles();
	?>
<dialog class="nlf nlf-sheet" id="nlf-compose" dir="rtl" aria-labelledby="nlf-compose-h">
	<form class="nlf-form" data-nlf-composeform novalidate>
		<div class="nlf-sheet-h"><button type="button" class="nlf-ico" data-nlf-close aria-label="סגירה"><?php echo nlf_svg( 'close' ); // phpcs:ignore ?></button><h2 class="nlf-h2" id="nlf-compose-h">הודעה חדשה</h2><span class="nlf-draft" data-nlf-draft aria-live="polite"></span></div>
		<fieldset class="nlf-kinds"><legend>מה תרצו לכתוב?</legend>
			<div class="nlf-grid2"><?php foreach ( nlf_kinds() as $k => $l ) : ?><button type="button" data-kind="<?php echo esc_attr( $k ); ?>" aria-pressed="<?php echo 'question' === $k ? 'true' : 'false'; ?>"><?php echo esc_html( $l ); ?></button><?php endforeach; ?></div>
		</fieldset>
		<div class="nlf-field"><label for="nlf-c-cat">נושא</label><select id="nlf-c-cat" name="cat"><?php foreach ( nlf_categories() as $k => $c ) : ?><option value="<?php echo esc_attr( $k ); ?>"<?php selected( 'general', $k ); ?>><?php echo esc_html( $c[0] ); ?></option><?php endforeach; ?></select></div>
		<div class="nlf-field"><label for="nlf-c-title">הכותרת, במשפט אחד</label><input id="nlf-c-title" name="title" type="text" maxlength="140" autocomplete="off" required>
			<div class="nlf-similar" data-nlf-similar hidden><span>כבר שאלו משהו דומה:</span><ul></ul></div></div>
		<div class="nlf-field"><label for="nlf-c-body">פרטים (לא חובה)</label><textarea id="nlf-c-body" name="body" rows="4" maxlength="4000" placeholder="עיר, סוג הנכס, מה כבר בדקתם"></textarea></div>
		<div class="nlf-field"><label for="nlf-c-city">עיר (לא חובה)</label><input id="nlf-c-city" name="city" type="text" maxlength="40" autocomplete="address-level2"></div>
		<div class="nlf-tobox" data-nlf-tobox hidden><span></span><button type="button" class="nlf-link" data-nlf-to-all>לכל הפורום במקום</button></div>
		<input type="hidden" name="pro_id" value="">
		<?php echo nlf_trap(); // phpcs:ignore ?>
		<button type="submit" class="nlf-btn nlf-btn-hot nlf-btn-big">פרסום ההודעה</button>
		<p class="nlf-sub nlf-center">הודעה ראשונה עולה אחרי בדיקה קצרה. מהשנייה והלאה, מיד.</p>
		<p class="nlf-msg" role="status" aria-live="polite"></p>
	</form>
</dialog>
<dialog class="nlf nlf-sheet" id="nlf-entry" dir="rtl" aria-labelledby="nlf-entry-h">
	<div class="nlf-sheet-h"><button type="button" class="nlf-ico" data-nlf-close aria-label="סגירה"><?php echo nlf_svg( 'close' ); // phpcs:ignore ?></button><h2 class="nlf-h2" id="nlf-entry-h">צעד אחד ואתם בפנים</h2></div>
	<p class="nlf-sub">שם ומייל. בלי סיסמה ובלי טופס הרשמה.</p>
	<form class="nlf-form" data-nlf-step1 novalidate>
		<div class="nlf-grid2">
			<div class="nlf-field"><label for="nlf-e-name">שם</label><input id="nlf-e-name" name="name" type="text" maxlength="40" autocomplete="name" required></div>
			<div class="nlf-field"><label for="nlf-e-mail">מייל</label><input id="nlf-e-mail" name="email" type="email" dir="ltr" autocomplete="email" inputmode="email" required></div>
		</div>
		<div class="nlf-field"><label for="nlf-e-role">אני</label><select id="nlf-e-role" name="role"><?php foreach ( $roles as $k => $l ) : ?><option value="<?php echo esc_attr( $k ); ?>"><?php echo esc_html( $l ); ?></option><?php endforeach; ?></select></div>
		<?php if ( function_exists( 'nadlan_forum_trade_groups' ) ) : // the trade list of inc/pro-forum-trades.php; the key is stored, "other" is free text for review ?>
		<div class="nlf-field" data-nlf-trade hidden><label for="nlf-e-trade">התחום שלי</label><select id="nlf-e-trade" name="trade"><option value="">בחרו תחום</option>
			<?php foreach ( (array) nadlan_forum_trade_groups() as $grp ) : ?><optgroup label="<?php echo esc_attr( $grp['label'] ); ?>"><?php foreach ( (array) $grp['trades'] as $tk => $tr ) : ?><option value="<?php echo esc_attr( $tk ); ?>"><?php echo esc_html( $tr[0] ); ?></option><?php endforeach; ?></optgroup><?php endforeach; ?>
			<option value="other">תחום אחר</option></select></div>
		<div class="nlf-field" data-nlf-trade-other hidden><label for="nlf-e-other">איזה תחום?</label><input id="nlf-e-other" name="trade_other" type="text" maxlength="60" autocomplete="organization-title"></div>
		<?php endif; ?>
		<label class="nlf-check"><input type="checkbox" name="consent" value="1" required><span><?php echo nlf_consent_html(); // phpcs:ignore -- escaped inside ?></span></label>
		<?php echo nlf_trap(); // phpcs:ignore ?>
		<button type="submit" class="nlf-btn nlf-btn-hot nlf-btn-big">שלחו לי קוד</button>
	</form>
	<form class="nlf-form" data-nlf-step2 novalidate hidden>
		<fieldset class="nlf-code"><legend>הקוד שקיבלתם במייל</legend>
			<div class="nlf-digits" dir="ltr"><?php for ( $i = 1; $i <= 6; $i++ ) : ?><input type="text" inputmode="numeric" pattern="[0-9]*" maxlength="1" autocomplete="<?php echo 1 === $i ? 'one-time-code' : 'off'; ?>" aria-label="<?php echo esc_attr( 'ספרה ' . $i ); ?>"><?php endfor; ?></div>
		</fieldset>
		<p class="nlf-sub">לא הגיע? <button type="button" class="nlf-link" data-nlf-again disabled>שליחה שוב</button> <span data-nlf-count></span></p>
		<?php echo nlf_trap(); // phpcs:ignore ?>
		<button type="submit" class="nlf-btn nlf-btn-hot nlf-btn-big">כניסה</button>
	</form>
	<p class="nlf-msg" role="status" aria-live="polite"></p>
</dialog>
<dialog class="nlf nlf-sheet nlf-sheet-sm" id="nlf-report" dir="rtl" aria-labelledby="nlf-report-h">
	<form class="nlf-form" data-nlf-reportform novalidate>
		<div class="nlf-sheet-h"><button type="button" class="nlf-ico" data-nlf-close aria-label="סגירה"><?php echo nlf_svg( 'close' ); // phpcs:ignore ?></button><h2 class="nlf-h2" id="nlf-report-h">דיווח על הודעה</h2></div>
		<fieldset class="nlf-radios nlf-radios-col"><legend>מה הבעיה?</legend><?php foreach ( nlf_report_reasons() as $k => $l ) : ?><label><input type="radio" name="reason" value="<?php echo esc_attr( $k ); ?>"> <?php echo esc_html( $l ); ?></label><?php endforeach; ?></fieldset>
		<?php echo nlf_trap(); // phpcs:ignore ?>
		<button type="submit" class="nlf-btn nlf-btn-fill nlf-btn-big">שליחת הדיווח</button>
		<p class="nlf-msg" role="status" aria-live="polite"></p>
	</form>
</dialog>
<dialog class="nlf nlf-sheet nlf-sheet-sm" id="nlf-request" dir="rtl" aria-labelledby="nlf-request-h">
	<form class="nlf-form" data-nlf-requestform novalidate>
		<div class="nlf-sheet-h"><button type="button" class="nlf-ico" data-nlf-close aria-label="סגירה"><?php echo nlf_svg( 'close' ); // phpcs:ignore ?></button><h2 class="nlf-h2" id="nlf-request-h">בקשה על הכרטיס</h2></div>
		<p class="nlf-note" data-nlf-mismatch hidden>לא מצאנו את המייל הזה בכרטיס. שלחו בקשה ונטפל בה היום.</p>
		<fieldset class="nlf-radios nlf-radios-col"><legend>מה תרצו?</legend>
			<label><input type="radio" name="kind" value="ownership" checked> הכרטיס שלי, אני רוצה לנהל אותו</label>
			<label><input type="radio" name="kind" value="removal"> הסרת הכרטיס מהאתר</label>
		</fieldset>
		<div class="nlf-field"><label for="nlf-r-body">כמה מילים עליכם ועל הבקשה</label><textarea id="nlf-r-body" name="body" rows="3" maxlength="1000"></textarea></div>
		<div class="nlf-field"><label for="nlf-r-phone">טלפון לחזרה (לא חובה)</label><input id="nlf-r-phone" name="phone" type="tel" dir="ltr" autocomplete="tel" maxlength="20"></div>
		<input type="hidden" name="pro_id" value="">
		<?php echo nlf_trap(); // phpcs:ignore ?>
		<button type="submit" class="nlf-btn nlf-btn-fill nlf-btn-big">שליחה</button>
		<p class="nlf-msg" role="status" aria-live="polite"></p>
	</form>
</dialog>
	<?php
}, 5 ); // 1.72.669: before the footer scripts (priority 20), so forum.js finds the sheets; at 20 they came after it and no button opened (live check 12.11)

/* ---------------------------------------------------------------- the page shell on this block theme (12.11.2026, live check) */

/**
 * This block theme has no header.php: get_header() alone prints WordPress's theme-compat header (a second h1 with the
 * site name and no site menu; seen live on 1.72.667). The forum pages open and close exactly as the professionals'
 * directory does (inc/directory.php): the compat header demoted and hidden, then the theme's own header and footer
 * template parts, which carry the site menu.
 */
function nlf_shell_open() {
	if ( function_exists( 'nadlan_dir_header_single_h1' ) ) { nadlan_dir_header_single_h1(); } else { get_header(); }
	if ( function_exists( 'block_template_part' ) ) { block_template_part( 'header' ); }
}
function nlf_shell_close() {
	if ( function_exists( 'block_template_part' ) ) { block_template_part( 'footer' ); }
	get_footer();
}

/* ---------------------------------------------------------------- rendering the forum pages inside the theme */

add_action( 'template_redirect', function () {
	$v = nlf_rendering();
	if ( '' === $v ) { return; }
	$html = 'topic' === $v ? nlf_render_topic( $GLOBALS['nlf_topic'] ) : nlf_render_home();
	nlf_shell_open();
	echo $html; // phpcs:ignore -- built from escaped parts
	nlf_shell_close();
	exit;
}, 1 );

/* ---------------------------------------------------------------- one-click mail links (?nlf_act=), gate or not */

add_action( 'template_redirect', function () {
	if ( ! isset( $_GET['nlf_act'] ) || is_admin() ) { return; } // phpcs:ignore
	$tok  = sanitize_text_field( wp_unslash( $_GET['nlf_act'] ) ); // phpcs:ignore -- signed token, checked below
	$link = nlf_link_read( $tok, time(), nlf_key() );
	// while the forum is hidden a made-up ?nlf_act= shows the normal page: no forum text, style or script (review 12.11.2026)
	if ( ! nlf_act_takeover( null !== $link, nlf_gate_open() ) ) { return; }
	$GLOBALS['nlf_act_page'] = true;
	nlf_nocache();
	nlf_install();
	$h    = 'הקישור לא תקף או שפג תוקפו.';
	$body = '';
	if ( $link ) {
		list( $act, $id ) = $link;
		global $wpdb;
		if ( 'unf' === $act && preg_match( '/^m(\d+)t(\d+)$/', $id, $mm ) ) {
			nlf_follow( (int) $mm[1], (int) $mm[2], false );
			$h = 'לא תקבלו עוד הודעות על הדיון הזה.';
		} elseif ( 'opt' === $act && preg_match( '/^p(\d+)$/', $id, $mm ) && 'nadlan_professional' === get_post_type( (int) $mm[1] ) ) {
			update_post_meta( (int) $mm[1], 'nl_forum_optout', '1' );
			$h = 'לא תקבלו עוד הודעות מהפורום.';
		} elseif ( in_array( $act, array( 'ok', 'no' ), true ) && preg_match( '/^([tr])(\d+)$/', $id, $mm ) ) {
			$type = 't' === $mm[1] ? 'topic' : 'reply';
			$row  = 'topic' === $type ? nlf_topic( (int) $mm[2] ) : nlf_reply( (int) $mm[2] );
			if ( ! $row ) {
				$h = 'ההודעה לא נמצאה.';
			} elseif ( 'pending' !== $row['status'] ) {
				$h = 'ההודעה כבר טופלה.';
			} elseif ( 'POST' === ( $_SERVER['REQUEST_METHOD'] ?? '' ) && isset( $_POST['nlf_confirm'] ) ) { // phpcs:ignore -- the signed token is the authority
				nlf_moderate( $type, (int) $mm[2], 'ok' === $act ? 'live' : 'removed' );
				$h = 'ok' === $act ? 'ההודעה אושרה ועלתה לפורום.' : 'ההודעה נדחתה.';
			} else {
				// a confirmation button: mail scanners open links by themselves, so one press on the page does the action
				$h    = 'ok' === $act ? 'אישור ההודעה' : 'דחיית ההודעה';
				$body = '<blockquote class="nlf-quote">' . nlf_body_html( nlf_excerpt( ( 'topic' === $type ? $row['title'] . "\n" : '' ) . $row['body'], 600 ) ) . '</blockquote>'
					. '<form method="post" action="' . esc_url( add_query_arg( 'nlf_act', $tok, home_url( '/' ) ) ) . '"><input type="hidden" name="nlf_confirm" value="1">'
					. '<button type="submit" class="nlf-btn ' . ( 'ok' === $act ? 'nlf-btn-fill' : 'nlf-btn-danger' ) . ' nlf-btn-big">' . ( 'ok' === $act ? 'אישור ההודעה' : 'דחיית ההודעה' ) . '</button></form>';
			}
		}
	}
	status_header( 200 );
	nlf_shell_open();
	echo '<div class="nlf nlf-page nlf-act" dir="rtl"><h1 class="nlf-h1">' . esc_html( $h ) . '</h1>' . $body . '</div>'; // phpcs:ignore -- escaped parts
	nlf_shell_close();
	exit;
}, -100 );

/* ---------------------------------------------------------------- the whole directory, connected (owner 12.11.2026) */

/**
 * The forum home shows the directory it lives next to: how many professionals the site lists from the public registers,
 * how many of them joined the forum (real counts), a link to every trade's list, and the way in for a professional.
 * People in the registers are never shown as members: the band says plainly that they did not necessarily join.
 */
function nlf_directory_band() {
	global $wpdb;
	$cnt = wp_count_posts( 'nadlan_professional' );
	$all = isset( $cnt->publish ) ? (int) $cnt->publish : 0;
	$joined = (int) $wpdb->get_var( 'SELECT COUNT(*) FROM ' . nlf_t( 'members' ) . " WHERE status = 'ok' AND role_label = 'pro'" );
	$links = '';
	foreach ( ( function_exists( 'nadlan_dir_professions_all' ) ? (array) nadlan_dir_professions_all() : array() ) as $key => $p ) {
		if ( empty( $p['label'] ) ) { continue; }
		$links .= '<a class="nlf-chip nlf-tag-plain" href="' . esc_url( home_url( '/professionals/?profession=' . rawurlencode( (string) $key ) ) ) . '">' . esc_html( $p['label'] ) . '</a>';
	}
	$line = $all > 0 ? number_format( $all ) . ' בעלי מקצוע במאגר, מהפנקסים הרשמיים' : 'המאגר של בעלי המקצוע';
	$line .= $joined > 0 ? ' · ' . ( 1 === $joined ? 'בעל מקצוע אחד הצטרף לפורום' : number_format( $joined ) . ' הצטרפו לפורום' ) : ' · היו הראשונים להצטרף לפורום';
	return '<section class="nlf-dir" aria-labelledby="nlf-dir-h">'
		. '<h2 class="nlf-dir-h" id="nlf-dir-h">כל בעלי המקצוע של נדל"ן במקום אחד</h2>'
		. '<p class="nlf-dir-line">' . esc_html( $line ) . '</p>'
		. '<p class="nlf-dir-note">בעלי המקצוע במאגר לא הצטרפו בהכרח לפורום. פרסמו בקשה, ומי שהצטרף יענה לכם ישירות.</p>'
		. ( $links ? '<div class="nlf-dir-links">' . $links . '</div>' : '' )
		. '<div class="nlf-dir-cta"><a class="nlf-btn nlf-btn-fill" href="' . esc_url( home_url( '/forum/?join=1' ) ) . '">הצטרפות לבעלי מקצוע</a>'
		. '<a class="nlf-btn nlf-btn-line" href="' . esc_url( home_url( '/professionals/' ) ) . '">לכל המאגר</a></div>'
		. '</section>';
}
