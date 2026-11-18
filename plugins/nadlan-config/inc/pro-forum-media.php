<?php
/**
 * nad-lan professionals' forum: images, plans (PDF) and files in posts, the full-screen gallery, "mark a point on a photo and
 * ask", and every member's profile picture (18.11.2026, Claude Design board 21 "תמונות, תוכניות וקבצים בהודעות, ותמונה לכל
 * חבר", forum-design/project/Media.dc.html, parts א to ה).
 *
 * Loaded by ONE line at the end of inc/pro-forum.php, after the reputation module:
 *   if ( file_exists( __DIR__ . '/pro-forum-media.php' ) ) { require_once __DIR__ . '/pro-forum-media.php'; }
 * Tables (own version option nadlan_forum_media_db, the house names): {prefix}nadlan_forum_media, {prefix}nadlan_forum_pins.
 * Files: wp-content/uploads/nlf-media/YYYY/MM/<32 hex>.jpg (re-encoded on the server, at most 2048 px, no metadata) with
 *   <hex>-480.jpg (the thumb); a PDF as <hex>.pdf, kept as it came, plus <hex>-p.jpg (its first page) and <hex>-480.jpg when the
 *   host's image editor can read a PDF (Imagick with Ghostscript); a profile picture is one 256 x 256 <hex>.jpg.
 * Hooks this module fills (added to the forum's own files as one-line hooks marked "HOOK (media module ...)"):
 *   nlf_post_check (filter, topic and reply routes, before the insert)  the attached files and the point are checked
 *   nlf_post_created (action, after the insert)  the files are attached in their order with their captions; the point is stored
 *   nlf_moderated (action, nlf_moderate)  the files follow the post: live = shown, hidden = not shown, removed = files deleted
 *   nlf_topic_after_body (5)  the gallery and the plans of the opening message, and the points of the whole discussion as JSON
 *   nlf_reply_after_body  the gallery of an answer, and the small crop of the point it asks about
 *   nlf_avatar_html  the member's picture instead of the initials, wherever nlf_avatar() prints
 *   nlf_jsonld  the first image of the discussion as `image` of DiscussionForumPosting / the Question of a QAPage
 *   nlf_member_bar_extra (30), nlf_owner_box_extra (30)  "תמונת פרופיל" in the member's own bar and box
 * The composer is added by assets/proforum/media.js into the forum's two forms; forum.js reads form.nlfExtra() on submit.
 * REST (nadlan/v1/forum/..., hidden from the index, errors are HTTP 400): POST media (one file), DELETE media/<id> (an own file
 *   not yet attached), DELETE media/avatar (the picture off). A logged-in member with the header nonce only; per member 80
 *   files and 400MB a day. The kind is read from the file's first bytes, never from its name.
 * No redirects, no robots changes, no long dashes in this file.
 */

if ( ! defined( 'ABSPATH' ) && ! defined( 'NLFMD_PURE_ONLY' ) ) { exit; }
if ( defined( 'NLFMD_LOADED' ) ) { return; }
define( 'NLFMD_LOADED', true );
define( 'NLFMD_DB', '1' );
define( 'NLFMD_DIR', 'nlf-media' );

/* =========================================================================================================
 * 1. Pure functions (no WordPress). tests-local/pro-forum-media-test.php loads only this part (NLFMD_PURE_ONLY), after the
 *    forum's own pure part.
 * ======================================================================================================= */

/** every number of this layer, in one place (the composer line and the page script read them from here) */
function nlfmd_limits() {
	return array(
		'topic' => 20, 'reply' => 10,       // files in one message / in one answer
		'img_mb' => 10, 'pdf_mb' => 25,     // a picture before the shrink in the browser / a plan
		'day_n' => 80, 'day_mb' => 400,     // per member per day
		'long' => 2048, 'thumb' => 480,     // the server's long side and the thumb
		'client_long' => 2560,              // the browser's long side before the upload
		'avatar' => 256, 'caption' => 180,
		'pixels' => 40000000,               // a larger picture is refused before it is decoded on the server
	);
}

function nlfmd_mb( $n ) { return (int) $n * 1048576; }

/** the line under the composer, word for word as board 21 part א (an answer says 10 and "בתגובה") */
function nlfmd_limits_text( $ctx ) {
	$l = nlfmd_limits();
	$r = 'reply' === $ctx;
	return 'עד ' . ( $r ? $l['reply'] : $l['topic'] ) . ' תמונות ב' . ( $r ? 'תגובה' : 'הודעה' ) . ', עד ' . $l['img_mb'] . 'MB כל אחת (מוקטנות אוטומטית). תוכנית או מסמך PDF עד ' . $l['pdf_mb'] . 'MB. תמונה מהאייפון מומרת לבד.';
}

/** the type by the first bytes (magic bytes), never by the name: jpeg | png | webp | gif | pdf | heic | '' */
function nlfmd_sniff( $head ) {
	$h = (string) $head;
	if ( 0 === strncmp( $h, "\xFF\xD8\xFF", 3 ) ) { return 'jpeg'; }
	if ( 0 === strncmp( $h, "\x89PNG\r\n\x1A\n", 8 ) ) { return 'png'; }
	if ( strlen( $h ) >= 12 && 'RIFF' === substr( $h, 0, 4 ) && 'WEBP' === substr( $h, 8, 4 ) ) { return 'webp'; }
	if ( 0 === strncmp( $h, 'GIF87a', 6 ) || 0 === strncmp( $h, 'GIF89a', 6 ) ) { return 'gif'; }
	if ( 0 === strncmp( $h, '%PDF-', 5 ) ) { return 'pdf'; }
	if ( strlen( $h ) >= 12 && 'ftyp' === substr( $h, 4, 4 ) && in_array( substr( $h, 8, 4 ), array( 'heic', 'heix', 'hevc', 'mif1', 'msf1' ), true ) ) { return 'heic'; }
	return '';
}

/** image | pdf | '' for a sniffed type */
function nlfmd_kind_of( $type ) {
	if ( in_array( (string) $type, array( 'jpeg', 'png', 'webp', 'gif' ), true ) ) { return 'image'; }
	return 'pdf' === (string) $type ? 'pdf' : '';
}

/** '' when this upload may go on, else the Hebrew message. $want: post (a picture or a plan) | avatar */
function nlfmd_upload_error( $want, $type, $bytes ) {
	$l    = nlfmd_limits();
	$kind = nlfmd_kind_of( $type );
	if ( (int) $bytes < 1 ) { return 'הקובץ ריק. נסו קובץ אחר.'; }
	if ( 'heic' === $type ) { return 'את התמונה הזאת הדפדפן לא המיר. שמרו אותה כ-JPG ונסו שוב.'; }
	if ( '' === $kind ) { return 'אפשר לצרף רק תמונה (JPG, PNG, WebP) או קובץ PDF.'; }
	if ( 'avatar' === $want && 'image' !== $kind ) { return 'לתמונת פרופיל צריך תמונה.'; }
	if ( 'image' === $kind && (int) $bytes > nlfmd_mb( $l['img_mb'] ) ) { return 'התמונה גדולה מ-' . $l['img_mb'] . 'MB. נסו תמונה קטנה יותר.'; }
	if ( 'pdf' === $kind && (int) $bytes > nlfmd_mb( $l['pdf_mb'] ) ) { return 'הקובץ גדול מ-' . $l['pdf_mb'] . 'MB.'; }
	return '';
}

/** the per-day ceiling of one member: $count files and $bytes already today, $add about to come */
function nlfmd_day_error( $count, $bytes, $add ) {
	$l = nlfmd_limits();
	if ( (int) $count >= $l['day_n'] ) { return 'הגעתם למספר הקבצים המרבי ליום. נסו שוב מחר.'; }
	if ( (int) $bytes + (int) $add > nlfmd_mb( $l['day_mb'] ) ) { return 'הגעתם לנפח הקבצים המרבי ליום. נסו שוב מחר.'; }
	return '';
}

/** files on one post: up to 20 on a discussion, 10 on an answer (pictures and plans together) */
function nlfmd_count_error( $ctx, $n ) {
	$l   = nlfmd_limits();
	$max = 'reply' === $ctx ? $l['reply'] : $l['topic'];
	return (int) $n > $max ? 'אפשר לצרף עד ' . $max . ( 'reply' === $ctx ? ' קבצים לתגובה.' : ' קבצים להודעה.' ) : '';
}

