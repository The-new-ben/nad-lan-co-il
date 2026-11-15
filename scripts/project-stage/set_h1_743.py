# -*- coding: utf-8 -*-
"""HAD-743: the H1 of /developer-deals/ (page 7214) is inside the article. Replace its text with the wording Ben approved on
15.11.2026; the h1's id (anchor) stays, nothing else in the article changes, the publish date stays. Backup of the raw content
before the change goes to docs/research/2026-11-15-deals-board/. python scripts/project-stage/set_h1_743.py"""
import io, os, re, time
HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.dirname(os.path.dirname(HERE))
src = open(os.path.join(REPO, "scripts", "skin-a", "deployskin.py"), encoding="utf-8").read()
ns = {"__name__": "h1743"}
exec(compile(src[:src.index('s, h, _ = req("GET", "/wp-json/nadlan/v1/health")')], "deployskin-helpers", "exec"), ns)
req = ns["req"]
OLD = "מבצעי קבלנים 2026: 20/80, 10/90, מכרזי דירות וההנחות שבאמת שוות כסף"
NEW = "מבצעי קבלנים 2026: מפת כל המבצעים בישראל"
s, r, _ = req("GET", "/wp-json/wp/v2/pages/7214?context=edit&_fields=content,date")
raw, date = r["content"]["raw"], r["date"]
h1 = re.findall(r'(<h1[^>]*>)(.*?)(</h1>)', raw, re.S)
assert len(h1) == 1 and h1[0][1] == OLD, h1
io.open(os.path.join(REPO, "docs", "research", "2026-11-15-deals-board", "page-7214-raw-before-h1-%s.html" % time.strftime("%Y%m%dT%H%M%S")), "w", encoding="utf-8").write(raw)
new_raw = raw.replace(h1[0][0] + OLD + h1[0][2], h1[0][0] + NEW + h1[0][2], 1)
assert len(new_raw) == len(raw) - len(OLD) + len(NEW)
s, r2, _ = req("POST", "/wp-json/wp/v2/pages/7214", {"content": new_raw})
print("http", s, "| date kept:", r2.get("date") == date)
s, r3, _ = req("GET", "/wp-json/wp/v2/pages/7214?context=edit&_fields=content")
print("h1 now:", re.findall(r'<h1[^>]*>(.*?)</h1>', r3["content"]["raw"], re.S))
