# Owner emails: how the best products design alerts and digests

Research date: 8.11.2026. Every URL below was "read 8.11.2026".
Scope: evidence for the nad-lan.co.il owner mail design (instant lead email, signed action buttons, 08:00 digest).
All text is paraphrased. Where a fact came from a search-result summary and not from a page I opened in full, it is marked **(search only)**. Where a number comes only from a vendor's own marketing or study it is marked **(vendor)**.

---

## 1. Product practice

### 1.1 Stripe
- Each team member sets their own email preferences under "Communication preferences"; teammates do not inherit yours. Events include successful payments, disputes and elevated-risk payments. https://docs.stripe.com/account/teams (search only), https://support.stripe.com/questions/set-up-account-email-notifications (search only)
- The Dashboard home surfaces unresolved disputes and verification tasks, so the email is not the only place to see them. https://docs.stripe.com/dashboard/basics (search only)
- Scheduled report emails (daily/weekly/monthly) are mentioned only by a third-party write-up; I did not confirm a built-in daily summary toggle in Stripe's own docs. https://www.putler.com/?p=185446 (search only)
- Gap: no evidence of signed actions from the email itself; the email leads to the Dashboard.

### 1.2 Shopify
- Staff order emails: recipients are added under Settings > Notifications; a recipient can be paused instead of deleted; a notification can be limited to a given POS location or the web channel. https://help.shopify.com/manual/orders/notifications/order-notifications (search only), https://community.shopify.com/t/how-do-i-receive-email-notifications-for-online-orders/93013 (search only)
- The Shopify app also has a staff-notification settings path (Menu > Settings > Notifications > Staff notifications) where the New order template is edited. https://help.shopify.com/en/manual/orders/notifications/order-notifications (search only)
- A summary email with a Daily or Weekly frequency choice is referenced in the search summary of Shopify's notification help. https://help.shopify.com/manual/orders/notifications (search only)
- Gap: I found no evidence of one-tap actions inside the email, nor a per-type mute from the email.
- Community threads show owners complaining that order emails do not arrive (spam folder, missing recipients), which is a delivery-reliability signal. https://community.shopify.com/t/why-am-i-not-receiving-staff-order-notifications-via-email/102044 (search only)

### 1.3 Linear
- Notification format can be chosen per user: digest or immediate. By default notifications are grouped into digests by urgency, and a digest waits a delay that depends on factors such as issue status. https://linear.app/docs/notifications
- A digest is sent only if the notification has not already been read in the Linear inbox. Same page.
- Individual types can be switched on or off per channel (some types come in groups that cannot be split). Same page.
- A single issue can be unsubscribed with a keyboard shortcut. Same page.
- The page does not cover reply-by-email or snooze, so I record those as unknown, not as absent.

### 1.4 GitHub
- Each notification email states in its footer why you got it (mention, team mention, and so on), and the same reason is exposed as a CC address and in the `X-GitHub-Reason` header for filtering. https://github.blog/news-insights/the-library/improvements-to-notification-emails/ (article from 2016, last updated 2019)
- A conversation can be muted from the email itself, but only in clients that render HTML. Same page.
- A real message from a mailing-list archive shows a `List-Unsubscribe` header with both a mailto address and an https notifications/unsubscribe URL. https://mail.python.org/archives/list/python-committers@python.org/message/OCVQ6IYOVTVYW7ADDNOHKR7JDRBYLM3T (search only)
- Header documentation (Enterprise Server edition): headers are consistent so mail clients can filter or forward. https://docs.github.com/en/enterprise-server@3.17/subscriptions-and-notifications/reference/email-notification-headers (search only)
- Reply-by-email: not confirmed by the sources I could open.

### 1.5 HubSpot
- Each user sets notification preferences in Settings > Notifications, with an Email column per activity (new leads, assigned tasks, ticket updates). https://knowledge.hubspot.com/settings/how-to-set-up-user-notifications-in-hubspot (search only)
- The weekday sales digest: compiled at 06:00, emailed at 08:00 in the account time zone; it lists the day's meetings, each with a "View meeting" button. It is NOT sent when there are no meetings, and it is on by default only for users with a Sales seat who completed at least three tasks in the last 17 days. https://knowledge.hubspot.com/prospecting/receive-a-summary-of-your-sales-activity-every-weekday
- Lead-revisit alerts (a daily email per contact who visited the site) need a Marketing Hub Professional or Enterprise plan. https://knowledge.hubspot.com/user-management/set-up-lead-revisit-notifications (search only)
- "Log a call from the email": no source found; recorded as unknown.

