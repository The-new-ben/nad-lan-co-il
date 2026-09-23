# -*- coding: utf-8 -*-
"""An owner's journey on the new /post-listing/ engine, as the admin user (app password), built as a DRAFT (test=1).
python e2e_owner.py run            photos, message, build (draft), my listings
python e2e_owner.py publish ID     publish for a few minutes, IndexNow detached, re-render
python e2e_owner.py trash ID DROP  back to draft, to the trash, and the test contact removed from the user"""
import importlib.util, io, json, secrets, sys, time, urllib.request, urllib.error
from PIL import Image, ImageDraw
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
ARGS = sys.argv[1:]
sys.argv = ["x"]
spec = importlib.util.spec_from_file_location("ms", r"C:/Users/777/nad-lan/nad-lan-co-il/handoff/meital-2026-09-17/runners/meital_site.py")
m = importlib.util.module_from_spec(spec)
try:
    spec.loader.exec_module(m)
except SystemExit:
    pass
API = "https://nad-lan.co.il/wp-json/nadlan/v1/owner"
MSG = ("להשכרה: דירת 3 חדרים ביפו, 75 מ\"ר, קומה 2 מתוך 4 בלי מעלית. מרפסת 6 מ\"ר, מזגנים בכל החדרים, מרוהטת חלקית. "
       "7,200 ש\"ח לחודש. כניסה ב-1.11.")


def photo(i):
    im = Image.new("RGB", (1500, 1000), (226, 221, 210))
    d = ImageDraw.Draw(im)
    d.rectangle([60, 60, 1440, 940], outline=(31, 75, 92), width=6)
    d.text((90, 90), "TEST PHOTO %d (nad-lan owner check)" % i, fill=(31, 75, 92))
    b = io.BytesIO()
    im.save(b, "JPEG", quality=82)
    return b.getvalue()


def call(method, path, body=None, raw=None, ctype="application/json"):
    data = raw if raw is not None else (None if body is None else json.dumps(body, ensure_ascii=False).encode())
    r = urllib.request.Request(API + path, data=data, method=method, headers={"Authorization": m.AUTH, "User-Agent": "nadlan-runner", "Content-Type": ctype})
    try:
        with urllib.request.urlopen(r, timeout=200) as x:
            return x.status, json.loads(x.read().decode())
    except urllib.error.HTTPError as e:
        return e.code, json.loads(e.read().decode() or "null")


def bridge(payload):
    tok = secrets.token_hex(24)
    code = r'''
add_action( 'rest_api_init', function () {
	register_rest_route( 'nadlan-ownertest/v1', '/run', array( 'methods' => 'POST', 'permission_callback' => function () { return current_user_can( 'manage_options' ); },
		'callback' => function ( $req ) {
			$b = $req->get_json_params();
			if ( ! hash_equals( '__T__', (string) ( $b['token'] ?? '' ) ) ) { return new WP_Error( 'x', 'x', array( 'status' => 403 ) ); }
			remove_action( 'save_post', 'nadlan_config_indexnow_on_save', 20 );
			$id = (int) $b['id'];
			if ( get_post_type( $id ) !== 'nadlan_property' || get_post_meta( $id, 'nl_owner', true ) !== '1' || strpos( (string) get_post_meta( $id, 'nl_owner_contact', true ), '0000000' ) === false ) { return new WP_Error( 'refused', 'not the owner test listing', array( 'status' => 403 ) ); }
			if ( $b['op'] === 'publish' ) {
				wp_update_post( array( 'ID' => $id, 'post_status' => 'publish' ) );
				nl_drop_render_all( $id, nl_owner_from_listing( $id ) );
				nl_drop_purge( array( $id ) );
				return array( get_post_status( $id ), get_permalink( $id ) );
			}
			if ( $b['op'] === 'trash' ) {
				wp_update_post( array( 'ID' => $id, 'post_status' => 'draft' ) );
				$out = array( $id => wp_trash_post( $id ) ? 'trashed' : 'failed' );
				$d = (int) $b['drop'];
				if ( get_post_type( $d ) === 'nadlan_drop' ) { $out[ $d ] = wp_trash_post( $d ) ? 'trashed drop' : 'failed'; }
				$u = (int) get_post_meta( $id, 'owner_user_id', true );
				delete_user_meta( $u, 'nl_owner_phone' ); delete_user_meta( $u, 'nl_owner_name' );
				nl_drop_purge( array( $id ) );
				return $out;
			}
			return new WP_Error( 'op', 'op' );
		} ) );
} );
'''.replace("__T__", tok)
    s, c = m.req("POST", "/code-snippets/v1/snippets", {"name": "tmp-ownertest-%d" % time.time(), "code": "/* x */", "scope": "global", "active": False})
    sid = c["id"]
    try:
        m.req("PUT", "/code-snippets/v1/snippets/%d" % sid, {"name": c["name"], "code": code, "scope": "global", "active": False})
        m.req("PUT", "/code-snippets/v1/snippets/%d/activate" % sid, {})
        payload["token"] = tok
        return m.req("POST", "/nadlan-ownertest/v1/run", payload)
    finally:
        m.req("PUT", "/code-snippets/v1/snippets/%d/deactivate" % sid, {})
        m.req("DELETE", "/code-snippets/v1/snippets/%d" % sid)


if ARGS[0] == "run":
    ids = []
    for i in (1, 2):
        bnd = "----nl%d" % time.time_ns()
        body = (("--%s\r\nContent-Disposition: form-data; name=\"photo\"; filename=\"owner-%d.jpg\"\r\nContent-Type: image/jpeg\r\n\r\n" % (bnd, i)).encode() + photo(i) + ("\r\n--%s--\r\n" % bnd).encode())
        s, j = call("POST", "/photo", raw=body, ctype="multipart/form-data; boundary=" + bnd)
        print("photo", i, s, j.get("id"))
        ids.append(j["id"])
    t0 = time.time()
    s, r = call("POST", "/submit", {"text": MSG, "photos": ids, "name": "בדיקה", "phone": "052-0000000", "who": "owner", "owner": "1", "consent": "1"})
    print("submit:", s, round(time.time() - t0, 1), "s", json.dumps(r, ensure_ascii=False)[:300])
    t0 = time.time()
    s, r = call("POST", "/build/%d" % r["drop"], {"test": "1"})
    print("build:", s, round(time.time() - t0, 1), "s", json.dumps(r, ensure_ascii=False)[:500])
    s, L = call("GET", "/listings")
    print("my listings:", s, json.dumps(L, ensure_ascii=False)[:400])
elif ARGS[0] == "publish":
    print(bridge({"op": "publish", "id": int(ARGS[1])}))
elif ARGS[0] == "trash":
    print(bridge({"op": "trash", "id": int(ARGS[1]), "drop": int(ARGS[2])}))
