<?php
/**
 * nadlan-config - the apartment designer, server side (HAD-701; architecture in docs/architecture/apartment-designer/).
 *
 * DRAFT FOR REVIEW. Not loaded by the plugin until 'designer' is added to the module list in nadlan-config.php
 * (see docs/design-lab/apartment-designer/server/NOTES.md). Nothing here runs at load time except hook registration.
 *
 *  - nadlan_dsg_on()                    the master switch: option nadlan_designer_enabled = '1', or ?designer=next
 *  - nadlan_dsg_clean_design( $d )      strict cleaner for nadlan-unit-design v2 (design.schema.json)
 *  - nadlan_dsg_clean_points( $p )      cleaner for the planned services layer (points[]); not used yet
 *  - POST /nadlan/v1/designer/save      anonymous save and update, no personal details
 *  - GET  /nadlan/v1/designer/design/<id>  the saved design for whoever holds the share id
 *  - nadlan_dsg_plan_url( $p, $t )      a plan file from assets/designer/plans/index.json, '' when unknown
 *  - [nadlan_designer project="" type="" plan="" height=""]  the embed
 *
 * WHAT IS STORED (privacy): one private post per saved design (post type nadlan_design) holding the cleaned design JSON,
 * the project slug, the unit id, the plan's geometry revision, a save counter and the DAY it was last opened. No IP
 * address, no name, phone, email, user agent or cookie. The decision log keeps a role ("buyer", "rep", "designer",
 * "family"), never a person's name. The IP is used only inside a salted hash that names a short-lived rate-limit
 * transient (one hour at most) and is never written anywhere else. Designs not opened for 180 days are deleted by a
 * daily cron.
 */

if ( ! defined( 'ABSPATH' ) ) { exit; }

if ( ! defined( 'NADLAN_DSG_MAX_DESIGN' ) ) { define( 'NADLAN_DSG_MAX_DESIGN', 200 * 1024 ); } // bytes of the design as JSON
if ( ! defined( 'NADLAN_DSG_MAX_BODY' ) ) { define( 'NADLAN_DSG_MAX_BODY', 256 * 1024 ); }     // bytes of the whole request body
if ( ! defined( 'NADLAN_DSG_KEEP_DAYS' ) ) { define( 'NADLAN_DSG_KEEP_DAYS', 180 ); }
if ( ! defined( 'NADLAN_DSG_IMPORTMAP' ) ) {
	// Byte for byte the map inc/project-stage.php prints (same id, same three.js 0.170.0 URLs), so there is never a second one.
	define( 'NADLAN_DSG_IMPORTMAP', '<script type="importmap" id="nadlan-ps-importmap">{"imports":{"three":"https://cdn.jsdelivr.net/npm/three@0.170.0/build/three.module.js","three/addons/":"https://cdn.jsdelivr.net/npm/three@0.170.0/examples/jsm/"}}</script>' );
}

/* ------------------------------------------------------------------ switch */

if ( ! function_exists( 'nadlan_dsg_on' ) ) {
	/**
	 * The master switch. On only when the owner turned it on (option nadlan_designer_enabled = '1'), or when the request
	 * carries ?designer=next so the owner can test before opening it.
	 * Review note: ?designer=next is a preview switch, not a security boundary. Anyone who knows it can reach the embed and
	 * the two REST routes; every route below is safe for an anonymous visitor on its own (cleaner, limits, no personal data).
	 */
	function nadlan_dsg_on() {
		// 11.11.2026 (Ben: "publish the pages"): the embed is open wherever the shortcode is placed; the option set to '0' closes it.
		return '0' !== (string) get_option( 'nadlan_designer_enabled', '1' );
	}
}

if ( ! function_exists( 'nadlan_dsg_save_on' ) ) {
	/**
	 * The server save and the share link: CLOSED until the cleaner keeps everything the engine writes (points, added and
	 * removed partitions, room names). Open only with option nadlan_designer_save = '1', or ?designer=next for the owner's test.
	 * Until then a design lives in the visitor's own browser only.
	 */
	function nadlan_dsg_save_on() {
		if ( ! nadlan_dsg_on() ) { return false; }
		if ( '1' === (string) get_option( 'nadlan_designer_save', '0' ) ) { return true; }
		return isset( $_GET['designer'] ) && 'next' === (string) wp_unslash( $_GET['designer'] ); // phpcs:ignore WordPress.Security.NonceVerification
	}
}

/* ------------------------------------------------------------------ the cleaner */

if ( ! function_exists( 'nadlan_dsg_num' ) ) {
	/** a finite number clamped to [$lo, $hi] and rounded to $dp decimals; null when the value is not a number */
	function nadlan_dsg_num( $v, $lo, $hi, $dp = 1 ) {
		if ( is_bool( $v ) || ! is_numeric( $v ) ) { return null; }
		$v = (float) $v;
		if ( ! is_finite( $v ) ) { return null; }
		$v = round( max( $lo, min( $hi, $v ) ), $dp );
		return 0.0 === $v ? 0 : ( floor( $v ) === $v && abs( $v ) < 1e9 ? (int) $v : $v ); // whole numbers stay integers in the JSON
	}
}

if ( ! function_exists( 'nadlan_dsg_deg' ) ) {
	/** a rotation in degrees brought into [0, 360): periodic, never clamped (a clamp turns the piece; rfp.php learned this) */
	function nadlan_dsg_deg( $v ) {
		if ( is_bool( $v ) || ! is_numeric( $v ) ) { return null; }
		$v = (float) $v;
		if ( ! is_finite( $v ) ) { return null; }
		$d = round( fmod( fmod( $v, 360.0 ) + 360.0, 360.0 ), 1 );
		if ( $d >= 360.0 ) { $d = 0.0; }
		return floor( $d ) === $d ? (int) $d : $d;
	}
}

if ( ! function_exists( 'nadlan_dsg_id' ) ) {
	/** a string that matches $re exactly, or null. Nothing is repaired: a bad id is dropped, never rewritten into another id. */
	function nadlan_dsg_id( $v, $re ) {
		if ( ! is_string( $v ) && ! is_int( $v ) ) { return null; }
		$v = (string) $v;
		return 1 === preg_match( $re, $v ) ? $v : null;
	}
}

if ( ! function_exists( 'nadlan_dsg_text' ) ) {
	/** free text: valid UTF-8, no tags, no control characters except line breaks, at most $n characters */
	function nadlan_dsg_text( $v, $n ) {
		if ( ! is_string( $v ) && ! is_numeric( $v ) ) { return ''; }
		$s = mb_scrub( (string) $v, 'UTF-8' );
		$s = wp_strip_all_tags( $s );
		$s = preg_replace( '/[\x00-\x09\x0B\x0C\x0E-\x1F\x7F]/u', '', $s );
		$s = preg_replace( '/[<>]/u', '', (string) $s ); // a stray bracket left by a broken tag is not needed in a note
		return mb_substr( trim( (string) $s ), 0, $n, 'UTF-8' );
	}
}

