# Homepage Specification

## Primary job

The homepage must look like the entrance to a functioning national portal, not a presentation about a product under construction. It should route real user intent into projects, properties, areas, data, tools and professionals while establishing image quality, freshness and institutional confidence.

## First-viewport requirement

At desktop 1440px, the first viewport contains:

- truthful utility/freshness strip;
- NadLan header with clear roots;
- wide approved real-estate hero image;
- concrete Hebrew H1;
- buy/rent/new-project/professional intent tabs;
- one location/project/developer search input and one primary action;
- a restrained quick-proof row such as “מידע מאומת”, “תוכניות”, “סיורי 3D” only when each item links to real inventory.

At mobile 390px, the hero retains the image, H1, intent tabs and search without horizontal overflow. The navigation collapses to one accessible menu; no ticker marquee, chat stack or map occupies the first screen.

## Recommended Hebrew copy

**H1:** פרויקטים ודירות בישראל — רואים, משווים ובודקים לפני שפונים
**Supporting line:** חיפוש לפי עיר, שכונה, פרויקט או יזם, עם תמונות, תוכניות, מידע עדכני וכלים לקבלת החלטה.
**Input label/placeholder:** עיר, שכונה, פרויקט או יזם
**Primary action:** חיפוש
**Secondary action:** הצגת פרויקטים על המפה

Avoid leading with “3D,” “AI,” “the future of real estate” or process explanations. These are capabilities, not the user's first intent.

## Zone-by-zone contract

### 1. Market utility strip

**Content:** up to four sourced current figures or service signals, each with an as-of date and link.
**Fallback:** if no fresh, approved values exist, show non-numeric utility links such as “עסקאות אחרונות”, “מחירי אזורים”, “מחשבון מס רכישה”, “מדריך קנייה”.
**Never:** stale figures, invented market averages or an automatic moving marquee that is difficult to read.

### 2. Header and mega navigation

Root destinations:

- דירות
- פרויקטים חדשים
- אזורים ומחירים
- מדריכים וכלים
- אנשי מקצוע

Utilities: HE/EN, saved items, account, developer/project completion. Mega panels are composed from WordPress menus and real destination records. Hover, focus and mobile-expanded states must all work.

### 3. Search hero

**Media:** approved photographic/rendering asset with stable crop and readable text overlay; no sketch as the default.
**Search:** GET-driven, server-readable and progressively enhanced with the existing suggestion endpoint.
**Tabs:** buying, renting, new projects, professionals.
**Popular links:** at most six real city/compound links derived from approved records.

### 4. Trust/current snapshot

Four concise cards, chosen from:

- last verified project updates;
- recent transaction/area data;
- approved project count;
- working floorplan/3D inventory;
- named source/verification explanation.

Every number is computed, dated and clickable. If a value is not current, the card collapses rather than displaying a marketing estimate.

### 5. Featured projects

Three large image-first project cards using the canonical project-card contract. They must represent distinct projects, not language variants. One promoted slot is allowed and visibly labelled. Homepage rendering uses a fast poster; any 3D opens on click or in the project page.

### 6. Active inventory

Two tabs: projects and properties (or buy/rent if the property inventory is ready). Show six to eight cards at desktop and a swipe/stack pattern at mobile. Include “view all” and saved-search actions. Do not publish this band with demo or image-less records.

### 7. Cities and compounds

Six to eight image/map-thumbnail cards. Each contains:

- place name;
- verified project/property count;
- one approved current data point or descriptive line;
- link to a true hub page.

Avoid decorative city cards that lead to empty archives.

### 8. Recently verified

This is NadLan's visible freshness differentiator. Cards/rows show the most recently rechecked records with a plain label such as “המידע נבדק בתאריך …”. “New” describes publication/lifecycle; “recently verified” describes data quality. They are not interchangeable.

### 9. Market intelligence and tools

Lead with tools that solve active buyer questions: price/area exploration, purchase-tax, mortgage, affordability, glossary and comparison. Data cards show source/date. Tool CTAs lead to real pages, not modal dead ends.

### 10. Guides and named expertise

One lead story, four compact current items and evergreen buyer guides. Each item shows category, headline, date and author/editorial owner. The band appears only when the freshness threshold is met; stale filler is worse than no band.

### 11. Foreign-buyer entry

Dark/high-contrast band with English as the primary alternate language, supported by Hebrew context. Promise only operational capabilities:

- English project records;
- currency and unit display;
- remote viewing/contact;
- process and total-cost guidance;
- named response owner.

Primary CTA: `Explore projects in English`. Secondary: `How buying in Israel works`.

### 12. Institutional footer

Six CMS-owned columns linking cities, compounds, projects, data, tools, professionals, languages, company/legal/contact. Include a plain source/estimate disclaimer and accessible labelled contact actions. The footer should feel complete but never contain fabricated scale statements.

## Homepage content density target

The page should expose many useful destinations while keeping each visual band legible:

- 3 featured project cards;
- 6–8 inventory cards;
- 6–8 city/compound cards;
- 4 recently verified rows/cards;
- 5–7 tools;
- 5–6 editorial/guide items;
- 4 professional categories or verified profiles;
- a comprehensive menu/footer graph.

The goal is not an arbitrary link count. Every link must lead to a real, useful destination. Empty hubs do not count as authority.

## Image rules

- Hero: 16:9 or wider, approved source, art-directed crop.
- Project cards: consistent 4:3; first image is the official project hero.
- City cards: real licensed place image, verified map crop or neutral honest missing state.
- Offscreen images: responsive and lazy-loaded.
- LCP hero: not lazy-loaded; reserve dimensions and provide responsive variants.
- Text is HTML, never baked into the source image.
- Every image has language-appropriate alt text and a provenance/rights record.

## States

| State | Required behavior |
| --- | --- |
| Loading | Stable reserved layout; no card jump |
| Empty band | Band collapses and adjacent spacing normalizes |
| Missing image | Dignified neutral state, not a random stock/project image |
| Stale project | Remove volatile values/badges; keep page only if identity/source remain trustworthy |
| Error | Plain retry/fallback link; never a blank band |
| Sponsored | Visible label before the user clicks |
| Illustrative | Visible label on the image and in its caption/source state |

## Accessibility and performance acceptance

- WCAG 2.2 AA target.
- Normal text contrast at least 4.5:1; large text at least 3:1.
- Internal product target: at least 44×44px for primary interactive controls, exceeding the WCAG minimum-target rule.
- Logical RTL properties and correct keyboard reading order.
- Visible focus, no hover-only information, labels for icons and form fields.
- LCP ≤2.5s, INP ≤200ms and CLS ≤0.1 at the 75th percentile.
- No page-level horizontal overflow at 390px.
- One initial hero image, no autoplay video or live 3D in the critical path.

## CMS/ownership requirement

Every zone reads WordPress content, taxonomies, menus, options or approved query results. The existing July 2 recommendation for a reorderable `nadlan_home_bands` control remains valid as an implementation direction, but adding/changing fields or code requires separate owner approval. This specification does not perform that work.

## Homepage acceptance gate before external presentation

- All visible projects are distinct, real records and pass the basic-verified state.
- No demo/test label, untranslated duplicate or empty image card is public.
- Every visible number has source/date or is removed.
- HE and EN journeys reach corresponding useful pages.
- Search, card, save/compare and contact destinations work.
- Desktop 1440 and mobile 390 screenshots show no overlap/overflow.
- At least the visible first two project rails use approved external-presentation media.
