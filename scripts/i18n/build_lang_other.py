# -*- coding: utf-8 -*-
"""LanguageOther (28.9.2026): the ADDITIONAL dictionary for the 89 language pages that are not a project's page
(the language homes /en/ /fr/ /ru/ /ar/, /xx/guides/..., /xx/new-projects/, /xx/brokers/..., the estimator...).
Measured that day (docs/i18n/lang-other.json): 309 Hebrew text nodes the project dictionary (lang-pages.json) does not
know: city names inside translated lines ("Projects in ירושלים"), profession labels, the market band's caption, the
magazine band's headlines, the footer lines the language homes half-translate, and a lot of guide text that keeps its
Hebrew terms on purpose.

Same format and lookup as scripts/i18n/build_lang_pages.py (read by inc/lang-pages.php, nadlan_lp_tr):
  exact     a whole text node or attribute, trimmed
  patterns  a text node with numbers inside it; {1}.. are the captures, a capture that is a known name or exact is
            translated, a capture still in Hebrew leaves the whole line as it was
  names     cities, neighbourhoods, projects, bodies; also replaced inside a longer line when no Hebrew is left after
Arrows: Hebrew's "←" means "go on"; left-to-right pages get "→", Arabic keeps "←". Units: מ״ר = m², ₪ stays.

Three things this file adds on top of the plain lists:
  1. Russian "in <city>": the homes print "Проекты в " + the Hebrew city; a name alone would give "Проекты в Иерусалим"
     (wrong case), so every Russian prefix x city is an exact line with the locative ("Проекты в Иерусалиме").
  2. Twins: on the language homes inc/i18n.php (nadlan_i18n_theme_map) runs strtr over the whole page, so a line that
     holds one of its words comes out half done ("Projects, דירות, אזורים וכלי בדיקה", "קונים דירה מContractor ב-2026?").
     The map is read from i18n.php and every exact key (lang-pages.json and this file) gets its rewritten twin.
  3. The check: the same lookup order as the PHP over the 309 measured strings, per language, with the reason for each
     string left in Hebrew. Strings kept in Hebrew ON PURPOSE are guarded (the build fails if a later name swallows them).

Left on purpose (never added): listing titles and descriptions (the broker's words), guide/article bodies (their Hebrew
terms sit in <code> or link to the Hebrew page on purpose), the broker form's Hebrew example and the Hebrew title choice,
and the language switcher's "עברית".

Writes plugins/nadlan-config/i18n/lang-other.json.   python scripts/i18n/build_lang_other.py [--samples N]
"""
import io, json, os, re, sys

REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT = os.path.join(REPO, "plugins", "nadlan-config", "i18n", "lang-other.json")
LP = os.path.join(REPO, "plugins", "nadlan-config", "i18n", "lang-pages.json")
STAGE = os.path.join(REPO, "plugins", "nadlan-config", "i18n", "stage-dict.json")
I18N_PHP = os.path.join(REPO, "plugins", "nadlan-config", "inc", "i18n.php")
INPUT = os.path.join(REPO, "docs", "i18n", "lang-other.json")
L = ("en", "fr", "ru", "ar")
HE = re.compile(r"[֐-׿]")


def row(he, en, fr, ru, ar):
    return he, {"en": en, "fr": fr, "ru": ru, "ar": ar}


