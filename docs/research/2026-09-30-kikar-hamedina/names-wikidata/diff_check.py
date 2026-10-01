# -*- coding: utf-8 -*-
"""Proof that names_wikidata_kikar.py changed nothing but the places' "names" / "names_src" (HAD-375, 1.10.2026).

  python docs/research/2026-09-30-kikar-hamedina/names-wikidata/diff_check.py [OLD_REV] [NEW_FILE]

OLD: the registry as committed at OLD_REV (default 89673407 = names_osm_kikar.py's committed output, this step's input; read
as the raw git blob). NEW: the working file (default plugins/nadlan-config/assets/project-stage/hamedina/places.json).
Checks
  1. both files are valid JSON and read back to their own bytes (compact, ensure_ascii off, one final LF);
  2. every top-level field except "places" is equal, with the same key order;
  3. the same number of places in the same order; each place, with "names" and "names_src" taken out, equal to the old one
     with the same key order (place ids are not unique in this file, so places are compared by position);
  4. every old "names" value is still there and unchanged, EXCEPT a value with Hebrew letters (it plainly fails the script
     check); each such removal is listed with its old value;
  5. every new value is in a language the old place lacked, passes names_osm.lang_ok(), and has names_src[lang] =
     "wikidata:Q..." whose saved Wikidata answer (names-wikidata/wikidata/) carries exactly that label in that language;
     names_src has no other keys; no empty "names" / "names_src" object;
  6. no names value anywhere in the new file fails the script check;
  7. the research copy and the assets copy have the same bytes.
Exit code 1 on any failure."""
import hashlib, io, json, os, re, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
RES = os.path.dirname(HERE)
sys.path.insert(0, RES)
import names_osm_kikar as no            # noqa: E402  (also sets utf-8 stdout)
import names_wikidata_kikar as nw       # noqa: E402

REPO = os.path.dirname(os.path.dirname(os.path.dirname(RES)))
REL = "plugins/nadlan-config/assets/project-stage/hamedina/places.json"
RES_REL = "docs/research/2026-09-30-kikar-hamedina/places.json"
rev = sys.argv[1] if len(sys.argv) > 1 else "89673407"
new_path = sys.argv[2] if len(sys.argv) > 2 else os.path.join(REPO, *REL.split("/"))

old_raw = subprocess.run(["git", "-C", REPO, "cat-file", "blob", "%s:%s" % (rev, REL)], capture_output=True, check=True).stdout.decode("utf-8")
new_raw = io.open(new_path, encoding="utf-8", newline="").read()
res_raw = io.open(os.path.join(REPO, *RES_REL.split("/")), encoding="utf-8", newline="").read()
old, new = json.loads(old_raw), json.loads(new_raw)
E, _ = nw.wd_load()
diffs, removed, added = [], [], []

if no.dumps(old) != old_raw:
    diffs.append("old file does not read back to its own bytes")
if no.dumps(new) != new_raw:
    diffs.append("new file does not read back to its own bytes")
if list(old) != list(new):
    diffs.append("top-level key order: %s -> %s" % (list(old), list(new)))
for k in old:
    if k != "places" and no.dumps(old.get(k)) != no.dumps(new.get(k)):
        diffs.append("top-level field changed: %s" % k)
po, pn = old["places"], new["places"]
if len(po) != len(pn):
    diffs.append("place count %d -> %d" % (len(po), len(pn)))
for i, (a, b) in enumerate(zip(po, pn)):
    strip = lambda p: {k: v for k, v in p.items() if k not in ("names", "names_src")}
    if no.dumps(strip(a)) != no.dumps(strip(b)):
        diffs.append("place %d (%s): a field other than names/names_src differs" % (i, a.get("id")))
        continue
    na, nb, sa, sb = a.get("names") or {}, b.get("names") or {}, a.get("names_src") or {}, b.get("names_src") or {}
    for l, v in na.items():
        if l in nb:
            if nb[l] != v:
                diffs.append("place %d (%s): names.%s changed %r -> %r" % (i, a["id"], l, v, nb[l]))
        elif no.HE_ANY.search(v):
            removed.append((i, a["id"], a["name"], l, v))
        else:
            diffs.append("place %d (%s): names.%s removed although it has no Hebrew letters: %r" % (i, a["id"], l, v))
    kept_order = [l for l in na if l in nb]
    if [l for l in nb if l in na] != kept_order:
        diffs.append("place %d (%s): the existing names were reordered" % (i, a["id"]))
    for l, v in sa.items():
        if sb.get(l) != v and l in nb:
            diffs.append("place %d (%s): names_src.%s changed" % (i, a["id"], l))
    for l in [l for l in nb if l not in na]:
        v, s = nb[l], sb.get(l, "")
        ok, why = no.lang_ok(l, v) if l in no.WANT else (False, "unknown language")
        m = re.match(r"^wikidata:(Q\d+)$", s)
        lab = nw.label(E.get(m.group(1), {}), l) if m else None
        if not ok:
            diffs.append("place %d (%s): added %s=%r fails the script check (%s)" % (i, a["id"], l, v, why))
        elif not m:
            diffs.append("place %d (%s): added %s=%r has no names_src wikidata:Q... (%r)" % (i, a["id"], l, v, s))
        elif lab != v:
            diffs.append("place %d (%s): added %s=%r is not the saved label of %s (%r)" % (i, a["id"], l, v, m.group(1), lab))
        else:
            added.append((i, a["id"], a["name"], l, v, s))
    extra = [l for l in sb if l not in sa and (l not in nb or l in na)]
    if extra:
        diffs.append("place %d (%s): names_src keys with no added value: %s" % (i, a["id"], extra))
    if ("names" in b and not nb) or ("names_src" in b and not sb):
        diffs.append("place %d (%s): an empty names / names_src object" % (i, a["id"]))
for i, p in enumerate(pn):
    for l, v in (p.get("names") or {}).items():
        if l not in no.WANT or not no.lang_ok(l, v)[0]:
            diffs.append("new place %d (%s): names.%s=%r fails the script check" % (i, p["id"], l, v))
if res_raw != new_raw:
    diffs.append("the research copy and the assets copy differ")

print("old  %s:%s  md5 %s  bytes %d" % (rev, REL, hashlib.md5(old_raw.encode("utf-8")).hexdigest(), len(old_raw.encode("utf-8"))))
print("new  %s  md5 %s  bytes %d" % (os.path.relpath(new_path, REPO), hashlib.md5(new_raw.encode("utf-8")).hexdigest(), len(new_raw.encode("utf-8"))))
print("research copy md5 %s (%s)" % (hashlib.md5(res_raw.encode("utf-8")).hexdigest(), "identical" if res_raw == new_raw else "DIFFERS"))
print("places compared: %d" % len(po))
print("values removed (Hebrew letters in a non-Hebrew name): %d" % len(removed))
for r in removed:
    print("  place %d %s %s: names.%s = %r" % r)
print("values added, each traced to the saved Wikidata label: %d" % len(added))
for r in added:
    print("  place %d %s %s: names.%s = %r (%s)" % r)
print("failures: %d" % len(diffs))
for d in diffs[:50]:
    print("  " + d)
sys.exit(1 if diffs else 0)
