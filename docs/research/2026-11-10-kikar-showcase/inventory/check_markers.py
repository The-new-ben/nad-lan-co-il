# Builds features.csv for the Kikar showcase inventory from the live HTML fetched on 10.11.2026 (plugin 1.72.630).
# Usage: python -I build_inventory.py <live_dir> <out_dir>
import csv, json, os, re, sys

LIVE, OUT = sys.argv[1], sys.argv[2]
PAGES = [('kikar_he', 'hamedina'), ('kikar_en', 'hamedina-en'), ('rainbow', 'rainbow'), ('duo', 'duo'), ('dimri', 'dimri'),
         ('ashira', 'ashira'), ('h_infinity', 'hinf'), ('sde_dov', 'sdedov')]
HTML = {k: open(os.path.join(LIVE, f + '.html'), encoding='utf-8', errors='replace').read() for k, f in PAGES}
JS = {}
for f in os.listdir(os.path.join(LIVE, 'js')):
    JS[f] = open(os.path.join(LIVE, 'js', f), encoding='utf-8', errors='replace').read()

def js_has(fname, s):
    return s in JS.get(fname, '')

WORLD = r'project-stage/world/world\.js'
BRIDGE = r'project-stage/bridge\.js'
W, X, B = 'project-stage_world_world.js', 'project-stage_world_example.js', 'project-stage_bridge.js'

# facilities.json read live (10.11): which projects have 360 rooms and the building walk
FAC360 = {'rainbow', 'duo', 'ashira'}          # rainbow: pools, club, lobby; duo: pool, lobby, club; ashira: 7 rooms
FACWALK = {'rainbow', 'duo'}                    # 'walk' key in live facilities.json
SIGHT = {'rainbow', 'duo'}                      # looksFor names in the 360 windows need a 360 + sight bands

# (id, group, feature, visitor sees/does, code, switch, marker, test, status, built_for, buyer_value, notes)
# test: ('html', regex) | ('htmljs', regex, jsfile, string) | ('set', {pages}) | ('none',)
F = []
def add(*a):
    F.append(a)

# ---------------- A. Page frame, head and SEO
add('A01', 'page', 'H1 with the Hebrew and English name', 'One visible H1: the searched name + the English name', 'inc/project-stage.php nadlan_ps_parts() $hero; nadlan_pt_compose() on pages without a stage', 'config name/name_en (h1_he on Kikar)', 'id="nl-project-page-title"', ('html', r'id="nl-project-page-title"'), '', 'all', 2, '')
add('A02', 'page', 'Kicker under the H1 (developer · place)', 'One line naming who builds and where', 'nadlan_ps_parts() .nlps-kicker', 'config developer, place', 'class="nlps-kicker', ('html', r'class="nlps-kicker'), '', 'stage pages', 1, '')
add('A03', 'page', 'Answer paragraph (.nl-lead)', '4-7 lines answering the search: names, place, status, a dated price', 'inc/legal-notice.php nadlan_lead_extract()', 'first <p> of 100+ chars in the content', 'class="nl-lead"', ('html', r'class="nl-lead"'), '', 'all', 3, '')
add('A04', 'page', 'Hero WhatsApp button', 'A WhatsApp button with the project name in the first fold', 'nadlan_ps_parts() $cta (data-nlps-ev=hero-wa)', 'always on stage pages', 'data-nlps-ev="hero-wa"', ('html', r'data-nlps-ev="hero-wa"'), '', 'stage pages', 4, '')
add('A05', 'page', 'Hero "choose a floor" button', 'Jumps to the 3D stage to pick a floor', 'nadlan_ps_parts() $cta (hero-pick, #nlps-t)', 'stage pages (bridge.js)', 'data-nlps-ev="hero-pick"', ('html', r'data-nlps-ev="hero-pick"'), '', 'R U D A', 3, 'Kikar has hero-world instead (A06)')
add('A06', 'page', 'Hero "tour the square" button (world)', 'Opens the Kikar 3D world', 'nadlan_ps_parts() world branch (hero-world)', 'config world', 'data-nlps-ev="hero-world"', ('html', r'data-nlps-ev="hero-world"'), '', 'Kikar', 3, '')
add('A07', 'page', 'Hero "for sale and rent" anchor', 'Jumps to the sale/rent section (#nlws-sale)', 'project-stage.php line ~1143 (hero-sale)', 'config world', 'data-nlps-ev="hero-sale"', ('html', r'data-nlps-ev="hero-sale"'), '', 'Kikar', 3, '')
add('A08', 'page', 'Hero video-call button', '"שיחת וידאו עם נציג" in the first fold, opens the booking band', 'nadlan_ps_parts() $cta (hero-video -> #nlsch)', 'nadlan_sched_on() and no nadlan_sched_off meta', 'data-nlps-ev="hero-video"', ('html', r'data-nlps-ev="hero-video"'), '', 'stage pages', 4, 'Loop V4 said Kikar had it lower only; it is in the hero now')
add('A09', 'page', 'Hero film button with its length', '"סרטון הפרויקט · N שניות" opens the film dialog at the top', 'nadlan_ps_parts() $cta (hero-film) + footer dialog #nlfilm', 'config film', 'data-nlps-ev="hero-film"', ('html', r'data-nlps-ev="hero-film"'), '', 'Rainbow', 3, 'Kikar has two films but only as sections lower on the page (G02, G03)')
add('A10', 'page', 'Numbered steps under the stage', '1 choose a floor 2 view and map 3 enter the apartment 4 design it', 'nadlan_ps_parts() .nlps-steps; bridge.js [data-nlps-step]', 'step 3 only when tour/living-25w-card.jpg exists', 'data-nlps-step', ('html', r'data-nlps-step'), '', 'stage pages', 2, 'Kikar world has its own 3-step picker (F03)')
add('A11', 'page', 'Rail: professional square / "רוצה להופיע כאן?" slot', 'An ad card of a real professional, or an invitation to appear', 'nadlan_ps_square(), nadlan_ps_slot()', 'config rail (post ids); Hebrew pages', 'data-nlps-ev="slot"', ('html', r'data-nlps-ev="slot"'), '', 'R (Meital); slot on all', 1, '')
add('A12', 'page', 'Six quick facts tiles', 'Value + source line per fact', 'nadlan_ps_parts() .nlpf', 'config facts', 'class="nlpf', ('html', r'class="nlpf'), '', 'stage pages', 4, '')
add('A13', 'page', 'Progress ladder', 'Done / now / next with dates', 'nadlan_ps_parts() .nlprog', 'config progress', 'class="nlprog', ('html', r'class="nlprog'), '', 'stage pages', 3, '')
add('A14', 'page', 'Milestone tracker band', 'The road from planning to keys from the project_status meta', 'inc/milestones.php (.nlms-*)', 'project_status meta; not printed on stage pages', 'class="nlms-', ('html', r'class="nlms-'), '/projects/gindi-vogue-sde-dov/ has class="nlms-"', 'non-stage projects', 2, 'Seen on /projects/gindi-vogue-sde-dov/')
add('A15', 'page', 'Non-affiliation notice', '"אתר עצמאי · עמוד זה אינו האתר הרשמי של..."', 'inc/legal-notice.php nadlan_project_notice_render()', 'developer_name meta; article wrapper', 'class="nl-projnotice', ('html', r'class="nl-projnotice'), '', 'all', 1, '')
add('A16', 'page', 'FAQ accordion + one FAQPage JSON-LD', 'Visible questions; FAQ rich data', 'nadlan_ps_compose() FAQ pass; inc/schema-meta.php _nl_faq_schema', 'Hebrew h2 "שאלות נפוצות" + h3/p pairs', '"@type":"FAQPage"', ('html', r'"@type":\s*"FAQPage"'), '', 'all', 2, 'Missing on Ashira')
add('A17', 'page', 'Breadcrumbs + language switcher at the top', 'בית › פרויקטים › name, and links to the language pages', 'inc/project-topbar.php (.nlptop), inc/breadcrumbs.php', 'project pages', 'class="nlptop"', ('html', r'class="nlptop"'), '', 'all', 1, '')
add('A18', 'page', 'ApartmentComplex JSON-LD', 'Structured data: geo, address, amenities', 'inc/schema.php', 'project meta', '"ApartmentComplex"', ('html', r'ApartmentComplex'), '', 'all', 1, '')
add('A19', 'page', 'VideoObject JSON-LD for the project film', 'Lets Google show the film as a video result', 'project-stage.php film block (nadlan-ps-film)', 'config film', '"VideoObject"', ('html', r'"VideoObject"'), '', 'R U D', 2, 'Kikar has two films (G02, G03) and no VideoObject')
add('A20', 'page', 'AggregateOffer price range in the schema', 'Price range in structured data (the pages ChatGPT cites carry one)', 'inc/schema.php (offers)', 'sourced price meta', '"AggregateOffer"', ('html', r'"AggregateOffer"'), '', 'Rainbow', 2, 'Kikar has sourced deals 9.58-10.63M but no AggregateOffer')
add('A21', 'page', 'SoftwareApplication JSON-LD for the tools', 'Each embedded tool marked as an app for search', 'inc/instruments.php (#nadlan-nli-ld)', 'a [nadlan_tool] on the page', 'id="nadlan-nli-ld"', ('html', r'id="nadlan-nli-ld"'), '', 'pages with the kit', 1, 'Comes with C01')
add('A22', 'page', 'Poster painted first (LCP)', 'The picture appears at once; the 3D loads after', 'nadlan_ps_poster_set() preload + srcset', 'config poster / world.poster', 'rel="preload" ... poster', ('html', r'rel="preload"[^>]+poster'), '', 'stage pages', 2, '')
add('A23', 'page', 'Feature bar', 'A row of tiles naming what the page can do', 'inc/feature-bar.php (.nlfb-*)', 'project pages', 'class="nlfb-row', ('html', r'class="nlfb-row'), '', 'all', 2, '')
add('A24', 'page', 'Facility chips in the hero', 'Booking-style chips (pool, spa...) linking to /premium/?fac=', 'inc/facility-chips.php (.nlfc-*)', 'project_facilities meta or premium row', 'class="nlfc-chip', ('html', r'class="nlfc-chip'), '', 'where data exists', 2, 'Kikar Hebrew yes, English no')
add('A25', 'page', 'Surroundings band (catalog context)', 'Project context tiles, nearby, FAQ from the catalog', 'inc/catalog-plus.php (.nlcp-*)', 'catalog row', 'class="nlcp-', ('html', r'class="nlcp-'), '', 'most projects', 1, 'Not on DUO')
add('A26', 'page', 'Area price line (city median)', 'A neutral area price signal under the lead', 'inc/area-price-line.php (.nl-areaprice)', 'wp_nadlan_deals with 5+ deals', 'class="nl-areaprice', ('html', r'class="nl-areaprice'), '', 'none seen', 1, 'CSS loads on project pages; no element on any checked page (deals table empty)')
add('A27', 'page', 'Sde Dov quarter-tour teaser band', 'A band inviting to the /tour/sde-dov/ 3D quarter tour', 'inc/sdedov-teaser.php (.nlsdt)', 'slugs in the quarter list', 'class="nlsdt', ('html', r'class="nlsdt'), '', 'Sde Dov quarter', 1, '')
add('A28', 'page', 'Accessibility panel', 'Text size, contrast and reset', 'inc/accessibility.php (#nla11y)', 'site-wide', 'id="nla11y"', ('html', r'id="nla11y"'), '', 'site-wide', 1, '')
add('A29', 'languages', 'Language sibling pages + hreflang', 'The page in en/fr/ru/ar with a two-way hreflang cluster', 'inc/project-lang.php, inc/lang-pages.php', '<slug>-en/-fr/-ru/-ar posts', 'hreflang="en"', ('html', r'hreflang="en"'), '', 'R U D A Kikar', 3, 'Kikar fr/ru/ar fetched 200 with world.js; H Infinity none')

