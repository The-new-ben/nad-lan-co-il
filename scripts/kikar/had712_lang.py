# -*- coding: utf-8 -*-
"""HAD-712, the language pages (11.11.2026, Ben's order through the Kikar session: "bring everything the Hebrew page gained today to
the four language pages, one language at a time"). The Hebrew Kikar article (post 8113) gained on 11.11.2026, by
scripts/kikar/had712_content.py and scripts/kikar/had712_images.py: height per tower, a towers table, five searched FAQ questions,
the building-fee and rent estimates worded as estimates, WXG, a table of the numbers publications give differently, and 7 figures
(18 renders, each captioned as an illustration). This script carries the same additions into the English (8114), French (8116),
Russian (8117) and Arabic (8118) posts, written in each page's own terms (read from the live post first).
Every number is the Hebrew round's, read at its source on 11.11.2026 (docs/qa/had-712/sources.md); nothing unverified is added.
The articles name no outlet (the owner's rule of 1.10.2026).
Small anchored replacements on the LIVE post text; the live md5 is pinned; each anchor must appear exactly once. Backup before,
read-back after (restored if it differs); dry by default (the dry run writes _had712_<lang>_preview.html beside this file).
  python scripts/kikar/had712_lang.py <en|fr|ru|ar> [--go]"""
import hashlib, io, json, os, sys, time
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.dirname(os.path.dirname(HERE))
G = "https://nad-lan.co.il/wp-content/plugins/nadlan-config/assets/project-stage/hamedina/gallery/"


def img(f, alt, w, h):
    return '<img src="%s%s" alt="%s" width="%d" height="%d" loading="lazy" decoding="async">' % (G, f, alt, w, h)


def cell(f, alt, w, h, label):
    return '<span class="nlws-fig__i">' + img(f, alt, w, h) + "<b>" + label + "</b></span>"


def fig(inner, cap):
    return '<figure class="nlws-fig">' + inner + "<figcaption>" + cap + "</figcaption></figure>"


def grid(n, cells):
    return '<div class="nlws-fig__g nlws-fig__g--%d">' % n + "".join(cells) + "</div>"


def figures(t):
    """the 7 figures of the Hebrew article, in the page's language; t = the translated alts, labels and captions"""
    L = "<b>" + t["label"] + "</b> "
    return {
        "aerial": fig(img("kikar-hamedina-towers-aerial.webp", t["aerial_alt"], 1600, 1000), L + t["aerial_cap"]),
        "towers": fig(grid(3, [cell("kikar-hamedina-tower-%s.webp" % k.lower(), t["tower_alt"] % (k, n), 756, 1080, t["tower_lbl"] % k)
                               for k, n in (("A", 40), ("B", 37), ("C", 40))]), L + t["towers_cap"]),
        "balcony": fig(img("kikar-hamedina-balcony.webp", t["balcony_alt"], 1200, 675), L + t["balcony_cap"]),
        "dirs": fig(grid(2, [cell("kikar-hamedina-floor-30-%s.webp" % d, t["dir_alt"] % t["dir_w"][i], 640, 360, t["dir_lbl"][i])
                             for i, d in enumerate(("north", "east", "south", "west"))]), L + t["dirs_cap"]),
        "floors": fig(grid(3, [cell("kikar-hamedina-view-floor-%d.webp" % n, t["floor_alt"] % n, 1200, 675, t["floor_lbl"] % n)
                               for n in (20, 30, 38)]), L + t["floors_cap"]),
        "home": fig(grid(2, [cell("kikar-hamedina-living-room.webp", t["living_alt"], 1200, 675, t["living_lbl"]),
                             cell("kikar-hamedina-bedroom.webp", t["bed_alt"], 1200, 675, t["bed_lbl"])]), L + t["home_cap"]),
        "fac": fig(grid(2, [cell("kikar-hamedina-%s.jpg" % f, t["fac_alt"][i], 1200, 675, t["fac_lbl"][i])
                            for i, f in enumerate(("pool", "gym", "spa", "lobby"))]), t["fac_cap"]),
    }


def table(head, rows):
    return ("<table><thead><tr>" + "".join("<th>%s</th>" % h for h in head) + "</tr></thead><tbody>"
            + "".join("<tr>" + "".join("<td>%s</td>" % c for c in r) + "</tr>" for r in rows) + "</tbody></table>")


# ------------------------------------------------------------------------------------------------------------------------ English
EN_EST = "According to an estimate by a real-estate professional published in October 2026"
EN_T = {
    "label": "Illustrative visualisation.",  # the page's own label (the film block, 1.72.646)
    "aerial_alt": "The three Kikar Hamedina Towers inside the square in Tel Aviv, aerial view",
    "aerial_cap": "The three Kikar Hamedina Towers inside the square, seen from the air towards the sea.",
    "tower_alt": "Tower %s of Kikar Hamedina Towers, %d floors", "tower_lbl": "Tower %s",
    "towers_cap": "Each tower on its own: A and C have 40 floors, B has 37.",
    "balcony_alt": "The view from a 30th-floor balcony in Tower C of Kikar Hamedina Towers, looking west",
    "balcony_cap": "The view from a 30th-floor balcony in Tower C, looking west towards sunset.",
    "dir_alt": "The view %s from the 30th floor of Kikar Hamedina Towers", "dir_w": ("north", "east", "south", "west"),
    "dir_lbl": ("North", "East", "South", "West"),
    "dirs_cap": "The view from the 30th floor of Tower C in four directions. The view from a particular apartment depends on the tower, the floor and the direction.",
    "floor_alt": "The view west from floor %d of Kikar Hamedina Towers", "floor_lbl": "Floor %d",
    "floors_cap": "The same direction, west, from three floors of Tower C.",
    "living_alt": "The living room of an example apartment on the 30th floor of Kikar Hamedina Towers", "living_lbl": "Living room",
    "bed_alt": "A bedroom in an example apartment on the 30th floor of Kikar Hamedina Towers", "bed_lbl": "Bedroom",
    "home_cap": "A living room and a bedroom in an example apartment on the 30th floor; not a photograph and not an official specification.",
    "fac_alt": ("The swimming pool of Kikar Hamedina Towers", "The gym of Kikar Hamedina Towers", "The spa of Kikar Hamedina Towers", "The lobby of Kikar Hamedina Towers"),
    "fac_lbl": ("Pool", "Gym", "Spa", "Lobby"),
    "fac_cap": "<b>An illustrative visualisation of the facilities:</b> not footage and not an official specification.",  # the clip's own wording
}
EN_F = figures(EN_T)
EN_TOWERS = ("<h3>How many floors and how tall is each tower?</h3>"
             "<p>Two towers have 40 floors and one has 37. The table brings together what has been published about each tower; the number of apartments in each tower has not been published.</p>"
             # every cell says what it is: on a phone the theme stacks the cells and hides the header row
             + table(("Tower", "Position on the plot", "Floors", "Published height"),
                     (("Tower A", "Southwest of the plot", "40 floors", "About 160 m"),
                      ("Tower B", "Southeast of the plot", "37 floors", "About 157 m"),
                      ("Tower C", "Northeast of the plot", "40 floors", "About 160 m"))))
