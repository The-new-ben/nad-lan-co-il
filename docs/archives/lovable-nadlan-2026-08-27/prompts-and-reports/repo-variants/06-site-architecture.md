# Site Architecture

Architecture principle:
One concept, one URL. Hub/spoke relationships should support money pages without cannibalizing them.

Primary hubs:
- Listings.
- Rentals.
- New projects.
- Urban renewal.
- Professionals.
- Tools/calculators.
- Legal/tax/mortgage guides.
- City and neighborhood hubs.
- Project pages.

Required URL rules:
- Latin slugs only.
- Hebrew titles are acceptable.
- Avoid duplicate page types for the same intent.
- Keep project pages under `/projects/<latin-slug>/`.
- Keep tool pages stable and internally linked from relevant guides.

P0 architecture work:
- Map existing URLs to P0 keywords. `NEEDS_VERIFICATION`
- Identify missing money pages.
- Identify duplicate/cannibalizing surfaces.
- Decide noindex/index status for thin or placeholder pages.
- Wire breadcrumbs and hub navigation.

