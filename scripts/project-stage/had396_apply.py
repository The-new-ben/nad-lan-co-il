# -*- coding: utf-8 -*-
"""HAD-396 data patch, the APPLY step (Maya 3.10.2026, urban-data-report-review.md: the target and backup conditions hold; apply
with the reviewed fingerprint, through main's queue; "applied 21" alone is no proof). urban's had396_data_patch.php at 30262c76
(md5 74cd59db) plus main's own verify/restore route, each as a temporary snippet, both deleted after.
  1. a fresh REPORT: ok, before_md5 == 360bf6ec05edbf92eda40fc252775b70, and the fresh before image == the reviewed one;
  2. main's route reads the 21 raw fields (exists, value, value count) and they must equal the reviewed before image; saved as
     the local backup (every field restorable);
  3. APPLY with expect_before_md5;
  4. readback of all 21: a deletion must be gone (metadata_exists false), every other field must equal the reviewed after value
     (JSON fields: valid JSON and equal);
  5. any mismatch: restore all 21 from the backup, read back, report ROLLED BACK;
  6. on success: delete the demo payload caches (nlur_demo_payload_<lang>) and purge LiteSpeed for the 4 posts.
The app password is decrypted in-process (DPAPI) and never printed.   python scripts/project-stage/had396_apply.py"""
import glob, hashlib, json, os, secrets, subprocess, time
HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(HERE))
_src = open(os.path.join(REPO, "scripts", "skin-a", "deployskin.py"), encoding="utf-8").read()
_ns = {"__name__": "had396_apply_helpers"}
exec(compile(_src[:_src.index('s, h, _ = req("GET", "/wp-json/nadlan/v1/health")')], "deployskin-helpers", "exec"), _ns)
req, must, snip = _ns["req"], _ns["must"], _ns["snip"]
H = "360bf6ec05edbf92eda40fc252775b70"
COMMIT, WANT = "30262c76", "74cd59dba9345c95125a6f4f169ff6d6"
QA = os.path.join(REPO, "docs", "qa", "had-396")
REPORT = sorted(glob.glob(os.path.join(QA, "data-report-live-*.json")))[-1]
REV = json.load(open(REPORT, encoding="utf-8"))
if REV.get("before_md5") != H or len(REV["before"]) != 21 or set(REV["before"]) != set(REV["after"]):
    raise SystemExit("FATAL: the reviewed report is not the 21-field report with " + H[:10])
stamp = time.strftime("%Y%m%dT%H%M%SZ", time.gmtime())

code_b = subprocess.run(["git", "-C", REPO, "show", f"{COMMIT}:scripts/urban-renewal/had396_data_patch.php"], capture_output=True, check=True).stdout
if hashlib.md5(code_b).hexdigest() != WANT:
    raise SystemExit("FATAL: the patch script is not " + WANT[:10])
PATCH = code_b.decode("utf-8").split("\n", 1)[1]
TOKEN = secrets.token_hex(16)
VERIFY = r"""
add_action( 'rest_api_init', function () {
	register_rest_route( 'nadlan-had396v/v1', '/state', array(
		'methods' => 'POST',
		'permission_callback' => function () { return current_user_can( 'manage_options' ); },
		'callback' => function ( $req ) {
			$b = (array) $req->get_json_params();
			if ( ! hash_equals( '__T__', (string) ( $b['token'] ?? '' ) ) ) { return new WP_Error( 'forbidden', 'token', array( 'status' => 403 ) ); }
			$ids = array( 5477, 5478, 5479, 5480 );
			$keys = array( 'rating', 'reviews_count', 'years_active', 'project_count', 'response_time', 'bio', 'address', 'renewal_updates', 'renewal_stage', 'renewal_stage_log' );
			$parse = function ( $f ) use ( $ids, $keys ) {
				$p = explode( ':', (string) $f );
				if ( 'room' === $p[0] && 2 === count( $p ) ) { return array( 5480, $p[1] ); }
				if ( 'profile' === $p[0] && 3 === count( $p ) ) { return array( (int) $p[1], $p[2] ); }
				return null;
			};
			$out = array( 'state' => array() );
			if ( 'restore' === ( $b['mode'] ?? '' ) ) {
				foreach ( (array) $b['values'] as $f => $v ) {
					$t = $parse( $f );
					if ( ! $t || ! in_array( $t[0], $ids, true ) ) { continue; }
					if ( 'post_title' === $t[1] ) { wp_update_post( array( 'ID' => $t[0], 'post_title' => wp_slash( (string) $v['value'] ) ) ); continue; }
					if ( ! in_array( $t[1], $keys, true ) ) { continue; }
					if ( empty( $v['exists'] ) ) { delete_post_meta( $t[0], $t[1] ); } else { update_post_meta( $t[0], $t[1], wp_slash( (string) $v['value'] ) ); }
				}
			}
			if ( 'purge' === ( $b['mode'] ?? '' ) ) {
				foreach ( array( 'he', 'en', 'ru', 'fr', 'ar' ) as $l ) { delete_transient( 'nlur_demo_payload_' . $l ); }
				foreach ( $ids as $i ) { clean_post_cache( $i ); do_action( 'litespeed_purge_post', $i ); }
				$out['purged'] = 1;
			}
			foreach ( (array) ( $b['fields'] ?? array() ) as $f ) {
				$t = $parse( $f );
				if ( ! $t || ! in_array( $t[0], $ids, true ) ) { $out['state'][ $f ] = array( 'error' => 'not allowed' ); continue; }
				clean_post_cache( $t[0] ); wp_cache_delete( $t[0], 'post_meta' );
				if ( 'post_title' === $t[1] ) { $out['state'][ $f ] = array( 'exists' => true, 'value' => (string) get_post_field( 'post_title', $t[0], 'raw' ), 'n' => 1 ); continue; }
				$all = get_post_meta( $t[0], $t[1], false );
				$out['state'][ $f ] = array( 'exists' => metadata_exists( 'post', $t[0], $t[1] ), 'value' => (string) get_post_meta( $t[0], $t[1], true ), 'n' => count( (array) $all ) );
			}
			return $out;
		},
	) );
} );
""".replace("__T__", TOKEN)
FIELDS = sorted(REV["before"])


