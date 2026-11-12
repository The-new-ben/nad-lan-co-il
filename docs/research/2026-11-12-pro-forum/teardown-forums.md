# Forum and Q&A products: a feature and micro-feature teardown

Retrieved: **12.11.2026**. Scope: Discourse, Flarum, Lemmy, Reddit, Stack Overflow / Stack Exchange, Circle (circle.so), Discord (forum channels and server features), plus Google's own structured-data and link documentation for the SEO rows.

The goal is a new forum for real-estate professionals on an Israeli portal. It has to work in Hebrew, right to left, on phones first, let people in without a long registration, and stop spam hard.

**How this was gathered.** Only official documentation, official help centres and blogs, Google's developer docs, and source code in the official GitHub repos were used. Nothing was logged in to, no account was created, and no robot check was touched. No Google search-results research was done. Every row cites a page or file that was actually opened on 12.11.2026.

Numbers come from source-code defaults (`site_settings.yml` and plugin `settings.yml` files on `main`) or from help-centre text. A default in code is the out-of-the-box value; operators can change it. Where only the name of a feature was seen, without its behaviour, the row says "unverified".

**Columns.** The last two columns are my own judgement, not sourced.
- **Effort:** how hard it would be to build as a custom WordPress plugin. S = days, M = 1–3 weeks, L = more than a month or needs a realtime/AI/infra component.
- **Value:** how much it matters for a *small, new* professional community.

**Product codes:** DSC Discourse · FLA Flarum · LEM Lemmy · RDT Reddit · SO Stack Overflow/Stack Exchange · CIR Circle · DCD Discord.

---

## The big table