if ( ! function_exists( 'nadlan_dsg_role' ) ) {
	/**
	 * The author of a log line or a note, reduced to a role. A personal name is never stored: anything that is not a
	 * known role (or a known alias of one) becomes 'buyer', the default the core itself writes when nobody is named.
	 * Review note: 'buyer' for an unknown author may misattribute a line; the alternative was dropping the line.
	 */
	function nadlan_dsg_role( $v ) {
		$map = array(
			'buyer' => 'buyer', 'client' => 'buyer', 'me' => 'buyer',
			'rep' => 'rep', 'agent' => 'rep', 'sales' => 'rep',
			'designer' => 'designer', 'architect' => 'designer',
			'family' => 'family', 'partner' => 'family', 'friend' => 'family',
		);
		$k = is_string( $v ) ? strtolower( trim( $v ) ) : '';
		return $map[ $k ] ?? 'buyer';
	}
}

if ( ! function_exists( 'nadlan_dsg_patterns' ) ) {
	/** every id pattern in one place, matching design.schema.json and apartment.schema.json */
	function nadlan_dsg_patterns() {
		return array(
			'project'  => '/^[a-z0-9][a-z0-9-]{0,79}$/',          // a project post slug (ascii; see NOTES open question)
			'unit'     => '/^[A-Za-z0-9_-]{1,96}$/',               // apartment.schema.json unit_id
			'georev'   => '/^[A-Za-z0-9._:-]{1,80}$/',             // design.schema.json geometry_revision
			'item'     => '/^[a-z0-9_-]{1,40}$/',                  // items[].id
			'sku'      => '/^[a-z0-9._-]{1,80}$/',
			'room'     => '/^[a-z0-9_-]{1,40}$/',                  // apartment.schema.json rooms[].id
			'wall'     => '/^[A-Za-z0-9_-]{1,40}$/',
			'finish_k' => '/^(floor|wall|ceiling|front|top):[A-Za-z0-9_:-]{1,60}$/',
			'finish_v' => '/^[a-z0-9_-]{1,80}$/',
			'gesture'  => '/^[A-Za-z0-9_.:-]{1,40}$/',
			'target'   => '/^[A-Za-z0-9_.:-]{1,60}$/',
			'time'     => '/^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(\.\d{1,6})?(Z|[+-]\d{2}:\d{2})$/',
		);
	}
}

if ( ! function_exists( 'nadlan_dsg_clean_item' ) ) {
	/** one piece of furniture; null when a required field is missing or bad */
	function nadlan_dsg_clean_item( $it ) {
		if ( ! is_array( $it ) ) { return null; }
		$P   = nadlan_dsg_patterns();
		$id  = nadlan_dsg_id( $it['id'] ?? null, $P['item'] );
		$sku = nadlan_dsg_id( $it['sku'] ?? null, $P['sku'] );
		$x   = nadlan_dsg_num( $it['x'] ?? null, -10000, 10000 );
		$y   = nadlan_dsg_num( $it['y'] ?? null, -10000, 10000 );
		$rot = nadlan_dsg_deg( $it['rot'] ?? null );
		if ( null === $id || null === $sku || null === $x || null === $y || null === $rot ) { return null; }
		$out = array( 'id' => $id, 'sku' => $sku, 'x' => $x, 'y' => $y, 'rot' => $rot );
		if ( array_key_exists( 'room', $it ) ) { $out['room'] = nadlan_dsg_id( $it['room'], $P['room'] ); } // null when outside or bad
		if ( isset( $it['status'] ) && in_array( $it['status'], array( 'base', 'upgrade', 'credit', 'decor', 'ai' ), true ) ) { $out['status'] = $it['status']; }
		if ( isset( $it['note'] ) ) { $n = nadlan_dsg_text( $it['note'], 200 ); if ( '' !== $n ) { $out['note'] = $n; } }
		return $out;
	}
}

if ( ! function_exists( 'nadlan_dsg_clean_op' ) ) {
	/** one operation of the decision log (design.schema.json $defs/op); null for an unknown or broken one */
	function nadlan_dsg_clean_op( $op ) {
		if ( ! is_array( $op ) || ! isset( $op['op'] ) || ! is_string( $op['op'] ) ) { return null; }
		$P = nadlan_dsg_patterns();
		switch ( $op['op'] ) {
			case 'item.add':
				$it = nadlan_dsg_clean_item( $op['item'] ?? null );
				return $it ? array( 'op' => 'item.add', 'item' => $it ) : null;
			case 'item.move':
				$id = nadlan_dsg_id( $op['id'] ?? null, $P['item'] );
				$x  = nadlan_dsg_num( $op['x'] ?? null, -10000, 10000 );
				$y  = nadlan_dsg_num( $op['y'] ?? null, -10000, 10000 );
				return ( null === $id || null === $x || null === $y ) ? null : array( 'op' => 'item.move', 'id' => $id, 'x' => $x, 'y' => $y );
			case 'item.rot':
				$id  = nadlan_dsg_id( $op['id'] ?? null, $P['item'] );
				$rot = nadlan_dsg_deg( $op['rot'] ?? null );
				return ( null === $id || null === $rot ) ? null : array( 'op' => 'item.rot', 'id' => $id, 'rot' => $rot );
			case 'item.remove':
				$id = nadlan_dsg_id( $op['id'] ?? null, $P['item'] );
				return null === $id ? null : array( 'op' => 'item.remove', 'id' => $id );
			case 'finish.set':
				$k = nadlan_dsg_id( $op['key'] ?? null, $P['finish_k'] );
				if ( null === $k || ! array_key_exists( 'value', $op ) ) { return null; }
				if ( null === $op['value'] ) { return array( 'op' => 'finish.set', 'key' => $k, 'value' => null ); }
				$v = nadlan_dsg_id( $op['value'], $P['finish_v'] );
				return null === $v ? null : array( 'op' => 'finish.set', 'key' => $k, 'value' => $v );
			case 'wall.shift':
				$id = nadlan_dsg_id( $op['id'] ?? null, $P['wall'] );
				$d  = nadlan_dsg_num( $op['d'] ?? null, -1000, 1000 );
				return ( null === $id || null === $d ) ? null : array( 'op' => 'wall.shift', 'id' => $id, 'd' => $d );
		}
		return null; // an operation this server does not know is dropped, never stored as it came
	}
}

