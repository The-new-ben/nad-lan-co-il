# Skill: Proptech Adoption Roadmap — out-feature Yad2/Madlan, mirror international leaders

> Cited product backlog and sprint workflow for nad-lan.co.il. Built from the global competitor feature audit (Zillow/Redfin/Realtor/Rightmove/REA/Idealista/Compass/Houzz/Opendoor/PropertyGuru/99.co/MAIA) + the Israeli incumbent gap analysis (Yad2 / Madlan / Komo / Homeless / Yad1 / Onmap). Honest about what we can adopt without traffic and what waits. Lawyer-owner moats called out.

## The strategic thesis (the "why anyone would prefer us")

No Israeli portal combines: **(a) Madlan-grade data + (b) Compass-grade workflow + (c) lawyer-grade document trust + (d) modern AI (NL search, concierge, virtual staging)**. That intersection is winnable — and **(c) is uniquely ours** because the owner is a licensed real-estate lawyer (bar 29020). Build (c) as the wedge and (a)/(d) around it. (b) is Phase 2.

## Gap map — us vs the field (real, by feature)

| Feature | Yad2 | Madlan | Compass | Zillow | **nad-lan today** | Verdict |
|---|---|---|---|---|---|---|
| Listings volume | ★★★★ | ★★★ | n/a IL | n/a IL | 5 seed | catch up via Phase 1 |
| Data layer (tax comps / heatmaps / schools / transit) | ★ | **★★★★★** | ★★ | ★★★★ | 0 | adopt Madlan-grade |
| AVM (Hebrew, explainable) | 0 | partial | n/a IL | Zestimate | 0 | **biggest data win** |
| AI search / concierge | 0 | 0 | 0 (US has) | ★★★★ | 0 | **easy first-mover IL** |
| AI listing copy + virtual staging | 0 | 0 | premium | ★★★★ | 0 | adopt |
| 3D tours from phone | 0 | 0 | premium | Zillow 3D Home | 0 | adopt mobile capture |
| Lawyer-grade doc trust (AI contract checker + lawyer review) | 0 | 0 | 0 | 0 | **owner is the moat** | **flagship** |
| Off-market / private exclusives | 0 | 0 | **Compass One** | 0 | 0 | adapt as "רישום שקט" |
| Voluntary residential auction | court only | court only | partial US | n/a | 0 | Phase 3 |
| Reverse auction (sellers post, brokers bid for exclusivity) | 0 | 0 | 0 | 0 | 0 | Phase 2 (compliance-first) |
| Client portal (broker↔client workflow) | 0 | 0 | **Compass One** | 0 | 0 | Phase 2 |
| Sponsored content (labeled ממומן) | partial | 0 | 0 | 0 | spec ready | adopt Phase 1 |
| Lead products + tracking | partial | broker leads | Premier Agent | Premier Agent | endpoint built | adopt Phase 0 |
| Trust badges (verified phone / lawyer-reviewed) | basic | basic | n/a | ✓ | spec ready | adopt |
| English foreign-buyer flow | 0 | 0 | 0 | 0 | 0 | adopt lite (Aliyah SEO) |
| iBuyer | 0 | 0 | 0 | sunset | — | **skip** (capital risk) |

## The product backlog (sprint workflow — sequenced, not à-la-carte)

### Phase 0 — Wedge (0-3 months): the unfair advantage layer

Goal: traffic-independent products that demonstrate uncompetitive value the day a customer registers. Money model: paid lawyer-review + leads + founding-tier directory.

| # | Build | What customer gets | Why now |
|---|---|---|---|
| 0.1 | **AI Contract Checker (free) + Paid Lawyer Review** | Upload חוזה רכישה PDF → AI flags risk sections (cited to §§ of חוק המכר and קוד חוזים) → upsell עו"ד review 48h ₪X | **flagship moat** — no IL competitor has it, the owner IS the licensed reviewer |
| 0.2 | **Hebrew AVM** grounded in `nadlan.gov.il` | Address in → estimate ₪ + explainable comps (last 6 transactions on the street) + lawyer caveat with confidence band | Madlan does data, we add explainability + legal layer |
| 0.3 | **All-in tax-impact calculator** | Inputs: property price + buyer profile + holding period → outputs מס רכישה + projected מס שבח + ריבית משכנתא + היטל השבחה in one number | No IL tool unifies these |
| 0.4 | **Sold-price database + heatmap** | Map view of every transaction in last 24mo from רשות המסים, click to drill | Catch up to Madlan on the data table-stakes |
| 0.5 | **תמ"א 38 / פינוי-בינוי per-address checker** | Address → "this building is in plan X, typical timeline Y, est. value uplift Z, status: at planning committee since 2024" | **uniquely Israeli, none combine address + status + uplift** |
| 0.6 | Lead products live (per leady.co.il pricing — already in customer-value-spec.md §F) | ₪90-150 per validated lead by category | Pay-per-result = no "what did I pay for" risk |
| 0.7 | Founding directory tier (Free/Basic/Pro/Premier already SKUd) | Verified profile + lead delivery + badge | Already built — needs seeding |

