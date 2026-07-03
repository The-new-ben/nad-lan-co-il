# God-mode scorecard - nad-lan.co.il, 2026-07-03

The whole product, broken into blocks and layers, graded like a parent
watching a child grow: against its own past (June 2026), against where it
must be (the "choose your apartment from inside the building" category), and
against Zillow, Compass, Madlan and Yad2. Evidence: live rendered bodies
fetched today (homepage, Ashira HE/RU, Rainbow, /properties/, /projects/,
/professionals/, /en/, /advertise/, sample listing) + healthcheck v1.70.0 +
the 2026-07-01 competitive teardown + the 2026-07-02 module audit.

Grade scale: A = world-class for our stage, B = solid but visibly behind the
benchmark, C = functioning but not competitive, D = liability.

## Weights (what actually decides if this product wins)
| Axis | Weight | Why |
|---|---|---|
| Differentiation (the showroom promise) | 25% | The only reason to exist next to Yad2/Madlan |
| Trust and honesty | 20% | Our declared brand law; Madlan wins today on data trust |
| Supply (real inventory + real data) | 20% | Zero real supply = beautiful empty mall |
| Design and brand | 15% | The premium feel is real leverage with contractors |
| SEO / distribution | 10% | Traffic engine, compounding |
| Tech foundation | 10% | Pipeline, stability, speed of iteration |

## Block 1 - Homepage (12 bands)
- Design: **A-**. The cream/ink/gold system with the sketch plates is now a
  coherent identity; no Israeli portal looks like this. Madlan's homepage is
  a search box with cards; Yad2 is a classifieds wall; we look like Compass.
  Minus: the dark intl band and theater band flirt with "two heroes".
- UX/practical: **B+**. Ticker, browse mega-menu, tabs, tools all work. The
  gap vs Zillow: their homepage IS a search engine; ours narrates first,
  searches second. Acceptable while supply is thin, wrong once real.
- Honesty: **A** (as of today). The fake "ארצי" average is gone with a
  structural gate, not a patch; snapshot labeled with source + date. This is
  now ahead of Yad2 (which shows asking-price noise as truth).
- Tech: **B+**. Video lazy + idle start, LCP untouched, content guard defends
  against the parent-theme ghost. Minus: the guard is a countermeasure, not a
  cure - the parent theme is still out-of-repo (see Block 9).
- SEO: **B**. Title/meta owned, magazine feeds fresh content. Two h1s render
  on index pages (brand + page title) - dilutes heading signal.
- vs past: June homepage was a dead showroom clone. Biggest single leap in
  the product's life.

## Block 2 - Flagship project pages (Ashira, Rainbow, Dimri)
- Design: **A-**. Long, editorial, one unified map with layer chips
  (comps/schools/transit/3D/satellite) - this beats Madlan's project pages
  and is the closest thing in Israel to a Compass listing page.
- UX: **B+**. Price band -> comps table -> map -> showroom flows well. Minus:
  page length on mobile is heavy; no sticky unit-CTA on scroll.
- Honesty: **B+**. Comps are real catalog-derived, language is non-binding.
  Missing: the price band should carry the same explicit "אומדן" framing on
  ALL projects (verified on Rainbow, weaker on Ashira).
- SEO: **B-** and inconsistent between siblings (a defect by our own law):
  - Ashira title is keyword-stuffed ("...שדה דב תל אביב מחיר") vs Rainbow's
    clean editorial title. h1 carries an en-dash entity.
  - Rainbow has AggregateOffer + Place + LocationFeatureSpecification;
    Ashira does not - same surface, unequal schema.
  - Translated pages (RU checked): NO h1 at all. FR/AR/EN likely same.
- vs competitors: structure ahead of Madlan; data depth behind (they show
  real transaction history from gov data, we show catalog comps).

## Block 3 - The 3D showroom engine (the differentiator)
- Product: **A-**. Per-unit selection inside the building with cinematic
  camera, facade picker, live view-from-unit - no Israeli competitor has a
  buyer-facing equivalent. Zillow's 3D Home is tours, not unit choice; this
  is genuinely category-defining.
- Coverage: **C**. 965 projects tracked, 13 with 3D, 7 with GLB (0.7%). The
  category-defining feature exists on less than 1% of the catalog. The
  generate-buildings.mjs factory works - it has not been industrialized.
- Robustness: **B**. The healthcheck flag list (60+ v16.9x fixes) tells the
  truth: mobile interaction needed a long tail of patches. It is stable now,
  but every new device class is a risk.
- Future: **A** if coverage scales; **C** if it stays a 7-building demo.

