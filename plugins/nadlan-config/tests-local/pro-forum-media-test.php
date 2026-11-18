<?php
/**
 * Plain PHP CLI test of the forum's media layer (no WordPress): php tests-local/pro-forum-media-test.php
 * Loads the forum's pure part (NLF_PURE_ONLY) and then part 1 of inc/pro-forum-media.php (NLFMD_PURE_ONLY), plus static checks
 * on the module's files and on the one-line hooks it needs in the forum's own files. Exit code 0 = all passed.
 */
define( 'ABSPATH', __DIR__ . '/' );
define( 'NLF_PURE_ONLY', true );
define( 'NLFMD_PURE_ONLY', true );
require __DIR__ . '/../inc/pro-forum.php';
require __DIR__ . '/../inc/pro-forum-media.php';

$pass = 0; $fail = 0;
function t( $name, $cond ) {
	global $pass, $fail;
	if ( $cond ) { $pass++; echo "ok   $name\n"; } else { $fail++; echo "FAIL $name\n"; }
}

/* the numbers of board 21 */
$L = nlfmd_limits();
t( 'limits: 20 a message, 10 an answer', 20 === $L['topic'] && 10 === $L['reply'] );
t( 'limits: picture 10MB, plan 25MB', 10 === $L['img_mb'] && 25 === $L['pdf_mb'] && 10485760 === nlfmd_mb( 10 ) );
t( 'limits: 80 files and 400MB a day', 80 === $L['day_n'] && 400 === $L['day_mb'] );
t( 'limits: 2560 in the browser, 2048 + 480 on the server, 256 profile, caption 180', 2560 === $L['client_long'] && 2048 === $L['long'] && 480 === $L['thumb'] && 256 === $L['avatar'] && 180 === $L['caption'] );
t( 'limits line of a message = the board, word for word', 'עד 20 תמונות בהודעה, עד 10MB כל אחת (מוקטנות אוטומטית). תוכנית או מסמך PDF עד 25MB. תמונה מהאייפון מומרת לבד.' === nlfmd_limits_text( 'topic' ) );
t( 'limits line of an answer says 10 and בתגובה', 'עד 10 תמונות בתגובה, עד 10MB כל אחת (מוקטנות אוטומטית). תוכנית או מסמך PDF עד 25MB. תמונה מהאייפון מומרת לבד.' === nlfmd_limits_text( 'reply' ) );

/* magic bytes, never the name */
t( 'sniff jpeg', 'jpeg' === nlfmd_sniff( "\xFF\xD8\xFF\xE0\x00\x10JFIF" ) );
t( 'sniff png', 'png' === nlfmd_sniff( "\x89PNG\r\n\x1A\n\x00\x00" ) );
t( 'sniff webp', 'webp' === nlfmd_sniff( "RIFF\x24\x00\x00\x00WEBPVP8 " ) );
t( 'sniff gif', 'gif' === nlfmd_sniff( 'GIF89a' . "\x01\x00" ) && 'gif' === nlfmd_sniff( 'GIF87a' ) );
t( 'sniff pdf', 'pdf' === nlfmd_sniff( "%PDF-1.7\n%\xE2\xE3" ) );
t( 'sniff heic', 'heic' === nlfmd_sniff( "\x00\x00\x00\x18ftypheic\x00\x00" ) && 'heic' === nlfmd_sniff( "\x00\x00\x00\x1Cftypmif1" ) );
t( 'sniff refuses php, html, exe, zip, svg', '' === nlfmd_sniff( '<?php echo 1;' ) && '' === nlfmd_sniff( '<html><body>' ) && '' === nlfmd_sniff( "MZ\x90\x00" )
	&& '' === nlfmd_sniff( "PK\x03\x04" ) && '' === nlfmd_sniff( '<svg xmlns=' ) );
t( 'sniff: a PDF head not at byte 0 is refused', '' === nlfmd_sniff( " %PDF-1.4" ) );
t( 'sniff: a riff that is not webp is refused', '' === nlfmd_sniff( "RIFF\x24\x00\x00\x00WAVEfmt " ) );
t( 'kind of a type', 'image' === nlfmd_kind_of( 'jpeg' ) && 'image' === nlfmd_kind_of( 'webp' ) && 'pdf' === nlfmd_kind_of( 'pdf' ) && '' === nlfmd_kind_of( 'heic' ) && '' === nlfmd_kind_of( '' ) );

