# -*- coding: utf-8 -*-
"""The design-system component GreecePriceMap (DS artifact L9Nqz7Viv7K3MYeZrBc9s8): README + a static preview drawn from the real data
(greece-map.json + greece-prices.json). Writes into the scratchpad DS folder; publish with the Artifact tool.
  python docs/research/2026-10-22-greece-prices/ds_component.py"""
import io, json, os
REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
D = r"C:\Users\777\AppData\Local\Temp\claude\C--Users-777-nad-lan\f8200c1d-6798-4a3e-8a9f-7b12503e42b2\scratchpad\ds\project\components\GreecePriceMap"
os.makedirs(D, exist_ok=True)
A = os.path.join(REPO, "plugins", "nadlan-config", "assets", "instruments", "data")
M = json.load(io.open(os.path.join(A, "greece-map.json"), encoding="utf-8"))
G = json.load(io.open(os.path.join(A, "greece-prices.json"), encoding="utf-8"))
pr = M["proj"]
X = lambda lng: (lng - pr["lon0"]) * pr["cos"] * pr["k"]
Y = lambda lat: (pr["lat1"] - lat) * pr["k"]
CUTS = [2000, 2600, 3200, 4200]
COL = ["#9CC3D1", "#4E93AC", "#2F6F86", "#1F4B5C", "#C42550"]
band = lambda v: next((i for i, c in enumerate(CUTS) if v <= c), 4)
dots = "".join('<circle cx="{:.1f}" cy="{:.1f}" r="6" fill="{}" stroke="#fff" stroke-width="1.4"/>'.format(X(p["lng"]), Y(p["lat"]), COL[band(p["m2"])])
               for p in sorted(G["places"], key=lambda p: p["m2"]) if p["z"] == "map")
labels = "".join('<text x="{:.1f}" y="{:.1f}" class="lb">{}</text>'.format(X(p["lng"]) + 9, Y(p["lat"]) + 4, p["lb"]) for p in G["places"] if p.get("lb"))
myk = [p for p in G["places"] if p["id"] == "mykonos"][0]
legend = "".join('<span><i style="background:{}"></i>{}</span>'.format(c, t) for c, t in zip(COL, ["עד €2,000", "€2,000 עד €2,600", "€2,600 עד €3,200", "€3,200 עד €4,200", "מעל €4,200"]))
TPL = io.open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "ds_preview_template.html"), encoding="utf-8").read()
html = (TPL.replace("{{VB}}", "0 0 {} {}".format(*M["vb"])).replace("{{NB}}", M["nb"]).replace("{{GR}}", M["gr"]).replace("{{DOTS}}", dots).replace("{{LABELS}}", labels)
        .replace("{{LEGEND}}", legend).replace("{{PER}}", myk["per"]).replace("{{SRC}}", myk["src"]).replace("{{M2}}", "{:,}".format(myk["m2"]))
        .replace("{{APT}}", "{:,}".format(myk["m2"] * 70)).replace("{{YOY}}", "{:+.1f}%".format(100 * (myk.get("yoy") or 0))))
io.open(os.path.join(D, "preview.html"), "w", encoding="utf-8").write(html)
print("preview", len(html.encode()), "bytes")
