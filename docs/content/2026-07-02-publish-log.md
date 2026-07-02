# Content publish log - 2026-07-02

Repo-side record of publishes reported by writing agents. Cowork's full session
log (SERP snapshots, sourced data, learnings) lives in the owner's Drive; this
file records the verifiable state so the repo stays the source of truth.

## Published and verified live (curl 200, indexable)

| Draft | URL | Lang | Notes |
|---|---|---|---|
| 4960 | /buy-property-israel-foreign-buyers/ | EN | Pillar, 4,329 words, focus kw "buying property in israel". LTR wrapper + mobile scrollable-table CSS added by Cowork (RTL theme right-aligned English body). |
| 4962 | /israel-mortgage-non-residents/ | EN | Commercial spoke, 3,392 words, focus kw "israel mortgage for foreigners". Pillar-spoke links wired. |
| - | 6 Hebrew news articles (IDs 4998-5003), category nadlan-news | HE | Seeded by Claude Code 2026-07-02, feed the homepage magazine band. |

## Housekeeping decisions (2026-07-02, Claude Code)

- Category `english` (id 34) created; EN cluster posts assigned to it.
- Homepage magazine band (home-v2) queries ONLY category `nadlan-news`, so the
  Hebrew homepage never shows English headlines. Writing agents: put Hebrew
  news/analysis into `nadlan-news`; EN cluster into `english`.
- Cowork reported `handoff/cowork/2026-07-02-content-writing-mission.md` and
  `docs/content/2026-07-02-content-skeleton-architecture.md` as missing - they
  exist on main (commits f25e0c8, f46b910). Its clone was stale; re-pull before
  the next session.

## Next-session queue (per Cowork)
4961 -> 4963 -> rest of EN cluster -> Hebrew spokes. Cadence: 2-3/week minimum
so the magazine band stays fresh (it collapses below 3 recent posts).
