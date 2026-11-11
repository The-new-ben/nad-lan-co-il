# -*- coding: utf-8 -*-
"""make deploy642.py from deploy641.py: 1.72.642 = HAD-709 (HAD-699, Ben 10.11.2026: "complete Kikar seriously"): the Kikar status
in the facts strip and the progress strip of the five Kikar pages. The October 2026 publications: the towers' construction completed,
Form 4 expected by the end of 2026 or early 2027, the keys between the first quarter of 2027 and May 2027 (docs/qa/had-709/sources.md).
  HUNK on the LIVE inc/project-stage.php (the 1.72.639 file, md5 23d2552d68: deploy-result-639.json; 1.72.640-641 wrote other files;
  the runner reads it live again): in he, en, fr, ru and ar, the "status" fact and the last three progress steps
  (frame 4.2026 done, construction now, occupancy 2026-2028 next -> construction completed 10.2026 done, Form 4 now, handover
  1 to 5.2027 next). The articles' text is fixed apart (scripts/kikar/had709_occupancy.py for the Hebrew post).
nadlan-config.php, on its LIVE text: the version only."""
import hashlib, json, os, re, subprocess, sys
H = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.dirname(os.path.dirname(H))
PLUG = os.path.join(REPO, "plugins", "nadlan-config")
QA = os.path.join(REPO, "docs", "qa", "project-stage-2026-09-24")
PREV, NEWV = 641, 642
md5 = lambda b: hashlib.md5(b).hexdigest()
FILES = []
PIN = {}
rp = json.load(open(os.path.join(QA, "deploy-result-%d.json" % PREV), encoding="utf-8"))
assert str(rp.get("state", "")).startswith("released"), "1.72.%d must be released first" % PREV
for n in range(640, PREV + 1):
    _f = json.load(open(os.path.join(QA, "deploy-result-%d.json" % n), encoding="utf-8")).get("files") or {}
    assert "inc/project-stage.php" not in _f, "1.72.%d wrote inc/project-stage.php" % n
REL = "inc/project-stage.php"
LIVE_MD5 = json.load(open(os.path.join(QA, "deploy-result-639.json"), encoding="utf-8"))["files"][REL]
assert LIVE_MD5 == "23d2552d68e7b3e41d79021352d41699"
_base = os.path.join(PLUG, "inc", "project-stage.php")
_bt = open(_base, "rb").read()
if md5(_bt) != LIVE_MD5:  # a second run: rebuild from git (the 639 commit holds the live text)
    _g = subprocess.run(["git", "-C", REPO, "show", "2a36e4ee:plugins/nadlan-config/inc/project-stage.php"], capture_output=True)
    assert _g.returncode == 0 and md5(_g.stdout) == LIVE_MD5, "no copy of the 1.72.639 project-stage.php to hunk"
    _bt = _g.stdout
