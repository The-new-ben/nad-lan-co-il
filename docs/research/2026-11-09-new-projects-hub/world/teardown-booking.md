# Teardown: Booking.com (UX benchmark, not real estate)

Read on 9.11.2026. Read-only. No sign-in, no booking, no form submitted.

**Evidence classes**
- **[code]:** read live in the owner's Chrome with a DOM script.
- **[prior]:** a known pattern from before this session, not re-checked today.

## Pages read
| Page | URL | Evidence |
|---|---|---|
| Search results (Tel Aviv, 10 to 12 December 2026, 2 adults) | https://www.booking.com/searchresults.en-gb.html?ss=Tel+Aviv&checkin=2026-12-10&checkout=2026-12-12&group_adults=2&no_rooms=1 | [code] |
| Property page (The Norman Tel Aviv) | https://www.booking.com/hotel/il/the-norman-tel-aviv-tel-aviv.en-gb.html | [code] |

A guessed hotel slug (`/hotel/il/the-norman.en-gb.html`) did not open the hotel. It showed a generic "Verified reviews from real guests / How does it work?" page. This is noted only.

## Search, filter and sort [code]
- **Controls:** `List` / `Grid` · **`Sort by: Our top picks`** · **`Show on map`** · a "Show entire homes & apartments" switch.
- **Filters with live counts on every option:**
  - **"Your budget (per night)":** a slider from ₪100 to ₪3,000+.
  - **"Popular filters"**, which change with demand: Capsule hotels 2 · City view 201 · Double bed 469 · Private pool 15 · Bidet 19 · Room service 42 …
  - **"Distance from centre of Tel Aviv":** Less than 1 km **189** · Less than 3 km **415** · Less than 5 km **463**.
  - **"Distance from address"**, measured from an address the buyer types.
  - **Review score:** Superb 9+ **173** · Very good 8+ **329** · Good 7+ **381** · Pleasant 6+ **398**.
  - **"Highly rated features, based on guest reviews"**.
  - Facilities, Room facilities, accessibility.
  - Long groups collapse behind **"Show all 14 / 25 / 20"**.

## Cards [code]
There are 20 per page. Each card shows:
- name ("Opens in new window")
- area and landmark, such as "Neve Tzedek, Tel Aviv (Tel Aviv Promenade)", with **"Show on map"**
- **"1.8 km from centre"**, **"Beach nearby"**, **"350 m from beach"**
- **"Scored 8.3 · Very good · 1,688 reviews"**, plus a **sub-score on the card**: "Location 9.3"
- room type and bed set-up
- terms: "Free cancellation", "No prepayment needed – pay at the property", "Breakfast included"

It also shows:
- **Scarcity from real stock:** "**We have 5 left at this price**".
- **The price in context:** "2 nights, 2 adults". The struck-through and current prices read **"₪ 2,854 ₪ 2,283"**, and screen readers hear "**Original price ₪ 2,854. Current price ₪ 2,283.**" A note says "Additional charges may apply".
- **Deal badges seen on the page:**

  | Badge | Count |
  |---|---|
  | "Late Escape Deal" | 4 |
  | "Limited-time Deal" | 1 |
  | "Genius loyalty programme" | 1 |
  | "Sustainability certification" | 1 |
- **A nudge to sign in that names the gain:** "To see if you can save 10% or more at this property – Sign in".
- **Photos:** square, **1:1 on 20 images**, with 29 of 30 lazy-loaded.

## Detail page modules, in rendered order [code]
- **Title tag:** "The Norman Tel Aviv, Tel Aviv **(updated prices 2027)**", a freshness word in the title.
1. H1 and gallery.
2. **"Guests who stayed here loved"**: a carousel of review snippets.
3. **"Property highlights"**: Fabulous breakfast · "Fabulous free WiFi, **Rated 9.0 by guests**" · Parking (valet, garage, accessible) · Wellness.
4. Description, then **"Most popular facilities"**.
5. **"Availability"**: the room table.
6. **"Guest reviews"** with **"Categories:"** Location 9.7 · Cleanliness 9.5 · Value for money 8.3 …, then "See what guests loved the most".
7. **"Travellers are asking"**: question chips such as "Do they serve breakfast?", "Is the spa open?", "Is there an airport shuttle service?", "Can I park there?", "Is the restaurant open?"
8. **"Still looking?"**: alternatives.
9. **"Hotel surroundings"**:
   - "What's nearby" (Meir Park 1.1 km, Bauhaus Foundation Museum 1.1 km, Dizengoff Square 1.6 km)
   - Restaurants & cafes
   - Top attractions
   - Beaches in the neighbourhood
   - **Public transport** (Tel Aviv Central Bus Station 1.9 km, HaHagana Train Station 2 km)
   - Closest airports
10. Facilities, then **"How are we doing?"** (feedback on the page itself).
11. Property policies, Child policies, Cot and extra bed policies, then **"The fine print"**.
12. **"FAQs about The Norman Tel Aviv"**: Does it have …? · What type of room can I book? · What are the check-in and check-out times? · **How much does it cost to stay?** · What is there to do? · How far is it from the centre? · How close to the beach is it?
13. Links to cities.

## Personalisation
- **[code]:** the sign-in nudge.
- **[prior]:**
  - **Wishlists:** a heart that saves to named lists, which can be shared.
  - **Recently viewed**, and searches resumed on the home page.
  - Price alerts in the app.
  - The Genius loyalty discount for members.
  - **Grid comparison.** There is no compare table.

## Trust
- **[code]:** verified reviews, with an explainer page. Every rating carries a review count. Scores are given per category. "Additional charges may apply". Fine print. A sustainability certification label.
- **[prior]:** Booking toned down fake-urgency lines ("X people are looking") after EU consumer-authority action in 2019. **This is why only true scarcity carries over.**

## Lead capture
There is no lead form. The conversion is the booking itself. The equivalent action for a real-estate hub is "reserve a meeting or save the project".

## Schema.org types [code]
`Hotel`, `AggregateRating`, `PostalAddress` on the detail page.

## What carries over honestly to a projects hub
| Booking pattern | Israeli new-projects version | Honest? |
|---|---|---|
| Counts on every filter option | "אכלוס מיידי (37)", "4 חדרים (212)" | Yes |
| Distance bands with counts | "Up to 500 m from the light rail (41)" | Yes, if computed from coordinates |
| "Distance from address" | "Distance from my workplace or from my parents" | Yes |
| "We have 5 left at this price" | "3 four-room apartments left in this price list" | **Only from a real developer price list**, dated |
| Strike-through price with screen-reader text | A real price-list change, with the date | Only if both prices were published |
| "Late Escape Deal" | A verified deal chip (20/80, no index linkage) | Only if the developer published it |
| Sub-score on the card | "Transport 9 · Schools 8" | Only from a published formula |
| "Travellers are asking" | "Buyers are asking": is there bank escort? when is occupancy? parking? | Yes |
| "(updated prices 2027)" in the title | "מעודכן נובמבר 2026" ("updated November 2026") | Only if the data really changed |
| "X people looking now" | **Do not use.** Fake urgency. | No |
