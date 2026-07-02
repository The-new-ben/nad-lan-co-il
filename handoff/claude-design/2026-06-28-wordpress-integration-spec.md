# NadLan Showroom — WordPress Integration Spec & Honest Diagnosis
Date: 2026-06-28 · Author: Claude Design · Audience: owner + Claude Code
Repo: The-new-ben/nad-lan-co-il · Live ref: /projects/ashira-sde-dov-en/

This document answers four things, in order:
1. Is the design I made actually possible on WordPress? (yes — and most of the wiring is already correct)
2. Why does the live page look bad? (precise root cause)
3. Exactly how to fix it — file by file, with code and tokens.
4. What I can do inside the repo vs what only you / Claude Code can do.

---

## 1. HONEST DIAGNOSIS — why the live page is not contractor-ready

The problem is **NOT** that the design can't be built on WordPress. It already IS built and wired
into the plugin correctly. The problem is **STACKING** — the exact failure mode the owner has warned
about repeatedly. Three generations of the project page are now layered on the same URL:

**Generation 1 — `inc/project-3d.php`** (+ `assets/css/project-3d-premium.css`, 20 KB)
The original showroom. Gated by the `nadlan_p3d_enabled` filter.

**Generation 2 — a STATIC "nlv2" showroom + SEO article baked into the post body**
The live EN page renders hand-written HTML with IDs like `nlv2-ashira-selector-en`,
`nlv2-ashira-info-en`, a flat hero `<img src=…ashira-hero-concept.jpg>`, static facade cells
(`18W Sea`, `14C City`…), an apartment card, a contact form, then a ~3,000-word SEO article.
This lives in `wp_posts.post_content` (the same mechanism `project-page-assembly.php` uses to inject
the Rainbow `nadlan-rainbow-seo-v1610` block). It renders in DEFAULT theme typography — flat text on
white — because its classes (`nadlan-guide*`, `nlv2-*`) are not styled by the engine CSS.

**Generation 3 — `inc/showroom-engine.php`** (my engine, Claude Code's port — this part is GOOD)
Prepends my live engine (`<div id="nl-root">`) ABOVE `the_content` at priority 8 for the Ashira
slugs, enqueues `tokens.css` + `showroom.css` + `model-viewer` + `i18n.js` + `engine.js`, injects
`window.NADLAN_SHOWROOM` from CMS meta, and disables Gen-1 via the filter. The bridge is written
correctly.

### The result in a browser
The page paints, top to bottom:
1. (Gen 3) my live dark-theater engine — IF its JS executes cleanly, and
2. (Gen 2) a SECOND, static, flat copy of the same showroom, then
3. (Gen 2) a long article in unstyled default type.

So a contractor sees the showroom **twice** — once cinematic, once flat — followed by a wall of
text. Even where my engine paints perfectly, it is buried in a duplicate + an unstyled article. That
is why it "cannot be shown to contractors." **Gen 3 was added on top of Gen 2 instead of replacing
it.** Classic stack.

### Confidence labels (so you know what I verified vs inferred)
- VERIFIED (read the code): the engine is ported + enqueued + payload-wired in `showroom-engine.php`;
  it prepends `#nl-root` and disables `project-3d`.
- VERIFIED (fetched live HTML): the EN page outputs static `nlv2-*` markup + a full SEO article from
  the post body, using `ashira-*-concept.jpg` flat images, not my GLB.
- HIGH-CONFIDENCE INFERENCE: that static block sits in `post_content`, so it renders below my engine
  = duplication. (I can read the repo, not your live DB, so I can't print the exact row — but the
  live output + the Rainbow seeding pattern make this certain.)
- CANNOT VERIFY from here: whether my engine's JS also throws on the live page (I can't run a real
  browser against the live server). The fix below makes the page correct in BOTH cases.

---

## 2. IS IT POSSIBLE ON WORDPRESS? — yes, unambiguously

Everything I designed runs on WordPress with no compromise:
- The dark 3D theater is `<model-viewer>` (a web component) reading a `.glb` URL from a CMS field.
  Already working in the bridge; the GLB is seeded into `project_model_glb`.
