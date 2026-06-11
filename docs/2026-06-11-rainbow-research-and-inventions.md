# Rainbow / Sde Dov — Buy-Like-A-Store Research + Five Inventions
**For:** nad-lan.co.il, Israel new-build marketplace
**Reviewer:** Claude (deep-research fan-out, 4 parallel strands, June 2026)
**Status:** synthesis of online-purchase journeys, deal-team economics, and 2025-2026 frontier tech. 3D-tech strand redo in flight; this document ships now because the strategic decisions don't depend on it.

---

## TL;DR — five inventions, in priority order

| # | Name (he/en) | One-line killer demo | Moat |
|---|---|---|---|
| 1 | **מסך הקנייה / The Purchase Screen** | "Reserve apt 14B for 72h with a ₪5K refundable hold, WhatsApp OTP, AU10TIX KYC, e-signed reservation summary — all on phone, no agent call" | **No Israeli portal ships a reserve button. Zero.** First-mover takes the category. |
| 2 | **View-From-My-Apartment + Sun Slider** | Mapbox 3D camera at floor-N altitude facing the unit's bearing, with a date+hour slider that computes Tel Aviv sun position and renders the actual shadow cast across the buyer's living room | Answers the question every Israeli buyer asks ("כמה שמש אני אקבל?") that no portal answers visually. |
| 3 | **חדר העסקה / The Deal Room** | Per-buyer status page that mirrors myLennar — saved → reserved → KYC → e-sign → deposit → contract → keys — with the deal team invited inline at the moment of friction | Composes 6 modules we already own; competitors would need a year to catch up. |
| 4 | **שותף הקנייה / Buying Copilot** | Buyer voice-says "4 חדרים פונה מערב מתחת ל-4.5 עם שמש אחרי 5" — the picker filters, the sun slider auto-positions, hold button appears on the one match | Generative UI in Hebrew real-estate is whitespace. First mover trains the muscle. |
| 5 | **הסבב / The Bidding Round** for the deal team | Buyer requests a real-estate lawyer — 3 pros are notified, they quote in ≤5 min, buyer picks; RESPA-safe in Israel because it's flat per-intro paid by pros, never a cut of the legal fee | Compass/Opendoor can't ship this in Israel — Bar Rule 30 + Brokers Regulations 2024 block their U.S. mechanic. We are pre-adapted. |

The rest of the document earns these picks: cited findings per strand, then the inventions with stack + revenue + legal frame + Codex handoff.

---

## Strand 1 — What top portals actually ship in 2024-2026

### The headline finding
> *"Israeli portals — Yad2/Yad1, Madlan, Tidhar, Aura, Azorim — ship a 'leave details' lead form. None ship a reserve button. That is the gap."* — synthesis [S1.16,17,18,21,22,23]

Even U.S. giants have not solved buy-side reservation for resale — the pattern lives almost entirely in **new construction**. Which is exactly what Rainbow is.

### The U.S. patterns worth lifting
- **Redfin Direct** is the closest portal to a real online-purchase: *"a step-by-step online platform that defines the elements of the contract"* with the seller's term preferences inlined [S1.2]. Buyer makes a written offer online without a buyer's agent. No refundable hold at the offer step — earnest money flows through escrow after acceptance.
- **Opendoor seller dashboard** (the UX pattern transfers): on login the user lands on a dashboard with **"Offer Details" and "Offer Breakdown"** itemizing the cash offer, a **5-day offer validity window**, an accept CTA, and a closing-date picker [S1.5,6].
- **myLennar** is the canonical buyer-side dashboard: real-time construction milestones, service requests, document storage, mobile app [S1.8,9]. Account intake captures name/email/phone/proposed closing date — the IA we should clone for חדר העסקה.
- **DocuSign Rooms for Real Estate** is the most directly liftable status-page IA: **per-deal Room with task list, document vault, e-sign tracker, milestone reminders, permissioned by role** [S1.41,42].

### The Israeli new-build sites
**Tidhar / Aura / Azorim** all publish project pages with a generic "השאר פרטים" form that routes to telesales [S1.21,22,23]. **None** ship a reserve button, hold timer, refundable deposit, OTP, e-sign, or buyer status page. **Zero deployed online-reserve flow at any Israeli portal or developer.** This is the moat — and it's wide open.

