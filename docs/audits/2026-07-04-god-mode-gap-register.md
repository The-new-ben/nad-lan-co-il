# God-mode gap register — the standing worry list (unprompted)

The owner asked what I worry about without being told. This is the living
register I hold against every change. Ranked by damage to the business.
Rule: every new lesson lands here AND in the god-skill.

## Trust surfaces a contractor/buyer hits BEFORE the product
1. **Share previews** — was: no og:image + stale favicon (FIXED v1.70.9,
   verified). Watch: per-page og on projects/professionals still SVG-based;
   FB/WhatsApp can't render SVG og — replace with PNG cards next plugin pass.
2. **Email deliverability** — before any contractor blast: SPF/DKIM/DMARC on
   nad-lan.co.il, a real From mailbox, unsubscribe headers. A perfect page
   means nothing if the mail lands in spam. NOT yet verified.
3. **Broken brand assets in repo** — `assets/branding/logo.png` is mirrored
   gibberish ("סכח ן״לדנ") of the RETIRED brand. Anyone grabbing it ships a
   broken logo into a deck/email. Should be deleted or replaced.
4. **404/soft surfaces**: old showroom URLs, /projects catalog showing 5×
   language duplicates of Ashira — catalog dedup still pending.

## Honesty debts (things currently on the site that could mislead)
5. Prototype prices/inventory in unit-maps are labeled honestly in data files,
   but every NEW surface must re-carry the label — the factory does, the future
   WP page must too.
6. ChatGPT coords quarantined in DB (good) — the RISK is someone "just uses"
   `coord_estimate_unverified` to light up the map. The map prototype
   deliberately renders only verified pins; keep that gate when productionizing.
7. hreflang on project pages exists only in the prototypes; the LIVE WP project
   pages still lack the language architecture the homepage now has.

## Product/competitive gaps (vs Madlan/Yardim-class rivals)
8. **Search & filtering** — Booking-style multi-parameter filters (ממ״ד, gym,
   parking, delivery year...) queued; without it we lose task-driven buyers.
9. **Real inventory** — until a developer feeds true availability, "choose your
   apartment" is a demo. The mega-prompt dataset + developer outreach is the
   unlock; this is THE moat and THE risk.
10. **Interior/view-from-unit** — promised experience, currently partial.
11. **Performance** — prototype pages embed ~1.1MB GLB as base64 inline; fine
    for prototypes, WRONG for production (no caching, blocks parse). Production
    must load GLB as a separate cached asset with poster-first LCP.
12. **Mobile** — factory pages QA'd on desktop; mobile pass pending.

## Platform/ops risks
13. **Squash-merge conflict loop** — every release needs the reset+cherry-pick
    dance; one day someone will force-push wrong. Consider merge-commit policy
    or release branch.
14. **Two translation systems risk** — if WPML/Polylang gets installed on top
    of our i18n engine, duplicate-content chaos. Documented, watch installs.
15. **Model-viewer v4 pitfalls** — `environment-image="neutral"` invalid in v4
    (harmless now), dynamic-scaling canvas artifact on weak GPUs (clamp
    insurance added in factory; add same to any WP-side viewer).
16. **Site icon/media hygiene** — old May favicons still exist as media items;
    scrapers with long caches may show them a while (harmless, expires).

## Data pipeline worries
17. Geocode pass not yet run — 33/33 records `needs_geocode`. Everything
    downstream (map, distance facts, "near the sea" 3D anchors) waits on it.
18. Price pass 0/33 — pages can ship with honest "no price yet" but conversion
    suffers; prioritize the price pass for the 4 flagship projects.
19. Rainbow unit-count conflict (459 vs 480) unresolved with the developer;
    page currently says 480 with FAQ sourcing.
20. No rich Dimri GLB exists in repo despite belief otherwise — needs upload
    from wherever it lives, or Tier-B regen from the 3D-generation pack fields.
