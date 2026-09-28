# -*- coding: utf-8 -*-
"""StageDict (HAD-361, 28.9.2026): the dictionary for the project stage on a project's language page
(/projects/<slug>-en|fr|ru|ar/). The stage, its 360 room, its floor slice and its facility and place cards are drawn in
the browser in Hebrew; assets/project-stage/i18n-dom.js swaps every Hebrew string they show by this dictionary joined to
i18n/lang-pages.json, and inc/lang-pages.php uses the same two files for the stage's server-printed parts.

Same format and rules as scripts/i18n/build_lang_pages.py:
  exact     a whole text node or attribute, trimmed, spaces collapsed
  patterns  a text node with numbers or a place inside it; {1}.. are the captures. A capture that is a known name or
            exact string is translated too; a capture still in Hebrew leaves the whole line in Hebrew (never half)
  names     projects, developers, places and streets; also replaced inside a longer line when nothing Hebrew remains
Lookup order (both runtimes): exact -> names -> the first pattern that matches (lang-pages.json's first, then these) ->
names inside the line. The PHP pass stops at the first pattern that matches, so specific patterns come before general
ones. Every regex must work in three engines: Python re, PCRE with '#' as its delimiter (no '#' in a pattern) and a
JavaScript RegExp with the 'u' flag (no escaping of anything but regex syntax characters).
Arrows: Hebrew's "←" means "go on"; left-to-right pages get "→", Arabic keeps "←". Units: מ׳ = m, ק״מ = km, מ״ר = m²,
דק׳ = min, ₪ stays. Brands stay Latin in every language (Rainbow, DUO, Dimri Yama, Ashira, Israel Canada...).

Left out on purpose (they stay Hebrew-only or are handled elsewhere): the Hebrew lead paragraph, the broker card, the
invitation square, the film button, the deals table; none of them is printed on a language page anyway
(nadlan_ps_current() drops film, deals and the rail there).

  python scripts/i18n/build_stage_dict.py            build plugins/nadlan-config/i18n/stage-dict.json, then check
  python scripts/i18n/build_stage_dict.py --no-check build only
The check replays the lookup on every example in docs/i18n/stage-harvest.json (and on the translatable strings of
docs/i18n/stage-server.json) per language, in Python, in node (the browser's i18n-dom.js logic) and in PHP (the
server's nadlan_lp_tr logic) when those are installed, and lists what stays Hebrew.
"""
import io, json, os, re, shutil, subprocess, sys, tempfile

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT = os.path.join(REPO, "plugins", "nadlan-config", "i18n", "stage-dict.json")
LP = os.path.join(REPO, "plugins", "nadlan-config", "i18n", "lang-pages.json")
HARVEST = os.path.join(REPO, "docs", "i18n", "stage-harvest.json")
SERVER = os.path.join(REPO, "docs", "i18n", "stage-server.json")
L = ("en", "fr", "ru", "ar")
HE = re.compile(r"[֐-׿]")


def row(he, en, fr, ru, ar):
    return he, {"en": en, "fr": fr, "ru": ru, "ar": ar}


# pattern templates: the Hebrew with {N}.. where a capture goes; everything else is taken literally
TOK = {
    "N": r"([\d.,]+)",   # a number: 290, 1.2, 4,004
    "I": r"(\d+)",       # a whole number: a floor, a lot
    "D": r"([\d.]+)",    # a date: 10.5.2023, 8.2026
    "R": r"([\d-]+)",    # a reference: 1-25-0172
    "L": r"([\d, ]+)",   # a list of floors: 10, 25
    "P": r"([\d ,]+)",   # permit numbers: 20240293 ,20261155
    "Q": r"(\d+:\d+)",   # a ratio: 1:1
    "X": r"(.+)",        # a name (greedy)
    "Y": r"(.+?)",       # a name (lazy)
    "F": r"(מ.+?)",      # "from <project>": מריינבו, מ־DUO (lazy)
    "G": r"(מ.+)",       # the same, to the end
}


def esc(s):
    return re.sub(r"([\\^$.*+?()\[\]{}|])", r"\\\1", s)


def rx(t):
    out = []
    for part in re.split(r"(\{[A-Z]\})", t):
        out.append(TOK[part[1]] if re.fullmatch(r"\{[A-Z]\}", part) else esc(part))
    return "^" + "".join(out) + "$"


def pat(t, en, fr, ru, ar):
    return (rx(t), en, fr, ru, ar)


# ---------------------------------------------------------------------------------------------------------------------
# sentences used in more than one place (captions made of parts, notes that also close the facility room's caption)
# ---------------------------------------------------------------------------------------------------------------------
# the 360 room's caption: A + [S] + [B] + [P] (tour.js joins them with a space)
A = row("הדמיית פנים להמחשה בלבד: החלוקה, הגמרים והנוף משוערים ואינם לפי תוכנית מכר.",
        "Interior illustration only: the layout, the finishes and the view are estimates and are not based on a sale plan.",
        "Illustration intérieure uniquement : l'agencement, les finitions et la vue sont estimés et ne reposent pas sur un plan de vente.",
        "Только иллюстрация интерьера: планировка, отделка и вид приблизительны и не основаны на плане продажи.",
        "تصور داخلي توضيحي فقط: التقسيم والتشطيبات والإطلالة تقديرية وليست بحسب مخطط البيع.")
S = row("רעיון עיצוב להמחשה, לא המפרט של היזם.",
        "A design idea for illustration, not the developer's specification.",
        "Une idée de décoration à titre indicatif, pas le descriptif du promoteur.",
        "Идея дизайна для иллюстрации, а не спецификация застройщика.",
        "فكرة تصميم للتوضيح، وليست مواصفات المطوّر.")
B = row("עומק המרפסת בציור להמחשה בלבד: לפי תכנית העיצוב ({D}), מרפסות המגדל בולטות עד {N} מ׳.",
        "The balcony depth in the drawing is an illustration only: per the design plan ({1}), the tower's balconies project up to {2} m.",
        "La profondeur du balcon sur le dessin est purement indicative : selon le plan d'aménagement ({1}), les balcons de la tour avancent jusqu'à {2} m.",
        "Глубина балкона на рисунке условна: по архитектурному плану ({1}) балконы башни выступают не более чем на {2} м.",
        "عمق الشرفة في الرسم للتوضيح فقط: بحسب مخطط التصميم ({1})، تبرز شرفات البرج حتى {2} م.")
P = row("הנפחים השקופים הם פרויקטים מתוכננים ברובע, בגובה לפי מספר הקומות.",
        "The transparent volumes are planned projects in the quarter, with heights by their number of floors.",
        "Les volumes transparents sont des projets prévus dans le quartier, à une hauteur fonction de leur nombre d'étages.",
        "Прозрачные объёмы — проектируемые здания в районе, высотой по числу этажей.",
        "الكتل الشفافة هي مشاريع مخطط لها في الحي، بارتفاع بحسب عدد طوابقها.")
# the facility room's caption: ROOM + " " + the facility's note (bridge.js)
ROOM = row("הדמיה להמחשה בלבד: המיקום, החלוקה והריהוט משוערים ואינם לפי תוכנית היזם.",
           "Illustration only: the location, the layout and the furniture are estimates and are not based on the developer's plan.",
           "Illustration uniquement : l'emplacement, l'agencement et le mobilier sont estimés et ne reposent pas sur le plan du promoteur.",
           "Только иллюстрация: расположение, планировка и мебель приблизительны и не основаны на плане застройщика.",
           "تصور توضيحي فقط: الموقع والتقسيم والأثاث تقديرية وليست بحسب مخطط المطوّر.")
# the stage's caption: CAP1 or CAP2 (+ " " + the stage's geometry line on DUO, Dimri Yama and Ashira)
CAP1 = row("הדמיה להמחשה בלבד, על בסיס מקורות פומביים. אינה תוכנית מכר.",
           "Illustration only, based on public sources. Not a sale plan.",
           "Illustration uniquement, d'après des sources publiques. Ce n'est pas un plan de vente.",
           "Только иллюстрация на основе открытых источников. Не является планом продажи.",
           "تصور توضيحي فقط، استناداً إلى مصادر علنية. ليس مخطط بيع.")
CAP2 = row("הדמיה להמחשה בלבד, על בסיס מקורות פומביים. חלוקת הקומה לדירות היא לדוגמה, ואינה לפי תוכנית מכר.",
           "Illustration only, based on public sources. The division of the floor into apartments is an example and is not based on a sale plan.",
           "Illustration uniquement, d'après des sources publiques. La répartition de l'étage en appartements est un exemple et ne repose pas sur un plan de vente.",
           "Только иллюстрация на основе открытых источников. Деление этажа на квартиры — пример и не основано на плане продажи.",
           "تصور توضيحي فقط، استناداً إلى مصادر علنية. تقسيم الطابق إلى شقق هو مثال وليس بحسب مخطط البيع.")
# the floor slice's note: SLICE (+ " " + the project's line)
SLICE = row("חתך להמחשה: קו החזית והמרפסות לפי הדגם של הבמה; הגרעין והחלוקה לדירות משוערים ואינם תוכנית מכר.",
            "An illustrative section: the facade line and the balconies follow the 3D model; the core and the division into apartments are estimates and are not a sale plan.",
            "Coupe indicative : la ligne de façade et les balcons suivent la maquette 3D ; le noyau et la répartition en appartements sont estimés et ne constituent pas un plan de vente.",
            "Условный разрез: линия фасада и балконы — по 3D-модели; ядро и деление на квартиры приблизительны и не являются планом продажи.",
            "مقطع توضيحي: خط الواجهة والشرفات بحسب النموذج ثلاثي الأبعاد؛ النواة وتقسيم الشقق تقديريان وليسا مخطط بيع.")
SLICE_NOTE = row("בקומה {I} עד {I} דירות, לפי היזם (ביזפורטל, {D}).",
                 "{1} to {2} apartments per floor, per the developer (Bizportal, {3}).",
                 "{1} à {2} appartements par étage, selon le promoteur (Bizportal, {3}).",
                 "От {1} до {2} квартир на этаже, по данным застройщика (Bizportal, {3}).",
                 "من {1} إلى {2} شقق في الطابق، بحسب المطوّر (Bizportal، {3}).")
# the tour card's paragraph (inc/project-stage.php): floors, the facing words, the balcony, the view's sources
TOUR_FACING = ("מול הים, תל ברוך, רמת אביב ומגדלי העיר",
               {"en": "facing the sea, Tel Baruch, Ramat Aviv and the city's towers",
                "fr": "face à la mer, Tel Baruch, Ramat Aviv et les tours de la ville",
                "ru": "с видом на море, Тель-Барух, Рамат-Авив и городские башни",
                "ar": "مقابل البحر وتل باروخ ورمات أفيف وأبراج المدينة"})
TOUR_BAL = (", מהסלון ומהמרפסת",
            {"en": ", from the living room and from the balcony", "fr": ", depuis le salon et depuis le balcon",
             "ru": ", из гостиной и с балкона", "ar": "، من الصالون ومن الشرفة"})
TOUR_SRC = ("הנוף בחלון בנוי מהבניינים הקיימים לפי שכבת המבנים של העירייה, מהפרויקטים המתוכננים ברובע כנפחים שקופים, מקו החוף ומהים.",
            {"en": "The view in the window is built from the existing buildings per the municipality's buildings layer, the quarter's planned projects as transparent volumes, the shoreline and the sea.",
             "fr": "La vue à la fenêtre est construite à partir des immeubles existants selon la couche des bâtiments de la municipalité, des projets prévus dans le quartier en volumes transparents, du littoral et de la mer.",
             "ru": "Вид в окне построен по существующим зданиям из слоя зданий муниципалитета, по проектируемым в районе зданиям в виде прозрачных объёмов, по линии берега и морю.",
             "ar": "الإطلالة في النافذة مبنية من المباني القائمة بحسب طبقة المباني في البلدية، ومن المشاريع المخطط لها في الحي ككتل شفافة، ومن خط الساحل والبحر."})
TOUR_OPEN = {"en": "A living room and open kitchen as handed over, unfurnished, ",
             "fr": "Un salon et une cuisine ouverte comme à la livraison, sans meubles, ",
             "ru": "Гостиная и открытая кухня как при сдаче, без мебели, ",
             "ar": "صالون ومطبخ مفتوح كما عند التسليم، دون أثاث، "}
TOUR_MULTI = {"en": "on floors {1} and {2}", "fr": "aux étages {1} et {2}", "ru": "на этажах {1} и {2}", "ar": "في الطوابق {1} و{2}"}
TOUR_ONE = {"en": "on floor {1}", "fr": "au {1}e étage", "ru": "на {1}-м этаже", "ar": "في الطابق {1}"}
COLON = {"en": ": ", "fr": " : ", "ru": ": ", "ar": ": "}

