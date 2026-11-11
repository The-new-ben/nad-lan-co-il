# Apartment designer: product teardown (HAD-701)

Date of all observations: 2026-11-10. Researcher: Claude Code research agent, for the lead session.

## How to read this file

Every claim carries an evidence class:

| Tag | Meaning |
|---|---|
| **[LT]** | Live-tested by us on 2026-11-10 in a scripted headless Chrome. The number or behaviour comes from our own run. |
| **[SL]** | Seen live. We saw a label, screenshot or control on the vendor's public page, but did not operate it. |
| **[VC]** | Vendor claim: the vendor's own pricing page, help centre, blog or case study. Not verified. |
| **[PR]** | Press or a sponsored article. |
| **[RV]** | Third-party review or directory listing. |

**Test rig, used for every [LT] number.** Headless Chrome (desktop install at `C:/Program Files/Google/Chrome/Application/chrome.exe`) was driven over the DevTools protocol by two zero-dependency Node 24 scripts. Desktop ran at 1366x900 and DPR 1. Mobile ran at 390x844 and DPR 2, with an Android Chrome user agent and touch emulation. Each run used a cold cache and no network throttling. WebGL ran on **SwiftShader, a software renderer, with no GPU**, so heavy 3D times are upper bounds and only comparable within this rig. Transfer sizes are the sum of `encodedDataLength` across all requests. "MB" in all these files means MiB (bytes ÷ 1,048,576). "Canvas ready" means the first `<canvas>` larger than 300x200 CSS px. Raw JSON for every run is in `evidence/*-results.json`, and the screenshots are in `evidence/*.jpg`.

**What we did not do.** We created no accounts, accepted no terms-of-service dialogs, uploaded nothing and submitted no forms. Any flow behind those walls is recorded as a limitation, not guessed.

---

## 1. Candidate long list (21 products) and selection

| # | Product | Type | Coverage | Why |
|---|---|---|---|---|
| 1 | Planner 5D | Consumer and pro planner, AI | **Deep** | Market leader. It has AI plan recognition, live co-editing, a price estimator and a budget widget. |
| 2 | Homestyler (Easyhome/Alibaba lineage) | Consumer and pro planner, cloud render | **Deep** | Up to 12K renders, an AI suite, BOM export and DWG/PDF import. It is the only deep product with an RTL language (Arabic). |
| 3 | Coohom (international arm of Kujiale) | Pro planner, cloud render, B2B | **Deep** | Strongest public visual output (path-traced 360 tours), plus a BOM and quotation engine, team co-editing and a panorama product list. |
| 4 | RoomSketcher | Floor-plan specialist | **Deep** | Plan accuracy focus, a human redraw service, synced 2D+3D "Live 3D" and team collaboration. |
| 5 | Floorplanner | Lightweight 2D/3D planner and embeddable engine | **Deep** | The only deep editor that is **publicly testable without sign-in** (`/demo`). |
| 6 | Higharc Showroom | **Developer-side configurator tied to real plans** | **Deep** | Plans are authored in the builder's own system, with options, lot pricing and lead handoff. Its public demo was testable. |
| 7 | GBuilder (Finland) | Developer-side **apartment** configurator | Reference column | It is the closest match to new-build apartments in towers: unit selector, material options with extra cost and e-signature. Evidence is vendor-only, because no public demo was found. |
| 8 | Zonda Envision / VR360+ (US) | Builder design-centre selections | Light | Options, real-time pricing and 360 scenes. Vendor-only evidence. |
| 9 | HomeByMe (Dassault Systèmes) | Consumer planner with branded catalogue | Light | Branded products and 4K renders. Its start flow returned 404 in our run [LT]. |
| 10 | IKEA Kreativ | Retail room designer and scan | Light | LiDAR scan, furniture erase and a priced own catalogue. Its web app URL returned 404 in our run [LT]. |
| 11 | magicplan | Scan, sketch and estimate for contractors | Light | It is the strongest at cost estimates and material lists, but has no interior design. |
| 12 | Roomle (Rubens Room Designer) | Retail configurator platform | Light | Public demo tested: 2D/3D, first-person, AR, parts list and cart. |
| 13 | Rayon | Multiplayer 2D plan editor ("Figma for plans") | Light | The reference for real-time collaboration. Its app host failed to connect from our rig [LT]. |
| 14 | Floorfy | Real-estate tours with **video calls** | Light | The only vendor found with video calls built into a property tour. There is no design editing. |
| 15 | CPQ3D / London Dynamics | 3D configurator plus video co-session | Light | Vendor claims both parties edit a configuration during a video call. Their market is outdoor structures. |
| 16 | Interior AI | AI image restyle | Light | Image generation only, with no model. |
| 17 | RoomGPT | AI image restyle | Light | Same: image generation only. |
| 18 | Spacely AI | AI render for pros, "Team Canvas" | Light | AI with a team canvas. |
| 19 | ReimagineHome | AI staging with **real products and structure lock** | Light | The only AI tool that claims to lock walls, windows and doors and to use real, purchasable products. |
| 20 | Collov AI | AI virtual staging | Light | Staging and material overlay. |
| 21 | Israeli: Muonovate, REALS (Simplex 3D), Vizit (3DCOM) | Pre-sale 3D and tenant change | Light | Muonovate describes online tenant-change requests (move an outlet, pick tiles). REALS covers view and shading. **vizit.co now serves a gambling-spam page [LT via fetch]. Do not link to it.** |

