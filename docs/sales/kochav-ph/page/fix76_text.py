# -*- coding: utf-8 -*-
"""Ben 27.10.2026: the terraces are 76 sqm (not 80), and the building has a gym and a residents' room.
The separate 74 sqm sun-terrace figure (from a Madlan listing, 74 + 4) no longer adds up with 76, so the pages speak of the
76 sqm total only. Applies the same replacements to round27.py's hero strings, to the pre-plan bases (the input of
round27_plan.py) and to the four pages' titles and Yoast meta (live76/<lang>.json -> <lang>.new.json for fix76_io.py --apply).
  python fix76_text.py            (French and Russian: the area facts only; their per-m² blocks wait for their own round)"""
import io, json, os, re, subprocess, sys
H = os.path.dirname(os.path.abspath(__file__)); D = os.path.join(H, "live76")
if hasattr(sys.stdout, "reconfigure"): sys.stdout.reconfigure(encoding="utf-8")
N = '<span class="nlx-num">%s</span>'
# (old, new, expected count) per language
HE = [("חדש עם 80 מ״ר מרפסות", "חדש עם 76 מ״ר מרפסות", None),
      ('<dt>מרפסות</dt><dd>כ-%s מ״ר</dd>' % (N % 80), '<dt>מרפסות</dt><dd>כ-%s מ״ר</dd>' % (N % 76), 1),
      ('<dt>מרפסות</dt><dd>%s מ״ר</dd>' % (N % 80), '<dt>מרפסות</dt><dd>%s מ״ר</dd>' % (N % 76), 1),
      ("בבניין בוטיק חדש: חמישה חדרים", "בבניין בוטיק חדש עם חדר כושר וחדר דיירים: חמישה חדרים", 1),
      ("במרפסת השמש הרחבה (כ-%s מ״ר), הנהנית" % (N % 74), "במרפסת השמש הרחבה, הנהנית", 1),
      ("<b>%s מ״ר מרפסות</b>" % (N % 80), "<b>%s מ״ר מרפסות</b>" % (N % 76), 1),
      ("<dd>%s מ״ר בסך הכול</dd>" % (N % 80), "<dd>%s מ״ר בסך הכול</dd>" % (N % 76), 1),
      ("<li><b>מרפסת שמש של כ-74 מ״ר</b><span>בערך פי שלושה מ-25 מ״ר, הגודל שמקובל בשוק לראות בו מיני פנטהאוז. עם שאר המרפסות, כ-80 מ״ר בחוץ.</span></li>",
       "<li><b>כ-76 מ״ר של מרפסות</b><span>בערך פי שלושה מ-25 מ״ר, הגודל שמקובל בשוק לראות בו מיני פנטהאוז.</span></li>", 1),
      ("מרפסת שמש של כ-%s מ״ר (בערך פי שלושה מ-%s מ״ר) ויחד עם שאר המרפסות כ-%s מ״ר," % (N % 74, N % 25, N % 80),
       "מרפסות של כ-%s מ״ר (בערך פי שלושה מ-%s מ״ר)," % (N % 76, N % 25), 1),
      ("מרפסת שמש של כ-74 מ״ר (בערך פי שלושה מ-25 מ״ר) ויחד עם שאר המרפסות כ-80 מ״ר,", "מרפסות של כ-76 מ״ר (בערך פי שלושה מ-25 מ״ר),", 1),
      ("ומרפסות של 80 מ״ר", "ומרפסות של 76 מ״ר", 1),
      ('"name": "מרפסות 80 מ״ר"', '"name": "מרפסות 76 מ״ר"', 1),
      ("ובבניין חדר כושר לדיירים.", "ובבניין חדר כושר וחדר דיירים.", 1),
      ("<dt>שירותים לדיירים</dt><dd>חדר כושר</dd>", "<dt>שירותים לדיירים</dt><dd>חדר כושר וחדר דיירים</dd>", 1),
      ('{"@type": "LocationFeatureSpecification", "name": "חדר כושר", "value": true}',
       '{"@type": "LocationFeatureSpecification", "name": "חדר כושר", "value": true}, {"@type": "LocationFeatureSpecification", "name": "חדר דיירים", "value": true}', 1)]
