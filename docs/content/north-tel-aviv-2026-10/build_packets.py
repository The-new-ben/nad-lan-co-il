# -*- coding: utf-8 -*-
"""HAD-460 Stage A: packets and ChatGPT prompts for the language versions of the North Tel Aviv hub and of Rova 4.
Modelled on docs/research/2026-10-kikar-v7/build_packets.py (evidence -> brief -> ChatGPT -> fact check).

    python docs/content/north-tel-aviv-2026-10/build_packets.py

Writes packets/<page>-<lang>.json and packets/prompt-<page>-<lang>.md for page in (hub, rova-4) and lang in (en, fr, ru, ar),
plus links.json (internal links per page and language, with the GET status of 7.10.2026) and live-headings.json (the title, H1
and H2s of the other live pages in each language, for the duplicate check).

Differences from V7, on purpose: these are CULTURAL REWRITES of two live Hebrew pages, not new articles. ChatGPT gets the Hebrew
source section by section and must keep its H1/H2 order, its tables and its numbers one to one (i18n-brief.md); word budgets
follow the Hebrew length, not 5,000+. The prompt is split into messages (one per output part) so every message stays under
ChatGPT's practical input size.
"""
import datetime, io, json, os, re, sys, time

sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import check_translation as CT  # noqa: E402

CLAIMS = json.load(io.open(os.path.join(HERE, "claims.json"), encoding="utf-8"))
BY_ID = {c["claim_id"]: c for c in CLAIMS}
SITE = "https://nad-lan.co.il"
LANGS = ("en", "fr", "ru", "ar")
LANG_NAME = {"en": "English", "fr": "French", "ru": "Russian", "ar": "Arabic"}
FACTOR = {"en": 1.2, "fr": 1.3, "ru": 1.0, "ar": 1.0}   # words in the language per Hebrew word (Hebrew glues prepositions)
MAX_MSG = 40000                                            # characters per pasted message (V7 prompts were 39-45K)
LINK_CHECK = os.path.join(HERE, "source", "linkcheck-20261007.json")

# ============================================================== the two pages: sections in Hebrew order
# (id, Hebrew H2 or None for the lead, output part, claims the section must use)
SECTIONS = {
    "hub": [
        ("hub-opening", "פתיחה", 1, ["H-01", "H-04", "H-09"]),
        ("hub-areas", "מהו צפון תל אביב והשכונות", 1, ["H-02", "H-03", "H-01", "H-09"]),
        ("hub-life", "אופי האזור ואיכות החיים", 1, ["H-11"]),
        ("hub-anchors", "מוסדות עוגן", 1, []),
        ("hub-projects", "הפרויקטים החדשים וההתחדשות", 1, ["H-04", "H-05", "H-06", "H-03", "H-01", "H-09"]),
        ("hub-prices", "מחירים לפי שכונה", 2, ["H-07", "H-08", "H-02", "H-01"]),
        ("hub-compare", "השוואת שכונות", 2, ["H-01"]),
        ("hub-transport", "תחבורה ונגישות", 2, ["H-11", "H-01"]),
        ("hub-fit", "למי מתאים האזור", 2, []),
        ("hub-legal", "זווית משפטית ומיסויית", 2, ["H-04", "H-05", "H-09"]),
        ("hub-faq", "שאלות נפוצות", 2, ["H-02", "H-03", "H-04", "H-05", "H-06", "H-01"]),
        ("hub-abroad", "משקיעים מחו״ל", 2, []),
    ],
    "rova-4": [
        ("r4-lead", None, 1, ["R4-01", "R4-04", "R4-17", "R4-53", "R4-55", "R4-60"]),
        ("r4-where", "איפה נמצא רובע 4: הגבולות והרחובות", 1, ["R4-02", "R4-06", "R4-07", "R4-08", "R4-09", "R4-10", "R4-19"]),
        ("r4-areas", "השכונות של רובע 4", 1, ["R4-11", "R4-52", "R4-53", "R4-54", "R4-10"]),
        ("r4-plan", "תוכנית רובע 4 (תא/3729/א) בשפה פשוטה", 1,
         ["R4-17", "R4-07", "R4-13", "R4-09", "R4-14", "R4-15", "R4-16", "R4-18", "R4-19", "R4-20", "R4-21", "R4-22"]),
        ("r4-prices", "מחירי דירות ברובע 4 ב-2026", 2,
         ["R4-52", "R4-53", "R4-54", "R4-55", "R4-56", "R4-57", "R4-58", "R4-59", "R4-64", "R4-67", "R4-60", "R4-61", "R4-62",
          "R4-63", "R4-65", "R4-87", "R4-68", "R4-69", "R4-70", "R4-71", "R4-72", "R4-73", "R4-74", "R4-75", "R4-76", "R4-77",
          "R4-78", "R4-79", "R4-81", "R4-80", "R4-82", "R4-65b", "R4-66", "R4-84"]),
        ("r4-kikar", "כיכר המדינה והמגדלים", 3, ["R4-34", "R4-36"]),
        ("r4-renewal", "התחדשות עירונית ברובע 4: הפרויקטים", 3,
         ["R4-39", "R4-14", "R4-41", "R4-44", "R4-45", "R4-43", "R4-46", "R4-50", "R4-47", "R4-42", "R4-49", "R4-40"]),
        ("r4-transport", "תחבורה ברובע 4", 3, ["R4-31"]),
        ("r4-vs3", "רובע 4 או הצפון הישן?", 3, ["R4-11b", "R4-06", "R4-07", "R4-02"]),
        ("r4-fit", "למי מתאים לגור ברובע 4", 3, ["R4-52", "R4-53", "R4-54", "R4-60", "R4-63", "R4-31", "R4-34", "R4-93"]),
        ("r4-faq", "שאלות נפוצות", 3, ["R4-01", "R4-17", "R4-07", "R4-11b", "R4-52", "R4-53", "R4-54", "R4-55", "R4-60",
                                       "R4-63", "R4-16"]),
    ],
}
HE_URL = {"hub": SITE + "/north-tel-aviv/", "rova-4": SITE + "/north-tel-aviv/rova-4/"}
TARGET = {p: {l: SITE + "/%s%s" % (l, HE_URL[p][len(SITE):]) for l in LANGS} for p in HE_URL}

