# -*- coding: utf-8 -*-
"""The world data's texts in French, Russian and Arabic (Kikar Hamedina P8, 1.72.370): writes
plugins/nadlan-config/assets/project-stage/hamedina/world-i18n.json, which assets/project-stage/world/world.js loads on the
fr / ru / ar pages only (world.json itself keeps its Hebrew and English and is not re-shipped).

The file is keyed by the English text of world.json (the fleet's rule: a line the data changes falls back to English, never to
a wrong translation). Names: a place keeps the name its sources give in that language (places.json OSM names, the fleet's
dictionaries i18n/stage-dict.json and i18n/lang-other.json: Тель-Авив, Рамат-Ган, Арлозоров, Азриэли, Больница Ихилов,
Еврейская Гимназия «Герцлия», Рединг, Сарона, كيكار همدينا, أرلوزوروف, عزرائيلي, غيمناسيا هرتسلية, ريدينغ ...); a name with no
source form in that language stays in its English (Latin) form, and only the common words around it are translated.

Checks: every English text of world.json has all three languages; no Hebrew letter, no long dash in any translation; every
English key is a real text of world.json (no stale key). Exit 1 on any failure.

  python scripts/project-stage/world_i18n_hamedina.py
"""
import io, json, os, re, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(HERE))
DIR = os.path.join(REPO, "plugins", "nadlan-config", "assets", "project-stage", "hamedina")
OUT = os.path.join(DIR, "world-i18n.json")

