# -*- coding: utf-8 -*-
"""Round 2 pages (26.10.2026): the site skin forces its link colour and underline inside page content, so the primary CTA of /sde-dov/
(page 4730) and /dira-behanacha/ (page 8541) showed dark text on the dark button. One rule per page appended to the page's own CTA
styles with !important (colour and no underline). Exact anchored replacement, backup, read-back, live check."""
import io, os, sys, time, urllib.request
H = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.dirname(os.path.dirname(os.path.dirname(H)))
src = open(os.path.join(REPO, "scripts", "skin-a", "deployskin.py"), encoding="utf-8").read(); ns = {"__name__": "r2cta"}
exec(compile(src[:src.index('s, h, _ = req("GET", "/wp-json/nadlan/v1/health")')], "h", "exec"), ns)
req = ns["req"]
if hasattr(sys.stdout, "reconfigure"): sys.stdout.reconfigure(encoding="utf-8")
FIX = {
    4730: (".nls1-cta a.s{background:#fff;color:#1F4B5C}",
           ".nls1-cta a.s{background:#fff;color:#1F4B5C}.nls1-cta a.p,.nls1-cta a.p:visited,.nls1-cta a.p:hover{color:#fff!important}.nls1-cta a.s,.nls1-cta a.s:visited{color:#1F4B5C!important}.nls1-cta a{text-decoration:none!important}"),
    8541: (".nlg1-cta a.is-primary{background:#1F4B5C;color:#fff}",
           ".nlg1-cta a.is-primary{background:#1F4B5C;color:#fff}\n.nlg1-cta a.is-primary,.nlg1-cta a.is-primary:visited,.nlg1-cta a.is-primary:hover{color:#fff!important}.nlg1-cta a:not(.is-primary),.nlg1-cta a:not(.is-primary):visited{color:#1F4B5C!important}.nlg1-cta a{text-decoration:none!important}"),
}
bk = os.path.join(H, "page-backup"); os.makedirs(bk, exist_ok=True)
for pid, (old, new) in FIX.items():
    s, r, _ = req("GET", "/wp-json/wp/v2/pages/%d?context=edit&_fields=content,link" % pid)
    raw = r["content"]["raw"]
    if new in raw:
        print(pid, "already fixed"); continue
    assert raw.count(old) == 1, (pid, raw.count(old))
    io.open(os.path.join(bk, "page-%d-cta-%s.html" % (pid, time.strftime("%Y%m%d-%H%M%S"))), "w", encoding="utf-8", newline="").write(raw)
    out = raw.replace(old, new)
    req("POST", "/wp-json/wp/v2/pages/%d" % pid, {"content": out})
    back = req("GET", "/wp-json/wp/v2/pages/%d?context=edit&_fields=content" % pid)[1]["content"]["raw"]
    time.sleep(2)
    page = urllib.request.urlopen(urllib.request.Request(r["link"] + "?x=%d" % time.time(), headers={"User-Agent": "Mozilla/5.0"}), timeout=90).read().decode("utf-8", "replace")
    print(pid, "read-back", back.strip() == out.strip(), "| on page", "color:#fff!important" in page)
