# -*- coding: utf-8 -*-
"""HAD-642, Ben 31.10.2026 night ("תבטל את החוק הזה ... תמשוך מהמאגר, תוסיף את העמודים האלה"): refresh the urban-renewal
compounds from the government registry (data.gov.il resource f65a0daf) through the site's own importer, POST
/nadlan/v1/import-run {which: urban}. It upserts by the registry key: an existing compound gets its status, units, plan,
track and year from the file; a compound the file has and the site lacks becomes a new page. An enriched compound (Gefen 8-10)
keeps its title and content.
Safety: a full snapshot of every project post (status, title, the registry meta) BEFORE, the same AFTER, and a diff.
A post that was not public before and the importer made public is put back to its old status (nothing that was hidden on
purpose comes back). Nothing is deleted: compounds that left the registry stay as they are.
Output: docs/qa/registry-2026-10-31/{before,after,diff}.json."""
import json, os, sys, time
H = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.dirname(os.path.dirname(H))
sys.path.insert(0, H); os.chdir(REPO)
src = open(os.path.join(H, "deploy544.py"), encoding="utf-8").read()
_ARGV = list(sys.argv)
sys.argv = ["deploy544.py", "--finish"]
ns = {"__name__": "registry", "__file__": os.path.join(H, "deploy544.py")}
exec(compile(src[:src.index("def page(path):")], "deploy544", "exec"), ns)
req, must = ns["req"], ns["must"]
OUT = os.path.join(REPO, "docs", "qa", "registry-2026-10-31"); os.makedirs(OUT, exist_ok=True)
KEYS = ("source", "source_id", "project_status", "num_units", "units_existing", "units_added", "plan_number", "renewal_track",
        "completion_year", "city", "data_quality")


def snapshot(tag):
    rows, page = {}, 1
    while True:
        for _try in range(4):  # the host answers 502 now and then on a heavy page: a short pause and again
            s, d = req("GET", f"/wp-json/wp/v2/nadlan_project?status=publish,draft,pending,private,future&per_page=40&page={page}&context=edit&_fields=id,slug,status,title,meta", timeout=180)
            if s not in (502, 503, 504):
                break
            time.sleep(6)
        if s == 400 and page > 1:
            break
        must(s, d, f"list page {page}")
        if not d:
            break
        for p in d:
            m = p.get("meta") or {}
            rows[str(p["id"])] = {"slug": p["slug"], "status": p["status"], "title": (p.get("title") or {}).get("raw", ""),
                                  **{k: m.get(k, "") for k in KEYS}}
        if len(d) < 40:
            break
        page += 1
    json.dump(rows, open(os.path.join(OUT, tag + ".json"), "w", encoding="utf-8"), ensure_ascii=False, indent=0)
    urb = [r for r in rows.values() if r["source"] == "urban_renewal"]
    by = {}
    for r in urb:
        by[r["status"]] = by.get(r["status"], 0) + 1
    print(f"[{tag}] {len(rows)} project posts, {len(urb)} from the registry, by status {by}")
    return rows


CONT = "--continue" in _ARGV[1:] or "--after" in _ARGV[1:]
if CONT:  # a call was cut by the gateway: the BEFORE snapshot on disk stays the reference; the cursor goes on (no reset)
    before = json.load(open(os.path.join(OUT, "before.json"), encoding="utf-8"))
    print(f"[before] from disk: {len(before)} project posts")
else:
    before = snapshot("before")
done, calls = "--after" in _ARGV[1:], 0
def total():
    import urllib.request
    r = urllib.request.Request(ns["BASE"] + "/wp-json/wp/v2/nadlan_project?per_page=1&status=publish,draft,pending,private,future&context=edit&_fields=id",
                               headers={"Authorization": ns["AUTH"], "User-Agent": ns["UA"]})
    with urllib.request.urlopen(r, timeout=120) as resp:
        return int(resp.headers.get("X-WP-Total"))


while not done and calls < 8:
    calls += 1
    s, d = req("POST", "/wp-json/nadlan/v1/import-run", {"which": "urban", "batches": 1, "reset": (calls == 1 and not CONT)}, timeout=600)
    if s in (502, 503, 504):  # the gateway gave up; PHP goes on until it ends or the host stops it: wait until the count is still
        print(f"[import] call {calls}: gateway {s}; waiting for the server to settle", flush=True)
        last, still = None, 0
        while still < 3:
            time.sleep(60)
            n = total()
            still = still + 1 if n == last else 0
            last = n
            print(f"         {time.strftime('%H:%M:%S')} project posts {n}", flush=True)
        continue
    must(s, d, f"import-run call {calls}")
    print(f"[import] call {calls}: {d}", flush=True)
    done = bool(d.get("done"))
    time.sleep(2)
after = snapshot("after")
new = [i for i in after if i not in before]
hidden_now_public = [i for i in before if before[i]["source"] == "urban_renewal" and before[i]["status"] != "publish" and after.get(i, {}).get("status") == "publish"]
restored = []
for i in hidden_now_public:
    s, d = req("POST", f"/wp-json/wp/v2/nadlan_project/{i}", {"status": before[i]["status"]})
    restored.append({"id": i, "slug": before[i]["slug"], "back_to": before[i]["status"], "http": s})
changed = {k: 0 for k in KEYS if k not in ("source", "source_id")}
titles = []
for i, b in before.items():
    a = after.get(i)
    if not a or b["source"] != "urban_renewal":
        continue
    for k in changed:
        if str(a.get(k, "")) != str(b.get(k, "")):
            changed[k] += 1
    if a["title"] != b["title"]:
        titles.append({"id": i, "before": b["title"], "after": a["title"]})
diff = {"new": [{"id": i, "slug": after[i]["slug"], "title": after[i]["title"], "city": after[i]["city"], "status": after[i]["project_status"]} for i in new],
        "restored_status": restored, "fields_changed": changed, "titles_changed": titles}
json.dump(diff, open(os.path.join(OUT, "diff.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(f"[diff] new pages {len(new)}, restored {len(restored)}, fields changed {changed}, titles changed {len(titles)}")
for t in titles[:10]:
    print("   title:", t["before"], "->", t["after"])
