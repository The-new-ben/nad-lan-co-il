# -*- coding: utf-8 -*-
"""יומן המתחמים (Q1 moat, docs/research/2026-10-26-upgrades/q1-renewal-map/dna.md 7.8): the official stage of every urban renewal
complex today and every change we saw between dated snapshots of the official lists. Nobody else keeps this history.

Snapshots (raw, private, dated by the version of the data, never copied into the plugin):
  site_2026-07-13.json   our own import of the data.gov.il file, read back from the public WordPress REST (947 complexes); read once
  file_<last_modified>   the Ministry of Construction and Housing open file (data.gov.il resource f65a0daf-...), every row
  map_<last edit, UTC>   the authority's live map layer (ArcGIS GIS_UrbanRenewal layer 1, feeds the gov.il map): attributes only,
                         no geometry (its licence field is empty, research F9); stages and counts are fact reporting
  xplan_<fetch date>     XPLAN (Planning Administration ArcGIS) by plan number: station, deposit discussion, approval publication
They live in RAW (default below, override with NADLAN_URTRACK_RAW). Every weekly run adds a snapshot only when a source changed
(a new file last_modified or a new map edit date), so the history only grows.

Writes plugins/nadlan-config/assets/instruments/data/renewal-track.json (key "urtrack", read by tools/urtrack.js).
  python tools/urban/build_renewal_track.py              fetch the sources (site only if no site snapshot yet), then build
  python tools/urban/build_renewal_track.py --offline    build from the saved snapshots only
  python tools/urban/build_renewal_track.py --import-map ROWS.json META.json
                                                         turn a saved ArcGIS pull (query rows + layer meta) into a dated snapshot
Read-only everywhere: GET requests to data.gov.il, ArcGIS, XPLAN and our public REST; nothing is written to any site."""
import argparse, collections, datetime, hashlib, html, io, json, os, re, ssl, sys, urllib.parse, urllib.request

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
H = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.dirname(os.path.dirname(H))
OUT = os.path.join(REPO, "plugins", "nadlan-config", "assets", "instruments", "data", "renewal-track.json")
STATS = os.path.join(REPO, "plugins", "nadlan-config", "data", "renewal-stats.json")
RAW = os.environ.get("NADLAN_URTRACK_RAW") or r"C:\Users\777\nad-lan\_private-research\2026-10-26-upgrades\raw\q1-track"
UA = {"User-Agent": "Mozilla/5.0 NadLan-RenewalTrack/1.0"}
FILE_RES = "f65a0daf-f737-49c5-9424-d378d52104f5"
LAYER = "https://services6.arcgis.com/I08Ekaykft5ELucH/arcgis/rest/services/GIS_UrbanRenewal/FeatureServer/1"
XPLAN = "https://ags.iplan.gov.il/arcgisiplan/rest/services/PlanningPublic/Xplan/MapServer/1/query"
SITE_REST = "https://nad-lan.co.il/wp-json/wp/v2/nadlan_project"
SITE_FIELDS = "id,date,modified,slug,link,title,meta.city,meta.project_status,meta.num_units,meta.source,meta.source_url,meta.project_type"
SITE_IMPORT_DATE = "2026-07-13"  # the import run that wrote the project pages (892 of 947 posts last modified that day; F11)
KIND_ORDER = {"site": 0, "file": 1, "map": 2}
# one ladder for every source; 0 = no stage in that source (the map leaves the stage empty mostly where the file says
# "after licensing"), so 0 is never compared across sources
STAGES = ["ללא שלב", "תכנון ראשוני", "תכנון סטטוטורי", "תכנית מאושרת לפני מימוש", "תכנית מאושרת במימוש", "תכנית מאושרת אחרי רישוי"]
RANK = {1: 1, 2: 2, 3: 3, 4: 4, 5: 4}  # 4 (in implementation) and 5 (after licensing) are both past approval: a move between them has no direction
TRACKS = ["", "מיסוי", "רשויות", "טרם הוכרז"]
SNAP_LABEL = {"site": "הייבוא שלנו", "file": "קובץ data.gov.il", "map": "מפת הרשות"}
SNAP_SHORT = {"site": "ייבוא", "file": "קובץ", "map": "מפה"}


