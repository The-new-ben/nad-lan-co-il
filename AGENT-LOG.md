# AGENT-LOG - the God brain (append-only, newest on top)

## 2026-07-06 (6) - Cowork interiors batch-1 COMPLETE: all 8 wired, DUO gap closed
Cowork delivered the 2 missing DUO interiors (media 5122 duo-a-21, 5123
duo-b-45; byte-verified 200) + inbox draft 5124. Wired both into 4893
project_3d_units.interior_url via REST (write-verified); the other 6 were
already wired from the earlier run (rainbow 4464, ashira 4744, dimri 4745 -
siblings confirmed synced via 5061 spot-check). Draft 5124 deleted per
protocol, caches purged. LIVE-VERIFIED headless on duo-a-21: view tab renders
interior-duo-tel-aviv-duo-a-21.jpg with NO generic label + btn_winview under
it. Eye-QA: walnut library interior matches brief and DNA.
NEXT FROM COWORK: a generic default interior (in progress on their side) ->
when it lands, set project_default_interior on all 4 flagships (dimri currently
borrows a rainbow interior as its default - replace first).

## 2026-07-06 (5) - v1.72.10 HOTFIX: safeHttpUrl("") == homepage (the REAL tour bug)
Headless verify of 1.72.9 exposed the root cause of "tour not working":
new URL("", location.origin) resolves an EMPTY tour_url to https://nad-lan.co.il/
so every unit with no tour got a truthy "virtual tour" link... to the homepage.
Affected the unit tour tab AND the page media section since safeHttpUrl was
introduced. Fix: trim + early-return "" on empty input. This also unblocked the
new walk-inside (tabPane fell into the tour-link branch, never reached fpMarkup).

## 2026-07-06 (4) - v1.72.9: the 3 broken features (owner report) - tour / view-from-window / walk-inside
OWNER REPORTED: tour tab "closed to save loading time" (bad copy + dead end),
view-from-window (old project-3d.php feature) gone, walk-inside not working.
ROOT CAUSES: (a) tour tab dead-ended into tour_pending text when no tour_url;
(b) view-from-window died twice - its code retired with project-3d.php v1.70.1
AND its map host was stood down by the ONE-map doctrine; (c) interior-fp.php
walkthrough existed but was never wired into the engine unit panel.
SHIPPED v1.72.9:
- WALK-INSIDE EVERYWHERE: engine tour tab now builds the schematic FP
  walkthrough from THIS unit's real data (fpRooms JS port of nadlan_ifp_rooms:
  salon 40%, kitchen, bedrooms w/ last=mamad, balcony, window wall from unit
  direction) whenever the developer has no tour_url. interior-fp.php refactored:
  nadlan_ifp_assets_html() (static-guarded CSS+JS + window.nadlanInitFP
  rescanner) printed in wp_footer on project pages; engine calls fpInit() on
  tab switch. Honest fp_tag label ("schematic, built from unit data") x5 langs.
- VIEW FROM WINDOW, REBUILT BETTER: gold btn_winview on the view tab ->
  winView(u): scrolls the unified map into view, FreeCamera at
  alt=max(10, floor*floor_height+1.6) at the project lngLat, lookAtPoint 700m
  toward DIR_BEARING[unit direction], then showViewCone(bearing). Lazy-map safe
  (nlpjx:map once-listener). Old feature was a detached fake - this one stands
  at the real floor height on the real POI map.
- COPY LAW: tour_lazy_hint "loads on click to keep page fast" (owner: bad
  language) -> "One click and you are inside." x5; tour_pending now points
  people to the walk-inside on the inventory board instead of apologizing.
- 10 new i18n keys (btn_winview, fp_*) in HE/EN tables + FR/RU/AR overrides.
FILES: engine.js (fpRooms/fpMarkup/fpInit/winView/tabPane/click), i18n.js,
inc/interior-fp.php, inc/showroom-engine.php (wp_footer assets), version 1.72.9.

## 2026-07-06 (3) - v1.72.8: HOMEPAGE STRIKE LIVE (flagship band leads the front door)
SHIPPED + LIVE-VERIFIED (flaggrid present, 4 cards, contain-fix, singular grammar):
- NEW FLAGSHIP BAND right under the hero: "בחרו דירה מתוך הבניין, בתלת ממד" -
  four flagships with hero plates + gold 3D badges + units count + tour CTA +
  link to /premium/. Spliced into the band order AT RUNTIME so a DB-stored
  nadlan_home_bands option cannot hide it. i18n keys x5 languages.
