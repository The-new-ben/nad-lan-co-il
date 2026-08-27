# WordPress Post-1.69.0 Review Packet for Lovable

This packet mirrors the WordPress showroom release history after the 1.69.1 cream release into the Lovable strategy hub as review material only. It is not executable code and it must not be imported into the TanStack app.

## Source and scope

- WordPress source repo: https://github.com/The-new-ben/nad-lan-co-il
- Base release: b25ff8a - 1.69.1 cream skin merge
- Final release reviewed: d5306af - 1.69.32 row-aligned model tap fallback
- Live proof commit after release: 3c08364 - 1.69.32 live QA proof
- Packet destination: handoff/lovable/2026-06-24-wp-pr-review/

## How to review

Read in this order:

1. timeline.md
2. proof-integrity.md
3. prs/1.69.32-row-aligned-fallback-deployed.md
4. qa/showroom-live-selection-16932-2026-06-24/README.md
5. Older prs/*.md only if you need to understand why so many patches happened.

## Lovable review focus

Lovable is asked to review only:

- Whether the showroom buyer experience matches the Nadlan3D strategy reports already in handoff/lovable/2026-06-23-war-room-sync/reports/.
- Mobile 390 behavior on /projects/ and /showroom/*.
- Public-language quality: no Lovable, Codex, prompt, token, GLB, SVG, Featured, Sponsored in buyer-facing UI.
- Whether row-aligned model-tap fallback is the right product behavior or a workaround hiding missing BIM.
- Whether the 30 plus patch-release cycle reflects a design gap Lovable should re-spec.

## Lovable is not asked to

- Import WordPress PHP, JavaScript, or CSS into this TanStack codebase.
- Treat any diff as code to run, build, or deploy.
- Compete with the WordPress source-of-truth repo.

## Honest scope note

The accepted live proof is 1.69.32 only. Older proof from 1.69.2 to 1.69.29 is marked weak, disputed, or superseded because duplicate PNG collisions were found and because later releases continued fixing the same behavior. This packet is intentionally strict so Lovable reviews the product truth, not a polished story.

