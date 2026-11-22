# -*- coding: utf-8 -*-
"""HAD-801: the old tour had a WhatsApp button inside it (#waFab, wa.me/972525101555); the site law is that WhatsApp stays.
Adds one small round WhatsApp link to the standalone tour pages (five languages; not the frame pages, whose host page has the
site's own bar). Bottom corner opposite the walking control, clear of the tour's bottom bar on phone and desktop.
  python wa_button.py <site2 package dir> <manifest out>"""
import gzip, hashlib, json, os, sys, urllib.parse
P, MAN = sys.argv[1], sys.argv[2]
assert "site2" in P
TXT = {"he": "שלום, הגעתי מהסיור ברובע שדה דב 2036 ואשמח לפרטים", "en": "Hello, I came from the Sde Dov 2036 walk and would like details",
       "fr": "Bonjour, je viens de la visite Sde Dov 2036 et je souhaite des informations", "ru": "Здравствуйте, я из прогулки по Сде-Дов 2036, хочу узнать подробности",
       "ar": "مرحبا، وصلت من جولة سدي دوف 2036 وأرغب بالتفاصيل"}
LBL = {"he": "ייעוץ בוואטסאפ", "en": "WhatsApp", "fr": "WhatsApp", "ru": "WhatsApp", "ar": "واتساب"}
def btn(l):
    return ('<a id="nlTourWa" href="https://wa.me/972525101555?text=%s" target="_blank" rel="noopener" aria-label="%s" title="%s">'
            '<svg viewBox="0 0 32 32" width="26" height="26" aria-hidden="true"><path fill="#fff" d="M16 3a13 13 0 0 0-11.2 19.6L3 29l6.6-1.7A13 13 0 1 0 16 3zm0 23.6c-2 0-3.9-.5-5.6-1.5l-.4-.2-3.9 1 1-3.8-.3-.4A10.6 10.6 0 1 1 16 26.6zm5.8-7.9c-.3-.2-1.9-.9-2.2-1s-.5-.2-.7.2-.8 1-1 1.2-.4.2-.7 0a8.7 8.7 0 0 1-4.3-3.8c-.3-.6.3-.5.9-1.7.1-.2 0-.4 0-.5l-1-2.4c-.3-.6-.5-.5-.7-.5h-.6a1.2 1.2 0 0 0-.9.4 3.7 3.7 0 0 0-1.1 2.7 6.5 6.5 0 0 0 1.4 3.4 14.6 14.6 0 0 0 5.6 5c2.1.9 2.9 1 4 .8a3.4 3.4 0 0 0 2.2-1.6 2.8 2.8 0 0 0 .2-1.6c-.1-.1-.3-.2-.6-.4z"/></svg></a>'
            '<style>#nlTourWa{position:fixed;z-index:2147483000;right:max(14px,env(safe-area-inset-right));bottom:calc(84px + env(safe-area-inset-bottom));'
            'width:50px;height:50px;border-radius:50%%;background:#1f8f4e;display:flex;align-items:center;justify-content:center;box-shadow:0 2px 10px rgba(18,55,80,.35)}'
            '#nlTourWa:focus-visible{outline:3px solid #123750;outline-offset:2px}@media(max-width:640px){#nlTourWa{bottom:calc(120px + env(safe-area-inset-bottom));width:46px;height:46px}}</style>') % (
        urllib.parse.quote(TXT[l]), LBL[l], LBL[l])
PG = os.path.join(P, "pages"); n = 0
for l in TXT:
    p = os.path.join(PG, l + ".html"); b = open(p, encoding="utf-8").read()
    if 'id="nlTourWa"' in b:
        continue
    assert b.count("</body>") == 1, l
    b = b.replace("</body>", btn(l) + "</body>")
    open(p, "w", encoding="utf-8", newline="").write(b)
    open(p + ".gz", "wb").write(gzip.compress(b.encode("utf-8"), compresslevel=6, mtime=0)); n += 1
dg = {f: hashlib.sha256(open(os.path.join(PG, f), "rb").read()).hexdigest() for f in sorted(os.listdir(PG)) if f.endswith(".html")}
open(os.path.join(PG, "digests.json"), "w", encoding="utf-8", newline="\n").write(json.dumps(dg, indent=2) + "\n")
man = {}
for root, _, files in os.walk(P):
    for f in files:
        q = os.path.join(root, f); man[os.path.relpath(q, P).replace(os.sep, "/")] = {"bytes": os.path.getsize(q), "md5": hashlib.md5(open(q, "rb").read()).hexdigest()}
json.dump(man, open(MAN, "w", encoding="utf-8"), indent=0)
print("pages with the WhatsApp button", n, "| files", len(man))