We also excluded Archilogic (plan-to-3D digitisation service with an API). It has no buyer design flow, but it is a potential supplier for plan digitisation. Help-centre caveats: "cannot guarantee an accurate model without a proper scale" [VC] https://help.archilogic.com/knowledge/best-practice-for-floor-plans

---

## 2. Deep teardowns

### 2.1 Planner 5D (planner5d.com)

**What it is.** A freemium home-design planner on web, iOS, Android, Windows and macOS. It draws 2D and 3D floor plans, furnishes from a catalogue, renders, and has an AI layer called "AI Studio" (Copilot, Smart Wizard, Design Generator).

**Flow from start to a result.**
1. Landing page, then "Get Started".
2. `/editor` redirects to `/auth/email`, a **sign-up wall** with Google, Apple or email [LT], `evidence/planner5d-editor-desktop.jpg`.
3. After sign-up the vendor describes this path: draw or upload a plan, then furnish, switch to 3D, render, and share or collaborate [VC].
4. The public gallery project page offers "Open in 3D", but that opens a **terms-of-service "I Agree" modal** before any 3D view [LT], `evidence/planner5d-12-open-in-3d.jpg`. We did not accept it, so the 3D viewer was not reached.

**Plan tools.**
- AI plan recognition converts JPEG, JPG or PNG into an editable 2D/3D project. The upload text also mentions PDF, so the page is inconsistent. It takes "typically 1-2 minutes", the user gets an email when it is ready, and "measurements are approximate" [VC] https://planner5d.com/use/ai-floor-plan-generator
- The B2B API lists JPEG, PNG, PDF, DWG, DXF and TIFF, and a designer checks quality [VC] https://tool.planner5d.com/b2b-floor-plan-recognition
- One review reports that wall snapping is finicky [RV] (search summary of third-party reviews).

**2D↔3D link.** A single project with 2D and 3D modes [VC]. Not testable by us.

**Visual quality.**
- Professional plan: "Unlimited 4K renders", "360° walkthrough and 360° panorama" [VC] https://planner5d.com/pricing
- No VR or AR is listed on the pricing page [VC]. Third-party listings mention VR and AR [RV].

**Catalogue.**
- Free plan has 50% of the catalogue. Premium has "10,000+ premium items" [VC].
- No brands are named. Enterprise customers can "own and manage your 3D product catalogue" [VC].

**Generation.** Copilot adds furniture and finishes from a text or voice description. Smart Wizard builds a design from room shape, style and type. Design Generator works from a room photo [VC].

**Collaboration.**
- Web "Live Collaboration" uses per-person roles: Can view, Can comment or Can edit [VC] https://support.planner5d.com/en/articles/14602018-how-to-use-live-collaboration-tool
- The marketing page claims multiplayer editing on any device and on the free plan [VC] https://planner5d.com/collaboration-tool
- The help centre is narrower. It says shared projects are view-only except for web Live Collaboration [VC] https://support.planner5d.com/en/articles/15116256-how-to-share-projects
- No video calling exists.

**Spec and cost.**
- Premium includes a "Budget Widget". Professional includes a "Specs & Docs Organizer", a "Price Estimator" and CAD export [VC] https://planner5d.com/pricing
- Price data sources, currency rules and VAT basis are not documented.

**Mobile UX.**
- The mobile landing primary CTA "Get Started" is centred at y=369 of 844 (44% of the screen height), above the comfortable thumb zone.
- 2 of 9 first-viewport controls are under 44 px.
- LCP 1.07 s, 3.5 MB. All three figures are [LT] from `evidence/mobile-results.json`.

**Performance.**
- Desktop landing: LCP 1.91 s, **CLS 0.441** (poor; the "good" threshold is ≤0.1), 3.0 MB, 136 requests, 25 hosts [LT].
- Editor: not measurable, because of the sign-up wall.

**Accessibility and RTL.**
- hreflang lists 14 locales and no Hebrew; `dir=ltr` [LT].
- 20 interactive controls have no accessible name [LT].
- `/accessibility` returns 404 [LT].
- The pricing page displays prices in ₪ to Israeli visitors, so the site is currency-localised but not language-localised [VC page fetch].

