# -*- coding: utf-8 -*-
"""Kochav HaTzafon mini penthouse (listing L07, Meital Katzir): the French and Russian pages. LOCAL FILES ONLY.

Built 21.10.2026 from the live English page (../after-7812.html): the same sections, FAQ, FAQPage, RealEstateListing,
WebApplication and VideoObject data, the 360 tour (?lang=en), the film, the 3D walk and the seo_tools.py calculator,
written for French and Russian buyers (campaign/keywords.md), not word for word.
  python docs/sales/kochav-ph/page/lang/build_lang.py [--page-id-fr N] [--page-id-ru N]
Writes after-fr.html, after-ru.html (the post_content), seo.json (title, meta, URL, parent, hreflang) and preview-*.html.
Nothing is published. The pages follow the drop engine's route: a WordPress page under /<lang>/brokers/meital-katzir/
with the Hebrew slug, nl_lang, nl_broker_id 7833, and nl_hreflang on all four siblings (snippet nl-i18n-hreflang-print).

Owner rules held by the checks at the bottom: an EXISTING home FOR SALE at 18,000,000 (no "neuf", no "новый" for the home);
no tenant, no current rent, no yield of this home (area averages stay); "mini-penthouse" / "мини-пентхаус", never attico
or cobertura; no Ben, no share, no commission, no "best in the world"; the engine's FR/RU word gate (no dashes, no "!")."""
import html, io, json, os, re, sys, urllib.parse

H = os.path.dirname(os.path.abspath(__file__))
P = os.path.dirname(H)
sys.path.insert(0, P)
import seo_tools as ST  # noqa: E402  (the calculator and the mini penthouse test, shared with he/en)

if (sys.stdout.encoding or "").lower() != "utf-8":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

BASE = "https://nad-lan.co.il"
SLUG = "kochav-hatzafon-new-mini-penthouse-for-sale"   # the Hebrew slug, as the engine gives every language (nofei-yam-5-rooms-for-rent pattern)
URL = {"he": BASE + "/properties/" + SLUG + "/", "en": BASE + "/en/brokers/meital-katzir/" + SLUG + "/",
       "fr": BASE + "/fr/brokers/meital-katzir/" + SLUG + "/", "ru": BASE + "/ru/brokers/meital-katzir/" + SLUG + "/"}
SITE = {"he": BASE + "/brokers/meital-katzir/", "en": BASE + "/en/brokers/meital-katzir/",
        "fr": BASE + "/fr/brokers/meital-katzir/", "ru": BASE + "/ru/brokers/meital-katzir/"}
PARENT = {"fr": 8375, "ru": 8372}                     # Meital's live FR and RU site pages (page-id on the live HTML, 21.10.2026)
WALK = BASE + "/wp-content/plugins/nadlan-config/assets/walk/kochav/"
WA_NUM = "972523631582"
TEL = "+972 52-363-1582"
LIC = "3131540"
NB = " "
MEDIA = json.load(open(os.path.join(P, "media.json"), encoding="utf-8"))
FILM_MP4 = MEDIA["kochav-film-en.mp4"]["url"]
FILM_JPG = MEDIA["kochav-film-en.jpg"]["url"]
ARGS = sys.argv[1:]
PAGE_ID = {l: int(ARGS[ARGS.index("--page-id-" + l) + 1]) for l in ("fr", "ru") if "--page-id-" + l in ARGS}

SRC = io.open(os.path.join(P, "after-7812.html"), encoding="utf-8").read()


# ------------------------------------------------------------------ typography and markup helpers
def ty(s, lang):
    """Thousands with a no-break space (18 000 000), no-break space before ₪ % m² $ €, and French spacing before : ; ?"""
    s = re.sub(r"(?<=\d) (?=\d{3}(?!\d))", NB, s)
    s = re.sub(r" (?=(?:₪|%|m²|м²|\$|€)(?!\w))", NB, s)
    if lang == "fr":
        s = re.sub(r" (?=[:;?])", NB, s)
    return s


NUM = re.compile(r"(?<![\w>#/])(?:\d[\d ,.]*\d|\d)(?: (?:₪|%|m²|м²|\$|€)(?!\w))?")  # the unit rides in the span: 80 m² never breaks


def nums(s, lang):
    """Plain text -> safe HTML with every number in the dossier's tabular span."""
    s = html.escape(ty(s, lang), quote=False)
    return NUM.sub(lambda m: '<span class="nlx-num">' + m.group(0) + "</span>", s)


def n(x):
    return '<span class="nlx-num">' + x + "</span>"


def money(x):
    return '<span class="nlx-money"><span class="nlx-num">' + x + "</span></span>"


def esc(s):
    return html.escape(s, quote=True)


def fmt(v, lang, dec=None):
    s = f"{v:,.{dec}f}" if dec is not None else f"{round(v):,}"
    return s.replace(",", NB).replace(".", ",") if dec is not None else s.replace(",", NB)


def cur(v, lang):
    return fmt(v, lang) + NB + "₪"


