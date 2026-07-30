# Five-Language Project Page End-to-End Runbook

## Purpose

This runbook turns one real-estate project into a public buyer page in Hebrew, English, French, Russian and Arabic without changing unrelated projects or inventing facts. It covers research, search intent, writing, media, 3D, WordPress integration, release safety, browser QA and post-release proof.

The finished page is for a person considering an apartment purchase. Internal SEO terminology, research notes, validation commentary and production instructions must never appear in the public article.

## Non-negotiable gates

The release stops if any of these conditions fails:

1. The target project identity is not certain.
2. A fact lacks a public source or is presented more strongly than its source permits.
3. Any language has fewer than 5,000 useful words.
4. A current official price, delivery date, inventory list, view or amenity is implied when it was not published.
5. Media rights are unclear.
6. Apartment-level model interaction is shown without an official apartment stack, BIM data or equivalent source.
7. Canonical or hreflang URLs point to missing, redirected or wrong-language pages.
8. A shared-engine change affects another project.
9. Desktop or mobile browser QA has a functional, language, console or layout failure.
10. A recoverable before-state, release lock and tested rollback do not exist.
11. Real Google Chrome search-intent evidence is missing for any language.
12. The candidate does not descend from the exact source installed in production at release time.

## Phase 1: lock the target and preserve the current site

### 1.1 Confirm the production identity

Record:

- exact public project name;
- live slug and URL;
- WordPress post type and post ID;
- current language siblings;
- developer;
- official project URL;
- current canonical and hreflang set;
- current featured media;
- current 3D model URL and checksum;
- current REST response checksum.

Do not trust the slug alone. A release migration must require the approved post ID, expected post type, exact slug, project name signal, expected source URL and a durable project identity marker. A translated slug that already belongs to an unmarked post is a hard collision, not a post to overwrite.

For UTOPIA the approved base is:

- post ID: 4749;
- slug: `utopia-sde-dov`;
- URL: `https://nad-lan.co.il/projects/utopia-sde-dov/`;
- official source root: `https://utopiatlv.co.il/`;
- durable identity family: `nadlan-utopia:lot-103:base-4749:{language}`.

### 1.2 Work outside the owner's checkout

1. Inspect the owner's checkout and record its branch, commit and dirty files.
2. Do not clean, reset, move or overwrite user-owned changes.
3. Create an isolated worktree from the exact commit that matches production.
4. Record production version, production commit, `origin/main` commit and any pre-existing drift.
5. Limit changes to the target project, target media, target content, inert styles and conditional runtime branches.

UTOPIA development was isolated in:

- worktree: `C:\Users\pro\nad-lan-utopia`;
- development branch: `codex/utopia-perfect-1.72.128`.

That branch is a research and implementation workspace, not a release base. Production changed while UTOPIA was being built. Before packaging, create a fresh release worktree from the exact commit corresponding to the currently installed production version. Transplant only the reviewed UTOPIA allowlist. Manually update the plugin module include and release version on that fresh source. Never merge, rebase or cherry-pick the old development branch over a newer production plugin tree.

Re-check the public health endpoint immediately before source alignment and again before building. A version observed earlier in the task is not a reservation. If production advances, discard the unshipped integration worktree and repeat the alignment from the new exact source.

### 1.3 Capture the before-state

Capture before editing:

- desktop screenshot at 1440 by 1000;
- mobile screenshot at 390 by 844;
- DOM snapshot;
- title, description, canonical, hreflang and schema;
- H1/H2 sequence and first crawlable text;
- word count;
- model request, byte size and SHA-256;
- featured-media request, byte size and SHA-256;
- console and page errors;
- target REST response and SHA-256;
- REST responses and SHA-256 values for comparison flagships in all available languages.

Store the machine-readable baseline in `docs/qa/`. Store visual evidence in the task evidence directory. Make every network artifact immutable by recording its URL, capture time, byte count and SHA-256. Do not overwrite a before screenshot or baseline JSON with a later run. Record known defects before making changes so they are not later attributed to the release.

UTOPIA baseline: `docs/qa/utopia-before-state-2026-07-29.json`.

