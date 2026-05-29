# NadLan — Project Briefing for Claude Cowork (or any new agent)

> **Read this in full before doing anything.** It's the condensed history, strategy, competitor map, and guardrails. After this, read `HANDOFF.md` (technical access) and `skills/agent-onboarding.md` (credentials). Then the skills tree.

Last updated: 2026-05-29 by Claude Code (claude-opus-4-8).

---

## 1. What this is, in one sentence

**`נדל״ן חכם` (nad-lan.co.il)** is a premium Hebrew/RTL real-estate **knowledge + tools + catalog** platform, monetized primarily through the **owner's own law practice** (he is a practicing Israeli lawyer, NOT a broker), plus a future **professional directory** (Free / Pro / Premier subscriptions via Stripe), **developer-project ads**, and **sponsored listings**.

## 2. The owner — context you must keep in mind

- **A practicing Israeli lawyer** (עורך דין). Specializes in real-estate transactions.
- Owns multiple legal portals; wife runs the family-law portal that actually makes money.
- Not a developer. Not a marketer. Wants **zero-friction**: people register & pay themselves, leads arrive in his inbox, he sees money in Stripe.
- Tech-tired by uploads/clicks. Heavy preference for self-managing agents. The plugin auto-updater (v1.2.0+) was built to eliminate the manual upload cycle.
- Token-conscious — he watches Claude usage. Honest, brief, value-dense answers; no fluff.
- Pivoted on look: rejected corporate-blue + cartoon-house logo; chose serif-led luxury (Sotheby's/Christie's caliber).

## 3. The goal — make money, beat competitors

