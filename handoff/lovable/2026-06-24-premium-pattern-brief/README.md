# Brief for Lovable — critical premium audit + one replicable showroom pattern

> Owner ask (2026-06-24): a very critical, very detailed examination of the live
> site, then a new plan with examples, code, and rationale (why / why not), down to
> the small details (fonts, favicon, branding). Produce ONE canonical picture of how
> the Rainbow showroom should look, as a PATTERN that replicates to every project,
> not a one-off. Add premium polish. The current site does not feel premium and the
> favicon is wrong.

## 0. What this is, and what it is not

This is a design and product specification task. Lovable reviews and specifies.
Lovable does **not** run, build, or deploy WordPress. The WordPress repo
(`The-new-ben/nad-lan-co-il`) is the source of truth for code. Implementation is
Codex's job, from your spec. Your output is a spec packet plus one canonical
mockup, written so Codex can build it to the pixel.

## 1. The standard we are holding to (cited, so it is not opinion)

- **"Quiet luxury," not loud.** Warm, muted, editorial; the page should read like a
  high-end architecture or fashion publication, not a listings board. Earthy palette,
  generous whitespace, restraint. (Vide Infra, *Luxury Real Estate Website Design
  Principles*; DMR Media, *2026 Luxury Real Estate Design Trends*.)
- **Immediate path to action in the hero.** A luxury buyer should be able to act in
  one click without scrolling: see the building, find an apartment, inquire. (Baymard
  Institute, *Luxury Goods Ecommerce UX*, 200,000+ research hours, 400+ guidelines;
  used by 71% of Fortune 500 ecommerce.)
- **The showroom IS the page.** Single-property luxury sites lead with the building
  and the availability, then support with editorial. (One57.com / Billionaires Row
  single-property benchmark.)
- **3D must guide the eye.** Hotspots immediately signal interactivity but must not
  overcrowd; surface-anchored picks beat scattered pins. Use model-viewer's
  `surfaceFromPoint` + `data-surface` so a pick travels with the mesh. (model-viewer
  docs; Vectary, *Hotspot alternatives for configurators*; The Digital Bunch,
  *Designing a 3D configurator that makes sense*.)
- **Build a system, not a page.** One token set, one component library, replicated
  across every project. Atoms → molecules → organisms → template → page, with design
  tokens as the single source. (Brad Frost, *Atomic Design*; *Design Tokens* course.)
- **Hebrew luxury type is its own craft.** RTL is not a flipped LTR layout; the
  Hebrew face carries the premium feel. Specify the exact Hebrew family, weights, and
  RTL logical-property rules. (Yanek Iontef / Fontef foundry, Hebrew type for Google,
  Typotheque, Commercial Type.)
- **Visualization benchmark.** The bar for "premium 3D building" is studios like The
  Boundary and Hayes Davidson (The Shard, Billionaires Row). We will not match their
  budget, but the lighting, calm camera, and material restraint are the reference.
- **Accessibility signals professionalism.** WCAG AA contrast, keyboard, focus
  states; a sophisticated audience reads sloppiness as cheapness. (Baymard; ALM Corp
  *2026 audit checklist*.)

## 2. What we need Lovable to deliver (definition of done)

A single packet under `handoff/lovable/2026-06-24-premium-pattern/` in YOUR repo:

1. **Critical audit of the live site** (`https://nad-lan.co.il`, the Rainbow project
   page, the `/projects/` archive, the homepage). Go small: fonts actually loading vs
   falling back, the favicon, the social card, spacing rhythm, color contrast, mobile
   390 behavior, the showroom hero, the apartment-pick affordance, public-language
   leaks. For each issue: what is wrong, why it reads cheap, the fix, and a code
   snippet (CSS custom properties / HTML / model-viewer attributes), and explicitly
   why NOT to do the tempting-but-wrong alternative.
2. **ONE canonical showroom mockup** — a single rendered picture of how the Rainbow
   showroom should look at desktop and at 390 mobile, on the cream system. This is the
   PATTERN. Annotate it with the token names and component names so it maps 1:1 to
   build.
3. **The replication rule.** State, in one page, how this exact pattern is applied to
   any project (Dimri, urban-renewal, the next 50) by filling fields only: which
   parts are fixed system, which are per-project content. A new project should reach
   "premium" by data entry, zero new design.