# ---------------- B. Prices and data
add('B01', 'prices', 'Price guide "מחירון · עודכן"', 'A dated price block: average per m2, published deals, WhatsApp for the price list', 'Rendered by scripts/project-stage/price_guide/render.py into the LIVE inc/project-stage.php (not in the repo copy)', 'per-project block in the live file', 'id="nlpg"', ('html', r'id="nlpg"'), '', 'all', 5, 'Repo inc/project-stage.php has no nlpg: live and repo differ')
add('B02', 'prices', 'Sold deals table by floor', 'Floor, apartment, price, per m2, date; a row can open that floor', 'nadlan_ps_deals(); config deals/deals_intro/deals_sum', '2+ sourced rows', 'id="nlps-deals"', ('html', r'id="nlps-deals"'), '', 'R U Kikar', 5, 'Hebrew only; not on Kikar English')
add('B03', 'prices', 'Deal rows that open their floor in 3D', 'Tap a deal: the stage jumps to that floor', 'nadlan_ps_deals() data-nlps-floor', 'deal n > 0 (tower known)', 'data-nlps-floor', ('html', r'data-nlps-floor'), '', 'R U', 3, 'Kikar deals have n=0 (tower not published)')
add('B04', 'prices', 'Deals inside the apartment card ("מידע גלוי")', 'Range, average, per m2 and the towers average in the chosen apartment card', 'world.js (dealsH, towersAvg)', 'config deals (world)', WORLD + ' + world.js "dealsH"', ('htmljs', WORLD, W, 'dealsH'), '', 'Kikar', 5, '')
add('B05', 'prices', 'Floor note: a sold deal on the picked floor', 'The floor card names a sold deal on that floor', 'bridge.js floorNote() from deals[].note', 'config deals with note, lowNote/highNote', BRIDGE + ' + config', ('set', {'rainbow', 'duo'}), '', 'R U', 3, 'Data-driven; set from config (live bridge has floorNote)')
add('B06', 'prices', 'RadiusPrices: deals within 500 m, official median, projects within 1.5 km', 'Median per m2 by rooms and year, the latest deals, the neighbourhood median, nearby projects', 'inc/radius-prices.php [nadlan_radius_prices]; data/radius-prices.json', 'shortcode in content; 5+ deals', 'id="nlrp"', ('html', r'id="nlrp"'), '', '28 projects', 5, 'Hebrew only; not on Kikar English or Ashira')
add('B07', 'prices', 'Price band + nearby projects per-m2 comparison', '"מחיר: איפה הפרויקט עומד מול הסביבה" with a comps table', 'inc/project-experience.php nadlan_pjx_price_band(), REST /nadlan/v1/comps', 'project_3d_avg_price_per_sqm meta', 'id="nlpjx-comps-data"', ('html', r'id="nlpjx-comps-data"'), '', 'all', 4, '')
add('B08', 'prices', 'Money, advisors and designers block', 'Monthly estimate, paid advisors, interior designers', 'nadlan_pjx_bottom() (#nlpjx-finance)', 'project pages', 'id="nlpjx-finance"', ('html', r'id="nlpjx-finance"'), '', 'all', 2, 'Baseline FORGOTTEN row 40: empty heading risk')
add('B09', 'prices', '"Everything around the project" links', 'Developer, professionals, calculators, guide, glossary', 'nadlan_pjx_bottom() (#nlpjx-world)', 'project pages', 'id="nlpjx-world"', ('html', r'id="nlpjx-world"'), '', 'all', 2, '')
add('B10', 'prices', 'ProjectFacts with linked sources and a checked date', 'Each fact with its source as a link under "checked on"', 'inc/project-facts.php [nadlan_project_facts]; data/project-facts.json', 'shortcode; not on stage pages', 'id="nlfx"', ('html', r'id="nlfx"'), '', 'H Infinity + 22 pages', 3, 'Kikar has facts tiles and a facts table instead (A12, F13)')
add('B11', 'prices', 'NeighbourCompare spotlight', 'The project as hero with one price range, three nearby projects as cards', 'inc/neighbour-compare.php; data/neighbour-spotlight.json', 'page id in the JSON (6 radius pages)', 'class="nlnb"', ('html', r'class="nlnb"'), '/projects/gindi-vogue-sde-dov/ has class="nlnb"', '6 Sde Dov pages', 3, '')
add('B12', 'prices', '"מחיר מוערך" label on map price chips', 'Every price chip says estimate, per m2, not binding', 'project-experience.php NLPJX_PRICE (v101)', 'branch claude/apartment-experience-b1 only', 'מחיר מוערך', ('html', r'מחיר מוערך'), '', 'all (planned)', 2, 'Not found on any live page')