live_txt = _bt.decode("utf-8").replace("\r\n", "\n")
T5, T7 = "\t" * 5, "\t" * 7
HUNKS = [
    # he
    (T5 + "array( 'מצב', 'השלד הושלם', 'ב-23.4.2026' ),\n",
     T5 + "array( 'מצב', 'הבנייה הושלמה', 'פורסם ב-10.2026 · גמר שלד ב-23.4.2026' ), // HAD-709 (1.72.642): the October 2026 publications\n"),
    (T5 + "array( 'השלד הושלם', '4.2026', 'done' ),\n" + T5 + "array( 'בבנייה', 'עכשיו', 'now' ),\n" + T5 + "array( 'אכלוס', '2026 עד 2028', 'next' ),\n",
     T5 + "array( 'הבנייה הושלמה', '10.2026', 'done' ),\n" + T5 + "array( 'טופס 4', 'סוף 2026 או תחילת 2027', 'now' ),\n" + T5 + "array( 'מסירת דירות', '1 עד 5.2027', 'next' ), // HAD-709: docs/qa/had-709/sources.md\n"),
    # en
    (T7 + "array( 'Status', 'Frame completed', 'On 23.4.2026' ),\n",
     T7 + "array( 'Status', 'Construction completed', 'Reported 10.2026 · frame 23.4.2026' ),\n"),
    (T7 + "array( 'Frame completed', '4.2026', 'done' ),\n" + T7 + "array( 'Construction', 'now', 'now' ),\n" + T7 + "array( 'Occupancy', '2026 to 2028', 'next' ),\n",
     T7 + "array( 'Construction completed', '10.2026', 'done' ),\n" + T7 + "array( 'Form 4 (occupancy permit)', 'end 2026 or early 2027', 'now' ),\n" + T7 + "array( 'Handover', '1 to 5.2027', 'next' ),\n"),
    # fr
    (T7 + "array( 'Avancement', 'Gros œuvre achevé', 'Le 23 avril 2026' ),\n",
     T7 + "array( 'Avancement', 'Construction achevée', 'Annoncée en 10/2026 · gros œuvre le 23 avril 2026' ),\n"),
    (T7 + "array( 'Gros œuvre achevé', '04/2026', 'done' ),\n" + T7 + "array( 'En construction', 'aujourd’hui', 'now' ),\n" + T7 + "array( 'Livraison', 'de 2026 à 2028', 'next' ),\n",
     T7 + "array( 'Construction achevée', '10/2026', 'done' ),\n" + T7 + "array( 'Formulaire 4', 'fin 2026 ou début 2027', 'now' ),\n" + T7 + "array( 'Livraison', '01 à 05/2027', 'next' ),\n"),
    # ru
    (T7 + "array( 'Статус', 'Каркас завершён', '23.04.2026' ),\n",
     T7 + "array( 'Статус', 'Строительство завершено', 'Объявлено в 10.2026 · каркас 23.04.2026' ),\n"),
    (T7 + "array( 'Каркас завершён', '04.2026', 'done' ),\n" + T7 + "array( 'Строительство', 'сейчас', 'now' ),\n" + T7 + "array( 'Заселение', 'с 2026 по 2028 год', 'next' ),\n",
     T7 + "array( 'Строительство завершено', '10.2026', 'done' ),\n" + T7 + "array( 'Форма 4', 'конец 2026 или начало 2027', 'now' ),\n" + T7 + "array( 'Заселение', '01–05.2027', 'next' ),\n"),
    # ar
    (T7 + "array( 'الوضع', 'اكتمل الهيكل', 'في 23.4.2026' ),\n",
     T7 + "array( 'الوضع', 'اكتمل البناء', 'أُعلن في 10.2026 · الهيكل في 23.4.2026' ),\n"),
    (T7 + "array( 'اكتمال الهيكل', '4.2026', 'done' ),\n" + T7 + "array( 'قيد البناء', 'الآن', 'now' ),\n" + T7 + "array( 'السكن', 'بين 2026 و2028', 'next' ),\n",
     T7 + "array( 'اكتمال البناء', '10.2026', 'done' ),\n" + T7 + "array( 'استمارة 4', 'نهاية 2026 أو بداية 2027', 'now' ),\n" + T7 + "array( 'السكن', '1 إلى 5.2027', 'next' ),\n"),
]
GONE = ["'2026 עד 2028'", "'2026 to 2028'", "'de 2026 à 2028'", "'с 2026 по 2028 год'", "'بين 2026 و2028'"]


def _apply(txt):
    for a, b in HUNKS:
        if txt.count(a) != 1:
            raise SystemExit("kikar_642: FATAL anchor x%d in %s: %r" % (txt.count(a), REL, a[:80]))
        txt = txt.replace(a, b)
    if any(g in txt for g in GONE) or txt.count("'10.2026', 'done' )") != 4 or txt.count("'10/2026', 'done' )") != 1:
        raise SystemExit("kikar_642: FATAL the five status strips are not where they should be")
    return txt


new_txt = _apply(live_txt)
_php = os.path.join(os.environ.get("LOCALAPPDATA", ""), "Microsoft", "WinGet", "Packages")
_php = next((os.path.join(_php, d, "php.exe") for d in sorted(os.listdir(_php)) if d.startswith("PHP.PHP.8.1_")), "php") if os.path.isdir(_php) else "php"
_tmp = os.path.join(H, "_tmp_642_project-stage.php")
open(_tmp, "w", encoding="utf-8", newline="\n").write(new_txt)
_o = subprocess.run([_php, "-l", _tmp], capture_output=True, text=True, encoding="utf-8", errors="replace")
os.remove(_tmp)
assert _o.returncode == 0, "php -l: " + _o.stdout + _o.stderr
print("[lint] live project-stage.php + the 642 hunks: php -l ok")
open(_base, "w", encoding="utf-8", newline="\n").write(new_txt)

