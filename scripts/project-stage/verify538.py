# -*- coding: utf-8 -*-
"""Finish release 1.72.538 read-only (the verify403 pattern). The first run wrote every file (health 1.72.538) and was cut in
its second check round by a local DNS outage plus the caller's own time limit, so neither a rollback nor the record's last
step ran. This script, with the regenerated deploy538.py (two wrong checks corrected): sweeps the dead run's bridge, proves
the live files are byte for byte what the run wrote, runs every check again, and only then marks the record "released and
verified". A failed check is printed and nothing is rolled back here: the decision is made by hand (--rollback exists)."""
import base64, hashlib, json, os, sys
H = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, H); os.chdir(os.path.dirname(os.path.dirname(H)))
src = open(os.path.join(H, "deploy538.py"), encoding="utf-8").read()
cut = src.index("\ncreated = False\ntry:")
sys.argv = ["deploy538.py", "--finish"]
ns = {"__name__": "verify538", "__file__": os.path.join(H, "deploy538.py")}
exec(compile(src[:cut], "deploy538", "exec"), ns)
RES = os.path.join(ns["QA"], "deploy-result-538.json")
rec = json.load(open(RES, encoding="utf-8"))
print("[record]", rec.get("state"), "| files:", len(rec.get("files") or {}))
ok = False
try:
    ns["sweep"]("start")
    ns["bridge_up"]()
    bad_md5 = []
    for rel, want in (rec.get("files") or {}).items():
        g = ns["live_get"](rel)
        got = "missing" if g.get("missing") else hashlib.md5(base64.b64decode(g["b64"])).hexdigest()
        print(f"[live] {rel}: {got[:10]} {'OK' if got == want else 'DIFFERS (want ' + want[:10] + ')'}")
        if got != want:
            bad_md5.append(rel)
    if bad_md5:
        raise SystemExit("STOP: the live files are not the run's: " + ", ".join(bad_md5))
    print("[purge]", ns["ops"]({"purge": 1}, "purge"))
    if not ns["wait_version"]("1.72.538"):
        raise SystemExit("STOP: health is not 1.72.538")
    bad = ns["run_checks"]("f")
    if bad:
        print("[checks] first round:", bad, "- purge and look again")
        ns["ops"]({"purge": 1}, "purge again")
        bad = ns["run_checks"]("g")
    if bad:
        print("[FAIL] checks:", bad)
    else:
        ok = True
finally:
    try:
        ns["bridge_down"]()
    except BaseException as e:
        print("[bridge] down failed:", e)
    try:
        ns["sweep"]("end")
    except BaseException as e:
        print("[sweep end] failed:", e)
if ok:
    rec["state"] = "released and verified"
    rec["verified_by"] = "verify538.py (read-only second pass, 31.10.2026): live files byte for byte + every check OK"
    json.dump(rec, open(RES, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print("RELEASE 1.72.538 VERIFIED")
