# -*- coding: utf-8 -*-
"""Kikar Hamedina, P2 step 4 (HAD-375, 1.10.2026): the places' names in other languages, from OpenStreetMap only.

  python docs/research/2026-09-30-kikar-hamedina/names_osm_kikar.py [--fetch]

Order of the chain: build_places.py kikar -> enrich_places_kikar.py -> THIS -> build_world_hamedina.py (which copies the
research registry to assets/). This step writes BOTH copies (docs/research/.../places.json and
plugins/nadlan-config/assets/project-stage/hamedina/places.json) with the same bytes, so the world build's copy stays a no-op.

Why: on the en/fr/ru/ar pages the area map (arealife/areamap.js nameOf: names[LANG] || names.en || a name without Hebrew
letters || the kind) shows a place whose name exists only in Hebrew by its kind ("School", "Café"). OpenStreetMap often
carries the real name in other languages (name:en, name:ar, name:ru, name:fr). Nothing is translated, transliterated or
invented here: a value is written only when it is the tag of the one OSM feature that carries the same Hebrew name within
80 m.

Method
  1. Overpass (names-osm/overpass.json, the raw answer; --fetch asks again, otherwise the saved answer is reused, so the
     output is reproducible offline): every node, way and relation in the places' bbox (+0.001 deg) with at least one of
     name:en/ar/ru/fr AND a `name` or a `name:he`; `out tags center`. "Hebrew" is checked here, not in Overpass (a
     Hebrew-letter `name` or any `name:he`), so no regex engine question can drop a feature.
  2. Targets: every non-generic place whose name has Hebrew letters and that has no names.en.
  3. A match needs ALL of: the Hebrew name identical to the feature's `name` or `name:he` after normalising whitespace,
     geresh/gershayim variants and hyphens (norm() below); the distance <= 80 m (the feature's node or its centre); exactly
     one such feature. Two or more features -> the place is skipped and listed (ambiguous).
  4. Each value must be in its language's script (ar: Arabic letters, ru: Cyrillic, en/fr: Latin) and carry no Hebrew
     letters and no letters of the other scripts; a value that fails is dropped and listed.
  5. Only the missing languages are written into "names" (never an existing value); a new "names" object goes right before
     "sight" (where the builders' twin merge leaves it), languages in the builders' order en, ru, fr, ar. Every other byte
     of the file stays as it was: names-osm/diff_check.py proves it.
Evidence: names-osm/ (overpass.json, overpass-query.overpassql, fetch-meta.json, matches.csv, README.md, diff_check.py).
OSM data (c) OpenStreetMap contributors, ODbL.
"""
import csv, hashlib, io, json, math, os, re, sys, time, unicodedata, urllib.parse, urllib.request

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))
RES_FILE = os.path.join(HERE, "places.json")
ASSET_FILE = os.path.join(REPO, "plugins", "nadlan-config", "assets", "project-stage", "hamedina", "places.json")
EV = os.path.join(HERE, "names-osm")
RAW = os.path.join(EV, "overpass.json")
QFILE = os.path.join(EV, "overpass-query.overpassql")
META = os.path.join(EV, "fetch-meta.json")
CSV_OUT = os.path.join(EV, "matches.csv")
UA = {"User-Agent": "nadlan-config/2.0 (nad-lan.co.il)"}
ENDPOINTS = ["https://overpass-api.de/api/interpreter", "https://overpass.kumi.systems/api/interpreter",
             "https://overpass.private.coffee/api/interpreter"]
MAX_M = 80.0
MARGIN = 0.001
LANGS = ("en", "ru", "fr", "ar")          # the builders' order (build_places.py)

HE_ANY = re.compile("[֐-׿]")    # areamap.js hasHe()
SCRIPT = {
    "latin": re.compile("[A-Za-zÀ-ÖØ-öø-ɏḀ-ỿ]"),
    "cyrillic": re.compile("[Ѐ-ԯ]"),
    "arabic": re.compile("[؀-ۿݐ-ݿࢠ-ࣿﭐ-﷿ﹰ-﻿]"),
    "hebrew": HE_ANY,
}
WANT = {"en": "latin", "fr": "latin", "ru": "cyrillic", "ar": "arabic"}


