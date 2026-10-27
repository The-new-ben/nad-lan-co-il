# -*- coding: utf-8 -*-
"""The architect's plan section on the French (8511) and Russian (8512) Kochav pages, as round27_plan.py does for Hebrew and English:
the plan with room names and no dimensions, the rendering toggle, a tap on a room marks it and shows Meital's photo when one exists,
quick links in the opening. The drawings plan/svg/plan-lux-fr.svg and plan-lux-ru.svg are the English drawing with French and
Russian labels (written here). The film was already swapped by round27_frru.py.
  python round27_plan_frru.py   (reads the live text live76/<lang>.json as the pre-plan base) -> after-27p-8511.html, after-27p-8512.html"""
import io, json, os, re, sys
H = os.path.dirname(os.path.abspath(__file__)); PLAN = os.path.join(os.path.dirname(H), "plan")
if hasattr(sys.stdout, "reconfigure"): sys.stdout.reconfigure(encoding="utf-8")
NB = " "
# label per data-for (a list = two lines, as the English drawing does), and the drawing's other labels
LAB = {
 "fr": {"living": "Séjour", "dining": "Salle à manger", "kitchen": "Cuisine", "entry": "Vestibule", "corridor": "Couloir", "wc": ["WC", "invités"],
        "room_a": ["Pièce", "en plus"], "bed1": "Chambre", "bed2": ["Chambre", "parentale"], "bed3": "Chambre", "closet": "Pièce de la suite",
        "ensuite": ["Salle de bains", "parentale"], "bath": "Salle de bains", "laundry": "Buanderie", "ledge": ["Séchoir", "à linge"],
        "terrace": "Toit-terrasse", "balcony": "Balcon", "service": "Balcon de service",
        "_": {"Lifts and stairs": "Ascenseurs et escalier", "Entrance": "Entrée", "Pergola": "Pergola"}},
 "ru": {"living": "Гостиная", "dining": "Столовая", "kitchen": "Кухня", "entry": "Прихожая", "corridor": "Коридор", "wc": ["Гостевой", "туалет"],
        "room_a": ["Ещё одна", "комната"], "bed1": "Спальня", "bed2": ["Главная", "спальня"], "bed3": "Спальня", "closet": "Комната в сюите",
        "ensuite": ["Ванная", "в сюите"], "bath": "Ванная", "laundry": "Прачечная", "ledge": ["Ниша", "для сушки"],
        "terrace": ["Терраса", "на крыше"], "balcony": "Балкон", "service": "Служебный балкон",
        "_": {"Lifts and stairs": "Лифты и лестница", "Entrance": "Вход", "Pergola": "Пергола"}}}
FULL = {"fr": {"room_a": "Pièce en plus", "bed2": "Chambre parentale", "wc": "WC invités", "ensuite": "Salle de bains parentale", "ledge": "Séchoir à linge"},
        "ru": {"room_a": "Ещё одна комната", "bed2": "Главная спальня", "wc": "Гостевой туалет", "ensuite": "Ванная в сюите", "ledge": "Ниша для сушки", "terrace": "Терраса на крыше"}}
# phone label sizes, as the English and Hebrew rules (the drawing is about 0.09 of its size on a 390px phone)
PHONE_CSS = {"fr": "html body .nlx .np-svg[lang=fr] text[data-for=living]{font-size:120px}html body .nlx .np-svg[lang=fr] text[data-for=terrace]{font-size:72px}"
                   "html body .nlx .np-svg[lang=fr] text[data-for=dining]{font-size:70px}",
             "ru": "html body .nlx .np-svg[lang=ru] text[data-for=living]{font-size:104px}html body .nlx .np-svg[lang=ru] text[data-for=terrace]{font-size:92px}"
                   "html body .nlx .np-svg[lang=ru] text[data-for=dining]{font-size:90px}"}


def drawing(lang):
    s = io.open(os.path.join(PLAN, "svg", "plan-lux-en.svg"), encoding="utf-8").read()
    s = s.replace('lang="en"', 'lang="%s"' % lang, 1)
    lab = LAB[lang]

    def one(m):
        attrs, inner = m.group(1), m.group(2)
        d = re.search(r'data-for="([^"]+)"', attrs)
        if d:
            v = lab[d.group(1)]
            if isinstance(v, list):
                xs = re.findall(r'<tspan x="([^"]+)"', inner)
                x = xs[0] if xs else re.search(r'\bx="([^"]+)"', attrs).group(1)
                inner = '<tspan x="%s" dy="-0.2em">%s</tspan><tspan x="%s" dy="1.05em">%s</tspan>' % (x, v[0], x, v[1])
            else:
                inner = v
        elif inner.strip() in lab["_"]:
            inner = lab["_"][inner.strip()]
        return "<text%s>%s</text>" % (attrs, inner)
    s = re.sub(r"<text\b([^>]*)>(.*?)</text>", one, s, flags=re.S)
    # the rooms' own names (data-name, aria-label) read by the page's script and by screen readers
    full = {k: FULL[lang].get(k, v if isinstance(v, str) else " ".join(v)) for k, v in lab.items() if k != "_"}

    def tag(m):
        g, rid = m.group(0), m.group(1)
        if rid not in full: return g
        g = re.sub(r'data-name="[^"]*"', 'data-name="%s"' % full[rid], g)
        return re.sub(r'aria-label="[^"]*"', 'aria-label="%s"' % full[rid], g)
    s = re.sub(r'<[^>]*\bdata-room="([^"]+)"[^>]*>', tag, s)
    p = os.path.join(PLAN, "svg", "plan-lux-%s.svg" % lang); io.open(p, "w", encoding="utf-8", newline="\n").write(s)
    return p


