# -*- coding: utf-8 -*-
"""Check-only pass for release 1.72.403 (Kikar V7, the five articles). READ-ONLY: public GETs, no bridge, no write.

Why it exists: the first run of deploy403.py (3.10.2026 01:25, deploy403-run.log) wrote the five posts and the version, then failed
verify_pages only on checks inherited from 1.72.369-391 that required the OLD articles' sentences (and a passing 502 on / and
/brokers/ in round two). Its rollback could not reach its bridge (a concurrent dry run's opening sweep had removed it), so the new
posts stayed live. make_gen403.py now drops those stale sentences; this script runs the regenerated deploy403.py's whole check
chain (verify_pages, served_exact, verify_order, verify_home_order, verify_kh) against live 1.72.403 and records the result.

    python scripts/project-stage/verify403.py
"""
import io, json, os, sys, time

HERE = os.path.dirname(os.path.abspath(__file__))
src = io.open(os.path.join(HERE, "deploy403.py"), encoding="utf-8").read()
cut = src.index("TOKEN = secrets.token_hex(24)")  # stop before the bridge: no write of any kind
mark = src.index("# ---------------------------------------------------------------- main")
# the module's definitions after the bridge text (the checks and their helpers) are needed; the bridge/up/main code is not run
pre, mid = src[:cut], src[cut:mark]
ns = {"__name__": "verify403", "__file__": os.path.join(HERE, "deploy403.py")}
exec(compile(pre, "deploy403(pre)", "exec"), ns)
if ns["LIVE_VER"] != "1.72.403":
    raise SystemExit("live is %s, not 1.72.403" % ns["LIVE_VER"])
exec(compile(mid, "deploy403(defs)", "exec"), ns)
# the check functions defined after the main marker (served_exact, ...): their definitions only, never the main statements
import ast  # noqa: E402
_tail = ast.parse(src[mark:])
_defs = ast.Module(body=[n for n in _tail.body if isinstance(n, ast.FunctionDef)], type_ignores=[])
exec(compile(_defs, "deploy403(tail defs)", "exec"), ns)
for _need in ("verify_pages", "served_exact", "verify_order", "verify_home_order", "verify_kh"):
    if _need not in ns:
        raise SystemExit("missing check function: " + _need)
ns.setdefault("FILES", [])
tag = "v403chk%d" % int(time.time())
res = {}
res["verify_pages"] = ns["verify_pages"](tag + "p")
res["served_exact"] = ns["served_exact"](tag + "s")
res["verify_order"] = ns["verify_order"](tag + "o")
res["verify_home_order"] = ns["verify_home_order"](tag + "h")
res["verify_kh"] = ns["verify_kh"](tag + "k")
ok = (not res["verify_pages"]) and all(res[k] for k in ("served_exact", "verify_order", "verify_home_order", "verify_kh"))
print("[verify403]", "ALL GREEN" if ok else "NOT GREEN", json.dumps(res, ensure_ascii=False))
rp = os.path.join(ns["QA"], "deploy-result-403.json")
rec = json.load(io.open(rp, encoding="utf-8")) if os.path.exists(rp) else {}
rec.setdefault("history", []).append({"t": time.strftime("%Y-%m-%dT%H:%M:%S"), "state": rec.get("state")})
rec["state"] = "released and verified (re-check)" if ok else "released, re-check NOT green"
rec["recheck"] = {"when": time.strftime("%Y-%m-%dT%H:%M:%S"), "results": res,
                  "why": "the first run failed only on inherited checks that required the old articles' sentences (removed by "
                         "make_gen403.py) and a passing 502; its rollback could not reach its bridge (removed by a concurrent dry "
                         "run's sweep), so the new posts stayed live; this pass runs the whole regenerated check chain, read-only"}
json.dump(rec, io.open(rp, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
sys.exit(0 if ok else 1)
