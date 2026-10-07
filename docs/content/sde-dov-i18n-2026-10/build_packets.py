# -*- coding: utf-8 -*-
"""HAD-439 Stage A: packets and ChatGPT prompts for the language versions of the Sde Dov hub (/sde-dov/) and the Sde Dov
prices page (/sde-dov/prices/). Modelled on docs/content/north-tel-aviv-2026-10/build_packets.py.

    python docs/content/sde-dov-i18n-2026-10/linkcheck.py       (first: GET status of every candidate link)
    python docs/content/sde-dov-i18n-2026-10/claims.py          (claims.json)
    python docs/content/sde-dov-i18n-2026-10/build_packets.py   (this file)

Writes packets/<page>-<lang>.json and packets/prompt-<page>-<lang>.md for page in (sde-dov-hub, sde-dov-prices) and lang in
(en, fr, ru, ar), plus links.json (internal links per page and language, from source/linkcheck-20261007.json), live-headings.json
(the title, H1 and H2s of the other live pages in each language, for the duplicate check) and source/<page>-he-clean.html (the
Hebrew each prompt carries).

These are CULTURAL REWRITES of two live Hebrew pages, not new articles: ChatGPT gets the Hebrew source section by section and
must keep its H1/H2 order, its tables and its numbers one to one (docs/content/rova-4-2026-10/i18n-brief.md); word budgets
follow the Hebrew length. The site's components are NOT written: the writer puts the exact marker (<!-- NLAM --> on the hub,
<!-- NLPG --> on the prices page) where the Hebrew page has the component, and the publish step swaps it for the shortcode.
"""
import datetime, io, json, os, re, sys, time

sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import check_translation as CT  # noqa: E402

CLAIMS = json.load(io.open(os.path.join(HERE, "claims.json"), encoding="utf-8"))
SITE = "https://nad-lan.co.il"
LANGS = ("en", "fr", "ru", "ar")
LANG_NAME = {"en": "English", "fr": "French", "ru": "Russian", "ar": "Arabic"}
FACTOR = {"en": 1.2, "fr": 1.3, "ru": 1.0, "ar": 1.0}   # words in the language per Hebrew word (Hebrew glues prepositions)
MAX_MSG = 40000                                            # characters per pasted message
LINK_CHECK = os.path.join(HERE, "source", "linkcheck-20261007.json")
PAGE_IDS = ("sde-dov-hub", "sde-dov-prices")

# ============================================================== the two pages: sections in Hebrew order
# (id, Hebrew H2, output part, claims the section must use)
SECTIONS = {
    "sde-dov-hub": [
        ("hub-what", "מה זה רובע שדה דב", 1, ["SD-01"]),
        ("hub-history", "ההיסטוריה: משדה התעופה דב הוז לרובע החדש", 1, ["SDH-01"]),
        ("hub-land", "הקרקע והמיקום: כ-1,300 דונם על חוף צפון תל אביב", 1, ["SDH-02", "SDH-03"]),
        ("hub-plan", "תוכנית המתאר: 16,000 דירות ל-40,000 תושבים", 1, ["SDH-04", "SDH-05", "SD-01"]),
        ("hub-compounds", "שלושת המתחמים: אשכול, מרכז הרובע, צפון הרובע", 1, ["SDH-06", "SDH-08", "SD-01"]),
        ("hub-projects", "הפרויקטים בשיווק ברובע", 2, ["SDH-09", "SDH-10"]),
        ("hub-developers", "היזמים: מי בונה בשדה דב", 2, []),
        ("hub-prices", "מחירים: כמה עולה דירה בשדה דב", 2,
         ["SD-02", "SD-03", "SD-04", "SDH-11", "SDH-12", "SDH-13", "SDH-14", "SD-05"]),
        ("hub-transport", "תחבורה, פארקים, חופים ומבני ציבור", 2, ["SDH-05"]),
        ("hub-affordable", "דיור בר-השגה ודיור מיוחד", 3, ["SDH-05", "SD-01"]),
        ("hub-invest", "השקעה בשדה דב: יתרונות, סיכונים ומה לבדוק", 3, ["SD-02", "SD-03", "SDH-09"]),
        ("hub-legal", "בדיקות משפטיות לפני רכישה על הנייר בשדה דב", 3, []),
        ("hub-faq", "שאלות נפוצות", 3,
         ["SDH-02", "SDH-03", "SD-01", "SDH-04", "SDH-09", "SD-02", "SD-03", "SDH-12", "SDH-06", "SDH-05"]),
        ("hub-summary", "סיכום קצר", 4, ["SD-01", "SDH-04"]),
        ("hub-planning", "תכנון הרובע: מהתכנית אל העיר החדשה", 4, ["SDH-07", "SD-01", "SDH-15", "SDH-16"]),
        ("hub-guide", "מדריך הרובע: מתחמים, נתונים ותשתיות", 4, []),
        ("hub-links", "פרויקטים, כלים וליווי בשדה דב", 4, []),
    ],
    "sde-dov-prices": [
        ("pr-lead", "מחירי דירות בשדה דב: תמונת שוק עדכנית", 1, ["SD-02", "SD-03", "SDP-01", "SDP-02"]),
        ("pr-m2", "מחיר למ״ר ברובע שדה דב", 1,
         ["SD-02", "SDP-04", "SDP-03", "SDP-05", "SDP-06", "SD-03", "SDP-07", "SDP-01", "SDP-08", "SDP-02"]),
        ("pr-gaps", "מה מסביר את פערי המחירים בתוך הרובע", 1, ["SDP-13", "SDP-12"]),
        ("pr-rooms", "מחירים לפי גודל דירה", 1,
         ["SD-02", "SDP-09", "SDP-10", "SDP-11", "SDP-02", "SDP-12", "SDP-13", "SD-05"]),
        ("pr-compounds", "מחירים לפי מתחם", 1, ["SD-01", "SD-02", "SD-04", "SDP-15", "SDP-16"]),
        ("pr-sea", "פרמיית קו ראשון לים ונוף", 2, ["SDP-08", "SDP-01", "SD-03", "SDP-07", "SDP-02", "SD-02"]),
        ("pr-records", "עסקאות שיא ועסקאות שפל", 2, ["SDP-09", "SDP-14", "SD-05", "SD-02"]),
        ("pr-compare", "השוואת מחירים מול שכונות יוקרה בתל אביב", 2, ["SDP-04", "SDP-17", "SD-02", "SD-03"]),
        ("pr-presale", "דינמיקת פריסייל מול אכלוס", 2, ["SD-03", "SDP-07", "SDP-05", "SD-01"]),
        ("pr-finance", "מימון, לוח תשלומים וליווי בנקאי", 2, ["SD-02"]),
        ("pr-legal", "הזווית המשפטית והמיסויית", 3, ["SDP-13"]),
        ("pr-forecast", "תחזית והערכת שווי עתידי", 3, ["SD-01", "SD-02", "SDP-18", "SDP-13", "SDP-19"]),
        ("pr-offer", "איך לקרוא הצעת מחיר בשדה דב", 3, ["SDP-15", "SDP-19", "SD-03", "SD-02", "SDP-08"]),
        ("pr-investors", "משמעות המחירים למשקיעים", 3, ["SDP-13"]),
        ("pr-faq", "שאלות נפוצות", 3,
         ["SD-02", "SDP-13", "SDP-10", "SD-03", "SDP-02", "SDP-08", "SDP-01", "SDP-17", "SDP-18"]),
        ("pr-abroad", "משקיעים זרים ומילות חיפוש בינלאומיות", 3, []),
    ],
}
HE_URL = {p: SITE + CT.PAGES[p]["he_path"] for p in PAGE_IDS}
TARGET = {p: {l: SITE + CT.PAGES[p]["target"].format(lang=l) for l in LANGS} for p in PAGE_IDS}
OTHER = {"sde-dov-hub": "sde-dov-prices", "sde-dov-prices": "sde-dov-hub"}

