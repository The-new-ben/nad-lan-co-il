# Lovable Report 0 - Strategy Intake + Keyword Workbook Blueprint

Source: Lovable project https://lovable.dev/projects/a7493b94-2e46-4d38-9c6a-80dcf0905f45
Captured: 2026-06-21
Mode: Plan mode / no build requested
Credits before first prompt: 145 left; 36.1 expiring on 28 June; 5 daily build credits left.

---

NadLan Strategy Hub

Plan

Approve
Today at 12:05 PM

Project name: NadLan SEO Product War Plan

You are Lovable in PLAN MODE. Do not build, do not edit code, do not deploy, do not use Try to fix, and do not continue automatically after this answer. This first run is research/strategy only and should be credit-conscious.

Important constraint: stop at the end and write exactly: READY FOR NEXT PROMPT.

Project context:

NadLan / nad-lan.co.il is a Heb ...

Show more
Waiting for user to approve plan

Planning strategic intents and targets READY FOR NEXT PROMPT

No tasks tracked yet.
Plan

Report 0: NadLan SEO strategy intake + keyword workbook blueprint (research only, no code).

Open plan
Review
Skip
Approve
Plan
Tell Lovable what to do instead...




Plan
Send message
Add files

Drop any files here to add them to your message

Report 0 — NadLan SEO Strategy Intake + Keyword Workbook Blueprint

Research-only. No code, no UI, no implementation. All market/volume/competitor numbers below are directional until verified in Semrush + GSC.

1. Executive Summary

NadLan's goal is to become a premium, trustworthy Israeli real-estate authority — not a long-tail blog farm. The competitive set is Yad2, Yad1, Madlan, Nadlan.com, OnMap, ad.co.il, Nadlan Center, Nadlan Master, Homeless, municipal/board portals, new-project portals, professional directories, and RE news sites. Winning requires owning the hardest commercial Hebrew terms (city + transaction, project names, urban-renewal, mortgage/tax) plus an English/international investor layer that almost no Israeli portal serves well.

Trust precedes growth. A real-estate portal is a YMYL surface (money + legal decisions). Until the public site is free of WooCommerce/cart/notifications/debug/internal-QA leakage, and until project showrooms honestly label official / concept / missing instead of faking facades, every SEO investment is at risk: Google's helpful-content and E-E-A-T signals punish portals that look commercially sloppy, and Israeli RE buyers/investors abandon on the first sign of fakeness. Therefore Stage 1 (public trust cleanup, honest showroom states, healthcheck verification) is a gating prerequisite to scaling content, hubs, and link acquisition.

Strategic posture:

Hubs over posts. City hubs, neighborhood hubs, project hubs, urban-renewal hubs, professional-category hubs, calculator hubs.

Spokes serve hubs. Long-tail only as supporting content for money pages, disambiguation, and anti-cannibalization.

Bilingual from day one (HE primary, EN secondary). International investor traffic is high-CPC, low-competition relative to HE, and a differentiator vs Yad2/Madlan.

Authored, sourced, dated. Every YMYL page gets author, reviewer, last-updated, sources — this is also a Google E-E-A-T requirement.

2. Current Site Audit — Assumptions

All items below are ASSUMPTION unless marked otherwise. None should be treated as verified until Semrush + GSC + a live crawl confirm.

#

	

Assumption

	

Label




A1

	

Public surfaces exist for: new projects, professionals, guides, calculators

	

ASSUMPTION




A2

	

Stage 1 trust cleanup is merged in repo but not confirmed live on UPress (theme pull / cache)

	

NEEDS_VERIFICATION




A3

	

Live plugin healthcheck reports nadlan-config 1.68.2

	

NEEDS_VERIFICATION (live re-check)




A4

	

WooCommerce/cart/notification/debug strings may still leak on non-commerce public pages

	

NEEDS_VERIFICATION




A5

	

Project showroom may still silently fall back to fake facades / stacked placeholders

	

NEEDS_VERIFICATION




A6

	

Site is Hebrew RTL; English surface is absent or minimal

	

ASSUMPTION




A7

	

Indexation hygiene (canonicals, hreflang, robots, sitemap split by type) is unknown

	

NEEDS_VERIFICATION




A8

	

Existing rankings, top pages, and backlink profile

	

NEEDS_VERIFICATION (Semrush + GSC)




A9

	

Schema coverage (RealEstateListing, Residence, Place, Organization, Person, FAQ, BreadcrumbList) is unknown

	

NEEDS_VERIFICATION




A10

	

