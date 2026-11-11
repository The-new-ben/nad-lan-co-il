# -*- coding: utf-8 -*-
"""HAD-712 (Ben 11.11.2026, evening: "search by hand how people really look for it; those suggested keywords go into the title and the
page, some of them at the very start"). The manual search in the owner's Chrome (docs/research/2026-11-11-kikar-search/manual-2026-11-11/,
five screenshots) shows Google's own suggestions: "כיכר המדינה פרויקט" is the second suggestion for the bare name and "פרויקט כיכר המדינה"
has ten continuations, yet the phrase was not in the page's opening sentence. This edit puts it there, with "מגדלי מגורים".
One anchored replacement on the LIVE post 8113; md5 pinned; backup before; read-back after; dry by default.
The page <title> is NOT changed here: a release check row requires the current title, so it changes only inside a release that
rewrites that row, and only after Ben sees the new wording.   python scripts/kikar/had712_lead.py [--go]"""
import hashlib, io, json, os, sys, time
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.dirname(os.path.dirname(HERE))
src = open(os.path.join(REPO, "scripts", "skin-a", "deployskin.py"), encoding="utf-8").read(); ns = {"__name__": "h712l"}
exec(compile(src[:src.index('s, h, _ = req("GET", "/wp-json/nadlan/v1/health")')], "h", "exec"), ns); req = ns["req"]
GO = "--go" in sys.argv
PID, SLUG, PIN = 8113, "hamedina", "733668e17282fdf3198111166ecc04cc"  # modified 2026-11-11T18:29:44 (the pictures)
OLD = "<p>מגדלי כיכר המדינה (Kikar Hamedina Towers) בצפון תל אביב הם שלושה מגדלים ובהם 453 דירות,"
NEW = "<p>מגדלי כיכר המדינה (Kikar Hamedina Towers), פרויקט כיכר המדינה בצפון תל אביב, הם שלושה מגדלי מגורים ובהם 453 דירות,"
s, g, _ = req("GET", "/wp-json/wp/v2/nadlan_project/%d?context=edit&_fields=id,slug,modified,content" % PID)
assert s == 200 and g["slug"] == SLUG, (s, g.get("slug"))
raw = g["content"]["raw"]
now = hashlib.md5(raw.encode("utf-8")).hexdigest()
if now != PIN:
    raise SystemExit("the live post changed since it was read (%s, modified %s): read it again before replacing anything" % (now[:10], g["modified"]))
assert raw.count(OLD) == 1 and raw.startswith(OLD), "the opening sentence is not where it was"
new = raw.replace(OLD, NEW)
print("[plan] post %d: the opening sentence; %d -> %d chars" % (PID, len(raw), len(new)))
if not GO:
    sys.exit(0)
bk = os.path.join(REPO, "docs", "qa", "had-712"); os.makedirs(bk, exist_ok=True)
stamp = time.strftime("%Y%m%dT%H%M%S")
io.open(os.path.join(bk, "backup-%d-%s.html" % (PID, stamp)), "w", encoding="utf-8", newline="").write(raw)
s1, r1, _ = req("POST", "/wp-json/wp/v2/nadlan_project/%d" % PID, {"content": new})
assert s1 in (200, 201), (s1, str(r1)[:300])
s, r, _ = req("GET", "/wp-json/wp/v2/nadlan_project/%d?context=edit&_fields=content,modified" % PID)
ok = r["content"]["raw"] == new
json.dump({"stamp": stamp, "result": {"post": PID, "before_md5": now, "after_md5": hashlib.md5(r["content"]["raw"].encode("utf-8")).hexdigest(), "read_back_equal": ok, "modified": r.get("modified")}},
          open(os.path.join(bk, "result-lead-%s.json" % stamp), "w", encoding="utf-8"), indent=1)
if not ok:
    sb, _, _ = req("POST", "/wp-json/wp/v2/nadlan_project/%d" % PID, {"content": raw})
    raise SystemExit("read-back differs: restored the backup (http %s)" % sb)
print("[done] post %d written and read back (%s)" % (PID, stamp))