# ============================================================== per language: H1, H2s, FAQ, names, SERP, culture
HUB_H3_PROJECTS = ["Rainbow Tel Aviv", "FIRST BY HAGAG", "ASHIRA BY AVISROR", "DIMRI YAMA", "ZOHI", "GINDI VOGUE", "UTOPIA"]
L = {
    "en": {
        "h1": {"sde-dov-hub": "Sde Dov, Tel Aviv: New Projects and Apartments for Sale",
               "sde-dov-prices": "Sde Dov Apartment Prices: Price per m², Deals and Comparisons"},
        "h2": {"sde-dov-hub": ["What Sde Dov is: Tel Aviv's new seafront quarter",
                               "History: from Dov Hoz airfield to a new quarter",
                               "Land and location: about 1,300 dunam on the north Tel Aviv coast",
                               "The master plan: 16,000 apartments for 40,000 residents",
                               "Three compounds: Eshkol, the Centre and the North",
                               "Projects on sale in Sde Dov", "The developers building in Sde Dov",
                               "Prices: how much an apartment in Sde Dov costs",
                               "Transport, parks, beaches and public buildings",
                               "Affordable and special housing in Sde Dov",
                               "Investing in Sde Dov: advantages, risks and what to check",
                               "Legal checks before buying off plan in Sde Dov", "Frequently asked questions",
                               "Sde Dov in short", "Planning the quarter: from plan to new city district",
                               "Guides to the quarter: compounds, data and infrastructure",
                               "Projects, tools and professional support in Sde Dov"],
               "sde-dov-prices": ["Sde Dov prices today: the market at a glance", "Price per m² in Sde Dov",
                                  "Why prices differ inside the quarter", "Prices by apartment size", "Prices by compound",
                                  "The sea-view and front-line premium", "Record deals and entry-level deals",
                                  "How Sde Dov compares with Tel Aviv's luxury neighborhoods", "Presale or near occupancy",
                                  "Financing, the payment schedule and bank supervision", "The legal and tax angle",
                                  "Forecast and future value", "How to read a price offer in Sde Dov",
                                  "What the prices mean for investors", "Frequently asked questions",
                                  "Buying in Sde Dov from abroad"]},
        "h3_planning": ["The plan builds a quarter, not a cluster of towers", "A coastal park is a system, not a strip of lawn",
                        "Infrastructure before apartments: the right order, and hard to coordinate",
                        "Public transport, walking and cycling will set the quality of life",
                        "How to check an apartment in a quarter under construction",
                        "What to check in the official documents",
                        "Public participation: how residents' comments enter the plan"],
        "faq": {"sde-dov-hub": ["Where is the Sde Dov quarter?", "How many apartments are planned in Sde Dov?",
                                "When will people move into Sde Dov?", "How much does an apartment in Sde Dov cost?",
                                "What is the Eshkol compound in Sde Dov?", "Who are the main developers in Sde Dov?",
                                "Is Sde Dov a good investment?", "Is there affordable housing in Sde Dov?",
                                "What should you check before signing for an apartment in Sde Dov?",
                                "Will management fees in Sde Dov be high?"],
                "sde-dov-prices": ["How much does an apartment in Sde Dov cost?", "What is the price per m² in Sde Dov?",
                                   "Is Sde Dov more expensive than Ramat Aviv?", "Is it worth buying in presale?",
                                   "What should you check legally before signing?",
                                   "Can prices reach ₪150,000 per m²?"]},
        "faq_h2": "Frequently asked questions",
        "names": "Sde Dov (שדה דב); the quarter: \"the Sde Dov quarter\" (rova = quarter; the site's own name for it: \"Sde Dov "
                 "quarter\"). Dov Hoz airport. The compounds: Eshkol (מתחם אשכול, the Eshkol compound), the Centre (מרכז הרובע), "
                 "the North (צפון הרובע). Projects as the developers write them: Rainbow Tel Aviv (Israel Canada), FIRST or "
                 "FIRST BY HAGAG (Hagag Group), ASHIRA (Avisror Moshe & Sons), DIMRI YAMA (Y.H. Dimri; architect Rani Ziss, "
                 "interiors Kelly Hoppen), ZOHI (Levinstein, Mivne and Allied), GINDI VOGUE (Gindi Holdings), UTOPIA (Nahmias "
                 "Group). Developers: Israel Canada, Hagag Group, Avisror Moshe & Sons, Y.H. Dimri, Gindi Holdings, Shikun & "
                 "Binui, Mor Group, Nahmias Group, Levinstein Group, Allied, Mivne, Africa Israel, Electra. Contractor: Ashtrom. "
                 "Places: Tzukei Aviv, Propes Street, Neve Yam, Program L (Tochnit Lamed), Levi Eshkol Street, Kochav HaTzafon, "
                 "the Reading compound, Shai Agnon Street, Yarkon Park, Ibn Gabirol, Ramat Aviv, Ramat Aviv Gimel, Park Tzameret, "
                 "the Green Line of the light rail. Bodies: the Israel Land Authority, the Tel Aviv District Planning Committee, "
                 "the Tel Aviv-Yafo Local Planning Committee, the Tel Aviv-Yafo municipality. Laws: the Sale (Apartments) Law; "
                 "the Sale (Apartments) (Assurance of Investments of Purchasers of Apartments) Law, \"the Sale Law guarantee\". "
                 "Terms: purchase tax, betterment levy, management fees (building maintenance and services), bank supervision "
                 "account (liva'i bank'ai), presale. Rooms: the Israeli count (\"4 rooms\"). Tel Aviv-Yafo for the municipality.",
        "keywords": [("sde dov (US)", 320), ("sde dov tel aviv (US)", 320), ("sde dov (Israel, English)", 390),
                     ("sde dov tel aviv (Israel, English)", 390), ("rainbow tel aviv (Israel, English)", 170),
                     ("sde dov project (Israel, English)", 20), ("sde dov apartments for sale (US)", 10),
                     ("tel aviv real estate (US, 7.10 morning)", 480), ("tel aviv apartments for sale (US)", 390),
                     ("buy apartment in tel aviv (US)", 390), ("ramat aviv (US)", 390), ("luxury apartments tel aviv (US)", 50),
                     ("tel aviv real estate prices (US)", 20),
                     ("sde dov apartments / sde dov prices / sde dov real estate / sde dov neighborhood", "no volume data")],
        "related": "Google US, \"sde dov\" (7.10.2026): AI overview SHOWN: the airport closed in mid-2019 for a waterfront "
                   "redevelopment; \"1,500 to 1,600 dunams\" (from a marketing site: NOT our number, the official plan is about "
                   "1,300), \"16,000 housing units\", \"over one kilometer of coastline\", Green Line stations, Eshkol permits, "
                   "and PFAS soil contamination reports (not on our Hebrew page: do not add). Organic: a developer FAQ site, "
                   "listing posts, a rental tower on lot 109, a news item on the contamination. The searcher wants: what Sde Dov "
                   "is, what is being built, prices, can I buy there.",
        "audience": "International buyers (US, UK, Canada, Australia, South Africa, France's English readers) and English-speaking "
                    "Israelis and olim. They compare in shekels, often buy from abroad, and need Israeli terms decoded once "
                    "(rooms, presale, the Sale Law guarantee, purchase tax, management fees).",
        "culture": "US spelling (neighborhood) because that is how the searches are typed. Decode the Israeli room count once. Warm, "
                   "confident and factual: a premium seafront real-estate guide, not a warning leaflet. Where the Hebrew speaks "
                   "to Israeli families, keep it, and add the foreign buyer's angle in words (no new numbers): managing from "
                   "abroad, a lawyer with a power of attorney, buying does not give residency.",
        "typography": "Dates as 12 March 2020 or March 2020, or keep the Hebrew style 4.2026 in tables; ₪ before the number "
                      "(₪83,000; ₪9.45 million); ranges with \"to\"; no em dash (—) and no en dash (–).",
        "units": "m² and ₪ only. No square feet, acres, dollars or euros. A dunam may be explained once (1 dunam = 1,000 m²).",
        "banned": "interface · demo · model (as 3D) · hotspot · overlay · engine · layer · tile · prototype · simulation · "
                  "technology · \"the system\" · \"the platform\" · digital experience · 3D · Atlas · coming soon · \"free "
                  "advice\" (only the site's floating bar says it) · any source or media name (Wikipedia, Globes, Calcalist, "
                  "TheMarker, Ynet, Maariv, Bizportal, Madlan, Yad2, Psagot) · delve · nestled · boasts · a testament to · red "
                  "flag · beware · it is important to note · in conclusion",
        "in_hebrew": "(in Hebrew)",
        "seo": "SEO title in English, at most 60 characters, containing \"Sde Dov\" (hub: with \"Tel Aviv\"; prices page: with "
               "\"prices\"). Description in English, at most 155 characters.",
    },
    "fr": {
        "h1": {"sde-dov-hub": "Sde Dov à Tel Aviv : programmes neufs et appartements à vendre",
               "sde-dov-prices": "Prix des appartements à Sde Dov : prix au m², transactions et comparaisons"},
        "h2": {"sde-dov-hub": ["Sde Dov, le nouveau quartier de Tel Aviv face à la mer",
                               "Histoire : de l'aéroport Dov Hoz à un nouveau quartier",
                               "Terrain et situation : environ 1 300 dounams sur le littoral nord",
                               "Le plan directeur : 16 000 logements pour 40 000 habitants",
                               "Trois secteurs : Eshkol, le Centre et le Nord", "Les programmes en vente à Sde Dov",
                               "Les promoteurs qui construisent à Sde Dov",
                               "Prix : combien coûte un appartement à Sde Dov",
                               "Transports, parcs, plages et équipements publics",
                               "Logement abordable et logement spécifique",
                               "Investir à Sde Dov : atouts, risques et points à vérifier",
                               "Vérifications juridiques avant d'acheter sur plan", "Questions fréquentes",
                               "Sde Dov en résumé", "L'urbanisme du quartier : du plan à la ville nouvelle",
                               "Guides du quartier : secteurs, données et infrastructures",
                               "Programmes, outils et accompagnement à Sde Dov"],
               "sde-dov-prices": ["Les prix à Sde Dov aujourd'hui : l'essentiel", "Le prix au m² à Sde Dov",
                                  "Pourquoi les prix varient à l'intérieur du quartier", "Les prix selon la taille de l'appartement",
                                  "Les prix par secteur", "La prime vue mer et front de mer",
                                  "Transactions records et premiers prix",
                                  "Sde Dov face aux quartiers de luxe de Tel Aviv", "Acheter sur plan ou à la livraison",
                                  "Financement, échéancier et accompagnement bancaire", "L'angle juridique et fiscal",
                                  "Perspectives et valeur future", "Comment lire une offre de prix à Sde Dov",
                                  "Ce que les prix signifient pour les investisseurs", "Questions fréquentes",
                                  "Acheter à Sde Dov depuis l'étranger"]},
        "h3_planning": ["Le plan construit un quartier, pas un ensemble de tours", "Un parc littoral est un système, pas une pelouse",
                        "Les infrastructures avant les logements : le bon principe, difficile à coordonner",
                        "Transports publics, marche et vélo feront la qualité de vie",
                        "Comment vérifier un appartement dans un quartier en chantier",
                        "Ce qu'il faut vérifier dans les documents officiels",
                        "La concertation : comment les remarques des habitants entrent dans le plan"],
        "faq": {"sde-dov-hub": ["Où se trouve le quartier de Sde Dov ?", "Combien de logements sont prévus à Sde Dov ?",
                                "Quand les premiers habitants s'installeront-ils à Sde Dov ?",
                                "Combien coûte un appartement à Sde Dov ?", "Qu'est-ce que le secteur Eshkol à Sde Dov ?",
                                "Quels sont les principaux promoteurs à Sde Dov ?", "Faut-il investir à Sde Dov ?",
                                "Y a-t-il du logement abordable à Sde Dov ?",
                                "Que vérifier avant de signer pour un appartement à Sde Dov ?",
                                "Les charges de gestion seront-elles élevées à Sde Dov ?"],
                "sde-dov-prices": ["Combien coûte un appartement à Sde Dov ?", "Quel est le prix au m² à Sde Dov ?",
                                   "Sde Dov est-il plus cher que Ramat Aviv ?", "Faut-il acheter sur plan (en presale) ?",
                                   "Que vérifier juridiquement avant de signer ?",
                                   "Les prix peuvent-ils atteindre 150 000 ₪ le m² ?"]},
        "faq_h2": "Questions fréquentes",
        "names": "Sde Dov (שדה דב) ; « le quartier de Sde Dov » (nom du site : Quartier de Sde Dov). L'aéroport Dov Hoz. Les "
                 "secteurs : Eshkol (le secteur Eshkol), le Centre, le Nord. Programmes comme les promoteurs les écrivent : "
                 "Rainbow Tel Aviv (Israel Canada), FIRST (Hagag Group), ASHIRA (Avisror Moshe & Fils), DIMRI YAMA (Y.H. Dimri ; "
                 "architecte Rani Ziss, intérieurs Kelly Hoppen), ZOHI, GINDI VOGUE (Gindi Holdings), UTOPIA (groupe Nahmias). "
                 "Entreprise générale : Ashtrom. Lieux : Tzukei Aviv, rue Propes, Neve Yam, le quartier Lamed (Tochnit Lamed), "
                 "rue Levi Eshkol, Kochav HaTzafon, le site de Reading, rue Shai Agnon, le parc HaYarkon, Ibn Gabirol, Ramat Aviv, "
                 "Park Tzameret, la ligne verte du tramway (métro léger). Institutions : l'Autorité foncière d'Israël, la "
                 "commission de district de Tel Aviv, la commission locale de Tel Aviv-Jaffa, la municipalité de Tel Aviv-Jaffa. "
                 "Lois : la loi sur la vente (appartements) et sa garantie bancaire (« garantie loi Sale »). Termes : taxe "
                 "d'acquisition (mas rechisha), taxe de plus-value (hetel hashbaha), charges de gestion, vente sur plan "
                 "(presale), compte d'accompagnement bancaire. « 4 pièces » israélien = 4 pièces français.",
        "keywords": [("sde dov (France)", 110), ("sde dov tel aviv (France)", 110), ("immobilier tel aviv", 140),
                     ("appartement tel aviv", 140), ("acheter appartement tel aviv", 110), ("prix immobilier tel aviv", 50),
                     ("programme neuf tel aviv", 10), ("immobilier israel (30.9)", 320),
                     ("quartier sde dov / sde dov immobilier / appartement bord de mer tel aviv", "no volume data")],
        "related": "Google France, « sde dov tel aviv » (7.10.2026) : pas d'aperçu IA. Organique : un guide anglophone (Sde Dov, "
                   "« la plus grande transformation urbaine »), un cabinet d'avocats (« environ 1 300 dounams »), un article de "
                   "presse de 2022 (1 490 dounams, 41 000 habitants : PAS nos chiffres), des pages de promoteurs (FIRST, ASHIRA "
                   "« la future Riviera de Tel Aviv »). Vidéos courtes d'agents francophones (« le Monaco de Tel Aviv »). "
                   "Questions associées : Quel est le quartier le plus riche de Tel Aviv ? Quel est le prix moyen d'un logement "
                   "à Tel Aviv ? Annonce payante : FIRST.",
        "audience": "Acheteurs français et belges (alyah, pied-à-terre, investissement) et olim francophones déjà en Israël qui "
                    "montent en gamme. Ils achètent souvent à distance et comparent en shekels.",
        "culture": "Le vocabulaire du lecteur : quartier balnéaire, programme neuf, sur plan, front de mer, alyah, pied-à-terre. "
                   "Expliquer une fois le compte israélien des pièces et la garantie de la loi sur la vente. Montrer qu'on peut "
                   "tout préparer à distance (avocat avec procuration) sans ajouter de chiffre.",
        "typography": "Espace insécable avant : ; ? ! et entre milliers (83 000 ₪ ; 9,45 millions de ₪) ; virgule décimale ; "
                      "dates « 12 mars 2020 » ou 4.2026 dans les tableaux ; guillemets « » ; pas de tiret long (—) ni moyen (–).",
        "units": "m² et ₪ seulement. Pas d'euros, pas d'hectares en plus du dounam (1 dounam = 1 000 m², une seule fois).",
        "banned": "interface · démo · modèle (au sens 3D) · moteur · calque · prototype · simulation · technologie · « le "
                  "système » · « la plateforme » · expérience digitale · 3D · Atlas · bientôt · « conseil gratuit » · tout nom "
                  "de source ou de média (Wikipédia, Globes, Calcalist, Ynet, Psagot...) · il est important de noter · force est "
                  "de constater · en conclusion · véritable écrin · niché",
        "in_hebrew": "(en hébreu)",
        "seo": "Titre SEO en français, 60 caractères au plus, avec « Sde Dov » et « Tel Aviv » (hub) / « Sde Dov » et « prix » "
               "(page des prix). Description en français, 155 caractères au plus.",
    },
    "ru": {
        "h1": {"sde-dov-hub": "Сде-Дов в Тель-Авиве: новые проекты и квартиры на продажу",
               "sde-dov-prices": "Цены на квартиры в Сде-Дов: цена за м², сделки и сравнение"},
        "h2": {"sde-dov-hub": ["Что такое Сде-Дов: новый приморский район Тель-Авива",
                               "История: от аэропорта Дов Хоз к новому району",
                               "Земля и расположение: около 1 300 дунамов на северном побережье",
                               "Генеральный план: 16 000 квартир для 40 000 жителей",
                               "Три комплекса: Эшколь, Центр и Север", "Проекты в продаже в Сде-Дов",
                               "Застройщики: кто строит в Сде-Дов", "Цены: сколько стоит квартира в Сде-Дов",
                               "Транспорт, парки, пляжи и общественные здания",
                               "Доступное и специальное жильё", "Инвестиции в Сде-Дов: плюсы, риски и что проверить",
                               "Юридические проверки перед покупкой на этапе котлована", "Частые вопросы",
                               "Коротко о Сде-Дов", "Планирование района: от плана к новому городу",
                               "Путеводитель по району: комплексы, данные и инфраструктура",
                               "Проекты, инструменты и сопровождение в Сде-Дов"],
               "sde-dov-prices": ["Цены в Сде-Дов сегодня: картина рынка", "Цена за квадратный метр в Сде-Дов",
                                  "Почему цены внутри района так различаются", "Цены по размеру квартиры",
                                  "Цены по комплексам", "Надбавка за вид на море и первую линию",
                                  "Рекордные сделки и самые доступные сделки",
                                  "Сде-Дов и элитные районы Тель-Авива: сравнение", "Покупка на старте продаж или к заселению",
                                  "Финансирование, график платежей и банковское сопровождение",
                                  "Юридическая и налоговая сторона", "Прогноз и будущая стоимость",
                                  "Как читать ценовое предложение в Сде-Дов", "Что цены значат для инвесторов",
                                  "Частые вопросы", "Покупка в Сде-Дов из-за границы"]},
        "h3_planning": ["План строит район, а не набор башен", "Прибрежный парк: система, а не полоса газона",
                        "Инфраструктура раньше квартир: верный принцип, требующий координации",
                        "Общественный транспорт, пешие маршруты и велосипед определят качество жизни",
                        "Как проверить квартиру в районе, который ещё строится",
                        "Что проверить в официальных документах",
                        "Участие жителей: как замечания попадают в план"],
        "faq": {"sde-dov-hub": ["Где находится район Сде-Дов?", "Сколько квартир планируется в Сде-Дов?",
                                "Когда ожидается заселение в Сде-Дов?", "Сколько стоит квартира в Сде-Дов?",
                                "Что такое комплекс Эшколь в Сде-Дов?", "Кто основные застройщики в Сде-Дов?",
                                "Стоит ли инвестировать в Сде-Дов?", "Есть ли в Сде-Дов доступное жильё?",
                                "Что проверить перед подписанием договора на квартиру в Сде-Дов?",
                                "Будет ли высокой плата за управление (дмей ниуль) в Сде-Дов?"],
                "sde-dov-prices": ["Сколько стоит квартира в Сде-Дов?", "Какая цена за м² в Сде-Дов?",
                                   "Сде-Дов дороже Рамат-Авива?", "Стоит ли покупать на старте продаж?",
                                   "Что проверить юридически перед подписанием?",
                                   "Могут ли цены достичь 150 000 ₪ за м²?"]},
        "faq_h2": "Частые вопросы",
        "names": "Сде-Дов (שדה דב); «район Сде-Дов» (название сайта: Район Сде-Дов). Аэропорт Дов Хоз. Комплексы: Эшколь "
                 "(квартал Эшколь, как на карте сайта), Центр района, Север района. Проекты латиницей, как их пишут застройщики: "
                 "Rainbow Tel Aviv (Israel Canada), FIRST (Hagag Group), ASHIRA (Avisror Moshe & Sons), DIMRI YAMA (Y.H. Dimri; "
                 "архитектор Рани Зис, интерьеры Kelly Hoppen), ZOHI, GINDI VOGUE (Gindi Holdings), UTOPIA (Nahmias Group). "
                 "Генподрядчик Ashtrom. Места: Цукей-Авив, улица Пропес, Неве-Ям, район Ламед (Тохнит Ламед), улица Леви Эшколь, "
                 "Кохав ха-Цафон, комплекс Рединг, улица Шай Агнон, парк Яркон, Ибн Гвироль, Рамат-Авив (так ищут: «рамат авив», "
                 "880 в месяц), Рамат-Авив Гимель, Парк Цамерет, Зелёная линия легкорельсового трамвая. Органы: Земельное "
                 "управление Израиля (Рами), окружная комиссия Тель-Авива, местная комиссия Тель-Авива-Яффо, муниципалитет "
                 "Тель-Авива-Яффо. Законы: закон о продаже (квартир) и гарантия по закону о продаже. Термины: налог на покупку "
                 "(мас рехиша), налог на улучшение (hetel hashbaha), плата за управление (дмей ниуль), продажа на этапе "
                 "котлована (пресейл), счёт банковского сопровождения.",
        "keywords": [("сде дов (Israel, ru)", 20), ("купить квартиру в тель авиве", 50), ("квартиры в тель авиве", 20),
                     ("цены на квартиры в тель авиве", 10), ("недвижимость в тель авиве", 10), ("рамат авив (7.10 morning)", 880),
                     ("купить квартиру в израиле (30.9)", 140),
                     ("сде дов тель авив / сде дов квартиры / район сде дов / новостройки тель авив", "no volume data")],
        "related": "Russian SERP not run (volumes near zero; the Kikar HaMedina Russian research of 30.9.2026 found buying intent "
                   "around Israel and Tel Aviv far larger than any place name). Typical questions: сколько стоит квартира, "
                   "цена за метр, налог на покупку, ипотека для нерезидентов, когда заселение.",
        "audience": "Русскоязычные израильтяне (знают слова салон, маклер, мас рехиша) и покупатели из-за границы. Им важны цена, "
                    "цена квадратного метра, налоги, сроки и надёжность застройщика.",
        "culture": "Объяснить один раз израильский счёт комнат («4 комнаты: салон и три спальни») и гарантию по закону о продаже. "
                   "Тон уверенный и тёплый, без канцелярита. Покупка через адвоката по доверенности возможна, без новых цифр.",
        "typography": "Десятичная запятая (9,45 млн ₪), неразрывный пробел между тысячами (83 000 ₪), даты 12.03.2020 или «12 "
                      "марта 2020 года», кавычки «ёлочки»; без длинного (—) и среднего (–) тире: предложения строятся без тире.",
        "units": "м² и ₪. Без долларов и гектаров; дунам можно объяснить один раз (1 дунам = 1 000 м²).",
        "banned": "интерфейс · демо · модель (в смысле 3D) · движок · слой · прототип · симуляция · технология · «система» · "
                  "«платформа» · цифровой опыт · 3D · Атлас · скоро · «бесплатная консультация» · любые названия источников и "
                  "СМИ (Википедия, Globes, Calcalist, Ynet, Маарив, Psagot...) · стоит отметить · важно понимать · в заключение · "
                  "уникальный шанс",
        "in_hebrew": "(на иврите)",
        "seo": "SEO-заголовок по-русски, не длиннее 60 знаков, со словами «Сде-Дов» и «Тель-Авив» (хаб) / «Сде-Дов» и «цены» "
               "(страница цен). Описание по-русски, не длиннее 155 знаков.",
    },
    "ar": {
        "h1": {"sde-dov-hub": "Sde Dov, Tel Aviv: New Projects and Apartments for Sale",
               "sde-dov-prices": "Sde Dov Apartment Prices: Price per m², Deals and Comparisons"},
        "h2": {"sde-dov-hub": ["ما هو حي سديه دوف: الحي الساحلي الجديد في تل أبيب",
                               "التاريخ: من مطار دوف هوز إلى حي جديد",
                               "الأرض والموقع: نحو 1,300 دونم على الساحل الشمالي",
                               "المخطط الهيكلي: 16,000 شقة لـ 40,000 نسمة",
                               "ثلاثة مجمعات: أشكول والمركز والشمال", "المشاريع المعروضة للبيع في سديه دوف",
                               "المطوّرون: من يبني في سديه دوف", "الأسعار: كم يكلّف شراء شقة في سديه دوف",
                               "المواصلات والحدائق والشواطئ والمباني العامة",
                               "السكن الميسّر والسكن الخاص", "الاستثمار في سديه دوف: المزايا والمخاطر وما يجب فحصه",
                               "الفحوص القانونية قبل الشراء على الخارطة", "أسئلة شائعة",
                               "سديه دوف باختصار", "تخطيط الحي: من المخطط إلى مدينة جديدة",
                               "دليل الحي: المجمعات والمعطيات والبنى التحتية",
                               "مشاريع وأدوات ومرافقة مهنية في سديه دوف"],
               "sde-dov-prices": ["الأسعار في سديه دوف اليوم: صورة السوق", "سعر المتر المربع في سديه دوف",
                                  "لماذا تختلف الأسعار داخل الحي", "الأسعار حسب حجم الشقة", "الأسعار حسب المجمع",
                                  "علاوة إطلالة البحر والخط الأول", "الصفقات القياسية والصفقات الأرخص",
                                  "مقارنة سديه دوف بأحياء الفخامة في تل أبيب", "الشراء في مرحلة ما قبل البيع أو قرب الإسكان",
                                  "التمويل وجدول الدفعات والمرافقة البنكية", "الجانب القانوني والضريبي",
                                  "التوقعات والقيمة المستقبلية", "كيف تقرأ عرض سعر في سديه دوف",
                                  "ماذا تعني الأسعار للمستثمرين", "أسئلة شائعة", "الشراء في سديه دوف من خارج البلاد"]},
        "h3_planning": ["المخطط يبني حياً لا مجموعة أبراج", "الحديقة الساحلية منظومة متكاملة لا شريط عشب",
                        "البنى التحتية قبل الشقق: مبدأ صحيح يحتاج إلى تنسيق",
                        "المواصلات العامة والمشي والدراجات تحدّد جودة الحياة",
                        "كيف تفحص شقة في حي ما زال قيد البناء", "ما الذي يجب فحصه في الوثائق الرسمية",
                        "مشاركة الجمهور: كيف تدخل ملاحظات السكان إلى المخطط"],
        "faq": {"sde-dov-hub": ["أين يقع حي سديه دوف؟", "كم شقة مخطط بناؤها في سديه دوف؟", "متى يُتوقع الإسكان في سديه دوف؟",
                                "كم سعر الشقة في سديه دوف؟", "ما هو مجمع أشكول في سديه دوف؟",
                                "من هم أبرز المطوّرين في سديه دوف؟", "هل يستحق الاستثمار في سديه دوف؟",
                                "هل يوجد سكن ميسّر في سديه دوف؟", "ماذا يجب فحصه قبل التوقيع على شقة في سديه دوف؟",
                                "هل ستكون رسوم الإدارة في سديه دوف مرتفعة؟"],
                "sde-dov-prices": ["كم سعر الشقة في سديه دوف؟", "كم سعر المتر المربع في سديه دوف؟",
                                   "هل سديه دوف أغلى من رمات أفيف؟", "هل يستحق الشراء في مرحلة ما قبل البيع؟",
                                   "ماذا يجب فحصه قانونياً قبل التوقيع؟", "هل يمكن أن تصل الأسعار إلى 150,000 ₪ للمتر المربع؟"]},
        "faq_h2": "أسئلة شائعة",
        "names": "سديه دوف (שדה דב)؛ «حي سديه دوف» (اسم الموقع: حي سديه دوف). مطار دوف هوز. المجمعات: أشكول (منطقة أشكول، كما "
                 "في خريطة الموقع)، مركز الحي، شمال الحي. المشاريع بأسمائها اللاتينية كما يكتبها المطوّرون: Rainbow Tel Aviv "
                 "(Israel Canada)، FIRST (Hagag Group)، ASHIRA (Avisror Moshe & Sons)، DIMRI YAMA (Y.H. Dimri؛ المهندس رني زيس، "
                 "التصميم الداخلي Kelly Hoppen)، ZOHI، GINDI VOGUE (Gindi Holdings)، UTOPIA (Nahmias Group). المقاول الرئيسي "
                 "Ashtrom. الأماكن: تسوكي أفيف، شارع بروبس، نافيه يام، حي لامد (Tochnit Lamed)، شارع ليفي أشكول، كوخاف هتسافون، "
                 "مجمع ريدينغ، شارع شاي عجنون، حديقة اليركون، ابن جبيرول، رمات أفيف (هكذا يُبحث عنها)، بارك تسامرت، الخط "
                 "الأخضر للقطار الخفيف. الجهات: سلطة أراضي إسرائيل، اللجنة اللوائية في تل أبيب، اللجنة المحلية في تل أبيب يافا، "
                 "بلدية تل أبيب يافا. القوانين: قانون البيع (شقق) وكفالة قانون البيع. مصطلحات: ضريبة الشراء، ضريبة التحسين "
                 "(هيتل هشبحاه)، رسوم الإدارة، البيع على الخارطة (ما قبل البيع)، حساب المرافقة البنكية. الأماكن التي لا اسم "
                 "عربياً لها في مصدرها تبقى بالإنجليزية: لا اسم مخترَع.",
        "keywords": [("تل أبيب", 140), ("شقق للبيع في اسرائيل", 10), ("رمات أفيف (7.10 morning)", 90),
                     ("سدي دوف / سديه دوف / شقق للبيع في تل أبيب / اسعار الشقق في تل أبيب / مشاريع جديدة تل أبيب / عقارات تل أبيب",
                      "no volume data")],
        "related": "Arabic-script searches for Sde Dov are close to none (Google Ads, Israel, 7.10.2026; the same finding as "
                   "docs/research/2026-09-30-kikar-hamedina/serp-ar.md). The Arabic page serves readers who arrive by a link, "
                   "the site's language switch or a shared WhatsApp message; titles stay in English (the owner's ruling of "
                   "28.9.2026).",
        "audience": "قرّاء عرب، معظمهم في إسرائيل وكثير منهم عائلات ومستثمرون: سعر المتر، التمويل، مواعيد التسليم، المدارس "
                    "والمواصلات.",
        "culture": "عربية فصحى معاصرة واضحة، قريبة من لغة الصحافة الاقتصادية. شرح عدد الغرف الإسرائيلي مرة واحدة («4 غرف: صالون "
                   "وثلاث غرف نوم»). كفالة قانون البيع تُشرح مرة واحدة. نبرة دافئة وواثقة.",
        "typography": "أرقام غربية كما تكتبها الصحافة العربية في إسرائيل (83,000 ₪؛ 9.45 مليون ₪)؛ تواريخ 12.3.2020؛ أسماء "
                      "الأشهر الشامية (آذار، نيسان...) عند ذكر الشهر بالكلمة؛ بلا شرطة طويلة (—) وبلا شرطة متوسطة (–).",
        "units": "م² و₪ فقط. يمكن شرح الدونم مرة واحدة (1 دونم = 1,000 م²).",
        "banned": "واجهة برمجية · عرض تجريبي · نموذج (بمعنى ثلاثي الأبعاد) · محرّك · طبقة · نموذج أولي · محاكاة · تكنولوجيا · «النظام» "
                  "· «المنصة» · تجربة رقمية · ثلاثي الأبعاد · أطلس · قريباً · «استشارة مجانية» · أي اسم لمصدر أو وسيلة إعلام "
                  "(ويكيبيديا، غلوبس، كالكاليست...) · تجدر الإشارة · في الختام · لا شك",
        "in_hebrew": "(بالعبرية)",
        "seo": "The SEO title in ENGLISH (the owner's ruling of 28.9.2026: Arabic pages carry English titles, like the H1), at "
               "most 60 characters, the same rule as English. The description in Arabic, at most 155 characters.",
    },
}
# the components' own headings in each language (the AreaMap translations exist; the PriceGuide ones are expected forms):
# the article's H2s must not start like them
COMPONENT_HEADINGS = {
    "en": ["The Sde Dov quarter on the map: the projects, the beach and the neighbourhood",
           "Sde Dov apartment price list by project", "Sde Dov apartment price calculator",
           "How much does an apartment cost in Sde Dov"],
    "fr": ["Le quartier de Sde Dov sur la carte : les projets, la plage et les environs",
           "Grille des prix des appartements à Sde Dov par programme", "Calculateur du prix d'un appartement à Sde Dov"],
    "ru": ["Район Сде-Дов на карте: проекты, пляж и окрестности", "Прейскурант квартир в Сде-Дов по проектам",
           "Калькулятор цены квартиры в Сде-Дов"],
    "ar": ["حي سديه دوف على الخريطة: المشاريع والشاطئ والمحيط", "قائمة أسعار الشقق في سديه دوف حسب المشروع",
           "حاسبة سعر الشقة في سديه دوف"],
}

