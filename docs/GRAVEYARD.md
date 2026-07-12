# Graveyard — deleted / scrapped assets (do not resurrect blindly)

When you delete or retire a valuable asset, log it here with: what, why, and
where a copy lives (branch/commit) if recoverable. This keeps other agents from
"rediscovering" known-bad work or panicking that something vanished.

| date | asset | why retired | recoverable from |
|---|---|---|---|
| 2026-07-03 | Ashira GLB (bad) | dot-on-1km-plate framing | `handoff/claude-design/2026-07-03-project-page-factory/_retired-bad-ashira-glb/` |
| 2026-07-04 | boutique project stubs (Amos/Remez/Malachi) | below premium/≥20-unit gate | `data/projects/_excluded.json` |
| 2026-07-04 | 10 stale pre-gate factory pages (blocked langs incl. duo) | violated 3,000-word/no-dash laws; gate no longer emits them | regenerate via generate.py once real translations land |

## 2026-07-12 - plugin-dist/nadlan-config-1.72.90.zip (DELETED, never restore)
Shipped with a PHP parse error in inc/home-v2.php (apostrophe inside a single-quoted
PHP string terminated it) and caused a full site outage. The fixed build is 1.72.91.
Deleted so no update path can ever grab it.