# English text -> (fr, ru, ar)
T = {
    # the public buildings
    "Kikar HaMedina school": ("École Kikar Hamedina", "Школа «Кикар ха-Медина»", "مدرسة كيكار همدينا"),
    "Community centre": ("Centre communautaire", "Общинный центр", "المركز الجماهيري"),
    # the park's features (their places in the park are an illustration)
    "Dog garden": ("Jardin pour chiens", "Площадка для собак", "حديقة للكلاب"),
    "A dog garden in the square's new park": ("Un jardin pour chiens dans le nouveau parc de la place", "Площадка для собак в новом парке площади", "حديقة للكلاب في الحديقة الجديدة للميدان"),
    "Playground": ("Aire de jeux", "Детская площадка", "ملعب أطفال"),
    "A playground with play equipment for children": ("Une aire de jeux équipée pour les enfants", "Детская площадка с игровым оборудованием", "ملعب مجهّز بألعاب للأطفال"),
    "Lawns and tables": ("Pelouses et tables", "Лужайки и столы", "مروج وطاولات"),
    "Lawns, game tables and seating": ("Pelouses, tables de jeux et coins pour s’asseoir", "Лужайки, игровые столы и места для отдыха", "مروج وطاولات ألعاب وأماكن للجلوس"),
    "Bridges and paths": ("Ponts et allées", "Мостики и дорожки", "جسور وممرات"),
    "Paths, flow channels and bridges around the pond": ("Allées, canaux d’eau et ponts autour de l’étang", "Дорожки, водные каналы и мостики вокруг пруда", "ممرات وقنوات مياه وجسور حول البركة"),
    "Boulevard and bike path": ("Boulevard et piste cyclable", "Бульвар и велодорожка", "جادة ومسار للدراجات"),
    "A new urban boulevard around the square, with a bike path": ("Un nouveau boulevard urbain autour de la place, avec une piste cyclable", "Новый городской бульвар вокруг площади с велодорожкой", "جادة حضرية جديدة حول الميدان مع مسار للدراجات"),
    "Three rows of trees": ("Trois rangées d’arbres", "Три ряда деревьев", "ثلاثة صفوف من الأشجار"),
    "Three rows of trees along the boulevard, including heritage trees": ("Trois rangées d’arbres le long du boulevard, dont des arbres remarquables conservés", "Три ряда деревьев вдоль бульвара, в том числе сохранённые старые деревья", "ثلاثة صفوف من الأشجار على طول الجادة، منها أشجار قديمة محفوظة"),
    "560 new trees and 36 mature trees kept": ("560 nouveaux arbres et 36 arbres adultes conservés", "560 новых деревьев и 36 сохранённых взрослых деревьев", "560 شجرة جديدة و36 شجرة ناضجة محفوظة"),
    "Running track, 750 m": ("Piste de course, 750 m", "Беговая дорожка, 750 м", "مسار جري، 750 م"),
    "A 750 m running track": ("Une piste de course de 750 m", "Беговая дорожка длиной 750 м", "مسار جري بطول 750 م"),
    "Kiosks and seating": ("Kiosques et coins détente", "Киоски и места для отдыха", "أكشاك وأماكن جلوس"),
    "Kiosks and shaded seating in the park": ("Kiosques et coins ombragés dans le parc", "Киоски и тенистые места для отдыха в парке", "أكشاك وأماكن جلوس مظللة في الحديقة"),
    "Three kiosks (2022) or four small cafés in kiosk form (2025)": ("Trois kiosques (2022) ou quatre petits cafés en forme de kiosque (2025)", "Три киоска (2022) или четыре небольших кафе в формате киоска (2025)", "ثلاثة أكشاك (2022) أو أربعة مقاهٍ صغيرة على شكل أكشاك (2025)"),
    # the landmarks seen from the windows
    "Ramat Aviv": ("Ramat Aviv", "Рамат-Авив", "رمات أفيف"),
    "Tel Aviv University": ("Université de Tel Aviv", "Тель-Авивский университет", "جامعة تل أبيب"),
    "Moshe Aviv Tower (Ramat Gan)": ("Tour Moshe Aviv (Ramat Gan)", "Башня Moshe Aviv (Рамат-Ган)", "برج Moshe Aviv (رمات غان)"),
    "Tel Aviv Savidor Center railway station": ("Gare Tel Aviv Savidor Center", "Ж/д станция «Тель Авив Савидор Центр»", "محطة قطار تل أبيب سفيدور مركز"),
    "Azrieli Center (the three towers)": ("Centre Azrieli (les trois tours)", "Центр Азриэли (три башни)", "مجمع عزرائيلي (الأبراج الثلاثة)"),
    "Ichilov (Tel Aviv Sourasky Medical Center)": ("Hôpital Ichilov (centre médical Sourasky de Tel Aviv)", "Больница Ихилов (медицинский центр Sourasky)", "مستشفى Ichilov (مركز Sourasky الطبي في تل أبيب)"),
    "Azrieli Sarona Tower": ("Tour Azrieli Sarona", "Башня Азриэли Сарона", "برج عزرائيلي سارونا"),
    "Habima Theatre": ("Théâtre Habima", "Театр Habima", "مسرح Habima"),
    "Tel Aviv-Yafo City Hall (Rabin Square)": ("Hôtel de ville de Tel Aviv-Jaffa (place Rabin)", "Мэрия Тель-Авива-Яффо (Rabin Square)", "مبنى بلدية تل أبيب يافا (Rabin Square)"),
    "Mediterranean Sea": ("Mer Méditerranée", "Средиземное море", "البحر الأبيض المتوسط"),
    "Tel Aviv Port": ("Port de Tel Aviv", "Порт Тель-Авива", "ميناء تل أبيب"),
    "Reading lighthouse": ("Phare de Reading", "Маяк Рединг", "منارة ريدينغ"),
    "Reading power station": ("Centrale électrique Reading", "Электростанция Рединг", "محطة كهرباء ريدينغ"),
    "Sportek": ("Sportek", "Sportek", "Sportek"),
    # the pins (the key places on the aerial view and from the windows)
    "Ichilov station, Purple Line": ("Station Ichilov, ligne violette", "Станция «Ихилов», Фиолетовая линия", "محطة Ichilov، الخط البنفسجي"),
    "Arlozorov station, Red Line": ("Station Arlozorov, ligne rouge", "Станция «Арлозоров», Красная линия", "محطة أرلوزوروف، الخط الأحمر"),
    "Tel Aviv Savidor Center railway": ("Gare Tel Aviv Savidor Center", "Ж/д станция «Тель Авив Савидор Центр»", "محطة قطار تل أبيب سفيدور مركز"),
    "Arlozorov station, Green Line": ("Station Arlozorov, ligne verte", "Станция «Арлозоров», Зелёная линия", "محطة أرلوزوروف، الخط الأخضر"),
    "Ichilov Hospital": ("Hôpital Ichilov", "Больница Ихилов", "مستشفى Ichilov"),
    "Park HaYarkon (Ganei Yehoshua)": ("Parc HaYarkon (Ganei Yehoshua)", "Парк Яркон (Ganei Yehoshua)", "حديقة اليركون (Ganei Yehoshua)"),
    "Abraham Park": ("Abraham Park", "Abraham Park", "Abraham Park"),
    "ZEST": ("ZEST", "ZEST", "ZEST"),
    "Kikar HaMedina Bakery": ("Boulangerie Kikar Hamedina", "Пекарня «Кикар ха-Медина»", "مخبز كيكار همدينا"),
    "Gucci": ("Gucci", "Gucci", "Gucci"),
    "Lehem Erez": ("Lehem Erez", "Lehem Erez", "Lehem Erez"),
    "Herzliya Hebrew Gymnasium": ("Gymnase hébraïque Herzliya", "Еврейская Гимназия «Герцлия»", "غيمناسيا هرتسلية"),
    "Tel Aviv Theatre": ("Théâtre de Tel Aviv", "Театр «Тель-Авив»", "مسرح تل أبيب"),
    "Arlozorov 97 sports centre": ("Centre sportif Arlozorov 97", "Спортивный центр Арлозоров 97", "مركز أرلوزوروف 97 الرياضي"),
    # what the model shows for illustration
    "Floor height 4.0 m: provisional (160 m / 40 floors); floor heights are not published": (
        "Hauteur d’étage 4,0 m : provisoire (160 m pour 40 étages) ; les hauteurs d’étage ne sont pas publiées",
        "Высота этажа 4,0 м: предварительно (160 м на 40 этажей); высота этажей не публиковалась",
        "ارتفاع الطابق 4.0 م: تقدير مؤقت (160 م على 40 طابقاً)؛ ارتفاعات الطوابق لم تُنشر"),
    "The turn's direction is not published: shown counter-clockwise from above": (
        "Le sens de rotation n’est pas publié : il est montré dans le sens inverse des aiguilles d’une montre, vu du ciel",
        "Направление поворота не публиковалось: показано против часовой стрелки, если смотреть сверху",
        "اتجاه الدوران لم يُنشر: يظهر هنا عكس عقارب الساعة عند النظر من الأعلى"),
    "Floor-plate shape is an illustration, circle-inspired, sized to the municipal footprint; no official plan is public": (
        "La forme de l’étage est une illustration inspirée du cercle, à la taille du contour municipal ; aucun plan officiel n’est public",
        "Форма этажа условная, по мотивам круга, по размеру контура из данных муниципалитета; официальный план не опубликован",
        "شكل الطابق توضيحي مستوحى من الدائرة وبحجم مخطط البلدية؛ لا يوجد مخطط رسمي منشور"),
    "The set-back between floors is not quantified, so it is not shown": (
        "Le retrait entre les étages n’est pas chiffré, il n’est donc pas montré",
        "Отступ между этажами не указан в цифрах, поэтому не показан",
        "التراجع بين الطوابق غير محدد بالأرقام، لذلك لا يظهر"),
    "Tower B's roof crown (148 to 157 m) is an illustration": (
        "Le couronnement de la tour B (de 148 à 157 m) est une illustration",
        "Верхняя часть башни B (от 148 до 157 м) показана условно",
        "تاج سطح البرج B (من 148 إلى 157 م) توضيحي"),
    # the towers
    "Three residential towers: towers A and C of 40 floors and 160 m, tower B of 37 floors and 157 m": (
        "Trois tours résidentielles : les tours A et C, 40 étages et 160 m, la tour B, 37 étages et 157 m",
        "Три жилые башни: башни A и C по 40 этажей и 160 м, башня B на 37 этажей и 157 м",
        "ثلاثة أبراج سكنية: البرجان A وC من 40 طابقاً وبارتفاع 160 م، والبرج B من 37 طابقاً وبارتفاع 157 م"),
    "Every floor turns 1.25° against the floor below": (
        "Chaque étage pivote de 1,25° par rapport à l’étage inférieur",
        "Каждый этаж повёрнут на 1,25° относительно нижнего",
        "كل طابق يدور 1.25 درجة عن الطابق الذي تحته"),
    "453 apartments in the three towers": ("453 appartements dans les trois tours", "453 квартиры в трёх башнях", "453 شقة في الأبراج الثلاثة"),
    "Architects: Yaski Mor Sivan · Built by Electra Construction and Ashtrom": (
        "Architectes : Yaski Mor Sivan · construction : Electra Construction et Ashtrom",
        "Архитекторы: Yaski Mor Sivan · строительство: Electra Construction и Ashtrom",
        "المعماريون: Yaski Mor Sivan · البناء: Electra Construction وAshtrom"),
    "A façade of floor slabs and white curtain walls repeated floor after floor": (
        "Une façade de dalles et de murs-rideaux blancs, répétée étage après étage",
        "Фасад из плит перекрытий и белых навесных стен, повторяющийся этаж за этажом",
        "واجهة من ألواح الطوابق والجدران الستائرية البيضاء تتكرر طابقاً بعد طابق"),
    "Pool, gym, spa, treatment rooms and multi-purpose halls on one of the basement levels": (
        "Piscine, salle de sport, spa, salles de soins et salles polyvalentes à l’un des niveaux du sous-sol",
        "Бассейн, тренажёрный зал, спа, процедурные кабинеты и многофункциональные залы на одном из подземных уровней",
        "بركة سباحة ونادٍ رياضي وسبا وغرف علاج وقاعات متعددة الاستخدامات في أحد الطوابق السفلية"),
    "Frame completed on 23.4.2026, per the municipality's building-site record": (
        "Gros œuvre achevé le 23 avril 2026, selon le registre des chantiers de la municipalité",
        "Каркас завершён 23.04.2026, по реестру стройплощадок муниципалитета",
        "اكتمل الهيكل في 23.4.2026، وفق سجل مواقع البناء في البلدية"),
    "40 floors · 160 m": ("40 étages · 160 m", "40 этажей · 160 м", "40 طابقاً · 160 م"),
    "In the south-west of the compound": ("Au sud-ouest de l’ensemble", "В юго-западной части комплекса", "في الجهة الجنوبية الغربية من المجمع"),
    "37 floors · 157 m": ("37 étages · 157 m", "37 этажей · 157 м", "37 طابقاً · 157 م"),
    "In the municipality's buildings data: 40 floors · 158.2 m": (
        "Dans les données des bâtiments de la municipalité : 40 étages · 158,2 m",
        "В данных муниципалитета о зданиях: 40 этажей · 158,2 м",
        "في بيانات المباني لدى البلدية: 40 طابقاً · 158.2 م"),
    "In the south-east of the compound": ("Au sud-est de l’ensemble", "В юго-восточной части комплекса", "في الجهة الجنوبية الشرقية من المجمع"),
    "In the north-east of the compound": ("Au nord-est de l’ensemble", "В северо-восточной части комплекса", "في الجهة الشمالية الشرقية من المجمع"),
    # the park and the pond
    "A public park of about 40 dunams in the heart of the square": (
        "Un parc public d’environ 4 hectares (40 dounams) au cœur de la place",
        "Общественный парк площадью около 40 дунамов (4 га) в центре площади",
        "حديقة عامة بمساحة نحو 40 دونماً في قلب الميدان"),
    "An ecological pond 1 m deep, lawns, a dog park and playgrounds": (
        "Un étang écologique de 1 m de profondeur, des pelouses, un parc à chiens et des aires de jeux",
        "Экологический пруд глубиной 1 м, лужайки, площадка для собак и детские площадки",
        "بركة بيئية بعمق 1 م ومروج وحديقة للكلاب وملاعب أطفال"),
    "A 750 m running track and a perimeter boulevard with a bike path": (
        "Une piste de course de 750 m et un boulevard périphérique avec piste cyclable",
        "Беговая дорожка длиной 750 м и кольцевой бульвар с велодорожкой",
        "مسار جري بطول 750 م وجادة محيطية مع مسار للدراجات"),
    "The works in the square and on the ה' באייר ring are due by the end of 2027 (the municipality)": (
        "Les travaux sur la place et sur la rue circulaire He Be’Iyar doivent s’achever d’ici fin 2027 (la municipalité)",
        "Работы на площади и на кольцевой улице должны завершиться к концу 2027 года (муниципалитет)",
        "من المتوقع أن تنتهي الأعمال في الميدان وعلى الشارع الدائري حتى نهاية 2027 (البلدية)"),
    "An ecological pond 1 m deep": ("Un étang écologique de 1 m de profondeur", "Экологический пруд глубиной 1 м", "بركة بيئية بعمق 1 م"),
    "Surrounded by perennial planting, with flow channels, bridges and paths": (
        "Entouré de plantes vivaces, avec des canaux d’eau, des ponts et des allées",
        "Окружён многолетними растениями, с водными каналами, мостиками и дорожками",
        "تحيط بها نباتات معمّرة مع قنوات مياه وجسور وممرات"),
    "Location and shape shown for illustration only: the pond's plan is not published": (
        "Emplacement et forme indicatifs : le plan de l’étang n’est pas publié",
        "Место и форма показаны условно: план пруда не опубликован",
        "الموقع والشكل للتوضيح فقط: مخطط البركة لم يُنشر"),
    # the public buildings
    "A primary school in the north of the square, opened with the start of the school year": (
        "Une école primaire au nord de la place, ouverte à la rentrée scolaire",
        "Начальная школа в северной части площади, открылась к началу учебного года",
        "مدرسة ابتدائية في شمال الميدان افتُتحت مع بداية العام الدراسي"),
    "A fan-shaped building with three upper floors and an active green roof": (
        "Un bâtiment en éventail sur trois étages, avec un toit végétalisé accessible",
        "Здание в форме веера с тремя верхними этажами и активной зелёной крышей",
        "مبنى على شكل مروحة من ثلاثة طوابق علوية مع سطح أخضر نشط"),
    "An underground sports hall, an active courtyard and a field open to the public in the afternoons": (
        "Une salle de sport souterraine, une cour animée et un terrain ouvert au public l’après-midi",
        "Подземный спортзал, активный двор и поле, открытое для всех после обеда",
        "قاعة رياضية تحت الأرض وساحة نشطة وملعب مفتوح للجمهور بعد الظهر"),
    "18 classes plus 6 special-education classes · 75 ה' באייר": (
        "18 classes et 6 classes d’enseignement spécialisé · 75 rue He Be’Iyar",
        "18 классов и ещё 6 классов специального образования · He Be’Iyar, 75",
        "18 صفاً و6 صفوف للتربية الخاصة · He Be’Iyar 75"),
    "The community centre in the south of the square: five floors of activity rooms, lecture halls, a dance studio, art rooms and a multi-purpose hall": (
        "Le centre communautaire au sud de la place : cinq étages de salles d’activités, d’amphithéâtres, un studio de danse, des ateliers d’art et une salle polyvalente",
        "Общинный центр в южной части площади: пять этажей с кружками, лекционными залами, танцевальной студией, художественными мастерскими и многофункциональным залом",
        "المركز الجماهيري في جنوب الميدان: خمسة طوابق من غرف النشاطات وقاعات المحاضرات واستوديو للرقص وغرف للفنون وقاعة متعددة الاستخدامات"),
    "In the 2021 design: 4 floors (up to 7 later), the park's management office, public toilets and a café of about 60 m²": (
        "Dans le projet de 2021 : 4 étages (jusqu’à 7 plus tard), le bureau de gestion du parc, des toilettes publiques et un café d’environ 60 m²",
        "В проекте 2021 года: 4 этажа (позднее до 7), офис управления парком, общественные туалеты и кафе площадью около 60 м²",
        "في تصميم 2021: 4 طوابق (حتى 7 لاحقاً) ومكتب إدارة الحديقة ومراحيض عامة ومقهى بمساحة نحو 60 م²"),
    # the square
    "The square's ring of buildings was built mostly in the early 1970s": (
        "L’anneau d’immeubles de la place a été construit pour l’essentiel au début des années 1970",
        "Кольцо зданий вокруг площади построено в основном в начале 1970-х годов",
        "بُنيت حلقة مباني الميدان في معظمها في مطلع السبعينيات"),
    "On the ground floors: fashion and luxury shops": ("Aux rez-de-chaussée : boutiques de mode et de luxe", "На первых этажах: магазины моды и люкса", "في الطوابق الأرضية: متاجر أزياء وفخامة"),
    "Designed by Israel Lotan and Abba Elhanani, with Oscar Niemeyer": (
        "Conçue par Israel Lotan et Abba Elhanani, avec Oscar Niemeyer",
        "Проект Israel Lotan и Abba Elhanani при участии Оскара Нимейера",
        "من تصميم Israel Lotan وAbba Elhanani مع أوسكار نيماير"),
    "The ring street ה' באייר circles the square": (
        "La rue circulaire He Be’Iyar fait le tour de la place",
        "Площадь окружает кольцевая улица",
        "يحيط الشارع الدائري بالميدان"),
    "A circular bike path, wider sidewalks and four new crossings": (
        "Une piste cyclable circulaire, des trottoirs élargis et quatre nouveaux passages",
        "Кольцевая велодорожка, расширенные тротуары и четыре новых перехода",
        "مسار دائري للدراجات وأرصفة أوسع وأربعة معابر جديدة"),
    "The largest square in Israel": ("La plus grande place d’Israël", "Самая большая площадь Израиля", "أكبر ميدان في إسرائيل"),
    "Residential lot 101 and lot 303 for open space and public buildings": (
        "Le lot résidentiel 101 et le lot 303 pour les espaces ouverts et les bâtiments publics",
        "Жилой участок 101 и участок 303 под открытое пространство и общественные здания",
        "القسيمة السكنية 101 والقسيمة 303 للمساحات المفتوحة والمباني العامة"),
    # the sources (the publisher keeps its name; the words around it are translated)
    "Hebrew Wikipedia, Kikar HaMedina Towers": ("Wikipédia en hébreu, tours Kikar Hamedina", "Википедия на иврите, башни Кикар ха-Медина", "ويكيبيديا العبرية، أبراج كيكار همدينا"),
    "Ashtrom, project page": ("Ashtrom, page du projet", "Ashtrom, страница проекта", "Ashtrom، صفحة المشروع"),
    "Electra Construction, project page": ("Electra Construction, page du projet", "Electra Construction, страница проекта", "Electra Construction، صفحة المشروع"),
    "Yaski Mor Sivan Architects": ("Yaski Mor Sivan Architectes", "Архитекторы Yaski Mor Sivan", "Yaski Mor Sivan للهندسة المعمارية"),
    "Mako, 24.9.2026": ("Mako, 24/09/2026", "Mako, 24.09.2026", "Mako، 24.9.2026"),
    "Mako, 11.11.2025": ("Mako, 11/11/2025", "Mako, 11.11.2025", "Mako، 11.11.2025"),
    "Globes, 25.9.2025": ("Globes, 25/09/2025", "Globes, 25.09.2025", "Globes، 25.9.2025"),
    "Globes, 14.12.2022": ("Globes, 14/12/2022", "Globes, 14.12.2022", "Globes، 14.12.2022"),
    "Alum Eshet": ("Alum Eshet", "Alum Eshet", "Alum Eshet"),
    "Tel Aviv-Yafo municipality, building sites (file 61-1-2018-0391)": (
        "Municipalité de Tel Aviv-Jaffa, chantiers (dossier 61-1-2018-0391)",
        "Муниципалитет Тель-Авива-Яффо, стройплощадки (дело 61-1-2018-0391)",
        "بلدية تل أبيب يافا، مواقع البناء (ملف 61-1-2018-0391)"),
    "Tel Aviv-Yafo municipality buildings data": ("Données des bâtiments, municipalité de Tel Aviv-Jaffa", "Данные о зданиях, муниципалитет Тель-Авива-Яффо", "بيانات المباني، بلدية تل أبيب يافا"),
    "Local planning committee decision, 4.8.2021": ("Décision de la commission locale d’urbanisme, 04/08/2021", "Решение местной строительной комиссии, 04.08.2021", "قرار لجنة التخطيط المحلية، 4.8.2021"),
    "Wikipedia, Kikar Hamedina": ("Wikipédia en anglais, Kikar Hamedina", "Википедия на английском, Кикар ха-Медина", "ويكيبيديا الإنجليزية، كيكار همدينا"),
    "Hebrew Wikipedia, Kikar HaMedina": ("Wikipédia en hébreu, Kikar Hamedina", "Википедия на иврите, Кикар ха-Медина", "ويكيبيديا العبرية، كيكار همدينا"),
    "ynetnews": ("ynetnews", "ynetnews", "ynetnews"),
    "Tel Aviv-Yafo municipality green areas": ("Espaces verts, municipalité de Tel Aviv-Jaffa", "Зелёные зоны, муниципалитет Тель-Авива-Яффо", "المساحات الخضراء، بلدية تل أبيب يافا"),
    "Tel Aviv-Yafo municipality tree canopies, 2024": ("Canopée, municipalité de Tel Aviv-Jaffa, 2024", "Кроны деревьев, муниципалитет Тель-Авива-Яффо, 2024", "تيجان الأشجار، بلدية تل أبيب يافا، 2024"),
    "Tel Aviv-Yafo municipality street axes": ("Axes des rues, municipalité de Tel Aviv-Jaffa", "Оси улиц, муниципалитет Тель-Авива-Яффо", "محاور الشوارع، بلدية تل أبيب يافا"),
    "Plan 2500B lots, Tel Aviv-Yafo municipality": ("Lots du plan 2500B, municipalité de Tel Aviv-Jaffa", "Участки плана 2500B, муниципалитет Тель-Авива-Яффо", "قسائم المخطط 2500B، بلدية تل أبيب يافا"),
    "Tel Aviv-Yafo municipality water bodies": ("Plans d’eau, municipalité de Tel Aviv-Jaffa", "Водоёмы, муниципалитет Тель-Авива-Яффо", "المسطحات المائية، بلدية تل أبيب يافا"),
    "tlvonline, 2.11.2025": ("tlvonline, 02/11/2025", "tlvonline, 02.11.2025", "tlvonline، 2.11.2025"),
}
LANGS = ("fr", "ru", "ar")