# ============================================================== Hebrew source: clean HTML per section
KEEP = {"h1", "h2", "h3", "p", "ul", "ol", "li", "table", "thead", "tbody", "tr", "th", "td", "a", "b"}


def clean_html(h):
    h = re.sub(r"<(script|style|svg|figure)\b.*?</\1>", "", h, flags=re.S | re.I)
    h = re.sub(r"<!--(?! NL(?:AM|PG) -->).*?-->", "", h, flags=re.S)
    h = re.sub(r"<blockquote\b[^>]*>(.*?)</blockquote>", r"<p>\1</p>", h, flags=re.S)
    h = re.sub(r"<(/?)strong\b[^>]*>", r"<\1b>", h)

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
        return "<%s%s>" % (name, (" " + " ".join(keep)) if keep else "")
    h = re.sub(r"<(/?)([a-zA-Z0-9]+)([^>]*)>", tag, h)
    h = re.sub(r"[ \t]+", " ", h)
    h = re.sub(r"\s*\n\s*", "\n", h)
    h = re.sub(r">\s+<", "><", h)
    h = re.sub(r"(</(?:p|h1|h2|h3|li|tr|table|ul|ol|thead|tbody)>|<!-- NL(?:AM|PG) -->)", r"\1\n", h)
    h = re.sub(r"(<!-- NL(?:AM|PG) -->)", r"\n\1", h)
    h = re.sub(r"<p></p>", "", h)
    return re.sub(r"\n{2,}", "\n", h).strip()


