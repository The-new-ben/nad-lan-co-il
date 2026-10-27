# Kochav HaTzafon mini penthouse: benchmark of the world's best listing pages

Read on 27 Oct 2026, 11:43 to 12:12 UTC. Local, read-only research: public pages only, nothing clicked except gallery or floor-plan tabs, no forms, no logins, no captchas.

Files in this folder:

- `board-390.png`, `board-1280.png`: our page next to the 4 best, with the measured price boxed.
- `board-plans.png`: 6 floor-plan presentations.
- `shots/NN-name-390.png` and `-1280.png`: the first screen at each width. Consent, survey and sign-in overlays are hidden with local CSS only.
- `shots/raw/*-raw.jpg`: the same first screen as a first-time visitor sees it, overlays included.
- `shots/full/*-full.jpg`: full-page reference captures.
- `shots/plans/`: floor-plan captures.
- `shots/before-change-1143utc/`: our Hebrew page before a live change that shipped during this research (see section 2).
- `data/benchmark-measurements.json`: every raw measurement.
- `data/keywords-2026-10-27.csv`, `data/keyword-suggestions-2026-10-27.json`, `data/serp-top20-2026-10-27.json`, `data/gsc-listing-impressions-by-day.csv`.
- `tools/probe.py`: the measuring script. `tools/reshoot.py` and `tools/declutter.js` make the clean shots, `tools/board.py` builds the boards, and `tools/fp_shoot.py` and `tools/jsclick.py` capture the plans.

## Method

- **Browser and viewports.** Playwright with the installed Chrome 141, headless, `wait_until="load"` plus 6 to 7 s.
  - Phone: 390x844 viewport, iPhone user agent, touch, DPR 2.
  - Desktop: 1280x800, DPR 1.
- **Measures.** For every page and both widths a DOM probe records:
  - the asking-price element: y in CSS px from the page top, font size and weight, its context, and inline prices inside sentences;
  - the visible H1 and any hidden H1;
  - the largest-font text in the first screen;
  - the facts line (rooms, size, floor) and the hero media with its share of the first screen;
  - the first image, video and iframe positions, and the photo counter;
  - floor-plan, mortgage, tour and map elements;
  - CTA buttons, tel/WhatsApp links, forms, and fixed or sticky bars.
- **Second pass.** The page is scrolled once to trigger lazy content, then measured again.
- **Above the fold** means the price's top edge is at y < 844 on the phone or y < 800 on the desktop.
- **Blocked or replaced pages** are recorded as such and never forced.
  - Madlan returned 403 "you are a robot" (PerimeterX-type page). Screenshots: `shots/14-madlan-BLOCKED-*`.
  - Yad2 showed a Radware captcha on some phone loads:
    - item `3dczaaes` was blocked on the phone twice;
    - item `5py5qlqi` worked on the first load and was blocked on a later reload.
  - The Sotheby's Central Park Tower penthouse URL (`/180-l-85361-3947296/`) now returns "Page Not Found". It was replaced by 39 Crosby St PHN.
  - The Property Finder Four Seasons DIFC penthouse is "no longer available". It was replaced by AVA at Palm Jumeirah by Omniyat.
  - Engel & Völkers has no live Israel listing site: `engelvoelkers.com/il/...` returns 404. Barnes Israel took that slot.

## 1. The pages

