# Limits: what could not be opened or measured

Written on 10.11.2026. Read this file before quoting any number from `features.csv`, `teardown.md`, `gaps.md` or `ours-only.md`.

## 1. What the coverage figure can and cannot prove

- **An enumerated list, not the whole world.**
  - The list has 221 atomic features from 49 products.
  - 'Present on our page' covers only those rows.
  - A feature that exists in a product we did not read, behind a sign-in, or in a native app is not in the list.
- **Quality of the evidence.** Every row records its evidence class. Rows marked 'claimed', 'search' or 'prior' are weaker than 'live':

  | Class | Rows |
  |---|---|
  | live | 156 |
  | press | 23 |
  | search | 16 |
  | claimed | 12 |
  | help | 9 |
  | prior | 5 |

- **Buyer value is a judgement.** The 1-5 score is the judgement of a buyer of a Kikar apartment; it was not measured. The weighted coverage (53.2%) inherits that judgement. The unweighted figure (47.4%: present = 1, partial = 0.5) does not.
- **Present / partial / absent is a binary-ish call** on a single page state.
  - 'Partial' means the job is done in part, or in another form; for example, a 360 of a model apartment instead of the actual unit.
  - The CSV says exactly what was seen in each case.
- **Merging rows was a judgement too.** 63 near-duplicate raw rows were merged into others. Every merged source is kept in `more_evidence` and `raw_ids`.

## 2. Our page: how it was checked and what was not

- **Release and tool:** 1.72.630, checked in the built-in browser in a tab of its own (opened, then closed at the end).
  - **Desktop:** the pane's 1024x768 viewport, not 1440x900.
  - **Phone:** 375x812 with Android emulation.
- **The pane was hidden during the run, so `requestAnimationFrame` was paused (tested: no frame in 2 s).** As a result:
  - **Stale canvas shots:** screenshots of the 3D canvas sometimes showed an earlier state.
  - **Basket sheet on the phone:** the open animation never ran. The `.nlbk__sheet` element (375x747) and its scrim were confirmed in the DOM, but the open state was not seen on screen.
  - **Desktop basket:** it did open (`.nlbk is-on`) and its text was read.
  - **Visual quality:** none of the visual quality of the 3D world on a phone was judged.
- **Real taps on the phone:** the south-west unit on the key plan (worked) and the basket button. Everything else on the phone was verified by DOM reads of the same responsive page.
- **Nothing was submitted.** The video-call form, the price-updates popup and the basket's WhatsApp send were not used, so these were not tested:
  - booking confirmation
  - WhatsApp delivery
  - cancellation
  - the languages the rep speaks
- **The price-updates popup** ('המחירים באזור זה במגמת שינוי') appeared by itself and was closed with 'לא עכשיו'.
- **Map pins:** one tap on a Mapbox pin missed, so the pin popups and list-to-pin sync were not confirmed. The page text says 'לחצו על כל סימון לקבלת פרטים'.
- **Not opened one by one:** the spa and car-park 360 scenes, and the 'המגדל מבחוץ' mode. Their buttons are present.
- **Other languages:** the en / fr / ru / ar pages were checked from their HTML only, not clicked through. Each has the 3D world, 6 videos, the FAQPage schema, WhatsApp links and video-call text. The fr / ru / ar pages carry English captions, not captions in their own language.
- **Chat widget:** a Tawk chat iframe is on the page at 0x0 px. It was treated as not visible and was not opened.
- **Real photos:** aerial photos made by other sessions exist in a scratch folder, but they are not on the live page. The page was judged as live.

## 3. Products that blocked us, or that we could not verify

