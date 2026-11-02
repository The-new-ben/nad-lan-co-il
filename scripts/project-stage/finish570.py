# Finish release 1.72.570: the runner was cut off from outside during its checks (files written, live 1.72.570, record
# "written, checks pending"). Run the same run_checks() once and close the record; if a check fails, say so and stop (no write).
import json, os, sys
H = r"C:\Users\777\nad-lan\nad-lan-co-il\scripts\project-stage"
sys.path.insert(0, H); os.chdir(r"C:\Users\777\nad-lan\nad-lan-co-il")
src = open(os.path.join(H, "deploy570.py"), encoding="utf-8").read()
sys.argv = [os.path.join(H, "deploy570.py"), "--finish"]
g = {"__name__": "finish570", "__file__": os.path.join(H, "deploy570.py")}
exec(compile(src[:src.index("created = False")], "deploy570.py", "exec"), g)
assert g["LIVE_VER"] == "1.72.570", g["LIVE_VER"]
REC = g["REC"]; REC.update(json.load(open(g["RESULT"], encoding="utf-8")))
assert str(REC.get("state", "")).startswith("written"), REC.get("state")
try:
    g["sweep"]("start"); g["bridge_up"]()
    bad = g["run_checks"]("f")
    if bad:
        print("CHECKS FAILED:", bad, "- record left as it is; decide: fix forward or --rollback")
    else:
        g["record"]("released and verified", checks="run_checks after the runner was cut off mid-checks (finish570.py): verify_pages + served_exact + verify_order + verify_home_order + verify_kh: OK")
        print("RELEASE 1.72.570 LIVE: the neighbours spotlight follows the facts table on four Sde Dov pages")
finally:
    try: g["bridge_down"]()
    except BaseException as e: print("[bridge] down failed:", e)
    try: g["sweep"]("end")
    except BaseException as e: print("[sweep end] failed:", e)
