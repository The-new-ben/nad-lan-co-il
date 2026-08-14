# Existing Hebrew ZOHI page audit

Page: https://nad-lan.co.il/projects/zohi-sde-dov/  
Captured in real user Chrome: 5 August 2026 at 02:52:51 Israel time  
Scope: rendered content, source integrity, buyer-facing semantics and structured data. No page, code, media or article changes were made.

## Executive verdict

The page has a substantial Hebrew article and a rich project-showroom shell, but the two layers do not operate from one fact contract. The showroom presents synthetic apartment inventory, a 12-floor building and a project price estimate. The article later says no unit-level price data was published and explicitly warns against inventing a price range. The structured data then revives the 12-floor and NIS 90,000 per sqm claims. A buyer and a search engine therefore encounter three different versions of the project on one URL.

This is not a thin-content problem. It is an evidence-governance and information-order problem.

The article contains approximately 3,935 words, one visible H1 and many buyer-oriented sections. Its H1 does not arrive until roughly 7,600 vertical pixels into the rendered page. Before it, Google and a first-time visitor meet an independence notice, a status rail, a capability menu, a generic 3D model, a demo apartment selector, an estimated-price module, an area map, a generic interior tour and lead forms. The earliest project-name heading is an H2, not the H1. This weakens the page's topic declaration even before factual conflicts are considered.

## Captured primary signals

| Element | Captured value | Assessment |
|---|---|---|
| Title | `ZOHI זוהי שדה דב - לוינשטין מבנה אלייד · תצוגת פרויקטים` | Project-led, but omits Tel Aviv and leads with partner names rather than the buyer's core decision terms |
| Meta description | Generic promise of project details, apartments and contact | Mentions apartments but not the strongest verified facts, current price status, Tel Aviv intent or a distinct buying question |
| Canonical | Self-canonical to the audited URL | Correct for this Hebrew page |
| Robots | index, follow | Indexable |
| HTML language | `he` | Correct language signal |
| Direction | `rtl` | Correct direction |
| Visible H1 count | 1 | Count is technically correct |
| Visible first project-name heading | H2 | Wrong semantic order because it precedes the H1 |
| Visible empty headings | One empty H2 | Invalid information architecture and noisy accessibility outline |
| Article length | About 23,100 characters and 3,935 words | Substantial but below the agreed 5,000-word depth standard |
| External links inside article | One `mailto:` correction/contact link | The article's source chapter contains no source URLs |
| Stated update | June 2026 | Several current claims were not revalidated against the August 2026 first-party record |
| Authorship | Site editorial system | No named researcher, fact checker or claim-level citation trail |

## What the page does well

- It has one actual H1 rather than two literal H1 elements.
- It uses a self-canonical and is indexable.
- The Hebrew article is written for a prospective buyer, not as a bare project database entry.
- The article discusses legal, financing, management-fee and contract checks that genuinely matter in an off-plan purchase.
- It exposes an independent-site statement and a correction email.
- It identifies the project as being in Sde Dov and gives the correct 230-apartment scale.
- It contains a visible FAQ section and an article-level structure that can be rebuilt into the required chapter pattern.
- The current first-party stage `בשיווק` is directionally consistent with Levinstein's marketed-project archive.

These strengths are recoverable. They should not be used to excuse unsupported inventory and price signals higher on the same page.

## Critical findings

### P0. Synthetic apartment controls look like real inventory

The showroom states:

- 12 floors
- 4 apartments to choose from
- 4 available apartments
- a 3-room, 85 sqm unit on floor 3 facing west
- a 4-room, 120 sqm unit on floor 6 facing southwest
- a 4-room, 125 sqm unit on floor 9 facing northwest
- a 5-room, 160 sqm unit on floor 12 facing west

Individual cards carry an illustration label, and a later notice says the units are demonstrations. That is not enough. The surrounding verbs and counters are transactional: choose an apartment, available, four apartments, mark the unit in the building, and send an inquiry about the selected apartment. The interface behaves like inventory even when the fine print says it is not.

No current first-party unit schedule was found. These unit facts must therefore remain demo-fixture data and must not enter any article, FAQ, schema, alt text, lead payload or buyer claim.

Buyer risk: a visitor may believe that a specific apartment, floor, orientation or size is offered.  
Search risk: structured and visible page signals may associate the project with fabricated unit-level facts.  
Required content gate: when no verified schedule exists, the public copy must say that current availability and unit-level details were not published, and no availability counter may be treated as content evidence.

### P0. The 12-floor claim conflicts with attributable project reporting

The page repeats 12 floors in the showroom summary, body text and FAQ schema. Research found:

- a 2024 planning report describing four buildings at 16 and 9 storeys;
- a January 2026 launch report describing two 15-storey towers and one 7-storey building above commerce;
- no numerical floor count in the current official ZOHI microsite text inspected in August 2026.

The page's 12-floor value matches a demo unit reaching floor 12, which suggests that a generic showroom fixture has leaked into the project facts.

Required content decision: reject 12 floors. Do not replace it with an undated current count. If the building configuration is discussed, attribute the January 2026 configuration as dated launch reporting.

### P0. The page contradicts itself on prices

High in the showroom, the page displays:

- NIS 79,200 to NIS 100,800 per sqm
- average asking price of NIS 90,000 per sqm
- labels identifying the numbers as non-binding estimates

Later, the article says that no unit-level price was provided and that a price-per-metre figure or range should not be invented. Its visible article table merely says `מחירי השקה`. FAQ schema then publishes about NIS 90,000 per sqm as an estimate.

The public page therefore contains three price positions:

1. an unexplained numerical estimate;
2. a prose instruction not to generate such a range;
3. structured data that reasserts the estimate.

No current official price list was found. A January 2026 Mako report published a launch range of NIS 70,000 to NIS 100,000 per sqm, but this is a dated report, not today's offer. It does not validate the page's 79,200 to 100,800 calculation or its NIS 90,000 average.

Required content decision: current price is not published or independently verified. The historical launch range may be used only with the publication date, source and explicit statement that it is not a current quote. No current project estimate should appear without a transparent, separately governed market methodology.

### P0. FAQ structured data does not match the visible FAQ

The page emits a four-question `FAQPage` object. It includes questions about the developer, price per sqm, floors and apartments, and how to choose an apartment through the experience.

The visible article FAQ contains nine different questions, including location, project parties, apartment count, architecture, amenities, 20/80 meaning, launch pricing, pre-contract checks and buyer fit.

This fails the basic rule that FAQ schema must represent the questions and answers visible to the user. It also puts unsupported claims into machine-readable form:

- NIS 90,000 per sqm
- 12 floors
- an apartment-selection flow that implies real unit choice

Required content gate: only visible, source-verified FAQ questions may be represented in schema, in the same language and with materially the same answers.

### P0. A planning lot is emitted as a postal street address

The `ApartmentComplex` schema uses:

`streetAddress: מגרש 110, מתחם אשכול, רובע שדה דב, תל אביב-יפו`

Lot 110 is supported as a planning-lot designation by attributable reporting. It is not a verified postal street address. The municipal lead could not be opened in Chrome, and no address assignment document was verified.

Required content rule: describe lot 110 as a planning lot. Do not mark it as `streetAddress`, write it as a navigable postal address, or imply that a buyer can use it as the final address.

## Search and semantic findings

### The H1 is technically singular but functionally late

The only H1 appears inside `.nlpf-name` within the long article container. Its rendered top is about 7,600 pixels below the page start. Before it, an H2 repeats the project name. This creates an upside-down hierarchy:

1. generic independence and experience modules;
2. an H2 project label;
3. many feature H2s;
4. lead capture;
5. the page H1;
6. the substantive buyer article.

A crawler can parse the whole document, but ordering still communicates emphasis. The first project-specific text should state the project, Tel Aviv/Sde Dov, apartments, published price status and the buying question. The current first substantive block is a disclaimer, not an overview.

### Title and H1 do not contain the full city query

Both use `ZOHI זוהי שדה דב` and partner names. They do not include `תל אביב` even though the body, breadcrumb and location block do. The agreed formula requires the project and city at the front because this is how a buyer differentiates a named project from a generic brand result.

The partner string is also factually compressed. The current official site presents Levinstein, Metropolis and Mivne, while historical lot reporting names Allied, Levinstein and Mivne and explains Metropolis's relation to Allied. A title is not the place to resolve this corporate structure. Buyer terms and city should take priority.

### The first screen is platform-first rather than query-first

The opening visible text declares that the site is independent. That statement should remain, but it should follow a concise, source-backed project overview. The current ordering asks the user to process platform status before learning the project's basic product facts.

The first modules then advertise capabilities such as model viewing, apartment choice, a window view, a design studio, a district tour and plans. Some of those capabilities are not supported by verified ZOHI unit data. This turns feature navigation into topical noise and makes the unsupported showroom claims Google's early project context.

### Generic modules dominate the raw and rendered reading order

The article is wrapped in one long `.entry-content`. The page-specific article begins only after a large common experience. That pattern makes generic interface language, demo inventory, price estimates and lead forms stronger early signals than the verified project narrative.