# ---------------------------------------------------------------------------------------------------------------- exact
EXACT = [
    # professions: the pros strip on the language homes (links to /professionals/?profession=...) and the pros' cards
    row("מפקח בנייה", "Construction supervisor", "Superviseur de chantier", "Строительный инспектор", "مشرف بناء"),
    row("מתווך", "Real-estate broker", "Agent immobilier", "Риелтор", "وسيط عقاري"),
    row("מתווכת", "Real-estate broker", "Agente immobilière", "Риелтор", "وسيطة عقارية"),
    row("מעצב/ת פנים", "Interior designer", "Architecte d'intérieur", "Дизайнер интерьера", "مصمم/ة ديكور داخلي"),
    row("מעצב פנים", "Interior designer", "Architecte d'intérieur", "Дизайнер интерьера", "مصمم ديكور داخلي"),
    row("מעצבת פנים", "Interior designer", "Architecte d'intérieur", "Дизайнер интерьера", "مصممة ديكور داخلي"),
    row("מהנדס/ת בניין", "Building engineer", "Ingénieur en bâtiment", "Инженер-строитель", "مهندس/ة بناء"),
    row("מהנדס בניין", "Building engineer", "Ingénieur en bâtiment", "Инженер-строитель", "مهندس بناء"),
    row("עו״ד מקרקעין", "Property lawyer", "Avocat en immobilier", "Юрист по недвижимости", "محامي عقارات"),
    row('עו"ד מקרקעין', "Property lawyer", "Avocat en immobilier", "Юрист по недвижимости", "محامي عقارات"),
    row("שמאי מקרקעין", "Property appraiser", "Expert immobilier", "Оценщик недвижимости", "مثمّن عقاري"),
    row("יועץ משכנתאות", "Mortgage adviser", "Conseiller en crédit immobilier", "Ипотечный консультант", "مستشار رهن عقاري"),
    row("רו״ח מיסוי נדל״ן", "Real-estate tax accountant", "Expert-comptable en fiscalité immobilière", "Бухгалтер по налогам на недвижимость", "محاسب ضرائب عقارية"),
    row('רו"ח מיסוי נדל"ן', "Real-estate tax accountant", "Expert-comptable en fiscalité immobilière", "Бухгалтер по налогам на недвижимость", "محاسب ضرائب عقارية"),
    row("בדק בית", "Home inspection", "Inspection du logement", "Осмотр жилья", "فحص المنزل"),
    row("אדריכל", "Architect", "Architecte", "Архитектор", "مهندس معماري"),
    # the market band on the language homes (the CBS bars): the source line around the link
    row("· מתעדכן רבעונית", "· Updated quarterly", "· Mise à jour trimestrielle", "· Обновляется ежеквартально", "· يُحدَّث كل ربع سنة"),
    row("מתעדכן רבעונית", "Updated quarterly", "Mise à jour trimestrielle", "Обновляется ежеквартально", "يُحدَّث كل ربع سنة"),
    # the video band on the language homes: its caption and its aria-label; the all-links block's aria-label
    row("ככה בוחרים דירה בנדלן", "This is how you choose an apartment on NadLan", "Voici comment choisir un appartement avec NadLan", "Вот как выбирают квартиру на NadLan", "هكذا تختارون شقة مع NadLan"),
    row("סיור תלת ממדי וסרטון היכרות", "3D tour and introduction video", "Visite 3D et vidéo de présentation", "3D-тур и вводное видео", "جولة ثلاثية الأبعاد وفيديو تعريفي"),
    row("כל הקישורים", "All links", "Tous les liens", "Все ссылки", "كل الروابط"),
    # the magazine band on the language homes: headlines of the site's own articles (the cards link to the Hebrew article)
    row("דירת 3 חדרים ב-690 אלף שקל: המספרים המלאים מאחורי הדירות הזולות בישראל 2026",
        "A 3-room apartment for 690 thousand shekels: the full numbers behind Israel's cheapest apartments in 2026",
        "Un 3 pièces à 690 mille shekels : tous les chiffres derrière les logements les moins chers d'Israël en 2026",
        "3-комнатная квартира за 690 тысяч шекелей: все цифры о самых дешёвых квартирах Израиля в 2026 году",
        "شقة من 3 غرف بـ690 ألف شيكل: الأرقام الكاملة وراء أرخص الشقق في إسرائيل 2026"),
    row("קונים דירה מקבלן ב-2026? כללי המשא ומתן השתנו לטובתכם",
        "Buying an apartment from a developer in 2026? The negotiation rules have changed in your favour",
        "Acheter un logement auprès d'un promoteur en 2026 ? Les règles de la négociation ont changé en votre faveur",
        "Покупаете квартиру у застройщика в 2026 году? Правила переговоров изменились в вашу пользу",
        "تشترون شقة من مطوّر في 2026؟ قواعد التفاوض تغيّرت لصالحكم"),
    row("הקו הירוק בירושלים נפתח ב-2026: איפה זה פוגש את מחירי הדירות",
        "Jerusalem's Green Line opens in 2026: where it meets apartment prices",
        "La ligne verte de Jérusalem ouvre en 2026 : là où elle rencontre les prix des logements",
        "Зелёная линия в Иерусалиме открывается в 2026 году: где она встречается с ценами на квартиры",
        "الخط الأخضر في القدس يُفتتح في 2026: أين يلتقي بأسعار الشقق"),
    row("עיצוב פנים 2026: הצבעים, החומרים והטרנדים שנכנסים לדירות החדשות",
        "Interior design 2026: the colours, materials and trends coming into new apartments",
        "Design d'intérieur 2026 : les couleurs, les matériaux et les tendances qui entrent dans les logements neufs",
        "Дизайн интерьера 2026: цвета, материалы и тренды, которые приходят в новые квартиры",
        "التصميم الداخلي 2026: الألوان والمواد والصيحات التي تدخل الشقق الجديدة"),
    row('תמ"א 38 פוקעת במאי 2026: מה עושים דיירים ויזמים עכשיו',
        "TAMA 38 expires in May 2026: what residents and developers do now",
        "La TAMA 38 expire en mai 2026 : ce que font maintenant les résidents et les promoteurs",
        "ТАМА 38 истекает в мае 2026 года: что делать жильцам и застройщикам сейчас",
        "تاما 38 تنتهي في أيار 2026: ماذا يفعل السكان والمطوّرون الآن"),
    row("תמ״א 38 פוקעת במאי 2026: מה עושים דיירים ויזמים עכשיו",
        "TAMA 38 expires in May 2026: what residents and developers do now",
        "La TAMA 38 expire en mai 2026 : ce que font maintenant les résidents et les promoteurs",
        "ТАМА 38 истекает в мае 2026 года: что делать жильцам и застройщикам сейчас",
        "تاما 38 تنتهي في أيار 2026: ماذا يفعل السكان والمطوّرون الآن"),
    # the project cards' illustrations on the language homes (image alt, the site's own media text)
    row("איור אדריכלי של מגדל ריינבו תל אביב עם מרפסות גליות ותגי מתקנים, הדמיה להמחשה",
        "Architectural illustration of the Rainbow Tel Aviv tower with wavy balconies and facility tags, an illustrative rendering",
        "Illustration architecturale de la tour Rainbow Tel Aviv, balcons ondulés et étiquettes des équipements, image d'illustration",
        "Архитектурная иллюстрация башни Rainbow Tel Aviv с волнистыми балконами и метками удобств, визуализация для наглядности",
        "رسم معماري لبرج Rainbow Tel Aviv بشرفاته المتموجة وعلامات المرافق، تصوير توضيحي"),
    row("איור אדריכלי של פרויקט דמרי ימה שדה דב, מגדל טורי לבן ותגי מתקנים, הדמיה להמחשה",
        "Architectural illustration of the DIMRI YAMA Sde Dov project, a white tower of vertical lines and facility tags, an illustrative rendering",
        "Illustration architecturale du projet DIMRI YAMA Sde Dov, une tour blanche aux lignes verticales et les étiquettes des équipements, image d'illustration",
        "Архитектурная иллюстрация проекта DIMRI YAMA Сде-Дов: белая башня с вертикальными линиями и метки удобств, визуализация для наглядности",
        "رسم معماري لمشروع DIMRI YAMA سديه دوف، برج أبيض بخطوط عمودية وعلامات المرافق، تصوير توضيحي"),
    row("איור אדריכלי של פרויקט אשירה שדה דב בקווים מעוגלים ותגי מתקנים, הדמיה להמחשה",
        "Architectural illustration of the ASHIRA Sde Dov project in rounded lines with facility tags, an illustrative rendering",
        "Illustration architecturale du projet ASHIRA Sde Dov aux lignes arrondies, avec les étiquettes des équipements, image d'illustration",
        "Архитектурная иллюстрация проекта ASHIRA Сде-Дов в плавных линиях с метками удобств, визуализация для наглядности",
        "رسم معماري لمشروع ASHIRA سديه دوف بخطوط منحنية وعلامات المرافق، تصوير توضيحي"),
]

