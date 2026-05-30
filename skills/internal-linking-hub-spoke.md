# Internal Linking — hub-and-spoke implementation log

> **Notice to all agents:** the live nad-lan.co.il site has 153 internal links added in the 2026-05-28 late-night session, mapping the 42 published pages into the hub-and-spoke architecture defined in `strategy-master.md` §5. **Before adding more internal links, read this file first** — the markers, cluster maps, and back-link patterns are documented here. Do not duplicate.

## What was implemented (2026-05-28)

Three linking sweeps via WP REST API on the live site:

### Sweep 1 — Pillar → Spokes ("Related Articles" block)
- **11 pillar pages** updated
- Each appended a `<!-- nadlan-hub-related-v1 -->` block at the end of content
- Block contains: separator, H2 "מדריכים קשורים — {cluster_label}", explanation paragraph, bullet list of links to all spokes in cluster
- Anchor text: each spoke's full Hebrew title (exact-match per strategy §5 anchor rules — 60% exact)
- Total outbound links from pillars: ~63

### Sweep 2 — Spoke → Pillar ("Back to pillar" block)
- **30 spoke pages** updated (every non-pillar page in the cluster map)
- Each appended a `<!-- nadlan-spoke-backlink-v1 -->` block at the end of content
- Block: wp:group with `accent-5` background (cream from brand palette), containing two paragraphs:
  - "**חלק מהמדריך:** [pillar title]"
  - "**ראה גם באותו אשכול:** [sibling 1] · [sibling 2]"
- Each spoke gets exactly ONE pillar parent (strategy §5: "one parent only")
- Each spoke gets 2 sibling recommendations (strategy: ≥2 incoming links per spoke)
- Total back-links: ~30 pillar back-links + ~60 sibling links = ~90 links

### Sweep 3 — Homepage Tools strip
- Homepage (id=2) appended a `<!-- nadlan-tools-strip-v1 -->` block at the end
- Block contains: separator, H2 "כלים מקצועיים לבדיקת עסקת נדל"ן", paragraph, list of all 5 calculator pages
- Strategy §2 + §5: tools get ≥5 incoming links; this contributes "home" link to each

## Cluster map (memorized — repeat the same shape if adding pages)

| Pillar slug | Cluster label (HE) | Spokes (slugs) |
|---|---|---|
| `buying-apartment` | קניית דירה | apartment-buying-checklist, tabu-extract-check, property-value, home-inspection, real-estate-broker, real-estate-appraiser, new-projects, purchase-tax-calculator, mortgage-calculator, apartment-purchase-cost-calculator, real-estate-lawyer |
| `selling-apartment` | מכירת דירה | real-estate-broker, real-estate-appraiser, property-value-estimator, real-estate-tax-advisor, real-estate-lawyer |
| `investment-apartment` | דירה להשקעה | investment-property-mortgage, investment-property-cashflow-calculator, property-management, commercial-real-estate, real-estate-tax-advisor, new-projects, real-estate-lawyer |
| `investment` (NEW 2026-05-29, pillar id 421) | נדל"ן להשקעה — איפה ואיך | apartments-for-investment (425), real-estate-yield (422), bank-guarantee-purchase (424), short-term-rentals-abroad (345) |
| `short-term-rentals-abroad` (NEW pillar id 345) | השכרה לטווח קצר בחו"ל | short-term-rentals-portugal (401), short-term-rentals-thailand (404), short-term-rentals-dubai (407), short-term-rentals-greece (398), short-term-rentals-italy (418), short-term-rentals-spain (417), short-term-rentals-cyprus (416) |
| `mortgage-calculator` (tool-pillar) | משכנתא | mortgage-advisor, mortgage-refinance, mortgage-home-insurance, investment-property-mortgage |
| `real-estate-tax-advisor` | מיסוי מקרקעין | purchase-tax-calculator, apartment-purchase-cost-calculator, real-estate-lawyer, tabu-extract-check |
| `real-estate-lawyer` | עורך דין מקרקעין | real-estate-tax-advisor, apartment-buying-checklist, tabu-extract-check, new-projects, urban-renewal |
| `urban-renewal` | התחדשות עירונית | real-estate-lawyer, apartment-buying-checklist, architect-building-permit, construction-supervisor |
| `commercial-real-estate` | נדל"ן מסחרי | investment-apartment, investment-property-cashflow-calculator, real-estate-tax-advisor, real-estate-lawyer |
| `new-projects` | דירה מקבלן | construction-supervisor, architect-building-permit, home-inspection, real-estate-lawyer, apartment-buying-checklist |
| `professionals` (hub) | אנשי מקצוע | real-estate-lawyer, real-estate-broker, real-estate-appraiser, mortgage-advisor, home-inspection, construction-supervisor, architect-building-permit, property-management, renovation-contractor, real-estate-tax-advisor |
| `tel-aviv-apartment-prices` (city hub) | מחירי דירות בתל אביב | tel-aviv-seafront-apartment-prices, tel-aviv-penthouse-prices, tel-aviv-luxury-apartment-prices, neve-tzedek-apartment-prices |

