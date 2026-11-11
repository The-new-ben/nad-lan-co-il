# Builds ../features.csv and evidence/scores.csv from the observation table below.
# Run: python -I build_features.py   (no dependencies)
# Each cell: (display text, score 0-100 | None for unknown | "NA" for not applicable, evidence class)
# Evidence classes: LT live-tested, SL seen-live, VC vendor claim, PR press, RV review, UNK unknown.
import csv, os

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, '..', 'features.csv')
SCORES = os.path.join(HERE, 'scores.csv')

PRODUCTS = ['planner5d', 'homestyler', 'coohom', 'roomsketcher', 'floorplanner', 'higharc_showroom', 'gbuilder_ref']
EVW = {'LT': 1.0, 'SL': 0.8, 'VC': 0.6, 'PR': 0.5, 'RV': 0.5}

U = {
 'p5d_price': 'https://planner5d.com/pricing',
 'p5d_ai': 'https://planner5d.com/use/ai-floor-plan-generator',
 'p5d_collab': 'https://support.planner5d.com/en/articles/14602018-how-to-use-live-collaboration-tool',
 'p5d_share': 'https://support.planner5d.com/en/articles/15116256-how-to-share-projects',
 'p5d_editor': 'https://planner5d.com/editor',
 'p5d_gallery': 'https://planner5d.com/gallery/floorplans/ZOTaeZ/floorplans-apartment-3d',
 'p5d_b2b': 'https://tool.planner5d.com/b2b-floor-plan-recognition',
 'hs_price': 'https://www.homestyler.com/pricing',
 'hs_import': 'https://www.homestyler.com/forum/view/2077998093719244802',
 'hs_editor': 'https://www.homestyler.com/floorplan',
 'hs_vr': 'https://www.homestyler.com/solution/visualization_VR-AR-Technology',
 'ch_price': 'https://www.coohom.com/pricing',
 'ch_fp': 'https://www.coohom.com/floor-planner',
 'ch_pano': 'https://www.coohom.com/pub/tool/panorama/show?obsPlanId=3FO43N7KQ0C1',
 'ch_walk': 'https://www.coohom.com/pub/tool/panorama/aiwalking?obsPlanId=3FO43N7KQ0C1&locale=en_US',
 'ch_vr': 'https://www.coohom.com/helpcenter/how-to-see-vr-effect-in-panorama',
 'ch_share': 'https://helpcenter.coohom.com/en/articles/8314349-panorama-editor-available-to-all-users',
 'ch_light': 'https://blog.coohom.com/?p=4974',
 'rs_price': 'https://www.roomsketcher.com/pricing/',
 'rs_live': 'https://www.roomsketcher.com/features/live-3d-floor-plans/',
 'rs_order': 'https://www.roomsketcher.com/order-floor-plans/',
 'fp_demo': 'https://floorplanner.com/demo',
 'fp_price': 'https://floorplanner.com/pricing',
 'ha_show': 'https://higharc.com/product/showroom',
 'ha_config': 'https://www.higharc.com/product/config',
 'ha_demo': 'https://demo.higharc.com/floorplans/belmont/',
 'ha_intro': 'https://app.higharc.com/showroom/intro?builderId=G3de6WX90K7nylNm&planId=X1BPz26zwx2yA7Qp&planType=master_plans&embedSource=script',
 'ha_help': 'https://intercom.help/higharc-ee9866fba7c9/en/articles/17313624-showroom-intro',
 'gb_sales': 'https://www.gbuilder.com/solutions/sales',
 'gb_sel': 'https://gbuilder.com/resources/market-and-sell-off-plan-homes-with-an-interactive-home-selector-and-high-definition-3d-models',
 'gb_cfg': 'https://www.gbuilder.com/resources/why-does-configuration-matter',
 'landing': 'evidence/landing-desktop-results.json + evidence/mobile-results.json (14 landing URLs)',
}

def C(d, s, e):
    return (d, s, e)
NA = lambda why: (f'n/a - {why}', 'NA', 'NA')
UNK = lambda why: (f'unknown - {why}', None, 'UNK')
WALL = 'editor behind sign-in wall'

ROWS = []
def row(pid, group, param, measure, unit, weight, cells, urls):
    assert len(cells) == 7, pid
    ROWS.append(dict(id=pid, group=group, parameter=param, measure=measure, unit=unit, weight=weight, cells=cells, urls=urls))

# ---------------- V: visualisation ----------------
G = 'visualisation'
row('V01', G, 'Real-time 3D interior in the browser, no install',
    'Open a shared or sample design in desktop Chrome on the reference GPU laptop; orbit and walk for 10 s; log frames via requestAnimationFrame. 100 = interactive and >=30 fps median; 75 = interactive, fps not yet measured or 24-30; 50 = pre-rendered node-hop only or <24 fps; 0 = none.',
    'level 0-100 (+ fps)', 5,
    [C('yes, web editor 3D [VC]; not reached: sign-up wall + ToS modal [LT]', 75, 'VC'),
     C('yes, WebGL editor [VC]; landing already uses WebGL [LT]', 75, 'VC'),
     C('public share = pre-rendered 360 node-hop [LT]; editor real-time [VC]', 50, 'LT'),
     C('Live 3D walkthrough in browser [VC]', 75, 'VC'),
     C('yes, WebGL2 orbit + first person, anonymous demo [LT]; fps not measurable on software GL', 75, 'LT'),
     C('WebGL2 viewport; 3D did not finish in 36 s on software GL [LT]; real-time 3D claimed [VC]', 75, 'VC'),
     C('HD interactive 3D model per unit [VC]', 75, 'VC')],
    [U['p5d_editor'], U['hs_editor'], U['ch_pano'], U['rs_live'], U['fp_demo'], U['ha_intro'], U['gb_sel']])
row('V02', G, 'First-person walk at eye height',
    'In 3D enter walk mode; can the camera move continuously through a doorway at a configurable eye height, with wall collision? Levels: 0 none; 25 node-hop 360; 50 free fly; 75 walk with eye height; 100 walk + collision.',
    'level 0-100', 5,
    [UNK(WALL), UNK(WALL),
     C('node-hop between ~16 panorama points [LT]', 25, 'LT'),
     C('walk room to room, turn, step closer [VC]', 75, 'VC'),
     C('First Person camera, height 143 cm default, FOV 75 deg [LT]; collision not tested', 75, 'LT'),
     C('Exterior/Interior tabs present [LT]; walk not reached', None, 'UNK'),
     C('walk inside unit and see actual views [VC]', 75, 'VC')],
    [U['p5d_editor'], U['hs_editor'], U['ch_walk'], U['rs_live'], U['fp_demo'], U['ha_intro'], U['gb_sel']])
row('V03', G, 'Maximum photoreal still or panorama resolution',
    'Highest still or 360 render width offered in any tier. Score: <1920 px 10; 1920 25; 3840 50; 7680 75; >=12K 100.',
    'px width', 3,
    [C('4K (Professional) [VC]', 50, 'VC'), C('12K panorama, 8K stills [VC]', 100, 'VC'), C('8K stills, up to 32K panorama [VC]', 100, 'VC'),
     UNK('3D Photos and 360 sold on credits; resolution not published'), C('8K 7680x4320 (credits) [VC]', 75, 'VC'),
     UNK('Photoreal exteriors [VC]; resolution not published'), UNK('not published')],
    [U['p5d_price'], U['hs_price'], U['ch_price'], U['rs_price'], U['fp_price'], U['ha_show'], U['gb_sales']])
row('V04', G, '360 panorama with shareable interactive viewer',
    'Create a 360 from a design and open its share link. 0 none; 50 panorama image export only; 100 interactive 360 viewer link.',
    'level 0-100', 3,
    [C('360 panorama and 360 walkthrough (Professional) [VC]', 100, 'VC'), C('virtual tour links from panoramas [VC]', 100, 'VC'),
     C('anonymous 360 tour link works on desktop and phone [LT]', 100, 'LT'), C('360 View on credits; share incl. Live 3D [VC]', 100, 'VC'),
     C('"3D tours" add-on via credits [VC]', 50, 'VC'), C('360-degree views of the home [VC]', 50, 'VC'), UNK('not described')],
    [U['p5d_price'], U['hs_price'], U['ch_pano'], U['rs_price'], U['fp_price'], U['ha_show'], U['gb_sel']])