| # | Area | Feature | Micro-feature (exact behaviour) | Who has it | Source URL | Effort | Value |
|---|---|---|---|---|---|---|---|
| 1 | Composer | Draft autosave | Drafts save automatically; on mobile a bar reads "Post draft in progress. Tap to resume." | DSC | https://www.discourse.org/features ; https://github.com/discourse/discourse/blob/main/config/locales/client.en.yml | S | high: phone users get interrupted |
| 2 | Composer | Quote reply from highlighted text | Highlighting text inside a post offers a quote button; each user can turn this off ("Enable quote reply for highlighted text", default on: `default_other_enable_quoting: true`). | DSC | https://github.com/discourse/discourse/blob/main/config/locales/client.en.yml ; https://github.com/discourse/discourse/blob/main/config/site_settings.yml | M | high: precise answers to professional questions |
| 3 | Composer | Share a quote | The selection pop-up also has a "Share" action next to quote. | DSC | https://github.com/discourse/discourse/blob/main/config/locales/client.en.yml | S | med |
| 4 | Composer | @mention autocomplete and caps | `@name` notifies the user. Default cap is 10 mentions per post (`max_mentions_per_post: 10`), and 2 for new users. | DSC, FLA (mentions ext.), LEM (@user, !community), DCD | https://github.com/discourse/discourse/blob/main/config/site_settings.yml ; https://join-lemmy.org/ | M | high |
| 5 | Composer | Mention without typing "@" | An experiment: start typing a name and press Tab to insert the mention. It searches username, display name, server nickname and friend nickname. | DCD | https://support.discord.com/hc/en-us/articles/35692242798743-Mention-Suggestions-FAQ | M | low |
| 6 | Composer | Group mention cap | `@group` notifies at most 100 users (`max_users_notified_per_group_mention: 100`). | DSC | https://github.com/discourse/discourse/blob/main/config/site_settings.yml | S | med: "@appraisers", "@brokers-north" |
| 7 | Composer | Link onebox (unfurl) | A pasted bare link to a known site expands into a preview card. Default cap is 50 oneboxes per post, with a domain blocklist (`blocked_onebox_domains`). | DSC | https://www.discourse.org/features ; https://github.com/discourse/discourse/blob/main/config/site_settings.yml | M | high: shared listings and gov.il links look rich |
| 8 | Composer | Drag-and-drop and paste image upload | Images upload by drag and drop. Default image size limit is 10,240 KB. | DSC, LEM (image uploads) | https://www.discourse.org/features ; https://github.com/discourse/discourse/blob/main/config/site_settings.yml ; https://join-lemmy.org/ | S | high: photos of plans and contracts |
| 9 | Composer | Download hotlinked images | `download_remote_images_to_local` copies external images to local storage so posts don't break later. | DSC | https://github.com/discourse/discourse/blob/main/config/site_settings.yml | S | med |
| 10 | Composer | Markdown, BBCode and HTML | All three formats are supported, plus a WYSIWYG ("rich text") mode with `enable_rich_text_paste`. | DSC, FLA (Markdown + WYSIWYG) | https://www.discourse.org/features ; https://flarum.org/ | M | high: pros won't type markdown, so WYSIWYG is needed |
| 11 | Composer | Emoji picker | Searchable emoji picker with five emoji sets and custom emoji. Lemmy autocompletes emoji. | DSC, FLA, LEM | https://www.discourse.org/features ; https://join-lemmy.org/ | S | med |
| 12 | Composer | Polls in posts | Up to 20 options by default. A poll can be edited for 5 minutes. Creating one requires trust level 1 or higher. Votes are public by default. | DSC | https://github.com/discourse/discourse/blob/main/plugins/poll/config/settings.yml | M | med: quick market-sentiment polls |
| 13 | Composer | "Your topic is similar to…" | While a new title is typed, similar topics appear. Matching starts at a 10-character title (`min_title_similar_length: 10`). | DSC | https://github.com/discourse/discourse/blob/main/config/locales/client.en.yml ; https://github.com/discourse/discourse/blob/main/config/site_settings.yml | M | high: avoids duplicate threads |
| 14 | Composer | Duplicate-title block | Duplicate topic titles are refused by default (`allow_duplicate_topic_titles: false`). | DSC | https://github.com/discourse/discourse/blob/main/config/site_settings.yml | S | med |
| 15 | Composer | Saved reply templates | Staff (and optionally private groups) insert canned replies from a template category. | DSC (discourse-templates, bundled) | https://github.com/discourse/discourse/blob/main/plugins/discourse-templates/config/settings.yml | S | med: moderator canned answers |
| 16 | Composer | Saved responses / removal reasons | Moderators keep saved responses for removals. | RDT | https://support.reddithelp.com/hc/en-us/search?query=removal+reasons (result: "Saved Responses") | S | med |
| 17 | Composer | Reply as linked topic | The composer offers "reply as new topic", which links back to the original. | DSC | https://github.com/discourse/discourse/blob/main/config/locales/client.en.yml | M | med |
| 18 | Composer | Edit grace window | Edits within 300 s, and under 100 changed characters (400 for high trust), create no new revision. | DSC | https://github.com/discourse/discourse/blob/main/config/site_settings.yml | S | high: typo fixes don't clutter history |
| 19 | Composer | Edit time limit | Authors can edit for 1,440 min (24 h) at TL0/TL1 and 43,200 min (30 days) from TL2. | DSC | https://github.com/discourse/discourse/blob/main/config/site_settings.yml ; https://blog.discourse.org/2018/06/understanding-discourse-trust-levels/ | S | med |
| 20 | Composer | Public edit history | Revision history is visible to the public by default (`edit_history_visible_to_public: true`). SO keeps a public revision history with attribution and rollback. | DSC, SO | https://github.com/discourse/discourse/blob/main/config/site_settings.yml ; https://stackoverflow.com/help/editing | M | high: trust in a professional forum |
| 21 | Composer | Edit reason | An optional "Why are you editing?" field. | DSC | https://github.com/discourse/discourse/blob/main/config/locales/client.en.yml | S | low |
| 22 | Composer | Community editing with review | Edits by users under 2,000 rep go to a queue and need 2 accept/reject votes. At 2,000+ edits apply at once. Many rejected edits bring a 7-day ban from suggesting edits. | SO | https://stackoverflow.com/help/editing | M | low for a small community |
| 23 | Composer | Collaborative wiki posts | A post can be made a wiki that others edit. On SO, creating wiki posts needs 10 rep and editing community wiki needs 100. | DSC, SO | https://www.discourse.org/features ; https://stackoverflow.com/help/privileges | M | med: shared "how to register a caveat" pages |
| 24 | Composer | Rule check while posting | Mods define rules with regex. Posters see an alert *while writing* and can be informed, reported or blocked. Mods are exempt. | RDT (Post & Comment Guidance) | https://support.reddithelp.com/hc/en-us/articles/17625458521748-Automations-Post-Comment-Guidance-Set-Up | M | high: stops listing spam before it posts |
| 25 | Composer | AI rule check before posting | On submit, an LLM checks the draft against community rules and highlights possible violations (an experiment). | RDT (Post Check) | https://support.reddithelp.com/hc/en-us/articles/35317229808660-Post-Check-Poster-Eligibility-Guide | L | med |
| 26 | Composer | Reply with ping toggle | Replies ping the original author by default; the replier can toggle the ping off. | DCD | https://support.discord.com/hc/en-us/articles/360057382374-Replies-FAQ | S | med |
| 27 | Composer | Spoiler / hidden details | Spoiler hiding, a details/expand block, footnotes and local-time dates are bundled plugins. | DSC | https://www.discourse.org/features ; https://github.com/discourse/discourse/tree/main/plugins | S | low |
| 28 | Composer | Minimum length and entropy | Defaults: posts at least 20 characters, titles at least 15, title entropy at least 10, body entropy at least 7. This blocks "aaaa" and one-word posts. | DSC | https://github.com/discourse/discourse/blob/main/config/site_settings.yml | S | high: cheap quality gate |
| 29 | Composer | Mandatory tag on new post | The forum can require at least one tag (REQUIRE_TAG flag). Up to 5 tags per post. | DCD | https://raw.githubusercontent.com/discord/discord-api-docs/main/developers/resources/channel.mdx ; https://support.discord.com/hc/en-us/articles/6208479917079-Forum-Channels-FAQ | S | high: forces "rent/sale/appraisal/legal" labels |
| 30 | Composer | Scheduled and recurring posts | Mods schedule posts hourly, daily, weekly or monthly, or on a custom pattern. | RDT | https://support.reddithelp.com/hc/en-us/articles/15484443169556-Scheduled-and-Recurring-Posts | M | high: weekly "deals of the week" thread keeps it alive |
| 31 | Reading | Just-in-time loading | Posts load as you scroll, with no pagination for people. | DSC | https://www.discourse.org/features | M | high on phones |
| 32 | Reading | Crawler pages with rel prev/next | Bots get server-rendered pages with `<link rel="prev/next">` and prev/next anchors. | DSC | https://github.com/discourse/discourse/blob/main/app/views/topics/show.html.erb | M | high for SEO (see SEO rows) |
| 33 | Reading | Read-position tracking | The client records per-post reading time. Tracking pauses if there is no scroll for 3 min and caps at 6 min. Anonymous visitors track up to 5 topics locally. | DSC | https://github.com/discourse/discourse/blob/main/frontend/discourse/app/services/screen-track.js | M | high: drives "unread" |
| 34 | Reading | New / unread counts | A topic counts as "new" for 2 days by default (`default_other_new_topic_duration_minutes: 2880`). It becomes tracked after 5 min of reading (`default_other_auto_track_topics_after_msecs: 300000`). | DSC | https://github.com/discourse/discourse/blob/main/config/site_settings.yml | M | high |
| 35 | Reading | Timeline scrubber | A vertical timeline with a scroller and a back button to jump around long topics. | DSC | https://github.com/discourse/discourse/tree/main/frontend/discourse/app/components/topic-timeline (tree listing) ; https://github.com/discourse/discourse/blob/main/config/locales/client.en.yml | M | med |
| 36 | Reading | Jump to post / last read / bottom | "Jump to #N", "Last Read" and "Jump to the last post" controls. | DSC | https://github.com/discourse/discourse/blob/main/config/locales/client.en.yml | S | high |
| 37 | Reading | Context expansion | A reply can be expanded above or below in place, and quotes expand to show the full original. | DSC | https://www.discourse.org/features | M | med |
| 38 | Reading | Topic summary (top posts) | "Summarize" condenses a topic to its most popular posts. Offered once a topic has 50 or more posts (`summary_posts_required: 50`). | DSC | https://www.discourse.org/features ; https://github.com/discourse/discourse/blob/main/config/site_settings.yml | M | low early, high later |
| 39 | Reading | AI summary and gists | AI topic summaries and one-line gists; optionally served to crawlers. Off by default. | DSC (discourse-ai) | https://github.com/discourse/discourse/blob/main/plugins/discourse-ai/config/settings.yml | L | med |
| 40 | Reading | Accepted solution | The asker (and TL4/staff) marks a solution. The answer is quoted under the question (700 chars). Schema markup is "always" emitted. Optional auto-close after solve. | DSC (discourse-solved, bundled) | https://github.com/discourse/discourse/blob/main/plugins/discourse-solved/config/settings.yml | M | high: professional Q&A needs "the answer" |
| 41 | Reading | Accepted answer + reputation | A coloured check mark. The acceptor gets +2 and the answerer +15. The asker must wait 48 h to accept their own answer, and gains no rep from it. | SO | https://stackoverflow.com/help/accepted-answer | M | high |
| 42 | Reading | Threaded comments | Comments nest in threads. Comment sorts: Hot (default), Top, New, Old, and "Chat" (flat, newest first). | LEM, RDT | https://join-lemmy.org/docs/users/03-votes-and-ranking.html | L | med: flat is simpler for a small forum |
| 43 | Reading | Collapse comments | Crowd Control can collapse comments from untrusted users. | RDT | https://support.reddithelp.com/hc/en-us/articles/15484545006996-Crowd-Control | M | med |
| 44 | Reading | Post sorts | Active (default), Hot, Scaled, Controversial, New, Old, Most Comments, New Comments (forum-style bump), and Top Day/Week/Month/Year/All. | LEM | https://join-lemmy.org/docs/users/03-votes-and-ranking.html | M | med |
| 45 | Reading | Search sorts | Search sorts are Relevance (default), Hot, Top, New and Comment count, with time filters (hour to all time). | RDT | https://support.reddithelp.com/hc/en-us/articles/19695706914196-What-filters-and-sorts-are-available | M | med |
| 46 | Reading | Forum default sort and layout | Sort by latest activity or creation date. List or gallery layout. | DCD | https://raw.githubusercontent.com/discord/discord-api-docs/main/developers/resources/channel.mdx | S | med: gallery suits property photos |
| 47 | Reading | Auto-hide inactive posts | Posts move to "Older Posts" after 1 h, 24 h, 3 days (default) or 1 week of inactivity. Any reply reopens them. | DCD | https://support.discord.com/hc/en-us/articles/6208479917079-Forum-Channels-FAQ | S | med |
| 48 | Reading | Pinned / highlights | Up to 6 highlighted posts in a carousel, each with a label (Event, Megathread, Announcement). | RDT | https://support.reddithelp.com/hc/en-us/articles/15484641176724-Community-highlights-sticky-posts | S | high |
| 49 | Reading | Pinned / sticky | Sticky discussions (Flarum core extension). Pinned topics and sitewide alerts (Discourse). Pinned forum posts (Discord PINNED flag). | FLA, DSC, DCD, LEM | https://docs.flarum.org/extensions/ ; https://www.discourse.org/features ; https://join-lemmy.org/docs/users/04-moderation.html | S | high |
| 50 | Reading | Suggested / related topics | "Suggested topics" and "related messages" blocks at the end of a topic. Optional AI semantic related topics (5 by default, off by default). | DSC | https://github.com/discourse/discourse/blob/main/config/locales/client.en.yml ; https://github.com/discourse/discourse/blob/main/plugins/discourse-ai/config/settings.yml | M | high: keeps visitors from Google reading |
| 51 | Reading | Topic view "heat" | View counts are coloured by low/medium/high thresholds (`topic_views_heat_*`). | DSC | https://github.com/discourse/discourse/blob/main/config/site_settings.yml | S | med: makes it feel busy |
| 52 | Reading | Read time stat | Users' total "read time" appears in profile stats. A per-topic estimated read time was not found. | DSC | https://github.com/discourse/discourse/blob/main/config/locales/client.en.yml | S | low |
| 53 | Reading | Duplicate closure banner | A question closed as a duplicate gets "[duplicate]" in its title and a banner linking the original. It takes 3 close votes, or 1 from a moderator or gold-tag holder. 50 close votes per day. | SO | https://stackoverflow.com/help/duplicates | M | med |
| 54 | Reading | Protected questions | A question becomes protected after more than 3 poor answers or more than 5 "thanks/same problem" answers from new users. Answering it then needs 10 rep. | SO | https://stackoverflow.com/help/privileges/new-user | S | med |
| 55 | Reading | Deck: side-by-side live columns | A page with live columns to follow discussions and notifications together. | FLA (Deck) | https://flarum.org/ | M | low |
| 56 | Reading | Filter by tag (multi-select) | Forum posts filter by one or several tags. | DCD | https://support.discord.com/hc/en-us/articles/6208479917079-Forum-Channels-FAQ | S | high |
| 57 | Reading | Flair as filter | Clicking post flair opens all posts with that flair. | RDT | https://support.reddithelp.com/hc/en-us/articles/15484545678996-Post-Flair | S | high |
| 58 | Reactions & reputation | Likes | A like is a heart. Default cap is 50 likes per day. TL2 gets 1.5× the daily like/edit/flag limits, TL3 2× and TL4 3×. | DSC | https://github.com/discourse/discourse/blob/main/config/site_settings.yml ; https://blog.discourse.org/2018/06/understanding-discourse-trust-levels/ | S | high |
| 59 | Reactions & reputation | Reaction set | Default reactions: +1, laughing, open_mouth, clap, confetti_ball, hugs. Negative emoji (for example -1, angry) don't count as likes. | DSC (discourse-reactions, bundled) | https://github.com/discourse/discourse/blob/main/plugins/discourse-reactions/config/settings.yml | M | med |
| 60 | Reactions & reputation | Likes (Flarum) | Likes ship as a bundled extension. | FLA | https://github.com/flarum/framework/tree/2.x/extensions | S | high |
| 61 | Reactions & reputation | Up/down votes with visible score | Full +/− scores are shown, and the user can hide scores. | LEM, RDT | https://join-lemmy.org/ ; https://join-lemmy.org/docs/users/01-getting-started.html | M | med: downvotes can feel hostile in a small pro group |
| 62 | Reactions & reputation | Reputation points | Question or answer upvote +10. Accepted answer +15 (acceptor +2). Approved edit +2 (cap 1,000). Downvote received −2, and casting a downvote on an answer costs −1. 4 spam/offensive flags −100. Daily cap 200. Rep never goes below 1. | SO | https://stackoverflow.com/help/whats-reputation | M | high: a reason to answer well |
| 63 | Reactions & reputation | Privilege ladder by reputation | 1: post, comment, chat. 5: meta. 10: drop new-user limits, create wiki. 15: upvote, flag. 75: bounty. 100: edit community wiki. 125: downvote. 500: review queues. 1,000: see vote counts. 1,500: create tags. 2,000: edit freely. 3,000: close/reopen. 10,000: mod tools. 15,000: protect. 20,000: trusted user. 25,000: analytics. | SO | https://stackoverflow.com/help/privileges | M | high (scaled down) |
| 64 | Reactions & reputation | Karma | Karma roughly reflects up/down votes on posts and comments (not 1:1). Communities may require karma before posting, as an anti-spam measure. | RDT | https://support.reddithelp.com/hc/en-us/articles/204511829-What-is-karma | M | med |
| 65 | Reactions & reputation | Trust levels (automatic) | TL1: enter 5 topics, read 30 posts, 10 min reading. TL2: 15 visit days, give and receive 1 like, reply to 3 topics, enter 20 topics, read 100 posts, 60 min. TL3: over 100 days, visit 50 days, reply to 10 topics, 20 likes received and 30 given, view 25% of topics and read 25% of posts. TL4 is manual only. | DSC | https://github.com/discourse/discourse/blob/main/config/site_settings.yml ; https://blog.discourse.org/2018/06/understanding-discourse-trust-levels/ | M | high: the backbone of anti-spam |
| 66 | Reactions & reputation | TL3 can be lost | TL3 is demoted if requirements lapse (with a 2-week grace period). It is blocked if the user was suspended or silenced in the last 6 months. | DSC | https://blog.discourse.org/2018/06/understanding-discourse-trust-levels/ | M | med |
| 67 | Reactions & reputation | Badges (3 tiers) | Bronze, silver and gold badges. Examples: Nice Question (score 10+), Good (25+), Great (100+), Curious (good questions on 5 separate days). | SO, DSC (`enable_badges: true`) | https://stackoverflow.com/help/badges ; https://github.com/discourse/discourse/blob/main/config/site_settings.yml | M | high: cheap motivation |
| 68 | Reactions & reputation | Community achievements | Badges such as Elder (member for 3 years) and Repeat Contributor (20 days of posting in one community), plus a community leaderboard. | RDT | https://support.reddithelp.com/hc/en-us/articles/25564722077588-Community-Achievements | M | med |
| 69 | Reactions & reputation | Points, levels, leaderboard | 1 point per like received. 9 colour-coded levels. Leaderboard tabs for 7 days, 30 days and all time, each showing the top 10 with the top 3 highlighted. The level badge and a progress bar sit on the avatar. | CIR | https://help.circle.so/p/audience/gamification/get-to-know-gamification | M | high |
| 70 | Reactions & reputation | Gamification scores | Defaults: like received 1, like given 1, solution 10, invite 10, topic created 5, post created 2, flag created 10, day visited 1, post read 1. | DSC (discourse-gamification, off by default) | https://github.com/discourse/discourse/blob/main/plugins/discourse-gamification/config/settings.yml | M | high: copy these weights |
| 71 | Reactions & reputation | Bounties | 50–500 rep in steps of 50, offered 2+ days after asking. Runs 7 days plus 24 h grace. At most 3 active per user. Non-refundable. | SO | https://stackoverflow.com/help/bounty | M | low now; later "paid urgent question" |
| 72 | Reactions & reputation | Awards (paid) | Free and paid awards on posts and comments. They can earn recipients cash via the Contributor Program. Communities can opt out. | RDT | https://support.reddithelp.com/hc/en-us/articles/26465598697876-What-are-awards-and-how-do-I-use-them | L | low |
| 73 | Reactions & reputation | User flair | Up to 350 user flair templates. Users may pick their own if allowed. Used to "distinguish trusted members, highlight specialized areas of knowledge". | RDT | https://support.reddithelp.com/hc/en-us/articles/15484503095060-User-Flair | S | high: "licensed broker", "appraiser", "lawyer" |
| 74 | Reactions & reputation | Verified checkmark | A grey checkmark confirms identity only. It does not change ranking or moderation. Free. Beta for businesses (Reddit Pro), alpha for individuals. | RDT | https://support.reddithelp.com/hc/en-us/articles/42763717293716-Verified-profiles-on-Reddit | M | high: broker licence verification is a real moat |
| 75 | Reactions & reputation | Topic voting | Vote on feature-request style topics with per-trust-level vote limits (TL0 default 2). Shows who voted. | DSC (discourse-topic-voting) | https://github.com/discourse/discourse/blob/main/plugins/discourse-topic-voting/config/settings.yml | M | low |
| 76 | Reactions & reputation | Post voting (Q&A mode) | A Q&A-style voting plugin for posts is bundled. Behaviour not opened (unverified). | DSC (discourse-post-voting) | https://github.com/discourse/discourse/tree/main/plugins | M | med |
| 77 | Structure | Categories required | Uncategorized topics are off by default (`allow_uncategorized_topics: false`). | DSC | https://github.com/discourse/discourse/blob/main/config/site_settings.yml | S | high |
| 78 | Structure | Tags | Tags are a bundled extension in Flarum. Discord allows 20 tags per forum (name up to 20 chars, optional emoji) and 5 per post, and "moderated" tags only mods can apply. | FLA, DCD, DSC | https://github.com/flarum/framework/tree/2.x/extensions ; https://raw.githubusercontent.com/discord/discord-api-docs/main/developers/resources/channel.mdx | S | high |
| 79 | Structure | Post flair | Up to 350 post flair templates. Can be required. Can tag removal reasons. | RDT | https://support.reddithelp.com/hc/en-us/articles/15484545678996-Post-Flair | S | high |
| 80 | Structure | Post guidelines per forum | Each forum channel shows guidelines when creating a post. | DCD | https://support.discord.com/hc/en-us/articles/6208479917079-Forum-Channels-FAQ | S | high |
| 81 | Structure | Policy posts (accept rules) | Staff posts that members must accept (bundled plugin, off by default). | DSC (discourse-policy) | https://github.com/discourse/discourse/blob/main/plugins/discourse-policy/config/settings.yml | S | high: accept the community code before the first post |
| 82 | Structure | Solved filter per category | Solved can be enabled per category or tag, and a "filter by solved status" option exists. | DSC | https://github.com/discourse/discourse/blob/main/plugins/discourse-solved/config/settings.yml | S | high |
| 83 | Structure | Assign topic to a person | Topics can be assigned, with statuses New / In Progress / Done. Up to 10 assigned topics by default. | DSC (discourse-assign) | https://github.com/discourse/discourse/blob/main/plugins/discourse-assign/config/settings.yml | M | low |
| 84 | Structure | Private messages | PMs are allowed from TL1. Default cap is 20 PMs per day. PM threads auto-close at 500 posts. | DSC, FLA (Messages), LEM, RDT (chat) | https://github.com/discourse/discourse/blob/main/config/site_settings.yml ; https://flarum.org/ | M | high: deal talk moves private |
| 85 | Structure | Built-in chat | Chat channels sit beside topics, and a chat message can be quoted into a topic. | DSC (chat, bundled), DCD | https://www.discourse.org/features | L | med |
| 86 | Structure | Groups and permissions | Groups with per-category access. Self-managing groups. | DSC, FLA | https://www.discourse.org/features ; https://flarum.org/ | M | high: private "verified brokers" room |
| 87 | Structure | User card on hover/tap | Hovering or tapping a name shows a card (with gamification score, cake day, chat button via plugins). Circle shows level and progress on the card. | DSC, CIR | https://github.com/discourse/discourse/tree/main/plugins/discourse-gamification ; https://help.circle.so/p/audience/gamification/get-to-know-gamification | M | high: see who is talking at a glance |
| 88 | Structure | Nicknames / display names | Display names alongside usernames (`enable_names: true`; Flarum Nicknames extension). | DSC, FLA | https://github.com/discourse/discourse/blob/main/config/site_settings.yml ; https://docs.flarum.org/extensions/ | S | high: Hebrew real names |
| 89 | Structure | User status | Users can set a status (off by default, `enable_user_status: false`). | DSC | https://github.com/discourse/discourse/blob/main/config/site_settings.yml | S | low |
| 90 | Structure | Custom profile fields | Custom profile fields exist (a help-centre section). | CIR | https://help.circle.so/ | M | high: licence no., region, speciality |
| 91 | Structure | Featured link on topic | A topic can carry a featured external link (`topic_featured_link_enabled`). | DSC | https://github.com/discourse/discourse/blob/main/config/site_settings.yml | S | med: link a listing |
| 92 | Structure | Calendar / events | Bundled events plugin. Circle has event spaces. | DSC (discourse-events), CIR | https://github.com/discourse/discourse/tree/main/plugins ; https://help.circle.so/ | M | med: open houses, meetups |
| 93 | Structure | Communities / spaces | Communities can be subscribed to and filtered (subscribed, local, all). Circle has post, image and chat spaces. | LEM, CIR | https://join-lemmy.org/docs/users/01-getting-started.html ; https://help.circle.so/ | M | med |
| 94 | Notifications | Bell + per-topic watch levels | Watching (every post plus count), Watching First Post, Tracking (mentions/replies plus count), Normal, Muted. Replying sets Tracking by default. | DSC | https://github.com/discourse/discourse/blob/main/config/locales/client.en.yml ; https://github.com/discourse/discourse/blob/main/config/site_settings.yml | M | high |
| 95 | Notifications | Follow discussions | Subscriptions extension (follow/ignore discussions). | FLA | https://github.com/flarum/framework/tree/2.x/extensions | S | high |
| 96 | Notifications | Email digest | Default every 10,080 min (weekly) with 5 topics. TL0 excluded by default. Stops after 180 days of inactivity. | DSC | https://github.com/discourse/discourse/blob/main/config/site_settings.yml | M | high: brings lurkers back |
| 97 | Notifications | Weekly digest content rules | Thursday 9 AM PT. Up to 5 popular posts (comments weigh more than likes), 5 popular comments, 5 events and 3 new members. Skipped if fewer than 2 new posts. | CIR | https://help.circle.so/p/audience/notifications/setting-up-the-weekly-digest | M | high: copy the "skip if empty" rule |
| 98 | Notifications | Email digests | Digest emails, and each email carries an unsubscribe link. | FLA | https://flarum.org/ | M | high |
| 99 | Notifications | Reply by email | Notifications go out by email and the user can reply from email. Off by default (`reply_by_email_enabled: false`). | DSC | https://www.discourse.org/features ; https://github.com/discourse/discourse/blob/main/config/site_settings.yml | L | med: pros live in email |
| 100 | Notifications | Mailing-list mode | Every post arrives by email. It overrides the activity summary. Disabled sitewide by default (`disable_mailing_list_mode: true`). | DSC | https://github.com/discourse/discourse/blob/main/config/locales/client.en.yml ; https://github.com/discourse/discourse/blob/main/config/site_settings.yml | M | low |
| 101 | Notifications | Push / PWA | Web-push prompt on by default (`push_notifications_prompt: true`). VAPID keys. Push time window 1 min. iOS/Android apps. | DSC | https://github.com/discourse/discourse/blob/main/config/site_settings.yml ; https://www.discourse.org/features | M | high on phones |
| 102 | Notifications | Live toast notifications | Realtime notification toasts dismiss after 10 s. | FLA (Realtime) | https://raw.githubusercontent.com/flarum/framework/2.x/extensions/realtime/extend.php | L | med |
| 103 | Notifications | Notification defaults for new members | Admins set default notification preferences for new members and per space. | CIR | https://help.circle.so/p/audience/notifications | S | med |
| 104 | Notifications | Bell + optional email | A bell for replies and PMs, optional pop-ups and email. | LEM | https://join-lemmy.org/docs/users/01-getting-started.html | S | high |
| 105 | Notifications | RSS / Atom | Feeds for several views. | LEM | https://join-lemmy.org/ | S | low |
| 106 | Onboarding | Browse without login | Login is not required by default (`login_required: false`). Users don't need approval (`must_approve_users: false`). | DSC | https://github.com/discourse/discourse/blob/main/config/site_settings.yml | S | high: Google traffic must read freely |
| 107 | Onboarding | Ask/answer without reputation | Asking, answering and editing need no reputation ("Reputation is entirely optional"). Anonymous internet users can take part, sandboxed. | SO | https://stackoverflow.com/help/whats-reputation ; https://stackoverflow.com/help/privileges/new-user | S | high |
| 108 | Onboarding | Social login | Google, Facebook, X, Discord, GitHub (Apple, Microsoft and OIDC plugins bundled). Google is off by default. | DSC | https://www.discourse.org/features ; https://github.com/discourse/discourse/tree/main/plugins | M | high: one-tap Google |
| 109 | Onboarding | Passkeys | Passkeys are on by default (`enable_passkeys: true`). | DSC | https://github.com/discourse/discourse/blob/main/config/site_settings.yml | M | high: no passwords on phones |
| 110 | Onboarding | Email login link | Login via an email link (`enable_local_logins_via_email`). Email tokens are valid for 48 h. | DSC | https://github.com/discourse/discourse/blob/main/config/site_settings.yml | S | high: magic link = lowest friction |
| 111 | Onboarding | SSO with the host site | DiscourseConnect lets the forum use the main site's login. | DSC | https://www.discourse.org/features ; https://github.com/discourse/discourse/blob/main/config/site_settings.yml | M | high: the portal's existing users |
| 112 | Onboarding | Invite links | Invites expire in 90 days. 10 invites per day. Allowed from TL2 by default (`invite_allowed_groups: 1/2/12`). | DSC | https://github.com/discourse/discourse/blob/main/config/site_settings.yml | S | high: seed by personal invites |
| 113 | Onboarding | Invite links, bulk import, email verification | Invite links, bulk member import, and enforced email verification for public sign-ups. | CIR | https://help.circle.so/p/audience/onboarding | S | high |
| 114 | Onboarding | Tutorial bot | The narrative bot (discobot) is enabled with a "new_user_track". The welcome post is disabled by default. | DSC | https://github.com/discourse/discourse/blob/main/plugins/discourse-narrative-bot/config/settings.yml | M | med |
| 115 | Onboarding | User tips | Contextual first-use tips exist; off by default (`enable_user_tips: false`). | DSC | https://github.com/discourse/discourse/blob/main/config/site_settings.yml | S | med |
| 116 | Onboarding | Onboarding questions | New members answer a few questions that assign roles and channels, and can change answers later. Multiple-choice or dropdown prompts. | DCD | https://support.discord.com/hc/en-us/articles/11074987197975-Community-Onboarding-FAQ ; https://raw.githubusercontent.com/discord/discord-api-docs/main/developers/resources/guild.mdx | M | high: "I'm a broker / appraiser / investor" |
| 117 | Onboarding | Welcome screen | A server description plus up to 5 suggested channels. | DCD | https://raw.githubusercontent.com/discord/discord-api-docs/main/developers/resources/guild.mdx | S | high |
| 118 | Onboarding | Welcoming guidance | Clear rules in the sidebar, a stickied rules thread, and AutoModerator reminders. | RDT | https://support.reddithelp.com/hc/en-us/articles/15484358732692-Welcoming-new-members | S | med |
| 119 | Onboarding | Anonymous posting | Anonymous mode is off by default. Allowed groups default to TL1+. | DSC | https://github.com/discourse/discourse/blob/main/config/site_settings.yml ; https://www.discourse.org/features | M | med: "is this deal legal?" questions |
| 120 | Onboarding | Pseudonymous usernames | Users choose usernames that need not reveal identity. | RDT | https://support.reddithelp.com/hc/en-us/articles/7420342178324-How-does-being-anonymous-work-on-Reddit | S | med |
| 121 | Onboarding | Signup CTA to lurkers | A sign-up call to action is shown to anonymous readers (`enable_signup_cta`). | DSC | https://github.com/discourse/discourse/blob/main/config/site_settings.yml | S | high |
| 122 | Onboarding | Registration application | The instance can require an answer to an application question that admins approve. | LEM | https://join-lemmy.org/docs/users/01-getting-started.html ; https://raw.githubusercontent.com/LemmyNet/lemmy/0.16.7/config/defaults.hjson | S | high: "your licence number?" |
| 123 | Anti-spam | New-user caps | TL0 defaults: 2 links, 5 embedded media, 0 attachments, 2 mentions per post, 3 replies per topic, 3 topics and 10 replies on the first day. | DSC | https://github.com/discourse/discourse/blob/main/config/site_settings.yml | S | high |
| 124 | Anti-spam | Posting rate limits | 15 s between topics, 5 s between posts, 30 s for new users, 20 topics/day, and identical post refused within 5 min (`unique_posts_mins`). | DSC | https://github.com/discourse/discourse/blob/main/config/site_settings.yml | S | high |
| 125 | Anti-spam | Daily action caps | Likes 50, flags 20, edits 30, invites 10, PMs 20, bookmarks 20 per day. | DSC | https://github.com/discourse/discourse/blob/main/config/site_settings.yml | S | med |
| 126 | Anti-spam | Spam-host detection | A new user who posts links to the same host 3 times is caught (`newuser_spam_host_threshold: 3`). There are allow/block link-domain lists. | DSC | https://github.com/discourse/discourse/blob/main/config/site_settings.yml | M | high: catches the agency-site link dropper |
| 127 | Anti-spam | Signup per IP | Default max 3 new accounts per registration IP. Logins 6/min and 30/hour per IP. Disposable domain mailinator.com blocked by default. | DSC | https://github.com/discourse/discourse/blob/main/config/site_settings.yml | S | high |
| 128 | Anti-spam | Honeypot + challenge with silent success | The signup form has a hidden honeypot field and a reversed challenge value. If either fails, the server answers "success, check your email" and creates nothing. | DSC | https://github.com/discourse/discourse/blob/main/frontend/discourse/app/components/honeypot-input.js ; https://github.com/discourse/discourse/blob/main/app/controllers/users_controller.rb | S | high: cheap, invisible to humans |
| 129 | Anti-spam | Captcha (optional) | hCaptcha or reCAPTCHA v2/v3, disabled by default. v3 score threshold 0.5. | DSC (discourse-captcha) | https://github.com/discourse/discourse/blob/main/plugins/discourse-captcha/config/settings.yml | S | med: only if honeypot fails |
| 130 | Anti-spam | Captcha and email verification at signup | Captcha off by default ("medium" difficulty), plus email verification. | LEM | https://raw.githubusercontent.com/LemmyNet/lemmy/0.16.7/config/defaults.hjson | S | med |
| 131 | Anti-spam | Akismet | Checks posts by users below TL1. Users with more than 50 posts are skipped. A TL1 user's first post goes to review by default. The poster is told. Runs every 10 min. | DSC (discourse-akismet plugin) | https://github.com/discourse/discourse-akismet/blob/main/config/settings.yml | S | high: WordPress already has Akismet |
| 132 | Anti-spam | Akismet with learning | Posts are checked on save. Hiding a post reports it as spam, and approving a post reports it as ham. | FLA (bundled) | https://raw.githubusercontent.com/flarum/framework/2.x/extensions/akismet/extend.php | S | high |
| 133 | Anti-spam | AI spam scan | An LLM scans the first 3 posts of users up to TL1. Off by default. | DSC (discourse-ai) | https://github.com/discourse/discourse/blob/main/plugins/discourse-ai/config/settings.yml | L | med |
| 134 | Anti-spam | Approval queue | Post approval exists. Defaults approve nobody's posts by force (TL0 is in the "unless" groups, `approve_post_count: 0`). There is a regex to auto-silence on the first post. | DSC | https://github.com/discourse/discourse/blob/main/config/site_settings.yml | M | high |
| 135 | Anti-spam | First post/comment approval | Holds a member's content until their first post or comment is approved. "Moderate after rejection" keeps a rejected member on approval. Per-space "flag all new posts". | CIR | https://help.circle.so/p/administration/moderation/manage-moderation-settings | M | high: exactly what a small pro forum needs |
| 136 | Anti-spam | Unapproved posts (Flarum) | The Approval extension holds posts as `is_approved=false` until someone with the approve permission approves. Silent approval is possible. | FLA | https://raw.githubusercontent.com/flarum/framework/2.x/extensions/approval/src/Listener/ApproveContent.php | M | high |
| 137 | Anti-spam | Post flood throttle | One post, discussion or content edit per 10 s per user, unless the user has the "postWithoutThrottle" permission. Email activation resend every 5 min. | FLA | https://raw.githubusercontent.com/flarum/framework/2.x/framework/core/src/Post/PostCreationThrottler.php ; https://raw.githubusercontent.com/flarum/framework/2.x/framework/core/src/User/Throttler/EmailActivationThrottler.php | S | high |
| 138 | Anti-spam | Rate limits (Lemmy 0.16.7 defaults) | Post 6 per 600 s, comment 6 per 600 s, register 3 per 3,600 s, image 6 per 3,600 s, message 180 per 60 s, search 60 per 600 s. Newer versions store these in the database; current defaults unverified. | LEM | https://raw.githubusercontent.com/LemmyNet/lemmy/0.16.7/config/defaults.hjson ; https://raw.githubusercontent.com/LemmyNet/lemmy/main/crates/db_schema/src/source/local_site_rate_limit.rs | S | high |
| 139 | Anti-spam | New-user restrictions (SO) | Below 10 rep: at most 8 links per post or profile, no links in comments, no answers on protected questions, rate-limited posting. | SO | https://stackoverflow.com/help/privileges/new-user | S | high |
| 140 | Anti-spam | Silent question ban | Users with mostly poor questions are blocked from asking, with no public sign. It lifts automatically when positive contributions outweigh the poor ones, never by request. | SO | https://stackoverflow.com/help/question-bans | M | med |
| 141 | Anti-spam | Flags → auto-hide | Hiding is driven by a score sensitivity (`hide_post_sensitivity` default 6, an enum, not a count). A hidden user waits 10 min to edit and repost (`cooldown_minutes_after_hiding_posts: 10`). TL3 spam flags hide TL0 posts at once. A TL4 flag hides any post at once. | DSC | https://github.com/discourse/discourse/blob/main/config/site_settings.yml ; https://blog.discourse.org/2018/06/understanding-discourse-trust-levels/ | M | high |
| 142 | Anti-spam | Flags → auto-silence | A new user flagged by 3 different users is silenced (`num_users_to_silence_new_user: 3`). Flagging needs TL1. | DSC | https://github.com/discourse/discourse/blob/main/config/site_settings.yml | M | high |
| 143 | Anti-spam | Flags → auto-close topic | 5 flaggers (`num_flaggers_to_close_topic: 5`) close a topic. Reopens after 4 h (`num_hours_to_close_topic: 4`). | DSC | https://github.com/discourse/discourse/blob/main/config/site_settings.yml | S | med |
| 144 | Anti-spam | Reports → flag after X | Circle has two thresholds. "Flag a post after X reports" hides one item. "Flag all member activity after X reports" puts the member on moderation. A space's own admin report flags at once. | CIR | https://help.circle.so/p/administration/moderation/manage-moderation-settings | M | high |
| 145 | Anti-spam | Profanity / banned words | Words you list flag and hide member posts. Admins and mods are exempt. | CIR | https://help.circle.so/p/administration/moderation/manage-moderation-settings | S | med |
| 146 | Anti-spam | AutoMod keyword rules | Up to 6 keyword rules per server, each with up to 1,000 keywords (60 chars), 10 regex (260 chars) and an allow-list of 100. Actions: block (custom message up to 150 chars), alert to a mod channel, timeout (max 4 weeks), block interaction. | DCD | https://raw.githubusercontent.com/discord/discord-api-docs/main/developers/resources/auto-moderation.mdx ; https://support.discord.com/hc/en-us/articles/4421269296535-AutoMod-FAQ | M | high: block phone-number and "WhatsApp" spam |
| 147 | Anti-spam | Mention-spam limit | Blocks messages with more than N unique mentions (N up to 50). Mention-raid detection. | DCD | https://raw.githubusercontent.com/discord/discord-api-docs/main/developers/resources/auto-moderation.mdx | S | med |
| 148 | Anti-spam | Server verification levels | None. Verified email. Account older than 5 min. Member for more than 10 min. Verified phone. | DCD | https://raw.githubusercontent.com/discord/discord-api-docs/main/developers/resources/guild.mdx | S | high: "10 minutes before first post" is free friction |
| 149 | Anti-spam | Membership screening | New members join "pending" and are restricted until they accept the rules. | DCD | https://raw.githubusercontent.com/discord/discord-api-docs/main/developers/resources/guild.mdx | S | high |
| 150 | Anti-spam | Slowmode | A per-user cooldown per channel of 0–21,600 s. In forums it also limits thread creation. A Bypass Slowmode permission exempts roles. | DCD | https://support.discord.com/hc/en-us/articles/360016150952-Slowmode-FAQ ; https://raw.githubusercontent.com/discord/discord-api-docs/main/developers/resources/channel.mdx | S | med: for heated threads |
| 151 | Anti-spam | Timeout | A temporary mute: no messages, reactions or voice. The reason is logged. Others see messages as normal. | DCD | https://support.discord.com/hc/en-us/articles/4413305239191-Time-Out-FAQ | S | high |
| 152 | Anti-spam | Activity alerts + security actions | Unusual activity raises a banner or push to mods, who can pause invites and DMs in one tap. | DCD | https://support.discord.com/hc/en-us/articles/17439993574167-Activity-Alerts-Security-Actions | M | med |
| 153 | Anti-spam | Crowd Control | Collapses or filters comments and posts from users not yet trusted in the community. Moderate = negative community karma. Stricter levels add more signals. | RDT | https://support.reddithelp.com/hc/en-us/articles/15484545006996-Crowd-Control | M | high |
| 154 | Anti-spam | Reputation filter | Filters content from likely spammers using a sitewide "Contributor Quality Score" (karma, verification, account signals). Approved users are exempt. | RDT | https://support.reddithelp.com/hc/en-us/articles/27441485903124-Reputation-filter | L | high (as an idea: a site-wide trust score) |
| 155 | Anti-spam | Ban-evasion filter | Filters content from suspected alternate accounts of banned users. Time frame: past few weeks / months / this year. | RDT | https://support.reddithelp.com/hc/en-us/articles/15484544471444-Ban-evasion-filter | L | med |
| 156 | Anti-spam | Harassment filter (LLM) | An LLM filters likely harassing comments to the mod queue, at Moderate or High level, with an allow-list of up to 15 keywords. | RDT | https://support.reddithelp.com/hc/en-us/articles/23856209638932-Harassment-filter | L | med |
| 157 | Anti-spam | 10% self-promotion norm | Many communities let at most 10% of a member's activity be self-promotional. | RDT | https://support.reddithelp.com/hc/en-us/articles/28012014962580-How-do-I-keep-spam-out-of-my-community | S | high: the rule for brokers advertising |
| 158 | Moderation | Mod queue UX | Needs Review, Reported, Removed, Edited and Unmoderated tabs. Sort by oldest, newest or most reported. Keyboard shortcuts, user profile side panel. | RDT | https://support.reddithelp.com/hc/en-us/articles/15484440494356-Moderation-Queue | M | high |
| 159 | Moderation | Review queue reminders | Staff are reminded about unhandled review items after 48 h (`notify_about_reviewable_item_after: 48`). | DSC | https://github.com/discourse/discourse/blob/main/config/site_settings.yml | S | high |
| 160 | Moderation | Community review queues | Triage, First questions, First answers, Close, Reopen, Low quality, Suggested edits, Late answers. Reviewers can be suspended from reviewing. | SO | https://stackoverflow.com/help/review-queues | L | low early |
| 161 | Moderation | Public mod log | Removals and other mod actions appear in a log linked from every page. Lock, pin, community ban, site ban, purge. | LEM | https://join-lemmy.org/docs/users/04-moderation.html ; https://join-lemmy.org/ | M | med: transparency builds trust |
| 162 | Moderation | Suspend / silence | Suspend extension (Flarum). Silence and suspend (Discourse). Silenced users are kept from TL3 for 6 months. | FLA, DSC | https://github.com/flarum/framework/tree/2.x/extensions ; https://blog.discourse.org/2018/06/understanding-discourse-trust-levels/ | S | high |
| 163 | Moderation | Removed posts auto-deleted | Removed posts are deleted after 24 h (`delete_removed_posts_after: 24`). Hidden posts are deleted over time (`delete_old_hidden_posts: true`). | DSC | https://github.com/discourse/discourse/blob/main/config/site_settings.yml | S | med |
| 164 | Moderation | Audit log + GDPR tools | An audit log, plus GDPR erasure and export. | FLA | https://flarum.org/ | M | high: Israeli privacy law |
| 165 | Moderation | Lock thread | Locking stops new replies (Flarum Lock extension; Lemmy lock). | FLA, LEM, RDT | https://github.com/flarum/framework/tree/2.x/extensions ; https://join-lemmy.org/docs/users/04-moderation.html | S | high |
| 166 | SEO | Crawler HTML view | Crawlers get a server-rendered page (`crawler.html.erb`) with title, description meta and noscript header/footer partials. Per-topic content is in `topics/show.html.erb`. | DSC | https://github.com/discourse/discourse/blob/main/app/views/layouts/crawler.html.erb ; https://github.com/discourse/discourse/blob/main/app/views/topics/show.html.erb | M (WP renders server-side already) | high |
| 167 | SEO | Crawler page markup | BreadcrumbList, Person author with nofollow `/u/` link, datePublished/dateModified, LikeAction InteractionCounter, `itemprop="text"` per post. Hidden or empty posts are skipped. | DSC | https://github.com/discourse/discourse/blob/main/app/views/topics/show.html.erb | M | high |
| 168 | SEO | Google DiscussionForumPosting rules | Required: author.name, datePublished, and text/image/video. Recommended: url (the first page for multi-page threads), headline (never invented from the text), comment (nested), interactionStatistic, isPartOf, dateModified, and creativeWorkStatus "Deleted" for removed posts. Later pages repeat the original post. | Google | https://developers.google.com/search/docs/appearance/structured-data/discussion-forum | M | high |
| 169 | SEO | Google QAPage rules | One question per page, and users must be able to answer. Required: name, answerCount, and acceptedAnswer or suggestedAnswer. Answer needs text. upvoteCount and an answer url are recommended. Don't apply sitewide to ineligible pages. | Google | https://developers.google.com/search/docs/appearance/structured-data/qapage | M | high: use QAPage on "question" threads, DiscussionForumPosting on discussions |
| 170 | SEO | Solved schema | The Solved plugin emits schema "always" by default (`solved_add_schema_markup`). | DSC | https://github.com/discourse/discourse/blob/main/plugins/discourse-solved/config/settings.yml | S | high |
| 171 | SEO | ProfilePage | mainEntity Person/Organization with name required. dateCreated/dateModified recommended, plus interactionStatistic, agentInteractionStatistic, sameAs, image and description. | Google | https://developers.google.com/search/docs/appearance/structured-data/profile-page | S | high: pro profiles as E-E-A-T |
| 172 | SEO | rel=ugc / nofollow | User links nofollowed by default (`add_rel_nofollow_to_user_content: true`). TL3 links can be followed (`tl3_links_no_follow: false`). Google recommends `ugc` on forum links and allows dropping it for consistently trusted contributors. | DSC, Google | https://github.com/discourse/discourse/blob/main/config/site_settings.yml ; https://developers.google.com/search/docs/crawling-indexing/qualify-outbound-links | S | high |
| 173 | SEO | Sitemap | On by default, 10,000 URLs per sitemap page. | DSC | https://github.com/discourse/discourse/blob/main/config/site_settings.yml | S | high |
| 174 | SEO | Non-Latin slugs | `slug_generation_method` is ascii (default), encoded, or none. ja/zh default to "none". For Hebrew, "encoded" keeps Hebrew words in the URL; "ascii" drops them. | DSC | https://github.com/discourse/discourse/blob/main/config/site_settings.yml ; https://github.com/discourse/discourse/blob/main/app/models/slug_setting.rb | S | high: decide before launch, slugs are forever (no-redirect law) |
| 175 | SEO | Thin / empty content handling | Crawler view skips hidden posts and posts with empty content. Very long topics auto-close at 10,000 posts and open a linked continuation topic. | DSC | https://github.com/discourse/discourse/blob/main/app/views/topics/show.html.erb ; https://github.com/discourse/discourse/blob/main/config/site_settings.yml | M | med |
| 176 | Realtime | "X is replying" presence | Names of people replying or editing show under the topic, up to 5 shown (`presence_max_users_shown: 5`). On by default. | DSC (discourse-presence) | https://github.com/discourse/discourse/blob/main/plugins/discourse-presence/config/settings.yml | L | high: the strongest "alive" signal |
| 177 | Realtime | Typing indicator + live updates | A typing indicator in discussions (and optionally the discussion list). New discussions, replies, notifications and removals appear live, with updates batched every 10 s. | FLA (Realtime) | https://flarum.org/ ; https://raw.githubusercontent.com/flarum/framework/2.x/extensions/realtime/extend.php | L | high |
| 178 | Realtime | Live chat | Realtime chat channels. | DSC, DCD | https://www.discourse.org/features | L | med |
| 179 | Realtime | Hide presence | Users can hide their presence (`default_hide_presence: false`). | DSC | https://github.com/discourse/discourse/blob/main/config/site_settings.yml | S | med: privacy |
| 180 | Access & RTL | Real RTL | RTL for ar, fa_IR, **he**, ug and ur. Uses the site default locale, or the user's locale if per-user locale is allowed. A `client.he.yml` translation exists. | DSC | https://github.com/discourse/discourse/blob/main/lib/rtl.rb | n/a | high: proof Hebrew RTL works in a mature forum |
| 181 | Access & RTL | WCAG and dark mode | A WCAG-compliant colour scheme and dark mode. | DSC, FLA (dark mode), LEM (themes) | https://www.discourse.org/features ; https://flarum.org/ ; https://join-lemmy.org/ | M | high |
| 182 | Access & RTL | Keyboard shortcuts | Shortcut keys include `?`, `/`, `=`, `.`, `!`, `#`, `g h`, `g l`, `g n`, `g u`, `g t`, `g b`, `g j/k`, `m m/r/t/w` (mute/regular/track/watch), `shift+j/k`, `shift+r`, `shift+s`, `shift+a`, `shift+b`, `shift+d`, `o/enter`, `ctrl+alt+f`. Actions inferred from key names only. | DSC | https://github.com/discourse/discourse/blob/main/frontend/discourse/app/services/keyboard-shortcuts.js | S | low (phones first) |
| 183 | Access & RTL | Full keyboard navigation | Tab/arrow navigation with a focus ring across the desktop app. | DCD | https://support.discord.com/hc/en-us/articles/1500000056121-Keyboard-Navigation-FAQ | M | med |
| 184 | Access & RTL | Mobile specifics | The search box sits in mobile navigation, menus open on the first tap, and haptic feedback is optional. | FLA | https://flarum.org/ | S | high |
| 185 | Access & RTL | Browser support target | Latest stable browsers. Safari on iOS 16.4+. | DSC | https://github.com/discourse/discourse | n/a | med |
| 186 | Monetisation | Paid subscriptions | Stripe subscriptions, a pricing table, crowdfunding campaign banner and goal, automatic tax. USD by default. Off by default. | DSC (discourse-subscriptions) | https://github.com/discourse/discourse/blob/main/plugins/discourse-subscriptions/config/settings.yml | M | high: "Pro" tier for brokers |
| 187 | Monetisation | Ads and affiliate | Bundled ad plugin (AdSense etc.) and an affiliate plugin. Patreon login/integration. | DSC | https://github.com/discourse/discourse/tree/main/plugins ; https://www.discourse.org/features | S | low |
| 188 | Monetisation | Paywalls | One-time, subscription and installment pricing. Buy-now-pay-later. Coupons and auto-applied coupon links. Gate individual spaces. Upsells. Stripe. | CIR | https://help.circle.so/p/payments/paywall-setup | M | high: gate a "verified pros" room |
| 189 | Monetisation | Server subscriptions | Role subscriptions can be purchased (ROLE_SUBSCRIPTIONS_* guild features). | DCD | https://raw.githubusercontent.com/discord/discord-api-docs/main/developers/resources/guild.mdx | M | med |
| 190 | Monetisation | Paid awards | Gold-funded awards; recipients can earn via the Contributor Program. | RDT | https://support.reddithelp.com/hc/en-us/articles/26465598697876-What-are-awards-and-how-do-I-use-them | L | low |
| 191 | Monetisation | Jobs, advertising, reduced ads | Help-centre sections "Stack Overflow Jobs" and "How do I advertise". At 200 rep "some ads are now automatically disabled". Job-board mechanics not opened (unverified). | SO | https://stackoverflow.com/help/privileges ; https://stackoverflow.com/help/editing | M | med: "fewer ads at level X" is a neat reward |