src = open(os.path.join(H, "deploy%d.py" % PREV), encoding="utf-8").read()
_m = re.search(r"^    import (\w+) as PX  # noqa: E402 \(.*$", src, re.M)
assert _m and _m.group(1) == "kikar_641", "no PX import"
_ns = {}
exec(compile(open(os.path.join(H, "kikar_641.py"), encoding="utf-8").read(), "kikar_641", "exec"), _ns)
LIST = _ns.get("MAIN_NEW") or _ns["MAIN_LIST"]
BUY = _ns["BUY"]
assert "'price-nudge'" in LIST and BUY == "'drone-map', 'buying-hub', 'i18n', "
MOD = ('# -*- coding: utf-8 -*-\n"""Release 1.72.642 (HAD-709, the Kikar status strips in five languages): ONE inc/ hunk set, on the LIVE '
       'inc/project-stage.php (proven by its md5 below), and NO module-list hunk. Generated by make_deploy642.py."""\n'
       "RELS = [%r]\nLIVE_MD5 = {%r: %r}\nPROOF = {%r: 'deploy-result-639.json (the 1.72.639 file); 1.72.640-641 wrote other files'}\n"
       "HUNKS = %r\nGONE = %r\nMAIN_LIST = %r\nMAIN_NEW = MAIN_LIST\nBUY = %r\n\n\n"
       "def apply(rel, txt):\n"
       "    if rel != %r:\n        raise SystemExit('kikar_642: no hunk on ' + rel)\n"
       "    for a, b in HUNKS:\n        if txt.count(a) != 1:\n            raise SystemExit('kikar_642: FATAL anchor x%%d in %%s: %%r' %% (txt.count(a), rel, a[:80]))\n"
       "        txt = txt.replace(a, b)\n"
       "    if any(g in txt for g in GONE) or txt.count(\"'10.2026', 'done' )\") != 4 or txt.count(\"'10/2026', 'done' )\") != 1:\n"
       "        raise SystemExit('kikar_642: FATAL the five status strips are not where they should be')\n"
       "    print('[hunk] inc/project-stage.php: the Kikar status strips in five languages, %%d hunks' %% len(HUNKS))\n    return txt\n\n\n"
       "def apply_main(txt):\n"
       "    \"\"\"the module list stays as the previous release left it\"\"\"\n"
       "    if txt.count(MAIN_LIST) != 1 or \"'price-nudge'\" not in MAIN_LIST:\n"
       "        raise SystemExit('kikar_642: FATAL: the live module list tail is not the one the previous release left')\n"
       "    if txt.count(BUY) != 1 or txt.count(\"'buying-hub'\") != 1:\n"
       "        raise SystemExit('kikar_642: FATAL: buying-hub is not once before i18n in the live nadlan-config.php; read it before releasing')\n"
       "    print(\"[hunk] nadlan-config.php: no module change ('price-nudge' loaded, 'buying-hub' once before 'i18n', proven)\")\n"
       "    return txt\n") % (REL, REL, LIVE_MD5, REL, HUNKS, GONE, LIST, BUY, REL)
open(os.path.join(H, "kikar_642.py"), "w", encoding="utf-8", newline="\n").write(MOD)
sys.path.insert(0, H)
import kikar_642 as _K  # noqa: E402
assert _K.apply(REL, live_txt) == new_txt

