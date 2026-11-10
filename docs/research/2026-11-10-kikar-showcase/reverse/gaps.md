# Gaps: what the leaders have that our Kikar page lacks or only half has

Page checked: https://nad-lan.co.il/projects/hamedina/ (release 1.72.630) on 10.11.2026, desktop 1024x768 and phone 375x812, in the built-in browser. Full rows, evidence links and the exact check for each row are in `features.csv` (same folder); the ids below point there.

**Count:** 77 rows absent and 68 partial, out of 211 rows that apply to this page (10 rows do not apply: rentals, hotel cancellation, sales-gallery kiosks).

**How the ranking works:** buyer value is a 1-5 judgement for someone choosing an apartment in these towers (5 = changes the choice or the price; 1 = nice to have). The top 10 are bundles of related rows, ranked by that value and by how many leaders already do it. Rows after the top 10 are sorted by value, then absent before partial.

**Owner rules that shape the ideas:** no fake urgency or public traffic counters; unknown values are omitted or written as 'לא פורסם'; renders and simulations stay labelled; the site is never a broker or the developer; no redirects; no indexing changes.

## The 10 most valuable gaps

### 1. Link to one apartment, and share it

- **Rows:** F157 (absent), related F161, F169. Buyer value 5/5.
- **Who has it:** Maverick Frame selector, Airbnb, Matterport.
- **Evidence:** https://maverickframe.com/services/interactive-apartment-selector/ ('Every apartment has its own link', claimed, 2026-11-10).
- **Our page today:** URL unchanged after selecting tower C, floor 30, SW unit; state kept only in localStorage.
- **How it would look on our page:** Each unit state gets a URL (?tower=C&floor=30&unit=SW&style=wood) that reopens it.
  - F161 Share sheet with copy link and messaging apps: 'שיתוף' button opening the phone share sheet with a link to the exact unit.
  - F169 Share a link to the exact viewpoint: Copy-link inside the 360 that reopens the same scene and angle.

### 2. Real floor plans per unit type with room sizes

- **Rows:** F022 (partial), related F024, F023, F002, F028. Buyer value 5/5.
- **Who has it:** Rightmove, Zoopla, Property Finder, ImmoScout24, Idealista, Zillow, Lennar, Toll Brothers, Matterport, Compass.
- **Evidence:** https://www.rightmove.co.uk/properties/94044159 ('PM_Apt81_Floorplan B', live, 2026-11-10).
- **Our page today:** schematic key plan ('תוכנית סכמטית: 4 דירות פינתיות בקומה טיפוסית') and schematic example plan only.
- **How it would look on our page:** Real plan image per type from published listings, labelled with source; keep the schematic until then.
  - F024 Room dimensions and total area on the floor plan: Room sizes on a plan per type once a source exists (permit file or listings), with the source named.
  - F023 Floor-plan directory for every unit or floor in the building: A plan directory by line and floor band, each plan with its source and date.
  - F002 3D floor plan per unit type: 3D extruded plan of each corner type, toggled from the key plan.
  - F028 Units named by direction with a PDF plan per unit: Name each line by direction and attach its plan when found.

### 3. Dated listings shown on the tower: which units are for sale, at what asking price

- **Rows:** F036 (partial), related F035, F039, F041, F051, F038. Buyer value 5/5.
- **Who has it:** Compass, Toll Brothers, Zillow, Apartments.com, REALS (Simplex 3D), BMBY 3D, Maverick Frame selector, SeLoger Neuf, Idealista, Emaar.
- **Evidence:** https://www.compass.com/building/the-henry-manhattan-ny/1633466331737096645/ ('$4,273/sf Avg.', live, 2026-11-10).
- **Our page today:** price block 'מחירון · עודכן 7.10.2026', table columns הנכס / ₪ למ״ר / מחיר הדירה, ₪ / הנתון / מועד lists 3 asking-price rows marked 'מודעה' (floor 12 10.3M, penthouse floor 39 43M, rights 148 m² 6.3M, all 4.2025).
- **How it would look on our page:** Pin dated listings on the key plan: 'מודעה · מחיר מבוקש · תאריך · מקור', grey where unknown.
  - F035 Live unit availability synced to stock, with plans and 360: Daily-checked listing feed shown on the plan with the check date.
  - F039 Availability colours on the floor plate: Key plan quadrants coloured by 'עסקה' / 'מודעה' / 'לא ידוע'.
  - F041 Live count of units still available: 'מודעות פעילות היום: N' counter from dated listings, with the check date.
  - F051 Site or building map coloured by availability: Colour floors on the 3D towers by number of dated listings (grey = none known).
  - F038 Active / Past Sales / Past Rentals tabs: Tabs 'עסקאות' / 'מודעות' / 'שכירות' above one table, each tab with its source.

