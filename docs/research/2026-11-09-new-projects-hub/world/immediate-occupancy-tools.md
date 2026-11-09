# Immediate occupancy: what exists in the world today

Checked on 9.11.2026 for the nad-lan immediate-occupancy finder (`אכלוס מיידי` now, `אכלוס קרוב` soon).
Read-only research. No sign-in, no form, no purchase, no CAPTCHA solved. Where a site blocked us, it is marked blocked and nothing was bypassed.

This file extends the teardowns in this folder (zillow, realtor, newhomesource, redfin, rightmove, idealista, domain, booking, compass, micro-features, matrix). It does not repeat them. It looks only at the move-in-ready angle.

**Evidence classes**
- **[code]:** read live today in the owner's Chrome with a DOM script.
- **[fetch]:** page text pulled today with WebFetch.
- **[search]:** a web-search result snippet read today; the page itself was not opened.
- **[file]:** taken from an earlier file in this research folder, read on 9.11.2026 (file named).
- **blocked:** the site refused us today; nothing was bypassed.

---

## 1. The short answer

1. **The best move-in filter in the world is NewHomeSource's.** It has a quick move-in channel with time bands (move now, 1-2 months, 3-6 months), a live count, a map, and a construction badge per home. It does not show a ready date on the card, does not value its deals, and has no waiting-cost tool.
2. **Dubai is the most data-rich market for stage.** Bayut filters by Ready or Off-Plan, by handover date and by percent complete. FAM Properties tracks construction progress from Dubai Land Department inspections, dates it, and flags projects that are past their promised handover.
3. **France and Japan own the clean landing page.** SeLoger Neuf has indexable `livraison immédiate` pages with counts. Yahoo! Real Estate Japan has a move-in-now theme page with a count; SUUMO has an immediate-handover filter.
4. **The UK, Australia, Germany and Spain have no move-in filter on the pages we read.** Readiness lives only in developer free text (move in now, ready for occupation) or in a per-card availability date (Immowelt).
5. **In Israel, Yad2 has one toggle (`אכלוס קרוב`) with filtered pages that carry a count, plus a month-and-year delivery field on project pages.** Madlan has no occupancy filter, only developer badges and a permit-stage tracker. Developers mark `אכלוס מיידי` by hand, and we found stale or contradictory labels.
6. **Calculators for ready versus on paper exist, but only as stand-alone tools** (India, Singapore, a generic rent-versus-buy site). None is fed by a real listing's delivery date, local rent or a construction-cost index.
7. **Nobody we found values a developer deal in money against a normal payment schedule, alerts when a project becomes ready, or checks that the immediate label matches the stated date.** These are the honest world-first candidates (section 5).

---

## 2. World, site by site

### 2.1 United States

**NewHomeSource (BDX / Zonda data)** [code]
- **Pages:** https://www.newhomesource.com/quickmoveinsearch (a landing form: state, area or ZIP, price) and https://www.newhomesource.com/communities/tx/austin-area?inventory=true (results).
- **Dedicated filter:** yes. The `Quick move-ins` chip switches the hub to quick move-in homes. The `Move-in date` menu offers `Floor Plans`, `All Quick Move-In`, `Move now`, `1-2 months`, `3-6 months`.
- **Count:** H1 switches to quick move-in homes in the Austin area and H2 shows 3,158 homes (of 8,327 homes in the area, so about 38% of the new-home stock there is quick move-in). The page title switches to a spec-homes wording.
- **Map:** the same page carries the map, with the filter applied, and a `Remove boundary` control.
- **Card fields:** price (with the old price struck through when cut), beds, baths, garage, square feet, a quick move-in type line, community, builder, builder rating, `Free brochure`, save. **No ready date and no price per square foot on the card.**
- **Home page (spec detail), for example 108 Top View Drive, Liberty Hill:** badges `QUICK MOVE-IN` and `UNDER CONSTRUCTION`; a note that the price was reduced in the last 14 days; plan name; a **Special offers** block with the builder's financing deal and an **expiry date** (runs through 31.12.2026); community, schools, builder and third-party reviews.
- **Deals:** `Hot deals` and `Price reduction` filters; offers as text, never valued in money.
- **Market snapshot:** average home price by nearby city, ZIP, county and top builder (counts and averages). Not a deal-price comparison per home.
- **Calculators:** separate pages for affordability and cost of ownership, linked from the hub. No calculator for move-in-ready versus build.
- **Alerts:** `Save search`.
- **Languages:** English only on the pages read.

