# Skill: Customer-Value Spec — what each paying customer actually receives

> Concrete, contractual deliverables per tier. Built to answer "I paid — what did I get?" with a verifiable artifact, fixed-duration position, or pay-per-result — never vague exposure. Aligned with: the global guarantee research (Rightmove/REA/Apartments.com model: position + duration + reporting), Israeli law (חוק המתווכים §2(c) publisher carve-out — we never call ourselves a מתווך and never take a transaction %), and the site's Phase-0 reality (no traffic yet → asset-based + pay-per-lead only).

## A. Professional directory — 4 tiers (already 4 WooCommerce SKUs exist)

### Free Listing — ₪0
**Artifact:** a basic public profile page under `/professionals/<slug>/`.
**Includes:** name, title, profession tag, city, photo, one paragraph bio, one contact link (form, not direct phone).
**Position:** appended to category lists by date.
**Duration:** indefinite (no removal as long as data is accurate).
**Reporting:** none.

### Basic — ₪299 / year (SKU 475)
**Artifact:** the same profile page, **enriched**.
**Includes:** everything in Free + bio up to 400 words, up to 5 portfolio images, areas-of-practice tags, license number badge (where applicable, e.g., bar/RE-broker number), 2 contact channels (form + WhatsApp/phone), a verified "✓ נדל"ן חכם" badge (we verify identity + license).
**Position:** above Free in city/profession listings.
**Duration:** 12 months.
**Reporting:** monthly automated email — profile views, contact clicks.

### Pro — ₪749 / month (SKU 476, first month free)
**Artifact:** enriched profile **+ lead delivery**.
**Includes:** everything in Basic + featured "Pro" badge, up to 15 portfolio images, embedded contact form on the profile, dedicated Q&A section, **inclusion in editor's-pick rotations** on relevant pillar pages (e.g., a real-estate lawyer in 1 of 5 lawyer-spoke articles), **share-of-voice leads from the lead REST endpoint** for matching profession+city (volume not guaranteed in Phase 0 — see policy below).
**Position:** above Basic; one of the first 5 in each city/profession card grid.
**Duration:** month-to-month; cancel anytime, 30-day notice.
**Reporting:** monthly PDF — profile views, profile click-throughs, leads delivered (with timestamps + advertiser-facing IDs), CTA clicks, search queries that surfaced the profile.

### Premier — ₪3,990 / year (SKU 477) **[review price up — currently underpriced for the deliverable below]**
**Artifact:** Pro profile + **dedicated landing microsite + homepage rotation slot**.
**Includes:** everything in Pro + a dedicated URL `/pro/<name>/` styled as a microsite (custom hero image, longer story, testimonials block, video, multiple sections, native green design), **rotating placement in a "מקצוענים נבחרים" homepage row** (currently 1 of 8 rotation slots), **priority lead routing** (leads matched to the profession+city are routed to the Premier first), inclusion in the "מומלצים" footer.
**Position:** top of city/profession listings; homepage rotation; 1 of 6 fixed slots in the editorial newsletter (when active).
**Duration:** 12 months.
**Reporting:** monthly PDF + one quarterly 30-min review call. Includes traffic to the microsite, search queries, leads.

## B. Promoted property listing — private seller/buyer (SKU 490 currently)

**Artifact:** a single `nadlan_property` listing page under `/properties/<slug>/`.
**Includes:** up to 20 photos, full description, map pin, key specs (rooms, area, floor, parking, etc.), embedded contact form, "✓ זוהה ע"י נדל"ן חכם" badge (basic verification: Tabu nesach uploaded + ID checked), share buttons.
**Position:** **guaranteed top-of-results** in its city for 14 days; then standard position for the remainder.
**Duration:** 60 days (renewable).
**Tiers we can sell now:**
- **Free** — basic listing, standard position, 60 days. (Per Yad2/Madlan benchmark — free private listings are the IL norm.)
- **Highlight ₪99 — 14 days top + colored badge + 30-day duration.** (WinWin/Yad2 benchmark: ₪49-99.)
- **Featured ₪249 — 30 days top + auto-bump every 5 days + 60-day duration + cross-post to the saved-search alert list when active.**
**Reporting:** the seller gets a self-serve dashboard widget on their listing — views, contacts, saved counts. Email digest weekly.

## C. Developer / יזם — project mini-site (SKU 489)

**The flagship deliverable** — the actual artifact a developer pays for, traffic-independent.

### Project Page Standard — ₪3,990 / 6 months (re-priced from ₪3,990 unspecified)
**Artifact:** a real project page under `/projects/<project-slug>/`.
**Includes:** hero with up to 5 images/renderings, project specs (location, units, sizes, expected delivery, planning status), floor-plan PDFs, gallery (up to 30 images), one embedded 3D tour (if supplied), full-description section, the developer's logo + about block, **embedded lead form integrated with the lead REST endpoint** (leads piped directly to the developer by email + CSV export), waitlist sign-up button, share buttons.
**Position:** guaranteed listing on `/projects/` and in the relevant city archive for 6 months.
**Duration:** 6 months, renewable.
**Reporting:** monthly PDF: page views, unique visitors, lead count + names/contact, conversion rate, top traffic sources, top search queries that surfaced the page.

