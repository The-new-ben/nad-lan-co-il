# Price-update popup for nad-lan.co.il: what the evidence says

All sources were read on 8 November 2026. [V] means vendor data: self-reported and biased toward "popups work". [I] means independent: Google, W3C, NN/g, Baymard, academic papers, statute text, law firms, or a forum. Source IDs point to the list at the end.

Local context read first: the cro and form.md skills, marketing-psychology, the lead-magnet benchmarks and the PriceNudge README. The README says 25 s is "inside the 10 to 50 that the timing studies recommend". I found no study that recommends 10 to 50 s (see question 2).

---

## 1. Benchmarks

Vendors define "conversion" differently. Wisepops and Sleeknote report means, which outliers inflate. Popupsmart reports medians, counts only submissions with an email or phone, and tests significance, so it is the closest to our case.

| Dataset | Average or median | Top 10% | Mobile vs desktop | Real estate |
|---|---|---|---|---|
| Popupsmart 2026, 28,674 campaigns, 499.6M displays [V] S1 | median lead rate **0.83%** | **3.87%** | **1.02% vs 0.57%** (63% of displays are on mobile) | **Real Estate & Construction 0.69%** (70 campaigns) |
| Wisepops 2026, about 1B displays, email popups only [V] S2 | mean 4.82% | 57.7% (mean, skewed) | 4.98% vs 3.67%; top 10%: 59.19% vs 52.56% | not reported |
| Sleeknote 2026, 516.9M views [V] S3 | mean 4.23% | n/a | 5.60% vs 2.86% | n/a |
| Getsitecontrol 2026, "thousands" of popups, about 90% ecommerce [V] S4 | n/a | n/a | 6.57% vs 3.77% (signups) | n/a |
| Omnisend 2025, 1.24B displays [V] S5 | 2.1% | "3.5%+" | 2.2% (mobile-only) vs 1.4% (desktop-only) | n/a |
| Sumo, 1,754,957,675 popups (archived 2018) [V] S6 | 3.09% | 9.28% | n/a | n/a |

**By format:** Getsitecontrol modal vs slide-in 7.39% vs 4.20% (mobile), 4.44% vs 3.49% (desktop); internal test full screen 3.41%, modal 2.95%, sticky bar 2.30%, slide-in 2.17% [V] S4. Sleeknote centred 4.68%, slide-in 3.69%, sticky bar 2.85% [V] S3. Wisepops centre 6.84% vs bottom-centre 3.41% [V] S2. Klaviyo's quoted "full-screen 3.54%": not found on a Klaviyo primary page. Format by device for the top 10%: not found.

**By trigger:** Wisepops average scroll 5.37%, on load 4.72%, exit 3.94% (top 10%: scroll 26.6%, exit 19.2%) [V] S2. Omnisend time 2.9%, scroll 2.1%, exit 1.8% [V] S5. Sleeknote timer 4.42% vs scroll 2.64% [V] S3. Popupsmart delay 0.83% vs on load 0.61%, exit 1.10% vs 0.78%, both "lean" (not statistically reliable) [V] S1. Inactivity: no numbers found.

**Real estate:** only Popupsmart's 0.69% is measured. Wisepops' real-estate page shows a valuation A/B (address only 4.1%, address plus timing 5.6%, control 0.4%), undated and illustrative [V] S7.

## 2. Timing, mobile exit signals, frequency

**Delay:** Wisepops on load 4.16%, 1-5 s 5.93%, 6-10 s 5.98%, **11-15 s 6.45%**, 16-20 s 2.95%, **21-30 s 1.53%** [V] S2. Omnisend peaks at 6-10 s (2.4%) on a flat 1.8-2.4% curve [V] S5. Popupsmart: 0-5 s vs 21-60 s **"no measurable difference"** [V] S1. Sumo: "Of the top 10% of pop-ups, only 8% had pop-ups appear in the 0-4 second mark." [V] S6. So: never on arrival; past that, the only tested source says the seconds barely matter. Our 25 s is outside the 6-15 s "sweet spot" of the means-based vendors; test it against the 20% holdout.

**When people act** (Popupsmart [V] S1): 40.5% of displays end in an explicit close; **71% of closers close within 5 s; 61% of leads arrive within 30 s.** The headline, fields and button must all be visible in the first frame.

**Mobile exit signals:** vendors use fast scroll-up, the Back button and tab switching [V] S8 S9. Wisepops calls tab-return unhelpful (it fires on return, not on leaving) and inactivity "not very relevant", and says scroll-up must be tuned [V] S8. OptiMonk limits Back to the entry page; "some mobile browsers don't support every signal" [V] S9. No vendor publishes thresholds; our 1,200 px/s is our own choice.