EN = [("New Mini Penthouse with 80 sqm of Terraces", "New Mini Penthouse with 76 sqm of Terraces", None),
      ("חדש עם 80 מ״ר מרפסות", "חדש עם 76 מ״ר מרפסות", None),
      ('<dt>Terraces</dt><dd>≈&nbsp;%s sqm</dd>' % (N % 80), '<dt>Terraces</dt><dd>≈&nbsp;%s sqm</dd>' % (N % 76), 1),
      ('<dt>Terraces</dt><dd>%s sqm</dd>' % (N % 80), '<dt>Terraces</dt><dd>%s sqm</dd>' % (N % 76), 1),
      ("in a new boutique building: five rooms", "in a new boutique building with a gym and a residents' room: five rooms", 1),
      ("on the wide sun terrace (about %s m²), open on" % (N % 74), "on the wide sun terrace, open on", 1),
      ("<b>%s sqm of terraces</b>" % (N % 80), "<b>%s sqm of terraces</b>" % (N % 76), 1),
      ("<dd>%s sqm in total</dd>" % (N % 80), "<dd>%s sqm in total</dd>" % (N % 76), 1),
      ("<li><b>A sun terrace of about 74 sqm</b><span>About three times the 25 sqm the market usually expects of a mini penthouse. With the other balconies, about 80 sqm outdoors.</span></li>",
       "<li><b>About 76 sqm of terraces</b><span>About three times the 25 sqm the market usually expects of a mini penthouse.</span></li>", 1),
      ("a sun terrace of about %s sqm (about three times %s sqm) and about %s sqm with the other balconies," % (N % 74, N % 25, N % 80),
       "about %s sqm of terraces (about three times %s sqm)," % (N % 76, N % 25), 1),
      ("a sun terrace of about 74 sqm (about three times 25 sqm) and about 80 sqm with the other balconies,", "about 76 sqm of terraces (about three times 25 sqm),", 1),
      ("about 197 sqm plus 80 sqm of terraces", "about 197 sqm plus 76 sqm of terraces", 1),
      ('"name": "80 sqm terraces"', '"name": "76 sqm terraces"', 1),
      ("and a residents' gym in the building.", "and a gym and a residents' room in the building.", 1),
      ("<dt>Resident services</dt><dd>Gym</dd>", "<dt>Resident services</dt><dd>Gym and residents&#x27; room</dd>", 1),
      ('{"@type": "LocationFeatureSpecification", "name": "Gym", "value": true}',
       '{"@type": "LocationFeatureSpecification", "name": "Gym", "value": true}, {"@type": "LocationFeatureSpecification", "name": "Residents\' room", "value": true}', 1)]
# French and Russian: area facts only (titles, facts, highlights, rows, FAQ, schema); the per-m² ledger, bars and calculator
# still carry 80 as their input and go away with those pages' own round (Meital: no price per m² on this listing).
FR = [("et autour d’elles %s de terrasses" % (N % "80 m²"), "et autour d’elles %s de terrasses" % (N % "76 m²"), 1),
      ("<dt>Terrasses</dt><dd>%s</dd>" % (N % "80 m²"), "<dt>Terrasses</dt><dd>%s</dd>" % (N % "76 m²"), 1),
      ("sur la grande terrasse ensoleillée (environ %s), ouverte" % (N % "74 m²"), "sur la grande terrasse ensoleillée, ouverte", 1),
      ("<b>%s de terrasses</b>" % (N % "80 m²"), "<b>%s de terrasses</b>" % (N % "76 m²"), 1),
      ("<dd>%s au total, dont une terrasse ensoleillée d’environ %s</dd>" % (N % "80 m²", N % "74 m²"), "<dd>%s au total</dd>" % (N % "76 m²"), 1),
      ("<li><b>Une terrasse ensoleillée d’environ 74 m²</b><span>Environ trois fois les 25 m² que le marché attend habituellement d’un mini-penthouse. Avec les autres balcons, environ 80 m² en extérieur.</span></li>",
       "<li><b>Environ 76 m² de terrasses</b><span>Environ trois fois les 25 m² que le marché attend habituellement d’un mini-penthouse.</span></li>", 1),
      ("habitables et %s de terrasses, est proposé" % (N % "80 m²"), "habitables et %s de terrasses, est proposé" % (N % "76 m²"), 1),
      ("une terrasse ensoleillée d’environ %s (environ trois fois %s) et environ %s avec les autres balcons," % (N % "74 m²", N % "25 m²", N % "80 m²"),
       "environ %s de terrasses (environ trois fois %s)," % (N % "76 m²", N % "25 m²"), 1),
      ("une terrasse ensoleillée d’environ 74 m² (environ trois fois 25 m²) et environ 80 m² avec les autres balcons,", "environ 76 m² de terrasses (environ trois fois 25 m²),", 1),
      ("environ 197 m² et 80 m² de terrasses", "environ 197 m² et 76 m² de terrasses", 1),
      ('"name": "80 m² de terrasses"', '"name": "76 m² de terrasses"', 1),
      ("habitables et 80 m² de terrasses, est proposé", "habitables et 76 m² de terrasses, est proposé", 1),
      ("et une salle de sport pour les résidents dans l’immeuble.", "et une salle de sport et une salle commune pour les résidents dans l’immeuble.", 1),
      ("<dd>Salle de sport</dd>", "<dd>Salle de sport, salle commune</dd>", 1),
      ('{"@type": "LocationFeatureSpecification", "name": "Salle de sport", "value": true}',
       '{"@type": "LocationFeatureSpecification", "name": "Salle de sport", "value": true}, {"@type": "LocationFeatureSpecification", "name": "Salle commune des résidents", "value": true}', 1)]