row('V05', G, 'Sun position or time-of-day control',
    'In interactive 3D, look for a sun or time control. 0 none; 50 manual sun or lighting control; 100 geolocated sun path for the real site, date and floor.',
    'level 0-100', 3,
    [UNK(WALL), C('custom lighting, LightMix [VC]', 50, 'VC'), C('real-time lighting engine [VC]', 50, 'VC'), UNK('not described'),
     C('manual sun-position dial in 3D [LT]', 50, 'LT'), UNK('not reached'), UNK('views described, light not')],
    [U['p5d_price'], U['hs_price'], U['ch_light'], U['rs_live'], U['fp_demo'], U['ha_intro'], U['gb_sel']])
row('V06', G, 'Visual realism of the default buyer-facing view',
    'Blind panel of 5 raters scores 3 standard scenes 1-5 (1 = flat CAD, 5 = indistinguishable from photo); score = (median-1)*25. Values here are a single-rater preliminary by the researcher.',
    'rating 1-5', 4,
    [UNK(WALL), UNK(WALL), C('5/5 path-traced 360 (glass reflections, soft shadows) [LT, single rater]', 100, 'LT'), UNK('no public sample'),
     C('2/5 flat raster shading, no visible shadows [LT, single rater]', 25, 'LT'), UNK('3D did not render in rig; elevation thumbnails photoreal'), UNK('no public sample')],
    [U['p5d_editor'], U['hs_editor'], U['ch_pano'], U['rs_live'], U['fp_demo'], U['ha_intro'], U['gb_sales']])
row('V07', G, 'VR headset viewing',
    '0 none; 50 phone split-screen (cardboard) mode; 100 WebXR 6-DoF on a standalone headset.',
    'level 0-100', 1,
    [C('VR walkthrough mentioned by third-party listings [RV]', 50, 'RV'), C('VR & AR technology page [VC]', 50, 'VC'), C('VR button in mobile tour; phone headset [LT]', 50, 'LT'),
     UNK('not described'), UNK('not described'), UNK('not described'), UNK('not described')],
    ['review aggregators via search', U['hs_vr'], U['ch_vr'], U['rs_price'], U['fp_price'], U['ha_show'], U['gb_sales']])
row('V08', G, 'AR placement on phone',
    'Place a catalogue item in the real room through the phone camera. 0/100.',
    'yes/no', 1,
    [C('AR listed by third parties [RV]', 100, 'RV'), C('AR on VR & AR page [VC]', 100, 'VC'), UNK('not described'), UNK('not described'), UNK('not described'),
     NA('house not built yet'), NA('apartment not built yet')],
    ['review aggregators via search', U['hs_vr'], U['ch_price'], U['rs_price'], U['fp_price'], U['ha_show'], U['gb_sales']])
row('V09', G, 'Video fly-through export',
    'Export an animated walkthrough video. 0 none; 50 <=720p; 100 >=1080p.',
    'level 0-100', 2,
    [UNK('not listed on pricing'), C('1080p video, quota per plan [VC]', 100, 'VC'), C('1080p video exports [VC]', 100, 'VC'), UNK('not listed'), UNK('not listed'), UNK('not listed'), UNK('not listed')],
    [U['p5d_price'], U['hs_price'], U['ch_price'], U['rs_price'], U['fp_price'], U['ha_show'], U['gb_sales']])

# ---------------- P: plan input & accuracy ----------------
G = 'plan accuracy'
row('P01', G, 'Import plan file as underlay',
    'Formats accepted for an existing plan. 0 none; 33 image only; 67 image + PDF; 100 image + PDF + DWG/DXF.',
    'level 0-100', 3,
    [C('JPEG/PNG (+PDF inconsistent); API adds DWG/DXF/TIFF [VC]', 67, 'VC'), C('JPG/PNG 5 MB, PDF 10 MB/20 pp, DWG <=2023 10 MB, LiDAR [VC]', 100, 'VC'),
     C('JPG, PNG, PDF, DWG, DXF, WEBP [VC]', 100, 'VC'), C('JPG/PNG/PDF blueprint trace (Pro) [VC]', 67, 'VC'),
     C('"Upload 2D floorplan" button in demo [LT]; formats not shown', 33, 'LT'), NA('plans authored by builder in Higharc'), NA('developer supplies unit models')],
    [U['p5d_ai'], U['hs_import'], U['ch_fp'], U['rs_price'], U['fp_demo'], U['ha_config'], U['gb_sel']])
row('P02', G, 'Automatic wall, door and window recognition',
    'Upload 3 reference Israeli plans (developer sales PDF, scanned paper plan, CAD-exported PDF); time to an editable model. 0 none; 50 human service only; 75 automatic in minutes; 100 automatic <=60 s.',
    'level 0-100 (+ s)', 3,
    [C('AI recognition 1-2 min, email when ready [VC]', 75, 'VC'), C('Auto Generate (Beta) [VC]', 75, 'VC'), C('AI detects walls/doors/windows "in seconds" [VC]', 100, 'VC'),
     C('AI Convert ($20/floor) + human redraw next business day [VC]', 75, 'VC'), UNK('not documented'), NA('builder-authored'), NA('developer-supplied')],
    [U['p5d_ai'], U['hs_import'], U['ch_fp'], U['rs_order'], U['fp_demo'], U['ha_config'], U['gb_sel']])
row('P03', G, 'Recognition accuracy (wall-length and room-area error)',
    'On the 3 reference plans with known dimensions: median absolute % error of wall lengths and room areas after automatic recognition, no manual fixes. <=1% 100; 2% 75; 5% 50; 10% 25; >10% 0.',
    '% error', 4,
    [UNK('no figure published; page says measurements are approximate; test needs account + upload'), UNK('no figure published; Beta'), UNK('no figure published'),
     UNK('no figure published'), UNK('no recognition documented'), NA('builder-authored'), NA('developer-supplied')],
    [U['p5d_ai'], U['hs_import'], U['ch_fp'], U['rs_price'], U['fp_demo'], U['ha_config'], U['gb_sel']])
row('P04', G, 'Dimension display and numeric editing',
    '0 none; 50 dimensions displayed; 75 numeric wall-length entry in cm; 100 numeric entry in mm + dimension chains + snapping.',
    'level 0-100', 3,
    [UNK(WALL), UNK(WALL), C('custom units, wall thickness, door sizes [VC]', 75, 'VC'), C('measurements and total area (Pro) [VC]', 75, 'VC'),
     C('dimension chains in m to 2 decimals, m/ft toggle [LT]; numeric entry not exercised', 50, 'LT'), C('buyer cannot edit dimensions [LT]', 'NA', 'NA'), NA('options only')],
    [U['p5d_editor'], U['hs_editor'], U['ch_fp'], U['rs_price'], U['fp_demo'], U['ha_intro'], U['gb_sel']])
row('P05', G, 'Room and total area calculation',
    '0 none; 50 per room; 75 per room + total; 100 per room + total + net/gross distinction (Israeli sales practice).',
    'level 0-100', 4,
    [UNK(WALL), UNK(WALL), UNK('unit shown in tour, area not seen'), C('measurements and total area [VC]', 75, 'VC'),
     C('room area shown, e.g. Living 40.2 m2 [LT]', 50, 'LT'), C('total 2,889 sqft in configurator vs 2,830 ft2 on plan page [LT]', 50, 'LT'), C('unit info and layout per apartment [VC]', 50, 'VC')],
    [U['p5d_editor'], U['hs_editor'], U['ch_walk'], U['rs_price'], U['fp_demo'], U['ha_intro'], U['gb_sel']])
row('P06', G, 'Structural constraints enforced (load-bearing walls, shafts, safe room)',
    'In a developer plan try to move a load-bearing wall, a shaft and the safe-room (mamad) wall. 0 nothing locked; 50 everything locked (options-only); 100 free non-structural editing AND structural edits blocked with a reason.',
    'level 0-100', 5,
    [C('free editing; no structural rules documented [VC]', 0, 'VC'), C('no structural rules documented [VC]', 0, 'VC'), C('no structural rules documented [VC]', 0, 'VC'),
     C('no structural rules documented [VC]', 0, 'VC'), C('walls freely draggable ("Drag a wall to enlarge the room") [LT]', 0, 'LT'),
     C('options-only; rules engine for codes [VC]', 50, 'VC'), C('options-only [VC]', 50, 'VC')],
    [U['p5d_price'], U['hs_price'], U['ch_price'], U['rs_price'], U['fp_demo'], U['ha_config'], U['gb_sel']])
row('P07', G, 'Phone room scan (LiDAR or photos)',
    '0/100: capture an existing room with the phone into the plan. Low weight: a new-build unit does not exist yet.',
    'yes/no', 1,
    [UNK('not confirmed'), C('RoomScan, iOS 16 + LiDAR [VC]', 100, 'VC'), UNK('not described'), UNK('not described'), UNK('not described'), NA('not built'), NA('not built')],
    [U['p5d_price'], U['hs_import'], U['ch_fp'], U['rs_price'], U['fp_price'], U['ha_show'], U['gb_sales']])

