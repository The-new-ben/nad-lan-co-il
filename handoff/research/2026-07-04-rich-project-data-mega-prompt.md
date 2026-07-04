# Rich per-project enrichment mega-prompt (fills a record to page-grade)

The collection prompt (v2) builds the base record. THIS prompt is run **once
per project** to make a page rich enough that it never needs mocking. Output
merges into that project's `data/projects/<slug>.json`. Same honesty law:
source + verbatim quote for every value, `null` when unknown, never invented.

Feed the model: the project name, developer, official URL, and the building
address already in the record.

---

> You are enriching ONE new-construction project to feed a premium property
> page. Project: **{NAME}** by **{DEVELOPER}**, official page {URL}, address
> {ADDRESS}. Gather EVERYTHING below from the official page first, then Madlan,
> Yad2, the municipality, press, and planning portals. For EVERY value give a
> source URL and a short verbatim quote proving it. Unknown = null. Never
> invent. If sources conflict, record both with quotes.
>
> **A. Building form (for the 3D model + facade):** floors (min/max), height_m,
> num_buildings, footprint shape + rough dims, main facade orientation
> (compass), podium yes/no + floors, facade material/colour, balcony pattern,
> roof/crown feature, any architectural signature. Architect + a link to their
> project page.
>
> **B. Units & inventory:** total units, unit mix (rooms → count, sqm range per
> type), penthouse/garden/mini-penthouse flags, parking & storage policy, ממ״ד
> (safe room), accessibility, delivery/occupancy year, how many remain / sold
> if published.
>
> **C. Price evidence (label clearly as asking/estimate + as-of date):**
> developer price list if any; else Madlan project price range; else Yad2 active
> listings range; else nadlan.gov.il/rmi recent transactions in the same
> building/street. Give ₪ range, ₪/sqm range, and the source + date for each.
> Never present an estimate as a developer-published price.
>
> **D. Location context (for the honest proximity band + 3D scene anchoring):**
> exact distance + walking time to: the sea/beach, nearest park, light-rail
> station (line + name), planned metro, train station, main highway, retail/
> mall, hospital, and 2–3 notable schools. Is it seafront / sea-view / inland?
> Terrain flat/slope? What dominates the skyline around it? Give the STREET
> ADDRESS and gush/helka so we can geocode — **do not output coordinates.**
>
> **E. Planning / future (the honesty differentiator competitors hide):** TABA/
> plan numbers + mavat.iplan.gov.il links; what is planned on adjacent lots
> (will the sea view be blocked? new tower next door?); urban-renewal type
> (pinui-binui / TAMA); infrastructure coming (metro, park, road). This is what
> makes a buyer trust us.
>
> **F. Media (raw material for the page — collect URLs, do not describe):**
> every render/visualization image URL, floor-plan image/PDF URLs, site-plan
> URL, brochure PDF, promo video URL, virtual-tour/3D URL, official gallery
> page. Note if a public BIM/3D model exists.
>
> **G. Story & SEO (5 languages he/en/fr/ru/ar):** 3–5 genuine USPs (with a
> source, not marketing fluff); the 8–10 real questions a buyer asks about THIS
> project; target audiences; and keyword sets per language. Do NOT write the
> final article — flag which claims are source-backed so our editor writes an
> honest 5-language body from them.
>
> OUTPUT: a single JSON object matching the record schema
> (`data/projects/_schema.json`) with `field_sources` and `evidence` populated,
> plus a `still_missing` list of anything you could not source.

---

## Why Ashira & Dimri Yama were missing (and the fix)
ChatGPT only crawled a handful of developer catalogues (Azorim, Ashtrom,
Israel-Canada, Metropolis, Shikun&Binui). Ashira and Dimri Yama (Y.H. Dimri)
weren't in those, so they never entered the batch — not a bug, a coverage gap.
The per-developer collection prompt (add **Y.H. Dimri** and the Ashira developer
to the developer list) plus these two stub records now in the DB close it. Run
this enrichment prompt on them like any other project.
