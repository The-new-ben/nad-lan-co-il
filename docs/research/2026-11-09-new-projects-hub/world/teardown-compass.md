# Teardown: Compass (development hub, Private Exclusives, Coming Soon)

Read on 9.11.2026. Read-only, no sign-in.

**Evidence classes**
- **[code]:** read live in the owner's Chrome with a DOM script.
- **[fetch]:** the page text pulled with WebFetch.
- **[prior]:** a known pattern from before this session, not re-checked today.

## Pages read
| Page | URL | Evidence |
|---|---|---|
| Development hub | https://www.compass.com/development/ | [code] |
| `/new-development/` | https://www.compass.com/new-development/ returns **404** ("This page is off the map"). The footer links were read from that page. | [code] |
| Private Exclusives and the three-phase strategy | https://www.compass.com/private-exclusives/ | [fetch] |
| Compass Coming Soon on Redfin cards | See the Redfin teardown ("COMPASS COMING SOON", "EARLY ACCESS"). | [code] |

The footer product links [code] are:
- See It First™ (`/see-it-first/`)
- Private Exclusives
- Coming Soon (`/coming-soon/listings/`)
- Current Developments (`/development/`)
- Compass Development Marketing Group (separate domain)
- Concierge
- 3-Phased Marketing Strategy (separate domain)
- Compass One
- Compass Luxury

## Development hub [code]
- **Page:** "New Development", then "Current Developments". Toggle: **`Sales` / `Rentals`**. Selects: **region** (All, California, Chicago, Florida … Washington) and **sub-region**.
- **Sort:** `Recommended` · **`Immediate Occupancy`**. Ready-to-move-in comes first, offered as a sort option, not only as a filter.
- **Card:** the development name ("The Henry"), the address, the neighbourhood ("Upper West Side"). There is **no price on the card**.
- **Status badges:** **"Sold Out" (11 on the page) is kept visible** and acts as proof of track record. "Coming Soon" appeared once.
- **Photos:** all **portrait, 3:4 (0.75), on 21 of 21 cards**. They are editorial architecture shots.
- **Paging:** a "Load more developments" button, with no numbered pages.
- **Schema:** `BreadcrumbList` only.
- **Performance:** no native lazy loading (0 of 23 images).

## Private Exclusives: the three-phase marketing [fetch]
- **Phase 1, Compass Private Exclusive ("Validate Pricing"):** the listing is shared with about 340,000 agents in the network and their buyers. There are no public days on market and no public price drops. Photos and floor plans are shared "only within our trusted network". Private showings are possible.
- **Phase 2, Compass Coming Soon ("Expand Reach With No Risks"):** the listing goes public on Compass.com and Redfin.com.
- **Phase 3, Public Websites ("Sell Better").**
- **Claims to sellers, with caveats on the page:** 4.6% higher closing price (labelled a causal estimate), 34% faster to contract, and 29% less likely to drop in price ("results may vary").
- **Calls to action and lead capture:** "List Your Home" and the "Sell With Us" form, with a consent line: contact may include automated calls and texts, and "Consent is not a condition to access real estate services". When no local agent is available, the page shows "We're Sorry" and "Find an Agent".

## Agent call-to-action pattern
- **[code, via Redfin]:** every listing names one agent and the brokerage. The form asks for first name, last name, email, phone and message. "This home is coming soon. Reach out to the listing agent."
- **[prior]:**
  - **Collections:** shared boards between an agent and a client, with comments and reactions, and side-by-side views.
  - Agent profile pages carry their listings and contact details.
  - Market reports and insights are offered as lead magnets.

## Mobile [prior]
App-first. Collections sync between the buyer and the agent, and push notifications are sent for new matches.

## SEO [code]
- **Dead URL:** `/new-development/` is a 404 while the live hub sits at `/development/`, so the old path is dead. This is a finding only; no redirect is suggested.
- **Weak hub:** the hub's schema is thin (breadcrumbs only), and it has no city sub-pages in the URL. It is weaker on SEO than Zillow, Redfin or Realtor.

## What nad-lan should take
1. **A sort for "immediate occupancy first"**, offered next to a filter for it.
2. **Keep sold-out projects visible**, labelled "נמכר במלואו / אוכלס" (sold out / occupied). This proves the developer's record and keeps the pages' SEO equity.
3. **Early access before launch:** a "register for the pre-launch update" list per project (טרום שיווק), which turns the pre-launch stage into a lead engine. The phase logic carries over; the private agent network does not.
4. **An editorial, single-ratio photo grid** for the luxury line (Ashira, Einstein and similar).
