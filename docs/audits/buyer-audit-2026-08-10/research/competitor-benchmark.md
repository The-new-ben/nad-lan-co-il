# Competitor UX benchmark: the skeptical buyer and office tenant

**Prepared for:** Nadlan 360 buyer audit  
**Access date for every URL in this report:** 2026-08-10  
**Scope:** residential buying and commercial office leasing; desktop and mobile decision journeys; patterns relevant to ToHa, Park, Living, Premium, and interactive 3D/floor experiences.

## Evidence rules

This benchmark deliberately separates evidence from interpretation:

- **Observed — live:** interacted with the public page in a real browser on 2026-08-10. No form was submitted and no account state was changed.
- **Observed — indexed:** current page content was visible through search-engine indexing, but direct browser access was blocked or gated. It is weaker evidence than a live observation.
- **Documented — official:** the platform's own product/help/API documentation describes the behavior. This establishes intent, not necessarily the exact current public rendering.
- **Inferred / recommendation:** a proposed Nadlan pattern derived from the evidence. It is not represented as a competitor fact.
- **Blocked / gated:** an anti-bot control, paywall, login, or error prevented full direct verification. The limitation is stated rather than silently filled with assumptions.

No competitor images, text, data feeds, or design assets were copied. URLs are supplied so the development and product teams can verify the source.

## Executive conclusion

No single competitor answers every question a cautious foreign buyer or an American startup tenant will ask. The best decision journey is a composite:

| Decision need | Best current reference | What is strong | Important limitation |
|---|---|---|---|
| Residential search, map and commute | Zillow | Search/map filters, custom boundaries, school layers, saved-search alerts, mode-based commute filtering | Direct property pages were anti-bot blocked in this audit; use official documentation as the authoritative behavior reference |
| Residential property dossier | Compass | Anchored long-form detail, multi-mode media, complete carrying costs, public history, records, nearby comps, explicit disclaimers | It is a residential pattern and does not solve commercial availability or fit-out |
| Commercial list and suite availability | LoopNet | Space-level rows with floor/suite, area, rent, term, build-out/condition, availability, amenity and mobility context | Direct rendering was anti-bot blocked; indexed current content was used |
| Commercial diligence and verified comps | CoStar | Property records, lease/sale comps, tenants, stack plans, analytics and verification freshness | Full workflow is a paid product; only official public product documentation was assessed |
| Current commercial disclosure behavior | Rightmove | Live search-to-detail journey, explicit fields, floor-plan/media routes, nearby stations, disclosures, mobile Call/Email tray | Many values are allowed to remain “Ask agent”; the user must still leave the evidence path to resolve them |
| Israel transaction and neighborhood evidence | nadlan.gov.il | Address search, government-data framing, sale/rent/nearby tabs, localized indicators, transit and environmental evidence | Exact address tested had no transactions; some fields showed unknown; a visible token verification error occurred |
| Israel market interpretation | Madlan and Nadlan Center | Address/neighborhood interpretation and current editorial office-market context | Direct Madlan pages were blocked; Nadlan Center is editorial rather than a property decision tool |
| Israel project storytelling and plan orientation | Nadlan Master | Direction-labeled apartment plans, project narrative, map and consent-aware lead form | No live inventory stack, exact unit pricing, comps or decision-grade commute layers |
| Nearby-place comprehension | Booking.com | Plain-language categorized nearby distances, review/facility context and availability CTA | Hospitality pattern only; distances are not a substitute for office commute or due diligence |
| Accessibility and map/media ideas | Airbnb | Officially documented accessibility-feature evidence, amenity structure, saved map places and trip distance | Useful pattern reference only, not a property pricing or records authority |

The competitive opening is therefore not “more content.” It is **one evidence-backed decision surface** where the selected building, selected floor, map, price, commute, availability, fit-out, records, risk flags, and the exact question sent to an adviser all stay synchronized.

## What a skeptical user must be able to decide

A user unfamiliar with Israel should be able to answer these questions without knowing local terminology and without opening another site:

1. **What exactly is available?** Building, tower, floor, compass orientation, suite/unit, net and gross area, status, release date, and last verification time.
2. **What will it cost all-in?** Asking price/rent, unit basis, VAT, management, municipal tax, parking, indexation/escalations, fit-out contribution, deposit/guarantees, legal/broker costs, and an explicitly labeled estimate of monthly and first-year occupancy cost.
3. **Will the space work?** Current condition, permitted use/occupancy, people capacity, test-fit, dimensions, daylight/views, HVAC, power, backup, connectivity, loading, access, security, accessibility, showers/bikes, parking/EV and building certifications.
4. **Can the team live with the location?** Door-to-door time by car, transit, bike and foot; peak/off-peak ranges; station entrances and service frequency; parking constraints; real nearby essentials and employee amenities.
5. **Can the evidence be trusted?** Source, observed/effective date, verification owner, method, confidence, conflicts, exclusions and what is unknown.
6. **What happened in the market?** Comparable closed deals, asking-versus-achieved context, price/rent history, tax/public records, neighborhood and submarket ranges, and a defensible explanation of estimate limitations.
7. **Can I compare and return?** Save/share a specific selected floor and map state; compare spaces on equivalent units; export a decision brief.
8. **Can I resolve the last unknown immediately?** Ask a question tied to the selected asset/floor/field, with attachments and consent, see the expected response time, and keep the context after submission.

## Benchmark by journey pattern

### 1. Search list → selected map item → detail

**Observed / documented competitor behavior**

