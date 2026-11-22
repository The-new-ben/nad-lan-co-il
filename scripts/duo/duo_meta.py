# -*- coding: utf-8 -*-
"""DUO fact audit (22.11.2026), the search descriptions: the Yoast meta description of the DUO posts still carried the old facts
(54 floors, "372 of 510 sold"). Read-only by default: prints each post's current _yoast_wpseo_metadesc and the proposed text.
--go writes ONLY the posts whose current value equals the expected old text exactly (anchored), through a temporary admin bridge
that is always deleted; backup in docs/research/2026-11-22-duo-audit/backup/meta-<stamp>.json.
The page titles are NOT touched (a title change needs Ben's wording)."""
import json, os, secrets, sys, time
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.dirname(os.path.dirname(HERE))
_src = open(os.path.join(REPO, "scripts", "skin-a", "deployskin.py"), encoding="utf-8").read()
_ns = {"__name__": "duometa"}
exec(compile(_src[:_src.index('s, h, _ = req("GET", "/wp-json/nadlan/v1/health")')], "h", "exec"), _ns)
req, must, snip = _ns["req"], _ns["must"], _ns["snip"]
GO = "--go" in sys.argv
KEY = "_yoast_wpseo_metadesc"
FIX = {  # 22.11 second pass: only the French description, shortened to 148 characters (the first pass made it 196)
    5195: ("DUO Tel Aviv réunit deux tours de 50 étages au carrefour d'Ibn Gabirol, Arlozorov et Ben Saruk, au centre de Tel-Aviv : 668 appartements, prix datés, chantier et achat depuis l'étranger.",
           "DUO Tel Aviv : deux tours de 50 étages au carrefour d'Ibn Gabirol et d'Arlozorov, 668 appartements, prix datés, chantier et achat depuis l'étranger."),
}
IDS = [4893, 5194, 5195, 5196, 5197]
TOKEN = secrets.token_hex(24)
BRIDGE = r'''
add_action( 'rest_api_init', function () {
	register_rest_route( 'nadlan-duo-meta/v1', '/m', array(
		'methods' => 'POST',
		'permission_callback' => function () { return current_user_can( 'manage_options' ); },
		'callback' => function ( $req ) {
			$b = $req->get_json_params();
			if ( ! is_array( $b ) || ! hash_equals( '__TOKEN__', (string) ( $b['token'] ?? '' ) ) ) { return new WP_Error( 'forbidden', 'token', array( 'status' => 403 ) ); }
			$out = array();
			foreach ( (array) ( $b['read'] ?? array() ) as $id ) { $out['read'][ (int) $id ] = (string) get_post_meta( (int) $id, '_yoast_wpseo_metadesc', true ); }
			foreach ( (array) ( $b['write'] ?? array() ) as $w ) {
				$id = (int) $w['id']; $cur = (string) get_post_meta( $id, '_yoast_wpseo_metadesc', true );
				if ( $cur !== (string) $w['old'] ) { $out['write'][ $id ] = 'skip: current differs'; continue; }
				update_post_meta( $id, '_yoast_wpseo_metadesc', wp_slash( (string) $w['new'] ) );
				clean_post_cache( $id );
				$out['write'][ $id ] = ( (string) get_post_meta( $id, '_yoast_wpseo_metadesc', true ) === (string) $w['new'] ) ? 'ok' : 'read-back differs';
			}
			return $out;
		},
	) );
} );
'''.replace("__TOKEN__", TOKEN)
s, c = snip("POST", "", {"name": "tmp-duo-meta-%d" % int(time.time()), "code": "/* placeholder */", "scope": "global", "active": False})
must(s, c, "bridge create")
BR = c["id"]
try:
    s, u = snip("PUT", "/%s" % BR, {"name": c["name"], "code": BRIDGE, "scope": "global", "active": False}); must(s, u, "bridge update")
    s, a = snip("PUT", "/%s/activate" % BR, {}); must(s, a, "bridge activate")
    s, r, _ = req("POST", "/wp-json/nadlan-duo-meta/v1/m", {"token": TOKEN, "read": IDS}); must(s, r, "read")
    cur = {int(k): v for k, v in r["read"].items()}
    for pid in IDS:
        print(pid, "NOW:", cur[pid][:170])
        if pid in FIX:
            print("     ", "MATCHES OLD" if cur[pid] == FIX[pid][0] else "DIFFERS FROM EXPECTED OLD", "-> NEW:", FIX[pid][1][:170])
    if GO:
        bk = os.path.join(REPO, "docs", "research", "2026-11-22-duo-audit", "backup"); os.makedirs(bk, exist_ok=True)
        json.dump(cur, open(os.path.join(bk, "meta-%s.json" % time.strftime("%Y%m%dT%H%M%S")), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
        s, w, _ = req("POST", "/wp-json/nadlan-duo-meta/v1/m", {"token": TOKEN, "write": [{"id": k, "old": v[0], "new": v[1]} for k, v in FIX.items()]}); must(s, w, "write")
        print("[write]", w.get("write"))
finally:
    s1, _ = snip("PUT", "/%s/deactivate" % BR, {}); s2, _ = snip("DELETE", "/%s" % BR, None)
    print("[bridge] cleanup", s1, s2)
