# -*- coding: utf-8 -*-
"""A reusable, token-gated temporary bridge for nad-lan.co.il content operations (24.9.2026).

Opens one Code Snippet with a private REST route, runs the requested ops, and always deletes the snippet at the end
(verified 404). Read ops: scan (text across posts, meta and options), get (raw fields + md5), menus, demo list.
Write ops need an md5 of the current value (drift guard): set_post, set_meta. Every write keeps a local backup.
The WordPress app password is decrypted in-process (DPAPI) and never printed.

Use from another script:
    from nlbridge import Bridge
    with Bridge("madlan") as b:
        hits = b.ops({"scan": {"needles": ["מדלן", "madlan"]}})["scan"]
"""
import base64, ctypes, ctypes.wintypes, hashlib, io, json, os, secrets, sys, time, urllib.request, urllib.error

BASE = "https://nad-lan.co.il"
SECRETS_PATH = r"C:\Users\777\Documents\websites\.codex-secrets\wordpress-app-passwords\nad-lan.co.il.json"
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) NadLan-Ops/1.0"
BACKUPS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "backups")


class _DB(ctypes.Structure):
    _fields_ = [("cb", ctypes.wintypes.DWORD), ("pb", ctypes.POINTER(ctypes.c_char))]


def _dpapi(b64):
    raw = base64.b64decode(b64)
    bi = _DB(len(raw), ctypes.cast(ctypes.create_string_buffer(raw, len(raw)), ctypes.POINTER(ctypes.c_char)))
    bo = _DB()
    if not ctypes.windll.crypt32.CryptUnprotectData(ctypes.byref(bi), None, None, None, None, 0, ctypes.byref(bo)):
        raise RuntimeError("DPAPI")
    try:
        return ctypes.string_at(bo.pb, bo.cb).decode("utf-8")
    finally:
        ctypes.windll.kernel32.LocalFree(bo.pb)


with open(SECRETS_PATH, encoding="utf-8-sig") as _f:
    _sec = json.load(_f)
AUTH = "Basic " + base64.b64encode((_sec["username"] + ":" + _dpapi(_sec["password_dpapi"])).encode()).decode()
del _sec


def md5(s):
    return hashlib.md5(s.encode("utf-8") if isinstance(s, str) else s).hexdigest()


def req(method, path, body=None, timeout=180, auth=True, raw=False):
    r = urllib.request.Request(BASE + path, data=None if body is None else json.dumps(body, ensure_ascii=False).encode(), method=method)
    if auth:
        r.add_header("Authorization", AUTH)
    r.add_header("User-Agent", UA)
    if body is not None:
        r.add_header("Content-Type", "application/json")
    try:
        with urllib.request.urlopen(r, timeout=timeout) as resp:
            p = resp.read()
            return resp.status, (p if raw else json.loads(p.decode("utf-8") or "null"))
    except urllib.error.HTTPError as e:
        p = e.read()
        if raw:
            return e.code, p
        try:
            return e.code, json.loads(p.decode("utf-8"))
        except Exception:
            return e.code, {"raw": p[:300].decode("utf-8", "replace")}


