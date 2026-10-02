# -*- coding: utf-8 -*-
"""V7: build packet-<lang>.json and prompt-<lang>.md for the five Kikar Hamedina articles (C1: evidence -> brief -> ChatGPT).

    python docs/research/2026-10-kikar-v7/build_packets.py

The packet is the ONLY material ChatGPT gets (it is not asked to research; the owner, 1.10.2026). It holds the claims with their
claim_id, the SERP intents per language, the outline with word budgets and the claims each section must use, the HTML contract,
the internal links (each checked 200 on 3.10.2026) and the language rules. Sources stay in claims.py, never in the article.
"""
import io, json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from claims import CLAIMS  # noqa: E402

LINKS = json.load(io.open(os.path.join(HERE, "links.json"), encoding="utf-8"))
BY_ID = {c["claim_id"]: c for c in CLAIMS}

# the sections, in page order: id, word budget, the claims each must use, the part of the ChatGPT run it belongs to
SECTIONS = [
    ("lead", 85, ["P01", "P02", "P04", "P10", "P07", "P12", "P25", "K01", "R02"], 1),
    ("nlws-facts", 300, ["P01", "P02", "P03", "P04", "P05", "P07", "P10", "P12", "P15", "P16", "P17", "P18", "F01", "F02", "K01",
                         "P25", "D01"], 1),
    ("nlws-choose", 550, ["P06", "P07", "P08", "P09", "T13", "U07", "U06", "P19", "R03"], 1),
    ("nlws-homes", 550, ["U01", "U02", "U03", "U04", "U05", "U06", "U08", "P10", "P20", "P09", "R05"], 1),
    ("nlws-life", 450, ["F01", "F02", "F03", "F04", "P19", "P21", "P20", "K06", "U08", "K04"], 1),
    ("nlws-prices", 650, ["R01", "R02", "R03", "R04", "R05", "R06"], 2),
    ("nlws-costs", 600, ["B01", "B02", "B03", "B04", "B05", "B06", "B07"], 2),
    ("nlws-buy", 400, ["P14", "B07", "R05", "U01", "D01", "U05"], 2),
    ("nlws-sale", 350, ["P12", "P13", "P14", "R07"], 2),
    ("nlws-when", 330, ["P25", "P22", "P23", "P24", "D01", "D02"], 2),
    ("nlws-timeline", 200, ["P26", "P25", "Q02", "P11"], 2),
    ("nlws-park", 480, ["K01", "K02", "K03", "K04", "K05", "K06", "K07", "K08", "D02", "T10"], 3),
    ("nlws-square", 450, ["Q01", "Q02", "Q03", "Q04", "Q05", "Q06", "Q07"], 3),
    ("nlws-transport", 420, ["T01", "T02", "T03", "T04", "T05", "T06", "T07", "T08", "T09", "T11", "T12", "T14"], 3),
    ("nlws-faq", 800, [], 3),
]
TOTAL = sum(s[1] for s in SECTIONS)

L = {}

