# Luxury Listing Page DNA
### Research brief for a bilingual (Hebrew RTL + English) listing template on nad-lan.co.il
Compiled 16 September 2026. Scope: high-end Tel Aviv and Herzliya Pituach apartments, mini penthouses and a private villa estate, for sale and for rent. Reader: high-net-worth local, returning-Israeli and foreign or diaspora buyers and renters.

---

## 0. How to read this report

- Evidence tags in square brackets (for example [CIRE-SOCAL]) map to full URLs in section 9. Every claim about buyer behavior or the market also carries its URL inline in section 6.
- All source text is paraphrased. No passages are reproduced.
- "Observed" means seen in the fetched page content or in the page's public HTML/CSS. "Not observed" means absent from what could be fetched, not proof of absence.
- Typography, color and image-ratio findings come from reading the public CSS and HTML of pages that the fetch tool could open (font-face declarations, CSS variables, hex frequency, aspect-ratio rules), not from screenshots.

### Access limits that shape the evidence
| Target | What happened | Substitute evidence used |
|---|---|---|
| sothebysrealty.com listing pages | Blocked by robots.txt for the fetch tool | Sotheby's International Realty Canada syndication of an Israel SIR villa [SIR-CA]; Israel SIR's own English and Hebrew sites [ISIR-EN1, ISIR-EN2, ISIR-HE]; titles of three sothebysrealty.com Israel listings from search results [SIR-COM1, SIR-COM2, SIR-COM3] |
| sothebys.ussl.co.il listing detail | Timeout (search page did load) | Search page [ISIR-USSL] |
| christiesrealestate.com | JavaScript shell only; no Israeli Christie's affiliate could be verified | Christie's International Real Estate Southern California affiliate listing [CIRE-SOCAL] |
| search.savills.com | HTTP 403 | Savills Portfolio listing [SAV-PORT]; a Savills-marketed listing on Rightmove [SAV-RM] |
| knightfrank.co.uk listing detail | JavaScript shell | KF sales index [KF-IDX], lettings index [KF-LET], KF brochure PDF [KF-BRO], KF listing on OnTheMarket [KF-OTM] |
| yad2.co.il detail pages | Bot protection | Yad1 new-projects index [YAD1]; public scraper schemas that document Yad2 fields [APIFY-YAD2, APIFY-YAD2B]; NBN Yad2 guide [NBN-YAD2] |
| madlan.co.il listing detail | JavaScript, metadata only | Madlan project page fetched in full [MADLAN-PRJ]; NBN Madlan tutorial [NBN-MADLAN]; scraper schema [APIFY-MADLAN] |
| Engel & Voelkers Israel | No Israel shop found on the global site [EV-HOME] | Two E&V expose pages (Spain, Italy) [EV-1, EV-2] |
| "Tzahi Levi" | Searches returned only unrelated individuals, no Israeli luxury brokerage | Excluded |
| Christie's 2026 report, NAR buyer profile | Gated downloads | Press coverage of the Christie's report [CIRE-26a, CIRE-26b]; NAR not used |

Israeli luxury brokerages verified through fetched pages: Israel Sotheby's International Realty; Anglo Saxon (its header carries a Luxury Apartments section and listings carry a "Luxury" label) [AS-SALE, AS-IDX]; Luxury Real Estate Israel [LREI]; Domestic Living Solutions / Domestic TLV [DOMESTIC]. Montefiore Real Estate Group and Alayof Group appear as listing brokers on Tel Aviv penthouses aggregated by LuxuryEstate [LUXEST].

---

## Executive summary: 12 findings that should drive the design