- HERO VIDEO FIX: 16/9 container + object-fit contain - the 16/11 cover crop
  was clipping the video's baked-in text ("Every apartment, explorable" now
  fully visible, letterboxed on the dark panel).
- UPSELL TILES: DNA cards (gold plus badge, cream gradient, solid border)
  instead of empty dashed slots that read unfinished.
- GRAMMAR: demand-areas singular forms (פרויקט אחד/דירה אחת) x5 langs.
EYE-QA: band reads premium; NIT for next pass - theme underline leaks onto
flag card titles (.nlhv2-flag * text-decoration none needed); fl_sub subtitle
contrast is low-ish. WEBSITE SWEEP STATUS (this session, all live-verified):
home v1.72.8 / projects catalog + drone map / premium / 4 flagship pages (3D,
map sync, cone, weaver, buy-flow, RFP) / professionals (labels fixed) /
2 mega guides / 4 calculators / https sitemap / zero long dashes site-wide.
OPEN GATES: owner decision #34 (seeded ratings), geocode expedition (drone map
+ near-me depend on it), Site Kit connect, email deliverability (last), DUO
translations + 2 interiors + ZOHI article via Cowork.

## 2026-07-06 (2) - v1.72.7: DRONE MAP LIVE + professionals fixes + homepage audit
DRONE MAP (owner ask): /nadlan/v1/project-map (geocoded, siblings excluded, 6h
cache) + collapsible band on /projects/ - satellite-streets, pitch 58, 3D
buildings, gold pins, popup w/ hero plate, fly-in on click. LIVE: 4 pins (the
flagships), canvas verified, honest note "grows with location verification".
Growth lever = the geocode pass over the 961 catalog (still open).
PROFESSIONALS: raw machine enums (urban_planner/engineer/accountant/surveyor/
property_manager/interior_designer) leaked as card badges - resolver read the
BASE map only while Hebrew labels existed in the extras map. Fixed (uses full
map, fallback never prints machine tokens). Live: 0 raw enums. Meta description
added. HONESTY FLAG FLOATED TO OWNER: top-sorted professional cards carry
seeded rating/reviews_count meta (4.9, 87 reviews etc.) with NO real review
records behind them; same seeded names (Dana Barak, Shira Golan) are matched
into RFP documents as advisors. Options: label as demo, zero the counts, or
seed-flag meta + "מאומת" only for real ones. OWNER DECISION NEEDED before
marketing push - fake social proof is a trust landmine.
HOMEPAGE AUDIT (design+business, screenshots):
STRONG: clear value-prop hero + tabbed search + live stat strip; sketch-plate
cards; visible 5-language switcher; price ticker; SEO link rows.
GAPS (ranked): (1) hero 3D showcase panel reads broken - dark-on-dark, clipped
LTR overlay ("very apartment, explorable"); our crown-jewel demo looks dim.
(2) THE FOUR FLAGSHIPS ARE ABSENT from the homepage - no premium 3D projects
band; front door doesn't sell the differentiator. (3) two big VACANT ad-slot
cards near the hero read unfinished (vacant inventory should collapse).
(4) "1 דירות" grammar + thin counts in demand-areas band. Queued as task #33.

