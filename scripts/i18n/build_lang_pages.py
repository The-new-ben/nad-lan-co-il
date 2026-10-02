# -*- coding: utf-8 -*-
"""LanguagePages v84 (28.9.2026): the dictionary for every block OUTSIDE the article on a project's language page
(/projects/<slug>-en|fr|ru|ar/). The owner, 28.9: "the languages has to be, and the SEO has to be perfect".

What it covers (measured on the 56 language pages, scratchpad lang/scope.py): the theme's header and footer, the
accessibility panel, the area-prices band (catalog-plus), the project's milestones (milestones.php), the price, finance and
"everything around the project" sections (project-experience.php), the card's facts (cards-render.php), the notice's
developer name (legal-notice.php). The article is real translated CMS text and is never touched.

Three kinds of entries:
  exact     a whole text node or attribute, trimmed
  patterns  a text node with numbers or a place inside it; {1}.. are the captures, a capture that is a known name is
            translated through `names`
  names     developers, cities, streets and the nearby projects' titles, also replaced inside longer text (the notice)
Arrows: Hebrew's "←" means "go on"; left-to-right pages get "→", Arabic keeps "←".

Writes plugins/nadlan-config/i18n/lang-pages.json.   python scripts/i18n/build_lang_pages.py
"""
import io, json, os, re

REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT = os.path.join(REPO, "plugins", "nadlan-config", "i18n", "lang-pages.json")
L = ("en", "fr", "ru", "ar")


def row(he, en, fr, ru, ar):
    return he, {"en": en, "fr": fr, "ru": ru, "ar": ar}


