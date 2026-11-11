# -*- coding: utf-8 -*-
"""HAD-712, the Kikar language pages (11.11.2026): one release per language, built by make_deploy<N>.py through build(prev, new, lang).
Each release does two things for ONE language page, on top of the article edit made before it by scripts/kikar/had712_lang.py:
  1. a hunk on the LIVE inc/project-stage.php: the Kikar price calculator of that language gains the financing block that the Hebrew
     calculator gained in 1.72.648 (k648_hunks.py): minimum equity with the purchase tax, the largest mortgage (75% / 50%), the first
     monthly repayment and the net income it needs. The data (window.NLPG_MM) and the script lines are already printed with every price
     guide since 1.72.648; the script fills the block wherever the markup has it. The default numbers are the Hebrew block's
     (the same default price), written in the page's number format; the script recomputes them on load and on every change.
  2. the language page's FAQPage meta (_nl_faq_schema, inc/schema-meta.php) follows the article's visible FAQ, which gained five
     questions: built by hamedina_page_data.faq_json() over the live post text. The method is proven first: faq_json() over the post's
     text BEFORE the article edit (the backup) must equal the FAQ JSON the live page prints today, byte for byte (as 1.72.642 did).
No asset file, no module-list change. The release runner is deploy<prev>.py transformed, as every Kikar release since 1.72.631."""
import base64, glob, hashlib, json, os, re, subprocess, sys, urllib.request
H = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.dirname(os.path.dirname(H))
PLUG = os.path.join(REPO, "plugins", "nadlan-config")
QA = os.path.join(REPO, "docs", "qa", "project-stage-2026-09-24")
md5 = lambda b: hashlib.md5(b).hexdigest()
REL = "inc/project-stage.php"
PIDS = {"en": 8114, "fr": 8116, "ru": 8117, "ar": 8118}
WHY = '</dl><p class="nlpg__why" data-pg="why">'


def fin_en():
    return ('<div class="nlpg__fin" data-pg="fin"><p class="nlpg__finh">Financing under the Bank of Israel rules</p><dl class="nlpg__rows">'
            '<div><dt>Minimum equity, including purchase tax</dt><dd data-pg="eq">about ₪<span class="nlds-num">2.72</span> million</dd></div>'
            '<div><dt>Largest mortgage, <span class="nlds-num"><span data-pg="lp">75</span>%</span> of the price</dt><dd data-pg="ln">about ₪<span class="nlds-num">6.83</span> million</dd></div>'
            '<div><dt>First monthly repayment</dt><dd data-pg="mo">about ₪<span class="nlds-num">37,000</span></dd></div>'
            '<div class="nlpg__inc"><dt>Net income needed</dt><dd><span data-pg="inc">about ₪<span class="nlds-num">93,000</span></span> <small>a month</small></dd></div></dl>'
            '<p class="nlpg__fina">A <span class="nlds-num">25</span>-year mortgage at the banking system’s average track mix and rates, <span class="nlds-num" data-pg="fm">9.2026</span> (Bank of Israel). '
            'The income needed assumes a repayment of <span class="nlds-num">40%</span> of disposable income; the limit is <span class="nlds-num">50%</span>. This is the first repayment, before changes in interest and the index.</p></div>')


def fin_fr():  # the French calculator writes thousands with U+202F (fr-FR), as its own rows do; "75 %" with U+202F
    N = " "
    return ('<div class="nlpg__fin" data-pg="fin"><p class="nlpg__finh">Financement, selon les règles de la Banque d’Israël</p><dl class="nlpg__rows">'
            '<div><dt>Apport minimal, taxe d’acquisition comprise</dt><dd data-pg="eq">environ <span class="nlds-num">2,72</span> M₪</dd></div>'
            '<div><dt>Prêt maximal, <span class="nlds-num"><span data-pg="lp">75</span>' + N + '%</span> du prix</dt><dd data-pg="ln">environ <span class="nlds-num">6,83</span> M₪</dd></div>'
            '<div><dt>Première mensualité</dt><dd data-pg="mo">environ <span class="nlds-num">37' + N + '000</span> ₪</dd></div>'
            '<div class="nlpg__inc"><dt>Revenu net nécessaire</dt><dd><span data-pg="inc">environ <span class="nlds-num">93' + N + '000</span> ₪</span> <small>par mois</small></dd></div></dl>'
            '<p class="nlpg__fina">Prêt immobilier sur <span class="nlds-num">25</span> ans, à la répartition et aux taux moyens du système bancaire, <span class="nlds-num" data-pg="fm">9.2026</span> (Banque d’Israël). '
            'Le revenu nécessaire correspond à une mensualité de <span class="nlds-num">40' + N + '%</span> du revenu disponible\xa0; la limite est de <span class="nlds-num">50' + N + '%</span>. '
            'C’est la première mensualité, avant les variations de taux et d’indexation.</p></div>')


def fin_ru():  # thousands and "млн ₪" with a no-break space, as the Russian calculator's own rows
    N = "\xa0"
    return ('<div class="nlpg__fin" data-pg="fin"><p class="nlpg__finh">Финансирование по правилам Банка Израиля</p><dl class="nlpg__rows">'
            '<div><dt>Минимальные собственные средства, включая налог на покупку</dt><dd data-pg="eq">около <span class="nlds-num">2,72</span> млн' + N + '₪</dd></div>'
            '<div><dt>Максимальная ипотека, <span class="nlds-num"><span data-pg="lp">75</span>%</span> от цены</dt><dd data-pg="ln">около <span class="nlds-num">6,83</span> млн' + N + '₪</dd></div>'
            '<div><dt>Первый ежемесячный платёж</dt><dd data-pg="mo">около <span class="nlds-num">37' + N + '000</span> ₪</dd></div>'
            '<div class="nlpg__inc"><dt>Необходимый чистый доход</dt><dd><span data-pg="inc">около <span class="nlds-num">93' + N + '000</span> ₪</span> <small>в месяц</small></dd></div></dl>'
            '<p class="nlpg__fina">Ипотека на <span class="nlds-num">25</span> лет при средних по банковской системе структуре и ставках, <span class="nlds-num" data-pg="fm">9.2026</span> (Банк Израиля). '
            'Необходимый доход рассчитан из платежа в <span class="nlds-num">40%</span> от располагаемого дохода; предел — <span class="nlds-num">50%</span>. Это первый платёж, до изменений ставки и индекса.</p></div>')