# ---------------------------------------------------------------------------------------------------------------------
# EXACT: whole strings
# ---------------------------------------------------------------------------------------------------------------------
EXACT = [
    A, S, P, ROOM, CAP1, CAP2, SLICE,
    # --- the stage's own labels (stage.js, bridge.js)
    row("דירה לדוגמה", "Example apartment", "Appartement témoin", "Пример квартиры", "شقة نموذجية"),
    row("לדוגמה", "Example", "Témoin", "Пример", "نموذجية"),
    row("הנוף מהדירה לדוגמה", "The view from the example apartment", "La vue depuis l'appartement témoin", "Вид из квартиры-примера", "الإطلالة من الشقة النموذجية"),
    row("הנוף מהקומה", "The view from the floor", "La vue depuis l'étage", "Вид с этажа", "الإطلالة من الطابق"),
    row("לצד אחר: הקישו על הטבעת", "Another side: tap the ring", "Autre côté : touchez l'anneau", "Другая сторона: нажмите на кольцо", "جهة أخرى: انقروا على الحلقة"),
    row("בחרו דירה לדוגמה בטבעת הקומה", "Choose an example apartment on the floor's ring", "Choisissez un appartement témoin sur l'anneau de l'étage", "Выберите квартиру-пример на кольце этажа", "اختاروا شقة نموذجية على حلقة الطابق"),
    row("להיכנס לדירה · 360°", "Enter the apartment · 360°", "Entrer dans l'appartement · 360°", "Войти в квартиру · 360°", "الدخول إلى الشقة · 360°"),
    row("הנוף והמפה", "The view and the map", "La vue et la carte", "Вид и карта", "الإطلالة والخريطة"),
    row("לעצב את הדירה", "Design the apartment", "Aménager l'appartement", "Оформить квартиру", "صمّموا الشقة"),
    row("לקבלת תוכניות ומחירים", "Get plans and prices", "Recevoir plans et prix", "Получить планировки и цены", "احصلوا على المخططات والأسعار"),
    row("לקבלת פרטים על הקומה", "Get details on this floor", "Recevoir les détails de cet étage", "Узнать подробности об этаже", "احصلوا على تفاصيل الطابق"),
    row("סיור וירטואלי בפרויקט", "Virtual tour of the project", "Visite virtuelle du projet", "Виртуальный тур по проекту", "جولة افتراضية في المشروع"),
    row("בחרו קומה במגדל", "Choose a floor in the tower", "Choisissez un étage de la tour", "Выберите этаж в башне", "اختاروا طابقاً في البرج"),
    row("בחרו מגדל וקומה", "Choose a tower and a floor", "Choisissez une tour et un étage", "Выберите башню и этаж", "اختاروا برجاً وطابقاً"),
    row("בחרו כיוון סביב הקומה", "Choose a direction around the floor", "Choisissez une direction autour de l'étage", "Выберите направление вокруг этажа", "اختاروا اتجاهاً حول الطابق"),
    row("שקיעה", "Sunset", "Coucher de soleil", "Закат", "الغروب"),
    row("צהריים", "Noon", "Midi", "Полдень", "الظهيرة"),
    row("תאורה", "Lighting", "Éclairage", "Освещение", "الإضاءة"),
    row("פונה", "Facing", "Orienté", "Ориентация", "باتجاه"),
    row("צפונה", "north", "nord", "север", "الشمال"),
    row("צפון מזרחה", "north-east", "nord-est", "северо-восток", "الشمال الشرقي"),
    row("מזרחה", "east", "est", "восток", "الشرق"),
    row("דרום מזרחה", "south-east", "sud-est", "юго-восток", "الجنوب الشرقي"),
    row("דרומה", "south", "sud", "юг", "الجنوب"),
    row("דרום מערבה", "south-west", "sud-ouest", "юго-запад", "الجنوب الغربي"),
    row("מערבה", "west", "ouest", "запад", "الغرب"),
    row("צפון מערבה", "north-west", "nord-ouest", "северо-запад", "الشمال الغربي"),
    row("צפון", "North", "Nord", "Север", "شمال"),
    row("מזרח", "East", "Est", "Восток", "شرق"),
    row("דרום", "South", "Sud", "Юг", "جنوب"),
    row("מערב", "West", "Ouest", "Запад", "غرب"),
    row("מגדל צפוני", "North tower", "Tour nord", "Северная башня", "البرج الشمالي"),
    row("מגדל דרומי", "South tower", "Tour sud", "Южная башня", "البرج الجنوبي"),
    row("צפוני", "North", "Nord", "Северная", "الشمالي"),
    row("דרומי", "South", "Sud", "Южная", "الجنوبي"),
    row("המגדל", "The tower", "La tour", "Башня", "البرج"),
    row("המגדלון", "The mid-rise", "La petite tour", "Малая башня", "البرج الصغير"),
    row("מסחר מערבי", "West retail", "Commerces ouest", "Западный торговый корпус", "المتاجر الغربية"),
    row("מסחר צפוני", "North retail", "Commerces nord", "Северный торговый корпус", "المتاجر الشمالية"),
    row("מסחר דרומי", "South retail", "Commerces sud", "Южный торговый корпус", "المتاجر الجنوبية"),
    row("קומות הפנטהאוז", "penthouse floors", "étages des penthouses", "этажи пентхаусов", "طوابق البنتهاوس"),
    row("קומות הפנטהאוז, לפי פרסומי השיווק", "Penthouse floors, per the marketing materials", "Étages des penthouses, selon les supports commerciaux", "Этажи пентхаусов, по маркетинговым материалам", "طوابق البنتهاوس، بحسب المواد التسويقية"),
    row("הדמיה של פרויקט ריינבו תל אביב, מגדל ובנייני בוטיק סביב גינה",
        "Illustration of the Rainbow Tel Aviv project: a tower and boutique buildings around a garden",
        "Illustration du projet Rainbow Tel Aviv : une tour et des immeubles boutique autour d'un jardin",
        "Иллюстрация проекта Rainbow Tel Aviv: башня и бутик-дома вокруг сада",
        "تصور لمشروع Rainbow Tel Aviv: برج ومبانٍ بوتيك حول حديقة"),
    row("הדמיה של פרויקט DUO תל אביב: שני מגדלי מגורים ומתחם מסחר, בין אבן גבירול, ארלוזורוב ובן סרוק",
        "Illustration of the DUO Tel Aviv project: two residential towers and a retail complex, between Ibn Gabirol, Arlozorov and Ben Saruk",
        "Illustration du projet DUO Tel Aviv : deux tours résidentielles et un complexe commercial, entre Ibn Gabirol, Arlozorov et Ben Saruk",
        "Иллюстрация проекта DUO Tel Aviv: две жилые башни и торговый комплекс между улицами Ибн Гвироль, Арлозоров и Бен-Сарук",
        "تصور لمشروع DUO Tel Aviv: برجا سكن ومجمّع تجاري، بين ابن جبيرول وأرلوزوروف وبن ساروك"),
    row("הדמיה של מגדלי דואו תל אביב: שני מגדלי מגורים, מבנה הלובי ביניהם ומבני המסחר במתחם",
        "Illustration of DUO Tel Aviv: two residential towers, the lobby building between them and the complex's retail buildings",
        "Illustration de DUO Tel Aviv : deux tours résidentielles, le bâtiment du hall entre elles et les bâtiments commerciaux de l'ensemble",
        "Иллюстрация DUO Tel Aviv: две жилые башни, здание лобби между ними и торговые корпуса комплекса",
        "تصور لـ DUO Tel Aviv: برجا سكن ومبنى الردهة بينهما ومباني المتاجر في المجمّع"),
    # the stage's geometry lines (they follow CAP1/CAP2 on DUO, Dimri Yama and Ashira)
    row("המגרש וקווי המגדלים לפי עיריית תל אביב-יפו; הגבהים (3.3 מ׳ לקומה), הלובי והמסחר להמחשה.",
        "The lot and the towers' outlines per the Tel Aviv-Yafo Municipality; the heights (3.3 m per floor), the lobby and the retail are an illustration.",
        "Le terrain et l'emprise des tours selon la municipalité de Tel Aviv-Jaffa ; les hauteurs (3.3 m par étage), le hall et les commerces sont indicatifs.",
        "Участок и контуры башен — по данным муниципалитета Тель-Авива-Яффо; высоты (3.3 м на этаж), лобби и торговые площади условны.",
        "القسيمة وخطوط البرجين بحسب بلدية تل أبيب يافا؛ الارتفاعات (3.3 م للطابق) والردهة والمتاجر للتوضيح."),
    row("המגרש לפי עיריית תל אביב-יפו; הבניינים, הקומות והגבהים לפי תכנית העיצוב (5.2023) בקירוב; החזיתות להמחשה.",
        "The lot per the Tel Aviv-Yafo Municipality; the buildings, the floors and the heights approximately per the design plan (5.2023); the facades are an illustration.",
        "Le terrain selon la municipalité de Tel Aviv-Jaffa ; les immeubles, les étages et les hauteurs approximativement selon le plan d'aménagement (5.2023) ; les façades sont indicatives.",
        "Участок — по данным муниципалитета Тель-Авива-Яффо; здания, этажи и высоты — приблизительно по архитектурному плану (5.2023); фасады условны.",
        "القسيمة بحسب بلدية تل أبيب يافا؛ المباني والطوابق والارتفاعات بحسب مخطط التصميم (5.2023) تقريباً؛ الواجهات للتوضيح."),
    # --- the view panel and what lies that way (bridge.js, the page's view block)
    row("מה יש לכיוון הזה", "What lies in this direction", "Ce qui se trouve dans cette direction", "Что находится в этом направлении", "ما الذي يقع في هذا الاتجاه"),
    row("אין בכיוון הזה מקומות מסומנים בקובץ הרובע.", "No places are marked in this direction in the quarter's data.", "Aucun lieu n'est signalé dans cette direction dans les données du quartier.", "В данных района в этом направлении нет отмеченных мест.", "لا توجد أماكن مُعلَّمة في هذا الاتجاه في بيانات الحي."),
    row("עכשיו בחרו דירה לדוגמה בטבעת הקומה, והנוף ממנה יופיע כאן.", "Now choose an example apartment on the floor's ring, and its view will appear here.", "Choisissez maintenant un appartement témoin sur l'anneau de l'étage, et sa vue apparaîtra ici.", "Теперь выберите квартиру-пример на кольце этажа, и вид из неё появится здесь.", "الآن اختاروا شقة نموذجية على حلقة الطابق، وستظهر إطلالتها هنا."),
    row("עכשיו בחרו נקודה בטבעת הקומה, והנוף לכיוון הזה יופיע כאן.", "Now choose a point on the floor's ring, and the view in that direction will appear here.", "Choisissez maintenant un point sur l'anneau de l'étage, et la vue dans cette direction apparaîtra ici.", "Теперь выберите точку на кольце этажа, и вид в этом направлении появится здесь.", "الآن اختاروا نقطة على حلقة الطابق، وستظهر الإطلالة في هذا الاتجاه هنا."),
    row("בחרו קומה ודירה לדוגמה", "Choose a floor and an example apartment", "Choisissez un étage et un appartement témoin", "Выберите этаж и квартиру-пример", "اختاروا طابقاً وشقة نموذجية"),
    row("בחרו קומה וכיוון", "Choose a floor and a direction", "Choisissez un étage et une direction", "Выберите этаж и направление", "اختاروا طابقاً واتجاهاً"),
    row("בחרו קומה במגדל ודירה לדוגמה בטבעת שלה, והנוף מהדירה יופיע כאן.", "Choose a floor in the tower and an example apartment on its ring, and the view from the apartment will appear here.", "Choisissez un étage de la tour et un appartement témoin sur son anneau, et la vue depuis l'appartement apparaîtra ici.", "Выберите этаж в башне и квартиру-пример на его кольце, и вид из квартиры появится здесь.", "اختاروا طابقاً في البرج وشقة نموذجية على حلقته، وستظهر الإطلالة من الشقة هنا."),
    row("בחרו קומה במגדל ונקודה בטבעת שלה, והנוף מהגובה ומהכיוון האלה יופיע כאן.", "Choose a floor in the tower and a point on its ring, and the view from that height and direction will appear here.", "Choisissez un étage de la tour et un point sur son anneau, et la vue depuis cette hauteur et dans cette direction apparaîtra ici.", "Выберите этаж в башне и точку на его кольце, и вид с этой высоты в этом направлении появится здесь.", "اختاروا طابقاً في البرج ونقطة على حلقته، وستظهر الإطلالة من هذا الارتفاع وفي هذا الاتجاه هنا."),
    row("מבט משוער מהקומה לכיוון שנבחר", "Estimated view from the floor in the chosen direction", "Vue estimée depuis l'étage dans la direction choisie", "Примерный вид с этажа в выбранном направлении", "إطلالة تقديرية من الطابق في الاتجاه المختار"),
    row("הכיוון על המפה", "The direction on the map", "La direction sur la carte", "Направление на карте", "الاتجاه على الخريطة"),
    row("הזיזו את המפה בשתי אצבעות", "Move the map with two fingers", "Déplacez la carte avec deux doigts", "Двигайте карту двумя пальцами", "حرّكوا الخريطة بإصبعين"),
    row("קיים", "Existing", "Existant", "Существует", "قائم"),
    row("בהליכי היתר", "In the permit process", "Permis en cours", "В процессе получения разрешения", "في إجراءات الترخيص"),
    row("מאושרת, עוד לא פועלת", "Approved, not yet running", "Approuvée, pas encore en service", "Утверждена, ещё не работает", "مُصادَق عليها، لم تعمل بعد"),
    row("שטח ציבורי פתוח", "Public open space", "Espace public ouvert", "Открытое общественное пространство", "مساحة عامة مفتوحة"),
    row("מבנה ציבור, 25 קומות", "Public building, 25 floors", "Bâtiment public, 25 étages", "Общественное здание, 25 этажей", "مبنى عام، 25 طابقاً"),
    row("תחנה תת־קרקעית", "Underground station", "Station souterraine", "Подземная станция", "محطة تحت الأرض"),
    # what lies each way (inc/project-stage.php 'sectors'): whole, and the tail the slice sets on its own line after "לכיוון"
    row("לכיוון", "towards", "vers", "в сторону", "باتجاه"),
    row("לכיוון הים", "towards the sea", "vers la mer", "в сторону моря", "باتجاه البحر"),
    row("הים", "the sea", "la mer", "моря", "البحر"),
    row("לכיוון תל ברוך והרצליה", "towards Tel Baruch and Herzliya", "vers Tel Baruch et Herzliya", "в сторону Тель-Баруха и Герцлии", "باتجاه تل باروخ وهرتسليا"),
    row("תל ברוך והרצליה", "Tel Baruch and Herzliya", "Tel Baruch et Herzliya", "Тель-Баруха и Герцлии", "تل باروخ وهرتسليا"),
    row("לכיוון רמת אביב והאוניברסיטה", "towards Ramat Aviv and the university", "vers Ramat Aviv et l'université", "в сторону Рамат-Авива и университета", "باتجاه رمات أفيف والجامعة"),
    row("רמת אביב והאוניברסיטה", "Ramat Aviv and the university", "Ramat Aviv et l'université", "Рамат-Авива и университета", "رمات أفيف والجامعة"),
    row("לכיוון פארק הירקון", "towards the Yarkon Park", "vers le parc HaYarkon", "в сторону парка Яркон", "باتجاه حديقة اليركون"),
    row("פארק הירקון", "the Yarkon Park", "le parc HaYarkon", "парка Яркон", "حديقة اليركون"),
    row("לכיוון מגדלי העיר", "towards the city's towers", "vers les tours de la ville", "в сторону городских башен", "باتجاه أبراج المدينة"),
    row("מגדלי העיר", "the city's towers", "les tours de la ville", "городских башен", "أبراج المدينة"),
    row("לכיוון הצפון הישן", "towards the Old North", "vers le Vieux Nord", "в сторону Старого Севера", "باتجاه الشمال القديم"),
    row("הצפון הישן", "the Old North", "le Vieux Nord", "Старого Севера", "الشمال القديم"),
    row("לכיוון נמל תל אביב והירקון", "towards the Tel Aviv Port and the Yarkon", "vers le port de Tel Aviv et le Yarkon", "в сторону Тель-Авивского порта и Яркона", "باتجاه ميناء تل أبيب واليركون"),
    row("נמל תל אביב והירקון", "the Tel Aviv Port and the Yarkon", "le port de Tel Aviv et le Yarkon", "Тель-Авивского порта и Яркона", "ميناء تل أبيب واليركون"),
    row("לכיוון כיכר המדינה", "towards Kikar HaMedina", "vers la place HaMedina", "в сторону площади Кикар-ха-Медина", "باتجاه ساحة همدينا"),
    row("כיכר המדינה", "Kikar HaMedina", "la place HaMedina", "площади Кикар-ха-Медина", "ساحة همدينا"),
    row("לכיוון מגדלי עזריאלי ושרונה", "towards the Azrieli towers and Sarona", "vers les tours Azrieli et Sarona", "в сторону башен Азриэли и Сароны", "باتجاه أبراج عزرائيلي وسارونا"),
    row("מגדלי עזריאלי ושרונה", "the Azrieli towers and Sarona", "les tours Azrieli et Sarona", "башен Азриэли и Сароны", "أبراج عزرائيلي وسارونا"),
    row("לכיוון כיכר רבין ומרכז העיר", "towards Rabin Square and the city centre", "vers la place Rabin et le centre-ville", "в сторону площади Рабина и центра города", "باتجاه ساحة رابين ومركز المدينة"),
    row("כיכר רבין ומרכז העיר", "Rabin Square and the city centre", "la place Rabin et le centre-ville", "площади Рабина и центра города", "ساحة رابين ومركز المدينة"),
    # --- the quarter's cards (stage.js)
    # "from <project>" in the quarter card's distance line (stage.js T.from); French elides before a vowel
    row("מריינבו", "from Rainbow", "de Rainbow", "от Rainbow", "من Rainbow"),
    row("מ־DUO", "from DUO", "de DUO", "от DUO", "من DUO"),
    row("מדמרי ימה", "from Dimri Yama", "de Dimri Yama", "от Dimri Yama", "من Dimri Yama"),
    row("מאשירה", "from Ashira", "d'Ashira", "от Ashira", "من Ashira"),
    row("מקום ברובע", "A place in the quarter", "Un lieu du quartier", "Место в районе", "مكان في الحي"),
    row("פרויקט ברובע", "A project in the quarter", "Un projet du quartier", "Проект в районе", "مشروع في الحي"),
    row("מקום בסביבה", "A place nearby", "Un lieu à proximité", "Место поблизости", "مكان في المحيط"),
    row("פרויקט בסביבה", "A project nearby", "Un projet à proximité", "Проект поблизости", "مشروع في المحيط"),
    row("לעמוד הפרויקט", "To the project's page", "Vers la page du projet", "На страницу проекта", "إلى صفحة المشروع"),
    row("מסה סכמטית לפי מספר הקומות בעמוד הפרויקט; המיקום לפי המגרש. הדמיה להמחשה בלבד.",
        "A schematic mass by the number of floors on the project's page; the position by the lot. An illustration only.",
        "Volume schématique selon le nombre d'étages indiqué sur la page du projet ; l'emplacement selon le terrain. Illustration uniquement.",
        "Схематический объём по числу этажей на странице проекта; расположение — по участку. Только иллюстрация.",
        "كتلة تخطيطية بحسب عدد الطوابق في صفحة المشروع؛ الموقع بحسب القسيمة. تصور توضيحي فقط."),
    row("עמוד הפרויקט באתר", "The project's page on the site", "La page du projet sur le site", "Страница проекта на сайте", "صفحة المشروع في الموقع"),
    row("שכבת הקו הירוק של עיריית תל אביב-יפו (תחנות)", "The Tel Aviv-Yafo Municipality's Green Line layer (stations)", "La couche de la ligne verte de la municipalité de Tel Aviv-Jaffa (stations)", "Слой Зелёной линии муниципалитета Тель-Авива-Яффо (станции)", "طبقة الخط الأخضر في بلدية تل أبيب يافا (المحطات)"),
    # --- the facilities (facilities.json): kicker, names, pins, room buttons and titles
    row("מתקן בפרויקט", "Facility in the project", "Équipement du projet", "Объект в проекте", "مرفق في المشروع"),
    row("מתקנים בפרויקט", "Facilities in the project", "Équipements du projet", "Инфраструктура проекта", "مرافق المشروع"),
    row("מתקן לדוגמה", "Example facility", "Équipement témoin", "Пример объекта", "مرفق نموذجي"),
    # --- AreaLife v97 (1.72.361): the groups, the planned station, the sources
    row("פארקים, חוף וספורט", "Parks, beach and sport", "Parcs, plage et sport", "Парки, пляж и спорт", "حدائق وشاطئ ورياضة"),
    row("קניות וסידורים", "Shops and errands", "Commerces et services", "Магазины и услуги", "تسوق وخدمات"),
    row("קהילה ותרבות", "Community and culture", "Vie locale et culture", "Сообщество и культура", "المجتمع والثقافة"),
    row("מתוכננת", "planned", "prévue", "планируется", "مخطط لها"),
    row("מקומות: findplace.co.il (עיריית תל אביב-יפו, מידע פתוח, ו-OpenStreetMap). זמני הליכה לפי מסלול הליכה של Mapbox, מהבניין; מרחק בקו אווירי.", "Places: findplace.co.il (Tel Aviv-Yafo open data, and OpenStreetMap). Walking times by Mapbox walking routes from the building; distance in a straight line.", "Lieux : findplace.co.il (données ouvertes de Tel Aviv-Jaffa, et OpenStreetMap). Temps de marche selon les itinéraires piétons Mapbox depuis l'immeuble ; distance à vol d'oiseau.", "Места: findplace.co.il (открытые данные Тель-Авива-Яффо и OpenStreetMap). Время пешком по пешеходным маршрутам Mapbox от здания; расстояние по прямой.", "الأماكن: findplace.co.il (بيانات تل أبيب-يافا المفتوحة وOpenStreetMap). أوقات السير وفق مسارات المشي من Mapbox من المبنى؛ المسافة بخط مستقيم."),
    row("השמות בחלון: findplace ו-OpenStreetMap, בכיוון ובמרחק האמיתיים מהבניין; מה שבניין מסתיר לא מסומן.", "The names in the window: findplace and OpenStreetMap, at their true direction and distance from the building; what a building hides is not marked.", "Les noms dans la fenêtre : findplace et OpenStreetMap, à leur direction et distance réelles depuis l'immeuble ; ce qu'un bâtiment cache n'est pas indiqué.", "Названия в окне: findplace и OpenStreetMap, в реальном направлении и на реальном расстоянии от здания; то, что закрывает здание, не отмечено.", "الأسماء في النافذة: findplace وOpenStreetMap، باتجاهها ومسافتها الحقيقيين من المبنى؛ ما يحجبه مبنى لا يُشار إليه."),
    # --- StageFacilities v95 (1.72.357), BuildingWalk v96 (1.72.358-359), DUO's 360 lines (1.72.353)
    row("המתקנים בפרויקט", "The project's facilities", "Les équipements du projet", "Объекты проекта", "مرافق المشروع"),
    row("הסלון בדירה לדוגמה בקומה 25 במגדלי דואו, מבט מערבה לכיוון הים (הדמיה)", "The living room of the example apartment on floor 25 at DUO, looking west toward the sea (illustration)", "Le séjour de l'appartement témoin au 25e étage de DUO, vue vers l'ouest et la mer (illustration)", "Гостиная квартиры-примера на 25-м этаже в DUO, вид на запад, к морю (иллюстрация)", "صالون الشقة النموذجية في الطابق 25 في DUO، إطلالة غربًا نحو البحر (تصوير توضيحي)"),
    row("סלון ומטבח פתוח כמו במסירה, בלי ריהוט, בגובה של כ־89 מ׳: מול הים, נמל תל אביב, כיכר המדינה ומרכז העיר. הנוף בחלון בנוי מהבניינים הקיימים לפי שכבת המבנים של העירייה ומקו החוף.", "A living room with an open kitchen, as delivered, without furniture, at about 89 m: facing the sea, Tel Aviv Port, Kikar HaMedina and the city centre. The view in the window is built from the existing buildings, by the municipality's buildings layer and the coastline.", "Un séjour avec cuisine ouverte, tel que livré, sans mobilier, à environ 89 m : face à la mer, au port de Tel Aviv, à la place HaMedina et au centre-ville. La vue par la fenêtre est construite à partir des bâtiments existants, selon la couche des bâtiments de la municipalité et le trait de côte.", "Гостиная с открытой кухней, как при сдаче, без мебели, на высоте около 89 м: вид на море, порт Тель-Авива, площадь Ха-Медина и центр города. Вид из окна построен по существующим зданиям, по слою зданий муниципалитета и береговой линии.", "صالون مع مطبخ مفتوح كما يُسلَّم، بلا أثاث، على ارتفاع نحو 89 م: مقابل البحر وميناء تل أبيب وساحة همدينا ومركز المدينة. الإطلالة من النافذة مبنية من المباني القائمة وفق طبقة المباني في البلدية وخط الساحل."),
    row("בבניין", "In the building", "Dans l'immeuble", "В здании", "في المبنى"),
    row("חזרה", "Back", "Retour", "Назад", "رجوع"),
    row("לאן?", "Where to?", "Où aller ?", "Куда?", "إلى أين؟"),
    row("מעבר להמחשה", "An illustrative move", "Passage indicatif", "Условный переход", "انتقال توضيحي"),
    row("מעבר בין הדמיות, לא לפי תוכנית", "A move between illustrations, not by a plan", "Passage entre illustrations, pas selon un plan", "Переход между иллюстрациями, не по плану", "انتقال بين صور توضيحية، لا وفق مخطط"),
    row("הדמיות; המעברים להמחשה", "Illustrations; the moves are indicative", "Illustrations ; les passages sont indicatifs", "Иллюстрации; переходы условные", "صور توضيحية؛ الانتقالات للتوضيح"),
    row("אתם כאן", "You are here", "Vous êtes ici", "Вы здесь", "أنتم هنا"),
    row("הדירה", "The apartment", "L'appartement", "Квартира", "الشقة"),
    row("יציאה מהדירה", "Leave the apartment", "Sortir de l'appartement", "Выйти из квартиры", "الخروج من الشقة"),
    row("לובי, מועדון, בריכה", "Lobby, club, pool", "Hall, club, piscine", "Лобби, клуб, бассейн", "الردهة، النادي، المسبح"),
    row("הלובי", "The lobby", "Le hall", "Лобби", "الردهة"),
    row("המועדון", "The club", "Le club", "Клуб", "النادي"),
    row("הבריכה על הגג", "The rooftop pool", "La piscine sur le toit", "Бассейн на крыше", "المسبح على السطح"),
    row("קומת הכניסה של המגדל", "The tower's entrance floor", "Le niveau d'entrée de la tour", "Входной этаж башни", "طابق مدخل البرج"),
    row("בבסיס המגדל, לפי תכנית העיצוב", "At the tower's base, by the design plan", "À la base de la tour, selon le plan de conception", "В основании башни, по плану дизайна", "في قاعدة البرج، وفق مخطط التصميم"),
    row("על גג של בניין בוטיק", "On a boutique building's roof", "Sur le toit d'un immeuble boutique", "На крыше бутик-здания", "على سطح مبنى بوتيك"),
    row("המעליות", "The lifts", "Les ascenseurs", "Лифты", "المصاعد"),
    row("לדירה, למועדון, לבריכה", "To the apartment, the club, the pool", "Vers l'appartement, le club, la piscine", "К квартире, клубу, бассейну", "إلى الشقة، النادي، المسبح"),
    row("לחצר ולבריכה", "To the courtyard and the pool", "Vers la cour et la piscine", "Во двор и к бассейну", "إلى الفناء والمسبح"),
    row("יציאה מהמועדון", "Leave the club", "Sortir du club", "Выйти из клуба", "الخروج من النادي"),
    row("לובי, דירה, בריכה", "Lobby, apartment, pool", "Hall, appartement, piscine", "Лобби, квартира, бассейн", "الردهة، الشقة، المسبح"),
    row("יציאה מהגג", "Leave the roof", "Quitter le toit", "Уйти с крыши", "الخروج من السطح"),
    row("לובי, מועדון, דירה", "Lobby, club, apartment", "Hall, club, appartement", "Лобби, клуб, квартира", "الردهة، النادي، الشقة"),
    row("לובי, וולנס, בריכה", "Lobby, wellness, pool", "Hall, bien-être, piscine", "Лобби, велнес, бассейн", "الردهة، العافية، المسبح"),
    row("הוולנס", "The wellness centre", "L'espace bien-être", "Велнес-центр", "مركز العافية"),
    row("מחבר בין שני המגדלים, לפי אתר היזם", "Connects the two towers, per the developer's site", "Relie les deux tours, selon le site du promoteur", "Соединяет две башни, по сайту застройщика", "يربط بين البرجين، وفق موقع المطوّر"),
    row("כניסה ישירה מהלובי, לפי אתר היזם", "Direct entry from the lobby, per the developer's site", "Accès direct depuis le hall, selon le site du promoteur", "Прямой вход из лобби, по сайту застройщика", "دخول مباشر من الردهة، وفق موقع المطوّر"),
    row("המגדל הצפוני", "The north tower", "La tour nord", "Северная башня", "البرج الشمالي"),
    row("המגדל הדרומי", "The south tower", "La tour sud", "Южная башня", "البرج الجنوبي"),
    row("ללובי", "To the lobby", "Vers le hall", "В лобби", "إلى الردهة"),
    row("כניסה ישירה, לפי אתר היזם", "Direct entry, per the developer's site", "Accès direct, selon le site du promoteur", "Прямой вход, по сайту застройщика", "دخول مباشر، وفق موقع المطوّر"),
    row("שאלה על המתקן בוואטסאפ", "Ask about this facility on WhatsApp", "Question sur cet équipement par WhatsApp", "Спросить об этом объекте в WhatsApp", "اسألوا عن هذا المرفق عبر واتساب"),
    row("כניסה ב־360°", "Step inside in 360°", "Entrer en 360°", "Войти в 360°", "الدخول بزاوية 360°"),
    row("כניסה לבריכה", "Step into the pool area", "Entrer dans l'espace piscine", "Войти в зону бассейна", "الدخول إلى المسبح"),
    row("כניסה למועדון", "Step into the club", "Entrer dans le club", "Войти в клуб", "الدخول إلى النادي"),
    row("כניסה ללובי", "Step into the lobby", "Entrer dans le hall", "Войти в лобби", "الدخول إلى الردهة"),
    row("בריכה על גג של בניין בוטיק · הדמיה", "A pool on the roof of a boutique building · illustration", "Piscine sur le toit d'un immeuble boutique · illustration", "Бассейн на крыше бутик-дома · иллюстрация", "مسبح على سطح مبنى بوتيك · تصور توضيحي"),
    row("מועדון הדיירים וחדר הכושר · הדמיה", "The residents' club and the gym · illustration", "Le club des résidents et la salle de sport · illustration", "Клуб жильцов и тренажёрный зал · иллюстрация", "نادي السكان والصالة الرياضية · تصور توضيحي"),
    row("הלובי במגדל · הדמיה", "The tower's lobby · illustration", "Le hall de la tour · illustration", "Лобби башни · иллюстрация", "ردهة البرج · تصور توضيحي"),
    # DUO's facility rooms (facilities.json, 28.9.2026 15:43: after the harvest)
    row("כניסה למתחם הוולנס", "Step into the wellness area", "Entrer dans l'espace bien-être", "Войти в велнес-зону", "الدخول إلى منطقة العافية"),
    row("הבריכה על גג מבנה הלובי · הדמיה", "The pool on the roof of the lobby building · illustration", "La piscine sur le toit du bâtiment du hall · illustration", "Бассейн на крыше здания лобби · иллюстрация", "المسبح على سطح مبنى الردهة · تصور توضيحي"),
    row("הלובי בגובה של כ־7 מטרים · הדמיה", "The lobby, about 7 metres high · illustration", "Le hall d'environ 7 mètres de haut · illustration", "Лобби высотой около 7 метров · иллюстрация", "الردهة بارتفاع نحو 7 أمتار · تصور توضيحي"),
    row("מתחם הוולנס וחדר הכושר · הדמיה", "The wellness area and the gym · illustration", "L'espace bien-être et la salle de sport · illustration", "Велнес-зона и тренажёрный зал · иллюстрация", "منطقة العافية والصالة الرياضية · تصور توضيحي"),
    row("שתי בריכות על הגגות", "Two pools on the roofs", "Deux piscines sur les toits", "Два бассейна на крышах", "مسبحان على الأسطح"),
    row("בריכות", "Pools", "Piscines", "Бассейны", "مسابح"),
    row("Rainbow Club, מועדון הדיירים", "Rainbow Club, the residents' club", "Rainbow Club, le club des résidents", "Rainbow Club, клуб жильцов", "Rainbow Club، نادي السكان"),
    row("מועדון דיירים", "Residents' club", "Club des résidents", "Клуб жильцов", "نادي السكان"),
    row("לובי בכל בניין", "A lobby in every building", "Un hall dans chaque immeuble", "Лобби в каждом здании", "ردهة في كل مبنى"),
    row("לובי", "Lobby", "Hall", "Лобби", "الردهة"),
    row("מסחר בקומת הקרקע", "Retail on the ground floor", "Commerces en rez-de-chaussée", "Торговля на первом этаже", "متاجر في الطابق الأرضي"),
    row("מסחר", "Retail", "Commerces", "Торговля", "متاجر"),
    row("חניון תת־קרקעי", "Underground car park", "Parking souterrain", "Подземный паркинг", "موقف سيارات تحت الأرض"),
    row("חניון", "Car park", "Parking", "Паркинг", "موقف السيارات"),
    row("בריכת אינפיניטי על גג מבנה הלובי", "An infinity pool on the roof of the lobby building", "Piscine à débordement sur le toit du bâtiment du hall", "Инфинити-бассейн на крыше здания лобби", "مسبح إنفينيتي على سطح مبنى الردهة"),
    row("בריכה", "Pool", "Piscine", "Бассейн", "المسبح"),
    row("לובי בגובה של כ־7 מטרים", "A lobby about 7 metres high", "Un hall d'environ 7 mètres de haut", "Лобби высотой около 7 метров", "ردهة بارتفاع نحو 7 أمتار"),
    row("מתחם וולנס, חדר כושר ומועדון דיירים", "A wellness area, a gym and a residents' club", "Espace bien-être, salle de sport et club des résidents", "Велнес-зона, тренажёрный зал и клуб жильцов", "منطقة عافية وصالة رياضية ونادٍ للسكان"),
    row("וולנס וכושר", "Wellness and gym", "Bien-être et sport", "Велнес и фитнес", "العافية والرياضة"),
    row("בריכות פרטיות בפנטהאוזים", "Private pools in the penthouses", "Piscines privées dans les penthouses", "Частные бассейны в пентхаусах", "مسابح خاصة في البنتهاوسات"),
    row("בריכות פרטיות", "Private pools", "Piscines privées", "Частные бассейны", "مسابح خاصة"),
    row("מתחם מסחר וחצר שקועה", "A retail complex and a sunken courtyard", "Complexe commercial et cour en contrebas", "Торговый комплекс и заглублённый двор", "مجمّع تجاري وساحة غائرة"),
    row("בריכות על גג מבנה המלון", "Pools on the roof of the hotel building", "Piscines sur le toit du bâtiment de l'hôtel", "Бассейны на крыше здания отеля", "مسابح على سطح مبنى الفندق"),
    row("בריכות פרטיות בקומות העליונות", "Private pools on the top floors", "Piscines privées aux derniers étages", "Частные бассейны на верхних этажах", "مسابح خاصة في الطوابق العليا"),
    row("ספא, חדרי כושר וסטודיו", "A spa, gyms and a studio", "Spa, salles de sport et studio", "Спа, тренажёрные залы и студия", "سبا وصالات رياضية واستوديو"),
    row("ספא וכושר", "Spa and gym", "Spa et sport", "Спа и фитнес", "سبا ورياضة"),
    row("מלון ומגורים במבנה הדרום מזרחי", "A hotel and homes in the south-eastern building", "Hôtel et logements dans le bâtiment sud-est", "Отель и квартиры в юго-восточном здании", "فندق ومساكن في المبنى الجنوبي الشرقي"),
    row("מלון", "Hotel", "Hôtel", "Отель", "الفندق"),
    row("מסחר וקולונדה ברחובות", "Retail and a colonnade on the streets", "Commerces et colonnade sur les rues", "Торговля и колоннада вдоль улиц", "متاجر ورواق أعمدة على الشوارع"),
    row("גינה פנימית עם מעבר ציבורי", "An inner garden with a public passage", "Jardin intérieur avec passage public", "Внутренний сад с общественным проходом", "حديقة داخلية مع ممر عام"),
    row("גינה", "Garden", "Jardin", "Сад", "الحديقة"),
    row("בריכה וחדרי כושר בקומת המרתף", "A pool and gyms on the basement floor", "Piscine et salles de sport au sous-sol", "Бассейн и тренажёрные залы на подземном этаже", "مسبح وصالات رياضية في طابق القبو"),
    row("בריכה וכושר", "Pool and gym", "Piscine et sport", "Бассейн и фитнес", "مسبح ورياضة"),
    row("שלושה מועדוני דיירים", "Three residents' clubs", "Trois clubs de résidents", "Три клуба для жильцов", "ثلاثة نوادٍ للسكان"),
    row("הכניסות והלובי", "The entrances and the lobby", "Les entrées et le hall", "Входы и лобби", "المداخل والردهة"),
    row("גן ילדים ומבנה ציבור", "A kindergarten and a public building", "Jardin d'enfants et bâtiment public", "Детский сад и общественное здание", "روضة أطفال ومبنى عام"),
    row("גן ילדים", "Kindergarten", "Jardin d'enfants", "Детский сад", "روضة أطفال"),
    row("מסחר וקולונדה בחזית הדרומית", "Retail and a colonnade on the southern front", "Commerces et colonnade sur la façade sud", "Торговля и колоннада на южном фасаде", "متاجر ورواق أعمدة على الواجهة الجنوبية"),
    row("חצר משותפת עם מעבר ציבורי", "A shared courtyard with a public passage", "Cour commune avec passage public", "Общий двор с общественным проходом", "ساحة مشتركة مع ممر عام"),
    row("חצר", "Courtyard", "Cour", "Двор", "الساحة"),
    # the facilities' lines and notes without numbers
    row("אתר הפרויקט מתאר בריכת אינפיניטי על הגג, בריכת ילדים ובריכה למבוגרים בלבד.",
        "The project's site describes a rooftop infinity pool, a children's pool and an adults-only pool.",
        "Le site du projet décrit une piscine à débordement sur le toit, une pataugeoire et une piscine réservée aux adultes.",
        "Сайт проекта описывает инфинити-бассейн на крыше, детский бассейн и бассейн только для взрослых.",
        "يصف موقع المشروع مسبح إنفينيتي على السطح ومسبحاً للأطفال ومسبحاً للبالغين فقط."),
    row("איזה שני גגות לא פורסם, והמיקום בדגם להמחשה. מקורות: תכנית העיצוב, אתר הפרויקט.",
        "Which two roofs they are has not been published, and the position in the model is an illustration. Sources: the design plan, the project's site.",
        "Les deux toits concernés n'ont pas été rendus publics, et l'emplacement dans la maquette est indicatif. Sources : le plan d'aménagement, le site du projet.",
        "Какие именно две крыши, не опубликовано, а расположение на модели условное. Источники: архитектурный план, сайт проекта.",
        "لم يُنشر أيّ السطحين، والموقع في النموذج للتوضيح. المصادر: مخطط التصميم، موقع المشروع."),
    row("לפי היזם: חדר כושר, סטודיו, ספא, סאונות ואמבטיות קרח, מרכז עסקים, מועדון ילדים ובית קפה פרטי.",
        "Per the developer: a gym, a studio, a spa, saunas and ice baths, a business centre, a kids' club and a private café.",
        "Selon le promoteur : salle de sport, studio, spa, saunas et bains glacés, centre d'affaires, club enfants et café privé.",
        "По данным застройщика: тренажёрный зал, студия, спа, сауны и ледяные ванны, бизнес-центр, детский клуб и частное кафе.",
        "بحسب المطوّر: صالة رياضية واستوديو وسبا وساونا وأحواض ثلج ومركز أعمال ونادٍ للأطفال ومقهى خاص."),
    row("לפי תכנית העיצוב: לכל בניין לובי משלו, עם חזית לרחוב וחזית לחצר.",
        "Per the design plan: each building has its own lobby, with a front to the street and a front to the courtyard.",
        "Selon le plan d'aménagement : chaque immeuble a son propre hall, avec une façade sur rue et une façade sur cour.",
        "По архитектурному плану: у каждого здания своё лобби, с фасадом на улицу и фасадом во двор.",
        "بحسب مخطط التصميم: لكل مبنى ردهة خاصة به، بواجهة على الشارع وواجهة على الساحة."),
    row("הלובי המסומן בדגם הוא של המגדל, להמחשה. מקור: תכנית העיצוב.",
        "The lobby marked in the model is the tower's, for illustration. Source: the design plan.",
        "Le hall signalé sur la maquette est celui de la tour, à titre indicatif. Source : le plan d'aménagement.",
        "Отмеченное на модели лобби — лобби башни, для иллюстрации. Источник: архитектурный план.",
        "الردهة المُعلَّمة في النموذج هي ردهة البرج، للتوضيح. المصدر: مخطط التصميم."),
    row("המיקום בדגם להמחשה. מקור: תכנית העיצוב.",
        "The position in the model is an illustration. Source: the design plan.",
        "L'emplacement dans la maquette est indicatif. Source : le plan d'aménagement.",
        "Расположение на модели условное. Источник: архитектурный план.",
        "الموقع في النموذج للتوضيح. المصدر: مخطط التصميم."),
    row("לפי פרסומי היזם: חניון תת־קרקעי מתחת למתחם.",
        "Per the developer's publications: an underground car park beneath the complex.",
        "Selon les publications du promoteur : un parking souterrain sous l'ensemble.",
        "По публикациям застройщика: подземный паркинг под комплексом.",
        "بحسب منشورات المطوّر: موقف سيارات تحت الأرض أسفل المجمّع."),
    row("לפי אתר היזם: בריכת אינפיניטי חיצונית ובריכת פעוטות, על גג מבנה הלובי שבין שני מגדלי המגורים.",
        "Per the developer's site: an outdoor infinity pool and a toddlers' pool, on the roof of the lobby building between the two residential towers.",
        "Selon le site du promoteur : une piscine extérieure à débordement et une pataugeoire, sur le toit du bâtiment du hall entre les deux tours résidentielles.",
        "По данным сайта застройщика: открытый инфинити-бассейн и бассейн для малышей на крыше здания лобби между двумя жилыми башнями.",
        "بحسب موقع المطوّر: مسبح إنفينيتي خارجي ومسبح للأطفال الصغار، على سطح مبنى الردهة بين برجي السكن."),
    row("צורת מבנה הלובי בדגם להמחשה. מקור: אתר DUO.",
        "The lobby building's shape in the model is an illustration. Source: the DUO site.",
        "La forme du bâtiment du hall dans la maquette est indicative. Source : le site DUO.",
        "Форма здания лобби на модели условна. Источник: сайт DUO.",
        "شكل مبنى الردهة في النموذج للتوضيح. المصدر: موقع DUO."),
    row("לפי אתר היזם: מתחם וולנס עם כניסה ישירה מהלובי, חדר כושר מתקדם ומועדון דיירים.",
        "Per the developer's site: a wellness area with direct access from the lobby, an advanced gym and a residents' club.",
        "Selon le site du promoteur : un espace bien-être avec accès direct depuis le hall, une salle de sport moderne et un club des résidents.",
        "По данным сайта застройщика: велнес-зона со входом прямо из лобби, современный тренажёрный зал и клуб жильцов.",
        "بحسب موقع المطوّر: منطقة عافية بمدخل مباشر من الردهة، وصالة رياضية متطورة، ونادٍ للسكان."),
    row("לפי אתר היזם: מתחם וולנס עם כניסה ישירה מהלובי, חדר כושר יוצא דופן בגודלו ומועדון דיירים.",
        "Per the developer's site: a wellness area with direct access from the lobby, an exceptionally large gym and a residents' club.",
        "Selon le site du promoteur : un espace bien-être avec accès direct depuis le hall, une salle de sport d'une taille exceptionnelle et un club des résidents.",
        "По данным сайта застройщика: велнес-зона со входом прямо из лобби, тренажёрный зал исключительно большого размера и клуб жильцов.",
        "بحسب موقع المطوّر: منطقة عافية بمدخل مباشر من الردهة، وصالة رياضية بحجم استثنائي، ونادٍ للسكان."),
    row("הקומה לא פורסמה, והמיקום בדגם להמחשה. מקור: אתר DUO.",
        "The floor has not been published, and the position in the model is an illustration. Source: the DUO site.",
        "L'étage n'a pas été rendu public, et l'emplacement dans la maquette est indicatif. Source : le site DUO.",
        "Этаж не опубликован, а расположение на модели условное. Источник: сайт DUO.",
        "لم يُنشر الطابق، والموقع في النموذج للتوضيح. المصدر: موقع DUO."),
    row("לפי החלטת רשות הרישוי: בחלקו המערבי של המגרש שלושה מבני מסחר, פיתוח שטח וחצר שקועה.",
        "Per the licensing authority's decision: in the western part of the lot, three retail buildings, landscaping and a sunken courtyard.",
        "Selon la décision de l'autorité d'octroi des permis : dans la partie ouest du terrain, trois bâtiments commerciaux, des aménagements extérieurs et une cour en contrebas.",
        "По решению органа выдачи разрешений: в западной части участка — три торговых корпуса, благоустройство и заглублённый двор.",
        "بحسب قرار سلطة الترخيص: في الجزء الغربي من القسيمة ثلاثة مبانٍ تجارية وتطوير للموقع وساحة غائرة."),
    row("לפי פרסומי היזם: בריכת אינפיניטי בקומת הגג ובריכה חצי אולימפית מקורה.",
        "Per the developer's publications: an infinity pool on the roof floor and a covered semi-Olympic pool.",
        "Selon les publications du promoteur : une piscine à débordement sur le toit et une piscine semi-olympique couverte.",
        "По публикациям застройщика: инфинити-бассейн на крыше и крытый полуолимпийский бассейн.",
        "بحسب منشورات المطوّر: مسبح إنفينيتي في طابق السطح ومسبح نصف أولمبي مغطى."),
    row("לפי תכנית העיצוב: הקומה התשיעית של מבנה המלון היא קומת שירותים לדיירים, משותפת לאורחי המלון.",
        "Per the design plan: the hotel building's ninth floor is a services floor for the residents, shared with the hotel's guests.",
        "Selon le plan d'aménagement : le neuvième étage du bâtiment de l'hôtel est un étage de services pour les résidents, partagé avec les clients de l'hôtel.",
        "По архитектурному плану: девятый этаж здания отеля — сервисный этаж для жильцов, общий с гостями отеля.",
        "بحسب مخطط التصميم: الطابق التاسع في مبنى الفندق طابق خدمات للسكان، مشترك مع نزلاء الفندق."),
    row("לפי פרסומי היזם: ספא, חדרי כושר, סטודיו ליוגה, ספרייה, חדר ילדים וחדר יין.",
        "Per the developer's publications: a spa, gyms, a yoga studio, a library, a children's room and a wine room.",
        "Selon les publications du promoteur : spa, salles de sport, studio de yoga, bibliothèque, salle pour enfants et cave à vin.",
        "По публикациям застройщика: спа, тренажёрные залы, студия йоги, библиотека, детская комната и винная комната.",
        "بحسب منشورات المطوّر: سبا وصالات رياضية واستوديو يوغا ومكتبة وغرفة أطفال وغرفة نبيذ."),
    row("מה מהשירותים נמצא בקומה התשיעית לא פורסם; המיקום בדגם להמחשה. מקורות: תכנית העיצוב, פרסומי היזם.",
        "Which of the services are on the ninth floor has not been published; the position in the model is an illustration. Sources: the design plan, the developer's publications.",
        "Les services situés au neuvième étage n'ont pas été rendus publics ; l'emplacement dans la maquette est indicatif. Sources : le plan d'aménagement, les publications du promoteur.",
        "Какие из услуг находятся на девятом этаже, не опубликовано; расположение на модели условное. Источники: архитектурный план, публикации застройщика.",
        "لم يُنشر أيّ الخدمات في الطابق التاسع؛ الموقع في النموذج للتوضيح. المصادر: مخطط التصميم، منشورات المطوّر."),
    row("לפי תכנית העיצוב: לכל בניין לובי מגורים בקומת הקרקע; לובי המלון במבנה הדרום מזרחי, בכניסה מדרום ומהחצר.",
        "Per the design plan: each building has a residential lobby on the ground floor; the hotel lobby is in the south-eastern building, entered from the south and from the courtyard.",
        "Selon le plan d'aménagement : chaque immeuble a un hall résidentiel au rez-de-chaussée ; le hall de l'hôtel est dans le bâtiment sud-est, avec une entrée par le sud et par la cour.",
        "По архитектурному плану: в каждом здании жилое лобби на первом этаже; лобби отеля — в юго-восточном здании, со входом с юга и со двора.",
        "بحسب مخطط التصميم: لكل مبنى ردهة سكنية في الطابق الأرضي؛ ردهة الفندق في المبنى الجنوبي الشرقي، بمدخل من الجنوب ومن الساحة."),
    row("לפי אתר היזם: בריכה חצי אולימפית מקורה, בריכת ילדים, ג׳קוזי וספא עם סאונה יבשה ורטובה וחדר מלח.",
        "Per the developer's site: a covered semi-Olympic pool, a children's pool, a jacuzzi and a spa with a dry and a wet sauna and a salt room.",
        "Selon le site du promoteur : une piscine semi-olympique couverte, une pataugeoire, un jacuzzi et un spa avec sauna sec et humide et salle de sel.",
        "По данным сайта застройщика: крытый полуолимпийский бассейн, детский бассейн, джакузи и спа с сухой и влажной сауной и соляной комнатой.",
        "بحسب موقع المطوّر: مسبح نصف أولمبي مغطى ومسبح للأطفال وجاكوزي وسبا مع ساونا جافة ورطبة وغرفة ملح."),
    row("לפי תכנית העיצוב: שלושה מועדוני דיירים, בקומות הקרקע של המגדל, של המגדלון ושל הבניין הדרום מזרחי.",
        "Per the design plan: three residents' clubs, on the ground floors of the tower, of the mid-rise and of the south-eastern building.",
        "Selon le plan d'aménagement : trois clubs de résidents, aux rez-de-chaussée de la tour, de la petite tour et du bâtiment sud-est.",
        "По архитектурному плану: три клуба для жильцов — на первых этажах башни, малой башни и юго-восточного здания.",
        "بحسب مخطط التصميم: ثلاثة نوادٍ للسكان، في الطوابق الأرضية للبرج والبرج الصغير والمبنى الجنوبي الشرقي."),
    row("לפי אתר היזם: לאונג׳ עם בר, קולנוע ואזור ילדים.",
        "Per the developer's site: a lounge with a bar, a cinema and a children's area.",
        "Selon le site du promoteur : un lounge avec bar, un cinéma et un espace enfants.",
        "По данным сайта застройщика: лаунж с баром, кинозал и детская зона.",
        "بحسب موقع المطوّر: صالة جلوس مع بار وسينما ومنطقة للأطفال."),
    row("לפי תכנית העיצוב: לבניינים שבמזרח נכנסים מרחוב לוי אשכול, למגדל נכנסים מהחצר המשותפת, ולבניין הצפון מערבי מהמערב.",
        "Per the design plan: the eastern buildings are entered from Levi Eshkol Street, the tower from the shared courtyard, and the north-western building from the west.",
        "Selon le plan d'aménagement : on entre dans les immeubles de l'est par la rue Levi Eshkol, dans la tour par la cour commune, et dans l'immeuble nord-ouest par l'ouest.",
        "По архитектурному плану: в восточные здания входят с улицы Леви Эшколя, в башню — из общего двора, а в северо-западное здание — с запада.",
        "بحسب مخطط التصميم: يُدخل إلى المباني الشرقية من شارع ليفي أشكول، وإلى البرج من الساحة المشتركة، وإلى المبنى الشمالي الغربي من الغرب."),
    row("לפי תכנית העיצוב: חצר במרכז המגרש, עם זיקת הנאה למעבר הציבור מצפון לדרום וממזרח למערב.",
        "Per the design plan: a courtyard in the middle of the lot, with a public right of way from north to south and from east to west.",
        "Selon le plan d'aménagement : une cour au centre du terrain, avec une servitude de passage public du nord au sud et d'est en ouest.",
        "По архитектурному плану: двор в центре участка с правом общественного прохода с севера на юг и с востока на запад.",
        "بحسب مخطط التصميم: ساحة في وسط القسيمة، مع حق مرور للجمهور من الشمال إلى الجنوب ومن الشرق إلى الغرب."),
    # --- the floor slice (slice.js)
    row("חתך הקומה", "Floor section", "Coupe de l'étage", "Разрез этажа", "مقطع الطابق"),
    row("חתך הקומה · להמחשה", "Floor section · illustration", "Coupe de l'étage · illustration", "Разрез этажа · иллюстрация", "مقطع الطابق · للتوضيح"),
    row("סגירת החתך", "Close the section", "Fermer la coupe", "Закрыть разрез", "إغلاق المقطع"),
    row("קומה", "Floor", "Étage", "Этаж", "الطابق"),
    row("קומה למעלה", "Floor up", "Étage au-dessus", "Этаж выше", "طابق للأعلى"),
    row("קומה למטה", "Floor down", "Étage en dessous", "Этаж ниже", "طابق للأسفل"),
    row("גרעין", "Core", "Noyau", "Ядро", "النواة"),
    row("לסל הדירה", "Add to the apartment basket", "Ajouter au panier de l'appartement", "Добавить в корзину квартиры", "أضيفوا إلى سلة الشقة"),
    row("קו החזית והמרפסות כמו בדגם שעל הבמה", "the facade line and the balconies as in the 3D model", "ligne de façade et balcons comme sur la maquette 3D", "линия фасада и балконы как на 3D-модели", "خط الواجهة والشرفات كما في النموذج ثلاثي الأبعاد"),
    row("הקומה נסוגה מקו החזית, והמרפסות עמוקות יותר", "the floor is set back from the facade line, and the balconies are deeper", "l'étage est en retrait de la façade, et les balcons sont plus profonds", "этаж отступает от линии фасада, а балконы глубже", "الطابق متراجع عن خط الواجهة، والشرفات أعمق"),
    # --- the 360 room (tour.js, the scenes and styles of inc/project-stage.php)
    row("גררו כדי להסתכל מסביב", "Drag to look around", "Faites glisser pour regarder autour", "Потяните, чтобы осмотреться", "اسحبوا للنظر حولكم"),
    row("איפה עומדים", "Where you stand", "Votre position", "Точка обзора", "نقطة المشاهدة"),
    row("כיוון הדירה", "The apartment's direction", "Orientation de l'appartement", "Направление квартиры", "اتجاه الشقة"),
    row("בסלון", "In the living room", "Dans le salon", "В гостиной", "في الصالون"),
    row("במרפסת", "On the balcony", "Sur le balcon", "На балконе", "على الشرفة"),
    row("עיצוב הדירה", "The apartment's design", "Décoration de l'appartement", "Дизайн квартиры", "تصميم الشقة"),
    row("רעיון להמחשה", "An idea, for illustration", "Une idée, à titre indicatif", "Идея для иллюстрации", "فكرة للتوضيح"),
    row("כמו במסירה", "As handed over", "Comme à la livraison", "Как при сдаче", "كما عند التسليم"),
    row("ריק, אריחים בהירים", "Empty, light tiles", "Vide, carrelage clair", "Без мебели, светлая плитка", "دون أثاث، بلاط فاتح"),
    row("עץ חם", "Warm wood", "Bois chaleureux", "Тёплое дерево", "خشب دافئ"),
    row("פרקט אלון, מטבח אגוז, פשתן", "Oak parquet, walnut kitchen, linen", "Parquet en chêne, cuisine en noyer, lin", "Дубовый паркет, кухня из ореха, лён", "باركيه بلوط، مطبخ جوز، كتان"),
    row("בהיר", "Light", "Clair", "Светлый", "فاتح"),
    row("אלון לבן, מטבח מרווה", "White oak, sage kitchen", "Chêne blanc, cuisine vert sauge", "Белый дуб, кухня цвета шалфея", "بلوط أبيض، مطبخ بلون المريمية"),
    row("אבן", "Stone", "Pierre", "Камень", "حجر"),
    row("אבן אפורה, עור קוניאק", "Grey stone, cognac leather", "Pierre grise, cuir cognac", "Серый камень, кожа цвета коньяка", "حجر رمادي، جلد بلون الكونياك"),
    row("הדירה לדוגמה מבפנים", "The example apartment from the inside", "L'appartement témoin de l'intérieur", "Квартира-пример изнутри", "الشقة النموذجية من الداخل"),
    # --- the page's stage parts printed by the server (inc/project-stage.php)
    # the hero's kicker: one text node after the developer's <b> (" · " + the place)
    row("· רובע שדה דב, צפון תל אביב", "· Sde Dov quarter, North Tel Aviv", "· Quartier de Sde Dov, nord de Tel Aviv", "· Район Сде-Дов, север Тель-Авива", "· حي سديه دوف، شمال تل أبيب"),
    row("· אבן גבירול פינת ארלוזורוב, מתחם סומייל", "· Ibn Gabirol corner of Arlozorov, the Sumail compound", "· Angle Ibn Gabirol et Arlozorov, complexe Sumail", "· Угол улиц Ибн Гвироль и Арлозоров, комплекс Сумейль", "· زاوية ابن جبيرول وأرلوزوروف، مجمّع سُميل"),
    row("· מתחם אשכול, רובע שדה דב", "· The Eshkol compound, Sde Dov quarter", "· Complexe Eshkol, quartier de Sde Dov", "· Комплекс Эшколь, район Сде-Дов", "· مجمّع أشكول، حي سديه دوف"),
    row("רובע שדה דב, צפון תל אביב", "Sde Dov quarter, North Tel Aviv", "Quartier de Sde Dov, nord de Tel Aviv", "Район Сде-Дов, север Тель-Авива", "حي سديه دوف، شمال تل أبيب"),
    row("אבן גבירול פינת ארלוזורוב, מתחם סומייל", "Ibn Gabirol corner of Arlozorov, the Sumail compound", "Angle Ibn Gabirol et Arlozorov, complexe Sumail", "Угол улиц Ибн Гвироль и Арлозоров, комплекс Сумейль", "زاوية ابن جبيرول وأرلوزوروف، مجمّع سُميل"),
    row("מתחם אשכול, רובע שדה דב", "The Eshkol compound, Sde Dov quarter", "Complexe Eshkol, quartier de Sde Dov", "Комплекс Эшколь, район Сде-Дов", "مجمّع أشكول، حي سديه دوف"),
    row("אבן גבירול פינת ארלוזורוב", "Ibn Gabirol corner of Arlozorov", "Angle Ibn Gabirol et Arlozorov", "Угол улиц Ибн Гвироль и Арлозоров", "زاوية ابن جبيرول وأرلوزوروف"),
    row("מתחם סומייל, תל אביב", "The Sumail compound, Tel Aviv", "Complexe Sumail, Tel Aviv", "Комплекс Сумейль, Тель-Авив", "مجمّع سُميل، تل أبيب"),
    row("לבחירת קומה", "Choose a floor", "Choisir un étage", "Выбрать этаж", "اختيار طابق"),
    row("שיחת וידאו עם נציג", "Video call with a representative", "Appel vidéo avec un conseiller", "Видеозвонок с представителем", "مكالمة فيديو مع ممثل"),
    row("סיור וירטואלי: הקומות והנוף", "Virtual tour: the floors and the view", "Visite virtuelle : les étages et la vue", "Виртуальный тур: этажи и вид", "جولة افتراضية: الطوابق والإطلالة"),
    row("בוחרים קומה", "Pick a floor", "Choisir l'étage", "Выбираем этаж", "نختار طابقاً"),
    row("נכנסים לדירה", "Step inside", "Entrer dans l'appartement", "Входим в квартиру", "ندخل إلى الشقة"),
    row("מעצבים את הדירה", "Design the apartment", "Aménager l'appartement", "Оформляем квартиру", "نصمّم الشقة"),
    row("קיים היום", "Standing today", "Existant aujourd'hui", "Уже построено", "قائم اليوم"),
    row("בשלב ההיתר", "At the permit stage", "Au stade du permis", "На стадии разрешения", "في مرحلة الترخيص"),
    row("מקורות הבמה: קו המגרש והבניינים הקיימים סביבו לפי עיריית",
        "3D model sources: the lot line and the existing buildings around it, per the Municipality of",
        "Sources du modèle 3D : le tracé du terrain et les immeubles existants alentour, selon la municipalité de",
        "Источники 3D-модели: граница участка и существующие здания вокруг — по данным муниципалитета города",
        "مصادر النموذج ثلاثي الأبعاد: حدود القسيمة والمباني القائمة حولها بحسب بلدية"),
    row("מקורות הבמה: קו המגרש, קווי המגדלים והבניינים הקיימים סביבם לפי עיריית",
        "3D model sources: the lot line, the towers' outlines and the existing buildings around them, per the Municipality of",
        "Sources du modèle 3D : le tracé du terrain, l'emprise des tours et les immeubles existants alentour, selon la municipalité de",
        "Источники 3D-модели: граница участка, контуры башен и существующие здания вокруг — по данным муниципалитета города",
        "مصادر النموذج ثلاثي الأبعاد: حدود القسيمة وخطوط البرجين والمباني القائمة حولها بحسب بلدية"),
    # the facts and the progress
    row("מיקום", "Location", "Emplacement", "Расположение", "الموقع"),
    row("בניינים", "Buildings", "Immeubles", "Здания", "المباني"),
    row("דירות", "Apartments", "Appartements", "Квартиры", "الشقق"),
    row("תמהיל", "Unit mix", "Typologies", "Состав квартир", "تشكيلة الشقق"),
    row("מחיר ממוצע", "Average price", "Prix moyen", "Средняя цена", "متوسط السعر"),
    row("מחיר", "Price", "Prix", "Цена", "السعر"),
    row("מצב", "Status", "Statut", "Статус", "الوضع"),
    row("חניה", "Parking", "Stationnement", "Парковка", "موقف السيارات"),
    row("גובה המגדל", "Tower height", "Hauteur de la tour", "Высота башни", "ارتفاع البرج"),
    row("מתקנים", "Facilities", "Équipements", "Инфраструктура", "المرافق"),
    row("ופנטהאוזים, לפי השיווק", "and penthouses, per the marketing", "et penthouses, selon la commercialisation", "и пентхаусы, по маркетинговым данным", "وبنتهاوسات، بحسب التسويق"),
    row("לפי היתר הבנייה", "Per the building permit", "Selon le permis de construire", "По разрешению на строительство", "بحسب رخصة البناء"),
    row("על גג מבנה הלובי", "On the roof of the lobby building", "Sur le toit du bâtiment du hall", "На крыше здания лобби", "على سطح مبنى الردهة"),
    row("בין שני המגדלים, לפי אתר היזם", "Between the two towers, per the developer's site", "Entre les deux tours, selon le site du promoteur", "Между двумя башнями, по данным сайта застройщика", "بين البرجين، بحسب موقع المطوّر"),
    row("לפי תכנית העיצוב", "Per the design plan", "Selon le plan d'aménagement", "По архитектурному плану", "بحسب مخطط التصميم"),
    row("מחיר הפתיחה שפורסם", "The published starting price", "Le prix de lancement publié", "Опубликованная стартовая цена", "سعر الافتتاح المنشور"),
    row("המכירה המוקדמת והבנייה החלו, לפי הפרסומים", "The pre-sale and the construction have started, per the publications", "La prévente et la construction ont commencé, selon les publications", "Предпродажа и строительство начались, по публикациям", "بدأ البيع المسبق والبناء، بحسب المنشورات"),
    row("בריכה וחדרי כושר", "A pool and gyms", "Piscine et salles de sport", "Бассейн и тренажёрные залы", "مسبح وصالات رياضية"),
    row("עכשיו", "Now", "Maintenant", "Сейчас", "الآن"),
    row("אכלוס", "Occupancy", "Livraison", "Заселение", "الإسكان"),
    row("תכנית", "Plan", "Plan", "План", "المخطط"),
    row("השלמה", "Completion", "Achèvement", "Завершение", "الإنجاز"),
    row("תכנית עיצוב", "Design plan", "Plan d'aménagement", "Архитектурный план", "مخطط التصميم"),
    row("דמרי רכשה את הפרויקט", "Dimri bought the project", "Dimri a racheté le projet", "Dimri купила проект", "اشترت Dimri المشروع"),
    row("שיווק ובנייה", "Sales and construction", "Commercialisation et construction", "Продажи и строительство", "التسويق والبناء"),
    row("יסודות", "Foundations", "Fondations", "Фундамент", "الأساسات"),
    row("עובדות בקצרה", "Facts at a glance", "L'essentiel en bref", "Коротко о главном", "حقائق باختصار"),
    row("שלב הפרויקט", "Project stage", "Étape du projet", "Этап проекта", "مرحلة المشروع"),
    # the view block and the area map (the chips; with a count they go through the chip pattern)
    row("הכל על מפה אחת: מחירים, סביבה, תוכניות עתידיות", "Everything on one map: prices, surroundings, future plans", "Tout sur une seule carte : prix, environs, projets futurs", "Всё на одной карте: цены, окрестности, будущие планы", "كل شيء على خريطة واحدة: الأسعار والمحيط والمخططات المستقبلية"),
    row("₪ מחירים בסביבה", "₪ Local prices", "₪ Prix du quartier", "₪ Цены в районе", "₪ أسعار المنطقة"),
    row("חינוך", "Education", "Éducation", "Образование", "التعليم"),
    row("פארקים", "Parks", "Parcs", "Парки", "الحدائق"),
    row("תחבורה", "Transport", "Transports", "Транспорт", "المواصلات"),
    row("קניות", "Shopping", "Commerces", "Магазины", "التسوق"),
    row("בריאות", "Health", "Santé", "Здоровье", "الصحة"),
    row("קפה ומסעדות", "Cafés and restaurants", "Cafés et restaurants", "Кафе и рестораны", "مقاهٍ ومطاعم"),
    row("◆ תוכניות עתידיות", "◆ Future plans", "◆ Plans futurs", "◆ Будущие планы", "◆ مخططات مستقبلية"),
    row("תלת ממד", "3D", "3D", "3D", "ثلاثي الأبعاد"),
    row("לוויין", "Satellite", "Satellite", "Спутник", "قمر صناعي"),
    row("לחצו על כל סימון לקבלת פרטים. תגי המחיר הם אומדן לא מחייב למ״ר בפרויקטים סמוכים.",
        "Click any marker for details. The price tags are a non-binding estimate per m² in nearby projects.",
        "Cliquez sur un repère pour les détails. Les étiquettes de prix sont une estimation non contractuelle au m² dans les projets voisins.",
        "Нажмите на любую метку, чтобы узнать подробности. Ценники — необязывающая оценка за м² в соседних проектах.",
        "انقروا على أي علامة للتفاصيل. بطاقات السعر تقدير غير ملزم للمتر المربع في المشاريع المجاورة."),
    row("◆ סגול = תוכניות התחדשות ופרויקטים עתידיים", "◆ Purple = urban renewal plans and future projects", "◆ Violet = plans de renouvellement urbain et projets futurs", "◆ Фиолетовый = планы обновления и будущие проекты", "◆ البنفسجي = مخططات تجديد عمراني ومشاريع مستقبلية"),
    row("מפה חיה של הסביבה", "Live map of the area", "Carte interactive du quartier", "Интерактивная карта района", "خريطة حية للمنطقة"),
    row("שכבות מפה", "Map layers", "Couches de la carte", "Слои карты", "طبقات الخريطة"),
    row("מה אפשר לעשות כאן", "What you can do here", "Ce que vous pouvez faire ici", "Что можно сделать здесь", "ما الذي يمكن فعله هنا"),
    row("אנשי מקצוע באזור", "Professionals in the area", "Professionnels du quartier", "Специалисты в районе", "مختصون في المنطقة"),
    # the surroundings band (catalog-plus-map.php)
    row("מה קורה מסביב", "What's happening nearby", "Ce qui se passe autour", "Что происходит вокруг", "ما الذي يحدث في المحيط"),
    row("הסביבה של הפרויקט", "The project's surroundings", "Les environs du projet", "Окрестности проекта", "محيط المشروع"),
    row("מה שקיים ומה שמתוכנן במרחק הליכה: תחבורה, חינוך, פארקים, בנייה ותוכניות. מקור: find-place, שכבות מידע עירוניות וממשלתיות.",
        "What exists and what is planned within walking distance: transport, education, parks, construction and plans. Source: find-place, municipal and government data layers.",
        "Ce qui existe et ce qui est prévu à distance de marche : transports, éducation, parcs, chantiers et plans. Source : find-place, couches de données municipales et gouvernementales.",
        "Что есть и что планируется в пешей доступности: транспорт, образование, парки, строительство и планы. Источник: find-place, муниципальные и государственные слои данных.",
        "ما هو قائم وما هو مخطط على مسافة سير: المواصلات والتعليم والحدائق والبناء والمخططات. المصدر: find-place، طبقات بيانات بلدية وحكومية."),
    row("פתיחת המפה עם המחירים מסביב", "Open the map with the prices around", "Ouvrir la carte avec les prix alentour", "Открыть карту с ценами вокруг", "افتحوا الخريطة مع الأسعار في المحيط"),
    row("רכבת קלה", "Light rail", "Tramway", "Лёгкое метро", "القطار الخفيف"),
    row("בתי ספר במרחק הליכה", "Schools within walking distance", "Écoles à distance de marche", "Школы в пешей доступности", "مدارس على مسافة سير"),
    row("גני ילדים", "Kindergartens", "Jardins d'enfants", "Детские сады", "رياض الأطفال"),
    row("פארקים וחופים", "Parks and beaches", "Parcs et plages", "Парки и пляжи", "حدائق وشواطئ"),
    row("בנייה מסביב", "Construction around", "Chantiers alentour", "Стройки вокруг", "البناء في المحيط"),
    row("תכנון עתידי", "Future planning", "Urbanisme futur", "Будущая застройка", "التخطيط المستقبلي"),
    row("בתוקף", "In force", "En vigueur", "Действует", "سارٍ"),
    row("מאושרת", "Approved", "Approuvé", "Утверждён", "مُصادَق عليه"),
    row("בהפקדה", "Deposited for objections", "Mis en dépôt", "Опубликован для возражений", "قيد الإيداع"),
    row("בתהליך", "In process", "En cours", "В процессе", "قيد الإجراء"),
    row("מוצעת", "Proposed", "Proposé", "Предложен", "مقترح"),
    row("· הפרויקט בתחום התוכנית", "· the project is within the plan", "· le projet est dans le périmètre du plan", "· проект находится в границах плана", "· المشروع ضمن حدود المخطط"),
    row("הפרויקט בתחום התוכנית", "the project is within the plan", "le projet est dans le périmètre du plan", "проект находится в границах плана", "المشروع ضمن حدود المخطط"),
    # the tools and the notice around the stage
    row("לפנייה ישירה ליזם", "Contact the developer directly", "Contacter directement le promoteur", "Связаться с застройщиком напрямую", "التواصل مباشرة مع المطوّر"),
    row("הכלים שלנו לבדיקת הפרויקט", "Our tools for checking the project", "Nos outils pour vérifier le projet", "Наши инструменты для проверки проекта", "أدواتنا لفحص المشروع"),
    row("מעצב הדירות שלנו", "Our apartment designer", "Notre outil d'aménagement", "Наш дизайнер квартир", "مصمّم الشقق لدينا"),
    row("בודקים ריהוט, מידות ומרחקים", "Check furniture, sizes and distances", "Vérifiez mobilier, dimensions et distances", "Проверяем мебель, размеры и расстояния", "نفحص الأثاث والمقاسات والمسافات"),
    row("סיור תלת ממדי ברובע", "A 3D tour of the quarter", "Visite 3D du quartier", "3D-тур по району", "جولة ثلاثية الأبعاد في الحي"),
    row("הסביבה של הפרויקט, בהפקת נדלן", "The project's surroundings, produced by NadLan", "Les environs du projet, réalisés par NadLan", "Окрестности проекта, в исполнении NadLan", "محيط المشروع، من إنتاج NadLan"),
    row("טיסה מעל האזור", "Fly over the area", "Survol du quartier", "Полёт над районом", "تحليق فوق المنطقة"),
    row("הדמיית כדור הארץ שלנו", "Our globe view", "Notre globe 3D", "Наш 3D-глобус", "مجسّم الكرة الأرضية لدينا"),
    row("אתר עצמאי", "Independent site", "Site indépendant", "Независимый сайт", "موقع مستقل"),
    row("כלי הבדיקה של נדלן", "NadLan's checking tools", "Les outils de vérification de NadLan", "Инструменты проверки NadLan", "أدوات الفحص من NadLan"),
    # --- DuoRooms v92 (1.72.353): the notes of DUO's 360 rooms
    row("הנפח הבהיר הוא אייץ׳ אינפיניטי, שנמצא בבנייה, בגובה לפי מספר הקומות.",
        "The pale mass is H Infinity, under construction, drawn to its number of floors.",
        "La masse claire est H Infinity, en construction, dessinée selon son nombre d'étages.",
        "Светлый объём — H Infinity, он строится и показан по числу этажей.",
        "الكتلة الفاتحة هي H Infinity قيد البناء، مرسومة حسب عدد طوابقها."),
    row("הדירה הזו במגדל הדרומי: החזית הדרומית של המגדל הצפוני פונה אל המגדל הדרומי.",
        "This apartment is in the south tower: the north tower's south face looks onto the south tower.",
        "Cet appartement est dans la tour sud : la façade sud de la tour nord fait face à la tour sud.",
        "Эта квартира в южной башне: южный фасад северной башни обращён к южной башне.",
        "هذه الشقة في البرج الجنوبي: الواجهة الجنوبية للبرج الشمالي تطل على البرج الجنوبي."),
]