def get(url, ctx=None, raw=False):
    r = urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=90, context=ctx)
    body = r.read().decode("utf-8")
    return (json.loads(body), r.headers) if raw else json.loads(body)


def xplan_ctx():
    """XPLAN's server only completes a handshake with an older cipher set (Python's default refuses it; curl accepts it)."""
    c = ssl.create_default_context()
    c.set_ciphers("DEFAULT@SECLEVEL=1")
    c.options |= getattr(ssl, "OP_LEGACY_SERVER_CONNECT", 0x4)
    return c


def cl(s):
    """Whitespace, no-break spaces and long dashes as the files carry them; the site prints no long dash."""
    return re.sub(r"\s+", " ", re.sub(r"\s*[\u2013\u2014]\s*", " - ", str(s if s is not None else "").replace("\xa0", " "))).strip()


def num(x):
    m = re.fullmatch(r"\d+", re.sub(r"[,\s]", "", str(x if x is not None else "")))
    return int(m.group(0)) if m else 0


def ncity(s):
    return re.sub(r"\s+", " ", cl(s).replace("-", " ")).replace("יי", "י").replace("וו", "ו").strip()


def nname(s):
    s = re.sub(r"[-,.\"'\u05f3\u05f4()/\\;:]", " ", html.unescape(cl(s)))
    return re.sub(r"\s+", " ", s).strip().replace("יי", "י").replace("וו", "ו")


def stage_of_text(s):
    t = re.sub(r"\s+", " ", cl(s).replace("-", " ")).strip()
    return {"תכנון ראשוני": 1, "תכנון סטטוטורי": 2, "תכנית מאושרת לפני מימוש": 3, "תכנית מאושרת במימוש": 4, "תכנית מאושרת אחרי רישוי": 5}.get(t, 0)


def track_of(s):
    t = cl(s)
    return "מיסוי" if "מיסוי" in t else "רשויות" if "רשויות" in t else "טרם הוכרז" if "טרם" in t else ""


def mavat_id(u):
    m = re.search(r"/SV4/1/(\d+)", u or "")
    return m.group(1) if m else ""


def dmy_iso(s):
    m = re.fullmatch(r"(\d{1,2})/(\d{1,2})/(\d{4})", cl(s))
    return "%s-%02d-%02d" % (m.group(3), int(m.group(2)), int(m.group(1))) if m else ""


def ms_iso(ms):
    return datetime.datetime.fromtimestamp(ms / 1000, datetime.timezone.utc).date().isoformat() if ms else ""


def plan_key(p):
    return re.sub(r"\s+", " ", cl(p)).strip()


# ---------- snapshots on disk ----------
def snap_path(kind, date, suffix=""):
    return os.path.join(RAW, "%s_%s%s.json" % (kind, date, suffix))


def rows_hash(rows):
    return hashlib.sha1(json.dumps(rows, ensure_ascii=False, sort_keys=True).encode("utf-8")).hexdigest()


def save_snapshot(kind, date, payload):
    """Snapshots are immutable evidence: the same version is never rewritten; a different body under the same date gets a suffix."""
    os.makedirs(RAW, exist_ok=True)
    payload["sha1"] = rows_hash(payload["rows"])
    p = snap_path(kind, date)
    if os.path.exists(p):
        old = json.load(io.open(p, encoding="utf-8"))
        if old.get("sha1") == payload["sha1"]:
            print("  %s %s: unchanged, kept %s" % (kind, date, os.path.basename(p)))
            return p
        p = snap_path(kind, date, "_r" + payload["fetched"][:10])
        if os.path.exists(p):
            print("  %s %s: kept existing revision %s" % (kind, date, os.path.basename(p)))
            return p
    io.open(p, "w", encoding="utf-8", newline="\n").write(json.dumps(payload, ensure_ascii=False))
    print("  saved", p, len(payload["rows"]), "rows")
    return p


def now_iso():
    return datetime.datetime.now(datetime.timezone.utc).replace(microsecond=0).isoformat()


