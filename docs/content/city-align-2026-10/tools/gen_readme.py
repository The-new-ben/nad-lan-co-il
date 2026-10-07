# -*- coding: utf-8 -*-
"""Summarise docs/content/city-align-2026-10/*.align-edits.json into tables for the README (printed as Markdown).
python gen_readme.py [--live]   (--live re-fetches every page and repeats the dry run against the current public content)"""
import io, json, os, re, sys, glob
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import check
OUT = check.OUTDIR
LIVE13 = ["tel-aviv", "jerusalem", "haifa", "herzliya", "netanya", "ramat-gan", "bat-yam", "hod-hasharon", "ashdod", "petah-tikva",
          "ashkelon", "eilat", "kiryat-ono"]
OTHER11 = ["beer-sheva", "bnei-brak", "givatayim", "holon", "kfar-saba", "modiin", "raanana", "ramat-hasharon", "rehovot", "rishon-lezion"]
ORDER = [s + "-apartment-prices" for s in LIVE13] + [s + "-apartment-prices" for s in OTHER11] + ["apartment-prices"]
live = "--live" in sys.argv

rows, tot = [], {"C": 0, "X": 0, "S": 0, "Uk": 0, "Ue": 0, "edits": 0, "t1": 0, "t2": 0, "risky": 0, "tables": 0, "sus": 0, "figX": 0}
conf_lines, dry_lines, notes_lines = [], [], []
import contextlib
for slug in ORDER:
    fn = os.path.join(OUT, slug + ".align-edits.json")
    if not os.path.exists(fn):
        rows.append(f"| {slug} | missing | | | | | | | |")
        continue
    J = json.load(io.open(fn, encoding="utf-8"))
    with contextlib.redirect_stdout(io.StringIO()):
        R = check.main(slug, live=live, quiet=True, show=False)
    cl = J.get("claims", [])
    C = sum(1 for x in cl if x["verdict"] == "CONSISTENT")
    X = sum(1 for x in cl if x["verdict"] == "CONFLICT")
    S = sum(1 for x in cl if x["verdict"] == "STALE")
    Uk = sum(1 for x in cl if x["verdict"] == "UNSOURCED" and not x["action"].startswith("edit"))
    Ue = sum(1 for x in cl if x["verdict"] == "UNSOURCED" and x["action"].startswith("edit"))
    figX = sum(int(x.get("figures") or 1) for x in cl if x["verdict"] in ("CONFLICT", "STALE"))
    E = J["edits"]
    t1 = sum(1 for e in E if e.get("tier", 1) == 1)
    t2 = len(E) - t1
    tables = sum(1 for e in E if e.get("spans_tags"))
    ra = sum(1 for e in E if e.get("replace_all"))
    risky = len(R["risky"])
    errs = len(R["errs"])
    sus = len(R["sus"])
    live_flag = "yes" if J["page"].get("modified") and "nlpg" in R["page"]["content"]["rendered"] else "no"
    has_list = 'id="nlpg"' in R["page"]["content"]["rendered"]
    rows.append(f"| [{slug}]({J['page']['link']}) | {J['page']['id']} | {'yes' if has_list else 'not yet'} | {C} | {X} | {S} | {Uk} / {Ue} | "
                f"{len(E)} ({t1}/{t2}) | {tables} | {risky} | {'pass' if errs == 0 else 'FAIL ' + str(errs)} | {sus} |")
    for k, v in (("C", C), ("X", X), ("S", S), ("Uk", Uk), ("Ue", Ue), ("edits", len(E)), ("t1", t1), ("t2", t2), ("risky", risky),
                 ("tables", tables), ("sus", sus), ("figX", figX)):
        tot[k] += v
    # top conflicts: sale-type conflicts first
    cx = [x for x in cl if x["verdict"] in ("CONFLICT", "STALE")]
    cx.sort(key=lambda x: (0 if x["measure"] in ("sale", "sale_avg") else 1))
    if cx:
        conf_lines.append(f"- **{slug}**: " + "; ".join(f"\"{x['quote'][:90]}\" ({x['verdict'].lower()}, official {x.get('official') or 'n/a'})" for x in cx[:3]))
    dry_lines.append((slug, len(E), ra, tables, risky, errs, R["errs"][:3], R["page"].get("retrieved_utc"), R["page"].get("modified")))
    if J.get("notes"):
        notes_lines.append(f"- **{slug}**: {J['notes']}")

print("| page | id | list on page | CONSISTENT | CONFLICT | STALE | UNSOURCED kept / edited | edits (tier 1/2) | whole-table edits | olds with risky chars | dry run | remaining suspects |")
print("|---|---|---|---|---|---|---|---|---|---|---|---|")
print("\n".join(rows))
print(f"| **total** | | | {tot['C']} | {tot['X']} | {tot['S']} | {tot['Uk']} / {tot['Ue']} | {tot['edits']} ({tot['t1']}/{tot['t2']}) | {tot['tables']} | {tot['risky']} | | {tot['sus']} |")
print()
print("TOP")
print("\n".join(conf_lines))
print()
print("DRY")
for d in dry_lines:
    print(d)
print()
print("NOTES")
print("\n".join(notes_lines))
print("FIGURES in conflict/stale:", tot["figX"])