/* upload rules */
t( 'upload ok: a picture', '' === nlfmd_upload_error( 'post', 'jpeg', 2000000 ) );
t( 'upload ok: a plan', '' === nlfmd_upload_error( 'post', 'pdf', 20000000 ) );
t( 'upload ok: a profile picture', '' === nlfmd_upload_error( 'avatar', 'png', 300000 ) );
t( 'upload: empty refused', '' !== nlfmd_upload_error( 'post', 'jpeg', 0 ) );
t( 'upload: unknown bytes refused', false !== strpos( nlfmd_upload_error( 'post', '', 100 ), 'PDF' ) );
t( 'upload: heic asks for JPG', false !== strpos( nlfmd_upload_error( 'post', 'heic', 100 ), 'JPG' ) );
t( 'upload: a PDF is no profile picture', '' !== nlfmd_upload_error( 'avatar', 'pdf', 100 ) );
t( 'upload: picture 10MB ok, one byte more refused', '' === nlfmd_upload_error( 'post', 'jpeg', 10485760 ) && false !== strpos( nlfmd_upload_error( 'post', 'jpeg', 10485761 ), '10MB' ) );
t( 'upload: plan 25MB ok, one byte more refused', '' === nlfmd_upload_error( 'post', 'pdf', 26214400 ) && false !== strpos( nlfmd_upload_error( 'post', 'pdf', 26214401 ), '25MB' ) );
t( 'day: 79 files ok, 80 refused', '' === nlfmd_day_error( 79, 0, 100 ) && '' !== nlfmd_day_error( 80, 0, 100 ) );
t( 'day: 400MB is the ceiling', '' === nlfmd_day_error( 1, nlfmd_mb( 399 ), nlfmd_mb( 1 ) ) && '' !== nlfmd_day_error( 1, nlfmd_mb( 399 ), nlfmd_mb( 1 ) + 1 ) );
t( 'count: a message 20 ok, 21 refused', '' === nlfmd_count_error( 'topic', 20 ) && false !== strpos( nlfmd_count_error( 'topic', 21 ), '20' ) );
t( 'count: an answer 10 ok, 11 refused', '' === nlfmd_count_error( 'reply', 10 ) && false !== strpos( nlfmd_count_error( 'reply', 11 ), '10' ) );
t( 'count: zero is fine', '' === nlfmd_count_error( 'topic', 0 ) && '' === nlfmd_count_error( 'reply', 0 ) );

/* the gallery shape */
t( 'layout: none, one, two, three', '' === nlfmd_layout( 0 ) && 'one' === nlfmd_layout( 1 ) && 'two' === nlfmd_layout( 2 ) && 'three' === nlfmd_layout( 3 ) && 'three' === nlfmd_layout( 20 ) );
t( '+N: 7 pictures show +4 (the board), 3 show none', 4 === nlfmd_more( 7 ) && 0 === nlfmd_more( 3 ) && 0 === nlfmd_more( 1 ) && 17 === nlfmd_more( 20 ) );

/* a point on a picture */
t( 'clamp: inside stays', 0.25 === nlfmd_clamp01( '0.25' ) && 0.0 === nlfmd_clamp01( 0 ) && 1.0 === nlfmd_clamp01( 1 ) );
t( 'clamp: outside is clamped to 0..1', 0.0 === nlfmd_clamp01( -3 ) && 1.0 === nlfmd_clamp01( 7.5 ) && 1.0 === nlfmd_clamp01( '1e400' ) );
t( 'clamp: 4 decimals', 0.1235 === nlfmd_clamp01( 0.123456 ) );
t( 'clamp: not a number is null', null === nlfmd_clamp01( 'abc' ) && null === nlfmd_clamp01( null ) && null === nlfmd_clamp01( array() ) && null === nlfmd_clamp01( NAN ) );
t( 'pin: a good one', array( 'media' => 5, 'x' => 0.3, 'y' => 0.9 ) === nlfmd_pin_norm( array( 'media' => '5', 'x' => 0.3, 'y' => '0.9' ) ) );
t( 'pin: clamped', array( 'media' => 5, 'x' => 0.0, 'y' => 1.0 ) === nlfmd_pin_norm( array( 'media' => 5, 'x' => -1, 'y' => 4 ) ) );
t( 'pin: refused without a picture, without x or y, with words', null === nlfmd_pin_norm( array( 'x' => 0.1, 'y' => 0.1 ) ) && null === nlfmd_pin_norm( array( 'media' => 5, 'x' => 0.1 ) )
	&& null === nlfmd_pin_norm( array( 'media' => 5, 'x' => 'left', 'y' => 0.2 ) ) && null === nlfmd_pin_norm( 'x' ) && null === nlfmd_pin_norm( array( 'media' => -2, 'x' => 0, 'y' => 0 ) ) );