EN_DIFF = ("<p><strong>Figures that differ between publications.</strong> Some of the project’s figures are published in more than one version. "
           "The table shows the versions found in November 2026 and the figure used on this page.</p>"
           + table(("Figure", "What publications give", "What this page uses"), (
               ("Floors", "In publications: three towers of 40 floors, and also two of 40 floors and one of 37", "On this page: 40, 37 and 40 floors, following the builder’s breakdown"),
               ("Height", "In publications: up to about 160 m for all the towers, and also 160 m for two and 157 m for the third", "On this page: up to about 160 m; Tower B, with 37 floors, about 157 m"),
               ("Number of apartments", "In publications: about 450, and also 453", "On this page: 453 apartments"),
               ("Landowners", "In publications: about 150, and also about 250", "On this page: about 250 rights holders"),
               ("Area", "In publications: about 27 dunam, about 50 dunam and also about 78 dunam", "On this page: about 78 dunam is the area of the whole plan, and the public park alone is about 40 dunam; the publications that give about 27 and about 50 dunam do not say what was measured"),
               ("End of construction", "In publications: 2026, and also April 2027", "On this page: completion of the towers’ construction was reported in October 2026, and handover is expected between the first quarter of 2027 and May 2027"))))
EN_FAQ = ("<h3>How many floors do Kikar Hamedina Towers have?</h3>"
          "<p>Towers A and C have 40 floors and Tower B has 37. Below the towers are three underground parking levels. Each floor turns 1.25 degrees relative to the floor below, so apartments on the same side of a tower face a slightly different direction on each floor. When choosing a floor, ask for the plan of that specific floor and check which way the living room and the balcony face.</p>"
          "<h3>What is the address of Kikar Hamedina Towers?</h3>"
          "<p>The towers stand inside Kikar Hamedina in north Tel Aviv’s New North, and their building-permit addresses are He Be’Iyar Street 25, 45 and 65. He Be’Iyar Street circles the square, with Weizmann Street reaching it from the south and Jabotinsky Street from the east. When asking about an apartment, request the tower’s address and the apartment number, because a general Kikar Hamedina address also fits the ring buildings around the square.</p>"
          "<h3>Who is the developer of Kikar Hamedina Towers, and is it a purchase group?</h3>"
          "<p>The landowners themselves are building the project: about 250 rights holders, heirs of the people who bought the plots in 1942, who incorporated in 1997 and act through the landowners’ company. They received apartments in exchange for the land, and the order in which apartments were chosen was set by lottery. In searches the project is sometimes called a purchase group; in practice it is an association of the landowners, not a group that bought the land together. There is no developer selling new apartments to the public: anyone buying today buys an apartment, or a right to one, from one of the rights holders.</p>"
          "<h3>Who is the architect of Kikar Hamedina Towers?</h3>"
          "<p>The towers were designed by Yaski Mor Sivan Architects, chosen through a competition in 2000. The design is based on a turning envelope: each floor is shifted 1.25 degrees relative to the floor below. The landscape design is by T.M.A., and Waxman Govrin Geva (WXG) coordinates the project management. Get the plan and the specification of the specific apartment from the seller, not from a general description of the design.</p>"
          "<h3>How much are the building fees (vaad bayit) in Kikar Hamedina Towers?</h3>"
          "<p>An official management-fee rate has not been published. " + EN_EST + ", the maintenance fees are expected to reach about ₪4,000 to ₪5,000 per apartment a month, depending on the apartment’s size. The estimate refers to a building with residents’ facilities, including a swimming pool, a spa and a gym. It is an early estimate, made before occupancy. Before deciding, ask for the monthly charge of the specific apartment and the list of services it covers.</p>")
EN_SWAPS = [
    # 1. the facts table: height per tower
    ("<td>Towers A and C have 40 floors; Tower B has 37 floors. The buildings reach up to about 160 m.</td>",
     "<td>Towers A and C have 40 floors; Tower B has 37 floors. The buildings reach up to about 160 m: according to the published figures, Towers A and C reach about 160 m and Tower B about 157 m.</td>"),
    # 2. the project manager's short name, as people search it
    ("<td>Waxman Govrin Geva, involved with the project since 2001.</td>",
     "<td>Waxman Govrin Geva (WXG), involved with the project since 2001.</td>"),
    # 3. the aerial picture before the facts table
    ("<table><tbody><tr><th>Location</th>", EN_F["aerial"] + "<table><tbody><tr><th>Location</th>"),
    # 4. after the facts table: the numbers that publications give differently
    ("</tbody></table></section><section class=\"nlws\" id=\"nlws-choose\">",
     "</tbody></table>" + EN_DIFF + "</section><section class=\"nlws\" id=\"nlws-choose\">"),
    # 5. the three towers side by side, and their pictures
    ("ask for the plan of the specific home you are considering.</p><h3>What the turning floors change</h3>",
     "ask for the plan of the specific home you are considering.</p>" + EN_TOWERS + EN_F["towers"] + "<h3>What the turning floors change</h3>"),
    # 6-8. the views
    ("<h3>What lies in each direction</h3>", EN_F["balcony"] + "<h3>What lies in each direction</h3>"),
    ("<h3>Lower floor or higher floor?</h3>", EN_F["dirs"] + "<h3>Lower floor or higher floor?</h3>"),
    ("</p></section><section class=\"nlws\" id=\"nlws-homes\">", "</p>" + EN_F["floors"] + "</section><section class=\"nlws\" id=\"nlws-homes\">"),
    # 9. the example apartment
    ("<h3>Glass, finishes and the mamad</h3>", EN_F["home"] + "<h3>Glass, finishes and the mamad</h3>"),
    # 10. the facilities
    ("<h3>Moving through the building</h3>", EN_F["fac"] + "<h3>Moving through the building</h3>"),
    # 11. the building fee
    ("<p>The management company and its monthly fee are not published.",
     "<p>The management company and an official monthly fee have not been published. " + EN_EST + ", the maintenance fees (vaad bayit) in the towers are expected to reach about ₪4,000 to ₪5,000 per apartment a month, depending on the apartment’s size. That is an early estimate, made before occupancy."),
    # 12. rent
    ("<p>Rentals begin only after occupancy, and rents for the towers are not published.",
     "<p>Rentals begin only after occupancy, and no rent actually agreed in the towers has been published yet. " + EN_EST + ", an apartment in the towers will rent for about ₪25,000 a month; that is an early estimate, not a signed lease."),
    # 13. the height answer
    ("Tower B has 37; the buildings reach up to about 160 m.",
     "Tower B has 37; the buildings reach up to about 160 m. According to the published figures, Towers A and C reach about 160 m and Tower B about 157 m."),
    # 14. five questions people search, after "who is building"
    ("<h3>What is Kikar Hamedina in Tel Aviv?</h3>", EN_FAQ + "<h3>What is Kikar Hamedina in Tel Aviv?</h3>"),
]

