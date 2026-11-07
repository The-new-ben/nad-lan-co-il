import os, sys
sys.stdout.reconfigure(encoding="utf-8")
REPO = r"C:\Users\777\nad-lan\nad-lan-co-il"
src = open(os.path.join(REPO, "scripts", "skin-a", "deployskin.py"), encoding="utf-8").read(); ns = {"__name__": "co"}
exec(compile(src[:src.index('s, h, _ = req("GET", "/wp-json/nadlan/v1/health")')], "h", "exec"), ns); req = ns["req"]
oid = int(sys.argv[1])
s, o, _ = req("GET", "/wp-json/wc/v3/orders/%d" % oid)
assert s == 200 and o["billing"]["email"] == "checkout-test@nad-lan.co.il" and o["status"] == "pending", (s, o.get("status"))
s, o, _ = req("PUT", "/wp-json/wc/v3/orders/%d" % oid, {"status": "cancelled"})
print(s, o.get("status"))
s, n, _ = req("POST", "/wp-json/wc/v3/orders/%d/notes" % oid, {"note": "הזמנת בדיקה של זרימת התשלום (7.11.2026). אחרי חיבור nad-lan.co.il במורנינג: טופס האשראי נטען (Grow). בוטלה."})
print("note", s)
