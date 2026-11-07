# World AI real-estate assistants, 2025-2026: what they actually do

Research for the nad-lan.co.il AI real-estate advisor. Web research only (WebSearch standard mode + WebFetch), no paid APIs, no DataForSEO.

- Research date: 7.11.2026. All sources were retrieved on 7.11.2026 between 18:53 and 19:06 Israel time (IST, UTC+2). Per-source times below are approximate (±5 min).
- Evidence rule: a feature or number is written only if it was read on a fetched page or in a search-engine excerpt of the named page. Where only an excerpt was seen (page itself blocked), the line says "excerpt only". Anything not found says "not verified".
- Almost every metric below is **company-reported** (press releases, vendor pages). None is independently audited.
- Several primary pages refused automated fetch (HTTP 403): zillow.com/news and zillow.com/tech pages, inman.com, businesswire.com, openai.com, madlan.co.il (Cloudflare challenge, not bypassed). Facts from those pages are marked "excerpt only".

---

## Quick matrix (consumer-facing assistants)

| Product | Search by chat | Listing Q&A | Area Q&A | Affordability | Valuation talk | Offer help | Tour booking | Human handoff | Fair-housing guardrail stated |
|---|---|---|---|---|---|---|---|---|---|
| Zillow AI mode (beta, Mar 2026) | yes | yes | yes | yes (BuyAbility) | yes (Zestimate history, user can challenge it) | yes (offer competitiveness, suggested fair offer price) | yes, in-flow | local agent | yes, classifier on input and output |
| Zillow in ChatGPT / Claude | yes | partial | yes | yes | estimates shown (Claude) | no | sends to Zillow | sends to Zillow | yes (neighbourhood text screened, excerpt only) |
| Ask Redfin (2024) | no | yes | yes | not stated | refers to agent | refers to agent | yes (8% ask) | licensed agent | yes, refuses |
| Redfin conversational search (Nov 2025) + ChatGPT app (Feb 2026) | yes | follow-ups | yes (commute, schools) | not stated | no | no | yes / via Redfin | Redfin agent | not stated |
| Realtor.com RealAssist AI (Jun 2026) + ChatGPT app (Mar 2026) | yes | yes | yes (commute, schools) | yes (income/expenses) | not stated | pitched as covering offers | yes, in-flow | local agent at every step | yes, real-time guardrails (no detail) |
| Homes.com Homes AI (Feb 2026) | yes, voice + text | yes | yes (data inputs) | not stated | not stated | finds agent at offer stage | not stated | listing agent ("Your Listing, Your Lead") | claimed in coverage, no technical detail |
| Rightmove "Ask Rightmove" (2026) | yes | yes (listing pages) | yes (Google Maps data) | not stated | no | no | no | about 2x leads to agents | not stated |
| Zoopla (AI search tests + ChatGPT app) | yes | not stated | not stated | not stated | not stated | no | no | pre-nurtured leads | not stated |
| idealista ChatGPT app (Mar 2026) | yes | summaries | no | no | no | no | no | not stated | not stated |
| realestate.com.au AI Assistant / AI Search / realAssist | yes | yes | yes (commute) | yes | yes (realAssist explains realEstimate) | no | enquiry/inspection in-flow | to agent enquiry | not stated |
| ImmoScout24 HeyImmo (Oct 2025) | yes | not stated | not stated | financing calc | market price help | no | no | not stated | not stated |

---

## 1. Zillow (USA)

Zillow has four AI surfaces: natural-language search inside its own apps (2023), the Zillow app inside ChatGPT (6.10.2025), "AI mode" inside Zillow (beta, 25.3.2026), and a Zillow connector for Claude (20.10.2026). Its guardrail is the open-source Fair Housing Classifier (May 2024).

**Jobs**
- AI mode (press release 25.3.2026): conversational search; affordability questions (including BuyAbility, and a renter asking whether they can afford a unit for a June move); compares listings and explains trade-offs, including units within one building; estimates renovation or repair cost from local data; interprets listing events such as price cuts and what they mean for offer strategy; explains how comps and market signals set list price and whether a home looks priced to sell fast; analyses offer competitiveness (the example is a $500k offer with waived contingencies) and suggests a fair offer price; rent-vs-buy for a one-year horizon; neighbourhood insights (amenities, shops, parks); summarises rental policies such as pets; explains and tracks a home's Zestimate over time and lets the user challenge it in real time; schedules tours and lets renters apply inside the flow; connects to a local agent; helps the user prepare for the conversation with the agent or property manager.
- Memory: adapts to activity and remembers preferences across sessions.
- ChatGPT app (6.10.2025): natural questions ("what can I afford", rentals in a city); listings with photos, maps, prices; rentals and for-sale listings by agents and owners. New construction and 3D tours were "planned", not live, at launch.
- Claude connector (20.10.2026): search for sale or rent by location, price and features; listing photos, prices, interactive maps, home value estimates, affordability tools; request tours, contact agents, explore financing.

**Presentation**
- AI mode is a mode inside Zillow's own app and site, pitched as a new way to use Zillow. The press release does not say exactly where the entry point sits. Beta for a limited group, expansion through 2026.
- In ChatGPT the app mirrors Zillow's own visual design and ranks results in Zillow's own order (onlinemarketplaces).
- Zillow's own natural-language search dates from January 2023 (search excerpt); its exact placement was not verified.

