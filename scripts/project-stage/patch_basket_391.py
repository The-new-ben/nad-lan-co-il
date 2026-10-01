# -*- coding: utf-8 -*-
"""1.72.391 (V4, the first parity step; HAD-380): the basket names the apartment a world page picked. A page whose stage has no
direction sectors (the shared 3D world: Kikar Hamedina) sends the apartment's own words in nl:facing ({label}); the basket keeps
them and shows "קומה 30 · דירה פינתית צפון-מערבית · מערבה". The fleet's stages send no label, so nothing changes for them.
  python patch_basket_391.py"""
import io, os, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
P = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "plugins", "nadlan-config", "assets", "basket", "basket.js")
s = open(P, encoding="utf-8").read()
if "1.72.391" in s:
    raise SystemExit("already patched")
for a, b in (
    ("  const unitLine = (u) => u ? ('קומה ' + u.floor + (u.bearing != null && words(u.bearing) ? ' · ' + words(u.bearing) : '')) : '';",
     "  // 1.72.391: a world page's own words for the apartment (its label) come before the sectors' direction words\n"
     "  const unitLine = (u) => u ? ('קומה ' + u.floor + (u.label ? ' · ' + u.label : (u.bearing != null && words(u.bearing) ? ' · ' + words(u.bearing) : ''))) : '';"),
    ("    S.unit = { floor: Number(d.floor), bearing: d.bearing != null ? Math.round(Number(d.bearing)) : null, unit: d.unit || null };",
     "    S.unit = { floor: Number(d.floor), bearing: d.bearing != null ? Math.round(Number(d.bearing)) : null, unit: d.unit || null, label: d.label ? String(d.label).slice(0, 60) : null };"),
):
    if s.count(a) != 1:
        raise SystemExit(f"anchor x{s.count(a)}: {a[:70]}")
    s = s.replace(a, b)
open(P, "w", encoding="utf-8", newline="\n").write(s)
print("basket.js patched (1.72.391)")
