# Kikar Hamedina V7: five articles, 5,000+ net words each (HAD-380), LIVE as 1.72.403 (3.10.2026)

The five Kikar Hamedina pages (/projects/hamedina/, -en, -fr, -ru, -ar) carry a new article each, written in ChatGPT Pro from an
evidence packet (project law 8: the agent prepares the packet and the prompt, ChatGPT writes, the agent fact-checks and releases).

## Result

| Language | Net words (Intl.Segmenter) | Without the lead | Numbers in the text | Matched to a claim | FAQ (schema) |
|---|---:|---:|---:|---:|---:|
| he | 7,264 | 7,174 | 357 | 357 | 13 visible, first 12 in FAQPage |
| en | 7,359 | 7,272 | 377 | 377 | 13 |
| fr | 7,463 | 7,376 | 349 | 349 | 13 |
| ru | 7,390 | 7,299 | 338 | 338 | 14 |
| ar | 7,249 | 7,157 | 337 | 337 | 13 |

The counts include the small phone labels in three tables (about 100 words a page); without them every article is still over 7,000.

Live checks after the release: `scripts/project-stage/verify403.py` all green (402 page checks, served files, page order, home order,
the five Kikar pages: one H1, one FAQPage, hreflang, section order); `tools/lang_pages_check.py hamedina` 0 Hebrew left outside the
article; `tools/content_first_check.py` 10/10 (phone and desktop); `tools/source_audit.py` GREEN on the five pages.
Screenshots of the live page: `shots/`.

## The chain (C1, Maya's breakthrough: evidence -> brief -> ChatGPT -> article)

1. `claims.py` -> `claims.json`: 84 claims, each with a claim_id, the numbers it allows, date, source (facts.md S-ids, area.md, and
   facts.md's new section "Additions, V7": purchase tax, mortgage limits, broker's fee), the conflict and how to write it.
   Sources live here only: the articles name none (the owner, 1.10.2026).
2. `build_packets.py` -> `packet-<lang>.json` + `prompt-<lang>.md`: the outline (14 sections, word budgets, the claims each must use),
   the SERP intents per language (serp-dna.md, serp-fr/ru/ar.md), names, culture, typography, banned words, the HTML contract and the
   internal links (`links.json`, 78 links, each GET 200 on 3.10.2026).
3. ChatGPT Pro (6 Pro, maximum thinking), chatgpt.com in the gmktec Chrome (access to the desktop app was declined): the brief attached
   (`upload/`), three parts per language. Conversation links: `chatgpt-runs.json`. Raw outputs: `raw/`.
4. `assemble.py` (joins the parts, strips ChatGPT's citation markers), `apply_fixes.py` + `fixes.json` (four factual corrections: the
   averages' dates in he/en), `phone_labels.py` (the page hides table headers on phones: the deals and cost tables carry the column name
   under each value), `check_article.py` (contract, banned words, every number to a claim, net words) -> `fact-check-<lang>.md`.
5. `article-<lang>.html` -> `docs/research/2026-09-30-kikar-hamedina/post-<lang>.html` -> release 1.72.403
   (`scripts/project-stage/make_gen403.py` -> gen_deploy403.py -> deploy403.py).

## What happened during the release (honest record)

- The first run (01:25) wrote the five posts and the version, then failed verify_pages ONLY on checks inherited from 1.72.369-391
  that required the old articles' sentences (and a passing 502 on / and /brokers/). Its rollback could not reach its bridge: a
  concurrent dry run by the rentals session (deploy404 --dry) swept it. So the new posts stayed live.
- make_gen403.py now drops those stale checks and requires the new article markers; deploy403.py was regenerated (the base for 404+).
- `verify403.py` ran the whole regenerated check chain read-only: ALL GREEN (`docs/qa/project-stage-2026-09-24/verify403.log`,
  deploy-result-403.json "released and verified (re-check)").
- About 01:40 the whole site's front end and REST returned nginx 502 for 1-2 minutes (wp-login and static files fine), then recovered by
  itself. No session reported running anything at that minute. Logged as a finding (HAD-380 comment).
- A release lock rule now lives in docs/coordination/claude-codex.md (written by the broker-site session): "RELEASE IN PROGRESS" /
  "RELEASE DONE" before and after any run, dry or live.

## Not in git

`preview/` (local previews of the live page with the article, 0.7 MB): rebuild with `preview_local.py <lang>`.
