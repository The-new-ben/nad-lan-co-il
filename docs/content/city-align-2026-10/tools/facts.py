# -*- coding: utf-8 -*-
"""Print the official fact sheet of a city JSON (the only numbers allowed in new text), with source keys = JSON paths."""
import json, os, sys
CITIES = r"C:\Users\777\nad-lan\nad-lan-co-il\scripts\project-stage\price_guide\cities"
QHE = {"1-3": "הרבעון הראשון", "4-6": "הרבעון השני", "7-9": "הרבעון השלישי", "10-12": "הרבעון הרביעי"}
QMON = {"1-3": "ינואר-מרץ", "4-6": "אפריל-יוני", "7-9": "יולי-ספטמבר", "10-12": "אוקטובר-דצמבר"}

def qhe(q):
    a, y = q.split(".")
    return f"{QHE[a]} של {y}"

def m(v):
    return "-" if v is None else f"{v:,}"

def mil(v):
    return "-" if v is None else (f"{v/1e6:.2f}".rstrip("0").rstrip(".") + " מיליון")

def load(slug):
    return json.load(open(os.path.join(CITIES, slug + ".json"), encoding="utf-8"))

if __name__ == "__main__":
    slug = sys.argv[1]
    d = load(slug)
    print(f"# {slug} | {d['city_he']} | data_quarter {d['data_quarter']} ({qhe(d['data_quarter'])}) | file {d.get('file_date_he')} | updated {d.get('updated_he')}")
    print("answer:", d["answer"])
    for k in ("3", "4", "5", "all"):
        r = d["rooms"][k]
        ser = ", ".join(f"{q}:{m(v)}" for q, v in r["quarters"])
        print(f"rooms.{k}.latest = {m(r['latest'])} ({mil(r['latest'])}) quarter {r['quarter']} = {qhe(r['quarter'])} | year_ago {m(r.get('year_ago'))} | change_pct {r.get('change_pct')}%")
        print(f"   rooms.{k}.quarters: {ser}")
    il = d.get("israel", {})
    print(f"israel ({il.get('quarter')}): 3={m(il.get('3'))} 4={m(il.get('4'))} 5={m(il.get('5'))} all={m(il.get('all'))}")
    if d.get("israel_latest"):
        il = d["israel_latest"]
        print(f"israel_latest ({il.get('quarter')}): 3={m(il.get('3'))} 4={m(il.get('4'))} 5={m(il.get('5'))} all={m(il.get('all'))}")
    for n in d.get("neighbourhoods") or []:
        r = n["rooms"]
        print(f"neighbourhoods[{n['name']}] ({n['quarter']}): 3={m(r.get('3'))} 4={m(r.get('4'))} 5={m(r.get('5'))}")
    if d.get("cities"):
        for c in d["cities"]:
            rr = c["rooms"]
            print(f"cities[{c['slug']}] {c['city_he']}: " + " | ".join(f"{k}={m(rr[k]['latest'])} ({rr[k]['quarter']}, {rr[k]['change_pct']}%)" for k in ("3", "4", "5", "all")))
    print("src_line:", d["src_line"])
