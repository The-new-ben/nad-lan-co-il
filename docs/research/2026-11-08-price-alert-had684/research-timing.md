# Popup timing evidence, round 2 (nad-lan.co.il price alert)

This file adds to research-popup-cro.md. It does not repeat that file's Wisepops delay buckets, Omnisend, Popupsmart, Sumo, Google, NN/g, Freedman & Fraser or GeekEstate 2008 material. [I] means independent (academic or forum). [V] means vendor or vendor-hosted. Every source was read on 8.11.2026 unless marked "snippet", which means it was seen only in search results because the page blocked my tools.

## 1. When to interrupt: academic research

- **Adamczyk & Bailey, CHI 2004** [I] https://hci.rwth-aachen.de/materials/conferences/CHI2004/1p271.pdf
  - Design: N=16; news alerts during editing, search and video tasks at a predicted best moment (between subtasks), a worst moment (mid-action), a random moment, or never.
  - Measured: annoyance, frustration, time pressure, effort, "respect" and resumption lag.
  - Results: the best moment showed "a 56% reduction from the worst condition" in annoyance, and was 43% lower than random. It earned 43% more respect than the worst moment and 27% more than random. Resumption lag showed no significant effect.
  - → A timer that is effectively random scores worse than a moment chosen from what the user is doing.
- **Bailey & Konstan, Computers in Human Behavior 2006** [I] https://interruptions.net/literature/Bailey-CHB06_1.pdf
  - Design: N=50; mid-task interruption compared with the same content shown at a task boundary.
  - Results: mid-task cost 3–27% more time, twice the errors, 31–106% more annoyance and twice the rise in anxiety.
  - Quote: "deferring presentation for a short time, i.e. just a few seconds".
  - → Hitting a boundary matters more than waiting a long time.
- **Iqbal & Bailey, CHI 2008** [I] https://www.interruptions.net/literature/Iqbal-CHI08.pdf
  - Design: 16 users doing 2-hour real tasks; breakpoints were detected automatically.
  - Quote: "scheduling notifications at breakpoints reduces frustration and reaction time".
  - Frustration (7-point scale): medium breakpoint 2.6, coarse 3.6, immediate 4.5, mid-action 5.5.
  - Reaction time: 3.07 s at breakpoints vs 4.08 s immediate (p<0.056).
  - Relevant content frustrated less (3.59 vs 4.98). Mean deferral was under 90 s.
  - → Wait for the next natural pause, usually under 90 s away, and make the message fit the page.
- **Okoshi, Tsubouchi et al., Yahoo! JAPAN app, PerCom/UbiComp 2017** [I, academic with industry] https://interruptions.net/literature/Tsubouchi-UbiComp17.pdf
  - Design: 687,840 users for 21 days; notifications held until the phone's sensors showed a breakpoint, an average delay of 4 minutes.
  - Quote: response time "is significantly reduced (49.7%)".
  - Results: higher click rate and engagement over the whole study.
  - → In the largest real-world test, waiting for a breakpoint on phones raised engagement.
- **Edwards, Li & Lee, Journal of Advertising 2002, pop-up ads** [I] https://www.gwern.net/doc/economics/advertising/2002-edwards.pdf
  - Design: about 373 participants; a centred pop-up appeared mid-reading, between pages, or on exit.
  - Cognitive intensity when it appeared: mid-reading 5.20, between pages 3.97, exit 3.87. Reactance: 3.32 vs 2.83 between pages.
  - Intrusiveness: 4.42 immersed vs 3.70 less engaged; task-related ad less intrusive (3.64 vs 4.24).
  - Quote: "viewers should be exposed to pop-up ads only at breaks in content".
  - Quote: "switching between pages offered such a break."
  - → Show the popup at a page change or at the end of a section, never mid-read. Area-relevant content lowers intrusiveness.

## 2. Psychology of asking after engagement

- **Reciprocity:** Regan 1971, JESP 7:627–639, https://doi.org/10.1016/0022-1031(71)90025-4 [I]. Paper not read. Secondary summaries give 1.73 vs 0.92 raffle tickets after an unasked-for favour. → Give the area's price data first, then ask.
- **Commitment and consistency:** Freedman & Fraser is already in the previous file (S23). → A small prior action (opening a second listing, using a filter or calculator) makes "keep me updated" consistent with what they already did.
- **Endowed progress:** Nunes & Drèze 2006, JCR 32(4):504–512. The Wharton summary at https://knowledge.wharton.upenn.edu/?p=5630 [I] confirms the design: 300 car-wash cards, 8 required washes, with or without 2 stamps given free. The 34% vs 19% completion rates come from secondary sources only. → Frame the alert as continuing their search ("we'll keep watching the area you looked at").
- **Goal gradient:** Kivetz, Urminsky & Zheng 2006, JMR 43:39–58, https://business.columbia.edu/sites/default/files-efs/pubfiles/1200/goalgradient.pdf [I]. Time between purchases fell 20% as customers neared the reward. Web users rated more songs per visit as they approached the goal. → Motivation grows with progress, so ask deep in a session rather than at its start.
- **IKEA effect:** Norton, Mochon & Ariely 2012, JCP 22(3):453–460, http://nrs.harvard.edu/urn-3:HUL.InstRepos:12136084 [I]. Builders bid $0.78 vs $0.48 (+63%). The effect holds only "when labor results in successful completion of tasks". → Ask right after they finish setting up a search or filter, not during it.
- **Sunk cost:** Arkes & Blumer 1985, OBHDP 35:124–140 [I]. Secondary summaries: 4.11 plays attended (full price) vs 3.32 and 3.29 (discounted). Kivetz ruled sunk cost out. → Weak; don't lean on it.
- **Reactance** (Brehm), measured for pop-ups in Edwards 2002 above: perceived value "tempered feelings of intrusiveness".

