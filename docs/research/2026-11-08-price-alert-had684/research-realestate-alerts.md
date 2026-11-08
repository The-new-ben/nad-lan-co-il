# How real-estate sites ask for price-alert / new-project sign-ups (teardown for nad-lan.co.il)

All sources read on 8 Nov 2026. Read-only research: no form was touched, no sign-up made.

**Status key**
- **V**: verified from the page text itself (help centre, app store listing, live page, press release).
- **S**: seen only in a search-engine summary of that page, because the page blocked direct fetching (Zillow, Realtor.com, Redfin and Zoopla help, Madlan, Yad2, Homeless all returned 403 or a bot wall).
- **U**: unverified or not found.

Quotes are kept short. Where a label isn't quoted, it's a paraphrase.

## 1. Global portals

| Site | Trigger | Format | Wording seen | Fields / account | Consent near form | After sign-up | Source | Status |
|---|---|---|---|---|---|---|---|---|
| Zillow | "Save" heart on a listing; saved search; "Claim" own home | U (no teardown found) | "tap or click Save"; notification center lets you tailor by "location, price, or saved homes" | Zillow account | U | Saved-search alerts daily or instant, on a new listing or a price reduction (2013). A claimed home gets a "home report email" on its Zestimate (frequency U). | zillow.com/learn/zillow-advanced-search ; inman.com/2013/08/26/alerts-let-agents-mine-zillow-for-potential-listings ; zillow.com/agent-resources/blog/make-instant-updates-to-zestimate/ | S |
| Redfin | Heart "Favorite" alerts on price drop, under contract and sold; "Claim home" signs you up for monthly Home Reports | App onboarding asks for push: "Turn on notifications" / "Not now" | 2012 search button "Email me new listings" | Account. Email must be verified to claim a home. Adding a phone number is optional, for text reminders. | U | Per-event "Update Types". Push within 15–30 min (2012 claim). | support.redfin.com/hc/en-us/articles/360001454951 ; …/360001432672-Home-Report ; design.lazyweb.com/canvas/flows/redfin/sign-in (capture Feb 2026) | S (push screen V) |
| Realtor.com | Saved search with price increase/decrease alerts. "My Home" claim-your-home dashboard relaunched 9 Jun 2026 (free; tracks the zip-code median listing price). | U | U | Account and claim | U | U | apps.apple.com/us/app/id336698281 ; prnewswire (My Home, Jun 2026) via search | S |
| Homes.com | Nothing found | | | | | | site 403 | U |
| Rightmove | Run a search, then the "create alert" button; heart saves a property (must be logged in) | Inline button on results | Frequency choices: "Instantly", "Daily", "Every 3 days", "Every 7 days" | Free My Rightmove account; alerts go to the account email | U | A listing marked "reduced today" goes into alerts. Agent help says a cut of 2% or more is re-sent in instant alerts. At most "14 new/reduced properties" in the email body. Up to 20 alerts. Track-my-property estimate refreshes monthly, with an email and/or push opt-in. | faq.rightmove.co.uk/…/7000048758 ; …/7000048780 ; customerfaq.rightmove.co.uk/…/7000098933 (modified 29 May 2026) ; …/7000082421 ; rightmove.freshdesk.com/…/7000090984 | V (2% rule S) |
| Rightmove New Homes | "Request Details" on a development listing | Enquiry form | Button: "Send enquiry" | "You must be signed in"; guest enquiries are not available. Three mandatory questions (timeframe, buyer status, affordability). Email verification. | U | The developer calls back to confirm a viewing. | customerfaq.rightmove.co.uk/…/7000098055 (modified 24 Apr 2026) | V |
| Zoopla | Saved search; bell icon sets frequency or "Never". Saved property: notified "when a saved property is reduced in price". MyHome tracks your own home. | U | U | Account needed to track | U | MyHome (Mar 2025): about 4M homeowners subscribed, 1.6M return monthly, push 3 times a month with value plus local stats, emails when a nearby home is listed or sold. | business.zoopla.co.uk/new-search-features-delivering-more-motivated-movers (19 Sep 2025) ; zoopla.co.uk/press/releases/over-4-million-homeowners-… ; help.zoopla.co.uk (S) | V/S |
| Idealista | App: save a search, then turn on instant notifications. Covers new listings "o che un immobile riduce il suo prezzo". | Push | "attiva le notifiche immediate" | Account | U | Instant push. In the 2009 web version, a link on each listing subscribed you to drops by daily email. | apps.apple.com/it/app/idealista/id465958311 ; idealista.com/news/node/53985 (2009) | V |
| Immobiliare.it | Saved search / saved listing | U | U | Registration needed for saved searches and automatic new-listing info | U | Price-drop alert U | immobiliare.it/terms/privacy/ (S) | S/U |
| realestate.com.au | Saved search; property profile for your own home | Push | "Save your favourite searches and be notified" | Member login | U | 3M properties owner-tracked (late 2023, S). Price alert U. | apps.apple.com/au/app/id404667893 ; onlinemarketplaces.com (3M) | V/S |
| Domain | Saved-search property alerts; shortlist push | Push and email | "Turn on property alerts to be notified…" | Account | U | Shortlist push on price change, sold, under offer and similar. Home Alerts include a "significant price change"; the threshold is "intentionally been kept un-disclosed". Daily or weekly. | apps.apple.com/app/id319908646 ; help.domain.com.au/…/360051786314 ; …/360016015433 | V/S |
| PropertyGuru | "Create Alert" / "Save Search", with frequency and an email-or-app choice (agent-written answer). Real-time price-change tracking exists only in the agent tool MarketWatch. | U | U | U | U | U | propertyguru.com.sg/property-investment-questions/how-do-i-create-alert-610247 (S) ; agentofferings.propertyguru.com.my/help-centre/all-about-marketwatch/ (S) | S |
| Bayut (UAE) | Project page "Register Interest" (header, description, payment plan) | Button (form not rendered in HTML) | "Express your interest in this project."; "Be the first to hear about new properties" / "Alert me of new properties"; "Save Search" | U | None visible beside the buttons | No price-change alert. (Bayut KSA app does offer alerts on price updates for saved properties, S.) | bayut.com/new-projects/uae/ ; bayut.com/for-sale/property/dubai/dubai-south/residential-district/cresswell-homes/ | V |
| Property Finder (UAE) | New-project page: "Download project brochure", "Inquire" per unit type, "WhatsApp" | Buttons | "Get in touch now for more information." Disclaimer: "Prices, availability, and purchase conditions may change frequently." | No form on the page; WhatsApp is the main channel | Footer links only | No price alert. Saved-search push in the app (S). | propertyfinder.ae/en/new-projects/emaar-properties/valia-tower ; …/eome ; apps.apple.com/sa/app/apple-store/id897540233 | V |

