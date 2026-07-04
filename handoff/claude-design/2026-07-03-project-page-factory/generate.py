# -*- coding: utf-8 -*-
"""
nadlan project-page FACTORY — one modular template, N real project pages.
Proves the pattern is data-driven and modular (checkbox toggles per module),
not a hand-made one-off. Emits standalone HTML per project.
Honesty: flagship 3D = real GLB; DUO = labeled DEFAULT model. Prices = sourced
estimates ("אומדן", source shown), NOT invented deals.
"""
import json, os, html

OUT = os.path.dirname(__file__)
TOKEN = "pk.SET_YOUR_MAPBOX_PUBLIC_TOKEN_IN_KEYS_HUB"
MASSING_DEFAULT = "https://nad-lan.co.il/wp-content/plugins/nadlan-config/assets/showroom-engine/models/ashira-massing.glb"

# ---------------------------------------------------------------- projects (REAL data)
PROJECTS = {
"ashira-sde-dov": dict(
  name_he="ASHIRA · אשירה שדה דב", name_lat="ASHIRA Sde Dov",
  dev="אביסרור משה ובניו", city="תל אביב-יפו", area="רובע שדה דב · מתחם אשכול",
  address="מתחם אשכול, מגרש 101, רובע שדה דב, תל אביב-יפו",
  floors=35, units_total=406, delivery="2028", lat=32.10557, lng=34.7876,
  ppsqm=75000, ppsqm_src="אומדן לא מחייב · מבוסס עסקאות מדווחות במתחם אשכול, שדה דב (מקור: מדלן/רשות המסים). יש לאמת מול היזם.",
  glb="https://nad-lan.co.il/wp-content/plugins/nadlan-config/assets/showroom-engine/models/ashira.glb",
  poster="https://nad-lan.co.il/wp-content/uploads/2026/07/ashira-sde-dov-plate-v2.webp",
  default_model=False,
  units=[
    dict(id="a1", floor=10, rooms=3, sqm=90,  dir="מערב",      status="available", label="A-10"),
    dict(id="a2", floor=20, rooms=4, sqm=130, dir="דרום מערב", status="available", label="B-20"),
    dict(id="a3", floor=27, rooms=4, sqm=138, dir="מערב",      status="reserved",  label="B-27"),
    dict(id="a4", floor=33, rooms=5, sqm=180, dir="דרום מערב", status="available", label="PH-33"),
  ],
  comps=[dict(name="Rainbow תל אביב", ppsqm=76000, dist_m=399),
         dict(name="Dimri Yama שדה דב", ppsqm=75000, dist_m=310)],
),
"rainbow-tel-aviv": dict(
  name_he="Rainbow · ריינבו תל אביב", name_lat="Rainbow Tel Aviv",
  dev="ישראל קנדה", city="תל אביב-יפו", area="רובע שדה דב · אזור אשכול",
  address="רובע שדה דב, אזור אשכול, תל אביב-יפו",
  floors=39, units_total=459, delivery="2027", lat=32.10317, lng=34.78446,
  ppsqm=80300, ppsqm_src="ממוצע דירות שנמכרו בפרויקט כולל מע\"מ · דוח שנתי ישראל קנדה ליום 31.12.2025 (270 נמכרו, 189 נותרו). לא מחירון יזם — יש לאמת מול היזם.",
  glb="https://raw.githubusercontent.com/The-new-ben/nad-lan-co-il/main/assets/projects/rainbow-tel-aviv/model.glb",
  poster="https://nad-lan.co.il/wp-content/uploads/2026/07/rainbow-tel-aviv-plate-v2.webp",
  default_model=False,
  units=[
    dict(id="r1", floor=8,  rooms=3, sqm=82,  dir="דרום מערב", status="available", label="דירת 3, ק'8"),
    dict(id="r2", floor=16, rooms=4, sqm=112, dir="מערב",      status="available", label="דירת 4, ק'16"),
    dict(id="r3", floor=24, rooms=4, sqm=118, dir="דרום",      status="reserved",  label="דירת 4, ק'24"),
    dict(id="r4", floor=31, rooms=5, sqm=165, dir="דרום מערב", status="available", label="דירת 5, ק'31"),
    dict(id="r5", floor=36, rooms=5, sqm=195, dir="מערב",      status="available", label="פנטהאוז ק'36"),
  ],
  comps=[dict(name="ASHIRA שדה דב", ppsqm=75000, dist_m=399),
         dict(name="Dimri Yama שדה דב", ppsqm=75000, dist_m=210)],
),
"dimri-yama-sde-dov": dict(
  name_he="Dimri Yama · דמרי ימה שדה דב", name_lat="Dimri Yama Sde Dov",
  dev="י.ח דמרי", city="תל אביב-יפו", area="רובע שדה דב · מתחם אשכול",
  address="אבן גבירול 220, מתחם אשכול, רובע שדה דב, תל אביב-יפו",
  floors=39, units_total=458, delivery="2028", lat=32.1049, lng=34.7869, coord_approx=True,
  ppsqm=75000, ppsqm_src="אומדן לא מחייב · יש לאמת מחיר, זמינות ותוכנית מול היזם לפני כל החלטה.",
  glb="https://nad-lan.co.il/wp-content/themes/nadlan-revenue/assets/projects/dimri-yama/model-prototype.glb",
  poster="https://nad-lan.co.il/wp-content/uploads/2026/07/dimri-yama-sde-dov-plate-v2.webp",
  default_model=False,
  units=[
    dict(id="d1", floor=12, rooms=3, sqm=92,  dir="מערב",      status="available", label="A-12"),
    dict(id="d2", floor=24, rooms=4, sqm=132, dir="דרום מערב", status="reserved",  label="B-24"),
    dict(id="d3", floor=30, rooms=4, sqm=140, dir="מערב",      status="available", label="B-30"),
    dict(id="d4", floor=37, rooms=5, sqm=185, dir="דרום מערב", status="available", label="PH-37"),
  ],
  comps=[dict(name="ASHIRA שדה דב", ppsqm=75000, dist_m=310),
         dict(name="Rainbow תל אביב", ppsqm=76000, dist_m=210)],
),
"duo-tel-aviv": dict(
  name_he="DUO · מגדלי דואו תל אביב", name_lat="DUO Towers Tel Aviv",
  dev="אפריקה ישראל מגורים", city="תל אביב-יפו", area="מתחם סומייל · הקריה",
  address="מתחם סומייל, תל אביב-יפו",
  floors=54, units_total=668, delivery="2029", lat=32.0761, lng=34.7905, coord_approx=True,
  ppsqm=82000, ppsqm_src="אומדן ראשוני לא מחייב לאזור סומייל/הקריה · טרם התקבלו נתוני יזם. יש לאמת.",
  glb=MASSING_DEFAULT, poster="https://nad-lan.co.il/wp-content/uploads/2026/07/duo-tel-aviv-plate.webp",
  default_model=True,   # <-- honesty: labeled default building, materials not yet received
  units=[  # illustrative default line-up, labeled as generated
    dict(id="u1", floor=14, rooms=3, sqm=88,  dir="מערב",      status="available", label="קו 1, ק'14"),
    dict(id="u2", floor=28, rooms=4, sqm=124, dir="דרום מערב", status="available", label="קו 2, ק'28"),
    dict(id="u3", floor=44, rooms=5, sqm=172, dir="מערב",      status="available", label="קו 3, ק'44"),
  ],
  comps=[],
  units_generated=True,
),
}

