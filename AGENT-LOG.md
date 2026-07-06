# AGENT-LOG - the God brain (append-only, newest on top)

## 2026-07-07 (5) - v1.72.31 DRIP RESTORED (WP edit_date gotcha) + tolerance + stuck guard
v1.72.30's first live tick: 3 GENERATED (was 0 forever) - proof the expand
pass works. But all 3 published INSTANTLY instead of entering the drip.
Root cause: WP core - wp_update_post on a draft (post_date_gmt
0000-00-00) silently resets a passed post_date to NOW unless
edit_date=true; then status future + date now = instant publish. Fixed in
the writer hand-off AND in the intake stage-2 fill path (same latent bug).
The 3 already-published articles stay up (honest content, within cadence):
אחוזי בנייה 5199 (808w, 0 bad dashes, 7 sections), מהנדס אזרחי רשוי 5329,
תכנית מתאר מקומית 5210. Also in v1.72.31: (a) 10% tolerance band on the
tier floor AFTER the expand pass (מכון התקנים failed at 668/700 - a
near-miss, not thin content); (b) enc_fail_count per entry, parked after
5 fails + 'stuck' count in status (prevents priority-front entries from
blocking the queue and burning API every tick); (c) duplicated opening
title heading stripped deterministically; (d) prompt nudge: natural
section headings (model was copying my structure list verbatim as
headings). OWNER MESSAGE MID-WORK: wants this writer system spec'd in
detail for reuse on jus-tice.co.il via another Claude chat - writing the
portable spec next.

## 2026-07-07 (4) - v1.72.30 WRITER FIXED: the 0/6 mystery solved (undershoot, not truncation)
FIRST TICK FAILED 0 generated / 6 failed while a simple diagnostic passed.
Full-fidelity diagnostic (encdiag2 temp snippet, exact write_one prompts on
real p1 skeleton 5245 'בטון מזוין'): http 200, finish_reason=stop,
completion_tokens 1114/3000, output 422 words vs floor 700. NOT truncation,
NOT the API, NOT kses - gpt-4o-mini simply undershoots long-form briefs
(wrote 422 against an 800-1300 target). The floor did its honest job.
FIX (v1.72.30): (a) expand pass - a draft under its tier floor goes back to
the model with the measured count + target ('הרחב והעמק... בלי מלל ריק')
and the longer result wins; (b) max_tokens 3000 -> 6000 headroom; (c) the
mandatory minimum stated again in the user prompt; (d) failures now leave a
trace: option nadlan_enc_writer_last_fail {pid,title,words,floor,at},
surfaced in /nadlan/v1/enc-writer-status as last_fail. Cost note: expand
pass doubles the call only on short drafts; on gpt-4o-mini still pennies.
Manifest updated via load->modify->dump + immediate re-validate (the new
law after the corruption incident).

## 2026-07-07 (3) - v1.72.29 SELF-WRITING ENCYCLOPEDIA + SITE-DOWN INCIDENT + manifest corruption repaired
SELF-INFLICTED CORRUPTION CAUGHT + FIXED: the v1.72.28 log script wrote
AGENT-LOG content OVER plugin-dist/nadlan-config.json (wrong variable in the
final write) - manifest was invalid JSON since 82d1903 and AGENT-LOG was
missing entry (2). Repaired: AGENT-LOG restored from the corrupted manifest
(which held the correct log text), manifest rebuilt from the last good JSON
(v1.72.27) + both changelog entries. LESSON: never reuse open(f) handles
across files in log scripts; validate manifest JSON after every write.
v1.72.29 BUILT (deploy blocked by site-down): inc/glossary-writer.php - the
in-site hourly writer. Owner asked about WP AI plugins (researched: AI
Puffer/GetGenie/AI Engine, $0.02-0.10/article API cost) - MY CALL: no 3rd
party plugin (knows nothing of entity fields/tiers/dash law/drip/anti-
cannibalization); built in-house on the site's own OpenAI key instead:
hourly cron, priority-ordered skeletons, tiered articles (p1 800-1300w /
p2 450-700 / p3 250-400, floors enforced), editorial system prompt (zero
invented facts, dash swap, clean HTML, no marketing), 3/run + 15/day caps,
model option default gpt-4o, drip handoff, /nadlan/v1/enc-writer-status.
Intake stores enc_priority for future batches; 197 existing skeletons
default tier 2 until backfill.
INCIDENT (OPEN): owner installed a "ChatGPT connector" plugin -> sitewide
500 incl. wp-json/wp-login; all remote channels dead (even static probes
500). Recovery steps sent: WP recovery-mode email OR hosting file-manager
rename of newest plugin folder. POST-RECOVERY CHECKLIST: deploy 1.72.29,
backfill enc_priority from handoff/research/encyclopedia/ontology-batch-1.json,
trigger one writer tick, eye-QA first article, verify drip schedule, ensure
crashed connector fully removed.