# ------------------------------------------------------------------ Hebrew
L["he"] = {
    "url": "https://nad-lan.co.il/projects/hamedina/", "h1": "מגדלי כיכר המדינה, תל אביב", "faq_h2": "שאלות נפוצות",
    "audience": "משפחה ישראלית שמשדרגת לבית ליד פארק בצפון תל אביב; זוג שמחפש יוקרה שקטה; משקיע; ישראלי שגר בחו\"ל ומחפש בית "
                "בעיר. הוא רוצה להתאהב, וגם לדעת שכל מספר אמיתי ומה כל החלטה עולה לו.",
    "names": "השם הראשי: מגדלי כיכר המדינה. בפעם הראשונה: \"מגדלי כיכר המדינה (Kikar Hamedina Towers)\". לשלב בטבעיות: \"פרויקט "
             "כיכר המדינה\", \"המגדלים בכיכר המדינה\", \"כיכר המדינה תל אביב\", \"רחוב ה׳ באייר\". פעם אחת: \"מגדלי הספירלה\". "
             "המגדלים: מגדל A, מגדל B, מגדל C. הבונים: אלקטרה בנייה ואשטרום. האדריכלים: יסקי מור סיון אדריכלים. הבעלים: בעלי "
             "הקרקע / חברת בעלי הקרקע. המילה \"יזם\" (בכל הטיה) אסורה: אין יזם בפרויקט הזה.",
    "keywords": [("כיכר המדינה תל אביב", 390), ("מגדלי כיכר המדינה", 260), ("פרויקט כיכר המדינה", 170), ("כיכר המדינה מגדלים", 110),
                 ("כיכר המדינה מפה", 90), ("דירות להשכרה כיכר המדינה", 90), ("מגדלי כיכר המדינה למכירה", 70),
                 ("פרויקט כיכר המדינה מחירים", 50), ("מס רכישה", "ראש ביקוש באתר"), ("מחשבון משכנתא", "ראש ביקוש באתר"),
                 ("מגדלי יוקרה", "87 הופעות בחודשים האחרונים")],
    "related": "מגדלי כיכר המדינה למכירה · להשכרה · אדריכל · חנויות כיכר המדינה · תמונות · הדמיה · מפה · אשטרום כיכר המדינה · "
               "אלקטרה כיכר המדינה · פארק כיכר המדינה",
    "headings": {
        "nlws-facts": ("הפרויקט במספרים", "מגדלי כיכר המדינה: כל העובדות"),
        "nlws-choose": ("מגדל, קומה וכיוון", "איזה מגדל, איזו קומה ואיזה כיוון לבחור במגדלי כיכר המדינה?"),
        "nlws-homes": ("הדירות", "הדירות במגדלי כיכר המדינה: גדלים, מרפסות ומפרט"),
        "nlws-life": ("החיים בבניין", "בריכה, ספא, חדר כושר וחניה: החיים במגדלי כיכר המדינה"),
        "nlws-prices": ("מחירים ועסקאות · מידע גלוי", "מחירי הדירות במגדלי כיכר המדינה"),
        "nlws-costs": ("עלויות הרכישה", "כמה עולה לקנות דירה במגדלי כיכר המדינה: מס רכישה ומשכנתא"),
        "nlws-buy": ("שלב אחר שלב", "איך קונים דירה במגדלי כיכר המדינה"),
        "nlws-sale": ("למכירה ולהשכרה", "מגדלי כיכר המדינה למכירה ולהשכרה"),
        "nlws-when": ("אכלוס", "מתי מגדלי כיכר המדינה יאוכלסו?"),
        "nlws-timeline": ("ציר הזמן", "מהמגרשים של 1942 ועד השלד של 2026"),
        "nlws-park": ("פארק כיכר המדינה", "פארק כיכר המדינה: כ-40 דונם, אגם אקולוגי ובית ספר חדש"),
        "nlws-square": ("הכיכר", "כיכר המדינה תל אביב: חנויות, בתי קפה וחיים סביב הכיכר"),
        "nlws-transport": ("הסביבה", "כיכר המדינה על המפה: רכבת קלה, בתי ספר ושירותים במרחק הליכה"),
        "nlws-faq": ("שאלות ותשובות", "שאלות נפוצות"),
    },
    "faq": ["מה הגובה של מגדלי כיכר המדינה?", "מה מחירי הדירות במגדלי כיכר המדינה?", "מי בנה את המגדלים בכיכר המדינה?",
            "מהי כיכר המדינה בתל אביב?", "מהו פרויקט כיכר המדינה?", "האם יש בית קפה בכיכר המדינה?",
            "איפה אפשר למצוא מסעדות כשרות בכיכר המדינה?", "מתי צפוי האכלוס במגדלי כיכר המדינה?",
            "כמה דירות וכמה חניות יש במגדלי כיכר המדינה?", "כמה מס רכישה משלמים על דירה במגדלי כיכר המדינה?",
            "איזו קומה וכיוון לבחור במגדלי כיכר המדינה?", "איזו רכבת קלה עוברת ליד כיכר המדינה?",
            "יש דירות להשכרה במגדלי כיכר המדינה?"],
    "wa": "לקבלת פרטים נוספים בוואטסאפ",
    "units": "מ״ר, ₪, \"מיליון ₪\", דונם, ק\"מ, דקות הליכה; מעלות במילה (\"1.25 מעלות\"), לא בסימן °.",
    "typography": "גרשיים וגרש עבריים בשמות (מ״ר, ה׳ באייר) בתוך HTML; תאריכים 23.4.2026 או 4.2026; טווח \"9.58 עד 10.63 מיליון ₪\"; "
                  "בלי מקף ארוך (—) ובלי מקף בינוני (–), גם לא בטווחים.",
    "culture": "כתיבה לקורא הישראלי: מושגים מקומיים בלי הסבר (טופס 4, ממ\"ד, מס רכישה, דירה יחידה, יד שנייה, הסכם מכר, מתווך, "
               "עורך דין מקרקעין). טון של עמוד פרויקט יוקרה ישראלי: פתיח נושם (מיקום לפני שם), גוף שלישי על הפרויקט, גוף שני רבים "
               "בפניות לקורא (\"בחרו\", \"השוו\", \"דמיינו\"), מתקנים כרשימת שמות עצם עם פאנץ' בסוף, מספר + שם עצם.",
    "banned": "ממשק · דמו · הדגמה · מודל (במובן תלת ממד) · מנגנון · נקודות חמות · שכבה · אריח · מפה חיה · מפה לחיצה · אינטראקטיבי · "
              "רספונסיבי · מובייל · סקיצה · סכמטי · פיילוט · פרוטוטייפ · \"המערכת\" · \"הפלטפורמה\" · \"החוויה הדיגיטלית\" · "
              "טכנולוגיה · סימולציה · מנוע · אטלס · \"אפס X\" · בקרוב · בבדיקה · תלת ממד (בגוף הכתבה) · יזם/יזמים/יזמית · "
              "\"ייעוץ חינם\" (רק בפס הצף של האתר, לא בכתבה) · \"לא היזם\" / \"אינו מתווך\" וכל הבהרה עצמית · חשוב להבין · "
              "חשוב לזכור · ראוי לציין · במילים אחרות · בעידן · עולם הנדל\"ן · ללא ספק · בסופו של דבר · לסיכום · מהווה · "
              "יש לציין כי · \"במאמר זה\" · \"להלן\" · יחסית · כמעט · אמור להיות · דגל אדום · מלכודת · היזהרו",
}