The UTOPIA comparison set is DUO, Rainbow Tel Aviv, Dimri Yama and Ashira Sde Dov. Capture every available language and both desktop and mobile states. For projects with mature showroom features, include the initial model, a selected apartment or building, the detail panel, interior-design entry, cinematic/window view, map orientation, nearby-place layers and language navigation wherever those controls exist. A simple HTTP or model-click check is not a sufficient baseline.

## Phase 2: research how buyers search

### 2.1 Use the real Google Chrome browser

Search in the real browser before writing any public copy. Do not rely only on a keyword API or a generic web search.

For each language:

1. Connect to the installed, user-visible Google Chrome browser and verify the connector with a tab-list call.
2. Open a fresh tab for the language. Do not substitute an API result or a headless-only browser capture.
3. Use the matching Google market and interface language: Google Israel for Hebrew, Google.com in English, Google France in French, and an explicit Russian or Arabic interface and geography appropriate to the intended reader.
4. Verify Chrome has not translated the Google page. Record the document language and the presence of any translation state before accepting evidence.
5. Search the exact brand plus city, apartment intent and price intent.
6. Run natural variants for floor plans, project status, location, investment and foreign-buyer questions when the results support those intents.
7. Record autocomplete suggestions from the live search box.
8. Record the visible title patterns and wording used by the strongest relevant organic results.
9. Record People Also Ask and related-search questions when present.
10. Separate project intent from same-name hotels, vacation rentals, unrelated developments or international brands.
11. Classify the visible intent: navigation, price, apartment availability, floor plans, permit status, location, investment, foreign-buyer process, financing or tax.
12. Save the Google URL, query, market, interface language, capture time and screenshot. Write a short intent brief before drafting.

UTOPIA search set:

- Hebrew: `UTOPIA שדה דב דירות מחיר`
- English: `UTOPIA Sde Dov Tel Aviv apartments for sale price`
- French on Google France: `UTOPIA Sde Dov Tel Aviv appartements à vendre prix`
- Russian: `UTOPIA Сде Дов Тель-Авив квартиры купить цена`
- Arabic: `UTOPIA سديه دوف تل أبيب شقق للبيع السعر`

Use the search language naturally in the article. Do not paste awkward variants repeatedly. The title and opening should resolve the dominant ambiguity immediately: this is the UTOPIA residential project in Sde Dov, Tel Aviv.

UTOPIA intent brief: `docs/research/2026-07-29-utopia-five-language-search-intent.md`.

Search suggestions and snippets guide wording and topic coverage. They do not prove project facts. Every factual claim still needs the source ledger.

When testing authored multilingual pages in the same Chrome profile, check for automatic browser translation before judging the copy. A translated DOM is contaminated evidence. Local preview documents may use a preview-only `notranslate` marker to preserve the authored language during QA. Do not add that marker to the public page, because public readers may rely on browser translation.

### 2.2 Write for cultural intent, not word substitution

All five versions must share the same facts, dates and source set. The decision framing may differ:

- Hebrew buyers often need planning status, contract checks, purchase tax, parking, storage and comparisons within Sde Dov.
- English-speaking overseas buyers often need exact location, non-resident process, mortgage feasibility, currency exposure and what is or is not included.
- French-speaking buyers often search `appartement à vendre`, price, financing from abroad, acquisition tax and non-resident process.
- Russian-speaking buyers often search `квартиры купить`, current price, permit status, plans, sea orientation, mortgage and currency.
- Arabic-speaking buyers often search apartments for sale, price, purchase process, financing, taxes, family suitability and verified project status.

These are reader needs, not permission to change facts or create legal conclusions.

## Phase 3: build a source and fact ledger

### 3.1 Source hierarchy

Use sources in this order:

1. statutory plans and Planning Administration documents;
2. municipal permit records and GIS;
3. official developer and architect materials;
4. official project plans and brochures;
5. dated reputable press reports;
6. calculations derived from published figures, labeled as non-binding estimates.

Search snippets are discovery aids, not factual sources.

### 3.2 Record each claim before writing

The ledger must contain:

- fact;
- exact value and unit;
- effective or publication date;
- source URL;
- source type;
- permitted wording;
- discrepancy note;
- whether the fact may appear in schema, a table, the model or only explanatory prose.

Keep unknowns explicit:

- current official price list;
- complete current inventory;
- binding delivery date;
- exact consumer street address;
- unit-specific parking and storage;
- unit-specific views;
- final management fees;
- official apartment stack or BIM model.

For UTOPIA the locked core includes 337 homes, four buildings, lot 103 in the Eshkol compound, a 5,203 square metre planning lot, the published 34/15/7/7 composition, 2 to 5-room marketing range, applications 20250165 and 20250403, early-works permit 20250566, the 18 June 2025 permit date and the 14 September 2025 work-start record.

UTOPIA source ledger: `docs/research/2026-07-29-utopia-source-ledger.md`.

### 3.3 Resolve discrepancies once

When public sources disagree:

1. prefer the current primary source;
2. explain the discrepancy once in the relevant project-stage section;
3. do not repeat it as a disclaimer;
4. never average incompatible figures.

Example: project marketing calls N1 a 15-floor building while the municipal packet describes 14 residential floors plus ground and technical levels. Both descriptions can be reported with their context.

## Phase 4: media and 3D

### 4.1 Rights-safe media

For every image record:

- source or generation method;
- creator;
- license or permission basis;
- modifications;
- project and language use;
- whether it is official, editorial or an independent concept;
- checksum and dimensions.

If official marketing images have no clear republication right, do not copy them. Produce independent concept media from public planning facts and label it once, close to the media. Do not imply an exact facade, material palette, furnished specification or apartment view.

UTOPIA uses four independent concept images:

- exterior massing context;
- interior mood;
- window-orientation mood;
- wellness mood.

Rights ledger: `assets/projects/utopia-sde-dov/rights-ledger.json`.

### 4.2 Model truth contract

Before modelling, decide the interaction level:

- building level: requires reliable building footprints, heights and orientation;
- floor level: requires reliable floor ranges and building structure;
- apartment level: requires an official apartment stack, BIM model, signed plans or equivalent mapping.

Never infer apartment inventory from sample plans.

For UTOPIA:

- model kind: independent concept massing;
- official model: false;
- asset technically validated: true;
- interaction: four buildings only;
- apartment inventory: empty;
- sample plans: seven official public examples;
- published apartment/floor references within those seven samples: 29;
- triangle count: 21,416;
- draw meshes after lossless join: 14;
- packaged size after flatten/join without simplification or extension compression: 309,148 bytes;
- GLB SHA-256: `ba267a241f7b5d943f5eebd6f32aae9241f14da420207ddadc4d5d74ac392f24`.

Each building hotspot must display source-backed floors, approximate planned maximum height, a municipal source link and only the sample plans associated with that building. Selecting one of the 29 published apartment/floor references may focus its known building and populate the enquiry context. It must not create a facade hotspot, availability signal, price, view, direction or inventory status.

The seven locked plan groups are N1 4A, N1 5G, N1 5E/C5, N1 3A, S1 5G, S1 3P and S1 4D. Preserve the official apartment and floor references exactly as published in the plan PDFs.

### 4.3 Map, window-view and orientation truth contract

The area map may show the planning-lot centroid, nearby facilities, transit, parks and other sourced context. It may not imply an apartment position or a verified line of sight.

Do not render an apartment window view, view cone, camera bearing, sea-facing claim or floor-relative horizon until all of these are verified:

- georeferenced building footprint;
- model north offset;
- official apartment stack and facade assignment;
- apartment facing or signed plan orientation;
- floor elevation;
- a dated obstruction and surrounding-development model.

Until those inputs exist, keep UTOPIA interaction at building level and state the boundary in buyer-facing language only where it helps a purchase decision. The local map adapter must remain scoped to `#utopia-showroom`; it must not write or replace shared globals such as `NLPJX_MAP` or `NADLAN_SHOWROOM`. A local preview without a Mapbox token must show the designed fallback. Production may use the existing client token, but the token must not be copied into reports, screenshots or source files.

Model validation: `docs/qa/utopia-model-validation.json`.

## Phase 5: assemble five public articles

### 5.1 Page order

The crawlable and visible order should be:

1. exact search-led H1;
2. fact-rich opening paragraph;
3. compact key facts;
4. interactive project experience;
5. overview;
6. location and surroundings;
7. buildings and apartments;
8. prices and estimates;
9. developer;
10. project stages;
11. buyer fit;
12. frequently asked questions;
13. sources.

