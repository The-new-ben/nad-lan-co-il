# -*- coding: utf-8 -*-
"""HAD-709 (Ben 10.11.2026, "complete Kikar seriously"): the five Kikar articles (/projects/hamedina/ and -en, -fr, -ru, -ar) still say
"occupancy 2026 to 2028" and "no Form 4 date was published". The October 2026 publications say the towers' construction was completed,
Form 4 is expected by the end of 2026 (one says early 2027) and the keys between the first quarter of 2027 and May 2027.
Small anchored replacements on the LIVE post text of each language (the Hebrew post carries 7.11.2026 links by another session; never
a full overwrite). Each post's live md5 is pinned; each anchor must appear exactly once. The articles name no outlet (the owner's
rule of 1.10.2026); the sources are in docs/qa/had-709/sources.md. Backup before, read-back after (restored if it differs); dry by default.
  python scripts/kikar/had709_occupancy.py [--go] [he,en,fr,ru,ar]"""
import hashlib, io, json, os, sys, time
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.dirname(os.path.dirname(HERE))
src = open(os.path.join(REPO, "scripts", "skin-a", "deployskin.py"), encoding="utf-8").read(); ns = {"__name__": "h709"}
exec(compile(src[:src.index('s, h, _ = req("GET", "/wp-json/nadlan/v1/health")')], "h", "exec"), ns); req = ns["req"]
GO = "--go" in sys.argv
ONLY = next((a.split(",") for a in sys.argv[1:] if not a.startswith("--")), ["he", "en", "fr", "ru", "ar"])

HE = "טופס 4 צפוי עד סוף 2026 או בתחילת 2027, ומסירת הדירות בין הרבעון הראשון של 2027 למאי 2027"
EN = "Form 4 is expected by the end of 2026 or early 2027, and handover between the first quarter of 2027 and May 2027"
FR = "le formulaire 4 est attendu d’ici fin 2026 ou début 2027, et la remise des clés entre le premier trimestre 2027 et mai 2027"
RU = "Форма 4 ожидается до конца 2026 года или в начале 2027 года, а передача квартир — между первым кварталом 2027 года и маем 2027 года"
AR = "يُتوقع صدور استمارة 4 حتى نهاية 2026 أو مطلع 2027، وتسليم الشقق بين الربع الأول من 2027 وأيار 2027"

