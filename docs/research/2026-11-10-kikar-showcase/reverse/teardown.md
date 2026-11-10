# Teardown: unit-level features of the leading property and booking products

Built on 10.11.2026 for the single project / unit page https://nad-lan.co.il/projects/hamedina/ (release 1.72.630).

**What this file holds:** one section per product family, with what each does best at the unit level and the rows that carry its evidence. The ids point to `features.csv` in this folder; every row there carries the evidence URL, the quoted UI label, the evidence class and our status.

## Method

- **Evidence gathering:** three research passes on 10.11.2026, run in parallel:
  - US portals and builders
  - UK, Europe, Australia, Gulf and Israel
  - Booking platforms, 3D tours, maps and new-development configurators
- **Sources:** the passes used the built-in browser in their own tabs, plus WebFetch and WebSearch. Rows from the 9.11.2026 hub teardowns and the 2.10.2026 side-by-side in this repo were reused where they apply to a unit page, and carry their original date.
- **Merging:** 269 raw rows became 206 after near-duplicates were merged; adding 15 rows from the earlier teardowns gives 221 atomic features. 'more_evidence' keeps every merged source.
- **Evidence classes:**
  - live: opened and seen
  - help: official help centre or product page
  - press: official newsroom
  - search: snippet only
  - claimed: vendor marketing, not seen working
  - prior: known pattern, not re-read