### 1.6 Salesforce
- I found no native daily lead digest in the sources. A Trailhead community post asks for exactly that (one daily summary of new open leads instead of one email per lead), which suggests it is a common request. https://trailhead.salesforce.com/fr/trailblazer-community/feed/0D54S00000A8fH7SAJ (search only)
- Assignment emails to lead owners exist through rules and apps; the Oracle documentation (a different vendor) describes a link appended to open the lead, so it is not evidence about Salesforce. https://docs.oracle.com/en/cloud/saas/sales/fasqa/how-do-i-notify-a-lead-owner-by-email-when-a-lead-is-assigned-to-them.html (search only)
- Mobile push depends on the app's push setting and Notification Delivery Settings. https://plauti.com/support/en_US/getting-started/sf-srr-send-notifications-on-assignment (search only, third party)
- Treat Salesforce as mostly unknown for this research.

### 1.7 Zillow Premier Agent
- Zillow dropped the automated "text-to-call" alert; agents still get email, push and text for a new lead, and a phone call only when a live connection is ready. https://www.zillow.com/premier-agent/pa4-more-leads-more-control (search only)
- Instant alerts need push enabled on the phone; the email goes to the profile address. https://www.zillow.com/agents/app-overview/ (search only)
- Team leaders can set a reminder when a lead stays in "New" status too long, for example 30 minutes. https://www.zillow.com/premier-agent/team-reminders-accountability (search only)
- Zillow publishes no required response window that I could find; claims that Zillow routes more leads to faster agents come from vendors and are unverified. https://followupace.com/learn/zillow-leads-playbook/response-time/ (vendor)
- Agent complaints: weak lead quality, and Zillow's answer that agents follow up too slowly; a 2018 trade report quoted Zillow's then-CEO saying consumers said they never heard back about half the time. https://www.inman.com/2018/11/27/this-blows-my-mind-agents-balk-at-return-of-zillow-unvetted-leads/ (search only), https://jefflenney.com/real-estate/is-zillow-premier-agent-worth-it/ (search only, agent blog)

### 1.8 Follow Up Boss
- On assignment of a new lead the user gets an email and a text (text works only if a phone number is saved); email goes to the login address; desktop and mobile push also exist. https://help.followupboss.com/hc/en-us/articles/360015270813 (search only), https://support.bramlettpartners.com/article/900-fub-how-to-adjust-or-turn-off-lead-notifications (search only, third party)
- Android users are told to exempt the app from battery sleeping so pushes arrive. Same help area. (search only)
- In 2025-26 the vendor announced a new notification system aimed at dependable delivery and more control over which alerts arrive; the post does not list alert contents. https://updates.followupboss.com/en/never-miss-an-alert-a-stronger-foundation-for-notifications
- Reviews: one reviewer says notifications sometimes fail to arrive even when enabled; I found no "too many notifications" complaint in the review summaries. https://www.capterra.com/p/130020/Follow-Up-Boss/reviews/ (search only)

### 1.9 kvCORE / BoldTrail
- New-lead email (default): lead name, contact details, registration source, and the property they signed up on if any. Text is optional via the app. https://help.insiderealestate.com/en/articles/11953440-boldtrail-new-lead-notifications (search only)
- Behavioural alerts ("Streams"): triggers include viewing five properties in a day, ten in a week, returning to the same listing three times, favouriting a property. Texts are the default, email is the fallback when no phone is on file. https://help.insiderealestate.com/en/articles/13170400-boldtrail-streams (search only; thresholds may be outdated)
- Each Streams card has one-tap call (through a managed number), text and email buttons; the card clears once the agent makes a personal call, text or email. Same page. (search only)
- The text shortcut shows only when the contact opted in to texts. Same page.

---

## 2. Gmail actions, AMP, one-click unsubscribe, link scanners

