# Deliberate package exclusions

The final ZIP is built from an explicit allowlist. The following local working artifacts are deliberately excluded even though they may remain in the local deliverables folder:

This policy record is intentionally included in the ZIP so reviewers can verify what was omitted and why; “excluded” below refers to the working artifacts, not to this Markdown record.

1. The five raw browser-probe JSON files directly under `evidence/`. They contain the same observations as `evidence/sanitized/`, but also include a public Mapbox browser token and local filesystem paths. The structure-preserving sanitized copies are shipped instead.
2. Temporary base files created while the portable report was being assembled. The final verified `report/report.html`, its source artifact, build/finalization scripts, inspection result and final screenshots are shipped.
3. Any environment files, browser profiles, cookies, WordPress credentials, passwords, authentication state, cache directories and repository working-tree files. None are necessary to understand or implement the proposal.

No research conclusion or acceptance evidence is removed by these exclusions. The shipped sanitized JSON files retain the measurement structure and values while replacing local paths and public client tokens with explicit redaction markers.