- **Counts by class:** live 156, press 23, search 16, claimed 12, help 9, prior 5.
- **Our page:** every row was checked on our page on desktop (1024x768, the pane's size) and on a 375x812 phone (Android emulation), using DOM reads, visible labels and real taps. The CSV gives the exact check per row.

## Coverage of our page against the list

- **Rows:** 221 features from 49 products.
  - 66 present
  - 68 partial
  - 77 absent
  - 10 not applicable to this page
- **Coverage of the 211 applicable rows:**
  - 47.4%, counting present as 1 and partial as 0.5
  - 53.2% when each row is weighted by its buyer value (1-5)
- **High-value rows (buyer value 4 or 5, 56 rows):** 27 present, 17 partial, 12 absent.
- **What can and cannot be claimed:** this measures coverage against an enumerated, sourced list. It does not prove that no feature exists elsewhere; see `limits.md`.

| Area | Rows | Present | Partial | Absent | Not applicable |
|---|---|---|---|---|---|
| 3d-tour | 13 | 6 | 2 | 5 | 0 |
| media | 8 | 4 | 3 | 1 | 0 |
| plan | 12 | 1 | 8 | 3 | 0 |
| inventory | 20 | 5 | 10 | 5 | 0 |
| price-cost | 22 | 7 | 7 | 6 | 2 |
| finance | 15 | 1 | 5 | 8 | 1 |
| location-map | 11 | 4 | 3 | 4 | 0 |
| commute | 3 | 1 | 0 | 2 | 0 |
| schools | 3 | 0 | 1 | 1 | 1 |
| environment | 16 | 4 | 2 | 10 | 0 |
| building-amenities | 8 | 5 | 2 | 1 | 0 |
| contact-booking | 21 | 5 | 9 | 5 | 2 |
| video-call | 4 | 2 | 1 | 1 | 0 |
| decision-tools | 29 | 6 | 6 | 17 | 0 |
| trust | 21 | 10 | 7 | 3 | 1 |
| accessibility | 4 | 2 | 0 | 2 | 0 |
| language | 3 | 1 | 0 | 1 | 1 |
| mobile-pattern | 8 | 2 | 2 | 2 | 2 |

## Zillow

**Best at the unit level:** Media and money on one listing. SkyTour gives an aerial 3D view of the building; 3D Home pins every photo on an interactive plan with AI room sizes; Showcase groups photos by room; AI staging offers a style grid and a before/after slider. The money side has the Zestimate with Rent Zestimate, BuyAbility, 'Est. payment' with 'Get pre-qualified', and Offer Insights. A sticky Contact / Request a tour bar sits at the bottom. Zillow's listing and building pages returned 403 to the browser on 10.11, so these rows rest on Zillow's press releases, its help pages and the 9.11 DOM read.

- **Rows that name these products:** 32.
- **Our page on those rows:** 14 present, 11 partial, 6 absent, 1 not applicable.

| Id | Feature | Product | UI label (quoted) | Evidence | Class | Ours |
|---|---|---|---|---|---|---|
| F001 | 360 / 3D walkthrough of the unit, room by room | Zillow | 1 Virtual tour | https://www.zoopla.co.uk/new-homes/details/67344265/ | live | present |
| F004 | SkyTour drone-style 3D exterior fly-around | Zillow | SkyTour | https://s25.q4cdn.com/975009107/files/doc_news/Summer-just-got-hotter-Zillow-debuts-five-powerful-new-features-2025.pdf | press | present |
| F015 | Photo or 360 tour grouped by room | Zillow | Photo tour · Living room · Full kitchen | https://www.airbnb.com/rooms/17674545 | live | present |
| F017 | AI Virtual Staging with style picker | Zillow | Stage this space | https://s25.q4cdn.com/975009107/files/doc_news/Zillow-brings-AI-powered-Virtual-Staging-to-Showcase-listings-2025.pdf | press | present |
| F018 | Media chips on the hero (photos, video, 3D, plan, street view) | Zillow | Video Tour | https://www.compass.com/homedetails/211-W-84th-St-Unit-PHB-Manhattan-NY-10024/1830501369843106121_lid/ | live | partial |
| F021 | Before/after slider and re-roll on a staged photo | Zillow | slide between views | https://s25.q4cdn.com/975009107/files/doc_news/Zillow-brings-AI-powered-Virtual-Staging-to-Showcase-listings-2025.pdf | press | partial |
| F024 | Room dimensions and total area on the floor plan | Zillow | 1st Floor / 2nd Floor | https://www.lennar.com/new-homes/florida/miami/miami/greenview-at-presidential/presidential-collection/victoria/50907600311 | live | absent |
| F025 | Interactive floor plan that pins every photo to its spot | Zillow | Interactive floor plan | https://zillow.mediaroom.com/2022-08-08-Zillows-AI-powered-interactive-home-tours-are-now-available-nationwide | press | partial |
| F036 | Per-unit inventory table with status and price | Zillow | $4,273/sf Avg. | https://www.compass.com/building/the-henry-manhattan-ny/1633466331737096645/ | live | partial |
| F054 | Automated value estimate for the unit | Zillow | Wertermittlung als KäuferPlus Nutzer inklusive | https://www.immobilienscout24.de/expose/172498251 | live | present |
| F059 | Payment calculator split with HOA dues line | Zillow | HOA dues | https://www.redfin.com/FL/Miami/725-NE-24th-St-33137/unit-3301/home/190141269 | live | absent |
| F061 | Sale history with price per sqft on every event | Zillow | Sale History | https://www.redfin.com/FL/Miami/725-NE-24th-St-33137/unit-3301/home/190141269 | live | present |
| F073 | Total Monthly Price badge (rent plus required fees) | Zillow | Total Monthly Price | https://www.apartments.com/grow/news/all-in-pricing-expansion | search | n-a |
| F077 | Inline mortgage calculator with editable deposit, rate and term | Zillow | Down payment 20% ($740,000) | https://www.redfin.com/FL/Miami/725-NE-24th-St-33137/unit-3301/home/190141269 | live | partial |
| F078 | Monthly payment line next to the price | Zillow | See my rate | https://www.redfin.com/FL/Miami/725-NE-24th-St-33137/unit-3301/home/190141269 | live | absent |
| F080 | BuyAbility tag and payment on every listing | Zillow | BuyAbility payment | https://s25.q4cdn.com/975009107/files/doc_news/Summer-just-got-hotter-Zillow-debuts-five-powerful-new-features-2025.pdf | press | absent |
| F082 | Zillow Home Loans pre-qualify link beside the payment estimate | Zillow | Get pre-qualified | https://s25.q4cdn.com/975009107/files/doc_news/Zillow-brings-AI-powered-Virtual-Staging-to-Showcase-listings-2025.pdf | press | partial |
| F096 | Walk, bike and transit scores out of 10 | Zillow | Very walkable | https://www.redfin.com/FL/Miami/725-NE-24th-St-33137/unit-3301/home/190141269 | live | partial |
| F105 | Nearby and assigned schools with rating and distance | Zillow | Public PreK-5 • Assigned • 0.9mi | https://www.redfin.com/FL/Miami/725-NE-24th-St-33137/unit-3301/home/190141269 | live | partial |
| F128 | Facts and features grouped by category | Zillow | Facts & features | https://www.zillow.com/community/parten/448105195_zpid/ | live | present |
| F133 | Tour sheet that offers the earliest free slot as one tap | Zillow | Request a tour as early as today at 1:30 PM | https://www.compass.com/homedetails/211-W-84th-St-Unit-PHB-Manhattan-NY-10024/1830501369843106121_lid/ | live | partial |
| F145 | Same-day tour requests from about 3 hours ahead | Zillow | as little as 2.5–3 hours in advance | https://www.zillow.help/article/faq-take-a-tour-and-tour-connections-zd360019248553 | help | present |
| F146 | Add a tour, open house or inspection to the calendar | Zillow | Add to calendar | https://s25.q4cdn.com/975009107/files/doc_news/Summer-just-got-hotter-Zillow-debuts-five-powerful-new-features-2025.pdf | press | absent |
| F153 | Tour by live video with an agent | Zillow | Virtual visit | https://www.lennar.com/new-homes/florida/miami/miami/greenview-at-presidential | live | present |
| F166 | Offer Insights: offer-strength chips with acceptance likelihood | Zillow | Offer Insights | https://s25.q4cdn.com/975009107/files/doc_news/Summer-just-got-hotter-Zillow-debuts-five-powerful-new-features-2025.pdf | press | absent |
| F171 | Similar or alternative projects nearby | Zillow | Still looking? | https://www.booking.com/hotel/il/the-norman-tel-aviv-tel-aviv.en-gb.html | live | present |
| F186 | Local legal-protections module on the listing | Zillow | Local legal protections | https://www.zillow.com/community/parten/448105195_zpid/ | live | partial |
| F193 | Honest 'no estimate' message with sold-price range | Zillow | We cannot show automated home-value estimates | https://www.redfin.com/FL/Miami/725-NE-24th-St-33137/unit-3301/home/190141269 | live | present |
| F194 | Label on renders and virtually staged images | Zillow | Virtually staged | https://zillow.mediaroom.com/2025-09-10-Zillow-brings-AI-powered-Virtual-Staging-to-Showcase-listings | prior | present |
| F196 | Price history row with source and Report a problem | Zillow | Report a problem | https://www.zillow.com/community/parten/448105195_zpid/ | prior | partial |
| F197 | Source attribution line on listing data | Zillow | Provided by Zillow | https://www.redfin.com/TX/Austin/Easton-Park/community/36463 | live | present |
| F214 | Sticky bottom contact / tour bar | Zillow | Get in touch now for more information. · WhatsApp | https://www.propertyfinder.ae/en/new-projects/emaar-properties/valia-tower | live | present |

## Redfin

**Best at the unit level:** The strongest single listing for environment and running cost. Sunscore 0-100 comes with a shading note, direct-sun hours for June and December, and a full-screen 3D sun simulation. First Street flood, heat and wind factors come with 30-year odds, plus a noise score and walk / bike / transit scores. The payment calculator includes HOA, taxes and insurance, with an editable down payment. Tours book by day and half-hour chips, including 'Tour via Video Chat'. The estimate is built from named comparables, and when it cannot value a unit it says so. Opened live on 10.11 (Miami condo unit 3301).

- **Rows that name these products:** 31.
- **Our page on those rows:** 15 present, 6 partial, 10 absent, 0 not applicable.

| Id | Feature | Product | UI label (quoted) | Evidence | Class | Ours |
|---|---|---|---|---|---|---|
| F001 | 360 / 3D walkthrough of the unit, room by room | Redfin | 1 Virtual tour | https://www.zoopla.co.uk/new-homes/details/67344265/ | live | present |
| F018 | Media chips on the hero (photos, video, 3D, plan, street view) | Redfin | Video Tour | https://www.compass.com/homedetails/211-W-84th-St-Unit-PHB-Manhattan-NY-10024/1830501369843106121_lid/ | live | partial |
| F057 | Estimate built from named comparable sales with map | Redfin | View comparables on map | https://www.redfin.com/FL/Miami/725-NE-24th-St-33137/unit-3301/home/190141269 | live | present |
| F059 | Payment calculator split with HOA dues line | Redfin | HOA dues | https://www.redfin.com/FL/Miami/725-NE-24th-St-33137/unit-3301/home/190141269 | live | absent |
| F061 | Sale history with price per sqft on every event | Redfin | Sale History | https://www.redfin.com/FL/Miami/725-NE-24th-St-33137/unit-3301/home/190141269 | live | present |
| F075 | Utilities line the buyer can add | Redfin | Utilities Add | https://www.redfin.com/FL/Miami/725-NE-24th-St-33137/unit-3301/home/190141269 | live | absent |
| F077 | Inline mortgage calculator with editable deposit, rate and term | Redfin | Down payment 20% ($740,000) | https://www.redfin.com/FL/Miami/725-NE-24th-St-33137/unit-3301/home/190141269 | live | partial |
| F078 | Monthly payment line next to the price | Redfin | See my rate | https://www.redfin.com/FL/Miami/725-NE-24th-St-33137/unit-3301/home/190141269 | live | absent |
| F096 | Walk, bike and transit scores out of 10 | Redfin | Very walkable | https://www.redfin.com/FL/Miami/725-NE-24th-St-33137/unit-3301/home/190141269 | live | partial |
| F105 | Nearby and assigned schools with rating and distance | Redfin | Public PreK-5 • Assigned • 0.9mi | https://www.redfin.com/FL/Miami/725-NE-24th-St-33137/unit-3301/home/190141269 | live | partial |
| F108 | Direct-sun hours in June vs December | Redfin | 6.9 hrs June / 6.7 hrs December | https://www.redfin.com/FL/Miami/725-NE-24th-St-33137/unit-3301/home/190141269 | live | present |
| F109 | Sun and shade simulation by date and hour | Redfin | View 3D sun simulation | https://www.redfin.com/FL/Miami/725-NE-24th-St-33137/unit-3301/home/190141269 | live | present |
| F110 | Sunscore 0-100 with shading note | Redfin | Good sunlight | https://www.redfin.com/FL/Miami/725-NE-24th-St-33137/unit-3301/home/190141269 | live | present |
| F113 | Noise score for the address | Redfin | Silent zone | https://www.redfin.com/FL/Miami/725-NE-24th-St-33137/unit-3301/home/190141269 | live | absent |
| F117 | Flood Factor with 30-year probability | Redfin | 9/10 Flood Factor | https://www.redfin.com/FL/Miami/725-NE-24th-St-33137/unit-3301/home/190141269 | live | absent |
| F118 | Heat Factor with hot-day count | Redfin | 10/10 Heat Factor | https://www.redfin.com/FL/Miami/725-NE-24th-St-33137/unit-3301/home/190141269 | live | absent |
| F120 | Wind Factor (storm-wind chance) | Redfin | 10/10 Wind Factor | https://www.redfin.com/FL/Miami/725-NE-24th-St-33137/unit-3301/home/190141269 | live | absent |
| F128 | Facts and features grouped by category | Redfin | Facts & features | https://www.zillow.com/community/parten/448105195_zpid/ | live | present |
| F134 | Tour slot picker: 14 day chips and 30-minute time chips | Redfin | See this home in person | https://www.redfin.com/FL/Miami/725-NE-24th-St-33137/unit-3301/home/190141269 | live | present |
| F137 | Ask a local expert with preset question chips | Redfin | Any recent upgrades? | https://www.redfin.com/FL/Miami/725-NE-24th-St-33137/unit-3301/home/190141269 | live | partial |
| F153 | Tour by live video with an agent | Redfin | Virtual visit | https://www.lennar.com/new-homes/florida/miami/miami/greenview-at-presidential | live | present |
| F163 | Market insights: days on market, sale-to-list, price drops | Redfin | Market insights | https://www.redfin.com/FL/Miami/725-NE-24th-St-33137/unit-3301/home/190141269 | live | partial |
| F171 | Similar or alternative projects nearby | Redfin | Still looking? | https://www.booking.com/hotel/il/the-norman-tel-aviv-tel-aviv.en-gb.html | live | present |
| F181 | Start an offer from the listing | Redfin | Start an offer | https://www.redfin.com/FL/Miami/725-NE-24th-St-33137/unit-3301/home/190141269 | live | absent |
| F184 | Hot Home banner | Redfin | Hot Home | https://support.redfin.com/hc/en-us/articles/360016475851-Hot-Home | help | absent |
| F185 | Public views and saves counters | Redfin | 270 views • 11 favorites | https://www.redfin.com/TX/Austin/219-Lessin-Ln-78704/unit-6/home/187798317 | live | absent |
| F189 | Data freshness / last-updated stamp | Redfin | Redfin checked: 2 minutes ago | https://www.redfin.com/FL/Miami/725-NE-24th-St-33137/unit-3301/home/190141269 | live | present |
| F193 | Honest 'no estimate' message with sold-price range | Redfin | We cannot show automated home-value estimates | https://www.redfin.com/FL/Miami/725-NE-24th-St-33137/unit-3301/home/190141269 | live | present |
| F197 | Source attribution line on listing data | Redfin | Provided by Zillow | https://www.redfin.com/TX/Austin/Easton-Park/community/36463 | live | present |
| F204 | Advertise-here line for builders and agents on the buyer page | Redfin | Are you a builder? Learn how to advertise | https://www.redfin.com/TX/Austin/Easton-Park/community/36463 | live | present |
| F208 | Photo buttons with descriptive accessible names | Redfin | View photo 1: 219 Lessin Ln #6 | https://www.redfin.com/TX/Austin/219-Lessin-Ln-78704/unit-6/home/187798317 | live | present |

## Realtor.com

**Best at the unit level:** Risk and cost. Environmental risk covers flood, fire, heat, wind and air, with the change at 15 and 30 years, plus a noise heat map. Commute times are saved once and shown on every property. RealEstimate shows three providers. The RealCost monthly cost has a veterans toggle and a disclosure. Tour requests take up to three dates, and RealAssist AI answers questions. On 10.11 the site was refused by both the browser and fetch, so these rows rest on press, search and the 9.11 DOM read.

- **Rows that name these products:** 20.
- **Our page on those rows:** 7 present, 4 partial, 9 absent, 0 not applicable.

| Id | Feature | Product | UI label (quoted) | Evidence | Class | Ours |
|---|---|---|---|---|---|---|
| F020 | AI visualise the home at night, in winter or with a new exterior | Realtor.com | See properties at night, in winter | https://www.googlecloudpresscorner.com/2026-06-02-Realtor-com-R-Launches-RealAssist-TM-AI-A-Completely-Reimagined-Way-to-Find-A-Home | press | present |
| F034 | Expected move-in / handover date on the unit or project | Realtor.com | Quick Move-In 9/2027 | https://www.tollbrothers.com/luxury-homes-for-sale/New-York/Overlook-by-Toll-Brothers/Ridge-Collection | live | present |
| F059 | Payment calculator split with HOA dues line | Realtor.com | HOA dues | https://www.redfin.com/FL/Miami/725-NE-24th-St-33137/unit-3301/home/190141269 | live | absent |
| F069 | RealEstimate: three provider estimates | Realtor.com | RealEstimate | https://www.housingwire.com/articles/look-out-zestimate-realtor-com-rolling-out-its-own-souped-up-home-value-estimate/ | search | partial |
| F076 | Buyer-status toggle that changes the cost (residency, first home, veterans) | Realtor.com | Residency status · Non-resident | https://www.propertyfinder.ae/en/plp/buy/apartment-for-sale-dubai-dubai-marina-park-island-blakely-tower-165046716.html | live | present |
| F077 | Inline mortgage calculator with editable deposit, rate and term | Realtor.com | Down payment 20% ($740,000) | https://www.redfin.com/FL/Miami/725-NE-24th-St-33137/unit-3301/home/190141269 | live | partial |
| F102 | Travel time from the home to my own places | Realtor.com | __mins driving to your place | https://www.rightmove.co.uk/properties/92765910 | live | absent |
| F105 | Nearby and assigned schools with rating and distance | Realtor.com | Public PreK-5 • Assigned • 0.9mi | https://www.redfin.com/FL/Miami/725-NE-24th-St-33137/unit-3301/home/190141269 | live | partial |
| F113 | Noise score for the address | Realtor.com | Silent zone | https://www.redfin.com/FL/Miami/725-NE-24th-St-33137/unit-3301/home/190141269 | live | absent |
| F117 | Flood Factor with 30-year probability | Realtor.com | 9/10 Flood Factor | https://www.redfin.com/FL/Miami/725-NE-24th-St-33137/unit-3301/home/190141269 | live | absent |
| F118 | Heat Factor with hot-day count | Realtor.com | 10/10 Heat Factor | https://www.redfin.com/FL/Miami/725-NE-24th-St-33137/unit-3301/home/190141269 | live | absent |
| F119 | Noise indicator with heat-map overlay of sources | Realtor.com | noise indicator | https://www.rismedia.com/2020/03/09/its-oh-so-quiet-realtor-com-new-noise-indicator-enables-home-shoppers-to-understand-property-noise-level | search | absent |
| F120 | Wind Factor (storm-wind chance) | Realtor.com | 10/10 Wind Factor | https://www.redfin.com/FL/Miami/725-NE-24th-St-33137/unit-3301/home/190141269 | live | absent |
| F121 | Climate risk now vs 15 and 30 years out | Realtor.com | Air Factor | https://www.realestatenews.com/2024/03/13/realtor-com-listings-now-display-5-climate-risk-factors | search | absent |
| F134 | Tour slot picker: 14 day chips and 30-minute time chips | Realtor.com | See this home in person | https://www.redfin.com/FL/Miami/725-NE-24th-St-33137/unit-3301/home/190141269 | live | present |
| F136 | AI or chat assistant answering questions about this property | Realtor.com | Hello, I'm AI Concierge. | https://www.tollbrothers.com/luxury-homes-for-sale/New-York/The-Rockwell | live | absent |
| F149 | Tour request with up to 3 preferred dates | Realtor.com | you can provide up to 3 dates | https://www.realtor.com/community-detail/Central-Living-Urban-Quick-Move-in-Homes_9000-Waterford-Centre-Blvd_Austin_TX_78758_Q717000115806 | prior | partial |
| F190 | Disclosure of how the monthly cost or estimate is calculated | Realtor.com | RealCost™ Disclosure | https://www.realtor.com/community-detail/Central-Living-Urban-Quick-Move-in-Homes_9000-Waterford-Centre-Blvd_Austin_TX_78758_Q717000115806 | live | present |
| F191 | FAQ on the property page with FAQPage schema | Realtor.com | FAQs about The Norman Tel Aviv | https://www.booking.com/hotel/il/the-norman-tel-aviv-tel-aviv.en-gb.html | live | present |
| F197 | Source attribution line on listing data | Realtor.com | Provided by Zillow | https://www.redfin.com/TX/Austin/Easton-Park/community/36463 | live | present |

## Compass

**Best at the unit level:** The best tower page in the set. The building header gives units, stories and active sales. The unit table shows status, price and $/sf, with tabs for Active / Past Sales / Past Rentals and 'Filter by unit or tier/line'. Past sales show the original price and % change, marked 'Verified by Public Record'. There is a floor-plan directory, building policies (minimum down payment) and common charges with '+ other costs'. Collections are shared boards with the agent. Opened live on 10.11.

- **Rows that name these products:** 19.
- **Our page on those rows:** 5 present, 10 partial, 4 absent, 0 not applicable.

| Id | Feature | Product | UI label (quoted) | Evidence | Class | Ours |
|---|---|---|---|---|---|---|
| F001 | 360 / 3D walkthrough of the unit, room by room | Compass | 1 Virtual tour | https://www.zoopla.co.uk/new-homes/details/67344265/ | live | present |
| F018 | Media chips on the hero (photos, video, 3D, plan, street view) | Compass | Video Tour | https://www.compass.com/homedetails/211-W-84th-St-Unit-PHB-Manhattan-NY-10024/1830501369843106121_lid/ | live | partial |
| F023 | Floor-plan directory for every unit or floor in the building | Compass | Floor Plan Directory | https://www.compass.com/building/the-henry-manhattan-ny/1633466331737096645/floorplans/ | live | absent |
| F036 | Per-unit inventory table with status and price | Compass | $4,273/sf Avg. | https://www.compass.com/building/the-henry-manhattan-ny/1633466331737096645/ | live | partial |
| F038 | Active / Past Sales / Past Rentals tabs | Compass | Past Rentals | https://www.compass.com/building/the-henry-manhattan-ny/1633466331737096645/ | live | partial |
| F045 | Filter units by tier or line | Compass | Filter by unit or tier/line | https://www.compass.com/building/the-henry-manhattan-ny/1633466331737096645/ | live | partial |
| F058 | Monthly service / common charges as a field | Compass | + other costs | https://www.compass.com/homedetails/211-W-84th-St-Unit-PHB-Manhattan-NY-10024/1830501369843106121_lid/ | live | partial |
| F061 | Sale history with price per sqft on every event | Compass | Sale History | https://www.redfin.com/FL/Miami/725-NE-24th-St-33137/unit-3301/home/190141269 | live | present |
| F065 | Past sales with original price, % change and public-record check | Compass | Verified by Public Record | https://www.compass.com/building/the-henry-manhattan-ny/1633466331737096645/ | live | partial |
| F078 | Monthly payment line next to the price | Compass | See my rate | https://www.redfin.com/FL/Miami/725-NE-24th-St-33137/unit-3301/home/190141269 | live | absent |
| F083 | Building financial policies (minimum down payment) | Compass | Min Down Payment: 25% | https://www.compass.com/building/the-henry-manhattan-ny/1633466331737096645/ | live | partial |
| F105 | Nearby and assigned schools with rating and distance | Compass | Public PreK-5 • Assigned • 0.9mi | https://www.redfin.com/FL/Miami/725-NE-24th-St-33137/unit-3301/home/190141269 | live | partial |
| F124 | Building summary header (buildings, floors, units) | Compass | 46 Units, 18 Stories | https://www.compass.com/building/the-henry-manhattan-ny/1633466331737096645/ | live | present |
| F133 | Tour sheet that offers the earliest free slot as one tap | Compass | Request a tour as early as today at 1:30 PM | https://www.compass.com/homedetails/211-W-84th-St-Unit-PHB-Manhattan-NY-10024/1830501369843106121_lid/ | live | partial |
| F134 | Tour slot picker: 14 day chips and 30-minute time chips | Compass | See this home in person | https://www.redfin.com/FL/Miami/725-NE-24th-St-33137/unit-3301/home/190141269 | live | present |
| F143 | Register interest on an off-plan project | Compass | Express your interest in this project · Register Interest | https://www.bayut.com/for-sale/property/dubai/business-bay/binghatti-skyhall/ | live | partial |
| F144 | Sales office and Email all Agents | Compass | Email all Agents | https://www.compass.com/building/the-henry-manhattan-ny/1633466331737096645/ | live | absent |
| F170 | Shared list with partner or agent (collaborative board) | Compass | anyone with a wishlist link can view the wishlist | https://www.airbnb.com/help/article/1236 | help | absent |
| F188 | Building facts: architect, developer, contractor | Compass | Building Facts | https://www.compass.com/building/the-henry-manhattan-ny/1633466331737096645/ | live | present |

## US rentals and portals (Homes.com, Apartments.com, Trulia)

**Best at the unit level:** Homes.com has produced neighbourhood video tours, school cards that lead to nearby homes, and a crime score. Apartments.com has a pricing and floor-plans table filtered by floor and move-in date, a per-unit rent estimate, a 'Total Monthly Price' badge, and 3D tour and video buttons on the photo. Trulia has 'What Locals Say'. All three blocked the browser on 10.11, so these rows rest on search snippets and help pages.

- **Rows that name these products:** 17.
- **Our page on those rows:** 2 present, 5 partial, 6 absent, 4 not applicable.

| Id | Feature | Product | UI label (quoted) | Evidence | Class | Ours |
|---|---|---|---|---|---|---|
| F001 | 360 / 3D walkthrough of the unit, room by room | Apartments.com | 1 Virtual tour | https://www.zoopla.co.uk/new-homes/details/67344265/ | live | present |
| F018 | Media chips on the hero (photos, video, 3D, plan, street view) | Apartments.com | Video Tour | https://www.compass.com/homedetails/211-W-84th-St-Unit-PHB-Manhattan-NY-10024/1830501369843106121_lid/ | live | partial |
| F036 | Per-unit inventory table with status and price | Apartments.com | $4,273/sf Avg. | https://www.compass.com/building/the-henry-manhattan-ny/1633466331737096645/ | live | partial |
| F048 | Pricing & Floor Plans with floor selector and move-in filter | Apartments.com | Pricing & Floor Plans | https://www.apartments.com/wyatt-sterling-va/392b10e | search | partial |
| F059 | Payment calculator split with HOA dues line | Homes.com | HOA dues | https://www.redfin.com/FL/Miami/725-NE-24th-St-33137/unit-3301/home/190141269 | live | absent |
| F073 | Total Monthly Price badge (rent plus required fees) | Apartments.com | Total Monthly Price | https://www.apartments.com/grow/news/all-in-pricing-expansion | search | n-a |
| F074 | Per-unit rent estimate calculator (lease term, move-in date, add-ons) | Apartments.com | Estimate Rental Cost | https://renterhelp.apartments.com/article/1176-how-do-i-estimate-rental-costs-for-a-specific-unit | help | n-a |
| F096 | Walk, bike and transit scores out of 10 | Homes.com | Very walkable | https://www.redfin.com/FL/Miami/725-NE-24th-St-33137/unit-3301/home/190141269 | live | partial |
| F097 | Crime score for the listing area | Homes.com | Crime Score | https://www.homes.com/local-guide/kingstowne-va/ | search | absent |
| F100 | What Locals Say neighborhood polls | Trulia | What Locals Say | https://www.trulia.com/blog/what-locals-say | search | absent |
| F102 | Travel time from the home to my own places | Apartments.com | __mins driving to your place | https://www.rightmove.co.uk/properties/92765910 | live | absent |
| F105 | Nearby and assigned schools with rating and distance | Homes.com | Public PreK-5 • Assigned • 0.9mi | https://www.redfin.com/FL/Miami/725-NE-24th-St-33137/unit-3301/home/190141269 | live | partial |
| F107 | School cards that link to homes near each school | Homes.com | Listing Features | https://www.homes.com/support/?p=120 | search | n-a |
| F113 | Noise score for the address | Homes.com | Silent zone | https://www.redfin.com/FL/Miami/725-NE-24th-St-33137/unit-3301/home/190141269 | live | absent |
| F117 | Flood Factor with 30-year probability | Homes.com | 9/10 Flood Factor | https://www.redfin.com/FL/Miami/725-NE-24th-St-33137/unit-3301/home/190141269 | live | absent |
| F150 | Apply Now with a reusable application | Apartments.com | Apply Now | https://renterhelp.apartments.com/article/136-how-to-apply-to-rentals-on-apartmentscom | search | n-a |
| F155 | Neighborhood video tours and narratives | Homes.com | video tours | https://homes.com/solutions/neighborhoods-schools | search | present |

## US builders (Lennar, Toll Brothers, KB Home, NewHomeSource)

**Best at the unit level:** Plans and inventory. Plans come with level tabs and room dimensions, an 'Everything's included' spec, a homesite map with status layers, a compare tool with a live count, in-person or virtual visits on a date strip, and a print flyer. Toll Brothers adds a residence table per condo tower with a plan link, a video for each residence line with its floor range ('Residence E, Floors 3-9'), a named on-site sales team with 'Get Directions', the offering-plan file number, an AI Concierge and personalisation options. Lennar and Toll were opened live; KB Home and NewHomeSource were blocked.

- **Rows that name these products:** 24.
- **Our page on those rows:** 5 present, 10 partial, 9 absent, 0 not applicable.

| Id | Feature | Product | UI label (quoted) | Evidence | Class | Ours |
|---|---|---|---|---|---|---|
| F001 | 360 / 3D walkthrough of the unit, room by room | Lennar | 1 Virtual tour | https://www.zoopla.co.uk/new-homes/details/67344265/ | live | present |
| F018 | Media chips on the hero (photos, video, 3D, plan, street view) | Lennar | Video Tour | https://www.compass.com/homedetails/211-W-84th-St-Unit-PHB-Manhattan-NY-10024/1830501369843106121_lid/ | live | partial |
| F019 | Video per residence line with floor range | Toll Brothers | Residence E, Floors 3-9 | https://www.tollbrothers.com/luxury-homes-for-sale/New-York/The-Rockwell | live | partial |
| F024 | Room dimensions and total area on the floor plan | Lennar | 1st Floor / 2nd Floor | https://www.lennar.com/new-homes/florida/miami/miami/greenview-at-presidential/presidential-collection/victoria/50907600311 | live | absent |
| F029 | Finish or upgrade packages with their price | Toll Brothers | See Personalization Options | https://www.tollbrothers.com/luxury-homes-for-sale/New-York/Overlook-by-Toll-Brothers/Ridge-Collection/Colgate | live | partial |
| F033 | Interactive floor plan with structural options | KB Home | interactive floor plan feature | https://www.kbhome.com/how-do-online-tools-make-homebuying-easier | search | absent |
| F034 | Expected move-in / handover date on the unit or project | Toll Brothers | Quick Move-In 9/2027 | https://www.tollbrothers.com/luxury-homes-for-sale/New-York/Overlook-by-Toll-Brothers/Ridge-Collection | live | present |
| F036 | Per-unit inventory table with status and price | Toll Brothers | $4,273/sf Avg. | https://www.compass.com/building/the-henry-manhattan-ny/1633466331737096645/ | live | partial |
| F051 | Site or building map coloured by availability | Lennar | Move-in ready | https://www.lennar.com/new-homes/florida/miami/miami/greenview-at-presidential | live | absent |
| F078 | Monthly payment line next to the price | Lennar | See my rate | https://www.redfin.com/FL/Miami/725-NE-24th-St-33137/unit-3301/home/190141269 | live | absent |
| F079 | Builder-mortgage payment estimate and buying-power calculator | Lennar | Est. payment $24,367/mo* | https://www.lennar.com/new-homes/florida/miami/miami/greenview-at-presidential/presidential-collection/victoria/50907600311 | live | partial |
| F089 | Limited-time rate badge on the project header | Toll Brothers | 5.49% (5.76% APR)†30-Year Fixed | https://www.tollbrothers.com/luxury-homes-for-sale/New-York/The-Rockwell | live | absent |
| F099 | One-tap directions to the site or sales centre | Toll Brothers | Get Directions | https://www.tollbrothers.com/luxury-homes-for-sale/New-York/Overlook-by-Toll-Brothers/Ridge-Collection/Colgate | live | absent |
| F125 | Specification / included features grouped by room | Lennar | Everything’s included with this home | https://www.lennar.com/new-homes/florida/miami/miami/greenview-at-presidential/presidential-collection/victoria/50907600311 | live | partial |
| F134 | Tour slot picker: 14 day chips and 30-minute time chips | Lennar | See this home in person | https://www.redfin.com/FL/Miami/725-NE-24th-St-33137/unit-3301/home/190141269 | live | present |
| F136 | AI or chat assistant answering questions about this property | Toll Brothers | Hello, I'm AI Concierge. | https://www.tollbrothers.com/luxury-homes-for-sale/New-York/The-Rockwell | live | absent |
| F137 | Ask a local expert with preset question chips | NewHomeSource | Any recent upgrades? | https://www.redfin.com/FL/Miami/725-NE-24th-St-33137/unit-3301/home/190141269 | live | partial |
| F140 | Named on-site sales rep, sales hours and directions | Lennar | Onsite Sales Team | https://www.tollbrothers.com/luxury-homes-for-sale/New-York/The-Rockwell | live | partial |
| F147 | Preferred contact method in the lead form | NewHomeSource | Preferred Contact Method | https://www.newhomesource.com/community/tx/liberty-hill/santa-rita-ranch-90ft-lots-by-highland-homes/147878 | live | partial |
| F153 | Tour by live video with an agent | Lennar | Virtual visit | https://www.lennar.com/new-homes/florida/miami/miami/greenview-at-presidential | live | present |
| F159 | Compare units side by side | Lennar | 10 homes available | https://www.lennar.com/new-homes/florida/miami/miami/greenview-at-presidential | live | absent |
| F171 | Similar or alternative projects nearby | NewHomeSource | Still looking? | https://www.booking.com/hotel/il/the-norman-tel-aviv-tel-aviv.en-gb.html | live | present |
| F179 | Printable flyer or brochure PDF | Lennar | Print flyer | https://www.lennar.com/new-homes/florida/miami/miami/greenview-at-presidential/presidential-collection/victoria/50907600311 | live | absent |
| F195 | Permit, licence or offering-plan numbers shown | Toll Brothers | File No. CD22-0088 | https://www.tollbrothers.com/luxury-homes-for-sale/New-York/The-Rockwell | live | partial |

## UK (Rightmove, Zoopla, OnTheMarket)

**Best at the unit level:** Material information sits in the summary: EPC, broadband speed, mobile signal (OnTheMarket), service charge, tenure and ground-rent review dates. The map has Stations and Schools tabs and 'My places' drive times. Other features: a dated 'Reduced on' chip, an affordability calculator, 'Ask Rightmove' AI and 'Summarise property details', shared lists, a lender check (Nationwide) and media counters. Rightmove and Zoopla listings were opened live; Zoopla's risk values need sign-in.

- **Rows that name these products:** 29.
- **Our page on those rows:** 8 present, 9 partial, 12 absent, 0 not applicable.

| Id | Feature | Product | UI label (quoted) | Evidence | Class | Ours |
|---|---|---|---|---|---|---|
| F001 | 360 / 3D walkthrough of the unit, room by room | Rightmove | 1 Virtual tour | https://www.zoopla.co.uk/new-homes/details/67344265/ | live | present |
| F018 | Media chips on the hero (photos, video, 3D, plan, street view) | Rightmove | Video Tour | https://www.compass.com/homedetails/211-W-84th-St-Unit-PHB-Manhattan-NY-10024/1830501369843106121_lid/ | live | partial |
| F022 | Floor plan image on the listing | Rightmove | PM_Apt81_Floorplan B | https://www.rightmove.co.uk/properties/94044159 | live | partial |
| F054 | Automated value estimate for the unit | Zoopla | Wertermittlung als KäuferPlus Nutzer inklusive | https://www.immobilienscout24.de/expose/172498251 | live | present |
| F058 | Monthly service / common charges as a field | Rightmove | + other costs | https://www.compass.com/homedetails/211-W-84th-St-Unit-PHB-Manhattan-NY-10024/1830501369843106121_lid/ | live | partial |
| F060 | Price per m² or sq ft next to the price | Zoopla | Kaufpreis 9.829 €/m² · Kalkuliert von ImmoScout24 | https://www.immobilienscout24.de/expose/172498251 | live | present |
| F070 | Dated price reduction or strike-through with stated basis | Rightmove | Reduced on 11/02/2026 | https://www.zoopla.co.uk/new-homes/details/67344265/ | live | absent |
| F071 | Lease length, ground rent and next ground-rent review | Rightmove | Ground rent date of next review | https://www.zoopla.co.uk/new-homes/details/74544885/ | live | partial |
| F077 | Inline mortgage calculator with editable deposit, rate and term | Rightmove | Down payment 20% ($740,000) | https://www.redfin.com/FL/Miami/725-NE-24th-St-33137/unit-3301/home/190141269 | live | partial |
| F078 | Monthly payment line next to the price | Zoopla | See my rate | https://www.redfin.com/FL/Miami/725-NE-24th-St-33137/unit-3301/home/190141269 | live | absent |
| F085 | Lender check: will a bank lend on this property | Rightmove | property lending check | https://www.rightmove.co.uk/press-centre/?p=4243 | press | absent |
| F092 | Stations and Schools tabs on the location map | Rightmove | My places · Stations · Schools | https://www.rightmove.co.uk/properties/92765910 | live | present |
| F102 | Travel time from the home to my own places | Rightmove | __mins driving to your place | https://www.rightmove.co.uk/properties/92765910 | live | absent |
| F105 | Nearby and assigned schools with rating and distance | Rightmove | Public PreK-5 • Assigned • 0.9mi | https://www.redfin.com/FL/Miami/725-NE-24th-St-33137/unit-3301/home/190141269 | live | partial |
| F106 | School catchment zone on the listing | Rightmove | school catchment zone information on all Domain listings | https://help.domain.com.au/hc/en-us/articles/360033742314-Search-for-properties-by-school-zone | search | absent |
| F112 | Flood risk, crime and planning applications after sign-in | Zoopla | Planning applications · Crime rates · Flood risk | https://www.zoopla.co.uk/new-homes/details/74544885/ | live | partial |
| F115 | Broadband / internet availability for the address | Rightmove | Internet · Verfügbarkeit prüfen | https://www.immobilienscout24.de/expose/172498251 | live | absent |
| F116 | Energy certificate / rating | Rightmove | EPC Rating: B | https://www.zoopla.co.uk/new-homes/details/67344265/ | live | absent |
| F122 | Mobile signal by network | OnTheMarket | Mobile signal | https://expert.onthemarket.com/help-centre/key-information/ | help | absent |
| F126 | Amenity and feature chips with 'show all' | Rightmove | מה יש בנכס · מעלית · ממ"ד | https://www.yad2.co.il/realestate/item/tel-aviv-area/3evliq9j | live | present |
| F136 | AI or chat assistant answering questions about this property | Rightmove | Hello, I'm AI Concierge. | https://www.tollbrothers.com/luxury-homes-for-sale/New-York/The-Rockwell | live | absent |
| F138 | Call, request details and email buttons | Rightmove | Request details · Email agent · Call agent | https://www.rightmove.co.uk/properties/94044159 | live | partial |
| F170 | Shared list with partner or agent (collaborative board) | Rightmove | anyone with a wishlist link can view the wishlist | https://www.airbnb.com/help/article/1236 | help | absent |
| F175 | Listing summary / highlights at the top | Rightmove | Summarise property details | https://www.rightmove.co.uk/properties/92765910 | live | present |
| F179 | Printable flyer or brochure PDF | Rightmove | Print flyer | https://www.lennar.com/new-homes/florida/miami/miami/greenview-at-presidential/presidential-collection/victoria/50907600311 | live | absent |
| F189 | Data freshness / last-updated stamp | Rightmove | Redfin checked: 2 minutes ago | https://www.redfin.com/FL/Miami/725-NE-24th-St-33137/unit-3301/home/190141269 | live | present |
| F192 | Fraud and security notice for buyers | Rightmove | Staying secure when looking for a property | https://www.rightmove.co.uk/new-homes-for-sale/London.html | live | partial |
| F194 | Label on renders and virtually staged images | Rightmove | Virtually staged | https://zillow.mediaroom.com/2025-09-10-Zillow-brings-AI-powered-Virtual-Staging-to-Showcase-listings | prior | present |
| F207 | Accessibility features of the home | Rightmove | ACCESSIBILITY · 2nd floor,Lift access | https://www.rightmove.co.uk/properties/92765910 | live | absent |

## Australia (Domain, realestate.com.au)

**Best at the unit level:** Inspections. Inspection times have add-to-calendar, and an inspection planner holds display-suite hours. Other features: 'My Commutes', school catchment zones, online video inspection and 3D tours linked to plans (iGUIDE). Both sites blocked the browser on 10.11 (403 / 429), so these rows rest on press and search.

- **Rows that name these products:** 10.
- **Our page on those rows:** 4 present, 1 partial, 5 absent, 0 not applicable.

| Id | Feature | Product | UI label (quoted) | Evidence | Class | Ours |
|---|---|---|---|---|---|---|
| F001 | 360 / 3D walkthrough of the unit, room by room | realestate.com.au | 1 Virtual tour | https://www.zoopla.co.uk/new-homes/details/67344265/ | live | present |
| F008 | Interactive 3D tour linked to the floor plan | realestate.com.au | iGUIDE interactive property tours | https://itbrief.com.au/story/realestate-com-au-launches-ai-property-search-suite | press | partial |
| F054 | Automated value estimate for the unit | Domain | Wertermittlung als KäuferPlus Nutzer inklusive | https://www.immobilienscout24.de/expose/172498251 | live | present |
| F102 | Travel time from the home to my own places | Domain | __mins driving to your place | https://www.rightmove.co.uk/properties/92765910 | live | absent |
| F106 | School catchment zone on the listing | Domain | school catchment zone information on all Domain listings | https://help.domain.com.au/hc/en-us/articles/360033742314-Search-for-properties-by-school-zone | search | absent |
| F136 | AI or chat assistant answering questions about this property | realestate.com.au | Hello, I'm AI Concierge. | https://www.tollbrothers.com/luxury-homes-for-sale/New-York/The-Rockwell | live | absent |
| F146 | Add a tour, open house or inspection to the calendar | Domain | Add to calendar | https://s25.q4cdn.com/975009107/files/doc_news/Summer-just-got-hotter-Zillow-debuts-five-powerful-new-features-2025.pdf | press | absent |
| F152 | Inspection planner with display-suite hours | Domain | Add to Plan | https://customer.realestate.com.au/news/developer/get-the-edge/ | press | absent |
| F153 | Tour by live video with an agent | Domain | Virtual visit | https://www.lennar.com/new-homes/florida/miami/miami/greenview-at-presidential | live | present |
| F194 | Label on renders and virtually staged images | Domain | Virtually staged | https://zillow.mediaroom.com/2025-09-10-Zillow-brings-AI-powered-Virtual-Staging-to-Showcase-listings | prior | present |

## Europe (Idealista, ImmoScout24, SeLoger Neuf)

**Best at the unit level:** Idealista: video visits ('vídeovisita'), energy-certificate values and the spec PDF. ImmoScout24: the total purchase cost with tax and fees itemised, parking priced separately, a portal-computed price per m², an internet check, 'Etage 4 von 6' and sibling units. SeLoger Neuf comes closest to a tower unit list: each lot shows floor, exposure (orientation), balcony m², parking and 'Demander le plan', plus '48 sur 50 lots encore disponibles' and the developer's other programmes. ImmoScout24 and SeLoger were opened live; Idealista was blocked.

- **Rows that name these products:** 26.
- **Our page on those rows:** 11 present, 7 partial, 8 absent, 0 not applicable.

| Id | Feature | Product | UI label (quoted) | Evidence | Class | Ours |
|---|---|---|---|---|---|---|
| F001 | 360 / 3D walkthrough of the unit, room by room | Idealista | 1 Virtual tour | https://www.zoopla.co.uk/new-homes/details/67344265/ | live | present |
| F022 | Floor plan image on the listing | Idealista | PM_Apt81_Floorplan B | https://www.rightmove.co.uk/properties/94044159 | live | partial |
| F026 | Request the plan of a specific unit | SeLoger Neuf | Demander le plan | https://www.selogerneuf.com/annonces/neuf/programme/massy-91/193966643/ | live | present |
| F034 | Expected move-in / handover date on the unit or project | Idealista | Quick Move-In 9/2027 | https://www.tollbrothers.com/luxury-homes-for-sale/New-York/Overlook-by-Toll-Brothers/Ridge-Collection | live | present |
| F041 | Live count of units still available | Idealista | 48 sur 50 lots encore disponibles | https://www.selogerneuf.com/annonces/neuf/programme/massy-91/193966643/ | live | partial |
| F042 | Per-unit row with floor, orientation, balcony and parking | SeLoger Neuf | 6e étage · Exposition Sud · Balcon 3.09m² | https://www.selogerneuf.com/annonces/neuf/programme/massy-91/193966643/ | live | partial |
| F047 | Other units in the same project | Idealista | Weitere Einheiten | https://www.immobilienscout24.de/expose/172498251 | live | partial |
| F054 | Automated value estimate for the unit | ImmoScout24 | Wertermittlung als KäuferPlus Nutzer inklusive | https://www.immobilienscout24.de/expose/172498251 | live | present |
| F055 | Total purchase cost with taxes and fees itemised | ImmoScout24 | 971.892 € Gesamtkosten · 71.992 € Nebenkosten | https://www.immobilienscout24.de/expose/172498251 | live | partial |
| F056 | 'From' / starting price per unit type | SeLoger Neuf | החל מ- 4,550,000 ₪ | https://www.yad2.co.il/yad1/project/13671 | live | present |
| F060 | Price per m² or sq ft next to the price | ImmoScout24 | Kaufpreis 9.829 €/m² · Kalkuliert von ImmoScout24 | https://www.immobilienscout24.de/expose/172498251 | live | present |
| F064 | Parking space priced separately | ImmoScout24 | Garage/ Stellplatz-Kaufpreis 38.900 € | https://www.immobilienscout24.de/expose/172498251 | live | partial |
| F078 | Monthly payment line next to the price | ImmoScout24 | See my rate | https://www.redfin.com/FL/Miami/725-NE-24th-St-33137/unit-3301/home/190141269 | live | absent |
| F084 | Default interest rate tied to a named public source | ImmoScout24 | ריבית ממוצעת % 4.97 | https://www.yad2.co.il/realestate/item/tel-aviv-area/3evliq9j | live | absent |
| F115 | Broadband / internet availability for the address | ImmoScout24 | Internet · Verfügbarkeit prüfen | https://www.immobilienscout24.de/expose/172498251 | live | absent |
| F116 | Energy certificate / rating | Idealista | EPC Rating: B | https://www.zoopla.co.uk/new-homes/details/67344265/ | live | absent |
| F125 | Specification / included features grouped by room | Idealista | Everything’s included with this home | https://www.lennar.com/new-homes/florida/miami/miami/greenview-at-presidential/presidential-collection/victoria/50907600311 | live | partial |
| F126 | Amenity and feature chips with 'show all' | ImmoScout24 | מה יש בנכס · מעלית · ממ"ד | https://www.yad2.co.il/realestate/item/tel-aviv-area/3evliq9j | live | present |
| F129 | Floor number out of total floors | ImmoScout24 | Etage 4 von 6 | https://www.immobilienscout24.de/expose/172498251 | live | present |
| F136 | AI or chat assistant answering questions about this property | ImmoScout24 | Hello, I'm AI Concierge. | https://www.tollbrothers.com/luxury-homes-for-sale/New-York/The-Rockwell | live | absent |
| F153 | Tour by live video with an agent | Idealista | Virtual visit | https://www.lennar.com/new-homes/florida/miami/miami/greenview-at-presidential | live | present |
| F179 | Printable flyer or brochure PDF | Idealista | Print flyer | https://www.lennar.com/new-homes/florida/miami/miami/greenview-at-presidential/presidential-collection/victoria/50907600311 | live | absent |
| F185 | Public views and saves counters | Idealista | 270 views • 11 favorites | https://www.redfin.com/TX/Austin/219-Lessin-Ln-78704/unit-6/home/187798317 | live | absent |
| F189 | Data freshness / last-updated stamp | SeLoger Neuf | Redfin checked: 2 minutes ago | https://www.redfin.com/FL/Miami/725-NE-24th-St-33137/unit-3301/home/190141269 | live | present |
| F199 | Developer profile and other projects | SeLoger Neuf | Autres programmes du même promoteur | https://www.selogerneuf.com/annonces/neuf/programme/massy-91/193966643/ | live | present |
| F207 | Accessibility features of the home | ImmoScout24 | ACCESSIBILITY · 2nd floor,Lift access | https://www.rightmove.co.uk/properties/92765910 | live | absent |

## Gulf (Bayut, Property Finder, Emaar)

**Best at the unit level:** The portals closest to what a tower buyer needs:
- Transactions in the same building by bedroom count (sale and rent).
- A price trend for the building against the community, and nearby towers ranked by price per sq ft.
- The off-plan payment plan with milestones and the handover quarter, and '31% Completed'.
- Building information (floors, elevators, parking).
- Plans of other units in the same tower by floor, and 3D plans.
- TruCheck verification with its date, 'Validated Information' from the land registry, and RERA and permit numbers.
- Residency status in the mortgage calculator.
- A sticky WhatsApp bar.

Emaar adds 'Instant Call' and a live 'Available · 16 units'. Bayut and Property Finder were opened live; Bayut on a phone width returned an empty page.

- **Rows that name these products:** 43.
- **Our page on those rows:** 18 present, 15 partial, 10 absent, 0 not applicable.

| Id | Feature | Product | UI label (quoted) | Evidence | Class | Ours |
|---|---|---|---|---|---|---|
| F002 | 3D floor plan per unit type | Bayut | 3D Live · Unit A07 FLOOR 12 | https://www.bayut.com/property/details-17137392.html | live | absent |
| F022 | Floor plan image on the listing | Property Finder | PM_Apt81_Floorplan B | https://www.rightmove.co.uk/properties/94044159 | live | partial |
| F023 | Floor-plan directory for every unit or floor in the building | Bayut | Floor Plan Directory | https://www.compass.com/building/the-henry-manhattan-ny/1633466331737096645/floorplans/ | live | absent |
| F026 | Request the plan of a specific unit | Bayut | Demander le plan | https://www.selogerneuf.com/annonces/neuf/programme/massy-91/193966643/ | live | present |
| F027 | Unit-type table with size, price and plan column | Bayut | TYPE · AREA (SQFT) · PRICE (AED) · FLOOR PLAN | https://www.bayut.com/for-sale/property/dubai/business-bay/binghatti-skyhall/ | live | partial |
| F034 | Expected move-in / handover date on the unit or project | Bayut | Quick Move-In 9/2027 | https://www.tollbrothers.com/luxury-homes-for-sale/New-York/Overlook-by-Toll-Brothers/Ridge-Collection | live | present |
| F041 | Live count of units still available | Emaar | 48 sur 50 lots encore disponibles | https://www.selogerneuf.com/annonces/neuf/programme/massy-91/193966643/ | live | partial |
| F044 | Construction progress percent | Bayut | Under Construction · 31% Completed | https://www.bayut.com/for-sale/property/dubai/business-bay/binghatti-skyhall/ | live | partial |
| F049 | Project timeline / permit-stage tracker with dates | Property Finder | Construction Started · Expected Completion | https://www.propertyfinder.ae/en/new-projects/emaar-properties/valia-tower | live | present |
| F050 | Resale vs initial-sale units inside an off-plan project | Bayut | Off-Plan / Resale · Initial Sale | https://www.bayut.com/for-sale/property/dubai/business-bay/binghatti-skyhall/ | live | present |
| F054 | Automated value estimate for the unit | Bayut | Wertermittlung als KäuferPlus Nutzer inklusive | https://www.immobilienscout24.de/expose/172498251 | live | present |
| F055 | Total purchase cost with taxes and fees itemised | Property Finder | 971.892 € Gesamtkosten · 71.992 € Nebenkosten | https://www.immobilienscout24.de/expose/172498251 | live | partial |
| F056 | 'From' / starting price per unit type | Bayut | החל מ- 4,550,000 ₪ | https://www.yad2.co.il/yad1/project/13671 | live | present |
| F058 | Monthly service / common charges as a field | Bayut | + other costs | https://www.compass.com/homedetails/211-W-84th-St-Unit-PHB-Manhattan-NY-10024/1830501369843106121_lid/ | live | partial |
| F060 | Price per m² or sq ft next to the price | Property Finder | Kaufpreis 9.829 €/m² · Kalkuliert von ImmoScout24 | https://www.immobilienscout24.de/expose/172498251 | live | present |
| F063 | Average yearly rent for this unit | Bayut | Average Rent AED 156,213 Yearly | https://www.bayut.com/property/details-17137392.html | live | absent |
| F076 | Buyer-status toggle that changes the cost (residency, first home, veterans) | Property Finder | Residency status · Non-resident | https://www.propertyfinder.ae/en/plp/buy/apartment-for-sale-dubai-dubai-marina-park-island-blakely-tower-165046716.html | live | present |
| F077 | Inline mortgage calculator with editable deposit, rate and term | Bayut | Down payment 20% ($740,000) | https://www.redfin.com/FL/Miami/725-NE-24th-St-33137/unit-3301/home/190141269 | live | partial |
| F078 | Monthly payment line next to the price | Property Finder | See my rate | https://www.redfin.com/FL/Miami/725-NE-24th-St-33137/unit-3301/home/190141269 | live | absent |
| F086 | Off-plan payment plan ratio in the header | Bayut | Payment Plan 70 / 30 · View complete plan | https://www.bayut.com/for-sale/property/dubai/business-bay/binghatti-skyhall/ | live | absent |
| F088 | Payment plan split into milestones | Bayut | MILESTONE · % OF PROPERTY VALUE TO BE PAID | https://www.bayut.com/for-sale/property/dubai/business-bay/binghatti-skyhall/ | live | absent |
| F124 | Building summary header (buildings, floors, units) | Property Finder | 46 Units, 18 Stories | https://www.compass.com/building/the-henry-manhattan-ny/1633466331737096645/ | live | present |
| F126 | Amenity and feature chips with 'show all' | Bayut | מה יש בנכס · מעלית · ממ"ד | https://www.yad2.co.il/realestate/item/tel-aviv-area/3evliq9j | live | present |
| F127 | Building facts block (year, floors, lifts, parking) | Bayut | Floors 85 · Elevators 12 · Parking Spaces 703 | https://www.bayut.com/property/details-17137392.html | live | present |
| F131 | Resident reviews and star rating of the building | Property Finder | 4.2 · 14 Reviews · Review this building | https://www.propertyfinder.ae/en/plp/buy/apartment-for-sale-dubai-dubai-marina-park-island-blakely-tower-165046716.html | live | absent |
| F135 | WhatsApp contact button | Bayut | Whatsapp | https://www.yad2.co.il/realestate/item/tel-aviv-area/3evliq9j | live | present |
| F143 | Register interest on an off-plan project | Bayut | Express your interest in this project · Register Interest | https://www.bayut.com/for-sale/property/dubai/business-bay/binghatti-skyhall/ | live | partial |
| F148 | Public Q&A or 'ask the developer' after the FAQ | Property Finder | לא מצאת את התשובה לשאלה שלך? שאל את היזם | https://www.yad2.co.il/yad1/project/15696 | live | partial |
| F154 | Instant call with sales from the project page | Emaar | Instant Call | https://www.emaar.com/en/properties/creek-bay-at-dubai-creek-harbour | live | absent |
| F158 | Asking price vs area average | Bayut | This property costs 20% more than the average | https://www.propertyfinder.ae/en/plp/buy/apartment-for-sale-dubai-dubai-marina-park-island-blakely-tower-165046716.html | live | present |
| F160 | Deals in the same building, by rooms, in-project vs nearby | Bayut | Similar Property Transactions · 2 Bedroom Apartments in DAMAC Heights | https://www.bayut.com/property/details-17137392.html | live | partial |
| F164 | Nearby towers ranked by price per sq ft and 3-month change | Bayut | Popular locations · Avg. price/sqft · 3M Change | https://www.bayut.com/property/details-17137392.html | live | present |
| F167 | Price trend chart: building vs community | Bayut | Prices & trends · 1Y · 2Y · 5Y | https://www.propertyfinder.ae/en/plp/buy/apartment-for-sale-dubai-dubai-marina-park-island-blakely-tower-165046716.html | live | partial |
| F179 | Printable flyer or brochure PDF | Property Finder | Print flyer | https://www.lennar.com/new-homes/florida/miami/miami/greenview-at-presidential/presidential-collection/victoria/50907600311 | live | absent |
| F189 | Data freshness / last-updated stamp | Bayut | Redfin checked: 2 minutes ago | https://www.redfin.com/FL/Miami/725-NE-24th-St-33137/unit-3301/home/190141269 | live | present |
| F195 | Permit, licence or offering-plan numbers shown | Bayut | File No. CD22-0088 | https://www.tollbrothers.com/luxury-homes-for-sale/New-York/The-Rockwell | live | partial |
| F199 | Developer profile and other projects | Property Finder | Autres programmes du même promoteur | https://www.selogerneuf.com/annonces/neuf/programme/massy-91/193966643/ | live | present |
| F202 | Registry-validated fields block | Bayut | Validated Information | https://www.bayut.com/property/details-17137392.html | live | partial |
| F203 | Verified-listing badge with validation date | Bayut | Checked · TruCheck | https://www.bayut.com/property/details-17137392.html | live | partial |
| F211 | Language (and currency) switch | Property Finder | عربي | https://www.propertyfinder.ae/en/new-projects/emaar-properties/valia-tower | live | present |
| F212 | Agent's spoken language shown | Property Finder | English · 5.0 · 4 Ratings | https://www.propertyfinder.ae/en/plp/buy/apartment-for-sale-dubai-dubai-marina-park-island-blakely-tower-165046716.html | live | absent |
| F214 | Sticky bottom contact / tour bar | Property Finder | Get in touch now for more information. · WhatsApp | https://www.propertyfinder.ae/en/new-projects/emaar-properties/valia-tower | live | present |
| F218 | Section anchor tabs | Bayut | Overview · Floor Plans · Mortgage · Trends & Indices | https://www.bayut.com/property/details-17137392.html | live | partial |

## Israel (Yad2 / Yad1, Madlan, nadlan.gov.il, Gindi)

**Best at the unit level:** The local baseline.
- **Yad1:** 'החל מ' per unit type, the spec grouped by room, a permit-stage tracker, sold-nearby with an honest empty state, and WhatsApp.
- **Madlan:** deals in the project against nearby with filters, yield, building sites nearby with their expected end, the architect and contractor named, and 20/80 payment terms.
- **nadlan.gov.il:** official deals at the address with gush / helka and the change since the previous sale, official rents, the neighbourhood median by rooms against city and country, area alerts and the Tabu extract.
- **Gindi:** a named agent with hours and six channels (read 2.10).

Yad1, Madlan project pages and nadlan.gov.il were opened live; Madlan resale listings showed a robot puzzle.

- **Rows that name these products:** 33.
- **Our page on those rows:** 15 present, 13 partial, 5 absent, 0 not applicable.

| Id | Feature | Product | UI label (quoted) | Evidence | Class | Ours |
|---|---|---|---|---|---|---|
| F027 | Unit-type table with size, price and plan column | Yad2 / Yad1 | TYPE · AREA (SQFT) · PRICE (AED) · FLOOR PLAN | https://www.bayut.com/for-sale/property/dubai/business-bay/binghatti-skyhall/ | live | partial |
| F034 | Expected move-in / handover date on the unit or project | Yad2 / Yad1 | Quick Move-In 9/2027 | https://www.tollbrothers.com/luxury-homes-for-sale/New-York/Overlook-by-Toll-Brothers/Ridge-Collection | live | present |
| F049 | Project timeline / permit-stage tracker with dates | Yad2 / Yad1 | Construction Started · Expected Completion | https://www.propertyfinder.ae/en/new-projects/emaar-properties/valia-tower | live | present |
| F056 | 'From' / starting price per unit type | Yad2 / Yad1 | החל מ- 4,550,000 ₪ | https://www.yad2.co.il/yad1/project/13671 | live | present |
| F060 | Price per m² or sq ft next to the price | Yad2 / Yad1 | Kaufpreis 9.829 €/m² · Kalkuliert von ImmoScout24 | https://www.immobilienscout24.de/expose/172498251 | live | present |
| F077 | Inline mortgage calculator with editable deposit, rate and term | Yad2 / Yad1 | Down payment 20% ($740,000) | https://www.redfin.com/FL/Miami/725-NE-24th-St-33137/unit-3301/home/190141269 | live | partial |
| F078 | Monthly payment line next to the price | Yad2 / Yad1 | See my rate | https://www.redfin.com/FL/Miami/725-NE-24th-St-33137/unit-3301/home/190141269 | live | absent |
| F081 | Developer payment terms and bank guarantee in project updates | Yad2 / Yad1 | פריסייל - תנאי תשלום 20/80 פטור מדד | https://www.madlan.co.il/projects/%D7%9E%D7%92%D7%A8%D7%A9_9_%D7%A4%D7%90%D7%A8%D7%A7_%D7%94%D7%97%D7%95%D7%A8%D7%A9%D7%95%D7%AA_%D7%AA%D7%9C_%D7%90%D7%91%D7%99%D7%91 | live | partial |
| F084 | Default interest rate tied to a named public source | Yad2 / Yad1 | ריבית ממוצעת % 4.97 | https://www.yad2.co.il/realestate/item/tel-aviv-area/3evliq9j | live | absent |
| F091 | Nearby places by category with walking minutes | Yad2 / Yad1 | מיקומים בקרבת הפרויקט · תחבורה · פארקים | https://www.yad2.co.il/yad1/project/13671 | live | present |
| F111 | Construction sites nearby with expected end date | Madlan | 1 אתרי בניה בסביבה · צפי סיום: סוף 2028 | https://www.madlan.co.il/projects/%D7%9E%D7%92%D7%A8%D7%A9_9_%D7%A4%D7%90%D7%A8%D7%A7_%D7%94%D7%97%D7%95%D7%A8%D7%A9%D7%95%D7%AA_%D7%AA%D7%9C_%D7%90%D7%91%D7%99%D7%91 | live | partial |
| F124 | Building summary header (buildings, floors, units) | Madlan | 46 Units, 18 Stories | https://www.compass.com/building/the-henry-manhattan-ny/1633466331737096645/ | live | present |
| F125 | Specification / included features grouped by room | Yad2 / Yad1 | Everything’s included with this home | https://www.lennar.com/new-homes/florida/miami/miami/greenview-at-presidential/presidential-collection/victoria/50907600311 | live | partial |
| F126 | Amenity and feature chips with 'show all' | Yad2 / Yad1 | מה יש בנכס · מעלית · ממ"ד | https://www.yad2.co.il/realestate/item/tel-aviv-area/3evliq9j | live | present |
| F129 | Floor number out of total floors | Yad2 / Yad1 | Etage 4 von 6 | https://www.immobilienscout24.de/expose/172498251 | live | present |
| F130 | Safe-room badge | Yad2 / Yad1 | נכס עם ממ״ד | https://www.yad2.co.il/realestate/item/tel-aviv-area/3evliq9j | live | partial |
| F135 | WhatsApp contact button | Yad2 / Yad1 | Whatsapp | https://www.yad2.co.il/realestate/item/tel-aviv-area/3evliq9j | live | present |
| F141 | Named sales agent with hours and six contact channels in one panel | Gindi (developer, Israel) | video chat ('בקרוב') | https://gindi.com/online/ | live | partial |
| F148 | Public Q&A or 'ask the developer' after the FAQ | Yad2 / Yad1 | לא מצאת את התשובה לשאלה שלך? שאל את היזם | https://www.yad2.co.il/yad1/project/15696 | live | partial |
| F160 | Deals in the same building, by rooms, in-project vs nearby | Madlan | Similar Property Transactions · 2 Bedroom Apartments in DAMAC Heights | https://www.bayut.com/property/details-17137392.html | live | partial |
| F162 | Area alerts for new deals or a new project | nadlan.gov.il | עסקאות חדשות לידי? יש פרויקט חדש בשכונה? | https://www.nadlan.gov.il/?view=address&id=53775079&page=deals | live | present |
| F165 | Neighbourhood median by rooms vs city vs country per quarter | nadlan.gov.il | מחיר חציוני המשתלה · מחיר ארצי | https://www.nadlan.gov.il/?view=address&id=53775079&page=deals | live | present |
| F172 | Sold-nearby table with filters and an honest empty state | Yad2 / Yad1 | נכסים שנמכרו באזור · אין נכסים שנמכרו באזור | https://www.yad2.co.il/realestate/item/tel-aviv-area/3evliq9j | live | partial |
| F174 | Gross rental yield | Madlan | תשואה・2.93% | https://www.madlan.co.il/projects/%D7%9E%D7%92%D7%A8%D7%A9_9_%D7%A4%D7%90%D7%A8%D7%A7_%D7%94%D7%97%D7%95%D7%A8%D7%A9%D7%95%D7%AA_%D7%AA%D7%9C_%D7%90%D7%91%D7%99%D7%91 | live | absent |
| F177 | Official deals at the address with block/parcel and repeat-sale change | nadlan.gov.il | גוש/חלקה/תת-חלקה · מגמת שינוי | https://www.nadlan.gov.il/?view=address&id=53775079&page=deals | live | partial |
| F178 | Official rent data next to sales | nadlan.gov.il | עסקאות מכירה · שכירות · מה בסביבה | https://www.nadlan.gov.il/?view=address&id=53775079&page=deals | live | absent |
| F188 | Building facts: architect, developer, contractor | Madlan | Building Facts | https://www.compass.com/building/the-henry-manhattan-ny/1633466331737096645/ | live | present |
| F189 | Data freshness / last-updated stamp | Yad2 / Yad1 | Redfin checked: 2 minutes ago | https://www.redfin.com/FL/Miami/725-NE-24th-St-33137/unit-3301/home/190141269 | live | present |
| F195 | Permit, licence or offering-plan numbers shown | Yad2 / Yad1 | File No. CD22-0088 | https://www.tollbrothers.com/luxury-homes-for-sale/New-York/The-Rockwell | live | partial |
| F199 | Developer profile and other projects | Yad2 / Yad1 | Autres programmes du même promoteur | https://www.selogerneuf.com/annonces/neuf/programme/massy-91/193966643/ | live | present |
| F201 | Order the official land-registry extract | nadlan.gov.il | הפקת נסח טאבו | https://www.nadlan.gov.il/?view=address&id=53775079&page=deals | live | partial |
| F207 | Accessibility features of the home | Yad2 / Yad1 | ACCESSIBILITY · 2nd floor,Lift access | https://www.rightmove.co.uk/properties/92765910 | live | absent |
| F209 | Site accessibility toolbar | nadlan.gov.il | ניגודיות גבוהה · פונט קריא · חסימת אנימציה | https://www.nadlan.gov.il/ | live | present |

## Booking and rentals (Booking.com, Airbnb, Expedia / Hotels.com, Vrbo)

**Best at the unit level:** The decision UX we do not have yet.
- **Price:** the total is the headline, with a price-details popover; a struck price states its basis, with a '60-day average' insight.
- **Sticky bars:** a bottom reserve bar with price, dates and the button; a basket bar on Booking; the free-cancellation date sits beside the button.
- **Listing content:** a photo tour by room, 'Where you'll sleep', category review scores and AI highlights with a disclosure, and public Q&A.
- **Saving and sharing:** a share sheet with WhatsApp, wishlists with notes and collaborators, and a compare toggle.
- **Location:** nearby places with walking minutes.

Airbnb and Booking were opened live at 375 px; the Expedia and Vrbo property pages were bot-walled.

- **Rows that name these products:** 45.
- **Our page on those rows:** 13 present, 8 partial, 19 absent, 5 not applicable.

| Id | Feature | Product | UI label (quoted) | Evidence | Class | Ours |
|---|---|---|---|---|---|---|
| F015 | Photo or 360 tour grouped by room | Airbnb | Photo tour · Living room · Full kitchen | https://www.airbnb.com/rooms/17674545 | live | present |
| F031 | 'Where you'll sleep' bedroom cards | Airbnb | Where you'll sleep · Bedroom 1 | https://www.airbnb.com/rooms/17674545 | live | partial |
| F043 | Unit-type table with area, view and bed per row | Booking.com | 27 m² · City view | https://www.booking.com/hotel/il/the-norman-tel-aviv-tel-aviv.en-gb.html | live | partial |
| F052 | True-inventory scarcity per unit type | Booking.com | We have 1 left | https://www.booking.com/hotel/il/the-norman-tel-aviv-tel-aviv.en-gb.html | live | absent |
| F053 | 'Rare find' availability note | Airbnb | This place is usually booked | https://community.withairbnb.com/t5/Community-cafe/Rare-find/td-p/226351 | search | absent |
| F062 | Total price for the whole stay as the headline price | Booking.com | ₪2,476 total | https://www.airbnb.com/rooms/17674545 | live | partial |
| F066 | Price details popover: nights x rate | Airbnb | Price details · 3 nights x ₪825.33 | https://www.airbnb.com/rooms/17674545 | live | present |
| F067 | Price tracking alerts | Expedia / Hotels.com | Price Tracking | https://www.businesswire.com/news/home/20250213557700/en | search | absent |
| F068 | Price-versus-comparables badge on result card | Expedia / Hotels.com | Lower than similar properties | https://www.expedia.com/Hotel-Search?destination=Tel%20Aviv%2C%20Israel | live | present |
| F070 | Dated price reduction or strike-through with stated basis | Airbnb | Reduced on 11/02/2026 | https://www.zoopla.co.uk/new-homes/details/67344265/ | live | absent |
| F072 | Price-history insight badge ('below the 60-day average') | Airbnb | Your price is below the 60-day average | https://www.airbnb.com/rooms/17674545 | live | absent |
| F090 | Reserve with nothing due today / pay later | Airbnb | ₪0 today · Free cancellation | https://www.airbnb.com/rooms/17674545 | live | n-a |
| F091 | Nearby places by category with walking minutes | Booking.com | מיקומים בקרבת הפרויקט · תחבורה · פארקים | https://www.yad2.co.il/yad1/project/13671 | live | present |
| F095 | Neighbourhood map block with description | Booking.com | Where you'll be · Show fullscreen map | https://www.airbnb.com/rooms/17674545 | live | present |
| F098 | Map and list stay in sync (pin raises card) | Booking.com | Show map | https://www.airbnb.com/s/Tel-Aviv--Israel/homes | prior | partial |
| F103 | Walk time to the key amenity on the result card | Vrbo | 2 min walk to the beach | https://www.vrbo.com/search?destination=Miami%20Beach%2C%20Florida | live | present |
| F126 | Amenity and feature chips with 'show all' | Booking.com | מה יש בנכס · מעלית · ממ"ד | https://www.yad2.co.il/realestate/item/tel-aviv-area/3evliq9j | live | present |
| F136 | AI or chat assistant answering questions about this property | Expedia / Hotels.com | Hello, I'm AI Concierge. | https://www.tollbrothers.com/luxury-homes-for-sale/New-York/The-Rockwell | live | absent |
| F137 | Ask a local expert with preset question chips | Booking.com | Any recent upgrades? | https://www.redfin.com/FL/Miami/725-NE-24th-St-33137/unit-3301/home/190141269 | live | partial |
| F139 | Message the host from the unit page | Airbnb | Message host | https://www.airbnb.com/rooms/17674545 | live | present |
| F148 | Public Q&A or 'ask the developer' after the FAQ | Booking.com | לא מצאת את התשובה לשאלה שלך? שאל את היזם | https://www.yad2.co.il/yad1/project/15696 | live | partial |
| F151 | Inline availability calendar on the unit page | Booking.com | Clear dates | https://www.airbnb.com/rooms/17674545 | live | n-a |
| F159 | Compare units side by side | Vrbo | 10 homes available | https://www.lennar.com/new-homes/florida/miami/miami/greenview-at-presidential | live | absent |
| F161 | Share sheet with copy link and messaging apps | Airbnb | Share this place · Copy Link · WhatsApp · Embed | https://www.airbnb.com/rooms/17674545 | live | absent |
| F168 | Save to wishlist (heart) | Airbnb | Save to wishlist | https://www.airbnb.com/rooms/17674545 | live | partial |
| F170 | Shared list with partner or agent (collaborative board) | Airbnb | anyone with a wishlist link can view the wishlist | https://www.airbnb.com/help/article/1236 | help | absent |
| F171 | Similar or alternative projects nearby | Booking.com | Still looking? | https://www.booking.com/hotel/il/the-norman-tel-aviv-tel-aviv.en-gb.html | live | present |
| F173 | AI side-by-side compare of shortlisted properties | Expedia / Hotels.com | AI Compare | https://www.hospitalitynet.org/news/4135182.html | press | absent |
| F175 | Listing summary / highlights at the top | Airbnb | Summarise property details | https://www.rightmove.co.uk/properties/92765910 | live | present |
| F176 | Notes on saved listings | Airbnb | can add and view notes | https://www.airbnb.com/help/article/1236 | help | absent |
| F183 | Feedback on the page itself | Booking.com | How are we doing? | https://www.booking.com/hotel/il/the-norman-tel-aviv-tel-aviv.en-gb.html | live | absent |
| F187 | 'Things to know': check-in, house rules, safety | Booking.com | Things to know · House rules · Safety & property | https://www.airbnb.com/rooms/17674545 | live | present |
| F191 | FAQ on the property page with FAQPage schema | Booking.com | FAQs about The Norman Tel Aviv | https://www.booking.com/hotel/il/the-norman-tel-aviv-tel-aviv.en-gb.html | live | present |
| F198 | Category review scores | Booking.com | Rated 4.9 out of 5 stars for location | https://www.airbnb.com/rooms/17674545 | live | absent |
| F200 | Host response rate and response time | Airbnb | Response rate: 100% · Responds within an hour | https://www.airbnb.com/rooms/17674545 | live | absent |
| F205 | Free-cancellation deadline beside the CTA | Booking.com | Free cancellation before December 5 | https://www.airbnb.com/rooms/17674545 | live | n-a |
| F206 | Guest favourite badge (top-rated, reliable homes) | Airbnb | Guest Favorites | https://news.airbnb.com/airbnb-2023-winter-release-highlights | press | absent |
| F207 | Accessibility features of the home | Airbnb | ACCESSIBILITY · 2nd floor,Lift access | https://www.rightmove.co.uk/properties/92765910 | live | absent |
| F210 | Verified accessibility with photos and 3D scan | Airbnb | Accessibility Review | https://news.airbnb.com/accessibility-review | search | absent |
| F211 | Language (and currency) switch | Booking.com | عربي | https://www.propertyfinder.ae/en/new-projects/emaar-properties/valia-tower | live | present |
| F213 | Per-review 'Show translation' toggle | Booking.com | Show translation | https://www.booking.com/hotel/il/the-norman-tel-aviv-tel-aviv.en-gb.html | live | n-a |
| F215 | Sticky bottom reserve bar on mobile | Airbnb | total · Dec 10 – 13 · Reserve | https://www.airbnb.com/rooms/17674545 | live | partial |
| F216 | Sticky selection basket bar on mobile | Booking.com | Finish your booking! 0 rooms for | https://www.booking.com/hotel/il/the-norman-tel-aviv-tel-aviv.en-gb.html | live | absent |
| F217 | Swipe hero gallery with photo counter | Booking.com | 1 / 20 | https://www.airbnb.com/rooms/17674545 | live | absent |
| F220 | Map toggle button over the result list | Airbnb | Map | https://www.vrbo.com/search?destination=Miami%20Beach%2C%20Florida | live | n-a |

## Matterport

**Best at the unit level:** The full kit for a scanned home: dollhouse, floor-plan view, walk-through, a measurement tool, guided tour, a link to an exact viewpoint, tags with media, Defurnish, VR and Property Intelligence room sizes. All of it needs a built, scanned unit, so it cannot cover an off-plan tower. A demo was opened live; Defurnish, VR and Property Intelligence come from Matterport's own blog and docs.

- **Rows that name these products:** 13.
- **Our page on those rows:** 4 present, 3 partial, 6 absent, 0 not applicable.

| Id | Feature | Product | UI label (quoted) | Evidence | Class | Ours |
|---|---|---|---|---|---|---|
| F005 | Defurnish: empty-room view by default | Matterport | present the Matterport 3D tour to visitors fully unfurnished | https://matterport.com/blog/matterports-winter-2025-release-productivity-multiplied | press | absent |
| F006 | Dollhouse view (whole unit in 3D) | Matterport | View Dollhouse | https://my.matterport.com/show/?m=SxQL3iGyoDo | live | absent |
| F007 | Guided tour / highlight reel playback | Matterport | Play · Previous · Next | https://my.matterport.com/show/?m=SxQL3iGyoDo | live | present |
| F009 | Measurement tool in the 3D tour | Matterport | Measurements | https://my.matterport.com/show/?m=SxQL3iGyoDo | live | absent |
| F010 | Tags: hotspots with media in the tour | Matterport | Tags (successor to Mattertags) | https://matterport.github.io/developer-docs/reference/tag/ | help | present |
| F011 | Walk-through mode inside the scan | Matterport | Explore 3D Space | https://my.matterport.com/show/?m=SxQL3iGyoDo | live | partial |
| F012 | Room labels and floor picking in dollhouse | Matterport | Labels in Dollhouse view | https://matterport.com/blog/dollhouse-view-just-got-upgrade | press | present |
| F013 | VR mode in the headset browser | Matterport | Enter VR | https://matterport.com/blog/introducing-new-vr-mode | press | absent |
| F024 | Room dimensions and total area on the floor plan | Matterport | 1st Floor / 2nd Floor | https://www.lennar.com/new-homes/florida/miami/miami/greenview-at-presidential/presidential-collection/victoria/50907600311 | live | absent |
| F030 | Floor plan view from the 3D tour | Matterport | View Floor Plan | https://my.matterport.com/show/?m=SxQL3iGyoDo | live | partial |
| F032 | Schematic floor plan with furniture on/off and languages | Matterport | add or remove furniture | https://matterport.com/news/matterport-launches-property-intelligence-transforming-real-estate | press | partial |
| F169 | Share a link to the exact viewpoint | Matterport | Link to this location | https://my.matterport.com/show/?m=SxQL3iGyoDo | live | absent |
| F219 | Touch gesture hint and bottom toolbar | Matterport | Touch and drag with two fingers to pan | https://my.matterport.com/show/?m=SxQL3iGyoDo | live | present |

## Maps (Google Immersive View, Street View / Earth, Apple Maps)

**Best at the unit level:** Immersive View has a time-of-day and weather slider over a 3D city, a flyover of the building and route previews. Street View has 'See more dates'. Google Earth has a sunlight slider, and Apple Maps has Look Around. Sources are Google's blog and help pages and an Apple search snippet; none of these was opened live as a map.

- **Rows that name these products:** 8.
- **Our page on those rows:** 3 present, 1 partial, 4 absent, 0 not applicable.

| Id | Feature | Product | UI label (quoted) | Evidence | Class | Ours |
|---|---|---|---|---|---|---|
| F093 | Fly over a building to see entrances | Google Maps Immersive View | virtually soar over the building | https://blog.google/products/maps/sustainable-immersive-maps-announcements/ | press | present |
| F094 | Look Around: 360 street-level 3D walk | Apple Maps | Look Around | https://support.apple.com/guide/iphone/iph65703a702/ios | search | partial |
| F099 | One-tap directions to the site or sales centre | Apple Maps | Get Directions | https://www.tollbrothers.com/luxury-homes-for-sale/New-York/Overlook-by-Toll-Brothers/Ridge-Collection/Colgate | live | absent |
| F101 | Street-level imagery by date ('See more dates') | Google Street View / Earth | See more dates | https://developers.google.com/maps/documentation/earth/historical-street-view | help | absent |
| F104 | Route preview with traffic and air-quality by time | Google Maps Immersive View | Immersive View for routes | https://blog.google/products/maps/google-maps-october-2023-update/ | press | absent |
| F109 | Sun and shade simulation by date and hour | Google Street View / Earth | View 3D sun simulation | https://www.redfin.com/FL/Miami/725-NE-24th-St-33137/unit-3301/home/190141269 | live | present |
| F114 | Time-of-day slider in a 3D city model | Google Maps Immersive View | With the time slider | https://blog.google/products/maps/sustainable-immersive-maps-announcements/ | press | present |
| F123 | Weather preview in the 3D view | Google Maps Immersive View | and what the weather will be like | https://blog.google/products/maps/sustainable-immersive-maps-announcements/ | press | absent |

## 3D sales configurators and new-development sites

**Best at the unit level:** The only group that matches our 3D picker. Claimed features:
- The building in a 3D city; pick building, then floor, then apartment.
- Live availability colours synced to the CRM.
- The view from the exact balcony, and the sun path.
- Finish packages that change the price, and comparison with the next unit.
- A link per apartment, a personal buyer link or QR with engagement tracking, and a request into the CRM.
- A sales-gallery touch-table mode.

Other sites:
- **Waldorf Miami:** shows 'SELECT THE CUBE' (floor bands) and, on 2.10, a real view from the top with a day / night switch.
- **Una:** names units by direction.
- **St Modwen:** takes a £150 online pre-reservation.
- **Houzz:** prices real products into an estimate.

Almost all configurator rows are vendor claims, because their live demos did not render in the pane.

- **Rows that name these products:** 24.
- **Our page on those rows:** 8 present, 4 partial, 11 absent, 1 not applicable.

| Id | Feature | Product | UI label (quoted) | Evidence | Class | Ours |
|---|---|---|---|---|---|---|
| F001 | 360 / 3D walkthrough of the unit, room by room | Waldorf Astoria Residences Miami | 1 Virtual tour | https://www.zoopla.co.uk/new-homes/details/67344265/ | live | present |
| F002 | 3D floor plan per unit type | BMBY 3D | 3D Live · Unit A07 FLOOR 12 | https://www.bayut.com/property/details-17137392.html | live | absent |
| F003 | Building in a 3D model of the real city | REALS (Simplex 3D) | Present properties within their 3D urban environment | https://www.simplex3d.com/reals/ | claimed | present |
| F014 | Simulated view from the exact unit and height | REALS (Simplex 3D) | Future views & pre-construction | https://www.simplex3d.com/reals/ | claimed | present |
| F016 | Real photographed view from the top with day/night toggle | Waldorf Astoria Residences Miami | VIEW FROM THE TOP | https://www.waldorfresidencesmiami.com/view/ | prior | absent |
| F028 | Units named by direction with a PDF plan per unit | Una Residences Miami | Upper North East Residence 4201 | https://www.unaresidencesmiami.com/ | live | partial |
| F029 | Finish or upgrade packages with their price | Maverick Frame selector | See Personalization Options | https://www.tollbrothers.com/luxury-homes-for-sale/New-York/Overlook-by-Toll-Brothers/Ridge-Collection/Colgate | live | partial |
| F035 | Live unit availability synced to stock, with plans and 360 | REALS (Simplex 3D) | real-time availability, rich attributes, floor plans | https://www.simplex3d.com/reals/ | claimed | absent |
| F037 | Pick building, then floor, then apartment in 3D | BMBY 3D | לעבור בין הבניינים, הקומות והדירות | https://bmby.co.il/bmby-3d-%D7%A1%D7%91%D7%99%D7%91%D7%94-%D7%9E%D7%A9%D7%9C%D7%99%D7%9E%D7%94-%D7%9C%D7%9E%D7%A2%D7%A8%D7%9B%D7%AA | claimed | present |
| F039 | Availability colours on the floor plate | Maverick Frame selector | coloured by status: available, reserved or sold | https://maverickframe.com/services/interactive-apartment-selector/ | claimed | absent |
| F040 | Floor-band picker on the tower ('SELECT THE CUBE') | Waldorf Astoria Residences Miami | SELECT THE CUBE · PREVIOUS · NEXT | https://www.waldorfresidencesmiami.com/floor-plans/ | live | present |
| F046 | Floor hover shows free units and starting price | Maverick Frame selector | Hover a floor to see how many apartments are free | https://maverickframe.com/services/interactive-apartment-selector/ | claimed | partial |
| F087 | Online pre-reservation of a specific home with a small fee | St Modwen Homes | Pre-reserve this home now | https://www.stmodwenhomes.co.uk/why-buy-with-us/online-reservations | help | absent |
| F088 | Payment plan split into milestones | Sobha | MILESTONE · % OF PROPERTY VALUE TO BE PAID | https://www.bayut.com/for-sale/property/dubai/business-bay/binghatti-skyhall/ | live | absent |
| F091 | Nearby places by category with walking minutes | REALS (Simplex 3D) | מיקומים בקרבת הפרויקט · תחבורה · פארקים | https://www.yad2.co.il/yad1/project/13671 | live | present |
| F109 | Sun and shade simulation by date and hour | REALS (Simplex 3D) | View 3D sun simulation | https://www.redfin.com/FL/Miami/725-NE-24th-St-33137/unit-3301/home/190141269 | live | present |
| F132 | Reservation request for the exact apartment into CRM | Maverick Frame selector | Every request carries the apartment, the finishes and the price | https://maverickframe.com/services/interactive-apartment-selector/ | claimed | present |
| F142 | Personal buyer link or QR code | REALS (Simplex 3D) | via reel link or QR code scan | https://www.simplex3d.com/reals/ | claimed | absent |
| F156 | Video call with a shared live tour and joint measuring | Floorfy | Video calls | https://floorfy.com/products/videocall | claimed | partial |
| F157 | Deep link per apartment | Maverick Frame selector | Every apartment has its own link | https://maverickframe.com/services/interactive-apartment-selector/ | claimed | absent |
| F159 | Compare units side by side | Maverick Frame selector | 10 homes available | https://www.lennar.com/new-homes/florida/miami/miami/greenview-at-presidential | live | absent |
| F180 | Real priced products and AR placement in your own room | Houzz | View in My Room 3D | https://pro.houzz.com/for-pros/feature-3d-floor-plan | press | absent |
| F182 | Buyer engagement tracking (views, time, shares) | REALS (Simplex 3D) | Buyer: Views, time spent, shares | https://www.simplex3d.com/reals/ | claimed | absent |
| F221 | Sales-gallery touch screen / touch-table mode | Maverick Frame selector | Sales gallery screen | https://maverickframe.com/services/interactive-apartment-selector/ | claimed | n-a |