## 3. Practitioner timing changes

- **HubSpot** [V, own test] https://blog.hubspot.com/marketing/how-to-add-a-slide-in-call-to-action-to-your-blog-posts
  - Test (2014): slide-in vs static end-of-post CTA, 10 posts, 1 month: CTR +192%, submissions +27%, lower conversion per click. Trigger options were 50% scroll or 7 s; the one used is not stated.
  - → A slide-in during reading beat an end-of-page ask most readers never reach.
- **Organic Aromas** [V-adjacent: written by an Omnisend marketer, published by Convert] https://www.convert.com/blog/growth-marketing/use-exit-intent-popups-to-boost-your-signups-by-150-in-just-15-minutes/
  - Baseline: about 250 signups a month.
  - Immediate popup: 135 signups in a week, 7.4% conversion.
  - "only show up after three clicks": fewer signups; 14.1% of the new subscribers bought.
  - Exit intent: 660 signups a month (+150%); 19.03% of subscribers bought.
  - → Later and behaviour-based triggers produced buyers rather than just more emails.
- **Sugarrae (Rae Hoffman, 2015)** [I-practitioner; uses affiliate links] https://sugarrae.com/blogging/do-popups-work/
  - 5 s delay plus 20% scroll: 0.47%. Exit intent alone: 0.22%. Sidebar form: 0.03%.
  - → On a content site, "engaged and still reading" beat exit intent by about 2x.
- **Backlinko / Brian Dean on Sumo** [V-hosted] https://bdow.com/?p=6266
  - Result: 1.73% → 4.83% (2-day window).
  - Quote: the form "shows up when someone has actually already engaged with your content".
  - Caveat: the copy also changed, so timing is not isolated.
- **ProBlogger (Darren Rowse, 23.10.2008)** [I-practitioner] https://problogger.com/how-to-drastically-increase-subscriber-numbers-to-your-email-newsletter/
  - Result: 40 → 350+ subscribers a day.
  - Quote: forms "that take longer periods of time to appear" have a "slightly higher signup rate".
- **Wisepops** [V; no sample given] https://wisepops.com/blog/popup-best-practice (4.12.2025) and https://wisepops.com/blog/guide-to-popup-targeting (16.1.2026)
  - A second-page trigger "increased attributed revenue by 39%" vs immediate display, with a 28.98% conversion rate.
  - Page 2+ "increases median conversion by 39–52%".
  - 20–50 s delays "reduce bounce by up to 45%".
  - "Immediate popups (under 5 seconds) can increase bounce rate by up to 5 times."
  - → The only vendor support found for a 20–50 s window, and it carries no methodology.
- **True Citrus (Privy blog, republished 27.3.2023)** [V] https://ecommercefastlane.com/how-to-optimize-your-shopify-store-with-a-b-tests-and-4-ways-privy-customers-are-using-them-to-improve-their-online-conversions/ — 10 s beat 15 s by 13.2%. Ecommerce, one store.
- **Thomasnet registration wall** [I, GoodUI, 19.2.2021] https://goodui.org/blog/why-did-thomasnet-reject-a-registration-wall-a-b-test-with-a-record-1135-to-signups/ — signups +1135%, company-profile visits −18%, so the wall was rejected. → Count downstream engagement, not signups alone.
- **Not found:** isolated timing results for Crossrope (exit intent, "900%", no clean baseline), Social Media Examiner (timing not isolated), Klaviyo AI timing (no published results), Justuno Smart Timing ("Up to 40% More subscribers", no method), Neil Patel, and HubSpot lead flows.

## 4. Real estate (IDX lead capture)

All of these are forced-registration walls, not optional alerts.