if ( ! function_exists( 'nadlan_dsg_clean_design' ) ) {
	/**
	 * A nadlan-unit-design v2 document, whitelisted key by key. Returns the clean array or WP_Error.
	 * Refused outright: not an object, not v2, a bad geometry_revision, or more than 200 KB as JSON (measured on the input,
	 * so an oversize body is refused rather than silently cut). Everything else that is bad is dropped or capped:
	 * unknown keys, bad ids, oversize arrays (items 200, notes 80, log 400 newest, finishes 400, walls 400), tags in text.
	 * Version 1 documents are not this function's business: inc/rfp.php nadlan_rfp_clean_design reads them.
	 */
	function nadlan_dsg_clean_design( $d ) {
		if ( ! is_array( $d ) ) { return new WP_Error( 'design_type', 'the design must be an object', array( 'status' => 400 ) ); }
		$raw = wp_json_encode( $d, JSON_UNESCAPED_UNICODE | JSON_UNESCAPED_SLASHES ); // measured as UTF-8 text, so Hebrew is not counted six times
		if ( false === $raw || strlen( $raw ) > NADLAN_DSG_MAX_DESIGN ) { return new WP_Error( 'design_size', 'the design is larger than 200 KB', array( 'status' => 413 ) ); }
		if ( 'nadlan-unit-design' !== ( $d['schema'] ?? null ) || 2 !== (int) ( $d['v'] ?? 0 ) ) {
			return new WP_Error( 'design_version', 'only nadlan-unit-design v2 is accepted here', array( 'status' => 422 ) );
		}
		$P   = nadlan_dsg_patterns();
		$rev = nadlan_dsg_id( $d['geometry_revision'] ?? null, $P['georev'] );
		if ( null === $rev ) { return new WP_Error( 'design_revision', 'geometry_revision is missing or malformed', array( 'status' => 422 ) ); }

		$out = array(
			'schema'            => 'nadlan-unit-design',
			'v'                 => 2,
			'project'           => nadlan_dsg_id( $d['project'] ?? null, $P['project'] ),
			'unit_id'           => nadlan_dsg_id( $d['unit_id'] ?? null, $P['unit'] ),
			'geometry_revision' => $rev,
			'frame'             => array( 'units' => 'cm', 'origin' => 'plan-top-left', 'rot' => 'deg-cw' ), // the only frame v2 has
			'geometry'          => array( 'walls' => array() ),
			'finishes'          => array(),
			'items'             => array(),
			'notes'             => array(),
			'log'               => array(),
			'rev'               => 0,
		);

		$walls = is_array( $d['geometry']['walls'] ?? null ) ? $d['geometry']['walls'] : array();
		foreach ( array_slice( $walls, 0, 400, true ) as $k => $v ) {
			$k = nadlan_dsg_id( $k, $P['wall'] );
			$v = nadlan_dsg_num( $v, -1000, 1000 );
			if ( null !== $k && null !== $v && 0 !== $v ) { $out['geometry']['walls'][ $k ] = $v; } // zero = base place = absent (as core.js writes it)
		}

		$fin = is_array( $d['finishes'] ?? null ) ? $d['finishes'] : array();
		foreach ( array_slice( $fin, 0, 400, true ) as $k => $v ) {
			$k = nadlan_dsg_id( $k, $P['finish_k'] );
			$v = nadlan_dsg_id( $v, $P['finish_v'] );
			if ( null !== $k && null !== $v ) { $out['finishes'][ $k ] = $v; }
		}

		$seen = array();
		foreach ( array_slice( is_array( $d['items'] ?? null ) ? array_values( $d['items'] ) : array(), 0, 200 ) as $it ) {
			$c = nadlan_dsg_clean_item( $it );
			if ( ! $c || isset( $seen[ $c['id'] ] ) ) { continue; } // a second piece with the same id would break undo and the call
			$seen[ $c['id'] ] = true;
			$out['items'][]   = $c;
		}

		foreach ( array_slice( is_array( $d['notes'] ?? null ) ? array_values( $d['notes'] ) : array(), 0, 80 ) as $n ) {
			if ( ! is_array( $n ) ) { continue; }
			$text = nadlan_dsg_text( $n['text'] ?? '', 400 );
			if ( '' === $text ) { continue; }
			$tg   = is_array( $n['target'] ?? null ) ? $n['target'] : array();
			$kind = in_array( $tg['kind'] ?? '', array( 'room', 'wall', 'item', 'general' ), true ) ? $tg['kind'] : 'general';
			$tid  = 'general' === $kind ? null : nadlan_dsg_id( $tg['id'] ?? null, $P['target'] );
			$note = array( 'target' => null === $tid ? array( 'kind' => 'general' ) : array( 'kind' => $kind, 'id' => $tid ), 'text' => $text );
			if ( isset( $n['by'] ) ) { $note['by'] = nadlan_dsg_role( $n['by'] ); }
			$out['notes'][] = $note;
		}

		$log = is_array( $d['log'] ?? null ) ? array_values( $d['log'] ) : array();
		if ( count( $log ) > 400 ) { $log = array_slice( $log, -400 ); } // the newest 400 lines are the ones the spec sheet needs
		foreach ( $log as $e ) {
			if ( ! is_array( $e ) ) { continue; }
			$op = nadlan_dsg_clean_op( $e['op'] ?? null );
			$t  = nadlan_dsg_id( $e['t'] ?? null, $P['time'] );
			$nn = nadlan_dsg_num( $e['n'] ?? null, 0, 1000000000, 0 );
			if ( null === $op || null === $t || null === $nn ) { continue; }
			$out['log'][] = array(
				'n'       => (int) $nn,
				't'       => $t,
				'by'      => nadlan_dsg_role( $e['by'] ?? '' ),
				'op'      => $op,
				'gesture' => nadlan_dsg_id( $e['gesture'] ?? null, $P['gesture'] ),
			);
		}

		$r          = nadlan_dsg_num( $d['rev'] ?? 0, 0, 1000000000, 0 );
		$out['rev'] = null === $r ? 0 : (int) $r;

		$enc = wp_json_encode( $out, JSON_UNESCAPED_UNICODE | JSON_UNESCAPED_SLASHES );
		if ( false === $enc || strlen( $enc ) > NADLAN_DSG_MAX_DESIGN ) { return new WP_Error( 'design_size', 'the design is larger than 200 KB', array( 'status' => 413 ) ); }
		return $out;
	}
}

if ( ! function_exists( 'nadlan_dsg_clean_points' ) ) {
	/**
	 * The services layer that ARCHITECTURE.md section 10b asks for (electrical, communication, plumbing and air-conditioning
	 * points). Ready now so the cleaner does not change when the layer arrives; NOT called by anything yet.
	 * A point sits on a wall (wall id + distance from the wall's a-end + height), or on the ceiling or the floor (x, y).
	 * status: base = in the developer's plan, added / moved / removed = the buyer's change.
	 */
	function nadlan_dsg_clean_points( $pts ) {
		if ( ! is_array( $pts ) ) { return array(); }
		$kinds = array( 'socket', 'socket_double', 'switch', 'light', 'data', 'tv', 'phone', 'ac', 'ac_drain', 'water_cold', 'water_hot', 'drain', 'gas', 'intercom' );
		$P     = nadlan_dsg_patterns();
		$out   = array();
		$seen  = array();
		foreach ( array_slice( array_values( $pts ), 0, 300 ) as $p ) {
			if ( ! is_array( $p ) ) { continue; }
			$id   = nadlan_dsg_id( $p['id'] ?? null, $P['item'] );
			$kind = in_array( $p['kind'] ?? '', $kinds, true ) ? $p['kind'] : null;
			$host = in_array( $p['host'] ?? '', array( 'wall', 'ceiling', 'floor' ), true ) ? $p['host'] : null;
			if ( null === $id || null === $kind || null === $host || isset( $seen[ $id ] ) ) { continue; }
			$c = array( 'id' => $id, 'kind' => $kind, 'host' => $host );
			if ( 'wall' === $host ) {
				$c['wall'] = nadlan_dsg_id( $p['wall'] ?? null, $P['wall'] );
				$c['at']   = nadlan_dsg_num( $p['at'] ?? null, 0, 5000 );
				$c['h']    = nadlan_dsg_num( $p['h'] ?? 30, 0, 400 );
				if ( null === $c['wall'] || null === $c['at'] || null === $c['h'] ) { continue; }
			} else {
				$c['x'] = nadlan_dsg_num( $p['x'] ?? null, -10000, 10000 );
				$c['y'] = nadlan_dsg_num( $p['y'] ?? null, -10000, 10000 );
				if ( null === $c['x'] || null === $c['y'] ) { continue; }
			}
			$c['status'] = in_array( $p['status'] ?? '', array( 'base', 'added', 'moved', 'removed' ), true ) ? $p['status'] : 'added';
			$seen[ $id ] = true;
			$out[]       = $c;
		}
		return $out;
	}
}