/** the gallery shape of board 21 part ב: one (full width), two (two columns), three (a big one and two small, "+N" on the last) */
function nlfmd_layout( $n ) {
	$n = (int) $n;
	if ( $n < 1 ) { return ''; }
	return 1 === $n ? 'one' : ( 2 === $n ? 'two' : 'three' );
}

/** the number on the "+N" tile: the pictures beyond the three shown */
function nlfmd_more( $n ) { return max( 0, (int) $n - 3 ); }

/** a point on a picture is a fraction of its width and height, always 0..1 (4 decimals); null for anything not a finite number */
function nlfmd_clamp01( $v ) {
	if ( ! is_numeric( $v ) ) { return null; }
	$f = (float) $v;
	if ( is_nan( $f ) ) { return null; }
	return round( max( 0.0, min( 1.0, $f ) ), 4 );
}

/** array( media, x, y ) or null */
function nlfmd_pin_norm( $p ) {
	if ( ! is_array( $p ) ) { return null; }
	$mid = isset( $p['media'] ) ? (int) $p['media'] : 0;
	$x   = isset( $p['x'] ) ? nlfmd_clamp01( $p['x'] ) : null;
	$y   = isset( $p['y'] ) ? nlfmd_clamp01( $p['y'] ) : null;
	if ( $mid <= 0 || null === $x || null === $y ) { return null; }
	return array( 'media' => $mid, 'x' => $x, 'y' => $y );
}

/**
 * The small crop of board 21 around a point, zoomed $k times: array( background-position %, marker position % ) for one axis.
 * The box has the picture's own proportions and background-size $k*100% on both axes, so one formula serves x and y.
 */
function nlfmd_crop( $v, $k = 3 ) {
	$v = nlfmd_clamp01( $v );
	$v = null === $v ? 0.5 : $v;
	$k = max( 1.5, (float) $k );
	$p = max( 0.0, min( 1.0, ( $v * $k - 0.5 ) / ( $k - 1 ) ) );
	return array( round( $p * 100, 2 ), round( ( $v * $k - $p * ( $k - 1 ) ) * 100, 2 ) );
}

/** one caption: plain text on one line, at most 180 characters */
function nlfmd_caption( $s ) {
	$s = function_exists( 'nlf_text_norm' ) ? nlf_text_norm( (string) $s, true ) : trim( (string) $s );
	return mb_substr( $s, 0, nlfmd_limits()['caption'], 'UTF-8' );
}

/** the attached files as sent: a list of array( id, caption ) or of ids; unique positive ids in their order */
function nlfmd_items_norm( $raw ) {
	$out  = array();
	$seen = array();
	if ( ! is_array( $raw ) ) { return $out; }
	foreach ( array_slice( array_values( $raw ), 0, 200 ) as $it ) {
		$id  = is_array( $it ) ? (int) ( $it['id'] ?? 0 ) : (int) $it;
		$cap = is_array( $it ) ? nlfmd_caption( $it['caption'] ?? '' ) : '';
		if ( $id <= 0 || isset( $seen[ $id ] ) ) { continue; }
		$seen[ $id ] = true;
		$out[] = array( 'id' => $id, 'caption' => $cap );
	}
	return $out;
}

/** '' when every attached file may go on this post, else the message. $rows: id => row of the media table */
function nlfmd_attach_error( array $items, array $rows, $member_id ) {
	foreach ( $items as $it ) {
		$r = $rows[ (int) $it['id'] ] ?? null;
		if ( ! $r || (int) $r['member_id'] !== (int) $member_id || ! in_array( (string) $r['kind'], array( 'image', 'pdf' ), true )
			|| 'pending' !== (string) $r['status'] || ! empty( $r['topic_id'] ) || ! empty( $r['reply_id'] ) ) {
			return 'אחד הקבצים כבר לא זמין. הסירו אותו ונסו שוב.';
		}
	}
	return '';
}

/** the stored address of a file under uploads: nlf-media/2026/11/<32 hex><suffix>.<ext> */
function nlfmd_rel( $ym, $hex, $ext, $suffix = '' ) { return NLFMD_DIR . '/' . $ym . '/' . $hex . $suffix . '.' . $ext; }

/** a main file address this module made (the only shape it ever reads, deletes or prints) */
function nlfmd_rel_ok( $rel ) { return (bool) preg_match( '~^nlf-media/\d{4}/\d{2}/[a-f0-9]{32}\.(jpg|pdf)$~', (string) $rel ); }

/** a sibling of a main file: -480 the thumb, -p the first page of a plan; always a .jpg */
function nlfmd_variant( $rel, $suffix ) { return (string) preg_replace( '~\.(jpg|pdf)$~', $suffix . '.jpg', (string) $rel ); }

/** the pages of a PDF when they can be counted cheaply from its bytes; 0 = unknown (the card then shows the size only) */
function nlfmd_pdf_pages( $data ) {
	$d = (string) $data;
	$n = (int) preg_match_all( '~/Type\s*/Page(?![A-Za-z])~', $d );
	if ( $n > 0 ) { return min( $n, 9999 ); }
	if ( preg_match( '~/Type\s*/Pages[^>]{0,200}?/Count\s+(\d{1,5})~', $d, $m ) || preg_match( '~/Count\s+(\d{1,5})[^>]{0,200}?/Type\s*/Pages~', $d, $m ) ) {
		return min( (int) $m[1], 9999 );
	}
	return 0;
}

/** "2.4MB" / "640KB" as on the board */
function nlfmd_size_text( $bytes ) {
	$b = max( 0, (int) $bytes );
	if ( $b < 1048576 ) { return max( 1, (int) round( $b / 1024 ) ) . 'KB'; }
	return rtrim( rtrim( number_format( $b / 1048576, 1, '.', '' ), '0' ), '.' ) . 'MB';
}

/** "PDF · 3 עמודים · 2.4MB" (the pages left out when unknown) */
function nlfmd_pdf_meta( $pages, $bytes ) {
	$p = (int) $pages;
	$parts = array( 'PDF' );
	if ( $p > 0 ) { $parts[] = 1 === $p ? 'עמוד אחד' : $p . ' עמודים'; }
	$parts[] = nlfmd_size_text( $bytes );
	return implode( ' · ', $parts );
}

function nlfmd_alt( $caption ) { $c = trim( (string) $caption ); return '' !== $c ? $c : 'תמונה מהדיון'; }

/**
 * A JPEG without its metadata segments: APP1 to APP15 (EXIF with GPS, XMP, IPTC) and comments go; APP0 (JFIF) and the colour
 * profile (APP2 "ICC_PROFILE") stay, so colours do not shift. '' when the bytes are not a well-formed JPEG head. Run on every
 * JPEG this module writes, whatever image editor the host has.
 */
function nlfmd_jpeg_strip( $bin ) {
	$b   = (string) $bin;
	$len = strlen( $b );
	if ( $len < 4 || "\xFF\xD8" !== substr( $b, 0, 2 ) ) { return ''; }
	$out = "\xFF\xD8";
	$i   = 2;
	while ( $i + 2 <= $len ) {
		if ( "\xFF" !== $b[ $i ] ) { return ''; }
		$mk = ord( $b[ $i + 1 ] );
		if ( 0xFF === $mk ) { $i++; continue; } // a fill byte
		if ( 0xDA === $mk || 0xD9 === $mk ) { return $out . substr( $b, $i ); } // start of scan (or the end): the rest is the picture
		if ( ( $mk >= 0xD0 && $mk <= 0xD7 ) || 0x01 === $mk ) { $out .= substr( $b, $i, 2 ); $i += 2; continue; }
		if ( $i + 4 > $len ) { return ''; }
		$seg = ( ord( $b[ $i + 2 ] ) << 8 ) | ord( $b[ $i + 3 ] );
		if ( $seg < 2 || $i + 2 + $seg > $len ) { return ''; }
		$icc  = 0xE2 === $mk && 'ICC_PROFILE' === substr( $b, $i + 4, 11 );
		$drop = ( $mk >= 0xE1 && $mk <= 0xEF && ! $icc ) || 0xFE === $mk;
		if ( ! $drop ) { $out .= substr( $b, $i, 2 + $seg ); }
		$i += 2 + $seg;
	}
	return '';
}

/** true when a JPEG still carries EXIF, XMP or a comment before its picture data */
function nlfmd_jpeg_has_meta( $bin ) {
	$s = nlfmd_jpeg_strip( $bin );
	return '' !== $s && strlen( $s ) !== strlen( (string) $bin );
}

if ( defined( 'NLFMD_PURE_ONLY' ) ) { return; }

/* =========================================================================================================
 * 2. Tables, files
 * ======================================================================================================= */

