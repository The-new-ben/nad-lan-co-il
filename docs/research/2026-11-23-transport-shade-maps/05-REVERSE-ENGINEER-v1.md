# 05 - Reverse engineering for the transit map v1 (HAD-816, 23.11.2026)

Public material only. Read 23.11.2026. "Checked how": Google page one by hand in Ben's Chrome (screenshots in serp/), the page itself through a fetch, or the 02-WORLD-BENCHMARK.md documentation (not pressed).

| Feature | Moovit / Google Maps | Zoopla / Realtor.com (TravelTime) | SeLoger | NTA nta.co.il | tevelmetro.co.il (operator) | derechkala.online | telavivmetro.org | gov.il metro system map (Planning Admin.) | **Us, v1 /transit/** |
|---|---|---|---|---|---|---|---|---|---|
| Every line of Gush Dan on one map (Red, Purple, Green, M1-M3, rail) | yes (running lines only) | no | no | per-line maps + PDF | Red only | Red; Green/Purple pages | static image + PDF | Metro + light rail + rail (planning layers) | **yes, switchable** |
| Status in words per line (running / under construction / planned) | no | no | no | yes | n/a | yes | yes | statutory stage | **yes, from official data, GTFS for "running"** |
| Opening dates | no | no | no | yes (own site, not readable to us: Cloudflare check) | n/a | yes, no source | yes, "estimated", no source | no | **no: none verified from an official source today (omitted, not guessed)** |
| Station list per line | yes | no | no | yes | yes, by city | yes, per station pages | yes (Red) | yes | **yes (server-printed lists + map)** |
| English | yes | n/a | n/a | yes | ? (403) | no | yes | partly | **yes /en/transit/** |
| Search station | yes | n/a | n/a | ? | city filter | origin/destination | no | address search | **station, project, address (Photon/OSM)** |
| Nearest station from a point | trip planner | n/a | n/a | no | no | "my location" | no | measure tool | **nearest station on every line from a project or an address** |
| Walking-minute rings around a station | no | isochrones (paid engine) | yes (commute) | no | no | no | no | no | **5/10/15 min rings (estimate, labelled)** |
| New projects around each station | no | listings by commute | listings by commute | no | no | no | no | parcels only | **yes: 900+ catalogue projects, minutes per station, links to project pages** |
| "Projects within 10 min of a station" table | no | no | no | no | no | no | no | no | **yes, server-printed (Google and AI answers can read it)** |
| Sources and date on the page | no | no | no | own | own | disclaimer only | "updated 21.11.2026" | official | **yes: dataset names, dates, GTFS date, checked date** |
| Map does not hold the page's scroll on a phone | app | ? | ? | ? | ? | ? | image | ArcGIS (captures) | **two-finger move on phones, wheel on intent** |
| Timetable / trip planning / real time | yes (the bar) | no | no | no | yes | yes (estimates) | links | no | **no (v1). Phase 2-3 in 04-PLAN-HE.md** |
| Travel time door to door, couples | trip by trip | yes | yes (2 workplaces) | no | no | no | no | no | **no (v1). Phase 3** |

Where v1 is behind: trip planning and real time (we link out, never compete with Moovit), door-to-door commute time (phase 3, needs a precomputed graph or a paid engine: Ben's cost decision), official opening dates (NTA site blocked automated and agent reading today; next round reads it by hand).
Where v1 is ahead of every Israeli page found: projects around stations with walking minutes, a dated source line, rail + light rail + Metro in one map with honest status words, English twin.