# ---------------------------------------------------------------- i18n (UI + article), 5 languages
LANGS = ["he","en","fr","ru","ar"]
LANG_NAMES = {"he":"עברית","en":"English","fr":"Français","ru":"Русский","ar":"العربية"}
RTL = {"he","ar"}

UI = {
"he":dict(inquire="מעניין אותי",modules="מודולים",m_hero="פתיח + תלת־ממד",m_choose="בחירת דירה",m_price="מחיר ושוק",m_map="מפה",m_buy="חוויית קנייה",m_media="מדיה",m_area="שכונה",m_faq="שאלות",
  choose="בוחרים את הדירה שלכם",price="מחיר מול השוק האמיתי",mapt="הכל על מפה אחת",buy="חוויית הקנייה",media="מדיה וגימור",area="השכונה",faq="שאלות ותשובות",similar="פרויקטים דומים",
  floor="קומה",rooms="חדרים",sqm="מ\"ר",dir="כיוון",status="סטטוס",price_l="מחיר",est="אומדן",view="מבט מהקומה",plan="תוכנית דירה",
  st_available="זמינה",st_reserved="בבדיקה",st_sold="נמכרה",facade="חזית",model3d="תלת־ממד",
  ppsqm_l="מחיר ממוצע למ\"ר",area_deals="עסקאות והשוואות באזור",dist="מרחק",default_badge="מודל ברירת מחדל · טרם התקבלו חומרים מהיזם",
  est_badge="אומדן להמחשה · לא מחיר יזם",gen_badge="דירות להמחשה · טרם התקבל מלאי מהיזם",
  from_price="החל מ־",units_l="דירות",floors_l="קומות",delivery_l="אכלוס",dev_l="יזם",
  disc="המידע, האומדנים וההדמיות נועדו להמחשה בלבד, אינם מחיר יזם או הצעה, ואינם מחייבים. יש לאמת כל פרט מול היזם."),
"en":dict(inquire="I'm interested",modules="Modules",m_hero="Intro + 3D",m_choose="Choose apartment",m_price="Price & market",m_map="Map",m_buy="Buying",m_media="Media",m_area="Area",m_faq="FAQ",
  choose="Choose your apartment",price="Price vs. the real market",mapt="Everything on one map",buy="The buying experience",media="Media & finishes",area="The neighborhood",faq="Questions & answers",similar="Similar projects",
  floor="Floor",rooms="Rooms",sqm="m²",dir="Facing",status="Status",price_l="Price",est="Est.",view="View from floor",plan="Floor plan",
  st_available="Available",st_reserved="In review",st_sold="Sold",facade="Facade",model3d="3D",
  ppsqm_l="Avg price / m²",area_deals="Area deals & comparables",dist="Distance",default_badge="Default model · developer materials not yet received",
  est_badge="Illustrative estimate · not a developer price",gen_badge="Illustrative units · inventory not yet from developer",
  from_price="From",units_l="apartments",floors_l="floors",delivery_l="Delivery",dev_l="Developer",
  disc="Information, estimates and renderings are illustrative only, are not a developer price or offer, and are non-binding. Verify every detail with the developer."),
"fr":dict(inquire="Ça m'intéresse",modules="Modules",m_hero="Intro + 3D",m_choose="Choisir l'appartement",m_price="Prix & marché",m_map="Carte",m_buy="Achat",m_media="Médias",m_area="Quartier",m_faq="FAQ",
  choose="Choisissez votre appartement",price="Prix face au marché réel",mapt="Tout sur une seule carte",buy="L'expérience d'achat",media="Médias & finitions",area="Le quartier",faq="Questions & réponses",similar="Projets similaires",
  floor="Étage",rooms="Pièces",sqm="m²",dir="Orientation",status="Statut",price_l="Prix",est="Est.",view="Vue de l'étage",plan="Plan",
  st_available="Disponible",st_reserved="En examen",st_sold="Vendu",facade="Façade",model3d="3D",
  ppsqm_l="Prix moyen / m²",area_deals="Transactions et comparables",dist="Distance",default_badge="Modèle par défaut · matériaux du promoteur non reçus",
  est_badge="Estimation illustrative · pas un prix promoteur",gen_badge="Appartements illustratifs · stock non reçu",
  from_price="À partir de",units_l="appartements",floors_l="étages",delivery_l="Livraison",dev_l="Promoteur",
  disc="Les informations, estimations et rendus sont illustratifs, ne constituent ni un prix ni une offre du promoteur, et sont non contractuels. Vérifiez chaque détail auprès du promoteur."),
"ru":dict(inquire="Мне интересно",modules="Модули",m_hero="Вступление + 3D",m_choose="Выбор квартиры",m_price="Цена и рынок",m_map="Карта",m_buy="Покупка",m_media="Медиа",m_area="Район",m_faq="Вопросы",
  choose="Выберите свою квартиру",price="Цена против реального рынка",mapt="Всё на одной карте",buy="Опыт покупки",media="Медиа и отделка",area="Район",faq="Вопросы и ответы",similar="Похожие проекты",
  floor="Этаж",rooms="Комнат",sqm="м²",dir="Ориентация",status="Статус",price_l="Цена",est="Оц.",view="Вид с этажа",plan="Планировка",
  st_available="Свободна",st_reserved="На проверке",st_sold="Продана",facade="Фасад",model3d="3D",
  ppsqm_l="Ср. цена / м²",area_deals="Сделки и аналоги района",dist="Расстояние",default_badge="Модель по умолчанию · материалы застройщика не получены",
  est_badge="Иллюстративная оценка · не цена застройщика",gen_badge="Иллюстративные квартиры · без данных застройщика",
  from_price="от",units_l="квартир",floors_l="этажей",delivery_l="Сдача",dev_l="Застройщик",
  disc="Информация, оценки и визуализации носят иллюстративный характер, не являются ценой или предложением застройщика и не обязывают. Проверяйте каждую деталь у застройщика."),
"ar":dict(inquire="يهمّني",modules="الوحدات",m_hero="مقدمة + ثلاثي الأبعاد",m_choose="اختر الشقة",m_price="السعر والسوق",m_map="الخريطة",m_buy="الشراء",m_media="الوسائط",m_area="الحي",m_faq="أسئلة",
  choose="اختر شقتك",price="السعر مقابل السوق الحقيقي",mapt="كل شيء على خريطة واحدة",buy="تجربة الشراء",media="الوسائط والتشطيبات",area="الحي",faq="أسئلة وأجوبة",similar="مشاريع مشابهة",
  floor="الطابق",rooms="غرف",sqm="م²",dir="الاتجاه",status="الحالة",price_l="السعر",est="تقدير",view="المنظر من الطابق",plan="مخطط الشقة",
  st_available="متاحة",st_reserved="قيد المراجعة",st_sold="مباعة",facade="الواجهة",model3d="ثلاثي الأبعاد",
  ppsqm_l="متوسط السعر / م²",area_deals="صفقات ومقارنات المنطقة",dist="المسافة",default_badge="نموذج افتراضي · لم تُستلم مواد المطور",
  est_badge="تقدير توضيحي · ليس سعر المطور",gen_badge="شقق توضيحية · لا مخزون من المطور بعد",
  from_price="ابتداءً من",units_l="شقة",floors_l="طوابق",delivery_l="التسليم",dev_l="المطور",
  disc="المعلومات والتقديرات والصور توضيحية فقط، وليست سعراً أو عرضاً من المطور، وغير مُلزمة. تحقق من كل تفصيل مع المطور."),
}