## 2026-07-07 (2) - v1.72.28: WIKIPEDIA-DEPTH DECISION + gate raised to 250w
OWNER: term pages look short, wants Wikipedia-length per term. MY CALL
(delivered in chat): TIERED depth like Wikipedia itself - priority 1
(~400-600 searched entries): 800-1300w full structure (definition, background,
tech spec, IL regulatory context, on-a-real-project, worked example, common
mistakes, related, sources, table where fitting); priority 2: 450-700w;
priority 3: 250-400w solid, no padding (filler = the actual scaled-content
risk + owner's no-AI-filler law). ~1.5-2M words at full build.
SHIPPED: intake publish gate 120w -> 250w (drip entry requires a real
article; shorter stays draft); fill-path threshold aligned. UPGRADED STAGE-2
PROMPT delivered in chat (Hebrew, tiered lengths, 10 articles/response, table
requirement for p1, zero-invented-facts + dash law baked in).
NOTE: current 197 staged drafts are stage-1 skeletons BY DESIGN - they carry
one-line defs and are NOT public; they publish only when their tiered
articles arrive and pass the 250w gate.
## 2026-07-07 (1) - v1.72.27: intake stage-2 fill path (pre-emptive bug kill)
CAUGHT BEFORE IT BIT: the intake skipped ANY existing title - so the owner's
stage-2 article upload would have skipped all 197 staged drafts. FIX: an
existing DRAFT with <120 words + incoming content_html = filled in place and
scheduled onto the drip; published/future terms are never overwritten.

## 2026-07-06 (26) - ENCYCLOPEDIA BATCH 1 INGESTED: 197 ontology drafts staged
Owner ran the mega-prompt on ChatGPT Pro and uploaded batch 1: 200 rows,
PERFECT schema compliance (all 8 fields, 12 entity types, 12 domains, 0 long
dashes, 0 in-batch dupes, 100% name_en coverage). Distribution: 45 terms /
35 materials / 25 tools / 25 methods / 18 roles / 18 regulations / 15
standards / 10 formulas / 5 software / 2 orgs / 1 publication / 1 person.
INGESTED via /nadlan/v1/glossary-intake: 199 created as DRAFTS (stage-1 rows
carry no content_html - articles come from stage 2 "כתוב מאמרים לבאצ' 1").
1 exact dupe auto-skipped (שיעור היוון exists). ANTI-CANNIBALIZATION PRUNE:
deleted drafts טופס 4 + תעודת גמר (existing indexed page covers both).
NET: 197 staged drafts awaiting articles. "דמי שכירות ראויים" kept (crude
consumer filter false-positive - it is a professional appraisal term).
Source archived handoff/research/encyclopedia/ontology-batch-1.json.
NEXT: owner runs stage 2 on the same ChatGPT thread (50 articles/response) ->
upload -> intake matches by title, fills content, schedules the 12/day drip.
## 2026-07-06 (25) - MEGA INGEST: DUO x4 LANGUAGES LIVE (flagship set complete) + 17 dev profiles
COWORK DELIVERED SIX (drafts 5184-5190, all validated: 0 long dashes):
1) DUO TRANSLATIONS (JOB 3 - the last flagship gap): en 6,118w / fr 6,810w /
   ru 5,098w / ar 4,866w, 13 h2 each. CREATED SIBLINGS 5194(en)/5195(fr)/
   5196(ru)/5197(ar), slugs duo-tel-aviv-<lang>, 15 showroom meta fields
   copied verbatim from HE parent 4893 (incl. project_3d_units w/ interiors,
   model, lat/lng). LIVE-VERIFIED duo-tel-aviv-en: 3D payload + model-viewer +
   6,202w article + weaver frames (81) + units + catalog exclusion intact.
   ALL FIVE FLAGSHIPS NOW COMPLETE IN 5 LANGUAGES. FAMILIES UPDATE:
   4893:[5194,5195,5196,5197].
2) DEVELOPERS BATCH-2 (17 sourced profiles incl. Shikun&Binui, Hagag, Alrov,
   Tshuva, Ashdar, Azorim, Aura...): stored developer_profile/developer_name
   meta across whole families (rainbow=Israel Canada x5, dimri=Y.H. Dimri x5,
   DUO=Africa Israel x5, ZOHI 4747=Levinstein/Mivne/Allied). 13 profiles
   unmapped (no unambiguous project) - archived for the developers directory
   idea. Source: handoff/research/developers/2026-07-06-batch-2.html.
3) ZOHI ARTICLE (5190, 3,670w): PARKED, NOT APPLIED - ZOHI page already
   carries 3,755 words; replacing would not be an upgrade (no-downgrade law).
   Archived handoff/content/zohi-article-he-PARKED.html. OWNER DECISION:
   swap, merge best-of, or discard.