| # | Page | URL | Asking price | Read (UTC) |
|---|---|---|---|---|
| 01 | Sotheby's International Realty, 39 Crosby St PHN, SoHo NYC (penthouse, 5 bd) | https://www.sothebysrealty.com/nyc/eng/sales/detail/709-l-1178-67s98b/39-crosby-street-phn-soho-new-york-ny-10013 | $25,000,000 | 11:48 |
| 02 | Compass, 432 Park Ave PH88, NYC (full-floor penthouse) | https://www.compass.com/homedetails/432-Park-Ave-Unit-PH88-Manhattan-NY-10022/1OX76E_pid/ | $88,500,000 | 11:44 |
| 03 | Douglas Elliman, 43 W 64th St PH10B, NYC (duplex penthouse + garden) | https://www.elliman.com/listing/43-w-64th-st-ph10b-new-york-ny-10023/32472947 | $13,995,000 | 11:44 |
| 04 | Knight Frank, The Penthouse, One Five Fields Square, Chelsea Barracks, London | https://www.knightfrank.co.uk/properties/residential/for-sale/the-penthouse-one-five-fields-square-chelsea-barracks-belgravia-london-sw1w-8bw/prd012606919 | £48,000,000 | 11:44 |
| 05 | Savills, Orla by Dorchester Collection (Omniyat) super penthouse, Palm Jumeirah (branded residence) | https://search.savills.com/property-detail/uaegyrb33887s | AED 45,000,000 | 11:44 |
| 06 | Property Finder (Dubai's top portal), AVA at Palm Jumeirah by Omniyat, 5BR penthouse | https://www.propertyfinder.ae/en/plp/buy/penthouse-for-sale-dubai-palm-jumeirah-ava-at-palm-jumeirah-by-omniyat-160111302.html | AED 400,000,000 | 11:48 |
| 07 | Sotheby's (Israel SIR on the global site), duplex penthouse with rooftop infinity pool, Tel Aviv | https://www.sothebysrealty.com/eng/sales/detail/180-l-86348-w3g3pv/exceptional-duplex-penthouse-with-rooftop-infinity-pool-tel-aviv-il | $29,506,177 / ₪91,000,000 | 11:45 |
| 08 | Barnes Israel, 203 m² penthouse, Nordau Blvd, Old North | https://www.barnes-israel.com/en/for-sale/tel-aviv-yafo/ref-6706358.html | ₪34,800,000 | 11:45 |
| 09 | Yad2, duplex, Levi Eshkol 2, **Kochav HaTzafon** (direct competitor, same street, Be'eri Nadlan, exclusive) | https://www.yad2.co.il/realestate/item/tel-aviv-area/5py5qlqi | ₪20,000,000 | 11:45 |
| 10 | Yad2, rooftop penthouse, Kineret St, Neve Tzedek (platinum ad) | https://www.yad2.co.il/realestate/item/tel-aviv-area/3dczaaes | ₪19,200,000 | 11:48 (phone blocked) |
| 11 | Homeless, 4-room penthouse, Bograshov, Old North | https://www.homeless.co.il/sale/viewad,252357.aspx | ₪12,750,000 | 11:45 |
| 12 | Israel Sotheby's own site, "פנטהאוז מודרני יוקרתי בכוכב הצפון" (**ranks #9 for "דירות למכירה בכוכב הצפון"**) | https://www.israelsir.co.il/property/פנטהאוז-מודרני-יוקרתי-בכוכב-הצפון/ | ₪12,250,000 | 11:57 |
| 13 | Domestic TLV, "למכירה מיני פנטהאוז מהמם בצפון הישן" (**ranks #7 for "מיני פנטהאוז"**) | https://www.domestictlv.co.il/estate/מיני-פנטהאוז-צפון-הישן-תל-אביב/ | ₪10,600,000 | 11:57 |
| 14 | Madlan, Tel Aviv penthouses | https://www.madlan.co.il/penthouses-for-sale/תל-אביב-יפו-ישראל | (blocked, 403) | 11:45 |
| 00 | **Ours (HE)** | https://nad-lan.co.il/properties/kochav-hatzafon-new-mini-penthouse-for-sale/ | ₪18,000,000 | 11:43 and 11:52 |
| 00 | **Ours (EN twin)** | https://nad-lan.co.il/en/brokers/meital-katzir/kochav-hatzafon-new-mini-penthouse-for-sale/ | NIS 18,000,000 | 11:52 |

## 2. First-screen measurements

y is in CSS px from the top of the page. The phone fold is 844 and the desktop fold is 800. Font sizes are computed CSS px.

| # | Price y / size, phone | Price y / size, desktop | Facts line next to price | Visible H1 (what it says) | Hero media (share of first screen) |
|---|---|---|---|---|---|
| 01 Sotheby's NYC | **682 / 22** | 722 / **14** (big copy 22px at 1104) | 5 bd, 5+2 ba, 5,607 sq ft (761 / 722) | address "39 Crosby Street, PHN" | photo carousel with **video play button**, 1/24 (31% / 34%) |
| 02 Compass | **438 / 28** | **626 / 28** | 4 beds 7 baths 8,200 sqft (480 / 668) | address | photo with **Floor Plan + Virtual Tour chips**; desktop collage 1+4 (40% / 27%) |
| 03 Elliman | **529 / 20** | 997 / 40 (below fold) | 4 BR, 4.5 BA, approx 4,002 SF (614 / 1126) | address "43 W 64TH ST PH10B" | full-bleed photo with **Photos (48) / Floor plan / Map** buttons (33% / **82%**) |
| 04 Knight Frank | 891 / 22 (below fold) | **440 / 24** | 6,911 sq ft (1801 / 1639) | full address, serif 30-38px | photo carousel 1/14 (72% / 38%) |
| 05 Savills | **521 / 28** | 834 / 38 (below fold) | 11,503 sq ft (726 / 1008) | development name | full-bleed photo with Gallery / Map / Street view buttons (29% / **84%**) |
| 06 Property Finder | **271 / 19** | **627 / 32** | 5 beds, size (495 / 870) | "Iconic 5BR Penthouse \| Palm Jumeirah" (low on page, 1355) | collage 1/26 (35%), survey pop-up over the first screen |
| 07 Sotheby's Israel | **539 / 22** (USD + ₪) | 703 / **14** (22px copy at 1010) | 6 bd, 6+1 ba, 6,458 sq ft (642 / 703) | "Tel Aviv, Israel" | **video play button** on hero, 1/12 (31% / 40%) |
| 08 Barnes Israel | **202 / 22** | **101 / 22** (top-right, next to H1) | 203 m², Old North (300 / 209) | "TEL AVIV-YAFO, 203 M² PENTHOUSE FOR SALE" | collage 1+4, "5 photos" (22% / 21%) |
| 09 Yad2 Kochav | **503 / 24** | **606 / 32** | 6 rooms, size, floor (744 / 842) | street "שדרות לוי אשכול 2" | collage 1/15 (31% / 34%) |
| 10 Yad2 Neve Tzedek | blocked (captcha) | **606 / 32** | 5 rooms (842) | "כנרת" | collage, 4 photos (34%) |
| 11 Homeless | **544 / 28** | **238 / 32** (next to H1) | 4 rooms, floor 5, 174 m² (610) | "פנטהאוז 4 חדרים למכירה בתל אביב יפו, בוגרשוב, צפון הישן" | photo + thumbnails (33% / 32%) |
| 12 israelsir.co.il | 1232 / 20 (below fold) | 1314 / 24 (below fold) | 174 m², duplex (1134 / 1170) | "פנטהאוז מודרני יוקרתי בכוכב הצפון" | full-width slider (77%) |
| 13 Domestic TLV | **561 / 18** | **797 / 18** | rooms 4, floor 4, 163 m² (831 / 977) | "למכירה מיני פנטהאוז מהמם בצפון הישן תל אביב" | single photo + map (23% / 25%) |
| **00 ours HE, 11:43** | price only **inside the lead sentence**: 546 / 16 (block at 2280 / 30) | inside sentence 625 / 22 (block at 1831 / 38) | none in first screen | **H1 hidden (1x1 px)**; visible headline is an H2 | 3D walk iframe (14%) / photo (16%) |
| **00 ours HE, 11:52 (v1.72.537)** | **669 / 32** + ≈$/€ 14px | **452 / 44** | 5 rooms, ~197 m², ~80 m² terraces, floor 11/12, by Yarkon Park (791, partly under the WhatsApp pill / 557) | **H1 still hidden (1x1 px)**; visible headline is an H2 (24-38px) | photo card 1/6 (22% / 26%) |
| 00 ours EN, 11:52 | 618 / 32 | 483 / 44 | 740 / 588 | visible H1 "New Mini Penthouse with 80 sqm of Terraces, Kochav HaTzafon" | photo card 1/6 (25%) |

**Live change during the research.** Between 11:43 and 11:50 UTC our Hebrew page changed: live health reported `nadlan-config 1.72.537` at 11:52 and still at 12:12. The price block, the facts row and the CTAs moved into the first screen. The before state is kept in `shots/before-change-1143utc/`. Every "ours" number below is the 11:52 state unless marked.

### Contact, media, plan and tools

| # | Contact on the first screen, phone | Contact on the first screen, desktop | Video | Floor plan | Photos | Tools near the price | Trust items |
|---|---|---|---|---|---|---|---|
| 01 | sticky bottom bar "Contact Agent" | "Contact Agent" (711) + 2 named agents with "Send message" | **on the hero** | **"Floor Plan" button at 445 on the phone**; on desktop the plan is the last gallery slide (23/23) | 21 photos + video + plan | CC and taxes per month | "Sotheby's International Realty® Listing", "New listing" |
| 02 | **sticky bar: Contact + "Request a tour as early as today 10:30"** | sticky agent card (photo, name, phone) + "Request a tour" | YouTube at 1764 / 2615; Virtual Tour chip on hero | **chip on the hero**, opens a full-screen tab: architect plan with room sizes + alternate plan | 17 | Est. $581,684/mo + "Get pre-approved", $/sq ft, common charges, taxes | "Listed by Compass", "New construction", building info |
| 03 | none sticky; agent photos from 718 | none in the first screen | none | **"Floor plan" on the hero (desktop)**; 2 lifestyle plans, current + alternate layout | 48 | "Estimate my mortgage", maintenance, tax | "Douglas Elliman Exclusive", licensed agents |
| 04 | sticky "Make an enquiry" | "Contact agent" at 1019 | none | PDF "Floorplan" link at 2030 / 1766: a 35-page brochure | 14 | Stamp-duty calculator (6009) | brand, "New Home" badge, brochure |
| 05 | sticky "Request details" + WhatsApp + chat bubble | agent card (name) at 725 | none | none | 13 | GBP conversion, stamp-duty calculator | "Price inclusive of agency fees" |
| 06 | (bottom taken by a sign-in prompt) | Call + WhatsApp at 808 | none | none | 26 | "Own from AED 1,439,567/month", price vs area average | "Verified", "SuperAgent", "Responds within 5 minutes" |
| 07 | sticky "Contact Agent" | "Contact Agent" in the strip | **on the hero** | none | 10 + video | USD + ₪ | Sotheby's listing banner |
| 08 | sticky icon bar (list, map, mail, phone) | sticky agent card "presented by Marc Lugassy" + phone | none | none | 5 | none | named agent |
| 09 | WhatsApp + "leave details" at 792 (not sticky) | at 879 (below fold) | none | none | 15 | **monthly payment under the price** (₪50,824) | "בלעדיות", shelter distance 450 m, broker licence no. |
| 11 | sticky "WhatsApp" + "show phone" | none | none | none | ~12 | none | date posted |
| 12 | floating "Call now" | header "צור קשר" | none | none | slider | ₪ + $ | Sotheby's brand |
| 13 | floating WhatsApp | contact form at 641 | none | none | 7 | none | office phone in header |
| **00 ours** | floating WhatsApp pill "לקבלת מחירים, תוכניות והטבות" at 716 (**covers the facts row**); "תיאום סיור פרטי" button at 1035 (below fold) | WhatsApp pill 726 + "תיאום סיור פרטי" / "חיוג למיטל" at 763 | film at **2480 phone / 1462 desktop** | **none on the page** | **6 in the hero gallery** (1/6); ~24 images on the page | ≈$ ≈€, price per m² (built / with balcony / weighted), calculator link at 1665 | "בלעדיות · מיטל קציר" as text, "צולם בדירה" tag on photos |

Page length on the phone: ours is 31,783 px, about 38 screens. The median of the benchmark pages that scroll normally is about 7,900 px.

## 3. What the numbers say (13 measured pages; Madlan blocked)

1. **Price on the first screen, as its own element.**
   - Phone: 10 of 12 (only Knight Frank 891 and israelsir.co.il 1232 are lower).
   - Desktop: 10 of 13 (Elliman 997, Savills 834 and israelsir.co.il 1314 are lower).
   - Median position: phone y=534, desktop y=627.
   - Median size: phone 22px, desktop 28px. Range: phone 18 to 28, desktop 14 to 44.
   - No page puts its price only inside a sentence. Ours did until 11:43.
2. **A one-line facts strip glued to the price** (rooms or beds and baths, size, sometimes floor): 12 of 13. The exception is Knight Frank, which shows only size and lower down.
3. **Media first, with doors.** Every page opens on a photo, filling 21% to 84% of the first screen. Galleries show a counter (1/14, 1/17, 1/24, "48 photos"; median 14).
   - The best put buttons on the media itself: Photos / Floor plan / Video / Virtual tour / Map / Street view (Compass, Sotheby's, Elliman, Savills).
   - Video on the hero: 2 of 13, both Sotheby's.
4. **Contact one tap away.**
   - Sticky or floating contact on the phone: 9 of 12.
   - Two-button bars (Compass "Contact" + "Request a tour", Homeless "WhatsApp" + "phone") beat single buttons.
   - A named agent (with a photo on most) inside the first screen: 5 of 13 (Compass, Savills, Barnes and Property Finder on desktop; Elliman on the phone).
5. **Money and trust context next to the price.**
   - Monthly payment or a mortgage link: 4 (Compass, Elliman, Yad2, Property Finder).
   - Second currency: 3 (Sotheby's Israel, Savills, ours).
   - Charges and taxes: 3 NYC pages.
   - Exclusivity or brand badges on the first screen: most pages ("Listed by Compass", "Douglas Elliman Exclusive", "Sotheby's International Realty® Listing", "בלעדיות").
6. **Floor plans: the gap nobody in Israel fills.**
   - A plan one tap from the first screen: 3 of 13 (Compass both widths, Sotheby's NYC on the phone, Elliman on the desktop).
   - A plan anywhere: 4 of 13, all international.
   - **0 of the 6 Israeli pages** show any plan.
7. **The H1 is the identity line.**
   - International pages use the address ("432 Park Avenue, Unit PH88").
   - Israeli pages that rank use type + rooms + neighbourhood ("פנטהאוז מודרני יוקרתי בכוכב הצפון", "למכירה מיני פנטהאוז מהמם בצפון הישן תל אביב").
   - Every page shows a visible H1 that names the property (Savills also marks two side headings as H1 on desktop). Ours hides its H1 (1x1 px) and shows the headline as an H2.

## 4. How the best turn an architect's plan into a luxury visual

Captures are in `shots/plans/` and on `board-plans.png`.

| Example | What it is | What makes it feel expensive | Dimensions |
|---|---|---|---|
| Knight Frank / Chelsea Barracks, One Five Fields Square penthouse brochure (the "Floorplan" link on the listing is a 35-page brochure, pp. 2, 23, 24) | Developer-grade lifestyle plan | Warm-grey slab with graphite walls. Every room furnished at scale. Terraces drawn as decking with planters and outdoor dining. A sunrise and sunset dial, a key plan of the floor in the building, a serif title "THE PENTHOUSE \| RESIDENCE 29". An "ARRANGEMENT" page lists the spaces and gives only two numbers: internal 642.1 m², external 282 m². | **No dimension lines on the drawing.** Room sizes sit in a small separate table under it. Disclaimer: "Not to scale and illustrative, by way of example, only … All items illustrated … including … areas, measurements or distances shown are approximate and subject to change." |
| Douglas Elliman, 43 W 64th PH10B (2 images, 1920x1080) | Broker lifestyle 2D plan | Solid black walls, light furniture symbols. **The garden and terrace are drawn in colour** (green lawn, deck, outdoor dining and lounge), so the outdoor space sells itself. Two versions, "Current Layout" and "Alternate Layout". | Room sizes in feet on each room |
| Compass, 432 Park PH88 | Architect drawing in a full-screen tab | Plan in its own tab beside Photos / Virtual Tour / Map / Street View. Price, beds and baths and "Contact" stay pinned at the top while you look. Broker monogram. An alternate plan is offered. | Room sizes on the drawing |
| Sotheby's, 39 Crosby PHN | Technical black-and-white plan | Mounted as a card on the navy gallery background, last slide (23/23). Brand logo, compass rose, tiny disclaimer. Functional, not emotional. | Room sizes, small |
| Central Park Tower (developer site) | Availability table | Each residence row: beds, baths, sq ft, offering price, monthly charges, taxes, and a "Floor plan · View" button. Decision data plus plan in one line. | (plans behind the button) |
| Giraffe360 interactive 3D floor plans (vendor docs, Sep 2025) | Interactive 2D/3D plan on the property website | "Rotate & explore … Select rooms – highlight a room, zoom in, and view its label … 2D/3D toggle". Jumps into the tour. | measurements optional |
| Matterport (support docs) | Dollhouse 3D + schematic floor plan from a scan | Visitors switch between Dollhouse and Floor plan views. Room types and measurements can be shown or hidden per space. | can be hidden |
| Zillow 3D Home interactive floor plan (press, 2021 to 2022; not captured, Zillow blocks automation) | AI-built plan with photo positions | Click a room on the plan and see that room's photos. | AI-predicted |
| CubiCasa (site returned 403 to automation; vendor material) | Phone-scanned plans; "Premium" furnished 3D plans in style sets (Scandinavian, French, Country) | Furnishing shows the space's potential. | optional |
| RoomSketcher (vendor page captured) | Furnished 2D/3D plans, "Live 3D" walk, letterhead branding | Vendor cites Zillow research: 81% of buyers are more likely to view a home whose listing has a floor plan they like. | optional |

What the expensive ones leave out:

- dimension lines and chains;
- wall hatching;
- door-swing clutter;
- electrical and plumbing symbols;
- the architect's title block and permit numbers;
- unit-number codes.

What they add instead:

- furniture at true scale;
- outdoor space in a material colour;
- light (a sun path);
- position in the building (a key plan);
- a short "arrangement" list with total areas.

Dimension practice:

- Developer brochures (London, Dubai) keep the drawing clean and put sizes in a table or leave them out, under an "illustrative / not to scale / approximate" line.
- New York brokerage listings usually print room sizes on the plan.
- So "no exact dimensions on the drawing" is a recognised luxury convention, provided the totals are honest and a disclaimer is shown.

Our architect file `../plan/plan-300dpi.png` is a permit-style drawing with dimension chains on every wall. **No north arrow is visible at preview size.** So sun, sea or park bearings must not be drawn unless they are verified from the permit plan or a survey (honesty law: never invent bearings or views).

## 5. Keywords (DataForSEO, 27 Oct 2026, Israel 2376, Hebrew)

Volumes are monthly. "Labs" is DataForSEO Labs keyword_overview. "Ads" is Google Ads search_volume (`language_code iw`). Both agree wherever both exist.

| Keyword | Monthly searches | KD | CPC $ | Intent | Notes |
|---|---|---|---|---|---|
| כוכב הצפון | 5,400 | 0 | 1.57 | informational | **Not a buyer term.** The SERP is about the North Star, a TV series, a newspaper, Sakhnin and Ashdod. |
| פנטהאוז | 3,600 | 9 | 1.10 | informational | Mixed (includes the furniture brand "פנטהאוז בייסיק" 1,600) |
| דירות למכירה בתל אביב | 880 | 3 | 2.75 | transactional | **Protected**, owner: city page (HAD-602) |
| כוכב הצפון תל אביב | 720 | 0 | 0.96 | informational | Neighbourhood term |
| מיני פנטהאוז | 170 | 0 | 6.19 to 6.71 | transactional | Our page's natural head term |
| פנטהאוז למכירה | 170 | 0 | 2.76 | transactional | **Protected, owner /properties/** (kw_guard BLOCKs a title that leads with it) |
| פנטהאוזים למכירה | 170 | 0 | 2.91 | transactional | |
| דירות יוקרה בתל אביב | 140 | 0 | 2.94 | informational | |
| פנטהאוז בתל אביב | 110 | 0 | 3.02 | informational | |
| מה זה פנטהאוז | 110 | 0 | none | informational | Owner: /glossary/penthouse/ |
| פנטהאוז למכירה בתל אביב | 90 | 0 | 4.24 (comp HIGH) | transactional | No nad-lan owner. Portals' category pages lead, but **single listings rank #4 and #7** (domestictlv.co.il) |
| דירות / דירה למכירה בצפון תל אביב | 70 | 0 | 5.65 | transactional | Leads with protected "דירות למכירה" |
| דירות יוקרה למכירה בתל אביב | 70 | 0 | 5.90 | transactional | |
| מה זה מיני פנטהאוז | 50 | 0 | none | informational | Owner: /glossary/penthouse/ |
| מיני פנטהאוז למכירה | 40 | 0 | 2.38 | transactional | |
| דירות למכירה בכוכב הצפון | 30 | 0 | 2.13 | transactional | **A single listing ranks #9** (israelsir.co.il, Kochav HaTzafon penthouse). Leads with protected "דירות למכירה", so use it in body, not as the title start. |
| דירות גג למכירה בתל אביב, פנטהאוז למכירה תל אביב, שדרות לוי אשכול תל אביב | 30 each | 12 to 13 | | | |
| פנטהאוז בצפון תל אביב, פנטהאוז למכירה בצפון תל אביב, מיני פנטהאוז למכירה בתל אביב, פנטהאוז חדש למכירה, דירת גג למכירה | 10 each | | | | |
| פנטהאוז ליד פארק הירקון, פנטהאוז בכוכב הצפון, דירה למכירה בכוכב הצפון, פנטהאוז חדש, מיני פנטהאוז תל אביב | no measurable volume | | | | Exact-match, zero competition |
| **English (Google Ads, Israel):** kochav hatzafon | 1,300 | | 0.50 | | Labs US: 20 |
| apartment for sale tel aviv / buy apartment in tel aviv | 210 (IL), 390 (US) | 0 | 3.2 to 4.1 | | |
| tel aviv real estate | 210 (IL), 480 (US) | 4 | | | |
| penthouse tel aviv | 50 (IL) | | 3.46 | | |
| penthouse for sale tel aviv, luxury penthouse tel aviv, mini penthouse tel aviv | below Google Ads threshold | | | | **single listings rank** (Barnes #2, israelsir.com #3 and #7) |

Live SERP, desktop, top 20, 27 Oct 2026 11:54 to 11:55 UTC (`data/serp-top20-2026-10-27.json`):

- **"פנטהאוז למכירה בתל אביב"** (plus a mobile check):
  - Leaders: Yad2 and Madlan category pages, nyg.co.il, israelsir.co.il tag pages.
  - Single listings that rank: domestictlv.co.il #4 and #7 ("פנטהאוז עם בריכה…", "פנטהאוז נדיר…").
  - AI overview shown.
- **"פנטהאוז למכירה":**
  - Leaders: indik.net, Yad2, domestictlv, Komo, israelsir.
  - AI overview names Yad2 and Madlan.
- **"מיני פנטהאוז":**
  - Mostly Facebook posts, ynet, Wikipedia.
  - Madlan's building page for Levi Eshkol 2 (our street) ranks #8.
  - A single listing (domestictlv) ranks #7.
  - Glossary pages from #15.
- **"דירות למכירה בכוכב הצפון":**
  - Broker neighbourhood pages, Yad2 neighbourhood, yadata.
  - Single listing: Israel Sotheby's "פנטהאוז מודרני יוקרתי בכוכב הצפון" at #9 and #10, and a Sotheby's new apartment in Kochav HaTzafon at #16.
- **"פנטהאוז בצפון תל אביב":**
  - Single listing: harova.co.il "פנטהאוז יוקרתי בצפון הישן" at #2.
- **"penthouse for sale tel aviv"** (English, Israel): Properstar, then a Barnes single listing #2, Israel SIR single listings #3 and #7, and a YouTube tour #4.
- **nad-lan.co.il is not in the top 20 for any of these.**

**Search Console** (read-only API query, property sc-domain:nad-lan.co.il, 1 Sep to 26 Oct 2026):

- The HE listing earned **16 impressions, 0 clicks** (9 to 25 Oct). Daily average position was 4 to 16. All queries are anonymised (too rare to show).
- The EN listing earned 3 impressions (14 and 19 Oct).
- Over 90 days the whole site has almost no penthouse visibility: /tel-aviv-penthouse-prices/ 2 impressions, /glossary/penthouse/ 1.
- The Sep 29 CSV exports in `GSC-Data` predate the listing.

kw_guard checks (protected-keyword law):

- OK: "מיני פנטהאוז 5 חדרים למכירה בכוכב הצפון | 80 מ״ר מרפסות" (title)
- OK: "מיני פנטהאוז חדש בכוכב הצפון: 5 חדרים ו-80 מ״ר מרפסות" (H1)
- OK: "מיני פנטהאוז חדש למכירה בכוכב הצפון, ליד פארק הירקון" (H1)
- OK: "New Mini Penthouse for Sale in Kochav HaTzafon, Tel Aviv" (title)
- **BLOCK**: "פנטהאוז למכירה בתל אביב: …" (leads with protected "פנטהאוז למכירה")
- **BLOCK**: "דירות למכירה בכוכב הצפון: …" (leads with protected "דירות למכירה")

## 6. Not verified / limits

- **Read-only DOM measurements.**
  - Prices in split nodes were matched by digits. Property Finder's price (AED 400,000,000) and Knight Frank's desktop price (440 / 24px) were read from the DOM text and screenshots by hand. The probe's automatic pick there was a sticky-header copy or an average-price line.
  - Positions shift with fonts, ads and consent banners. The raw shots show what a first-time visitor actually sees: cookie banners cover about 13% to 60% of the phone screen on Knight Frank (60%), Savills (38%), Yad2 (about 45% with its Google sign-in prompt), Barnes (28%) and Domestic (13%), and Property Finder opens a survey pop-up.
- **Not captured as screenshots:**
  - the Zillow interactive floor plan (Zillow blocks automation);
  - CubiCasa (403);
  - the Central Park Tower plan modal (its "View" control did not open headless).
  - These are described from vendor or press sources only.
- **Branded-residence developer sites** (Aman, Bulgari, Four Seasons, Omniyat, Chelsea Barracks) show no prices and gate plans behind enquiry. They were reviewed, not measured as listings.
- **Our page changed live during the work** (1.72.537). Numbers marked 11:52 are current as of 12:12 UTC.