**Frequency:** Popupsmart fatigue curve: 1st view 1.33%, 2nd 1.22%, falling from the 3rd to **0.41% at the 6th** [V] S1, so cap at two showings. Days to wait after a close: no measured study found; practitioners suggest 5 days (Klaviyo community) or 7-14 days (Shopify guide); a 90-day Klaviyo default is claimed, unverified [I-forum] S10.

## 3. Google's guidance (exact wording)

**Current document**, "Avoid intrusive interstitials and dialogs", last updated 2025-12-10 [I] S11:
- "Instead of full page interstitials, use banners that take up only a small fraction of the screen".
- "Don't obscure the entire page with interstitials."
- "Don't redirect the user to a separate page for their consent or input."
- "Mandatory interstitials are exempted" (for example age gates).
- "Intrusive dialogs and interstitials make it hard for Google ... to understand your content, which may lead to poor search performance."

**Original 2016 signal**, effective 10 January 2017 [I] S12. Penalised examples:
- "Showing a popup that covers the main content, either immediately after the user navigates to a page from the search results, **or while they are looking through the page**."
- "a standalone interstitial that the user has to dismiss before accessing the main content"
- an above-the-fold layout that looks like an interstitial.

Not affected, "used responsibly": cookie and age-verification interstitials; login dialogs on non-indexable content; "Banners that use a reasonable amount of screen space and are easily dismissible."

**Page experience** (updated 2026-09-22) [I] S13 still asks "Do your pages avoid using intrusive interstitials?", and adds: "Beyond Core Web Vitals, other page experience aspects don't directly help your website rank higher".

**Delayed and exit popups:** Mueller (2016) limited the signal to "the interaction between the search click and going through the page"; on popups shown when leaving: "So at the moment those wouldn't count" [I] S14. That was a hangout remark. The official text also lists a popup covering content "while they are looking through the page", so a delayed centred modal on a phone is still a listed example, while a small, easily dismissed bottom banner is the listed exception. A delayed close button would break "easily dismissible".

## 4. Form friction

- **Field count:** Popupsmart 1 field 0.88%, **2 fields 0.94%**, 3 fields 0.56% (the 1-2 vs 3 gap passed their tests); a name field had no measurable effect [V] S1. Omnisend flat at about 2.1% for 1-3 fields, 1.5% at 4 [V] S5. Sleeknote 4.41%, 2.90%, 1.93% [V] S3. Phone plus email is already two fields: add nothing else.
- **Phone:** University of Wisconsin-Extension, mandatory phone cut conversion **52%** (96% confidence, 24 h, 2014, one case) [V-Unbounce] S15. Popupsmart: phone 0.46% vs email-only 0.88%, a "lean"; the phone share of leads rose from 21.3% to 33.5% (2024-2026) [V] S1. Baymard (n=1,026): **14%** would never give a store their phone; unexplained required phone fields bring fake numbers or abandonment; 39% of sites do not explain; fix with a short inline reason [I] S16. HubSpot (40,000+ pages): pages "referring to telephone numbers or calling had lower conversion rates" [V] S17. Real-estate tools report fake numbers when phone is forced [V] S18.
- **Other:** Imagescape, 11 to 4 fields, **+160%** (before-after 2007/2008) [V] S19. Expedia: deleting an optional "Company" field was worth **$12M profit a year** (its VP, SAS conference) [I-press] S20.

**Two-step and multi-step:** Popupsmart **"no measurable difference"** once step-1 clicks without contact details are excluded [V] S1. Omnisend 2.3% vs 2.0% [V] S5; Wisepops 5.17% vs 4.62% [V] S2; Sleeknote: 76% of step-1 finishers finish step 2 [V] S3. OptinMonster Yes/No 2% to 20% and two-step 2.5% to 40%+, no samples disclosed [V] S21. Venture Harbour 0.96% to 8.1%, before-after, sells Leadformly [V] S22.

**Foot-in-the-door, primary:** Freedman & Fraser 1966, **76.0%** agreed to a large request after a similar small one (N=25) vs **16.7%** control (N=24); Experiment 1: 52.8% vs 22.2% (N=36) [I-academic] S23. Burger's 1999 review: conditional, smaller in general [I] S24.

## 5. Copy and design