def split_sections(page, h):
    """the cleaned Hebrew article -> {section id: html}; the H1 belongs to the first section"""
    secs = SECTIONS[page]
    pos = []
    for sid, h2, part, _ in secs:
        i = h.find("<h2>%s</h2>" % h2)
        assert i >= 0, (page, h2)
        pos.append((sid, i))
    out = {}
    for k, (sid, i) in enumerate(pos):
        j = pos[k + 1][1] if k + 1 < len(pos) else len(h)
        out[sid] = h[i:j].strip()
    first = pos[0][0]
    out[first] = h[:pos[0][1]].strip() + "\n" + out[first]
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
    he_links = {}
    for page in PAGE_IDS:
        h, _ = CT.hebrew_source(page, quiet=True)
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
    # language equivalents that exist (GET 200 in source/linkcheck-20261007.json); everything else stays Hebrew
    eq = {}
    for s in CT.SDD_PROJECTS:
        eq[SITE + "/projects/%s/" % s] = {l: SITE + "/projects/%s-%s/" % (s, l) for l in LANGS}
    eq[SITE + "/new-projects/"] = {l: SITE + "/%s/new-projects/" % l for l in LANGS}
    eq[SITE + "/purchase-tax-calculator/"] = {"en": SITE + "/israel-purchase-tax-foreign-residents/"}
    eq[SITE + "/mortgage-calculator/"] = {"en": SITE + "/israel-mortgage-non-residents/"}
    extras = {
        "sde-dov-hub": {
            "en": [("/en/north-tel-aviv/", "North Tel Aviv: neighborhoods, new projects and prices"),
                   ("/en/buy-property-in-israel/", "buying a home in Israel from abroad"),
                   ("/projects/hamedina-en/", "Kikar HaMedina Towers"), ("/en/brokers/", "licensed real estate brokers")],
            "fr": [("/fr/brokers/", "agents immobiliers agréés"), ("/fr/property-value-estimator/", "estimer la valeur d'un appartement"),
                   ("/projects/hamedina-fr/", "les tours Kikar HaMedina")],
            "ru": [("/ru/brokers/", "лицензированные маклеры"), ("/ru/property-value-estimator/", "оценка стоимости квартиры"),
                   ("/projects/hamedina-ru/", "башни Кикар ха-Медина")],
            "ar": [("/projects/hamedina-ar/", "أبراج كيكار همدينا"), ("/ar/guides/", "أدلة المشتري")]},
        "sde-dov-prices": {
            "en": [("/en/north-tel-aviv/rova-4/", "apartment prices in Rova 4 (the New North)"),
                   ("/en/north-tel-aviv/", "North Tel Aviv"), ("/projects/rainbow-tel-aviv-en/", "Rainbow Tel Aviv"),
                   ("/projects/dimri-yama-sde-dov-en/", "DIMRI YAMA Sde Dov"), ("/projects/ashira-sde-dov-en/", "ASHIRA Sde Dov"),
                   ("/israel-purchase-tax-foreign-residents/", "purchase tax for foreign residents"),
                   ("/israel-mortgage-non-residents/", "a mortgage for non-residents"), ("/en/new-projects/", "new projects in Israel")],
            "fr": [("/projects/rainbow-tel-aviv-fr/", "Rainbow Tel Aviv"), ("/projects/dimri-yama-sde-dov-fr/", "DIMRI YAMA Sde Dov"),
                   ("/projects/ashira-sde-dov-fr/", "ASHIRA Sde Dov"), ("/fr/new-projects/", "programmes neufs en Israël"),
                   ("/fr/property-value-estimator/", "estimer la valeur d'un appartement")],
            "ru": [("/projects/rainbow-tel-aviv-ru/", "Rainbow Tel Aviv"), ("/projects/dimri-yama-sde-dov-ru/", "DIMRI YAMA Sde Dov"),
                   ("/projects/ashira-sde-dov-ru/", "ASHIRA Sde Dov"), ("/ru/new-projects/", "новостройки в Израиле"),
                   ("/ru/property-value-estimator/", "оценка стоимости квартиры")],
            "ar": [("/projects/rainbow-tel-aviv-ar/", "Rainbow Tel Aviv"), ("/projects/dimri-yama-sde-dov-ar/", "DIMRI YAMA Sde Dov"),
                   ("/projects/ashira-sde-dov-ar/", "ASHIRA Sde Dov"), ("/ar/new-projects/", "مشاريع جديدة")]},
    }
    pages = {}
    for page in PAGE_IDS:
        pages[page] = {"he": [dict(x, role="source") for x in he_links[page]]}
        for l in LANGS:
            lst = []
            for x in he_links[page]:
                u = x["url"]
                tgt = eq.get(u, {}).get(l)
                lang_page = SITE + "/%s%s" % (l, u[len(SITE):])
                if tgt and st(tgt) == 200:
                    lst.append({"url": tgt, "maps_from": u, "target_language": l if "/projects/" in tgt or "/%s/" % l in tgt else "en",
                                "status": st(tgt), "role": "mirror (same-topic page in this language)"})
                else:
                    lst.append({"url": u, "maps_from": u, "target_language": "he", "status": st(u),
                                "language_version": lang_page, "language_version_status": st(lang_page),
                                "role": "mirror (no %s version yet: link the Hebrew page and say so)" % l})
            for path, anchor in extras[page][l]:
                if not any(y["url"] == SITE + path for y in lst):
                    lst.append({"url": SITE + path, "anchor_suggestion": anchor,
                                "target_language": "en" if path.startswith("/israel-") else l, "status": st(SITE + path),
                                "role": "optional extra (at most 3 in the article)"})
            pages[page][l] = lst
    for page in pages:
        for l in pages[page]:
            for x in pages[page][l]:
                assert x["status"] == 200, (page, l, x)
    doc = {"checked_utc": lc["checked_utc"], "method": "GET without following redirects, UA 'nad-lan.co.il i18n link check "
           "(HAD-439)', one request per 0.4 s (linkcheck.py); every URL below answered 200. A /<lang>/<path>/ version of a Hebrew "
           "target that answered 404 is listed as language_version_status 404, and that link stays Hebrew.", "pages": pages,
           "swap_after_publish": {
               "rule": "When /<lang>/sde-dov/ and /<lang>/sde-dov/prices/ are both live, point the hub <-> prices links of that "
                       "language to each other (and add them here). Also: /en/north-tel-aviv/ links the Hebrew /sde-dov/ today; "
                       "swap it to /en/sde-dov/ when that page is live.",
               "sde-dov-hub": {l: [HE_URL["sde-dov-prices"], TARGET["sde-dov-prices"][l]] for l in LANGS},
               "sde-dov-prices": {l: [HE_URL["sde-dov-hub"], TARGET["sde-dov-hub"][l]] for l in LANGS}}}
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
  inline style, no br, no images, no scripts, no emoji, no shortcodes (the site inserts its own components). The ONLY HTML
  comment allowed is the component marker below.
