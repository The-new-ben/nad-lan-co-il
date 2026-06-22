# Lovable Master Prompt - NadLan Product War Room

Paste this into the Lovable project.

```text
You are building a premium real-estate product prototype for NadLan.co.il. This is not a generic landing page. It is a visual/product operating system for an Israeli real-estate portal with buyer tools, new-project showrooms, professional marketplace, legal/tax authority, and international buyer support.

LANGUAGE AND DIRECTION
- Primary UI language: Hebrew RTL.
- Also prepare structure for English, French, Russian, and Arabic versions.
- Public copy must never expose internal words like lead funnel, CRM, debug, test, staging, QA, implementation, plugin, prompt, or automation.

AUDIENCE
- Israeli apartment buyers.
- Israeli and foreign investors.
- Families evaluating projects and neighborhoods.
- Developers/contractors who may pay for premium project pages.
- Brokers, lawyers, mortgage advisors, appraisers, and real-estate professionals.
- Foreign buyers who need English/French/Russian/Arabic guidance.

NOT THE AUDIENCE
- Internal agents.
- Developers reading implementation notes.
- SEO operators.
- "Lead funnel" or "CRM" viewers.

DESIGN SYSTEM
- Typography: Heebo for UI/content, IBM Plex Mono for metrics and technical labels.
- Colors:
  - Brand blue: #1561D8
  - Ink: #0B0F14
  - Background: #F5F7FA
  - Success: #0E7C66
  - Warning/gold: #B57700
  - Danger: #B5311B
  - Surface: #FFFFFF
  - Border: #D9DEE7
- Style: premium, product-grade, calm, data-rich, not a marketing-only hero.
- Avoid beige/brown one-note palettes and generic SaaS gradients.
- Use real estate product language: maps, project cards, unit cards, legal trust, price estimates, source dates.

CORE RULES
- No fake facade.
- No fake listings.
- No silent fallback.
- No dead buttons.
- No internal public copy.
- No hidden broken states.
- If an official asset is missing, show a clear missing state.
- If an asset is generated/conceptual, label it: "הדמיה מקורית להמחשה - לא חומר רשמי".
- If an asset is official, label it: "חומר רשמי מהיזם".

BUILD A STATIC VISUAL GALLERY, NOT A PRODUCTION APP
Create a route/page called /gallery or a home screen that displays a navigation sidebar and the following 15 screens. Each screen must be responsive and visually polished at desktop/tablet/mobile.

SCREENS TO BUILD
1. Homepage hero/product board:
   - Search entry.
   - Main paths: דירות, פרויקטים חדשים, מחשבונים, בעלי מקצוע.
   - Trust line with lawyer-owned real-estate guidance.
   - No fake listing counts.

2. Search results / listings map-list:
   - Split map/list desktop.
   - Mobile list/map toggle.
   - Filter chips.
   - Empty/missing inventory state.
   - Listing cards with image, price, rooms, sqm, source, updated date.

3. Listing detail:
   - Gallery, facts, map, contact card.
   - Source/verification label.
   - No fake seller claims.

4. Projects hub:
   - Cards for Rainbow, Dimri Yama, and future projects.
   - Each card shows asset state: official/concept/missing.
   - Strong CTA to view project.

5. Project showroom hero:
   - Short SEO intro above the product.
   - 3D context model area on one side.
   - Facade/unit picker nearby.
   - Selected apartment card.
   - On mobile: intro -> model -> picker -> selected card.

6. Facade/unit picker:
   - Use a premium bitmap/render placeholder surface, not CSS squares.
   - Overlay clickable polygon-like apartment zones.
   - Status colors: available green, reserved gold, unavailable muted/red.
   - Support multiple buildings/compound.
   - Include dismiss/collapse control for mobile.

7. Selected apartment card:
   - Unit name, floor, rooms, sqm, balcony, view, direction, price estimate.
   - Price label: "אומדן לא מחייב".
   - Actions: פרטים, מבט מהדירה, סיור בדירה, דברו עם נציג.
   - Dismiss button.

8. View from apartment / Mapbox state:
   - Map/lookaround panel.
   - Sea/park/context labels.
   - If map is unavailable, show visible error state, not a dead button.

9. Interior tour / Matterport-style state:
   - Tour iframe/card placeholder.
   - Floor plan / room journey.
   - Missing state if no tour exists.
   - Public label if generated concept.

10. Price/investor panel:
   - Price estimate range.
   - payment/financing hints.
   - non-binding disclaimer.
   - source/date rows.

11. Sde Dov district page:
   - project comparison.
   - map/transport/parks/schools.
   - links to Rainbow and Dimri.

12. Professional directory:
   - balanced categories: lawyers, mortgage advisors, appraisers, contractors, brokers.
   - verified profile cards.
   - no taxonomy imbalance.

13. Join Pro:
   - packages and benefits.
   - clean commercial copy.
   - no WooCommerce debug/checkout/coming-soon leakage.

14. Legal/tax guide:
   - lawyer byline.
   - source dates.
   - disclaimer.
   - guide layout with headings above paragraphs.

15. International buyer page:
   - EN/FR/RU/AR language cards.
   - legal/tax/process sections.
   - contact path by language.

COMPONENTS TO CREATE
- Header and mobile nav.
- Search bar.
- Filter chips.
- Listing card.
- Project card.
- Showroom shell.
- 3D model placeholder state.
- Facade picker component.
- Unit polygon/cell overlay component.
- Selected unit card.
- Map/view state.
- Interior tour state.
- Missing/error state.
- Price estimate block.
- Lead/contact card.
- Professional card.
- Legal article block.
- QA status panel.

RESPONSIVE RULES
- Desktop 1440: use side-by-side model + facade/picker where possible.
- Tablet 768: stack but keep model and picker close.
- Mobile 390: guided vertical journey, no overflow, no overlapping floating UI, all controls at least 44px tap target.
- Headings sit above paragraphs, not offset sideways.

OUTPUT EXPECTATION
Give a complete visual/product prototype. If you need to ask questions, ask only after building a first static version using the assumptions above. Use realistic Hebrew copy, but do not invent official prices or official assets. Mark unverifiable facts as estimates or missing.
```