ALSO NOTED: Cowork re-ran JOB 2 (duo interiors) - media 5191 duplicates the
already-wired 5122; parked, not wired. Cowork should mark jobs 2+3+4+8 DONE.
All 6 drafts deleted per protocol. Caches purged via sibling snippet.
## 2026-07-06 (24) - v1.72.26 ENCYCLOPEDIA INTAKE + mega-prompt delivered (owner mega-project)
OWNER SCOPE EXPANSION: full world - not only terms/materials/tools but PEOPLE
(researchers, famous architects), ORGANIZATIONS (biggest companies world+IL),
REGULATIONS (תקנות תכנון ובנייה, תמ"א), STANDARDS (תקן 413 etc), PUBLICATIONS,
FORMULAS, SOFTWARE. Target: beat Designing Buildings Wiki (7,500 articles,
5M/yr). Owner runs the research himself on ChatGPT Pro extended / Gemini (ONE
mega multi-prompt, delivered in chat) - Cowork bypassed (busy). PACE DECISION
(owner asked my opinion, delivered in chat): 10-15/day via scheduled drip is
legitimate for genuine reference content; start 10-12/day, watch GSC, ramp.
SHIPPED v1.72.26: inc/glossary-intake.php -
- meta name_en/entity_type/enc_domain/enc_sources/enc_related on nadlan_term
  (12 entity types validated).
- POST /nadlan/v1/glossary-intake: JSON entries batch -> content-bearing rows
  scheduled as FUTURE posts on a drip (per_day param, default 12, spread
  09:00-19:00, resumes after latest scheduled term, never bulk-dumps);
  ontology-only rows -> drafts awaiting articles; title dupes skipped;
  domain -> nadlan_term_cat.
- EN-term chip rendered under term titles (dir=ltr pill).
Existing engine reused: DefinedTerm schema, autolinker (4 links/page cap),
thin guard, A-Z archive. INTAKE FLOW: owner runs mega-prompt -> pastes/uploads
result -> I validate (dash law, dupes, cannibalization flags, entity types) ->
POST to intake -> drip runs itself. Hub pages per domain + schema name_en
inclusion queued for the first real batch.

## 2026-07-06 (23) - INCIDENT + v1.72.25: catalog 404 healed + TRUE free month + dev batch ingest
INCIDENT (owner report): /projects/ + /professionals/ + ALL project singles
404. Root cause: CPT rewrite rules dropped (stale rules survived a deploy
window while the plugin was mid-swap). FIX: flush_rewrite_rules via snippet -
all 200 within minutes (530 rules, 30 project rules regenerated). HARDENING
SHIPPED (v1.72.25): final-hardening.php re-flushes rules automatically on
every NADLAN_CONFIG_VERSION change (option nadlan_rw_flushed_for) - the
catalog can never silently drop again.
TRIAL DECISION (owner delegated discretion; web search down, decision from
established knowledge + earlier Morning research): KEEP the free first month
and make it TRUE. Rationale: supply-side marketplace - an empty directory
converts nobody; no-card trials maximize professional signups (2-10x) and
nobody in the IL market (Yad2 upfront bundles, Madlan sales-call subs) offers
a clean self-serve free month = differentiator. IMPLEMENTED: WC coupon
'firstmonth' (id 5183, 100%, product 476 only, 1/user, individual use),
auto-applied in cart via funnel.php when Pro present -> first checkout is a
GENUINE 0, no card; renewal engine (v1.72.24) bills 349 at day 27. Premier
(749) stays paid-now by design (serious-buyer filter + revenue-now path).
Product 476 renamed honestly: "Pro - ... (חודש ראשון חינם, לאחר מכן 349 לחודש)".
COWORK DEV BATCH-1 (draft 5182) INGESTED: 7 developer profiles (Israel
Canada, Africa Israel, Y.H. Dimri, Avisror, Mivne, Nachmias, Gindi) - stored
as developer_profile/developer_name meta on unambiguous flagships (rainbow
4464=Israel Canada, dimri 4745=Y.H. Dimri), full batch committed
handoff/research/developers/, draft deleted per protocol. DISPLAY DECISION
FLOATED: an "about the developer" block on project pages would use this meta
(new block, not a text change - safe to add).

## 2026-07-06 (22) - v1.72.24 RENEWAL ENGINE: month-2 revenue machine (owner core-business)
RESEARCH (web): the Morning WooCommerce gateway natively supports WooCommerce
Subscriptions + card tokens (changelog: "improved WooCommerce Subscriptions
integration", "replacing a token for existing subscriptions"); GreenInvoice
API supports charge-by-token. INDUSTRY STANDARD = WC Subscriptions plugin
(paid, ~$239/yr) + this gateway -> fully automatic monthly token charges.
OWNER DECISION QUEUED: buy WCS for full autopilot.
SHIPPED NOW (zero purchases, zero blockers): inc/renewals.php -
- twicedaily cron nadlan_renewals_tick: paid cards (pro/premier) expiring
  within 3 days (or up to 7 days past) -> auto-create a WC renewal order for
  the SAME product + SAME card (_nadlan_card_id item meta preserved so the
  existing woocommerce_payment_complete pipe re-activates and STACKS
  campaign_end), bill copied from the last order, WC customer-invoice email
  with the one-click order-pay link (Morning card/Bit/GPay).
- Same-cycle guard (renewal_cycle_end), open-order dedupe, guest orders
  skipped (manual via lead inbox), stale pending renewals auto-cancelled
  after lead+grace+1 days, everything logged as order notes.
- Existing downgrade cron unchanged (tier drops at expiry; late payment
  within grace re-activates from payment date).
ENTITLEMENT PIPE VERIFIED (read): products 476/477/489/490 -> paid_tier +
campaign_end stacking + auto-downgrade already existed and works; the ONLY
missing piece was renewal order creation = now closed.
STILL OWNER: (a) "first month free" vs 349-now mismatch on product 476;
(b) WCS purchase decision for token autopilot; (c) WC transactional email
FROM/deliverability sanity (order emails ride core WC, not the marketing
email project - but worth one test purchase end-to-end).

## 2026-07-06 (21) - FUNNEL ROUND 3: THE PAYMENT PIPE WAS ARMED ALL ALONG (correction)
OWNER WAS RIGHT: my round-2 "GreenInvoice key missing" was WRONG-LENS. I was
probing our custom recurring module (nadlan_gi_api_key - EMPTY, module
designed for GI payment-page IPN flow, still unarmed). The REAL money path
runs through WooCommerce + wc-gateway-greeninvoice (official Morning plugin):
license_key present (36ch, activated=yes), 4 gateway types (100/120/150/160),
WooCommerce active, ILS. PRODUCTS ALREADY PUBLISHED: 475 basic 0 / 476 Pro
349 (first month free) / 477 Premier 749 / 489 project campaign 3,990 / 490
promoted listing 299. /join-pro/ ALREADY carries add-to-cart links for all 4
paid products. HEADLESS E2E: add-to-cart 476 -> /checkout/ renders the order
+ THREE live payment methods (Morning credit cards / Bit / Google Pay), zero
JS errors. Stopped before paying (real charge). SELF-SERVE PURCHASE = WORKING.
REAL REMAINING GAPS (floated):
1) RENEWALS: products are simple one-time charges; "349/month" needs either
   WooCommerce Subscriptions, Morning standing-order pages, or our custom
   dunning module armed (nadlan_gi_api_key + plan URLs). Month-2 revenue is
   currently manual.
2) COPY/PRICE MISMATCH: product 476 says "first month free" but checkout
   charges 349 now - either rename or configure a trial. Trust risk at the
   exact moment of payment.
