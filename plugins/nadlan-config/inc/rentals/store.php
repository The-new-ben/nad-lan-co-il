<?php
/**
 * nadlan-config - RENTALS v2: the store (HAD-383, 1.10.2026).
 *
 * Ten private tables (prefix {wp}nlrm_), one owner per row (owner_id = the
 * landlord's WP user id). Personal data of tenants, prospects, guarantors
 * and vendors is encrypted at rest (sodium secretbox, AES-256-GCM fallback)
 * with a key that lives in wp-config, never in the database: a database
 * dump alone does not reveal a tenant's name, phone, e-mail or ID number.
 * Phones and e-mails also get a keyed hash so a record can be found by
 * them without decrypting the table.
 *
 * Privacy law (Amendment 13): the landlord is the controller of his
 * tenants' data, nad-lan is the holder (מחזיק). Every read of personal data
 * is owner-scoped; every change is written to the events table (audit).
 */

if ( ! defined( 'ABSPATH' ) ) { exit; }

if ( ! defined( 'NLRM_DB_VERSION' ) ) { define( 'NLRM_DB_VERSION', '2.1.0' ); }

/* ---------- tables ---------- */
if ( ! function_exists( 'nlrm_t' ) ) {
	function nlrm_t( $name ) {
		global $wpdb;
		return $wpdb->prefix . 'nlrm_' . $name;
	}
}

if ( ! function_exists( 'nlrm_install' ) ) {
	function nlrm_install() {
		global $wpdb;
		require_once ABSPATH . 'wp-admin/includes/upgrade.php';
		$c = $wpdb->get_charset_collate();
		$sql = array();
		$sql[] = 'CREATE TABLE ' . nlrm_t( 'properties' ) . " (
  id bigint(20) unsigned NOT NULL AUTO_INCREMENT,
  owner_id bigint(20) unsigned NOT NULL,
  title varchar(160) NOT NULL DEFAULT '',
  address varchar(160) NOT NULL DEFAULT '',
  city varchar(80) NOT NULL DEFAULT '',
  lat decimal(9,6) DEFAULT NULL,
  lng decimal(9,6) DEFAULT NULL,
  floors smallint(5) unsigned NOT NULL DEFAULT 1,
  units_per_floor smallint(5) unsigned NOT NULL DEFAULT 1,
  meta longtext,
  legacy_id bigint(20) unsigned NOT NULL DEFAULT 0,
  created_at datetime NOT NULL,
  updated_at datetime NOT NULL,
  deleted_at datetime DEFAULT NULL,
  PRIMARY KEY  (id),
  KEY owner_id (owner_id)
) $c;";
		$sql[] = 'CREATE TABLE ' . nlrm_t( 'units' ) . " (
  id bigint(20) unsigned NOT NULL AUTO_INCREMENT,
  owner_id bigint(20) unsigned NOT NULL,
  property_id bigint(20) unsigned NOT NULL,
  label varchar(60) NOT NULL DEFAULT '',
  floor smallint(6) NOT NULL DEFAULT 0,
  pos smallint(5) unsigned NOT NULL DEFAULT 0,
  dir varchar(8) NOT NULL DEFAULT '',
  rooms decimal(3,1) DEFAULT NULL,
  sqm smallint(5) unsigned DEFAULT NULL,
  meta longtext,
  created_at datetime NOT NULL,
  updated_at datetime NOT NULL,
  deleted_at datetime DEFAULT NULL,
  PRIMARY KEY  (id),
  KEY owner_id (owner_id),
  KEY property_id (property_id)
) $c;";
		$sql[] = 'CREATE TABLE ' . nlrm_t( 'contacts' ) . " (
  id bigint(20) unsigned NOT NULL AUTO_INCREMENT,
  owner_id bigint(20) unsigned NOT NULL,
  kind varchar(16) NOT NULL DEFAULT 'tenant',
  name_enc text,
  phone_enc text,
  phone_hash char(64) NOT NULL DEFAULT '',
  email_enc text,
  email_hash char(64) NOT NULL DEFAULT '',
  idno_enc text,
  notes_enc longtext,
  lang varchar(5) NOT NULL DEFAULT 'he',
  stage varchar(16) NOT NULL DEFAULT '',
  tags varchar(255) NOT NULL DEFAULT '',
  meta longtext,
  created_at datetime NOT NULL,
  updated_at datetime NOT NULL,
  deleted_at datetime DEFAULT NULL,
  PRIMARY KEY  (id),
  KEY owner_id (owner_id),
  KEY phone_hash (phone_hash)
) $c;";
		$sql[] = 'CREATE TABLE ' . nlrm_t( 'leases' ) . " (
  id bigint(20) unsigned NOT NULL AUTO_INCREMENT,
  owner_id bigint(20) unsigned NOT NULL,
  unit_id bigint(20) unsigned NOT NULL,
  status varchar(12) NOT NULL DEFAULT 'active',
  start_date date DEFAULT NULL,
  end_date date DEFAULT NULL,
  option_until date DEFAULT NULL,
  rent int(10) unsigned NOT NULL DEFAULT 0,
  pay_day tinyint(3) unsigned NOT NULL DEFAULT 1,
  linkage longtext,
  securities longtext,
  parties longtext,
  terms longtext,
  signing longtext,
  created_at datetime NOT NULL,
  updated_at datetime NOT NULL,
  deleted_at datetime DEFAULT NULL,
  PRIMARY KEY  (id),
  KEY owner_id (owner_id),
  KEY unit_id (unit_id)
) $c;";
		$sql[] = 'CREATE TABLE ' . nlrm_t( 'ledger' ) . " (
  id bigint(20) unsigned NOT NULL AUTO_INCREMENT,
  owner_id bigint(20) unsigned NOT NULL,
  property_id bigint(20) unsigned NOT NULL DEFAULT 0,
  unit_id bigint(20) unsigned NOT NULL DEFAULT 0,
  lease_id bigint(20) unsigned NOT NULL DEFAULT 0,
  kind varchar(10) NOT NULL DEFAULT 'charge',
  category varchar(16) NOT NULL DEFAULT 'rent',
  amount bigint(20) NOT NULL DEFAULT 0,
  due_date date DEFAULT NULL,
  paid_date date DEFAULT NULL,
  method varchar(16) NOT NULL DEFAULT '',
  ref varchar(40) NOT NULL DEFAULT '',
  status varchar(10) NOT NULL DEFAULT 'open',
  applies_to bigint(20) unsigned NOT NULL DEFAULT 0,
  note varchar(255) NOT NULL DEFAULT '',
  doc_id bigint(20) unsigned NOT NULL DEFAULT 0,
  auto_key varchar(64) DEFAULT NULL,
  created_at datetime NOT NULL,
  updated_at datetime NOT NULL,
  deleted_at datetime DEFAULT NULL,
  PRIMARY KEY  (id),
  UNIQUE KEY owner_auto (owner_id,auto_key),
  KEY owner_id (owner_id),
  KEY unit_id (unit_id),
  KEY lease_id (lease_id)
) $c;";
		$sql[] = 'CREATE TABLE ' . nlrm_t( 'tickets' ) . " (
  id bigint(20) unsigned NOT NULL AUTO_INCREMENT,
  owner_id bigint(20) unsigned NOT NULL,
  property_id bigint(20) unsigned NOT NULL DEFAULT 0,
  unit_id bigint(20) unsigned NOT NULL DEFAULT 0,
  title varchar(160) NOT NULL DEFAULT '',
  body_enc longtext,
  category varchar(20) NOT NULL DEFAULT 'general',
  urgency varchar(10) NOT NULL DEFAULT 'standard',
  status varchar(12) NOT NULL DEFAULT 'new',
  reporter varchar(10) NOT NULL DEFAULT 'owner',
  vendor_id bigint(20) unsigned NOT NULL DEFAULT 0,
  cost int(10) unsigned NOT NULL DEFAULT 0,
  due_by date DEFAULT NULL,
  opened_at datetime NOT NULL,
  closed_at datetime DEFAULT NULL,
  meta longtext,
  updated_at datetime NOT NULL,
  deleted_at datetime DEFAULT NULL,
  PRIMARY KEY  (id),
  KEY owner_id (owner_id),
  KEY unit_id (unit_id)
) $c;";
		$sql[] = 'CREATE TABLE ' . nlrm_t( 'docs' ) . " (
  id bigint(20) unsigned NOT NULL AUTO_INCREMENT,
  owner_id bigint(20) unsigned NOT NULL,
  scope varchar(10) NOT NULL DEFAULT '',
  scope_id bigint(20) unsigned NOT NULL DEFAULT 0,
  kind varchar(16) NOT NULL DEFAULT 'other',
  name varchar(160) NOT NULL DEFAULT '',
  mime varchar(60) NOT NULL DEFAULT '',
  size int(10) unsigned NOT NULL DEFAULT 0,
  path varchar(190) NOT NULL DEFAULT '',
  sha256 char(64) NOT NULL DEFAULT '',
  enc tinyint(1) NOT NULL DEFAULT 1,
  created_by varchar(24) NOT NULL DEFAULT '',
  created_at datetime NOT NULL,
  deleted_at datetime DEFAULT NULL,
  PRIMARY KEY  (id),
  KEY owner_id (owner_id),
  KEY scope (scope,scope_id)
) $c;";
		$sql[] = 'CREATE TABLE ' . nlrm_t( 'events' ) . " (
  id bigint(20) unsigned NOT NULL AUTO_INCREMENT,
  owner_id bigint(20) unsigned NOT NULL,
  actor varchar(24) NOT NULL DEFAULT '',
  scope varchar(10) NOT NULL DEFAULT '',
  scope_id bigint(20) unsigned NOT NULL DEFAULT 0,
  type varchar(20) NOT NULL DEFAULT '',
  channel varchar(10) NOT NULL DEFAULT '',
  body_enc longtext,
  meta longtext,
  at datetime NOT NULL,
  PRIMARY KEY  (id),
  KEY owner_id (owner_id),
  KEY scope (scope,scope_id)
) $c;";
		$sql[] = 'CREATE TABLE ' . nlrm_t( 'links' ) . " (
  id bigint(20) unsigned NOT NULL AUTO_INCREMENT,
  owner_id bigint(20) unsigned NOT NULL,
  token_hash char(64) NOT NULL DEFAULT '',
  purpose varchar(16) NOT NULL DEFAULT '',
  scope varchar(10) NOT NULL DEFAULT '',
  scope_id bigint(20) unsigned NOT NULL DEFAULT 0,
  contact_id bigint(20) unsigned NOT NULL DEFAULT 0,
  expires_at datetime NOT NULL,
  uses int(10) unsigned NOT NULL DEFAULT 0,
  max_uses int(10) unsigned NOT NULL DEFAULT 0,
  revoked_at datetime DEFAULT NULL,
  created_at datetime NOT NULL,
  last_used_at datetime DEFAULT NULL,
  PRIMARY KEY  (id),
  KEY token_hash (token_hash),
  KEY owner_id (owner_id)
) $c;";
		$sql[] = 'CREATE TABLE ' . nlrm_t( 'tasks' ) . " (
  id bigint(20) unsigned NOT NULL AUTO_INCREMENT,
  owner_id bigint(20) unsigned NOT NULL,
  scope varchar(10) NOT NULL DEFAULT '',
  scope_id bigint(20) unsigned NOT NULL DEFAULT 0,
  title varchar(200) NOT NULL DEFAULT '',
  due date DEFAULT NULL,
  done_at datetime DEFAULT NULL,
  created_at datetime NOT NULL,
  PRIMARY KEY  (id),
  KEY owner_id (owner_id)
) $c;";
		$sql[] = 'CREATE TABLE ' . nlrm_t( 'members' ) . " (
  id bigint(20) unsigned NOT NULL AUTO_INCREMENT,
  owner_id bigint(20) unsigned NOT NULL,
  user_id bigint(20) unsigned NOT NULL,
  role varchar(12) NOT NULL DEFAULT 'viewer',
  created_at datetime NOT NULL,
  PRIMARY KEY  (id),
  KEY owner_id (owner_id),
  KEY user_id (user_id)
) $c;";
		foreach ( $sql as $q ) { dbDelta( $q ); }
		update_option( 'nlrm_db_version', NLRM_DB_VERSION, false );
		nlrm_keycheck_init();
	}
}

