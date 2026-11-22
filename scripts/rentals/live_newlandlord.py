# -*- coding: utf-8 -*-
"""HAD-795 (22.11.2026): the brand-new landlord on the LIVE site, through Ben's own test account (he opened it himself on 22.11; no
password is typed or read anywhere). An admin-only temporary bridge (token, deleted at the end) does four things for that ONE account:
  state   the rentals options and the account's rows
  pilot   add/remove the account to/from nadlan_rentals_v2_pilot, set nadlan_rentals_today2_pilot
  flip    set nadlan_rentals_v2 (the sign-up switch)
  session a 30-minute login session for the account, handed to a headless browser in this process only (never printed or saved);
          every session of the account is destroyed at the end.
The account must be a subscriber registered in the last 72 hours, or the bridge refuses.
Usage: python scripts/rentals/live_newlandlord.py <uid> <step> [out dir]
  steps: state | pilot-on | press | flip-new | pilot-off | press-new | flip-back"""
import json, os, secrets, sys, time
HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.dirname(os.path.dirname(HERE))
src = open(os.path.join(REPO, "scripts", "skin-a", "deployskin.py"), encoding="utf-8").read()
ns = {"__name__": "nl795"}
exec(compile(src[:src.index('s, h, _ = req("GET", "/wp-json/nadlan/v1/health")')], "deployskin-helpers", "exec"), ns)
req, snip = ns["req"], ns["snip"]
UID = int(sys.argv[1]); STEP = sys.argv[2]; OUT = sys.argv[3] if len(sys.argv) > 3 else os.path.join(REPO, "docs", "rentals", "build", "newlandlord")
os.makedirs(OUT, exist_ok=True)
BRIDGE = r'''
add_action( 'rest_api_init', function () {
	register_rest_route( 'nadlan-nl795/v1', '/run', array(
		'methods' => 'POST',
		'permission_callback' => function () { return current_user_can( 'manage_options' ); },
		'callback' => function ( $req ) {
			$b = $req->get_json_params();
			if ( ! is_array( $b ) || ! hash_equals( '__TOKEN__', (string) ( $b['token'] ?? '' ) ) ) { return new WP_Error( 'forbidden', 'token', array( 'status' => 403 ) ); }
			$uid = (int) __UID__; $u = get_userdata( $uid );
			if ( ! $u || array_values( $u->roles ) !== array( 'subscriber' ) || strtotime( $u->user_registered . ' UTC' ) < time() - 72 * 3600 ) { return new WP_Error( 'refused', 'not a fresh subscriber', array( 'status' => 409 ) ); }
			$do = (string) ( $b['do'] ?? 'state' ); $out = array( 'do' => $do );
			$pilot = array_values( array_map( 'intval', (array) get_option( 'nadlan_rentals_v2_pilot', array() ) ) );
			if ( 'pilot-on' === $do ) { if ( ! in_array( $uid, $pilot, true ) ) { $pilot[] = $uid; } update_option( 'nadlan_rentals_v2_pilot', $pilot, false ); update_option( 'nadlan_rentals_today2_pilot', '1', false ); }
			if ( 'pilot-off' === $do ) { update_option( 'nadlan_rentals_v2_pilot', array_values( array_diff( $pilot, array( $uid ) ) ), false ); }
			if ( 'flip-new' === $do ) { update_option( 'nadlan_rentals_v2', 'new', false ); }
			if ( 'flip-back' === $do ) { update_option( 'nadlan_rentals_v2', 'admin', false ); }
			if ( 'session' === $do ) {
				$exp = time() + 1800; $tok = WP_Session_Tokens::get_instance( $uid )->create( $exp );
				$out['c'] = array( LOGGED_IN_COOKIE => wp_generate_auth_cookie( $uid, $exp, 'logged_in', $tok ), SECURE_AUTH_COOKIE => wp_generate_auth_cookie( $uid, $exp, 'secure_auth', $tok ) );
			}
			if ( 'end' === $do ) { WP_Session_Tokens::get_instance( $uid )->destroy_all(); }
			global $wpdb; $rows = array();
			foreach ( array( 'properties', 'units', 'leases', 'contacts', 'ledger', 'tickets', 'docs', 'events' ) as $t ) { $tn = $wpdb->prefix . 'nlrm_' . $t; if ( $wpdb->get_var( $wpdb->prepare( 'SHOW TABLES LIKE %s', $tn ) ) === $tn ) { $rows[ $t ] = (int) $wpdb->get_var( $wpdb->prepare( "SELECT COUNT(*) FROM $tn WHERE owner_id = %d", $uid ) ); } }
			$out['state'] = array( 'v2' => get_option( 'nadlan_rentals_v2', '(unset)' ), 'pilot' => get_option( 'nadlan_rentals_v2_pilot', '(unset)' ), 'today2_pilot' => get_option( 'nadlan_rentals_today2_pilot', '(unset)' ), 'rows' => $rows,
				'sessions' => count( WP_Session_Tokens::get_instance( $uid )->get_all() ) );
			return $out;
		},
	) );
} );
'''
def run(fn):
    tok = secrets.token_hex(24); nm = "tmp-nl795-%d" % int(time.time())
    s, sn = snip("POST", "", {"name": nm, "code": "/* placeholder */", "scope": "global", "active": False}); bid = sn["id"]
    try:
        s1, _ = snip("PUT", "/%d" % bid, {"name": nm, "code": BRIDGE.replace("__TOKEN__", tok).replace("__UID__", str(UID)), "scope": "global", "active": False})
        s2, _ = snip("PUT", "/%d/activate" % bid, {})
        assert s1 == 200 and s2 == 200, (s1, s2)
        time.sleep(2)
        call = lambda do: req("POST", "/wp-json/nadlan-nl795/v1/run", {"token": tok, "do": do}, timeout=120)[:2]
        return fn(call)
    finally:
        a, _ = snip("PUT", "/%d/deactivate" % bid, {}); b, _ = snip("DELETE", "/%d" % bid, None)
        c, _, _ = req("POST", "/wp-json/nadlan-nl795/v1/run", {"token": "x"})
        print("[bridge] deactivate", a, "| delete", b, "| route now", c, "(want 404)")