Core Web Vitals, mobile usability, RTL layout stability on listing/project pages

	

NEEDS_VERIFICATION

Pre-growth gating checks (must pass before Report 2 onward):

Public non-commerce pages show zero Woo/cart/debug/QA strings.

Project showroom states are explicit: official | concept | missing — no silent fallback.

Healthcheck endpoint confirms nadlan-config 1.68.2 live.

robots.txt + sitemap.xml + hreflang are sane.

3. Keyword Workbook Blueprint (column spec)

This is the schema for the future Excel/CSV. Do not populate fully now — Report 2+ will fill it in batches.

Column

	

Type

	

Notes




keyword

	

string

	

Hebrew preserved verbatim; no transliteration




language

	

enum

	

he / en / mixed




audience

	

enum

	

buyer_local / renter_local / seller / investor_local / investor_intl / professional / developer / researcher




country_market

	

enum

	

IL / IL-TLV / IL-JLM / IL-HFA / US / UK / FR / intl




funnel_stage

	

enum

	

awareness / research / comparison / decision / transaction / post_purchase




page_type

	

enum

	

home / city_hub / neighborhood_hub / project_hub / project_page / listing / developer_page / professional_category / professional_profile / calculator / guide / glossary / news / legal_explainer




target_url

	

string

	

Canonical slug pattern, HE + /en/ mirror where applicable




hub_or_spoke

	

enum

	

hub / spoke




search_intent

	

enum

	

informational / navigational / commercial / transactional / local




commercial_value

	

1–5

	

Lead/revenue proximity




difficulty

	

0–100

	

Semrush KD (NEEDS_VERIFICATION)




volume

	

int

	

Semrush monthly (NEEDS_VERIFICATION)




cpc

	

float

	

ILS or USD; mark currency




top_competitor

	

string

	

Domain currently ranking #1–3




serp_features

	

csv

	

local_pack / map / ai_overview / people_also_ask / news / images / video / sitelinks




status

	

enum

	

seed / validated / assigned / published / ranking / parked




verification_flag

	

enum

	

verified / NEEDS_VERIFICATION




legal_flag

	

enum

	

none / LEGAL_REVIEW




asset_flag

	

enum

	

none / REQUIRES_OFFICIAL_ASSET




notes

	

string

	

Cannibalization warnings, hub linkage, schema needs

4. Initial Keyword Clusters (themes, not exhaustive lists)

Each cluster lists hub anchors + representative spoke patterns. Volumes/KD = NEEDS_VERIFICATION.

4.1 Hebrew listings & rentals (highest commercial pressure — Yad2 territory)

Hubs: דירות למכירה ב{עיר}, דירות להשכרה ב{עיר}, {שכונה} דירות למכירה

Spokes: {עיר} {מספר חדרים} חדרים, דירות גן {עיר}, פנטהאוז {עיר}, דופלקס {שכונה}

Notes: Yad2/Madlan dominate. Win via neighborhood depth + transparent comps + honest availability, not by faking inventory.

4.2 New projects & developer/project pages

Hubs: פרויקטים חדשים {עיר}, פרויקטים חדשים ישראל, developer brand hubs ({יזם} פרויקטים)

Project pages: {שם פרויקט} {עיר}, {שם פרויקט} מחירון, {שם פרויקט} תוכניות דירה

Asset rule: each project page is official | concept | missing — REQUIRES_OFFICIAL_ASSET when claiming official.

4.3 Urban renewal — TAMA 38 / pinui binui / hithadshut ironit

Hubs: תמא 38, פינוי בינוי, התחדשות עירונית

Spokes: תמא 38/1 לעומת 38/2, פינוי בינוי {עיר}, זכויות דיירים פינוי בינוי, מיסוי תמא 38, עורך דין תמא 38

LEGAL_REVIEW on all tax/rights claims.

4.4 Mortgage / tax / legal due diligence

Hubs: משכנתא, מס רכישה, מס שבח, בדיקת נכס לפני קניה

Spokes: מחשבון משכנתא, מס רכישה דירה שניה, מס רכישה תושב חוץ, היטל השבחה, הסכם מכר דירה, זכרון דברים

All LEGAL_REVIEW. Pair with calculators (cluster 4.6).

4.5 Professionals directory

Categories: שמאי מקרקעין, עורך דין מקרקעין, בודק דירות / מהנדס בדק בית, מתווך, יועץ משכנתאות

Hub pattern: {מקצוע} ב{עיר} + profile pages.

