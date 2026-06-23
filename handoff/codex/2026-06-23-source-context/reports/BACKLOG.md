# BACKLOG — the living follow-up list

> **Why this exists.** The owner asked for one place that captures everything we agree to
> do, so nothing is forgotten between sessions. **Any agent: read this at session start,
> update it at session end.** Newest decisions win. Don't delete done items — move them to
> the bottom log so we keep the history.
>
> Status keys: 🔴 not started · 🟡 in progress · 🟢 shipped · 🧊 future/parked · ❓ needs owner decision
>
> Last updated: 2026-06-05

---

## Finish-line draft PR train - 2026-06-05

- In draft review: GAP 5 geo search, GAP 6 roles, GAP 3 recurring, placement auction, AI support, business metrics, reliability, and seams/final hardening.
- Current final-hardening branch adds the future seams `nadlan_after_lead_closed`, `nadlan_search_executed`, `nadlan_real_estate_listing_jsonld`, `nadlan_card_jsonld`, and `nadlan_card_jsonld_ready`.
- Deferred after these PRs: review invitation workflow, saved-search alert productization, native MySQL POINT/SRID 4326 migration, and board-grade expansion/contraction/reactivation accounting.
- Owner prerequisites before recurring revenue deploy: set `nadlan_gi_ipn_secret`, configure Morning recurring webhook and links, decide cycle days, set server cron, set uptime monitor, and set heartbeat URLs.
- Business metrics caveat: churn and NRR are directional owner-dashboard numbers until event-level expansion, contraction, reactivation, and signup cohorts are tracked separately.

---

## P0 — Revenue (do first; the site earns ₪0 today)

- 🟡 **GAP 2 lead routing to paying card owners (Codex branch `codex/gap2-lead-routing`).**
  Draft PR in progress for `nadlan-config` v1.42.9: route exact `lead_card_id`
  inquiries to the paid card owner, add owner inbox in Advertiser Center, and
  expose delivery trace in NadLan Ops. Claude reviews and ships after PR.
- 🟡 **Advertiser Center / post-payment handoff (v1.41.2 Codex branch).** New
  `/advertiser-center/` module gives logged-in advertisers one place for owned
  cards/projects, completion score, views, inquiries, reviews, recent orders,
  Studio edit links, and upgrade paths. WooCommerce order-received page now
  points paid products 476/477/489/490 to the center. `inc/advertiser-orders.php`
  preserves `card_id`, activates the existing `paid_tier` on
  `woocommerce_payment_complete`, writes `campaign_end` / `paid_order_id` /
  `paid_product_id`, and runs a daily downgrade cron so expired one-time paid
  tiers return to free. Needs PR merge, owner plugin update, and live Journey-2
  QA before marking shipped.
- 🟡 **Wire tier-upgrade buttons → existing WooCommerce checkout.** Payments are LIVE
  (WooCommerce + Green Invoice/Morning gateway, products 476 ₪349 Pro / 477 ₪749 Premier,
  `/join-pro/` page exists, smoke test passed). The "upgrade" button just doesn't go to the
  cart yet. *No new infra needed — just wire it up.* (in progress this session)
- 🔴 **Recurring billing decision.** Green Invoice gateway is one-charge-only. Options:
  (a) reframe Pro/Premier as **annual** one-time products (₪3,490/yr, ₪7,490/yr) —
  recommended for zero friction; (b) keep monthly + owner manually sets up Morning הוראת
  קבע per subscriber. ❓ owner decision.
- 🔴 **Mortgage-advisor referral funnel.** "מצאו יועץ משכנתאות" CTA on the mortgage
  calculator → routes the lead to ONE partnered advisor. Fat money = per-closed-deal
  commission (₪3k–8k), not subscription. Needs the lead ledger below.
