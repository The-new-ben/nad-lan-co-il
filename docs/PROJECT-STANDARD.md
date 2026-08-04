# THE PROJECT STANDARD - what every nad-lan project page must have

Written 2026-08-03 per the owner's order: "I throw a name of a project and an
agent builds it from A to Z, everyone has the same standards." This document IS
the standard. The factory pipeline (owner's content agent gathers, Claude
assembles and QAs, owner deploys) executes against this checklist. UTOPIA and
the ashira theater are the two source templates; the standard is their UNION.
The additive law applies: no project ever loses a feature to "match" another.

## A. Content (the UTOPIA bar)

- [ ] 3,000+ article words in Hebrew. Structure: סקירה, מיקום וסביבה, הבניינים
      והדירות, מחירים ואומדנים, היזם, שלבי הפרויקט, למי זה מתאים, שאלות נפוצות,
      מקורות.
- [ ] Real sources cited at the bottom (developer site, plan documents, press).
      No invented facts, no invented numbers. Estimates marked as estimates.
- [ ] City-plan and developer-drawing references where they exist (UTOPIA has
      them; every project should).
- [ ] FAQ section structured as H3 question + paragraph answer (feeds FAQPage
      schema automatically).
- [ ] Zero em/en dashes. No AI-tell phrasing.
- [ ] The non-affiliation notice present and naming the actual developer.

## B. 3D and visual (the theater bar)

- [ ] A facade image (plate) stamped "הדמיה להמחשה בלבד" where it is a render.
- [ ] Selectable apartments ON the model where a GLB exists: hotspots with
      status colours (available / reserved / sold), unit panel with plan view.
- [ ] Window view where available, exposed as a visible button.
- [ ] Feature bar present (in-flow, never floating).
- [ ] GLB is metre-scaled, logged in INVENTORY, never silently deleted.

## C. Data integrity

- [ ] lat/lng at PLOT precision, verified against an official source (developer
      site, govmap, city GIS, plan plot number). Never a copied placeholder.
      Duplicated coordinates across projects = automatic audit failure.
- [ ] earth_heading / earth_scale / earth_alt set when the project has a GLB
      (so the Google Earth scene plants it correctly).
- [ ] Claimed neighborhood matches reverse-geocoded location.
- [ ] Unit counts, floors, delivery dates match the cited source.

## D. Languages

- [ ] Variants as separate posts, slug exactly `<base>-<lang>` (en, fr, ru, ar).
      The platform auto-wires language context, hreflang cluster and chrome
      retranslation from the slug alone. No manual canonicals, no manual
      hreflang.
- [ ] Translation follows the UTOPIA method: per-language search-intent research
      first, the leading phrase as it appears on Google goes into the title and
      H1. Not a straight translation.
- [ ] Brand and project names stay Latin. Numbers and facts identical to the
      Hebrew original.

## E. Lead surfaces and legal

- [ ] Contact points carry the correct notice: independent-site disclaimer when
      the developer is not a client (wording pending owner approval, tracked in
      the session board), partner label when they are.
- [ ] Lead forms carry the privacy notice (the biggest quantified exposure -
      see nadlan-lead-privacy-obligations).
- [ ] Nothing on the page presents nad-lan as a broker (Brokers Law exemption
      depends on it).

## F. QA gates before publish (Claude's job, every time)

1. php -l on any code touched; MD5-verified deploy through the owner-run
   pipeline.
2. Live GET of the page: 200, full length, title correct.
3. Computed-style check on any dark-surface heading (the theme's !important
   cascade makes failures invisible to the eye - see nadlan-css-cascade-hazard).
4. Mobile 375px numeric overflow scan on the showroom.
5. Dash scan (U+2013/U+2014 = fail).
6. Internal links resolve 200.
7. hreflang cluster prints once and lists only published variants.

## The factory flow

1. Owner throws a project name (or slug).
2. Content agent (ChatGPT) runs the standing gather-prompt against this
   standard: facts, sources, plans, verified coordinates, Hebrew article,
   then the four language variants by the UTOPIA method.
3. Claude assembles: page/post creation via the seed pipeline, showroom wiring,
   meta, schema; runs every QA gate above.
4. Owner runs deployNNN.ps1. The script self-verifies and self-rolls-back.
5. The session board and AGENT-LOG record the result.