# ---------------------------------------------------------------------------------------------------------------------
# PATTERNS (after lang-pages.json's): specific first, general last (the PHP pass stops at the first pattern that matches)
# ---------------------------------------------------------------------------------------------------------------------
# facility notes with numbers: shown on the card, and also after ROOM in the facility's 360 room caption
NOTE_PATS = [
    ("מקורות: אתר {X}, תכנית העיצוב ({D}).",
     "Sources: the {1} site, the design plan ({2}).", "Sources : le site {1}, le plan d'aménagement ({2}).",
     "Источники: сайт {1}, архитектурный план ({2}).", "المصادر: موقع {1}، مخطط التصميم ({2})."),
    ("צורת הבריכה ומקומה על הגג בדגם להמחשה. מקורות: אתר DUO, החלטת רשות הרישוי {R}.",
     "The pool's shape and its place on the roof in the model are an illustration. Sources: the DUO site, the licensing authority's decision {1}.",
     "La forme de la piscine et sa place sur le toit dans la maquette sont indicatives. Sources : le site DUO, la décision de l'autorité d'octroi des permis {1}.",
     "Форма бассейна и его место на крыше на модели условны. Источники: сайт DUO, решение органа выдачи разрешений {1}.",
     "شكل المسبح وموقعه على السطح في النموذج للتوضيح. المصادر: موقع DUO، قرار سلطة الترخيص {1}."),
    ("צורת הבריכה ומקומה על הגג בדגם להמחשה. מקורות: תכנית העיצוב למגרש {I}, פרסומי היזם.",
     "The pool's shape and its place on the roof in the model are an illustration. Sources: the design plan for lot {1}, the developer's publications.",
     "La forme de la piscine et sa place sur le toit dans la maquette sont indicatives. Sources : le plan d'aménagement du lot {1}, les publications du promoteur.",
     "Форма бассейна и его место на крыше на модели условны. Источники: архитектурный план участка {1}, публикации застройщика.",
     "شكل المسبح وموقعه على السطح في النموذج للتوضيح. المصادر: مخطط التصميم للقسيمة {1}، منشورات المطوّر."),
    ("באיזו מרפסת כל בריכה לא פורסם; המיקום בדגם להמחשה. מקור: החלטת רשות הרישוי {R}.",
     "Which balcony each pool is on has not been published; the position in the model is an illustration. Source: the licensing authority's decision {1}.",
     "Le balcon de chaque piscine n'a pas été rendu public ; l'emplacement dans la maquette est indicatif. Source : la décision de l'autorité d'octroi des permis {1}.",
     "На каком балконе какой бассейн, не опубликовано; расположение на модели условное. Источник: решение органа выдачи разрешений {1}.",
     "لم يُنشر على أيّ شرفة يقع كل مسبح؛ الموقع في النموذج للتوضيح. المصدر: قرار سلطة الترخيص {1}."),
    ("צורת המבנים ומקומם בחצי המערבי להמחשה. מקורות: החלטת רשות הרישוי {R}, דוח {X}.",
     "The buildings' shape and their place in the western half are an illustration. Sources: the licensing authority's decision {1}, the {2} report.",
     "La forme des bâtiments et leur place dans la moitié ouest sont indicatives. Sources : la décision de l'autorité d'octroi des permis {1}, rapport {2}.",
     "Форма зданий и их место в западной половине условны. Источники: решение органа выдачи разрешений {1}, отчёт {2}.",
     "شكل المباني وموقعها في النصف الغربي للتوضيح. المصادر: قرار سلطة الترخيص {1}، تقرير {2}."),
    ("מקום הכניסה לחניון לא פורסם; הסימון בדגם להמחשה. מקור: החלטת רשות הרישוי {R}.",
     "The car park entrance's location has not been published; the marking in the model is an illustration. Source: the licensing authority's decision {1}.",
     "L'emplacement de l'entrée du parking n'a pas été rendu public ; le repère dans la maquette est indicatif. Source : la décision de l'autorité d'octroi des permis {1}.",
     "Место въезда в паркинг не опубликовано; отметка на модели условна. Источник: решение органа выдачи разрешений {1}.",
     "لم يُنشر موقع مدخل موقف السيارات؛ العلامة في النموذج للتوضيح. المصدر: قرار سلطة الترخيص {1}."),
    ("באילו מרפסות הבריכות לא פורסם; המיקום בדגם להמחשה. מקור: תכנית העיצוב למגרש {I}.",
     "Which balconies the pools are on has not been published; the position in the model is an illustration. Source: the design plan for lot {1}.",
     "Les balcons des piscines n'ont pas été rendus publics ; l'emplacement dans la maquette est indicatif. Source : le plan d'aménagement du lot {1}.",
     "На каких балконах бассейны, не опубликовано; расположение на модели условное. Источник: архитектурный план участка {1}.",
     "لم يُنشر على أيّ الشرفات تقع المسابح؛ الموقع في النموذج للتوضيح. المصدر: مخطط التصميم للقسيمة {1}."),
    ("מקורות: תכנית העיצוב למגרש {I}, פרסומי היזם.",
     "Sources: the design plan for lot {1}, the developer's publications.", "Sources : le plan d'aménagement du lot {1}, les publications du promoteur.",
     "Источники: архитектурный план участка {1}, публикации застройщика.", "المصادر: مخطط التصميم للقسيمة {1}، منشورات المطوّر."),
    ("מקום הכניסות בדגם להמחשה. מקור: תכנית העיצוב למגרש {I}.",
     "The entrances' position in the model is an illustration. Source: the design plan for lot {1}.",
     "L'emplacement des entrées dans la maquette est indicatif. Source : le plan d'aménagement du lot {1}.",
     "Расположение входов на модели условное. Источник: архитектурный план участка {1}.",
     "موقع المداخل في النموذج للتوضيح. المصدر: مخطط التصميم للقسيمة {1}."),
    ("עיצוב הגינה בדגם להמחשה. מקור: תכנית העיצוב למגרש {I}.",
     "The garden's design in the model is an illustration. Source: the design plan for lot {1}.",
     "Le dessin du jardin dans la maquette est indicatif. Source : le plan d'aménagement du lot {1}.",
     "Оформление сада на модели условное. Источник: архитектурный план участка {1}.",
     "تصميم الحديقة في النموذج للتوضيح. المصدر: مخطط التصميم للقسيمة {1}."),
    ("מקום פתח הרמפה בדגם להמחשה. מקור: תכנית העיצוב למגרש {I}.",
     "The ramp opening's position in the model is an illustration. Source: the design plan for lot {1}.",
     "L'emplacement de l'ouverture de la rampe dans la maquette est indicatif. Source : le plan d'aménagement du lot {1}.",
     "Расположение въезда на рампу на модели условное. Источник: архитектурный план участка {1}.",
     "موقع فتحة المنحدر في النموذج للتوضيح. المصدر: مخطط التصميم للقسيمة {1}."),
    ("מקום החצר האנגלית בדגם להמחשה. מקורות: תכנית העיצוב למגרש {I}, אתר היזם.",
     "The sunken light court's position in the model is an illustration. Sources: the design plan for lot {1}, the developer's site.",
     "L'emplacement de la cour anglaise dans la maquette est indicatif. Sources : le plan d'aménagement du lot {1}, le site du promoteur.",
     "Расположение английского дворика на модели условное. Источники: архитектурный план участка {1}, сайт застройщика.",
     "موقع الفناء الغائر في النموذج للتوضيح. المصادر: مخطط التصميم للقسيمة {1}، موقع المطوّر."),
    ("המקום בקומת הקרקע של כל בניין בדגם להמחשה. מקורות: תכנית העיצוב למגרש {I}, אתר היזם.",
     "The place on each building's ground floor in the model is an illustration. Sources: the design plan for lot {1}, the developer's site.",
     "L'emplacement au rez-de-chaussée de chaque immeuble dans la maquette est indicatif. Sources : le plan d'aménagement du lot {1}, le site du promoteur.",
     "Место на первом этаже каждого здания на модели условное. Источники: архитектурный план участка {1}, сайт застройщика.",
     "المكان في الطابق الأرضي لكل مبنى في النموذج للتوضيح. المصادر: مخطط التصميم للقسيمة {1}، موقع المطوّر."),
    ("מקום החצר בדגם להמחשה. מקור: תכנית העיצוב למגרש {I}.",
     "The yard's position in the model is an illustration. Source: the design plan for lot {1}.",
     "L'emplacement de la cour dans la maquette est indicatif. Source : le plan d'aménagement du lot {1}.",
     "Расположение двора на модели условное. Источник: архитектурный план участка {1}.",
     "موقع الساحة في النموذج للتوضيح. المصدر: مخطط التصميم للقسيمة {1}."),
    ("עיצוב החצר בדגם להמחשה. מקור: תכנית העיצוב למגרש {I}.",
     "The courtyard's design in the model is an illustration. Source: the design plan for lot {1}.",
     "Le dessin de la cour dans la maquette est indicatif. Source : le plan d'aménagement du lot {1}.",
     "Оформление двора на модели условное. Источник: архитектурный план участка {1}.",
     "تصميم الساحة في النموذج للتوضيح. المصدر: مخطط التصميم للقسيمة {1}."),
    ("מקור: תכנית העיצוב למגרש {I}.",
     "Source: the design plan for lot {1}.", "Source : le plan d'aménagement du lot {1}.",
     "Источник: архитектурный план участка {1}.", "المصدر: مخطط التصميم للقسيمة {1}."),
    ("מקור: אתר {X}.",
     "Source: the {1} site.", "Source : le site {1}.", "Источник: сайт {1}.", "المصدر: موقع {1}."),
]