POSTS = {
    "he": (8113, "hamedina", "ee11b1bf7dbb98c941294987deb531c8", [  # modified 2026-11-07T20:51:24 (the 7.11 links)
        ("נכון ל-23.4.2026 נרשם גמר שלד, והערכות האכלוס שפורסמו נעות בין 2026 ל-2028.",
         "באוקטובר 2026 פורסם על השלמת הקמת המגדלים, ולפי הפרסומים מאותו חודש " + HE + "."),
        ("<td>נכון ל-23.4.2026 מצוין גמר שלד. זהו שלב בבנייה, בנפרד ממסירת הדירות.</td>",
         "<td>גמר שלד ב-23.4.2026, והשלמת הקמת המגדלים פורסמה ב-10.2026. זהו שלב בבנייה, בנפרד ממסירת הדירות.</td>"),
        ("<td>2026 עד 2028. מועד אכלוס רשמי לא פורסם.",
         "<td>לפי פרסומים מ-10.2026, " + HE + ". מועד אכלוס רשמי לא פורסם."),
        ("<p>הערכות האכלוס שפורסמו נעות בין 2026 ל-2028; מועד אכלוס רשמי לא פורסם. אבן הדרך המתועדת בבנייה היא גמר שלד ב-23.4.2026.",
         "<p>נכון ל-11.2026: באוקטובר 2026 פורסם על השלמת הקמת המגדלים, אחרי גמר השלד ב-23.4.2026. לפי הפרסומים מאוקטובר 2026, " + HE + ". מועד אכלוס רשמי לא פורסם."),
        ("<p>בפרסומי חברות הבנייה מופיעים 2026 ו-4.2027. בהערכה של הגורם המממן מ-9.2025 דובר על השלמה בתוך כשנתיים, סביב 2027. פרסום מ-4.2025 הצביע על סוף 2028.",
         "<p>בפרסומים מאוקטובר 2026, עם השלמת הבנייה, הופיעו שלושה טווחים למסירת הדירות: מרץ עד אפריל 2027, אפריל עד מאי 2027 והרבעון הראשון של 2027. "
         "קודם לכן הופיעו בפרסומי חברות הבנייה 2026 ו-4.2027, בהערכה של הגורם המממן מ-9.2025 דובר על השלמה בתוך כשנתיים, סביב 2027, ופרסום מ-4.2025 הצביע על סוף 2028."),
        ("<p>מועד רשמי לקבלת טופס 4 לא פורסם. לקראת המעבר,",
         "<p>מועד רשמי לקבלת טופס 4 לא פורסם. בפרסומים מאוקטובר 2026 טופס 4 צפוי עד סוף 2026, ובאחד מהם בתחילת 2027. לקראת המעבר,"),
        ("<li class=\"is-now\"><b>4.2026</b> ב-23.4.2026 נרשם גמר שלד. אבן הדרך מתעדת את השלמת השלד, בנפרד מהמשך ההתקדמות למסירת הדירות ולאכלוס.</li></ol>",
         "<li><b>4.2026</b> ב-23.4.2026 נרשם גמר שלד. אבן הדרך מתעדת את השלמת השלד, בנפרד מהמשך ההתקדמות למסירת הדירות ולאכלוס.</li>"
         "<li class=\"is-now\"><b>10.2026</b> פורסם על השלמת הקמת המגדלים. לפי הפרסומים מאותו חודש, " + HE + ".</li></ol>"),
        ("<p>הערכות האכלוס שפורסמו נעות בין 2026 ל-2028, ומועד רשמי לקבלת טופס 4 לא פורסם. גמר השלד מתועד ל-23.4.2026.",
         "<p>לפי פרסומים מאוקטובר 2026, עם השלמת הקמת המגדלים, " + HE + ". מועד אכלוס רשמי לא פורסם. גמר השלד מתועד ל-23.4.2026."),
    ]),
    "en": (8114, "hamedina-en", "24284c4d38195dbd71fa49c2cd72d2f8", [
        ("The frame was recorded as completed on 23 April 2026. Three published deals",
         "The frame was recorded as completed on 23 April 2026, and the towers’ construction was reported completed in October 2026. Three published deals"),
        ("<td>The frame was recorded as completed on 23 April 2026.</td>",
         "<td>The frame was recorded as completed on 23 April 2026; the towers’ construction was reported completed in October 2026.</td>"),
        ("<td>Published estimates range from 2026 to 2028. An official date for Form 4",
         "<td>According to publications from October 2026, " + EN + ". An official date for Form 4"),
        ("Published occupancy estimates span 2026 to 2028, and an official Form 4 date is not published.",
         "Publications from October 2026, when the towers’ construction was reported completed, say that " + EN + "; an official Form 4 date is not published."),
        ("<p>The builders’ published estimates include 2026 and April 2027.",
         "<p>Publications from October 2026, when construction was completed, gave three handover windows: March to April 2027, April to May 2027, and the first quarter of 2027. Before that, the builders’ published estimates included 2026 and April 2027."),
        ("<li class=\"is-now\"><b>23 April 2026</b> The frame is recorded as completed, the latest recorded structural milestone in this timeline.</li>",
         "<li><b>23 April 2026</b> The frame is recorded as completed.</li><li class=\"is-now\"><b>October 2026</b> The towers’ construction is reported completed. Publications from that month say that " + EN + ".</li>"),
        ("<p>There is no published official occupancy date; estimates for the towers range from 2026 to 2028.",
         "<p>There is no published official occupancy date. Publications from October 2026, when the towers’ construction was reported completed, say that " + EN + "."),
    ]),
    "fr": (8116, "hamedina-fr", "2e43e7bbc331c2543f179b7eb973536e", [
        ("Le gros œuvre était déclaré achevé le 23 avril 2026. En 2024",
         "Le gros œuvre était déclaré achevé le 23 avril 2026, et l’achèvement de la construction des tours a été annoncé en octobre 2026. En 2024"),
        ("<td>Déclaré achevé au 23 avril 2026.</td>",
         "<td>Gros œuvre déclaré achevé au 23 avril 2026 ; achèvement de la construction annoncé en octobre 2026.</td>"),
        ("<td>De 2026 à 2028 ; la date propre à un appartement",
         "<td>Selon les publications d’octobre 2026, " + FR + " ; la date propre à un appartement"),
        ("<p>Le gros œuvre des tours Kikar Hamedina était déclaré achevé au 23 avril 2026. Ce jalon renseigne sur l’avancement de la structure ; il ne fixe pas à lui seul la date à laquelle vous pourrez emménager.",
         "<p>Le gros œuvre des tours Kikar Hamedina était déclaré achevé au 23 avril 2026, et l’achèvement de la construction a été annoncé en octobre 2026. Selon les publications de ce mois, " + FR + ". "
         "Ces jalons renseignent sur l’avancement du chantier ; ils ne fixent pas à eux seuls la date à laquelle vous pourrez emménager."),
        ("<p>Les calendriers publiés des constructeurs mentionnent 2026 et avril 2027. Une estimation du responsable du financement, en septembre 2025, envisageait une livraison dans environ 2 ans, soit autour de 2027. Une estimation d’avril 2025 allait jusqu’à la fin de 2028. La fourchette des échéances publiées s’étend donc de 2026 à 2028.</p>",
         "<p>Les publications d’octobre 2026, au moment de l’achèvement de la construction, donnent trois fenêtres de livraison : mars à avril 2027, avril à mai 2027 et le premier trimestre 2027. "
         "Auparavant, les calendriers publiés des constructeurs mentionnaient 2026 et avril 2027 ; une estimation du responsable du financement, en septembre 2025, envisageait une livraison dans environ 2 ans, soit autour de 2027 ; et une estimation d’avril 2025 allait jusqu’à la fin de 2028.</p>"),
        ("<p>Aucune date officielle de délivrance du formulaire 4 n’est publiée. Pour l’appartement retenu",
         "<p>Aucune date officielle de délivrance du formulaire 4 n’est publiée ; les publications d’octobre 2026 l’attendent d’ici fin 2026, l’une d’elles début 2027. Pour l’appartement retenu"),
        ("<li class=\"is-now\"><b>23 avril 2026</b> Le suivi municipal du chantier porte la mention « gros œuvre achevé ». C’est le jalon daté concernant la structure des bâtiments.</li>",
         "<li><b>23 avril 2026</b> Le suivi municipal du chantier porte la mention « gros œuvre achevé ». C’est le jalon daté concernant la structure des bâtiments.</li>"
         "<li class=\"is-now\"><b>Octobre 2026</b> L’achèvement de la construction des tours est annoncé. Selon les publications de ce mois, " + FR + ".</li>"),
        ("<p>Les estimations publiées vont de 2026 à 2028, sans date officielle de délivrance du formulaire 4 publiée.",
         "<p>Selon les publications d’octobre 2026, au moment de l’achèvement de la construction, " + FR + " ; aucune date officielle de délivrance du formulaire 4 n’est publiée."),
    ]),
    "ru": (8117, "hamedina-ru", "3f3f765bea17eae062dece4d4d302e89", [
        ("На 23.04.2026 зафиксировано завершение каркаса; оценки заселения охватывают период с 2026 по 2028 год.",
         "На 23.04.2026 зафиксировано завершение каркаса, а в октябре 2026 года объявлено о завершении строительства башен; по публикациям того месяца, " + RU + "."),
        ("<td>На 23.04.2026 указан этап завершения каркаса. Это строительная веха, отдельная от разрешения на заселение.</td>",
         "<td>На 23.04.2026 указан этап завершения каркаса; в октябре 2026 года объявлено о завершении строительства. Это строительные вехи, отдельные от разрешения на заселение.</td>"),
        ("<td>Опубликованные оценки охватывают период с 2026 по 2028 год. Официальная дата",
         "<td>По публикациям октября 2026 года, " + RU + ". Официальная дата"),
        ("<p>Опубликованные оценки заселения охватывают период с 2026 по 2028 год. На 23.04.2026 зафиксирован этап завершения каркаса.",
         "<p>На ноябрь 2026 года: в октябре 2026 года объявлено о завершении строительства башен, после завершения каркаса 23.04.2026. По публикациям октября 2026 года, " + RU + "."),
        ("<p>В опубликованных строителями сроках фигурируют 2026 год и апрель 2027 года.",
         "<p>В публикациях октября 2026 года, на момент завершения строительства, названы три окна передачи: март–апрель 2027 года, апрель–май 2027 года и первый квартал 2027 года. Ранее в опубликованных строителями сроках фигурировали 2026 год и апрель 2027 года."),
        ("<li class=\"is-now\"><b>Апрель 2026 года.</b> В строительной записи зафиксировано завершение каркаса. Эта отметка завершает приведённую хронологию строительных вех.</li>",
         "<li><b>Апрель 2026 года.</b> В строительной записи зафиксировано завершение каркаса.</li><li class=\"is-now\"><b>Октябрь 2026 года.</b> Объявлено о завершении строительства башен. По публикациям того месяца, " + RU + ".</li>"),
        ("<p>Опубликованные оценки заселения охватывают период с 2026 по 2028 год; официальная дата получения Формы 4 не опубликована.",
         "<p>По публикациям октября 2026 года, когда было объявлено о завершении строительства башен, " + RU + "; официальная дата получения Формы 4 не опубликована."),
    ]),
    "ar": (8118, "hamedina-ar", "76c204ec12ee9cafaedd1ce9f4ccd02d", [
        ("سُجّل اكتمال الهيكل في 23.4.2026، فيما تتراوح تقديرات السكن بين 2026 و2028.",
         "سُجّل اكتمال الهيكل في 23.4.2026، وأُعلن عن اكتمال بناء الأبراج في تشرين الأول 2026؛ ووفق منشورات ذلك الشهر " + AR + "."),
        ("<td>اكتمال الهيكل، في تحديث مؤرخ في 23.4.2026.</td>",
         "<td>اكتمال الهيكل في 23.4.2026، والإعلان عن اكتمال بناء الأبراج في تشرين الأول 2026.</td>"),
        ("<td>من 2026 إلى 2028؛ موعد رسمي للإشغال باستمارة 4 غير منشور",
         "<td>وفق منشورات تشرين الأول 2026، " + AR + "؛ موعد رسمي للإشغال باستمارة 4 غير منشور"),
        ("<p>تتراوح تقديرات الإشغال المنشورة بين 2026 و2028، ولا يوجد موعد رسمي منشور لاستمارة 4.",
         "<p>حتى تشرين الثاني 2026: أُعلن في تشرين الأول 2026 عن اكتمال بناء الأبراج، ووفق منشورات ذلك الشهر " + AR + "، ولا يوجد موعد رسمي منشور لاستمارة 4."),
        ("<p>تتضمن مواعيد جهتي البناء المنشورة تقديراً لعام 2026 وآخر لنيسان 2027.",
         "<p>ذكرت منشورات تشرين الأول 2026، مع اكتمال البناء، ثلاث فترات للتسليم: آذار إلى نيسان 2027، ونيسان إلى أيار 2027، والربع الأول من 2027. وقبل ذلك تضمنت مواعيد جهتي البناء المنشورة تقديراً لعام 2026 وآخر لنيسان 2027."),
        ("<li class=\"is-now\"><b>4.2026</b> سُجّلت مرحلة اكتمال الهيكل، وهي المرحلة التي يستند إليها وصف تقدم الموقع، مع بقاء موعد الإشغال الرسمي منفصلاً عنها.</li>",
         "<li><b>4.2026</b> سُجّلت مرحلة اكتمال الهيكل، وهي المرحلة التي يستند إليها وصف تقدم الموقع، مع بقاء موعد الإشغال الرسمي منفصلاً عنها.</li>"
         "<li class=\"is-now\"><b>10.2026</b> أُعلن عن اكتمال بناء الأبراج. ووفق منشورات ذلك الشهر " + AR + ".</li>"),
        ("<p>تتراوح تقديرات الإشغال المنشورة بين 2026 و2028، ولم يُنشر موعد رسمي لاستمارة 4.",
         "<p>وفق منشورات تشرين الأول 2026، مع الإعلان عن اكتمال بناء الأبراج، " + AR + "، ولم يُنشر موعد رسمي لاستمارة 4."),
    ]),
}
def _fr(s):  # the French article's typography: a no-break space before ; and : and inside « »
    return s.replace(" ;", "\xa0;").replace(" :", "\xa0:").replace("« ", "«\xa0").replace(" »", "\xa0»")