# ---------------- L: 2D<->3D link ----------------
G = '2D-3D link'
row('L01', G, 'Single model: a 2D edit appears in 3D without export',
    'Move a wall in 2D, switch to 3D, check the change; pass/fail. 75 when same model observed but edit not exercised.',
    'pass/fail', 5,
    [C('one project, 2D and 3D modes [VC]', 100, 'VC'), C('one project [VC]', 100, 'VC'), C('draw in 2D, preview in 3D [VC]', 100, 'VC'), C('same plan in 2D and Live 3D [VC]', 100, 'VC'),
     C('same project shown in 2D and 3D toggle [LT]; wall move not exercised', 75, 'LT'), C('one parametric model for 3D, renders and documents [VC]', 100, 'VC'), UNK('not described')],
    [U['p5d_price'], U['hs_price'], U['ch_fp'], U['rs_live'], U['fp_demo'], U['ha_config'], U['gb_sel']])
row('L02', G, 'Synced split view (plan + 3D with camera marker)',
    '0 full-screen toggle only; 50 minimap or inset; 100 resizable split with live camera marker on the plan.',
    'level 0-100', 4,
    [UNK(WALL), UNK(WALL), C('minimap with viewpoint pins and live view cone [LT]', 50, 'LT'), C('2D plan with camera marker beside synced 3D window [SL]', 100, 'SL'),
     C('full-screen 2D/3D toggle only [LT]', 0, 'LT'), C('mini-map tile beside 3D viewport [LT]', 50, 'LT'), UNK('not described')],
    [U['p5d_editor'], U['hs_editor'], U['ch_walk'], U['rs_live'], U['fp_demo'], U['ha_intro'], U['gb_sel']])
row('L03', G, '2D to 3D switch latency and added download',
    'Click 3D; time until a complete frame (median of 5 runs, GPU laptop) and MB downloaded by the switch. <=0.5 s and <=2 MB 100; <=1 s 75; <=3 s 50; <=6 s 25; >6 s 0.',
    's / MB', 3,
    [UNK(WALL), UNK(WALL), UNK('editor not reachable'), UNK('no public sample'),
     C('<=3.2 s to full frame on software GL, +12.2 MB on first switch [LT]', 25, 'LT'), UNK('3D not rendered in rig'), UNK('no public demo')],
    [U['p5d_editor'], U['hs_editor'], U['ch_fp'], U['rs_live'], U['fp_demo'], U['ha_intro'], U['gb_sales']])
row('L04', G, 'Plan as navigator (click plan to place the 3D camera)',
    '0 none; 25 saved camera list; 75 click predefined pins; 100 click or drag anywhere on the plan.',
    'level 0-100', 4,
    [UNK(WALL), UNK(WALL), C('click viewpoint pins on minimap; Room Select [LT]', 75, 'LT'), C('camera marker on plan drives 3D [SL]', 100, 'SL'),
     C('saved cameras with prev/next and "Play viewpoints" [LT]', 25, 'LT'), UNK('not reached'), UNK('not described')],
    [U['p5d_editor'], U['hs_editor'], U['ch_walk'], U['rs_live'], U['fp_demo'], U['ha_intro'], U['gb_sel']])
row('L05', G, 'Edit inside the 3D view',
    'Change a finish and move an object while in 3D. 0 none; 75 finish/option change only; 100 finishes + objects.',
    'level 0-100', 4,
    [C('edit in 3D [VC]', 100, 'VC'), C('edit in 3D [VC]', 100, 'VC'), C('edit in 3D [VC]', 100, 'VC'), UNK('not described'),
     UNK('not exercised'), C('option rail beside live 3D viewport [LT]', 75, 'LT'), C('try material options in 3D [VC]', 75, 'VC')],
    [U['p5d_price'], U['hs_price'], U['ch_fp'], U['rs_live'], U['fp_demo'], U['ha_intro'], U['gb_sel']])

# ---------------- C: catalogue & pricing ----------------
G = 'catalogue and pricing'
row('C01', G, 'Catalogue size',
    'Distinct 3D items and materials available to a paying user. log scale: 1k 25; 10k 50; 100k 75; >=1M 100.',
    'items', 2,
    [C('10,000+ premium items [VC]', 50, 'VC'), C('100,000+ (pricing) vs "1M+" (page title) [VC/LT]', 75, 'VC'), C('100K+ premium, +500 a week [VC]', 75, 'VC'),
     UNK('"full catalog", size not published'), UNK('size not published'), C('builder options, "hundreds of options" per plan [VC]', 25, 'VC'), UNK('developer options, size not published')],
    [U['p5d_price'], U['hs_price'], U['ch_price'], U['rs_price'], U['fp_price'], 'https://www.higharc.com/ready-to-build', U['gb_sel']])
row('C02', G, 'Items tied to real purchasable SKUs',
    'Sample 50 items in a living room + kitchen; share carrying a brand and model code. 0 generic; 50 some branded; 100 all real SKUs.',
    'share %', 4,
    [C('generic; enterprise can load own catalogue [VC]', 25, 'VC'), C('branded models available [VC]', 50, 'VC'), C('Brand tab in product list; some real brands [LT]', 50, 'LT'),
     UNK('not described'), C('generic finish names, e.g. "Wood Planks Bare 0335" [LT]', 0, 'LT'), C('options are builder SKUs [VC]', 100, 'VC'), C('developer material options [VC]', 100, 'VC')],
    [U['p5d_price'], U['hs_price'], U['ch_walk'], U['rs_price'], U['fp_demo'], U['ha_show'], U['gb_sel']])
row('C03', G, 'Price visible in context on every selectable item',
    'Open the finish or option picker; is a price shown next to each item? 0 none; 50 price in separate estimator or export; 100 price in context.',
    'level 0-100', 5,
    [C('Price Estimator + Budget Widget (paid) [VC]', 50, 'VC'), UNK('BOM export; prices not stated'), C('public product list shows no prices [LT]; enterprise quotation [VC]', 0, 'LT'),
     C('no pricing features [VC]', 0, 'VC'), C('no prices anywhere in demo [LT]', 0, 'LT'), C('no price in demo option rail (0 "$" lines) [LT]; real-time pricing claimed [VC]', 0, 'LT'),
     C('extra cost per material option [VC]', 100, 'VC')],
    [U['p5d_price'], U['hs_price'], U['ch_walk'], U['rs_price'], U['fp_demo'], U['ha_intro'], U['gb_sel']])
row('C04', G, 'Israeli catalogue: ILS prices, Israeli suppliers, VAT basis',
    '0 none; 50 ILS currency only; 100 ILS + Israeli suppliers + stated VAT basis.',
    'level 0-100', 5,
    [C('subscription shown in ILS; catalogue not localised [VC]', 0, 'VC'), C('none found [VC]', 0, 'VC'), C('subscription in ILS; share list has CN/EN names [LT]', 0, 'LT'),
     C('none [VC]', 0, 'VC'), C('none [LT]', 0, 'LT'), C('US only [LT]', 0, 'LT'), C('Nordic/EU markets [SL]', 0, 'SL')],
    [U['p5d_price'], U['hs_price'], U['ch_walk'], U['rs_price'], U['fp_demo'], U['ha_intro'], U['gb_sales']])
row('C05', G, 'Price provenance shown (supplier, date, VAT incl./excl.)',
    'For 10 priced items check that supplier, price date and VAT basis are visible. % of items passing.',
    '% items', 4,
    [UNK('estimator walled; not documented'), UNK('not documented'), C('no prices shown [LT]', 0, 'LT'), C('no prices [VC]', 0, 'VC'),
     C('no prices [LT]', 0, 'LT'), C('no prices shown [LT]', 0, 'LT'), UNK('not documented')],
    [U['p5d_price'], U['hs_price'], U['ch_walk'], U['rs_price'], U['fp_demo'], U['ha_intro'], U['gb_sel']])
row('C06', G, 'Buy, quote or contract action from the design',
    '0 none; 50 lead or quote request carrying the design; 100 transactional (cart, contract addendum, e-sign).',
    'level 0-100', 3,
    [C('Enterprise: cart, CRM, ERP, quoting [VC]', 50, 'VC'), UNK('not documented'), C('Enterprise K&B order management [VC]', 50, 'VC'),
     C('none [VC]', 0, 'VC'), C('none [LT]', 0, 'LT'), C('lead captured with plan, options, price [VC]; Save/Share [LT]', 50, 'VC'), C('selection confirmed by built-in e-signature [VC]', 100, 'VC')],
    [U['p5d_price'], U['hs_price'], U['ch_price'], U['rs_price'], U['fp_demo'], U['ha_show'], U['gb_cfg']])