/* ------------------------------------------------------------------ ids, keys, limits */

if ( ! function_exists( 'nadlan_dsg_new_id' ) ) {
	/** 26 random base32 characters (a-z, 2-7): 130 bits, URL-safe, lowercase so it survives as a post_name unchanged */
	function nadlan_dsg_new_id() {
		$alpha = 'abcdefghijklmnopqrstuvwxyz234567';
		$bits  = '';
		foreach ( str_split( random_bytes( 17 ) ) as $b ) { $bits .= str_pad( decbin( ord( $b ) ), 8, '0', STR_PAD_LEFT ); }
		$out = '';
		for ( $i = 0; $i < 26; $i++ ) { $out .= $alpha[ bindec( substr( $bits, $i * 5, 5 ) ) ]; }
		return $out;
	}
}

if ( ! function_exists( 'nadlan_dsg_valid_id' ) ) {
	function nadlan_dsg_valid_id( $id ) { return is_string( $id ) && 1 === preg_match( '/^[a-z2-7]{26}$/', $id ); }
}

if ( ! function_exists( 'nadlan_dsg_edit_key' ) ) {
	/**
	 * The edit key of a design id. HOW IT WORKS: key = HMAC-SHA256( 'nadlan-dsg-edit|' . id, wp_salt('auth') . a fixed
	 * pepper ), first 32 hex characters (128 bits). It is returned ONCE, to the browser that created the design, and is
	 * never stored: the server recomputes it on every update and compares with hash_equals. The id alone (the share link)
	 * can read but not change. Consequence: rotating the WordPress salts turns every saved design read-only (they stay
	 * readable; a new save makes a new id).
	 */
	function nadlan_dsg_edit_key( $id ) {
		return substr( hash_hmac( 'sha256', 'nadlan-dsg-edit|' . (string) $id, wp_salt( 'auth' ) . 'nadlan-designer-v2' ), 0, 32 );
	}
}

if ( ! function_exists( 'nadlan_dsg_key_ok' ) ) {
	function nadlan_dsg_key_ok( $id, $key ) {
		if ( ! nadlan_dsg_valid_id( $id ) || ! is_string( $key ) || 1 !== preg_match( '/^[a-f0-9]{32}$/', $key ) ) { return false; }
		return hash_equals( nadlan_dsg_edit_key( $id ), $key );
	}
}

if ( ! function_exists( 'nadlan_dsg_rl' ) ) {
	/**
	 * A fixed-window rate limit per visitor. The transient's NAME is an HMAC of (bucket, IP, window) under the site salt,
	 * so the IP is never stored, not even as a plain hash that could be reversed by trying all IPv4 addresses; the
	 * transient lives one window at most. Review note: REMOTE_ADDR only (as together.php), never X-Forwarded-For, which a
	 * visitor can write; if uPress puts a proxy in front, check that REMOTE_ADDR is the visitor (see NOTES).
	 */
	function nadlan_dsg_rl( $bucket, $max, $window ) {
		$ip = isset( $_SERVER['REMOTE_ADDR'] ) ? (string) $_SERVER['REMOTE_ADDR'] : '0'; // phpcs:ignore
		$k  = 'nldsg_rl_' . substr( hash_hmac( 'sha256', $bucket . '|' . $ip . '|' . (int) floor( time() / $window ), wp_salt( 'nonce' ) ), 0, 32 );
		$n  = (int) get_transient( $k );
		if ( $n >= $max ) { return false; }
		set_transient( $k, $n + 1, $window );
		return true;
	}
}

if ( ! function_exists( 'nadlan_dsg_write_refusal' ) ) {
	/**
	 * Why a write request is refused, or '' when it may go on. $h: header name (lowercase, '_' for '-') => value.
	 *
	 * WHY NO NONCE: the visitors are anonymous and the pages are cached, so a nonce would be stale or shared between
	 * visitors; and the route changes nothing that belongs to anybody except through the edit key. What a nonce would
	 * stop (a cross-site form posting into the route) is stopped here instead:
	 *  - the custom header X-NL-Designer: 1 cannot be sent by a form, and a cross-site fetch that sets it needs a CORS
	 *    preflight that WordPress does not grant for this route;
	 *  - the body must be application/json (a form can send only urlencoded, multipart or text/plain);
	 *  - Sec-Fetch-Site, when the browser sends it, must be same-origin; Origin, when sent, must be this site's host.
	 */
	function nadlan_dsg_write_refusal( array $h, $len, $home_host ) {
		if ( '1' !== trim( (string) ( $h['x_nl_designer'] ?? '' ) ) ) { return 'header'; }
		if ( 0 !== stripos( trim( (string) ( $h['content_type'] ?? '' ) ), 'application/json' ) ) { return 'json'; }
		if ( (int) $len > NADLAN_DSG_MAX_BODY ) { return 'size'; }
		$sfs = strtolower( trim( (string) ( $h['sec_fetch_site'] ?? '' ) ) );
		if ( '' !== $sfs && 'same-origin' !== $sfs ) { return 'site'; }
		$origin = trim( (string) ( $h['origin'] ?? '' ) );
		if ( '' !== $origin ) {
			$oh = strtolower( (string) wp_parse_url( $origin, PHP_URL_HOST ) );
			if ( '' === $oh || $oh !== strtolower( (string) $home_host ) ) { return 'origin'; }
		}
		return '';
	}
}

if ( ! function_exists( 'nadlan_dsg_err' ) ) {
	function nadlan_dsg_err( $code, $status ) { return new WP_Error( 'nadlan_dsg_' . $code, $code, array( 'status' => $status ) ); }
}

if ( ! function_exists( 'nadlan_dsg_no_store' ) ) {
	function nadlan_dsg_no_store( $data, $status = 200 ) {
		$r = new WP_REST_Response( $data, $status );
		$r->header( 'Cache-Control', 'no-store, max-age=0' );
		$r->header( 'X-Robots-Tag', 'noindex, nofollow' );
		return $r;
	}
}

/* ------------------------------------------------------------------ storage */