PATTERNS = [
    # --- the floor card (stage.js: the floor, its line; bridge.js: the button into the room)
    # --- BuildingWalk v96: the building's places and stops
    pat("הדירה · קומה {I}", "The apartment · floor {1}", "L'appartement · étage {1}", "Квартира · этаж {1}", "الشقة · الطابق {1}"),
    pat("המגדל הצפוני · קומה {I}", "The north tower · floor {1}", "La tour nord · étage {1}", "Северная башня · этаж {1}", "البرج الشمالي · الطابق {1}"),
    pat("המגדל הדרומי · קומה {I}", "The south tower · floor {1}", "La tour sud · étage {1}", "Южная башня · этаж {1}", "البرج الجنوبي · الطابق {1}"),
    pat("המעליות · לדירה בקומה {I}", "The lifts · to the apartment on floor {1}", "Les ascenseurs · vers l'appartement au {1}e étage", "Лифты · к квартире на {1}-м этаже", "المصاعد · إلى الشقة في الطابق {1}"),
    # --- AreaLife v97: counts and walking minutes
    pat("{I} בכיוון הזה", "{1} this way", "{1} dans cette direction", "{1} в этом направлении", "{1} في هذا الاتجاه"),
    pat("{I} דק׳ הליכה", "{1} min walk", "{1} min à pied", "{1} мин пешком", "{1} دقيقة سيرًا"),
    pat("{I} דק׳", "{1} min", "{1} min", "{1} мин", "{1} د"),
    pat("קומה {I}", "Floor {1}", "Étage {1}", "Этаж {1}", "الطابق {1}"),
    pat("להיכנס לדירה · מקומה {I}", "Enter the apartment · from floor {1}", "Entrer dans l'appartement · depuis l'étage {1}", "Войти в квартиру · с {1}-го этажа", "الدخول إلى الشقة · من الطابق {1}"),
    pat("פונה {X} ·", "Facing {1} ·", "Orienté {1} ·", "Ориентация: {1} ·", "باتجاه {1} ·"),
    pat("בקומות עד {I} בערך יש גם דירות {I} חדרים, לפי היזם",
        "Up to about floor {1} there are also {2}-room apartments, per the developer",
        "Jusqu'à l'étage {1} environ, il y a aussi des appartements de {2} pièces, selon le promoteur",
        "Примерно до {1}-го этажа есть и {2}-комнатные квартиры, по данным застройщика",
        "حتى الطابق {1} تقريباً توجد أيضاً شقق من {2} غرف، بحسب المطوّر"),
    pat("בפרויקט דירות {I} עד {I} חדרים, לפי פרסומי השיווק",
        "The project has {1}- to {2}-room apartments, per the marketing materials",
        "Le projet compte des appartements de {1} à {2} pièces, selon les supports commerciaux",
        "В проекте квартиры от {1} до {2} комнат, по маркетинговым материалам",
        "في المشروع شقق من {1} إلى {2} غرف، بحسب المواد التسويقية"),
    pat("דירות {I} עד {I} חדרים ופנטהאוזים, לפי אתר הפרויקט",
        "{1}- to {2}-room apartments and penthouses, per the project's site",
        "Appartements de {1} à {2} pièces et penthouses, selon le site du projet",
        "Квартиры от {1} до {2} комнат и пентхаусы, по данным сайта проекта",
        "شقق من {1} إلى {2} غرف وبنتهاوسات، بحسب موقع المشروع"),
    pat("קומות הפנטהאוזים ({I} עד {I}), עם בריכות פרטיות בקומות {I} ו־{I}, לפי החלטת רשות הרישוי ({D})",
        "Penthouse floors ({1} to {2}), with private pools on floors {3} and {4}, per the licensing authority's decision ({5})",
        "Étages des penthouses ({1} à {2}), avec piscines privées aux étages {3} et {4}, selon la décision de l'autorité d'octroi des permis ({5})",
        "Этажи пентхаусов (с {1} по {2}), с частными бассейнами на {3}-м и {4}-м этажах, по решению органа выдачи разрешений ({5})",
        "طوابق البنتهاوس ({1} إلى {2})، مع مسابح خاصة في الطابقين {3} و{4}، بحسب قرار سلطة الترخيص ({5})"),
    pat("בפרויקט {I} דירות, לפי פרסומי היזם",
        "{1} apartments in the project, per the developer's publications",
        "{1} appartements dans le projet, selon les publications du promoteur",
        "Квартир в проекте: {1}, по публикациям застройщика",
        "عدد الشقق في المشروع: {1}، بحسب منشورات المطوّر"),
    pat("שתי הקומות העליונות, עם בריכות פרטיות, לפי תכנית העיצוב ({D})",
        "The two top floors, with private pools, per the design plan ({1})",
        "Les deux derniers étages, avec piscines privées, selon le plan d'aménagement ({1})",
        "Два верхних этажа, с частными бассейнами, по архитектурному плану ({1})",
        "الطابقان العلويان، مع مسابح خاصة، بحسب مخطط التصميم ({1})"),
    pat("המגדלון: {I} קומות עם קומת הקרקע, מעל רמפת החניון, לפי תכנית העיצוב",
        "The mid-rise: {1} floors including the ground floor, above the car park ramp, per the design plan",
        "La petite tour : {1} étages rez-de-chaussée compris, au-dessus de la rampe du parking, selon le plan d'aménagement",
        "Малая башня: {1} эт. с учётом первого, над рампой паркинга, по архитектурному плану",
        "البرج الصغير: {1} طابقاً مع الطابق الأرضي، فوق منحدر موقف السيارات، بحسب مخطط التصميم"),
    pat("שתי הקומות העליונות במגדלון, עם בריכות פרטיות, לפי תכנית העיצוב ({D})",
        "The mid-rise's two top floors, with private pools, per the design plan ({1})",
        "Les deux derniers étages de la petite tour, avec piscines privées, selon le plan d'aménagement ({1})",
        "Два верхних этажа малой башни, с частными бассейнами, по архитектурному плану ({1})",
        "الطابقان العلويان في البرج الصغير، مع مسابح خاصة، بحسب مخطط التصميم ({1})"),
    pat("קומות הפנטהאוזים, בגובה של כ־{N} מ׳, לפי תכנית העיצוב ({D})",
        "The penthouse floors, about {1} m high, per the design plan ({2})",
        "Les étages des penthouses, d'environ {1} m de haut, selon le plan d'aménagement ({2})",
        "Этажи пентхаусов высотой около {1} м, по архитектурному плану ({2})",
        "طوابق البنتهاوس، بارتفاع نحو {1} م، بحسب مخطط التصميم ({2})"),
    pat("במגדל {I} דירות: {I} קטנות, {I} בינוניות ו־{I} גדולות, לפי תכנית העיצוב ({D})",
        "{1} apartments in the tower: {2} small, {3} medium and {4} large, per the design plan ({5})",
        "{1} appartements dans la tour : {2} petits, {3} moyens et {4} grands, selon le plan d'aménagement ({5})",
        "Квартир в башне: {1} — маленьких {2}, средних {3} и больших {4}, по архитектурному плану ({5})",
        "عدد الشقق في البرج: {1}، منها {2} صغيرة و{3} متوسطة و{4} كبيرة، بحسب مخطط التصميم ({5})"),
    pat("הבסיס המרקמי של הבניין; בבניין {I} דירות, לפי תכנית העיצוב ({D})",
        "The building's street-scale base; {1} apartments in the building, per the design plan ({2})",
        "La base de l'immeuble à l'échelle de la rue ; {1} appartements dans l'immeuble, selon le plan d'aménagement ({2})",
        "Малоэтажное основание здания; квартир в здании: {1}, по архитектурному плану ({2})",
        "القاعدة المنخفضة للمبنى؛ عدد الشقق في المبنى: {1}، بحسب مخطط التصميم ({2})"),
    pat("קומות המגדלון; בבניין {I} דירות, לפי תכנית העיצוב ({D})",
        "The mid-rise floors; {1} apartments in the building, per the design plan ({2})",
        "Les étages de la petite tour ; {1} appartements dans l'immeuble, selon le plan d'aménagement ({2})",
        "Этажи малой башни; квартир в здании: {1}, по архитектурному плану ({2})",
        "طوابق البرج الصغير؛ عدد الشقق في المبنى: {1}، بحسب مخطط التصميم ({2})"),
    # a sold apartment on this floor (the Hebrew page's floor card; the language pages leave the deals out)
    pat("בקומה הזו בבניין השני נמכרה במכירה המוקדמת דירת {I} חדרים, כ-{N} מ״ר, בכ-{N} מיליון ₪ ({D})",
        "On this floor of the second building, a {1}-room apartment of about {2} m² was sold in the pre-sale for about {3} million ₪ ({4})",
        "À cet étage du second immeuble, un appartement de {1} pièces d'environ {2} m² a été vendu en prévente pour environ {3} millions ₪ ({4})",
        "На этом этаже второго здания в предпродаже продана {1}-комнатная квартира площадью около {2} м² примерно за {3} млн ₪ ({4})",
        "في هذا الطابق من المبنى الثاني بيعت في البيع المسبق شقة من {1} غرف، نحو {2} م²، بنحو {3} مليون ₪ ({4})"),
    pat("בקומה הזו נמכרה דירת {I} חדרים, {N} מ״ר, ביותר מ-{N} מיליון ₪ ({D})",
        "On this floor, a {1}-room apartment of {2} m² was sold for more than {3} million ₪ ({4})",
        "À cet étage, un appartement de {1} pièces de {2} m² a été vendu plus de {3} millions ₪ ({4})",
        "На этом этаже продана {1}-комнатная квартира площадью {2} м² более чем за {3} млн ₪ ({4})",
        "في هذا الطابق بيعت شقة من {1} غرف، {2} م²، بأكثر من {3} مليون ₪ ({4})"),
    pat("בקומה הזו נמכרה דירת {I} חדרים, {N} מ״ר, ב-{N} מיליון ₪ ({D})",
        "On this floor, a {1}-room apartment of {2} m² was sold for {3} million ₪ ({4})",
        "À cet étage, un appartement de {1} pièces de {2} m² a été vendu {3} millions ₪ ({4})",
        "На этом этаже продана {1}-комнатная квартира площадью {2} м² за {3} млн ₪ ({4})",
        "في هذا الطابق بيعت شقة من {1} غرف، {2} م²، بـ{3} مليون ₪ ({4})"),
    pat("בקומה הזו נמכרה דירת חדר, {N} מ״ר, ב-{N} מיליון ₪ ({D})",
        "On this floor, a one-room apartment of {1} m² was sold for {2} million ₪ ({3})",
        "À cet étage, un studio de {1} m² a été vendu {2} millions ₪ ({3})",
        "На этом этаже продана однокомнатная квартира площадью {1} м² за {2} млн ₪ ({3})",
        "في هذا الطابق بيعت شقة من غرفة واحدة، {1} م²، بـ{2} مليون ₪ ({3})"),
    # --- the view panel (bridge.js)
    pat("הדמיה להמחשה בלבד: מבט משוער מגובה של כ־{N} מ׳, לפי מפה. אינו צילום מהדירה.",
        "Illustration only: an estimated view from a height of about {1} m, based on a map. Not a photo from the apartment.",
        "Illustration uniquement : vue estimée depuis une hauteur d'environ {1} m, d'après une carte. Ce n'est pas une photo prise depuis l'appartement.",
        "Только иллюстрация: примерный вид с высоты около {1} м, по карте. Это не фотография из квартиры.",
        "تصور توضيحي فقط: إطلالة تقديرية من ارتفاع نحو {1} م، بحسب الخريطة. ليست صورة من الشقة."),
    pat("מרחק בקו אווירי מהבניין, לפי המפה; זמן ההליכה משוער. מקור: נתוני עיריית תל אביב-יפו ו-OpenStreetMap, {D}; הפרויקטים לפי העמודים שלהם באתר.",
        "Straight-line distance from the building, per the map; the walking time is an estimate. Source: Tel Aviv-Yafo Municipality data and OpenStreetMap, {1}; the projects per their pages on the site.",
        "Distance à vol d'oiseau depuis l'immeuble, d'après la carte ; le temps de marche est estimé. Source : données de la municipalité de Tel Aviv-Jaffa et OpenStreetMap, {1} ; les projets d'après leurs pages sur le site.",
        "Расстояние по прямой от здания, по карте; время в пути пешком приблизительное. Источник: данные муниципалитета Тель-Авива-Яффо и OpenStreetMap, {1}; проекты — по их страницам на сайте.",
        "المسافة بخط مستقيم من المبنى، بحسب الخريطة؛ مدة المشي تقديرية. المصدر: بيانات بلدية تل أبيب يافا وOpenStreetMap، {1}؛ المشاريع بحسب صفحاتها في الموقع."),
    pat("כ־{N} דק׳ הליכה · {X}", "About {1} min walk · {2}", "Environ {1} min à pied · {2}", "Около {1} мин пешком · {2}", "نحو {1} د مشياً · {2}"),
    pat("כ־{N} דק׳ הליכה", "About {1} min walk", "Environ {1} min à pied", "Около {1} мин пешком", "نحو {1} د مشياً"),
    pat("{N} ק״מ", "{1} km", "{1} km", "{1} км", "{1} كم"),  # lang-pages.json's km pattern has a \" the browser's 'u' flag refuses
    # --- the quarter's card (stage.js): the distance line, the facts, the button
    # "{N} מ׳ מריינבו, ..." the whole "from <project>" word is the capture (EXACT below), so French can elide (d'Ashira)
    pat("{N} מ׳ {F}, כ-{N} דקות הליכה, {X}",
        "{1} m {2}, about {3} min walk, {4}", "À {1} m {2}, environ {3} min à pied, {4}",
        "{1} м {2}, около {3} мин пешком, {4}", "على بعد {1} م {2}، نحو {3} د مشياً، {4}"),
    pat("{N} מ׳ {F}, כ-{N} דקות הליכה",
        "{1} m {2}, about {3} min walk", "À {1} m {2}, environ {3} min à pied",
        "{1} м {2}, около {3} мин пешком", "على بعد {1} م {2}، نحو {3} د مشياً"),
    pat("{N} מ׳ {F}, {X}", "{1} m {2}, {3}", "À {1} m {2}, {3}", "{1} м {2}, {3}", "على بعد {1} م {2}، {3}"),
    pat("{N} מ׳ {G}", "{1} m {2}", "À {1} m {2}", "{1} м {2}", "على بعد {1} م {2}"),
    pat("מה רואים מ־{X} לכיוונו", "The view from {1} towards it", "La vue depuis {1} dans sa direction", "Вид из {1} в эту сторону", "الإطلالة من {1} باتجاهه"),
    pat("מה רואים מ{X} לכיוונו", "The view from {1} towards it", "La vue depuis {1} dans sa direction", "Вид из {1} в эту сторону", "الإطلالة من {1} باتجاهه"),
    pat("{I} קומות · {I} דירות", "{1} floors · {2} apartments", "{1} étages · {2} appartements", "Этажей: {1} · квартир: {2}", "الطوابق: {1} · الشقق: {2}"),
    pat("{I} קומות", "{1} floors", "{1} étages", "Этажей: {1}", "الطوابق: {1}"),
    pat("{I} דירות", "{1} apartments", "{1} appartements", "Квартир: {1}", "الشقق: {1}"),
    pat("אכלוס צפוי {I}, לפי עמוד הפרויקט", "Occupancy expected in {1}, per the project's page", "Livraison prévue en {1}, selon la page du projet", "Заселение ожидается в {1} году, по странице проекта", "الإسكان متوقع في {1}، بحسب صفحة المشروع"),
    pat("find-place, נתוני עיריית תל אביב-יפו ו-OpenStreetMap, {D}",
        "find-place, Tel Aviv-Yafo Municipality data and OpenStreetMap, {1}",
        "find-place, données de la municipalité de Tel Aviv-Jaffa et OpenStreetMap, {1}",
        "find-place, данные муниципалитета Тель-Авива-Яффо и OpenStreetMap, {1}",
        "find-place، بيانات بلدية تل أبيب يافا وOpenStreetMap، {1}"),
    pat("גבול המגרש מצפון לפי החלטת רשות הרישוי ({D}); השטח לפי שכבת המגרשים של העירייה (תכנית {I})",
        "The lot's northern boundary per the licensing authority's decision ({1}); the area per the municipality's lots layer (plan {2})",
        "La limite nord du terrain selon la décision de l'autorité d'octroi des permis ({1}) ; la surface selon la couche des terrains de la municipalité (plan {2})",
        "Северная граница участка — по решению органа выдачи разрешений ({1}); территория — по слою участков муниципалитета (план {2})",
        "الحد الشمالي للقسيمة بحسب قرار سلطة الترخيص ({1})؛ المساحة بحسب طبقة القسائم في البلدية (المخطط {2})"),
    pat("שכבת המבנים של עיריית תל אביב-יפו (מבנה ציבור, {I} קומות, {I}); החיבור אליו במרתף לפי החלטת רשות הרישוי ({D})",
        "The Tel Aviv-Yafo Municipality's buildings layer (public building, {1} floors, {2}); the basement link to it per the licensing authority's decision ({3})",
        "La couche des bâtiments de la municipalité de Tel Aviv-Jaffa (bâtiment public, {1} étages, {2}) ; la liaison en sous-sol selon la décision de l'autorité d'octroi des permis ({3})",
        "Слой зданий муниципалитета Тель-Авива-Яффо (общественное здание, этажей: {1}, {2}); подземный переход к нему — по решению органа выдачи разрешений ({3})",
        "طبقة المباني في بلدية تل أبيب يافا (مبنى عام، {1} طابقاً، {2})؛ الربط به في القبو بحسب قرار سلطة الترخيص ({3})"),
    pat("עמוד הפרויקט באתר; המגרש לפי עיריית תל אביב-יפו (מגרש {I})",
        "The project's page on the site; the lot per the Tel Aviv-Yafo Municipality (lot {1})",
        "La page du projet sur le site ; le terrain selon la municipalité de Tel Aviv-Jaffa (lot {1})",
        "Страница проекта на сайте; участок — по данным муниципалитета Тель-Авива-Яффо (участок {1})",
        "صفحة المشروع في الموقع؛ القسيمة بحسب بلدية تل أبيب يافا (القسيمة {1})"),
    # --- the facilities' lines with numbers (facilities.json)
    pat("לפי תכנית העיצוב שאושרה ב־{D}: שתי בריכות שחייה על גגות של שני בנייני בוטיק.",
        "Per the design plan approved on {1}: two swimming pools on the roofs of two boutique buildings.",
        "Selon le plan d'aménagement approuvé le {1} : deux piscines sur les toits de deux immeubles boutique.",
        "По архитектурному плану, утверждённому {1}: два плавательных бассейна на крышах двух бутик-домов.",
        "بحسب مخطط التصميم المصادق عليه في {1}: مسبحان على سطحي مبنيين من مباني البوتيك."),
    pat("לפי תכנית העיצוב: {N} מ״ר לשימוש הדיירים בקומת הקרקע ובקומת הבסיס של המגדל.",
        "Per the design plan: {1} m² for the residents' use on the ground floor and the tower's base floor.",
        "Selon le plan d'aménagement : {1} m² à l'usage des résidents au rez-de-chaussée et au niveau de socle de la tour.",
        "По архитектурному плану: {1} м² для жильцов на первом этаже и на этаже основания башни.",
        "بحسب مخطط التصميم: {1} م² لاستخدام السكان في الطابق الأرضي وطابق القاعدة في البرج."),
    pat("לפי תכנית העיצוב: קומת קרקע מסחרית, בגובה של עד {N} מטרים.",
        "Per the design plan: a commercial ground floor, up to {1} metres high.",
        "Selon le plan d'aménagement : un rez-de-chaussée commercial, d'une hauteur allant jusqu'à {1} mètres.",
        "По архитектурному плану: торговый первый этаж высотой до {1} метров.",
        "بحسب مخطط التصميم: طابق أرضي تجاري بارتفاع يصل إلى {1} أمتار."),
    pat("לפי החלטת רשות הרישוי ({D}): בקומה {I} למגורים שטחי הדיירים, בריכת הפעוטות ופרגולת הצללה לבריכה.",
        "Per the licensing authority's decision ({1}): on residential floor {2}, the residents' areas, the toddlers' pool and a shading pergola for the pool.",
        "Selon la décision de l'autorité d'octroi des permis ({1}) : au niveau résidentiel {2}, les espaces des résidents, la pataugeoire et une pergola d'ombrage pour la piscine.",
        "По решению органа выдачи разрешений ({1}): на {2}-м жилом этаже — помещения для жильцов, бассейн для малышей и затеняющая пергола для бассейна.",
        "بحسب قرار سلطة الترخيص ({1}): في الطابق السكني {2} مساحات السكان ومسبح الأطفال الصغار وعريشة تظليل للمسبح."),
    pat("לפי אתר היזם: לובי ראשי בגובה של כ־{N} מטרים, המחבר בין שני המגדלים כמו רחוב פנימי, ולובי בכל קומה.",
        "Per the developer's site: a main lobby about {1} metres high, connecting the two towers like an inner street, and a lobby on every floor.",
        "Selon le site du promoteur : un hall principal d'environ {1} mètres de haut, qui relie les deux tours comme une rue intérieure, et un hall à chaque étage.",
        "По данным сайта застройщика: главное лобби высотой около {1} метров, соединяющее две башни, как внутренняя улица, и лобби на каждом этаже.",
        "بحسب موقع المطوّر: ردهة رئيسية بارتفاع نحو {1} أمتار، تربط بين البرجين كشارع داخلي، وردهة في كل طابق."),
    pat("לפי החלטת רשות הרישוי ({D}): קומות הפנטהאוזים הן {I} עד {I}, והבריכות הפרטיות בקומות {I} ו־{I}.",
        "Per the licensing authority's decision ({1}): the penthouse floors are {2} to {3}, and the private pools are on floors {4} and {5}.",
        "Selon la décision de l'autorité d'octroi des permis ({1}) : les étages des penthouses vont du {2} au {3}, et les piscines privées sont aux étages {4} et {5}.",
        "По решению органа выдачи разрешений ({1}): этажи пентхаусов — с {2} по {3}, а частные бассейны — на {4}-м и {5}-м этажах.",
        "بحسب قرار سلطة الترخيص ({1}): طوابق البنتهاوس من {2} إلى {3}، والمسابح الخاصة في الطابقين {4} و{5}."),
    pat("לפי דוח החברה: מתחם מסחרי בן {I} קומות.",
        "Per the company's report: a {1}-storey retail complex.",
        "Selon le rapport de la société : un complexe commercial de {1} niveaux.",
        "По отчёту компании: {1}-этажный торговый комплекс.",
        "بحسب تقرير الشركة: مجمّع تجاري من {1} طوابق."),
    pat("לפי החלטת רשות הרישוי: {I} קומות מרתף מתחת למגרש.",
        "Per the licensing authority's decision: {1} basement floors beneath the lot.",
        "Selon la décision de l'autorité d'octroi des permis : {1} niveaux de sous-sol sous le terrain.",
        "По решению органа выдачи разрешений: подземных этажей под участком — {1}.",
        "بحسب قرار سلطة الترخيص: {1} طوابق تحت الأرض أسفل القسيمة."),
    pat("לפי תכנית העיצוב ({D}): בריכות השחייה ימוקמו על גג מבנה המלון או בתת הקרקע מתחתיו, והקומה התשיעית של המבנה היא קומת שירותי הדיירים עם בריכה.",
        "Per the design plan ({1}): the swimming pools will be on the roof of the hotel building or underground beneath it, and the building's ninth floor is the residents' services floor, with a pool.",
        "Selon le plan d'aménagement ({1}) : les piscines seront sur le toit du bâtiment de l'hôtel ou en sous-sol en dessous, et le neuvième étage du bâtiment est l'étage des services aux résidents, avec une piscine.",
        "По архитектурному плану ({1}): плавательные бассейны разместятся на крыше здания отеля или под землёй под ним, а девятый этаж здания — сервисный этаж для жильцов с бассейном.",
        "بحسب مخطط التصميم ({1}): ستقام المسابح على سطح مبنى الفندق أو تحت الأرض أسفله، والطابق التاسع من المبنى هو طابق خدمات السكان مع مسبح."),
    pat("לפי תכנית העיצוב: בשתי הקומות העליונות של המגדל ושל המגדלון בריכות פרטיות, וגובה הקומות האלה עד {N} מ׳.",
        "Per the design plan: private pools on the two top floors of the tower and of the mid-rise, and these floors are up to {1} m high.",
        "Selon le plan d'aménagement : des piscines privées aux deux derniers étages de la tour et de la petite tour, et ces étages ont une hauteur allant jusqu'à {1} m.",
        "По архитектурному плану: частные бассейны на двух верхних этажах башни и малой башни, а высота этих этажей — до {1} м.",
        "بحسب مخطط التصميم: مسابح خاصة في الطابقين العلويين للبرج وللبرج الصغير، وارتفاع هذين الطابقين حتى {1} م."),
    pat("לפי תכנית העיצוב: המבנה הדרום מזרחי, {I} קומות, משלב מלון ודירות, ולובי המלון בכניסה מדרום דרך קולונדה.",
        "Per the design plan: the south-eastern building, {1} floors, combines a hotel and apartments, and the hotel lobby is entered from the south through a colonnade.",
        "Selon le plan d'aménagement : le bâtiment sud-est, de {1} étages, associe un hôtel et des logements, et on entre dans le hall de l'hôtel par le sud, sous une colonnade.",
        "По архитектурному плану: юго-восточное здание ({1} этажей) сочетает отель и квартиры, а вход в лобби отеля — с юга, через колоннаду.",
        "بحسب مخطط التصميم: المبنى الجنوبي الشرقي، {1} طوابق، يجمع بين فندق وشقق، ومدخل ردهة الفندق من الجنوب عبر رواق أعمدة."),
    pat("לפי פרסומי היזם: כ־{N} חדרי מלון.",
        "Per the developer's publications: about {1} hotel rooms.",
        "Selon les publications du promoteur : environ {1} chambres d'hôtel.",
        "По публикациям застройщика: около {1} гостиничных номеров.",
        "بحسب منشورات المطوّر: نحو {1} غرفة فندقية."),
    pat("לפי תכנית העיצוב: מסחר בקומת הקרקע של המגדל, המגדלון ומבנה המלון, וקולונדה ברוחב {N} מ׳ ובגובה {N} מ׳ לאורך הרחובות במזרח ובדרום.",
        "Per the design plan: retail on the ground floor of the tower, the mid-rise and the hotel building, and a colonnade {1} m wide and {2} m high along the streets on the east and the south.",
        "Selon le plan d'aménagement : des commerces au rez-de-chaussée de la tour, de la petite tour et du bâtiment de l'hôtel, et une colonnade de {1} m de large et {2} m de haut le long des rues à l'est et au sud.",
        "По архитектурному плану: торговля на первом этаже башни, малой башни и здания отеля, и колоннада шириной {1} м и высотой {2} м вдоль улиц на востоке и юге.",
        "بحسب مخطط التصميم: متاجر في الطابق الأرضي للبرج والبرج الصغير ومبنى الفندق، ورواق أعمدة بعرض {1} م وارتفاع {2} م على امتداد الشوارع في الشرق والجنوب."),
    pat("לפי פרסומי היזם: כ־{N} מ״ר מסחר.",
        "Per the developer's publications: about {1} m² of retail.",
        "Selon les publications du promoteur : environ {1} m² de commerces.",
        "По публикациям застройщика: около {1} м² торговых площадей.",
        "بحسب منشورات المطوّر: نحو {1} م² من المتاجر."),
    pat("לפי תכנית העיצוב: {N} מ״ר שטח פתוח עם זיקת הנאה למעבר הציבור {I} שעות ביממה, בחיבור לשטחים הפתוחים השכנים.",
        "Per the design plan: {1} m² of open space with a public right of way {2} hours a day, connected to the neighbouring open spaces.",
        "Selon le plan d'aménagement : {1} m² d'espace ouvert avec une servitude de passage public {2} heures sur 24, reliés aux espaces ouverts voisins.",
        "По архитектурному плану: {1} м² открытого пространства с правом общественного прохода {2} часа в сутки, в связке с соседними открытыми пространствами.",
        "بحسب مخطط التصميم: {1} م² من المساحة المفتوحة مع حق مرور للجمهور {2} ساعة يومياً، متصلة بالمساحات المفتوحة المجاورة."),
    pat("לפי תכנית העיצוב: {I} קומות מרתף וגלריית אופניים; הרמפה נכנסת מהרחוב במזרח, מתחת למגדלון. {I} מקומות חניה בתקן {Q}.",
        "Per the design plan: {1} basement floors and a bicycle gallery; the ramp enters from the street on the east, under the mid-rise. {2} parking spaces at a {3} standard.",
        "Selon le plan d'aménagement : {1} niveaux de sous-sol et une galerie à vélos ; la rampe part de la rue à l'est, sous la petite tour. {2} places de stationnement selon la norme {3}.",
        "По архитектурному плану: подземные этажи ({1}) и галерея для велосипедов; рампа ведёт с улицы на востоке, под малой башней. Машино-мест: {2}, по норме {3}.",
        "بحسب مخطط التصميم: {1} طوابق تحت الأرض ورواق للدراجات؛ يدخل المنحدر من الشارع في الشرق، تحت البرج الصغير. {2} موقفاً للسيارات بمعيار {3}."),
    pat("לפי תכנית העיצוב: בתת הקרקע בריכת שחייה וחדרי כושר, וחצר אנגלית של עד {N} מ״ר וברוחב של עד {N} מ׳ מכניסה אליהם אור.",
        "Per the design plan: underground, a swimming pool and gyms, and a sunken light court of up to {1} m² and up to {2} m wide lets daylight into them.",
        "Selon le plan d'aménagement : en sous-sol, une piscine et des salles de sport, éclairées par une cour anglaise de {1} m² au plus et de {2} m de large au plus.",
        "По архитектурному плану: под землёй — плавательный бассейн и тренажёрные залы, а английский дворик площадью до {1} м² и шириной до {2} м даёт им дневной свет.",
        "بحسب مخطط التصميم: تحت الأرض مسبح وصالات رياضية، وفناء غائر بمساحة تصل إلى {1} م² وبعرض يصل إلى {2} م يُدخل إليها الضوء."),
    pat("לפי תכנית העיצוב: בקומת הקרקע של הבניין הצפון מערבי גן ילדים של {I} כיתות ושטח קהילתי, {N} מ״ר בסך הכול, עם חצר מגודרת ומוצללת של {N} מ״ר.",
        "Per the design plan: on the ground floor of the north-western building, a kindergarten of {1} classes and a community space, {2} m² in all, with a fenced and shaded yard of {3} m².",
        "Selon le plan d'aménagement : au rez-de-chaussée de l'immeuble nord-ouest, un jardin d'enfants de {1} classes et un espace communautaire, {2} m² au total, avec une cour clôturée et ombragée de {3} m².",
        "По архитектурному плану: на первом этаже северо-западного здания — детский сад (групп: {1}) и общественное помещение, всего {2} м², с огороженным затенённым двором площадью {3} м².",
        "بحسب مخطط التصميم: في الطابق الأرضي من المبنى الشمالي الغربي روضة أطفال (عدد الصفوف: {1}) ومساحة مجتمعية، {2} م² في المجموع، مع ساحة مسيّجة ومظللة مساحتها {3} م²."),
    pat("לפי תכנית העיצוב: חזית מסחרית במערב ובדרום, וקולונדה של {N} מ׳ לאורך כל החזית הדרומית; החנויות פונות בעיקר ללוי אשכול ולרחוב החדש.",
        "Per the design plan: a retail front on the west and the south, and a {1} m colonnade along the whole southern front; the shops face mainly Levi Eshkol and the new street.",
        "Selon le plan d'aménagement : une façade commerciale à l'ouest et au sud, et une colonnade de {1} m sur toute la façade sud ; les boutiques donnent surtout sur Levi Eshkol et sur la nouvelle rue.",
        "По архитектурному плану: торговый фронт на западе и юге и колоннада шириной {1} м вдоль всего южного фасада; магазины выходят в основном на Леви Эшколя и на новую улицу.",
        "بحسب مخطط التصميم: واجهة تجارية في الغرب والجنوب، ورواق أعمدة بعرض {1} م على طول الواجهة الجنوبية كلها؛ المتاجر تطل أساساً على ليفي أشكول والشارع الجديد."),
    pat("לפי תכנית העיצוב: קומות מרתף על {N}% משטח המגרש, והרמפה נפתחת בחזית הבניין הצפון מערבי, בתוך הבניין. מספר קומות המרתף לא פורסם בטקסט שנקרא.",
        "Per the design plan: basement floors under {1}% of the lot's area, and the ramp opens in the front of the north-western building, inside the building. The number of basement floors was not published in the text that was read.",
        "Selon le plan d'aménagement : des niveaux de sous-sol sous {1} % de la surface du terrain, et la rampe s'ouvre sur la façade de l'immeuble nord-ouest, à l'intérieur de l'immeuble. Le nombre de niveaux de sous-sol n'est pas publié dans le texte consulté.",
        "По архитектурному плану: подземные этажи под {1}% площади участка, а рампа открывается на фасаде северо-западного здания, внутри здания. Число подземных этажей в прочитанном тексте не опубликовано.",
        "بحسب مخطط التصميم: طوابق تحت الأرض على {1}% من مساحة القسيمة، ويُفتح المنحدر في واجهة المبنى الشمالي الغربي، داخل المبنى. لم يُنشر عدد الطوابق تحت الأرض في النص الذي قُرئ."),
    pat("חניון: {I} קומות מרתף", "Car park: {1} basement floors", "Parking : {1} niveaux de sous-sol", "Паркинг: подземных этажей — {1}", "موقف السيارات: {1} طوابق تحت الأرض"),
    # --- the floor slice (slice.js)
    pat("גובה העין כ־{N} מ׳ מהרחוב · {X}",
        "Eye level about {1} m above the street · {2}", "Hauteur des yeux à environ {1} m au-dessus de la rue · {2}",
        "Уровень глаз — около {1} м над улицей · {2}", "مستوى النظر نحو {1} م فوق الشارع · {2}"),
    pat("תוכנית להמחשה של קומה {I}", "Illustrative plan of floor {1}", "Plan indicatif de l'étage {1}", "Условный план {1}-го этажа", "مخطط توضيحي للطابق {1}"),
    pat("קומה {I} · {X} · קומות הפנטהאוז", "Floor {1} · {2} · penthouse floors", "Étage {1} · {2} · étages des penthouses", "Этаж {1} · {2} · этажи пентхаусов", "الطابق {1} · {2} · طوابق البنتهاوس"),
    pat("קומה {I} · במרפסת, {X}", "Floor {1} · on the balcony, {2}", "Étage {1} · sur le balcon, {2}", "Этаж {1} · на балконе, {2}", "الطابق {1} · على الشرفة، {2}"),
    # --- the tour card and the 360 room's titles (inc/project-stage.php)
    pat("קומות {L} ו־{I}, בארבעת הכיוונים", "Floors {1} and {2}, in all four directions", "Étages {1} et {2}, dans les quatre directions", "Этажи {1} и {2}, во всех четырёх направлениях", "الطوابق {1} و{2}، في الاتجاهات الأربعة"),
    pat("קומה {I}, בארבעת הכיוונים", "Floor {1}, in all four directions", "Étage {1}, dans les quatre directions", "Этаж {1}, во всех четырёх направлениях", "الطابق {1}، في الاتجاهات الأربعة"),
    pat("קומות {L} ו־{I} · {X}", "Floors {1} and {2} · {3}", "Étages {1} et {2} · {3}", "Этажи {1} и {2} · {3}", "الطوابق {1} و{2} · {3}"),
    pat("הסלון בדירה לדוגמה בקומה {I}, מבט אל הים (הדמיה)",
        "The living room of the example apartment on floor {1}, looking out to sea (illustration)",
        "Le salon de l'appartement témoin au {1}e étage, vue sur la mer (illustration)",
        "Гостиная квартиры-примера на {1}-м этаже, вид на море (иллюстрация)",
        "صالون الشقة النموذجية في الطابق {1}، إطلالة على البحر (تصور توضيحي)"),
    # --- the page's stage parts printed by the server
    pat("המצב של כל פרויקט לפי העמוד שלו באתר, {D}. שנת אכלוס מוצגת רק כשהעמוד נותן אותה.",
        "Each project's status per its page on the site, {1}. An occupancy year is shown only when the page gives one.",
        "Le statut de chaque projet d'après sa page sur le site, {1}. L'année de livraison n'est indiquée que si la page la donne.",
        "Статус каждого проекта — по его странице на сайте, {1}. Год заселения показан, только если он указан на странице.",
        "حالة كل مشروع بحسب صفحته في الموقع، {1}. تُعرض سنة الإسكان فقط عندما تذكرها الصفحة."),
    pat("(שכבות התוכניות והמבנים, {D}); הפרויקטים ברובע לפי העמודים שלהם באתר.",
        "(the plans and buildings layers, {1}); the quarter's projects per their pages on the site.",
        "(couches des plans et des bâtiments, {1}) ; les projets du quartier d'après leurs pages sur le site.",
        "(слои планов и зданий, {1}); проекты района — по их страницам на сайте.",
        "(طبقات المخططات والمباني، {1})؛ مشاريع الحي بحسب صفحاتها في الموقع."),
    pat("(שכבות המגרשים, המבנים, הרחובות, השטחים הירוקים והעצים, {D}). הגבהים, החזית ומיקום המתקנים להמחשה.",
        "(the lots, buildings, streets, green areas and trees layers, {1}). The heights, the facade and the facilities' positions are an illustration.",
        "(couches des terrains, bâtiments, rues, espaces verts et arbres, {1}). Les hauteurs, la façade et l'emplacement des équipements sont indicatifs.",
        "(слои участков, зданий, улиц, зелёных зон и деревьев, {1}). Высоты, фасад и расположение объектов условны.",
        "(طبقات القسائم والمباني والشوارع والمساحات الخضراء والأشجار، {1}). الارتفاعات والواجهة ومواقع المرافق للتوضيح."),
    pat("(שכבות המגרשים, המבנים, הרחובות, השטחים הירוקים והעצים, {D}); הבניינים במגרש, הקומות והגבהים לפי תכנית העיצוב ({D}); קו החוף לפי OpenStreetMap. החזיתות ומיקום המתקנים להמחשה.",
        "(the lots, buildings, streets, green areas and trees layers, {1}); the buildings on the lot, the floors and the heights per the design plan ({2}); the shoreline per OpenStreetMap. The facades and the facilities' positions are an illustration.",
        "(couches des terrains, bâtiments, rues, espaces verts et arbres, {1}) ; les immeubles du terrain, les étages et les hauteurs selon le plan d'aménagement ({2}) ; le littoral selon OpenStreetMap. Les façades et l'emplacement des équipements sont indicatifs.",
        "(слои участков, зданий, улиц, зелёных зон и деревьев, {1}); здания на участке, этажи и высоты — по архитектурному плану ({2}); береговая линия — по OpenStreetMap. Фасады и расположение объектов условны.",
        "(طبقات القسائم والمباني والشوارع والمساحات الخضراء والأشجار، {1})؛ المباني في القسيمة والطوابق والارتفاعات بحسب مخطط التصميم ({2})؛ خط الساحل بحسب OpenStreetMap. الواجهات ومواقع المرافق للتوضيح."),
    pat("{N} בניינים", "{1} buildings", "{1} immeubles", "зданий: {1}", "{1} مبنى"),
    # the facts' values and lines
    pat("צפון תל אביב, כ-{N} מ׳ מהים", "North Tel Aviv, about {1} m from the sea", "Nord de Tel Aviv, à environ {1} m de la mer", "Север Тель-Авива, около {1} м от моря", "شمال تل أبيب، على بعد نحو {1} م من البحر"),
    pat("מגרש {I}, כ-{N} מ׳ מהים", "Lot {1}, about {2} m from the sea", "Lot {1}, à environ {2} m de la mer", "Участок {1}, около {2} м от моря", "القسيمة {1}، على بعد نحو {2} م من البحر"),
    pat("מגרש {I}, על רחוב לוי אשכול", "Lot {1}, on Levi Eshkol Street", "Lot {1}, rue Levi Eshkol", "Участок {1}, на улице Леви Эшколя", "القسيمة {1}، على شارع ليفي أشكول"),
    pat("מגדל {I} קומות", "A {1}-floor tower", "Une tour de {1} étages", "{1}-этажная башня", "برج من {1} طابقاً"),
    pat("מגדל של {I} קומות", "A {1}-floor tower", "Une tour de {1} étages", "{1}-этажная башня", "برج من {1} طابقاً"),
    pat("ובנייני בוטיק בני {I} קומות", "and {1}-floor boutique buildings", "et des immeubles boutique de {1} étages", "и {1}-этажные бутик-дома", "ومبانٍ بوتيك بارتفاع {1} طوابق"),
    pat("{I} מגדלים של {I} קומות", "{1} towers of {2} floors", "{1} tours de {2} étages", "Башен: {1} · этажей в каждой: {2}", "عدد الأبراج: {1}، في كل منها {2} طابقاً"),
    pat("{I} קומות מגורים בכל מגדל", "{1} residential floors in each tower", "{1} étages résidentiels par tour", "Жилых этажей в каждой башне: {1}", "{1} طابقاً سكنياً في كل برج"),
    pat("מגדלון של {I} ושני מבנים של {I}, לפי תכנית העיצוב",
        "A {1}-floor mid-rise and two {2}-floor buildings, per the design plan",
        "Une petite tour de {1} étages et deux bâtiments de {2} étages, selon le plan d'aménagement",
        "{1}-этажная малая башня и два {2}-этажных здания, по архитектурному плану",
        "برج صغير من {1} طابقاً ومبنيان من {2} طوابق، بحسب مخطط التصميم"),
    pat("מגדלון של {I} ושני בניינים של {I}, לפי תכנית העיצוב",
        "A {1}-floor mid-rise and two {2}-floor buildings, per the design plan",
        "Une petite tour de {1} étages et deux immeubles de {2} étages, selon le plan d'aménagement",
        "{1}-этажная малая башня и два {2}-этажных здания, по архитектурному плану",
        "برج صغير من {1} طابقاً ومبنيان من {2} طوابق، بحسب مخطط التصميم"),
    pat("{N} מהן נמכרו עד {D}, לפי דוחות היזם",
        "{1} of them sold by {2}, per the developer's reports",
        "Dont {1} vendus au {2}, selon les rapports du promoteur",
        "Из них продано {1} на {2}, по отчётам застройщика",
        "بيع منها {1} حتى {2}، بحسب تقارير المطوّر"),
    pat("{N} במגדל ו-{N} בשלושת הבניינים האחרים, לפי תכנית העיצוב",
        "{1} in the tower and {2} in the three other buildings, per the design plan",
        "{1} dans la tour et {2} dans les trois autres immeubles, selon le plan d'aménagement",
        "{1} в башне и {2} в трёх других зданиях, по архитектурному плану",
        "{1} في البرج و{2} في المباني الثلاثة الأخرى، بحسب مخطط التصميم"),
    pat("{I} עד {I} חדרים", "{1} to {2} rooms", "{1} à {2} pièces", "От {1} до {2} комнат", "من {1} إلى {2} غرف"),
    pat("כ-{N} ₪ למ״ר", "About {1} ₪ per m²", "Environ {1} ₪ le m²", "Около {1} ₪ за м²", "نحو {1} ₪ للمتر المربع"),
    pat("דוחות היזם, עד {D}", "The developer's reports, up to {1}", "Rapports du promoteur, jusqu'au {1}", "Отчёты застройщика, до {1}", "تقارير المطوّر، حتى {1}"),
    pat("וכ-{N} חדרי מלון, לפי היזם", "and about {1} hotel rooms, per the developer", "et environ {1} chambres d'hôtel, selon le promoteur", "и около {1} гостиничных номеров, по данным застройщика", "ونحو {1} غرفة فندقية، بحسب المطوّر"),
    pat("{I} קומות מרתף", "{1} basement floors", "{1} niveaux de sous-sol", "Подземных этажей: {1}", "{1} طوابق تحت الأرض"),
    pat("לפי החלטת רשות הרישוי, {D}", "Per the licensing authority's decision, {1}", "Selon la décision de l'autorité d'octroi des permis, {1}", "По решению органа выдачи разрешений, {1}", "بحسب قرار سلطة الترخيص، {1}"),
    pat("השלמה מתוכננת ב-{I}, לפי דוח החברה", "Completion planned for {1}, per the company's report", "Achèvement prévu en {1}, selon le rapport de la société", "Завершение запланировано на {1} год, по отчёту компании", "الإنجاز مخطط له في {1}، بحسب تقرير الشركة"),
    pat("בקומת המרתף, ו-{I} מועדוני דיירים, לפי תכנית העיצוב",
        "On the basement floor, and {1} residents' clubs, per the design plan",
        "Au sous-sol, et {1} clubs de résidents, selon le plan d'aménagement",
        "На подземном этаже, а также клубы для жильцов ({1}), по архитектурному плану",
        "في طابق القبو، و{1} نوادٍ للسكان، بحسب مخطط التصميم"),
    pat("יסודות באביב {I}, יעד השלמה ב-{I}, לפי הפרסומים",
        "Foundations in spring {1}, completion targeted for {2}, per the publications",
        "Fondations au printemps {1}, achèvement visé en {2}, selon les publications",
        "Фундамент весной {1} года, завершение намечено на {2} год, по публикациям",
        "الأساسات في ربيع {1}، والإنجاز مستهدف في {2}، بحسب المنشورات"),
    pat("אכלוס צפוי ב-{I}", "Occupancy expected in {1}", "Livraison prévue en {1}", "Заселение ожидается в {1} году", "الإسكان متوقع في {1}"),
    pat("צפוי ב-{I}", "Expected in {1}", "Prévue en {1}", "Ожидается в {1} году", "متوقع في {1}"),
    pat("מתוכננת ב-{I}", "Planned for {1}", "Prévu en {1}", "Запланировано на {1} год", "مخطط له في {1}"),
    pat("אביב {I}", "Spring {1}", "Printemps {1}", "Весна {1}", "ربيع {1}"),
    pat("יעד {I}", "Target {1}", "Objectif {1}", "Цель: {1}", "الهدف {1}"),
    pat("מ-{N} מיליון ₪", "From {1} million ₪", "À partir de {1} millions ₪", "От {1} млн ₪", "من {1} مليون ₪"),
    pat("כ-{N} מ׳", "About {1} m", "Environ {1} m", "Около {1} м", "نحو {1} م"),
    pat("עד {N} מ׳", "Up to {1} m", "Jusqu'à {1} m", "До {1} м", "حتى {1} م"),
    # the surroundings band (catalog-plus-map.php)
    pat("מאושרת, {N} מ׳", "Approved, {1} m", "Approuvée, {1} m", "Утверждена, {1} м", "مُصادَق عليها، {1} م"),
    pat("פעילה, {N} מ׳ הליכה", "Running, {1} m walk", "En service, {1} m à pied", "Работает, {1} м пешком", "تعمل، {1} م مشياً"),
    pat("{I} עד {N} מ׳", "{1} within {2} m", "{1} à moins de {2} m", "{1} в радиусе {2} м", "{1} ضمن {2} م"),
    pat("{N} מ׳ לקרוב", "{1} m to the nearest", "{1} m pour le plus proche", "{1} м до ближайшего", "{1} م إلى الأقرب"),
    pat("{I} אתרים פעילים", "{1} active sites", "{1} chantiers actifs", "Активных площадок: {1}", "مواقع نشطة: {1}"),
    pat("ברדיוס {N} מ׳ · הקרוב: אתר בנייה ב{X}, היתר {P}, {N} מ׳",
        "Within {1} m · the nearest: a construction site in {2}, permit {3}, {4} m",
        "Dans un rayon de {1} m · le plus proche : un chantier à {2}, permis {3}, {4} m",
        "В радиусе {1} м · ближайшая: стройплощадка в {2}, разрешение {3}, {4} м",
        "ضمن دائرة {1} م · الأقرب: موقع بناء في {2}، الرخصة {3}، {4} م"),
    pat("ברדיוס {N} מ׳ · הקרוב: אתר הבנייה ב{X} {I}, {N} מ׳",
        "Within {1} m · the nearest: the construction site at {2} {3}, {4} m",
        "Dans un rayon de {1} m · le plus proche : le chantier au {3} {2}, {4} m",
        "В радиусе {1} м · ближайшая: стройплощадка на {2}, {3}, {4} м",
        "ضمن دائرة {1} م · الأقرب: موقع البناء في {2} {3}، {4} م"),
    pat("ברדיוס {N} מ׳ · הקרוב: {X}, {N} מ׳",
        "Within {1} m · the nearest: {2}, {3} m", "Dans un rayon de {1} m · le plus proche : {2}, {3} m",
        "В радиусе {1} м · ближайшая: {2}, {3} м", "ضمن دائرة {1} م · الأقرب: {2}، {3} م"),
    pat("תוכנית {I}: {X}", "Plan {1}: {2}", "Plan {1} : {2}", "План {1}: {2}", "المخطط {1}: {2}"),
    pat("{X} · הפרויקט בתחום התוכנית", "{1} · the project is within the plan", "{1} · le projet est dans le périmètre du plan", "{1} · проект находится в границах плана", "{1} · المشروع ضمن حدود المخطط"),
    pat("הסביבה: {X}", "The area: {1}", "Le quartier : {1}", "Район: {1}", "المنطقة: {1}"),
    pat("מפת הסביבה של {X}, {X}", "Map of the area around {1}, {2}", "Carte des environs du projet {1}, {2}", "Карта окрестностей {1}, {2}", "خريطة محيط {1}، {2}"),
    pat("מפת הסביבה של {X}", "Map of the area around {1}", "Carte des environs du projet {1}", "Карта окрестностей {1}", "خريطة محيط {1}"),
    # the tools and the notice
    pat("לעמוד הרשמי של {X}", "To the official page of {1}", "Vers la page officielle de la société {1}", "На официальную страницу {1}", "إلى الصفحة الرسمية لـ {1}"),
    pat("עמוד זה אינו האתר הרשמי של {X} ואינו מופעל מטעמה. נדל״ן היא פלטפורמת מידע עצמאית, ללא קשר מסחרי עם היזם. הפרטים נאספו ממקורות גלויים ויש לאמת אותם מול היזם.",
        "This page is not the official website of {1} and is not operated on its behalf. NadLan is an independent information platform with no commercial connection to the developer. The details were gathered from public sources and should be verified with the developer.",
        "Cette page n'est pas le site officiel de la société {1} et n'est pas exploitée en son nom. NadLan est une plateforme d'information indépendante, sans lien commercial avec le promoteur. Les informations proviennent de sources publiques et doivent être vérifiées auprès du promoteur.",
        "Эта страница не является официальным сайтом {1} и не управляется от её имени. NadLan — независимая информационная платформа без коммерческой связи с застройщиком. Сведения собраны из открытых источников и должны быть проверены у застройщика.",
        "هذه الصفحة ليست الموقع الرسمي لـ {1} ولا تُدار نيابةً عنها. NadLan منصة معلومات مستقلة، دون أي علاقة تجارية بالمطوّر. جُمعت التفاصيل من مصادر علنية ويجب التحقق منها لدى المطوّر."),
    pat("הדמיה של דמרי ימה ברובע שדה דב: מגדל, מגדלון ושני מבנים נמוכים סביב גינה, על מגרש {I}",
        "Illustration of Dimri Yama in the Sde Dov quarter: a tower, a mid-rise and two low buildings around a garden, on lot {1}",
        "Illustration de Dimri Yama dans le quartier de Sde Dov : une tour, une petite tour et deux bâtiments bas autour d'un jardin, sur le lot {1}",
        "Иллюстрация Dimri Yama в районе Сде-Дов: башня, малая башня и два низких здания вокруг сада, на участке {1}",
        "تصور لـ Dimri Yama في حي سديه دوف: برج وبرج صغير ومبنيان منخفضان حول حديقة، على القسيمة {1}"),
    pat("הדמיה של פרויקט דמרי ימה ברובע שדה דב: מגדל, מגדלון ושני מבנים נמוכים סביב גינה, על מגרש {I}",
        "Illustration of the Dimri Yama project in the Sde Dov quarter: a tower, a mid-rise and two low buildings around a garden, on lot {1}",
        "Illustration du projet Dimri Yama dans le quartier de Sde Dov : une tour, une petite tour et deux bâtiments bas autour d'un jardin, sur le lot {1}",
        "Иллюстрация проекта Dimri Yama в районе Сде-Дов: башня, малая башня и два низких здания вокруг сада, на участке {1}",
        "تصور لمشروع Dimri Yama في حي سديه دوف: برج وبرج صغير ومبنيان منخفضان حول حديقة، على القسيمة {1}"),
    pat("הדמיה של פרויקט אשירה ברובע שדה דב: מגדל, מגדלון ושני בניינים נמוכים סביב חצר, על מגרש {I}",
        "Illustration of the Ashira project in the Sde Dov quarter: a tower, a mid-rise and two low buildings around a courtyard, on lot {1}",
        "Illustration du projet Ashira dans le quartier de Sde Dov : une tour, une petite tour et deux immeubles bas autour d'une cour, sur le lot {1}",
        "Иллюстрация проекта Ashira в районе Сде-Дов: башня, малая башня и два низких здания вокруг двора, на участке {1}",
        "تصور لمشروع Ashira في حي سديه دوف: برج وبرج صغير ومبنيان منخفضان حول ساحة، على القسيمة {1}"),
]