/* install / upgrade lazily: on admin, on our REST routes and on our pages */
if ( ! function_exists( 'nlrm_maybe_install' ) ) {
	function nlrm_maybe_install() {
		if ( get_option( 'nlrm_db_version' ) === NLRM_DB_VERSION ) { return; }
		if ( get_transient( 'nlrm_installing' ) ) { return; }
		set_transient( 'nlrm_installing', 1, 60 );
		nlrm_install();
		delete_transient( 'nlrm_installing' );
	}
}
add_action( 'admin_init', 'nlrm_maybe_install' );

/* ---------- crypto ---------- */
/*
 * Keys (3.10.2026). A tenant's personal data must stay readable for the
 * ten years a landlord keeps it, through host moves, restores and a
 * WordPress salt change (security plugins rotate salts). So the data key is
 * its OWN secret, never derived from the salts:
 *  1. the constant NADLAN_RM_KEY in wp-config (when the operator sets it), or
 *  2. a random key generated once, in uploads/nlrm-private/.nlrm-key.php
 *     (a PHP file that exits when requested; the database never holds it).
 * Every ciphertext names its key ('s2:<kid>:'), so keys can be rotated: a
 * new key becomes current, the old ones stay readable, and a resumable job
 * re-encrypts every field and file. Data written by the first build ('s1:',
 * salts-derived key) stays readable through the legacy key.
 * If the key file is ever missing while data exists, the app refuses to
 * write (nlrm_key_ok) instead of mixing keys; restore the file.
 */