- **Page context:** Wisepops URL targeting **5.53% vs 2.40%**, but geo targeting **3.48% vs 5.29%** without [V] S2. Take the area from the page, not from IP. One agency saw a city-name headline lower conversion [V] S25.
- **Urgency:** countdowns: Wisepops 12.84% vs 4.73% [V] S2, Omnisend 1.9% vs 2.1% [V] S5, so contradictory. No test of honest "prices are changing" framing found; claim it only where the data changed (the PriceNudge rule).
- **First person:** Unbounce/ContentVerve "my" 90% more clicks than "your" (2014, no sample); Wiebe replication +24% S26. Hebrew tests: not found.
- **Close:** Recart says delaying the X by 2-4 s lifts signups [V] S27, but that breaks Google's "easily dismissible" condition, so do not use it. Opt-out button popups: 8.05% vs 7.04% (response, not leads) [V] S4. NN/g: guilt-trip "manipulinks" offend; use a neutral decline [I] S28.
- **Social proof:** "Join 500,000…" moved above the copy: 1.65% to 1.71% [V] S29; Recart: clean popups win [V] S27.
- **Animation:** Recart: pulsing mostly lost, animated background lowered conversion [V] S30; Popupsmart's lift is observational, by their own account [V] S30. WCAG 2.2.2: blinking that "lasts more than five seconds" needs pause/stop/hide; "Certain groups ... find blinking content distracting" [I] S31. So the arrow moves once, under 5 s, and stays still under reduced motion.
- **Success state:** confirm it worked, name the next step and when, no dead end [I] S32.
- **NN/g:** "never show a popup before users can glean value"; "show only one at a time" [I] S33.

## 6. Practitioner forums

Reddit: not accessible to my tools (blocked to this crawler), none read. CXL: 403. GrowthHackers, WebmasterWorld: nothing relevant found.

- **Hacker News** (2023) S34: "popups that cover up the article I was trying to read"; on exit intent, "That's a much better way of doing it."; an owner: "Revenue is meaningfully better with the popup than without." 2025: "I will just close the tab" S35.
- **Indie Hackers** (search snippets; pages 403) S36: a popup got 80 signups from 80,000 views (0.1%) vs 430 (over 0.5%) for an embedded box of the same design; another owner found popups beat sidebars, and the offer mattered most.
- **Real estate:** GeekEstate 2008, citing IDX Inc. studies: quality leads rose "over 70%" when users could "view a minimum of 5 properties" first [V-reported] S37. Forced phone brings fake numbers S18.
- **SEO:** a Moz Q&A owner saw traffic decay weeks after adding a popup, cause unconfirmed S38.

Recurring advice: wait for engagement, one popup at a time, easy close, a specific offer, measure with a holdout.

## 7. Israeli law

