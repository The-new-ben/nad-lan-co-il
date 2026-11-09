# Tools for "the person who wakes up in the morning looking for an apartment" (proposal, 9.11.2026)

The research says what this person types: a stage (על הנייר / לאכלוס מיידי), a budget (עד 1.2 / 2 מיליון), a city, "במבצע", "20 80", and sometimes "לידי".
No competitor turns those words into answers: they offer filters and free-text badges. The tools below do.

Data held today (repo paths under `plugins/nadlan-config/`):
- `data/projects-market.json`: 566 projects on the market (read 25.10.2026). 348 with a price, 483 with rooms, 115 with a delivery date, 64 with a deal text. **No coordinates; only 10 linked to our project pages.**
- Project posts (about 1,087; 1,019 in the catalog), with meta for city, address, neighbourhood, developer, units, floors, buildings, type, status, completion year, architect; the near-me finder uses lat/lng where posts have it.
- `assets/instruments/data/`: `value.json` (Tax Authority medians by rooms, 24 cities), `value-series.json`, `garden.json`, `prices-hub.json`, `rent.json` (72 cities by rooms), `cbs-200010.json` (residential construction input index, to 2026-09), `cbs-120010.json` (CPI), `boi-rate.json`, `boi-mortgage.json`, `mready.json`, `nrm.json`, `ptax.json`, `cost.json`, `orechdin.json`, `bedek.json`, `pinkas-meta.json` (contractor register), `dira.json` and `dira-round.json` (government discount program: projects, units, price per m², registrations, winners), `buying.json`, `hazards.json` + `hazards-lines.json`, `sdplan.json`, `urcity.json`, `renewal-track.json`.

Legend: **Have** = data and logic exist; **Partly** = data exists but needs a field or a join; **Need** = new data.