**Zillow** [code], plus teardown-zillow.md [file]
- **Page:** https://www.zillow.com/austin-tx/new-construction/ (5,475 results; the path is not a strong filter, see the teardown).
- **Filters panel (read today):** `Listing type` has `New construction`; `Listing status` has `Active`, `Coming soon`, `Zillow Preview`, `Accepting backup offers`, `Pending & under contract`. **No move-in timeframe and no construction-status filter.**
- **Inside a community:** an `Available homes` table with listing, price, beds, baths and status [file]. Cards mark plans (a plan name) versus built homes (an address).
- **Strengths for this angle:** price history per row with source and date, `Not available` instead of a fake estimate, payment calculator, days on Zillow [file].

**Realtor.com** [code], plus teardown-realtor.md [file]
- **Page:** https://www.realtor.com/newhomecommunities/Austin_TX (46 communities).
- **Filters:** `Price`, `Beds`, `More` (bathrooms, square feet, expand search). Deal chips: `All deals`, `Reduced rates`, `Cash at closing`, `Flex cash`, `Appliance package`, `Free upgrades`, with `Promotions explained`. **No move-in filter.**
- **Quick move-in appears only as a community name** chosen by the builder (one community name contains the words quick move-in).
- **Inside a community:** a `Move-in Ready Homes` list with price, beds, baths, square feet, plus the RealCost monthly payment [file].