# ------------------------------------------------------------------ the copy
T = {}
T["fr"] = dict(
    locale="fr-FR", toc_label="Sur cette page", site_link="Le site de Meital Katzir",
    title="Mini-penthouse à vendre, Tel Aviv Nord | Kochav HaTzafon",
    meta="Mini-penthouse de 5 pièces à Kochav HaTzafon, nord de Tel Aviv : 197 m², 80 m² de terrasses, 11e étage sur 12, près du parc HaYarkon. 18 000 000 ₪.",
    kicker="À vendre · Kochav HaTzafon, nord de Tel Aviv",
    h1="Mini-penthouse de 5 pièces à vendre à Kochav HaTzafon, Tel Aviv Nord",
    dek="Un étage sous le dernier, dans un immeuble boutique récent de Kochav HaTzafon : cinq pièces sur environ 197 m², et autour d’elles 80 m² de terrasses ouvertes sur la ligne d’horizon de Tel Aviv. Un appartement à vendre au nord de Tel Aviv, à 18 000 000 ₪.",
    chips=["En exclusivité : <a href=\"" + SITE["fr"] + "\">Meital Katzir</a>", "Immeuble boutique de 12 étages", "Aile des enfants avec balcon vue mer"],
    plate="Kochav HaTzafon, 11e étage",
    alt_base="Mini-penthouse à vendre à Kochav HaTzafon, Tel Aviv",
    alts={"המרפסת הראשית והנוף לתל אביב": "la terrasse principale et la vue sur Tel Aviv", "הסלון עם יציאה למרפסת": "le séjour ouvert sur la terrasse",
          "המטבח והמקרר האינטגרלי": "la cuisine et le réfrigérateur intégré", "אגף הילדים והמרפסת לים": "l’aile des enfants et le balcon vue mer",
          "תמונה 8": "photo 8", "תמונה 9": "photo 9"},
    facts=[("Pièces", "5"), ("Surface habitable", "env. 197 m²"), ("Terrasses", "80 m²"), ("Étage", "11 sur 12"), ("Orientations", "3 à 4"),
           ("Parking", "2 places"), ("Cave", "Oui"), ("Mamad (pièce sécurisée), ascenseur", "Oui")],
    toc=[("film", "Film"), ("tour", "Visite 360°"), ("world", "3D"), ("home", "Le bien"), ("mini", "Mini-penthouse"), ("building", "L’immeuble"),
         ("location", "Le quartier"), ("future", "Urbanisme"), ("value", "Valeur"), ("numbers", "Les chiffres"), ("calc", "Calculateur"),
         ("market", "Marché"), ("checks", "Vérifications"), ("faq", "Questions")],
    photos=("Photos", "L’appartement en images"),
    film=("Film", "Une journée à Kochav HaTzafon",
          "Le matin dans le quartier, un café au centre commercial voisin, la nouvelle passerelle vers le parc HaYarkon, l’appartement lui-même, une soirée entre amis sur la terrasse, et les chiffres du quartier. Film en anglais.",
          "L’appartement a été filmé sur place. La passerelle, les vues aériennes et les scènes de vie sont des illustrations, signalées comme telles dans le film."),
    tour=("Visite virtuelle", "Pièce par pièce, en 360°",
          "L’entrée, le séjour, la cuisine, le coin repas et la terrasse, de jour et au crépuscule. La visite est construite à partir des vraies images de l’appartement ; les parties que la caméra n’a pas vues ont été complétées, il s’agit donc d’une illustration. Interface en anglais.",
          "L’appartement en 360°", "Faites glisser pour regarder autour de vous et passer d’une pièce à l’autre", "Commencer la visite", "Fermer"),
    world=("En 3D", "De l’appartement au parc HaYarkon, par la nouvelle passerelle",
           "Kochav HaTzafon tel qu’il est, reconstitué à partir des plans de la municipalité de Tel Aviv-Yafo : les rues, les immeubles et les arbres, la passerelle prévue au-dessus du boulevard Rokach, les pelouses de Ganei Yehoshua et le Yarkon. Parcourez les rues, traversez la passerelle et voyez à combien de minutes à pied se trouvent chaque café, chaque école et chaque jardin d’enfants.",
           "Se promener dans le quartier et sur la passerelle", "De jour, au coucher du soleil et la nuit. Plus de 1 000 lieux alentour, avec les temps de marche. Interface en hébreu.",
           "Commencer la promenade", "La passerelle prévue au-dessus du boulevard Rokach vers le parc HaYarkon, illustration 3D",
           "Illustration réalisée à partir des plans de la municipalité. La passerelle suit sa description publiée (environ 170 m, 6 m de large, ouverture prévue en 2027), pas les plans d’exécution."),
    home_eyebrow="Le bien", home_h2="La ville, le parc, et tout ce qui les relie",
    home=["Certains biens comprennent le rythme de Tel Aviv, et savent aussi offrir un calme absolu une fois la porte refermée. En hauteur dans le quartier de Kochav HaTzafon, dans un immeuble boutique récent et élégant, ce mini-penthouse redéfinit l’habitat haut de gamme au nord de la ville, à quelques minutes à pied de la verdure du parc HaYarkon et de tout ce qu’il offre.",
          "L’intérieur (près de 200 m²) se distingue par une menuiserie sur mesure réalisée par un artisan et une ligne de design soignée. Le cœur de l’appartement est un vaste espace de réception, ouvert sur une cuisine de designer entièrement équipée, avec électroménager intégré.",
          "L’architecture offre une vue entièrement dégagée sur la ligne d’horizon de Tel Aviv depuis la suite parentale et les pièces de vie, tandis que la suite des enfants donne aussi sur la ligne scintillante de la mer.",
          "La vraie expérience commence sur la grande terrasse ensoleillée (environ 74 m²), ouverte sur 3 côtés, dans une continuité naturelle entre intérieur et extérieur, avec une climatisation VRF de dernière génération.",
          "Cinq pièces au 11e étage sur 12. Deux places de parking, une cave, un mamad (pièce sécurisée) et un ascenseur, et une salle de sport pour les résidents dans l’immeuble."],
    features=[("11e étage sur 12", "Vue dégagée sur Tel Aviv"), ("Environ 197 m² habitables", "Cinq pièces et une grande suite parentale"),
              ("80 m² de terrasses", "Dont un balcon vue mer côté chambres des enfants"), ("Climatisation VRF", "Et une cuisine avec réfrigérateur intégré dissimulé"),
              ("Deux places de parking et une cave", "Un mamad et un ascenseur"), ("Une passerelle vers le parc HaYarkon", "Environ 170 m, ouverture prévue en 2027")],
    spec=[("L’appartement", [("Type et pièces", "Mini-penthouse, 5 pièces (décompte israélien, séjour inclus)"), ("Surface habitable", "Environ 197 m²"),
                             ("Terrasses", "80 m² au total, dont une terrasse ensoleillée d’environ 74 m²"), ("Étage", "11 sur 12"), ("Orientations", "3 à 4"),
                             ("Agencement", "Suite parentale, aile des enfants avec balcon vue mer, grand séjour")]),
          ("Prestations et services", [("Cuisine", "Cuisine équipée avec électroménager et réfrigérateur intégré dissimulé"), ("Climatisation", "Système VRF multi-split"),
                                       ("Menuiserie", "Menuiserie sur mesure"), ("Parking et cave", "2 places de parking et une cave"), ("Mamad et ascenseur", "Oui")])],
    building=("L’immeuble", "Un immeuble boutique de douze étages", "L’adresse de l’immeuble, le promoteur et les charges de copropriété sont communiqués sur demande directe.",
              [("Emplacement", "Kochav HaTzafon, Tel Aviv-Yafo"), ("Étages", "12"), ("Année de construction", "2022 ou 2023"), ("Services aux résidents", "Salle de sport"),
               ("Prix en euros", "Environ 5,1 millions d’euros au taux représentatif"), ("Prix en dollars", "Environ 5,9 millions de dollars au taux représentatif")]),
    location=("Le quartier", "Kochav HaTzafon, le parc au sud et Sde Dov au nord",
              ["Kochav HaTzafon est délimité par le boulevard Rokach et le parc HaYarkon au sud, la route Namir à l’est, la rue Shai Agnon et le quartier de Sde Dov au nord, et la rue Ibn Gabirol à l’ouest. Il a été construit pour l’essentiel dans les années 1990 et 2000, en immeubles de 8 à 12 étages autour d’un parc central, aux côtés de tours résidentielles et d’immeubles boutique. Selon les données publiées par Mako, la transaction médiane entre 2023 et octobre 2025 y atteignait 6,1 millions ₪, la quatrième plus élevée d’Israël.",
               "Le parc HaYarkon, environ 3 750 dounams (375 hectares) avec le Sportek, borde le quartier le long du boulevard Rokach, et le port de Tel Aviv, un complexe de loisirs de 220 dounams, se trouve au bout du parc. À l’angle de Rokach et de Namir, le projet du Séminaire HaKibboutzim prévoit trois tours résidentielles de 28 étages et 450 logements.",
               "Le tronçon sud de la ligne verte du tramway doit ouvrir en 2028 et la ligne complète en 2030, avec la station Reading sur le nouveau pont au nord du boulevard Rokach. Une nouvelle passerelle piétonne et cyclable de 180 m au-dessus du Yarkon a ouvert en mai 2026."],
              "Écoles", [("École primaire Kochav HaTzafon", "École publique du quartier, environ 82 élèves par niveau ; la zone d’inscription de l’immeuble reste à confirmer"),
                         ("Ironi Kaf-Daled (24), Amos Oz", "Situé dans le quartier, environ 47 élèves par niveau ; zone d’inscription à confirmer")],
              "Transports", [("Ligne verte du tramway, station Reading", "En construction ; tronçon sud prévu en 2028 et ligne complète en 2030 ; la station Reading sera au nord du boulevard Rokach, sur le nouveau pont de la ligne verte (station couverte de 12 m de haut)"),
                             ("Passerelle Rokach-Levi Eshkol vers le parc HaYarkon", "En construction depuis l’été 2026, ouverture prévue en 2027 ; environ 170 m de long et 6 m de large, accessible sans ascenseur"),
                             ("Passerelle du Yarkon (du parc HaYarkon à Ibn Gabirol)", "En service depuis mai 2026 ; 180 m sur 6 m")],
              "Pour aller plus loin : <a href=\"" + BASE + "/fr/north-tel-aviv/\">l’immobilier au nord de Tel Aviv, quartier par quartier</a> · <a href=\"" + BASE + "/fr/sde-dov/\">Sde Dov, programmes neufs et prix</a> · <a href=\"" + BASE + "/acheter-appartement-israel-2026/\">acheter un appartement en Israël en 2026</a>"),
    future=("Urbanisme", "Ce qui est prévu à proximité", "Les projets et travaux publiés, et ce qu’ils peuvent signifier pour un acheteur. D’après les informations publiées ; ne remplace pas une vérification auprès des services d’urbanisme.",
            [("La passerelle Rokach-Levi Eshkol vers le parc HaYarkon", "Un accès direct à pied et à vélo depuis la rue Levi Eshkol jusqu’au parc à partir de 2027, avec des travaux sur le boulevard Rokach d’ici là. Le projet a été approuvé en janvier 2022, avec un budget de 35 millions ₪."),
             ("Projet du Séminaire HaKibboutzim, angle boulevard Rokach et route Namir", "Environ 55 dounams : trois tours de 28 étages avec 450 logements et trois immeubles de 6 étages le long de la rue Maurizio Vitale, jusqu’à 1 550 m² de commerces et 4 600 m² d’équipements publics. Première phase (134 logements et un nouveau bâtiment pour le collège) en environ 5 ans ; financement d’environ 1,7 milliard ₪. Des années de travaux et de nouvelles tours à l’angle sud-est du quartier."),
             ("Les tours du quartier de Sde Dov", "Le plan du centre, dont les recours ont été rejetés le 3 février 2025, prévoit 7 128 logements dans des tours de 20 et 45 étages ; la plupart des appartements du quartier sont attendus d’ici 3 à 6 ans. Les tours au nord peuvent modifier la ligne d’horizon et la vue vers la mer."),
             ("Ligne verte du tramway", "Un meilleur accès au rail depuis la station Reading, au nord du boulevard Rokach, une fois ouverte (tronçon sud en 2028, ligne complète en 2030) ; des travaux autour de Rokach et du Yarkon d’ici là."),
             ("Le site de la centrale Reading", "Fin de la production selon la décision de 2024 : une partie du site passe à un usage civil et à la plage, le reste est conservé pour le stockage et une liaison par câble sous-marin ; un plan de conservation transforme Reading A en musée, centre d’accueil et lieu d’événements. Calendrier à confirmer.")]),
    value=("Valeur", "La passerelle, le parc et le quartier : l’effet sur la valeur",
           "Ce que l’on sait de la passerelle, ce que les études ont montré sur l’effet des parcs et des liaisons piétonnes sur le prix des logements, et ce qui est prévu autour. Des informations pour décider, pas une prévision.",
           [("La passerelle vers le parc HaYarkon", "Environ 170 m de long et 6 m de large : 3 m pour les piétons et 3 m pour les vélos, un tablier en bambou et un éclairage LED dans les garde-corps, de plain-pied, sans ascenseur. Les travaux ont commencé en juin 2026 et l’ouverture est prévue en 2027 (Maariv, Walla, Bizportal, 3 août 2026). Elle fait partie d’un axe nord-sud prévu, avec une seconde passerelle au-dessus du Yarkon."),
            ("L’étude sur le parc HaYarkon", "Une étude du Technion (Shefer et Zakai, 2003) a montré que les logements situés à moins de 100 m du parc HaYarkon valaient environ 136 dollars de plus par m² que ceux situés entre 100 et 1 500 m."),
            ("Parcs et liaisons à l’étranger", "Près de parcs urbains connus, les logements voisins ont pris de la valeur : environ 5 % autour de la Greenway de Boston, environ 20 % autour de la High Line à New York, environ 23 % autour de Klyde Warren à Dallas et 30 % à 40 % autour du Millennium Park à Chicago (HR&A, 2014). Une synthèse de 20 études a trouvé 3 % à 5 % pour les maisons proches des voies piétonnes et cyclables (Crompton et Nicholls, 2019). L’effet est le plus fort près de la liaison et diminue avec la distance."),
            ("Sde Dov, au nord du quartier", "Environ 16 000 logements, environ 365 dounams de parcs et des tours jusqu’à 40 étages selon le plan approuvé. Le neuf du quartier s’est vendu en moyenne environ 79 000 ₪ le m² (février 2026)."),
            ("La ligne verte du tramway", "Environ 39 km et 62 stations, de Rishon LeZion à Herzliya ; selon les informations publiées, l’ouverture est prévue en 2028."),
            ("Les prix du quartier aujourd’hui", "En moyenne environ 49 000 à 51 000 ₪ le m² à Kochav HaTzafon, et 90 000 à 95 000 ₪ le m² dans les programmes neufs et les biens d’exception (Bizportal, juillet 2026).")],
           "Scénarios illustratifs uniquement, ni prévision ni promesse", ("Scénario", "Variation de valeur", "Valeur", "Au m² habitable"),
           "Calcul : 18 000 000 ₪ multipliés par le taux du scénario, rapportés à 197 m² habitables. La taxe d’acquisition et l’avocat représentent à eux seuls environ 7 % à 9,9 % du prix : les scénarios se lisent donc sur le long terme. Ceci n’est pas un conseil en investissement ; consultez un expert immobilier, un avocat et un conseiller fiscal."),
    numbers=dict(eyebrow="Les chiffres", h2="18 000 000 ₪, le calcul d’un acheteur", small="Le prix de 18 000 000 ₪, calculé selon les règles fiscales et de crédit publiées jusqu’au 16 septembre 2026.",
                 kpis=[("Prix demandé", "18 000 000 ₪", "≈ 5 903 575 $ · ≈ 5 118 144 €"), ("Prix au m² habitable", "91 371 ₪", ""),
                       ("Moyenne au m², Kochav HaTzafon", "51 000 ₪", "49 000 à 51 000 ₪, Bizportal, juillet 2026"), ("Prêt maximal, seul logement", "13 500 000 ₪", "75 % de la valeur, Banque d’Israël")],
                 seg_h3="Ce que cela coûte, selon le profil d’acheteur",
                 seg_labels=["Seul logement, résident israélien", "Résidence supplémentaire ou non-résident", "Nouvel immigrant (olé)"],
                 rows=["Taxe d’acquisition", "Prêt maximal", "Apport minimal", "Apport et taxe d’acquisition"],
                 notes=[["Taux effectif 6,41 %", "75 % de la valeur", "", "Avant les frais d’avocat, d’expertise et autres frais"],
                        ["Taux effectif 9,33 %", "50 % pour un logement d’investissement ou un acheteur qui n’est pas citoyen israélien", "", "Avant les frais d’avocat, d’expertise et autres frais"],
                        ["Taux effectif 5,42 %. Éligibilité : d’un an avant à sept ans après l’alya", "75 % de la valeur", "", "Avant les frais d’avocat, d’expertise et autres frais"]],
                 seg_small="Le barème de la taxe d’acquisition est gelé jusqu’au 15 janvier 2028. Les taux de 8 % et 10 % pour les résidences supplémentaires relèvent d’une disposition temporaire valable jusqu’au début de 2027. Pas un conseil fiscal.",
                 bars_h3="Le prix au m² face au marché",
                 bars=["Cet appartement, sur 197 m² habitables", "Cet appartement, terrasses à un tiers", "Programmes neufs du quartier, jusqu’à", "Vente : Séminaire HaKibboutzim, 4 pièces, juillet 2026",
                       "Vente : Shai Agnon 40, 5 pièces, 2026", "Moyenne du quartier"],
                 range_txt=("90 000 à 95 000 ₪", "49 000 à 51 000 ₪"),
                 bars_small="Toutes les barres partagent la même échelle. Pondérer les terrasses à un tiers ou à la moitié de leur surface est une convention courante dans les rapports de transactions.",
                 ledger_h3="Charges et devises",
                 ledger=[("Au m² pondéré, terrasses à un tiers", "80 477 ₪", "18 000 000 / (197 + 80 / 3)"), ("Au m² pondéré, terrasses à la moitié", "75 949 ₪", "18 000 000 / (197 + 80 / 2)"),
                         ("Arnona (taxe municipale), estimation annuelle", "21 469 à 38 669 ₪", "197 m² en zone 2 jusqu’à 277 m² terrasses comprises en zone 1, au tarif au-delà de 140 m². La zone et le calcul des terrasses ouvertes restent à confirmer."),
                         ("Charges de copropriété (vaad bayit)", "Communiquées sur demande", ""),
                         ("Transactions de 10 millions ₪ et plus en 2025", "635", "dont 60 % à Tel Aviv"),
                         ("Taux représentatifs du dollar et de l’euro", "1 USD = 3,0490 ₪ · 1 EUR = 3,5169 ₪", "Banque d’Israël, 15 septembre 2026"),
                         ("Taux directeur de la Banque d’Israël et taux prime", "3,25 % · 4,75 %", "Décision du 1er septembre 2026")],
                 foot="Tous les chiffres de cette section sont des illustrations calculées, ni un devis, ni une expertise, ni un conseil."),
    market=dict(eyebrow="Le marché", h2="Le prix face au marché de Kochav HaTzafon",
                lead="Ventes de 2025 et 2026 à Kochav HaTzafon et alentour, annonces de penthouses et de duplex en cours, et données du marché de Tel Aviv. Certaines ventes sont des achats sur plan dans des programmes neufs.",
                stats=[("Prix moyen au m², Kochav HaTzafon", "juil. 2026", "Environ 49 000 à 51 000 ₪ ; les programmes neufs le long et autour de Shai Agnon atteignent 90 000 ₪ et plus"),
                       ("Prix types", "juil. 2026", "Un 4 pièces environ 4,9 millions ₪ ; des 4-5 pièces neufs proposés à partir d’environ 5,39 millions ₪"),
                       ("Loyer moyen et rendement brut du quartier", "juil. 2026", "Environ 13 900 ₪ par mois ; rendement brut d’environ 3 %"),
                       ("Transaction médiane, début 2023 à octobre 2025", "oct. 2025", "6,1 millions ₪, 4e quartier le plus élevé d’Israël (Eshkol, très probablement l’ensemble Eshkol de Sde Dov, en tête avec 7,2 millions ₪)"),
                       ("Référence du neuf à Sde Dov", "févr. 2026", "Moyenne de 79 000 à 85 000 ₪ le m² ; un penthouse au 15e étage au-delà de 103 000 ₪ le m² ; les penthouses environ 30 % au-dessus des appartements standard (contenu partenaire)"),
                       ("Cet appartement face à la moyenne du quartier", "sept. 2026", "91 371 ₪ le m² habitable, soit environ 1,8 à 1,9 fois la moyenne de 49 000 à 51 000 ₪ (calcul : 91 371 / 51 000 et 91 371 / 49 000)"),
                       ("Pondération des terrasses", "juil. 2025", "Globes a évalué un penthouse de Levi Eshkol en 2025 à 35 300 ₪ le m² en comptant la moitié de la terrasse, et à 38 800 ₪ en comptant un tiers, ce qui se pratique selon lui dans d’autres méthodes"),
                       ("Transactions de 10 millions ₪ et plus", "sept. 2026", "635 en Israël en 2025, dont 60 % à Tel Aviv"),
                       ("Logements neufs invendus, Tel Aviv", "sept. 2026", "9 725"),
                       ("Indice des prix du CBS, district de Tel Aviv", "juil. 2026", "+0,7 % en juin-juillet 2026 ; -0,9 % sur un an"),
                       ("Indice des prix de revente du CBS, Tel Aviv", "juin 2026", "-2,0 % au 2e trimestre 2026 par rapport au 1er")],
                sales_h3="Ventes et prix demandés pour comparaison",
                sales_th=["Date", "Emplacement", "Pièces", "m²", "Étage", "Prix", "Au m²"],
                sales_cap="Les ventes enregistrées figurent avant les prix demandés. Le prix au m² est calculé sur la surface publiée. Vérifiez les ventes sur le site immobilier de l’Autorité fiscale. Ceci n’est pas une expertise.",
                rents_h3="Loyers dans le quartier, pour comparaison",
                rents_th=["Date", "Emplacement", "Pièces", "m²", "Loyer / mois", "Au m²"],
                rents_cap="Loyers demandés dans des annonces d’autres biens, pas des baux signés. Le loyer au m² est calculé sur la surface publiée."),
    checks=("Avant de décider", "Les vérifications utiles", "Les questions que pose un acheteur à ce niveau de prix, et les documents à obtenir avant de négocier.",
            ["Quelles sont l’adresse exacte, le bloc et la parcelle, et quel promoteur a construit l’immeuble ? Peut-on voir le certificat d’achèvement (formulaire 4) et vérifier l’enregistrement de la copropriété au registre foncier (Tabou) ?",
             "Quelles sont la surface habitable, les surfaces de terrasses (ouvertes et couvertes) et les orientations dans les plans du permis, l’annexe du contrat de vente et l’avis d’arnona ?",
             "Qu’y a-t-il au 12e étage, au-dessus de l’appartement, et quelqu’un détient-il des droits à construire restants sur le toit ?",
             "Quels sont les charges mensuelles (salle de sport comprise) et l’arnona annuelle, et dans quelle zone d’arnona et sous quel code d’immeuble se trouve le bien ?",
             "Les 2 places de parking et la cave sont-elles enregistrées ou rattachées à l’appartement, et où se trouvent-elles ?",
             "Quels délais de contrôle et de garantie de la loi israélienne sur la vente d’appartements sont encore ouverts, et des défauts ont-ils été signalés au promoteur ?",
             "Que peut-on construire face au balcon vue mer de l’aile des enfants et face aux vues du séjour (tours de Sde Dov, Séminaire HaKibboutzim) ? Le vendeur peut-il fournir une étude d’urbanisme ?",
             "Comment l’expert du vendeur ou de l’acheteur a-t-il pondéré les terrasses, et existe-t-il une expertise récente ?",
             "Quelles écoles primaires et secondaires desservent cette adresse selon la carte scolaire municipale ?",
             "Le plan de l’appartement et le permis de construire, avec les surfaces de terrasses couvertes et ouvertes",
             "Le certificat d’occupation (formulaire 4) et l’enregistrement de la copropriété",
             "Une expertise récente et la manière dont elle pondère les terrasses",
             "Une étude d’urbanisme de ce qui pourrait être construit face aux vues"]),
    faq_eyebrow="Questions et réponses", faq_h2="Les questions à poser",
    faq_a=[("Ce bien a-t-il un potentiel de plus-value ?", "La nouvelle passerelle entre Levi Eshkol et le parc HaYarkon (environ 170 m, ouverture prévue en 2027), le quartier de Sde Dov au nord et la ligne verte du tramway (ouverture prévue en 2028) transforment le secteur. L’étude du Technion sur le parc HaYarkon a montré environ 136 dollars de plus par m² pour les logements situés à moins de 100 m du parc, et à l’étranger, des hausses de 3 % à 40 % ont été mesurées près de liaisons et de parcs, selon la distance. Ce sont des informations pour décider, pas une prévision."),
           ("Quel est le prix moyen au m² à Kochav HaTzafon ?", "Environ 49 000 à 51 000 ₪ le m² en moyenne, et 90 000 à 95 000 ₪ dans les programmes neufs et les biens d’exception (Bizportal, juillet 2026). Le neuf du quartier voisin de Sde Dov s’est vendu en moyenne environ 79 000 ₪ le m² (février 2026)."),
           ("Combien coûte un appartement à vendre à Kochav HaTzafon, au nord de Tel Aviv ?", "En juillet 2026, un 4 pièces s’y vendait autour de 4,9 millions ₪, et des 4-5 pièces neufs étaient proposés à partir d’environ 5,39 millions ₪. La transaction médiane de début 2023 à octobre 2025 était de 6,1 millions ₪. Ce mini-penthouse de 5 pièces, avec 197 m² habitables et 80 m² de terrasses, est proposé à 18 000 000 ₪.")],
    faq_b=[("Quel est le prix au m² ?", "Sur 197 m² habitables, environ 91 371 ₪ le m². En pondérant les 80 m² de terrasses à un tiers, on obtient environ 80 477 ₪, et à la moitié environ 75 949 ₪. La moyenne du quartier est de 49 000 à 51 000 ₪ le m², et les programmes neufs y atteignent 90 000 à 95 000 ₪."),
           ("Quel montant de taxe d’acquisition un acheteur paierait-il ?", "Selon le barème 2026 : environ 1 153 886 ₪ pour un seul logement (6,41 %), environ 1 678 899 ₪ pour une résidence supplémentaire ou un non-résident (9,33 %), et environ 975 976 ₪ pour un nouvel immigrant éligible (5,42 %)."),
           ("Comment rejoindre le parc HaYarkon à pied ?", "Une passerelle piétonne et cyclable d’environ 170 m, de la rue Levi Eshkol jusqu’au parc, est en construction depuis l’été 2026 et doit ouvrir en 2027."),
           ("Qu’est-ce qui pourrait changer dans la vue ?", "Le quartier de Sde Dov s’élève au nord, avec des tours de 20 à 45 étages dans le plan du centre, et trois tours de 28 étages sont prévues à l’angle de Rokach et de Namir. Certaines vues dégagées du quartier devraient être bouchées."),
           ("Combien cela fait-il en euros et en dollars ?", "Au taux représentatif du 15 septembre 2026, 18 000 000 ₪ représentent environ 5,1 millions d’euros ou 5,9 millions de dollars.")],
    broker=dict(eyebrow="L’agente", line="Real Estate by the Sea · agente immobilière agréée, licence n° " + LIC + " · " + TEL,
                cta="Organiser une visite privée", call="Appeler " + TEL, call_short="Appeler", aside="Prix et contact",
                wa="Bonjour Meital, je souhaite des détails et une visite privée : mini-penthouse à vendre à Kochav HaTzafon (nad-lan.co.il)"),
    rail=dict(lbl="Prix demandé", sub=("≈ 5 903 575 $", "≈ 5 118 144 €"), rows=[("Au m² habitable", "91 371 ₪"), ("Au m² terrasses comprises", "64 982 ₪"), ("Au m² pondéré, terrasses à un tiers", "80 477 ₪")]),
    ld=dict(desc="Cinq pièces, environ 197 m² et 80 m² de terrasses au 11e étage sur 12, dans un immeuble boutique récent de Kochav HaTzafon, au nord de Tel Aviv. 18 000 000 ₪, avec prix au m², taxe d’acquisition et comparables.",
            amen=["80 m² de terrasses", "Climatisation VRF", "Mamad (pièce sécurisée)", "2 places de parking", "Cave", "Salle de sport"],
            video="Une journée à Kochav HaTzafon : un mini-penthouse entre Tel Aviv et le parc HaYarkon"),
    langs=[("he", "עברית"), ("en", "English"), ("ru", "Русский")],
    rep_date={"Jul 2025": "Publié en juil. 2025", "Dec 2025": "Publié en déc. 2025", "Jul 2026": "Publié en juil. 2026", "Apr 2025": "Publié en avr. 2025",
              "9 Jul 2026": "9 juil. 2026", "12 Jul 2026": "12 juil. 2026", "14 Jul 2026": "14 juil. 2026", "L16 Sep 2026": "Annonce, 16 sept. 2026"},
    sales_loc=["Boulevard Levi Eshkol, plan Lamed : penthouse dans un immeuble d’environ 40 ans", "Tour FIRST de Hagag, Sde Dov", "Shai Agnon 40, Kochav HaTzafon",
               "Levi Eshkol 16, Kochav HaTzafon", "Maurizio Vitale 3, Kochav HaTzafon", "Rue Levi Eshkol (numéro non précisé), Kochav HaTzafon",
               "Projet du Séminaire HaKibboutzim, Kochav HaTzafon", "Isaac Stern 18, Lamed HaHadasha", "Tour de 25 étages, Kochav HaTzafon : penthouse sur tout l’étage",
               "Tours Sportek TLV (groupe Hagag), rue Levi Eshkol, Kochav HaTzafon", "Rue Levi Eshkol, Kochav HaTzafon : duplex neuf", "Kochav HaTzafon : penthouse duplex (rue Boney HaIr)",
               "Shai Agnon 28, Kochav HaTzafon (projet Philharmonic)", "Rue Meir Yaari, Kochav HaTzafon : penthouse duplex", "Savyonei Ramat Aviv, Kochav HaTzafon : mini-penthouse",
               "Sde Dov Eshkol : appartement de 5 pièces"],
    rents_loc=["Savyonei Ramat Aviv, Kochav HaTzafon : mini-penthouse", "Rue Meir Yaari, Kochav HaTzafon : penthouse", "Kochav HaTzafon : appartement de 5,5 pièces",
               "Kochav HaTzafon : penthouse", "Abba Kovner 13, Kochav HaTzafon : penthouse", "Projet Philharmonic, Shai Agnon 28, Kochav HaTzafon"],
)