3) The custom greeninvoice-recurring module (dunning/reconcile/IPN) stays
   unarmed until its own key/urls are set - fine while WC handles charges.
COWORK SWEEPS 6-7 (drafts 5161-5180): echoes of OUR OWN meta (facilities from
project meta; prices 7 real values already in meta, 954 NONE) - nothing to
ingest; drafts deleted per protocol. Owner chose "enrich ~20 named projects"
externally - Cowork proceeding; those batches WILL carry new info.

## 2026-07-06 (20) - v1.72.23 FUNNEL ROUND 2: one-step signup, advertiser form, /pricing/ fix
AUDIT FINDINGS (money paths, headless + config):
- users_can_register=true, default_role=subscriber (self-serve possible) BUT
  the wizard gate handed visitors to wp-login screens; wp_registration_url()
  loses the return path and the default flow is an email round-trip = classic
  drop-off. FIXED: inline quick-register on the gate itself - name+email ->
  POST /nadlan/v1/quick-register (creates user, auto-login cookie, honeypot,
  5/hour/IP rate limit, existing email -> 409 with login link, new-user
  notification doubles as set-password email) -> page reloads INTO the wizard.
- /advertise/ had strong copy but WhatsApp-only conversion. FIXED: native
  call-back form (name/phone/interest select incl. project-flag/claim/pro-tier)
  appended via the_content filter, posts to /nadlan/v1/lead with
  context=advertiser:<topic>, honeypot, inline validation.
- /pricing/ 301-guessed to an article about apartment pricing. FIXED:
  template_redirect 301 -> /join-pro/.