**Guardrails and disclaimers**
- AI mode includes the Fair Housing Classifier as a real-time guardrail that evaluates both the user's question and the AI's answer to prevent discriminatory steering (press release).
- AI mode supports but does not replace licensed expertise; Zillow says it runs as a licensed brokerage within industry rules (press release).
- ChatGPT app: listing displays keep broker and MLS attribution; Zillow says it does not send MLS listing data to OpenAI / Anthropic (realestatenews, two articles).
- ChatGPT app: Zillow says every ChatGPT-generated neighbourhood description is run through the Fair Housing Classifier before it is shown (excerpt only, zillow.com page blocked). A search excerpt also says non-compliant queries get an explanation of the fair-housing issue plus a suggested rephrase (excerpt only, not verified on the page).
- Fair Housing Classifier (GitHub repo zillow/fair-housing-guardrail): a stop list plus a fine-tuned BERT-base binary classifier (compliant / non-compliant, 0.5 threshold) and a RoBERTa-large multi-class model naming the category (for example age, disability). Trained mainly on steering risk. It only labels; the developer decides how to respond. The README recommends pairing it with a fair-housing-specific system prompt and says it is informational, not legal advice. The trained model and dataset are by email request only.
- History: in June 2023 OpenAI deactivated real-estate ChatGPT plugins, including Zillow's and Redfin's, over Fair Housing Act concerns (onlinemarketplaces). Zillow built the classifier after that.
- Industry pushback on the ChatGPT app was about MLS / IDX licensing, not fair housing: whether a chatbot display is under the broker's "actual and apparent control", whether brokers consented, and a test that produced a downloadable CSV/JSON of 100 listings (realestatenews 22.10.2025).

**Handoff**
- ChatGPT and Claude: discovery happens in the chat; the user is sent into Zillow to book a tour, contact a Zillow-affiliated agent, or explore financing. No transaction inside ChatGPT.
- AI mode: tours and agent connection happen inside the mode.

**Metrics found**
- AI mode early testing: users mostly ask about affordability, neighbourhood insights and comparing homes by feature (no percentages given).
- No usage numbers found for the ChatGPT app or the Claude connector.

**Sources**
- https://zillow.mediaroom.com/2026-03-25-Zillow-debuts-AI-mode,-bringing-guided-intelligence-to-every-step-of-the-housing-journey (≈18:59) — quote: "helping people move from discovery to keys in hand" (CEO Jeremy Wacksman)
- https://www.onlinemarketplaces.com/articles/zillow-puts-its-ai-promises-to-the-test-with-new-conversational-tool/ (≈18:58)
- https://zillow.mediaroom.com/2025-10-06-Zillow-debuts-the-only-real-estate-app-in-ChatGPT (≈19:04)
- https://www.housingwire.com/articles/zillow-chatgpt-launch-app-integration/ (≈18:55)
- https://www.onlinemarketplaces.com/articles/zillow-collaborates-with-openai-for-seamless-home-search-on-chatgpt/ (≈19:03)
- https://www.realestatenews.com/2026/10/20/zillows-home-search-tools-now-available-in-claude (≈18:55)
- https://www.realestatenews.com/2025/10/22/zillows-chatgpt-integration-forces-industry-reckoning (≈19:04)
- https://github.com/zillow/fair-housing-guardrail (≈19:03)
- https://zillow.mediaroom.com/2024-05-21-Zillow-providing-open-source-technology-to-promote-fair-housing-in-AI-powered-real-estate-conversations (search excerpt, ≈18:56)
- https://www.zillowgroup.com/news/zillow-in-chatgpt-fair-housing → redirects to zillow.com, HTTP 403 (excerpt only, ≈18:55 and ≈19:02)
- https://onlinemarketplaces.com/articles/openai-deactivates-all-real-estate-plugins (search excerpt, ≈19:02)

---

## 2. Redfin (USA)

Three generations: Ask Redfin (listing-page assistant, beta 7.3.2024, nationwide 2.5.2024), conversational search built with Sierra (13.11.2025), Redfin app in ChatGPT (6.2.2026).

**Jobs**
- Ask Redfin: answers questions about a for-sale listing: open house times, HOA fees, school districts, features, local prices, zoning (for example whether an ADU is allowed), nearby amenities, touring availability. Draws on the listing page and beyond.
- Conversational search: describe the home in your own words, refine by dialogue, comment on a suggested home ("more modern kitchen"), follow-ups on commute time or school proximity, "more like this but one more bedroom", and it suggests neighbourhoods outside the user's usual map. When nothing matches it says so and suggests widening the radius or dropping filters (the example: $300k, 3+ bedrooms, Baltimore County).
- ChatGPT app: listings updated from the MLS with photos, maps, prices; follow-ups on neighbourhoods, commute, past price changes without re-entering filters.

**Presentation**
- Ask Redfin: appears automatically on listing pages in the iPhone app (first in 12 metros, then all US), opt-in via "Try Ask Redfin".
- Conversational search: not a separate page. It is built into the existing search bar on the homepage, map and listing pages; clicking the search bar invites a description. Multilingual. iOS "Find Homes" bar.
- Sierra frames it as "The conversation is the interface."

**Guardrails**
- Ask Redfin: Redfin wrote detailed instructions so answers follow fair-housing guidelines; on a potential fair-housing issue it "appropriately says that it can't answer the question"; Redfin says it monitors this.
- Conversational search and ChatGPT app: no guardrail described in the releases (only the generic site footer about the Fair Housing Act).
- Honest "no match" answer instead of stretching results (a quality guardrail).