# ---------------- G: generation ----------------
G = 'generation'
row('G01', G, 'One-action style apply producing an editable 3D design',
    '0 none; 50 rule-based style/packages per room; 75 AI per room; 100 AI whole apartment, result stays editable 3D.',
    'level 0-100', 3,
    [C('AI Studio furnish, Smart Wizard [VC]', 75, 'VC'), C('AI Decor applies a style to a floor plan [VC]', 100, 'VC'), C('AI templates [VC]', 50, 'VC'),
     C('none [VC]', 0, 'VC'), C('Styleboards (rule-based) [LT]', 50, 'LT'), C('curated exterior palettes [LT]', 50, 'LT'), C('predefined interior packages [VC]', 50, 'VC')],
    [U['p5d_ai'], U['hs_price'], U['ch_price'], U['rs_price'], U['fp_demo'], U['ha_intro'], U['gb_cfg']])
row('G02', G, 'Text or voice instruction edits the 3D model',
    '0 none; 50 text to image only; 100 text edits the 3D model.',
    'level 0-100', 2,
    [C('Copilot adds furniture and finishes from text or voice [VC]', 100, 'VC'), C('"Spark" AI design agent (single source) [RV]', 100, 'RV'), C('"AI agent floor planner" page [SL]', 100, 'VC'),
     C('none [VC]', 0, 'VC'), C('none [LT]', 0, 'LT'), C('none [LT]', 0, 'LT'), C('none described [VC]', 0, 'VC')],
    [U['p5d_ai'], 'https://www.stork.ai/en/homestyler', 'https://www.coohom.com/ai-agent-floor-planner', U['rs_price'], U['fp_demo'], U['ha_intro'], U['gb_sales']])
row('G03', G, 'Generation respects structure lock, allowed options and budget',
    'Ask for a redesign with a budget cap; check that walls, windows and shafts did not move, only developer-allowed items were used, and total <= cap. 0/33/67/100 for 0-3 constraints.',
    'constraints met (0-3)', 4,
    [C('not documented [VC]', 0, 'VC'), C('not documented [VC]', 0, 'VC'), C('not documented [VC]', 0, 'VC'), C('no generation [VC]', 0, 'VC'),
     C('no generation [LT]', 0, 'LT'), C('no generation [LT]', 0, 'LT'), C('no generation [VC]', 0, 'VC')],
    [U['p5d_ai'], U['hs_price'], U['ch_price'], U['rs_price'], U['fp_demo'], U['ha_intro'], U['gb_sales']])
row('G04', G, 'Design variants compared side by side with cost delta',
    '0 none; 50 several designs per project; 100 compare view with cost difference.',
    'level 0-100', 3,
    [UNK('not documented'), UNK('not documented'), UNK('not documented'), UNK('not documented'),
     C('up to 3 designs per project (free) [VC]', 50, 'VC'), C('Reset to original; variants not seen [LT]', None, 'UNK'), C('several variants, one confirmed by e-sign [VC]', 50, 'VC')],
    [U['p5d_price'], U['hs_price'], U['ch_price'], U['rs_price'], U['fp_price'], U['ha_intro'], U['gb_cfg']])

# ---------------- K: collaboration & video ----------------
G = 'collaboration and video'
row('K01', G, 'Anonymous share link opens on a phone',
    'Open the share link in a fresh mobile browser profile. 0 none; 50 needs sign-in or terms acceptance; 75 opens but renders blank/slow (>8 s); 100 opens and renders.',
    'level 0-100', 4,
    [C('gallery 3D gated by ToS "I Agree" modal [LT]', 50, 'LT'), C('virtual tour link [VC]', 100, 'VC'), C('tour opened anonymously on 390 px phone, 11 s [LT]', 100, 'LT'),
     C('share link, Live 3D on credits [VC]', 100, 'VC'), C('demo link opens anonymously on phone [LT]', 100, 'LT'), C('intro opens anonymously; mobile blank at 7.6 s [LT]', 75, 'LT'), UNK('no public demo')],
    [U['p5d_gallery'], U['hs_price'], U['ch_pano'], U['rs_price'], U['fp_demo'], U['ha_intro'], U['gb_sales']])
row('K02', G, 'Real-time co-editing with presence',
    'Two browsers edit one design; median latency of a change appearing on the other (20 trials). 0 none; 50 async sharing or team library; 100 simultaneous with presence.',
    'level 0-100 (+ ms)', 4,
    [C('web Live Collaboration with view/comment/edit roles [VC]', 100, 'VC'), C('Team shared design space [VC]', 50, 'VC'), C('Elite team co-editing up to 20 seats [VC]', 100, 'VC'),
     C('Team project collaboration [VC]', 50, 'VC'), C('Teams, more users [VC]', 50, 'VC'), UNK('not described'), C('"real-time collaboration" (unspecified) [VC]', 50, 'VC')],
    [U['p5d_collab'], U['hs_price'], U['ch_price'], U['rs_price'], U['fp_price'], U['ha_show'], U['gb_sales']])
row('K03', G, 'Comments pinned to locations in the model',
    '0 none; 50 comments on project; 100 comments pinned to a 3D or plan location.',
    'level 0-100', 3,
    [C('"Can comment" role [VC]', 50, 'VC'), UNK('not documented'), UNK('not documented'), UNK('not documented'), UNK('not seen in demo'), UNK('not seen'), UNK('not documented')],
    [U['p5d_collab'], U['hs_price'], U['ch_price'], U['rs_price'], U['fp_demo'], U['ha_intro'], U['gb_sales']])
row('K04', G, 'Built-in video and audio call inside the design session',
    'Start a call from inside the designer with 3 participants (buyer, rep, designer). 0 none; 50 external call link alongside; 100 embedded A/V >=3 people.',
    'level 0-100', 5,
    [C('none [VC]', 0, 'VC'), C('none [VC]', 0, 'VC'), C('none in tour UI [LT]', 0, 'LT'), C('none [VC]', 0, 'VC'), C('none [LT]', 0, 'LT'), C('none in intro UI [LT]', 0, 'LT'), C('none described [VC]', 0, 'VC')],
    [U['p5d_collab'], U['hs_price'], U['ch_pano'], U['rs_price'], U['fp_demo'], U['ha_intro'], U['gb_sales']])
row('K05', G, 'Follow-me camera and control handover between participants',
    'Presenter mode: others follow the presenter camera; control passes buyer to rep to designer with one tap; handover latency (ms). 0 none; 50 follow-only; 100 follow + handover.',
    'level 0-100', 5,
    [C('none documented [VC]', 0, 'VC'), C('none [VC]', 0, 'VC'), C('none [LT]', 0, 'LT'), C('none [VC]', 0, 'VC'), C('none [LT]', 0, 'LT'), C('none [LT]', 0, 'LT'), C('none [VC]', 0, 'VC')],
    [U['p5d_collab'], U['hs_price'], U['ch_pano'], U['rs_price'], U['fp_demo'], U['ha_intro'], U['gb_sales']])
row('K06', G, 'Roles and formal approval of selections',
    '0 none; 50 view/comment/edit roles; 100 roles + buyer approval or e-signature of the change list.',
    'level 0-100', 4,
    [C('view/comment/edit roles [VC]', 50, 'VC'), C('sub-account management (Team) [VC]', 50, 'VC'), C('team roles (Elite) [VC]', 50, 'VC'), C('Team users [VC]', 50, 'VC'),
     C('none in demo [LT]', 0, 'LT'), C('sales handoff of selections [VC]', 50, 'VC'), C('built-in e-signature confirms one variant [VC]', 100, 'VC')],
    [U['p5d_collab'], U['hs_price'], U['ch_price'], U['rs_price'], U['fp_demo'], U['ha_show'], U['gb_cfg']])
row('K07', G, 'Decision log (who changed what, when) exportable',
    '0 undo only; 50 version history; 100 timestamped per-user change log exportable with the spec.',
    'level 0-100', 3,
    [UNK('not documented'), UNK('not documented'), UNK('not documented'), UNK('not documented'), C('undo/redo only [LT]', 0, 'LT'), UNK('not seen'), UNK('not documented')],
    [U['p5d_collab'], U['hs_price'], U['ch_price'], U['rs_price'], U['fp_demo'], U['ha_intro'], U['gb_sales']])

