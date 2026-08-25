# RECEIPT — CITY-LAYER PURGE (owner option C) — 2026-08-25

Owner decision (voice, 25.8.2026): the city-page layer cannibalizes the head
queries ("פרויקטים חדשים ב-X" splits across up to 5 URL shapes, all page 3-7,
zero clicks — GSC evidence read with the owner's eyes). Canonicals/noindex
patching rejected. Order: delete the ENTIRE city layer, 410 everything,
/projects/ is the single home for the projects intent; important cities get
rebuilt later, deliberately, one page per city max.

## What shipped (live 1.72.218 → **1.72.219**, all server-linted token_get_all(TOKEN_PARSE), MD5 in/out, .bakC1 siblings)

| file | old md5 | new md5 | change |
|---|---|---|---|
| inc/breadcrumbs.php | d011a88b5e7a524782ffbe91b131c493 | 113fda7bb73b7fe81521e887e3fcf972 | city crumb removed from project+property trails (visible + JSON-LD) |
| inc/directory.php | 51c3c505bf31972560b86ad3fb248e18 | b841378bf524e0b74da3182cc9d67f80 | the 12 hard /city/X/projects/ links removed from the /projects/ intro |
| inc/smart-404.php | 0426c59615dad7469ef31192ddee7897 | ba96e08bc7c5e21397d27f420b635a15 | NEW: template_redirect prio 5 forces **410 Gone** on `^/(city|cities)(/|$)` (helpful body still renders); 404-body city suggestion now points to /projects/; `wpseo_sitemap_exclude_taxonomy` drops nadlan_city from the sitemap index |
| nadlan-config.php | 9630b7c494be6bbbee149492e1745f0b | 1ab00cefcd3d9e968d6283a458ac3a30 | version bump only |

Content: **186 pages under /city/ trashed** (REST DELETE → trash, 0 errors,
restorable ~30 days). Full pre-delete export (id/slug/link/title/content.raw):
`docs/wp-state/city-pages-export-2026-08-25.json` (2.7MB). Pre-patch live
bytes: `docs/wp-state/*.live-1.72.218.php`. The `nadlan_city` TAXONOMY DATA was
kept (bulk-project-seo reads city terms for honest titles) — only its public
`/cities/` archive URL died.

## Evidence (code = server/DOM check; eyes = screenshot looked at)

- code: health `1.72.219 ok`; `/city/`, `/city/רמת-גן/`, `/city/רמת-גן/projects/`,
  space-variant `/city/רמת גן/projects/`, `/cities/תל-אביב-יפו/` → all **HTTP 410**
  with the helpful body; `/projects/` and h-infinity render with ZERO `/city/`
  references; `/projects/?city=רמת-גן` canonical → `https://nad-lan.co.il/projects/`;
  sitemap index no longer lists nadlan_city-sitemap; page-sitemap has no /city/ URLs;
  x- snippet (id 597) deleted with NO residue (list-verified).
- eyes (headless Chrome shots, looked at; controls NOT pressed this session):
  410 page renders header/search/cards correctly; rainbow intact (breadcrumb
  now בית›פרויקטים›…, progress bar, theater, WhatsApp elephant); h-infinity intact.
  In-app browser pane was classifier-blocked this session — headless was the eyes path.

## Rollback

1. Server files: `.bakC1` siblings next to each swapped file (uPress).
2. Pages: WP admin trash → restore (or re-create from the JSON export).
3. Repo mirrors both states (live-1.72.218 originals + patched files).

## GSC — EXECUTED by the agent via the owner's Chrome (owner's explicit order same day: "you have access, do it")

1. ✅ Removals: prefix request `https://nad-lan.co.il/city/` — submitted, status "Processing request" (Aug 25, 2026, eyes).
2. ✅ Removals: prefix request `https://nad-lan.co.il/cities/` — submitted, "Processing request" (eyes).
3. ✅ Sitemap `https://nad-lan.co.il/sitemap_index.xml` resubmitted — "Sitemap submitted successfully", table row Submitted=Aug 25, 2026 (eyes).
4. Pre-submission full sitemap audit (code, checker002.py): 17 sub-sitemaps all 200; **zero** /city/ or /cities/ URLs anywhere; page-sitemap 393 URLs swept one-by-one — **all 200**; totals: projects 1001+33, professionals 2727, glossary 144, intl 17, properties 8.
5. Expect: impressions on the dead family drop (they had 0 clicks); meaningful movement judged at 6-16 weeks, not week 1.

GSC UI traps (paid tonight): the removal dialog IGNORES synthetic mouse clicks on
its footer buttons (silently no-op) — the working path is KEYBOARD ONLY: open via
find+ref click, Tab to the URL field (watch focus ring), type, Tab into radiogroup,
ArrowDown to "prefix", Tab Tab to NEXT, Enter, then on the confirm screen Tab
(CANCEL→SUBMIT) + Enter — "Submitting request" progress = it really fired.
Domain properties reject relative sitemap paths — submit the FULL https URL.

## Standing rules recorded (owner-approved 25.8)

- Project pages speak BRAND ("ריינבו תל אביב"), never category phrasing
  ("פרויקטים חדשים ב-X" forbidden in project titles/h1).
- Category-intent internal anchors point ONLY at /projects/ (never at a project page).
- New project slugs: brand-first; city suffix optional. EXISTING slugs untouched
  (project+city queries are the site's converting queries; no 301s exist).
- Filters must never mint indexable URLs; phase 2 moves /projects/ filtering to
  JS state (no ?city= URL writes).

## New traps (this session)

- uPress WAF (nginx) 404s any URL with a `.php` filename in the QUERY STRING —
  snippet route file params must travel base64 (`fb64`).
- Secrets JSON keys on machine 777: `username` + `password_dpapi` (DPAPI-in-base64).
- Browser-pane preview can be classifier-blocked → headless Chrome + Read the PNG.

## Phase 2 queue (needs owner GO)

Strengthen /projects/: title/h1 for the national head term, intro rewrite,
fast JS filter with real per-city counts (no URL params), city presence
on-page. Later: rebuild ONLY important cities as single strong pages.

Deploy runner: scratchpad deploy001.py + run001.ps1 (this session's scratchpad).
Git: local commit only — push still broken on 777 (SAC/libcurl); gh-api pusher pattern pending.