- CRITICAL BLOCKER FLOATED TO OWNER: GreenInvoice API key NOT configured
  (gi_key_present=false) - the recurring billing module is unarmed; the Pro
  tier (349/mo seen on cards) has NO self-serve payment path. Join-pro leans
  on 1 WhatsApp link. Owner can push the key via /nadlan/v1/keys pattern
  (needs a gi field added) or paste like the OpenAI key.
NEW MODULE inc/funnel.php (loader wired). Gate CSS in wizard inline styles.
NEXT ROUNDS: headless click-through of the logged-in wizard (AI step incl.),
GreenInvoice checkout wiring once key arrives, competitor benchmark
(Madlan/Yad2 pro onboarding), lead-inbox ops view sanity.

## 2026-07-06 (19) - OPENAI KEY LIVE + FR GUIDE PUBLISHED + funnel audit round 1 (v1.72.22)
KEY: owner pasted in chat (his call); written via /nadlan/v1/keys, validated
server-side against api.openai.com: HTTP 200, 120 models visible. AI features
alive. Rotation reminder queued (key passed through chat). NOTE: health.php
openai probe hits /v1/models WITHOUT auth - its 401 is reachability only, not
key validity; keytest snippet pattern is the real check.
COWORK CORRECTION RELAYED: Cowork claimed geo drafts still pending + lat/lng
"still 0" - STALE/BUGGY read on its side; 954 coords ingested hours ago
(958 live on the map), drafts 5143-5152 deleted per protocol. Cowork must NOT
write coordinates directly. Owner chose JOBS 6-8 (data sweeps) next.
FR GUIDE (JOB 5) PUBLISHED: post 5156 -> /acheter-appartement-israel-2026/,
4,171 words, 0 long dashes, verified 2026 figures (8%/10% @ 6,055,070 frozen
to 01/2028; oleh 0%/0.5% @ ~1.988M; LTV 50/75/90), title/slug/category set,
Yoast meta, 12-item guide_faq_json -> FAQPage schema live, guide_lang=fr meta
(html lang filter for fr = TODO next release), hub French section now links it.
FUNNEL AUDIT ROUND 1 (owner god-mission, money paths):
- /contact/ 404 but premium catalog developer CTA pointed there = dead money
  path -> repointed to /advertise/ (v1.72.22).
- /post-listing/ page title carried an em dash -> swapped per dash law.
- /pricing/ 301s to an article about apartment pricing (semantic trap for a
  developer looking for OUR pricing) - FLOAT: reserve /pricing/ for the
  commercial page. /join/ -> /join-pro/ 200 ok (Pro/Premier/campaign tiers).
- /post-listing/ + /advertise/ + /join-pro/: no native <form> elements found
  (wizard is JS-driven; advertise/join-pro lean on WhatsApp links). DEEP
  HEADLESS CLICK-THROUGH of the wizard + join flows = next round (task).
- greeninvoice probe: reachable (404 on bare API root is expected unauth).

