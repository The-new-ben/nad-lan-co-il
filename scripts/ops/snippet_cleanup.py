# -*- coding: utf-8 -*-
"""Ben 15.10.2026: clean the ~480 INACTIVE Code Snippets left behind by agents (temporary deploy bridges, tests, old ops).
Never touches an active snippet. Before any delete, the full JSON of every inactive snippet is saved locally (so nothing is
lost: any one can be re-created from the backup). Default is a dry run that only counts.
   python scripts/ops/snippet_cleanup.py            dry run: counts by kind, the backup path it would write
   python scripts/ops/snippet_cleanup.py --delete   backup, then delete the inactive snippets, then verify the active count
The WordPress app password is decrypted inside the process (DPAPI) and never printed."""
import collections
import io
import json
import os
import re
import sys
import time

REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
src = open(os.path.join(REPO, "scripts", "skin-a", "deployskin.py"), encoding="utf-8").read()
ns = {"__name__": "snipclean"}
exec(compile(src[:src.index('s, h, _ = req("GET", "/wp-json/nadlan/v1/health")')], "deployskin-helpers", "exec"), ns)
req = ns["req"]
BK = os.path.join(REPO, "docs", "qa", "snippets-backup")  # git-ignored: old bridge code stays on this computer only

allsn = []
for pg in range(1, 20):
    s, sn, _ = req("GET", f"/wp-json/code-snippets/v1/snippets?per_page=100&page={pg}")
    if not isinstance(sn, list) or not sn:
        break
    allsn += sn
active = [x for x in allsn if x.get("active")]
inactive = [x for x in allsn if not x.get("active")]
kinds = collections.Counter(re.sub(r"[-_]?\d{6,}$", "", (x.get("name") or "")).strip() or "(no name)" for x in inactive)
print(f"snippets {len(allsn)} | active {len(active)} (kept) | inactive {len(inactive)} (to delete)")
for k, n in kinds.most_common(12):
    print(f"   {n:4d}  {k}")
print("active, kept:", ", ".join(sorted((x.get("name") or "")[:28] for x in active)))
if "--delete" not in sys.argv and "--bridge" not in sys.argv:
    print("dry run: nothing deleted. Run with --delete to back up and delete.")
    raise SystemExit(0)
if "--bridge" not in sys.argv:
    os.makedirs(BK, exist_ok=True)
    with open(os.path.join(BK, ".gitignore"), "w", encoding="utf-8") as fh:
        fh.write("*\n")
    path = os.path.join(BK, f"inactive-snippets-{time.strftime('%Y%m%dT%H%M%S')}.json")
    json.dump(inactive, io.open(path, "w", encoding="utf-8"), ensure_ascii=False)
    print("backup:", path, f"({len(inactive)} snippets, {os.path.getsize(path):,} bytes)")
    ok = bad = 0
    for x in inactive:
        s, _, _ = req("DELETE", f"/wp-json/code-snippets/v1/snippets/{x['id']}")
        if s in (200, 204):
            ok += 1
        else:
            bad += 1
    print(f"deleted {ok}, failed {bad}")
    s, h, _ = req("GET", "/wp-json/nadlan/v1/health")
    left = []
    for pg in range(1, 20):
        s2, sn, _ = req("GET", f"/wp-json/code-snippets/v1/snippets?per_page=100&page={pg}")
        if not isinstance(sn, list) or not sn:
            break
        left += sn
    print(f"after: {len(left)} snippets, active {sum(1 for x in left if x.get('active'))} (was {len(active)}) | site health {s}")


def bridge_delete(ids):
    """Fallback (15.10.2026): the Code Snippets REST delete returns 500 for most old inactive snippets. A temporary,
    token-gated route deletes them in the snippets table, ONLY rows that are inactive AND in the backup list, then the route
    itself is deactivated and deleted (verified 404)."""
    import secrets
    tok = secrets.token_hex(24)
    php = ("add_action( 'rest_api_init', function () { register_rest_route( 'nadlan-snipclean/v1', '/run', array( 'methods' => 'POST', "
           "'permission_callback' => function () { return current_user_can( 'manage_options' ); }, 'callback' => function ( $r ) { global $wpdb; "
           "$b = $r->get_json_params(); if ( ! is_array( $b ) || ! hash_equals( '" + tok + "', (string) ( $b['token'] ?? '' ) ) ) { return new WP_Error( 'forbidden', 'token', array( 'status' => 403 ) ); } "
           "$ids = array_values( array_filter( array_map( 'intval', (array) ( $b['ids'] ?? array() ) ) ) ); if ( ! $ids ) { return array( 'deleted' => 0 ); } "
           "$t = $wpdb->prefix . 'snippets'; $in = implode( ',', $ids ); $n = $wpdb->query( \"DELETE FROM {$t} WHERE active = 0 AND id IN ({$in})\" ); "
           "return array( 'deleted' => (int) $n, 'left_active' => (int) $wpdb->get_var( \"SELECT COUNT(*) FROM {$t} WHERE active = 1\" ) ); } ) ); } );")
    s, c, _ = req("POST", "/wp-json/code-snippets/v1/snippets", {"name": f"tmp-snipclean-{int(time.time())}", "code": "/* placeholder */", "scope": "global", "active": False})
    br = c["id"]
    try:
        req("PUT", f"/wp-json/code-snippets/v1/snippets/{br}", {"name": c["name"], "code": php, "scope": "global", "active": False})
        req("PUT", f"/wp-json/code-snippets/v1/snippets/{br}/activate", {})
        total = 0
        for i in range(0, len(ids), 200):
            s, r, _ = req("POST", "/wp-json/nadlan-snipclean/v1/run", {"token": tok, "ids": ids[i:i + 200]})
            total += int((r or {}).get("deleted", 0)); print("  batch", i // 200 + 1, s, r)
        return total
    finally:
        print("  bridge cleanup", req("PUT", f"/wp-json/code-snippets/v1/snippets/{br}/deactivate", {})[0], req("DELETE", f"/wp-json/code-snippets/v1/snippets/{br}")[0],
              "| route after:", req("POST", "/wp-json/nadlan-snipclean/v1/run", {"token": "x"})[0], "(want 404)")


if "--bridge" in sys.argv:
    bks = sorted(f for f in os.listdir(BK) if f.startswith("inactive-snippets-"))
    left = [x for x in allsn if not x.get("active")]
    backed = {x["id"] for f in bks for x in json.load(io.open(os.path.join(BK, f), encoding="utf-8"))}
    ids = [x["id"] for x in left if x["id"] in backed]
    print(f"bridge delete: {len(ids)} inactive snippets, all present in the backup")
    print("deleted:", bridge_delete(ids))