P, N, PP = str(PREV), str(NEWV), str(PREV - 1)
assert src.count('WANT_LIVE = "1.72.%s"' % PP) == 1, "deploy641.py is not built on 1.72.640"
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
src, n = re.subn(r"^    import kikar_641 as PX  # noqa: E402 \(.*$", "    import kikar_642 as PX  # noqa: E402 (1.72.642: the Kikar status strips on the live project-stage.php; the module list unchanged, proven)", src, flags=re.M); assert n == 1, n
src, n = re.subn(r'print\("RELEASE 1\.72\.642 LIVE: [^"]*"\)', 'print("RELEASE 1.72.642 LIVE: the Kikar status strips (construction completed 10.2026, Form 4, handover 1 to 5.2027) in five languages")', src); assert n == 1, n
# the language pages' FAQPage lives in post meta _nl_faq_schema (inc/schema-meta.php), built from the visible FAQ by
# hamedina_page_data.faq_json(). The articles were fixed by scripts/kikar/had709_occupancy.py (11.11.2026); here the meta follows.
# Proof: faq_json() over each post's text BEFORE that fix equals the JSON the live page prints today, byte for byte.
import base64, glob, html as _html, urllib.request  # noqa: E402
import hamedina_page_data as KD  # noqa: E402
_src = open(os.path.join(REPO, "scripts", "skin-a", "deployskin.py"), encoding="utf-8").read(); _rq = {"__name__": "m642"}
exec(compile(_src[:_src.index('s, h, _ = req("GET", "/wp-json/nadlan/v1/health")')], "h", "exec"), _rq)
_res = sorted(glob.glob(os.path.join(REPO, "docs", "qa", "had-709", "result-*.json")))
assert _res, "run scripts/kikar/had709_occupancy.py --go first"
_R = json.load(open(_res[-1], encoding="utf-8")); _stamp = _R["stamp"]
FAQ_META = []
for _lang, _pid in (("en", 8114), ("fr", 8116), ("ru", 8117), ("ar", 8118)):
    _old = open(os.path.join(REPO, "docs", "qa", "had-709", "backup-%d-%s.html" % (_pid, _stamp)), encoding="utf-8").read()
    _s, _g, _ = _rq["req"]("GET", "/wp-json/wp/v2/nadlan_project/%d?context=edit&_fields=content" % _pid)
    _new = _g["content"]["raw"]
    assert md5(_new.encode("utf-8")) == _R["posts"][_lang]["after_md5"], _lang + ": the live post is not the one had709 wrote"
    _page = urllib.request.urlopen(urllib.request.Request("https://nad-lan.co.il/projects/%s/?m642=%d" % (KD.POSTS[_lang]["slug"], _pid), headers={"User-Agent": "Mozilla/5.0"}), timeout=60).read().decode("utf-8")
    _live = [j for j in re.findall(r'<script type="application/ld\+json">(.*?)</script>', _page, re.S) if '"FAQPage"' in j and '"inLanguage":"%s"' % _lang in j]
    assert len(_live) == 1, (_lang, len(_live))
    KD.content = (lambda t: (lambda lang: re.sub(r">\s*\n\s*<", "><", t.strip())))(_old)
    assert KD.faq_json(_lang) == _live[0], _lang + ": faq_json() over the old text is not the live FAQ meta; the method is not proven"
    _before = base64.b64encode(_live[0].encode("utf-8")).decode("ascii")
    KD.content = (lambda t: (lambda lang: re.sub(r">\s*\n\s*<", "><", t.strip())))(_new)
    _j = KD.faq_json(_lang); json.loads(_j)
    assert _j != _live[0] and "2027" in _j and "2028" not in _j.split('"name"')[0], _lang
    _after = base64.b64encode(_j.encode("utf-8")).decode("ascii")
    FAQ_META.append({"id": _pid, "before": _before, "before_md5": md5(_before.encode("ascii")), "after": _after, "n": len(json.loads(_j)["mainEntity"])})
    print("[faq] %s %d: proven on the live meta; new FAQ JSON %d questions" % (_lang, _pid, FAQ_META[-1]["n"]))
_GUARD_OLD = "if ( 0 !== strpos( $key, '_yoast_wpseo_' ) ) { return new WP_Error( 'key', 'only Yoast metas', array( 'status' => 400 ) ); }"
_GUARD_NEW = ("if ( 0 !== strpos( $key, '_yoast_wpseo_' ) && ! ( '_nl_faq_schema' === $key && in_array( $pid, array( 8114, 8116, 8117, 8118 ), true ) ) ) "
              "{ return new WP_Error( 'key', 'only Yoast metas and, since 1.72.642, the Kikar language pages FAQ meta', array( 'status' => 400 ) ); }")
assert src.count(_GUARD_OLD) == 1, "the bridge's pmeta guard is not where it should be"
src = src.replace(_GUARD_OLD, _GUARD_NEW, 1)
_HOOK = "        # 1.72.642: no option is written (the advisor key and pages stay as 1.72.619 stored them)\n"
assert src.count(_HOOK) == 1, "the place after the post writes is not where it should be"
src = src.replace(_HOOK, _HOOK + (
    "        for _fm in FAQ_META:  # 1.72.642 (HAD-709): the language pages' FAQPage meta follows their new visible FAQ answer\n"
    "            _g = ops({\"pmeta\": {\"id\": _fm[\"id\"], \"key\": \"_nl_faq_schema\", \"get\": 1}}, \"faq meta get %d\" % _fm[\"id\"])[\"pmeta\"]\n"
    "            if _g[\"md5\"] != _fm[\"before_md5\"]:\n"
    "                raise SystemExit(f\"FATAL faq meta {_fm['id']}: live {_g['md5'][:10]} is not the proven {_fm['before_md5'][:10]}\")\n"
    "            UNDO.append((\"meta\", {\"id\": _fm[\"id\"], \"key\": \"_nl_faq_schema\", \"before\": _fm[\"before\"].encode(\"ascii\"), \"before_md5\": _fm[\"before_md5\"]}))\n"
    "            _w = ops({\"pmeta\": {\"id\": _fm[\"id\"], \"key\": \"_nl_faq_schema\", \"expect\": _fm[\"before_md5\"], \"b64\": base64.b64encode(_fm[\"after\"].encode(\"ascii\")).decode(), \"md5\": md5(_fm[\"after\"].encode(\"ascii\"))}}, \"faq meta %d\" % _fm[\"id\"])[\"pmeta\"]\n"
    "            if _w[\"md5\"] != md5(_fm[\"after\"].encode(\"ascii\")):\n"
    "                raise SystemExit(f\"FATAL faq meta {_fm['id']}: read back {_w['md5'][:10]}\")\n"
    "            print(f\"[faq] {_fm['id']}: _nl_faq_schema written and read back ({_fm['n']} questions)\")\n"), 1)