# ---------------- C. Tools
add('C01', 'tools', 'ProjectToolkit: 4 tools preset for the project', 'Tabs: all the costs (pcost), construction index (indexation), purchase tax (ptax), late delivery (delay); opens with the project price range', 'inc/project-kit.php [nadlan_project_kit]; assets/instruments/', 'shortcode in the content; never Ashira (Ben)', 'id="nlkit"', ('html', r'id="nlkit"'), '/projects/gindi-vogue-sde-dov/ id="nlkit"', 'R U D H + radius pages', 5, 'Kikar content has no [nadlan_project_kit]')
add('C02', 'tools', 'Tool share bar: copy result, WhatsApp, print', 'Copy the computed result, send it on WhatsApp, print it', 'assets/instruments/core.js (nli__share)', 'any [nadlan_tool]', 'assets/instruments/core.js', ('html', r'assets/instruments/core\.js'), '', 'pages with tools', 4, 'The only result-sharing feature on project pages')
add('C03', 'tools', 'Purchase tax calculator (ptax)', 'Tax by the brackets in force: single, additional, foreign resident', 'assets/instruments/tools/ptax.js', 'kit or /purchase-tax-calculator/', 'tools/ptax.js', ('html', r'tools/ptax\.js'), '/purchase-tax-calculator/ loads tools/ptax.js', 'site', 5, 'Kikar: basket computes tax (H07) and a text section (F13) only')
add('C04', 'tools', 'Total purchase cost (pcost)', 'Price + tax + lawyer + broker + indexation + moving, from a contractor', 'tools/pcost.js', 'kit or /apartment-purchase-cost-calculator/', 'tools/pcost.js', ('html', r'tools/pcost\.js'), '/apartment-purchase-cost-calculator/ loads tools/pcost.js', 'site', 5, '')
add('C05', 'tools', 'Construction input index calculator (indexation)', 'Indexation add-on by the payment schedule (Sale Law amendment 9)', 'tools/indexation.js; data/cbs-200010.json', 'kit or /new-projects/construction-input-index/', 'tools/indexation.js', ('html', r'tools/indexation\.js'), '/new-projects/construction-input-index/', 'site', 5, 'Key for an off-plan buyer like Kikar')
add('C06', 'tools', 'Late delivery compensation (delay)', 'Section 5A compensation month by month', 'tools/delay.js', 'kit or /new-projects/contractor-delay-compensation/', 'tools/delay.js', ('html', r'tools/delay\.js'), '/new-projects/contractor-delay-compensation/', 'site', 4, 'Kikar delivery is disputed 2026-2028')
add('C07', 'tools', 'Property value estimator (pval)', 'An estimate of an apartment value from area data', 'tools/pval.js', '/property-value-estimator/', 'tools/pval.js', ('html', r'tools/pval\.js'), '/property-value-estimator/ loads tools/pval.js', 'site', 3, 'Not on any project page')
add('C08', 'tools', 'Tel Aviv arnona 2026 (arnona)', 'Municipal tax for an apartment by zone and size', 'tools/arnona.js; data/arnona-tlv.json', '/arnona/', 'tools/arnona.js', ('html', r'tools/arnona\.js'), '/arnona/ loads tools/arnona.js', 'site', 3, 'Kikar is in Tel Aviv: monthly cost of a 140 m2 home')
add('C09', 'tools', 'Repayment capacity (afford)', 'Which apartment a household can buy', 'tools/afford.js', '/mortgage-calculator/mortgage-repayment-capacity/', 'tools/afford.js', ('html', r'tools/afford\.js'), '/mortgage-calculator/mortgage-repayment-capacity/', 'site', 3, '')
add('C10', 'tools', 'Mortgage by tracks + 16 mortgage tools (incl. mkeys "from contract to keys")', 'Monthly payment by tracks; payments, indexation and mortgage from contract to keys', 'tools/mortgage.js, mkeys.js, mquick.js ...', '/mortgage-calculator/', 'tools/mortgage.js', ('html', r'tools/mortgage\.js'), '/mortgage-calculator/ loads 16 tools', 'site', 4, 'Kikar shows only the ~90 m2 finance line (B08)')