# ---------------- S: spec / BOM / cost ----------------
G = 'spec, BOM and cost'
row('S01', G, 'Itemised BOM export',
    '0 none; 50 list in UI; 100 exportable file (CSV/PDF/XLSX) with item, qty, room, finish code.',
    'level 0-100', 4,
    [C('Specs & Docs Organizer (Professional) [VC]', 50, 'VC'), C('BOM export (Pro+) [VC]', 100, 'VC'), C('downloadable BOM (Pro) [VC]; product list in tour [LT]', 100, 'VC'),
     C('none [VC]', 0, 'VC'), C('none in demo [LT]', 0, 'LT'), C('downloadable takeoff data [VC]', 100, 'VC'), UNK('not documented')],
    [U['p5d_price'], U['hs_price'], U['ch_price'], U['rs_price'], U['fp_demo'], U['ha_show'], U['gb_sales']])
row('S02', G, 'Live cost total that updates on each change',
    'Change 3 finishes; is a currency total on screen and updated within 1 s? 0 none; 50 total in separate step or export; 100 live on-screen total.',
    'level 0-100 (+ s)', 5,
    [C('Budget Widget + Price Estimator [VC]', 100, 'VC'), UNK('not documented'), C('Enterprise custom quotation [VC]', 50, 'VC'), C('none [VC]', 0, 'VC'),
     C('none [LT]', 0, 'LT'), C('no total visible in demo [LT]; real-time pricing claimed [VC]', 0, 'LT'), C('buyer sees cost change as they choose [VC]', 100, 'VC')],
    [U['p5d_price'], U['hs_price'], U['ch_price'], U['rs_price'], U['fp_demo'], U['ha_intro'], U['gb_sales']])
row('S03', G, 'Spec sheet (mifrat-style) document per room',
    'Export a PDF finish schedule room by room with finish code, quantity, supplier. 0 none; 50 generic report or drawings; 100 room-by-room spec sheet.',
    'level 0-100', 5,
    [C('Specs & Docs Organizer [VC]', 50, 'VC'), C('construction drawings + BOM [VC]', 50, 'VC'), C('construction drawings + BOM [VC]', 50, 'VC'), C('plan print to scale only [VC]', 0, 'VC'),
     C('image exports only [LT/VC]', 0, 'LT'), C('construction documents via Config [VC]', 50, 'VC'), C('selection confirmation [VC]', 50, 'VC')],
    [U['p5d_price'], U['hs_price'], U['ch_price'], U['rs_price'], U['fp_price'], U['ha_config'], U['gb_cfg']])
row('S04', G, 'Delta against the developer base specification (upgrades and credits)',
    '0 none; 50 upgrade prices only; 100 upgrades + credits for removed standard items + net delta.',
    'level 0-100', 5,
    [C('no base-spec concept [VC]', 0, 'VC'), C('no base-spec concept [VC]', 0, 'VC'), C('no base-spec concept [VC]', 0, 'VC'), C('no base-spec concept [VC]', 0, 'VC'),
     C('no base-spec concept [LT]', 0, 'LT'), C('standard vs "Upgrade to..." options [LT]; prices claimed [VC]', 50, 'VC'), C('extra cost per option [VC]', 50, 'VC')],
    [U['p5d_price'], U['hs_price'], U['ch_price'], U['rs_price'], U['fp_demo'], U['ha_intro'], U['gb_sel']])
row('S05', G, 'Cost basis disclosed (VAT, labour/installation, currency, validity date)',
    'For the cost total: are VAT basis, labour, currency and price-valid-until all stated? 25 per item.',
    'items 0-4', 4,
    [UNK('estimator walled'), UNK('not documented'), UNK('enterprise quotation not public'), C('no costs [VC]', 0, 'VC'), C('no costs [LT]', 0, 'LT'), C('no costs visible [LT]', 0, 'LT'), UNK('not documented')],
    [U['p5d_price'], U['hs_price'], U['ch_price'], U['rs_price'], U['fp_demo'], U['ha_intro'], U['gb_sales']])
row('S06', G, 'Contractor-grade drawings or CAD export',
    '0 none; 25 scaled image; 50 print to scale; 100 CAD (DWG/DXF) or permit-grade documents.',
    'level 0-100', 2,
    [C('CAD export (Professional) [VC]', 100, 'VC'), C('construction drawings (Pro+) [VC]', 100, 'VC'), C('Export to CAD (Elite) [VC]', 100, 'VC'), C('print to scale (Pro) [VC]', 50, 'VC'),
     C('image exports SD-8K only [VC]', 25, 'VC'), C('permit-ready construction documents [VC]', 100, 'VC'), UNK('not documented')],
    [U['p5d_price'], U['hs_price'], U['ch_price'], U['rs_price'], U['fp_price'], U['ha_show'], U['gb_sales']])

# ---------------- M: mobile UX ----------------
G = 'mobile UX'
row('M01', G, 'Full editing in the mobile browser (no app)',
    'On 390x844: change a finish and move an object in the browser. 0 view-only or nothing; 50 editing only in native app; 100 mobile-web editing.',
    'level 0-100', 5,
    [C('native apps [VC]; web editor walled', 50, 'VC'), C('native app; m. site is marketing [VC/LT]', 50, 'VC'), C('native app (download link) [SL]', 50, 'SL'), C('native app [VC]', 50, 'VC'),
     C('mobile web is view-only: 2D/3D, Settings, Undo [LT]', 0, 'LT'), C('blank white screen at 7.6 s [LT]', 0, 'LT'), C('mobile, tablet, desktop [VC]', 100, 'VC')],
    [U['p5d_price'], 'https://m.homestyler.com/', 'https://www.coohom.com/app-download', U['rs_price'], U['fp_demo'], U['ha_intro'], U['gb_cfg']])
row('M02', G, 'Primary call to action in the thumb zone',
    'Mobile landing 390x844: vertical centre of the primary CTA / viewport height. >=75% 100; 60-75% 75; 45-60% 40; 30-45% 20; <30% or none 0.',
    '% of viewport height', 3,
    [C('"Get Started" at 44% [LT]', 20, 'LT'), C('"Floor Planner for Web" at 47% [LT]', 40, 'LT'), C('"Start for free" at 47%, 350 px wide [LT]', 40, 'LT'), C('"Get Started for Free" at 49% [LT]', 40, 'LT'),
     C('"Free Account" at 4% (top bar) [LT]', 0, 'LT'), C('no CTA in first viewport [LT]', 0, 'LT'), C('no CTA in first viewport (video lightbox only) [LT]', 0, 'LT')],
    [U['landing']] * 7)
row('M03', G, 'Tap targets at least 44 px',
    'Share of interactive elements in the first mobile viewport with min side >=44 CSS px (Apple HIG; WCAG 2.5.8 floor is 24 px). Score = share %.',
    '%', 3,
    [C('7/9 = 78% (landing) [LT]', 78, 'LT'), C('4/8 = 50% (landing) [LT]', 50, 'LT'), C('2/7 = 29% (landing) [LT]', 29, 'LT'), C('2/6 = 33% (landing) [LT]', 33, 'LT'),
     C('editor 1/6 = 17%; landing 1/2 [LT]', 17, 'LT'), C('intro 0/5 = 0%; landing 1/4 [LT]', 0, 'LT'), C('5/7 = 71% (landing) [LT]', 71, 'LT')],
    [U['landing'], U['landing'], U['landing'], U['landing'], U['fp_demo'], U['ha_intro'], U['landing']])
row('M04', G, 'First-screen clarity',
    'Mobile first viewport: (a) H1 names the task, (b) exactly one primary action, (c) <=400 visible text characters. 33 points each.',
    'criteria met 0-3', 4,
    [C('H1 yes; 3 competing CTAs; 636 chars [LT]', 33, 'LT'), C('H1 yes; 2 CTAs; 289 chars [LT]', 67, 'LT'), C('empty H1; 1 CTA; 449 chars [LT]', 33, 'LT'), C('H1 yes; 1 CTA; 267 chars [LT]', 100, 'LT'),
     C('H1 vague; 1 CTA; 583 chars [LT]', 33, 'LT'), C('H1 yes; no CTA; 333 chars [LT]', 67, 'LT'), C('H1 generic; no CTA; 454 chars [LT]', 0, 'LT')],
    [U['landing']] * 7)
row('M05', G, 'One-thumb 3D navigation',
    'In the mobile 3D view: are primary controls in the bottom 40% and is tap-to-move available? 0 controls at top or none; 50 gestures/hotspots only; 100 bottom controls + tap-to-walk.',
    'level 0-100', 4,
    [UNK(WALL), UNK(WALL), C('drag + hotspots; all buttons top-right [LT]', 50, 'LT'), UNK('no public sample'),
     C('2D/3D toggle at top; no walk controls on mobile [LT]', 0, 'LT'), C('blank at 7.6 s [LT]', None, 'UNK'), UNK('no public demo')],
    [U['p5d_editor'], U['hs_editor'], U['ch_pano'], U['rs_live'], U['fp_demo'], U['ha_intro'], U['gb_sales']])