- **Zillow:** official help documents a synchronized map/list search with location entry, filters, map type, custom-drawn boundary, schools and saved-search updates. Mobile documentation exposes deeper property filters. A destination-based commute filter is officially documented for walk, bike, transit and car, including rush/off-peak choices. Direct property rendering was blocked in this audit.
- **LoopNet:** current indexed search exposes a list beside a map, result cards with space/rate/class/year summaries, virtual-tour indicators, brokers, draw polygon/radius and map layers for transit, traffic, biking and places. Current indexed details move from a property card to space rows and the building dossier. Direct rendering returned an access-denied response.
- **PropertyShark:** indexed search presents space/property cards with type, asking rent, available-space counts/ranges and a map. Official help describes map/spatial search and regional data coverage.
- **Rightmove — observed live:** commercial results showed image cards, asking rent, size, badge/summary and a property link. Opening a card led to a full, route-addressable detail. Search alerts and saved search were visible. This was the cleanest fully live commercial transition verified in the audit.
- **nadlan.gov.il — observed live:** the home search supports free text and proposes an exact address. Selecting `יצחק שדה 38 תל אביב יפו` opened an address route with sale/rent/nearby tabs and a map. It is evidence-first rather than an inventory marketplace.
- **Yad2:** direct search was stopped by Radware browser verification. Indexed cards expose the familiar minimum set: price, location, property type, rooms, floor and square meters; sponsored-project cards add ranges and starting price.

**Gap to close for Nadlan**

The map cannot be decorative. Selecting a pin, card, tower, floor or 3D hotspot must update the same canonical selection object:

```ts
type DecisionSelection = {
  projectId: number;
  projectContractId: string;
  buildingId: string;
  towerId: string;
  floorId: string;
  suiteId: string | null;
  view: "list" | "map" | "stack" | "model" | "plan";
  mapViewport?: string;
  commuteProfileId?: string;
};
```

Encode that state in the URL. The tuple is mandatory even for a one-building/one-tower project, and translated labels never substitute for IDs; two towers may legally share the same visible floor label. Browser Back must restore the previous list, scroll, filters and map viewport. On desktop, open a detail rail without erasing context. Competitors often use an expandable half-height sheet on mobile; Nadlan should **not** copy it for the 3D theatre because its tested 46vh sheet retained coverage and inner-scroll failures. Nadlan’s selected floor instead becomes one bounded decision viewport, with heavy evidence isolated in a full-screen tool. A pin must never open a generic building card when the user selected a particular available floor.

### 2. Detail information architecture

**Observed live — Compass**

The tested Compass property used anchored sections for Overview, Location, Property History, Public Records, Schools, Similar Homes and Nearby Home Values. The top facts combined sold price, beds, baths, area and price per square foot. Details then exposed status, days on market, taxes, common charges, total rooms, property type, MLS, year, county and buyer-agent compensation. The page also contained amenities, building facts, map, “Add your commute,” payment calculator, property history, public-record links, comparable homes and nearby values.

**Observed live — Rightmove**

The commercial page grouped headline price/size, primary and alternative uses, key features, description, amenities, media, contact, map/street view, stations, additional information, EPC and environmental data. Unknown commercial values were not hidden; lease length, EPC, parking, price per square foot and desks/capacity appeared as “Ask agent.”

**Recommendation**

Use a short decision header followed by anchored sections. The selected space, not the project marketing story, is the page's primary noun:

1. Decision summary
2. Availability and floor stack
3. Plans, 3D, photos and views
4. Pricing and all-in cost
5. Fit-out and infrastructure
6. Building operations and access
7. Map, commute and neighborhood
8. Comparable deals and history
9. Records, risks and disclosures
10. Contact, questions and next steps

Each section header should show a completeness status such as `Complete`, `2 items unverified`, or `Data requested 10 Aug 2026`. Do not use promotional prose to fill a missing fact.

### 3. Gallery, fullscreen and Back behavior

**Observed live — Compass**

The property opened a media dialog from the photo count. The dialog retained price, core facts and address and included Contact, Save, Share and Close. Media modes were visible together: Photos, Virtual Tour, Floor Plan, Map and Street View. Closing returned to the same detail state. This keeps the identity and conversion context while the user inspects evidence.

**Observed live — Rightmove**

Selecting a photo navigated to a dedicated media route ending in `/media?id=photos0`. The mobile viewer supplied Back, Photos/3D Tours tabs, `1 of 6`, share and agent contact. Route-backed media is resilient: the browser Back action is predictable and a particular media state can be shared.

**Documented — Airbnb**

Airbnb's official help emphasizes complete interior/exterior/neighborhood media and evidence for accessibility features. Its accessibility program describes verified images and, where available, Matterport-derived two-dimensional floor plans with dimensions. This is a useful trust pattern: the image proves a declared capability.

**Recommendation**

Use a route-backed media viewer with one consistent order:

`3D model → selected-floor plan → photos → 360 tour → daylight/view simulation → map/street → documents`.

Always show selected building/tower/floor, orientation, media count, capture/render date and whether an image is a photograph, verified measurement, marketing render, virtually staged view or simulation. Preserve zoom/rotation when switching floor plan ↔ 3D. On mobile, provide a prominent Back control in addition to browser Back. Never place a lead form over the plan the user is trying to read.

### 4. Availability and the floor stack

**Observed — LoopNet indexed current pages**

The current 22 Cortlandt Street detail exposed a space row for the 23rd floor / Suite 2300, 9,000–18,700 square feet, 10–15 year term, $61/SF/year, monthly and yearly equivalents, office use, condition and a future availability date. Other indexed current examples exposed multiple suites, floors, size, rate, build-out and availability; some included floor plans or Matterport tours. This is the closest public-market benchmark for an actionable commercial availability table.

**Documented — CoStar**

Official Lease Comps help describes result list, analytics and map tabs, and detail tabs for Summary, Lease Analysis, Lease Comps, Property, Tenant, Analytics and Images. The tenant detail documentation includes a stacking plan. Official marketing pages describe vacant space, tenants, rents, floor plans, 3D assets and transaction context.

