# SKILLS TREE — the portable DNA

> **Purpose.** This is not another flat index (see `README.md` for that). This is the
> **reuse skeleton**: it sorts every skill into a tree and marks what is **🧬 PORTABLE
> DNA** (drop onto any site in the network) vs **🏠 SITE-SPECIFIC** (nad-lan real-estate
> only). When we start a new site in the network — the legal portal, the travel /
> relocation verticals, the regional desks — we open this file, walk the DNA branches in
> order, and stamp our identity onto the new domain fast.
>
> **Rule:** never delete knowledge. When a skill evolves, revise it in place and note the
> date. When a new skill is learned, file it under the right branch here AND in `README.md`.
> Public repo — no partner names, closed prices, or client data (see `security-public-repo.md`).

---

## How to read the tree

- 🧬 **DNA** — portable. The "how we operate" that makes any site feel like ours.
- 🏠 **SITE** — nad-lan-specific (real-estate data, Israeli RE keywords, gov.il sources).
- 🔧 **CODE** — lives as a `plugins/nadlan-config/inc/*.php` module, not just a doc.
- 📄 **DOC** — knowledge/process only.

---

## BRANCH 1 — Operating system (how agents work) 🧬 DNA

The contract layer. Identical on every site.

| Skill | Type | Reuse note |
|---|---|---|
| `../AGENTS.md` | DNA·DOC | Cross-agent contract. Copy verbatim, swap site name. |
| `../HANDOFF.md` | DNA·DOC | Public-safe access map template. |
| `agent-onboarding.md` | DNA·DOC | Credential handshake pattern. |
| `agent-coordination-protocol.md` | DNA·DOC | Multi-agent sync rules. |
| `agent-tooling-strategy.md` | DNA·DOC | Which agent does what. |
| `honesty-statement.md` | DNA·DOC | **Core DNA.** No-flattery, cite-or-flag. Non-negotiable on every site. |
| `security-public-repo.md` | DNA·DOC | What never goes in a public repo. |
| `plugin-discipline.md` / `plugin-auto-update.md` | DNA·DOC | One-capability modules + self-hosted update channel. |
| `nadlan-config-plugin.md` | DNA·DOC | Plugin lessons (rename per site). |
| `codex-plugin-access-and-deploy.md` | DNA·DOC | **The deploy pipeline operator guide** — how ANY agent (Codex/Claude/Cowork) changes the plugin and ships it live. Portable to every site (swap names/URLs). Read before touching plugin code. |

**New-site action:** copy this whole branch first. It is the spine.

---

## BRANCH 2 — SEO & content engine 🧬 DNA (method) / 🏠 SITE (keywords)

| Skill | Type | Reuse note |
|---|---|---|
| `google-blueprint-workflow.md` | DNA·DOC | Research-a-query-before-writing. Portable. |
| `internal-linking-hub-spoke.md` | DNA·DOC | Hub/spoke + anti-cannibalization. **Portable law.** |
| `authority-eeat-program.md` | DNA·DOC | E-E-A-T program. Portable; swap the expert (RE lawyer → travel expert). |
| `article-publishing-protocol.md` / `article-qa-audit.md` | DNA·DOC | Publish checklist + QA gate. Portable. |
| `article-guide-design-pattern.md` | DNA·DOC | Guide/pillar layout. Portable. |
| `copywriting-skill.md` | DNA·DOC | Voice, em-dash ban, forbidden phrases. Portable. |
| `yoast-config.md` | DNA·DOC | Required meta + Person schema. Portable. |
| `content-encyclopedia-glossary-plan.md` | DNA·DOC | Glossary/encyclopedia model. Portable concept — **needs rework, see BACKLOG**. |
| `strategy-master.md` | SITE·DOC | Israeli RE keyword strategy. Re-derive per site. |
| `lovable-competitor-blueprint-2026-06.md` | SITE·DOC | RE competitor teardown. Re-run method per niche. |
| `nadlanmaster-anatomy-and-attack.md` | SITE·DOC | Specific competitor. |

**Portable sub-method = "keyword DNA":** money-pillar → spokes → glossary terms, all
interlinked, expert-authored, schema'd. The *map* changes per site; the *method* doesn't.

---

## BRANCH 3 — Directory / listings platform 🔧 CODE — 🧬 DNA engine, 🏠 SITE data

**This is our strongest reusable asset.** The premium directory engine works for ANY
"index of entities with claim → review → upgrade" — contractors, lawyers, travel agents,
clinics, relocation services. Only the entity type + facets + colors change.

| Module / Skill | Type | Reuse note |
|---|---|---|
| `inc/directory.php` + `inc/directory-assets.php` | DNA·CODE | **Generic directory engine.** Live AJAX filter/sort/search, colour-coded category pills, premium cards, REST. Swap the taxonomy (profession → lawyer-specialty / travel-service). |
| `inc/reviews.php` | DNA·CODE | **Generic reviews engine.** 5-star + moderation + schema.org. Works on any entity CPT. |
| `inc/archive-grid.php` | DNA·CODE | Branded archive fallback. |
| `inc/facets.php` | DNA·CODE | Server-side filter translation. |
| `inc/claim.php` + `inc/tiers.php` | DNA·CODE | Free-card → claim → trial → paid-tier funnel. **The monetization spine.** |
| `inc/catalog-meta.php` | DNA·CODE | Entity + claim meta registration. |
| `inc/import.php` | SITE·CODE | gov.il CKAN importer. Per site: new data source, same upsert/normalize pattern. |
| `inc/city-hubs.php` | DNA·CODE | Geo-hub generator w/ noindex floor. Portable to any geo-indexed site. |
| `inc/schema.php` | DNA·CODE | Per-entity JSON-LD + **thin-content noindex guard** (anti-cannibalization). Critical DNA. |
| `inc/auction.php` + `inc/esign.php` | SITE·CODE | Auction engine (RE-specific; dormant). |
| `listings-auction-directory-architecture.md` | DNA·DOC | The architecture doc behind all of the above. |
| `directory-listings-project-plan.md` | SITE·DOC | nad-lan rollout plan. |

