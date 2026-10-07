# -*- coding: utf-8 -*-
"""Raw file check for the Sde Dov files (as rawcheck.py for Rova 4): the set of numbers in the whole Hebrew JSON file equals
the set in each language file, every key and value included (sources, src, notes, coordinates, ui). The metadata keys
(sources/src/note/...) are copied unchanged, so they are read with the Hebrew separators; month names are read as numbers
(check_i18n_sde_dov.nums)."""
import io
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from check_i18n_sde_dov import nums, PG, AM  # noqa: E402

META = {"sources", "src", "note", "tax_src", "gap_src", "research", "page", "updated"}


def allnums(fn, lang):
    d = json.load(io.open(fn, encoding="utf-8"))
    out = set()

    def walk(x, meta=False):
        if isinstance(x, dict):
            for k, v in x.items():
                walk(k, meta)
                walk(v, meta or k in META)
        elif isinstance(x, list):
            for v in x:
                walk(v, meta)
        elif isinstance(x, str):
            out.update(nums(x, "he" if meta else lang))
        elif isinstance(x, (int, float)) and not isinstance(x, bool):
            out.add(repr(x))
    walk(d)
    return out


res = {}
for comp, folder, base in (("price_guide", PG, "sde-dov-prices"), ("area_map", AM, "sde-dov")):
    he = allnums(os.path.join(folder, base + ".json"), "he")
    for lang in ("en", "fr", "ru", "ar"):
        tr = allnums(os.path.join(folder, "%s.%s.json" % (base, lang)), lang)
        res["%s %s" % (comp, lang)] = {"he_distinct": len(he), "tr_distinct": len(tr), "only_he": sorted(he - tr), "only_tr": sorted(tr - he)}
print(json.dumps(res, indent=1))
