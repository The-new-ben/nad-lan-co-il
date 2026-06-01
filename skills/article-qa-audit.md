# Skill: Article QA & Site Audit (pixel-level, GEO + E-E-A-T grounded)

> The repeatable audit any agent runs against the live site. Grounded in verified 2025-2026 research (sources at bottom). Run the automated scan first, then the manual/judgment layer. **Audit reads the LIVE rendered page, never trusts the writer's self-report** — Cowork's "QA-clean" claims were wrong on en-dashes and CTAs; only the live HTML is truth.

## How to run the automated scan
The scan script lives conceptually in this skill (reproduce in Python via WP REST `wp/v2/pages/<id>?_fields=content`). Per article it measures and gates:

### Hard gates (fail = do not publish / must fix)
| Check | Threshold | Why |
|---|---|---|
| em-dash `—` | 0 | owner-banned AI-tell |
| **en-dash `–` / `&#8211;`** | **0** | the loophole Cowork used — same AI-tell, different glyph. Ranges use `-`, separators use `:` or `,` |
| `{index=N}`, `Source+N`, `AADE+N`, `[1]` | 0 | LLM citation artifacts |
| preamble (`<p>להלן`, `<p>הנה המאמר`) | 0 | AI framing |
| opener `במאמר זה נציג/נפרט/נדון` outside disclaimer | 0 | AI-tell |
| body-byline (`<p>מאת` outside disclaimer) | 0 | duplicate byline |
| h2 count | 6-11, **all unique** | duplicate h2 = stitched output |
| word count | 1800-3500 | floor for depth; 543 failed at 1593 |
| numeric data points | ≥20 | YMYL needs hard numbers |
| law/regulator refs | ≥15 **for legal/tax topics** (judgment: a "pricing"/"selling-without-broker" piece naturally has fewer — don't blanket-fail) | trust + entity grounding |
| `div.cards` / `<table>` / `div.note` / `div.cta` | ≥1 / ≥1 / ≥3 / **≥2** | structure + conversion |
| AI-tell phrases | 0 | list below |

### AI-tell phrase blocklist (Hebrew)
חשוב להבין · חשוב מאוד · חשוב לזכור · חשוב לבדוק · ראוי לציין · במילים אחרות · בעידן · עולם הנדל · ללא ספק · אינסוף · באופן כללי · בסופו של דבר · לסיכום · כפי שראינו · חוד החנית · אבן יסוד · מורכבות ההליך · דורשת הבנה מעמיקה · **מהווה** (overuse — appeared in ~20/22 articles) · **מטבע הדברים** · **יש לציין כי**

Also flag **templated H2 openers** ("למה X היא ההחלטה הקריטית/החשובה ביותר") repeating across articles — vary them.

## Answer-engine readiness layer (GEO/AEO — VERIFIED research)
The Princeton/Georgia-Tech "GEO" paper (KDD 2024, arXiv 2311.09735) measured what lifts AI-citation visibility:
- **quotations from named experts/sources: ~+41%**
- **statistics: ~+32%**
- **citations to sources: ~+30%**
- fluency + authoritative language: ~+28%
- keyword stuffing: no help / sometimes hurts

Per-article GEO checks:
- [ ] First sentence of the article AND of each H2 directly answers/defines the heading (definitional lead — "מס רכישה הוא...").
- [ ] A TL;DR / summary block in the **top 30% of the page** (Surfer: ~55% of AI citations come from the top third).
- [ ] ≥2 statistics with **inline cited source** (e.g. "(רשות המסים, 2026)").
- [ ] ≥1 named-expert attribution or quotation.
- [ ] ≥1 data table + ≥1 list.
- [ ] Named entities correct (law names + numbers, רשות המסים, בנק ישראל, court names).
- [ ] H2/H3 phrased as real Hebrew user questions (mirror PAA).

Note: AI Overviews now cite only ~37% from top-10 organic (Ahrefs, 2026) due to query fan-out → being the best answer to the *specific sub-question* beats raw ranking.

## E-E-A-T / YMYL layer (Google SQRG, updated 2025-09-11)
- [ ] Visible author byline + credentials + link to author page (`/author/ben-betesh/` exists ✓).
- [ ] "נכתב/נבדק על ידי" reviewer line with credentials + review date.
- [ ] Publish date + **last-updated date** visible (tax/rate content re-checked yearly).
- [ ] ≥2 outbound links to **primary authoritative sources** (רשות המסים, בנק ישראל, חקיקה ב-nevo/הכנסת, פסיקה).
- [ ] No unreviewed AI boilerplate (SQRG rates unreviewed AI + no added value "Lowest Quality").

## Schema layer (verified current status)
- [ ] `Article` (author, datePublished, dateModified, publisher) — present ✓
- [ ] `Person` with `sameAs` (bar profile, jus-tice.co.il) — present, but verify `sameAs` populated
- [ ] `BreadcrumbList` — present ✓
- [ ] `Organization` site-wide — present ✓
- [ ] `FAQPage` — OPTIONAL: FAQ **rich results** fully removed by Google over 2026 (restricted to gov/health since Aug 2023; full removal May-Aug 2026). Markup still machine-readable for AI; keep lightweight, expect no SERP feature.
- [ ] Do NOT rely on `HowTo` (deprecated desktop Sep 2023) for rich results.

## Internal-linking / topical-authority layer
- [ ] Links **up to pillar** (✓ on all 22 after 2026-05-31 fix).
- [ ] **3-8 contextual in-body links** (pillars: 8-15).
- [ ] **≥1 inbound link from a sibling** (no orphans). Mortgage pillar 121 had 0 down-links until fixed 2026-05-31 — re-audit quarterly.
- [ ] ≤3 clicks from homepage.
- [ ] Anchor text descriptive + varied (no repeated exact-match).

## Site-wide / technical layer (audit beyond single articles)
- [ ] robots.txt references the sitemap (`Sitemap: https://nad-lan.co.il/sitemap_index.xml`) — **was MISSING 2026-05-31**.
- [ ] WooCommerce system pages (cart/checkout/my-account/shop) set to **noindex** — they're thin + were in sitemap.
- [ ] Exactly **one H1** per page — **homepage had 2 H1s 2026-05-31** (demote the second to H2).
- [ ] og:image present (homepage missing it — social + some AI engines use it).
- [ ] Submit sitemap to **Bing Webmaster Tools** (ChatGPT Search uses Bing's index).
- [ ] Every published page has ≥1 inbound internal link (orphan sweep across all 97 pages).

## Sources (verified 2026-05-31)
- GEO paper: https://arxiv.org/abs/2311.09735 · https://collaborate.princeton.edu/en/publications/geo-generative-engine-optimization/
- AI Overview citations vs top-10: https://ahrefs.com/blog/ai-overview-citations-top-10/
- AI citation position-on-page: https://surferseo.com/blog/ai-citation-report/
- Google SQRG 2025-09-11 (PDF): https://services.google.com/fh/files/misc/hsw-sqrg.pdf
- FAQ rich-result removal timeline: https://searchengineland.com/google-to-no-longer-support-faq-rich-results-476957
- Topic clusters: https://searchengineland.com/guide/topic-clusters
- E-E-A-T for AI search: https://ipullrank.com/eeat-ymyl-ai-search

_Created 2026-05-31 by Claude Code (claude-opus-4-7/4-8). Unverified marketing stats ("2.3x tables", "3.2x FAQ") deliberately excluded — only traceable research used._