# ------------------------------------------------------------------ English
L["en"] = {
    "url": "https://nad-lan.co.il/projects/hamedina-en/", "h1": "Kikar Hamedina Towers, Tel Aviv", "faq_h2": "Frequently asked questions",
    "audience": "International buyers (US, UK, Canada, Australia, South Africa) and English-speaking Israelis and olim. Many buy from "
                "abroad, compare in shekels and need the Israeli terms decoded once: rooms, Form 4, purchase tax, mamad.",
    "names": "Main name: Kikar Hamedina Towers. First mention: \"Kikar Hamedina Towers (מגדלי כיכר המדינה)\". Use naturally: "
             "\"Kikar Hamedina, Tel Aviv\", \"the Kikar Hamedina project\", \"HaMedina Square\" (once, with its meaning \"State "
             "Square\"), \"He Be’Iyar Street\". Once: \"the Spiral Towers\". Towers A, B and C. Builders: Electra Construction and "
             "Ashtrom. Architects: Yaski Mor Sivan Architects. Owners: the landowners / the landowners' company. Never \"developer\".",
    "keywords": [("kikar hamedina towers", 320), ("kikar hamedina", 260), ("kikar hamedina tel aviv", 140),
                 ("tel aviv luxury apartments for sale", "intent"), ("buy property in tel aviv", "intent"),
                 ("can foreigners buy property in israel", "intent"), ("israel purchase tax foreign resident", "intent"),
                 ("mortgage in israel for foreigners", "intent"), ("tel aviv real estate prices per square meter", "intent")],
    "related": "Kikar Hamedina towers price · for sale · architect · Ashtrom · Electra · park · map · shops · light rail",
    "headings": {
        "nlws-facts": ("The project in numbers", "Kikar Hamedina Towers: the key facts"),
        "nlws-choose": ("Tower, floor and direction", "Which tower, floor and direction to choose at Kikar Hamedina Towers"),
        "nlws-homes": ("The apartments", "The apartments: sizes, balconies and specification"),
        "nlws-life": ("Life in the building", "Pool, spa, gym and parking: daily life in Kikar Hamedina Towers"),
        "nlws-prices": ("Prices and deals · public information", "Apartment prices in Kikar Hamedina Towers"),
        "nlws-costs": ("The cost of buying", "What it costs to buy: Israeli purchase tax and mortgages"),
        "nlws-buy": ("Step by step", "How to buy an apartment in Kikar Hamedina Towers, from Israel or from abroad"),
        "nlws-sale": ("For sale and for rent", "Kikar Hamedina Towers apartments for sale and for rent"),
        "nlws-when": ("Occupancy", "When will Kikar Hamedina Towers be ready?"),
        "nlws-timeline": ("Timeline", "From the plots of 1942 to the frame of 2026"),
        "nlws-park": ("The park", "Kikar Hamedina Park: about 40 dunam, an ecological pond and a new school"),
        "nlws-square": ("The square", "Kikar Hamedina, Tel Aviv: luxury shops, cafés and life around the square"),
        "nlws-transport": ("The area", "Kikar Hamedina on the map: light rail, schools and services within walking distance"),
        "nlws-faq": ("Questions and answers", "Frequently asked questions"),
    },
    "faq": ["How tall are Kikar Hamedina Towers?", "What do apartments in Kikar Hamedina Towers cost?",
            "What is the price per square meter in Kikar Hamedina Towers?", "Who is building the towers in Kikar Hamedina?",
            "What is Kikar Hamedina in Tel Aviv?", "When will Kikar Hamedina Towers be ready for occupancy?",
            "How many apartments and parking spaces are there?", "Can foreigners buy an apartment in Kikar Hamedina Towers?",
            "How much purchase tax does a foreign buyer pay?", "Can a non-resident get an Israeli mortgage?",
            "Do the apartments have a sea view?", "What does \"4 rooms\" mean in Israel?",
            "Which light rail lines serve Kikar Hamedina?"],
    "wa": "More details on WhatsApp",
    "units": "m² first, with square feet once for the average apartment (150 m², about 1,615 sq ft); ₪ with \"million\" "
             "(₪9.58 million); dunam explained once (1 dunam = 1,000 m²; 40 dunam = about 10 acres); minutes on foot.",
    "typography": "US spelling is fine but keep \"metre\" out: use m and m²; dates as 23 April 2026 or April 2026; ranges with \"to\"; "
                  "no long dash (—) and no en dash (–).",
    "culture": "Explain the Israeli room count once (4 rooms = a living room and 3 bedrooms). Explain Form 4 (the occupancy permit) "
               "once. Purchase tax: give the foreign-resident rule clearly. Show that everything can be done from abroad (a lawyer with "
               "a power of attorney), and that buying does not give residency. Warm, confident, factual: the voice of a luxury "
               "project page, not of a warning leaflet.",
    "banned": "interface · demo · model (as 3D) · hotspot · overlay · engine · layer · tile · prototype · simulation · technology · "
              "\"the system\" · \"the platform\" · digital experience · 3D (in the article body) · coming soon · developer · "
              "\"free advice\" (only the site's floating bar says it) · \"we are not the developer\" / \"not a broker\" and every "
              "self-disclaimer · it is important to note · in today's world · needless to say · in conclusion · delve · "
              "nestled · boasts · a testament to · red flag · beware",
}

# ------------------------------------------------------------------ French
L["fr"] = {
    "url": "https://nad-lan.co.il/projects/hamedina-fr/", "h1": "Tours Kikar Hamedina, Tel Aviv", "faq_h2": "Questions fréquentes",
    "audience": "Acheteurs français et belges, souvent en préparation d'alyah ou à la recherche d'un pied-à-terre ; olim francophones "
                "déjà en Israël qui montent en gamme. Ils achètent à distance et comparent en shekels.",
    "names": "Nom principal : les tours Kikar Hamedina. Première mention : « les tours Kikar Hamedina (Kikar Hamedina Towers, "
             "מגדלי כיכר המדינה) ». À placer naturellement : « Kikar Hamedina à Tel Aviv », « la place Kikar Hamedina » (une fois : "
             "« la place de l’État »), « rue He Be’Iyar ». Une fois : « les tours en spirale ». Tours A, B et C. Constructeurs : "
             "Electra Construction et Ashtrom. Architectes : Yaski Mor Sivan Architectes. Propriétaires : les propriétaires fonciers "
             "/ la société des propriétaires fonciers. Jamais « promoteur ».",
    "keywords": [("immobilier israel", 320), ("appartement tel aviv", 140), ("immobilier tel aviv", 140),
                 ("acheter appartement tel aviv", 110), ("appartement a vendre tel aviv", 110),
                 ("acheter un appartement en israel", 90), ("prix immobilier tel aviv", 50), ("prix m2 tel aviv", 50),
                 ("kikar hamedina", 40), ("kikar hamedina tel aviv", 30), ("appartement tel aviv vue mer", 20),
                 ("immobilier de luxe tel aviv", 10), ("kikar hamedina towers", 10)],
    "related": "« tours » seul se lit comme « visites » : toujours « tours Kikar Hamedina » avec « appartements » ou « prix » à côté. "
               "PAA : « Quel est le quartier le plus chic de Tel Aviv ? »",
    "headings": {
        "nlws-facts": ("Le projet en chiffres", "Tours Kikar Hamedina : toutes les données"),
        "nlws-choose": ("Tour, étage et orientation", "Quelle tour, quel étage et quelle orientation choisir ?"),
        "nlws-homes": ("Les appartements", "Les appartements : surfaces, balcons et prestations"),
        "nlws-life": ("La vie dans les tours", "Piscine, spa, salle de sport et parking : le quotidien aux tours Kikar Hamedina"),
        "nlws-prices": ("Prix et ventes · information publique", "Prix des appartements dans les tours Kikar Hamedina"),
        "nlws-costs": ("Les frais d’achat", "Combien coûte l’achat : taxe d’acquisition et prêt immobilier en Israël"),
        "nlws-buy": ("Étape par étape", "Acheter un appartement aux tours Kikar Hamedina depuis la France ou la Belgique"),
        "nlws-sale": ("À vendre et à louer", "Appartements à vendre et à louer dans les tours Kikar Hamedina"),
        "nlws-when": ("Livraison", "Quand les tours Kikar Hamedina seront-elles livrées ?"),
        "nlws-timeline": ("La chronologie", "Des parcelles de 1942 au gros œuvre de 2026"),
        "nlws-park": ("Le parc", "Le parc de Kikar Hamedina : 4 hectares, un étang écologique et une nouvelle école"),
        "nlws-square": ("La place", "Kikar Hamedina à Tel Aviv : boutiques de luxe, cafés et quartier chic"),
        "nlws-transport": ("Le quartier", "Kikar Hamedina sur la carte : tramway, écoles et services à pied"),
        "nlws-faq": ("Questions et réponses", "Questions fréquentes"),
    },
    "faq": ["Quelle est la hauteur des tours Kikar Hamedina ?", "Combien coûte un appartement dans les tours Kikar Hamedina ?",
            "Quel est le prix au m² dans les tours ?", "Qui construit les tours de Kikar Hamedina ?",
            "Qu’est-ce que Kikar Hamedina à Tel Aviv ?", "Quand les tours Kikar Hamedina seront-elles livrées ?",
            "Combien d’appartements et de places de parking ?", "Peut-on acheter depuis la France ou la Belgique ?",
            "Quels frais prévoir : la taxe d’acquisition (mas rechisha) ?", "Un non-résident peut-il obtenir un prêt immobilier en Israël ?",
            "Les appartements ont-ils vue sur la mer ?", "Quel est le quartier le plus chic de Tel Aviv ?",
            "Y a-t-il un café à Kikar Hamedina ?"],
    "wa": "Plus de détails sur WhatsApp",
    "units": "m², M₪ ou « millions de shekels » (9,58 M₪), hectares (40 dunams = environ 4 hectares ; 1 dunam = 1 000 m²), minutes à pied.",
    "typography": "Espace insécable avant : ; ? ! et entre milliers (75 900) ; virgule décimale (9,58) ; dates « 23 avril 2026 » ; "
                  "guillemets « » ; pas de tiret long (—) ni de tiret moyen (–).",
    "culture": "« 4 pièces » israélien = 4 pièces français (séjour + 3 chambres) : le dire une fois. Expliquer une fois le formulaire 4 "
               "(certificat d’habitation) et la taxe d’acquisition (mas rechisha). Les maisons françaises de l’anneau (Dior, Saint "
               "Laurent, Givenchy, Chloé) parlent à ce lecteur. Montrer qu’on peut tout préparer à distance (avocat avec procuration), "
               "et que l’achat ne donne pas la résidence. Pied-à-terre, alyah, vue mer, quartier chic : les mots du lecteur.",
    "banned": "interface · démo · modèle (au sens 3D) · moteur · calque · prototype · simulation · technologie · « le système » · "
              "« la plateforme » · expérience digitale · 3D (dans le corps du texte) · bientôt · promoteur · « conseil gratuit » "
              "(seule la barre flottante du site le dit) · « nous ne sommes pas le promoteur » / « pas une agence » et toute "
              "auto-précaution · il est important de noter · force est de constater · en conclusion · véritable écrin · niché",
}