### 2.1 Gmail email markup actions (schema.org ConfirmAction and friends)
- Google's reference still documents the one-click confirm action: Gmail sends an HTTP request to the handler URL you declare; a ConfirmAction can be used only once. The page I opened carries no deprecation notice; I found no 2025-26 announcement either way. https://developers.google.com/workspace/gmail/markup/reference/one-click-action
- Registration page: needs a steady record of high-volume mail to Gmail (roughly hundreds a day for a few weeks), very low spam complaints, DKIM or SPF aligned with the From domain, a static sender address, and a real production email (not a test) sent directly to Google's review address and validated in the Email Markup Tester; then submit the form. https://developers.google.com/workspace/gmail/markup/registering-with-google
- Third-party guides say the volume bar is about 100 mails a day for several weeks and add DMARC. https://www.suped.com/knowledge/email-deliverability/technical/how-do-i-register-with-gmail-for-email-markup (search only)
- Verdict for a single-recipient owner mail: the volume requirement cannot be met by one alert stream to one inbox, so registration is not realistic. Without registration Gmail ignores the markup for other people's mail (own-account testing works only for the sender's own address, per the tester guidance in the same Google page family).

### 2.2 AMP for Email
- Registration is per sender address (not per domain), once; send a real production dynamic email with a matching HTML or text fallback to Google's review address, then submit the form; Google aims to answer within about five working days. Requires SPF, DKIM and DMARC, low spam complaints, and a live legitimate root-domain website. Third parties may not author the emails; Google can revoke at any time. https://developers.google.com/workspace/gmail/ampemail/register
- Mechanics: the AMP part is `text/x-amp-html` inside `multipart/alternative`, placed before the HTML part; forwarding or replying strips it, so the HTML part must stand on its own. https://amp.dev/documentation/guides-and-tutorials/integrate/add-email/ (search only)
- Form posts must use `action-xhr`; one vendor's documentation says XHR endpoints must not answer 302 and must be on the same domain zone as the sender. https://docs.actionkit.com/docs/manual/guide/mailings-amp.html (vendor, search only)
- Client support is limited to Gmail, Yahoo Mail, Mail.ru and a few others; Yahoo and Mail.ru also run their own sender registration. https://www.mailmodo.com/guides/register-amp-email/ (vendor, search only), https://amp.dev/support/faq/email-support/ (search only)
- Brevo: I found no Brevo documentation that mentions AMP, and Brevo is absent from the AMP provider lists I saw. Brevo's transactional API takes HTML, text or a template id. Verdict: unconfirmed, probably unsupported; must be asked of Brevo support before any plan relies on it. https://developers.brevo.com/reference/send-transac-email (search only), https://amp.dev/support/faq/email-support/ (search only)

### 2.3 RFC 8058 one-click unsubscribe and why POST
- Anti-spam software often fetches every URL in message headers, so a GET on an unsubscribe link could act without the person knowing; the standard therefore uses an HTTPS POST that automated fetchers do not normally send. https://www.rfc-editor.org/rfc/rfc8058
- Requirements: `List-Unsubscribe` with an https URI, `List-Unsubscribe-Post` with the one-click value, a hard-to-forge identifier in the URI, no cookies or login in the POST, no redirect response, and a DKIM signature that covers both headers. Same page.
- Practitioner reports of scanners silently opting out thousands of contacts through GET links exist but are anecdotal. https://www.suped.com/learn/email-deliverability/how-should-one-click-unsubscribe-links-handle-get-vs-post-requests (search only)

### 2.4 Link scanners (Microsoft Defender Safe Links, Gmail scanning)
- Safe Links rewrites URLs and checks them at click time; community reports say the scanner can open a link before the person does and thereby consume a one-time URL. A 2019 Microsoft Tech Community thread and an Auth0 community post (fix was a Safe Links exception) describe this. Anecdotal; I found no current Microsoft page that states prefetch behaviour for one-time links. https://techcommunity.microsoft.com/t5/office-365/o365-url-scan-safe-links-impact-to-one-time-url/m-p/977132 (search only), https://community.auth0.com/t/safelink-process-with-microsoft-outlook/142113 (search only)
- Advice from deliverability sources: GET shows a page, a human-triggered POST changes state. https://www.suped.com/learn/email-deliverability/how-can-i-prevent-microsoft-defender-from-triggering-unwanted-one-click-unsubscribes (vendor, search only)
- The best primary source for the principle is RFC 8058's own rationale (section 2.3).

