# The Self-Writing Encyclopedia - Full Implementation Specification

A portable, battle-tested spec for building an autonomous, self-writing professional
encyclopedia inside any WordPress site. Built and proven in production on
nad-lan.co.il (real-estate encyclopedia, 200+ entries staged, writing and
publishing itself daily). Written so a fresh AI coding session (or a developer)
can implement it end to end on another site, for example a legal encyclopedia
on jus-tice.co.il.

Every design decision below was validated in production, including several
WordPress and LLM failure modes that cost real debugging time. Do not skip the
"Hard-won gotchas" section.

---

## 1. The concept

The owner should never sit and feed ChatGPT by hand. The pipeline is:

1. The owner (or an AI research assistant) produces ONTOLOGY BATCHES: structured
   JSON lists of entry titles with metadata (English term, entity type, domain,
   priority, related entries, source hints). No article text needed.
2. An INTAKE endpoint ingests batches into WordPress as skeleton drafts.
3. A WRITER cron wakes hourly, picks the highest-priority skeletons, writes each
   one a full tiered article through the site's own OpenAI API key, validates it
   (word floor per tier, style laws, clean HTML), and hands it to a drip.
4. A DRIP scheduler publishes N articles per day spread across working hours -
   a believable human cadence, never a bulk dump (this is the anti
   "scaled content abuse" discipline for search engines).
5. A STATUS endpoint reports everything: how many written today, how many
   waiting, how many scheduled, how many published, the last failure with its
   reason, and how many entries are stuck.

Result: the owner drops a JSON file in; the site researches nothing by itself
(zero invented facts is a hard prompt law), writes, validates, schedules and
publishes on its own, forever, within a daily cap.

## 2. Architecture overview

All server-side, one WordPress plugin (or theme include), no third-party AI
plugin. Third-party AI plugins were evaluated and rejected: they know nothing
about your entity fields, tiers, style laws, drip cadence or anti-cannibalization
rules, and one of them took the production site down with a fatal error.

Components (each is one PHP file):

| Component | Responsibility |
|---|---|
| CPT + taxonomy | The encyclopedia post type, its category taxonomy, archive |
| Intake endpoint | POST batch of entries -> skeleton drafts (or scheduled posts if content included) |
| Writer | Hourly cron: pick skeletons -> OpenAI -> validate -> drip |
| Status endpoint | GET live counters + failure telemetry |
| Key storage | POST endpoint that stores the API key in an option, never echoes it |
| Page decorations | English-term chip, JSON-LD schema, autolinker (optional but valuable) |

## 3. Prerequisites

- WordPress 6.x, PHP 7.4+.
- An application password for an admin user (all write endpoints check
  `current_user_can('update_plugins')` or `manage_options`).
- An OpenAI API key with access to a chat-completions model.
  Production choice: `gpt-4o-mini` (quality passed editorial review; cost is
  roughly 0.5 to 2 cents per article including the expand pass). Keep the model
  in an option so it can be upgraded without a deploy.
- WP-Cron working (or a real cron hitting wp-cron.php; on managed hosting this
  usually just works).

## 4. Data model

Custom post type, for example `justice_term` (on nad-lan it is `nadlan_term`):

- public, has_archive (the encyclopedia hub page), rewrite slug for example
  `/encyclopedia/` or `/law-wiki/`, supports title, editor, excerpt.
- `show_in_rest => true` so wp/v2 REST works for auditing.

Taxonomy `justice_term_cat` (hierarchical, the domain tree).

Post meta (register with `register_post_meta`, sanitize_text_field, single):