- Exactly ONE <h1>, first, with the H1 given below. Then the sections in the order of the outline. Each section opens with its
  <h2> (the suggested heading, or a better one in the same order that keeps its keywords and does not start with the same 4
  words as another page of the site: the "avoid" list). H3s exactly where the Hebrew has them.
- THE MARKER: write MARKER on its own line right after the FIRST paragraph of the first section, exactly where the Hebrew
  source has it (the site puts COMPONENT there). Exactly once, copied character for character. Do not describe the component.
- Tables: one table wherever the Hebrew has one, same columns, same rows, same order, every number identical:
  <table><thead><tr><th>..</th></tr></thead><tbody><tr><td>..</td></tr></tbody></table>. Translate labels and words in cells.
- FAQ: <h2>FAQ_H2</h2> then, for each question in order, <h3>question</h3><p>answer</p> (one paragraph, the first sentence
  answers directly, the same facts and numbers as the Hebrew answer).
- Links: <a href="FULL_URL">anchor in the article's language</a>, only URLs from internal_links, each where the Hebrew has its
  link (a list of links stays a <ul> list). A link to a Hebrew page carries IN_HEBREW after the anchor, outside the <a>. At
  most 3 optional extras. No external link.
- Do NOT write: the site disclaimer, an "updated" or "checked on" line (the site adds it), a list of sources, the multilingual
  keyword line, a table of contents.
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
   (9.45 million stays 9.45 million; 81,800 stays 81,800); never convert currency or units. Each message gives the claims of
   its part (claims_for_part_1 in the packet, then one list in each later message) with every allowed number and its
   meaning: if a number is not there, it may not appear in that part. The SEO title and description may use any claim
   already given. Every number you write is checked by a script.