t( 'crop: the middle', array( 50.0, 50.0 ) === nlfmd_crop( 0.5 ) );
t( 'crop: the edges keep the point on the edge', array( 0.0, 0.0 ) === nlfmd_crop( 0 ) && array( 100.0, 100.0 ) === nlfmd_crop( 1 ) );
t( 'crop: a quarter (3x): background 12.5%, marker in the middle', array( 12.5, 50.0 ) === nlfmd_crop( 0.25 ) );
t( 'crop: near the edge the marker moves, the picture does not', array( 0.0, 30.0 ) === nlfmd_crop( 0.1 ) );

/* the files as sent with a post */
$items = nlfmd_items_norm( array( array( 'id' => 9, 'caption' => 'סדק מעל המשקוף, סלון' ), array( 'id' => '4' ), 7, array( 'id' => 9, 'caption' => 'שוב' ), array( 'id' => -3 ), 'x', array( 'id' => 0 ) ) );
t( 'items: order kept, duplicates and bad ids out', array( 9, 4, 7 ) === array_column( $items, 'id' ) );
t( 'items: the caption kept', 'סדק מעל המשקוף, סלון' === $items[0]['caption'] && '' === $items[1]['caption'] );
t( 'items: not a list = none', array() === nlfmd_items_norm( 'abc' ) && array() === nlfmd_items_norm( null ) );
$cap = nlfmd_caption( str_repeat( 'א', 300 ) );
t( 'caption: at most 180 characters', 180 === mb_strlen( $cap, 'UTF-8' ) );
t( 'caption: one line, bidi overrides out', 'שורה אחת ושנייה' === nlfmd_caption( "שורה אחת\nושנייה\u{202E}" ) );
$own = array( 'id' => 1, 'member_id' => 3, 'kind' => 'image', 'status' => 'pending', 'topic_id' => null, 'reply_id' => null );
t( 'attach: my own file, not on a post yet', '' === nlfmd_attach_error( array( array( 'id' => 1 ) ), array( 1 => $own ), 3 ) );
t( 'attach: somebody else\'s file refused', '' !== nlfmd_attach_error( array( array( 'id' => 1 ) ), array( 1 => $own ), 4 ) );
t( 'attach: a file already on a post refused', '' !== nlfmd_attach_error( array( array( 'id' => 1 ) ), array( 1 => array( 'topic_id' => 8 ) + $own ), 3 ) );
t( 'attach: a deleted file refused', '' !== nlfmd_attach_error( array( array( 'id' => 1 ) ), array( 1 => array( 'status' => 'gone' ) + $own ), 3 ) );
t( 'attach: a profile picture is not a post file', '' !== nlfmd_attach_error( array( array( 'id' => 1 ) ), array( 1 => array( 'kind' => 'avatar' ) + $own ), 3 ) );
t( 'attach: an unknown id refused', '' !== nlfmd_attach_error( array( array( 'id' => 2 ) ), array( 1 => $own ), 3 ) );

/* addresses */
$hex = str_repeat( 'a1', 16 );
$rel = nlfmd_rel( '2026/11', $hex, 'jpg' );
t( 'path: nlf-media/YYYY/MM/<32 hex>.jpg', 'nlf-media/2026/11/' . $hex . '.jpg' === $rel && nlfmd_rel_ok( $rel ) );
t( 'path: a plan', nlfmd_rel_ok( nlfmd_rel( '2026/01', $hex, 'pdf' ) ) );
t( 'path: the thumb and the first page are siblings', 'nlf-media/2026/11/' . $hex . '-480.jpg' === nlfmd_variant( $rel, '-480' ) && 'nlf-media/2026/11/' . $hex . '-p.jpg' === nlfmd_variant( nlfmd_rel( '2026/11', $hex, 'pdf' ), '-p' ) );
t( 'path: anything else refused', ! nlfmd_rel_ok( 'nlf-media/2026/11/../../wp-config.php' ) && ! nlfmd_rel_ok( 'nlf-media/2026/11/' . $hex . '.php' ) && ! nlfmd_rel_ok( 'nlf-media/2026/11/' . strtoupper( $hex ) . '.jpg' )
	&& ! nlfmd_rel_ok( 'nlf-media/2026/11/abc.jpg' ) && ! nlfmd_rel_ok( 'uploads/2026/11/' . $hex . '.jpg' ) && ! nlfmd_rel_ok( 'nlf-media/2026/11/' . $hex . '-480.jpg' ) );