**Money path (priority order):**
1. **Closing-attorney fees** from leads → owner's law practice. ~0.5–1% of deal value × 2.5M ₪ apartment = 12,500–25,000 ₪ per closed deal per side. **This is the big number.**
2. **Urban-renewal representation** (tama 38 / pinui-binui) — multi-year, 6–7 figure engagements per building.
3. **Foreign-Jewish investor representation** (US/FR/UK buyers). High ticket, underserved.
4. **Professional directory subscriptions**: Free / Pro 99₪/mo / Premier 299₪/mo. Plan in `skills/payments-pmpro-stripe.md`.
5. **Developer-project advertising** (potentially 20–80K ₪/mo per project — comparable to Madlan/Yad2's rate cards).
6. **Sponsored listings + map pins** (designed-in per `skills/design-monetization-surfaces.md`).
7. **Affiliate referrals** (mortgage brokers, appraisers, inspectors).

**Strategy:** content → calculators → recommender → lead → owner's law practice or partner.

## 4. The competitors — who we beat and how

Researched live (May 2026 Semrush + SERP). Full DNA in `skills/strategy-master.md` §1.

| Competitor | What they win on | Where they're weak |
|---|---|---|
| **Yad2** (~3.2M monthly traffic, whole site) | Inventory, brand recall, "פרסם מודעה חינם" | Looks like a 2010 classifieds board; no calculators; no editorial content |
| **Madlan** (~192K/mo) | Data intelligence (neighborhood profiles, transaction history, price graphs) | Limited editorial; calculators absent; brand reads as "data dashboard" not "trusted advisor" |
| **nadlan.gov.il** | Official transaction source (we cite it) | Government UX, not consumer-facing |
| **nadlanmaster** (#1 SERP for "נדלן להשקעה" 260/mo KD 5) | Editorial investment content, leads → consultants | Bloggy look, weak schema |
| **doron-aharoni / israel-law / prlaw / avocat-en-israel** | Top SERP for "מס רכישה 2026" — **lawyer competitors** | Plain text calculators; no visual interactivity |
| **mizrahi/hapoalim/leumi banks** | Own SERP for "מחשבון משכנתא" (40,500/mo, KD 35) | No 3-track Israeli mix; not Israel-investor-specific |
| **beta-estate, nadlanmaster (Hebrew)** | Top SERP for "השקעה ביוון/פורטוגל" | No regulatory updates, no comparison tool |

**Our wedge — verified via SERP scans:**
- `מחשבון משכנתא` (40,500/mo, KD 35) — banks dominate; we add a 3-track Israel-specific calculator with stress-test. **No property platform competes here.**
- `מס רכישה 2026` — law-firm SERP. Owner IS a lawyer → instant E-E-A-T moat + the only visual bracket simulator.
- `נדלן להשקעה` (260/mo, KD 5) — no dominant authority. We outrank with depth + tools.
- `Airbnb בחו"ל` / `השקעה ביוון` — the new pillar at `/short-term-rentals-abroad/`. Deep article + AI recommender + 7-country comparison. Zero IL competitor offers this combination.

## 5. What we've built — the evolution (May 2026, one massive session)

### Foundation
- **Skills tree** (`skills/*.md` + `AGENTS.md`) — the shared brain across Claude/Codex/Antigravity/Cowork. Append-only `site-state.md` is the living log.
- **Strategy master** + **monetization-lawyer-angle** + **competitor analysis** all committed.
- **Honesty rule** — every doc separates verified vs assumed vs needs-real-input.

### Plugin (`nadlan-config`, v1.2.0 active)
Lived through versions 1.0.0 (mu-plugin, failed) → 1.0.1 (fatal) → 1.0.2 (bare-minimum, success) → 1.0.3 (lead handler) → 1.0.4 (Abilities API attempts) → 1.0.5 (register_meta) → 1.1.0 (catalog CPTs) → 1.1.1 (public lead REST) → 1.1.2 (IndexNow + generator removal) → **1.2.0 (self-hosted auto-updater via plugin-update-checker)** → 1.2.1 (BUILT, NOT UPLOADED — Site Kit generator strip + property meta REST + healthcheck filter). Lessons captured in `skills/nadlan-config-plugin.md`.

### Theme (`nadlan-revenue` v1.1.0)
Forked from Twenty Twenty-Five via owner's UPress server download. Two design rounds with **Lovable**:
- **Round 1** (`docs/design/lovable-output-2026-05-28.md`) — full luxury design system: competitor DNA, WCAG-verified palette, type scale, all components, monogram logo.
- **Round 2** (`docs/design/lovable-output-round-2.md`) — port artifacts: 1,315-line CSS bundle, theme.json fragment, 10 Gutenberg block patterns, monetization surfaces. All ported live.

### Content + UI live
- **Homepage** rebuilt type-led: hero, 6 working tool cards, trust band, guides, dark CTA band.
- **Pillars + 42 city/neighborhood pages** Codex-authored, hub-spoke linked (~153 internal links).
- **Calculators**: mortgage (3-track + stress test), purchase tax (2026 brackets + visual simulator), buy-vs-rent (NYT-style break-even chart).
- **Short-rent-abroad pillar** at `/short-term-rentals-abroad/`: deep 32KB Hebrew article + AI recommender (4 inputs → ranked country) + 7-country comparison (Greece/Portugal/Spain/Italy/Cyprus/Thailand/Dubai with 2026 regulation).
- **Dynamic sitemap** at `/sitemap/` (REST-driven, sort by modified, "חדש" badges).
- **Catalog** at `/catalog/`: REST archive + MapLibre map (free OSM tiles) + 5 seed properties.
- **Site-wide FAB**: WhatsApp `wa.me/972525101555` + tel + lead modal → `POST /wp-json/nadlan/v1/lead` → owner's email.
- **Header**: serif wordmark + monogram seal + pulsing gold dot.
- **Yoast**: 41/42 meta descriptions written, 11 pillars marked cornerstone, breadcrumbs in templates.
- **IndexNow auto-ping** on every publish (Bing/Yandex; Google deprecated theirs).

### Tools we used (and why)
- **Claude Code** (this agent, claude-opus-4-7 then 4-8) — strategy, code, REST orchestration, theme/plugin development, skill authoring.
- **Lovable** (https://lovable.dev) — visual design system. Two prompts ran by the owner; outputs ported by Claude.
- **Codex** (CLI, by owner) — early Hebrew content generation (42 pages). On break until June 2.
- **ChatGPT (owner's $200 tier)** — planned for spoke article writing (prompts in `skills/spoke-prompts-short-rent-abroad.md`).
- **plugin-update-checker** (yahnis-elsts) — vendored, gives "click Update inside WP" UX.
- **MapLibre GL JS** + **OpenStreetMap raster tiles** — free, no key. Map for catalog.
- **Fonts**: Frank Ruhl Libre (Hebrew serif, OFL) + Heebo (Hebrew sans, OFL), both bundled local.
- **Web research**: WebSearch (luxury design references, Israeli SERPs, country regulations for 2026).

## 6. Hard rules for any new agent

1. **Repo is public.** Never commit `WP_APP_PASSWORD` or any secret. See `skills/security-public-repo.md`.
2. **Don't write long Hebrew content yourself** — that burns tokens and isn't your strongest tool. **For long articles use ChatGPT** (owner runs it manually with the prompts in `skills/spoke-prompts-short-rent-abroad.md` and the system rules in `skills/copywriting-skill.md`). You handle short UI strings, publishing, structure, schema, internal linking, design.
3. **No em-dashes (`—`) anywhere user-facing.** Owner explicit. Use `" - "` (regular hyphen with spaces), comma, or colon depending on context. The repo's user-facing files and all live pages were swept on 2026-05-29. Keep them clean. See `skills/copywriting-skill.md`.
4. **No AI-tell phrases:** "חשוב להבין", "ראוי לציין", "במילים אחרות", "בעידן הנוכחי", "עולם הנדל"ן", "אכן", "ללא ספק", stacks of rhetorical questions.
5. **One capability per plugin version** with `function_exists` guards. Don't break the plugin foundation.
6. **Update `skills/site-state.md` after every session.** It's the situation report for the next agent.
7. **Don't put runtime code in the theme `functions.php`** — failed in the past. Use the plugin.
8. **Owner decisions you cannot fake:** Stripe install, PMPro install, PR merges, UPress pull, photography. Stage everything for one click; don't decide for him.

## 7. What you're not building (so you don't drift)

- A generic listings board competing with Yad2 on inventory volume. **We curate.**
- A multi-vertical platform. **Israeli real estate only**, with a focused offshoot for Israelis investing abroad.
- Anything with em-dashes, glassmorphism, parallax, autoplay video, neon colors, pop-ups, exit-intent modals, IAB-style banner ads.
- An English version (yet). Hebrew RTL is everything.
- A blog with daily news. Pillars are evergreen; spokes are evergreen-with-yearly-updates.

## 8. Where things are — pointer map

| Topic | File |
|---|---|
| Technical onboarding + credentials | `HANDOFF.md`, `skills/agent-onboarding.md` |
| Strategy + competitor DNA + keyword clusters | `skills/strategy-master.md` |
| Money model | `skills/monetization-lawyer-angle.md`, `skills/lead-funnel.md`, `skills/payments-pmpro-stripe.md`, `skills/design-monetization-surfaces.md` |
| Brand & design system | `skills/luxury-design-system.md` + sister `design-*.md` files + `docs/design/lovable-output-*.md` |
| Copywriting voice + bans | `skills/copywriting-skill.md` |
| Plugin everything | `skills/nadlan-config-plugin.md`, `skills/plugin-auto-update.md` |
| Catalog architecture | `skills/properties-catalog.md` |
| Short-rent pillar + spoke prompts | `skills/short-term-rentals-abroad.md`, `skills/spoke-prompts-short-rent-abroad.md` |
| Live snapshot (read last 6 blocks!) | `skills/site-state.md` |
| Cross-agent contract | `AGENTS.md`, `skills/agent-coordination-protocol.md` |
| Honest acknowledgments | `skills/honesty-statement.md` |

## 9. Open work waiting for you (in priority order)

1. **Merge PR #2** (owner action) → auto-updater starts working.
2. **Upload plugin v1.2.1** (one last manual upload OR push v1.2.1 onto main once PR #2 is merged so the auto-updater pulls it) → unlocks property meta REST + Site Kit generator strip + IndexNow log proof.
3. **Re-seed property meta** for the 5 catalog properties (ids 360–364) once v1.2.1 active → catalog cards show prices, map shows pins.
4. **Build PMPro+Stripe self-registration flow** per `skills/payments-pmpro-stripe.md` once owner installs PMPro (one click in wp-admin).
5. **Owner runs ChatGPT spoke prompts** → you publish each spoke per the checklist in `skills/spoke-prompts-short-rent-abroad.md`.
6. **Property photography** — blocked on Codex (returns June 2) handling `C:\Users\pro\.codex\generated_images`.

## 10. The voice when you talk to the owner

- Brief. Value-dense. No flattery.
- Honest done / partial / blocked scorecards.
- Don't pretend you did things you didn't. If a sync didn't take effect, say so before he asks.
- He values seeing the cause-and-effect chain, not just outcomes.
- He'll often say "do it all, do it deep" — that's permission, not a request to skip verification.

---

**End of briefing. Now read `HANDOFF.md` + `skills/agent-onboarding.md` + the last 6 blocks of `skills/site-state.md`. Verify REST connectivity. Then resume from the priority list in §9.**
