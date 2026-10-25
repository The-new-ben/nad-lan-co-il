# MyPlace (Tel Aviv boutique brokerage + marketing) - "פרויקטים חדשים"

- URL: https://www.myplace.co.il/פרויקטים-חדשים/
- SERP: #4 for "פרויקטים חדשים תל אביב" (serp.md, 25.10.2026). Not in the top 8 for "פרויקטים חדשים".
- Retrieved: 25.10.2026 07:34 UTC (09:34 Israel), curl with a Chrome UA, server-rendered WordPress (Yoast). Raw: `raw/myplace.html` (+ `raw/myplace-llm-view.html`).
- Freshness: article:modified_time 2023-11-14 (stale for two years and still ranking).
- Title: `פרויקטים חדשים בתל אביב | פרויקט מגורים ת״א נכסים שווים ← MyPlace`
- Meta description: invites searchers looking for new-project apartments in Tel Aviv, promising variety, attractive prices and a unique buying experience, with a contact CTA.
- H1: `פרויקטים חדשים בתל אביב`
- Visible words: ~790 total; ~650 main content (intro checklist ~280, cards, 3 area blurbs ~170).

## Heading outline
- h1 פרויקטים חדשים בתל אביב
  - h3 x12 project cards: במדרחוב הולנדי בקרבת פארק הירקון / יונתן הופסי – דירות יוקרה צמוד לפארק הירקון / פרויקט מגורים בצפון הישן והאיכותי של תל אביב / פרויקט יוקרתי ליד הים ומרינת תל אביב / אדריכלות נצחית בלב רובע 5 / פרויקט באוהאוס בסמטה שקטה מרוטשילד / ברחוב לוי יצחק בוטיק בלב רובע 3 / יהלל. זה כל הסיפור. / פרויקט חדש בקו הראשון לפארק הירקון / גן עדן על הפארק / בודנהיימר לחיות היכן שהשקט והיוקרה נפגשים / פרויקט בוטיק בקרבת כיכר דיזנגוף
- h2 פרויקטים חדשים בצפון תל אביב היוקרתי
- h2 אזור שוקק חיים ומלא בעושר במרכז תל אביב
- h2 דרום תל אביב – אורבניות גולמית לצד איכות חיים קפדנית

## Sections in order
1. Breadcrumb (MyPlace > פרויקטים חדשים).
2. Intro: buying from a project differs from second-hand; a 4-point due-diligence checklist (who is the developer/contractor, Sale Law guarantee, technical spec and customisation, timelines and permit stage) each tied to "we can check this for you".
3. Advanced search panel (filters, see tools).
4. Listing grid: 12 cards. Each card = permit/stage badge, project tagline as the title, city, area, sometimes street, "view project". Lazy "load more" (ends with "no more projects").
5. Three short area blurbs: north, centre, south Tel Aviv (generic, no data).
6. Footer contact + lead form, WhatsApp, "Hey AI, learn about this page" link (?llm_view=1).

## Data points published
- 12 Tel Aviv projects, no prices, no unit counts, no developer names, no delivery dates.
- Stage badges as data: "התקבל היתר בניה" x7, "בהליך רישוי מתקדם" x2, "הבניה החלה" x1, "הפרויקט בביצוע" x2.
- Areas used: Old North (7), near the sea (1), Lev Hair (2), city centre (2). Streets named: Yonatan Hofsi, Rothschild Blvd, Rav Levi Yitzhak, Yahalal, Bnei Dan (x2), Bodenheimer; landmarks: Yarkon Park, Marina, Dizengoff Square, Rova 3, Rova 5.
- Mentions the Sale Law guarantee (ערבות חוק מכר) and permit stages as purchase checks.

## Tools / interactive
- Filter panel: listing type (all / properties / from projects), area (9: city centre, Lev Hair, Old North, near the sea, east, south, Jaffa, Neve Tzedek, northern neighbourhoods), property type (10: apartment, rooftop, garden, penthouse, mini-penthouse, tower apartment, project apartment, luxury, private house, plot/building), features (8: new/renovated building, parking, elevator, balcony, new/renovated, storage, yard, pool), price slider 0-20M NIS, rooms 1-10, "find me a property".
- Favourites (heart) list, "let us search for you" service page, WhatsApp, phone.
- No map, no calculator, no compare, no alerts.

## Structured data
- JSON-LD (Yoast): WebPage, WebSite (+SearchAction), BreadcrumbList. No ItemList, no FAQPage, no listing types. hreflang he/en/fr.
- GEO trick: footer link to an "LLM version" of the page (?llm_view=1). With a browser UA it returns essentially the same HTML (no noindex seen).

## FAQ questions
- None.

## Internal linking
- ~32 unique internal links: 12 project pages (/projects/...), sale/rent/luxury city pages, magazine, video gallery, media, about, "seller?" page, EN/FR versions. No developer pages, no other-city pages.

## Judgement
- Ranks for the Tel Aviv query on exact-match h1/title, a tight Tel Aviv-only grid, and brand/locality signals (Tel Aviv office, EN/FR versions). Intent match is good for buyers who want a shortlist.
- The permit-stage badge on each card is a useful, rare data point (most rivals show only "in marketing").
- Weaknesses: two-year-old content, no prices, no developers, no dates, generic area text, no FAQ, no schema beyond breadcrumbs, card titles are slogans not project names.
- Beatable easily on depth and freshness; worth copying the idea of a visible permit/stage badge and a due-diligence checklist next to the grid.