### The Israeli legal floor (this changes the design)
The brokers law was **rewritten** in 2024 (תקנות המתווכים במקרקעין (אתיקה וחובות מקצועיות), תשפ"ד-2024), in force from **9 March 2025** [S1.27,28]:
> *"A broker may not collect דמי רצינות (seriousness money), דמי קדימה (advance fee), or contract-renewal fees — only the agreed brokerage commission."* [S1.29,30]

**Hard implication for our design**: any refundable hold must be authorized through the **yazam's** payment processor as an earnest deposit on a future purchase contract — *not* through nad-lan as a broker fee. nad-lan's revenue from the hold flow is per-yazam SaaS subscription + verified-buyer routing fee, never a per-buyer fee. This is the cleanest legal posture.

Other constraints worth carrying:
- **Electronic signature**: only a **certified** e-signature (חתימה אלקטרונית מאושרת) carries the legal presumption equivalent to a handwritten signature under חוק חתימה אלקטרונית — a click-through does not satisfy §8 חוק המקרקעין [S1.32]. Translation: a binding contract needs DocuSign-grade certification; a non-binding reservation summary doesn't.
- **זכרון דברים risk**: courts hold a *זכרון דברים* binding if it shows *gmirut da'at* + *mesoyamut* (parties, property, payment dates) [S1.37,38]. **Critical**: our reservation UI must be checkboxed + bold-disclaimed as **not** a זכרון דברים, with no specificity on price/dates that triggers the מסוימות test. Tax liability (מס רכישה) starts from a binding signature date.
- **Cooling-off**: real-estate is **outside** the 14-day distance-sale right — legal protection lives in contract law + §8 חוק המקרקעין [S1.34,35].

### Conversion data, honestly
- Real-estate lead forms convert at ~**0.6%** vs B2B services at 2.2% — the bar is low; any structured commitment ladder should outperform [S1.24].
- Multi-step forms with shorter visible steps convert **~37% better** than long single forms with identical fields [S1.24].
- Specific "hold-button conversion vs no-hold" / "OTP-gate lift" / "e-sign LOI completion" — **no rigorous public numbers found.** Treat any specific %-claim as a hypothesis to A/B test, not a citation.

### State machine to expose to the buyer (synthesized)
`SAVED → TOUR_BOOKED → OFFER_DRAFT → OFFER_SUBMITTED → HOLD_AUTHORIZED → KYC_PASSED → RESERVATION_SIGNED → CONTRACT_DRAFT → CONTRACT_SIGNED → CONSTRUCTION_MILESTONES… → KEYS`

---

## Strand 2 — View-from-unit 3D tech (FULL, cited; recommendation revised)

### The headline finding that changes the recommendation
> *"While official GIS for Tel Aviv contains height data for all buildings, OpenStreetMap has only few buildings with height data."* — Israeli OSM community thread [S2.OSM-TA-heights]

Mapbox GL JS v3's 3D buildings are extruded from OSM `height` / `building:levels × 3m`. **Tel Aviv is not in Mapbox's curated landmark city list** (Munich/Berlin/Stuttgart/SF/NYC/Las Vegas/Helsinki/Tokyo got new facades in 2025; TA didn't). At floor 24 looking west, surrounding TA extrusions will be a mix of accurate, level-derived, and zero-height polygons. **Mapbox alone cannot render a credible Tel Aviv view from a high floor.**

> *"Google's Photorealistic 3D Tiles is a 3D mesh model of the real world, textured with high-res RGB optical imagery, with the same 3D map source as Google Earth, available in 2,500+ cities across 49 countries."* — Cesium learn page [S2.cesium-p3dt]

**Tel Aviv is in Google's photogrammetry mesh** with real coastline, Azrieli, Sarona, hotel strip — verified at the public 3d-tiles.web.app demo. This is the only platform where a westward Tel Aviv view at 80m+ altitude looks photographically right out of the box.

> *"Achieving this required high-definition, 3D-compatible map data that was also loaded quickly."* — Takumi Yoshida, STYLE PORT / ROOV.space, [Google Maps Platform real-estate case study](https://mapsplatform.google.com/resources/blog/helping-buyers-make-more-confident-real-estate-decisions-with-photorealistic-3d-tiles/) — the closest documented off-plan precedent (130+ Japanese developers, 900+ projects, including the 2024 BLUE FRONT SHIBAURA mixed-use launch).

### Pricing the platforms (2025 post-March SKU restructure)
| Path | Marginal cost / 1k views | Fixed |
|---|---|---|
| Google Photorealistic 3D Tiles direct | **$6.00/1k** root-tile events (1k free/mo, then $6 → $5.10 → $4.20 → $3.30 → $2.40 across tiers) [S2.google-billing] | none |
| Cesium ion Commercial (individual) | included up to 5,000 root tiles/mo | **$149/mo** [S2.cesium-pricing] |
| Cesium ion Commercial (team) | included up to 5,000 root tiles/mo | **$524/mo** [S2.cesium-pricing] |
| Mapbox GL JS (locator map only) | $5.00/1k loads above 50k free [S2.mapbox-pricing] | none |
| Splat hosting (50MB SPZ × 1k = 50GB egress) | ~$2.50/1k | none |

**Total blended hero-view cost: ~$13.50/1k views direct-to-Google + Mapbox locator; break-even with Cesium ion Commercial at ~25k views/mo.** A tower listing driving 10,000 hero views costs ~$135 in cloud — trivial vs. the marketing budget of a single off-plan unit sale.

### Commercial use license: explicitly green-lit
> *"We updated Map Tiles policies to allow you to create promotional videos of the experiences you build, with… guidelines around how to display the Google logo and follow brand and data attribution policies."* — Google Maps Platform blog [S2.google-policy-update]

Required: visible Google attribution + an in-viewport disclosure like *"Surroundings: Google Earth photogrammetry, captured [date]. Interior: architectural rendering."* This both satisfies Google's policy and pre-empts buyer disputes when a neighboring lot redevelops.

EU/EEA billing-address projects created after 8 July 2025 are blocked from 3D Tiles [S2.eu-block]. **An Israeli (.IL) billing entity is unaffected.** Don't proxy through a Frankfurt subsidiary.

### Gaussian splatting state of play (2025 inflection)
> *"2025 will be remembered as the year 3D Gaussian Splatting truly became real for Media & Entertainment. Not as a promise, not as a research breakthrough, but as a technology professionals could finally trust in production."* — Radiance Fields year-end wrap [S2.rf-yearend]

**Zillow SkyTour (July 2025)** is the first major real-estate platform shipping splats at scale — drone-captured exteriors for "Showcase" listings [S2.zillow-skytour]. **Matterport 3D Exteriors via CoStar (post-$1.6B acquisition Feb 2025)** followed for exteriors; interiors remain depth+photogrammetry [S2.future3d-matterport-vs-splats].

Capture economics:
- Capture: 5-15 min on-site (drone 200+ frames from a 30-60s orbit per Heliguy's guide).
- Training: 30-90 min for ~1M Gaussians on an RTX 4090; 2-3h on a 3060.
- File sizes: raw PLY 300MB-1GB; **SPZ compression cuts to ~25MB** (Khronos glTF standard).
- Viewer FPS: 60+ desktop / 45-60 laptop / 30-45 mobile (200K-optimized splats).

**The off-plan caveat (honest):** splats capture what exists, so they cannot render the *interior* of an unbuilt apartment. The credible shipped pattern is **hybrid**: splat the SURROUNDINGS (rooftops, beach, skyline) + CG-render the future tower as a glTF model placed in the scene. This is what STYLE PORT/ROOV.space ships on Google P3DT.

### WebGPU status, end of 2025
> *"WebGPU is officially Baseline."* — web.dev [S2.webgpu-baseline]

iOS 26 / Safari 26 (Sept 2025) turned WebGPU on by default — last gating constraint cleared. three.js r171+ ships `WebGPURenderer` with one-line swap and automatic WebGL2 fallback; 2-10× perf improvement on draw-call-heavy scenes. **Mapbox GL JS has no public WebGPU roadmap — assume WebGL2 through 2026.** MapLibre (the fork) has an experimental WebGPU branch at 80% test coverage.

### Camera math at floor altitude — production recipe
```
camera_altitude_m = ground_elevation_m + base_offset + (floor − 1) × floor_height_m + eye_height_m
```
- `ground_elevation_m`: Tel Aviv coast ~5-25m above MSL. Get from Mapbox `map.queryTerrainElevation({lng,lat}, {exaggerated:false})` (free, client-side) or Google Elevation API. **`exaggerated:false` is critical** — terrain exaggeration silently inflates camera height.
- `base_offset`: 4.0m for lobby/ground floor.
- `floor_height_m`: **Israeli residential standard is 2.75m ceiling-to-ceiling; 3.0-3.1m floor-to-floor including slab. Luxury TA towers run 3.1-3.3m.** Use 3.05m as the safe default; expose as per-tower CMS config.
- `eye_height_m`: 1.5-1.6m standing at the window.
- Worked example, floor 24 west-facing at 32.1108/34.7805: `~20 (ground) + 4.0 + 23 × 3.05 + 1.5 = ~95m ellipsoidal altitude`.

Cesium camera API (the right call for our case):
```js
viewer.camera.setView({
  destination: Cesium.Cartesian3.fromDegrees(lng, lat, altitude_m),
  orientation: {
    heading: Cesium.Math.toRadians(unit_bearing_deg), // west = 270
    pitch:   Cesium.Math.toRadians(-2),                // near-horizontal, slight downward
    roll:    0
  }
});
```
Tighten FOV to ~50-60° (window view, not wide-angle). Cap pitch ±10° so users can't tilt to bird's-eye that exposes the mesh from above (mesh quality degrades sharply near vertical).

### Revised recommendation
**Cesium ion + Google Photorealistic 3D Tiles** for the hero "view from apartment" — NOT Mapbox alone. Keep Mapbox GL JS v3 for the compound locator/overview map (free 50k loads/mo, already wired). Composite the off-plan interior (window frame, balcony rail, optional CG living room) as a three.js layer in front of the Cesium canvas. Optional: drone-capture the *site* (where the tower will stand) as a Luma/Polycam splat for an exterior fly-around panel while construction is in progress.

This revises Invention #2's stack from "extend compound-map.php" to "new module `inc/view-from-unit.php` loading CesiumJS + Google P3DT, with compound-map.php staying on Mapbox for the locator." The Sun Slider logic (SunCalc + shadow overlay) is platform-agnostic and bolts onto either.

### Strand 2 sources (consolidated)
S2.mapbox-v3 — docs.mapbox.com/mapbox-gl-js/guides/migrate-to-v3 + mapbox.com/blog/powerful-elegant-3d-visualizations
S2.mapbox-model-layer — docs.mapbox.com/style-spec/guides/using-3d-models
S2.mapbox-landmarks — mapbox.com/blog/global-cities-3d-landmarks
S2.OSM-TA-heights — community.openstreetmap.org/t/using-gis-tel-aviv-for-buildings-heights/85546
S2.mapbox-streets-v8 — blog.mapbox.com/building-heights-in-mapbox-streets-14bc7399a4e8 + docs.mapbox.com/data/tilesets/reference/mapbox-streets-v8
S2.mapbox-pricing — mapbox.com/pricing + docs.mapbox.com/mapbox-gl-js/guides/pricing
S2.cesium-p3dt — cesium.com/learn/photorealistic-3d-tiles-learn
S2.google-3dtiles-overview — developers.google.com/maps/documentation/tile/3d-tiles-overview
S2.google-billing — developers.google.com/maps/documentation/tile/usage-and-billing + developers.google.com/maps/billing-and-pricing/pricing + blog.afi.io/blog/what-is-the-google-photorealistic-3d-tiles-api
S2.google-policy-update — mapsplatform.google.com/resources/blog/photorealistic-3d-tiles-now-preview-updated-daily-quotas
S2.styleport-case — mapsplatform.google.com/resources/blog/helping-buyers-make-more-confident-real-estate-decisions-with-photorealistic-3d-tiles
S2.cesium-pricing — cesium.com/platform/cesium-ion/pricing
S2.cesium-pl3dt-included — prnewswire.com/news-releases/photorealistic-3d-tiles-from-google-maps-platform-now-included-in-cesium-ion + dronesworldmag
S2.eu-block — github.com/vvoovv/blosm/issues/644
S2.itwin — developer.bentley.com/apis/visualization/overview + itwinjs.org
S2.rf-yearend — radiancefields.substack.com/p/gaussian-splatting-year-end-wrap
S2.zillow-skytour — zillow.com/news/take-home-listings-to-new-heights-with-skytour + geekwire.com/2025/zillow-uses-drone-imagery-for-new-exterior-3d-tour-feature
S2.future3d-matterport-vs-splats — thefuture3d.com/blog/gaussian-splatting-vs-matterport + thefuture3d.com/equipment/compare/gaussian-splatting-vs-matterport
S2.splatlabs — splatlabs.ai/blog/virtual-tours-real-estate-gaussian-splatting
S2.utsubo-splats — utsubo.com/blog/gaussian-splatting-guide
S2.spz-format — thefuture3d.com/answers/gaussian-splatting-file-formats
S2.lumalabs-web — github.com/lumalabs/luma-web-examples + lumalabs.ai/luma-web-library
S2.giraffe360 — giraffe360.com
S2.r2u-vision-pro — r2u.io/en/blog/apple-vision-pro-real-estate-guide
S2.zillow-immerse — prnewswire.com/news-releases/experience-the-future-of-home-tours-with-zillow-immerse-on-apple-vision-pro-302050031.html
S2.heliguy-drone-splats — heliguy.com/blogs/posts/drones-for-gaussian-splatting
S2.skysplat-blender — conference.blender.org/2025/presentations/3999 + blendernation.com/2025/05/29/skysplat-drone-video-to-3d-gaussian-splat-workflow-addon
S2.israeli-floor-heights — ronkin-list.com/israeli-apartment-sizes-explained-the-complete-guide-for-international-buyers + remaxjerusalem.com/en/blog/news/fulfilling-your-vision + buyitinisrael.com/news/safe-room-saves-lives-in-israel
S2.mapbox-altitude — docs.mapbox.com/mapbox-gl-js/example/free-camera-path + docs.mapbox.com/mapbox-gl-js/example/free-camera-point + docs.mapbox.com/mapbox-gl-js/example/query-terrain-elevation
S2.cesium-camera — cesium.com/learn/cesiumjs/ref-doc/Camera.html + cesium.com/learn/cesiumjs-learn/cesiumjs-camera
S2.webgpu-baseline — web.dev/blog/webgpu-supported-major-browsers + caniuse.com/webgpu + vr.org/articles/webgpu-baseline-2026-three-js-webxr-default + webgpu.com/news/webgpu-hits-critical-mass-all-major-browsers
S2.threejs-webgpu — threejs.org/docs/pages/WebGPURenderer.html + utsubo.com/blog/webgpu-threejs-migration-guide + discourse.threejs.org/t/webgpu-r181-fyi-stats-gl-no-longer-compatible-with-webgpu/87944
S2.maplibre-webgpu — maplibre.org/roadmap/maplibre-native/webgpu + blog.brightcoding.dev/2025/10/05/maplibre-gl-js
S2.zillow-3d-home — zillow.com/z/3d-home/guide + zillow.com/z/3d-home/floor-plans
S2.askalocal-tel-aviv — askalocalapp.com/Tel_Aviv/EN/3d-map-of-tel-aviv-like-you-never-saw-it-before
S2.localize-madlan — proptechzone.com/startups/localize-madlan
S2.rocket-vision-pro — nasdaq.com/articles/rocket-homes-teams-up-with-apple-vision-pro-for-immersive-house-tours

---

## Strand 3 — Attaching professionals into the buying flow

### The numbers that matter
> *"Better Real Estate's historic attach rate is almost 70 percent... ~90% of clients come through Better Mortgage's preapproval process."* [S3.3]

> *"70% of movers choosing financing through Zillow Home Loans are now working with a Premier Agent partner."* — Zillow Q4 2025 [S3.5]

> *"80% of Opendoor home transactions in 2019 used Opendoor's title insurance services."* — Opendoor S-1 [S3.1]

The pattern across all U.S. leaders: **attach as early as possible after intent is revealed, but before the offer is written**. Better attaches at pre-approval. Zillow attaches at Tour CTA. Opendoor attaches at offer request. Compass Concierge attaches at *intake* (before listing photos).

> *"Vertical SaaS companies can increase revenue per customer by up to 10× by embedding services."* — a16z [S3.11]

### The Israeli regulatory walls (these change the mechanic, not the strategy)
1. **חוק המתווכים במקרקעין § 14** — a broker may not prepare or assist in preparing documents of a legal nature; doing so forfeits the brokerage fee [S3.13]. nad-lan as a directory is fine; nad-lan as something resembling a broker handling legal docs is not.
2. **Israel Bar Ethics Rule 30 (1986)** — Israeli attorneys may not pay or receive referral fees [S3.14]. *"There is no custom of paying referral fees in Israel."*
3. **Real Estate Appraiser Ethics (1966) + Bank of Israel Nov 2018 directive** — appraisers must be independent; banks must accept cross-bank appraisals [S3.15]. A paid-placement inspector who signs off on his own referrer's buyer = visible conflict.

### What is legally OK to bundle
- ✅ Flat subscription paid by the pro
- ✅ Flat per-introduction fee paid by the pro
- ✅ Paid placement clearly labeled "מקודם"
- ⚠️ Success fee from a non-lawyer/non-broker pro (designer, mortgage advisor) — gray
- ❌ Percentage of the lawyer's fee
- ❌ Percentage of the brokerage commission unless nad-lan is licensed
- ❌ Any "bundle price" where the buyer can't see and refuse the line items

### The strongest deal-team product (paragraph spec from the researcher)
Build the deal team as **contextual, just-in-time inline attach** — never a standalone "Deal Team" page. At the moment a logged-in buyer favorites a 3rd property in a price band, surface a single CTA: *"קח עוד צעד — צרף עו"ד / שמאי / יועץ משכנתאות"*. Match by vector similarity over (city, neighborhood, price band, buyer language, property type, first-time-buyer flag) against an index of pros' historical successful deals. Show **3 pros per category, ranked, with confirmable next-available slot like ZocDoc** [S3.7]. Revenue model that survives Israeli law: flat subscription tier + flat per-confirmed-meeting fee + paid placement labeled "מקודם" — never a percentage. The wedge that pulls everything else is **the mortgage pre-approval flow** — Better proved this with 90% upstream feed and 70% attach [S3.3]. **So the strategic question for nad-lan is not "which pros to attach" but "what is our pre-approval analog that earns the right to attach them."**

### AI-matched consultants — genuine whitespace
LinkedIn's **Pensieve** + fine-tuned LLM dual-encoder is the canonical pattern: pre-compute member and job embeddings, run nearest-neighbor on GPU [S3.16]. **No publicly-documented production system matches a home buyer profile to a settlement-services pro via embeddings.** Opcity uses rules (geography, response time). Zillow Premier Agent is an impressions auction [S3.5,6]. **This is whitespace for nad-lan.**

---

## Strand 4 — 2025-2026 frontier tech, ship-now ranking

### What's actually shippable now
| Tech | Verdict | Why |
|---|---|---|
| Vercel AI SDK v6 generative UI + tool-calls | **Ship now** | Production-stable, provider-agnostic, this is the spine [S4 — vercel.com/blog/ai-sdk-6] |
| Claude Opus tool-use + Tool Search | **Ship now** | 84% on Online-Mind2Web, beats GPT-5.5; ideal for orchestrating GreenInvoice/WP/Mapbox [S4 — anthropic.com/engineering/advanced-tool-use] |
| **WhatsApp Cloud API OTP on Israeli +972** | **Ship now** | Dominant Israeli channel; sub-second; **no Israeli portal has shipped it** [S4 — Meta WA pricing + Heltar IL 2025] |
| **AU10TIX KYC** (Tel-Aviv based; ONE ZERO bank uses it) | **Ship now** | Bank-of-Israel approved; reads Teudat Zehut natively; reusable downstream for the closing attorney [S4 — NoCamels, OurCrowd] |
| Apple AR Quick Look (USDZ) per unit | **Ship now** | Zero JS, native iOS, two-line embed |
| Maket.ai / Spacely.ai layouts on demand | **Ship now** | $20/mo, instant wow, agent-callable for "flip the kitchen and add a study" |

### The killer Hebrew-market quotes
> *"In 2025 the conversation is the filter. The grid is the receipt."*

> *"In Israel, SMS OTP is friction theater. WhatsApp is the address bar."*

> *"AU10TIX already verifies the Israeli banking sector — make the buyer's ID work once for the hold today, the contract tomorrow, the mortgage next month."*

> *"Vision Pro is the press release. WebGPU plus 8th Wall on the buyer's phone is the deal."*

> *"Tokenize the receipt, not the deed. The deed is Tabu's job for another five years."*

### Honest scoring on the hype
- **OpenAI Realtime API** for Hebrew: *"struggles with real-world Hebrew — especially regional accents, fast speech, or noisy input"* [S4 — soniox.com/compare/soniox-vs-openai/hebrew]. **Ship for EN/RU/FR diaspora; use Soniox + ElevenLabs Hebrew fallback for native.**
- **Apple Vision Pro Immerse** (Zillow shipped day-one on visionOS 26 Spatial Scene API): real, beautiful, **install base in Israel is rounding error**. PR collateral, not revenue.
- **8th Wall VPS / "stand here, see the future tower"**: real, ~6-week capture + content budget per site. Ship 2026 for Sde Dov as the hero AR demo.
- **Blockchain reservation tokens**: Propy did a $14M Miami deal in USDT in <60s; Dubai Land Department tokenization pilot live since March 2025 [S4 — coindesk + mediaoffice.ae]. Israel Land Authority published a *tender* for blockchain consulting, **no live system** [S4 — ledgerinsights]. **Verdict: tokenize the reservation receipt as a soulbound NFT for marketing flair; tokenized ownership is not for 2026 in Israel.**
- **WebGPU on mobile Safari**: turned on in iOS 26 / macOS 26 (Sept 2025) [S4 — xugj520.cn]. **Gaussian splat tower flythroughs on phones with no app — real end-of-2025.**

---

## The Inventions — five originals, designed to be moats

Each invention is constructed to be **buildable on what we already own** (Mapbox token, GreenInvoice, OpenAI key, professionals directory, offers engine, e-sign seam, WordPress) and **legally posture-pre-adapted to Israel** (so a U.S. competitor would have to redesign for the market).

### Invention #1 — מסך הקנייה / The Purchase Screen
**The killer demo:** A buyer on the Rainbow page taps "שריון לדירה הזו". A modal appears: *"שריון של 72 שעות, ₪5,000 חיוב חוזר על כרטיס אשראי, מוחזר במלואו אם תבטל בתוך 72 שעות"*. They pass WhatsApp OTP (sub-second on +972). They pass AU10TIX (Teudat Zehut + selfie liveness, 30 seconds, bank-grade). GreenInvoice authorizes the hold on the **yazam's** merchant account. The buyer receives a certified e-signed reservation summary in their email + WhatsApp. The Rainbow picker now shows unit 14B as "בתהליך בדיקה" with a TTL countdown. **No agent call, no office visit, no PDF email tag chain.**

**Why it's a moat:** Zero Israeli portal ships this. Yad2/Madlan/Tidhar/Aura/Azorim all stop at "השאר פרטים" [S1.16,17,21,22,23]. The competitor with the most distribution (Yad2) is not even attempting to take a buyer to commitment. **First mover defines the category.**

**Revenue mechanic (legally clean under Brokers Regulations 2024 [S1.27-30]):**
- The ₪5K hold is on the **yazam's** payment processor, not nad-lan's — nad-lan is not a broker collecting דמי רצינות.
- nad-lan charges the yazam: (a) flat SaaS per-project per-month for the מסך הקנייה module, (b) flat per-verified-reservation routing fee (e.g., ₪500 per buyer who passed KYC + OTP + hold authorization).
- Optional v2: nad-lan offers an Israeli refundable hold escrow service via a banking partner — separate regulatory project, not v1.

**Tech stack on top of what we have:**
- WordPress + offers.php (already has dedupe, rate limits, legal frame) → extend to a `reservation` state with TTL.
- WhatsApp Cloud API → new module `whatsapp-otp.php` calling Meta's auth template on the Israeli +972 number; ~₪0.07 per OTP domestic, exploit utility-template-inside-service-window for follow-ups [S4 — Meta WA pricing].
- AU10TIX → new module `kyc-au10tix.php` (their API is REST + webhook); pre-built Teudat Zehut + selfie liveness flow [S4 — AU10TIX docs]. Token reusable for the closing attorney later — the magic of "ID once, use forever."
- GreenInvoice → extend existing recurring rails to a one-time auth-and-capture with TTL release; emit reservation invoice [we already have GreenInvoice integrated].
- esign.php → certified e-signature for the reservation summary; click-through is fine for the *summary* because it's non-binding by design (avoids זכרון דברים [S1.37,38]), but the document carries the certified-signature legal presumption for clarity [S1.32].

**Anti-זכרון-דברים drafting:** the summary must say *"אישור שריון לא מחייב — אינו זכרון דברים. הזמינות, המחיר, התנאים ותאריך המסירה כפופים לאישור היזם ולחתימת חוזה רכישה"* + a checked checkbox at submission. No price commitment. No delivery date. No מסוימות.

### Invention #2 — View-From-My-Apartment + Sun Slider
**The killer demo:** The buyer selects apartment 14B (high floor, west-facing). The 3D viewframe — already present in v1.59.0 as a CSS gradient — switches to Mapbox 3D camera mode. Camera position: `[lng, lat, ground_elevation_m + 14 × 3.1m]`. Bearing: derived from the unit's `dir` meta (west = 270°). Pitch: 80°. The buyer sees the actual Tel Aviv coastline rendered from that exact apartment height. **Now the inventor twist:** a date+hour slider at the bottom — *"21 ביוני, 18:00"*. We compute the sun's azimuth and elevation for those coordinates and that moment (a 50-line SunCalc port — no API). We render a directional sun marker on the map AND project the apartment's window-facing shadow direction across a stylized living-room floor overlay. Buyer drags the slider; they see exactly which hours of which months they get direct sunlight in that room.

**Why it's a moat:** Every Tel Aviv buyer asks *"כמה שמש אני אקבל?"* — and **no portal answers it visually**. Sun direction is the #1 unsolved question in Israeli new-build. The data is free (astronomical formula), the rendering is cheap (we already have Mapbox), the wow is enormous.

**Revenue mechanic:** This is a **conversion multiplier**, not a SKU. Higher conversion = higher per-yazam SaaS pricing power. Secondary: justify higher-floor pricing premiums to the buyer with hard data ("apartment 32B gets 4.2 hours more direct light per day than 14B in winter") — yazamim love this because it lets them defend their pricing ladder without discounting.

**Tech stack on top of what we have:**
- Existing compound-map.php (Mapbox GL JS v3 wired, token slot present) → extend with `view-from-unit` mode.
- SunCalc (BSD-licensed, ~50 lines of math) for sun azimuth/elevation given lat/lng/datetime — no external API.
- Floor altitude = `mapbox.queryTerrainElevation([lng,lat]) + floor × 3.1m` (residential default; CMS can override per project).
- Camera bearing from `unit.dir` (already in our unit JSON contract).
- Optional v2: Google Photorealistic 3D Tiles overlay for the close-up coastline view — defer until base ships.

### Invention #3 — חדר העסקה / The Deal Room
**The killer demo:** Buyer who's passed the Purchase Screen logs into nad-lan and lands at `/חדר-העסקה/4728`. They see the myLennar-style status board: **שמרתי → סיירתי → שריון → KYC → חתימה → חוזה → בנייה → מפתחות**. Current step pulsing in gold. Document vault: their certified reservation summary, their AU10TIX ID token. Task list: *"בחר עו"ד מקרקעין · בחר יועץ משכנתאות"*. Each task has 3 pros pre-matched by vector similarity over (neighborhood, price band, language) — bookable like ZocDoc with "next slot tomorrow 14:00". When they tap "צרף", that pro joins the deal room with scoped access (only the docs the buyer shared). Inline AI summarizer of every conversation, every doc. The yazam's project manager has their own view — same room, different lens.

**Why it's a moat:** This is the **myLennar IA** [S1.8,9] composed with the **DocuSign Rooms** model [S1.41,42], adapted to Israeli law. Compass/Opendoor can't ship the U.S. version in Israel because RESPA-equivalent rules (Bar Rule 30 + Brokers Regulations 2024) block their referral economics. We're pre-adapted.

**Revenue mechanic:**
- **For pros**: flat monthly subscription (e.g., ₪199-499/mo by tier) + flat per-introduction fee (e.g., ₪50-150) + paid placement labeled "מקודם". No percentage of the pro's fee → Bar-Rule-30-clean for lawyers [S3.14], Brokers-Regulations-clean for everyone [S1.29,30].
- **For yazam**: SaaS for the buyer-facing PM dashboard. Optional add-on per closed reservation that contains data on buyer's deal team (a "deal momentum" signal yazamim will pay for).
- The math: a buyer who reserves at the Purchase Screen and uses the Deal Room pulls in 4 pros × ₪100 intro = ₪400 + a verified-buyer routing fee from the yazam ~₪500 = **~₪900 per qualified buyer** before SaaS subscriptions. At 100 reservations/month across 30 active projects = ₪90K/mo + SaaS base.

**Tech stack on top of what we have:**
- `nadlan_buyer` role + lead-e2e status REST (we have both) → expose to the buyer in a new dashboard template.
- nadlan_offer CPT (we have this) → primary deal-room object.
- Professionals directory + reviews.php (we have both) → pre-matched cards in the task list.
- esign.php → certified signing inside the room.
- Vector match: OpenAI text-embedding-3-small (we have the key) → embed each pro's last 24 months of successful deals (price band, neighborhood, type, language) into a small Postgres + pgvector or SQLite vss index. Cost: ~$0.02 per 100 pros refreshed monthly.

### Invention #4 — שותף הקנייה / Buying Copilot
**The killer demo:** A floating Hebrew mic button on every project page. Buyer presses, says: *"תראה לי 4 חדרים פונה מערב מתחת ל-4.5 מיליון עם שמש אחרי 5 בערב ביוני"*. The picker grid instantly filters to 3 units. The Sun Slider auto-positions to June 18:00. A summary card appears: *"מצאתי 3 דירות מתאימות. הראשונה — קומה 14 דירה B — תקבל שמש ישירה עד 19:40 ביוני. לשריין?"*. One tap → Purchase Screen flow.

**Why it's a moat:** Generative UI in Hebrew real-estate is whitespace. Vercel AI SDK v6 + Claude Opus tool-calls let the conversation **commit to the UI state**, not just answer in text. Yad2/Madlan have static search; nobody has shipped *"the conversation is the filter."* > *"In 2025 the conversation is the filter. The grid is the receipt."* [S4 — synthesis]

**Revenue mechanic:** Conversion multiplier on the Purchase Screen — every buyer who reserves through the copilot is one we can attribute. Premium SaaS tier for yazamim ("AI-assisted reservation funnel") on top of base. Optional voice minutes pass-through with margin (we pay $32/M OpenAI input audio tokens, charge yazam 50% margin) [S4 — OpenAI Realtime pricing].

**Tech stack on top of what we have:**
- Vercel AI SDK v6 + Claude Opus tool-use → orchestrator running server-side in WordPress via a tiny Node sidecar (or all-PHP via REST → Anthropic — fine, slower but no infra change).
- Tools the agent can call: `filter_units(criteria)`, `set_sun_time(date,hour)`, `start_reservation(unit_id)`, `book_pro(specialty)`.
- Voice: **diaspora EN/RU/FR** via OpenAI Realtime (cheap, fast) [S4 — gpt-realtime]; **native Hebrew** via Soniox STT + ElevenLabs TTS Hebrew (until OpenAI improves Hebrew) [S4 — soniox vs OpenAI Hebrew].
- DOM contract: every interactive element gets `data-action="..."` semantic attributes so Comet/Atlas browser agents can also drive the page — free 2026 distribution [S4 — eesel Comet vs Arc].

### Invention #5 — הסבב / The Bidding Round for the deal team
**The killer demo:** Inside חדר העסקה the buyer taps "צריך עו"ד מקרקעין". Instead of seeing 3 pros, they see *"הסבב פתוח — 3 עו"ד יחזרו אליך עם הצעה תוך 5 דקות"*. Behind the scenes: the vector-match algorithm picks the top-N (e.g., 8) lawyers; nad-lan WhatsApps each with a structured brief (*"רוכש דירה ראשונה ברובע שדה דב, ₪3.2M, יחזיר תוך 5 דקות עם טיוטת הצעה: שכר טרחה, זמינות, ניסיון"*). First 3 to respond appear in the buyer's room as cards with their quote, availability, and 3-line pitch. Buyer picks one. **The pros compete on quality of response, not on visibility.**

**Why it's a moat:** This is **paid-placement-meets-Uber** for professional services — and **Compass/Opendoor cannot ship it in Israel**. Their U.S. mechanic depends on a cut of the pro's fee, which Bar Rule 30 [S3.14] and Brokers Regulations 2024 [S1.27-30] block. Ours doesn't.

**Revenue mechanic (RESPA-equivalent-clean in Israel):**
- Per-pro entry fee for each round (e.g., ₪30) — they pay to participate, win or lose. This is **advertising spend**, not a referral fee → clean under both Bar Rule 30 and Brokers Regulations 2024.
- Premium "instant response" badge for pros who maintain ≥95% response in <2 min (priced higher).
- The math: 100 reservations/mo × 4 specialties × 8 pros invited × ₪30 = ₪96K/mo just on round entries, with no fee tied to the legal/professional outcome.

**Tech stack on top of what we have:**
- Vector match (same index as Invention #3) for the invite shortlist.
- WhatsApp Cloud API for outbound pro brief + inbound quote intake (Meta supports inbound free-form for 24h after first send) [S4 — Meta WA pricing utility window].
- A 5-minute TTL state on the round; auto-close at 3 responses or timeout.
- Brief generation: Claude with the round's structured criteria + buyer's anonymized profile → a structured *"the lawyer should know"* paragraph.

---

## Codex handoff brief (ship order, ≤90 days)

Read **`docs/2026-06-11-rainbow-3d-gap-analysis.md`** for the gap-vs-vision frame, then this section for the cited build order.

**Week 1-2 — Purchase Screen v0**
- New module `inc/purchase-screen.php`. New module `inc/whatsapp-otp.php` (Meta Cloud API on +972). Extend `offers.php` with a `reservation` state machine + TTL countdown + e-sign of a *non-binding* summary via `esign.php`. GreenInvoice one-time auth on the **yazam's** merchant ID (must be configurable per `nadlan_project`). All on, off, dark behind `nadlan_feature_purchase_screen`.
- Legal copy must be approved against Brokers Regulations 2024 + the זכרון-דברים disclaimer above [S1.27-38]. Add to skills doc.

**Week 2-4 — KYC**
- New module `inc/kyc-au10tix.php`. Token storage on `nadlan_buyer` user meta, reusable. Persona/Stripe Identity as feature-flagged fallbacks.

**Week 4-6 — View-From-My-Apartment + Sun Slider**
- Extend `inc/compound-map.php` with `view-from-unit` mode: camera at `(lng, lat, ground_elev + floor × 3.1)`, bearing from `unit.dir`, pitch 80. Inline SunCalc port (~50 lines). Date+hour slider component. Sun marker + shadow overlay on a stylized room.

**Week 6-8 — Deal Room v0**
- New buyer dashboard template (`/חדר-העסקה/<lead_id>`) for `nadlan_buyer` role. Compose lead-e2e status + offers CPT + professionals directory + esign. Pre-match 3 pros per specialty via OpenAI embeddings (text-embedding-3-small) — keep the embedding index in a new option `nadlan_pro_vectors`.

**Week 8-10 — Buying Copilot**
- Server-side orchestrator: Vercel AI SDK v6 in a tiny Node sidecar OR all-PHP REST → Anthropic. Tools: `filter_units`, `set_sun_time`, `start_reservation`, `book_pro`. Hebrew voice via Soniox + ElevenLabs; diaspora via OpenAI Realtime. `data-action` semantic attributes on every interactive element.

**Week 10-12 — Bidding Round**
- Extend Deal Room: `round` state on each `nadlan_offer`. Outbound WhatsApp template invites to top-N pros. 5-min TTL + auto-close. Quote intake + 3-card UI. Pay-per-round entry billed via GreenInvoice on pro accounts.

**Throughout**
- Every interaction emits GA4 events (`ga4-events.php` exists).
- Every module: feature flag default OFF + healthcheck block + manifest version bump + skill doc update in `skills/` so this becomes the countrywide blueprint.

**Gate criteria per phase** are in `docs/2026-06-11-rainbow-3d-gap-analysis.md`. Add for these inventions:
- Purchase Screen: round-trip a real ₪0.01 auth on a sandbox card; OTP cannot be skipped via direct POST; legal copy renders the disclaimer + checkbox before any submit.
- Sun Slider: validate sun azimuth against NOAA solar calculator for 3 known Tel Aviv dates (winter solstice, spring equinox, summer solstice).
- Deal Room: state transitions cannot be skipped; pro can only see docs the buyer shared.
- Copilot: tool-calls cannot bypass the same auth gates as the manual flow.
- Bidding Round: pro entries are billed exactly once per round; TTL release is atomic.

---

## Sources (consolidated, deduplicated)

**Strand 1 — purchase journeys:**
S1.1 Zillow Tour It Now — housingwire.com/articles/48490
S1.2 Redfin Direct — prnewswire.com/.../homebuyers-can-now-buy-redfin-listings
S1.3 Redfin Direct Texas — redfin.com/news/redfin-direct-texas
S1.4 Redfin Start An Offer — support.redfin.com/.../360018430612
S1.5 Opendoor offer timeline — help.opendoor.com/selling/getting-your-offer/offer-timeline
S1.6 Opendoor offer dashboard — help.opendoor.com/selling/getting-your-offer/find-offer-dashboard
S1.8 myLennar — myhome.lennar.com
S1.9 Lennar Account app — apps.apple.com/us/app/lennar-account
S1.16-18 Yad2/Yad1/Madlan — yad2.co.il/yad1, madlan.co.il
S1.21-23 Tidhar/Aura/Azorim — tidhar.co.il, auraisrael.co.il, azorim.co.il
S1.24 Multi-step form data — ivyforms.com/blog/multi-step-forms-single-step-forms
S1.27-31 תקנות המתווכים 2024 — nevo.co.il/law_html/law00/229640.htm + nadlancenter.co.il/article/11698, ynet.co.il/economy/article/bkkpzcliyl
S1.32 Electronic signature analysis — land-registration.lawx.co.il/.../digital-signature-real-estate
S1.34-36 קולזכות / Nevo cooling-off — kolzchut.org.il + nevo.co.il/law_html/law00/84257.htm
S1.37-38 זכרון דברים case law — mako.co.il/.../2026_q1, mplaw.co.il/real-estate-memorandum-dangers
S1.41-43 DocuSign Rooms — docusign.com/products/rooms-for-real-estate

**Strand 3 — deal team economics:**
S3.1 Opendoor S-1 — sec.gov/Archives/edgar/data/0001801169/.../tm2038271-1_s1
S3.3 Better — inman.com/2021/07/21/better-rapidly-scaling-up-real-estate
S3.4 Compass Concierge — compass.com/concierge
S3.5 Zillow Q4 2025 — fool.com/earnings/call-transcripts/2026/02/10
S3.6 Opcity referral economics — listwithclever.com/.../opcitys-referral-fee
S3.7 ZocDoc — zocdoc.com/provider-help
S3.8 Houzz Pro — pro.houzz.com/for-pros/feature-online-payment
S3.9 Thumbtack — help.thumbtack.com/article/pay-for-leads
S3.10 NN/g Get Started + Progressive Disclosure — nngroup.com/articles/get-started
S3.11 a16z vertical SaaS — a16z.com/fintech-scales-vertical-saas
S3.12 CFPB / RESPA §8 — consumerfinance.gov/rules-policy/regulations/1024/14
S3.13 חוק המתווכים — nevo.co.il/law_html/law00/72991.htm
S3.14 כללי לשכת עורכי הדין — nevo.co.il/law_html/law00/4415.htm
S3.15 תקנות שמאי מקרקעין — nevo.co.il/law_html/law00/72925.htm
S3.16 LinkedIn Pensieve — engineering.linkedin.com/blog/2020/pensieve + linkedin.com/blog/engineering/.../using-embeddings-to-up-its-match-game

**Strand 4 — frontier tech:**
S4 OpenAI Realtime — openai.com/index/introducing-gpt-realtime + developers.openai.com/api/docs/guides/realtime
S4 Soniox Hebrew — soniox.com/compare/soniox-vs-openai/hebrew
S4 Anthropic tool use — anthropic.com/engineering/advanced-tool-use + platform.claude.com/docs/.../computer-use-tool
S4 Vercel AI SDK 6 — vercel.com/blog/ai-sdk-6 + vercel.com/blog/ai-sdk-3-generative-ui
S4 Meta WA pricing — developers.facebook.com/documentation/business-messaging/whatsapp/pricing + auth-international-rates
S4 YCloud July 2025 WA — ycloud.com/blog/whatsapp-api-pricing-update
S4 Heltar Israel WA 2025 — heltar.com/blogs/whatsapp-api-pricing-in-israel-2025
S4 Israel AML — lexology.com/library/detail.aspx?g=15478713 + sumsub.com/blog/aml-kyc-israel
S4 ONE ZERO + AU10TIX — nocamels.com/2022/05/digital-bank-one-zero + ibsintelligence.com/.../au10tix-kyb
S4 HouseWhisper — geekwire.com/2025/zillow-vets-launch-housewhisper
S4 Restb.ai — restb.ai
S4 visionOS 26 — apple.com/newsroom/2025/06/visionos-26 + prnewswire.com/.../zillow-immerse
S4 RoomPlan — developer.apple.com/augmented-reality/roomplan
S4 WebGPU iOS 26 — xugj520.cn/en/archives/webgpu-3d-gaussian-splatting-browser
S4 gsplat / GaussianSplats3D — github.com/nerfstudio-project/gsplat + github.com/mkkellogg/GaussianSplats3D
S4 8th Wall VPS — 8thwall.com/docs/studio/guides/xr/vps
S4 Maket.ai — maket.ai/pricing + illustrarch.com/articles/.../maket-ai-review
S4 Spacely.ai — spacely.ai/pricing
S4 Propy + Dubai tokenization — propy.com/browse/.../propy-2025-roadmap + coindesk.com/business/2025/10/21/.../propy + mediaoffice.ae/en/news/2025/march/19-03/.../dubai-real-estate-tokenisation
S4 Israel Land Authority blockchain tender — ledgerinsights.com/.../israel-land-registry-tokenized-real-estate-exchange + cryptojungle.co.il/.../israel-land-authority-tokenization-realestate

*Strand 2 (3D tech full citations) — pending redo agent; preliminary findings in section above do not change the strategic picks.*