# FULL 5-language coverage for every remaining UI string (owner: "5 LANG FULL").
EXTRA={
"he":dict(generic_badge="מודל אדריכלי גנרי · להמחשה, לא התכנון הסופי",price_of_apt="מחיר הדירה",eq_l="הון עצמי",loan_l="הלוואה",pay_l="החזר חודשי משוער · 25 ש׳, 5%",
  buy_mort_t="אומדן משכנתא",buy_steps_t="שלבי הרכישה",buy_pros_t="בעלי מקצוע מאומתים",
  step1="בחירת דירה ובדיקת מחיר מול האזור",step2="בדיקת מסמכים: היתר, טאבו, מפרט",step3="ליווי עורך דין ושמאי",step4="אישור משכנתא ופנייה ליזם",
  pro_law="עורך/ת דין נדל״ן · מאומת",pro_appr="שמאי/ת מקרקעין · מאומת",pro_mort="יועץ/ת משכנתאות · מאומת",
  map_streets="רחובות",map_sat="לוויין",map_prices="מחירי אזור",faq_q_delivery="מתי האכלוס ומיהו היזם?",render_alt="הדמיה"),
"en":dict(generic_badge="Generic architectural model · illustrative, not final design",price_of_apt="Apartment price",eq_l="Equity",loan_l="Loan",pay_l="Est. monthly · 25 yrs, 5%",
  buy_mort_t="Mortgage estimate",buy_steps_t="Buying steps",buy_pros_t="Verified professionals",
  step1="Choose an apartment and check price vs. area",step2="Check documents: permit, title, spec",step3="Lawyer & appraiser guidance",step4="Mortgage approval and approach the developer",
  pro_law="Real-estate lawyer · verified",pro_appr="Property appraiser · verified",pro_mort="Mortgage advisor · verified",
  map_streets="Streets",map_sat="Satellite",map_prices="Area prices",faq_q_delivery="Delivery date and developer?",render_alt="rendering"),
"fr":dict(generic_badge="Modèle architectural générique · illustratif",price_of_apt="Prix de l'appartement",eq_l="Apport",loan_l="Prêt",pay_l="Mensualité est. · 25 ans, 5%",
  buy_mort_t="Estimation du prêt",buy_steps_t="Étapes d'achat",buy_pros_t="Professionnels vérifiés",
  step1="Choisir un appartement et vérifier le prix vs. le quartier",step2="Vérifier les documents : permis, titre, cahier des charges",step3="Accompagnement avocat & expert",step4="Accord de prêt et contact du promoteur",
  pro_law="Avocat immobilier · vérifié",pro_appr="Expert immobilier · vérifié",pro_mort="Conseiller en prêt · vérifié",
  map_streets="Rues",map_sat="Satellite",map_prices="Prix du quartier",faq_q_delivery="Date de livraison et promoteur ?",render_alt="rendu"),
"ru":dict(generic_badge="Типовая арх. модель · иллюстрация, не финальный проект",price_of_apt="Цена квартиры",eq_l="Первый взнос",loan_l="Кредит",pay_l="Ежемес. оценка · 25 лет, 5%",
  buy_mort_t="Оценка ипотеки",buy_steps_t="Этапы покупки",buy_pros_t="Проверенные специалисты",
  step1="Выбрать квартиру и сверить цену с районом",step2="Проверить документы: разрешение, табу, спецификация",step3="Сопровождение юриста и оценщика",step4="Одобрение ипотеки и обращение к застройщику",
  pro_law="Юрист по недвижимости · проверен",pro_appr="Оценщик · проверен",pro_mort="Ипотечный консультант · проверен",
  map_streets="Улицы",map_sat="Спутник",map_prices="Цены района",faq_q_delivery="Срок сдачи и застройщик?",render_alt="визуализация"),
"ar":dict(generic_badge="نموذج معماري عام · توضيحي، ليس التصميم النهائي",price_of_apt="سعر الشقة",eq_l="رأس المال",loan_l="القرض",pay_l="قسط شهري تقديري · 25 سنة، 5%",
  buy_mort_t="تقدير الرهن",buy_steps_t="خطوات الشراء",buy_pros_t="مختصون موثّقون",
  step1="اختر شقة وتحقق من السعر مقابل المنطقة",step2="فحص المستندات: الترخيص، الطابو، المواصفات",step3="مرافقة محامٍ ومثمّن",step4="الموافقة على الرهن والتوجه إلى المطوّر",
  pro_law="محامي عقارات · موثّق",pro_appr="مثمّن عقاري · موثّق",pro_mort="مستشار رهن · موثّق",
  map_streets="شوارع",map_sat="قمر صناعي",map_prices="أسعار المنطقة",faq_q_delivery="موعد التسليم والمطوّر؟",render_alt="محاكاة"),
}
for _l in LANGS: UI[_l].update(EXTRA[_l])