- The cinematic select, slide-out panel, facade backup, inventory, compare, favourites, deep-links,
  sticky inquiry, language switch — all vanilla JS in `engine.js`, already enqueued.
- The lead form already posts to the real `/wp-json/nadlan/v1/lead` route.
- The "complete world" map is `<div id>` + Mapbox GL when `nadlan_mapbox_token` is set (the bridge
  already conditionally enqueues `mapbox-gl` + `mapbox-init.js`); otherwise the stylized SVG map.

The feasibility question is settled. What remains is **de-stacking, styling the article, filling the
area data, and wiring the homepage**. All of that is code I can write into the repo.

---

## 3. THE FIX — file by file, exact

### 4A. DE-STACK: remove the Gen-2 static showroom from the Ashira post bodies  ⚠ destructive to DB content — run with approval
The static `nlv2` showroom must come OUT of `post_content` so only my engine (Gen 3) renders the
showroom. KEEP the SEO article — it is good and it is the SEO asset — but strip the duplicated
interactive showroom block that precedes it.

One-shot migration (new file `inc/showroom-destack.php`, add `'showroom-destack'` to the module
loop in `nadlan-config.php`):

```php
<?php
if ( ! defined( 'ABSPATH' ) ) { exit; }
/**
 * One-shot: strip the legacy static "nlv2" showroom block from project post bodies.
 * The live engine (#nl-root, prepended by showroom-engine.php) is now the ONLY showroom.
 * The SEO article (everything from the first <h2>/nadlan-guide onward) is preserved.
 * Reversible: a backup of the original body is saved to post meta before edit.
 */
add_action( 'init', function () {
	if ( get_option( 'nadlan_destack_nlv2_v1' ) === '1' ) { return; }
	$slugs = array(
		'ashira-sde-dov','ashira-sde-dov-en','ashira-sde-dov-fr','ashira-sde-dov-ru','ashira-sde-dov-ar',
	);
	foreach ( $slugs as $slug ) {
		$p = get_page_by_path( $slug, OBJECT, 'nadlan_project' );
		if ( ! $p ) { continue; }
		$body = (string) $p->post_content;
		// Match the legacy block: from a known nlv2 marker to the start of the SEO article.
		// Adjust the END anchor to your article's first heading wrapper.
		$start = strpos( $body, 'nlv2-' );                 // first nlv2 id
		$artic = strpos( $body, 'nadlan-guide' );          // SEO article wrapper (kept)
		if ( $start !== false && $artic !== false && $artic > $start ) {
			update_post_meta( $p->ID, '_nadlan_body_backup_predestack', $body ); // reversible
			$kept = substr( $body, $artic );
			// re-open the wrapper element the offset cut into, if needed:
			$kept = '<section class="nadlan-project-article nadlan-guide" dir="'
			      . ( in_array( $slug, array('ashira-sde-dov','ashira-sde-dov-ar'), true ) ? 'rtl' : 'ltr' )
			      . '">' . $kept;
			wp_update_post( array( 'ID' => $p->ID, 'post_content' => $kept ) );
		}
	}
	update_option( 'nadlan_destack_nlv2_v1', '1' );
}, 40 );
```

> The exact `$start`/`$artic` anchors must be confirmed against the real stored body (Claude Code can
> `wp post get <id> --field=content` first). The backup meta makes it safe to re-run/revert.

### 4B. Guarantee the engine PAINTS (no blank flash, correct order)
`showroom-engine.php` already enqueues in the right order and injects the payload `before` engine.js.
Three hardening checks:
1. `engine.js` is enqueued with `i18n` as a dependency, and `data` is the inline payload `before`
   engine — VERIFIED correct. Ensure `engine.js` is registered with `array('nadlan-engine-i18n')`
   (it is) so i18n is parsed first.
2. The poster-until-paint guard in `engine.js` (`#nl-poster` fades on model-viewer `load`) means the
   building image shows immediately and the live 3D replaces it — no blank flash. KEEP.
3. model-viewer must load as a module: `wp_script_add_data('nadlan-model-viewer','type','module')` —
   VERIFIED present.