- 🟡 **Lead Ledger + lock-in** (owner's #1 pain — building this session). Every routed
  lead gets a tracked record; partner accepts under terms; **customer** (not partner)
  confirms status via auto follow-ups at 14/30/60 days; commission ledger logs what's owed
  and paid. See inc/lead-ledger.php.

## P1 — Product polish that drives revenue/SEO

- 🟡 **Apply the professional directory standard to projects** — projects directory shipped
  (1.33); still TODO: premium single-project profile header (parity w/ professionals) +
  richer SEO info on project cards/pages (יזם, שלב, יח״ד, כתובת, schema).
- 🔴 **SEO-value float-up (shark idea, owner liked it).** Rank-boost contractors that Google
  already knows + associates with our keywords, so featured results create buzz → then
  upsell premium to *stay* floated. Needs an authority signal (brand search / backlinks /
  manual editorial pick). *Shark note: start with a manual `editor_pick` flag; automate later.*
- 🔴 **Kill all pagination → "load more" everywhere** (owner hates pages, bad for SEO).
  Professionals + projects already use load-more. Audit remaining `paginate_links` (archive
  -grid for properties) and any blog/term archives; replace with load-more.
- 🔴 **Reviews → world-class.** Engine shipped (1.33). Level-up: verified-reviewer badge,
  photo reviews, helpful-votes, reply-from-owner, review-request emails, rich snippet QA.
- 🔴 **Verified-claim review boost.** Show "verified reviews" badges; claimed+verified cards
  float above unclaimed. Reinforces claim → pay funnel.

## P2 — Content / SEO

- 🟢 **Glossary slugs migrated Hebrew → clean Latin** (2026-06-02). All 22 terms; old URLs
  301 → new via WP `_wp_old_slug`; Hebrew titles intact. Record:
  `docs/glossary-slug-migration-2026-06-02.md`. Owner decided to KEEP the glossary.
- 🔴 **Re-index the new glossary URLs** — ping sitemap / submit in Search Console so Google
  recrawls the 22 new Latin URLs and follows the 301s.
- 🔴 **`/glossary/` archive redesign** as an entity map (link each term to 2-4 decision
  guides; clean title; stop repeating the same 3 headings). Codex audit confirmed this.
- 🔴 **Canonical gap:** some `nadlan_project`/`nadlan_professional` pages lack a self
  canonical (Codex audit + verified live on a profile). Fix via Yoast config or a
  single-source canonical — do NOT add a 2nd canonical on top of Yoast.
- 🟢 **URL namespace contract** written (`skills/url-namespace-contract.md`) — the
  100-steps-ahead law: Latin concept slugs, one-concept-one-URL, namespace map, pre-publish
  collision check, cannibalization rules. All agents follow it before publishing.
- 🔴 **Glossary rewrite to "magic"** (titles/prose). Wikipedia-DNA flowing prose + two-way
  linking. Lower priority now that slugs + namespace are fixed. ❓ after archive redesign.
- 🔴 **Codex coordination:** PR #17 (Codex 1.35.0 archive polish) CLOSED + locked
  "DO NOT MERGE" (fragile regex HTML surgery, dup schema, pagination links, edited
  directory.php). Good parts (title/desc map) to be cherry-picked into a clean module if/when
  needed. Division: Codex = content/research/audit; Claude = structural plugin code + review
  gate. No agent edits another's module; no self-merge of plugin code.
- 🔴 **Missing glossary terms** the owner expects: bill-of-materials / machinery / materials
  terms (כתב כמויות, ציוד, חומרי גלם...) — not present yet.
- 🟢 (guard confirmed) Stub records are `noindex,follow` via `schema.php` — 1,700+ imported
  contractors are NOT polluting Google. Good.

## P3 — Off-site growth (FREE only — owner has no ad budget now)

- 🔴 **Google Business Profile** setup for the business (via Cowork).
- 🔴 **Free backlink program** (via Cowork): directories, HARO-style, gov/edu, partner swaps.
- 🔴 **Organic social for SEO signals** (TikTok/IG/FB) via Cowork — free, no paid spend.
- 🔴 **Off-site playbooks** missing from skills Branch 6 — write them as reusable DNA.

## P4 — AI / automation (the "zero-friction, I don't manage people" goal)

- 🟡 **GAP 4 OpenAI provider adapter.** Branch `codex/gap4-openai-agent` makes the
  concierge, Studio copy assist, listing-description generator, and NL search provider
  agnostic with OpenAI default, Anthropic fallback, daily token cap, and usage trace.
  Draft PR/review pending; not live until merged + owner plugin update.
- 🧊 **100% AI support layer** so the owner doesn't deal with people directly. Long-term.

## P5 — Assets

- 🧊 **Project/listing images.** Generate realistic images (ChatGPT/Cowork) and attach to
  projects. Don't bloat the DB (use a CDN/external URLs or limited sizes). Parked until
  Cowork access is sorted.
- ❓ **Cowork access.** Owner can't activate the Cowork display/app reliably; checking CLI
  access. Many tasks above are delegated to Cowork — blocked until this works.

## Network (future — connect the owner's other sites)

- 🧊 Multi-site group: legal portal + travel/relocation verticals + regional desks.
  Plan cross-linking + **shared lead-sharing** between sites. Reuse the SKILLS-TREE DNA to
  stamp each new site. Capture per-site entity models when we start each one.

## Parked decisions (raised earlier, not urgent)

- ❓ Homepage hero redesign (owner currently says don't touch homepage).
- ❓ Menu/nav architecture rethink.
- ❓ WooCommerce store — what (if anything) is sold there.
- ❓ Properties CPT = 0 records — decide a source or drop the surface.

---

## QA program (added 2026-06-03)

- 🟢 QA journey-testing script for Cowork shipped: `skills/qa-journey-testing.md`
  (5 personas incl. the Rainbow-Project advertiser; SBTM charters; reports land in
  `docs/qa/`; fix→re-run loop). Hand the PART-A brief to Cowork to start a run.
- 🔴 First full QA run pending (Cowork). Known gaps it will surface and we must
  decide on: advertiser exposure/impressions reporting, project image upload,
  post-payment "what happens next" clarity, advertiser results dashboard.

## Shipped log (history — do not delete)

- 🟢 1.33.0 — projects premium directory + real reviews engine (moderation + schema.org).
- 🟢 1.32.0 — premium professional profile pages + "similar pros".
- 🟢 1.31.0 — state-of-the-art professionals directory (live AJAX filter/sort, colour pills,
  trust badges); city filter LIKE fix; duplicate facets form removed; clean archive title.
- 🟢 1.30.0 — CRITICAL fix: archives showed 5/2702 due to tier INNER JOIN.
- 🟢 1.29.0 — branded archive grids; gov.il whitespace normalization; project mislink fix.
- 🟢 1.27–1.28 — homepage discovery block (kept per owner) + footer directory links (4).
- 🟢 1.26.0 — /catalog/ as directory hub.
- 🟢 Skills tree (`skills/SKILLS-TREE.md`) + this backlog created (2026-06-02).
