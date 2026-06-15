# SKILL: Project Page SEO + Assembly Standard (replicate for EVERY project, countrywide)
**Created:** 2026-06-12, from the Rainbow Tel Aviv work (v1.60.4). Owner directive: "what you did here is very important for the other pages to be with quality."

Use this skill whenever creating or upgrading a `nadlan_project` page. It encodes the full method: audit → SERP → intent map (incl. international) → paste assets → schema meta → design wrapper. Companion skills: `article-guide-design-pattern.md` (the framed body design), `project-3d-sales-experience.md` (the interactive module), `copywriting-skill.md`.

## 1. Page assembly standard (what a complete project page IS)
Order on the page:
1. `nlpf` profile header (one visible H1 = `{English name} – {Hebrew name}`).
2. Interactive 3D module (project-3d, auto-embedded after header).
3. **Article body wrapped in `nadlan-guide`** (see article-guide-design-pattern.md) — NEVER bare `<h2>/<p>` black-on-white bold. The Rainbow page shipped bare and the owner flagged it immediately: framed sections, cards, notes, byline, disclaimer are the house design language. Live references: /real-estate-lawyer/, /investment/.
4. FAQ section (H2 "שאלות נפוצות על {name}") + `project_faq_json` meta for FAQPage schema.
5. Sources section ("מקורות שנבדקו") — every market figure cited with outlet + date.

## 2. SEO method (the Rainbow dossier recipe — repeat per project)
1. **Audit the live page**: title, meta description, H1 count, H2s, schema blocks, Hebrew word count, and a transactional-keyword count (למכירה / מחיר / פנטהאוז / חדרים / דירות יוקרה). The classic failure: rich informational content with ZERO transactional vocabulary.
2. **SERP check** (the project name + "פרויקט דירות", and + "דירות למכירה מחיר"): list who ranks. The developer's official site always wins navigational — DON'T fight it. Win the gaps: price queries, evaluation queries ("כדאי?"), comparison queries, foreign-buyer queries. Harvest **citable market facts** from news coverage (Calcalist/Bizportal/Ynet/Madlan) — sold counts, ₪/m², entry prices, notable transactions.
3. **Title formula**: `דירות למכירה ב-{Name} {City} | מחירים, תוכניות ובחירת דירה ב{Area} | נדל"ן חכם` — transactional first, features never.
4. **Meta description formula**: name (EN+HE) + area + REAL cited price hooks + the interactive differentiator + "כולל לרוכשים מחו"ל".
5. **Three mandatory content blocks** (paste-ready Hebrew, engineered to survive translation):
   - A: "דירות למכירה ב-{Name} — מה זמין עכשיו" (mix, sold count w/ source, CTA into the picker).
   - B: "מחירי דירות ב-{Name} — נתונים מדווחים" (₪/m² + avg + entry, EVERY figure with source+date, disclaimer "אינם הצעת מחיר").
   - C: "מדריך לרוכשים מחו"ל" (מס רכישה לתושב חוץ [owner-lawyer verifies rates], ~50% LTV, ייפוי כוח, multilingual lawyer). This block targets the EN/FR/RU/AR "buying property in Israel as a foreigner" query family when translated.
6. **International intent packing**: structure Hebrew around intents that exist in EN ("tel aviv apartments for sale", "israel real estate investment"), FR ("acheter appartement tel aviv"), RU ("купить квартиру в тель-авиве"), AR ("شقق فاخرة تل أبيب"). Numbers stay language-neutral (meta-driven, `Intl.NumberFormat` later). Keep ₪ + m² figures — international buyers search by m².

## 3. Schema meta fields (v1.60.4+ emits automatically — just fill the meta)
| Meta key | What | Example (Rainbow) |
|---|---|---|
| `lat`, `lng` | geo (also drives 3D view + sun) | 32.1108 / 34.7805 |
| `amenities` | comma-separated | בריכות שחייה, ספא, חדר כושר... |
| `official_site_url` | sameAs link(s), comma-separated | https://rainbowtlv.com/ |
| `price_range` | text w/ sources | דירות 3 חד׳ מ-5.5 מ׳ ₪ (כלכליסט, Bizportal) |
| `price_min`/`price_max` | numbers for AggregateOffer | 5500000 / 30000000 |
| `project_faq_json` | `[{"q":"...","a":"..."}]` → FAQPage | price/developer/availability/foreign-buyer Qs |
| `num_units`, `address`, `city`, `developer_name` | already standard | — |
Assign the `nadlan_compound` term → schema emits containedInPlace + internal-link hub.

## 4. Honesty rails (non-negotiable)
- Every price = source + date, framed as "נתונים מדווחים", never an offer.
- Tax/legal rates flagged `[לאישור הבעלים]` until the owner-lawyer verifies.
- Original imagery only, labeled "הדמיה מקורית להמחשה" when not the developer's.
- No invented availability; "נכון ל{date} דווח..." phrasing.

## 5. Definition of done (gate checklist per project page)
- [ ] Title + meta description per formulas; one visible H1.
- [ ] Body in `nadlan-guide` wrapper (framed, cards, notes — not bare bold).
- [ ] Blocks A/B/C present with citations; FAQ section + `project_faq_json`.
- [ ] All §3 meta filled; Rich Results Test passes ApartmentComplex + FAQPage.
- [ ] Transactional keyword check: למכירה ≥3, מחיר ≥8 occurrences.
- [ ] IndexNow ping fired (automatic on save).
- [ ] Compound term assigned; appears on /compound/ hub.

## 6. Live SEO Verification Addendum

Before a project page becomes the template for another project, verify the rendered public URL, not
only saved meta fields:

1. `node scripts/qa-project-showroom-live.mjs --site <site> --slug <slug> --post-id <id> --strict`
   must pass its structural gates.
2. Extract and record title, meta description, canonical, robots, H1 count, first H2s, OG image,
   schema types and `hreflang`.
3. `hreflang` may be empty only when there are no real translated pages. Do not add language links
   until equivalent translated URLs exist.
4. `og:image` should use HTTPS and a stable project image/poster.
5. Record the SERP landscape: official developer page, district/project aggregators, listing portals
   and news/investor sources. The NadLan angle is the buyer/investor gap: price context, apartment
   selection, plans, view, surroundings and non-binding inquiry, not fake official status.
6. Store the audit in `docs/` or `docs/qa/` with the live plugin version and date. If the visual QA
   is still pending, say so directly and do not mark the page clone-ready.
