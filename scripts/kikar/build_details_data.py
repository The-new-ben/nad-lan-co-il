# -*- coding: utf-8 -*-
"""HAD-712 (Ben 11.11.2026 night): "נוף עם פירוט" / "View with details": the names of the places a window looks at, drawn over the
rendered view itself. This writes the small data file the showroom reads for it (the big world.json and places.json stay with the
old 3D stage): plugins/nadlan-config/assets/project-stage/hamedina/details.json.

  cam:    the render camera of the window views (scripts/interior/kikar_interior.py shot "view": hfov 70, pitch -4; the eye 1.6 m over the
          floor, floor f at (f-1)*4 m: the same formula as showroom.js eyeH, and views.json's "world eye" lines agree)
  towers: each tower's centre in the world frame (x metres east, z metres south of the plot centre; Blender y = -z)
  marks:  the named landmarks of world.json (the old stage's window view), with he/en names and the French of world-i18n.json
  places: a few nearby stations, parks, malls and culture places from places.json that have walking minutes and an English name
Every name is the data's own; nothing is invented. Run after world.json, places.json or world-i18n.json change.
  python scripts/kikar/build_details_data.py"""
import json, os, sys
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.dirname(os.path.dirname(HERE))
D = os.path.join(REPO, "plugins", "nadlan-config", "assets", "project-stage", "hamedina")
W = json.load(open(os.path.join(D, "world.json"), encoding="utf-8"))
P = json.load(open(os.path.join(D, "places.json"), encoding="utf-8"))
FR = json.load(open(os.path.join(D, "world-i18n.json"), encoding="utf-8"))["fr"]

towers = {t["key"]: {"cx": round(t["cx"], 1), "cz": round(t["cz"], 1), "floors": t["floors"]} for t in W["towers"]}
marks = []
for m in W["marks"]:
    if m.get("key") == "sea":  # the sea is the horizon itself, not a point: the page says it in words
        continue
    marks.append({"key": m["key"], "he": m["he"], "en": m["en"], "fr": FR.get(m["en"], m["en"]), "x": m["x"], "z": m["z"], "h": m.get("h")})
LINE_FR = {"Purple": "violette", "Red": "rouge", "Green": "verte"}


def fr_name(en):  # "Ibn Gabirol station, Purple Line" -> "Station Ibn Gabirol, ligne violette"; else world-i18n's French, else the name
    if en in FR:
        return FR[en]
    if en.endswith(" Line") and " station, " in en:
        st, line = en[:-5].split(" station, ")
        if line in LINE_FR:
            return "Station %s, ligne %s" % (st, LINE_FR[line])
    return en


KEEP = {"station": 3, "tram_stop": 2, "park": 2, "mall": 2, "culture": 2}
places, seen, n = [], set(), {}
for p in sorted(P["places"], key=lambda p: p["dist"]):
    k = p.get("k")
    en = (p.get("names") or {}).get("en") or ""
    if k not in KEEP or not en or not p.get("walk") or not (250 <= p["dist"] <= 1600) or p.get("generic"):
        continue
    if en in seen or n.get(k, 0) >= KEEP[k]:
        continue
    if any(en in m["en"] or m["en"] in en for m in marks):  # e.g. Savidor is a landmark already
        continue
    seen.add(en); n[k] = n.get(k, 0) + 1
    places.append({"k": k, "he": p["name"], "en": en, "fr": fr_name(en), "x": p["x"], "z": p["z"], "walk": p["walk"]})
out = {"v": 1, "src": "world.json marks, places.json, world-i18n.json (HAD-712)", "cam": {"hfov": 70, "pitch": -4, "eye0": 1.6, "storey": 4},
       "towers": towers, "marks": marks, "places": places}
json.dump(out, open(os.path.join(D, "details.json"), "w", encoding="utf-8"), ensure_ascii=False, separators=(",", ":"))
print("details.json: %d towers, %d marks, %d places" % (len(towers), len(marks), len(places)))
for x in marks + places:
    print("  ", x.get("k", "mark"), "|", x["he"], "|", x["en"], "|", x["fr"], "| walk", x.get("walk"))