### 4. Monthly payment and the full buying cost next to the estimate

- **Rows:** F078 (absent), related F059, F077, F055, F062. Buyer value 4/5.
- **Who has it:** Redfin, Zillow, Compass, Lennar, Property Finder, Zoopla, ImmoScout24, Yad2 / Yad1, Realtor.com, Homes.com.
- **Evidence:** https://www.redfin.com/FL/Miami/725-NE-24th-St-33137/unit-3301/home/190141269 ('See my rate', live, 2026-11-10).
- **Our page today:** not found: page text and every visible control searched for 'בחודש' line next to the price (1024x768).
- **How it would look on our page:** One line under the estimate: 'כ-X ₪ בחודש במשכנתא של 75%' with 'איך חישבנו'.
  - F059 Payment calculator split with HOA dues line: Monthly card: mortgage + arnona + management fee 'לא פורסם' + insurance.
  - F077 Inline mortgage calculator with editable deposit, rate and term: Inline down payment, rate and term fields prefilled from the estimate.
  - F055 Total purchase cost with taxes and fees itemised: Itemise lawyer (about 0.5% + VAT), brokerage (about 2% + VAT), appraiser and mortgage fees under the total.
  - F062 Total price for the whole stay as the headline price: Put 'סה״כ כולל מס רכישה' as the first number of the calculator result.

### 5. Compare two units side by side

- **Rows:** F159 (absent), related F173. Buyer value 4/5.
- **Who has it:** Lennar, Vrbo, Maverick Frame selector, Expedia / Hotels.com.
- **Evidence:** https://www.lennar.com/new-homes/florida/miami/miami/greenview-at-presidential ('10 homes available', live, 2026-11-10).
- **Our page today:** not found: page text and every visible control searched for compare ('השוו') (1024x768).
- **How it would look on our page:** Compare 2 units: view, sun hours, eye height, ₪/m² estimate, side by side.
  - F173 AI side-by-side compare of shortlisted properties: Later, on top of the compare tool.

### 6. Travel time to my own places

- **Rows:** F102 (absent). Buyer value 4/5.
- **Who has it:** Apartments.com, Realtor.com, Rightmove, Domain.
- **Evidence:** https://www.rightmove.co.uk/properties/92765910 ('__mins driving to your place', live, 2026-11-10).
- **Our page today:** not found: page text and every visible control searched for 'הוסיפו מקום' / travel time to my address (1024x768).
- **How it would look on our page:** 'כמה זמן לעבודה?': add an address, see walk / transit / drive minutes.

### 7. Real photographed view at floors 20, 30 and 38

- **Rows:** F016 (absent). Buyer value 4/5.
- **Who has it:** Waldorf Astoria Residences Miami.
- **Evidence:** https://www.waldorfresidencesmiami.com/view/ ('VIEW FROM THE TOP', prior, 2026-11-10).
- **Our page today:** views are simulations ('מה בתמונה להמחשה'); 'צילום אמיתי' appears only in the site menu, not in this page body.
- **How it would look on our page:** Drone panoramas at floors 20 / 30 / 38 per direction, chip 'צילום אמיתי · תאריך', simulation as fallback.

### 8. Save several units, share the list, add notes

- **Rows:** F168 (partial), related F170, F176. Buyer value 3/5.
- **Who has it:** Airbnb, Compass, Rightmove.
- **Evidence:** https://www.airbnb.com/rooms/17674545 ('Save to wishlist', live, 2026-11-10).
- **Our page today:** dialog .nlbk opened from 'לסל הדירה: המחיר המלא, הצוות והנציג' keeps one selection: 'הסל נשמר רק בדפדפן הזה' (localStorage nl-basket:hamedina).
- **How it would look on our page:** Heart on each chosen unit; 'הרשימה שלי' holds several.
  - F170 Shared list with partner or agent (collaborative board): Share 'הרשימה שלנו' (several units) by link with a partner or lawyer.
  - F176 Notes on saved listings: A note field per saved unit.