## 2. Israel

| Site | Trigger | Format | Wording seen | Fields | Consent wording | After | Source | Status |
|---|---|---|---|---|---|---|---|---|
| Yad2 | Create alert; heart; searches saved automatically | App and email | "יצירת התראות וסימון מודעות אהובות" ; email alerts "לפי תדירות משתנה" (daily, or fast up to 15 min) | Account | U | Email alert. A price-drop alert was not found. Third-party Chrome extensions (Price Agent, Pricey) add price history to Yad2 listings, which signals unmet demand. | apps.apple.com/il/app/…/id406318295 (v16.3.0) ; chromewebstore.google.com/detail/…/oaonnmffbhimnbgnmhippgkiabgahcln | V (site behind Radware wall) |
| Yad2 Yad1 (new projects) | Project page form | Inline | "השאירו פרטים ונחזור אליכם בהקדם" ; "למידע נוסף ותיאום סיור בנכס" | U | U | Callback | yad2.co.il/yad1/project/15258 (S) | S |
| Madlan | "יצירת התראה" item in for-sale navigation; project-page lead form | U | "השאירו פרטים" ; "מעוניינים לקבל פרטים על פרויקטים נוספים באיזור?" | U | U | The app description doesn't mention alerts; v1.4 "added apple sign in". | madlan.co.il/projects/… (S, 403) ; apps.apple.com/app/id6472173076 | S |
| Homeless | Nothing found | | | | | | 403 | U |
| nadlan.gov.il | No sign-up found (JavaScript app, only the title rendered) | | | | | | nadlan.gov.il | U |
| Azorim | No popup. Contact block at the page foot, reached by the header link "ליצירת קשר" | Inline | "מתלבטים בין כמה פרויקטים? נשמח לעזור" ; button "שלח >" | Project dropdown "בחר\י פרויקט"; name/phone/email labels not rendered (U) | "אני מאשר/ת קבלת פרסומים, עדכונים ומבצעים מחברת אזורים ושותפתיה העסקיים" | "הפרטים התקבלו בהצלחה, תודה." Project page has floor-plan PDFs, no price list. | azorim.co.il/projects/ ; azorim.co.il/projects/exchange/ | V |
| Y.H. Dimri | No popup. Inline form on home and project pages. | Inline | "השאירו את מספר הטלפון שלכם ונציג מטעמנו ייצור איתכם קשר" ; project page: "רוצים לדעת עוד?" plus "החל מ" 1,750,000 | First name, last name, phone, email and project, all required | Marketing: "אני מאשר/ת קבלת הטבות, עדכונים ומידע שיווקי מקבוצת דמרי" (email, SMS, WhatsApp). Second statement: consent to pass the data to Dimri. Notice: "ידוע לי כי איני מחויב/ת למסור מידע זה על פי חוק" | "הטופס נשלח בהצלחה!" | dimri.co.il ; dimri.co.il/project/harmony | V |
| Tidhar | Inline form, topic picker | Inline | "נשמח לשמוע מכם" ; "בחרו את נושא הפניה, השאירו פרטים" | Full name, phone and email required; message optional | "אני מאשר/ת כי קראתי את מדיניות הפרטיות ומסכים לתנאיה" ; "אני מאשרת קבלת פניות שיווקיות" (even if the visitor is on the do-not-call registry) ; "חלק מהשיחות מוקלטות" | U | tidhar.co.il | V |
| Rotshtein | Promotional popup with no form, plus an award-image popup; floating CTA | Modal and floating button | "יש לכם יופי של טיימינג!" → "כל הפרטים כאן" (landing page) ; "לחצו לקביעת פגישת ייעוץ" | None in the popup | Footer links only | Popup timing U | rotshtein.co.il | V |
| Ashtrom / Ashtrom Megurim | No form or popup in the fetched home pages | | | | | | ashtrom.co.il ; ashtromegurim.co.il | U |
| Africa Israel Residences | Same form on its Yad1 project pages | | "השאירו פרטים ונחזור אליכם בהקדם" | U | U | | yad2.co.il/yad1/project/16141 (S) | S |
| Gindi / Electra | Gindi: TLS certificate expired on fetch. Electra: domain not found. | | | | | | | U |

