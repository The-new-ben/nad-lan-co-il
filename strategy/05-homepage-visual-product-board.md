# Homepage Visual Product Board

Purpose: define the homepage as a product entry, not a generic blog front page.

## Audience

Primary:
- Israeli buyers looking for apartments/projects/tools.
- Investors comparing projects, prices, tax, and financing.
- Foreign buyers who need trust, language support, and legal clarity.
- Contractors/developers who may pay for premium project/showroom pages.
- Real estate professionals who may join the marketplace.

Not the audience:
- Internal agents.
- Developers reading implementation notes.
- "Lead funnel" operators. Do not leak internal funnel language.

## Homepage Job

Within the first screen, users must understand:

1. What NadLan does.
2. Why it is trustworthy.
3. Where to start: search/projects/tools/professionals.
4. That the site has premium product experiences, not only text.

## Reference Patterns

- Zillow: search-led real estate entry, strong listing/tour media, buyer-first paths.
- Homes.com: neighborhood, schools, market insight and Matterport/digital-tour language.
- Rightmove: focused search and category entry.
- Mapbox real estate: map as product, not decoration.
- Premium legal/financial pages: authority, author, date, and disclaimers.

## Design Tokens

Use the exact project token direction from the reset pack, not ad hoc colors.

| Token | Value | Use |
|---|---|---|
| Brand blue | `#1561D8` | links, primary buttons, active states |
| Ink | `#0B0F14` | primary text |
| Background | `#F5F7FA` | page background |
| Success | `#0E7C66` | available/status success |
| Warning | `#B57700` | estimate/disclaimer/high-demand |
| Danger | `#B5311B` | errors/unavailable |
| Surface | `#FFFFFF` | cards/forms |
| Border | `#D9DEE7` | quiet dividers |

Typography:
- Primary: Heebo.
- Technical/metrics: IBM Plex Mono.
- Do not switch to Assistant unless the whole design system is re-approved.

## Homepage Sections

### 1. Search/Product Hero

Must include:
- H1 in Hebrew.
- Search entry.
- Three clear start paths: דירות, פרויקטים חדשים, מחשבונים/מיסוי.
- One trust line: lawyer-owned real estate guidance, with no overclaim.

Avoid:
- giant vague marketing text.
- internal words like leads, funnel, CRM.
- fake map/listing count.

### 2. Project Showroom Teaser

Show Rainbow / Dimri as premium examples:
- 3D model available if real/concept state exists.
- Facade selector only if real/concept asset is present.
- If missing official asset, show honest state.

Public labels:
- "הדמיה מקורית להמחשה" for generated concept.
- "חומר רשמי מהיזם" only when official.
- "ממתין לחומר רשמי" when missing.

### 3. Buyer Tools

Mortgage, purchase tax, property value, yield. Each card links to a real tool or a draft-safe placeholder. Do not publish fake tools.

### 4. District/City Knowledge

Entry to Sde Dov, Tel Aviv, neighborhoods, urban renewal.

### 5. Professionals

Directory teaser with taxonomy balance. Current "mostly contractor" taxonomy is a trust risk and must be corrected before heavy promotion.

### 6. Foreign Buyer Entry

English/French/Russian/Arabic entry cards. Pages can be draft until complete, but homepage should indicate support only when there is a real page.

## Lovable Visual Gallery Plan

Lovable can be used for a static component gallery, but only as a visual sandbox. The source of truth remains this repo.

Route: `/gallery` or local static preview only.

Screens to prototype:
1. Homepage hero.
2. Search results map/list.
3. Listing card system.
4. Project showroom hero.
5. Facade selector state.
6. Apartment detail card.
7. Interior tour state.
8. Map/lookaround state.
9. Missing asset state.
10. Price estimate/disclaimer pattern.
11. Professional directory.
12. Join Pro packages.
13. Legal guide article.
14. International buyer page.
15. QA state board.

Lovable output rules:
- Must be copied into repo if used.
- No hidden Lovable memory as source of truth.
- No product code deploy from Lovable without review.
- Screens must use the same tokens above.
- Every component needs mobile 390, tablet 768, desktop 1440 screenshots.

## Acceptance Criteria

- One H1.
- No Woo/cart/notification leakage.
- No internal terms.
- No fake counts.
- No fake listings.
- Clear public value above the fold.
- Lighthouse/mobile visual QA before publishing major homepage changes.