1. **One spine, with small variations.** The brands studied share the same backbone: gallery-led hero, title plus price plus 3 to 8 key facts, narrative, grouped specifications, location, agent card and form, similar listings, disclaimers. Variations are local (The Agency opens with a map widget; Compass inserts financial tools and public records). Brands differentiate mainly inside blocks.
2. **Facts beat adjectives.** The strongest openers pair one idea of scarcity or provenance with verifiable facts (building, architect, size, view) in the first sentence [SAV-RM, KF-OTM, CIRE-SOCAL].
3. **Cost of ownership is formalized abroad, missing in Israel.** UK pages list tenure, service charge, council tax, EPC and broadband [SAV-RM, KF-OTM]; US pages list HOA with an itemized list of what the fee covers, taxes and a payment calculator [COMPASS-1]. The Israeli pages observed, including a NIS 37,000 per month rental, omit arnona and va'ad bayit [AS-RENT, DOMESTIC]. This is the clearest opening for nad-lan.co.il.
4. **Israeli portals are strong on practical fields** (mamad, parking count, storage, elevator, floor X of Y, entry date, condition) [APIFY-YAD2, APIFY-MADLAN, AS-RENT]; **luxury brands are strong on story and design** [ISIR-EN1, CIRE-SOCAL]. The template must do both.
5. **Documented global priorities:** security (81% of Sotheby's affiliated agents cite it as a top concern), lifestyle and wellness (60%), turnkey condition, service and privacy [SIR-LO26, KF-WR26].
6. **Foreign buyers dominate Israeli luxury demand.** Nearly 60% of Israel's 2025 luxury transactions were by foreign residents, and Herzliya Pituach is back in focus [YNET-25]. English must be a first-class original, with USD/EUR display and square feet as a secondary unit.
7. **Buyer type changes the price of the same home.** Purchase tax for an additional apartment or a foreign resident is 8% up to NIS 6,055,070 and 10% above; olim pay 0.5% up to NIS 6,055,070 on a single residence; foreign residents face a 50% loan-to-value cap [BIZ-PT, YTAX, NBN-PT, ILAN]. A buyer-profile cost panel is a high-value differentiator that none of the studied sites offers.
8. **Luxury rentals sit outside the Fair Rental Law's core protections.** Its deposit caps and habitability rules apply only where rent is up to NIS 20,000 a month [KZ-HAB, KZ-GUAR], so the RENT page must spell out guarantees, lease term and who pays what.
9. **Visual DNA:** high-contrast serif for display, neutral sans for data, one accent, light warm grounds, large galleries with a curated lead image [KF-CSS, CIRE-SOCAL-SRC, EV-SRC, EV-1, COMPASS-1].
10. **Price is shown.** Numeric pricing is the norm in Israel and among brands; price on application appeared on 1 of 16 Tel Aviv penthouses on LuxuryEstate [LUXEST]. UK brands use qualifiers such as Guide price or Offers in excess of [KF-IDX].
11. **RTL is under-engineered even at the top.** Israel SIR and Anglo Saxon set direction through body classes or CSS rather than on the html element; the market is split on whether the shekel sign precedes or follows the number [ISIR-HE, AS-HE, W3C-DIR].
12. **Honesty signals are becoming standard.** Engel & Voelkers labels AI-modified images; Compass warns that photos may be virtually staged [EV-1, COMPASS-1].

---

## 1. Section order of a top luxury listing page

### 1.1 Observed order, site by site

**Sotheby's International Realty, global syndication of an Israel SIR villa in Herzliya Pituach [SIR-CA]**
1. Header with language and currency selector
2. Hero image with share (email, Facebook, X, Pinterest, LinkedIn)
3. Title showing area and country only, price converted to Canadian dollars
4. Key facts: property ID, original price in ILS, type, style, living area, lot size, bedrooms, bathrooms
5. Description (architecture, systems such as VRF and heated floors, pool, wine cellar, location)
6. Amenities tags
7. Listing agent card (name, office phone, contact link)
8. Contact form (name, email, phone, question, consent boxes)
9. Neighborhood module (request area data, five-minute walk radius)
10. Brokerage block (office address and phone)
11. Similar properties (12) with a see-all link
12. Footer disclaimers (measurement footnote, fair housing, company structure)

sothebysrealty.com Israel listing titles (search results): superlative plus type plus signature amenity plus project or area, for example a superlative sea-view penthouse tied to a named Jaffa project, a two-level Tel Aviv penthouse sold on its pool and sea panorama, and investment-led wording for a Herzliya Pituach property [SIR-COM1, SIR-COM2, SIR-COM3].

**Israel Sotheby's International Realty, English and Hebrew sites [ISIR-EN1, ISIR-EN2, ISIR-HE, ISIR-USSL]**
1. Gallery hero with thumbnails and full-screen view (about 16 images)
2. Title (type, view, neighborhood) and location line
3. Price in ILS and USD together
4. Key details: property type, interior m2, balcony or terrace m2
5. Features and amenities: bedrooms, full baths, balconies, parking, plus tags (VRF air conditioning, mamad, private elevator, smart home, sea view, storage, walk-in closet, designer kitchen, privacy, beach access)
6. Description (floors, exposures, terrace areas, suites, named furniture brands). Sold listings stay live with a bilingual Sold line
7. Agent card (photo, name, office phone, office email, agent ID, a first-person request-information button)
8. SEO tags in English and Hebrew
9. Similar properties (6)
10. Disclaimer (information supplied by third parties and not guaranteed) and copyright

The portal version adds Buy, Rent, Commercial, Projects and International sections, English, Hebrew and Russian, map view and WhatsApp [ISIR-USSL].

**Christie's International Real Estate, Southern California affiliate [CIRE-SOCAL]**
1. Hero gallery with a see-all-photos link
2. Status badge, street address as headline, price
3. Tabs: Photos, Map, Street View; share buttons
4. Key facts (beds, baths, acres) and an Inquire button
5. Description led by the architecture firm's name
6. Grouped features: Interior; Area and Lot (status, lot, MLS ID, neighborhood, style, views); Exterior (stories, pool type, parking, heating, cooling); Financial (price, zoning)
7. Schedule a showing (in person or by video chat, time slot, contact, consent)
8. Mortgage calculator (price, term, down payment, property tax, rate, HOA)
9. Two agent cards (photo, title, phone, protected email, state license number)
10. Press and media (three articles about the listing)
11. Brand block with contact call to action
12. Footer form (interest: buy, sell, rent), offices, company license, disclaimers

**Engel & Voelkers expose [EV-1, EV-2]**
1. Breadcrumb (country, region, town)
2. Gallery (63 images on EV-1, several flagged as AI-generated or AI-modified)
3. Title, price and key metrics (rooms, bedrooms, bathrooms, total surface, living area, completion date)
4. Description
5. Feature tags (air conditioning, garage, sea view, security system, terrace, open view, covered parking)
6. Details table (object type, floor, number of floors, garages, parking spaces, flooring, property ID)
7. Energy block (construction year, certificate available, energy class, energy source)
8. Location narrative
9. Floor plans (EV-2)
10. Shop card (shop name, advisor, legal provider entity, phone, imprint, privacy link)
11. Contact form with data-processing consent and two separate newsletter opt-ins
12. Nearby properties (4)

Repeated calls to action: Request details, Add to favorites, Share.

**Knight Frank [KF-IDX, KF-LET, KF-BRO, KF-OTM]**
- Brochure order: price and tenure block (guide price, tenure and lease years, service charge, ground rent, local authority, council tax, bedrooms, bathrooms, receptions), description, location and transport, office address with two named agents (direct phone and email each), then an Important Notice (particulars not binding, photos indicative, dates of particulars and photographs).
- Portal listing adds six key-feature bullets, EPC rating, broadband speed and a brochure PDF.
- Sales index shows price qualifiers (Guide price, Asking Price, Offers in excess of, Prices from for developments) and statuses such as Sold STC.
- Lettings index shows weekly or monthly rent, a separate short-let rent, and labels such as Managed and Long and Short Let.

**Savills [SAV-PORT, SAV-RM]**
- Portfolio (luxury editorial page): property type as headline, location breadcrumb, a one-line hero statement, price, bedrooms and bathrooms beside a named agent's contact details, a property-details button, three-image gallery, an about-this-property section, highlights bullets, nearby facilities with distances (schools, restaurants, airport), second button, share.
- Savills listing on Rightmove: guide price, type, bedrooms and bathrooms, size in both sq ft and m2, tenure and lease years, service charge per sq ft plus a separate parking service charge, ground rent, council tax band, EPC, six key features (floor and views, terrace area, interiors, 24-hour concierge and security and valet, spa, pool, gym, cinema), material information (parking, garden, accessibility, utilities, broadband, flood risk), floorplan, request details, mortgage in principle.

**Compass [COMPASS-1, COMPASS-2]**
1. Gallery (98 photos on COMPASS-1)
2. Address and status
3. Key facts panel
4. Description
5. Location
6. Payment calculator (principal and interest, property taxes, HOA dues)
7. Property information (dozens of structured fields, see section 2)
8. Property history
9. Public records (tax, taxable value)
10. Schools (ratings, grades, distance)
11. Similar homes
12. Nearby home values
13. Explore nearby
14. Footer (state licenses, disclaimers)

COMPASS-2 adds a comparable-sales module (median sold price, average days on market, sale-to-list ratio).

**The Agency [AGENCY]**
Map widget, share, title and status, primary image, key facts bar (beds, baths, sq ft, type, status, MLS number), description, videos and tours, floor plan, flyers, agent card (presented-by format), showing request form, similar-properties interest form, agent card repeated, property map, similar listings (login-gated), footer disclaimer.

**Anglo Saxon, Israel [AS-SALE, AS-RENT, AS-HE]**
Header (Hebrew, English, French; Luxury Apartments section; national short number), templated title (type, rooms, street, area, city), opening description, details (price, rooms, area, floor X of Y, balconies, entry date), characteristics (air conditioning, parking, elevator, balcony, mamad, storage), type and property ID, call button, share by WhatsApp, Facebook and email, contact form, gallery (5 images on AS-SALE), more properties from the same branch area, footer with app links. The rental example adds the agent's name and spoken languages [AS-RENT].

**Madlan [MADLAN-PRJ, NBN-MADLAN, APIFY-MADLAN]**
- Project page: project name and location, developer with linked profile, buildings, floors, units, construction type, status timeline (initial planning, permit application, permit granted, construction completed), architect, more projects nearby (room range, floors, price from, contact), transaction history table (address, distance, date, price, area, NIS per m2, rooms, floor, year built, brokered or not), area averages (average NIS per m2, rental yield), nearby neighborhoods, school links.
- Listing modules per the NBN tutorial: asking price next to an estimated value, building and neighborhood transactions, price per m2 over time, condition, school rankings, socio-economic data, public transport, resident ratings.

**Yad2 and Yad1 [YAD1, APIFY-YAD2, APIFY-YAD2B]**
- Yad1 project cards: name and address, room range, price from, m2, floors, status (on sale, near occupancy), financing promotion.
- Listing data model: deal type, private or agency, property type, address, price, rooms, floor, total floors, area and built area, condition, elevator, parking count, balcony, safe room, images, video URL, contact, agency name, licence number, exclusive flag, publish and update dates, entry date.

**Israeli boutique luxury [LREI, DOMESTIC]**
- Luxury Real Estate Israel: language flags (Hebrew, French, Russian, English), status, ID plus title, description, details (type, terrace m2, built m2, bedrooms), feature tags (first line to the sea, sea access, pool, gym, smart electrical system, elevator, underground parking, 24-hour guard, sea view), price with EUR, GBP and ILS switch, agent card titled licensed broker with email form and WhatsApp, print, tell-a-friend, newsletter.
- Domestic TLV: headline, opener, details (price, type, area, m2, rooms, terrace, elevator, parking, mamad), key features (built versus terrace split, 7-meter double height, shell condition, concierge, pool, gym), office card (address, phone, email, WhatsApp promising an immediate reply; no license number shown), inquiry form with privacy consent, similar filters.

### 1.2 What the comparison shows
- **Universal:** gallery-first hero; price and a handful of facts above the fold; narrative; grouped specifications; agent card with form; similar listings; disclaimers.
- **Two philosophies:** luxury brands put story before the spec sheet [CIRE-SOCAL, ISIR-EN1, SAV-PORT]; data-led platforms put tools and records next to the story (calculator, history, public records, schools at Compass; transactions and yield at Madlan) [COMPASS-1, MADLAN-PRJ].
- **Cost transparency is regional:** UK and US pages formalize service charge, council tax, HOA and taxes [SAV-RM, KF-OTM, COMPASS-1]; the Israeli pages observed do not [AS-RENT, DOMESTIC].
- **Address discretion is regional:** US and UK titles are street addresses [CIRE-SOCAL, KF-IDX]; Israeli listings and Sotheby's syndication of Israeli homes use neighborhood or project only [SIR-CA, ISIR-EN1].
- **Agent cards vary most:** richest at the Christie's affiliate (photo, title, license number) [CIRE-SOCAL]; thinnest on Israeli boutique sites (office phone, no license number) [DOMESTIC].
- **Sold stays live as social proof:** Israel SIR, Luxury Real Estate Israel, Knight Frank (Sold STC) and Compass (closed price) [ISIR-EN2, LREI, KF-IDX, COMPASS-1].

### 1.3 Synthesized best-practice order for nad-lan.co.il
| # | Block | Borrowed from |
|---|---|---|
| 1 | Utility bar: breadcrumb (city, neighborhood, project), HE/EN switch, save, share | E&V breadcrumb, Compass explore links |
| 2 | Hero: curated lead image or short silent loop, status badges, title, micro-location, price line, media tabs (photos, video, floor plan, map, 3D) | Christie's affiliate tabs, Israel SIR dual price |
| 3 | Key facts bar (6 to 8 facts; icons allowed only here) | All |
| 4 | Primary call-to-action module: private viewing, WhatsApp, call, brochure (sticky rail on desktop, bottom bar on mobile) | Christie's showing form, Israeli WhatsApp norm |
| 5 | The story: one-line dek, short narrative, six signature features | Savills and Knight Frank key features, Christie's narrative |
| 6 | Sequenced gallery with captions and editing labels | E&V AI labels, Compass photo depth |
| 7 | Plans and areas: floor plans, area table | E&V floor plans, The Agency floor plan section |
| 8 | Residence details: grouped specification table | Christie's grouped features, Compass property information |
| 9 | Building, services and security | Savills key features, Compass amenities and security |
| 10 | Location: map, walking times, schools, planned changes | Sotheby's walk radius, Savills distances, Compass schools |
| 11 | SALE: Costs and ownership. RENT: Lease terms and monthly costs | UK material information, US payment calculator, Israeli law (section 6) |
| 12 | Legal and documents status | Israel-specific checks (section 6) |
| 13 | Market context (source-linked, explicitly not a valuation) | Madlan transactions, Compass comparables |
| 14 | Agent card and private viewing form | Christie's agent card, E&V consent handling |
| 15 | Similar and recently sold nearby | Sotheby's, Israel SIR, E&V |
| 16 | FAQ (optional) | New |
| 17 | Disclaimers, listing ID, last updated | Knight Frank Important Notice, Compass disclaimers |

---

## 2. Data fields

Class: **S** = standard (most studied sites show it). **D** = differentiator (few show it, high value). **IL** = Israel-specific. Hebrew labels are suggested, drawn from observed Israeli pages where possible.

### 2.1 Identity, status and media
| Field | Class | Hebrew label | Seen at |
|---|---|---|---|
| Listing / property ID, MLS number | S | מספר נכס | SIR-CA, EV-1, EV-2, COMPASS-1, CIRE-SOCAL, AS-SALE, LREI |
| Status (for sale, under offer, sold, closed) | S | סטטוס | CIRE-SOCAL, ISIR-EN2, KF-IDX, COMPASS-1 |
| Exclusive mandate flag | D (common on Israeli portals) | בבלעדיות | APIFY-YAD2 |
| Property type and sub-type (penthouse, mini penthouse, duplex, garden apartment, villa) | S | סוג הנכס | all |
| Architectural style | D | סגנון | SIR-CA, CIRE-SOCAL |
| Listed / published / updated date | D on brand sites, S on portals | עודכן בתאריך | AGENCY, APIFY-YAD2 |
| Days on market | D (data platforms; comparables only at Compass) | ימים בשוק | COMPASS-2 |
| Photo count; video URL; virtual tour; floor plan images; brochure or flyer | S photos, D the rest | | COMPASS-1, EV-1, AGENCY, APIFY-YAD2B, APIFY-MADLAN, KF-OTM |
| Image editing disclosure (AI-modified, virtually staged) | D | תמונה מעובדת / הדמיה | EV-1, COMPASS-1 |
| Press coverage of the listing | D | בתקשורת | CIRE-SOCAL |

### 2.2 Price and costs
| Field | Class | Hebrew label | Seen at |
|---|---|---|---|
| Price, numeric | S | מחיר | all |
| Price qualifier (guide, asking, offers in excess of, prices from) | S in UK, D elsewhere | | KF-IDX |
| Price on application | D, rare | מחיר לפי בקשה | LUXEST (1 of 16) |
| Second currency or currency switcher | D | | ISIR-EN1 (ILS + USD), AS-LEGACY (NIS, USD, EUR, GBP), LREI (EUR, GBP, ILS), SIR-CA (CAD with original ILS kept) |
| Price per m2 or sq ft | D on brand sites, S on data platforms | מחיר למ״ר | COMPASS-1, MADLAN-PRJ |
| Price history | D | היסטוריית מחיר | COMPASS-1, APIFY-MADLAN |
| Estimated value next to asking | D | הערכת שווי | NBN-MADLAN |
| Management fee / HOA / service charge, with what it includes | S in US and UK, not observed on Israeli pages | דמי ניהול / ועד בית | COMPASS-1 (itemized), KF-BRO, SAV-RM (per sq ft) |
| Parking service charge | D | דמי חניה | SAV-RM |
| Property tax (annual and monthly estimate) or council tax band | S in US and UK | ארנונה | COMPASS-1, KF-OTM |
| Tenure, lease years, ground rent | S in UK | | KF-BRO, SAV-RM |
| Payment or mortgage estimate | D | מחשבון משכנתא | CIRE-SOCAL, COMPASS-1, SAV-RM |
| Purchase tax estimate by buyer type | IL, D (not observed anywhere) | אומדן מס רכישה | KZ-PT, BIZ-PT |
| Rental yield | D | תשואה | MADLAN-PRJ |

### 2.3 Size and layout
| Field | Class | Hebrew label | Seen at |
|---|---|---|---|
| Interior / built area | S | שטח בנוי | ISIR-EN1, SIR-CA, EV-1, DOMESTIC |
| Balcony / terrace area and count | S in Israel, D abroad | שטח מרפסות / מספר מרפסות | ISIR-EN1, AS-RENT, COMPASS-1 |
| Total surface versus living area | D | שטח כולל | EV-1 |
| Lot / plot area | S for houses | שטח מגרש | SIR-CA, CIRE-SOCAL |
| Rooms (Israeli count, half-room steps such as 3.5) | S, IL | חדרים | AS-RENT, AS-IDX, APIFY-YAD2 |
| Bedrooms; bathrooms split full, three-quarter, half; reception rooms | S abroad | חדרי שינה / חדרי רחצה | CIRE-SOCAL, KF-BRO, ISIR-EN1 |
| Suites and primary-suite detail | D | סוויטות / מאסטר | ISIR-EN1 |
| Levels (duplex, triplex) | D | מפלסים | COMPASS-1 |
| Ceiling height | D | גובה תקרה | DOMESTIC (7 m double height), SIR-CA |
| Floor plan | S at brands | תוכנית הנכס | EV-2, AGENCY |

### 2.4 Position, view and orientation
| Field | Class | Hebrew label | Seen at |
|---|---|---|---|
| Floor and total floors | S, IL | קומה X מתוך Y | AS-RENT, EV-1, APIFY-MADLAN |
| Corner unit, full-floor unit | D | דירה פינתית / קומה שלמה | COMPASS-1, ISIR-EN2 |
| View list (sea, park, skyline) | S | נוף | COMPASS-1, CIRE-SOCAL, ISIR-EN2 |
| Orientation / exposures | D | כיווני אוויר | ISIR-EN1, KF-BRO |
| Waterfront, first line to sea, beach access | D | קו ראשון לים / גישה לחוף | COMPASS-1, LREI, ISIR-EN2 |

### 2.5 Building, services and security
| Field | Class | Hebrew label | Seen at |
|---|---|---|---|
| Building or project name, developer, architect | D (S on Israeli project pages) | פרויקט / יזם / אדריכל | COMPASS-1, MADLAN-PRJ, CIRE-SOCAL |
| Year built, completion date, construction status | S | שנת בנייה / מועד אכלוס | COMPASS-1, EV-1, MADLAN-PRJ |
| Building size (stories, units) | D | קומות / יחידות | COMPASS-1, MADLAN-PRJ |
| Amenities (pool, spa, gym, cinema, lounge) | S | מתקני הבניין | COMPASS-1, SAV-RM, LREI |
| Concierge, doorman, valet | D | קונסיירז׳ / לובי מאויש | SAV-RM, COMPASS-1 |
| Security detail (CCTV, patrol, secured garage, 24-hour guard) | D | אבטחה | COMPASS-1, LREI |
| Elevator; private elevator | S; D | מעלית / מעלית פרטית | APIFY-YAD2, ISIR-EN2 |
| Shabbat elevator | IL, D | מעלית שבת | KZ-SHABBAT |
| Pet policy | D | חיות מחמד | COMPASS-1 |
| Broadband | D | תשתית סיבים | KF-OTM |
| Energy rating, certificate, source | S in EU and UK | דירוג אנרגטי | EV-1, EV-2, KF-OTM, SAV-RM |

### 2.6 Parking, storage, safety and systems
| Field | Class | Hebrew label | Seen at |
|---|---|---|---|
| Parking count and type (garage, underground, assigned, valet) | S | חניות | COMPASS-1, CIRE-SOCAL, ISIR-EN1, APIFY-YAD2 |
| Storage room | S, IL | מחסן | ISIR-EN1, AS-RENT, APIFY-MADLAN |
| Mamad (reinforced safe room), count | S, IL | ממ״ד | ISIR-EN1, ISIR-EN2, DOMESTIC, APIFY-YAD2 |
| Heating and cooling (central, VRF, underfloor) | S | מיזוג / חימום תת רצפתי | COMPASS-1, SIR-CA, ISIR-EN1 |
| Smart home | D | בית חכם | ISIR-EN1, LREI |
| Flooring, kitchen maker, appliances | D | ריצוף / מטבח / מכשירים | COMPASS-1, CIRE-SOCAL |
| Accessibility | D | נגישות | APIFY-MADLAN, SAV-RM |

### 2.7 Condition and timing
| Field | Class | Hebrew label | Seen at |
|---|---|---|---|
| Condition (new, renovated, needs renovation, shell) | S, IL | מצב הנכס | APIFY-YAD2, DOMESTIC |
| Entry date or availability | S, IL | תאריך כניסה | AS-SALE, AS-RENT, APIFY-YAD2B |
| Furnished | S for rentals | ריהוט | APIFY-MADLAN, COMPASS-1 |

### 2.8 Legal and records
| Field | Class | Hebrew label | Seen at |
|---|---|---|---|
| Tenure / where rights are registered | S in UK; IL, D | רישום זכויות (טאבו / רמ״י / חברה משכנת) | KF-BRO, YASMINT |
| Parcel number, zoning | D | גוש / חלקה / ייעוד | COMPASS-1, CIRE-SOCAL, GOV-TABU |
| Public tax records | D | | COMPASS-1 |
| Flood zone or flood risk | D in US and UK | | COMPASS-1, SAV-RM |
| Occupancy approval (Tofes 4) | IL, D | טופס 4 | NC-T4 |
| Developer security under the Sale Law (new builds) | IL, D | בטוחה לפי חוק המכר | WS-SALELAW |

### 2.9 Location and market
| Field | Class | Hebrew label | Seen at |
|---|---|---|---|
| Neighborhood and breadcrumb | S | שכונה | EV-1, COMPASS-2 |
| Walk radius or distances to amenities | D | זמני הליכה | SIR-CA, SAV-PORT |
| Schools with rating and distance | D | מוסדות חינוך | COMPASS-2, NBN-MADLAN |
| Public transport | D | תחבורה ציבורית | KF-BRO, NBN-MADLAN |
| Comparable sales / transaction table | D | עסקאות באזור | COMPASS-2, MADLAN-PRJ |
| Socio-economic data, resident ratings | D (Israeli platform) | | NBN-MADLAN |

### 2.10 Rental-specific
| Field | Class | Hebrew label | Seen at |
|---|---|---|---|
| Rent period (weekly or monthly) and short-let rent | S | שכר דירה חודשי | KF-LET |
| Let type (long let, short let, managed) | S in UK | סוג שכירות | KF-LET |
| Minimum lease period, leases allowed per year | D | תקופת שכירות מינימלית | COMPASS-1 |
| Roommates allowed | IL portal field | מתאים לשותפים | APIFY-YAD2 |
| Guarantees, deposit, broker fee, who pays arnona and va'ad bayit | IL, D (not observed on any listing) | ערבויות / דמי תיווך / תשלומים שוטפים | KZ-GUAR, NC-RENT |

**Takeaway for the template:** the Israeli standard set (rooms, built m2, balcony m2, floor X of Y, parking, storage, mamad, elevator, condition, entry date) is the floor. The differentiators that none of the Israeli pages studied combines are: exposures, ceiling height, management fee with inclusions, arnona, registration status, Tofes 4, buyer-type purchase tax, lease terms, image-editing labels, and source-linked market context.

---

## 3. Visual language

### 3.1 Typography, read from public CSS
| Site | Display / heading | Text / data | Notes |
|---|---|---|---|
| Knight Frank [KF-CSS] | Tiempos Headline (serif) | Suisse Intl (sans) | Heading variable used 16 times, body variable 131 times in the base stylesheet |
| Compass [COMPASS-CSS] | Compass Serif (defined in design tokens) | Compass Sans; Inter; Open Sans as the "legible" family | Also loads Material Symbols icons for chair, car, pets, resize, calendar, handyman |
| Christie's affiliate, Luxury Presence platform [CIRE-SOCAL-SRC] | Didot LT Std and Cormorant Garamond (serif) | Gilroy and Montserrat (sans) | Primary family variable is the serif, secondary is the sans |
| Engel & Voelkers [EV-SRC] | Proprietary EngelVoelkersHead (serif fallback Georgia) | Proprietary EngelVoelkersText (sans fallback Arial) | |
| Savills Portfolio [SAV-PORT-CSS] | Adobe Caslon Pro (serif) | | Loaded through an Adobe Fonts kit |
| Israel SIR, English [ISIR-EN1-SRC] | Open Sans Condensed | Arial | Font Awesome 4.7 icons |
| Israel SIR, Hebrew [ISIR-HE-SRC] | Open Sans Hebrew | | |
| Anglo Saxon [AS-HE-SRC] | Open Sans plus a custom font file | | Font Awesome |
| Madlan [MADLAN-LST-SRC] | NovemberHebrew (sans) | | |

**Pattern:** international luxury brands pair a high-contrast serif for display with a neutral grotesque or geometric sans for data. Every Israeli site whose CSS was inspected (Israel SIR, Anglo Saxon, Madlan) uses sans only, so a Hebrew editorial serif voice is an open position.

**Hebrew-capable fonts, verified through the Google Fonts API (Hebrew subset present) [GFONTS]:** serif: Frank Ruhl Libre, David Libre, Noto Serif Hebrew, Bellefair; sans: Heebo, Assistant, Rubik, Noto Sans Hebrew, IBM Plex Sans Hebrew. Cormorant Garamond and Playfair Display have no Hebrew subset, so if either is chosen for English it needs a Hebrew twin.

**Recommended pairings (design recommendation):**
- Editorial classic: Frank Ruhl Libre for titles and deks in both scripts, Assistant or Heebo for facts, tables and UI.
- Modern couture: Bellefair for display (one family covers Hebrew and Latin), IBM Plex Sans Hebrew for data.
- Numbers (prices, areas, floors) always in the sans with tabular figures where the font supports them (font-variant-numeric), never in a display serif.

### 3.2 Color, read from public CSS
| Site | Grounds and text | Accent | Evidence |
|---|---|---|---|
| Knight Frank | White and black variables, warm neutrals (#f0f0e4, #e2e2cb), charcoal #373a36 | Red #d0103a (most frequent hex in the base stylesheet) | [KF-CSS] |
| Christie's affiliate | Warm off-white #fbf9f7, charcoal #4d4d4d, near-black #1a1a1a | Bronze gold #b58d4a (most frequent color in page CSS) | [CIRE-SOCAL-SRC] |
| Engel & Voelkers | Light grays #f4f4f4 and #f0f0f0, charcoal #262626, warm beige #fff8e8 / #efe8df | Red #c80000 / #e60000 | [EV-SRC] |
| Compass | Black token #000 | Blue token scale (#003375 and lighter steps) | [COMPASS-CSS] |

**Pattern:** light, warm-neutral grounds, near-black text, one accent used sparingly for calls to action, rules and status.

**Contrast warning (computed with the WCAG formula):** the Christie's-style bronze #b58d4a on warm off-white measures 2.91:1, and white text on it 3.06:1, which fails the 4.5:1 requirement for body text. A darker brass such as #8a6a3b measures 4.71:1 on #faf8f5 (and white on it 4.99:1); #7a5a2e reaches 5.95:1.

**Suggested tokens (recommendation):** ground #faf8f5; surface #ffffff; ink #1c1c1c (16.08:1 on ground); secondary text #5e5a55 (6.45:1); hairlines #e6e1da; accent brass #8a6a3b for small text and rules; deep Mediterranean blue #1f3a4d for primary buttons (white text 11.86:1). Hairline-gray #8c8780 (3.36:1) only for non-text decoration.

### 3.3 Layout, whitespace and image ratios
- E&V image containers use a 3:2 aspect ratio (39 declarations on the expose page) [EV-SRC]; the Christie's affiliate hero uses 25:14, close to 16:9 [CIRE-SOCAL-SRC]; Compass declares a wide 16:7 ratio [COMPASS-SRC].
- Photo depth at the top: 98 photos at Compass, 63 at E&V; Israeli pages are thinner, about 16 at Israel SIR and 5 on an Anglo Saxon listing [COMPASS-1, EV-1, ISIR-EN1, AS-SALE].
- Recommendation: hero 16:9 on desktop and 4:5 on mobile; gallery images 3:2; text measure about 60 to 75 characters; one idea per viewport on mobile; generous vertical spacing between blocks, tight spacing inside fact tables.

### 3.4 Photography, video and tours
- Observed: dedicated videos-and-tours, floor plan and flyers sections [AGENCY]; virtual tour link [COMPASS-1]; map and Street View tabs next to photos [CIRE-SOCAL]; showings by video chat [CIRE-SOCAL]; video URLs and floor plan images in Israeli portal data models [APIFY-YAD2B, APIFY-MADLAN]; per-image AI labels [EV-1]; virtual staging warning [COMPASS-1].
- Drone footage was not observable in fetched text, so no claim is made about its prevalence.
- Recommended shot sequence: arrival or building, the defining view, living and dining, kitchen, primary suite, terraces at golden hour, secondary bedrooms, amenities, neighborhood (beach, promenade, park). Caption each with room, floor and orientation. For the villa estate add aerial context and a twilight exterior. Label every virtually staged or digitally altered image on the image itself.

### 3.5 Maps
- Observed: map plus Street View tabs [CIRE-SOCAL]; map widget at the top and a property map lower down [AGENCY]; five-minute walk radius [SIR-CA]; nearby facilities with distances [SAV-PORT]; schools with distances [COMPASS-2].
- Israeli luxury listings withhold the street [ISIR-EN1, SIR-CA].
- Recommendation: muted monochrome basemap; an approximate-area circle rather than a pin until a viewing is booked; walking-time chips for beach, promenade, park, schools, transit; no Street View for private homes.

### 3.6 Icons
- Observed: Compass loads a Material Symbols subset (chair, car, pets, resize, calendar) for compact facts [COMPASS-SRC]; Knight Frank's lettings index pairs bedrooms and bathrooms with icons [KF-LET]; Israel SIR and Anglo Saxon load Font Awesome [ISIR-EN1-SRC, AS-HE-SRC].
- Recommendation: one thin-line icon set, used only in the key facts bar and amenity chips. Narrative and specification tables stay text-only. In Hebrew, mirror directional icons (arrows, chevrons) but not objects (car, bed, safe room).

### 3.7 How price is shown
| Pattern | Where |
|---|---|
| Large numeric price near the title | CIRE-SOCAL, COMPASS-1, EV-1, AS-SALE, MADLAN-LST |
| Two currencies side by side (ILS and USD) | ISIR-EN1, ISIR-HE |
| Currency switcher (NIS, USD, EUR, GBP) | AS-LEGACY, LREI |
| Converted price plus the original ILS price as a separate field | SIR-CA |
| Qualifiers: Guide price, Asking Price, Offers in excess of, Prices from | KF-IDX |
| Price on application: 1 of 16 Tel Aviv penthouses | LUXEST |
| Rent: weekly or monthly, plus a separate short-let rent | KF-LET |
| Sold price or Sold label kept visible | COMPASS-1, ISIR-EN2, LREI |

Recommendation: numeric price by default. "Price on request" only when the owner insists, paired with a one-step "request price" form. Rentals show monthly rent plus a payment-terms line.

### 3.8 Light or dark
All palettes read from CSS are light-dominant with dark text [KF-CSS, CIRE-SOCAL-SRC, EV-SRC]. Recommendation: light pages; reserve dark for a twilight hero overlay, the sticky mobile call-to-action bar and full-screen gallery mode, where photography benefits and Hebrew small text is not at stake.

---

## 4. Copywriting DNA

### 4.1 Tone
- Third person, declarative, calm. At most one superlative per opener, immediately backed by a fact [SAV-RM, KF-OTM, CIRE-SOCAL].
- Proper nouns carry prestige better than adjectives: architecture firms, designers, building names, furniture brands [CIRE-SOCAL, COMPASS-1, ISIR-EN1].
- Israeli portal copy tends toward adjective stacking and compressed benefit lists [AS-SALE]; Israel SIR's English is calmer and location-first [ISIR-EN1]. Israeli boutique luxury pages rely on feature tags such as first line to the sea, sea access, pool, gym, 24-hour guard [LREI].

### 4.2 Headline patterns (paraphrased)
| Pattern | Shape | Where |
|---|---|---|
| Address as title | street number, street, city or postcode | CIRE-SOCAL, COMPASS-1, KF-IDX |
| Type + signature feature + micro-location | two-level penthouse, its sea view, and the northern Tel Aviv area | ISIR-EN1, ISIR-TAG |
| Superlative + type + amenity + project | a superlative, the sea view, the type and a Jaffa project name | SIR-COM1, SIR-COM2 |
| Investment framing | investment-led wording plus Herzliya Pituach | SIR-COM3 |
| Type only, editorial | the single word Penthouse as the headline | SAV-PORT |
| Type + view, short | the type followed by the view (two-level penthouse, sea panorama) | EV-1 |
| Templated portal | type, room count, street, area, city | AS-SALE |
| ID + type + intensifier + place | listing number, penthouse, super luxury, on the sea, city | LREI |

**Rule for nad-lan.co.il:** [type] + [one irrefutable differentiator with a number or proper noun] + [micro-location]. Up to about 8 words in English and 7 in Hebrew. No superlatives in the title; the dek carries emotion.

Illustrative titles written for the broker's current listings (facts taken from batch1_notes.md, verify before publishing):
- EN: Mini Penthouse with a 76 m² Terrace, Kochav HaTzafon / HE: מיני פנטהאוז עם מרפסת 76 מ״ר, כוכב הצפון
- EN: Private Estate on 1.1 Dunam, Herzliya Pituach / HE: אחוזה פרטית על 1.1 דונם, הרצליה פיתוח
- EN: Sea-View 5-Room Residence, B.S.R Towers, Sarona / HE: דירת 5 חדרים עם נוף פתוח לים, מגדלי B.S.R שרונה
- EN: Double-Height Mini Penthouse, First Line to the Sea / HE: מיני פנטהאוז בגובה כפול, קו ראשון לים

### 4.3 Opening lines: archetypes (paraphrased)
| Archetype | What the example does | Source | Verdict |
|---|---|---|---|
| Provenance | Names the architecture firm first, then positions the estate as defining contemporary design with resort-style living | CIRE-SOCAL | Strong for the villa |
| Scarcity + pedigree | Calls the penthouse irreplaceable, names the designer behind the building and the micro-neighborhood, claims a new benchmark | COMPASS-1 | Strong if the claim is defensible |
| Rarity + fact stack | One sentence carries rarity, bed and bath count, terraces, park and skyline views, and total size | SAV-RM | Best model for penthouses |
| Plain factual anchor | Building name plus exact size, a single adjective | KF-OTM | Best model for quiet confidence |
| Location-first | Leads with the neighborhood's desirability; the body adds exposures, terrace areas, furniture brands | ISIR-EN1 | Good for Israeli neighborhoods known abroad |
| Regional framing | Places the villa in a Mediterranean Riviera lifestyle, then lists systems (VRF, heated floors, wine cellar) | SIR-CA | Good for foreign buyers |
| Buyer fit | Steps from the sea, then states who the home suits (move-in-ready seaside living) | EV-2 | Useful for rentals |
| Sensory "imagine" | Invites the reader to imagine waking to the view | EV-1 | Avoid, it is the category cliché |
| Adjective stacking | Street and landmark followed by a run of adjectives | AS-SALE | Avoid |

**Opening-sentence formulas (recommendation):**
- A, the one thing plus proof: [defining attribute], [proof in numbers], [micro-location].
- B, provenance: [architect or developer] + [what they made] + [where].
- C, the life around it: [minutes on foot] to [beach, promenade, park] + [what the home gives daily].

### 4.4 Length and structure
- Luxury brands run multi-paragraph narratives plus long grouped feature lists [CIRE-SOCAL, COMPASS-1]. UK brands add six key-feature bullets above or beside the description [SAV-RM, KF-OTM]. Israeli portals use one short paragraph [AS-SALE, AS-RENT].
- Recommendation: dek of one sentence (up to 25 words); narrative of 150 to 250 words per language in three paragraphs: (1) the defining quality (view, scale, provenance), (2) plan and light (flow, exposures, suites, ceiling height), (3) life around it (building services, walking times); then six signature features, each containing a number or a proper noun.

### 4.5 Cliche control (editorial rules)
- Avoid unless proven on the page: breathtaking, stunning, one of a kind, rare opportunity, dream home, unique, luxurious, must see. Hebrew equivalents to avoid: נכס נדיר, הזדמנות חד פעמית, יוקרה ללא פשרות, מושלם, חלום, מהמם, חובה לראות. No all caps, no emojis in listing copy.
- Replace every adjective with a measurable fact: m², floor, ceiling height, exposures, meters or minutes to the promenade, kitchen or system maker, completion year.
- Hebrew typography: digits for numbers; gershayim in abbreviations (מ״ר, ממ״ד) with search normalizing both gershayim and straight quotes; keep Latin brand names in Latin script inside Hebrew, as Israel SIR's Hebrew page does with furniture brands and VRF [ISIR-HE].
- Write English and Hebrew as parallel originals, not translations. English explains Israeli terms once, in a glossary tooltip: mamad, va'ad bayit, arnona, Tofes 4. NBN's Yad2 guide already treats these as vocabulary that English speakers need [NBN-YAD2].
- Room counts: Israeli listings count rooms in half steps (a 3.5-room penthouse, a 4-room apartment of 204 m²) [AS-RENT, AS-IDX], while international brands count bedrooms and bathrooms [ISIR-EN1]. English pages should show both, for example "5 rooms (4 bedrooms, 3 bathrooms)".

---

## 5. Trust and conversion elements

| Element | Best observed implementation | Evidence | Recommendation for nad-lan.co.il |
|---|---|---|---|
| Agent card | Photo, name, title, phone, protected email, state license number; two agents per listing | CIRE-SOCAL | Photo, name, role, license number, agency legal name, languages spoken, direct phone, WhatsApp, email, office address |
| Agent ID and personal button | Agent ID and a personal call to action | ISIR-EN1 | Personal button text using the agent's first name, in both languages |
| Legal entity and imprint | Shop name, advisor, legal provider entity, imprint link | EV-1 | Show the brokerage's legal name and license in the card footer |
| License number | Per-agent license numbers; company license list in footer; licence number field in Yad2's data model; licensed broker title | CIRE-SOCAL, COMPASS-1, APIFY-YAD2, LREI | Always visible next to the name in both languages (Domestic TLV omits it, a trust gap) [DOMESTIC] |
| Private viewing | Showing request with in-person or video-chat option and time slots | CIRE-SOCAL, AGENCY | "Book a private viewing": in person or video, date slots, preferred language, buyer profile |
| Request details | Repeated buttons through the page | EV-1, CIRE-SOCAL | Repeat after story, after costs and at the end; sticky on mobile |
| WhatsApp | Portal integration; WhatsApp button promising immediate reply; WhatsApp share | ISIR-USSL, DOMESTIC, LREI, AS-SALE | Deep link with prefilled message including listing ID, title and page language |
| Call | Call button with number | AS-SALE | Tap to call, number isolated as left-to-right text |
| Brochure, flyer, print | Brochure PDF; flyers section; print | KF-OTM, KF-BRO, AGENCY, LREI | Auto-generated PDF per language with plan, key facts, costs and disclaimers |
| Financing tools | Mortgage calculator with taxes and HOA; payment breakdown; mortgage in principle | CIRE-SOCAL, COMPASS-1, SAV-RM | Collapsed "Financing" panel with buyer-type LTV note; no lender advertising |
| Save | Add to favorites | EV-1, EV-2 | Save without login; optional price-change alert |
| Share | Social share bar; WhatsApp, Facebook, email; tell a friend | SIR-CA, CIRE-SOCAL, AS-SALE, LREI | WhatsApp, email, copy link; per-language share image with title and price |
| Similar properties | 12, 6 or 4 cards; same-branch listings; nearby projects; login-gated at The Agency | SIR-CA, ISIR-EN1, EV-1, AS-SALE, MADLAN-PRJ, AGENCY | 3 to 6 cards, same area and price band, never gated |
| Sold proof | Sold labels and closed prices kept live | ISIR-EN2, LREI, KF-IDX, COMPASS-1 | "Recently sold or let" strip for the broker's own deals |
| Press and media | Articles about the listing linked on the page | CIRE-SOCAL | Use for the villa estate if coverage exists |
| Market records | Price history, public records; transactions and yield | COMPASS-1, MADLAN-PRJ | Market context block with sources (section 8, S13) |
| Disclaimers | Important Notice with dates of particulars and photos; measurement and virtual-staging warnings; third-party information notice; prior sale and withdrawal | KF-BRO, COMPASS-1, ISIR-EN1, CIRE-SOCAL | See S17 |
| Consent | Separate consent for data processing and for each newsletter | EV-1 | Separate unticked boxes for privacy and marketing |
| Freshness | Published and updated dates | APIFY-YAD2 | "Details verified on [date]" per block, not days on market |
| Exclusivity | Exclusive flag | APIFY-YAD2 | "בבלעדיות / Exclusive" badge in hero and agent card |
| Languages of service | Agent's spoken languages listed | AS-RENT | Show languages as text, not flags |

---

## 6. What HNW buyers and renters actually check

### 6.1 Buyers: documented priorities
| Priority | Evidence | Source | What the listing page must answer |
|---|---|---|---|
| Security | 81% of Sotheby's affiliated agents cite security as a top concern; gated access, CCTV, backup power and panic rooms increasingly common | https://www.prnewswire.com/news-releases/sothebys-international-realty-releases-2026-luxury-outlook-report-shows-luxury-residences-leading-the-years-real-estate-market-302655246.html | Guard hours, access control, CCTV, secured parking, mamad count, generator (villa) |
| Lifestyle and wellness | 60% of Sotheby's affiliated agents say lifestyle factors and wellness amenities matter more than ever. Mid-year: 62% say lifestyle is increasingly important, ahead of taxes (60%), economic stability (53%), political stability (49%) | SIR-LO26 URL above; https://www.rsir.com/blog/introducing-sothebys-international-realtys-2026-mid-year-luxury-outlook-report/ | Spa, gym, pool, promenade and beach access, walking times |
| Longevity, aging in place | Nearly 38% of $10M+ specialists say aging in place drives purchase decisions | https://www.rsir.com/blog/introducing-sothebys-international-realtys-2026-mid-year-luxury-outlook-report/ | Elevator to the door, private elevator, step-free access, bedroom on entry level |
| Turnkey condition | Wealthy buyers want turnkey homes; well-priced turnkey homes draw intense competition and sell quickly (Wealth Report 2026, pp. 29-30). Limited supply of move-in-ready luxury homes is a named demand theme | https://www.knightfrank.ie/wp-content/uploads/2026/04/The-Wealth-Report-2026_Final-Web-Spreads-2042026.pdf ; https://www.knightfrank.com/research/article/2026/4/piri-100-ultimate-prime-residential-property-index | Condition, never-lived-in status, furnished option, entry date |
| Service, privacy, amenities | Buyers pay premiums for curated communities, assured top-tier service, privacy, convenience and amenities (p. 29); privacy framed as the greatest luxury for wealthy families (p. 17) | KF Wealth Report URL above | Concierge and management company, privacy features, address withheld until viewing |
| Branded and hospitality living | Branded residences command premiums. In Israel, the largest Tel Aviv deal in ynet's 2025 top-10 list was a NIS 51M apartment in a Rothschild tower complex that includes a Six Senses hotel and spa; affluent buyers value hospitality elements and international-quality services | KF PIRI URL above; https://www.ynetnews.com/real-estate/article/rykjqf11hbl | Building services block equal in weight to the apartment specs |
| Flexibility, renting instead of buying | The super-prime rental market surged; top-end rents rose 63% in New York, 53% in London and 48% in Singapore over five years; mobile UHNWIs avoid transaction taxes on homes used a few days a month (p. 30) | KF Wealth Report URL above | A RENT page as polished as the SALE page |
| Asset logic, selectivity | Christie's 2026 report frames luxury property as an asset tied to lifestyle, identity and long-term wealth; its Prime Sentiment Index fell from 15.6 to 14.4, with the buyer-demand component down from 37.7 to 29.3; $10M+ cross-border capital shifting toward Dubai and Singapore | https://www.inman.com/2026/03/25/christies-international-real-estate-housing-global-luxury-report/ ; https://www.austintop50.com/christies-2026-annual-luxury-report-global-perspectives-data/ | Honest cost of ownership and source-linked market context |
| Cross-border demand | US foreign buyer activity up 44%. In Israel, nearly 60% of 2025 luxury transactions were by foreign residents. Israel's UHNWI population is forecast to grow from 5,462 (2026) to 6,889 (2031), +26%, 16th fastest globally (p. 11) | SIR-LO26 URL above; YNET URL above; KF Wealth Report URL above | English original, USD/EUR display, foreign-resident tax and LTV notes, video viewings |
| Israeli location shifts | Tel Aviv's super-luxury deals concentrated in the south Rothschild area; Jerusalem and Herzliya Pituach returning to center stage; buyers value iconic views, penthouses and irreplaceable locations | https://www.ynetnews.com/real-estate/article/rykjqf11hbl | View and micro-location storytelling, Herzliya Pituach context for the villa |
| Schools and family | Prime London family renters prioritize houses near leading schools; Compass lists schools with ratings and distances; Madlan shows school rankings | https://theintermediary.co.uk/2026/02/prime-london-lettings-activity-falls-in-2025-as-super-prime-market-expands-survey-finds/ ; COMPASS-2 URL in section 9; https://www.nbn.org.il/madlan/ | Schools and kindergartens with walking or driving times |
| Price verification | Madlan shows asking price next to an estimated value, transactions and price per m²; a Herzliya project page shows an area average of about NIS 40,000 per m² and a 3.28% rental yield | https://www.nbn.org.il/madlan/ ; https://www.madlan.co.il/projects/%D7%94%D7%AA%D7%96%D7%9E%D7%95%D7%A8%D7%AA_%D7%92%D7%9C%D7%99%D7%9C_%D7%99%D7%9D | Buyers will check anyway; show sources on the page |
| Younger wealthy buyers | 66% of Sotheby's surveyed professionals report more Millennial luxury buyers | RSIR URL above | Implication (inference): mobile-first layout, video, WhatsApp |

### 6.2 Luxury renters: documented priorities
| Priority | Evidence | Source |
|---|---|---|
| Concierge developments and schools | UHNW tenants in prime London prefer apartments in luxury developments with concierge; families prefer houses near leading schools | https://theintermediary.co.uk/2026/02/prime-london-lettings-activity-falls-in-2025-as-super-prime-market-expands-survey-finds/ |
| Flexibility has a price | 2025 prime central London short-let houses averaged £4,974 a week (+81.5%) and short-let apartments £2,142 (+21%), while long-let houses fell 8% | Same as above |
| Relocating families and waiting buyers | March 2026 tenant registrations up 16.6% year on year, +16.9% above £1,000 a week; tenants include families with Middle East ties who already have a London network, and buyers renting while they wait | https://www.knightfrank.co.uk/research/article/2026/4/prime-london-lettings-buck-the-trend-as-demand-builds |
| Freedom to leave | Mobile UHNWIs rent to keep the option to leave and to avoid transaction taxes (p. 30) | https://www.knightfrank.ie/wp-content/uploads/2026/04/The-Wealth-Report-2026_Final-Web-Spreads-2042026.pdf |
| Connectivity and quiet (mass-market proxy) | 86% of US renters call high-speed internet very important or essential; Multifamily Dive's summary of the same survey lists soundproofing and noise-reducing windows among top unit features | https://www.nmhc.org/news/press-release/2023/national-multifamily-housing-council-nmhc-and-grace-hill-2024-renter-preferences-survey-report-reveals-renters-evolving-priorities/ ; https://www.multifamilydive.com/news/nmhc-survey-reveals-renters-top-preferences/700666/ |
| Israeli legal reality at the top end | Fair Rental Law provisions apply to leases of 3+ months with rent up to NIS 20,000 a month. A NIS 37,000 Sarona listing and the broker's NIS 27,000 mini-penthouse listing sit above that line | https://www.kolzchut.org.il/he/%D7%94%D7%A9%D7%9B%D7%A8%D7%AA_%D7%93%D7%99%D7%A8%D7%94_%D7%A8%D7%90%D7%95%D7%99%D7%94_%D7%9C%D7%9E%D7%92%D7%95%D7%A8%D7%99%D7%9D ; AS-RENT URL in section 9; batch1_notes.md |
| Gap in Israeli rental pages | An observed luxury rental page lists entry date, parking, mamad and storage but no arnona, va'ad bayit, guarantees or lease length | https://www.anglo-saxon.co.il/en/properties/single/?id=425358 |

### 6.3 Practical checks supported by platform practice (not surveys)
- Parking and storage are core data fields on Yad2 and Madlan and amenity tags at Israel SIR [APIFY-YAD2, APIFY-MADLAN, ISIR-EN1].
- Mamad appears as a field or amenity, including counts, at Israel SIR, Domestic TLV, Anglo Saxon and Yad2 [ISIR-EN2, DOMESTIC, AS-RENT, APIFY-YAD2].
- Views and exposures are primary differentiators in Compass's view list and Israel SIR descriptions [COMPASS-1, ISIR-EN1].
- Beach proximity is expressed as first line to the sea, sea access and beach access [LREI, ISIR-EN2].
- Developer and build quality are surfaced through developer, architect and permit status on Madlan project pages [MADLAN-PRJ].
- Time to move in appears as entry date or completion date [APIFY-YAD2B, AS-RENT, EV-1].
- Not evidenced in this research (keep as optional fields, make no claims): air quality, view-protection risk, noise mapping.

### 6.4 Israel-specific checks
| Check | What to verify | Show on the page as | Source |
|---|---|---|---|
| Where rights are registered | Tabu for private ownership, Israel Land Authority for state-land leases, or a housing company when registration is not yet settled. Verify owner identity, mortgages, liens, warning notes, condominium bylaws; unsettled registration complicates resale and refinancing | Registration: Tabu / ILA / housing company. Condominium registered: yes / in process | https://yasmint-law.com/pre-agreement/%D7%90%D7%99%D7%9A-%D7%90%D7%93%D7%A2-%D7%94%D7%99%D7%9B%D7%9F-%D7%96%D7%9B%D7%95%D7%99%D7%95%D7%AA-%D7%94%D7%9E%D7%95%D7%9B%D7%A8-%D7%A8%D7%A9%D7%95%D7%9E%D7%95%D7%AA/ |
| Land registry extract | Shows registered owners, mortgages, liens, court orders, restrictions and condominium information; ordered online by block and parcel | "Tabu extract dated [date] available on request" | https://www.gov.il/he/service/land_registration_extract |
| Tofes 4 (occupancy approval) | Issued by the local planning committee; permanent utility connection depends on it; possession and the final mortgage payment typically follow; a later completion certificate confirms works per permit | "Tofes 4: issued [date] / expected [date]" on new buildings | https://www.nadlancenter.co.il/article/2123 |
| Sale Law security (buying from a developer) | Once payments exceed 7% of the price, the developer must provide one of: bank guarantee, insurance policy, first mortgage, warning note, or transfer of ownership | "Buyer security: [type]" in the new-build add-on | https://he.wikisource.org/wiki/%D7%97%D7%95%D7%A7_%D7%94%D7%9E%D7%9B%D7%A8_(%D7%93%D7%99%D7%A8%D7%95%D7%AA)_(%D7%94%D7%91%D7%98%D7%97%D7%AA_%D7%94%D7%A9%D7%A7%D7%A2%D7%95%D7%AA_%D7%A9%D7%9C_%D7%A8%D7%95%D7%9B%D7%A9%D7%99_%D7%93%D7%99%D7%A8%D7%95%D7%AA) |
| Mamad | Reinforced room with thick concrete walls and airtight steel door and window; technical specs set in 1992; required in new residential buildings since the early 1990s; known issues with cellular reception and temperature | "Mamad: yes, [count]; current use; air conditioned; mobile and Wi-Fi coverage" | https://en.wikipedia.org/wiki/Mamad |
| Shabbat elevator | Installing Shabbat control in an existing building needs a majority of owners; with two or more elevators where one already has it, one owner's request suffices; requesters pay installation proportionally | "Shabbat elevator: yes / no" | https://www.kolzchut.org.il/he/%D7%94%D7%AA%D7%A7%D7%A0%D7%AA_%D7%9E%D7%A2%D7%9C%D7%99%D7%AA_%D7%A9%D7%91%D7%AA_%D7%91%D7%91%D7%99%D7%AA_%D7%9E%D7%A9%D7%95%D7%AA%D7%A3 |
| Purchase tax, Israeli resident | Single apartment: 0% to NIS 1,978,745; 3.5% to 2,347,040; 5% to 6,055,070; 8% to 20,183,565; 10% above. Additional apartment: 8% to NIS 6,055,070, 10% above. Bizportal reports brackets frozen without indexation until 15 Jan 2028; Kol Zchut lists the additional-apartment schedule as effective to 31 Dec 2026 and Ilan Nadlan calls it a temporary order to end-2026, so re-verify in January 2027 | Buyer-profile purchase tax estimator with bracket date | https://www.kolzchut.org.il/he/%D7%97%D7%99%D7%A9%D7%95%D7%91_%D7%9E%D7%A1_%D7%A8%D7%9B%D7%99%D7%A9%D7%94 ; https://www.bizportal.co.il/realestates/news/article/20038028 ; https://ilan-nadlan.com/en/buying-as-a-foreigner |
| Purchase tax, foreign resident | Not eligible for single-apartment brackets; 8% to NIS 6,055,070 and 10% above | Same estimator, "foreign resident" profile | https://y-tax.co.il/purchase-tax-for-foreign-residents/ ; https://ilan-nadlan.com/en/buying-as-a-foreigner |
| Purchase tax, olim and veteran returning residents | Olim: 0.5% up to NIS 6,055,070 and 8% from there to NIS 20,183,565 on a single residence; purchase from one year before to seven years after aliyah; Bizportal says this schedule covers those making aliyah between 15 Aug 2024 and 15 Jan 2028. Veteran returning residents (10+ consecutive years abroad) may qualify for the reduced treatment | Same estimator, "oleh / returning resident" profile | https://www.nbn.org.il/life-in-israel/finances/taxes/planning-your-aliyah-purchase-tax/ ; BIZ-PT URL above ; https://y-tax.co.il/purchase-tax-for-foreign-residents/ |
| Mortgage limits, foreign residents | Investment category: up to 50% loan-to-value; repayment up to 50% of income; variable-rate share capped at two thirds; term up to 30 years; actual bank terms vary | Financing note under the price for the foreign-resident profile | https://ilan-nadlan.com/en/buying-as-a-foreigner |
| VAT on professional fees | 18% VAT on top of lawyer, broker and appraiser fees, separate from purchase tax | "Transaction costs: fees plus 18% VAT" | https://ilan-nadlan.com/en/buying-as-a-foreigner |
| Arnona | Annual municipal tax paid by the occupant regardless of ownership; the Interior Ministry sets minimum and maximum rates and each local authority sets its rates within them; discounts for defined groups | "Arnona: NIS [x] per two months (last bill, [date])" | https://www.kolzchut.org.il/he/ארנונה |
| Va'ad bayit and management | The house committee represents owners, collects fees, contracts services and maintains common property; it may hire a management company but must oversee it | "Management / va'ad bayit: NIS [x] per month; includes [list]" | https://www.kolzchut.org.il/he/ועד_הבית |
| Fair Rental Law scope | Residential leases of 3+ months with monthly rent up to NIS 20,000; excludes hotels, dormitories and protected housing | RENT badge: "Fair Rental Law provisions apply" or "Terms set by contract (rent above statutory threshold)" | https://www.kolzchut.org.il/he/%D7%94%D7%A9%D7%9B%D7%A8%D7%AA_%D7%93%D7%99%D7%A8%D7%94_%D7%A8%D7%90%D7%95%D7%99%D7%94_%D7%9C%D7%9E%D7%92%D7%95%D7%A8%D7%99%D7%9D |
| Habitability standard | Drainage and sewage, electricity and lighting, ventilation and natural light, doors and windows, drinking water, a partitioned toilet, no unreasonable safety or health risk | RENT "Handover condition" checklist | Same as above |
| Rental guarantees | Cap is the lower of three months' rent or one third of the whole term's rent; several types may be combined within the cap (bank guarantee, promissory note, security check, guarantors); return within 60 days of the apartment's return | RENT "Guarantees required" line items | https://www.kolzchut.org.il/he/%D7%94%D7%92%D7%91%D7%9C%D7%AA_%D7%A1%D7%9B%D7%95%D7%9D_%D7%94%D7%A2%D7%A8%D7%95%D7%91%D7%94_%D7%A9%D7%9E%D7%95%D7%AA%D7%A8_%D7%9C%D7%93%D7%A8%D7%95%D7%A9_%D7%9E%D7%A9%D7%95%D7%9B%D7%A8_%D7%93%D7%99%D7%A8%D7%94 |
| Repairs, notice, who pays (per Nadlan Center's guide to the law) | Urgent defects within 3 days; landlord notice 90 days, tenant 60 days; tenant pays no broker fee when the broker represented the landlord; landlord pays building insurance and fixed systems; tenant pays arnona, va'ad bayit and utilities | RENT "Who pays what" table | https://www.nadlancenter.co.il/article/766 |
| Transaction data | Madlan project pages publish transaction tables (address, date, price, area, NIS per m², floor, year built). The government real estate website is the official counterpart to link (confirm its module scope at build time) | Market context block with outbound source links | https://www.madlan.co.il/projects/%D7%94%D7%AA%D7%96%D7%9E%D7%95%D7%A8%D7%AA_%D7%92%D7%9C%D7%99%D7%9C_%D7%99%D7%9D ; https://www.nadlan.gov.il/ |

---

## 7. Bilingual and RTL presentation lessons

### 7.1 What Israeli and international sites actually do
| Site | Language architecture | Direction markup | Hebrew font | Currency and units |
|---|---|---|---|---|
| Israel SIR [ISIR-EN1, ISIR-HE, ISIR-HE-SRC] | Separate domains (.com English, .co.il Hebrew) with reciprocal hreflang en-us and he-il | html element has no lang or dir; RTL set through a body class and CSS | Open Sans Hebrew | Hebrew page shows ₪ before the number plus USD; m² written as מ"ר; Latin brand names kept inline |
| Anglo Saxon [AS-SALE, AS-HE, AS-HE-SRC, AS-LEGACY] | Hebrew at the root (hreflang x-default), English and French in subfolders | lang="he" on html, direction set lower in the page | Open Sans plus a custom file | Hebrew page shows ₪ after the number; English uses Rooms and Sqm; currency switch NIS, USD, EUR, GBP |
| Madlan [MADLAN-LST, MADLAN-LST-SRC, NBN-MADLAN] | Hebrew only | RTL through CSS | NovemberHebrew | ₪ before the number in titles; NBN publishes an English tutorial with a vocabulary table for it |
| sothebys.ussl.co.il [ISIR-USSL] | English, Hebrew, Russian | Not inspected | Not inspected | ₪ |
| Luxury Real Estate Israel [LREI] | Hebrew primary, French, Russian, English | Not inspected | Not inspected | EUR, GBP, ILS switch |
| Sotheby's Canada syndication [SIR-CA] | English | LTR | n/a | Converted to CAD with the original ILS price kept; sizes converted to sq ft with two decimals (9,687.52 sq ft is exactly 900 m²; the 10,763.91 sq ft lot is exactly 1,000 m², one dunam) |
| LuxuryEstate [LUXEST] | English | LTR | n/a | Tel Aviv prices converted to EUR; sizes kept in m² |

Arabic RTL sites were not studied; the rules below rely on W3C, Apple and MDN guidance, which cover both scripts.

### 7.2 Rules for nad-lan.co.il
**Direction and markup**
- Put `lang="he" dir="rtl"` on the html element of Hebrew pages and `lang="en" dir="ltr"` on English pages; do not rely on CSS for base direction [W3C-DIR]. Both Israel SIR and Anglo Saxon fall short of this [ISIR-HE-SRC, AS-HE-SRC].
- Use CSS logical properties (margin-inline-start, padding-inline, inset-inline, text-align: start) so one stylesheet serves both directions [MDN-LOGICAL]. In WordPress, either write logical CSS or register an RTL stylesheet with wp_style_add_data and generate it with RTLCSS [WP-RTL].
- Isolate left-to-right runs inside Hebrew text with `<bdi>` or `dir="ltr"` spans: prices, areas, phone numbers, emails, URLs, listing IDs, Latin brand names (B.S.R, VRF). Set `dir="auto"` on form inputs [W3C-DIR]. WordPress's own guidance keeps emails, phone numbers and URLs left-to-right in RTL layouts [WP-RTL].
- Mirror layout and directional icons (arrows, chevrons, carousel order, progress), but do not mirror numerals, phone numbers, media playback controls, logos or photographs [APPLE-RTL].

**Numbers and currency**
- The CLDR Hebrew locale (ICU 78.2, CLDR 48, tested locally) places ₪ after the number with right-to-left marks and a no-break space; English locales place ₪ before [INTL-TEST]. The Israeli market is split: Israel SIR and Madlan put ₪ first, Anglo Saxon puts it last [ISIR-HE-SRC, MADLAN-LST, AS-HE-SRC]. Pick one per language and hard-code it in a single formatter. Recommendation: Hebrew "16,750,000 ₪", English "₪16,750,000".
- Do not use compact number formatting in Hebrew: it outputs a Latin "M" (17M). Write "16.75 מיליון ₪" [INTL-TEST].
- The Intl API has no square-meter unit (the meter unit renders as מ׳), so render מ״ר explicitly [INTL-TEST].
- Western digits with comma thousands separators in both languages, as every Israeli site observed does [ISIR-HE-SRC, AS-HE-SRC].
- Show USD and EUR as secondary, clearly approximate values with a conversion date, never replacing the NIS price. Israel SIR shows both currencies; Sotheby's Canada keeps the original ILS price as its own field [ISIR-EN1, SIR-CA].

**Units and counts**
- m² primary in both languages. English adds sq ft rounded to the nearest 10 (248 m² becomes about 2,670 sq ft), avoiding the two-decimal false precision of syndicated conversions [SIR-CA]. Savills shows both units side by side [SAV-RM].
- Plots in dunam with m² (1 dunam = 1,000 m²).
- Rooms in Hebrew; rooms plus bedrooms and bathrooms in English [AS-RENT, ISIR-EN1].
- Floor as "קומה 12 מתוך 15" / "Floor 12 of 15" [AS-RENT].

**Dates and language switching**
- Hebrew dates with month names (16 בספטמבר 2026); English day-month-year with month names to avoid US/EU ambiguity [INTL-TEST].
- One URL per language with reciprocal hreflang plus x-default; no automatic redirect by browser language [G-HREFLANG]. Israel SIR's cross-domain pairs and Anglo Saxon's x-default setup are workable models [ISIR-HE-SRC, AS-HE-SRC].
- Language switch keeps the user on the same listing and scroll position.

**Structured data**
- RealEstateListing (schema.org "new" area; datePosted, leaseLength) wrapping an Apartment or house entity with numberOfRooms, numberOfBedrooms, numberOfBathroomsTotal, floorSize (unit code MTK for m²), floorLevel, amenityFeature, petsAllowed, yearBuilt, accommodationFloorPlan and tourBookingPage [SCHEMA-REL, SCHEMA-APT].

**Type**
- Choose families that cover both scripts so rhythm stays consistent (section 3.1) [GFONTS].
- Keep Hebrew and English type scales as separate tokens (size, line height, letter spacing) and tune them by eye; do not letter-space Hebrew.

---

## 8. Recommended listing template for nad-lan.co.il

### 8.1 Build rules
- Every block renders from structured fields stored once per listing, with Hebrew and English text fields side by side, so both pages stay in sync.
- Each factual field carries two hidden attributes: source (owner, broker, lawyer, developer spec, municipal bill) and verified date. Blocks S11, S12, R11 and R12 print "verified on [date]".
- Blocks hide when empty, with one exception: the legal and documents block shows "not yet verified" instead of disappearing.
- Hebrew is the x-default page; English is a parallel original, not a machine translation.
- Numbers, IDs, phones, emails and Latin brand names are always isolated as left-to-right runs (section 7.2).

### 8.2 SALE variant (apartment, penthouse, mini penthouse)

**S1. Utility bar**
- Breadcrumb: city, neighborhood, project or building
- Language switch (עברית / English) to the same listing
- Save; Share (WhatsApp, email, copy link)
- Listing ID

**S2. Hero**
- Lead media: image (16:9 desktop, 4:5 mobile) or a 10 to 20 second muted loop with a poster frame
- Badges (two at most): למכירה / For sale; בבלעדיות / Exclusive; חדש מקבלן / New from developer; נמכר / Sold
- Title (rule in 4.2)
- Micro-location: neighborhood, project, city (street hidden by default)
- Price line: NIS price, or "מחיר לפי בקשה / Price on request" when the owner insists; approximate USD and EUR with conversion date (on by default in English)
- Media tabs: Photos (count), Video, Floor plan, 3D tour, Map

**S3. Key facts bar (eight at most, in this order)**
1. Rooms (Hebrew) / rooms and bedrooms (English)
2. Bathrooms
3. Built area m² (English adds sq ft)
4. Outdoor area m² with type (terrace, sun balcony, roof terrace, garden)
5. Floor X of Y
6. Parking (count and type)
7. Mamad and storage
8. Entry: immediate or date

**S4. Call-to-action module (sticky)**
- Book a private viewing (in person or video call)
- WhatsApp (prefilled with listing ID, title and page language)
- Call
- Download brochure (Hebrew PDF, English PDF)
- Mini agent card: photo, name, license number

**S5. The story**
- Dek: one sentence, up to 25 words
- Narrative: three paragraphs, 150 to 250 words per language
- Signature features: six bullets, each with a number or proper noun

**S6. Gallery**
- Ordered images with captions (space, floor, orientation)
- Per-image labels: הדמיה / Virtually staged; עיבוד דיגיטלי / Digitally enhanced
- Videos: walkthrough, neighborhood
- Photo date (month and year)

**S7. Plans and areas**
- Floor plan per level (image and PDF) with north arrow
- Area table: built m² with measurement basis (permit, measured, developer specification); each balcony or terrace m²; roof terrace m²; garden m²; storage m²; parking spaces and type
- Ceiling height in meters and any double-height zones
- Levels (single, duplex, triplex)

**S8. Residence details (grouped table)**
- Layout: rooms, bedrooms, suites, bathrooms, guest WC, living and dining, kitchen (maker, island), laundry, study
- Light and view: exposures (N, E, S, W); views (sea, park, city; open or partial); corner or full floor
- Systems: air conditioning type (VRF, central), underfloor heating, smart home, lighting system, window system, electric shutters, water heating, soundproofing
- Finishes: flooring, carpentry, built-in appliances, bathroom fittings
- Safety: mamad (count, current use, air conditioning, mobile coverage), security door, alarm
- Condition: new and never lived in; renovated (year); well maintained; needs renovation; shell. Furniture included: yes, partial, no
- Accessibility: step-free from street, elevator to the floor, private elevator

**S9. Building, services and security**
- Project or building name, developer, architect, completion year, floors, units
- Lobby and concierge hours; guard (24/7 or hours); CCTV; access control
- Elevators: count, private elevator, Shabbat elevator
- Amenities: pool, spa, gym, residents' lounge, children's room, cinema, EV charging, bike storage
- Management company; monthly management or va'ad bayit fee (NIS) and what it includes
- Building pet policy

**S10. Location**
- Map: monochrome, approximate-area circle
- Walking-time chips: beach, promenade, park, cafes and shopping, schools and kindergartens, public transport
- Driving times to key destinations (for example Ben Gurion Airport)
- Neighborhood summary (about 80 words per language)
- Planned changes nearby (optional, each with source link and date)

**S11. Costs and ownership**
- Asking price (NIS); price per built m² (automatic; hidden for estates or when built area is unverified)
- Purchase tax estimator with profile selector: Israeli resident, single apartment; Israeli resident, additional apartment; foreign resident; oleh or eligible returning resident. Output: estimated NIS amount, bracket table date, "consult a lawyer" note [KZ-PT, BIZ-PT, YTAX, NBN-PT]
- Arnona: NIS per two months, date of the bill [KZ-ARNONA]
- Management or va'ad bayit: NIS per month, inclusions [KZ-VAAD]
- Other recurring charges: parking, club, pool
- Financing: LTV note by profile (foreign residents up to 50%) [ILAN]; optional collapsed calculator (price, down payment, rate, term)
- Transaction costs: lawyer, broker, appraiser, each plus 18% VAT [ILAN]

**S12. Legal and documents status**
- Rights registration: Tabu, Israel Land Authority, or housing company [YASMINT]
- Condominium registration: registered, in process, not registered
- Encumbrances: none; mortgage to be released at closing; other (disclosed) [GOV-TABU]
- Permits and occupancy: Tofes 4 date; completion certificate; deviations declared by the owner [NC-T4]
- Documents available after viewing registration: Tabu extract (date), permit plans, arnona bill, management statement, technical specification
- Verified by (broker or lawyer) and date

**S13. Market context (not a valuation)**
- Recent nearby transactions: count, period, NIS per m² range for similar type and size, outbound source links [MADLAN-PRJ, NADLAN-GOV]
- Last transactions in the same building, if any
- Note: indicative only; sources and date shown

**S14. Agent and private viewing**
- Agent card: photo, full name, role, broker license number, agency legal name, languages, phone, WhatsApp, email, office address, exclusive-mandate badge, typical response time
- Viewing form: full name; phone with country code; email; preferred language (Hebrew, English, French, Russian); viewing type (in person, video); preferred dates; buyer profile (resident, foreign resident, oleh, returning resident); timeline; financing (cash, mortgage); message; privacy consent; separate marketing opt-in

**S15. Similar and recently sold**
- Three to six cards: image, title, micro-location, price, rooms, built m², outdoor m², floor
- "Recently sold by [broker]" cards with a Sold label

**S16. FAQ (optional, built from fields)**
- Is there a mamad? What does the management fee include? Where are the rights registered? When can I move in? Can a foreign resident finance this purchase? Is there a Shabbat elevator?

**S17. Footer notes**
- Disclaimers: particulars are not an offer or contract; areas are approximate, with measurement basis; images may be virtually staged or enhanced and are labelled; information supplied by the owner or third parties, verified as of [date]; tax and cost figures are indicative and not legal or tax advice; subject to prior sale, price change or withdrawal
- Listing ID; last updated; language switch

### 8.3 RENT variant

**R1. Utility bar:** same fields as S1.

**R2. Hero**
- Lead media as S2
- Badges (two at most): להשכרה / For rent; מרוהטת / Furnished; כניסה מיידית / Immediate entry; בבלעדיות / Exclusive; הושכרה / Let
- Title and micro-location as S2
- Price line: monthly rent (NIS) with approximate USD and EUR
- Payment-terms line: payment method and months paid upfront
- Media tabs as S2

**R3. Key facts bar (eight at most)**
1. Rooms / rooms and bedrooms
2. Bathrooms
3. Built area m²
4. Outdoor area m² with type
5. Floor X of Y
6. Furnishing: full, partial, none
7. Available from
8. Minimum lease (months)

Chips under the bar: parking count, mamad, storage, pets allowed.

**R4. Call-to-action module:** book a viewing (in person or video), WhatsApp, call, "request lease terms" PDF, mini agent card.

**R5. The story:** same structure as S5; the third paragraph leans on building services and daily life.

**R6. Gallery:** as S6, plus dated inventory photos.

**R7. Plans and areas:** same fields as S7.

**R8. Residence details:** S8 groups plus furnishing inventory (list), appliances included, pets policy (yes, no, conditions), smoking policy, fiber internet availability, optional cleaning service.

**R9. Building, services and security:** S9 fields plus tenant building rules (moving hours, amenity access fees).

**R10. Location:** same fields as S10.

**R11. Lease terms and monthly costs**
- Monthly rent (NIS); indexation (CPI-linked or fixed); payment method; months upfront
- Lease term: minimum and maximum months; extension option (months) and rent on renewal; early-exit clause and notice
- Monthly costs: arnona per two months (tenant) [KZ-ARNONA]; management or va'ad bayit per month (tenant); utilities estimate (electricity, water, gas); internet; parking fee [NC-RENT]
- Guarantees: deposit (NIS); bank guarantee (NIS); promissory note (NIS); number of guarantors; return timing [KZ-GUAR]
- Broker fee: amount plus VAT, and who pays [NC-RENT]
- Legal framework badge: "Fair Rental Law provisions apply" when rent is up to NIS 20,000 a month and the lease is 3+ months, otherwise "Terms set by contract" [KZ-HAB]
- Who pays what: landlord (building insurance, structure, fixed systems) and tenant (ongoing costs) [NC-RENT]; recommend the tenant insures contents

**R12. Legal and documents status**
- Landlord verified as owner against a Tabu extract (date) [GOV-TABU]
- Building Tofes 4 (new buildings) [NC-T4]
- Handover checklist covering the habitability items, plus inventory report [KZ-HAB]
- Landlord insurance in place
- Documents on request: draft lease, inventory list
- Verified by and date

**R13. Market context:** comparable asking rents (range, source, date); optional gross yield for investors [MADLAN-PRJ].

**R14. Agent and viewing**
- Agent card as S14
- Form: full name; phone with country code; email; preferred language; viewing type; desired move-in date; lease length; household size; pets; corporate lease (company name optional); message; privacy consent; separate marketing opt-in. Relocating families and would-be buyers are documented luxury tenant segments [KF-PCL-LET]

**R15. Similar rentals and recently let:** as S15 with "Let" labels.

**R16. FAQ:** Is it furnished? Which guarantees are required? What do monthly costs include? Are pets allowed? Is there parking and storage? How flexible is the lease?

**R17. Footer notes:** S17 disclaimers plus "lease terms are indicative until a contract is signed".

### 8.4 Add-on for the villa estate (Herzliya Pituach)
- Replaces S3 with: plot (dunam and m²), built area (above ground and basement), bedrooms and suites, bathrooms, pool (heated or not), parking (covered and driveway), elevator, entry
- Adds to S7: built area per floor, basement, garden, pool deck, guest or staff unit
- Adds to S8 and S9: architect, year built or renovated, landscaping, generator or backup power, perimeter security and gate, CCTV, safe-room count, wine cellar, spa, home cinema, smart home [SIR-CA, SIR-LO26]
- Adds to S12: block and parcel on request [GOV-TABU]; documented remaining building rights, if any
- Privacy rule: address and street-facing exterior photos withheld until a qualified viewing is booked

### 8.5 Add-on for new builds (projects such as those in Kochav HaTzafon or Tzukei Aviv)
- Developer, contractor, architect
- Status timeline: planning, permit, construction, Tofes 4 [MADLAN-PRJ, NC-T4]
- Delivery date; technical specification PDF
- Buyer security type under the Sale Law [WS-SALELAW]
- Payment schedule and indexation terms; price list date

### 8.6 Field label dictionary
| Key | Hebrew | English | Display format |
|---|---|---|---|
| price | מחיר | Price | 16,750,000 ₪ / ₪16,750,000 |
| rent_monthly | שכר דירה לחודש | Monthly rent | 27,000 ₪ לחודש / ₪27,000 per month |
| rooms | חדרים | Rooms | 4.5 |
| bedrooms | חדרי שינה | Bedrooms | 3 |
| bathrooms | חדרי רחצה | Bathrooms | 3 |
| built_area | שטח בנוי | Interior area | 200 מ״ר / 200 m² (about 2,150 sq ft) |
| terrace_area | שטח מרפסות | Terraces | 76 מ״ר / 76 m² |
| sun_balcony | מרפסת שמש | Sun terrace | yes / m² |
| roof_terrace | מרפסת גג | Roof terrace | m² |
| garden_area | שטח גינה | Garden | m² |
| plot_area | שטח מגרש | Plot | 1.1 דונם (1,100 מ״ר) / 1.1 dunam (1,100 m²) |
| floor | קומה X מתוך Y | Floor X of Y | 12 / 15 |
| exposures | כיווני אוויר | Exposures | צפון, מערב / North, West |
| view | נוף | View | ים, פארק / Sea, park |
| ceiling_height | גובה תקרה | Ceiling height | 7 מ׳ / 7 m |
| parking | חניות | Parking | 2 (תת קרקעית) / 2 (underground) |
| storage | מחסן | Storage room | yes / m² |
| mamad | ממ״ד | Safe room (mamad) | yes / count |
| elevator | מעלית | Elevator | count |
| shabbat_elevator | מעלית שבת | Shabbat elevator | yes / no |
| private_elevator | מעלית פרטית | Private elevator | yes / no |
| ac | מיזוג אוויר | Air conditioning | VRF |
| underfloor_heating | חימום תת רצפתי | Underfloor heating | yes / no |
| condition | מצב הנכס | Condition | חדש / New |
| furnished | ריהוט | Furnishing | מלא, חלקי, ללא / Full, partial, none |
| entry | תאריך כניסה | Available from | מיידי / Immediate |
| lease_min | תקופת שכירות מינימלית | Minimum lease | 12 חודשים / 12 months |
| mgmt_fee | דמי ניהול / ועד בית | Management fee | ₪ per month |
| arnona | ארנונה | Municipal tax (arnona) | ₪ per two months |
| guarantees | ערבויות | Guarantees | list |
| broker_fee | דמי תיווך | Broker fee | amount plus VAT |
| registration | רישום זכויות | Title registration | טאבו / רמ״י / חברה משכנת |
| condo_registration | רישום בית משותף | Condominium registration | רשום / בתהליך |
| tofes4 | טופס 4 | Occupancy approval (Tofes 4) | date |
| developer | יזם | Developer | name |
| architect | אדריכל | Architect | name |
| year_built | שנת סיום בנייה | Year completed | 2025 |
| concierge | קונסיירז׳ / לובי מאויש | Concierge | hours |
| security | אבטחה | Security | list |
| pets | חיות מחמד | Pets | policy |
| license | רישיון תיווך מס׳ | Broker license no. | number |
| exclusive | בבלעדיות | Exclusive | badge |
| listing_id | מספר נכס | Listing ID | code |
| updated | עודכן | Last verified | date |

---

## 9. Sources

### 9.1 Listing pages and site evidence
| Tag | URL | Notes |
|---|---|---|
| SIR-CA | https://sothebysrealty.ca/en/property/global/region-israel/herzliya-pituach-real-estate/3160368/ | Sotheby's Canada syndication of an Israel SIR villa |
| SIR-COM1 | https://www.sothebysrealty.com/eng/sales/detail/180-l-86348-lp4k46/extraordinary-sea-views-penthouse-at-the-jaffa-residences-tel-aviv-il | Title from search results only (robots-blocked) |
| SIR-COM2 | https://www.sothebysrealty.com/eng/sales/detail/180-l-86348-ntbc5c/spectacular-penthouse-duplex-with-a-private-pool-and-panoramic-sea-views-tel-aviv-il | Title from search results only |
| SIR-COM3 | https://www.sothebysrealty.com/eng/sales/detail/180-l-86348-nts4vp/unique-investment-opportunity-in-herzliya-pituach-herzliya-il | Title from search results only |
| ISIR-EN1 | https://www.israelsir.com/property/sea-view-duplex-penthouse-in-north-tel-aviv/ | Israel SIR, English |
| ISIR-EN2 | https://www.israelsir.com/property/full-floor-duplex-penthouse-in-tel-avivs-old-north-en/ | Israel SIR, English, sold |
| ISIR-HE | https://www.israelsir.co.il/property/sea-view-duplex-penthouse-north-tel-aviv/ | Israel SIR, Hebrew |
| ISIR-TAG | https://www.israelsir.com/property_tags/luxury-penthouse-in-tel-aviv-for-sale/ | Israel SIR penthouse index (dual pricing) |
| ISIR-USSL | https://sothebys.ussl.co.il/property-search/ | Israel SIR portal search |
| CIRE-SOCAL | https://christiesresocal.com/properties/11005-bellagio-pl-los-angeles-ca-us-90077-26856275 | Christie's International Real Estate Southern California |
| EV-HOME | https://www.engelvoelkers.com/de/en | E&V global site (no Israel shop found) |
| EV-1 | https://www.engelvoelkers.com/es/en/exposes/ce175b24-85bc-5764-aaab-4c75c5a4e234 | E&V expose, Salou |
| EV-2 | https://www.engelvoelkers.com/it/en/exposes/af591b0e-26f4-5e37-bef7-cd4a580b628a | E&V expose, Alassio |
| KF-IDX | https://www.knightfrank.co.uk/property-for-sale/penthouses | Knight Frank sales index |
| KF-LET | https://www.knightfrank.co.uk/property-to-rent/london | Knight Frank lettings index |
| KF-BRO | https://content.knightfrank.com/property/bgv012449768/brochures/en/bgv012449768-en-brochure-b8c1c3cc-4cd2-420b-883b-99f79d10e0f0-1.pdf | Knight Frank brochure |
| KF-OTM | https://www.onthemarket.com/details/17325672/ | Knight Frank listing on OnTheMarket |
| SAV-PORT | https://portfolio.savills.com/property/penthouse-2/ | Savills Portfolio |
| SAV-RM | https://www.rightmove.co.uk/properties/89011206 | Savills listing on Rightmove |
| COMPASS-1 | https://www.compass.com/listing/450-alton-road-unit-ph1-miami-beach-fl-33139/1438587235119419665/ | Compass penthouse |
| COMPASS-2 | https://www.compass.com/homedetails/5001-Collins-Ave-Unit-PH4-Miami-Beach-FL-33140/505042719362813457_lid/ | Compass record page |
| AGENCY | https://www.theagencyre.com/single-family/clr/24-413783/2571-wallingford-dr-beverly-hills-ca-90210 | The Agency |
| AS-SALE | https://www.anglo-saxon.co.il/en/properties/single/?id=393716 | Anglo Saxon sale, English |
| AS-RENT | https://www.anglo-saxon.co.il/en/properties/single/?id=425358 | Anglo Saxon rental, English (NIS 37,000 per month) |
| AS-HE | https://www.anglo-saxon.co.il/properties/single/?id=425358 | Anglo Saxon rental, Hebrew |
| AS-IDX | https://www.anglo-saxon.co.il/en/locales/%D7%AA%D7%9C%20%D7%90%D7%91%D7%99%D7%91%20%D7%99%D7%A4%D7%95/%D7%93%D7%99%D7%A8%D7%95%D7%AA_%D7%9C%D7%9E%D7%9B%D7%99%D7%A8%D7%94/ | Anglo Saxon Tel Aviv sale index |
| AS-LEGACY | https://real-estate-herzliya-pituach.com/legacy-2/ | Anglo Saxon Herzliya Pituach page with currency switcher |
| MADLAN-PRJ | https://www.madlan.co.il/projects/%D7%94%D7%AA%D7%96%D7%9E%D7%95%D7%A8%D7%AA_%D7%92%D7%9C%D7%99%D7%9C_%D7%99%D7%9D | Madlan project page (LOVE Glil Yam, Herzliya) |
| MADLAN-LST | https://www.madlan.co.il/listings/hu5iGl04ofA | Madlan listing (metadata and source only) |
| NBN-MADLAN | https://www.nbn.org.il/madlan/ | Nefesh B'Nefesh Madlan tutorial |
| NBN-YAD2 | https://www.nbn.org.il/yad2/ | Nefesh B'Nefesh Yad2 guide and word bank |
| YAD1 | https://www.yad2.co.il/yad1/newprojects/tel-aviv-area?area=1&city=5000 | Yad1 new projects, Tel Aviv |
| APIFY-YAD2 | https://apify.com/parsebird/yad2-real-estate-scraper | Documents Yad2 listing fields |
| APIFY-YAD2B | https://apify.com/haketa/yad2-scraper | Documents Yad2 fields incl. entry date, video URL |
| APIFY-MADLAN | https://apify.com/parsebird/madlan-real-estate-scraper | Documents Madlan listing fields |
| LREI | https://luxury-realestate-israel.com/1403_325_פנטהאוז-סופר-יוקרתי-למכירה-על-הים-בתל-אביב.htm | Luxury Real Estate Israel listing |
| DOMESTIC | https://www.domestictlv.co.il/estate/%D7%A4%D7%A0%D7%98%D7%94%D7%90%D7%95%D7%96-%D7%A0%D7%93%D7%99%D7%A8-%D7%A0%D7%95%D7%A3-%D7%9C%D7%99%D7%9D-%D7%9E%D7%A8%D7%9B%D7%96-%D7%AA%D7%9C-%D7%90%D7%91%D7%99%D7%91/ | Domestic TLV listing |
| LUXEST | https://www.luxuryestate.com/penthouses-israel/tel-aviv | LuxuryEstate Tel Aviv penthouses |

### 9.2 Code-level evidence (public HTML and CSS of the pages above, plus local tests)
| Tag | What was inspected |
|---|---|
| KF-CSS | https://www.knightfrank.co.uk/assets/css/style-base.css (font families, hex frequency) and font files referenced by KF-IDX |
| COMPASS-CSS | https://www.compass.com/ucfe-assets/fonts/3/fonts.min.css and https://www.compass.com/ucfe-assets/cx/4/cx.min.css |
| COMPASS-SRC | HTML of COMPASS-1 (Material Symbols subset, aspect-ratio rules) |
| CIRE-SOCAL-SRC | HTML of CIRE-SOCAL (font variables, Google Fonts links, hex frequency, aspect ratio) |
| EV-SRC | HTML and CSS chunks of EV-1 (font files, color variables, 3:2 aspect-ratio rules) |
| SAV-PORT-CSS | https://use.typekit.net/kth0hyt.css loaded by SAV-PORT |
| ISIR-EN1-SRC, ISIR-HE-SRC | HTML of ISIR-EN1 and ISIR-HE (fonts, body class, hreflang, price strings) |
| AS-HE-SRC | HTML of AS-HE (lang attribute, hreflang, price strings, fonts) |
| MADLAN-LST-SRC | HTML of MADLAN-LST (NovemberHebrew font, CSS direction) |
| GFONTS | https://fonts.googleapis.com/css2?family=Frank+Ruhl+Libre (and the other families listed in 3.1), checked for a Hebrew subset |
| INTL-TEST | Node.js 22 Intl API with ICU 78.2 / CLDR 48, run locally: he-IL and en currency, compact, unit and date formatting |

### 9.3 Market and buyer research
| Tag | URL |
|---|---|
| KF-WR26 | https://www.knightfrank.ie/wp-content/uploads/2026/04/The-Wealth-Report-2026_Final-Web-Spreads-2042026.pdf |
| KF-PIRI | https://www.knightfrank.com/research/article/2026/4/piri-100-ultimate-prime-residential-property-index |
| SIR-LO26 | https://www.prnewswire.com/news-releases/sothebys-international-realty-releases-2026-luxury-outlook-report-shows-luxury-residences-leading-the-years-real-estate-market-302655246.html |
| SIR-MY26 | https://www.rsir.com/blog/introducing-sothebys-international-realtys-2026-mid-year-luxury-outlook-report/ |
| CIRE-26a | https://www.inman.com/2026/03/25/christies-international-real-estate-housing-global-luxury-report/ |
| CIRE-26b | https://www.austintop50.com/christies-2026-annual-luxury-report-global-perspectives-data/ |
| YNET-25 | https://www.ynetnews.com/real-estate/article/rykjqf11hbl |
| KF-PCL-LET | https://www.knightfrank.co.uk/research/article/2026/4/prime-london-lettings-buck-the-trend-as-demand-builds |
| INTERMED | https://theintermediary.co.uk/2026/02/prime-london-lettings-activity-falls-in-2025-as-super-prime-market-expands-survey-finds/ |
| NMHC | https://www.nmhc.org/news/press-release/2023/national-multifamily-housing-council-nmhc-and-grace-hill-2024-renter-preferences-survey-report-reveals-renters-evolving-priorities/ |
| MFD | https://www.multifamilydive.com/news/nmhc-survey-reveals-renters-top-preferences/700666/ |

### 9.4 Israeli law, tax and registration
| Tag | URL |
|---|---|
| KZ-PT | https://www.kolzchut.org.il/he/%D7%97%D7%99%D7%A9%D7%95%D7%91_%D7%9E%D7%A1_%D7%A8%D7%9B%D7%99%D7%A9%D7%94 |
| BIZ-PT | https://www.bizportal.co.il/realestates/news/article/20038028 |
| NBN-PT | https://www.nbn.org.il/life-in-israel/finances/taxes/planning-your-aliyah-purchase-tax/ |
| YTAX | https://y-tax.co.il/purchase-tax-for-foreign-residents/ |
| ILAN | https://ilan-nadlan.com/en/buying-as-a-foreigner |
| KZ-HAB | https://www.kolzchut.org.il/he/%D7%94%D7%A9%D7%9B%D7%A8%D7%AA_%D7%93%D7%99%D7%A8%D7%94_%D7%A8%D7%90%D7%95%D7%99%D7%94_%D7%9C%D7%9E%D7%92%D7%95%D7%A8%D7%99%D7%9D |
| KZ-GUAR | https://www.kolzchut.org.il/he/%D7%94%D7%92%D7%91%D7%9C%D7%AA_%D7%A1%D7%9B%D7%95%D7%9D_%D7%94%D7%A2%D7%A8%D7%95%D7%91%D7%94_%D7%A9%D7%9E%D7%95%D7%AA%D7%A8_%D7%9C%D7%93%D7%A8%D7%95%D7%A9_%D7%9E%D7%A9%D7%95%D7%9B%D7%A8_%D7%93%D7%99%D7%A8%D7%94 |
| NC-RENT | https://www.nadlancenter.co.il/article/766 |
| KZ-SHABBAT | https://www.kolzchut.org.il/he/%D7%94%D7%AA%D7%A7%D7%A0%D7%AA_%D7%9E%D7%A2%D7%9C%D7%99%D7%AA_%D7%A9%D7%91%D7%AA_%D7%91%D7%91%D7%99%D7%AA_%D7%9E%D7%A9%D7%95%D7%AA%D7%A3 |
| NC-T4 | https://www.nadlancenter.co.il/article/2123 |
| WS-SALELAW | https://he.wikisource.org/wiki/%D7%97%D7%95%D7%A7_%D7%94%D7%9E%D7%9B%D7%A8_(%D7%93%D7%99%D7%A8%D7%95%D7%AA)_(%D7%94%D7%91%D7%98%D7%97%D7%AA_%D7%94%D7%A9%D7%A7%D7%A2%D7%95%D7%AA_%D7%A9%D7%9C_%D7%A8%D7%95%D7%9B%D7%A9%D7%99_%D7%93%D7%99%D7%A8%D7%95%D7%AA) |
| YASMINT | https://yasmint-law.com/pre-agreement/%D7%90%D7%99%D7%9A-%D7%90%D7%93%D7%A2-%D7%94%D7%99%D7%9B%D7%9F-%D7%96%D7%9B%D7%95%D7%99%D7%95%D7%AA-%D7%94%D7%9E%D7%95%D7%9B%D7%A8-%D7%A8%D7%A9%D7%95%D7%9E%D7%95%D7%AA/ |
| GOV-TABU | https://www.gov.il/he/service/land_registration_extract |
| WIKI-MAMAD | https://en.wikipedia.org/wiki/Mamad |
| KZ-ARNONA | https://www.kolzchut.org.il/he/ארנונה |
| KZ-VAAD | https://www.kolzchut.org.il/he/ועד_הבית |
| NADLAN-GOV | https://www.nadlan.gov.il/ |

### 9.5 RTL, bilingual and structured-data guidance
| Tag | URL |
|---|---|
| W3C-DIR | https://www.w3.org/International/questions/qa-html-dir |
| APPLE-RTL | https://developer.apple.com/design/human-interface-guidelines/right-to-left |
| MDN-LOGICAL | https://developer.mozilla.org/en-US/docs/Web/CSS/CSS_logical_properties_and_values |
| WP-RTL | https://codex.wordpress.org/Right-to-Left_Language_Support |
| G-HREFLANG | https://developers.google.com/search/docs/specialty/international/localized-versions |
| SCHEMA-REL | https://schema.org/RealEstateListing |
| SCHEMA-APT | https://schema.org/Apartment |

### 9.6 Internal context
- batch1_notes.md in the same folder: the broker's recent Instagram listings (titles and figures used only for illustrative headlines and the NIS 27,000 rental example).

### 9.7 Open items to verify before launch
- Additional-apartment and foreign-resident purchase tax schedule after 31 December 2026 (sources disagree on end date) [KZ-PT, BIZ-PT, ILAN].
- Scope of nadlan.gov.il transaction modules for deep links [NADLAN-GOV].
- Whether the Fair Rental Law NIS 20,000 threshold has been updated (Kol Zchut shows no indexation mechanism) [KZ-HAB].
- Legal wording of disclaimers and consent text with Israeli counsel (not researched here).
