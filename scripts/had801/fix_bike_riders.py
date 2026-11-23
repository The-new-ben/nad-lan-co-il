# -*- coding: utf-8 -*-
"""HAD-801 (Ben, 23.11.2026 morning): bicycles rode without riders at the start of the tour. Cause, in Codex's walk bundle
(walk-DGQMIG45.js): the street kit makes every moving bicycle as a pair, {kind:"bicycle"} + {kind:"personBlue", rider:true};
inside the junction radius the detailed crossing cast takes over the people, so a filter drops the street-kit walkers but keeps
"bicycle" - and with it drops the rider. Fix: keep riders together with their bicycles (J.kind==="bicycle"||J.rider).
The fixed bundle gets a NEW name (walk-DGQMIG45-r1.js; static .js files are cached for a year), registered in transfer/ as well;
the ten street pages (5 languages, main + light) point to it. The old file stays.
  python fix_bike_riders.py <site2 package dir> <manifest out>"""
import gzip, hashlib, json, os, subprocess, sys
P, MAN = sys.argv[1], sys.argv[2]
assert "site2" in P
OLD, NEW = "walk-DGQMIG45.js", "walk-DGQMIG45-r1.js"
A, B = 'J.kind==="bicycle"', 'J.kind==="bicycle"||J.rider'
def sha(b): return hashlib.sha256(b).hexdigest()
def brotli(b):
    return subprocess.run(["node", "-e", "const z=require('zlib');const c=[];process.stdin.on('data',d=>c.push(d));process.stdin.on('end',()=>process.stdout.write(z.brotliCompressSync(Buffer.concat(c),{params:{[z.constants.BROTLI_PARAM_QUALITY]:11}})))"],
                          input=b, capture_output=True, check=True).stdout
st = open(os.path.join(P, "packed", OLD), "rb").read().decode("utf-8")
assert st.count(A) == 1 and st.count('rider:!0') == 1, (st.count(A), st.count('rider:!0'))
open(os.path.join(P, "packed", NEW), "w", encoding="utf-8", newline="").write(st.replace(A, B))
res_p = os.path.join(P, "transfer", "resources.json"); res = json.load(open(res_p, encoding="utf-8"))
raw = open(os.path.join(P, "transfer", res["packed"][OLD]["sha256"] + ".raw"), "rb").read().decode("utf-8")
assert raw.count(A) == 1
nb = raw.replace(A, B).encode("utf-8"); h = sha(nb); gz = gzip.compress(nb, compresslevel=9, mtime=0); br = brotli(nb)
for ext, data in (("raw", nb), ("gz", gz), ("br", br)):
    open(os.path.join(P, "transfer", "%s.%s" % (h, ext)), "wb").write(data)
res["packed"][NEW] = {"sha256": h, "bytes": len(nb), "br": len(br), "gzip": len(gz)}
open(res_p, "w", encoding="utf-8", newline="\n").write(json.dumps(res, ensure_ascii=False, indent=2) + "\n")
PG = os.path.join(P, "pages"); n = 0
for f in sorted(os.listdir(PG)):
    if not f.endswith(".html") or f.endswith(("-directory.html", "-places.html")):
        continue
    p = os.path.join(PG, f); b = open(p, encoding="utf-8").read()
    if "./packed/" + OLD in b:
        b = b.replace("./packed/" + OLD, "./packed/" + NEW)
        open(p, "w", encoding="utf-8", newline="").write(b)
        open(p + ".gz", "wb").write(gzip.compress(b.encode("utf-8"), compresslevel=6, mtime=0)); n += 1
dg = {f: hashlib.sha256(open(os.path.join(PG, f), "rb").read()).hexdigest() for f in sorted(os.listdir(PG)) if f.endswith(".html")}
open(os.path.join(PG, "digests.json"), "w", encoding="utf-8", newline="\n").write(json.dumps(dg, indent=2) + "\n")
man = {}
for root, _, files in os.walk(P):
    for f in files:
        q = os.path.join(root, f); man[os.path.relpath(q, P).replace(os.sep, "/")] = {"bytes": os.path.getsize(q), "md5": hashlib.md5(open(q, "rb").read()).hexdigest()}
json.dump(man, open(MAN, "w", encoding="utf-8"), indent=0)
print("pages pointed to", NEW, n, "| files", len(man))
