# -*- coding: utf-8 -*-
"""Validate docs/content/city-align-2026-10/<slug>.align-edits.json against the page's public content.rendered.
python check.py <slug> [--live] [--quiet]
Checks: schema; sequential match (each old exactly once, or expect_matches with replace_all; spans_tags via anchor);
matches outside script/style/nlpg; risky characters in old (raw may differ); new-text rules; every number in new
traced to the city JSON or to the old text; source_keys resolve; heuristic scan for remaining per-room conflicts."""
import json, os, re, sys, time, urllib.request, urllib.parse
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from blocks import strip_ranges, blocks
REPO = r"C:\Users\777\nad-lan\nad-lan-co-il"
OUTDIR = os.path.join(REPO, "docs", "content", "city-align-2026-10")
CITIES = os.path.join(REPO, "scripts", "project-stage", "price_guide", "cities")
NEWSPAPERS = ["גלובס", "כלכליסט", "דה מרקר", "דהמרקר", "ynet", "וואלה", "מעריב", "הארץ", "ביזפורטל", "bizportal", "מרכז הנדל",
              "ידיעות", "N12", "mako", "themarker", "calcalist", "globes"]
PORTALS = ["מדדירות", "דירובוט", "יד2", "יד 2", "madlan", "מדלן", "הומלס", "onmap", "אונמפ", "נדלן נט"]
RISKY = {'"': "straight double quote (texturize could curl it)", "'": "apostrophe/geresh (texturize could curl it)",
         "\u2013": "en dash", "\u2014": "em dash", "...": "three dots (texturize -> ellipsis)", "--": "double hyphen (texturize -> dash)",
         " - ": "spaced hyphen (texturize -> en dash)", "\n": "line break (wpautop)", "&": "ampersand/entity", "  ": "double space"}


def load_page(slug, live=False):
    if live:
        u = "https://nad-lan.co.il/wp-json/wp/v2/pages?slug=%s&_fields=id,link,title,content,modified&nlca=%d" % (urllib.parse.quote(slug), time.time())
        p = json.loads(urllib.request.urlopen(urllib.request.Request(u, headers={"User-Agent": "Mozilla/5.0 NadLan-cityalign"}), timeout=90).read().decode("utf-8"))[0]
        p["retrieved_utc"] = time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())
        return p
    return json.load(open(os.path.join(HERE, "pages", slug + ".json"), encoding="utf-8"))


def cbs_official_numbers():
    """CBS table 4.9 (average monthly rent, Q2 2026) rounded half up and with one decimal, plus the CBS dwelling share (tools/cbs_rent_2026_q2.json)"""
    fn = os.path.join(HERE, "cbs_rent_2026_q2.json")
    if not os.path.exists(fn):
        return set()
    from decimal import Decimal, ROUND_HALF_UP
    J = json.load(open(fn, encoding="utf-8"))
    out = set()
    for r in J["rows"].values():
        for v in [r["total"]] + list(r["groups"].values()):
            if v is not None:
                out.add(f"{int(Decimal(str(v)).quantize(Decimal('1'), rounding=ROUND_HALF_UP)):,}")
                out.add(f"{v:,.1f}")
    out.add(str(J["dwellings_share"]["tel_aviv_district_pct"]))
    return out


def official_numbers(d):
    vals = cbs_official_numbers()

    def add(v):
        if v is None:
            return
        if isinstance(v, float) and abs(v) < 100:
            a = abs(v)
            vals.add(f"{a:g}")
            vals.add(f"{a:.1f}")
            if a == int(a):
                vals.add(str(int(a)))
            return
        v = int(v)
        vals.add(f"{v:,}")
        vals.add(str(v))
        mm = v / 1e6
        for nd in (1, 2, 3):
            s = f"{mm:.{nd}f}"
            vals.add(s)
            vals.add(s.rstrip("0").rstrip("."))
        if v < 1e6:
            vals.add(f"{round(v / 1000):,}")

    for k, r in d["rooms"].items():
        for f in ("latest", "year_ago"):
            add(r.get(f))
        if r.get("change_pct") is not None:
            add(float(r["change_pct"]))
        for q, v in r.get("quarters", []):
            add(v)
    for key in ("israel", "israel_latest"):
        for k, v in (d.get(key) or {}).items():
            if k != "quarter":
                add(v)
    for n in d.get("neighbourhoods") or []:
        for v in n["rooms"].values():
            add(v)
    for c in d.get("cities") or []:
        for k, r in c["rooms"].items():
            add(r.get("latest"))
            if r.get("change_pct") is not None:
                add(float(r["change_pct"]))
    return vals


