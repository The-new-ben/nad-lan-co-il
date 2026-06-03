# Codex Onboarding & Mission Brief — get inside, see everything, finish the job

> **Audience:** the Codex agent (Codex CLI or Codex Cloud) starting work on
> `the-new-ben/nad-lan-co-il`. This file is also useful for Cowork, Gemini-via-
> browser, and any future agent.
>
> **What this brief does (one shot):** explains exactly how to enter the repo,
> see *every* feature we've built, understand the user journeys, change code
> safely, and **finish the mission to the last mile**.
>
> **Why it matters:** prior Codex sessions stopped one step short of merging
> (PR #17, archive polish — never reached `main`). The "Last-Mile Contract"
> below is the explicit anti-premature-completion rule for this repo.

---

# 0. ONE-SHOT PROMPT YOU PASTE TO CODEX

(The owner pastes this verbatim. The brief below is what Codex then reads.)

> You are Codex, joining the `the-new-ben/nad-lan-co-il` repository as a coding
> agent. **Before any action**, fetch and read in order:
> 1. `https://raw.githubusercontent.com/The-new-ben/nad-lan-co-il/main/AGENTS.md`
> 2. `https://raw.githubusercontent.com/The-new-ben/nad-lan-co-il/main/docs/codex-onboarding-and-mission-brief.md` (this file)
> 3. `https://raw.githubusercontent.com/The-new-ben/nad-lan-co-il/main/skills/MAP.md`
> 4. `https://raw.githubusercontent.com/The-new-ben/nad-lan-co-il/main/BACKLOG.md`
> 5. `https://raw.githubusercontent.com/The-new-ben/nad-lan-co-il/main/skills/codex-plugin-access-and-deploy.md`
>
> Operating posture:
> - **Branch off `origin/main` every time.** Never touch a stale branch.
> - **Honour the Last-Mile Contract in section 9 of the brief.** "Done" is
>   defined there with a numbered checklist; don't claim done unless every box
>   is verifiably ticked (with terminal output you can paste).
> - **Coordinate version numbers** with Claude (`git show
>   origin/main:plugin-dist/nadlan-config.json` tells you the current). Bump to
>   the next available patch.
> - **Stay in your lane**: research / content / docs / audits / brand-new modules
>   that don't overlap with Claude's open modules (see §6).
> - **If you cannot complete a step, do NOT silently stop.** Open a draft PR
>   describing the blocker, the exact terminal output, and what you'd need to
>   proceed. Then ping me.
>
> Today's mission: <the owner fills this line; example: "Audit the Studio
> feature end-to-end and complete the onboarding wizard for first-time
> advertisers per BACKLOG"> .

---

# 1. WHERE YOU ARE (the lay of the land)

| Thing | Location |
|---|---|
| Repo | `https://github.com/The-new-ben/nad-lan-co-il` (public) |
| Default branch | `main` |
| Live site | `https://nad-lan.co.il` |
| WordPress 7.0 / PHP 8.5 / Yoast active / Site Kit active | |
| Theme | custom (kept in repo under `themes/` — read-only unless explicitly asked) |
| **Plugin source** | `plugins/nadlan-config/` |
| Plugin **deploy** | bumped ZIP + manifest on `main` → owner clicks Update in WP-admin (see §3) |
| Healthcheck (live version probe) | `https://nad-lan.co.il/wp-json/nadlan/v1/healthcheck` |
| Public sitemap | `https://nad-lan.co.il/sitemap_index.xml` |

The repo is **PUBLIC**. No secrets, partner names, prices, or client data may be
committed. See `skills/security-public-repo.md`.

---

# 2. HOW TO GET INSIDE — every access channel

There are five channels. Pick the right one per task.

| Channel | Used for | Auth |
|---|---|---|
| **Git** (clone/pull/push) | Code, docs, skills, plugin source, manifests | GitHub login |
| **GitHub REST/MCP** (PRs, issues, comments) | Open + merge PRs, list branches, file comments | GitHub login |
| **WP REST API** for content | Read public + write authenticated content (Yoast meta, posts, terms, settings, OUR custom REST routes) | `WP_USER` + `WP_APP_PASSWORD` env vars |
| **Browser (Codex Cloud)** for QA / user journeys | Real-browser persona testing per `skills/qa-journey-testing.md` | Logged in |
| **WP-admin / FTP / SSH** | **NONE — no agent has these.** Owner is the only one who clicks "Update" in Plugins. | n/a |

**Authentication for the WP REST API** (when reading/writing live content from
your shell):
```bash
# env vars — set by the owner once; never commit values to the repo
echo "auth as: $WP_USER"   # owner WP login
# WP_APP_PASSWORD is a WordPress *application password*, NOT the login password.
curl -s -u "$WP_USER:$WP_APP_PASSWORD" "https://nad-lan.co.il/wp-json/wp/v2/users/me"
```

If you don't have the env vars set in your environment, **ask the owner — do
not guess and do not commit a password.**

---

# 3. PLUGIN SHIP LOOP (the only way code reaches the live site)

**Mandatory reading:** `skills/codex-plugin-access-and-deploy.md`. Summary:

```bash
# 1. Always branch off latest main
git fetch origin main
git checkout -b codex/<topic>-<ver> origin/main

# 2. edit plugins/nadlan-config/inc/<module>.php
#    new module? add to the foreach() loader in plugins/nadlan-config/nadlan-config.php

# 3. bump version in TWO places in plugins/nadlan-config/nadlan-config.php:
#    line ~5  ' * Version: X.Y.Z'
#    line ~73 "'version' => 'X.Y.Z'"

# 4. lint — ZERO failures allowed
fail=0; for f in $(find plugins/nadlan-config -name "*.php"); do
  php -l "$f" >/dev/null 2>&1 || { echo "FAIL $f"; fail=1; }
done
[ $fail -eq 0 ] && echo "ALL CLEAN"

# 5. build dist ZIP (folder MUST be top-level "nadlan-config/")
NEW=X.Y.Z
cd plugins && rm -f /tmp/nadlan-config-$NEW.zip && \
  zip -rq /tmp/nadlan-config-$NEW.zip nadlan-config -x "*.DS_Store" && cd ..
cp /tmp/nadlan-config-$NEW.zip plugin-dist/nadlan-config-$NEW.zip
unzip -l plugin-dist/nadlan-config-$NEW.zip | head -3  # MUST start with "nadlan-config/"

# 6. update manifest plugin-dist/nadlan-config.json
#    bump "version", set "download_url" to the new zip, prepend a changelog block.

# 7. HARD GATE — verify the change you made is actually inside the built zip
#    (this is the gate that caught the v1.40.0 → v1.41.1 blank-page mistake)
unzip -p plugin-dist/nadlan-config-$NEW.zip nadlan-config/inc/<your-module>.php | grep -c '<unique-string-from-your-change>'

# 8. commit, push, PR, squash-merge to main
git add -A
git commit -m "vX.Y.Z <summary>"
git push -u origin codex/<topic>-$NEW
# open PR via gh or the GitHub MCP tool. Squash-merge.

# 9. RUNTIME SMOKE TEST after merge (caught by our process retroactively)
sleep 5
curl -s -m20 -o /dev/null -w "homepage %{http_code} %{size_download} bytes\n" \
  "https://raw.githubusercontent.com/The-new-ben/nad-lan-co-il/main/plugin-dist/nadlan-config.json"
# then verify the ZIP + manifest on raw.githubusercontent are correct.

# 10. tell the owner exactly what to click:
#    "WP-admin → Plugins → NadLan Config → Update to vX.Y.Z"

# 11. AFTER the owner updates, curl the live pages your change affected and
#     confirm bytes > 0 and the new signature appears. This is the last mile.
```

⚠️ **Common landmines (every one of these has bitten us — DO NOT repeat):**
- Branch divergence after a prior squash-merge → always `git checkout -b <new> origin/main`.
- ZIP without top-level `nadlan-config/` folder → must zip *from* `plugins/`, not from inside.
- Manifest `version` not bumped or `download_url` mismatched → owner sees no update.
- Forgot to add new module to the `foreach()` loader → file exists but never loads.
- **`ob_start()` inside an `ob_start()` handler** → silent fatal → blank page (this exact bug blanked `/projects/` from v1.40.0 to v1.41.1).
- Used `git checkout <otherbranch> -- file` after starting a fresh branch → clobbers working-tree edits → shipped no-op versions twice. Use `cp` from a known-good path instead.

---

# 4. EVERY FEATURE WE'VE BUILT (the inventory, ground truth)

The plugin is **49 modules** under `plugins/nadlan-config/inc/`. Each is one
capability, all guarded with `function_exists()` and `ABSPATH`. Loaded via the
single `foreach()` in `plugins/nadlan-config/nadlan-config.php` line 25.

## 4.1 Directory engine (the heart)
| Module | What it does | Public surface |
|---|---|---|
| `directory.php` | Premium AJAX directory for `nadlan_professional` AND `nadlan_project`: hero, profession/project-type pills with colours, sidebar facets, server-render first page + REST AJAX load-more. **OWNS the rendering of `/professionals/` and `/projects/`.** | `/professionals/`, `/projects/` |
| `directory-assets.php` | CSS + JS for directory + the share `nadlan_dir_css()` / `nadlan_dir_js()` | (loaded by directory.php) |
| `archive-grid.php` | Branded archive grid for `nadlan_property` (and a generic fallback) | `/properties/` |
| `cards-render.php` | Single-card body: facts table, photo gallery (reads `photos_csv`), claim CTA, provenance | every single `nadlan_*` page |
| `facets.php` | Server-side query-arg → meta_query translation (city/profession/etc.) | `?city=…&profession=…` query strings |
| `city-hubs.php` | Programmatic `/city/<city>/contractors/` etc. with noindex floor | dozens of city URLs |
| `breadcrumbs.php` | Visible breadcrumbs + BreadcrumbList JSON-LD | everywhere |
| `autocomplete.php` | `/nadlan/v1/suggest` REST for city/pro/proj names | the search inputs |

## 4.2 Claim → trial → tier funnel
| Module | What it does |
|---|---|
| `claim.php` | Free-card claim funnel: REST endpoints, admin approval, ownership stamp via `owner_user_id` |
| `claim-prompt.php` | Blue "this is my card?" CTA on every unclaimed profile |
| `tiers.php` | `paid_tier` meta (free/pro/premier), 30-day trial timer, surface gating, upgrade CTAs to WooCommerce products 476/477 |
| `featured-upsell.php` | "Your card is at position #X — upgrade to top 5" on claimed-but-free profiles |
| `preferred-partners.php` | Owner-managed allowlist of partners that lead auto-routing targets |
| `owner-config-rest.php` | REST endpoints to read/write owner config (WhatsApp, preferred partners) — closes preferred-partners auto-route into the `nadlan_lead` flow |
| `lead-ledger.php` | `nadlan_referral` CPT with tokenised tracking, partner accept, customer-confirmed close, commission ledger. Solves "deal closed and nobody paid me." |
| `lead-drip.php` | 6-step lead nurture email sequence |
| `lead-inbox.php` | Unified admin Inbox: leads / referrals / reviews / claims / paid orders + daily 08:00 digest email |
| `conversion-cta.php` | Floating WhatsApp button + GA helper + public `/nadlan/v1/lead` REST endpoint (sticky bar + exit popup REMOVED v1.40.3) |

## 4.3 Reviews + advertising surfaces
| Module | What it does |
|---|---|
| `reviews.php` | 5-star public reviews for professional + project, moderation queue, AggregateRating + Review JSON-LD |
| `sponsored-spot.php` | "Your spot here" sponsored card injected after the 6th directory card (server) + once per AJAX batch. **REWRITTEN v1.41.1** — ob-free, uses the `nadlan_dir_cards_html` filter |
| `pricing-schema.php` | Product + Offer JSON-LD on `/join-pro/` for rich-result eligibility |
| `social-proof.php` | Stats counters + "recently claimed" + "popular this week" on the homepage + per-page view counter on profiles (v1.40.2 hotfix to skip heavy queries when empty data) |

## 4.4 The Advertiser STUDIO (v1.41 — the cutting-edge piece)
| Module | What it does |
|---|---|
| `studio.php` | Self-serve frontend editor at `/studio/?id=<post_id>` — drag-drop upload, AI copy assist, Leaflet+OSM map picker, social links, video embed, type-specific fields. Tooltips on every input |
| `studio-rest.php` | Six owner-authenticated REST endpoints (save / upload / gallery reorder / gallery delete / AI copy / mine) |
| `profile-extras.php` | Renders social pills + video embed on public profile pages |

## 4.5 AI + intelligence
| Module | What it does |
|---|---|
| `ai-concierge.php` | Floating chat widget powered by Claude Haiku via Anthropic API, RAG over our glossary + directory + pages |
| `ai-features.php` | AI description generator + compliance scanner (for owner copy generation) |

## 4.6 SEO + structured data
| Module | What it does |
|---|---|
| `schema.php` | Per-entity JSON-LD + `noindex,follow` guard for `data_quality=stub` records (anti-cannibalization — the 2,700 imported pros are NOT in Google's index by design) |
| `term-faq-schema.php` | FAQPage + BreadcrumbList JSON-LD on glossary terms |
| `og-image.php` | Dynamic SVG social-share preview at `/wp-json/nadlan/v1/og/<id>.svg` |
| `sitemap-ping.php` | Pings Google/Bing on enriched content changes (throttled 1/h) |
| `ga4-events.php` | dataLayer pushes for directory_card_click / profile_view / upgrade_click / quote_request / purchase |
| `glossary.php` | `nadlan_term` CPT + DefinedTerm schema |
| `glossary-autolink.php` | In-text auto-linker for glossary terms across the site |

## 4.7 Content + listings ancillary
| Module | What it does |
|---|---|
| `catalog-meta.php` | Registers project + professional + property meta + claim meta |
| `catalog-shine.php` | WooCommerce catalog premium skin |
| `homepage.php` | Below-the-fold sections shortcode (disabled auto-injection per owner) |
| `import.php` | gov.il CKAN importer for רשם הקבלנים + התחדשות עירונית (1,700+ pros, 941 projects) |
| `properties-catalog.md` (skill) | Property data model |
| `media.php` | Rich media: 3D tour / video / floorplan (mostly latent — sponsored-spot was the active media surface) |
| `nearby-poi.php` | OpenStreetMap Overpass-API POI panel on profiles |
| `compare.php` | Multi-listing compare table |
| `map.php` | Leaflet archive map with clustering |
| `interactive-widgets.md` (skill) | Calculator widget pattern |
| `calculators.php` | Lead-magnet calculators (purchase tax, mortgage, etc.) |
| `saved-search.php` | Saved searches + email alerts |
| `avm-deals.php` | Deal history + AVM + neighborhood data |
| `listings-ux.php` | Listings engagement UX |
| `auction.php` | Timed auctions engine (latent — built, not yet productized) |
| `esign.php` | E-sign on auction win (latent) |
| `ops-dashboard.php` | Admin ops dashboard |

---

# 5. THE REST API SURFACE (every endpoint we've added)

Read-only unless noted. Auth pattern: `Authorization: Basic <user:app_password>`.

| Method · Route | Auth | What |
|---|---|---|
| `GET /nadlan/v1/healthcheck` | none | Live plugin version + module presence |
| `GET /nadlan/v1/suggest?q=…&type=city\|professional\|project` | none | Autocomplete |
| `GET /nadlan/v1/directory?city=…&profession=…&q=…&paged=…` | none | Premium professionals directory AJAX |
| `GET /nadlan/v1/projects?city=…&project_type=…&paged=…` | none | Premium projects directory AJAX |
| `POST /nadlan/v1/lead` | none (rate-limited) | Generic lead capture → `nadlan_lead` + admin email |
| `POST /nadlan/v1/concierge` | none | AI chat — returns model response + retrieved sources |
| `POST /nadlan/v1/concierge-lead` | none | Lead handoff from the concierge |
| `POST /nadlan/v1/referral/route` | none | Create a tracked referral; `notify_partner:0` keeps it owner-only |
| `GET/POST /nadlan/v1/referral/<token>/accept` | by-token | Partner accepts the commission terms |
| `POST /nadlan/v1/referral/<token>/status` | by-token | Customer confirms outcome (won/lost/in_progress) |
| `POST /nadlan/v1/review-submit` | none (rate-limited) | Submit a review (lands `pending`) |
| `GET /nadlan/v1/og/<id>.svg` | none | Social-card SVG generator |
| `GET /nadlan/v1/studio/<id>` | owner of card | Snapshot for the Studio editor |
| `POST /nadlan/v1/studio/<id>/save` | owner | Save Studio fields + meta |
| `POST /nadlan/v1/studio/<id>/upload` | owner (multipart) | Add an image |
| `POST /nadlan/v1/studio/<id>/gallery/reorder` | owner | Reorder photos |
| `POST /nadlan/v1/studio/<id>/gallery/delete` | owner | Remove a photo from gallery |
| `POST /nadlan/v1/studio/<id>/ai-copy` | owner | Claude rewrite of description (5 modes) |
| `GET /nadlan/v1/studio/mine` | logged-in user | Their owned cards |
| `GET/POST /nadlan/v1/owner/whatsapp` | manage_options | Read/set owner WhatsApp |
| `GET/POST /nadlan/v1/owner/partners` | manage_options | Read/replace preferred-partners list |

Standard WordPress REST (`/wp-json/wp/v2/*`) is also available for posts, terms,
media, etc. The 2,700 contractor profiles are at
`/wp-json/wp/v2/nadlan_professional`.

---

# 6. WHO OWNS WHICH MODULE (coordination — don't step on toes)

These modules are actively maintained by Claude (the code agent). **If you need
to change one, open a PR and tag for review; do NOT self-merge into `main`:**

- `directory.php`, `directory-assets.php`, `archive-grid.php`, `studio*.php`,
  `lead-ledger.php`, `owner-config-rest.php`, `reviews.php`, `claim*.php`,
  `tiers.php`, `featured-upsell.php`, `sponsored-spot.php`, `conversion-cta.php`,
  `ai-concierge.php`, `social-proof.php`, `schema.php`.

**Codex's lane** (high-leverage, no overlap):
- Content audits, SERP research, drafting articles/guides/glossary terms.
- New `inc/<module>.php` files that don't overlap with the above.
- `skills/` and `docs/` writing.
- QA test execution per `skills/qa-journey-testing.md` and reporting to `docs/qa/`.
- Catching specific bugs Claude missed (we welcome it — file a PR).

**Hard rules** (multi-agent etiquette):
- Always branch off `origin/main` (no exceptions).
- Read `git show origin/main:plugin-dist/nadlan-config.json` BEFORE choosing a
  version number. Use the next available patch.
- Never edit another agent's open module in a parallel branch.
- Never self-merge a plugin-code PR without a Claude review unless the owner
  has explicitly told you "go solo on this."

---

# 7. USER JOURNEYS (what we're really trying to make work)

These are the 5 personas + journeys from `skills/qa-journey-testing.md`. If you
run QA, follow that file's PART A → D exactly.

1. **דנה — tire-kicker buyer** (mobile): land on a money page, find a tool/CTA,
   become a lead.
2. **יעל — Rainbow Project advertiser** (THE big one): wants premium placement,
   photos, exposure data, pays the ₪3,990 campaign (product 489), upgrades to
   Premier, demands a results report.
3. **משה — contractor** finds his auto-imported card → claim → 30-day Pro trial
   → upgrade.
4. **אבי — lead-seeker** uses calculator → wants a human → routed preferred-
   partner lead (via `lead-ledger.php` + `preferred-partners.php`).
5. **adversary** — empty forms, XSS, double-tap, mid-checkout back-button.

Each journey has a predefined "DONE =" cutoff in the QA skill. Don't hand-wave.

---

# 8. CODING EXAMPLES (paste-ready)

### A. Read a professional via REST (curl + python)
```bash
curl -s "https://nad-lan.co.il/wp-json/wp/v2/nadlan_professional/123?_fields=id,title,slug,meta" \
  | python3 -m json.tool
```

### B. Write a new post meta from a script (authenticated)
```bash
curl -s -u "$WP_USER:$WP_APP_PASSWORD" \
  -X POST "https://nad-lan.co.il/wp-json/wp/v2/nadlan_professional/123" \
  -H "Content-Type: application/json" \
  -d '{"meta":{"video_url":"https://youtube.com/watch?v=abc"}}'
```

### C. Add a new plugin module — minimal template
File: `plugins/nadlan-config/inc/<your-module>.php`
```php
<?php
/**
 * nadlan-config — <one-line purpose> (vX.Y.Z)
 *
 * <a paragraph explaining what + why>
 */
if ( ! defined( 'ABSPATH' ) ) { exit; }

if ( ! function_exists( 'nadlan_xyz_do' ) ) {
    function nadlan_xyz_do() {
        // ...
    }
}
add_action( 'init', 'nadlan_xyz_do' );
```
Then add `'<your-module>'` to the `foreach()` array in
`plugins/nadlan-config/nadlan-config.php` line 25, bump the version in TWO
places, lint, ZIP, hard-gate, PR.

### D. Add a REST endpoint
```php
add_action( 'rest_api_init', function () {
    register_rest_route( 'nadlan/v1', '/xyz', array(
        'methods'             => 'GET',
        'permission_callback' => '__return_true', // or current_user_can('manage_options')
        'callback'            => function ( $req ) {
            return array( 'ok' => true, 'foo' => 42 );
        },
    ) );
} );
```

### E. Add a tooltip to a Studio field (4-year-old-friendly UX standard)
In `inc/studio.php`, every label gets a `<span class="nlst-help" title="…">?</span>` — the title is the tooltip.

### F. Make a page noindex when thin (anti-cannibalization rule)
Set the post meta `data_quality` to `'stub'`. `schema.php` will add
`<meta name="robots" content="noindex,follow">` automatically.

### G. Verify a plugin change actually shipped (the hard gate)
```bash
git fetch origin main
git show origin/main:plugin-dist/nadlan-config.json \
  | python3 -c "import sys,json;print(json.load(sys.stdin)['version'])"
git show origin/main:plugin-dist/nadlan-config-<ver>.zip > /tmp/m.zip
unzip -p /tmp/m.zip nadlan-config/inc/<your-module>.php | grep -c '<unique-string>'
# also runtime-verify a live page:
curl -s -m20 -o /dev/null -w "%{http_code} %{size_download}\n" "https://nad-lan.co.il/<affected-url>/"
```

---

# 9. THE LAST-MILE CONTRACT (the anti-premature-completion rule)

> *Research basis: Codex's official prompting guide + community reports that
> agents abandon mid-task when they hit ambiguity. The cure (per OpenAI Codex
> docs and AGENTS.md best practice) is explicit "done means" criteria with
> verifiable checkboxes, AND a written escalation path when blocked.*

**"Done" on any plugin-code task means ALL of these are verifiable with terminal
output you can paste back:**

```
[ ] 1. Code edited, lint passes:
       for f in $(find plugins/nadlan-config -name "*.php"); do php -l "$f" >/dev/null || echo FAIL $f; done

[ ] 2. Version bumped in BOTH places in nadlan-config.php (Version header + healthcheck array).

[ ] 3. ZIP built with top-level nadlan-config/ folder:
       unzip -l plugin-dist/nadlan-config-<ver>.zip | head -3

[ ] 4. ZIP-content gate: the change is INSIDE the zip:
       unzip -p plugin-dist/nadlan-config-<ver>.zip nadlan-config/inc/<file>.php | grep -c '<sig>'

[ ] 5. Manifest plugin-dist/nadlan-config.json bumped (version + download_url + changelog).

[ ] 6. Branch pushed, PR opened, PR squash-merged into main.

[ ] 7. After merge: re-verify ZIP signature on origin/main:
       git fetch origin main && git show origin/main:plugin-dist/nadlan-config-<ver>.zip > /tmp/m.zip
       unzip -p /tmp/m.zip nadlan-config/inc/<file>.php | grep -c '<sig>'

[ ] 8. Tell the owner the EXACT click path: "WP-admin → Plugins → NadLan Config → Update to vX.Y.Z"

[ ] 9. After owner updates, run a runtime smoke test (curl one or more affected URLs and
       paste the response codes + byte counts in the chat). This is the LAST MILE.
```

**If you cannot tick one of the boxes, you have NOT finished. Two acceptable
actions:**

1. Loop back and complete the missing step now.
2. **Open a draft PR explaining the blocker** with the exact failing terminal
   output. Title it `[DRAFT] vX.Y.Z — BLOCKED: <reason>`. **Ping the owner with
   the specific question you need answered.** Do NOT silently stop.

**Behaviours we have observed and explicitly forbid here:**
- Claiming "done" without the ZIP-content gate (caused 2 no-op shipped versions).
- Claiming a feature works without curl-verifying the live HTML signature
  (caused the v1.40.0–v1.41.0 blank-page bug to ship and persist).
- Quietly abandoning a PR after the build step (PR #17 sat unmerged; archive
  polish was never live).
- Using `git checkout <otherbranch> -- file` after starting a new branch (this
  clobbers your edits, has shipped no-ops twice; use `cp` instead).
- Editing a Claude-owned module in a parallel branch without coordination.

---

# 10. THE NETWORK DNA (this knowledge is reusable on other sites)

The owner runs additional sites (legal portal, travel/relocation, regional
desks). Most skills are tagged 🟪 DNA in `skills/MAP.md` — these are reusable
verbatim. The bootstrap order is in `skills/SKILLS-TREE.md`. When opening a new
site:

1. Copy Branch 1 (Operating system) verbatim.
2. Fork `plugins/nadlan-config/` → `plugins/<new-site>-config/`.
3. Define the new site's entity CPT + category taxonomy + colours.
4. Re-derive the keyword tree using the SEO method (Branch 2).
5. Re-skin per the design system (Branch 5).
6. Wire the same monetization spine (Branch 4): claim → trial → upgrade →
   commissioned lead routing.

---

# 11. WHAT NOT TO DO (boundaries)

From `AGENTS.md`:
1. Never commit secrets (passwords, API keys, partner names, prices, client
   data). Public repo.
2. Never expose internal language (CRM, UTM, paid lead, supplier routing,
   "money page", "revenue") in public copy.
3. Never publish/rename a page without `skills/url-namespace-contract.md`'s
   slug check.
4. Never edit another agent's open module in a parallel branch.
5. Never claim a UI/behavior change is "live" without curl-verifying the live
   HTML signature.
6. **Never `git checkout <otherbranch> -- file`** on a branch where you have
   working-tree edits to that file. Use `cp` from a known-good copy instead.
7. Stop and ask if a task requires acting outside the repo (sending email,
   posting reviews, contacting partners, purchasing plugins, changing DNS).

---

# 12. SOURCES (research backing this brief)

- **AGENTS.md open spec** (Linux Foundation steward, 60k+ repos, OpenAI Codex
  origin, August 2025): [agents.md](https://agents.md/), [augmentcode.com 2026
  guide](https://www.augmentcode.com/guides/how-to-build-agents-md), [arxiv
  impact study](https://arxiv.org/pdf/2601.20404).
- **Codex AGENTS.md & cascading rules** (the file system Codex walks before
  every action): [OpenAI Codex AGENTS.md guide](https://developers.openai.com/codex/guides/agents-md),
  [openai/codex repo](https://github.com/openai/codex),
  [llmx.tech 2026 setup guide](https://llmx.tech/blog/openai-codex-setup-agents-md-mcps-skills-definitive-guide/),
  [The Prompt Shelf — AGENTS.md complete guide](https://thepromptshelf.dev/blog/agents-md-codex-setup-guide-2026/),
  [Verdent — Codex AGENTS.md explained](https://www.verdent.ai/guides/codex-agents-md-explained).
- **Codex sandbox + approval defaults** (workspace-write + on-request
  approval): [Agent approvals & security](https://developers.openai.com/codex/agent-approvals-security),
  [CLI command-line options](https://developers.openai.com/codex/cli/reference),
  [Codex CLI features](https://developers.openai.com/codex/cli/features).
- **Codex prompting guide** (how to write instructions Codex follows):
  [Codex prompting guide](https://developers.openai.com/cookbook/examples/gpt-5/codex_prompting_guide),
  [Codex Skills](https://developers.openai.com/codex/skills),
  [Unrolling the Codex agent loop](https://openai.com/index/unrolling-the-codex-agent-loop/).
- **Premature completion / agent abandonment community discussion**:
  [Codex troubleshooting](https://developers.openai.com/codex/app/troubleshooting),
  [GitHub issue: agent working too long](https://github.com/openai/codex/issues/14973),
  [OpenAI dev community: doesn't stop a task](https://community.openai.com/t/codex-doesnt-stop-a-task/1375913).

---

## Revision log
- 2026-06-03 — Created (Claude). Built from web research of the Codex official
  prompting/AGENTS.md docs + community forums on premature-completion. Inventories
  every plugin module, REST endpoint, persona/journey, and adds the explicit
  Last-Mile Contract (anti-premature-completion checklist) that PR #17 violated.
