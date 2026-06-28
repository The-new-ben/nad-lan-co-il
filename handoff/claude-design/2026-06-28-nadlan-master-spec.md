# NadLan — MASTER BUILD & FIX SPEC (the single source of truth)
Date 2026-06-28 · Author Claude Design · For: owner + any build agent (Claude Code / other)
Repo The-new-ben/nad-lan-co-il · Theme `nadlan-revenue` · Plugin `nadlan-config` (v1.69.x)

This document + `2026-06-28-agent-build-prompt.md` are a matched pair. This is the REFERENCE
(what to build, exact). The prompt is the EXECUTABLE INSTRUCTION (how the agent must work, with
boundaries). Nothing here is left to interpretation. Where you see `CODE:` it is paste-ready and
must be used as written unless the agent has a concrete reason logged in the PR.

═══════════════════════════════════════════════════════════════════════════════════════
PART A — GROUND TRUTH (verified 2026-06-28, do not re-litigate)
═══════════════════════════════════════════════════════════════════════════════════════

WHAT WORKS (do NOT rebuild — this is good and must be preserved):
- The ROOT homepage `https://nad-lan.co.il/` renders correctly. It is a real real-estate hub:
  hero "לפני שחותמים – יודעים", 6 live calculators (mortgage, purchase-tax, buy-vs-rent, yield,
  value-estimate, Airbnb-abroad), guides, neighborhoods, professionals index (2,711), glossary.
  This is already a Zillow/Compass-class CONTENT surface. KEEP IT.
- The plugin `nadlan-config` is a mature product: CPTs `nadlan_project` / `nadlan_property` /
  `nadlan_professional` / `nadlan_lead`; SEO machinery (Yoast, IndexNow, schema, sitemap, og-image);
  monetization (advertiser-center, greeninvoice billing, placement-auction, featured-upsell);
  lead AI. DO NOT refactor or "clean up" this. Touch only the showroom + project-page surface.
- The showroom engine IS ported into `plugins/nadlan-config/assets/showroom-engine/` (engine.js,
  showroom.css, tokens.css, i18n.js, data.js, models/, mapbox-init.js) and wired by
  `inc/showroom-engine.php`. The factory architecture is sound.

WHAT IS BROKEN (the actual defects to fix, root-caused):
1. STACKING on the project page — the #1 problem. Three layers render on /projects/ashira-sde-dov/:
   (a) the live engine `#nl-root`, (b) a DUPLICATE static `<main class="nlv2-showroom">` baked into
   the post body, (c) an unstyled SEO article. Result: showroom shown twice, then a wall of text.
   → Fix in PART C-1. (A v1.69.52 release attempted this; verify it actually removed the duplicate
     in a real browser, not just in code.)
2. LANGUAGE SWITCHER broken / "only English loads." Root cause: each language is a SEPARATE
   WordPress post (`ashira-sde-dov`, `-en`, `-fr`, `-ru`, `-ar`). The engine's language bar does a
   CLIENT-SIDE string swap only; it does not navigate to the sibling post, and the per-page article
   is single-language. So switching does nothing useful, and whichever post you land on is "stuck"
   in its language. → Fix in PART E (language switcher must navigate to sibling posts via a
   payload-provided URL map, AND set the engine UI language to match).
3. "Homepage is 404." The ROOT renders. The 404 is one of: the engine gallery route (`home.html`
   has no WordPress home; the catalog lives at `/projects/`), OR a language homepage that was never
   created (e.g. `/en/`), OR the `/projects/` archive template missing. → Fix in PART D-0: the
   project CATALOG at `/projects/` is the gallery; do not rely on the standalone `home.html`.
4. UNSTYLED article — the SEO body renders in default theme type. → Fix: enqueue `editorial.css`
   (already written, in this handoff) on single `nadlan_project`. PART C-2.
5. i18n LEAK — `dir_מערב` style raw keys can show if a unit's `dir` value isn't a known enum. →
   Fix in PART F-4 (normalize `dir`/`status` to enums before render; never echo a raw key).

CONFIDENCE: items 1,2,4,5 are verified from the live HTML + the plugin code. Item 3 needs the agent
to reproduce the exact 404 URL first (PART D-0 step 1) — do not guess which route.