# ---------------- D. The 3D stage (Rainbow, DUO, Dimri, Ashira)
add('D01', 'stage', 'Per-project 3D stage (three.js)', 'White model at golden hour on the real lot and city; poster first', 'assets/project-stage/<dir>/stage.js mount<Name>Stage()', 'nadlan_ps_config() dir/mount; option nadlan_project_stage', 'project-stage/<dir>/stage.js', ('html', r'project-stage/[a-z]+/stage\.js'), '', 'R U D A', 4, 'Kikar uses the world engine instead (F01)')
add('D02', 'stage', 'Quarter legend chips + "facilities" pill on the model', 'Chips show facilities / existing / under construction / marketing / permit stage', 'nadlan_ps_parts() $legend; stage.focusPhase()', 'quarter.json', 'data-nlps-phase', ('html', r'data-nlps-phase'), '', 'R U D A', 3, '')
add('D03', 'stage', 'Example apartment deep link (?unit=)', 'The address keeps the chosen apartment, so a link reopens it', 'bridge.js keepUnit(), stage.selectUnit()', 'stage pages', BRIDGE + ' + bridge.js "keepUnit"', ('htmljs', BRIDGE, B, 'keepUnit'), '', 'R U D A', 5, 'Kikar world has no URL state: a chosen tower/floor/apartment cannot be shared')
add('D04', 'stage', 'Floor slice "חתך הקומה"', 'The floor as a plan: glass line, balconies, example apartments; tap to pick', 'assets/project-stage/slice.js openSlice()', 'stage pages', BRIDGE + ' + bridge.js "openSlice"', ('htmljs', BRIDGE, B, 'openSlice'), '', 'R U D A', 3, 'Kikar has the key plan instead (F04)')
add('D05', 'stage', 'Several towers: pick a tower, then a floor', 'Tower chips; the card names the tower', 'TOWERS / TOWER_BY in duo, dimri, ashira stage.js', 'stage constants', 'project-stage/(duo|dimri|ashira)/stage.js', ('html', r'project-stage/(duo|dimri|ashira)/stage\.js'), '', 'U D A', 3, 'Kikar world has it (F03)')
add('D06', 'stage', 'View from the floor on a real satellite map (Mapbox)', 'Satellite + 3D buildings from the floor eye height, turned to the direction; drag to look', 'bridge.js showView(), winCam() (Mapbox GL)', 'stage pages; nadlan_mapbox_token', 'id="nlps-view"', ('html', r'id="nlps-view"'), '', 'R U D A', 4, 'Kikar renders its own window view from city data (F05), not real imagery')
add('D07', 'stage', '"What is that way" list with walking minutes', 'Named places and projects in the chosen direction, nearest first', 'bridge.js addViewPins(), showNear(); arealife.js', 'quarter.json + places.json', 'id="nlps-near"', ('html', r'id="nlps-near"'), '', 'R U D A', 3, 'Kikar places mode lists by category, not by the chosen window direction')
add('D08', 'stage', 'The beam (cone) on the area map', 'A wedge turns with the chosen direction', 'bridge.js showBeam()', 'stage pages', BRIDGE + ' + bridge.js "showBeam"', ('htmljs', BRIDGE, B, 'showBeam'), '', 'R U D A', 2, '')
add('D09', 'stage', 'Facility pins and cards with a WhatsApp question', 'Pins on the model; card with sourced lines and "ask about this facility"', '<dir>/facilities.json; stage.js anchorOf()', 'facilities.json', 'project-stage/<dir>/stage.js', ('html', r'project-stage/[a-z]+/stage\.js'), '', 'R U D A', 3, 'Kikar facilities are underground; reached from the album (E05)')
add('D10', 'stage', 'Floor card link to the apartment designer', '"לעצב את הדירה" opens /tour/designer/', 'bridge.js DESIGNER = /tour/designer/', 'stage pages', BRIDGE + ' + bridge.js "/tour/designer/"', ('htmljs', BRIDGE, B, '/tour/designer/'), '', 'R U D A', 3, 'Live link is the bare URL: the chosen unit is lost (branch fixes it, L10)')
add('D11', 'stage', 'Light presets sunset / noon', 'Two lighting buttons', 'stage.js PRESETS', 'stage pages', 'project-stage/<dir>/stage.js', ('html', r'project-stage/[a-z]+/stage\.js'), '', 'R U D A', 1, 'Kikar has the full sun clock (F06)')

# ---------------- E. Inside the building
add('E01', 'inside', 'Example apartment 360 card: floors x directions x living/balcony', 'Full-screen 360 of the living room and balcony per floor and direction', 'assets/project-stage/tour.js openTour(); .nlat in nadlan_ps_parts(); tour/living-<f><d>.jpg', 'tour/living-25w-card.jpg exists', 'id="nlps-tour"', ('html', r'id="nlps-tour"'), '', 'R (24 scenes) U (4) A (floors 10/25/34)', 5, 'Kikar: one apartment (tower C floor 30 west) in the album (E10)')
add('E02', 'inside', 'Design styles in the 360 (warm, light, stone)', 'Switch the room style inside the 360', 'tour.js styles panel; scripts/interior/render_styles.py', 'files living-<f><d>-<style>.jpg', 'living-NN<d>-warm in the scenes JSON', ('html', r'living-[0-9]+[nesw]-warm'), 'Kikar: example.js styleNames + 3 style panos (living360-c30w-sunset-warm.jpg answers 200)', 'R A Kikar', 4, 'Kikar has them inside the album, so the stage-page marker does not apply; see E11')
add('E03', 'inside', 'Room as delivered (empty) vs furnished', 'The base picture is the empty room as delivered; a switch furnishes it', 'tour.js bare style; project-stage.php "כמו במסירה" thumb; Ashira data-nlps-tour-style', 'files *-bare-thumb.jpg', 'bare-thumb', ('html', r'bare-thumb'), '', 'R A', 5, 'Kikar base picture is furnished ("העיצוב המקורי"); no empty apartment')
add('E04', 'inside', 'Facility 360 rooms from the facility card', 'Enter the pool, lobby, club... in 360', 'facilities.json tour -> tour.js (nl:facility-tour)', 'facilities.json tour.src', 'live facilities.json "tour"', ('set', FAC360), 'Kikar: lobby, pool, gym, spa, parking 360 (examples.json facilities, 4096x2048)', 'R U A Kikar', 4, 'Dimri has none')
add('E05', 'inside', 'Building walk: apartment door -> lift "לאן?" -> lobby and facilities', 'Walk between 360 scenes through doors and the lift', 'facilities.json walk + bridge.js openWalk(); Kikar: example.js walk', 'facilities.json walk', 'live facilities.json "walk"', ('set', FACWALK), 'Kikar: example.js walk (6 stops incl. car park)', 'R U Kikar', 4, 'Ashira live facilities.json has no walk; its walk.json answers 404 (L02)')
add('E06', 'inside', 'Real place names in the 360 windows', 'The places a window really sees are named in the panorama', 'arealife.js looksFor() (places.json sight bands)', 'places.json bands + 360', 'arealife.js + bands', ('set', SIGHT), '', 'R U', 3, 'Not on Kikar album')
add('E07', 'inside', 'Free walk in the compound (Ashira)', 'Walk between the buildings, into the lobby, facilities and apartment, with walking minutes', 'assets/walk/ashira/index.html (button data-nlps-ev="walk")', 'link printed on the Ashira page', 'walk/ashira/index.html', ('html', r'walk/ashira/index\.html'), '', 'Ashira', 4, 'Kikar walk stays outside on the square (F07)')
add('E08', 'inside', 'How-to film + video-call demo film in the rail (English, captions)', 'Two tabs: how to use the showroom, what a video call looks like', 'live inc/project-stage.php .nlps-howto (1.72.466-470); ashira/film-*-en.mp4', 'Ashira only', 'class="nlps-howto', ('html', r'class="nlps-howto'), '', 'Ashira', 3, '')
add('E09', 'inside', 'Hebrew how-to film (howto-he.mp4)', 'A Hebrew film on using the showroom', 'assets/project-stage/ashira/howto-he.mp4', 'none', 'howto-he', ('html', r'howto-he'), 'File answers 200 (4.28 MB); no checked page references it', 'Ashira', 3, 'Replaced by the English tabs in 1.72.470')
add('E10', 'inside', 'Kikar example apartment album', 'Living room by day, sunset, evening; corner bedroom; balcony; picture captions with date and hour', 'assets/project-stage/world/example.js; hamedina/tour/examples.json', 'world config examples', WORLD + ' + example.js "go360"', ('htmljs', WORLD, X, 'go360'), '', 'Kikar', 5, 'One apartment only: C30 west')
add('E11', 'inside', 'Kikar living-room 360 in 4 styles', 'Original, warm wood, light, stone', 'examples.json pano.styles; tour.js', 'files living360-c30w-sunset-<style>', WORLD + ' + example.js "styleNames"', ('htmljs', WORLD, X, 'styleNames'), '', 'Kikar', 4, '')
add('E12', 'inside', 'Twist strip: the same window on floors 20, 30, 38', 'Shows how the 1.25 degree turn moves the view', 'example.js twist', 'examples.json twist', WORLD + ' + example.js "twistH"', ('htmljs', WORLD, X, 'twistH'), '', 'Kikar', 3, 'Unique to Kikar')
add('E13', 'inside', 'Car park 360 with the lift vestibule', 'The underground parking as a 360 room', 'example.js fac.parking; tour/fac-parking-c.jpg', 'examples.json facilities', WORLD + ' + example.js "parking"', ('htmljs', WORLD, X, 'parking'), '', 'Kikar', 2, 'Kikar leads the fleet here')