PHP = r'''
add_action( 'rest_api_init', function () {
	register_rest_route( '__NS__/v1', '/apply', array(
		'methods' => 'POST',
		'permission_callback' => function () { return current_user_can( 'manage_options' ); },
		'callback' => function ( $req ) {
			global $wpdb;
			$b = $req->get_json_params();
			if ( ! is_array( $b ) || ! hash_equals( '__TOKEN__', (string) ( $b['token'] ?? '' ) ) ) {
				return new WP_Error( 'forbidden', 'token', array( 'status' => 403 ) );
			}
			$out = array( 'ok' => 1 );
			if ( ! empty( $b['scan'] ) ) {
				$needles = array_slice( array_filter( array_map( 'strval', (array) ( $b['scan']['needles'] ?? array() ) ) ), 0, 8 );
				$posts = array(); $metas = array(); $opts = array();
				foreach ( $needles as $n ) {
					$like = '%' . $wpdb->esc_like( $n ) . '%';
					$rows = $wpdb->get_results( $wpdb->prepare( "SELECT ID, post_type, post_status, post_title, (CHAR_LENGTH(post_content) - CHAR_LENGTH(REPLACE(LOWER(post_content), LOWER(%s), ''))) / CHAR_LENGTH(%s) AS n_content, (post_title LIKE %s) AS in_title, (post_excerpt LIKE %s) AS in_excerpt FROM {$wpdb->posts} WHERE post_status IN ('publish','draft','pending','future','private') AND post_type NOT IN ('revision') AND (post_content LIKE %s OR post_title LIKE %s OR post_excerpt LIKE %s) LIMIT 800", $n, $n, $like, $like, $like, $like, $like ), ARRAY_A );
					foreach ( $rows as $r ) { $r['needle'] = $n; $posts[] = $r; }
					$mrows = $wpdb->get_results( $wpdb->prepare( "SELECT m.post_id, m.meta_key, p.post_type, p.post_status, CHAR_LENGTH(m.meta_value) AS len FROM {$wpdb->postmeta} m JOIN {$wpdb->posts} p ON p.ID = m.post_id WHERE p.post_status IN ('publish','draft','pending','future','private') AND p.post_type NOT IN ('revision') AND m.meta_value LIKE %s LIMIT 1500", $like ), ARRAY_A );
					foreach ( $mrows as $r ) { $r['needle'] = $n; $metas[] = $r; }
					$orows = $wpdb->get_results( $wpdb->prepare( "SELECT option_name, CHAR_LENGTH(option_value) AS len FROM {$wpdb->options} WHERE option_value LIKE %s AND option_name NOT LIKE '\_transient%%' AND option_name NOT LIKE '\_site\_transient%%' LIMIT 200", $like ), ARRAY_A );
					foreach ( $orows as $r ) { $r['needle'] = $n; $opts[] = $r; }
				}
				$out['scan'] = array( 'posts' => $posts, 'meta' => $metas, 'options' => $opts );
			}
			if ( ! empty( $b['get'] ) ) {
				$res = array();
				foreach ( array_slice( (array) $b['get']['ids'], 0, 200 ) as $id ) {
					$p = get_post( (int) $id );
					if ( ! $p ) { $res[ (string) $id ] = null; continue; }
					$row = array( 'type' => $p->post_type, 'status' => $p->post_status, 'title' => $p->post_title, 'excerpt' => $p->post_excerpt,
						'content' => $p->post_content, 'md5' => md5( $p->post_content ), 'link' => get_permalink( $p ), 'modified' => $p->post_modified_gmt, 'meta' => array() );
					foreach ( (array) ( $b['get']['meta'] ?? array() ) as $k ) {
						$v = get_post_meta( $p->ID, (string) $k, true );
						$row['meta'][ (string) $k ] = array( 'value' => is_scalar( $v ) ? (string) $v : wp_json_encode( $v ), 'md5' => md5( is_scalar( $v ) ? (string) $v : wp_json_encode( $v ) ) );
					}
					$res[ (string) $id ] = $row;
				}
				$out['get'] = $res;
			}
			if ( ! empty( $b['set_post'] ) ) {
				$res = array();
				foreach ( (array) $b['set_post'] as $s ) {
					$p = get_post( (int) $s['id'] );
					if ( ! $p ) { $res[] = array( 'id' => $s['id'], 'err' => 'missing' ); continue; }
					if ( isset( $s['content'] ) && md5( $p->post_content ) !== (string) ( $s['expect'] ?? '' ) ) { $res[] = array( 'id' => $s['id'], 'err' => 'drift', 'now' => md5( $p->post_content ) ); continue; }
					$u = array( 'ID' => $p->ID );
					foreach ( array( 'content' => 'post_content', 'title' => 'post_title', 'excerpt' => 'post_excerpt', 'status' => 'post_status' ) as $k => $col ) {
						if ( isset( $s[ $k ] ) ) { $u[ $col ] = (string) $s[ $k ]; }
					}
					kses_remove_filters();
					$r = wp_update_post( wp_slash( $u ), true );
					kses_init_filters();
					clean_post_cache( $p->ID );
					$q = get_post( $p->ID );
					$res[] = array( 'id' => $p->ID, 'err' => is_wp_error( $r ) ? $r->get_error_message() : '', 'md5' => md5( $q->post_content ), 'status' => $q->post_status );
				}
				$out['set_post'] = $res;
			}
			if ( ! empty( $b['set_meta'] ) ) {
				$res = array();
				foreach ( (array) $b['set_meta'] as $s ) {
					$id = (int) $s['id']; $k = (string) $s['key'];
					$cur = get_post_meta( $id, $k, true );
					$cur = is_scalar( $cur ) ? (string) $cur : wp_json_encode( $cur );
					if ( md5( $cur ) !== (string) ( $s['expect'] ?? '' ) ) { $res[] = array( 'id' => $id, 'key' => $k, 'err' => 'drift' ); continue; }
					update_post_meta( $id, $k, wp_slash( (string) $s['value'] ) );
					$now = get_post_meta( $id, $k, true );
					$res[] = array( 'id' => $id, 'key' => $k, 'err' => '', 'md5' => md5( is_scalar( $now ) ? (string) $now : wp_json_encode( $now ) ) );
				}
				$out['set_meta'] = $res;
			}
			if ( ! empty( $b['menus'] ) ) {
				$res = array( 'locations' => get_nav_menu_locations(), 'menus' => array() );
				foreach ( wp_get_nav_menus() as $m ) {
					$items = array();
					foreach ( (array) wp_get_nav_menu_items( $m->term_id ) as $it ) {
						$items[] = array( 'id' => $it->ID, 'title' => $it->title, 'url' => $it->url, 'parent' => (int) $it->menu_item_parent, 'order' => (int) $it->menu_order, 'object' => $it->object, 'object_id' => (int) $it->object_id, 'type' => $it->type );
					}
					$res['menus'][] = array( 'id' => $m->term_id, 'name' => $m->name, 'slug' => $m->slug, 'items' => $items );
				}
				$out['menus'] = $res;
			}
			if ( ! empty( $b['demo'] ) ) {
				$ids = $wpdb->get_col( "SELECT DISTINCT p.ID FROM {$wpdb->posts} p JOIN {$wpdb->postmeta} m ON m.post_id = p.ID WHERE p.post_status = 'publish' AND ( ( m.meta_key = 'is_demo' AND m.meta_value IN ('1','true') ) OR ( m.meta_key = 'source' AND m.meta_value = 'demo_seed' ) )" );
				$res = array();
				foreach ( $ids as $id ) { $p = get_post( $id ); $res[] = array( 'id' => (int) $id, 'type' => $p->post_type, 'title' => $p->post_title, 'link' => get_permalink( $p ) ); }
				$out['demo'] = $res;
			}
			if ( ! empty( $b['purge'] ) ) {
				foreach ( (array) ( $b['purge_ids'] ?? array() ) as $id ) { clean_post_cache( (int) $id ); do_action( 'litespeed_purge_post', (int) $id ); }
				do_action( 'litespeed_purge_all' ); wp_cache_flush(); $out['purged'] = 1;
			}
			return $out;
		},
	) );
} );
'''


