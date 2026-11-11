# Raw notes and source log: HAD-701 reverse engineering, 2026-11-10

These are working notes, not a report. The analysis is in `../products.md`, `../rubric.md` and `../white-space.md`.

## Runs (all on 2026-11-10, headless Chrome over CDP, software WebGL)

| Job file (tools/) | Results file | What it did |
|---|---|---|
| landing-desktop.json | landing-desktop-results.json | Landing pages of 16 candidates at 1366x900: load, LCP, CLS, bytes, hosts, accessibility counts, hreflang, text sample |
| editors.json | editors-results.json | Tried 10 editor or demo URLs. Planner 5D became the sign-up wall; Homestyler became the sign-in wall; Coohom was marketing only; HomeByMe /en/start 404; IKEA /home-design/app/ 404; Rayon app connection error; Floorplanner demo opened |
| mobile.json | mobile-results.json | Mobile 390x844 landing pages for the deep products and GBuilder, plus the Roomle room demo on desktop and mobile |
| fp-deep.json | fp-deep-results.json | Floorplanner demo: 2D, room panel, objects, finishes, styleboards, 3D first person, orbit, info. Also mobile view |
| viewers.json | viewers-results.json | Planner 5D gallery "Open in 3D" (ToS modal, not accepted); Coohom panorama desktop, mobile and AI-walk; Homestyler project page; Higharc plan page |
| coohom2.json | coohom2-results.json | Coohom AI-walk tour: Product List, Floor Plan minimap, Room Select, More |
| hs2.json | hs2-results.json | Homestyler public project page text (AI gallery, no 3D); Higharc Belmont page text ("Design in 3D" button with data-higharc-plan-id) |
| ha.json / ha2.json / ha3.json | ha*-results.json | Higharc: button click did not open the overlay in headless. Showroom intro opened directly; 3D still loading at 36 s; mobile blank at 7.6 s |

The Higharc intro URL was derived by reading the public embed script `https://app.higharc.com/static/builders/scripts/showroom.js?builderId=G3de6WX90K7nylNm`. It builds `/showroom/intro?builderId&planId&planType&embedSource=script`.

## Pages read through fetch or search (evidence class, date 2026-11-10)

**Planner 5D**
- planner5d.com/pricing [VC]
- planner5d.com/use/ai-floor-plan-generator [VC]
- tool.planner5d.com/b2b-floor-plan-recognition [VC]
- support.planner5d.com articles 14602018 and 15116256 [VC]
- planner5d.com/collaboration-tool [VC]

**Homestyler**
- homestyler.com/pricing [VC]
- homestyler.com/forum/view/2077998093719244802 (Import Floor Plan) [VC]

**Coohom**
- coohom.com/pricing [VC]
- coohom.com/floor-planner [VC]
- coohom.com/helpcenter/3FO4K4WJT1J8.md (gave the public panorama demo links) [VC]
- blog.coohom.com/?p=4974 [VC]
- coohom.com/de/helpcenter/enterprise-cabinet-projection-area-quotation-settings [VC]

**RoomSketcher**
- roomsketcher.com/pricing/ [VC]
- roomsketcher.com/order-floor-plans/ [VC]
- roomsketcher.com/demo/ (video only) [VC]

**Floorplanner**
- floorplanner.com/pricing (subscription prices did not render; credit packs did) [VC]

**Higharc**
- higharc.com/product/showroom [VC]
- intercom.help Higharc "Showroom intro" [VC]
- Higharc customer playbook, Landmark 24 [VC]
- HousingWire sponsored piece [PR]
- Unreal Engine news on builder configurators [PR]

**GBuilder**
- gbuilder.com/solutions/sales [VC/SL]
- gbuilder.com/resources/market-and-sell-off-plan-homes-… (dated 2020-09-03) [VC]
- e-signature, margin and package claims came from a search summary of gbuilder.com resources [VC]

**Zonda**
- zondahome.com/digital-solutions/envision/ [VC]: "35% average increase in options sold". Another Zonda case-study page says 15–30% [VC]

**Others**
- HomeByMe: home.by.me/en/ [VC]
- IKEA Kreativ: IKEA help pages and press (Engadget, TechCrunch) [VC/PR]
- magicplan: Capterra and GetApp listings [RV]
- Rayon: ArchDaily, Archinect, Liveblocks blog [PR/VC]
- Floorfy: floorfy.com/products/videocall (direct fetch hit a redirect loop; content came from the search summary) [VC]
- CPQ3D / London Dynamics: vendor blogs through the search summary [VC]
- Israel: startupim.com/company/muonovate [RV]; the REALS press release [PR]; drushim.co.il job ads for a tenant-change coordinator [RV]
- **vizit.co (3DCOM) now serves a gambling-spam page.** Domain likely lapsed. Its links were not followed.

## Things noticed but not scored

- Planner 5D and Coohom pricing pages displayed ₪ prices to our fetcher. They detect currency from the visitor's location, but neither has a Hebrew UI.
- The Homestyler mobile site m.homestyler.com took 30.6 s to its load event in our rig.
- The GBuilder mobile landing took 39 s to its load event, despite LCP 1.08 s (late third-party scripts).
- The Roomle room demo shows partner products (for example Tom Dixon lighting), AR, first person and a cart. It was a public demo but is outside the deep set.
- Higharc option copy is plain-language and buyer-friendly, with "standard" against "Upgrade to …" descriptions. That is a good pattern to learn from; write original Hebrew copy rather than translating theirs.