# ---------------- F. The Kikar world
add('F01', 'world', 'One 3D world with 4 modes', 'Aerial, walk, floor and view, nearby', 'assets/project-stage/world/world.js mountWorld()', "config 'world' (dir hamedina)", WORLD, ('html', WORLD), '', 'Kikar', 5, '')
add('F02', 'world', 'Aerial cards for everything', 'Tap a tower, the ring, the park, the pond, a public building, a block or a landmark for its card with sources', 'world.js show(kind,id)', 'world.json', WORLD + ' + world.js "aboutRing"', ('htmljs', WORLD, W, 'aboutRing'), '', 'Kikar', 4, '')
add('F03', 'world', 'Tower -> floor -> apartment by direction', 'Three steps; the towers turn 1.25 degrees a floor', 'world.js steps, pickTower, setFloor, setFacing', 'world.json towers + model.twist', WORLD + ' + world.js "steps"', ('htmljs', WORLD, W, 'steps:'), '', 'Kikar', 5, '')
add('F04', 'world', 'Floor key plan: 4 corner apartments', 'North up, turns with the floor; a tap picks the apartment and lights its glass in 3D', 'world.js plan (nlw-plan*)', 'world.json model.plan', WORLD + ' + world.js "planNote"', ('htmljs', WORLD, W, 'planNote'), '', 'Kikar', 5, 'Schematic; candidate ids, not unit numbers')
add('F05', 'world', 'Window view rendered from the world', 'The view out of the chosen window at the floor eye height', "world.js setView('window')", 'world.json', WORLD + ' + world.js "viewWin"', ('htmljs', WORLD, W, 'viewWin'), '', 'Kikar', 5, 'City massing from GIS, not photo imagery')
add('F06', 'world', 'Sun clock and time of day', '4 dates x 5:00-22:00, sun hours in this window, day / sunset / night with lit windows', 'world.js setSun(), sunHours()', 'world.json', WORLD + ' + world.js "sunHours"', ('htmljs', WORLD, W, 'sunHours'), '', 'Kikar', 4, 'Stage pages only have sunset/noon (D11)')
add('F07', 'world', 'Walk on the square (first person)', 'WASD/arrows or a round pad; spots: ring, park, between the towers, the school', "world.js setMode('walk'), walkTo()", 'world.json', WORLD + ' + world.js "walkKeysDesk"', ('htmljs', WORLD, W, 'walkKeysDesk'), '', 'Kikar', 4, 'Does not enter the buildings')
add('F08', 'world', 'Nearby mode: categories, walking minutes, routes', '7 groups, minutes from the ring, a marked route', "world.js setMode('places'); hamedina/places.json", 'places.json', WORLD + ' + world.js "routeNote"', ('htmljs', WORLD, W, 'routeNote'), '', 'Kikar', 4, '')
add('F09', 'world', 'Apartment card with sizes and the basket', 'Sizes as public information, deals, "לסל הדירה" (Hebrew)', 'world.js aptSize, basket line', 'config basket_hint; Hebrew pages', WORLD + ' + world.js "aptSize"', ('htmljs', WORLD, W, 'aptSize'), '', 'Kikar', 5, '')
add('F10', 'world', 'Full screen, collapse, fading card', 'Full-screen world; the floating card fades after 8 s', 'world.js full/collapse', 'always', WORLD + ' + world.js "unfull"', ('htmljs', WORLD, W, 'unfull'), '', 'Kikar', 2, '')
add('F11', 'world', 'World in 5 languages', 'he, en, fr, ru, ar words and data names', 'world.js I18N + hamedina/world-i18n.json', 'page language', WORLD + ' on -en/-fr/-ru/-ar', ('html', WORLD), 'hamedina-fr/-ru/-ar load world.js', 'Kikar', 3, '')
add('F12', 'world', 'The pick reaches the WhatsApp message', 'window.__nlpsPick names tower, floor and facing in the source line', 'world.js window.__nlpsPick; inc/wa-source.php', 'always', WORLD + ' + world.js "__nlpsPick"', ('htmljs', WORLD, W, '__nlpsPick'), '', 'Kikar', 4, 'Stage pages: live bridge.js never sets __nlpsPick (H02 note)')
add('F13', 'world', 'World long-form sections (nlws-*)', 'Facts table; which tower/floor/direction; homes; life; prices; costs; how to buy; sale and rent; when; history timeline 1942-2026; park; square; transport; FAQ', 'project-stage.php .nlws sections (lines ~1277-1340)', 'world pages', 'id="nlws-timeline"', ('html', r'id="nlws-timeline"'), '', 'Kikar', 4, '')

# ---------------- G. Films
add('G01', 'films', 'Project film dialog (v1 motion films)', 'Wide on desktop, upright on phones', 'project-stage.php #nlfilm; config film', 'config film', 'id="nlfilm"', ('html', r'id="nlfilm"'), '', 'R U D', 3, '')
add('G02', 'films', 'Kikar narrated film (v2r1, he/en, wide + upright)', 'A narrated film of the project in a section', 'project-stage.php nlws-film (lines ~1660-1675)', 'world pages', 'id="nlws-film"', ('html', r'id="nlws-film"'), '', 'Kikar', 4, 'No VideoObject (A19)')
add('G03', 'films', 'Kikar facilities film', 'Pool, gym, spa and car park', 'project-stage.php #nlws-facilities', 'world pages', 'id="nlws-facilities"', ('html', r'id="nlws-facilities"'), '', 'Kikar', 3, '')
add('G04', 'films', 'Kikar film cuts uploaded but not shown', 'The "no-around" set and the clean facilities-only cut', 'docs/design-lab/films/kikar/v2r1/', 'none', 'kikar-hamedina-film-v2-...-noaround', ('html', r'noaround'), 'Memory nadlan-video-loop-state: "the noaround set is uploaded but not shown"', 'Kikar', 1, 'Not verified in the media library')
add('G05', 'films', 'Ashira "how a buyer decides" journey film', 'A 78.8 s replay of a buyer journey', 'docs/sales/ashira-meeting-2026-10/film/journey-en.mp4', 'none', '-', ('none',), 'Sales kit file', 'Ashira', 2, '')

