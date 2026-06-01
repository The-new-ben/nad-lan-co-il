# Reply to Cowork — you are UNBLOCKED (state corrected with proof)

> Paste this to the Cowork session that hit §STOP on the glossary batch.

```
COWORK — STATE CORRECTION + GREEN LIGHT (read fully before re-stopping)

Your §STOP was correct discipline, but it fired on STALE state. Here is the
verified current reality (re-checked live, cache-busted, 2026-06-01 17:02 UTC):

PROOF (run these yourself against PRODUCTION, with a cache-buster):
  GET https://nad-lan.co.il/wp-json/nadlan/v1/healthcheck?cb=RANDOM
    → "version":"1.18.0"  (NOT 1.3.0)
    → directory.claim_cpt=true, auction_cpt=true, bids_table=true, ga4_hardcode=false
    → tiers:{free,pro,premier}
  GET https://nad-lan.co.il/glossary/                    → HTTP 200
  GET https://nad-lan.co.il/wp-json/wp/v2/nadlan_term     → HTTP 200 (CPT is live)
  POST https://nad-lan.co.il/wp-json/nadlan/v1/import-enrich → HTTP 401
    (endpoint EXISTS, just needs auth — a 401 proves it is live; 404 would mean missing)

WHY YOU SAW 1.3.0 (resolve this first):
You are almost certainly checking a LOCAL/STAGING WordPress (which was last at
1.3.0) or a stale repo clone — NOT the production site. The glossary content must
be published to PRODUCTION. So:
  1. Set your target to the LIVE site: base URL = https://nad-lan.co.il
     (env WP_BASE_URL). Do NOT use a localhost/staging WP for this batch.
  2. Re-run the healthcheck above against that URL with a cache-buster. It WILL
     read 1.18.0. Your version gate now PASSES.
  3. If — after pointing at https://nad-lan.co.il with a cache-buster — you STILL
     see 1.3.0, then STOP and report the EXACT URL/host you queried + the raw JSON,
     because that would mean a DNS/proxy problem worth diagnosing. (We do not
     expect this; the live site is confirmed 1.18.0.)

CORRECTIONS to your briefing's assumptions:
  - "PR #4 only reaches v1.6.0" → FALSE now. PR #4 was MERGED to main (commit
    7156866) and the plugin spans v1.4.0 → v1.18.0 (23 modules). main contains
    plugins/nadlan-config/inc/glossary.php, tiers.php, etc.
  - "You held the deploy" → FALSE now. The owner merged + clicked WP Update; the
    live plugin is 1.18.0 (owner-confirmed in WP admin + verified via healthcheck).
  - "No v1.18.0 anywhere" → it is on origin/main AND live. If your LOCAL clone
    lacks it, you do not need it: you operate against the LIVE REST API, not your
    repo files. Just `git fetch && git checkout main` if you want the files too.

YOU DO NOT NEED THE REPO TO MATCH — the glossary publish runs entirely against the
live WordPress REST API. The only thing that matters is that PRODUCTION reads 1.18.0,
which it does.

OBSTACLE REMOVAL (so you can run at full speed):
  - AUTH for the 401: create/confirm a WordPress Application Password for an editor
    account (WP Admin → Users → Profile → Application Passwords) and use it as
    HTTP Basic auth on wp/v2 + nadlan/v1 writes. This clears the 401.
  - CREATE a term: POST https://nad-lan.co.il/wp-json/wp/v2/nadlan_term
      {"title":"<Hebrew term>","status":"draft"}  → note the id.
  - WRITE the body via ChatGPT (you never hand-write Hebrew — preserve tokens;
    use the sub-prompt in docs/prompts-lovable-and-cowork-glossary.md, PROMPT B,
    step 3).
  - PUBLISH the body: POST https://nad-lan.co.il/wp-json/nadlan/v1/import-enrich
      {"post_id":<id>,"content":"<html>","data_quality":"enriched",
       "meta":{"term_en":...,"wikipedia_en":...,"related_pillar":...,
               "related_anchor":...,"source_url":...,"source_label":...}}
    Then set the term status=publish (the plugin pings IndexNow automatically).
  - WIKIPEDIA-VOID CHECK (step 1 of the loop): for each term, search
    "<term> site:he.wikipedia.org"; if a comprehensive Hebrew article exists, SKIP
    and log "HE-WIKI EXISTS"; else proceed. This is safe to do regardless of deploy.

NOW PROCEED with the WAVE-1 60-term batch (list in docs/master-plan-and-sequencing.md
§WAVE 1) under the iron rules in PROMPT B (no em-dashes, no AI markers, 100%
original, cite a source, add the upward pillar link, single H1, near-duplicate check).

DELIVERABLE: published count, skipped-as-HE-WIKI count, 3 sample /glossary/ URLs
(confirm they are indexable — no noindex meta), and your progress cursor.

If you can do useful work with ZERO risk regardless of any doubt, the safe prep is:
run the Wikipedia-void scan on all 60 terms + draft the term→pillar mapping first,
then publish in one fast pass. But you are cleared to publish to production now.
```