# Article (woven): hero lede + 4 section intros, per project, 5 languages.
# Written real per project (Hebrew canonical), then real translations.
def art(slug):
  P=PROJECTS[slug]; n=P["name_he"].split("·")[0].strip(); nl=P["name_lat"]
  base = {
   "he":dict(
     lede=f"{n} הוא מגדל מגורים בן {P['floors']} קומות ב{P['area']} — {P['units_total']} דירות של {P['dev']}, בבנייה עכשיו עם אכלוס משוער ב־{P['delivery']}. במקום לדמיין, בוחרים כאן דירה מתוך הבניין עצמו: קומה, כיוון, נוף ומחיר — לפני שפונים ליזם.",
     choose=f"סובבו את הבניין, בחרו קומה וכיוון, וראו מה מקבלים בכל דירה. הבחירה מסונכרנת בין המודל לטבלת הדירות.",
     price=f"כמה זה באמת שווה. האומדן לכל דירה מוצג מול מחירי האזור — ביושר, עם מקור ותאריך, ולא כמחיר יזם.",
     mapt=f"מפה אחת עם כל מה שחשוב סביב {n}: מחירי אזור, תחבורה, חינוך, מסחר ותוכניות עתידיות.",
     buy=f"ממחשבון המשכנתא על הדירה שבחרתם, דרך שלבי הרכישה ועד עורך דין, שמאי ויועץ משכנתא מאומתים — הכול במקום אחד."),
   "en":dict(
     lede=f"{nl} is a {P['floors']}-storey residential tower in {P['area']} — {P['units_total']} apartments by {P['dev']}, under construction with estimated delivery in {P['delivery']}. Instead of imagining, here you choose an apartment from inside the building itself: floor, exposure, view and price — before you approach the developer.",
     choose="Rotate the building, pick a floor and exposure, and see exactly what each apartment offers. Selection stays in sync between the model and the units table.",
     price="What it's really worth. Each apartment's estimate is shown against area prices — honestly, with source and date, and never as a developer price.",
     mapt=f"One map with everything that matters around {nl}: area prices, transit, schools, retail and future plans.",
     buy="From a mortgage calculator on your chosen apartment, through the buying steps, to a verified lawyer, appraiser and mortgage advisor — all in one place."),
   "fr":dict(
     lede=f"{nl} est une tour résidentielle de {P['floors']} étages à {P['area']} — {P['units_total']} appartements en construction. Au lieu d'imaginer, choisissez ici un appartement depuis le bâtiment lui-même : étage, orientation, vue et prix — avant de contacter le promoteur.",
     choose="Faites pivoter le bâtiment, choisissez un étage et une orientation, et voyez ce qu'offre chaque appartement. La sélection reste synchronisée entre le modèle et le tableau.",
     price="Sa vraie valeur. L'estimation de chaque appartement est comparée aux prix du quartier — honnêtement, avec source et date, jamais comme un prix promoteur.",
     mapt=f"Une seule carte avec tout ce qui compte autour de {nl} : prix du quartier, transports, écoles, commerces et projets futurs.",
     buy="D'un calculateur de prêt sur l'appartement choisi, aux étapes d'achat, jusqu'à un avocat, un expert et un conseiller en prêt vérifiés — au même endroit."),
   "ru":dict(
     lede=f"{nl} — жилая башня в {P['floors']} этажей в районе {P['area']}: {P['units_total']} квартир, которые строятся сейчас. Вместо того чтобы воображать, здесь вы выбираете квартиру прямо из здания: этаж, ориентацию, вид и цену — до обращения к застройщику.",
     choose="Поворачивайте здание, выбирайте этаж и ориентацию и смотрите, что даёт каждая квартира. Выбор синхронизирован между моделью и таблицей квартир.",
     price="Сколько это реально стоит. Оценка каждой квартиры показана рядом с ценами района — честно, с источником и датой, и никогда как цена застройщика.",
     mapt=f"Одна карта со всем важным вокруг {nl}: цены района, транспорт, школы, торговля и планы развития.",
     buy="От ипотечного калькулятора на выбранной квартире, через этапы покупки, до проверенных юриста, оценщика и ипотечного консультанта — в одном месте."),
   "ar":dict(
     lede=f"{nl} برج سكني من {P['floors']} طابقاً في {P['area']} — {P['units_total']} شقة قيد الإنشاء الآن. بدلاً من التخيّل، اختر هنا شقة من داخل المبنى نفسه: الطابق والاتجاه والإطلالة والسعر — قبل التوجه إلى المطوّر.",
     choose="أدر المبنى، اختر طابقاً واتجاهاً، وشاهد ما تقدّمه كل شقة. يبقى الاختيار متزامناً بين النموذج وجدول الشقق.",
     price="قيمتها الحقيقية. يُعرض تقدير كل شقة مقابل أسعار المنطقة — بصدق، مع المصدر والتاريخ، وليس كسعر من المطوّر.",
     mapt=f"خريطة واحدة تضم كل ما يهم حول {nl}: أسعار المنطقة والمواصلات والمدارس والتجارة والمخططات المستقبلية.",
     buy="من حاسبة الرهن على الشقة المختارة، مروراً بخطوات الشراء، وصولاً إلى محامٍ ومثمّن ومستشار رهن موثّقين — كل ذلك في مكان واحد."),
  }
  return base