row('M06', G, 'Mobile bytes before the first interactive design view',
    'Mobile emulation, cold cache: MB transferred when the first design canvas is interactive. <=2 100; <=5 75; <=10 50; <=20 25; >20 0.',
    'MB', 3,
    [UNK(WALL), UNK(WALL), C('15.7 MB [LT]', 25, 'LT'), UNK('no public sample'), C('8.8 MB [LT]', 50, 'LT'), C('5.7 MB but blank [LT]', None, 'UNK'), UNK('no public demo')],
    [U['p5d_editor'], U['hs_editor'], U['ch_pano'], U['rs_live'], U['fp_demo'], U['ha_intro'], U['gb_sales']])

# ---------------- F: performance (desktop) ----------------
G = 'performance'
row('F01', G, 'Landing LCP (desktop, cold)',
    'Largest Contentful Paint, 1366x900, no throttling. <=1.2 s 100; <=2.5 s 75; <=4 s 25; >4 s 0.',
    'ms', 2,
    [C('1,908 ms [LT]', 75, 'LT'), C('3,980 ms [LT]', 25, 'LT'), C('1,780 ms [LT]', 75, 'LT'), C('1,816 ms [LT]', 75, 'LT'), C('2,580 ms [LT]', 25, 'LT'), C('1,836 ms [LT]', 75, 'LT'), C('664 ms [LT]', 100, 'LT')],
    [U['landing']] * 7)
row('F02', G, 'Landing transfer size (desktop)',
    'Sum of encoded bytes, cold cache. <=1 MB 100; <=2 75; <=4 50; <=8 25; >8 0.',
    'MB', 2,
    [C('3.0 MB / 136 req [LT]', 50, 'LT'), C('20.1 MB / 217 req (9.1 MB video) [LT]', 0, 'LT'), C('3.2 MB / 107 req [LT]', 50, 'LT'), C('1.9 MB / 88 req [LT]', 75, 'LT'),
     C('2.7 MB / 56 req [LT]', 50, 'LT'), C('2.1 MB / 72 req [LT]', 50, 'LT'), C('4.7 MB / 63 req [LT]', 25, 'LT')],
    [U['landing']] * 7)
row('F03', G, 'Landing layout stability (CLS)',
    'Cumulative Layout Shift after load. <=0.1 100; <=0.25 50; >0.25 0.',
    'CLS', 1,
    [C('0.441 [LT]', 0, 'LT'), C('0.040 [LT]', 100, 'LT'), C('0.047 [LT]', 100, 'LT'), C('0.003 [LT]', 100, 'LT'), C('0.008 [LT]', 100, 'LT'), C('0.002 [LT]', 100, 'LT'), C('0.035 [LT]', 100, 'LT')],
    [U['landing']] * 7)
row('F04', G, 'Time to first interactive design canvas from a cold link',
    'Navigation start to first design canvas >300x200 px (desktop). <=2 s 100; <=4 s 75; <=8 s 50; <=15 s 25; >15 s 0. Software-GL rig; repeat on GPU.',
    's', 4,
    [UNK(WALL), UNK(WALL), C('360 tour canvas ~15.0 s (AI-walk tour 8.6 s) [LT]', 25, 'LT'), UNK('no public sample'),
     C('5.6 s to editor canvas [LT]', 50, 'LT'), C('canvas element ~13.5 s, 3D still loading at 36 s [LT]', 25, 'LT'), UNK('no public demo')],
    [U['p5d_editor'], U['hs_editor'], U['ch_pano'], U['rs_live'], U['fp_demo'], U['ha_intro'], U['gb_sales']])
row('F05', G, 'Bytes to first 3D interior frame',
    'MB transferred until the first complete interior 3D frame. <=5 100; <=10 75; <=15 50; <=25 25; >25 0.',
    'MB', 3,
    [UNK(WALL), UNK(WALL), C('15.2 MB [LT]', 25, 'LT'), UNK('no public sample'), C('21.1 MB (8.8 2D + 12.2 3D switch) [LT]', 25, 'LT'),
     C('>=11.8 MB and not rendered in rig [LT]', None, 'UNK'), UNK('no public demo')],
    [U['p5d_editor'], U['hs_editor'], U['ch_pano'], U['rs_live'], U['fp_demo'], U['ha_intro'], U['gb_sales']])
row('F06', G, 'Requests to first 3D view',
    'HTTP requests until the first 3D frame. <=50 100; <=100 75; <=200 50; <=500 25; >500 0.',
    'requests', 1,
    [UNK(WALL), UNK(WALL), C('182 [LT]', 50, 'LT'), UNK('no public sample'), C('276 [LT]', 25, 'LT'), C('1,209 and still loading [LT]', 0, 'LT'), UNK('no public demo')],
    [U['p5d_editor'], U['hs_editor'], U['ch_pano'], U['rs_live'], U['fp_demo'], U['ha_intro'], U['gb_sales']])
row('F07', G, 'Third-party hosts contacted by landing',
    'Distinct hosts in network log (privacy and latency). <=5 100; <=10 75; <=20 50; <=35 25; >35 0.',
    'hosts', 1,
    [C('25 [LT]', 25, 'LT'), C('49 [LT]', 0, 'LT'), C('22 [LT]', 25, 'LT'), C('32 [LT]', 25, 'LT'), C('10 [LT]', 75, 'LT'), C('39 [LT]', 0, 'LT'), C('14 [LT]', 50, 'LT')],
    [U['landing']] * 7)

# ---------------- A: accessibility & RTL ----------------
G = 'accessibility and RTL'
row('A01', G, 'Hebrew user interface',
    'Switch UI language to Hebrew. 0/100.',
    'yes/no', 5,
    [C('no he in 14 hreflang locales [LT]', 0, 'LT'), C('no he; 14 locales [LT]', 0, 'LT'), C('no he; 18 locales [LT]', 0, 'LT'), C('English only [LT]', 0, 'LT'),
     C('English only [LT]', 0, 'LT'), C('English only [LT]', 0, 'LT'), C('EN/DE/SV/ES/NL [SL]', 0, 'SL')],
    [U['landing']] * 7)
row('A02', G, 'Right-to-left layout support',
    '0 none; 50 an RTL language on marketing site only; 100 designer UI mirrors (panels, rails, number entry) for RTL.',
    'level 0-100', 4,
    [C('none [LT]', 0, 'LT'), C('Arabic (ar) on marketing site [LT]; editor unknown (walled)', 50, 'LT'), C('none [LT]', 0, 'LT'), C('none [LT]', 0, 'LT'),
     C('none; editor dir=ltr [LT]', 0, 'LT'), C('none [LT]', 0, 'LT'), C('none [SL]', 0, 'SL')],
    [U['landing']] * 7)
row('A03', G, 'Bidi-correct Hebrew labels on plan and in 3D',
    'Name a room with mixed Hebrew + number (e.g. Hebrew "living" + 24.5 m2) and check rendering order on plan, 3D labels and PDF. % correct of 6 checks.',
    '% checks', 4,
    [UNK('no Hebrew UI; walled'), UNK('walled'), UNK('walled'), UNK('walled'), UNK('room rename not exercised'), UNK('buyer cannot name rooms'), UNK('no demo')],
    [U['p5d_editor'], U['hs_editor'], U['ch_fp'], U['rs_live'], U['fp_demo'], U['ha_intro'], U['gb_sales']])
row('A04', G, 'Unnamed interactive controls (landing)',
    'Count of a/button/input without accessible name. 0 100; <=5 75; <=15 50; <=30 25; >30 0.',
    'count', 2,
    [C('20 [LT]', 25, 'LT'), C('11 [LT]', 50, 'LT'), C('18 [LT]', 25, 'LT'), C('0 [LT]', 100, 'LT'), C('3 [LT]', 75, 'LT'), C('6 [LT]', 50, 'LT'), C('7 [LT]', 50, 'LT')],
    [U['landing']] * 7)
row('A05', G, 'Images with alt attribute (landing)',
    'Share of <img> with an alt attribute. Score = %.',
    '%', 1,
    [C('57/57 [LT]', 100, 'LT'), C('124/166 = 75% [LT]', 75, 'LT'), C('73/73 [LT]', 100, 'LT'), C('33/33 [LT]', 100, 'LT'), C('11/11 [LT]', 100, 'LT'), C('22/22 [LT]', 100, 'LT'), C('111/111 [LT]', 100, 'LT')],
    [U['landing']] * 7)
