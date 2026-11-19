"""Bill of materials of a rented home (HAD-795): validate tree/*.json, write BOM.md, counts.json, bom.min.json.

Usage:
  python docs/rentals/bom/build_bom.py            # validate all, write outputs
  python docs/rentals/bom/build_bom.py --check tree/06-maintenance.json   # validate one file only
"""
import json, re, sys, glob, os, collections

HERE = os.path.dirname(os.path.abspath(__file__))
WHO = {"landlord", "tenant", "both", "professional", "authority", "house-committee"}
STATUS = {"works", "partly", "missing"}
DASH = re.compile("[–—]")
ID = re.compile(r"^\d{2}(\.\d{2})*$")


LANGS = ["he", "en", "fr", "ru", "ar"]
# The product's string tables today (checked 20.11.2026): v2 assets/rentals/i18n/{he,en}.json, v1 he/en inline.
PRODUCT_LANGS = {"he", "en"}


def lang_missing(n):
    """Which language pages lack this leaf today: all five when the product lacks it, else those without a string table."""
    st = (n.get("product_today") or {}).get("status")
    if st == "missing":
        return list(LANGS)
    return [l for l in LANGS if l not in PRODUCT_LANGS]


def check(path):
    errs, warns = [], []
    try:
        nodes = json.load(open(path, encoding="utf-8"))
    except Exception as e:  # noqa
        return None, ["%s: not valid JSON: %s" % (path, e)], []
    if not isinstance(nodes, list):
        return None, ["%s: top level must be an array" % path], []
    ids = set()
    branch_prefix = os.path.basename(path)[:2]
    for i, n in enumerate(nodes):
        where = "%s[%d] %s" % (os.path.basename(path), i, n.get("id"))
        nid = n.get("id", "")
        if not ID.match(str(nid)):
            errs.append(where + ": bad id")
            continue
        if not nid.startswith(branch_prefix):
            errs.append(where + ": id outside this branch")
        if nid in ids:
            errs.append(where + ": duplicate id")
        ids.add(nid)
        parent = nid.rsplit(".", 1)[0] if "." in nid else None
        if parent and parent not in ids:
            errs.append(where + ": parent %s missing or after child" % parent)
        if n.get("kind") not in ("branch", "leaf"):
            errs.append(where + ": kind")
        t = n.get("title") or {}
        if not t.get("he") or not t.get("en"):
            errs.append(where + ": title he/en")
        if not n.get("what"):
            errs.append(where + ": what")
        who = n.get("who") or []
        if not who or any(w not in WHO for w in who):
            errs.append(where + ": who %r" % who)
        pt = n.get("product_today") or {}
        if pt.get("status") not in STATUS:
            errs.append(where + ": product_today.status")
        for law in n.get("law") or []:
            for k in ("source", "section", "url", "read_on"):
                if not law.get(k):
                    errs.append(where + ": law.%s" % k)
            if law.get("url") and re.search(r"kolzchut|lawoffice|\.law\b|lawyer", law["url"], re.I):
                warns.append(where + ": law cites a secondary site " + law["url"])
        if n.get("kind") == "leaf":
            th = n.get("thumb") or {}
            if not th.get("he") or not th.get("en"):
                errs.append(where + ": leaf without thumb he/en")
        blob = json.dumps(n, ensure_ascii=False)
        if DASH.search(blob):
            errs.append(where + ": long dash")
    # every branch must have a child
    for n in nodes:
        if n.get("kind") == "branch" and not any(m["id"].startswith(n["id"] + ".") for m in nodes if isinstance(m.get("id"), str)):
            warns.append("%s: branch %s has no children" % (os.path.basename(path), n.get("id")))
    return nodes, errs, warns