---

## 3. Research and industry studies

### 3.1 Email and notification load
- Dabbish and Kraut, CSCW 2006, "Email overload at work: an analysis of factors associated with email strain": defines overload as the feeling that email use is out of control and builds an initial scale for email overload and perceived work importance of email. I could not open the full text; effect sizes are unverified. https://dx.doi.org/10.1145/1180875.1180941 (search only)
- Kushlev and Dunn 2015, "Checking email less frequently reduces stress": field experiment, 124 adults, limited to three checks a day for a week; lower stress on the limited days; participants found the limit hard to keep. https://www.interruptions.net/literature/Kushlev-ComputHumBehav15.pdf (search only)
- Mark, Iqbal, Czerwinski, Johns, Sano, CHI 2016, "Email duration, batching and self-interruption": more daily time on email went with lower rated productivity and higher stress; people who chose when to check (not notification-driven) rated their day more productive; one secondary source reports no evidence that batching lowers stress. Full text not opened. https://www.microsoft.com/en-us/research/wp-content/uploads/2016/06/Email20Duration20Camera20Ready20submission3-1.pdf (search only), https://www.cmswire.com/social-business/how-are-we-coping-with-technology-in-the-digital-workplace (secondary)
- Pielot, Church, de Oliveira, MobileHCI 2014: a one-week study of 15 users counted an average of about 63.5 notifications a day, mostly messengers and email. https://ic.unicamp.br/~oliveira/doc/MHCI2014_An-in-situ-study-of-mobile-phone-notifications.pdf (search only)
- Mehrotra et al., CHI 2016, "My Phone and Me": 10,372 notifications from 20 users; studies how cognitive and physical factors affect response time and perceived disruption. https://discovery.ucl.ac.uk/1502364/1/CHI16.pdf (search only)
- Not found in this pass: Dabbish et al. 2005 "Understanding email use" and Iqbal and Horvitz notification papers (no sources retrieved).
- Reading for design: the evidence supports fewer, self-paced, relevant interruptions, but it does not prove that a digest lowers stress (the 2016 study is mixed), so the design should be tested, not assumed.

### 3.2 Lead response time
- InsideSales.com and MIT (Oldroyd) Lead Response Management Study, 2007: six companies, over 15,000 web leads, over 100,000 call attempts. Odds of contacting a lead called within 5 minutes were about 100 times those at 30 minutes; odds of qualifying about 21 times. A 5 to 10 minute delay cut odds roughly 4-5 times. Secondary summaries only; I did not locate the original report. The study was co-run with a vendor. (vendor) https://www.real-estate.ca/blog/the-lead-response-management-study (search only), https://www.mortech.com/hs-fs/hub/25649/file-13535879-pdf/docs/mit_study.pdf (search only)
- Oldroyd, McElheran, Elkington, HBR March 2011 "The Short Life of Online Sales Leads": 2,241 US companies were sent a test web lead; among firms that replied within 30 days the average reply time was 42 hours; reported shares: about 37 percent within an hour, 16 percent within 24 hours, 23 percent never replied. A "7 times more likely to qualify within an hour" figure appears in secondary sources only. https://scholarsarchive.byu.edu/facpub/9711 (search only), https://ainora.lt/blog/lead-response-time-statistics-every-study-2026 (secondary)
- Caution: the 100x and 21x multipliers belong to the 2007 study, not the HBR paper, and a later infographic turned "4 times" into "400 percent" (a misreading). https://www.leadsigma.com/resources/blog/five-minute-lead-response-stat.md (search only)
- No newer independent replication or real-estate-specific NAR or Zillow figure was verified; claims of a NAR 2025 average were not confirmed. https://www.usecarly.com/blog/speed-to-lead-statistics/ (vendor)

---

## 4. What real people say

