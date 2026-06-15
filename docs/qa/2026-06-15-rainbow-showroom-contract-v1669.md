# Rainbow Showroom Product Contract v1.66.9

This is the practical product contract from the Hebrew alignment discussion.

## Buyer Surface

- The rotating 3D model is the context rail. It shows the project massing, nearby environment, sun direction, sea/landmarks where available, and the premium first impression.
- The fixed facade beside the model is the apartment picker. Buyers choose apartments from visible facade cells, not from floating dots.
- Green means available for inquiry. Amber means checking or reserved. Red means unavailable.
- The selected apartment opens a card with status, floor, rooms, sqm, view, non-binding price or "by inquiry", and actions for details, apartment view, and developer contact.
- Prototype media is allowed only when clearly replaceable. Official BIM, facade, prices, floor plans, tours, and availability should replace it when the contractor supplies them.

## Contractor Surface

- The project must be clone-ready by fields, not by new code.
- Each project needs one model or fallback massing, one facade/unit map, one environment payload, one poster/social image, one SEO/content pack, and one contact path.
- Contractor-supplied materials belong in CMS fields: GLB/BIM, facade image, floor plans, interior tour, sales video, prices, status, and contact/WhatsApp.

## QA Gate

- Check 1440, 768, 390 and Edge-mobile.
- The showroom must stay inside the viewport before and after apartment selection.
- Unit cells must read as apartment inventory with color/status and useful labels.
- Card close and next apartment selection must work.
- Public copy must speak to buyers, families, investors and foreign buyers only. No internal words.
- Healthcheck must expose the active version and the showroom markers used by the gate.