# ------------------------------------------------------------------------------------------------------------- patterns
# {1}.. = the captures; numbers are captured as printed and never reformatted
PATTERNS = [
    (r"^מחיר ממוצע לדירה בשוק החופשי · רבעון (\d+), (\d{4})$",
     "Average apartment price on the open market · Q{1} {2}",
     "Prix moyen d'un logement sur le marché libre · T{1} {2}",
     "Средняя цена квартиры на свободном рынке · {1}-й квартал {2}",
     "متوسط سعر الشقة في السوق الحرة · الربع {1}، {2}"),
    (r"^שינוי מדד מחירי הדירות בשנה האחרונה: ([+\-−]?[\d.,]+%) · המקור:$",
     "Change in the home price index over the last year: {1} · Source:",
     "Variation de l'indice des prix des logements sur un an : {1} · Source :",
     "Изменение индекса цен на жильё за последний год: {1} · Источник:",
     "تغيّر مؤشر أسعار الشقق في السنة الأخيرة: {1} · المصدر:"),
]

# ---------------------------------------------------------------------------------------------------------------- names
# places: he, en, fr, ru, ru "in <place>" (the locative, or "в районе" for a neighbourhood/compound), ar.
# The first three are already names in lang-pages.json (same words, asserted) and are here only for the Russian lines.
# פלורנטין is deliberately NOT a name: the broker form's hint shows Hebrew examples on purpose (guarded below).
PLACES = [
    ("תל אביב יפו", "Tel Aviv-Yafo", "Tel Aviv-Jaffa", "Тель-Авив-Яффо", "в Тель-Авиве-Яффо", "تل أبيب يافا"),
    ("תל אביב-יפו", "Tel Aviv-Yafo", "Tel Aviv-Jaffa", "Тель-Авив-Яффо", "в Тель-Авиве-Яффо", "تل أبيب يافا"),
    ("בני ברק", "Bnei Brak", "Bnei Brak", "Бней-Брак", "в Бней-Браке", "بني براك"),
    # cities
    ("תל אביב", "Tel Aviv", "Tel Aviv", "Тель-Авив", "в Тель-Авиве", "تل أبيب"),
    ("ירושלים", "Jerusalem", "Jérusalem", "Иерусалим", "в Иерусалиме", "القدس"),
    ("רמת גן", "Ramat Gan", "Ramat Gan", "Рамат-Ган", "в Рамат-Гане", "رمات غان"),
    ("חיפה", "Haifa", "Haïfa", "Хайфа", "в Хайфе", "حيفا"),
    ("נתניה", "Netanya", "Netanya", "Нетания", "в Нетании", "نتانيا"),
    ("בת ים", "Bat Yam", "Bat Yam", "Бат-Ям", "в Бат-Яме", "بات يام"),
    ("פתח תקוה", "Petah Tikva", "Petah Tikva", "Петах-Тиква", "в Петах-Тикве", "بيتح تكفا"),
    ("פתח תקווה", "Petah Tikva", "Petah Tikva", "Петах-Тиква", "в Петах-Тикве", "بيتح تكفا"),
    ("הרצליה", "Herzliya", "Herzliya", "Герцлия", "в Герцлии", "هرتسليا"),
    ("חולון", "Holon", "Holon", "Холон", "в Холоне", "حولون"),
    ("גבעתיים", "Givatayim", "Givatayim", "Гиватаим", "в Гиватаиме", "غفعتايم"),
    ("גבעתים", "Givatayim", "Givatayim", "Гиватаим", "в Гиватаиме", "غفعتايم"),
    ("באר שבע", "Beersheba", "Beer-Sheva", "Беэр-Шева", "в Беэр-Шеве", "بئر السبع"),
    ("אופקים", "Ofakim", "Ofakim", "Офаким", "в Офакиме", "أوفاكيم"),
    ("חדרה", "Hadera", "Hadera", "Хадера", "в Хадере", "الخضيرة"),
    ("ראשון לציון", "Rishon LeZion", "Rishon LeZion", "Ришон-ле-Цион", "в Ришон-ле-Ционе", "ريشون لتسيون"),
    ("אשדוד", "Ashdod", "Ashdod", "Ашдод", "в Ашдоде", "أسدود"),
    ("אשקלון", "Ashkelon", "Ashkelon", "Ашкелон", "в Ашкелоне", "عسقلان"),
    ("רחובות", "Rehovot", "Rehovot", "Реховот", "в Реховоте", "رحوفوت"),
    ("רעננה", "Ra'anana", "Ra'anana", "Раанана", "в Раанане", "رعنانا"),
    ("כפר סבא", "Kfar Saba", "Kfar Saba", "Кфар-Саба", "в Кфар-Сабе", "كفار سابا"),
    ("הוד השרון", "Hod HaSharon", "Hod HaSharon", "Ход-ха-Шарон", "в Ход-ха-Шароне", "هود هشارون"),
    ("מודיעין", "Modi'in", "Modiin", "Модиин", "в Модиине", "موديعين"),
    ("ראש העין", "Rosh HaAyin", "Rosh HaAyin", "Рош-ха-Аин", "в Рош-ха-Аине", "روش هعاين"),
    ("נס ציונה", "Ness Ziona", "Ness Ziona", "Нес-Циона", "в Нес-Ционе", "نيس تسيونا"),
    ("נהריה", "Nahariya", "Nahariya", "Нагария", "в Нагарии", "نهاريا"),
    ("אילת", "Eilat", "Eilat", "Эйлат", "в Эйлате", "إيلات"),
    # neighbourhoods and compounds (the listings' "city" field prints some of them)
    ("הרצליה פיתוח", "Herzliya Pituah", "Herzliya Pituah", "Герцлия-Питуах", "в Герцлии-Питуах", "هرتسليا بيتوح"),
    ("רמת אביב", "Ramat Aviv", "Ramat Aviv", "Рамат-Авив", "в Рамат-Авиве", "رمات أفيف"),
    ("נווה צדק", "Neve Tzedek", "Neve Tzedek", "Неве-Цедек", "в районе Неве-Цедек", "نفيه تسيدك"),
    ("יפו", "Jaffa", "Jaffa", "Яффо", "в Яффо", "يافا"),
    ("צוקי אביב", "Tzukei Aviv", "Tzukei Aviv", "Цукей-Авив", "в районе Цукей-Авив", "تسوكي أفيف"),
    ("נופי ים", "Nofei Yam", "Nofei Yam", "Нофей-Ям", "в районе Нофей-Ям", "نوفي يام"),
    ("שרונה", "Sarona", "Sarona", "Сарона", "в районе Сарона", "سارونا"),
    ("כוכב הצפון", "Kochav HaTzafon", "Kochav HaTzafon", "Кохав-ха-Цафон", "в районе Кохав-ха-Цафон", "كوخاف هتسافون"),
    ("שדה דב", "Sde Dov", "Sde Dov", "Сде-Дов", "в районе Сде-Дов", "سديه دوف"),
]

