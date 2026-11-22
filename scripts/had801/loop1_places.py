# -*- coding: utf-8 -*-
"""HAD-801 polish loop, cycle 1: the places-and-sources list (/tour/sde-dov/places/) had no way to reach the office and no
canonical address. Adds the tour's WhatsApp button (wa_button.btn) and a self canonical to the five language versions.
Backup of the previous files: D:\\Scratch\\sde-dov-release-2026-11-22\\backup-loop1\\pages.
  python loop1_places.py <site2 package dir> <manifest out>"""
import gzip, hashlib, json, os, sys, importlib.util
P, MAN = sys.argv[1], sys.argv[2]
assert "site2" in P
spec = importlib.util.spec_from_file_location("wab", os.path.join(os.path.dirname(os.path.abspath(__file__)), "wa_button.py"))
src = open(spec.origin, encoding="utf-8").read()
ns = {}
exec(compile(src[:src.index("PG = os.path.join(P, \"pages\")")].replace("P, MAN = sys.argv[1], sys.argv[2]\nassert \"site2\" in P\n", ""), "wab", "exec"), ns)
btn = ns["btn"]
PG = os.path.join(P, "pages"); n = 0
for l in ("he", "en", "fr", "ru", "ar"):
    p = os.path.join(PG, l + "-directory.html"); b = open(p, encoding="utf-8").read()
    if 'id="nlTourWa"' in b:
        continue
    canon = "https://nad-lan.co.il/tour/sde-dov/places/" + ("" if l == "he" else "?lang=" + l)
    assert b.count("</body>") == 1 and 'rel="canonical"' not in b and b.count("</title>") == 1, l
    b = b.replace("</title>", '</title><link rel="canonical" href="%s">' % canon, 1).replace("</body>", btn(l) + "</body>")
    open(p, "w", encoding="utf-8", newline="").write(b)
    open(p + ".gz", "wb").write(gzip.compress(b.encode("utf-8"), compresslevel=6, mtime=0)); n += 1
dg = {f: hashlib.sha256(open(os.path.join(PG, f), "rb").read()).hexdigest() for f in sorted(os.listdir(PG)) if f.endswith(".html")}
open(os.path.join(PG, "digests.json"), "w", encoding="utf-8", newline="\n").write(json.dumps(dg, indent=2) + "\n")
man = {}
for root, _, files in os.walk(P):
    for f in files:
        q = os.path.join(root, f); man[os.path.relpath(q, P).replace(os.sep, "/")] = {"bytes": os.path.getsize(q), "md5": hashlib.md5(open(q, "rb").read()).hexdigest()}
json.dump(man, open(MAN, "w", encoding="utf-8"), indent=0)
print("list pages with WhatsApp + canonical", n, "| files", len(man))