def fetch_site():
    rows, page = [], 1
    while True:
        d, hd = get("%s?per_page=100&page=%d&_fields=%s" % (SITE_REST, page, SITE_FIELDS), raw=True)
        rows += [x for x in d if (x.get("meta") or {}).get("source") == "urban_renewal"]
        if page >= int(hd.get("X-WP-TotalPages") or 1):
            break
        page += 1
    mode = collections.Counter(x["modified"][:10] for x in rows).most_common(1)
    if mode and mode[0][0] != SITE_IMPORT_DATE:
        print("  WARNING: most project pages were last modified on %s, not %s" % (mode[0][0], SITE_IMPORT_DATE))
    save_snapshot("site", SITE_IMPORT_DATE, {"kind": "site", "date": SITE_IMPORT_DATE, "fetched": now_iso(), "source": SITE_REST + " (source=urban_renewal)", "rows": rows})


def fetch_file():
    meta = get("https://data.gov.il/api/3/action/resource_show?id=" + FILE_RES)["result"]
    rows, off = [], 0
    while True:
        d = get("https://data.gov.il/api/3/action/datastore_search?resource_id=%s&limit=1000&offset=%d" % (FILE_RES, off))["result"]
        rows += d["records"]; off += len(d["records"])
        if not d["records"] or off >= d["total"]:
            break
    date = (meta.get("last_modified") or meta.get("metadata_modified") or "")[:10]
    save_snapshot("file", date, {"kind": "file", "date": date, "fetched": now_iso(), "source": "https://data.gov.il/dataset/urban_renewal resource " + FILE_RES,
                                 "last_modified": meta.get("last_modified"), "rows": rows})


def map_payload(feats, meta, fetched):
    edit = (meta.get("editingInfo") or {}).get("dataLastEditDate")
    date = ms_iso(edit)
    rows = sorted([f["attributes"] for f in feats], key=lambda a: (a.get("OBJECTID") or 0))
    for a in rows:
        a.pop("Shape__Area", None); a.pop("Shape__Length", None)
    return date, {"kind": "map", "date": date, "fetched": fetched, "source": LAYER, "dataLastEditDate": edit, "rows": rows}


def fetch_map():
    meta = get(LAYER + "?f=json")
    total = get(LAYER + "/query?where=1%3D1&returnCountOnly=true&f=json")["count"]
    feats, off = [], 0
    while len(feats) < total:
        q = get(LAYER + "/query?" + urllib.parse.urlencode({"where": "1=1", "outFields": "*", "returnGeometry": "false", "f": "json",
                                                            "orderByFields": "OBJECTID", "resultOffset": off, "resultRecordCount": 1000}))
        fs = q.get("features", [])
        if not fs:
            break
        feats += fs; off += len(fs)
    if len(feats) != total:
        raise SystemExit("map: got %d rows, layer says %d" % (len(feats), total))
    date, payload = map_payload(feats, meta, now_iso())
    save_snapshot("map", date, payload)


def import_map(rows_file, meta_file):
    feats = json.load(io.open(rows_file, encoding="utf-8"))["features"]
    meta = json.load(io.open(meta_file, encoding="utf-8"))
    fetched = datetime.datetime.fromtimestamp(os.path.getmtime(rows_file), datetime.timezone.utc).replace(microsecond=0).isoformat()
    date, payload = map_payload(feats, meta, fetched)
    payload["note"] = "imported from a saved pull: " + os.path.basename(rows_file)
    save_snapshot("map", date, payload)


def fetch_xplan(plans):
    ctx, rows = xplan_ctx(), []
    plans = sorted(set(p for p in plans if p))
    for i in range(0, len(plans), 40):
        chunk = plans[i:i + 40]
        d = get(XPLAN + "?" + urllib.parse.urlencode({"where": "pl_number IN (" + ",".join("'" + p.replace("'", "''") + "'" for p in chunk) + ")",
                                                      "outFields": "pl_number,station_desc,internet_short_status,depositing_date,pl_date_8,last_update_date",
                                                      "returnGeometry": "false", "f": "json"}), ctx=ctx)
        if "error" in d:
            raise SystemExit("xplan error: %s" % d["error"])
        rows += [f["attributes"] for f in d.get("features", [])]
    today = datetime.date.today().isoformat()
    save_snapshot("xplan", today, {"kind": "xplan", "date": today, "fetched": now_iso(), "source": XPLAN, "asked": len(plans), "rows": rows})