**Developer integration.**
- Enterprise offers a white-label planner, a 3D configurator, connections to cart, CRM, ERP and quoting, and APIs [VC].
- Real-estate B2B offers staging of empty or unfinished properties [VC] https://tool.planner5d.com/b2b-real-estate
- No unit-plan pipeline from a developer is documented.

**Business model.**
- Freemium: Premium ₪199.99 a year, Professional ₪1,349.99 a year (₪ display), Enterprise custom [VC].
- AI credits: 100 a month on Premium, 1,000 a month on Professional [VC].

---

### 2.2 Homestyler (homestyler.com)

**What it is.** A cloud 3D home-design platform with very large render capacity, an "AI Studio" (AI Planner, AI Stager, AI Moodboard, AI Render, AI Animator) and community galleries.

**Flow.**
1. Landing page, then "Floor Planner for Web" (mobile) or "Get started".
2. `/floorplan` redirects to `3d.homestyler.com`, which shows a **sign-in modal** (Google, Facebook, Apple, VK, Telegram, X, QR or email) [LT], `evidence/homestyler-floorplan-desktop.jpg`.
3. A public community project page loads as an AI-gallery detail page with images and no 3D model [LT], `evidence/homestyler-11-project-detail.jpg`.

**Plan tools.** Build > Import Floor Plan [VC] https://www.homestyler.com/forum/view/2077998093719244802 accepts:
- images (JPG/PNG, 5 MB each, up to 10 floors);
- DWG (AutoCAD 2023 or earlier, 10 MB);
- PDF (versions 1.0 to 1.7, 10 MB, 20 pages; PDF/A and encrypted files are not supported);
- RoomScan (iOS 16 with LiDAR).

You can trace it manually or use "Auto Generate (Beta)". No accuracy figure is published and no scale-calibration step is documented.

**Visual quality.**
- Free: unlimited 1K. Pro+: 75 2K and 75 4K renders a month, 20 8K a month, and 2 12K a month.
- Pay-per-render: 12K panorama $3.99; video 1080p at $5.99 per 10 s. "LightMix" and custom lighting [VC] https://www.homestyler.com/pricing
- The landing page uses WebGL and plays heavy video (9.1 MB of media) [LT].

**Catalogue.**
- "100,000+ free 3D models and materials" (pricing page) against "1M+ Models" in the page title [LT title, VC count]. That is an internal inconsistency.
- Branded models exist. Prices per item are not documented.

**Generation.** AI Planner 15 credits a plan; AI Stager, AI Texturer and AI Painter 10 credits an image; AI Render 25 to 35 credits; AI Animator by the second [VC].

**Collaboration.** The Team plan has a "shared design space" and shared libraries [VC]. Virtual-tour links are generated from panoramas [VC forum]. No video calling exists.

**Spec and cost.** Pro+ can "Export colored floor plans, BOM, and construction drawings" [VC]. Whether the BOM carries prices is not stated.

**Mobile.**
- The landing redirects to `m.homestyler.com`. It **blocks pinch-zoom** (`user-scalable=no` or `maximum-scale=1`) [LT].
- LCP 6.4 s and load event 30.6 s in our rig [LT].
- The primary CTA sits at y=395 of 844 (47%) [LT].

**Performance (desktop landing).** **20.1 MB** transfer (9.1 MB of it video), 217 requests, 49 hosts, LCP 3.98 s [LT]. Heaviest landing page of the deep set.

**Accessibility and RTL.**
- hreflang includes **`ar` (Arabic, an RTL language)** but not Hebrew [LT].
- Whether the editor mirrors for RTL is unknown, because of the sign-in wall.
- 42 of 166 images lack alt text, and 11 controls are unnamed [LT].
- `/accessibility` returns 404 [LT].

**Developer integration.** Enterprise offers SSO, white label, a custom API and 3D model creation [VC]. No unit-plan pipeline is documented.

**Business model.** Freemium plus credits: Pro+ from $6.8 a month, Master+ from $11.8, Team from $19.9 per seat a month, plus pay-as-you-go renders [VC].

---

### 2.3 Coohom (coohom.com, international arm of Kujiale)

**What it is.** A pro-grade interior and kitchen platform with cloud ray-traced rendering, "720°" panorama tours, cabinet manufacturing output (BOM, CAM export) and enterprise quotation.

**Flow.**
1. Landing page, then "Start for free" (a full-width button on mobile) [LT].
2. The editor requires an account; `/floor-planner` is a marketing page [LT].
3. The public share output is a **panorama tour link that opens with no sign-in** [LT]:
   https://www.coohom.com/pub/tool/panorama/show?obsPlanId=3FO43N7KQ0C1
   https://www.coohom.com/pub/tool/panorama/aiwalking?obsPlanId=3FO43N7KQ0C1&locale=en_US

