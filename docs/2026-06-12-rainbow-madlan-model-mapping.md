# Rainbow / Madlan Data Mapping For The 3D Picker

Date: 2026-06-12
Branch: `codex/rainbow-3d-hotfix`
Scope: v1.59.2 Rainbow 3D visual follow-up

## What Was Inspected

Using the owner-provided Chrome session and Madlan subscription access, Codex inspected:

`https://www.madlan.co.il/projects/חלקה_15_שדה_דב_תל_אביב?marketplace=residential`

The page title rendered as:

`Rainbow Boutique - Tel Aviv - פרויקט בניה חדשה | מדלן`

## Public / Visible Project Facts Observed

These facts were visible in the rendered page and are suitable for validation against other public sources before publishing:

- Project name on Madlan: `Rainbow Boutique - Tel Aviv`
- Location label: `שדה תעופה שדה דב תל אביב יפו`
- Developer: `ישראל קנדה`
- Building count: `7 בניינים`
- Height range: `8-40 קומות`
- Apartment count shown by Madlan: `459 דירות`
- Amenities called out: infinity pool, adults pool, two minutes from the sea, near light rail
- Estimated occupancy text visible: `תאריך איכלוס משוער 2029`
- Apartment mix text visible: `2-5 חדרים` plus penthouse villas
- Visible market panel: `היסטוריית עסקאות`, `בפרויקט (664)`, average price per sqm around `76 א׳ ₪`

Existing Rainbow content already discloses the developer-marketing 480 versus permit/Madlan-style 459 unit discrepancy. Keep that truth-first disclosure.

## Transaction Table Shape

The transaction history table exposes these columns:

- Address
- Distance / `בניין זה`
- Deal date
- Price in NIS
- Area sqm
- NIS per sqm
- Rooms
- Brokerage indicator

Top visible rows included recent 2026 transactions with prices, sqm, and room counts. Do not bulk-copy or republish the paid-source table until the owner confirms the subscription terms allow publication or the same facts are independently sourced from an open/public source.

## CMS Mapping

`project_3d_units` JSON now supports these keys:

```json
{
  "id": "unit-24-c",
  "title": "קו C",
  "floor": 24,
  "rooms": 4,
  "sqm": 118,
  "balcony": 14,
  "dir": "דרום מערב",
  "line": "C",
  "view": "קו החוף והמרינה",
  "building": "מגדל Rainbow",
  "availability": "זמינות לפי פנייה",
  "note": "תיאור קצר של הדירה או הטיפוס",
  "market_note": "עסקה דומה / מחיר למ\"ר / מקור מאושר",
  "source_note": "Madlan / יזם / היתר / תכנית מכר, לפי הרשאה",
  "price": 0,
  "status": "available",
  "plan": "",
  "points": "576,380 654,380 654,396 576,396"
}
```

## Safe Use Rule

For public display:

- Use exact prices only when sourced from the developer, an official/open source, or an owner-approved data license.
- Use Madlan subscription rows as internal enrichment and QA until rights are clear.
- If the data is not official, label it as comparison or market context, never as live availability.
- Never show a unit as available/sold based only on a third-party transaction row unless the developer confirms inventory.

## Current Implementation

The v1.59.2 patch now:

- Adds building, availability, note, market_note, and source_note to unit JSON.
- Shows these fields in the unit drawer.
- Passes building, availability, and market_note through the lead payload.
- Adds the same context to the owner routing email.
- Mirrors the same context into the optional `non_binding_inquiry` offer seam when offers are enabled.
- Replaces the old generic facade with a tower plus boutique-buildings concept SVG aligned to the new clickable polygon coordinates.

## Next Phase

After this PR is stable, the next mission should be a dedicated data importer/admin screen:

1. Owner uploads an authorized CSV/JSON of sales or inventory.
2. Admin maps columns to `project_3d_units`.
3. System previews the facade points before publishing.
4. Public page labels each source: official inventory, developer marketing, public/open transaction, or private comparison.
5. Only official/developer-approved inventory can drive real availability or reservation flow.