if ( ! function_exists( 'nlrm_key_legacy' ) ) {
	function nlrm_key_legacy() {
		if ( defined( 'NADLAN_RM_KEY' ) && strlen( (string) NADLAN_RM_KEY ) >= 32 ) {
			$material = (string) NADLAN_RM_KEY;
		} else {
			$material = ( defined( 'AUTH_KEY' ) ? AUTH_KEY : '' ) . '|' . ( defined( 'SECURE_AUTH_KEY' ) ? SECURE_AUTH_KEY : '' ) . '|' . ( defined( 'LOGGED_IN_KEY' ) ? LOGGED_IN_KEY : '' ) . '|' . ( defined( 'NONCE_KEY' ) ? NONCE_KEY : '' );
		}
		return hash_hmac( 'sha256', 'nlrm-field-key-v1', $material, true );
	}
}
if ( ! function_exists( 'nlrm_keyfile_path' ) ) {
	function nlrm_keyfile_path() {
		$p = apply_filters( 'nlrm_keyfile_path', null );
		if ( $p ) { return $p; }
		$up = wp_upload_dir( null, false );
		return trailingslashit( $up['basedir'] ) . 'nlrm-private/.nlrm-key.php';
	}
}
if ( ! function_exists( 'nlrm_keyfile_read' ) ) {
	function nlrm_keyfile_read() {
		$p = nlrm_keyfile_path();
		if ( ! is_readable( $p ) ) { return null; }
		$raw = (string) @file_get_contents( $p ); // phpcs:ignore
		$j = json_decode( trim( (string) preg_replace( '/^<\?php exit; \?>/', '', $raw ) ), true );
		return is_array( $j ) && ! empty( $j['cur'] ) && ! empty( $j['keys'][ $j['cur'] ] ) ? $j : null;
	}
}
if ( ! function_exists( 'nlrm_keyfile_write' ) ) {
	function nlrm_keyfile_write( $j ) {
		$p = nlrm_keyfile_path();
		$dir = dirname( $p );
		if ( ! is_dir( $dir ) ) {
			wp_mkdir_p( $dir );
			@file_put_contents( $dir . '/.htaccess', "Require all denied\nDeny from all\n" ); // phpcs:ignore
			@file_put_contents( $dir . '/index.php', "<?php // Silence.\n" ); // phpcs:ignore
		}
		$tmp = $p . '.' . bin2hex( random_bytes( 4 ) ) . '.tmp';
		if ( false === @file_put_contents( $tmp, "<?php exit; ?>\n" . wp_json_encode( $j ) . "\n" ) ) { return false; } // phpcs:ignore
		@chmod( $tmp, 0600 ); // phpcs:ignore
		if ( ! @rename( $tmp, $p ) ) { @unlink( $tmp ); return false; } // phpcs:ignore
		return true;
	}
}
if ( ! function_exists( 'nlrm_kid' ) ) {
	function nlrm_kid( $key ) { return substr( hash( 'sha256', 'nlrm-kid|' . $key ), 0, 8 ); }
}
if ( ! function_exists( 'nlrm_keyring' ) ) {
	/* array( 'cur' => kid|null, 'keys' => kid => raw 32 bytes, 'idx' => raw, 'src' ) */
	function nlrm_keyring( $reset = false ) {
		static $ring = null;
		if ( $reset ) { $ring = null; }
		if ( null !== $ring ) { return $ring; }
		$ring = array( 'cur' => null, 'keys' => array( 'L' => nlrm_key_legacy() ), 'idx' => hash_hmac( 'sha256', 'nlrm-index', nlrm_key_legacy(), true ), 'src' => 'none' );
		$file = nlrm_keyfile_read();
		if ( $file ) {
			foreach ( (array) $file['keys'] as $kid => $b64 ) {
				$k = base64_decode( (string) $b64, true );
				if ( $k && 32 === strlen( $k ) ) { $ring['keys'][ $kid ] = $k; }
			}
			$ring['cur'] = isset( $ring['keys'][ $file['cur'] ] ) ? (string) $file['cur'] : null;
			if ( ! empty( $file['idx'] ) ) { $ring['idx'] = (string) base64_decode( (string) $file['idx'] ); }
			$ring['src'] = 'file';
		}
		if ( defined( 'NADLAN_RM_KEY' ) && strlen( (string) NADLAN_RM_KEY ) >= 32 ) {
			$k = hash_hmac( 'sha256', 'nlrm-field-key-v2', (string) NADLAN_RM_KEY, true );
			$ring['keys'][ nlrm_kid( $k ) ] = $k;
			$ring['cur'] = nlrm_kid( $k );
			$ring['src'] = 'constant';
			foreach ( defined( 'NADLAN_RM_KEY_PREV' ) ? explode( ',', (string) NADLAN_RM_KEY_PREV ) : array() as $prev ) {
				$prev = trim( $prev );
				if ( strlen( $prev ) >= 32 ) {
					$pk = hash_hmac( 'sha256', 'nlrm-field-key-v2', $prev, true );
					$ring['keys'][ nlrm_kid( $pk ) ] = $pk;
				}
			}
		}
		if ( null === $ring['cur'] && '' === (string) get_option( 'nlrm_key_fp', '' ) ) {
			/* first use on this site: make the key, once */
			$k = random_bytes( 32 );
			$kid = nlrm_kid( $k );
			$j = array( 'v' => 1, 'cur' => $kid, 'keys' => array( $kid => base64_encode( $k ) ), 'idx' => base64_encode( random_bytes( 32 ) ), 'created' => gmdate( 'c' ) );
			if ( nlrm_keyfile_write( $j ) && nlrm_keyfile_read() ) {
				$ring['keys'][ $kid ] = $k;
				$ring['cur'] = $kid;
				$ring['idx'] = base64_decode( $j['idx'] );
				$ring['src'] = 'file';
				update_option( 'nlrm_key_fp', $kid, false );
			}
		}
		return $ring;
	}
}
if ( ! function_exists( 'nlrm_key' ) ) {
	/* the current data key (raw 32 bytes); the legacy key when no other exists */
	function nlrm_key() {
		$r = nlrm_keyring();
		return $r['cur'] ? $r['keys'][ $r['cur'] ] : $r['keys']['L'];
	}
}
if ( ! function_exists( 'nlrm_enc' ) ) {
	function nlrm_enc( $plain ) {
		$plain = (string) $plain;
		if ( '' === $plain ) { return ''; }
		$r = nlrm_keyring();
		$kid = $r['cur'];
		$key = $kid ? $r['keys'][ $kid ] : $r['keys']['L'];
		if ( function_exists( 'sodium_crypto_secretbox' ) ) {
			$n = random_bytes( 24 );
			return ( $kid ? 's2:' . $kid . ':' : 's1:' ) . base64_encode( $n . sodium_crypto_secretbox( $plain, $n, $key ) );
		}
		$iv  = random_bytes( 12 );
		$tag = '';
		$c   = openssl_encrypt( $plain, 'aes-256-gcm', $key, OPENSSL_RAW_DATA, $iv, $tag );
		return ( $kid ? 'g2:' . $kid . ':' : 'g1:' ) . base64_encode( $iv . $tag . $c );
	}
}
if ( ! function_exists( 'nlrm_dec' ) ) {
	function nlrm_dec( $stored ) {
		$stored = (string) $stored;
		if ( '' === $stored ) { return ''; }
		$r = nlrm_keyring();
		$v = substr( $stored, 0, 3 );
		if ( 's2:' === $v || 'g2:' === $v ) {
			$kid = substr( $stored, 3, 8 );
			if ( ':' !== substr( $stored, 11, 1 ) || ! isset( $r['keys'][ $kid ] ) ) { return ''; }
			$key = $r['keys'][ $kid ];
			$raw = base64_decode( substr( $stored, 12 ), true );
			$v = 's2:' === $v ? 's1:' : 'g1:';
		} else {
			$key = $r['keys']['L'];
			$raw = base64_decode( substr( $stored, 3 ), true );
		}
		if ( false === $raw ) { return ''; }
		if ( 's1:' === $v && function_exists( 'sodium_crypto_secretbox_open' ) && strlen( $raw ) > 24 ) {
			$out = sodium_crypto_secretbox_open( substr( $raw, 24 ), substr( $raw, 0, 24 ), $key );
			return false === $out ? '' : $out;
		}
		if ( 'g1:' === $v && strlen( $raw ) > 28 ) {
			$out = openssl_decrypt( substr( $raw, 28 ), 'aes-256-gcm', $key, OPENSSL_RAW_DATA, substr( $raw, 0, 12 ), substr( $raw, 12, 16 ) );
			return false === $out ? '' : $out;
		}
		return '';
	}
}
if ( ! function_exists( 'nlrm_blob_enc' ) ) {
	/* files: 'S2' + kid (8 bytes) + nonce + box, or 'G2' + kid + iv + tag + data */
	function nlrm_blob_enc( $bytes ) {
		$r = nlrm_keyring();
		$kid = $r['cur'] ?: 'LLLLLLLL';
		$key = $r['cur'] ? $r['keys'][ $r['cur'] ] : $r['keys']['L'];
		if ( function_exists( 'sodium_crypto_secretbox' ) ) {
			$n = random_bytes( 24 );
			return 'S2' . $kid . $n . sodium_crypto_secretbox( $bytes, $n, $key );
		}
		$iv = random_bytes( 12 );
		$tag = '';
		$c = openssl_encrypt( $bytes, 'aes-256-gcm', $key, OPENSSL_RAW_DATA, $iv, $tag );
		return 'G2' . $kid . $iv . $tag . $c;
	}
}
if ( ! function_exists( 'nlrm_blob_kid' ) ) {
	function nlrm_blob_kid( $blob ) {
		$t = substr( (string) $blob, 0, 2 );
		if ( 'S2' === $t || 'G2' === $t ) {
			$k = substr( $blob, 2, 8 );
			return 'LLLLLLLL' === $k ? 'L' : $k;
		}
		return 'L';
	}
}
if ( ! function_exists( 'nlrm_blob_dec' ) ) {
	function nlrm_blob_dec( $blob ) {
		$blob = (string) $blob;
		$r = nlrm_keyring();
		$t = substr( $blob, 0, 2 );
		if ( 'S2' === $t || 'G2' === $t ) {
			$kid = nlrm_blob_kid( $blob );
			if ( ! isset( $r['keys'][ $kid ] ) ) { return false; }
			$key = $r['keys'][ $kid ];
			$body = substr( $blob, 10 );
			$t = 'S2' === $t ? 'S1' : 'G1';
		} else {
			$key = $r['keys']['L'];
			$body = substr( $blob, 2 );
		}
		if ( 'S1' === $t && function_exists( 'sodium_crypto_secretbox_open' ) && strlen( $body ) > 24 ) {
			return sodium_crypto_secretbox_open( substr( $body, 24 ), substr( $body, 0, 24 ), $key );
		}
		if ( 'G1' === $t && strlen( $body ) > 28 ) {
			return openssl_decrypt( substr( $body, 28 ), 'aes-256-gcm', $key, OPENSSL_RAW_DATA, substr( $body, 0, 12 ), substr( $body, 12, 16 ) );
		}
		return false;
	}
}
if ( ! function_exists( 'nlrm_hash' ) ) {
	/* a blind index (find a tenant by phone without decrypting the table); its
	   key never rotates, so lookups survive a data-key rotation */
	function nlrm_hash( $value ) {
		$value = trim( mb_strtolower( (string) $value ) );
		if ( '' === $value ) { return ''; }
		$r = nlrm_keyring();
		return hash_hmac( 'sha256', $value, $r['idx'] );
	}
}
if ( ! function_exists( 'nlrm_keycheck_init' ) ) {
	function nlrm_keycheck_init() {
		if ( '' === (string) get_option( 'nlrm_keycheck', '' ) ) {
			update_option( 'nlrm_keycheck', nlrm_enc( 'nlrm-ok' ), false );
		}
	}
}
if ( ! function_exists( 'nlrm_key_ok' ) ) {
	/* the stored check decrypts AND the key the data was made with is present
	   (a lost key file is caught here, before anything is written) */
	function nlrm_key_ok() {
		$c = (string) get_option( 'nlrm_keycheck', '' );
		$r = nlrm_keyring();
		$fp = (string) get_option( 'nlrm_key_fp', '' );
		if ( $fp && ! isset( $r['keys'][ $fp ] ) && 'constant' !== $r['src'] ) { return false; }
		return '' === $c || 'nlrm-ok' === nlrm_dec( $c );
	}
}

