# Teardown: Redfin (new homes and communities)

Read on 9.11.2026. Read-only, no sign-in.

**Evidence classes**
- **[code]:** read live in the owner's Chrome with a DOM script.
- **[prior]:** a known pattern from before this session, not re-checked today.

## Pages read
| Page | URL | Evidence |
|---|---|---|
| City new homes | https://www.redfin.com/city/30818/TX/Austin/new-homes | [code] |
| Community | https://www.redfin.com/TX/Austin/Easton-Park/community/36463 | [code] |
| Home detail (a Compass "Coming Soon" listing) | https://www.redfin.com/TX/Austin/219-Lessin-Ln-78704/unit-6/home/187798317 | [code] |

## Search, filter and sort [code]
- **Titles:** the page title is "Austin, TX New Homes for Sale & New Construction in Austin, TX | Redfin". The H1 begins "New homes for sale & real estate in …".
- **Controls:** **`AI Search`** (natural-language search) · `For sale` · `Price` · `Beds/baths` · `Home type` · **`Filters • 1`** (the button shows how many filters are active) · `Save search` · `Layout` (map and list split).
- **Map tools:** `Draw` · `Remove outline` · `Undo last edit` · `Keyboard shortcuts` · `Toggle fullscreen view` · map type options.
- **Hidden filters [prior]:** time on Redfin, open house and 3D-tour toggles, price-reduced, "include new construction", school rating, and HOA ceiling.

## Cards [code]
- **Freshness badge:** "NEW 11 HRS AGO".
- **"ABOUT THIS HOME":** a one-line pitch printed on the card.
- **Fields:** price · beds · baths · sq ft · address.
- **Key-feature line:** for example, "Layered millwork • Inset cabinetry • Substantial trim".
- **Pre-market badges:** "**EARLY ACCESS**" and "**COMPASS COMING SOON**". Redfin shows listings before they reach the open market (Compass phase 2).
- **Caption from the agent:** "HUGE PRICE ADJUSTMENTS".
- **Photos:** 3:2 (1.50) on 50 of the 54 large images, which is very uniform.

## Community page (Easton Park, Pacesetter Homes) [code]
- **Summary strip:** **"$437,900 Price from · 14 Listings · 1,700 - 2,942 Sq Ft · 3 - 5 Bedrooms"**.
- **Section nav:** `Community details` · `All new homes` · `Around this area` · `Schools`.
- **Modules, in order:**
  1. Experience [community], the description.
  2. Community amenities: Clubhouse, Park, Swimming Pool, Trails.
  3. **Sales office**, with the address and "Provided by Zillow" (the data is credited even when it comes from a rival).
  4. **About the builder**, "Built by …", with the founding year.
  5. **All new homes**, split into **"Available homes (2)"** (move-in now, each with a NEW CONSTRUCTION badge) and **"Ready-to-build homes (12)"**. The second list has bedroom chips with counts, **"All (12) · 3 Bed (7) · 4 Bed (4) · 5 Bed (1)"**, plan cards with "from" prices ("Veranda II Plan … $640,900+") and a "Show all ready-to-build" link.
  6. Commute, then Around Easton Park: Walk Score 9/100 "Car-dependent", Transit 0/100.
  7. Schools.
  8. **"Are you a builder? Learn how to advertise your homes on Redfin"**, a sales line to builders on a buyer page.
  9. Recommended nearby communities, then "New Listings in 78744".

## Home detail [code]
- **Tabs:** `Overview` · `Neighborhood` · `Property details`. **Actions:** `Favorite` · `Hide` · `Share`. Every photo button has an accessible label ("View photo 1: 219 Less…").
- **Modules:**
  - About this home
  - Listing agent
  - **Payment calculator**: "$6,303 per month", split into principal and interest $4,576, property taxes $1,515, HOA dues $0, home insurance $212 and utilities, with a `Reset` button
  - **Open houses** ("No upcoming open houses.")
  - Around this home: schools K-12, preschool and daycare
  - Property details
  - Public record
  - **Sun exposure**: Sunscore **77/100 "Good sunlight"**, with the note that there "appears to be minimal shading by surrounding buildings, terrain, and vegetation"
  - **"This home is coming soon"**, which asks the buyer to contact the listing agent
  - **"Early Access listings"** carousel
  - Nearby similar homes
- **Lead form:** first name, last name, email, phone, message, sent to the named agent of the listing brokerage (Compass).

## Personalisation
- **[code]:** Save search, Favorite, Hide.
- **[prior]:** saved-search alerts (instant or daily), favourites with notes and sharing, the "Redfin Estimate" (a value range with comparable sales), a "Hot Home" badge (likely to sell fast), a "Go tour" slot picker, and price-drop notices.

## Trust [code]
- Data sources are named ("Provided by Zillow", GreatSchools, Walk Score).
- A Fair Housing statement sits in the footer.
- The named agent and brokerage appear on every listing.

## Schema.org types [code]
- **Search:** `Organization`, `SingleFamilyResidence`, `PostalAddress`, `GeoCoordinates`, `QuantitativeValue`, `Product`, `Offer`, `Event` + `VirtualLocation`, `Place`, `Accommodation`, `BreadcrumbList`, `ListItem`, `State`, `City`.
- **Community:** `Organization`, `SingleFamilyResidence`, `Product`, `Offer`, `BreadcrumbList`.
- **Detail:** `Product`/`RealEstateListing`, `ImageObject`, `Offer`, **`BuyAction`**, `Apartment`, **`LocationFeatureSpecification`**, `BreadcrumbList`.

## Performance [code]
- **Search:** 72 images, 48 with native lazy loading.
- **Community:** 50 images, 27 lazy.
- Photos are 3:2 throughout.

## SEO [code]
- **Footer link blocks:** Neighborhoods · Nearby Cities · Zip Codes · **Nearby Cities with New Homes** · **Nearby Neighborhoods with New Homes** · More to explore · **"How to buy a house in Austin, TX"** (How much house can I afford? / How to buy a house in 10 steps / First-time homebuyer's guide) · "38 Redfin agents serving Austin" · Popular Markets in Texas.
- **URL patterns:**
  - city new homes: `/city/{id}/{ST}/{City}/new-homes`
  - community: `/{ST}/{City}/{Community}/community/{id}`
  - home: `/{ST}/{City}/{address}/unit-{n}/home/{id}`

## What nad-lan should take
1. **The project summary strip:** "from ₪ · units available · m² range · rooms range".
2. **Two lists inside every project:** "available now" (דירות זמינות) and "plans on paper" (על הנייר), with room chips that carry counts.
3. **A "sun and light" score, only when it is computed from real building-height data.** It must never be a guessed bearing (our honesty law).
4. **"Developer? Advertise here"** on every project page, which earns money.
5. **Footer blocks for nearby cities and neighbourhoods with new projects**, for internal linking.