def resolve_key(d, key):
    """rooms.3.latest | rooms.3.year_ago | rooms.3.change_pct | rooms.3.quarters[10-12.2025] | israel.4 | israel_latest.4 |
    neighbourhoods[name].rooms.4 | cities[slug].rooms.3.latest | page (a number kept from the page itself) | data_quarter"""
    if key in ("page", "data_quarter", "src_line") or key.startswith("page:"):
        return True
    if key.startswith("cbs_rent[") or key.startswith("cbs_dwellings["):
        J = json.load(open(os.path.join(HERE, "cbs_rent_2026_q2.json"), encoding="utf-8"))
        m = re.fullmatch(r"cbs_rent\[(.+?)\]\.(total|1-2|2\.5-3|3\.5-4|4\.5\+)\.q2_2026", key)
        if m and m.group(1) in J["rows"]:
            r = J["rows"][m.group(1)]
            return (r["total"] if m.group(2) == "total" else r["groups"].get(m.group(2))) is not None
        return key == "cbs_dwellings[מחוז תל אביב].share_2025"
    m = re.fullmatch(r"rooms\.(3|4|5|all)\.(latest|year_ago|change_pct|quarter)", key)
    if m:
        return d["rooms"][m.group(1)].get(m.group(2)) is not None
    m = re.fullmatch(r"rooms\.(3|4|5|all)\.quarters\[([\d\-\.]+)\]", key)
    if m:
        return any(q == m.group(2) and v is not None for q, v in d["rooms"][m.group(1)]["quarters"])
    m = re.fullmatch(r"(israel|israel_latest)\.(3|4|5|all|quarter)", key)
    if m:
        return (d.get(m.group(1)) or {}).get(m.group(2)) is not None
    m = re.fullmatch(r"neighbourhoods\[(.+?)\]\.rooms\.(3|4|5)", key)
    if m:
        return any(n["name"] == m.group(1) and n["rooms"].get(m.group(2)) is not None for n in d.get("neighbourhoods") or [])
    m = re.fullmatch(r"cities\[(.+?)\]\.rooms\.(3|4|5|all)\.(latest|change_pct|quarter)", key)
    if m:
        return any(c["slug"] == m.group(1) and c["rooms"][m.group(2)].get(m.group(3)) is not None for c in d.get("cities") or [])
    m = re.fullmatch(r"sources\[(\d+)\]", key)
    if m:
        return int(m.group(1)) < len(d.get("sources") or [])
    return False


NUM = re.compile(r"(?<![\w\d])\d[\d,]*(?:\.\d+)?")


def numbers_in(s):
    return [x.rstrip(",.") for x in NUM.findall(s)]


RANGE_M = re.compile(r"(\d+(?:\.\d+)?)\s*(?:-|\u2013|עד|ל-)\s*(\d+(?:\.\d+)?)\s*מיליון")
ONE_M = re.compile(r"(?<![\d\.])(\d+(?:\.\d+)?)\s*מיליון")
RANGE_N = re.compile(r"(\d{1,3}(?:,\d{3}){1,2})\s*(?:-|\u2013|עד|ל-)\s*(\d{1,3}(?:,\d{3}){1,2})")
ONE_N = re.compile(r"(?<![\d,])(\d{1,3}(?:,\d{3}){1,2})(?![\d,])")
ROOMS = re.compile("(?<![\\d.])([2-6])\\s*(?:\u05d7\u05d3\u05e8\u05d9\u05dd|\u05d7\u05d3')")