POSTS["fr"] = POSTS["fr"][:3] + ([(_fr(a), _fr(b)) for a, b in POSTS["fr"][3]],)
OLD_WINDOW = ["2026 ל-2028", "2026 עד 2028", "2026 to 2028", "de 2026 à 2028", "с 2026 по 2028", "بين 2026 و2028", "من 2026 إلى 2028"]


def apply(raw, swaps):
    for old, new in swaps:
        c = raw.count(old)
        if c != 1:
            raise SystemExit("anchor x%d: %s" % (c, old[:90]))
        raw = raw.replace(old, new)
    left = [w for w in OLD_WINDOW if w in raw]
    if left:
        raise SystemExit("the old window is still in the text: %s" % left)
    return raw


plan = {}
for lang in ONLY:
    pid, slug, pin, swaps = POSTS[lang]
    s, g, _ = req("GET", "/wp-json/wp/v2/nadlan_project/%d?context=edit&_fields=id,slug,modified,content" % pid)
    assert s == 200 and g["slug"] == slug, (lang, s, g.get("slug"))
    raw = g["content"]["raw"]
    now = hashlib.md5(raw.encode("utf-8")).hexdigest()
    if now != pin:
        raise SystemExit("%s: the live post changed since it was read (%s, modified %s): read it again before replacing anything" % (lang, now[:10], g["modified"]))
    new = apply(raw, swaps)
    plan[lang] = (pid, raw, new, now)
    print("[plan] %s post %d: %d replacements; %d -> %d chars" % (lang, pid, len(swaps), len(raw), len(new)))
