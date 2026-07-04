# MEGA-PROMPT v3 — deep-scan Israel premium projects (paste into ChatGPT/Gemini)

Supersedes v2 for COLLECTION. Changes per owner: deep scan of the WHOLE net
(Madlan explicitly included, but never alone), include projects **not yet
built** or with thin info — if they exist, they enter the dataset with a
lifecycle stage; locations may be *determined* from cross-referenced sources
but stay quarantined until our geocoder confirms; collect the 3D-generation
fields (floor plans, apartments-per-floor, facade data) so pages and GLB
models can be generated without faking. Run ONE prompt per developer or per
city-district; merge downstream. The enrichment prompt
(2026-07-04-rich-project-data-mega-prompt.md) still runs per-project afterward.

---

> ## Mission
> Build a verified dataset of **premium new residential projects in Israel** —
> prioritize Gush Dan (Tel Aviv-Yafo, Ramat Gan, Givatayim, Bat Yam, Holon,
> Herzliya, Petah Tikva, Ramat HaSharon, Bnei Brak, Rishon LeZion) — covering
> the FULL lifecycle: **planning/approved, pre-marketing, in marketing (בשיווק),
> under construction, final units**. This run covers: **{DEVELOPER or DISTRICT}**.
>
> ## Deep-scan directive (do not skim one site)
> Sweep ALL of these source classes and cross-reference:
> 1. Developer official sites & project microsites (rainbowtlv.com-style).
> 2. **Madlan** (madlan.co.il) — project pages, prices, inventory. USE it, cite
>    it; but never as the only source for a fact.
> 3. Yad2 new-projects listings.
> 4. Business press: Globes, Calcalist, TheMarker, Bizportal (deals, prices,
>    marketing launches).
> 5. Municipal + planning: mavat.iplan.gov.il, city engineering sites, local
>    committee decisions (for approved-not-yet-built).
> 6. Skyscraper/urbanism forums & Wikipedia for tower specs (secondary,
>    flag as unofficial).
> 7. Architect & contractor portfolios (Rani Ziss, Barel Levitsky, etc.).
> 8. The developer's investor-relations reports (TASE filings) for unit counts
>    and sales pace — these are gold and rarely wrong.
> A project that exists but has thin data is INCLUDED with `lifecycle` set and
> a `data_gaps` list — never silently dropped. (Ashira and Dimri Yama in Sde
> Dov were dropped in a previous run because only 5 developer catalogues were
> crawled — that failure mode is forbidden.)
>
> ## Per project — collect with evidence
> For EVERY field: value + source URL + a verbatim quoted snippet. Unknown =
> null + entry in `data_gaps`. Conflicts: record ALL versions with quotes.
> - identity: name he/en/aka, developer, co-developers, contractor, architect,
>   interior designer, lifecycle stage (with the exact status wording quoted),
>   official/madlan/yad2 URLs.
> - location: **street address of the BUILDING** (sales office separately),
>   city, neighborhood, gush/helka. If no explicit address: triangulate from
>   multiple sources (press + planning docs + map descriptions) and output your
>   best `location_hypothesis` — address-words only, PLUS the evidence for it.
>   **Never output lat/lng as fact.** You may add `coord_estimate_unverified`
>   {lat,lng,basis} — it goes to quarantine until our geocoder confirms.
> - scale: floors per building (exact), height_m, num_buildings, total_units,
>   podium floors, floor_height_m if published.
> - **3D-generation pack** (feeds our GLB/facade factory):
>   * typical floor plan image URL (תוכנית קומה טיפוסית) + apartments per
>     floor + their arrangement (which lines face which direction),
>   * facade renders per orientation + which facade faces which street/sea,
>   * site plan / building placement image,
>   * facade materials & colors, balcony pattern, roof/crown feature.
> - units & inventory: mix (rooms→count, sqm ranges), penthouses/garden,
>   parking/storage, ממ״ד, delivery year, remaining/sold if published.
> - prices: developer price list if published; else Madlan range; else press
>   quotes; else recent same-street transactions (nadlan.gov.il). Each with
>   URL + as-of date + basis label. Never invent, never average silently.
> - context: distance + walking time to sea/park/light-rail (line+station)/
>   planned metro/train/highway/mall/hospital/schools; what will be built on
>   ADJACENT lots (view-blocking risk!); urban-renewal type; planned
>   infrastructure.
> - media: every render/floorplan/brochure/video/virtual-tour URL.
> - story: 3-5 sourced USPs; 8-10 real buyer questions; audiences; keyword
>   sets he/en/fr/ru/ar.
>
> ## Output
> Real downloadable files: (1) JSON array matching our schema with
> `field_sources` + `evidence` + `data_gaps` per project; (2) an `excluded`
> array (name, reason, status quote, source); (3) a `coverage` report: which
> source classes you actually swept for each developer, and what you did NOT
> get to — silence about skipped ground is forbidden.
>
> ## Hard rules
> - No invented values, URLs, prices, or coordinates. Quotes must be verbatim.
> - Thin-but-real projects are IN (with gaps listed), duplicates merged,
>   sold-out/occupied go to `excluded` with the status quote.
> - If two sources disagree, keep both; do not adjudicate.

---

## Developer/district run list (to reach full Israel coverage)
Azorim, Ashtrom/Ashdar, Israel-Canada (incl. rainbowtlv microsites), Metropolis,
Shikun&Binui, **Y.H. Dimri**, **Avisror** (Ashira), Acro, Aura, Gindi, BSR,
Rotshtein, Tidhar, Africa-Israel, Almogim, Electra Residence, Ampa, Prashkovsky,
Hagag, Levinstein, Kardan, ILDC/נכסים ובניין, Menivim, plus districts: Sde Dov
(all), Bursa RG, Herzliya coast, Bat Yam seafront, TLV Rova 3/4.

## Pipeline reminder (our side, not the model's)
model output → `data/projects/` merge → **geocode pass** (govmap/Mapbox from
addresses; coord estimates stay quarantined) → **price pass** dates verified →
enrichment prompt per project → 5-lang articles → factory (pages + GLB) →
`ready_for_page: true`.
