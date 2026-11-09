# Teardown: NewHomeSource (builder data, quick move-in homes)

Read on 9.11.2026. Read-only, no form submitted.

**Evidence classes**
- **[code]:** read live in the owner's Chrome with a DOM script.
- **[prior]:** a known pattern from before this session, not re-checked today.

This is the closest model in the world to an Israeli new-projects hub. Builders feed it directly: communities, plans, quick move-in homes, deals and reviews.

## Pages read
| Page | URL | Evidence |
|---|---|---|
| Old quick move-in URL | https://www.newhomesource.com/specs/tx/austin-area returns **404** (`/mvcerror?statuscode=404`) | [code] |
| Communities hub (Austin area) | https://www.newhomesource.com/communities/tx/austin-area | [code] |
| Community page | https://www.newhomesource.com/community/tx/liberty-hill/santa-rita-ranch-90ft-lots-by-highland-homes/147878 | [code] |

Zonda, the builder-data company, was not read this session. Its builder data feeds this market [prior].

## Search, filter and sort [code]
- **Page:** "New Construction Homes in Austin, TX | **594 Communities**". Tabs: **`Communities` · `Homes` · `Builders`**.
- **Quick chips:** **"Hot deals"** · "Condos & Townhomes" · "55+ Communities" · **"Coming soon"**.
- **Filters:**
  - **Price**, min and max.
  - **Bed / Bath** (Any, 1+ to 5+).
  - **Move-In Date**, with the options: **"Floor Plans" · "All Quick Move-In" · "Move now" · "1-2 months" · "3-6 months"**.
  - **Home type:** Single Family · Custom Build Homes · Luxury Homes · Condos & Townhomes · **Model Homes**.
  - **Community status:** **Coming soon · Grand opening · Active · Closeout**.
  - **Amenities:** nature areas · pool · golf course · green · sport facilities · parks · views · waterfront · gated community.
  - **55+:** "55+ Communities only" / "Exclude 55+ communities" / "Show all communities".
  - **Deals and data:** "**Price reduction**" · "Hot deals" · "**Listings with reviews**" · "**Listings with HOA information**".
  - **Builder:** "All builders" and then every builder by name (Ashton Woods, D.R. Horton, David Weekley Homes …).
- **Apply buttons:** **"Show 594 communities"**, a live count on the apply button, plus "Clear all".
- **Saving and sorting:** `Save search` · `Sort`.
- **Map:** `List` / `Map`, "Remove boundary" (search by a drawn area), zoom, fullscreen, keyboard shortcuts.

## Cards [code]
- **"SPOTLIGHT"** marks the paid placement.
- **Price:** **"From $339,999"**. When no price exists, the card says **"Pricing coming soon"**.
- **"Recently reduced"**.
- **Ranges:** "2-4 Beds · 2-3 Baths · 1,700 - 2,678 SqFt".
- **Place and builder:** "Community in Manor, TX 78653", then "**By Milestone Community Builders**".
- **Builder rating** on the card ("4.4").
- **Calls to action:** **"Free brochure"** (the main lead magnet) or "Get more information", plus "Save this item to my favourites".
- **Photos:** **16:9 (1.78) on 40 images**; 42 of 66 images lazy-loaded.

## Community page [code]
- **Header summary:** "4-5 Beds · 4-5 Baths · 3-4 Car garage · 3,709 - 4,488 Sq Ft · **3 Quick move-ins**".
- **Modules, in order:**
  - Gallery
  - **Community highlights**, with amenity tags (Cabana, Community Center, Park, Picnic Area, Playground, Pool, Splash Pad, Trails, Volleyball)
  - About
  - **"Get more details"**, the lead form
  - "Your free brochure has been sent", the inline confirmation
  - **"Available homes"** with **"Quick move-ins (3)"**. Each unit shows its address and plan name, for example "260 Jates Field Bend (**Plan Varese**)", then "$998,260 · 5 Beds · 5.5 Baths · 3 Gr · 4,488 SqFt · **Quick move-in** · Single family home". There are "Clear all filters" and "Show 3 results" buttons.
  - **"Community map"** and **"View interactive site map"**, a lot plan
  - Neighborhood and amenities, with schools by district
  - **Builder details** (Highland Homes)
  - **"TrustBuilder reviews"**, which are third-party verified
  - **"More communities by Highland Homes"**
- **The lead form ("Get more details"):**
  - Full Name, Email, Phone, Zip, an "Outside U.S." option.
  - **Preferred Contact Method:** Email / Phone Call / Text Message.
  - **"Are you working with a real estate agent?"**
  - **Ready-made question chips:** "Tell me about your c[ommunity]" · "**Are there HOA fees?**"
  - Submit request.
- **Tour:** "Request a tour" with day chips **"TODAY MON 9 · TOMORROW TUE 10 · WED 11 …"**.
- **Brochure:** "Download brochure" and "No, ignore".

## Schema.org types [code]
- **Hub:** `BreadcrumbList`, `ListItem`, **`Product`/`House`**, `ImageObject`, `PostalAddress`, `GeoCoordinates`, `Offer`.
- **Community:** `BreadcrumbList`, **`HomeAndConstructionBusiness`**, `PostalAddress`, `Place`, `GeoCoordinates`.

## SEO [code]
- **URL patterns:**
  - metro hub: `/communities/{st}/{metro}-area`
  - community: `/community/{st}/{city}/{community-slug}-by-{builder-slug}/{id}`. The builder name is inside the slug.
- **Dead URL:** the old `/specs/` quick move-in hub is a 404, with no replacement path visible. This is a finding only.
- **Link blocks:** "Search by popular metro", "Search new homes by state", "Homebuying guides", "Homebuying tools".

## What nad-lan should take (the most direct mapping of all the sites)
| NewHomeSource | nad-lan /projects/ |
|---|---|
| Move-In Date: Move now / 1-2 months / 3-6 months / Floor Plans | **אכלוס מיידי / עד 6 חודשים / עד שנה / על הנייר** (immediate occupancy / up to 6 months / up to a year / on paper) |
| Status: Coming soon / Grand opening / Active / Closeout | **טרום שיווק / השקה / בשיווק / מלאי אחרון** (pre-marketing / launch / marketing / last stock), plus **אוכלס** (occupied) |
| Tabs: Communities · Homes · Builders | **פרויקטים · דירות · יזמים** (projects · apartments · developers) |
| "Quick move-ins (3)" inside the community | "**דירות לאכלוס מיידי (3)**" ("immediate-occupancy apartments (3)") inside the project |
| Model Homes filter | "**יש דירה לדוגמה**" ("has a model apartment"), labelled under the 25.9 rule |
| Free brochure | **The developer's price list and brochure (PDF)**, an honest lead magnet |
| Preferred contact method | **WhatsApp / שיחה / מייל** (WhatsApp / call / email) |
| Question chips | "מה המחיר לדירת 4 חדרים?" · "מתי האכלוס?" · "יש ליווי בנקאי?" (price of a four-room apartment? when is occupancy? is there bank escort?) |
| Show 594 communities | "**הצג 1,087 פרויקטים**" ("show 1,087 projects"), a live count |
| TrustBuilder reviews | Verified buyer reviews, only if we run real verification. Otherwise the slot is left out. |
| Interactive site map | A building and lot plan with availability per building |