NAMES = [
    # a body the market band links to
    row("הלשכה המרכזית לסטטיסטיקה", "Central Bureau of Statistics", "Bureau central des statistiques", "Центральное статистическое бюро", "دائرة الإحصاء المركزية"),
    # projects' titles in the "leading projects" strip of /xx/new-projects/ (the Latin brand, as lang-pages.json does)
    row("מגדלי DUO תל אביב - פרוייקט דואו אבן גבירול תל אביב", "DUO Tel Aviv", "DUO Tel Aviv", "DUO Tel Aviv", "DUO Tel Aviv"),
    row("ToHa2 תל אביב - משרדים להשכרה מגדל תוהא תל אביב", "ToHa2 Tel Aviv", "ToHa2 Tel Aviv", "ToHa2 Tel Aviv", "ToHa2 Tel Aviv"),
    row("THE PARK - משרדים להשכרה בני ברק ליד רכבת", "THE PARK Bnei Brak", "THE PARK Bnei Brak", "THE PARK Bnei Brak", "THE PARK Bnei Brak"),
    row("H Infinity - מגדל אינפיניטי של קבוצת חג'ג' במתחם סומייל, תל אביב", "H Infinity Tel Aviv", "H Infinity Tel Aviv", "H Infinity Tel Aviv", "H Infinity Tel Aviv"),
]

