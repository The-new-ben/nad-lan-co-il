# -*- coding: utf-8 -*-
"""Round N follow-up (HAD-675): in the lead of page 121, the money sentence goes back before the definition sentence (benchmark
first_money_y 302 -> 356 after round N); both stay in the first paragraph. One anchored swap. python fix_lead_order_n.py [--dry]"""
import io, os, re, sys, time, urllib.request
H = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.abspath(os.path.join(H, "..", "..", "..", ".."))
if hasattr(sys.stdout, "reconfigure"): sys.stdout.reconfigure(encoding="utf-8")
src = open(os.path.join(REPO, "scripts", "skin-a", "deployskin.py"), encoding="utf-8").read(); ns = {"__name__": "fx"}
exec(compile(src[:src.index('s, h, _ = req("GET", "/wp-json/nadlan/v1/health")')], "h", "exec"), ns); req = ns["req"]
s, r, _ = req("GET", "/wp-json/wp/v2/pages/121?context=edit&_fields=content,link"); assert s == 200, s
raw = r["content"]["raw"]
DEF = "משכנתא, ובכתיב הרשמי משכנתה, היא הלוואה לקניית דירה שהדירה משועבדת בה לבנק ונרשמת בטאבו עד הסילוק. "
m = re.search(r'<p class="nlu1-lead">(.*?)</p>', raw, re.S); assert m and raw.count('<p class="nlu1-lead">') == 1
lead = m.group(1); assert lead.count(DEF) == 1, lead[:200]
i = lead.index(DEF); rest = lead[i + len(DEF):]; head = lead[:i]
new_lead = head + rest.rstrip() + " " + DEF.rstrip()
print("OLD:", lead); print("NEW:", new_lead)
new = raw.replace(m.group(0), '<p class="nlu1-lead">' + new_lead + '</p>', 1)
if "--dry" in sys.argv: sys.exit(0)
bk = os.path.join(H, "page-backup"); os.makedirs(bk, exist_ok=True)
io.open(os.path.join(bk, "page-121-%s.html" % time.strftime("%Y%m%d-%H%M%S")), "w", encoding="utf-8", newline="").write(raw)
s2, _, _ = req("POST", "/wp-json/wp/v2/pages/121", {"content": new}); assert s2 in (200, 201), s2
time.sleep(3)
page = urllib.request.urlopen(urllib.request.Request(r["link"] + "?x=%d" % time.time(), headers={"User-Agent": "Mozilla/5.0"}), timeout=90).read().decode("utf-8", "replace")
print("live:", new_lead[:60] in page)
