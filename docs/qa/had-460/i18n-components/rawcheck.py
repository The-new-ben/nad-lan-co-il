# -*- coding: utf-8 -*-
"""Raw file check (metadata keys sources/src/note/... read with the Hebrew separators, since they are copied unchanged): the set of numbers (digit runs, locale separators normalised) in the whole Hebrew JSON file equals the
set in each language file, every key and value included (sources, src, notes, coordinates, ui)."""
import io, json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from check_i18n import nums, PG, AM
def allnums(fn, lang):
    d = json.load(io.open(fn, encoding="utf-8"))
    out = set()
    META = {"sources", "src", "note", "tax_src", "gap_src", "research", "page", "updated"}
    def walk(x, meta=False):
        if isinstance(x, dict):
            for k, v in x.items():
                walk(k, meta); walk(v, meta or k in META)
        elif isinstance(x, list):
            for v in x: walk(v, meta)
        elif isinstance(x, str):
            # the English/ISO metadata (sources, src, notes) is copied unchanged, so it is read with the Hebrew separators
            out.update(nums(x, "he" if meta else lang))
        elif isinstance(x, (int, float)) and not isinstance(x, bool):
            out.add(repr(x))
    walk(d)
    return out
res = {}
for comp, folder in (("price_guide", PG), ("area_map", AM)):
    he = allnums(os.path.join(folder, "rova-4.json"), "he")
    for lang in ("en", "fr", "ru", "ar"):
        tr = allnums(os.path.join(folder, "rova-4.%s.json" % lang), lang)
        res["%s %s" % (comp, lang)] = {"he_distinct": len(he), "tr_distinct": len(tr), "only_he": sorted(he - tr), "only_tr": sorted(tr - he)}
print(json.dumps(res, indent=1))