**Row count: 191.**

---

## (a) The 25 micro-features that most create a feeling of life and ease

1. **"X is replying…" under the thread.** Up to 5 names, on by default (DSC presence). Flarum shows a typing indicator.
2. **Live insertion of new replies and new threads**, batched every few seconds (FLA Realtime, every 10 s).
3. **Draft autosave with "tap to resume"** on phones (DSC).
4. **Quote by highlighting text**, one tap (DSC).
5. **Link previews (onebox)** for pasted listings, gov.il and YouTube links (DSC).
6. **Paste or drag an image straight into the composer** (DSC, LEM).
7. **"Your topic is similar to…" while typing the title** (DSC), which prevents empty duplicates.
8. **Unread/new counts and "jump to last read"**, so a visitor sees there is something new (DSC).
9. **5-minute silent-edit grace**: fixing a typo adds no history (DSC).
10. **Accepted answer pinned under the question**, with a check mark (DSC Solved, SO).
11. **Likes and a small positive reaction set**, with no visible downvotes (DSC Reactions).
12. **Visible view "heat" and reply counts on the list** (DSC).
13. **User card on tap** showing role flair, level and progress (DSC, CIR).
14. **Role flair next to names**: broker, appraiser, lawyer (RDT user flair, 350 templates).
15. **Verified checkmark** for licensed professionals (RDT verified profiles).
16. **Points for likes and solutions, 9 levels, weekly leaderboard showing the top 10** (CIR; DSC gamification weights).
17. **One-tap per-thread "watch / track / mute"** (DSC levels).
18. **Weekly digest that skips itself when there is nothing new** (CIR: fewer than 2 posts, no email).
19. **Web push on phones**, with the prompt on by default (DSC).
20. **Onboarding questions** ("I am a broker / investor / appraiser") that set what you see (DCD).
21. **Welcome screen with up to 5 suggested places to start** (DCD).
22. **Magic-link email login and passkeys**, with no password (DSC).
23. **Read without logging in, plus a sign-up nudge only after reading** (DSC `login_required: false`, `enable_signup_cta`).
24. **Pinned highlights carousel with labels** (Event / Megathread / Announcement, up to 6; RDT).
25. **Scheduled recurring threads** (for example a weekly "deals and questions" thread), so the forum never looks empty (RDT).