### Cluster wiring status (audit 2026-05-30)

| Cluster | Pillar→spoke links present | Spoke→pillar links present | Spoke→sibling links present | Lawyer-CTA on spokes |
|---|---|---|---|---|
| `investment` (421) | ✓ 4 of 4 | ✓ on spoke 10 only | ✗ MISSING on 422, 425, 424 | ✗ MISSING everywhere |
| `short-term-rentals-abroad` (345) | ✓ (pillar links to all 7) | ✓ 7 of 7 (each spoke has 1 link to pillar) | ✗ MISSING on all 7 | ✗ MISSING everywhere |

**Action required:** wire spoke→sibling + lawyer CTA across both new clusters. Use the `<!-- nadlan-spoke-backlink-v1 -->` marker pattern. Until done, these clusters are orphan-spoke trees that bleed link equity.

## Primary-pillar map for spokes (each spoke → ONE pillar)

| Spoke | Primary pillar |
|---|---|
| apartments-for-investment (425) | investment (421) |
| real-estate-yield (422) | investment (421) |
| bank-guarantee-purchase (424) | investment (421) |
| short-term-rentals-portugal (401) | short-term-rentals-abroad (345) |
| short-term-rentals-thailand (404) | short-term-rentals-abroad (345) |
| short-term-rentals-dubai (407) | short-term-rentals-abroad (345) |
| short-term-rentals-greece (398) | short-term-rentals-abroad (345) |
| short-term-rentals-italy (418) | short-term-rentals-abroad (345) |
| short-term-rentals-spain (417) | short-term-rentals-abroad (345) |
| short-term-rentals-cyprus (416) | short-term-rentals-abroad (345) |
| apartment-buying-checklist | buying-apartment |
| tabu-extract-check | real-estate-lawyer |
| property-value | buying-apartment |
| home-inspection | buying-apartment |
| real-estate-broker | professionals |
| real-estate-appraiser | professionals |
| purchase-tax-calculator | real-estate-tax-advisor |
| apartment-purchase-cost-calculator | real-estate-tax-advisor |
| property-value-estimator | selling-apartment |
| investment-property-cashflow-calculator | investment-apartment |
| mortgage-advisor | mortgage-calculator |
| mortgage-refinance | mortgage-calculator |
| mortgage-home-insurance | mortgage-calculator |
| investment-property-mortgage | investment-apartment |
| property-management | investment-apartment |
| construction-supervisor | new-projects |
| architect-building-permit | new-projects |
| renovation-contractor | professionals |
| tel-aviv-seafront-apartment-prices | tel-aviv-apartment-prices |
| tel-aviv-penthouse-prices | tel-aviv-apartment-prices |
| tel-aviv-luxury-apartment-prices | tel-aviv-apartment-prices |
| neve-tzedek-apartment-prices | tel-aviv-apartment-prices |
| herzliya-apartment-prices | buying-apartment (until a "Sharon" pillar exists) |
| herzliya-pituach-apartment-prices | buying-apartment |
| ramat-hasharon-apartment-prices | buying-apartment |
| raanana-apartment-prices | buying-apartment |
| kfar-shmaryahu-house-prices | buying-apartment |
| savyon-house-prices | buying-apartment |
| rishpon-house-prices | buying-apartment |
| arsuf-house-prices | buying-apartment |

**Sharon-area note:** these 8 neighborhood pages currently parent to `buying-apartment` because no dedicated "Sharon" pillar exists. When a Sharon pillar is created (suggestion: `/cities/sharon/`), re-parent these via the same script.

## Idempotency markers (don't add the same block twice)

Three markers in page content; any future agent's link-sweep script MUST check for these before adding:

```
<!-- nadlan-hub-related-v1 -->        ← pillar pages have a Related Articles block
<!-- nadlan-spoke-backlink-v1 -->      ← spoke pages have a Back-link + Siblings block
<!-- nadlan-tools-strip-v1 -->         ← home page has the Tools strip
```

To extend (e.g., add more spokes to a cluster's related block): bump marker to `-v2` and write a migration that removes `-v1` block + adds new one.

## Anchor text discipline (strategy §5)

The current implementation uses **100% exact-match anchor text** (page's full Hebrew title). Strategy targets:
- 60% exact match → current ratio is over-rotated to exact
- 30% partial / context anchor → not yet implemented
- 10% branded or "כאן" → not yet implemented

**Next agent should** introduce variation in a future link sweep. Examples of partial anchors:
- For `mortgage-calculator`: "מחשבון משכנתא", "החזר חודשי", "תכנון המשכנתא"
- For `real-estate-lawyer`: "עורך דין נדל"ן", "בדיקה משפטית", "ייצוג בעסקת מקרקעין"

Branded anchors: "במדריך של נדלן חכם", "אצלנו".

## What's still missing for "ranks first on Google" — TODO

- [ ] **Breadcrumbs on every page.** Block themes need a breadcrumb block in the `templates/page.html` template. Yoast SEO provides a breadcrumbs block; add it. Requires theme template edit + UPress sync.
- [ ] **Yoast cornerstone marking** for the 11 pillars. Currently blocked by Yoast Free REST limitation (`_yoast_wpseo_is_cornerstone` not exposed). Must be done in WP admin manually OR by adding a tiny `register_meta` filter in the plugin (v1.0.5, owner approval gate).
- [ ] **Yoast meta descriptions** (42 pages empty). Same blocker. Same fix.
- [ ] **Yoast Person schema** for the lawyer-owner. Needs owner's full Hebrew name + bar number. Configure in WP admin → SEO → Search Appearance, or via Yoast REST (verify which fields are writable).
- [ ] **Anchor diversity** (above).
- [ ] **Featured images on all pages** (1 image total on site as of 2026-05-28). Codex side: pick from `C:\Users\pro\.codex\generated_images` per `image-pipeline.md`.
- [ ] **Submit sitemap to GSC.** GSC is connected via Site Kit; verify sitemap was auto-submitted, or submit manually at https://search.google.com/search-console.
- [ ] **Mark pillars as cornerstone in WP admin manually** (5 minutes of clicking; affects internal-link analyzer).
- [ ] **Sharon cluster:** create a `cities/sharon/` pillar page + re-parent the 8 Sharon-area neighborhood pages.

## How to verify the linking is live

Visit any pillar page (e.g. `https://nad-lan.co.il/buying-apartment/`), scroll to the bottom — you should see "מדריכים קשורים — קניית דירה" heading with the list of 11 spoke links.

Visit any spoke (e.g. `https://nad-lan.co.il/mortgage-advisor/`), scroll to the bottom — you should see a cream-coloured group block with "חלק מהמדריך:" linking to mortgage-calculator + "ראה גם" with 2 sibling links.

Visit homepage — scroll to bottom — Tools strip with 5 calculator links.

## Revision 2026-05-30 — Claude Code (claude-opus-4-7)

Audited the 2026-05-29 publishes by Cowork. Findings:

- **6 of 7 short-rent country spokes shipped with escaped HTML** (`&lt;h2&gt;` visible as literal text). Fixed by REST PATCH with html.unescape() + removal of ChatGPT preamble + citation footnotes.
- **All 7 short-rent spokes are orphans** — each links only back to the pillar; none link to siblings or to the lawyer CTA.
- **3 of 4 investment-cluster spokes are orphans** (422, 425, 424). Only spoke 10 (investment-apartment) has proper internal linking from the earlier 2026-05-28 sweep.
- **Missing Yoast metadesc** on pages 398, 416, 417, 418, 421, 425 (6 pages). Google falls back to first paragraph for these.
- **No lawyer CTA block** anywhere in the new clusters. Money-path zero from these pages.

This is exactly the failure pattern that `article-publishing-protocol.md` exists to prevent. The protocol now exists; the next sweep must apply it retroactively to these 11 pages.

Updated cluster map to include the two new pillars + spokes. Added wiring-status table at end of map showing what's still missing.

---
_Created 2026-05-28 by Claude Code (claude-opus-4-7) during the "make it rank on Google" session. Updated 2026-05-30 with the 2026-05-29 Cowork audit + new clusters._
