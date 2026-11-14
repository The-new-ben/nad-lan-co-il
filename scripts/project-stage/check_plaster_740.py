# -*- coding: utf-8 -*-
"""HAD-740 stage 2 check, read-only, no gate: every catalog page (/projects/page/N/) is read as a visitor. Counts default-picture
cards, cards still showing one of the 49 plaster files (by their exact file names from featured.json), and where the 49 former
plaster pages' cards are and what they show. Also reads the 49 project pages themselves (http 200).
python scripts/project-stage/check_plaster_740.py"""
import io, json, os, re, time, urllib.request
HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.dirname(os.path.dirname(HERE))
d = json.load(io.open(os.path.join(REPO, "docs", "design", "project-defaults-2026-11", "fable", "audit", "featured.json"), encoding="utf-8"))
rec = json.load(io.open(os.path.join(REPO, "docs", "qa", "project-stage-2026-09-24", "plaster-thumbs-removed-2026-11-14.json"), encoding="utf-8"))
names = sorted({d["media"][k]["slug"] for k in d["media"] if 7531 <= int(k) <= 7580})
slugs = {r["slug"] for r in rec["rows"]}
UA = {"User-Agent": "Mozilla/5.0 (site owner audit)"}


def get(u):
    with urllib.request.urlopen(urllib.request.Request(u, headers=UA), timeout=120) as f:
        return f.read().decode("utf-8", "replace")


out = {"pages": 0, "default": 0, "plaster_hits": [], "former": {}}
n = 1
while True:
    u = "https://nad-lan.co.il/projects/" + ("" if n == 1 else "page/%d/" % n) + "?nl740=%d" % int(time.time())
    try:
        h = get(u)
    except Exception as e:
        break
    cards = re.findall(r'<a class="nldc nldc-project[^"]*" href="https://nad-lan\.co\.il/projects/([^/"]+)/".*?<div class="nldc-media([^"]*)">\s*<img src="([^"]+)"', h, re.S)
    if not cards:
        break
    out["pages"] += 1
    for slug, cls, src in cards:
        if "has-default-pic" in cls:
            out["default"] += 1
        if any(nm in src for nm in names):
            out["plaster_hits"].append((n, slug, src[-60:]))
        s2 = urllib.request.unquote(slug)
        if s2 in slugs or slug in slugs:
            out["former"][s2] = (n, cls.strip(), src.split("/")[-1][:60])
    if n == 1:
        out["page1_first"] = [c[0] for c in cards[:6]]
        out["page1_default"] = sum(1 for c in cards if "has-default-pic" in c[1])
    n += 1
print("catalog pages read", out["pages"], "| default cards", out["default"], "| cards still showing a plaster file", len(out["plaster_hits"]), out["plaster_hits"][:5])
print("page 1: default cards", out.get("page1_default"), "| first", out.get("page1_first"))
print("former plaster pages found in the catalog", len(out["former"]), "of", len(slugs), "| not default:", [(k, v) for k, v in out["former"].items() if "has-default-pic" not in v[1]][:5])
bad = []
for r in rec["rows"]:
    try:
        h = get(r["url"] + ("&" if "?" in r["url"] else "?") + "nl740=1")
        if any(nm in h for nm in names) and "og:image" in h:
            m = re.search(r'<meta property="og:image" content="([^"]+)"', h)
            if m and any(nm in m.group(1) for nm in names):
                bad.append((r["slug"], "og still plaster"))
    except Exception as e:
        bad.append((r["slug"], str(e)[:60]))
print("project pages read", len(rec["rows"]), "| problems", bad[:8])
missing = sorted(slugs - set(out["former"]))
print("former plaster pages not in the catalog listing:", len(missing), missing[:6])