Reddit, Hacker News and BiggerPockets threads did not return usable results in this pass (HN search returned only unrelated Show HN items). What I could read is thin, so this section is mostly "unknown".
- Follow Up Boss reviewers: praise for timely lead-activity notifications; one complaint of notifications not arriving. https://www.getapp.com/real-estate-property-software/a/follow-up-boss/ (search only), https://www.capterra.com/p/130020/Follow-Up-Boss/reviews/ (search only)
- Shopify merchants: repeated "I am not receiving order notification emails" threads. https://community.shopify.com/t/order-notifications-via-email-not-working/342028/3 (search only)
- Zillow agents: low lead quality; a coaching blog says nobody can answer in 5 minutes while showing homes or asleep. https://callingly.com/blog/how-to-follow-up-with-zillow-leads-before-they-ghost-you (vendor, search only)
- Salesforce users: ask for one daily summary instead of one email per lead (section 1.6).
- HN: a small Show HN named "A News Service That Almost Never Emails You (By Design)" shows interest in low-frequency mail but is not evidence. https://www.notably.news/ (search only)
- Open item: the owner-complaint theme "useless nagging" has no direct source here; it should be tested with Ben's own inbox data.

---

## Requirements

Each is testable. "Backed by" lists the evidence sections above.

- **R1. Lead alert reaches the owner within 60 seconds of form submit (measured, logged).** Backed by 3.2 (5-minute odds, 42-hour average), 1.7 (30-minute reminder), 1.9.
- **R2. The alert contains who, phone, source page, what they looked at, and a heat score, in a fixed order, the same for every lead.** Backed by 1.9 (name, contact, source, property).
- **R3. The phone number is a `tel:` link in a button at least 48 px high, readable without zoom on a 360 px screen.** Backed by 1.9 (one-tap call).
- **R4. A WhatsApp button opens a chat with a ready, editable message that names the property or page.** Backed by 1.9 (text shortcut); no source for WhatsApp itself.
- **R5. No link in the email changes state on GET; every action opens a confirm page and changes state only on POST.** Backed by 2.3, 2.4.
- **R6. Action links carry a signed, hard-to-forge token bound to one lead and one action, with an expiry; the POST needs no login or cookie.** Backed by 2.3 (opaque identifier, no cookies).
- **R7. Actions offered: contacted, not relevant, remind me tomorrow, mute this alert type.** Backed by 1.3, 1.4 (mute from email), 1.9 (card clears after response).
- **R8. Mute works per alert type and is visible: each email says which type it is and how to undo the mute.** Backed by 1.3, 1.4.
- **R9. Every email has a one-line reason ("you get this because...") in the footer.** Backed by 1.4.
- **R10. Marketing-style bulk headers are not needed for a single owner, but if `List-Unsubscribe` is added it follows RFC 8058: https URI, one-click POST header, DKIM covering both, no redirect.** Backed by 2.3, 1.4.
- **R11. The morning digest is not sent when nothing is new or urgent.** Backed by 1.5 (not sent with no meetings).
- **R12. The digest leaves out items the owner already handled or saw.** Backed by 1.3 (digest only if unread).
- **R13. The digest is sent at a fixed local time (08:00 Israel time, daylight saving handled) and never twice for the same content.** Backed by 1.5.
- **R14. Digest layout: urgent items first, one action per line, then yesterday-vs-today numbers (leads, sign-ups, Search Console traffic, revenue) with the unit and date range stated.** Backed by 1.5 (buttons per line); numbers layout has no external source, so it must be reader-tested.
- **R15. An unanswered lead triggers one escalation reminder after a set time (default 30 minutes), then stops.** Backed by 1.7 (30-minute "New" reminder).
- **R16. Bursts collapse: at most a set number of instant emails per hour; extra leads roll into one grouped email.** Backed by 3.1 (notification load), 1.3 (grouping).
- **R17. A lead marked contacted or not relevant cancels pending reminders and does not appear in the next digest.** Backed by 1.9 (card clears), 1.3.
- **R18. Delivery is monitored: failed or bounced owner emails raise a visible error, and a daily heartbeat check confirms the system sent mail.** Backed by 1.2 and 1.8 (non-arrival complaints).
- **R19. The email works with no Gmail markup and no AMP: plain HTML and a plain-text part carry every action as a normal link.** Backed by 2.1, 2.2 (registration volume, per-address, Brevo unconfirmed).
- **R20. Time from alert to first owner action is recorded per lead and appears in the digest.** Backed by 3.2 (response speed matters), 1.7 (status reminders).