/* ---------- key rotation (resumable; the old key stays readable) ---------- */
if ( ! function_exists( 'nlrm_rotate_begin' ) ) {
	function nlrm_rotate_begin() {
		$j = nlrm_keyfile_read();
		if ( ! $j ) { return new WP_Error( 'nlrm_key', 'no key file to rotate (a constant key rotates through NADLAN_RM_KEY + NADLAN_RM_KEY_PREV)' ); }
		$k = random_bytes( 32 );
		$kid = nlrm_kid( $k );
		$j['keys'][ $kid ] = base64_encode( $k );
		$j['prev'] = array_values( array_unique( array_merge( (array) ( $j['prev'] ?? array() ), array( $j['cur'] ) ) ) );
		$j['cur'] = $kid;
		$j['rotated'] = gmdate( 'c' );
		if ( ! nlrm_keyfile_write( $j ) ) { return new WP_Error( 'nlrm_key', 'key file not writable' ); }
		nlrm_keyring( true );
		update_option( 'nlrm_key_fp', $kid, false );
		update_option( 'nlrm_keycheck', nlrm_enc( 'nlrm-ok' ), false );
		update_option( 'nlrm_rotate', array( 'to' => $kid, 'started' => gmdate( 'c' ), 'done' => false ), false );
		return $kid;
	}
}
if ( ! function_exists( 'nlrm_rotate_step' ) ) {
	/* re-encrypts up to $batch values under the current key; returns 1 while
	   work is left and 0 when everything is under the current key */
	function nlrm_rotate_step( $batch = 500 ) {
		global $wpdb;
		$r = nlrm_keyring();
		if ( ! $r['cur'] ) { return 0; }
		$cur = 's2:' . $r['cur'] . ':';
		$curg = 'g2:' . $r['cur'] . ':';
		$cols = array( 'contacts' => array( 'name_enc', 'phone_enc', 'email_enc', 'idno_enc', 'notes_enc' ), 'tickets' => array( 'body_enc' ), 'events' => array( 'body_enc' ) );
		$done = 0;
		foreach ( $cols as $t => $list ) {
			foreach ( $list as $c ) {
				$rows = $wpdb->get_results( $wpdb->prepare( 'SELECT id, ' . $c . ' AS v FROM ' . nlrm_t( $t ) . ' WHERE ' . $c . " <> '' AND " . $c . ' NOT LIKE %s AND ' . $c . ' NOT LIKE %s LIMIT %d', $cur . '%', $curg . '%', $batch - $done ), ARRAY_A );
				foreach ( (array) $rows as $row ) {
					$plain = nlrm_dec( $row['v'] );
					$wpdb->update( nlrm_t( $t ), array( $c => '' === $plain ? '' : nlrm_enc( $plain ) ), array( 'id' => (int) $row['id'] ) );
					$done++;
				}
				if ( $done >= $batch ) { return 1; }
			}
		}
		/* signatures inside the leases' signing JSON */
		foreach ( (array) $wpdb->get_results( $wpdb->prepare( 'SELECT id, signing FROM ' . nlrm_t( 'leases' ) . ' WHERE signing LIKE %s', '%sig_enc%' ), ARRAY_A ) as $row ) {
			$sg = json_decode( (string) $row['signing'], true );
			$changed = false;
			foreach ( (array) ( $sg['parties'] ?? array() ) as $i => $pty ) {
				if ( ! empty( $pty['sig_enc'] ) && 0 !== strpos( $pty['sig_enc'], $cur ) && 0 !== strpos( $pty['sig_enc'], $curg ) ) {
					$sg['parties'][ $i ]['sig_enc'] = nlrm_enc( nlrm_dec( $pty['sig_enc'] ) );
					$changed = true;
				}
			}
			if ( $changed ) {
				$wpdb->update( nlrm_t( 'leases' ), array( 'signing' => wp_json_encode( $sg, JSON_UNESCAPED_UNICODE ) ), array( 'id' => (int) $row['id'] ) );
				$done++;
			}
			if ( $done >= $batch ) { return 1; }
		}
		/* the landlords' own ID numbers */
		foreach ( (array) $wpdb->get_results( $wpdb->prepare( 'SELECT umeta_id, meta_value FROM ' . $wpdb->usermeta . " WHERE meta_key = 'nlrm_idno_enc' AND meta_value <> '' AND meta_value NOT LIKE %s AND meta_value NOT LIKE %s", $cur . '%', $curg . '%' ), ARRAY_A ) as $row ) {
			$wpdb->update( $wpdb->usermeta, array( 'meta_value' => nlrm_enc( nlrm_dec( $row['meta_value'] ) ) ), array( 'umeta_id' => (int) $row['umeta_id'] ) );
			$done++;
			if ( $done >= $batch ) { return 1; }
		}
		/* files */
		if ( function_exists( 'nlrm_private_dir' ) ) {
			foreach ( (array) $wpdb->get_results( 'SELECT id, path FROM ' . nlrm_t( 'docs' ) . " WHERE path <> ''", ARRAY_A ) as $d ) {
				$f = nlrm_private_dir() . $d['path'];
				$blob = @file_get_contents( $f ); // phpcs:ignore
				if ( false === $blob || nlrm_blob_kid( $blob ) === $r['cur'] ) { continue; }
				$plain = nlrm_blob_dec( $blob );
				if ( false === $plain ) { continue; }
				$tmp = $f . '.rot';
				if ( false !== @file_put_contents( $tmp, nlrm_blob_enc( $plain ) ) ) { @rename( $tmp, $f ); $done++; } // phpcs:ignore
				if ( $done >= $batch ) { return 1; }
			}
		}
		$st = (array) get_option( 'nlrm_rotate', array() );
		$st['done'] = gmdate( 'c' );
		update_option( 'nlrm_rotate', $st, false );
		return 0;
	}
}

