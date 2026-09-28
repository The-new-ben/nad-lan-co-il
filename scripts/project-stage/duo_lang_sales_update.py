# -*- coding: utf-8 -*-
"""DUO's four language pages with the developer's Q2 2026 figures (28.9.2026; Linear HAD-365), as duo_sales_update.py did
for the Hebrew page. Each page kept Q1 2026 as "the latest official snapshot" (366 contracts, 144 not sold at 31.3.2026);
Africa Israel Residences' Q2 2026 report (https://res.afi-g.com/about/Documents/2026/Q2-2026.pdf, sections 1.3 and 7.13.2)
gives 372 contracts and 138 not sold at 30.6.2026 in the same 510-apartment pool, and about 71K ₪ per m² before VAT in
the contracts of 1-6.2026. One sentence is added after the body's and after the questions' "144 is not current" line;
nothing is removed. Raw content over REST (the app password decrypted in-process, never printed), each anchor exactly once,
md5-guarded, the old raw content saved first.
  python scripts/project-stage/duo_lang_sales_update.py            # show
  python scripts/project-stage/duo_lang_sales_update.py --apply    # write"""
import io, os, sys, hashlib, time
REPO = r"C:\Users\777\nad-lan\nad-lan-co-il"
src = io.open(os.path.join(REPO, "scripts", "project-stage", "rainbow_content4.py"), encoding="utf-8").read()
exec(compile(src[src.index("import base64, ctypes"):src.index("def read():")]
             .replace('QA = os.path.join(REPO, "docs", "qa", "rainbow-content-2026-09-24")', 'QA = os.path.join(REPO, "docs", "qa", "duo-content-2026-09-28")'), "head", "exec"))

ADD = {
    "en": [
        ("Later transactions were reported, so 144 cannot honestly be presented as the number available today.",
         " The company's report for the second quarter of 2026 updates the count: at 30 June 2026, 372 contracts had been signed within the same 510-apartment pool, leaving 138, and contracts signed from January to June 2026 averaged about ₪71,000 per square metre before VAT."),
        ("Later reported transactions mean that 144 is not current availability.",
         " The Q2 2026 report puts the count at 372 contracts and 138 apartments not sold at 30 June 2026."),
    ],
    "fr": [
        ("Il serait également faux de reprendre 144 comme disponibilité actuelle, car des opérations ont été rapportées après la clôture du trimestre.",
         " Le rapport de la société pour le deuxième trimestre 2026 met ce chiffre à jour : au 30 juin 2026, 372 contrats avaient été signés dans le même périmètre de 510, il en restait 138, et les contrats signés de janvier à juin 2026 s'établissaient en moyenne à environ 71 000 ₪ le m² hors TVA."),
        ("Le chiffre de 144 ne doit donc pas être présenté comme le stock actuel.",
         " Selon le rapport du deuxième trimestre 2026, 372 contrats étaient signés et 138 logements restaient non vendus au 30 juin 2026."),
    ],
    "ru": [
        ("Значит, показатель 144 уже не отражает наличие на 4 августа 2026 года.",
         " Отчет компании за второй квартал 2026 года обновляет цифры: на 30 июня 2026 года в том же пуле из 510 квартир было заключено 372 договора, непроданными оставались 138, а средняя цена по договорам января–июня 2026 года составила около 71 000 ₪ за м² без НДС."),
        ("На 31 марта 2026 года отчетность указывала 144 непроданные квартиры в 510-квартирном пуле, но после этой даты сообщалось о новых сделках.",
         " По отчету за второй квартал 2026 года, на 30 июня 2026 года было заключено 372 договора и 138 квартир оставались непроданными."),
    ],
    "ar": [
        ("الصياغة الدقيقة هي أن 144 كان عدد الشقق غير المباعة في تلك المجموعة في 31 مارس 2026، وليس عدد الشقق المتاحة اليوم.",
         " ويحدّث تقرير الشركة للربع الثاني من 2026 هذا الرقم: في 30 يونيو 2026 كانت قد وُقّعت 372 عقدا ضمن مجموعة الـ510 نفسها، وبقيت 138 شقة، وبلغ متوسط العقود الموقعة بين يناير ويونيو 2026 نحو 71,000 ₪ للمتر المربع قبل ضريبة القيمة المضافة."),
        ("في 31 مارس 2026 سجلت الشركة 144 شقة غير مباعة ضمن مجموعة الـ510.",
         " وبحسب تقرير الربع الثاني من 2026، كانت قد وُقّعت 372 عقدا وبقيت 138 شقة غير مباعة في 30 يونيو 2026."),
    ],
}


def read_pid(pid):
    s, d = req("GET", "/wp-json/wp/v2/nadlan_project/%d?context=edit&_fields=id,content" % pid)
    if s != 200:
        raise SystemExit("FATAL read %d: %s" % (pid, s))
    return d["content"]["raw"]


plans = []
for lang, fixes in ADD.items():
    s, d = req("GET", "/wp-json/wp/v2/nadlan_project?slug=duo-tel-aviv-%s&_fields=id" % lang)
    pid = int(d[0]["id"])
    raw = read_pid(pid)
    new = raw
    for a, add in fixes:
        n = new.count(a)
        print("[%s %d] x%d  %s..." % (lang, pid, n, a[:60]))
        if n != 1:
            raise SystemExit("FATAL: anchor not found exactly once")
        new = new.replace(a, a + add)
    plans.append((lang, pid, raw, new))
    print("[plan] %s: %d -> %d chars" % (lang, len(raw), len(new)))
if "--apply" not in sys.argv:
    raise SystemExit(0)
os.makedirs(QA, exist_ok=True)
for lang, pid, raw, new in plans:
    io.open(os.path.join(QA, "duo-%s-%d-before-%s.html" % (lang, pid, time.strftime("%Y%m%dT%H%M%S"))), "w", encoding="utf-8").write(raw)
    if hashlib.md5(read_pid(pid).encode("utf-8")).hexdigest() != hashlib.md5(raw.encode("utf-8")).hexdigest():
        raise SystemExit("FATAL: %s changed while this ran" % lang)
    s, r = req("POST", "/wp-json/wp/v2/nadlan_project/%d" % pid, {"content": new})
    ok = read_pid(pid) == new
    print("[write] %s %d http %s, verified %s" % (lang, pid, s, ok))