**Redfin** (teardown-redfin.md [file]; Chrome permission prompt timed out today)
- Inside a community, two lists: `Available homes (2)` and `Ready-to-build homes (12)` [file].
- Redfin's own help post says new construction is a `Listing type` in Filters; it names no move-in or construction-status filter [search: https://www.redfin.com/news/redfin-adds-new-construction-listings-and-features/].
- Note: US MLS data already carries a construction-status field (to be built, under construction, completed and never occupied) [search: https://connectmls.smartmls.com/hc/en-us/articles/24500604326299-Search-for-new-construction-listings]. The portals do not expose it as a buyer filter on the pages we read.

**Homes.com:** **blocked** (Akamai access-denied page in Chrome today on https://www.homes.com/austin-tx/new-construction/). Its own guide says its new-home filter shows move-in-ready listings and that spec homes sit in a move-in-ready section [search: https://www.homes.com/learn/searching-online-for-new-construction-homes]. Not verified.

**Other US signals [search]:** New Homes Guide has a `Move-In-Now` yes box; builders (Richmond American, Shea, Smith Douglas) run their own quick move-in toggles and pages.

### 2.2 United Kingdom

**Rightmove** [fetch], plus teardown-rightmove.md [file]
- **Page:** https://www.rightmove.co.uk/new-homes-for-sale/London.html (4,064 results).
- **No filter** for completion, ready to move in, Help to Buy or incentives in the visible controls. Readiness and incentives appear only inside descriptions (one listing says ready for occupation; another offers a choice of stamp duty, legal fees, deposit contribution or discount).
- Badges: paid tiers, `Reduced on [date]`, `Added on [date]`. Alerts: instantly, daily, every 3 days, every 7 days [file].

**Zoopla** [fetch]
- **Page:** https://www.zoopla.co.uk/new-homes/property/london/ (6,473 in the heading).
- **No filter** for completion, move-in date or incentives. Sort includes `Most reduced`.
- Badges: `New home`, `Just added`, `Reduced`, `Chain free`, `Showhome Launch`. Ready-to-move-in wording, incentives and deposit boosts appear only in descriptions. `Create alert`.

**OnTheMarket** [fetch]
- **Page:** https://www.onthemarket.com/new-homes/property/london/ (5,054 results).
- **No completion or incentive filter.** Useful neighbours: `Only show: New build homes`, `Recently reduced`, and `Added to site` (24 hours, 3 days, 7 days). Card age labels (`Added yesterday`, `Added > 14 days`).

### 2.3 Spain

**Idealista obra nueva:** **blocked** today (403 and a slider CAPTCHA, see teardown-idealista.md [file]).
- From search snippets: finished developments carry an `ENTREGA INMEDIATA` tag, and projects under construction show a planned delivery quarter (for example `3 TR 2026`). Sorting found was by price and size only [search: https://www.idealista.com/news/inmobiliario/vivienda/2026/09/08/740655-viviendas-sobre-plano-a-la-venta]. No delivery filter confirmed.

**Fotocasa:** the obra nueva hub URL we tried returned a page-not-found message behind a cookie wall (https://www.fotocasa.es/es/comprar/obra-nueva/madrid-capital/todas-las-zonas/l). Search snippets show development pages with a delivery-date line (for example last quarter 2027) and an indicative mortgage payment, in Spanish, English and German URLs [search]. No delivery filter confirmed.

### 2.4 Australia

**realestate.com.au** [code]
- **Page:** https://www.realestate.com.au/new-apartments/melbourne-city-greater-region-vic/ (29 off-the-plan apartments).
- **No filter.** Readiness is the developer's headline text: Move In Now, Construction complete with move in today, Ready 2027 with over 70% sold, construction starting early 2027, Last 5 three-beds. An `Explore Map` link sits on the state page.

**Domain** [code] on the hub; project page not read (Chrome permission prompt timed out)
- **Page:** https://www.domain.com.au/new-homes/melbourne-region-vic/ (10,723 new homes).
- **Filters in the bar:** `Price`, `Beds`, `Property types`, `Map view`, `Create Property Alert`, sort. **No completion filter seen.** Project cards list unit rows with price, beds, baths, parking. Some cards invite VIP previews before launch.

**apartments.com.au** [fetch]
- **Page:** https://www.apartments.com.au/developments (9,430 developments).
- Status badges on cards: `Pre-construction`, `Under construction`, `Construction complete`, plus `SELLING NOW`. **No filter** for them on the page text. Move-in timing only in free text.

### 2.5 Germany

**ImmoScout24** [fetch] https://www.immobilienscout24.de/neubau/baugesellschaft
- A Neubau hub (3,000+ projects nationwide). It explains that a project can be planned, under construction or just finished, but shows **no stage filter**.

**Immowelt** [fetch] https://www.immowelt.de/suche/berlin/wohnungen/kaufen?neubau=true
- Quick chip `Neubauwohnung`. **No stage filter.**
- Each card shows **an availability date** (`frei ab sofort` or a date such as 01.06.2028), **price per m²**, `Erstbezug` and `Neubau` labels, floor, energy class. This is the cleanest per-card readiness field in Europe that we saw.

### 2.6 France

**SeLoger Neuf** [fetch] https://www.selogerneuf.com/immobilier/neuf/bien-programme/ile-de-france/livraison-immediate/
- **Dedicated indexable landing pages** for `Livraison immédiate` by region, department and type (apartment, house): 127 programmes and 1,016 lots in Ile-de-France today. Many department variants exist [search].
- Card badges: `Livraison immédiate`, `Travaux en cours`, `Offre spéciale`, `Dernières opportunités`. Fields: from price, room range, amenities, developer (`Proposé par`).
- **No delivery-year or quarter filter, no sort, no structured delivery date** on cards. Reduced notary fees and VAT appear only in text.

### 2.7 United Arab Emirates (Dubai)

**Bayut** [fetch] https://www.bayut.com/new-projects/dubai/
- Filters: completion status **`All` / `Ready` / `Off-Plan`**, **`Handover By`**, **`Payment Plan`**, **`% Completion`**, beds, type.
- Cards: launch price, developer, payment plan ratio (for example 68/32), handover quarter (for example Q4 2028), Register Interest. 2,454 projects.
- **Transactions** (Dubai Land Department data) can be filtered by ready or off-plan, with price per square foot and dates, at area and building level, in a separate Market Intelligence tab (article updated 14.10.2026) [fetch: https://www.bayut.com/mybayut/dubai-transactions-feature-bayut]. Not seen on a project card.

**Property Finder** [fetch]
- Main search has an `Off-plan` / `Ready` control (https://www.propertyfinder.ae/en/search?c=1&fu=0&ob=mr&cs=completed). Cards: `Verified`, days since listing, floor plan, and sometimes a mortgage cashback amount in money.
- New projects page (https://www.propertyfinder.ae/en/new-projects/lp/dubai): 2,393 off-plan projects, 1,111 projects with developer stock, **Delivery Date** per card, launch price, number of payment plans, **Compare**, Map. Tools: mortgage, rent versus buy, affordability.

**FAM Properties, Dubai Projects Status Tracker** [fetch] https://famproperties.com/dubai-projects-construction-progress
- Per project: **progress percent with an `As of` month**, launch date, handover date, and either **`Due in`** or **`Past its date by`**. Sort: about to complete first. Area summary: projects on site, average progress, due this year, past their date. Source: Dubai Land Department inspections.
- This is the closest thing in the world to an honest delivery tracker. It is a brokerage site, not a listing finder.

**Developer on-time rankings:** a Dubai brokerage blog (joinoliva.com) publishes developers ranked by delivery rate [search]. Unverified against official records, but it means a developer delivery record is not new.

### 2.8 India

**99acres, MagicBricks, Housing.com:** **blocked** to our fetch agent today (403, refused, 406); Chrome permission prompt timed out. Evidence from search only:
- 99acres runs indexable ready-to-move flats pages per area with counts in the title, including budget variants, and a RERA badge on cards [search: https://www.99acres.com/ready-to-move-flats-apartments-in-hinjewadi-pune-ffid].
- Housing.com has `Ready to move` / `Under Construction` filters and `ready_to_move_projects` pages [search].
- Squareyards lists statuses (ready to move, under construction, new launch, partially ready, upcoming) and **possession-year filters** (2026 to 2029) [search].
- No portal found with an occupancy-certificate (OC) filter or badge [search].
- **Dealplexus calculator** [fetch] https://www.dealplexus.com/tools/under-construction-vs-ready-property: under-construction versus ready, inputs price, construction years, current rent, appreciation, loan rate, down payment; outputs GST, rent during construction, pre-EMI interest and a verdict. Not linked to listings, no delay input.

### 2.9 Singapore and Malaysia

- **PropertyGuru:** **blocked** (403). Its Malaysian guide says new launches can be shortlisted by stage of completion; listings show a completion year [search].
- **EdgeProp SG** [fetch]: new-launch search with an `All TOP Years` filter (TOP is the completion permit), developer, tenure, district.
- **Stacked Homes:** a `Date of TOP` min and max filter [search].
- **PropertyNet SG calculator** [fetch] https://propertynet.sg/new-launch-vs-resale-calculator/: new launch (rent until completion, progressive interest) versus resale; years to completion typed by the user; PDF and WhatsApp to an adviser. Not linked to listings.

### 2.10 Japan and China

- **SUUMO** [fetch] https://suumo.jp/ms/shinchiku/tokyo/: a feature filter `即引渡可` (immediate handover). No move-in date or completion filter otherwise.
- **Yahoo! Real Estate Japan** [fetch] https://realestate.yahoo.co.jp/new/mansion/03/theme/02/: a move-in-now theme page for new condos in Kanto, 155 properties. It notes that units completed more than a year ago and never occupied are included.
- **Beike (China)** [fetch, news]: on 26.8.2026 its Suzhou station started a one-year trial in which **the platform pays the buyer 1,000 yuan a month, up to 6 months, if the developer delays handover**, plus a free handover inspection (https://stock.10jqka.com.cn/20260827/c679342808.shtml). A platform-backed delay guarantee already exists.

### 2.11 Generic calculators (not portals)

- **BeGoodTool rent versus buy** [fetch] https://begoodtool.com/rent-vs-buy/en: a pre-sale mode with installments during construction and the mortgage starting at delivery. Generic.
- Bank and portal rent-versus-buy calculators (Redfin, Bankrate, Property Finder) do not model a construction period [search].

---

## 3. Israel, site by site

**Yad2 (Yad1 new projects)**: fetch **blocked** (Radware check); Chrome prompt timed out today. Facts from competitors.md, read in Chrome on 9.11.2026 [file], plus search snippets.
- **Filter:** an `אכלוס קרוב` (near occupancy) toggle next to price, rooms, type and 3D tours [file]. One toggle only: no time bands, no immediate versus soon split.
- **Indexable filtered pages with a count in the title**, for example 14 projects in the Tel Aviv area for near occupancy [file].
- **Cards:** badge row (`אכלוס קרוב`, `במבצע`), name, address, rooms, floors, m² range, from price, sometimes price per m², one developer marketing line such as `אכלוס מיידי!` [file].
- **Project and unit pages:** an expected occupancy field by month and year, and unit pages with rooms, m², price and occupancy month [search: https://www.yad2.co.il/yad1/project/15696, https://www.yad2.co.il/yad1/project/13214].
- **Deals:** a national deals hub (`/yad1/projectsale`) with free-text deals [file]. Hebrew only. A separate value-estimate tool is linked [file].
- **Freshness problem seen:** a Tidhar project in Bitzaron carries an immediate-occupancy mark while its expected occupancy field still says 7/2026; a Shikun & Binui project in Lod (Ben Shemen) advertises immediate occupancy and, on the same page, occupancy within the coming year [search]. No checked-on date is shown.

**Madlan**: fetch **blocked** (403). Facts from competitors.md [file] and search.
- **No occupancy filter** [file]. Filters: price, rooms, type, more filters; project / brokerage / private tabs; `יצירת התראה` (create alert) next to the filters.
- Readiness appears only as **developer free-text badges** (`אכלוס דצמבר 2026 !`, `הטבות לרגל האכלוס !`, `שלמו 10% - היתרה באכלוס!`) and lines such as two apartments available for immediate occupancy [file, search].
- **Project pages show a permit-stage tracker:** initial planning, permit application, permit granted, construction finished, with the current stage marked [search: https://www.madlan.co.il/projects/%D7%9E%D7%92%D7%A8%D7%A9_77_89_%D7%9E%D7%91%D7%95%D7%90_%D7%9E%D7%95%D7%93%D7%99%D7%A2%D7%99%D7%9D]. No structured delivery date. Hebrew only.

**Homeless**: fetch **blocked** (403). competitors.md records that its new-projects URL returns 404 and that it appears on none of 27 result pages [file].

**Dira Plus (דירה פלוס)**: **not found** by search in Hebrew or Latin script. If the owner meant a specific site, its address is needed.

**BuyMe / BuyIt**: no Israeli new-project portal by that name found. The closest match is **BuyItInIsrael** [fetch] https://www.buyitinisrael.com/: an English magazine with a project list (developer, types, rooms, from price, city; filters for location, type, rooms, max price with a currency selector). **No delivery date and no move-in filter.** Purchase-tax calculator only.

**immobilier.co.il** (Israel portal in eight languages) [fetch] https://www.immobilier.co.il/en/city/netanya/new-projects
- New projects with a **delivery-year filter** (all, 2026, 2028, 2029, 2030, 2031 in Netanya; 120 listings), a delivery-year badge, unit count, from and up-to price, a list of available units (rooms, m²), list and map views, `Create Alert`, prices also in dollars and euros.
- **No ready-now option**, no developer on the card, no price per m², no check date.
- Languages: French, English, Hebrew, Russian, Portuguese, Spanish, Italian, German. This is the main multilingual rival for an Israeli finder.

**nadlanmaster.co.il** [fetch] https://www.nadlanmaster.co.il/immediate/
- A content page titled for immediate-occupancy new flats, ranking on the phrase. Three featured tiles and plain links. **No filters, no prices, no dates, no map.** Links to yield and purchase-tax calculators.

**nadlan.com**: no occupancy filter; an AI search box first [file: competitors.md].

**Developers' own sites**

| Developer | URL read | What it offers for ready now | Evidence |
|---|---|---|---|
| Ashtrom Megurim | https://www.ashtrom-megurim.co.il/ (today the fetch was truncated before the project list) | Home page tiles each badged `אכלוס מיידי`; project titles carry the phrase; ranks top 3 on immediate-occupancy queries | [file: competitors.md]; today [fetch] partial |
| Aura | https://www.auraisrael.co.il/ | A **project-status filter**: all, in marketing, soon in marketing, in planning, **occupied** (`מאוכלסים`). No immediate label. Stale example: its own news says occupancy of Aura City Hadera began on 11.02.2026, yet the project still shows as in marketing | [fetch] |
| Africa Israel Residences | https://res.afi-g.com/ | **Construction-milestone banners** per project: permit received, construction started, construction in full swing, presale; a separate occupied-projects page; city and rooms search. No immediate-occupancy filter | [fetch] |
| Azorim | https://www.azorim.co.il/projects/ | Region and city filters with a live count on the apply button (show 24 projects). **No status labels** | [fetch] |
| Tidhar | https://www.tidhar.co.il/residences/for-sale/ | City, type (2-7 rooms, duplex, garden, penthouse) and price filters; a 10-year warranty badge. **No status, no price, no delivery** on the list | [fetch] |
| Shikun & Binui | https://www.shikunbinui.co.il/ failed (certificate mismatch); https://shikunbinui.com/ is the English corporate site with no residential status | Readiness only visible through Yad2 listings (Ben Shemen, contradictory) | [fetch], [search] |
| Electra Residential | official residential site not located | Only third-party listings found | [search] |
| Sela Binui | from competitors.md | A model-apartments page titled with immediate occupancy and a pay-5%-now offer | [file] |

---

## 4. Feature matrix

**Legend**
- **Y:** seen today on the pages read.
- **p:** partial: free text only, a narrower version, or in a separate tab rather than on the listing.
- **y:** known pattern, not re-checked today.
- **-:** not seen on the pages read.
- **?:** blocked, or not verified today.

**Columns:** NHS = NewHomeSource · Zil = Zillow · Rltr = Realtor.com · Rdfn = Redfin · RM = Rightmove · Zpl = Zoopla · OTM = OnTheMarket · REA = realestate.com.au · Dom = Domain · SLN = SeLoger Neuf · Imw = Immowelt · Bay = Bayut · PF = Property Finder · FAM = FAM tracker · SUU = SUUMO · YJP = Yahoo! Real Estate Japan · Yad2 · Mad = Madlan · ImIL = immobilier.co.il · ILdev = Israeli developers (best of the seven).

Idealista, Fotocasa, Homes.com, 99acres, MagicBricks, Housing.com and PropertyGuru are left out of the grid because they blocked us; their search-only facts are in section 2.

| Feature | NHS | Zil | Rltr | Rdfn | RM | Zpl | OTM | REA | Dom | SLN | Imw | Bay | PF | FAM | SUU | YJP | Yad2 | Mad | ImIL | ILdev |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| **Finding the ready set** | | | | | | | | | | | | | | | | | | | | |
| Move-in-ready filter or toggle | Y | - | - | - | - | - | - | - | - | Y | - | Y | Y | p | Y | Y | Y | - | - | p |
| Indexable ready-now landing page with a count | Y | - | - | - | - | - | - | - | - | Y | - | ? | - | - | ? | Y | Y | - | - | p |
| Time bands (now, months, by year) | Y | - | - | - | - | - | - | - | - | - | - | Y | - | p | - | - | - | - | Y | - |
| Construction stage or percent complete | p | - | - | p | - | - | - | p | ? | p | - | Y | - | Y | - | - | - | Y | - | p |
| Count of ready results | Y | - | - | p | - | - | - | - | - | Y | - | p | p | p | ? | Y | Y | - | - | - |
| Map with the ready filter applied | Y | - | - | - | - | - | - | - | - | - | - | ? | ? | - | ? | - | ? | - | - | - |
| **Listing fields** | | | | | | | | | | | | | | | | | | | | |
| Delivery or availability date (structured) | - | - | - | - | - | - | - | p | ? | p | Y | Y | Y | Y | ? | - | Y | p | Y | - |
| Ready or construction badge on the card | Y | p | - | p | p | p | - | p | ? | Y | p | p | p | Y | - | ? | Y | p | p | Y |
| Table of ready units inside the project | Y | Y | Y | Y | - | - | - | - | p | - | - | ? | ? | - | - | - | Y | - | Y | - |
| Price on the card | Y | Y | Y | Y | Y | Y | Y | Y | Y | Y | Y | Y | Y | - | Y | Y | Y | p | Y | - |
| Price per m² or sq ft on the card | - | p | - | - | - | - | - | - | - | - | Y | - | - | - | - | - | p | - | - | - |
| Developer named | Y | Y | Y | Y | Y | ? | ? | p | ? | Y | p | Y | Y | - | ? | ? | Y | Y | - | Y |
| Units left (count) | Y | p | p | Y | - | p | - | p | - | p | - | - | p | - | - | - | - | p | Y | - |
| Days on market or added date | - | Y | p | Y | Y | Y | Y | - | ? | - | - | ? | Y | - | p | - | - | - | - | - |
| **Money** | | | | | | | | | | | | | | | | | | | | |
| Incentives or deals shown | Y | - | Y | - | p | p | - | p | - | Y | - | Y | Y | - | - | - | Y | p | - | p |
| Incentive valued in money against a normal schedule | - | - | - | - | - | - | - | - | - | - | - | - | p | - | - | - | - | p | - | - |
| Offer expiry date | Y | - | - | - | - | - | - | - | - | - | - | - | - | - | - | - | - | p | - | - |
| Comparison to recorded deal prices | p | p | p | p | p | ? | - | - | - | - | - | p | p | - | p | - | p | ? | - | - |
| Ready versus off-plan price comparison | - | - | - | - | - | - | - | - | - | - | - | p | - | - | - | - | - | - | - | - |
| Mortgage or payment calculator | p | Y | Y | Y | p | ? | ? | ? | ? | ? | ? | y | Y | - | ? | ? | ? | ? | - | - |
| Ready versus on-paper cost calculator (any) | - | - | - | - | - | - | - | - | - | - | - | - | p | - | - | - | - | - | - | - |
| Same calculator fed by the listing's own date and local rent | - | - | - | - | - | - | - | - | - | - | - | - | - | - | - | - | - | - | - | - |
| Construction-cost indexation avoided, in money | - | - | - | - | - | - | - | - | - | - | - | - | - | - | - | - | - | - | - | - |
| **Trust and timing** | | | | | | | | | | | | | | | | | | | | |
| Overdue-delivery flag (past promised date) | - | - | - | - | - | - | - | - | - | - | - | - | - | Y | - | - | - | - | - | - |
| Developer on-time delivery record | - | - | - | - | - | - | - | - | - | - | - | - | - | p | - | - | - | - | - | - |
| Per-row checked-on or as-of date | p | Y | - | p | p | p | p | - | ? | - | - | ? | p | Y | ? | - | - | - | - | - |
| Immediate label checked against the stated date | - | - | - | - | - | - | - | - | - | - | - | - | - | p | - | - | - | - | - | - |
| Official proof of readiness (occupancy permit) | - | - | - | - | - | - | - | - | - | - | - | - | - | p | - | - | - | p | - | p |
| **Staying in touch** | | | | | | | | | | | | | | | | | | | | |
| Saved search or alerts | Y | Y | y | Y | Y | Y | ? | ? | Y | ? | ? | ? | ? | - | ? | ? | ? | Y | Y | - |
| Alert when a project becomes ready or its date slips | - | - | - | - | - | - | - | - | - | - | - | - | - | - | - | - | - | - | - | - |
| Compare projects side by side | - | - | - | - | - | - | - | - | - | - | - | - | Y | - | - | - | - | - | - | - |
| Languages beyond the local one | - | - | - | - | - | - | - | - | - | - | - | y | y | - | - | - | - | - | Y | - |

**Notes on the grid**
- Bayut's deal-price and ready-versus-off-plan rows are **p** because the Dubai Land Department transactions split by completion status sit in a separate market tab, not on the project card.
- Property Finder's incentive-in-money row is **p** because the money figure on cards is a mortgage cashback, not a developer deal valued against a schedule.
- Madlan **p** on incentive money and expiry: the developer writes the amount or the date into a free-text badge; Madlan does not normalise it.
- FAM **p** on the label-check row: it compares the announced handover with official progress, not marketing labels.
- Official proof of readiness: FAM uses official inspections of progress; Madlan and Africa Israel show building-permit milestones. None shows an occupancy permit (in Israel: טופס 4 or תעודת גמר).
- Outside the grid: Beike pays buyers for developer delays (China); a Dubai brokerage blog ranks developers by delivery rate; Dealplexus, PropertyNet SG and BeGoodTool are stand-alone ready-versus-paper calculators.

---

## 5. World-first candidates (strict)

A candidate is listed only if we looked for it and did not find it on any site above. Each line says where we looked and what came closest. These are claims about **what we could find on 9.11.2026**, not proof that nothing exists anywhere.

| # | Candidate | What we searched | Closest thing found (so it is not claimed more widely) |
|---|---|---|---|
| 1 | **A ready-versus-on-paper cost calculator on each listing, fed by that listing's real delivery month, the local rent for that room count, and the construction-cost index the buyer avoids** | English and Hebrew web searches for under-construction versus ready calculators, off-plan versus ready calculators, and a Hebrew search for a ready-versus-paper calculator with rent and indexation; filter panels of all portals in section 2 | Stand-alone, generic tools: Dealplexus (India), PropertyNet SG, BeGoodTool, Property Finder rent versus buy. All need the user to type the waiting years; none links to listings; none models a construction-cost index. In Hebrew we found only articles that work an example by hand (Mako) and separate index calculators (hon.co.il) |
| 2 | **Every developer deal turned into a money value against a normal payment schedule, shown on the card and comparable across projects** (20/80, no indexation, deferred payment, gifts) | Search for portals that value builder incentives; deal chips on Realtor, NHS offers, Madlan and Yad2 badges, SeLoger badges, Bayut and Property Finder payment plans | Realtor names deal types; NHS shows the offer text and its expiry; Bayut and Property Finder show payment-plan ratios; Property Finder shows a mortgage cashback amount; Madlan badges carry the developer's own amounts. Nobody computes the value |
| 3 | **An alert when a followed project moves to near or immediate occupancy, or when its delivery date slips** | Alert features on NHS, Zillow, Rightmove, Zoopla, Domain, Madlan, immobilier.co.il; a search for portal alerts on construction-status change | Saved-search, new-listing and price alerts everywhere. Builder software (Builder Signal) notifies people who already bought; it is not a portal alert |
| 4 | **A check that the immediate-occupancy label agrees with the stated delivery date and the project status, with the mismatch shown to the buyer** | Yad2 and Madlan labels, developer sites, FAM tracker | FAM flags projects past their announced handover (Dubai, official inspections). Nobody checks marketing labels. Real Israeli mismatches exist today: Shikun & Binui Ben Shemen on Yad2; Aura City Hadera still in marketing after occupancy began; a Tidhar project marked immediate with a delivery field of 7/2026 |
| 5 | **The price of each ready unit set against recorded deal prices for flats of the same size nearby, on the card** (in Israel: Tax Authority deals) | Card fields on all portals; Bayut transactions article; Zillow estimate module; NHS market snapshot | Bayut has official transactions split ready versus off-plan, by area and building, in a separate tab. Zillow shows `Not available` on plans. NHS shows average prices by city and ZIP. None puts the comparison on a new-build ready card |
| 6 | **An occupancy-permit proof line per building (טופס 4 or תעודת גמר) with its date and source** | Indian portals (search for occupancy-certificate filters), Madlan stage tracker, developer sites, FAM | India shows RERA registration badges, not occupancy certificates. Madlan and Africa Israel show building-permit milestones. FAM shows official progress percent. **Caveat:** in Israel this needs a public source per building; where none exists the line must be omitted, never guessed |

**The combination claim.** No column in the grid has more than a handful of the rows. No site combines a ready filter with time bands, a structured delivery date, units left, valued deals, a deal-price comparison, a waiting-cost calculator wired to the listing, status-change alerts, a label check and more than one language. A finder that does all of these would be the first such combination we could find.

## 6. Already done elsewhere (do not claim as first)

- Move-in time bands with a live count and a map: **NewHomeSource**.
- Ready / Off-Plan filter plus handover-by and percent-complete filters: **Bayut**.
- Official progress percent with an as-of month and a past-its-date flag: **FAM Properties**.
- Developer delivery-rate rankings: a **Dubai brokerage blog** (unverified).
- Platform-paid compensation for a late handover: **Beike** (Suzhou trial).
- Indexable delivered-now landing pages by region and type, with counts: **SeLoger Neuf**; also **Yahoo! Real Estate Japan** and **99acres** [search].
- Immediate-handover filter: **SUUMO**.
- Availability date and price per m² on every card: **Immowelt**.
- Ready-units table inside a project: **NewHomeSource, Zillow, Realtor, Redfin, Yad2, immobilier.co.il**.
- Offer with an expiry date: **NewHomeSource**.
- Generic ready-versus-paper or rent-during-construction calculators: **Dealplexus, PropertyNet SG, BeGoodTool**.
- Delivery-year filter and eight languages for Israeli new projects: **immobilier.co.il** (no ready-now option).
- A near-occupancy toggle and counted filter pages in Israel: **Yad2**.

## 7. What this means for the claim nad-lan can make

- **Safe to claim (with this file as proof):** the first finder we could find that values each developer deal in shekels, prices the cost of waiting from each project's own delivery month, local rent and the construction-cost index, alerts on a move to occupancy, and checks the immediate label against the stated date.
- **Also safe:** the first Israeli finder with time bands (now, up to 6 months, up to a year, on paper), a structured delivery month and a check date on every row, in four languages.
- **Not safe:** first move-in-ready filter, first delivery tracker, first developer track record, first ready-versus-paper calculator. Each exists somewhere (section 6).
- **Recheck before publishing any claim:** the blocked sites (Idealista, Fotocasa, Homes.com, 99acres, MagicBricks, Housing.com, PropertyGuru, Yad2 live filters, Madlan project pages, Domain project pages). Allowing them once in the Chrome permission prompt would let a follow-up read them.

## 8. Access log (9.11.2026)

| Site | Result |
|---|---|
| NewHomeSource, Zillow, Realtor.com, realestate.com.au, Domain hub | Read in Chrome [code] |
| Rightmove, Zoopla, OnTheMarket, SeLoger Neuf, ImmoScout24, Immowelt, Bayut, Property Finder, FAM, apartments.com.au, SUUMO, Yahoo! Real Estate Japan, EdgeProp SG, Dealplexus, PropertyNet SG, BeGoodTool, immobilier.co.il, BuyItInIsrael, nadlanmaster, Azorim, Tidhar, Aura, Africa Israel Residences | Read with WebFetch [fetch] |
| Homes.com | Blocked (Access Denied in Chrome) |
| Idealista | Blocked earlier today (CAPTCHA); search only |
| Fotocasa | Obra nueva URL tried returned a page-not-found message; search only |
| 99acres, MagicBricks, Housing.com, PropertyGuru | Blocked to WebFetch; Chrome permission prompt timed out; search only |
| Yad2 | Radware check on WebFetch; Chrome prompt timed out; facts from competitors.md and search |
| Madlan, Homeless | 403 on WebFetch; facts from competitors.md and search |
| Redfin, Domain project page | Chrome permission prompt timed out; facts from teardowns and search |
| Shikun & Binui Hebrew site | Certificate mismatch at shikunbinui.co.il; English corporate site read |
| Electra Residential, Dira Plus | Not located |
| Ashtrom Megurim | WebFetch truncated before the project list; facts from competitors.md |
