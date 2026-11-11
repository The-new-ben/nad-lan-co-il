# Slug for the apartment design hub (HAD-701)

Audit run 10.11.2026 with `python C:\Users\777\Documents\GSC-Data\tools\url_word_audit.py --token <word>` against the live sitemap (4,665 URLs). Raw output: `url-word-audit-raw-2026-11-10.txt`. Cross-checked against the 4,664 URLs pulled from `https://nad-lan.co.il/sitemap_index.xml` the same evening.

Owner rules applied: English URL segments; a word never appears twice in one URL; a new URL never re-uses a head word (first word of the path) that an existing URL owns. No redirect is proposed for anything.

## Token audit

| Token | URLs holding it | Is it the head word of an existing URL? | Verdict |
|---|---:|---|---|
| apartment | 106 | **yes**: `/apartment-prices/`, `/apartment-deal-check/`, `/apartment-buying-checklist/`, `/apartment-purchase-cost-calculator/` | cannot lead the new slug |
| interior | 2 | **yes**: `/interior-design-trends-2026-israel/` | cannot lead the new slug |
| design | 3 (`/interior-design-trends-2026-israel/`, `/glossary-category/interior-design/`, `/professionals/demo-dana-barak-design/`) | no (always second word or later) | free as a head word |
| designer | 2 (both the BSR Sarona rental listing) | no | free as a head word |
| planner | 2 (`/glossary/last-planner-system/`, `/professionals/demo-amit-ron-planner/`) | no | free |
| home | 3 | **yes**: `/home-inspection/` | cannot lead |
| price | 1 | **yes**: `/price-list-dubai/` | cannot lead |
| cost | 2 | no | free, but better kept for a child page |
| renovation | 1 | **yes**: `/renovation-contractor/` | cannot lead |
| plan | 1 (`/tel-aviv-plans/neve-avivim-plan/`) | no | free |
| room | 8 (listings) | no | free |
| studio, 3d, styling, consultation, decor, kitchen, living, visualization, layout, floor | 0 | no | free |

Also noted: `/tour/designer/` exists (HTTP 200, noindex, not in the sitemap, so the audit does not see it). It is the current designer demo.

## Options

### 1. Recommended: `/design-planner/`

- Head word `design` is not the head of any existing URL; `planner` is never a head word either. No word repeats.
- It names both halves of the page: design (`עיצוב דירה`) and the planning engine (`תכנון דירה`, `כלי תכנון אונליין`, `Home Planner`, IKEA `planners`, all on page 1 of the tool queries; see serp.md).
- Clean children later, without breaking the one-word-once rule: `/design-planner/kitchen/` (תכנון מטבח), `/design-planner/living-room/` (עיצוב סלון), `/design-planner/small-apartment/` (עיצוב דירה קטנה), `/design-planner/designer-cost/` (מחיר מעצבת פנים), if any of these ever earns its own page.

### 2. `/designer/`

- One word, free as a head word, short in the SERP.
- Same word as the existing demo `/tour/designer/` and as the `/tours/` H2 `מעצב הדירות`, which ties the brand of the engine together.
- Risk: two live URLs ending in `designer` (one noindex). Fine for Google today, but the owner may see it as a second designer page. Children would read `/designer/kitchen/`, `/designer/designer-cost/` (repeats a word, not allowed), so price children need another word (`/designer/fees/`).

### 3. `/design-studio/`

- Free head word, no repetition. `סטודיו` is how Israeli designers name their firms (סטודיו לעיצוב פנים) and redesignai calls its planner `סטודיו שרטוט`.
- Risk: in Hebrew real estate `סטודיו` also means a studio apartment (`עיצוב דירת סטודיו קטנה` is a related search on `עיצוב דירה קטנה`). Ambiguous.

### Rejected

- `/apartment-design/` and `/apartment-designer/`: literal match to `עיצוב דירה`, but `apartment` is the head word of many existing URLs.
- `/interior-designer/` and `/interior-design/`: `interior` is the head word of `/interior-design-trends-2026-israel/`, and `interior-design` is already the glossary category slug.
- `/home-design/`: `home` is the head word of `/home-inspection/`.
- `/design-price/` or `/price-...`: `price` leads `/price-list-dubai/`, and price is one section of the hub, not the hub.

Before publishing, run `url_word_audit.py --token design` and `--token planner` again in case another agent mints a URL in the meantime.
