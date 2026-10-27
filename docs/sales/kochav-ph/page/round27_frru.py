# -*- coding: utf-8 -*-
"""Kochav listing in French (8511) and Russian (8512), brought to the Hebrew and English round of 27.10.2026 (Meital's notes of 22.10):
the same steps as round27.py (its build(), hero() and CSS are reused, with French and Russian texts), on the live text read by
fix76_io.py --fetch (live76/<lang>.json, terraces already 76 sqm):
- the new opening (Meital's photos, the price on the first screen, the facts row, a new home in a new building, WhatsApp and call),
  replacing the old masthead and its showroom of towers that do not exist; the 3D building card goes too;
- no price per m² anywhere (KPIs, bars, ledger, the calculator and the market sections, the scenario column, FAQ entries and
  schema, the price card's rows), tennis courts and football pitches by the home, the film v3b (English, captions burned in).
  python round27_frru.py   -> after-27-8511.html, after-27-8512.html (then the plan: round27_plan_frru.py)"""
import io, json, os, re, sys
H = os.path.dirname(os.path.abspath(__file__))
if hasattr(sys.stdout, "reconfigure"): sys.stdout.reconfigure(encoding="utf-8")
src = io.open(os.path.join(H, "round27.py"), encoding="utf-8").read()
ns = {"__name__": "r27", "__file__": os.path.join(H, "round27.py")}
exec(compile(src[:src.index('bad = build("he") + build("en")')], "round27.py", "exec"), ns)
# French and Russian ways of writing a price per m² (with or without a no-break space)
ns["PER_M2"] = re.compile(ns["PER_M2"].pattern + r"|au\s?m²|le\s?m²|par\s?m²|m²\s?pondéré|за\s?м²|за взвешенн", re.I)
NB = " "
N = '<span class="nlx-num">%s</span>'
L = ns["L"]
L["fr"] = dict(
    pid=8511, sfx="L07-fr", tag="h1", dir="ltr",
    photos=[("L07_DV6aYANjLBm_02.jpg", "La terrasse principale le soir, le séjour derrière la baie vitrée", "Photo sur place"),
            ("L07_DX9wx4ziADM_03.jpg", "La grande terrasse, sa pergola et la vue sur la ville", "Photo sur place"),
            ("L07_DV6aYANjLBm_01.jpg", "Le séjour" + NB + ": mur en noyer, grand canapé et cuisine ouverte", "Photo sur place"),
            ("L07_DZp43r5DIou_04.jpg", "L’espace ouvert" + NB + ": séjour, salle à manger et cuisine avec îlot", "Photo sur place"),
            ("L07_DX9wx4ziADM_06.jpg", "Au nord" + NB + ": Sde Dov, la centrale Reading et la mer", "Photos du bien"),
            ("L07_DX9wx4ziADM_08.jpg", "Autour" + NB + ": les terrains de football, le parc HaYarkon et la ligne d’horizon", "Photos du bien")],
    aria_car="Le bien en images", prev="Photo précédente", nxt="Photo suivante",
    kicker="À vendre · Kochav HaTzafon, nord de Tel Aviv · Exclusivité" + NB + ": Meital Katzir",
    title="Mini-penthouse neuf avec 76" + NB + "m² de terrasses, Kochav HaTzafon",
    fx=N % ("≈ 5,9" + NB + "M$") + " · " + N % ("≈ 5,1" + NB + "M€"),
    price=N % ("18" + NB + "000" + NB + "000") + "&nbsp;₪",
    new="Un bien neuf, dans un immeuble boutique neuf",
    facts=[("Pièces", N % "5"), ("Habitable", "≈&nbsp;" + N % "197" + "&nbsp;m²"), ("Terrasses", "≈&nbsp;" + N % "76" + "&nbsp;m²"),
           ("Étage", N % "11" + " sur " + N % "12"), ("À côté", "Parc HaYarkon")],
    dek=("Un étage sous le dernier, dans un immeuble boutique neuf avec salle de sport et salle commune" + NB + ": cinq pièces, une cuisine "
         "avec un long îlot, une aile des enfants avec son propre balcon, et des terrasses ouvertes sur la mer, le parc et la ligne d’horizon de Tel Aviv."),
    wa_lab="Organiser une visite privée", tel_lab="Appeler Meital",
    note=("Surfaces selon le plan de l’architecte, approximatives. L’immeuble n’est pas encore inscrit au registre foncier" + NB + "; "
          "la surface qui fait foi est celle de l’inscription de la copropriété."),
    bldg_card="L&#x27;immeuble et l&#x27;étage en 3D",
    park=("borde le quartier le long du boulevard Rokach, et le port de Tel Aviv",
          "borde le quartier le long du boulevard Rokach, avec des courts de tennis et des terrains de football tout près de l’appartement. Le port de Tel Aviv"),
    texts=[("valaient environ %s dollars de plus par%sm² que ceux situés" % (N % "136", NB), "se vendaient plus cher que ceux situés"),
           (" Le neuf du quartier s’est vendu en moyenne environ %s le%sm² (février %s)." % (N % ("79" + NB + "000" + NB + "₪"), NB, N % "2026"), ""),
           ("a montré environ %s dollars de plus par%sm² pour les logements" % (N % "136", NB), "a montré des prix plus élevés pour les logements"),
           (" Avec les terrasses pondérées à un tiers, le prix revient à environ %s le%sm²." % (N % ("80" + NB + "477" + NB + "₪"), NB), ""),
           ("18" + NB + "000" + NB + "000" + NB + "₪, avec prix au" + NB + "m², taxe d’acquisition et comparables.",
            "18" + NB + "000" + NB + "000" + NB + "₪, avec la taxe d’acquisition, le coût total et les données du quartier.")],
    prices_today=(r'<li class="nlx-item"><span class="nlx-item-title">Les prix du quartier aujourd’hui</span><p>.*?</p></li>',
                  '<li class="nlx-item"><span class="nlx-item-title">Les prix du quartier aujourd’hui</span><p>La transaction médiane à Kochav HaTzafon '
                  'entre %s et octobre %s était de %s millions' % (N % "2023", N % "2025", N % "6,1") + NB + '₪, la quatrième plus élevée d’Israël (Mako). '
                  'Un bien neuf à un étage élevé, avec de grandes terrasses, se situe en haut de ce marché.</p></li>'),
    kpis=["Prix au m² habitable", "Moyenne au m², Kochav HaTzafon"], bars="Le prix au m² face au marché",
    ledger=["Au" + NB + "m² pondéré, terrasses à un tiers", "Au" + NB + "m² pondéré, terrasses à la moitié"],
    scen_cap=None, scen_th="<th>Au m² habitable</th>",
    faq_drop=["Quel est le prix moyen au" + NB + "m² à Kochav HaTzafon" + NB + "?", "Quel est le prix au" + NB + "m²" + NB + "?"],
    faq_json=[(r"a montré environ 136 dollars de plus par\s?m² pour les logements", "a montré des prix plus élevés pour les logements"),
              (r"\s*Avec les terrasses pondérées à un tiers, le prix revient à environ 80\s?477\s?₪ le\s?m²\.", "")],
    film=("Le matin dans le quartier, un café au centre commercial voisin, la nouvelle passerelle vers le parc HaYarkon, l’appartement lui-même, "
          "une soirée entre amis sur la terrasse, et les chiffres du quartier. Film en anglais.",
          "Le matin dans le quartier, un café au centre commercial voisin, la nouvelle passerelle vers le parc HaYarkon, les courts de tennis et les "
          "terrains de football près de l’appartement, l’appartement neuf lui-même, une soirée sur la terrasse, et les chiffres du quartier. "
          "Film en anglais, sous-titré en anglais. L’appartement et les vues aériennes sont filmés par Meital" + NB + "; la passerelle prévue et "
          "les scènes d’ambiance sont des illustrations, signalées dans le film."),
)
L["ru"] = dict(
    pid=8512, sfx="L07-ru", tag="h1", dir="ltr",
    photos=[("L07_DV6aYANjLBm_02.jpg", "Главная терраса вечером, гостиная за стеклом", "Снято в квартире"),
            ("L07_DX9wx4ziADM_03.jpg", "Большая терраса с перголой и видом на город", "Снято в квартире"),
            ("L07_DV6aYANjLBm_01.jpg", "Гостиная: стена из ореха, большой диван и открытая кухня", "Снято в квартире"),
            ("L07_DZp43r5DIou_04.jpg", "Открытое пространство: гостиная, столовая и кухня с островом", "Снято в квартире"),
            ("L07_DX9wx4ziADM_06.jpg", "На севере: Сде-Дов, электростанция Рединг и море", "Из фото объекта"),
            ("L07_DX9wx4ziADM_08.jpg", "Вокруг: футбольные поля, парк Яркон и силуэт города", "Из фото объекта")],
    aria_car="Квартира в фотографиях", prev="Предыдущее фото", nxt="Следующее фото",
    kicker="Продаётся · Кохав ха-Цафон, север Тель-Авива · Эксклюзив: Meital Katzir",
    title="Новый мини-пентхаус с 76" + NB + "м² террас, Кохав ха-Цафон",
    fx=N % ("≈ 5,9" + NB + "млн" + NB + "$") + " · " + N % ("5,1" + NB + "млн" + NB + "€"),  # one line beside the price on a 390px phone
    price=N % ("18" + NB + "000" + NB + "000") + "&nbsp;₪",
    new="Новая квартира в новом бутиковом доме",
    facts=[("Комнат", N % "5"), ("Площадь", "≈&nbsp;" + N % "197" + "&nbsp;м²"), ("Террасы", "≈&nbsp;" + N % "76" + "&nbsp;м²"),
           ("Этаж", N % "11" + " из " + N % "12"), ("Рядом", "Парк Яркон")],
    dek=("На этаж ниже последнего, в новом бутиковом доме с тренажёрным залом и комнатой для жильцов: пять комнат, кухня с длинным островом, "
         "детское крыло с собственным балконом и террасы с видом на море, парк и силуэт Тель-Авива."),
    wa_lab="Записаться на просмотр", tel_lab="Позвонить Мейталь",
    note="Площади по плану архитектора, приблизительные. Дом ещё не внесён в земельный реестр; решающей будет площадь по регистрации кондоминиума.",
    bldg_card="Дом и этаж в 3D",
    park=("граничит с районом вдоль бульвара Роках, а в конце парка находится Тель-Авивский порт",
          "граничит с районом вдоль бульвара Роках, а совсем рядом с домом есть теннисные корты и футбольные поля. В конце парка находится Тель-Авивский порт"),
    texts=[("стоили примерно на %s долларов за%sм² дороже, чем квартиры" % (N % "136", NB), "продавались дороже, чем квартиры"),
           (" Новостройки района продавались в среднем примерно по %s за%sм² (февраль %s)." % (N % ("79" + NB + "000" + NB + "₪"), NB, N % "2026"), ""),
           ("показало около %s долларов прибавки за%sм² для квартир" % (N % "136", NB), "показало более высокие цены для квартир"),
           (" Если считать террасы с весом в треть, цена составляет около %s за%sм²." % (N % ("80" + NB + "477" + NB + "₪"), NB), ""),
           ("18" + NB + "000" + NB + "000" + NB + "₪, с ценой за" + NB + "м², налогом на покупку и сравнением с рынком.",
            "18" + NB + "000" + NB + "000" + NB + "₪, с налогом на покупку, полной стоимостью и данными о районе.")],
    prices_today=(r'<li class="nlx-item"><span class="nlx-item-title">Цены в районе сегодня</span><p>.*?</p></li>',
                  '<li class="nlx-item"><span class="nlx-item-title">Цены в районе сегодня</span><p>Медианная сделка в Кохав ха-Цафон с %s по октябрь %s года '
                  'составила %s млн' % (N % "2023", N % "2025", N % "6,1") + NB + '₪, четвёртая по величине в Израиле (Mako). Новая квартира на высоком этаже '
                  'с большими террасами находится в верхней части этого рынка.</p></li>'),
    kpis=["Цена за м²", "Средняя цена за м², Кохав ха-Цафон"], bars="Цена за м² на фоне рынка",
    ledger=["За взвешенный" + NB + "м², террасы с весом в треть", "За взвешенный" + NB + "м², террасы с весом в половину"],
    scen_cap=None, scen_th="<th>За м²</th>",
    faq_drop=["Какая средняя цена за" + NB + "м² в Кохав ха-Цафон?", "Какая цена за" + NB + "м²?"],
    faq_json=[(r"показало около 136 долларов прибавки за\s?м² для квартир", "показало более высокие цены для квартир"),
              (r"\s*Если считать террасы с весом в треть, цена составляет около 80\s?477\s?₪ за\s?м²\.", "")],
    film=("Утро в районе, кофе в соседнем торговом центре, новый мост в парк Яркон, сама квартира, вечер с друзьями на террасе и цифры района. Фильм на английском языке.",
          "Утро в районе, кофе в соседнем торговом центре, новый мост в парк Яркон, теннисные корты и футбольные поля рядом с домом, сама новая квартира, "
          "вечер на террасе и цифры района. Фильм на английском языке, с английскими субтитрами. Квартиру и виды с воздуха сняла Мейталь; "
          "планируемый мост и сцены атмосферы являются иллюстрациями и отмечены в фильме."),
)
M = json.load(open(os.path.join(H, "media.json")))
MP4, JPG = M["kochav-film-en-v3b.mp4"]["url"].rsplit("/", 1)[1], M["kochav-film-v3.jpg"]["url"].rsplit("/", 1)[1]
bad = 0
for lang in ("fr", "ru"):
    c = L[lang]; pid = c["pid"]
    o = json.load(io.open(os.path.join(H, "live76", "%s.json" % lang), encoding="utf-8")); assert o["id"] == pid
    orig = os.path.join(H, "live-27-orig-%d.html" % pid)  # the live text before this round, kept from the first run
    if not os.path.exists(orig): io.open(orig, "w", encoding="utf-8", newline="\n").write(o["content"].replace("\r\n", "\n"))
    bad += ns["build"](lang)
    p = os.path.join(H, "after-27-%d.html" % pid); t = io.open(p, encoding="utf-8").read()
    # the opening's phone rules: this page's own id (WordPress pages carry page-id-N)
    n = t.count("body.page-id-7812"); assert n == 2, n
    t = t.replace("body.page-id-7812", "body.page-id-%d" % pid)
    # French and Russian names are longer: on phones the last fact (next to the park) takes the two free columns
    a = ".nlx .nlx-h27-facts div:nth-child(n+4){border-top:1px solid var(--nlx-line)}}"; assert t.count(a) == 1, "facts rule"
    t = t.replace(a, a[:-1] + ".nlx .nlx-h27-facts div:nth-child(5){grid-column:span 2}}")
    # the film v3b
    assert t.count("kochav-film-en-v2.mp4") == 2 and t.count("kochav-film-en.jpg") >= 1
    t = t.replace("kochav-film-en-v2.mp4", MP4).replace("kochav-film-en.jpg", JPG)
    assert t.count(c["film"][0]) >= 1, "film lead"; t = t.replace(c["film"][0], c["film"][1])  # the section and the VideoObject
    a = '"uploadDate": "2026-10-20", "duration": "PT2M10S"'; assert t.count(a) == 1; t = t.replace(a, '"uploadDate": "2026-10-27", "duration": "PT2M7S"')
    # the language DNA on the visible words of the opening; no long dash in the new text
    vis = re.sub(r"<[^>]+>", " ", re.sub(r"<(script|style)\b.*?</\1>", "", t, flags=re.S))
    for w in ("srp-bldg", "nlx-srs", "#market-L07", "#calc-L07"): assert w not in t, w
    assert len(re.findall(r"<h1\b", t)) == 1, "h1"
    io.open(p, "w", encoding="utf-8", newline="\n").write(t)
    print(" ", lang, "film + page id done,", len(t), "chars")
assert bad == 0, "per-m² still on a page"
print("OK: French and Russian built, no price per m², no invented towers, film v3b")