EXACT = [
    # the header (theme parts/header.html) and the skip link
    row("לדלג לתוכן", "Skip to content", "Aller au contenu", "Перейти к содержимому", "تخطَّ إلى المحتوى"),
    row("דלג לתוכן", "Skip to content", "Aller au contenu", "Перейти к содержимому", "تخطَّ إلى المحتوى"),
    # the header's tagline has about 30 characters of room (1.72.338 cut "Real estate - before you approa..."), so it is short
    row("נדל״ן לפני שפונים ליזם", "Before you call the developer", "Avant d'appeler le promoteur", "До звонка застройщику", "قبل التوجه إلى المطوّر"),
    row("פרויקטים", "Projects", "Projets", "Проекты", "مشاريع"),
    row("קטלוג תלת ממד", "3D catalogue", "Catalogue 3D", "3D-каталог", "كتالوج ثلاثي الأبعاد"),
    # the header's menu has one row (1.72.350: the French and Russian menus ran under the button, 67 and 191 px at 1440)
    row("אזורי ביקוש", "Top areas", "Quartiers", "Районы", "مناطق مطلوبة"),
    row("מחשבונים", "Calculators", "Simulateurs", "Калькуляторы", "حاسبات"),
    row('נדל"ן בחו"ל', "Property abroad", "À l'étranger", "За рубежом", "عقارات في الخارج"),
    row("נדל״ן בחו״ל", "Property abroad", "Immobilier à l'étranger", "Недвижимость за рубежом", "عقارات في الخارج"),
    row("אנשי מקצוע", "Professionals", "Professionnels", "Специалисты", "مختصون"),
    row("מתווכים", "Brokers", "Agents", "Риелторы", "وسطاء عقاريون"),
    row("מדריכים", "Guides", "Guides", "Гиды", "أدلة"),
    row("בחרו פרויקט", "Choose a project", "Choisir un projet", "Выбрать проект", "اختر مشروعاً"),
    row("פתיחת תפריט ניווט", "Open the navigation menu", "Ouvrir le menu de navigation", "Открыть меню навигации", "فتح قائمة التنقل"),
    row("ניווט ראשי", "Main navigation", "Navigation principale", "Главная навигация", "التنقل الرئيسي"),
    row("קישורי אתר", "Site links", "Liens du site", "Ссылки сайта", "روابط الموقع"),
    # the accessibility panel
    row("נגישות", "Accessibility", "Accessibilité", "Доступность", "إمكانية الوصول"),
    row("הגדרות נגישות", "Accessibility settings", "Paramètres d'accessibilité", "Настройки доступности", "إعدادات إمكانية الوصول"),
    row("תפריט נגישות", "Accessibility menu", "Menu d'accessibilité", "Меню доступности", "قائمة إمكانية الوصول"),
    row("גופן קריא", "Readable font", "Police lisible", "Удобочитаемый шрифт", "خط سهل القراءة"),
    row("הגדלת טקסט", "Larger text", "Agrandir le texte", "Увеличить текст", "تكبير النص"),
    row("הדגשת קישורים", "Highlight links", "Surligner les liens", "Выделить ссылки", "إبراز الروابط"),
    row("ניגודיות גבוהה", "High contrast", "Contraste élevé", "Высокий контраст", "تباين عالٍ"),
    row("עצירת אנימציות", "Stop animations", "Arrêter les animations", "Остановить анимацию", "إيقاف الحركة"),
    row("איפוס", "Reset", "Réinitialiser", "Сбросить", "إعادة الضبط"),
    row("סגירה", "Close", "Fermer", "Закрыть", "إغلاق"),
    # the footer (theme parts/footer.html)
    row("פרויקטים, דירות, אזורים וכלי בדיקה", "Projects, homes, areas and checking tools", "Projets, logements, quartiers et outils de vérification", "Проекты, квартиры, районы и инструменты проверки", "مشاريع وشقق ومناطق وأدوات فحص"),
    row("מידע נדל״ן, פרויקטים חדשים, סביבת מגורים וכלים לבדיקת עסקה לפני שמתקדמים לפנייה.",
        "Property information, new projects, the neighbourhood and tools to check a deal before you make an enquiry.",
        "Informations immobilières, projets neufs, cadre de vie et outils pour vérifier une transaction avant de prendre contact.",
        "Информация о недвижимости, новые проекты, район и инструменты для проверки сделки до обращения.",
        "معلومات عقارية ومشاريع جديدة وبيئة السكن وأدوات لفحص الصفقة قبل التواصل."),
    row("כל הפרויקטים", "All projects", "Tous les projets", "Все проекты", "كل المشاريع"),
    row("בדיקה לפני קנייה", "Check before you buy", "Vérifier avant d'acheter", "Проверка перед покупкой", "الفحص قبل الشراء"),
    row("מחשבון משכנתא", "Mortgage calculator", "Simulateur de prêt", "Ипотечный калькулятор", "حاسبة الرهن العقاري"),
    row("מס רכישה", "Purchase tax", "Taxe d'acquisition", "Налог на покупку", "ضريبة الشراء"),
    row("מדריך קנייה", "Buying guide", "Guide d'achat", "Руководство покупателя", "دليل الشراء"),
    row("בדיקה משפטית", "Legal check", "Vérification juridique", "Юридическая проверка", "الفحص القانوني"),
    row("מערכת NadLan", "The NadLan platform", "La plateforme NadLan", "Платформа NadLan", "منصة NadLan"),
    row("רובע שדה דב", "Sde Dov quarter", "Quartier de Sde Dov", "Район Сде-Дов", "حي سديه دوف"),
    row("אודות", "About", "À propos", "О нас", "من نحن"),
    row("צור קשר", "Contact", "Contact", "Контакты", "اتصل بنا"),
    row("המידע באתר אינו ייעוץ משפטי, פיננסי או שמאי. יש לבדוק כל נתון מול הגורמים המוסמכים.",
        "The information on this site is not legal, financial or valuation advice. Check every figure with the competent bodies.",
        "Les informations de ce site ne constituent pas un conseil juridique, financier ou d'évaluation. Vérifiez chaque donnée auprès des instances compétentes.",
        "Информация на сайте не является юридической, финансовой или оценочной консультацией. Проверяйте каждую цифру в уполномоченных органах.",
        "المعلومات في الموقع ليست استشارة قانونية أو مالية أو تقييمية. يجب التحقق من كل معطى لدى الجهات المختصة."),
    row("תנאי שימוש", "Terms of use", "Conditions d'utilisation", "Условия использования", "شروط الاستخدام"),
    row("מדיניות פרטיות", "Privacy policy", "Politique de confidentialité", "Политика конфиденциальности", "سياسة الخصوصية"),
    row("הצהרת נגישות", "Accessibility statement", "Déclaration d'accessibilité", "Заявление о доступности", "بيان إمكانية الوصول"),
    row("מפת האתר המלאה: כל הכלים, המדריכים והמאגרים ←", "The full site map: every tool, guide and database →", "Le plan complet du site : tous les outils, guides et bases de données →", "Полная карта сайта: все инструменты, руководства и базы данных →", "خريطة الموقع الكاملة: كل الأدوات والأدلة وقواعد البيانات ←"),
    # the area-prices band under the lead (catalog-plus)
    row("מחירי הסביבה", "Local prices", "Prix du quartier", "Цены в районе", "أسعار المنطقة"),
    row("בפרויקט, לפי היזם", "In the project, per the developer", "Dans le projet, selon le promoteur", "В проекте, по данным застройщика", "في المشروع، بحسب المطوّر"),
    row("לא מחייב", "Non-binding", "Non contractuel", "Не является обязательством", "غير ملزم"),
    row("יד שנייה וחדש", "Resale and new", "Ancien et neuf", "Вторичное и новое жильё", "مستعمل وجديد"),
    row("המחירים הם של הסביבה, לא של הדירות בפרויקט. מחיר הדירה נקבע מול היזם.",
        "These are local prices, not the prices of the project's apartments. An apartment's price is set with the developer.",
        "Ce sont les prix du quartier, pas ceux des appartements du projet. Le prix d'un appartement se fixe avec le promoteur.",
        "Это цены в районе, а не цены квартир в проекте. Цена квартиры устанавливается с застройщиком.",
        "هذه أسعار المنطقة وليست أسعار شقق المشروع. يُحدَّد سعر الشقة مع المطوّر."),
    row("כל הפרויקטים החדשים", "All new projects", "Tous les projets neufs", "Все новые проекты", "كل المشاريع الجديدة"),
    # where the project stands (milestones)
    row("איפה הפרויקט עומד", "Where the project stands", "Où en est le projet", "На каком этапе проект", "أين يقف المشروع"),
    row("תכנון", "Planning", "Planification", "Проектирование", "التخطيط"),
    row("היתר בנייה", "Building permit", "Permis de construire", "Разрешение на строительство", "رخصة البناء"),
    row("שיווק ומכירות", "Marketing and sales", "Commercialisation et ventes", "Маркетинг и продажи", "التسويق والمبيعات"),
    row("בנייה", "Construction", "Construction", "Строительство", "البناء"),
    row("השלב כפי שדווח לפרויקט; לוחות הזמנים באחריות היזם.", "The stage as reported for the project; timelines are the developer's responsibility.", "L'étape telle que déclarée pour le projet ; les délais relèvent du promoteur.", "Этап указан по данным проекта; за сроки отвечает застройщик.", "المرحلة كما أُبلغ عنها للمشروع؛ الجداول الزمنية من مسؤولية المطوّر."),
    row("בבנייה", "Under construction", "En construction", "Строится", "قيد البناء"),
    row("בשיווק", "On sale", "En commercialisation", "В продаже", "في مرحلة التسويق"),
    row("בהקמה", "Under development", "En cours de réalisation", "В стадии реализации", "قيد الإنشاء"),
    row("בהיתר בנייה", "At the building-permit stage", "Au stade du permis de construire", "На стадии разрешения на строительство", "في مرحلة رخصة البناء"),
    row("הושלם", "Completed", "Achevé", "Завершён", "مكتمل"),
    row("באכלוס", "Being occupied", "En cours de livraison", "Заселяется", "قيد الإسكان"),
    # the price section (project-experience)
    row("מחיר: איפה הפרויקט עומד מול הסביבה", "Price: where the project stands against its area", "Prix : où se situe le projet par rapport au quartier", "Цена: как проект соотносится с районом", "السعر: أين يقف المشروع مقارنة بالمنطقة"),
    row("מחירים והשוואה", "Prices and comparison", "Prix et comparaison", "Цены и сравнение", "الأسعار والمقارنة"),
    row("מחיר ממוצע למ״ר בפרויקט. אומדן לא מחייב.", "Average price per m² in the project. A non-binding estimate.", "Prix moyen au m² dans le projet. Estimation non contractuelle.", "Средняя цена за м² в проекте. Необязывающая оценка.", "متوسط سعر المتر المربع في المشروع. تقدير غير ملزم."),
    row("פרויקטים סמוכים להשוואה · מבוסס על קטלוג נדלן", "Nearby projects to compare · based on the NadLan catalogue", "Projets voisins à comparer · d'après le catalogue NadLan", "Соседние проекты для сравнения · по каталогу NadLan", "مشاريع مجاورة للمقارنة · بحسب كتالوج NadLan"),
    row("פרויקט", "Project", "Projet", "Проект", "المشروع"),
    row("₪/מ״ר", "₪/m²", "₪/m²", "₪/м²", "₪/م²"),
    row("מרחק", "Distance", "Distance", "Расстояние", "المسافة"),
    row("כל המחירים, המוסדות והתוכניות - על המפה החיה למטה ←", "Every price, institution and plan on the area map below →", "Tous les prix, établissements et plans sur la carte du quartier ci-dessous →", "Все цены, учреждения и планы на карте района ниже →", "كل الأسعار والمؤسسات والمخططات على خريطة المنطقة أدناه ←"),
    row("כל המחירים, המוסדות והתוכניות על מפת האזור ←", "Every price, institution and plan on the area map →", "Tous les prix, établissements et plans sur la carte du quartier →", "Все цены, учреждения и планы на карте района →", "كل الأسعار والمؤسسات والمخططات على خريطة المنطقة ←"),
    row("האומדנים מבוססים על נתונים גלויים בקטלוג נדלן ואינם מחייבים. יש לאמת מחירים מול היזם.",
        "The estimates are based on public data in the NadLan catalogue and are not binding. Verify prices with the developer.",
        "Les estimations reposent sur des données publiques du catalogue NadLan et ne sont pas contractuelles. Vérifiez les prix auprès du promoteur.",
        "Оценки основаны на открытых данных каталога NadLan и не являются обязательством. Проверяйте цены у застройщика.",
        "التقديرات مبنية على بيانات علنية في كتالوج NadLan وهي غير ملزمة. يجب التحقق من الأسعار لدى المطوّر."),
    # finance
    row("מימון, ייעוץ ועיצוב - הכל במקום אחד", "Financing, advice and design, all in one place", "Financement, conseil et design, tout au même endroit", "Финансирование, консультации и дизайн в одном месте", "التمويل والاستشارة والتصميم في مكان واحد"),
    row("מימון וליווי", "Financing and support", "Financement et accompagnement", "Финансирование и сопровождение", "التمويل والمرافقة"),
    row("לחישוב אישי במחשבון המשכנתא ←", "Your own figure in the mortgage calculator →", "Votre calcul personnel dans le simulateur de prêt →", "Личный расчёт в ипотечном калькуляторе →", "حساب شخصي في حاسبة الرهن العقاري ←"),
    # everything around the project
    row("כל מה שסביב הפרויקט", "Everything around the project", "Tout autour du projet", "Всё вокруг проекта", "كل ما يحيط بالمشروع"),
    row("כל המידע סביב הפרויקט", "All the information around the project", "Toutes les informations autour du projet", "Вся информация вокруг проекта", "كل المعلومات حول المشروع"),
    row("פרופיל, רישום ופרויקטים נוספים ←", "Profile, registration and other projects →", "Profil, immatriculation et autres projets →", "Профиль, регистрация и другие проекты →", "الملف والتسجيل ومشاريع أخرى ←"),
    row("בעלי מקצוע", "Professionals", "Professionnels", "Специалисты", "مختصون"),
    row("עו״ד מקרקעין, שמאים, בדק בית ←", "Property lawyers, appraisers, home inspection →", "Avocats en immobilier, experts, inspection du logement →", "Юристы по недвижимости, оценщики, осмотр жилья →", "محامو عقارات ومثمّنون وفحص المنزل ←"),
    row("כמה תשלמו בחודש ←", "What you will pay each month →", "Ce que vous paierez chaque mois →", "Сколько вы будете платить в месяц →", "كم ستدفعون شهرياً ←"),
    row("מדריך קנייה מקבלן", "Guide: buying from a developer", "Guide : acheter auprès d'un promoteur", "Руководство: покупка у застройщика", "دليل الشراء من المطوّر"),
    row("שלב-אחר-שלב, ערבויות חוק מכר ←", "Step by step, Sale Law guarantees →", "Étape par étape, garanties de la loi sur la vente →", "Шаг за шагом, гарантии по Закону о продаже →", "خطوة بخطوة، ضمانات قانون البيع ←"),
    row("מילון מונחים", "Glossary", "Glossaire", "Словарь терминов", "معجم المصطلحات"),
    row("תמ״א, פינוי-בינוי, הערת אזהרה ←", "TAMA, Pinui-Binui, warning note →", "TAMA, Pinouï-Binouï, note d'avertissement →", "ТАМА, «Пинуй-Бинуй», предупредительная запись →", "تاما، الإخلاء والبناء، ملاحظة تحذيرية ←"),
    # the card's facts (cards-render)
    row("עיר", "City", "Ville", "Город", "المدينة"),
    row("יזם", "Developer", "Promoteur", "Застройщик", "المطوّر"),
    row("קבלן", "Contractor", "Entrepreneur", "Подрядчик", "المقاول"),
    row("סוג פרויקט", "Project type", "Type de projet", "Тип проекта", "نوع المشروع"),
    row("סטטוס", "Status", "Statut", "Статус", "الحالة"),
    row("יחידות דיור", "Housing units", "Logements", "Жилых единиц", "وحدات سكنية"),
    row('יח"ד קיימות', "Existing units", "Logements existants", "Существующих квартир", "وحدات قائمة"),
    row('יח"ד נוספות', "Added units", "Logements ajoutés", "Дополнительных квартир", "وحدات إضافية"),
    row("מספר תוכנית", "Plan number", "Numéro du plan", "Номер плана", "رقم المخطط"),
    row("שנת תוקף", "Completion year", "Année d'achèvement", "Год завершения", "سنة الإنجاز"),
    row("אתר", "Website", "Site web", "Сайт", "الموقع الإلكتروني"),
    row("בנייה חדשה", "New build", "Construction neuve", "Новостройка", "بناء جديد"),
    row("משרדים ומסחר", "Offices and retail", "Bureaux et commerces", "Офисы и торговля", "مكاتب وتجارة"),
    # the head's structured data (Yoast's WebSite piece, the site's tagline), 28.9.2026
    row("פרויקטים חדשים, דירות, אנשי מקצוע ומחשבונים - רואים הכל לפני שקונים",
        "New projects, apartments, professionals and calculators - see everything before you buy",
        "Projets neufs, appartements, professionnels et calculateurs - tout voir avant d'acheter",
        "Новые проекты, квартиры, специалисты и калькуляторы - всё видно до покупки",
        "مشاريع جديدة وشقق ومختصون وحاسبات - كل شيء أمامكم قبل الشراء"),
]

