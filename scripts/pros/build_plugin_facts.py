# -*- coding: utf-8 -*-
"""ProNetwork v98: the register facts the site shows, for the contractors in our directory only (plugins/nadlan-config/data/
register-facts.json), from scripts/pros/data/register-facts.json (build_register_facts.py) and the directory's contractors
(public REST: their registry numbers). Per contractor: y = registered since (year), b = up to three branches [branch,
group-classification, unlimited scope 1/0] the highest classification first, r = recognised for government work, co = a
company. Nothing else: no phones, e-mails, addresses or employees.
  python scripts/pros/build_plugin_facts.py"""
import io, json, os, sys, time, urllib.request
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
SRC = os.path.join(REPO, "scripts", "pros", "data", "register-facts.json")
OUT = os.path.join(REPO, "plugins", "nadlan-config", "data", "register-facts.json")
os.makedirs(os.path.dirname(OUT), exist_ok=True)
ORDER = "אבגדה"


def rank(c):
    g, _, n = c.partition("-")
    return (ORDER.index(g) if g in ORDER else -1, int(n) if n.isdigit() else 0)


def ours():
    nums, page = set(), 1
    while True:
        url = "https://nad-lan.co.il/wp-json/wp/v2/nadlan_professional?per_page=100&page=%d&_fields=meta" % page
        try:
            d = json.load(urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": "NadLan-facts/1.0"}), timeout=60))
        except Exception:
            break
        if not d:
            break
        for p in d:
            m = p.get("meta") or {}
            if m.get("profession") == "kablan" and m.get("registry_number"):
                nums.add(str(m["registry_number"]))
        page += 1
    return nums


def main():
    src = json.load(io.open(SRC, encoding="utf-8"))
    facts, nums = src["facts"], ours()
    out = {}
    for k in sorted(nums):
        f = facts.get(k)
        if not f:
            continue
        br = sorted(f["branches"], key=lambda b: rank(b["c"]), reverse=True)[:3]
        e = {"b": [[b["b"].replace("  ", " "), b["c"], 1 if b["s"] == "ב.מ." else 0] for b in br]}
        if f.get("since"):
            e["y"] = f["since"]
        if f.get("recognised"):
            e["r"] = 1
        if f.get("company"):
            e["co"] = 1
        out[k] = e
    io.open(OUT, "w", encoding="utf-8", newline="\n").write(json.dumps({"src": src["source"], "f": out}, ensure_ascii=False, separators=(",", ":")))
    print("directory contractors", len(nums), "with facts", len(out), "bytes", os.path.getsize(OUT))


if __name__ == "__main__":
    main()
