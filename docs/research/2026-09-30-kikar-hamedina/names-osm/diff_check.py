# -*- coding: utf-8 -*-
"""Proof that names_osm_kikar.py changed nothing but the places' "names" (HAD-375, 1.10.2026).

  python docs/research/2026-09-30-kikar-hamedina/names-osm/diff_check.py [OLD_REV] [NEW_FILE]

OLD: the registry as committed at OLD_REV (default HEAD; read as the raw git blob, so line endings are the committed ones).
NEW: the working file (default plugins/nadlan-config/assets/project-stage/hamedina/places.json).
Checks
  1. both files read back to their own bytes (compact JSON, ensure_ascii off, one final LF), so comparing parsed data is
     comparing bytes;
  2. every top-level field except "places" is equal, with the same key order;
  3. the same number of places in the same order; each place, with "names" taken out, equal to the old one with the same key
     order (ids are not unique in this file, so places are compared by position);
  4. every old "names" value is still there, unchanged, in the same order; the new values are only added languages;
  5. the research copy and the assets copy have the same bytes.
Exit code 1 on any difference."""
import hashlib, io, json, os, subprocess, sys

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(HERE))))
REL = "plugins/nadlan-config/assets/project-stage/hamedina/places.json"
RES_REL = "docs/research/2026-09-30-kikar-hamedina/places.json"
rev = sys.argv[1] if len(sys.argv) > 1 else "HEAD"
new_path = sys.argv[2] if len(sys.argv) > 2 else os.path.join(REPO, *REL.split("/"))

old_raw = subprocess.run(["git", "-C", REPO, "cat-file", "blob", "%s:%s" % (rev, REL)], capture_output=True, check=True).stdout.decode("utf-8")
new_raw = io.open(new_path, encoding="utf-8", newline="").read()
res_raw = io.open(os.path.join(REPO, *RES_REL.split("/")), encoding="utf-8", newline="").read()
old, new = json.loads(old_raw), json.loads(new_raw)
dumps = lambda d: json.dumps(d, ensure_ascii=False, separators=(",", ":")) + "\n"
diffs = []

if dumps(old) != old_raw:
    diffs.append("old file does not read back to its own bytes")
if dumps(new) != new_raw:
    diffs.append("new file does not read back to its own bytes")
if list(old) != list(new):
    diffs.append("top-level key order: %s -> %s" % (list(old), list(new)))
for k in old:
    if k != "places" and dumps(old.get(k)) != dumps(new.get(k)):
        diffs.append("top-level field changed: %s" % k)
po, pn = old["places"], new["places"]
if len(po) != len(pn):
    diffs.append("place count %d -> %d" % (len(po), len(pn)))
added = {"places": 0, "values": 0}
per_lang = {}
for i, (a, b) in enumerate(zip(po, pn)):
    a2 = {k: v for k, v in a.items() if k != "names"}
    b2 = {k: v for k, v in b.items() if k != "names"}
    if dumps(a2) != dumps(b2):
        diffs.append("place %d (%s): a field other than names differs" % (i, a.get("id")))
        continue
    na, nb = a.get("names") or {}, b.get("names") or {}
    if list(nb)[:len(na)] != list(na) or any(nb.get(l) != v for l, v in na.items()):
        diffs.append("place %d (%s): an existing name was changed, removed or reordered: %s -> %s" % (i, a.get("id"), na, nb))
        continue
    new_langs = [l for l in nb if l not in na]
    if new_langs:
        added["places"] += 1
        added["values"] += len(new_langs)
        for l in new_langs:
            per_lang[l] = per_lang.get(l, 0) + 1
    if "names" in b and not nb:
        diffs.append("place %d (%s): an empty names object" % (i, a.get("id")))
if res_raw != new_raw:
    diffs.append("the research copy and the assets copy differ")

print("old  %s:%s  md5 %s  bytes %d" % (rev, REL, hashlib.md5(old_raw.encode("utf-8")).hexdigest(), len(old_raw.encode("utf-8"))))
print("new  %s  md5 %s  bytes %d" % (os.path.relpath(new_path, REPO), hashlib.md5(new_raw.encode("utf-8")).hexdigest(), len(new_raw.encode("utf-8"))))
print("research copy md5 %s" % hashlib.md5(res_raw.encode("utf-8")).hexdigest())
print("places compared: %d | places with names added: %d | values added: %d %s" % (len(po), added["places"], added["values"], per_lang))
print("differences outside names: %d" % len(diffs))
for d in diffs[:50]:
    print("  " + d)
sys.exit(1 if diffs else 0)