# ------------------------------------------------------------------ Russian
L["ru"] = {
    "url": "https://nad-lan.co.il/projects/hamedina-ru/", "h1": "Башни Кикар ха-Медина, Тель-Авив", "faq_h2": "Частые вопросы",
    "audience": "Русскоязычные израильтяне, которые знают местные слова (салон, маклер, Форма 4, мас рехиша), и покупатели из-за "
                "границы, которые покупают на расстоянии. Им важны цена квадратного метра, налоги, ипотека и сроки.",
    "names": "Главное имя: башни Кикар ха-Медина. Первое упоминание: «башни Кикар ха-Медина (Kikar Hamedina Towers, מגדלי כיכר "
             "המדינה)». Варианты написания, которые ищут: Кикар Хамедина, Кикар Амедина (дать один раз, в FAQ о названии), перевод "
             "«Площадь Государства» (один раз). Улица: He Be’Iyar (латиницей, как в остальной странице). Один раз: «спиральные "
             "башни». Башни A, B и C. Строители: Electra Construction и Ashtrom. Архитекторы: Yaski Mor Sivan Architects. "
             "Владельцы: владельцы земли / компания владельцев земли. Никогда «застройщик» или «девелопер».",
    "keywords": [("купить квартиру в израиле", 140), ("квартиры в израиле", 140), ("недвижимость в израиле", 90),
                 ("купить квартиру в тель авиве", 50), ("недвижимость израиль", 40), ("квартира в тель авиве", 20),
                 ("кикар ха медина", 10), ("кикар хамедина", 10), ("кикар а медина", 10), ("цены на квартиры в тель авиве", 10),
                 ("новостройки тель авива", 10)],
    "related": "налог на покупку квартиры в Израиле · ипотека для нерезидентов · сколько стоит квадратный метр · вид на море",
    "headings": {
        "nlws-facts": ("Проект в цифрах", "Башни Кикар ха-Медина: все данные"),
        "nlws-choose": ("Башня, этаж и сторона света", "Какую башню, этаж и сторону света выбрать?"),
        "nlws-homes": ("Квартиры", "Квартиры: площади, балконы и отделка"),
        "nlws-life": ("Жизнь в доме", "Бассейн, спа, тренажёрный зал и парковка: быт в башнях Кикар ха-Медина"),
        "nlws-prices": ("Цены и сделки · открытые данные", "Цены на квартиры в башнях Кикар ха-Медина"),
        "nlws-costs": ("Расходы на покупку", "Сколько стоит покупка: налог на покупку и ипотека в Израиле"),
        "nlws-buy": ("Шаг за шагом", "Как купить квартиру в башнях Кикар ха-Медина, в том числе из-за границы"),
        "nlws-sale": ("Продажа и аренда", "Квартиры на продажу и в аренду в башнях Кикар ха-Медина"),
        "nlws-when": ("Заселение", "Когда сдадут башни Кикар ха-Медина?"),
        "nlws-timeline": ("Хронология", "От участков 1942 года до каркаса 2026 года"),
        "nlws-park": ("Парк", "Парк Кикар ха-Медина: около 40 дунамов, экологический пруд и новая школа"),
        "nlws-square": ("Площадь", "Кикар ха-Медина в Тель-Авиве: бутики, кафе и жизнь вокруг площади"),
        "nlws-transport": ("Район", "Кикар ха-Медина на карте: легкорельсовый транспорт, школы и всё в шаговой доступности"),
        "nlws-faq": ("Вопросы и ответы", "Частые вопросы"),
    },
    "faq": ["Какой высоты башни Кикар ха-Медина?", "Сколько стоят квартиры в башнях Кикар ха-Медина?",
            "Сколько стоит квадратный метр в башнях?", "Кто строит башни на Кикар ха-Медина?",
            "Что такое Кикар ха-Медина в Тель-Авиве?", "Как правильно: Кикар ха-Медина или Кикар Хамедина?",
            "Когда планируется заселение башен Кикар ха-Медина?", "Сколько в башнях квартир и парковочных мест?",
            "Можно ли купить квартиру, находясь за границей?", "Какой налог на покупку квартиры (мас рехиша) придётся заплатить?",
            "Дают ли ипотеку нерезидентам?", "Есть ли из квартир вид на море?", "Что значит «4 комнаты» в Израиле?",
            "Какие линии легкорельсового транспорта проходят рядом?"],
    "wa": "Подробнее в WhatsApp",
    "units": "м², ₪ и «млн ₪» (9,58 млн ₪), дунам (1 дунам = 1 000 м²; 40 дунамов = около 4 га), минуты пешком.",
    "typography": "Десятичная запятая (9,58), неразрывный пробел в 75 900 и перед ₪, даты 23.04.2026, кавычки «ёлочки», градусы словом "
                  "(«1,25 градуса»); без длинного тире (—) и без среднего тире (–): предложения строятся без тире-связки.",
    "culture": "Объяснить один раз израильский счёт комнат («4 комнаты: салон и три спальни»). Форма 4 = разрешение на заселение. "
               "Отдельно: налог на покупку для нерезидента и для «единственной квартиры», ипотека до 50% для нерезидента, покупка "
               "через адвоката по доверенности, покупка не даёт статуса. Тон уверенный и тёплый, как у страницы элитного проекта, без "
               "канцелярита.",
    "banned": "интерфейс · демо · модель (в смысле 3D) · движок · слой · прототип · симуляция · технология · «система» · «платформа» · "
              "цифровой опыт · 3D (в тексте статьи) · скоро · застройщик · девелопер · «бесплатная консультация» (её говорит только "
              "плавающая полоса сайта) · «мы не застройщик» / «не маклер» и любые самооговорки · стоит отметить · важно понимать · "
              "в заключение · уникальный шанс",
}