function nlfmd_t( $name ) { global $wpdb; return $wpdb->prefix . 'nadlan_forum_' . $name; }

function nlfmd_ready() { return NLFMD_DB === (string) get_option( 'nadlan_forum_media_db' ); }

/** the two tables once per NLFMD_DB (never on every request); a failed attempt waits an hour */
function nlfmd_install() {
	if ( nlfmd_ready() || get_transient( 'nlfmd_install_wait' ) || ! function_exists( 'nlf_db_ready' ) || ! nlf_db_ready() ) { return; }
	global $wpdb;
	require_once ABSPATH . 'wp-admin/includes/upgrade.php';
	$c = $wpdb->get_charset_collate();
	dbDelta( 'CREATE TABLE ' . nlfmd_t( 'media' ) . " (
		id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
		member_id BIGINT UNSIGNED NOT NULL,
		topic_id BIGINT UNSIGNED NULL,
		reply_id BIGINT UNSIGNED NULL,
		kind VARCHAR(8) NOT NULL DEFAULT 'image',
		path VARCHAR(120) NOT NULL DEFAULT '',
		w INT UNSIGNED NOT NULL DEFAULT 0,
		h INT UNSIGNED NOT NULL DEFAULT 0,
		bytes BIGINT UNSIGNED NOT NULL DEFAULT 0,
		sha256 CHAR(64) NOT NULL DEFAULT '',
		caption VARCHAR(200) NOT NULL DEFAULT '',
		sort SMALLINT UNSIGNED NOT NULL DEFAULT 0,
		pages SMALLINT UNSIGNED NOT NULL DEFAULT 0,
		preview TINYINT(1) NOT NULL DEFAULT 0,
		status VARCHAR(8) NOT NULL DEFAULT 'pending',
		created_at DATETIME NOT NULL,
		PRIMARY KEY  (id),
		KEY topic_id (topic_id),
		KEY reply_id (reply_id),
		KEY member_id (member_id,created_at),
		KEY kind_status (kind,status)
	) $c;" );
	dbDelta( 'CREATE TABLE ' . nlfmd_t( 'pins' ) . " (
		id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
		media_id BIGINT UNSIGNED NOT NULL,
		reply_id BIGINT UNSIGNED NOT NULL,
		x DECIMAL(5,4) NOT NULL DEFAULT 0.5,
		y DECIMAL(5,4) NOT NULL DEFAULT 0.5,
		created_at DATETIME NOT NULL,
		PRIMARY KEY  (id),
		KEY media_id (media_id),
		KEY reply_id (reply_id)
	) $c;" );
	foreach ( array( 'media', 'pins' ) as $name ) {
		if ( nlfmd_t( $name ) !== (string) $wpdb->get_var( $wpdb->prepare( 'SHOW TABLES LIKE %s', $wpdb->esc_like( nlfmd_t( $name ) ) ) ) ) {
			set_transient( 'nlfmd_install_wait', 1, HOUR_IN_SECONDS );
			return;
		}
	}
	update_option( 'nadlan_forum_media_db', NLFMD_DB, true );
}
add_action( 'admin_init', 'nlfmd_install', 20 );

/** the uploads folder and address (wp_upload_dir without creating a month folder of its own) */
function nlfmd_base() {
	static $b = null;
	if ( null === $b ) {
		$u = wp_upload_dir( null, false );
		$b = array( 'dir' => trailingslashit( (string) $u['basedir'] ), 'url' => trailingslashit( (string) $u['baseurl'] ) );
	}
	return $b;
}

function nlfmd_abs( $rel ) { return nlfmd_base()['dir'] . $rel; }

function nlfmd_url( $rel ) { return nlfmd_base()['url'] . $rel; }

/** a new main address in this month's folder; the folder, and the guard files at the top folder, are made on the way */
function nlfmd_new_rel( $ext ) {
	$rel = nlfmd_rel( gmdate( 'Y/m' ), bin2hex( random_bytes( 16 ) ), $ext );
	$top = nlfmd_abs( NLFMD_DIR );
	if ( ! is_dir( dirname( nlfmd_abs( $rel ) ) ) && ! wp_mkdir_p( dirname( nlfmd_abs( $rel ) ) ) ) { return ''; }
	if ( ! file_exists( $top . '/index.html' ) ) { @file_put_contents( $top . '/index.html', '' ); } // phpcs:ignore -- no folder listing
	if ( ! file_exists( $top . '/.htaccess' ) ) { // the file names are always <hex>.jpg / .pdf; nothing here ever runs as code
		@file_put_contents( $top . '/.htaccess', "Options -Indexes\n<FilesMatch \"\\.(php|phtml|phar|pht|shtml|cgi|pl|py)$\">\nRequire all denied\n</FilesMatch>\n" ); // phpcs:ignore
	}
	return $rel;
}

/** rewrite a JPEG on disk without its metadata (see nlfmd_jpeg_strip) */
function nlfmd_strip_file( $abs ) {
	$bin = (string) @file_get_contents( $abs ); // phpcs:ignore
	$out = nlfmd_jpeg_strip( $bin );
	if ( '' !== $out && strlen( $out ) !== strlen( $bin ) ) { @file_put_contents( $abs, $out ); } // phpcs:ignore
}

/** delete the files of a row (main, thumb, first page); only addresses this module made */
function nlfmd_unlink_row( $row ) {
	$rel = (string) ( $row['path'] ?? '' );
	if ( ! nlfmd_rel_ok( $rel ) ) { return; }
	foreach ( array( $rel, nlfmd_variant( $rel, '-480' ), nlfmd_variant( $rel, '-p' ) ) as $r ) {
		$a = nlfmd_abs( $r );
		if ( is_file( $a ) ) { @unlink( $a ); } // phpcs:ignore
	}
}

/** rows go: files deleted, status gone (the row stays, so the day's count cannot be reset by deleting), their points removed */
function nlfmd_gone_rows( array $rows ) {
	if ( ! $rows ) { return 0; }
	global $wpdb;
	$ids = array();
	foreach ( $rows as $r ) { nlfmd_unlink_row( $r ); $ids[] = (int) $r['id']; }
	$in = implode( ',', array_map( 'intval', $ids ) );
	$wpdb->query( 'UPDATE ' . nlfmd_t( 'media' ) . " SET status = 'gone' WHERE id IN ($in)" ); // phpcs:ignore -- integers only
	$wpdb->query( 'DELETE FROM ' . nlfmd_t( 'pins' ) . " WHERE media_id IN ($in)" ); // phpcs:ignore -- integers only
	return count( $ids );
}

/** the stored picture: re-encoded as JPEG (2048 long side, a 256 square for a profile picture), a 480 thumb, no metadata */
function nlfmd_store_image( $tmp, $avatar ) {
	$l  = nlfmd_limits();
	$sz = @getimagesize( $tmp ); // phpcs:ignore
	if ( ! $sz || (int) $sz[0] < 1 || (int) $sz[1] < 1 ) { return 'לא הצלחנו לקרוא את התמונה. נסו תמונה אחרת.'; }
	if ( (int) $sz[0] * (int) $sz[1] > $l['pixels'] ) { return 'התמונה גדולה מדי. נסו תמונה קטנה יותר.'; }
	$ed = wp_get_image_editor( $tmp );
	if ( is_wp_error( $ed ) ) { return 'לא הצלחנו לעבד את התמונה. נסו תמונה אחרת.'; }
	try {
		if ( $avatar ) { $ed->resize( $l['avatar'], $l['avatar'], true ); }
		elseif ( max( (int) $sz[0], (int) $sz[1] ) > $l['long'] ) { $ed->resize( $l['long'], $l['long'], false ); }
		$ed->set_quality( 82 );
		$rel = nlfmd_new_rel( 'jpg' );
		if ( '' === $rel ) { return 'לא הצלחנו לשמור את התמונה. נסו שוב.'; }
		$abs = nlfmd_abs( $rel );
		$s   = $ed->save( $abs, 'image/jpeg' );
	} catch ( Throwable $e ) {
		return 'לא הצלחנו לעבד את התמונה. נסו תמונה אחרת.';
	}
	if ( is_wp_error( $s ) || ! is_file( $abs ) ) { return 'לא הצלחנו לשמור את התמונה. נסו שוב.'; }
	nlfmd_strip_file( $abs );
	$w = (int) $s['width'];
	$h = (int) $s['height'];
	if ( ! $avatar ) { nlfmd_make_thumb( $abs, nlfmd_abs( nlfmd_variant( $rel, '-480' ) ), $w, $h ); }
	return array( 'path' => $rel, 'w' => $w, 'h' => $h, 'bytes' => (int) filesize( $abs ), 'sha' => (string) hash_file( 'sha256', $abs ), 'pages' => 0, 'preview' => 0 );
}

