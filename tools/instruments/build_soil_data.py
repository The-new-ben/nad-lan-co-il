# -*- coding: utf-8 -*-
"""Builds plugins/nadlan-config/assets/instruments/data/sde-dov-soil.json for the Sde Dov soil map (HAD-534).

Plots: every plot of the district from the Tel Aviv municipal GIS layer 837 (plans 3001, 1/4444, 2/4444), polygons in
WGS84. Status, boreholes and values: docs/research/2026-10-15-sde-dov-soil/samples.json (each record carries its source).
Thresholds: the reports compare to "direct-contact values for Sde Dov, June 2026" (ng/kg): PFOS 6,321.4, PFOA 1,896.4,
PFHxS 39,824.6. Nothing is invented: a plot without a published report keeps its reported status and no number.
Run: python tools/instruments/build_soil_data.py
"""
import datetime
import io
import json
import os
import urllib.parse
import urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
SAMPLES = os.path.join(ROOT, "docs", "research", "2026-10-15-sde-dov-soil", "samples.json")
OUT = os.path.join(ROOT, "plugins", "nadlan-config", "assets", "instruments", "data", "sde-dov-soil.json")
LAYER = "https://gisn.tel-aviv.gov.il/arcgis/rest/services/IView2/MapServer/837"
TH = {"pfos": 6321.4, "pfoa": 1896.4, "pfhxs": 39824.6}
# Ben 15.10.2026: the public file carries NO project or company names (the named research stays in docs/research/...). Per plot
# only the phase: a project in marketing (our own catalogue) and the sourced stage (RMI tender, municipal permit request).
PHASE = {
    "107": {"mkt": True, "stage": "פרויקט בשיווק"},
    "103": {"mkt": True, "stage": "פרויקט בשיווק"},
    "106": {"mkt": True, "stage": "פרויקט בשיווק"},
    "2206": {"mkt": True, "stage": "פרויקט בשיווק · הוגשה בקשה להיתר חפירה ודיפון (8.10.2026)"},
    "2255": {"mkt": False, "stage": "הוגשה בקשה להיתר חפירה ודיפון (8.10.2026)"},
    "2270": {"mkt": False, "stage": "נמכר במכרז רמ\"י (פברואר 2025)"},
    "303": {"mkt": False, "stage": "נמכר במכרז רמ\"י (דצמבר 2024)"},
    "301": {"mkt": False, "stage": "נמכר במכרז רמ\"י (דצמבר 2024)"},
}


def gis(params):
    q = urllib.parse.urlencode(params)
    with urllib.request.urlopen(LAYER + "/query?" + q, timeout=60) as r:
        return json.loads(r.read().decode("utf-8"))


def rnd(rings):
    return [[[round(x, 6), round(y, 6)] for x, y in ring] for ring in rings]


def main():
    feats, off = [], 0
    while True:
        d = gis({"where": "st_taba IN ('3001','תמ\"ל3001','1/4444','2/4444','4444')", "outFields": "oid_migrash,st_mispar_migrash_betaba,st_taba,t_yeud_karka,ms_shetach_rashum",
                 "returnGeometry": "true", "outSR": "4326", "geometryPrecision": "6", "maxAllowableOffset": "0.000006", "resultOffset": str(off), "resultRecordCount": "1000", "f": "json"})
        if d.get("error"):
            raise SystemExit("GIS error: %r" % d["error"])
        got = d.get("features", [])
        feats += got
        if not d.get("exceededTransferLimit") or not got:
            break
        off += len(got)
    samples = json.load(io.open(SAMPLES, encoding="utf-8"))
    by_oid = {}
    for s in samples:
        for oid in (s.get("municipal_gis") or {}).get("oid_migrash") or []:
            by_oid[oid] = s["plot"]
    plots = []
    for f in feats:
        a = f["attributes"]
        g = (f.get("geometry") or {}).get("rings")
        if not g:
            continue
        plots.append({"oid": a["oid_migrash"], "n": str(a["st_mispar_migrash_betaba"] or "").strip(), "plan": (a["st_taba"] or "").strip(),
                      "use": (a["t_yeud_karka"] or "").strip(), "m2": round(a["ms_shetach_rashum"] or 0), "ref": by_oid.get(a["oid_migrash"]), "g": rnd(g)})
    recs = []
    for s in samples:
        bh = []
        for b in s.get("boreholes") or []:
            if b.get("lat") is None:
                continue
            bh.append({"id": b.get("id"), "lat": b["lat"], "lng": b["lng"], "pfos": b.get("pfos_max_ng_kg"), "pfosD": b.get("pfos_max_depth_m"),
                       "pfoa": b.get("pfoa_max_ng_kg"), "n": b.get("samples"), "approx": b.get("coord_kind") == "digitized_from_figure"})
        pf = s.get("pfos_max") if isinstance(s.get("pfos_max"), dict) else {}
        pa = s.get("pfoa_max") if isinstance(s.get("pfoa_max"), dict) else {}
        recs.append({"plot": s["plot"], "status": s["data_status"], "plan": s.get("plan"), "use": s.get("land_use_gis"),
                     "phase": PHASE.get(s["plot"]), "oids": (s.get("municipal_gis") or {}).get("oid_migrash") or [],
                     "dates": s.get("sampling_dates"), "holes": s.get("boreholes_executed"), "pfosMax": pf.get("value_ng_kg"),
                     "pfosDepth": pf.get("depth_m"), "pfosX": pf.get("multiple"), "pfosHoles": pf.get("boreholes_exceeding"),
                     "pfoaMax": pa.get("value_ng_kg"), "pfoaX": pa.get("multiple"), "pfoaHoles": pa.get("boreholes_exceeding"),
                     "report": s.get("report_date"),
                     "src": s.get("source_url") if s["data_status"] == "published_report" else None, "bh": bh})  # only the official report
    out = {"key": "soil", "built": datetime.date.today().isoformat(), "thresholds": TH,
           "thresholdsLabel": "ערכי סף למגע ישיר עבור שדה דב, יוני 2026 (כפי שמצוטטים בדו\"חות)",
           "sourcesNote": "דו\"חות סקרי הקרקע של פרויקט אבן דרך במאגר המשרד להגנת הסביבה; שכבת המגרשים 837 של עיריית תל אביב",
           "plots": plots, "records": recs}
    io.open(OUT, "w", encoding="utf-8", newline="\n").write(json.dumps(out, ensure_ascii=False, separators=(",", ":")))
    print("plots", len(plots), "records", len(recs), "boreholes", sum(len(r["bh"]) for r in recs), "bytes", os.path.getsize(OUT))
    print("linked plots", sorted({p["ref"] for p in plots if p["ref"]}))


if __name__ == "__main__":
    main()