**Plan tools.**
- Uploads accept JPG, PNG, PDF, DWG, DXF and WEBP.
- The "AI floor plan generator detects walls, doors, and windows" [VC] https://www.coohom.com/floor-planner
- Units, wall thickness and door sizes are configurable [VC].
- No accuracy figure is published.

**2D↔3D link.** The design is drawn in 2D and previewed in 3D [VC]. In the shared tour, a floor-plan **minimap shows about 16 viewpoint pins and a live view cone**, and "Room Select" jumps between rooms [LT], `evidence/coohom-16-floor-plan.jpg`.

**Visual quality.**
- The **best public visual of the deep set**. Pre-rendered path-traced 360 panoramas show realistic glass reflections, soft shadows and exterior views [LT], `evidence/coohom-11-panorama.jpg`, `coohom-14-aiwalking.jpg`.
- Navigation hops between fixed nodes; there is no free walk.
- A VR button for a phone headset [LT mobile]; VR mode needs a merchant setting [VC] https://www.coohom.com/helpcenter/how-to-see-vr-effect-in-panorama
- Pro: unlimited 4K, 8K panoramas, and 720° tours on Pro and above [VC] https://www.coohom.com/pricing
- The real-time lighting engine claims whole-house render time cut "from 2 hours to under 15 minutes" [VC] https://blog.coohom.com/?p=4974

**Catalogue.**
- "100K+ premium model catalog (500 added weekly)" with branded models [VC].
- The tour's **"Product List" panel** has Brand and Reference tabs. It lists items in the scene with thumbnails, but **shows no prices**, and item names leak in Chinese (for example 玻璃窗 "glass window") on an English-locale link [LT], `evidence/coohom-15-product-list.jpg`.

**Generation.** AI templates, an "AI agent floor planner" page (link [SL]) and AI home design pages [SL].

**Collaboration.**
- Elite plan: "Team co-editing", up to 20 seats, and a "3D presentation (shareable interactive link)" [VC].
- Panorama shares can carry a password, an expiry date, a QR code or a poster [VC] https://helpcenter.coohom.com/en/articles/8314349-panorama-editor-available-to-all-users
- No video calling exists.

**Spec and cost.**
- Pro: "Downloadable bill of materials".
- Enterprise: "Custom quotation and BOM export", ERP/CRM integration, K&B order management [VC].
- Cabinet quoting by unfolded or projected panel area, with formula-based pricing [VC] https://www.coohom.com/de/helpcenter/enterprise-cabinet-projection-area-quotation-settings

**Mobile.**
- The landing CTA sits at y=400 of 844 (47%) and is 350 px wide [LT].
- In the mobile panorama, all controls (menu, fullscreen, VR, share) sit in the **top-right corner**, outside the thumb zone [LT], `evidence/coohom-13-panorama-mobile.jpg`.
- On mobile, the panorama canvas was ready about 11.1 s after navigation, with 15.7 MB transferred [LT].

**Performance.**
- Landing: LCP 1.78 s, 3.2 MB [LT].
- Panorama tour, desktop: canvas about 15.0 s after navigation, **15.2 MB / 182 requests at first view** and 16.9 MB after one drag [LT].
- AI-walking tour: canvas about 8.6 s, 12.1 MB [LT].

**Accessibility and RTL.**
- hreflang lists 18 locales and no Hebrew or Arabic [LT].
- The tour UI renders in an inner document, and our accessible-text read returned nothing.
- `/accessibility` returns 404 [LT].

**Developer integration.** Enterprise offers a white-label room planner, cross-enterprise project sharing and ERP/CRM integration [VC]. Kujiale is widely used by Chinese developers and decoration firms [RV]. No Israeli or Hebrew deployment was found.

**Business model.** Basic free (3 projects). Pro ₪1,100 a year. Elite ₪2,100 per seat a year. Enterprise custom (₪ shown to us) [VC].

---

### 2.4 RoomSketcher (roomsketcher.com)

**What it is.** A floor-plan specialist with an app and a web app. It produces 2D and 3D floor plans, 3D photos, 360 views, "Live 3D" walkthroughs, and offers a paid human redraw service.

**Flow.**
1. Landing page, then "Get Started for Free" (sign-up).
2. The `/demo/` page is a video page with no interactive demo [VC fetch].
3. We found no public Live 3D sample link, so there was **nothing operable without an account**.

**Plan tools.**
- "Draw From a Blueprint" (Pro) and "AI Convert" ($20 a floor on Free; credits on paid plans) [VC] https://www.roomsketcher.com/pricing/
- Human "Order Floor Plans": $38 a floor on Free, from $18 a floor on subscriptions. JPG, PNG or PDF in, delivered the next business day, with free regeneration for 30 days [VC] https://www.roomsketcher.com/order-floor-plans/
- "Measurements and total area" and "Print to scale" (Pro) [VC].