### 9. Noise and environment data for the towers

- **Rows:** F113 (absent), related F119, F117, F118, F120. Buyer value 3/5.
- **Who has it:** Redfin, Homes.com, Realtor.com.
- **Evidence:** https://www.redfin.com/FL/Miami/725-NE-24th-St-33137/unit-3301/home/190141269 ('Silent zone', live, 2026-11-10).
- **Our page today:** not found: page text and every visible control searched for noise ('רעש') (1024x768).
- **How it would look on our page:** Road-noise layer from the municipal noise map; ring road and Weizmann traffic named.
  - F119 Noise indicator with heat-map overlay of sources: Noise as a map layer chip.
  - F117 Flood Factor with 30-year probability: Flood note from the municipal drainage map, if published.
  - F118 Heat Factor with hot-day count: Heat note per facade from the sun model (west-facing afternoon sun).
  - F120 Wind Factor (storm-wind chance): Wind exposure note for high balconies, only from a published study.

### 10. Empty-apartment mode and a ruler in the 360

- **Rows:** F005 (absent), related F009. Buyer value 3/5.
- **Who has it:** Matterport.
- **Evidence:** https://matterport.com/blog/matterports-winter-2025-release-productivity-multiplied ('present the Matterport 3D tour to visitors fully unfurnished', press, 2026-11-10).
- **Our page today:** not found: page text and every visible control searched for 'ללא ריהוט' / empty apartment (1024x768).
- **How it would look on our page:** Add a fifth style chip 'דירה ריקה' in the 360 style list.
  - F009 Measurement tool in the 3D tour: A ruler in the 360 that shows published sizes, e.g. balcony area, marked 'לדוגמה'.

## All other gaps, by buyer value