## Block 4 - Listings (index, detail, wizard)
- Design: **A-** after the plate factory - all cards now share one artist's
  hand (verified today: both panes, 6 cards, zero off-DNA images).
- Practical/supply: **D+**. Seven demo listings. The wizard works, the pages
  are world-class, and there is nothing real to buy. Yad2 has hundreds of
  thousands; Madlan mirrors them. This is THE existential gap.
- Honesty: **A**. "לדוגמה" on every demo listing, disclaimers present (5 on
  the checked listing page).
- SEO: **B+**. ItemList schema on the index; listing pages carry structured
  data.

## Block 5 - Professionals directory
- **C+** overall. Structure, tiers, claim flow, vignette plan all exist;
  actual verified professionals: effectively zero (tiers: 1 free, 1 premier).
  Monogram avatars keep it honest. Same disease as listings: supply.

## Block 6 - Content and magazine
- **B+**. Eight articles including the 2,000+ word 690K pair (HE+EN) with
  NewsArticle+FAQPage schema and branded charts; magazine band feeds the
  homepage; IndexNow pinging works. vs Madlan's content machine: per-article
  quality equal or better, volume ~2 orders of magnitude behind. Content is
  currently our only compounding traffic asset - cadence matters more than
  any single piece.

## Block 7 - International (/en/ + translated project pages)
- **B-**. /en/ hub is clean (single h1, good narrative). Translated project
  pages are content-rich but structurally broken (no h1, unchecked hreflang
  wiring). Ambition ahead of execution; fine for this stage if the h1/hreflang
  layer gets one focused pass.

## Block 8 - Monetization (/advertise/, advertiser center, tiers)
- **B-** on plumbing, **D** on revenue: MRR 0, one active paid tier, 0 leads
  in 7 days. The Woo products, order bridge, dunning, admin control all exist
  and are healthchecked - the machine is built and idling. It waits on
  Block 4/5 supply and on the contractor outreach (plan written 2026-07-02,
  not yet executed).

## Block 9 - Infrastructure and ops
- **A-**. The deploy pipeline is now a codified skill proven across 30+
  releases including today's (merge -> deploy -> verify -> route deleted in
  minutes). Healthcheck depth is exceptional. Version-constant cache-busting
  works (verified ?ver=1.70.0 on engine assets today).
- Standing risks: the parent theme nadlan-revenue is NOT in the repo and
  actively fights us (ghost renderer); Code Snippets remains a loaded gun
  (mitigated by skill law + recovery drill); kill-list modules still ship
  dead weight in every zip.

## Block 10 - Data honesty layer
- **A-** and genuinely differentiating. Authenticity ladder for imagery
  (blur beats fake), honest ticker gate (today), non-binding language,
  source+date labels. The missing piece for an A: REAL market data - the
  nadlan.gov.il transaction feed would let us show true neighborhood prices
  where Madlan currently owns trust.

## The report card, one line per block
| Block | Today | June | Trajectory |
|---|---|---|---|
| Homepage | A- | D (ghost) | steep up |
| Project pages | B+ | B- | up, consistency debt |
| 3D showroom | A- product / C coverage | B- | up, must scale |
| Listings | A- craft / D+ supply | C | craft up, supply flat |
| Professionals | C+ | C | flat |
| Content | B+ | D | up |
| International | B- | none | new |
| Monetization | B- plumbing / D revenue | C- | plumbing up |
| Infrastructure | A- | B- | up |
| Data honesty | A- | B | up |

## Weighted verdict - are we growing in the right direction?
**Yes - the child is growing into exactly who we said he would be, and the
next year of his life is decided by supply, not by more beauty.**

Applying the weights: differentiation (25%) scores high but on 0.7% coverage;
honesty (20%) is now a real asset; supply (20%) is the near-failing grade
dragging everything - demo listings, two professionals, zero MRR; design
(15%) is bankable; SEO (10%) is mid with cheap known fixes; tech (10%) is
strong. Weighted, the product sits around **B**, with an A-grade soul and a
D-grade inventory.

The strategic read: we have finished building the thing that makes contractors
say yes (premium look, per-unit showroom, honest data culture). Every
additional aesthetic hour now yields less than an hour spent putting REAL
projects, REAL transaction data, and REAL professionals inside it. The three
moves that change the grade: (1) execute the contractor outreach with the
flagships as the demo; (2) wire the gov transaction feed so price surfaces
match Madlan's trust; (3) industrialize the GLB factory so 3D coverage stops
being a rounding error. In parallel, one cheap consistency pass (titles, h1s,
sibling schema, ItemList on /projects/, duplicate h1s) removes the SEO drag.