add_action( 'init', function () {
	register_post_type( 'nadlan_design', array(
		'labels'              => array( 'name' => 'עיצובי דירה שמורים', 'singular_name' => 'עיצוב דירה' ),
		'public'              => false,
		'publicly_queryable'  => false,
		'exclude_from_search' => true,
		'show_ui'             => false,
		'show_in_rest'        => false,
		'show_in_nav_menus'   => false,
		'rewrite'             => false,
		'query_var'           => false,
		'can_export'          => false,
		'supports'            => array( 'title' ), // no 'revisions': an update does not keep old copies
	) );
	if ( ! wp_next_scheduled( 'nadlan_dsg_cleanup' ) ) {
		wp_schedule_event( time() + HOUR_IN_SECONDS, 'daily', 'nadlan_dsg_cleanup' );
	}
}, 20 );

/* retention: a design not opened (read or saved) for 180 days is deleted, 200 a day at most. Runs whether the switch is on or off. */
add_action( 'nadlan_dsg_cleanup', function () {
	$ids = get_posts( array(
		'post_type'        => 'nadlan_design',
		'post_status'      => 'any',
		'fields'           => 'ids',
		'numberposts'      => 400,
		'no_found_rows'    => true,
		'suppress_filters' => true,
		'meta_query'       => array( array( 'key' => '_dsg_seen', 'value' => time() - NADLAN_DSG_KEEP_DAYS * DAY_IN_SECONDS, 'compare' => '<', 'type' => 'NUMERIC' ) ),
	) );
	foreach ( (array) $ids as $id ) { if ( 'nadlan_design' !== get_post_type( (int) $id ) ) { continue; } wp_delete_post( (int) $id, true ); }
} );

if ( ! function_exists( 'nadlan_dsg_find' ) ) {
	function nadlan_dsg_find( $id ) {
		if ( ! nadlan_dsg_valid_id( $id ) ) { return 0; }
		$q = get_posts( array(
			'post_type' => 'nadlan_design', 'post_status' => 'private', 'name' => $id, 'numberposts' => 1,
			'fields' => 'ids', 'no_found_rows' => true, 'suppress_filters' => true,
		) );
		return $q ? (int) $q[0] : 0;
	}
}

if ( ! function_exists( 'nadlan_dsg_touch' ) ) {
	/** "last opened", kept to the day (less precise on purpose, and at most one write a day per design) */
	function nadlan_dsg_touch( $pid ) {
		$day = (int) ( floor( time() / DAY_IN_SECONDS ) * DAY_IN_SECONDS );
		if ( (int) get_post_meta( $pid, '_dsg_seen', true ) !== $day ) { update_post_meta( $pid, '_dsg_seen', $day ); }
	}
}

if ( ! function_exists( 'nadlan_dsg_encode' ) ) {
	/** stored JSON without < > & ' " characters, so the kses filter WordPress runs on post_content for anonymous
	 *  visitors has nothing to change in it */
	function nadlan_dsg_encode( $design ) {
		return wp_json_encode( $design, JSON_HEX_TAG | JSON_HEX_AMP | JSON_HEX_APOS | JSON_HEX_QUOT | JSON_UNESCAPED_SLASHES );
	}
}

/* ------------------------------------------------------------------ REST */

if ( ! function_exists( 'nadlan_dsg_rest_save' ) ) {
	/** POST /nadlan/v1/designer/save  body { design, id?, key?, base_rev? } */
	function nadlan_dsg_rest_save( WP_REST_Request $req ) {
		if ( ! nadlan_dsg_save_on() ) { return nadlan_dsg_err( 'off', 404 ); }
		$h = array();
		foreach ( array( 'x_nl_designer', 'content_type', 'sec_fetch_site', 'origin' ) as $n ) { $h[ $n ] = (string) $req->get_header( $n ); }
		$why = nadlan_dsg_write_refusal( $h, strlen( (string) $req->get_body() ), (string) wp_parse_url( home_url(), PHP_URL_HOST ) );
		if ( '' !== $why ) { return nadlan_dsg_err( $why, 'size' === $why ? 413 : 403 ); }
		if ( ! nadlan_dsg_rl( 'save', 20, HOUR_IN_SECONDS ) ) { return nadlan_dsg_err( 'rate', 429 ); }
		$p = $req->get_json_params();
		if ( ! is_array( $p ) ) { return nadlan_dsg_err( 'body', 400 ); }
		$design = nadlan_dsg_clean_design( $p['design'] ?? null );
		if ( is_wp_error( $design ) ) { return $design; }
		$json = nadlan_dsg_encode( $design );

		$id = isset( $p['id'] ) ? (string) $p['id'] : '';
		if ( '' !== $id ) { // an update: only the holder of the edit key, only the same apartment
			if ( ! nadlan_dsg_key_ok( $id, (string) ( $p['key'] ?? '' ) ) ) { return nadlan_dsg_err( 'key', 403 ); }
			$pid = nadlan_dsg_find( $id );
			if ( ! $pid ) { return nadlan_dsg_err( 'gone', 404 ); }
			// Review note: a share link must keep showing the same apartment, so the project, unit and plan revision of a
			// saved design cannot change; a design for another unit or a redrawn plan is a new save with a new id.
			if ( (string) get_post_meta( $pid, '_dsg_project', true ) !== (string) $design['project']
				|| (string) get_post_meta( $pid, '_dsg_unit', true ) !== (string) $design['unit_id']
				|| (string) get_post_meta( $pid, '_dsg_georev', true ) !== $design['geometry_revision'] ) {
				return nadlan_dsg_err( 'other_unit', 409 );
			}
			$saves = (int) get_post_meta( $pid, '_dsg_saves', true );
			if ( isset( $p['base_rev'] ) && (int) $p['base_rev'] !== $saves ) { return nadlan_dsg_err( 'stale', 409 ); } // optional: a second tab
			$r = wp_update_post( array( 'ID' => $pid, 'post_content' => wp_slash( $json ) ), true );
			if ( is_wp_error( $r ) ) { return nadlan_dsg_err( 'store', 500 ); }
			update_post_meta( $pid, '_dsg_saves', $saves + 1 );
			nadlan_dsg_touch( $pid );
			return nadlan_dsg_no_store( array( 'ok' => true, 'id' => $id, 'rev' => $saves + 1 ) );
		}

		// a new design: a site-wide ceiling per day as well, so many addresses together cannot fill the database
		$day_k = 'nldsg_day_' . gmdate( 'Ymd' );
		$day_n = (int) get_transient( $day_k );
		if ( $day_n >= (int) apply_filters( 'nadlan_dsg_daily_cap', 300 ) ) { return nadlan_dsg_err( 'rate', 429 ); }
		set_transient( $day_k, $day_n + 1, DAY_IN_SECONDS );
		$id  = nadlan_dsg_new_id();
		$pid = wp_insert_post( array(
			'post_type'    => 'nadlan_design',
			'post_status'  => 'private',
			'post_author'  => 0,
			'post_name'    => $id,
			'post_title'   => 'design ' . substr( $id, 0, 6 ),
			'post_content' => wp_slash( $json ),
		), true );
		if ( is_wp_error( $pid ) || ! $pid ) { return nadlan_dsg_err( 'store', 500 ); }
		update_post_meta( $pid, '_dsg_project', (string) $design['project'] );
		update_post_meta( $pid, '_dsg_unit', (string) $design['unit_id'] );
		update_post_meta( $pid, '_dsg_georev', $design['geometry_revision'] );
		update_post_meta( $pid, '_dsg_saves', 1 );
		nadlan_dsg_touch( $pid );
		return nadlan_dsg_no_store( array( 'ok' => true, 'id' => $id, 'key' => nadlan_dsg_edit_key( $id ), 'rev' => 1 ), 201 );
	}
}