## 2026-07-06 (18) - v1.72.21: buyer-mode map + free-look window + notranslate + hub link
OWNER DIRECTIVES BATCH: simple key handoff (offered to paste in chat - accepted,
see chat), link the hub, near-me with minimum user effort (IP approximation),
premium flags w/ 3D badge on map, default view TLV-JLM core, buyer language
not map-splaining, window view must be lookable not a still, Rainbow AR
machine-translate mangling (tabs/logo), JOB 7 waiting - keep floating.
SHIPPED:
- MAP: default camera [34.86,31.95] z8.6 (TLV-JLM-Holon-Rishon core), terrain
  relief (mapbox-dem 1.35x) + sky; featured projects w/ non-city geo fly a
  FLAG marker (pole + dark card + model poster thumb + 3D chip) outside the
  clusters, one click to the project; silent ipwho.is IL-only ease-to visitor
  area (no permission), "Projects near me" button (5 langs) uses browser
  geolocation on demand; sub/note rewritten to buyer language ("Where do you
  want to live?"), technical map-splaining removed.
- WINDOW: winCam now setPitchBearing (pitch 86 eye-level, clamp 35-96);
  drag on the stage = look sideways/down/up (bearing 0.35deg/px, vert
  0.22deg/px, clamp -45..+10); turn buttons preserved; notes rewritten x5.
- NOTRANSLATE: lang switcher/[data-act=lang]/brand/model-viewer/langbar get
  translate=no + notranslate class in afterRender (Chrome translate was
  translating language tabs + AR badge on Rainbow).
- HUB LINKED: intl band on HE homepage now carries the /en/buy-property-in-israel/
  link alongside Explore in English.
FLOATS logged for chat: DUO translations still pending (flagships must be
perfect x5 langs - owner demo priority), JOB 7 facilities stalled on Cowork
side, premium flags currently = 4 flagships only (others need non-city geo +
featured flag = the monetization lever).

## 2026-07-06 (17) - v1.72.20: DRONE MAP SHOWCASE on homepage + premium (owner ask)
OWNER: drone map on the front page + premium, "very very professional". MY
CALL (relayed): yes - but as a DESIGNED band, not the collapsible toggle;
showcase mode = LIVE eyebrow badge, Frank Ruhl title, sub line, 560px stage
w/ gold shadow frame, boots via IntersectionObserver (rootMargin 260px) so
the homepage LCP pays nothing. Placement: spliced at runtime right after the
flagships band (hero -> flagships 3D -> live map = the differentiator front
door), all 5 language homepages; premium page gets it under the grid.
nadlan_drone_map_band($mode,$lang) + nadlan_drone_map_i18n (title/sub/note/
popup labels x5). Catalog keeps toggle mode. Point popups dir=auto.

## 2026-07-06 (16) - EN INVESTORS HUB LIVE + geo drafts closed + /en/ title dash swap
HUB: page 5154 https://nad-lan.co.il/en/buy-property-in-israel/ (child of /en/
homepage 5011 - hierarchy, zero cannibalization: /en/=brand home, hub=buyer
intent "buy property in israel from abroad"). Content: buyer-addressed EN,
~1,600 words own content, 2026 numbers CONSISTENT with the published EN guide
(8%/10% @ 6,055,070; 50% LTV non-resident; Sale Law arvut bankit; TLV yields
3-3.6%; Sde Dov 1,300 dunams/16,000 homes), 7-step remote purchase process,
city map for international buyers, language sections incl. Gulf/Abraham
Accords positioning (respectful, factual), 6-question FAQ + FAQPage JSON-LD
inline, honest disclaimers, links: premium/3 EN flagships/catalog/EN guide.
Yoast title/desc/focuskw set. Live-verified: schema present, 5/5 links, no
long dashes in our content. Source committed handoff/content/.
DASH SWEEP: /en/ page 5011 title carried an em dash (pre-existing) leaking
into breadcrumb JSON-LD - swapped to hyphen per dash law.
GEO PROTOCOL CLOSED: drafts 5143-5152 deleted after ingest; Cowork asked
"write coordinates directly now?" - ANSWER RELAYED TO OWNER: NO, already
ingested by cloud agent (double-write hazard).
OPEN: hub not yet in any nav/menu (floated to owner - recommend footer +
/en/ homepage link); FR guide (JOB 5) incoming -> link from hub French
section when published; SEO plugin question answered in chat (keep Yoast,
no Rank Math - conflict, not a lever).

## 2026-07-06 (15) - GEO EXPEDITION INGESTED + v1.72.19: 958 projects on the map, clustered
Cowork JOB 1 delivered 10 CSV drafts (5143-5152): 957 rows, 954 valid
(12 neighborhood / 942 city centroid via Nominatim, source URL per row),
3 NONE, 0 out-of-box. Bulk server-side ingest via temp snippet: 954 written
(lat/lng/geo_confidence), existing coords skipped (flagships untouched),
drafts to delete after verify. project-map endpoint was CAPPED at 200 -
uncapped (-1). v1.72.19:
- DRONE MAP CLUSTERED: geojson source cluster:true r44, gold cluster bubbles
  with counts, terracotta unclustered points, cluster click = expansion zoom
  or (>=15.5z) popup listing up to 8 projects + "and N more", city-level
  popups say "מיקום ברמת עיר". Band note updated to the honest full-catalog
  wording. 197 Jerusalem projects = one honest bubble, not fake pins.
- CONFIDENCE GATE: geo.confidence ships in engine payload; winstage/winView
  disabled when confidence=city (a window view from a city centroid is
  fiction; flagships/neighborhood keep it).
KNOWN DATA CAVEATS (logged, not blockers): meier-on-rothschild neighborhood
point looks ~3km east of Rothschild (Nominatim match); city centroids shared
by hundreds of projects until facilities sweep (JOB 7) brings addresses.
Cowork proceeding to JOB 5 (FR guide) with 2026 number verification.

## 2026-07-06 (14) - v1.72.18: RFP demo unblock + noindex retirement + key endpoint
OWNER DIRECTIVES: (a) RFP seeded-advisor exclusion REVERTED - demonstration
phase, seeded advisors stay matchable (badge stays in directory; re-add
exclusion before marketing push - IN THE LIST); (b) GSC shows a big
not-indexed pile - "don't leave noindex on contents/listings, take care of
thin content"; (c) key handoff via script, never chat; (d) EN investors hub
next (in progress this turn); (e) RFP must be English + personal.
SHIPPED:
- rfp.php: matcher guard reverted w/ dated comment; AR-page buyers now get the
  ENGLISH doc (was Hebrew - Gulf buyers read English). EN doc + buyer name
  already existed (buyflow sends page lang; verified earlier).