**Observed live — Nadlan Master**

The tested project page labeled apartment-plan types and compass orientations—for example, southwest/northwest and northeast/southeast variants. That is useful orientation language, but there was no live tower/floor/unit availability matrix and no exact unit pricing.

**Critical Nadlan requirement**

Every 3D floor must resolve to a real availability record, even when the state is unknown:

| Field | Required behavior |
|---|---|
| Status | `Available`, `future`, `under offer`, `option/hold`, `leased/sold`, `not released`, or `unknown`; color plus text/icon, never color alone |
| Identity | Building, tower, floor, suite/unit, address and stable ID |
| Orientation | North arrow plus named primary exposures and view corridor |
| Area | Net usable, rentable/gross and efficiency ratio; display measurement standard |
| Divisibility | Minimum/maximum contiguous area and legal subdivision assumptions |
| Delivery | Current condition, offered condition, fit-out responsibility and target delivery date |
| People | Legal maximum occupancy and practical planning range with chosen desk-density assumption |
| Price | Asking basis, currency, period and all mandatory additions |
| Evidence | Source, verifier, verified-at timestamp and confidence |
| Action | Open dossier, compare, save, download plan, ask specifically about this space |

A floor that is unavailable should remain inspectable in a subdued state when it provides stack context. Clicking it must explain the status rather than doing nothing. An `unknown` status must not be rendered as available. If two sources conflict, show the conflict and the verification request rather than silently selecting the more favorable value.

### 5. Area, facilities and amenity layers

**Observed live — Booking.com**

The tested Tel Aviv hotel page translated “nearby” into named places with readable distances, including the promenade, public squares, cultural landmarks, park and museums. It attributed description distances to OpenStreetMap. Facilities and review context sat near a See availability action. This is effective progressive disclosure for a visitor who has no local mental map.

**Documented — Airbnb**

Official help describes map pins that expose a place and allow it to be saved into the itinerary, with time/distance from the stay. Official amenity and accessibility filters provide structured categories rather than one long marketing list.

**Observed live — nadlan.gov.il**

The “what's nearby” route grouped real-estate indicators, education, gardens/parks, services/commerce/leisure, transport/accessibility, demographics and environment. The tested neighborhood transport panel reported 137 bus lines reaching the neighborhood, 22 stations/routes, 24 public parking areas and an average 113-meter distance to a bus stop. The environmental panel showed a current air-pollution indicator, cellular antennas and industrial-emission counts. A station table supplied station ID, name, address and “show on map.”

**Observed live — Rightmove**

The commercial detail included a map, street view and nearest stations with distances. This is useful orientation but not a door-to-door commute model.

**Recommendation**

Put contextual layers on the selected asset's map, not in an unrelated article:

- Rail/light rail/metro and station entrances
- Bus stops, routes, headways and first/last service
- Peak and off-peak car time, current/typical traffic and route reliability
- Parking garages, expected monthly cost, EV charging and bike parking
- Cafés, lunch, groceries, pharmacy, healthcare, gyms and childcare
- Hotels, airport/train access and visitor facilities
- Parks, shade/walkability, noise, construction, air quality and other environmental constraints
- Schools and community layers for residential journeys

Every point must show **straight-line distance, network distance and estimated time**, source and last update. A count such as “137 lines” is not enough: rank the options relevant to the chosen employee/home profile. Let a user add up to three origins—home cluster, airport/hotel and client destination—and save them with the comparison.

### 6. Commute, transport and traffic

**Documented — Zillow**

Zillow officially documents a commute-time filter in which the user sets a destination, chooses car, transit, bike or walk, and can distinguish rush-hour from off-peak driving. This turns the map from a static amenity picture into a personal feasibility test.

**Observed live — Compass**

The Location section exposed “Add your commute,” placing the decision inside the property dossier.

**Observed live — nadlan.gov.il / Rightmove**

Both provide transport evidence, but at different resolution: nadlan.gov.il exposes neighborhood counts and stations; Rightmove gives nearby station distance. Neither observed public surface answered a company-specific peak door-to-door question on the selected office.

**Recommendation**

Provide a commute drawer accessible from the main header and map. It should show:

- mode, departure window and day type;
- median time plus a realistic range, not false single-minute precision;
- transfers, walking segments and accessible-route constraints;
- typical traffic and exceptional-condition caveat;
- source/provider and calculated-at time;
- an “open route” link and a save-to-comparison action.

For an overseas startup, include Ben Gurion Airport, Savidor/HaShalom rail, major hotels and a user-entered employee catchment as presets. Clearly distinguish planned transport from operating transport and display the expected opening date/source for future infrastructure.

### 7. Price, total cost, comparables and history

**Observed / documented — Zillow**

Official Zestimate material explains that the value is a model estimate rather than an appraisal, provides model context and reports that history may extend up to ten years when data exists. Indexed property content exposes price/listing and public-tax history. The key lesson is not the estimate itself; it is putting the estimate, history and limitations together.

**Observed live — Compass**

The tested page exposed sold price, price per square foot, taxes, common charges and a payment calculator. Its property-history table showed date, event, source, price and appreciation and linked to a public ACRIS record. Similar and nearby values supplied comparable context. The calculator and records included limitations rather than implying guaranteed accuracy.

**Documented / observed — Rightmove**

Rightmove's sold-price product says it is based on HM Land Registry information and can retain historic photos/floor plans. Its current commercial detail showed rent and size, while missing values such as price per square foot were explicitly “Ask agent.” An older indexed commercial page contained annual and per-square-foot equivalents, business-rates caveat, VAT and lease terms, but that route returned HTTP 410 on 2026-08-10 and must not be treated as a current live example.