The first paragraph must immediately include project name, city, apartments, price and purchase language in a natural way. It should establish the developer, planning locator, published home count, building composition, apartment range, price-list status and the first practical buying action.

### 5.2 Content rules

For every language:

- at least 5,000 useful words;
- one H1;
- exactly the required nine H2 chapters in order;
- short, active sentences;
- buyer decision framing;
- dates and numbers near the claims they support;
- compact tables where comparisons are easier to scan;
- one clear label on every derived estimate;
- no current inventory claim without a current source;
- no process notes, keyword discussion or AI-generation language;
- no repeated caveats;
- no long dash characters;
- no banned filler phrases;
- the same 23 real source URLs;
- natural internal links to the mortgage calculator, purchase-tax calculator, new-project buying guide, city page and Sde Dov page.

### 5.3 Language independence

Do not translate sentence by sentence. Write each language as a native buyer guide from the same locked ledger. Then run a cross-language fact audit to ensure:

- every locked number appears consistently;
- no language adds or removes a factual claim;
- press reports remain dated reports;
- calculations remain estimates;
- unknowns remain unknown;
- plan labels and source URLs remain exact.

UTOPIA content gate: `scripts/qa-utopia-content-depth.mjs`.

## Phase 6: integrate only the target project

### 6.1 Isolated project runtime

Do not change a shared showroom engine to make one project work. UTOPIA uses a project-specific renderer, payload, CSS and JavaScript under the UTOPIA asset directory.

Use:

- an exact target-family predicate that requires the approved base ID or a per-language identity marker, not a slug alone;
- `inc/utopia-sde-dov.php` for release data, identity, migration, metadata and final composition;
- `inc/utopia-showroom.php` for the UTOPIA-only showroom payload and markup;
- `projects/utopia-sde-dov/utopia-showroom.js` for local interaction and map behavior;
- `projects/utopia-sde-dov/utopia.css` for styles rooted under `#utopia-showroom`;
- UTOPIA-only model, media and article URLs;
- four building-level hotspots and an intentionally empty apartment-unit collection;
- a final target-only content composer that reads the reviewed raw article after the generic WordPress filter chain, places the factual lead before the showroom, and discards legacy project blocks only for the verified target family.

The target renderer may dequeue generic showroom scripts only after the exact UTOPIA family predicate succeeds. It must not mutate shared dictionaries, shared JavaScript globals, shared map state, model defaults or comparison-project metadata. Prefix PHP functions, DOM IDs, CSS selectors, event state and client data with the UTOPIA namespace.

Test the final rendered composition, not only the stored article. Assert one H1, no empty heading, no legacy profile/navigation classes, no language leakage, and no template-relative `home.html` or `project.html` links.

Do not:

- replace the global translation dictionary;
- change default model behavior;
- change existing unit selection;
- alter comparison project metadata;
- stack another showroom;
- transplant stale shared-engine files into the release;
- introduce a global layout correction while doing a single-project release.

The runtime release allowlist is:

- `inc/utopia-sde-dov.php`;
- `inc/utopia-showroom.php`;
- five UTOPIA article files;
- `utopia-showroom.js`;
- `utopia.css`;
- four UTOPIA concept WebP files;
- `utopia-rich-v1.glb`;
- the minimal module include and release-version edits in `nadlan-config.php`.

Treat every other plugin file as protected. Compare protected-file hashes with the fresh production source before packaging.

### 6.2 SEO and schema

For each language:

- server-render the exact title;
- publish a self-canonical;
- output reciprocal hreflang for all five pages and `x-default`;
- keep one H1;
- provide localized title, description and social metadata;
- omit Offer schema when no current official offer exists;
- omit unverified amenities;
- do not put the planning lot into `PostalAddress.streetAddress`;
- represent lot 103 as an identifier/additional property;
- describe coordinates as the planning-lot centroid;
- generate FAQPage entities from the visible FAQ content, not a separate copy.

## Phase 7: publish with an atomic, recoverable migration

### 7.1 Before any mutation