def build_combos():
    """The captions made of parts, and the tour card's paragraph: one entry per combination the page can show.
    Returns (exact rows, specific patterns, general patterns); the general ones go last."""
    ex, pats, general = [], [], []
    # the 360 room's caption: A [S] [B] [P]
    for parts in ([A, P], [A, S, P], [A, S], [A, B, P], [A, B], [A, S, B, P], [A, S, B]):
        he = " ".join(p[0] for p in parts)
        tr = {l: " ".join(p[1][l] for p in parts) for l in L}
        if "{" in he:
            pats.append((rx(he),) + tuple(tr[l] for l in L))
        else:
            ex.append((he, tr))
    # the slice's note with the project's line; the room's caption with a note that has numbers
    pats.append((rx(SLICE[0] + " " + SLICE_NOTE[0]),) + tuple(SLICE[1][l] + " " + SLICE_NOTE[1][l] for l in L))
    for n in NOTE_PATS:
        pats.append((rx(ROOM[0] + " " + n[0]),) + tuple(ROOM[1][l] + " " + n[1 + i] for i, l in enumerate(L)))
    # the tour card's paragraph: several floors or one, with or without the balcony
    for multi in (True, False):
        for bal in (True, False):
            fl = "בקומות {L} ו־{I}" if multi else "בקומה {I}"
            he = "סלון ומטבח פתוח כמו במסירה, בלי ריהוט, " + fl + ": " + TOUR_FACING[0] + (TOUR_BAL[0] if bal else "") + ". " + TOUR_SRC[0]
            tr = []
            for l in L:
                tr.append(TOUR_OPEN[l] + (TOUR_MULTI if multi else TOUR_ONE)[l] + COLON[l] + TOUR_FACING[1][l]
                          + (TOUR_BAL[1][l] if bal else "") + ". " + TOUR_SRC[1][l])
            pats.append((rx(he),) + tuple(tr))
    # general: the stage's caption with its geometry line, the slice's note with another line, the room's caption with an
    # exact note (the captured part must be an exact string)
    for base in (CAP1, CAP2, SLICE, ROOM):
        general.append((rx(base[0] + " {X}"),) + tuple(base[1][l] + " {1}" for l in L))
    return ex, pats, general