def lang_ok(lang, v):
    """(ok, reason): the value carries letters of its language's script and none of the other three scripts"""
    want = WANT[lang]
    if not SCRIPT[want].search(v):
        return False, "no %s letters" % want
    bad = [s for s in SCRIPT if s != want and SCRIPT[s].search(v)]
    if bad:
        return False, "contains %s letters" % "+".join(bad)
    return True, ""


def norm(s):
    s = unicodedata.normalize("NFC", s or "")
    s = re.sub("[‎‏‪-‮⁦-⁩­]", "", s)       # direction marks, soft hyphen
    s = re.sub("[׳'’‘`´ʼ]", "'", s)                    # geresh variants
    s = s.replace("''", '"')                                                     # gershayim written as two gereshes
    s = re.sub("[״\"“”„]", '"', s)                           # gershayim variants
    s = re.sub("[\\-‐‑‒–—―־]", "-", s)        # hyphens, dashes, maqaf
    s = re.sub(r"\s*-\s*", "-", s)
    return re.sub(r"\s+", " ", s).strip()


def meters(la1, ln1, la2, ln2):
    r = 6371008.8
    p1, p2 = math.radians(la1), math.radians(la2)
    dp, dl = p2 - p1, math.radians(ln2 - ln1)
    a = math.sin(dp / 2) ** 2 + math.cos(p1) * math.cos(p2) * math.sin(dl / 2) ** 2
    return 2 * r * math.asin(math.sqrt(a))


def query_text(bbox):
    s, w, n, e = bbox
    return ("[out:json][timeout:120][bbox:%.6f,%.6f,%.6f,%.6f];\n"
            "(\n  nwr[\"name:en\"];\n  nwr[\"name:ar\"];\n  nwr[\"name:ru\"];\n  nwr[\"name:fr\"];\n)->.other;\n"
            "(\n  nwr.other[\"name\"];\n  nwr.other[\"name:he\"];\n);\n"
            "out tags center;\n") % (s, w, n, e)


def fetch(q):
    for ep in ENDPOINTS:
        for attempt in range(2):
            try:
                req = urllib.request.Request(ep, data=urllib.parse.urlencode({"data": q}).encode(), headers=UA)
                raw = urllib.request.urlopen(req, timeout=180).read()
                d = json.loads(raw.decode("utf-8"))
                if isinstance(d, dict) and d.get("elements") is not None and not d.get("remark", "").lower().startswith("runtime error"):
                    print("overpass", ep, "elements", len(d["elements"]), "bytes", len(raw))
                    return ep, raw
                print("overpass", ep, "unusable answer:", str(d.get("remark"))[:120])
            except Exception as ex:
                print("overpass", ep, "failed:", str(ex)[:120])
            time.sleep(5 + 10 * attempt)
    return None, None


def features(d):
    out = []
    for e in d["elements"]:
        t = e.get("tags") or {}
        la = e.get("lat", (e.get("center") or {}).get("lat"))
        ln = e.get("lon", (e.get("center") or {}).get("lon"))
        if la is None or ln is None:
            continue
        keys = set()
        if t.get("name") and HE_ANY.search(t["name"]):
            keys.add(norm(t["name"]))
        if t.get("name:he"):
            keys.add(norm(t["name:he"]))
        if not keys or not any(t.get("name:" + l) for l in LANGS):
            continue
        kind = next(("%s=%s" % (k, t[k]) for k in ("amenity", "shop", "leisure", "tourism", "healthcare", "office", "railway",
                                                  "public_transport", "highway", "building", "landuse", "place", "craft",
                                                  "historic", "man_made", "sport", "club") if t.get(k)), "")
        out.append({"ref": "%s/%s" % (e["type"], e["id"]), "lat": la, "lng": ln, "keys": keys, "tags": t, "kind": kind,
                    "street": street_or_area(t)})
    return out


