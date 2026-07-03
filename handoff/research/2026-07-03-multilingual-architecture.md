# Systematic 5-language architecture (he/en/fr/ru/ar) — the right way

Owner law: full, systematic translation. If the Hebrew changes, every language
reflects it. Full page incl. footer. No hard-coding. No duplicate-content
penalty. The switcher design from the HTML blueprint, on the homepage and
site-wide. This doc is the plan; one decision needed before I build the engine.

## The two layers (this is the key mental model)
A page is **chrome** + **content**. They translate differently, and conflating
them is where sites go wrong.

1. **Chrome** = nav, footer, buttons, band titles, labels, disclaimers, the
   switcher itself. This is FINITE and SYSTEMATIC: one string table per
   language (`nadlan_i18n('key')`). Change the table once → every page, every
   band, the footer, all reflect it automatically. This is 100% automatable now,
   no generation run. It is what makes the site "fully translatable
   systematically."
2. **Content** = article bodies, news, project descriptions, prices-with-notes.
   This CANNOT be honestly auto-mirrored — it must be REAL translated text.
   Two honest options per content type:
   - a real translated CMS entry (best; from the generation run with an agent), OR
   - graceful fallback: show the Hebrew original with a clear language note AND a
     correct hreflang, so Google is not penalised and the user is not deceived.
   NEVER machine-translate on the fly and pass it as native — that is the exact
   "beautiful lie" the honesty law forbids.

## URL scheme — THE ONE DECISION I NEED
Google requires a distinct URL per language. Options:
- **A. Subdirectories** `/`, `/en/`, `/fr/`, `/ru/`, `/ar/` (recommended).
  Cleanest for SEO, standard, WPML/Polylang-compatible, easy hreflang.
- **B. Query param** `/?lang=en`. Easier to bolt on, weaker SEO, Google may
  ignore/merge. Not recommended.
- **C. ccTLD/subdomain** `en.nad-lan.co.il`. Overkill, ops-heavy.
**My recommendation: A (subdirectories).** Hebrew stays at the root (canonical
default). I need your yes on A before wiring routing.

## SEO wiring (per the research — mandatory, applies to ALL language pages)
- **Self-referencing canonical** on each language page (the `/en/` page's
  canonical points to itself, NOT to the Hebrew — that was the mistake that
  causes the "5 Ashiras look like duplicates" penalty).
- **Bidirectional hreflang** cluster on every page: he ↔ en ↔ fr ↔ ru ↔ ar,
  plus `x-default` → Hebrew.
- **Switcher links to the real language URLs** (crawlable `<a href>`), not a
  JS-only toggle. JS enhances; the href is the truth.
- **Per-language XML sitemap** with hreflang, submitted to GSC.
- **Localised `<title>`/meta** per language (not the Hebrew title translated
  by Google).

## The "5 Ashiras in the catalog" fix
Today the 5 language project posts each appear in `/projects/`. Fix:
- Mark the 5 as hreflang alternates of ONE canonical project.
- The catalog (`/projects/`, homepage bands) shows ONLY the current-language
  version (query filtered by language), never all five. One project, five
  language faces — not five listings.

## Build phases (so nothing ships half-broken)
1. **i18n engine** (chrome, systematic): string-table loader + `nadlan_i18n()`,
   used by home-v2 bands + footer + nav. Ship with Hebrew + the switcher; other
   languages light up as their tables fill. No live page breaks — Hebrew is
   unchanged; `/en/` etc. are NEW URLs.
2. **Language routing + hreflang/canonical** on the homepage; the switcher wired
   to `/en/…` real URLs.
3. **Content model**: per-language content resolution with honest fallback;
   catalog dedup by language.
4. **Generation run** (agent/ChatGPT): produce real translated article/news/
   project bodies → drop into the CMS → pages become fully native per language.
5. Roll the same engine to project pages, listings, professionals.

## Honesty commitments
- No live page flipped to a half-translated state. Hebrew stays whole; new
  language URLs appear only as their content is real.
- No machine-translation passed as native.
- Chrome is systematic (reflects changes); content is real (generated), never
  faked.

## Next after this: project filtering (owner: "mission for next")
Booking-style multi-parameter filtering — gym, ממ״ד/safe room, A/C, parking,
elevator, accessibility, balcony, storage, nearby (school/park/transit/retail),
price, rooms, floor, delivery year, developer, status. Needs the project data
model from the mega-prompt dataset. Queued.