**Documented — CoStar**

Official product pages describe verified sales comps with asking versus achieved pricing, time on market, transaction notes, parties, brokers, tax/loan/deed/public records and lease-deal insight. This is the due-diligence benchmark for explaining a commercial comparable, not just listing a nearby number.

**Observed live — nadlan.gov.il**

The tested address route had no exact-address deals. The site preserved that zero rather than inventing a value, then supplied neighborhood indicators and room-based charts, with some categories marked unknown. It disclosed that analysis combines multiple databases and may contain inaccuracies.

**Observed / indexed — Madlan, Nadlan Center, Yad2 tools**

Madlan's indexed address/project pages expose transactions, transport and neighborhood interpretation. Nadlan Center supplies editorial/current office-market rent and occupancy context by market area, but it is separate from a selected listing. Yad2's official Yadata/Yzer surfaces valuation inputs, demand/trends, recent transactions and planning context with an accuracy caveat.

**Commercial all-in-cost requirement**

Display the asking basis first, then calculate an auditable occupancy-cost bridge:

```text
Base rent
+ management/service charge
+ municipal tax (arnona)
+ parking and storage
+ VAT where applicable
+ utilities/after-hours HVAC estimate
+ fit-out amortization and furniture assumption
+ brokerage/legal/move assumptions
- landlord contribution / free rent
= estimated monthly run-rate and first-year cash cost
```

Show NIS/month, NIS/sqm/month and annual total; allow USD conversion with exchange-rate timestamp. Keep asking, estimated and closed-comparable values visually distinct. Every comp needs distance, date, building grade, floor/condition, area, term and why it is or is not comparable. “Market average” without methodology is not decision-grade.

### 8. Disclosures, confidence and missing data

**Observed live — Compass**

The page stated that measurements and condition should be independently verified, photos may be virtually staged or digitally enhanced, and listing data is not guaranteed. It named data sources. This is a strong example of putting media and data limitations near the evidence.

**Observed live — Rightmove**

The page stated that the advert is not warranted by Rightmove and is maintained by the agent. Missing fields were visible as “Ask agent.” This is honest but incomplete: the user still lacks a structured resolution path per missing fact.

**Documented — CoStar**

Official listing help says a listing can be removed if it is not updated or verified at least every 75 days. A visible verification cadence is a useful commercial trust standard, although Nadlan should use shorter SLAs for active availability.

**Observed live — Nadlan Master and nadlan.gov.il**

Nadlan Master used marketing-render and errors/omissions disclaimers. nadlan.gov.il explicitly surfaced unknown chart values and analysis limitations. A token verification error modal was also seen during the address/neighborhood journey, showing that evidence access needs graceful error recovery.

**Recommendation: an evidence envelope for every material fact**

```json
{
  "state": "source_estimate",
  "value": 130,
  "unit": "ILS/rentable_sqm/month",
  "scope": "project/toha2/building/toha2/tower/main/floor/F18",
  "effective_at": "2026-08-01",
  "sources": [{
    "type": "owner_document",
    "label": "Owner data-room term sheet",
    "uri": null,
    "document_id": "term-sheet-F18-r3",
    "revision": "3",
    "published_at": "2026-08-01",
    "retrieved_at": "2026-08-10T11:30:00+03:00"
  }],
  "observations": [{
    "observation_id": "obs-term-sheet-F18-r3",
    "value": 130,
    "scope": "Floor F18 base rent only",
    "source": "term-sheet-F18-r3"
  }],
  "verified_at": null,
  "expires_at": "2026-08-15T23:59:59+03:00",
  "owner": {
    "team": "landlord-leasing",
    "accountable_role": "leasing director",
    "contact_ref": "internal-route:toha2-leasing"
  },
  "confidence": "medium",
  "reason": null,
  "applicability": "screening estimate; not an offer",
  "conflict_ids": [],
  "note": "Base asking rent indication",
  "caveat": "Excludes management, VAT and parking",
  "required_document_ids": ["signed-current-heads-of-terms"],
  "decision_grade": "screening_only"
}
```

This is the exact server snake_case envelope; the browser may change casing only. Use the four canonical evidence states: `unknown`, `source_estimate`, `verified`, `contradictory`. “Reported” belongs in source type/provenance; stale is derived from `expires_at`; requested is a workflow flag; withheld/not-applicable are reasons on an unknown envelope. A missing value should render an inline card with:

- the exact missing question;
- why it matters;
- who owns the answer;
- request sent / not sent status;
- expected response time;
- “Ask this question” prefilled with property, floor and field;
- subscribe to answer update.

Never replace a missing fact with “contact us for details” at page level. The contact action must preserve what was missing.

### 9. Office infrastructure and fit-out

**Observed — current indexed commercial listings**

- LoopNet examples included full or partial build-out, floor/suite, future/immediate availability, people capacity, furniture, kitchens, conference/AV, security, high-speed internet/wiring, services and Matterport/floor-plan assets.
- PropertyShark's indexed 405 Lexington example exposed a 45th-floor full-build-out turnkey sublease, 10,511 square feet, 68 workstations, four conference rooms, three offices, pantries, reception, furniture, views and tenant-club access.
- CommercialCafe indexed details exposed floor, size, lease type, tentative availability and a contact action with property intent.
- Rightmove's live page exposed primary/alternative uses and a long building-amenity set, but capacity/desks and several commercial facts remained “Ask agent.”

**Recommendation: mandatory floor-specific office schema**

At minimum, collect and display:

- net usable / rentable / gross area and measurement standard;
- current layout, condition, handover specification and demolition constraints;
- test-fit variants, desk count, meeting rooms, focus rooms, kitchen, reception and accessible WC;
- legal use, permitted occupancy, fire/life-safety status and accessibility route;
- slab-to-slab and clear ceiling heights, column grid, raised floor and loading capacity;
- HVAC type, zones, standard hours, after-hours cost, fresh-air capacity and landlord control;
- electrical capacity, distribution, generator/UPS coverage and resilience assumptions;
- fiber carriers, entry diversity, risers, mobile coverage and provisioning lead time;
- security, 24/7 access, loading/delivery, freight lift and visitor management;
- parking ratio and price, EV, bicycle rooms, showers and lockers;
- green/building certifications, energy evidence, utility responsibility and waste services;
- furniture/equipment inclusion, landlord work, tenant allowance, approval process and delivery schedule.

The same schema powers the floor card, compare table, PDF brief and adviser question. Do not bury these facts in marketing copy or a downloadable brochure only.

### 10. Contact, lead routing and mobile controls

**Observed live — Compass**

The desktop detail showed named agents and an “Inquire About Property” action. At a 390×844 viewport, the inquiry control sat in a fixed full-width bottom ancestor, keeping conversion available without covering the main page.

**Observed live — Rightmove**

At mobile width the detail and media viewer used a fixed bottom tray with Call and Email. Agent enquiry and share remained accessible in the media route.

**Observed live — Nadlan Master**

The project included an inline name/email/phone/message form and required privacy consent before submit. It also rendered floating contact and duplicated off-canvas form instances in the DOM. Consent is positive; duplicated competing lead surfaces risk confusion, accessibility repetition and inconsistent analytics.

**Observed / indexed — LoopNet, CommercialCafe and PropertyShark**

Commercial listings tie Call/Message/Contact to the property or broker. CommercialCafe's indexed form carries the property intent. The important pattern is context, not merely the existence of a form.

**Recommendation**

Use one lead composer with multiple entry points. Its context payload should contain:

```json
{
  "assetId": "toha-2",
  "floorId": "18",
  "spaceId": "18-ne",
  "questionCode": "HVAC_AFTER_HOURS_COST",
  "locale": "en-US",
  "sourceUrl": "...",
  "savedComparisonId": "..."
}
```

The user sees property/floor, selected question, channel, adviser identity/team, consent, privacy link and realistic response SLA. CRM routing should be asset + deal type + language + question expertise, with owner, duplicate detection, timestamp and closed-loop status. Send the user a copy/secure link to the question and preserve the page state. Track `lead_started`, `question_selected`, `consent_checked`, `lead_submitted`, `assigned`, `first_response`, `answered`, `tour_booked`, and `qualified`—without sending sensitive free text to general analytics.

Compass and Rightmove demonstrate compact mobile action trays, but Nadlan’s old fixed/sticky controls already collide with the selected scene. Keep `Ask`, `Save` and the commercial CTA inside the bounded decision surface; open the contextual enquiry composer as a body-level full-screen tool. Respect safe-area insets. Do not show floating WhatsApp/contact bubbles on top of map zoom, 3D controls or media captions.

### 11. Compare, save and share

**Observed / documented competitor behavior**

- Compass retained Save and Share in both detail and media.
- Rightmove retained share/contact in detail and media and offered saved-search/alert paths.
- Zillow officially documents saving searches and receiving updates.
- LoopNet indexed search/details expose saving and notification patterns.
- Nadlan Master claims project comparison on the site, but no visible comparison control was found on the tested live project/home flow.

**Recommendation**

Save and share the **decision state**, not only the building URL: selected floor/space, open media, filters, commute origins, cost assumptions, locale/currency and visible data version. Comparison should normalize units and keep unknowns visible. Recommended comparison groups:

- availability and timing;
- usable area/efficiency/capacity;
- base and all-in cost;
- fit-out/infrastructure;
- commute and nearby essentials;
- evidence quality and unresolved questions.

Allow a share recipient to open read-only without an account. If data changed since the share was created, show a version banner and a compact change log.

### 12. Mobile decision experience

Competitors demonstrate three useful mobile principles:

1. **Persistent next action:** Compass inquiry and Rightmove Call/Email remain reachable in a bottom tray.
2. **Route-aware media:** Rightmove's media view supplies its own Back control and count.
3. **Progressive depth:** property facts remain readable before the user enters a large media or map mode.

Nadlan should use a single-column summary, wrapping non-scrolling status chips and a fixed evidence summary inside one selected-floor viewport—**not** a bottom sheet, horizontal carousel or expandable in-surface group. Floor pack, context map, cost, media and infrastructure open as body-level full-screen tools with one-tap Back and bounded button-driven pagination; a swipe gesture may optionally change the same page, but every page must remain reachable through visible buttons and no scroll container. The 3D model must never be the only route to a floor. Provide a text/table equivalent for accessibility, low-power devices and users who need to compare values. Test at 320, 360, 390, 412 and 768 CSS pixels; include landscape, 200% zoom, keyboard-only and screen-reader order. Every fixed control needs safe-area padding and must not obscure the final row of a table or map attribution.

## Platform profiles and access notes

### Zillow — residential search and personalized location feasibility

- **Evidence:** official help/product documentation plus indexed property content; live property detail blocked with HTTP 403/denial.
- **Strengths:** map/list search, filters, custom boundaries, school context, saved-search updates, commute-time filter, modeled value/history and public-price/tax context.
- **Weakness for Nadlan use case:** no commercial floor availability/fit-out; model estimate must not be confused with an offer or appraisal.
- **Adopt:** personal commute, saveable map state, estimate limitations and history.

### Compass — residential detail dossier

