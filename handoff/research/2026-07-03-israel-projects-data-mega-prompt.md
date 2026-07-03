# MEGA-PROMPT — Israel premium new-project dataset (for Gemini / Google Pro)

Paste everything between the lines into Gemini (or another deep-research model
with web access). It collects a structured dataset of Israel's premium new
residential projects currently in marketing, with enough parameters to generate
rich multilingual pages AND realistic 3D massing on nad-lan.co.il.

Owner note: run it ONE AREA AT A TIME (start Tel Aviv + Gush Dan). Depth beats
breadth. Expect partial coverage — that is fine and honest.

------------------------------------------------------------------------------
ROLE
You are a senior Israeli real-estate data researcher and GIS analyst. You are
meticulous, source-driven, and you NEVER invent facts. Unknown = null, always.

MISSION
Build a structured dataset of NEW residential projects in Israel that are
CURRENTLY IN ACTIVE MARKETING (pre-sale, "בשיווק", or under construction with
units still for sale). Focus on PREMIUM / large / landmark projects. I will use
this to generate rich, multilingual, SEO-strong project pages and to generate
3D building massing, so I need location, context, prices, media links, and GIS.

SCOPE (do this batch only)
- AREA: {{Tel Aviv + Gush Dan: Tel Aviv-Yafo, Ramat Gan, Givatayim, Bat Yam,
  Holon, Herzliya, Petah Tikva}}  ← change per run (e.g., "Jerusalem", "Haifa
  + Krayot", "Netanya + Sharon", or "all Israel — top 100").
- TARGET COUNT: aim for 40–60 projects this batch. Quality over quantity.
- INCLUDE: new-construction towers, פינוי-בינוי / התחדשות עירונית flagships,
  luxury and mega projects. EXCLUDE: resale-only, single small buildings,
  projects already fully sold/occupied.

HARD HONESTY RULES (most important section)
1. Every non-obvious field MUST carry a source URL in the parallel `_src` field.
   No source → put the value in `_unverified` and flag confidence "low".
2. Prices: developers rarely publish. If no published price, derive an ESTIMATE
   from Madlan/גזית area ppsqm or recent gov deals, and set price_basis:
   "estimate" + the source + the date. NEVER present an estimate as a firm price.
3. Coordinates/GIS: use official/municipal/Mapbox geocoding of the real
   address. If you cannot verify to building level, set gis_confidence:"approx".
4. If a project cannot be verified as "in marketing", drop it and list it under
   `excluded` with the reason.
5. Do not merge two projects; do not guess developer/architect. Null is better
   than wrong.

WHERE TO LOOK (use several, cross-check)
- Developer official project sites (best for renders, brochures, floor plans,
  unit mix, marketing status).
- madlan.co.il (project pages, area ppsqm, transactions, future plans).
- yad2.co.il / yad1 (new-projects, unit types, virtual tours).
- nadlan.gov.il / רשות המסים (recent real transaction prices in the area).
- mavat.iplan.gov.il and municipal GIS (TABA / תב"ע plan numbers, plot polygon,
  permitted floors/height, land use).
- gov.il urban-renewal and התחדשות עירונית registries.
- News/real-estate press (Globes, Calcalist, TheMarker) for scale, price,
  timeline, developer.
- Google Maps / satellite for context (sea distance, parks, transit, skyline).

OUTPUT
Return a single JSON array `projects` (schema below), plus:
- `methodology`: 3–5 lines on sources used and how prices were derived.
- `coverage`: per-project % of fields filled + overall.
- `excluded`: [{name, reason}].
- `could_not_verify`: fields you most often had to leave null.
Return valid JSON only in a fenced block, then the prose notes.

PER-PROJECT SCHEMA (fill every key; null if unknown; each factual key has a
matching `<key>_src` URL where possible)

{
  "id": "slug-lowercase-latin",
  "identity": {
    "name_he": "", "name_en": "", "aka": [],
    "developer": "", "contractor": "", "architect": "",
    "marketing_status": "presale|under_construction|final_units|unknown",
    "urls": {"official":"", "madlan":"", "yad2":"", "developer":""}
  },
  "location": {
    "address_he": "", "city": "", "neighborhood": "",
    "gush": "", "helka": "",
    "lat": null, "lng": null, "gis_confidence": "building|approx|city",
    "plot_polygon_geojson": null, "ground_elevation_m": null
  },
  "context": {                              // drives realistic 3D + copy
    "dist_to_sea_m": null, "sea_bearing_deg": null, "seafront": false,
    "terrain": "flat|hill|slope|null",
    "skyline": "tower_cluster|midrise|lowrise|mixed|null",
    "near": {
      "park": {"name":"","dist_m":null},
      "light_rail": {"line":"","station":"","dist_m":null},
      "metro_planned": {"line":"","dist_m":null},
      "train": {"station":"","dist_m":null},
      "highway": {"name":"","dist_m":null},
      "retail_mall": {"name":"","dist_m":null},
      "hospital": {"name":"","dist_m":null},
      "schools": [], "landmarks": []
    }
  },
  "building_form": {                        // for 3D massing generation
    "floors": null, "height_m": null, "num_buildings": null,
    "footprint_shape": "rect|L|T|curved|twin|null",
    "footprint_dims_m": {"x":null,"z":null},
    "main_facade_orientation_deg": null,    // 0=N,90=E,180=S,270=W
    "has_podium": null, "podium_floors": null,
    "setbacks": null, "twist": null,
    "facade_material": "glass|stone|mixed|null", "balconies": null
  },
  "units": {
    "total_units": null,
    "mix": [{"rooms":null,"count":null,"sqm_min":null,"sqm_max":null}],
    "price_min": null, "price_max": null,
    "ppsqm_min": null, "ppsqm_max": null,
    "price_basis": "published|estimate|null", "price_date": ""
  },
  "market": {
    "area_ppsqm": null,
    "nearby_projects": [{"name":"","dist_m":null,"ppsqm":null}],
    "recent_area_deals": [{"address":"","price":null,"sqm":null,"date":""}]
  },
  "urban_future": {
    "taba_plan_numbers": [], "taba_urls": [],
    "planned_infrastructure": [],           // metro line, park, road
    "renewal_type": "tama38|pinui_binui|new|null"
  },
  "media": {                                // for our generation + internal tools
    "render_urls": [], "video_urls": [], "brochure_pdf": "",
    "floorplan_urls": [], "site_plan_url": "",
    "virtual_tour_url": "", "bim_or_3d_available": "yes|no|unknown",
    "aerial_or_streetview_ref": ""
  },
  "content_angles": {                       // seeds the multilingual article
    "usp": [], "buyer_questions": [],
    "audiences": ["local","investor","olim_en","olim_fr","ru","ar"],
    "keywords_he": [], "keywords_en": []
  },
  "confidence": {"overall":"high|med|low","notes":""}
}

FINAL REMINDERS
- One area per run. 40–60 projects. Cross-check every price.
- Prefer null over a guess. Flag every estimate.
- Return downloadable JSON. This dataset must be safe to publish, so no
  fabricated numbers and no unverifiable claims.
------------------------------------------------------------------------------

## Why these exact parameters (for our side)
- `context.*` + `building_form.*` let the factory generate a building that
  matches reality — inland vs seafront, correct orientation, real footprint —
  killing the "every tower is on the sea" defect.
- `units` + `market` feed the honest price block and comps.
- `media.*` gives us real renders/floorplans/tours to power the gallery,
  facade, and interior view instead of placeholders.
- `urban_future.*` is unique, high-trust content Madlan/Yad2 barely surface.
- `content_angles.*` seeds the 5-language article so SEO has real fuel.
