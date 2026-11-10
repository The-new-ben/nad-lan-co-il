# -*- coding: utf-8 -*-
"""HAD-700 (Ben 10.11.2026: "if scripts like Tawk weigh on the page, remove them"): switch OFF Code Snippet 1477
"tawk.to visitor tracking (hidden widget)". The chat was hidden on load sitewide (Tawk_API.hideWidget), nothing on the site opens
it, and it cost 13 requests per page view (measured on /projects/ 10.11.2026). Deactivate only, never delete: the code stays in
the snippet and in a local backup; --rollback switches it back on.
python scripts/project-stage/tawk_off_1477.py [--dry | --rollback]"""
import hashlib, io, json, os, sys, time, urllib.request
HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.dirname(os.path.dirname(HERE))
BK = os.path.join(REPO, "docs", "qa", "had-700", "snippet-1477")
SID = 1477
src = open(os.path.join(REPO, "scripts", "skin-a", "deployskin.py"), encoding="utf-8").read()
ns = {"__name__": "tawk1477"}
exec(compile(src[:src.index('s, h, _ = req("GET", "/wp-json/nadlan/v1/health")')], "deployskin-helpers", "exec"), ns)
snip = ns["snip"]
PAGES = ["/", "/projects/", "/projects/rainbow-tel-aviv/", "/mortgage-calculator/"]


def page(p):
    u = "https://nad-lan.co.il" + p + ("&" if "?" in p else "?") + "nltawk=" + str(int(time.time()))
    try:
        with urllib.request.urlopen(urllib.request.Request(u, headers={"User-Agent": "Mozilla/5.0 (site owner audit)"}), timeout=90) as f:
            return f.status, f.read().decode("utf-8", "replace")
    except Exception as e:
        return 0, str(e)


s, sn = snip("GET", "/%d" % SID, None)
if s != 200:
    raise SystemExit("FATAL read snippet %d: %s" % (SID, s))
print("[read] id", SID, "|", sn.get("name"), "| scope", sn.get("scope"), "| active", sn.get("active"), "| md5", hashlib.md5(sn["code"].encode()).hexdigest()[:10])
if "tawk" not in sn["code"].lower():
    raise SystemExit("FATAL: snippet 1477 is not the Tawk embed")
want = "--rollback" in sys.argv
if bool(sn.get("active")) == want:
    print("already", "on" if want else "off"); raise SystemExit(0)
before = {p: page(p) for p in PAGES}
for p, (st, h) in before.items():
    print("[before]", st, p, "tawk" if "embed.tawk.to" in h else "-")
if "--dry" in sys.argv:
    raise SystemExit(0)
os.makedirs(BK, exist_ok=True)
bkp = os.path.join(BK, "snippet-1477-%s.json" % time.strftime("%Y%m%dT%H%M%S"))
io.open(bkp, "w", encoding="utf-8").write(json.dumps({"id": SID, "name": sn["name"], "scope": sn["scope"], "active": sn.get("active"), "code": sn["code"]}, ensure_ascii=False))
s, r = snip("PUT", "/%d" % SID, {"name": sn["name"], "code": sn["code"], "scope": sn["scope"], "active": want})
s2, back = snip("GET", "/%d" % SID, None)
ok = s == 200 and bool(back.get("active")) == want and back.get("code") == sn["code"]
print("[write]", s, "| read-back active:", back.get("active"), "| code unchanged:", back.get("code") == sn["code"], "| backup", os.path.relpath(bkp, REPO))
time.sleep(4)
bad = [] if ok else ["write"]
for p in PAGES:
    st, h = page(p)
    has = "embed.tawk.to" in h
    good = st == 200 and "Fatal error" not in h and "critical error" not in h and (has == want)
    print("[after]", "OK " if good else "BAD", st, p, "tawk" if has else "-")
    if not good:
        bad.append(p)
if bad:
    s, r = snip("PUT", "/%d" % SID, {"name": sn["name"], "code": sn["code"], "scope": sn["scope"], "active": bool(sn.get("active"))})
    raise SystemExit("ROLLED BACK (%s): %s" % (s, bad))
print("DONE: snippet 1477 is", "on" if want else "off")
