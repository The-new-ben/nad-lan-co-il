# nad-lan.co.il: consolidation audit of 5.10.2026 (read-only)

**Who asked:** Ben. He has many scattered sessions with unfinished jobs, isn't sure all the outputs were used, and wants everything gathered into one project.

**What this is:** one list of every piece of nad-lan.co.il work that is finished but not published, half-done, forgotten, or already live with its ticket still open.
- Nothing was changed while making it: no deploy, commit, push, Linear or Notion edit, or message to any session or person.
- This file is the only thing written, and it is not committed.

**Evidence classes used below:**
- **code** means a git, file or public-GET check was run on 5.10.2026 between about 21:00 and 22:30.
- **record** means the item was read in Linear, Notion, `claude-codex.md` or memory, and not re-checked live.
- **unknown** means it could not be verified.

## The state in numbers (code, unless marked)

**The live site**
- Live version: `1.72.429`, from `GET /wp-json/nadlan/v1/health`.
- Form leads in the last 7 days: **0** (`lead_e2e.leads_7d = 0`, `delivered_7d = 0`).
  - WhatsApp-bar clicks are not counted there. Whether leads arrive by WhatsApp is unknown.

**The production line**
- Branch `claude/apartment-experience-b1`, tip `9a291b9d` (5.10 21:25), pushed to origin.
- Its plugin source is **not** a copy of the live site (section C1).

**Git**
- 14 worktrees and 22 local branches.
- 326 branches on GitHub; 303 of them are older than 1.8.2026.
- 28 open PRs. The newest is #494, from 2.9; every other one is from August or earlier.
- GitHub's default branch `main` is stale: last commit 14.8, and 779 of its commits are not in the production line.

**Linear (record)**
- 79 open nad-lan issues in team Hadmaia, updated since 5.9.
- About 30 of them are already live but still open.

**Notion "מרכז הבקרה של הפרויקטים" (record)**
- 74 nad-lan rows are not marked הושלם:
  - 45 stale;
  - 13 waiting on Ben;
  - 7 active;
  - 9 probably done.

**The owner board** (artifact `Sot2mJCpiWSiEwEwMtErxL`): last updated **30.9 22:20, at version 1.72.372**. The law says to update it after every release, and 57 releases have gone out since.

**One law from today changes many "waiting" items.**
- Ben said on 5.10: "הכל מאושר: תעלה ואז תשלח קישורים. אל תשאיר חומר לא מפורסם." The memory file is `nadlan-publish-and-links-law`.
- So an item blocked only on "Ben's OK to publish" can be published by main now.
- Only these still need Ben:
  - keys or passwords;
  - payments;
  - a third party's consent;
  - licence, legal or business choices.
- The "Who" column below follows that rule.

**Priority key:**
- **P1:** leads and money.
- **P2:** traffic, trust and legal exposure that feed leads.
- **P3:** product quality.
- **P4:** cleanup.

---

## A. Every item

Status words:
- **LIVE, ticket open:** the work is on the site but its Linear issue or Notion row is not closed.
- **FINISHED NOT PUBLISHED:** the work is done but is not on the site.
- **HALF-DONE:** the work is started but not finished.
- **STALE / ABANDONED:** no activity, or overtaken by later work.
- **DUPLICATE:** the same work is recorded twice.

### A1. Leads, money, brokers, listings

