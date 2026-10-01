# -*- coding: utf-8 -*-
"""Kikar Hamedina, P2 step 5 (HAD-375, 1.10.2026): the places' names in other languages from Wikidata LABELS, reached only
through the `wikidata=Q...` tag of the place's own OpenStreetMap feature.

  python docs/research/2026-09-30-kikar-hamedina/names_wikidata_kikar.py [--fetch] [--dry]
  (--dry: compute everything and print the md5 the registry would have; write nothing)

Order of the chain: build_places.py kikar -> enrich_places_kikar.py -> names_osm_kikar.py -> THIS -> build_world_hamedina.py
(which copies the research registry to assets/ byte for byte). Like names_osm, this step writes BOTH copies
(docs/research/.../places.json and plugins/nadlan-config/assets/project-stage/hamedina/places.json) with the same bytes.

Why: names_osm reads only OSM's own name:xx tags. Many OSM features carry no name:xx tag but do carry `wikidata=Q...`, and the
Wikidata item has the real name in English, Arabic, French and Russian as its LABEL. Nothing is translated, transliterated
or invented here, and no description or alias is ever used: a value is the item's label in that language, or nothing.

Method
  0. Script audit of EVERY existing names value (coordinator's order, 1.10.2026): each value is run through names_osm's
     lang_ok(). A value with Hebrew letters inside names.en/ru/fr/ar plainly fails and is REMOVED (an emptied "names"
     object goes with it); any other failure (no letter of its own script, letters of another non-Hebrew script) is only
     listed. Both go to names-wikidata/script-audit.csv. Known cause: build_places.py copies an OSM `name` that has any
     Latin letter into names.en, so a mixed name such as "צמרת G" became an English name.
  1. Overpass (names-wikidata/overpass.json, the raw answer; --fetch asks again, otherwise the saved answer is reused):
     every node, way and relation in the places' bbox (the same bbox as names_osm) that has a `wikidata` tag OR one of
     name:en/ar/ru/fr, AND a `name` or a `name:he`; `out tags center`. This is a superset of names_osm's query, so a
     place's candidates (and its ambiguity) are counted over every feature either step can see.
  2. Targets: every non-generic place whose name has Hebrew letters and that still lacks at least one of names.en/ar/fr/ru.
  3. The place's OSM feature, under names_osm's strict rule (its functions are imported, not copied):
     (A) the place id carries an OSM element (osm:node/N, fp:osm-way-N ...) and that element is in the answer: it is the
         feature, and strict() must give rule (a) (NEVER still wins: a street, a parking lot, place/landuse/boundary or a
         bare building is refused even when it is the place's own element); otherwise
     (B) exactly one feature with the same Hebrew name (norm()) within 80 m, counted over ALL same-name features before the
         strict rule, and strict() must give rule (a) or (b). Zero -> no match; two or more -> ambiguous, skipped.
  4. The feature must carry a well-formed `wikidata=Q<digits>` tag. Labels are fetched with wbgetentities
     (props=labels|sitelinks, languages=en|ar|fr|ru|he, no language fallback), 50 ids per request; the raw answers are saved
     in names-wikidata/wikidata/ so a run without --fetch is reproducible offline. A redirected id is followed to its target.
  5. Identity guard: the item's Hebrew label or its hewiki sitelink title must equal the place's Hebrew name after norm().
     If the item has neither (no Hebrew label and no hewiki article), the OSM feature's own `name`/`name:he` must equal the
     place's name. Otherwise the place is skipped and listed (he-mismatch).
  6. Script check (names_osm.lang_ok): ar Arabic letters, ru Cyrillic, en/fr Latin, and no letters of the other scripts.
  7. Only missing languages are written (never an existing names.xx value); a different existing value is kept and listed.
     Each added value gets names_src[lang] = "wikidata:Q..." (names_src sits right after "names"; languages in the
     builders' order en, ru, fr, ar). Every other byte of the file stays as it was: names-wikidata/diff_check.py proves it.
Evidence: names-wikidata/ (overpass.json, overpass-query.overpassql, fetch-meta.json, wikidata/batch-NN.json,
wikidata/fetch-meta.json, matches.csv, stats.json, tlv-gis-check.json, README.md, diff_check.py).
OSM data (c) OpenStreetMap contributors, ODbL. Wikidata labels: CC0.
"""
import csv, hashlib, io, json, os, re, sys, time, urllib.parse, urllib.request
from collections import Counter, OrderedDict

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import names_osm_kikar as no      # noqa: E402  (also sets utf-8 stdout)

