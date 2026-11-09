# Teardown: Idealista (obra nueva)

Read attempted on 9.11.2026. **Blocked.**

## What happened
| Page | URL | Result |
|---|---|---|
| New builds, Madrid | https://www.idealista.com/obra-nueva/madrid-madrid/ | WebFetch: **HTTP 403**. Chrome: a **slider CAPTCHA** (DataDome-style: "too many requests", "slide right to continue"). Seen in a screenshot. |

Under the rules we do not solve CAPTCHAs, so this page was skipped. Nothing below was read live this session.

## Known patterns [prior], for the matrix only and not proof
- **Hub structure:** a "Promociones de obra nueva" hub for each city, with cards for whole developments ("promoción"). Units inside a development are listed under it.
- **Development card:**
  - the developer's logo and name
  - "desde X €", a "from" price
  - the unit types available (pisos, áticos, dúplex) and how many
  - a delivery date ("Entrega: [trimestre/año]")
  - energy rating
  - photos, which are often renders
- **Filters:** price, size in m², rooms, type, and "obra nueva" as its own channel. Draw on map ("Dibuja tu zona"). Saved searches and email alerts ("Guardar búsqueda").
- **Data products:** a price-per-m² report by area ("informe de precios") linked from search hubs, and ad stats per listing.
- **Lead form:** name, email, phone and message, with ready-made checkboxes (for example "visit", "more photos"). A first-message template is filled in.
- **SEO:** a city / district / neighbourhood URL tree under `/obra-nueva/` mirrors the resale tree under `/venta-viviendas/`.

## What nad-lan should take (verify before using)
- A **delivery-date field on every project card** (quarter and year), which feeds the occupancy filter.
- A **city / neighbourhood URL tree for new projects that mirrors the resale tree.** Mint any new slug only through `url_word_audit.py`. No redirects: existing URLs stay.

## To finish later
Read again from the owner's own browser session at a calm hour, or use a published secondary source (screenshots or docs). Do not use automation that solves the CAPTCHA.