# ---------------- H. Contact and selling
add('H01', 'selling', 'Floating WhatsApp bar "ייעוץ חינם"', 'A wide bar with the NadLan mark on every page', 'inc/conversion-cta.php (#nlcta)', 'site-wide', 'id="nlcta"', ('html', r'id="nlcta"'), '', 'site-wide', 4, '')
add('H02', 'selling', 'Source line in every WhatsApp message', '"מקור: <H1> · קומה N" + the path', 'inc/wa-source.php (#nadlan-wa-source)', 'site-wide', 'id="nadlan-wa-source"', ('html', r'id="nadlan-wa-source"'), '', 'site-wide', 3, 'On R U D A the floor never reaches it: live bridge.js sets no __nlpsPick')
add('H03', 'selling', 'ConsultSheet: an editable WhatsApp message with chips', 'Chips for what, when, a note; per-unit drafts', 'inc/cta-sheet.php (dialog #nlcta-sheet)', 'site-wide (was)', 'id="nlcta-sheet"', ('html', r'id="nlcta-sheet"'), 'No #nlcta-sheet on any checked page', 'all', 3, 'Built 29.9; not printed live now')
add('H04', 'selling', 'Video-call booking band', 'Pick a slot for a video call with a representative', 'inc/scheduler.php, assets/scheduler/booking.js (#nlsch)', 'nadlan_sched_on(); nadlan_sched_off meta', 'id="nlsch"', ('html', r'id="nlsch"'), '', 'all projects', 4, '')
add('H05', 'selling', 'Shared-room chooser', 'Start or join a shared viewing room', 'inc/together.php (#nadlan-together-chooser)', 'slug in nadlan_ps_config()', 'id="nadlan-together-chooser"', ('html', r'id="nadlan-together-chooser"'), '', 'stage pages + Kikar', 4, '')
add('H06', 'selling', 'TogetherRoom with LiveKit video (?room=new)', 'Rep leads, family joins from a link; same view; pinned notes; the file to WhatsApp; invite copy/share', 'inc/together.php + assets/together/together.js; Supabase token function', 'LiveKit via nadlan_tr_lk_proxy_secret (live 1.72.463)', '?room=new loads together/together.js', ('set', {'kikar_he'}), '/projects/hamedina/?room=new loads together.js (fetched 10.11)', 'all stage pages', 5, 'On Kikar the 3D world view is not shared: together.js reads window.__nlpsStage, which only bridge.js sets (code, not a live test)')
add('H07', 'selling', 'Basket: apartment + style + team + full price with purchase tax', 'Collects the apartment, style, real professionals, tax (single/additional/foreign) and lawyer fee; to WhatsApp or the room', 'inc/basket.php, assets/basket/basket.js (localStorage)', 'option nadlan_basket; Hebrew pages', 'nadlan-basket-cfg', ('html', r'nadlan-basket-cfg'), '', 'R U D A Kikar', 5, 'Not on Kikar English')
add('H08', 'selling', 'Price-alert window (phone + email)', '"prices in this area are changing" sign-up', 'inc/price-nudge.php, assets/nudge/price-alert.js (#nlnu)', 'Hebrew projects; never Ashira; off per box', 'id="nlnu"', ('html', r'id="nlnu"'), '', 'Hebrew projects', 3, '')
add('H09', 'selling', 'Apartment designer /tour/designer/', 'A 3D sample apartment: furniture, notes, a contact step', 'assets/tours/designer-tour.html via inc/tour-routes.php', 'route', '/tour/designer/ answers 200', ('none',), '/tour/designer/ 200 (title "מעצבים את הבית — דירת דוגמה ברובע שדה דב")', 'Sde Dov sample', 3, 'Linked from R U D A floor cards (D10); not from Kikar')
add('H10', 'selling', 'Request document (RFP)', 'A printable request with the unit, choices, notes, suggested professionals', 'inc/rfp.php (POST /nadlan/v1/rfp, GET /rfp/<token>)', 'designer / buy-flow', '-', ('none',), 'Code only; reached from designer and showroom engine', 'designer', 3, '')
add('H11', 'selling', 'Per-apartment brochure (print one-pager)', 'Floor, direction, size, price estimate, mortgage line', 'inc/brochure.php (REST /brochure)', 'showroom engine', '-', ('none',), 'Code only; showroom engine', 'Aurelia', 3, '')
add('H12', 'selling', 'Non-binding offer letter (LOI)', 'Submit a non-binding offer on a unit', 'inc/loi-form.php [nadlan_loi_form]', 'shortcode', 'nadlan-loi', ('html', r'nadlan-loi|nlloi'), 'Not found on checked pages', '-', 2, '')
add('H13', 'selling', 'Price offers on listings', 'Non-binding offers on a listing', 'inc/offers.php', "option nadlan_feature_offers = '0' (dark)", '-', ('none',), 'Off by default', 'listings', 1, '')
add('H14', 'selling', 'Follow a project by email (near-alerts "proj")', 'Mail when the estimated price, stage or units change', 'inc/near-alerts.php; assets/near-finder/finder.js', 'near-finder only: /properties/ and home, never project pages', '-', ('none',), 'Code: near-finder.php "never /projects/ or a project page"', 'site', 4, 'No "follow this project" on any project page')
add('H15', 'selling', 'Saved search + email alerts', 'Save a listing search, daily matches', 'inc/saved-search.php [nadlan_save_search]', 'listings', '-', ('none',), 'Listings only', 'listings', 2, '')
add('H16', 'selling', 'Milestone change email', 'An inquirer gets a mail when the project stage advances', 'inc/milestone-notify.php', 'project_status meta change', '-', ('none',), 'Back end; not verified', 'all projects', 2, '')