def money_values(seg):
    out, used = [], []
    for m in RANGE_M.finditer(seg):
        out.append(("range", float(m.group(1)) * 1e6, float(m.group(2)) * 1e6, m.group(0)))
        used.append(m.span())
    for m in ONE_M.finditer(seg):
        if any(a <= m.start() < b for a, b in used):
            continue
        out.append(("point", float(m.group(1)) * 1e6, None, m.group(0)))
        used.append(m.span())
    for m in RANGE_N.finditer(seg):
        if any(a <= m.start() < b for a, b in used):
            continue
        a, b = int(m.group(1).replace(",", "")), int(m.group(2).replace(",", ""))
        if a >= 300000:
            out.append(("range", a, b, m.group(0)))
            used.append(m.span())
    for m in ONE_N.finditer(seg):
        if any(a <= m.start() < b for a, b in used):
            continue
        v = int(m.group(1).replace(",", ""))
        tail = seg[m.end():m.end() + 14]
        if v >= 300000 and "למ" not in tail:
            out.append(("point", v, None, m.group(0)))
    return out


def scan_remaining(text_blocks, d, offs=None):
    offs = offs or set()
    sus = []
    for b in text_blocks:
        segs = re.split(r"(?<=[\.;:])\s+", b["text"]) if b["tag"] != "tr" else [b["text"]]
        for seg in segs:
            rooms = set(ROOMS.findall(seg))
            if len(rooms) != 1:
                continue
            k = rooms.pop()
            if k not in ("3", "4", "5"):
                continue
            if re.search(r"שכיר|שכר דירה|לחודש|בחודש", seg):
                continue
            off = d["rooms"][k]["latest"]
            for kind, a, bnd, raw in money_values(seg):
                if ("," in raw and raw.strip() in offs) or ("מיליון" in raw and "חציון" in seg):
                    continue
                if kind == "range":
                    ok = a * 0.99 <= off <= bnd * 1.01
                else:
                    ok = abs(a - off) / off <= 0.05
                if not ok and a > 300000:
                    sus.append((b["tag"] + "@" + str(b["start"]), k, raw, f"{off:,}", seg[:170]))
    return sus


def apply_edit(text, e):
    """returns (new_text, count, note)"""
    if e.get("spans_tags"):
        anc = e.get("anchor", "")
        if not anc or text.count(anc) != 1:
            return text, -1, f"anchor found {text.count(anc) if anc else 0} times"
        i = text.find(anc)
        a, z = text.rfind("<table", 0, i), text.find("</table>", i)
        if a < 0 or z < 0:
            return text, -1, "table not found around anchor"
        c_old = text.count(e["old"])
        return text[:a] + e["new"] + text[z + len("</table>"):], 1, f"table element replaced via anchor (old string itself matches {c_old}x)"
    c = text.count(e["old"])
    if e.get("replace_all"):
        if c != int(e.get("expect_matches", 2)):
            return text, c, f"replace_all expected {e.get('expect_matches')} got {c}"
        return text.replace(e["old"], e["new"]), c, ""
    if c != 1:
        return text, c, f"matches {c}"
    return text.replace(e["old"], e["new"]), c, ""