row('A06', G, 'Pinch-zoom not blocked on mobile',
    'viewport meta has no user-scalable=no / maximum-scale=1. 0/100.',
    'yes/no', 2,
    [C('allowed [LT]', 100, 'LT'), C('BLOCKED on m.homestyler.com [LT]', 0, 'LT'), C('allowed [LT]', 100, 'LT'), C('allowed [LT]', 100, 'LT'), C('allowed [LT]', 100, 'LT'), C('allowed [LT]', 100, 'LT'), C('allowed [LT]', 100, 'LT')],
    [U['landing']] * 7)
row('A07', G, 'Accessibility statement published',
    'HTTP check of /accessibility plus site search for an accessibility statement or VPAT. 0/100. (Israel requires a Hebrew statement under IS 5568.)',
    'yes/no', 2,
    [C('/accessibility 404 [LT]', 0, 'LT'), C('404 [LT]', 0, 'LT'), C('404 [LT]', 0, 'LT'), C('404 [LT]', 0, 'LT'), C('redirects to /login [LT]', 0, 'LT'), C('404 [LT]', 0, 'LT'), C('404 [LT]', 0, 'LT')],
    ['https://planner5d.com/accessibility', 'https://www.homestyler.com/accessibility', 'https://www.coohom.com/accessibility', 'https://www.roomsketcher.com/accessibility/', 'https://floorplanner.com/accessibility', 'https://www.higharc.com/accessibility', 'https://www.gbuilder.com/accessibility'])
row('A08', G, 'Keyboard operability of the design surface',
    'Without a mouse: reach every tool by Tab, move camera with keys, change a finish. % of 10 scripted tasks completed.',
    '% tasks', 2,
    [UNK(WALL), UNK(WALL), UNK('not tested'), UNK('no public sample'), UNK('not tested'), C('labelled controls + ctrl+K option search [LT]; full test not run', 50, 'LT'), UNK('no demo')],
    [U['p5d_editor'], U['hs_editor'], U['ch_pano'], U['rs_live'], U['fp_demo'], U['ha_intro'], U['gb_sales']])

# ---------------- I: integration with project plans ----------------
G = 'integration with project plans'
row('I01', G, 'Starts from the developer real unit plan',
    'From a project page, open unit X: does the designer load that unit model with no upload or drawing? 0 buyer must draw/upload; 50 possible via enterprise/API; 100 native per-unit pipeline.',
    'level 0-100', 5,
    [C('Enterprise white-label configurator [VC]', 50, 'VC'), C('Enterprise custom API [VC]', 50, 'VC'), C('Enterprise white-label planner [VC]', 50, 'VC'), C('buyer draws or orders redraw [VC]', 0, 'VC'),
     C('embed/API exists; demo loads a sample project [SL]', 50, 'SL'), C('plan page button loads that plan model [LT]', 100, 'LT'), C('unit selected on building map opens its 3D [VC]', 100, 'VC')],
    [U['p5d_price'], U['hs_price'], U['ch_price'], U['rs_price'], U['fp_price'], U['ha_demo'], U['gb_sel']])
row('I02', G, 'Unit picker: building, floor, apartment with availability and price',
    '0 none; 50 plan or community picker with prices; 100 building > floor > unit with live availability.',
    'level 0-100', 4,
    [C('none [VC]', 0, 'VC'), C('none [VC]', 0, 'VC'), C('none [VC]', 0, 'VC'), C('none [VC]', 0, 'VC'), C('none [LT]', 0, 'LT'),
     C('community/plan picker with "starting at" prices on builder site [LT]', 50, 'LT'), C('interactive building/site map with price and availability [VC]', 100, 'VC')],
    [U['p5d_price'], U['hs_price'], U['ch_price'], U['rs_price'], U['fp_demo'], U['ha_demo'], U['gb_sel']])
row('I03', G, 'Developer-controlled option catalogue with upgrade prices',
    '0 none; 50 options without prices; 100 developer-defined options with prices.',
    'level 0-100', 5,
    [C('Enterprise own catalogue [VC]', 50, 'VC'), C('Enterprise catalogue [VC]', 50, 'VC'), C('enterprise catalogues + custom quotation [VC]', 100, 'VC'), C('none [VC]', 0, 'VC'),
     C('none [LT]', 0, 'LT'), C('options live [LT]; option and lot pricing claimed [VC]', 100, 'VC'), C('options with extra cost [VC]', 100, 'VC')],
    [U['p5d_price'], U['hs_price'], U['ch_price'], U['rs_price'], U['fp_demo'], U['ha_show'], U['gb_sel']])
row('I04', G, 'Buildability rules engine validating buyer choices',
    'Attempt 5 known-invalid combinations; % blocked with explanation.',
    '% blocked', 4,
    [C('none [VC]', 0, 'VC'), C('none [VC]', 0, 'VC'), C('none [VC]', 0, 'VC'), C('none [VC]', 0, 'VC'), C('none [LT]', 0, 'LT'),
     C('rules for codes, standards, materials [VC]', 100, 'VC'), UNK('not documented')],
    [U['p5d_price'], U['hs_price'], U['ch_price'], U['rs_price'], U['fp_demo'], U['ha_config'], U['gb_sales']])
row('I05', G, 'Selections flow to developer CRM/ERP with the lead',
    '0 none; 50 via enterprise integration project; 100 out-of-the-box lead with full configuration.',
    'level 0-100', 3,
    [C('Enterprise CRM/ERP/quoting [VC]', 50, 'VC'), C('Enterprise API [VC]', 50, 'VC'), C('Enterprise ERP/CRM [VC]', 50, 'VC'), C('none [VC]', 0, 'VC'),
     C('API only [SL]', 25, 'SL'), C('lead with plan, options, pricing; ERP pricing [VC]', 100, 'VC'), C('selections, margins, automation [VC]', 100, 'VC')],
    [U['p5d_price'], U['hs_price'], U['ch_price'], U['rs_price'], U['fp_price'], U['ha_show'], U['gb_cfg']])
row('I06', G, 'Embeddable in a project page with own branding',
    '0 none; 50 branding only; 100 embed/SDK + white label.',
    'level 0-100', 4,
    [C('white-label planner (Enterprise) [VC]', 100, 'VC'), C('white label (Enterprise) [VC]', 100, 'VC'), C('white-label room planner (Enterprise) [VC]', 100, 'VC'), C('branding on plans [VC]', 50, 'VC'),
     C('embed/API docs linked [SL]', 75, 'SL'), C('embed script observed on builder site [LT]', 100, 'LT'), C('embed on developer website or GBuilder domain [VC]', 100, 'VC')],
    [U['p5d_price'], U['hs_price'], U['ch_price'], U['rs_price'], U['fp_price'], U['ha_demo'], U['gb_sel']])
row('I07', G, 'Tenant-change window and construction-stage awareness',
    'Does the tool know per-unit deadlines for changes and lock categories after their cut-off? 0/50 (deadline shown)/100 (deadline + auto-lock per category).',
    'level 0-100', 3,
    [C('none [VC]', 0, 'VC'), C('none [VC]', 0, 'VC'), C('none [VC]', 0, 'VC'), C('none [VC]', 0, 'VC'), C('none [LT]', 0, 'LT'), UNK('not seen'), UNK('not documented')],
    [U['p5d_price'], U['hs_price'], U['ch_price'], U['rs_price'], U['fp_demo'], U['ha_intro'], U['gb_sales']])

# ---------------- T: trust & honesty ----------------
G = 'trust and honesty labels'
row('T01', G, 'Included / upgrade / decor-only labels on every visual element',
    'Inspect 20 visible items in 3D and in the spec: each labelled as in the base price, paid upgrade, or decoration not included? 0 none; 50 options vs standard distinguished; 100 per-item badges in 3D + spec.',
    'level 0-100', 5,
    [C('none [VC]', 0, 'VC'), C('none [VC]', 0, 'VC'), C('none in tour [LT]', 0, 'LT'), C('none [VC]', 0, 'VC'), C('none [LT]', 0, 'LT'),
     C('standard vs "Upgrade to..." in option text [LT]', 50, 'LT'), C('options with extra cost [VC]', 50, 'VC')],
    [U['p5d_price'], U['hs_price'], U['ch_walk'], U['rs_price'], U['fp_demo'], U['ha_intro'], U['gb_sel']])
