# -*- coding: utf-8 -*-
"""G5 /דירות-להשכרה/ (26.10.2026): the skin's link colour (!important) beats ".nlrh-cta a.is-primary{color:#fff}", so the main button
"בדקו את שכר הדירה" showed teal on its deep fill, 1.68:1 (found by the 3.0 sweep, missed at 1.6). One scoped style right before the CTA
row, as in fix_r2_cta_c.py. Backup, read-back."""
import io, os, sys, time, urllib.parse
H = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.dirname(os.path.dirname(os.path.dirname(H)))
src = open(os.path.join(REPO, "scripts", "skin-a", "deployskin.py"), encoding="utf-8").read(); ns = {"__name__": "r2ctad"}
exec(compile(src[:src.index('s, h, _ = req("GET", "/wp-json/nadlan/v1/health")')], "h", "exec"), ns)
req = ns["req"]
if hasattr(sys.stdout, "reconfigure"): sys.stdout.reconfigure(encoding="utf-8")
SLUG, row = "דירות-להשכרה", "nlrh-cta"
pid = [x for x in req("GET", "/wp-json/wp/v2/pages?slug=%s&_fields=id,slug" % urllib.parse.quote(SLUG))[1]][0]["id"]
raw = req("GET", "/wp-json/wp/v2/pages/%d?context=edit&_fields=content" % pid)[1]["content"]["raw"]
tag = '<style id="%s-fix">' % row
if tag in raw:
    raise SystemExit("%d already fixed" % pid)
a = '<div class="%s">' % row
assert raw.count(a) == 1, raw.count(a)
css = tag + "html body .%s a[href],html body .%s a[href]:visited{color:#1F4B5C!important;text-decoration:none!important}html body .%s a.is-primary,html body .%s a.is-primary:visited{color:#fff!important}</style>\n" % (row, row, row, row)
bk = os.path.join(H, "page-backup"); os.makedirs(bk, exist_ok=True)
io.open(os.path.join(bk, "page-%d-cta-%s.html" % (pid, time.strftime("%Y%m%d-%H%M%S"))), "w", encoding="utf-8", newline="").write(raw)
out = raw.replace(a, css + a, 1)
req("POST", "/wp-json/wp/v2/pages/%d" % pid, {"content": out})
back = req("GET", "/wp-json/wp/v2/pages/%d?context=edit&_fields=content" % pid)[1]["content"]["raw"]
print(pid, row, "read-back", back.strip() == out.strip())
