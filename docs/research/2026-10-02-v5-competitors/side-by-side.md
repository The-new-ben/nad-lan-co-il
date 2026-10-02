# V5: competitors side by side, the Kikar Hamedina page against the best new-build presentations

Read on 2.10.2026. Loop item V5. Research only: no forms were filled, nothing was signed up for, no cookies were accepted, and nothing was downloaded. The PDFs and brochures were noted but not opened.

## How this was checked

- **Phone width:** every page was loaded in Chrome emulating a 390x844 phone (Playwright, headless, `channel="chrome"`). For each page I recorded the visible text, the HTML keyword hits, the iframes, the hreflang tags and the timing.
- **Bot walls:** Zillow, Madlan and Emaar's project page were blocked or redirected in headless mode (Zillow and Madlan show a "Press & Hold"/robot check, and Emaar's old `properties.emaar.com` URL redirects to the homepage). I read those three in the owner's normal Chrome instead. I did not solve or bypass any challenge. Those pages have no phone timing.
- **What "speed" means here:** these are time to DOMContentLoaded and to the load event, measured on a desktop broadband line with phone emulation and no throttling. They are rough. The transfer size is a lower bound, because cross-origin resources often report 0 bytes.
- **Our own page** was checked on the live site (release 1.72.394 in asset URLs). I opened "דירה לדוגמה: מגדל C, קומה 30, פונה מערבה" and then "היכנסו לדירה לדוגמה", and read the controls that appeared. Screenshots of both steps are in this folder.
- **Evidence labels in cells:** "yes" or "no" comes from what was on the page that day. "not found" means I looked and it was not there. "claimed" means vendor marketing text, not something I saw working.

### Pages read (all on 2.10.2026)

| Short name | Exact URL(s) read |
|---|---|
| **Ours: Kikar** | https://nad-lan.co.il/projects/hamedina/ and https://nad-lan.co.il/projects/hamedina-en/ (references checked: /projects/rainbow-tel-aviv/ and /projects/duo-tel-aviv/, both 200) |
| **Zillow** | Community page: https://www.zillow.com/community/one-wall-street-sales/458738705_zpid/ (found from https://www.zillow.com/manhattan-new-york-ny/new-homes/). Builder FAQ: https://zillow.zendesk.com/hc/en-us/articles/203865940-New-Construction-Listings-FAQ. Virtual Staging release (10.9.2025): https://zillow.mediaroom.com/2025-09-10-Zillow-brings-AI-powered-Virtual-Staging-to-Showcase-listings |
| **Matterport** | Winter 2025 release (Defurnish): https://matterport.com/blog/matterports-winter-2025-release-productivity-multiplied. Property Intelligence: https://matterport.com/news/matterport-launches-property-intelligence-transforming-real-estate |
| **Compass** | The Henry (new development, 2026): https://www.compass.com/building/the-henry-manhattan-ny/1633466331737096645/. One Thousand Museum, Miami: https://www.compass.com/building/one-thousand-museum-miami-fl/756397767420241325/. New-dev hub: https://www.compass.com/development/ |
| **Houzz** | https://pro.houzz.com/for-pros/feature-3d-floor-plan. View in My Room 3D: https://www.houzz.com/press/398/Houzz-App-Upgrades-3D-Augmented-Reality-Tool-with-ARKit-to-Help-You-Design-and-Shop |
| **REALS (Simplex 3D, Herzliya)** | https://www.simplex3d.com/reals/. Second Israeli platform: BMBY 3D at https://bmby.co.il/bmby-3d-%D7%A1%D7%91%D7%99%D7%91%D7%94-%D7%9E%D7%A9%D7%9C%D7%99%D7%9E%D7%94-%D7%9C%D7%9E%D7%A2%D7%A8%D7%9B%D7%AA |
| **Yad1 (Yad2)** | https://www.yad2.co.il/yad1/project/13671 (Bnei Efraim 236-240), https://www.yad2.co.il/yad1/project/11351 (Gallipolis, Yad Eliyahu), listing https://www.yad2.co.il/yad1/newprojects/tel-aviv-area?area=1&city=5000 |
| **Madlan** | https://www.madlan.co.il/projects/%D7%9E%D7%92%D7%A8%D7%A9_9_%D7%A4%D7%90%D7%A8%D7%A7_%D7%94%D7%97%D7%95%D7%A8%D7%A9%D7%95%D7%AA_%D7%AA%D7%9C_%D7%90%D7%91%D7%99%D7%91 (המגדל בחורשות, a developer-fed project) and https://www.madlan.co.il/projects/GINDI%20TOWERS%20%D7%94%D7%A9%D7%95%D7%A7%20%D7%94%D7%A1%D7%99%D7%98%D7%95%D7%A0%D7%90%D7%99 (Gindi TLV, "היזם לא סיפק מידע נוסף"). Madlan has no project page for the Kikar towers; it only has resale listings there. |
| **Gindi TLV (developer)** | https://gindi.com/online/ and https://gindi.com/ |
| **Ashtrom and Electra (Kikar, official)** | https://www.ashtrom.co.il/projects/kikar-hamedina and https://www.electra.co.il/%D7%90%D7%9C%D7%A7%D7%98%D7%A8%D7%94_%D7%91%D7%99%D7%9C%D7%93%D7%99%D7%A0%D7%92/%D7%A4%D7%A8%D7%95%D7%99%D7%A7%D7%98%D7%99%D7%9D/%D7%9E%D7%92%D7%93%D7%9C%D7%99_%D7%9B%D7%99%D7%9B%D7%A8_%D7%94%D7%9E%D7%93%D7%99%D7%A0%D7%94. Also read: Acro Tel Aviv Towers, https://acronadlan.com/project/tel-aviv-towers/ |
| **Waldorf Astoria Residences Miami (pre-construction)** | https://www.waldorfresidencesmiami.com/, /floor-plans/ and /view/ |
| **Emaar Creek Bay (Dubai, off-plan)** | https://www.emaar.com/en/properties/creek-bay-at-dubai-creek-harbour. Also read: Una Residences Brickell, https://www.unaresidencesmiami.com/ (now complete, immediate occupancy) |

