# -*- coding: utf-8 -*-
"""Fold the Codex language fixes into group_texts.py, restore French/Russian non-breaking spaces, refuse any fact drift."""
import io, json, re, os, sys
sys.stdout.reconfigure(encoding="utf-8")
H = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, H)
import group_texts as G
NB = "\u00a0"
KEY = {"group-C-family.txt": "C", "group-D-listing.txt": "D", "group-E-question.txt": "E"}
FACTS = ["3131540", "+972 52-363-1582", "197", "76", "11", "12", "18"]


def nbsp(t, l):
    t = t.replace(NB, " ")
    t = re.sub(r"18 000 000 ₪", "18" + NB + "000" + NB + "000" + NB + "₪", t)
    t = re.sub(r"(\d) (m²|м²)", r"\1" + NB + r"\2", t)
    if l == "fr":
        t = re.sub(r" ([:?!;])", NB + r"\1", t).replace("n° ", "n°" + NB)
    if l == "ru":
        t = t.replace("№ ", "№" + NB)
    return t


fixed = 0
for line in io.open(os.path.join(H, "review_out.txt"), encoding="utf-8"):
    line = line.strip().rstrip(",")
    if not line.startswith("{"):
        continue
    d = json.loads(line)
    if not d["fixed"]:
        continue
    l, f = d["file"].split("/")
    k = KEY[f]; old = getattr(G, k)[l]; new = nbsp(d["fixed"], l) if l in ("fr", "ru") else d["fixed"]
    for x in FACTS:  # every fact token keeps its count
        assert old.count(x) == new.count(x), (d["file"], x)
    getattr(G, k)[l] = new; fixed += 1
src = io.open(os.path.join(H, "group_texts.py"), encoding="utf-8").read().split("\nC = {")[0]
body = "".join("\n%s = %s\n" % (k, json.dumps(getattr(G, k), ensure_ascii=False, indent=1)) for k in ("C", "D", "E"))
io.open(os.path.join(H, "group_texts.py"), "w", encoding="utf-8").write(
    src.replace('NB = "\\u00a0"\n', 'NB = "\\u00a0"\n# language edit by Codex (GPT) 30.10.2026 folded in; NBSP kept as \\u00a0\n') + body)
print("fixed", fixed)
