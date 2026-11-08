# OwnerMail v1: the counted comparison (HAD-687, 8.11.2026)

Ben, 8.11.2026: "תוכיח לי מדעית שאין אף מקום בעולם שעושה את זה יותר טוב".

**Method.** The research (`research.md`, sources read 8.11.2026) produced 20 testable requirements, each tied to evidence: lead-response studies, interruption and email-stress studies, RFC 8058, and the product practice of nine leaders. R10 (bulk-mail unsubscribe headers) does not apply to a mail with one recipient (the owner), so 19 rows count.

Scoring: Yes = 1, Partial = 0.5. Competitor cells hold **only what was seen in evidence**. "?" means not seen, which is **not** the same as "they do not have it". So a competitor score is a floor, not a ceiling. The NadLan columns were checked in our own code (before: the code as live on 8.11; after: this release, its logic test, and the live click test).

| # | Requirement (evidence) | NadLan before | **NadLan v1** | Stripe | Shopify | Linear | GitHub | HubSpot | Salesforce | Zillow PA | Follow Up Boss | kvCORE |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| R1 | Lead mail within 60 s (Oldroyd/MIT: 5 min vs 30 min; HBR 2011: 42 h average) | ½ (120 s, plain text) | ½ → measured live | ? | ? | ? | ? | ? | ? | ½ | ? | ? |
| R2 | The same card every time: who, phone, page, interest, heat | ½ | ✓ | ? | ? | ? | ? | ? | ? | ? | ? | ✓ |
| R3 | Phone as a tap button, at least 48 px | ✗ | ✓ (50 px) | ? | ? | ? | ? | ? | ? | ? | ? | ½ |
| R4 | WhatsApp with a ready, editable line naming the page | ½ (link, no line) | ✓ | ? | ? | ? | ? | ? | ? | ? | ? | ½ |
| R5 | Opening a link never writes; only a POST does (RFC 8058, link scanners) | ✗ | ✓ | ? | ? | ? | ? | ? | ? | ? | ? | ? |
| R6 | Signed link bound to one lead, one action, with expiry; no login | ✗ | ✓ (HMAC-SHA256, 30 days) | ? | ? | ? | ? | ? | ? | ? | ? | ? |
| R7 | Act from the mail: contacted, not relevant, remind tomorrow, mute | ✗ | ✓ (+ undo) | ✗ | ? | ? | ½ | ½ | ? | ? | ? | ½ |
| R8 | Mute per alert type, and the undo is visible | ✗ | ✓ | ½ | ½ | ½ | ✓ | ½ | ? | ? | ½ | ½ |
| R9 | A "why you got this" line | ½ | ✓ | ? | ? | ? | ✓ | ? | ? | ? | ? | ? |
| R11 | No digest when nothing is new (HubSpot's own rule) | ✓ | ✓ | ? | ? | ? | ? | ✓ | ? | ? | ? | ? |
| R12 | Handled items leave the digest | ½ | ✓ | ? | ? | ✓ | ? | ? | ? | ? | ? | ? |
| R13 | Fixed time, never the same content twice | ½ | ✓ | ? | ½ | ½ | ? | ✓ | ? | ? | ? | ? |
| R14 | Urgent first, one action per line, numbers vs yesterday | ✗ | ✓ | ? | ? | ? | ? | ½ | ? | ? | ? | ? |
| R15 | One repeat reminder after 30 min | ✗ | ✗ (Ben 23.10: no reminder mails; the morning mail is the one reminder) | ? | ? | ? | ? | ? | ? | ✓ | ? | ? |
| R16 | Bursts collapse | ½ (6 a day) | ½ (6 a day; each lead stays instant) | ? | ? | ✓ | ? | ? | ? | ? | ? | ? |
| R17 | A handled lead stops its reminders | ½ | ✓ | ? | ? | ½ | ? | ? | ? | ? | ? | ✓ |
| R18 | Delivery is visible (sent, failed, held) | ✗ | ½ (dashboard widget; no bounce tracking) | ? | ? | ? | ? | ? | ? | ? | ½ | ? |
| R19 | Works with no AMP and no Gmail markup | ✓ | ✓ | ? | ? | ? | ✓ | ? | ? | ? | ? | ? |
| R20 | Time to first action recorded and shown | ✗ | ✓ (morning row) | ? | ? | ? | ? | ? | ? | ½ | ? | ? |
| | **Score (of 19)** | **6** | **16.5** | 0.5 | 1 | 3.5 | 3.5 | 3.5 | 0 | 2 | 1 | 4 |

## What this proves, and what it does not
- **Proven:** v1 meets 15 requirements in full and 3 in part. The old NadLan mails met 2 in full and 8 in part.
- **Proven:** on R5 and R6, the two that make "act from the mail" safe, none of the nine leaders showed evidence of it.
- **Not proven:** that the leaders lack the cells marked "?". The research could not sign in to their products (no test accounts), so many of their mails were not seen. The honest claim is "ahead on everything that could be checked", not "the best in the world".
- **Open, by decision:** R15 (a 30-minute repeat reminder). Zillow does it; Ben ruled out reminder mails on 23.10.2026.
- **Open, technical:** R18 bounce tracking needs the Brevo webhook (after Ben saves the Brevo key). R1 depends on WordPress cron firing on time; the live test measures it.

## Why each choice (the science in one line each)
- **One instant mail per lead, everything else in one morning mail:** Kushlev and Dunn 2015 (124 adults, 3 email checks a day, lower stress). Mark et al. 2016 found batching alone mixed, so only non-urgent items wait; a lead never waits.
- **Speed:** the card leaves 60 s after the form (it was 120 s). Oldroyd/MIT and InsideSales: odds of contact about 100 times higher at 5 minutes than at 30. HBR 2011: the average first reply was 42 hours, and 23% of firms never replied.
- **A confirm page:** RFC 8058 requires POST for one-click actions because mail software opens links by itself.
- **No Gmail action buttons or AMP:** both need Google sender registration with sustained high volume, and Brevo documents no AMP part. Plain HTML links work in every mail app.
