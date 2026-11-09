# Teardown: Realtor.com (new construction and new-home communities)

Read on 9.11.2026. Read-only, no sign-in.

**Evidence classes**
- **[code]:** read live in the owner's Chrome with a DOM script.
- **[prior]:** a known pattern from before this session, not re-checked today.

## Pages read
| Page | URL | Evidence |
|---|---|---|
| Search with the new-construction flag | https://www.realtor.com/realestateandhomes-search/Austin_TX/show-newconstruction | [code] |
| Communities hub | https://www.realtor.com/newhomecommunities/Austin_TX | [code] |
| Community detail | https://www.realtor.com/community-detail/Central-Living-Urban-Quick-Move-in-Homes_9000-Waterford-Centre-Blvd_Austin_TX_78758_Q717000115806 | [code] |

## Search (`show-newconstruction`) [code]
- **Filters:** `Price` · `Rooms` · `Home type` (plus more). The first cards were still mostly resale or pending homes, so the URL flag is not a strong filter. The real new-construction experience is the communities hub.
- **Card:** "Brokered by …" on the first line; a status chip (`Pending`, `House for sale`, `Condo for sale`, `New`); `Spotlight` (a paid placement); the price; **a price-cut amount chip** (for example "$300k"); beds, baths, sq ft and lot; the address; `Contact agent`; and `Save property {address}`, a save button whose accessible label includes the address. Photos are counted ("Photo 1 of 3").
- **AI assistant inside the results list:** prompt chips sit between the cards: "Help me narrow down my search" · "Popular neighborhoods in the area" · "What should I know about bu[ying] …" · "How competitive is the market" · "Check local interest rates" · "Ask a question".
- **FAQPage (in JSON-LD) built from live data:** median home price, average time to sell, number of active homes, most popular neighbourhoods, popular ZIP codes and neighbourhoods.
- **Photos:** 30 images, 20 lazy, all 3:2 (1.50).

## Communities hub [code]
- **Page:** "New home communities in Austin, TX", **"46 Communities"**. Sort: `Newest listings` · `Lowest price` · `Highest price`. Toggle: `List` / `Map`.
- **"Popular filters" built on deals:** `All deals` · `Reduced rates` · `Cash at closing` · `Flex cash` · `Appliance package` · `Free upgrades`, plus a **"Promotions explained"** link to an explainer.
- **Card:** "Built by David Weekley Homes" · a deal badge ("Reduced rates") · "tour available" · type ("Community") · **"From $1,649,950"** · "4 - 5 bed · 4 - 5 bath · 3,028 - 3,392 sqft" · name, city and ZIP · `Contact builder`. Some cards are marked "Advertisement".
- **City facts block:** "Median listing home price $525k · Median days on market 78 · Median listing home price per sq.ft $325 · Active listings 6710 · Median rent $1.95k".
- **"How to buy a home in Austin, TX":** get pre-approved, a moving-cost calculator, and `Get estimates` (moving quotes).

## Community detail [code]
- **Modules:**
  - Gallery (`View Gallery`)
  - **`Request a tour`**
  - **"Move-in Ready Homes"** ("These are Ready to Move-in homes at …", a list of units with price, beds, baths and sq ft)
  - **"Office hours"** (here: "Not Available")
  - **Monthly payment, "RealCost™"**: **$12,380/month**, with an **"Apply veterans benefits" toggle**, "Edit payment", home price, loan (30-year fixed average 7.010%), `Get pre-approved`, `View today's rates`, and 30-year and 15-year tabs
  - **"RealCost™ Disclosure"**
  - **"Is this affordable? Calculate your buying power"**
  - Nearby schools
  - Neighborhood ("Explore schools, safety, and lifestyle")
  - **"Veterans & military benefits"**
  - More about this community
  - `Street View`, `See map view in full`
- **Tour request flow:** "Start by selecting a date, **you can provide up to 3 dates** (based on CST)". Date chips run Mon 9 Nov, Tue 10 Nov and so on, with "See more dates". The form then asks for `fullName`, `email`, `phone`, `message` and `isVeteran`.
- **Actions:** `Save listing` · `Share listing` · `Hide listing` · the builder-name button · `Contact builder`.

## Personalisation
- **[code]:** save, hide, share; `Sign up`.
- **[prior]:** saved searches with email alerts, recently viewed, an "Open House" badge with a date, "Price reduced" with the amount and date, "New – X hrs ago", flood, noise and environmental-risk modules, and search by commute time.

## Trust [code]
The broker is named on every card ("Brokered by"). The payment calculation has a disclosure link. Advertisements are labelled. The rates come from named averages.

## Schema.org types [code]
- **Search:** `CollectionPage`, `Audience`, `Country`, `Place`, `State`, `ItemList`, `RealEstateListing`/`Product`, **`BuyAction`**, `Offer`, `SingleFamilyResidence`, `Apartment`, `QuantitativeValue`, `PostalAddress`, `GeoCoordinates`, **`FAQPage`/`Question`/`Answer`**, `BreadcrumbList`, `Organization`, `ImageObject`.
- **Communities hub:** the same set, without the FAQ.
- **Community detail:** `SingleFamilyResidence`, `QuantitativeValue`, `PostalAddress`, `GeoCoordinates`, `BreadcrumbList`, `Organization`, `ImageObject`.

## SEO [code]
- **URL patterns:**
  - city search: `/realestateandhomes-search/{City}_{ST}/` with flag segments (`show-newconstruction`)
  - **separate communities hub:** `/newhomecommunities/{City}_{ST}`
  - community: `/community-detail/{Name}_{Address}_{City}_{ST}_{ZIP}_{id}`
- The FAQ and the city facts block are fed by live market numbers.

## What nad-lan should take
1. **Deal chips, with an explainer page.** The Israeli versions are 20/80 payment, no index linkage (ללא הצמדה), a developer loan (הלוואת קבלן), a discount, and an upgrade package. Each chip shows only on a verified deal.
2. **Tour requests with up to three preferred slots.** The buyer chooses times, not just "contact me".
3. **A full monthly cost with an eligibility toggle.** The Israeli version of "veterans benefits" is "only apartment / Housing Ministry eligibility" (דירה יחידה / זכאות). The total covers mortgage, municipal tax (ארנונה), building committee (ועד בית) and insurance, with a disclosure link.
4. **A city facts block and an FAQ built from live data:** median price per m², projects in marketing, and projects with immediate occupancy.
5. **A separate projects hub per city**, distinct from the general listings search.