---

## (b) Anti-spam defaults worth copying (real numbers, with sources)

**Discourse.** All values are defaults in https://github.com/discourse/discourse/blob/main/config/site_settings.yml unless another source is named.

New users (TL0):
- 2 links, 5 embedded media, 0 attachments and 2 @mentions per post; 3 replies per topic.
- First day: at most 3 topics and 10 replies.
- Any of the user's posts: min 20 chars, title min 15 chars, title entropy 10, body entropy 7.

Rates:
- 15 s between topics, 5 s between posts, 30 s between posts for new users.
- 20 topics/day. An identical post is refused within 5 min.

Daily caps:
- 50 likes, 20 flags, 30 edits, 10 invites, 20 PMs, 20 bookmarks.
- TL2 gets ×1.5, TL3 ×2 and TL4 ×3 (https://blog.discourse.org/2018/06/understanding-discourse-trust-levels/).

Links:
- 3 posts to the same host by a new user trips spam-host detection.
- User links are nofollow, with an allow/block domain list.

Signup:
- At most 3 accounts per IP.
- Logins 6 per minute and 30 per hour per IP.
- mailinator.com blocked.
- Email token valid 48 h.
- Honeypot + challenge that returns a *fake success* to bots (https://github.com/discourse/discourse/blob/main/app/controllers/users_controller.rb).

Flags:
- Flagging needs TL1.
- 3 distinct flaggers silence a new user.
- A hidden poster waits 10 min.
- 5 flaggers close a topic, which reopens after 4 h.
- TL3 spam flags hide TL0 posts at once; a TL4 flag hides any post.

Trust promotion:
- TL1 = 5 topics entered, 30 posts read, 10 min reading.
- TL2 = 15 days visited, give 1 like, receive 1 like, 3 topic replies, 20 topics, 100 posts, 60 min.

Plugins:
- **Akismet** checks users below TL1 and skips users with more than 50 posts. A TL1 user's first post goes to review. Runs every 10 min (https://github.com/discourse/discourse-akismet/blob/main/config/settings.yml).
- **AI spam scan** covers the first 3 posts of users at TL1 or below, off by default (https://github.com/discourse/discourse/blob/main/plugins/discourse-ai/config/settings.yml).
- **reCAPTCHA v3** threshold 0.5, off by default (https://github.com/discourse/discourse/blob/main/plugins/discourse-captcha/config/settings.yml).

**Stack Overflow**
- Below 10 rep: at most 8 links per post or profile, and no links in comments (https://stackoverflow.com/help/privileges/new-user).
- Flagging and upvoting need 15 rep (https://stackoverflow.com/help/privileges).
- 4 spam/offensive flags on a post cost the author −100 (https://stackoverflow.com/help/whats-reputation).
- Question bans are silent and lift automatically (https://stackoverflow.com/help/question-bans).

**Flarum**
- One post, discussion or content edit per 10 s per user (https://raw.githubusercontent.com/flarum/framework/2.x/framework/core/src/Post/PostCreationThrottler.php).
- Activation email resend every 5 min.
- Akismet learns from hide (spam) and approve (ham).

**Lemmy** (0.16.7 config file; current versions keep these in the database, current defaults unverified, https://raw.githubusercontent.com/LemmyNet/lemmy/0.16.7/config/defaults.hjson):
- Posts 6 per 10 min, comments 6 per 10 min.
- Registrations 3 per hour, images 6 per hour.
- Messages 180 per minute, searches 60 per 10 min.
- Email verification and a registration application with a question.

**Discord**
- Verification levels: verified email, account older than 5 min, member for more than 10 min, verified phone.
- Slowmode 0–21,600 s.
- AutoMod (https://raw.githubusercontent.com/discord/discord-api-docs/main/developers/resources/auto-moderation.mdx):
  - Up to 6 keyword rules × 1,000 keywords each, plus 10 regex.
  - Mention-spam cap up to 50.
  - Block message up to 150 chars.
  - Timeout up to 4 weeks.

**Circle** (https://help.circle.so/p/administration/moderation/manage-moderation-settings):
- First post/comment approval.
- Moderate a member after a rejection.
- "Flag post after X reports" and "flag all member activity after X reports" (X set by the admin, no default published).
- Profanity filter.

**Reddit**
- Crowd Control (negative community karma → collapse/filter).
- Reputation filter on a sitewide Contributor Quality Score.
- Ban-evasion filter.
- LLM harassment filter with a 15-keyword allow-list.
- The "10% self-promotion" norm.
- Sources: https://support.reddithelp.com/hc/en-us/articles/28012014962580-How-do-I-keep-spam-out-of-my-community and the linked filter articles.

**Suggested starting bundle for the portal** (judgement, built from the above):
- Honeypot + time challenge with fake success.
- One-tap magic link or Google sign-in.
- First post held for approval (Circle model).
- TL0 limits copied from Discourse: 2 links, 0 attachments, 3 topics and 10 replies on day one.
- 30 s between posts for new users.
- Same-host link counter set to 3.
- Akismet on everyone below "member" level.
- A phone-number/WhatsApp/URL keyword rule that holds the post (Discord AutoMod idea).
- 3 distinct flags silence a new user.
- All user links `rel="ugc nofollow"`, lifted for verified professionals.

---

## (c) Not checked / blocked

- **meta.discourse.org**: a robot check ("Checking your browser…", HTTP 403) appeared in the browser, and WebFetch also got 403. Blocked, not checked. Every Discourse row instead uses source code, discourse.org/features, the official blog and plugin settings files.
- **Stack Exchange network sites other than stackoverflow.com** (meta.stackexchange.com, superuser.com): the fetch tool refused them, and they were not retried. Not checked. All SO rows come from stackoverflow.com/help pages opened in the browser.
- **SO Staging Ground details**: the guessed article URL returned 404; only the index page was seen. Not checked.
- **SO "similar questions while asking"** and **SO Jobs mechanics**: not opened (unverified).
- **reddit.com/wiki/automoderator** (full AutoModerator docs): the fetch tool refused it, and it was not retried. Not checked. Only the help-centre titles were seen (an "Automoderator" and a "Full automoderator documentation" article).
- **circle.so/features**: HTTP 406, not checked. Circle magic-link login, RTL, SEO, AI moderation, push and DM details: not checked (only the help-centre pages listed in the table were read).
- **Discord RTL / Hebrew support**, typing indicator documentation, and the Server Subscriptions creator article (a pointer page only): not checked.
- **Flarum RTL**, composer behaviour (docked while browsing), mentions/subscriptions/flags extension internals: not checked (only the extension list, the realtime/akismet/approval wiring and the throttle code were read).
- **Lemmy current-version rate-limit defaults** (stored in the database since newer versions), the ranking formula page and registration-application details in the docs: not checked.
- **Discourse**: these are present in code, but their exact UI behaviour was not seen on a live site:
  - Composer draft save interval.
  - Similar-topics UI details.
  - Timeline scrubber behaviour.
  - Exact keyboard shortcut meanings.
  - Flag score maths (`hide_post_sensitivity` is an enum, not a flag count).
  - `personal_message_enabled_groups` default.
  - Whether a per-topic estimated read time exists (not found).
- **Accessibility audits** of any product: not done. Only vendor claims are recorded.
