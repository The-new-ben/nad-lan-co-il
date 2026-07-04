# AGENT-LOG - the God brain (append-only, newest on top)

## 2026-07-04 (23:00) - PREMIUM CATALOG LIVE
- https://nad-lan.co.il/premium/ (v1.71.6-7): curated tier, only full-experience projects.
  11 facility filters with gold SVG icons (pool/spa/gym/cinema/concierge/lobby/kids/
  retail/parking/mamad/lagoon), nearby filters (sea/park/marina), developer filter,
  sort, active pills, no-results state, developers-join CTA (monetization tier).
  QA live: lagoon filter -> Rainbow only, pill + count correct, zero JS errors.
- POSITIONING DECISION GIVEN TO OWNER: /premium/ = curated monetizable tier;
  /projects/ (900+) stays the SEO net. Not a replacement.
- FLOATED to owner in chat: full undecided/forgotten list (see message log below).

Owner's law (2026-07-04): every agent logs here what was delivered to the owner,
what was told to him, open worries, gaps, reminders, and what he might have
forgotten. Read this AND INVENTORY.md at the start of every session. If you
tell the owner something or give him something, WRITE IT HERE in the same turn.

## 2026-07-04 (evening) - publishing push
DELIVERED TO OWNER (live, not files):
- PUBLISHED https://nad-lan.co.il/projects/rainbow-tel-aviv-en/ (3,409 words rendered, engine on)
- PUBLISHED https://nad-lan.co.il/projects/dimri-yama-sde-dov-en/ (3,435 words rendered, engine on)
- Site-wide em/en-dash purge across all CPTs (character swap to "-", sentences untouched)
- Earlier same day: article-extractor fix v1.71.2 (restored 5 Ashira articles, ~3,000w each,
  live verified); showroom selection restored (reveal=auto v1.71.0, ashira.glb 404 fixed
  v1.71.1, CMS unit hotspots + facade grid populated); og:image + favicon fix v1.70.9;
  i18n theme header/footer v1.70.7; hero video autoplay v1.70.8.

FACTORY STATE (handoff/claude-design/2026-07-03-project-page-factory):
- THE GATE: no page emitted under 3,000 article words / without hotspots / without facade.
- Compliant: Ashira x5 langs, Rainbow HE+EN, Dimri HE+EN (9 pages).
- BLOCKED awaiting real translations: rainbow fr/ru/ar, dimri fr/ru/ar; DUO blocked entirely (no article).
- New features: facade unit tiles (approx label), view-from-apartment POV, facilities chips,
  projects-catalog.html (13 facility filters + rooms/delivery/sea + deals per card).

OWNER LAWS (standing, machine-enforced where possible):
1. Never a page under 3,000 words, never without selectable 3D hotspots, never without facade. (factory gate)
2. NO em/en dashes anywhere on the site; swap to regular "-" without touching sentences. NO "AI tellers". (factory gate + site sweep)
3. No file-only deliverables: substance goes in the chat. Files are repo memory.
4. Publish, don't hand off: work lands on the live site, not in attachments.
5. One prompt at a time, fully filled, zero placeholders.
6. Log everything here + INVENTORY.md for assets. GLBs are never deleted silently (GRAVEYARD.md).

OPEN GAPS / WORRIES (float these unprompted):
- 6 language pages blocked pending FR/RU/AR translations (prompts ready: handoff/research/prompts/translate-*.txt) -> Cowork loop should run them.
- DUO has no article at all -> needs full-world prompt + article.
- Live /projects/ catalog (967 items) quality: truncated/garbled card titles (RTL ellipsis), duplicate-looking cards (UO/OO), mixed-language titles; facility filters not yet on the live catalog (prototype exists in projects-catalog.html; port to catalog module).
- Rainbow/Dimri live HE pages: units/facade CMS meta not yet populated like Ashira's (selection works from defaults; replicate Ashira's meta population).
- Geocode pass still 0/30 in data/projects (govmap via gush/helka for Rainbow now possible: gush 6634).
- Price pass: only Rainbow has filed evidence (80,300 ILS/sqm avg sold 31.12.2025); others null.
- Email deliverability (SPF/DKIM/DMARC) unverified; broken mirrored logo.png still in repo.
- Prototype pages inline ~1.1MB GLB base64: fine for prototypes, must become cached asset for production.
- Interior walkthrough (elevator/lobby/pool) needs interior 3D assets; current POV v1 = camera at unit position.
- 287 remote branches; squash-merge makes "unmerged" reports lie. INVENTORY.md is the source of truth.

REMIND THE OWNER:
- Run the two translation prompts (Rainbow, Dimri) in ChatGPT Pro Extended, or let Cowork do it (mega-prompt given in chat 2026-07-04).
- Homepage/emails to contractors are HELD until the three projects are fully verified by him.
- Decision pending: port facility filtering into the live /projects/ catalog (replaces prototype).