/** the 480 thumb of a stored JPEG; a copy of it when the editor fails, so the address always answers */
function nlfmd_make_thumb( $from, $to, $w, $h ) {
	$l  = nlfmd_limits();
	$ok = false;
	$te = wp_get_image_editor( $from );
	if ( ! is_wp_error( $te ) ) {
		try {
			if ( max( (int) $w, (int) $h ) > $l['thumb'] ) { $te->resize( $l['thumb'], $l['thumb'], false ); }
			$te->set_quality( 78 );
			$ok = ! is_wp_error( $te->save( $to, 'image/jpeg' ) ) && is_file( $to );
		} catch ( Throwable $e ) { $ok = false; }
	}
	if ( ! $ok ) { @copy( $from, $to ); } // phpcs:ignore
	if ( is_file( $to ) ) { nlfmd_strip_file( $to ); }
}

/** a plan: stored as it came (the %PDF- head was checked), its pages counted, its first page drawn when the host can */
function nlfmd_store_pdf( $tmp ) {
	$rel = nlfmd_new_rel( 'pdf' );
	if ( '' === $rel ) { return 'לא הצלחנו לשמור את הקובץ. נסו שוב.'; }
	$abs = nlfmd_abs( $rel );
	if ( ! @move_uploaded_file( $tmp, $abs ) ) { return 'לא הצלחנו לשמור את הקובץ. נסו שוב.'; } // phpcs:ignore
	@chmod( $abs, 0644 ); // phpcs:ignore
	$pages = nlfmd_pdf_pages( (string) @file_get_contents( $abs ) ); // phpcs:ignore
	$prev  = 0; $w = 0; $h = 0;
	$ed    = wp_get_image_editor( $abs, array( 'mime_type' => 'application/pdf' ) ); // Imagick + Ghostscript reads page 1; GD cannot (then no first page)
	if ( ! is_wp_error( $ed ) ) {
		try {
			$ed->resize( nlfmd_limits()['long'], nlfmd_limits()['long'], false );
			$ed->set_quality( 82 );
			$pp = nlfmd_abs( nlfmd_variant( $rel, '-p' ) );
			$s  = $ed->save( $pp, 'image/jpeg' );
			if ( ! is_wp_error( $s ) && is_file( $pp ) ) {
				nlfmd_strip_file( $pp );
				$prev = 1; $w = (int) $s['width']; $h = (int) $s['height'];
				nlfmd_make_thumb( $pp, nlfmd_abs( nlfmd_variant( $rel, '-480' ) ), $w, $h );
			}
		} catch ( Throwable $e ) { $prev = 0; }
	}
	return array( 'path' => $rel, 'w' => $w, 'h' => $h, 'bytes' => (int) filesize( $abs ), 'sha' => (string) hash_file( 'sha256', $abs ), 'pages' => $pages, 'preview' => $prev );
}

/** what the page script gets back for one file (addresses only, nothing private) */
function nlfmd_public( array $r ) {
	$rel = (string) $r['path'];
	$o   = array( 'id' => (int) $r['id'], 'kind' => (string) $r['kind'], 'w' => (int) $r['w'], 'h' => (int) $r['h'], 'bytes' => (int) $r['bytes'], 'url' => nlfmd_url( $rel ) );
	if ( 'image' === $r['kind'] ) { $o['thumb'] = nlfmd_url( nlfmd_variant( $rel, '-480' ) ); }
	if ( 'pdf' === $r['kind'] ) {
		$o['pages'] = (int) $r['pages'];
		$o['meta']  = nlfmd_pdf_meta( (int) $r['pages'], (int) $r['bytes'] );
		if ( ! empty( $r['preview'] ) ) { $o['page'] = nlfmd_url( nlfmd_variant( $rel, '-p' ) ); $o['thumb'] = nlfmd_url( nlfmd_variant( $rel, '-480' ) ); }
	}
	return $o;
}

/** rows by id (one query) */
function nlfmd_rows( array $ids ) {
	$ids = array_values( array_unique( array_filter( array_map( 'intval', $ids ) ) ) );
	if ( ! $ids ) { return array(); }
	global $wpdb;
	$out = array();
	foreach ( (array) $wpdb->get_results( $wpdb->prepare( 'SELECT * FROM ' . nlfmd_t( 'media' ) . ' WHERE id IN (' . implode( ',', array_fill( 0, count( $ids ), '%d' ) ) . ')', $ids ), ARRAY_A ) as $r ) {
		$out[ (int) $r['id'] ] = $r;
	}
	return $out;
}

/* =========================================================================================================
 * 3. REST: nadlan/v1/forum/media
 * ======================================================================================================= */

/** a logged-in member of an open forum with the page's nonce; the member row or a WP_Error 400 */
function nlfmd_member( WP_REST_Request $q ) {
	if ( ! function_exists( 'nlf_gate_open' ) || ! nlf_gate_open() ) { return nlf_err( 'הדף לא נמצא.', 'nlf_closed' ); }
	nlf_install();
	nlfmd_install();
	if ( ! nlfmd_ready() ) { return nlf_err( 'צירוף קבצים לא זמין כרגע. נסו שוב בעוד רגע.' ); }
	$m = nlf_me();
	if ( ! $m ) { return nlf_err( 'כדי לצרף קבצים צריך להיכנס. זה צעד אחד.', 'nlf_need_entry' ); }
	if ( ! hash_equals( nlf_nonce_for( $m ), (string) $q->get_header( 'x_nlf_nonce' ) ) ) { return nlf_err( 'הדף ישן. רעננו אותו ונסו שוב.', 'nlf_nonce' ); }
	if ( 'ok' !== (string) $m['status'] ) { return nlf_err( 'החשבון הזה לא יכול לכתוב בפורום כרגע.', 'nlf_blocked' ); }
	if ( ! nlf_rl( 'md_ip', 300, DAY_IN_SECONDS ) ) { return nlf_err( 'נסו שוב מאוחר יותר.' ); }
	return $m;
}

function nlfmd_rest_upload( WP_REST_Request $q ) {
	$m = nlfmd_member( $q );
	if ( is_wp_error( $m ) ) { return $m; }
	$want  = 'avatar' === (string) $q->get_param( 'kind' ) ? 'avatar' : 'post';
	$files = $q->get_file_params();
	$f     = isset( $files['file'] ) && is_array( $files['file'] ) ? $files['file'] : null;
	if ( ! $f || ! empty( $f['error'] ) || empty( $f['tmp_name'] ) || ! is_uploaded_file( $f['tmp_name'] ) ) { return nlf_err( 'הקובץ לא הגיע. נסו שוב.' ); }
	$bytes = (int) @filesize( $f['tmp_name'] ); // phpcs:ignore
	$type  = nlfmd_sniff( (string) @file_get_contents( $f['tmp_name'], false, null, 0, 16 ) ); // phpcs:ignore
	$e     = nlfmd_upload_error( $want, $type, $bytes );
	if ( '' !== $e ) { return nlf_err( $e ); }
	global $wpdb;
	$mt  = nlfmd_t( 'media' );
	$day = $wpdb->get_row( $wpdb->prepare( "SELECT COUNT(*) AS n, COALESCE(SUM(bytes),0) AS b FROM $mt WHERE member_id = %d AND created_at >= %s", (int) $m['id'], gmdate( 'Y-m-d H:i:s', time() - DAY_IN_SECONDS ) ), ARRAY_A );
	$e   = nlfmd_day_error( (int) ( $day['n'] ?? 0 ), (int) ( $day['b'] ?? 0 ), $bytes );
	if ( '' !== $e ) { return nlf_err( $e ); }
	$kind = 'avatar' === $want ? 'avatar' : nlfmd_kind_of( $type );
	$s    = 'pdf' === $kind ? nlfmd_store_pdf( $f['tmp_name'] ) : nlfmd_store_image( $f['tmp_name'], 'avatar' === $kind );
	if ( is_string( $s ) ) { return nlf_err( $s ); }
	$row = array( 'member_id' => (int) $m['id'], 'topic_id' => null, 'reply_id' => null, 'kind' => $kind, 'path' => $s['path'], 'w' => $s['w'], 'h' => $s['h'],
		'bytes' => $s['bytes'], 'sha256' => $s['sha'], 'caption' => '', 'sort' => 0, 'pages' => (int) $s['pages'], 'preview' => (int) $s['preview'],
		'status' => 'avatar' === $kind ? 'ok' : 'pending', 'created_at' => nlf_now_sql() );
	$wpdb->insert( $mt, $row );
	$id = (int) $wpdb->insert_id;
	if ( $id <= 0 ) { nlfmd_unlink_row( $row ); return nlf_err( 'משהו השתבש. נסו שוב.' ); }
	// uploads are NOT counted in the forum's 20-writes-an-hour ceiling (20 pictures would block the post itself); they have their own
	if ( 'avatar' === $kind ) { // the newest picture wins; the older ones go with their files
		nlfmd_gone_rows( (array) $wpdb->get_results( $wpdb->prepare( "SELECT * FROM $mt WHERE member_id = %d AND kind = 'avatar' AND status <> 'gone' AND id <> %d", (int) $m['id'], $id ), ARRAY_A ) );
	}
	return nlf_ok( array( 'media' => nlfmd_public( $row + array( 'id' => $id ) ), 'message' => 'avatar' === $kind ? 'התמונה נשמרה.' : '' ) );
}