## (a) The table

One line per cell. The last row is the most important one.

| Feature | **Ours: Kikar** | Zillow | Matterport | Compass | Houzz | REALS / BMBY 3D | Yad1 | Madlan | Gindi TLV | Ashtrom / Electra (Kikar) | Waldorf Miami | Emaar Creek Bay |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| **3D building model** | **Yes.** Three rotating towers in a city model from municipal GIS (2 canvases live) | No (not found on the community page) | No building; a captured interior "digital twin" only | No | No (3D rooms, not buildings) | **Yes** (claimed): building in a real 3D city model | No (not found on 2 project pages) | No | No (not found) | No | **Yes.** 3D tower in city context, "SELECT THE CUBE" | No (photo gallery) |
| **Pick unit by floor and direction** | **Yes.** Tower, then floor, then apartment by bearing (NE/SE/SW/NW), plus a schematic key plan | No; pick by plan ("Floor plan: 3505") | No | Partial: "Filter by unit or tier/line", and unit names carry direction (PHEAST, 14EAST) | No | **Yes** (claimed): "Unit selection by floor and direction" | No; by room count only | No; by apartment type | Partial: search wizard by rooms, size, type, price range | No | Partial: by cube (floor band), with up/down arrows | No; "Available Units 21" counter only |
| **Floor plan per unit** | Schematic only: "התוכנית להמחשה, חלוקת הדירות לא פורסמה" | **Yes**, a floor-plan image per plan | **Yes**, auto schematic plan with measurements (Property Intelligence) | **Yes**, "View available floor plans" | **Yes**, 2D and 3D plans (AI 2D→3D) | **Yes** (claimed): plans with live availability | **Yes**, per type ("תוכניות דירה 3 חד' 4 חד'") | **Yes**, a "תכניות דירה" column per type | Not verified | No | **Yes**, the floor-plans step after the cube | Not on this project (`floorPlanUpload: null`) |
| **Price per unit or range** | **Yes**, published: 9.58 to 10.63M ₪ deals, about 65K ₪/m², dated asking prices | **Yes**: "from $8,995,000", $3,123/sqft, Zestimate | n/a | **Yes**, exact price per unit plus $/sf plus "Contract Signed" | Product prices, then an estimate | **Yes** (claimed): "Pricing information" | **Yes**, "החל מ-3,215,000 ₪" per type | **Yes**, "החל מ-36,000 ש"ח למ"ר" and from 2,990,000 ₪ | Price-range filter only | **No** | **No** (no price on site) | **Yes**, "Starting Price AED 1.8 Mn" / "Prices from AED 3,252,888" |
| **Past deals or market data** | **Yes**: 3 tower deals by floor, area medians (Tax Authority 10.2023 to 10.2025), price tags on the map | **Yes**: Zestimate, estimated sales range, Rent Zestimate, market value | No | **Yes**, "Past Sales" and "Past Rentals" tabs for the same building | No | Not mentioned | **Yes**, "נכסים שנמכרו באזור" with room and year filters | **Yes, strongest**: "היסטוריית עסקאות, בפרויקט (14), בסביבה (1000)", filters for rooms, year, distance and ₪/m², plus yield | No | No | No | No |
| **360 of the apartment** | **Yes**: "סיור 360 בסלון · 3 סגנונות עיצוב", bedroom, balcony, day / sunset / evening | Not on this page (3D tours exist for resale via Zillow 3D Home) | **Yes**, the core product (needs a built, scanned unit) | Partial: "Virtual Tour" badges on units (Matterport in the HTML) | AR "Life-Sized Walkthroughs" | **Yes** (claimed): "Interactive 360° virtual tours" | Not found on sampled pages; a third-party summary claims "view from every window" (unverified) | Not found | No | No | Partial: "CLICK & DRAG TO LOOK AROUND" at the plan step | Not on the project page |
| **360 of amenities** | **Yes**: 360 lobby, pool and gym; spa and car-park buttons on the page | No | Only if scanned | Not found | No | Claimed: "Amenities highlighting" | No | No | No (Rooftop page has photos) | Text only (pool, gym, spa) | Not found (amenities page) | No (amenity list only) |
| **Design styles / furniture** | **Yes**: 3 fixed styles in the living-room 360 | **Yes**, AI "Stage this home": 7 styles, remove furniture, slide to compare | **Yes**, Defurnish (one click, can be the default view) | No | **Yes, strongest**: real catalogue products, finishes, mood boards, AR "View in My Room 3D" | Not mentioned | No (spec text only) | No | No | No | No | No |
| **Neighbourhood map with places** | **Yes**: Mapbox, 434 places in 7 categories, walking time 5/10/15 min, price tags, future plans | **Yes**: Walk Score 100, Transit Score, travel times | No | **Yes**: map, schools (GreatSchools), neighbourhood guide | No | **Yes** (claimed): transit, schools, POIs, sun and shadow | **Yes**: categories (bus, light rail, train, cafés, parks...) | Partial: "תחבורה" section | "השכונה" section (not a POI map) | No | Neighbourhood page | Landmarks plus "View on Google Maps" |
| **Video with voice** | Not found on Kikar (Rainbow has a narrated film) | Not found | "Highlight reel", coming soon (no voice) | Not verified | n/a | Not verified | Not found | Not found | Background video, no voice | Not found | Background video | Video present, voice not verified |
| **Languages** | **5**: he / en / fr / ru / ar (hreflang) | English | Site in 8 locales (not the tours) | English | n/a | Site en / he; product "Multi-language" (claimed) | Hebrew | Hebrew | Hebrew | he / en (Ashtrom); he (Electra) | English | en / ar / ru |
| **Contact path** | One-tap WhatsApp "ייעוץ חינם", scheduled video call with a NadLan rep, broker hand-off | Phone, "Request tour": in-person or **"Real-time video"** with a date picker | n/a | Agent phone, contact | Pro client portal | Rep's personal link, lead capture, Calendly | Lead form, WhatsApp, chat | "ליצירת קשר" form | **Named agent with hours** plus chat / phone / WhatsApp / SMS / Messenger / video chat ("בקרוב") | General contact form | Contact and sales-team pages | **WhatsApp, "Instant Call", "Sales Video Call"**, Register Interest |
| **Basket or online reservation** | **Partial**: "לסל הדירה: המחיר המלא, הצוות והנציג" (apartment plus team plus rep); no deposit | No ("Get pre-qualified" only) | n/a | No | Plan to estimate or proposal | Not found | No ("פרויקטים במבצע") | No (payment terms "20/80 פטור מדד" shown) | "קבלו הצעה" (get an offer) | No | No | Register Interest only |
| **Phone load (rough)** | **Fast**: DCL 1.0 to 1.5 s, load 1.2 to 1.7 s, about 1.7 MB first load | Not measured (bot wall in headless) | Blog DCL 1.0 s | DCL 0.8 to 1.7 s, load 1.1 to 2.1 s | n/a | **Slow**: marketing page load over 25 s, 39 MB | DCL 0.3 to 0.5 s, load 1.2 to 2.5 s | Not measured (bot wall) | Load 2.2 s | Ashtrom 4.8 s, Electra 2.4 s (Acro 11.3 s) | Load 1.4 s | Not measured (headless redirect) |
| **Genuinely new that we do not have** | n/a | AI restyle with 7 styles and "remove furniture"; live **real-time video tour** booking with a date picker; monthly payment estimate on the price line | **Defurnish** as default; auto room **measurements** in the twin | **Per-unit live status** ("Contract Signed") and **past sales of the same building** in one table | Real purchasable products, priced, turned into an estimate; AR walk in your own room | **Personal link or QR per buyer, with interest tracking**; CRM-live availability (BMBY: send plans from the CRM) | "נכסים שנמכרו" with filters; construction-stage tracker; promotions shelf | **Deal table of 14 in the project plus 1,000 nearby, filterable**; yield %; payment terms | One panel with a named agent, hours and 6 channels | Electra: "15 מעליות במהירויות של 4 ו-6 מ'" (we already have it) | **Real photographed panorama from the top with a day/night toggle**; 3D cube picker as the first screen | **Instant "Sales Video Call"** button; live "Available Units 21" count |