# the Russian homes print one of these (inc/i18n.php: projects_in, prices_in, apts_in, ls_city_pre) + the Hebrew place
RU_IN = [
    # ru prefix,              en,                         fr,                            ru,                        ar
    ("Проекты в ",             "Projects in {en}",          "Projets à {fr}",              "Проекты {ru_in}",         "مشاريع في {ar}"),
    ("Цены в ",                "Prices in {en}",            "Prix à {fr}",                 "Цены {ru_in}",            "الأسعار في {ar}"),
    ("Квартиры в ",            "Apartments in {en}",        "Appartements à {fr}",         "Квартиры {ru_in}",        "شقق في {ar}"),
    ("Квартиры на продажу в ", "Apartments for sale in {en}", "Appartements à vendre à {fr}", "Квартиры на продажу {ru_in}", "شقق للبيع في {ar}"),
]

# -------------------------------------------------------------------------------------------------- left on purpose
# Hebrew that must STAY Hebrew: guarded, the build fails if the lookup ever translates one of these
KEEP = {
    "In Hebrew, separated by commas. For example: נווה צדק, פלורנטין, יפו": "broker form hint: the field takes Hebrew, the example is Hebrew on purpose",
    "На иврите, через запятую. Например: נווה צדק, פלורנטין, יפו": "broker form hint: the field takes Hebrew, the example is Hebrew on purpose",
    "En hébreu, séparés par des virgules. Par exemple : נווה צדק, פלורנטין, יפו": "broker form hint: the field takes Hebrew, the example is Hebrew on purpose",
    "מתווך (m)": "broker form choice 'Hebrew pages call you': the Hebrew title itself is the answer",
    "מתווכת (f)": "broker form choice 'Hebrew pages call you': the Hebrew title itself is the answer",
    "מתווך (м)": "broker form choice 'Hebrew pages call you': the Hebrew title itself is the answer",
    "מתווכת (ж)": "broker form choice 'Hebrew pages call you': the Hebrew title itself is the answer",
    "עברית": "the language switcher names Hebrew in Hebrew",
}
# content written by people: listing titles and descriptions (the broker's words)
LISTINGS = {
    "אחוזה פרטית של 700 מ״ר על מגרש של 1.1 דונם, הרצליה פיתוח",
    "5 חדרים בקומה גבוהה במתחם עם בריכה, רמת אביב",
    "מיני פנטהאוז של 5 חדרים עם נוף לים, נופי ים",
}
# guide and article bodies: the translated text keeps its Hebrew terms on purpose (<code>, links to the Hebrew page)
GUIDE_URL = re.compile(r"/(?:en|fr|ru|ar)/(?:guides/[a-z0-9-]+/|property-value-estimator/)$")


