# Competitive teardown: residential listing pages and listing-creation flows, 2024–2026

> **Provenance:** supplied by the owner 2026-07-01 (external research, Zillow/Redfin/Realtor.com/
> Rightmove/Idealista/ImmobilienScout24/Compass/Madlan). Saved verbatim as the canonical
> gap-closing spec for the nad-lan listings vertical. The source text ended mid-sentence in
> the Realtor.com/Avail section — everything below is as received. Implementation status
> against this spec is tracked at the bottom (added by Claude).

Scope note. This is the public, observable anatomy of the leading portals as of July 1, 2026. Some details vary by country, MLS feed, listing class, brokerage account, paid ad package, and A/B test. Authenticated agent back offices are only visible where portals publish help docs or marketing pages, so I distinguish observed listing-page behavior from documented creation tooling.

## 1. The complete world-class listing-page anatomy

A world-class residential listing page is no longer just "photos + price + contact agent." The leaders converge on a layered product: media, price/facts, financing or total-cost explanation, structured facts, location intelligence, risk/compliance, history/valuation, trust/provenance, and conversion CTAs.

### A. Above-the-fold: identity, status, trust, and conversion

- **Listing status and transaction type:** for sale, for rent, sold, off-market, coming soon, pending/contingent, price reduced, added/reduced date, active/rental availability date. Zillow shows status, price, beds/baths/sqft, address, year built, garage, HOA, price/sqft, days/views/saves, and source/MLS checked timestamps. Redfin: Overview/Neighborhood/Property details/Sale & tax history/Climate tabs plus price, status, key facts, listing source, days/views/favorites. Realtor.com: tabs for property details, home value, property history, improvements, neighborhood/schools, environmental risk.
- **Price/rent presentation:** asking price; price qualifier; rent per month; price/sqft or price/m²; cold rent/warm rent; deposits (rent/holding/security); service charges; council tax/EPC (UK); Kaution/Nebenkosten/Warmmiete (DE); HOA/condo/co-op fees (US). Rightmove exposes tenure, council tax, parking/garden/accessibility, EPC, deposits. ImmoScout24 exposes cold/warm rent, price/m², SCHUFA, balcony/cellar/elevator/fitted kitchen/accessibility, floor, available date. Compass exposes co-op/condo maintenance, common charges, min down, taxes, HOA, pet policy, lease/availability.
- **Primary fact strip:** beds, baths, living area, lot area, rooms, floor, total floors, property type, year built, tenure, parking/garage, pet policy, furnished, available date, lease term, smoking, lift, balcony/terrace/garden, energy rating — localized (sqft US/UK, m² ES/DE/IL, arnona/vaad bayit/mamad IL).
- **Trust/provenance:** listing agent/broker, MLS number/source, "last checked"/"listing updated" timestamps, public-record source, verification, listing ref/object ID, report-a-problem. Madlan has "report mistake."
- **Lead/contact block:** contact agent/manager/landlord; tour request; phone reveal; callback; consent language; apply-online for rentals. Idealista: Contact / Call / View phone / Discard / Save.

### B. Hero media and gallery patterns

- Photo gallery + visible count (Realtor.com "1/33", Idealista "1/41"). Zillow guidance: 22–27 photos for sale, 10–15 minimum for rentals (performance guidance, not upload caps).
- Full-screen gallery UX: grid, thumbnails, room labels, swipe/keyboard, "see all media", captions, order, hero cover, map/street-view entry, "Fly around"/aerial (Realtor.com).
- 3D/virtual tours: Zillow 3D Home (free tours + interactive floor plans); Zillow Showcase (interactive floor plans + SkyTour); Rightmove Overseas virtual tours/videos; idealista/tools videos + 360 tours + floor plans.
- Floor plans: more standard in UK/EU than US. Rightmove "Floorplan 1"; Showcase interactive plans.
- AI media: Zillow Showcase AI virtual staging + AI auto-selects top 3–5 photos/featured rooms. Rightmove 2025: AI Keywords + "Style with AI" (restyle, remove furniture, relight).
- Disclosure/moderation: image rights; California 2026 law requires disclosure of digitally-altered listing photos.

### C. Price, affordability, and total monthly cost

- Mortgage/monthly module: price, down payment, term, rate/APR, P&I, property tax, insurance, HOA, mortgage insurance, utilities, closing costs, affordability, preapproval CTA (Zillow/Redfin/Realtor.com RealCost/Compass).
- Rent total-cost fields: base vs all-in rent, deposits, move-in/pet/application fees, utilities included, lease length, availability, furnishing, screening, online apply, tour availability.
- Localized ownership costs: UK tenure/council tax/EPC/service charge; DE Hausgeld/commission/energy cert; IL arnona, vaad bayit, mamad, parking, elevator, entry date.

### D. Description, highlights, and AI summaries

- Agent/owner narrative + legal caveats + listing ref.
- Highlights / "What's special": Zillow shows highlights above description; algorithmically/AI-derived from remarks; needs human correction + audit trail.
- AI assistants: Zillow AI Mode (affordability Q&A, compare, book tours); Redfin conversational search + "Ask Redfin" (answers from listing details, market, schools, amenities, zoning/ADU, touring).
- Multilingual: Idealista EN pages; IS24 partial EN; hreflang not reliably observed — implement language versions explicitly.

### E. Facts & features taxonomy (superset data dictionary)