- schema.php: word-floor noindex on nadlan_professional/nadlan_property
  RETIRED (was the main not-indexed driver: ~2,700 professionals under 80
  words). Demo-profile noindex (is_demo) + facet junk guards + glossary stub
  guard + city-hub floor KEPT (true junk protection). RISK FLOATED: thousands
  of similar directory pages entering the index can read low-quality to
  Google; watch GSC after Site Kit connect; enrichment sweeps (Cowork jobs
  6-8) are the real fix.
- keys-hub.php: POST /nadlan/v1/keys {openai_key|anthropic_key|mapbox_token},
  manage_options via app password; never echoes the key (prefix+length only).
  PowerShell handoff script delivered in chat.

## 2026-07-06 (13) - v1.72.17: competitor-gap strike (owner: "close all competitor gaps")
SHIPPED:
- MONTHLY PAYMENT STRIP (Zillow's highest-converting element) in the apartment
  panel: 70% financing / 25y / 5% on price||price_estimate, rounded to 50,
  gold-tinted card, honest note "estimate only, not a financing offer" x5
  langs (mortgage_est/mortgage_note).
- RFP HONESTY GUARD: nadlan_rfp_match_advisors meta_query now requires
  (rating NOT EXISTS) OR reviews_verified=1 - seeded fictional profiles can
  never be named in a buyer document; empty match falls back to the honest
  "team will match an advisor" line.
- PREMIUM DEFAULT WALK: featured projects auto-switch to premium-default-*
  set when it has 4+ spaces (nadlan_showroom_premium_tour + tier in payload,
  dtour_tag_premium x5). Cowork premium set at 1 flat + 1 seam-passed 360
  (5139/5140) - standard remains until the premium set grows.
OPENAI KEY HANDOFF: wp-admin left menu "נדלן מפתחות" (Keys Hub, slug
nadlan-keys) -> OpenAI API Key field -> save. NEVER paste keys in chat.
NEXT (floated): EN investors hub page, real review capture loop, saved-search
alerts (email infra last), per-project video tours.

## 2026-07-06 (12) - v1.72.16: scrollbar kill + DEDICATED per-project walk + #34 demo note
OWNER (Rainbow review): (a) gray scrollbar in the 3D area = frame-in-frame
(it's .nl-panel__scroll, the unit panel over the theater; probe missed it
because no unit was selected); (b) walk must use the project's OWN pictures
when they exist (Rainbow has generated interiors) with a CMS path for
dedicated sets per listed asset; (c) #34 decision: just add a demonstration
note to seeded ratings.
SHIPPED:
- SCROLLBAR: .nl-panel__scroll + .nlbuy__panel scrollbar hidden
  (scrollbar-width none + webkit display none), wheel/touch still scroll,
  bottom fade cue (.nl-panel::after gradient) hints continuation.
- WALK PRIORITY (page tour): 1) dedicated media walk-<slug>-<space>
  (nadlan_showroom_project_walk, 30min transient, sibling slugs normalized to
  parent, same canonical order/aliases/360-exclusion via generalized
  nadlan_showroom_scan_walk_media) -> 2) project's unit interiors as steps
  labeled "{rooms} · קומה {n}" (dtour_tag_units) -> 3) standard default set ->
  4) pending text. Rainbow now walks through its own generated apartments.
  CMS hint added in the showroom metabox (upload title convention, zero saves).
- #34 (owner decision): rating stars without reviews_verified meta get a
  "נתוני דוגמה" badge on directory cards + profile pages. Flip
  reviews_verified=1 per professional when real reviews arrive.
i18n dtour_tag_dedicated/_units x5. Next in chat: worries/leftovers/competitor
gaps float (owner asked).

## 2026-07-06 (11) - v1.72.15 + set ingest COMPLETE: 12-space walk live, 12x lighter
Standard set finished: alias fix (v1.72.14) put the building first; JPEG
conversion done server-side (12 attachments repointed, q82, metadata regen,
PNG originals kept on disk): ~2MB -> 130-370KB each, ~12x lighter walk.
Draft 5137 deleted per protocol. Live payload verified: 12 steps in canonical
order exterior -> entrance -> lobby -> stairwell -> elevator -> entry-hall ->
living-room -> kitchen -> master-bedroom -> second-bedroom -> bathroom ->
balcony, all .jpg.
CATCH (live payload showed 13 steps): Cowork's 360 seam-TEST upload
(standard-default-360-living-room, 2:1 equirect) was swept into the flat walk
by the scanner - would render warped to buyers. v1.72.15: keys starting 360-
excluded from the walk, reserved for the future pannellum layer
(standard-default-360-<space> convention agreed with Cowork).

