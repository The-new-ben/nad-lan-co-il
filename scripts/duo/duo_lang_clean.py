# -*- coding: utf-8 -*-
"""DUO Tel Aviv language posts (en 5194, fr 5195, ru 5196, ar 5197): the same audit rules as duo_he_edit.py, as a cleaner.
  1. whole sections whose subject is the company's sales, contracts, unsold stock, partners' share or project finance go
     (heading and body, up to the next heading of the same or a higher level);
  2. list items, table rows and paragraphs that carry such numbers go; a sentence with research-memo or broker wording goes;
  3. the floors read as the developer, the architects and the contractor publish them (50 per tower);
  4. the sources paragraph is replaced by a short, respectful one with the invitation to the developer.
Dry by default (writes docs/research/2026-11-22-duo-audit/proposed/<id>.html); --go <lang> writes that live post
(md5 pin from raw/index.json, backup, read-back, restore on mismatch).   python scripts/duo/duo_lang_clean.py en [--go]"""
import hashlib, html, io, json, os, re, sys, time
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.dirname(os.path.dirname(HERE))
AUD = os.path.join(REPO, "docs", "research", "2026-11-22-duo-audit")
IDS = {"en": 5194, "fr": 5195, "ru": 5196, "ar": 5197}

R = {
    "en": {
        "sections": ["The 668 and 510 numbers answer different questions", "What to check about the seller and project finance",
                     "Why are there 668 apartments but sales reports cover 510?", "Who should pause before proceeding",
                     "A dated five-apartment transaction is context, not", "Ten image alt suggestions"],
        "hard": ["510", "372", "361", "366", "144", "149", "138", "contracts", "contracted", "not sold", "inventory", "stock", "74.26", "70%",
                 "partners", "Calcalist", "broker", "listing", "consideration", "remaining developer"],
        "soft": ["contradiction", "not found", "was not found", "verified", "reconcil", "54", "December 2026", "secondary", "cannot honestly",
                 "missing", "asking price", "should not be trusted", "no verified", "inconsistent", "live quarterly filing", "dated reporting measure", "room-by-room"],
        "repl": [("Two towers, 54 total floors and 50 residential floors", "Two towers of 50 floors"),
                 ("What is publicly verified about DUO Tel Aviv?", "What are the key facts about DUO Tel Aviv?"),
                 ("Why do some sources say 50 floors and others 54?", "How many floors does each DUO tower have?"),
                 ("A buyer's verified snapshot", "The project at a glance"),
                 ("Floors: 54 total floors in each tower, including 50 residential floors.", "Floors: 50 in each tower, according to the project website, Yashar Architects and Electra."),
                 ("82% financial or engineering completion", "82% completion"), ("76% financial completion", "76% completion")],
        "faq_answers": {"How many floors does each DUO tower have?": "Each of the two towers rises 50 floors, according to the project website, Yashar Architects and Electra.",
                        "What are the key facts about DUO Tel Aviv?": "DUO Tel Aviv is a residential and commercial project by Africa Israel Residences at Arlozorov and Ibn Gabirol: two 50-floor towers with 668 apartments, a commercial complex and underground parking. Completion is planned for 2027, according to the company."},
        "floor_head": "Two towers of 50 floors",
        "floor_line": "Each tower rises 50 floors, according to the project website, Yashar Architects and Electra.",
        "sources_head": "Sources",
        "sources": "Built from public sources: the project website www.duo-tlv.com (Hebrew and English); Africa Israel Residences' public filings on the TASE Maya system; the Tel Aviv-Yafo licensing authority; Yashar Architects (yashararch.com/projects/duo); Electra (electra.co.il); Globes and Ynet. Checked on 22 November 2026. This page is independent and does not speak for the developer; the binding materials are the developer's own website, sales office and sale contract. Africa Israel Residences is welcome to send us official materials, and we will update the page.",
    },
}


