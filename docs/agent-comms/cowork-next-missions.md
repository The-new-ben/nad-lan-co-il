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

- [ ] **JOB 1 — Activate the DESIGNED homepage live.** #260 flipped on the real Claude Design
      home-showroom (`patterns/nadlan-home-showroom.php`: gallery-mode multi-project 3D + embedded
      he/en/fr/ru/ar switching) and removed the wrong flagship patch. It is a THEME change:
      UPress panel -> **ניהול GIT -> Pull `main`** (pre-authorized), clear cache. Verify `/`:
      one H1, the project gallery (choose between projects), language buttons switch cards +
      panel (correct dir), `[data-nle-home-showroom]`=1, no 2nd homepage renderer, no overflow,
      HE+EN. Screenshot.
- [ ] **JOB 2 — Translate every project + per-language keyword SEO.** All Hebrew project content ->
      EN/FR/RU/AR, targeting each language's buyer intent (NOT literal translation). SERP research +
      reverse-engineer per language via `skills/runbook-cowork-article-batch-v3.md`,
      `skills/google-blueprint-workflow.md`, the multilingual-architecture research, Madlan +
      subscriptions. Publish the translated sibling posts (-en/-fr/-ru/-ar) with correct keywords +
      hreflang. Report progress per project/language.
- [ ] **JOB 3 — Map accuracy + surroundings (research).** Maps show projects in the WRONG location and
      lack surrounding data. For each project get the correct lat/lng + real POIs (transport, schools,
      beach, Reading Tower, nearby projects) from Madlan/Google. Post verified coordinates + POIs here;
      Claude Code wires accurate geo + map pins (never invented).
- [ ] **JOB 4 — Create the missing broad content** (this is a real-estate CONTENT site, not just projects):
      listings (`nadlan_property`=0) + news/articles (posts=0), published in wp-admin via the runbooks.
      When they exist, tell Claude Code to surface them on the homepage + menus.

## DONE (verified)
- [x] PR4 single section nav (1.69.57)
- [x] PR5 price + comps, real data (1.69.58)
- [x] PR6 interior tour, lazy (1.69.59)

## RULES (always)
One showroom/band per surface; one model-viewer on home; single lead endpoint; no duplicate hreflang;
no fake data (real listings/comps only, ranges + non-binding label); no internal words; no em dash.