T["ru"] = dict(
    locale="ru-RU", toc_label="На этой странице", site_link="Сайт: Meital Katzir",
    title="Мини-пентхаус на продажу в Тель-Авиве, Кохав ха-Цафон",
    meta="Мини-пентхаус в Кохав ха-Цафон, север Тель-Авива: 5 комнат, 197 м², террасы 80 м², 11-й этаж из 12, рядом парк Яркон. Цена 18 000 000 ₪.",
    kicker="Продажа · Кохав ха-Цафон, север Тель-Авива",
    h1="Мини-пентхаус, 5 комнат, на продажу в Кохав ха-Цафон, север Тель-Авива",
    dek="На этаж ниже последнего, в современном бутиковом доме в Кохав ха-Цафон: пять комнат на площади около 197 м² и 80 м² террас с видом на силуэт Тель-Авива. Квартира на продажу на севере Тель-Авива, цена 18 000 000 ₪.",
    chips=["Эксклюзивно: <a href=\"" + SITE["ru"] + "\">Meital Katzir</a>", "Бутиковый дом в 12 этажей", "Детское крыло с балконом на море"],
    plate="Кохав ха-Цафон, 11-й этаж",
    alt_base="Мини-пентхаус на продажу в Кохав ха-Цафон, Тель-Авив",
    alts={"המרפסת הראשית והנוף לתל אביב": "главная терраса и вид на Тель-Авив", "הסלון עם יציאה למרפסת": "гостиная с выходом на террасу",
          "המטבח והמקרר האינטגרלי": "кухня и встроенный холодильник", "אגף הילדים והמרפסת לים": "детское крыло и балкон с видом на море",
          "תמונה 8": "фото 8", "תמונה 9": "фото 9"},
    facts=[("Комнаты", "5"), ("Площадь", "около 197 м²"), ("Террасы", "80 м²"), ("Этаж", "11 из 12"), ("Стороны света", "от 3 до 4"),
           ("Парковка", "2 места"), ("Кладовая", "Есть"), ("Мамад (защищённая комната), лифт", "Есть")],
    toc=[("film", "Фильм"), ("tour", "Тур 360°"), ("world", "3D"), ("home", "Квартира"), ("mini", "Мини-пентхаус"), ("building", "Дом"),
         ("location", "Район"), ("future", "Планы"), ("value", "Стоимость"), ("numbers", "Цифры"), ("calc", "Калькулятор"),
         ("market", "Рынок"), ("checks", "Проверки"), ("faq", "Вопросы")],
    photos=("Фотографии", "Квартира в фотографиях"),
    film=("Фильм", "Один день в Кохав ха-Цафон",
          "Утро в районе, кофе в соседнем торговом центре, новый мост в парк Яркон, сама квартира, вечер с друзьями на террасе и цифры района. Фильм на английском языке.",
          "Квартира снята на месте. Мост, виды с высоты и сцены жизни района являются иллюстрациями и отмечены в фильме."),
    tour=("Виртуальный тур", "Комната за комнатой, в 360°",
          "Вход, гостиная, кухня, обеденная зона и терраса, днём и в сумерках. Тур собран из реальной съёмки квартиры; то, чего не видела камера, дорисовано, поэтому это иллюстрация. Интерфейс на английском языке.",
          "Квартира в 360°", "Потяните, чтобы осмотреться и перейти из комнаты в комнату", "Начать тур", "Закрыть"),
    world=("В 3D", "Из дома в парк Яркон по новому мосту",
           "Кохав ха-Цафон таким, какой он есть, по картам муниципалитета Тель-Авив-Яффо: улицы, дома и деревья, планируемый мост над бульваром Роках, газоны Гане Иехошуа и река Яркон. Пройдитесь по улицам, перейдите мост и посмотрите, сколько минут пешком до каждого кафе, школы и детского сада.",
           "Прогулка по району и по мосту", "Днём, на закате и ночью. Более 1 000 мест вокруг, со временем пути пешком. Интерфейс на иврите.",
           "Начать прогулку", "Планируемый мост над бульваром Роках в парк Яркон, 3D-иллюстрация",
           "Иллюстрация по картам муниципалитета. Мост показан по опубликованному описанию (около 170 м, ширина 6 м, открытие ожидается в 2027 году), а не по рабочим чертежам."),
    home_eyebrow="Квартира", home_h2="Город, парк и всё, что между ними",
    home=["Есть дома, которые понимают ритм Тель-Авива и при этом умеют дарить полную тишину, как только закрывается дверь. На верхних этажах района Кохав ха-Цафон, в современном элегантном бутиковом доме, находится мини-пентхаус, который по-новому определяет жизнь премиум-класса на севере города, в нескольких минутах ходьбы от зелени парка Яркон и всего, что он предлагает.",
          "Интерьер (почти 200 м²) отличают столярные работы мастера на заказ и выверенная дизайнерская линия. Сердце дома составляет просторная гостиная для приёма гостей, открытая на полностью оборудованную дизайнерскую кухню со встроенной техникой.",
          "Архитектура открывает свободный вид на силуэт Тель-Авива из родительской сюиты и жилых комнат, а из детской сюиты видна ещё и сверкающая линия моря.",
          "Настоящая жизнь начинается на большой солнечной террасе (около 74 м²), открытой на 3 стороны, с плавным переходом от комнат к открытому пространству, под современной системой кондиционирования VRF.",
          "Пять комнат на 11-м этаже из 12. Две парковки, кладовая, мамад (защищённая комната) и лифт, а в доме есть тренажёрный зал для жителей."],
    features=[("11-й этаж из 12", "Открытый вид на Тель-Авив"), ("Около 197 м²", "Пять комнат и просторная родительская сюита"),
              ("80 м² террас", "Включая балкон с видом на море у детского крыла"), ("Кондиционирование VRF", "И кухня со скрытым встроенным холодильником"),
              ("Две парковки и кладовая", "Мамад и лифт"), ("Мост в парк Яркон", "Около 170 м, открытие ожидается в 2027 году")],
    spec=[("Квартира", [("Тип и комнаты", "Мини-пентхаус, 5 комнат (по израильскому счёту, включая салон)"), ("Площадь", "Около 197 м²"),
                        ("Террасы", "80 м² в сумме, из них солнечная терраса около 74 м²"), ("Этаж", "11 из 12"), ("Стороны света", "от 3 до 4"),
                        ("Планировка", "Родительская сюита, детское крыло с балконом на море, большая гостиная")]),
          ("Отделка и сервис", [("Кухня", "Оборудованная кухня с техникой и скрытым встроенным холодильником"), ("Кондиционирование", "Система VRF мульти-сплит"),
                                ("Столярные работы", "На заказ"), ("Парковка и кладовая", "2 парковочных места и кладовая"), ("Мамад и лифт", "Есть")])],
    building=("Дом", "Бутиковый дом в двенадцать этажей", "Адрес дома, застройщик и плата за обслуживание (ваад байт) сообщаются по прямому запросу.",
              [("Расположение", "Кохав ха-Цафон, Тель-Авив-Яффо"), ("Этажей", "12"), ("Год постройки", "2022 или 2023"), ("Для жителей", "Тренажёрный зал"),
               ("Цена в долларах", "Около 5,9 млн долларов по представительскому курсу"), ("Цена в евро", "Около 5,1 млн евро по представительскому курсу")]),
    location=("Район", "Кохав ха-Цафон: парк на юге и Сде-Дов на севере",
              ["Кохав ха-Цафон ограничен бульваром Роках и парком Яркон с юга, шоссе Намир с востока, улицей Шай Агнон и районом Сде-Дов с севера и улицей Ибн Гвироль с запада. Район застраивался в основном в 1990-х и 2000-х годах домами от 8 до 12 этажей вокруг центрального парка, рядом с жилыми башнями и бутиковыми домами. По данным, опубликованным Mako, медианная сделка здесь с 2023 года по октябрь 2025 года составила 6,1 млн ₪, это четвёртый результат в Израиле.",
               "Парк Яркон площадью около 3 750 дунамов (375 гектаров) вместе со Спортеком граничит с районом вдоль бульвара Роках, а в конце парка находится Тель-Авивский порт, зона отдыха площадью 220 дунамов. На углу Роках и Намир проект Семинар ха-Кибуцим предусматривает три жилые башни по 28 этажей на 450 квартир.",
               "Южный участок Зелёной линии трамвая планируют открыть в 2028 году, а всю линию в 2030 году; станция Рединг будет на новом мосту к северу от бульвара Роках. Новый пешеходно-велосипедный мост длиной 180 м через Яркон открылся в мае 2026 года."],
              "Школы", [("Начальная школа Кохав ха-Цафон", "Государственная школа в районе, около 82 учеников в параллели; школьный округ дома нужно уточнить"),
                        ("Ирони Каф-Далет (24), имени Амоса Оза", "Указана в районе, около 47 учеников в параллели; школьный округ нужно уточнить")],
              "Транспорт", [("Зелёная линия трамвая, станция Рединг", "Строится; южный участок ожидается в 2028 году, вся линия в 2030 году; станция Рединг будет к северу от бульвара Роках, на новом мосту Зелёной линии (крытая станция высотой 12 м)"),
                            ("Пешеходно-велосипедный мост Роках-Леви Эшколь в парк Яркон", "Строится с лета 2026 года, открытие ожидается в 2027 году; длина около 170 м, ширина 6 м, доступен без лифтов"),
                            ("Мост через Яркон (от парка Яркон к Ибн Гвироль)", "Действует с мая 2026 года; 180 на 6 м")],
              "Подробнее: <a href=\"" + BASE + "/ru/north-tel-aviv/\">север Тель-Авива: районы, квартиры и цены</a> · <a href=\"" + BASE + "/ru/sde-dov/\">Сде-Дов: новые проекты и цены</a>"),
    future=("Планы", "Что планируется рядом", "Опубликованные планы и работы и что они могут означать для покупателя. По опубликованным данным; не заменяет проверку в отделе планирования и строительства муниципалитета.",
            [("Мост Роках-Леви Эшколь в парк Яркон", "Прямой пешеходный и велосипедный выход с улицы Леви Эшколь в парк с 2027 года, а до тех пор работы на бульваре Роках. План утверждён в январе 2022 года, на него выделено 35 млн ₪."),
             ("Проект Семинар ха-Кибуцим, угол бульвара Роках и шоссе Намир", "Около 55 дунамов: три башни по 28 этажей на 450 квартир и три 6-этажных дома вдоль улицы Маурицио Витале, до 1 550 м² торговых площадей и 4 600 м² общественных зданий. Первый этап (134 квартиры и новое здание колледжа) займёт около 5 лет; финансирование около 1,7 млрд ₪. Годы строительства и новые башни на юго-восточном углу района."),
             ("Башни района Сде-Дов", "Центральный план, возражения против которого отклонены 3 февраля 2025 года, предусматривает 7 128 квартир в башнях по 20 и 45 этажей; большинство квартир района ожидается в течение от 3 до 6 лет. Башни на севере могут изменить силуэт города и вид на море."),
             ("Зелёная линия трамвая", "Удобный рельсовый транспорт от станции Рединг к северу от бульвара Роках после открытия (южный участок в 2028 году, вся линия в 2030 году); до тех пор работы вокруг Роках и Яркона."),
             ("Территория электростанции Рединг", "Выработка электроэнергии прекращается по решению 2024 года: часть территории перейдёт под городское использование и пляж, остальное останется под хранилища и подводный кабель; план сохранения превращает Рединг А в музей, центр для посетителей и площадку для мероприятий. Сроки нужно уточнить.")]),
    value=("Стоимость", "Мост, парк и район: как это влияет на стоимость",
           "Что известно о мосте, что показали исследования о влиянии парков и пешеходных связей на цены жилья и что планируется вокруг. Информация для решения, а не прогноз.",
           [("Мост в парк Яркон", "Длина около 170 м, ширина 6 м: 3 м для пешеходов и 3 м для велосипедистов, бамбуковый настил и светодиодная подсветка в перилах, без ступеней и без лифтов. Работы начались в июне 2026 года, открытие ожидается в 2027 году (Maariv, Walla, Bizportal, 03.08.2026). Мост входит в планируемую ось север-юг со вторым мостом через реку Яркон."),
            ("Исследование о парке Яркон", "Исследование Техниона (Шефер и Закаи, 2003) показало, что квартиры в пределах 100 м от парка Яркон стоили примерно на 136 долларов за м² дороже, чем квартиры на расстоянии от 100 до 1 500 м."),
            ("Парки и пешеходные связи в мире", "Рядом с известными городскими парками соседнее жильё дорожало: около 5% вокруг Гринвэя в Бостоне, около 20% вокруг Хай-Лайн в Нью-Йорке, около 23% вокруг парка Клайд Уоррен в Далласе и от 30% до 40% вокруг Миллениум-парка в Чикаго (HR&A, 2014). Обзор 20 исследований показал от 3% до 5% для домов у пешеходных и велосипедных маршрутов (Crompton и Nicholls, 2019). Эффект сильнее всего рядом со связью и ослабевает с расстоянием."),
            ("Сде-Дов, к северу от района", "Около 16 000 квартир, около 365 дунамов парков и башни до 40 этажей по утверждённому плану. Новостройки района продавались в среднем примерно по 79 000 ₪ за м² (февраль 2026)."),
            ("Зелёная линия трамвая", "Около 39 км и 62 станции, от Ришон-ле-Циона до Герцлии; по сообщениям, открытие планируется в 2028 году."),
            ("Цены в районе сегодня", "В среднем от 49 000 до 51 000 ₪ за м² в Кохав ха-Цафон и от 90 000 до 95 000 ₪ за м² в новых проектах и особых объектах (Bizportal, июль 2026).")],
           "Сценарии только для наглядности, не прогноз и не обещание", ("Сценарий", "Изменение стоимости", "Стоимость", "За м²"),
           "Расчёт: 18 000 000 ₪, умноженные на ставку сценария, на 197 м² площади. Налог на покупку и услуги адвоката сами по себе составляют от 7% до 9,9% цены, поэтому сценарии лучше читать в долгосрочной перспективе. Это не инвестиционная консультация; посоветуйтесь с оценщиком, адвокатом и налоговым консультантом."),
    numbers=dict(eyebrow="Цифры", h2="18 000 000 ₪: расчёт покупателя", small="Цена 18 000 000 ₪, рассчитанная по налоговым и ипотечным правилам, опубликованным до 16 сентября 2026 года.",
                 kpis=[("Цена", "18 000 000 ₪", "≈ 5 903 575 $ · ≈ 5 118 144 €"), ("Цена за м²", "91 371 ₪", ""),
                       ("Средняя цена за м², Кохав ха-Цафон", "51 000 ₪", "от 49 000 до 51 000 ₪, Bizportal, июль 2026"), ("Максимальная ипотека, единственное жильё", "13 500 000 ₪", "75% стоимости, Банк Израиля")],
                 seg_h3="Сколько это стоит для разных покупателей",
                 seg_labels=["Единственное жильё, житель Израиля", "Дополнительное жильё или нерезидент", "Новый репатриант"],
                 rows=["Налог на покупку", "Максимальная ипотека", "Минимальный собственный капитал", "Собственный капитал и налог"],
                 notes=[["Эффективная ставка 6,41%", "75% стоимости", "", "Без учёта адвоката, оценки и прочих расходов"],
                        ["Эффективная ставка 9,33%", "50% для инвестиционного жилья или покупателя без израильского гражданства", "", "Без учёта адвоката, оценки и прочих расходов"],
                        ["Эффективная ставка 5,42%. Право на льготу: от года до репатриации до семи лет после неё", "75% стоимости", "", "Без учёта адвоката, оценки и прочих расходов"]],
                 seg_small="Шкала налога на покупку заморожена до 15 января 2028 года. Ставки 8% и 10% для дополнительного жилья действуют по временному распоряжению до начала 2027 года. Не налоговая консультация.",
                 bars_h3="Цена за м² на фоне рынка",
                 bars=["Эта квартира, на 197 м²", "Эта квартира, террасы с весом в треть", "Новые проекты в районе, до", "Сделка: Семинар ха-Кибуцим, 4 комнаты, июль 2026",
                       "Сделка: Шай Агнон 40, 5 комнат, 2026", "Средняя по району"],
                 range_txt=("от 90 000 до 95 000 ₪", "от 49 000 до 51 000 ₪"),
                 bars_small="Все полосы в одном масштабе. Учёт террас с весом в треть или половину площади принят в отчётах о сделках.",
                 ledger_h3="Расходы и курсы валют",
                 ledger=[("За взвешенный м², террасы с весом в треть", "80 477 ₪", "18 000 000 / (197 + 80 / 3)"), ("За взвешенный м², террасы с весом в половину", "75 949 ₪", "18 000 000 / (197 + 80 / 2)"),
                         ("Арнона (муниципальный налог), оценка в год", "от 21 469 до 38 669 ₪", "От 197 м² в зоне 2 до 277 м² с террасами в зоне 1, по ставке для площади свыше 140 м². Зону и порядок учёта открытых террас нужно уточнить."),
                         ("Плата за обслуживание дома (ваад байт)", "По запросу", ""),
                         ("Сделки от 10 млн ₪ в 2025 году", "635", "из них 60% в Тель-Авиве"),
                         ("Представительские курсы доллара и евро", "1 USD = 3,0490 ₪ · 1 EUR = 3,5169 ₪", "Банк Израиля, 15 сентября 2026"),
                         ("Ставка Банка Израиля и прайм", "3,25% · 4,75%", "Решение от 1 сентября 2026")],
                 foot="Все цифры в этом разделе являются расчётными иллюстрациями, а не предложением, оценкой или консультацией."),
    market=dict(eyebrow="Рынок", h2="Цена на фоне рынка Кохав ха-Цафон",
                lead="Сделки 2025 и 2026 годов в Кохав ха-Цафон и рядом, текущие объявления о пентхаусах и дуплексах и данные рынка Тель-Авива. Часть сделок заключена на стадии строительства в новых проектах.",
                stats=[("Средняя цена за м², Кохав ха-Цафон", "июль 2026", "Около 49 000-51 000 ₪; новые проекты на улице Шай Агнон и рядом достигают 90 000 ₪ и выше"),
                       ("Типичные цены", "июль 2026", "4-комнатная квартира около 4,9 млн ₪; новые квартиры на 4-5 комнат предлагаются примерно от 5,39 млн ₪"),
                       ("Средняя аренда и валовая доходность по району", "июль 2026", "Около 13 900 ₪ в месяц; валовая доходность около 3%"),
                       ("Медианная сделка, с начала 2023 по октябрь 2025", "окт. 2025", "6,1 млн ₪, 4-й по уровню район Израиля (первым идёт Эшколь, скорее всего комплекс Эшколь в Сде-Дов, 7,2 млн ₪)"),
                       ("Ориентир новостроек Сде-Дов", "февр. 2026", "В среднем 79 000-85 000 ₪ за м²; пентхаус на 15-м этаже дороже 103 000 ₪ за м²; пентхаусы примерно на 30% дороже стандартных квартир (партнёрский материал)"),
                       ("Эта квартира на фоне средней цены района", "сент. 2026", "91 371 ₪ за м², примерно в 1,8-1,9 раза выше средних 49 000-51 000 ₪ (расчёт: 91 371 / 51 000 и 91 371 / 49 000)"),
                       ("Как учитывают террасы", "июль 2025", "Globes оценил пентхаус на Леви Эшколь в 2025 году в 35 300 ₪ за м² при учёте половины террасы и в 38 800 ₪ при учёте трети, что, по его словам, принято в других методиках"),
                       ("Сделки от 10 млн ₪", "сент. 2026", "635 в Израиле в 2025 году, из них 60% в Тель-Авиве"),
                       ("Непроданные новые квартиры, Тель-Авив", "сент. 2026", "9 725"),
                       ("Индекс цен ЦСБ, Тель-Авивский округ", "июль 2026", "+0,7% за июнь-июль 2026; -0,9% за год"),
                       ("Индекс цен вторичного жилья ЦСБ, Тель-Авив", "июнь 2026", "-2,0% во 2-м квартале 2026 года к 1-му")],
                sales_h3="Сделки и цены предложения для сравнения",
                sales_th=["Дата", "Адрес", "Комнат", "м²", "Этаж", "Цена", "За м²"],
                sales_cap="Зарегистрированные сделки идут перед ценами предложения. Цена за м² рассчитана по опубликованной площади. Проверяйте сделки на сайте недвижимости Налогового управления. Это не оценка.",
                rents_h3="Аренда в районе, для сравнения",
                rents_th=["Дата", "Адрес", "Комнат", "м²", "Аренда в месяц", "За м²"],
                rents_cap="Запрашиваемая аренда из объявлений о других объектах, а не подписанные договоры. Аренда за м² рассчитана по опубликованной площади."),
    checks=("Перед решением", "Что стоит проверить", "Вопросы, которые задаёт покупатель на этом уровне цен, и документы, которые нужно получить до переговоров.",
            ["Какой точный адрес, блок и участок (гуш и хелка), и какой застройщик построил дом? Можно ли увидеть акт о завершении строительства (форма 4) и проверить регистрацию кондоминиума в Табу?",
             "Какие жилая площадь, площади террас (открытых и крытых) и стороны света указаны в планах разрешения, в приложении к договору купли-продажи и в счёте арноны?",
             "Что находится на 12-м этаже над квартирой, и есть ли у кого-то оставшиеся права на застройку крыши?",
             "Какова ежемесячная плата за обслуживание (включая тренажёрный зал) и годовая арнона, в какой зоне арноны и под каким кодом дома числится квартира?",
             "Зарегистрированы ли 2 парковочных места и кладовая или закреплены ли они за квартирой, и где они находятся?",
             "Какие сроки проверки и гарантии по израильскому закону о продаже квартир ещё не истекли, и сообщалось ли застройщику о дефектах?",
             "Что можно построить напротив балкона детского крыла с видом на море и напротив видов из гостиной (башни Сде-Дов, Семинар ха-Кибуцим)? Может ли продавец предоставить градостроительную проверку?",
             "Как оценщик продавца или покупателя учёл террасы, и есть ли свежая оценка?",
             "Какие начальные и средние школы обслуживают этот адрес по муниципальным школьным округам?",
             "План квартиры и разрешение на строительство, с площадями крытых и открытых террас",
             "Разрешение на заселение (форма 4) и регистрация кондоминиума",
             "Свежая оценка и то, как в ней учтены террасы",
             "Градостроительная проверка того, что может быть построено напротив видов"]),
    faq_eyebrow="Вопросы и ответы", faq_h2="Вопросы, которые стоит задать",
    faq_a=[("Есть ли у квартиры потенциал роста стоимости?", "Новый мост от Леви Эшколь в парк Яркон (около 170 м, открытие ожидается в 2027 году), район Сде-Дов на севере и Зелёная линия трамвая (открытие планируется в 2028 году) меняют этот район. Исследование Техниона о парке Яркон показало около 136 долларов прибавки за м² для квартир в пределах 100 м от парка, а в мире рядом с пешеходными связями и парками измеряли рост от 3% до 40%, в зависимости от расстояния. Это информация для решения, а не прогноз."),
           ("Какая средняя цена за м² в Кохав ха-Цафон?", "В среднем от 49 000 до 51 000 ₪ за м² и от 90 000 до 95 000 ₪ в новых проектах и особых объектах (Bizportal, июль 2026). Новостройки соседнего района Сде-Дов продавались в среднем примерно по 79 000 ₪ за м² (февраль 2026)."),
           ("Сколько стоит купить квартиру в Тель-Авиве, в районе Кохав ха-Цафон?", "В июле 2026 года 4-комнатная квартира здесь стоила около 4,9 млн ₪, а новые квартиры на 4-5 комнат предлагались примерно от 5,39 млн ₪. Медианная сделка с начала 2023 года по октябрь 2025 года составила 6,1 млн ₪. Этот мини-пентхаус на 5 комнат, 197 м² и 80 м² террас продаётся за 18 000 000 ₪.")],
    faq_b=[("Какая цена за м²?", "При 197 м² около 91 371 ₪ за м². Если учитывать 80 м² террас с весом в треть, получается около 80 477 ₪, а с весом в половину около 75 949 ₪. Средняя по району от 49 000 до 51 000 ₪ за м², а новые проекты здесь доходят до 90 000-95 000 ₪."),
           ("Какой налог на покупку заплатит покупатель?", "По шкале 2026 года: около 1 153 886 ₪ за единственное жильё (6,41%), около 1 678 899 ₪ за дополнительное жильё или для нерезидента (9,33%) и около 975 976 ₪ для нового репатрианта с правом на льготу (5,42%)."),
           ("Как дойти пешком до парка Яркон?", "Пешеходно-велосипедный мост длиной около 170 м от улицы Леви Эшколь в парк строится с лета 2026 года и должен открыться в 2027 году."),
           ("Что может измениться в виде из окон?", "На севере растёт район Сде-Дов с башнями от 20 до 45 этажей по центральному плану, а на углу Роках и Намир планируются три башни по 28 этажей. Часть открытых видов в районе, вероятно, будет закрыта."),
           ("Сколько это в долларах и евро?", "По представительскому курсу на 15 сентября 2026 года 18 000 000 ₪ составляют около 5,9 млн долларов или около 5,1 млн евро.")],
    broker=dict(eyebrow="Риелтор", line="Real Estate by the Sea · лицензированный риелтор, лицензия № " + LIC + " · " + TEL,
                cta="Записаться на просмотр", call="Позвонить " + TEL, call_short="Позвонить", aside="Цена и контакты",
                wa="Здравствуйте, Meital. Хочу узнать подробности и записаться на просмотр: мини-пентхаус на продажу в Кохав ха-Цафон (nad-lan.co.il)"),
    rail=dict(lbl="Цена", sub=("≈ 5 903 575 $", "≈ 5 118 144 €"), rows=[("За м²", "91 371 ₪"), ("За м² с террасами", "64 982 ₪"), ("За взвешенный м², террасы с весом в треть", "80 477 ₪")]),
    ld=dict(desc="Пять комнат, около 197 м² и 80 м² террас на 11-м этаже из 12, в современном бутиковом доме в Кохав ха-Цафон на севере Тель-Авива. 18 000 000 ₪, с ценой за м², налогом на покупку и сравнением с рынком.",
            amen=["Террасы 80 м²", "Кондиционирование VRF", "Мамад (защищённая комната)", "2 парковочных места", "Кладовая", "Тренажёрный зал"],
            video="Один день в Кохав ха-Цафон: мини-пентхаус между Тель-Авивом и парком Яркон"),
    langs=[("he", "עברית"), ("en", "English"), ("fr", "Français")],
    rep_date={"Jul 2025": "Опубл. в июле 2025", "Dec 2025": "Опубл. в декабре 2025", "Jul 2026": "Опубл. в июле 2026", "Apr 2025": "Опубл. в апреле 2025",
              "9 Jul 2026": "09.07.2026", "12 Jul 2026": "12.07.2026", "14 Jul 2026": "14.07.2026", "L16 Sep 2026": "Объявление, 16.09.2026"},
    sales_loc=["Бульвар Леви Эшколь, план Ламед: пентхаус в доме около 40 лет", "Башня FIRST группы Хагаг, Сде-Дов", "Шай Агнон 40, Кохав ха-Цафон",
               "Леви Эшколь 16, Кохав ха-Цафон", "Маурицио Витале 3, Кохав ха-Цафон", "Улица Леви Эшколь (номер дома не указан), Кохав ха-Цафон",
               "Проект Семинар ха-Кибуцим, Кохав ха-Цафон", "Исаак Стерн 18, Ламед ха-Хадаша", "25-этажная башня, Кохав ха-Цафон: пентхаус на весь этаж",
               "Башни Sportek TLV (группа Хагаг), улица Леви Эшколь, Кохав ха-Цафон", "Улица Леви Эшколь, Кохав ха-Цафон: новый дуплекс", "Кохав ха-Цафон: пентхаус-дуплекс (улица Боней ха-Ир)",
               "Шай Агнон 28, Кохав ха-Цафон (проект Филармония)", "Улица Меир Яари, Кохав ха-Цафон: пентхаус-дуплекс", "Савьоней Рамат-Авив, Кохав ха-Цафон: мини-пентхаус",
               "Сде-Дов Эшколь: 5-комнатная квартира"],
    rents_loc=["Савьоней Рамат-Авив, Кохав ха-Цафон: мини-пентхаус", "Улица Меир Яари, Кохав ха-Цафон: пентхаус", "Кохав ха-Цафон: квартира на 5,5 комнаты",
               "Кохав ха-Цафон: пентхаус", "Абба Ковнер 13, Кохав ха-Цафон: пентхаус", "Проект Филармония, Шай Агнон 28, Кохав ха-Цафон"],
)

