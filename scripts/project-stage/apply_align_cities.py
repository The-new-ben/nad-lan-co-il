# -*- coding: utf-8 -*-
"""HAD-460: the body numbers of the 24 city price pages aligned with the official price lists now on them (the CEO's approval,
7.10.2026: read first, a sourced edit list, then the fix with backups; titles and H1s untouched). Edits:
docs/content/city-align-2026-10/<slug>.align-edits.json (the audit: README.md there). Tier 1 = sale prices that contradict the
official medians or have no source; tier 2 = unsourced rent/percent/renovation figures (applied only with --tier 2).
Rules per page (all or nothing): each "old" must match the RAW content exactly once (replace_all: exactly expect_matches times);
a whole-table edit ("spans_tags") that does not match raw is applied to the one <table> element holding its "anchor" cell.
The H1 and the page title must be identical after the edits. Backup before, read-back after.
App password in-process, never printed.
python apply_align_cities.py <slug>|--all [--tier 2] [--dry]      python apply_align_cities.py --rollback <backup.json>"""
import glob
import io
import json
import os
import re
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(HERE))
DIR = os.path.join(REPO, "docs", "content", "city-align-2026-10")
BK = os.path.join(REPO, "docs", "qa", "had-460", "city-align-backup")
ARGS = sys.argv[1:]
TIER = int(ARGS[ARGS.index("--tier") + 1]) if "--tier" in ARGS else 1
src = open(os.path.join(REPO, "scripts", "skin-a", "deployskin.py"), encoding="utf-8").read()
ns = {"__name__": "aligncity"}
exec(compile(src[:src.index('s, h, _ = req("GET", "/wp-json/nadlan/v1/health")')], "deployskin-helpers", "exec"), ns)
req = ns["req"]
T = lambda v: str(v).lower() in ("true", "1", "yes")


def get(pid):
    s, b, _ = req("GET", f"/wp-json/wp/v2/pages/{pid}?context=edit&_fields=id,link,title,content,modified")
    if s != 200:
        raise SystemExit(f"FATAL read {pid}: {s}")
    return b


def h1(raw):
    m = re.search(r"<h1\b[^>]*>(.*?)</h1>", raw, re.S)
    return m.group(1).strip() if m else ""


if "--rollback" in ARGS:
    bk = json.load(io.open(ARGS[ARGS.index("--rollback") + 1], encoding="utf-8"))
    s, r, _ = req("POST", f"/wp-json/wp/v2/pages/{bk['id']}", {"content": bk["content"]})
    print("[rollback]", bk["id"], s, "identical:", get(bk["id"])["content"]["raw"] == bk["content"])
    raise SystemExit(0)

files = sorted(glob.glob(os.path.join(DIR, "*.align-edits.json")))
# --file <path>: one edits file elsewhere (the New North hub: docs/content/north-tel-aviv-2026-10/align-edits.json)
if "--file" in ARGS:
    files = [os.path.abspath(ARGS[ARGS.index("--file") + 1])]
want = [a for a in ARGS if not a.startswith("--") and not a.isdigit() and not a.endswith(".json")]
if "--all" not in ARGS and "--file" not in ARGS:
    files = [f for f in files if os.path.basename(f).split(".")[0] in want]
os.makedirs(BK, exist_ok=True)
stamp = time.strftime("%Y%m%dT%H%M%S")
tot = {"pages": 0, "edits": 0, "skipped": []}
for f in files:
    slug = os.path.basename(f).split(".")[0]
    d = json.load(io.open(f, encoding="utf-8"))
    # --only: exactly this tier (tier 2 after tier 1 is live: the tier-1 "old" strings no longer exist)
    edits = sorted([e for e in d["edits"] if (int(e.get("tier", 1)) == TIER if "--only" in ARGS else int(e.get("tier", 1)) <= TIER)], key=lambda e: int(e["n"]))
    if not edits:
        print(f"[{slug}] no tier<={TIER} edits"); continue
    pid = int(edits[0]["page_id"])
    b = get(pid)
    raw, title = b["content"]["raw"], b["title"]["raw"]
    new, bad = raw, []
    for e in edits:
        old, rep = e["old"], e["new"]
        c = new.count(old)
        if T(e.get("replace_all")):
            if c != int(e.get("expect_matches", 2)):
                bad.append((e["n"], c)); continue
            new = new.replace(old, rep)
        elif c == 1:
            new = new.replace(old, rep)
        elif c == 0 and T(e.get("spans_tags")) and e.get("anchor"):
            k = new.count(e["anchor"])
            i = new.find(e["anchor"])
            a, z = new.rfind("<table", 0, i), new.find("</table>", i)
            if k != 1 or a < 0 or z < 0 or new.find("</table>", a) != z:
                bad.append((e["n"], "anchor x%d" % k)); continue
            new = new[:a] + rep + new[z + len("</table>"):]
        else:
            bad.append((e["n"], c))
    if bad:
        print(f"[{slug}] page {pid}: {len(edits)} edits, {len(bad)} not matching {bad[:6]}: nothing written")
        tot["skipped"].append(slug); continue
    if h1(new) != h1(raw):
        print(f"[{slug}] the H1 would change: nothing written"); tot["skipped"].append(slug); continue
    print(f"[{slug}] page {pid}: {len(edits)} tier<={TIER} edits match; {len(raw):,} -> {len(new):,} chars")
    if "--dry" in ARGS:
        continue
    bkp = os.path.join(BK, f"page-{pid}-{stamp}.json")
    io.open(bkp, "w", encoding="utf-8").write(json.dumps({"id": pid, "slug": slug, "content": raw, "title": title, "modified": b["modified"]}, ensure_ascii=False))
    s, r, _ = req("POST", f"/wp-json/wp/v2/pages/{pid}", {"content": new})
    a = get(pid)
    ok = s == 200 and a["content"]["raw"] == new and a["title"]["raw"] == title
    print(f"   written {s}, read-back identical {a['content']['raw'] == new}, title unchanged {a['title']['raw'] == title}; backup {os.path.relpath(bkp, REPO)}")
    if not ok:
        print("   [rollback]", req("POST", f"/wp-json/wp/v2/pages/{pid}", {"content": raw})[0]); tot["skipped"].append(slug); continue
    tot["pages"] += 1; tot["edits"] += len(edits)
print("[done]", tot)
