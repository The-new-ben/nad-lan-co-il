# -*- coding: utf-8 -*-
"""Summarise discover-*.json compactly: h1/lead y, big id blocks in order, controls grouped by section."""
import json, sys, os, collections
HERE = os.path.dirname(os.path.abspath(__file__))
for key in sys.argv[1:]:
    d = json.load(open(os.path.join(HERE, f"discover-{key}.json"), encoding="utf-8"))
    print("=" * 30, key, d["title"], "H", d["scrollHeight"])
    for h in d["h1"]: print("H1", h["y"], h["v"], h["t"][:90])
    for l in d["lead"]: print("LEAD", l["y"], l["v"], l["t"][:90])
    seen = set()
    for i in sorted(d["ids"], key=lambda r: r["y"]):
        if i["h"] < 150 or i["id"] in seen: continue
        seen.add(i["id"]); print(f"  ID {i['y']:>6} h{i['h']:>5} {i['tag']} #{i['id']} .{i['cls'][:40]}")
    g = collections.OrderedDict()
    for c in sorted(d["controls"], key=lambda r: r["y"]):
        if not c["v"]: continue
        g.setdefault(c["sec"], []).append(c)
    for s, cs in g.items():
        ys = cs[0]["y"]
        texts = []
        for c in cs:
            a = c["attrs"]; da = " ".join(f"{k}={v}" for k, v in a.items() if k.startswith("data-"))[:60]
            texts.append((c["text"][:22] or a.get("id", "") or a.get("class", "")[:20]) + (f"[{da}]" if da else ""))
        print(f"SEC #{s} y{ys} n{len(cs)}: " + " | ".join(texts[:40]))
    print("console:", len(d["console"]), "failed:", len(d["failed"]), "bad:", len(d["bad_status"]))
