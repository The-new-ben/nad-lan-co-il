# -*- coding: utf-8 -*-
"""HAD-801, after static_routes.py: on this host only some file types are served as plain static files (js, css, images, fonts);
.bin and .json go through a per-visitor rate limit (about 20 in a burst, then 429). The tour asks for ~55 of them on start.
The server keeps every original file and gets a byte-identical twin "<name>.js" for each .bin/.json (tour_ship.py dupjs).
This puts one small script first in the tour pages (main + frame, five languages): same-origin requests under the tour folder
that end in .bin or .json (fetch, XMLHttpRequest, and URLs handed to workers) are sent to the twin. The engine is not touched.
  python shim_routes.py <site2 package dir> <manifest out>"""
import gzip, hashlib, json, os, sys
P, MAN = sys.argv[1], sys.argv[2]
assert "site2" in P
SHIM = (b"<script>/* nad-lan host: .bin/.json are read from their .js twins (static, not rate-limited) */(()=>{"
        b"const B=new URL('./',location.href).pathname,R=/\\.(bin|json)$/i;"
        b"const fx=u=>{try{const x=new URL(u,document.baseURI);if(x.origin===location.origin&&x.pathname.startsWith(B)&&R.test(x.pathname)){x.pathname+='.js';return x.href}}catch(e){}return null};"
        b"const F=window.fetch;window.fetch=function(i,o){if(typeof i==='string'||i instanceof URL){const n=fx(String(i));if(n)i=n}else if(i&&i.url){const n=fx(i.url);if(n)i=new Request(n,i)}return F.call(this,i,o)};"
        b"const O=XMLHttpRequest.prototype.open;XMLHttpRequest.prototype.open=function(m,u,...r){const n=fx(String(u));return O.call(this,m,n||u,...r)};"
        b"if(window.Worker){const W=Worker.prototype.postMessage;Worker.prototype.postMessage=function(m,...r){if(typeof m==='string'){const n=fx(m);if(n)m=n}return W.call(this,m,...r)}}"
        b"})();</script>")
PG = os.path.join(P, "pages"); n = 0
for f in sorted(os.listdir(PG)):
    if not f.endswith(".html") or f.endswith("-directory.html") or f.endswith("-places.html"):
        continue
    p = os.path.join(PG, f); b = open(p, "rb").read()
    if b"nad-lan host: .bin/.json" in b:
        continue
    assert b.count(b'<meta charset="utf-8">') >= 1, f
    b = b.replace(b'<meta charset="utf-8">', b'<meta charset="utf-8">' + SHIM, 1)
    open(p, "wb").write(b); open(p + ".gz", "wb").write(gzip.compress(b, compresslevel=6, mtime=0)); n += 1
dg = {f: hashlib.sha256(open(os.path.join(PG, f), "rb").read()).hexdigest() for f in sorted(os.listdir(PG)) if f.endswith(".html")}
open(os.path.join(PG, "digests.json"), "w", encoding="utf-8", newline="\n").write(json.dumps(dg, indent=2) + "\n")
# the twins, locally too, so the manifest describes exactly what the server holds
tw = 0
for root, dirs, files in os.walk(P):
    rel = os.path.relpath(root, P).replace(os.sep, "/")
    if rel.split("/")[0] in ("transfer", "pages"):
        continue
    for f in files:
        if f.endswith((".bin", ".json")):
            q = os.path.join(root, f + ".js")
            if not os.path.exists(q):
                open(q, "wb").write(open(os.path.join(root, f), "rb").read()); tw += 1
man = {}
for root, _, files in os.walk(P):
    for f in files:
        p = os.path.join(root, f); man[os.path.relpath(p, P).replace(os.sep, "/")] = {"bytes": os.path.getsize(p), "md5": hashlib.md5(open(p, "rb").read()).hexdigest()}
json.dump(man, open(MAN, "w", encoding="utf-8"), indent=0)
print("pages with the shim", n, "| twins", tw, "| files", len(man))
