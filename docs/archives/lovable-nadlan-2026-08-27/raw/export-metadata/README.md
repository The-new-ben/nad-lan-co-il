# Lovable Nadlan export

Exported on 2026-08-27 from the official Lovable connector and the currently signed-in Lovable editor.

## Included

- Sanitized project metadata in `metadata/projects.json`.
- Complete path manifests for both projects.
- All 536 text files exposed by Lovable `read_file`, kept under their original relative paths:
  - Design Lab: 100 text files in `raw/design-lab/`.
  - NadLan Strategy Hub: 436 text files in `raw/strategy-hub/`.
- Three empty `.gitkeep` files recreated as empty files.
- Route inventory for 13 audited routes in `route-index.json`.
- Eleven 1440×900 viewport screenshots for the Design Lab Nadlan routes.
- A machine-readable inventory of 80 binary files that could not be exported byte-faithfully in `binary-assets-unexported.json`.

Text files were normalized to LF line endings during local export. No environment files or secret-named files were present in the official manifests. A strong-key scan found no private keys, AWS access-key identifiers, or OpenAI-style secret keys in the exported text.

## Source projects

- Design Lab: private and unpublished. Editor: https://lovable.dev/projects/627f6877-57f3-4821-9e77-2b2011c56292
- NadLan Strategy Hub: project private, existing deployment public. Editor: https://lovable.dev/projects/a7493b94-2e46-4d38-9c6a-80dcf0905f45
- Existing public Strategy Hub: https://nadlan-vision-quest.lovable.app/

No project was published, deployed, generated, edited, connected to Git, or given new permissions during this export.