/* ---------- phone, dates, money ---------- */
if ( ! function_exists( 'nlrm_phone' ) ) {
	/* Israeli mobile/landline to E.164 digits (972...), foreign numbers kept. */
	function nlrm_phone( $raw ) {
		$d = preg_replace( '/[^0-9+]/', '', (string) $raw );
		if ( '' === $d ) { return ''; }
		if ( 0 === strpos( $d, '+' ) ) { return substr( preg_replace( '/\D/', '', $d ), 0, 15 ); }
		if ( 0 === strpos( $d, '00' ) ) { return substr( substr( $d, 2 ), 0, 15 ); }
		if ( 0 === strpos( $d, '0' ) ) { return '972' . substr( $d, 1, 12 ); }
		return substr( $d, 0, 15 );
	}
}
if ( ! function_exists( 'nlrm_date' ) ) {
	function nlrm_date( $raw ) {
		$raw = (string) $raw;
		return preg_match( '/^\d{4}-\d{2}-\d{2}$/', $raw ) ? $raw : null;
	}
}
if ( ! function_exists( 'nlrm_time' ) ) {
	/* the one clock of the module (a test moves it through the 'nlrm_time' filter) */
	function nlrm_time() { return (int) apply_filters( 'nlrm_time', time() ); }
}
if ( ! function_exists( 'nlrm_now' ) ) {
	function nlrm_now() { return gmdate( 'Y-m-d H:i:s', nlrm_time() ); }
}

/* ---------- who owns what ---------- */
if ( ! function_exists( 'nlrm_owner' ) ) {
	/* The account whose portfolio the current request acts on: the user
	   himself, or the owner who invited him as a team member. */
	function nlrm_owner() {
		static $cache = array();
		$uid = get_current_user_id();
		if ( isset( $cache[ $uid ] ) ) { return $cache[ $uid ]; }
		if ( ! $uid ) { return 0; }
		$o = $uid;
		$act = isset( $_COOKIE['nlrm_acct'] ) ? (int) $_COOKIE['nlrm_acct'] : 0; // phpcs:ignore
		if ( $act && $act !== $uid ) {
			global $wpdb;
			$m = $wpdb->get_var( $wpdb->prepare( 'SELECT role FROM ' . nlrm_t( 'members' ) . ' WHERE owner_id = %d AND user_id = %d', $act, $uid ) );
			if ( $m ) { $o = $act; }
		}
		$cache[ $uid ] = $o;
		return $o;
	}
}
if ( ! function_exists( 'nlrm_role' ) ) {
	function nlrm_role() {
		$uid = get_current_user_id();
		$own = nlrm_owner();
		if ( ! $uid || ! $own ) { return ''; }
		if ( $own === $uid ) { return 'owner'; }
		global $wpdb;
		return (string) $wpdb->get_var( $wpdb->prepare( 'SELECT role FROM ' . nlrm_t( 'members' ) . ' WHERE owner_id = %d AND user_id = %d', $own, $uid ) );
	}
}
if ( ! function_exists( 'nlrm_can_write' ) ) {
	function nlrm_can_write() { return in_array( nlrm_role(), array( 'owner', 'manager' ), true ); }
}