### 4C. STYLE the SEO article in the token system  (file delivered: engine/editorial.css)
The article currently uses default theme type. Enqueue `editorial.css` (in this handoff) on single
project pages so the existing `.nadlan-guide*` markup becomes a designed magazine section in
cream/gold. In `showroom-engine.php`, in the shortcode enqueue block, add:

```php
wp_enqueue_style( 'nadlan-engine-editorial', $base . 'editorial.css',
	array( 'nadlan-engine-tokens' ), '1.69.51' );
```
Copy `editorial.css` to `plugins/nadlan-config/assets/showroom-engine/editorial.css`. It is scoped to
`.entry-content .nadlan-guide` + `.nadlan-project-article`, so it cannot leak into tools or directory.

### 4D. BLOCK 8 — give the map + spokes real data (currently empty → collapses)
In `showroom-engine.php`, `nadlan_showroom_engine_shortcode()` builds `areas[...]` with
`pins => array()`, `spoke_groups => array()`, `stats => array()`. That is why the "complete world"
shows only an empty map. Wire it from area taxonomy / a shared spokes option. Minimum viable: ship a
real Sde-Dov area record (the one in this handoff's `engine/data.js` AREAS.`sde-dov`) as a PHP array
and attach it to any project whose `area` resolves to Sde Dov:

```php
function nadlan_showroom_engine_area_sde_dov( $geo ) {
	return array(
		'label_key' => 'area_sde_dov', 'blurb_key' => 'area_sde_dov_blurb',
		'map' => array(
			'center' => $geo, 'zoom' => 14,
			'bbox' => array('w'=>34.766,'s'=>32.092,'e'=>34.802,'n'=>32.116),
			'coast_x' => 16, 'project_pin' => array('x'=>33,'y'=>50),
			'pins' => array(
				array('ref'=>'reading-tower','x'=>24,'y'=>82),
				array('ref'=>'tlv-beach','x'=>11,'y'=>34),
				array('ref'=>'light-rail-green','x'=>58,'y'=>60),
				array('ref'=>'yarkon-park','x'=>70,'y'=>80),
				array('ref'=>'sde-dov-school','x'=>62,'y'=>30),
				array('ref'=>'commercial-hub','x'=>52,'y'=>42),
			),
		),
		'stats' => array(
			array('id'=>'plan','value'=>'TA/4444','label_key'=>'stat_plan'),
			array('id'=>'units','value'=>'16,000','label_key'=>'stat_units'),
			array('id'=>'dunams','value'=>'1,300','label_key'=>'stat_dunams'),
			array('id'=>'residents','value'=>'40,000','label_key'=>'stat_residents'),
		),
		'spoke_groups' => array(
			array('id'=>'transport','icon'=>'train','label_key'=>'spoke_transport','items'=>array('light-rail-green','ayalon-access')),
			array('id'=>'education','icon'=>'school','label_key'=>'spoke_education','items'=>array('sde-dov-school')),
			array('id'=>'facilities','icon'=>'store','label_key'=>'spoke_facilities','items'=>array('tlv-beach','yarkon-park','commercial-hub')),
			array('id'=>'anchor','icon'=>'landmark','label_key'=>'spoke_anchor','items'=>array('reading-tower')),
		),
	);
}
```
…and include the matching `spokes => array(...)` map (copy SPOKES from `engine/data.js`). The engine
already renders all of this; it just needs non-empty arrays. The stats are public Sde-Dov figures the
owner should verify before publish.

### 4E. HOMEPAGE — wire the gallery (the project catalog is its own SEO surface)
The homepage should NOT be the showroom. It is the real-estate hub (it already is — nav, tools,
neighborhoods, professionals, glossary). Add the project gallery as ONE band on it via the existing
shortcode: `[nadlan_showroom_engine page="home"]` in a homepage section, OR call the gallery builder
in `inc/homepage.php`. The engine's `data-page="home"` renders the cream card grid (poster, name,
tagline, unit count, "enter project"). Featured/paid projects already sort first (monetization).