## 2026-07-06 - v1.72.6: BIG CATALOG SEVERE UPGRADE LIVE + guides categorized
GUIDES: category "מדריכים" (id 35, slug guides) created; both mega guides (5117,
5118) assigned - byline no longer "Uncategorized".
CATALOG /projects/ - evidence-driven surgery (before/after screenshots to owner):
ROOT CAUSES FOUND: (1) language siblings (-en/-fr/-ru/-ar) flooded the grid as
garbled duplicate cards (Russian/Arabic/English titles start-truncated by the RTL
container); (2) machine enum "אחר" badge printed on most cards; (3) the sponsored
slot card nested <a> inside <a> - ILLEGAL HTML that browsers split into a broken
empty gold card; (4) archive had NO meta description; (5) counts included siblings.
FIXES SHIPPED: posts_where REGEXP excludes sibling slugs from grid + facets + total
(973 -> 961 honest); card titles dir=auto + unicode-bidi:plaintext (correct-side
ellipsis); "other" badge suppressed; sponsored card rebuilt as DIV with real inner
links; meta description with buyer keywords (דירות למכירה מקבלן, תמ"א 38).
LIVE VERIFIED: 0 sibling links in grid, no nested-anchor card, meta desc present,
grid now shows distinct plate-art cards (YOO, DUO, Aura, Rainbow, Akirov, Marina
Herzliya, Einstein, Recanati, Park Bavli, Utopia...). Eye-QA: reads premium.
POLISH OPTIONS (not shipped): 2-line title clamp instead of 1-line ellipsis;
near-me chip on the catalog (geo-search /near exists); facility filters port from
premium tier needs per-project facility meta on the wide DB (data pass, not code).

## 2026-07-05 (10) - MEGA GUIDE PUBLISHED (HE+EN, 5,000+ words each, foreign-investor SEO)
Owner asked for an aveliving-style "elevated apartment living" guide, mega-length,
Israel-adapted, foreign buyer/investor intent, full SEO/AEO with schema+Yoast,
internal links, no cited sources, win competitors.
PUBLISHED LIVE (verified, cache-busted):
- EN post 5117 /luxury-apartments-israel-guide/ (5,615 rendered words)
- HE post 5118 /luxury-apartments-israel-guide-he/ (5,052 words)
Both: FAQPage JSON-LD live, hreflang he/en/x-default reciprocal, Yoast SEO title +
metadesc + focus kw + cornerstone flag, canonical, EN lang=en-US (overrode he-IL
default via guide-schema filter), zero long dashes, 13-15 H2 + 23-30 H3, 21 internal
links each (projects, /premium/, calculators, existing foreign-buyer posts), 2
tables, hero image (Cowork interiors 5109/5113). Content: real facts from research +
existing site data (tax 8/10% at 6,055,070; 50% LTV non-resident; Sale Law arvut
bankit; Sde Dov 1,300 dunam/16,000 homes; TLV yields ~3%; developer lines). Prices
estimate-labeled, per-unit pricing "on developer proposal" (never invented).
NEW MODULE v1.72.5 guide-schema.php: FAQPage + hreflang + lang from post meta,
reusable for every future guide. Fact base + article HTML saved to
handoff/research/2026-07-05-elevated-living/.
FLOAT: posts landed in category "Uncategorized" - create a "Guides/מדריכים" category
and reassign for cleaner byline + archive SEO. EN byline shows Hebrew author name.
NEXT: big catalog #31 (still pending), or reassign guide category first.

## 2026-07-05 (9) - v1.72.4: THE RFP DOCUMENT IS REAL (buy-flow phase 2)
inc/rfp.php: POST nadlan/v1/rfp creates a tokenized document from SERVER-side
project/unit facts (client only points at slug+unit, never dictates data); GET
/rfp/<token> renders a branded printable page: masthead (ID/date/30-day validity),
unit table, configuration pills, ADVISORS MATCHED FROM THE REAL PROFESSIONALS
DIRECTORY by profession (designer->interior_designer/architect, lawyer->lawyer,
mortgage->mashkanta, inspect->bedek_bait), status timeline, estimate disclaimers,
print button. noindex, unguessable 24-char token, stored as private nadlan_rfp
post + linked to the lead (rfp_id meta) so the owner can forward it.
buyflow.js: the document generates WHILE the dispatch stages play; the done screen
links it in the page language. E2E LIVE: created doc for dimri B-24 premium +
designer + mortgage -> rendered 200 with real advisors (Dana Barak interior
designer TLV, Shira Golan mortgage Ramat Gan). Eye-QA PASSED - the document looks
like a bank-grade branded page. The professionals directory is now WIRED into the
buying machine (owner's "it all has to connect" fulfilled at v1 level).
REMAINING for #30: owner-driven status advance (stage 2/3) UI in lead inbox,
WhatsApp pings (needs WhatsApp Business API), AI summary paragraph (openai key
currently 401 - float to owner), buyer email copy (blocked on deliverability).
NEXT: big catalog severe upgrade (#31).

## 2026-07-05 (8) - v1.72.3: BUY-FLOW V1 LIVE + full Cowork ingest sweep
COWORK OUTPUT AUDIT (owner ask "check all cowork outputs"): 5 MORE interiors landed
18:33-18:45 (rainbow penthouse, ashira 18W + 4G, dimri u2 + u4) -> eye-QA passed
(dimri penthouse suite exactly per batch brief) -> wired into their units on all 15
posts. 6/8 interiors done; missing: duo-a-21, duo-b-45 (float for Cowork re-run).
ZOHI dossier saved to data/projects/dossiers/zohi-sde-dov.dossier.json + merged into
the project record (developer: Mivne, Levinstein and Metropolis; has article
material + units + prices). Session log archived to handoff/cowork-logs/. Both
AGENT-INBOX drafts DELETED per protocol - inbox is clean.
BUY-FLOW V1 SHIPPED (buyflow.js, per research spec): gold "בנו לי הצעה" CTA on every
apartment panel -> finish level (no invented prices, "exact pricing in the
developer proposal") -> add-ons: designer/lawyer/mortgage/inspection/furniture,
never pre-checked, skippable -> 2 fields only (name + WhatsApp) + explicit consent
-> staged dispatch animation with HONEST wording ("sent to the NadLan team to
coordinate with the developer" - we do not claim direct contractor delivery yet)
-> what-happens-next timeline. Structured rfp-v1 JSON posted to nadlan/v1/lead.
5 languages. LIVE E2E DRIVEN headless: unit selected -> configure -> submit ->
POST ok -> dispatch stages ticked green on screen. Zero page errors.
NEXT PHASES (task #30): AI RFP document generation (ai-provider exists), status
timeline page, WhatsApp pings, professionals upgrade feeding advisor cards.
STILL OPEN: big catalog severe upgrade (#31), ZOHI article (dossier ready, article
must pass the 3,000-word gate), DUO translations + 2 DUO interiors, nlpjx price
band i18n, email deliverability (ack leg), Site Kit connection (owner, 2 min).

## 2026-07-05 (7) - v1.72.2: WEAVER LIVE + default interiors + two site-wide SEO bugs killed
WEAVER (owner go): article splits at its own chapter boundaries into numbered gold
frames + asset thumbs + jump-TOC pills. Content law IN CODE: every node survives
verbatim, <3 chapters -> untouched. LIVE on all 4 (13-17 chapters each), TOC jump
verified, EN sibling shows "Chapter 1", word counts intact (4.5k-6.5k rendered).
DEFAULT INTERIORS (owner law: no blanks): project_default_interior meta (registered
in showroom fields) feeds units without interior_url + honest generic label in page
language. Set on 16/16 posts using Cowork's first interior (media 5104). Verified on
DUO unit A-9: image + label render in the view tab.
SEO BUGS FOUND + FIXED SITE-WIDE:
1. WP home/siteurl options were HTTP -> the whole Yoast sitemap emitted http URLs =
   every crawl a redirect ("Page with redirect" in GSC, depressed indexing). Fixed
   options to https via tmp snippet (before/after logged), sitemap now https,
   pages 200. Likely a major answer to "why many pages are not indexed".
2. wptexturize was converting " - " to en dash AT RENDER on clean stored content
   (found in dimri H2 + nlpjx intro). run_wptexturize disabled (owner law #2).
   All 4 pages now render ZERO long dashes.
GSC AUTH ANSWER (owner asked): google-site-kit plugin ACTIVE but connection NEVER
completed (connected:false, setupCompleted:false). No service account in repo. Owner
must either finish Site Kit setup (his Google login, ~2 min) or add a service
account to the GSC property so agents can read indexing/query data. ALSO: many
catalog pages are noindexed BY DESIGN (schema.php thin-content guard, anti-
cannibalization) - part of "not indexed" is intentional.
LEAD E2E TEST: POST nadlan/v1/lead -> ok, lead_id 5114, route_status fallback_admin,
ack_sent FALSE -> leads are stored + routed but acknowledgment/email leg unverified
(deliverability float stands). Buy-flow research DONE (Wolt/Booking/Tesla/StockX
patterns): spec at handoff/research/2026-07-05-buy-experience/spec.md, build queued.
STILL OPEN: big-catalog severe upgrade (owner: "looks awful") - next strike;
professionals upgrade feeds RFP advisor cards; nlpjx price band i18n; ZOHI ingest;
DUO translations; interiors batch (7 remaining) via Cowork.

## 2026-07-05 (6) - v1.72.1: view cone, hero/poster split, 3D badge on premium cards
OWNER CORRECTION UNDERSTOOD + FIXED: my poster swap accidentally replaced the page
HERO and the premium-card media with the 3D render (model_poster drives both). The
owner generated NEW hero plates via Cowork (media 5099 rainbow-v3, 5100 ashira-v3,
5101 dimri-v3, 5102 duo-v2). Architecture fixed: project_3d_image = marketing hero
(page hero band + premium card media); project_model_poster = 3D render (loading
crossfade + small 3D badge on the premium card). Set on all 16 posts, live-verified:
hero=v3 plate, poster=3D render, 3 premium cards each with a gold-bordered 3D badge.
VIEW CONE SHIPPED (owner ask): selecting an apartment draws a terracotta cone on the
building pin, rotationAlignment map (turns with the terrain), pointing the apartment
view direction; honors pre-map selections via nlpjx:map ready event. Verified live:
dimri unit-2 (Hebrew dir "דרום מערב") -> cone drawn, bearing -135 = south-west.
COWORK DELIVERED TODAY: 4 hero plates + more project plates (einstein x3, and the
plate set from 7/3) + FIRST INTERIOR image (5104 interior-rainbow-tel-aviv-unit-16-w)
-> wired into rainbow unit-16-w interior_url on HE + 4 siblings. Cowork then stalled
on the rest of the interior batch (7 images remain) - float.
ARTICLE WEAVING: owner unsure what it means -> before/after HTML illustration
delivered in chat (structure only, zero word changes). Awaiting his go.

## 2026-07-05 (5) - v1.72.0 THE MAP SURGERY: one synced map beside the 3D, live-verified
Owner gave full go ("you are responsible for the success of this project").
SHIPPED + VERIFIED on all 4 HE pages + dimri-EN:
- ONE MAP: engine adopts #nlpjx-map (POI layers: prices/education/transit/shopping/
  health/future-plans/3D/satellite) directly AFTER the theater section (#building);
  engine's plain .nl-map hidden; mapbox-init stands down when unified map present.
  Root cause of double map: nlpjx moved/hid at DOMContentLoaded, engine renders
  after -> race. Now engine-owned in afterRender() (idempotent, rescued before
  ROOT.innerHTML re-render wipes).
- SYNC: model orbit -> map bearing (-theta, user gestures only so auto-rotate never
  spins the map); selecting an apartment eases the map to the apartment's view
  bearing (west unit -> bearing 270, verified numerically = -90 live).
  Convention: model -z = north (true for factory GLBs; Rainbow approximate).
- I18N: map section localized he/en/fr/ru/ar (chips verified English on dimri-en);
  Hebrew compass names in unit meta resolve via HE_DIRS map (dir badge leak fixed);
  world band renamed "כל מה שסביב הפרויקט" per owner ("all around", not "all world").
- Zero page errors on all verified pages; exactly 1 mapbox canvas per page.
STILL OPEN (owner knows): article wall weaving (11.9k px) - next surgical band;
nlpjx price/world sections still Hebrew-only on siblings; interiors default via
Cowork batch; buy-flow research; ZOHI ingest; professionals upgrade; GSC indexing.

## 2026-07-05 (4) - owner round: menu, coords, poster crossfade; TWO-RENDERER diagnosis
OWNER DIRECTIVES (this round, standing): presume he did NOT see every problem - god
mode + design + critical skills always on; study worldwide top-league competitors and
worry we are not there; ONE map NEAR the 3D model, synchronized (avoid the word
"world-around"); never leave blanks - approximate coordinates with disclaimer are
ALLOWED (1km tolerance), default interiors instead of empty; TEXT/TITLES must not be
changed without his explicit permission; buying experience research = e-commerce
grade (Wolt/booking-style progress, add designer/furniture/advisors bundles -> RFP);
upgrade professionals dramatically; check why many pages not indexed; four projects
identical in structure, side-by-side comparison, ready to show developers.
DONE THIS TURN (live-verified):
- "קטלוג תלת ממד" added to primary nav -> /premium/ (template-part DB override + repo
  file mirror).
- Approximate coords + honest address disclaimer: dimri 32.1068,34.7823; duo (Sumail)
  32.0840,34.7830 -> both pages now have the map band. Dimri siblings synced.
- POSTER CROSSFADE FIX (the "CSS stacking" complaint): engine overlays .nl-poster
  (model_poster meta) over the viewer until GLB loads; posters were OLD plate art ->
  jarring swap. Rendered real model posters on the exact stage gradient for all 4
  projects, set on all 16 posts. Refresh now crossfades poster->model seamlessly.
DIAGNOSED (surgical plan given to owner, NOT executed):
- TWO RENDERERS stacked on every project page: showroom-engine (nl-*) AND
  project-experience (nlpjx-*). nlpjx renders the SECOND map (#nlpjx-unimap with POI
  filters) after the engine (which has its own .nl-map). Page anatomy: engine 6.5k px
  -> nlpjx-map -> 11.9k px article wall -> nlpjx-price -> world grid. Merge plan:
  ONE filterable map adjacent to the theater, model-orbit <-> map-bearing sync,
  hotspot select -> view cone on map; suppress the duplicate; weave the article.
- i18n leak I created: facade_images label/notice are Hebrew strings synced verbatim
  to EN/FR/RU siblings (untranslated badges). Fix via engine i18n keys.
- Mobile: only designed scroller is the unit drawer body; no horizontal overflow.
COWORK STATUS: delivered ZOHI Sde Dov dossier (8,615w, draft 5094) + session log
  (5070), then stalled on the rest. ZOHI = 5th project to ingest. Ashira dossier
  still on me.

## 2026-07-05 (3) - RICH MODELS LIVE ON ALL FOUR PROJECTS (v1.71.8 + v1.71.9)
SHIPPED + VERIFIED LIVE (headless, screenshots to owner):
- ashira-HE/EN/FR/RU/AR: ashira-rich.glb (stepped 4-building complex, NO sea - owner
  correction honored), 5 hotspots aligned via floor_height 3.2, 5 facade tiles, 1 map.
- dimri-HE + 4 siblings: dimri-rich.glb (39fl seafront tower + podium, sea on west),
  4 hotspots, NEW facade band (tight west-elevation render, media 5090), tiles at
  floors 12/24/36/39. Map still absent = no lat/lng (honest; geocode pass pending).
- duo-HE: duo-rich.glb twin 50fl towers, FIRST 3D ever on this page: 5 new honest demo
  units (A-9/21/33, B-27/45) with explicit per-tower hotspot_position, facade band
  (south elevation showing both twins, media 5091), click-to-zoom + full spec panel
  verified. No language siblings yet (no translations) - queue.
- rainbow: kept its authored model.glb (owner-approved). ADDED the missing facade band
  (rainbow-facade.jpg + 6 tiles incl. boutique) - it violated law #1 (never without
  facade) until today. Explicit authored hotspot_position now honored -> boutique
  hotspot anchors to the boutique building instead of floating.
ENGINE FIXES (v1.71.8/9):
- unitPos() honors explicit hotspot_position/hotspot_normal (offset twin towers,
  boutique buildings); floor x floor_height formula stays as fallback.
- FACADE RTL MIRROR BUG found in live QA: tiles used inset-inline-start, the facade
  photo never mirrors -> DUO A-units sat on tower B on Hebrew/Arabic pages. Fixed to
  physical left/top; all four projects' stage coords re-authored physical-from-left.
- fly-to-unit radius scales with tower height (150m fallback flew inside DUO's crown).
- HEALTH ENDPOINT WAS LYING: version hardcoded '1.69.67' since then; every deploy
  verification against it was theater. Now reads NADLAN_CONFIG_VERSION. Deploy
  verification law: verify by fetching a shipped file (byte size), not just health.
DEPLOY HAZARD LOG: a STALE cherry-pick sequencer from a dead session blocked the
  squash-dance (git cherry-pick --quit cleared it). Code Snippets DELETE returns 204
  but snippet persists until deactivated first - always POST active:false then DELETE.
WORRIES/FLOATS (told to owner in chat this turn):
- ~60 stale tmp deploy snippets (ids 5-65) still registered in Code Snippets - residue;
  should be swept in a maintenance pass.
- dimri + duo have no map (no lat/lng). DUO has no language siblings. Interior stills
  prompt for Cowork delivered in chat. Zoom-to-unit on 150m towers is close-up of the
  crown area - improved with height-scaled radius, could get per-unit orbit tuning.

## 2026-07-05 (2) - rich-model factory built; v1 candidates NOT deployed (under standard)
- scripts/generate-rich-building.py: parametric Rainbow-style factory (glass core,
  floor slabs, balcony rhythm, fins, crown+gold, podium, honest small site, sea ONLY
  when seafront:true). Specs from real compositions: Ashira 8/8/16/35 NO SEA (owner
  correction honored), Dimri 39fl+podium seafront, DUO 2x50fl (dossier).
- v1 outputs in assets/engine/rich-v1/ (5.8k/4.8k/12k tris). EYE-QA VERDICT: clean +
  correct composition but NOT Rainbow-grade yet: balconies too subtle, palette too
  pale, site too bare. Per owner law (never under standard, walk slowly) NOT deployed;
  live pages untouched. Next: beauty pass (deeper balconies w/ contrast, warmer stone,
  saturated teal glass, amenity court, trees, ground texture) then swap + hotspot
  alignment + facade tiles + sibling sync + plugin release in ONE reviewed step.
- Owner directives logged: rich model on ALL projects; ONE map doctrine (rebuild as
  single mobile-first layered map: facilities/schools/paths/area-info for foreigners);
  PROJECT PAGE STANDARD to machine-enforce band order + assets (design next turn:
  STANDARD.md + /nadlan/v1/project-standard compliance endpoint); interior = generated
  stills v1; premium cards mini-3D + near-me + big-catalog SEO cleanup approved queue.

## 2026-07-05 - MAX GOD MODE: #2 deep audit + fixes + DUO live
COWORK INGESTED: DUO dossier (8,605w) + DUO Hebrew article (4,531w, 0 dashes) ->
  PUBLISHED into live /projects/duo-tel-aviv/ (4,656w rendered). Ashira dossier BLOCKED
  by ChatGPT Pro (2 failed runs, empty output) - I will author it from web research.
  Inbox drafts deleted.
#2 AUDIT (live, headless, evidence-based):
  rainbow-HE: 6 hotspots, RICH model.glb (the good one IS live - my earlier claim it
    used dot-on-plate was WRONG, corrected to owner), article 3,150w, ONE mapbox map.
  ashira-HE: 5 hotspots + 5 facade tiles, article 2,783w rendered, one map.
  dimri-HE: 4 hotspots, model = 8KB model-prototype.glb (PLACEHOLDER - worst model live),
    NO map (post 4745 lacks lat/lng).
  duo-HE: article live, NO 3D at all (no model meta) - next: attach duo.glb + units.
  LANGUAGE BUG CONFIRMED + FIXED: siblings had no units/facade/latlng meta ->
    synced HE meta to all 12 siblings; verified ashira-EN/AR 5 hotspots+5 tiles+map,
    rainbow-FR 6 hotspots+map. Task #21 done (dimri map still absent = no geocode, honest).
  DOUBLE MAP: automated count finds ONE mapbox canvas per page. Owner sees two ->
    need his pointer (which page/where) or a visual scroll-through next turn.
CALCULATORS: added buy-or-rent + apartment-deal-check links to /mortgage-calculator/ hub
  (nav points there). Homepage tools band pending.
DECISIONS GIVEN: emails from domain via SMTP/deliverability check first; 3D presentation
  assets plan (massing factory + AI facade drape / Meshy-Tripo for hero); costs explained.
NEXT QUEUE: dimri model upgrade (assets/engine dimri 52-180KB vs placeholder), DUO 3D meta,
  ashira dossier by me, premium cards mini-3D + near-me geolocation, big-catalog overhaul+SEO.

## 2026-07-04 (23:00) - PREMIUM CATALOG LIVE
- https://nad-lan.co.il/premium/ (v1.71.6-7): curated tier, only full-experience projects.
  11 facility filters with gold SVG icons (pool/spa/gym/cinema/concierge/lobby/kids/
  retail/parking/mamad/lagoon), nearby filters (sea/park/marina), developer filter,
  sort, active pills, no-results state, developers-join CTA (monetization tier).
  QA live: lagoon filter -> Rainbow only, pill + count correct, zero JS errors.
- POSITIONING DECISION GIVEN TO OWNER: /premium/ = curated monetizable tier;
  /projects/ (900+) stays the SEO net. Not a replacement.
- FLOATED to owner in chat: full undecided/forgotten list (see message log below).

Owner's law (2026-07-04): every agent logs here what was delivered to the owner,
what was told to him, open worries, gaps, reminders, and what he might have
forgotten. Read this AND INVENTORY.md at the start of every session. If you
tell the owner something or give him something, WRITE IT HERE in the same turn.

## 2026-07-04 (evening) - publishing push
DELIVERED TO OWNER (live, not files):
- PUBLISHED https://nad-lan.co.il/projects/rainbow-tel-aviv-en/ (3,409 words rendered, engine on)
- PUBLISHED https://nad-lan.co.il/projects/dimri-yama-sde-dov-en/ (3,435 words rendered, engine on)
- Site-wide em/en-dash purge across all CPTs (character swap to "-", sentences untouched)
- Earlier same day: article-extractor fix v1.71.2 (restored 5 Ashira articles, ~3,000w each,
  live verified); showroom selection restored (reveal=auto v1.71.0, ashira.glb 404 fixed
  v1.71.1, CMS unit hotspots + facade grid populated); og:image + favicon fix v1.70.9;
  i18n theme header/footer v1.70.7; hero video autoplay v1.70.8.

FACTORY STATE (handoff/claude-design/2026-07-03-project-page-factory):
- THE GATE: no page emitted under 3,000 article words / without hotspots / without facade.
- Compliant: Ashira x5 langs, Rainbow HE+EN, Dimri HE+EN (9 pages).
- BLOCKED awaiting real translations: rainbow fr/ru/ar, dimri fr/ru/ar; DUO blocked entirely (no article).
- New features: facade unit tiles (approx label), view-from-apartment POV, facilities chips,
  projects-catalog.html (13 facility filters + rooms/delivery/sea + deals per card).

OWNER LAWS (standing, machine-enforced where possible):
1. Never a page under 3,000 words, never without selectable 3D hotspots, never without facade. (factory gate)
2. NO em/en dashes anywhere on the site; swap to regular "-" without touching sentences. NO "AI tellers". (factory gate + site sweep)
3. No file-only deliverables: substance goes in the chat. Files are repo memory.
4. Publish, don't hand off: work lands on the live site, not in attachments.
5. One prompt at a time, fully filled, zero placeholders.
6. Log everything here + INVENTORY.md for assets. GLBs are never deleted silently (GRAVEYARD.md).

OPEN GAPS / WORRIES (float these unprompted):
- 6 language pages blocked pending FR/RU/AR translations (prompts ready: handoff/research/prompts/translate-*.txt) -> Cowork loop should run them.
- DUO has no article at all -> needs full-world prompt + article.
- Live /projects/ catalog (967 items) quality: truncated/garbled card titles (RTL ellipsis), duplicate-looking cards (UO/OO), mixed-language titles; facility filters not yet on the live catalog (prototype exists in projects-catalog.html; port to catalog module).
- Rainbow/Dimri live HE pages: units/facade CMS meta not yet populated like Ashira's (selection works from defaults; replicate Ashira's meta population).
- Geocode pass still 0/30 in data/projects (govmap via gush/helka for Rainbow now possible: gush 6634).
- Price pass: only Rainbow has filed evidence (80,300 ILS/sqm avg sold 31.12.2025); others null.
- Email deliverability (SPF/DKIM/DMARC) unverified; broken mirrored logo.png still in repo.
- Prototype pages inline ~1.1MB GLB base64: fine for prototypes, must become cached asset for production.
- Interior walkthrough (elevator/lobby/pool) needs interior 3D assets; current POV v1 = camera at unit position.
- 287 remote branches; squash-merge makes "unmerged" reports lie. INVENTORY.md is the source of truth.

REMIND THE OWNER:
- Run the two translation prompts (Rainbow, Dimri) in ChatGPT Pro Extended, or let Cowork do it (mega-prompt given in chat 2026-07-04).
- Homepage/emails to contractors are HELD until the three projects are fully verified by him.
- Decision pending: port facility filtering into the live /projects/ catalog (replaces prototype).