# ---------------- I. Other surfaces built for one project
add('I01', 'other', 'Showroom engine: 2D studio, "בנו לי הצעה", compare, favourites, unit sheet', 'Furniture planning with SI 1918 clearances; an offer flow', 'assets/showroom-engine/ (engine.js frozen, studio.js, buyflow.js)', "project_mode = 'showroom'", 'showroom-engine/engine.js', ('html', r'showroom-engine/engine\.js'), '/projects/aurelia/ loads engine.js, studio.js, buyflow.js', 'Aurelia', 4, 'Not on stage pages; engine is frozen')
add('I02', 'other', 'Legacy live co-tour (agent leads the 3D)', 'Agent camera broadcast every 1.5 s', 'inc/cotour.php', 'showroom engine', 'cotour', ('none',), '/projects/aurelia/ contains "cotour"', 'Aurelia', 2, 'Superseded by TogetherRoom')
add('I03', 'other', 'Utopia Sde Dov showroom', 'Building navigation with 29 sample-plan references', 'inc/utopia-showroom.php', 'Utopia page', 'utopia-showroom.js', ('none',), '/projects/utopia-sde-dov/ loads utopia-showroom.js', 'Utopia', 3, '')
add('I04', 'other', 'Einstein lab / flagship v3 decision room', 'Evidence states, shareable deep link, 9-slot contract page', 'inc/einstein-lab.php, assets/einstein-lab/, inc/flagship-surface.php, assets/flagship-v3/', 'post 4867; meta project_surface_version', 'einstein-lab/lab.js', ('none',), '/projects/einstein-tower/ loads einstein-lab/lab.js', 'Einstein', 3, 'flagship-v3 not seen in the page')
add('I05', 'other', 'First-person interior from unit data (CSS 3D)', 'Walk inside an apartment built from rooms and sizes', 'inc/interior-fp.php [nadlan_interior_fp]', 'shortcode', 'class="nlifp-', ('html', r'class="nlifp-'), 'Only its CSS loads on checked pages; no element', '-', 2, '')
add('I06', 'other', 'Project matcher', 'Pick what matters, get ranked matches with a percentage', 'inc/matcher.php [nl_matcher]', 'shortcode on pillar pages', '-', ('none',), 'Not checked live', 'pillars', 2, '')
add('I07', 'other', 'Modular project-page preview (DUO)', 'A standalone redesign of a project page with a GLB', 'inc/project-preview.php, assets/preview/duo.html + duo.glb', 'REST /nadlan/v1/preview/duo', '-', ('none',), 'Code only', 'DUO', 1, '')
add('I08', 'other', 'Sde Dov quarter tour (time machine 2026/2035, narration)', 'A 3D quarter tour with narration he/en', 'assets/tours/sde-dov-tour.html via inc/tour-routes.php', '/tour/sde-dov/', '-', ('none',), '/tour/sde-dov/ 200', 'Sde Dov', 3, '')
add('I09', 'other', 'Somail quarter tour', 'The same for Somail (H Infinity area)', 'assets/tours/somail-tour.html', '/tour/somail/', '-', ('none',), '/tour/somail/ 200', 'Somail', 2, '')
add('I10', 'other', 'Earth experience (Google photoreal 3D tiles)', 'Photoreal city with clickable buildings and our pins', 'inc/earth-experience.php (CesiumJS)', "option nadlan_gmaps_key (none exists)", '-', ('none',), '/earth/ answers 404 on 10.11 (was 401 on 30.9)', 'Sde Dov, Somail', 3, 'Broken/removed')
add('I11', 'other', 'Kochav HaTzafon walk (building, view, home photos)', 'A walk and a 3D building for a resale listing', 'assets/walk/kochav/ (index.html, home.html)', 'listing 7634/7812', '-', ('none',), 'walk/kochav/index.html 200, home.html 200', 'Kochav listing', 3, '')
add('I12', 'other', 'Listings compare (up to 4)', 'Side-by-side comparison tray', 'inc/compare.php (/compare/)', 'property pages', '-', ('none',), '/compare/ 200', 'listings', 2, 'No project comparison tray')

# ---------------- J. Maps
add('J01', 'maps', 'Area map (Mapbox) with layers', 'Prices, education, parks, transit, shops, health, food, future plans, 3D, satellite; 5 languages', 'inc/project-experience.php nadlan_pjx_bottom() (#nlpjx-map)', 'nadlan_mapbox_token', 'id="nlpjx-map"', ('html', r'id="nlpjx-map"'), '', 'all', 4, '')
add('J02', 'maps', 'Unified map block', 'One map that joins prices, surroundings and plans', '#nlpjx-unimap', 'project pages', 'id="nlpjx-unimap"', ('html', r'id="nlpjx-unimap"'), '', 'all', 3, '')
add('J03', 'maps', 'AreaLife place registry', '7 daily-life groups, walking minutes, 5/10/15-minute walking areas', 'assets/arealife/areamap.js, project-stage/arealife.js; <dir>/places.json', 'places.json', '<dir>/places.json', ('html', r'project-stage/[a-z]+/places\.json'), '', 'R U D A Kikar', 4, 'H Infinity falls back to OSM straight lines')
add('J04', 'maps', 'Sde Dov AreaMap v1 (quarter page)', 'The quarter map with projects, beach and neighbourhood', 'assets/arealife/areamap.js (#nlam)', 'area pages', 'id="nlam"', ('html', r'id="nlam"'), '', 'Sde Dov page', 2, '')

# ---------------- K. AI and avatars
add('K01', 'ai', 'AI real-estate advisor (HAD-680)', 'Teaches and computes from the site data; never a broker', 'inc/expert-advisor.php, assets/expert-advisor/', "?advisor=on + option nadlan_advisor_pages (now []); option nadlan_advisor", 'expert-advisor/ with ?advisor=on', ('none',), '/projects/hamedina/?advisor=on: no advisor markup (fetched 10.11)', 'Kikar 8113 + 2 guides', 2, 'Switched off on Ben word 7.11')
add('K02', 'ai', 'Talking face 0.2.0 (lip sync, voice)', 'A face pops up, greets, listens, answers', 'assets/expert-advisor/face/ (untracked), advisor.js (modified)', 'none', '-', ('none',), 'Live advisor.js differs from the repo copy', 'Kikar (planned)', 2, 'Local only')
add('K03', 'ai', 'Small talking avatar (HAD-682)', 'Small portrait, captions, mic or text, 46 pre-recorded answers', 'Documents/agent-tools/talking-agent/; deploy_live.py', 'page content on 5154', 'v-ee73901c5a53', ('none',), '/en/buy-property-in-israel/ contains v-ee73901c5a53', 'English guide', 2, 'Not on any project page')