RU = [("и %s террас с видом" % (N % "80 м²"), "и %s террас с видом" % (N % "76 м²"), 1),
      ("<dt>Террасы</dt><dd>%s</dd>" % (N % "80 м²"), "<dt>Террасы</dt><dd>%s</dd>" % (N % "76 м²"), 1),
      ("на большой солнечной террасе (около %s), открытой" % (N % "74 м²"), "на большой солнечной террасе, открытой", 1),
      ("<b>%s террас</b>" % (N % "80 м²"), "<b>%s террас</b>" % (N % "76 м²"), 1),
      ("<dd>%s в сумме, из них солнечная терраса около %s</dd>" % (N % "80 м²", N % "74 м²"), "<dd>%s в сумме</dd>" % (N % "76 м²"), 1),
      ("<li><b>Солнечная терраса около 74 м²</b><span>Примерно втрое больше 25 м², которые рынок обычно ожидает от мини-пентхауса. Вместе с другими балконами около 80 м² открытого пространства.</span></li>",
       "<li><b>Около 76 м² террас</b><span>Примерно втрое больше 25 м², которые рынок обычно ожидает от мини-пентхауса.</span></li>", 1),
      ("%s и %s террас продаётся" % (N % "197 м²", N % "80 м²"), "%s и %s террас продаётся" % (N % "197 м²", N % "76 м²"), 1),
      ("солнечная терраса около %s (примерно втрое больше %s) и около %s вместе с другими балконами," % (N % "74 м²", N % "25 м²", N % "80 м²"),
       "около %s террас (примерно втрое больше %s)," % (N % "76 м²", N % "25 м²"), 1),
      ("солнечная терраса около 74 м² (примерно втрое больше 25 м²) и около 80 м² вместе с другими балконами,", "около 76 м² террас (примерно втрое больше 25 м²),", 1),
      ("около 197 м² и 80 м² террас", "около 197 м² и 76 м² террас", 1),
      ('"name": "Террасы 80 м²"', '"name": "Террасы 76 м²"', 1),
      ("197 м² и 80 м² террас продаётся", "197 м² и 76 м² террас продаётся", 1),
      ("а в доме есть тренажёрный зал для жителей.", "а в доме есть тренажёрный зал и комната для жильцов.", 1),
      ("<dd>Тренажёрный зал</dd>", "<dd>Тренажёрный зал, комната для жильцов</dd>", 1),
      ('{"@type": "LocationFeatureSpecification", "name": "Тренажёрный зал", "value": true}',
       '{"@type": "LocationFeatureSpecification", "name": "Тренажёрный зал", "value": true}, {"@type": "LocationFeatureSpecification", "name": "Комната для жильцов", "value": true}', 1)]
TITLE = {"he": ("מיני פנטהאוז 5 חדרים עם מרפסת של 80 מ״ר, כוכב הצפון", "מיני פנטהאוז 5 חדרים עם 76 מ״ר מרפסות, כוכב הצפון"),
         "en": ("Five-Room Mini Penthouse with 80 sqm Balcony, Kochav HaTzafon", "Five-Room Mini Penthouse with 76 sqm of Terraces, Kochav HaTzafon")}
DESC = {"he": [("מרפסת 80 מ״ר", "76 מ״ר מרפסות"), ("חדר כושר לדיירים", "חדר כושר וחדר דיירים")],
        "en": [("80 sqm balcony", "76 sqm of terraces"), ("residents' gym", "a gym and residents' room")],
        "fr": [("80 m² de terrasses", "76 m² de terrasses")], "ru": [("террасы 80 м²", "террасы 76 м²")]}