4. **Branding + favicon.** A proper mark that works as favicon, app icon, and social
   card. Specify the exact files, sizes, and the OG/Twitter card. The current favicon
   is rejected.
5. **The apartment-selection product decision.** The live build selects 6 authored
   units plus a nearest-tap surface fallback; it is NOT true per-window BIM picking.
   Tell us whether the right premium answer is (a) keep authored units but make the
   affordance unmistakable, or (b) require real per-unit GLB/BIM geometry, and what
   that costs the owner to supply. Do not paper over the gap.
6. **Premium uplift list.** The specific touches that move it from "fine" to
   "expensive": hero treatment, type scale, one shadow, hairlines, micro-interaction
   on hover, the inquiry moment. Each with a reason and a code example.

## 3. The hard rules your spec must respect (so Codex can actually ship it)

- **No stacking.** Replace at the source. Never specify a cream layer painted over a
  dark one. The WordPress showroom is one CSS source: `nadlan_p3d_lovable_showroom_v1690_css()`.
- **Vanilla only for the WordPress showroom.** No React, no Tailwind, no shadcn in the
  spec's implementation notes. Plain CSS custom properties and DOM. Your TanStack
  prototype is visual reference, not shippable code (your own §5 perf budget).
- **No public-language leaks.** Nothing buyer-facing may contain internal terms
  (GLB, SVG, BIM, hotspot, Featured, Sponsored, React, Tailwind, Lovable, Codex,
  token names). Those live only in the spec, never in rendered copy.
- **Hebrew first, RTL correct.** Logical properties, `text-align:start`, the right
  Hebrew family with self-hosted woff2. Latin tokens inside Hebrew wrapped so numbers
  and brand do not flip.
- **No em dashes, no AI tells** in any copy you propose.
- **Proof or it did not happen.** Real screenshots at 1280 and 390, HE and EN. No
  duplicated or reused images.

## 4. Two things to answer before you start the work

1. **Credit estimate.** Tell the owner how many Lovable credits this full audit +
   canonical mockup + replication spec + branding will consume, before you run it, so
   he approves with eyes open.
2. **Scope confirmation.** Confirm you will deliver the pattern as a replicable system
   for all projects, not a Rainbow-only redesign.

## 5. Where the materials go and who builds

- Your spec packet: your repo, `handoff/lovable/2026-06-24-premium-pattern/`.
- Implementation: Codex, into the WordPress repo, one small PR per piece, off latest
  main, guarded ZIP, verifier, real screenshots, PR ready-for-review. Codex does not
  merge his own PRs.
- Source of truth for live behavior and current code: the WordPress repo, live
  version 1.69.32.

## 6. Sources cited above (people and institutions, verifiable)

- Baymard Institute, *Luxury Goods Ecommerce UX Research* — https://baymard.com/research/luxury-goods
- Brad Frost, *Atomic Design* — https://atomicdesign.bradfrost.com/ ; *Design Tokens* — https://designtokenscourse.com/
- Vide Infra, *Luxury Real Estate Website Design: Principles, Strategy, Best Practices* — https://videinfra.com/blog/luxury-real-estate-website-design-principles-strategy-and-best-practices
- DMR Media, *7 Luxury Real Estate Website Design Trends 2026* — https://www.dmrmedia.org/blog/Real-Estate-Website-Design-Trends
- model-viewer documentation (surfaceFromPoint, data-surface hotspots) — https://modelviewer.dev/docs/
- Vectary, *5 tips on hotspot alternatives* — https://www.vectary.com/3d-modeling-blog/5-tips-for-hotspots-alternatives/
- The Digital Bunch, *How to UX/UI Design a 3D Configurator That Makes Sense* — https://www.thedigitalbunch.com/blog/how-to-uxui-design-a-3d-configurator-that-makes-sense
- The Boundary — https://www.the-boundary.com/ ; Hayes Davidson — https://www.hayesdavidson.com/
- One57 single-property benchmark — https://one57.com/
- Yanek Iontef / Fontef (Hebrew type) — https://fontwerk.com/en/designers/yanek-iontef
- ALM Corp, *2026 Website Audit Checklist* — https://almcorp.com/blog/website-audit-checklist/