R["fr"] = {
    "sections": ["Pourquoi 668 ne veut pas dire", "Les visuels et la maquette ne sont pas un stock", "Suggestions de textes alternatifs",
                 "Les ventes officielles, avec leur date", "Ce que la structure du projet change", "Quand faut-il continuer à comparer",
                 "Des appartements sont-ils actuellement disponibles", "Quel était le prix moyen déclaré", "Pourquoi parle-t-on de 668 appartements",
                 "Que signifie le taux d'avancement"],
    "hard": ["510", "372", "366", "361", "144", "149", "138", "appartements vendus", "ont été vendus", "non vendus", "stock", "74,26", "74.26",
             "Calcalist", "courtier", "annonce", "partenaires", "54 étages", "54 niveaux", "contrats signés", "contrats cumul", "neuf contrats", "80,147"],
    "soft": ["contradiction", "écart", "n'a pas été trouvé", "introuvable", "54", "décembre 2026", "secondaire", "Les rapports financiers", "Ce pourcentage est une mesure"],
    "repl": [("Les tours comptent-elles 50 ou 54 étages ?", "Combien d'étages compte chaque tour ?"),
             ("Quelles informations sur DUO Tel Aviv sont vérifiées publiquement ?", "Quels sont les faits essentiels sur DUO Tel Aviv ?"),
             ("avancement financier ou technique", "avancement"), ("un avancement financier de 76 %", "un avancement de 76 %")],
    "faq_answers": {"Existe-t-il une liste de prix actuelle ?": "Aucune liste de prix n'a été publiée. Le prix d'un appartement précis s'obtient auprès du bureau de vente du promoteur.",
                    "Combien d'étages compte chaque tour ?": "Chacune des deux tours compte 50 étages, selon le site du projet, Yashar Architects et Electra.",
                    "Quels sont les faits essentiels sur DUO Tel Aviv ?": "DUO Tel Aviv est un projet résidentiel et commercial d'Africa Israel Résidences, au croisement d'Arlozorov et d'Ibn Gabirol : deux tours de 50 étages, 668 appartements, un ensemble commercial et un parking souterrain. L'achèvement est prévu en 2027, selon la société."},
    "sources_head": "Sources",
    "sources": "Page établie à partir de sources publiques : le site du projet www.duo-tlv.com (hébreu et anglais) ; les publications d'Africa Israel Résidences sur le système Maya de la Bourse de Tel-Aviv ; l'autorité des permis de Tel Aviv-Yafo ; Yashar Architects (yashararch.com/projects/duo) ; Electra (electra.co.il) ; Globes et Ynet. Vérifié le 22 novembre 2026. Cette page est indépendante et ne parle pas au nom du promoteur ; les documents qui engagent sont ceux du promoteur : son site, son bureau de vente et le contrat de vente. Africa Israel Résidences est invitée à nous transmettre ses documents officiels, et nous mettrons la page à jour.",
}
R["ru"] = {
    "sections": ["Почему 668 и 510", "Варианты alt-текста", "Продажи 2025 года", "Сделка на пять квартир",
                 "Отчетность на конец 2025 года", "Как оценивать опыт девелопера", "Документы, которые раскрывают", "Кому стоит продолжить сравнение",
                 "Есть ли сейчас квартиры в продаже", "Почему в проекте 668 квартир", "Что означает показатель готовности"],
    "sections_exact": ["Первый квартал 2026 года"],
    "hard": ["510", "372", "366", "361", "144", "149", "138", "подписанных договоров", "заключено", "продано", "продан", "непродан", "74,26", "74.26",
             "Calcalist", "Калькалист", "брокер", "объявлени", "партнер", "54 этаж", "девять договоров", "80,147"],
    "soft": ["противореч", "расхожд", "не найден", "54", "декабр", "вторичн", "раскрывает кварт"],
    "repl": [("Какие факты о DUO Tel Aviv подтверждены публично?", "Главное о DUO Tel Aviv"), ("82% финансовой или инженерной готовности", "82% готовности")],
    "faq_answers": {"Сколько этажей в каждой башне?": "В каждой из двух башен 50 этажей, по данным сайта проекта, Yashar Architects и Electra.",
                    "Главное о DUO Tel Aviv": "DUO Tel Aviv: жилой и коммерческий проект Africa Israel Residences на пересечении улиц Арлозоров и Ибн Гвироль. Две башни по 50 этажей, 668 квартир, торговый комплекс и подземный паркинг. Завершение запланировано на 2027 год, по данным компании."},
    "sources_head": "Источники",
    "sources": "Страница составлена по открытым источникам: сайт проекта www.duo-tlv.com (на иврите и английском); публичные отчеты Africa Israel Residences в системе Maya Тель-Авивской биржи; отдел лицензирования Тель-Авива-Яффо; Yashar Architects (yashararch.com/projects/duo); Electra (electra.co.il); Globes и Ynet. Проверено 22 ноября 2026 года. Страница независима и не говорит от имени девелопера; обязывающие материалы: сайт девелопера, его отдел продаж и договор купли-продажи. Africa Israel Residences может прислать нам официальные материалы, и мы обновим страницу.",
}
R["ar"] = {
    "sections": ["لماذا يظهر الرقمان 668 و510", "النموذج التفاعلي ليس قائمة مبيعات", "عشرة اقتراحات لنصوص الصور", "صفقة أبريل 2026",
                 "ما الذي يفحص عن البائع وتمويل المشروع", "متى يجب التوقف", "هل توجد شقق متاحة للبيع حاليا", "لماذا يوجد 668 شقة"],
    "hard": ["510", "372", "366", "361", "144", "149", "138", "مخزون", "لم تبع", "غير المباعة", "بيعت", "74.26", "74,26", "كالكاليست", "Calcalist",
             "وسيط", "إعلان", "الشركاء", "54 طابقا", "عقدا", "عقود", "80.147", "1,281", "المدير التنفيذي"],
    "soft": ["تناقض", "لم يعثر", "لم نجد", "54", "ديسمبر 2026", "ثانوي"],
    "repl": [("54 طابقا بالمجموع و50 طابقا سكنيا", "برجان من 50 طابقا"),
             ("لماذا تقول بعض الصفحات 50 طابقا وأخرى 54؟", "كم عدد الطوابق في كل برج؟"),
             ("ما المعلومات المثبتة علنا عن DUO Tel Aviv؟", "ما أهم المعلومات عن DUO Tel Aviv؟"),
             ("إنجاز مالي أو هندسي", "إنجاز"), ("إنجازا ماليا أو هندسيا", "إنجازا"), ("إنجازا ماليا", "إنجازا")],
    "faq_answers": {"كم عدد الطوابق في كل برج؟": "يرتفع كل من البرجين 50 طابقا، بحسب موقع المشروع وYashar Architects وElectra.",
                    "ما أهم المعلومات عن DUO Tel Aviv؟": "DUO Tel Aviv مشروع سكني وتجاري لشركة Africa Israel Residences عند تقاطع شارعي أرلوزوروف وابن جبيرول: برجان من 50 طابقا، و668 شقة، ومجمع تجاري وموقف سيارات تحت الأرض. ومن المخطط إنجازه في 2027 بحسب الشركة."},
    "floor_head": "برجان من 50 طابقا",
    "floor_line": "يرتفع كل برج 50 طابقا، بحسب موقع المشروع وYashar Architects وElectra.",
    "sources_head": "المصادر",
    "sources": "أعدت هذه الصفحة من مصادر علنية: موقع المشروع www.duo-tlv.com (بالعبرية والإنجليزية)؛ إفصاحات Africa Israel Residences العلنية في نظام مايا لبورصة تل أبيب؛ سلطة الترخيص في بلدية تل أبيب-يافا؛ Yashar Architects (yashararch.com/projects/duo)؛ Electra (electra.co.il)؛ Globes وYnet. تم التحقق في 22 تشرين الثاني 2026. هذه الصفحة مستقلة ولا تتحدث باسم المطور؛ المواد الملزمة هي موقع المطور ومكتب مبيعاته وعقد البيع. نرحب بأن ترسل لنا شركة Africa Israel Residences موادها الرسمية، وسنحدث الصفحة وفقا لها.",
}