# the general patterns: last, so a specific one always wins
GENERAL = [
    pat("{X} · {N} ק״מ", "{1} · {2} km", "{1} · {2} km", "{1} · {2} км", "{1} · {2} كم"),
    pat("{X} · {N} מ׳", "{1} · {2} m", "{1} · {2} m", "{1} · {2} м", "{1} · {2} م"),
    pat("קומה {I} · {X}", "Floor {1} · {2}", "Étage {1} · {2}", "Этаж {1} · {2}", "الطابق {1} · {2}"),
    pat("{X} · בשיווק", "{1} · On sale", "{1} · En commercialisation", "{1} · В продаже", "{1} · في مرحلة التسويق"),
    pat("{X} · בבנייה", "{1} · Under construction", "{1} · En construction", "{1} · Строится", "{1} · قيد البناء"),
    pat("{X} · בהיתר בנייה", "{1} · At the building-permit stage", "{1} · Au stade du permis de construire", "{1} · На стадии разрешения на строительство", "{1} · في مرحلة رخصة البناء"),
    pat("{X} · בהליכי היתר", "{1} · In the permit process", "{1} · Permis en cours", "{1} · В процессе получения разрешения", "{1} · في إجراءات الترخيص"),
    pat("{X} · הושלם", "{1} · Completed", "{1} · Achevé", "{1} · Завершён", "{1} · مكتمل"),
    # the legend chips with a count: a closed list (a general "(.+) \((\d+)\)" would, on the server, stop the names-inside
    # fallback for any other "... (n)" line of the page)
    (r"^(₪ מחירים בסביבה|חינוך|פארקים|תחבורה|קניות|בריאות|קפה ומסעדות|◆ תוכניות עתידיות) \((\d+)\)$", "{1} ({2})", "{1} ({2})", "{1} ({2})", "{1} ({2})"),
    pat("לכיוון {X}", "towards {1}", "vers {1}", "в сторону {1}", "باتجاه {1}"),
    pat("מה סביב {X}", "What is around {1}", "Autour du projet {1}", "Что вокруг {1}", "ما حول {1}"),
]