**Handoff**
- Ask Redfin is wired to Redfin's support team. Questions beyond the listing (how to make an offer, an agent's opinion of market value) go to a licensed agent.
- ChatGPT app: tour, Redfin agent or financing "handled seamlessly through Redfin".

**Metrics found**
- Ask Redfin, about two months after launch: 59% of questions are about the property being viewed; nearly 1 in 10 users who open it do so to request an agent; 8% request a tour; 93% return to the app within a week and use it near-daily.
- Conversational search (early): users view nearly twice as many listings and are 47% more likely to request tours or other services than standard-search users.

**Sources**
- https://www.redfin.com/news/introducing-ask-redfin/ (≈18:57)
- https://redfin.com/news/ask-redfin-launches-nationwide (≈18:57) — quote: says "it can't answer the question" on fair-housing issues
- https://www.redfin.com/news/redfin-debuts-conversational-search-to-reinvent-how-people-find-homes/ (≈18:56)
- https://sierra.ai/blog/ai-agents-in-action-redfin (≈18:56)
- https://www.redfin.com/news/redfin-debuts-its-home-search-app-in-chatgpt/ (≈18:58)

---

## 3. Compass (USA)

Compass AI is agent-facing, not consumer-facing. Launched September 2023 (marketing content and client communications), next phase June 2025 (voice prompts, proactive follow-up recommendations), AI Assistant across the "Home Platform" on 21.7.2026.

**Jobs (for agents)**: turns plain-language requests into platform actions; daily briefings; "Likely to Sell" opportunities with drafted outreach; updates client records, drafts follow-up emails, creates saved searches for clients, manages transactions, flags anniversaries and birthdays, schedules reminders.
**Presentation**: conversational layer across the agent platform. Company-owned brands in 2026, franchisees in 2027.
**Guardrails / metrics**: none stated in the July 2026 coverage.
**Consumer side**: Compass One (3.2.2025) is a client dashboard, not an AI assistant.
**Why it matters for us**: the "assistant that drafts the next action for a human" pattern (briefing plus drafted outreach) is the agent-side twin of a consumer advisor.

**Sources**
- https://www.rismedia.com/2026/07/21/compass-expands-ai-capabilities-ai-assistant-home-platform/ (≈19:05) — quote: "Technology should understand how agents work." (CTO Shay Artzi)
- https://www.inman.com/2025/06/17/compass-ai-is-poised-to-bring-agents-massive-productivity-gains/ (search excerpt, ≈18:54)
- https://www.nasdaq.com/press-release/compass-launches-compass-one-industrys-first-ever-all-one-client-dashboard-connecting (search excerpt, ≈18:54)

---

## 4. Realtor.com (USA)

Realtor.com app in ChatGPT (30.3.2026) and RealAssist AI on its own site, built with Google Gemini (beta 2.6.2026).

**Jobs**
- ChatGPT app: "pre-search" for first-time buyers: prompts that turn vague questions into search criteria, an affordability calculator from savings and income, neighbourhood comparison by commute, amenities and school boundaries, rent vs buy.
- RealAssist AI: plain-language affordability breakdown from income and expenses; side-by-side comparison of homes or neighbourhoods; commute-based search and mapping a daily route to school or work; visuals of a property at night, in winter or with a proposed exterior finish; tour scheduling inside the experience; pitched as covering the journey from research through touring, offers and closing.
- Memory: keeps budget and priorities across sessions, resumes a conversation after a day or two, cross-device.

**Presentation**: own conversational experience for logged-in beta users on desktop, app and mobile web, with suggested "Ask RealAssist AI" prompts. A secondary source says banners open a chat box (not verified on the primary page).

**Guardrails**
- RealAssist "built with real-time guardrails intended to promote compliance with Fair Housing standards" and to protect MLS data integrity (no technical detail).
- ChatGPT app: only a preview of images and details in ChatGPT; strict prohibition on model training with MLS data; no IDX feed, direct MLS relationships.
- Positioning: the tool does not replace the agent.

**Handoff**: ChatGPT app sends users to Realtor.com to connect with a local professional, book tours and use full search. RealAssist offers a local agent at every step; lead routing not described.

**Metrics found**: only a Realtor.com survey (October 2025): 82% of Americans use AI for housing-market information, and agents are rated the most trusted source. No usage metrics for either product.

**Sources**
- https://www.googlecloudpresscorner.com/2026-06-02-Realtor-com-R-Launches-RealAssist-TM-AI-A-Completely-Reimagined-Way-to-Find-A-Home (≈19:00)
- https://www.housingwire.com/articles/realtor-com-launches-realassistai-powered-by-google/ (≈19:00) — quote: "RealAssist AI removes the uncertainty and builds confidence at every step." (Mickey Neuberger)
- https://ycharts.com/news/story/PRN-LA11192-20260330 (Realtor.com ChatGPT app release, ≈19:00)

---

## 5. Homes.com / CoStar (USA)

Homes AI, launched 17.2.2026, open to all consumers, built on Microsoft Azure OpenAI. CoStar says it will extend it to Apartments.com (Apartments.com AI announced 16.6.2026), LoopNet, Land.com and others, and an owned Australian portal (Domain) is named by commentators only.

**Jobs**: search, refine and explore homes in real-time two-way voice or text; draws on Homes.com property data, Matterport 3D digital twins, images, proprietary school data, neighbourhood insights, market intelligence; filters out listings the user dislikes from open-ended requests. Planned (not committed): better memory, natural-light and grocery-proximity data.