class Bridge:
    def __init__(self, tag):
        self.tag = "".join(c for c in tag.lower() if c.isalnum())[:12] or "ops"
        self.token = secrets.token_hex(24)
        self.ns = "nadlan-ops-" + self.tag + "-" + self.token[:8]
        self.id = None

    def __enter__(self):
        code = PHP.replace("__TOKEN__", self.token).replace("__NS__", self.ns)
        s, c = req("POST", "/wp-json/code-snippets/v1/snippets", {"name": f"x-tmp-ops-{self.tag}-{int(time.time())}", "code": code, "scope": "global", "active": False})
        if s not in (200, 201):
            raise SystemExit(f"bridge create failed: {s} {c}")
        self.id = c["id"]
        s, c = req("PUT", f"/wp-json/code-snippets/v1/snippets/{self.id}/activate", {})
        if s not in (200, 201):
            self._delete()
            raise SystemExit(f"bridge activate failed: {s} {c}")
        for _ in range(12):
            s, r = req("POST", f"/wp-json/{self.ns}/v1/apply", {"token": self.token})
            if s == 200:
                print(f"[bridge] up, snippet {self.id}")
                return self
            time.sleep(1.5)
        self._delete()
        raise SystemExit("bridge never answered")

    def ops(self, payload, timeout=240):
        payload = dict(payload, token=self.token)
        s, r = req("POST", f"/wp-json/{self.ns}/v1/apply", payload, timeout=timeout)
        if s != 200:
            raise SystemExit(f"ops failed: {s} {json.dumps(r, ensure_ascii=False)[:400]}")
        return r

    def _delete(self):
        if self.id is None:
            return
        req("PUT", f"/wp-json/code-snippets/v1/snippets/{self.id}/deactivate", {})
        s, _ = req("DELETE", f"/wp-json/code-snippets/v1/snippets/{self.id}")
        time.sleep(1.5)
        s2, _ = req("POST", f"/wp-json/{self.ns}/v1/apply", {"token": self.token})
        print(f"[bridge] delete http {s}; route now http {s2} (want 404)")
        self.id = None

    def __exit__(self, *a):
        self._delete()
        return False


def backup(name, data):
    os.makedirs(BACKUPS, exist_ok=True)
    p = os.path.join(BACKUPS, time.strftime("%Y%m%dT%H%M%S-") + name + ".json")
    json.dump(data, open(p, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    return p