# ------------------------------------------------------------------------------------------------------------------------ French


def _fr(s):  # the French article's typography: "~" is a no-break space; a no-break space before ; : ? ! and inside « »
    s = s.replace("~", "\xa0")
    for p in (";", ":", "?", "!"):
        s = s.replace(" " + p, "\xa0" + p)
    return s.replace("« ", "«\xa0").replace(" »", "\xa0»")


FR_EST = "Selon l’estimation d’un professionnel de l’immobilier publiée en octobre 2026"
FR_T = {k: (_fr(v) if isinstance(v, str) else tuple(_fr(x) for x in v)) for k, v in {
    "label": "Visualisation illustrative.",  # the page's own label (the film block, 1.72.646)
    "aerial_alt": "Les trois tours Kikar Hamedina au centre de la place, à Tel Aviv, vue aérienne",
    "aerial_cap": "Les trois tours Kikar Hamedina au centre de la place, vues du ciel en direction de la mer.",
    "tower_alt": "Tour %s des tours Kikar Hamedina, %d étages", "tower_lbl": "Tour %s",
    "towers_cap": "Chaque tour séparément : A et C comptent 40 étages, B en compte 37.",
    "balcony_alt": "La vue depuis un balcon du 30e étage de la tour C, tours Kikar Hamedina, vers l’ouest",
    "balcony_cap": "La vue depuis un balcon du 30e étage de la tour C, vers l’ouest, à l’approche du coucher du soleil.",
    "dir_alt": "La vue %s depuis le 30e étage des tours Kikar Hamedina", "dir_w": ("vers le nord", "vers l’est", "vers le sud", "vers l’ouest"),
    "dir_lbl": ("Nord", "Est", "Sud", "Ouest"),
    "dirs_cap": "La vue depuis le 30e étage de la tour C dans quatre directions. La vue depuis un appartement donné dépend de la tour, de l’étage et de l’orientation.",
    "floor_alt": "La vue vers l’ouest depuis le %de étage des tours Kikar Hamedina", "floor_lbl": "%de étage",
    "floors_cap": "La même direction, l’ouest, depuis trois étages de la tour C.",
    "living_alt": "Le séjour d’un appartement type au 30e étage des tours Kikar Hamedina", "living_lbl": "Séjour",
    "bed_alt": "Une chambre d’un appartement type au 30e étage des tours Kikar Hamedina", "bed_lbl": "Chambre",
    "home_cap": "Le séjour et une chambre d’un appartement type au 30e étage ; ni une photographie, ni une spécification officielle.",
    "fac_alt": ("La piscine des tours Kikar Hamedina", "La salle de sport des tours Kikar Hamedina", "Le spa des tours Kikar Hamedina", "Le hall d’accueil des tours Kikar Hamedina"),
    "fac_lbl": ("Piscine", "Salle de sport", "Spa", "Hall"),
    "fac_cap": "<b>Une visualisation illustrative des équipements :</b> ni un tournage, ni une spécification officielle.",  # the clip's own wording
}.items()}
FR_F = figures(FR_T)
FR_TOWERS = _fr("<h3>Combien d’étages et quelle hauteur pour chaque tour ?</h3>"
                "<p>Deux tours comptent 40 étages et la troisième en compte 37. Le tableau réunit ce qui a été publié pour chaque tour ; le nombre d’appartements par tour n’a pas été publié.</p>"
                + table(("Tour", "Position sur la parcelle", "Étages", "Hauteur publiée"),
                        (("Tour A", "Au sud-ouest de la parcelle", "40 étages", "Environ 160~m"),
                         ("Tour B", "Au sud-est de la parcelle", "37 étages", "Environ 157~m"),
                         ("Tour C", "Au nord-est de la parcelle", "40 étages", "Environ 160~m"))))
FR_DIFF = _fr("<p><strong>Des chiffres qui varient selon les publications.</strong> Certaines données du projet circulent en plusieurs versions. "
              "Le tableau présente les versions relevées en novembre 2026 et le chiffre retenu sur cette page.</p>"
              + table(("Donnée", "Ce que donnent les publications", "Ce que retient cette page"), (
                  ("Étages", "Dans les publications : trois tours de 40 étages, et aussi deux tours de 40 étages et une de 37", "Sur cette page : 40, 37 et 40 étages, selon le détail de l’entreprise de construction"),
                  ("Hauteur", "Dans les publications : jusqu’à environ 160~m pour toutes les tours, et aussi 160~m pour deux d’entre elles et 157~m pour la troisième", "Sur cette page : jusqu’à environ 160~m ; la tour B, de 37 étages, environ 157~m"),
                  ("Nombre d’appartements", "Dans les publications : environ 450, et aussi 453", "Sur cette page : 453 appartements"),
                  ("Propriétaires fonciers", "Dans les publications : environ 150, et aussi environ 250", "Sur cette page : environ 250 détenteurs de droits"),
                  ("Surface", "Dans les publications : environ 27 dunams, environ 50 dunams et aussi environ 78 dunams", "Sur cette page : environ 78 dunams correspondent à l’ensemble du plan, et le parc public seul à environ 40 dunams ; les publications qui donnent environ 27 et environ 50 dunams ne précisent pas ce qui a été mesuré"),
                  ("Fin des travaux", "Dans les publications : 2026, et aussi avril 2027", "Sur cette page : l’achèvement de la construction des tours a été annoncé en octobre 2026, et la remise des clés est attendue entre le premier trimestre 2027 et mai 2027"))))