# ============================================================== per language: H1, H2s, FAQ, names, SERP, culture
L = {
    "en": {
        "h1": {"hub": "North Tel Aviv: Neighborhoods, New Projects and Apartment Prices",
               "rova-4": "Rova 4, Tel Aviv's New North: Boundaries, the Plan and Apartment Prices"},
        "seo_kw": {"hub": "North Tel Aviv", "rova-4": "Rova 4 Tel Aviv / New North"},
        "h2": {"hub": ["North Tel Aviv at a glance", "What North Tel Aviv includes: the neighborhoods",
                       "Character and quality of life in North Tel Aviv",
                       "The anchors: Tel Aviv University, Ramat Aviv Mall and Yarkon Park",
                       "New projects and urban renewal in North Tel Aviv", "Apartment prices by neighborhood",
                       "Comparing the neighborhoods", "Transport and access", "Who North Tel Aviv suits",
                       "Legal and tax points before you buy", "Frequently asked questions",
                       "Buying in North Tel Aviv from abroad"],
               "rova-4": [None, "Where Rova 4 is: boundaries and main streets", "The neighborhoods of Rova 4",
                          "The Rova 4 plan (TA/3729/A) in plain English", "Apartment prices in Rova 4 in 2026",
                          "Kikar HaMedina and the towers", "Urban renewal in Rova 4: the projects",
                          "Getting around Rova 4: light rail and main roads", "Rova 4 or the Old North?", "Who Rova 4 suits",
                          "Frequently asked questions"]},
        "h3_hub": ["Tel Aviv University", "Ramat Aviv Mall", "Yarkon Park"],
        "faq": {"hub": ["Is North Tel Aviv better for living or for investment?",
                        "What is the difference between Ramat Aviv and Neve Avivim?",
                        "Why is Einstein Street a focus of new building?",
                        "Will the Sde Dov quarter bring prices down in North Tel Aviv?",
                        "What should you check before buying in a new project in North Tel Aviv?"],
                "rova-4": ["Where is Rova 4 in Tel Aviv?", "What is the Rova 4 plan?", "What is Tel Aviv's quarters plan?",
                           "Which streets are in Rova 4?", "How much does an apartment in Rova 4 cost?",
                           "Where is Rova 3, and how is it different from Rova 4?",
                           "Are Kikar HaMedina and Bavli in Rova 4?", "Will I have to pay a betterment levy in Rova 4?"]},
        "faq_h2": "Frequently asked questions",
        "names": "North Tel Aviv (צפון תל אביב). The New North (הצפון החדש) = Rova 4, Tel Aviv's 4th quarter: write \"Rova 4 "
                 "(the New North)\" at first mention, then \"Rova 4\" or \"the New North\". The Old North (הצפון הישן) = Rova 3. "
                 "Kikar HaMedina Towers (מגדלי כיכר המדינה); the square: Kikar HaMedina (once: \"State Square\"). Ramat Aviv, "
                 "Ramat Aviv Gimel, Green Ramat Aviv, Neve Avivim, Shikun Lamed (שכונת ל׳; in the official data \"Tochnit "
                 "Lamed\"), Bavli, Sde Dov, Yarkon Park, Tel Aviv University, Ramat Aviv Mall, Einstein Street, Ibn Gabirol, "
                 "Namir Road, the Ayalon highway, Herzliya, Givat Amal B, Park Tzameret, He Be'Iyar Street, Weizmann, "
                 "Jabotinsky, Arlozorov, Pinkas, Yehuda HaMaccabi, Shaul HaMelech Boulevard, David HaMelech, Dubnov, Bnei Dan, "
                 "Be'eri, Henrietta Szold, Ichilov (Tel Aviv Sourasky Medical Center), Tel Aviv Center (Savidor) station, "
                 "Habima, Rabin Square. Plans: TAMA 38 (the national plan for strengthening buildings, explained once), "
                 "pinui-binui (evacuation and rebuilding), TA/3729/A. Companies as they write themselves: Hagag Group, "
                 "Ashdar, Azorim, Shikun & Binui, Bayit VeGag, Africa Israel Renewal (the Hebrew says \"אפריקה התחדשות\"), "
                 "Adam Shuster, Anshei HaIr, Yaaz, Levinstein Group, Noga. Architect: Moshe Tzur. Tel Aviv-Yafo for the city "
                 "as a municipality. Rooms: the Israeli count (\"4 rooms\").",
        "keywords": [("tel aviv real estate", 480), ("tel aviv apartments for sale", 390), ("buy apartment in tel aviv", 390),
                     ("ramat aviv", 390), ("sde dov", 320), ("tel aviv neighborhoods", 140), ("old north tel aviv", 70),
                     ("kikar hamedina", 70), ("hamedina square", 50), ("luxury apartments tel aviv", 50),
                     ("north tel aviv", 40), ("kikar hamedina tel aviv", 40), ("tama 38", 40), ("neve avivim", 20),
                     ("bavli tel aviv", 20), ("best neighborhoods in tel aviv", 20), ("tel aviv real estate prices", 20),
                     ("new north tel aviv", "no volume data; Google shows related searches for it"),
                     ("rova 4 tel aviv / tel aviv district 4", "no volume data")],
        "related": "Google (Israel, English) for \"new north tel aviv\": AI overview SHOWN (\"the urban area east of Ibn Gabirol "
                   "developed after 1948\"); related searches: new north tel aviv for sale / price / for rent / apartments for "
                   "sale, Old North Tel Aviv, Tel Aviv neighborhoods map, North Star Tel Aviv. People also ask (US, \"north tel "
                   "aviv neighborhoods real estate\"): What is the most desirable neighborhood to live in Tel Aviv? Can "
                   "foreigners buy property in Tel Aviv? What are the richest neighborhoods in Tel Aviv? What is the best place "
                   "for Americans to live in Israel?",
        "audience": "International buyers (US, UK, Canada, Australia, South Africa) and English-speaking Israelis and olim. They "
                    "compare in shekels, often buy from abroad, and need Israeli terms decoded once (rooms, TAMA 38, "
                    "pinui-binui, purchase tax, a median deal price).",
        "culture": "US spelling (neighborhood) because that is how the searches are typed. Decode the Israeli room count and "
                   "TAMA 38 once. Warm, confident and factual: a premium real-estate guide, not a warning leaflet. Where the "
                   "Hebrew speaks to Israeli families, keep it, and add the foreign buyer's angle in words (no new numbers): "
                   "managing from abroad, a lawyer with a power of attorney, buying does not give residency.",
        "typography": "Dates as 23 May 2018 or May 2018, or keep the Hebrew style 23.5.2018 in tables; ₪ before the number "
                      "(₪6,835,800); ranges with \"to\"; no em dash (—) and no en dash (–).",
        "units": "m² and ₪ only. No square feet, acres, dollars or euros. A dunam may be explained once (1 dunam = 1,000 m²).",
        "banned": "interface · demo · model (as 3D) · hotspot · overlay · engine · layer · tile · prototype · simulation · "
                  "technology · \"the system\" · \"the platform\" · digital experience · 3D · Atlas · coming soon · \"free "
                  "advice\" (only the site's floating bar says it) · any source or media name (Wikipedia, Globes, Calcalist, "
                  "TheMarker, Ynet, Maariv, Bizportal, Madlan, Yad2) · delve · nestled · boasts · a testament to · red flag · "
                  "beware · it is important to note · in conclusion",
        "in_hebrew": "(in Hebrew)",
        "seo": "SEO title in English, at most 60 characters, containing \"North Tel Aviv\" (hub) / \"Rova 4\" and \"New North\" "
               "(Rova 4). Description in English, at most 155 characters.",
    },
    "fr": {
        "h1": {"hub": "Nord de Tel Aviv : quartiers, programmes neufs et prix de l'immobilier",
               "rova-4": "Rova 4 à Tel Aviv, le Nouveau Nord : limites, plan d'urbanisme et prix"},
        "seo_kw": {"hub": "nord de Tel Aviv / immobilier Tel Aviv", "rova-4": "Rova 4 Tel Aviv / Nouveau Nord"},
        "h2": {"hub": ["Le nord de Tel Aviv en bref", "Les quartiers du nord de Tel Aviv", "Cadre de vie et qualité de vie",
                       "Les grands repères : l'université, le centre commercial et le parc HaYarkon",
                       "Programmes neufs et rénovation urbaine dans le nord", "Prix de l'immobilier par quartier",
                       "Comparer les quartiers du nord", "Transports et accès", "À qui s'adresse le nord de Tel Aviv",
                       "Points juridiques et fiscaux avant d'acheter", "Questions fréquentes",
                       "Acheter dans le nord de Tel Aviv depuis l'étranger"],
               "rova-4": [None, "Où se trouve le Rova 4 : limites et grandes rues", "Les quartiers du Rova 4",
                          "Le plan du Rova 4 (TA/3729/A) expliqué simplement", "Rova 4 : les prix des appartements en 2026",
                          "Kikar HaMedina et ses tours", "Rénovation urbaine dans le Rova 4 : les projets",
                          "Se déplacer dans le Rova 4 : tramway et grands axes", "Rova 4 ou Vieux Nord ?",
                          "À qui convient le Rova 4", "Questions fréquentes"]},
        "h3_hub": ["L'université de Tel Aviv", "Le centre commercial de Ramat Aviv", "Le parc HaYarkon"],
        "faq": {"hub": ["Le nord de Tel Aviv convient-il mieux pour y vivre ou pour investir ?",
                        "Quelle différence entre Ramat Aviv et Neve Avivim ?",
                        "Pourquoi la rue Einstein concentre-t-elle autant de constructions neuves ?",
                        "Le quartier de Sde Dov va-t-il faire baisser les prix dans le nord de Tel Aviv ?",
                        "Que vérifier avant d'acheter dans un programme neuf du nord de Tel Aviv ?"],
                "rova-4": ["Où se trouve le Rova 4 à Tel Aviv ?", "Qu'est-ce que le plan du Rova 4 ?",
                           "Qu'est-ce que le plan des quartiers (Rova) de Tel Aviv ?", "Quelles rues font partie du Rova 4 ?",
                           "Combien coûte un appartement dans le Rova 4 ?",
                           "Où se trouve le Rova 3 et en quoi diffère-t-il du Rova 4 ?",
                           "Kikar HaMedina et Bavli sont-ils dans le Rova 4 ?",
                           "Faut-il payer une taxe de plus-value (hetel hashbaha) dans le Rova 4 ?"]},
        "faq_h2": "Questions fréquentes",
        "names": "le nord de Tel Aviv (צפון תל אביב). Le Nouveau Nord (הצפון החדש) = le Rova 4, 4e arrondissement de la ville : "
                 "« le Rova 4 (le Nouveau Nord) » à la première mention. Le Vieux Nord (הצפון הישן) = le Rova 3. Les tours "
                 "Kikar HaMedina (Kikar HaMedina Towers, מגדלי כיכר המדינה) ; la place Kikar HaMedina (une fois : « la place de "
                 "l'État »). Ramat Aviv, Ramat Aviv Gimel, Ramat Aviv la verte, Neve Avivim, le quartier Lamed (שכונת ל׳), "
                 "Bavli, Sde Dov, le parc HaYarkon, l'université de Tel Aviv, le centre commercial de Ramat Aviv, la rue "
                 "Einstein, Ibn Gabirol, la route Namir, l'autoroute Ayalon, Herzliya, Givat Amal B, Park Tzameret, la rue He "
                 "Be'Iyar, Weizmann, Jabotinsky, Arlozorov, Pinkas, Yehuda HaMaccabi, le boulevard Shaul HaMelech, Ichilov, la "
                 "gare Tel Aviv Centre (Savidor), Habima, la place Rabin. TAMA 38 (plan national de renforcement des immeubles, "
                 "expliqué une fois), pinoui-binoui (démolition-reconstruction), TA/3729/A. Sociétés comme elles s'écrivent "
                 "(Hagag Group, Ashdar, Azorim, Shikun & Binui, Bayit VeGag...). Tel Aviv-Jaffa pour la municipalité.",
        "keywords": [("immobilier israel", 320), ("ramat aviv", 170), ("immobilier tel aviv", 140),
                     ("appartement tel aviv", 140), ("acheter appartement tel aviv", 110),
                     ("appartement a vendre tel aviv", 110), ("acheter un appartement en israel", 90),
                     ("quartiers tel aviv", 50), ("prix immobilier tel aviv", 50), ("kikar hamedina", 40),
                     ("nord tel aviv / quartier nord tel aviv / vieux nord tel aviv", "no volume data")],
        "related": "Google France, « quartiers nord tel aviv immobilier » : aperçu IA AFFICHÉ (Vieux Nord, Park Tzameret, Ramat "
                   "Aviv Alef/Bet/Gimel). Questions associées : Quel est le meilleur quartier de Tel Aviv ? Quel est le "
                   "quartier le plus huppé de Tel Aviv ? Quel est le prix moyen d'un appartement à Tel Aviv ? Recherches "
                   "associées : immobilier de luxe Tel Aviv, prix tel aviv immobilier, agence immobilière Tel Aviv.",
        "audience": "Acheteurs français et belges (alyah, pied-à-terre, investissement) et olim francophones déjà en Israël qui "
                    "montent en gamme. Ils achètent souvent à distance et comparent en shekels.",
        "culture": "« 4 pièces » israélien = 4 pièces français (séjour + 3 chambres) : le dire une fois. Expliquer TAMA 38 et "
                   "pinoui-binoui une fois. Les mots du lecteur : quartier chic, programme neuf, sur plan, alyah, "
                   "pied-à-terre, rénovation urbaine. Montrer qu'on peut tout préparer à distance (avocat avec procuration) "
                   "sans ajouter de chiffre.",
        "typography": "Espace insécable avant : ; ? ! et entre milliers (6 835 800 ₪) ; virgule décimale (30,7 %) ; dates « 23 "
                      "mai 2018 » ou 23.5.2018 dans les tableaux ; guillemets « » ; pas de tiret long (—) ni de tiret moyen (–).",
        "units": "m² et ₪ seulement. Pas d'euros, pas d'hectares en plus du dunam (1 dunam = 1 000 m², une seule fois).",
        "banned": "interface · démo · modèle (au sens 3D) · moteur · calque · prototype · simulation · technologie · « le "
                  "système » · « la plateforme » · expérience digitale · 3D · Atlas · bientôt · « conseil gratuit » · tout nom "
                  "de source ou de média (Wikipédia, Globes, Calcalist, Ynet...) · il est important de noter · force est de "
                  "constater · en conclusion · véritable écrin · niché",
        "in_hebrew": "(en hébreu)",
        "seo": "Titre SEO en français, 60 caractères au plus, avec « Tel Aviv » et « nord » (hub) / « Rova 4 » et « Nouveau Nord » "
               "(Rova 4). Description en français, 155 caractères au plus.",
    },
    "ru": {
        "h1": {"hub": "Север Тель-Авива: районы, новые проекты и цены на квартиры",
               "rova-4": "Рова 4 в Тель-Авиве, Новый Север: границы, план застройки и цены"},
        "seo_kw": {"hub": "север Тель-Авива / квартиры в Тель-Авиве", "rova-4": "Рова 4 / Новый Север Тель-Авива"},
        "h2": {"hub": ["Север Тель-Авива коротко", "Какие районы входят в север Тель-Авива",
                       "Характер района и качество жизни",
                       "Главные ориентиры: университет, торговый центр «Рамат-Авив» и парк Яркон",
                       "Новые проекты и городское обновление на севере", "Цены на квартиры по районам",
                       "Сравнение районов севера", "Транспорт и доступность", "Кому подходит север Тель-Авива",
                       "Юридические и налоговые вопросы перед покупкой", "Частые вопросы",
                       "Покупка на севере Тель-Авива из-за границы"],
               "rova-4": [None, "Где находится Рова 4: границы и главные улицы", "Районы Рова 4",
                          "План Рова 4 (TA/3729/A) простыми словами", "Рова 4: цены на квартиры в 2026 году",
                          "Кикар ха-Медина и башни", "Городское обновление в Рова 4: проекты",
                          "Транспорт в Рова 4: легкорельсовые линии и главные дороги", "Рова 4 или Старый Север?",
                          "Кому подходит Рова 4", "Частые вопросы"]},
        "h3_hub": ["Тель-Авивский университет", "Торговый центр «Рамат-Авив»", "Парк Яркон"],
        "faq": {"hub": ["Север Тель-Авива больше подходит для жизни или для инвестиций?",
                        "Чем Рамат-Авив отличается от Неве-Авивим?",
                        "Почему улица Эйнштейна стала центром новой застройки?",
                        "Снизит ли квартал Сде-Дов цены на севере Тель-Авива?",
                        "Что проверить перед покупкой квартиры в новом проекте на севере Тель-Авива?"],
                "rova-4": ["Где находится Рова 4 в Тель-Авиве?", "Что такое план Рова 4?",
                           "Что такое план районов (рова) Тель-Авива?", "Какие улицы входят в Рова 4?",
                           "Сколько стоит квартира в Рова 4?", "Где находится Рова 3 и чем он отличается от Рова 4?",
                           "Кикар ха-Медина и Бавли находятся в Рова 4?", "Придётся ли платить налог на улучшение (hetel hashbaha) в Рова 4?"]},
        "faq_h2": "Частые вопросы",
        "names": "север Тель-Авива (צפון תל אביב). Новый Север (הצפון החדש) = Рова 4, четвёртый административный район (рова) "
                 "города: «Рова 4 (Новый Север)» при первом упоминании. Старый Север (הצפון הישן) = Рова 3. Башни Кикар "
                 "ха-Медина (Kikar HaMedina Towers, מגדלי כיכר המדינה); площадь Кикар ха-Медина (один раз: «Площадь "
                 "Государства»). Рамат-Авив (так ищут: «рамат авив», 880 в месяц), Рамат-Авив Гимель, Зелёный Рамат-Авив, "
                 "Неве-Авивим, район Ламед (שכונת ל׳), Бавли, Сде-Дов, парк Яркон, Тель-Авивский университет, торговый центр "
                 "«Рамат-Авив», улица Эйнштейна, Ибн Гвироль, дорога Намир, шоссе Аялон, Герцлия, Гиват-Амаль Бет, Парк "
                 "Цамерет, улица Хе бе-Ияр (He Be'Iyar), Вейцман, Жаботинский, Арлозоров, Пинкас, Иегуда ха-Маккаби, бульвар "
                 "Шауль ха-Мелех, больница Ихилов, станция Тель-Авив Центр (Савидор), Габима, площадь Рабина. ТАМА 38 "
                 "(национальный план укрепления зданий, объяснить один раз), пинуй-бинуй (снос и новое строительство), код "
                 "плана латиницей: TA/3729/A. Компании так, как они пишутся сами (Hagag Group, Ashdar, Azorim, Shikun & Binui, "
                 "Bayit VeGag...). Тель-Авив-Яффо для муниципалитета.",
        "keywords": [("рамат авив", 880), ("купить квартиру в израиле", 140), ("квартиры в израиле", 140),
                     ("недвижимость в израиле", 90), ("купить квартиру в тель авиве", 50), ("районы тель авива", 30),
                     ("квартиры в тель авиве", 20), ("кикар ха медина", 10), ("недвижимость в тель авиве", 10),
                     ("цены на квартиры в тель авиве", 10),
                     ("север тель авива / новый север тель авив / старый север тель авива", "no volume data")],
        "related": "Google Israel in Russian: the live SERP request timed out on 7.10.2026 (not recorded). The Kikar HaMedina "
                   "Russian SERP of 30.9.2026 (docs/research/2026-09-30-kikar-hamedina/serp-ru.md) showed buying intent around "
                   "Israel and Tel Aviv ten times larger than any place name. Typical questions: сколько стоит квартира, налог "
                   "на покупку, ипотека для нерезидентов, какой район выбрать.",
        "audience": "Русскоязычные израильтяне (знают слова салон, маклер, мас рехиша, ТАМА 38) и покупатели из-за границы. Им "
                    "важны цена, цена квадратного метра, налоги, сроки и надёжность проекта.",
        "culture": "Объяснить один раз израильский счёт комнат («4 комнаты: салон и три спальни»). ТАМА 38 и пинуй-бинуй объяснить "
                   "один раз. Тон уверенный и тёплый, без канцелярита. Покупка через адвоката по доверенности возможна, без "
                   "новых цифр.",
        "typography": "Десятичная запятая (30,7%), неразрывный пробел между тысячами (6 835 800 ₪), даты 23.05.2018 или «23 мая "
                      "2018 года», кавычки «ёлочки»; без длинного (—) и среднего (–) тире: предложения строятся без тире.",
        "units": "м² и ₪. Без долларов и гектаров; дунам можно объяснить один раз (1 дунам = 1 000 м²).",
        "banned": "интерфейс · демо · модель (в смысле 3D) · движок · слой · прототип · симуляция · технология · «система» · "
                  "«платформа» · цифровой опыт · 3D · Атлас · скоро · «бесплатная консультация» · любые названия источников и "
                  "СМИ (Википедия, Globes, Calcalist, Ynet, Маарив...) · стоит отметить · важно понимать · в заключение · "
                  "уникальный шанс",
        "in_hebrew": "(на иврите)",
        "seo": "SEO-заголовок по-русски, не длиннее 60 знаков, со словами «север Тель-Авива» (hub) / «Рова 4» и «Новый Север» "
               "(Rova 4). Описание по-русски, не длиннее 155 знаков.",
    },
    "ar": {
        "h1": {"hub": "North Tel Aviv: Neighborhoods, New Projects and Apartment Prices",
               "rova-4": "Rova 4, Tel Aviv's New North: Boundaries, the Plan and Apartment Prices"},
        "seo_kw": {"hub": "North Tel Aviv (English title, the owner's ruling)",
                   "rova-4": "Rova 4 / New North (English title, the owner's ruling)"},
        "h2": {"hub": ["شمال تل أبيب في لمحة", "ما الذي يشمله شمال تل أبيب: الأحياء", "طابع المنطقة وجودة الحياة",
                       "المعالم الكبرى: الجامعة والمجمع التجاري وحديقة اليركون", "المشاريع الجديدة والتجديد الحضري في الشمال",
                       "أسعار الشقق حسب الحي", "مقارنة بين أحياء الشمال", "المواصلات وسهولة الوصول",
                       "لمن يناسب شمال تل أبيب", "جوانب قانونية وضريبية قبل الشراء", "أسئلة شائعة",
                       "الشراء في شمال تل أبيب من خارج البلاد"],
               "rova-4": [None, "أين يقع روفاع 4: الحدود والشوارع الرئيسية", "أحياء روفاع 4",
                          "مخطط روفاع 4 (TA/3729/A) بلغة بسيطة", "أسعار الشقق في روفاع 4 في 2026", "كيكار همدينا والأبراج",
                          "التجديد الحضري في روفاع 4: المشاريع", "المواصلات في روفاع 4: القطار الخفيف والطرق الرئيسية",
                          "روفاع 4 أم الشمال القديم؟", "لمن يناسب السكن في روفاع 4", "أسئلة شائعة"]},
        "h3_hub": ["جامعة تل أبيب", "مجمع رمات أفيف التجاري", "حديقة اليركون"],
        "faq": {"hub": ["هل شمال تل أبيب أنسب للسكن أم للاستثمار؟", "ما الفرق بين رمات أفيف ونافيه أفيفيم؟",
                        "لماذا أصبح شارع أينشتاين مركزاً للبناء الجديد؟", "هل سيخفض حي سدي دوف الأسعار في شمال تل أبيب؟",
                        "ماذا يجب فحصه قبل شراء شقة في مشروع جديد في شمال تل أبيب؟"],
                "rova-4": ["أين يقع روفاع 4 في تل أبيب؟", "ما هو مخطط روفاع 4؟", "ما هو مخطط الأحياء (روفاع) في تل أبيب؟",
                           "ما الشوارع التي تقع في روفاع 4؟", "كم سعر شقة في روفاع 4؟",
                           "أين يقع روفاع 3 وما الفرق بينه وبين روفاع 4؟", "هل كيكار همدينا وبافلي ضمن روفاع 4؟",
                           "هل يجب دفع ضريبة التحسين (هيتل هشبحاه) في روفاع 4؟"]},
        "faq_h2": "أسئلة شائعة",
        "names": "شمال تل أبيب (צפון תל אביב). الشمال الجديد (הצפון החדש) = روفاع 4، المنطقة الإدارية الرابعة في المدينة: «روفاع 4 "
                 "(الشمال الجديد)» عند أول ذكر. الشمال القديم (הצפון הישן) = روفاع 3. أبراج كيكار همدينا (Kikar HaMedina Towers، "
                 "מגדלי כיכר המדינה)؛ ساحة كيكار همدينا (مرة واحدة: «ساحة الدولة»). رمات أفيف (هكذا يُبحث عنها: 90 بحثاً "
                 "شهرياً)، رمات أفيف غيمل، نافيه أفيفيم، حي لامد (שכונת ל׳)، بافلي، سدي دوف، حديقة اليركون، جامعة تل أبيب، "
                 "مجمع رمات أفيف التجاري، شارع أينشتاين، ابن جبيرول، طريق نمير، طريق أيالون السريع، هرتسليا، غفعات عمال ب، "
                 "بارك تسامرت، شارع He Be'Iyar، وايزمان، جابوتنسكي، أرلوزوروف، بنكاس، يهودا همكابي، جادة شاؤول هملخ، مستشفى "
                 "إيخيلوف، محطة تل أبيب المركز (سافيدور)، هبيما، ساحة رابين. تاما 38 (الخطة القطرية لتدعيم المباني، تُشرح "
                 "مرة واحدة)، بينوي بينوي (الهدم وإعادة البناء)، رمز المخطط بالحروف اللاتينية TA/3729/A. الشركات بأسمائها "
                 "اللاتينية (Hagag Group، Ashdar، Azorim، Shikun & Binui، Bayit VeGag...). الأماكن التي لا اسم عربياً لها "
                 "في مصدرها تبقى بالإنجليزية: لا اسم مخترَع. تل أبيب يافا للبلدية.",
        "keywords": [("تل أبيب", 140), ("رمات أفيف", 90), ("شقق للبيع في اسرائيل", 10), ("التجديد الحضري", 10),
                     ("شمال تل أبيب، أحياء تل أبيب، عقارات تل أبيب، شقق للبيع في تل أبيب، اسعار الشقق في تل أبيب، كيكار همدينا",
                      "no volume data")],
        "related": "Arabic-script searches for Tel Aviv property are close to none (Google Ads, Israel, 7.10.2026; the same "
                   "finding as docs/research/2026-09-30-kikar-hamedina/serp-ar.md). The Arabic page serves readers who arrive "
                   "by a link, the site's language switch or a shared WhatsApp message; Ramat Aviv is the one place name they "
                   "type in Arabic.",
        "audience": "قرّاء عرب، معظمهم في إسرائيل وكثير منهم عائلات: المدارس، مواقف السيارات، المواصلات، سعر المتر، والتمويل.",
        "culture": "عربية فصحى معاصرة واضحة، قريبة من لغة الصحافة الاقتصادية. شرح عدد الغرف الإسرائيلي مرة واحدة («4 غرف: صالون "
                   "وثلاث غرف نوم»). تاما 38 وبينوي بينوي يُشرحان مرة واحدة. نبرة دافئة وواثقة.",
        "typography": "أرقام غربية كما تكتبها الصحافة العربية في إسرائيل (6,835,800 ₪؛ 30.7%)؛ تواريخ 23.5.2018؛ أسماء الأشهر "
                      "الشامية (أيار، أيلول...) عند ذكر الشهر بالكلمة؛ بلا شرطة طويلة (—) وبلا شرطة متوسطة (–).",
        "units": "م² و₪ فقط. يمكن شرح الدونم مرة واحدة (1 دونم = 1,000 م²).",
        "banned": "واجهة برمجية · عرض تجريبي · نموذج (بمعنى ثلاثي الأبعاد) · محرّك · طبقة · نموذج أولي · محاكاة · تكنولوجيا · «النظام» "
                  "· «المنصة» · تجربة رقمية · ثلاثي الأبعاد · أطلس · قريباً · «استشارة مجانية» · أي اسم لمصدر أو وسيلة إعلام "
                  "(ويكيبيديا، غلوبس، كالكاليست...) · تجدر الإشارة · في الختام · لا شك",
        "in_hebrew": "(بالعبرية)",
        "seo": "The SEO title in ENGLISH (the owner's ruling of 28.9.2026: Arabic pages carry English titles, like the H1), at "
               "most 60 characters, the same rule as English. The description in Arabic, at most 155 characters.",
    },
}

