# -*- coding: utf-8 -*-
"""Kikar V8 step 2b (design v104.27, DS version 176, 2.10.2026): Kikar Hamedina enters the neighbours' table "פרויקטים סמוכים
להשוואה". The table (inc/project-experience.php, nadlan_pjx_comps) lists the six nearest projects that carry
project_3d_avg_price_per_sqm; Kikar had none. It gets 65,000: the towers' published deal average, "כ-65,000 ₪ למ״ר", the same number
as its own deals paragraph (docs/research/2026-09-30-kikar-hamedina/facts.md: mako 24.9.2026, Globes 23.9.2025; the conservative
figure, the three upper-floor deals average about 71,000).

Runs only after 1.72.399 is live (the generic ~90 m2 finance line skips world pages). Steps, through a temporary admin bridge:
  1. read the post (slug hamedina, id 8113) and its current value: it must be empty;
  2. set the meta, read it back, clear the comps cache (transients nlpjx_comps_v2_*), purge;
  3. checks: the comps API of DUO and Rainbow lists Kikar; Kikar's price section shows ~65,000 and still no finance estimate;
     DUO's page lists Kikar in its table; Rainbow keeps its own estimate. Any failure deletes the meta again (the value before
     was empty), clears the cache and purges. The bridge is always deleted.
The app password is decrypted in-process (DPAPI) and never printed.   python scripts/project-stage/kikar_ppsqm_v8.py [--dry]"""
import io, json, os, secrets, sys, time
HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(HERE))
DRY = "--dry" in sys.argv
PID, SLUG, KEY, VAL = 8113, "hamedina", "project_3d_avg_price_per_sqm", "65000"
QA = os.path.join(REPO, "docs", "qa", "v8-traffic")

_src = open(os.path.join(REPO, "scripts", "skin-a", "deployskin.py"), encoding="utf-8").read()
_ns = {"__name__": "kikar_ppsqm_v8_helpers"}
exec(compile(_src[:_src.index('s, h, _ = req("GET", "/wp-json/nadlan/v1/health")')], "deployskin-helpers", "exec"), _ns)
req, must, snip = _ns["req"], _ns["must"], _ns["snip"]