- **Evidence:** live direct interaction with the Brooklyn property detail, its media dialog and 390×844 mobile layout.
- **Strengths:** anchored dossier, media modes, carrying cost, history/public record, comps, transparent disclaimers, save/share/contact continuity.
- **Weakness:** not a commercial stack/occupancy workflow.
- **Adopt:** one long but navigable dossier and consistent context in fullscreen media.

### LoopNet — public commercial marketplace

- **Evidence:** current indexed search/details; live direct access denied.
- **Strengths:** space-level availability rows, rate units, term, dates, build-out, building facts, amenities, mobility scores, map layers and broker contact.
- **Weakness:** availability trust still depends on listing verification; direct interaction could not be verified in this audit.
- **Adopt:** floor/suite rows and map/list pattern; strengthen with source/version per value.

### CoStar — paid commercial intelligence

- **Evidence:** public official product and help documentation; no paid-product session.
- **Strengths:** property/space/tenant/transaction/comps/analytics depth, stack plan, verified data and update cadence.
- **Weakness:** gated workflow and enterprise complexity; not evidence of an anonymous public user's experience.
- **Adopt:** verification metadata, comp anatomy and structured tabs; simplify for self-service users.

### CommercialCafe — commercial listing lead path

- **Evidence:** current indexed details; direct access stopped by Cloudflare 403.
- **Strengths:** floor/space, lease type/availability and property-context contact.
- **Weakness:** direct map/media/mobile behavior was not verifiable here.
- **Adopt:** preserve selected property/suite in the lead.

### PropertyShark — commercial and public-record context

- **Evidence:** indexed listings plus official help; direct access stopped by Cloudflare 403.
- **Strengths:** detailed fit-out/capacity on some listings, map/spatial search, zoning/land use, characteristics and comparables; its help acknowledges regional data differences.
- **Weakness:** direct current rendering not verified and data coverage can vary.
- **Adopt:** structured fit-out/capacity and explicit coverage statements.

### Rightmove — current live commercial disclosure and media

- **Evidence:** live search, detail, media route and mobile layout; official feed, sold-price and broadband documentation.
- **Strengths:** predictable search→detail, explicit commercial fields, route-backed gallery, nearby stations, disclosures and mobile contact tray. Its feed supports floor plans, EPC, brochures and virtual tours.
- **Weakness:** “Ask agent” is honest but shifts basic diligence to a contact; postcode broadband is an estimate, not office circuit evidence.
- **Adopt:** route-backed media, explicit unknowns, documents; add an inline structured request workflow.

### Booking.com — visitor-friendly nearby comprehension

- **Evidence:** live Tel Aviv property page.
- **Strengths:** categorized named places, readable distance, attribution, facilities and review proof.
- **Weakness:** hospitality availability/reviews are not sale/lease evidence.
- **Adopt:** plain-language nearby list synchronized with map; avoid star/review metaphors for professional due diligence.

### Airbnb — media, saved places and accessibility evidence

- **Evidence:** official help documentation only for the cited patterns.
- **Strengths:** media expectations, saved map points, travel time/distance and evidence-backed accessibility features.
- **Weakness:** no comparable transaction, title, building or lease diligence.
- **Adopt:** accessible media evidence and user-saved nearby points.

### Yad2 — Israel inventory baseline

- **Evidence:** indexed search/cards and official Yad2 tools/content; live search stopped by Radware.
- **Strengths:** familiar compact listing facts; Yadata/Yzer add valuation, demand, transaction and planning context.
- **Weakness:** direct decision flow and commercial depth could not be validated; card facts do not answer a foreign user's full diligence questions.
- **Adopt:** compact baseline facts; add sources, translation and all-in cost.

### Madlan — Israel address/neighborhood interpretation

- **Evidence:** indexed residential, project and ToHa commercial listing content; official professional-system help; direct listing blocked 403.
- **Strengths:** transactions, schools, transport, neighborhood/project explanation and commercial listing facts such as rooms/kitchens/security where supplied.
- **Weakness:** direct present UX not verified; evidence can remain dispersed across address, project and listing contexts.
- **Adopt:** local interpretation beside the selected asset, not a separate research detour.

### Nadlan Center — market editorial context

- **Evidence:** public editorial pages live/indexed.
- **Strengths:** current office-market rent/occupancy interpretation by business area and historical context.
- **Weakness:** it is not an inventory or floor-decision application.
- **Adopt:** source market commentary into a clearly labeled “market context” block with publication date; never represent editorial figures as a selected floor's price.

### Nadlan Master — project narrative and plan orientation

- **Evidence:** live home and project interaction.
- **Strengths:** rich project story, direction-labeled plans, map, marketing-render disclosure and consent-aware lead form.
- **Weakness:** no live inventory, status by floor/unit, exact pricing, transaction comps, commute model or strong map layers; duplicate lead surfaces.
- **Adopt:** orientation labels and consent; replace editorial sprawl and duplicated forms with a decision stack.

### nadlan.gov.il — government transaction/neighborhood evidence

- **Evidence:** live address search, sale/nearby routes, transport/environment accordions and map on 2026-08-10.
- **Strengths:** government-data framing, multiple search modes, explicit unknowns, local indicators, transit station details, parking and environmental evidence.
- **Weakness:** exact-address data may be empty; several outputs are neighborhood aggregates; analysis admits possible inaccuracies; a token verification failure interrupted the tested journey.
- **Adopt:** link directly to authoritative evidence, label geographic scope and preserve unknown; add resilient retries and a human-readable fallback.

## “One-click answer” reference UX for Nadlan

The following is a product requirement, not a claim about competitor behavior.

```text
Search/map/3D selection
  → Decision drawer for the exact building + floor + space
      → Availability + orientation + verified time
      → All-in cost + assumptions
      → Capacity + fit-out + infrastructure
      → Commute + nearby essentials
      → Media + plans + records
      → Comps + market context
      → Risks, unknowns and evidence sources
      → Save / compare / share / ask this exact question
```