| # | Tool | What it answers | Data it needs | Do we have it |
|---|---|---|---|---|
| 1 | **Immediate-occupancy finder** ("לאכלוס מיידי עכשיו") | Which projects I can move into within 0-6 months, by city and budget, with the developer's delivery note | stage = immediate / near_occupancy, delivery month, price from, rooms, city, check date | **Partly.** 67 immediate + 18 near-occupancy rows; delivery on 115 rows. Need a check date per row and a link to each project page |
| 2 | **Deals finder** ("במבצע", "20/80", "ללא הצמדה") | Which projects run a deal now, grouped by deal type, with the source and date | deal type (payment split, indexation waiver, deferral, gift, price cut), amount or share, expiry, source URL, check date | **Partly.** 64 rows of free-text deals. Need a normalised deal type and an expiry field |
| 3 | **What the deal is worth in shekels** | "20/80 without indexation" or "900K deferred for ten years" turned into a present value against a normal schedule | contract price, payment schedule, construction input index trend, Bank of Israel rate, mortgage rates | **Have.** `cbs-200010`, `boi-rate`, `boi-mortgage`; extends the existing indexation calculator. Answers the SERP that today shows only news and lawyers |
| 4 | **Below-market check** ("האם המחיר גבוה?") | Starting price of a project against what same-size flats sold for in the city and street | price from with its room count, city and street medians by rooms | **Partly.** `value.json` (24 cities, by rooms) and the street ₪/m² already on catalog cards; the "from" flat's rooms and size are missing on most rows (₪/m² on only 6) |
| 5 | **Government-priced projects next to market projects** | Where the state sells cheaper (מחיר מטרה, מחיר מופחת) and where the "flats without a lottery" are | program projects, price per m², units, lottery status, the gov.il list of flats without a lottery | **Partly.** `dira.json` and `dira-round.json`; the gov.il "דירות למכירה ללא הגרלה" list is not yet read. Clearly labelled, linked to `/dira-behanacha/` |
| 6 | **Budget finder** ("מה אפשר לקנות ב־2 מיליון") | Projects whose starting price fits my budget, and the budget my income allows | price from, city, rooms; income, equity, rates | **Have.** `projects-market.json` + the existing affordability tool (`mready`, `nrm`, `boi-mortgage`) |
| 7 | **Near-me finder** ("קרוב אליי") | Projects around me with walking or driving minutes | coordinates for every project, the visitor's location (on request) | **Partly.** The finder exists for posts with lat/lng; the 566 market rows have **no coordinates**. Need geocoding by address or neighbourhood |
| 8 | **New-project alert** | An email or WhatsApp-style notice when a project opens in my city and budget | a daily diff of the market file, subscriber preferences, mail sending | **Partly.** Mail stack exists (owner mails, price-alert work); need dated snapshots of `projects-market.json` |
| 9 | **"About to be occupied" alert** | Tell me when a project I follow moves to near or immediate occupancy | stage history per project | **Need.** Stage history does not exist; start keeping snapshots |
| 10 | **Price-change alert** | Tell me when a starting price drops or a deal appears | price and deal history | **Need.** Same snapshots as 8 and 9 |
| 11 | **Compare 2-3 projects** | One table: price from, rooms, stage, delivery, deal, developer, units, street deal price, hazards nearby | market rows, project posts, `value`, `hazards` | **Partly.** All parts exist; needs the market-to-post link (10 of 566 today) and coordinates for hazards |
| 12 | **Payment-schedule check** | Upload or type the developer's schedule; see what indexation adds and when money is due | schedule, construction input index, CPI | **Have.** Existing indexation and total-cost calculators; extend to two schedules side by side |
| 13 | **"Ready or on paper?" decision tool** | What waiting costs (rent paid meanwhile, indexation) against the premium of a ready flat | rent by city and rooms, input index trend, price from by stage | **Have.** `rent.json`, `cbs-200010`, market rows by stage |
| 14 | **Developer and contractor check** | Is the contractor registered, in which class, how many projects we hold for this developer | contractor register, developer-to-register mapping | **Partly.** `pinkas-meta.json` and the existing check tool; need the mapping from developer names to register entries |
| 15 | **Delivery-delay compensation** | How much the developer owes if keys are late | contract date, delivery date, rent | **Have** (existing tool) |
| 16 | **Purchase tax and the full cost** | Tax, lawyer, mortgage fees, upgrades | `ptax`, `cost`, `orechdin` | **Have** (existing tools) |
| 17 | **Warranty clock** | What the developer must fix and until when | `bedek` | **Have** (existing tool) |
| 18 | **Market this month** (a dated box) | Unsold new flats, months of supply, sales, price index, the month's developer campaigns | CBS new-dwellings stock series, `prices-hub`, news | **Partly.** Price index is in `prices-hub`; the CBS unsold-stock series is quoted on the Tel Aviv page but not stored as data. Need it as a data file |
| 19 | **Investor lens** | Gross rent yield of a project's starting price | price from by rooms, rent by city and rooms | **Have.** `rent.json` + market rows (with rooms on 483) |
| 20 | **Project stage timeline** | Where the project stands from permit to keys, and typical time left | stage per project, typical durations | **Partly.** `buying.json` stages and `renewal-track.json`; per-project dates are missing |
| 21 | **Around the project** | Antennas, fuel stations, soil, planned works near the address | coordinates | **Partly.** `hazards.json`, `sdplan.json`; blocked by missing coordinates on market rows |

## The three data jobs that unlock most tools
1. **Link every market row to its project page** (10 of 566 today). Unlocks 1, 2, 4, 11, 20 and the cards on the hub.
2. **Add coordinates to the 566 market rows** (address or neighbourhood geocoding). Unlocks 7, 11, 21 and the map.
3. **Keep dated snapshots of `projects-market.json`** and add a check date and a normalised deal type per row. Unlocks 2, 8, 9, 10 and lets the page print honest "נכון ל־" dates.

## Order for the first release (most searched, least new data)
1. The stage + budget + city filter bar with live counts (the answer paragraph comes from the same counts).
2. Immediate-occupancy finder and deals finder (tools 1 and 2), each with a dated source line.
3. Deal value calculator (tool 3), which no ranking page has.
4. Budget finder (tool 6) joined to the existing affordability tool.
5. Near-me (tool 7) once coordinates exist; alerts (8-10) once snapshots exist.