if not GO:
    sys.exit(0)
bk = os.path.join(REPO, "docs", "qa", "had-709"); os.makedirs(bk, exist_ok=True)
stamp = time.strftime("%Y%m%dT%H%M%S")
res = {}
for lang, (pid, raw, new, now) in plan.items():
    io.open(os.path.join(bk, "backup-%d-%s.html" % (pid, stamp)), "w", encoding="utf-8", newline="").write(raw)
    s1, r1, _ = req("POST", "/wp-json/wp/v2/nadlan_project/%d" % pid, {"content": new})
    assert s1 in (200, 201), (lang, s1, str(r1)[:300])
    s, r, _ = req("GET", "/wp-json/wp/v2/nadlan_project/%d?context=edit&_fields=content,modified" % pid)
    ok = r["content"]["raw"] == new
    res[lang] = {"post": pid, "before_md5": now, "after_md5": hashlib.md5(r["content"]["raw"].encode("utf-8")).hexdigest(), "read_back_equal": ok, "modified": r.get("modified")}
    if not ok:  # put the old text back and stop
        sb, _, _ = req("POST", "/wp-json/wp/v2/nadlan_project/%d" % pid, {"content": raw})
        json.dump(res, open(os.path.join(bk, "result-%s.json" % stamp), "w", encoding="utf-8"), indent=1)
        raise SystemExit("%s: read-back differs: restored the backup (http %s)" % (lang, sb))
    print("[done] %s post %d written and read back" % (lang, pid))
json.dump({"stamp": stamp, "posts": res}, open(os.path.join(bk, "result-%s.json" % stamp), "w", encoding="utf-8"), indent=1)
print("[done] backups and result in docs/qa/had-709/ (%s)" % stamp)