### 4F. MULTILINGUAL / hreflang — keep it inert until all pages exist
Per the gate doc: one page per language under `/projects/`, no plugin. The reciprocal hreflang set is
emitted server-side once every language page is published + QA'd. The pages already exist as separate
posts (`ashira-sde-dov-en/-fr/-ru/-ar`). Wire `wpseo` alternate hooks (or a `wp_head` emitter) to
print the 5 + x-default set from a publication manifest. Do NOT client-switch for SEO — each language
is its own crawlable URL (the engine's language bar is for UX only).

---

## 5. TOKENS — the locked reference (every value the design uses)
```
--cream #FAF7F1   --ink #1B1A17   --gold #9C7A3C   --terracotta #C2563A (accent only)
--sage #7A8F6A    --border #D9D2C4 --muted #6B6457  --radius 0.25rem
theater: #14130F / #211F19 / #2C2A22 (dark stage), line rgba(242,236,222,.14)
Fonts HE: Frank Ruhl Libre (serif) + Heebo (sans)    EN: Fraunces (serif) + Inter Tight (sans)
Type: display clamp(2.25→4rem) · h1 clamp(1.875→3) · h2 clamp(1.5→2.25) · body 1rem/1.55
Shadow (one family): card 0 8px 24px -12px rgba(27,26,23,.18) · theater 0 40px 90px -30px rgba(20,19,15,.55)
Space (8pt): 4 8 12 16 20 24 32 40 48 64 80 96
```
Production: self-host the four font families as woff2 in the theme and drop the Google `@import` in
`tokens.css` (prototype convenience only). `theme.json` should mirror cream/ink/gold/terracotta/sage
as palette slots so the block editor and any native blocks inherit the same colors.

---

## 6. THE BIGGER PICTURE — this is an SEO real-estate site first (you're right)
The live site is ALREADY structured like a real-estate authority: buying/selling/investment guides,
mortgage + tax + valuation calculators, a 2,711-strong professionals index, a glossary, neighborhood
hubs (Sde Dov, Ramat Aviv, Bat Yam, Herzliya), urban-renewal. That is the Zillow/Compass/Homes.com
content surface, and it is good. The showroom is ONE buying-experience module inside it, not the
product. So the strategy is sound. What drags the perceived quality down is purely that the flagship
project page (the thing a contractor judges) is currently the stacked mess in §1.

To out-compete on real estate SEO, the project page must do three jobs at once, and the design already
supports all three — they just need the de-stack:
1. RANK: the SEO article (kept), FAQ schema, source citations, per-language pages, district facts.
2. CONVERT: the cinematic showroom + unit-level inquiry (the moat that makes contractors pay).
3. CONNECT: block 8 — map, transport, schools, beach, nearby projects — the "full world" like Compass.

Every project becomes a self-contained world: the building (3D), the units (inventory + facade), the
area (map + spokes + stats), the money (inquiry + WhatsApp), the SEO (article + FAQ + sources). One
engine, every project inherits it.

---

## 7. WHAT I CAN DO IN THE REPO vs WHAT ONLY YOU CAN DO
**I can (write into the repo, ready for Claude Code to commit + you to deploy):**
- `editorial.css` — DONE (this handoff).
- The de-stack migration (§4A), the area/spokes data (§4D), the editorial enqueue line (§4C), the
  homepage gallery wiring (§4E) — as PHP files / patches in the handoff.
- Refinements to `engine.js` / `showroom.css` (already in the plugin) for any visual gap you point to.
- Regenerate / improve the GLB + poster + facade assets.

**Only you / Claude Code can (server + DB, not in the repo):**
- Run the migrations (they execute on the live DB; I can only write them).
- Set `nadlan_mapbox_token` + `nadlan_whatsapp_e164` options (turns on the real map + WhatsApp).
- Verify the stored post body anchors for §4A, then commit + deploy + activate.
- Confirm in a real browser on the live host (I can't reach your server with a JS-running browser).

**Bottom line:** the design is fully achievable on WordPress and ~80% wired already. The reason it
looks bad is one specific, fixable thing — the Gen-2 static showroom was never removed when my engine
was added. De-stack it, style the article with `editorial.css`, fill block 8, wire the homepage band,
and the page becomes the contractor-grade experience in the screenshots. I can write every one of
those changes into the repo; deploying + the two option values + running the migration are yours.