FR_FAQ = _fr("<h3>Combien d’étages comptent les tours Kikar Hamedina ?</h3>"
             "<p>Les tours A et C comptent 40 étages et la tour B en compte 37. Sous les tours se trouvent trois niveaux de stationnement souterrain. Chaque étage pivote de 1,25 degré par rapport à celui du dessous : d’un étage à l’autre, les appartements d’une même façade regardent donc dans une direction légèrement différente. Pour choisir un étage, demandez le plan de cet étage précis et vérifiez l’orientation du séjour et du balcon.</p>"
             "<h3>Quelle est l’adresse des tours Kikar Hamedina ?</h3>"
             "<p>Les tours se trouvent au centre de la place Kikar Hamedina, dans le Nouveau Nord de Tel Aviv, et leurs adresses au permis de construire sont les 25, 45 et 65, rue He Be’Iyar. La rue He Be’Iyar fait le tour de la place ; la rue Weizmann y arrive par le sud et la rue Jabotinsky par l’est. Pour vous renseigner sur un appartement, demandez l’adresse de la tour et le numéro de l’appartement : une adresse générale « Kikar Hamedina » correspond aussi aux immeubles de l’anneau qui entoure la place.</p>"
             "<h3>Qui est le promoteur des tours Kikar Hamedina, et s’agit-il d’un groupe d’achat ?</h3>"
             "<p>Ce sont les propriétaires fonciers eux-mêmes qui réalisent le projet : environ 250 détenteurs de droits, héritiers des acquéreurs des parcelles en 1942, qui se sont regroupés en 1997 et agissent au sein de la société des propriétaires fonciers. Ils ont reçu des appartements en échange du terrain, et l’ordre de choix des appartements a été fixé par tirage au sort. Dans les recherches, le projet est parfois qualifié de groupe d’achat ; en réalité, c’est une association de propriétaires fonciers, et non un groupe qui a acheté le terrain ensemble. Aucun promoteur ne vend d’appartements neufs au public : acheter aujourd’hui, c’est acheter un appartement, ou un droit à un appartement, à l’un des détenteurs de droits.</p>"
             "<h3>Qui est l’architecte des tours Kikar Hamedina ?</h3>"
             "<p>Les tours ont été conçues par l’agence Yaski Mor Sivan Architectes, retenue à l’issue d’un concours en 2000. Le projet repose sur une enveloppe qui pivote : chaque étage est décalé de 1,25 degré par rapport à celui du dessous. L’architecture paysagère est signée T.M.A., et Waxman Govrin Geva (WXG) coordonne la gestion du projet. Le plan et le descriptif de l’appartement précis s’obtiennent auprès du vendeur, et non dans une présentation générale du projet.</p>"
             "<h3>Combien coûtent les charges (vaad bayit) dans les tours Kikar Hamedina ?</h3>"
             "<p>Aucun tarif officiel des charges n’a été publié. " + FR_EST + ", les charges d’entretien devraient atteindre environ 4~000 à 5~000~₪ par appartement et par mois, selon la surface. L’estimation concerne un immeuble doté d’équipements pour les résidents, dont une piscine, un spa et une salle de sport. C’est une estimation précoce, antérieure à l’emménagement. Avant de décider, demandez le montant mensuel facturé pour l’appartement concerné et la liste des services qu’il couvre.</p>")
FR_SWAPS = [(_fr(a), _fr(b)) for a, b in [
    # 1. the facts table: height per tower
    ("<td>Jusqu’à environ 160~m.</td>",
     "<td>Jusqu’à environ 160~m. Selon les données publiées, les tours A et C atteignent environ 160~m et la tour B environ 157~m.</td>"),
    # 2. the project manager's short name, as people search it
    ("<td>Waxman Govrin Geva assure la gestion du projet ;", "<td>Waxman Govrin Geva (WXG) assure la gestion du projet ;"),
    # 3. the aerial picture before the facts table
    ("<table><tbody><tr><th>Implantation</th>", FR_F["aerial"] + "<table><tbody><tr><th>Implantation</th>"),
    # 4. after the facts table: the numbers that publications give differently
    ("</tbody></table></section><section class=\"nlws\" id=\"nlws-choose\">",
     "</tbody></table>" + FR_DIFF + "</section><section class=\"nlws\" id=\"nlws-choose\">"),
    # 5. the three towers side by side, and their pictures
    ("pour confirmer votre sélection.</p><h3>Ce que la rotation change pour votre appartement</h3>",
     "pour confirmer votre sélection.</p>" + FR_TOWERS + FR_F["towers"] + "<h3>Ce que la rotation change pour votre appartement</h3>"),
    # 6-8. the views
    ("<h3>Les directions à examiner pour une vue mer ou une vue sur la ville</h3>", FR_F["balcony"] + "<h3>Les directions à examiner pour une vue mer ou une vue sur la ville</h3>"),
    ("<h3>Arbitrer entre hauteur, surface et prix au m²</h3>", FR_F["dirs"] + "<h3>Arbitrer entre hauteur, surface et prix au m²</h3>"),
    ("</p></section><section class=\"nlws\" id=\"nlws-homes\">", "</p>" + FR_F["floors"] + "</section><section class=\"nlws\" id=\"nlws-homes\">"),
    # 9. the example apartment
    ("<h3>Le confort intérieur et les prestations annoncées</h3>", FR_F["home"] + "<h3>Le confort intérieur et les prestations annoncées</h3>"),
    # 10. the facilities
    ("<h3>De l’accueil à la porte de l’appartement</h3>", FR_F["fac"] + "<h3>De l’accueil à la porte de l’appartement</h3>"),
    # 11. the building fee
    ("<p>La société de gestion et le montant mensuel des charges ne sont pas publiés.",
     "<p>La société de gestion et un tarif officiel des charges ne sont pas publiés. " + FR_EST + ", les charges d’entretien (le « vaad bayit ») devraient atteindre environ 4~000 à 5~000~₪ par appartement et par mois, selon la surface. Il s’agit d’une estimation précoce, antérieure à l’emménagement."),
    # 12-13. rent
    ("La location commencera seulement après la mise en habitation. Aucun loyer n’est publié pour les tours Kikar Hamedina.",
     "La location commencera seulement après la mise en habitation, et aucun loyer effectivement conclu dans les tours n’est encore publié. " + FR_EST + ", un appartement des tours se louerait environ 25~000~₪ par mois ; c’est une estimation précoce, pas un bail signé."),
    ("gardez cette absence de loyer chiffré", "gardez cette absence de loyer effectivement conclu"),
    # 14. the height answer
    ("jusqu’à environ 160~m : les tours A et C comptent 40 étages chacune, et la tour B en compte 37.",
     "jusqu’à environ 160~m : les tours A et C comptent 40 étages chacune, et la tour B en compte 37. Selon les données publiées, les tours A et C atteignent environ 160~m et la tour B environ 157~m."),
    # 15. five questions people search, after "who is building"
    ("<h3>Qu’est-ce que Kikar Hamedina à Tel Aviv ?</h3>", FR_FAQ + "<h3>Qu’est-ce que Kikar Hamedina à Tel Aviv ?</h3>"),
]]

