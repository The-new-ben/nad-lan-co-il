# Micro-feature catalogue for the nad-lan /projects/ hub

Compiled on 9.11.2026 from the teardowns in this folder.

**Abbreviations**
- **Z** Zillow · **RE** Realtor.com · **RF** Redfin · **C** Compass · **B** Booking.com · **RM** Rightmove · **NHS** NewHomeSource · **D** Domain · **I** Idealista · **M** Google and Apple Maps

**Evidence classes**
- **[code]:** seen live today in Chrome, read by a DOM script.
- **[fetch]:** seen today through WebFetch.
- **[prior]:** a known pattern, not re-checked today.

**Priority**
- **Must:** needed to be at least level with the leaders.
- **Should:** a clear gain.
- **Nice:** polish.

**Owner laws applied in the "fit" column**
- **Honesty:** unknown values are omitted, never shown as "0" and never as "being checked".
- **Labels:** "צילום אמיתי" (real photo) only on real photos; "דירה לדוגמה" (model apartment) labelled as such.
- **No broker posture:** the site never presents itself as a broker.
- **Near me:** no floating "near me" button.
- **Map pins:** no numbered dots.
- **No runtime filters** that rewrite content.

## A. Search, filters and sort
| # | Feature | Who has it | What it does for the buyer | Fit for the Israeli hub (אכלוס מיידי = immediate occupancy) | Priority |
|---|---|---|---|---|---|
| 1 | Move-in timeframe filter: Move now / 1-2 months / 3-6 months / Floor plans | NHS [code] | Picks homes by when they can actually live there | The core of the hub: **אכלוס מיידי / עד 6 חודשים / עד שנה / על הנייר** (immediate / up to 6 months / up to a year / on paper), fed by the delivery date of each building | Must |
| 2 | "Immediate Occupancy" as a **sort** option | C [code] | Ready stock first, without losing the rest | Sort option "אכלוס קרוב קודם" ("nearest occupancy first") | Must |
| 3 | Community lifecycle status: Coming soon / Grand opening / Active / Closeout | NHS [code] | Tells how early or late in the sale the buyer is | **טרום שיווק / השקה / בשיווק / מלאי אחרון / אוכלס** (pre-marketing / launch / marketing / last stock / occupied) chips | Must |
| 4 | Deal-type chips: All deals · Reduced rates · Cash at closing · Flex cash · Appliance package · Free upgrades | RE [code] | Shops by the kind of deal, not only by price | 20/80 · no index linkage (ללא הצמדה) · developer loan (הלוואת קבלן) · discount · upgrade package · free parking. **Only verified, dated deals.** | Must |
| 5 | "Promotions explained" link beside the deal chips | RE [code] | Learns what a deal really means | An explainer: "what 20/80 really costs", linked to /buying-apartment/ | Must |
| 6 | Live count on the apply button ("Show 594 communities") | NHS [code] | Never applies a filter into zero results | "הצג 214 פרויקטים" ("show 214 projects") | Must |
| 7 | Count beside every filter option (City view 201, <1 km 189) | B [code] | Sees the shape of the market before clicking | Counts on rooms, city, stage, occupancy and deals | Must |
| 8 | Active-filter count on the Filters button ("Filters • 1") | RF [code] | Knows something is narrowing the results | "סינון • 3" ("filters • 3") | Should |
| 9 | Budget slider with a wide range (₪100–3,000+) | B [code]; histogram [prior] | Sets a budget visually | Slider in total ₪ or ₪/m², with a price histogram behind it | Should |
| 10 | Distance-from-centre bands with counts | B [code] | Proximity as a filter | "Up to 500 m from the light rail (41)", sea, train | Should |
| 11 | "Distance from address" | B [code] | Distance from my own anchor | From work, from my parents, from a school | Should |
| 12 | Builder filter listing every builder | NHS [code] | Trusts a known developer | יזם / קבלן (developer / contractor) filter with counts | Must |
| 13 | Tabs Communities · Homes · Builders | NHS [code] | Changes the unit of search | **פרויקטים · דירות · יזמים** (projects · apartments · developers) | Must |
| 14 | Bedroom chips with counts inside a community ("3 Bed (7)") | RF [code] | Jumps to the right flat size | "4 חדרים (12)" ("4 rooms (12)") inside each project | Must |
| 15 | Amenity filters (pool, gated, views, waterfront, parks) | NHS [code] | Lifestyle filters | Pool, gym, lobby, view of the sea, garden flat, penthouse, parking, storage | Should |
| 16 | "Model Homes" filter | NHS [code] | Can visit a finished sample | "יש דירה לדוגמה" ("has a model apartment"), labelled under the 25.9 rule | Should |
| 17 | Filters "Listings with reviews" / "with HOA information" | NHS [code] | Prefers listings with complete data | "With a published price list" / "with a building-committee (ועד בית) estimate" / "with a permit" | Should |
| 18 | "Price reduction" and "Hot deals" quick filters | NHS [code] | Bargain hunting | "Price list went down" (from real price-list history) | Should |
| 19 | Exclude 55+ / only 55+ | NHS [code] | Removes irrelevant stock | Toggle to exclude or include subsidised lottery and assisted-living projects | Should |
| 20 | Popular filters that follow demand | B [code] | Sees what others filter by | "Popular in Tel Aviv: 4 rooms, immediate occupancy" | Nice |
| 21 | AI keyword refine with a disclaimer | RM [fetch] | Free-text needs | Hebrew free text ("קרוב לפארק, מרפסת גדולה", near a park, big balcony), with an AI notice | Nice |
| 22 | Natural-language "AI Search" | RF [code]; RE prompt chips [code] | Asks the way they talk | "4 חדרים בגבעתיים עד 3.5 מיליון אכלוס 2027" (4 rooms in Givatayim, up to 3.5 million, occupancy 2027), parsed into filters, which stay visible | Should |
| 23 | Radius selector (this area only up to 40 miles) | RM [fetch] | Widens a thin area | "Include up to 5 km around" | Should |
| 24 | Draw on map / Remove outline / Undo | RF, NHS [code] | Searches the exact streets they want | Draw a zone; useful for TLV north and Sde Dov | Should |
| 25 | Sort: Newest listed / Lowest / Highest price | RM [fetch], RE [code] | Standard control | Plus "₪/m² lowest" and "occupancy nearest" | Must |
| 26 | Sales / Rentals toggle on the developments hub | C [code] | Separates buy from rent | Sale / build-to-rent (דירה להשכרה ארוכת טווח) toggle | Nice |
| 27 | List / Grid / Map layout switch | B, RF, NHS [code] | Chooses a density | List, map and split on desktop; list and map on phones | Must |
| 28 | Map keyboard shortcuts | RF, NHS [code] | Accessibility and power use | Keyboard access on the map | Nice |