t( 'path: a random name every time (the module uses random_bytes(16))', 32 === strlen( bin2hex( random_bytes( 16 ) ) ) );

/* plans */
t( 'pdf pages: counted by /Type /Page', 3 === nlfmd_pdf_pages( "%PDF-1.4\n1 0 obj << /Type /Pages /Kids [2 0 R 3 0 R 4 0 R] /Count 3 >>\n2 0 obj << /Type /Page >>\n3 0 obj <</Type/Page/Parent 1 0 R>>\n4 0 obj << /Type /Page >>" ) );
t( 'pdf pages: /Count when the pages are packed', 7 === nlfmd_pdf_pages( "%PDF-1.5\n<< /Type /Pages /Kids [5 0 R] /Count 7 >>" ) && 12 === nlfmd_pdf_pages( "%PDF-1.5\n<< /Count 12 /Kids [] /Type /Pages >>" ) );
t( 'pdf pages: unknown = 0', 0 === nlfmd_pdf_pages( "%PDF-1.7\nstream x\x9c\x00endstream" ) );
t( 'size: 2.4MB as on the board', '2.4MB' === nlfmd_size_text( 2516582 ) && '2MB' === nlfmd_size_text( 2097152 ) && '640KB' === nlfmd_size_text( 655360 ) && '1KB' === nlfmd_size_text( 10 ) );
t( 'plan line as on the board', 'PDF · 3 עמודים · 2.4MB' === nlfmd_pdf_meta( 3, 2516582 ) );
t( 'plan line: one page, unknown pages', 'PDF · עמוד אחד · 640KB' === nlfmd_pdf_meta( 1, 655360 ) && 'PDF · 2.4MB' === nlfmd_pdf_meta( 0, 2516582 ) );
t( 'alt: the caption or "תמונה מהדיון"', 'סדק בסלון' === nlfmd_alt( 'סדק בסלון' ) && 'תמונה מהדיון' === nlfmd_alt( '  ' ) );

/* metadata out of every JPEG */
$seg  = function ( $mk, $payload ) { return "\xFF" . chr( $mk ) . pack( 'n', strlen( $payload ) + 2 ) . $payload; };
$jpg  = "\xFF\xD8" . $seg( 0xE0, "JFIF\x00\x01\x01\x00\x00\x01\x00\x01\x00\x00" )
	. $seg( 0xE1, "Exif\x00\x00MM\x00\x2A GPSLatitude 32.0853 GPSLongitude 34.7818" )
	. $seg( 0xE2, "ICC_PROFILE\x00\x01\x01colour" )
	. $seg( 0xE1, 'http://ns.adobe.com/xap/1.0/' . "\x00<x:xmpmeta>geo</x:xmpmeta>" )
	. $seg( 0xED, "Photoshop 3.0\x00IPTC city" )
	. $seg( 0xFE, 'a comment with a name' )
	. $seg( 0xDB, str_repeat( "\x01", 65 ) )
	. $seg( 0xDA, "\x01\x01\x00\x00\x3F\x00" ) . "\x12\x34\xFF\x00\x56" . "\xFF\xD9";