def main():
    args = sys.argv[1:]
    files = [os.path.join(HERE, args[1])] if args[:1] == ["--check"] else sorted(glob.glob(os.path.join(HERE, "tree", "*.json")))
    allnodes, bad = [], 0
    for f in files:
        nodes, errs, warns = check(f)
        for e in errs:
            print("ERROR", e)
        for w in warns:
            print("WARN ", w)
        bad += len(errs)
        if nodes:
            allnodes += nodes
    leaves = [n for n in allnodes if n.get("kind") == "leaf"]
    for n in leaves:
        n["lang_missing"] = lang_missing(n)
    lgap = collections.Counter(l for n in leaves for l in n["lang_missing"])
    st = collections.Counter((n.get("product_today") or {}).get("status") for n in leaves)
    withlaw = sum(1 for n in allnodes if n.get("law"))
    print("nodes %d, leaves %d, product works %d / partly %d / missing %d, nodes with a primary legal source %d"
          % (len(allnodes), len(leaves), st["works"], st["partly"], st["missing"], withlaw))
    if args[:1] == ["--check"]:
        sys.exit(1 if bad else 0)
    # outputs
    per = collections.OrderedDict()
    for n in allnodes:
        b = n["id"][:2]
        p = per.setdefault(b, {"nodes": 0, "leaves": 0, "works": 0, "partly": 0, "missing": 0, "law": 0})
        p["nodes"] += 1
        if n.get("law"):
            p["law"] += 1
        if n.get("kind") == "leaf":
            p["leaves"] += 1
            p[(n.get("product_today") or {}).get("status", "missing")] += 1
    json.dump({"total": {"nodes": len(allnodes), "leaves": len(leaves), **dict(st), "law": withlaw},
               "leaves_missing_per_language": {l: lgap[l] for l in LANGS}, "branches": per},
              open(os.path.join(HERE, "counts.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    # a slim copy for the product (titles, who, when, thumb, status, law refs)
    slim = [{k: n.get(k) for k in ("id", "kind", "title", "who", "when", "proof", "thumb", "product_today", "lang_missing")} |
            {"law": [{"source": l.get("source"), "section": l.get("section"), "url": l.get("url")} for l in (n.get("law") or [])]}
            for n in allnodes]
    json.dump(slim, open(os.path.join(HERE, "bom.min.json"), "w", encoding="utf-8"), ensure_ascii=False, separators=(",", ":"))
    out = ["# The bill of materials of a rented home in Israel", "",
           "Generated by build_bom.py from tree/*.json. Do not edit by hand.", "",
           "Totals: %d nodes, %d one-tap leaves. Product today on the leaves: works %d, partly %d, missing %d. Nodes resting on a primary legal source: %d."
           % (len(allnodes), len(leaves), st["works"], st["partly"], st["missing"], withlaw), "",
           "Leaves missing per language page today: " + ", ".join("%s %d" % (l, lgap[l]) for l in LANGS) + ".", "",
           "| Branch | Nodes | Leaves | Works | Partly | Missing | With law |", "|---|---|---|---|---|---|---|"]
    for b, p in per.items():
        out.append("| %s | %d | %d | %d | %d | %d | %d |" % (b, p["nodes"], p["leaves"], p["works"], p["partly"], p["missing"], p["law"]))
    out.append("")
    mark = {"works": "[x]", "partly": "[~]", "missing": "[ ]"}
    for n in allnodes:
        depth = n["id"].count(".")
        t = n["title"]
        pt = (n.get("product_today") or {}).get("status", "missing")
        if n["kind"] == "branch" and depth == 0:
            out += ["", "## %s %s / %s" % (n["id"], t["he"], t["en"]), "", n.get("what", ""), ""]
            continue
        line = "%s- %s **%s** %s / %s" % ("  " * (depth - 1), mark[pt] if n["kind"] == "leaf" else "", n["id"], t["he"], t["en"])
        bits = []
        if n.get("who"):
            bits.append("who: " + ", ".join(n["who"]))
        if n.get("when"):
            bits.append("when: " + n["when"])
        if n.get("law"):
            bits.append("law: " + "; ".join("%s %s" % (l["source"], l["section"]) for l in n["law"]))
        if n["kind"] == "leaf" and n.get("thumb"):
            bits.append("tap: " + n["thumb"]["he"])
        if n["kind"] == "leaf" and n.get("lang_missing"):
            bits.append("missing in: " + ",".join(n["lang_missing"]))
        out.append(line + ("  \n" + "  " * depth + "  " + " · ".join(bits) if bits else ""))
    open(os.path.join(HERE, "BOM.md"), "w", encoding="utf-8").write("\n".join(out) + "\n")
    print("wrote BOM.md, counts.json, bom.min.json")
    sys.exit(1 if bad else 0)


if __name__ == "__main__":
    main()