def sec_remove(t, head):
    m = re.search(r'<h([23])[^>]*>\s*' + re.escape(head) + r'[^<]*</h\1>', t)
    if not m:
        return t, False
    lvl = m.group(1)
    stop = r'<h2\b' if lvl == '2' else r'<h[23]\b'
    n = re.search(stop, t[m.end():])
    e = m.end() + (n.start() if n else len(t) - m.end())
    return t[:m.start()] + t[e:], True


def text(s):
    return html.unescape(re.sub(r'<[^>]+>', ' ', s))


def clean(t, cfg):
    log = {"sections": [], "elements": [], "sentences": []}
    for h in cfg["sections"]:
        t, ok = sec_remove(t, h)
        if ok:
            log["sections"].append(h)
    for h in cfg.get("sections_exact", []):
        m = re.search(r'<h3[^>]*>\s*' + re.escape(h) + r'\s*</h3>', t)
        if m:
            n = re.search(r'<h[23]', t[m.end():])
            t = t[:m.start()] + t[m.end() + (n.start() if n else 0):]
            log["sections"].append(h)
    for a, b in cfg["repl"]:
        t = t.replace(a, b)
    # FAQ answers that are rewritten whole (the question stays)
    for q, a in cfg.get("faq_answers", {}).items():
        m = re.search(r'(<h3[^>]*>\s*' + re.escape(q) + r'[^<]*</h3>)(.*?)(?=<h[23]\b)', t, re.S)
        if m:
            t = t[:m.start()] + m.group(1) + '\n<p>' + a + '</p>\n' + t[m.end():]

    def drop_el(m):
        if any(k in text(m.group(0)) for k in cfg["hard"]):
            log["elements"].append(text(m.group(0))[:120])
            return ''
        return m.group(0)
    for tag in ('li', 'tr', 'p'):
        t = re.sub(r'<%s\b[^>]*>.*?</%s>' % (tag, tag), drop_el, t, flags=re.S)

    def drop_sent(m):
        inner = m.group(2)
        if '<' in re.sub(r'</?(?:strong|em|b|i|a)\b[^>]*>', '', inner):
            return m.group(0)
        parts = re.split(r'(?<=[.!?])\s+(?=\S)', inner)
        keep = []
        for s in parts:
            if any(k in text(s) for k in cfg["soft"]):
                log["sentences"].append(text(s)[:120])
            else:
                keep.append(s)
        if not keep:
            return ''
        return m.group(1) + ' '.join(keep) + m.group(3)
    t = re.sub(r'(<p\b[^>]*>)(.*?)(</p>)', drop_sent, t, flags=re.S)
    # lists and tables left empty, and the floors line under a heading left with no paragraph
    for _ in range(2):
        t = re.sub(r'<ul\b[^>]*>\s*</ul>', '', t)
        t = re.sub(r'<ol\b[^>]*>\s*</ol>', '', t)
        t = re.sub(r'<tbody\b[^>]*>\s*</tbody>', '', t)
        t = re.sub(r'<table\b[^>]*>\s*(?:<thead\b.*?</thead>)?\s*</table>', '', t, flags=re.S)
    if cfg.get("floor_head"):
        t = re.sub(r'(<h3[^>]*>\s*' + re.escape(cfg["floor_head"]) + r'\s*</h3>)\s*(?=<h[23]\b)', lambda m: m.group(1) + '\n<p>' + cfg["floor_line"] + '</p>\n', t)
    # the sources section: one respectful paragraph
    m = re.search(r'(<h2[^>]*>\s*' + re.escape(cfg["sources_head"]) + r'\s*</h2>)(.*?)(?=<h2\b|$)', t, re.S)
    if m:
        t = t[:m.start()] + m.group(1) + '\n<p>' + cfg["sources"] + '</p>\n' + t[m.end():]
    # an h2/h3 left with nothing under it before the next heading goes too
    t = re.sub(r'<h3[^>]*>[^<]*</h3>\s*(?=<h[23]\b)', '', t)
    return t, log