1. Permit automatic seeding only on a non-AJAX WordPress admin request from a user who has both `manage_options` and `unfiltered_html`.
2. Refuse to seed while an operator or blocked-recovery hold exists.
3. Acquire an atomic, non-autoloaded WordPress option lock.
4. Recover only a lock older than the defined stale threshold, using a database compare-and-swap against the exact serialized stale value. Never delete a stale lock unconditionally.
5. If an incomplete run journal exists, recover it before resolving translated slugs or starting another run.
6. Validate base ID, type, slug, name, source URL and identity marker.
7. Hard-stop on unmarked translated-slug collisions.
8. Validate each article against a release manifest:
   - SHA-256;
   - language and direction;
   - H1;
   - H2 sequence;
   - Unicode word count;
   - source URL set;
   - internal-link set.
9. Validate the packaged model and every packaged media file against release SHA-256 values before touching WordPress content.
10. If a marked featured attachment already exists, require exactly one marker match and verify its file path, MIME type, SHA-256 and public alt text. A marker alone is not proof that the attachment is usable.
11. Create a non-autoloaded backup option and verify its checksum.
12. Create a checksummed write-ahead run journal with a unique token before the first post, attachment or file mutation.

The backup must include:

- every post field that will change;
- original publication and modified timestamps;
- the exact pre-release revision ID set;
- every metadata key that will change;
- canonical and identity metadata;
- thumbnail metadata;
- `nadlan_city` and `nadlan_compound` terms;
- created post IDs;
- created attachment IDs;
- created upload paths.

### 7.2 Stage, validate, publish

1. Create missing language siblings as drafts. Put the run token into `post_content_filtered` in the same insert that creates each row, so recovery can identify a row even if the process stops before metadata is written.
2. Record each created ID in the run journal and backup immediately after insertion.
3. Resolve the exact upload destination and write it to the run journal before copying the file.
4. Create the rights-safe featured attachment without overwriting an existing file. Put the same run token in the attachment insert.
5. Stage and validate only new or previously non-public siblings before the public commit. Do not mutate an existing published page yet.
6. Confirm that the posts, postmeta, term relationship, term taxonomy and options tables use a transactional engine.
7. Start one MySQL transaction and suspend cache additions for the duration.
8. Inside that transaction, update every existing published language page without demoting it. Write content, title, excerpt, metadata, canonical, identity, thumbnail and both taxonomies.
9. Read every staged value back and compare it with the release manifest.
10. Publish the siblings that are still drafts and verify all five final statuses, slugs, identities and content hashes.
11. Write the release manifest and completion flag and delete the run journal with direct database writes inside the same transaction. Do not expose a completion flag through object cache before commit.
12. Commit once. A process stop before commit must leave all previously public languages on their old database state; a process stop after commit must find the direct-database completion flag and refuse a second release.
13. Restore cache behavior, clear target post and release-option caches, verify completion directly from the database, then release the lock.

On any failure:

1. roll back the open database transaction before any file cleanup;
2. restore every pre-existing post field;
3. restore every mutated metadata value;
4. restore both taxonomies;
5. restore original post dates and modified timestamps with direct database writes;
6. remove release-created revisions and verify that the original revision ID set remains intact;
7. discover and remove token-tagged rows from an interrupted run, including rows created before their identity metadata was written;
8. remove only posts with this release's identity marker or exact run token;
9. remove only the attachment with this release's asset marker or exact run token;
10. remove only the exact planned or created upload file under the WordPress upload directory;
11. read back every restored post field, full multi-value metadata set, thumbnail, timestamps, revisions and sorted taxonomy set;
12. clear completion and release-manifest options only after the restored state passes readback verification;
13. on any mismatch, retain the completion state, run journal and backup, set `blocked-recovery`, and refuse automatic reseeding;
14. retire a successfully used automatic-recovery backup so the next attempt captures a fresh baseline, then write the error.

Provide a lock-aware WP-CLI restore command. Require `--user=<administrator>` and verify both `manage_options` and `unfiltered_html` before any HTML restoration. A successful operator restore must set a persistent operator hold so the next request cannot immediately reseed. Provide a separate explicit resume command that validates the backup, confirms no incomplete run journal remains, retires the old backup so later operator edits become the fresh baseline, and removes only an operator hold.