# ------------------------------------------------------------------------------------------------------------------------ Russian
# the page's own terms: владельцы прав, компания владельцев земли, салон, Новый Север, Форма 4, плата за обслуживание; thousands and
# "млн ₪" with a no-break space ("~" below), metres with a plain space, as the live post writes them
RU_EST = "По оценке специалиста по недвижимости, опубликованной в октябре 2026 года"
_ru = lambda s: s.replace("~", "\xa0")
RU_T = {k: (_ru(v) if isinstance(v, str) else tuple(_ru(x) for x in v)) for k, v in {
    "label": "Иллюстративная визуализация.",  # the page's own label (the film block, 1.72.646)
    "aerial_alt": "Три башни Кикар ха-Медина внутри площади в Тель-Авиве, вид с воздуха",
    "aerial_cap": "Три башни Кикар ха-Медина внутри площади, вид с воздуха в сторону моря.",
    "tower_alt": "Башня %s комплекса Кикар ха-Медина, %d этажей", "tower_lbl": "Башня %s",
    "towers_cap": "Каждая башня отдельно: в A и C по 40 этажей, в B 37.",
    "balcony_alt": "Вид с балкона на 30-м этаже башни C, Кикар ха-Медина, на запад",
    "balcony_cap": "Вид с балкона на 30-м этаже башни C на запад, ближе к закату.",
    "dir_alt": "Вид %s с 30-го этажа башен Кикар ха-Медина", "dir_w": ("на север", "на восток", "на юг", "на запад"),
    "dir_lbl": ("Север", "Восток", "Юг", "Запад"),
    "dirs_cap": "Вид с 30-го этажа башни C в четыре стороны. Вид из конкретной квартиры зависит от башни, этажа и направления.",
    "floor_alt": "Вид на запад с %d-го этажа башен Кикар ха-Медина", "floor_lbl": "%d-й этаж",
    "floors_cap": "Одно и то же направление, запад, с трёх этажей башни C.",
    "living_alt": "Салон в квартире-примере на 30-м этаже башен Кикар ха-Медина", "living_lbl": "Салон",
    "bed_alt": "Спальня в квартире-примере на 30-м этаже башен Кикар ха-Медина", "bed_lbl": "Спальня",
    "home_cap": "Салон и спальня в квартире-примере на 30-м этаже; не фотография и не официальная спецификация.",
    "fac_alt": ("Бассейн в башнях Кикар ха-Медина", "Тренажёрный зал в башнях Кикар ха-Медина", "Спа в башнях Кикар ха-Медина", "Лобби башен Кикар ха-Медина"),
    "fac_lbl": ("Бассейн", "Тренажёрный зал", "Спа", "Лобби"),
    "fac_cap": "<b>Иллюстративная визуализация удобств:</b> не съёмка и не официальная спецификация.",  # the clip's own wording
}.items()}
RU_F = figures(RU_T)
RU_TOWERS = ("<h3>Сколько этажей и какой высоты каждая башня?</h3>"
             "<p>В двух башнях по 40 этажей, в одной 37. В таблице собрано то, что опубликовано о каждой башне; число квартир в каждой башне не опубликовано.</p>"
             + table(("Башня", "Положение на участке", "Этажи", "Опубликованная высота"),
                     (("Башня A", "На юго-западе участка", "40 этажей", "Около 160 м"),
                      ("Башня B", "На юго-востоке участка", "37 этажей", "Около 157 м"),
                      ("Башня C", "На северо-востоке участка", "40 этажей", "Около 160 м"))))
RU_DIFF = ("<p><strong>Цифры, которые расходятся в разных публикациях.</strong> Часть данных о проекте публикуется в нескольких вариантах. "
           "В таблице показаны варианты, найденные в ноябре 2026 года, и цифра, которая используется на этой странице.</p>"
           + table(("Показатель", "Что указано в публикациях", "Что указано на этой странице"), (
               ("Этажность", "В публикациях: три башни по 40 этажей, а также две по 40 этажей и одна в 37", "На этой странице: 40, 37 и 40 этажей, по данным строительной компании"),
               ("Высота", "В публикациях: до примерно 160 м для всех башен, а также 160 м для двух и 157 м для третьей", "На этой странице: до примерно 160 м; башня B, в 37 этажей, — примерно 157 м"),
               ("Число квартир", "В публикациях: около 450, а также 453", "На этой странице: 453 квартиры"),
               ("Владельцы земли", "В публикациях: около 150, а также около 250", "На этой странице: около 250 владельцев прав"),
               ("Площадь", "В публикациях: около 27 дунамов, около 50 дунамов, а также около 78 дунамов", "На этой странице: около 78 дунамов — площадь всего плана, а один только общественный парк — около 40 дунамов; в публикациях с цифрами около 27 и около 50 дунамов не указано, что именно измерено"),
               ("Окончание строительства", "В публикациях: 2026 год, а также апрель 2027 года", "На этой странице: о завершении строительства башен объявлено в октябре 2026 года, а передача квартир ожидается между первым кварталом 2027 года и маем 2027 года"))))
RU_FAQ = _ru("<h3>Сколько этажей в башнях Кикар ха-Медина?</h3>"
             "<p>В башнях A и C по 40 этажей, в башне B 37. Под башнями расположены три подземных уровня парковки. Каждый этаж повёрнут на 1,25 градуса относительно нижнего, поэтому квартиры на одной стороне башни на разных этажах смотрят в немного разные стороны. Выбирая этаж, запросите план именно этого этажа и проверьте, куда выходят салон и балкон.</p>"
             "<h3>Какой адрес у башен Кикар ха-Медина?</h3>"
             "<p>Башни стоят внутри площади Кикар ха-Медина на севере Тель-Авива, в районе Новый Север; адреса в разрешениях на строительство — He Be’Iyar 25, 45 и 65. Улица He Be’Iyar окружает площадь, улица Вейцман подходит к ней с юга, а улица Жаботинского — с востока. Спрашивая о квартире, уточните адрес башни и номер квартиры: общий адрес «Кикар ха-Медина» подходит и к домам кольца вокруг площади.</p>"
             "<h3>Кто застройщик башен Кикар ха-Медина и является ли проект покупательской группой?</h3>"
             "<p>Проект возводят сами владельцы земли: около 250 владельцев прав, наследники тех, кто купил участки в 1942 году. В 1997 году они объединились и действуют через компанию владельцев земли. Квартиры они получили в обмен на землю, а очерёдность выбора квартир определила жеребьёвка. В поиске проект иногда называют покупательской группой (квуцат рехиша); на деле это объединение владельцев земли, а не группа, которая вместе купила участок. Застройщика, который продаёт новые квартиры всем желающим, нет: сегодня покупают квартиру или право на неё у одного из владельцев прав.</p>"
             "<h3>Кто архитектор башен Кикар ха-Медина?</h3>"
             "<p>Башни спроектировало бюро Yaski Mor Sivan Architects, выбранное по итогам конкурса в 2000 году. В основе проекта поворачивающаяся оболочка: каждый этаж смещён на 1,25 градуса относительно нижнего. Ландшафтный проект выполнило бюро T.M.A., а управление проектом координирует Waxman Govrin Geva (WXG). План и спецификацию конкретной квартиры получайте у продавца, а не из общего описания проекта.</p>"
             "<h3>Какая плата за обслуживание дома (ваад байт) в башнях Кикар ха-Медина?</h3>"
             "<p>Официальный тариф платы за управление не опубликован. " + RU_EST + ", плата за обслуживание составит около 4~000–5~000~₪ в месяц за квартиру, в зависимости от её площади. Оценка относится к дому с помещениями для жильцов, в том числе с бассейном, спа и тренажёрным залом. Это предварительная оценка, сделанная до заселения. Прежде чем решать, запросите ежемесячный платёж для конкретной квартиры и перечень входящих в него услуг.</p>")