## B. Cards
| # | Feature | Who has it | What it does for the buyer | Fit | Priority |
|---|---|---|---|---|---|
| 29 | "From ₪X" plus ranges (beds 3-5, baths, sq ft) | RE, NHS, RF [code] | A project at a glance | "מ-₪2.4M · 3–5 חד' · 85–140 מ"ר" (from ₪2.4M · 3–5 rooms · 85–140 m²). Unknown values are omitted. | Must |
| 30 | "Built by X" / "By Builder" on the card | RE, NHS [code] | Trust in the developer | Developer name, linked to the developer page | Must |
| 31 | Builder rating on the card (4.4) | NHS [code] | Quality signal | Only with a real verified source. Otherwise leave the slot out. | Nice |
| 32 | Freshness badge ("NEW 11 HRS AGO", "10 hours ago", "Added on …") | RF, Z [code], RM [fetch] | Knows the data is live | "מחירון עודכן 3.11" ("price list updated 3.11") / "חדש באתר" ("new on the site") | Must |
| 33 | "Reduced on [date]" / "Recently reduced" / cut amount ("$300k") | RM [fetch], NHS, RE [code] | Spots real price moves | "The price list dropped by ₪120K on 1.11", only from saved price-list history | Must |
| 34 | One-fact highlight chip ("Cozy fireplace") | Z [code] | One memorable reason to click | Fact chip from data: "קומה 28", "מרפסת 18 מ"ר", "נוף לים" (28th floor, 18 m² balcony, sea view). No AI wording. | Should |
| 35 | Key-feature bullet line ("Layered millwork • Inset cabinetry") | RF [code], RM [fetch] | Scans the specification | "ממ"ד · 2 חניות · מחסן" (safe room · 2 parking spaces · storage) | Should |
| 36 | "Pricing coming soon" | NHS [code] | No dead card | **Adapt:** omit the price (owner law) and show the button "קבלו מחירון" ("get the price list") instead | Must |
| 37 | Media icons: floor plan, virtual tour, photo count "1/16", "tour available" | RM [fetch], RE [code] | Knows what is inside before clicking | Icons for תוכנית / 360 / סרטון / מודל תלת־ממד (plan / 360 / video / 3D model) / count | Must |
| 38 | Paid-placement label (Spotlight, Showcase, FEATURED NEW HOME, Premium) | RE, Z, NHS [code], RM [fetch] | Knows what is an advertisement | "מקודם" ("promoted") label; ties to the advertiser-deal skill (annual prime spot) | Should |
| 39 | Sold-out projects kept on the hub ("Sold Out") | C [code] | The developer's track record | "נמכר במלואו / אוכלס" ("sold out / occupied"), kept and dimmed | Should |
| 40 | Status chip (Pending, Coming soon, Early access, Closeout) | RE, RF, NHS [code] | Stage at a glance | The stage chip (row 3) on every card | Must |
| 41 | Deal badge on the card ("Reduced rates", "Late Escape Deal") | RE, B [code] | The deal is visible on the card | "20/80" / "ללא הצמדה" / "הלוואת קבלן", verified and dated | Must |
| 42 | Distance line ("350 m from beach", "1.8 km from centre") | B [code] | Location in plain numbers | "6 דק' הליכה לרכבת הקלה · 900 מ' לים" (6 minutes' walk to the light rail · 900 m to the sea), computed | Must |
| 43 | Sub-score on the card ("Location 9.3") | B [code] | The best attribute pops out | "תחבורה 9" ("transport 9") from a published formula only | Nice |
| 44 | Photo carousel inside the card | Z [code], RM [fetch] | Browses without leaving the list | Up to 5 photos, lazy-loaded, swipe on phones | Should |
| 45 | Save heart on every card | all [code] | Builds a shortlist | Heart that saves to "הרשימה שלי" ("my list"), no login (local) | Must |
| 46 | Hide listing | Z, RF, RE [code] | Removes noise | "הסתר" ("hide") | Nice |
| 47 | Contact on the card: Contact builder / Call / Book Viewing | RE, NHS [code], RM [fetch] | Acts at once | WhatsApp, call the developer's sales office, or "קבעו ביקור" ("book a visit"). Never posing as a broker. | Must |
| 48 | "Free brochure" button on the card | NHS [code] | A low-commitment lead | "קבלו מחירון וחוברת" ("get the price list and brochure") | Must |
| 49 | Save button with the address in its accessible label | RE [code] | Screen-reader clarity | aria-label "שמור את מגדלי X ברמת גן" ("save Towers X in Ramat Gan") | Should |
| 50 | Struck-through old price with screen-reader text ("Original price … Current price …") | B [code] | An honest price change | Only when both price lists were published | Should |
| 51 | "We have 5 left at this price" | B [code] | True scarcity | "נותרו 3 דירות 4 חד' במחירון הזה" (3 four-room apartments left in this price list), only from a real price list. Never fake. | Should |

## C. Project detail modules
| # | Feature | Who has it | What it does for the buyer | Fit | Priority |
|---|---|---|---|---|---|
| 52 | Sticky section tabs (Overview, Facts, Community, Market value, Payment, Neighborhood) | Z, RF [code] | Jumps to what matters | Tabs **below** the H1, answer and calls to action (content-first law) | Must |
| 53 | Summary strip: "Price from · 14 Listings · sq ft range · bedrooms" | RF [code] | The project in one line | "מ-₪ · 12 דירות זמינות · 85–140 מ"ר · 3–5 חד'" (from ₪ · 12 available · 85–140 m² · 3–5 rooms) | Must |
| 54 | Move-in-now table (Listing · Price · Bed/bath · Status) | Z, RE ("Move-in Ready Homes"), NHS ("Quick move-ins (3)") [code] | Sees exactly what is ready | "דירות לאכלוס מיידי" (immediate-occupancy apartments): unit, floor, rooms, m², price, status | Must |
| 55 | Plan cards with "from $X+" ("Ready-to-build homes (12)") | RF [code] | Compares the typical plans | "דירות על הנייר / תוכניות טיפוסיות" (apartments on paper / typical plans) | Must |
| 56 | Exterior design options (Design 1–5) | Z [code] | Sees the variants | Building façades and stages, labelled "הדמיה" (render) | Nice |
| 57 | Price history with ₪/sqft, source and "Report a problem" per row | Z [code] | Verifies the price trend | **Price-list history per m², with date, source and a "דווחו על טעות" ("report an error") link** | Must |
| 58 | Automated estimate, or an honest "Not available" | Z [code], RF [prior] | A reference value | Area ₪/m² from real transactions (נדל"ן נט, the official deals data). Omitted when missing. | Should |
| 59 | Rent estimate ("Rent Zestimate") | Z [code] | Investor yield | Expected rent and gross yield, sourced | Should |
| 60 | Payment calculator with a breakdown (P&I, taxes, HOA, insurance) | RF, RE, Z [code] | The real monthly cost | Mortgage, municipal tax (ארנונה), building committee (ועד בית), insurance; links to /mortgage-calculator/ | Must |
| 61 | "Is this affordable? Calculate your buying power" | RE [code] | Budget fit | "כמה אני יכול לקנות" ("how much can I buy"), linked to the mortgage universe | Should |
| 62 | Eligibility toggle inside the payment ("Apply veterans benefits") | RE [code] | Personal cost | Purchase tax for an only apartment versus an additional one; Housing Ministry eligibility | Should |
| 63 | Disclosure on the calculation (RealCost™ Disclosure) | RE [code] | Trusts the number | "איך חישבנו" ("how we calculated") link | Should |
| 64 | Tour type: in person or live video | Z [code] | Remote buyers | Sales-office visit or a video call (abroad and new immigrant buyers) | Must |
| 65 | Tour request with up to 3 date chips ("TODAY MON 9 …") | RE, NHS [code] | Picks times, not "call me" | Three slots, inside sales-office hours | Must |
| 66 | Office hours and sales-office address | RE, RF [code] | Knows when to come | שעות משרד מכירות (sales-office hours) and a Waze link | Must |
| 67 | Ready-made question chips in the form ("Are there HOA fees?") | NHS [code] | Asks without typing | "מה מחיר 4 חד'?" · "מתי אכלוס?" · "יש ליווי בנקאי?" · "יש מבצע?" (price of 4 rooms? when is occupancy? bank escort? any deal?) | Must |
| 68 | Preferred contact method (Email / Phone / Text) | NHS [code] | Contacted the way they want | WhatsApp / call / email | Must |
| 69 | "Are you working with an agent?" | NHS [code] | Routing | "יש לכם מתווך?" ("do you have a broker?") as an optional field | Nice |
| 70 | "Travellers are asking" question chips | B [code] | Answers before contact | "קונים שואלים" ("buyers are asking"), answered from data | Should |
| 71 | "What's nearby" with distances, plus public transport and closest airports | B [code] | Location in numbers | Light rail and train, schools, parks, sea, malls, with distance and walking minutes | Must |
| 72 | Walk / Transit / Bike Score | Z, RF [code] | Car-free living | An Israeli score with a published method | Should |
| 73 | Sun exposure "Sunscore 77/100" | RF [code] | Light and heat | Computed from building heights and orientation data only; never a guessed bearing | Should |
| 74 | Schools module with a named source | Z, RF, RE [code] | Family fit | Schools from data.gov.il, distances | Should |
| 75 | "Local legal protections" | Z [code] | Feels protected | **חוק המכר (the Sale Law), the guarantee, bank escort, delay compensation**, in plain Hebrew | Must |
| 76 | About the builder, plus "More communities by builder" | RF, NHS [code] | The developer's track record | A developer profile and their other projects (live and occupied) | Must |
| 77 | Third-party builder reviews (TrustBuilder) | NHS [code] | Social proof | Only with real verification; otherwise left out | Nice |
| 78 | Interactive site map (lot plan) | NHS [code] | Picks a building or lot | A buildings plan with availability per building | Should |
| 79 | Community amenity chips | RF, Z, NHS [code] | Lifestyle at a glance | Lobby, gym, pool, garden, children's room | Must |
| 80 | "Guests who stayed here loved" (review snippets) | B [code] | Real voices | Buyer quotes only with consent | Nice |
| 81 | Highlights with evidence ("Rated 9.0 by guests") | B [code] | A claim with proof | "Near the light rail: 350 m", always with the number | Nice |
| 82 | Policies and "The fine print" | B [code] | No surprises | Payment terms, index linkage, delivery date, delay compensation | Should |
| 83 | FAQ per page plus FAQPage schema | B, RE [code] | Fast answers; rich results | Project and city FAQs built from live data | Must |
| 84 | Alternatives ("Still looking?", nearby communities, similar homes) | B, RF [code] | No dead end | "פרויקטים דומים באזור" ("similar projects nearby") | Must |
| 85 | "Are you a builder? Advertise" on the consumer page | RF [code] | — (earns money) | "יזם? פרסמו את הפרויקט" ("developer? advertise your project"), linked to /marketing/ | Must |
| 86 | Street View button | RE [code] | Sees the street | A Street View deep link | Should |
| 87 | Commute module | RF [code] | Daily time | Travel time to TLV centre, Herzliya Pituach, Bnei Brak, Jerusalem | Should |
| 88 | Outbound "View builder website" | Z [code] | Transparency | Link to the developer's site as the source | Should |
| 89 | Inline confirmation "Your free brochure has been sent" | NHS [code] | Feedback | The thank-you state stays on the page | Must |
| 90 | Freshness in the title tag ("updated prices 2027") | B [code] | Click-through from Google | "מחירון מעודכן נובמבר 2026" ("price list updated November 2026"), only when the data changed | Should |

## D. Personalisation
| # | Feature | Who has it | What it does for the buyer | Fit | Priority |
|---|---|---|---|---|---|
| 91 | Save search plus alerts: Instantly / Daily / Every 3 days / Every 7 days | RM [fetch]; Z, RF, NHS save search [code] | Hears about new matches | Email or WhatsApp alerts, with a choice of frequency | Must |
| 92 | Favourites / wishlists | all [code]; named lists on B [prior] | Shortlist | "הרשימה שלי" ("my list"), shareable with a partner | Must |
| 93 | Hide | Z, RF, RE [code] | Cleaner results | Local hide | Nice |
| 94 | Recently viewed | Z, B [prior] | Goes back fast | A "נצפו לאחרונה" ("recently viewed") strip | Should |
| 95 | Price-drop alert on a saved item | Z, RF [prior]; B app [prior] | Catches the moment | Ties to the live price alert (HAD-684), only on real price-list drops | Must |
| 96 | Early access: Private Exclusive → Coming Soon → Public | C [fetch], RF badges [code] | First in line | "הרשמה מוקדמת לפני השקה" ("early registration before launch") on pre-marketing projects | Must |
| 97 | Sign-in nudge that states the gain ("save 10%") | B [code] | A reason to sign in | "שמרו והשוו בין מכשירים" ("save and compare across devices"), with no fake discount | Nice |
| 98 | Compare projects side by side | C collections, B [prior] | Decides between two or three | The decision tool (HAD-642) on up to 3 projects | Should |
| 99 | Shared boards between a buyer and an agent (Collections) | C [prior] | Joint decisions | Share "our list" with a partner or a lawyer | Nice |

## E. Trust and lead capture
| # | Feature | Who has it | What it does for the buyer | Fit | Priority |
|---|---|---|---|---|---|
| 100 | Source on every data row ("Source: Highland Homes", "Provided by Zillow") | Z, RF [code] | Believes the data | "מקור: מחירון היזם, 3.11.2026" ("source: the developer's price list, 3.11.2026") | Must |
| 101 | "Report a problem" per row | Z [code] | Fixes errors | A form that writes to the owner's mail | Must |
| 102 | Broker or source line ("Brokered by", "Listing provided by") | RE, Z [code] | Knows who is behind the listing | "משווק: [יזם / משרד]" ("marketed by: [developer / office]"). The site itself is never a broker. | Must |
| 103 | Security centre (fraud) | RM [fetch] | Safety | "Never pay a deposit outside bank escort" | Should |
| 104 | Fair-housing or legal statement | RF [code] | Fairness | The accessibility statement | Nice |
| 105 | AI disclaimer on AI tools | RM [fetch] | Honest AI | Required whenever AI suggests | Must |
| 106 | Verified-reviews explainer | B [code] | Trusts reviews | Only if reviews are introduced | Nice |
| 107 | Consent text ("Consent is not a condition …") | C [fetch] | Privacy | The lead-form notice (privacy law) | Must |
| 108 | Enquiry intents as checkboxes (price list / plans / visit) | D [prior] | One clear form | Checkbox intents | Should |

## F. SEO, data and performance
| # | Feature | Who has it | What it does for the buyer | Fit | Priority |
|---|---|---|---|---|---|
| 109 | Link blocks to nearby cities, neighbourhoods and ZIP codes "with new homes" | Z, RF [code] | Finds the next area | Cities and neighbourhoods "with new projects" | Must |
| 110 | FAQ built from live data (median price, days on market, active count) | RE [code] | Fast answers | "כמה פרויקטים חדשים יש בחולון?" ("how many new projects are in Holon?"), answered with live numbers | Must |
| 111 | City facts block (median price, ₪/sqft, active listings, rent) | RE [code] | Context | City ₪/m², projects in marketing, immediate-occupancy count | Must |
| 112 | "How to buy in [city]" guides | RF, RE [code] | Learns the process | Links to /buying-apartment/ and the mortgage universe | Should |
| 113 | A separate communities hub per city (`/newhomecommunities/{City}`) | RE [code] | A clear entry point | City hubs under /projects/ (slugs only through `url_word_audit.py`) | Must |
| 114 | Builder name inside the community slug | NHS [code] | Search match | **Report only.** Existing slugs are never renamed (no redirects). | Nice |
| 115 | Schema: RealEstateListing + Offer + Event (open house) + FAQPage + BreadcrumbList + ItemList; HomeAndConstructionBusiness for the developer | Z, RE, RF, NHS [code] | Rich results | ItemList on the hub; RealEstateListing / Offer / Event on projects | Must |
| 116 | Native lazy loading below the fold (RF 48/72, B 29/30, NHS 42/66) | [code] | Speed | Lazy below row 1; LCP image eager | Must |
| 117 | Numbered, crawlable pagination (RM 1–42) versus "Load more" (C) | RM [fetch], C [code] | Crawlable depth | Numbered pages plus "load more" for people | Must |
| 118 | Filter-path URLs set to noindex (Z /new-construction/) | Z [code] | — | **Owner decision only. Never add noindex without his order.** Report only. | Nice |
| 119 | Advertisements interleaved and labelled ("Advertisement") | RE [code] | — (earns money) | Labelled developer advertisements in the grid | Should |
| 120 | Mortgage-in-principle partner box | RM [fetch] | Next step | Partner bank or mortgage adviser (earns money) | Should |
| 121 | Moving and services estimates ("Get estimates") | RE [code] | Next step | Movers, lawyer, appraiser | Nice |

## G. Map and "near me"
| # | Feature | Who has it | What it does for the buyer | Fit | Priority |
|---|---|---|---|---|---|
| 122 | "Search this area" after panning | M [prior]; RF / NHS map [code] | A calm map | "חפש באזור הזה" ("search this area") | Must |
| 123 | "Near me" through location permission, with a typed fallback | M [prior] | One tap | A sort option and chip. **No floating button.** | Must |
| 124 | Price-labelled pins (name plus one fact), not numbered dots | Z, RF [prior]; M [prior] | Reads the map | "מגדלי X · מ-₪2.9M" ("Towers X · from ₪2.9M") (Ben's taste rule) | Must |
| 125 | Pins and cards stay in sync | Z, RF, M [prior] | Where and what, together | Hover or tap sync | Must |
| 126 | Bottom sheet with three heights on mobile | M [prior] | One-hand use | Peek / half / full list over the map | Should |
| 127 | Look Around / Street View | M [prior] | Sees the street | Deep link | Should |
| 128 | Travel-time search | RE [prior] | Commute-first search | "Up to 30 minutes from my work" | Nice |
| 129 | One-tap directions to the sales office | M [prior] | Turns interest into a visit | Waze and Google deep links | Must |

**Total: 129 micro-features.** By priority: 64 Must, 44 Should, 21 Nice (counted by script).