| Meta key | Purpose |
|---|---|
| `name_en` | The attached English term. Doubles the search surface. Rendered as a chip under the title. |
| `entity_type` | One of a fixed whitelist. For legal: `term, law, regulation, ruling, court, procedure, role, person, organization, publication, form, doctrine`. Unknown values fall back to `term`. |
| `enc_domain` | Free-text domain label (also mapped to the taxonomy). |
| `enc_priority` | 1, 2 or 3. Drives BOTH writing order and article depth tier. |
| `enc_related` | Comma list of related entry titles, woven into the text by the writer. |
| `enc_sources` | Source direction hints for the writer (names of laws, standards, official bodies). |
| `enc_fail_count` | Internal: incremented on each validation failure; 5+ parks the entry. |
| `enc_written_by` | Internal: `site-writer:<model>` provenance stamp. |
| `enc_written_words` | Internal: validated word count. |

### The tier system (the depth contract)

| Priority | Target words | Hard floor | Use for |
|---|---|---|---|
| 1 | 800-1300 | 700 | Cornerstone entries (for legal: major laws, landmark rulings, core doctrines) |
| 2 | 450-700 | 400 | Standard professional entries |
| 3 | 250-400 | 250 | Narrow or niche entries |

The floor is enforced in code, not trusted to the prompt (see gotcha 1).
After the expand pass a 10% tolerance band applies to the floor (see gotcha 3).

## 5. Component: intake endpoint

`POST /justice/v1/glossary-intake` - permission: `current_user_can('update_plugins')`
(admin app password over HTTPS).

Body: `{"entries": [ ... ], "per_day": 12}` where each entry is:

```json
{
  "name_he": "the title (required)",
  "name_en": "English term",
  "entity_type": "law",
  "domain": "family-law",
  "priority": 1,
  "def": "one-line basic definition (becomes the excerpt)",
  "related": "entry A, entry B",
  "sources": "the statute name, official body",
  "content_html": "OPTIONAL full article HTML"
}
```

Behavior rules, in order, per entry:

1. Empty title -> skip, count it.
2. Duplicate title lookup. If an existing post is found:
   - If it is a DRAFT under 250 words AND the incoming entry has real
     `content_html` -> STAGE-2 FILL: update that draft in place (this lets a
     two-stage ontology-then-articles workflow work). Never touch a published
     or already-scheduled post - no silent overwrites, ever.
   - Otherwise -> skip as duplicate.
3. Word-count the incoming content (strip tags first). 250+ words -> it is a
   real article: schedule it as a FUTURE post on the drip. Under 250 (including
   empty) -> create as a plain DRAFT skeleton awaiting the writer.
4. Content passes through `wp_kses_post`. Excerpt = the `def` line.
5. Write all meta (with the entity_type whitelist fallback), set the taxonomy
   term from `domain`.
6. Respond with counters: created, scheduled, drafted, skipped, first and last
   scheduled datetime, per_day.

### The drip slot algorithm (used by intake AND writer)

- Cadence: `per_day` posts (default 12) spread across 09:00-19:00 local time,
  i.e. one slot every `10h / per_day`.
- Resume, never restart: find the latest already-scheduled (`future`) post and
  continue after it; if a day already holds `per_day` posts, roll to 09:00 the
  next day. If nothing is scheduled, first slot is now + 1 hour.
- Any computed slot in the past gets pushed to now + a small offset.

## 6. Component: the writer (the heart)

File pattern: one hourly cron + one write-one function.

### Scheduling and caps

- `wp_schedule_event(time()+600, 'hourly', 'justice_enc_writer_tick')` guarded
  by `wp_next_scheduled`.
- Options: `enc_writer_enabled` (1), `enc_writer_model` (`gpt-4o-mini`),
  `enc_writer_daily` (15 = generation cap per day). Per-tick batch cap: 3
  (keeps each cron run short; hourly ticks reach the daily cap naturally).
- Daily stat option `{date, generated, failed}` resets when the date changes.
  Room = daily cap minus generated; zero room -> return.

### Selection

`WP_Query`: post_type = the CPT, status draft, `orderby meta_value_num
enc_priority ASC` (cornerstones first), meta_query `entity_type EXISTS`
(only ontology-born skeletons, not random drafts), fetch `batch * 2` ids.
Per candidate, skip if:

- `enc_fail_count >= 5` (parked as stuck - needs a human look), or
- existing content already 250+ words (already written).

### The call

`wp_remote_post` to `https://api.openai.com/v1/chat/completions`, timeout 120,
Bearer key from the option, body:

```json
{"model": "<option>", "temperature": 0.4, "max_tokens": 6000,
 "messages": [{"role": "system", ...}, {"role": "user", ...}]}
```

### The system prompt (translate/adapt the bracketed parts for legal)

Hebrew, one block. The production prompt, structurally:

> You are chief editor of a professional [real-estate/legal] encyclopedia in
> Hebrew, at Wikipedia level and above. The reader is a professional. Hard
> rules: ZERO invented facts - an uncertain datum is omitted; no long dash of
> any kind (regular hyphen only) [site style law - keep or drop per site]; the
> English term integrated in the body text; clean HTML only: h2, h3, p, ul,
> li, table, tr, th, td; no h1, no opening title (the title exists on the
> page), no marketing summary, no addressing the reader. Open directly with a
> definition paragraph. Structure: definition; background or mechanism;
> technical detail with numbers and references to the statute/standard where
> they exist; the Israeli context; "in a real case/project" - how a
> professional meets this in practice; a numeric example or formula where
> fitting; common mistakes; a matter-of-fact closing sentence. Section
> headings must be phrased naturally per entry, not copied from this structure
> list. For entries about people or companies: neutral biographical facts with
> dates only. Target length: [lo] to [hi] words. Return ONLY the HTML body,
> no code fences.

For jus-tice.co.il swap the domain framing: "the Israeli context" becomes
statutory basis + key case law; "in a real project" becomes "in a real
proceeding"; sources are statutes, regulations and rulings. Keep the zero
invented facts law verbatim - it is what makes unsupervised publishing safe.
For rulings and case-law entries consider adding: cite only case numbers and
parties that appear in the input metadata; never invent citations.

### The user prompt

One line assembled from the skeleton:

```
Write the full encyclopedia entry for: "<title>" (EN: <name_en>)
 | entry type: <entity_type> | domain: <enc_domain>
 | basic definition: <excerpt> | related entries to weave in: <enc_related>
 | source directions: <enc_sources> | mandatory length: at least <lo> words.
```

The mandatory length repeated here matters (see gotcha 1).

### Post-processing and validation (deterministic, in code)

