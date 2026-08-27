# 06 Replication Rule

## Fixed across every project

These never change by project:

- Header structure.
- Cream editorial palette.
- Typography system.
- Showroom stage layout.
- Unit rail behavior.
- Selected apartment panel.
- Inquiry actions.
- Missing asset state.
- Mobile 390 layout.
- Public language rules.

## Per-project content

These change per project:

- Project name.
- City and neighborhood.
- Developer.
- Hero image or facade.
- Building asset state.
- Unit list.
- Unit facts.
- Price label.
- Status.
- Floor plans.
- Inquiry destination.
- Legal or availability note approved by owner.

## Minimum viable project

A project can go live in the premium pattern if it has:

1. Project name.
2. City.
3. Developer.
4. One high-quality visual.
5. At least three apartments or unit types.
6. Inquiry destination.

## Premium project

A premium project should have:

1. Real building model or high-quality facade.
2. Apartment coordinates or polygons.
3. Official unit plans.
4. View stills or orientation descriptions.
5. Updated availability.
6. Dedicated English copy.

## Rule for weak assets

Do not fake strong assets. Use a premium missing state.

## Rainbow-specific items that must not leak into the system

- Unit IDs with Rainbow-only naming.
- Fixed camera values as product assumptions.
- Rainbow project copy.
- Any assumption that all projects have a real model.

## What makes the system reusable

The UI depends on a simple contract:

```json
{
  "project": { "name": "Rainbow Tel Aviv", "city": "Tel Aviv", "asset_state": "real" },
  "units": [
    { "id": "unit-16-w", "floor": 16, "rooms": 4, "sqm": 112, "direction": "west", "status": "available" }
  ]
}
```

The renderer does not care whether the project is luxury beachfront, urban renewal, or small boutique. Only the data changes.