row('T02', G, 'Visualisation / AI disclaimer on renders and shares',
    'Rendered or AI image carries a visible "illustration, not a contractual representation" label in-app and on shares. 0/50 (in terms only)/100 (on output).',
    'level 0-100', 4,
    [UNK('walled'), UNK('walled'), C('none on share [LT]', 0, 'LT'), UNK('no sample'), C('none [LT]', 0, 'LT'), C('none seen [LT]', 0, 'LT'), UNK('no demo')],
    [U['p5d_editor'], U['hs_editor'], U['ch_pano'], U['rs_live'], U['fp_demo'], U['ha_intro'], U['gb_sales']])
row('T03', G, 'Plan accuracy disclosure next to dimensions',
    '0 none; 25 label like Beta or human-drawn; 50 page-level caveat; 100 per-dimension tolerance shown in the plan.',
    'level 0-100', 3,
    [C('"measurements are approximate" on page [VC]', 50, 'VC'), C('"Beta" on auto-generate [VC]', 25, 'VC'), C('none [VC]', 0, 'VC'), C('human redraw, 30-day regeneration [VC]', 25, 'VC'),
     C('none [LT]', 0, 'LT'), NA('builder-authored'), NA('developer-supplied')],
    [U['p5d_ai'], U['hs_import'], U['ch_fp'], U['rs_order'], U['fp_demo'], U['ha_intro'], U['gb_sel']])
row('T04', G, 'Data consistency across surfaces',
    'Compare 5 facts (area, rooms, price, item names, locale) between listing page and designer; % consistent.',
    '% consistent', 4,
    [UNK('walled'), C('"100,000+" vs "1M+" models on own pages [LT]', 50, 'LT'), C('Chinese item names on an English share [LT]', 50, 'LT'), UNK('not checked'),
     UNK('not checked'), C('2,830 ft2 on plan page vs 2,889 sqft in configurator [LT]', 0, 'LT'), UNK('no demo')],
    [U['p5d_editor'], U['hs_price'], U['ch_walk'], U['rs_live'], U['fp_demo'], U['ha_intro'], U['gb_sales']])
row('T05', G, 'Site-true orientation and window view',
    '0 none; 50 manual sun; 75 real view or real orientation; 100 geolocated sun path + real floor-height view.',
    'level 0-100', 3,
    [UNK(WALL), UNK(WALL), C('generic exterior backdrop [LT]', 0, 'LT'), UNK('not described'), C('manual sun dial, not geolocated [LT]', 50, 'LT'),
     UNK('lot-specific collateral [VC]; view not seen'), C('"view the actual views" [VC]', 75, 'VC')],
    [U['p5d_editor'], U['hs_editor'], U['ch_pano'], U['rs_live'], U['fp_demo'], U['ha_show'], U['gb_sel']])
row('T06', G, 'Share-link privacy controls',
    '0 none; 50 private by default; 100 password + expiry + no personal data in URL.',
    'level 0-100', 2,
    [UNK('not documented'), UNK('not documented'), C('password, expiry, QR, poster on panorama shares [VC]', 100, 'VC'), UNK('not documented'), UNK('not documented'), UNK('not documented'), UNK('not documented')],
    [U['p5d_share'], U['hs_price'], U['ch_share'], U['rs_price'], U['fp_price'], U['ha_show'], U['gb_sales']])

# ---------------- output ----------------
def cell_text(c):
    d, s, e = c
    tag = {'NA': 'n/a', 'UNK': 'UNK'}.get(e, e)
    sc = '' if s in (None, 'NA') else f' (score {s})'
    return f'{d} {{class={tag}}}{sc}'

with open(OUT, 'w', newline='', encoding='utf-8') as f:
    w = csv.writer(f)
    w.writerow(['id', 'group', 'parameter', 'measure', 'unit', 'weight_1to5'] + PRODUCTS + ['evidence_urls'])
    for r in ROWS:
        urls = ' | '.join(f'{p}: {u}' for p, u in zip(PRODUCTS, r['urls']))
        w.writerow([r['id'], r['group'], r['parameter'], r['measure'], r['unit'], r['weight']] + [cell_text(c) for c in r['cells']] + [urls + ' | all observed 2026-11-10'])

# scores
groups = []
for r in ROWS:
    if r['group'] not in groups:
        groups.append(r['group'])

def score(prod_idx, rows):
    num_v = num_c = den = cov = 0.0
    for r in rows:
        d, s, e = r['cells'][prod_idx]
        if s == 'NA':
            continue
        wgt = r['weight']
        den += wgt
        if s is None:
            continue
        num_c += wgt * s
        num_v += wgt * s * EVW.get(e, 0)
        if e == 'LT':
            cov += wgt
    return (num_v / den if den else 0, num_c / den if den else 0, 100 * cov / den if den else 0)

with open(SCORES, 'w', newline='', encoding='utf-8') as f:
    w = csv.writer(f)
    w.writerow(['scope', 'product', 'verified_score', 'claimed_score', 'live_tested_weight_share_pct'])
    for i, p in enumerate(PRODUCTS):
        v, c, cov = score(i, ROWS)
        w.writerow(['ALL', p, f'{v:.1f}', f'{c:.1f}', f'{cov:.0f}'])
    for g in groups:
        rows = [r for r in ROWS if r['group'] == g]
        for i, p in enumerate(PRODUCTS):
            v, c, cov = score(i, rows)
            w.writerow([g, p, f'{v:.1f}', f'{c:.1f}', f'{cov:.0f}'])

# white-space: best claimed value per parameter across products
best = []
for r in ROWS:
    vals = [c[1] for c in r['cells'] if isinstance(c[1], (int, float))]
    bmax = max(vals) if vals else None
    best.append((r['id'], r['parameter'], r['weight'], bmax))
with open(os.path.join(HERE, 'best-per-parameter.csv'), 'w', newline='', encoding='utf-8') as f:
    w = csv.writer(f)
    w.writerow(['id', 'parameter', 'weight', 'best_claimed_score_any_deep_product'])
    for b in best:
        w.writerow([b[0], b[1], b[2], '' if b[3] is None else b[3]])

print(len(ROWS), 'parameters written')
for i, p in enumerate(PRODUCTS):
    v, c, cov = score(i, ROWS)
    print(f'{p:18s} verified {v:5.1f}  claimed {c:5.1f}  LT-share {cov:4.0f}%')
print('weak everywhere (best claimed < 75):')
for b in best:
    if b[3] is None or b[3] < 75:
        print(' ', b[0], b[2], b[3], b[1])

# ---------------- sensitivity analysis ----------------
import random
random.seed(20261110)
NEUTRAL_GROUPS = {'visualisation', 'plan accuracy', '2D-3D link', 'mobile UX', 'performance'}
NEUTRAL_EXTRA = {'A04', 'A05', 'A06', 'A07', 'A08'}
neutral_rows = [r for r in ROWS if r['group'] in NEUTRAL_GROUPS or r['id'] in NEUTRAL_EXTRA]
target_rows = [r for r in ROWS if r not in neutral_rows]

def score_w(prod_idx, rows, weights):
    num = den = 0.0
    for r, wgt in zip(rows, weights):
        d, s, e = r['cells'][prod_idx]
        if s == 'NA':
            continue
        den += wgt
        if s is None:
            continue
        num += wgt * s * EVW.get(e, 0)
    return num / den if den else 0

lines = []
def rank_report(label, rows, weights):
    vals = [(score_w(i, rows, weights), p) for i, p in enumerate(PRODUCTS)]
    vals.sort(reverse=True)
    lines.append([label] + [f'{p}={v:.1f}' for v, p in vals])

rank_report('verified, buyer weights, all 78', ROWS, [r['weight'] for r in ROWS])
rank_report('verified, equal weights, all 78', ROWS, [1] * len(ROWS))
rank_report('verified, buyer weights, neutral subset', neutral_rows, [r['weight'] for r in neutral_rows])
rank_report('verified, buyer weights, target-fit subset', target_rows, [r['weight'] for r in target_rows])

N = 10000
top = {p: 0 for p in PRODUCTS}
for _ in range(N):
    ws = [max(1, min(5, r['weight'] + random.choice([-1, 0, 1]))) for r in ROWS]
    vals = [(score_w(i, ROWS, ws), p) for i, p in enumerate(PRODUCTS)]
    top[max(vals)[1]] += 1
lines.append(['P(rank 1) under +-1 weight noise, 10k draws'] + [f'{p}={100*top[p]/N:.1f}%' for p in PRODUCTS])

with open(os.path.join(HERE, 'sensitivity.csv'), 'w', newline='', encoding='utf-8') as f:
    csv.writer(f).writerows(lines)
for l in lines:
    print(' ; '.join(l))