# the shared numbers of the two comparison tables (the English page, 16.9.2026): date key, rooms, sqm, floor, price, per sqm
SALES = [("Jul 2025", "", "165", "7", 7950000, 48182), ("Dec 2025", "", "260", "39", 31041000, 119388), ("Jul 2026", "5", "133.5", "5", 10050000, 75281),
         ("Jul 2026", "7", "135", "16", 10000000, 74074), ("Jul 2026", "4", "121", "1", 7100000, 58678), ("9 Jul 2026", "4.5", "125", "13", 10000000, 80000),
         ("12 Jul 2026", "4", "126", "", 9550000, 75793), ("14 Jul 2026", "5", "123", "6", 7550000, 61382), ("Apr 2025", "", "180", "", 37000000, 205556),
         ("L16 Sep 2026", "6", "192", "20", 20000000, 104167), ("L16 Sep 2026", "6.5", "200", "2", 15500000, 77500), ("L16 Sep 2026", "5", "157", "", 12500000, 79618),
         ("L16 Sep 2026", "4", "130", "3", 11900000, 91538), ("L16 Sep 2026", "5", "207", "7", 10450000, 50483), ("L16 Sep 2026", "5.5", "135", "11", 10500000, 77778),
         ("L16 Sep 2026", "5", "146", "10", 9200000, 63014)]
