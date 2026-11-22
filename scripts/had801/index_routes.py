# -*- coding: utf-8 -*-
"""HAD-801: the host (uPress nginx) answers 403 to every PHP file except index.php. Codex's package serves its data, code and
lists through load.php / file.php / places.php / catalog.php. This makes a copy of the package that reaches the same PHP through
folder index files, nothing else changed:
  packed/load.php?f=X     -> packed/?f=X           (packed/index.php = load.php)
  data/load.php?f=X       -> data/?f=X             (data/index.php = load.php)
  entry-*/file.php?f=X    -> entry-*/?f=X          (entry-*/index.php = file.php)
  places.php              -> places/               (places/index.php: the readable list of places and sources)
  catalog.php?lang=       -> catalog/?lang=        (catalog/index.php)
The rewritten code files get new registered triplets (raw/gz/br) in transfer/ and resources.json; the page digests are rebuilt.
The list pages are served one folder deeper, so their <base href="./"> becomes "../" (same targets as before).
  python index_routes.py <package dir (edited in place, must be a copy)> <manifest out>"""
import gzip, hashlib, json, os, re, subprocess, sys
P, MAN = sys.argv[1], sys.argv[2]
assert os.path.basename(os.path.dirname(P.rstrip("/\\"))) == "tour" and "site2" in P, "work only on the site2 copy"
def sha(b): return hashlib.sha256(b).hexdigest()
def brotli(b):
    return subprocess.run(["node", "-e", "const z=require('zlib');const c=[];process.stdin.on('data',d=>c.push(d));process.stdin.on('end',()=>process.stdout.write(z.brotliCompressSync(Buffer.concat(c),{params:{[z.constants.BROTLI_PARAM_QUALITY]:11}})))"],
                          input=b, capture_output=True, check=True).stdout
def w(rel, b):
    p = os.path.join(P, *rel.split("/")); os.makedirs(os.path.dirname(p), exist_ok=True); open(p, "wb").write(b)
def r(rel): return open(os.path.join(P, *rel.split("/")), "rb").read()
ENTRY = [d for d in os.listdir(P) if d.startswith("entry-")]
assert len(ENTRY) == 1, ENTRY
ENTRY = ENTRY[0]
# 1. folder index files (copies of the existing loaders; page wrappers that keep page.php where it is)
w("packed/index.php", r("packed/load.php")); w("data/index.php", r("data/load.php")); w(ENTRY + "/index.php", r(ENTRY + "/file.php"))
w("places/index.php", b"<?php\n$catalogue = false;\n$reading = true;\nrequire dirname(__DIR__) . '/page.php';\n")
w("catalog/index.php", b"<?php\n$catalogue = true;\nrequire dirname(__DIR__) . '/page.php';\n")
SUBS = [(b"./load.php?f=", b"./?f="), (b"./catalog.php?lang=", b"./catalog/?lang="), (b"./packed/load.php?f=", b"./packed/?f="),
        (b"./data/load.php?f=", b"./data/?f="), (("./%s/file.php?f=" % ENTRY).encode(), ("./%s/?f=" % ENTRY).encode()),
        (b'"./places.php"', b'"./places/"'), (b"'./places.php'", b"'./places/'"), (b"./places.php?lang=", b"./places/?lang=")]
def sub(b):
    n = 0
    for a, c in SUBS:
        n += b.count(a); b = b.replace(a, c)
    return b, n
stats = {"code": {}, "pages": {}}
# 2. registered code (transfer triplets)
res_p = os.path.join(P, "transfer", "resources.json"); res = json.load(open(res_p, encoding="utf-8"))
for name, v in res["packed"].items():
    raw = r("transfer/%s.raw" % v["sha256"]); nb, n = sub(raw)
    if not n:
        continue
    h = sha(nb); gz = gzip.compress(nb, compresslevel=9, mtime=0); br = brotli(nb)
    w("transfer/%s.raw" % h, nb); w("transfer/%s.gz" % h, gz); w("transfer/%s.br" % h, br)
    res["packed"][name] = {"sha256": h, "bytes": len(nb), "br": len(br), "gzip": len(gz)}
    stats["code"][name] = n
open(res_p, "w", encoding="utf-8", newline="\n").write(json.dumps(res, ensure_ascii=False, indent=2) + "\n")
for rel in ("app.js",):
    nb, n = sub(r(rel))
    if n:
        w(rel, nb); stats["code"][rel] = n
# 3. pages
PG = os.path.join(P, "pages")
for f in sorted(os.listdir(PG)):
    if not f.endswith(".html"):
        continue
    b, n = sub(r("pages/" + f))
    if f.endswith("-directory.html") or f.endswith("-places.html"):
        k = b.count(b'<base href="./'); b = b.replace(b'<base href="./">', b'<base href="../">').replace(b'<base href="./?lang=', b'<base href="../?lang='); n += k
    if n:
        w("pages/" + f, b); w("pages/" + f + ".gz", gzip.compress(b, compresslevel=6, mtime=0)); stats["pages"][f] = n
dg = {f: sha(r("pages/" + f)) for f in sorted(os.listdir(PG)) if f.endswith(".html")}
open(os.path.join(PG, "digests.json"), "w", encoding="utf-8", newline="\n").write(json.dumps(dg, indent=2) + "\n")
# 4. nothing left that points at a blocked PHP name (pages + registered code)
left = []
for f in os.listdir(PG):
    if f.endswith(".html") and re.search(rb"(load|file|places|catalog)\.php", r("pages/" + f)):
        left.append(f)
for name, v in res["packed"].items():
    if re.search(rb"(load|file|places|catalog)\.php", r("transfer/%s.raw" % v["sha256"])):
        left.append(name)
man = {}
for root, _, files in os.walk(P):
    for f in files:
        p = os.path.join(root, f); man[os.path.relpath(p, P).replace(os.sep, "/")] = {"bytes": os.path.getsize(p), "md5": hashlib.md5(open(p, "rb").read()).hexdigest()}
json.dump(man, open(MAN, "w", encoding="utf-8"), indent=0)
print(json.dumps({"code_files": len(stats["code"]), "code_refs": sum(stats["code"].values()), "pages": len(stats["pages"]),
                  "page_refs": sum(stats["pages"].values()), "left": left, "files": len(man)}, indent=1))