# {1}.. = the captures; a capture that is a known name goes through NAMES
PATTERNS = [
    (r"^כמה עולה דירה ב(.+)\?$", "What does an apartment cost in {1}?", "Combien coûte un appartement à {1} ?", "Сколько стоит квартира в городе {1}?", "كم يبلغ سعر شقة في {1}؟"),
    (r"^עסקאות שדווחו לרשות המסים, ([\d.]+) עד ([\d.]+?)\. חציון של דירות בבתי קומות\. מ[־-]?(\d{4}) עד (\d{4}): ([+\-−]?\d+%) במחיר למ[״\"]ר בעיר\.$",
     "Deals reported to the Tax Authority, {1} to {2}. The median of apartments in multi-storey buildings. {3} to {4}: {5} in the city's price per m².",
     "Transactions déclarées à l'administration fiscale, de {1} à {2}. Médiane des appartements en immeubles collectifs. De {3} à {4} : {5} sur le prix au m² de la ville.",
     "Сделки, заявленные в Налоговое управление, с {1} по {2}. Медиана по квартирам в многоквартирных домах. С {3} по {4}: {5} к цене за м² в городе.",
     "صفقات أُبلغت بها سلطة الضرائب، من {1} حتى {2}. الوسيط لشقق في مبانٍ متعددة الطوابق. من {3} حتى {4}: {5} في سعر المتر المربع في المدينة."),
    (r"^מחיר למ[״\"]ר ב(.+)$", "Price per m² in {1}", "Prix au m² à {1}", "Цена за м² в городе {1}", "سعر المتر المربع في {1}"),
    (r"^([\d,]+) עסקאות$", "{1} deals", "{1} transactions", "Сделок: {1}", "عدد الصفقات: {1}"),
    (r"^([\d,]+) ₪ למ[״\"]ר$", "{1} ₪ per m²", "{1} ₪ le m²", "{1} ₪ за м²", "{1} ₪ للمتر المربع"),
    (r"^דירת (\d+) חדרים ב(.+), חציון$", "{1}-room apartment in {2}, median", "Appartement de {1} pièces à {2}, médiane", "{1}-комнатная квартира в городе {2}, медиана", "شقة من {1} غرف في {2}، الوسيط"),
    (r"^ברחוב (.+)$", "On {1} Street", "Rue {1}", "Улица {1}", "في شارع {1}"),
    (r"^עוד פרויקטים חדשים ב(.+)$", "More new projects in {1}", "Autres projets neufs à {1}", "Другие новые проекты в городе {1}", "مشاريع جديدة أخرى في {1}"),
    (r"^טופס (\d+) ומסירה$", "Form {1} and handover", "Formulaire {1} et livraison", "Форма {1} и сдача", "النموذج {1} والتسليم"),
    (r"^~([\d,]+) ₪/מ[״\"]ר$", "~{1} ₪/m²", "~{1} ₪/m²", "~{1} ₪/м²", "~{1} ₪/م²"),
    (r"^מחיר ממוצע למ[״\"]ר בפרויקט, דירות (\d+)-(\d+) מ[״\"]ר\. אומדן לא מחייב\.$",
     "Average price per m² in the project, apartments of {1}-{2} m². A non-binding estimate.",
     "Prix moyen au m² dans le projet, appartements de {1} à {2} m². Estimation non contractuelle.",
     "Средняя цена за м² в проекте, квартиры {1}-{2} м². Необязывающая оценка.",
     "متوسط سعر المتر المربع في المشروع، شقق من {1} إلى {2} م². تقدير غير ملزم."),
    (r"^([\d.,]+) מ[׳']$", "{1} m", "{1} m", "{1} м", "{1} م"),
    (r"^([\d.,]+) ק[״\"]מ$", "{1} km", "{1} km", "{1} км", "{1} كم"),
    (r"^סדר גודל של החזר חודשי לדירת ~(\d+) מ[״\"]ר\. אומדן לא מחייב, תלוי במסלול ובריבית\.$",
     "The order of magnitude of the monthly repayment for a ~{1} m² apartment. A non-binding estimate that depends on the loan track and the rate.",
     "Ordre de grandeur de la mensualité pour un appartement d'environ {1} m². Estimation non contractuelle, selon le type de prêt et le taux.",
     "Примерный ежемесячный платёж за квартиру ~{1} м². Необязывающая оценка, зависит от программы и ставки.",
     "حجم تقريبي للقسط الشهري لشقة بمساحة ~{1} م². تقدير غير ملزم، يعتمد على المسار والفائدة."),
    (r"^היזם: (.+)$", "Developer: {1}", "Promoteur : {1}", "Застройщик: {1}", "المطوّر: {1}"),
    (r"^בעלי מקצוע ב(.+)$", "Professionals in {1}", "Professionnels à {1}", "Специалисты в городе {1}", "مختصون في {1}"),
    (r"^מדרגות (\d{4}) ומחשבון ←$", "The {1} brackets and a calculator →", "Les tranches {1} et un simulateur →", "Ставки {1} и калькулятор →", "شرائح {1} والحاسبة ←"),
    # Kikar Hamedina P8 (1.72.370): the project card's source line (inc/cards-render.php) on a language page whose "source" meta
    # is in that language; a Hebrew source stays as it was (a capture with Hebrew the dictionary does not know keeps the line)
    (r"^המקור: (.+) · עודכן (\d{2}/\d{2}/\d{4})$", "Source: {1} · updated {2}", "Source : {1} · mis à jour le {2}", "Источник: {1} · обновлено {2}", "المصدر: {1} · حُدّث في {2}"),
]