UTOPIA 1.72.135 release QA: `python -B scripts/verify-plugin-release.py 1.72.135`, `php scripts/qa-utopia-notice-contract.php`, and `docs/qa/utopia-release-artifact-1.72.135.json`.

## Phase 8: browser and regression QA

### 8.1 Local previews

Build an exact static preview for every language using the same article, payload, CSS, JavaScript, model and localized payload that will ship. The preview may replace only environment-specific URLs and may add the preview-only anti-translation marker.

Run the checks in the installed Chrome browser with trusted clicks and taps. Automated DOM assertions supplement this review; they do not replace it.

Desktop checks for all five languages:

- HTTP 200;
- exact document title;
- expected `lang` and `dir`;
- one H1;
- first visible paragraph is the buyer lead;
- four building hotspots;
- zero apartment hotspots;
- seven sample-plan cards;
- four article media images;
- every media response returns 200 and has non-zero natural dimensions;
- model request returns GLB;
- model becomes visible;
- GLB validation reports 21,416 triangles;
- building click opens the correct localized panel;
- each of the seven plan groups exposes exactly its published references, for 29 total;
- selecting a reference updates only its known building and enquiry context;
- zero apartment facade hotspots and zero view cones;
- exactly one head canonical and six head alternates: `he`, `en`, `fr`, `ru`, `ar`, `x-default`;
- no English interface leakage in French, Russian or Arabic;
- no first-party console or page errors;
- no clipped primary controls.

Mobile checks for all five languages at 390 by 844:

- no horizontal content loss;
- every visible UTOPIA control has a minimum 44 by 44 CSS-pixel target;
- model and hotspots remain usable;
- panel can open and close;
- RTL order is correct;
- article tables and media do not escape the viewport.

Use the actual language links at least once in each direction family, rather than validating only direct URLs. Save initial, building-selected and reference-selected screenshots with a JSON report. Classify third-party warnings separately; for example, a `model-viewer` request-animation-frame timeout is not a pass or fail by itself, but it must be paired with proof that the model rendered and remained interactive.

### 8.2 Regression checks

Before and after release:

- compare REST SHA-256 for every comparison flagship and language;
- verify comparison model SHA-256 values;
- open DUO, Rainbow Tel Aviv, Dimri Yama and Ashira Sde Dov in every available language on desktop and mobile;
- test the actual controls each mature project exposes, including unit selection, detail panel, apartment design, cinematic/interior view, window view, relative floor and angle behavior, map direction, nearby-place layers, language navigation and title behavior;
- inspect console and network errors;
- confirm no UTOPIA dictionary or building UI loads on comparison projects.

Store trusted-click evidence and side-by-side before/after screenshots for every tested state. A checksum comparison proves byte parity; it does not prove that an already broken interaction works. Conversely, a browser interaction pass does not replace protected-file hash parity.

If a shared defect is discovered, document it, identify whether it existed in the immutable before-state and raise it separately. Do not expand the UTOPIA release to fix the whole site.

## Phase 9: package and deploy

1. Re-fetch every remote branch before choosing a version. Reject a number already used by any concurrent release, even when that release is not live.
2. Set the same unique version in the plugin header, cache constant, health response, migration identifiers, recovery commands, tests and distribution manifest.
3. Prove that the candidate still descends from the exact live source. Never rebuild a live plugin from a stale default branch.
4. Check repository visibility and test the manifest and ZIP URL without GitHub authentication. A private raw URL that returns 404 is not a deployment path.
5. If the default branch has drifted from production, reconcile histories in a clean integration worktree while restoring the reviewed plugin tree byte-for-byte from the candidate. Do not cherry-pick the project patch onto an older plugin.
6. Build and validate a rollback ZIP from the exact live-source commit before building the candidate. Record its version, source commit, byte count, SHA-256, entry count, CRC and rooted-path result. Keep it separate from the candidate.
7. Before replacing production, capture the exact live plugin directory and a scoped database/uploads backup. A Git tag or source commit is not operational rollback unless the matching plugin ZIP is already present and verified.
8. Set the manifest download URL only after the exact immutable ZIP has an anonymously reachable destination. When the repository remains private, use an approved public artifact host or have an administrator upload the reviewed ZIP manually. Do not replace a stale manifest with another URL that returns 404.
9. Build the candidate ZIP once with the canonical release script.
10. Require forward-slash paths rooted at `nadlan-config/`.
11. Run CRC, file-completeness and extracted-file hash checks.
12. Confirm the ZIP contains:
    - the UTOPIA module;
    - the UTOPIA showroom renderer;
    - five articles;
    - four concept images;
    - the validated GLB;
    - UTOPIA-only CSS and JavaScript.