**Presentation**: speech-to-speech, blended into the site rather than a separate chatbot, aware of what the user is viewing (for example the photo gallery), works alongside mouse and keyboard; users will be able to control how chatty it is. A secondary source says it shows which filters were applied (not verified, page blocked).

**Guardrails**: data stays inside Homes.com and is never used to train external models; it declines off-topic requests. Fair-housing guardrails are asserted in some coverage but the press release and the team interview give no detail (not verified).

**Handoff**: CoStar's "Your Listing, Your Lead" commitment: buyer and renter inquiries go directly to the listing agent. At offer stage the AI should help find a local agent. Agents may be able to train it before clients use it.

**Metrics found**: none on usage. Team claims fifty languages (only five demoed).

**Sources**
- https://www.rismedia.com/2026/02/17/costar-launches-ai-experience-refining-future-home-shopping/ (≈19:01)
- https://www.onlinemarketplaces.com/articles/the-new-industry-leader-in-ai-home-search-in-conversation-with-the-team-behind-homes-ai/ (≈19:05) — quote: "We have controls in there to make sure it doesn't go off the rails."
- https://www.businesswire.com/news/home/20260217810823/en/ (HTTP 403, ≈19:00)

---

## 6. Rightmove (UK)

"Ask Rightmove", built with Google Gemini, rolled out in phases to a subset of users: conversational search via a "Use AI" button in the homepage search bar (beta, about February 2026, date inferred), then answers on individual listing pages, then a Comparison Assistant inside search results (around late October 2026, date inferred from neighbouring releases). Also a Rightmove app in ChatGPT, launched as an experiment.

**Jobs**
- Search in your own words (examples: green space and commutable to a city; solar panels within 10 minutes of a station) returning a shortlist of live listings.
- Listing pages: instant answers about a specific home (nearby supermarkets, room for two cars on the drive) combining the listing, area and market data, plus Google Maps geospatial data.
- Comparison Assistant: compare several homes side by side and add your own comparison rows (supermarkets, hybrid-work suitability, schools, transport), drawing on agent listing data, Rightmove data, Google Maps, Experian (schools) and Land Registry.
- ChatGPT app: "@Rightmove" in a prompt, a carousel of live listings, sale and rent including new homes.

**Presentation**: a chat window that sits next to, not instead of, the normal search; then embedded in listing pages and in results pages.

**Guardrails**: none stated in the three releases.

**Handoff**: positioned as sending "more informed and confident" buyers to agents and developers. ChatGPT app is a "stepping stone": full details, filters and agent contact only on Rightmove.

**Metrics found** (assistant users vs non-users, "period to 30 June", year not stated, most likely 2026): 40% longer time on Rightmove, more than twice as many saved properties, around twice as many leads sent to agents.

**Sources**
- https://www.rightmove.co.uk/press-centre/?p=4791 (conversational search beta, ≈19:01) — quote: "describing, searching and refining in their own words"
- https://www.rightmove.co.uk/press-centre/?p=5125 (listing pages, ≈19:01)
- https://www.rightmove.co.uk/press-centre/?p=5309 (Comparison Assistant and the metrics, ≈19:01)
- https://www.rightmove.co.uk/press-centre/?p=4863 (ChatGPT app, ≈19:06)

## 7. Zoopla (UK)

**Jobs / presentation**: an AI-powered search experience tested in the Zoopla app for about 18 months; all listings available in a Zoopla app inside ChatGPT; earlier "Homes for You" AI recommendations (2024) and smart tags; enterprise agreement with OpenAI (24.4.2026); consumer slogan "Just Ask Zoopla" (search excerpt). Zoopla says AI platforms are still a small share of property-search traffic.
**Guardrails**: only a stated aim to scale AI tools safely. Not verified beyond that.
**Handoff**: AI is meant to produce pre-nurtured buyer leads for agents and to turn 6 million future sellers into high-intent leads. Mechanics not described.
**Metrics found**: early test results of AI search in the Zoopla app: +80% listing views, +150% leads.
**Sources**
- https://business.develop.zoopla.co.uk/zoopla-signs-enterprise-agreement-with-open-ai (≈19:02) — quote: "AI will have the greatest benefit for the UK property market." (CEO Paul Whitehead)
- https://propertyindustryeye.com/zoopla-bets-big-on-ai-in-landmark-openai-deal (search excerpt, ≈19:01)

---

## 8. Idealista (Spain, Portugal, Italy)

**Jobs**: idealista app inside ChatGPT (13.3.2026): search homes, rooms, garages, commercial premises and land in everyday language; photos, prices, descriptions, map view; ask ChatGPT to compare results or summarise a listing.
**Presentation**: only inside ChatGPT (free app connection). No on-site conversational assistant found (not verified either way).
**Guardrails / handoff / metrics**: none stated. Contacting the advertiser is not described.
**Sources**
- https://www.idealista.com/en/news/node/887103 (≈19:02) — quote: "designed to feel like a natural conversation"

---

## 9. REA Group / realestate.com.au and Domain (Australia)