def load_snapshots():
    snaps = []
    for fn in sorted(os.listdir(RAW)) if os.path.isdir(RAW) else []:
        m = re.fullmatch(r"(site|file|map|xplan)_(\d{4}-\d{2}-\d{2})(_r[\d-]+)?\.json", fn)
        if m:
            d = json.load(io.open(os.path.join(RAW, fn), encoding="utf-8"))
            d["_file"] = fn
            snaps.append(d)
    # one snapshot per kind and date: a revision (_r...) replaces the first body of the same version
    best = {}
    for s in snaps:
        k = (s["kind"], s["date"])
        if k not in best or s["_file"] > best[k]["_file"]:
            best[k] = s
    return sorted(best.values(), key=lambda s: (s["date"], KIND_ORDER.get(s["kind"], 9)))


# ---------- one row shape for every source ----------
def rows_file(s):
    out = []
    for r in s["rows"]:
        out.append({"id": num(r.get("MisparMitham")) or None, "name": cl(r.get("ShemMitcham")), "city": cl(r.get("Yeshuv")),
                    "st": stage_of_text(r.get("Status")), "tr": track_of(r.get("Maslul")), "e": num(r.get("YachadKayam")), "p": num(r.get("YachadMutza")),
                    "plan": plan_key(r.get("MisparTochnit")), "mv": mavat_id(cl(r.get("KishurLatar"))), "dc": dmy_iso(r.get("TaarichHachraza")),
                    "pm": num(r.get("SachHeterim")), "bz": cl(r.get("Bebitzua")) == "כן", "ty": "", "ap": ""})
    return out


def rows_map(s):
    out, seen = [], set()
    for a in s["rows"]:
        i = a.get("MisparProject")
        if i in seen:  # a complex drawn as several polygons appears once per polygon, with the same attributes
            continue
        seen.add(i)
        out.append({"id": i, "name": cl(a.get("ShemMitcham")), "city": cl(a.get("Yeshuv")), "st": a.get("codeStatusHarashut") or 0,
                    "tr": track_of(a.get("TeurSugMaslul")), "e": num(a.get("yachadKayamRashut")), "p": num(a.get("yachadMutzaRashut")),
                    "plan": plan_key(a.get("plan_name")), "mv": mavat_id(a.get("Kishur")), "ap": ms_iso(a.get("taarichTokef")),
                    "ty": cl(a.get("TeurMaslul")), "dc": "", "pm": 0, "bz": False})
    return out


def rows_site(s):
    out = []
    for x in s["rows"]:
        m = x.get("meta") or {}
        out.append({"id": None, "name": cl(html.unescape(x["title"]["rendered"])), "city": cl(m.get("city")), "st": stage_of_text(m.get("project_status")),
                    "tr": "", "e": 0, "p": num(m.get("num_units")), "plan": "", "mv": mavat_id(cl(m.get("source_url"))), "ap": "", "dc": "", "pm": 0, "bz": False, "ty": "",
                    "slug": urllib.parse.unquote(x.get("slug") or "")})
    return out