### Phase 1 — Listings + workflow (3-9 months): the catch-up + AI layer

Goal: full listing onboarding + modern AI features at parity with Rightmove/REA/Realtor.com — usually with a small lawyer-twist.

| # | Build | Reference | Notes |
|---|---|---|---|
| 1.1 | **AI listing copywriting** (HE + EN) | Rightmove, PropertyGuru | LLM with our voice guardrails + auto-generates the עו"ד-friendly disclaimer block |
| 1.2 | **AI virtual staging** (premium tier) | Zillow Showcase Sept 2025 (+~$7K sale value) | API: Virtual Staging AI / Styldod |
| 1.3 | **Zillow-3D-style mobile 3D capture** | Zillow 3D Home (free) | Skip Matterport hardware path |
| 1.4 | **Map layers** schools/transit/crime/walk score/planning + תמ"א overlay | Walk Score API + Madlan-style | תמ"א overlay = unique |
| 1.5 | **Saved-search alerts + digests** | Standard everywhere | Re-engagement before traffic compounds |
| 1.6 | **"Online Valuation → Broker" lead** | Rightmove (+50% YoY) | Photos → broker reply → we route the lead |
| 1.7 | **LLM property concierge** ("שאל הכל על הנכס") | MAIA (SG), Realtor.com+ | Hebrew RAG per listing + neighborhood facts |
| 1.8 | **NL search + ChatGPT app** | Idealista, Realtor.com in ChatGPT | Submit nad-lan to ChatGPT app directory |
| 1.9 | **Trust-badge system** | PropertyGuru Verified | "✓ נבדק ע"י עו"ד" is the unique one |
| 1.10 | **Auto-generated 9:16 reels** for listings | NAR: videos +400% inquiries; LotZoom auto-vertical | Cheap to ship |
| 1.11 | **Sponsored articles live** (ממומן labeled per §7(c)) | TheMarker model | Honest, no traffic guarantee in Phase 1 — make-good clause |
| 1.12 | **Multi-area map search** (non-contiguous) | Idealista Jan 2026 | Hot in IL where buyers consider 2-3 cities |

### Phase 2 — Marketplace + pro tools (9-18 months): the moat layer

Goal: a place professionals NEED to be, with workflow they don't get elsewhere.

| # | Build | Reference | Compliance notes |
|---|---|---|---|
| 2.1 | **Compass-One-style client portal** (broker ↔ client workflow) | Compass One Feb 2025 | White-label per broker. No IL competitor. Major broker wedge. |
| 2.2 | **Off-market / "רישום שקט" tier** | Compass Private Exclusives | Pre-MLS / pre-public window |
| 2.3 | **Broker commission reverse auction** | Bid My Listing (US), Reverse-auction model | **CRITICAL:** the bid is TERMS (commission %, exclusivity period, marketing plan) — not a property-price bid. Every engagement uses a compliant הזמנה בכתב לתיווך per חוק המתווכים + 2024 transparency תקנות. **Legal review before launch.** |
| 2.4 | **REA-Ignite-style vendor reporting** for brokers | REA Ignite | White-label PDF + dashboard |
| 2.5 | **Developer pre-launch waitlists / VIP signup** | Prefinery / LaunchList | Easy revenue from יזמים |
| 2.6 | **English foreign-buyer + Aliyah flow** | Onmap precedent | SEO + tax/Form 7000 / remote signing module |
| 2.7 | **My Home owner dashboard** | Realtor.com | Equity tracker = strong retention |
| 2.8 | **MLS-style broker feed** (CSV / API in & out) | REA, Compass | No true MLS in IL — we can be the open feed |

### Phase 3 — Premium / moat extension (18+ months)

| # | Build | Reference | Caveat |
|---|---|---|---|
| 3.1 | **Voluntary residential auction product** ("מכרז למכירה") | Allsop UK (88% sale rate 2025), Ten-X | Must comply with **חוק המקרקעין §8 (writing requirement)** — fall of gavel + 72h signing window, not click-to-bind. Bidspirit precedent. Lawyer-mediated. |
| 3.2 | Photo-based valuation uplift/discount | Opendoor 2.0 AI scoping | Adds condition to AVM |
| 3.3 | Houzz-style trades/renovation marketplace | Houzz Pro | Long build, separate brand probably |
| 3.4 | Lead routing + scoring | Zillow Premier Agent | Only once traffic justifies it |
| 3.5 | Property-management SaaS for landlords | (no IL leader) | Tier the platform sells later |

