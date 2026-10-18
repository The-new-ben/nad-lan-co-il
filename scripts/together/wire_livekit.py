# -*- coding: utf-8 -*-
"""HAD-543 (Ben 18.10.2026: "we already have LiveKit, use the infrastructure"): wire nad-lan's shared viewing room to the
LiveKit project that already runs the jus-tice courtroom (Supabase project mlnwpocuvjnelttvscja), without any key leaving it.
1. a fresh random shared secret (never printed) -> Supabase secret NADLAN_ROOM_SECRET
2. deploy the edge function nadlan-room-token (courtai/supabase/functions/nadlan-room-token, rooms "nadlan-*" only)
3. a temporary token-gated bridge writes WordPress options nadlan_tr_lk_proxy (function URL) and nadlan_tr_lk_proxy_secret,
   then the bridge snippet is deleted (verified 404). The secret travels only in request bodies, never in snippet code.
python wire_livekit.py"""
import os, secrets, subprocess, sys, time, json
HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(HERE))
COURT = r"C:\Users\777\Documents\ChatGPT-Work\courtai"
REF = "mlnwpocuvjnelttvscja"
FN_URL = f"https://{REF}.supabase.co/functions/v1/nadlan-room-token"
src = open(os.path.join(REPO, "scripts", "skin-a", "deployskin.py"), encoding="utf-8").read()
ns = {"__name__": "wire"}
exec(compile(src[:src.index('s, h, _ = req("GET", "/wp-json/nadlan/v1/health")')], "h", "exec"), ns)
req, snip = ns["req"], ns["snip"]
NPX = "npx.cmd" if os.name == "nt" else "npx"

shared = secrets.token_hex(32)
env = dict(os.environ, NADLAN_ROOM_SECRET=shared)
r = subprocess.run(f'{NPX} supabase secrets set NADLAN_ROOM_SECRET="%NADLAN_ROOM_SECRET%" --project-ref {REF}', cwd=COURT, env=env, shell=True, capture_output=True, text=True)
print("[supabase] secret set:", r.returncode, (r.stdout + r.stderr).replace(shared, "***")[-200:].strip())
if r.returncode != 0:
    sys.exit("FATAL: secret not set")
r = subprocess.run(f"{NPX} supabase functions deploy nadlan-room-token --no-verify-jwt --project-ref {REF}", cwd=COURT, shell=True, capture_output=True, text=True)
print("[supabase] deploy:", r.returncode, (r.stdout + r.stderr)[-300:].strip())
if r.returncode != 0:
    sys.exit("FATAL: deploy failed")

TOKEN = secrets.token_hex(24)
BRIDGE = r"""
add_action( 'rest_api_init', function () {
	register_rest_route( 'nadlan-lk-wire/v1', '/apply', array( 'methods' => 'POST',
		'permission_callback' => function () { return current_user_can( 'manage_options' ); },
		'callback' => function ( $req ) {
			$b = $req->get_json_params();
			if ( ! is_array( $b ) || ! hash_equals( '__TOKEN__', (string) ( $b['token'] ?? '' ) ) ) { return new WP_Error( 'forbidden', 'token', array( 'status' => 403 ) ); }
			update_option( 'nadlan_tr_lk_proxy', esc_url_raw( (string) $b['url'] ), false );
			update_option( 'nadlan_tr_lk_proxy_secret', preg_replace( '/[^a-f0-9]/', '', (string) $b['secret'] ), false );
			return array( 'ok' => true, 'url' => get_option( 'nadlan_tr_lk_proxy' ), 'secret_len' => strlen( (string) get_option( 'nadlan_tr_lk_proxy_secret' ) ) );
		} ) );
} );
""".replace("__TOKEN__", TOKEN)
s, c = snip("POST", "", {"name": f"tmp-lk-wire-{int(time.time())}", "code": "/* placeholder */", "scope": "global", "active": False})
br = c["id"]
try:
    snip("PUT", f"/{br}", {"name": c["name"], "code": BRIDGE, "scope": "global", "active": False})
    snip("PUT", f"/{br}/activate", {})
    time.sleep(1.5)
    s2, out, _ = req("POST", "/wp-json/nadlan-lk-wire/v1/apply", {"token": TOKEN, "url": FN_URL, "secret": shared})
    print("[wp] options:", s2, out)
finally:
    snip("POST", f"/{br}/deactivate", {})
    s3, _ = snip("DELETE", f"/{br}", None)
    time.sleep(1)
    s4, _, _ = req("POST", "/wp-json/nadlan-lk-wire/v1/apply", {"token": TOKEN})
    print("[wp] bridge deleted:", s3, "route now:", s4, "(want 404)")