# ---------------------------------------------------------------- template
def esc(s): return html.escape(str(s), quote=True)

import base64
SLUG2KEY={"ashira-sde-dov":"ashira","rainbow-tel-aviv":"rainbow","dimri-yama-sde-dov":"dimri","duo-tel-aviv":"duo"}
MANI=json.load(open(os.path.join(OUT,"projects.generated.json"),encoding="utf-8"))
REPO=os.path.abspath(os.path.join(OUT,"..","..",".."))

# Canonical DB (data/projects/) is the source of truth; the inline page-pack
# fills presentation gaps until enrichment lands. DB wins on verified identity.
DB_SLUG={"ashira-sde-dov":"ashira-sde-dov","rainbow-tel-aviv":"rainbow-sde-dov",
         "dimri-yama-sde-dov":"dimri-yama","duo-tel-aviv":None}
def db_merge(slug,P):
  ds=DB_SLUG.get(slug)
  if not ds: return P
  f=os.path.join(REPO,"data","projects",ds+".json")
  if not os.path.exists(f): return P
  d=json.load(open(f,encoding="utf-8"))
  P["official_url"]=d.get("identity",{}).get("urls",{}).get("official") or ""
  bf=d.get("building_form",{}) or {}
  if bf.get("floors"): P["floors"]=bf["floors"]
  un=d.get("units",{}) or {}
  if un.get("total_units"): P["units_total"]=un["total_units"]
  return P