RES_FILE, ASSET_FILE, LANGS, MAX_M, MARGIN = no.RES_FILE, no.ASSET_FILE, no.LANGS, no.MAX_M, no.MARGIN
EV = os.path.join(HERE, "names-wikidata")
RAW = os.path.join(EV, "overpass.json")
QFILE = os.path.join(EV, "overpass-query.overpassql")
META = os.path.join(EV, "fetch-meta.json")
WD_DIR = os.path.join(EV, "wikidata")
WD_META = os.path.join(WD_DIR, "fetch-meta.json")
CSV_OUT = os.path.join(EV, "matches.csv")
AUDIT_OUT = os.path.join(EV, "script-audit.csv")
DRY = "--dry" in sys.argv
WD_API = "https://www.wikidata.org/w/api.php"
UA = {"User-Agent": "nadlan-config/2.0 (https://nad-lan.co.il; research, read-only)"}
QID = re.compile(r"^Q[1-9]\d*$")
KIND_KEYS = ("amenity", "shop", "leisure", "tourism", "healthcare", "office", "railway", "public_transport", "highway",
             "building", "landuse", "place", "craft", "historic", "man_made", "sport", "club")   # names_osm.features() order


def query_text(bbox):
    s, w, n, e = bbox
    return ("[out:json][timeout:120][bbox:%.6f,%.6f,%.6f,%.6f];\n"
            "(\n  nwr[\"wikidata\"];\n  nwr[\"name:en\"];\n  nwr[\"name:ar\"];\n  nwr[\"name:ru\"];\n  nwr[\"name:fr\"];\n)->.other;\n"
            "(\n  nwr.other[\"name\"];\n  nwr.other[\"name:he\"];\n);\n"
            "out tags center;\n") % (s, w, n, e)


def features(d):
    """names_osm.features() with one change: a feature is kept when it has a Hebrew key AND (a wikidata tag OR a name:xx)"""
    out = []
    for e in d["elements"]:
        t = e.get("tags") or {}
        la = e.get("lat", (e.get("center") or {}).get("lat"))
        ln = e.get("lon", (e.get("center") or {}).get("lon"))
        if la is None or ln is None:
            continue
        keys = set()
        if t.get("name") and no.HE_ANY.search(t["name"]):
            keys.add(no.norm(t["name"]))
        if t.get("name:he"):
            keys.add(no.norm(t["name:he"]))
        if not keys or not (t.get("wikidata") or any(t.get("name:" + l) for l in LANGS)):
            continue
        kind = next(("%s=%s" % (k, t[k]) for k in KIND_KEYS if t.get(k)), "")
        out.append({"ref": "%s/%s" % (e["type"], e["id"]), "lat": la, "lng": ln, "keys": keys, "tags": t, "kind": kind})
    return out


# ---------------------------------------------------------------- Wikidata
def wd_get(ids):
    url = WD_API + "?" + urllib.parse.urlencode({"action": "wbgetentities", "ids": "|".join(ids), "props": "labels|sitelinks",
                                                 "languages": "en|ar|fr|ru|he", "format": "json"})
    for attempt in range(4):
        try:
            raw = urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=60).read()
            d = json.loads(raw.decode("utf-8"))
            if "entities" in d:
                return url, raw
            print("wikidata unusable answer:", str(d.get("error"))[:160])
        except Exception as ex:
            print("wikidata failed:", str(ex)[:160])
        time.sleep(3 + 5 * attempt)
    return url, None


