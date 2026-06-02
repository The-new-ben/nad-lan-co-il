# BACKLOG — the living follow-up list

> **Why this exists.** The owner asked for one place that captures everything we agree to
> do, so nothing is forgotten between sessions. **Any agent: read this at session start,
> update it at session end.** Newest decisions win. Don't delete done items — move them to
> the bottom log so we keep the history.
>
> Status keys: 🔴 not started · 🟡 in progress · 🟢 shipped · 🧊 future/parked · ❓ needs owner decision
>
> Last updated: 2026-06-02

---

## P0 — Revenue (do first; the site earns ₪0 today)

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

- 🔴 **Glossary rewrite to "magic."** Owner: current writing + titles are weak, reads like a
  flat page. Wants flowing, Wikipedia-DNA prose with two-way linking (pages → terms, terms
  → pillars/spokes). Research best-in-class glossary UX. Keep noindex on thin terms until
  enriched (anti-cannibalization). ❓ keep/restructure decision after redesign.
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

- 🔴 **AI concierge.** Embedded assistant that knows glossary + directory + calculators,
  answers visitors, qualifies + routes leads before they reach the owner. **Research GitHub
  for existing WP AI-chat / RAG plugins — do NOT build from zero.** Owner approved.
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
