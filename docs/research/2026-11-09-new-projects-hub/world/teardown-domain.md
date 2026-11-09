# Teardown: Domain.com.au (new homes and developments)

Read attempted on 9.11.2026. **Blocked.**

## What happened
| Page | URL | Result |
|---|---|---|
| New homes, Sydney region | https://www.domain.com.au/new-homes/sydney-region-nsw/ | WebFetch: **HTTP 403** |
| New homes, Melbourne region | https://www.domain.com.au/new-homes/melbourne-region-vic/ | Chrome opened the page, but the Claude-in-Chrome **site-permission prompt timed out**, so no script ran |
| Search for project pages | web search | It returned only Domain's "new developments" news section and the rival apartments.com.au |

The sibling site apartments.com.au [search] shows a development count ("8,767 new and off the plan developments for sale"), city filters by budget ("under $4.5 million"), and project facts such as "197 apartments with 33 one bedroom, 140 two bedrooms and 24 three bedroom units".

## Known patterns [prior], for the matrix only and not proof
- **Project card:**
  - "Off the plan" / "Under construction" / "Completed – ready to move in"
  - a "From $" price or a price range
  - the developer's name and logo
  - the number of residences
  - an "Artist impression" caption on renders
- **Project page:**
  - a **display suite** with its address and opening hours, which is the sales office
  - the **completion date**
  - a unit mix with bedroom counts
  - the developer's profile and past projects
  - a gallery split into renders, the display suite, and the area
  - a "Get price list" or "Download brochure" lead magnet
- **Enquiry form:** name, email, phone, postcode, plus checkbox intents: "Price information", "Floor plans", "Brochure", "Inspection / display suite visit", "Similar properties".
- **Filters:** a "New homes" channel with off-the-plan versus completed as separate choices. A "Ready to move in" choice exists for completed stock.
- **SEO:** region hubs at `/new-homes/{region}-{state}/`, and project pages at `/project/{id}/{slug}/`.

## What nad-lan should take (verify before using)
- **Enquiry intents as checkboxes:** price list (מחירון) · floor plans (תוכניות) · visit to the sales office (ביקור במשרד מכירות) · similar projects (פרויקטים דומים). One form, and the intent is clear for the developer.
- **The sales office as a first-class field:** address, hours, a navigation link. This matches the Realtor "Office hours" module seen live.
- Every render captioned "הדמיה" ("render"), the Israeli equivalent of "Artist impression".

## To finish later
Allow domain.com.au once in the Claude-in-Chrome prompt (the owner clicks Allow), then read one region hub and one `/project/` page.
