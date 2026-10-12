# -*- coding: utf-8 -*-
"""HAD-495 / 1.72.444: DealSign v2 on the local inc/deal-sign.php (Ben, 13.10.2026: Meital first approaches developers as a
regular broker; the showroom offer comes later). (1) the agreement has a kind: 'broker' (the brokerage agreement alone, the
default) or 'package' (with the advertising order); (2) the broker's office gets a "materials" tab: the owner uploads her
working files (admin REST /sg/file), each served only through its own 32-hex link (?nlsg_dl=), with byte ranges for video;
(3) Rainbow's asset line names lot 111. Run once; it refuses to run twice."""
import io
import os

P = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "plugins", "nadlan-config", "inc", "deal-sign.php")
s = io.open(P, encoding="utf-8").read()
if "nadlan_sg_rest_file" in s:
    raise SystemExit("already patched")


def rep(a, b, n=1):
    global s
    c = s.count(a)
    if c != n:
        raise SystemExit(f"x{c}: {a[:90]!r}")
    s = s.replace(a, b)


rep("'asset' => 'פרויקט ריינבו (Rainbow Tel Aviv), רובע שדה דב, תל אביב-יפו'",
    "'asset' => 'פרויקט ריינבו (Rainbow Tel Aviv), מגרש 111, רובע שדה דב, תל אביב-יפו'")
rep("משווקת יחידות דיור ומסחר בפרויקט, ומפרסמת אותו באתר nad-lan.co.il בהזמנה נפרדת; ",
    "משווקת יחידות דיור ומסחר בפרויקט{ADV}; ")
rep("			'{RATE}' => $e( 'rate' ),",
    "			'{ADV}' => 'package' === ( $d['kind'] ?? 'package' ) ? ', ומפרסמת אותו באתר nad-lan.co.il בהזמנה נפרדת' : '',\n			'{RATE}' => $e( 'rate' ),")
# the kind of a new agreement
rep("		$d = array(\n			'v' => 1, 'office' => $office,",
    "		$kind = 'package' === (string) $r->get_param( 'kind' ) ? 'package' : 'broker';\n		$d = array(\n			'v' => 2, 'kind' => $kind, 'office' => $office,")
# signing: the advertising order only in a package
rep("		if ( ! in_array( $plan, array( '1', '3', '6' ), true ) ) { return nadlan_sg_err( 'בחרו מסלול פרסום.' ); }\n		if ( ! $r->get_param( 'agree_a' ) || ! $r->get_param( 'agree_b' ) ) { return nadlan_sg_err( 'יש לאשר את שני המסמכים.' ); }",
    "		$pkg = 'package' === ( $d['kind'] ?? 'package' );\n		if ( $pkg && ! in_array( $plan, array( '1', '3', '6' ), true ) ) { return nadlan_sg_err( 'בחרו מסלול פרסום.' ); }\n		if ( ! $r->get_param( 'agree_a' ) || ( $pkg && ! $r->get_param( 'agree_b' ) ) ) { return nadlan_sg_err( $pkg ? 'יש לאשר את שני המסמכים.' : 'יש לאשר את ההסכם.' ); }")
rep("$d['devnum'] = $f['devnum']; $d['devaddr'] = $f['devaddr']; $d['plan'] = $plan;",
    "$d['devnum'] = $f['devnum']; $d['devaddr'] = $f['devaddr']; $d['plan'] = $pkg ? $plan : '';")
rep("$d['doc_a'] = nadlan_sg_doc_a( $d ); $d['doc_b'] = nadlan_sg_doc_b( $d );",
    "$d['doc_a'] = nadlan_sg_doc_a( $d ); $d['doc_b'] = $pkg ? nadlan_sg_doc_b( $d ) : '';")
rep("'hash_b' => hash( 'sha256', $d['doc_b'] ) ) );",
    "'hash_b' => $pkg ? hash( 'sha256', $d['doc_b'] ) : '' ) );")
