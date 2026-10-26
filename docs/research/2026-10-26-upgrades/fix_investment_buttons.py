# -*- coding: utf-8 -*-
"""/investment/ (page 421), 26.10.2026: two core button blocks ("קבעו ייעוץ עם עורך דין", "מחשבון מס רכישה") had text in the skin's
link colour #2F6F86 on a #2F6F86 fill = invisible. One scoped style before the first buttons block (white text, no underline).
Backup, read-back, live check."""
import io, os, sys, time, urllib.request
H = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.dirname(os.path.dirname(os.path.dirname(H)))
src = open(os.path.join(REPO, "scripts", "skin-a", "deployskin.py"), encoding="utf-8").read(); ns = {"__name__": "invbtn"}
exec(compile(src[:src.index('s, h, _ = req("GET", "/wp-json/nadlan/v1/health")')], "h", "exec"), ns)
req = ns["req"]
if hasattr(sys.stdout, "reconfigure"): sys.stdout.reconfigure(encoding="utf-8")
PID = 421
STYLE = '<style id="nlinv-btn">.wp-block-button:not(.is-style-outline) .wp-block-button__link,.wp-block-button:not(.is-style-outline) .wp-block-button__link:visited{color:#fff!important;text-decoration:none!important}</style>\n'
s, r, _ = req("GET", "/wp-json/wp/v2/pages/%d?context=edit&_fields=content,link" % PID)
raw = r["content"]["raw"]
if 'id="nlinv-btn"' in raw:
    sys.exit("already fixed")
A = '<div class="wp-block-buttons'
i = raw.find(A); assert i > 0
bk = os.path.join(H, "page-backup"); os.makedirs(bk, exist_ok=True)
io.open(os.path.join(bk, "page-%d-buttons-%s.html" % (PID, time.strftime("%Y%m%d-%H%M%S"))), "w", encoding="utf-8", newline="").write(raw)
new = raw[:i] + STYLE + raw[i:]
req("POST", "/wp-json/wp/v2/pages/%d" % PID, {"content": new})
back = req("GET", "/wp-json/wp/v2/pages/%d?context=edit&_fields=content" % PID)[1]["content"]["raw"]
time.sleep(2)
page = urllib.request.urlopen(urllib.request.Request(r["link"] + "?x=%d" % time.time(), headers={"User-Agent": "Mozilla/5.0"}), timeout=90).read().decode("utf-8", "replace")
print("read-back", back.strip() == new.strip(), "| style on page", 'id="nlinv-btn"' in page)