- **Interior:** bedrooms, bathrooms (full/half/¾), total rooms, room names/levels, appliances, laundry, flooring, basement, fireplace, closets, pantry, ceilings, windows, smart-home, furnished, accessibility adaptations.
- **Building/construction:** property type, style, building/unit type, levels/floor, total floors, year built, materials, roof, foundation, condition, renovation history, new build, energy cert/EPC, heating/cooling source, elevator, concierge/amenities.
- **Lot/exterior:** lot size, parcel/cadastral ID, zoning, frontage, yard/garden/patio/balcony/terrace, pool, fencing, views, waterfront, outbuildings; IL adds bars, storage, mamad.
- **Utilities:** heating, cooling, fuel, water/sewer, electricity/gas, internet, solar/green, consumption, utility estimates, included utilities (rentals).
- **Parking:** garage y/n + spaces, attached/detached, driveway, allocated, included/optional, purchase price, bike storage, street parking.
- **Accessibility:** step-free, lift, accessible route, adapted features, "ask agent" if unknown.

### F. History, valuation, and public-record intelligence

- Price/listing history: list date, price changes, prior sales, removed/relisted, sold price, rent history, tax assessed value.
- Tax history: annual tax, assessed/taxable value, APN/parcel (Redfin most detailed).
- AVM/estimates: Zestimate/Rent Zestimate; Redfin Estimate + verified-owner Owner Estimate (edit facts, choose comps); Realtor.com estimated value/similar estimates.
- Comps/nearby: similar homes, nearby solds, nearby rentals, price trends, price per m²; Madlan unusually strong in IL with nearby/building/street transaction tables.

### G. Schools, neighborhood, commute, risk, and map intelligence

- Schools: US portals use GreatSchools; Rightmove School Checker by Experian (Ofsted, admissions, age ranges). Fields: assigned/nearby, rating, grades, type, distance, boundary, district search, catchment.
- Walk/transit/bike + commute: Zillow Walk/Transit/Bike Score + Travel Times; Redfin owns Walk Score; Realtor.com commute by TravelTime.
- Map layers/POIs: pin, approximate/exact, Street View, satellite, schools, transit, cafes/groceries, traffic/noise/flood/wildfire layers, draw-on-map/polygon search, saved-search alerts. Idealista draw-your-area; Realtor.com noise heat map (traffic, airports, restaurants, gas stations, stadiums, schools).
- Climate/environmental risk: First Street flood/fire/heat/wind/air on Redfin/Realtor.com; Zillow surfaces/links climate risk. Redfin adds historical weather + sun exposure (Shadowmap).

### H. Conversion and retention actions

Save/favorite, hide/discard, share, report, alerts/new-listings email, recent searches, tour scheduling (instant/self-guided/virtual/in-person on Zillow rentals; video-chat on Redfin), open house, contact/call/view phone, apply online, mortgage/preapproval, seller/owner CTAs.

## 2. Portal-by-portal notes (as received)

- **Zillow:** hero media, price, facts, "What's special", days/views/saves, Zillow-checked/updated, agent/MLS, 3D Home, floor plan, room media, travel times, payment estimate, Zestimate/Rent Zestimate, price/tax history, schools, neighborhood, nearby homes, climate link. Rentals add fees/deposit/lease/utilities/pets/apply/tours. Differentiators: Showcase, AI featured media/staging, AI Mode, Instant Tour Scheduling, owner/renter funnels.
- **Redfin:** dense tabbed page (Overview/Neighborhood/Details/Sale & tax/Climate), Street View, favorite/hide/share, checked/updated/source, tour dates, calculator, sale+tax history tables, public record, climate + weather/sun, Redfin Estimate + comps. Owner dashboard: verified owners edit facts, 20 owner photos on off-market pages, Owner Estimate; Rental Tools dashboard + TurboTenant.
- **Realtor.com:** estimated value, tabs, "Fly around", RealCost, similar estimates, nearby solds/rentals, lead forms; noise indicator + heat map; First Street + FEMA flood; DIY landlord via Avail (build, publish, syndicate to ~19–20 rental sites, add photos… [source truncated here]

---

## Implementation status vs this spec (nad-lan.co.il, added 2026-07-01, v1.69.74)

**Live already:** fact strip w/ IL fields (arnona/vaad/mamad/entry) · monthly costs (mortgage est + arnona + vaad) · days-on-market + views + favorite (FOMO) · WhatsApp + visit-scheduling lead CTAs · similar listings · real schools/kindergartens/transit/shops/health via OSM Overpass · live map w/ streets+satellite layers and POI markers · sketch facade w/ unit highlight + click-to-inspect interior plan (differentiator none of the leaders has) · "What's special" AI highlights · share + report-a-mistake + updated timestamp (trust) · RealEstateListing JSON-LD · media tabs (Kuula 3D/video/floorplan meta) · AVM/deals-table plumbing (needs ETL data) · free AI listing wizard (text→fields+highlights→review→real photo upload→pending) · demo listings noindexed.

**Open gaps (prioritized):** price/listing history UI (needs nadlan.gov.il ETL into the existing deals table) · commute/travel-times module · language versions + hreflang for listings · listing-from-photo (vision AI in wizard) · virtual tours ingestion UX (meta exists) · saved-search alerts surfacing · open-house scheduling · monetization tiers for listings (featured placement exists via paid_tier/is_sponsored; needs archive sort + upsell UI) · draw-on-map archive search · climate/risk (no IL data source yet) · Owner Estimate-style flow.