### Skip / Don't build
- **iBuyer / cash-offer** (Opendoor losing $1.3B 2025 — capital + IL market depth = no).
- **Matterport hardware-heavy 3D** — Zillow-style mobile capture is enough.
- **Star-rating system for lawyers/brokers** — IL bar advertising rules + 2024 broker transparency תקנות make star reviews risky. Use **"verified transactions" counter** instead — factual, complies.

## The sprint workflow (next 30 days, owner decisions called out)

> Order matters. Each task either unblocks the next or stands alone.

```
WEEK 1 — Foundations & measurement
  □ Plugin v1.3.0 actually deployed to /wp-content/plugins/ (owner: pick deploy path)
  □ /robots.txt resolves 200 OK (owner: drop file or add nginx line)
  □ GA4 property created → owner sends Measurement ID
  □ Plugin v1.4.0 (GA4 + Clarity gate) pushed → live
  □ /advertise/ page published from customer-value-spec.md (Cowork TASK 4)
  □ /pricing/ → /advertise/ redirect

WEEK 2 — Wedge: contract-checker MVP
  □ Owner decision: "AI flag layer free, lawyer review paid at ₪X"
       Price recommendation: ₪450-750 for 48h review (between TheMarker ₪1.5k sponsored & lawyer cluster lead ₪50-90 — premium service rate)
  □ Upload form on /contract-check/ + Drive intake + lawyer SLA promise
  □ Free AI flag layer behind API (OpenAI/Anthropic w/ Hebrew RAG; system prompt grounds in חוק המכר/חוזה רכישה)
  □ Owner: explicit non-legal-advice disclaimer + bar-rule clearance for marketing language

WEEK 3 — Data wedge
  □ Ingest רשות המסים נדל"ן sold-price database (free, public)
  □ Per-address page template: last 6 transactions on the street + AVM band + תמ"א/פינוי-בינוי status (if available)
  □ Map heatmap (catch Madlan minimum bar)
  □ All-in tax calculator MVP

WEEK 4 — Directory seed + first paying customer
  □ Cowork seeds 6 sample nadlan_professional drafts (already in TASK 5)
  □ Owner recruits 3 founding professionals (lawyer + appraiser + mortgage advisor)
       at free-to-discounted launch tier in exchange for a real testimonial
  □ Owner takes one paid contract-review case (paid customer #1)
  □ Owner posts before/after of /advertise/ to a relevant FB/LinkedIn IL real-estate group (no spam, value-first)

OWNER DECISIONS THIS SPRINT (block until answered)
  1. Plugin deploy path? (zip+upload / sftp / fix pipeline)
  2. GA4 Measurement ID? (G-XXXXXXXXXX)
  3. Contract-review price? (recommended ₪450-750 48h)
  4. Lawyer schema: still "keep as-is"? (decision from previous round — confirming)
  5. Founding professionals: who do you recruit first? (lawyer + appraiser + mortgage advisor)
```

## Verified caveats and unverified items (from the research — keep honest)

- **חוק המתווכים §2(c) carve-out** for publishers: confirmed in the law's structure (§1 definition + §2 license requirement + §9 written-engagement rule) but the agent flagged my sub-section reference as not directly verified in their fetched sources. **Re-confirm before publicly relying on §2(c) as the explicit carve-out** — work with an attorney to nail the exact citation.
- **Zillow ↔ BrightInvestor partnership**: unverified. Confirmed is a separate Zillow ↔ Bright MLS partnership Sept 2025.
- **AVM accuracy** even at Redfin/Zillow runs 1.88-7% median error — publish error bands and disclaimers as part of our AVM trust layer.
- **AI contract review**: Stanford research (cited by LegalOnTech) found general LLMs hallucinate legal advice 69% of the time. Use **specialized RAG with retrieved IL law text**, not raw GPT/Claude calls. The lawyer review is the verification, the AI is the flag-and-explain layer.
- **Israel Bar advertising rules (כללי לשכת עורכי הדין — פרסומת ושידול)**: research couldn't fully verify current text. Owner must clear marketing language with the Bar before launch — the "lawyer-reviewed" badge and any "expert" language is sensitive. See accessibility-israel-is5568.md notes pattern of the same caveat for IS 5568.
- **Voluntary residential auction**: legal in Israel — no specific prohibition — but must satisfy **חוק המקרקעין §8** (writing requirement for real estate transactions). Cannot be click-to-bind UK-Allsop style. Pair gavel-fall with a 72h signing window.

