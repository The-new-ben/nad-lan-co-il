# Project 3D Sales Experience Skill

Use this when adding or improving an interactive real-estate project model on nad-lan.co.il.

## Standard

- Start with a fast, premium model that can ship without BIM: architectural massing, floor selection, unit selection, and clear inquiry flow.
- The model must be interactive, not a static image. Minimum interaction: drag-to-rotate, floor selection, unit selection, selected-unit facts, and a view/inside preview mode.
- Do not publish invented prices, availability, apartment numbers, or floorplans. If data is illustrative, label it clearly and render price as `לפי פנייה`.
- Keep all real interest capture inside the existing lead system. Do not create a second lead endpoint.
- Every unit-level CTA must include `card_id`, `unit`, `floor`, `rooms`, `sqm`, and a source marker so the owner can see which apartment created the lead.
- A theoretical purchase CTA is allowed only as a non-binding inquiry. It must say availability, price, and terms require human verification.
- Use dark blueprint, champagne linework, restrained glass, and architectural geometry. Avoid cartoon buildings, fake stock photos, fake people, and fantasy renders.
- Make mobile usable first: no horizontal overflow at 390px, 44px tap targets for model controls, and stacked forms.

## CMS Contract

Use the existing `nadlan_project` metadata:

- `project_3d_image`
- `project_3d_viewbox`
- `project_3d_units`
- `project_3d_demo`

Recommended unit JSON fields:

```json
{
  "id": "R-34-E",
  "title": "קו E",
  "floor": 34,
  "rooms": 5,
  "sqm": 158,
  "balcony": 22,
  "dir": "צפון מערב",
  "line": "E",
  "view": "ים, פארק ושדה דב",
  "price": 0,
  "status": "available",
  "plan": ""
}
```

`price: 0` means `לפי פנייה`. Only official owner/developer data should set a price.

## Long-Term Upgrade Path

- Phase 1: pseudo-3D tower picker in `inc/project-3d.php`.
- Phase 2: owner-approved elevation image and real unit inventory.
- Phase 3: traced polygons or GeoJSON per floor.
- Phase 4: compound map with Mapbox 3D buildings and project pins.
- Phase 5: real BIM/IFC/glTF/3D Tiles when the developer provides source files.

## Sde Dov To Countrywide Rollout

Treat Sde Dov as the first district template, not as a one-off.

For each district:

- Create one `nadlan_compound` term for the district or subdistrict.
- Assign every real project card to that compound.
- Require city, lat, lng, developer, project status, unit count when sourced, and official links.
- Enable the compound map only after token, term, and project pins are present.
- Add project-level 3D only where the card has `project_3d_demo=1` or real unit/elevation metadata.

For countrywide expansion:

- Start with high-value districts: Sde Dov, Park Hayam Bat Yam, Glilot, Pi Glilot, Bavli, Kikar Hamedina, Givat Amal, Ramat Hasharon west, Herzliya marina and business district, Jerusalem entrance district.
- Normalize every project into the same unit JSON contract so one renderer can power all projects.
- Keep official data provenance in the project body or references list.
- Never generate fake inventory to fill gaps. Use a premium illustrative model with clear demo labeling until official data arrives.

## Data Quality Levels

- `concept`: visual massing only, no official unit data. Price shows `לפי פנייה`.
- `traced`: owner-approved elevation/floor polygons, but availability not verified. Price shows `לפי פנייה`.
- `inventory`: verified unit fields from owner/developer, still non-binding unless contract process exists.
- `bim`: real BIM/IFC/glTF/3D Tiles source connected to project/unit data.

Only `inventory` and `bim` can show specific prices or availability.
