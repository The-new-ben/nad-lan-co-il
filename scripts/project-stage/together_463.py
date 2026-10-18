# -*- coding: utf-8 -*-
"""Release 1.72.463 (HAD-543, Ben 18.10.2026 "use the LiveKit we already have"): the shared viewing room gets real video.
Tokens come from the Supabase edge function nadlan-room-token (the jus-tice LiveKit project; keys never leave it), called
server-side with an HMAC over room|identity|ts (options nadlan_tr_lk_proxy + nadlan_tr_lk_proxy_secret). The old path
(own LiveKit key in Settings) still wins when it is set. One hunk set on the LIVE text of inc/together.php."""
RELS = ["inc/together.php"]
A1 = "\t\treturn '' !== (string) nadlan_tr_opt( 'lk_url' ) && '' !== (string) nadlan_tr_opt( 'lk_key' ) && '' !== (string) nadlan_tr_opt( 'lk_secret' );\n"
B1 = ("\t\tif ( '' !== (string) nadlan_tr_opt( 'lk_url' ) && '' !== (string) nadlan_tr_opt( 'lk_key' ) && '' !== (string) nadlan_tr_opt( 'lk_secret' ) ) { return true; }\n"
      "\t\treturn '' !== (string) nadlan_tr_opt( 'lk_proxy' ) && 64 === strlen( (string) nadlan_tr_opt( 'lk_proxy_secret' ) ); // 1.72.463: the shared LiveKit project\n")
A2 = ("\t\t\t\t$out['url']   = (string) nadlan_tr_opt( 'lk_url' );\n"
      "\t\t\t\t$out['token'] = nadlan_tr_lk_token( $room, $pid, $name, $role, nadlan_tr_opt( 'lk_key' ), nadlan_tr_opt( 'lk_secret' ) );\n")
B2 = ("\t\t\t\tif ( '' !== (string) nadlan_tr_opt( 'lk_key' ) ) {\n"
      "\t\t\t\t\t$out['url']   = (string) nadlan_tr_opt( 'lk_url' );\n"
      "\t\t\t\t\t$out['token'] = nadlan_tr_lk_token( $room, $pid, $name, $role, nadlan_tr_opt( 'lk_key' ), nadlan_tr_opt( 'lk_secret' ) );\n"
      "\t\t\t\t} else { // 1.72.463: a token from the shared LiveKit project's edge function (HMAC-signed, rooms 'nadlan-*' only)\n"
      "\t\t\t\t\t$lk_room = 'nadlan-' . $room; $lk_ts = time();\n"
      "\t\t\t\t\t$lk_sig  = hash_hmac( 'sha256', $lk_room . '|' . $pid . '|' . $lk_ts, (string) nadlan_tr_opt( 'lk_proxy_secret' ) );\n"
      "\t\t\t\t\t$lk_res  = wp_remote_post( (string) nadlan_tr_opt( 'lk_proxy' ), array( 'timeout' => 8, 'headers' => array( 'content-type' => 'application/json' ),\n"
      "\t\t\t\t\t\t'body' => wp_json_encode( array( 'room' => $lk_room, 'identity' => $pid, 'name' => $name, 'role' => $role, 'ts' => $lk_ts, 'sig' => $lk_sig ) ) ) );\n"
      "\t\t\t\t\t$lk_body = is_wp_error( $lk_res ) ? null : json_decode( (string) wp_remote_retrieve_body( $lk_res ), true );\n"
      "\t\t\t\t\tif ( is_array( $lk_body ) && ! empty( $lk_body['token'] ) && ! empty( $lk_body['url'] ) ) { $out['url'] = (string) $lk_body['url']; $out['token'] = (string) $lk_body['token']; }\n"
      "\t\t\t\t\telse { $out['mode'] = 'fallback'; } // the room still works (state over REST) if the function does not answer\n"
      "\t\t\t\t}\n")


def apply(rel, txt):
    if rel != "inc/together.php":
        raise SystemExit("together_463: no hunk on " + rel)
    for a, b in ((A1, B1), (A2, B2)):
        n = txt.count(a)
        if n != 1:
            raise SystemExit(f"together_463: anchor x{n} in the live {rel}: {a.strip()[:80]!r}")
        txt = txt.replace(a, b)
    return txt