def english_texts():
    d = json.load(io.open(os.path.join(DIR, "world.json"), encoding="utf-8"))
    seen = []

    def walk(o):
        if isinstance(o, dict):
            if isinstance(o.get("en"), str) and o["en"] not in seen:
                seen.append(o["en"])
            for k, v in o.items():
                if k != "src" and isinstance(v, (dict, list)):
                    walk(v)
        elif isinstance(o, list):
            for v in o:
                walk(v)
    for k in ("civic", "park_features", "marks", "pins", "model", "facts", "sources"):
        walk(d.get(k))
    return seen


def main():
    ok = True
    en = english_texts()
    miss = [e for e in en if e not in T]
    stale = [e for e in T if e not in en]
    if miss:
        ok = False
        print("MISSING (no translation):", *miss, sep="\n  ")
    if stale:
        ok = False
        print("STALE (not a text of world.json):", *stale, sep="\n  ")
    for e, tr in T.items():
        if len(tr) != 3:
            ok = False
            print("BAD tuple:", e)
            continue
        for l, s in zip(LANGS, tr):
            if not s.strip() or re.search(r"[֐-׿]", s) or "—" in s or "–" in s:
                ok = False
                print(f"BAD {l}: {e!r} -> {s!r}")
    if not ok:
        print("RESULT BLOCKED")
        return 1
    doc = {"v": 1, "note": "Kikar Hamedina P8 (1.72.370): the world data's texts in fr / ru / ar, keyed by the English text of world.json. "
                            "Built by scripts/project-stage/world_i18n_hamedina.py; read by assets/project-stage/world/world.js on those pages only."}
    for i, l in enumerate(LANGS):
        doc[l] = {e: T[e][i] for e in en}
    io.open(OUT, "w", encoding="utf-8", newline="\n").write(json.dumps(doc, ensure_ascii=False, separators=(",", ":")) + "\n")
    print(f"ok: {len(en)} texts x {len(LANGS)} languages -> {OUT} ({os.path.getsize(OUT)} bytes)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
