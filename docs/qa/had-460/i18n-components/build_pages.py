# -*- coding: utf-8 -*-
"""Local preview pages (not the site): <lang>.html = a stand-in page head, the PriceGuide section (price_guide/rova-4[.<lang>].json)
and the AreaMap section (area_map/rova-4[.<lang>].json) with their CSS and script, in the page's language and direction."""
import io
import json
import os
import sys

REPO = r"C:\Users\777\nad-lan\nad-lan-co-il"
sys.path.insert(0, os.path.join(REPO, "scripts", "project-stage", "price_guide"))
sys.path.insert(0, os.path.join(REPO, "scripts", "project-stage", "area_map"))
import render as PG  # noqa: E402
import render_map as AM  # noqa: E402

OUT = os.path.dirname(os.path.abspath(__file__))
HEAD = {"he": ("רובע 4 בתל אביב: הצפון החדש", "(פסקת הפתיחה של העמוד)"),
        "en": ("Rova 4, Tel Aviv: the New North", "(The page's opening paragraph, translated elsewhere.)"),
        "fr": ("Rova 4 à Tel Aviv : le Nouveau Nord", "(Le paragraphe d’ouverture de la page, traduit ailleurs.)"),
        "ru": ("Рова 4 в Тель-Авиве: Новый Север", "(Вступительный абзац страницы, переводится отдельно.)"),
        "ar": ("روفاع 4 في تل أبيب: الشمال الجديد", "(الفقرة الافتتاحية للصفحة، تُترجم في مكان آخر.)")}
CSSX = """
body{margin:0;background:#f7f6f2;font-family:Assistant,"Segoe UI",Arial,sans-serif;color:#14212b}
.px{padding:24px 0 60px}
.px-ctx{max-width:1240px;margin:0 auto;padding:0 clamp(16px,3vw,32px);display:grid;gap:10px}
.px-h1{font-family:"Noto Serif Hebrew",Georgia,serif;font-weight:600;font-size:clamp(26px,4vw,34px);line-height:1.2;margin:0}
.px-lead{margin:0;font-size:17px;line-height:1.7;color:#3b4753}
.px-gap{max-width:1240px;margin:28px auto 0;padding:0 clamp(16px,3vw,32px)}
.px-gap div{height:600px;border-radius:22px;background:#1f4b5c}
"""


def page(lang):
    pgf = os.path.join(REPO, "scripts", "project-stage", "price_guide", "rova-4.json" if lang == "he" else "rova-4.%s.json" % lang)
    pd = json.load(io.open(pgf, encoding="utf-8"))
    md = AM.load("rova-4" if lang == "he" else "rova-4." + lang)
    u = PG.ui(pd)
    h1, lead = HEAD[lang]
    return ('<!doctype html>\n<html lang="%s" dir="%s"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">'
            '<title>Rova 4 components %s</title>'
            '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Noto+Serif+Hebrew:wght@500;600;700&amp;family=Assistant:wght@400;600;700&amp;display=swap">'
            '<style>%s%s%s</style></head><body><div class="px"><div class="px-ctx"><h1 class="px-h1">%s</h1><p class="px-lead">%s</p></div>'
            '%s%s<div class="px-gap"><div></div></div></div><script>%s</script><script>%s</script></body></html>\n') % (
        u["lang"], u["dir"], lang, CSSX, PG.CSS, AM.CSS, h1, lead, PG.html(pd, "972525101555"), AM.html(md), PG.JS, AM.JS)


if __name__ == "__main__":
    for lang in ("he", "en", "fr", "ru", "ar"):
        fn = os.path.join(OUT, lang + ".html")
        io.open(fn, "w", encoding="utf-8", newline="\n").write(page(lang))
        print("wrote", fn)