RENTS = [("5.5", "280", 37500, 134), ("4", "165", 25000, 152), ("5.5", "230", 27000, 117), ("5", "130", 18000, 138), ("5.5", "160", 15000, 94), ("4", "103", 21300, 207)]

# the calculator and the mini penthouse test (seo_tools.py) in French and Russian
ST.TX["fr"] = {
    "m_eyebrow": "Mini-penthouse", "m_h2": "Ce qui fait de cet appartement un vrai mini-penthouse",
    "m_lead": "En Israël, un mini-penthouse est un appartement situé à l’un des derniers étages, avec une terrasse ensoleillée bien plus grande qu’un balcon ordinaire. Le penthouse est l’appartement du dernier étage lui-même, généralement avec un toit-terrasse. La loi n’en donne aucune définition : chaque bien mérite donc d’être vérifié selon les mêmes critères.",
    "m_test": [("11e étage sur 12", "L’un des deux derniers étages de l’immeuble, avec une vue dégagée sur la ligne d’horizon de Tel Aviv."),
               ("Une terrasse ensoleillée d’environ 74 m²", "Environ trois fois les 25 m² que le marché attend habituellement d’un mini-penthouse. Avec les autres balcons, environ 80 m² en extérieur."),
               ("Ouverte sur 3 côtés", "La terrasse s’ouvre dans trois directions et prolonge le séjour et la cuisine vers l’extérieur."),
               ("197 m² habitables, cinq pièces", "Une suite parentale, une suite enfants avec vue mer, un mamad, deux places de parking et une cave.")],
    "m_cap": "Penthouse, mini-penthouse et les types intermédiaires",
    "m_th": ["Type", "Où dans l’immeuble", "Espace extérieur", "À vérifier avant d’acheter"],
    "m_rows": [("Penthouse", "Le dernier étage", "Un grand toit-terrasse, parfois la plus grande partie du toit", "Quelle partie du toit est rattachée à l’appartement au registre foncier (Tabou) et dans le règlement de copropriété"),
               ("Mini-penthouse", "L’un des derniers étages, sous le penthouse", "Une grande terrasse ensoleillée, en général 25 m² ou plus", "La surface de la terrasse dans le permis et dans le contrat, pas seulement dans l’annonce"),
               ("Appartement sur le toit", "Sur le toit, souvent dans un immeuble ancien", "Un toit rattaché, parfois avec des droits à construire", "Les droits à construire sur le toit, et les ajouts construits sans permis"),
               ("Duplex", "Deux niveaux à l’intérieur de l’appartement", "Selon l’étage", "L’escalier intérieur, et la surface de chaque niveau"),
               ("Appartement avec jardin", "Le rez-de-chaussée", "Un jardin rattaché", "Le rattachement du jardin dans le règlement de copropriété, l’intimité et l’évacuation des eaux")],
    "m_note": "Le droit israélien ne donne pas une seule définition ; la distinction suit ici l’usage du marché. Ce qui compte, c’est ce qu’indiquent l’extrait du registre foncier (Tabou), le règlement de copropriété et le permis de construire.",
    "m_links": "",  # as on the English page; the French reading links sit once, under the location section
    "c_eyebrow": "Calculateur", "c_h2": "Calculateur mini-penthouse : prix au m², terrasses et taxe d’acquisition",
    "c_lead": "Dans un mini-penthouse, une grande partie de la valeur se trouve sur la terrasse. Les experts immobiliers israéliens comptent généralement un mètre de terrasse comme une fraction de mètre habitable, entre 0,2 et 0,5. Le calculateur s’ouvre avec les chiffres de cet appartement, et l’on peut y saisir n’importe quel autre penthouse.",
    "c_in": ["Prix (₪)", "Surface habitable (m²)", "Terrasses (m²)", "Poids d’un mètre de terrasse", "Acheteur", "Avocat (%), hors TVA"],
    "c_kinds": [("single", "Seul logement"), ("extra", "Résidence supplémentaire"), ("foreign", "Non-résident"), ("oleh", "Nouvel immigrant (olé)")],
    "c_out": ["Prix au m² habitable", "Surface pondérée", "Prix au m² pondéré", "Taxe d’acquisition", "Avocat, TVA comprise", "Coût total"],
    "c_unit": "m²", "c_cur": "₪", "c_third": "un tiers",
    "c_market": "Pour comparaison à Kochav HaTzafon : environ 49 000 à 51 000 ₪ le m² en moyenne, et 90 000 à 95 000 ₪ dans les programmes neufs et les biens d’exception (Bizportal, juillet 2026).",
    "c_note": "Barème de la taxe d’acquisition (mas rehisha) selon l’Autorité fiscale israélienne, en vigueur du 16 janvier 2025 au 15 janvier 2028. Les non-résidents relèvent du barème de la résidence supplémentaire. Illustration, pas un conseil fiscal ; le montant final est fixé par l’Autorité fiscale.",
    "toc_m": "Mini-penthouse", "toc_c": "Calculateur",
    "faq": [("Quelle est la différence entre un penthouse et un mini-penthouse ?", "Le penthouse se trouve au dernier étage de l’immeuble, généralement avec un toit-terrasse. Le mini-penthouse se trouve à l’un des derniers étages en dessous, avec une terrasse ensoleillée bien plus grande qu’un balcon ordinaire, en général 25 m² ou plus. La loi israélienne n’en donne aucune définition ; le registre foncier, le règlement de copropriété et le permis font foi."),
            ("Cet appartement est-il vraiment un mini-penthouse ?", "Oui, selon tous les critères habituels : 11e étage sur 12, une terrasse ensoleillée d’environ 74 m² (environ trois fois 25 m²) et environ 80 m² avec les autres balcons, 197 m² habitables et cinq pièces. Avec les terrasses pondérées à un tiers, le prix revient à environ 80 477 ₪ le m².")],
    "app": "Calculateur mini-penthouse : prix au m², terrasses et taxe d’acquisition",
}
ST.TX["ru"] = {
    "m_eyebrow": "Мини-пентхаус", "m_h2": "Почему это настоящий мини-пентхаус",
    "m_lead": "В Израиле мини-пентхаусом называют квартиру на одном из верхних этажей с солнечной террасой, намного больше обычного балкона. Пентхаус находится на самом верхнем этаже, обычно с террасой на крыше. Закон не даёт определения, поэтому каждую квартиру стоит проверять по одним и тем же признакам.",
    "m_test": [("11-й этаж из 12", "Один из двух верхних этажей дома, с открытым видом на силуэт Тель-Авива."),
               ("Солнечная терраса около 74 м²", "Примерно втрое больше 25 м², которые рынок обычно ожидает от мини-пентхауса. Вместе с другими балконами около 80 м² открытого пространства."),
               ("Открыта на 3 стороны", "Терраса выходит на три стороны и продолжает гостиную и кухню наружу."),
               ("197 м², пять комнат", "Родительская сюита, детская сюита с видом на море, мамад, две парковки и кладовая.")],
    "m_cap": "Пентхаус, мини-пентхаус и другие типы квартир",
    "m_th": ["Тип", "Где в доме", "Открытое пространство", "Что проверить перед покупкой"],
    "m_rows": [("Пентхаус", "Верхний этаж", "Большая терраса на крыше, иногда почти вся крыша", "Какая часть крыши закреплена за квартирой в выписке из Табу и в уставе дома"),
               ("Мини-пентхаус", "Один из верхних этажей, под пентхаусом", "Большая солнечная терраса, обычно от 25 м²", "Площадь террасы в разрешении на строительство и в договоре, а не только в объявлении"),
               ("Квартира на крыше", "На крыше, часто в старом доме", "Прилегающая крыша, иногда с правами на застройку", "Права на застройку крыши и пристройки без разрешения"),
               ("Дуплекс", "Два уровня внутри квартиры", "Зависит от этажа", "Внутренняя лестница и площадь каждого уровня"),
               ("Квартира с садом", "Первый этаж", "Прилегающий сад", "Закрепление сада в уставе дома, приватность и дренаж")],
    "m_note": "Единого определения в израильском законе нет; здесь различие проведено по рыночной практике. Решающее значение имеют выписка из Табу, устав кондоминиума и разрешение на строительство.",
    "m_links": "",
    "c_eyebrow": "Калькулятор", "c_h2": "Калькулятор мини-пентхауса: цена за м², террасы и налог на покупку",
    "c_lead": "В мини-пентхаусе значительная часть стоимости приходится на террасу. Израильские оценщики обычно считают метр террасы долей жилого метра, от 0,2 до 0,5. Калькулятор открывается с данными этой квартиры, и в него можно ввести любой другой пентхаус.",
    "c_in": ["Цена (₪)", "Площадь (м²)", "Террасы (м²)", "Вес метра террасы", "Покупатель", "Адвокат (%), без НДС"],
    "c_kinds": [("single", "Единственное жильё"), ("extra", "Дополнительное жильё"), ("foreign", "Нерезидент Израиля"), ("oleh", "Новый репатриант")],
    "c_out": ["Цена за м²", "Взвешенная площадь", "Цена за взвешенный м²", "Налог на покупку", "Адвокат, с НДС", "Итого"],
    "c_unit": "м²", "c_cur": "₪", "c_third": "треть",
    "c_market": "Для сравнения в Кохав ха-Цафон: в среднем от 49 000 до 51 000 ₪ за м² и от 90 000 до 95 000 ₪ в новых проектах и особых объектах (Bizportal, июль 2026).",
    "c_note": "Шкала налога на покупку (мас рехиша) по данным Налогового управления Израиля, действует с 16.1.2025 по 15.1.2028. Для нерезидентов действует шкала дополнительного жилья. Расчёт для наглядности, не налоговая консультация; окончательную сумму определяет Налоговое управление.",
    "toc_m": "Мини-пентхаус", "toc_c": "Калькулятор",
    "faq": [("Чем пентхаус отличается от мини-пентхауса?", "Пентхаус находится на верхнем этаже дома, обычно с террасой на крыше. Мини-пентхаус расположен на одном из верхних этажей под ним и имеет солнечную террасу намного больше обычного балкона, как правило от 25 м². В израильском законе определения нет; решают выписка из Табу, устав дома и разрешение на строительство."),
            ("Эта квартира действительно мини-пентхаус?", "Да, по всем принятым признакам: 11-й этаж из 12, солнечная терраса около 74 м² (примерно втрое больше 25 м²) и около 80 м² вместе с другими балконами, 197 м² площади и пять комнат. Если считать террасы с весом в треть, цена составляет около 80 477 ₪ за м².")],
    "app": "Калькулятор мини-пентхауса: цена за м², террасы и налог на покупку",
}
for _l in ("fr", "ru"):  # the same typography inside the shared blocks
    _t = ST.TX[_l]
    for _k, _v in list(_t.items()):
        if isinstance(_v, str) and _k != "m_links":
            _t[_k] = ty(_v, _l)
    _t["m_test"] = [(ty(a, _l), ty(b, _l)) for a, b in _t["m_test"]]
    _t["m_rows"] = [tuple(ty(x, _l) for x in r) for r in _t["m_rows"]]
    _t["faq"] = [(ty(a, _l), ty(b, _l)) for a, b in _t["faq"]]