- **Union Street Media** [V, snippet; page returned 403] https://unionstreetmedia.com/the-benefits-of-forced-registration-for-real-estate/ — registrations +425% when the wall came at the 1st detail view, +213% at the 3rd, +159% at the 5th; recommends the 1st. Lead quality not shown.
- **Real Geeks** [V] https://support.realgeeks.com/allow-lead-to-view-more-properties-before-registration — default is registration after one property; "requiring registration after one property view produces the highest conversion rates".
- **kvCORE / eXp** [V] https://support.expcloud.com/portal/en/kb/articles/force-lead-registration-website-setting — default "Prompt required registration after 1 property view".
- **BoomTown** [V] https://intercom.help/boomtown/en/articles/8451767-how-leads-use-the-website — two-step registration on the second property's full details, or on the fourth photo. Searching and browsing stay open.
- **Sierra Interactive** [V] https://help.sierrainteractive.com/helpcenter/global-site-settings-in-sierra-configuration-for-leads-permissions-and-compliance — PPC traffic: "Required with 0 views"; "Common example: Require on All Listings with 4 views."
- **IDX Broker guidance via IDXAddons/RealtyCandy** [V, third party, updated 12.5.2026] https://idxaddons.com/knowledge-base/idx-leads/request-or-force-registration — "Request registration after the 1st or 2nd Details Page view", force after the 7th or 8th, "Based on aggregated data and client feedback".
- **GeekEstate, Jeff Manson (10.9.2009)** [I-practitioner] https://geekestateblog.com/should-you-required-registration-or-not — forced vs optional: +35% conversion. First click vs after 4 views: the first click had "a 5% higher conversion rate". Lead quality not measured.
- **Zillow agent blog (22.1.2014)** [I, snippet; page returned 403] https://www.zillow.com/agents/force-search-registration-or-not — five views before asking was best for volume plus quality. Not verified on the page.
- **Counter-evidence: Huang et al., Information Systems Research 2021** [I] https://ideas.repec.org/a/inm/orisre/v32y2021i3p914-931.html
  - Design: Collage.com, about 75,000 new users, randomised: a request before shopping vs only at checkout.
  - Results: registration +58.08%, purchase likelihood +10.89%, orders +16.76%, long-run revenue +13.22%. No short-term conversion loss. The format of the request is not described.
  - → Asking early can work when it sits at a task boundary (before the user starts) and the visitor intends to transact.
- Summary: walls get the most volume at view 1, the soft "request" sits at views 1–2, and quality claims favour about 5 views. No published test of an optional alert popup in real estate was found.

## 5. Forum voices

- **HN 9625039, jgaxn (29.5.2015)** [I] https://news.ycombinator.com/item?id=9625039 — 73.5% (5 s) and 75.8% (10 s) "left the page without closing the popup". A scroll trigger reached "only 2.6% of users". → A deep-scroll trigger can reach almost no one; set thresholds from real scroll data.
- **HN 9624731 (29.5.2015)** https://news.ycombinator.com/item?id=9624731
  - gk1: a popup "on a delayed timer": 232 of 11,848 viewers signed up (1.96%).
  - probably_wrong: "piss off 98 people, sign up 2."
- **HN 7842457 (6.2014)** https://news.ycombinator.com/item?id=7842457
  - squeaky-clean: "It showed up before I was even a paragraph into the article."
  - davelocity: "time-delay, wait until 2nd article viewed".
- **HN 19120081, cmod, owner (10.2.2019)** https://news.ycombinator.com/item?id=19120081 — the popup "won't trigger until you're at the bottom of the screen" and is "insanely effective at converting folks".
- **Klaviyo Community** https://community.klaviyo.com/sign-up-forms-38/pop-up-timing-8937
  - Joseph Hsieh, Champion (2.8.2023): "some lift switching from scrolling percentage to a timed delay". Suggested 30 s against a 1-minute average visit.
- **Klaviyo Community** https://community.klaviyo.com/marketing-30/signup-form-popup-triggering-strategy-19517
  - marika-t (8.7.2026): "a timed popup can interrupt someone mid-evaluation".
- **Klaviyo Help, official counterpoint** [V] https://help.klaviyo.com/hc/en-us/articles/4413544555547
  - Quote: "visitors usually do not spend more than a few seconds on each page".
  - Quote, for crucial messages: "display the form immediately or after 1 or 2 seconds".
- **Shopify Community** https://community.shopify.com/t/whats-one-change-you-made-that-unexpectedly-increased-your-shopify-sales/661727
  - clickfromai (7.8.2026): "Removing the immediate email popup on mobile helped us more than expected."
  - Same poster: "Delay the popup until 30 seconds or the second page view."
- **Shopify Community** https://community.shopify.com/t/whats-your-strategy-for-getting-people-to-sign-up-for-your-email-list/555925
  - lumine (15.3.2026): "triggering it after someone has actually browsed a few products".
- **Shopify Community** https://community.shopify.com/t/raising-the-discount-from-10-to-20-dropped-signup-rates-in-our-client-data/666659
  - Binaery (30.8.2026; builds a competing app): "In practice timing moves opt-ins more than the percentage".
- **WordPress.org forums** and **ux.stackexchange.com:** no outcome reports found.

## What it means for our timing

1. Hitting a break is what matters, not the seconds on a timer: page change, end of a price table or chart, back to results, or a finished filter.
2. Require proof of engagement first: a 2nd page view or 2nd listing, or a finished section with about 20–30 s of active time.
3. Never show it on the first screen from Google, mid-scroll, while typing or while panning the map.
4. Make it about the area being viewed.
5. Measure leads that act later, not raw signups.
