# Renewal room vs the real competitors (26.10.2026)

Scope: the organizer's management room on /my-renewal/ (RenewalRoomPro, built locally in `build/`, **not live**), compared with 16 Israeli tools and 17 global ones. Every competitor claim comes from a public page read on 26.10.2026 (no form, account, trial, demo or contact; no captcha). Full evidence with quotes, per-product 18-row matrices, every search run and the excluded results: `research/israel-raw.md` and `research/global-raw.md`.

Evidence classes in this file: **[page]** seen on the vendor's public page (URL in the evidence file), **[code]** checked in our build by a test or a screenshot (`build/tests/`, `build/shots/checks.json`), **[unverified]** inferred or vendor claim not checked.

## Bottom line (read this first)

1. **The room is not "the best in the world", and this file does not claim it.** The Israeli market already has at least six products built for urban-renewal signatures at published prices from ₪85 to ₪1,190 a month: OneStep, BinuGo, BuildLy, Redirectx, Pinui.Info and VPlans [page]. They do everything our room does on the core rows, and most of them add e-signature, file storage and WhatsApp/SMS sending [page].
2. **After this build the room is at parity on the core rows:** consent per apartment, multi-building complexes, a portfolio, owners per apartment, a change log, neighbour privacy and a committee report [code].
3. **It leads on a narrow, provable set:**
   - the statutory majority shown condition by condition, per building, with "data missing" instead of a guess [code];
   - neighbour privacy proven by an automated test (41 assertions, including a control that proves the leak detector works) [code];
   - no ID copies or files kept anywhere, so less to leak [code];
   - free for residents and committees (the norm, not an edge [page]);
   - Hebrew, English and Russian (only OneStep and Redirectx match this [page]).
4. **It is behind on:** e-signature, file storage, building the owner list from a Tabu extract, sending reminders by WhatsApp or SMS, votes and meeting minutes, staff tasks and a CRM, a published privacy and hosting statement, Arabic, and a published price.
5. **What can honestly be sold to ADAM'S:** a legally careful, privacy-first room that is free for their residents, bundled with exposure on the portal. It is not a replacement for a signing platform. If they already pay for OneStep or BinuGo, our room is an add-on for the residents' side, not a switch.

## The products read

### Israel (16)
| Product | URL (main page read) | For | Price (as published) |
|---|---|---|---|
| OneStep | onestep.co.il/software/hitchadshut-ironit | organizers, developers, law firms | ₪85 / ₪183–218 / ₪490–590 a month + VAT, 14-day trial |
| BinuGo | binugo.com (+ llms.txt) | committees free; lawyers, developers paid | Free; Pro ₪200, Business ₪400 a month |
| BuildLy | buildly.co.il/pricing | developers, organizers | ₪190 / ₪790 / ₪1,190 a month + ₪3 per extra signature |
| Redirectx | redirectx.co.il/he | nine roles incl. organizer, committee, city | free for residents and committee; paid plans unpriced |
| Pinui.Info ("Yazam") | pinui.info | developers, committees | ₪149 / ₪349 / ₪699 / ₪999 a month; residents free |
| VPlans | vplans.com/he/products/urban-renewal | developer ERP + resident portal | ₪500–700 per project a month |
| Asset Rise | asset-rise.byclick.co.il | owners, committee, developers | not published |
| GetStatus | search.getstatus.online/he | owners (transparency), organizers | not shown |
| RolyHome | rolyhome.com/he/product-overview | real-estate firms | per module, not published |
| BMBY | bmby.co.il/התחדשות-עירונית | developers, law firms, tenant-management firms | not published |
| Nadlan2U | nadlan2u.co.il | real-estate CRM adapted | not published |
| ComSign "Nadlan Online" | via nadlancenter.co.il/article/7161 (site blocked automated reading) | lawyers (e-signature) | not stated |
| EasyDo | easydo.co.il | construction companies (bulk signing) | free trial, prices not on page |
| "מגן דיירים" app | App Store id1637421586 | residents (votes) | free; last update May 2024 |
| "משתדרגים" app (Ramat Gan) | Google Play | residents (city information) | free |
| Government Urban Renewal Authority | gov.il (Cloudflare, read from Google snippets only) | everyone | free; no consent tool |