| Product | What happened (10.11.2026 unless noted) | What the rows rest on |
|---|---|---|
| Zillow listing and building pages | 403 bot check in the built-in browser; WebFetch 403 on the news, 3D Home and help pages | Zillow press releases (including the 14.7.2025 release PDF), zillow.help, and the 9.11.2026 DOM read |
| Zillow climate scores | Press says they were removed in late November 2025 | No row |
| Realtor.com | Refused by the browser ('not allowed due to safety restrictions') and by WebFetch | Press, search and the 9.11.2026 DOM read. 'RealCost' has no public source. |
| Homes.com, Apartments.com, Trulia | 403 Access Denied | Search snippets only |
| NewHomeSource, KB Home | 403 / Cloudflare challenge (not attempted) | Zonda product page, search, and the 9.11.2026 read |
| Redfin | Opened live. The 3D sun canvas did not render (hidden pane), the commute module was not shown to a signed-out visitor, and tour checkout was not opened | Live labels |
| Toll Brothers | 'See Personalization Options' opens a new tab, which the pane blocked | The label only |
| Compass Collections | Needs sign-in | Press release of 28.10.2024 |
| Domain | 403 (Akamai) on the site and help centre | Search snippets |
| realestate.com.au | Refused by the browser; WebFetch 429 | Press and search |
| Idealista | 403 | Its news pages and search |
| Madlan resale listings | Robot puzzle (not solved) | Project pages opened live |
| Yad2 / Yad1 | An automatic Radware check cleared by itself (no puzzle was solved). The 'נכסים שנמכרו באזור' table stayed an empty skeleton, and plans per type were not on the two projects opened | Live labels |
| ImmoScout24 | An interstitial cleared by itself. Plus-only values were blurred | Live labels |
| Zoopla | Flood, crime and planning values need sign-in | Labels only |
| Rightmove | Stations, Schools and broadband values load on click; no EPC graph was seen | Labels and headings |
| Bayut | Empty page with 375 px emulation; desktop read fine | Desktop only; mobile pattern not verified |
| OnTheMarket | Help centre only | Help page |
| Homeless | Not opened; no lead found that it leads on a unit-page feature | No row |
| Expedia, Vrbo property pages | HTTP 429 'Bot or Not?' wall | Search result pages and press |
| Airbnb | At 375 px one listing stopped at an app interstitial. The listing read had no Guest favourite, Rare find or translation label | Press and help for those three |
| Waldorf Astoria Residences Miami | The WebGL view stayed on LOADING; the view page rendered only its title | DOM labels; the day / night view rests on the 2.10.2026 screenshot (prior) |
| Emaar | Text fetch only. 'Sales Video Call' (seen 2.10) was not in today's text; the VR hub was not opened | Text |
| Maverick Frame, REALS, BMBY 3D, Volume Vision, Shadowmap, Floorfy | Demos did not render, or none exist publicly | Vendor claims ('claimed') |
| Matterport | The demo is a construction site | Defurnish, Tags, VR and Property Intelligence come from Matterport's blog and docs |
| Google Immersive View, Apple Look Around | Help page 404; Apple guide not fetched | Google blog (2023) and an Apple search snippet |
| Hotels.com compare | Fetch timed out | Search snippet |
| Propvr, Realiz3D, Spacewise, Binyan, Pikcells, Omniyat, Sobha, DAMAC, One Thousand Museum, Battersea, Una | No official page showed a 3D unit picker, sun study or per-unit payment calculator | No rows, except Una (2.10 read) and a payment-plan row for Sobha, Omniyat and DAMAC (search) |
| Hotel and rental price alerts | Not verified on any of the four booking sites | Expedia Price Tracking rests on a search snippet |

**Full raw logs:** the three passes logged every URL. The entries are folded into the table above, and the merged `more_evidence` column keeps every source URL.

## 4. Rules followed

- **Browser use:** cookies were declined; no CAPTCHA or puzzle was solved; nothing was signed into; no personal data was typed; no form was submitted; no tour or viewing was requested.
- **Copying:** no competitor text or image was copied into the site. Only short UI labels are quoted as evidence.
- **Scope:** no website was changed and nothing was written to Linear or Notion. The only files written are the five in this folder.