**Jobs**
- Natural-language AI search: moved from a 12-month pilot to all property seekers (late 2025).
- realAssist (3.12.2025, OpenAI-powered): helps owners understand their realEstimate valuation, why it changed, and what to do next; logged-in members who track a property only. Note: Realtor.com's "RealAssist" and REA's "realAssist" are separate products (the shared News Corp ownership link is background knowledge, not verified in this pass).
- ChatGPT app (February 2026): map-based results inside ChatGPT for logged-in users in Australia.
- AI Assistant (rolled out to members across iOS, Android, web, August 2026): chat answers, discovery, affordability, evaluating and comparing homes, then an enquiry or inspection inside the same conversation (itbrief). Part of "NextGen Now" (AI Assistant, AI Search, Campaign Assist for agents, iGUIDE tours, walkthrough reels).
**Presentation**: chat interface for AI Assistant; AI Search is a conversational layer on top of filters, REA says "a partner, not a replacement, for search filters".
**Guardrails**: none stated in the articles read. Valuation disclaimers for realAssist not stated in the article (not verified).
**Handoff**: enquiry or inspection from inside the conversation; REA tells agents to write listings detailed enough for conversational search to read.
**Metrics found (AI search sessions, Aug 2026)**: 59% start wide (lifestyle or commute before suburbs); 32% include a commute or travel radius; 18% specify an exact travel time; 40% ask about architectural style, condition or renovation potential; 72% adjust their search at least once during the conversation.
**Domain**: CoStar completed its acquisition of Domain in August 2025. No Domain-branded AI assistant launch was found (not verified).
**Sources**
- https://itbrief.com.au/story/realestate-com-au-launches-ai-property-search-suite (≈19:02) — quote: "speak the same language buyers are using in their search" (Jonathan Swift)
- https://www.realestatebusiness.com.au/industry/32322-rea-bets-on-ai-assistance-to-bolster-property-search (≈19:05)
- https://onlinemarketplaces.com/articles/rea-group-partners-with-openai-for-improved-property-valuations-experience/ (≈19:02)
- https://itbrief.com.au/story/realestate-com-au-launches-chatgpt-app-for-homebuyers (search excerpt, ≈19:01)

---

## 10. Opendoor (USA)

Not a consumer chat advisor. AI is used internally for pricing and assessment, plus an agent app.
- Key Agent app (15.7.2025): agents collect home details room by room with inline questions and photos, offline capable; data refines valuation and repair-estimate models; human annotation teams work alongside the models; cash offer in as little as two days.
- 2026 "AI-native" pivot: secondary sources claim AI pricing upgrades, smartphone video inspections and assessments in about 10 minutes (Zacks, Mammoth Times). Not verified on an Opendoor primary page.
- Q1 2026: more than 5,000 acquisition contracts, double Q4 2025; aged inventory down from 33% to 10% (not attributed to AI specifically).
**Sources**
- https://www.opendoor.com/articles/key-agent-app (≈19:05) — quote: "We built the Key Agent app to directly address common feedback from agents."
- https://www.onlinemarketplaces.com/articles/opendoor-q1-2026-acquisitions-double-as-ai-and-agent-pivot-gains-traction/ (≈19:05)
- https://www.zacks.com/stock/news/2792629/can-opendoor-20-redefine-ibuying-through-ai-and-automation (search excerpt, ≈19:05)

---

## 11. Startups and vendors

### Epique AI (Epique Realty)
Agent-side suite: bios, blogs, listing descriptions, email campaigns, "Sound Smarter" rewriting, virtual staging; EpiqueAI 2.0 (26.6.2025) adds BrokerAI (answers complex real-estate questions), AI coaches, ERIQ 2.0 analytics. Aggregators also list "Legal AI" (state real-estate law information) for Epique agents (not verified on a primary page). No disclaimers or metrics in the release.
- https://www.newswire.com/news/epique-realty-unveils-epiqueai-2-0-thinking-outside-the-chatbox (≈19:05)

### Restb.ai (computer vision, B2B)
White-label vision for MLSs and portals: photo room-type and feature tagging, photo compliance, auto-filling 450+ standardised listing fields (2025), listing descriptions from 300+ detected details, visually similar listings search, and a Property Condition score on the UAD C1-C6 scale with kitchen, bath, interior and exterior sub-scores plus a confidence score that drops with too few or poor photos. Restb.ai says it reaches more than 1 million agents via MLS partnerships (April 2026, search excerpt). Useful pattern: every AI score shown with a confidence signal.
- https://restb.ai/solutions/property-condition/ (search excerpt, ≈19:04)
- https://www.housingwire.com/company-profile/restb-ai-3/ (search excerpt, ≈19:03)

### "RealGPT"
No product with that name was found (not verified). Closest: The Real Brokerage's Leo stack: Leo CoPilot for agents (can escalate to a human broker) and HeyLeo (4.11.2025), a consumer concierge by voice or text on the agent's number that asks location, price and must-haves, answers property questions (closets, pool, HVAC age), connects to a Real agent and to One Real Mortgage; beta in 20 states. A search excerpt says HeyLeo introduces itself as a "real estate concierge"; the HousingWire article does not state whether it says it is an AI (not verified).
- https://www.housingwire.com/articles/meet-heyleo-reals-ai-concierge-that-lets-homebuyers-talk-their-way-to-a-dream-home (≈19:05)

### Ylopo AI (lead nurture, B2B)
AI text (two-way SMS, 24/7) and AI voice (outbound calls, callbacks, up to 90 days); successful calls are live-transferred to the agent with notes synced to the CRM; agents can jump into the text thread. Vendor numbers: 25,000,000+ text conversations, 48% response rate, "on average it takes 7 calls to connect with a lead". A search excerpt says the voice agent introduces itself as a digital assistant (not verified on the fetched page).
- https://www.ylopo.com/ylopo-ai (≈19:04)