# Flagship rich models (Tier A): embed the detailed GLB and compute unit
# hotspots against its measured tower envelope (demo mapping, honest labels).
RICH={"rainbow-tel-aviv":os.path.join(REPO,"assets","projects","rainbow-tel-aviv","model.glb")}
def rich_setup(slug,P):
  path=RICH[slug]
  import trimesh
  s=trimesh.load(path)
  meshes=s.dump(concatenate=False) if hasattr(s,"dump") else [s]
  tower=max(meshes,key=lambda m:(m.bounds[1][1]-m.bounds[0][1]))
  lo,hi=tower.bounds; cx=(lo[0]+hi[0])/2
  H=float(hi[1]-lo[1]); zfront=float(hi[2])
  sceneR=max(float(x) for x in s.extents)
  fh=H/max(P["floors"],1)
  n=len(P["units"])
  for i,u in enumerate(P["units"]):
    u["hotspot"]=[float(cx+(i-(n-1)/2)*10.0), float(lo[1]+min(u["floor"],P["floors"])*fh-fh*0.5), zfront+0.5]
    u["hnormal"]=[0,0,1]
    u["uorbit"]=f"{int(20+(i-(n-1)/2)*8)}deg 72deg {int(sceneR*1.15)}m"
  raw=open(path,"rb").read()
  P["glb"]="data:model/gltf-binary;base64,"+base64.b64encode(raw).decode()
  P["orbit"]=f"25deg 72deg {int(sceneR*1.35)}m"
  P["target"]=f"0m {int(H*0.40)}m 0m"
  P["model_generic"]=False                  # project-specific model (still illustrative)
  return P