**2D↔3D link.** The Live 3D feature page shows **a 2D plan with a camera marker beside a synced 3D window** [SL], `evidence/roomsketcher-live3d-desktop.jpg`, https://www.roomsketcher.com/features/live-3d-floor-plans/. This is the clearest shared-camera 2D↔3D pattern in the set.

**Visual quality.** 3D photos and 360 views on credits; Live 3D on Pro [VC]. Render engine and quality: unknown (no sample reachable).

**Catalogue.** The furniture and symbol library is "Limited" on Free and "Full catalog" on paid plans [VC]. No brands or prices are given.

**Generation.** None found.

**Collaboration.**
- "Share project", and "Share project incl. Live 3D" (credit-based) [VC].
- "Project collaboration" on the Team plan only; real-time behaviour is not described [VC].
- No video calling exists.

**Spec and cost.** None (no BOM or cost) [VC pricing table].

**Mobile.**
- Landing CTA at y=413 of 844 (49%); 4 of 6 controls under 44 px; LCP 1.71 s [LT].
- Native apps exist [VC].

**Performance (desktop landing).** LCP 1.82 s, 1.9 MB, 88 requests, 32 hosts, CLS 0.003 [LT]. Lightest landing page of the deep set.

**Accessibility and RTL.**
- No hreflang; English only; `dir=ltr` [LT].
- 0 unnamed controls and 0 images without alt: the best landing-page hygiene of the deep set [LT].
- `/accessibility` returns 404 [LT].

**Developer integration.** Branding and customer profiles on Team [VC]. Industry pages target real estate [SL]. No unit-plan pipeline exists.

**Business model.** Free / Pro $144 a year / Team $420 per user a year, credits, plus the per-floor redraw service [VC].

---

### 2.5 Floorplanner (floorplanner.com)

**What it is.** A Dutch lightweight browser planner with an embeddable engine and API (there is an API docs link on its pricing page). Credits unlock export resolution.

**Flow (fully live-tested).**
1. https://floorplanner.com/demo opens an "Example House" editor **with no sign-in** [LT], `evidence/floorplanner-demo-desktop.jpg`.
2. A left rail offers Project, Build, Info, Objects, Styleboards, Finishes and Help.
3. Build offers "Upload 2D floorplan", Draw Room, Wall, Surface, Doors, Windows and Structurals [LT].
4. Clicking a room opens a property panel: "Living, 40.2 m²", Floor Finish "Wood Planks Bare 0335", Wall Finish names and a styleboard slot. **No prices appear anywhere** [LT], `evidence/floorplanner-02-room-selected.jpg`.
5. The 2D/3D toggle (top right) opens 3D. Camera types are None, Dollhouse and **First Person**, with camera height (143 cm default), field of view (75°), a **sun-position dial**, "Play viewpoints" and saved cameras [LT], `evidence/floorplanner-07-3d-8s.jpg`.

**Plan tools.**
- Dimension chains in metres with two decimals, and an m/ft toggle [LT].
- The demo shows an uploaded plan used as an underlay [LT]. Auto-recognition: unknown.

**2D↔3D link.**
- The same model is shown through a full-screen toggle, not a side-by-side split [LT].
- A complete first-person frame was on screen **≤3.2 s after clicking 3D**, but the switch downloaded **+12.2 MB** (cumulative 21.1 MB at first 3D frame, 25.5 MB after 15 s) [LT].

**Visual quality.**
- Real-time WebGL2 [LT]. The real-time view is rasterised with flat lighting and no visible soft shadows or GI.
- Stills are SD free; HD, 4K and 8K are paid with credits [VC] https://floorplanner.com/pricing

**Catalogue.** A furniture library and "Finishes" (named materials) with no brands or prices visible [LT]. Library size: unknown.

**Generation.** "Styleboards", a rule-based style apply, exist [LT]. There is no AI text-to-design.

**Collaboration.** Teams pricing and "more users" [VC]. No co-editing is described. No video calling exists.

**Spec and cost.** None visible in the editor [LT].

**Mobile.**
- The demo on a 390 px viewport is **view-only**: the UI is just 2D/3D, Settings and Undo/Redo, and **5 of 6 controls are under 44 px** [LT], `evidence/floorplanner-10-mobile.jpg`.
- The 2D/3D toggle sits near the top (y≈90 of 844).
- The canvas was ready ≈4.6 s after navigation, with 8.8 MB [LT].

**Performance.**
- Desktop editor canvas ready at 5.6 s; **8.8 MB / 118 requests at 2D ready**; 21.1 MB at first 3D frame [LT].
- Landing: LCP 2.58 s, 2.7 MB [LT].

**Accessibility and RTL.**
- No hreflang; English UI; `lang=en`, `dir=ltr` in the editor [LT].
- Only 3 unnamed controls on the landing page [LT].
- `/accessibility` redirects to `/login` [LT].