Market context: from January to May 2026, about 1 in 5 Yad2 resale listings cut their asking price, by 4.2% on average (Haifa 22% of listings, Tel Aviv 13.9%). Source: mako.co.il/finances-real-estate/Article-c3482c03ef5be91026.htm (12 Jun 2026), V.

## 3. Published tests and benchmarks

No published A/B test of a price-alert popup on a real-estate site was found. The closest evidence:

| Study | What was tested | Result | URL | Status |
|---|---|---|---|---|
| Locations Hawaii (VWO) | Listing-page CTA changed from "Inquire" to "Contact Agent" and moved higher | +22.97% inquiries; 37,000 visitors over 26 days; confidence not reported | wingify.com/success-stories/locations-hawaii | V |
| Woodside Communities (OptinMonster), a gated-community developer | Lightbox 5 s after landing on the "planning a visit" page | Converts 3.57% of visitors; April leads 46 (2017) vs 242 (2018), 116 of them from the popup. The vendor's own headline figures (426% vs 476%) don't match each other. | optinmonster.com/case-study-woodside-increased-revenue-294435-two-months | V |
| Union Street Media | Forced registration after the 1st property-detail view | +425% registrations (lead quality not shown) | unionstreetmedia.com/the-benefits-of-forced-registration-for-real-estate/ | S |
| Point2 via Search Engine Watch | Registration-gated leads, 100,000 sites over 3.5 years | Effectiveness reportedly fell about 80% | searchenginewatch.com/?p=31050 | S |
| IDX Broker guidance | Request registration after 1–2 detail views, force it after 7–8 | Vendor advice; data not published | idxaddons.com/knowledge-base/idx-leads/request-or-force-registration | S |
| Omnisend benchmark (9 Feb 2026), 1.24B popup displays | Delay, fields, trigger, device | Average 2.1%. Best delay 6–10 s (2.4%) vs 0–1 s (1.9%). Exit intent 1.8%. 1–3 fields 2.1–2.2%; 4 fields 1.5%; 5+ fields 1.4%. Multi-step 2.3% vs single 2.0%. Desktop-only 1.4%. The article's chart captions contradict some of these figures. | omnisend.com/blog/email-popup-statistics/ | V |
| Unbounce | Real-estate landing pages | Median 2.2% | unbounce.com/industry/real-estate/ | S |
| Baymard (survey of 1,026 US adults) | Forced account creation | 18–19% of checkout abandoners cite it | baymard.com/blog/reduce-cart-abandonment | S |