def fin_ar():  # Western digits with a comma, as the Arabic calculator's own rows
    return ('<div class="nlpg__fin" data-pg="fin"><p class="nlpg__finh">التمويل وفق قواعد بنك إسرائيل</p><dl class="nlpg__rows">'
            '<div><dt>الحد الأدنى من رأس المال الذاتي، شاملاً ضريبة الشراء</dt><dd data-pg="eq">نحو <span class="nlds-num">2.72</span> مليون ₪</dd></div>'
            '<div><dt>أقصى قرض سكني، <span class="nlds-num"><span data-pg="lp">75</span>%</span> من السعر</dt><dd data-pg="ln">نحو <span class="nlds-num">6.83</span> مليون ₪</dd></div>'
            '<div><dt>القسط الشهري الأول</dt><dd data-pg="mo">نحو <span class="nlds-num">37,000</span> ₪</dd></div>'
            '<div class="nlpg__inc"><dt>صافي الدخل المطلوب</dt><dd><span data-pg="inc">نحو <span class="nlds-num">93,000</span> ₪</span> <small>شهرياً</small></dd></div></dl>'
            '<p class="nlpg__fina">قرض سكني لمدة <span class="nlds-num">25</span> سنة بالتركيبة والفوائد المتوسطة في الجهاز المصرفي، <span class="nlds-num" data-pg="fm">9.2026</span> (بنك إسرائيل). '
            'الدخل المطلوب محسوب على أساس قسط يعادل <span class="nlds-num">40%</span> من الدخل المتاح؛ والحد الأقصى <span class="nlds-num">50%</span>. هذا هو القسط الأول، قبل تغيّرات الفائدة والمؤشر.</p></div>')


FIN = {"en": fin_en, "fr": fin_fr, "ru": fin_ru, "ar": fin_ar}
# the default "total with tax" row of each language's Kikar calculator, the anchor the block goes after
TT = {"en": '<dd data-pg="tt">about ₪<span class="nlds-num">9.54</span> million</dd></div>',
      "fr": '<dd data-pg="tt">environ <span class="nlds-num">9,54</span> M₪</dd></div>',
      "ru": '<dd data-pg="tt">около <span class="nlds-num">9,54</span> млн\xa0₪</dd></div>',
      "ar": '<dd data-pg="tt">نحو <span class="nlds-num">9.54</span> مليون ₪</dd></div>'}
# what the release's check row requires on the language page (the block, its data, and the new FAQ questions in the schema)
NEED = {"en": ['data-pg="fin"', 'Net income needed', 'window.NLPG_MM={"pm":', 'class="nlws-fig"', 'Waxman Govrin Geva (WXG)',
               '"name":"How many floors do Kikar Hamedina Towers have?"', '"name":"Who is the architect of Kikar Hamedina Towers?"'],
        "fr": ['data-pg="fin"', 'Revenu net nécessaire', 'window.NLPG_MM={"pm":', 'class="nlws-fig"', 'Waxman Govrin Geva (WXG)',
               '"name":"Combien d’étages comptent les tours Kikar Hamedina\xa0?"', '"name":"Qui est l’architecte des tours Kikar Hamedina\xa0?"'],
        "ru": ['data-pg="fin"', 'Необходимый чистый доход', 'window.NLPG_MM={"pm":', 'class="nlws-fig"', 'Waxman Govrin Geva (WXG)',
               '"name":"Сколько этажей в башнях Кикар ха-Медина?"', '"name":"Кто архитектор башен Кикар ха-Медина?"'],
        "ar": ['data-pg="fin"', 'صافي الدخل المطلوب', 'window.NLPG_MM={"pm":', 'class="nlws-fig"', 'Waxman Govrin Geva (WXG)',
               '"name":"كم طابقاً في أبراج كيكار همدينا؟"', '"name":"من المهندس المعماري لأبراج كيكار همدينا؟"']}


def hunks(lang):
    a = TT[lang] + WHY
    return [(a, TT[lang] + "</dl>" + FIN[lang]() + '<p class="nlpg__why" data-pg="why">')]