| # | Item | What exists | Status | What is missing | Who | Pri |
|---|---|---|---|---|---|---|
| 1 | **Owner listing journey `/post-listing/`** (owner-wizard 2.0.x + broker-drop 1.1.4) | Worktree `.claude/worktrees/agent-a61b211e083144352`, branch `worktree-agent-a61b211e083144352`, 23 commits not in production, tip `2c428852`, the runner `scripts/had-256/deploy_had256.py`. Docs: `docs/qa/had-256/RELEASE.md`, `README.md`, `THEME.md`. Staged DB proof passed on live MariaDB (`95e4b377`). Linear HAD-256 In Progress. Notion row 3eeab55b…d5 | FINISHED NOT PUBLISHED (being worked on tonight, 21:03) | 1. Pick 2.0.1 (`e28df264`, main's pick at 20:49) or 2.0.2 (`d83de8b8`/`85fa0b67`, committed after it).<br>2. The page 4958 wording: old, A or B (`771abcf4`).<br>3. The private photo folder: inside or outside the web root.<br>4. SMTP credentials and a test mail (same blocker as HAD-260).<br>5. Run the runner, then merge the branch into production | main; Ben for SMTP only | P1 |
| 2 | **Broker plan price differs between languages, live** | Checked by public GET on 5.10: `/brokers/` shows 349 / 3,490 / 1,490; `/en/brokers/` shows **149** and 1,490; `/fr/brokers/` and `/ru/brokers/` show **149**. Only the Hebrew page was changed (`f392e1f0`). Still 149: `scripts/broker-drop/pages/brokers-{he,en,fr,ru}.html`, `.claude/skills/broker-minisite/SKILL.md:79`, `RECEIPT-BROKER-OFFER-2026-09-23.md`. Linear HAD-395 Todo, HAD-257 In Review; Notion #11 and #47 | HALF-DONE (code) | Ben ruled Pro = ₪349 on 28.9 (memory `nadlan-owner-decisions-2026-09-28`). Update the en/fr/ru pages and every repo source so a republish cannot bring 149 back | main | P1 |
| 3 | **Nobody can pay on the site** | Linear HAD-184 In Progress (no activity since 17.9). Notion row "קופה: Pro יוצא 0 (קופון)…". The `firstmonth` coupon brings Pro to ₪0, there is no recurring charge, and the Morning API key is missing | WAITS ON BEN | The Morning key in wp-admin; recurring or one-off billing; a ₪1 test purchase | Ben only, then main | P1 |
| 4 | **First broker sale plan** (a ₪1,490 broker site, 4.10 to 11.10) | Session "מוצר ראשון למכירה — 2026-10-01" (local_047b0b73) has message drafts for Meital and ABI. Notion 3ecab55be7a18175bcc6e634d30f70be; Linear HAD-389 Backlog. A side chip to list 30 brokers was offered; no session for it exists (it was probably never started) | STALE: inside its own window, no step ticked | A payment link and invoice (Ben), sending the two messages (Ben), and the 30-broker list (a side session) | Ben only, then main | P1 |
| 5 | **Broker Gili** (biyar.co.il) | `docs/brokers/biyar-2026-10/` (`275b3a49`, local): call prep and 32 screenshots. Private preview https://claude.ai/artifact/SaHzBmdpGeHK9zRJTxxXbN. Linear HAD-394 In Review; Notion #11 | FINISHED NOT PUBLISHED (private by design) | Ben's green light to approach him. His licence: no active register row for גיל נסים. The promise to pin his apartments to the Kikar picker is not built. The price (row 2) | Ben only | P1 |
| 6 | **Meital Katzir**: her WhatsApp update link is broken | Linear HAD-384 Backlog: diagnosed 1.10 (`claude-codex.md:922-926`: she most likely holds the link replaced on 23.9, price updates are refused, the WhatsApp update was never built), not fixed. HAD-217 In Progress (her written OK). HAD-252 Backlog ("מדלן" appears 55 times). Her 11 listings have lat/lng 0. Notion #15 (urgent bug, untouched) and #48 | HALF-DONE | Fix it with the rentals pattern (token after `#`, stored as SHA-256, revocable), then send her the current link. Ben gets her written OK | main; Ben (message) | P1 |
| 7 | **New broker ABI נכסים** | Linear HAD-385 Backlog; Notion #14 (owner Codex). No work anywhere | STALE | Ben's go, then research and a site, like Gili | Ben, then main | P1 |
| 8 | **Batch 2: a design request per apartment** (design system v102, UnitDesignRequest), plus parts of Batch 1 v101 and v101.2 | Commits `6286d747`, `644d0025`, `65760d31` on the production line. Files: `inc/rfp.php`, `inc/lead-e2e.php`, `assets/showroom-engine/studio.js`, `buyflow.js`, `assets/project-stage/bridge.js`, `assets/tours/designer-tour.html`. Frozen build at `C:\Users\777\nad-lan\_journey-b2\` (manifest 24073ee8af4f). `claude-codex.md:213` says "NOT released", and no later runner ships these files (code: no deploy3xx/4xx file lists rfp.php after 366). Linear HAD-346 and HAD-329 Backlog; Notion #17 and #20 | FINISHED NOT PUBLISHED (since 29.9) | Rebase onto the live text (the repo's project-stage.php has drifted). Fix the known defects: a retried send can create a second lead; the phone studio does not reopen; the 320 px layout. Maya's QA, then release. Live leads carry no `lead_key` today | main + Maya | P1 |
| 9 | **Site leads do not reach HubSpot** | Linear HAD-220 In Progress (no activity since 17.9); Notion #52 "HubSpot לכל הלידים" waits on Ben. Health shows 0 form leads in 7 days | STALE / WAITS ON BEN | Ben: the email-footer business details and the plan choice. Then main builds the form wiring and checks that the forms deliver at all | Ben, then main | P1 |
| 10 | **The developers' film** (50 s, no voice) | `scripts/project-video/out/nadlan-developers_{1920x1080,1080x1920}{,_web}.mp4` plus posters, rendered 28.9. Ignored by git. `/developers/` and `/film/` still play `uploads/2026/08/nadlan-developer-film-hq.mp4` (code, public GET 5.10) | FINISHED NOT PUBLISHED | Upload it and swap the source on both pages (covered by the 5.10 law) | main | P1 |
| 11 | **A developer product and price; recruiting developers** | Owner board item q-devprice (no price yet). Notion "מודל הכנסה בלי תיווך ופנייה ליזמים" (stale since 24.9); HAD-195 | WAITS ON BEN | The developer price, then the list of developers and the package | Ben only | P2 |
| 12 | **Self-serve buying: a reservation and a personal apartment file** | Linear HAD-358 Backlog (epic, 10 boxes unticked); design v93; owner board item q-pay | WAITS ON BEN | Approve the flow up to the legal line, then build it | Ben, then main | P2 |
| 13 | **The video call in the shared room** (LiveKit) | The room has been live since 1.72.334 without video. The `nadlan_tr_lk_*` options are empty. Owner board item q-livekit; Notion "חדר צפייה משותף" (stale) | WAITS ON BEN | Paste 3 values at wp-admin, page `nadlan-together` | Ben only | P2 |
| 14 | **Rentals v2 for real landlords** (HAD-383) | Branch `claude/rentals-proptech-v2`, 54 commits not in production, worktree `.claude/worktrees/bold-cray-ad2cea`. Live since 1.72.404/406/408 for **administrators only**, plus the public guide (1.72.410). `docs/rentals/audience-decision.md` (on that branch) recommends option C, a pilot. Hidden WooCommerce drafts 8138 (₪39) and 8139 (₪199). Linear HAD-383 and HAD-401 In Progress; Notion #8 | LIVE for admins, WAITS ON BEN | Ben: the audience (A, B or C), the prices, the first client's email, counsel and which payment company. Before any flip, close the security finding: `/rm/*` checks login only, so any logged-in user reaches the v2 API (`claude-codex.md:2526`) | Ben; the rentals session or main for the security fix | P1 |
| 15 | **Rentals films** | Landlord film `docs/design-lab/films/rentals/rentals-{he,en}-{16x9,9x16}.mp4` (64.5 s; temporary voice that mispronounces words; the voice reference came from EcoCity material). Tutorial `films/rentals/tutorial/` (90 s, silent, "טיוטה פנימית · לא לפרסום" burned into every frame, no English 9x16). Notion #9 and #10 | FINISHED NOT PUBLISHED, blocked | Re-render without the draft tag, re-voice or stay silent, and open v2 to the public first | the producer, then Ben | P3 |
| 16 | **Maya's 3D building for /my-rentals/** ("R3") | Built in her lab on 127.0.0.1:47919 (`docs/coordination/codex-cyprus-rentals-local-2026-10-03.md`, untracked). Never acknowledged (`claude-codex.md:3255`) | FINISHED NOT PUBLISHED | Decide whether it or the rentals session's `rm-3d.js` is the one. Maya's diff disables the map for the lab only, and that part must not ship | the rentals session or main | P3 |
| 17 | **Demo content still live** (7 demo listings 4951-4957, 15 demo professionals) | Linear HAD-248 Backlog and HAD-219; Notion #33 and #49 (the same decision twice) | WAITS ON BEN | His word to move them to draft. The seeded ratings were dropped in 1.72.362 | Ben only | P2 |
| 18 | **Import the 24,724 registered brokers** | Linear HAD-250 Backlog; rescoped on 24.9 to a sample from luxury areas | STALE | Scope and sitemap decision | Ben, then a side session | P3 |

### A2. Kikar Hamedina (HAD-375 / 380 / 381 / 421 / 433)

| # | Item | What exists | Status | What is missing | Who | Pri |
|---|---|---|---|---|---|---|
| 19 | **Kikar English and Russian pages not in Google** | `docs/loop/KIKAR-HAMEDINA-LOOP.md:114` (V8 unticked): EN "Discovered, not indexed", RU unknown. Re-inspect around 9.10 | WAITS ON BEN | Asking Google to index is a Search Console write, so it needs his word | Ben, then main | P2 |
| 20 | **Who answers WhatsApp in French, Russian and Arabic** | LOOP:1270 (question Q3, 30.9) | WAITS ON BEN | A name or a routing rule | Ben only | P2 |
| 21 | **Kikar owners and sellers** (supply of real apartments) | Linear HAD-387 Backlog; Notion #13. Every box unticked | STALE | Research from public bodies only | a side session | P2 |
| 22 | **Press facts of 5.10 onto the pages; the traffic and business plan** | `docs/research/2026-10-05-kikar-press-facts.md` (`9a291b9d`), P1-P13 "not yet on them". Linear HAD-433 Backlog; Notion #1 waits on Ben | HALF-DONE (started today) | Ben approves the direction and the celebrity-names question, then main writes | Ben, then main | P2 |
| 23 | **Film decisions left after going live** (V6) | Live 1.72.417-419. Open: voice-reference rights and a human listening (F08); whether the map credit stays on the end card; the players' download button. Linear HAD-380 In Progress; Notion #5 | LIVE, ticket open | Ben's three answers, then tick V6 | Ben only | P3 |
| 24 | **Unused films in the media library** | The no-voice "noaround" cut was uploaded as 8160-8167 and is not shown. Also: the old v2 review copies 8130-8137, the V1 duplicates 8122-8124, the old Rainbow v79 8106-8109 | STALE | Use them or delete them. Deleting media is permanent, so it is his call | Ben only | P4 |
| 25 | **Licence: stored Mapbox walking areas on 5 projects** | Linear HAD-406 Backlog (High): storing the results "breaks the terms on all five projects". The MIT notice is missing in `place-icons.js` (`claude-codex.md:2696`) | HALF-DONE (not started) | Replace them from open data, and add the notice | main + Maya QA | P2 |
| 26 | **Phone speed track** (HAD-421) | Steps 1-9 live (1.72.420-428). Paused "until the owner's word" (`claude-codex.md:3834`). Linear state is **Backlog** | LIVE, ticket open | Continue or stop. Remaining: the world's own build CPU, WooCommerce scripts on project pages, Leaflet in the showroom and profile modules | Ben (go or stop) | P3 |
| 27 | **New defects** | HAD-431: the accessibility button covers the film button (rainbow-fr at 1366, Dimri he at 1280), caused by 1.72.429. HAD-425: 12 project pages have no area map. HAD-426: the /projects/ hero flickers on phones | HALF-DONE (not started) | Design first, then a release | main | P3 |
| 28 | **Execution queue tasks 02-10 and 12** | `docs/coordination/codex-kikar-execution-2026-10-02.md` (untracked). Examples: map beam cone0/viewnull; the basket is Hebrew only (`inc/basket.php:23`); task 05, the map rail clipping and the hero-walk Escape | STALE since 3.10 | Pick them up as one package | main + Maya | P3 |
| 29 | **P9 "masterpiece" sub-items** | LOOP:1276-1286: generic EN/AR place names, pinch gestures, a check on Ben's iPhone, the full-size evening interior, the twist direction from a source, the shared room wired to the world | STALE ("IN PROGRESS" since 30.9) | Re-plan or drop | main | P4 |

### A3. Urban renewal (HAD-392..412)

| # | Item | What exists | Status | What is missing | Who | Pri |
|---|---|---|---|---|---|---|
| 30 | **Linked articles still carry the old wrong figures** (/pinui-binui/, /tama-38/, the glossary) | `docs/qa/had-396/article-conflicts.md` (on the urban branch). `claude-codex.md:2549` "LISTED, not edited" | HALF-DONE | Fix them to match the corrected calculator (honesty law) | main | P2 |
| 31 | **8 pages without the site header, or with two h1s** | Linear HAD-412 Backlog; assigned to urban, which has had no commit after `82f41176`. Affected: auction, login/signup, global, site-map, advertiser-center, studio, compare | HALF-DONE (not started) | One package, design first | the urban session or main | P3 |
| 32 | **Renewal bugs** (lookup "גבעתיים" not found, a 429 shown as "no compounds", the map schema never printed) | Linear HAD-397 Backlog; 2 of its items were fixed in 1.72.416 | HALF-DONE | The rest | urban or main | P3 |
| 33 | **Upgrade plan, steps 1-3** | `docs/research/urban-renewal-2026-10/upgrade-plan.md`; Linear HAD-392 In Review; Notion #6 waits on Ben (8 decisions) | FINISHED NOT PUBLISHED (a plan only) | Ben picks the next stage | Ben | P3 |
| 34 | **Compound data drift against data.gov.il** | 33 missing, 18 stale statuses, 10 orphans; no refresh job (memory handoff 3.10 00:50) | STALE | A refresh job | main | P3 |
| 35 | **Small leftovers** | HAD-411: the main button contrast is below AA (design call). HAD-408 follow-ups: the search link goes to `#nlhp-hero`, the home buttons drop the language, the logged-in room is untested. Copy: "עוד 1 דירות", "100% הסכמה!", the EN/RU sample title is in Hebrew (`claude-codex.md:3085/3126/3159`) | HALF-DONE | One small package | main; Ben for HAD-411 | P4 |

### A4. Content and SEO

| # | Item | What exists | Status | What is missing | Who | Pri |
|---|---|---|---|---|---|---|
| 36 | **H Infinity article: the Hebrew output was never saved** | `docs/research/2026-09-28-h-infinity/article-he-chatgpt-pro.md` (38,444 bytes, untracked) is the prompt with its header removed: `prompt-he.md` is 38,645 bytes (code, by size; the diff was checked by a sub-agent). The text exists only in the ChatGPT conversation linked in that folder's README. The en/fr/ru/ar prompts were never run. The page still has the errors listed in the README: the pin 154 m off, the stale 52 floors / 242 units, the 71 m station, the light-rail claim, and "DUO 510" against DUO's 668. Linear HAD-357, HAD-356 and HAD-332 | HALF-DONE (lost output) | Copy the article out of his ChatGPT, run the other 4 languages, fix the page facts, release | Ben (copy the text), then main | P2 |
| 37 | **STORY Galei Yam Netanya, 5 articles** | `docs/research/2026-10-05-story-package/` (`5b906677`); `manifest.json` says 0 written, and the CMS id is not verified. Linear HAD-430; Notion #3 | HALF-DONE | Writing in ChatGPT (law 8), then pages | Ben / main | P2 |
| 38 | **The 3 mega articles of August** | `docs/content/mega-articles-2026-08/01-apartment-valuation-guide.md`, `02-investment-mortgage-guide.md`, `03-tlv-projects-comparison.md`. The ChatGPT output came back (`9198ca2a`); never published | FINISHED NOT PUBLISHED (since August) | URL word audit (the head words valuation, mortgage, investment), a fact check, release | main | P2 |
| 39 | **Ultra-prime guide package** (/guides/ultra-prime-construction/, a flagship guide + 12 deep dives) | `docs/content/ultra-prime-2026-08-10/` (`05_flagship_draft.md`, `06_deep_dives`, `13_wordpress_handoff.csv`). No publish commit. 10 owner decisions listed in `12_QA_report.md` | FINISHED NOT PUBLISHED | Those 10 decisions (any that are legal or business stay Ben's), the URL audit, release | Ben for the decisions, then main | P2 |
| 40 | **New-projects package** (/new-projects/ in 4 languages + 11 guides) | `docs/content/new-projects-2026-08-07/`. No publish receipt found | unknown | A live check first | main | P3 |
| 41 | **Page 5154: FAQ schema** | The article went live 5.10 (`7bdea0a6`); "the new FAQ gets its schema only after review" (`claude-codex.md:3858`) | HALF-DONE | Review, then the schema | main | P3 |
| 42 | **Old SEO items** | HAD-264 (a page on "דמי תיווך": 215 impressions, position 46), HAD-265 (fr/ru buyer pages), HAD-218 (the abroad hierarchy), HAD-298/299/301 (copy), HAD-186 (16 competitor gaps) | STALE | Re-rank against the GSC data | main | P3 |
| 43 | **Homepage competitor deep research** | `docs/research/2026-09-25-homepage/homepage-audit.md:80`: planned, never run | STALE | Run it or drop it | main / a side session | P4 |
| 44 | **SIX-8 article briefs** | `docs/projects/six8/article-brief-{he,en}.md` (20.8). SIX-8 is frozen (HAD-183) | STALE | Ben unfreezes it or drops it | Ben | P4 |
| 45 | **Plate factory, wave 3** | `docs/content/plate-factory-2026-08-28/` (untracked); `queue-wave3-ranked.csv` (~920 rows) never run; 5 projects have no image (5583-5590); `plate-factory-2026-08-28.bundle` in the repo root | STALE | Run the 5 missing images at least | main | P3 |

### A5. Films and the project fleet

| # | Item | What exists | Status | What is missing | Who | Pri |
|---|---|---|---|---|---|---|
| 46 | **DUO, Rainbow and Dimri films live; tickets open** | Live 1.72.429 (`2ad8ee41`). Linear HAD-400, HAD-419 and HAD-420 are In Progress, while Notion has them as הושלם | LIVE, ticket open | Close them; HAD-431 carries the button overlap | main | P4 |
| 47 | **Narration for the DUO, Rainbow and Dimri films** | All three are silent. The zero-cost rule applies, and the ElevenLabs quota is spent until 21.10. Their READMEs still say "PRIVATE DRAFT" | WAITS ON BEN | Lift the zero-cost rule, or wait for 21.10 | Ben | P3 |
| 48 | **Ashira, H Infinity and Einstein films** | Planned in `claude-codex.md:1754`; no folders exist | STALE | Copy the Rainbow pipeline (`films/rainbow/build/`) | the producer session | P3 |
| 49 | **Social formats and the YouTube channel** | 1080x1920 masters exist for every film; only the 720p copies were uploaded. No 1:1 or 4:5 cuts. Linear HAD-398 Backlog | WAITS ON BEN (accounts) | Ben opens the accounts | Ben only | P3 |
| 50 | **The developers' floor plans** (Israel Canada for Rainbow, Africa Israel for DUO) | Owner board item q-plans | WAITS ON BEN | Ben asks the developers | Ben only | P2 |
| 51 | **Real furniture in the interiors** (CC0 assets) | Owner board item q-furn; Notion "1.72.335" | WAITS ON BEN | His OK to download the assets | Ben | P3 |
| 52 | **28 Rainbow `*-card.jpg` images** | `plugins/nadlan-config/assets/project-stage/rainbow/tour/*-card.jpg`, untracked and referenced by no code; 3 of them appear in the live film | STALE | Ship them as album cards, or remove them | main | P4 |
| 53 | **Codex UnitCut lab and the designer adapter** | `C:\Users\777\nad-lan\worktrees\codex-rainbow-unit-lab-2026-09-27` (branch 0 commits ahead; `labs/` untracked) | STALE | Integrate it with row 8, or drop it | main | P3 |
| 54 | **Design-to-Deal** | Linear HAD-373 Backlog. "No product edits until agreed": waiting for Maya since 30.9 | STALE | Maya's scope answer | Maya | P3 |
| 55 | **Aurelia Sports, gates 3-4** | `docs/design-lab/aurelia-sports/` (untracked); lab pages under `uploads/aurelia-sports-lab/`. Idle since 7.9; Notion #43 | STALE / ABANDONED? | Ben: continue or archive | Ben | P4 |
| 56 | **Small Rainbow items** | HAD-295 (balconies vs the permit), HAD-377 (an empty places list once), HAD-378 (window labels), HAD-287 (X1 defects) | STALE | Verify, then fix or close | main | P4 |

### A6. Legal and privacy

| # | Item | What exists | Status | What is missing | Who | Pri |
|---|---|---|---|---|---|---|
| 57 | **Lawyer review** of /privacy/ (8103) and /terms/ (8104); the listings' distance chip sends the visitor's IP to ipwho.is | Linear HAD-259 (the page has been live since 1.72.254) and HAD-347; Notion #26 | WAITS ON BEN | Counsel; keep, replace or drop the IP chip | Ben | P2 |
| 58 | **Ben-only small rulings** | HAD-263 (the daily AI token cap), HAD-266 (the city name in listing slugs), HAD-267 (delete 6 test images) | WAITS ON BEN | One answer each | Ben only | P4 |
| 59 | **Sde Dov duplicate pages merge** | Notion #65 and #68 (the same item twice; waiting on Ben since 28.8). It conflicts with the no-redirects law | WAITS ON BEN | Very likely "no", then close both | Ben | P4 |

### A7. Repository and record hygiene that affects the work

| # | Item | What exists | Status | What is missing | Who | Pri |
|---|---|---|---|---|---|---|
| 60 | **Live source not in git** | `tools/deals/` (the builders behind the live catalog-plus map), `scripts/interior/kikar_cafe.py` (source of the café scene in the live film), `.claude/skills/language-dna/` (the master copy skill), and 12 of Maya's coordination files (the 8 `codex-kikar-*`, `codex-had407-409-qa`, `codex-portfolio-decision`, `rentals-status.md`, the Cyprus file). Uncommitted edits: `BACKLOG.md` (+4), `skills/MAP.md` (+3), `codex-listing-journey-2026-10-04.md` (+134) | FINISHED, not committed | Commit by path (the index is shared) | main | P3 |
| 61 | **`docs/coordination/rentals-status.md` in the main tree is stale** | Last entry 2.10, "NOT live", although 404-410 are live | STALE | Refresh it from the rentals branch | rentals / main | P4 |
| 62 | **Lab experiments asked of Maya on 1.10** (floor plan to JSON; payment proof to a record) | `claude-codex.md:933-943`; no `codex-rentals-lab-2026-10.md` exists | STALE | Ask again or drop | Maya | P4 |
| 63 | **The owner board is 5 days stale** | Artifact `Sot2mJCpiWSiEwEwMtErxL`, "עודכן 30.9.2026, 22:20 · גרסה 1.72.372" | STALE | Republish it with this list | main | P2 |
| 64 | **The project constitution points to old truths** | `C:\Users\777\nad-lan\CLAUDE.md` says the production branch is `claude/sde-dov-experience-v1` and that live is 1.72.210 with Einstein defects open. Both are superseded: production is `claude/apartment-experience-b1`, live is 1.72.429, and Einstein was fixed in 1.72.211 (`einstein-tower-prototype/README-NEXT-SESSION.md` header) | STALE | Ben or main updates the pointer lines (a CLAUDE.md edit is the owner's file) | Ben / main | P3 |
| 65 | **einstein-tower-prototype** | 3 local commits not pushed since 20.8 (`e676cf7`, `a4ee98f`, `3fb83fc`, receipts only) | STALE | Push or ignore | main | P4 |

---

## B. The 10 fastest moves from finished work to live value

Ordered by how much money or leads they unlock per hour of work. Moves 1, 2, 5, 6 and 7 need nothing from Ben under the 5.10 publish law.

1. **Release the owner listing journey (row 1).**
   - It is the only finished feature that creates supply (owner listings) and has a live-DB proof.
   - Main picks 2.0.1 or 2.0.2 in writing and runs `scripts/had-256/deploy_had256.py`.
   - Ship it even if mail is unproven: the recovery mail is labelled as a known gap, and HAD-260 (SMTP) is the only Ben item.
   - After it is live, merge `worktree-agent-a61b211e083144352` into production.
2. **Make the broker price one price everywhere (row 2).**
   - /en/, /fr/ and /ru/brokers/ sell Pro at ₪149 tonight, while Hebrew says ₪349 (code, live GET).
   - Ben ruled ₪349 on 28.9, so this is a page update plus the four source files and the skill.
3. **Ben, 15 minutes, unlocks every sale (rows 3, 4).**
   - Paste the Morning API key and fix the `firstmonth` coupon that makes Pro ₪0.
   - Run a ₪1 test.
   - Create the ₪1,490 payment link.
   - Without these, a broker who says yes cannot pay.
4. **Send the three ready broker messages (rows 4, 5, 7).**
   - Meital and ABI: drafts in session local_047b0b73 and in Notion 3ecab55b…be.
   - Gili: the call prep in `docs/brokers/biyar-2026-10/`.
   - Only Ben can send them; the plan's week (4.10-11.10) is already running.
5. **Fix Meital's update link (row 6).**
   - Reuse the rentals token pattern and send her the new link.
   - She is the reference customer for every broker sale.
6. **Publish the developers' film (row 10).**
   - The files have been ready since 28.9; /developers/ still plays the August film.
   - One upload and a source swap on two pages.
7. **Release Batch 2: a design request per apartment, as a lead with its key (row 8).**
   - Rebase it on the live text and fix the duplicate-lead retry first.
   - It turns the designer from a demo into a lead form tied to an apartment.
8. **Wire site leads to HubSpot and prove form delivery (row 9).**
   - Health shows 0 form leads in 7 days, so first prove a test lead arrives end to end.
   - Then the HubSpot wiring. Ben gives the footer details.
9. **Rentals pilot (row 14).**
   - Close the `/rm/*` access gap first.
   - Then Ben picks option C and the prices.
   - Then the bridge op `rm_pilot` opens v2 for the first client by email.
   - This is a real client and a recurring product.
10. **Publish content that is already written (rows 36, 38, 39).**
    - Ben copies the H Infinity Hebrew article out of ChatGPT.
    - Main runs the URL word audit and fact check on the three August mega articles and the ultra-prime guide, then releases them.
    - Ben says yes to "request indexing" for Kikar EN and RU (row 19).

**Prerequisite for every move:** the one-line release lock in `claude-codex.md`. A runner is chained on the newest verified one, never on a branch file (section C1).

---

## C. Duplicates and conflicts between branches and sessions

### C1. The repository is not a copy of the live site, in both directions (code)

This is the core of "gather all the branches into one project".

| What | Live since | Where the code is | In production branch? |
|---|---|---|---|
| Rentals v2: 110 plugin files, about 12,000 lines (`inc/rentals/*`, `assets/rentals/*`, `rentals-manager.php`) | 1.72.404/406/408/410 | `claude/rentals-proptech-v2` only (54 commits ahead, merge-base `2ddf9192`) | **No.** All 110 files differ from production's HEAD |
| Urban renewal: 17 plugin files (`urban-*.php`, `smart-form.php`, `catalog-plus.php`, `matcher.php`, `reviews.php`, `i18n.php`, …) | 1.72.413/415/416 | `claude/had-407-409-urban-polish` (12 ahead; it contains all of `had-396-urban-honesty` (11) and supersedes `had-393-focus-only` (2)) | **No.** All 17 differ |
| Films and speed: 1.72.414-429 | 414-429 | Hunks applied to the live text by `scripts/project-stage/film_4xx.py`, `perf_4xx.py`, `sf_413.py`, `cc_r4.py`; backups in `docs/qa/project-stage-2026-09-24/` | **No.** `inc/project-stage.php` has the 1.72.401 `nlws-film` code but 0 matches for `film-cc` or `nadlan_ps_world_film_v2` |
| Batch 1/2 (row 8) | never | production branch (`644d0025`, `6286d747`, `65760d31`) | Yes, but **not live**. So the same `project-stage.php` is ahead of live and behind live at once |
| Listing journey 2.0.x + broker-drop 1.1.4 | not yet | builder branch `worktree-agent-a61b211e083144352` | No |

**Risk.** A whole-file deploy from any one branch would silently remove live films, rentals or urban fixes, or ship the unreleased Batch 2. Today's runners avoid this by patching the live text, but the repo cannot serve as the source of truth.

**Suggested consolidation, for main to run; nothing done here:**
1. Cut `claude/consolidation-1.72.429` from the production line.
2. Merge `claude/had-407-409-urban-polish` and then `claude/rentals-proptech-v2`. Merge the HAD-256 builder branch after its release.
3. Pull every live plugin file with `scripts/project-stage/live_read.py` and diff it against the merged tree.
4. Commit the result as "repo = live 1.72.4xx", with the per-file diff kept as evidence.
5. Move Batch 2 behind a flag, or onto its own branch, until it ships.
6. After that, retire the merged branches and worktrees.

### C2. Which branch is "production"

The records disagree about it:
- GitHub's default `main` is stale (14.8).
- `C:\Users\777\nad-lan\CLAUDE.md` names `claude/sde-dov-experience-v1`.
- Memory names `claude/production-truth-1.72.212`.
- The release commits are actually on `claude/apartment-experience-b1`. `production-truth-1.72.212` and `sde-dov-experience-v1` are fully contained in it (0 commits ahead).

### C3. The same feature built twice, or the records disagree

- **HAD-256 version:**
  - Main's pick is 2.0.1 (`claude-codex.md:3868`), while the builder committed 2.0.2 and a runner afterwards.
  - Maya's QA was a release gate at `:3702` and is gone from the gate list at `:3886`.
  - Maya's `codex-listing-journey-2026-10-04.md` still says "R1 rejected".
- **Kikar narrated film:**
  - Maya's records treat narration as excluded and options A/C as open.
  - Live 1.72.417 publishes the narration, on Ben's 3.10 word.
  - Ben said "nothing about credit on the page", but the end card keeps the OSM/GIS line (OSM requires it).
- **Rentals 3D:** Maya's lab build against the rentals session's `rm-3d.js` (row 16).
- **The designer:**
  - Live is `designer-tour-1.72.366.html` (the live designer plus a contact step).
  - The branch copy is Batch 2 plus the same step (`claude-codex.md:210`).
- **Films:**
  - There are two rentals films for one product.
  - Rainbow and DUO were each built twice: in `scripts/project-video/` (retired; `build_duo.py` never rendered) and in `docs/design-lab/films/` (live).
  - Staging copies are byte-identical duplicates: `docs/qa/film-v2r1/stage/`, `docs/qa/film-facilities/stage/`, `docs/qa/film-v1-projects/stage/`.
- **Broker price:** 149 / 349 / 1,490 across the four language pages, `scripts/broker-drop/pages/*`, the skill, HAD-257's description, HAD-394 and HAD-395.
- **OpenAI "401":** HAD-384 and HAD-397 still call it a bad key. HAD-432 (cancelled 5.10) shows it is the expected answer of a keyless reachability probe.
- **The earlier audit** `docs/loop/FORGOTTEN-2026-09-28.md` (52 rows) is partly stale:
  - HAD-262 went live in 1.72.356;
  - the floor card was fixed in 1.72.355;
  - walking inside the building is live in 358-359;
  - the DUO film is live in 429.
  - Its other rows are folded into this list.

### C4. Stale branches, worktrees and folders

| What | Evidence | Suggestion |
|---|---|---|
| `worktrees/had-393-focus-only`, `had-396-urban-honesty` | Both are contained in `had-407-409-urban-polish`, and all of it is live | Remove after the C1 merge |
| `worktrees/ecocity-*` (3 worktrees, 4 `codex/ecocity-*` branches) | The EcoCity takedown of 30.8: never republish | Archive; never merge |
| `codex/project-area-fail-closed-production-truth-2026-08-28` (1 commit, `6dd0a937`) | Built for the EcoCity parcels; it touches the frozen `engine.js` | Abandon |
| `codex/lovable-nadlan-archive-2026-08-27` (2 docs commits) and `qa/search-featured-image-aspect-2026-08-28` | Archive material from August | Keep as an archive, or delete |
| `codex/rainbow-unit-lab-2026-09-27` | 0 commits ahead; only untracked `labs/` | Integrate the lab (row 53) or remove |
| `claude/seo-wave2-live-swaps`, `claude/bold-cray-ad2cea` (not the worktree), `codex/project-area-fail-closed-2026-08-28` | 0 ahead, or equal to the old `main` | Delete the local refs |
| `C:\Users\777\nad-lan\push-pending-bundles\` (two bundles, 0.76 GB) | `9198ca2` and `2aea39c` are already in their repos | Owner may delete |
| 303 GitHub branches older than 1.8 and 28 open PRs (the newest from 2.9) | Listing in the scratchpad file `remote_refs.txt` | Ben decides a bulk close or delete; none is production |
| Cyprus worktree `C:\Users\777\Documents\Codex\2026-10-02\task-2\cyprus-nadlan` | Local `f66ec416` is behind the remote `a8dde9b6` (Cyprus 1.6.1, 5.10) | Out of scope; Ben paused the Cyprus loop on 5.10 |

### C5. Sessions (listed read-only; none was messaged)

| Session | Last activity | State |
|---|---|---|
| DUNE Cyprus (local_bdec6bcd) | 5.10 | Out of scope; loop stopped by Ben |
| Film loop, Sonnet 5.5 (local_3767d4a4) | 3.10 21:08 | Idle. Its outputs are live, except the rentals films and the Ashira, H Infinity and Einstein films (rows 15, 48) |
| HAD-396 + HAD-393, urban (local_85f99cd3) | 3.10 18:16 | Idle. HAD-412 is assigned to it and not started (row 31) |
| HAD-383 rentals A-Z (local_de38227d) and the rentals PropTech session (local_26d8f4dc) | 3.10 / 1.10 | Idle. Its branch is not merged (C1) |
| V7 Kikar articles (local_73cddb3f) | 3.10 | Done (1.72.403 live) |
| Urban research (local_f5c0c974) | 2.10 | Done (plan only, row 33) |
| biyar / Gili (local_f8643f54) | 2.10 | Done; waits on Ben (row 5) |
| First product to sell (local_047b0b73) | 1.10 | Plan written; nothing executed (row 4) |
| Sight lines (local_01b7edc5) | 30.9 | Done (1.72.372); HAD-376 waits on a Fable review |
| HAD-247 listing 3D, broker listing rule, "NADLAN ROSH SHANA" | 23-24.9 | Done and live; tickets In Review (section D) |
| HAD-256 builder (a sub-agent of the main session; worktree `agent-a61b211e083144352`) | 5.10 21:03 | Active (row 1) |

---

## D. Linear and Notion hygiene

### D1. Linear issues that are live and should be closed (record; each has a "LIVE" comment)

**Close now:**
- the films: HAD-400, HAD-419, HAD-420 (1.72.429);
- urban: HAD-407, HAD-408, HAD-409 (1.72.416). Move HAD-408's leftovers to a new small issue;
- the rest:
  - HAD-262 (1.72.356; it is in **Todo**);
  - HAD-340 (fixed 28.9);
  - HAD-344 (1.72.364);
  - HAD-347 (1.72.296-299);
  - HAD-297 (1.72.310);
  - HAD-361 (1.72.350-351, 429);
  - HAD-259 (1.72.254);
  - HAD-249 (1.72.227/230);
  - HAD-251 (1.72.227/233);
  - HAD-221 (move its Aurelia part to HAD-425).

**Close after one check:**
- HAD-403 (1.72.409/411; it is in **Backlog**): Maya's confirmation.
- HAD-390 (1.72.412): Maya's live QA.
- HAD-376 (1.72.372): a Fable review.
- HAD-247 (1.72.233): Ben's look on a phone.
- HAD-298: probably replaced in 1.72.300; check the raw page.
- HAD-379: a read-only task, done.

**Narrow:**
- HAD-332 to "the H Infinity English answer paragraph".
- HAD-356 to "the H Infinity page model".
- HAD-421 is in Backlog with 9 steps live: set it to "paused on the owner".

**Cancel:**
- HAD-113 (the May SEO plan, superseded).
- The umbrellas HAD-186, HAD-246 and HAD-258 (three gap maps of 23-24.9) once their live rows are re-ticked. Move what is left into this file's rows.

**Merge as duplicates:**
- HAD-219 into HAD-248;
- HAD-260 with HAD-256's mail gate;
- HAD-395, HAD-257 and HAD-394 on the price (one issue);
- HAD-425 with the Aurelia items in HAD-287 and HAD-221;
- HAD-433 with HAD-381 and HAD-387 (or link them);
- HAD-329 into HAD-346 (Batch 2).

**Fix the text:** in HAD-384 and HAD-397, the OpenAI 401 is not a bad key (see HAD-432).

### D2. Notion rows (record)

**Mark done:**
- #16 (WhatsApp wording; Linear HAD-382 is Done);
- #21, #22, #23, #24 (their next steps are already done rows);
- #50 (HAD-229 is Done);
- #10 (replaced by #9);
- #35 (covered by a done row and #29).

**Mark done after one nod from Ben:** #25, #26, #27, #28, #29, #45, #47, #48.

**Close as void** (the מצב field has no "cancelled" option, so ask Ben whether to add one or use הושלם):
- the 8 EcoCity rows: #61, #63, #66, #67, #70, #72, #73, #74 (takedown of 30.8);
- the Codex batch of 1.9: #53 to #60, plus #62 (the homepage was rebuilt in 273-310).

**Duplicate pairs:**
- #33 / #49 (demo content);
- #65 / #68 (the Sde Dov merge);
- #32 / #41 (the 24.9 plan; #36 and #44 overlap them);
- #9 / #10 (the rentals film);
- #11 / #47 (the price);
- #12 / #14 (ABI);
- #34 / #45 (HAD-247);
- #61 / #70 / #71 (the palette work).

**Rows with no עדיפות or אחראי:** #20 to #24.

**Linear and Notion disagree:** HAD-400, HAD-419 and HAD-420 are הושלם in Notion and In Progress in Linear. Close them in Linear (D1).

**Missing rows:** each of these has no Notion row. Each needs one, and each needs its own Linear issue too, or a Linear id:
- the developers' film (row 10);
- the H Infinity lost article (row 36);
- the August mega articles and the ultra-prime guide (rows 38, 39);
- the repo-equals-live consolidation (C1).

### D3. Files whose status lines are out of date

- `docs/coordination/rentals-status.md` (2.10).
- `docs/loop/FORGOTTEN-2026-09-28.md` (see C3).
- `BACKLOG.md` ("Last updated 2026-06-05").
- The READMEs of `films/duo`, `films/rainbow` and `films/dimri` still say "PRIVATE DRAFT", although the films are live.
- `KIKAR-HAMEDINA-LOOP.md`: P4, P5 and P6 are done but unticked (lines 1179, 1229, 1235); V6 is live but unticked.
- The owner board (row 63).
- The constitution's "Current state pointers" (row 64).

---

## What could not be verified (unknown)

- Whether leads arrive by WhatsApp: the bar opens WhatsApp directly, and health counts only form leads.
- Whether the "30 brokers" list chip of 1.10 ever ran: no session with that task was found.
- Whether the new-projects package of 7.8 (row 40) is live.
- Whether the rentals AI key was fixed: HAD-432 says the health 401 is a keyless probe, which is a separate question.
- Maya's own Codex state beyond the files in `docs/coordination/`.

**Sources:**
- git and worktrees in `C:\Users\777\nad-lan\nad-lan-co-il`, plus the GitHub API (branches and PRs);
- `docs/coordination/*.md` (`claude-codex.md` lines 2300-3894 read in full, the rest by keyword);
- `docs/loop/*.md`, `docs/design-lab/`, `docs/qa/`, `docs/research/`, `docs/content/`, `handoff/`;
- Linear team Hadmaia and the Notion data source `dfb3f22d-e709-4af5-b830-44fe8a250c28`, read only;
- the memory folder `C:\Users\777\.claude\projects\C--Users-777-nad-lan\memory\`;
- the list of desktop sessions;
- the owner board artifact;
- public GETs of `/wp-json/nadlan/v1/health`, `/developers/`, `/film/` and `/brokers/` in four languages.
