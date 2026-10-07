# -*- coding: utf-8 -*-
"""Check the TIER-2 edits (CEO rule of 7.10.2026) of docs/content/city-align-2026-10/<slug>.align-edits.json against the LIVE page.

Tier 1 is already live, so only the tier-2 edits are applied, in the listed order, on the current content.rendered.
Checks: every old matches exactly once (whole tables through their anchor); no em/en dash, "!", HTML entity, newspaper name in new;
every number in new is in old, in kept_numbers, an official city-file number, a CBS table 4.9 figure (rounded half up or one decimal), or the CBS
dwelling share; source_keys resolve (city-file paths, cbs_rent[...], cbs_dwellings[...]); ceo_action / source_url present and consistent; then a
residual scan: each number that left the page is searched in the page text that remains (outside the price list, scripts and styles).

python check_tier2.py [slug ...] [--live-dir DIR] [--quiet]
"""
import io, json, os, re, sys, time, urllib.request
from decimal import Decimal, ROUND_HALF_UP

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import check as C  # official_numbers, resolve_key, numbers_in, NEWSPAPERS, PORTALS, apply_edit
from blocks import strip_ranges

OUTDIR = C.OUTDIR
CBS = json.load(io.open(os.path.join(HERE, "cbs_rent_2026_q2.json"), encoding="utf-8"))
ARGS = sys.argv[1:]
LIVE_DIR = ARGS[ARGS.index("--live-dir") + 1] if "--live-dir" in ARGS else None
QUIET = "--quiet" in ARGS


def cbs_numbers():
    vals = set()

    def add(v):
        if v is None:
            return
        vals.add(f"{int(Decimal(str(v)).quantize(Decimal('1'), rounding=ROUND_HALF_UP)):,}")
        vals.add(f"{v:,.1f}")
    for r in CBS["rows"].values():
        add(r["total"])
        for g in r["groups"].values():
            add(g)
    vals.add(str(CBS["dwellings_share"]["tel_aviv_district_pct"]))
    return vals


def resolve_cbs(key):
    m = re.fullmatch(r"cbs_rent\[(.+?)\]\.(total|1-2|2\.5-3|3\.5-4|4\.5\+)\.q2_2026", key)
    if m:
        row = CBS["rows"].get(m.group(1))
        if not row:
            return False
        return (row["total"] if m.group(2) == "total" else row["groups"].get(m.group(2))) is not None
    return key == "cbs_dwellings[מחוז תל אביב].share_2025"


def live_page(slug, pid):
    if LIVE_DIR:
        return json.load(io.open(os.path.join(LIVE_DIR, slug + ".json"), encoding="utf-8"))
    u = "https://nad-lan.co.il/wp-json/wp/v2/pages/%d?_fields=id,link,modified,content&nlca=%d" % (pid, time.time())
    p = json.loads(urllib.request.urlopen(urllib.request.Request(u, headers={"User-Agent": "Mozilla/5.0 NadLan-cityalign"}), timeout=90).read().decode("utf-8"))
    p["retrieved_utc"] = time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())
    return p


def visible(h):
    """page text outside <script>, <style> and the price list (for the residual scan)"""
    for s, e, kind in sorted(strip_ranges(h), reverse=True):
        h = h[:s] + " " + h[e:]
    h = re.sub(r"</t[dh]>", " | ", h)
    h = re.sub(r"</tr>", " // ", h)
    h = re.sub(r"<[^>]+>", " ", h)
    return re.sub(r"\s+", " ", h)


