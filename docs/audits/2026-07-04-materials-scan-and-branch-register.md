# Materials scan + agent-branch register (2026-07-04)

Owner asked to scan `C:\Users\pro\nad-lan-co-il` and `C:\Users\pro\.codex` for
materials/GLBs left by other agents and pull anything useful into the repo.

## Reachability (the honest limit)
I run in a **remote cloud container**. I **cannot** reach the owner's local
Windows paths (`C:\Users\pro\...`) or his local `.codex` folder. To ingest
those, the owner must zip + upload them. Anything Codex produced locally after
2026-06-24 is only on his machine until then.

## What I CAN reach — scanned in full
1. **Uploads (prior sessions):** all fully ingested already. Every GLB is a
   duplicate of one in the repo; every spec MD is already in the repo; the
   facade/poster mockups match files already serving. Nothing new.
2. **`handoff/codex/` (114 files):** prior Codex work (through ~2026-06-24) was
   already collected here — skills, design, data, reports, lovable-prompts,
   language-cleanup. Nothing missing from it.
3. **287 remote branches** from many agent sessions (claude/*, antigravity/*,
   codex, strategy/*). NOTE: `git --no-merged` reports 284 as "unmerged", but
   that is inflated by **squash-merges** (the squash commit has a new SHA, so
   git can't see the branch as merged even though its content is in main). Most
   of these are already-merged work.

## Genuinely-new material found + captured
- **`assets/projects/ashira-sde-dov/massing-spec.json`** (from
  `claude/ashira-grounded-model`, never merged to main): Ashira's REAL sourced
  composition — Avisror 'Ashira' Sde Dov, **4 buildings 8/8/16/35 floors, 406
  units, sea to the west, floor 3.2 m** (building.org.il / ice.co.il /
  sdedov.co.il). Now in the repo + folded into `data/projects/ashira-sde-dov.json`.
- **`scripts/generate-massing.py`** (same branch): the **materials→GLB factory**
  — spec.json (per-building floors/footprints/orientation/sea-side) → grounded
  illustrative GLB, optional facade-photo drape. Places volumes at REAL relative
  heights, does not invent architecture. This is the foundation for task #22.
  Verified: runs, produced Ashira's real 35/16/8/8 massing (113 m tower).

## GLB verdict (checked every Ashira candidate across branches)
No branch has a better Ashira model than what is live. The "grounded" branch
GLB is the "dot on a 1 km plate" (67 m building, 1090 m ground). The live
deployed factory model (2004 tris, 440×113×360) is the best-framed available.
The regen from massing-spec is truthful to the real composition but only 72
boxy tris — the factory needs a detail/facade pass (task #22) before it beats
the live model.

## Standing worry (floated, per god-mode)
With 287 branches and squash-merge history, I cannot be 100% certain no branch
holds unique unmerged product code without a full content-diff sweep — a large
job. Recommendation: if the owner suspects a specific stranded feature (e.g. an
`antigravity/unified-ecommerce-engine` buy-flow), name it and I'll diff that
branch precisely. Otherwise the canonical DB (`data/projects/`) + `handoff/`
remain the single consolidation point all agents read from.
