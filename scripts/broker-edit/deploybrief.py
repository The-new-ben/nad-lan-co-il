# -*- coding: utf-8 -*-
"""Broker self-edit (x-broker-edit) deploy and test fixtures (HAD-543 follow-up, Ben 20.10.2026: "she should be able to
edit everything").

  python deployedit.py                 lint locally, install/update the Code Snippet "x-broker-brief", activate, verify
  python deployedit.py --off           deactivate it (the private page returns to x-broker-drop alone)
  python deployedit.py --fixtures      two DRAFT test listings owned by Meital (7833), never public:
                                       T-old = a copy of 7634 without stored facts (tests "prepare for editing"),
                                       T-new = a copy of 8456 with its facts, copy and photos (tests every edit)
  python deployedit.py --cleanup       the test drafts to the trash (WordPress trash: reversible)
The app password is decrypted in-process (DPAPI) and never printed. Fixture ids are kept in fixtures.json beside this file.
"""
import json, os, re, secrets, subprocess, sys, time
HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(HERE))
SRC = os.path.join(REPO, "plugins", "nadlan-config", "inc", "broker-brief.php")
src = open(os.path.join(REPO, "scripts", "skin-a", "deployskin.py"), encoding="utf-8").read(); ns = {"__name__": "de"}
exec(compile(src[:src.index('s, h, _ = req("GET", "/wp-json/nadlan/v1/health")')], "h", "exec"), ns)
req, snip = ns["req"], ns["snip"]
ARGS = sys.argv[1:]
NAME = "x-broker-brief"
FIX = os.path.join(HERE, "fixtures.json")


def find(name):
    s, lst = snip("GET", "")
    return next((x for x in lst if x.get("name") == name), None)


def bridge(ops_php, payload):
    tok = secrets.token_hex(24)
    code = r"""
add_action( 'rest_api_init', function () {
	register_rest_route( 'nadlan-edit-ops/v1', '/run', array( 'methods' => 'POST',
		'permission_callback' => function () { return current_user_can( 'manage_options' ); },
		'callback' => function ( $req ) {
			$b = $req->get_json_params();
			if ( ! is_array( $b ) || ! hash_equals( '__T__', (string) ( $b['token'] ?? '' ) ) ) { return new WP_Error( 'forbidden', 'token', array( 'status' => 403 ) ); }
			__OPS__
		} ) );
} );
""".replace("__T__", tok).replace("__OPS__", ops_php)
    s, c = snip("POST", "", {"name": f"tmp-edit-ops-{int(time.time())}", "code": "/* placeholder */", "scope": "global", "active": False})
    br = c["id"]
    try:
        snip("PUT", f"/{br}", {"name": c["name"], "code": code, "scope": "global", "active": False}); snip("PUT", f"/{br}/activate", {}); time.sleep(1.5)
        payload["token"] = tok
        s2, out, _ = req("POST", "/wp-json/nadlan-edit-ops/v1/run", payload)
        return s2, out
    finally:
        snip("POST", f"/{br}/deactivate", {}); s3, _ = snip("DELETE", f"/{br}", None); time.sleep(1)
        s4, _, _ = req("POST", "/wp-json/nadlan-edit-ops/v1/run", {"token": "x"})
        print("[bridge] deleted", s3, "route now", s4, "(want 404)")


s, h, _ = req("GET", "/wp-json/nadlan/v1/health")
print("[health]", h.get("version"), h.get("status"))

if "--off" in ARGS:
    x = find(NAME)
    print(NAME, "deactivate", snip("PUT", f"/{x['id']}/deactivate", {})[0] if x else "not installed")
    raise SystemExit(0)

