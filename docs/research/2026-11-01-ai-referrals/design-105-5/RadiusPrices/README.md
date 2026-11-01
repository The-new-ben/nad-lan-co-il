# RadiusPrices

**What it is:** the price list around a project. It answers the question a buyer and an AI assistant both ask: what apartments really sell for around this building. It has three parts, each with its source and its period:
1. **The deals around the project.** Apartment deals reported to the Tax Authority within 500 m of the project:
   - the median price per m²;
   - the median by rooms;
   - the median by year;
   - the latest deals.
2. **The official price in the neighbourhood.** The median deal price by rooms, as nadlan.gov.il publishes it for the official neighbourhood, with its quarter.
3. **The projects around.** The developer projects within about 1.5 km, side by side:
   - the developer;
   - the stage;
   - units and floors;
   - the distance from this project.
   Each one links to its page.

**Version 105.5** (1.11.2026, the HAD-654 radius loop). Ben asked for "tools, price lists around, a lot of data and numbers, everything that attracts ChatGPT". The GA4 evidence: ChatGPT cites the pages that carry a dated price per m² with a source (Rainbow 55 mentions, 19 AI visits). Pages without one get none.

## Where
- **The base Hebrew page of every developer project in the radius:** Sde Dov, Einstein (Ramat Aviv and Neve Avivim), Kochav HaTzafon, Shikun Lamed, then Herzliya.
- **Placement:** at the end of the article, right before the ProjectToolkit. It is never inside a stage, and nothing is removed.
- **Not on Ashira** (Ben). Ashira may appear as a card among the projects around another project; that only links to it.

## Anatomy
- **Kicker:** "<neighbourhood> · מחירים מסביב".
- **H2, serif:** "מחירי הדירות סביב <project>". The project's name leads, so the block never competes with the city price pages.
- **Intro line, 15px ink2:** "העסקאות שדווחו לרשות המסים ברדיוס 500 מטר מהפרויקט, והמחיר הרשמי בשכונה."
- **Tiles** (`nlrp__sum`), each a serif number and a one-line source with its period:
  - the median per m² around the project, and the number of deals;
  - the official median price in the neighbourhood, with its quarter;
  - the median for the most common room count.
- **By rooms:** a small table, rooms / median per m² / deals. A row with fewer than 5 deals shows the count without a median.
- **By year:** bars of the median per m², with the number of deals under each bar. The years are drawn only where there are 5 deals or more.
- **The latest deals:** a real table of street and number, rooms, m², floor, price, per m² and month.
  - On a phone each row becomes a card.
  - A deal in a new building carries a small "דירה חדשה" chip, only when the Tax Authority marks it so.
- **The projects around:** cards with the name (serif), the developer, the stage chip, units and floors when known, and the distance in metres or km. Nearest first.
- **Closing note, 12.5px:**
  - the sources (Tax Authority deals as published by nadlan.gov.il, and the Tel Aviv-Yafo address layer);
  - how per m² is computed (the price divided by the registered area);
  - "חציון מוצג רק כשיש 5 עסקאות לפחות".

## Honesty
- **Every number carries its period.** The deals file runs to the month printed. Nothing is extrapolated to today.
- **No deal is moved.** A deal that cannot be placed on the map by its block and parcel is not counted.
- **The block never estimates the project's own price.** That stays with the developer's published figure, in the facts.
- **No buyer names.** No judgement words such as "זול" or "הזדמנות".
- **Unknown = omitted.** An area without enough deals (the new Sde Dov plots) shows the nearest official neighbourhood, named as such, and the deals within 500 m. If there are fewer than 5, the deals part is not drawn.

## Data
- `tools/deals/build_radius_prices.py`: deals within 500 m, by block and parcel. Output `radius-prices-v1.json` keyed by project id.
- The official neighbourhood files: `data.nadlan.gov.il/api/pages/neighborhood/buy/<id>.json`. These are public, need no token, and are the same files the government site loads.

## Look
- **Skin A tokens.** The tiles and chips take a cool tint of the sea colour (`color-mix(sea 9%, white)`), not the sand. Ben's law of 13.10 rules out a cream or beige ground. This block reads like a map legend and a price ledger: sea blue, ink, white.
- **Figures:** IBM Plex Mono, tabular. A unit (מ׳, ק״מ, ₪) sits outside the left-to-right number span, so it reads in Hebrew order.
- **The year chart runs left to right** (2020 to 2024), the way Israeli price charts run.