RU_SWAPS = [(_ru(a), _ru(b)) for a, b in [
    # 1. the facts table: height per tower
    ("Высота комплекса достигает примерно 160 м.</td>",
     "Высота комплекса достигает примерно 160 м. По опубликованным данным, башни A и C достигают примерно 160 м, а башня B — примерно 157 м.</td>"),
    # 2. the project manager's short name, as people search it
    ("Управление проектом ведёт Waxman Govrin Geva, участвующая", "Управление проектом ведёт Waxman Govrin Geva (WXG), участвующая"),
    # 3. the aerial picture before the facts table
    ("<table><tbody><tr><th>Расположение</th>", RU_F["aerial"] + "<table><tbody><tr><th>Расположение</th>"),
    # 4. after the facts table: the numbers that publications give differently
    ("</tbody></table></section><section class=\"nlws\" id=\"nlws-choose\">",
     "</tbody></table>" + RU_DIFF + "</section><section class=\"nlws\" id=\"nlws-choose\">"),
    # 5. the three towers side by side, and their pictures (this page puts the directions before the rotation)
    ("<h3>Что находится вокруг и где искать вид на море</h3>", RU_TOWERS + RU_F["towers"] + "<h3>Что находится вокруг и где искать вид на море</h3>"),
    # 6-8. the views: the four directions after the directions table, the balcony after the rotation, the floors at the end
    ("<h3>Почему поворот этажа меняет выбор</h3>", RU_F["dirs"] + "<h3>Почему поворот этажа меняет выбор</h3>"),
    ("<h3>Нижний или высокий этаж: за что платить</h3>", RU_F["balcony"] + "<h3>Нижний или высокий этаж: за что платить</h3>"),
    ("</p></section><section class=\"nlws\" id=\"nlws-homes\">", "</p>" + RU_F["floors"] + "</section><section class=\"nlws\" id=\"nlws-homes\">"),
    # 9. the example apartment
    ("<h3>Как читать площадь и планировку</h3>", RU_F["home"] + "<h3>Как читать площадь и планировку</h3>"),
    # 10. the facilities
    ("<h3>Подъём домой, климат и домашние дела</h3>", RU_F["fac"] + "<h3>Подъём домой, климат и домашние дела</h3>"),
    # 11. the building fee
    ("<p>Управляющая компания и размер ежемесячной платы за обслуживание не опубликованы.",
     "<p>Управляющая компания и официальный размер ежемесячной платы за обслуживание не опубликованы. " + RU_EST + ", плата за обслуживание дома (ваад байт) в башнях составит около 4~000–5~000~₪ в месяц за квартиру, в зависимости от её площади. Это предварительная оценка, сделанная до заселения."),
    # 12-13. rent
    ("Арендные ставки для комплекса не опубликованы.",
     "Договоры аренды, реально заключённые в башнях, пока не опубликованы: башни ещё не заселены. " + RU_EST + ", квартира в башнях будет сдаваться примерно за 25~000~₪ в месяц; это предварительная оценка, а не договор аренды."),
    ("Пока для башен нет опубликованной ставки,", "Пока для башен нет ставки из реальных договоров,"),
    # 14. the height answer
    ("<p>Высота башен достигает примерно 160 м: в башнях A и C по 40 этажей, в башне B 37.",
     "<p>Высота башен достигает примерно 160 м: в башнях A и C по 40 этажей, в башне B 37. По опубликованным данным, башни A и C достигают примерно 160 м, а башня B — примерно 157 м."),
    # 15. five questions people search, after "who is building"
    ("<h3>Что такое Кикар ха-Медина в Тель-Авиве?</h3>", RU_FAQ + "<h3>Что такое Кикар ха-Медина в Тель-Авиве?</h3>"),
]]

# ------------------------------------------------------------------------------------------------------------------------ Arabic
# the page's own terms and figures: Western digits with a comma for thousands, Levantine month names, أصحاب الحقوق, شركة أصحاب الأرض,
# الصالون, رسوم الإدارة, الشمال الجديد, قسائم, رابطة (1997)
AR_EST = "ووفق تقدير لأحد العاملين في مجال العقارات نُشر في تشرين الأول 2026"
AR_T = {
    "label": "تصور توضيحي.",  # the page's own label (the film block, 1.72.646)
    "aerial_alt": "أبراج كيكار همدينا الثلاثة داخل الساحة في تل أبيب، منظر من الجو",
    "aerial_cap": "أبراج كيكار همدينا الثلاثة داخل الساحة، منظر من الجو باتجاه البحر.",
    "tower_alt": "البرج %s في أبراج كيكار همدينا، %d طابقاً", "tower_lbl": "البرج %s",
    "towers_cap": "كل برج على حدة: A وC من 40 طابقاً، وB من 37 طابقاً.",
    "balcony_alt": "المنظر من شرفة في الطابق 30 في البرج C، أبراج كيكار همدينا، باتجاه الغرب",
    "balcony_cap": "المنظر من شرفة في الطابق 30 في البرج C باتجاه الغرب، قبيل الغروب.",
    "dir_alt": "المنظر %s من الطابق 30 في أبراج كيكار همدينا", "dir_w": ("باتجاه الشمال", "باتجاه الشرق", "باتجاه الجنوب", "باتجاه الغرب"),
    "dir_lbl": ("الشمال", "الشرق", "الجنوب", "الغرب"),
    "dirs_cap": "المنظر من الطابق 30 في البرج C في أربعة اتجاهات. المنظر من شقة محددة يتوقف على البرج والطابق والاتجاه.",
    "floor_alt": "المنظر باتجاه الغرب من الطابق %d في أبراج كيكار همدينا", "floor_lbl": "الطابق %d",
    "floors_cap": "الاتجاه نفسه، الغرب، من ثلاثة طوابق في البرج C.",
    "living_alt": "الصالون في شقة نموذجية في الطابق 30 في أبراج كيكار همدينا", "living_lbl": "الصالون",
    "bed_alt": "غرفة نوم في شقة نموذجية في الطابق 30 في أبراج كيكار همدينا", "bed_lbl": "غرفة النوم",
    "home_cap": "الصالون وغرفة النوم في شقة نموذجية في الطابق 30؛ ليست صورة فوتوغرافية ولا مواصفات رسمية.",
    "fac_alt": ("المسبح في أبراج كيكار همدينا", "النادي الرياضي في أبراج كيكار همدينا", "السبا في أبراج كيكار همدينا", "بهو الاستقبال في أبراج كيكار همدينا"),
    "fac_lbl": ("المسبح", "النادي الرياضي", "السبا", "البهو"),
    "fac_cap": "<b>تصوّر توضيحي للمرافق:</b> ليس تصويرًا حقيقيًا ولا مواصفات رسمية.",  # the clip's own wording
}
AR_F = figures(AR_T)
AR_TOWERS = ("<h3>كم طابقاً في كل برج وما ارتفاعه؟</h3>"
             "<p>برجان من 40 طابقاً وبرج واحد من 37 طابقاً. يجمع الجدول ما نُشر عن كل برج؛ عدد الشقق في كل برج غير منشور.</p>"
             + table(("البرج", "الموقع في قطعة الأرض", "الطوابق", "الارتفاع المنشور"),
                     (("البرج A", "في الجنوب الغربي من قطعة الأرض", "40 طابقاً", "نحو 160 متراً"),
                      ("البرج B", "في الجنوب الشرقي من قطعة الأرض", "37 طابقاً", "نحو 157 متراً"),
                      ("البرج C", "في الشمال الشرقي من قطعة الأرض", "40 طابقاً", "نحو 160 متراً"))))
