# Teardown: Zillow (new construction)

Read on 9.11.2026 for the /projects/ hub rebuild. Read-only, no sign-in.

**Evidence classes**
- **[code]:** read live in the owner's Chrome with a DOM script (headings, buttons, JSON-LD types, image boxes).
- **[search]:** a web-search snippet.
- **[prior]:** a known pattern from before this session, not re-checked today.

## Pages read
| Page | URL | Evidence |
|---|---|---|
| City new-construction search | https://www.zillow.com/austin-tx/new-construction/ | [code] |
| Community "buildable plan" page | https://www.zillow.com/community/parten/448105195_zpid/ (resolves to `/community/parten-65ft-lots/448105195_zpid/`) | [code] |
| Builder directory | https://www.zillow.com/home-builders/austin-tx/10221 ("32 builders building 60 communities") | [search] |

## Search, filter and sort
- **Filter bar [code]:** `For sale` · `Price` · `Beds & baths` · `Property type` · `Filters` (the full panel) · `Save search` · `Sort: Homes for You` (a personalised default sort).
- **Result count [code]:** shown as an H2, "5,473 results". The `/new-construction/` path did not visibly narrow the first cards: they were resale homes, and the count is close to the whole city. The new-construction filter appears to live inside the `Filters` panel (listing type), not in the path. This is a finding, not a recommendation.
- **The `Filters` panel [prior]:** listing type (by agent, by owner, new construction, foreclosures, coming soon), open houses only, 3D tour, "must have" (garage, pool, view), days on Zillow, keywords.
- **Map [prior]:** price pins, draw-a-boundary, pin and card hover sync, "Remove boundary", and a list that re-queries when the map moves.

## Cards [code]
- **Fields:** price · `4 bds 3 ba 2,575 sqft` · status (`Active`) · address · brokerage name in small type (the source).
- **Freshness:** "10 hours ago".
- **AI highlight chip:** a short phrase pulled from the listing remarks, such as "Cozy fireplace", "Good sized patio" or "Poolside setting". It gives one memorable fact per card.
- **`Showcase` badge:** the paid premium-media product, labelled on the card.
- **Card controls:** `Save` (heart), `Previous photo` / `Next photo` (a carousel inside the card), and `More` (hide or report).
- **Photo shape:** card photos measured about **1.72:1** (27 of the large images).

## Detail page (community "buildable plan", Plan 228 by Highland Homes) [code]
The modules in rendered order:
1. **Header:** "Buildable plan: Plan 228, Parten: 65ft. lots …", `4 beds 4 baths 3,523 sqft`, an outbound **"View … website"** link to the builder, **"Est.: $7,211/mo"** with **"Get pre-qualified"**.
2. **Sticky tabs:** `Overview` · `Facts & features` · `Community` · `Market value` · `Payment calculator` · `Neighborhood`.
3. **Gallery:** "See all 40 photos", plus an **"Exterior design options"** carousel (`Design 1` to `Design 5`, the elevations).
4. **"What's special":** upper-case highlight tags (GRAND OAK TREES …) above the description.
5. **"Schedule tour":** "Select your preferred tour type, either in-person or real-time video tour", then talk to the builder's representative.
6. **Facts & features**, grouped as Interior · Property · Construction · Community & HOA · Financial & listing details.
7. **About the community:** amenity tags (POOL PARK TRAILS).
8. **"Available homes" table:** `Listing | Price | Bed / bath | Status` (for example, 791 Bird Holw, $1,074,600, 4 bed / 5 bath, Available). This is how buyers see what is ready now inside a plan.
9. **"Estimated market value":** Zestimate® "Not available", estimated sales range "Not available", Rent Zestimate® $4,669/mo. The site says "not available" instead of inventing a value.
10. **"Price history":** `Date | Event | Price`. Each row shows the change in percent, **price per sqft**, **"Source: Highland Homes"** and a **"Report a problem"** link (for example, 11/3/2026, price change, $1,007,990, +1%, $286/sqft).
11. Public tax history.
12. **"Getting around":** Walk Score 0/100 "Car-Dependent", Transit Score 0, Bike Score 20.
13. Nearby schools (source: GreatSchools).
14. Nearby homes, then **"Local legal protections"** (state-level buyer protections), then "Other available plans", "Listing provided by", and nearby cities.
- **Page controls:** `Back to search` · `Save` · `Share` · `Hide` · `More`.

## Personalisation
- **[code]:** Save search, Save, Hide.
- **[prior]:** saved-search emails (instant or daily), the "Saved homes" board, recently viewed, a price-cut notice on saved homes, and view and save counters on the detail page.

## Trust and lead capture
- **Trust [code]:** source attribution on every price-history row, plus "Report a problem"; "Listing provided by"; brokerage name on every card; the local legal-protections module.
- **Lead capture [code]:** "Schedule tour" with a choice of in-person or video, "Get pre-qualified" next to the monthly estimate, and the builder website link.
- **Lead form fields [prior]:** name, phone, email, message, and a financing opt-in checkbox.

## Mobile [prior]
A sticky bottom bar with the "Request a tour" and "Contact" buttons, a floating map/list toggle, and full-screen filter sheets.

## Schema.org types [code]
- **Search:** `Place`, `ItemList`/`ListItem`, `RealEstateListing`+`Product`, `Offer`, `SingleFamilyResidence`, `Apartment`, `QuantitativeValue`, `PostalAddress`, `GeoCoordinates`, `Event` + `VirtualLocation` (open houses and virtual tours), `BreadcrumbList`.
- **Plan page:** the same, without `Event`.

## Performance [code]
- **Search:** 49 images, only 2 with native `loading=lazy`. The list is virtualised by JavaScript.
- **Plan page:** 81 images, 6 lazy, 4 `<link rel=preload>`, gallery tiles at about 1.56:1 and the hero at about 1.84:1.

## SEO [code]
- **Robots:** the `/austin-tx/new-construction/` page carried `meta robots NOINDEX, NOFOLLOW`, with its canonical pointing to itself. Zillow ranks the city hub, not the filter path. This is a finding only; on nad-lan indexing is the owner's decision.
- **Link blocks under the results:** "Search by Bedroom Size", "Homes by Price", "Choose Homes by Amenity", "Select Property Type", "Popular Searches in Austin TX", "Explore Nearby & Average Home Values" (nearby cities, neighbourhoods, ZIP codes), "Estimate Your Home Sale Proceeds", "Have You Considered Renting?".
- **URL patterns:**
  - city: `/austin-tx/`
  - filter: `/austin-tx/new-construction/`
  - community plan: `/community/{slug}/{id}_zpid/`
  - builder directory: `/home-builders/austin-tx/{id}/`, paginated as `/3_p/`

## What nad-lan should take
1. The **"available now" table inside each project**, with columns for unit, price, rooms and status. This is the core of "אכלוס מיידי" (immediate occupancy).
2. **Price history per m², with the source and date on each row and a "report an error" link**, built from the developer's own price lists.
3. **Show nothing rather than a fake estimate.** Where no estimate exists, Zillow writes "Not available"; under our honesty law we omit the field.
4. A **legal protections** module covering the Sale Law guarantee and bank escort (ערבות חוק המכר, ליווי בנקאי).
5. **One AI-free highlight chip per card**, taken from verified facts (for example, "מרפסת 18 מ"ר", an 18 m² balcony).
