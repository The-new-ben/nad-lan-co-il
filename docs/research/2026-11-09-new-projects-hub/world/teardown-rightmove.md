# Teardown: Rightmove (new homes)

Read on 9.11.2026 with WebFetch (the page text). The site was not blocked.

**Evidence classes**
- **[fetch]:** the page text pulled with WebFetch.
- **[prior]:** a known pattern from before this session, not re-checked today.

## Pages read
| Page | URL | Evidence |
|---|---|---|
| London new homes | https://www.rightmove.co.uk/new-homes-for-sale/London.html | [fetch] |
| A development-area page | https://www.rightmove.co.uk/new-homes-for-sale/development.html (it resolved to "St Peters Development, Sunderland", which had no results and contradictory counts) | [fetch] |

## Search, filter and sort [fetch]
- **H1:** "New Homes and Developments For Sale in London". **4,074 results**, in 42 numbered pages with Previous and Next.
- **Filters:**
  - **Radius:** "This area only", then "Within 1/4 mile" up to "Within 40 miles".
  - Min and max price, from £50,000 to £20,000,000.
  - Min and max beds, from Studio to 10.
  - Property Type.
  - `Filters`.
- **AI keyword refine:** "**Choose 3 keywords to refine your search**", with an AI disclaimer: the tool "uses AI to help you find relevant properties but it can make mistakes". Buttons: Cancel / Done.
- **Sort:** Highest Price · Lowest Price · **Newest Listed** · Oldest Listed.
- **Map:** "Map view" and "Show results on map", on a separate map URL. Detail pages show an "Approximate location" map.

## Cards [fetch]
- **Photos:** a carousel with a counter ("**1/16**"), plus icons for **"Property has a floorplan"** and **"Property has virtual tour"**.
- **Badges:**

  | Kind | Labels |
  |---|---|
  | Paid tiers | **"FEATURED NEW HOME"**, "**FEATURED NEW HOME - NEW RELEASE**", "Premium Listing" |
  | Type | "New Home" |
  | Price change | "**Reduced on [date]**" |
  | How the price is quoted | "Guide Price", "**From**", "Offers in Region of" |
  | Feature tags | "Stunning Views", "Substantial Plot" |
- **Fields:** price, address, type (Apartment, Penthouse, Town House, Detached, Duplex), bed and bath counts, a short description, and key-feature bullets.
- **Agent or developer block:** logo, name, "**Added on [date] by [agent]**".
- **Actions:**
  - **"Call"** with the phone number and "Local call rate"
  - "Click to email [agent]"
  - **Save**
  - on developer cards: **"Book Viewing"** and **"View development"**

## Personalisation [fetch]
- `Save Search`, **`Create Alert`**, a per-card `Save`, and "My Rightmove".
- **Alert frequency:** "When would you like to be alerted?" **Instantly · Daily · Every 3 days · Every 7 days**.

## Trust [fetch]
- **"Staying secure when looking for a property"**, which links to a security centre (fraud guidance).
- The footer prohibits scraping.

## Lead capture
- **[fetch]:** enquiry pages at `/new-homes-for-sale/contactBranch.html?propertyId={id}`, plus Call, Email and Book Viewing.
- **[prior]:** the form asks for name, email and phone, then a choice of "I'd like to view" or "more details", and a short status ("first-time buyer", "property to sell").

## Money and partners [fetch]
"**Get a Mortgage in Principle**", powered by NatWest: "Personalised result in just 20 minutes", "No impact on your credit score".

## SEO [fetch]
- **URL patterns:**
  - city hub: `/new-homes-for-sale/London.html`
  - map: `/new-homes-for-sale/map.html?…channel=NEW_HOME&locationIdentifier=REGION^87490…`
  - listing: `/properties/{id}#/?channel=RES_NEW`
  - **developer branch:** `/developer/branch/{Developer}/{Name}-{id}.html`
- **Links to sibling hubs:** "View house prices in London" and "Estate agents in London".
- **Thin pages:** the development-area page shows "no properties" and "139 properties match" at the same time. This is an example of a thin area page.

## Mobile [prior]
The app is the main channel. Instant alerts arrive as push notifications, and saved properties sync.

## What nad-lan should take
1. **Alert frequency choices:** instantly, daily, every 3 days, weekly.
2. **Icons on the card for floor plan, virtual tour and photo count.** The Israeli set is "תוכנית דירה", "סיור 360", "סרטון" and "1/16".
3. **"Reduced on [date]"** with a real date, and **"From ₪"** as the price form for projects.
4. **A developer page per developer** (`/developer/...`), linked from every card.
5. **A security notice:** never transfer money outside the bank escort or the guarantee (ליווי בנקאי / ערבות).