Also read: **Una Brickell** names units by direction ("Upper North East Residence 4201"), gives a PDF floor plan per unit, and hides prices behind "Request Pricing & Availability". **Acro Tel Aviv Towers** is occupied and shows facts plus a lead form only.

## (b) Where we trail: what to build, ranked by impact on a buyer's decision

1. **No live unit inventory or status on the tower.** Compass lists every unit for sale in the building with its price, $/sf and "Contract Signed" status, next to "Past Sales" and "Past Rentals" for the same building: https://www.compass.com/building/the-henry-manhattan-ny/1633466331737096645/. Emaar shows "Available Units 21": https://www.emaar.com/en/properties/creek-bay-at-dubai-creek-harbour. REALS and BMBY claim CRM-live availability: https://www.simplex3d.com/reals/.
   - **Build:** pin the apartments now on the market in the towers onto our 3D floor and direction picker. Use the published asking price, the date and the source. We already hold some asking prices, for example 10M ₪ for a floor-16 unit in 9.2026. Mark each pin "מודעה שפורסמה". The towers have no developer price list, so this is the only honest form of inventory.
2. **No real floor plan per apartment.** Ours is schematic and says the split was not published. Una gives a PDF plan for each named unit: https://www.unaresidencesmiami.com/. Yad1 and Madlan show plans per type: https://www.yad2.co.il/yad1/project/13671. Zillow shows a plan per community plan: https://www.zillow.com/community/one-wall-street-sales/458738705_zpid/.
   - **Build:** collect real plans from published listings and brokers, and check whether the permit file is public. Attach them per type and floor, with the source. Until then, keep the schematic label.
