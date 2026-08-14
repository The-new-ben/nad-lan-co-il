# NadLan SEO War Plan - 2026-07-29

Grounded in real Search Console data (90d to 2026-07-28): 251 clicks, 31K
impressions, avg position 36.7, indexed 2,394 pages, impressions in 87
countries. Chat carries the full reasoning (owner law: substance in chat);
this file is the repo memory.

## What the data proves
- Branded project queries convert: DUO ranks ~15 on "duo tel aviv" family and
  produced the first unit-level WhatsApp lead. Rainbow page = #2 page sitewide
  (13 clicks). People search PROJECT NAMES; our pages answer with generic titles.
- Valuation intent is the #1 tool magnet: /property-value-estimator/ = top page
  (15 clicks, 2,062 impressions), plus "הערכת שווי נכס/דירה" atop queries.
- Commercial real estate guides quietly earn (3 of top-10 pages).
- "שדה דב" queries exist (30+ impressions) with weak coverage - now we own the
  quarter experience.

## The four workstreams
1. **W1 Branded title rotation (highest ROI, uses existing bulk-project-seo
   module):** batch-retitle catalog projects to `<שם פרויקט> <עיר> - מחירים,
   דירות ובחירה מהבניין | נדלן`. Wave 1 = 50 projects with the most impressions
   at positions 8-40 (pull list from GSC pages tab). Measure weekly.
2. **W2 Mega comparison pages (data-driven, from our own 987-project DB):**
   /projects/tel-aviv-compare/ "כל הפרויקטים החדשים בתל אביב 2026 - ההשוואה
   המלאה" with sortable table: ₪/sqm, floors, units, delivery, developer, sea
   distance, 3D availability. Then per-city clones. Interlink down to project
   pages (feeds W1 positions).
3. **W3 Valuation & commercial hubs:** deepen the winners - estimator hub gets
   related guides + internal links; commercial cluster gets 2 new guides/mo.
4. **W4 Sde Dov authority cluster:** the tour page (indexable version once
   owner approves removing noindex) + /sde-dov/ area page + 12 project pages +
   weekly quarter-news notes = own "שדה דב" outright.

## Cadence and measurement
- Weekly: GSC snapshot (clicks/imps/position for W1 wave pages) -> log deltas
  in AGENT-LOG. Internal-only; never public counters (owner law).
- Monthly: next 50-project wave + one mega page + two guides.

## Prompts (ready to run)
- Mega-article generator, city comparison (Hebrew, no em dashes, tables from
  DB export, honesty labels on estimates).
- Project-title rewriter (keeps legal name, adds intent suffix, <=60 chars).
- Commercial guide writer (cites gov sources, 2026 data, FAQ schema block).
(Full prompt texts delivered in chat 2026-07-29; keep them with the operator.)

## Blockers / owner inputs
- Removing noindex from the tour when he calls it ready.
- GSC API key only if we want the internal dashboard automated (manual weekly
  pull works today via the connected Chrome).
