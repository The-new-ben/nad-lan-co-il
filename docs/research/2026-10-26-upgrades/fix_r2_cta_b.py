# -*- coding: utf-8 -*-
"""Round 2 pages of 1.72.531 (26.10.2026): the skin's link colour and underline reach the CTA rows of /urban-renewal/pinui-binui/ (nlpb-cta)
and /urban-renewal/ (nlur3-cta): primary text 1.68:1 on its fill, tan underlines. One scoped style right before each CTA row. Backup,
read-back, live check."""
import io, os, sys, time, urllib.request
H = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.dirname(os.path.dirname(os.path.dirname(H)))
src = open(os.path.join(REPO, "scripts", "skin-a", "deployskin.py"), encoding="utf-8").read(); ns = {"__name__": "r2ctab"}
exec(compile(src[:src.index('s, h, _ = req("GET", "/wp-json/nadlan/v1/health")')], "h", "exec"), ns)
req = ns["req"]
if hasattr(sys.stdout, "reconfigure"): sys.stdout.reconfigure(encoding="utf-8")
FIX = [("pinui-binui", "nlpb-cta", "nlpb-go"), ("urban-renewal", "nlur3-cta", "nlur3-go")]
bk = os.path.join(H, "page-backup"); os.makedirs(bk, exist_ok=True)
for slug, row, go in FIX:
    pid = req("GET", "/wp-json/wp/v2/pages?slug=%s&_fields=id,link,parent" % slug)[1]
    pid = [x for x in pid if x["link"].rstrip("/").endswith("/" + slug)][0]
    raw = req("GET", "/wp-json/wp/v2/pages/%d?context=edit&_fields=content" % pid["id"])[1]["content"]["raw"]
    tag = '<style id="%s-fix">' % row
    if tag in raw:
        print(slug, "already fixed"); continue
    a = '<div class="%s"' % row
    assert raw.count(a) == 1, (slug, raw.count(a))
    css = tag + ".%s a.%s,.%s a.%s:visited,.%s a.%s:hover{color:#fff!important}.%s a{text-decoration:none!important}.%s a:not(.%s),.%s a:not(.%s):visited{color:#1F4B5C!important}</style>\n" % (row, go, row, go, row, go, row, row, go, row, go)
    io.open(os.path.join(bk, "page-%d-cta-%s.html" % (pid["id"], time.strftime("%Y%m%d-%H%M%S"))), "w", encoding="utf-8", newline="").write(raw)
    out = raw.replace(a, css + a, 1)
    req("POST", "/wp-json/wp/v2/pages/%d" % pid["id"], {"content": out})
    back = req("GET", "/wp-json/wp/v2/pages/%d?context=edit&_fields=content" % pid["id"])[1]["content"]["raw"]
    print(slug, pid["id"], "read-back", back.strip() == out.strip())