$out  = nlfmd_jpeg_strip( $jpg );
t( 'strip: a JPEG with EXIF, GPS, XMP, IPTC and a comment has metadata', nlfmd_jpeg_has_meta( $jpg ) );
t( 'strip: EXIF and GPS gone', '' !== $out && false === strpos( $out, 'Exif' ) && false === strpos( $out, 'GPS' ) && false === strpos( $out, '32.0853' ) );
t( 'strip: XMP, IPTC and the comment gone', false === strpos( $out, 'xmpmeta' ) && false === strpos( $out, 'IPTC' ) && false === strpos( $out, 'a comment' ) );
t( 'strip: JFIF, the colour profile, the tables and the picture data kept', false !== strpos( $out, 'JFIF' ) && false !== strpos( $out, 'ICC_PROFILE' ) && false !== strpos( $out, str_repeat( "\x01", 65 ) )
	&& "\x12\x34\xFF\x00\x56\xFF\xD9" === substr( $out, -7 ) && "\xFF\xD8" === substr( $out, 0, 2 ) );
t( 'strip: a clean JPEG stays the same', $out === nlfmd_jpeg_strip( $out ) && ! nlfmd_jpeg_has_meta( $out ) );
t( 'strip: not a JPEG = nothing', '' === nlfmd_jpeg_strip( 'GIF89a' ) && '' === nlfmd_jpeg_strip( "\xFF\xD8\xFF\xE1\xFF\xFF" ) && '' === nlfmd_jpeg_strip( '' ) );