### Structurely (AI ISA, B2B)
AI inside-sales assistant over SMS, email and web chat that qualifies leads and books appointments; persona names (for example "Stephanie Holmes"). eXp case study: of the first 300 Zillow Premier Agent leads, 50 qualified and booked (17%). AI disclosure to leads not stated (not verified).
- https://www.casestudies.com/company/structurely/case-study/outsourcing-lead-follow-up-using-ai (≈19:04)

### Lofty (formerly Chime, CRM)
"AI Sales Agent" persona ("Anna") that texts, qualifies and nurtures new leads, call screening and transfers; vendor claims up to 240% higher lead engagement and 114% more appointments (press release 23.9.2025, search excerpt only). Note: "Lofty AI" is also the name of an unrelated tokenised-property platform; this entry is the Lofty CRM.
- https://lofty.com/ai/sales-agent (search excerpt, ≈19:04)

### Rechat Lucy (agent super-app)
Launched 28.7.2025: reads and interprets standard real-estate documents and answers agents' questions about them; writes listing descriptions, CMA reports, emails, social posts, property websites; client communications; "Hey Lucy" voice commands (2026). Vendor numbers: usage +114% from May to June 2025; some client brokerages above 75% CRM adoption and 95% satisfaction.
- https://www.rismedia.com/2025/07/28/rechat-releases-lucy-ai-agent-assistant (≈19:04) — quote: "creating for you, not just responding to you."