def wd_fetch(qids):
    os.makedirs(WD_DIR, exist_ok=True)
    for f in os.listdir(WD_DIR):
        if f.startswith("batch-") and f.endswith(".json"):
            os.remove(os.path.join(WD_DIR, f))
    meta = {"api": WD_API, "user_agent": UA["User-Agent"], "fetched_at": time.strftime("%Y-%m-%dT%H:%M:%S%z"),
            "ids": len(qids), "batches": []}
    for b in range(0, len(qids), 50):
        ids = qids[b:b + 50]
        url, raw = wd_get(ids)
        if raw is None:
            sys.exit("Wikidata gave nothing for batch %d" % (b // 50 + 1))
        name = "batch-%02d.json" % (b // 50 + 1)
        io.open(os.path.join(WD_DIR, name), "wb").write(raw)
        meta["batches"].append({"file": name, "url": url, "ids": ids, "bytes": len(raw), "sha256": hashlib.sha256(raw).hexdigest()})
        print("wikidata", name, len(ids), "ids", len(raw), "bytes")
        time.sleep(1)
    io.open(WD_META, "w", encoding="utf-8", newline="\n").write(json.dumps(meta, ensure_ascii=False, indent=1) + "\n")


def wd_load():
    """{requested id: entity} from the saved batches (a redirect is stored under the id we asked for)"""
    if not os.path.exists(WD_META):
        return {}, set()
    meta = json.load(io.open(WD_META, encoding="utf-8"))
    E, asked = {}, set()
    for b in meta["batches"]:
        d = json.load(io.open(os.path.join(WD_DIR, b["file"]), encoding="utf-8"))
        asked.update(b["ids"])
        for k, ent in d["entities"].items():
            E[k] = ent
            r = ent.get("redirects") or {}
            if r.get("from"):
                E[r["from"]] = ent
    return E, asked


def label(ent, lang):
    return (((ent.get("labels") or {}).get(lang) or {}).get("value") or "").strip()


def with_src(p, src):
    """names_src right after "names": an existing one keeps its keys, the new languages follow"""
    if "names_src" in p:
        for l in LANGS:
            if l in src and l not in p["names_src"]:
                p["names_src"][l] = src[l]
        return p
    out = {}
    for k, v in p.items():
        out[k] = v
        if k == "names":
            out["names_src"] = {l: src[l] for l in LANGS if l in src}
    return out


def script_audit(P):
    """every names value that fails lang_ok(); a Hebrew-letter value in names.en/ru/fr/ar is removed, the rest only listed"""
    out = []
    for i, p in enumerate(P):
        names = p.get("names") or {}
        for l, v in list(names.items()):
            ok, why = no.lang_ok(l, v) if l in no.WANT else (False, "not one of en/ru/fr/ar")
            if ok:
                continue
            plain = l in no.WANT and bool(no.HE_ANY.search(v))
            out.append(OrderedDict([("idx", i), ("id", p["id"]), ("name_he", p["name"]), ("g", p["g"]), ("lang", l), ("value", v),
                                    ("why", why), ("action", "removed" if plain else "listed only")]))
            if plain:
                del names[l]
                (p.get("names_src") or {}).pop(l, None)
        if "names" in p and not p["names"]:
            P[i] = {k: v for k, v in p.items() if k not in ("names", "names_src")}
        elif "names_src" in P[i] and not P[i]["names_src"]:
            P[i] = {k: v for k, v in P[i].items() if k != "names_src"}
    return out


def main():
    raw_res = io.open(RES_FILE, encoding="utf-8", newline="").read()
    raw_ast = io.open(ASSET_FILE, encoding="utf-8", newline="").read()
    if raw_res != raw_ast:
        sys.exit("the research registry and the assets copy differ: run build_world_hamedina.py (it copies) or resolve first")
    reg = json.loads(raw_res)
    if no.dumps(reg) != raw_res:
        sys.exit("places.json does not read back to its own bytes: a names-only rewrite could change more than the names")
    P = reg["places"]
    audit = script_audit(P)
    print("script audit: %d failing values, %d removed (Hebrew letters), %d listed only" % (
        len(audit), sum(a["action"] == "removed" for a in audit), sum(a["action"] != "removed" for a in audit)))
    lats, lngs = [p["lat"] for p in P], [p["lng"] for p in P]
    bbox = (round(min(lats) - MARGIN, 6), round(min(lngs) - MARGIN, 6), round(max(lats) + MARGIN, 6), round(max(lngs) + MARGIN, 6))
    q = query_text(bbox)
    os.makedirs(EV, exist_ok=True)
    fetching = "--fetch" in sys.argv or not os.path.exists(RAW)
    if fetching and DRY:
        sys.exit("--dry never fetches: run once without --dry first")
    if fetching:
        ep, body = no.fetch(q)
        if body is None:
            sys.exit("Overpass gave nothing (all endpoints)")
        io.open(RAW, "wb").write(body)
        io.open(QFILE, "w", encoding="utf-8", newline="\n").write(q)
        meta = {"endpoint": ep, "fetched_at": time.strftime("%Y-%m-%dT%H:%M:%S%z"), "user_agent": no.UA["User-Agent"],
                "bbox_swne": bbox, "bytes": len(body), "sha256": hashlib.sha256(body).hexdigest(),
                "osm_base": (json.loads(body.decode("utf-8")).get("osm3s") or {}).get("timestamp_osm_base")}
        io.open(META, "w", encoding="utf-8", newline="\n").write(json.dumps(meta, ensure_ascii=False, indent=1) + "\n")
    else:
        saved_q = io.open(QFILE, encoding="utf-8").read() if os.path.exists(QFILE) else None
        if saved_q is not None and saved_q != q:
            sys.exit("the saved Overpass answer was asked for another bbox: run with --fetch")
        print("overpass: the saved answer", RAW)
    d = json.load(io.open(RAW, encoding="utf-8"))
    F = features(d)
    byref = {f["ref"]: f for f in F}
    print("OSM features with a Hebrew name and (wikidata or name:xx):", len(F), "of", len(d["elements"]), "elements;",
          sum(1 for f in F if f["tags"].get("wikidata")), "with wikidata; osm_base", (d.get("osm3s") or {}).get("timestamp_osm_base"))

    # ---- pass 1: targets and their feature (no Wikidata needed yet)
    targets = []
    for i, p in enumerate(P):
        have = p.get("names") or {}
        miss = [l for l in LANGS if not have.get(l)]
        if p.get("generic") or not no.HE_ANY.search(p["name"]) or not miss:
            continue
        key = no.norm(p["name"])
        own = no.own_osm_ref(p["id"])
        row = OrderedDict([("idx", i), ("id", p["id"]), ("name_he", p["name"]), ("g", p["g"]), ("k", p["k"]),
                           ("walk_min", p.get("walk")), ("missing", ",".join(miss)), ("own_osm_ref", own), ("path", ""),
                           ("status", ""), ("osm_ref", ""), ("osm_kind", ""), ("rule", ""), ("strict", ""), ("dist_m", ""),
                           ("osm_name", ""), ("osm_name_he", ""), ("wikidata", ""), ("wd_he_label", ""), ("wd_hewiki", ""),
                           ("he_check", ""), ("wd_en", ""), ("wd_ru", ""), ("wd_fr", ""), ("wd_ar", ""), ("written", ""),
                           ("dropped", ""), ("kept_existing", ""), ("candidates", "")])
        f = None
        if own and own in byref:
            f = byref[own]
            row["path"] = "A own element"
            rule, why = no.strict(p, f, own)
        else:
            cands = sorted(((no.meters(p["lat"], p["lng"], g["lat"], g["lng"]), g) for g in F if key in g["keys"]), key=lambda c: c[0])
            cands = [c for c in cands if c[0] <= MAX_M]
            row["path"] = "B same name <= 80 m"
            if not cands:
                row["status"] = "no-match"
                targets.append((i, p, miss, row, None))
                continue
            if len(cands) > 1:
                row["status"] = "ambiguous"
                row["candidates"] = " | ".join("%s %.1fm %s wikidata=%s" % (g["ref"], m, g["kind"], g["tags"].get("wikidata", ""))
                                               for m, g in cands)
                targets.append((i, p, miss, row, None))
                continue
            f = cands[0][1]
            rule, why = no.strict(p, f, own)
        t = f["tags"]
        row.update({"osm_ref": f["ref"], "osm_kind": f["kind"], "rule": rule, "strict": why,
                    "dist_m": "%.1f" % no.meters(p["lat"], p["lng"], f["lat"], f["lng"]),
                    "osm_name": t.get("name", ""), "osm_name_he": t.get("name:he", ""), "wikidata": t.get("wikidata", "")})
        if not rule:
            row["status"] = "rejected-strict"
        elif not t.get("wikidata"):
            row["status"] = "no-wikidata-tag"
        elif not QID.match(t["wikidata"].strip()):
            row["status"] = "bad-wikidata-tag"
        else:
            row["wikidata"] = t["wikidata"].strip()
            row["status"] = "pending"
        targets.append((i, p, miss, row, f))

    need = sorted({r["wikidata"] for _, _, _, r, _ in targets if r["status"] == "pending"}, key=lambda s: int(s[1:]))
    if (fetching or not os.path.exists(WD_META)) and not DRY:
        wd_fetch(need)
    E, asked = wd_load()
    lost = [x for x in need if x not in asked]
    if lost:
        sys.exit("the saved Wikidata answers do not cover %s: run with --fetch" % ", ".join(lost[:10]))
    print("wikidata ids needed:", len(need), "| entities in the saved answers:", len(E))

    # ---- pass 2: identity guard, labels, script check, write only missing languages
    rows = []
    stats = OrderedDict()
    stats["script_audit"] = {"values_scanned": sum(len(p.get("names") or {}) for p in P) + sum(a["action"] == "removed" for a in audit),
                             "failing": len(audit), "removed": sum(a["action"] == "removed" for a in audit),
                             "listed_only": sum(a["action"] != "removed" for a in audit),
                             "list": ["%s %s %s=%s (%s; %s)" % (a["id"], a["name_he"], a["lang"], a["value"], a["why"], a["action"]) for a in audit]}
    stats["targets"] = len(targets)
    stats["targets_by_group"] = dict(Counter(p["g"] for _, p, _, _, _ in targets).most_common())
    stats["targets_missing_by_lang"] = {l: sum(1 for _, _, m, _, _ in targets if l in m) for l in LANGS}
    stats["targets_lacking_en"] = sum(1 for _, _, m, _, _ in targets if "en" in m)
    stats["targets_w10"] = sum(1 for _, p, _, _, _ in targets if p.get("walk") is not None and p["walk"] <= 10)
    filled_g = {}
    filled_lang = {l: 0 for l in LANGS}
    places_changed = places_changed_w10 = 0
    dropped_n = kept_n = 0
    qid_places = Counter()
    for i, p, miss, row, f in targets:
        if row["status"] != "pending":
            rows.append(row)
            continue
        qid = row["wikidata"]
        ent = E.get(qid)
        if not ent or "missing" in ent:
            row["status"] = "wikidata-missing"
            rows.append(row)
            continue
        if ent.get("id") and ent["id"] != qid:
            row["wikidata"] = qid = ent["id"]          # followed a redirect: the target's id is the source
        key = no.norm(p["name"])
        he_l = label(ent, "he")
        he_w = (((ent.get("sitelinks") or {}).get("hewiki") or {}).get("title") or "").strip()
        row["wd_he_label"], row["wd_hewiki"] = he_l, he_w
        for l in LANGS:
            row["wd_" + l] = label(ent, l)
        if he_l or he_w:
            ok = any(no.norm(x) == key for x in (he_l, he_w) if x)
            row["he_check"] = ("he label = name" if he_l and no.norm(he_l) == key else
                               "hewiki title = name" if ok else "he label/hewiki differ")
        else:
            ok = key in f["keys"]
            row["he_check"] = "no Hebrew on the item; OSM name = name" if ok else "no Hebrew on the item; OSM name differs"
        if not ok:
            row["status"] = "he-mismatch"
            rows.append(row)
            continue
        have = p.get("names") or {}
        good, src, dropped, kept = {}, {}, [], []
        for l in LANGS:
            v = label(ent, l)
            if not v:
                continue
            okl, why = no.lang_ok(l, v)
            if not okl:
                dropped.append("%s=%s (%s)" % (l, v, why))
                continue
            if have.get(l):
                if have[l] != v:
                    kept.append("%s: kept %s, Wikidata %s" % (l, have[l], v))
                continue
            good[l] = v
            src[l] = "wikidata:" + qid
        dropped_n += len(dropped)
        kept_n += len(kept)
        row["dropped"] = "; ".join(dropped)
        row["kept_existing"] = "; ".join(kept)
        if not good:
            row["status"] = "matched-nothing-new"
            rows.append(row)
            continue
        row["status"] = "filled"
        row["written"] = ",".join(l for l in LANGS if l in good)
        for l in good:
            filled_lang[l] += 1
            filled_g.setdefault(p["g"], {x: 0 for x in LANGS})[l] += 1
        places_changed += 1
        places_changed_w10 += p.get("walk") is not None and p["walk"] <= 10
        qid_places[qid] += 1
        P[i] = with_src(no.with_names(p, good), src)
        rows.append(row)

    st = Counter(r["status"] for r in rows)
    stats["outcome"] = dict(st.most_common())
    stats["path_A_own_element"] = sum(1 for r in rows if r["path"].startswith("A"))
    stats["places_filled"] = places_changed
    stats["places_filled_w10"] = places_changed_w10
    stats["values_filled_by_lang"] = filled_lang
    stats["values_filled"] = sum(filled_lang.values())
    stats["filled_by_group"] = filled_g
    stats["dropped_by_script_check"] = dropped_n
    stats["kept_existing_conflict"] = kept_n
    stats["skipped_by_reason"] = {k: v for k, v in st.items() if k not in ("filled",)}
    stats["features_with_wikidata_in_answer"] = sum(1 for f in F if f["tags"].get("wikidata"))
    stats["wikidata_ids_fetched"] = len(need)
    stats["wikidata_items_serving_2plus_places"] = {k: v for k, v in qid_places.items() if v > 1}
    stats["he_mismatch_list"] = ["%s %s -> %s %s (he=%s, hewiki=%s)" % (r["id"], r["name_he"], r["osm_ref"], r["wikidata"],
                                 r["wd_he_label"], r["wd_hewiki"]) for r in rows if r["status"] == "he-mismatch"]
    stats["rejected_strict_with_wikidata"] = ["%s %s -> %s %s (%s)" % (r["id"], r["name_he"], r["osm_ref"], r["wikidata"], r["strict"])
                                              for r in rows if r["status"] == "rejected-strict" and r["wikidata"]]

    def shown_by_kind(lang, w10_only):
        return sum(1 for p in P if not p.get("generic") and no.HE_ANY.search(p["name"]) and not (p.get("names") or {}).get(lang)
                   and not (p.get("names") or {}).get("en") and (not w10_only or (p.get("walk") is not None and p["walk"] <= 10)))
    stats["shown_by_kind_w10"] = {l: shown_by_kind(l, True) for l in LANGS}
    stats["shown_by_kind_all"] = {l: shown_by_kind(l, False) for l in LANGS}

    bad = [(p["id"], l, v) for p in P for l, v in (p.get("names") or {}).items() if not no.HE_ANY.search(v) and not no.lang_ok(l, v)[0]]
    hebrew_left = [(p["id"], l, v) for p in P for l, v in (p.get("names") or {}).items() if no.HE_ANY.search(v)]
    if hebrew_left:
        sys.exit("a names value with Hebrew letters is still there: %s" % hebrew_left[:5])
    out = no.dumps(reg)
    if DRY:
        print("--dry: nothing written; values failing the script check (listed only): %d" % len(bad))
        print("md5", hashlib.md5(out.encode("utf-8")).hexdigest(), "bytes", len(out.encode("utf-8")))
        return
    for path in (RES_FILE, ASSET_FILE):
        io.open(path, "w", encoding="utf-8", newline="\n").write(out)
    with io.open(AUDIT_OUT, "w", encoding="utf-8-sig", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=["idx", "id", "name_he", "g", "lang", "value", "why", "action"])
        w.writeheader()
        for a in audit:
            w.writerow(a)
    order = {"filled": 0, "matched-nothing-new": 1, "he-mismatch": 2, "wikidata-missing": 3, "bad-wikidata-tag": 4,
             "no-wikidata-tag": 5, "rejected-strict": 6, "ambiguous": 7, "no-match": 8}
    with io.open(CSV_OUT, "w", encoding="utf-8-sig", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0].keys()))
        w.writeheader()
        for r in sorted(rows, key=lambda r: (order[r["status"]], r["walk_min"] if r["walk_min"] is not None else 99, r["idx"])):
            w.writerow(r)
    io.open(os.path.join(EV, "stats.json"), "w", encoding="utf-8", newline="\n").write(json.dumps(stats, ensure_ascii=False, indent=1) + "\n")
    print(json.dumps(stats, ensure_ascii=False))
    print("md5", hashlib.md5(out.encode("utf-8")).hexdigest(), "bytes", len(out.encode("utf-8")))


if __name__ == "__main__":
    main()