3. **No filterable deal table.** Madlan shows "היסטוריית עסקאות, בפרויקט (14), בסביבה (1000)" with filters for rooms, year, distance and ₪/m²: https://www.madlan.co.il/projects/%D7%9E%D7%92%D7%A8%D7%A9_9_%D7%A4%D7%90%D7%A8%D7%A7_%D7%94%D7%97%D7%95%D7%A8%D7%A9%D7%95%D7%AA_%D7%AA%D7%9C_%D7%90%D7%91%D7%99%D7%91. Yad1 has "נכסים שנמכרו באזור" with filters: https://www.yad2.co.il/yad1/project/13671.
   - **Build:** we show 3 tower deals and city medians. Add a sortable and filterable table of Tax Authority deals within walking distance (rooms, year, ₪/m², distance from the towers), using the data we already use for the medians.
4. **No personal buyer link with interest tracking.** REALS claims "personalized shareable links and QR codes" and "real-time buyer interest tracking": https://www.simplex3d.com/reals/. BMBY sends plans to the buyer from the CRM: https://bmby.co.il/bmby-3d-%D7%A1%D7%91%D7%99%D7%91%D7%94-%D7%9E%D7%A9%D7%9C%D7%99%D7%9E%D7%94-%D7%9C%D7%9E%D7%A2%D7%A8%D7%9B%D7%AA.
   - **Build:** a "שלחו לי את הבחירה" link that reopens the exact tower, floor, direction, design style, time of day and basket. It should go with the WhatsApp message, and our rep should see which apartments the buyer opened. This needs the privacy notice to be in order first: the lead-privacy rule applies.