### Bonus, Europe and Israel
- **ImmoScout24 HeyImmo** (Germany, 21.10.2025, GPT-5 per OpenAI's customer story, excerpt only): free assistant in app, site and "Meine Immobilien"; personalised listings, market-price help, financing calculations, tenant help on service-charge statements and rent increases, owner advice on modernisation; login keeps conversation history; multilingual; beta. Also a ChatGPT app, voice input and travel-time search (June 2026). No disclaimers, handoff or metrics stated. https://www.immobilienscout24.de/unternehmen/news-medien/news/default-title/immoscout24-startet-kostenlosen-ki-assistenten-heyimmo/ (≈19:05)
- **Zumper Zoe** (USA rentals, Dec 2024): chat inside select listings answering renter questions about the unit and area, tours, rent and maintenance questions; Zumper ChatGPT app February 2026 (search excerpt only).
- **Madlan AI (Israel, direct competitor)**: Madlan blog post dated 22.10.2026 describes free-text apartment search replacing filters, with answers combining available apartments and Madlan data on transactions, education, safety and future planning, and says it handles complex questions too (search excerpt only; page behind a Cloudflare challenge, not bypassed). https://www.madlan.co.il/blog/?p=88893 (≈19:04)
- **Yad2**: AI "personal analyst" announced for the car marketplace (February 2026); no apartment AI chat found (not verified).

---

## 12. Guardrail rules and published practice

### US Fair Housing Act and HUD (2024 guidance, and what happened to it)
- On 2.5.2024 HUD announced two documents (issued 29.4.2024): one on tenant screening (including machine learning and AI by screening vendors), one on advertising housing through digital platforms. HUD's message: the Fair Housing Act applies when AI or algorithms do the screening or the ad targeting and delivery; avoid targeting or delivery that withholds housing information by protected characteristic, avoid predatory targeting, avoid content that discourages people, avoid charging differently by protected characteristic. Covers intentional discrimination and unjustified discriminatory effect.
- **Status change (verified in the Federal Register)**: HUD FHEO's notice in the Federal Register of 6.4.2026 (Vol. 91, No. 65, p. 17292) lists the 29.4.2024 "Guidance on Application of the Fair Housing Act to the Advertising of Housing, Credit, and Other Real Estate-Related Transactions through Digital Platforms" as **withdrawn effective 17.9.2025**, removed from HUD.gov and "should not be relied upon". The same notice says actions that do not comply with the Act's text remain subject to enforcement.
- The 2024 tenant-screening guidance is **not** on that FHEO list, and **not** on the separate OGC withdrawal list (Federal Register 17.7.2026, 13 documents, effective 25.9.2025). Its current status is not verified.
- Practical reading: the statute, steering prohibitions and private litigation risk are unchanged; only the agency's interpretive guidance moved. Commentators: "The law still applies." (Navigate Housing).
- Litigation-side practice (Spencer Fane, 6.2.2026): chatbots create verbatim transcripts and can be queried repeatedly by testers, so one bad answer pattern multiplies; variable tone or detail between similar questions is itself a risk; vendors are treated as extensions of the leasing office. Recommended: keep and review transcripts, test common questions periodically with legal and ops, and write vendor contracts with fair-housing duties, audit rights and fast correction.

Sources
- https://archives.hud.gov/news/2024/pr24-098.cfm (≈19:02) — quote: "the Fair Housing Act applies to tenant screening and the advertising of housing"
- https://www.govinfo.gov/content/pkg/FR-2026-04-06/pdf/2026-06607.pdf (PDF text extracted locally, ≈19:03)
- https://www.govinfo.gov/content/pkg/FR-2026-07-17/html/2026-14432.htm (≈19:04)
- https://www.navigatehousing.com/fair-housing-guidance-withdrawal-what-huds-2026-notice-means-for-housing-providers/ (≈19:03)
- https://www.spencerfane.com/insight/the-next-frontier-of-fair-housing-risk-ai-chatbots-and-early-stage-applicant-interactions/ (≈19:05)

### NAR (National Association of REALTORS)
- NAR article (23.10.2026): verify every AI fact against the MLS record or source documents; human review of listings, ads, emails, CMAs and anything with a client's name; Code of Ethics Articles 2 and 12 (no exaggeration or misrepresentation) apply to AI output; describe the property, not the people who should live there, including in ad targeting and lead scoring; label materially altered or AI-generated images (California requires a statement plus a link or QR code to the original; Wisconsin from 1.1.2027; NorthstarMLS wants a "before" image); some states require disclosure when a bot talks to consumers; chatbot risks named: wrong recipient, auto-replies that sound like advice, AI answering price or value questions; AI may not do licensed activities.
- NAR Brokerage AI Policy Kit (template, March 2026; NAR says it is a resource, not legal advice). Key lines read in the PDF:
  - Agentic AI needs human supervision for high-impact decisions (client communications, transaction documents, pricing); "Fully autonomous execution without human review is prohibited." AI may not perform licensed activities or create agency obligations.
  - Prohibited: discriminatory or misleading content; fake testimonials or reviews without written approval; AI property values for clients without agent review and disclaimers; AI deciding which clients to serve or prioritise without human review; presenting AI content as human-written where disclosure is required.
  - Fair housing: review all AI listing and marketing text before publication; no targeting or exclusion by protected class; no steering language; no AI descriptions of neighbourhoods, school districts, demographics or "community characteristics" without careful human review; review lead scoring and matching for disparate impact. The kit's banned examples (paraphrased): naming the ideal occupant (a young professional couple, families with children), walking distance to a named house of worship, a quiet mature community, and any reference to the racial, ethnic or religious make-up of an area.
  - Chatbots: clearly identified as AI where required; must not give legal advice, financial advice or specific property valuations to consumers; must escalate to a licensed agent on transaction-specific questions, pricing, negotiation or contracts; comply with privacy policy.
  - Vendors: contracts prohibiting model training on brokerage or client data; vendors must disclose known limitations.
- NAR on AI chat surfaces and MLS data (21.10.2025): MLSs should check whether data reaches an unauthorised party, whether the displaying participant keeps control, and local display rules.

Sources
- https://www.nar.realtor/news/real-estate-news/technology/faster-cheaper-riskier-what-brokers-should-know-before-putting-ai-to-work (≈19:02)
- https://bayeast.org/wp-content/uploads/NAR-Brokerage-AI-Policy-Kit-March-2026.pdf (PDF text extracted locally, ≈19:03)
- https://www.realestatenews.com/2025/10/22/zillows-chatgpt-integration-forces-industry-reckoning (NAR position, ≈19:04)

### EU AI Act, Article 50 (transparency)
- Applies from **2.8.2026** (Article 113). Art. 50(1): providers must design AI systems that interact directly with people so the people are informed they are dealing with an AI, unless obvious to a reasonably well-informed, observant and circumspect person. Art. 50(5): the information must be clear and distinguishable, accessible, given "at the latest at the time of the first interaction or exposure."
- Art. 50(2): machine-readable marking of synthetic audio, image, video and text by providers (generative systems already on the market before 2.8.2026 have until 2.12.2026, per the AI Omnibus as summarised by Seyfarth). Art. 50(4): deployers must disclose deepfakes, and AI-generated text published to inform the public on matters of public interest unless a human reviewed it under editorial responsibility.
- Commission guidelines (as summarised by Seyfarth / Legal 500, 3.8.2026, not read in the original): disclosure cannot be buried in terms or privacy notices; acceptable as a session-start introduction or a persistent visible label, with an accessible alternative; wording not prescribed ("You are interacting with an AI system" is one option); the "obvious" exception is narrow, and helpdesk-style agents generally do not qualify; consider vulnerable users. Fines up to EUR 15 million or 3% of worldwide turnover.
- Whether the Act binds an Israeli site depends on its territorial scope (for example output used in the EU, or EU users on the English pages). Not analysed in this pass; needs a legal check.

Sources
- https://artificialintelligenceact.eu/article/50/ (≈19:03)
- https://www.legal500.com/intelligence/global/privacy/european-commission-press-release-eu-ai-act-transparency-enforcement-starts-this-sunday-do-you-know-who-your-chatbots-are-we-break-down-the-commissions-guidelines-on-transparency-below (≈19:04)
- https://www.addleshawgoddard.com/en/insights/insights-briefings/2026/technology/ai-transparency-ai-act-what-businesses-need-know/ (≈19:03)

---

## Patterns worth copying

1. **Put the assistant inside the existing search bar and listing page, not in a floating bubble.** Redfin (search bar on home, map and listing pages), Rightmove (chat window next to search, then listing pages, then results pages), Homes.com (blended into the page, aware of what the user is looking at). Only Rightmove and Redfin publish lift numbers, and both are embedded.
2. **Listing-page Q&A is the highest-intent job.** 59% of Ask Redfin questions were about the home on screen; Rightmove added listing answers as phase two. Ground answers in the listing, then in area data (maps, schools, transport).
3. **Comparison as a first-class job.** Zillow (compare units, explain trade-offs), Rightmove Comparison Assistant (user-added comparison rows), Realtor.com (side-by-side homes or neighbourhoods), idealista (compare results).
4. **Affordability in plain language from the user's own income and savings.** Zillow BuyAbility, Realtor.com calculator and RealAssist, REA, ImmoScout24 financing. Early Zillow tests: affordability is a top question.
5. **Commute and lifestyle search.** REA: 32% of AI searches include a commute radius, 59% start wide on lifestyle. Redfin and Realtor.com do commute and school proximity.
6. **Honest "no match" answers with a concrete relaxation suggestion** (Redfin: widen radius, drop a filter) instead of padding results.
7. **Explain valuation, don't issue one.** REA realAssist explains why an estimate changed; Zillow lets users see and challenge the Zestimate history; Restb.ai shows a confidence score with every condition score. Pair any number with its source, date and confidence.
8. **The next action lives in the same conversation**: book a tour, send an enquiry, talk to an agent (Zillow AI mode, REA, Realtor.com). Redfin: 8% of Ask Redfin users asked for a tour and nearly 1 in 10 for an agent; conversational search users 47% more likely to request a tour.
9. **Escalate to a human on offers, value opinions, contracts and negotiation.** Ask Redfin hands "how to make an offer" and value opinions to a licensed agent; NAR kit requires escalation on transaction-specific, pricing, negotiation and contract questions.
10. **Help the user prepare for the human.** Zillow AI mode helps users prepare for the conversation with the agent or property manager; give the receiving side a summary of what the buyer said (Ylopo sends call notes and outcomes to the CRM with the live transfer).
11. **Lead goes to the listing's own advertiser.** Homes.com "Your Listing, Your Lead". Clear, simple routing builds advertiser trust.
12. **Memory across sessions, with login.** Zillow, Realtor.com (resume after a day or two), Homes.com (planned), ImmoScout24 (history needs login).
13. **A fair-housing / anti-discrimination checker on both input and output**, not just a system prompt. Zillow: stop list plus classifier, runs on the question and the answer, generated neighbourhood text screened before display. Redfin: explicit refusal on protected-class questions.
14. **Write area descriptions about places, never about people.** NAR's banned examples (ideal-occupant phrasing such as families with children, distance to a named house of worship, a quiet mature community, ethnic or religious make-up) are a ready test set.
15. **AI disclosure at first contact plus a persistent label** (EU Article 50 guidance), with an accessible alternative.
16. **Keep and review transcripts; test the same questions repeatedly** (Spencer Fane), and treat a vendor model as your own office.
17. **AI-ready listings.** REA tells agents to write listings detailed enough for conversational search; Restb.ai auto-fills 450+ fields from photos. Structured listing data is what the assistant can answer from.
18. **Use external chat apps (ChatGPT, Claude) as discovery doors that hand back to the site** for tours, contact and full detail (Zillow, Redfin, Realtor.com, Rightmove "stepping stone"), showing only previews and keeping data out of model training.

## Patterns to avoid

1. **Launching a demographic-aware chat with no fair-housing layer.** OpenAI deactivated Zillow's and Redfin's 2023 plugins over Fair Housing Act concerns.
2. **Answering "is this a good neighbourhood for [group]" questions**, describing who lives somewhere, or ranking areas by religious or ethnic composition (steering). Also lead scoring or ad targeting that proxies protected traits.
3. **Specific valuations, legal advice or financial advice from the bot.** NAR kit: chatbots must not give legal advice, financial advice or specific property valuations to consumers. Zillow and Realtor.com both say the AI does not replace licensed expertise. Note the tension: Zillow AI mode does suggest a fair offer price; it can do this as a licensed brokerage, which nad-lan is not.
4. **Fully autonomous actions on high-impact steps** (sending client messages, pricing, transaction documents) without human review (NAR kit: prohibited).
5. **Hiding that it is a bot, or burying the disclosure in terms.** Persona names (Structurely "Stephanie Holmes", Lofty "Anna") without a clear AI notice are a risk under EU Article 50 and some US state bot laws.
6. **Inconsistent answers to similar questions**, which testers can compare across transcripts.
7. **Over-claiming unverified features or guardrails.** Several launches assert "guardrails" with no detail (Homes.com, Realtor.com); others publish no metrics. Claims that cannot be shown become a liability.
8. **Letting listing data leak** (bulk CSV/JSON export from a chat surface, model training on listings). Zillow's ChatGPT app drew MLS licensing complaints over exactly this.
9. **A chat that replaces filters entirely.** REA calls AI search "a partner, not a replacement, for search filters"; Rightmove keeps the normal search next to the chat; 72% of REA AI-search users still adjust their search mid-conversation.
10. **Stretching results when nothing matches**, or inventing facts to fill gaps (Redfin's design explicitly tells the user that no homes fit).
11. **Off-topic drift.** Homes AI declines unrelated requests (football, recipes); scope the assistant to housing.
12. **Synthetic images without labels.** NAR: label AI-altered images and keep the original; California and some MLSs require it. Realtor.com's "home at night / in winter / new finish" visuals need a clear "illustration" label.

## Fit with nad-lan's own rules (for the design brief)

- Honesty law: the "no match" answer and "unknown = omitted" match patterns 6 and avoid-10; any valuation or price talk must cite source, date and range (pattern 7).
- The site never presents itself as a broker (Brokers Law exemption): handoff should go to the listing's developer, advertiser or a named licensed professional, like Homes.com's "Your Listing, Your Lead", and the bot should not negotiate or give offer advice itself.
- Lead privacy: the lead form notice is already the biggest exposure; a chat that collects budget, income or family details needs the same notice at first contact, plus the AI disclosure.
- Israeli discrimination and AI-disclosure law were not researched in this pass; a legal check is needed before launch. Madlan AI (22.10.2026) is the local competitor to benchmark by hand.
