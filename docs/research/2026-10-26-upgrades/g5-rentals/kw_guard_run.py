# -*- coding: utf-8 -*-
"""G5: runs tools/seo/kw_guard.py (unchanged) on the new page's title, H1, slug, meta and anchors, twice: (A) against the list as it
stands (no owner for "דירות להשכרה" / "דירה להשכרה": the guard must block, keyword-guard rule 7), (B) against a scratch copy of
docs/seo/protected-keywords.json where the proposed owner /דירות-להשכרה/ is set (the repo file is NOT changed; Ben names the owner).
Writes kw-guard.txt.  python kw_guard_run.py <gsc query,page csv> <scratch dir>"""
import io, json, os, shutil, subprocess, sys
if hasattr(sys.stdout, "reconfigure"): sys.stdout.reconfigure(encoding="utf-8")
H = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(H))))
GSC, TMP = sys.argv[1], sys.argv[2]
os.makedirs(os.path.join(TMP, "tools", "seo"), exist_ok=True); os.makedirs(os.path.join(TMP, "docs", "seo"), exist_ok=True)
shutil.copy(os.path.join(REPO, "tools", "seo", "kw_guard.py"), os.path.join(TMP, "tools", "seo", "kw_guard.py"))
d = json.load(io.open(os.path.join(REPO, "docs", "seo", "protected-keywords.json"), encoding="utf-8"))
for t in d["terms"]:
    if t["term"] in ("דירות להשכרה", "דירה להשכרה"): t["owner"] = "/דירות-להשכרה/"
io.open(os.path.join(TMP, "docs", "seo", "protected-keywords.json"), "w", encoding="utf-8").write(json.dumps(d, ensure_ascii=False))
src = io.open(os.path.join(H, "write_g5_page.py"), encoding="utf-8").read()
grab = lambda k: src.split(k + ' = "', 1)[1].split('"', 1)[0]
TITLE, SEO_T, SEO_D = grab("TITLE"), grab("SEO_T"), grab("SEO_D")
env = dict(os.environ, PYTHONIOENCODING="utf-8")
out = []
def run(tool, page, kind, text):
    r = subprocess.run([sys.executable, tool, "--page", page, "--kind", kind, "--text", text, "--gsc", GSC], capture_output=True, text=True, encoding="utf-8", env=env)
    out.append("== %s | %s | %s\n%s%sexit %d" % (kind, page, text, r.stdout, r.stderr, r.returncode))
LIVE = os.path.join(REPO, "tools", "seo", "kw_guard.py"); PROP = os.path.join(TMP, "tools", "seo", "kw_guard.py"); P = "/דירות-להשכרה/"
out.append("### A. The list as it stands (no owner yet): the guard blocks until Ben names the owner (keyword-guard rule 7)")
run(LIVE, P, "title", SEO_T); run(LIVE, P, "slug", "דירות-להשכרה")
out.append("\n### B. With the proposed owner /דירות-להשכרה/ (scratch copy of protected-keywords.json; the repo file is unchanged)")
run(PROP, P, "title", SEO_T); run(PROP, P, "h1", TITLE); run(PROP, P, "slug", "דירות-להשכרה"); run(PROP, P, "meta", SEO_D)
out.append("\n### C. The page's outgoing anchors (target, text)")
for tgt, txt in (("/post-listing/", "פרסום מודעה בחינם"), ("/my-rentals/", "ניהול נכסים מושכרים"), ("/cpi-calculator/", "מחשבון הצמדה למדד"),
                 ("/real-estate-lawyer/residential-lease-agreement/", "חוזה שכירות דירה"), ("/tabu-extract-check/", "בדיקת נסח טאבו"), ("/investment/", "נדל״ן להשקעה"),
                 ("/buy-vs-rent/", "מחשבון קנייה מול שכירות"), ("/properties/", "לכל המודעות באתר, עם סינון לפי עיר, חדרים ומחיר")):
    run(PROP, tgt, "anchor", txt)
out.append("\n### D. Today's sitewide anchors with the bare term point to /properties/?listing_type=rent (home-v3.php menus and grid, skin-a menu).\n"
           "Under the proposed owner the guard blocks them; re-pointing them is a sitewide link change (Ben's word, not done here).")
run(PROP, "/properties/", "anchor", "דירות להשכרה")
io.open(os.path.join(H, "kw-guard.txt"), "w", encoding="utf-8").write("\n".join(out) + "\n")
print("\n".join(out))
