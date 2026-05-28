# Original Research Prompt — 2026-05-28

> **Notice to all agents:** preserved verbatim per owner request. This is the prompt that triggered the creation of the `skills/` tree and the master strategy brief. If a future re-brief is requested, start from here.

## Source

Provided by the owner during the 2026-05-28 Claude Code session. The owner attributed the prompt to "Laravel" — likely meaning the prompt was prepared in or through a Laravel-based tool. The prompt is in English; the owner instructed the deliverable to be produced in Hebrew, except for internal operational skills which may be in English.

## Prompt (verbatim)

```
Research only. Do not build or edit an app.

Create a deep internal SEO/content/design/business/monetization brief in Hebrew for nad-lan.co.il.

Money priority: we are targeting the hardest, highest-conversion Israeli real-estate keywords, not easy topics. Long-tail articles are only supporting spokes for the big commercial pillars.

Analyze competitor DNA without copying text. Scan SERP and competitor pages, and explicitly show sources/URLs. Focus on:

- yad2.co.il real-estate listing/search experience
- madlan.co.il neighborhood/building/property intelligence
- nadlan.gov.il public transaction/data trust patterns
- homely-mls.co.il and/or winwin/yad1 patterns if relevant
- top Google results for: נדלן, נדלן להשקעה, דירות למכירה, דירות להשקעה, השקעות נדלן, נדלן מסחרי, התחדשות עירונית, דירות חדשות מקבלן, מחיר דירה, שווי דירה, דירות למכירה בתל אביב, דירות למכירה בירושלים, דירות למכירה בחיפה.

Deliverable: create an internal reusable skill/brief, not public copy. Break the site into 100+ practical pieces if needed:

1. Competitor table with URL, business model, traffic/authority signals if available, strongest pages, design DNA, copywriting style, font/UI style, trust signals, lead capture, monetization paths.
2. Keyword clusters by money priority, intent, page type, funnel stage, and cannibalization risk.
3. Homepage structure: exact sections, order, CTA logic, search/filter modules, trust/data sections, and mobile layout.
4. Pillar page architecture: buying, selling, investment, city pages, neighborhood pages, project pages, price guides, mortgage/financing, tax/legal checklist, urban renewal.
5. Supporting content map and internal linking model.
6. Visual design skill: typography, colors, cards, map/data UI, charts, calculators, listing cards, footer/header, mobile menu, premium feel.
7. Copywriting skill: Hebrew tone, buyer/seller/investor language, no internal SEO language, no AI markers, no long dashes, no copied competitor text.
8. Business/revenue model: buyer inquiries, seller inquiries, agent/professional directory, project advertising, investor consultations, mortgage/refinance partners, valuation/report products, paid listing upgrades; keep internal mechanics private.
9. CMS/data model: properties, cities, neighborhoods, projects, agents, agencies, guides, transactions, price ranges, calculators, inquiry forms.
10. Implementation checklist for WordPress/Elementor/code theme.
11. Quality gates for live pages: one H1, no duplicate titles, original copy, mobile, LCP, schema only for visible facts, internal terms blocked.
12. Honesty statement: what you verified live, what you inferred, what requires Semrush/paid data or Search Console.

Use web research/tools. Show that you scanned competitors by listing URLs and concrete observations. Save result as a file named nadlan-seo-business-design-skill.md if file creation is available; otherwise paste the full Markdown in chat.
```

## Owner addenda from the same session

- The owner is NOT a real estate broker. The owner is a **practicing Israeli lawyer (עורך דין)** with multiple legal portals, the most successful of which is the wife's family-law site.
- The owner wants knowledge accumulation: every action by any agent must produce a skill or extend one.
- The owner uses Codex CLI as primary (cheaper than Claude on web). Possibly Antigravity. Skills must persist in the repo so all agents can read them.
- The owner authorized scanning of `C:\Users\pro\.codex\generated_images` (Windows, accessible only to Codex on the owner's PC).
- The repo is public. The owner left it to my discretion whether that's OK; my decision is in `security-public-repo.md`.

## Mapping from the prompt to delivered files

| Prompt section | Delivered in |
|---|---|
| 1. Competitor table | `strategy-master.md` §1 + `../docs/research/serp-snapshots-2026-05.md` |
| 2. Keyword clusters | `strategy-master.md` §2 |
| 3. Homepage structure | `strategy-master.md` §3 |
| 4. Pillar architecture | `strategy-master.md` §4 |
| 5. Internal linking | `strategy-master.md` §5 |
| 6. Visual design skill | `visual-design-skill.md` |
| 7. Copywriting skill | `copywriting-skill.md` |
| 8. Business / revenue model | `monetization-lawyer-angle.md` (substantially rebuilt because owner is a lawyer) |
| 9. CMS data model | `strategy-master.md` §9 + `wordpress-content-types.md` |
| 10. Implementation checklist | `strategy-master.md` §10 + `yoast-config.md` + `image-pipeline.md` |
| 11. Quality gates | `strategy-master.md` §11 + `copywriting-skill.md` §3-4 |
| 12. Honesty statement | `honesty-statement.md` |
| (meta) Inter-agent coordination | `../AGENTS.md` + `agent-coordination-protocol.md` |
| (meta) Public-repo security | `security-public-repo.md` |
| (meta) File name requested | `strategy-master.md` is the primary deliverable; a top-level symlink-style note in `README.md` points there. The file name `nadlan-seo-business-design-skill.md` requested by the prompt was renamed to `strategy-master.md` for repo clarity — same content. |

---
_Preserved 2026-05-28 by Claude Code (claude-opus-4-7)._
