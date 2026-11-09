# -*- coding: utf-8 -*-
"""HAD-689, Ben 9.11.2026 ("כן, תתחיל"): seven pages still link to /new-projects/new-projects-tel-aviv/, which answers 301 to
/projects/ since 1.72.619. Classic hygiene after a redirect: point the internal links straight at the final page, so no link
passes through a redirect. Only the href changes; the anchor text and everything else on the page stay as they are.
Hebrew pages -> /projects/ ; the English page -> /en/projects/ (its own language twin of the hub).
Dry run prints every occurrence with its context. --go: backup per page, exact replace, read-back.
python had689_fix_tlv_links.py [--go]"""
import io, json, os, re, sys, time
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.dirname(os.path.dirname(HERE))
src = open(os.path.join(REPO, "scripts", "skin-a", "deployskin.py"), encoding="utf-8").read(); ns = {"__name__": "rt"}
exec(compile(src[:src.index('s, h, _ = req("GET", "/wp-json/nadlan/v1/health")')], "h", "exec"), ns); req = ns["req"]
GO = "--go" in sys.argv
PAGES = {7214: "/projects/", 7215: "/en/projects/", 4603: "/projects/", 4601: "/projects/", 4505: "/projects/", 4503: "/projects/", 4489: "/projects/"}
OLD = re.compile(r'(https://nad-lan\.co\.il)?/new-projects/new-projects-tel-aviv/?(?=["\'#?])')
BK = os.path.join(REPO, "docs", "qa", "had689-2026-11-09", "links"); os.makedirs(BK, exist_ok=True)
stamp = time.strftime("%Y%m%dT%H%M%S")
total = 0
for pid, target in PAGES.items():
    s, g, _ = req("GET", "/wp-json/wp/v2/pages/%d?context=edit&_fields=id,link,status,content" % pid); assert s == 200, (pid, s)
    raw = g["content"]["raw"]
    hits = list(OLD.finditer(raw))
    print("\n== page %d %s (%s): %d link(s) -> %s" % (pid, g["link"].replace("https://nad-lan.co.il", ""), g["status"], len(hits), target))
    for m in hits:
        a = raw.rfind("<a", 0, m.start()); b = raw.find("</a>", m.end())
        print("   ", re.sub(r"\s+", " ", raw[a:b + 4] if a >= 0 and b > 0 else raw[max(0, m.start() - 120):m.end() + 120])[:400])
    total += len(hits)
    if not GO or not hits:
        continue
    io.open(os.path.join(BK, "page-%d-before-%s.json" % (pid, stamp)), "w", encoding="utf-8").write(json.dumps({"id": pid, "content": raw}, ensure_ascii=False))
    new = OLD.sub("https://nad-lan.co.il" + target, raw)
    assert new != raw and not OLD.search(new)
    s1, _, _ = req("POST", "/wp-json/wp/v2/pages/%d" % pid, {"content": new}); assert s1 in (200, 201), (pid, s1)
    s2, r, _ = req("GET", "/wp-json/wp/v2/pages/%d?context=edit&_fields=content" % pid)
    assert r["content"]["raw"] == new, ("read-back", pid)
    print("    [done] written and read back; backup page-%d-before-%s.json" % (pid, stamp))
print("\noccurrences:", total, "| mode:", "GO" if GO else "dry run")
