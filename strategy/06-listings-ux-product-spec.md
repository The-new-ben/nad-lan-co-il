# Listings UX Product Spec

Purpose: define how NadLan listings should work when real inventory exists. Do not publish fake listings to make the site look full.

## User Jobs

1. Find apartments by location, price, rooms, size, floor, availability, and project.
2. Understand trust: source, update date, whether broker/developer/private.
3. Compare options quickly.
4. Contact with context attached.
5. Save/search later.

## Listing Modes

| Mode | When to use | Public status |
|---|---|---|
| Real inventory | property has source, price, photos, contact path | index/list |
| Project inventory | unit belongs to project/showroom | show inside project and maybe aggregate |
| Aggregated market data | price guide/statistical data | do not show as individual listing |
| Demo/prototype | generated sample | noindex or hidden |

## Desktop Layout

- Map/list split for inventory pages.
- Cards in dense but premium style.
- Sticky filter bar with city/neighborhood/project/status.
- Map pins cluster by price/status.
- Listing detail preview opens inline or side panel.

## Mobile Layout

- Search/filter first.
- Toggle list/map.
- Large tap targets.
- Sticky contact/save at bottom only on detail page, not on list cards.
- No overlapping floating button stacks.

## Listing Card Content

Required:
- image or honest missing-image state.
- price or "מחיר לפי פניה" when legitimate.
- rooms, sqm, floor, city/neighborhood.
- source/contact type.
- updated date.
- primary CTA.

Optional:
- balcony, parking, elevator, view, orientation, project label.
- estimated price range with disclaimer.

Forbidden:
- "lead funnel", "CRM", "test", "debug".
- fake urgency.
- fake availability.
- hidden code/class leakage.

## Data Contract

Minimum source-of-truth fields:

```json
{
  "id": "",
  "status": "available|reserved|sold|inactive",
  "listing_type": "sale|rent|project_unit",
  "source_type": "owner|broker|developer|internal|public_data",
  "price": null,
  "price_label": "",
  "city": "",
  "neighborhood": "",
  "lat": null,
  "lng": null,
  "rooms": null,
  "sqm": null,
  "floor": null,
  "images": [],
  "contact": {},
  "updated_at": "",
  "verification": "verified|unverified|concept|missing"
}
```

## SEO Rules

- Noindex thin listing-search result pages until real inventory depth exists.
- Index city/neighborhood/category pages only when they include unique content, map/data, and useful listing depth.
- Use `ItemList` only for real items.
- Use `RealEstateListing` only when data is real and public.

## Inspiration Sources

- Zillow and Homes.com: search, rich media, maps, tours.
- Yad2/Madlan: local inventory expectations, but do not copy visual style.
- Mapbox real estate: maps for search and market insight.

## Acceptance Criteria

- No fake inventory.
- No horizontal overflow at 390/768/1440.
- Card scan time under 3 seconds for price/location/rooms/status.
- Contact payload includes listing/project/unit context.
- Public pages do not show Woo debug/cart artifacts unless commerce screen.
