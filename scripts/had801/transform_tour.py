# -*- coding: utf-8 -*-
"""HAD-801: prepare Codex's Sde Dov 2036 tour package (copied, never edited in place) for release at /tour/sde-dov/.
  1. Names instead of codes: a plot with a published project or a tender winner carries that name; the buildings inside it
     carry the project's or developer's name before their plot and building number. The old label is kept as a search alias
     and inside the new name, so nothing is lost. Names come only from the package's own sourced records (the project names
     Codex linked to our pages, the tender committee winners in the RMI tender facts).
  2. Other languages: the new name is added to the tour's own translation table, in the same pattern scheme the tour uses
     (numbers become {n0}, {n1}); a developer with no known Latin, Cyrillic or Arabic spelling keeps the old translated label.
  3. The standalone tour pages keep the noindex they carry today on the live site (meta robots), nothing more.
  4. Data versions that no page or registry references (old builds) are dropped from transfer/.
  python scripts/had801/transform_tour.py <src package dir> <out package dir> <proof json>"""
import gzip, hashlib, html, json, os, re, shutil, subprocess, sys
SRC, OUT, PROOF = sys.argv[1], sys.argv[2], sys.argv[3]
NUMBER = re.compile(r"[0-9]+(?:[.,][0-9]+)*")
LANGS = ["en", "fr", "ru", "ar"]

# lot id -> (Hebrew name as the tender record gives it, without the company-form suffix; {lang: name} where the spelling is known)
DEV = {
    "lot-eshkol-106": ("ריט ש.ב. נדל״ן נכסים", {}),
    "lot-eshkol-301": ("הדס קפיטל מקרקעי ישראל", {}),
    "lot-eshkol-302": ("רמי שבירו, רייסדור ות. סורנטו", {}),
    "lot-eshkol-303": ("מבנה נדל״ן", {"en": "Mivne Real Estate", "fr": "Mivne Real Estate", "ru": "Мивне", "ar": "ميفنيه"}),
    "lot-eshkol-305": ("רבד", {}),
    "lot-merkaz-2102": ("פרשקובסקי מניבים", {"en": "Prashkovsky", "fr": "Prashkovsky", "ru": "Прашковски", "ar": "براشكوفسكي"}),
    "lot-merkaz-2103": ("האחים ישראל", {}),
    "lot-merkaz-2104": ("פאלאס רעננה, דיור מוגן", {}),
    "lot-merkaz-2203": ("פרשקובסקי מניבים", {"en": "Prashkovsky", "fr": "Prashkovsky", "ru": "Прашковски", "ar": "براشكوفسكي"}),
    "lot-merkaz-2207": ("פרשקובסקי מניבים", {"en": "Prashkovsky", "fr": "Prashkovsky", "ru": "Прашковски", "ar": "براشكوفسكي"}),
    "lot-merkaz-2208": ("אלקטרה מגורים ונהור", {}),
    "lot-merkaz-2226": ("א.א.י. אבו מגורים ותומר קוקו", {}),
    "lot-merkaz-2227": ("לוזון רונסון", {"en": "Luzon Ronson", "fr": "Luzon Ronson", "ru": "Лузон Ронсон", "ar": "لوزون رونسون"}),
    "lot-tzafon-3102": ("תשלוז השקעות והחזקות", {}),
    "lot-tzafon-3106": ("לוזון רונסון ושמעון אמיר", {"en": "Luzon Ronson and Shimon Amir", "fr": "Luzon Ronson et Shimon Amir", "ru": "Лузон Ронсон и Шимон Амир", "ar": "لوزون رونسون وشمعون أمير"}),
    "lot-tzafon-3109": ("יוסי אברהמי", {"en": "Yossi Avrahami", "fr": "Yossi Avrahami", "ru": "Йоси Авраами", "ar": "يوسي أفراهامي"}),
    "lot-tzafon-3201": ("יורו ישראל", {}),
    "lot-tzafon-3202": ("א.מ. ישראל מגורים", {}),
    "lot-tzafon-3203": ("שיכון ובינוי", {"en": "Shikun & Binui", "fr": "Shikun & Binui", "ru": "Шикун у-Бинуй", "ar": "شيكون وبينوي"}),
    "lot-tzafon-3205": ("אביב מגורים בשדה דב", {}),
    "lot-tzafon-3207": ("כלנית נכסים ופיתוח", {}),
    "lot-tzafon-3208": ("יוניון ליב", {}),
    "lot-tzafon-3209": ("א.מ. ישראל מגורים", {}),
    "lot-tzafon-3210": ("י.ח. דמרי", {"en": "Y.H. Dimri", "fr": "Y.H. Dimri", "ru": "Й.Х. Димри", "ar": "ي.ح. ديمري"}),
}


def canon(text):
    vals = []
    def cap(m):
        vals.append(m.group(0)); return "{n%d}" % (len(vals) - 1)
    return NUMBER.sub(cap, text), vals


