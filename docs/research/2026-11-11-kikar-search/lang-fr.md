# Kikar Hamedina towers in French: how people search, and what the French page needed (11.11.2026)

Page: https://nad-lan.co.il/projects/hamedina-fr/ (post 8116). Kikar languages session (Opus 5.5), HAD-712.
MEASURED = read today; INFERENCE = my reading; NOT CHECKED = said plainly.

## Sources
- Search Console, 90 days: one French query on the French page in 90 days ("prix des appartements", France, 1 impression, position 1).
  File `gsc-hamedina-fr-2026-08-13_2026-11-10.csv`.
- Autocomplete, hl=fr, gl=fr and gl=il, 10 seeds: `autocomplete-fr.json`.
- Two hand searches in Ben's Chrome (gmktec), google.fr, hl=fr, gl=fr, pws=0, about 22:00 local; screenshots in `manual-fr-2026-11-11/`.
  No robot check. Two page loads in all.
- Search volumes: NOT AVAILABLE (DataForSEO balance zero).

## MEASURED
1. French searchers name the project in its Latin form, not in French: "kikar hamedina" gives the same continuations as in English
   (tel aviv, plan, stores, towers, towers for sale, map, shops, project). "tours kikar hamedina" -> "tour kikar hamedina" only.
2. French area and buyer continuations:
   - "acheter appartement tel aviv" -> neve tzedek, studio, vente appartement tel aviv particulier, florentine, maison, achat appartement luxe tel aviv.
   - "appartement de luxe tel aviv" -> immobilier de luxe tel aviv, location appartement luxe, achat appartement luxe.
   - "prix appartement tel aviv" -> prix studio, location (longue durée, particulier), prix immobilier tel aviv, vente ... particulier.
   - "acheter en israel" -> acheter un appartement en israel, acheter un bien en israel, comment acheter en israel.
   - "taxe d'acquisition israel" -> "taxe d acquisition israel 2025". "pret immobilier israel non resident" -> no suggestion.
3. google.fr, "tours kikar hamedina tel aviv": an AI answer that reads "tours" as visits (sightseeing, walks, shopping); then a Facebook
   post (Kef Israel), then **our French page, second organic result** ("Tours Kikar Hamedina à Tel Aviv : appartements, prix et 3D"),
   then ogo.co.il, Expedia, Ashtrom, ip-tlv.com ("KIKAR HAMEDINA TOWERS | TEL AVIV - FOR SALE", French text), Tripadvisor, Rome2Rio, DUO.
   Related searches: Kikar Hamedina towers, Kikar Hamedina towers for sale.
4. google.fr, "kikar hamedina appartement à vendre": Hebrew ads (Yoshpe, First to Sea, Electra, Infinity); an AI answer with prices
   **in euros beside shekels** (sources it names: BARNES International, Neot Shiran, Immo-IL, Le Figaro Propriétés); organic: BARNES Israel,
   immobilier-telaviv.com (prices in ₪, $ and €), a Facebook group of French speakers in Tel Aviv, EvenisGroup, BARNES International,
   luxury-realestate-israel.com ("Appartement à vendre dans le projet Kikar HaMedina", Bâtiment C, 12e étage, nord-ouest, 5 pièces),
   immo-il.com, Le Figaro Propriétés. **nad-lan.co.il is not on page one** for this query.

## INFERENCE
- The French reader is a buyer from France or Belgium who works with French-speaking agencies and thinks in euros. Every French
  competitor on page one prints euros. The page printed shekels only.
- "vente ... particulier" is how French buyers search for a private sale. These towers are only that: owners resell, there is no developer.
- "location longue durée" is the French rent search; the page answered rent but not in those words.
- The ambiguity of "tours" (towers / visits) is not ours to fix; the page title already pairs "tours" with "appartements, prix et 3D".

## Done on 11.11.2026 (scripts/kikar/had712_fr_intent.py, post 8116, backup in docs/qa/had-712/)
- The opening: the 2024 deal range gains "soit environ 2,75 à 3,05 M€ au cours de la Banque d’Israël du 23 octobre 2026".
- The prices chapter: one paragraph on how the euro figures are made (shekels are the price; Bank of Israel representative rate
  of 23.10.2026, 1 € = 3,4844 ₪, from the site's own file assets/instruments/data/boi-fx.json; 10 M₪ ≈ 2,87 M€; it moves with the rate).
  Ben's rule of 25.10.2026: the shekel stays the price; the foreign figure is approximate and dated.
- The sale chapter: "Il s’agit donc de ventes entre particuliers : le vendeur est le propriétaire de l’appartement, et non un promoteur."
- The rent paragraph: "en location longue durée".
- No FAQ answer changed (no schema release needed). Title and H1 untouched.

## NOT CHECKED
- Belgian (gl=be) and Swiss (gl=ch) results; Bing.
- Whether the French page will rise for "appartement à vendre": re-measure on 25.11.2026 with the other pages.
- The French showroom: not started (Ben: the showroom in English only for now).