if ( ! function_exists( 'nadlan_dsg_rest_read' ) ) {
	/** GET /nadlan/v1/designer/design/<id> : a share link, readable by whoever holds the id; never the edit key */
	function nadlan_dsg_rest_read( WP_REST_Request $req ) {
		if ( ! nadlan_dsg_save_on() ) { return nadlan_dsg_err( 'off', 404 ); }
		if ( ! nadlan_dsg_rl( 'read', 120, MINUTE_IN_SECONDS ) ) { return nadlan_dsg_err( 'rate', 429 ); }
		$id  = (string) $req['id'];
		$pid = nadlan_dsg_find( $id );
		if ( ! $pid ) { return nadlan_dsg_err( 'gone', 404 ); }
		$design = json_decode( (string) get_post_field( 'post_content', $pid ), true );
		if ( ! is_array( $design ) ) { return nadlan_dsg_err( 'gone', 410 ); }
		nadlan_dsg_touch( $pid );
		return nadlan_dsg_no_store( array(
			'design'            => $design,
			'project'           => $design['project'] ?? null,
			'unit_id'           => $design['unit_id'] ?? null,
			'geometry_revision' => $design['geometry_revision'] ?? '',
			'saved'             => mysql2date( 'c', (string) get_post_field( 'post_modified_gmt', $pid ), false ),
			'rev'               => (int) get_post_meta( $pid, '_dsg_saves', true ),
		) );
	}
}

add_action( 'rest_api_init', function () {
	register_rest_route( 'nadlan/v1', '/designer/save', array(
		'methods' => 'POST', 'permission_callback' => '__return_true', 'callback' => 'nadlan_dsg_rest_save',
	) );
	register_rest_route( 'nadlan/v1', '/designer/design/(?P<id>[a-z2-7]{26})', array(
		'methods' => 'GET', 'permission_callback' => '__return_true', 'callback' => 'nadlan_dsg_rest_read',
	) );
} );

/* ------------------------------------------------------------------ plans */

if ( ! function_exists( 'nadlan_dsg_plans_dir' ) ) {
	function nadlan_dsg_plans_dir() {
		return (string) apply_filters( 'nadlan_dsg_plans_dir', dirname( __DIR__ ) . '/assets/designer/plans' ); // filter for tests only
	}
}

if ( ! function_exists( 'nadlan_dsg_plans_index' ) ) {
	/**
	 * plans/index.json : { "plans": { "<project slug>": { "<type>": "<file>.json" } } }. Parsed once per version of the file
	 * (the transient name carries the file's mtime and size), so an upload of a new index is read at once.
	 */
	function nadlan_dsg_plans_index() {
		$f = nadlan_dsg_plans_dir() . '/index.json';
		if ( ! is_readable( $f ) ) { return array(); }
		$k   = 'nldsg_plans_' . md5( $f . '|' . (int) filemtime( $f ) . '|' . (int) filesize( $f ) );
		$hit = get_transient( $k );
		if ( is_array( $hit ) ) { return $hit; }
		$j   = json_decode( (string) file_get_contents( $f ), true );
		$idx = array();
		foreach ( ( is_array( $j['plans'] ?? null ) ? $j['plans'] : array() ) as $pk => $row ) {
			if ( is_array( $row ) && isset( $row['file'] ) ) { // the list form: { id, file, project, type }
				if ( ! empty( $row['project'] ) && ! empty( $row['type'] ) && is_string( $row['project'] ) && is_string( $row['type'] ) && is_string( $row['file'] ) ) { $idx[ $row['project'] ][ $row['type'] ] = $row['file']; }
			} elseif ( is_string( $pk ) && is_array( $row ) ) { // the map form: project => { type => file }
				$idx[ $pk ] = $row;
			}
		}
		set_transient( $k, $idx, DAY_IN_SECONDS );
		return $idx;
	}
}

if ( ! function_exists( 'nadlan_dsg_plan_file' ) ) {
	/** a plan file name inside plans/ that exists, or ''. Only a plain name: no slash, no '..', no other extension. */
	function nadlan_dsg_plan_file( $name ) {
		if ( ! is_string( $name ) || 1 !== preg_match( '/^([a-z0-9][a-z0-9-]{0,79}\/)?[A-Za-z0-9][A-Za-z0-9_-]{0,79}(\.[a-z0-9_-]{1,40})?\.json$/', $name ) || 'index.json' === $name ) { return ''; } // one folder level (plans/<project>/<type>.json); realpath below still refuses anything outside plans/
		$dir  = realpath( nadlan_dsg_plans_dir() );
		$path = realpath( nadlan_dsg_plans_dir() . '/' . $name );
		if ( ! $dir || ! $path || 0 !== strpos( $path, $dir . DIRECTORY_SEPARATOR ) || ! is_file( $path ) ) { return ''; }
		return $name;
	}
}

if ( ! function_exists( 'nadlan_dsg_plan_url' ) ) {
	/** the plan of one unit type of one project, as a URL; '' when the index does not name it. Never a neighbour's plan. */
	function nadlan_dsg_plan_url( $project, $type ) {
		$P = nadlan_dsg_patterns();
		if ( null === nadlan_dsg_id( $project, $P['project'] ) || ! is_string( $type ) || 1 !== preg_match( '/^[A-Za-z0-9_-]{1,40}$/', $type ) ) { return ''; }
		$idx  = nadlan_dsg_plans_index();
		$row  = is_array( $idx[ $project ] ?? null ) ? $idx[ $project ] : array();
		$file = isset( $row[ $type ] ) && is_string( $row[ $type ] ) ? nadlan_dsg_plan_file( $row[ $type ] ) : ''; // exact type only
		return '' === $file ? '' : nadlan_dsg_asset_url( 'plans/' . $file );
	}
}

if ( ! function_exists( 'nadlan_dsg_asset_url' ) ) {
	function nadlan_dsg_asset_url( $rel ) {
		$v = defined( 'NADLAN_CONFIG_VERSION' ) ? NADLAN_CONFIG_VERSION : '0';
		return plugins_url( 'assets/designer/' . $rel, dirname( __FILE__ ) ) . '?v=' . rawurlencode( $v );
	}
}

/* ------------------------------------------------------------------ the embed */

if ( ! function_exists( 'nadlan_dsg_stage_has_map' ) ) {
	/** inc/project-stage.php prints its import map in wp_head on every stage page */
	function nadlan_dsg_stage_has_map() {
		return function_exists( 'nadlan_ps_current' ) && (bool) nadlan_ps_current();
	}
}

