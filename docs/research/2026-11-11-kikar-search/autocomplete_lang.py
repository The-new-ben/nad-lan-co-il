# -*- coding: utf-8 -*-
"""HAD-712, the language pages' search research (11.11.2026): Google autocomplete for the project and the area, per language and market.
GETs to Google's public suggest endpoint, slowly (1.2 s apart), no login. Saves the raw answers to autocomplete-<lang>.json beside this file.
  python autocomplete_lang.py <en|fr|ru|ar>"""
import json, os, sys, time, urllib.parse, urllib.request
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
LANG = sys.argv[1]
MARKETS = {"en": ["us", "gb", "il"], "fr": ["fr", "il"], "ru": ["il", "ru"], "ar": ["il", "ae", "jo"]}[LANG]
SEEDS = {
    "en": ["kikar hamedina", "kikar hamedina towers", "kikar hamedina tel aviv", "hamedina square tel aviv", "kikar hamedina apartments",
           "kikar hamedina towers price", "tel aviv luxury apartments", "tel aviv new apartments for sale", "buy apartment in tel aviv",
           "tel aviv apartment prices", "north tel aviv apartments", "tel aviv towers for sale", "buying property in israel as a foreigner",
           "israel purchase tax foreign resident", "mortgage in israel for non residents", "kikar hamedina towers "],
    "fr": ["kikar hamedina", "tours kikar hamedina", "kikar hamedina tel aviv", "acheter appartement tel aviv", "appartement de luxe tel aviv",
           "prix appartement tel aviv", "acheter en israel", "taxe d'acquisition israel", "pret immobilier israel non resident", "kikar hamedina "],
    "ru": ["кикар ха медина", "кикар а медина", "кикар хамедина", "башни кикар", "квартира в тель авиве купить", "элитные квартиры тель авив",
           "цены на квартиры в тель авиве", "купить квартиру в израиле", "налог на покупку квартиры в израиле", "ипотека в израиле для нерезидентов"],
    "ar": ["كيكار همدينا", "ساحة الدولة تل ابيب", "ابراج كيكار همدينا", "شقق للبيع في تل ابيب", "شقق فاخرة تل ابيب", "اسعار الشقق في تل ابيب",
           "شراء شقة في اسرائيل", "ضريبة الشراء في اسرائيل", "شقق للبيع في يافا"],
}[LANG]


def suggest(q, gl):
    u = "https://suggestqueries.google.com/complete/search?" + urllib.parse.urlencode({"client": "firefox", "q": q, "hl": LANG, "gl": gl})
    with urllib.request.urlopen(urllib.request.Request(u, headers={"User-Agent": "Mozilla/5.0"}), timeout=20) as r:
        raw = r.read()
    for enc in ("utf-8", "cp1255", "latin-1"):
        try:
            return json.loads(raw.decode(enc))[1]
        except Exception:
            continue
    return []


out = {"lang": LANG, "markets": MARKETS, "fetched": time.strftime("%Y-%m-%dT%H:%M:%S"), "results": {}}
for gl in MARKETS:
    for q in SEEDS:
        try:
            out["results"]["%s | %s" % (gl, q)] = suggest(q, gl)
        except Exception as e:
            out["results"]["%s | %s" % (gl, q)] = ["ERROR " + str(e)[:80]]
        time.sleep(1.2)
json.dump(out, open(os.path.join(HERE, "autocomplete-%s.json" % LANG), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
for k, v in out["results"].items():
    print(k, "->", "; ".join(v[:10]))