def left_reason(s, url):
    if s in KEEP:
        return "hebrew-on-purpose"
    if s in LISTINGS:
        return "listing"
    if GUIDE_URL.search(url):
        return "guide-body"
    if url.endswith("/ar/guides/") and "מרחב מוגן דירתי" in s:
        return "guide-body"      # the guides index quotes the mamad guide's opening lines
    if "3ג1" in s:
        return "guide-body"      # /ar/new-projects/ body text: 3ג1 is a statute section number (Sale Law 3C1)
    return None


# -------------------------------------------------------------------------------------------------------------- twins
def theme_maps():
    """inc/i18n.php nadlan_i18n_theme_map: the strtr map the language homes run over the whole page."""
    php = io.open(I18N_PHP, encoding="utf-8").read()
    a = php.index("function nadlan_i18n_theme_map")
    body = php[a:php.index("return isset", a)]
    q = r"""(?:'((?:[^'\\]|\\.)*)'|"((?:[^"\\]|\\.)*)")"""
    maps = {}
    for m in re.finditer(r"'(en|fr|ru|ar)'\s*=>\s*array\((.*?)\)\s*,\s*\n", body, re.S):
        pairs = {}
        for p in re.finditer(q + r"\s*=>\s*" + q, m.group(2)):
            k = p.group(1) if p.group(1) is not None else p.group(2)
            v = p.group(3) if p.group(3) is not None else p.group(4)
            pairs[k.replace("\\'", "'")] = v.replace("\\'", "'")
        maps[m.group(1)] = pairs
    assert set(maps) == set(L) and all(len(v) >= 20 for v in maps.values()), "i18n.php theme map changed shape"
    return maps


def strtr(s, mp):
    """PHP strtr($s, array): longest key first at each position, replaced text is not searched again."""
    if not mp:
        return s
    keys = sorted(mp, key=len, reverse=True)
    return re.sub("|".join(re.escape(k) for k in keys), lambda m: mp[m.group(0)], s)


# ------------------------------------------------------------------------------------------------------------- lookup
class Dict:
    """lang-pages.json + this dictionary, merged the way inc/lang-pages.php merges a second file (the first file wins)."""

    def __init__(self, *docs):
        self.exact, self.names, self.patterns = {}, {}, []
        for d in docs:
            for k, v in d.get("exact", {}).items():
                self.exact.setdefault(k, v)
            for k, v in d.get("names", {}).items():
                self.names.setdefault(k, v)
            self.patterns += d.get("patterns", [])
        self._rx = [(re.compile(p["re"]), p) for p in self.patterns]
        self._nm = {}

    def tr(self, s, lang):
        """inc/lang-pages.php nadlan_lp_tr: exact -> names -> patterns -> known names inside the line."""
        if lang in self.exact.get(s, {}):
            return self.exact[s][lang]
        if lang in self.names.get(s, {}):
            return self.names[s][lang]
        for rx, p in self._rx:
            m = rx.search(s)
            if not m or not p.get(lang):
                continue
            out = p[lang]
            for i in range(len(m.groups()), 0, -1):
                c = m.group(i) or ""
                if lang in self.names.get(c, {}):
                    c = self.names[c][lang]
                elif lang in self.exact.get(c, {}):
                    c = self.exact[c][lang]
                elif HE.search(c):
                    return None
                out = out.replace("{%d}" % i, c)
            return out
        if lang not in self._nm:
            self._nm[lang] = {k: v[lang] for k, v in self.names.items() if lang in v}
        t = strtr(s, self._nm[lang])
        if t != s and not HE.search(t):
            return t
        return None