RES = []
def check(name, ok, info=""):
    RES.append({"check": name, "ok": bool(ok), "info": str(info)[:400]}); print(("PASS " if ok else "FAIL ") + name + ("" if ok else " | " + str(info)[:300]))

PAGE = """() => { const r = document.getElementById('nlrm-root'), nt2 = document.getElementById('nt2'), t = s => (document.querySelector(s) || {}).innerText || '';
  return { loggedIn: document.body.classList.contains('logged-in'), root: !!r, mode: r ? r.dataset.mode : null, v1: !!document.querySelector('.nlrm-landing, #nlrm-new, .nlrm-hero'), stage: !!document.getElementById('nlpf'), tour: !!document.getElementById('nlrm-tour'),
    title: document.title, h1: t('h1').slice(0, 80), brand: t('.nlrm-brand b'), nt2: !!(nt2 && !nt2.hidden), text: (r ? r.innerText : document.body.innerText).replace(/\\s+/g, ' ').slice(0, 600),
    maker: document.querySelectorAll('[data-act="lease-doc"], [data-act="sign-link"]').length, plans: /פרימיום|Premium|₪\\s*\\d+\\s*לחודש|מנוי|תוכנית תשלום/i.test(document.body.innerText),
    signup: (() => { try { return localStorage.getItem('nlrm-signup'); } catch (e) { return 'x'; } })(), ov: document.scrollingElement.scrollWidth - innerWidth }; }"""

def press(call, tag):
    from playwright.sync_api import sync_playwright
    s, r = call("session"); assert s == 200 and "c" in r, (s, r)
    cookies = [{"name": k, "value": v, "domain": "nad-lan.co.il", "path": "/", "secure": True, "httpOnly": True, "sameSite": "Lax"} for k, v in r["c"].items()]
    out = {}
    try:
        with sync_playwright() as p:
            b = p.chromium.launch(channel="msedge", headless=True)
            for w, h, dev in ((1440, 900, "desk"), (390, 844, "phone")):
                ctx = b.new_context(viewport={"width": w, "height": h}, device_scale_factor=2 if w < 900 else 1, has_touch=w < 900, locale="he-IL")
                ctx.add_cookies(cookies)
                pg = ctx.new_page(); errs = []; ev = []
                pg.on("pageerror", lambda e: errs.append(str(e)[:160]))
                pg.on("request", lambda q: ev.append(q.url) if ("collect" in q.url or "nltrack" in q.url.lower() or "/track" in q.url) else None)
                pg.goto("https://nad-lan.co.il/my-rentals/?nl=%s" % tag, wait_until="domcontentloaded")
                pg.wait_for_timeout(7000)
                m = pg.evaluate(PAGE); m["errs"] = errs[:3]; m["track"] = len(ev)
                out[dev] = m
                pg.screenshot(path=os.path.join(OUT, "%s-%s-1-first.png" % (tag, dev)))
                ctx.close()
            b.close()
    finally:
        s, r = call("end"); print("[session] all sessions of the account ended:", s, r.get("state", {}).get("sessions"))
    return out

def main(call):
    s, r = call("state" if STEP in ("press", "press-new") else STEP)
    print("state before/after", STEP, s, json.dumps(r.get("state"), ensure_ascii=False))
    if STEP in ("press", "press-new"):
        o = press(call, STEP)
        for dev, m in o.items():
            print(dev, json.dumps({k: m[k] for k in ("loggedIn", "root", "mode", "v1", "stage", "tour", "title", "h1", "brand", "nt2", "maker", "plans", "signup", "ov", "errs", "track")}, ensure_ascii=False))
            print("   text:", m["text"][:420])
            check("%s %s: the new landlord lands in version 2 (the app, not the public page), with the product name" % (STEP, dev), m["loggedIn"] and m["root"] and m["mode"] != "demo" and not m["stage"] and not m["tour"] and ("השכרות" in m["title"] or "השכרות" in m["brand"]), m)
            check("%s %s: no lease text maker, no plans or prices, no script error, no sideways scroll" % (STEP, dev), m["maker"] == 0 and not m["plans"] and not m["errs"] and m["ov"] <= 0, m)
        json.dump({"step": STEP, "out": o, "checks": RES}, open(os.path.join(OUT, "%s-results.json" % STEP), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
run(main)
print("RESULT %d/%d" % (sum(x["ok"] for x in RES), len(RES)))