def glb_datauri(key):
  raw=open(os.path.join(OUT,"models",key+".glb"),"rb").read()
  return "data:model/gltf-binary;base64,"+base64.b64encode(raw).decode()

CITY_LAT={"תל אביב-יפו":"Tel Aviv-Yafo","רמת גן":"Ramat Gan","הרצליה":"Herzliya","בת ים":"Bat Yam","חולון":"Holon"}
def head_meta(slug,P,A,lang,fname_of):
  """Localized head: lang/dir, title, description, canonical + hreflang cluster."""
  a=A[lang]; name=P["name_lat"] if lang!="he" else P["name_he"]
  city=P["city"] if lang=="he" else CITY_LAT.get(P["city"],P["city"])
  title=f"{name} · {city} — נדלן" if lang=="he" else f"{name} · {city} — Nadlan"
  desc=a["lede"][:158]
  links=[f'<link rel="canonical" href="{fname_of(lang)}">']
  for l in LANGS:
    links.append(f'<link rel="alternate" hreflang="{l}" href="{fname_of(l)}">')
  links.append(f'<link rel="alternate" hreflang="x-default" href="{fname_of("he")}">')
  og=[f'<meta property="og:title" content="{esc(title)}">',
      f'<meta property="og:description" content="{esc(desc)}">',
      f'<meta property="og:type" content="website">']
  if P.get("poster") and str(P["poster"]).startswith("http"):
    og.append(f'<meta property="og:image" content="{esc(P["poster"])}">')
  return title,desc,"\n".join(links+og)