AR_DIFF = ("<p><strong>أرقام تختلف بين المنشورات.</strong> تُنشر بعض معطيات المشروع بأكثر من صيغة. يعرض الجدول الصيغ التي وُجدت في تشرين الثاني 2026 والرقم المعتمد في هذه الصفحة.</p>"
           + table(("المعطى", "ما يرد في المنشورات", "ما تعتمده هذه الصفحة"), (
               ("الطوابق", "في المنشورات: ثلاثة أبراج من 40 طابقاً، وأيضاً برجان من 40 طابقاً وبرج من 37", "في هذه الصفحة: 40 و37 و40 طابقاً، وفق تفصيل شركة البناء"),
               ("الارتفاع", "في المنشورات: حتى نحو 160 متراً لكل الأبراج، وأيضاً 160 متراً لبرجين و157 متراً للثالث", "في هذه الصفحة: حتى نحو 160 متراً؛ والبرج B، ذو الـ37 طابقاً، نحو 157 متراً"),
               ("عدد الشقق", "في المنشورات: نحو 450، وأيضاً 453", "في هذه الصفحة: 453 شقة"),
               ("أصحاب الأرض", "في المنشورات: نحو 150، وأيضاً نحو 250", "في هذه الصفحة: نحو 250 صاحب حقوق"),
               ("المساحة", "في المنشورات: نحو 27 دونماً، ونحو 50 دونماً، وأيضاً نحو 78 دونماً", "في هذه الصفحة: نحو 78 دونماً هي مساحة المخطط كله، والحديقة العامة وحدها نحو 40 دونماً؛ ولا توضح المنشورات التي تذكر نحو 27 ونحو 50 دونماً ما الذي قيس"),
               ("انتهاء البناء", "في المنشورات: 2026، وأيضاً نيسان 2027", "في هذه الصفحة: أُعلن عن اكتمال بناء الأبراج في تشرين الأول 2026، ويُتوقع تسليم الشقق بين الربع الأول من 2027 وأيار 2027"))))
AR_FAQ = ("<h3>كم طابقاً في أبراج كيكار همدينا؟</h3>"
          "<p>يتكون البرجان A وC من 40 طابقاً، والبرج B من 37 طابقاً. وتحت الأبراج ثلاثة مستويات لمواقف السيارات تحت الأرض. ويلتف كل طابق بمقدار 1.25 درجة عن الطابق الذي تحته، لذا تتجه الشقق الواقعة في الجهة نفسها من البرج اتجاهاً مختلفاً قليلاً في كل طابق. عند اختيار الطابق، اطلبوا مخطط هذا الطابق تحديداً وتحققوا من جهة الصالون والشرفة.</p>"
          "<h3>ما عنوان أبراج كيكار همدينا؟</h3>"
          "<p>تقع الأبراج داخل ساحة كيكار همدينا في تل أبيب، في الشمال الجديد، وعناوينها في رخص البناء هي He Be’Iyar 25 و45 و65. يحيط شارع He Be’Iyar بالساحة، ويصل إليها شارع Weizmann من الجنوب وشارع Jabotinsky من الشرق. عند الاستفسار عن شقة، اطلبوا عنوان البرج ورقم الشقة، لأن العنوان العام «كيكار همدينا» يصدق أيضاً على مباني الحلقة المحيطة بالساحة.</p>"
          "<h3>من المطوّر في أبراج كيكار همدينا، وهل هي مجموعة شراء؟</h3>"
          "<p>يقيم المشروعَ أصحابُ الأرض أنفسهم: نحو 250 صاحب حقوق، هم ورثة من اشتروا القسائم عام 1942، وقد أسسوا رابطة عام 1997 ويعملون من خلال شركة أصحاب الأرض. حصلوا على شقق مقابل الأرض، وتحدد ترتيب اختيار الشقق بالقرعة. في عمليات البحث يُسمّى المشروع أحياناً مجموعة شراء؛ لكنه فعلياً اتحاد لأصحاب الأرض، لا مجموعة اشترت الأرض معاً. لا يوجد مطوّر يبيع شققاً جديدة للجمهور: من يشتري اليوم يشتري شقة، أو حقاً في شقة، من أحد أصحاب الحقوق.</p>"
          "<h3>من المهندس المعماري لأبراج كيكار همدينا؟</h3>"
          "<p>صمّم الأبراجَ مكتب Yaski Mor Sivan، الذي اختير في مسابقة معمارية عام 2000. يقوم التصميم على غلاف ملتف: كل طابق مُزاح بمقدار 1.25 درجة عن الطابق الذي تحته. هندسة المشهد من T.M.A.، وتنسّق Waxman Govrin Geva (WXG) إدارة المشروع. احصلوا على مخطط الشقة المحددة ومواصفاتها من البائع، لا من الوصف العام للتصميم.</p>"
          "<h3>كم تبلغ رسوم لجنة البيت في أبراج كيكار همدينا؟</h3>"
          "<p>لم تُنشر تعريفة رسمية لرسوم الإدارة. " + AR_EST + "، يُتوقع أن تبلغ رسوم الصيانة نحو 4,000 إلى 5,000 ₪ للشقة شهرياً، بحسب مساحتها. ويتعلق التقدير بمبنى فيه مرافق للسكان، منها مسبح وسبا ونادٍ رياضي. هذا تقدير مبكر قبل السكن. قبل اتخاذ القرار، اطلبوا الرسوم الشهرية للشقة المحددة وقائمة الخدمات التي تشملها.</p>")