# ============================================================== Hebrew source: clean HTML per section
KEEP = {"h1", "h2", "h3", "p", "ul", "ol", "li", "table", "thead", "tbody", "tr", "th", "td", "a", "b"}


def clean_html(h):
    h = re.sub(r"<(script|style|svg|figure)\b.*?</\1>", "", h, flags=re.S | re.I)
    h = re.sub(r"<!--.*?-->", "", h, flags=re.S)
    h = re.sub(r"<span class='eyebrow'>(.*?)</span>", r'<p class="nl-eyebrow">\1</p>', h)
    h = re.sub(r"<div class='cards'>", "<ul class=\"nl-cards\">", h)
    h = re.sub(r"<div class='card'>(.*?)</div>", lambda m: "<li>%s</li>" % re.sub(r"</?p>", " ", m.group(1)).strip(), h,
               flags=re.S)
    h = re.sub(r"<div class='note'>(.*?)</div>", r'<p class="nl-note">\1</p>', h, flags=re.S)
    h = re.sub(r"<div class='cta'>(.*?)</div>", r'<p class="nl-cta">\1</p>', h, flags=re.S)
    h = re.sub(r"<div class='disclaimer'>.*?</div>", "", h, flags=re.S)

    def tag(m):
        close, name, attrs = m.group(1), m.group(2).lower(), m.group(3) or ""
        if name not in KEEP:
            return ""
        if close:
            return "</%s>" % name
        keep = []
        hm = re.search(r"href=[\"']([^\"']+)[\"']", attrs)
        if name == "a" and hm:
            href = hm.group(1)
            if href.startswith("/"):
                href = SITE + href
            keep.append('href="%s"' % href)
        cm = re.search(r"class=[\"'](nl-[a-z-]+|lede)[\"']", attrs)
        if cm:
            keep.append('class="%s"' % cm.group(1))
        return "<%s%s>" % (name, (" " + " ".join(keep)) if keep else "")
    h = re.sub(r"<(/?)([a-zA-Z0-9]+)([^>]*)>", tag, h)
    h = re.sub(r"<ul class=\"nl-cards\">(.*?)(?=<p class=\"nl-note\">)", lambda m: "<ul class=\"nl-cards\">" + m.group(1) + "</ul>",
               h, flags=re.S)
    h = re.sub(r"[ \t]+", " ", h)
    h = re.sub(r"\s*\n\s*", "\n", h)
    h = re.sub(r">\s+<", "><", h)
    h = re.sub(r"(</(?:p|h1|h2|h3|li|tr|table|ul|ol|thead|tbody)>)", r"\1\n", h)
    return h.strip()