### Global (17)
BuildingLink, Condo Control, AppFolio (associations), Buildium, FrontSteps, TownSq, Vantaca, PayHOA (condo and HOA portals); Commonplace (now Zencity), Go Vocal, EngagementHQ (Granicus), Open Point (ex Social Pinpoint) (resident engagement for councils and regeneration); Civica Election Services, ElectionBuddy, Simply Voting, Lumi (ballots); Borealis Land Agreements (owner-by-owner agreement tracking for land assembly). Published prices: AppFolio from $1.49 per unit a month (50-unit minimum), Buildium $62/$192/$400 a month, TownSq $90–$435 per community a month (e-vote $250 + $25), PayHOA from $49 a month, ElectionBuddy free to 20 voters then $29–$299+ per election, Commonplace £2,250–£50,000 per licence and EngagementHQ £12,000 per unit a year (UK G-Cloud) [page]. **No real product page was found for Singapore en-bloc, Hong Kong compulsory sale or Japanese condo rebuilding consent tracking**; searches returned law and process articles only.

## The capability matrix

Y = yes, P = partial, N = no, ? = not stated on the pages read. "Best competitor" = the strongest product on that row as its page shows it.

| # | Capability an organizer and a committee need | Our room (build, local) | Best competitor on the row | Verdict |
|---|---|---|---|---|
| 1 | Consent status per apartment | Y: five statuses plus a derived "some owners signed", on a facade per building [code] | OneStep "סטטוס חתימה לכל דירה", "מפת החתמה לפי בניין וקומה"; Pinui.Info floor map; VPlans [page] | Parity |
| 2 | Multi-building complex | Y: up to 12 buildings and 1,200 apartments per organizer room; legacy rooms read as one building [code] | OneStep, BuildLy (each building separately), Pinui.Info (% per building) [page] | Parity |
| 3 | Portfolio of complexes | Y: KPIs, filters, stage, signed bar with the two-thirds tick, missing documents, attention reasons, next step [code] | OneStep (one control screen, GIS map), BuildLy, Pinui.Info, VPlans [page] | Parity; OneStep's GIS map is ahead |
| 4 | Owners per apartment, co-owners, heirs | Y: up to 8 owners, share, heir flag, signed flag; typed by hand [code] | OneStep (heirs, abroad, guardians, companies); OneStep, BinuGo, BuildLy, GetStatus and Pinui.Info **import owners from the Tabu PDF** [page] | **Behind** on Tabu import |
| 5 | Documents per apartment, without storing files | Y: four ticks per apartment, no file ever stored (the live rule) [code] | OneStep 3–60 GB, Redirectx 10–60 GB encrypted, VPlans unlimited, BinuGo collects ID and Tabu over WhatsApp [page] | A stance, not a lead: **behind** on convenience, ahead on data minimisation |
| 6 | Stage ladder with legal clocks | P: ten stages with actions; durations only where a source exists (1 of 10); deadlines typed by the organizer with a 30-day warning; **no legal period hard-coded** [code] | OneStep milestones, BinuGo Gantt; GetStatus claims Organizers-Law timeline alerts (in an article only) [page] | Parity; nobody showed legal clocks on a product page |
| 7 | Majority by the law | Y: two thirds of the complex (exact fraction: 50 need 34), three fifths per building (4–5 apartments: 3 and more than two owners), more than half of the common property per building from Tabu shares, an apartment counts only when every owner signed, "data missing" instead of a guess [code, 12 law tests] | BinuGo (weighted by common-property share, all owners must sign), BuildLy (each building, all owners), OneStep (by ownership share, forecast to threshold) [page]; Pinui.Info's FAQ tells residents 80% per building [page] | **Lead, narrow**: all three conditions on one panel with explicit unknowns; others cover some of it |
| 8 | Change log per apartment as evidence | Y: one row per change (who, when, field, from, to, version), append-only from the room; notes logged without their text [code] | OneStep "יומן ביקורת מלא"; Redirectx "מתועדת ובלתי ניתנת לשינוי", kept 12 months [page] | Parity; Redirectx claims immutability, ours is append-only (a DB admin could still edit rows) |
| 9 | Role-based privacy (a neighbour sees only their apartment) | Y: filtered on the server per role; neighbour gets totals plus their approved apartment; committee gets statuses without names; 41 automated checks [code] | Asset Rise (resident sees own threads), Pinui.Info (tenant sees own status), Redirectx ("כל אחד רואה רק את מה שמותר לו") [page] | Parity on the promise; **lead on proof** (nobody else publishes a test) |
| 10 | Committee report | Y: print / PDF report per building and per legal condition, plus an Excel (CSV) export [code] | OneStep: consent report in the format the authority requires, PDF and Excel RTL [page] | **Behind** OneStep (authority format) |
| 11 | Updates feed + WhatsApp | P: feed in the room; each update and the invite link open WhatsApp with the text ready (the organizer's own WhatsApp); periodic consent note [code] | OneStep official WhatsApp through Meta + branded SMS; BinuGo WhatsApp broadcasts with read tracking and an answering bot; Redirectx, VPlans, BMBY, PayHOA, BuildingLink [page] | **Behind**: no sending, no reminders, no read tracking |
| 12 | Languages | P: room in Hebrew, English, Russian; landing in Hebrew and English [code] | OneStep He/En/Ar/Ru; Redirectx He/En/Ru; Simply Voting 17 languages incl. Arabic [page] | Behind OneStep (Arabic) |
| 13 | Phone use | Y: mobile web, checked at 390 px with no sideways scroll [code] | Most Israeli tools are mobile web; VPlans, EasyDo native apps; BuildingLink, TownSq and others native apps [page] | Parity in Israel; behind global portals on native apps |
| 14 | Price for residents / for the organizer | Free for residents and committees (live promise); organizer price **not set** [code] | Free for residents is the norm (BinuGo, Redirectx, BuildLy, Pinui.Info); organizer prices published from ₪85 a month [page] | Behind until Ben sets a price |
| 15 | E-signature | N | 7 of 16 Israeli tools: OneStep, BinuGo (Electronic Signature Law 2001, audit trail), Redirectx, BuildLy (inside the contract), Asset Rise (PAdES), VPlans, BMBY [page] | **Behind** |
| 16 | Assemblies, votes, minutes | N | OneStep (signed minutes, attendance), BinuGo (recorded meetings, Hebrew transcript), Asset Rise (verified votes); Civica, Lumi, TownSq for legal-standing votes [page] | **Behind** |
| 17 | Staff tasks / CRM | P: derived task list and deadlines; no assignable tasks, no CRM [code] | OneStep (tasks with owner and date, AI dialer), Pinui.Info, VPlans, BMBY; BuildLy syncs to Google Calendar [page] | **Behind** |
| 18 | Privacy, hosting, law statement | N for now: a data-processing agreement is open (Ben, lawyer) | Redirectx (servers in Israel, Privacy Law, Amendment 13), BinuGo (Amendment 13, sub-processors), VPlans ISO 27001; global: SOC 2 / ISO 27001 at Vantaca, Lumi, BuildingLink, Go Vocal [page] | **Behind** |

Extra rows Ben asked about:
- **Facade of the building:** not unique. OneStep and Pinui.Info show signing maps by building and floor [page]. Ours draws the facade as an elevation with a pattern for every status, so it reads in black and white and for colour-blind users [code].
- **Distribution:** the room sits on a real-estate portal, but Search Console shows one impression for /my-renewal/ in 90 days (AUDIT.md). That is not a demand argument yet.

## Where competitors are ahead, in order of what an organizer will ask first
1. **"Can the owner sign on the phone?"** Seven Israeli tools: yes. Ours: no.
2. **"Do I have to type every owner?"** Five tools read the Tabu extract. Ours: yes, you type them.
3. **"Does it send the reminders for me?"** OneStep, BinuGo and VPlans send by WhatsApp, SMS and email. Ours only opens WhatsApp for the organizer to send.
4. **"Where do I keep the ID copies?"** Others store them. Ours deliberately does not; the organizer keeps them elsewhere.
5. **Votes and minutes, staff tasks, a CRM, a privacy statement, Arabic, a price list.**

## What the build changed so the comparison is fair (all local, nothing live)
- Organizer account with staff; complexes with several buildings; portfolio route (`build/inc/renewal-org.php`).
- Payload filtered by role before it leaves the server; one-apartment save with a version (409 on a stale save, compare-and-swap merge for two staff on different apartments); append-only change log; owners per apartment; the law panel; deadlines; neighbour claims with organizer approval (`build/inc/renewal-room.php`).
- The RenewalRoomPro UI (`build/assets/urban/renewal-space.js`, `renewal-room.css`), Instruments tokens on the landing and the calculator, and the language-dna word fixes (`build/inc/urban-space.php`, `urban-tools.php`).
- Billing hook coded and **off** (option `nadlan_rr_billing_on`, product id `nadlan_rr_org_product`).
- Tests: `build/tests/test_privacy.php` (41/41), `build/tests/test_room.php` (51/51), `build/shots/checks.json` (22 screenshots: 0 console errors, 0 sideways scroll, every enabled button at 8.83:1 contrast or more).

## What would move the room from parity to a lead (proposals, not built)
1. E-signature through an Israeli provider (ComSign is the incumbent for lawyers [page]), or an export to the organizer's own provider: the biggest gap.
2. Tabu-extract import into owners and common-property shares: it also feeds the third legal condition automatically.
3. WhatsApp Business API reminders (Meta), with read tracking.
4. A public privacy and hosting page plus the data-processing agreement (Amendment 13).
5. Arabic in the room.
6. A published organizer price (Ben).
