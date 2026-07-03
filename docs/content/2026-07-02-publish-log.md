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

## Cowork session 2 (2026-07-02, relayed by owner)
- Published: /israel-purchase-tax-foreign-residents/ (~3,045 words, focus kw
  "israel purchase tax foreigners", category english, 3 tables incl. NIS 4M
  worked example, FAQ schema, branded featured chart).
- Featured images backfilled on 4960 + 4962; all EN articles now share with
  og:image cards.
- NOTE for Cowork: its sandbox remote is STALE (tip at May 29) - GitHub
  main has the mission files and this log (PRs #320/#325). Fix the remote or
  re-clone from https://github.com/The-new-ben/nad-lan-co-il before session 3.
  Its dangling log commit was superseded by this entry.
- Next queue: 4963 (transfer-money-to-israel-property) -> rest of EN cluster
  -> first Hebrew news batch into nadlan-news.

## News pair published 2026-07-02 (Claude Code) - the 690K story
| Post | URL | Lang | Words | Notes |
|---|---|---|---|---|
| 5030 | /3-room-apartment-690k-israel-2026/ | HE (nadlan-news) | 2,045 | 6 tables, NewsArticle+FAQ schema, 43 internal links, sourced Maariv/Ynet |
| 5031 | /affordable-apartments-israel-2026/ | EN (english) | 2,153 | 5 tables, foreign-buyer angle, links into EN cluster (tax/mortgage/pillar) |
Anti-cannibalization: HE targets "דירה ב-690 אלף שקל"/"דירות זולות בישראל" (distinct from the buyers-market piece); EN targets "affordable apartments in Israel" (distinct from the tax/mortgage/buying guides, which it links into). Both in the sitemap; HE feeds the homepage magazine band.