/* ---------- entity schemas: one sanitizer for every write ---------- */
if ( ! function_exists( 'nlrm_schema' ) ) {
	function nlrm_schema( $entity ) {
		$S = array(
			'property' => array( 'table' => 'properties', 'fields' => array(
				'title' => array( 'str', 160 ), 'address' => array( 'str', 160 ), 'city' => array( 'str', 80 ),
				'lat' => array( 'float', -90, 90 ), 'lng' => array( 'float', -180, 180 ),
				'floors' => array( 'int', 1, 80 ), 'units_per_floor' => array( 'int', 1, 24 ),
				'meta' => array( 'json' ),
			) ),
			'unit' => array( 'table' => 'units', 'fields' => array(
				'property_id' => array( 'ref', 'property' ), 'label' => array( 'str', 60 ),
				'floor' => array( 'int', -5, 80 ), 'pos' => array( 'int', 0, 24 ),
				'dir' => array( 'enum', array( '', 'north', 'south', 'east', 'west', 'ne', 'nw', 'se', 'sw' ) ),
				'rooms' => array( 'float', 0, 20 ), 'sqm' => array( 'int', 0, 2000 ), 'meta' => array( 'json' ),
			) ),
			'contact' => array( 'table' => 'contacts', 'fields' => array(
				'kind' => array( 'enum', array( 'tenant', 'prospect', 'guarantor', 'vendor', 'coowner', 'other' ) ),
				'name' => array( 'enc', 120 ), 'phone' => array( 'encphone' ), 'email' => array( 'encmail' ),
				'idno' => array( 'enc', 20 ), 'notes' => array( 'enc', 4000 ),
				'lang' => array( 'enum', array( 'he', 'en', 'fr', 'ru', 'ar' ) ),
				'stage' => array( 'enum', array( '', 'new', 'contacted', 'viewing', 'applied', 'approved', 'signed', 'lost' ) ),
				'tags' => array( 'str', 255 ), 'meta' => array( 'json' ),
			) ),
			'lease' => array( 'table' => 'leases', 'fields' => array(
				'unit_id' => array( 'ref', 'unit' ),
				'status' => array( 'enum', array( 'draft', 'active', 'ended', 'cancelled' ) ),
				'start_date' => array( 'date' ), 'end_date' => array( 'date' ), 'option_until' => array( 'date' ),
				'rent' => array( 'int', 0, 1000000 ), 'pay_day' => array( 'int', 1, 28 ),
				'linkage' => array( 'json' ), 'securities' => array( 'json' ), 'parties' => array( 'json' ),
				'terms' => array( 'json' ),
			) ),
			'ledger' => array( 'table' => 'ledger', 'fields' => array(
				'property_id' => array( 'ref', 'property' ), 'unit_id' => array( 'ref', 'unit' ), 'lease_id' => array( 'ref', 'lease' ),
				'kind' => array( 'enum', array( 'charge', 'payment', 'expense', 'income', 'refund' ) ),
				'category' => array( 'enum', array( 'rent', 'deposit', 'arnona', 'vaad', 'water', 'electric', 'gas', 'repair', 'insurance', 'mortgage', 'tax', 'fee', 'other' ) ),
				'amount' => array( 'money' ), 'due_date' => array( 'date' ), 'paid_date' => array( 'date' ),
				'method' => array( 'enum', array( '', 'transfer', 'cheque', 'bit', 'paybox', 'cash', 'card', 'standing', 'other', 'deposit', 'writeoff', 'renewal' ) ),
				'ref' => array( 'str', 40 ),
				'status' => array( 'enum', array( 'open', 'paid', 'partial', 'pending', 'deposited', 'bounced', 'void' ) ),
				'applies_to' => array( 'ref', 'ledger' ), 'note' => array( 'str', 255 ), 'doc_id' => array( 'ref', 'doc' ),
			) ),
			'ticket' => array( 'table' => 'tickets', 'fields' => array(
				'property_id' => array( 'ref', 'property' ), 'unit_id' => array( 'ref', 'unit' ),
				'title' => array( 'str', 160 ), 'body' => array( 'enc', 4000 ),
				'category' => array( 'enum', array( 'general', 'plumbing', 'electric', 'ac', 'appliance', 'boiler', 'roof', 'mold', 'locks', 'pests', 'paint', 'other' ) ),
				'urgency' => array( 'enum', array( 'urgent', 'standard' ) ),
				'status' => array( 'enum', array( 'new', 'scheduled', 'progress', 'waiting', 'done', 'cancelled' ) ),
				'reporter' => array( 'enum', array( 'owner', 'tenant', 'vendor' ) ),
				'vendor_id' => array( 'ref', 'contact' ), 'cost' => array( 'int', 0, 10000000 ),
				'due_by' => array( 'date' ), 'meta' => array( 'json' ),
			) ),
			'task' => array( 'table' => 'tasks', 'fields' => array(
				'scope' => array( 'enum', array( '', 'property', 'unit', 'lease', 'contact', 'ticket' ) ),
				'scope_id' => array( 'int', 0, PHP_INT_MAX ), 'title' => array( 'str', 200 ), 'due' => array( 'date' ),
				'done' => array( 'bool' ),
			) ),
		);
		return isset( $S[ $entity ] ) ? $S[ $entity ] : null;
	}
}

if ( ! function_exists( 'nlrm_clean_row' ) ) {
	/* input array -> array of DB columns, only the fields that were sent */
	function nlrm_clean_row( $entity, $in, $owner ) {
		$sc = nlrm_schema( $entity );
		if ( ! $sc ) { return new WP_Error( 'nlrm_bad_entity', 'bad entity', array( 'status' => 400 ) ); }
		$row = array();
		foreach ( $sc['fields'] as $f => $spec ) {
			if ( ! array_key_exists( $f, $in ) ) { continue; }
			$v = $in[ $f ];
			switch ( $spec[0] ) {
				case 'str':
					$row[ $f ] = mb_substr( sanitize_text_field( (string) $v ), 0, $spec[1] );
					break;
				case 'int':
					$row[ $f ] = max( $spec[1], min( $spec[2], (int) $v ) );
					break;
				case 'float':
					$row[ $f ] = ( '' === $v || null === $v ) ? null : max( $spec[1], min( $spec[2], (float) $v ) );
					break;
				case 'money': /* agorot, signed */
					$row[ $f ] = (int) round( (float) $v );
					break;
				case 'bool':
					if ( 'done' === $f ) { $row['done_at'] = $v ? nlrm_now() : null; } else { $row[ $f ] = $v ? 1 : 0; }
					break;
				case 'enum':
					$row[ $f ] = in_array( (string) $v, $spec[1], true ) ? (string) $v : $spec[1][0];
					break;
				case 'date':
					$row[ $f ] = nlrm_date( $v );
					break;
				case 'json':
					$row[ $f ] = wp_json_encode( nlrm_clean_json( $v ), JSON_UNESCAPED_UNICODE );
					break;
				case 'ref':
					$id = (int) $v;
					if ( $id && ! nlrm_owns( $spec[1], $id, $owner ) ) {
						return new WP_Error( 'nlrm_forbidden', 'not yours', array( 'status' => 403 ) );
					}
					$row[ $f ] = $id;
					break;
				case 'enc':
					$row[ $f . '_enc' ] = nlrm_enc( mb_substr( sanitize_textarea_field( (string) $v ), 0, $spec[1] ) );
					break;
				case 'encphone':
					$p = nlrm_phone( $v );
					$row['phone_enc']  = nlrm_enc( $p );
					$row['phone_hash'] = nlrm_hash( $p );
					break;
				case 'encmail':
					$m = sanitize_email( (string) $v );
					$row['email_enc']  = nlrm_enc( $m );
					$row['email_hash'] = nlrm_hash( $m );
					break;
			}
		}
		return $row;
	}
}

if ( ! function_exists( 'nlrm_clean_json' ) ) {
	/* free-form JSON blobs: depth 4, strings 2,000 chars, 300 keys, no HTML */
	function nlrm_clean_json( $v, $depth = 0 ) {
		if ( $depth > 4 ) { return null; }
		if ( is_array( $v ) ) {
			$out = array();
			$n = 0;
			foreach ( $v as $k => $x ) {
				if ( ++$n > 300 ) { break; }
				$key = is_int( $k ) ? $k : mb_substr( preg_replace( '/[^A-Za-z0-9_\-]/', '', (string) $k ), 0, 40 );
				$out[ $key ] = nlrm_clean_json( $x, $depth + 1 );
			}
			return $out;
		}
		if ( is_bool( $v ) || is_null( $v ) ) { return $v; }
		if ( is_int( $v ) || is_float( $v ) ) { return $v; }
		return mb_substr( wp_strip_all_tags( (string) $v ), 0, 2000 );
	}
}

if ( ! function_exists( 'nlrm_owns' ) ) {
	function nlrm_owns( $entity, $id, $owner ) {
		$tables = array( 'property' => 'properties', 'unit' => 'units', 'contact' => 'contacts', 'lease' => 'leases', 'ledger' => 'ledger', 'ticket' => 'tickets', 'doc' => 'docs', 'task' => 'tasks' );
		if ( ! isset( $tables[ $entity ] ) || ! $id || ! $owner ) { return false; }
		global $wpdb;
		return (bool) $wpdb->get_var( $wpdb->prepare( 'SELECT id FROM ' . nlrm_t( $tables[ $entity ] ) . ' WHERE id = %d AND owner_id = %d AND ' . ( 'tasks' === $tables[ $entity ] ? '1=1' : 'deleted_at IS NULL' ), $id, $owner ) );
	}
}