Trust: verified license #, reviews, response time. REQUIRES_OFFICIAL_ASSET (license verification).

4.6 Calculators & tools (link magnets + lead capture)

מחשבון משכנתא, מחשבון מס רכישה, מחשבון מס שבח, מחשבון החזר חודשי, מחשבון תשואה על נכס, מחשבון היטל השבחה

LEGAL_REVIEW for tax calculators; show formula + last-updated date + disclaimer.

4.7 International investors (English + mixed)

Hubs: buying property in Israel, Israeli real estate for foreign buyers, Tel Aviv apartments for sale, investment property Israel, new developments Tel Aviv

Sub-hubs: Sde Dov apartments, Tel Aviv luxury real estate, Jerusalem property for sale English, Netanya French buyers

Due diligence: Israel real estate tax for foreigners, purchase tax Israel non-resident, Israeli real estate lawyer English, Aliyah property purchase, mortgage Israel foreign buyer

Mixed/transliterated: Tama 38 explained, pinui binui meaning, Nadlan Israel

LEGAL_REVIEW on all foreign-buyer tax/legal pages. High CPC, lower KD than HE equivalents — strategic differentiator.

5. Competitor Research Plan

Targets (tiered):

Tier 1 (portal scale): yad2.co.il, madlan.co.il, yad1.co.il, nadlan.com, onmap.co.il, ad.co.il

Tier 2 (vertical/aggregators): nadlancenter.co.il, nadlanmaster.co.il, homeless.co.il, new-project portals

Tier 3 (content/news/professional): globes/themarker RE sections, lawyer/appraiser directories, municipal urban-renewal pages

Intl benchmark: english.madlan, jpost RE, timesofisrael RE, buyitinisrael, anglo-list

Data to collect per competitor (Semrush + manual):

Domain Authority Score, organic traffic trend (12 mo), top 25 pages by traffic, top 50 keywords by position, branded vs non-branded split.

Hub architecture: city pages, neighborhood pages, project pages — URL patterns, internal linking depth, schema usage.

Content depth on YMYL topics (mortgage, tax, urban renewal): word count, author bylines, last-updated, sources cited.

SERP feature ownership: local pack, AI overview, PAA, image, map.

Backlink profile: referring domains, anchor distribution, top linking pages (Semrush backlink_analysis).

Bilingual coverage: does competitor serve English? hreflang? quality?

UX trust signals: how do they handle missing listings/projects? do they fake? do they label?

Keyword gaps: terms competitors rank for that NadLan does not (competitive_analysis).

Output: competitor matrix + gap list feeding Reports 3–5.

6. Next Lovable Prompts (credit-conscious sequence)

Run these one at a time. Each is scoped to keep credit use small and gate on verification.

Report 1 — Live Trust Verification Checklist. Read-only crawl plan + manual QA checklist to confirm A2–A5 + A7 on the live UPress site. No code. Output: pass/fail table + list of public URLs to recheck.

Report 2 — Semrush Pull Plan (HE). Exact Semrush queries to run for HE clusters 4.1–4.6: domain_analysis on top 6 competitors, keyword_research seeds, serp_analysis on top 20 commercial terms. Output: query list + expected workbook rows. No execution yet.

Report 3 — Semrush Pull Plan (EN + intl investor). Same shape as Report 2 for cluster 4.7.

Report 4 — Workbook Population Batch 1. Execute Report 2 queries, fill workbook rows for clusters 4.1 + 4.2 only. Mark all volume/KD as verified.

Report 5 — Workbook Population Batch 2. Clusters 4.3 + 4.4 + 4.6 (LEGAL_REVIEW heavy).

Report 6 — Workbook Population Batch 3. Cluster 4.5 + 4.7.

Report 7 — Hub Architecture & URL Map. Proposed URL patterns, hreflang plan, sitemap split, canonical rules, anti-cannibalization map. Still no code.

Report 8 — Schema & E-E-A-T Plan. Per page_type: required schema, author/reviewer model, last-updated, sources, disclaimers.

Report 9 — Editorial Calendar + Asset Requirements. Per hub: spokes, owner, LEGAL_REVIEW gates, REQUIRES_OFFICIAL_ASSET list.

Report 10 — Link Acquisition Plan. Digital PR angles, calculator-as-link-magnet plan, partnerships (lawyers, appraisers, developers).

Only after Report 7 approval: first implementation prompt (one hub type at a time).

7. Seed Keyword CSV (sample, ~40 rows)

Volume/KD/CPC = NEEDS_VERIFICATION. Hebrew preserved.