add_action( 'rest_api_init', function () {
	$reg = function ( $path, $method, $cb ) {
		register_rest_route( 'nadlan/v1', '/forum/' . $path, array( 'methods' => $method, 'permission_callback' => '__return_true', 'callback' => $cb, 'show_in_index' => false ) );
	};
	$reg( 'media', 'POST', 'nlfmd_rest_upload' );

	// a file of mine that is not on any post yet (the × in the composer); the page sends POST + X-HTTP-Method-Override: DELETE
	$reg( 'media/(?P<id>\d+)', 'DELETE', function ( WP_REST_Request $q ) {
		$m = nlfmd_member( $q );
		if ( is_wp_error( $m ) ) { return $m; }
		$rows = nlfmd_rows( array( (int) $q['id'] ) );
		$r    = $rows[ (int) $q['id'] ] ?? null;
		if ( ! $r || (int) $r['member_id'] !== (int) $m['id'] || 'avatar' === $r['kind'] || 'gone' === $r['status'] || ! empty( $r['topic_id'] ) || ! empty( $r['reply_id'] ) ) {
			return nlf_err( 'הקובץ לא נמצא.' );
		}
		nlfmd_gone_rows( array( $r ) );
		return nlf_ok( array( 'gone' => (int) $r['id'] ) );
	} );

	// the profile picture off (initials again)
	$reg( 'media/avatar', 'DELETE', function ( WP_REST_Request $q ) {
		$m = nlfmd_member( $q );
		if ( is_wp_error( $m ) ) { return $m; }
		global $wpdb;
		nlfmd_gone_rows( (array) $wpdb->get_results( $wpdb->prepare( 'SELECT * FROM ' . nlfmd_t( 'media' ) . " WHERE member_id = %d AND kind = 'avatar' AND status <> 'gone'", (int) $m['id'] ), ARRAY_A ) );
		return nlf_ok( array( 'message' => 'התמונה הוסרה. במקומה מופיעים ראשי התיבות.' ) );
	} );
} );

/* =========================================================================================================
 * 4. The files on posts: checked before the insert, attached after it, following the post's status
 * ======================================================================================================= */

// HOOK nlf_post_check (inc/pro-forum.php, the topic and reply routes, before the insert)
add_filter( 'nlf_post_check', function ( $err, $type, $m, $q, $t = null ) {
	if ( '' !== (string) $err || ! ( $q instanceof WP_REST_Request ) || ! is_array( $m ) ) { return $err; }
	$items = nlfmd_items_norm( $q->get_param( 'media' ) );
	$pin   = 'reply' === $type ? nlfmd_pin_norm( $q->get_param( 'pin' ) ) : null;
	if ( ! $items && ! $pin ) { return $err; }
	nlfmd_install();
	if ( ! nlfmd_ready() ) { return 'צירוף קבצים לא זמין כרגע. שלחו בלי הקבצים או נסו שוב בעוד רגע.'; }
	$e = nlfmd_count_error( 'reply' === $type ? 'reply' : 'topic', count( $items ) );
	if ( '' !== $e ) { return $e; }
	$rows = nlfmd_rows( array_merge( array_column( $items, 'id' ), $pin ? array( $pin['media'] ) : array() ) );
	$e    = nlfmd_attach_error( $items, $rows, (int) $m['id'] );
	if ( '' !== $e ) { return $e; }
	if ( $pin ) {
		$pm = $rows[ $pin['media'] ] ?? null;
		if ( ! $pm || 'image' !== $pm['kind'] || 'ok' !== $pm['status'] || ! is_array( $t ) || (int) $pm['topic_id'] !== (int) $t['id'] ) { return 'התמונה שסימנתם לא נמצאה. נסו שוב.'; }
	}
	return '';
}, 10, 5 );

// HOOK nlf_post_created (inc/pro-forum.php, after the insert of a topic or a reply)
add_action( 'nlf_post_created', function ( $type, $id, $m, $q, $status, $tid ) {
	if ( ! ( $q instanceof WP_REST_Request ) || ! nlfmd_ready() ) { return; }
	global $wpdb;
	$items = array_slice( nlfmd_items_norm( $q->get_param( 'media' ) ), 0, 'reply' === $type ? nlfmd_limits()['reply'] : nlfmd_limits()['topic'] );
	$st    = 'live' === (string) $status ? 'ok' : 'pending';
	$rid   = 'reply' === $type ? (string) (int) $id : 'NULL'; // an integer or the word NULL, nothing else
	foreach ( $items as $i => $it ) { // the WHERE repeats the owner and "not attached yet": a file can never go on two posts
		$wpdb->query( $wpdb->prepare( 'UPDATE ' . nlfmd_t( 'media' ) . " SET topic_id = %d, reply_id = $rid, caption = %s, sort = %d, status = %s
			WHERE id = %d AND member_id = %d AND topic_id IS NULL AND reply_id IS NULL AND status = 'pending' AND kind IN ('image','pdf')",
			(int) $tid, $it['caption'], (int) $i, $st, (int) $it['id'], (int) $m['id'] ) ); // phpcs:ignore -- $rid is an integer or NULL
	}
	$pin = 'reply' === $type ? nlfmd_pin_norm( $q->get_param( 'pin' ) ) : null;
	if ( $pin ) {
		$wpdb->insert( nlfmd_t( 'pins' ), array( 'media_id' => $pin['media'], 'reply_id' => (int) $id, 'x' => $pin['x'], 'y' => $pin['y'], 'created_at' => nlf_now_sql() ) );
	}
}, 10, 6 );

// HOOK nlf_moderated (inc/pro-forum.php, nlf_moderate): live = shown, hidden = not shown, removed = the files deleted
add_action( 'nlf_moderated', function ( $type, $id, $to ) {
	if ( ! nlfmd_ready() ) { return; }
	global $wpdb;
	$mt    = nlfmd_t( 'media' );
	$where = 'topic' === $type ? $wpdb->prepare( 'topic_id = %d', (int) $id ) : $wpdb->prepare( 'reply_id = %d', (int) $id );
	if ( 'removed' === $to ) {
		nlfmd_gone_rows( (array) $wpdb->get_results( "SELECT * FROM $mt WHERE $where AND status <> 'gone'", ARRAY_A ) ); // phpcs:ignore -- prepared above
		if ( 'reply' === $type ) { $wpdb->delete( nlfmd_t( 'pins' ), array( 'reply_id' => (int) $id ) ); }
		return;
	}
	$own = 'topic' === $type ? ' AND reply_id IS NULL' : '';
	if ( 'live' === $to ) { $wpdb->query( "UPDATE $mt SET status = 'ok' WHERE $where$own AND status = 'pending'" ); } // phpcs:ignore -- prepared above
	if ( 'hidden' === $to ) { $wpdb->query( "UPDATE $mt SET status = 'pending' WHERE $where$own AND status = 'ok'" ); } // phpcs:ignore -- prepared above
}, 10, 3 );