**Section 30A(b), Communications Law** (primary text, Wikisource S39)
- No advertising message by fax, autodialer, "הודעה אלקטרונית" (electronic message) or SMS "בלא קבלת הסכמה מפורשת מראש של הנמען, בכתב, לרבות בהודעה אלקטרונית" (without the recipient's prior explicit consent, in writing, including by electronic message).
- Damages of up to **₪1,000 per message** without proof of harm (30A(j)).
- Every message must start with the word "פרסומת" (advertisement) and give the sender's name, contact details and a way to opt out (30A(e)).
- The purchase or negotiation exception in 30A(c) requires that the person was told at collection that their details would be used for advertising, plus a chance to refuse.
- Live human calls are outside 30A. They fall under the "אל תתקשר אליי" (Do Not Call) registry, Consumer Protection Law sections 16B-16C. Calling back someone who asked to be called back is allowed. A separate explicit consent is valid for at most one year, and the business carries the burden of proof (Kol Zchut, updated 9.9.2026) [I] S40.
- Whether WhatsApp counts as an "electronic message": my reading of the definition, not verified in case law.

**Checkbox or button wording:** a definitive ruling: **not found**. Courts accepted registration forms that contained explicit consent; whether terms-of-use acceptance alone suffices is argued in Kronenberg v. Getpackage (class action 32069-01-24), outcome unknown S41. The Privacy Protection Authority's final consent opinion (25.2.2026) requires active consent for direct mailing, "כגון לחיצה על רובריקה 'אני מסכים'" (such as clicking an "I agree" box), says "שתיקה או היעדר מחאה אינם מספיקים" (silence is not enough), and treats section 11 as the minimum (Shibolet S42); pre-ticked boxes "may be considered 'suspicious consent'" (Pearl Cohen S43). Cost: a mandatory consent checkbox lost 25.82% in one Getsitecontrol test [V] S4. Safe pattern: an unticked separate box, or a button whose own words state the consent; log the time, page and wording shown.

**Section 11, Privacy Protection Law, as amended in 2024** (Amendment 13, in force 14.8.2025; primary text S44). The request must state:
1. whether there is a legal duty to give the data, or it is voluntary, and what happens if the person refuses;
2. the purpose;
3. the controller's name and contact details;
4. to whom the data will be passed, and why (for example the developer or broker);
5. the rights of access (section 13) and correction (section 14).

---

## Sources (all read 8.11.2026)

- S1 https://popupsmart.com/our-data ; https://popupsmart.com/blog/popup-conversion-benchmark-report
- S2 https://wisepops.com/blog/popup-stats
- S3 https://sleeknote.com/blog/popup-statistics
- S4 https://getsitecontrol.com/blog/website-popup-timing/
- S5 https://www.omnisend.com/blog/email-popup-statistics/
- S6 https://web.archive.org/web/20180718215607/https://sumo.com/stories/pop-up-statistics
- S7 https://wisepops.com/industry/real-estate
- S8 https://wisepops.com/mobile-exit-intent
- S9 https://www.optimonk.com/features/mobile-triggers
- S10 https://community.klaviyo.com/marketing-30/is-there-a-way-to-have-a-pop-up-appear-only-one-time-during-a-site-visit-495 ; https://ninety9.dev/blog/popup-frequency-capping.html
- S11 https://developers.google.com/search/docs/appearance/avoid-intrusive-interstitials
- S12 https://developers.google.com/search/blog/2016/08/helping-users-easily-access-content-on
- S13 https://developers.google.com/search/docs/appearance/page-experience
- S14 https://www.seroundtable.com/google-interstitials-mobile-penalty-search-click-through-22857.html
- S15 https://unbounce.com/conversion-rate-optimization/psychology-of-choice-conversion-rates/
- S16 https://baymard.com/blog/explain-phone-number-field
- S17 https://blog.hubspot.com/blog/tabid/6307/bid/6748/3-form-fields-that-kill-landing-page-conversion-rates.aspx
- S18 https://support.expcloud.com/portal/kb/articles/can-you-force-leads-to-provide-phone-numbers (Zurple page now redirects; seen in search only)
- S19 https://imagescape.com/filer/canonical/1455648270/152
- S20 http://www.zdnet.com/expedia-on-how-one-extra-data-field-can-cost-12m-3040153863/ (via search)
- S21 https://optinmonster.com/case-study-how-chinaimportal-increased-webinar-registrations-18-using-yesno-optins ; https://optinmonster.com/how-wholesale-suite-gains-6500-leads-a-year-using-two-step-optins
- S22 https://ventureharbour.com/multi-step-lead-forms-get-300-conversions/
- S23 https://web.mit.edu/curhan/www/docs/Articles/15341_Readings/Influence_Compliance/Freedman_Fraser_Foot-in-the-door.pdf
- S24 https://www.slideshare.net/slideshow/burger/2497673
- S25 https://www.bmg360.com/blog/post/landing-page-localization-does-geo-personalization-work
- S26 https://sitetuners.com/blog/me-vs-you-how-pronouns-affect-click-conversion-rates/
- S27 https://recart.com/laboratory/postponed-close-button-test-2-second-delay ; https://recart.com/laboratory/weekly-subscriber-count-widget-email-test
- S28 https://www.nngroup.com/articles/shaming-users/
- S29 https://optinmonster.com/how-social-media-examiner-250000-subscribers-using-optinmonster-split-testing/
- S30 https://recart.com/laboratory/animated-popup-background-experiment ; https://community.popupsmart.com/t/display-effects-do-animations-affect-popup-conversion-data-from-17k-popup-campaigns/493
- S31 https://www.w3.org/WAI/WCAG22/Understanding/pause-stop-hide.html
- S32 https://city-of-austin.gitbook.io/digital-forms-guide/show-the-way-to-completion ; https://designsystem.gov.scot/patterns/form-submission-results-page
- S33 https://www.nngroup.com/articles/popups/
- S34 https://news.ycombinator.com/item?id=35684807
- S35 https://news.ycombinator.com/item?id=46449109
- S36 https://www.indiehackers.com/post/pop-ups-don-t-work-6e02727ddf ; https://www.indiehackers.com/post/would-you-use-a-popup-for-capturing-email-address-ce709dff88
- S37 https://geekestateblog.com/forced-registration-pros-and-cons
- S38 https://mozdev.nodebb.com/community/q/topic/63583/
- S39 https://he.wikisource.org/wiki/חוק_התקשורת_(בזק_ושידורים) (section 30A)
- S40 https://www.kolzchut.org.il/he/מאגר_אל_תתקשר_אליי
- S41 https://www.law.co.il/media/computer-law/kronenberg18.pdf (via search)
- S42 https://www.shibolet.com/גילוי-דעת-סופי-בנושא-הסכמה-מטעם-הרשות/
- S43 https://www.pearlcohen.com/israeli-privacy-regulator-issues-position-paper-on-valid-consent/
- S44 https://he.wikisource.org/wiki/חוק_הגנת_הפרטיות (section 11, amended 2024)
