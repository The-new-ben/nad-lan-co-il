# -*- coding: utf-8 -*-
"""HAD-654 radius loop R7: create one new project page for a gap project from a ChatGPT-written article (HTML file) and a spec
(JSON: slug, title, meta, kit_name). The article is checked first: the language-DNA blacklist, no long dash, no h1, and every
number in it must appear in the spec's allowed list (the brief's sourced facts). The page opens with [nadlan_project_facts] and
ends with [nadlan_radius_prices] and [nadlan_project_kit]: both render nothing until their data holds the new id (next release).
Usage: gap_page_create.py <spec.json> <article.html> [--dry]. Writes docs/qa/gap-pages/<slug>-created.json."""
import json, os, re, sys
H = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.dirname(os.path.dirname(H))
ARGV = list(sys.argv[1:]); sys.path.insert(0, H); os.chdir(REPO)
SPEC, ART = ARGV[0], ARGV[1]
spec = json.load(open(SPEC, encoding="utf-8"))
html = open(ART, encoding="utf-8").read().strip()
BLACK = ["ממשק", "דמו", "הדגמה", "מודל", "מנגנון", "נקודות חמות", "נקודה חמה", "שכבה", "אינטראקטיב", "רספונסיבי", "סקיצה",
         "פלטפורמה", "טכנולוגיה", "סימולציה", "תלת ממד", "תלת-ממד", "בקרוב", "בבדיקה", "אטלס", "הכי ", "—", "–"]
bad = [w for w in BLACK if w in re.sub(r"<[^>]+>", " ", html)]
if "<h1" in html.lower():
    bad.append("<h1>")
nums = set(re.findall(r"\d[\d,\.]*\d|\d", re.sub(r"<[^>]+>", " ", html)))
allowed = set(spec["allowed_numbers"])
extra = sorted(n for n in nums if n.replace(",", "") not in {a.replace(",", "") for a in allowed})
print("blacklist:", bad or "clean"); print("numbers not in the brief:", extra or "none")
if bad or extra:
    raise SystemExit("STOP: fix the article first")
body = "[nadlan_project_facts]\n\n<!-- wp:html -->\n" + html + "\n<!-- /wp:html -->\n\n[nadlan_radius_prices]\n\n[nadlan_project_kit]"
if "--dry" in ARGV:
    print("[dry] ok,", len(re.sub(r"<[^>]+>", " ", html).split()), "words"); raise SystemExit(0)
RUNNER = sorted([f for f in os.listdir(H) if f.startswith("deploy5") and f.endswith(".py") and f[6:9].isdigit()])[-1]
src = open(os.path.join(H, RUNNER), encoding="utf-8").read(); sys.argv = [RUNNER, "--finish"]
ns = {"__name__": "gap", "__file__": os.path.join(H, RUNNER)}
exec(compile(src[:src.index("def page(path):")], RUNNER, "exec"), ns)
req, must = ns["req"], ns["must"]
s, ex = req("GET", f"/wp-json/wp/v2/nadlan_project?slug={spec['slug']}&status=publish,draft&_fields=id")
if isinstance(ex, list) and ex:
    raise SystemExit(f"STOP: a project with slug {spec['slug']} exists already: {ex}")
meta = dict(spec["meta"]); meta["nadlan_kit_name"] = spec["kit_name"]
st, d = req("POST", "/wp-json/wp/v2/nadlan_project", {"title": spec["title"], "slug": spec["slug"], "status": "publish", "content": body, "meta": meta})
must(st, d, "create")
out = {"id": d["id"], "slug": d["slug"], "link": d["link"], "status": d["status"], "meta_back": {k: (d.get("meta") or {}).get(k) for k in meta}}
os.makedirs(os.path.join(REPO, "docs", "qa", "gap-pages"), exist_ok=True)
json.dump(out, open(os.path.join(REPO, "docs", "qa", "gap-pages", spec["slug"] + "-created.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(json.dumps(out, ensure_ascii=False))
