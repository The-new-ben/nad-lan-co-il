# Showroom live QA - 1.69.36

Date: 2026-06-24
URL: https://nad-lan.co.il/projects/rainbow-tel-aviv/
Version verified live: 1.69.36

This folder is live proof after installing NadLan Config 1.69.36 through WordPress admin.

What passed:

- WordPress healthcheck reports 1.69.36.
- The `single_selection_surface_v16936` health flag is present.
- `unit-16-w` selection opens the selected apartment card.
- Camera orbit and camera target change after selection.
- The old duplicate lower selection dock is no longer populated.
- Mobile 390 reports no document-level horizontal overflow.
- Public leak scan found no Codex, Lovable, prompt, token, GLB, SVG, Featured, Sponsored, or Promoted text in the checked showroom surface.

What did not pass visually:

- Mobile toolbar controls still stack too tall above the model.
- The mobile selected apartment card title wraps awkwardly.
- The visual shell is cleaner than 1.69.35, but it is not yet premium enough for contractor presentation.

Decision:

1.69.36 is a cleanup release, not the final showroom. The next release must tighten the mobile control layout and selected card typography.