# names: developers, places, streets, the nearby projects' titles (the Latin brand is kept as the developer writes it)
NAMES = [
    row("תל אביב יפו", "Tel Aviv-Yafo", "Tel Aviv-Jaffa", "Тель-Авив-Яффо", "تل أبيب يافا"),
    row("תל אביב-יפו", "Tel Aviv-Yafo", "Tel Aviv-Jaffa", "Тель-Авив-Яффо", "تل أبيب يافا"),
    row("בני ברק", "Bnei Brak", "Bnei Brak", "Бней-Брак", "بني براك"),
    row("אבן גבירול", "Ibn Gabirol", "Ibn Gabirol", "Ибн Гвироль", "ابن جبيرول"),
    row("ישראל קנדה", "Israel Canada", "Israel Canada", "Israel Canada", "Israel Canada"),
    row("י.ח דמרי", "Y.H. Dimri", "Y.H. Dimri", "Y.H. Dimri", "Y.H. Dimri"),
    row("אפריקה ישראל מגורים", "Africa Israel Residences", "Africa Israel Residences", "Africa Israel Residences", "Africa Israel Residences"),
    row('אמות השקעות ואלייד נדל"ן', "Amot Investments and Allied Real Estate", "Amot Investments et Allied Real Estate", "Amot Investments и Allied Real Estate", "Amot Investments وAllied Real Estate"),
    row("אמות השקעות וגב-ים", "Amot Investments and Gav-Yam", "Amot Investments et Gav-Yam", "Amot Investments и Gav-Yam", "Amot Investments وGav-Yam"),
    row("Rainbow Tel Aviv - ריינבו תל אביב", "Rainbow Tel Aviv", "Rainbow Tel Aviv", "Rainbow Tel Aviv", "Rainbow Tel Aviv"),
    row("ZOHI זוהי שדה דב - לוינשטין מבנה אלייד", "ZOHI Sde Dov", "ZOHI Sde Dov", "ZOHI Sde Dov", "ZOHI Sde Dov"),
    row("DIMRI YAMA שדה דב - י.ח דמרי", "DIMRI YAMA Sde Dov", "DIMRI YAMA Sde Dov", "DIMRI YAMA Sde Dov", "DIMRI YAMA Sde Dov"),
    row("GINDI VOGUE שדה דב - פרוייקט גינדי ווג", "GINDI VOGUE Sde Dov", "GINDI VOGUE Sde Dov", "GINDI VOGUE Sde Dov", "GINDI VOGUE Sde Dov"),
    row("ASHIRA - פרויקט אשירה שדה דב תל אביב מחיר", "ASHIRA Sde Dov", "ASHIRA Sde Dov", "ASHIRA Sde Dov", "ASHIRA Sde Dov"),
    row("FIRST שדה דב - קבוצת חג'ג'", "FIRST Sde Dov", "FIRST Sde Dov", "FIRST Sde Dov", "FIRST Sde Dov"),
    # v104.27 (2.10.2026): Kikar Hamedina in the neighbours' comparison table; the names its own language pages use (Arabic titles in English, owner 28.9)
    row("מגדלי כיכר המדינה, תל אביב", "Kikar Hamedina Towers, Tel Aviv", "Tours Kikar Hamedina, Tel Aviv", "Башни Кикар ха-Медина, Тель-Авив", "Kikar Hamedina Towers, Tel Aviv"),
    row("הרברט סמואל SIX-8 תל אביב - דירות יוקרה בקו הראשון לים", "SIX-8 Herbert Samuel Tel Aviv", "SIX-8 Herbert Samuel Tel Aviv", "SIX-8 Herbert Samuel Tel Aviv", "SIX-8 Herbert Samuel Tel Aviv"),
]


