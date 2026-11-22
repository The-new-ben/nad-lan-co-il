# -*- coding: utf-8 -*-
"""HAD-801 polish loop, cycle 3: a direct visit to /tour/sde-dov/ gets the light page (the one already used inside the /sde-dov/
dialog: same interface, places filtered on the device) instead of the 5 MB page that carries all 3,032 places as HTML.
Measured on a mid phone profile: walk ready 3.82 s -> 1.18 s. The full page stays at ?full=1; the indexable list stays at /places/.
The WhatsApp button goes on the five light pages too and removes itself when the page runs inside a frame (the host page has its own).
Backup: D:\\Scratch\\sde-dov-release-2026-11-22\\backup-loop3.
  python loop3_light.py <site2 package dir> <manifest out>"""
import gzip, hashlib, json, os, sys
P, MAN = sys.argv[1], sys.argv[2]
assert "site2" in P
src = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "wa_button.py"), encoding="utf-8").read()
ns = {}
exec(compile(src[:src.index('PG = os.path.join(P, "pages")')].replace('P, MAN = sys.argv[1], sys.argv[2]\nassert "site2" in P\n', ""), "wab", "exec"), ns)
btn = ns["btn"]
pp = os.path.join(P, "page.php"); t = open(pp, encoding="utf-8").read()
old = "$in_frame = ($_SERVER['HTTP_SEC_FETCH_DEST'] ?? '') === 'iframe' || ($_GET['walk'] ?? '') === '1';"
new = ("/* HAD-801 (22.11.2026): every visit to the street gets the light page; the full page with all places as HTML stays at ?full=1 */\n"
       "$in_frame = ($_GET['full'] ?? '') !== '1';")
if old in t:
    open(pp, "w", encoding="utf-8", newline="").write(t.replace(old, new, 1))
else:
    assert new in t, "page.php anchor not found"
PG = os.path.join(P, "pages"); n = 0
GUARD = "<script>if(window.top!==window.self){var w=document.getElementById('nlTourWa');if(w)w.remove()}</script>"
for l in ("he", "en", "fr", "ru", "ar"):
    p = os.path.join(PG, l + "-frame.html"); b = open(p, encoding="utf-8").read()
    if 'id="nlTourWa"' in b:
        continue
    assert b.count("</body>") == 1, l
    b = b.replace("</body>", btn(l) + GUARD + "</body>")
    open(p, "w", encoding="utf-8", newline="").write(b)
    open(p + ".gz", "wb").write(gzip.compress(b.encode("utf-8"), compresslevel=6, mtime=0)); n += 1
dg = {f: hashlib.sha256(open(os.path.join(PG, f), "rb").read()).hexdigest() for f in sorted(os.listdir(PG)) if f.endswith(".html")}
open(os.path.join(PG, "digests.json"), "w", encoding="utf-8", newline="\n").write(json.dumps(dg, indent=2) + "\n")
man = {}
for root, _, files in os.walk(P):
    for f in files:
        q = os.path.join(root, f); man[os.path.relpath(q, P).replace(os.sep, "/")] = {"bytes": os.path.getsize(q), "md5": hashlib.md5(open(q, "rb").read()).hexdigest()}
json.dump(man, open(MAN, "w", encoding="utf-8"), indent=0)
print("light pages with WhatsApp", n, "| page.php light by default | files", len(man))