# the signing page
rep("		$h = nadlan_sg_head( $d['pname'] . ' · ' . $d['bname'] . ', מתווכת מורשית, רישיון ' . $d['blic'], $signed ? 'ההסכם נחתם' : 'הסכם שיתוף פעולה לחתימה', $signed ? 'זה העותק החתום. שמרו את הקישור, או הדפיסו ושמרו כקובץ.' : 'שני מסמכים: ההסכם עם ' . esc_html( $d['bname'] ) . ' והזמנת הפרסום באתר. חתימה אחת, ועותק חתום לשני הצדדים.' );",
    "		$pkg = 'package' === ( $d['kind'] ?? 'package' );\n"
    "		$h = nadlan_sg_head( $d['pname'] . ' · ' . $d['bname'] . ', מתווכת מורשית, רישיון ' . $d['blic'], $signed ? 'ההסכם נחתם' : 'הסכם שיתוף פעולה לחתימה', $signed ? 'זה העותק החתום. שמרו את הקישור, או הדפיסו ושמרו כקובץ.' : ( $pkg ? 'שני מסמכים: ההסכם עם ' . esc_html( $d['bname'] ) . ' והזמנת הפרסום באתר. חתימה אחת, ועותק חתום לשני הצדדים.' : 'הסכם שיתוף הפעולה והזמנת שירותי התיווך עם ' . esc_html( $d['bname'] ) . '. עותק חתום לשני הצדדים.' ) );")
rep("			$h .= '<div class=\"card doc\"><div class=\"docbody\">' . $d['doc_b'] . '</div>",
    "			if ( '' !== (string) ( $d['doc_b'] ?? '' ) ) $h .= '<div class=\"card doc\"><div class=\"docbody\">' . $d['doc_b'] . '</div>")
rep("		$h .= '<div class=\"card doc\"><div class=\"kick\">מסמך 1 מתוך 2</div><div class=\"docbody\">' . nadlan_sg_doc_a( $d ) . '</div>' . $sigs . '</div>';\n		$h .= '<div class=\"card doc\"><div class=\"kick\">מסמך 2 מתוך 2</div><div class=\"docbody\">' . nadlan_sg_doc_b( $d ) . '</div></div>';",
    "		$h .= '<div class=\"card doc\">' . ( $pkg ? '<div class=\"kick\">מסמך 1 מתוך 2</div>' : '' ) . '<div class=\"docbody\">' . nadlan_sg_doc_a( $d ) . '</div>' . $sigs . '</div>';\n		if ( $pkg ) { $h .= '<div class=\"card doc\"><div class=\"kick\">מסמך 2 מתוך 2</div><div class=\"docbody\">' . nadlan_sg_doc_b( $d ) . '</div></div>'; }")
rep("			. '<div class=\"f\"><label>מסלול הפרסום</label>",
    "			. ( $pkg ? '<div class=\"f\"><label>מסלול הפרסום</label>")
rep("<small class=\"muted\">כולל מע״מ, כפי שמפורסם באתר.</small></div>'\n",
    "<small class=\"muted\">כולל מע״מ, כפי שמפורסם באתר.</small></div>' : '' )\n")
rep("			. '<label class=\"chk\"><input type=\"checkbox\" name=\"agree_b\" value=\"1\" required> קראתי את הזמנת הפרסום, ואני מוסמך/ת לחתום עליה בשם החברה.</label>'\n",
    "			. ( $pkg ? '<label class=\"chk\"><input type=\"checkbox\" name=\"agree_b\" value=\"1\" required> קראתי את הזמנת הפרסום, ואני מוסמך/ת לחתום עליה בשם החברה.</label>' : '' )\n")
rep("			. '<button class=\"btn\">חתימה על שני המסמכים</button>",
    "			. '<button class=\"btn\">' . ( $pkg ? 'חתימה על שני המסמכים' : 'חתימה על ההסכם' ) . '</button>")
# the office: the kind, and the materials tab first
rep("			. '<div class=\"f\"><label>לאן נשלחים רישומי לקוחות (מייל או וואטסאפ של החברה)</label><input name=\"regto\" required></div>'\n",
    "			. '<div class=\"f\"><label>לאן נשלחים רישומי לקוחות (מייל או וואטסאפ של החברה)</label><input name=\"regto\" required></div>'\n"
    "			. '<div class=\"f\"><label>סוג ההסכם</label><div class=\"plans\"><label><input type=\"radio\" name=\"kind\" value=\"broker\" checked> הסכם תיווך: רישום לקוחות ושכר תיווך על עסקה</label><label><input type=\"radio\" name=\"kind\" value=\"package\"> הסכם תיווך יחד עם הזמנת פרסום באתר (אולם התצוגה)</label></div></div>'\n")