NB = lambda x: re.sub(r"(\d) (m²|м²)", lambda m: m.group(1) + " " + m.group(2), x)  # French and Russian keep a no-break space before the unit
FR = [(NB(a), NB(b), n) for a, b, n in FR]; RU = [(NB(a), NB(b), n) for a, b, n in RU]
REPL = {"he": HE, "en": EN, "fr": FR, "ru": RU}


def apply(t, pairs, label):
    for a, b, n in pairs:
        c = t.count(a)
        assert c >= 1 if n is None else c == n, (label, c, a[:80])
        t = t.replace(a, b)
    return t


# 1. round27.py: the hero strings (the source of the opening)
p = os.path.join(H, "round27.py"); s = io.open(p, encoding="utf-8", newline="").read()
for a, b in (('title="מיני פנטהאוז חדש עם 80 מ״ר מרפסות, כוכב הצפון"', 'title="מיני פנטהאוז חדש עם 76 מ״ר מרפסות, כוכב הצפון"'),
             ('("מרפסות", \'כ-<span class="nlx-num">80</span> מ״ר\')', '("מרפסות", \'כ-<span class="nlx-num">76</span> מ״ר\')'),
             ('dek="קומה אחת מתחת לאחרונה, בבניין בוטיק חדש: חמישה', 'dek="קומה אחת מתחת לאחרונה, בבניין בוטיק חדש עם חדר כושר וחדר דיירים: חמישה'),
             ('title="New Mini Penthouse with 80 sqm of Terraces, Kochav HaTzafon"', 'title="New Mini Penthouse with 76 sqm of Terraces, Kochav HaTzafon"'),
             ('("Terraces", \'≈&nbsp;<span class="nlx-num">80</span> sqm\')', '("Terraces", \'≈&nbsp;<span class="nlx-num">76</span> sqm\')'),
             ('dek="One floor below the top, in a new boutique building: five', 'dek="One floor below the top, in a new boutique building with a gym and a residents\' room: five')):
    if b not in s: assert s.count(a) == 1, a; s = s.replace(a, b)
io.open(p, "w", encoding="utf-8", newline="").write(s)
# 2. the pre-plan bases, then the rebuild
rd = lambda f: io.open(os.path.join(H, f), encoding="utf-8", newline="").read().replace("\r\n", "\n")
for lang, pid in (("he", 7634), ("en", 7812)):
    f = "live-27-preplan-%d.html" % pid; t = rd(f)
    if "76 מ״ר מרפסות" not in t: io.open(os.path.join(H, f), "w", encoding="utf-8", newline="").write(apply(t, REPL[lang], f))
subprocess.run([sys.executable, os.path.join(H, "round27_plan.py")], check=True, cwd=H)
# 3. the four pages: content, title, meta -> <lang>.new.json; the rebuilt he/en must equal live + these replacements only
for lang in ("he", "en", "fr", "ru"):
    o = json.load(io.open(os.path.join(D, "%s.json" % lang), encoding="utf-8"))
    want = apply(o["content"].replace("\r\n", "\n"), REPL[lang], lang)
    if lang in ("he", "en"):
        got = rd("after-27-%d.html" % o["id"])
        print(lang, "rebuild == live + replacements:", got == want); assert got == want
    n = dict(o); n["content"] = want
    if lang in TITLE: assert o["title"] == TITLE[lang][0], o["title"]; n["title"] = TITLE[lang][1]
    n["meta"] = dict(o["meta"])
    for k in ("_yoast_wpseo_metadesc", "_yoast_wpseo_opengraph-description", "_yoast_wpseo_twitter-description"):
        v = n["meta"].get(k) or ""
        for a, b in DESC[lang]:
            if a in v: v = v.replace(a, b)
        if v: n["meta"][k] = v
    assert DESC[lang][0][1] in n["meta"]["_yoast_wpseo_metadesc"], (lang, n["meta"]["_yoast_wpseo_metadesc"])
    left = [re.sub(r"\s+", " ", re.sub(r"<[^>]+>", "", want[max(0, m.start() - 70):m.end() + 30]))
            for m in re.finditer(r"(?<![\d,. ])(80|74)(?:</span>)?(?:&nbsp;| )?(?:<span[^>]*>)?(?:מ״ר|sqm|m²|м²)", want)]
    print(lang, "title:", n["title"][:70], "| desc:", n["meta"]["_yoast_wpseo_metadesc"], "| 80/74 area left:", len(left))
    for x in left: print("    ", x)
    io.open(os.path.join(D, "%s.new.json" % lang), "w", encoding="utf-8").write(json.dumps(n, ensure_ascii=False, indent=1))
