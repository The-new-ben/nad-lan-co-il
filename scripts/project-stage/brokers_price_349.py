# -*- coding: utf-8 -*-
"""The brokers page's professional plan at the owner's price (28.9.2026 evening: "it's three forty nine").
/brokers/ (page 7645) offered it at 149 ש״ח a month or 1,490 a year, while the professionals directory and the pricing
schema say 349. Now 349 a month and 3,490 a year (the same ten-month ratio the page used); "בונים לכם" stays 1,490 once.
Design system BrokersList, addendum of 28.9. Same mechanism as duo_sales_update.py: raw content over REST (the app password
decrypted in-process, never printed), each fix must match exactly once, guarded by the md5 of the content read just
before; the old raw content is saved first.
  python scripts/project-stage/brokers_price_349.py            # show
  python scripts/project-stage/brokers_price_349.py --apply    # write"""
import io, os, sys, hashlib, time
REPO = r"C:\Users\777\nad-lan\nad-lan-co-il"
src = io.open(os.path.join(REPO, "scripts", "project-stage", "rainbow_content4.py"), encoding="utf-8").read()
exec(compile(src[src.index("import base64, ctypes"):src.index("FIXES = [")].replace("PID = 4464", "PID = 7645")
             .replace("/wp-json/wp/v2/nadlan_project/%d", "/wp-json/wp/v2/pages/%d")
             .replace('QA = os.path.join(REPO, "docs", "qa", "rainbow-content-2026-09-24")', 'QA = os.path.join(REPO, "docs", "qa", "brokers-price-2026-09-28")'), "head", "exec"))
FIXES = [
    ('<p class="nlof-name">מקצועי</p><p class="nlof-price"><span class="nlof-num">149</span> ש״ח לחודש</p><p class="nlof-sub">או <span class="nlof-num">1,490</span> ש״ח לשנה</p>',
     '<p class="nlof-name">מקצועי</p><p class="nlof-price"><span class="nlof-num">349</span> ש״ח לחודש</p><p class="nlof-sub">או <span class="nlof-num">3,490</span> ש״ח לשנה</p>'),
]
d = read()
raw = d["content"]["raw"]
md5 = hashlib.md5(raw.encode("utf-8")).hexdigest()
new, bad = raw, []
for a, b in FIXES:
    n = new.count(a)
    print("[fix] x%d  %s..." % (n, a[:70]))
    if n != 1:
        bad.append(a[:60])
        continue
    new = new.replace(a, b)
if bad:
    raise SystemExit("FATAL: anchors not found exactly once: %r" % bad)
print("[plan] %d fixes, %d -> %d chars, md5 %s; other 149 left: %d" % (len(FIXES), len(raw), len(new), md5[:10], new.count(">149<")))
if not APPLY:
    raise SystemExit(0)
os.makedirs(QA, exist_ok=True)
io.open(os.path.join(QA, "brokers-7645-before-%s.html" % time.strftime("%Y%m%dT%H%M%S")), "w", encoding="utf-8").write(raw)
again = hashlib.md5(read()["content"]["raw"].encode("utf-8")).hexdigest()
if again != md5:
    raise SystemExit("FATAL: the content changed while this ran; read it again")
s, r = req("POST", "/wp-json/wp/v2/pages/%d" % PID, {"content": new})
print("[write]", s)
after = read()["content"]["raw"]
print("[verify] written:", hashlib.md5(after.encode("utf-8")).hexdigest() == hashlib.md5(new.encode("utf-8")).hexdigest())