# ------------------------------------------------------------------ Arabic
L["ar"] = {
    "url": "https://nad-lan.co.il/projects/hamedina-ar/", "h1": "Kikar Hamedina Towers, Tel Aviv (English, the owner's ruling)",
    "faq_h2": "أسئلة شائعة",
    "audience": "قرّاء عرب، معظمهم في إسرائيل وكثير منهم عائلات: المدرسة والروضة، مواقف السيارات، المواصلات، سعر المتر، والتمويل. "
                "يصلون عبر رابط أو مشاركة واتساب أو مفتاح اللغة في الموقع.",
    "names": "الاسم الرئيسي: أبراج كيكار همدينا. أول ذكر: «أبراج كيكار همدينا (Kikar Hamedina Towers، מגדלי כיכר המדינה)». "
             "مرة واحدة: «ساحة الدولة» (الترجمة). الشارع: He Be’Iyar بالحروف اللاتينية كما في بقية الصفحة. مرة واحدة: «الأبراج "
             "الحلزونية». الأبراج A وB وC. البناء: Electra Construction وAshtrom. المعماريون: Yaski Mor Sivan. المالكون: أصحاب "
             "الأرض / شركة أصحاب الأرض. لا تُستعمل كلمة «مطوّر» إطلاقاً. أماكن بلا اسم عربي في مصدرها تبقى باسمها الإنجليزي "
             "(Ichilov, Habima, Sportek): لا اسم مخترَع.",
    "keywords": [("شقق للبيع في اسرائيل", 10), ("كيكار همدينا", "no data"), ("ميدان الدولة تل أبيب", "no data"),
                 ("شقق للبيع في تل أبيب", "intent"), ("اسعار الشقق في تل أبيب", "intent"), ("أبراج تل أبيب", "intent")],
    "related": "لا توجد صفحة عقارية عربية عن الأبراج في أي لغة على Google: الحقل مفتوح.",
    "headings": {
        "nlws-facts": ("المشروع بالأرقام", "أبراج كيكار همدينا: كل المعطيات"),
        "nlws-choose": ("البرج والطابق والاتجاه", "أي برج وأي طابق وأي اتجاه تختارون في أبراج كيكار همدينا؟"),
        "nlws-homes": ("الشقق", "الشقق: المساحات والشرفات والمواصفات"),
        "nlws-life": ("الحياة في البرج", "بركة وسبا ونادٍ رياضي ومواقف: الحياة اليومية في أبراج كيكار همدينا"),
        "nlws-prices": ("الأسعار والصفقات · معلومات منشورة", "أسعار الشقق في أبراج كيكار همدينا"),
        "nlws-costs": ("تكاليف الشراء", "كم يكلّف الشراء: ضريبة الشراء والقرض السكني"),
        "nlws-buy": ("خطوة بخطوة", "كيف تشترون شقة في أبراج كيكار همدينا"),
        "nlws-sale": ("للبيع وللإيجار", "شقق للبيع وللإيجار في أبراج كيكار همدينا"),
        "nlws-when": ("السكن", "متى تُسلَّم أبراج كيكار همدينا للسكن؟"),
        "nlws-timeline": ("التسلسل الزمني", "من قسائم 1942 إلى هيكل 2026"),
        "nlws-park": ("الحديقة", "حديقة كيكار همدينا: نحو 40 دونماً وبركة بيئية ومدرسة جديدة"),
        "nlws-square": ("الساحة", "كيكار همدينا في تل أبيب: متاجر فاخرة ومقاهٍ وحياة حول الساحة"),
        "nlws-transport": ("المنطقة", "كيكار همدينا على الخريطة: القطار الخفيف والمدارس والخدمات سيراً على الأقدام"),
        "nlws-faq": ("أسئلة وأجوبة", "أسئلة شائعة"),
    },
    "faq": ["ما ارتفاع أبراج كيكار همدينا؟", "ما أسعار الشقق في أبراج كيكار همدينا؟", "كم سعر المتر المربع في الأبراج؟",
            "من يبني الأبراج في كيكار همدينا؟", "ما هو كيكار همدينا في تل أبيب؟", "متى يبدأ السكن في أبراج كيكار همدينا؟",
            "كم عدد الشقق ومواقف السيارات؟", "ما المدارس والروضات القريبة من الأبراج؟", "كم تبلغ ضريبة الشراء على شقة في الأبراج؟",
            "ما نسبة التمويل في القرض السكني؟", "هل تطل الشقق على البحر؟", "ماذا يعني دوران الطوابق لمن يسكن في الأبراج؟",
            "ما الذي يقع على مسافة قريبة سيراً من الأبراج؟"],
    "wa": "لمزيد من التفاصيل عبر واتساب",
    "units": "م²، ₪ و«مليون ₪» (9.58 مليون ₪)، دونم، دقائق سيراً. الدرجات بالكلمة («1.25 درجة»): علامة ° تقفز إلى الجهة الخطأ في "
             "النص من اليمين إلى اليسار.",
    "typography": "أرقام غربية كما تكتبها الصحافة العربية في إسرائيل (75,900؛ 9.58)؛ تواريخ 23.4.2026؛ أسماء الأشهر الشامية (نيسان، "
                  "أيلول، كانون الأول) عند ذكر الشهر بالكلمة؛ بلا شرطة طويلة (—) وبلا شرطة متوسطة (–).",
    "culture": "عربية فصحى معاصرة واضحة، قريبة من لغة الصحافة الاقتصادية. شرح عدد الغرف الإسرائيلي مرة واحدة («4 غرف: صالون وثلاث "
               "غرف نوم»). المدرسة الجديدة والروضات وموقف السيارات ومسار إنزال الأطفال للمدرسة تهمّ هذا القارئ. الدوران يُشرح بما "
               "يعنيه للإطلالة والشمس. نبرة دافئة وواثقة.",
    "banned": "واجهة برمجية · عرض تجريبي · نموذج (بمعنى ثلاثي الأبعاد) · محرّك · طبقة · نموذج أولي · محاكاة · تكنولوجيا · «النظام» · "
              "«المنصة» · تجربة رقمية · ثلاثي الأبعاد (في متن المقال) · قريباً · مطوّر/المطوّرون · «استشارة مجانية» (يقولها شريط "
              "الموقع العائم فقط) · «لسنا المطوّر» / «لسنا وسيطاً» وكل تحفّظ ذاتي · تجدر الإشارة · في الختام · لا شك",
}