def main():
    ex, seen = {}, set()
    for he, tr in EXACT:
        assert he not in seen, he
        seen.add(he)
        for l in L:
            assert tr[l] and not re.search(r"[֐-׿]", tr[l]), (he, l)
        ex[he] = tr
    pats = []
    for p in PATTERNS:
        # a quote needs no backslash in a class, and the browser (i18n-dom.js, RegExp with the u flag) refuses \" there
        p = (p[0].replace('\\"', '"'),) + tuple(p[1:])
        re.compile(p[0])
        n = re.compile(p[0]).groups
        tr = dict(zip(L, p[1:]))
        for l in L:
            for k in range(1, n + 1):
                assert "{%d}" % k in tr[l], (p[0], l, k)
            assert not re.search(r"[֐-׿]", tr[l]), (p[0], l)
        pats.append({"re": p[0], **tr})
    names = {}
    for he, tr in NAMES:
        names[he] = tr
    doc = {"note": "LanguagePages v84 (28.9.2026): the words outside the article on a project's language page. Built by scripts/i18n/build_lang_pages.py; read by inc/lang-pages.php. Keys are the exact Hebrew the site prints.",
           "exact": ex, "patterns": pats, "names": names}
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    io.open(OUT, "w", encoding="utf-8", newline="\n").write(json.dumps(doc, ensure_ascii=False, indent=1) + "\n")
    print("ok", len(ex), "exact,", len(pats), "patterns,", len(names), "names ->", OUT)


if __name__ == "__main__":
    main()
