# /fr/projects/ : French SERP DNA, French buyer vocabulary and needs (read 25.10.2026)

Research only, Opus 5.5 sub-agent, 25.10.2026, about 11:29 to 12:05 Israel time. Nothing on nad-lan.co.il was touched and no copy was written for our site.
Inputs: `serp-lang.md` (French SERPs), `languages.md` (GSC demand, safe URL `/fr/projects/`), `competitors/dna.md`, `facts.md` (same folder).

How the pages were read: curl with a Chrome 141 user agent and `Accept-Language: fr-FR`, raw HTML only (view-source, not the rendered DOM). Raw files are saved outside the repo in
`C:\Users\777\nad-lan\_private-research\2026-10-25-projects-hub\raw-fr\` (20 files). Text was extracted with a stdlib parser. Words are counted on the editorial text with the card grid, menus, footers and form country lists left out (the raw count is given where it differs).
Official checks used the BOI SDMX API, Tax Authority and BOI PDFs, Wikisource law texts, service-public.gouv.fr, BOFiP, INSEE and Kol Zchut (Kol Zchut was read in the owner's Chrome "gmktec").
Demand data: the GSC 90-day query+page export already in the session scratchpad (25.7 to 23.10.2026, read only) and DataForSEO Google Ads search volume for France, Belgium, Switzerland and Israel in French (4 saved calls at $0.09 each plus one earlier MCP call whose view was truncated, about $0.45 in total; saved in `C:\Users\777\Documents\GSC-Data\dataforseo\nad-lan-co-il-2026-10-25-fr\`).
Legifrance (bot wall) and impots.gouv.fr (maintenance page) could not be opened. Each item says what it rests on: **verified** means an official text opened today or in the dated earlier file named; **secondary** means a reliable non-official source; **unverified** means no official text was found.

---

## 0. The French SERP in one view

| Page | Type | Ranks for (serp-lang.md) | Words (editorial) | Cards | € shown | FAQ | Schema |
|---|---|---|---|---|---|---|---|
| barnes-israel.com/fr/acheter/programmes-neufs.html | broker (luxury) | projet immobilier israël #1, programme neuf tel aviv, acheter appartement neuf israël, appartement neuf tel aviv | ~314 | 25 | switcher only | 0 | none |
| barnes-international.com/fr/programme-neuf/israel/tel-aviv-yafo.html | broker network | projet immobilier israël, programme neuf tel aviv (#1), acheter appartement neuf israël, programme neuf israël (#1) | ~0 | 17 | **yes, € and ₪ on every card** | 0 | BreadcrumbList |
| e-projects.fr/nos-projets/ | agency (FR + IL phones) | projet immobilier israël, acheter appartement neuf israël | ~12 | 9 (page 1 of 5) | no | 0 | WebPage, Breadcrumb |
| e-projects.fr/projets-immobiliers-a-tel-aviv/ | same | programme neuf tel aviv | ~10 | 6 | no | 0 | WebPage, Breadcrumb |
| immoneuf.co.il (home) | francophone portal | projet immobilier israël, programme neuf tel aviv, acheter appartement neuf israël | ~96 + blog teasers | ~31 | no | 4 in schema, **not visible** | FAQPage, RealEstateAgent, Organization |
| immoneuf.co.il/ville/tel-aviv/ | same | appartement neuf tel aviv | ~224 | 24 (new + resale) | no | 1 visible | CollectionPage |
| alloj.com/fr/immobilier-israel.html | kosher-lifestyle directory | projet immobilier israël, acheter appartement neuf israël | ~234 + 357 boilerplate | 12 (incl. lawyer, accountant, Cyprus) | no | 3 visible, no schema | none |
| alloj.com/fr/projet-immobilier-neuf-israel.html | same | (requested) | ~0 | 16 | no | 0 | none, **empty title and meta** |
| ba-hit.com/projets-neufs/ | agency | projet immobilier israël, programme neuf tel aviv, appartement neuf tel aviv | ~28 | 32 (most "vendu") | land priced in € | 0 | none |
| evenisgroup.com/projets-neufs/tel-aviv/ | agency network | projet immobilier israël, programme neuf tel aviv, appartement neuf tel aviv | ~62 + ~60 dated listing posts | ~60 | live EUR/ILS and USD/ILS widget | 0 | Organization, WebPage, Breadcrumb |
| immobilier.co.il/ville/telaviv/projets-neufs | portal since 2004, 8 languages | programme neuf tel aviv, appartement neuf tel aviv (#1) | ~287 intro + ~284 FAQ | 5 server-rendered (146 total) | **yes, ₪ + $ + €** | 5 visible + FAQPage | CollectionPage + Product/AggregateOffer, FAQPage, Breadcrumb |
| comacom.co.il/projets-neufs-en-israel-immobilier-neuf/ | agency | acheter appartement neuf israël | 0 | 9 (110 total) | no | 0 | none, no meta description |
| acheter-appartement-israel.com (immobilier neuf article) | lead-gen guide | acheter appartement neuf israël | ~2,600 | 0 | no | 1 + FAQPage | Article, FAQPage, Breadcrumb |
| shoshia-law.com/fr/blog/buying-from-developer-12-risks/ | law firm (Netanya) | acheter appartement neuf israël | ~520 | 0 | no | 1 real + 1 broken, FAQPage | LegalService, Person, HowTo, FAQPage, AggregateRating, Speakable |
| extra in the SERP: yafoinvest.com/fr/neuf/tel-aviv | agency | programme neuf tel aviv | ~0 | **JS-only, empty in raw HTML** | - | 0 | none |
| extra in the SERP: israelstart.com (/explorer serves the home) | "300+ programmes" catalogue | programme neuf israël | ~775 | map is JS-only | - | 0 | RealEstateAgent, Service, Offer |

Headline: **no French page combines a real multi-developer catalogue with numbers that explain the purchase.** The catalogues (Barnes, immobilier.co.il, Comacom, Evenis) have almost no text; the text pages (acheter-appartement-israel, Shoshia) have no projects and no figures. Only immobilier.co.il has a price-per-m² band, a cost simulator and a visible FAQ with schema. **Nobody gives purchase-tax rates, nobody has an oleh track, nobody explains Israeli room counting or how Israeli m² are measured, and nobody mentions the France–Israel tax treaty on a catalogue page.** No page has ItemList markup.

Google's own French SERP extras (read in the owner's Chrome, tab already open from the SERP session, 25.10.2026):
- "programme neuf israël", People also ask ("Autres questions"): "Où puis-je acheter un appartement en Israël ?", "Où acheter pas cher en Israël ?", "Quelles sont les tendances actuelles dans le secteur immobilier en Israël ?", "Quel est l'avenir d'Israël ?" (the last one is off topic).
- Related searches: Programme neuf Tel Aviv · Projet immobilier neuf jerusalem · Immobilier neuf Bat Yam, Israël · Projet immobilier israel · Promoteur immobilier Israël · Immobilier Israël location · Immobilier Israël pas cher · Projet immobilier Ramat Aviv.
- AI overview (serp-lang.md): Tel Aviv and suburbs (Ramat Gan, Holon, Bat Yam), Jerusalem, Netanya, Herzliya, Ashdod; prices "en shekels ₪ et euros"; Tel Aviv 3-4 pièces often 4.5M to 7M ₪.

---

## 1. Per page

### 1.1 BARNES Israel, /fr/acheter/programmes-neufs.html
- **Title:** "Immobilier Neuf Israël - Programmes et Constructions de nouveaux projets". **Meta:** "Découvrez nos programmes neufs et projets de construction dans les plus belles villes d'Israel".
- **H1:** "Immobilier Neuf Israel".
- **Outline:** H2 "BARNES vous présente une sélection de programmes neufs et Projets de construction en vente en Israël" → 25 card H3s, names cut off in the HTML ("Complexe Eve Nord Tel Aviv -...", "RAV KOOK RESIDENCES, LA...", "DUO® Tel Aviv – Le Nouveau...", "THE WEIZMANN PROJECT | TEL...", "Projet Nordau 65, Tel Aviv") → H3 "Découvrez l'Excellence des Programmes Neufs en Israël" (the editorial block) → H3 "BARNES Israel" → H3 "Recevoir une alerte personnalisée".
- **Words:** about 314 editorial plus about 775 in the grid. The raw count of 1,766 includes a 700-word country-code list inside the form.
- **Sections:** grid; a "why invest" block with four bullets (growing market, prestigious locations, build quality, "avantages fiscaux attractifs" for foreign investors, with no source); contact form; newsletter.
- **Data:** 25 cards. 22 show a from-price in ₪, from 2,197,987 ₪ to 20,980,784 ₪; 3 say "Prix sur demande". Each card has an m² range (36 to 424 m²), a pièces range ("du Studio au 2 Pièces", "du 4 Pièces au 9 Pièces"), the delivery month on most cards (Octobre 2026 to Octobre 2029; one card still says "Livraison Avril 2025", already past) and a named agent. Neighbourhoods: HaTzafon HaYashan, Neveh Tzedek, HaKfar HaYarok. Cities: Tel Aviv-Yafo (about 21 cards), Bat Yam, Ra'anana, Ramat Hasharon.
- **Euro:** only through a currency switcher (€, CHF, $, £, ₿ and more) and an m²/sqft switch. The server HTML prints ₪.
- **Tools:** currency and unit switcher, personalised alert (needs at least 3 criteria), contact form, newsletter, WhatsApp link. No filters, no sort, no map on this page.
- **Schema:** none. **hreflang:** fr, en, he, with x-default = en. Canonical to itself.
- **FAQ:** none. The only question is the heading "Pourquoi investir dans un programme neuf en Israël ?".

### 1.2 BARNES International, /fr/programme-neuf/israel/tel-aviv-yafo.html (also /tel-aviv.html and /israel.html)
- **Title:** "17 programmes neufs en vente à Tel Aviv-Yafo" (the city page). The sibling /tel-aviv.html is titled "1 programmes neufs en vente à Tel-Aviv"; it is a duplicate city bucket with 1 listing plus nearby properties. /israel.html: "Programme neuf de luxe Israël : 21 biens immobiliers neufs de prestige en Israël".
- **H1:** "Immobilier Neuf Tel Aviv-Yafo - projets de constructions haut de gamme" (Israel page: "Programmes neufs de luxe Israël"). **H2:** "17 programmes neufs en vente à Tel Aviv-Yafo". The cards have no headings.
- **Words:** no editorial text at all; about 456 words of card and filter labels.
- **Data:** 17 cards, each with **price in € and ₪ side by side** ("1 291 137 € | 4 500 000 ₪"), from 3,000,000 ₪ (860,758 €) to 27,600,000 ₪ (7,918,974 €), 2 "Prix sur demande", m², neighbourhood (HaTzafon HaYashan, Lev Hair, Neveh Tzedek, Tel Aviv Center) and an "Exclusivité" badge. The implied rate is 3.4853 ₪ per €; the BOI rate published 23.10.2026 is 3.4844. Nearby: Ra'anana 2,200,000 ₪ (631,223 €), Ramat Hasharon. The Israel page adds Bat Yam. No rooms and no delivery date on these cards.
- **Tools:** sort (price up/down, newest, exclusive, random), list/map toggle, favourites, "élargir aux villes voisines", personalised alert, currency and unit switcher.
- **Schema:** BreadcrumbList only. **hreflang:** fr, en, es, it, de, with x-default = fr.
- **FAQ:** none.

### 1.3 E-Projects, /nos-projets/ and /projets-immobiliers-a-tel-aviv/
- **Titles:** "Nos projets immobiliers neufs en Israël — E-Projects - Projets neufs en Israel" and "Appartements neufs à Tel Aviv — Programmes immobiliers 2026 - Projets neufs en Israel". The accessibility-toolbar text leaks into both titles.
- **Meta:** "…appartements sur plan à Jérusalem, Tel Aviv, Bat Yam, Netanya. Prix, livraison, plans." and "Programmes immobiliers neufs à Tel Aviv en 2026 : appartements standing, immeubles de prestige, prix et livraison."
- **H1:** "Nos projets immobiliers neufs en Israël — E-Projects". **The Tel Aviv page has no H1**; its headings start at H2.
- **Outline:** one H2 per project ("PROJET IMMOBILIER A NETIVOT", "APPARTEMENTS NEUFS ARNONA", "APPARTEMENTS NEUFS NATANYA SUD", "PROJET IMMOBILIER NEVE HEN TEL AVIV", "PROJET IMMOBILIER A REHAVIA JERUSALEM"…), then H3 "Villes".
- **Words:** about 12 words of copy on each page ("E-Projects vous permet d'investir dans les meilleurs projets immobiliers neufs en Israël").
- **Data:** national page, 9 cards on page 1 of 5. From-prices in ₪: Netivot 1,470,000; Jerusalem Mekor Haim 1,690,000, Rasco 4,100,000, Arnona 7,800,000, Rehavia 14,700,000; Netanya Sud 2,800,000; Bat Yam 2,000,000 and 2,320,000; Tel Aviv Neve Hen 5,900,000. m² ranges appear on some cards. Tel Aviv page: 6 cards, 2,700,000 to 6,500,000 ₪. Cities in the menu: Bat Yam, Beer Sheva, Ben Shemen, Eilat, Hadera, Jérusalem, Modi'in, Naharya, Natanya, Netivot, Or Akiva, Raanana, Sderot, Tel Aviv. Phones "Depuis Israel" and "Depuis la France".
- **Tools:** filters for ville, **disponibilité** (1 an / Entre 1 et 2 ans / Plus de 2 ans / Déjà disponible), **idéal pour** (Alya / Investissement / Achat plaisir / Luxe / Résidence principale / Airbnb) and prix bands written in "sh" (500.000-1000.000sh …); compare; WhatsApp. A separate page "FAQ — Achat immobilier en Israël" sits in the menu.
- **Schema:** WebPage, BreadcrumbList, WebSite + SearchAction (Yoast). dateModified 11.7.2026. No hreflang.
- **FAQ:** none on these pages.

### 1.4 Immoneuf (home), immoneuf.co.il
- **Title:** "Immoneuf — Portail immobilier neuf en Israël pour francophones". **Meta:** "…Projets à Jérusalem, Tel Aviv, Netanya, Ashdod, Bat Yam. Accompagnement A à Z…".
- **H1: none.** H2s: "Trouvez votre bien neuf, sur plan ou d'occasion en Israël" · "Nos coups de coeurs projets neufs en Israel" · "Zoom sur Jérusalem" · "Zoom sur Netanya" · "Les derniers biens ajoutés dans tout Israel" · "Découvrez les villes d'Israël préférées des francophones" · "Conseils et actualités sur l'immobilier en Israel" · "Explorez nos projets neufs par ville en Israël".
- **Words:** about 96 words in the about block, plus blog teasers and city labels. The raw count is 2,103.
- **Data:** about 31 cards, with duplicates across rails, from 1,850,000 ₪ (Netivot, Ashkelon) to 15,000,000 ₪ (a resale villa in Netanya). Named projects: Carasso, Mekor Chaim, LEGACY (Dimri), AMIM TOWERS (Talpiot), Armon HaNatziv, Halperin Tower, Marine Reserve (Dimri), Venezia Eilat. **City list with listing counts "préférées des francophones":** Netanya 51, Jérusalem 40, Tel Aviv 26, Bat Yam 26, Ashdod 18, Ashkelon 16, Netivot 8, Eilat 8, Holon 8, Petah Tikva 5, Kiryat Gat 5, Givat Shmuel 5, Hadera 4, Herzliya 4, Beer Sheva 4, Ra'anana 4, Ramat Gan 3, Tibériade 3, Rishon 2, Kfar Saba 1. Blog posts dated 15.10.2026 and 6.10.2026 ("ventes de neuf, luxe et taux de crédit", "nouveaux quartiers, tram et taux de crédit").
- **Defects seen (finding only):** a "Properties from leading developers in UAE" block is leftover theme demo text (a "zero-gravity penthouses" resort); the counters print "0"; "Welcome to San Jose Real Estate" leaks in the login modal.
- **Tools:** "guide personnalisé gratuit en 2 minutes" quiz (budget réel, villes idéales, prix par quartier), WhatsApp, services directory (avocat, crédit, déménagement, expertise avant achat).
- **Schema:** FAQPage with 4 questions **that are not visible on the page**, RealEstateAgent, Organization, WebSite. No hreflang. dateModified 21.7.2026.
- **FAQ (schema only):** "Peut-on acheter un appartement neuf en Israel en tant que francophone ?" · "Quelles villes proposent les meilleurs projets immobiliers neufs en Israel ?" · "Qu'est-ce qu'une dira hadasha en Israel ?" · "Comment financer un achat immobilier neuf en Israel ?". Blog questions: "Ashdod ou Ashkelon, quelle ville choisir pour votre projet immobilier ?" · "Netanya ou Hadera, quelle ville choisir pour votre projet immobilier ?" · "Tel Aviv reste-t-elle le meilleur choix face à Bat Yam ?" · "Acheter un bien immobilier au nom de ses enfants…".

### 1.5 Immoneuf, /ville/tel-aviv/
- **Title:** "Archives des Tel Aviv - Immoneuf Israel", the WordPress default. **The meta description is a whole multi-paragraph block.**
- **H1:** "Properties listed in Tel Aviv", in English (a template leftover). H2 "Derniers articles", then **H2 "Acheter un appartement neuf à Tel Aviv"** › H3 "Pourquoi investir à Tel Aviv" · "Les quartiers de Tel Aviv où acheter" · "Questions fréquentes — Immobilier neuf à Tel Aviv".
- **Words:** about 224 editorial. The raw count is 1,187.
- **Data:** 24 cards mixing new ("Projets neufs") and resale ("2e main"), from 1,900,000 ₪ (Yafo) to 10,850,000 ₪. Named: YAMA TLV (Dimri), Vieux Nord Yarkon / Kikar HaMedina / Dizengoff, Est Bitzaron, Boulevard Rothschild, Nahalat Binyamin. Neighbourhood blurbs for Neve Tzedek, Vieux Nord ("apprécié des familles francophones"), Florentin, Rothschild, Kikar HaMedina/Park Tzameret, Sarona/Yaffo. The claims "valeur refuge" and "les prix résistent et progressent" have no source.
- **Tools:** filters for types (2e Main / A Louer / Exclusivité / Projets Neufs / **Tama 38**), catégories, régions, villes, zones; sort by price, date, chambres, salles de bain; lead form.
- **Schema:** CollectionPage, BreadcrumbList, Organization. No hreflang.
- **FAQ (visible):** "Pourquoi acheter du neuf à Tel Aviv ?".

### 1.6 Alloj, /fr/immobilier-israel.html and /fr/projet-immobilier-neuf-israel.html
- **Title:** "Immobilier en Israël – Achat, vente & projets neufs | Alloj Immo". **The projet-immobilier-neuf page has an empty `<title>` and an empty meta description.** Neither page has a canonical or a robots meta.
- **H1:** "Immobilier en Israël : Achetez, vendez et investissez en toute confiance" and "16 Projet Immobilier Neuf Israel".
- **Outline (immobilier page):** H2 "Pourquoi choisir Israël pour investir ?" · "Les villes les plus dynamiques" · "L'achat immobilier en Israël : ce qu'il faut savoir" · business-card H3s · "Immobilier Israël : vous cherchez plus d'informations ?" (a 357-word keyword-stuffed boilerplate).
- **Words:** about 234 editorial on the immobilier page; about 0 on the projet page.
- **Data:** cards are businesses, not units: Shahar Levi SEA YOU I (Ir Yamim, "Livraison Juillet 2027"), Yuvalim City Boy (Tel Aviv, from 3,850,000 ₪), Abarbanel (from 3,280,000 ₪), Amim Towers, Briga Glil Yam (Herzliya, "5 immeubles et 180 logements, 31 configurations"), Arthur Tower, Venezia Eilat, plus a lawyer, an accountant and Cyprus projects. Each card shows a **view counter and a "demandes effectuées" count** as social proof. Cities: Tel-Aviv, Netanya ("prisée par les francophones"), Jérusalem, Ashdod, Haïfa.
- **Tools:** service menu (Courtier en Crédit, **Simulateur prêt**, Projet sur plan, Cabinet d'Avocats), WhatsApp group, app download.
- **Schema:** none.
- **FAQ (visible, no schema):** "Puis-je acheter en Israël sans être résident ?" · "Quel budget prévoir ?" · "Comment optimiser un investissement locatif ?" · and the heading "Pourquoi choisir Israël pour investir ?".

### 1.7 BA-HIT, /projets-neufs/
- **Title:** "Projets neufs – BA-HIT – Immobilier en Israel". **Meta:** "Si parmi la liste ci-dessous, aucun projet neuf ne vous convient…".
- **H1:** "Projets neufs"; one H3 per card ("Projet neuf à vendre sur Bat Yam n. 291", "Projet TAMA 38 à vendre sur Bat Yam n. S619", "Projet Neuf sur Tel Aviv (Florentine)", "Projet neuf sur Tel Aviv: Les 4 Florentines"…).
- **Words:** about 28 of intro.
- **Data:** 32 cards, **most stamped "vendu"**; one still says "PRE SALE Garantie Bancaire Fin du projet en 2020". Prices in ₪ from 1,400,000 (an Ashdod TAMA 38 flat, "100 m2 net + balcon 15 m2") to 10,000,000. Land is priced in euros (Tel Aviv land at 650,000 €, Hadera at 165,000 €). Feature icons: Parking, Terrasse, Ascenseur. Cities: Tel Aviv (Neve Tsedek, Florentine, Yad Eliyahu, Bavli, Rothschild, Ben Yehuda), Bat Yam, Yavne, Herzliya Pituah, Ashdod, Rishon.
- **Tools:** filters (type, **Nombre de Pièces 1, 2, 2.5, 3, 3.5, 4, 4.5, 5…**, sale and rent price), "Recherche Ciblée" service, translation service, newsletter, WhatsApp.
- **Schema:** none. **hreflang:** fr, en, he.
- **FAQ:** none.

### 1.8 Evenis Group, /projets-neufs/tel-aviv/
- **Title:** "Projet neuf Tel Aviv - Annonces Immobilières Israel en français" (plus leaked toolbar text). **Meta:** "Voici les projets neufs à Tel Aviv - annonces Immobilières à Tel Aviv en français. Catalogue exclusif d'appartements."
- **H1:** "Projets Neufs à Tel Aviv : Annonces Immobilières"; about 60 listing H3s ("#REF MS 17407 * A VENDRE PROJET NEUF FLORENTINE TEL AVIV *", "#REF DBS 16213 *PRE VENTE PROJET KEREM HATEIMANIM TEL AVIV*", "#REF AAS189. PROJET NEUF TEL AVIV LIVRÉ DANS 8-9 MOIS!!!!").
- **Words:** a 62-word intro; the whole page is about 4,500 words of listing excerpts.
- **Data:** posts dated from 14.9.2026 back to **July 2017** ("Livraison fin 2018", "Prêt en octobre 2018"). Prices in "nis"/"NIS" ("A partir de 1.850.000 nis pour un 4 pièces de 88m2", "à partir de 3 350 000 NIS", "From 1,930,000 Nis"). Terms: **rez de jardin**, duplex, mini-penthouse, **pré-vente**, "livré dans X mois", **mamad**, "Récupérez vos clés et payez seulement en 2028 !" (deferred payment), "30% DE LA TOUR DÉJÀ VENDUE". Areas: Allenby, Neve Tzedek, Levinsky, Florentine, Kerem Hateimanim, Kikar Rabin, Kikar Hamedina, Park Tsameret (Bavli tower), Yad Eliyahu, Ramat Aviv, Vieux Nord.
- **Tools:** **live EUR/ILS and USD/ILS exchange-rate widget** (currencyrate.today iframe), exit-intent phone capture ("Tous nos biens ne sont pas sur le site"), WhatsApp, links to "Lexique Immobilier Traduction Hébreu", "Crédit immobilier en France et en Israël" and a TAMA 38 guide.
- **Schema:** Organization, WebPage, BreadcrumbList, WebSite. **hreflang:** fr-FR, en-US. dateModified 23.12.2021.
- **FAQ:** none. A disclaimer says the prices are indicative and not contractual.

### 1.9 Immobilier.co.il, /ville/telaviv/projets-neufs (the strongest page)
- **Title:** "Immobilier Tel Aviv : 146 Projets neufs | Immobilier.co.il". **Meta:** "Immobilier Tel Aviv : 146 Projets neufs en Israël. Appartements, villas, penthouses. Portail immobilier N°1 depuis 2004."
- **H1:** "Programmes Neufs à Tel Aviv". **H2:** "Les quartiers avec les projets neufs les plus actifs" · "Le marché du neuf à Tel Aviv" · "Questions fréquentes sur Tel Aviv" (5 FAQ H3s).
- **Words:** about 287 of intro and market text, plus about 284 of FAQ.
- **Data:**
  - **₪/m² band per area:** Rothschild/Sarona/Neve Tzedek 80,000 to 150,000; Tel Aviv Nord (Ramat Aviv, Park Tzamaret) 65,000 to 100,000; Yafo 55,000 to 80,000; Florentin and the south 50,000 to 75,000.
  - **Ranges:** 3-4 pièces neuf 3.5M to 7M ₪; premium towers 5M to 15M; penthouses up to 50M ₪.
  - **Developers named:** Azrieli, Aura, Electra, Aldar, Africa Israel, Canada Israel. Tower heights of 30 to 70 floors, deliveries 2024 to 2029.
  - **Cards:** € and $ next to ₪, e.g. "3,550,000 ₪ $1,139,550 | €1,018,850". The implied rate is 3.4843, which is the BOI rate of 23.10.2026. Project cards show a range ("À partir de 3,590,000 ₪ Jusqu'à 7,570,000 ₪") and the units available by pièces and m².
  - **Neighbourhood filter values:** Bavli, Bazel, Ben-Yehuda, Centre Ville, Dizengof, Ezorei Hen, Florentine, Hatsafon hayachan, Kefar Shalem, Kerem Hatemanim, Kikar Hamedina, Lev Tel-Aviv, Neve Tsedek, quart de la mer, Rothshild, Shenkin, Sokolov, Tel Aviv north, Tel Barouch, Yaffo, Yehouda hamakaby.
- **Unsourced or wrong claims (finding only):** "40 % d'acheteurs internationaux… investisseurs du Golfe depuis 2020"; "notaires habitués" (Israeli deeds are not done by a notary); "Financement bancaire possible pour non-résidents (apport 50 % minimum)" (it matches BOI 329 for non-citizens, but no source is given); "Dan Panorama Tower" listed as an emblematic new project.
- **Tools:**
  - **Filters:** quartier, type (Villa, Appartement, Duplex, Penthouse, **Rez de jardin**, Duplex-Penthouse, Mini-Penthouse), price range, **pièces 1+ to 6+**, surface, **livraison year 2024 to 2030**.
  - **Navigation:** sort (most recent, price up/down, surface); list/map; alerts; favourites.
  - **"Combien me coûtera ce bien ?" simulator:** price; **Taxe d'achat (Mas Rechisha) Résident vs Investisseur / Étranger**; Apport (25%); Frais d'avocat (1% + 18% VAT); Frais d'agence (2% + 18% VAT); term 10 to 30 years; rate 2.5 / 4.2 / 7%. **There is no oleh track.**
  - **Lead routing:** form check boxes for "capacité d'emprunt" and "conseil d'un avocat immobilier"; partner-lawyer card (Me Eden Allouche); dial codes for France, Belgium, Switzerland, Luxembourg and Monaco first.
- **Schema:** CollectionPage with mainEntity **Product + AggregateOffer** (lowPrice 2,490,000, highPrice 26,000,000 ILS, offerCount 145), which is a Product snippet on a list page and a policy risk. Also FAQPage (5) and BreadcrumbList. **hreflang:** fr, en, he, ru, pt, es, it, de, with x-default = fr.
- **FAQ (visible + schema):** "Combien coûte un appartement neuf à Tel Aviv ?" · "Qui achète du neuf à Tel Aviv ?" · "Quels sont les projets neufs emblématiques à Tel Aviv ?" · "Peut-on acheter à Tel Aviv depuis la France ?" · "Le Pinui-Binui à Tel Aviv est-il une opportunité ?".

### 1.10 Comacom, /projets-neufs-en-israel-immobilier-neuf/
- **Title:** "Projets neufs en Israël – Immobilier Neuf – Agence COMACOM – Immobilier en Israël". **No meta description.**
- **H1:** "Projets neufs en Israël – Immobilier Neuf"; one H2 per card ("Projet neuf à Netivot, Ramot Yoram", "À ne pas manquer! Projet Tama 38, Centre ville, Bat Yam").
- **Words:** 0 editorial.
- **Data:** "110 Propriétés", 9 per page. Page 1 runs from 1,380,000 ₪ (Netivot) to 1,920,000 ₪ (Bat Yam TAMA 38), in Jerusalem-Arnona, Netivot, Eilat, Beer Sheva, Ashkelon and Bat Yam. Cards show pièces, salles de bain, m², étage and agent name, with ages like "il y a 2 ans".
- **Tools:**
  - **Features filter:** Ascenseur, **Ascenseur chabat**, Ascenseur privé, Cave, Climatisation, Jardin, **Mamad**, Meublé, Neuf, Parking, **Parking (au cadastre)**, Piscine, **Proche mer**, **Souccah**, **Tama 38**, Terrasse, **Vue mer**.
  - **Other filters:** separate **Pièces / Chambres / Salles de bain**, and about 230 neighbourhoods in French spelling ("Ashdod - Youd Alef", "Netanya - Ir Yamim", "Tel Aviv - Quart de la mer").
  - **Sort:** price and date.
- **Schema:** none.
- **FAQ:** none.

### 1.11 Acheter-appartement-israel.com, "Immobilier neuf en Israël : Comment bien choisir sur plan"
- **Title:** "Immobilier neuf en Israël | AcheterIsraël". **Meta:** "Découvrez comment bien choisir votre programme neuf en Israël et maîtriser l'achat sur plan…".
- **H1:** "Immobilier neuf en Israël : Comment bien choisir sur plan". **H2:** "Comprendre la dynamique de la vente sur plan en Israël" · "Définir votre profil d'acheteur et vos objectifs de vie" · "Évaluer la solidité du promoteur et la fiabilité du projet" · "Maîtriser l'emplacement et les plans d'urbanisme de la mairie" · "Sécuriser l'aspect juridique et contractuel de l'achat" · "Anticiper les coûts annexes et la fiscalité immobilière" · "Gérer les délais de construction et les garanties" · "Personnalisation et choix des finitions : Maximiser la valeur" · "Préparer l'après-achat : De la remise des clés à l'intégration" · "Checklist finale pour sécuriser votre acquisition" · "Questions fréquentes".
- **Words:** about 2,600. It has a "Réponse rapide" answer box and a table of contents.
- **Data:** **no numbers at all**: no rates, no prices, no law names.
- **Terms used:** Mas Rekhisha, Arnona, Mas Shevah, Tabou, Mashkanta, oulpan, Alyah, "Zikaron Dvarim".
- **Errors (finding only):** "Zikaron Dvarim" is glossed as "souvenirs des échanges" (it is a memorandum of understanding). Purchase tax is said to vary with "la localisation du bien" (it does not). The Sale Law guarantee is never named.
- **Tools:** lead popup "Recevez les nouveaux biens… en avant-première".
- **Schema:** Article, FAQPage, BreadcrumbList, Organization.
- **FAQ:** "Quels sont les principaux risques de l'achat sur plan en Israël ?". On its home: "Peut-on vraiment acheter sans résider en Israël ?" · "Quel apport prévoir ?".

### 1.12 Shoshi Arbib law firm, /fr/blog/buying-from-developer-12-risks/
- **Title:** "Acheter un appartement neuf en Israë… | Cabinet d'avocats Shoshi Arbib" (truncated in the HTML).
- **H1:** "Acheter un appartement neuf en Israël : 12 risques à vérifier". **H2:** "Les risques spécifiques aux achats sur plan" · "Risques principaux" · "Étapes d'un achat immobilier en Israël" · "Notre expertise".
- **Words:** about 520. Dated 29 mars 2026; modified 20.6.2026.
- **Data:** the title promises **12 risks but the page lists 6** (stabilité financière du promoteur, garantie bancaire, permis de construire, délai de livraison et pénalités, modifications de spécifications, délai d'inscription). It names "Chok Mechira", the developer as "**Katchlan**" (sic; it is kablan), "VEFA", "Tabu" and the "district de Sharon". There are no numbers.
- **Schema:** heavy (LegalService/LocalBusiness, Person, HowTo, FAQPage, **AggregateRating**, Speakable, DefinedTermSet). The FAQPage holds a broken auto-generated question "What is risques principaux?" and "Qu'est-ce que Acheter un appartement neuf en Israël : 12 risques à vérifier?". **hreflang:** he, en, ru, fr.
- **FAQ (visible):** "La garantie bancaire est-elle obligatoire lors d'un achat sur plan en Israël ?". The checklist questions: "Un permis valide est-il délivré ou le projet est-il encore en phase de planification ?" · "Quelle est la date contractuelle ?" · "Quelle indemnisation est prévue en cas de retard ?" · "Le promoteur peut-il substituer matériaux et finitions ?" · "Quand l'appartement sera-t-il inscrit à votre nom au registre foncier ?".

### 1.13 Extras in the same SERPs (not in the brief list)
- **yafoinvest.com/fr/neuf/tel-aviv:** "Programmes immobiliers exclusifs en vente à Tel-Aviv | YafoInvest", H1 "Programmes immobiliers à Tel-Aviv". **The grid is JS-only** (a React root, no listing in the raw HTML), with filters for budget max (₪) and surface min and an alert form. It is a live example of a client-only catalogue that still ranks on brand and URL.
- **israelstart.com** (/explorer redirects to the home in raw HTML; the "carte interactive" is JS-only): "Parcourez 300+ programmes neufs dans tout Israël", "catalogue par ville, budget et nombre de pièces", a neuf vs ancien comparison table, 7 languages. **Best French vocabulary in the set:** "taxe d'acquisition (mas rechisha)", "les prix incluent une TVA de 18 %", "partiellement indexés pendant la construction", "pièce sécurisée (mamad)", "registre foncier (Tabo)", "date de livraison prévisionnelle", "échéancier de paiement", "appartement témoin".

---

## 2. The French searcher's vocabulary

### 2.1 Demand: what French speakers actually type

GSC, all French queries for nad-lan.co.il, 25.7 to 23.10.2026 (impressions, 0 clicks on all of them):

| Query | Impr. | Lands on |
|---|---|---|
| projet immobilier israël | 184 | `/projects/` 127 @75.6, `/fr/` 29 |
| appartement neuf israël | 89 | `/fr/` 89 @37 |
| financement immobilier israël | 35 | `/investment/` |
| programme neuf israël | 21 | `/fr/` |
| agence immobilière israël francophone | 7 | `/fr/` |
| programme neuf tel aviv | 4 | `/projects/` |
| investir en israël immobilier / investissement immobilier israël / credit immobilier en israel | 2-3 each | `/investment/` |
| acheter sur plan en israël / achat sur plan israël | 2 / 1 | `/fr/` |
| projet immobilier tel aviv / projet immobilier en cours israël | 2 / 1 | `/`, `/projects/` |
| prêt immobilier israël étranger | 1 | `/israel-mortgage-non-residents/` |
| "pouvez-vous me recommander des plateformes pour comparer les prix des propriétés à vendre en israël ?" | 1 | `/fr/` (an assistant-style long query: the catalogue should answer "comparer les prix") |

DataForSEO Google Ads monthly volume in French (FR = France, BE = Belgium, CH = Switzerland, IL = Israel; 10 is the floor bucket):

| Keyword | FR | BE | CH | IL | CPC FR (€) |
|---|---|---|---|---|---|
| immobilier israel | 320 | 10 | 10 | 90 | 2.61 |
| immobilier tel aviv | 140 | 10 | 10 | 40 | 2.87 |
| appartement tel aviv | 140 | 10 | 10 | 30 | 2.86 |
| convention fiscale france israel | **110** | 10 | 10 | 20 | - |
| immobilier netanya | 90 | 10 | 10 | 50 | 0.77 |
| immobilier bat yam | 90 | 10 | 10 | 10 | 1.22 |
| acheter (un) appartement (en) israel / achat appartement israel | 70 | 10 | 10 | 10 | 1.30 |
| appartement netanya | 50 | 10 | 10 | 30 | 0.82 |
| prix immobilier tel aviv / prix m2 tel aviv | 50 / 50 | 10 | 10 | 10 | 5.68 / **6.65** |
| immobilier jerusalem / immobilier ashdod | 40 / 40 | 10 | 10 | 40 / 30 | 1.22 / 0.35 |
| penthouse tel aviv | 30 | 10 | 10 | 50 | 3.45 |
| immobilier raanana | 30 | 10 | 10 | 20 | 0.11 |
| tama 38 / pinui binui | 10 / 10 | 10 | 10 | **140 / 30** | - |
| credit immobilier israel | 10 | 10 | 10 | 40 | - |
| programme neuf tel aviv / programme neuf netanya | 10 / 10 | - | - | 10 | **5.26 / 3.37** |
| projet immobilier israel, projet neuf israel, immobilier neuf israel, promoteur immobilier israel, taxe d'acquisition israel, mas rechisha, avocat immobilier israel, pret immobilier israel, immobilier israel pas cher | 10 each | | | | |
| mamad | 720 | 40 | 40 | 260 | - (war-shelter interest, not real estate) |
| programme(s) neuf(s) israel, appartement neuf israel, acheter sur plan israel, vefa israel, frais de notaire israel, garantie bancaire israel, alyah immobilier | no data (below threshold) | | | | |

Reading: the **broad heads are "immobilier israël / immobilier [ville]" and "appartement [ville]"**; "programme neuf" is a small but expensive commercial phrase (CPC above 5 €). Google already ties "projet immobilier israël" to new-build catalogues (serp-lang.md). Searchers in Israel (French-speaking residents) type Israeli loanwords: TAMA 38 (140), pinui binui (30), credit immobilier (40). From France the money and tax angle stands out: "convention fiscale france israel" (110) and "prix m2 tel aviv" (6.65 € CPC).

### 2.2 Exact phrases and who uses them (counts in the raw text)

Page keys: BI = barnes-israel, BX = barnes-international (TLV-Yafo + Israel), EP = e-projects (2 pages), IN = immoneuf (home + TLV), AL = alloj (2), BH = ba-hit, EV = evenis, IC = immobilier.co.il, CO = comacom, AA = acheter-appartement-israel, SH = shoshia, IS = israelstart.

| Phrase | Used by (count) | Note |
|---|---|---|
| programme(s) neuf(s) | BX 89, BI 10, IN 1, IC 1, AA 1 | luxury and network brokers' word; it is Google's AI-overview word |
| projet(s) neuf(s) | EV 172, IN 65, CO 29, BH 28, IC 9, AL 4, EP 2 | **the dominant word of the Franco-Israeli market** (calque of פרויקט חדש) |
| projet(s) immobilier(s) | AL 28, EP 20, IN 9, BI 2 | matches the GSC head "projet immobilier israël" |
| immobilier neuf | AL 19, CO 5, AA 3, IN 3, BI 2, BX 1 | a title word, rarely in body text |
| appartement(s) neuf(s) | IN 27, SH 8, EP 6, YafoInvest 6 | matches "appartement neuf israël" |
| nouveau projet | BH 48, EV 19, CO 4, BI 3 | card label |
| sur plan / achat sur plan / vente sur plan | AA 14, AL 7, SH 2, IN 1, IC 1 | the right French term for buying off-plan |
| VEFA | SH 3 | lawyers only, and the Israeli regime is **not** the French VEFA (see 2.3) |
| promoteur | AA 17, SH 13, IC 3, AL 1 | the natural word for קבלן/יזם; "constructeur" is rare |
| pré-vente / prévente / presale | EV 8, BH 1 | = פריסייל (Google's Hebrew PAA "האם יש פריסייל בתל אביב?") |
| livraison / livré | BI 20, EV 14, AA 9, IC 7, BX 6, AL 6 | delivery = מסירה; Barnes prints "Livraison Octobre 2027" |
| garantie bancaire | SH 8, BH 1, AA 1 | nobody names the law or the 7% rule |
| loi Mekher / Chok Mechira / loi sur la vente | SH 5 only | |
| avocat (immobilier) | SH 16, IC 14, AL 11, AA 4, IN 3 | the French buyer expects a "notaire"; in Israel it is the avocat |
| notaire | IC 1 ("notaires habitués", wrong for Israel) | French searchers think "frais de notaire" (no volume measured) |
| taxe d'acquisition / taxe d'achat | SH 3, AA 2, IC 1, IS 1 | |
| Mas Rechisha / Mas Rekhisha | AA 3, IC 1, IS 1 | both spellings are live; keep "mas rechisha" with "taxe d'acquisition" |
| TVA / VAT | IC 2 ("1% + 18% VAT"), IS ("TVA de 18 %") | "TVA incluse" appears nowhere |
| prix au m² / ₪/m² | IC 6, BI 1 | only immobilier.co.il gives figures |
| pièces | EV 45, BI 44, IC 22, IN 26, CO 13, BH 4 | listings count in pièces (2 pièces … 6 pièces; BA-HIT also 2.5, 3.5, 4.5) |
| chambres | CO 2, IN 2, EV 1 | used as a separate filter (Comacom: Pièces and Chambres) |
| mamad | CO 4, EV 2, IS ("pièce sécurisée (mamad)") | |
| alyah / alya | AA 5, EP 2, IN 2 | e-projects filter "Alya" |
| olim / olé | **0** | **no page addresses olim as such** |
| crédit immobilier / prêt / mashkanta | IN 6, AA 2, SH 2, IC 2 ("MASHKENTA"), AL 2, EV 1 | |
| arnona | IN 7, AA 4, CO 3, EP 1 | |
| Tabou / Tabu / Tabo / registre foncier | SH 8, AA 4, IS | three spellings in use |
| Pinui-Binui / TAMA 38 | IC 6 / CO 5, BH 3, EV 3, IN 1 | |
| penthouse, mini-penthouse, rez-de-jardin, duplex | EV, BH, IC, IN, CO | Israeli product types, French words |
| investissement / investir; rendement / rentabilité | AA, EV, AL, BI | promises are mostly unsourced |
| résidence secondaire / pied-à-terre | AA 2, BI 1, IC 1, IS | a real French buyer profile |
| € / euros | BX 52, BI 4, IC 3, BH 2 | only Barnes Intl and immobilier.co.il print euros on cards |
| shekel / nis / sh | EV 10 ("nis"), EP ("sh"), BX 8 | |
| Souccah / Ascenseur chabat | CO 4 | **community features** |
| francophone(s) | IN 10, AL 4, IC 2 | |
| depuis la France / étranger / non-résident | AL 5, IC 3, SH 2, EP 2 | |

### 2.3 Natural French forms of the Israeli terms (recommended usage)

| Israeli term | Natural French | Notes for our page |
|---|---|---|
| פרויקט חדש / פרויקטים בשיווק | **projet immobilier neuf**, programme neuf, projets neufs en commercialisation | use all three: "projet immobilier" (GSC head), "programme neuf" (Google AI, CPC) and "projets neufs" (the market's word) |
| קבלן / יזם | **promoteur (immobilier)** | "kablan" in brackets once; Shoshia's "Katchlan" is wrong |
| רכישה על הנייר | **achat sur plan** | say once "l'équivalent israélien de la VEFA" while stating the differences (no notary, a bank guarantee per payment instead of a GFA, payment schedule set by contract) |
| פריסייל / מחיר השקה | **prévente**, prix de lancement | |
| מפרט טכני (המכר) | **descriptif technique** (the French VEFA term is "notice descriptive") | the official form is in facts.md 1a |
| ערבות חוק המכר / ערבות בנקאית | **garantie bancaire de la loi Mekher** (loi sur la vente d'appartements) | the 7% rule is in 3.3 |
| פנקס שוברים | **carnet de bordereaux de paiement** (pinkas shovarim) | in an accompanied project every payment goes through it (verified, facts.md 1c) |
| ליווי בנקאי | **accompagnement bancaire** (financement du projet) | |
| מס רכישה | **taxe d'acquisition (mas rechisha)** | it plays the role of the French "droits de mutation" inside the "frais de notaire" |
| מע"מ | **TVA (18 %), incluse dans le prix promoteur** | |
| עורך דין | **avocat** (pas de notaire dans l'achat) | |
| טאבו / הערת אזהרה | **registre foncier (Tabou)** / **note d'avertissement (heara azhara)** | |
| חדרים | **pièces** (4 pièces = salon + 3 chambres) | see 3.6 |
| חדרי שינה | chambres | |
| ממ"ד | **mamad (pièce sécurisée)** | "abri" is ambiguous (it also means a building shelter) |
| מרפסת שמש | balcon / terrasse | |
| דירת גן / פנטהאוז / מיני פנטהאוז / דופלקס | rez-de-jardin / penthouse / mini-penthouse / duplex | |
| מחסן / חניה | cave (débarras) / parking (place de parking au cadastre) | |
| שטח (לפי מפרט) | **surface (mesure israélienne, murs extérieurs inclus)** | see 3.6 |
| מדד תשומות הבנייה | **indice des coûts de la construction (madad tsoumot)** | at most 40% of the price can be indexed (facts.md 2a) |
| 20/80 | paiement 20/80 (20 % à la signature, 80 % à la remise des clés) | |
| מסירה / תקופת בדק / אחריות | livraison (remise des clés) / période de garantie (bedek) / garantie | |
| משכנתא | **prêt immobilier (mashkanta)** | |
| ארנונה | arnona (taxe municipale) | |
| ועד בית / חברת ניהול | frais de copropriété / syndic | |
| תמ"א 38 / פינוי בינוי | TAMA 38 / pinoui-binoui (renouvellement urbain) | the market writes "Pinui-Binui" and "Tama 38" |
| עולה חדש / עלייה | **olé hadach (nouvel immigrant)** / alyah | use "olim" in the FAQ (zero competitors do) |
| תושב חוץ / תושב חוזר | non-résident (résident étranger) / résident de retour | |
| ייפוי כוח | procuration | |

---

## 3. What French-speaking buyers need that Hebrew buyers do not

### 3.1 Purchase tax (taxe d'acquisition) 2026 by status (**verified 25.10.2026**)
Source: Tax Authority instruction 1/2026 (18.1.2026), opened today: https://www.gov.il/BlobFolder/policy/inst-01-2026/he/realestate_inst-01-2026.pdf

| Buyer | Brackets (₪) | Valid |
|---|---|---|
| Israeli resident individual, single home (דירה יחידה) | 0% to 1,978,745 · 3.5% to 2,347,040 · 5% to 6,055,070 · 8% to 20,183,565 · 10% above | 16.1.2025 to 15.1.2028 |
| **Non-resident (foreign resident), company, or additional home** | **8% to 6,055,070 · 10% above, from the first shekel** | temporary order to **31.12.2026**; the 2027 rate is **unverified** |
| **Olé (regulation 12A), single home, bought from 1 year before aliyah to 7 years after** | 0% to 1,978,745 · **0.5%** to 6,055,070 · 8% to 20,183,565; the relief does not apply above 20,183,565 | 16.1.2025 to 15.1.2028 |
| Olé, regulation 12 (business; an olé who arrived before 15.8.2024 may choose it, per Kol Zchut) | 0.5% to 1,988,090 · 5% above | same |

Worked examples (our calculation from the brackets; € at the BOI rate of 23.10.2026, 3.4844):

| Price | Price in € | Resident (single) | Non-resident | Olé 12A |
|---|---|---|---|---|
| 3,000,000 ₪ | 860,980 € | 45,538 ₪ (13,069 €) | **240,000 ₪ (68,878 €)** | 5,106 ₪ (1,465 €) |
| 5,229,800 ₪ (official TLV 4-room median, Q1 2026) | 1,500,918 € | 157,028 ₪ (45,066 €) | **418,384 ₪ (120,073 €)** | 16,255 ₪ (4,665 €) |

- "A buyer who becomes a resident or returning resident within 2 years counts as a resident" (Tax Authority 2026 buyer guide p.50, verified 22.10.2026 in `docs/research/2026-10-22-purchase-tax/brief.md` F6). With the 12A window this is the key planning fact for French buyers who are preparing aliyah. **How the refund works in practice is unverified; confirm with a lawyer.**
- Declare within 30 days; pay no earlier than 60 days from the deal (facts.md 3). The tax on a new apartment is computed on the price **including VAT** (Kol Zchut, secondary).
- Competitor gap: immobilier.co.il's simulator has Resident vs "Investisseur / Étranger" only, with no olé track and no dates; nobody else has rates.

### 3.2 Mortgage for non-residents and olim
- **BOI Directive 329, version (13) 06/26, opened today** (https://www.boi.org.il/media/ez4npagt/329.pdf):
  - LTV caps: 75% for a single home, 70% for a replacement home, **50% for an "investment home"**.
  - The directive defines a "single home" and a "replacement home" as bought by an "**individual Israeli citizen**" as defined in s.16A(a) of the Land Taxation Law, and a "foreign resident" (תושב חוץ) as "one who is not an Israeli citizen".
  - Housing loans in foreign currency or FX-linked given to a foreign resident are exempt from the repayment-to-income limits (s.12.3).
- **s.16A(a) of the Land Taxation Law** (Wikisource consolidated text, opened today) defines an "Israeli citizen" as anyone **registered (or obliged to register) in the Population Registry**, an individual Israeli resident, or someone entitled under the Law of Return who lives in the Area.
- **Our reading (to confirm with a bank):** a French buyer who is not registered in Israel is treated as an investment buyer, so **50% LTV at most, apport 50%**; a French buyer who already holds Israeli citizenship (registered), and any olé, can reach 75% on a single home. Immobilier.co.il's "apport 50 % minimum" for non-residents is consistent with this, but no competitor explains the citizenship nuance.
- **Olim state-assisted mortgage (secondary: Kol Zchut, updated 2.3.2025, read in Chrome today):**
  - **Who:** holders of a valid oleh certificate who are "homeless" (חסרי דירה), **for 15 years from aliyah**.
  - **How:** an eligibility certificate from the Ministry of Construction and Housing and the Ministry of Aliyah, issued through the mortgage banks.
  - **How much:** the amount follows points (families 1,700 points in year one and 1,800 after; singles 600, plus 400 at 45 and over); equity of at least 25%.
  - Official pages (gov.il) were not opened; **verify before quoting amounts**.
- Rates: BOI rate 3.25% (held 21.10.2026; next decision 23.11.2026); prime 4.75% (derived) (facts.md 4c).

### 3.3 Buying from France: what changes
- **No notary.** In Israel the deed is handled by lawyers. The developer may charge the buyer for **the developer's lawyer** at most the lower of **5,915 ₪ or 0.5% before VAT**, and this cap **does not apply above 4,642,750 ₪** (facts.md 1a, verified). The buyer's own lawyer fee is a market practice (immobilier.co.il assumes 1% + 18% VAT): **unverified**.
- **The contrast French buyers expect (service-public.gouv.fr F2961, "Vérifié le 18 septembre 2026", opened today):**
  - A French VEFA is signed **before a notary**, with proof of a **GFA or GFR** (completion or refund guarantee) and a 10-day withdrawal period.
  - Staged payments are capped at 35% / 70% / 95% at foundations / weathertight / completion (from the official page F39743 as shown in search, not opened).
  - In Israel the protection is a **bank guarantee (or insurance policy, or a warning note) for anything paid above 7% of the price**, VAT excluded (Sale Law (Assurance of Investments) 1974, s.2, facts.md 1c, verified). Payments go through the project's voucher booklet, and the guarantee is due within 14 business days. The payment schedule is contractual, the 20/80 deals are capped by the BOI (facts.md 4b), and at most 40% of the price can be indexed to the construction-inputs index (facts.md 2a).
- **Late delivery:** under Israeli law the indemnity is automatic: 1× the comparable rent for months 2 to 4, 1.25× for months 5 to 10, 1.5× from month 11 (contracts from 7.7.2022; facts.md 1b, verified). In a French VEFA there are penalties only if the contract provides them (**unverified**, general knowledge).
- **After delivery:** Israeli inspection periods run 1 to 7 years by item, followed by a 3-year warranty and 20 years for structural defects (facts.md 1a). The French reference points are garantie de parfait achèvement 1 an / biennale 2 ans / décennale 10 ans (the search snippet confirms biennale and décennale). A comparison table would be unique in the SERP.
- **Registration (Tabou):** the condominium is registered within 1 year, and the buyer's rights within 6 months of that (facts.md 1a).
- **Procuration (power of attorney):** a POA signed in France for an Israeli deal usually needs an Israeli-consulate certification or an apostille. **Unverified**: no official page was opened.
- **Compte bancaire / transfert:** payments in accompanied projects go to the voucher account (law text). Whether an Israeli account is required, and which source-of-funds documents Israeli banks ask for: **unverified**.
- **French tax side:**
  - **The France–Israel tax treaty was signed in Jerusalem on 31.7.1995**, came into force on 18.7.1996, applies from 1.1.1997 and has been modified by the MLI (BOFiP BOI-INT-CVB-ISR-20120912, PDF exported today: https://bofip.impots.gouv.fr/bofip/1113-PGP.html/identifiant=BOI-INT-CVB-ISR-20120912). **Verified.**
  - Article 6 gives the State where the property sits the right to tax rental income. **Unverified wording**: practitioner sources only; the impots.gouv.fr consolidated PDF was in maintenance and Legifrance (https://www.legifrance.gouv.fr/jorf/id/JORFTEXT000000379336) was behind a bot check, which was not bypassed. How France then eliminates double taxation (a tax credit?) is **unverified**.
  - French residents must declare accounts opened abroad every year (box 8UU, form 3916-3916 bis); the fine is **1,500 € per undeclared account** (service-public.gouv.fr A18891, published 18.5.2026, opened today). **Verified.**
  - Search demand: "convention fiscale france israel" 110 a month in France (DataForSEO).
  - How Israel taxes rental income of foreign residents: **unverified**.
- **Israel Land Authority approval for foreign buyers on state land:** **unverified** (nothing official found); answer "à vérifier avec votre avocat".

### 3.4 Prices in euros at the Bank of Israel rate (**verified**)
BOI representative rates, SDMX API (https://edge.boi.gov.il/FusionEdgeServer/sdmx/v2/data/dataflow/BOI.STATISTICS/EXR/1.0/RER_EUR_ILS), last published **23.10.2026** (25.10 is a Sunday):
**1 € = 3.4844 ₪ · 1 CHF = 3.7808 ₪ · 1 $ = 3.112 ₪**. EUR/ILS moved between 3.4722 and 3.4919 over 15 to 23.10.

| Official median deal price (nadlan.gov.il, facts.md 5c) | ₪ | € | CHF |
|---|---|---|---|
| Israel, 4 rooms, Apr to Jun 2026 | 2,028,800 | 582,252 | 536,606 |
| Tel Aviv-Yafo, 3 rooms, Jan to Mar 2026 | 4,225,800 | 1,212,777 | 1,117,700 |
| Tel Aviv-Yafo, 4 rooms, Jan to Mar 2026 | 5,229,800 | 1,500,918 | 1,383,252 |
| Tel Aviv-Yafo, 5 rooms, Jan to Mar 2026 | 7,497,700 | 2,151,791 | 1,983,099 |

These are all deals, new and second-hand together. Rule for the page: **₪ is the contract price; € and CHF are indicative, with the rate and its date printed.** The Barnes and immobilier.co.il cards follow the same principle without printing the rate.

### 3.5 French-community cities
Market evidence only; **no official per-city aliyah statistics were found (unverified)**:
- immoneuf's "villes préférées des francophones" (Netanya 51, Jérusalem 40, Tel Aviv 26, Bat Yam 26, Ashdod 18, Ashkelon 16 listings);
- Google's AI overview (Tel Aviv + Ramat Gan / Holon / Bat Yam, Jerusalem, Netanya, Herzliya, Ashdod);
- the related searches (Bat Yam, Jérusalem, Ramat Aviv);
- the depth of Comacom's neighbourhood lists (Netanya, Ashdod, Jérusalem, Ra'anana);
- search volume (immobilier netanya 90, bat yam 90, jerusalem 40, ashdod 40, raanana 30).

Our own market file (`market.json`, read 25.10.2026, from-prices as published):

| City | Projects | From-price range (₪) |
|---|---|---|
| Tel Aviv-Yafo | 143 | 1,990,000 to 9,490,000 |
| Ramat Gan | 37 | 2,250,000 to 4,790,000 |
| Jérusalem | 34 | 2,070,000 to 10,150,000 |
| Netanya | 29 | 1,990,000 to 8,700,000 |
| Bat Yam | 29 | 2,150,000 to 4,250,000 |
| Herzliya | 19 | 2,750,000 to 5,390,000 |
| Holon | 12 | 1,660,000 to 2,799,000 |
| Ra'anana | 10 | 2,680,000 to 3,700,000 |
| Ashkelon | 10 | 1,585,000 to 2,490,000 |
| Ashdod | 7 | 1,770,000 to 2,990,000 |
| Hadera | 7 | 1,350,000 to 2,990,000 |
| Eilat / Beer Sheva / Netivot | 5 / 5 / 4 | from 1,290,000 / 1,330,000 / 1,320,000 |

The last rows answer "immobilier Israël pas cher". **Gap:** our 15 French project pages (`/projects/*-fr/`) are all Tel Aviv, plus one Bnei Brak office project, and none is in Netanya, Ashdod, Jerusalem or Ra'anana. Under the honesty law the French hub can only list what we publish; the community cities need real pages, not placeholders.

### 3.6 Counting rooms, measuring m², mamad
- **France:** INSEE counts "pièces d'habitation" as the rooms used for living; entrances, corridors, bathrooms and WC are excluded, and the kitchen counts only above 12 m² (https://www.insee.fr/fr/metadonnees/definition/c1572; census rule). Market usage: T4 / 4 pièces = séjour + 3 chambres.
- **Israel:** market listings count the salon as a room ("4 rooms" = salon + 3 bedrooms), so **the counting matches France**. No official definition of "rooms" was found (unverified).
  - The official sale-specification form (צו מכר דירות (טופס של מפרט), Wikisource, opened today) lists "חדר דיור" (living room), bedrooms and "**ממ"ד המשמש כ…**" (a mamad used as a bedroom, storage or other).
  - The form asks for the **number of bedrooms "including / not including the mamad"**: in Israel the mamad is usually one of the bedrooms.
  - Half rooms (2.5, 3.5, 4.5) exist in Israeli listings (BA-HIT filter) and have no French equivalent.
- **Area:** the same official form defines the apartment area as **measured to the outer faces of the exterior walls** (to the middle of walls shared with another apartment). Balcony, parking, storage and garden are listed separately, and a 2% deviation is allowed.
  - French "surface habitable" (CCH R.156-1, as quoted on service-public.gouv.fr F35977) **excludes walls, partitions, stairs and window recesses**.
  - **An Israeli "100 m²" is therefore larger than a French "100 m²".** The gap depends on wall thickness and no official ratio exists; do not publish a percentage. No competitor says this.
- **Mamad:** a reinforced room inside the apartment.
  - It is mandatory in new residential construction since **1992** (State Comptroller follow-up report on sheltering, https://library.mevaker.gov.il/sites/DigitalLibrary/Pages/Reports/2905-92.aspx).
  - The minimum size is 9 m² (Knesset document https://fs.knesset.gov.il/25/law/25_lst_3751647.pdf; check against the regulation text before quoting).
  - We already have `/fr/guides/new-apartment-mamad/` to link.

---

## 4. For our French page

### 4.1 Union checklist (everything any French rival has, plus the Hebrew union where it applies)

Page basics
- Head phrases in title, H1, meta and first lines:
  - "projet(s) immobilier(s) neuf(s) en Israël" (GSC head);
  - "programme(s) neuf(s)" (Google AI, CPC);
  - "projets neufs" (the market's word);
  - "appartement(s) neuf(s)" (GSC, our `/fr/` @37).
- Tel Aviv as a section heading ("programmes neufs à Tel Aviv"). City headings for Jérusalem, Netanya, Bat Yam, Ashdod, Ra'anana, Herzliya **only where we list real projects**.
- Visible "mis à jour le" date and the year (e-projects "2026", immoneuf blog dates).
- Breadcrumbs (e-projects, immoneuf, Barnes Intl, immobilier.co.il).
- hreflang cluster fr ↔ he ↔ en ↔ ru ↔ ar with x-default `/projects/`, as planned in languages.md. Barnes, immobilier.co.il, BA-HIT, Evenis and Shoshia all pair languages.
- Exactly one H1, in French. The rivals' faults: no H1 (immoneuf home, e-projects TLV), an English H1 (immoneuf TLV), an empty title (alloj).

Cards (the rivals' field union)
- Name, city, neighbourhood, street, developer (promoteur).
- **From-price in ₪, with € (and CHF) at the dated BOI rate** (Barnes Intl, immobilier.co.il). A price range ("à partir de … jusqu'à …", immobilier.co.il).
- m² range and pièces range ("du 2 au 5 pièces", Barnes), with the m² measurement note.
- **Delivery month or year** (Barnes, immobilier.co.il filter 2024 to 2030); "livré dans X mois" or "déjà disponible" (e-projects, Evenis).
- Status: prévente / en commercialisation / en construction / livré (Evenis "pré-vente", BA-HIT "vendu").
- Type: TAMA 38, pinoui-binoui, boutique, tour, penthouse, rez-de-jardin, duplex, mini-penthouse.
- Units available by pièces and m² (immobilier.co.il project cards).
- Feature tags, including community features where true: parking, terrasse, ascenseur, **ascenseur de chabbat**, **souccah** (balcon souccah), **mamad**, vue mer, proche mer (Comacom).
- Payment hooks as published: 20/80, "clés maintenant, payez en 2028" (Evenis), presale price.
- Exclusivity or launch badges, only if true.

Content
- An answer paragraph with numbers (count, ₪ and € range, cities) before the grid. Only immobilier.co.il has an intro, and it is unsourced.
- A **₪/m² band per Tel Aviv area** (immobilier.co.il), computed from our own listed projects with dates.
- City sections for the francophone cities (immoneuf zooms; e-projects city menu).
- The "neuf vs ancien" choice (IsraelStart table).
- "Idéal pour": alyah / résidence principale / investissement / pied-à-terre / location saisonnière (e-projects filter).
- Buyer protections with law names and numbers (Shoshia, vaguely).
- Total cost: taxe d'acquisition by status, TVA incluse, avocat, indexation (immobilier.co.il simulator, IsraelStart).
- Financing: apport, LTV, olim (immoneuf FAQ, alloj "Simulateur prêt").
- "Depuis la France": remote purchase, procuration, banking, tax treaty, form 3916 (immobilier.co.il FAQ, partly).
- Pinui-Binui / TAMA 38 explainers (immobilier.co.il FAQ, Evenis guide).
- A lexique of Hebrew terms (Evenis links one).
- FAQ (immobilier.co.il 5, alloj 3, immoneuf 4 hidden, Shoshia 1, AA 1).

Tools
- Filters: ville, quartier, pièces, prix, surface, livraison year, statut, type, features, "idéal pour".
- Sort (price, delivery, newest); list/map; favourites; compare (e-projects); alerts (Barnes, immobilier.co.il, YafoInvest); currency switcher (Barnes); exchange-rate display (Evenis).
- A cost simulator with an **olé track** (nobody has one).
- WhatsApp in French; phone numbers for France and Israel (e-projects, Evenis). Lead routing to lawyer and mortgage advice (immobilier.co.il), without becoming a broker (memory: the Brokers Law exemption holds only while the site never presents itself as a broker).

Structured data
- CollectionPage + **ItemList** of the listed projects (nobody has it), BreadcrumbList, FAQPage that matches visible text (immoneuf's is hidden, Shoshia's is broken), Offer `lowPrice` in ILS only where a price is published. Avoid Product/AggregateOffer on the list page (immobilier.co.il) and self-ratings (Shoshia's AggregateRating).

Internal links (existing French pages)
- `/fr/new-projects/` (the guide: keep the intent split from languages.md), `/fr/sde-dov/` + `/fr/sde-dov/prices/`, `/fr/north-tel-aviv/` + `rova-4/`.
- `/fr/guides/` and in particular `/fr/guides/new-apartment-mamad/`, `/fr/guides/new-apartment-sale-specification/`, `/fr/guides/remote-new-apartment-handover-israel/`.
- `/fr/property-value-estimator/` and the 15 `/projects/*-fr/` siblings.

### 4.2 French FAQ union (deduplicated, natural French)
1. Combien coûte un appartement neuf en Israël en 2026, en shekels et en euros ?
2. Quel est le prix au m² d'un appartement neuf à Tel Aviv ?
3. Où acheter un appartement neuf en Israël : Tel Aviv, Jérusalem, Netanya, Ashdod, Bat Yam ou Ra'anana ?
4. Où trouver un programme neuf pas cher en Israël ?
5. Un non-résident peut-il acheter un appartement neuf en Israël sans faire son alyah ?
6. Peut-on acheter depuis la France, à distance (procuration, visites en vidéo, signature) ?
7. Quelle taxe d'acquisition (mas rechisha) paie-t-on en 2026 : résident, olé hadach ou non-résident ?
8. Y a-t-il des frais de notaire en Israël ? Qui rédige l'acte et combien coûte l'avocat ?
9. Le prix affiché par le promoteur inclut-il la TVA ?
10. Qu'est-ce que la garantie bancaire de la loi Mekher et est-elle obligatoire ?
11. Acheter sur plan en Israël : est-ce comme une VEFA en France, et quels sont les risques ?
12. Comment se passe le paiement : échéancier, formule 20/80, indexation sur l'indice de la construction ?
13. Que se passe-t-il si le promoteur livre en retard ?
14. Quelles garanties après la remise des clés en cas de défauts ou de malfaçons ?
15. Peut-on obtenir un prêt immobilier en Israël quand on vit en France, et quel apport faut-il ?
16. Les olim ont-ils droit à une aide pour leur prêt immobilier ?
17. Que veut dire « 4 pièces » en Israël : le salon est-il compté, et le mamad ?
18. Comment sont mesurés les m² d'un appartement neuf en Israël ?
19. Qu'est-ce qu'un mamad, et tous les appartements neufs en ont-ils un ?
20. Qu'est-ce qu'une prévente et un prix de lancement ?
21. TAMA 38 et pinoui-binoui : de quoi s'agit-il, et est-ce une opportunité ?
22. Comment vérifier un promoteur : permis de construire, accompagnement bancaire, projets déjà livrés ?
23. Quand l'appartement est-il inscrit à mon nom au Tabou ?
24. Comment déclarer en France un appartement ou des loyers en Israël (convention fiscale France-Israël, formulaire 3916) ?
25. Faut-il ouvrir un compte bancaire en Israël, et comment transférer les fonds ?
26. Les prix de l'immobilier neuf en Israël montent-ils ou baissent-ils en 2026 ?
27. Quels sont les projets neufs emblématiques à Tel Aviv (Sde Dov, Kikar Hamedina, Park Tzameret) ?
28. Quel rendement locatif attendre d'un appartement neuf en Israël ?
29. Peut-on acheter un appartement au nom de ses enfants ?
30. Comment comparer les prix des programmes neufs en Israël ?

Sources of the union: immobilier.co.il (1/2, 6, 21, 27), immoneuf (3, 5, 15, 29, "dira hadasha"), alloj (5, 28, budget), Shoshia (10, 11, 13, 22, 23), AA (11, apport), Google PAA (3, 4, 26), GSC (15, 30, "financement"), DataForSEO (2, 18/19, 24), related searches (4, "promoteur", Bat Yam, Jérusalem, Ramat Aviv). Q7, 8, 9, 12, 14, 16, 17, 18 and 20 are asked by no competitor; they come from French buyer needs (section 3). Answers must use only the verified items in section 3 and mark the rest "à vérifier avec votre avocat".

### 4.3 Top 12 things that would put our French page above all of them
1. **One page that is both catalogue and answer.** The H1 and the first paragraph give the count of listed projects, the ₪ range with its **€ equivalent at the dated BOI rate**, and the cities, before the grid (content-first law). Barnes and Comacom have a grid with no answer; AA and Shoshia have an answer with no grid.
2. **Multi-developer cards with the full honest field set**: promoteur, ville/quartier, à partir de ₪ + € (+ CHF), pièces and m² ranges, **livraison**, statut (prévente / commercialisation / chantier / livré), type (TAMA 38, pinoui-binoui, tour, boutique) and an "au" date. Fields we do not have are omitted. Rivals show stale "vendu" cards and 2017 posts (BA-HIT, Evenis) and an expired delivery (Barnes "Avril 2025").
3. **A cost calculator in French with three statuses**: résident, **olé hadach (12A)** and non-résident, with the 31.12.2026 end date of the non-resident rate, TVA incluse, the avocat note and the € conversion. Immobilier.co.il has no olé track and nobody else has rates.
4. **A financing box with the real rule**: 50% maximum LTV for non-citizens and 75% for Israeli citizens on a single home (BOI 329 definitions), plus the olim assisted loan. Rivals say "apport 50 %" with no source, or nothing.
5. **"Lire une annonce israélienne"**: 4 pièces = salon + 3 chambres (as in France), the mamad often counted as a bedroom (official spec form), half rooms, and **Israeli m² measured with the exterior walls** compared with French surface habitable. No rival explains this, and it prevents the first misunderstanding every French buyer has.
6. **Israeli protections, named and numbered, set against the French VEFA**: loi Mekher bank guarantee above 7%, carnet de bordereaux, indexation at most 40%, the automatic late-delivery indemnity (1, 1.25, 1.5 × rent), bedek periods against parfait achèvement, biennale and décennale. Shoshia lists 6 vague risks under a "12 risques" title.
7. **A "Depuis la France" block** with only verified items: the treaty (31.7.1995, in force 1996, MLI), form 3916 (1,500 € fine), the no-notary process. Procuration and banking are marked "à vérifier avec votre avocat". 110 searches a month for "convention fiscale france israel" and no catalogue answers it.
8. **Francophone-city coverage that is real**: Tel Aviv quarters now, with Netanya, Jérusalem, Bat Yam, Ashdod, Ra'anana and Herzliya added as filters and sections only when we publish real projects there (market.json has 7 to 143 per city). Never placeholders (honesty law). The chips mirror the related searches (Bat Yam, Jérusalem, Ramat Aviv, pas cher), as filter states on one URL (URL word law, no rival URLs).
9. **A visible FAQ of 25 to 30 questions that matches its FAQPage markup**, including the questions nobody answers (olim, TVA, notaire, pièces, m², retard, 3916). Immoneuf's FAQ is hidden in schema and Shoshia's is broken.
10. **Clean structured data and language pairing**: CollectionPage + **ItemList** (no rival has it) + BreadcrumbList + FAQPage; Offer only for published ILS prices; no Product snippet on the list, no self-rating; a full hreflang cluster with `/projects/` as x-default. Server-rendered: YafoInvest and the IsraelStart map are empty in raw HTML.
11. **Community-aware features shown only when true**: mamad, ascenseur de chabbat, balcon souccah, parking au cadastre, vue mer. Only Comacom has these, as a filter with no data behind it.
12. **Freshness and trust**: a "mis à jour le" date, each card dated, outdated projects removed, sources kept in the repo, a short neutral line on who we are (a portal, not a broker), WhatsApp in French, France and Israel numbers. Per-project 3D, view and map stages in French are the moat that no francophone agency has.

Findings to report only (no action implied, and no redirect is suggested for any of them):
- **Immoneuf:** UAE demo filler text, FAQPage not visible, English H1 and "Archives des" title on the Tel Aviv page.
- **Alloj:** empty title and meta on `/fr/projet-immobilier-neuf-israel.html`.
- **Barnes International:** a duplicate Tel Aviv city bucket ("1 programmes neufs").
- **E-Projects:** no H1 on the Tel Aviv page.
- **Immobilier.co.il:** Product schema on a list page; "notaires" in an Israeli context.
- **Shoshia:** the 12/6 mismatch, the broken FAQ entity, "Katchlan".
- **AcheterIsraël:** the "Zikaron Dvarim" gloss and "taxe selon la localisation".

Not done here: no copy for our page; Linear and Notion entries are left to the parent session; no GSC write, no indexing action.