def page(path):
    s, b, _ = req("GET", path + ("&" if "?" in path else "?") + "nlv8=" + str(int(time.time() * 1000)), raw=True, auth=False,
                  headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/130 Safari/537.36"})
    t = b.decode("utf-8", "replace") if isinstance(b, (bytes, bytearray)) else json.dumps(b)
    i = t.find("<body")
    return s, (t[i:] if i > -1 else t)


def comps_of(pid):
    s, b = page(f"/wp-json/nadlan/v1/comps?id={pid}")
    try:
        return [c["url"].split("/projects/")[1].strip("/") for c in json.loads(b)["comps"]]
    except Exception:  # noqa: BLE001
        return []


def checks(tag):
    bad = []
    duo, rb = comps_of(4893), comps_of(4464)
    print(f"[{tag}] comps DUO {duo}")
    print(f"[{tag}] comps Rainbow {rb}")
    if SLUG not in duo:
        bad.append("DUO comps lack Kikar")
    if SLUG not in rb:
        bad.append("Rainbow comps lack Kikar")
    s, k = page("/projects/hamedina/")
    seg = k[k.find('id="nlpjx-price"'):k.find('id="nlpjx-price"') + 3000] if 'id="nlpjx-price"' in k else ""
    if s != 200 or "~65,000 ₪/מ״ר" not in seg:
        bad.append("Kikar price section lacks ~65,000")
    if "nlpjx-fin-est" in k:
        bad.append("Kikar shows the generic finance estimate")
    s, d = page("/projects/duo-tel-aviv/")
    tbl = d[d.find('class="nlpjx-comps"'):d.find('class="nlpjx-comps"') + 4000] if 'class="nlpjx-comps"' in d else ""
    if s != 200 or "/projects/hamedina/" not in tbl:
        bad.append("DUO's table lacks the Kikar link")
    s, r = page("/projects/rainbow-tel-aviv/")
    if s != 200 or 'nlpjx-fin-est"><b>' not in r:
        bad.append("Rainbow lost its finance estimate")
    print(f"[{tag}] " + ("OK" if not bad else "BAD: " + "; ".join(bad)))
    return bad


s, h, _ = req("GET", "/wp-json/nadlan/v1/health"); must(s, h, "health"); print("[health]", h.get("version"), h.get("status"))
if h.get("version") != "1.72.399":
    raise SystemExit("FATAL: run after 1.72.399 is live (the finance line must skip world pages first)")
TOKEN = secrets.token_hex(24)
BRIDGE = r'''
add_action( 'rest_api_init', function () {
	register_rest_route( 'nadlan-v8-ops/v1', '/apply', array(
		'methods' => 'POST',
		'permission_callback' => function () { return current_user_can( 'manage_options' ); },
		'callback' => function ( $req ) {
			$b = $req->get_json_params();
			if ( ! is_array( $b ) || ! hash_equals( '__TOKEN__', (string) ( isset( $b['token'] ) ? $b['token'] : '' ) ) ) { return new WP_Error( 'forbidden', 'token', array( 'status' => 403 ) ); }
			$pid = __PID__; $key = '__KEY__';
			$p = get_post( $pid );
			if ( ! $p || 'nadlan_project' !== $p->post_type || '__SLUG__' !== $p->post_name ) { return new WP_Error( 'post', 'not the Kikar post', array( 'status' => 409 ) ); }
			$out = array( 'id' => $pid, 'slug' => $p->post_name, 'status' => $p->post_status );
			if ( ! empty( $b['set'] ) ) { update_post_meta( $pid, $key, '__VAL__' ); }
			if ( ! empty( $b['unset'] ) ) { delete_post_meta( $pid, $key ); }
			if ( ! empty( $b['clear'] ) ) {
				global $wpdb;
				$out['cleared'] = (int) $wpdb->query( "DELETE FROM {$wpdb->options} WHERE option_name LIKE '\\_transient\\_nlpjx\\_comps\\_v2\\_%' OR option_name LIKE '\\_transient\\_timeout\\_nlpjx\\_comps\\_v2\\_%'" );
				if ( function_exists( 'wp_cache_flush' ) ) { wp_cache_flush(); }
			}
			if ( ! empty( $b['purge'] ) ) { do_action( 'litespeed_purge_all' ); $out['purged'] = 1; }
			clean_post_cache( $pid );
			$out['exists'] = metadata_exists( 'post', $pid, $key );
			$out['value']  = (string) get_post_meta( $pid, $key, true );
			return $out;
		},
	) );
} );
'''.replace("__TOKEN__", TOKEN).replace("__PID__", str(PID)).replace("__KEY__", KEY).replace("__SLUG__", SLUG).replace("__VAL__", VAL)
s, c = snip("POST", "", {"name": f"tmp-v8-ppsqm-{int(time.time())}", "code": "/* placeholder */", "scope": "global", "active": False})
must(s, c, "bridge create")
BR = c["id"]
written, ok = False, False
rec = {"release": "Kikar V8 step 2b: project_3d_avg_price_per_sqm 65000 (design v104.27)", "at": time.strftime("%Y%m%dT%H%M%SZ", time.gmtime())}
try:
    s, u = snip("PUT", f"/{BR}", {"name": c["name"], "code": BRIDGE, "scope": "global", "active": False}); must(s, u, "bridge update")
    s, a = snip("PUT", f"/{BR}/activate", {}); must(s, a, "bridge activate")

    def ops(payload, what):
        payload["token"] = TOKEN
        s, r, _ = req("POST", "/wp-json/nadlan-v8-ops/v1/apply", payload, timeout=180); must(s, r, what); return r

    st = ops({}, "state"); print("[state]", st); rec["before"] = st
    if st.get("exists") and st.get("value") not in ("", "0"):
        raise SystemExit(f"FATAL: Kikar already has {KEY} = {st.get('value')!r}; diff before replacing")
    if DRY:
        print("[dry] stop here: nothing written")
    else:
        r = ops({"set": 1, "clear": 1, "purge": 1}, "set"); written = True; print("[write]", r); rec["after"] = r
        if r.get("value") != VAL:
            raise SystemExit("FATAL: the value read back is " + repr(r.get("value")))
        time.sleep(6)
        bad = checks("after")
        if bad:
            raise SystemExit("FATAL checks failed")
        ok = True
finally:
    if written and not ok:
        try:
            print("[rollback]", ops({"unset": 1, "clear": 1, "purge": 1}, "rollback"))
        except BaseException as e:  # noqa: BLE001
            print("[rollback] FAILED:", e)
    s1, _ = snip("PUT", f"/{BR}/deactivate", {}); s2, _ = snip("DELETE", f"/{BR}", None)
    print("[bridge] cleanup", s1, s2)
rec["ok"] = ok
if not DRY:
    os.makedirs(QA, exist_ok=True)
    io.open(os.path.join(QA, "kikar-ppsqm-result.json"), "w", encoding="utf-8").write(json.dumps(rec, ensure_ascii=False, indent=1))
print("RELEASE LIVE: Kikar Hamedina enters the neighbours' 'nearby projects to compare' table (65,000/m2)" if ok else ("DRY OK" if DRY else "NOT RELEASED"))
