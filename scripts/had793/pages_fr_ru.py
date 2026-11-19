# -*- coding: utf-8 -*-
"""HAD-793 gap 23: create /fr/mortgage-calculator/ and /ru/mortgage-calculator/ (children of the language roots 5055 and 5056), the
twins of /en/mortgage-calculator/ (8780). Run only AFTER the release that gives mquick and inc/instruments.php their fr / ru blocks.
Titles and openings come from the manual Google pass of 19.11.2026 (docs/research/2026-11-19-pkg78/manual-2026-11-19/README.md).
Refuses to run if a page already holds the slug under that parent (no duplicates, nothing overwritten).
  python scripts/had793/pages_fr_ru.py [--go]"""
import io, json, os, sys, time
H = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.dirname(os.path.dirname(H))
_src = open(os.path.join(REPO, "scripts", "skin-a", "deployskin.py"), encoding="utf-8").read(); ns = {"__name__": "h793p"}
exec(compile(_src[:_src.index('s, h, _ = req("GET", "/wp-json/nadlan/v1/health")')], "h", "exec"), ns)
req, must = ns["req"], ns["must"]
CSS = io.open(os.path.join(H, "nlen-css.html"), encoding="utf-8").read()
PAGES = {
    "fr": {"parent": 5055, "title": "Simulateur de crédit immobilier en Israël : la mensualité de votre mashkanta",
           "yt": "Simulateur crédit immobilier Israël 2026 : mensualité et taux",
           "yd": "Simulateur de prêt immobilier en Israël (mashkanta) : mensualité en shekels aux derniers taux de la Banque d’Israël, par banque et tranche, apport et règles 2026.",
           "file": "page-fr.html"},
    "ru": {"parent": 5056, "title": "Ипотечный калькулятор Израиля: платёж по машканте",
           "yt": "Ипотечный калькулятор Израиль 2026: ежемесячный платёж и ставки",
           "yd": "Ипотечный калькулятор Израиля (машканта): ежемесячный платёж в шекелях по последним ставкам Банка Израиля, по банкам и трекам, собственные средства и правила 2026.",
           "file": "page-ru.html"},
}
s, h, _ = req("GET", "/wp-json/nadlan/v1/health"); must(s, h, "health"); print("live", h["version"])
for lang, P in PAGES.items():
    s, q, _ = req("GET", "/wp-json/wp/v2/pages?slug=mortgage-calculator&parent=%d&status=publish,draft,private&_fields=id,link,status" % P["parent"])
    must(s, q, "lookup " + lang)
    if q:
        print("[skip]", lang, "already exists:", q); continue
    body = io.open(os.path.join(H, P["file"]), encoding="utf-8").read().replace("@@CSS@@", CSS)
    assert "@@" not in body and "[nadlan_tool id=\"mquick\"]" in body
    if "--go" not in sys.argv:
        print("[dry]", lang, len(body), "chars under parent", P["parent"]); continue
    s, c, _ = req("POST", "/wp-json/wp/v2/pages", {"title": P["title"], "slug": "mortgage-calculator", "parent": P["parent"], "status": "publish",
                                                  "content": body, "meta": {"_yoast_wpseo_title": P["yt"], "_yoast_wpseo_metadesc": P["yd"]}})
    must(s, c, "create " + lang)
    print("[created]", lang, c["id"], c["link"])
    rec = {"at": time.strftime("%Y-%m-%d %H:%M"), "lang": lang, "id": c["id"], "link": c["link"], "title": P["title"], "yoast_title": P["yt"]}
    with open(os.path.join(REPO, "docs", "research", "2026-11-19-pkg78", "pages-created.jsonl"), "a", encoding="utf-8") as f:
        f.write(json.dumps(rec, ensure_ascii=False) + "\n")
