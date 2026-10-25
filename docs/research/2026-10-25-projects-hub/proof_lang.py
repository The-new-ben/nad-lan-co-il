# -*- coding: utf-8 -*-
"""Depth proof per language (Ben 25.10.2026: the language hubs must be above every competitor page). Runs tools/depth_proof.py with
our /<lang>/projects/ against the first-page pages read in lang-dna-<lang>.md (URLs = the canonicals of the saved raw pages).
  python docs/research/2026-10-25-projects-hub/proof_lang.py en|ru|fr  -> proof-depth-<lang>.md"""
import os, subprocess, sys
H = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.dirname(os.path.dirname(H))
THEM = {
    "en": ["https://homeinisrael.com/en/new-projects/", "https://www.buyitinisrael.com/projects/",
           "https://www.immobilier.co.il/en/city/telaviv/new-projects",
           "https://www.barnes-international.com/en/new-development/israel/tel-aviv-yafo.html",
           "https://www.myplace.co.il/en/new-projects/", "https://www.onmap.co.il/en/projects/tel-aviv-yafo",
           "https://newkey.co.il/en/projects/", "https://www.israel-properties.com/new-projects", "https://sellingisrael.com/",
           "https://semerenkogroup.com/new-projects/",
           "https://www.strn.co.il/practice/real-estate-attorney-israel/buying-property-from-a-developer/"],
    "ru": ["https://www.immobilier.co.il/ru/%D0%BD%D0%BE%D0%B2%D0%BE%D1%81%D1%82%D1%80%D0%BE%D0%B9%D0%BA%D0%B8",
           "https://www.immobilier.co.il/ru/%D0%B3%D0%BE%D1%80%D0%BE%D0%B4/telaviv/%D0%BD%D0%BE%D0%B2%D0%BE%D1%81%D1%82%D1%80%D0%BE%D0%B9%D0%BA%D0%B8",
           "https://newkey.co.il/ru/projects/", "https://newkey.co.il/ru/new-projects/telaviv/",
           "https://tranio.ru/israel/apartments/new-homes/", "https://geoln.com/ru/israel", "https://isratowers.com/projects/",
           "https://www.onmap.co.il/ru/projects/tel-aviv-yafo", "https://bhii.co.il/ru/real-estate/new-projects"],
    "fr": ["https://www.barnes-israel.com/fr/acheter/programmes-neufs.html",
           "https://www.barnes-international.com/fr/programme-neuf/israel/tel-aviv-yafo.html",
           "https://e-projects.fr/projets-immobiliers-a-tel-aviv/", "https://immoneuf.co.il/ville/tel-aviv/",
           "https://www.ba-hit.com/projets-neufs/", "https://www.evenisgroup.com/projets-neufs/tel-aviv/",
           "https://www.immobilier.co.il/ville/telaviv/projets-neufs",
           "https://www.comacom.co.il/projets-neufs-en-israel-immobilier-neuf/",
           "https://acheter-appartement-israel.com/articles/immobilier-neuf-en-isra-l-comment-bien-choisir-sur-plan.html",
           "https://www.yafoinvest.com/fr/neuf/tel-aviv"],
}
lang = sys.argv[1]
cmd = [sys.executable, os.path.join(REPO, "tools", "depth_proof.py"), "--ours", "https://nad-lan.co.il/%s/projects/" % lang,
       "--them"] + THEM[lang] + ["--out", os.path.join(H, "proof-depth-%s.md" % lang)]
sys.exit(subprocess.call(cmd))
