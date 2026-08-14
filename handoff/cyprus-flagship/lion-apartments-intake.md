# LION APARTMENTS (Oliel Group, Paphos) - intake dossier
Date: 2026-07-12 | Source: https://olielgroup.co.il/properties/kings-apartments/
Owner authorization: the developer asked to list his properties (owner has corporations in Cyprus). Real materials, real name allowed later by owner; page ships with real project data.

## Why this project (selection round)
41 properties scanned via properties-sitemap.xml. Compared 8 apartment candidates:
Lion Apartments wins decisively: 72 units (next best: boutique-complex 50),
9,100 sqm plot, 5 buildings, from EUR 290,000, richest material set
(20+ renders, 2 architectural master-plan sheets, full amenity list).

## The verified spec (extracted from the live page)
- Name: Lion Apartments | Location: Tombs of the Kings road, Paphos, Cyprus
- Status: under construction (בבניה)
- Plot: 9,100 sqm, GATED community, 5 separate buildings, 72 luxury apartments
- Mix: 1-3 bedrooms, 1-3 baths | 52-107 sqm built, 65-138 sqm total (incl. balconies)
- Price: from EUR 290,000
- Location: 2-5 min drive to beaches, restaurants, tavernas, supermarkets,
  cafes, the mall, the harbour and the old town; on the Tombs of the Kings axis.
- Amenities (developer list): spa + gym (jacuzzi + sauna), lobby, LARGE MAIN
  POOL + separate kids pool + pool bar, lounge areas, concierge, 24h security,
  green areas + playgrounds, covered private parking, spacious balconies,
  built-in closets (kitchen + bedrooms), alarm per apartment, quality ceramic
  tiles, AC throughout, kitchen/living/dining open plan.

## Visual DNA (from renders + master plan, viewed 2026-07-12)
- Architecture: modern white Cypriot low-rise. 3 residential floors above a
  ground/pilotis parking level. DEEP cantilevered balconies with glass
  railings + planter boxes. Oversailing flat roof slab. Floor-to-ceiling
  glazing, white plaster, warm night lighting.
- Site (master plan "THIRD FLOOR" sheet): 4 residential slabs at the corners
  (NW long, NE, SW, SE long) around a CENTRAL RECTANGULAR POOL courtyard,
  + a smaller 5th amenity/technical building on the west edge. Internal road
  loop, perimeter landscaping. Each residential building ~6 units/floor.
- Unit inventory derivation: 72 units / 4 residential buildings = 18 each =
  6 per floor x 3 floors. Mix per floor: 2x1BR (52-58 sqm), 3x2BR (75-88),
  1x3BR (100-107, corner). Pricing: 1BR from 290K, 2BR ~360-430K, 3BR
  ~480-560K EUR, top floor premium ~6-8%.

## Materials downloaded (scratchpad/oliel/) - to re-upload to OUR media
- lion-render-1.jpg (facade night render - HERO)
- lion-render-7.jpg, lion-9.jpg, lion-15.jpg (renders/interiors)
- lion-plan-a.png, lion-plan-b.png (architectural master plan sheets)
- Full-size URLs on the source site (never hotlink; upload to our WP media).
- More renders available: uploads/2025/01/{1,3,4,5,6,7,8,9,11,13,14,15,16,17,19,20,21,22,23}.jpg

## Build plan (layers)
L1 intake (THIS FILE) - done.
L2 world: add 'cyprus' to nadlan_gw_worlds (VAT 5% reduced first-home /
   19% standard, NO annual property tax since 2017, transfer fees waived on
   VAT sales, title-deed caution, non-dom, 300+ sun days, Paphos market).
L3 model: bespoke GLB via the factory scripts (5 white blocks around a blue
   pool courtyard per the master plan; 3 floors + pilotis + roof slabs +
   balcony bands). Register in INVENTORY.md.
L4 unit data: 72-unit JSON per the derivation above, hotspots per building
   (the intl picker needs multi-building placement - extend geometry).
L5 page: nadlan_intl post lion-apartments-paphos, world=cyprus, gallery of
   uploaded renders, plans section, real map (34.7754, 32.4066 approx -
   verify on the Tombs of the Kings axis), facilities (real list), engine-
   grade picker, lead form, scheduler? (intl not whitelisted - keep lead).
L6 pipeline doc: docs/playbooks/international-project-intake-pipeline.md.
L7 verify live E2E + AGENT-LOG + commit + owner honesty statement.