## Source bibliography (verified during 2026-06-01 research)

- **Zillow** Showcase + AI Virtual Staging Sept 2025 — zillow.mediaroom.com/2025-09-10-Zillow-brings-AI-powered-Virtual-Staging-to-Showcase-listings ; Zillow AI Mode Mar 2026 — rismedia.com/2026/03/25/zillow-debuts-ai-mode...
- **Redfin** Estimate — redfin.com/redfin-estimate ; Hot Homes — redfin.com/about/hot-homes
- **Realtor.com** AI image tagging — builtinaustin.com/articles/inside-realtorcoms-ai-powered-image-tagging-service ; Realtor.com+ — nationalmortgageprofessional.com/news/realtorcom-seeks-redefine-digital-home-search-experience-realtorcom
- **Rightmove** Online Valuation — hub.rightmove.co.uk/rightmove-valuations/ ; estateagenttoday.co.uk/breaking-news/2025/08/rightmove-launches-new-digital-valuation-tool
- **REA** Ignite — apps.apple.com/au/app/ignite-by-realestate-com-au/id1303978257 ; iGUIDE acquisition Oct 2025
- **Idealista** multi-area Jan 2026 — idealista.com/en/news/property-for-sale-in-spain/2026/01/28/874395-goodbye-to-grey-maps ; prospecting map — idealista.com/tools/centrodeayuda/en/articulos/prospecting-map/
- **Compass One** Feb 2025 — inman.com/2025/02/03/compass-to-launch-compass-one-client-portal-and-dashboard/ ; prnewswire.com/news-releases/compass-launches-compass-one
- **Houzz Pro AI** — pro.houzz.com/for-pros/software-ai-ar-tools
- **Opendoor 2.0** — inman.com/2025/09/17/opendoors-resurrection-will-there-be-an-ibuyer-afterlife/ ; mikedp.com/opendoor
- **99.co AI Tags** — 99.co/singapore/insider/99-cos-ai-tags/ ; **MAIA** virtual property agent — macaubusiness.com/mogul-sg-launches-maia
- **Madlan** — madlan.co.il + /local/pricesHeatmap + /explore ; **Onmap** — onmap.co.il/en
- **IL portal comparison** — reloux.com/post/best-property-search-platforms-in-israel-2026-guide ; semerenkogroup.com/mapping-the-holy-land-why-israels-statistical-areas-are-the-gold-standard-for-real-estate-tech/
- **AI contract review** (real estate) — dioptra.ai, docjacket.com, listedkit.com, goheather.io ; LegalOnTech buyer guide — legalontech.com/ai-contract-review-software (Stanford 69% hallucination figure)
- **חוק המתווכים** — nevo.co.il/law_html/law00/72991.htm ; 2024 תקנות — barlaw.co.il/practice_areas/litigation/real-estate-litigation/client_updates/new-real-estate-brokers-regulations ; Ynet on exclusivity — ynet.co.il/economy/article/h1mmcwl5p
- **רשות המסים נדל"ן** — nadlan.gov.il
- **תמ"א 38** — gov.il/he/departments/topics/tama38 ; ynet.co.il/economy/article/b1v2ejw1n
- **Auctions** — allsop.co.uk/auctions/residential-auctions/ ; ten-x.com ; il.bidspirit.com/ui/houses?lang=en ; israel-law.co (כינוס נכסים guide 2026) ; tel-aviv.gov.il/AuctionAndCareers/Pages/Property.aspx
- **Reverse listing auction** precedent — washingtonpost.com/business/2021/04/07/online-auction-site-lets-homeowners-list-their-properties-real-estate-agents-bid-sell/
- **Walk Score + Crime Grade** — walkscore.com/professional/walk-score-apis.php ; retechnology.com/news-list/9155-walk-score-launches-crime-grade-for-homes-and-apartments
- **Listing video reels** ROI — blog.hootsuite.com/real-estate-social-media/ (NAR: video +400% inquiries); lotzoom.foundforai.com/platforms/
- **ChatGPT property search apps** — realestatenews.com/2026/03/30/realtor-com-the-latest-portal-to-launch-search-app-in-chatgpt ; idealista.com/en/news/2026/03/13/887103-idealista-launches-its-app-on-chatgpt

_Created 2026-06-01 by Claude Code (claude-opus-4-8). Backlog is sequenced; each phase has a clear owner-decision gate. Phase 0 = unfair advantage (flagship contract-checker + data wedge); Phase 1 = catch-up + AI; Phase 2 = workflow moat; Phase 3 = auction + premium. Skip iBuyer and star-ratings (legal risk in IL)._