def split_sections(page, h):
    """the cleaned Hebrew article -> {section id: html}"""
    secs = SECTIONS[page]
    out = {}
    pos = []
    for sid, h2, part, _ in secs:
        if h2 is None:
            pos.append((sid, 0))
            continue
        i = h.find("<h2>%s</h2>" % h2)
        assert i >= 0, (page, h2)
        pos.append((sid, i))
    for k, (sid, i) in enumerate(pos):
        j = pos[k + 1][1] if k + 1 < len(pos) else len(h)
        out[sid] = h[i:j].strip()
    if page == "hub":   # the H1 and eyebrow before the opening's H2 belong to the opening
        first = pos[0][1]
        out["hub-opening"] = h[:first].strip() + "\n" + out["hub-opening"]
        # the multilingual keyword line and the 'sources' line close the abroad section: not translated
        out["hub-abroad"] = re.sub(r"<p>North Tel Aviv real estate /.*?</p>\n?", "", out["hub-abroad"])
        out["hub-abroad"] = re.sub(r"<p>מקורות לעיון:.*?</p>\n?", "", out["hub-abroad"])
    return out


def words(h):
    return CT.word_count(CT.visible_text(h), "he")


def table_words(h):
    return sum(words(t) for t in re.findall(r"<table>.*?</table>", h, re.S))


