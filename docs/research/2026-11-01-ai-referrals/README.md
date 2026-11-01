# Why ChatGPT sends visitors to Rainbow (1.11.2026)

## Source
GA4 property 539731843 (nad-lan.co.il), read in the gmktec Chrome on 1.11.2026 16:00. Range 1.6-31.10.2026.

## Channels
- Total sessions: 3,849.
- Google organic: 1,999.
- Direct: 1,336.
- AI Assistant channel: 282 (7.3%).
  - chatgpt.com 246, plus 16 more counted as Referral.
  - gemini.google.com 19.
  - perplexity.ai 13.
- Bing organic: 49. ChatGPT search leans on the Bing index, so the Bing number matters.
- Key events configured: 0. A WhatsApp click is not counted as a lead, so we cannot yet prove leads from AI visitors.

## AI landing pages (114 pages in total)
Projects:
- /projects/rainbow-tel-aviv 19
- /projects/hamedina 8
- /projects/dimri-yama-sde-dov 6
- /projects/zohi-sde-dov-en 4
- /projects/ashira-sde-dov 3
- /projects/gindi-vogue-sde-dov 1
- /projects/utopia-sde-dov-ar 1

Meital's listings, together about 60:
- nofei-yam 19 + 6 + 4
- bsr-sarona 8 + 4 + 3 + 1
- tzukei-aviv 8 + 2
- herzliya-pituach-private-estate 6 + 4
- ramat-aviv-5-rooms-pool 5 + 3
- kochav-hatzafon mini penthouse 3
- migdalei-neeman 3 + 2

Other pages:
- /developer-deals 7
- /commercial-real-estate/* about 30 in total
- /en/sde-dov/contamination 3, with 4 minutes on page
- registry compounds: about 30 pages with 1 visit each

## What the cited pages share (raw HTML of 20 radius pages, `score.json`)
- **Price per sqm, many times, with a source:**
  - Rainbow 55 mentions, Hamedina 63, Ashira 41, Dimri 40.
  - Pages with 3-5 mentions get 0 AI visits: Akirov, Einstein 19, YOO, Park Bavli, Ashdar Einstein, Recanati, Marina.
- **A dated line with named sources.** Rainbow opens "עודכן בספטמבר 2026 · מקורות: ...". Only Rainbow and DUO carry a date.
- **FAQ in schema** that answers the questions people type into ChatGPT: where, who builds, how many units and floors, the stage, delivery, apartment types. Rainbow has 10.
- **ApartmentComplex schema:**
  - geo coordinates;
  - sameAs links to the developer's own sites;
  - an AggregateOffer with a sourced price range (5.5M-16M, 75-92 thousand per sqm, "estimate").
- **A strong entity:** Israel Canada plus Sde Dov, which people already ask about by name.
- **Listings win** because they are specific: an address, rooms, a price and a real photo.

## Defects found
- Rainbow says 459 units in the text and 480 in the schema (numberOfAccommodationUnits). Fix it to the developer's figure.
- 8 radius pages have no language versions: einstein-19, ashdar-einstein, akirov-towers, first-sde-dov, marina-towers-herzliya, h-infinity, einstein-tower, migdalei-hayam.
- No FAQ in schema on DUO, H Infinity, Einstein Tower, Shikun Binui, Migdalei HaYam and Ashira. Ashira: do not touch.