| Id | Area | Feature | Status | Value | Who has it | Idea for our page |
|---|---|---|---|---|---|---|
| F025 | plan | Interactive floor plan that pins every photo to its spot | partial | 4 | Zillow | Pin the 360 scenes on the example plan; tapping a pin opens that room. |
| F027 | plan | Unit-type table with size, price and plan column | partial | 4 | Bayut; Madlan; Yad2 / Yad1 | Unit-type table: type, m² range, rooms, deals range, plan thumbnail when available. |
| F042 | inventory | Per-unit row with floor, orientation, balcony and parking | partial | 4 | SeLoger Neuf | Per-unit card: floor, facing, balcony m², parking, storage, each with source or 'לא פורסם'. |
| F043 | inventory | Unit-type table with area, view and bed per row | partial | 4 | Booking.com | Table of the 4 corner types: facing, view chips, sun hours, m² range. |
| F058 | price-cost | Monthly service / common charges as a field | partial | 4 | Compass; Bayut; Property Finder; Rightmove; Zoopla | Monthly-costs line with 'דמי ניהול: לא פורסם' and arnona estimate from the city tariff. |
| F125 | building-amenities | Specification / included features grouped by room | partial | 4 | Lennar; Yad2 / Yad1; Madlan; Idealista | Spec table split by kitchen / rooms / building, each item with source. |
| F133 | contact-booking | Tour sheet that offers the earliest free slot as one tap | partial | 4 | Zillow; Compass | Show the first free slot as one button: 'שיחה היום ב-15:00'. |
| F160 | decision-tools | Deals in the same building, by rooms, in-project vs nearby | partial | 4 | Bayut; Property Finder; Madlan | One deals table with tabs 'בפרויקט' / 'בסביבה' and filters for rooms and year. |
| F186 | trust | Local legal-protections module on the listing | partial | 4 | Zillow | Block 'ההגנות שלכם': Sale Law guarantee, escrow account, warning note, in plain Hebrew. |
| F006 | 3d-tour | Dollhouse view (whole unit in 3D) | absent | 3 | Matterport | A cut-away 3D model of the example apartment, toggled from the 360 viewer, labelled 'הדמיה'. |
| F063 | price-cost | Average yearly rent for this unit | absent | 3 | Bayut | Rent of comparable new towers nearby, labelled as a proxy, until the towers have rents. |
| F067 | price-cost | Price tracking alerts | absent | 3 | Expedia / Hotels.com | 'עדכנו אותי על מחירים בכיכר' that fires on a new deal or listing in the towers. |
| F080 | finance | BuyAbility tag and payment on every listing | absent | 3 | Zillow | After the buyer runs the site mortgage calculator, label the estimate 'בתקציב שלכם' / 'מעל'. |
| F106 | schools | School catchment zone on the listing | absent | 3 | Domain; Rightmove | Tel Aviv school registration zone for the towers' addresses, with the municipal source. |
| F144 | contact-booking | Sales office and Email all Agents | absent | 3 | Compass | Show the brokers who list units in the towers, labelled 'מודעה בתשלום' if paid. |
| F136 | contact-booking | AI or chat assistant answering questions about this property | absent | 3 | Toll Brothers; Realtor.com; Rightmove; ImmoScout24; realestate.com.... | Assistant that answers from the page's own facts, with an AI notice. |
| F142 | contact-booking | Personal buyer link or QR code | absent | 3 | REALS (Simplex 3D) | 'קישור אישי' that the rep sends; it opens the buyer's saved tower, floor, style and basket. |
| F154 | video-call | Instant call with sales from the project page | absent | 3 | Emaar | 'זמין עכשיו' state in office hours that starts a WhatsApp video call at once. |
| F166 | decision-tools | Offer Insights: offer-strength chips with acceptance likelihood | absent | 3 | Zillow | Not planned without data. |
| F216 | mobile-pattern | Sticky selection basket bar on mobile | absent | 3 | Booking.com | A small basket badge in the sticky bar ('הסל: מגדל C · 30 · דרום-מערב'). |
| F217 | mobile-pattern | Swipe hero gallery with photo counter | absent | 3 | Airbnb; Booking.com | A swipe gallery of real site photos and renders, each chip-labelled 'צילום אמיתי' or 'הדמיה', with '1 / N'. |
| F008 | 3d-tour | Interactive 3D tour linked to the floor plan | partial | 3 | realestate.com.au | Tap a room on the plan of the example apartment to jump to that room's 360. |
| F011 | 3d-tour | Walk-through mode inside the scan | partial | 3 | Matterport | Add step points between living room, bedroom and balcony inside the 360. |
| F018 | media | Media chips on the hero (photos, video, 3D, plan, street view) | partial | 3 | Compass; Redfin; Lennar; Zillow; Zoopla; Rightmove; Apartments.com | A media chip row under the H1: '360 · 8 חללים', 'סרט 1:30', 'תוכנית סכמטית', 'מפה'. |
| F019 | media | Video per residence line with floor range | partial | 3 | Toll Brothers | Short clip per corner line (NE, SE, SW, NW) showing the view change by floor. |
| F029 | plan | Finish or upgrade packages with their price | partial | 3 | Toll Brothers; KB Home; Maverick Frame selector; Zaha Hadid Archite... | Show an indicative cost range per style, from the designer directory, labelled 'הערכה'. |
| F030 | plan | Floor plan view from the 3D tour | partial | 3 | Matterport | Top-down plan of the example apartment, synced with the 360 position. |
| F045 | inventory | Filter units by tier or line | partial | 3 | Compass | Filter the deals and listings table by line (NE / SE / SW / NW) and floor band. |
| F048 | inventory | Pricing & Floor Plans with floor selector and move-in filter | partial | 3 | Apartments.com | Floor chips that list dated listings on that floor. |
| F047 | inventory | Other units in the same project | partial | 3 | ImmoScout24; Idealista | Carousel of other dated listings in the towers under the chosen unit. |
| F044 | inventory | Construction progress percent | partial | 3 | Bayut | Construction-progress line with a dated source; no percent unless published. |
| F046 | inventory | Floor hover shows free units and starting price | partial | 3 | Maverick Frame selector | When a floor is chosen, show 'מודעות פעילות בקומה הזו: N' from dated listings. |
| F065 | price-cost | Past sales with original price, % change and public-record check | partial | 3 | Compass | Show change since the previous sale of the same unit when the official file has it. |
| F069 | price-cost | RealEstimate: three provider estimates | partial | 3 | Realtor.com | Keep sources side by side; add the official neighbourhood median as a second reference line. |
| F064 | price-cost | Parking space priced separately | partial | 3 | ImmoScout24 | Parking and storage included or priced, per listing, with source. |
| F082 | finance | Zillow Home Loans pre-qualify link beside the payment estimate | partial | 3 | Zillow | 'אישור עקרוני' route to the site's mortgage-adviser directory. |
| F079 | finance | Builder-mortgage payment estimate and buying-power calculator | partial | 3 | Lennar; Toll Brothers | Buying-power mini form inline: income and equity to a max price. |
| F081 | finance | Developer payment terms and bank guarantee in project updates | partial | 3 | Madlan; Yad2 / Yad1 | A short 'תנאי תשלום וערבויות' block in the page body, not only in the basket. |
| F096 | location-map | Walk, bike and transit scores out of 10 | partial | 3 | Redfin; Zillow; Homes.com | A 'הליכה' summary: places within 5 / 10 / 15 minutes, with counts, no invented score. |
| F094 | location-map | Look Around: 360 street-level 3D walk | partial | 3 | Apple Maps | 'Street View' link on the map for the ring road. |
| F105 | schools | Nearby and assigned schools with rating and distance | partial | 3 | Redfin; Compass; Zillow; Homes.com; Realtor.com; Rightmove | Schools list with type, grades and walking minutes; no ratings. |
| F112 | environment | Flood risk, crime and planning applications after sign-in | partial | 3 | Zoopla | Name each plan's status and date in its pin. |
| F111 | environment | Construction sites nearby with expected end date | partial | 3 | Madlan | Add expected completion per nearby site, with source. |
| F130 | building-amenities | Safe-room badge | partial | 3 | Yad2 / Yad1; Madlan | Chip 'ממ״ד' in the unit card when the listing states it. |
| F137 | contact-booking | Ask a local expert with preset question chips | partial | 3 | Redfin; NewHomeSource; Booking.com | Question chips that prefill WhatsApp: 'מה המחיר בקומה 30?', 'מתי האכלוס?', 'מה דמי הניהול?'. |
| F140 | contact-booking | Named on-site sales rep, sales hours and directions | partial | 3 | Toll Brothers; Lennar | Rep name, photo and hours next to the WhatsApp bar. |
| F138 | contact-booking | Call, request details and email buttons | partial | 3 | Rightmove; Zoopla | Add 'שיחה' (tel:) and 'מייל' next to WhatsApp. |
| F143 | contact-booking | Register interest on an off-plan project | partial | 3 | Bayut; Property Finder; Compass | 'עדכנו אותי על כיכר המדינה' for new deals or listings in the towers. |
| F141 | contact-booking | Named sales agent with hours and six contact channels in one panel | partial | 3 | Gindi (developer, Israel) | One contact card: rep name, hours, WhatsApp, phone, video. |
| F156 | video-call | Video call with a shared live tour and joint measuring | partial | 3 | Floorfy | Shared session: the rep moves the 3D world and the buyer sees it live. |
| F163 | decision-tools | Market insights: days on market, sale-to-list, price drops | partial | 3 | Redfin | Days on market for tracked listings, once we track them. |
| F172 | decision-tools | Sold-nearby table with filters and an honest empty state | partial | 3 | Yad2 / Yad1 | Filters for rooms, year and distance. |
| F167 | decision-tools | Price trend chart: building vs community | partial | 3 | Property Finder; Bayut | Line chart: towers' deals vs radius median by year. |
| F196 | trust | Price history row with source and Report a problem | partial | 3 | Zillow | 'דווחו על טעות' link per row that opens a prefilled WhatsApp or mail. |
| F195 | trust | Permit, licence or offering-plan numbers shown | partial | 3 | Toll Brothers; Bayut; Property Finder; Yad2 / Yad1 | Permit number with a link to the municipal file. |
| F192 | trust | Fraud and security notice for buyers | partial | 3 | Rightmove | One-line fraud notice near the WhatsApp bar. |
| F215 | mobile-pattern | Sticky bottom reserve bar on mobile | partial | 3 | Airbnb | Show the chosen unit and its estimate in the sticky bar after a selection. |
| F052 | inventory | True-inventory scarcity per unit type | absent | 2 | Booking.com; Expedia / Hotels.com | Only if a real dated list exists: 'N מודעות פעילות בקו הזה'. |
| F070 | price-cost | Dated price reduction or strike-through with stated basis | absent | 2 | Zoopla; Rightmove; Airbnb; Vrbo; Expedia / Hotels.com | When a tracked listing drops, show the old and new price with both dates. |
| F072 | price-cost | Price-history insight badge ('below the 60-day average') | absent | 2 | Airbnb | Badge 'מתחת לממוצע העסקאות במגדלים' on a listing price, only from dated data. |
| F084 | finance | Default interest rate tied to a named public source | absent | 2 | Yad2 / Yad1; ImmoScout24 | Show the Bank of Israel average rate with its date in the inline calculator. |
| F086 | finance | Off-plan payment plan ratio in the header | absent | 2 | Bayut; Property Finder | Payment terms per listing when the ad states them. |
| F088 | finance | Payment plan split into milestones | absent | 2 | Bayut; Property Finder; Sobha; Omniyat; DAMAC | Milestone schedule per listing when published. |
| F085 | finance | Lender check: will a bank lend on this property | absent | 2 | Rightmove | Note whether banks lend on rights before Form 4, with source. |
| F087 | finance | Online pre-reservation of a specific home with a small fee | absent | 2 | St Modwen Homes | Keep as is; offer 'שריון מול הנציג' only through the seller's channel. |
| F097 | location-map | Crime score for the listing area | absent | 2 | Homes.com | Only with an official source (Israel Police open data), by area. |
| F100 | location-map | What Locals Say neighborhood polls | absent | 2 | Trulia | Short resident quotes with consent, later. |
| F099 | location-map | One-tap directions to the site or sales centre | absent | 2 | Toll Brothers; Google Maps; Apple Maps | 'ניווט לכיכר' with Waze and Google Maps deep links. |
| F116 | environment | Energy certificate / rating | absent | 2 | Zoopla; Rightmove; OnTheMarket; Idealista; ImmoScout24 | Green-building standard or energy label if the permit states it. |
| F115 | environment | Broadband / internet availability for the address | absent | 2 | OnTheMarket; Rightmove; Zoopla; ImmoScout24 | Fibre availability line for the addresses. |
| F131 | building-amenities | Resident reviews and star rating of the building | absent | 2 | Property Finder | After occupancy: resident ratings with verification. |
| F146 | contact-booking | Add a tour, open house or inspection to the calendar | absent | 2 | Zillow; Domain | 'הוספה ליומן' (.ics) on the booking confirmation. |
| F181 | decision-tools | Start an offer from the listing | absent | 2 | Redfin | Route 'הצעת מחיר' to the seller's broker only. |
| F179 | decision-tools | Printable flyer or brochure PDF | absent | 2 | Lennar; SeLoger Neuf; Rightmove; Property Finder; Idealista | 'הדפסה / PDF' of the chosen unit card with sources. |
| F178 | decision-tools | Official rent data next to sales | absent | 2 | nadlan.gov.il | Official rents of comparable nearby buildings, labelled as nearby. |
| F174 | decision-tools | Gross rental yield | absent | 2 | Madlan; nadlan.gov.il | Yield only when a rent source exists. |
| F180 | decision-tools | Real priced products and AR placement in your own room | absent | 2 | Houzz | Link styles to the site's apartment designer tool with priced items. |
| F198 | trust | Category review scores | absent | 2 | Airbnb; Booking.com | Only verified buyer reviews, later. |
| F200 | trust | Host response rate and response time | absent | 2 | Airbnb | 'זמן מענה ממוצע' only if measured. |
| F207 | accessibility | Accessibility features of the home | absent | 2 | Rightmove; ImmoScout24; Yad2 / Yad1; Airbnb | Accessibility line: lifts, step-free entry, parking, per the permit. |
| F212 | language | Agent's spoken language shown | absent | 2 | Property Finder | 'שיחה בעברית, English, Русский, Français, العربية' on the booking card. |
| F021 | media | Before/after slider and re-roll on a staged photo | partial | 2 | Zillow | Split-screen slider between 'העיצוב המקורי' and a chosen style. |
| F031 | plan | 'Where you'll sleep' bedroom cards | partial | 2 | Airbnb | Room cards (living, 3 bedrooms, balcony) with sizes when known. |
| F032 | plan | Schematic floor plan with furniture on/off and languages | partial | 2 | Matterport | Furniture on/off switch on the example plan. |
| F071 | price-cost | Lease length, ground rent and next ground-rent review | partial | 2 | Zoopla; Rightmove; OnTheMarket | One line on how the units will be registered, with source, or 'לא פורסם'. |
| F083 | finance | Building financial policies (minimum down payment) | partial | 2 | Compass | - |
| F098 | location-map | Map and list stay in sync (pin raises card) | partial | 2 | Airbnb; Booking.com; Expedia / Hotels.com; Vrbo | Tapping a list row highlights its pin and the reverse. |
| F149 | contact-booking | Tour request with up to 3 preferred dates | partial | 2 | Realtor.com | Allow up to 3 preferred slots. |
| F148 | contact-booking | Public Q&A or 'ask the developer' after the FAQ | partial | 2 | Yad2 / Yad1; Property Finder; Booking.com | 'לא מצאתם תשובה? שאלו' under the FAQ, opening WhatsApp. |
| F147 | contact-booking | Preferred contact method in the lead form | partial | 2 | NewHomeSource | Channel choice in the video-call form: WhatsApp / phone / email. |
| F177 | decision-tools | Official deals at the address with block/parcel and repeat-sale change | partial | 2 | nadlan.gov.il | Show gush/helka when public and the change since the last sale. |
| F203 | trust | Verified-listing badge with validation date | partial | 2 | Bayut; Property Finder | 'נבדק ב-[date]' on each data block. |
| F202 | trust | Registry-validated fields block | partial | 2 | Bayut | Registry-checked fields with a date once checked. |
| F201 | trust | Order the official land-registry extract | partial | 2 | nadlan.gov.il | 'הפקת נסח טאבו' link next to the addresses. |
| F218 | mobile-pattern | Section anchor tabs | partial | 2 | Bayut | Sticky section chips under the header: מחיר · תלת ממד · מפה · עסקאות · שיחה. |
| F013 | 3d-tour | VR mode in the headset browser | absent | 1 | Matterport | WebXR 'VR' button in the 360 viewer for headset browsers. |
| F033 | plan | Interactive floor plan with structural options | absent | 1 | KB Home | Not planned: owners already ordered their changes. |
| F053 | inventory | 'Rare find' availability note | absent | 1 | Airbnb | Not recommended (urgency rule). |
| F075 | price-cost | Utilities line the buyer can add | absent | 1 | Redfin | Optional utilities line in the monthly card. |
| F089 | finance | Limited-time rate badge on the project header | absent | 1 | Toll Brothers | Only with a real dated lender offer. |
| F101 | location-map | Street-level imagery by date ('See more dates') | absent | 1 | Google Street View / Earth | Before/after aerial of 2010 vs 2026 next to the timeline. |
| F104 | commute | Route preview with traffic and air-quality by time | absent | 1 | Google Maps Immersive View | Not planned. |
| F121 | environment | Climate risk now vs 15 and 30 years out | absent | 1 | Realtor.com | Not planned. |
| F122 | environment | Mobile signal by network | absent | 1 | OnTheMarket | Not planned. |
| F123 | environment | Weather preview in the 3D view | absent | 1 | Google Maps Immersive View | Not planned. |
| F152 | contact-booking | Inspection planner with display-suite hours | absent | 1 | realestate.com.au; Domain | Not planned. |
| F185 | decision-tools | Public views and saves counters | absent | 1 | Redfin; ImmoScout24; Idealista | Not planned (owner rule). |
| F184 | decision-tools | Hot Home banner | absent | 1 | Redfin | Not planned (urgency rule). |
| F182 | decision-tools | Buyer engagement tracking (views, time, shares) | absent | 1 | REALS (Simplex 3D) | Rep dashboard only, never public. |
| F183 | decision-tools | Feedback on the page itself | absent | 1 | Booking.com | 'האם הדף עזר?' at the end. |
| F206 | trust | Guest favourite badge (top-rated, reliable homes) | absent | 1 | Airbnb | Not planned. |
| F210 | accessibility | Verified accessibility with photos and 3D scan | absent | 1 | Airbnb | Not planned before occupancy. |

## Not planned on purpose

Some absent rows conflict with the owner's rules and are listed so nobody builds them by accident: public view and save counters (F185), demand banners such as Hot Home and 'usually booked' (F184, F053), selling or reserving the unit on the site (F087). They count as absent in the coverage figures.