HTML_CONTRACT = """\
- Output HTML only, as one line per block element is fine. Allowed tags: p, h2, h3, section, table, thead, tbody, tr, th, td, ul, ol,
  li, b, a, small. No <h1> (the page has its own), no <div> except the closing marker below, no inline styles, no <br>, no emoji,
  no images, no scripts, no comments.
- The article opens with ONE lead paragraph: <p>…</p> (70 to 95 words, the keywords first). It is lifted to the top of the page.
- Then one <section> per block, in this exact order and with these exact ids:
  <section class="nlws" id="nlws-facts">, nlws-choose, nlws-homes, nlws-life, nlws-prices, nlws-costs, nlws-buy, nlws-sale,
  nlws-when, nlws-timeline, nlws-park, nlws-square, nlws-transport, and last <section class="nlws nlws-faq" id="nlws-faq">.
- Each section opens with <p class="nlws-k">KICKER</p> then <h2>HEADING</h2>. H3s inside as needed.
- Tables: <table><thead><tr><th>…</th></tr></thead><tbody>…</tbody></table>. The facts table is a two-column table with <th> as
  the row label: <tr><th>label</th><td>value</td></tr> (no thead).
- Lists: <ul class="nlws-list"><li>…</li></ul>. Numbered steps: <ol><li>…</li></ol>.
- The timeline section: <ol class="nlws-time"><li><b>DATE</b>text</li>…</ol>; the last item (4.2026, the frame) is
  <li class="is-now">.
- A short side note: <p class="nlws-note">…</p> (at most 3 in the whole article).
- WhatsApp: exactly twice (in nlws-sale and nlws-buy): <p><a class="nlws-wa" href="#nlws-wa">WA_TEXT</a></p>.
- Internal links: <a href="FULL_URL">anchor words</a>, only from the list given, 10 to 14 in the whole article, each URL once,
  anchors in the article's language and different from each other.
- FAQ: <h2>FAQ_H2</h2> exactly, then for each question: <h3>question</h3><p>answer</p> (ONE paragraph, 40 to 75 words, the first
  sentence answers directly, no list inside, links allowed).
- The very last element after the FAQ section: <div class="nadlan-project-article"></div>
"""


def packet(lang):
    d = L[lang]
    used = []
    for _, _, ids, _ in SECTIONS:
        for i in ids:
            if i not in used:
                used.append(i)
    for c in CLAIMS:  # every claim is available; the sections say which ones they must use
        if c["claim_id"] not in used:
            used.append(c["claim_id"])
    outline = []
    for sid, words, ids, part in SECTIONS:
        k, h = d["headings"].get(sid, ("", ""))
        outline.append({"id": sid, "part": part, "words": words, "kicker": k, "h2": h, "must_use": ids})
    return {
        "project": "Kikar Hamedina Towers (מגדלי כיכר המדינה), Tel Aviv",
        "language": lang, "page_url": d["url"], "page_h1": d["h1"], "faq_h2": d["faq_h2"],
        "audience": d["audience"], "names": d["names"], "keywords_monthly": d["keywords"], "related_searches": d["related"],
        "outline": outline, "words_target": TOTAL, "words_minimum": 5600, "faq_questions": d["faq"],
        "whatsapp_text": d["wa"], "internal_links": LINKS[lang], "units": d["units"], "typography": d["typography"],
        "culture": d["culture"], "banned": d["banned"],
        "claims": [{k: BY_ID[i][k] for k in ("claim_id", "topic", "claim", "conflict", "write_as") if BY_ID[i][k]} for i in used],
        "not_published": ["units per tower and per floor; an official unit mix; official floor plans",
                          "ceiling and floor-to-floor heights", "which basement level holds the pool, spa and gym",
                          "a green-building rating for the residential towers", "an official occupancy date (Form 4)",
                          "a sales office or an official price list (there is none)", "the pond's final size",
                          "rents in the towers", "the management company and its monthly fee",
                          "exactly what each apartment sees (it depends on tower, floor and direction)"],
        "page_context": "The article sits under the page's own tools, which the reader has just used: a picker that chooses tower, "
                        "floor and apartment by direction and shows the view from its windows (an illustration), an example "
                        "apartment to walk through, the deals table, the area map with walking minutes, and a WhatsApp button. "
                        "Mention them in plain buyer words at most 3 times in the whole article (\"choose tower, floor and "
                        "apartment by direction on this page\", \"the deals table above\", \"the area map\"), never as technology.",
    }