The drawer should answer the top questions without navigation; deeper sections open in-place and update the URL. “One click” does not mean crowding every fact above the fold. It means the user never has to guess which menu, project article or third-party site holds the answer and never loses the selected floor while exploring it.

### Required response to a missing datum

Example for a floor with no confirmed HVAC detail:

> **After-hours HVAC cost — not yet verified**  
> Needed to estimate true occupancy cost. Owner: building operations. Last requested: 10 Aug 2026. Expected answer: within 1 business day.  
> `[Ask this question]` `[Notify me]` `[See current assumptions]`

The question composer opens inline with the floor already attached. Once answered, the evidence envelope changes to `source_estimate` or `verified`, includes the source/date and notifies every saved comparison that used the old assumption. “Reported by owner” may remain a human-readable provenance label, but it is not a fifth evidence state.

## Priority patterns to implement

| Priority | Pattern | Why it closes a competitive gap | Acceptance signal |
|---|---|---|---|
| P0 | Canonical building/floor/space selection in URL | Prevents map, 3D, list and dossier from disagreeing | Back/forward/share restore selection, filters and viewport |
| P0 | Live availability stack with controlled statuses | Public commercial competitors expose space rows; Israeli project pages often stop at plans/story | Every floor is inspectable; unknown cannot appear available; freshness is visible |
| P0 | Evidence envelope and inline missing-data request | Competitors disclose uncertainty but usually do not resolve it per field | Every material fact has status/source/date; every unknown can be asked in one click |
| P0 | All-in commercial cost model | Asking rent alone is unusable to an overseas tenant | User can reconcile every included/excluded component and currency timestamp |
| P0 | Floor-specific fit-out/infrastructure schema | Strong commercial listings surface capacity/build-out; marketing pages do not | Selected floor answers capacity, delivery, MEP/connectivity/access questions |
| P1 | Personalized commute with peak/off-peak modes | Zillow demonstrates personal feasibility; local layers are mostly generic | Saved origins and mode/time ranges compare across properties |
| P1 | Route-backed media hub | Compass/Rightmove preserve identity and Back behavior in media | Deep link opens same floor/media; close/back restores prior scroll/state |
| P1 | Context-preserving lead and CRM routing | Property contact is common; exact unresolved question is usually lost | Submitted lead includes asset/floor/question and has owner/SLA/status |
| P1 | Normalized compare/save/share | Users otherwise rebuild the decision in spreadsheets | 2–4 spaces compare on equivalent units with unknowns/version changes shown |
| P2 | Curated nearby and environmental layers | Booking and government data make unfamiliar areas legible | Each point shows time/distance/source; planned vs operating infrastructure differs |

## Source registry

All links below were accessed on **2026-08-10**. A source may be live, indexed, officially documented or blocked as specified.

### Zillow

- Official search help: https://zillow.zendesk.com/hc/en-us/articles/227953268-How-do-I-search-for-properties
- Official search/help alternative: https://zillow.zendesk.com/hc/en-us/articles/203523760-How-do-I-search-for-homes-
- Official Android search filters: https://zillow.zendesk.com/hc/en-us/articles/360000998828-How-do-I-search-for-homes-on-the-Zillow-mobile-app-Android-
- Official commute filter: https://www.zillow.com/news/zillows-commute-time-filter/
- Official Zestimate explanation: https://www.zillow.com/zestimate/
- Property detail attempted; blocked: https://www.zillow.com/homedetails/70-Barrensdale-Dr-Severna-Park-MD-21146/36065110_zpid/

### Compass

- Live tested property detail/media/mobile: https://www.compass.com/homedetails/545-Washington-Ave-Unit-606-Brooklyn-NY-11238/207T3R_pid/
- Indexed floor-plan example: https://www.compass.com/listing/100-morton-street-unit-th-manhattan-ny-10014/455791970433108593/floorplans

### LoopNet and CoStar

- LoopNet current search; direct access denied, indexed content observed: https://www.loopnet.com/search/office-space/usa/for-lease/
- LoopNet 22 Cortlandt detail; direct access denied, indexed content observed: https://www.loopnet.com/Listing/22-Cortlandt-St-New-York-NY/3938731/
- CoStar products: https://www.costar.com/products
- CoStar property records: https://www.costar.com/products/property-records
- CoStar sales comps: https://www.costar.com/products/sales-comps
- CoStar tenants: https://www.costar.com/products/tenants
- CoStar Lease Comps result detail help: https://product.costar.com/LeaseComps/Help/en-US/LC_Result_Detail.htm
- CoStar tenant/stacking-plan help: https://product.costar.com/LeaseComps/Help/en-US/LC_Detail_Tenant.htm
- CoStar search result tabs: https://product.costar.com/LeaseComps/Help/en-US/LC_Search_Results.htm
- CoStar listing verification/update help: https://marketingcenter-help.costar.com/article/13-article-1-for-how-to-add-edit-update-listings

### CommercialCafe and PropertyShark

- CommercialCafe 600 Third Avenue; Cloudflare blocked, indexed content observed: https://www.commercialcafe.com/commercial-property/us/ny/new-york/600-third-avenue-2/
- CommercialCafe 69 Mercer; indexed content observed: https://www.commercialcafe.com/commercial-property/us/ny/new-york/69-mercer-street/
- PropertyShark NYC office search; direct access blocked, indexed content observed: https://www.propertyshark.com/cre/office/us/ny/new-york-city/
- PropertyShark 405 Lexington; Cloudflare blocked, indexed content observed: https://www.propertyshark.com/cre/commercial-property/us/ny/new-york/405-lexington-1/
- PropertyShark commercial listing help: https://support.propertyshark.com/hc/en-us/articles/360010663460-How-to-Find-Use-Commercial-Listings-on-PropertyShark
- PropertyShark product/data coverage help: https://support.propertyshark.com/hc/en-us/articles/360022586511-Overview-of-PropertyShark-Services-and-Features