2. No source names in the text (no newspapers, websites, Wikipedia, survey firms, "according to X"); dates carry the evidence
   ("a survey of the developers' reports published in April 2026" is the right form).
3. Deals stay deals, price lists stay price lists, estimates and forecasts stay estimates and forecasts: never upgrade one into
   the other.
4. Marketing language of an Israeli real-estate site, warm and concrete; no tech or demo talk. Banned: {banned}
5. No self-disclaimers, no pile of caveats, no "red flags" chapter.
6. Do not research. Your only material is this message: the packet (JSON) and the Hebrew source below.

## The reader
{audience}
{culture}

## Names (use exactly)
{names}

## What {lang_name} speakers search (Google Ads monthly searches, 12-month average; DataForSEO, 7.10.2026)
{keywords}
{related}
Use the words people type in the H1, the first paragraph and the H2s where natural; never stuff.

## Structure and length
Mirror the Hebrew: {n_h2} H2 sections in this order (outline in the packet: suggested H2, word budget, the claims each section
must use). Length close to the Hebrew: about {target_words} words in all ({lo} to {hi}), each section within about 15% of its
budget. {length_note}

## The HTML contract
{contract}
(FAQ_H2 = "{faq_h2}", IN_HEBREW = "{in_hebrew}", H1 = "{h1}", MARKER = "{marker}", COMPONENT = {component})

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