PROMPT_HE = """\
אתה כותב תוכן נדל"ן בכיר בישראל, עם יד של קופירייטר של פרויקט יוקרה. תכתוב כתבה אחת בעברית על מגדלי כיכר המדינה בתל אביב,
לעמוד {url} . הכתבה היא מדריך החלטה מלא למי שבוחר דירה במגדלים: לא מילוי ולא חזרות. גוגל לא מדרג אורך, הוא מדרג מענה מלא
לכוונה, ולכן כל פסקה עונה על שאלה שקונה שואל באמת: כמה זה עולה, מה מקבלים, איזו קומה ואיזה כיוון, מה מסביב, מתי נכנסים, ואיך
קונים.

החומר היחיד שלך הוא חבילת הראיות (JSON) בסוף ההודעה. אל תחפש ברשת ואל תוסיף שום עובדה, מספר, תאריך, שם עסק או טענה שאינם
בחבילה. כל מספר בכתבה חייב להופיע בטענה (claim) בחבילה. מה שלא פורסם נכתב כ"לא פורסם", בקצרה ובלי דרמה (רשימת not_published).
כשיש סתירה בין מקורות (שדה conflict), כותבים את הנתון השמרני עם "כ-", כפי ששדה write_as אומר, ולא מציגים את הגרסה האחרת.

## חוקי הבעלים (מחייבים)
- אין שמות מקורות בגוף הכתבה: לא עיתונים, לא אתרים, לא ויקיפדיה, לא "לפי X". מחירים הם "מידע גלוי" שפורסם, עם התאריך.
- אין יזם בפרויקט הזה: זה פרויקט של בעלי הקרקע. המילה "יזם" לא מופיעה בשום הטיה.
- בלי הבהרות עצמיות ובלי ערימת הסתייגויות ("לא היזם", "אינו מתווך", "אינו ייעוץ"). הערה קטנה אחת על מחיר מבוקש מול עסקה מספיקה.
- מידע החלטה לפני גימיקים. מסגור חיובי וקונקרטי, הגון לגמרי. בלי פרק "סיכונים", בלי "דגלים אדומים".
- כפתור הוואטסאפ בתוך הכתבה כתוב בדיוק: "{wa}".

## הקורא
{audience}

## השמות
{names}

## מילות המפתח (חיפושים בחודש) והיכן הן יושבות
{keywords}
חיפושים קשורים שגוגל מציג: {related}
- המשפט הראשון של הפתיח: מגדלי כיכר המדינה + תל אביב + שלושה מגדלים + 453 דירות.
- הכותרות (H2) הן הכותרות שבמבנה. מותר לשפר ניסוח, חובה לשמור את מילות המפתח שבהן.
- לאורך הכתבה, בטבעיות: "למכירה" 3 פעמים לפחות, "מחיר/מחירים" 8 פעמים לפחות, "דירות יוקרה" פעמיים, "מגדלי יוקרה בתל אביב" פעם
  אחת, "פרויקטים חדשים בצפון תל אביב" פעם אחת.

## המבנה, אורך ותקציב מילים
סך הכול לפחות {minimum} מילים נטו (בלי ה-HTML), יעד כ-{target}. תקציב לכל פרק והטענות שהוא חייב להשתמש בהן נמצאים בשדה outline.
מה כל פרק עושה:
- lead: פסקה נושמת אחת, מיקום לפני שם, 70 עד 95 מילים, התשובה הקצרה לכל העמוד.
- nlws-facts: פסקת פתיחה קצרה וטבלת עובדות דו-טורית (כ-16 שורות).
- nlws-choose: מה משנה את הבחירה בין מגדל A, B ו-C, בין קומה נמוכה לגבוהה ובין כיוונים: מה נמצא בכל כיוון ובאיזה מרחק (טבלה),
  מה הסיבוב של 1.25 מעלות עושה למרפסות ולנוף, איך המחיר למ"ר עולה עם הגובה. השמש והצל: משפט אחד בלבד, כפרט משני.
- nlws-homes: הגדלים שפורסמו (טבלה), 4 ו-5 חדרים ופנטהאוזים, מרפסות, ממ"ד, מפרט כפי שמודעות מתארות אותו, חניה ומחסן, ורשימה
  "מה לבקש מהמוכר" (תוכנית הדירה, מגדל וקומה וכיוון, שטח ומרפסת, חניות ומחסן, נספח המפרט, מועד מסירה, והאם המחיר לזכות או לדירה גמורה).
- nlws-life: יום בחיים, מתקני המרתף, המעליות המהירות, שוטי האשפה, המיזוג, החניון, מסלול ההורדה לבית הספר.
- nlws-prices: טבלת שלוש העסקאות, הממוצע והטווח, המחיר למ"ר לפי גובה, טבלת מחירים מבוקשים, זכות מול דירה גמורה, והשוואה לסביבה.
- nlws-costs: מס רכישה (טבלת מדרגות: דירה יחידה מול דירה נוספת ותושב חוץ) עם הדוגמה של 10 מיליון ₪; אחוזי מימון (75/70/50) עם
  הדוגמה; עורך דין מקרקעין; דמי תיווך לפי הזמנה בכתב; עולים חדשים. קישורים למחשבונים.
- nlws-buy: רשימה ממוספרת של 7 עד 8 שלבים, מהבחירה בעמוד ועד החתימה והמסירה, כולל קנייה מחו"ל בייפוי כוח; כפתור הוואטסאפ.
- nlws-sale: שוק של בעלי זכויות, כ-250 בעלים, עד 200 עד 250 דירות צפויות להימכר, מה ידוע על השכרה; כפתור הוואטסאפ; קישור למתווכים.
- nlws-when: השלד הושלם, קצב הבנייה, טווח ההערכות 2026 עד 2028, טופס 4, העבודות הציבוריות עד סוף 2027.
- nlws-timeline: 9 עד 11 נקודות מתוארכות.
- nlws-park, nlws-square, nlws-transport: החיים מסביב, עם טבלת תחבורה ומרחקים ודקות הליכה.
- nlws-faq: השאלות בשדה faq_questions, בסדר הזה, שבע הראשונות מילה במילה.

## חוזה ה-HTML
{contract}
(WA_TEXT = "{wa}", FAQ_H2 = "{faq_h2}")

## הטון והשפה
{culture}
- {typography}
- יחידות: {units}
- מילים וביטויים אסורים: {banned}

## איך מחזירים את הכתבה (חשוב)
הכתבה ארוכה, ולכן היא נשלחת בשלושה חלקים, כל חלק בבלוק קוד אחד ```html בלי שום טקסט לפניו או אחריו:
- חלק 1 (עכשיו): lead, nlws-facts, nlws-choose, nlws-homes, nlws-life.
- חלק 2 (כשאכתוב "המשך"): nlws-prices, nlws-costs, nlws-buy, nlws-sale, nlws-when, nlws-timeline.
- חלק 3 (כשאכתוב "המשך"): nlws-park, nlws-square, nlws-transport, nlws-faq, וה-div המסיים.
אל תקצר: כל פרק לפחות בתקציב שלו. אל תחזור על אותו משפט או אותה עובדה בשני פרקים, חוץ מהפתיח ומטבלת העובדות.

## חבילת הראיות
```json
{packet}
```
"""