# ------------------------------------------------------------------ pieces taken from the live English page
def cut(pattern, s=SRC, flags=re.S):
    m = re.search(pattern, s, flags)
    assert m, pattern
    return m.group(0)


def styles(lang):
    css = SRC[SRC.index("<style>"):SRC.index("</style>", SRC.index('<style id="nlx-kochav-add">')) + len("</style>")]
    # the English page scopes its frame rules to page-id-7812; here they follow the article itself (and the page id once known)
    sel = ["body:has(#nlx-L07-" + lang + ")"] + (["body.page-id-%d" % PAGE_ID[lang]] if lang in PAGE_ID else [])
    css = re.sub(r"body\.page-id-7812 ([^,{]+)", lambda m: ",".join(x + " " + m.group(1) for x in sel), css)
    assert "7812" not in css
    extra = ('.nlx[lang="' + lang + '"] .nlx-kicker,.nlx[lang="' + lang + '"] .nlx-eyebrow{text-transform:uppercase;letter-spacing:.09em;font-size:12px}\n'
             ".nlx .nlx-toc .nlx-lang--more{margin-inline-start:0}\n")
    return css.replace("</style>", extra + "</style>", 1)


ART = SRC[SRC.index('<article class="nlx"'):]   # the markup only (the stylesheet's comments hold sample markup too)
WALK_JS = cut(r'<script>\(function\(\)\{if\(window\.__nlxWalk\).*?</script>', ART)
GALLERY = cut(r'<div class="nlx-gallery">.*?</div></section>', ART)[:-len("</section>")]
COVER = cut(r'<figure class="nlx-plate nlx-plate--photo".*?</figure>', ART)
EN_LD = json.loads(cut(r'<script type="application/ld\+json">(.*?)</script>').split(">", 1)[1].rsplit("</script>", 1)[0])
EN_LISTING = next(g for g in EN_LD["@graph"] if g["@type"] == "RealEstateListing")


def localise_alts(s, t):
    def fix(m):
        he = m.group(1)
        tail = he.split("כוכב הצפון, ", 1)[-1]
        return 'alt="' + esc(t["alt_base"] + ", " + t["alts"].get(tail, tail)) + '"'
    out = re.sub(r'alt="([^"]*)"', fix, s)
    assert not re.search(r"[֐-׿]", out), "a Hebrew alt is left"
    return out


# ------------------------------------------------------------------ the page
def sec_head(e, h2, lead=None, lang="fr", small=False):
    tail = ""
    if lead:
        tail = '<p class="' + ("nlx-small" if small else "nlx-lead") + '">' + nums(lead, lang) + "</p>"
    return '<div class="nlx-sec-head"><p class="nlx-eyebrow">' + esc(e) + '</p><h2 class="nlx-h2">' + nums(h2, lang) + "</h2>" + tail + "</div>"