5. **The design step stops at 3 fixed styles.** Zillow's "Stage this home" offers 7 styles, "remove furniture" and a slider between original and staged: https://zillow.mediaroom.com/2025-09-10-Zillow-brings-AI-powered-Virtual-Staging-to-Showcase-listings, live on https://www.zillow.com/community/one-wall-street-sales/458738705_zpid/. Matterport makes the unfurnished view the default: https://matterport.com/blog/matterports-winter-2025-release-productivity-multiplied. Houzz links finishes to real priced products: https://pro.houzz.com/for-pros/feature-3d-floor-plan.
   - **Build:** an "empty apartment" state (no furniture) and a before/after slider in the 360 we already have. Later, priced finish packages that flow into the basket.
6. **Our views are simulations, not photographs.** Waldorf Miami shows a real photographed panorama from the top with a day/night toggle: https://www.waldorfresidencesmiami.com/view/ (screenshot `waldorf-miami-view-from-top-390.png`).
   - **Build:** the Kikar towers are topped out, so drone panoramas at floors 20, 30 and 38 are now possible. They would replace "הדמיה" with a real photo per height and direction, keeping the simulation as a fallback.
7. **No instant video call.** Emaar has a one-tap "Sales Video Call" and "Instant Call": https://www.emaar.com/en/properties/creek-bay-at-dubai-creek-harbour. Zillow books an in-person or "Real-time video" tour on a date strip: https://www.zillow.com/community/one-wall-street-sales/458738705_zpid/. Gindi shows a named agent with hours and 6 channels: https://gindi.com/online/.
   - **Build:** we already have a scheduled video call ("שיחת וידאו עם נציג נדל״ן"). Add a "now available" state during office hours, and show the rep's name and hours next to the WhatsApp bar.
8. **No room measurements in the example apartment.** Matterport Property Intelligence measures rooms, walls and ceiling heights automatically: https://matterport.com/news/matterport-launches-property-intelligence-transforming-real-estate. Zillow shows sqft per plan.
   - **Build:** put room sizes on the example-apartment plan and in the 360 (living room, bedroom, balcony 15.5 m² as published), marked "לדוגמה".
9. **The monthly payment is not next to the price.** Zillow puts "Est. payment: $60,827/mo" beside the price: https://www.zillow.com/community/one-wall-street-sales/458738705_zpid/. Madlan shows payment terms: see item 3.
   - **Build:** we link to "מחשבון משכנתא". Pre-fill it from the chosen deal or asking price, and show one line of monthly payment under the price.

Seen but not recommended: Zillow shows public view and save counters ("510 views, 13 saves"). This conflicts with the owner's rule of no public traffic numbers (developer-recruitment strategy), so it is not on the build list.

## (c) Where we lead, ranked

1. **Choosing an apartment by tower, floor and direction, with the window view, on a free public page.**
   - Our page has tower, floor and bearing, the view at floors 20/30/38, a sun and shadow clock, and a key plan.
   - None of the portals checked (Zillow, Compass, Yad1, Madlan) do this.
   - The only comparables are a B2B tool sold to developers (REALS, claimed) and Waldorf's cube picker, which works by floor band with no prices.
   - The official Kikar pages (Ashtrom, Electra) show only facts.
