# -*- coding: utf-8 -*-
"""HAD-801 hierarchy step 1 (Ben, 23.11.2026: "nothing is born without a parent"). The places list (/tour/sde-dov/places/) and the
tour's light page (/tour/sde-dov/) are children of /sde-dov/:
  - a small visible breadcrumb at the top (page language, RTL where the page is RTL) + BreadcrumbList JSON-LD with the same path;
    places: home > Sde Dov quarter > Sde Dov 2036 walk > Places and sources; tour: home > Sde Dov quarter > Sde Dov 2036 walk.
    On the tour the crumb sits in the blue card above the name and removes itself inside a frame (the host page is the parent).
  - places only: one plain line under the crumb ("the list is part of the guide to the Sde Dov quarter", the quarter linked), and
    the 21 source-citation links up to /sde-dov/ read the same words as the 22nd ("רובע שדה דב" / the page language's name).
Nothing else changes: no URL, title, H1, content order, robots or loading. Backup: backup-hierarchy.
  python hierarchy.py <site2 package dir> <manifest out>"""
import gzip, hashlib, json, os, re, sys
P, MAN = sys.argv[1], sys.argv[2]
assert "site2" in P
HOME = "https://nad-lan.co.il/"; HUB = "https://nad-lan.co.il/sde-dov/"; TOUR = "https://nad-lan.co.il/tour/sde-dov/"; LIST = TOUR + "places/"
L = {
 "he": dict(home="נדל״ן", hub="רובע שדה דב", tour="סיור שדה דב 2036", nav="מיקום באתר", old="נדל״ן, מגרשים, פרויקטים ושלבי בנייה",
            line='הרשימה היא חלק מהמדריך ל<a href="%s">רובע שדה דב</a>' % HUB),
 "en": dict(home="NadLan", hub="Sde Dov Quarter", tour="Sde Dov 2036 walk", nav="Where you are", old="Real Estate, plots, projects, and construction phases",
            line='This list is part of the guide to the <a href="%s">Sde Dov Quarter</a>.' % HUB),
 "fr": dict(home="NadLan", hub="Quartier Sde Dov", tour="Visite Sde Dov 2036", nav="Vous êtes ici", old="Immobilier, parcelles, projets et phases de construction",
            line='Cette liste fait partie du guide du <a href="%s">Quartier Sde Dov</a>.' % HUB),
 "ru": dict(home="NadLan", hub="Район Сде-Дов", tour="Прогулка Сде-Дов 2036", nav="Вы здесь", old="Недвижимость, участки, проекты и этапы строительства",
            line='Список входит в путеводитель «<a href="%s">Район Сде-Дов</a>».' % HUB),
 "ar": dict(home="NadLan", hub="منطقة سدي دوف", tour="جولة سدي دوف 2036", nav="موقعك في الموقع", old="العقارات، القسائم والمشاريع ومراحل البناء",
            line='هذه القائمة جزء من دليل <a href="%s">منطقة سدي دوف</a>.' % HUB),
}
def esc(s): return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")
def q(url, l): return url if l == "he" else url + "?lang=" + l
def jsonld(items):
    return ('<script type="application/ld+json">' + json.dumps({"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": i + 1, "name": n, "item": u} for i, (n, u) in enumerate(items)]}, ensure_ascii=False) + "</script>")
def crumbs(items, cls, label):
    parts = []
    for i, (n, u) in enumerate(items):
        parts.append('<span aria-current="page">%s</span>' % esc(n) if i == len(items) - 1 else '<a href="%s">%s</a>' % (u, esc(n)))
    return '<nav class="%s" aria-label="%s">%s</nav>' % (cls, esc(label), ' <span aria-hidden="true">›</span> '.join(parts))
PG = os.path.join(P, "pages"); stats = {}
for l, t in L.items():
    # places list
    p = os.path.join(PG, l + "-directory.html"); b = open(p, encoding="utf-8").read()
    if 'class="nlbc"' not in b:
        h1 = re.search(r'<h1 id="directory-title">(.*?)</h1>', b).group(1)
        items = [(t["home"], HOME), (t["hub"], HUB), (t["tour"], q(TOUR, l)), (re.sub("<[^>]+>", "", h1), q(LIST, l))]
        head = ('<style>.nlbc{font:500 13px/1.6 Heebo,Arial,sans-serif;color:#4a5f6b;padding:10px 1rem 0}.nlbc a{color:#17617c}'
                '.nlparent{padding:2px 1rem 6px;margin:0;font:400 15px/1.6 Heebo,Arial,sans-serif}.nlparent a{color:#17617c}</style>' + jsonld(items))
        assert b.count("</head>") == 1 and b.count("<main>") == 1
        b = b.replace("</head>", head + "</head>", 1).replace("<main>", "<main>" + crumbs(items, "nlbc", t["nav"]) + '<p class="nlparent">%s</p>' % t["line"], 1)
        old_a = re.compile(r'<a href="%s" target="_blank" rel="noopener noreferrer" aria-label="%s([^"]*)">%s</a>' % (re.escape(HUB), re.escape(t["old"]), re.escape(t["old"])))
        b, k = old_a.subn(lambda m: '<a href="%s" target="_blank" rel="noopener noreferrer" aria-label="%s%s">%s</a>' % (HUB, t["hub"], m.group(1), t["hub"]), b)
        open(p, "w", encoding="utf-8", newline="").write(b); open(p + ".gz", "wb").write(gzip.compress(b.encode("utf-8"), compresslevel=6, mtime=0))
        stats[l + "-directory"] = {"relinked": k, "hub_links_now": len(re.findall(r'href="%s"' % re.escape(HUB), b))}
    # tour light page
    p = os.path.join(PG, l + "-frame.html"); b = open(p, encoding="utf-8").read()
    if 'class="nlbc' not in b:
        items = [(t["home"], HOME), (t["hub"], HUB), (t["tour"], q(TOUR, l))]
        head = ('<style>#hud .identity .nlbc{display:block;font:500 11px/1.45 Heebo,Arial,sans-serif;color:#cfe0e8;margin:0 0 3px;max-width:100%%;white-space:normal}'
                '#hud .identity .nlbc a{color:#fff;text-decoration:underline;text-underline-offset:2px}</style>') + jsonld(items)
        anchor = '<div><h1>'
        assert b.count("</head>") == 1 and b.count(anchor) == 1, (l, b.count(anchor))
        guard = "<script>if(window.top!==window.self){var c=document.querySelector('#hud .nlbc');if(c)c.remove()}</script>"
        b = b.replace("</head>", head + "</head>", 1).replace(anchor, '<div>' + crumbs(items, "nlbc", t["nav"]) + guard + '<h1>', 1)
        open(p, "w", encoding="utf-8", newline="").write(b); open(p + ".gz", "wb").write(gzip.compress(b.encode("utf-8"), compresslevel=6, mtime=0))
        stats[l + "-frame"] = "crumb"
dg = {f: hashlib.sha256(open(os.path.join(PG, f), "rb").read()).hexdigest() for f in sorted(os.listdir(PG)) if f.endswith(".html")}
open(os.path.join(PG, "digests.json"), "w", encoding="utf-8", newline="\n").write(json.dumps(dg, indent=2) + "\n")
man = {}
for root, _, files in os.walk(P):
    for f in files:
        x = os.path.join(root, f); man[os.path.relpath(x, P).replace(os.sep, "/")] = {"bytes": os.path.getsize(x), "md5": hashlib.md5(open(x, "rb").read()).hexdigest()}
json.dump(man, open(MAN, "w", encoding="utf-8"), indent=0)
print(json.dumps(stats, ensure_ascii=False))