rep("nadlan_sg_doc_a( array( 'bname' => $b['name'], 'blic' => $b['lic'], 'boffice' => $b['office'], 'dev' => '', 'asset' => '', 'rate' => '', 'regto' => '', 'bid' => '' ) )",
    "nadlan_sg_doc_a( array( 'kind' => 'broker', 'bname' => $b['name'], 'blic' => $b['lic'], 'boffice' => $b['office'], 'dev' => '', 'asset' => '', 'rate' => '', 'regto' => '', 'bid' => '' ) )")
rep("		$h .= '<main class=\"w\"><nav class=\"tabs\"><a href=\"#deals\" class=\"on\" data-tab=\"deals\">הסכמים</a><a href=\"#regs\" data-tab=\"regs\">רישום לקוח</a></nav>';\n		$h .= '<section id=\"deals\" class=\"tab on\">",
    "		$h .= '<main class=\"w\"><nav class=\"tabs\"><a href=\"#kit\" class=\"on\" data-tab=\"kit\">החומרים</a><a href=\"#deals\" data-tab=\"deals\">הסכמים</a><a href=\"#regs\" data-tab=\"regs\">רישום לקוח</a></nav>';\n"
    "		$h .= nadlan_sg_kit_tab( $tok );\n"
    "		$h .= '<section id=\"deals\" class=\"tab\">")
# routes and the download
rep("		register_rest_route( $ns, '/sg/admin',",
    "		register_rest_route( $ns, '/sg/file', array( 'methods' => 'POST', 'permission_callback' => function () { return current_user_can( 'manage_options' ); }, 'callback' => 'nadlan_sg_rest_file' ) );\n		register_rest_route( $ns, '/sg/admin',")
rep("	add_action( 'template_redirect', function () {\n		foreach ( array( 'nlsg_office', 'nlsg_sign', 'nlsg_rev' ) as $k ) {",
    "	add_action( 'template_redirect', function () {\n		if ( isset( $_GET['nlsg_dl'] ) ) { nadlan_sg_download( sanitize_text_field( wp_unslash( $_GET['nlsg_dl'] ) ) ); }\n		foreach ( array( 'nlsg_office', 'nlsg_sign', 'nlsg_rev' ) as $k ) {")
rep("		$out = array( 'deals' => array(), 'regs' => array() );",
    "		$out = array( 'deals' => array(), 'regs' => array(), 'files' => nadlan_sg_files() );")