def translate(table, text):
    if text in table and isinstance(table[text], str):
        return table[text]
    c, vals = canon(text)
    v = table.get(c)
    if not isinstance(v, str):
        return text
    return re.sub(r"\{n(\d+)\}", lambda m: vals[int(m.group(1))] if int(m.group(1)) < len(vals) else "", v)


def sha(b): return hashlib.sha256(b).hexdigest()
def md5(b): return hashlib.md5(b).hexdigest()


def brotli(b):
    p = subprocess.run(["node", "-e", "const z=require('zlib');const c=[];process.stdin.on('data',d=>c.push(d));process.stdin.on('end',()=>process.stdout.write(z.brotliCompressSync(Buffer.concat(c),{params:{[z.constants.BROTLI_PARAM_QUALITY]:11}})))"],
                       input=b, capture_output=True, check=True)
    return p.stdout


# 0. fresh copy
if os.path.exists(OUT):
    raise SystemExit("output exists: " + OUT)
shutil.copytree(SRC, OUT)
res_p = os.path.join(OUT, "transfer", "resources.json")
res = json.load(open(res_p, encoding="utf-8"))
dj_p, st_p = os.path.join(OUT, "data", "district.json"), os.path.join(OUT, "data", "strings.json")
dj_b, st_b = open(dj_p, "rb").read(), open(st_p, "rb").read()
assert sha(dj_b) == res["data"]["district.json"]["sha256"], "district.json is not the registered version"
assert sha(st_b) == res["data"]["strings.json"]["sha256"], "strings.json is not the registered version"
D = json.loads(dj_b.decode("utf-8")); S = json.loads(st_b.decode("utf-8"))
places = D["places"]; byid = {p["id"]: p for p in places}
before = {"places": len(places), "kinds": {}, "layers": len(D["layers"]), "route": len(D["route"]), "sources": len(D["sources"]),
          "rails": len(D["rails"]), "links": len(D["links"]), "languages": sorted(S.keys()),
          "catalogText": {l: len(S[l].get("catalogText") or {}) for l in S}}
for p in places:
    before["kinds"][p["kind"]] = before["kinds"].get(p["kind"], 0) + 1
years = sorted({y for p in places for y in ([p.get("fromYear")] if p.get("fromYear") else []) + list(p.get("opening") or [])})
before["years"] = [years[0], years[-1], len(years)] if years else []
before["facts"] = sum(len(p.get("facts") or []) for p in places)

# 1. labels for parents (projects + tender-winner plots)
plabel = {}
for p in places:
    if p["kind"] == "project":
        he = re.sub(r"\s*·\s*מגרש\s*[0-9]+$", "", p["name"])
        tr = {l: translate(S[l]["catalogText"], he) for l in LANGS}
        plabel[p["id"]] = (he, tr)
for lid, (he, tr) in DEV.items():
    assert lid in byid and byid[lid]["kind"] == "lot", lid
    win = [f for f in byid[lid].get("facts", []) if "נבחרה ההצעה" in f["text"]]
    assert win, "no tender winner fact on " + lid
    plabel[lid] = (he, tr)

renames = []
new_keys = {l: {} for l in LANGS}


def rename(p, new_he, prefix_tr, suffix_tr):
    old = p["name"]
    renames.append({"id": p["id"], "kind": p["kind"], "old": old, "new": new_he,
                    "source": ",".join(s for s in (p.get("sources") or []) if s.startswith("rmi") or s.startswith("dev") or s.startswith("catalog") or s.startswith("lot")) or ",".join(p.get("sources") or [])})
    for l in LANGS:
        table = S[l]["catalogText"]
        old_tr = translate(table, old)
        oc, ovals = canon(old)
        nc, nvals = canon(new_he)
        assert ovals == nvals, (old, new_he)
        key_old_pattern = table.get(oc) if isinstance(table.get(oc), str) else (table.get(old) if isinstance(table.get(old), str) else None)
        if key_old_pattern is None:
            continue  # the old label was not translated in this language either; leave as it was
        if table.get(old) == key_old_pattern and oc != old:
            pass
        pre, suf = prefix_tr.get(l) if prefix_tr else None, suffix_tr.get(l) if suffix_tr else None
        if prefix_tr is not None and pre is None or suffix_tr is not None and suf is None:
            val = key_old_pattern  # no known spelling: keep the old translated label
        else:
            val = (pre + " · " if pre else "") + key_old_pattern + (" · " + suf if suf else "")
        if nc in table and table[nc] != val:
            assert new_keys[l].get(nc) == val, ("conflicting key", l, nc)
        table[nc] = val; new_keys[l][nc] = val
    al = list(p.get("aliases") or [])
    if old not in al:
        al.append(old)
    p["aliases"] = al
    p["name"] = new_he


for p in places:
    if p["kind"] == "lot" and p["id"] in DEV:
        he, tr = plabel[p["id"]]
        rename(p, p["name"] + " · " + he, None, tr)
for p in places:
    if p["kind"] == "building" and p.get("parentId") in plabel:
        he, tr = plabel[p["parentId"]]
        rename(p, he + " · " + p["name"], tr, None)