keyword,language,audience,country_market,funnel_stage,page_type,hub_or_spoke,search_intent,commercial_value,verification_flag,legal_flag,asset_flag,notes
דירות למכירה בתל אביב,he,buyer_local,IL-TLV,decision,city_hub,hub,transactional,5,NEEDS_VERIFICATION,none,none,Yad2/Madlan dominate; depth + comps
דירות להשכרה בתל אביב,he,renter_local,IL-TLV,decision,city_hub,hub,transactional,5,NEEDS_VERIFICATION,none,none,Yad2 dominant
דירות למכירה ברמת גן,he,buyer_local,IL,decision,city_hub,hub,transactional,5,NEEDS_VERIFICATION,none,none,
דירות למכירה בירושלים,he,buyer_local,IL-JLM,decision,city_hub,hub,transactional,5,NEEDS_VERIFICATION,none,none,
דירות למכירה בחיפה,he,buyer_local,IL-HFA,decision,city_hub,hub,transactional,4,NEEDS_VERIFICATION,none,none,
דירות גן בתל אביב,he,buyer_local,IL-TLV,decision,city_hub,spoke,transactional,4,NEEDS_VERIFICATION,none,none,
פנטהאוז למכירה תל אביב,he,investor_local,IL-TLV,decision,city_hub,spoke,transactional,5,NEEDS_VERIFICATION,none,none,high CPC
פרויקטים חדשים בתל אביב,he,buyer_local,IL-TLV,research,project_hub,hub,commercial,5,NEEDS_VERIFICATION,none,REQUIRES_OFFICIAL_ASSET,
פרויקטים חדשים בישראל,he,investor_local,IL,research,project_hub,hub,commercial,5,NEEDS_VERIFICATION,none,REQUIRES_OFFICIAL_ASSET,
שדה דב פרויקטים,he,investor_local,IL-TLV,research,project_hub,hub,commercial,5,NEEDS_VERIFICATION,none,REQUIRES_OFFICIAL_ASSET,flagship
מחירון פרויקטים חדשים תל אביב,he,buyer_local,IL-TLV,comparison,project_hub,spoke,commercial,5,NEEDS_VERIFICATION,none,REQUIRES_OFFICIAL_ASSET,
תמא 38,he,buyer_local,IL,research,legal_explainer,hub,informational,4,NEEDS_VERIFICATION,LEGAL_REVIEW,none,
תמא 38/1 לעומת 38/2,he,buyer_local,IL,research,legal_explainer,spoke,informational,3,NEEDS_VERIFICATION,LEGAL_REVIEW,none,
פינוי בינוי,he,buyer_local,IL,research,legal_explainer,hub,informational,4,NEEDS_VERIFICATION,LEGAL_REVIEW,none,
פינוי בינוי תל אביב,he,buyer_local,IL-TLV,research,legal_explainer,spoke,commercial,4,NEEDS_VERIFICATION,LEGAL_REVIEW,none,
התחדשות עירונית,he,buyer_local,IL,research,legal_explainer,hub,informational,3,NEEDS_VERIFICATION,LEGAL_REVIEW,none,
זכויות דיירים פינוי בינוי,he,buyer_local,IL,research,legal_explainer,spoke,informational,4,NEEDS_VERIFICATION,LEGAL_REVIEW,none,
מחשבון משכנתא,he,buyer_local,IL,research,calculator,hub,commercial,5,NEEDS_VERIFICATION,LEGAL_REVIEW,none,link magnet
מחשבון מס רכישה,he,buyer_local,IL,research,calculator,hub,commercial,5,NEEDS_VERIFICATION,LEGAL_REVIEW,none,
מחשבון מס שבח,he,seller,IL,research,calculator,hub,commercial,5,NEEDS_VERIFICATION,LEGAL_REVIEW,none,
מס רכישה דירה שניה,he,investor_local,IL,research,legal_explainer,spoke,commercial,5,NEEDS_VERIFICATION,LEGAL_REVIEW,none,
מס רכישה תושב חוץ,he,investor_intl,IL,research,legal_explainer,spoke,commercial,5,NEEDS_VERIFICATION,LEGAL_REVIEW,none,intl bridge
היטל השבחה,he,seller,IL,research,legal_explainer,spoke,informational,4,NEEDS_VERIFICATION,LEGAL_REVIEW,none,
בדיקת נכס לפני קניה,he,buyer_local,IL,research,guide,hub,commercial,4,NEEDS_VERIFICATION,none,none,
שמאי מקרקעין,he,buyer_local,IL,decision,professional_category,hub,commercial,5,NEEDS_VERIFICATION,none,REQUIRES_OFFICIAL_ASSET,license verify
עורך דין מקרקעין,he,buyer_local,IL,decision,professional_category,hub,commercial,5,NEEDS_VERIFICATION,LEGAL_REVIEW,REQUIRES_OFFICIAL_ASSET,
עורך דין מקרקעין תל אביב,he,buyer_local,IL-TLV,decision,professional_category,spoke,commercial,5,NEEDS_VERIFICATION,LEGAL_REVIEW,REQUIRES_OFFICIAL_ASSET,
בודק דירות,he,buyer_local,IL,decision,professional_category,hub,commercial,4,NEEDS_VERIFICATION,none,REQUIRES_OFFICIAL_ASSET,
יועץ משכנתאות,he,buyer_local,IL,decision,professional_category,hub,commercial,5,NEEDS_VERIFICATION,LEGAL_REVIEW,REQUIRES_OFFICIAL_ASSET,
מתווך תל אביב,he,buyer_local,IL-TLV,decision,professional_category,spoke,commercial,4,NEEDS_VERIFICATION,none,REQUIRES_OFFICIAL_ASSET,
buying property in Israel,en,investor_intl,intl,research,guide,hub,commercial,5,NEEDS_VERIFICATION,LEGAL_REVIEW,none,differentiator
Tel Aviv apartments for sale,en,investor_intl,intl,decision,city_hub,hub,transactional,5,NEEDS_VERIFICATION,none,none,
Jerusalem apartments for sale,en,investor_intl,intl,decision,city_hub,hub,transactional,4,NEEDS_VERIFICATION,none,none,
investment property Israel,en,investor_intl,intl,research,guide,hub,commercial,5,NEEDS_VERIFICATION,LEGAL_REVIEW,none,
new developments Tel Aviv,en,investor_intl,intl,research,project_hub,hub,commercial,5,NEEDS_VERIFICATION,none,REQUIRES_OFFICIAL_ASSET,
Sde Dov apartments,en,investor_intl,intl,decision,project_hub,spoke,transactional,5,NEEDS_VERIFICATION,none,REQUIRES_OFFICIAL_ASSET,flagship
Israel real estate tax for foreigners,en,investor_intl,intl,research,legal_explainer,hub,commercial,5,NEEDS_VERIFICATION,LEGAL_REVIEW,none,
purchase tax Israel non-resident,en,investor_intl,intl,research,legal_explainer,spoke,commercial,5,NEEDS_VERIFICATION,LEGAL_REVIEW,none,
mortgage Israel foreign buyer,en,investor_intl,intl,research,guide,hub,commercial,5,NEEDS_VERIFICATION,LEGAL_REVIEW,none,
Israeli real estate lawyer English,en,investor_intl,intl,decision,professional_category,hub,commercial,5,NEEDS_VERIFICATION,LEGAL_REVIEW,REQUIRES_OFFICIAL_ASSET,
Aliyah property purchase,en,investor_intl,intl,research,guide,spoke,commercial,4,NEEDS_VERIFICATION,LEGAL_REVIEW,none,
Tama 38 explained,mixed,investor_intl,intl,research,legal_explainer,spoke,informational,3,NEEDS_VERIFICATION,LEGAL_REVIEW,none,bridge term
pinui binui meaning,mixed,investor_intl,intl,research,glossary,spoke,informational,2,NEEDS_VERIFICATION,LEGAL_REVIEW,none,
8. Risks & Label Legend

ASSUMPTION — stated without source; revisit before acting.

NEEDS_VERIFICATION — requires Semrush, GSC, or live-site crawl before commitment.

LEGAL_REVIEW — tax, mortgage, contract, foreign-buyer content must be reviewed by qualified IL counsel/tax advisor; publish with author + reviewer + last-updated + disclaimer.

REQUIRES_OFFICIAL_ASSET — project pages, developer pages, professional profiles must use official/verified assets or be labeled concept / missing. No silent fallback, no fake facades.

Top risks:

Skipping trust gating → E-E-A-T penalty, wasted content investment.

Publishing tax/legal content without LEGAL_REVIEW → user harm + liability.

Faking project showrooms → reputational collapse, hard to recover.

Cannibalization between city hubs and project hubs without clear canonical/internal-link rules.

Launching EN surface without hreflang + native-quality copy → worse than not launching.

READY FOR NEXT PROMPT.

B
I
Title