def street_or_area(t):
    """a street / road / path (not a bus stop or platform) or a named area (place=*, landuse=*, boundary=*): its name is the
    street's or the neighbourhood's, which the city's layers sometimes give a place (a playground called by its street). A
    feature that is also a thing (a park that is a square, a sports ground with a landuse) is the thing, not an area."""
    if any(t.get(k) for k in THING):
        return False
    if t.get("highway") and t.get("highway") != "bus_stop":
        return True
    return bool(t.get("place") or t.get("landuse") or t.get("boundary"))


THING = ("amenity", "leisure", "shop", "tourism", "building", "healthcare", "office", "railway", "public_transport", "historic",
         "craft", "club", "sport", "man_made", "emergency")


def own_osm_ref(pid):
    m = re.match(r"^(?:osm:(node|way|relation)/(\d+)|fp:osm-(node|way|relation)-(\d+))", pid)
    if not m:
        return ""
    return "%s/%s" % (m.group(1) or m.group(3), m.group(2) or m.group(4))


def with_names(p, names):
    """the place with its "names" object: an existing one keeps its keys and values, the new languages follow; a new one goes
    right before "sight" (all places have it; append if not)"""
    if "names" in p:
        for l in LANGS:
            if l in names and l not in p["names"]:
                p["names"][l] = names[l]
        return p
    obj = {l: names[l] for l in LANGS if l in names}
    out = {}
    for k, v in p.items():
        if k == "sight":
            out["names"] = obj
        out[k] = v
    if "names" not in out:
        out["names"] = obj
    return out


def dumps(d):
    return json.dumps(d, ensure_ascii=False, separators=(",", ":")) + "\n"