# ============================================================== links
def build_links():
    lc = json.load(io.open(LINK_CHECK, encoding="utf-8"))
    status = {SITE + u: v["status"] for u, v in lc["results"].items()}

    def st(u):
        return status.get(u, "not checked")
    (hub_html, _), (rova_html, _) = CT.hebrew_sources()
    he_links = {}
    for page, h in (("hub", hub_html), ("rova-4", rova_html)):
        seen, lst = set(), []
        for href, anchor in re.findall(r"<a\b[^>]*href=[\"']([^\"']+)[\"'][^>]*>(.*?)</a>", h, re.S):
            if href.startswith("mailto:") or href.startswith("#"):
                continue
            full = SITE + href if href.startswith("/") else href
            if full in seen:
                continue
            seen.add(full)
            lst.append({"url": full, "anchor_he": CT.strip_tags(anchor), "status": st(full)})
        he_links[page] = lst
    # language equivalents that exist (GET 200 on 7.10.2026); everything else stays Hebrew
    eq = {
        SITE + "/projects/hamedina/": {l: SITE + "/projects/hamedina-%s/" % l for l in LANGS},
        SITE + "/purchase-tax-calculator/": {"en": SITE + "/israel-purchase-tax-foreign-residents/"},
        SITE + "/mortgage-calculator/": {"en": SITE + "/israel-mortgage-non-residents/"},
    }
    extras = {
        "en": [("/en/new-projects/", "new projects in Israel"), ("/en/buy-property-in-israel/", "buying a home in Israel from abroad"),
               ("/projects/hamedina-en/", "Kikar HaMedina Towers"), ("/projects/rainbow-tel-aviv-en/", "Rainbow in Sde Dov"),
               ("/en/brokers/", "licensed real estate brokers")],
        "fr": [("/fr/new-projects/", "programmes neufs en Israël"), ("/projects/hamedina-fr/", "les tours Kikar HaMedina"),
               ("/projects/rainbow-tel-aviv-fr/", "Rainbow à Sde Dov"), ("/fr/brokers/", "agents immobiliers agréés"),
               ("/fr/property-value-estimator/", "estimer la valeur d'un appartement")],
        "ru": [("/ru/new-projects/", "новостройки в Израиле"), ("/projects/hamedina-ru/", "башни Кикар ха-Медина"),
               ("/projects/rainbow-tel-aviv-ru/", "Rainbow в Сде-Дов"), ("/ru/brokers/", "лицензированные маклеры"),
               ("/ru/property-value-estimator/", "оценка стоимости квартиры")],
        "ar": [("/ar/new-projects/", "مشاريع جديدة"), ("/projects/hamedina-ar/", "أبراج كيكار همدينا"),
               ("/projects/rainbow-tel-aviv-ar/", "مشروع Rainbow في سدي دوف")],
    }
    pages = {}
    for page in ("hub", "rova-4"):
        pages[page] = {"he": [dict(x, role="source") for x in he_links[page]]}
        for l in LANGS:
            lst = []
            for x in he_links[page]:
                u = x["url"]
                tgt = eq.get(u, {}).get(l)
                lang_page = SITE + "/%s%s" % (l, u[len(SITE):])
                if tgt:
                    lst.append({"url": tgt, "maps_from": u, "target_language": l if "hamedina" in tgt else "en",
                                "status": st(tgt), "role": "mirror (same-topic page in this language)"})
                else:
                    lst.append({"url": u, "maps_from": u, "target_language": "he", "status": st(u),
                                "language_version": lang_page, "language_version_status": st(lang_page),
                                "role": "mirror (no %s version yet: link the Hebrew page and say so)" % l})
            for path, anchor in extras[l]:
                if not any(y["url"] == SITE + path for y in lst):
                    lst.append({"url": SITE + path, "anchor_suggestion": anchor, "target_language": l, "status": st(SITE + path),
                                "role": "optional extra (at most 3 in the article)"})
            pages[page][l] = lst
    for page in pages:
        for l in pages[page]:
            for x in pages[page][l]:
                assert x["status"] == 200, (page, l, x)
    doc = {"checked_utc": lc["checked_utc"], "method": "GET without following redirects, UA 'nad-lan.co.il i18n link check "
           "(HAD-460)', one request per 0.4 s; every URL below answered 200. The language versions /<lang>/<path>/ of the "
           "Hebrew targets answered 404 (none exists yet), so those links stay Hebrew.", "pages": pages,
           "swap_after_publish": {"rule": "When /<lang>/north-tel-aviv/ and /<lang>/north-tel-aviv/rova-4/ are both live, "
                                          "point the hub <-> Rova 4 links of that language to each other (and add them here).",
                                  "hub": {l: [HE_URL["rova-4"], TARGET["rova-4"][l]] for l in LANGS},
                                  "rova-4": {l: [HE_URL["hub"], TARGET["hub"][l]] for l in LANGS}}}
    io.open(os.path.join(HERE, "links.json"), "w", encoding="utf-8").write(json.dumps(doc, ensure_ascii=False, indent=1) + "\n")
    return doc


