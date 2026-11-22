# -*- coding: utf-8 -*-
"""HAD-801, after index_routes.py: the host rate-limits PHP requests (about 20 in a burst, then 429 and a short block for that
visitor), and the tour asks for ~20 code parts and data files at once. So the visitor's browser now loads the SAME bytes as plain
static files (nginx compresses them on the fly; no limit on static files). The PHP loaders stay in place and still work.
  pages:   ./packed/?f=X -> ./packed/X ; ./data/?f=X -> ./data/X?v=<sha8> ; ./entry-*/?f= -> ./entry-*/assets/
  code:    the registered parts import ./?f=part-X.js -> ./part-X.js, written to packed/<name> (the registered bytes, nothing else)
  entry:   the two non-media rows (entry.js, worker.js) are copied into entry-*/assets/ so one prefix serves every file
  python static_routes.py <site2 package dir> <manifest out>"""
import hashlib, json, os, re, sys
P, MAN = sys.argv[1], sys.argv[2]
assert "site2" in P
def r(rel): return open(os.path.join(P, *rel.split("/")), "rb").read()
def w(rel, b): open(os.path.join(P, *rel.split("/")), "wb").write(b)
ENTRY = [d for d in os.listdir(P) if d.startswith("entry-")][0]
res = json.load(open(os.path.join(P, "transfer", "resources.json"), encoding="utf-8"))
n_code = 0
for name, v in res["packed"].items():
    b = r("transfer/%s.raw" % v["sha256"]).replace(b'"./?f=', b'"./').replace(b"'./?f=", b"'./")
    assert b"?f=" not in b, name
    w("packed/" + name, b); n_code += 1
rows = json.load(open(os.path.join(P, ENTRY, "files.json"), encoding="utf-8"))
for name, row in rows.items():
    if not row["media"]:
        w(ENTRY + "/assets/" + name, r(ENTRY + "/" + name))
        if os.path.exists(os.path.join(P, ENTRY, name + ".gz")):
            w(ENTRY + "/assets/" + name + ".gz", r(ENTRY + "/" + name + ".gz"))
ver = {n: v["sha256"][:8] for n, v in res["data"].items()}
for n in list(ver):
    assert hashlib.sha256(r("data/" + n)).hexdigest()[:8] == ver[n], ("static data differs from the registered version", n)
n_pages = 0
PG = os.path.join(P, "pages")
for f in sorted(os.listdir(PG)):
    if not f.endswith(".html"):
        continue
    b0 = b = r("pages/" + f)
    b = b.replace(b"./packed/?f=", b"./packed/").replace(("./%s/?f=" % ENTRY).encode(), ("./%s/assets/" % ENTRY).encode())
    b = re.sub(rb"\./data/\?f=([A-Za-z0-9_.-]+)", lambda m: b"./data/" + m.group(1) + b"?v=" + ver[m.group(1).decode()].encode(), b)
    assert not re.search(rb"\./(packed|data)/\?f=|/\?f=", b), f
    if b != b0:
        import gzip
        w("pages/" + f, b); w("pages/" + f + ".gz", gzip.compress(b, compresslevel=6, mtime=0)); n_pages += 1
dg = {f: hashlib.sha256(r("pages/" + f)).hexdigest() for f in sorted(os.listdir(PG)) if f.endswith(".html")}
open(os.path.join(PG, "digests.json"), "w", encoding="utf-8", newline="\n").write(json.dumps(dg, indent=2) + "\n")
man = {}
for root, _, files in os.walk(P):
    for f in files:
        p = os.path.join(root, f); man[os.path.relpath(p, P).replace(os.sep, "/")] = {"bytes": os.path.getsize(p), "md5": hashlib.md5(open(p, "rb").read()).hexdigest()}
json.dump(man, open(MAN, "w", encoding="utf-8"), indent=0)
print("code parts written", n_code, "| pages", n_pages, "| files", len(man))
