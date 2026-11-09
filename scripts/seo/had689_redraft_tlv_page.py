# -*- coding: utf-8 -*-
"""HAD-689, Ben 9.11.2026 (after the 1.72.624 correction): "this URL cannot exist... it's dragging down the new project page...
we need one page". So the Tel Aviv immediate-occupancy page (page 4484) goes back to "draft", exactly as on the morning of 9.11,
and release 1.72.624 is rolled back (the 301 to /projects/ returns). Run it AFTER the rollback, so the URL never answers 404.
Content, title and Yoast meta stay untouched and are compared with the backup; its content moves into /projects/ next, by hand.
python had689_redraft_tlv_page.py [--go]"""
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
s, g, _ = req("GET", "/wp-json/wp/v2/pages/%d?context=edit&_fields=id,status,title,content,meta" % PID); assert s == 200, s
print("[now] status=%s | content same as the morning backup: %s" % (g["status"], g["content"]["raw"] == b_content))
assert g["status"] == "publish", "expected publish, found %s" % g["status"]
assert g["content"]["raw"] == b_content, "the page changed since the backup: stop and read it by hand"
if not GO:
    print("[plan] status publish -> draft, nothing else"); sys.exit(0)
stamp = time.strftime("%Y%m%dT%H%M%S")
io.open(os.path.join(REPO, "docs", "qa", "had689-2026-11-09", "page-4484-before-redraft-%s.json" % stamp), "w", encoding="utf-8").write(
    json.dumps({"id": PID, "status": g["status"], "title": g["title"]["raw"], "content": g["content"]["raw"], "meta": g.get("meta")}, ensure_ascii=False))
s1, _, _ = req("POST", "/wp-json/wp/v2/pages/%d" % PID, {"status": "draft"}); assert s1 in (200, 201), s1
s, r, _ = req("GET", "/wp-json/wp/v2/pages/%d?context=edit&_fields=status,content" % PID)
assert r["status"] == "draft" and r["content"]["raw"] == b_content, "read-back"
print("[done] page %d is a draft again, content kept" % PID)