1. Take `choices[0].message.content`, trim.
2. Strip markdown code fences (`^```(html)?` and trailing fences) - models add
   them despite instructions.
3. Style law transforms if the site has them (nad-lan: replace en/em dashes
   U+2013 and U+2014 with a regular hyphen).
4. `wp_kses_post` the whole thing.
5. Word count on the tag-stripped text.

### The expand pass (gotcha 1 - the most important mechanism)

If the draft is non-empty but under the tier floor: append the draft as an
assistant message plus a user message:

> The entry currently has only <wc> words and the target is <lo> to <hi>
> words. Expand and deepen it: detail the technical mechanism, the
> [Israeli/legal] context, a numeric example and common mistakes as missing,
> with no filler and no invented facts. Return only the full expanded entry,
> same HTML rules.

Call again; keep whichever result is longer. Then apply a 10% tolerance to the
floor (floor = floor * 0.9). Still under -> record failure telemetry
(option `enc_writer_last_fail` = {pid, title, words, floor, at}), increment
`enc_fail_count` on the post, return false; it retries next tick and parks
after 5 failures.

### Final cleanup and drip hand-off

- Strip a duplicated opening `<h2>` or `<h3>` that equals the post title
  (models repeat the title despite instructions; strip it deterministically).
- Compute the next drip slot (same algorithm as intake).
- `wp_update_post` with post_content, `post_status => 'future'`, post_date,
  AND `edit_date => true` (gotcha 2 - without this the whole drip silently
  collapses to instant publishing).
- Stamp `enc_written_by` and `enc_written_words` meta.

## 7. Component: status endpoint

`GET /justice/v1/enc-writer-status` - public read is fine (no secrets in it):

```json
{"enabled": 1, "model": "gpt-4o-mini", "daily_cap": 15,
 "today": {"date": "...", "generated": 6, "failed": 15},
 "last_fail": {"pid": 5393, "title": "...", "words": 668, "floor": 700, "at": "..."},
 "stuck": 0, "skeletons_waiting": 194, "scheduled_to_publish": 3, "published": 30}
```

This endpoint is how the owner (and any agent) supervises the machine without
opening wp-admin. `last_fail` and `stuck` exist because "generated: 0,
failed: 6" with no reason cost a full diagnostic cycle in production.

## 8. Component: key storage

`POST /justice/v1/keys` body `{"openai_key": "sk-..."}` - permission
`manage_options`. Stores to an option (autoload false), responds with only a
prefix and length, NEVER echoes the key. A tiny helper
`justice_ai_openai_key()` reads it everywhere. The owner pastes the key once
(over an authenticated HTTPS call), and it never appears in code, git, or
responses.

## 9. Page decorations (optional, recommended)

- EN-term chip: a `the_content` filter on the CPT rendering
  `EN: <name_en> · <entity_type>` as a small pill under the title.
- JSON-LD: `DefinedTerm` schema per entry (for legal consider `Legislation`
  schema for law entries).
- Autolinker: scan published entry titles and link first occurrences in other
  content, capped (nad-lan: 4 links per page) to stay natural.
- A-Z / domain archive as the hub page.
- Anti-cannibalization: before ingesting a batch, check new titles against
  existing site pages that already rank for that topic; drop or merge
  collisions. On nad-lan this pruned 2 of 200 in the first batch.

## 10. HARD-WON GOTCHAS (all hit in production - do not relearn them)

1. **LLMs undershoot long-form word targets. It is not truncation.**
   First production tick: 0 generated, 6 failed. Diagnosis: HTTP 200,
   `finish_reason: "stop"`, 1114 of 3000 tokens used, output 422 words against
   an 800-1300 brief. The model just stops early. Fixes that work together:
   the mandatory minimum repeated in the user prompt, max_tokens with real
   headroom (6000), the expand pass (measured count sent back with the
   target), and the 10% post-expansion tolerance. With all four: 6 of 6
   generated in the next ticks, zero failures.
2. **WordPress silently discards post_date on draft updates.**
   `wp_update_post` on a draft whose `post_date_gmt` is `0000-00-00 00:00:00`
   resets a passed `post_date` to NOW unless `edit_date => true` is passed.
   Status `future` + date now = instant publish. Symptom: your entire drip
   schedule works in testing with `wp_insert_post` (new posts) and silently
   collapses in production with `wp_update_post` (filling drafts). Set
   `edit_date => true` on EVERY drip hand-off that updates an existing post.
3. **Fail-looping burns the API budget at the queue front.**
   Priority-ordered selection means a stubborn entry (for example an
   organization entry that honestly cannot reach 800 words without inventing
   facts) is retried at the front of EVERY tick forever. The 10% tolerance
   plus the `enc_fail_count >= 5` parking (surfaced as `stuck` in status)
   guarantees the queue always advances.
4. **Models wrap output in code fences and repeat the title as a heading**
   despite explicit instructions. Strip both deterministically in code; never
   rely on the prompt alone for format guarantees.
5. **Always send the failure reason somewhere you can read.** The single most
   time-saving feature was `last_fail` {title, words, floor}: it turned the
   next incident from "run a server-side diagnostic" into "read one field".
6. **Diagnose with a FULL-fidelity reproduction.** A simplified test call
   (short prompt, same params) succeeded while production failed; only
   reproducing the exact system+user prompts on a real skeleton revealed the
   undershoot. Build the diagnostic as a temporary endpoint that returns
   http code, api error, finish_reason, token usage, and word counts.
7. **Zero invented facts is the license to publish unsupervised.** The prompt
   must order omission of uncertain data. For a legal site this is doubly
   critical: an invented citation or misstatement of law is worse than a
   short article. Prefer a failed floor over padded fiction.
8. **Publish on a drip, not in bulk.** Hundreds of AI articles appearing in
   one day is the classic scaled-content-abuse footprint. 12-15 per day across
   working hours, with a real quality gate, reads like an editorial team.
9. **Third-party AI plugins are not the answer.** Evaluated and rejected: no
   entity model, no tiers, no style laws, no drip, and one connector plugin
   fataled the whole site on activation. ~250 lines of first-party PHP replace
   them entirely.
10. **Never let the key leak.** Store in an option via an authenticated
    endpoint; log prefixes and lengths only; the status endpoint carries no
    secrets; rotate a key that ever passed through a chat.

## 11. Cost model (production numbers)

With `gpt-4o-mini` (input ~$0.15 / output ~$0.60 per 1M tokens): an article is
~500 prompt + ~1100-2500 completion tokens; the expand pass roughly doubles
the short cases. Real-world: about 0.5 to 2 cents per article, so a 2,500
entry encyclopedia lands around $15-50 total spread over months. At 15
articles per day the monthly spend is under $10. Keep the model an option:
upgrading cornerstone entries to a stronger model later is a one-option
change, no deploy.

## 12. Build order + acceptance checklist

Build order:
1. CPT + taxonomy + meta registration + archive page.
2. Key storage endpoint; store the key; verify with one authenticated
   server-side test call (a 401 from an unauthenticated probe proves nothing).
3. Intake endpoint; ingest a 10-entry test batch; verify drafts + meta + dupes
   + the stage-2 fill path.
4. Writer with everything in section 6 INCLUDING the expand pass, tolerance,
   fail counter, edit_date, and telemetry from day one.
5. Status endpoint.
6. Decorations (chip, schema, autolinker, hub).

Acceptance checklist (each was a real production check):
- [ ] Intake: batch of N -> correct created/scheduled/drafted/skipped counters.
- [ ] Duplicate title -> skipped; published posts never overwritten.
- [ ] Stage-2: thin draft + incoming article -> filled in place, enters drip.
- [ ] Writer tick generates > 0 on real priority-1 skeletons.
- [ ] Generated article: opens with a definition, sections natural, no h1, no
      code fences, no title repetition, word count >= tier floor, style laws
      hold (run a dash scan if adopted).
- [ ] Scheduled posts appear with `future` status at the expected drip
      intervals (for 12/day: 50 minutes apart) - and do NOT publish instantly.
- [ ] Daily cap respected across multiple ticks.
- [ ] A forced-fail entry increments enc_fail_count and shows in last_fail;
      after 5 failures it stops being selected and shows in `stuck`.
- [ ] Status endpoint returns all counters and no secrets.

## 13. Adaptation notes for jus-tice.co.il specifically

- Entity types: `term, law, regulation, ruling, court, procedure, role,
  person, organization, publication, form, doctrine`.
- Priority-1 candidates: foundational statutes, landmark Supreme Court
  rulings, core doctrines. Priority-2: standard procedures, common forms,
  roles. Priority-3: narrow terms.
- Add to the system prompt: cite statutes by their official name and year;
  case citations only from the input metadata, never generated; where the law
  changed over time, state the current position and date it.
- `enc_sources` per entry should name the statute/regulation so the writer
  anchors to it instead of improvising.
- A visible disclaimer on every entry ("general legal information, not legal
  advice") is standard for legal content sites - render it via the same
  `the_content` filter as the EN chip.
- The ontology batches themselves are best produced by a deep-research AI
  session per domain (family law, labor law, torts...), 100-200 entries per
  batch, delivered as the intake JSON. Two-stage workflow supported: titles
  first (skeletons), long articles later (stage-2 fill), or skip stage 2
  entirely and let the writer do all the writing.