═══════════════════════════════════════════════════════════════════════════════════════
PART B — THE MISTAKES LOG (why it kept breaking — the agent MUST read this)
═══════════════════════════════════════════════════════════════════════════════════════

M1. STACKING instead of replacing. Every past agent ADDED a new showroom layer on top of the old
    one instead of removing the old one. Three generations now coexist. RULE: when you add a
    renderer, you MUST disable/remove the previous one in the SAME release, and prove in a browser
    that only ONE renders.
M2. Editing `post_content` with fragile assumptions. The duplicate showroom lives in the DB post
    body. Stripping it with a loose regex risks eating the article too. RULE: cut on a SINGLE,
    unique, self-contained boundary (`<main class="nlv2-showroom">…</main>`), back up the original
    body to post meta first, and make it reversible + idempotent.
M3. Claiming files were delivered that never landed in the repo. A prior "integration spec +
    editorial.css" was described but not pushed. RULE: after writing, run `git status` + `git show
    --stat HEAD` and paste the file list in the PR. "Done" means present on `main`, verified.
M4. Shipping without browser proof. Code-level "looks right" ≠ renders right (model-viewer is
    client-rendered; web-fetch can't see it). RULE: every release is gated by REAL screenshots at
    1440 desktop + 390 mobile, in HE and EN, attached to the PR.
M5. Inventing prices / certainty. Fake "₪X" numbers destroy trust and are legally risky. RULE:
    show an estimate RANGE from public comps, always labelled "אומדן לא מחייב", never a single
    invented price.
M6. Breaking language pages. Treating the 5 posts as one. RULE: the 5 language posts are siblings;
    the switcher NAVIGATES between them; each is independently crawlable.
M7. Touching the whole plugin / theme. Over-broad edits broke unrelated surfaces. RULE: scope every
    change to the showroom + single-project template. Never edit calculators, directory, billing.

═══════════════════════════════════════════════════════════════════════════════════════
PART C — FIX THE PROJECT PAGE (do these first, in order, one release each)
═══════════════════════════════════════════════════════════════════════════════════════

C-1. DE-STACK (verify or implement). Goal: exactly ONE showroom on the page.
  Step 1 — reproduce: `wp post get <ashira_en_id> --field=content | grep -c "nlv2-showroom"`.
           If > 0, the duplicate is still in the body.
  Step 2 — strip on the unique boundary, reversible + idempotent. CODE (PHP, render-time filter so
           it works even if the body still holds it; priority BEFORE the engine prepend at 8):
  ```php
  add_filter( 'the_content', function ( $html ) {
      if ( ! is_singular( 'nadlan_project' ) || ! in_the_loop() || ! is_main_query() ) return $html;
      // Remove the legacy static showroom block by its unique wrapper. DOM-safe: single boundary.
      $open = '<main class="nlv2-showroom"';
      $s = strpos( $html, $open );
      if ( $s !== false ) {
          $e = strpos( $html, '</main>', $s );
          if ( $e !== false ) { $html = substr( $html, 0, $s ) . substr( $html, $e + 7 ); }
      }
      return $html;
  }, 7 ); // 7 = before the engine prepend at 8
  ```
  Step 3 — prove: load the page, assert `document.querySelectorAll('.nlv2-showroom').length === 0`
           AND `document.querySelectorAll('#nl-root').length === 1`. Screenshot.

C-2. STYLE THE ARTICLE. Copy `editorial.css` (in this handoff at
  `handoff/claude-design/2026-06-27-showroom-engine/engine/editorial.css`) to
  `plugins/nadlan-config/assets/showroom-engine/editorial.css`, then enqueue it in
  `nadlan_showroom_engine_shortcode()` right after `showroom.css`:
  ```php
  wp_enqueue_style( 'nadlan-engine-editorial', $base . 'editorial.css',
      array( 'nadlan-engine-tokens' ), '1.69.53' );
  ```
  Also wrap the article body so the CSS has a hook: ensure the SEO section carries
  `class="nadlan-project-article nadlan-guide"`. (The editorial.css styles both `.nadlan-guide*`
  and generic h2/p/ul inside `.nadlan-project-article`.)

C-3. SECTION NAV (Zillow pattern). Add a sticky in-page nav under the hero so the long page is
  navigable: tabs scroll to the engine sections. The engine already has the sections
  (theater, inventory, world, media, about, inquiry); add a sticky strip. CODE pattern (vanilla,
  add to engine.js `projectMain()` right after the hero):
  ```html
  <nav class="nl-secnav"><a href="#theater">בניין</a><a href="#inventory">דירות</a>
  <a href="#world">סביבה</a><a href="#about">מידע</a><a href="#inquiry">פנייה</a></nav>
  ```
  ```css
  .nl-secnav{position:sticky;top:64px;z-index:30;display:flex;gap:18px;overflow-x:auto;
    background:rgba(250,247,241,.92);backdrop-filter:blur(8px);border-bottom:1px solid var(--border);
    padding:12px clamp(14px,3vw,28px)}
  .nl-secnav a{white-space:nowrap;font-size:14px;font-weight:600;color:#4b4639;text-decoration:none}
  .nl-secnav a.is-active{color:var(--ink);border-bottom:2px solid var(--gold);padding-bottom:6px}
  ```

═══════════════════════════════════════════════════════════════════════════════════════
PART D — INFORMATION ARCHITECTURE (the whole site)
═══════════════════════════════════════════════════════════════════════════════════════

D-0. The 404. Reproduce the exact URL first. Then:
  - If it's the project CATALOG: the gallery is the `nadlan_project` archive at `/projects/`. Ensure
    `templates/archive-nadlan_project.html` (or the plugin's `archive-grid.php`) renders the engine
    gallery OR a card grid. Do NOT depend on the standalone `home.html` from the handoff — that was a
    prototype shell; on WordPress the catalog is `/projects/`.
  - If it's a language homepage (`/en/`): either create it or remove the link. Don't link to routes
    that don't exist.

D-1. SITE MAP (what exists / what to add):
  - `/` root hub (KEEP as-is). Add ONE band: "פרויקטים חדשים" featuring 3-4 project cards → `/projects/`.
  - `/projects/` CATALOG (gallery of all `nadlan_project`, featured/paid first). This is a key SEO page.
  - `/projects/<slug>/` PROJECT PAGE (the showroom + article). 5 language siblings each.
  - `/sde-dov/`, `/ramat-aviv/` … AREA hubs (already exist). Link each project to its area; link the
    area to its projects (the "full world" connective tissue, Compass-style).
  - Tools/calculators/professionals/glossary (KEEP).

D-2. THE PROJECT PAGE — section order (Zillow's sectioned single-scroll, adapted). Each is an engine
  block; each collapses cleanly if its data is absent (no empty box, no fake):
  1. HERO — name, area, one-line value, poster image, 2 CTAs (enquire / choose apartment), key facts.
  2. SECTION NAV (sticky) — C-3.
  3. THE BUILDING (3D theater) — model-viewer + apartment hotspots + orientation pins (sea/Reading).
  4. APARTMENTS (inventory + facade backup) — filterable list; facade selector as the mobile/precise
     picker; selecting drives the slide-out panel.
  5. SELECTED APARTMENT (slide-out) — facts, plan/view/tour tabs, save/compare/share, enquire.
  6. PRICE & COMPS (NEW — Zillow/Compass pattern) — see PART F: an estimate RANGE + recent nearby
     deals (Madlan/gov comps). Honest, non-binding, dated, sourced.
  7. THE COMPLETE WORLD (neighborhood) — real map (Mapbox) + transport/education/facilities/stats +
     nearby projects. PART G-map.
  8. MEDIA — gallery/video/tour (collapses while empty).
  9. ABOUT / SEO ARTICLE — the long buyer guide (styled via editorial.css). The SEO asset.
  10. INQUIRY (money moment) — unit-context-attached form + sticky inquire/WhatsApp.
  11. DISCLAIMER — illustrative notice.

═══════════════════════════════════════════════════════════════════════════════════════
PART E — LANGUAGE / i18n (one-click switch, SEO-safe) — CRITICAL, currently broken
═══════════════════════════════════════════════════════════════════════════════════════

ARCHITECTURE: 5 separate WordPress posts per project (one per language), each its own crawlable URL,
each with its own translated article + Yoast meta. The engine UI strings come from i18n.js. The
language bar must do BOTH: (1) navigate to the sibling post, (2) set engine UI language.

E-1. Provide a per-project language map in the payload. In `nadlan_showroom_engine_build_project()`
  add the sibling URLs (resolve by slug convention `<base>` / `<base>-en` / `-fr` / `-ru` / `-ar`):
  ```php
  $langs = array(); $bases = array('he'=>'','en'=>'-en','fr'=>'-fr','ru'=>'-ru','ar'=>'-ar');
  // derive the canonical base slug (strip any -en/-fr/-ru/-ar suffix)
  $canon = preg_replace('/-(en|fr|ru|ar)$/', '', $post->post_name);
  foreach ( $bases as $lng => $suf ) {
      $sib = get_page_by_path( $canon . $suf, OBJECT, 'nadlan_project' );
      if ( $sib ) { $langs[ $lng ] = get_permalink( $sib->ID ); }
  }
  // …add to the returned project array: 'lang_urls' => $langs,
  // …and set the page's own language from its slug suffix:
  $self_lang = 'he';
  foreach ( array('en','fr','ru','ar') as $l ) { if ( substr($post->post_name,-3) === '-'.$l ) $self_lang = $l; }
  // pass $self_lang into config.default_lang for THIS render.
  ```
E-2. In `config`, set `default_lang` to the page's own language (so the EN post loads in EN, HE in HE).
E-3. In engine.js `switchLang(l)`: if `project().lang_urls[l]` exists, `location.href = that URL`
  (navigate to the sibling post). Else fall back to client-side string swap. CODE:
  ```js
  function switchLang(l){
    var p = project();
    if (p && p.lang_urls && p.lang_urls[l]) { location.href = p.lang_urls[l]; return; }
    if (!I18N.langs[l]) return;
    state.lang = l; var u=new URL(location.href); u.searchParams.set('lang',l);
    history.replaceState(null,'',u); render();
  }
  ```
E-4. hreflang (SEO): emit the reciprocal set server-side from the same `lang_urls`, in `wp_head` on
  single project pages, only for languages whose sibling post exists + is published:
  ```php
  add_action('wp_head', function(){
    if (!is_singular('nadlan_project')) return;
    $pid = get_queried_object_id();
    $proj = nadlan_showroom_engine_build_project( get_post($pid) );
    if (empty($proj['lang_urls'])) return;
    foreach ($proj['lang_urls'] as $lng=>$url) {
      printf('<link rel="alternate" hreflang="%s" href="%s">'."\n", esc_attr($lng), esc_url($url));
    }
    $xd = $proj['lang_urls']['he'] ?? reset($proj['lang_urls']);
    printf('<link rel="alternate" hreflang="x-default" href="%s">'."\n", esc_url($xd));
  }, 5);
  ```
E-5. RTL: `he` + `ar` are RTL; `en`/`fr`/`ru` LTR. The engine already sets `<html dir>` from
  `rtl_languages`. The model-viewer stage MUST stay `direction:ltr` (known model-viewer RTL bug —
  hotspots mirror otherwise). KEEP `.nl-stage{direction:ltr}`.

ACCEPTANCE: on `/projects/ashira-sde-dov-en/` the page loads in English; clicking עברית/HE navigates
to `/projects/ashira-sde-dov/` and it loads in Hebrew RTL; view-source shows 5 hreflang + x-default.

═══════════════════════════════════════════════════════════════════════════════════════
PART F — DATA LAYER (live, Zillow/Compass-grade, honest)
═══════════════════════════════════════════════════════════════════════════════════════

F-1. PRICE ESTIMATE + RANGE (the Zestimate pattern, done honestly). Never a single invented number.
  Show: a midpoint estimate + a low–high range + "אומדן לא מחייב, מבוסס עסקאות ציבוריות, עודכן <date>".
  Source per-sqm from the project meta `project_3d_avg_price_per_sqm` (already used for Rainbow) ×
  unit sqm, with a ±band (e.g. ±12%). CODE (engine, in the apartment panel):
  ```js
  function estimate(u){
    var ppsqm = +(project().avg_price_per_sqm||0); if(!ppsqm) return null;
    var mid = ppsqm*u.sqm, lo=Math.round(mid*0.88/10000)*10000, hi=Math.round(mid*1.12/10000)*10000;
    return {lo:lo, hi:hi, note:t('estimate_note')}; // render "₪lo – ₪hi" + note, never a single ₪
  }
  ```
F-2. COMPARABLE DEALS (the comps section). Pull recent nearby transactions (rashut hamisim / Madlan)
  for the area, filtered to similar rooms/sqm, last 6 months, within ~1km (the standard comp window).
  The plugin already imports gov data (`inc/import.php`, `avm-deals.php`). Wire a REST endpoint
  `/wp-json/nadlan/v1/comps?area=sde-dov&rooms=4` returning 3-5 deals; render a small table in the
  Price & Comps section. Honest label: "עסקאות שנמכרו באזור, מקור: רשות המסים".
F-3. LIVE DATA refresh. Comps + estimate update via a daily WP-Cron that re-pulls gov/Madlan data
  into post meta (don't fetch on every page view — cache in meta, refresh daily). The healthcheck
  should report `comps_last_refresh`.
F-4. NORMALIZE ENUMS (fix the i18n leak). Before render, map any free `dir`/`status` to a known enum;
  if unknown, show the raw Hebrew value, NEVER the key `dir_xxx`. CODE (engine normalize step):
  ```js
  var DIRS={west:1,east:1,north:1,south:1,'south-west':1,'north-west':1,'south-east':1,'north-east':1};
  function dirLabel(d){ return DIRS[d] ? t('dir_'+d) : (d||''); }   // never echo 'dir_'+unknown
  ```

═══════════════════════════════════════════════════════════════════════════════════════
PART G — DESIGN SYSTEM (tokens + components, exact)
═══════════════════════════════════════════════════════════════════════════════════════

TOKENS (locked — in tokens.css; mirror into theme.json palette so native blocks inherit):
  --cream #FAF7F1  --ink #1B1A17  --gold #9C7A3C  --terracotta #C2563A (accent only)
  --sage #7A8F6A   --border #D9D2C4  --muted #6B6457  --radius 0.25rem
  theater dark: #14130F / #211F19 / #2C2A22 ; theater line rgba(242,236,222,.14)
  Fonts HE: "Frank Ruhl Libre" (serif headings) + "Heebo" (sans body)
        EN: "Fraunces" (serif headings) + "Inter Tight" (sans body)  [self-host woff2 in prod]
  Type: display clamp(2.25→4rem)/h1 clamp(1.875→3)/h2 clamp(1.5→2.25)/h3 clamp(1.25→1.625)/body 1rem
  Line-height tight 1.15 / snug 1.35 / normal 1.55 / loose 1.75
  Shadow (ONE family): card 0 8px 24px -12px rgba(27,26,23,.18) ; theater 0 40px 90px -30px rgba(20,19,15,.55)
  Space (8pt): 4 8 12 16 20 24 32 40 48 64 80 96

COMPONENT RULES:
  - Buttons: primary = ink bg / cream text; accent = terracotta (CTAs only); ghost = border. min 46px.
  - One soft shadow family only. Hairline borders (--border). Generous whitespace. Radius 0.25rem.
  - Motion only on interaction (hover lift, panel slide, cinematic select). Respect prefers-reduced-motion.
  - The DARK 3D theater is the ONE dramatic surface on an otherwise cream page. Don't make the whole
    page dark; don't make the theater cream. Contrast IS the design.
  - NO: aggressive gradients, emoji, rounded-corner+left-accent "AI card", Inter/Roboto everywhere,
    em-dashes, invented stats. (These are AI-slop tells and are banned.)

MAP (block 7, the "full world"): Mapbox GL when `nadlan_mapbox_token` option is set (the bridge
  already enqueues it conditionally). Center on the project geo; pins for transport/schools/beach/
  Reading/nearby-projects from the area record. Fallback: the stylized SVG map already in the engine.
  Provide real area data (pins/stats/spokes) — see the handoff data.js AREAS.sde-dov (copy into PHP).

═══════════════════════════════════════════════════════════════════════════════════════
PART H — SEO ARCHITECTURE (this is a real-estate SEO product, not a 3D demo)
═══════════════════════════════════════════════════════════════════════════════════════

- Real-estate-first language everywhere. Titles/H1/meta are about buying apartments in the area, never
  about "3D models". (The live EN title "Ashira Sde Dov apartments for sale in Tel Aviv" is correct —
  keep that framing.) NEVER expose internal words (GLB/BIM/SVG/polygon/hotspot/mesh/token/Featured/
  Sponsored/Lovable/Codex) on any buyer surface.
- Each language = its own crawlable URL + hreflang (PART E). No language is a dead button.
- Per-project: JSON-LD (Residence/Apartment + FAQ + BreadcrumbList), the styled SEO article (1,500+
  words, source-cited), the FAQ accordion, the comps section (fresh data = freshness signal).
- The CATALOG `/projects/` and AREA hubs interlink projects ↔ areas ↔ tools (internal link equity).
- IndexNow ping on publish (already wired). Keep <lastmod> fresh via the daily comps refresh.
- Core Web Vitals: poster-until-paint (no CLS/blank), lazy model-viewer, one GLB+poster per project
  (~100-200KB), self-hosted fonts. The dark theater must not block first paint.

═══════════════════════════════════════════════════════════════════════════════════════
PART I — RESEARCH CONCLUSIONS (Compass / Zillow / Homes.com → what to adopt)
═══════════════════════════════════════════════════════════════════════════════════════

From Zillow's biggest property-page redesign: a sectioned, single-scroll layout with named sections
("What's Special / Market Value / Monthly Cost / Neighborhood") that users click into, and a
media-first top that expands to a magazine-style gallery. → ADOPT: PART D-2 section order + C-3 nav
+ media-first hero. <cite index="9-8,9-12,9-13">Zillow's redesign presents home details in sections like "What's Special," "Market Value," "Monthly Cost" and "Neighborhood," in a wider single-scroll format, with a media section at the top showcasing photos and 3D tours.</cite>

From Zillow's Zestimate: a value estimate PLUS an estimated sales RANGE, built from comps + public
records, updated multiple times a week, explicitly "not an appraisal." → ADOPT: PART F-1 estimate+range,
honest + dated + non-binding. <cite index="5-16,5-25">In addition to a single value, Zillow provides an estimated sales range, and Zestimates for most homes update multiple times per week.</cite> Comps method: 3-5 similar recently-sold properties, same beds/baths/sqm, within ~1 mile, last 3-6 months. <cite index="11-2,11-3,11-4">Comps include homes sold in the past three to six months, pulled from the same neighborhood in close proximity — in an urban area usually within a mile or so.</cite> → ADOPT: PART F-2 comps section.

From Compass: save/share/collaborate Collections with real-time price+status updates; Similar Homes +
personalized recommendations drove large engagement lift; property history; a layout reviewers call
cleaner than Zillow. → ADOPT: favorites/compare (already built) + "nearby/similar projects" + price/
status freshness. <cite index="13-1">Compass buyers can browse and share favorite listings, with the platform providing real-time status and price updates.</cite> <cite index="18-3">Compass reported a 153% increase in homepage clickthrough and a 107% increase in engagement actions (sharing, saving, contacting) from Similar Homes and personalized recommendations.</cite>

NadLan's MOAT beyond all three: the interactive 3D building + apartment selector as the conversion
moment, on top of a real SEO content engine and the local data (gov/Madlan). That combination is what
makes contractors pay. Keep it honest (illustrative until real BIM) and it differentiates.

═══════════════════════════════════════════════════════════════════════════════════════
PART J — ACCEPTANCE CRITERIA (a release is DONE only when ALL pass, with screenshots)
═══════════════════════════════════════════════════════════════════════════════════════
□ Exactly ONE showroom on the project page (`.nlv2-showroom` count = 0; `#nl-root` count = 1).
□ Article is styled (cream/gold), not default theme type.
□ `/projects/ashira-sde-dov-en/` loads in English; switching to HE navigates to the HE sibling and
  loads RTL Hebrew; FR/RU/AR likewise (or the button is hidden if that sibling doesn't exist).
□ view-source shows 5 hreflang + x-default, self-referencing, only for existing published siblings.
□ The 3D building paints (poster-until-paint, no blank flash); hotspots sit ON the building; clicking
  opens the slide-out with the unit; camera frames the unit; never seen from underneath.
□ Price shows a RANGE + "אומדן לא מחייב" + date; comps section shows 3-5 real nearby deals (or
  collapses cleanly if none).
□ Map renders (Mapbox if token set, else stylized) with real area pins.
□ No internal words on any buyer surface; no em-dashes; no invented single price.
□ Screenshots attached: desktop 1440 + mobile 390, HE + EN, for the project page AND the catalog.
□ Healthcheck version bumped; ZIP + manifest aligned; PR shows `git show --stat` file list on main.

END OF MASTER SPEC.
