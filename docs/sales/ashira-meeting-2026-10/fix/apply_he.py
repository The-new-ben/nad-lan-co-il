# -*- coding: utf-8 -*-
"""HAD-543: publish the narrow Hebrew Ashira article repair (post 4744) ONLY on Ben's direct word.
Checks the live CMS content still equals before-he-4744.html (no one edited since), saves the live raw HTML before,
writes after-he-4744.html, verifies the live page, and keeps everything for rollback (rollback = POST before-he-4744.html)."""
import os, sys, time, urllib.request
HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", "..", "..", ".."))
src = open(os.path.join(REPO, "scripts", "skin-a", "deployskin.py"), encoding="utf-8").read()
ns = {"__name__": "apply"}
exec(compile(src[:src.index('s, h, _ = req("GET", "/wp-json/nadlan/v1/health")')], "h", "exec"), ns)
req = ns["req"]
before = open(os.path.join(HERE, "before-he-4744.html"), encoding="utf-8").read()
after = open(os.path.join(HERE, "after-he-4744.html"), encoding="utf-8").read()
rollback = "--rollback" in sys.argv
s, d, _ = req("GET", "/wp-json/wp/v2/nadlan_project/4744?context=edit")
cur = d["content"]["raw"]
if cur != (after if rollback else before):
    sys.exit("STOP: the live content is not what this runner expects (someone edited it). Nothing written.")
get = lambda: urllib.request.urlopen(urllib.request.Request("https://nad-lan.co.il/projects/ashira-sde-dov/?nlv=%d" % time.time(), headers={"User-Agent": "Mozilla/5.0 Chrome/128"}), timeout=90).read().decode("utf-8", "replace")
open(os.path.join(HERE, "live-before.html"), "w", encoding="utf-8").write(get())
s2, r2, _ = req("POST", "/wp-json/wp/v2/nadlan_project/4744", {"content": before if rollback else after})
print("saved", s2)
time.sleep(3)
live = get()
open(os.path.join(HERE, "live-after.html"), "w", encoding="utf-8").write(live)
for x in ("תא ירוק", "נקודות העוגן לפי המקום", "סרטון יוטיוב", "בשלב הראשון נכון ליצור"):
    print("gone" if x not in live else "STILL THERE", x)
import re
print("title:", re.search(r"<title>(.*?)</title>", live, re.S).group(1).strip(), "| h1:", live.count("<h1"), "| canonical:", re.search(r'rel="canonical" href="([^"]+)"', live).group(1))