2. **Published deal prices for this exact project, with sources and dates.**
   - We show 3 deals by floor, a ₪/m² range, area medians and dated asking prices.
   - The official Ashtrom and Electra pages show no price at all.
   - Madlan has no Kikar project page.
   - Waldorf and Una hide prices behind a form.
3. **One page holds the 360 example apartment, 3 design styles, 3 times of day, and 360 lobby, pool and gym.**
   - Zillow's staging works on single photos.
   - Matterport needs a finished, scanned unit, so it cannot work for off-plan.
   - Neither Waldorf nor Emaar shows a 360 of amenities on the project page.
4. **5 languages including Arabic, French and Russian.** Every Israeli competitor checked is Hebrew only, apart from Ashtrom (he/en). The US sites are English only. Emaar has en/ar/ru.
5. **A deeper area map.** It has 434 places in 7 categories, walking time bands (5/10/15 min), price tags and future plans on one map. Yad1 lists categories, Compass lists schools, and Zillow gives a score.
6. **A basket that combines the apartment, the team and the rep** ("לסל הדירה: המחיר המלא, הצוות והנציג"). No property competitor has a basket. The closest is Houzz turning a design into an estimate.
7. **Honest, dated facts that no competitor has.** The occupancy dates are given source by source (Electra "April 2027", Ashtrom "2026", media reports), the timeline runs from 1942, and the lift fact is stated. Ashtrom still says completion in 2026; Electra says April 2027.
8. **Speed on a phone.** Our DCL is 1.0 to 1.5 s, against more than 25 s for the REALS marketing page, 11.3 s for Acro and 4.8 s for Ashtrom. Measured on broadband with phone emulation.

## Not verified (said honestly)

- **Yad1:** "virtual tour and the real view from every window" comes only from a third-party summary (broker-re.co.il via search). It was not seen on the two Yad1 project pages read.
- **REALS and BMBY:** all features are vendor claims from their marketing pages. I did not see a live buyer link. "Duo" in REALS's featured projects may be DUO Tel Aviv; this was not confirmed.
- **Zillow:**
  - The 3D Home interactive floor plan page was bot-walled.
  - That 3D tours are possible on new-construction pages comes from Zillow's builder FAQ, not from a live community page.
  - SkyTour was not seen.
- **Matterport:** AI "restyle" (Genesis) is reported by third-party 2026 reviews only. Defurnish is confirmed on Matterport's own blog.
- **Compass:** the virtual-tour vendor (Matterport) is inferred from HTML hits, and the floor-plan sub-page was not opened.
- **Waldorf:** I did not click past "SELECT THE CUBE", so the 360 step and any choice of direction were not checked.
- **Emaar:** the 360 VR hub (https://www.emaar.com/en/vrtours-for-partners) was not opened, and the brochure was not downloaded (by rule).
- **Houzz:** the consumer AR "View in My Room 3D" is app-only and was not tested on the web.
- **Our page:**
  - The lobby, pool and gym 360 were seen.
  - The lift-panel building walk and the spa and car-park scenes were not clicked through in this audit. The spa and car-park buttons are on the page.
  - No narrated video was found on the Kikar page.
- **Speed:** there are no phone timings for Zillow, Madlan or Emaar (bot wall or redirect in headless mode).

## Screenshots in this folder (390 wide)

- `compass-henry-building-390.png`: per-unit prices, status, "Filter by unit or tier/line", Past Sales.
- `yad1-bnei-efraim-project-390.png`: units by type with "from" price, plans, nearby places, sold deals.
- `gindi-tlv-online-390.png`: apartment search wizard and the 6-channel contact panel with a named agent.
- `waldorf-miami-select-the-cube-390.png`: 3D tower cube picker as the first screen.
- `waldorf-miami-view-from-top-390.png`: real photographed panorama with a day/night toggle.
- `una-brickell-residences-390.png`: units named by direction, PDF plan per unit, prices behind a form.
- `ours-kikar-example-apartment-390.png` and `ours-kikar-360-inside-390.png`: our flow at the same width, for comparison.