/* ---------- row -> API object (decrypts personal data) ---------- */
if ( ! function_exists( 'nlrm_out' ) ) {
	function nlrm_out( $entity, $r ) {
		if ( ! $r ) { return null; }
		$r = (array) $r;
		$o = array( 'id' => (int) $r['id'] );
		$sc = nlrm_schema( $entity );
		foreach ( $sc['fields'] as $f => $spec ) {
			switch ( $spec[0] ) {
				case 'enc':      $o[ $f ] = nlrm_dec( $r[ $f . '_enc' ] ?? '' ); break;
				case 'encphone': $o['phone'] = nlrm_dec( $r['phone_enc'] ?? '' ); break;
				case 'encmail':  $o['email'] = nlrm_dec( $r['email_enc'] ?? '' ); break;
				case 'json':     $o[ $f ] = json_decode( (string) ( $r[ $f ] ?? '' ), true ) ?: new stdClass(); break;
				case 'int': case 'ref': $o[ $f ] = (int) ( $r[ $f ] ?? 0 ); break;
				case 'money':    $o[ $f ] = (int) ( $r[ $f ] ?? 0 ); break;
				case 'float':    $o[ $f ] = isset( $r[ $f ] ) && null !== $r[ $f ] ? (float) $r[ $f ] : null; break;
				case 'bool':     $o['done'] = ! empty( $r['done_at'] ); break;
				default:         $o[ $f ] = isset( $r[ $f ] ) ? $r[ $f ] : null;
			}
		}
		foreach ( array( 'created_at', 'updated_at', 'opened_at', 'closed_at', 'signing' ) as $k ) {
			if ( isset( $r[ $k ] ) ) { $o[ $k ] = 'signing' === $k ? ( json_decode( (string) $r[ $k ], true ) ?: new stdClass() ) : $r[ $k ]; }
		}
		return $o;
	}
}

/* ---------- CRUD ---------- */
if ( ! function_exists( 'nlrm_get_all' ) ) {
	function nlrm_get_all( $entity, $owner, $where = '' ) {
		$sc = nlrm_schema( $entity );
		if ( ! $sc ) { return array(); }
		global $wpdb;
		$del = 'tasks' === $sc['table'] ? '' : ' AND deleted_at IS NULL';
		$rows = $wpdb->get_results( $wpdb->prepare( 'SELECT * FROM ' . nlrm_t( $sc['table'] ) . ' WHERE owner_id = %d' . $del . $where . ' ORDER BY id ASC LIMIT 5000', $owner ), ARRAY_A );
		return array_map( function ( $r ) use ( $entity ) { return nlrm_out( $entity, $r ); }, (array) $rows );
	}
}
if ( ! function_exists( 'nlrm_get' ) ) {
	function nlrm_get( $entity, $id, $owner ) {
		$sc = nlrm_schema( $entity );
		if ( ! $sc ) { return null; }
		global $wpdb;
		$r = $wpdb->get_row( $wpdb->prepare( 'SELECT * FROM ' . nlrm_t( $sc['table'] ) . ' WHERE id = %d AND owner_id = %d', $id, $owner ), ARRAY_A );
		return $r ? nlrm_out( $entity, $r ) : null;
	}
}
if ( ! function_exists( 'nlrm_save' ) ) {
	/* create (no id) or update (id); returns the API object or WP_Error */
	function nlrm_save( $entity, $in, $owner, $actor = '' ) {
		$sc = nlrm_schema( $entity );
		if ( ! $sc || ! $owner ) { return new WP_Error( 'nlrm_bad', 'bad request', array( 'status' => 400 ) ); }
		$row = nlrm_clean_row( $entity, (array) $in, $owner );
		if ( is_wp_error( $row ) ) { return $row; }
		global $wpdb;
		$t   = nlrm_t( $sc['table'] );
		$id  = isset( $in['id'] ) ? (int) $in['id'] : 0;
		$now = nlrm_now();
		if ( 'unit' === $entity && ! $id && empty( $row['property_id'] ) ) {
			return new WP_Error( 'nlrm_bad', 'unit needs a property', array( 'status' => 400 ) );
		}
		if ( $id ) {
			if ( ! nlrm_owns( $entity, $id, $owner ) ) { return new WP_Error( 'nlrm_forbidden', 'not yours', array( 'status' => 403 ) ); }
			/* money is append-only: a recorded line keeps its amount, kind and lease;
			   a mistake is voided and recorded again, and the audit keeps both */
			if ( 'ledger' === $entity ) {
				foreach ( array( 'amount', 'kind', 'lease_id', 'unit_id', 'property_id', 'auto_key' ) as $frozen ) { unset( $row[ $frozen ] ); }
			}
			if ( 'tasks' !== $sc['table'] ) { $row['updated_at'] = $now; }
			if ( 'ticket' === $entity && isset( $row['status'] ) ) {
				$row['closed_at'] = in_array( $row['status'], array( 'done', 'cancelled' ), true ) ? $now : null;
			}
			if ( $row ) { $wpdb->update( $t, $row, array( 'id' => $id, 'owner_id' => $owner ) ); }
			nlrm_event( $owner, $actor, $entity, $id, 'update', '', '', array( 'fields' => array_keys( $row ) ) );
		} else {
			$row['owner_id'] = $owner;
			if ( 'tasks' === $sc['table'] ) {
				$row['created_at'] = $now;
			} elseif ( 'tickets' === $sc['table'] ) {
				$row['opened_at']  = $now;
				$row['updated_at'] = $now;
			} else {
				$row['created_at'] = $now;
				$row['updated_at'] = $now;
			}
			$ok = $wpdb->insert( $t, $row );
			if ( ! $ok ) { return new WP_Error( 'nlrm_db', 'save failed', array( 'status' => 500 ) ); }
			$id = (int) $wpdb->insert_id;
			nlrm_event( $owner, $actor, $entity, $id, 'create', '', '', array() );
		}
		return nlrm_get( $entity, $id, $owner );
	}
}
if ( ! function_exists( 'nlrm_delete' ) ) {
	/* soft delete (kept 30 days for undo, then purged by the daily job) */
	function nlrm_delete( $entity, $id, $owner, $actor = '' ) {
		$sc = nlrm_schema( $entity );
		/* the books are never deleted: a wrong line is voided (nlrm_ledger_act) */
		if ( ! $sc || 'ledger' === $entity || ! nlrm_owns( $entity, $id, $owner ) ) { return false; }
		global $wpdb;
		if ( 'tasks' === $sc['table'] ) {
			$wpdb->delete( nlrm_t( 'tasks' ), array( 'id' => $id, 'owner_id' => $owner ) );
		} else {
			$wpdb->update( nlrm_t( $sc['table'] ), array( 'deleted_at' => nlrm_now() ), array( 'id' => $id, 'owner_id' => $owner ) );
		}
		nlrm_event( $owner, $actor, $entity, $id, 'delete', '', '', array() );
		return true;
	}
}