if __name__ == "__main__":
    lang = sys.argv[1]; GO = "--go" in sys.argv
    pid = IDS[lang]; cfg = R[lang]
    idx = json.load(open(os.path.join(AUD, "raw", "index.json"), encoding="utf-8"))
    src = open(os.path.join(REPO, "scripts", "skin-a", "deployskin.py"), encoding="utf-8").read(); ns = {"__name__": "duolang"}
    exec(compile(src[:src.index('s, h, _ = req("GET", "/wp-json/nadlan/v1/health")')], "h", "exec"), ns); req = ns["req"]
    s, g, _ = req("GET", "/wp-json/wp/v2/nadlan_project/%d?context=edit&_fields=id,slug,modified,content" % pid)
    assert s == 200, s
    raw = g["content"]["raw"]
    now = hashlib.md5(raw.encode("utf-8")).hexdigest()
    if now != idx[str(pid)]["md5"]:
        raise SystemExit("the live %s post changed since the audit read it (%s)" % (lang, now[:10]))
    new, log = clean(raw.replace('\r\n', '\n'), cfg)
    os.makedirs(os.path.join(AUD, "proposed"), exist_ok=True)
    open(os.path.join(AUD, "proposed", "%d.html" % pid), "w", encoding="utf-8", newline="").write(new)
    json.dump(log, open(os.path.join(AUD, "proposed", "%d-dropped.json" % pid), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print("[plan] %s post %d: %d -> %d chars; %d sections, %d elements, %d sentences dropped" % (lang, pid, len(raw), len(new), len(log["sections"]), len(log["elements"]), len(log["sentences"])))
    if not GO:
        sys.exit(0)
    bk = os.path.join(AUD, "backup"); os.makedirs(bk, exist_ok=True)
    stamp = time.strftime("%Y%m%dT%H%M%S")
    io.open(os.path.join(bk, "backup-%d-%s.html" % (pid, stamp)), "w", encoding="utf-8", newline="").write(raw)
    s1, r1, _ = req("POST", "/wp-json/wp/v2/nadlan_project/%d" % pid, {"content": new})
    assert s1 in (200, 201), (s1, str(r1)[:300])
    s, r, _ = req("GET", "/wp-json/wp/v2/nadlan_project/%d?context=edit&_fields=content,modified" % pid)
    ok = r["content"]["raw"] == new
    json.dump({"stamp": stamp, "post": pid, "before_md5": now, "after_md5": hashlib.md5(r["content"]["raw"].encode("utf-8")).hexdigest(), "read_back_equal": ok},
              open(os.path.join(bk, "result-%d-%s.json" % (pid, stamp)), "w", encoding="utf-8"), indent=1)
    if not ok:
        sb, _, _ = req("POST", "/wp-json/wp/v2/nadlan_project/%d" % pid, {"content": raw})
        raise SystemExit("read-back differs: restored the backup (http %s)" % sb)
    print("[done] %s post %d written and read back equal" % (lang, pid))