/* files picked but never sent with a post: gone after a day (daily, through WP-Cron) */
function nlfmd_gc() {
	if ( ! nlfmd_ready() ) { return; }
	global $wpdb;
	nlfmd_gone_rows( (array) $wpdb->get_results( $wpdb->prepare( 'SELECT * FROM ' . nlfmd_t( 'media' ) . " WHERE status = 'pending' AND topic_id IS NULL AND reply_id IS NULL AND kind IN ('image','pdf') AND created_at < %s LIMIT 500",
		gmdate( 'Y-m-d H:i:s', time() - DAY_IN_SECONDS ) ), ARRAY_A ) );
}
add_action( 'nlfmd_gc', 'nlfmd_gc' );
add_action( 'init', function () {
	if ( nlfmd_ready() && function_exists( 'wp_next_scheduled' ) && ! wp_next_scheduled( 'nlfmd_gc' ) ) { wp_schedule_event( time() + HOUR_IN_SECONDS, 'daily', 'nlfmd_gc' ); }
}, 30 );

/**
 * The test kit (scripts/project-stage/forum_testkit.py, `clean`): the rows, files and points of the members it removes, of the
 * discussions they opened and of every answer on those discussions. Rows are deleted, not marked. Returns the count.
 */
function nlfmd_purge_members( array $ids, array $tids = array() ) {
	$ids  = array_values( array_filter( array_map( 'intval', $ids ) ) );
	$tids = array_values( array_filter( array_map( 'intval', $tids ) ) );
	if ( ! $ids || ! nlfmd_ready() ) { return 0; }
	global $wpdb;
	$in   = implode( ',', $ids );
	$rids = array_map( 'intval', (array) $wpdb->get_col( 'SELECT id FROM ' . nlf_t( 'replies' ) . " WHERE member_id IN ($in)" . ( $tids ? ' OR topic_id IN (' . implode( ',', $tids ) . ')' : '' ) ) ); // phpcs:ignore -- integers only
	$w    = "member_id IN ($in)" . ( $tids ? ' OR topic_id IN (' . implode( ',', $tids ) . ')' : '' ) . ( $rids ? ' OR reply_id IN (' . implode( ',', $rids ) . ')' : '' );
	$rows = (array) $wpdb->get_results( 'SELECT * FROM ' . nlfmd_t( 'media' ) . " WHERE $w", ARRAY_A ); // phpcs:ignore -- integers only
	foreach ( $rows as $r ) { nlfmd_unlink_row( $r ); }
	$mids = array_map( 'intval', array_column( $rows, 'id' ) );
	if ( $mids ) { $wpdb->query( 'DELETE FROM ' . nlfmd_t( 'pins' ) . ' WHERE media_id IN (' . implode( ',', $mids ) . ')' ); } // phpcs:ignore -- integers only
	if ( $rids ) { $wpdb->query( 'DELETE FROM ' . nlfmd_t( 'pins' ) . ' WHERE reply_id IN (' . implode( ',', $rids ) . ')' ); } // phpcs:ignore -- integers only
	if ( $mids ) { $wpdb->query( 'DELETE FROM ' . nlfmd_t( 'media' ) . ' WHERE id IN (' . implode( ',', $mids ) . ')' ); } // phpcs:ignore -- integers only
	return count( $mids );
}

/* =========================================================================================================
 * 5. HTML: galleries, plans, the point an answer asks about (board 21 part ב), the picture of every member (part ד)
 * ======================================================================================================= */

/**
 * Everything of one discussion in two queries (memoised): files by post ('t' for the opening message, 'r<id>' for an answer),
 * the points of live answers on shown pictures, and the names behind them.
 */