/* ---------- the timeline (messages, notes, audit) ---------- */
if ( ! function_exists( 'nlrm_event' ) ) {
	function nlrm_event( $owner, $actor, $scope, $scope_id, $type, $channel = '', $body = '', $meta = array() ) {
		global $wpdb;
		if ( '' === $actor ) { $actor = get_current_user_id() ? 'u:' . get_current_user_id() : 'sys'; }
		$wpdb->insert( nlrm_t( 'events' ), array(
			'owner_id' => (int) $owner, 'actor' => mb_substr( (string) $actor, 0, 24 ), 'scope' => mb_substr( (string) $scope, 0, 10 ),
			'scope_id' => (int) $scope_id, 'type' => mb_substr( (string) $type, 0, 20 ), 'channel' => mb_substr( (string) $channel, 0, 10 ),
			'body_enc' => nlrm_enc( mb_substr( (string) $body, 0, 4000 ) ),
			'meta' => wp_json_encode( nlrm_clean_json( $meta ), JSON_UNESCAPED_UNICODE ), 'at' => nlrm_now(),
		) );
		return (int) $wpdb->insert_id;
	}
}
if ( ! function_exists( 'nlrm_events' ) ) {
	function nlrm_events( $owner, $scope = '', $scope_id = 0, $limit = 200 ) {
		global $wpdb;
		$w = '';
		if ( $scope ) { $w = $wpdb->prepare( ' AND scope = %s AND scope_id = %d', $scope, $scope_id ); }
		$rows = $wpdb->get_results( $wpdb->prepare( 'SELECT * FROM ' . nlrm_t( 'events' ) . ' WHERE owner_id = %d' . $w . " AND type NOT IN ('update','create') ORDER BY id DESC LIMIT %d", $owner, $limit ), ARRAY_A );
		return array_map( function ( $r ) {
			return array( 'id' => (int) $r['id'], 'actor' => $r['actor'], 'scope' => $r['scope'], 'scope_id' => (int) $r['scope_id'],
				'type' => $r['type'], 'channel' => $r['channel'], 'body' => nlrm_dec( $r['body_enc'] ), 'meta' => json_decode( (string) $r['meta'], true ) ?: new stdClass(), 'at' => $r['at'] );
		}, (array) $rows );
	}
}

/* ---------- the whole portfolio in one payload (owner only) ---------- */
if ( ! function_exists( 'nlrm_bootstrap' ) ) {
	function nlrm_bootstrap( $owner ) {
		$today = nlrm_today();
		/* the books shown in full from January of last year (the tax year and the
		   one before), plus every line still open; balances and reports come from
		   the FULL history (nlrm_money, nlrm_stats), never from this window */
		$since = ( (int) substr( $today, 0, 4 ) - 1 ) . '-01-01';
		$states = array();
		$money = nlrm_money( $owner, $today, null, $states );
		return array(
			'properties' => nlrm_get_all( 'property', $owner ),
			'units'      => nlrm_get_all( 'unit', $owner ),
			'contacts'   => nlrm_get_all( 'contact', $owner ),
			'leases'     => nlrm_get_all( 'lease', $owner ),
			'ledger'     => nlrm_ledger_window( $owner, $since, $states ),
			'money'      => (object) $money,
			'stats'      => (object) nlrm_stats( $owner ),
			'today'      => $today,
			'since'      => $since,
			'tickets'    => nlrm_get_all( 'ticket', $owner ),
			'tasks'      => nlrm_get_all( 'task', $owner ),
			'docs'       => nlrm_docs_meta( $owner ),
			'events'     => nlrm_events( $owner, '', 0, 150 ),
			'plan'       => nlrm_plan( $owner ),
			'role'       => nlrm_role(),
			'key_ok'     => nlrm_key_ok(),
		);
	}
}
if ( ! function_exists( 'nlrm_ledger_rows' ) ) {
	/* ledger rows as API objects, each charge with its derived state */
	function nlrm_ledger_rows( $rows, $states ) {
		return array_map( function ( $r ) use ( $states ) {
			$o = nlrm_out( 'ledger', $r );
			$o['auto'] = isset( $r['auto_key'] ) && $r['auto_key'] && 0 !== strpos( (string) $r['auto_key'], 'cref:' ) ? (string) $r['auto_key'] : '';
			if ( 'charge' === $o['kind'] && 'void' !== $o['status'] ) {
				$st = $states[ (int) $o['id'] ] ?? array( 'open', 0 );
				$o['status'] = $st[0];
				$o['covered'] = (int) $st[1];
			}
			/* lean: empty fields are not sent (the 200-apartment account sends ~11,000 lines) */
			foreach ( array( 'auto', 'note', 'ref', 'method' ) as $k ) { if ( isset( $o[ $k ] ) && '' === $o[ $k ] ) { unset( $o[ $k ] ); } }
			foreach ( array( 'applies_to', 'doc_id' ) as $k ) { if ( isset( $o[ $k ] ) && 0 === $o[ $k ] ) { unset( $o[ $k ] ); } }
			if ( null === $o['paid_date'] ) { unset( $o['paid_date'] ); }
			if ( null === $o['due_date'] ) { unset( $o['due_date'] ); }
			unset( $o['updated_at'] );
			return $o;
		}, (array) $rows );
	}
}
if ( ! function_exists( 'nlrm_ledger_window' ) ) {
	function nlrm_ledger_window( $owner, $since, $states ) {
		global $wpdb;
		$t = nlrm_t( 'ledger' );
		$rows = (array) $wpdb->get_results( $wpdb->prepare( 'SELECT * FROM ' . $t . " WHERE owner_id = %d AND deleted_at IS NULL AND (COALESCE(paid_date, due_date) IS NULL OR COALESCE(paid_date, due_date) >= %s OR status = 'pending') ORDER BY id ASC LIMIT 60000", $owner, $since ), ARRAY_A );
		$seen = array();
		foreach ( $rows as $r ) { $seen[ (int) $r['id'] ] = 1; }
		/* older charges that are still unpaid */
		$old = array();
		foreach ( $states as $id => $st ) { if ( 'paid' !== $st[0] && ! isset( $seen[ $id ] ) ) { $old[] = (int) $id; } }
		foreach ( array_chunk( $old, 500 ) as $chunk ) {
			$rows = array_merge( $rows, (array) $wpdb->get_results( 'SELECT * FROM ' . $t . ' WHERE id IN (' . implode( ',', $chunk ) . ')', ARRAY_A ) );
		}
		return nlrm_ledger_rows( $rows, $states );
	}
}
if ( ! function_exists( 'nlrm_lease_pack' ) ) {
	/* after a money action: the lease's summary and its whole history */
	function nlrm_lease_pack( $owner, $lease_id, $extra = array() ) {
		global $wpdb;
		$states = array();
		$money = nlrm_money( $owner, null, array( (int) $lease_id ), $states );
		$rows = $wpdb->get_results( $wpdb->prepare( 'SELECT * FROM ' . nlrm_t( 'ledger' ) . ' WHERE owner_id = %d AND lease_id = %d ORDER BY id ASC', $owner, $lease_id ), ARRAY_A );
		return array_merge( array( 'lease_id' => (int) $lease_id, 'money' => (object) $money, 'rows' => nlrm_ledger_rows( $rows, $states ), 'lease' => nlrm_get( 'lease', (int) $lease_id, $owner ) ), $extra );
	}
}
if ( ! function_exists( 'nlrm_docs_meta' ) ) {
	function nlrm_docs_meta( $owner ) {
		global $wpdb;
		$rows = $wpdb->get_results( $wpdb->prepare( 'SELECT id, scope, scope_id, kind, name, mime, size, created_by, created_at FROM ' . nlrm_t( 'docs' ) . ' WHERE owner_id = %d AND deleted_at IS NULL ORDER BY id DESC LIMIT 2000', $owner ), ARRAY_A );
		return array_map( function ( $r ) {
			$r['id'] = (int) $r['id']; $r['scope_id'] = (int) $r['scope_id']; $r['size'] = (int) $r['size'];
			return $r;
		}, (array) $rows );
	}
}

/* ---------- plans: inc/rentals/billing.php (the landlord's subscription) ---------- */