# ---------------------------------------------------------------------------------------------------------------------
# NAMES: projects (brands in Latin), developers, places, streets, areas
# ---------------------------------------------------------------------------------------------------------------------
def same(he, latin):
    return row(he, latin, latin, latin, latin)


NAMES = [
    same("ריינבו", "Rainbow"),
    same("ריינבו תל אביב", "Rainbow Tel Aviv"),
    same("מגדלי דואו תל אביב", "DUO Tel Aviv"),
    same("דמרי ימה", "Dimri Yama"),
    same("דמרי ימה שדה דב", "Dimri Yama Sde Dov"),
    same("אשירה", "Ashira"),
    same("פרויקט אשירה שדה דב", "Ashira Sde Dov"),
    same("זוהי", "ZOHI"),
    same("אוטופיה", "Utopia"),
    same("גינדי ווג", "GINDI VOGUE"),
    same("מגדל איינשטיין", "Einstein Tower"),
    same("פירסט", "FIRST"),
    same("שיכון ובינוי", "Shikun & Binui"),
    row("שיכון ובינוי, מגרש 109", "Shikun & Binui, lot 109", "Shikun & Binui, lot 109", "Shikun & Binui, участок 109", "Shikun & Binui، القسيمة 109"),
    # developers (Israel Canada, Y.H. Dimri and Africa Israel Residences are in lang-pages.json)
    row("לוינשטין, מבנה ואלייד נדל״ן", "Levinstein, Mivne and Allied Real Estate", "Levinstein, Mivne et Allied Real Estate", "Levinstein, Mivne и Allied Real Estate", "Levinstein وMivne وAllied Real Estate"),
    same("קבוצת חג'ג'", "Hagag Group"),
    same("גינדי החזקות", "Gindi Holdings"),
    same("קבוצת נחמיאס", "Nachmias Group"),
    same("אביסרור משה ובניו", "Avisror Moshe & Sons"),
    # places in the quarter and around
    row("תחנת רידינג", "Reading station", "Station Reading", "Станция «Рединг»", "محطة ريدينغ"),
    row("תחנת רידינג, הרכבת הקלה", "Reading station, light rail", "Station Reading, tramway", "Станция «Рединг», лёгкое метро", "محطة ريدينغ، القطار الخفيف"),
    row("בית הספר כוכב הצפון", "Kochav HaTzafon school", "École Kochav HaTzafon", "Школа «Кохав-ха-Цафон»", "مدرسة كوخاف هتسافون"),
    row("גן כוכב הצפון", "Kochav HaTzafon Park", "Parc Kochav HaTzafon", "Парк «Кохав-ха-Цафон»", "حديقة كوخاف هتسافون"),
    row("כוכב הצפון", "Kochav HaTzafon", "Kochav HaTzafon", "«Кохав-ха-Цафон»", "كوخاف هتسافون"),
    row("ארן", "Aran", "Aran", "«Аран»", "أران"),
    row("אלומות", "Alumot", "Alumot", "«Алумот»", "ألوموت"),
    row("חוף רידינג", "Reading Beach", "Plage Reading", "Пляж Рединг", "شاطئ ريدينغ"),
    row("שפך נחל הירקון", "Yarkon River mouth", "Embouchure du Yarkon", "Устье реки Яркон", "مصب نهر اليركون"),
    row("גבעת המורה", "Givat HaMoreh", "Givat HaMoreh", "Гиват-ха-Море", "جفعات همورية"),
    row("בניין העירייה החדש", "The new municipality building", "Le nouveau bâtiment de la municipalité", "Новое здание муниципалитета", "مبنى البلدية الجديد"),
    row("תחנת ארלוזורוב", "Arlozorov station", "Station Arlozorov", "Станция «Арлозоров»", "محطة أرلوزوروف"),
    row("תחנת ארלוזורוב, הקו הירוק", "Arlozorov station, Green Line", "Station Arlozorov, ligne verte", "Станция «Арлозоров», Зелёная линия", "محطة أرلوزوروف، الخط الأخضر"),
    row("תחנת זהרה לביטוב", "Zohara Levitov station", "Station Zohara Levitov", "Станция «Зохара Левитов»", "محطة زوهارا ليفيتوف"),
    # streets over the model (city.json 'labels'; Ibn Gabirol is in lang-pages.json) and in the surroundings band
    row("ארלוזורוב", "Arlozorov", "Arlozorov", "Арлозоров", "أرلوزوروف"),
    row("בן סרוק", "Ben Saruk", "Ben Saruk", "Бен-Сарук", "بن ساروك"),
    row("ישראל גלילי", "Israel Galili", "Israel Galili", "Исраэль Галили", "يسرائيل جليلي"),
    row("יעקב אפטר", "Yaakov Apter", "Yaakov Apter", "Яаков Аптер", "يعقوب أبتر"),
    row("לוי אשכול", "Levi Eshkol", "Levi Eshkol", "Леви Эшколь", "ليفي أشكول"),
    row("אשכול לוי", "Levi Eshkol", "Levi Eshkol", "Леви Эшколь", "ليفي أشكول"),
    # areas
    row("שדה דב", "Sde Dov", "Sde Dov", "Сде-Дов", "سديه دوف"),
    row("תל אביב", "Tel Aviv", "Tel Aviv", "Тель-Авив", "تل أبيب"),
    row("תכנית ל'", "Tochnit Lamed", "Tochnit Lamed", "Тохнит-Ламед", "تخنيت لامد"),
]