# ---------------- L. Prototypes, labs, branches
add('L01', 'prototype', 'Plan Studio (published building-E plans)', 'Pick E-3B/E-4A/E-5E/E-5F, tap a room; 3D building and apartment; window view with distance; facility 360s; WhatsApp', 'docs/sales/ashira-meeting-2026-10/tour/studio/, make_artifact.py', 'private artifact', '-', ('none',), 'https://claude.ai/artifact/363bRm1N5CsXXc1jG4PWZx', 'Ashira', 5, 'Kikar has no published plans; the format is reusable')
add('L02', 'prototype', 'Ashira round-3 360s and walk data', 'E-plan living rooms, balconies, master bedroom on floors 5/10/15; cinema, kids, club; walk.json, views.json', 'assets/project-stage/ashira/tour/e3b-*, e4a-*, e5e-*, e5f-*, walk.json, views.json (untracked)', 'none', '-', ('none',), 'ashira/tour/walk.json and views.json answer 404 live', 'Ashira', 4, '')
add('L03', 'prototype', 'BuildingLife facility navigation', 'Photo cards under the stage open lobby/pool/gym/spa/parking 360 and keep the unit; DUO gym node; tower-aware basket', 'worktree codex-kikar-duo-experience-2026-10-09 (facility-nav.js, bridge-duo.js)', 'none', '-', ('none',), 'ACCEPTANCE.md: no production change', 'Kikar, DUO', 4, 'Blocked by a wp-admin 403 in October')
add('L04', 'prototype', 'UnitCut section cut + selected-unit contract', 'A cut that shows the unit volume; one unit kept across stage, tour, studio, request', 'worktree codex-rainbow-unit-lab-2026-09-27 labs/unit-journey/', 'none', '-', ('none',), 'Lab', 'Rainbow', 3, '')
add('L05', 'prototype', 'Designer remembers each apartment and sends furniture + notes in the request', 'Per-unit designs and notes into the RFP', 'labs/unit-journey/designer-context.mjs; repo bridge.js v102 (branch)', 'none', '-', ('none',), 'Lab + branch', 'Rainbow', 3, '')
add('L06', 'prototype', 'Higher-quality interior furniture (CC0 glTF)', 'Textured real furniture models', 'labs/interior-quality/', 'none', '-', ('none',), 'Lab', 'Rainbow', 3, 'Waits for the owner OK on CC0 downloads')
add('L07', 'prototype', 'Walkthrough 3D lab (continuous walk)', 'Park -> lobby -> clubs -> lift -> pool/spa/parking -> floors 1-40 -> apartment; sun, styles, furniture, curtains, laser measure', 'C:/Users/777/nad-lan/walkthrough-3d-lab/ (not in git)', 'none', '-', ('none',), 'Lab, 16.10', 'Kikar, Ashira', 5, 'Closest thing to the owner "walk continuously inside"')
add('L08', 'prototype', 'Kochav real-photo layer', 'Real photos room by room, drone and dusk shots, pins to the park', 'assets/walk/kochav/real/*, sr-*.jpg (untracked)', 'none', '-', ('none',), 'Local only', 'Kochav listing', 2, '')
add('L09', 'prototype', 'Rainbow style cards', 'Card pictures for light/stone/warm and floors 10/36', 'assets/project-stage/rainbow/tour/*-card.jpg (untracked)', 'none', '-', ('none',), 'Local only', 'Rainbow', 1, '')
add('L10', 'prototype', 'Branch bridge v101/v102', 'Floor card docked under the stage, +/- zoom, map landing with the unit line and "חזרה לבניין", designer opened with the unit, __nlpsPick on stage pages', 'repo assets/project-stage/bridge.js (55 KB) vs live (39 KB)', 'branch claude/apartment-experience-b1', 'nlps-mapsum / cardHost', ('html', r'nlps-mapsum'), 'Live bridge.js: 0 hits for __nlpsPick, cardHost, nlps-mapsum; repo: 3, 1, 14', 'R U D A', 3, '')
add('L11', 'prototype', 'Opening cinematic flight + sun path with soft shadows', 'A flight into the stage; soft shadows', 'design R6 part 2 (parked)', 'none', '-', ('none',), 'Baseline 30.9 row 26', 'Rainbow', 2, '')
add('L12', 'prototype', 'Aurelia community options', 'Demand board, voting pins, social login, chat rooms', 'docs/design-lab/aurelia-sports/COMMUNITY-OPTIONS.md, 01-tiles-lab.html, 02-building-map-lab.html', 'none', '-', ('none',), 'Proposal and labs', 'Aurelia', 2, '')
add('L13', 'prototype', 'EcoCity five-language flagship pages', 'Static he/en/fr/ru/ar flagship pages', 'branches codex/ecocity-local-flagship-2026-08-28, codex/ecocity-meeting-package-2026-08-28', 'none', '-', ('none',), 'Branch only', 'EcoCity', 1, '')
add('L14', 'prototype', 'Lovable showroom redesign', 'External TanStack prototype', 'branch codex/lovable-nadlan-archive-2026-08-27', 'none', '-', ('none',), 'Branch only', 'general', 1, '')

# ---------------- evaluate
res = {}
for f in F:
    fid, test = f[0], f[7]
    row = {}
    for k, _ in PAGES:
        h = HTML[k]
        if test[0] == 'html':
            v = bool(re.search(test[1], h))
        elif test[0] == 'htmljs':
            v = bool(re.search(test[1], h)) and js_has(test[2], test[3])
        elif test[0] == 'set':
            v = k in test[1]
        else:
            v = None
        row[k] = 'n/a' if v is None else ('yes' if v else 'no')
    if fid in ('E02', 'E04', 'E05'):
        js_key = {'E02': 'styleNames', 'E04': 'fac:', 'E05': 'walk:'}[fid]
        for k in ('kikar_he', 'kikar_en'):
            if re.search(WORLD, HTML[k]) and js_has(X, js_key):
                row[k] = 'yes (world album)'
    if fid == 'H06':
        for k, _ in PAGES:
            row[k] = 'yes' if k == 'kikar_he' else 'not checked'
    res[fid] = row

def status(f, row):
    fid = f[0]
    if fid[0] == 'L':
        return 'prototype only'
    over = {'K01': 'built, off', 'K02': 'prototype only', 'K03': 'elsewhere only (not a project page)', 'I10': 'removed or broken',
            'H03': 'built, not live on any checked page', 'B12': 'built, not live anywhere (branch)', 'E09': 'built, not live on checked pages', 'G04': 'built, not live anywhere',
            'G05': 'prototype only', 'A26': 'built, not live on checked pages', 'I05': 'built, not live on checked pages', 'I07': 'built, not live anywhere',
            'H13': 'built, off', 'H12': 'built, not live on checked pages', 'H16': 'built (back end, not verified)', 'I06': 'built (live pages not checked)'}
    if fid in over:
        return over[fid]
    kk = row['kikar_he'].startswith('yes') or row['kikar_en'].startswith('yes')
    other = any(row[k] == 'yes' for k in ('rainbow', 'duo', 'dimri', 'ashira', 'h_infinity', 'sde_dov'))
    if fid in ('E02', 'E04', 'E05'):
        return 'on Kikar (album) + elsewhere'
    if fid in ('H06',):
        return 'on Kikar (world view not shared)'
    if kk and other:
        return 'on Kikar + elsewhere'
    if kk:
        return 'on Kikar only'
    if other or f[8]:
        return 'elsewhere only'
    return 'built, not live on checked pages'

os.makedirs(OUT, exist_ok=True)
cols = ['id', 'group', 'feature', 'visitor_sees_and_does', 'code', 'switch', 'marker'] + [k for k, _ in PAGES] + ['other_live_evidence', 'status', 'built_for', 'buyer_value_1_5', 'notes']
with open(os.path.join(OUT, 'features.csv'), 'w', encoding='utf-8-sig', newline='') as fh:
    w = csv.writer(fh)
    w.writerow(cols)
    for f in F:
        row = res[f[0]]
        st = status(f, row)
        w.writerow([f[0], f[1], f[2], f[3], f[4], f[5], f[6]] + [row[k] for k, _ in PAGES] + [f[8] or '', st, f[9], f[10], f[11]])
json.dump({f[0]: {'feature': f[2], 'status': status(f, res[f[0]]), 'value': f[10], **res[f[0]]} for f in F},
          open(os.path.join(LIVE, 'inventory_result.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print(len(F), 'rows')
from collections import Counter
print(Counter(status(f, res[f[0]]) for f in F))