AR_SWAPS = [
    # 1. the facts table: height per tower
    ("الارتفاع يصل إلى نحو 160 متراً.</td>",
     "الارتفاع يصل إلى نحو 160 متراً. ووفق المعطيات المنشورة، يصل البرجان A وC إلى نحو 160 متراً، والبرج B إلى نحو 157 متراً.</td>"),
    # 2. the project manager's short name, as people search it
    ("إدارة المشروع لدى Waxman Govrin Geva منذ 2001", "إدارة المشروع لدى Waxman Govrin Geva (WXG) منذ 2001"),
    # 3. the aerial picture before the facts table
    ("<table><tbody><tr><th>الموقع</th>", AR_F["aerial"] + "<table><tbody><tr><th>الموقع</th>"),
    # 4. at the end of the facts section (this page closes it with a paragraph after the table): the numbers publications give differently
    ("</p></section><section class=\"nlws\" id=\"nlws-choose\">", "</p>" + AR_DIFF + "</section><section class=\"nlws\" id=\"nlws-choose\">"),
    # 5. the three towers side by side, and their pictures
    ("<h3>ماذا يغيّر التفاف الطوابق؟</h3>", AR_TOWERS + AR_F["towers"] + "<h3>ماذا يغيّر التفاف الطوابق؟</h3>"),
    # 6-8. the views
    ("<h3>ما الذي يقع في كل اتجاه؟</h3>", AR_F["balcony"] + "<h3>ما الذي يقع في كل اتجاه؟</h3>"),
    ("<h3>هل تختارون طابقاً منخفضاً أم مرتفعاً؟</h3>", AR_F["dirs"] + "<h3>هل تختارون طابقاً منخفضاً أم مرتفعاً؟</h3>"),
    ("</p></section><section class=\"nlws\" id=\"nlws-homes\">", "</p>" + AR_F["floors"] + "</section><section class=\"nlws\" id=\"nlws-homes\">"),
    # 9. the example apartment
    ("<h3>ماذا تتضمن المواصفات المنشورة؟</h3>", AR_F["home"] + "<h3>ماذا تتضمن المواصفات المنشورة؟</h3>"),
    # 10. the facilities
    ("<h3>الموقف والمصاعد والخدمات اليومية</h3>", AR_F["fac"] + "<h3>الموقف والمصاعد والخدمات اليومية</h3>"),
    # 11. the building fee
    ("اسم شركة الإدارة وقيمة الرسوم الشهرية غير منشورين.",
     "اسم شركة الإدارة وتعريفة رسمية للرسوم الشهرية غير منشورين. " + AR_EST + "، يُتوقع أن تبلغ رسوم الصيانة (لجنة البيت) في الأبراج نحو 4,000 إلى 5,000 ₪ للشقة شهرياً، بحسب مساحتها. هذا تقدير مبكر قبل السكن."),
    # 12. rent
    ("ولم تُنشر أسعار إيجار لها.",
     "ولم يُنشر بعدُ إيجار أُبرم فعلاً فيها، لأن الأبراج لم تُسكن بعد. " + AR_EST + "، ستُؤجَّر الشقة في الأبراج بنحو 25,000 ₪ شهرياً؛ هذا تقدير مبكر، لا عقد إيجار."),
    # 13. the height answer
    ("يصل ارتفاع الأبراج إلى نحو 160 م، ويتكون البرجان A وC من 40 طابقاً، بينما يتكون B من 37 طابقاً.",
     "يصل ارتفاع الأبراج إلى نحو 160 م، ويتكون البرجان A وC من 40 طابقاً، بينما يتكون B من 37 طابقاً. ووفق المعطيات المنشورة، يصل البرجان A وC إلى نحو 160 م، والبرج B إلى نحو 157 م."),
    # 14. five questions people search, after "who is building"
    ("<h3>ما هو كيكار همدينا في تل أبيب؟</h3>", AR_FAQ + "<h3>ما هو كيكار همدينا في تل أبيب؟</h3>"),
]

POSTS = {
    "ar": (8118, "hamedina-ar", "687e3e9ea921d15915518fa9a18deefd", AR_SWAPS),  # modified 2026-11-11T03:49:56 (HAD-709)
    "ru":(8117, "hamedina-ru", "772b0464f8dc1ea0c023572258254eaf", RU_SWAPS),  # modified 2026-11-11T03:49:54 (HAD-709)
    "en":(8114, "hamedina-en", "d6bbb5ceda58dd611fa2ced2731b7cbd", EN_SWAPS),  # modified 2026-11-11T03:49:48 (HAD-709); written 11.11 18:50
    "fr": (8116, "hamedina-fr", "f1256765874cd9ef0db923d27fc7f913", FR_SWAPS),  # modified 2026-11-11T03:49:51 (HAD-709)
}


def apply(raw, swaps):
    for old, new in swaps:
        c = raw.count(old)
        if c != 1:
            raise SystemExit("anchor x%d: %s" % (c, old[:90]))
        raw = raw.replace(old, new)
    return raw


if __name__ == "__main__":
    lang = next((a for a in sys.argv[1:] if not a.startswith("--")), "")
    if lang not in POSTS:
        raise SystemExit("usage: had712_lang.py <%s> [--go]" % "|".join(POSTS))
    GO = "--go" in sys.argv
    src = open(os.path.join(REPO, "scripts", "skin-a", "deployskin.py"), encoding="utf-8").read(); ns = {"__name__": "h712l"}
    exec(compile(src[:src.index('s, h, _ = req("GET", "/wp-json/nadlan/v1/health")')], "h", "exec"), ns); req = ns["req"]
    PID, SLUG, PIN, SWAPS = POSTS[lang]
    GAL = os.path.join(REPO, "plugins", "nadlan-config", "assets", "project-stage", "hamedina", "gallery")
    s, g, _ = req("GET", "/wp-json/wp/v2/nadlan_project/%d?context=edit&_fields=id,slug,modified,content" % PID)
    assert s == 200 and g["slug"] == SLUG, (s, g.get("slug"))
    raw = g["content"]["raw"]
    now = hashlib.md5(raw.encode("utf-8")).hexdigest()
    if now != PIN:
        raise SystemExit("the live post changed since it was read (%s, modified %s): read it again before replacing anything" % (now[:10], g["modified"]))
    new = apply(raw, SWAPS)
    for f in set(x.split('"')[0] for x in new.split(G)[1:]):
        assert os.path.isfile(os.path.join(GAL, f)), "no gallery file " + f
    assert new.count("<table>") == raw.count("<table>") + 2 and new.count("</table>") == new.count("<table>")
    assert new.count("<h3>") == raw.count("<h3>") + 6 and new.count("<h2>") == raw.count("<h2>")
    assert new.count("<figure") == 7 and new.count("</figure>") == 7 and new.count("<img ") == raw.count("<img ") + 18
    print("[plan] %s post %d: %d replacements, 7 figures, 18 pictures, 6 headings; %d -> %d chars" % (lang, PID, len(SWAPS), len(raw), len(new)))
    if not GO:
        io.open(os.path.join(HERE, "_had712_%s_preview.html" % lang), "w", encoding="utf-8", newline="").write(new)
        sys.exit(0)
    bk = os.path.join(REPO, "docs", "qa", "had-712"); os.makedirs(bk, exist_ok=True)
    stamp = time.strftime("%Y%m%dT%H%M%S")
    io.open(os.path.join(bk, "backup-%d-%s.html" % (PID, stamp)), "w", encoding="utf-8", newline="").write(raw)
    s1, r1, _ = req("POST", "/wp-json/wp/v2/nadlan_project/%d" % PID, {"content": new})
    assert s1 in (200, 201), (s1, str(r1)[:300])
    s, r, _ = req("GET", "/wp-json/wp/v2/nadlan_project/%d?context=edit&_fields=content,modified" % PID)
    ok = r["content"]["raw"] == new
    res = {"lang": lang, "post": PID, "before_md5": now, "after_md5": hashlib.md5(r["content"]["raw"].encode("utf-8")).hexdigest(),
           "read_back_equal": ok, "modified": r.get("modified"), "replacements": len(SWAPS)}
    json.dump({"stamp": stamp, "result": res}, open(os.path.join(bk, "result-%s-%s.json" % (lang, stamp)), "w", encoding="utf-8"), indent=1)
    if not ok:  # put the old text back and stop
        sb, _, _ = req("POST", "/wp-json/wp/v2/nadlan_project/%d" % PID, {"content": raw})
        raise SystemExit("read-back differs: restored the backup (http %s)" % sb)
    print("[done] %s post %d written and read back; backup and result in docs/qa/had-712/ (%s)" % (lang, PID, stamp))