function nlfmd_thread( $tid ) {
	static $memo = array();
	$tid = (int) $tid;
	if ( isset( $memo[ $tid ] ) ) { return $memo[ $tid ]; }
	$out = array( 'posts' => array(), 'pins' => array(), 'byreply' => array() );
	if ( $tid <= 0 || ! nlfmd_ready() ) { return $memo[ $tid ] = $out; }
	global $wpdb;
	$me    = nlf_me();
	$admin = nlf_is_admin();
	$rows  = (array) $wpdb->get_results( $wpdb->prepare( 'SELECT * FROM ' . nlfmd_t( 'media' ) . " WHERE topic_id = %d AND status IN ('ok','pending') AND kind IN ('image','pdf') ORDER BY sort ASC, id ASC", $tid ), ARRAY_A );
	foreach ( $rows as $r ) {
		// a file of a post that waits or is hidden shows only to its author and to administrators
		if ( 'ok' !== $r['status'] && ! $admin && ! ( $me && (int) $me['id'] === (int) $r['member_id'] ) ) { continue; }
		$out['posts'][ empty( $r['reply_id'] ) ? 't' : 'r' . (int) $r['reply_id'] ][] = $r;
	}
	$pins = (array) $wpdb->get_results( $wpdb->prepare( 'SELECT p.media_id, p.reply_id, p.x, p.y, r.member_id FROM ' . nlfmd_t( 'pins' ) . ' p JOIN ' . nlfmd_t( 'media' ) . ' m ON m.id = p.media_id
		JOIN ' . nlf_t( 'replies' ) . " r ON r.id = p.reply_id WHERE m.topic_id = %d AND m.status = 'ok' AND r.status = 'live' ORDER BY p.id ASC LIMIT 500", $tid ), ARRAY_A );
	$mem  = $pins ? nlf_members( array_column( $pins, 'member_id' ) ) : array();
	foreach ( $pins as $p ) {
		$a = nlf_author( $mem[ (int) $p['member_id'] ] ?? null );
		$x = array( 'm' => (int) $p['media_id'], 'r' => (int) $p['reply_id'], 'x' => (float) $p['x'], 'y' => (float) $p['y'], 'n' => $a['name'] );
		$out['pins'][] = $x;
		$out['byreply'][ (int) $p['reply_id'] ] = $x;
	}
	return $memo[ $tid ] = $out;
}

/** the rows of one post by kind, in their order */
function nlfmd_split( array $rows ) {
	$img = array(); $pdf = array();
	foreach ( $rows as $r ) { if ( 'pdf' === $r['kind'] ) { $pdf[] = $r; } else { $img[] = $r; } }
	return array( $img, $pdf );
}

/** the "sizes" of a tile: the whole column for one, half for two, two thirds and one third for three (max column 728px) */
function nlfmd_sizes( $lay, $i ) {
	if ( 'one' === $lay ) { return '(max-width:760px) 100vw, 728px'; }
	if ( 'two' === $lay ) { return '(max-width:760px) 50vw, 364px'; }
	return 0 === $i ? '(max-width:760px) 66vw, 486px' : '(max-width:760px) 34vw, 243px';
}

/**
 * The gallery of one post (board 21 part ב): real <img> with width, height and alt for every picture (the ones beyond three stay
 * in the page, hidden, so the full-screen view and search engines have all of them); each tile is a link to the picture itself,
 * so it opens with the script off too.
 */
function nlfmd_gallery_html( array $img, $by, $at ) {
	$n = count( $img );
	if ( ! $n ) { return ''; }
	$lay  = nlfmd_layout( $n );
	$more = nlfmd_more( $n );
	$h    = '<div class="nlfmd-gal nlfmd-gal-' . $lay . '" data-nlfmd-gal data-by="' . esc_attr( $by ) . '" data-at="' . esc_attr( $at ) . '">';
	foreach ( array_values( $img ) as $i => $r ) {
		$rel   = (string) $r['path'];
		if ( ! nlfmd_rel_ok( $rel ) ) { continue; }
		$full  = nlfmd_url( $rel );
		$thumb = nlfmd_url( nlfmd_variant( $rel, '-480' ) );
		$w     = max( 1, (int) $r['w'] ); $hh = max( 1, (int) $r['h'] );
		$tw    = $w >= $hh ? min( 480, $w ) : (int) round( $w * min( 480, $hh ) / $hh );
		$th    = $w >= $hh ? (int) round( $hh * min( 480, $w ) / $w ) : min( 480, $hh );
		$isx   = 2 === $i && $more > 0;
		$h    .= '<a class="nlfmd-tile' . ( $isx ? ' is-more' : '' ) . ( 'pending' === $r['status'] ? ' is-wait' : '' ) . '" href="' . esc_url( $full ) . '" data-nlfmd-id="' . (int) $r['id'] . '" data-w="' . $w . '" data-h="' . $hh . '" data-cap="' . esc_attr( (string) $r['caption'] ) . '"'
			. ' aria-label="' . esc_attr( 'פתיחת תמונה ' . ( $i + 1 ) . ' מתוך ' . $n . ' במסך מלא' . ( $isx ? ', ועוד ' . $more : '' ) ) . '"' . ( $i < 3 ? '' : ' hidden' ) . '>'
			. '<img src="' . esc_url( $thumb ) . '" srcset="' . esc_url( $thumb ) . ' ' . $tw . 'w, ' . esc_url( $full ) . ' ' . $w . 'w" sizes="' . esc_attr( nlfmd_sizes( $lay, $i ) ) . '"'
			. ' width="' . $tw . '" height="' . $th . '" alt="' . esc_attr( nlfmd_alt( $r['caption'] ) ) . '" loading="lazy" decoding="async">'
			. ( $isx ? '<span class="nlfmd-plus" aria-hidden="true">+' . (int) $more . '</span>' : '' ) . '</a>';
	}
	return $h . '</div>';
}

/** a plan's card and its two buttons (board 21 part ב); the board button only where a video room can open */
function nlfmd_pdf_html( array $pdf, $topic, $rooms ) {
	$h = '';
	foreach ( $pdf as $r ) {
		$rel = (string) $r['path'];
		if ( ! nlfmd_rel_ok( $rel ) ) { continue; }
		$url   = nlfmd_url( $rel );
		$title = '' !== trim( (string) $r['caption'] ) ? (string) $r['caption'] : 'קובץ PDF';
		$prev  = ! empty( $r['preview'] );
		$h .= '<div class="nlfmd-pdf"><a class="nlfmd-pdf-card" href="' . esc_url( $url ) . '" target="_blank" rel="noopener">'
			. '<span class="nlfmd-pdf-th" aria-hidden="true">' . ( $prev ? '<img src="' . esc_url( nlfmd_url( nlfmd_variant( $rel, '-480' ) ) ) . '" alt="" width="58" height="72" loading="lazy" decoding="async">' : '' ) . '</span>'
			. '<span class="nlfmd-pdf-tx"><b>' . esc_html( $title ) . '</b><span>' . esc_html( nlfmd_pdf_meta( (int) $r['pages'], (int) $r['bytes'] ) ) . '</span></span></a>'
			. '<div class="nlfmd-pdf-acts">'
			. ( $rooms && $topic > 0 ? '<button type="button" class="nlfmd-btn nlfmd-btn-ink" data-nlf-room="' . (int) $topic . '"' . ( $prev ? ' data-nlfmd-board="' . esc_url( nlfmd_url( nlfmd_variant( $rel, '-p' ) ) ) . '"' : '' ) . '>לשרטט עליה ביחד</button>' : '' )
			. '<a class="nlfmd-btn nlfmd-btn-line" href="' . esc_url( $url ) . '" download aria-label="' . esc_attr( 'הורדה: ' . $title ) . '">הורדה</a></div></div>';
	}
	return $h;
}

/** a video room can open on this discussion (the call module is on and LiveKit is set up) */
function nlfmd_rooms( $t ) {
	return is_array( $t ) && 'live' === (string) ( $t['status'] ?? '' ) && function_exists( 'nlfc_rooms_ready' ) && nlfc_rooms_ready();
}

/** "מיכל א." and "לפני 20 דקות" for the full-screen view's top row */
function nlfmd_by_at( $member_id, $created ) {
	$mem = nlf_members( array( (int) $member_id ) );
	$a   = nlf_author( $mem[ (int) $member_id ] ?? null );
	$ts  = nlf_ts( $created );
	$ago = nlf_ago( $ts, time() );
	return array( $a['name'], '' !== $ago ? $ago : wp_date( 'j.n.Y', $ts ) );
}

// HOOK nlf_topic_after_body (5, before the social chips at 10 and the call row at 20): the opening message's files, and the
// points of the whole discussion for the full-screen view
add_filter( 'nlf_topic_after_body', function ( $html, $t ) {
	if ( ! is_array( $t ) || ! nlfmd_ready() ) { return $html; }
	$th  = nlfmd_thread( (int) $t['id'] );
	$out = '';
	if ( ! empty( $th['posts']['t'] ) ) {
		list( $img, $pdf ) = nlfmd_split( $th['posts']['t'] );
		list( $by, $at )   = nlfmd_by_at( (int) $t['member_id'], $t['created_at'] );
		$out = '<div class="nlfmd-media">' . nlfmd_gallery_html( $img, $by, $at ) . nlfmd_pdf_html( $pdf, (int) $t['id'], nlfmd_rooms( $t ) ) . '</div>';
	}
	if ( $th['pins'] ) { $out .= '<script type="application/json" id="nlfmd-pins">' . nlf_json_script( $th['pins'] ) . '</script>'; }
	return $out . $html;
}, 5, 2 );

// HOOK nlf_reply_after_body (inc/pro-forum-render.php): an answer's files, and the crop of the point it asks about
add_filter( 'nlf_reply_after_body', function ( $html, $r, $me, $t ) {
	if ( ! is_array( $r ) || ! is_array( $t ) || ! nlfmd_ready() ) { return $html; }
	$th  = nlfmd_thread( (int) $t['id'] );
	$key = 'r' . (int) $r['id'];
	$out = '';
	$pin = $th['byreply'][ (int) $r['id'] ] ?? null;
	if ( $pin ) { $out .= nlfmd_pinq_html( $pin ); }
	if ( ! empty( $th['posts'][ $key ] ) ) {
		list( $img, $pdf ) = nlfmd_split( $th['posts'][ $key ] );
		list( $by, $at )   = nlfmd_by_at( (int) $r['member_id'], $r['created_at'] );
		$out .= '<div class="nlfmd-media">' . nlfmd_gallery_html( $img, $by, $at ) . nlfmd_pdf_html( $pdf, (int) $t['id'], nlfmd_rooms( $t ) ) . '</div>';
	}
	return $html . $out;
}, 10, 4 );

/** the small crop with the raspberry marker at the top of an answer that asks about a point (opens the picture full screen) */
function nlfmd_pinq_html( array $pin ) {
	$rows = nlfmd_rows( array( (int) $pin['m'] ) );
	$m    = $rows[ (int) $pin['m'] ] ?? null;
	if ( ! $m || ! nlfmd_rel_ok( (string) $m['path'] ) ) { return ''; }
	list( $px, $mx ) = nlfmd_crop( $pin['x'] );
	list( $py, $my ) = nlfmd_crop( $pin['y'] );
	$ar = max( 1, (int) $m['w'] ) . '/' . max( 1, (int) $m['h'] );
	return '<button type="button" class="nlfmd-pinq" data-nlfmd-open="' . (int) $m['id'] . '" data-nlfmd-pin="' . (int) $pin['r'] . '" aria-label="' . esc_attr( 'פתיחת התמונה עם הנקודה המסומנת' ) . '">'
		. '<span class="nlfmd-pinq-crop" style="' . esc_attr( 'aspect-ratio:' . $ar . ';background-image:url(' . esc_url( nlfmd_url( nlfmd_variant( (string) $m['path'], '-480' ) ) ) . ');background-position:' . $px . '% ' . $py . '%' ) . '" aria-hidden="true">'
		. '<i class="nlfmd-dot" style="' . esc_attr( 'left:' . $mx . '%;top:' . $my . '%' ) . '"></i></span>'
		. '<span class="nlfmd-pinq-t">שאלה על נקודה בתמונה</span></button>';
}

// HOOK nlf_jsonld (inc/pro-forum.php, wp_head): the discussion's first shown picture
add_filter( 'nlf_jsonld', function ( $ld, $t ) {
	if ( ! is_array( $ld ) || ! is_array( $t ) || ! nlfmd_ready() ) { return $ld; }
	$th    = nlfmd_thread( (int) $t['id'] );
	$first = null;
	foreach ( $th['posts'] as $rows ) {
		foreach ( $rows as $r ) { if ( 'image' === $r['kind'] && 'ok' === $r['status'] && nlfmd_rel_ok( (string) $r['path'] ) ) { $first = $r; break 2; } }
	}
	if ( ! $first ) { return $ld; }
	$img = array( '@type' => 'ImageObject', 'url' => nlfmd_url( (string) $first['path'] ), 'width' => (int) $first['w'], 'height' => (int) $first['h'] );
	if ( '' !== trim( (string) $first['caption'] ) ) { $img['caption'] = (string) $first['caption']; }
	if ( 'QAPage' === ( $ld['@type'] ?? '' ) && isset( $ld['mainEntity'] ) && is_array( $ld['mainEntity'] ) ) { $ld['mainEntity']['image'] = $img; }
	else { $ld['image'] = $img; }
	return $ld;
}, 10, 2 );

/** member id => the address of his picture (every picture in one query per request) */
function nlfmd_avatar_url( $mid ) {
	static $map = null;
	if ( null === $map ) {
		$map = array();
		if ( nlfmd_ready() ) {
			global $wpdb;
			foreach ( (array) $wpdb->get_results( 'SELECT member_id, path FROM ' . nlfmd_t( 'media' ) . " WHERE kind = 'avatar' AND status = 'ok' ORDER BY id ASC", ARRAY_A ) as $r ) { // phpcs:ignore -- no input
				if ( nlfmd_rel_ok( (string) $r['path'] ) ) { $map[ (int) $r['member_id'] ] = nlfmd_url( (string) $r['path'] ); }
			}
		}
	}
	return $map[ (int) $mid ] ?? '';
}

// HOOK nlf_avatar_html (inc/pro-forum-render.php, nlf_avatar): the picture in place of the initials; the initials stay without one
add_filter( 'nlf_avatar_html', function ( $html, $a, $big ) {
	$mid = is_array( $a ) ? (int) ( $a['mid'] ?? 0 ) : 0;
	$url = $mid > 0 ? nlfmd_avatar_url( $mid ) : '';
	if ( '' === $url ) { return $html; }
	$cls = 'nlf-av nlfmd-av' . ( ! empty( $a['pro'] ) ? ' nlf-av-sq' : '' ) . ( $big ? ' nlf-av-lg' : '' );
	return '<span class="' . $cls . '" aria-hidden="true"><img src="' . esc_url( $url ) . '" alt="" width="44" height="44" loading="lazy" decoding="async"></span>';
}, 10, 3 );

/** "תמונת פרופיל", the member's own button (part ד) */
function nlfmd_avatar_button() {
	return '<button type="button" class="nlf-link nlfmd-avlink" data-nlfmd-avatar aria-haspopup="dialog">תמונת פרופיל</button>';
}
add_filter( 'nlf_member_bar_extra', function ( $html, $me ) { return is_array( $me ) && nlfmd_ready() ? $html . nlfmd_avatar_button() : $html; }, 30, 2 );
add_filter( 'nlf_owner_box_extra', function ( $html, $pro, $me ) { return is_array( $me ) && nlfmd_ready() ? $html . '<p class="nlfmd-ownrow">' . nlfmd_avatar_button() . '</p>' : $html; }, 30, 3 );

/** the picture sheet (part ד): the stage with the circle, the zoom, the two sample faces and "לשמור את התמונה" */
function nlfmd_avatar_sheet( $me ) {
	$a   = nlf_author( $me );
	$url = nlfmd_avatar_url( (int) $me['id'] );
	$mine = '' !== $url ? '<img src="' . esc_url( $url ) . '" alt="" width="40" height="40">' : esc_html( nlf_initials( $a['name'] ) );
	return '<dialog class="nlf nlf-sheet nlf-sheet-sm nlfmd-avsheet" id="nlfmd-avatar" dir="rtl" aria-labelledby="nlfmd-av-h">'
		. '<div class="nlf-sheet-h"><button type="button" class="nlf-ico" data-nlf-close aria-label="סגירה">' . nlf_svg( 'close' ) . '</button><h2 class="nlf-h2" id="nlfmd-av-h">תמונת פרופיל</h2></div>'
		. '<div class="nlfmd-avbody">'
		. '<div class="nlfmd-avrow"><div class="nlfmd-stage" data-nlfmd-stage tabindex="0" role="group" aria-label="מיקום התמונה בעיגול: גוררים, או חיצים להזזה ופלוס ומינוס להגדלה">'
		. '<canvas width="224" height="224" aria-hidden="true"></canvas><span class="nlfmd-ring" aria-hidden="true"></span>'
		. '<button type="button" class="nlfmd-stage-empty" data-nlfmd-avpick>בחירת תמונה</button></div>'
		. '<div class="nlfmd-avside"><span class="nlfmd-hint">גוררים כדי למרכז. תמונה אמיתית של הפנים או לוגו של העסק.</span>'
		. '<label class="nlfmd-sr" for="nlfmd-zoom">הגדלה</label><input type="range" id="nlfmd-zoom" class="nlfmd-zoom" min="100" max="400" step="1" value="100" data-nlfmd-zoom disabled></div></div>'
		. '<div class="nlfmd-avsamples"><span class="nlf-av nlfmd-avme' . ( $a['pro'] ? ' nlf-av-sq' : '' ) . '" style="' . nlf_tint_style( $a['tint'] ) . '" data-nlfmd-avme aria-hidden="true">' . $mine . '</span>'
		. '<span class="nlf-av" style="' . nlf_tint_style( array( '#DCE6F2', '#1D3B66' ) ) . '" aria-hidden="true">רב</span>'
		. '<span class="nlf-av" style="' . nlf_tint_style( array( '#E3F0EA', '#1D5A40' ) ) . '" aria-hidden="true">דש</span>'
		. '<span class="nlfmd-avnote">מי שלא העלה: ראשי תיבות בצבע של המקצוע</span></div>'
		. '<div class="nlfmd-avbtns"><button type="button" class="nlfmd-btn nlfmd-btn-line" data-nlfmd-avpick>בחירת תמונה</button>'
		. '<button type="button" class="nlf-link" data-nlfmd-avremove' . ( '' === $url ? ' hidden' : '' ) . '>הסרת התמונה</button></div>'
		. '<input type="file" accept="image/*" hidden data-nlfmd-avfile>'
		. '<button type="button" class="nlfmd-btn nlfmd-btn-sea nlfmd-btn-wide" data-nlfmd-avsave disabled>לשמור את התמונה</button>'
		. '<p class="nlf-msg" role="status" aria-live="polite"></p></div></dialog>';
}

/* =========================================================================================================
 * 6. Assets (forum surfaces only) and the picture sheet
 * ======================================================================================================= */

function nlfmd_surface() {
	if ( ! function_exists( 'nlf_surface' ) ) { return false; }
	if ( '' === nlf_rendering() && ! empty( $GLOBALS['nlf_act_page'] ) ) { return false; } // a one-click page needs none of this
	return nlf_surface();
}

/** the page script's numbers and words (from section 1), the discussion, and whether a video room can open */
function nlfmd_config() {
	$l  = nlfmd_limits();
	$t  = 'topic' === nlf_rendering() && ! empty( $GLOBALS['nlf_topic'] ) ? $GLOBALS['nlf_topic'] : null;
	$ed = function_exists( 'wp_image_editor_supports' ) && wp_image_editor_supports( array( 'mime_type' => 'image/webp' ) );
	return array(
		'rest'   => esc_url_raw( rest_url( 'nadlan/v1/forum/' ) ),
		'on'     => nlfmd_ready() ? 1 : 0,
		'limits' => array( 'topic' => $l['topic'], 'reply' => $l['reply'], 'img' => nlfmd_mb( $l['img_mb'] ), 'pdf' => nlfmd_mb( $l['pdf_mb'] ), 'imgMb' => $l['img_mb'], 'pdfMb' => $l['pdf_mb'],
			'long' => $l['client_long'], 'caption' => $l['caption'], 'avatar' => $l['avatar'] ),
		'text'   => array( 'topic' => nlfmd_limits_text( 'topic' ), 'reply' => nlfmd_limits_text( 'reply' ) ),
		'webp'   => $ed ? 1 : 0, // the browser sends WebP only when the host's image editor can read it
		'topic'  => $t ? (int) $t['id'] : 0,
		'rooms'  => $t && nlfmd_rooms( $t ) ? 1 : 0,
	);
}

add_action( 'wp_enqueue_scripts', function () {
	if ( ! nlfmd_surface() ) { return; }
	nlfmd_install();
	$base = plugins_url( 'assets/proforum/', dirname( __FILE__ ) );
	$ver  = function_exists( 'nlf_ver' ) ? nlf_ver() : '1';
	wp_enqueue_style( 'nlf-media', $base . 'media.css', array( 'nlf' ), $ver );
	if ( ! nlfmd_ready() ) { return; } // without the tables only the style (old pages may still print nothing of this layer)
	wp_enqueue_script( 'nlf-media', $base . 'media.js', array( 'nlf' ), $ver, true );
	wp_add_inline_script( 'nlf-media', 'window.NLFMD=' . nlf_json_script( nlfmd_config() ) . ';', 'before' );
}, 34 );

add_action( 'wp_footer', function () {
	if ( ! nlfmd_surface() || ! nlfmd_ready() || ( '' === nlf_rendering() && empty( $GLOBALS['nlf_card_printed'] ) ) ) { return; }
	$me = nlf_me();
	if ( $me ) { echo nlfmd_avatar_sheet( $me ); } // phpcs:ignore -- escaped inside
}, 7 ); // before the footer scripts (forum.js wires every dialog.nlf when it runs)
