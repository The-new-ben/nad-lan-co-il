# -*- coding: utf-8 -*-
"""Build the TIER-3 edits (listing-site rents left in the body, CEO rule of 7.10.2026) and APPEND them to
docs/content/city-align-2026-10/<slug>.align-edits.json as "tier": 3 entries (n continues the numbering; tier 1 and tier 2 are untouched).

DATA ONLY: reads the live pages (public GET), writes only the JSON files of the pages that get tier-3 edits.

Rule (approved by the owner): for every remaining rent figure from a listing site: if the CBS publishes the same thing (city + size group, table 4.9, Q2 2026),
REPLACE it with the CBS value and its quarter; if not (neighbourhood rents, cities outside the CBS big-city list, houses), REMOVE the number and keep a
sentence only if it is still true and useful without it (no level claim without an official figure), else DELETE the sentence, row, column or paragraph.

python b_tier3_ceo.py [--live-dir DIR] [--dry] [slug ...]
"""
import importlib, io, json, os, sys, time, urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import b3lib as L

ARGS = sys.argv[1:]
LIVE_DIR = ARGS[ARGS.index("--live-dir") + 1] if "--live-dir" in ARGS else None
DRY = "--dry" in ARGS
ONLY = [a for a in ARGS if not a.startswith("--") and a != LIVE_DIR]
OUTDIR = L.OUTDIR

MODULES = {  # slug -> module name
    "ashdod-apartment-prices": "b3_ashdod",
    "ashkelon-apartment-prices": "b3_ashkelon",
    "bat-yam-apartment-prices": "b3_batyam",
    "beer-sheva-apartment-prices": "b3_beersheva",
    "bnei-brak-apartment-prices": "b3_bnei",
    "eilat-apartment-prices": "b3_eilat",
    "givatayim-apartment-prices": "b3_giv",
    "haifa-apartment-prices": "b3_haifa",
    "herzliya-apartment-prices": "b3_herzliya",
    "hod-hasharon-apartment-prices": "b3_hod",
    "holon-apartment-prices": "b3_holon",
    "jerusalem-apartment-prices": "b3_jerusalem",
    "kfar-saba-apartment-prices": "b3_kfarsaba",
    "kiryat-ono-apartment-prices": "b3_kiryatono",
    "modiin-apartment-prices": "b3_modiin",
    "netanya-apartment-prices": "b3_netanya",
    "petah-tikva-apartment-prices": "b3_petah",
    "raanana-apartment-prices": "b3_raa",
    "ramat-gan-apartment-prices": "b3_ramatgan",
    "ramat-hasharon-apartment-prices": "b3_rhs",
    "rehovot-apartment-prices": "b3_rehovot",
    "rishon-lezion-apartment-prices": "b3_rishon",
}


def load_live(slug, pid):
    if LIVE_DIR:
        return json.load(io.open(os.path.join(LIVE_DIR, slug + ".json"), encoding="utf-8"))
    u = "https://nad-lan.co.il/wp-json/wp/v2/pages/%d?_fields=id,link,modified,content&nlca=%d" % (pid, time.time())
    p = json.loads(urllib.request.urlopen(urllib.request.Request(u, headers={"User-Agent": "Mozilla/5.0 NadLan-cityalign"}), timeout=90).read().decode("utf-8"))
    p["retrieved_utc"] = time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())
    return p


def main():
    summary = []
    for slug, modname in MODULES.items():
        if ONLY and slug not in ONLY:
            continue
        if not os.path.exists(os.path.join(HERE, modname + ".py")):
            print(f"{slug}: module {modname}.py missing, skipped")
            continue
        path = os.path.join(OUTDIR, slug + ".align-edits.json")
        J = json.loads(io.open(path, encoding="utf-8", newline="").read())
        J["edits"] = [e for e in J["edits"] if e.get("tier") != 3]  # idempotent rebuild
        t2 = [e for e in J["edits"] if e.get("tier") == 2]
        page = load_live(slug, J["page"]["id"])
        live = page["content"]["rendered"]
        stale = [e["n"] for e in t2 if e["new"] not in live]
        assert not stale, (slug, "tier-2 'new' texts not live yet", stale)
        mod = importlib.import_module(modname)
        n_start = max(e["n"] for e in J["edits"]) + 1
        P = L.P3(slug, J, live, n_start)
        mod.build(P)
        t3 = P.edits
        if not t3:
            continue
        J["edits"].extend(t3)
        cs = J["claims_summary"]
        cs["edits"] = len(J["edits"])
        cs["tier3"] = len(t3)
        rules = [r for r in J["apply_rules"] if not r.startswith("Tier 3 under the CEO rule")]
        rules.append("Tier 3 under the CEO rule (7.10.2026): listing-site rents left in the body. Apply AFTER tier 1 and tier 2 (both are live on this page), on the live "
                     "content, in the listed order. ceo_action: replaced = the CBS value (table 4.9, Q2 2026) now stands there, with its source_url; removed = number gone, "
                     "sentence or cell kept; deleted = sentence, row, column or paragraph gone. Whole elements deleted with their tags (paragraph) carry the tags in 'old'.")
        J["apply_rules"] = rules
        J["tier3_ceo_recheck"] = {"retrieved_utc": page.get("retrieved_utc"), "modified": page.get("modified"),
                                  "result": "fetched 7.10.2026 with tier 1 and tier 2 live; every tier-3 'old' matches exactly once in the live content.rendered, in the order listed",
                                  "edits": len(t3), "replaced": sum(1 for e in t3 if e["ceo_action"] == "replaced"),
                                  "removed": sum(1 for e in t3 if e["ceo_action"] == "removed"),
                                  "deleted": sum(1 for e in t3 if e["ceo_action"] == "deleted")}
        out = json.dumps(J, ensure_ascii=False, indent=1) + "\n"
        if not DRY:
            io.open(path, "w", encoding="utf-8", newline="\n").write(out)
        c3 = J["tier3_ceo_recheck"]
        print(f"{slug}: {len(t3)} tier-3 edits (replaced {c3['replaced']}, removed {c3['removed']}, deleted {c3['deleted']}) {'dry' if DRY else 'written'}")
        for e in t3:
            summary.append((slug, e["n"], e["ceo_action"], e["ceo_note"], e.get("source_url")))
    print(len(summary), "tier-3 edits", {a: sum(1 for x in summary if x[2] == a) for a in ("replaced", "removed", "deleted")})


if __name__ == "__main__":
    main()