# ---------------------------------------------------------------------------------------------------------------------
def build():
    lp = json.load(io.open(LP, encoding="utf-8"))
    combo_ex, combo_pats, combo_general = build_combos()
    ex, names, pats, seen_re = {}, {}, [], set()
    for he, tr in EXACT + combo_ex:
        assert he not in ex, ("duplicate exact", he)
        assert he not in lp.get("exact", {}) and he not in lp.get("names", {}), ("already in lang-pages.json", he)
        for l in L:
            assert tr[l] and not HE.search(tr[l]), (he, l, tr[l])
            assert not re.search(r"\{\d+\}", tr[l]), ("placeholder in an exact row", he, l)
        ex[he] = tr
    for he, tr in NAMES:
        assert he not in names, ("duplicate name", he)
        assert he not in ex, ("name also exact", he)
        assert he not in lp.get("exact", {}) and he not in lp.get("names", {}), ("already in lang-pages.json", he)
        for l in L:
            assert tr[l] and not HE.search(tr[l]), (he, l, tr[l])
        names[he] = tr
    for p in PATTERNS + [pat(*n) for n in NOTE_PATS] + combo_pats + GENERAL + combo_general:
        r = p[0]
        assert r not in seen_re, ("duplicate pattern", r)
        seen_re.add(r)
        assert "#" not in r, ("'#' is the PHP pass's delimiter", r)
        n = re.compile(r).groups
        tr = dict(zip(L, p[1:]))
        for l in L:
            for k in range(1, n + 1):
                assert "{%d}" % k in tr[l], (r, l, k)
            for k in re.findall(r"\{(\d+)\}", tr[l]):
                assert 1 <= int(k) <= n, ("placeholder without a capture", r, l, k)
            assert not HE.search(tr[l]), (r, l, tr[l])
        pats.append({"re": r, **tr})
    doc = {"note": "StageDict (HAD-361, 28.9.2026): the project stage's words on a project's language page (the 3D stage, its "
                   "360 room, its floor slice, the facility and place cards, the view panel and the stage's server-printed parts). "
                   "Built by scripts/i18n/build_stage_dict.py; read with i18n/lang-pages.json by assets/project-stage/i18n-dom.js "
                   "(the browser) and inc/lang-pages.php (the server). Keys are the exact Hebrew the stage prints.",
           "exact": ex, "patterns": pats, "names": names}
    io.open(OUT, "w", encoding="utf-8", newline="\n").write(json.dumps(doc, ensure_ascii=False, indent=1) + "\n")
    print("ok", len(ex), "exact,", len(pats), "patterns,", len(names), "names ->", OUT)
    return doc, lp


# ---------------------------------------------------------------------------------------------------------------------
# the check: replay both runtimes' lookup on what the stage shows
# ---------------------------------------------------------------------------------------------------------------------
# server-printed strings left out on purpose (lead paragraph, broker card, invitation, film, deals table)
SERVER_SKIP_PREFIX = ("ריינבו תל אביב (Rainbow Tel Aviv) הוא", "DUO Tel Aviv הוא", "DIMRI YAMA הוא", "אשירה (ASHIRA) הוא")
SERVER_SKIP = {
    "פרסומת", "מיטל קציר", "מתווכת", "· נופי ים, כוכב הצפון, צוקי אביב", "רישיון תיווך", "התייעצות בוואטסאפ",
    "רוצה להופיע כאן?", "מתווכים ואנשי מקצוע באזור: הכרטיס שלכם ליד הפרויקט, מול מי שבודק אותו עכשיו.", "לפרטים ולהצטרפות",
    "סרטון הפרויקט", "· 49 שניות",
    "עסקאות בפרויקט", "דירות שנמכרו בריינבו תל אביב, לפי קומה", "דירות שנמכרו במגדלי דואו תל אביב, לפי קומה",
    "הדירות שנמכרו בפרויקט ופורסמו עם הקומה שלהן, לפי נתוני רשות המסים כפי שפורסמו בעיתונות. לא כל העסקאות פורסמו, ועסקאות של בניינים שכנים אינן כאן.",
    "הדירות שנמכרו בפרויקט ופורסמו עם הקומה שלהן, לפי דיווח החברה כפי שפורסם בעיתונות. לא כל העסקאות פורסמו, ועסקאות של בניינים שכנים אינן כאן.",
    "275 מתוך 459", "372 מתוך 510", "דירות נמכרו עד 6.2026, לפי דוחות היזם", "דירות נמכרו עד 6.2026, לפי דוח היזם",
    "המחיר הממוצע בדירות שנמכרו עד 3.2026, לפי דוחות היזם", "המחיר הממוצע לפני מע״מ בחוזים שנחתמו ב-1-6.2026, לפי דוח היזם",
    "כ-11 מיליון ₪", "המחיר הממוצע לדירה, כולל מע״מ, ב-12 הדירות שנמכרו ב-1-6.2026, לפי דוח היזם",
    "הדירה", "למ״ר", "מועד", "מקור", "בבמה", "אחת הגבוהות", "מגדל", "כמה דירות באותה קומה, לאיחוד לכ-550 מ״ר",
    "כ-50 מיליון ₪", "לא פורסם", "גלובס", "3 חדרים · 98 מ״ר", "יותר מ-8 מיליון ₪", "מעל 81,600 ₪", ", לפי רשות המסים",
    "לקומה במגדל", "בניין בוטיק, מתוך 9", "6 חדרים · 182 מ״ר", "כ-21.7 מיליון ₪", "כ-119,200 ₪", "6 חדרים · 202 מ״ר",
    "20 מיליון ₪", "כ-99,000 ₪", "הבניין לא צוין", "5 חדרים · 133 מ״ר ומרפסת 17 מ״ר, עם נוף לים", "10.18 מיליון ₪",
    "כ-76,500 ₪", "ביזפורטל", "3 חדרים · 60 מ״ר, ללא חניה", "4 מיליון ₪", "כ-66,700 ₪", "חדר אחד · 32 מ״ר",
    "3.1 מיליון ₪", "כ-96,900 ₪", "המחיר למ״ר מחושב: המחיר שפורסם חלקי שטח הדירה, בלי המרפסת והחניה.",
    "קומה 13 במגדל, בבמה", "קומה 6 במגדל, בבמה", "קומה 4 במגדל, בבמה", "קומה 17 במגדל, בבמה", "קומה 16 במגדל, בבמה",
    "קומה 12 במגדל, בבמה", "הבניין השני בפרויקט", "4 חדרים · כ-102 מ״ר ומרפסת כ-17 מ״ר, עם חניה", "כ-7.44 מיליון ₪",
    "כ-72,900 ₪", "מרכז הנדל״ן", ", לפי דיווח החברה: מכירה מוקדמת לבעלי עניין", "כ-7.33 מיליון ₪", "כ-71,900 ₪",
    "כ-7.03 מיליון ₪", "כ-68,900 ₪",
}


def merged(lp, sd, lang):
    """The dictionary one language page gets (inc/project-stage.php's footer): lang-pages.json first, then this file."""
    out = {"lang": lang, "exact": {}, "names": {}, "patterns": []}
    for d in (lp, sd):
        for he, tr in d.get("exact", {}).items():
            if lang in tr:
                out["exact"][he] = tr[lang]
        for he, tr in d.get("names", {}).items():
            if lang in tr:
                out["names"][he] = tr[lang]
        for p in d.get("patterns", []):
            if p.get("re") and lang in p:
                out["patterns"].append({"re": p["re"], "tr": p[lang]})
    return out


def tr_py(s, D, comp, strict):
    """i18n-dom.js's tr() (strict=False) or inc/lang-pages.php's nadlan_lp_tr() (strict=True: the first match decides)."""
    ex, nm = D["exact"], D["names"]
    if s in ex:
        return ex[s]
    if s in nm:
        return nm[s]
    for rxc, t in comp:
        if rxc is None:
            continue
        m = rxc.search(s)
        if not m:
            continue
        r, ok = t, True
        for i in range(len(m.groups()), 0, -1):
            c = m.group(i) or ""
            if c in nm:
                c = nm[c]
            elif c in ex:
                c = ex[c]
            elif HE.search(c):
                ok = False
                break
            r = r.replace("{%d}" % i, c)
        if ok:
            return r
        if strict:
            return None
    t = s
    for k in sorted(nm, key=len, reverse=True):
        if k in t:
            t = t.replace(k, nm[k])
    if t != s and not HE.search(t):
        return t
    return None


NODE_JS = r"""
const fs = require('fs');
const job = JSON.parse(fs.readFileSync(process.argv[2], 'utf8'));
const out = {}, bad = {};
for (const D of job.dicts) {
  const HE = /[֐-׿]/;
  const exact = D.exact || {}, names = D.names || {};
  const refused = [];
  const pats = (D.patterns || []).map((p) => { try { return { re: new RegExp(p.re, 'u'), tr: p.tr }; } catch (e) { refused.push(p.re); return null; } }).filter(Boolean);
  const nameKeys = Object.keys(names).sort((a, b) => b.length - a.length);
  function tr(s) {
    let out = null;
    if (Object.prototype.hasOwnProperty.call(exact, s)) out = exact[s];
    else if (Object.prototype.hasOwnProperty.call(names, s)) out = names[s];
    else {
      for (const p of pats) {
        const m = p.re.exec(s);
        if (!m) continue;
        let r = p.tr, ok = true;
        for (let i = m.length - 1; i >= 1; i--) {
          let c = m[i] == null ? '' : m[i];
          if (Object.prototype.hasOwnProperty.call(names, c)) c = names[c];
          else if (Object.prototype.hasOwnProperty.call(exact, c)) c = exact[c];
          else if (HE.test(c)) { ok = false; break; }
          r = r.split('{' + i + '}').join(c);
        }
        if (ok) { out = r; break; }
      }
      if (out == null && nameKeys.length) {
        let t = s;
        for (const k of nameKeys) if (t.indexOf(k) >= 0) t = t.split(k).join(names[k]);
        if (t !== s && !HE.test(t)) out = t;
      }
    }
    return out;
  }
  out[D.lang] = job.strings.map(tr);
  bad[D.lang] = refused;
}
process.stdout.write(JSON.stringify({ out, bad }));
"""

PHP_SRC = r"""<?php
$job = json_decode( file_get_contents( $argv[1] ), true );
$out = array(); $bad = array();
foreach ( $job['dicts'] as $d ) {
	$lang = $d['lang']; $bad[ $lang ] = array();
	foreach ( $d['patterns'] as $p ) { if ( false === @preg_match( '#' . $p['re'] . '#u', '' ) ) { $bad[ $lang ][] = $p['re']; } }
	$nm = $d['names'];
	$res = array();
	foreach ( $job['strings'] as $s ) {
		$r = null; $done = false;
		if ( isset( $d['exact'][ $s ] ) ) { $r = $d['exact'][ $s ]; $done = true; }
		elseif ( isset( $d['names'][ $s ] ) ) { $r = $d['names'][ $s ]; $done = true; }
		if ( ! $done ) {
			foreach ( $d['patterns'] as $p ) {
				if ( ! preg_match( '#' . $p['re'] . '#u', $s, $m ) ) { continue; }
				$o = $p['tr']; $ok = true;
				for ( $i = count( $m ) - 1; $i >= 1; $i-- ) {
					$c = $m[ $i ];
					if ( isset( $d['names'][ $c ] ) ) { $c = $d['names'][ $c ]; }
					elseif ( isset( $d['exact'][ $c ] ) ) { $c = $d['exact'][ $c ]; }
					elseif ( preg_match( '/[\x{0590}-\x{05FF}]/u', $c ) ) { $ok = false; break; }
					$o = str_replace( '{' . $i . '}', $c, $o );
				}
				$r = $ok ? $o : null; $done = true;
				break;
			}
		}
		if ( ! $done && $nm ) {
			$t = strtr( $s, $nm );
			if ( $t !== $s && ! preg_match( '/[\x{0590}-\x{05FF}]/u', $t ) ) { $r = $t; }
		}
		$res[] = $r;
	}
	$out[ $lang ] = $res;
}
echo json_encode( array( 'out' => $out, 'bad' => $bad ), JSON_UNESCAPED_UNICODE );
"""


def find_php():
    for c in (shutil.which("php"), os.path.expanduser(r"~/tools/php-8.3/php.exe"), os.path.expanduser(r"~/tools/php-8.3/php")):
        if c and os.path.exists(c):
            return c
    return None


def check(sd, lp):
    harvest = json.load(io.open(HARVEST, encoding="utf-8"))["strings"]
    server = [x["he"] for x in json.load(io.open(SERVER, encoding="utf-8"))["strings"]]
    server_t = [s for s in dict.fromkeys(server) if s not in SERVER_SKIP and not s.startswith(SERVER_SKIP_PREFIX)]
    h_ex = [e for sh in harvest for e in sh["examples"]]
    strings = list(dict.fromkeys(h_ex + server_t))
    dicts = {l: merged(lp, sd, l) for l in L}
    py = {}
    for l in L:
        comp = []
        for p in dicts[l]["patterns"]:
            try:
                comp.append((re.compile(p["re"]), p["tr"]))
            except re.error:
                comp.append((None, p["tr"]))
        py[l] = {"js": [tr_py(s, dicts[l], comp, False) for s in strings], "php": [tr_py(s, dicts[l], comp, True) for s in strings]}
    tmp = tempfile.mkdtemp()
    job = os.path.join(tmp, "job.json")
    io.open(job, "w", encoding="utf-8").write(json.dumps({"dicts": [dicts[l] for l in L], "strings": strings}, ensure_ascii=False))
    engines = {}
    node = shutil.which("node")
    if node:
        js = os.path.join(tmp, "check.js")
        io.open(js, "w", encoding="utf-8").write(NODE_JS)
        r = subprocess.run([node, js, job], capture_output=True)
        engines["node"] = json.loads(r.stdout.decode("utf-8")) if r.returncode == 0 else None
        if r.returncode:
            print("node failed:", r.stderr.decode("utf-8", "replace")[:400])
    php = find_php()
    if php:
        ph = os.path.join(tmp, "check.php")
        io.open(ph, "w", encoding="utf-8").write(PHP_SRC)
        r = subprocess.run([php, ph, job], capture_output=True)
        engines["php"] = json.loads(r.stdout.decode("utf-8")) if r.returncode == 0 and r.stdout else None
        if not engines["php"]:
            print("php failed:", (r.stdout + r.stderr).decode("utf-8", "replace")[:400])
    idx = {s: i for i, s in enumerate(strings)}
    # the engines agree with the Python replay?
    for eng, res in engines.items():
        if not res:
            continue
        mode = "js" if eng == "node" else "php"
        for l in L:
            ref = py[l][mode]
            diff = [strings[i] for i in range(len(strings)) if res["out"][l][i] != ref[i]]
            if diff:
                print("  %s/%s differs from the Python replay on %d strings, e.g. %r" % (eng, l, len(diff), diff[:3]))
        own = set(p["re"] for p in sd["patterns"])
        refused_own = sorted(set(r for l in L for r in res["bad"][l] if r in own))
        refused_lp = sorted(set(r for l in L for r in res["bad"][l] if r not in own))
        print("%s: this file's patterns refused: %d%s" % (eng, len(refused_own), (" " + repr(refused_own)) if refused_own else ""))
        if refused_lp:
            print("%s: lang-pages.json patterns the %s refuses (dropped at run time): %d %r" % (eng, "browser" if eng == "node" else "server", len(refused_lp), refused_lp))
    print()
    print("HARVEST (docs/i18n/stage-harvest.json): %d shapes, %d examples" % (len(harvest), len(h_ex)))
    for l in L:
        for mode, label in (("js", "browser"), ("php", "server ")):
            res = py[l][mode]
            ok_ex = sum(1 for e in h_ex if res[idx[e]] is not None)
            ok_sh = sum(1 for sh in harvest if all(res[idx[e]] is not None for e in sh["examples"]))
            print("  %s %s: examples %d/%d, shapes %d/%d" % (l, label, ok_ex, len(h_ex), ok_sh, len(harvest)))
    miss = [e for e in h_ex if any(py[l][m][idx[e]] is None for l in L for m in ("js", "php"))]
    print("  left in Hebrew:", len(miss))
    for e in miss:
        print("    -", e)
    print()
    print("SERVER (docs/i18n/stage-server.json): %d strings to translate (%d left out on purpose)" % (len(server_t), len(dict.fromkeys(server)) - len(server_t)))
    for l in L:
        res = py[l]["php"]
        print("  %s server: %d/%d" % (l, sum(1 for s in server_t if res[idx[s]] is not None), len(server_t)))
    miss = [s for s in server_t if any(py[l]["php"][idx[s]] is None for l in L)]
    print("  left in Hebrew:", len(miss))
    for s in miss:
        print("    -", s)
    return py, strings, idx


if __name__ == "__main__":
    doc, lp = build()
    if "--no-check" not in sys.argv:
        check(doc, lp)