def main():
    raw_res = io.open(RES_FILE, encoding="utf-8", newline="").read()
    raw_ast = io.open(ASSET_FILE, encoding="utf-8", newline="").read()
    if raw_res != raw_ast:
        sys.exit("the research registry and the assets copy differ: run build_world_hamedina.py (it copies) or resolve first")
    reg = json.loads(raw_res)
    if dumps(reg) != raw_res:
        sys.exit("places.json does not read back to its own bytes: a names-only rewrite could change more than the names")
    P = reg["places"]
    lats, lngs = [p["lat"] for p in P], [p["lng"] for p in P]
    bbox = (round(min(lats) - MARGIN, 6), round(min(lngs) - MARGIN, 6), round(max(lats) + MARGIN, 6), round(max(lngs) + MARGIN, 6))
    q = query_text(bbox)
    os.makedirs(EV, exist_ok=True)
    if "--fetch" in sys.argv or not os.path.exists(RAW):
        ep, body = fetch(q)
        if body is None:
            sys.exit("Overpass gave nothing (all endpoints)")
        io.open(RAW, "wb").write(body)
        io.open(QFILE, "w", encoding="utf-8", newline="\n").write(q)
        meta = {"endpoint": ep, "fetched_at": time.strftime("%Y-%m-%dT%H:%M:%S%z"), "user_agent": UA["User-Agent"], "bbox_swne": bbox,
                "bytes": len(body), "sha256": hashlib.sha256(body).hexdigest(),
                "osm_base": (json.loads(body.decode("utf-8")).get("osm3s") or {}).get("timestamp_osm_base")}
        io.open(META, "w", encoding="utf-8", newline="\n").write(json.dumps(meta, ensure_ascii=False, indent=1) + "\n")
    else:
        saved_q = io.open(QFILE, encoding="utf-8").read() if os.path.exists(QFILE) else None
        if saved_q is not None and saved_q != q:
            sys.exit("the saved Overpass answer was asked for another bbox: run with --fetch")
        print("overpass: the saved answer", RAW)
    d = json.load(io.open(RAW, encoding="utf-8"))
    F = features(d)
    print("OSM features with a Hebrew name and another language:", len(F), "of", len(d["elements"]), "elements;",
          "osm_base", (d.get("osm3s") or {}).get("timestamp_osm_base"))
    if "--no-streets" in sys.argv:        # the stricter reading: a street's or a neighbourhood's name never names a place
        F = [f for f in F if not f["street"]]
        print("--no-streets: streets and named areas left out,", len(F), "features")

    rows, stats = [], {l: 0 for l in LANGS}
    stats.update({"targets": 0, "targets_w10": 0, "matched": 0, "matched_nothing_new": 0, "ambiguous": 0, "no_match": 0, "dropped": 0,
                  "places_changed": 0, "places_changed_w10": 0, "kept_existing_conflict": 0})
    for i, p in enumerate(P):
        if p.get("generic") or not HE_ANY.search(p["name"]) or (p.get("names") or {}).get("en"):
            continue
        stats["targets"] += 1
        w10 = p.get("walk") is not None and p["walk"] <= 10
        stats["targets_w10"] += w10
        key = norm(p["name"])
        cands = []
        for f in F:
            if key in f["keys"]:
                m = meters(p["lat"], p["lng"], f["lat"], f["lng"])
                if m <= MAX_M:
                    cands.append((m, f))
        cands.sort(key=lambda c: c[0])
        row = {"idx": i, "id": p["id"], "name_he": p["name"], "g": p["g"], "k": p["k"], "walk_min": p.get("walk"),
               "own_osm_ref": own_osm_ref(p["id"]), "status": "", "osm_ref": "", "osm_kind": "", "street_or_area": "",
               "osm_name": "", "osm_name_he": "", "dist_m": "", "same_osm_id": "", "candidates": "",
               "en": "", "ru": "", "fr": "", "ar": "", "written": "", "dropped": "", "kept_existing": "", "near_miss": ""}
        if not cands:
            stats["no_match"] += 1
            row["status"] = "no-match"
            # for the record only (never written): the same name farther than 80 m, or a name that contains / is contained
            # in ours within 80 m (the rules need identity; these show what the rules leave out)
            far = min((meters(p["lat"], p["lng"], f["lat"], f["lng"]), f) for f in F if key in f["keys"]) if any(key in f["keys"] for f in F) else None
            if far:
                row["near_miss"] = "same name at %.0f m: %s %s" % (far[0], far[1]["ref"], far[1]["tags"].get("name:en", ""))
                stats["nm_same_name_farther"] = stats.get("nm_same_name_farther", 0) + 1
            else:
                part = [(meters(p["lat"], p["lng"], f["lat"], f["lng"]), f) for f in F
                        if len(key) >= 3 and any(len(k) >= 3 and (k in key or key in k) for k in f["keys"])]
                part = sorted([c for c in part if c[0] <= MAX_M], key=lambda c: c[0])
                if part:
                    row["near_miss"] = "similar name within 80 m: %s (%s) %.0f m %s" % (
                        part[0][1]["ref"], part[0][1]["tags"].get("name:he") or part[0][1]["tags"].get("name", ""), part[0][0],
                        part[0][1]["tags"].get("name:en", ""))
                    stats["nm_similar_within_80"] = stats.get("nm_similar_within_80", 0) + 1
            rows.append(row)
            continue
        if len(cands) > 1:
            stats["ambiguous"] += 1
            row["status"] = "ambiguous"
            # for the record only: do the candidates carry the same value in every language (two platforms of one stop)?
            agree = all(len({f["tags"].get("name:" + l) for _, f in cands if f["tags"].get("name:" + l)}) <= 1 for l in LANGS)
            row["near_miss"] = "candidates carry no conflicting value" if agree else "candidates conflict"
            stats["ambiguous_no_conflicting_value"] = stats.get("ambiguous_no_conflicting_value", 0) + agree
            row["candidates"] = " | ".join("%s %.1fm %s en=%s ar=%s ru=%s fr=%s" % (
                f["ref"], m, f["kind"], f["tags"].get("name:en", ""), f["tags"].get("name:ar", ""), f["tags"].get("name:ru", ""),
                f["tags"].get("name:fr", "")) for m, f in cands)
            rows.append(row)
            continue
        m, f = cands[0]
        t = f["tags"]
        row.update({"status": "matched", "osm_ref": f["ref"], "osm_kind": f["kind"], "street_or_area": "yes" if f["street"] else "",
                    "osm_name": t.get("name", ""),
                    "osm_name_he": t.get("name:he", ""), "dist_m": "%.1f" % m,
                    "same_osm_id": ("yes" if row["own_osm_ref"] == f["ref"] else "no") if row["own_osm_ref"] else ""})
        stats["matched"] += 1
        good, dropped, kept = {}, [], []
        have = p.get("names") or {}
        for l in LANGS:
            v = (t.get("name:" + l) or "").strip()
            if not v:
                continue
            row[l] = v
            ok, why = lang_ok(l, v)
            if not ok:
                dropped.append("%s=%s (%s)" % (l, v, why))
                continue
            if l in have:
                if have[l] != v:
                    kept.append("%s: kept %s, OSM %s" % (l, have[l], v))
                continue
            good[l] = v
        stats["dropped"] += len(dropped)
        stats["kept_existing_conflict"] += len(kept)
        row["dropped"] = "; ".join(dropped)
        row["kept_existing"] = "; ".join(kept)
        if not good:
            stats["matched_nothing_new"] += 1
            row["status"] = "matched-nothing-new"
            rows.append(row)
            continue
        row["written"] = ",".join(l for l in LANGS if l in good)
        for l in good:
            stats[l] += 1
        stats["places_changed"] += 1
        stats["places_changed_w10"] += w10
        P[i] = with_names(p, good)
        rows.append(row)

    left_w10 = sum(1 for p in P if not p.get("generic") and HE_ANY.search(p["name"]) and not (p.get("names") or {}).get("en")
                   and p.get("walk") is not None and p["walk"] <= 10)
    # what a language page shows now: a place still shown by its kind = no names[lang], no names.en, a Hebrew name
    def kind_shown(lang, w10_only):
        return sum(1 for p in P if not p.get("generic") and HE_ANY.search(p["name"]) and not (p.get("names") or {}).get(lang)
                   and not (p.get("names") or {}).get("en") and (not w10_only or (p.get("walk") is not None and p["walk"] <= 10)))
    stats["left_no_en_w10"] = left_w10
    stats["changed_from_street_or_area"] = sum(1 for r in rows if r["written"] and r["street_or_area"])
    stats["changed_same_osm_id"] = sum(1 for r in rows if r["written"] and r["same_osm_id"] == "yes")
    from collections import Counter
    stats["osm_features_serving_2plus_places"] = {k: v for k, v in Counter(r["osm_ref"] for r in rows if r["written"]).items() if v > 1}
    stats["shown_by_kind_w10"] = {l: kind_shown(l, True) for l in LANGS}
    stats["shown_by_kind_all"] = {l: kind_shown(l, False) for l in LANGS}

    out = dumps(reg)
    for path in (RES_FILE, ASSET_FILE):
        io.open(path, "w", encoding="utf-8", newline="\n").write(out)
    with io.open(CSV_OUT, "w", encoding="utf-8-sig", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0].keys()) if rows else ["idx"])
        w.writeheader()
        order = {"matched": 0, "matched-nothing-new": 1, "ambiguous": 2, "no-match": 3}
        for r in sorted(rows, key=lambda r: (order[r["status"]], r["walk_min"] if r["walk_min"] is not None else 99, r["idx"])):
            w.writerow(r)
    io.open(os.path.join(EV, "stats.json"), "w", encoding="utf-8", newline="\n").write(json.dumps(stats, ensure_ascii=False, indent=1) + "\n")
    print(json.dumps(stats, ensure_ascii=False))
    print("md5", hashlib.md5(out.encode("utf-8")).hexdigest(), "bytes", len(out.encode("utf-8")))


if __name__ == "__main__":
    main()