if ( ! function_exists( 'nadlan_dsg_print_importmap' ) ) {
	/** the import map, at most once per page and never when the stage already printed it */
	function nadlan_dsg_print_importmap() {
		if ( ! empty( $GLOBALS['nadlan_dsg_map_done'] ) || nadlan_dsg_stage_has_map() ) { return ''; }
		$GLOBALS['nadlan_dsg_map_done'] = true;
		return NADLAN_DSG_IMPORTMAP . "\n";
	}
}

/* best place for the map is <head>, before any module script: on a page whose content holds the shortcode and that has no
 * stage of its own. Priority 30, after the stage's own wp_head hook. The shortcode prints it in the body only as a fallback. */
add_action( 'wp_head', function () {
	if ( ! is_singular() || ! nadlan_dsg_on() ) { return; }
	$post = get_post();
	if ( ! $post || ! has_shortcode( (string) $post->post_content, 'nadlan_designer' ) ) { return; }
	echo nadlan_dsg_print_importmap(); // phpcs:ignore WordPress.Security.EscapeOutput -- a fixed constant
}, 30 );

if ( ! function_exists( 'nadlan_dsg_embed_config' ) ) {
	/** what the page passes to the designer; filter nadlan_dsg_embed_config lets a project page add { project, type, unitLabel, lang } */
	function nadlan_dsg_embed_config( $atts ) {
		$cfg = array(
			'project'   => (string) ( $atts['project'] ?? '' ),
			'type'      => (string) ( $atts['type'] ?? '' ),
			'unitLabel' => '',
			'lang'      => 'he',
			'title'     => '',
		);
		$cfg = apply_filters( 'nadlan_dsg_embed_config', $cfg, $atts );
		$cfg = is_array( $cfg ) ? $cfg : array();
		$P   = nadlan_dsg_patterns();
		return array( // whatever a filter returned is cleaned again
			'project'   => (string) nadlan_dsg_id( (string) ( $cfg['project'] ?? '' ), $P['project'] ),
			'type'      => 1 === preg_match( '/^[A-Za-z0-9_-]{1,40}$/', (string) ( $cfg['type'] ?? '' ) ) ? (string) $cfg['type'] : '',
			'unitLabel' => nadlan_dsg_text( $cfg['unitLabel'] ?? '', 80 ),
			'lang'      => in_array( ( $cfg['lang'] ?? '' ), array( 'he', 'en', 'fr', 'ru', 'ar' ), true ) ? $cfg['lang'] : 'he',
			'title'     => nadlan_dsg_text( $cfg['title'] ?? '', 80 ),
		);
	}
}

if ( ! function_exists( 'nadlan_dsg_shortcode' ) ) {
	function nadlan_dsg_shortcode( $atts ) {
		if ( ! nadlan_dsg_on() ) { return ''; }
		if ( ! empty( $GLOBALS['nadlan_dsg_n'] ) ) { return ''; } // one designer per page: two would share ?design= and the browser's saved design
		$atts = shortcode_atts( array( 'project' => '', 'type' => '', 'plan' => '', 'plans' => '', 'height' => '' ), $atts, 'nadlan_designer' );
		$cfg  = nadlan_dsg_embed_config( $atts );

		// plans="example-3r,example-4r,example-5r": the visitor picks one of several plans with buttons above the designer.
		// Each name is a plan file in plans/ (the same check as plan=""); the label is the plan's own rooms count.
		$choices = array();
		foreach ( array_slice( array_filter( array_map( 'trim', explode( ',', (string) $atts['plans'] ) ) ), 0, 6 ) as $nm ) {
			$f = nadlan_dsg_plan_file( $nm . '.json' );
			if ( '' === $f ) { continue; }
			$pj = json_decode( (string) file_get_contents( nadlan_dsg_plans_dir() . '/' . $f ), true );
			$rooms = 0;
			foreach ( ( is_array( $pj['rooms'] ?? null ) ? $pj['rooms'] : array() ) as $rm ) { if ( in_array( $rm['type'] ?? '', array( 'living', 'bedroom', 'master', 'kids', 'study', 'mamad', 'room' ), true ) ) { $rooms++; } }
			if ( 1 === preg_match( '/-(\d)r$/', $nm, $mm ) ) { $rooms = (int) $mm[1]; }
			$choices[] = array( 'url' => nadlan_dsg_asset_url( 'plans/' . $f ), 'label' => $rooms ? $rooms . ' חדרים' : $nm );
		}

		// which plan: an explicit file in plans/, else the index for project + type, else (only on a page that names no
		// project) the example flat, which labels itself "דירה לדוגמה". A project whose plan is unknown shows nothing:
		// an example drawn on a real project's page would read as that project's apartment.
		$plan = '' !== (string) $atts['plan'] ? nadlan_dsg_plan_file( (string) $atts['plan'] ) : '';
		$url  = '' !== $plan ? nadlan_dsg_asset_url( 'plans/' . $plan ) : '';
		if ( '' === $url && '' !== $cfg['project'] ) {
			$url = nadlan_dsg_plan_url( $cfg['project'], $cfg['type'] );
			if ( '' === $url ) { return '<!-- nadlan-designer: no plan for this project and type -->'; }
		}
		if ( '' === $url && count( $choices ) > 1 ) { $url = $choices[ min( 1, count( $choices ) - 1 ) ]['url']; } // open on the second choice (4 rooms)
		if ( '' === $url ) { $url = nadlan_dsg_asset_url( 'plans/example-4r.json' ); }

		$h = (string) $atts['height'];
		if ( 1 === preg_match( '/^(\d{2,4})(px|vh)?$/', $h, $m ) ) {
			$h = (int) $m[1] . ( empty( $m[2] ) ? 'px' : $m[2] );
		} else {
			$h = '86vh';
		}

		// THE SEND BUTTON (marked for review): today it saves anonymously and shows the share link. Connecting it to the
		// lead and request path (/nadlan/v1/lead then /nadlan/v1/rfp) is a later, reviewed step. A plugin can name a global
		// JS function instead (for example 'NadlanLead.sendDesign'); it is called with (designer, receipt) after the save.
		$send = (string) apply_filters( 'nadlan_dsg_send_handler', 'share', $cfg );
		$send = 'share' === $send || 1 === preg_match( '/^[A-Za-z_$][A-Za-z0-9_$]{0,40}(\.[A-Za-z_$][A-Za-z0-9_$]{0,40}){0,3}$/', $send ) ? $send : 'share';

		$GLOBALS['nadlan_dsg_n'] = (int) ( $GLOBALS['nadlan_dsg_n'] ?? 0 ) + 1;
		$host = 'nldsg-' . $GLOBALS['nadlan_dsg_n'];
		$js   = array(
			'host'    => $host,
			'module'  => nadlan_dsg_asset_url( 'designer.js' ),
			'planUrl' => $url,
			'rest'    => rest_url( 'nadlan/v1/designer/' ),
			'test'    => '1' !== (string) get_option( 'nadlan_designer_save', '0' ), // while the save is closed for the public, REST calls carry ?designer=next
			'save'    => nadlan_dsg_save_on(),
			'plans'   => count( $choices ) > 1 ? $choices : array(),
			'version' => defined( 'NADLAN_CONFIG_VERSION' ) ? NADLAN_CONFIG_VERSION : '0',
			'send'    => $send,
		) + $cfg;
		$json = wp_json_encode( $js, JSON_HEX_TAG | JSON_HEX_AMP | JSON_HEX_APOS | JSON_HEX_QUOT | JSON_UNESCAPED_SLASHES | JSON_UNESCAPED_UNICODE );

		$out  = nadlan_dsg_print_importmap();
		$out .= '<div class="nadlan-designer-pick" id="' . esc_attr( $host ) . '-pick" role="group" aria-label="גודל הדירה לדוגמה" hidden></div>' . "\n";
		$out .= '<div class="nadlan-designer" id="' . esc_attr( $host ) . '" style="position:relative;width:100%;height:' . esc_attr( $h ) . ';min-height:520px"></div>' . "\n";
		$out .= '<script type="module">' . nadlan_dsg_inline_js( $json ) . '</script>' . "\n";
		return $out;
	}
}