def main(slug, live=False, quiet=False, show=True):
    fn = os.path.join(OUTDIR, slug + ".align-edits.json")
    d = json.load(open(os.path.join(CITIES, slug + ".json"), encoding="utf-8"))
    p = load_page(slug, live)
    c0 = p["content"]["rendered"]
    rng = strip_ranges(c0)
    J = json.load(open(fn, encoding="utf-8")) if os.path.exists(fn) else {"edits": []}
    edits = sorted(J.get("edits", []), key=lambda e: e["n"])
    offs = official_numbers(d)
    errs, warns, risky_list = [], [], []
    ns = [e["n"] for e in edits]
    if ns != list(range(1, len(ns) + 1)):
        errs.append(f"edit numbers not 1..N: {ns[:10]}...")
    text = c0
    for e in edits:
        n = e["n"]
        for f in ("page_id", "field", "old", "new", "source_keys", "audit_verdict", "why"):
            if f not in e:
                errs.append(f"#{n} missing field {f}")
        if e.get("page_id") != p["id"]:
            errs.append(f"#{n} page_id {e.get('page_id')} != {p['id']}")
        if e.get("field", "content") != "content":
            errs.append(f"#{n} field {e.get('field')}")
        if e.get("verdict", e.get("audit_verdict")) not in ("CONFLICT", "STALE", "UNSOURCED", "CONSISTENT", "WORDING"):
            errs.append(f"#{n} verdict {e.get('verdict')}")
        old, new = e.get("old", ""), e.get("new", "")
        if not e.get("spans_tags"):
            for m in re.finditer(re.escape(old), c0):
                for s0, e0, kind in rng:
                    if s0 <= m.start() < e0:
                        errs.append(f"#{n} old matches inside {kind} at {m.start()}")
        text2, cnt, note = apply_edit(text, e)
        if cnt == -1 or (note and not e.get("spans_tags")):
            errs.append(f"#{n} {note}: {old[:80]!r}")
        elif note:
            warns.append(f"#{n} {note}")
        text = text2
        rk = [why for ch, why in RISKY.items() if ch in old]
        if e.get("spans_tags"):
            rk.append("spans tags (whole table; apply via anchor)")
        elif "<" in old:
            rk.append("contains tags")
        if rk:
            risky_list.append((n, rk))
        for bad in ("\u2014", "\u2013", "!", "&#", "&quot;", "&amp;", "&nbsp;"):
            if bad in new:
                errs.append(f"#{n} new contains {bad!r}")
        low = re.sub(r"(בכל|ברחבי|רחבי|כל) הארץ", " ", new.lower())
        for w in NEWSPAPERS:
            if (w.lower() in low) and not (w.lower() in old.lower()):
                errs.append(f"#{n} new names a newspaper/site: {w}")
        if re.search(r"(?<![a-z])ice(?![a-z])", low) and not re.search(r"(?<![a-z])ice(?![a-z])", old.lower()):
            errs.append(f"#{n} new names a newspaper/site: ice")
        for w in PORTALS:
            if w in new and w not in old:
                warns.append(f"#{n} new adds a portal name: {w}")
        oldnums = set(numbers_in(old)) | set(x.replace(",", "") for x in numbers_in(old))
        kept = set(str(x) for x in e.get("kept_numbers", []))
        for x in numbers_in(new):
            xs = x.replace(",", "")
            if x in oldnums or xs in oldnums or x in kept or x in offs or xs in offs:
                continue
            if re.fullmatch(r"20[12]\d", xs) or (xs.isdigit() and int(xs) <= 12):
                continue
            if re.fullmatch(r"\d{1,2}", xs):
                warns.append(f"#{n} small number {x} in new (structure?)")
                continue
            errs.append(f"#{n} number {x} in new is not official and not in old (add to kept_numbers only if the page already shows it)")
        for k in e.get("source_keys", []):
            if not resolve_key(d, k):
                errs.append(f"#{n} source_key does not resolve: {k}")
    # tier-1-only application must also match
    t1 = c0
    for e in edits:
        if e.get("tier", 1) != 1:
            continue
        t1b, cnt, note = apply_edit(t1, e)
        if cnt == -1 or (note and not e.get("spans_tags")):
            errs.append(f"#{e['n']} tier-1-only run: {note}")
        t1 = t1b
    # claims inventory
    cl = J.get("claims", [])
    if not cl:
        warns.append("no claims inventory")
    for x in cl:
        if x.get("verdict") not in ("CONFLICT", "STALE", "UNSOURCED", "CONSISTENT"):
            errs.append(f"claim {x.get('id')} verdict {x.get('verdict')}")
        m = re.match(r"edit (\d+)", x.get("action", ""))
        if m and not (1 <= int(m.group(1)) <= len(edits)):
            errs.append(f"claim {x.get('id')} points at missing {x.get('action')}")
        if x.get("verdict") in ("CONFLICT", "STALE") and not x.get("action", "").startswith("edit"):
            errs.append(f"claim {x.get('id')} is {x.get('verdict')} but not edited: {x.get('quote','')[:60]}")
    bl, _ = blocks(text)
    sus = scan_remaining(bl, d, offs)
    if show:
        print(f"[{slug}] page {p['id']} rendered {len(c0):,} chars (retrieved {p.get('retrieved_utc')}) | {len(edits)} edits | errors {len(errs)} | "
              f"warnings {len(warns)} | risky-old {len(risky_list)} | remaining suspects {len(sus)}")
        for x in errs:
            print("  ERR", x)
        if not quiet:
            for x in warns:
                print("  WARN", x)
            for n, rk in risky_list:
                print(f"  RISKY #{n}: {', '.join(rk)}")
            for s in sus:
                print("  SUSPECT", s)
    return {"errs": errs, "warns": warns, "risky": risky_list, "sus": sus, "edits": edits, "page": p, "text_after": text}


if __name__ == "__main__":
    main(sys.argv[1], "--live" in sys.argv, "--quiet" in sys.argv)