The content repair is architectural at the information level:

- one project-and-city H1 at the top of the substantive experience;
- a source-backed opening paragraph immediately below it;
- a compact verified-facts block;
- only then capabilities that are genuinely active for ZOHI;
- the full buyer article after the core decision data, not after misleading demos.

This audit does not authorize a template or code change. It records the required output order for the future content owner.

### Heading outline contains an empty H2 and an H2 before H1

The captured page includes one visible empty H2 and several generic showroom H2s before the H1. Empty headings harm accessibility and add no topical value. Headings should describe content sections, not act as styling hooks.

### City internal URL is not governed as a stable ASCII slug

The breadcrumb links to a percent-encoded Hebrew city path. This conflicts with the established ASCII-slug governance used for scalable multilingual internal linking. This run did not change or validate routing. The issue should be escalated to the platform owner, not silently changed during a content update.

## Factual and editorial drift

| Topic | Current page | Best evidence from this run | Required disposition |
|---|---|---|---|
| Project scale | 230 homes | Official site publishes 230 | Keep |
| Apartment mix | Vague intimate and large apartments; demo 3, 4 and 5 room units | Official current site publishes 2 to 6 rooms plus penthouses | Rewrite to the official current mix; remove demo types from content evidence |
| Floors | 12 | No current first-party count; Jan 2026 report says 15, 15 and 7 | Remove 12; use dated attribution only if needed |
| Building count | Implied single showroom building | 2024 report says four; 2026 launch says three | Do not lock a current count without first-party confirmation |
| Garden | Urban garden, no consistently governed number in early UI | Official site says about 2.8 dunams | Normalize to about 2.8 dunams |
| Ceiling height | 3 metres | Official site supports 3 metres | Keep with specification-verification language |
| Gym, yoga, lounge | Presented as project amenities | Official site supports all three | Keep |
| Pool | Stated as a project amenity | Supported by dated reports, not found in current official text | Attribute as reported/planned, or omit until first-party text confirms |
| Current price | 79,200 to 100,800 per sqm; average 90,000 | No current first-party price; Jan 2026 report gives a dated 70,000 to 100,000 launch range | Remove current estimate; date any historical range |
| Payment | 20/80 written as a live project feature | Verified only in Jan 2026 early-marketing report | Convert to dated historical term, not current offer |
| Stage | Launch/early sale in article; marketed in status rail | Levinstein currently lists `בשיווק` | Use current marketed status; date the launch history |
| Delivery | No stable visible fact in article | Jan 2026 report forecast H2 2030; no current contractual source | Mark current delivery date unpublished; optionally cite dated forecast |
| Construction | Article encourages checking status but page can imply progress | Jan 2026 report said site works began; no current verification | Do not state current construction stage |
| Project parties | Levinstein, Mivne, Allied; Metropolis as marketer | Official site presents Levinstein, Metropolis and Mivne and explains Metropolis/Allied relationship | Explain roles accurately; avoid four-name pileup |
| Revenue | About NIS 1.5bn, presented as meaningful scale | Company estimate reported by Mako in Jan 2026 | Low buyer value; date and attribute or omit |

## Source and trust audit

### The source chapter is not a source chapter

The article ends with generic categories such as project information supplied, developer publications, Metropolis publications and public planning information. It provides no direct source URLs. The only external article link captured is the site's correction email.

This prevents a buyer, editor or search system from tracing any numerical claim. It also makes later updates fragile because an editor cannot tell which claim came from which publication date.

Required source design:

1. use real links;
2. state publication dates for historical commercial terms;
3. connect claims to sources in prose, not only in an end list;
4. keep a source precedence rule;
5. record what was not published;
6. do not cite Google search pages or generic source categories.

The exact source order is locked in `00-source-ledger.md`.

### The update line does not equal freshness

The article says it was updated in June 2026, but it carries launch terms from January, an unsupported showroom price model and a floor count that conflicts with published configurations. A date alone is not evidence of review.

For a durable update process, every volatile field needs a verification date:

- price;
- availability;
- stage;
- payment terms;
- delivery;
- permit and construction;
- unit schedule;
- amenities if the current sales specification changes.

### Authorship is generic

The site identifies its editorial system and gives a correction email. That is better than anonymous content, but not enough for a high-stakes real-estate decision page. The future package should preserve a short methodology line and a visible research date. If the site has a named editorial reviewer or property researcher, that identity should be tied to the finished article. This is a governance recommendation, not permission to invent credentials.

## Structured-data inventory

Four JSON-LD blocks were captured:

1. Yoast WebPage, ImageObject, BreadcrumbList, WebSite and Organization graph.
2. Custom `ApartmentComplex` with 230 units, coordinates and a planning lot used as a postal address.
3. A second custom `BreadcrumbList`, duplicating the Yoast breadcrumb path.
4. A custom four-question `FAQPage` that does not match the visible FAQ and contains unsupported price and floor claims.

The duplicate breadcrumb is not the main problem, but it adds competing representations. The content-critical failures are the false `streetAddress`, unsupported FAQ answers and mismatch between visible and machine-readable FAQs.

Required structured-data acceptance criteria:

- every factual value must exist in the locked contract;
- every FAQ question and answer must be visible in the same language;
- no estimated price enters project schema unless the page visibly explains its source, date and non-binding method;
- a planning lot is not encoded as a postal street address;
- one coherent breadcrumb representation should describe the same hierarchy;
- translated pages must have localized visible text and localized schema without changing facts.

## Buyer-journey problems

### A buyer cannot distinguish what is real from what is demonstrative

The page uses three disclosure layers, but the operational controls still invite selection. A buyer should not need to reconcile labels such as illustration, available, selected apartment, generic building and project information.

The decision rule should be simple:

- verified building model and schedule exist: selection may be project-specific;
- they do not exist: show building-level context only and state that apartment availability has not been published.

### The page asks for a lead before resolving basic uncertainty

Lead forms appear before the article explains what is known and unknown. A buyer has not yet received a current price status, valid building configuration, delivery-status statement or source trail. The CTA should follow a compact verified-facts block and should request details rather than imply that a selected apartment is available.

### Useful legal guidance overwhelms project-specific evidence

The article's legal checklists are valuable, but they occupy substantial space while current project facts remain weakly sourced. A 5,000-word article should not become longer by repeating generic due-diligence advice. Additional depth should come from:

- verified location and planning context;
- product and design distinctions;
- current versus historical commercial information;
- role clarity among the project parties;
- practical buyer questions tied to this project;
- culturally relevant remote-purchase, family and investment concerns without unsupported promises.

## Recommended content disposition

### Keep and strengthen

- 230 apartments.
- Sde Dov and Tel Aviv location.
- current official 2 to 6 room mix plus penthouses.
- 3 metre published ceiling language.
- about 2.8 dunam private urban garden.
- shared workspaces, gym, yoga and residents' lounge.
- Galor Fishbein and Tal Goldschmidt Fish credits.
- buyer checks for contract, specification, management fees, financing and tax.
- independent-site statement, placed after the opening overview.

### Rewrite with date and attribution

- launch price range;
- 20/80 payment structure;
- expected occupancy in the second half of 2030;
- works having begun;
- expected revenue;
- reported three-building launch configuration;
- pool and rooftop-level description.

### Remove from the factual layer

- 12 floors;
- four available apartments;
- all demo apartment sizes, floors and directions as project facts;
- NIS 79,200 to NIS 100,800 per sqm;
- NIS 90,000 average asking price;
- lot 110 as a street address;
- current presale wording;
- guaranteed sea view or view claims;
- generic source categories without links.

### State as unpublished

- current unit price list;
- current inventory;
- contractual delivery date;
- current permit status;
- current construction stage;
- current numerical building configuration unless a first-party source is obtained.

## Acceptance gates for the future language content

The English, French, Russian and Arabic packages should fail review if any of these occurs:

- a factual value differs between languages;
- 12 floors reappears;
- a demo unit is described as available inventory;
- current price is inferred from the showroom estimate;
- the January 2026 20/80 term becomes present tense;
- the reported 2030 forecast becomes a promised delivery date;
- lot 110 is written as a street address;
- a current permit or construction stage is asserted without a new direct source;
- the four-building 2024 design is mixed with the three-building 2026 report;
- FAQ schema differs from the visible FAQ;
- sources are generic labels rather than direct links;
- the title or H1 omits Tel Aviv;
- the opening project overview is displaced by internal platform or compliance language.

## Priority order

1. Remove unsupported inventory, floor and price facts from the content contract.
2. Make visible FAQ and schema identical and source-safe.
3. Treat lot 110 as a planning designation.
4. Put the project, city and verified overview before generic experience modules in the content hierarchy.
5. Rebuild the source chapter with direct links and dated attribution.
6. Normalize the party roles and the current official apartment mix.
7. Separate current facts from January 2026 launch history.
8. Expand future articles to the agreed depth through project-specific research, not generic repetition.

This audit intentionally stops at diagnosis and content requirements. It does not authorize edits to the Hebrew page, shared templates, showroom engines, schema emitters or any project media.