---

## Matrix

Cells: Yes / Partial / No / Unknown, only from evidence above. "Unknown" means no evidence found, not "absent".

| Req | Stripe | Shopify | Linear | GitHub | HubSpot | Salesforce | Zillow PA | Follow Up Boss | kvCORE |
|---|---|---|---|---|---|---|---|---|---|
| R1 alert within 60 s | Unknown | Unknown | Unknown | Unknown | Unknown | Unknown | Partial | Unknown | Unknown |
| R2 fixed content (who, source, interest) | Unknown | Unknown | Unknown | Unknown | Unknown | Unknown | Unknown | Unknown | Yes |
| R3 big tap-to-call | Unknown | Unknown | Unknown | Unknown | Unknown | Unknown | Unknown | Unknown | Partial |
| R4 WhatsApp ready message | Unknown | Unknown | Unknown | Unknown | Unknown | Unknown | Unknown | Unknown | Partial |
| R5 GET safe, POST changes state | Unknown | Unknown | Unknown | Unknown | Unknown | Unknown | Unknown | Unknown | Unknown |
| R6 signed token, no login | Unknown | Unknown | Unknown | Unknown | Unknown | Unknown | Unknown | Unknown | Unknown |
| R7 actions from the email | No | Unknown | Unknown | Partial | Partial | Unknown | Unknown | Unknown | Partial |
| R8 per-type mute | Partial | Partial | Partial | Yes | Partial | Unknown | Unknown | Partial | Partial |
| R9 reason line | Unknown | Unknown | Unknown | Yes | Unknown | Unknown | Unknown | Unknown | Unknown |
| R10 List-Unsubscribe one-click | Unknown | Unknown | Unknown | Yes | Unknown | Unknown | Unknown | Unknown | Unknown |
| R11 digest not sent when empty | Unknown | Unknown | Unknown | Unknown | Yes | Unknown | Unknown | Unknown | Unknown |
| R12 skip already-handled items | Unknown | Unknown | Yes | Unknown | Unknown | Unknown | Unknown | Unknown | Unknown |
| R13 fixed time, no repeat | Unknown | Partial | Partial | Unknown | Yes | Unknown | Unknown | Unknown | Unknown |
| R14 urgent first, one action per line, numbers | Unknown | Unknown | Unknown | Unknown | Partial | Unknown | Unknown | Unknown | Unknown |
| R15 one escalation reminder | Unknown | Unknown | Unknown | Unknown | Unknown | Unknown | Yes | Unknown | Unknown |
| R16 burst collapse | Unknown | Unknown | Yes | Unknown | Unknown | Unknown | Unknown | Unknown | Unknown |
| R17 handled lead cancels reminders | Unknown | Unknown | Partial | Unknown | Unknown | Unknown | Unknown | Unknown | Yes |
| R18 delivery monitoring | Unknown | Unknown | Unknown | Unknown | Unknown | Unknown | Unknown | Partial | Unknown |
| R19 works without AMP / Gmail markup | Unknown | Unknown | Unknown | Yes | Unknown | Unknown | Unknown | Unknown | Unknown |
| R20 time-to-first-action recorded | Unknown | Unknown | Unknown | Unknown | Unknown | Unknown | Partial | Unknown | Unknown |

Matrix notes: Stripe R7 "No" is judged from the Dashboard-link pattern only and should be rechecked with a real Stripe email. GitHub R19 "Yes" rests on its mute link being HTML-only with a fallback via headers (1.4). The nad-lan design is intended to be "Yes" on all twenty rows; none of the nine products showed evidence of R5 or R6, which is the main place the design can be ahead.

## Open items
- Open and read the primary 2007 InsideSales/MIT report and the full HBR article text; confirm numbers.
- Ask Brevo support in writing whether a `text/x-amp-html` part can be sent (R19 assumes not).
- Collect real screenshots of Stripe, Shopify, Linear, GitHub emails from a test account (could not be done here; no sign-in allowed).
- Find forum evidence (Reddit, BiggerPockets, Follow Up Boss community) with a browser-based pass.
