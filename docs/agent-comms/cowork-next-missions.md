# COWORK — STANDING MISSION QUEUE (pull from the top, never wait)

> Cowork has no event-listener (unlike Claude Code, which is subscribed to PR #251).
> So Cowork must run in CONTINUOUS / loop mode on its side and PULL its next job from
> here every cycle. Claude Code keeps this list current. The top unchecked item is the
> current mission. Finish it, check it, comment "verified, next" on PR #251, pull the next.

## How the loop stays alive (no lost connection)
1. Cowork runs in its own continuous loop (owner enables this; Claude Code cannot wake Cowork remotely).
2. Each cycle: read this file (top unchecked = current job) + PR #251 for Claude Code's latest reply.
3. Do the job in Chrome (wp-admin / SERP / content / verify). 
4. Comment the result on PR #251 ("verified, next" or findings).
5. Claude Code (event-woken by that comment) ships the next code slice and updates this queue.

## CURRENT MISSIONS (top = now)

- [ ] **Activate the homepage live (theme deploy).** #256 is theme-side (plugin Update will NOT ship it).
      EXACT path: UPress panel -> "ניהול GIT" (Git management) -> **Pull from `main`** (UPress Git is
      `main`-only; #256 is merged, ready to pull). Owner's UPress login only. Do NOT use the file-manager
      upload (partial-sync risk). After pull, clear cache + hard-reload. There is NO feature flag/WP option;
      the flagship 3D auto-renders once the theme code is live (Ashira has a model). Keep the orchestrator
      `nlpo_auto_insert_home_band` OFF (ON = second band). Verify `/`: `.nlux-flagship` present,
      `model-viewer` count = 1 (was 0), `[data-nlpo-home-projects]` = 1, no overflow, HE + EN. Screenshot.
- [ ] **Create the missing content (your job, in Chrome, as a user).** Per the runbooks:
      `skills/runbook-cowork-article-batch-v3.md`, `skills/google-blueprint-workflow.md`
      (SERP reverse-engineer), `skills/article-publishing-protocol.md`,
      `skills/directory-listings-project-plan.md`, `skills/nadlan-seo-content-design-monetization-rulebook.md`.
      You are logged in to Madlan + subscribed services. Steps you've done before:
      search Google for the target query, analyze the SERP/competitor pages, reverse-engineer the
      winning structure, draft via ChatGPT to the copywriting rules, then **manually publish in
      wp-admin** as: (a) **listings** (`nadlan_property`, currently 0) and (b) **news/articles/guides**
      (posts, currently 0). Real, sourced, no fabricated prices. Report counts on PR #251 when a batch lands.
- [ ] **Verify the homepage broad-content bands** once Claude Code ships them (Guides + Glossary + Area hubs).
- [ ] **When listings/news exist:** tell Claude Code, and it un-hides the Listings + News homepage bands
      (they are wire-ready, hidden while empty).

## DONE (verified)
- [x] PR4 single section nav (1.69.57)
- [x] PR5 price + comps, real data (1.69.58)
- [x] PR6 interior tour, lazy (1.69.59)

## RULES (always)
One showroom/band per surface; one model-viewer on home; single lead endpoint; no duplicate hreflang;
no fake data (real listings/comps only, ranges + non-binding label); no internal words; no em dash.