src = io.open(os.path.join(H, "round27_plan.py"), encoding="utf-8").read()
ns = {"__name__": "r27p", "__file__": os.path.join(H, "round27_plan.py")}
exec(compile(src[:src.index('build("he"); build("en")')], "round27_plan.py", "exec"), ns)
ns["FILM"] = None  # the French and Russian pages already carry the film v3b
L = ns["L"]
L["fr"] = dict(pid=8511, sfx="L07-fr", svg="plan-lux-fr.svg", closet=(LAB["fr"]["closet"], LAB["fr"]["closet"]),
    names={k: FULL["fr"].get(k, v if isinstance(v, str) else " ".join(v)) for k, v in LAB["fr"].items() if k != "_"},
    chip={"bed1": "Chambre A", "bed3": "Chambre B"},
    eyebrow="Plan de l’appartement", h2="Cinq pièces, un grand espace ouvert et un toit-terrasse",
    lead=("Séjour, salle à manger et cuisine avec un long îlot dans un seul espace ouvert sur le toit-terrasse et ses pergolas, et une aile nuit "
          "séparée avec la suite parentale. Choisissez une pièce pour la voir sur le plan et, pour les pièces photographiées, sa photo prise dans l’appartement."),
    seg="Affichage du plan", b2d="Plan", b3d="Rendu", stage="Le plan de l’appartement. Choisissez une pièce dans la liste ou sur le plan. Plus et moins pour zoomer.",
    svg_label="Mini-penthouse à Kochav HaTzafon, illustration d’après le plan de l’architecte",
    alt3d="L’appartement vu d’en haut, coupé à hauteur de taille, d’après le plan de l’architecte",
    badge="Illustration d’après le plan de l’architecte", hint="Choisissez une pièce sur le plan ou dans la liste · deux doigts ou un double tap pour zoomer",
    zoom=("Zoomer", "Dézoomer", "Revenir à la vue complète", "Zoom"), chips="Les pièces de l’appartement",
    photo_cap="Photo prise dans l’appartement", no_photo="La pièce est indiquée sur le plan. Les photos de l’appartement sont dans la galerie plus haut.",
    foot="Illustration d’après le plan de l’architecte, à titre indicatif et sans dimensions. Mobilier tel que dessiné sur le plan" + NB + "; les lits sont indicatifs.",
    wa_lab="Une question sur le plan" + NB + "? Écrivez à Meital",
    jump=[("film", "Le film"), ("plan", "Plan de l’appartement"), ("location", "Emplacement")], jump_lab="Accès rapide")
L["ru"] = dict(pid=8512, sfx="L07-ru", svg="plan-lux-ru.svg", closet=(LAB["ru"]["closet"], LAB["ru"]["closet"]),
    names={k: FULL["ru"].get(k, v if isinstance(v, str) else " ".join(v)) for k, v in LAB["ru"].items() if k != "_"},
    chip={"bed1": "Спальня A", "bed3": "Спальня B"},
    eyebrow="Планировка", h2="Пять комнат, одно открытое пространство и терраса на крыше",
    lead=("Гостиная, столовая и кухня с длинным островом в одном открытом пространстве с выходом на террасу на крыше с перголами, и отдельное "
          "спальное крыло с родительской сюитой. Выберите комнату, чтобы увидеть её на плане, а у сфотографированных комнат и фото из квартиры."),
    seg="Вид плана", b2d="План", b3d="Визуализация", stage="План квартиры. Выберите комнату в списке или на плане. Плюс и минус для масштаба.",
    svg_label="Мини-пентхаус в Кохав ха-Цафон, визуализация по плану архитектора",
    alt3d="Квартира сверху, разрез на уровне пояса, по плану архитектора",
    badge="Визуализация по плану архитектора", hint="Выберите комнату на плане или в списке · два пальца или двойное касание для увеличения",
    zoom=("Увеличить", "Уменьшить", "Вернуть полный вид", "Масштаб"), chips="Комнаты квартиры",
    photo_cap="Фото из квартиры", no_photo="Комната отмечена на плане. Фото из квартиры в галерее выше.",
    foot="Визуализация по плану архитектора, только для наглядности и без размеров. Мебель как на плане, кровати условные.",
    wa_lab="Вопрос о планировке? Напишите Мейталь",
    jump=[("film", "Фильм"), ("plan", "Планировка"), ("location", "Расположение")], jump_lab="Быстрые ссылки")
for lang in ("fr", "ru"):
    c = L[lang]; pid = c["pid"]
    print(lang, "drawing:", drawing(lang))
    o = json.load(io.open(os.path.join(H, "live76", "%s.json" % lang), encoding="utf-8")); assert o["id"] == pid
    pre = os.path.join(H, "live-27-preplan-%d.html" % pid)  # the live text before the plan, kept from the first run
    if not os.path.exists(pre): io.open(pre, "w", encoding="utf-8", newline="\n").write(o["content"].replace("\r\n", "\n"))
    ns["build"](lang)
    p = os.path.join(H, "after-27-%d.html" % pid); t = io.open(p, encoding="utf-8").read()
    a = "html body .nlx .np-svg[lang=en] text[data-for=terrace]{font-size:86px}"; assert t.count(a) == 1
    t = t.replace(a, a + PHONE_CSS[lang])
    assert len(re.findall(r"<h1\b", t)) == 1 and t.count('id="plan-L07-%s"' % lang) == 1
    for w in ("Living room", "Walk-in", "Roof terrace", "Bedroom", "Kitchen"):
        assert w not in t[t.find('id="plan-L07-%s"' % lang):t.find('id="photos-L07-%s"' % lang)], ("English left in the plan", w)
    io.open(os.path.join(H, "after-27p-%d.html" % pid), "w", encoding="utf-8", newline="\n").write(t)
    print(" ", lang, "plan section done,", len(t), "chars")