def faq_meta(lang, KD, req, added=5):
    """before = the live meta (proven equal to faq_json over the pre-edit text), after = faq_json over the live post text"""
    pid = PIDS[lang]
    res = sorted(glob.glob(os.path.join(REPO, "docs", "qa", "had-712", "result-%s-*.json" % lang)))
    assert res, "run scripts/kikar/had712_lang.py %s --go first" % lang
    R = json.load(open(res[-1], encoding="utf-8"))
    stamp, r = R["stamp"], R["result"]
    assert r["post"] == pid and r["read_back_equal"], r
    old = open(os.path.join(REPO, "docs", "qa", "had-712", "backup-%d-%s.html" % (pid, stamp)), encoding="utf-8").read()
    s, g, _ = req("GET", "/wp-json/wp/v2/nadlan_project/%d?context=edit&_fields=content" % pid)
    new = g["content"]["raw"]
    assert md5(new.encode("utf-8")) == r["after_md5"], lang + ": the live post is not the one had712_lang.py wrote"
    page = urllib.request.urlopen(urllib.request.Request("https://nad-lan.co.il/projects/%s/?mkl=%d" % (KD.POSTS[lang]["slug"], pid), headers={"User-Agent": "Mozilla/5.0"}), timeout=60).read().decode("utf-8")
    live = [j for j in re.findall(r'<script type="application/ld\+json">(.*?)</script>', page, re.S) if '"FAQPage"' in j and '"inLanguage":"%s"' % lang in j]
    assert len(live) == 1, (lang, len(live))
    KD.content = (lambda t: (lambda l: re.sub(r">\s*\n\s*<", "><", t.strip())))(old)
    assert KD.faq_json(lang) == live[0], lang + ": faq_json() over the pre-edit text is not the live FAQ meta; the method is not proven"
    before = base64.b64encode(live[0].encode("utf-8")).decode("ascii")
    KD.content = (lambda t: (lambda l: re.sub(r">\s*\n\s*<", "><", t.strip())))(new)
    j = KD.faq_json(lang)
    n = len(json.loads(j)["mainEntity"])
    assert j != live[0] and n == len(json.loads(live[0])["mainEntity"]) + added and n <= 20, (lang, n)
    after = base64.b64encode(j.encode("utf-8")).decode("ascii")
    # word for word: every question and answer of the schema is visible in the post text
    vis = re.sub(r"<[^>]+>", "", new)
    for q in json.loads(j)["mainEntity"]:
        assert q["name"] in vis and q["acceptedAnswer"]["text"] in vis, (lang, q["name"])
    print("[faq] %s %d: proven on the live meta; new FAQ JSON %d questions, each visible word for word" % (lang, pid, n))
    return {"id": pid, "before": before, "before_md5": md5(before.encode("ascii")), "after": after, "n": n}


YOAST_BLOCK = (
    "        for _ym in YOAST_META:  # @@N@@: a Yoast meta the owner approved, guarded by the md5 of the text it replaces\n"
    "            for _pk in _ym.get(\"peek\", []):  # read only: the share titles, reported, never written here\n"
    "                print(f\"[yoast] {_ym['id']} {_pk}: md5 {ops({'pmeta': {'id': _ym['id'], 'key': _pk, 'get': 1}}, 'yoast peek')['pmeta']['md5']} (empty = d41d8cd98f)\")\n"
    "            _g = ops({\"pmeta\": {\"id\": _ym[\"id\"], \"key\": _ym[\"key\"], \"get\": 1}}, \"yoast get %d\" % _ym[\"id\"])[\"pmeta\"]\n"
    "            if _g[\"md5\"] != _ym[\"before_md5\"]:\n"
    "                raise SystemExit(f\"FATAL yoast {_ym['id']} {_ym['key']}: live {_g['md5'][:10]} is not the expected {_ym['before_md5'][:10]}; nothing written\")\n"
    "            UNDO.append((\"meta\", {\"id\": _ym[\"id\"], \"key\": _ym[\"key\"], \"before\": _ym[\"before\"].encode(\"utf-8\"), \"before_md5\": _ym[\"before_md5\"]}))\n"
    "            _w = ops({\"pmeta\": {\"id\": _ym[\"id\"], \"key\": _ym[\"key\"], \"expect\": _ym[\"before_md5\"], \"b64\": base64.b64encode(_ym[\"after\"].encode(\"utf-8\")).decode(), \"md5\": md5(_ym[\"after\"].encode(\"utf-8\"))}}, \"yoast %d\" % _ym[\"id\"])[\"pmeta\"]\n"
    "            if _w[\"md5\"] != md5(_ym[\"after\"].encode(\"utf-8\")):\n"
    "                raise SystemExit(f\"FATAL yoast {_ym['id']}: read back {_w['md5'][:10]}\")\n"
    "            print(f\"[yoast] {_ym['id']} {_ym['key']}: written and read back\")\n")


