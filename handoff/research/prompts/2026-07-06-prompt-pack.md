# Cowork prompt pack - 2026-07-06

Copy-paste each block into Cowork as a separate job. Delivery protocol for all
jobs: create ONE WordPress draft titled "AGENT-INBOX: {job}: {batch}" with the
payload; the cloud agent ingests it and deletes the draft. Never publish drafts.

---

## JOB 1 - GEO EXPEDITION (the big one: coordinates for 961 projects)

You are a geodata researcher for nad-lan.co.il. Mission: find coordinates for
every project in the catalog that has none.

1. Pull the project list: GET
   https://nad-lan.co.il/wp-json/wp/v2/nadlan_project?per_page=100&page=N&_fields=id,slug,title,link
   (iterate N until empty). Skip slugs ending in -en/-fr/-ru/-ar.
2. For each project, open its page link and note the address/city text if
   present. Then determine coordinates by (in order of preference):
   a. Exact address match on Google Maps / GovMap (govmap.gov.il).
   b. Project name + developer + city on Madlan / Yad2 / developer site.
   c. Gush/Helka lookup on GovMap if the page mentions them.
   d. Neighborhood centroid if only the neighborhood is known.
   e. City centroid ONLY as last resort, flagged.
3. Tolerance: up to ~1km is acceptable for unbuilt projects; we display an
   "approximate location" disclaimer for anything below confidence=exact.
4. Deliver in batches of 100 as AGENT-INBOX drafts titled
   "AGENT-INBOX: geo: batch-K". Body = CSV, one line per project:
   post_id,slug,lat,lng,confidence,method,source_url
   confidence in {exact,street,neighborhood,city}; method is one short phrase.
5. Never invent coordinates. If truly unfindable, write NONE in lat/lng and say
   why. Israel bounding box sanity check: lat 29.4-33.4, lng 34.2-35.9.

## JOB 2 - two remaining DUO interior images

(Global rules from interiors-4-projects.txt apply: photorealistic, 24mm eye
level, daylight, 4:3, no people/text/logos, cream+oak+stone palette, original
illustration not developer material.)

Image A - duo-tel-aviv, duo-a-21 (4 rooms, 110 sqm, city skyline):
Contemporary urban living room in a 50 floor Tel Aviv tower, skyline view east,
walnut and off-white palette, built-in library wall, cinematic late afternoon.

Image B - duo-tel-aviv, duo-b-45 (5 rooms, 160 sqm, panoramic):
High floor open living space with wraparound glazing, panoramic city and sea
horizon, pale stone floor, designer curved sofa, twilight with city lights on.

Upload to WP media as interior-duo-tel-aviv-duo-a-21.jpg /
interior-duo-tel-aviv-duo-b-45.jpg, then draft "AGENT-INBOX: interiors:
duo-batch" listing media IDs next to unit ids.

## JOB 3 - DUO language siblings (en/fr/ru/ar)

Open https://nad-lan.co.il/projects/duo-tel-aviv/ and translate the FULL
article body (everything below the 3D theater) into English, French, Russian
and Arabic. Rules: keep every heading level and order; keep all numbers,
prices, disclaimers exactly; do not shorten; no em or en dashes anywhere, plain
hyphen only; translate honestly including all "estimate, not binding" notes.
Deliver 4 drafts titled "AGENT-INBOX: duo-translation: {lang}", body = the
translated HTML.

## JOB 4 - ZOHI Sde Dov article (Hebrew, 3000+ words)

Source material: the ZOHI dossier already ingested (developer Mivne, Levinstein
and Metropolis; Sde Dov district). Write a 3000+ word Hebrew magazine article
for the project page: neighborhood story, the Sde Dov plan (1,300 dunams,
16,000 homes), the developers' track record, apartment mix, buyer fit analysis,
honest market context (2025 correction, current yields), FAQ section (6+
questions). H2/H3 hierarchy, no em/en dashes, every claim sourced from the
dossier or marked as estimate. Deliver as draft "AGENT-INBOX: zohi-article: he".

## JOB 5 - French cornerstone guide

Write "Acheter un appartement en Israel en 2026: le guide complet" in French,
4000+ words, aimed at francophone buyers (France/Belgium/Switzerland Jewish
communities, largest olim group). Cover: purchase process step by step, purchase
tax brackets for foreign residents vs olim (8%/10% above 6,055,070 ILS; oleh
benefits), financing (50% LTV for non-residents), Sale Law guarantees (arvut
bankit), currency transfer, popular cities for francophones (Netanya, Ashdod,
Jerusalem, Tel Aviv, Raanana) with price levels, new-build vs second hand,
lawyer role, 8+ FAQ. Honest numbers only, no dashes, H2/H3 hierarchy. Deliver
as draft "AGENT-INBOX: guide-fr: acheter-2026".

## JOB 6 - price data sweep (batches)

For each project in the catalog batch I give you (50 slugs per run): find the
current asking price range and average price per sqm from public sources
(Madlan, Yad2, developer sites, news). Deliver CSV draft "AGENT-INBOX: prices:
batch-K": post_id,slug,min_price,max_price,avg_sqm_price,source,as_of_date.
Only real published numbers; NONE when nothing public exists. Never guess.

## JOB 7 - facilities and facts sweep (batches)

For each project batch (50 slugs per run): floors, total units, developer name,
architect, expected completion year, amenities (pool/gym/lobby/parking/storage),
construction status. CSV draft "AGENT-INBOX: facilities: batch-K" with a source
URL per row. NONE for unknowns; no guessing.

## JOB 8 - developer profiles

For each developer name I give you (10 per run): founding year, scale (units
delivered), notable projects, stock exchange listing if any, reliability signals
(Sale Law incidents, court cases, delivery delays reported in press), current
active projects. 200-400 words each, Hebrew, with source links. Draft
"AGENT-INBOX: developers: batch-K".