# -------------------------------------------------------------------------------------------------------------- build
def build():
    lp = json.load(io.open(LP, encoding="utf-8"))
    lp_keys = set(lp["exact"]) | set(lp["names"])
    lp_res = {p["re"] for p in lp["patterns"]}

    def clean(he, tr, where):
        for l in L:
            assert tr.get(l) and not HE.search(tr[l]), (where, he, l)
            assert "←" not in tr[l] or l == "ar", (where, he, l, "a left-to-right line points →")
            assert "→" not in tr[l] or l != "ar", (where, he, l, "Arabic keeps ←")

    ex, names = {}, {}
    for he, tr in EXACT:
        assert he not in ex and he not in lp_keys, ("duplicate exact", he)
        clean(he, tr, "exact")
        ex[he] = tr
    for he, tr in NAMES:
        assert he not in names and he not in ex and he not in lp_keys, ("duplicate name", he)
        clean(he, tr, "names")
        names[he] = tr
    for he, en, fr, ru, ru_in, ar in PLACES:
        tr = {"en": en, "fr": fr, "ru": ru, "ar": ar}
        if he in lp["names"]:
            assert lp["names"][he] == tr, ("a place differs from lang-pages.json", he)
            continue
        assert he not in names and he not in ex and he not in lp_keys, ("duplicate place", he)
        clean(he, tr, "places")
        names[he] = tr
    # 1. the Russian "in <place>" lines
    for pre, t_en, t_fr, t_ru, t_ar in RU_IN:
        for he, en, fr, ru, ru_in, ar in PLACES:
            key = pre + he
            assert key not in ex and key not in lp_keys, ("duplicate", key)
            v = {"en": en, "fr": fr, "ru": ru, "ru_in": ru_in, "ar": ar}
            tr = {"en": t_en.format(**v), "fr": t_fr.format(**v), "ru": t_ru.format(**v), "ar": t_ar.format(**v)}
            clean(key, tr, "ru-in")
            ex[key] = tr
    n_ru = len(RU_IN) * len(PLACES)
    # 2. the twins the language homes' strtr makes of every exact line (lang-pages.json's and this file's)
    maps, twins = theme_maps(), {}
    for he, tr in list(lp["exact"].items()) + list(ex.items()):
        for l in L:
            t = strtr(he, maps[l])
            if t == he or not HE.search(t) or t in lp_keys or t in ex or t in names:
                continue
            assert twins.get(t, tr) == tr, ("two lines give the same twin", t)
            twins[t] = tr
    ex.update(twins)
    # patterns
    pats = []
    for p in PATTERNS:
        assert p[0] not in lp_res, ("pattern already in lang-pages.json", p[0])
        n = re.compile(p[0]).groups
        tr = dict(zip(L, p[1:]))
        for l in L:
            for k in range(1, n + 1):
                assert "{%d}" % k in tr[l], (p[0], l, k)
            assert not re.search(r"\{%d\}" % (n + 1), tr[l]), (p[0], l, "a placeholder with no capture")
        clean(p[0], tr, "patterns")
        pats.append({"re": p[0], **tr})
    doc = {"note": "LanguageOther (28.9.2026): the words outside the article on the non-project language pages (the language homes, guides, new-projects, brokers). Built by scripts/i18n/build_lang_other.py; an addition to lang-pages.json for inc/lang-pages.php. Keys are the exact Hebrew the site prints, including the half-translated twins the language homes print.",
           "exact": ex, "patterns": pats, "names": names}
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    io.open(OUT, "w", encoding="utf-8", newline="\n").write(json.dumps(doc, ensure_ascii=False, indent=1) + "\n")
    print("ok", len(ex), "exact (%d Russian 'in <place>' lines, %d twins of the homes' strtr)," % (n_ru, len(twins)),
          len(pats), "patterns,", len(names), "names ->", os.path.relpath(OUT, REPO))
    return lp, doc


# -------------------------------------------------------------------------------------------------------------- check
# attributes the harvest (text nodes only) did not list, seen in the raw HTML of the language homes on 28.9.2026
EXTRA_SEEN = [
    ("סיור תלת ממדי וסרטון היכרות", "https://nad-lan.co.il/ar/"),
    ("כל הקישורים", "https://nad-lan.co.il/ar/"),
    ("איור معماريי של מגדל ריינבו תל אביב עם מרפסות גליות ותגי מתקנים, הדמיה להמחשה", "https://nad-lan.co.il/ar/"),
    ("איור Architectי של פרויקט דמרי ימה שדה דב, מגדל טורי לבן ותגי מתקנים, הדמיה להמחשה", "https://nad-lan.co.il/en/"),
    ("איור Architecteי של פרויקט אשירה שדה דב בקווים מעוגלים ותגי מתקנים, הדמיה להמחשה", "https://nad-lan.co.il/fr/"),
    ("איור Архитекторי של מגדל ריינבו תל אביב עם מרפסות גליות ותגי מתקנים, הדמיה להמחשה", "https://nad-lan.co.il/ru/"),
    ("עברית", "https://nad-lan.co.il/en/"),
]