# 2. write the data, then the registered transfer triplets
dj_new = json.dumps(D, ensure_ascii=False, separators=(",", ":")).encode("utf-8")
st_new = json.dumps(S, ensure_ascii=False, separators=(",", ":")).encode("utf-8")
open(dj_p, "wb").write(dj_new); open(st_p, "wb").write(st_new)
for name, b in (("district.json", dj_new), ("strings.json", st_new)):
    h = sha(b); base = os.path.join(OUT, "transfer", h)
    gz = gzip.compress(b, compresslevel=9, mtime=0); br = brotli(b)
    open(base + ".raw", "wb").write(b); open(base + ".gz", "wb").write(gz); open(base + ".br", "wb").write(br)
    res["data"][name] = {"sha256": h, "bytes": len(b), "br": len(br), "gzip": len(gz)}
open(res_p, "w", encoding="utf-8", newline="\n").write(json.dumps(res, ensure_ascii=False, indent=2) + "\n")
cur = {v["sha256"] for g in res.values() for v in g.values()}
dropped = []
for f in sorted(os.listdir(os.path.join(OUT, "transfer"))):
    if f == "resources.json":
        continue
    if f.split(".")[0] not in cur:
        dropped.append(f); os.remove(os.path.join(OUT, "transfer", f))

# 3. pages: the server-rendered names in every language, and the noindex the live tour already carries
PG = os.path.join(OUT, "pages"); page_counts = {}
for f in sorted(os.listdir(PG)):
    if not f.endswith(".html"):
        continue
    lang = f.split("-")[0].split(".")[0]
    t = open(os.path.join(PG, f), encoding="utf-8").read(); t0 = t
    n_rep = 0
    for r in sorted(renames, key=lambda r: -len(r["old"])):
        if lang == "he":
            o, n = r["old"], r["new"]
        else:
            o = translate(json.loads(st_b.decode("utf-8"))[lang]["catalogText"], r["old"])
            n = translate(S[lang]["catalogText"], r["new"])
        if o == n:
            continue
        eo, en_ = html.escape(o, quote=True), html.escape(n, quote=True)
        pat = re.compile(r"(?:(?<=[>\"])|(?<=· ))" + re.escape(eo) + r"(?=[<\"]| \()")
        t, k = pat.subn(en_, t); n_rep += k
    robots = 0
    if f in ("he.html", "en.html", "fr.html", "ru.html", "ar.html") or f.endswith("-frame.html"):
        if 'name="robots"' not in t:
            t = t.replace('<meta charset="utf-8">', '<meta charset="utf-8"><meta name="robots" content="noindex">', 1); robots = 1
            assert 'name="robots"' in t, f
    page_counts[f] = {"names_replaced": n_rep, "noindex_kept": robots, "bytes_before": len(t0.encode("utf-8")), "bytes_after": len(t.encode("utf-8"))}
    if t != t0:
        b = t.encode("utf-8")
        open(os.path.join(PG, f), "wb").write(b)
        open(os.path.join(PG, f + ".gz"), "wb").write(gzip.compress(b, compresslevel=6, mtime=0))
dg = {f: sha(open(os.path.join(PG, f), "rb").read()) for f in sorted(os.listdir(PG)) if f.endswith(".html")}
open(os.path.join(PG, "digests.json"), "w", encoding="utf-8", newline="\n").write(json.dumps(dg, indent=2) + "\n")

# 4. after counts + manifest
after = {"places": len(places), "kinds": {}, "layers": len(D["layers"]), "route": len(D["route"]), "sources": len(D["sources"]),
         "rails": len(D["rails"]), "links": len(D["links"]), "languages": sorted(S.keys()),
         "catalogText": {l: len(S[l].get("catalogText") or {}) for l in S}, "facts": sum(len(p.get("facts") or []) for p in places)}
for p in places:
    after["kinds"][p["kind"]] = after["kinds"].get(p["kind"], 0) + 1
years = sorted({y for p in places for y in ([p.get("fromYear")] if p.get("fromYear") else []) + list(p.get("opening") or [])})
after["years"] = [years[0], years[-1], len(years)] if years else []
man = {}
for root, _, files in os.walk(OUT):
    for f in files:
        p = os.path.join(root, f); b = open(p, "rb").read()
        man[os.path.relpath(p, OUT).replace(os.sep, "/")] = {"bytes": len(b), "md5": md5(b)}
proof = {"before": before, "after": after, "renames": renames, "new_translation_keys": {l: len(v) for l, v in new_keys.items()},
         "pages": page_counts, "dropped_unreferenced_transfer": len(dropped), "dropped_bytes": None,
         "package": {"files": len(man), "bytes": sum(v["bytes"] for v in man.values())}}
json.dump(proof, open(PROOF, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
json.dump(man, open(os.path.join(os.path.dirname(PROOF), "manifest.json"), "w", encoding="utf-8"), indent=0)
print("renamed", len(renames), "| new keys", proof["new_translation_keys"], "| dropped", len(dropped), "| package", proof["package"])
print("before", json.dumps(before, ensure_ascii=False)); print("after ", json.dumps(after, ensure_ascii=False))
for f, c in page_counts.items():
    print(f, c)
