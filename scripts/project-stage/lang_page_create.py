# -*- coding: utf-8 -*-
"""HAD-654 radius loop R8: create the language pages of a project, /projects/<base>-en|fr|ru|ar/, each its own nadlan_project post
with its own article (written by ChatGPT from the same sourced brief, checked here: no long dash, no h1, every number in the
brief's allowed list). inc/project-lang.php joins a slug ending -(en|fr|ru|ar) to its Hebrew page by itself: the language
context, the chrome and the hreflang cluster. Usage: lang_page_create.py <spec.json> <base-slug> <lang>@@<title>@@<article.html> ...
[--dry]. Writes docs/qa/gap-pages/<base>-<lang>-created.json. A slug that exists already is never touched."""
import json, os, re, sys
H = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.dirname(os.path.dirname(H))
ARGV = list(sys.argv[1:]); sys.path.insert(0, H); os.chdir(REPO)
SPEC, BASE = ARGV[0], ARGV[1]
ITEMS = [a.split("@@", 2) for a in ARGV[2:] if not a.startswith("--")]
allowed = {a.replace(",", "").replace(" ", "") for a in json.load(open(SPEC, encoding="utf-8"))["allowed_numbers"]}
jobs = []
for lang, title, art in ITEMS:
    assert lang in ("en", "fr", "ru", "ar"), lang
    html = open(art, encoding="utf-8").read().strip()
    txt = re.sub(r"<[^>]+>", " ", html)
    bad = [w for w in ("—", "–") if w in txt + title] + (["<h1>"] if "<h1" in html.lower() else [])
    # thousands may be written 2 200 (fr, ru) or 2,200; decimals 8,7 (fr, ru) or 8.7
    nums = re.findall(r"\d+(?:[   ,\.]\d+)*", txt)
    extra = sorted({n for n in nums if re.sub(r"[   ,]", "", n) not in allowed and n.replace(",", ".") not in allowed})
    print(f"[{lang}] {len(txt.split())} words | bad: {bad or 'none'} | numbers not in the brief: {extra or 'none'}")
    if bad or extra:
        raise SystemExit("STOP: fix the article first")
    jobs.append((lang, title, "<!-- wp:html -->\n" + html + "\n<!-- /wp:html -->"))
if "--dry" in ARGV:
    raise SystemExit(0)
RUNNER = sorted([f for f in os.listdir(H) if f.startswith("deploy5") and f.endswith(".py") and f[6:9].isdigit()])[-1]
src = open(os.path.join(H, RUNNER), encoding="utf-8").read(); sys.argv = [RUNNER, "--finish"]
ns = {"__name__": "lang", "__file__": os.path.join(H, RUNNER)}
exec(compile(src[:src.index("def page(path):")], RUNNER, "exec"), ns)
req, must = ns["req"], ns["must"]
for lang, title, body in jobs:
    slug = f"{BASE}-{lang}"
    s, ex = req("GET", f"/wp-json/wp/v2/nadlan_project?slug={slug}&status=publish,draft&_fields=id")
    if isinstance(ex, list) and ex:
        print(f"[skip] {slug} exists already: {ex}"); continue
    st, d = req("POST", "/wp-json/wp/v2/nadlan_project", {"title": title, "slug": slug, "status": "publish", "content": body})
    must(st, d, "create " + slug)
    out = {"id": d["id"], "slug": d["slug"], "link": d["link"], "status": d["status"], "title": title}
    json.dump(out, open(os.path.join(REPO, "docs", "qa", "gap-pages", slug + "-created.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(json.dumps(out, ensure_ascii=False))