PAGE_NAME = {
    "sde-dov-hub": "the Sde Dov quarter guide (the hub of Tel Aviv's new seafront quarter on the former Sde Dov airfield: "
                   "history, land, the master plan and its three compounds, the projects on sale, developers, prices, "
                   "transport, affordable housing, investment, legal checks before buying off plan, FAQ, the planning chapter "
                   "and the links to the quarter's guides and projects)",
    "sde-dov-prices": "Sde Dov apartment prices (the quarter's price page: average price per m2 from the developers' reports, "
                      "prices by room count and by compound, the sea-view premium, record and entry deals, a comparison with "
                      "Tel Aviv's luxury neighborhoods, presale versus occupancy, financing, legal and tax points, forecast, how "
                      "to read a price offer, FAQ)",
}
COMPONENT = {"sde-dov-hub": "the quarter's interactive area map (projects, beaches, parks, schools, Green Line stations)",
             "sde-dov-prices": "the quarter's price list by project and its price calculator"}
NOT_PUBLISHED = {
    "sde-dov-hub": ["a delivery date for the whole quarter", "the management fees of any project", "rents and rental yields",
                    "prices per m2 per compound other than those given", "the PFAS soil contamination reports (not in the "
                    "Hebrew page: do not add)", "a separate hotel figure for the Eshkol compound"],
    "sde-dov-prices": ["an official median per room count for Sde Dov itself (the official neighborhood file has none)",
                       "a separate average for the Centre or the North compound", "Park Tzameret prices",
                       "the floor area of the 2-room deals of May 2026", "an average floor area of 4-room apartments",
                       "rents and rental yields", "the names of buyers"],
}


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
        if sid == "hub-projects":
            item["h3"] = HUB_H3_PROJECTS
        if sid == "hub-planning":
            item["h3"] = d["h3_planning"]
            item["note"] = ("The Hebrew has a short quote line after the H3 on checking an apartment: keep it as a <p>. The "
                            "official-sources list that closes the Hebrew chapter is NOT translated.")
        if sid.endswith("faq"):
            item["faq_questions"] = d["faq"][page]
        if sid in ("hub-guide", "hub-links"):
            item["note"] = ("A list of links, one <li> per Hebrew link, in the same order. Translate each anchor; a link to a "
                            "Hebrew page carries IN_HEBREW.")
        if sid == secs[0][0]:
            item["note"] = ("The first section: the H1, then this H2, then the first paragraph, then the marker %s on its own "
                            "line%s." % (CT.PAGES[page]["marker"], ", then the rest of the section's paragraphs" if page ==
                                         "sde-dov-prices" else " (the Hebrew section has one paragraph)"))
        if sid == "pr-abroad":
            item["note"] = ("The Hebrew H2 says 'foreign investors and international search words': write a reader's heading "
                            "(the suggested one). The multilingual keyword line under it is NOT translated.")
        outline.append(item)
        parts.setdefault(part, []).append(sid)
    target_words = int(round(total_he * FACTOR[lang] / 10.0) * 10)
    lo, hi = int(target_words * 0.85), int(target_words * 1.2)
    claims = [c for c in CLAIMS if c["page"] in (page, "both")]
    avoid = sorted(set(CT.key4(t) for u, x in comps.items() if x.get("status") == 200 for k in ("title", "h1", "h2")
                       for t in x.get(k, []) if t and not re.search(r"[א-ת]", t)) |
                   set(CT.key4(t) for t in COMPONENT_HEADINGS[lang]))
    packet = {
        "page": page, "language": lang, "target_url": TARGET[page][lang], "hebrew_url": HE_URL[page], "h1": d["h1"][page],
        "faq_h2": d["faq_h2"], "marker": CT.PAGES[page]["marker"], "words_target": target_words, "words_total_range": [lo, hi],
        "hebrew_words": total_he, "h2_count": len(secs), "outline": outline, "names": d["names"],
        "keywords_monthly": d["keywords"], "serp": d["related"], "audience": d["audience"], "culture": d["culture"],
        "typography": d["typography"], "units": d["units"], "banned": d["banned"], "in_hebrew_marker": d["in_hebrew"],
        "internal_links": links_doc["pages"][page][lang], "avoid_headings_first_4_words": avoid,
        "component_headings_in_this_language": COMPONENT_HEADINGS[lang], "not_published": NOT_PUBLISHED[page],
        "seo_request": d["seo"],
        "claims": [{k: c[k] for k in ("claim_id", "topic", "claim", "numbers", "date", "conflict", "write_as") if c[k]}
                   for c in claims],
        "sources_note": "Sources stay in the repo (claims.json source field, align-check.md, sde-dov-prices.json); never in the "
                        "text.",
    }
    os.makedirs(os.path.join(HERE, "packets"), exist_ok=True)
    io.open(os.path.join(HERE, "packets", "%s-%s.json" % (page, lang)), "w", encoding="utf-8").write(
        json.dumps(packet, ensure_ascii=False, indent=1) + "\n")
    # ---- the prompt, one message per output part
    kw = "\n".join("- %s: %s" % (k, v) for k, v in d["keywords"])
    typo_short = {"en": "83,000 / 9.45 million", "fr": "83 000 / 9,45 millions", "ru": "83 000 / 9,45 млн",
                  "ar": "83,000 / 9.45 مليون (Western digits)"}[lang]
    plan = []
    for p in sorted(parts):
        plan.append("- Part %d (%s): %s." % (p, "now, with message 1" if p == 1 else "when I send message %d" % p,
                                             ", ".join("%s (%s)" % (s, next(o["h2"] for o in outline if o["id"] == s))
                                                       for s in parts[p])))
    length_note = ("The Hebrew counts %d words (tables included); %s runs about %d%% of the Hebrew word count for the same "
                   "content." % (total_he, LANG_NAME[lang], int(FACTOR[lang] * 100)))

    def part_claims(p):
        ids = []
        for o in outline:
            if o["part"] == p:
                ids += [i for i in o["must_use"] if i not in ids]
        ids += [c["claim_id"] for c in claims if c["claim_id"].startswith("G-") and c["claim_id"] not in ids]
        return [x for x in packet["claims"] if x["claim_id"] in ids]
    lean = {"h1": packet["h1"], "target_url": packet["target_url"], "faq_h2": packet["faq_h2"], "marker": packet["marker"],
            "outline": packet["outline"], "claims_for_part_1": part_claims(1),
            "internal_links": [{k: x[k] for k in ("url", "maps_from", "target_language", "anchor_suggestion") if k in x}
                               for x in packet["internal_links"]],
            "avoid_headings_first_4_words": packet["avoid_headings_first_4_words"], "not_published": packet["not_published"]}
    compact = json.dumps(lean, ensure_ascii=False, separators=(",", ":"))
    head = PROMPT.format(lang_name=LANG_NAME[lang], page_name=PAGE_NAME[page], target=TARGET[page][lang],
                         source_url=HE_URL[page], typo_short=typo_short, banned=d["banned"], audience=d["audience"],
                         culture=d["culture"], names=d["names"], keywords=kw, related=d["related"], n_h2=packet["h2_count"],
                         target_words=target_words, lo=lo, hi=hi, length_note=length_note, contract=HTML_CONTRACT,
                         faq_h2=d["faq_h2"], in_hebrew=d["in_hebrew"], h1=d["h1"][page], marker=CT.PAGES[page]["marker"],
                         component=COMPONENT[page], typography=d["typography"], units=d["units"], n_parts=len(parts),
                         parts_plan="\n".join(plan), seo=d["seo"], packet=compact)
    msgs = []
    for p in sorted(parts):
        src = "\n\n".join("<!-- section %s -->\n%s" % (s, he_secs[s]) for s in parts[p])
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
    md = ["# Prompt: %s, %s (HAD-439 Stage A)\n" % (page, LANG_NAME[lang]),
          "Built by build_packets.py on %s UTC from claims.json (%d claims for this page), links.json (every link GET 200 on "
          "7.10.2026) and the live Hebrew page%s. Paste each message into ONE new ChatGPT conversation in order (message 1 now; "
          "each next message after the previous part arrives). Message sizes (characters): %s; each is under %d. The section "
          "comments in the Hebrew source (<!-- section ... -->) are for orientation only; the writer outputs only the marker "
          "%s. Then run: python check_translation.py <joined parts>.html --page %s --lang %s --meta <text block>.txt\n"
          % (datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M"), len(claims),
             " (with align-edits.json applied)" if CT.PAGES[page]["edits"] else "", ", ".join("%d" % s for s in sizes),
             MAX_MSG, CT.PAGES[page]["marker"], page, lang)]
    for k, m in enumerate(msgs, 1):
        md.append("\n---\n\n## Message %d of %d\n\n%s" % (k, len(msgs), m))
    io.open(os.path.join(HERE, "packets", "prompt-%s-%s.md" % (page, lang)), "w", encoding="utf-8").write("\n".join(md) + "\n")
    assert max(sizes) < MAX_MSG, (page, lang, sizes)
    # own headings vs live pages (first 4 words), and vs the other page of the pair in the same language
    own = [("h1", d["h1"][page])] + [("h2", o["h2"]) for o in outline if o["h2"]]
    other = OTHER[page]
    comps2 = dict(comps)
    comps2["(pair: %s)" % other] = {"status": 200, "title": [], "h1": [d["h1"][other]], "h2": d["h2"][other]}
    comps2["(components)"] = {"status": 200, "title": [], "h1": [], "h2": COMPONENT_HEADINGS[lang]}
    dupes = CT.heading_dupes(own, lang, comps2)
    return {"page": page, "lang": lang, "words_target": target_words, "range": [lo, hi], "hebrew_words": total_he,
            "h2": len(secs), "parts": len(parts), "msg_sizes": sizes, "claims": len(claims),
            "links": len(links_doc["pages"][page][lang]), "dupes": dupes}


