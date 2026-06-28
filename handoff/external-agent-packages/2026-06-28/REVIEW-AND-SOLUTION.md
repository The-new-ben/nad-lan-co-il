# External agent packages — review, verdict, and the solution (2026-06-28)

Two outside agents (OpenAI/Codex sandbox) delivered showroom packages. This folder
archives all of them verbatim (zips + mockup + QA + the Ashira spec PDF) so nothing is
ever lost again. This file records the honest verdict on each and the agreed solution.

## What is archived here
- `Ashira_Target_Mockup.dc.html` + `../../claude-design/2026-06-28-mockup/` — the VISUAL TARGET (NADLAN brand, dark theater, price+comps, clean map, styled article, inquiry). This is the contract the live page must match.
- `NadLan_Ashira_Factory_Run*.zip` — the 2026-06-27 design pack + factory bundle (engine, models, screenshots).
- `nadlan-rescue-showroom-theme.zip` + `nadlan-rescue-qa.zip` — a standalone THEME (rejected, see below).
- `nadlan-content-showroom-bridge.zip` + `-qa.zip` — a second PLUGIN bridge (rejected as-is, see below).
- `Ashira-spec.pdf` — the Ashira reference document.

## Verdict 1 — Rescue THEME: DO NOT ACTIVATE
A standalone theme that REPLACES the active `nadlan-revenue` theme. Activating it would erase
the calculator hub, the 2,711-professional directory, billing/monetization, and all SEO
machinery. It renders only 3 demo projects from a bundled `data.js` (its own note says
"CMS-ready, not CMS-wired"); it does not read the 282 real `nadlan_project` posts or the real
5-language article. It also re-ships the blunt `<main class="nlv2-showroom">` strip that ate the
article (fixed live in 1.69.54). Directly violates the spec boundary "do not rebuild from scratch."
Use only as a visual reference on staging.

## Verdict 2 — Content Showroom BRIDGE plugin: RIGHT DIRECTION, DO NOT RUN ALONGSIDE nadlan-config
A plugin overlay (not a theme) — correct architecture, but it is a parallel re-implementation of
what `nadlan-config` already does live, and it COLLIDES:
- Registers the same shortcode `nadlan_showroom_engine` (override conflict).
- Hooks `the_content` to inject a showroom on project pages (nadlan-config already does at pri 8) -> two showrooms = stacking returns.
- Emits its own `wp_head` hreflang (nadlan-config already does) -> duplicate hreflang.
- Wraps the article in the same `.nadlan-project-article .nadlan-guide` class.
- Re-ships the blunt legacy strip (the 1.69.54 article-eating bug).
- Falls back to Ashira/Rainbow/Dimri demo data when meta is missing.
Running it next to `nadlan-config` = the exact stacking we removed. Do not activate.
Salvageable, additive ideas to port surgically into `nadlan-config`: the SVG floor-plan assets,
the `[nadlan_seo_booster]` concept, and a homepage gallery band.

## Verdict 3 — Platform package (child theme + orchestrator plugin): CORRECT ARCHITECTURE, STAGING-FIRST
The third delivery (`nadlan-platform-child-theme.zip`, `nadlan-platform-orchestrator-plugin.zip`,
`nadlan-complete-platform-solution.zip`) is the first one built the right way. Audit findings:
- **Child theme** declares `Template: nadlan-revenue` (a real child, does not replace the parent);
  `functions.php` only adds a body_class (non-destructive); `single-nadlan_project.html` uses
  `wp:post-content` (so the engine's the_content injection still fires once — no baked showroom).
- **Orchestrator plugin** is anti-stack-safe: shortcodes are namespaced `nadlan_platform_*` (no
  `nadlan_showroom_engine` collision); `[nadlan_platform_showroom]` DELEGATES to the existing
  `nadlan_showroom_engine_shortcode()`; its only `the_content` filter targets `is_front_page()`
  ONLY, is OFF by default (`nlpo_auto_insert_home_band`), and has a dedup guard; REST is a
  separate `nadlan-platform/v1` admin content-gap route; it emits NO hreflang (no dup).
- Ships 5-language Ashira content drafts + a rollout/QA plan.

ANTI-STACK: at the plugin level this is clean and complementary — it does not duplicate the engine,
the shortcode, or hreflang. The remaining risk is presentation-only and unavoidable: the child
theme's `theme.json` (site-wide colors/typography/spacing) and template overrides (`home.html`,
`archive-nadlan_project.html`, `single-nadlan_project.html`) change the look of the WHOLE site, so
they MUST be visually verified on STAGING against the real hub, calculators, directory, and a lead
flow before going live. Activate the orchestrator first (home band off), then the child theme on
staging, screenshot everything, and only then consider live. This package and finishing the engine
(PR4/PR5) are complementary, not alternatives.

## THE SOLUTION (how the mockup gets onto the live site)
The vehicle already exists and is live, de-stacked, and CMS-wired: the showroom engine inside
`nadlan-config` (`inc/showroom-engine.php` + `assets/showroom-engine/`). Both outside packages
reinvented it. We do NOT add a third/fourth engine. We finish the engine to match the mockup,
against real data, one clean release at a time:

1. PR4 — sticky in-page section nav under the hero (spec C-3).
2. PR5 — price estimate RANGE + comps table + the clean neighborhood map (spec F-1/F-2/G-map),
   reading real meta / a cached comps endpoint; Mapbox when the token is set, stylized otherwise.
3. Adopt the mockup's exact CSS/section styling into `showroom.css`/`editorial.css` so the live
   render matches `Ashira_Target_Mockup.dc.html` pixel-for-intent.
4. Port the salvageable bridge assets (SVG floor plans, seo booster) additively.

Every release: one concern, all version surfaces bumped together, ZIP+manifest verified, and an
anti-stack scan (`#nl-root`=1, `.nlv2-showroom`=0, no second engine/hreflang) before and after.

Blocking inputs that only the owner can provide: Mapbox token, WhatsApp number, real Avisror BIM
(for a true model), and real photos (to replace concept images, labelled "הדמיה להמחשה").