KIT = r'''
	/* ------------------------------------------------------------------ the broker's materials (1.72.444) */

	function nadlan_sg_files() { $f = get_option( 'nadlan_sg_files', array() ); return is_array( $f ) ? $f : array(); }

	/** The private folder of the materials: a random name under uploads, never linked; files are served by nadlan_sg_download(). */
	function nadlan_sg_kitdir() {
		$u = wp_upload_dir( null, false );
		$k = (string) get_option( 'nadlan_sg_kitdir', '' );
		if ( ! preg_match( '/^nlsg-[a-f0-9]{32}$/', $k ) ) { $k = 'nlsg-' . nadlan_sg_token(); update_option( 'nadlan_sg_kitdir', $k, false ); }
		$dir = trailingslashit( $u['basedir'] ) . $k;
		if ( ! is_dir( $dir ) ) { wp_mkdir_p( $dir ); @file_put_contents( $dir . '/index.html', '' ); }
		return $dir;
	}

	/** Admin: put a file into a broker's materials (the same office and name replace it), or remove one. */
	function nadlan_sg_rest_file( WP_REST_Request $r ) {
		$files = nadlan_sg_files();
		$rm = nadlan_sg_valid( (string) $r->get_param( 'remove' ) );
		if ( $rm ) {
			if ( isset( $files[ $rm ] ) ) { @unlink( nadlan_sg_kitdir() . '/' . $rm . '.' . strtolower( pathinfo( $files[ $rm ]['name'], PATHINFO_EXTENSION ) ) ); unset( $files[ $rm ] ); update_option( 'nadlan_sg_files', $files, false ); }
			return array( 'ok' => true, 'removed' => $rm );
		}
		$office = nadlan_sg_valid( (string) $r->get_param( 'office' ) );
		if ( ! nadlan_sg_broker( $office ) ) { return nadlan_sg_err( 'no such office', 404 ); }
		$name = sanitize_file_name( (string) $r->get_param( 'name' ) );
		$ext = strtolower( pathinfo( $name, PATHINFO_EXTENSION ) );
		$types = array( 'pdf' => 'application/pdf', 'mp4' => 'video/mp4', 'jpg' => 'image/jpeg', 'png' => 'image/png', 'docx' => 'application/vnd.openxmlformats-officedocument.wordprocessingml.document' );
		if ( ! isset( $types[ $ext ] ) ) { return nadlan_sg_err( 'file type' ); }
		$raw = base64_decode( (string) $r->get_param( 'b64' ), true );
		if ( false === $raw || strlen( $raw ) < 100 ) { return nadlan_sg_err( 'no data' ); }
		$id = '';
		foreach ( $files as $fid => $f ) { if ( ( $f['office'] ?? '' ) === $office && ( $f['name'] ?? '' ) === $name ) { $id = $fid; } }
		if ( ! $id ) { $id = nadlan_sg_token(); }
		if ( false === @file_put_contents( nadlan_sg_kitdir() . '/' . $id . '.' . $ext, $raw ) ) { return nadlan_sg_err( 'write failed', 500 ); }
		$files[ $id ] = array( 'office' => $office, 'name' => $name, 'title' => nadlan_sg_txt( $r, 'title' ), 'desc' => nadlan_sg_txt( $r, 'desc', 500 ),
			'group' => nadlan_sg_txt( $r, 'group', 80 ), 'order' => (int) $r->get_param( 'order' ), 'mime' => $types[ $ext ], 'size' => strlen( $raw ),
			'md5' => md5( $raw ), 'at' => time(), 'dl' => (int) ( $files[ $id ]['dl'] ?? 0 ) );
		update_option( 'nadlan_sg_files', $files, false );
		return array( 'ok' => true, 'id' => $id, 'url' => nadlan_sg_url( 'nlsg_dl', $id ), 'md5' => md5( $raw ), 'size' => strlen( $raw ) );
	}

	/** One file, by its own link; byte ranges so a phone can play the video. */
	function nadlan_sg_download( $id ) {
		$id = nadlan_sg_valid( $id );
		$files = nadlan_sg_files();
		$f = $id && isset( $files[ $id ] ) ? $files[ $id ] : null;
		$path = $f ? nadlan_sg_kitdir() . '/' . $id . '.' . strtolower( pathinfo( $f['name'], PATHINFO_EXTENSION ) ) : '';
		if ( ! $f || ! is_readable( $path ) ) { status_header( 404 ); nocache_headers(); echo 'not found'; exit; }
		$size = (int) filesize( $path ); $start = 0; $end = $size - 1; $part = false;
		if ( isset( $_SERVER['HTTP_RANGE'] ) && preg_match( '/bytes=(\d*)-(\d*)/', (string) $_SERVER['HTTP_RANGE'], $m ) ) {
			if ( '' !== $m[1] ) { $start = (int) $m[1]; if ( '' !== $m[2] ) { $end = min( (int) $m[2], $size - 1 ); } } elseif ( '' !== $m[2] ) { $start = max( 0, $size - (int) $m[2] ); }
			if ( $start > $end || $start >= $size ) { status_header( 416 ); header( 'Content-Range: bytes */' . $size ); exit; }
			$part = true;
		}
		if ( 0 === $start ) { $files[ $id ]['dl'] = (int) ( $f['dl'] ?? 0 ) + 1; $files[ $id ]['last'] = time(); update_option( 'nadlan_sg_files', $files, false ); }
		while ( ob_get_level() ) { ob_end_clean(); }
		status_header( $part ? 206 : 200 );
		header( 'Content-Type: ' . $f['mime'] );
		header( 'Accept-Ranges: bytes' );
		header( 'Cache-Control: private, max-age=0, no-store' );
		header( 'X-Content-Type-Options: nosniff' );
		header( 'Referrer-Policy: no-referrer' );
		header( 'Content-Disposition: ' . ( isset( $_GET['save'] ) ? 'attachment' : 'inline' ) . "; filename*=UTF-8''" . rawurlencode( $f['name'] ) );
		if ( $part ) { header( 'Content-Range: bytes ' . $start . '-' . $end . '/' . $size ); }
		header( 'Content-Length: ' . ( $end - $start + 1 ) );
		$fp = fopen( $path, 'rb' ); fseek( $fp, $start ); $left = $end - $start + 1;
		while ( $left > 0 && ! feof( $fp ) ) { $c = fread( $fp, (int) min( 65536, $left ) ); echo $c; $left -= strlen( $c ); flush(); } // phpcs:ignore
		fclose( $fp );
		exit;
	}

	/** The materials tab of the office. */
	function nadlan_sg_kit_tab( $tok ) {
		$mine = array_filter( nadlan_sg_files(), function ( $f ) use ( $tok ) { return ( $f['office'] ?? '' ) === $tok; } );
		uasort( $mine, function ( $a, $b ) { return array( $a['order'] ?? 0, $a['title'] ?? '' ) <=> array( $b['order'] ?? 0, $b['title'] ?? '' ); } );
		$h = '<section id="kit" class="tab on">';
		if ( ! $mine ) { return $h . '<div class="card"><p class="muted">עוד אין חומרים.</p></div></section>'; }
		$group = null;
		foreach ( $mine as $id => $f ) {
			if ( $f['group'] !== $group ) {
				if ( null !== $group ) { $h .= '</div>'; }
				$group = $f['group'];
				$h .= '<div class="card"><h2>' . esc_html( $group ) . '</h2>';
			}
			$u = nadlan_sg_url( 'nlsg_dl', $id );
			$mb = $f['size'] >= 1048576 ? number_format( $f['size'] / 1048576, 1 ) . ' MB' : max( 1, (int) round( $f['size'] / 1024 ) ) . ' KB';
			$kind = 'video/mp4' === $f['mime'] ? 'סרטון' : ( 'application/pdf' === $f['mime'] ? 'PDF' : 'קובץ' );
			$h .= '<div class="kit"><div class="kt"><b>' . esc_html( $f['title'] ) . '</b><small>' . esc_html( $kind . ' · ' . $mb ) . '</small></div><p>' . esc_html( $f['desc'] ) . '</p>'
				. '<div class="ka"><a class="btn sm" href="' . esc_url( $u ) . '" target="_blank" rel="noopener">פתיחה</a><a class="btn sm ghost" href="' . esc_url( add_query_arg( 'save', '1', $u ) ) . '">הורדה</a>'
				. '<a class="btn sm ghost" href="' . esc_url( 'https://wa.me/?text=' . rawurlencode( $f['title'] . "\n" . $u ) ) . '" target="_blank" rel="noopener">שליחה בוואטסאפ</a></div></div>';
		}
		return $h . '</div></section>';
	}
'''
rep("	/* ------------------------------------------------------------------ pages */\n", KIT + "\n	/* ------------------------------------------------------------------ pages */\n")
rep(".msg{margin-top:12px;font-size:15px}",
    ".kit{border-top:1px solid var(--hair);padding:14px 0 4px}.kit:first-of-type{border-top:0}.kt{display:flex;justify-content:space-between;gap:12px;align-items:baseline}.kt b{font-size:17px}.kit p{margin:4px 0 10px;color:var(--ink2);font-size:15px}"
    ".ka{display:flex;flex-wrap:wrap;gap:8px}.btn.sm{min-height:42px;padding:9px 18px;font-size:15px;text-decoration:none;display:inline-flex;align-items:center}.btn.ghost{background:#fff;color:var(--ink);border:1px solid var(--hair)}\n.msg{margin-top:12px;font-size:15px}")
io.open(P, "w", encoding="utf-8", newline="\n").write(s)
print("patched", P)