def main():
    links_doc = build_links()
    heads = build_live_headings()
    he = {}
    for page in PAGE_IDS:
        h, _ = CT.hebrew_source(page, quiet=True)
        he[page] = split_sections(page, clean_html(h))
        io.open(os.path.join(HERE, "source", "%s-he-clean.html" % page), "w", encoding="utf-8").write(
            "\n\n".join("<!-- section %s -->\n%s" % (k, v) for k, v in he[page].items()) + "\n")
    rows = []
    for page in PAGE_IDS:
        for lang in LANGS:
            comps = {u: x for u, x in heads["pages"].items() if u in CT.COMPARATORS[lang]}
            r = build(page, lang, he[page], links_doc, comps)
            rows.append(r)
            print("%-15s %s | Hebrew %d words -> target %d (%d-%d) | H2 %d | parts %d, message chars %s | claims %d | links %d | "
                  "heading dupes %d" % (page, lang, r["hebrew_words"], r["words_target"], r["range"][0], r["range"][1], r["h2"],
                                        r["parts"], r["msg_sizes"], r["claims"], r["links"], len(r["dupes"])))
            for x in r["dupes"]:
                print("    DUPLICATE", x)
    io.open(os.path.join(HERE, "packets", "build-summary.json"), "w", encoding="utf-8").write(
        json.dumps(rows, ensure_ascii=False, indent=1) + "\n")


if __name__ == "__main__":
    main()