def wa_link(t):
    return "https://wa.me/" + WA_NUM + "?text=" + urllib.parse.quote(t["broker"]["wa"], safe="")


SVG_WA = cut(r'<svg viewBox="0 0 24 24" aria-hidden="true" focusable="false"><path fill="currentColor".*?</svg>', ART)
SVG_TEL = cut(r'<svg viewBox="0 0 24 24" aria-hidden="true" focusable="false"><path fill="none".*?</svg>', ART)


def build(lang):
    t = T[lang]
    s = "-L07-" + lang
    L = lambda x: nums(x, lang)  # noqa: E731
    out = ["<!-- wp:html -->", styles(lang), "",
           '<article class="nlx" lang="' + lang + '" dir="ltr" id="nlx' + s + '" data-listing="L07">', '<div class="nlx-wrap">']
    # masthead
    cover = localise_alts(COVER, t)
    cover = re.sub(r'<span class="nlx-plate-name">[^<]*</span>', '<span class="nlx-plate-name">' + L(t["plate"]) + "</span>", cover)
    # chips are flex boxes: no number spans inside (each span would become its own flex item)
    chips = '<span class="nlx-chip nlx-chip--sea">' + ty(t["chips"][0], lang) + "</span>" + "".join('<span class="nlx-chip">' + esc(ty(c, lang)) + "</span>" for c in t["chips"][1:])
    out += ['<header class="nlx-mast">', '<div class="nlx-mast-copy">', '<p class="nlx-kicker">' + esc(t["kicker"]) + "</p>",
            '<h1 class="nlx-title">' + esc(ty(t["h1"], lang)) + "</h1>", '<p class="nlx-dek">' + L(t["dek"]) + "</p>", '<div class="nlx-chips">' + chips + "</div>", "</div>", cover, "</header>", ""]
    out += ['<dl class="nlx-facts">'] + ['<div class="nlx-fact"><dt>' + esc(a) + "</dt><dd>" + L(b) + "</dd></div>" for a, b in t["facts"]] + ["</dl>"]
    toc = '<a class="nlx-home" href="' + SITE[lang] + '">' + esc(t["site_link"]) + "</a>" + "".join('<a href="#' + k + s + '">' + esc(v) + "</a>" for k, v in t["toc"])
    for i, (l2, name) in enumerate(t["langs"]):
        toc += '<a class="nlx-lang' + (" nlx-lang--more" if i else "") + '" href="' + URL[l2] + '" hreflang="' + l2 + '" lang="' + l2 + '">' + name + "</a>"
    out += ['<nav class="nlx-toc" aria-label="' + esc(t["toc_label"]) + '">' + toc + "</nav>", "", '<div class="nlx-layout">', '<div class="nlx-main">', ""]
    # photos, film, tour, 3D
    out.append('<section class="nlx-sec" id="photos' + s + '">' + sec_head(*t["photos"], lang=lang) + localise_alts(GALLERY, t) + "</section>")
    fe, fh, fl, fn = t["film"]
    out += ['<section class="nlx-sec" id="film' + s + '">', sec_head(fe, fh, fl, lang),
            '<div class="nlx-film"><video controls playsinline preload="metadata" width="1920" height="1080" poster="' + FILM_JPG + '"><source src="' + FILM_MP4 + '" type="video/mp4"></video></div>',
            '<p class="nlx-walk-note">' + L(fn) + "</p>", "</section>"]
    te, th, tl, tb, ts, ti, tc = t["tour"]
    out += ['<section class="nlx-sec" id="tour' + s + '">', sec_head(te, th, tl, lang),
            '<a class="nlx-walk" data-nlx-walk="' + esc(tb) + '" data-close="' + esc(tc) + '" href="' + WALK + 'home.html?lang=en"><img src="' + WALK + 'pano/living-card.jpg?ver=1.72.474" alt="' + esc(tb) + '" width="640" height="360" loading="lazy" decoding="async">'
            '<span class="nlx-walk-b"><b>' + L(tb) + "</b><small>" + L(ts) + "</small><i>" + esc(ti) + "</i></span></a>", "</section>"]
    we, wh, wl, wb, ws, wi, wa, wn = t["world"]
    out += ['<section class="nlx-sec" id="world' + s + '">', sec_head(we, wh, wl, lang),
            '<a class="nlx-walk" data-nlx-walk="' + esc(wb) + '" data-close="' + esc(tc) + '" href="' + WALK + 'index.html?ver=1.72.473"><img src="' + WALK + 'thumb.jpg?ver=1.72.473" alt="' + esc(wa) + '" width="1280" height="720" loading="lazy" decoding="async">'
            '<span class="nlx-walk-b"><b>' + L(wb) + "</b><small>" + L(ws) + "</small><i>" + esc(wi) + "</i></span></a>",
            '<p class="nlx-walk-note">' + L(wn) + "</p>", WALK_JS, "</section>"]
    # the residence
    feats = "".join("<li><b>" + L(a) + "</b><span>" + L(b) + "</span></li>" for a, b in t["features"])
    spec = "".join('<div class="nlx-spec-group"><h3 class="nlx-h3">' + esc(g) + '</h3><dl class="nlx-rows">' +
                   "".join('<div class="nlx-row"><dt>' + esc(a) + "</dt><dd>" + L(b) + '</dd><span class="nlx-row-tag"></span></div>' for a, b in rows) + "</dl></div>" for g, rows in t["spec"])
    out += ['<section class="nlx-sec" id="home' + s + '">', sec_head(t["home_eyebrow"], t["home_h2"], lang=lang),
            '<div class="nlx-prose">' + "".join("<p>" + L(p) + "</p>" for p in t["home"]) + "</div>",
            '<ul class="nlx-features">' + feats + "</ul>", '<div class="nlx-spec">' + spec + "</div>", "</section>", ""]
    out.append(ST.mini_section(lang))
    be, bh, bl, brows = t["building"]
    out += ['<section class="nlx-sec" id="building' + s + '">', sec_head(be, bh, bl, lang), '<dl class="nlx-rows">'] + \
           ['<div class="nlx-row"><dt>' + esc(a) + "</dt><dd>" + L(b) + '</dd><span class="nlx-row-tag"></span></div>' for a, b in brows] + ["</dl>", "</section>", ""]
    le, lh, lps, sh, schools, trh, trans, more = t["location"]
    items = lambda xs: "".join('<li class="nlx-item"><div class="nlx-item-top"><span class="nlx-item-title">' + L(a) + "</span></div><p>" + L(b) + "</p></li>" for a, b in xs)  # noqa: E731
    out += ['<section class="nlx-sec" id="location' + s + '">', sec_head(le, lh, lang=lang), '<div class="nlx-prose">' + "".join("<p>" + L(p) + "</p>" for p in lps) + "</div>", "",
            '<div class="nlx-two">', '<div><h3 class="nlx-subhead">' + esc(sh) + '</h3><ul class="nlx-items">' + items(schools) + "</ul></div>",
            '<div><h3 class="nlx-subhead">' + esc(trh) + '</h3><ul class="nlx-items">' + items(trans) + "</ul></div>", "</div>",
            '<p class="nlx-more">' + ty(more, lang) + "</p>", "</section>", ""]
    fe2, fh2, fl2, fitems = t["future"]
    out += ['<section class="nlx-sec" id="future' + s + '">', sec_head(fe2, fh2, fl2, lang), '<ul class="nlx-items">'] + \
           ['<li class="nlx-item"><span class="nlx-item-title">' + L(a) + "</span><p>" + L(b) + "</p></li>" for a, b in fitems] + ["</ul>", "</section>", ""]
    # value
    ve, vh, vl, vitems, vcap, vth, vnote = t["value"]
    rows = ""
    for pct in (3, 5, 8, 12):
        ch = 18000000 * pct // 100
        val = 18000000 + ch
        pc = (str(pct) + NB + "%") if lang == "fr" else (str(pct) + "%")
        rows += "<tr><td>+" + n(pc) + "</td><td>+" + n(cur(ch, lang)) + "</td><td>" + n(cur(val, lang)) + "</td><td>" + n(cur(val / 197, lang)) + "</td></tr>"
    out += ['<section class="nlx-sec" id="value' + s + '">', sec_head(ve, vh, vl, lang), '<ul class="nlx-items">'] + \
           ['<li class="nlx-item"><span class="nlx-item-title">' + L(a) + "</span><p>" + L(b) + "</p></li>" for a, b in vitems] + \
           ["</ul>", '<div class="nlx-tbl"><table><caption>' + esc(vcap) + "</caption><thead><tr>" + "".join("<th>" + esc(h) + "</th>" for h in vth) + "</tr></thead><tbody>" + rows + "</tbody></table></div>",
            '<p class="nlx-tbl-note">' + L(vnote) + "</p>", "</section>"]
    # the numbers band
    N = t["numbers"]
    out += ['<section class="nlx-sec" id="numbers' + s + '">', '<div class="nlx-band">', sec_head(N["eyebrow"], N["h2"], N["small"], lang, small=True),
            '<dl class="nlx-kpis nlx-kpis--4 nlx-kpis--wide">'] + \
           ['<div class="nlx-kpi"><dt>' + esc(a) + "</dt><dd>" + money(ty(b, lang)) + '</dd><span class="nlx-small">' + L(c) + "</span></div>" for a, b, c in N["kpis"]] + ["</dl>"]
    vals = [(1153886, 13500000, 4500000, 5653886), (1678899, 9000000, 9000000, 10678899), (975976, 13500000, 4500000, 5475976)]
    panels = ""
    for v, notes in zip(vals, N["notes"]):
        panels += '<dl class="nlx-seg-panel nlx-ledger">' + "".join("<div><dt>" + esc(r) + "</dt><dd>" + money(cur(x, lang)) + "</dd>" + ('<span class="nlx-ledger-note">' + L(nt) + "</span>" if nt else "") + "</div>"
                                                                     for r, x, nt in zip(N["rows"], v, notes)) + "</dl>"
    radios = "".join('<input type="radio" name="nlx-buyer' + s + '" id="nlx-buyer' + s + "-" + str(i) + '"' + (" checked" if i == 1 else "") + ">" for i in (1, 2, 3))
    labels = "".join('<label for="nlx-buyer' + s + "-" + str(i + 1) + '">' + esc(x) + "</label>" for i, x in enumerate(N["seg_labels"]))
    bar_vals = [(money(cur(91371, lang)), "99.7", True), (money(cur(80477, lang)), "87.4", True), (L(N["range_txt"][0]), "100.0", False),
                (money(cur(75793, lang)), "79.8", False), (money(cur(75281, lang)), "79.2", False), (L(N["range_txt"][1]), "53.7", False)]
    bars = "".join('<div class="nlx-bar' + (" nlx-bar--this" if this else "") + '"><div class="nlx-bar-top"><span>' + L(lbl) + "</span><span>" + v + '</span></div><div class="nlx-bar-track"><i style="width:' + w + '%"></i></div></div>'
                   for lbl, (v, w, this) in zip(N["bars"], bar_vals))
    ledger = "".join("<div><dt>" + L(a) + "</dt><dd>" + L(b) + "</dd>" + ('<span class="nlx-ledger-note">' + L(c) + "</span>" if c else "") + "</div>" for a, b, c in N["ledger"])
    out += ['<div class="nlx-band-grid">', '<div class="nlx-seg">', '<h3 class="nlx-h3">' + esc(N["seg_h3"]) + "</h3>", radios,
            '<div class="nlx-seg-labels" role="presentation">' + labels + "</div>", '<div class="nlx-seg-panels">' + panels + "</div>",
            '<p class="nlx-small">' + L(N["seg_small"]) + "</p>", "</div>", '<div class="nlx-bars">', '<h3 class="nlx-h3">' + esc(N["bars_h3"]) + "</h3>", bars,
            '<p class="nlx-small">' + L(N["bars_small"]) + "</p>", "</div>", "</div>", "<div>", '<h3 class="nlx-h3">' + esc(N["ledger_h3"]) + "</h3>",
            '<dl class="nlx-ledger">' + ledger + "</dl>", "</div>", '<p class="nlx-small">' + L(N["foot"]) + "</p>", "</div>", "</section>", ""]
    # the calculator, in the page's locale
    calc = ST.calc_section(lang).replace('L="en-US"', 'L="' + t["locale"] + '"').replace("w.toFixed(2)", 'w.toFixed(2).replace(".",",")')
    # the slider opens on exactly one third, so the live result matches the page's 80 477 (value 0.33 gave 80 573; the English page still does)
    calc = calc.replace('step="0.01" value="0.33"', 'step="any" value="0.333333"')
    calc = re.sub(r'(<dd data-o="\w+">)([\d,]+)', lambda m: m.group(1) + m.group(2).replace(",", NB), calc)
    calc = re.sub(r'(<dd data-o="\w+">[\d ]+) ', lambda m: m.group(1) + NB, calc)
    out.append(calc)
    # the market
    M = t["market"]
    stats = "".join("<div><dt>" + L(a) + ' <span class="nlx-muted">(' + n(esc(d)) + ")</span></dt><dd>" + L(b) + "</dd></div>" for a, d, b in M["stats"])
    dec = lambda x: x.replace(".", ",")  # noqa: E731
    srows = ""
    for (dk, rooms, sqm, fl, price, per), loc in zip(SALES, t["sales_loc"]):
        srows += ("<tr><td>" + L(t["rep_date"][dk]) + "</td><td>" + L(loc) + '</td><td class="nlx-r">' + (n(dec(rooms)) if rooms else "") + '</td><td class="nlx-r">' + n(dec(sqm)) +
                  '</td><td class="nlx-r">' + (n(fl) if fl else "") + '</td><td class="nlx-r">' + money(cur(price, lang)) + '</td><td class="nlx-r">' + money(cur(per, lang)) + "</td></tr>")
    rrows = ""
    for (rooms, sqm, rent, per), loc in zip(RENTS, t["rents_loc"]):
        rrows += ("<tr><td>" + L(t["rep_date"]["L16 Sep 2026"]) + "</td><td>" + L(loc) + '</td><td class="nlx-r">' + n(dec(rooms)) + '</td><td class="nlx-r">' + n(sqm) +
                  '</td><td class="nlx-r">' + money(cur(rent, lang)) + '</td><td class="nlx-r">' + money(cur(per, lang)) + "</td></tr>")
    table = lambda h3, th, cap, body: ('<div><h3 class="nlx-subhead">' + esc(h3) + '</h3><div class="nlx-scroll" role="region" aria-label="' + esc(h3) + '" tabindex="0"><table class="nlx-table">'  # noqa: E731
                                       "<caption>" + L(cap) + "</caption><thead><tr>" + "".join('<th scope="col">' + esc(x) + "</th>" for x in th) + "</tr></thead><tbody>" + body + "</tbody></table></div></div>")
    out += ['<section class="nlx-sec" id="market' + s + '">', sec_head(M["eyebrow"], M["h2"], M["lead"], lang), '<dl class="nlx-stats">' + stats + "</dl>",
            table(M["sales_h3"], M["sales_th"], M["sales_cap"], srows), table(M["rents_h3"], M["rents_th"], M["rents_cap"], rrows), "</section>", ""]
    ce, ch2, cl, cl_items = t["checks"]
    out += ['<section class="nlx-sec" id="checks' + s + '">', sec_head(ce, ch2, cl, lang),
            '<ul class="nlx-checks">' + "".join("<li><span>" + L(x) + "</span></li>" for x in cl_items) + "</ul>", "</section>", ""]
    # FAQ: the listing's own questions, then the mini penthouse pair, then the numbers
    faq = [(ty(q, lang), ty(a, lang)) for q, a in t["faq_a"]] + ST.TX[lang]["faq"] + [(ty(q, lang), ty(a, lang)) for q, a in t["faq_b"]]
    out += ['<section class="nlx-sec" id="faq' + s + '">', sec_head(t["faq_eyebrow"], t["faq_h2"], lang=lang),
            '<div class="nlx-faq">' + "".join("<details><summary>" + esc(q) + '</summary><div class="nlx-faq-a">' + L(a) + "</div></details>" for q, a in faq) + "</div>", "</section>", ""]
    B = t["broker"]
    btns = ('<div class="nlx-cta"><a class="nlx-btn" href="' + esc(wa_link(t)) + '" rel="noopener" target="_blank">' + SVG_WA + "<span>" + esc(B["cta"]) + "</span></a>"
            '<a class="nlx-btn nlx-btn--ghost" href="tel:+' + WA_NUM + '">' + SVG_TEL + "<span>" + esc(B["call"]) + "</span></a></div>")
    line = L(B["line"].replace(TEL, "⁠TEL⁠")).replace("⁠TEL⁠", TEL)
    out += ['<section class="nlx-sec" id="broker' + s + '">', '<div class="nlx-agent">', '<span class="nlx-monogram" aria-hidden="true">M</span>',
            '<div><p class="nlx-eyebrow">' + esc(B["eyebrow"]) + '</p><p class="nlx-agent-name"><a href="' + SITE[lang] + '">Meital Katzir</a></p><p class="nlx-small">' + line + "</p></div>",
            btns, "</div>", "</section>", "", "</div>"]
    R = t["rail"]
    out += ['<aside class="nlx-rail" aria-label="' + esc(B["aside"]) + '">', '<div class="nlx-card nlx-price-card">', '<span class="nlx-price-lbl">' + esc(R["lbl"]) + "</span>",
            '<span class="nlx-price">' + money(cur(18000000, lang)) + "</span>",
            '<div class="nlx-price-sub">' + "".join("<span>" + n(ty(x, lang)) + "</span>" for x in R["sub"]) + "</div>",
            '<dl class="nlx-price-rows">' + "".join("<div><dt>" + esc(a) + "</dt><dd>" + money(ty(b, lang)) + "</dd></div>" for a, b in R["rows"]) + "</dl>", btns, "</div>",
            '<div class="nlx-card nlx-agent-mini"><span class="nlx-monogram" aria-hidden="true">M</span><div><b><a href="' + SITE[lang] + '">Meital Katzir</a></b><br><span class="nlx-muted">' + line + "</span></div></div>",
            "</aside>", "</div>",
            '<div class="nlx-mbar"><a class="nlx-btn" href="' + esc(wa_link(t)) + '" rel="noopener" target="_blank">' + SVG_WA + '<span>WhatsApp</span></a><a class="nlx-btn nlx-btn--ghost" href="tel:+' + WA_NUM + '">' + SVG_TEL + "<span>" + esc(B["call_short"]) + "</span></a></div>",
            "</div>"]
    # structured data
    D = t["ld"]
    listing = {"@type": "RealEstateListing", "@id": URL[lang] + "#listing", "name": ty(t["h1"], lang), "description": ty(D["desc"], lang), "inLanguage": lang,
               "datePosted": EN_LISTING["datePosted"], "url": URL[lang],
               "about": {"@type": "Apartment", "name": ty(t["h1"], lang),
                         "address": {"@type": "PostalAddress", "addressLocality": "Tel Aviv-Yafo", "addressRegion": "Kochav HaTzafon", "addressCountry": "IL"},
                         "numberOfRooms": 5, "floorSize": {"@type": "QuantitativeValue", "value": 197, "unitCode": "MTK"},
                         "amenityFeature": [{"@type": "LocationFeatureSpecification", "name": ty(a, lang), "value": True} for a in D["amen"]],
                         "image": EN_LISTING["about"]["image"]},
               "offers": dict(EN_LISTING["offers"]), "image": EN_LISTING["image"]}
    assert listing["offers"]["price"] == 18000000 and listing["offers"]["businessFunction"].endswith("#Sell")
    graph = [listing, {"@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faq]},
             ST.app_ld(lang, URL[lang]),
             {"@type": "VideoObject", "name": ty(D["video"], lang), "description": ty(t["film"][2], lang), "thumbnailUrl": FILM_JPG, "contentUrl": FILM_MP4,
              "uploadDate": "2026-10-20", "duration": "PT2M10S", "inLanguage": "en"}]
    out += ['<script type="application/ld+json">' + json.dumps({"@context": "https://schema.org", "@graph": graph}, ensure_ascii=False) + "</script>", "</article>", "<!-- /wp:html -->", ""]
    return "\n".join(out), faq


# ------------------------------------------------------------------ the gates
BAN = {
    "all": ["tenant", "locataire", "loué actuellement", "арендатор", "сдана в аренду", "сдаётся", "attico", "cobertura", "Ben ", "commission", "комисси", "brokerage",
            "best in the world", "meilleur au monde", "le meilleur du monde", "лучший в мире", "penthouse neuf", "neuf de 5", "appartement neuf", "новый мини", "новая квартира", "новом доме",
            "L07)", "Madlan", "Yad2", "nad-lan.co.il, L07"],
    # the drop engine's FR/RU word gate (plugins/nadlan-config/inc/broker-drop.php, nl_drop_banned)
    "fr": ["madlan", "yad2", "instagram", "non vérifié", "non confirmé", "selon l’agent", "non publié", "unique", "uniques", "rêve*", "parfait*", "exceptionnel*", "magnifique*",
           "sublime*", "incroyable*", "à ne pas manquer", "coup de cœur", "opportunité*", "dépêchez", "—", "–", "!"],
    "ru": ["мадлан", "яд2", "инстаграм", "не проверено", "не подтверждено", "по словам риелтора", "не опубликовано", "уникальн*", "мечт*", "идеальн*", "потрясающ*",
           "шикарн*", "невероятн*", "сказочн*", "не упустите", "спешите", "успейте", "эксклюзивное предложение", "—", "–", "!"],
}


def visible_text(page):
    a = page[page.index("<article"):page.index("</article>")]
    a = re.sub(r"<(script|style)[^>]*>.*?</\1>", " ", a, flags=re.S)
    a = re.sub(r"<svg.*?</svg>", " ", a, flags=re.S)
    return html.unescape(re.sub(r"<[^>]+>", " ", a))


def gate(lang, page, faq, seo):
    txt = visible_text(page)
    ld = json.loads(re.search(r'<script type="application/ld\+json">(.*?)</script>', page, re.S).group(1))
    every = txt + " " + json.dumps(ld, ensure_ascii=False) + " " + seo["title"] + " " + seo["metadesc"] + " " + urllib.parse.unquote(page)
    low = every.lower()
    words = set(re.findall(r"[\wʼ’'-]+", low))
    hits = []
    for w in BAN["all"]:
        if w.lower() in low:
            hits.append(w)
    for w in BAN[lang]:
        wl = w.lower()
        if " " in wl or not re.match(r"^[\w*-]+$", wl):
            if wl.rstrip("*") in txt.lower() + " " + seo["title"].lower() + " " + seo["metadesc"].lower():
                hits.append(w)
        elif wl.endswith("*"):
            if any(x.startswith(wl[:-1]) for x in words):
                hits.append(w)
        elif wl in words:
            hits.append(w)
    assert not hits, (lang, "banned", hits)
    assert len(seo["title"]) <= 60, (lang, "title", len(seo["title"]))
    assert len(seo["metadesc"]) <= 155, (lang, "meta", len(seo["metadesc"]))
    art = page[page.index("<article"):]
    assert len(re.findall(r"<h1[ >]", art)) == 1
    assert art.count("<details>") == len(faq) == len(next(g for g in ld["@graph"] if g["@type"] == "FAQPage")["mainEntity"])
    for k in re.findall(r'href="#([\w-]+)"', art):
        assert 'id="' + k + '"' in page, (lang, "anchor", k)
    assert "home.html?lang=en" in page and FILM_MP4 in page and 'id="nlxcalc-L07-' + lang + '"' in page
    lst = next(g for g in ld["@graph"] if g["@type"] == "RealEstateListing")
    assert lst["inLanguage"] == lang and lst["url"] == URL[lang] and lst["offers"]["price"] == 18000000
    assert next(g for g in ld["@graph"] if g["@type"] == "WebApplication")["inLanguage"] == lang
    assert ("mini-penthouse" if lang == "fr" else "мини-пентхаус") in seo["title"].lower() and "18" in seo["metadesc"]
    assert not re.search(r"[֐-׿]", txt.replace("עברית", "")), (lang, "Hebrew text left on the page")
    for need in ("197", "80", "74", "11", "12"):
        assert need in txt
    return {"title_len": len(seo["title"]), "meta_len": len(seo["metadesc"]), "faq": len(faq), "chars": len(page), "sections": len(re.findall(r'<section class="nlx-sec"', page))}


def preview(lang, page):
    return ("<!doctype html><html lang=\"" + lang + "\"><head><meta charset=\"utf-8\"><meta name=\"viewport\" content=\"width=device-width,initial-scale=1\">"
            "<meta name=\"robots\" content=\"noindex\"><title>" + esc(T[lang]["title"]) + "</title>"
            "<link rel=\"stylesheet\" href=\"https://fonts.googleapis.com/css2?family=Assistant:wght@400;600;700&family=Noto+Serif:wght@500;600&display=swap\">"
            "<style>body{background:#F7F6F2;margin:0}</style></head><body><div class=\"entry-content\">" + page + "</div></body></html>")


if __name__ == "__main__":
    seo_all = {}
    for lang in ("fr", "ru"):
        page, faq = build(lang)
        seo = {"lang": lang, "url": URL[lang], "slug": SLUG, "parent_page_id": PARENT[lang], "parent_url": SITE[lang],
               "title": ty(T[lang]["title"], lang).replace(NB, " "), "metadesc": ty(T[lang]["meta"], lang).replace(NB, " "),
               "post_title": ty(T[lang]["h1"], lang).replace(NB, " "),
               "meta": {"nl_lang": lang, "nl_broker_id": "7833", "nl_card_key": "L07", "nl_twin": "7634", "nl_status": "active", "nl_dossier": "1"},
               "nl_hreflang": {"he": URL["he"], "en": URL["en"], "fr": URL["fr"], "ru": URL["ru"]}}
        stats = gate(lang, page, faq, seo)
        io.open(os.path.join(H, "after-" + lang + ".html"), "w", encoding="utf-8", newline="\n").write(page)
        io.open(os.path.join(H, "preview-" + lang + ".html"), "w", encoding="utf-8", newline="\n").write(preview(lang, page))
        seo_all[lang] = seo
        print(lang, json.dumps(stats, ensure_ascii=False), "|", seo["title"], "|", seo["metadesc"])
    io.open(os.path.join(H, "seo.json"), "w", encoding="utf-8", newline="\n").write(json.dumps(seo_all, ensure_ascii=False, indent=1))
    print("written: after-fr.html after-ru.html preview-fr.html preview-ru.html seo.json (nothing published)")