def check(slug):
    J = json.load(io.open(os.path.join(OUTDIR, slug + ".align-edits.json"), encoding="utf-8"))
    d = json.load(io.open(os.path.join(C.CITIES, slug + ".json"), encoding="utf-8"))
    t2 = [e for e in J["edits"] if e.get("tier") == 2]
    if not t2:
        return None
    page = live_page(slug, J["page"]["id"])
    live = page["content"]["rendered"]
    text = live
    offs = C.official_numbers(d) | cbs_numbers()
    errs, warns, left = [], [], []
    t1_in = sum(1 for e in J["edits"] if e.get("tier") == 1 and e["new"] in live)
    t1_n = sum(1 for e in J["edits"] if e.get("tier") == 1)
    if t1_in != t1_n:
        errs.append(f"tier 1 not fully live: {t1_in} of {t1_n} 'new' texts found")
    counts = {"replaced": 0, "removed": 0, "deleted": 0}
    for e in t2:
        n = e["n"]
        for f in ("page_id", "field", "old", "new", "source_keys", "verdict", "why", "tier", "raw_risk", "ceo_action", "ceo_note"):
            if f not in e:
                errs.append(f"#{n} missing {f}")
        if e.get("page_id") != page["id"]:
            errs.append(f"#{n} page_id")
        text2, cnt, note = C.apply_edit(text, e)
        if cnt == -1 or (note and not e.get("spans_tags")):
            errs.append(f"#{n} {note}: {e['old'][:70]!r}")
        elif e.get("spans_tags") and e["old"] not in text:
            errs.append(f"#{n} whole table: old string does not match the live table exactly")
        text = text2
        new, old = e["new"], e["old"]
        for bad in ("—", "–", "!", "&#", "&quot;", "&amp;", "&nbsp;"):
            if bad in new:
                errs.append(f"#{n} new contains {bad!r}")
        low = re.sub(r"(בכל|ברחבי|רחבי|כל) הארץ", " ", new.lower())
        for w in C.NEWSPAPERS:
            if w.lower() in low and w.lower() not in old.lower():
                errs.append(f"#{n} new names a newspaper/site: {w}")
        oldnums = set(C.numbers_in(old)) | set(x.replace(",", "") for x in C.numbers_in(old))
        kept = set(str(x) for x in e.get("kept_numbers", []))
        for x in C.numbers_in(new):
            xs = x.replace(",", "")
            if x in oldnums or xs in oldnums or x in kept or x in offs or xs in offs:
                continue
            if re.fullmatch(r"20[12]\d", xs) or (xs.isdigit() and int(xs) <= 12) or x in ("2.5", "3.5", "4.5"):
                continue
            errs.append(f"#{n} number {x} in new is not in old, not official, not kept")
        for k in e.get("source_keys", []):
            if not (C.resolve_key(d, k) or resolve_cbs(k)):
                errs.append(f"#{n} source_key does not resolve: {k}")
        act = e.get("ceo_action")
        if act not in counts:
            errs.append(f"#{n} ceo_action {act!r}")
        else:
            counts[act] += 1
        if act == "replaced" and not e.get("source_url", "").startswith("https://www.cbs.gov.il/"):
            errs.append(f"#{n} replaced without a cbs.gov.il source_url")
        if act != "replaced" and e.get("source_url"):
            errs.append(f"#{n} source_url on a non-replaced edit")
        if e.get("tier") != 2:
            errs.append(f"#{n} tier")
    # residual scan: numbers that left the page
    vis = visible(text)
    for e in t2:
        gone = [x for x in C.numbers_in(e["old"]) if x not in C.numbers_in(e["new"]) and ("," in x or "." in x or len(x) >= 3)]
        for x in sorted(set(gone)):
            hits = [m for m in re.finditer(r"(?<![\d,.])" + re.escape(x) + r"(?![\d,])(?!\.\d)", vis)]
            if hits:
                i = hits[0].start()
                left.append((e["n"], x, len(hits), vis[max(0, i - 70):i + 70]))
    # the old text of every removed number must not be in the visible page any more (spot: whole old strings)
    for e in t2:
        if not e.get("spans_tags") and e["old"] in text and e["old"] not in e["new"]:
            errs.append(f"#{e['n']} old string still present after the run")
    return {"slug": slug, "errs": errs, "left": left, "counts": counts, "n": len(t2), "retrieved": page.get("retrieved_utc"), "modified": page.get("modified"),
            "chars_before": len(live), "chars_after": len(text)}


if __name__ == "__main__":
    slugs = [a for a in ARGS if not a.startswith("--") and a != LIVE_DIR]
    if not slugs:
        slugs = sorted(f[:-len(".align-edits.json")] for f in os.listdir(OUTDIR) if f.endswith(".align-edits.json"))
    tot = {"replaced": 0, "removed": 0, "deleted": 0}
    bad = 0
    for s in slugs:
        r = check(s)
        if not r:
            continue
        for k in tot:
            tot[k] += r["counts"][k]
        bad += len(r["errs"])
        print(f"[{s}] tier-2 edits {r['n']} | replaced {r['counts']['replaced']} removed {r['counts']['removed']} deleted {r['counts']['deleted']} | "
              f"errors {len(r['errs'])} | numbers that left the edit but still stand elsewhere on the page {len(r['left'])} | live {r['retrieved']} UTC, modified {r['modified']}")
        for x in r["errs"]:
            print("  ERR", x)
        if not QUIET:
            for n, x, k, ctx in r["left"]:
                print(f"  LEFT #{n} {x} x{k}: ...{ctx}...")
    print("TOTAL", tot, "errors", bad)
