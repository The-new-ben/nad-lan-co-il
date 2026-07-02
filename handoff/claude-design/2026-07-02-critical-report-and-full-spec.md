# NADLAN — CRITICAL DESIGN & 3D EXPERIENCE REPORT + FULL IMPLEMENTATION SPEC
Date: 2026-07-02 · Author: Claude Design · Scope: nad-lan.co.il (live), repo The-new-ben/nad-lan-co-il
Companion docs (already in `handoff/claude-design/`): `2026-06-28-nadlan-master-spec.md` (fix spec),
`2026-06-28-agent-build-prompt.md` (agent leash), `2026-06-27-showroom-engine/` (engine + NOTES.md),
`2026-06-28-mockup/` (the pixel target). This report SUPERSEDES nothing — it deepens them with a
live-site audit, competitor gap analysis, the 3D "drawer" spec with code, and the business logic.

HONESTY STATEMENT: everything in PART 1 is from fetching the live pages on 2026-07-02 (text layer —
I cannot run a real browser against your server, so JS-rendered visuals are inferred from markup and
from the repo code I've read). File references use FUNCTION NAMES and grep-able strings, not line
numbers — line numbers rot with every commit; strings don't. Where something is my judgment rather
than verified fact, it says so. I did not explore `nadlan-strategy-hub`; if that repo is the strategy
home, commit this report there.

═══════════════════════════════════════════════════════════════════════════════
PART 0 — EXECUTIVE VERDICT
═══════════════════════════════════════════════════════════════════════════════

The site's information architecture and SEO content are genuinely strong — better than most Israeli
competitors. The Ashira SEO article is excellent: long, honest, buyer-first, source-cited. The
homepage hub structure (projects / areas / calculators / professionals / guides) is the correct
Zillow-class skeleton. KEEP ALL OF THAT.

What's dragging the product below "showable to contractors" is ONE pattern repeated everywhere:
**accretion**. Widgets keep getting appended to the project page — each individually defensible,
together incoherent. The flagship page currently runs: engine showroom → article → a SECOND floor
picker (with wrong floor count) → a schematic interior-tour widget → mortgage teaser → map → link
cards → a facts table leaking raw enum values → a "claim this card" directory widget → an empty
reviews box. That is nine competing modules, three of which are apartment pickers. A buyer cannot
tell which one is "the product," and a contractor sees clutter, not a premium showroom.

The fix is not more features. It is: ONE picker, ONE narrative order, delete or gate everything
else. The rest of this report specifies exactly that, plus how to make the 3D moment genuinely
world-class.

═══════════════════════════════════════════════════════════════════════════════
PART 1 — LIVE SITE SCAN: DEFECT REGISTER (evidence-based)
═══════════════════════════════════════════════════════════════════════════════

### 1A. Project page — /projects/ashira-sde-dov/ (fetched 2026-07-02)

| # | Severity | Defect (evidence) | Root / file | Fix |
|---|----------|-------------------|-------------|-----|
| D1 | CRITICAL | THREE apartment pickers stacked: engine facade/model (top), "בחרו דירה בבניין" floor strip listing floors 35→1, and a "סיור פנימי בדירה לדוגמה" walkthrough widget | the floor-strip + tour widgets are injected after the article (post body or a later `the_content` hook in `inc/project-page-assembly.php` / a `nadlan-guide` sibling module) | DELETE both lower pickers. One selection system: the engine. Anything they offer (floor list, interior peek) becomes a TAB inside the engine's unit panel (PART 4) |
| D2 | CRITICAL | Floor strip shows 35 floors; Ashira payload says `floors: 20`. Invented data on the flagship page | hardcoded floor count in the widget, not payload-driven | delete with D1; any floor UI must read `floors` from the payload |
| D3 | HIGH | Raw enum leaked to buyers: facts table prints `new_build` | facts-table renderer prints meta value without label map — grep `new_build` in `inc/` (likely `project-page-assembly.php` or `archive-grid.php` helper) | label map: `array('new_build'=>'בנייה חדשה','urban_renewal'=>'התחדשות עירונית',…)`; NEVER echo raw meta (master spec F-4 has the JS twin) |
| D4 | HIGH | "זה הכרטיס שלכם? … בקשו בעלות על הכרטיס" (claim-card widget) on the flagship page | directory claim module renders on ALL nadlan_project singles | gate it: show ONLY on unclaimed auto-imported directory cards (the 965), never when the project is engine-active: `if ( nadlan_showroom_engine_active_for( $post_id ) ) return;` in the claim-card render fn |
| D5 | HIGH | Empty reviews block ("היו הראשונים לשתף חוות דעת" + star input) on a pre-sales project | reviews module unconditional | collapse when zero reviews on `nadlan_project` (graceful-collapse rule); reviews make sense for professionals, not unsold buildings |
| D6 | MEDIUM | "מימון, ייעוץ ועיצוב" band shows a computed monthly payment ("27,177 ₪ החזר חודשי משוער") — an invented-precision number derived from an unofficial estimate | mortgage teaser module | keep the band but show it as a RANGE with the assumptions inline, or link-only ("בדקו החזר חודשי במחשבון ←"). A single shekel-precise number from a non-binding estimate violates the honesty rule |
| D7 | MEDIUM | og:image is SVG: `/wp-json/nadlan/v1/og/4744.svg`. WhatsApp/Facebook/LinkedIn do NOT render SVG og:images → shares show no image | og endpoint in `inc/` (grep `nadlan/v1/og`) | render PNG (1200×630). Server-side: rasterize with GD/Imagick from the same template, or pre-generate per project on save |
| D8 | MEDIUM | og:description is a raw dump of page text ("…סובבו את המודל … בחרו דירה קראו על הפרויקט […]") | Yoast fallback grabbing first content | set per-project meta description (the SEO article's lede is perfect material) |
| D9 | LOW | Engine top shows loading placeholders as static text ("טוען פרויקט", "טוען תיאור פרויקט") in the crawled HTML | engine renders client-side; the shell has placeholder copy | fine for JS, but placeholders should be skeleton shapes, not indexable Hebrew strings; wrap in `aria-busy` divs the engine replaces; keep real SEO text server-side (it already exists below) |
| D10 | LOW | Footer prints the raw wa.me URL as visible text | footer template link text = href | give it a label ("וואטסאפ ←") |

### 1B. Homepage — nad-lan.co.il (fetched 2026-07-02)

| # | Severity | Defect | Fix |
|---|----------|--------|-----|
| H1 | HIGH | `<title>` leads with the mechanism: "דירות חדשות ופרויקטים עם בחירת דירה בתלת ממד". Buyers search apartments, not 3D (owner's own rule) | Title: "דירות חדשות למכירה בתל אביב ובישראל \| NadLan" (pattern: {intent keyword} \| brand). Keep 3D as a differentiator in body copy, never in title/H1 |
| H2 | MEDIUM | Home showroom band shows "טוען פרויקטים / טוען פרויקט / בחרו דירה — קומה — חדרים —" skeleton text in crawlable HTML — a second full apartment-picker UI ON THE HOMEPAGE | The homepage should tease, not duplicate, the project experience. Replace the embedded full picker with the PROJECT BROWSER component (PART 5): poster cards + one lazy 3D preview. Depth lives on the project page |
| H3 | MEDIUM | Language links on the homepage go to the 5 Ashira pages directly — fine for now, but reads as project links, not site languages | label them as project language entries ("Ashira in English") or move under the project card |
| H4 | LOW | Search band ("אזור / מה מחפשים / בדקו עכשיו") — verify it actually filters; a dead search is worse than none | wire to /projects/ archive query args or remove until wired |

### 1C. Catalog — /projects/ (from footer counts: "פרויקטים והתחדשות עירונית (965)")
965 auto-imported cards next to 3 flagship showrooms. The catalog MUST tier: flagship (engine
projects, big cards, poster + "בחירת דירה" badge) → standard (claimed cards) → directory (unclaimed,
compact rows). One undifferentiated grid of 965 buries the product you sell. Renderer:
`inc/archive-grid.php` — add a tier sort: engine-active first (`nadlan_showroom_engine_active_for`),
then claimed, then the rest paginated.

### 1D. What is GOOD and must not be touched
- The SEO article body (structure, honesty, sources block, FAQ-able headings). This is E-E-A-T gold.
- Homepage IA: hero promise → search → projects → checklist → areas → tools/guides/professionals.
- The honest-language system ("אומדן לא מחייב", "בדיקת זמינות") — a real differentiator vs pushy
  developer sites. It converts trust-seeking organic traffic.
- hreflang-ready sibling pages for 5 languages; WhatsApp CTA; healthcheck; monetization rails.

═══════════════════════════════════════════════════════════════════════════════
PART 2 — DESIGN STEERING: THE VIBE (critical + prescriptive)
═══════════════════════════════════════════════════════════════════════════════

### 2A. What the design must say
One sentence: **"A calm, expensive editorial magazine about buying a home — with one dark, cinematic
room in the middle where the building itself is the product."**

The buyer's emotional journey: *arrive anxious (biggest purchase of their life) → feel calm
(editorial cream, honest language, no pressure) → feel excited (the dark theater, the building
responds to their touch) → feel in control (they chose the apartment; the enquiry is about THEIR
unit) → act.* Every design decision is judged against that sequence.

### 2B. The current vibe vs the target
Current (live): a knowledgeable but cluttered portal. Nine modules compete; emoji icons (🏫 🚌 🛒 ⚕️ 🚶)
cheapen the surface; a claim-card and empty reviews say "directory," not "flagship"; raw enums say
"unfinished." The content voice is premium; the visual voice is not yet.
Target (the mockup in `handoff/claude-design/2026-06-28-mockup/`): cream field, one gold hairline
per section head, serif display headings, ONE dark theater, one terracotta CTA per screen,
whitespace as the luxury signal.

### 2C. Non-negotiable design rules (give these to any agent verbatim)
1. **Two worlds, one page.** Cream editorial (`--cream #FAF7F1`) everywhere; dark theater
   (`#14130F→#211F19`) ONLY for the 3D stage and the inquiry block. Never a third background.
2. **One accent does the selling.** Terracotta `#C2563A` appears exactly where money happens (primary
   CTA, project pin, sticky inquire). Gold `#9C7A3C` is structure (eyebrows, rules, accents) — never
   a button fill except the theater's internal controls. Sage `#7A8F6A` = "available" only.
3. **Type hierarchy is the brand.** HE: Frank Ruhl Libre (headings) + Heebo (UI/body). EN: Fraunces +
   Inter Tight. Display sizes from tokens.css. If a heading is under 22px it isn't a heading.
4. **No emoji on buyer surfaces** (replace 🏫🚌🛒⚕️ with the stroke icon set already in engine.js
   `ICON`). No em-dashes. No raw enums. No internal words (model/mesh/GLB/hotspot/token…).
5. **One shadow family** (`--shadow-card`, `--shadow-theater`). Radius 0.25rem. Hairline borders
   `#D9D2C4`. Anything rounder/softer drifts toward AI-slop.
6. **Graceful collapse.** A module with no data renders nothing. No empty boxes, no "be the first."
7. **Density ceiling.** Max ONE module per scroll-viewport on desktop; a section = eyebrow + rule +
   heading + ≤2 content rows. When in doubt, delete.
8. **RTL is first-class.** Logical properties only (`inset-inline-start`, `margin-inline`) — the
   engine CSS already does this; the theme must too. The 3D stage stays `direction:ltr` (model-viewer
   hotspot-mirroring bug — documented in NOTES.md §8).
9. **Motion only on interaction** (hover lift 2px, panel slide 420ms cubic-bezier(.22,.61,.36,1),
   camera fly ~800ms). Nothing auto-animates except the model's idle rotation. Respect
   `prefers-reduced-motion`.
10. **The logo** is the 3-bar ascending mark + NADLAN wordmark (Fraunces 600, +1px tracking) already
    built in the mockup header. Favicon = the 3 bars on ink. Do not commission a new identity;
    ship this one consistently (header, footer, og:image template, favicon).

### 2D. Competitor gap analysis → features to adopt
Research base: the cited findings in `2026-06-28-nadlan-master-spec.md` PART I (Zillow's sectioned
single-scroll redesign, Zestimate value+range, 3-5 comps within ~1.6km/6mo, Compass save/share
collections and Similar-Homes engagement lift). Plus current best practice: <cite index="3-22">high-quality visuals like photos, 3D tours, and videos capture attention, showcase properties effectively, and create a lasting impression</cite>, and <cite index="3-24">CTAs work best when bold, action-focused, and clear to guide users toward next steps like scheduling visits, saving listings, or contacting agents</cite>. For pre-construction specifically, <cite index="9-11,9-12">fully immersive experiences serve remote buyers and international investors — ideal for luxury developments and large-scale projects</cite>, and <cite index="9-18">virtual staging eliminates the need for expensive model units — faster, reusable, and scalable</cite>.

| Competitor pattern | They have | NadLan today | Adopt as |
|---|---|---|---|
| Zillow sectioned single-scroll PDP with sticky section nav | yes | one long unstructured scroll | sticky secnav (master spec C-3) — ship |
| Zillow value + RANGE + "not an appraisal" | yes | "אומדן לפי פנייה" only | estimate range card (master spec F-1) — ship in unit panel + price section |
| Zillow/Madlan recent-deals table | yes | none | comps table via `/nadlan/v1/comps` (F-2) |
| Compass saved collections + share | yes | engine has favorites/compare (not live) | ship engine favorites/compare; add "share this unit" deep link |
| Compass "Similar Homes" cross-sell | yes | "פרויקטים סמוכים" links exist | similar-UNITS row inside the panel ("דירות דומות בפרויקטים סמוכים") — the cross-project tunnel |
| Homes.com neighborhood storytelling | yes | Sde Dov hub exists (good) | link block 8 spokes → area hub anchors |
| NOBODY has | — | interactive per-unit 3D building selection | THIS IS THE MOAT — invest here (PART 4) |

Positioning line for every design decision: *Zillow's data honesty + Compass's editorial calm +
a selection experience none of them have.*

═══════════════════════════════════════════════════════════════════════════════
PART 3 — THE BUYER JOURNEY (press-by-press) & BUSINESS LOGIC
═══════════════════════════════════════════════════════════════════════════════

### 3A. The funnel (SEO → tunnel → money)
```
Google "דירות חדשות בשדה דב" / "פרויקטים חדשים תל אביב" / "מחשבון מס רכישה"
   │
   ├─ AREA HUB (/sde-dov/)          ← ranks on area intent; links every project card
   ├─ GUIDE/TOOL (calculators)      ← ranks on task intent; banner → relevant area/projects
   └─ PROJECT PAGE (ashira…)        ← ranks on brand+intent ("אשירה שדה דב מחירים")
          │  hero promise → theater (choose) → panel (understand) → price/comps (trust)
          │  → world/map (context) → article (depth) → INQUIRY (unit-attached lead)
          ▼
       LEAD with unit context  →  contractor dashboard  →  monetization
```
Every surface has ONE primary CTA pointing down-funnel. Calculators/guides never dead-end: each ends
with "בדקו פרויקטים באזור ←".

### 3B. Press-by-press on the project page (the experience contract)
1. **Land** — hero paints < 1.5s (poster img, server-rendered text). Buyer sees: project name, area,
   the promise ("בוחרים דירה מתוך הבניין"), 3 facts, 2 CTAs. No loading spinners above the fold.
2. **Scroll to theater** — building idles (slow 14°/s rotation). Legend explains 3 colors. Orientation
   pins name the sea / Reading / district. Hint chip: "גררו לסיבוב · הקישו על דירה".
3. **First touch** — drag rotates (auto-rotate pauses). On mobile: one finger pans page, drag inside
   stage rotates (touch-action="pan-y" already set).
4. **Tap a unit** — THE MOMENT (full spec PART 4): scene dims, camera flies to the unit's face, the
   unit "lifts out" toward the viewer, panel slides in with its facts. 900ms total. This is where
   the buyer's brain switches from "browsing a website" to "holding an apartment."
5. **In the panel** — floor/rooms/sqm/balcony/view/facing; estimate RANGE + date + disclaimer; tabs
   תכנית/מבט/סיור (real asset or honest "coming after developer approval" line); save ♥, compare ⇄,
   share. Primary CTA: "מעניין אותי · קומה 10" (unit-labeled, terracotta).
6. **Price section** — range bar + comps table (source + date). Trust before ask.
7. **Inquiry** — form pre-chipped with the chosen unit ("הפנייה מתייחסת לדירה 10C · קומה 10").
   Name + phone OR email only (2 required fields — every extra field costs leads). Sticky bar with
   unit context follows the scroll after 540px. WhatsApp secondary.
8. **After submit** — thank-you + "מה הלאה": add the comparison PDF? see similar units? book a call?
   (post-lead engagement keeps them on-site).

### 3C. Lead & monetization logic (CMS-wired)
- **Lead payload** (already implemented in engine.js `onSubmit`): source, project_slug, lang, unit,
  floor, rooms, sqm, direction, status, message. ADD: `entry_page` (first URL in session — measures
  which SEO page fed the lead) and `saved_units` (localStorage favorites) — 2 fields, huge analytics
  value for selling contractors.
- **Contractor value ladder** (what they pay for): tier 1 directory card (free, claimable — the 965)
  → tier 2 claimed card + media → tier 3 FLAGSHIP SHOWROOM (the engine page: 3D, per-unit leads,
  analytics report: views per unit, saves, compares, leads by floor/type). The per-unit analytics is
  the killer sales artifact — no Israeli portal gives a contractor "unit 18W got 40 saves this week."
- **Claim-card widget** belongs ONLY to tier 1 (defect D4). On flagship pages it destroys the story
  that the contractor already owns a premium presence.
- **Featured placement** (existing auction/upsell modules): flagship projects sort first in catalog
  and home browser — already the plan; keep.

═══════════════════════════════════════════════════════════════════════════════
PART 4 — THE 3D SHOWROOM: FULL TECHNICAL SPEC (the drawer, the quality, the CMS)
═══════════════════════════════════════════════════════════════════════════════

### 4A. Architecture decision (and why)
Two-phase, honestly staged:

- **PHASE A (ship now, 1-2 releases):** keep `<model-viewer>` + the generated concept GLB. The
  "drawer" moment is achieved with camera choreography + a DOM "lift card" + scene dim. 100%
  achievable today with the assets in the repo — code below. No three.js rewrite.
- **PHASE B (when Avisror BIM/professional model arrives):** per-unit meshes in the GLB enable TRUE
  geometry lift-out (the apartment volume itself slides from the building). Contract below so the
  Phase A code doesn't change shape — only gains capability.

Why not three.js custom now: model-viewer gives camera interpolation, hotspot projection, AR,
lazy-loading and a11y for free; a custom three.js viewer is 2-3k lines of new liability that stacks
a fourth renderer generation. Phase B can still mount three.js INSIDE the same section if needed —
behind the same payload contract.

### 4B. PHASE A — the cinematic select ("drawer") with model-viewer — full code
Files: `plugins/nadlan-config/assets/showroom-engine/engine.js` (functions `selectUnit`, `flyChip`,
`closePanel` — grep those names; the skeleton already exists from my handoff) and `showroom.css`.

**4B-1. Camera choreography (the fly-to).** Replace the current instant assignment in `selectUnit()`
with a two-beat move — pull back, then land on the unit's face (reads as "the camera walks around"):

```js
// engine.js — inside selectUnit(id), replacing the single cameraOrbit assignment
function flyCamera(mv, u) {
  var p = project();
  var fr = p.frame_radius_m || 150;
  var end = orbitRadius(u.camera_orbit, Math.round(fr * 0.62)); // land close on the unit
  var endTarget = unitPos(u).pos;
  // beat 1: ease out to a wide orbit on the unit's bearing (300ms)
  var mid = orbitRadius(u.camera_orbit, Math.round(fr * 1.15));
  mv.interpolationDecay = 160;           // slower, filmic interpolation (default 50)
  mv.cameraOrbit = mid;
  setTimeout(function () {
    // beat 2: dive to the unit face + retarget (model-viewer interpolates both)
    mv.cameraTarget = endTarget;
    mv.cameraOrbit  = end;
    mv.fieldOfView  = '28deg';
  }, 300);
  setTimeout(function () { mv.interpolationDecay = 50; }, 1400); // restore snappy manual orbit
}
```
`interpolationDecay` is the under-used model-viewer property that makes camera moves feel directed
instead of snappy — that alone is 50% of the "cinematic" feel.

**4B-2. The lift-out drawer card.** The current `flyChip` (a small floor-number chip) upgrades to an
"apartment card" that visually LIFTS from the unit's position on the facade, scales up while the
scene dims, then docks into the panel header. Works on any model because it's DOM, keyed to the
hotspot's projected screen position:

```js
// engine.js — replace flyChip() with liftCard()
function liftCard(srcEl, u) {
  var panelEl = document.getElementById('nl-panel'); if (!panelEl || !srcEl) return;
  var s = srcEl.getBoundingClientRect();
  var card = document.createElement('div');
  card.className = 'nl-lift';
  card.innerHTML =
    '<div class="nl-lift__floor">' + esc(u.floor) + '</div>' +
    '<div class="nl-lift__meta">' + esc(roomsLabel(u.rooms)) + ' · ' + esc(u.sqm) + ' ' + esc(t('sqm_unit')) + '</div>' +
    '<div class="nl-lift__dir">' + esc(dirLabel(u.dir)) + '</div>';
  document.body.appendChild(card);
  var head = panelEl.querySelector('.nl-panel__title') || panelEl;
  requestAnimationFrame(function () {
    var d = head.getBoundingClientRect();
    var x0 = s.left + s.width / 2, y0 = s.top + s.height / 2;
    var x1 = d.left + d.width / 2, y1 = d.top + d.height / 2;
    card.animate([
      { transform: 'translate(' + (x0 - 90) + 'px,' + (y0 - 60) + 'px) scale(.32)', opacity: .0 },
      { transform: 'translate(' + (x0 - 90) + 'px,' + (y0 - 130) + 'px) scale(1)', opacity: 1, offset: .38 },  // lift straight OUT of the building
      { transform: 'translate(' + ((x0 + x1) / 2 - 90) + 'px,' + (Math.min(y0, y1) - 150) + 'px) scale(1.02)', opacity: 1, offset: .7 },
      { transform: 'translate(' + (x1 - 90) + 'px,' + (y1 - 60) + 'px) scale(.45)', opacity: 0 }
    ], { duration: 920, easing: 'cubic-bezier(.22,.61,.36,1)' }).onfinish = function () { card.remove(); };
  });
}
```
```css
/* showroom.css — the lift card (dark, gold-edged, reads as "the apartment") */
.nl-lift { position: fixed; z-index: 70; width: 180px; padding: 14px 16px; pointer-events: none;
  border-radius: 10px; border: 1.5px solid #cdb274;
  background: linear-gradient(180deg, rgba(38,35,28,.97), rgba(20,19,15,.97));
  color: #f4eede; box-shadow: 0 30px 60px -18px rgba(0,0,0,.75); }
.nl-lift__floor { font-family: var(--font-serif-he); font-size: 34px; font-weight: 700; line-height: 1; }
.nl-lift__meta  { font-size: 13px; color: #d8c79a; margin-top: 6px; }
.nl-lift__dir   { font-size: 12px; color: #b8b1a2; margin-top: 2px; }
```
Sequence when a hotspot is tapped: `selectUnit()` → scrim `.is-on` (dim, spotlight origin at the
hotspot — already implemented) → `flyCamera()` (beat 1 starts) → `liftCard()` (drawer lifts during
beat 1-2) → panel `.is-open` slides (existing 420ms transform). Total ≈ 920ms, all three motions
overlapping — that's the "drawer out of the building" the owner asked for, TODAY, without BIM.

**4B-3. The interior peek ("see inside").** Do NOT fake a 3D interior. The honest ladder:
1. Now: tab "מבט" shows the unit's view photo / plan; if absent, the "coming after developer
   approval" line (already implemented).
2. When the developer provides a 360 pano (one equirect JPG per unit type): render it inside the
   SAME panel tab with a tiny pano viewer — model-viewer trick: a sphere GLB with the pano as
   emissive texture, `camera-controls` + `disable-zoom`, camera inside. One 4k JPG ≈ 800KB. Payload
   field `pano_url` per unit (already reserved as `tour_url`/`interior_url` in NOTES.md §3).
3. When Matterport exists: `tour_url` → embed iframe inside the tab (lazy, on tab click only).
No new page, no new module — everything inside the panel. This kills the D1 duplicate-tour widget.

**4B-4. Facade sync.** Selecting anywhere (hotspot / facade square / inventory card) drives the
same `selectUnit(id)` — already true in engine.js. Keep it the law: ONE select function, three
entry surfaces.

### 4C. PHASE B — real-model contract (when BIM/pro model arrives)
Asset contract (give this to Avisror / the 3D vendor verbatim):
- Format: glTF 2.0 (.glb), Y-up, meters, origin at building center ground level.
- **Every sellable unit is a separate named mesh/node: `UNIT_<id>`** (e.g. `UNIT_ashira-18-west`),
  ids matching CMS `project_3d_units[].id`. Shared shell (core, slabs, facade) in separate nodes.
- Materials: PBR, ≤ 4 texture sets @ 2048px, KTX2/BasisU compressed; Draco geometry compression.
- Budget: ≤ 8 MB total, ≤ 300k triangles.
- Optimization command (run per delivery, in repo CI or locally):
```bash
npx @gltf-transform/cli optimize input.glb output.glb --compress draco --texture-compress ktx2 --simplify 0.75
```
With named unit nodes, Phase B upgrades in ONE engine function: on select, model-viewer's
`model.materials` / scene-graph API sets the unit's material `emissiveFactor` + moves the node 1.2m
outward along its facade normal (true geometry drawer), everything else unchanged. If model-viewer's
scene-graph API proves too limited for the node translation, mount three.js in the same stagewrap
(`GLTFLoader` + the same payload) — the select/panel/lead layers don't change at all.

### 4D. Model & stage quality bar (why the current one "looks like nothing" and the fix)
The live model regressed because a 3.7KB box-massing replaced the 170KB detailed model (that swap is
already reverted per the Claude-Code session — VERIFY `project_model_glb` meta points to
`assets/showroom-engine/models/ashira.glb`, 170KB, not `ashira-massing.glb`). Beyond that:
- **Lighting is 80% of perceived quality.** In `showroom-engine.php` the `<model-viewer>` attrs must
  include `environment-image="neutral" exposure="1.02" shadow-intensity="0.55" shadow-softness="1"`.
  A GLB that looks flat almost always = no environment light.
- **Never under the building:** `min-camera-orbit="auto 46deg auto" max-camera-orbit="auto 87deg auto"`
  + radius clamps from `frame_radius_m` (implemented in engine.js `afterRender` — keep).
- **Poster-until-paint:** `#nl-poster` covers the stage until the `load` event (implemented — keep;
  this is the no-blank-flash guarantee).
- **Context = trust:** the concept scene already includes sea plane, beach, street grid, Reading
  Tower landmark, context blocks. When regenerating any project model use the generator in this
  project's history (parameters in `handoff/claude-design/2026-06-27-showroom-engine/NOTES.md` §1)
  — a lone tower on a void reads fake; a tower in a city reads real.

### 4E. CMS wiring — how EVERY new project gets all of this with zero code
The payload builder `nadlan_showroom_engine_build_project()` in `inc/showroom-engine.php` maps post
meta → engine fields (table in NOTES.md §3). Onboarding a new project is DATA ENTRY ONLY:
1. Create `nadlan_project` post (+ language siblings when translated).
2. Fill meta: `project_floors`, `project_3d_floor_height_m`, `project_model_glb` (concept GLB from
   the generator or vendor GLB), `project_model_poster`, `project_3d_facade_images`,
   `project_3d_units` (id, label, floor, rooms, sqm, balcony, dir, status, stage_x/y, camera_orbit),
   `project_3d_avg_price_per_sqm`, area taxonomy.
3. The engine renders the full experience; the catalog and home browser pick it up from the same CPT
   query. NOTHING is hardcoded per project — if an agent ever writes "ashira" inside engine.js or a
   template, reject the PR (grep gate: `grep -rn "ashira" assets/showroom-engine/engine.js` = 0).

═══════════════════════════════════════════════════════════════════════════════
PART 5 — HOMEPAGE PROJECT BROWSER (replace the embedded full picker)
═══════════════════════════════════════════════════════════════════════════════

Concept: a cream band, "הפרויקטים שלנו", horizontal row of flagship cards. Each card = poster image
(static, fast), name, tagline, unit count, availability dots. ONE card at a time can go live-3D:
hover (desktop) / "סובבו את הבניין" button (mobile) swaps the poster for a `<model-viewer>` with the
same GLB, auto-rotate, NO hotspots (depth lives on the project page). Click anywhere → project page.

Rules that keep it fast and unbroken:
- Exactly ONE `<model-viewer>` instance on the homepage, created lazily on first hover/tap
  (`IntersectionObserver` + event), reused across cards by swapping `src`. Never N live viewers.
- `loading="lazy" reveal="interaction"` so zero GPU cost until the user asks.
- Card CTA text: "כניסה לפרויקט ←"; badge: "בחירת דירה" (the moat, in buyer words).

```js
// home browser: one shared viewer, swapped between cards (vanilla, engine.js homeMain() add-on)
var shared = null;
function preview3D(card, glbUrl, posterUrl) {
  if (!shared) {
    shared = document.createElement('model-viewer');
    shared.setAttribute('camera-controls', ''); shared.setAttribute('auto-rotate', '');
    shared.setAttribute('interaction-prompt', 'none');
    shared.setAttribute('environment-image', 'neutral');
    shared.setAttribute('rotation-per-second', '16deg');
    shared.style.cssText = 'position:absolute;inset:0;width:100%;height:100%;direction:ltr;';
  }
  shared.setAttribute('poster', posterUrl);
  shared.setAttribute('src', glbUrl);           // swapping src reuses the one GPU context
  card.querySelector('.nl-pcard__img').appendChild(shared);
}
```
PHP side: the home band is the existing shortcode with `page="home"` (`[nadlan_showroom_engine
page="home"]`) — the gallery renderer already exists in engine.js `homeMain()`; add the preview3D
behavior there. The homepage full picker (H2) is REMOVED in the same release (no-stacking law).

═══════════════════════════════════════════════════════════════════════════════
PART 6 — WORDPRESS EMBEDDING RULES (exact anchors, no breaking)
═══════════════════════════════════════════════════════════════════════════════

File: `plugins/nadlan-config/inc/showroom-engine.php` (all anchors are function names — grep them):
- `nadlan_showroom_engine_active_for( $post_id )` — the single gate. Claim-card, reviews, legacy
  pickers, project-3d ALL check this and stand down when true.
- `nadlan_showroom_engine_build_project()` — payload builder. Additions land here (lang_urls,
  avg_price_per_sqm, area record — master spec PART E / F).
- The `the_content` prepend (priority 8) mounts `#nl-root` — the strip filter (priority 7) that
  removes legacy `<main class="nlv2-showroom">` must stay ABOVE it forever (regression test:
  `.nlv2-showroom` count = 0).
- Enqueues: `nadlan-engine-tokens` → `nadlan-engine-style` → `nadlan-engine-editorial` →
  model-viewer (module) → `nadlan-engine-i18n` → inline payload (`wp_add_inline_script`, position
  `before`) → `nadlan-engine-core`. Any new CSS/JS joins THIS chain — never a second chain, never
  inline `<script>` in post bodies.
- CSS isolation: all engine selectors are `.nl-*`; editorial is scoped `.nadlan-project-article` /
  `.entry-content .nadlan-guide`. The theme must never style `.nl-*`; the engine must never style
  bare tags. That's the no-bleed contract in both directions.
- Version surfaces (all bumped together, every release): plugin header, `NADLAN_CONFIG_VERSION`
  constant if defined, enqueue `?ver`, `nadlan-config.json` manifest (version + download_url +
  changelog), rebuilt ZIP. Healthcheck must echo it after deploy.
- Tokens → `theme.json`: mirror cream/ink/gold/terracotta/sage/border into `settings.color.palette`
  so native blocks inherit the brand (one-time change, theme repo).

═══════════════════════════════════════════════════════════════════════════════
PART 7 — SEO SPEC (hard-keyword machine)
═══════════════════════════════════════════════════════════════════════════════

- **Titles/H1 = buyer intent, never mechanism** (defect H1). Patterns:
  home "דירות חדשות למכירה בישראל | NadLan" · area "דירות חדשות בשדה דב — מחירים, פרויקטים ומפה |
  NadLan" · project "דירות למכירה ב{project} {area} | מחירים ותוכניות | NadLan" (the live project
  title is already right).
- **JSON-LD per project page** (emit in `wp_head`, from payload — one template):
```php
$ld = array(
  '@context' => 'https://schema.org', '@type' => 'ApartmentComplex',
  'name' => $proj['building'], 'url' => get_permalink(),
  'address' => array('@type'=>'PostalAddress','addressLocality'=>'תל אביב-יפו','addressCountry'=>'IL'),
  'numberOfAccommodationUnits' => count( $proj['units'] ),
  'petsAllowed' => null, // omit unknowns entirely — no fake fields
);
printf('<script type="application/ld+json">%s</script>', wp_json_encode( array_filter( $ld ) ));
```
  Plus `FAQPage` from the article's Q-headings and `BreadcrumbList`. Never `Product`+price schema on
  non-binding estimates (Google penalty risk + honesty rule).
- **og:image → PNG** (defect D7); template = poster crop + logo bar, 1200×630.
- **hreflang**: emit server-side from `lang_urls` (master spec PART E-4) — only published siblings.
- **Freshness**: daily comps cron updates `comps_last_refresh` + page `<lastmod>`; IndexNow on save
  (exists). The comps table gives every project page a real "updated today" signal.
- **Internal mesh**: project ⇄ area hub ⇄ tools ⇄ professionals (mostly exists; block 8 spokes must
  link INTO the area hub anchors, not be dead chips).
- **Skeleton text** (D9): loading placeholders must not be indexable copy.

═══════════════════════════════════════════════════════════════════════════════
PART 8 — RELEASE ROADMAP (each = one PR, gated per master-spec PART J)
═══════════════════════════════════════════════════════════════════════════════

R1 **De-clutter the flagship** — delete duplicate floor-strip + tour widget (D1/D2); gate claim-card
   (D4); collapse empty reviews (D5); enum label map (D3); mortgage teaser → range/link (D6).
   GATE: page = engine → price → world → article → inquiry → disclaimer. Nothing else.
R2 **Language + hreflang** (master spec PART E) — switcher navigates siblings; server hreflang;
   PNG og (D7) + meta description (D8). GATE: click-through all 5 languages.
R3 **Cinematic select** — interpolationDecay fly (4B-1), lift card (4B-2), panel polish.
   GATE: tap→panel ≤ 1s, 60fps on mid-range mobile, screenshots desktop+390.
R4 **Price + comps + map data** (master spec F-1/F-2/G-map). GATE: range+date+source visible;
   comps ≤ 6 months; Mapbox pins from area record.
R5 **Homepage browser** (PART 5) — replaces embedded picker (H2); title fix (H1); catalog tiering
   (1C). GATE: one live viewer max; LCP ≤ 2.5s.
R6 **Similar units + saved/compare live + lead analytics fields** (3C). GATE: lead JSON carries
   entry_page + saved_units; contractor report query works.

═══════════════════════════════════════════════════════════════════════════════
PART 9 — WHAT I NEED FROM THE OWNER (blockers, honestly)
═══════════════════════════════════════════════════════════════════════════════
1. Confirm R1 deletions (the duplicate pickers/widgets are someone's work — I'm telling you to
   delete them; the interior-peek value returns INSIDE the panel in R3).
2. Mapbox token + confirmation the WhatsApp number (972525101555, live in footer) is the lead line.
3. From Avisror when available: BIM/pro model per the PART 4C contract, real photos, price list,
   approved plans, 360 panos. Until then everything stays labelled הדמיה להמחשה.
4. Decision: keep title-tag rewrite (H1) — it changes what you rank for, in the right direction.

END OF REPORT.