**New-site action:** fork `directory.php` + `reviews.php` + `tiers.php` + `claim.php` →
rename CPT, redefine the category taxonomy + colours, point `import.php` at the new source.
~1 day to a working premium directory on a new vertical.

---

## BRANCH 4 — Monetization & revenue 🧬 DNA (model) / 🔧 partial CODE

| Skill | Type | Reuse note |
|---|---|---|
| `inc/tiers.php` | DNA·CODE | Free/Pro/Premier gating. Checkout activation is wired by `inc/advertiser-orders.php`; live QA still required. |
| `inc/advertiser-center.php` | DNA·CODE | Customer-facing paid advertiser center: owned assets, completion, orders, views, inquiries, Studio links, upgrade paths. |
| `inc/advertiser-orders.php` | DNA·CODE | Woo paid order bridge: `card_id` to `paid_tier`, `campaign_end`, paid order/product ids, and daily expiry downgrade. |
| `inc/lead-routing.php` | DNA·CODE | Paid-card inquiry delivery boundary: exact `lead_card_id` -> owner, `paid_tier` gate, delivery trace, bounded ops log. |
| `inc/lead-drip.php` | DNA·CODE | 6-step nurture sequence. Portable. |
| `lead-funnel.md` | DNA·DOC | Funnel design. Portable. |
| `advertiser-monetization-system.md` | DNA·DOC | Self-serve advertiser journey standard: pay, edit, upload, report, renew. |
| `monetization-lawyer-angle.md` | SITE·DOC | RE-lawyer lead angle (owner is the expert). |
| `monetization-readiness-and-adsales.md` | DNA·DOC | Ad-sales readiness. Portable. |
| `design-monetization-surfaces.md` | DNA·DOC | Sponsored slots, ad reservations. Portable. |
| `payments-woo-greeninvoice.md` | DNA·DOC | **LIVE stack:** WooCommerce + PMS + Green Invoice/Morning gateway. Smoke-tested. Cards: ₪349 Pro, ₪749 Premier, ₪3,990 project campaign. Gateway is one-charge — monthly = manual standing order, or sell annual. |
| `customer-value-spec.md` | DNA·DOC | What the customer actually pays for. |

**Revenue DNA (the model, portable to every site):**
1. Free useful entity pages → traffic + claim incentive
2. Reviews + trust badges → reason to claim
3. Claim → trial → **paid tier to stay featured / unlock contact** (recurring)
4. High-intent lead routing to a partner → **per-lead or per-deal commission** (the fat)
5. Sponsored featured placement sold to the biggest players (the fatter)

---

## BRANCH 5 — Design system 🧬 DNA

Portable look-and-feel. Re-skin colours per brand, keep the structure.

| Skill | Type |
|---|---|
| `luxury-design-language.md` / `luxury-design-system.md` | DNA·DOC |
| `design-components.md` / `design-page-patterns.md` / `design-implementation.md` | DNA·DOC |
| `design-rtl-hebrew.md` | DNA·DOC (Hebrew/RTL sites) |
| `design-micro-interactions.md` / `visual-design-skill.md` | DNA·DOC |
| `design-logo-mark.md` | DNA·DOC (per-brand output) |
| `accessibility-israel-is5568.md` | DNA·DOC (IL legal requirement) |
| `theme-fork-decision.md` | DNA·DOC |
| `image-pipeline.md` / `interactive-widgets.md` | DNA·DOC |

---

## BRANCH 6 — Off-site growth & business presence 🧬 DNA  *(thin — see BACKLOG)*

The weakest branch today. Needs building (free-channel playbooks).

| Skill | Type | Status |
|---|---|---|
| `cowork-prompt-business-readiness.md` | DNA·DOC | Cowork business-profile prompt |
| `cowork-prompt-ga4-sitekit.md` | DNA·DOC | Analytics setup |
| `proptech-adoption-roadmap.md` | SITE·DOC | RE adoption |
| **MISSING: free-backlink playbook** | — | TODO |
| **MISSING: Google Business Profile playbook** | — | TODO |
| **MISSING: organic social (TikTok/IG/FB) SEO-signal playbook** | — | TODO |

---

## NEW-SITE BOOTSTRAP (the DNA stamp, in order)

When we open a new domain in the network:

1. **Spine** — copy Branch 1 (operating system), rename site.
2. **Plugin** — fork `nadlan-config` → `<site>-config`; keep Branch 3 + 4 CODE modules.
3. **Entity model** — define the directory's entity + category taxonomy + colours + data source.
4. **SEO map** — run Branch 2 method to derive the new keyword tree (money pillar → spokes → glossary).
5. **Design** — re-skin Branch 5 to the new brand.
6. **Monetize** — wire Branch 4 model (claim → tier → lead/commission) from day one.
7. **Off-site** — run Branch 6 playbooks for free traffic + links.

**Network note (private context, kept generic on purpose):** the owner runs a multi-site
group — a legal portal, travel/relocation verticals, and regional desks — intended to
cross-link and share leads. Cross-site lead-sharing + shared identity is a future program;
capture requirements in BACKLOG under "Network".