if ( ! function_exists( 'nadlan_dsg_inline_js' ) ) {
	/**
	 * The one small module that mounts the designer. Opening ?design=<id> loads that saved design (when it belongs to the
	 * same project and plan revision). The edit key of a design this browser created is kept in localStorage under
	 * 'nl-dsg-keys' (id => key, 20 newest): it is not a personal detail, and without it a visitor could not return and
	 * keep editing. Review note: drop it and every return becomes a copy.
	 */
	function nadlan_dsg_inline_js( $json ) {
		return 'const C=' . $json . ';(async()=>{' .
'const host=document.getElementById(C.host);if(!host)return;' .
'const he=C.lang==="he";' .
'const S={saved:he?"העיצוב נשמר. הקישור הועתק:":"Design saved. Link copied:",fail:he?"השמירה לא הצליחה. נסו שוב בעוד רגע.":"Saving failed. Please try again shortly."};' .
'const api=(p)=>C.rest+p+(C.test?(p.includes("?")?"&":"?")+"designer=next":"");' .
'const KS="nl-dsg-keys";' .
'const keys=()=>{try{return JSON.parse(localStorage.getItem(KS)||"{}")||{};}catch(e){return {};}};' .
'const keep=(id,key)=>{try{const k=keys();delete k[id];k[id]=key;const ids=Object.keys(k);while(ids.length>20)delete k[ids.shift()];localStorage.setItem(KS,JSON.stringify(k));}catch(e){}};' .
'let cur={id:null,rev:null};let design=null;' .
'const q=new URLSearchParams(location.search).get("design");' .
'if(C.save&&q&&/^[a-z2-7]{26}$/.test(q)){try{const r=await fetch(api("design/"+q),{credentials:"omit",cache:"no-store"});' .
'if(r.ok){const j=await r.json();const d=j&&j.design;' .
'if(d&&(d.project||"")===(C.project||"")){design=d;cur={id:q,rev:j.rev};}}}catch(e){}}' .
'const getPlan=(u)=>fetch(u).then((r)=>r.ok?r.json():null).catch(()=>null);' .
'const PK="nl-dsg-plan";let planUrl=C.planUrl;' .
'if(C.plans.length&&!design){try{const w=localStorage.getItem(PK);if(w&&C.plans.some((x)=>x.url.split("?")[0]===w))planUrl=C.plans.find((x)=>x.url.split("?")[0]===w).url;}catch(e){}}' .
'const [{mount},plan0]=await Promise.all([import(C.module),getPlan(planUrl)]);let plan=plan0;' .
'if(!plan){host.hidden=true;return;}' .
'if(design&&design.geometry_revision!==plan.geometry_revision){design=null;cur={id:null,rev:null};}' .
'const save=async(dz)=>{const k=cur.id&&keys()[cur.id];const body={design:dz};if(k){body.id=cur.id;body.key=k;body.base_rev=cur.rev;}' .
'let r=await fetch(api("save"),{method:"POST",credentials:"omit",headers:{"Content-Type":"application/json","X-NL-Designer":"1"},body:JSON.stringify(body)});' .
'if(k&&(r.status===409||r.status===403||r.status===404)){r=await fetch(api("save"),{method:"POST",credentials:"omit",headers:{"Content-Type":"application/json","X-NL-Designer":"1"},body:JSON.stringify({design:dz})});}' .
'if(!r.ok)throw new Error("save "+r.status);const j=await r.json();if(j.key)keep(j.id,j.key);cur={id:j.id,rev:j.rev};return j;};' .
'const link=(id)=>{const u=new URL(location.href);if(!C.test)u.searchParams.delete("designer");u.searchParams.set("design",id);u.hash="";return u.href;};' .
'const onSend=async(d)=>{let j;try{j=await save(d.getDesign());}catch(e){d.toast(S.fail,"stop");return;}' .
'const url=link(j.id);try{const h=new URL(location.href);h.searchParams.set("design",j.id);history.replaceState(history.state,"",h.href);}catch(e){}' .
'if(C.send!=="share"){const fn=C.send.split(".").reduce((o,k)=>o&&o[k],window);if(typeof fn==="function"){fn(d,Object.assign({url},j));return;}}' .
'try{await navigator.clipboard.writeText(url);}catch(e){}d.toast(S.saved+" "+url);};' .
'const mk=(pl,pu)=>{const o={plan:pl,planUrl:pu,lang:C.lang,version:C.version};if(C.save)o.onSend=onSend;if(C.unitLabel)o.unitLabel=C.unitLabel;if(C.title)o.title=C.title;return o;};' .
'const opts=mk(plan,planUrl);if(design)opts.design=design;' .
'let inst=null;try{inst=await mount(host,opts);}catch(e){host.hidden=true;return;}' .
'const pick=document.getElementById(C.host+"-pick");' .
'if(pick&&C.plans.length){let busy=false;C.plans.forEach((x)=>{const b=document.createElement("button");b.type="button";b.textContent=x.label;b.setAttribute("aria-pressed",String(x.url===planUrl));' .
'b.addEventListener("click",async()=>{if(busy||x.url===planUrl)return;busy=true;const pl=await getPlan(x.url);if(!pl){busy=false;return;}' .
'try{if(inst&&inst.destroy)inst.destroy();}catch(e){}host.innerHTML="";planUrl=x.url;plan=pl;cur={id:null,rev:null};' .
'try{localStorage.setItem(PK,x.url.split("?")[0]);}catch(e){}' .
'pick.querySelectorAll("button").forEach((o)=>o.setAttribute("aria-pressed",String(o===b)));' .
'try{inst=await mount(host,mk(pl,x.url));}catch(e){host.hidden=true;}busy=false;});pick.appendChild(b);});pick.hidden=false;}' .
'})();';
	}
}

add_action( 'init', function () {
	add_shortcode( 'nadlan_designer', 'nadlan_dsg_shortcode' );
} );

/* 11.11.2026 (HAD-707): the design pages (the neutral designers list and the designers page address); loaded only if present */
if ( file_exists( __DIR__ . '/design-pages.php' ) ) { require_once __DIR__ . '/design-pages.php'; }