def page_lang(url):
    m = re.match(r"https?://[^/]+/(en|fr|ru|ar)/", url)
    return m.group(1) if m else "?"


def check(lp, doc, samples=0):
    strings = json.load(io.open(INPUT, encoding="utf-8"))["strings"]
    d = Dict(lp, doc)
    bad = []
    # the guard: Hebrew on purpose stays Hebrew in every language
    for s in KEEP:
        for l in L:
            if d.tr(s, l) is not None:
                bad.append("KEEP translated (%s): %r -> %r" % (l, s, d.tr(s, l)))
    print("\ncheck: %d measured strings (docs/i18n/lang-other.json), lookup = lang-pages.json + lang-other.json" % len(strings))
    rows = []
    for s, url in strings.items():
        res = {l: d.tr(s, l) for l in L}
        rows.append((s, url, page_lang(url), res, left_reason(s, url)))
    def left_of(rs, l):
        left = {}
        for r in rs:
            if r[3][l] is None:
                left[r[4] or "MISSING"] = left.get(r[4] or "MISSING", 0) + 1
        return ", ".join("%s %d" % kv for kv in sorted(left.items())) or "none"

    for l in L:
        ok = sum(1 for r in rows if r[3][l] is not None)
        nat = [r for r in rows if r[2] == l]
        nat_ok = sum(1 for r in nat if r[3][l] is not None)
        print("  %s: all %d strings: translated %d (%.0f%%), left %s | first seen on a /%s/ page: %d, translated %d, left %s" % (
            l, len(rows), ok, 100.0 * ok / len(rows), left_of(rows, l), l, len(nat), nat_ok, left_of(nat, l)))
    missing = [r for r in rows if r[4] is None and r[3][r[2]] is None]
    for s, url, pl, res, why in missing:
        bad.append("MISSING (%s) %r  %s" % (pl, s, url))
    # translated although the page keeps the word in Hebrew on purpose (a guide's <code> term): the pass must skip there
    for s, url, pl, res, why in rows:
        if why == "guide-body" and res[pl] is not None:
            print("  NOTE: %r is a label elsewhere but a Hebrew term in the guide body of %s -> the pass must skip the guide body" % (s, url))
    by = {}
    for r in rows:
        if r[3][r[2]] is None:
            by.setdefault(r[4] or "MISSING", []).append(r)
    for why in sorted(by):
        print("  left on its own page, %s: %d" % (why, len(by[why])))
    print("  attributes the harvest missed:")
    for s, url in EXTRA_SEEN:
        pl = page_lang(url)
        t = d.tr(s, pl)
        print("    %s %s -> %s" % (pl, s[:60], t[:60] if t else "(stays: %s)" % KEEP.get(s, "MISSING")))
        if t is None and s not in KEEP:
            bad.append("MISSING attribute (%s) %r" % (pl, s))
    if os.path.exists(STAGE):   # read only: the stage dictionary is another builder's
        st = json.load(io.open(STAGE, encoding="utf-8"))
        both = [k for k in doc["exact"] if k in st.get("exact", {})] + [k for k in doc["names"] if k in st.get("names", {})]
        diff = [k for k in both if (st.get("exact", {}).get(k) or st.get("names", {}).get(k)) != (doc["exact"].get(k) or doc["names"].get(k))]
        print("  stage-dict.json overlap: %d keys, %d with other words%s" % (len(both), len(diff), (": " + ", ".join(diff[:8])) if diff else ""))
    if samples:
        for l in L:
            print("\n  samples %s:" % l)
            n, seen = 0, set()
            for s, url, pl, res, why in rows:
                shape = HE.sub("", s)[:10]     # one line per shape ("Projects in " once, not for every city)
                if pl == l and res[l] is not None and n < samples and shape not in seen:
                    seen.add(shape)
                    print("    %s\n      -> %s" % (s, res[l]))
                    n += 1
    if bad:
        print("\nFAILED:")
        for b in bad:
            print("  " + b)
        sys.exit(1)
    print("\ncheck ok: every measured string is translated or left on purpose")


if __name__ == "__main__":
    n = 0
    if "--samples" in sys.argv:
        n = int(sys.argv[sys.argv.index("--samples") + 1])
    lp_doc, out_doc = build()
    check(lp_doc, out_doc, n)