def state(mode="read", values=None):
    body = {"token": TOKEN, "mode": mode, "fields": FIELDS}
    if values is not None:
        body["values"] = values
    s, r, _ = req("POST", "/wp-json/nadlan-had396v/v1/state", body, timeout=120); must(s, r, "state " + mode)
    return r


def as_text(v):
    return "" if v is None else (str(v) if not isinstance(v, str) else v)


def same_as(f, st, want, deleted_ok):
    if want is None:
        return (not st.get("exists")) if deleted_ok else False
    if not st.get("exists") or st.get("n") not in (1, None):
        return False
    a, b = st.get("value", ""), as_text(want)
    if f.endswith("renewal_updates") or f.endswith("renewal_stage_log"):
        try:
            return json.loads(a) == json.loads(b)
        except ValueError:
            return False
    return a == b


snips = []
log = {"stamp": stamp, "report": os.path.relpath(REPORT, REPO), "fingerprint": H}
try:
    for name, code in (("tmp-had396-apply", PATCH), ("tmp-had396-verify", VERIFY)):
        s, c = snip("POST", "", {"name": f"{name}-{int(time.time())}", "code": "/* placeholder */", "scope": "global", "active": False}); must(s, c, name + " create")
        snips.append(c["id"])
        s, u = snip("PUT", f"/{c['id']}", {"name": c["name"], "code": code, "scope": "global", "active": False}); must(s, u, name + " update")
        s, a = snip("PUT", f"/{c['id']}/activate", {}); must(s, a, name + " activate")
    # 1. a fresh report
    s, fr, _ = req("POST", "/wp-json/nadlanfix/v1/had396-data", {}, timeout=120); must(s, fr, "fresh report")
    log["fresh_report"] = {"ok": fr.get("ok"), "before_md5": fr.get("before_md5"), "planned": fr.get("planned_writes"), "mode": fr.get("mode")}
    if not fr.get("ok") or fr.get("before_md5") != H or fr.get("before") != REV["before"] or fr.get("after") != REV["after"]:
        raise SystemExit("STOP before any write: the fresh report differs from the reviewed one " + json.dumps(log["fresh_report"]))
    # 2. the raw before state = the backup
    before = state()["state"]
    bad = [f for f in FIELDS if not same_as(f, before[f], REV["before"][f], False)]
    if bad:
        raise SystemExit("STOP before any write: the raw state differs from the reviewed before image: " + ", ".join(bad))
    backup = os.path.join(QA, f"data-apply-backup-{stamp}.json")
    open(backup, "w", encoding="utf-8").write(json.dumps({"fields": before, "reviewed_before": REV["before"]}, ensure_ascii=False, indent=1))
    log["backup"] = os.path.relpath(backup, REPO)
    print("[backup]", log["backup"], "| 21 fields equal the reviewed before image")
    # 3. apply
    s, ap, _ = req("POST", "/wp-json/nadlanfix/v1/had396-data", {"apply": True, "expect_before_md5": H}, timeout=120); must(s, ap, "apply")
    log["apply"] = {"ok": ap.get("ok"), "mode": ap.get("mode"), "errors": ap.get("errors")}
    print("[apply]", json.dumps(log["apply"], ensure_ascii=False))
    # 4. readback of all 21
    after = state()["state"]
    mism = [f for f in FIELDS if not same_as(f, after[f], REV["after"][f], True)]
    log["readback"] = {"checked": len(FIELDS), "mismatch": mism, "deleted": sum(1 for f in FIELDS if REV["after"][f] is None and not after[f].get("exists"))}
    print("[readback]", json.dumps(log["readback"], ensure_ascii=False))
    if mism or not ap.get("ok"):
        # 5. restore everything from the backup
        state("restore", before)
        back = state()["state"]
        still = [f for f in FIELDS if not same_as(f, back[f], REV["before"][f], False)]
        log["rolled_back"] = {"restored": len(FIELDS), "not_equal_after_restore": still}
        print("[ROLLED BACK]", json.dumps(log["rolled_back"], ensure_ascii=False))
    else:
        # 6. caches
        state("purge")
        s, r2, _ = req("POST", "/wp-json/nadlanfix/v1/had396-data", {}, timeout=120)
        log["report_after"] = {"ok": r2.get("ok") if isinstance(r2, dict) else None, "planned": r2.get("planned_writes") if isinstance(r2, dict) else None}
        print("[report after]", json.dumps(log["report_after"]), "(want planned 0)")
finally:
    for sid in snips:
        s1, _ = snip("PUT", f"/{sid}/deactivate", {}); s2, _ = snip("DELETE", f"/{sid}", None); print("[snippet] cleanup", sid, s1, s2)
    out = os.path.join(QA, f"data-apply-{stamp}.json")
    open(out, "w", encoding="utf-8").write(json.dumps(log, ensure_ascii=False, indent=1))
    print("[log]", os.path.relpath(out, REPO))