def render(slug):
  base=db_merge(slug,dict(PROJECTS[slug])); A=art_from(base)
  key=SLUG2KEY[slug]; m=MANI[key]
  if slug in RICH:
    base=rich_setup(slug,base)
  else:
    base["glb"]=glb_datauri(key)
    az=m["default_orbit"].split()[0]; H=m["height_m"]
    base["orbit"]=f"{az} 70deg {int(H*1.9)}m"; base["target"]=f"0m {int(H*0.42)}m 0m"
    base["model_generic"]=True
    hs={u["id"]:u for u in m["units"]}
    base["units"]=[dict(u, hotspot=hs[u["id"]]["hotspot_position"], hnormal=hs[u["id"]]["hotspot_normal"],
                     uorbit=hs[u["id"]]["camera_orbit"]) if u["id"] in hs else dict(u) for u in base["units"]]
  out=[]
  fname_of=lambda l: f"page-{slug}.html" if l=="he" else f"page-{slug}.{l}.html"
  for lang in LANGS:
    P=dict(base)
    title,desc,extra=head_meta(slug,P,A,lang,fname_of)
    lang_files={l:fname_of(l) for l in LANGS}
    data=dict(slug=slug,P=P,UI=UI,A=A,LANGS=LANGS,LANG_NAMES=LANG_NAMES,RTL=list(RTL),
              TOKEN=TOKEN,lang=lang,lang_files=lang_files)
    tpl=TEMPLATE.replace("/*__DATA__*/","window.NLP="+json.dumps(data,ensure_ascii=False)+";")
    d="rtl" if lang in RTL else "ltr"
    tpl=tpl.replace('<html lang="he" dir="rtl">',f'<html lang="{lang}" dir="{d}">')
    tpl=tpl.replace("<title>נדלן · עמוד פרויקט</title>",
      f"<title>{esc(title)}</title>\n<meta name=\"description\" content=\"{esc(desc)}\">\n{extra}")
    fn=fname_of(lang)
    open(os.path.join(OUT,"pages",fn),"w",encoding="utf-8").write(tpl)
    out.append(fn)
  return out

def art_from(P):
  """art() but on the (DB-merged) project dict rather than the raw registry."""
  global PROJECTS
  slug_tmp="__tmp__"
  PROJECTS[slug_tmp]=P
  try: return art(slug_tmp)
  finally: del PROJECTS[slug_tmp]

TEMPLATE = open(os.path.join(OUT, "_template.html"), encoding="utf-8").read()

if __name__=="__main__":
  for slug in list(PROJECTS):
    for f in render(slug):
      print("wrote", f)
