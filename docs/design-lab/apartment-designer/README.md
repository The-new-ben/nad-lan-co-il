# Apartment designer lab (HAD-701)

Local only. Nothing in this folder is live or linked from the site.

- `spike/`: the HAD-703 proof that one apartment model drives a 2D plan and a live 3D view on a phone.
  - Run: `python -m http.server 47960 --bind 127.0.0.1 --directory docs/design-lab/apartment-designer/spike`, then open `http://127.0.0.1:47960/`.
  - `model.js` (the core: wall graph, rooms, operations, rules, undo, quantities), `plan2d.js`, `space3d.js`, `catalog.js` (generic pieces, no prices), `example-4r.json` (an invented four-room layout, labelled as an example).
  - `node test-model.mjs`: 24 checks of the core with no browser.
  - `node check-spike.mjs`: presses the page like a phone user in headless Chrome and writes `evidence/receipt.json` and screenshots (the server above must be running). `--gl=soft` runs it without a GPU.
  - `node dump-design.mjs`: prints a design document as the store writes it (used to validate the schema).
- Architecture and schemas: `docs/architecture/apartment-designer/`.
- Design boards (Claude Design, private to the owner): https://claude.ai/artifact/V8wiqeJ4qtS4qnzgxmXyCA
  Seven boards: the engine on a phone (plan and 3D, catalogue with prices, spec sheet, video call), the engine on a desktop, and the "עיצוב דירה" page on a phone and a desktop.
  Identity: the architect's working drawing. Drafting white `#F2F5F7`, plan ink `#0F2233`, blueprint blue `#1F5FA8` for what you hold or may move, dimension red `#B5302A` for measurements only, green `#1C7A4E` for "included". Faces: IBM Plex Sans Hebrew and IBM Plex Mono.
- Research: `docs/research/2026-11-10-apartment-designer/`.