**Developer integration.** An embeddable engine and API exist (the pricing page links to API docs) [SL]. No developer unit-plan pipeline.

**Business model.**
- Free for 5 projects.
- Credits from $8.15 for 5 credits to $163 for 100 credits.
- Per-project levels: SD free, then HD, 4K and 8K [VC].

---

### 2.6 Higharc Showroom (developer-side, real plans)

**What it is.** Higharc is a US homebuilding platform where builders author plans as rule-driven parametric models (Higharc Config). Showroom is the buyer-facing 3D configurator of those **same** plans, with "real-time pricing", "lot premiums and options pricing", "ERP-integrated pricing" and a captured lead that carries plan, options and price [VC] https://higharc.com/product/showroom. Showroom is labelled beta [VC].

**Flow (live-tested on the vendor's demo builder site).**
1. https://demo.higharc.com/floorplans/belmont/ is the plan page: 3 bed, 2.5 bath, 2,830 ft², four elevations, prices "Starting at $405,000" and more by community, and a **"Design in 3D"** button [LT].
2. The button carries `data-higharc-plan-id`. An embed script, `app.higharc.com/static/builders/scripts/showroom.js?builderId=…`, opens an iframe to `app.higharc.com/showroom/intro?...` [LT, source read]. In headless Chrome the click did not open the overlay, so we opened the intro URL directly:
   https://app.higharc.com/showroom/intro?builderId=G3de6WX90K7nylNm&planId=X1BPz26zwx2yA7Qp&planType=master_plans&embedSource=script
3. The intro shows a split screen [LT], `evidence/higharc-15-intro-orbit.jpg`:
   - left: a 3D viewport with **Exterior / Interior** tabs and a mini-map tile;
   - right: an option rail (Elevation with renders, Exterior Palettes, Mirror, Watertable height, Exterior wall 2x4/2x6, Tier, Foundation type, garage count, door height and so on, with plain-language descriptions);
   - "Reset to original", "Share", "Save", and an option search with a **ctrl+K** shortcut.

**Data inconsistency (trust).** The plan page says **2,830 ft²** and the configurator header says **2,889 sqft** for the same plan [LT].

**Plan tools.** Buyers cannot draw. The plan comes from the builder's model. This is the **correct pattern for new-build** [LT/VC].

**2D↔3D link.** One parametric model drives 3D, renders and construction documents [VC] https://www.higharc.com/product/config. A plan mini-map tile is present [LT]. The 2D floor-plan view itself was not reached in our rig.

**Visual quality.**
- WebGL2 [LT]. **The 3D viewport stayed on "Loading your 3d home…" for 36 s** in our software-WebGL rig, after 1,209 requests and 11.8 MB [LT]. Real-GPU performance: unknown.
- Elevation thumbnails are photoreal renders [LT].
- "Higharc Photoreal" exterior renders [VC case study].

**Catalogue and pricing.**
- The options are the builder's real SKUs [VC].
- **No price appeared** in the demo's option rail: 0 lines containing "$" [LT]. Real-time pricing is claimed but was not visible in this demo configuration.

**Generation.** The rule engine produces compliant variants [VC]. There is no AI styling for buyers.

**Collaboration.** Save and Share buttons [LT]. Sales handoff with selections [VC]. No co-editing or video.

**Spec and cost.**
- "Downloadable takeoff data and construction document previews" [VC].
- Buyer-facing BOM: not seen.

**Mobile.** At 390 px the intro was a **blank white screen 7.6 s after navigation** (5 of 5 visible controls under 44 px) [LT], `evidence/higharc-16-intro-mobile.jpg`. It may have rendered later; we stopped there.

**Performance.** The intro reached 8.1 MB / 1,070 requests at 28 s and 11.8 MB / 1,209 requests at 36 s [LT]. The request count is very high, with many small asset fetches.

**Accessibility and RTL.**
- English only [LT].
- Controls are labelled ("Zoom in", "Reset zoom", "Search options (ctrl+K)") [LT].
- `/accessibility` returns 404 on the main site [LT].

**Developer integration.** The strongest of the set. Plans, options, lot rules, pricing and ERP sit in one platform. An embed is available on the builder's site ("Showroom Intro") [VC] https://intercom.help/higharc-ee9866fba7c9/en/articles/17313624-showroom-intro. A customer case study (Landmark 24 Homes) claims higher option sales [VC] https://www.higharc.com/customer-playbooks/how-greyson-miller-digitally-transformed-landmark-24-homes-buyer-experience

**Business model.** Included in Higharc Enterprise and Ready to Build tiers; enterprise SaaS for builders. The price is not public [VC].

---

### 2.7 GBuilder (reference column; vendor evidence only)

**What it is.** A Finnish platform for apartment and house developers. It provides a sales module (interactive building or site map with unit info, layout, price and availability), an "interactive, high definition 3D model" of the selected unit, buyer material options "with accurate extra costs", furnishing try-on, and an embed or own-domain deployment [VC] https://gbuilder.com/resources/market-and-sell-off-plan-homes-with-an-interactive-home-selector-and-high-definition-3d-models

**Other claims.**
- Buyers make several design variants, and **one is confirmed by built-in e-signature**.
- The developer sees the margin per choice and predefined interior packages [VC, search summary of gbuilder.com resources].
- Customers named on the sales page: YIT, Bonava, Aldar, Thakeham, Hartela [SL] https://www.gbuilder.com/solutions/sales
- Languages: EN, DE, SV, ES, NL. No Hebrew [SL].

**Limits.** No public demo was found, so every behavioural value is a vendor claim.

**Measured landing page.** Desktop LCP 0.66 s, 4.7 MB [LT]. Mobile LCP 1.08 s but load event 39 s [LT].

**Why it matters.** It is the nearest existing product to "a buyer opens a tower-apartment plan and picks finishes with prices". It has no free interior design, AI, video call or Hebrew.

---

## 3. Light coverage (one paragraph each)

**Zonda Envision / VR360+.** US design-centre selections. Builders publish options, wish lists and pricing online before the in-person appointment. VR360+ adds "real-time pricing and manufacturer-sourced product content" to 360 scenes [VC] https://zondahome.com/digital-solutions/envision/
- Vendor metrics: "35% average increase in options sold", "4.3K+ live new-home communities" and "375K product assets" [VC]. A case-study page elsewhere says 15–30% [VC].
- Not tested: there is no public buyer portal.

**HomeByMe (Dassault).**
- 2D to 3D with "4K images" and a "catalog of branded products" [VC] https://home.by.me/en/
- Five locales, no Hebrew. Pinch-zoom is blocked on the landing page [LT]. `/en/start` returned 404 [LT].

**IKEA Kreativ.**
- LiDAR room scan (iPhone 12 Pro and later), erase furniture, 3D showrooms, and IKEA catalogue items [VC/PR].
- The US landing page loads fast: LCP 0.96 s [LT]. `/home-design/app/` returned 404 [LT].
- Not available in Hebrew. IKEA Israel is a franchise, and no Kreativ was found there.

**magicplan.** Scan or sketch on site, then estimate. It covers material quantities, labour and material costs, custom price lists (CSV) and a PDF report [RV] (Capterra and GetApp listings). It is the benchmark for **cost estimate output**. It has no interior design or 3D walk.

**Roomle (Rubens Room Designer).** Public demo [LT] https://www.roomle.com/t/cp/?configuratorId=mocdemo&id=3fx5c6u9bwyveh010jzuu2dsnbjxaqu&api=false&catalogRootTag=rubens_room_demo_root&locale=en&startInDetail=false&state.mode=catalog
- It shows a room in 3D, a categorised catalogue (named partner products such as Tom Dixon lighting), and 2D/3D, first-person, AR, snapshot, parts-list and save-draft controls, plus a cart button. See `evidence/roomle-room-demo-desktop.jpg`.
- Canvas at 13.3 s desktop and 4.9 s mobile in our rig; 7.9 MB; 440 requests. **Zoom is blocked** on mobile [LT].

**Rayon.**
- Multiplayer 2D plan editing with comments; DWG, DXF and PDF import and export; image tracing by AI [RV/VC] https://rayon.design/use-cases/collaborative-space-design
- Real-time infrastructure on Liveblocks [VC] https://liveblocks.io/blog/how-rayon-replaced-their-own-websocket-infrastructure-with-liveblocks-to-power-real-time-collaboration
- `app.rayon.design` failed to connect from our rig [LT].

**Floorfy.** 360 property tours with **built-in video calls**. The agent shares the tour live and takes measurements with the client, who joins by link with no install [VC] https://floorfy.com/products/videocall. Shared control by the client: unknown. No design editing.

**CPQ3D / London Dynamics.** Vendor blogs describe sending a link so that seller and customer "both edit the configuration … in real time" during a video call [VC] (search summary; outdoor structures). This is the only claim found of **co-controlled configuration over video**.

**Interior AI.**
- Photo restyle, virtual staging and "3d flythrough videos" [VC] https://interiorai.com/
- The landing page headline is "Fire your interior designer" (a trust signal of its own).
- 195 of 209 images lack alt text; LCP 7.5 s [LT].
- The output is images, not an editable model.

**RoomGPT.** Photo restyle; "4 million" users claimed [VC] https://www.roomgpt.io/. Login required. LCP 1.04 s [LT].

**Spacely AI.** AI renders for professionals, with a new "Team Canvas" [VC] https://www.spacely.ai/. Zoom is blocked [LT].

**ReimagineHome.** It claims to design "with real products available near you and within budget, without touching walls, windows, or doors", with add-to-cart on Amazon or Shopify [VC] https://www.reimaginehome.ai/. This is the only **structure-lock plus real-product plus budget** claim among the AI tools.

**Collov AI.** Virtual staging, furniture eraser, declutter and material overlay [VC] https://collov.ai/. 532 requests on the landing page [LT].

**Israel.**
- Muonovate (Hadera) describes buyers requesting tenant changes online, such as moving an outlet or choosing tiles, without visiting the developer [RV directory] https://startupim.com/company/muonovate
- REALS / Simplex 3D shows views, shading and nearby development before purchase [PR] https://www.multifamilydive.com/press-release/20250708-the-end-of-buying-blind-how-reals-is-redefining-pre-construction-sales/
- Israeli job ads for "מתאם/ת שינויי דיירים" (tenant-change coordinator) require AutoCAD and manual coordination [RV] https://www.drushim.co.il/job/38949395/e622195e/. This suggests that tenant changes are still run by hand at Israeli developers.

---

## 4. Cross-product observations

1. **Sign-in walls.** 4 of 6 deep editors require an account: Planner 5D (sign-up, and a ToS modal even for gallery 3D), Homestyler (sign-in), Coohom (account) and RoomSketcher (account). Only Floorplanner's demo and Higharc's buyer intro were operable anonymously. A buyer arriving from a project page would hit a wall in most tools.
2. **Nobody shows prices inside the visual.** Floorplanner shows finish names, Coohom lists products, and Higharc shows options, all with **no prices on screen**, as of 2026-11-10 [LT]. Prices exist only as vendor claims (Planner 5D Price Estimator, Higharc real-time pricing, GBuilder extra cost, Zonda).
3. **No Hebrew anywhere.** Across 16 landing pages, hreflang shows no `he` or `iw` [LT]. Homestyler is the only one offering an RTL language (Arabic).
4. **Mobile is an afterthought.** Floorplanner mobile is view-only. Coohom's mobile tour puts every control in the top-right corner. Higharc mobile was blank at 7.6 s. Homestyler, HomeByMe, Spacely and Roomle block pinch-zoom. No deep product's primary CTA sits in the lower half of the phone screen.
5. **Heavy payloads.** The first interior 3D view costs 12–21 MB in every product we could open: Floorplanner 21.1 MB, Coohom 15.2 MB, Higharc 11.8 MB (still loading). The Higharc intro made 1,000+ requests.
6. **Video plus co-design does not exist in one product.** Live co-editing exists (Planner 5D web, Coohom Elite, Rayon). Video exists in tours (Floorfy). Co-controlled configuration over video is claimed only by CPQ3D, outside housing.
7. **Developer plan integration exists only in US houses and Nordic apartments.** Higharc, Zonda and GBuilder each have it, with no Hebrew and no Israeli specification (מפרט) logic.

## 5. Screenshot index (evidence/)

| File | Shows |
|---|---|
| planner5d-editor-desktop.jpg | Editor URL becomes the sign-up wall |
| planner5d-12-open-in-3d.jpg | Gallery "Open in 3D" behind the ToS "I Agree" modal |
| homestyler-floorplan-desktop.jpg | Editor sign-in wall |
| homestyler-11-project-detail.jpg | Public design page (images only) |
| coohom-11-panorama.jpg / coohom-12-panorama-rotated.jpg | Path-traced 360 tour, desktop |
| coohom-13-panorama-mobile.jpg | Mobile tour; controls top-right |
| coohom-14-aiwalking.jpg | AI-walking tour with Product List, Floor Plan, Room Select |
| coohom-15-product-list.jpg | Product list: no prices, Chinese names leak |
| coohom-16-floor-plan.jpg | Minimap with viewpoint pins and view cone |
| coohom-17-room-select.jpg / coohom-18-more.jpg | Room picker, more menu |
| roomsketcher-live3d-desktop.jpg | Live 3D marketing: synced 2D plan and 3D window [SL] |
| floorplanner-01-2d.jpg … floorplanner-09-info.jpg | Full demo editor walk-through: 2D, room panel, objects, finishes, styleboards, 3D first-person, orbit |
| floorplanner-10-mobile.jpg | Mobile view-only editor |
| higharc-11-belmont.jpg | Builder plan page with "Design in 3D" |
| higharc-13-intro.jpg / higharc-14-intro-loaded.jpg / higharc-15-intro-orbit.jpg | Showroom intro: option rail, Exterior/Interior, 3D still loading |
| higharc-16-intro-mobile.jpg | Mobile intro blank at 7.6 s |
| roomle-room-demo-desktop.jpg / roomle-room-demo-mobile.jpg | Public room configurator demo |
| *-home-desktop.jpg / *-home-mobile.jpg | Landing pages used for the performance, CTA and accessibility metrics |
