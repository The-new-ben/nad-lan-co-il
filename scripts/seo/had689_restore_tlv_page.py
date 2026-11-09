# -*- coding: utf-8 -*-
"""HAD-689 correction, Ben 9.11.2026 ("כן, תתחיל"): the Tel Aviv immediate-occupancy page (page 4484,
/new-projects/new-projects-tel-aviv/) was redirected to /projects/ BEFORE its content had a home there. The right order is the
reverse: content first, redirect after. So the page goes back to "publish" exactly as it was (title, content and Yoast meta are
compared with the backup taken before it went to draft), and the redirect for its path is removed in release 1.72.624.
Step 1 (this script) runs first: while the redirect still answers for the path, publishing changes nothing a visitor sees.
python had689_restore_tlv_page.py [--go]"""
import io, json, os, sys, time
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.dirname(os.path.dirname(HERE))
src = open(os.path.join(REPO, "scripts", "skin-a", "deployskin.py"), encoding="utf-8").read(); ns = {"__name__": "rt"}
exec(compile(src[:src.index('s, h, _ = req("GET", "/wp-json/nadlan/v1/health")')], "h", "exec"), ns); req = ns["req"]
GO = "--go" in sys.argv
PID = 4484
BK = os.path.join(REPO, "docs", "qa", "had689-2026-11-09", "page-4484-before-draft-20261109T100837.json")
b = json.load(io.open(BK, encoding="utf-8"))
b_content = b["content"]["raw"] if isinstance(b["content"], dict) else b["content"]
b_title = b["title"]["raw"] if isinstance(b["title"], dict) else b["title"]

s, g, _ = req("GET", "/wp-json/wp/v2/pages/%d?context=edit&_fields=id,status,title,content,meta,slug,link" % PID); assert s == 200, s
same_c = g["content"]["raw"] == b_content
same_t = g["title"]["raw"] == b_title
meta_diff = {k: ((g.get("meta") or {}).get(k), v) for k, v in (b.get("meta") or {}).items() if (g.get("meta") or {}).get(k) != v}
print("[now] status=%s slug=%s" % (g["status"], g.get("slug")))
print("[check] content same as backup: %s (%d chars) | title same: %s | meta differences: %s" % (same_c, len(g["content"]["raw"]), same_t, meta_diff or "none"))
assert g["status"] == "draft", "expected draft, found %s" % g["status"]
assert same_c and same_t and not meta_diff, "the page changed since the backup: stop and read it by hand"
if not GO:
    print("[plan] status draft -> publish, nothing else"); sys.exit(0)
stamp = time.strftime("%Y%m%dT%H%M%S")
io.open(os.path.join(REPO, "docs", "qa", "had689-2026-11-09", "page-4484-before-republish-%s.json" % stamp), "w", encoding="utf-8").write(
    json.dumps({"id": PID, "status": g["status"], "title": g["title"]["raw"], "content": g["content"]["raw"], "meta": g.get("meta")}, ensure_ascii=False))
s1, _, _ = req("POST", "/wp-json/wp/v2/pages/%d" % PID, {"status": "publish"}); assert s1 in (200, 201), s1
s, r, _ = req("GET", "/wp-json/wp/v2/pages/%d?context=edit&_fields=status,title,content,meta,link" % PID)
assert r["status"] == "publish" and r["content"]["raw"] == b_content and r["title"]["raw"] == b_title, "read-back"
print("[done] page %d published again, content and title identical to the backup; link %s" % (PID, r.get("link")))