## 2026-07-06 (10) - v1.72.14 + standard set COMPLETE: 12-space default walk, JPEG diet
Cowork finished the standard-default set (5125-5136, 12 images, draft 5137).
CATCH: building images titled standard-default-building-exterior/-building-
entrance did not match the canonical keys (exterior/entrance) -> would append
at the walk's END with raw English labels. Fixed in the scanner with an alias
map (building-exterior->exterior, building-entrance->entrance, facade->
exterior, bedroom->second-bedroom) so naming variants can never break order
or labels. v1.72.14 shipped.
ALSO THIS TURN (owner said the run is done): converting the 12 PNG originals
(~2MB each) to JPEG q82 server-side (attachment repoint + metadata regen,
PNG originals kept on disk), transient + cache purge, draft 5137 deleted after
ingest per protocol, full-order live verify.
360 LAYER: Cowork will seam-test ChatGPT equirectangular output before any
upload (honest path; fake 360s rejected by both sides). pannellum awaits real
2:1 seamless panoramas as standard-default-360-<space> when a source exists.

## 2026-07-06 (9) - v1.72.13: walk transition honesty fix (load-aware reveal)
Headless QA on 1.72.12 caught it: clicking next updated the label to the new
space while the OLD room stayed on screen (2MB PNGs load slowly; the 220ms
transition revealed before decode). Fix: token-guarded go() keeps the stage in
the faded "doorway" state until img.onload fires (6s failsafe), label/chips
update immediately, rapid clicks cancel stale reveals. Also: default set is
already 6 spaces live (entry-hall joined via the self-maintaining scanner with
zero manual wiring - the feed works). WEIGHT NOTE for later: Cowork uploads are
~2MB PNGs; after the owner's run finishes, converting originals to JPEG q82
would cut the walk's payload ~5x. Do NOT touch media mid-run.

## 2026-07-06 (8) - v1.72.12: THE DEFAULT WALK (owner law: default, not fallback)
OWNER: every page must have the walk-inside/360 experience working with a
DEFAULT standard apartment + building set; "tour pending" dead-ends read as
"we are not working". Cowork (owner-driven) is uploading standard-default-*
media now (5125 living-room, 5126 kitchen, 5127 master-bedroom, 5128
second-bedroom, 5129 bathroom at build time; entry-hall/balcony/exterior/
street-entrance/lobby/stairwell/elevator incoming).
SHIPPED: page-level interior-tour section now renders the DEFAULT WALK when no
developer tour/panoramas exist: first-person step-through viewer (16:10 stage,
drag pans the gaze +-9% with scale 1.12 headroom, walk transition between
spaces, prev/next arrows, door chips, keyboard arrows RTL-aware, preloading).
SELF-MAINTAINING FEED: nadlan_showroom_default_tour() scans media titled
standard-default-* (1h transient, purged on add_attachment), canonical order
building -> apartment (exterior, street-entrance, entrance, lobby, stairwell,
elevator, entry-hall, living-room, kitchen, master-bedroom, second-bedroom,
bathroom, balcony), ships in the engine payload as default_tour. New uploads
appear automatically - zero manual wiring per image.
HONESTY: tag on the stage "standard sample apartment - illustration, the
developer's dedicated tour replaces it" x5 langs; dt_* space names x5 langs.
Priority chain per project: dedicated tour_url > 360 panoramas > DEFAULT WALK >
pending text (now nearly unreachable).

## 2026-07-06 (7) - v1.72.11: the view tab IS the window (owner intent clarified)
OWNER: mvt/מבט must mean STANDING AT THE WINDOW seeing the real world - not an
interior picture. Floor 50 sees one thing, floor 1 another; buyer must know if
the window faces a building, a school, the sea. Interior renders belong to the
upcoming POV first-shooter walkthrough (owner generating room images).
SHIPPED: view tab now renders an INLINE window viewport - dedicated mini
Mapbox (satellite-streets-v12 + sky atmosphere + 3D building extrusions,
non-interactive) with FreeCamera standing at alt = floor*floor_height + 1.6m
at the project lngLat, looking 700m out in the unit's real compass direction.
Look-left/right buttons rotate the gaze in 30deg steps (winLook, per-unit
bearing state). Honest note ("real satellite + buildings, illustration, not a
photo") x5 langs. Interior render demoted to a <details> expandable below;
btn_winview reworded to "continue on the live area map" (the big POI map with
the cone stays one tap away). Engine: winState/winCam/winStageInit/winLook,
setTab inits on view; CSS .nl-winstage__*; i18n winview_note/turn_left/
turn_right/view_interior_label + btn_winview rewrite x5.
NOTE TO SELF: ONE-map doctrine intact - this is a separate purpose viewport
(the window), not a second POI map; non-interactive, removed/rebuilt per open.
SITE KIT: owner's setup link failed = expired one-time nonce in the URL; must
enter wp-admin -> Site Kit menu -> Start setup fresh (explained in chat).

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