def build_meta_only(PREV, NEWV, lang, LIVE_MD5, yoast=None, msg=None):
    """a release that writes only post metas (a language page's FAQ meta, and/or an owner-approved Yoast meta): no file, no hunk
    (RELS empty), the version bump only. yoast = {"id", "key", "before", "after", "peek": [...], "path"}"""
    label = lang or "Hebrew page title"
    P, N, PP = str(PREV), str(NEWV), str(PREV - 1)
    src = open(os.path.join(H, "deploy%d.py" % PREV), encoding="utf-8").read()
    _m = re.search(r"^    import (\w+) as PX  # noqa: E402 \(.*$", src, re.M)  # the previous release may come from another session (myplan_653)
    assert _m, "no PX import in deploy%d.py" % PREV
    PXN = _m.group(1)
    _ns = {}
    exec(compile(open(os.path.join(H, PXN + ".py"), encoding="utf-8").read(), PXN, "exec"), _ns)
    LIST = _ns.get("MAIN_NEW") or _ns["MAIN_LIST"]
    BUY = _ns["BUY"]
    assert "'designer'" in LIST and BUY == "'drone-map', 'buying-hub', 'i18n', ", (LIST[-80:], BUY)
    MOD = ('# -*- coding: utf-8 -*-\n"""Release 1.72.%d (HAD-712, the Kikar %s page: the FAQ meta follows a rewording of the article): NO file, NO hunk '
           '(inc/project-stage.php stays the 1.72.%d text, md5 %s), NO module-list hunk. Generated by make_deploy%d.py (kl_release.py)."""\n'
           "RELS = []\nLIVE_MD5 = {}\nPROOF = {}\nHUNKS = []\nMAIN_LIST = %r\nMAIN_NEW = MAIN_LIST\nBUY = %r\n\n\n"
           "def apply(rel, txt):\n    raise SystemExit('kikar_%d: no hunk in this release (' + rel + ')')\n\n\n"
           "def apply_main(txt):\n"
           "    if txt.count(MAIN_LIST) != 1 or \"'designer'\" not in MAIN_LIST:\n"
           "        raise SystemExit('kikar_%d: FATAL: the live module list tail is not the one the previous release left')\n"
           "    if txt.count(BUY) != 1 or txt.count(\"'buying-hub'\") != 1:\n"
           "        raise SystemExit('kikar_%d: FATAL: buying-hub is not once before i18n in the live nadlan-config.php; read it before releasing')\n"
           "    print(\"[hunk] nadlan-config.php: no module change (proven); the FAQ meta only\")\n"
           "    return txt\n") % (NEWV, label, PREV, LIVE_MD5[:10], NEWV, LIST, BUY, NEWV, NEWV, NEWV)
    open(os.path.join(H, "kikar_%d.py" % NEWV), "w", encoding="utf-8", newline="\n").write(MOD)
    assert src.count('WANT_LIVE = "1.72.%s"' % PP) == 1
    src = src.replace('WANT_LIVE = "1.72.%s"' % PP, 'WANT_LIVE = "@@WANT@@"')
    for a, b in [("1.72." + P, "1.72." + N), ("ps" + P, "ps" + N), ("bak" + P, "bak" + N), ("make_deploy" + P, "make_deploy" + N),
                 ("deploy-result-" + P, "deploy-result-" + N), ("speed-" + P, "speed-" + N), ("posts-before-" + P, "posts-before-" + N),
                 ("deploy-result-" + PP, "deploy-result-" + P)]:
        src = src.replace(a, b)
    src = src.replace('WANT_LIVE = "@@WANT@@"', 'WANT_LIVE = "1.72.%s"' % P)
    BS = chr(92)
    src = re.sub(r"\?t" + P + r"([a-z]*)=1", "?t" + N + BS + "1=1", src)
    src = re.sub(r"&t" + P + r"([a-z]*)=1", "&t" + N + BS + "1=1", src)
    src, n = re.subn(r"for n in range\(\d+, 329, -1\)", "for n in range(%s, 329, -1)" % P, src); assert n == 1, n
    # the designer's tour page (/tour/designer/) is a static file stamped with the version it was built for (1.72.653): its rows
    # must not follow the version rename (the first run of 1.72.654 failed on them); they ask for "<module>.js?v=" without a number
    src = "\n".join(re.sub(r"(\.js\?v=)1\.72\.\d+", r"\1", l) if "/tour/designer/" in l else l for l in src.split("\n"))
    src, n = re.subn(r"^    import %s as PX  # noqa: E402 \(.*$" % PXN, "    import kikar_%s as PX  # noqa: E402 (1.72.%s: no hunk; post metas only: %s)" % (N, N, label), src, flags=re.M); assert n == 1, n
    assert src.count("        for _fm in FAQ_META:") == 1 and src.count("'_nl_faq_schema' === $key && in_array( $pid, array( 8114, 8116, 8117, 8118 ), true )") == 1, "the FAQ meta path is not in deploy%s.py" % P
    src, n = re.subn(r'print\("RELEASE 1\.72\.%s LIVE: [^"]*"\)' % N, 'print("RELEASE 1.72.%s LIVE: %s")' % (N, msg or ("the Kikar %s page FAQ schema follows the reworded article" % lang)), src); assert n == 1, n
    _src = open(os.path.join(REPO, "scripts", "skin-a", "deployskin.py"), encoding="utf-8").read(); _rq = {"__name__": "mkl"}
    exec(compile(_src[:_src.index('s, h, _ = req("GET", "/wp-json/nadlan/v1/health")')], "h", "exec"), _rq)
    sys.path.insert(0, H)
    import hamedina_page_data as KD  # noqa: E402
    FM = [faq_meta(lang, KD, _rq["req"], 0)] if lang else []
    YM = []
    if yoast:
        y = dict(yoast)
        y["before_md5"] = md5(y["before"].encode("utf-8"))
        YM = [y]
        # the rows that ask for the old title now ask for the new one (a release that left them would roll itself back)
        old_t, new_t = y["before"] + "</title>", y["after"] + "</title>"
        assert src.count(old_t) >= 1, "no check row names the old title"
        src = src.replace(old_t, new_t)
        assert y["before"] not in src.split("CHECKS = [", 1)[1], "another check row still names the old title"
        _anchor = "            print(f\"[faq] {_fm['id']}: _nl_faq_schema written and read back ({_fm['n']} questions)\")\n"
        assert src.count(_anchor) == 1, "the FAQ loop is not where it should be"
        src = src.replace(_anchor, _anchor + YOAST_BLOCK.replace("@@N@@", "1.72." + N), 1)
        assert src.count("\nUNDO = []") == 1
        src = src.replace("\nUNDO = []", "\nYOAST_META = " + repr(YM) + "  # 1.72.%s\nUNDO = []" % N, 1)
    lines = src.split("\n")
    seen = set()
    for k, l in enumerate(lines):
        if l.startswith("PIN = {"):
            lines[k] = "PIN = {}  # 1.72.%s: no swapped file" % N; seen.add("PIN")
        elif l.startswith("NEWFILES = "):
            lines[k] = "NEWFILES = set()  # 1.72.%s: no new file" % N; seen.add("NEWFILES")
        elif l.startswith("FILES = ["):
            lines[k] = "FILES = []  # 1.72.%s: no file" % N; seen.add("FILES")
        elif l.startswith("PHP_RELS = ["):
            lines[k] = "PHP_RELS = []  # 1.72.%s: no hunked file (inc/project-stage.php stays the 1.72.%s text)" % (N, P); seen.add("PHP_RELS")
        elif l.startswith("FAQ_META = "):
            lines[k] = "FAQ_META = " + repr(FM) + "  # 1.72.%s: before = the live meta (proven), after = the %s FAQ as reworded" % (N, lang); seen.add("FAQ_META")
    assert seen == {"PIN", "NEWFILES", "FILES", "PHP_RELS", "FAQ_META"}, seen
    src = "\n".join(lines)
    ROWS = ""
    if lang:
        ROWS += "    ('/projects/hamedina-%s/?t%sm=1', %r, ['Fatal error', 'Warning</b>'], []),\n" % (lang, N, NEED_META[lang])
    if YM:
        ROWS += "    (%r, %r, ['Fatal error', 'Warning</b>'], %r),\n" % (YM[0]["path"] + "?t%sy=1" % N, ["<title>" + YM[0]["after"] + "</title>"], ["<title>" + YM[0]["before"] + "</title>"])
    src = src.replace("CHECKS = [\n", "CHECKS = [\n" + ROWS, 1)
    assert src.count('if new != "1.72.%s":' % N) == 1 and src.count('BAK = ".bak%s"' % N) == 1
    open(os.path.join(H, "deploy%s.py" % N), "w", encoding="utf-8", newline="\n").write(src)
    print("deploy%s.py + kikar_%s.py written | no file, no hunk | FAQ meta %s | Yoast %s | %d new check row(s)" % (
        N, N, [(f["id"], f["n"]) for f in FM], [(y["id"], y["key"]) for y in YM], ROWS.count("\n")))


