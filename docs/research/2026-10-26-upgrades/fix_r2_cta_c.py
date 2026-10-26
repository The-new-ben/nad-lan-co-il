# -*- coding: utf-8 -*-
"""G7 /real-estate-appraiser/ (page 86, nlsm-cta) and G8 /real-estate-lawyer/ (page 11, nlod-cta), 26.10.2026: on the guide template the
skin's "body.nl-skin-a .nadlan-guide a" (0,2,2, !important) beat the CTA rules, so the primary button showed teal text on its deep fill
(seen on the 390 px screenshots). One scoped style right before each CTA row, stronger by one element. Backup, read-back."""
import io, os, sys, time
H = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.dirname(os.path.dirname(os.path.dirname(H)))
src = open(os.path.join(REPO, "scripts", "skin-a", "deployskin.py"), encoding="utf-8").read(); ns = {"__name__": "r2ctac"}
exec(compile(src[:src.index('s, h, _ = req("GET", "/wp-json/nadlan/v1/health")')], "h", "exec"), ns)
req = ns["req"]
if hasattr(sys.stdout, "reconfigure"): sys.stdout.reconfigure(encoding="utf-8")
FIX = [(86, "nlsm-cta", "nlsm-go"), (11, "nlod-cta", "nlod-go")]
bk = os.path.join(H, "page-backup"); os.makedirs(bk, exist_ok=True)
for pid, row, go in FIX:
    raw = req("GET", "/wp-json/wp/v2/pages/%d?context=edit&_fields=content" % pid)[1]["content"]["raw"]
    tag = '<style id="%s-fix">' % row
    if tag in raw:
        print(pid, "already fixed"); continue
    a = '<div class="%s"' % row
    assert raw.count(a) == 1, (pid, raw.count(a))
    css = tag + "html body .%s a[href],html body .%s a[href]:visited{color:#1F4B5C!important;text-decoration:none!important}html body .%s a.%s,html body .%s a.%s:visited{color:#fff!important}</style>\n" % (row, row, row, go, row, go)
    io.open(os.path.join(bk, "page-%d-cta-%s.html" % (pid, time.strftime("%Y%m%d-%H%M%S"))), "w", encoding="utf-8", newline="").write(raw)
    out = raw.replace(a, css + a, 1)
    req("POST", "/wp-json/wp/v2/pages/%d" % pid, {"content": out})
    back = req("GET", "/wp-json/wp/v2/pages/%d?context=edit&_fields=content" % pid)[1]["content"]["raw"]
    print(pid, row, "read-back", back.strip() == out.strip())
