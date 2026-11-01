# ProjectFacts

The project's facts in one place, each with its source, under a line that says when they were checked. It is the part of Rainbow's page that ChatGPT quotes. Now every project gets it, in the same order, so a buyer and an assistant find the same answer on every page.

**Version 105.5** (1.11.2026, the HAD-654 radius loop). The GA4 evidence for 1.6-31.10.2026: 282 AI-assistant visits, 246 of them from ChatGPT. Rainbow leads with 19. Its page opens with "עודכן בספטמבר 2026 · מקורות: …" and carries a sourced price per m², FAQ and a facts schema. Pages without these got no AI visits.

## Where
- **Projects:** the base Hebrew page of every developer project, the radius first (Sde Dov, Einstein, Kochav HaTzafon, Lamed, Herzliya).
- **Placement:** at the top of the article, right after the stage and the map. This is the "facts" slot of the content-first order: H1, answer, CTAs, stage, view and map, facts, article. On a page without a stage it follows the lead.
- **Language pages:** the same block, written in their own language.
- **Not on Ashira** (Ben).
- **Einstein Tower:** the block goes after the pinned Hebrew article, never inside it.

## Anatomy
- **The checked line, 13px ink2, first:** "עודכן ב<month year> · מקורות: <names>". The names are the real sources behind the rows below, nothing more.
- **H2, serif:** "<project> במספרים".
- **The facts** are a definition list (`dl`), never a table: the article skin turns tables into cards. Each row is a label, the value in serif, and its source as a small link chip. The order is fixed:
  - היזם;
  - הקבלן המבצע;
  - האדריכל;
  - המיקום (street or plot, neighbourhood, distance to the sea when published);
  - גוש וחלקה או מגרש;
  - דירות;
  - קומות ובניינים;
  - תמהיל;
  - שלב;
  - מכירות;
  - מחיר ממוצע למ״ר, labelled with whose figure it is and its period;
  - אכלוס צפוי;
  - אתר הפרויקט.
- **"שאלות שקונים שואלים":** 6-10 short questions, written the way people type them into Google and ChatGPT, each answered in one or two sentences from the rows above. They are emitted once as FAQPage. If the ProjectToolkit already prints the page's FAQPage, the questions join that one object; there are never two.
- **The schema:** an ApartmentComplex built from the same rows (name, address, geo, numberOfAccommodationUnits, sameAs, an AggregateOffer only for a published price). One source of truth: the number on screen and the number in the schema can never differ again (Rainbow showed 459 on screen and 480 in the schema).

## Honesty
- **A row without a source is not drawn.** Never "לא ידוע" and never "0".
- **A developer's figure is labelled as the developer's** ("לפי דוחות היזם"). A press figure names the paper and the date.
- **The checked month changes only** when the rows were really checked again.
- **No ranking or judging words** ("הכי", "זול").