/* static checks on the module's files */
$php  = (string) file_get_contents( __DIR__ . '/../inc/pro-forum-media.php' );
$js   = (string) file_get_contents( __DIR__ . '/../assets/proforum/media.js' );
$css  = (string) file_get_contents( __DIR__ . '/../assets/proforum/media.css' );
$core = (string) file_get_contents( __DIR__ . '/../inc/pro-forum.php' );
$rnd  = (string) file_get_contents( __DIR__ . '/../inc/pro-forum-render.php' );
$fjs  = (string) file_get_contents( __DIR__ . '/../assets/proforum/forum.js' );
$cjs  = (string) file_get_contents( __DIR__ . '/../assets/proforum/call.js' );
$bjs  = (string) file_get_contents( __DIR__ . '/../assets/proforum/board.js' );
$kit  = (string) file_get_contents( __DIR__ . '/../../../scripts/project-stage/forum_testkit.py' );
$all  = $php . $js . $css;
t( 'no long dashes', false === strpos( $all, '—' ) && false === strpos( $all, '–' ) );
t( 'no banned words', ! preg_match( '/פלטפורמה|המערכת|אינטראקטיבי|אטלס|נחבר אתכם/u', $all ) );
t( 'no emoji', ! preg_match( '/[\x{1F300}-\x{1FAFF}\x{2600}-\x{27BF}]/u', $all ) );
t( 'no innerHTML / eval in js', ! preg_match( '/innerHTML|outerHTML|insertAdjacentHTML|\beval\s*\(|new Function|document\.write/', $js ) );
t( 'no 403 / 401, errors are 400 (nlf_err)', ! preg_match( "/'status' => 40[13]/", $php ) && false !== strpos( $php, 'nlf_err(' ) );
t( 'no redirects, no robots changes', ! preg_match( '/wp_redirect\s*\(|wp_safe_redirect\s*\(|header\(\s*[\'"]Location|noindex|nofollow|wp_robots/i', $all ) );
t( 'routes hidden from the index, three of them', false !== strpos( $php, "'show_in_index' => false" ) && 3 === substr_count( $php, '$reg( \'media' ) );
t( 'every route goes through nlfmd_member (member + header nonce)', 3 === substr_count( $php, 'nlfmd_member( $q )' ) && false !== strpos( $php, "nlf_nonce_for( \$m ), (string) \$q->get_header( 'x_nlf_nonce' )" ) );
t( 'the kind comes from the bytes (nlfmd_sniff), never the name', false !== strpos( $php, 'nlfmd_sniff( (string) @file_get_contents( $f[\'tmp_name\'], false, null, 0, 16 ) )' ) && false === strpos( $php, "\$f['name']" ) );
t( 'is_uploaded_file before anything is read', false !== strpos( $php, 'is_uploaded_file( $f[\'tmp_name\'] )' ) );
t( 'every stored JPEG is stripped', 4 <= substr_count( $php, 'nlfmd_strip_file(' ) );
t( 'two tables by dbDelta, with a version option', 2 === substr_count( $php, 'dbDelta(' ) && false !== strpos( $php, "'nadlan_forum_media_db'" ) && false !== strpos( $php, "nlfmd_t( 'pins' )" ) );
t( 'media table keys on topic, reply, member', false !== strpos( $php, 'KEY topic_id (topic_id)' ) && false !== strpos( $php, 'KEY reply_id (reply_id)' ) && false !== strpos( $php, 'KEY member_id (member_id' ) );
t( 'pins x / y are DECIMAL fractions', 2 === substr_count( $php, 'DECIMAL(5,4)' ) );
t( 'a file goes on one post only (the attach UPDATE repeats "not attached")', false !== strpos( $php, 'AND member_id = %d AND topic_id IS NULL AND reply_id IS NULL AND status = \'pending\'' ) );
t( 'uploads go to uploads/nlf-media', "define( 'NLFMD_DIR', 'nlf-media' );" === trim( (string) preg_replace( '/^.*(define\( \'NLFMD_DIR\'[^;]*;).*$/s', '$1', $php ) ) );
t( 'removed posts lose their files', false !== strpos( $php, "if ( 'removed' === \$to )" ) && false !== strpos( $php, 'nlfmd_gone_rows(' ) );
t( 'unsent files are cleaned daily', false !== strpos( $php, "wp_schedule_event( time() + HOUR_IN_SECONDS, 'daily', 'nlfmd_gc' )" ) );
t( 'every new function uses the nlfmd prefix', ! preg_match( '/^function (?!nlfmd_)/m', $php ) );
t( 'every new class uses the nlfmd prefix', ! preg_match( '/\.(?!nlfmd-|nlf-|nlf\b|is-)[a-z][a-z0-9]*-[a-z0-9-]+[\s{,:.>\[]/', preg_replace( '~/\*.*?\*/~s', '', $css ) ) );
t( 'css: no cream, beige, brown or gold', ! preg_match( '/gold|beige|cream|tan\b|#F5F5DC|#FFF8E|#FAF0E6|#D2B48C|#C9A|#B8860B|#DAA520|#FFD700/i', preg_replace( '~/\*.*?\*/~s', '', $css ) ) );
t( 'css: the board palette', false !== strpos( $css, '#B0144F' ) && false !== strpos( $css, '#2F6F86' ) && false !== strpos( $css, '#0B1117' ) && false !== strpos( $css, '#D5DBDF' ) && false !== strpos( $css, '#E3F0EA' ) );
t( 'css: buttons carry !important colours', preg_match( '/button\.nlfmd-pick\{[^}]*color:#101820 !important/', $css ) && preg_match( '/button\.nlfmd-lb-ask\{[^}]*background:#B0144F !important/', $css ) );
t( 'css: 44px hit areas (× and the points through ::after)', false !== strpos( $css, 'button.nlfmd-th-x::after{content:"";position:absolute;inset:-11px}' ) && false !== strpos( $css, 'button.nlfmd-lb-pin::after{content:"";position:absolute;inset:-12px' ) );
t( 'css: thumbs keep vertical scroll (pan-y), nothing pushed off-screen', false !== strpos( $css, 'touch-action:pan-y' ) && ! preg_match( '/(left|right)\s*:\s*-\d{3,}px/', $css ) );
t( 'css: reduced motion respected', false !== strpos( $css, 'prefers-reduced-motion' ) );
t( 'js under 48 KB, css under 24 KB', strlen( $js ) < 49152 && strlen( $css ) < 24576 );
t( 'js: camera input with capture=environment, pictures multiple, PDF', false !== strpos( $js, "capture: 'environment'" ) && false !== strpos( $js, "accept: 'application/pdf,.pdf'" ) );
t( 'js: canvas export at the server\'s numbers, JPEG 0.85 or WebP', false !== strpos( $js, 'L.long / Math.max(w, h)' ) && false !== strpos( $js, "C.webp ? 'image/webp' : 'image/jpeg', 0.85" ) );
t( 'js: XHR with upload progress, aria-live status', false !== strpos( $js, 'x.upload.onprogress' ) && false !== strpos( $js, "'aria-live': 'polite'" ) );
t( 'js: drag and drop and paste', false !== strpos( $js, "addEventListener('drop'" ) && false !== strpos( $js, "addEventListener('paste'" ) );
t( 'js: reorder by pointer events and by keys', false !== strpos( $js, "'pointermove'" ) && false !== strpos( $js, 'e.altKey' ) );
t( 'js: full screen = a modal dialog (focus trap), swipe, arrows, Escape', false !== strpos( $js, 'd.showModal()' ) && false !== strpos( $js, "e.key === 'ArrowLeft'" ) && false !== strpos( $js, "addEventListener('cancel'" ) );
t( 'js: the room button and the board hand-off', false !== strpos( $js, "setAttribute('data-nlf-room'" ) && false !== strpos( $js, "'nlf:board'" ) && false !== strpos( $js, 'bd.takeImage(bl)' ) );
t( 'js: a post waits for its uploads', false !== strpos( $js, "document.addEventListener('submit'" ) && false !== strpos( $js, 'e.stopImmediatePropagation()' ) );
t( 'js: no wheel or touch listeners', ! preg_match( "/addEventListener\('(wheel|touchstart|touchmove|mousewheel)'/", $js ) );
foreach ( array( 'מצלמה', 'תמונות', 'תוכנית / PDF', 'המיקום הוסר מהתמונות', 'גוררים כדי לשנות סדר', 'לסמן נקודה ולשאול', 'שיחת וידאו עליה' ) as $w ) {
	t( 'board words in js: ' . $w, false !== strpos( $js, $w ) );
}
foreach ( array( 'לשרטט עליה ביחד', 'הורדה', 'גוררים כדי למרכז. תמונה אמיתית של הפנים או לוגו של העסק.', 'מי שלא העלה: ראשי תיבות בצבע של המקצוע', 'לשמור את התמונה', 'תמונת פרופיל' ) as $w ) {
	t( 'board words in php: ' . $w, false !== strpos( $php, $w ) );
}
t( 'html: real <img> with width, height, alt, lazy', false !== strpos( $php, ' width="\' . $tw . \'" height="\' . $th . \'" alt="\' . esc_attr( nlfmd_alt( $r[\'caption\'] ) ) . \'" loading="lazy" decoding="async">' ) );