def build():
    snaps = load_snapshots()
    base = [s for s in snaps if s["kind"] in KIND_ORDER]
    xp = [s for s in snaps if s["kind"] == "xplan"]
    if not base:
        raise SystemExit("no snapshots in " + RAW)
    conv = {"site": rows_site, "file": rows_file, "map": rows_map}
    S = [conv[s["kind"]](s) for s in base]
    # site rows carry no complex id: join them to the authority id by city + name, then by the planning-site link. Our import was
    # made from the data.gov.il file, so the file's ids come first; the map only when the file has no unique match.
    idx = {"file": collections.defaultdict(set), "map": collections.defaultdict(set)}
    by_mv = {"file": collections.defaultdict(set), "map": collections.defaultdict(set)}
    for s, rows in zip(base, S):
        if s["kind"] == "site":
            continue
        for r in rows:
            idx[s["kind"]][(ncity(r["city"]), nname(r["name"]))].add(r["id"])
            if r["mv"]:
                by_mv[s["kind"]][r["mv"]].add(r["id"])
    joined = {"name": 0, "link": 0, "none": 0}
    for s, rows in zip(base, S):
        if s["kind"] != "site":
            continue
        for r in rows:
            nk = (ncity(r["city"]), nname(r["name"]))
            hit = next((("name", idx[k][nk]) for k in ("file", "map") if len(idx[k].get(nk, ())) == 1), None)
            if not hit and r["mv"]:
                hit = next((("link", by_mv[k][r["mv"]]) for k in ("file", "map") if len(by_mv[k].get(r["mv"], ())) == 1), None)
            if hit:
                r["id"] = next(iter(hit[1])); joined[hit[0]] += 1
            else:
                joined["none"] += 1
    key = lambda r: str(r["id"]) if r["id"] else "s:" + ncity(r["city"]) + "|" + nname(r["name"])
    N = len(base)
    recs = collections.OrderedDict()
    for i, rows in enumerate(S):
        for r in rows:
            recs.setdefault(key(r), [None] * N)[i] = r
    # renumbered: in one snapshot a complex leaves under one id and a complex with the same city and name enters under another.
    # That is one complex with a new number, not a removal and an addition: the history moves to the new id (the stable key).
    renum = []
    for i in range(1, N):
        gone, new = collections.defaultdict(list), collections.defaultdict(list)
        for k, per in recs.items():
            if per[i - 1] and not per[i] and not any(per[j] for j in range(i, N)):
                gone[(ncity(per[i - 1]["city"]), nname(per[i - 1]["name"]))].append(k)
            if per[i] and not any(per[j] for j in range(i)):
                new[(ncity(per[i]["city"]), nname(per[i]["name"]))].append(k)
        for nk, ks in gone.items():
            if len(ks) == 1 and len(new.get(nk, ())) == 1:
                old, nw = ks[0], new[nk][0]
                for j in range(i):
                    recs[nw][j] = recs[old][j]
                del recs[old]
                renum.append((base[i]["date"], old, nw))
    last_file = max([i for i, s in enumerate(base) if s["kind"] == "file"], default=None)
    last_map = max([i for i, s in enumerate(base) if s["kind"] == "map"], default=None)
    xrows = {}
    if xp:
        for a in xp[-1]["rows"]:
            xrows[a["pl_number"]] = a
    xst = []  # XPLAN station names, indexed

    def latest(per, field, kinds=None):
        for i in range(N - 1, -1, -1):
            r = per[i]
            if r and r.get(field) and (kinds is None or base[i]["kind"] in kinds):
                return r[field], i
        return None, None

    out_recs, changes = [], []
    for k, per in recs.items():
        s_list = [(-1 if r is None else r["st"]) for r in per]
        first = next(i for i, r in enumerate(per) if r)
        ch = []
        for i in range(1, N):
            a, b = per[i - 1], per[i]
            d = base[i]["date"]
            if a is None and b is not None:
                if i > first:
                    ch.append([d, "back", -1, b["st"]])
                elif i == first:
                    ch.append([d, "new", -1, b["st"]])
            elif a is not None and b is None:
                ch.append([d, "gone", a["st"], -1])
            elif a is not None and b is not None:
                if a["id"] and b["id"] and a["id"] != b["id"]:
                    ch.append([d, "renum", a["id"], b["id"]])
                same_kind = base[i - 1]["kind"] == base[i]["kind"]
                if a["st"] != b["st"] and (a["st"] and b["st"] or same_kind):
                    ra, rb = RANK.get(a["st"], 0), RANK.get(b["st"], 0)
                    ch.append([d, "up" if rb > ra and ra else "down" if rb < ra and rb else "chg", a["st"], b["st"]])
                if a["tr"] and b["tr"] and a["tr"] != b["tr"]:
                    ch.append([d, "trk", TRACKS.index(a["tr"]), TRACKS.index(b["tr"])])
        # a complex first seen in the first snapshot gets no "new": we do not know when it entered the list
        cur = next(r for r in reversed(per) if r)
        name, _ = latest(per, "name"); city, _ = latest(per, "city")
        rec = {"k": k, "n": name, "c": city, "s": s_list, "f": first}
        tr, _ = latest(per, "tr", ("map",))
        if not tr:
            tr, _ = latest(per, "tr")
        if tr:
            rec["t"] = TRACKS.index(tr)
        ty, _ = latest(per, "ty")
        if ty and ty != "פינוי בינוי":
            rec["ty"] = ty
        # units: the freshest source that publishes them; the file's figures beside them when they differ
        ui = next((i for i in range(N - 1, -1, -1) if per[i] and per[i]["p"] and base[i]["kind"] != "site"), None)
        if ui is None:
            ui = next((i for i in range(N - 1, -1, -1) if per[i] and per[i]["p"]), None)
        if ui is not None:
            rec["e"], rec["p"], rec["u"] = per[ui]["e"], per[ui]["p"], ui
            if last_file is not None and per[last_file] and ui != last_file and (per[last_file]["e"], per[last_file]["p"]) != (per[ui]["e"], per[ui]["p"]) and per[last_file]["p"]:
                rec["ef"], rec["pf"] = per[last_file]["e"], per[last_file]["p"]
        plan, _ = latest(per, "plan")
        if plan:
            rec["pl"] = plan
        mv, _ = latest(per, "mv")
        if mv:
            rec["mv"] = mv
        ap, _ = latest(per, "ap")
        if ap:
            rec["ap"] = ap
        if last_file is not None and per[last_file]:
            fr = per[last_file]
            if fr["dc"]:
                rec["dc"] = fr["dc"]
            if fr["pm"]:
                rec["pm"] = fr["pm"]
            if fr["bz"]:
                rec["bz"] = 1
        if plan and plan in xrows:
            x = xrows[plan]
            stn = cl(x.get("station_desc"))
            if stn not in xst:
                xst.append(stn)
            rec["x"] = [xst.index(stn), ms_iso(x.get("depositing_date")), ms_iso(x.get("pl_date_8"))]
        sl = next((r.get("slug") for r in per if r and r.get("slug")), None)
        if sl:
            rec["w"] = sl
        if ch:
            rec["ch"] = ch
            for c in ch:
                changes.append({"k": k, "n": name, "c": city, "d": c[0], "kind": c[1], "a": c[2], "b": c[3]})
        out_recs.append(rec)
    out_recs.sort(key=lambda r: (r["c"], r["n"]))
    # page level: since the last official file, against the freshest map
    agg = {"since": base[last_file]["date"] if last_file is not None else "", "to": base[last_map]["date"] if last_map is not None else ""}
    by_city = collections.OrderedDict()
    tot = collections.Counter()
    if last_file is not None and last_map is not None:
        for k, per in recs.items():
            f, m = per[last_file], per[last_map]
            r = f or m
            if not r:  # only in our import: counted in the change list, not in the file-to-map comparison
                continue
            c = by_city.setdefault(r["city"], collections.Counter())
            if m:
                c["n"] += 1
            if m and not f:
                c["add"] += 1; tot["add"] += 1
            elif f and not m:
                c["gone"] += 1; tot["gone"] += 1
            else:
                if f["id"] != m["id"]:
                    c["renum"] += 1; tot["renum"] += 1
                if f["st"] and m["st"] and f["st"] != m["st"]:
                    ra, rb = RANK[f["st"]], RANK[m["st"]]
                    kk = "up" if rb > ra else "down" if rb < ra else "chg"
                    c[kk] += 1; tot[kk] += 1
    agg.update({"added": tot["add"], "up": tot["up"], "down": tot["down"], "chg": tot["chg"], "gone": tot["gone"], "renum": tot["renum"]})
    agg["cities"] = {c: dict(v) for c, v in sorted(by_city.items(), key=lambda x: (-x[1]["n"], x[0])) if v}
    if N >= 2:
        prev = base[N - 2]["date"]; lastd = base[N - 1]["date"]
        lc = collections.Counter(x["kind"] for x in changes if x["d"] == lastd)
        agg["last"] = {"from": prev, "to": lastd, **{k2: lc[k2] for k2 in ("new", "up", "down", "chg", "gone", "back", "trk", "renum")}}
    order = {"up": 0, "new": 1, "down": 2, "chg": 3, "trk": 4, "renum": 5, "back": 6, "gone": 7}
    changes.sort(key=lambda x: (order[x["kind"]], x["c"], x["n"]))
    changes.sort(key=lambda x: x["d"], reverse=True)  # stable: newest check first, then by kind, city, name
    snaps_out = []
    for i, s in enumerate(base):
        rows = S[i]
        snaps_out.append({"k": s["kind"], "d": s["date"], "label": SNAP_LABEL[s["kind"]], "short": SNAP_SHORT[s["kind"]], "rows": len(s["rows"]), "n": len(rows),
                          "fetched": s["fetched"][:10]})
    stats = json.load(io.open(STATS, encoding="utf-8")) if os.path.exists(STATS) else {}
    out = {
        "key": "urtrack", "built": datetime.date.today().isoformat(),
        "snaps": snaps_out, "stages": STAGES, "tracks": TRACKS, "xst": xst,
        "xplan": {"d": xp[-1]["date"], "asked": xp[-1].get("asked"), "found": len(xp[-1]["rows"])} if xp else None,
        "agg": agg,
        "avg": {"years": 4.0, "n": 28, "year": 2025, "src": "דוח הרשות הממשלתית להתחדשות עירונית לשנת 2025"},
        "sources": [
            {"label": "מפת הרשות הממשלתית להתחדשות עירונית, gov.il", "url": "https://www.gov.il/he/departments/topics/mapa-renewal"},
            {"label": "קובץ מתחמי ההתחדשות העירונית, data.gov.il", "url": "https://data.gov.il/dataset/urban_renewal"},
            {"label": "XPLAN, מינהל התכנון", "url": "https://www.gov.il/he/service/searching-plans-submitted-planning-institutes-in-xplan-site"},
            {"label": "דוח הרשות לשנת 2025", "url": "https://www.gov.il/he/pages/urban_renewal_report_2025"}],
        "recs": out_recs,
    }
    io.open(OUT, "w", encoding="utf-8", newline="\n").write(json.dumps(out, ensure_ascii=False, separators=(",", ":")) + "\n")
    size = os.path.getsize(OUT)
    print("snapshots:", ", ".join("%s %s (%d rows, %d complexes)" % (s["k"], s["d"], s["rows"], s["n"]) for s in snaps_out))
    print("site join: by name %(name)d, by plan link %(link)d, unmatched %(none)d" % joined)
    print("records %d | changes %d %s" % (len(out_recs), len(changes), dict(collections.Counter(x["kind"] for x in changes))))
    print("renumbered (merged):", [(d0, o, n) for d0, o, n in renum])
    print("since %s to %s: added %d, up %d, down %d, other %d, gone %d, renumbered %d" % (agg["since"], agg["to"], agg["added"], agg["up"], agg["down"], agg["chg"], agg["gone"], agg["renum"]))
    if "last" in agg:
        print("last step", agg["last"])
    if out["xplan"]:
        print("xplan %s: %d of %d plan numbers found; records with XPLAN data %d" % (out["xplan"]["d"], out["xplan"]["found"], out["xplan"]["asked"], sum(1 for r in out_recs if "x" in r)))
    if stats:
        print("renewal-stats.json: file %s total %s | map %s total %s" % (stats["file"]["last_modified"], stats["file"]["total"], stats["map"]["last_edit"], stats["map"]["total"]))
    print("wrote %s (%d KB)" % (OUT, size // 1024))
    if size > 600 * 1024:
        print("WARNING: over 600 KB")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--offline", action="store_true", help="build from the saved snapshots only")
    ap.add_argument("--site", action="store_true", help="read our import back even if a site snapshot exists")
    ap.add_argument("--import-map", nargs=2, metavar=("ROWS", "META"), help="turn a saved ArcGIS pull into a dated snapshot")
    a = ap.parse_args()
    if a.import_map:
        import_map(*a.import_map)
    if not a.offline:
        print("fetching (read only) into", RAW)
        if a.site or not any(fn.startswith("site_") for fn in (os.listdir(RAW) if os.path.isdir(RAW) else [])):
            fetch_site()
        fetch_file()
        fetch_map()
        plans = set()
        for s in load_snapshots():
            if s["kind"] == "map":
                plans |= {plan_key(r.get("plan_name")) for r in s["rows"]}
            elif s["kind"] == "file":
                plans |= {plan_key(r.get("MisparTochnit")) for r in s["rows"]}
        fetch_xplan(plans)
    build()


if __name__ == "__main__":
    main()