# what a meta-only release requires on the page: the reworded answers inside the schema
NEED_META = {"ru": ['"name":"Какой адрес у башен Кикар ха-Медина?"', 'адреса в разрешениях на строительство: He Be’Iyar 25, 45 и 65',
                    'составит примерно от 4\xa0000 до 5\xa0000\xa0₪ в месяц за квартиру', 'а башня B достигает примерно 157 м.', 'data-pg="fin"']}


def build(PREV, NEWV, lang, prev_commit, meta_only=False):
    """meta_only: no PHP hunk (the calculator block is already live); only the FAQ meta follows a rewording of the article"""
    rp = json.load(open(os.path.join(QA, "deploy-result-%d.json" % PREV), encoding="utf-8"))
    assert str(rp.get("state", "")).startswith("released"), "1.72.%d must be released first (state: %s)" % (PREV, rp.get("state"))
    if meta_only:  # the previous release may not have written inc/project-stage.php (1.72.653 was the designer's)
        return build_meta_only(PREV, NEWV, lang, rp["files"].get(REL) or "unchanged since its last release")
    LIVE_MD5 = rp["files"][REL]
    _base = os.path.join(PLUG, "inc", "project-stage.php")
    _bt = open(_base, "rb").read()
    if md5(_bt) != LIVE_MD5:  # a second run: rebuild from git (the previous release's commit holds the live text)
        _g = subprocess.run(["git", "-C", REPO, "show", prev_commit + ":plugins/nadlan-config/inc/project-stage.php"], capture_output=True)
        assert _g.returncode == 0 and md5(_g.stdout) == LIVE_MD5, "no copy of the 1.72.%d project-stage.php to hunk" % PREV
        _bt = _g.stdout
    live_txt = _bt.decode("utf-8")
    assert "\r\n" not in live_txt
    HUNKS = [] if meta_only else hunks(lang)
    fins = live_txt.count('data-pg="fin"')
    if meta_only:
        return build_meta_only(PREV, NEWV, lang, LIVE_MD5)
    new_txt = live_txt
    for a, b in HUNKS:
        assert new_txt.count(a) == 1, "anchor x%d: %r" % (new_txt.count(a), a[:80])
        new_txt = new_txt.replace(a, b)
    assert new_txt.count('data-pg="fin"') == fins + 1
    _php = os.path.join(os.environ.get("LOCALAPPDATA", ""), "Microsoft", "WinGet", "Packages")
    _php = next((os.path.join(_php, d, "php.exe") for d in sorted(os.listdir(_php)) if d.startswith("PHP.PHP.8.1_")), "php") if os.path.isdir(_php) else "php"
    _tmp = os.path.join(H, "_tmp_%d_project-stage.php" % NEWV)
    open(_tmp, "w", encoding="utf-8", newline="\n").write(new_txt)
    _o = subprocess.run([_php, "-l", _tmp], capture_output=True, text=True, encoding="utf-8", errors="replace")
    os.remove(_tmp)
    assert _o.returncode == 0, "php -l: " + _o.stdout + _o.stderr
    print("[lint] live project-stage.php + the %d hunk(s) for %s: php -l ok" % (len(HUNKS), lang))
    open(_base, "w", encoding="utf-8", newline="\n").write(new_txt)

    src = open(os.path.join(H, "deploy%d.py" % PREV), encoding="utf-8").read()
    _m = re.search(r"^    import (\w+) as PX  # noqa: E402 \(.*$", src, re.M)
    assert _m and _m.group(1) == "kikar_%d" % PREV, "no PX import"
    _ns = {}
    exec(compile(open(os.path.join(H, "kikar_%d.py" % PREV), encoding="utf-8").read(), "kikar_%d" % PREV, "exec"), _ns)
    LIST = _ns.get("MAIN_NEW") or _ns["MAIN_LIST"]
    BUY = _ns["BUY"]
    assert "'price-nudge'" in LIST and "'designer'" in LIST and BUY == "'drone-map', 'buying-hub', 'i18n', "
    MOD = ('# -*- coding: utf-8 -*-\n"""Release 1.72.%d (HAD-712, the Kikar %s page: the calculator financing block and the FAQ meta): ONE hunk on '
           'the LIVE inc/project-stage.php (proven by its md5 below), and NO module-list hunk. Generated by make_deploy%d.py (kl_release.py)."""\n'
           "RELS = [%r]\nLIVE_MD5 = {%r: %r}\nPROOF = {%r: 'deploy-result-%d.json (the 1.72.%d file)'}\n"
           "HUNKS = %r\nFINS = %d\nMAIN_LIST = %r\nMAIN_NEW = MAIN_LIST\nBUY = %r\n\n\n"
           "def apply(rel, txt):\n"
           "    if rel != %r:\n        raise SystemExit('kikar_%d: no hunk on ' + rel)\n"
           "    for a, b in HUNKS:\n        if txt.count(a) != 1:\n            raise SystemExit('kikar_%d: FATAL anchor x%%d in %%s: %%r' %% (txt.count(a), rel, a[:60]))\n"
           "        txt = txt.replace(a, b)\n"
           "    if txt.count('data-pg=\"fin\"') != FINS + 1:\n"
           "        raise SystemExit('kikar_%d: FATAL the file is not as expected after the hunks')\n"
           "    print('[hunk] inc/project-stage.php: the %s Kikar calculator financing block, %%d hunk(s)' %% len(HUNKS))\n    return txt\n\n\n"
           "def apply_main(txt):\n"
           "    \"\"\"the module list stays as the previous release left it\"\"\"\n"
           "    if txt.count(MAIN_LIST) != 1 or \"'designer'\" not in MAIN_LIST:\n"
           "        raise SystemExit('kikar_%d: FATAL: the live module list tail is not the one the previous release left')\n"
           "    if txt.count(BUY) != 1 or txt.count(\"'buying-hub'\") != 1:\n"
           "        raise SystemExit('kikar_%d: FATAL: buying-hub is not once before i18n in the live nadlan-config.php; read it before releasing')\n"
           "    print(\"[hunk] nadlan-config.php: no module change ('designer' loaded, 'buying-hub' once before 'i18n', proven)\")\n"
           "    return txt\n") % (NEWV, lang, NEWV, REL, REL, LIVE_MD5, REL, PREV, PREV, HUNKS, fins, LIST, BUY, REL, NEWV, NEWV, NEWV, lang, NEWV, NEWV)
    open(os.path.join(H, "kikar_%d.py" % NEWV), "w", encoding="utf-8", newline="\n").write(MOD)
    sys.path.insert(0, H)
    _K = __import__("kikar_%d" % NEWV)
    assert _K.apply(REL, live_txt) == new_txt

    P, N, PP = str(PREV), str(NEWV), str(PREV - 1)
    assert src.count('WANT_LIVE = "1.72.%s"' % PP) == 1, "deploy%s.py is not built on 1.72.%s" % (P, PP)
    src = src.replace('WANT_LIVE = "1.72.%s"' % PP, 'WANT_LIVE = "@@WANT@@"')
    for a, b in [("1.72." + P, "1.72." + N), ("ps" + P, "ps" + N), ("bak" + P, "bak" + N), ("make_deploy" + P, "make_deploy" + N),
                 ("deploy-result-" + P, "deploy-result-" + N), ("speed-" + P, "speed-" + N), ("posts-before-" + P, "posts-before-" + N),
                 ("deploy-result-" + PP, "deploy-result-" + P)]:
        src = src.replace(a, b)
    src = src.replace('WANT_LIVE = "@@WANT@@"', 'WANT_LIVE = "1.72.%s"' % P)
    BS = chr(92)
    src = re.sub(r"\?t" + P + r"([a-z]*)=1", "?t" + N + BS + "1=1", src)
    src = re.sub(r"&t" + P + r"([a-z]*)=1", "&t" + N + BS + "1=1", src)
    src, n = re.subn(r"for n in range\(\d+, 329, -1\)", "for n in range(%s, 329, -1)" % P, src); assert n == 1, n
    src, n = re.subn(r"^    import kikar_%s as PX  # noqa: E402 \(.*$" % P,
                     "    import kikar_%s as PX  # noqa: E402 (1.72.%s: the %s Kikar calculator block on the live project-stage.php; the module list unchanged, proven)" % (N, N, lang), src, flags=re.M); assert n == 1, n
    src, n = re.subn(r'print\("RELEASE 1\.72\.%s LIVE: [^"]*"\)' % N, 'print("RELEASE 1.72.%s LIVE: the Kikar %s page: the calculator financing block and the FAQ schema with the five new questions")' % (N, lang), src); assert n == 1, n
    # no row may forbid what this release adds on the language page
    for _l in src.split("\n"):
        if "hamedina-%s/" % lang in _l and any(x in _l for x in ('data-pg="fin"', "nlpg__fin", "nlws-fig", "NLPG_MM")):
            if not any(x in _l.split("], [")[0] for x in ('data-pg="fin"',)):  # a row that REQUIRES them is fine
                raise SystemExit("a check row on the %s page names what this release adds; read it: %s" % (lang, _l.strip()[:200]))
    # the FAQ meta (the bridge's pmeta guard allows _nl_faq_schema on the four ids since 1.72.642)
    assert src.count("'_nl_faq_schema' === $key && in_array( $pid, array( 8114, 8116, 8117, 8118 ), true )") == 1, "the bridge's pmeta guard is not the 642 one"
    assert src.count("        for _fm in FAQ_META:") == 1, "the FAQ meta loop is not in the runner"
    _src = open(os.path.join(REPO, "scripts", "skin-a", "deployskin.py"), encoding="utf-8").read(); _rq = {"__name__": "mkl"}
    exec(compile(_src[:_src.index('s, h, _ = req("GET", "/wp-json/nadlan/v1/health")')], "h", "exec"), _rq)
    import hamedina_page_data as KD  # noqa: E402
    FM = [faq_meta(lang, KD, _rq["req"])]
    lines = src.split("\n")
    seen = set()
    for k, l in enumerate(lines):
        if l.startswith("PIN = {"):
            lines[k] = "PIN = {}  # 1.72.%s: no swapped file" % N; seen.add("PIN")
        elif l.startswith("NEWFILES = "):
            lines[k] = "NEWFILES = set()  # 1.72.%s: no new file" % N; seen.add("NEWFILES")
        elif l.startswith("FILES = ["):
            lines[k] = "FILES = []  # 1.72.%s: only the hunked live inc/project-stage.php" % N; seen.add("FILES")
        elif l.startswith("PHP_RELS = ["):
            lines[k] = "PHP_RELS = ['inc/project-stage.php']  # 1.72.%s: the hunked live file; restored from .bak%s on rollback with nadlan-config.php" % (N, N); seen.add("PHP_RELS")
        elif l.startswith("FAQ_META = "):
            lines[k] = "FAQ_META = " + repr(FM) + "  # 1.72.%s: before = the live meta (proven), after = the %s FAQ with five new questions" % (N, lang); seen.add("FAQ_META")
    assert seen == {"PIN", "NEWFILES", "FILES", "PHP_RELS", "FAQ_META"}, seen
    src = "\n".join(lines)
    ROWS = "    ('/projects/hamedina-%s/?t%sl=1', %r, ['Fatal error', 'Warning</b>'], []),\n" % (lang, N, NEED[lang])
    assert src.count("CHECKS = [\n") == 1
    src = src.replace("CHECKS = [\n", "CHECKS = [\n" + ROWS, 1)
    assert src.count("int(m.group(3)) + 1}") == 1, "the version bump is not +1 in deploy%s.py" % P
    assert ("kikar_%s as PX" % P) not in src and ("t" + P + "a=1") not in src
    assert src.count('WANT_LIVE = "1.72.%s"' % P) == 1 and src.count('BAK = ".bak%s"' % N) == 1 and src.count("range(%s, 329, -1)" % P) == 1
    assert src.count('if new != "1.72.%s":' % N) == 1
    open(os.path.join(H, "deploy%s.py" % N), "w", encoding="utf-8", newline="\n").write(src)
    print("deploy%s.py + kikar_%s.py written | the %s calculator block (1 hunk on project-stage.php) | FAQ meta %d (%d questions) | 1 new check row" % (N, N, lang, FM[0]["id"], FM[0]["n"]))

