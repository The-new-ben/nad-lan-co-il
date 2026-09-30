# -*- coding: utf-8 -*-
"""HAD-376: what the sight-line frame fix changed in places.json, project by project.

  python scripts/project-stage/sight_diff.py <before-dir>      (before-dir holds <project>.places.json, the files as they were)

Checks that every field other than "sight" is the same (places and landmarks, in order), then writes
docs/qa/had-376-sightlines/changes-<project>.csv (every place and landmark whose label changed on any floor band) and prints
the counts. Labels: street = the place itself is seen, roof = only its building's top, hidden = neither."""
import csv, io, json, os, sys
from collections import Counter
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT = os.path.join(REPO, "docs", "qa", "had-376-sightlines")
os.makedirs(OUT, exist_ok=True)
BEFORE = sys.argv[1]
lab = lambda v: v or "hidden"


def strip(items):
    return [{k: v for k, v in it.items() if k != "sight"} for it in items]


summary = {}
for pk in ("rainbow", "duo", "dimri", "ashira"):
    a = json.load(io.open(os.path.join(BEFORE, pk + ".places.json"), encoding="utf-8"))
    b = json.load(io.open(os.path.join(REPO, "plugins", "nadlan-config", "assets", "project-stage", pk, "places.json"), encoding="utf-8"))
    same_top = {k: a[k] for k in a if k not in ("places", "landmarks")} == {k: b[k] for k in b if k not in ("places", "landmarks")}
    same_items = strip(a["places"]) == strip(b["places"]) and strip(a.get("landmarks", [])) == strip(b.get("landmarks", []))
    if not (same_top and same_items):
        sys.exit(f"FATAL {pk}: something other than the sight lines changed (top {same_top}, items {same_items})")
    bands = sorted(a["places"][0]["sight"], key=int)
    rows, trans, seen_flip = [], Counter(), Counter()
    for kind, xs, ys in (("place", a["places"], b["places"]), ("landmark", a.get("landmarks", []), b.get("landmarks", []))):
        for p, q in zip(xs, ys):
            if p["sight"] == q["sight"]:
                continue
            row = {"kind": kind, "id": p.get("id", ""), "name": p.get("name") or p.get("pin", ""), "group": p.get("g", p.get("kind", "")),
                   "generic": p.get("generic", 0), "dist_m": p.get("dist"), "bearing": p.get("bearing"), "lat": p.get("lat", ""), "lng": p.get("lng", "")}
            for fl in bands:
                o, n = lab(p["sight"].get(fl)), lab(q["sight"].get(fl))
                row["floor_" + fl] = o if o == n else f"{o} -> {n}"
                if o != n:
                    trans[f"{o} -> {n}"] += 1
                    if (o == "hidden") != (n == "hidden"):
                        seen_flip["now shown" if o == "hidden" else "now hidden"] += 1
            rows.append(row)
    rows.sort(key=lambda r: (r["kind"] != "landmark", r["dist_m"] or 0))
    path = os.path.join(OUT, f"changes-{pk}.csv")
    with io.open(path, "w", encoding="utf-8-sig", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0].keys()) if rows else ["kind"])
        w.writeheader(); w.writerows(rows)
    named = sum(1 for r in rows if r["kind"] == "place" and not r["generic"])
    summary[pk] = {"places": len(a["places"]), "landmarks": len(a.get("landmarks", [])), "changed": len(rows), "changed_named": named,
                   "changed_landmarks": sum(1 for r in rows if r["kind"] == "landmark"), "bands": bands,
                   "transitions": dict(trans.most_common()), "shown_or_hidden_flips": dict(seen_flip)}
    print(f"{pk}: {len(rows)} of {len(a['places'])} places + {len(a.get('landmarks', []))} landmarks changed on some band "
          f"({named} named places, {summary[pk]['changed_landmarks']} landmarks); every other field identical")
    print("   ", dict(trans.most_common()), "| band flips shown/hidden:", dict(seen_flip))
json.dump(summary, io.open(os.path.join(OUT, "summary.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("written:", OUT)