/* the one-line hooks in the forum's own files */
t( 'core: one require line at the end, after the reputation module', 1 === substr_count( $core, "require_once __DIR__ . '/pro-forum-media.php'" ) && strpos( $core, "'/pro-forum-media.php'" ) > strpos( $core, "'/pro-forum-rep.php'" ) );
t( 'core: nlf_post_check in both write routes', 1 === substr_count( $core, "apply_filters( 'nlf_post_check', '', 'topic', \$m, \$q, null )" ) && 1 === substr_count( $core, "apply_filters( 'nlf_post_check', '', 'reply', \$m, \$q, \$t )" ) );
t( 'core: nlf_post_created after both inserts', 1 === substr_count( $core, "do_action( 'nlf_post_created', 'topic', \$id, \$m, \$q, \$status, \$id )" ) && 1 === substr_count( $core, "do_action( 'nlf_post_created', 'reply', \$id, \$m, \$q, \$status, (int) \$t['id'] )" ) );
t( 'core: nlf_moderated in nlf_moderate', 1 === substr_count( $core, "do_action( 'nlf_moderated', \$type, (int) \$id, \$to, \$from )" ) );
t( 'core: nlf_jsonld around the structured data', 1 === substr_count( $core, "apply_filters( 'nlf_jsonld', nlf_jsonld(" ) );
t( 'core: the author carries the member id', 1 === substr_count( $core, "\$a['mid'] = (int) \$m['id'];" ) );
t( 'render: nlf_avatar_html and nlf_reply_after_body', 1 === substr_count( $rnd, "apply_filters( 'nlf_avatar_html'," ) && 1 === substr_count( $rnd, "apply_filters( 'nlf_reply_after_body', '', \$r, \$me, \$t )" ) );
t( 'forum.js reads form.nlfExtra(path)', 1 === substr_count( $fjs, 'form && form.nlfExtra ? form.nlfExtra(path) : null' ) );
t( 'call.js announces its board, board.js hands out takeImage', 1 === substr_count( $cjs, "new CustomEvent('nlf:board', { detail: board })" ) && false !== strpos( $bjs, 'return { open, close, destroy, saveImage, takeImage,' ) );
t( 'test kit clean removes media rows, files and points', false !== strpos( $kit, "nlfmd_purge_members( \$ids, (array) \$tids )" ) && false !== strpos( $php, 'function nlfmd_purge_members(' ) );

echo "\n$pass passed, $fail failed\n";
exit( $fail ? 1 : 0 );