### Rightmove

- Live commercial search: https://www.rightmove.co.uk/commercial-property-to-let/London.html
- Live tested commercial detail/media/mobile: https://www.rightmove.co.uk/properties/765063575843297
- Current feed API overview: https://api-docs.rightmove.co.uk/docs/property-feed-api-product/1/overview
- Official listing quality guidance: https://customerfaq.rightmove.co.uk/support/solutions/articles/7000096792-how-do-i-make-my-property-listing-stand-out-
- Sold prices: https://www.rightmove.co.uk/house-prices
- Sold-price source: https://customerfaq.rightmove.co.uk/support/solutions/articles/7000098008-where-the-sold-house-price-data-comes-from
- Broadband estimate methodology: https://customerfaq.rightmove.co.uk/support/solutions/articles/7000098828-how-is-broadband-speed-calculated-
- Stale indexed commercial example, HTTP 410 on access date: https://www.rightmove.co.uk/properties/124660286

### Airbnb and Booking.com

- Airbnb map/place help: https://www.airbnb.com/help/article/4192
- Airbnb amenity/accessibility filters: https://www.airbnb.com/help/article/3740
- Airbnb accessibility verification/floor-plan help: https://www.airbnb.com/help/article/3282
- Airbnb photo guidance: https://www.airbnb.com/help/article/746
- Live tested Booking.com Tel Aviv page: https://www.booking.com/hotel/il/dan-tel-aviv.en-gb.html

### Yad2

- Search attempted; Radware blocked, indexed content observed: https://www.yad2.co.il/realestate/forsale?page=1
- Tel Aviv search attempted; Radware blocked, indexed content observed: https://www.yad2.co.il/realestate/forsale/tel-aviv-area?property=1
- Official Yad2 buyer/local-information article: https://magazine.yad2.co.il/real-estate/%D7%A7%D7%95%D7%A0%D7%99%D7%9D-%D7%97%D7%9B%D7%9D-%D7%9B%D7%9C-%D7%94%D7%9E%D7%99%D7%93%D7%A2-%D7%91%D7%93%D7%A8%D7%9A-%D7%9C%D7%A7%D7%A0%D7%95%D7%AA-%D7%93%D7%99%D7%A8%D7%94-%D7%9E%D7%97%D7%9B%D7%94/23321
- Yadata valuation: https://yadata.yad2.co.il/property-valuation
- Yzer market information: https://yzer.yad2.co.il/

### Madlan, Nadlan Center and Nadlan Master

- Madlan ToHa commercial listing; direct 403, indexed content observed: https://www.madlan.co.il/commercial/listings/aiEBULuVrYY
- Madlan project page; indexed content observed: https://www.madlan.co.il/projects/%D7%91%D7%9F_%D7%A2%D7%98%D7%A8_19_%D7%AA%D7%9C_%D7%90%D7%91%D7%99%D7%91_%D7%99%D7%A4%D7%95
- Madlan address page; indexed content observed: https://www.madlan.co.il/%D7%99%D7%A6%D7%97%D7%A7-%D7%A9%D7%93%D7%94-38-%D7%AA%D7%9C-%D7%90%D7%91%D7%99%D7%91-%D7%99%D7%A4%D7%95-%D7%99%D7%A9%D7%A8%D7%90%D7%9C
- Madlan professional map/help: https://help.madlan.co.il/hc/he/articles/360008092118-%D7%9E%D7%A2%D7%A8%D7%9B%D7%AA-%D7%9E%D7%93%D7%9C%D7%9F-%D7%9C%D7%9E%D7%A7%D7%A6%D7%95%D7%A2%D7%A0%D7%99%D7%9D
- Nadlan Center current 2025 office-market summary: https://www.nadlancenter.co.il/article/14328
- Nadlan Center 2024 context: https://www.nadlancenter.co.il/article/10620
- Nadlan Center 2023 context: https://www.nadlancenter.co.il/article/9517
- Nadlan Master home: https://www.nadlanmaster.co.il/
- Nadlan Master live tested project: https://www.nadlanmaster.co.il/%d7%a0%d7%91%d7%95-%d7%a0%d7%95%d7%a3-%d7%94%d7%a9%d7%a8%d7%95%d7%9f-%d7%a0%d7%aa%d7%a0%d7%99%d7%94/

### nadlan.gov.il

- Live home/search: https://www.nadlan.gov.il/
- Live tested address/sale route: https://www.nadlan.gov.il/?view=address&id=53795926&page=deals
- Live tested neighborhood information route: https://www.nadlan.gov.il/?view=neighborhood_info&id=65210047&page=info

## Audit limitations

- Zillow, LoopNet, Yad2, Madlan, CommercialCafe and PropertyShark limited or denied automated direct access. Their claims are limited to indexed current content and/or official documentation and are labeled accordingly.
- CoStar's full product is paid/gated; this report uses its public official product/help pages and does not claim to have observed the authenticated application.
- Search-indexed snippets can be stale or incomplete. They were used only when direct access was blocked and never promoted to a live observation.
- One older Rightmove commercial URL returned HTTP 410 and is explicitly treated as stale historical evidence.
- No contact, callback, tour, alert, save, login or lead form was submitted. Thus delivery, CRM ownership and response-time behavior could not be externally verified; the lead-routing design in this report is a recommendation.
- Dynamic commute/traffic results depend on origin, time, provider and service conditions. Recommended commute behavior is a product requirement, not a claim that a tested Israeli platform already supplies it.
