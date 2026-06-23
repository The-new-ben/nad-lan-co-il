# Listings UX Spec

Goal:
Make NadLan useful as a listings/search surface, not only a content site.

Expected user capabilities:
- Search by city, neighborhood, price, rooms, area, floor, parking, balcony, elevator, status, and property type.
- Map/list toggle.
- Save or compare listings.
- Contact path with tracked lead payload.
- Clear source and freshness labels.
- Sponsored placement disclosure where paid. `LEGAL_REVIEW`

P0 UX standards:
- Fast scannable cards.
- No horizontal overflow.
- Filters are reachable on mobile.
- No dead sort/filter controls.
- Empty states explain what is missing without fake inventory.

Data dependencies:
- Current inventory source and freshness. `NEEDS_VERIFICATION`
- Paid/free listing entitlement rules. `LEGAL_REVIEW`
- Analytics events.