### Project Campaign Premium — ₪10,990 / 6 months (SKU under name "קמפיין פרויקט")
**Artifact:** Project Page Standard + **active editorial integration**.
**Includes:** everything Standard + a dedicated **sponsored editorial article** (labeled "תוכן שיווקי") explaining the project for the buyer (written by us, reviewed by the developer), placement in a project-specific landing page with custom URL, **homepage rotation slot** (1 of 8) for 30 days at campaign launch, a **lawyer-friendly disclaimer block** on the project page explaining tax, ערבויות, and lawyer recommendation (E-E-A-T + trust), **priority on saved-search alerts when the project matches**.
**Reporting:** monthly PDF + WhatsApp lead notifications.

### Developer Showcase Annual — ₪19,990 / year **(re-frame to honest deliverable below; do not sell as "exposure")**
**Artifact:** Premium campaign for 2 projects per year + permanent developer profile page (`/developers/<name>/`) with all projects archived + **city analytics report quarterly** (Israel-wide market view, our search-query data on relevant terms).
**Reporting:** monthly + quarterly business review.

## D. Sponsored article (when traffic justifies it — Phase 1+)

**Artifact:** a real article on the site, written by us, reviewed by the brand, labeled **"תוכן שיווקי"** at the top (Consumer Protection Law §7(c) compliant).
**Includes:** 1,800-2,400 words, green canonical design, full editorial style (cards, table, notes, CTAs), bylined to "צוות נדל"ן חכם" with the disclosure label, brand mention + product link + CTA to brand page.
**Position:** indexed in the relevant pillar's spoke list, linked from 2-3 related articles.
**Duration:** evergreen (we maintain SEO refresh quarterly for 12 months; after that, archived link).
**Reporting:** monthly PDF: views, time-on-page, scroll depth, CTA clicks.

**Pricing:** **₪1,500 (client provides draft) / ₪2,500 (we write)**, plus **₪500/month optional "traffic-share"** that adds banner cross-promotion on relevant pages.
**Phase 0 (now):** sell only with transparent live stats and a make-good clause: "if the article gets fewer than X visitors in 90 days, we extend exposure free for another 90 days." No traffic guarantee.
**Phase 2 (≥3,000 mo visitors on the relevant pillar):** add a **guaranteed-minimum visitors** clause (TheMarker model: "≥1,500 uniques in 90 days or extend free / partial refund").

## E. Display advertising — Phase 1+ (NOT YET)

Sell only when we have measurement and a reliable CPM. Israeli digital benchmark ₪4-20 CPM. Targets:
- **Above-the-fold pillar banner** — visible on the pillar page (≥10,000 mo views in Phase 2).
- **Inline article banner** — between H2 sections.
- **Footer banner** — site-wide rotation.

## F. Lead products (Phase 0 OK — we carry the risk)

Per-lead pricing, ex-VAT, aligned to Israeli market (leady.co.il benchmarks):
- **New apartment lead** — ₪100-140 per lead (exclusive ₪140, shared up to 3 ₪100).
- **Investment lead** — ₪80-130.
- **Mortgage lead** — ₪60-90.
- **Lawyer lead** — ₪50-90.
- **Renovation lead** — ₪70-180.

**Definition of a deliverable lead:** name + valid phone or email + Hebrew comment (50+ characters) describing intent + city + budget range. Duplicates within 90 days don't count. Refund/replace if invalid.
**Volume not guaranteed in Phase 0.** Customer buys a pack of 10/50/200 leads; we deliver as they come; unused leads roll over 60 days or refund.

## G. Trust + verification badges (free, but the artifact)

Every paid tier carries a **"✓ אומת על ידי נדל"ן חכם"** badge. Verification = identity + license + Tabu/business registration as relevant. This is **the trust artifact** — it costs us nothing to verify but is the seller of the upsell. Lawyer-owner E-E-A-T: every legal claim we make is reviewed (in JSON-LD schema today).

## H. Universal policies (publish on /advertise/ + advertiser terms)

1. **Traffic commitments**: NONE in Phase 0 (we honestly say "we are growing — these are this month's audited numbers"). We sell the **asset, the position, and the duration**, not the audience.
2. **Make-good policy**: if any guaranteed-position/duration product fails to deliver (downtime, bug, missed placement), we extend free for the equivalent period.
3. **Sponsored content disclosure**: ALL paid/benefit-driven content labeled "תוכן שיווקי" or "ממומן" at the top (Consumer Protection Law §7(c)). Non-negotiable, fines ₪29,490-53,070/violation.
4. **No transaction commissions**: we never take a % of a property sale. We are a publisher/advertising platform (Brokers Law §2(c) carve-out). We never call ourselves or our staff "מתווך".
5. **Cancellation**: month-to-month products cancel with 30-day notice, no penalty. Annual products: full refund within 14 days minus any leads/services already consumed; after 14 days, pro-rata refund of unused months.
6. **Reporting frequency**: monthly PDF (or live dashboard once GA4 is wired). Quarterly review for Premier/Showcase tiers.
7. **Honest current metrics**: every paid product page surfaces a small "audience snapshot" widget — last 30 days views (whole site + relevant pillar), so the advertiser can decide. Updates monthly.

_Created 2026-05-31 by Claude Code. Aligned to monetization-readiness-and-adsales.md (the broader playbook). This file = the public-facing product spec to publish on /advertise/ and into the advertiser terms PDF._