if "--fixtures" in ARGS:
    OPS = r"""
			$mk = function ( $from, $title, $keep_meta ) {
				$p = get_post( $from );
				$id = wp_insert_post( array( 'post_type' => 'nadlan_property', 'post_status' => 'draft', 'post_title' => $title, 'post_content' => $p->post_content, 'post_excerpt' => $p->post_excerpt, 'post_name' => 'nle-test-' . $from . '-' . time() ), true );
				if ( is_wp_error( $id ) ) { return $id; }
				foreach ( array( 'nl_broker_id', 'listing_type', 'price', 'rooms', 'nl_status', 'status' ) as $k ) { update_post_meta( $id, $k, get_post_meta( $from, $k, true ) ); }
				if ( $keep_meta ) { foreach ( array( 'nl_facts', 'nl_copy', 'nl_photos_json', 'photos_csv', 'source', 'nl_drop_id' ) as $k ) { update_post_meta( $id, $k, wp_slash( get_post_meta( $from, $k, true ) ) ); } }
				$t = get_post_thumbnail_id( $from ); if ( $t ) { set_post_thumbnail( $id, $t ); }
				update_post_meta( $id, 'nl_edit_test', '1' );
				return $id;
			};
			$old = $mk( 7634, 'בדיקת עריכה פנימית (מודעה ישנה), לא לפרסום', false );
			$new = $mk( 8456, 'בדיקת עריכה פנימית (מודעה חדשה), לא לפרסום', true );
			return array( 'old' => $old, 'new' => $new );
"""
    s2, out = bridge(OPS, {})
    print("fixtures", s2, out)
    json.dump(out, open(FIX, "w"), indent=1)
    raise SystemExit(0)

if "--cleanup" in ARGS:
    fx = json.load(open(os.path.join(HERE, "fixtures-all.json")) if os.path.exists(os.path.join(HERE, "fixtures-all.json")) else open(FIX))
    OPS = r"""
			$out = array();
			foreach ( (array) ( $b['ids'] ?? array() ) as $id ) {
				$id = (int) $id;
				if ( get_post_meta( $id, 'nl_edit_test', true ) !== '1' ) { $out[ $id ] = 'not a test post: left alone'; continue; }
				$out[ $id ] = wp_trash_post( $id ) ? 'trashed' : 'failed';
			}
			return $out;
"""
    s2, out = bridge(OPS, {"ids": fx.get("all") or [fx.get("old"), fx.get("new")]})
    print("cleanup", s2, out)
    raise SystemExit(0)

# install
r = subprocess.run(["php", "-l", SRC], capture_output=True, text=True)
print("[lint]", r.stdout.strip() or r.stderr.strip())
if r.returncode != 0:
    raise SystemExit("FATAL: lint")
code = re.sub(r"^\s*<\?php\s*", "", open(SRC, encoding="utf-8").read(), count=1)
x = find(NAME)
body = {"name": NAME, "code": code, "scope": "global", "active": False,
        "desc": "Material request for one property: a private upload and questions page per brief. Source: plugins/nadlan-config/inc/broker-brief.php"}
if x:
    sid = x["id"]; s3, u = snip("PUT", f"/{sid}", body); print("[snippet] update", s3)
else:
    s3, c3 = snip("POST", "", body); sid = c3["id"]; print("[snippet] create", s3, sid)
s4, a = snip("PUT", f"/{sid}/activate", {}); print("[snippet] activate", s4, (a or {}).get("active") if isinstance(a, dict) else a)
time.sleep(2)
s5, h2, _ = req("GET", "/wp-json/nadlan/v1/health")
print("[health after]", s5, h2.get("version") if isinstance(h2, dict) else h2, h2.get("status") if isinstance(h2, dict) else "")
if s5 != 200 or (isinstance(h2, dict) and h2.get("status") != "ok"):
    snip("PUT", f"/{sid}/deactivate", {}); raise SystemExit("ROLLED BACK: health not ok after activation")
s6, page, _ = req("GET", "/", None, raw=True, auth=False)
print("[home]", s6, "ok" if s6 == 200 else "BAD")
if s6 != 200:
    snip("PUT", f"/{sid}/deactivate", {}); raise SystemExit("ROLLED BACK: home page not 200")
print("x-broker-edit ACTIVE, id", sid)