def build_live_headings():
    out = {"retrieved_utc": datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S"), "pages": {}}
    urls = sorted(set(u for l in CT.COMPARATORS for u in CT.COMPARATORS[l]) | set(CT.PAIR.values()))
    for u in urls:
        try:
            stc, body = CT.fetch(SITE + u)
        except Exception as e:
            stc, body = str(e), ""
        out["pages"][u] = {"status": stc, **(CT.page_headings(body) if stc == 200 else {"title": [], "h1": [], "h2": []})}
        time.sleep(0.4)
    io.open(os.path.join(HERE, "live-headings.json"), "w", encoding="utf-8").write(json.dumps(out, ensure_ascii=False, indent=1) + "\n")
    return out


# ============================================================== packet + prompt
HTML_CONTRACT = """\
- Output HTML only. Allowed tags: h1, h2, h3, p, ul, ol, li, table, thead, tbody, tr, th, td, a, b. No div, no span, no
  inline style, no br, no images, no scripts, no comments, no emoji, no shortcodes (the site inserts its own components).
- Exactly ONE <h1>, first, with the H1 given below. Then the sections in the order of the outline. Each section opens with its
  <h2> (the suggested heading, or a better one in the same order that keeps its keywords and does not start with the same 4
  words as another page of the site: the "avoid" list). H3s exactly where the Hebrew has them.
- Tables: one table wherever the Hebrew has one, same columns, same rows, same order, every number identical:
  <table><thead><tr><th>..</th></tr></thead><tbody><tr><td>..</td></tr></tbody></table>. Translate labels and words in cells.
- FAQ: <h2>FAQ_H2</h2> then, for each question in order, <h3>question</h3><p>answer</p> (one paragraph, the first sentence
  answers directly, the same facts and numbers as the Hebrew answer).
- Links: <a href="FULL_URL">anchor in the article's language</a>, only URLs from internal_links, each where the Hebrew has its
  link. A link to a Hebrew page carries IN_HEBREW after the anchor, outside the <a>. At most 3 optional extras. No external link.
- Do NOT write: the site disclaimer or an "updated" line (the site adds it), a list of sources, the multilingual keyword line
  that closes the Hebrew hub, a table of contents.
- No em dash (—) and no en dash (–), also not in ranges."""

PROMPT = """\
You are a senior {lang_name}-language real-estate writer who lives in Tel Aviv and writes for {lang_name}-speaking buyers. Your task:
write the {lang_name} version of a live Hebrew page of nad-lan.co.il, an Israeli real-estate portal: {page_name}.
Target URL: {target}. Hebrew source: {source_url}.

This is a CULTURAL REWRITE, not a word-for-word translation (the owner's rule): the {lang_name} reader must feel the page was
written for them (a buyer from abroad, an investor, a new immigrant). But the content is the Hebrew page's content: the same
H1/H2 order, the same tables, the same facts, and the same numbers, ONE TO ONE.

## Hard rules
1. Numbers: every number, price, date, size, count and percentage must appear exactly as in the Hebrew source (locale formatting
   is fine: {typo_short}). Never add a number, price, direction, view or facility the Hebrew does not have; never round
   (6,835,800 stays 6,835,800, not "6.8 million"); never convert currency or units. Each message gives the claims of its part
   (claims_for_part_1 in the packet, then one list in each later message) with every allowed number and its meaning: if a
   number is not there, it may not appear in that part. The SEO title and description may use any claim already given. Every
   number you write is checked by a script.
2. No source names in the text (no newspapers, websites, Wikipedia, "according to X"); dates carry the evidence.
3. Marketing language of an Israeli real-estate site, warm and concrete; no tech or demo talk. Banned: {banned}
4. No self-disclaimers, no pile of caveats, no "red flags" chapter.
5. Do not research. Your only material is this message: the packet (JSON) and the Hebrew source below.

## The reader
{audience}
{culture}

## Names (use exactly)
{names}

## What {lang_name} speakers search (Google, monthly searches; DataForSEO, 7.10.2026)
{keywords}
{related}
Use the words people type in the H1, the first paragraph and the H2s where natural; never stuff.

## Structure and length
Mirror the Hebrew: {n_h2} H2 sections in this order (outline in the packet: suggested H2, word budget, the claims each section
must use). Length close to the Hebrew: about {target_words} words in all ({lo} to {hi}), each section within about 15% of its
budget. {length_note}

## The HTML contract
{contract}
(FAQ_H2 = "{faq_h2}", IN_HEBREW = "{in_hebrew}", H1 = "{h1}")

## Typography and units
{typography}
{units}

## How to return the page (important)
The page comes in {n_parts} parts. Each part is ONE ```html code block with nothing before or after it.
{parts_plan}
After the last part, in the SAME answer, add one ```text block with exactly three lines:
title: <SEO title>
description: <SEO description>
url: {target}
SEO: {seo}

## The packet
```json
{packet}
```
"""


def build(page, lang, he_secs, links_doc, comps):
    d = L[lang]
    secs = SECTIONS[page]
    outline, parts = [], {}
    total_he = 0
    for k, (sid, h2he, part, must) in enumerate(secs):
        sh = he_secs[sid]
        w, tw = words(sh), table_words(sh)
        total_he += w
        budget = int(round(w * FACTOR[lang] / 10.0) * 10)
        item = {"id": sid, "part": part, "hebrew_h2": h2he, "h2": d["h2"][page][k], "hebrew_words": w,
                "hebrew_table_words": tw, "words": budget, "must_use": must}
        if sid == "hub-anchors":
            item["h3"] = d["h3_hub"]
        if sid.endswith("faq"):
            item["faq_questions"] = d["faq"][page]
        if sid == "r4-lead":
            item["note"] = ("The lead: the H1, then the lead paragraph (<p class=\"lede\">) and the 'in numbers' paragraph, no H2. "
                            "The site inserts its price list and its area map right after these two paragraphs: do not write "
                            "them, and do not mention them as technology.")
        if sid == "hub-opening":
            item["note"] = ("The opening: <h2>, two paragraphs, then <p class=\"nl-cta\"> with the two links of the Hebrew, then "
                            "<ul class=\"nl-cards\"> with the three cards as <li><b>title</b> text</li>, then <p class=\"nl-note\">, "
                            "then the bridging paragraph. Write a real H2 (the Hebrew one is just 'Opening').")
        outline.append(item)
        parts.setdefault(part, []).append(sid)
    target_words = int(round(total_he * FACTOR[lang] / 10.0) * 10)
    lo, hi = int(target_words * 0.85), int(target_words * 1.2)
    claims = [c for c in CLAIMS if c["page"] in (page, "both")]
    avoid = sorted(set(CT.key4(t) for u, x in comps.items() if x.get("status") == 200 for k in ("title", "h1", "h2")
                       for t in x.get(k, []) if t and not re.search(r"[א-ת]", t)))
    not_pub = {"hub": ["rents and rental yields in each neighborhood", "management fees of specific buildings",
                       "a delivery date for the Sde Dov quarter", "per-m2 prices for neighborhoods other than those given"],
               "rova-4": ["the 5-room median of the southern part in Q1 2026", "the floor of the Remez 27 penthouses",
                          "the developers of Remez 27 and Zlotzisti 4", "the 'before' state of Remez 44, 22, 25 and 42 and of "
                          "Henkin 3", "rents and yields in Rova 4", "school catchment areas"]}[page]
    page_name = {"hub": "North Tel Aviv, the area guide (the hub page of the north of the city: Ramat Aviv, Neve Avivim, Shikun "
                        "Lamed, the Old North, Bavli, Sde Dov, the Einstein Street projects, prices, transport, legal points)",
                 "rova-4": "Rova 4 (the New North): Tel Aviv's 4th quarter around Kikar HaMedina: boundaries, neighborhoods, "
                           "the Rova 4 plan, official prices and deals, urban renewal projects, transport"}[page]
    packet = {
        "page": page, "language": lang, "target_url": TARGET[page][lang], "hebrew_url": HE_URL[page], "h1": d["h1"][page],
        "faq_h2": d["faq_h2"], "words_target": target_words, "words_total_range": [lo, hi], "hebrew_words": total_he,
        "h2_count": sum(1 for s in secs if s[1] is not None), "outline": outline, "names": d["names"],
        "keywords_monthly": d["keywords"], "serp": d["related"], "audience": d["audience"], "culture": d["culture"],
        "typography": d["typography"], "units": d["units"], "banned": d["banned"], "in_hebrew_marker": d["in_hebrew"],
        "internal_links": links_doc["pages"][page][lang], "avoid_headings_first_4_words": avoid,
        "not_published": not_pub, "seo_request": d["seo"],
        "claims": [{k: c[k] for k in ("claim_id", "topic", "claim", "numbers", "date", "conflict", "write_as") if c[k]}
                   for c in claims],
        "sources_note": "Sources stay in the repo (claims.json source field, align-check.md, rova-4 facts.md); never in the text.",
    }
    os.makedirs(os.path.join(HERE, "packets"), exist_ok=True)
    io.open(os.path.join(HERE, "packets", "%s-%s.json" % (page, lang)), "w", encoding="utf-8").write(
        json.dumps(packet, ensure_ascii=False, indent=1) + "\n")
    # ---- the prompt, one message per output part
    kw = "\n".join("- %s: %s" % (k, v) for k, v in d["keywords"])
    typo_short = {"en": "6,835,800 / 30.7%", "fr": "6 835 800 / 30,7 %", "ru": "6 835 800 / 30,7%",
                  "ar": "6,835,800 / 30.7% (Western digits)"}[lang]
    plan = []
    for p in sorted(parts):
        plan.append("- Part %d (%s): %s." % (p, "now, with message 1" if p == 1 else "when I send message %d" % p,
                                             ", ".join("%s (%s)" % (s, next(o["h2"] or "lead" for o in outline if o["id"] == s))
                                                       for s in parts[p])))
    length_note = ("The Hebrew counts %d words (tables included); %s runs about %d%% of the Hebrew word count for the same "
                   "content." % (total_he, LANG_NAME[lang], int(FACTOR[lang] * 100)))
    # the prompt carries only what the text above does not already say (the full packet stays in packets/<page>-<lang>.json)
    def part_claims(p):
        ids = []
        for o in outline:
            if o["part"] == p:
                ids += [i for i in o["must_use"] if i not in ids]
        ids += [c["claim_id"] for c in claims if c["page"] == "both" and c["claim_id"] not in ids]
        return [x for x in packet["claims"] if x["claim_id"] in ids]
    lean = {"h1": packet["h1"], "target_url": packet["target_url"], "faq_h2": packet["faq_h2"],
            "outline": packet["outline"], "claims_for_part_1": part_claims(1),
            "internal_links": [{k: x[k] for k in ("url", "maps_from", "target_language", "anchor_suggestion") if k in x}
                               for x in packet["internal_links"]],
            "avoid_headings_first_4_words": packet["avoid_headings_first_4_words"], "not_published": packet["not_published"]}
    compact = json.dumps(lean, ensure_ascii=False, separators=(",", ":"))
    head = PROMPT.format(lang_name=LANG_NAME[lang], page_name=page_name, target=TARGET[page][lang], source_url=HE_URL[page],
                         typo_short=typo_short, banned=d["banned"], audience=d["audience"], culture=d["culture"],
                         names=d["names"], keywords=kw, related=d["related"], n_h2=packet["h2_count"],
                         target_words=target_words, lo=lo, hi=hi, length_note=length_note,
                         contract=HTML_CONTRACT, faq_h2=d["faq_h2"], in_hebrew=d["in_hebrew"], h1=d["h1"][page],
                         typography=d["typography"], units=d["units"], n_parts=len(parts), parts_plan="\n".join(plan),
                         seo=d["seo"], packet=compact)
    msgs = []
    for p in sorted(parts):
        src = "\n\n".join("<!-- %s -->\n%s" % (s, he_secs[s]) for s in parts[p])
        if p == 1:
            body = head + "\n## The Hebrew source, part 1 (sections %s)\n```html\n%s\n```\n\nWrite part 1 now." % (
                ", ".join(parts[p]), src)
        else:
            body = ("Continue with part %d of the same page, same rules and packet. The claims this part may use (every number "
                    "you write in it must be in them):\n```json\n%s\n```\nThe Hebrew source, part %d (sections %s):\n"
                    "```html\n%s\n```\n\nWrite part %d now%s." % (
                        p, json.dumps(part_claims(p), ensure_ascii=False, separators=(",", ":")), p, ", ".join(parts[p]),
                        src, p, ", then the ```text block with title, description and url" if p == max(parts) else ""))
        msgs.append(body)
    sizes = [len(m) for m in msgs]
    md = ["# Prompt: %s, %s (HAD-460 Stage A)\n" % (page, LANG_NAME[lang]),
          "Built by build_packets.py on %s UTC from claims.json (%d claims for this page), links.json (every link GET 200 on "
          "7.10.2026) and the live Hebrew page (hub with align-edits.json applied). Paste each message into ONE new ChatGPT "
          "conversation in order (message 1 now; message 2 after part 1 arrives%s). Message sizes (characters): %s; each is "
          "under %d. Then run: python check_translation.py <joined parts>.html --page %s --lang %s --meta <text block>.txt\n"
          % (datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M"), len(claims),
             "; message 3 after part 2" if len(msgs) > 2 else "", ", ".join("%d" % s for s in sizes), MAX_MSG, page, lang)]
    for k, m in enumerate(msgs, 1):
        md.append("\n---\n\n## Message %d of %d\n\n%s" % (k, len(msgs), m))
    io.open(os.path.join(HERE, "packets", "prompt-%s-%s.md" % (page, lang)), "w", encoding="utf-8").write("\n".join(md) + "\n")
    assert max(sizes) < MAX_MSG, (page, lang, sizes)
    # own headings vs live pages (first 4 words)
    own = [("h1", d["h1"][page])] + [("h2", o["h2"]) for o in outline if o["h2"]]
    dupes = CT.heading_dupes(own, lang, comps)
    return {"page": page, "lang": lang, "words_target": target_words, "range": [lo, hi], "hebrew_words": total_he,
            "parts": len(parts), "msg_sizes": sizes, "claims": len(claims), "links": len(links_doc["pages"][page][lang]),
            "dupes": dupes}


def main():
    links_doc = build_links()
    heads = build_live_headings()
    (hub_html, _), (rova_html, _) = CT.hebrew_sources()
    he = {"hub": split_sections("hub", clean_html(hub_html)), "rova-4": split_sections("rova-4", clean_html(rova_html))}
    for page in he:
        io.open(os.path.join(HERE, "source", "%s-he-clean.html" % page), "w", encoding="utf-8").write(
            "\n\n".join("<!-- %s -->\n%s" % (k, v) for k, v in he[page].items()) + "\n")
    rows = []
    for page in ("hub", "rova-4"):
        for lang in LANGS:
            comps = {u: x for u, x in heads["pages"].items() if u in CT.COMPARATORS[lang]}
            r = build(page, lang, he[page], links_doc, comps)
            rows.append(r)
            print("%-6s %s | Hebrew %d words -> target %d (%d-%d) | parts %d, message chars %s | claims %d | links %d | "
                  "heading dupes %d" % (page, lang, r["hebrew_words"], r["words_target"], r["range"][0], r["range"][1],
                                        r["parts"], r["msg_sizes"], r["claims"], r["links"], len(r["dupes"])))
            for x in r["dupes"]:
                print("    DUPLICATE", x)
    io.open(os.path.join(HERE, "packets", "build-summary.json"), "w", encoding="utf-8").write(
        json.dumps(rows, ensure_ascii=False, indent=1) + "\n")


if __name__ == "__main__":
    main()