PROMPT_XX = """\
You are a senior {lang_name}-language real-estate writer who knows Tel Aviv and writes for {lang_name}-speaking buyers. Write ONE
article in native {lang_name} (written for this reader, NOT translated from Hebrew or English) about Kikar Hamedina Towers in Tel
Aviv, for the page {url} . The instructions are in English; the article must read as if written by a {lang_name}-speaking expert
living in Tel Aviv.

The article is a complete decision guide for someone choosing an apartment in the towers: no padding and no repetition. Google does
not rank length, it ranks complete answers to the searcher's intent, so every paragraph answers a question a buyer really asks: what
it costs, what you get, which floor and direction, what is around, when you move in, and how to buy (also from abroad).

Your ONLY material is the evidence packet (JSON) at the end. Do not research and do not add any fact, number, date, business name or
claim that is not in the packet. Every number in the article must appear in a claim of the packet. What is not published is written
as "not published", briefly and calmly (the not_published list). Where sources conflict (the conflict field), write the conservative
figure with "about", as write_as says, and do not show the other version.

## The owner's rules (binding)
- No source names in the article body: no newspapers, websites, Wikipedia, "according to X". Prices are published public
  information, with their date.
- The project has NO developer: it belongs to the landowners. Never use the word for "developer" in any form.
- No self-disclaimers and no pile of caveats ("we are not the developer", "not a broker", "not advice"). One small note on asking
  price versus deal is enough.
- Decision information before gimmicks. Positive and concrete framing, fully honest. No "risks" chapter, no "red flags".
- The WhatsApp button inside the article reads exactly: "{wa}".

## The reader
{audience}

## Names
{names}

## Keywords (monthly searches) and where they sit
{keywords}
Related / People Also Ask: {related}
- The lead's first sentence: the towers' name + Tel Aviv + three towers + 453 apartments.
- The H2s are the outline's headings. You may improve the wording but must keep their keywords.

## Structure, length and word budget
At least {minimum} net words in all (not counting HTML), target about {target}. Each section's budget and the claims it must use are in
the outline field. What each section does:
- lead: one breathing paragraph, place before name, 70 to 95 words: the short answer to the whole page.
- nlws-facts: a short opening paragraph and a two-column facts table (about 16 rows).
- nlws-choose: what changes between towers A, B and C, low and high floors, and directions: what lies in each direction and how far
  (a table), what the 1.25-degree turn does for balconies and views, how the price per m² rises with height. Sun and shade: one
  sentence only, as a side detail.
- nlws-homes: the sizes that were published (a table), 4 and 5 rooms and penthouses, balconies, the safe room (mamad), the
  specification as listings describe it, parking and storage, and a list "what to ask the seller" (the apartment plan; tower, floor
  and direction; area and balcony; parking and storage; the specification appendix; delivery date; and whether the price is for a
  right or for a finished apartment).
- nlws-life: a day in the life, the basement facilities, the fast lifts, the garbage chutes, the air conditioning, the car park, the
  school drop-off road.
- nlws-prices: the table of the three deals, their average and range, price per m² by height, a table of asking prices, a right
  versus a finished apartment, and the comparison with the area.
- nlws-costs: purchase tax (a bracket table: single apartment versus additional apartment and foreign resident) with the ₪10 million
  example; mortgage limits (75/70/50) with the example; the real-estate lawyer; the broker's fee under a written order; new
  immigrants. Links to the guides.
- nlws-buy: a numbered list of 7 to 8 steps, from choosing on this page to signing and taking delivery, including buying from abroad
  with a power of attorney; the WhatsApp button.
- nlws-sale: a market of rights holders, about 250 owners, at most 200 to 250 apartments expected for sale, what is known about
  renting; the WhatsApp button; a link to the brokers.
- nlws-when: the frame completed, the construction pace, the range of estimates 2026 to 2028, Form 4, the public works to the end of 2027.
- nlws-timeline: 9 to 11 dated points.
- nlws-park, nlws-square, nlws-transport: life around the towers, with a transport and distances table and walking minutes.
- nlws-faq: the questions in faq_questions, in that order.

## The HTML contract
{contract}
(WA_TEXT = "{wa}", FAQ_H2 = "{faq_h2}")

## Tone and language
{culture}
- {typography}
- Units: {units}
- Banned words and phrases: {banned}

## How to return the article (important)
The article is long, so it comes in three parts, each in ONE ```html code block with no text before or after it:
- Part 1 (now): lead, nlws-facts, nlws-choose, nlws-homes, nlws-life.
- Part 2 (when I write "continue"): nlws-prices, nlws-costs, nlws-buy, nlws-sale, nlws-when, nlws-timeline.
- Part 3 (when I write "continue"): nlws-park, nlws-square, nlws-transport, nlws-faq, and the closing div.
Do not shorten: every section reaches at least its budget. Do not repeat a sentence or a fact in two sections, except the lead and
the facts table.

## The evidence packet
```json
{packet}
```
"""

NAMES = {"en": "English", "fr": "French", "ru": "Russian", "ar": "Arabic"}


def main():
    for lang in ("he", "en", "fr", "ru", "ar"):
        p = packet(lang)
        js = json.dumps(p, ensure_ascii=False, indent=1)
        io.open(os.path.join(HERE, "packet-%s.json" % lang), "w", encoding="utf-8").write(js + "\n")
        d = L[lang]
        kw = " · ".join("%s (%s)" % (k, v) for k, v in d["keywords"])
        compact = json.dumps(p, ensure_ascii=False, separators=(",", ":"))
        fmt = dict(url=d["url"], wa=d["wa"], audience=d["audience"], names=d["names"], keywords=kw, related=d["related"],
                   minimum=p["words_minimum"], target=TOTAL, contract=HTML_CONTRACT, faq_h2=d["faq_h2"], culture=d["culture"],
                   typography=d["typography"], units=d["units"], banned=d["banned"], packet=compact,
                   lang_name=NAMES.get(lang, "Hebrew"))
        body = (PROMPT_HE if lang == "he" else PROMPT_XX).format(**fmt)
        head = ("# V7 prompt (%s): Kikar Hamedina article, 5,000+ net words\n\nBuilt by build_packets.py on 3.10.2026 from claims.py "
                "(%d claims) and links.json (every link GET 200 on 3.10.2026). Pasted as is into a new ChatGPT conversation; "
                "everything below the line is the prompt.\n\n---\n\n") % (lang, len(CLAIMS))
        io.open(os.path.join(HERE, "prompt-%s.md" % lang), "w", encoding="utf-8").write(head + body)
        print(lang, "packet", len(js), "chars | prompt", len(body), "chars | claims", len(p["claims"]))


if __name__ == "__main__":
    main()
