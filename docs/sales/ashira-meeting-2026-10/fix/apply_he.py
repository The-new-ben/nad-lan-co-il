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
N = lambda x: x.replace(chr(13) + chr(10), chr(10))  # WordPress stores CRLF; the reviewed files are LF (same text)
cur = d["content"]["raw"]
NB = lambda x: [l for l in x.replace(chr(13), "").split(chr(10)) if l.strip()]
# WordPress keeps mixed line endings; the reviewed files lost them on a Windows text-mode save. So: compare non-blank lines
# with the reviewed snapshot, and build the target by applying the SAME reviewed edits to the live raw (whitespace preserved).
if rollback:
    if NB(cur) != NB(after): sys.exit("STOP: live is not the published repair. Nothing written.")
    built = open(os.path.join(HERE, "live-raw-before-publish.html"), "rb").read().decode("utf-8")
else:
    if NB(cur) != NB(before): sys.exit("STOP: the live content is not what this runner expects (someone edited it). Nothing written.")
    src2 = open(os.path.join(HERE, "patch_he2.py"), encoding="utf-8").read()
    src2 = src2.replace('t = open(os.path.join(HERE, "before-he-4744.html"), encoding="utf-8").read()', "t = LIVE")
    src2 = src2[:src2.index('open(os.path.join(HERE, "after-he-4744.html")')]
    g = {"LIVE": cur, "__file__": os.path.join(HERE, "patch_he2.py")}
    exec(compile(src2, "patch_he2", "exec"), g)
    built = g["t"]
    if NB(built) != NB(after): sys.exit("STOP: the edits applied to live do not reproduce the reviewed after-file. Nothing written.")
    open(os.path.join(HERE, "live-raw-before-publish.html"), "wb").write(cur.encode("utf-8"))
get = lambda: urllib.request.urlopen(urllib.request.Request("https://nad-lan.co.il/projects/ashira-sde-dov/?nlv=%d" % time.time(), headers={"User-Agent": "Mozilla/5.0 Chrome/128"}), timeout=90).read().decode("utf-8", "replace")
import re
inv = lambda h: (re.search(r"<title>(.*?)</title>", h, re.S).group(1).strip(), (re.search(r'rel="canonical" href="([^"]+)"', h) or [None, None])[1], h.count("<h1"))
lb = get(); open(os.path.join(HERE, "live-before.html"), "w", encoding="utf-8").write(lb)
target = built
s2, r2, _ = req("POST", "/wp-json/wp/v2/nadlan_project/4744", {"content": target})
if s2 not in (200, 201):
    sys.exit(f"FAIL: POST status {s2}. Run with --rollback manually if anything changed.")
s3, d3, _ = req("GET", "/wp-json/wp/v2/nadlan_project/4744?context=edit")
if d3["content"]["raw"] != target:
    sys.exit("FAIL: CMS fetch-back differs from the target. Manual --rollback required.")
time.sleep(3)
live = get(); open(os.path.join(HERE, "live-after.html"), "w", encoding="utf-8").write(live)
ok = True
if inv(live) != inv(lb):
    print("FAIL invariants: before", inv(lb), "after", inv(live)); ok = False
if not rollback:
    for x in ("תא ירוק", "נקודות העוגן לפי המקום", "סרטון יוטיוב", "בשלב הראשון נכון ליצור", "שערי איכות", "בדפי הפרויקטים הבאים"):
        if x in live: print("FAIL still there:", x); ok = False
if not ok:
    sys.exit("FAIL: verification failed. Do NOT write RELEASE DONE. Manual --rollback is available.")
print("PASS: status", s2, "| fetch-back equal | invariants", inv(live))
