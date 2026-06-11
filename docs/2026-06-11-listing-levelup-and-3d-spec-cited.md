# Listing Level-Up ×10 + Rainbow 3D Apartment Picker — Build Spec (cited, 25 sources)

## A. LISTING FEATURES — priority by MEASURED impact
1. 3D/virtual tour embed (Matterport/iGUIDE/Kuula seam): Zillow data = up to +68% views, saved
   36-79% more, sells 10-14% faster; Matterport = 31% faster, up to +9% price. THE top lever.
2. Floor plans (2D + interactive): +30% more interest (UK data); 80% of buyers rate >=7/10.
3. Multi-step lead form (open with ONE low-commitment question): +37% conversion; 3-step flows
   68% completion vs 41% single-page. + STICKY CTA: ~+35% lead conversion.
4. Inline monthly-cost calculator (משכנתא לפי ריבית בנק ישראל + ארנונה + ועד בית) in the price block.
5. Save/favorite + saved-search alerts (the retention loop the tours feed).
6. WhatsApp-first share + click-to-chat CTA (highest-intent channel in Israel) + callback scheduling.
7. Trust: developer/agent profile card, verified badge, days-on-market, "X צפיות, Y שמירות".
8. Data: price history (gov transaction data), price-per-sqm vs neighborhood median, transit/schools.
   CAUTION (cited): Zillow ADDED then REMOVED climate-risk scores after pushback - only show data we
   can defend.
9. Compare units side-by-side (natural for new projects).
10. AI virtual staging seam (Zoopla×Roomvo pattern) - later differentiator for empty units.

## B. RAINBOW 3D PICKER — recommended stack (Tier 1 now, wow-layer next)
PATTERN (what the SaaS vendors actually do): SVG polygon overlay traced over the developer's
building render; each polygon bound to a unit record; click → unit card → lead CTA.
- Tier 1 MVP (1-3 dev days, ₪0 licensing): responsive <svg viewBox> over the elevation image,
  one <path data-unit-id> per apartment, status colors (זמין=ירוק/שמור=כתום/נמכר=אפור), hover
  tooltip, click → side panel (קומה, חדרים, מ"ר, מרפסת, כיוון, מחיר, תוכנית דירה) + sticky
  "דברו עם היזם" WhatsApp/lead CTA (2-3 step form per A3). units.json feeds it; admin screen
  updates statuses (developer feed later via admin-control).
- Signature wow-layer (phase 2): Mapbox GL fly-in (3D fill-extrusion buildings, animate-camera) from
  city view to the project pin, cross-fade into the SVG building view. CesiumJS OSM Buildings
  (350M+ footprints) for the future all-Israel "drone view" portal map; GovMap for parcels/zoning
  (no public 3D API - use OSM extrusions).
- Tier 3 (per flagship project, developer-funded): Smplrspace (flat fee per floor plan, JS SDK) or
  3D Estate / Render Vision photoreal twins.
HONEST DEPENDENCIES: (1) we need the Rainbow developer's elevation render + per-unit data
(floors/rooms/sqm/price/status) - the engine can ship with demo geometry, real polygons need real
assets; (2) unit status MUST be developer-fed - a stale "available" destroys trust.

## SEO guardrails (owner directive: listings give power, never cannibalize money pages)
- Listing/unit pages target TRANSACTIONAL queries ("דירה 4 חדרים פרויקט קשת תל אביב"); money pages
  keep RESEARCH queries ("מחירי דירות תל אביב"). No price-guide content blocks on listing pages.
- Listing pages link UP to their money/hub page (one contextual link); hubs link DOWN to listings.
- Unit-level pages: noindex until they have unique content; project page is the canonical.
- New listing sections get their own sitemap (already the pattern) + breadcrumbs (already shipped).

Sources (25): Zillow Research 3D, DesignLenz, Matterport ×2, The Negotiator floor plans, AIM Group
Zoopla AI, Zillow climate + Inman reversal, Fast Company Realtor.com, Amra&Elma CTA stats,
WiserNotify, Smplrspace docs+pricing, 3D Estate, UnitAtlas, Render Vision, Flatter, WP Interactive
Real Estate plugin, img-mapper, model-viewer, Mapbox 3D+camera examples, Cesium OSM Buildings,
GovMap, Kuula/Rightmove. (Full URLs in research transcript.)
