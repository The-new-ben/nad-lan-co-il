# Proof table: /environmental-hazards/ against every competitor (HAD-670 R13f, 3.11.2026)

Ben, 3.11.2026: "an honesty statement, compare it, prove everything". The rubric is the research agent's, set **before** our page existed
(`competitors.md`, "Scoring"). It has 12 criteria, each scored 0, 1 or 2, for a maximum of 24. Our page is scored on the same rubric, on the live page
https://nad-lan.co.il/environmental-hazards/ (page 8768). It was pressed in real Chrome at 390 and 1366 px (`docs/qa/hazards/press-live.json`).

| Page | Words | Tool | Tables | Maps | Sources | Prices | Pros | Langs | FAQ | Hazards | IL | RE | **Total /24** |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| **nad-lan /environmental-hazards/ + /en/** | 2 (5,794 he + 5,689 en words) | 2 (5 own tools, he + en) | 2 (article tables + antenna and city tables) | 2 (own 3D map, 8 layers) | 1 (named and dated, not linked in text) | 2 (survey and inspection ranges) | 0 (professions explained, no list of named pros yet) | 1 (Hebrew and English, hreflang pair) | 2 (17 he / 16 en, FAQPage) | 2 (8 hazard layers) | 2 (law, thresholds, 8,531 measured sites) | 2 (central) | **20** |
| [spectrum.fit](https://www.spectrum.fit/מפת-אנטנות-סלולריות/) | 1 | 2 | 1 | 2 | 1 | 0 | 0 | 0 | 2 | 0 | 2 | 0 | **11** |
| [midrag](https://www.midrag.co.il/Content/Tip/5238) | 1 | 0 | 0 | 0 | 0 | 2 | 2 | 0 | 1 | 1 | 1 | 1 | **9** |
| [tnuda.org.il](https://www.tnuda.org.il/אנטנות-סלולריות) | 2 | 0 | 2 | 0 | 1 | 0 | 0 | 1 | 0 | 0 | 2 | 0 | **8** |
| [norad4u](https://www.norad4u.co.il/knowledge-h/cellphone-antennas/cellphone-antenna-maps/) | 1 | 1 | 0 | 1 | 2 | 0 | 0 | 0 | 0 | 1 | 1 | 0 | **7** |
| [cellular.wmh](https://cellular.wmh.co.il/) | 0 | 2* | 0 | 2* | 1 | 0 | 0 | 0 | 0 | 0 | 1 | 0 | **6*** |
| [afikil](https://afikil.co.il/real-estates/בדיקת-אנטנות-סלולריות-ליד-בית-מה-לבדוק/) | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 2 | **3** |
| [RFNSA, Australia](https://www.rfnsa.com.au/) (world reference) | 1 | 2 | 0 | 2 | 2 | 0 | 2 | 0 | 0 | 0 | n/a | 0 | **9 of 22** |
| [US EPA EJScreen](https://www.epa.gov/ejscreen) | the tool was taken down (404); a volunteer rebuild exists | | | | | | | | | | | | **n/a** |

\* Claimed by the page; not verified (JavaScript only).

## What only this page has (checked against every row above)
- **One address, every published hazard:**
  - antennas, each with its measured share of the health threshold;
  - pending antenna permits;
  - high-voltage lines, substations and power plants;
  - reporting plants by sector;
  - fuel stations, soil sites and air stations.
  - All of them come with distances, at radii from 100 m to 1 km.
- **Comparing two addresses** side by side.
- **By city:** 779 places, each with antennas, the median and highest measured share, plants and fuel stations.
- **A check planner** with the professions and their published prices.
- **An honesty statement:**
  - the page shows distance, not exposure;
  - there is no official safe distance;
  - "no mark" does not mean "no hazard".
- **A data correction nobody else made:** the Ministry of Energy register's own coordinates are about 77 m off. We place every station from its ITM grid coordinates, checked to about 1 m against the Tel Aviv-Yafo address layer.

## Honest gaps (they stay visible)
- **Languages:** Hebrew and English since 4.11.2026 (https://nad-lan.co.il/en/environmental-hazards/), so we score 1. A third language would make it 2.
- **Professionals:** the professions are explained, but no list of named, licensed professionals exists yet. The sponsor slot is ready for one.
- **Sources:** named and dated on the page, but not linked in the text (the house rule). The repo holds `facts.json`: 117 facts from 43 source documents.
- **Not mappable today:** transformer rooms, pipelines, airport noise contours, live air values, seismic data and radon. None of them is open data; the page says so.
