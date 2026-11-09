# Teardown: Google Maps and Apple Maps "near me" patterns

Written on 9.11.2026. **Not read live this session.** All of it is a known pattern from before this session, marked [prior]. Use it as a design reference, and check it on a phone before building.

## Patterns
| Pattern | Google Maps | Apple Maps | What it gives the buyer |
|---|---|---|---|
| **"Search this area"**: after the user pans, the button re-runs the query instead of re-querying on every drag | Yes | Yes | Control and a calm map. The list never jumps under the finger. |
| **"Near me" through the browser's location permission**, with a fallback to a typed address or city when the user says no | Yes | Yes | One tap gives "what is close to me", with no form to fill |
| Results sorted by distance, with **the distance and the travel time on each card** | Yes | Yes | Real proximity, not straight-line marketing |
| **Filter chips over the map** (Open now, Top rated, Price) | Yes | Yes | One-tap filtering that does not hide the map |
| **The list and the pins stay in sync**: tapping a pin raises the card; scrolling cards moves the pin | Yes | Yes | Where a place is and what it is, together |
| Labels on pins with the name and one key fact (rating, price) | Yes | Yes | Readable without opening the place |
| **Save to lists**, with notes, shared with family | Yes | Yes ("Guides") | Planning with a partner |
| **Street View / Look Around** | Yes | Yes | See the street before a visit |
| "Popular times" chart (live busyness) | Yes | Partly | Plan the visit |
| A bottom sheet with three heights on mobile (peek / half / full) | Yes | Yes | One-hand use; the map stays visible |
| Directions in one tap to the sales office | Yes | Yes | Turns interest into a visit |

## How this fits nad-lan /projects/ (and the owner's laws)
- **The owner's law on the near-me finder (HAD-672):** no floating button, ever, and positive layers only. So "near me" is **a sort option and a filter chip inside the hub** ("הכי קרוב אליי", "closest to me"), not a floating button.
- **The owner's taste on map labels:** no numbered dots. Pins carry **small readable labels with the name and one fact**, for example "מגדלי X · מ-₪2.9M" (Towers X, from ₪2.9M).
- **Search this area:** do not re-query on every drag. Show "חפש באזור הזה" ("search this area") after the user pans. This also protects smooth scrolling (Ben's smooth-scroll law: no capture of the wheel or touch).
- **Travel time** to the light rail or train, the sea and the main employment centres, computed and labelled with its method.
- **Directions** to the sales office in one tap (Waze or Google Maps deep link).
- **Save to lists, shared with a partner:** "הרשימה שלנו" ("our list"), a shareable link of saved projects.