13. Extract the ZIP to a temporary directory. Prove every extracted file is byte-identical to the linted source tree, or lint every packaged PHP file directly.
14. Compute and record the exact ZIP SHA-256. Do not rebuild after approval.
15. Commit and push the exact reviewed source and artifact through a review branch. Do not push an unreviewed release directly to the default branch.
16. Ensure the artifact and its matching source are both present on the reviewed release commit.
17. Install through the approved WordPress path. If publication is gated to a privileged non-AJAX admin request, an administrator with the required capabilities must load a normal wp-admin page after installation.

If the real Chrome browser reaches `wp-login.php` instead of an authenticated administrator page, stop before upload. Leave the reviewed candidate and rollback artifacts ready, then ask an authorized administrator to sign in. Do not guess credentials, initiate an OAuth account choice or weaken the release gate.

No live claim may be made before the installed health endpoint reports the new version.

## Phase 10: post-release acceptance

For each live URL:

- status 200;
- exact title and description;
- exact self-canonical;
- reciprocal five-language hreflang plus `x-default`;
- one H1;
- correct first paragraph;
- correct article language and direction;
- model and four hotspots work;
- no apartment inventory is shown;
- seven sample plans work;
- all 29 published apartment/floor references match their official plan groups;
- four media files return 200;
- the area map renders with the existing production token, or its designed fallback appears without a token;
- no apartment view cone, false bearing or unit-specific window view appears;
- FAQ schema matches visible questions;
- ApartmentComplex schema contains no offer and no false street address;
- no console or page errors;
- desktop and mobile screenshots match the approved preview.

Then:

1. re-fetch every comparison REST response;
2. compare with the saved baseline hashes;
3. re-fetch comparison models and compare hashes;
4. record any pre-existing differences separately;
5. save the after-state JSON, screenshots and side-by-side contact sheets;
6. verify every protected shared-plugin file remains byte-identical to the exact pre-release production source;
7. record the production health version and release commit.

For the UTOPIA release, run the read-only AFTER gate only after deployment and
the authenticated admin seeding request have completed:

```powershell
node scripts/qa-utopia-after-regression.mjs --expected-version 1.72.135
```

Release `1.72.133` was aborted without deployment after an independent release
advanced production to `1.72.134`. UTOPIA therefore resumes at `1.72.135`; do
not reuse the abandoned version.

The command fails closed before creating evidence unless the health endpoint
reports the expected release and all five exact UTOPIA URLs return HTTP 200
without redirects. A passing preflight creates a new versioned UTC-stamped
directory, replays the mature comparison journeys across all five languages at
desktop and mobile sizes, captures UTOPIA in the same matrix, compares the
available BEFORE URL/REST/model evidence, creates side-by-side contact sheets
and seals the result with a SHA-256 manifest. It blocks every non-GET request
and never writes to WordPress. Before sealing, it repeats a cache-busted
terminal probe and requires the opening and closing plugin version, five route
statuses, normalized URLs, raw source hashes and UTOPIA model hash to match.
Page-source hashes for the mature comparison set are current-availability
evidence only because the immutable BEFORE report did not record source hashes.
Blocked telemetry is normalized to method, host and path and must remain a
subset of the endpoints observed in the immutable BEFORE report.

Only after these checks pass should the five live URLs be handed off as complete.

## Reusable improvement loop

After every project:

1. add newly discovered source patterns to the research checklist;
2. add a regression assertion for every defect caught;
3. refine language-intent prompts without changing the fact contract;
4. record recurring missing developer inputs such as BIM, apartment stack, current inventory, prices and delivery;
5. request those inputs early for the next project;
6. preserve project-specific code until a pattern has succeeded on several projects and can safely become a shared feature.

The goal is not only a long article. It is a page whose facts, media, interaction, language, URLs and release path can all be independently verified.