**UX and SEO guidance**
- Nielsen Norman Group ("Popups: 10 Problematic Trends", Kaley, 2019): "never show a popup before users can glean value". Ask for an email only after engagement, and offer something tangible in return. nngroup.com/articles/popups/ (V)
- Google Search Central: intrusive dialogs make content hard for search engines to understand. Banners that take a small part of the screen are acceptable; don't cover the whole page. developers.google.com/search/docs/appearance/avoid-intrusive-interstitials (V)

**Israeli legal context (not legal advice)**
- Communications Law section 30A requires prior consent before sending advertising by email or SMS, with statutory damages of up to ₪1,000 per message. chamber.org.il/serviceslobby/legal/74023/115485/ (S)
- The developers above all use a separate marketing statement plus a "not obliged by law" notice. Counsel should confirm whether a price alert counts as advertising.

## 4. Findings that matter for the nad-lan popup

1. **Alerts are attached to an object, not pushed at visitors.** Every global portal ties the alert to a heart, a saved search or "claim my home". None found uses a cold "prices are changing" modal.
2. **Global alert products ask for email only (through an account).** No phone, apart from Redfin's optional text reminder. Asking for phone and email together, both required, matches Israeli developer sales forms (Dimri asks for 5 required fields), not alert products. Omnisend's data shows conversion dropping at 4+ fields.
3. **Frequency control is standard.** Rightmove offers 4 options, Yad2 daily or 15 minutes, Domain daily or weekly. Only Rightmove publishes its price-cut trigger (2%). Domain hides its threshold on purpose.
4. **New-project flows on the portals are sales leads, not alerts.** Bayut has "Register Interest", Property Finder has WhatsApp, "Inquire" and a brochure, and Rightmove has a signed-in enquiry with buyer-profile questions. None offers "tell me when this project's price list changes".
5. **No Israeli site found offers a price-change alert** on a listing, a project or an area. Developers run static callback forms; Rotshtein runs a promotional popup with no form.
6. **No popup shows the evidence.** None of the prompts found shows the actual change (for example, how many nearby listings cut their price and by how much). The Yad2 data shows those changes are real and frequent.
7. **WhatsApp is used for agent contact (Property Finder) and named in marketing consent (Dimri).** Using it as an alert channel was not found anywhere.