def build_release(PREV, NEWV, files, newfiles, hunks, live_md5, rows, msg, label):
    """a release that swaps asset files (FILES/NEWFILES/PIN) and hunks live PHP files (hunks: {rel: [(old, new), ...]},
    live_md5: {rel: md5 the live text must have}). Built on deploy<PREV>.py as every Kikar release. rows: extra CHECKS rows (source text)."""
    P, N, PP = str(PREV), str(NEWV), str(PREV - 1)
    src = open(os.path.join(H, "deploy%d.py" % PREV), encoding="utf-8").read()
    _m = re.search(r"^    import (\w+) as PX  # noqa: E402 \(.*$", src, re.M)
    assert _m, "no PX import in deploy%d.py" % PREV
    PXN = _m.group(1)
    _ns = {}
    exec(compile(open(os.path.join(H, PXN + ".py"), encoding="utf-8").read(), PXN, "exec"), _ns)
    LIST = _ns.get("MAIN_NEW") or _ns["MAIN_LIST"]
    BUY = _ns["BUY"]
    assert "'designer'" in LIST and BUY == "'drone-map', 'buying-hub', 'i18n', ", (LIST[-80:], BUY)
    # lint every hunked PHP file against its proven text (the repo copy must be the live text)
    _php = os.path.join(os.environ.get("LOCALAPPDATA", ""), "Microsoft", "WinGet", "Packages")
    _php = next((os.path.join(_php, d, "php.exe") for d in sorted(os.listdir(_php)) if d.startswith("PHP.PHP.8.1_")), "php") if os.path.isdir(_php) else "php"
    NEWTXT = {}
    for rel, hs in hunks.items():
        bt = open(os.path.join(PLUG, *rel.split("/")), "rb").read()
        assert md5(bt) == live_md5[rel], "the repo %s is not the proven live text (%s vs %s)" % (rel, md5(bt)[:10], live_md5[rel][:10])
        txt = bt.decode("utf-8")
        for a, b in hs:
            assert txt.count(a) == 1, "anchor x%d in %s: %r" % (txt.count(a), rel, a[:80])
            txt = txt.replace(a, b)
        tmp = os.path.join(H, "_tmp_%d_%s" % (NEWV, rel.replace("/", "_")))
        open(tmp, "w", encoding="utf-8", newline="\n").write(txt)
        o = subprocess.run([_php, "-l", tmp], capture_output=True, text=True, encoding="utf-8", errors="replace")
        os.remove(tmp)
        assert o.returncode == 0, "php -l %s: %s" % (rel, o.stdout + o.stderr)
        NEWTXT[rel] = txt
    for f in files:
        assert os.path.isfile(os.path.join(PLUG, *f.split("/"))), "no file " + f
        if f.endswith(".js"):
            o = subprocess.run(["node", "--check", os.path.join(PLUG, *f.split("/"))], capture_output=True, text=True)
            assert o.returncode == 0, "node --check %s: %s" % (f, o.stderr[-300:])
    PIN = {f: md5(open(os.path.join(PLUG, *f.split("/")), "rb").read()) for f in files}
    RELS = list(hunks)
    MOD = ('# -*- coding: utf-8 -*-\n"""Release 1.72.%d (HAD-712, %s). Generated by make_deploy%d.py (kl_release.build_release)."""\n'
           "RELS = %r\nLIVE_MD5 = %r\nPROOF = %r\nHUNKS = %r\nMAIN_LIST = %r\nMAIN_NEW = MAIN_LIST\nBUY = %r\n\n\n"
           "def apply(rel, txt):\n"
           "    if rel not in HUNKS:\n        raise SystemExit('kikar_%d: no hunk on ' + rel)\n"
           "    for a, b in HUNKS[rel]:\n        if txt.count(a) != 1:\n            raise SystemExit('kikar_%d: FATAL anchor x%%d in %%s: %%r' %% (txt.count(a), rel, a[:60]))\n"
           "        txt = txt.replace(a, b)\n"
           "    print('[hunk] %%s: %%d hunk(s)' %% (rel, len(HUNKS[rel])))\n    return txt\n\n\n"
           "def apply_main(txt):\n"
           "    if txt.count(MAIN_LIST) != 1 or \"'designer'\" not in MAIN_LIST:\n"
           "        raise SystemExit('kikar_%d: FATAL: the live module list tail is not the one the previous release left')\n"
           "    if txt.count(BUY) != 1 or txt.count(\"'buying-hub'\") != 1:\n"
           "        raise SystemExit('kikar_%d: FATAL: buying-hub is not once before i18n in the live nadlan-config.php')\n"
           "    print(\"[hunk] nadlan-config.php: no module change (proven)\")\n    return txt\n") % (
        NEWV, label, NEWV, RELS, {r: live_md5[r] for r in RELS}, {r: "the repo copy, equal to the live text the runner reads" for r in RELS},
        {r: hunks[r] for r in RELS}, LIST, BUY, NEWV, NEWV, NEWV, NEWV)
    open(os.path.join(H, "kikar_%d.py" % NEWV), "w", encoding="utf-8", newline="\n").write(MOD)
    assert src.count('WANT_LIVE = "1.72.%s"' % PP) == 1
    src = src.replace('WANT_LIVE = "1.72.%s"' % PP, 'WANT_LIVE = "@@WANT@@"')
    for a, b in [("1.72." + P, "1.72." + N), ("ps" + P, "ps" + N), ("bak" + P, "bak" + N), ("make_deploy" + P, "make_deploy" + N),
                 ("deploy-result-" + P, "deploy-result-" + N), ("speed-" + P, "speed-" + N), ("posts-before-" + P, "posts-before-" + N),
                 ("deploy-result-" + PP, "deploy-result-" + P)]:
        src = src.replace(a, b)
    src = src.replace('WANT_LIVE = "@@WANT@@"', 'WANT_LIVE = "1.72.%s"' % P)
    BS = chr(92)
    src = re.sub(r"\?t" + P + r"([a-z]*)=1", "?t" + N + BS + "1=1", src)
    src = re.sub(r"&t" + P + r"([a-z]*)=1", "&t" + N + BS + "1=1", src)
    src, n = re.subn(r"for n in range\(\d+, 329, -1\)", "for n in range(%s, 329, -1)" % P, src); assert n == 1, n
    src = "\n".join(re.sub(r"(\.js\?v=)1\.72\.\d+", r"\1", l) if "/tour/designer/" in l else l for l in src.split("\n"))
    src, n = re.subn(r"^    import %s as PX  # noqa: E402 \(.*$" % PXN, "    import kikar_%s as PX  # noqa: E402 (1.72.%s: %s)" % (N, N, label), src, flags=re.M); assert n == 1, n
    src, n = re.subn(r'print\("RELEASE 1\.72\.%s LIVE: [^"]*"\)' % N, 'print("RELEASE 1.72.%s LIVE: %s")' % (N, msg), src); assert n == 1, n
    lines = src.split("\n")
    seen = set()
    for k, l in enumerate(lines):
        if l.startswith("PIN = {"):
            lines[k] = "PIN = " + repr(PIN); seen.add("PIN")
        elif l.startswith("NEWFILES = "):
            lines[k] = "NEWFILES = " + repr(set(newfiles)) + "  # 1.72.%s" % N; seen.add("NEWFILES")
        elif l.startswith("FILES = ["):
            lines[k] = "FILES = " + repr(list(files)); seen.add("FILES")
        elif l.startswith("PHP_RELS = ["):
            lines[k] = "PHP_RELS = %r  # 1.72.%s: the hunked live files; restored from .bak%s on rollback with nadlan-config.php" % (RELS, N, N); seen.add("PHP_RELS")
        elif l.startswith("FAQ_META = "):
            lines[k] = "FAQ_META = []  # 1.72.%s: no meta" % N; seen.add("FAQ_META")
        elif l.startswith("YOAST_META = "):
            lines[k] = "YOAST_META = []  # 1.72.%s" % N
    assert seen == {"PIN", "NEWFILES", "FILES", "PHP_RELS", "FAQ_META"}, seen
    src = "\n".join(lines)
    src = src.replace("CHECKS = [\n", "CHECKS = [\n" + rows, 1)
    assert src.count('if new != "1.72.%s":' % N) == 1 and src.count('BAK = ".bak%s"' % N) == 1
    open(os.path.join(H, "deploy%s.py" % N), "w", encoding="utf-8", newline="\n").write(src)
    for rel, txt in NEWTXT.items():
        open(os.path.join(PLUG, *rel.split("/")), "w", encoding="utf-8", newline="\n").write(txt)
    print("deploy%s.py + kikar_%s.py written | %d files (%d new) | hunks on %s | %d row(s)" % (N, N, len(files), len(newfiles), RELS, rows.count("\n")))