_FM = "FAQ_META = " + repr([{k: v for k, v in f.items()} for f in FAQ_META]) + "  # 1.72.642: before = the live meta (proven), after = the new FAQ\n"
assert src.count("\nUNDO = []") == 1
src = src.replace("\nUNDO = []", "\n" + _FM + "UNDO = []", 1)
# the strips (this release) and the articles (scripts/kikar/had709_occupancy.py, run before this release); the old window is
# forbidden in the whole HTML, so the FAQ schema in the head is checked too
ROWS = ("    ('/projects/hamedina/?t642s=1', ['class=\"nlprog\"', 'הבנייה הושלמה', 'סוף 2026 או תחילת 2027', '1 עד 5.2027', 'ומסירת הדירות בין הרבעון הראשון של 2027 למאי 2027', 'פורסם על השלמת הקמת המגדלים'], [], ['2026 עד 2028', '2026 ל-2028']),\n"
        "    ('/projects/hamedina-en/?t642s=1', ['class=\"nlprog\"', 'Construction completed', 'end 2026 or early 2027', '1 to 5.2027', 'handover between the first quarter of 2027 and May 2027'], [], ['2026 to 2028']),\n"
        "    ('/projects/hamedina-fr/?t642s=1', ['class=\"nlprog\"', 'Construction achevée', '01 à 05/2027', 'la remise des clés entre le premier trimestre 2027 et mai 2027'], [], ['de 2026 à 2028']),\n"
        "    ('/projects/hamedina-ru/?t642s=1', ['class=\"nlprog\"', 'Строительство завершено', '01–05.2027', 'между первым кварталом 2027 года и маем 2027 года'], [], ['с 2026 по 2028']),\n"
        "    ('/projects/hamedina-ar/?t642s=1', ['class=\"nlprog\"', 'اكتمل البناء', '1 إلى 5.2027', 'وتسليم الشقق بين الربع الأول من 2027 وأيار 2027'], [], ['بين 2026 و2028', 'من 2026 إلى 2028']),\n")
assert src.count("CHECKS = [\n") == 1
src = src.replace("CHECKS = [\n", "CHECKS = [\n" + ROWS, 1)
assert src.count("int(m.group(3)) + 1}") == 1, "the version bump is not +1 in deploy641.py"
lines = src.split("\n")
seen = set()
for k, l in enumerate(lines):
    if l.startswith("PIN = {"):
        lines[k] = "PIN = {}  # 1.72.642: no swapped file"; seen.add("PIN")
    elif l.startswith("NEWFILES = "):
        lines[k] = "NEWFILES = set()  # 1.72.642: no new file"; seen.add("NEWFILES")
    elif l.startswith("FILES = ["):
        lines[k] = "FILES = []  # 1.72.642: only the hunked live inc/project-stage.php"; seen.add("FILES")
    elif l.startswith("PHP_RELS = ["):
        lines[k] = "PHP_RELS = ['inc/project-stage.php']  # 1.72.642: the hunked live file; restored from .bak642 on rollback with nadlan-config.php"; seen.add("PHP_RELS")
assert seen == {"PIN", "NEWFILES", "FILES", "PHP_RELS"}, seen
src = "\n".join(lines)
assert "kikar_641 as PX" not in src and ("t" + P + "p=1") not in src
assert src.count('WANT_LIVE = "1.72.641"') == 1 and src.count('BAK = ".bak642"') == 1 and src.count("range(641, 329, -1)") == 1
assert src.count('if new != "1.72.642":') == 1
open(os.path.join(H, "deploy642.py"), "w", encoding="utf-8", newline="\n").write(src)
print("deploy642.py + kikar_642.py written | the status strips hunk (%d anchors) | 5 new check rows" % len(HUNKS))
