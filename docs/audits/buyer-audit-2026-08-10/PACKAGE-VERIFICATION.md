# Package verification record

- Package: `nadlan-360-buyer-audit-2026-08-10`
- Built: `2026-08-11T06:22:32+03:00`
- Files before this record, inventory and manifest: 127
- Raw browser JSON with client tokens/local paths: excluded
- Structure-preserving sanitized JSON: included
- Prior unit-journey ZIP: included byte-for-byte under `archive/`
- Live-site or product-repository mutations: none
- Primary entry point: `report/report.html`
- Developer entry point: `README-FIRST.md`

The outer ZIP is verified again after creation by reopening it, rejecting absolute/traversal/duplicate entries, extracting it to a dedicated temporary directory, validating `MANIFEST.sha256`, parsing all CSV/JSON files, checking code syntax and executing the packaged synthetic proposal fixtures. After upload, delivery must separately download the remote object and compare its SHA-256 with the local archive before giving the link to the user; that post-upload proof cannot truthfully be embedded in this pre-upload record.
