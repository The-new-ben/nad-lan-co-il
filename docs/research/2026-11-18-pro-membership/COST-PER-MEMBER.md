# What one active professional member costs us per month

18.11.2026. Our stack: WordPress on uPress (card page, mini-site, images, forum), mail codes through Brevo, video calls on LiveKit Cloud (`assets/designer/call.js`, reused by the forum). Every price below is a published price with its URL. Every usage figure is an **assumption** and is labelled so. Nothing here is a revenue forecast.

## Published prices used

| Item | Price | Source (opened 18.11.2026) |
|---|---|---|
| LiveKit Build (free) | 0 USD; 5,000 WebRTC minutes and 50 GB downstream included; **hard cap, new requests fail after it** | https://livekit.com/pricing ; https://docs.livekit.io/deploy/admin/quotas-and-limits/ |
| LiveKit Ship | from 50 USD/month; 150,000 minutes and 250 GB included; then 0.0005 USD per minute and 0.12 USD per GB; 1,000 concurrent connections | https://livekit.com/pricing |
| LiveKit Scale | from 500 USD/month; 1.5M minutes and 3 TB included; then 0.0004 USD per minute and 0.10 USD per GB | https://livekit.com/pricing |
| What a LiveKit minute is | "Time that a single user is connected to LiveKit Cloud via a LiveKit SDK" (per participant), billed per second, 10-second minimum per session | quotas page above; https://docs.livekit.io/home/cloud/billing/ |
| What a LiveKit GB is | "The total data transferred out of LiveKit Cloud during a session, including media tracks and data packets" | quotas page above |
| Video bitrate we publish | Our call publishes 960x540 (`VideoPresets.h540`) with simulcast layers h180 and h360 (`call.js` line 1742 to 1743). h540 = 800,000 bit/s, h360 = 450,000, h180 = 160,000; speech audio 24,000 bit/s | https://raw.githubusercontent.com/livekit/client-sdk-js/main/src/room/track/options.ts |
| uPress VPS | from 292.14 ₪/month (listed as from 90 USD), 40 GB storage, 3 TB monthly traffic | https://www.upress.co.il/ ; plans https://www.upress.co.il/plans/vps/ |
| USD to ₪ | 3.246, taken from uPress's own pair (292.14 ₪ = 90 USD); uPress says the ₪ amount follows a bank rate and may change | same |
| Cloudflare R2 (an outside option for images) | 0.015 USD per GB-month; first 10 GB-month free; no egress charge | https://developers.cloudflare.com/r2/pricing/ |
| SMS code | about 0.04 ₪ each (1,000 for 40 ₪, sms4free, read 12.11.2026) | `../2026-11-12-pro-forum/DECISION-PACK-HE.md` |
| Brevo mail | **not read**: the pricing page did not render to the tool | https://www.brevo.com/pricing/ |

Which uPress plan nad-lan.co.il is on was not checked in this research. The VPS line is used as the unit price because it is the plan with the most storage per shekel on the page; if the site is on another plan the per-GB price changes.

## Usage assumptions (ours, not measured)

| | Light | Medium | Heavy |
|---|---|---|---|
| Video calls per month | 2 | 8 | 40 (within today's cap of 8 per member per day) |
| Minutes per call | 20 | 30 | 45 |
| People in the call | 2 | 2 | 3 |
| Participant minutes (calls x minutes x people) | 80 | 480 | 5,400 |
| Photos on card and mini-site | 10 | 40 | 150 |
| Stored size per photo, all WordPress sizes together | 0.6 MB | 0.6 MB | 0.6 MB |
| Card and mini-site views per month | 100 | 500 | 2,000 |
| Page weight per view | 1.5 MB | 1.5 MB | 1.5 MB |
| SMS codes per month | 2 | 4 | 10 |

Downstream data per participant minute, worst case (everyone receives every other camera at the top layer, h540 plus audio = 824,000 bit/s per stream):
- 2 people: 824,000 x 60 / 8 = 6.18 MB per participant minute = 0.00618 GB.
- 3 people: two streams each = 0.01236 GB per participant minute.
LiveKit's adaptive stream (on in our call) drops to h360 or h180 for small video tiles, so real data should be lower. This is an upper bound.

## The arithmetic, as overage on LiveKit Ship (the marginal cost)

| | Light | Medium | Heavy |
|---|---|---|---|
| Minutes x 0.0005 USD | 80 x 0.0005 = 0.04 | 480 x 0.0005 = 0.24 | 5,400 x 0.0005 = 2.70 |
| Data GB | 80 x 0.00618 = 0.49 | 480 x 0.00618 = 2.97 | 5,400 x 0.01236 = 66.74 |
| Data x 0.12 USD | 0.059 | 0.356 | 8.009 |
| **Video total USD** | **0.099** | **0.596** | **10.709** |
| Video total ₪ (x 3.246) | 0.32 | 1.93 | 34.76 |
| Image storage GB (photos x 0.6 MB) | 0.006 | 0.024 | 0.09 |
| Image storage ₪ on uPress VPS (292.14 / 40 = 7.30 ₪ per GB) | 0.04 | 0.18 | 0.66 |
| Same on R2 (0.015 USD per GB) | under 0.01 ₪ | under 0.01 ₪ | 0.004 ₪ |
| Page traffic GB (views x 1.5 MB) | 0.15 | 0.75 | 3.0 |
| Page traffic ₪ on uPress VPS (292.14 / 3,000 GB = 0.097 ₪ per GB) | 0.02 | 0.07 | 0.29 |
| SMS ₪ (x 0.04) | 0.08 | 0.16 | 0.40 |
| Card page and mini-site text (database rows) | about zero | about zero | about zero |
| **Total ₪ per member per month** | **about 0.46** | **about 2.34** | **about 36.11** |

Notes on the totals:
- Video is the only line that grows fast. At the heavy level it is 96% of the cost (34.76 of 36.11).
- Data, not minutes, is the bigger video cost: at the medium level 0.356 of 0.596 USD.
- The heavy level counts all 3 people's minutes against the member who opened the call.
- Mail codes are left out because the Brevo price was not read.

## What the plans mean in members

- **Build (free)**: 50 GB is reached first. 50 / 0.49 = about 101 light members, or 50 / 2.97 = about 16 medium members, and one heavy member alone (66.74 GB) passes it. Because Build is a hard cap, calls would **fail** for everyone after that, so a public paid tier needs Ship first.
- **Ship (50 USD)**: 250 GB covers 250 / 2.97 = about 84 medium members (minutes would allow 150,000 / 480 = 312). 50 USD / 84 = about 0.59 USD per medium member, the same as the overage figure above. Beyond that each medium member adds about 0.60 USD.

## Costs that are real but have no published price

- **Staff time for verification** (VERIFY-NO-REGISTER.md): about 3 to 5 minutes for level 2 and 2 to 5 minutes for level 3, per member, once a year (our assumption). No money figure, because the hourly cost is Ben's to set.
- **Review of first posts and reports** (first post of every writer is held for review, `../2026-11-12-pro-forum/DECISION-PACK-HE.md`): time, not money.
- **Brevo mail** above its free allowance: price not read.
- **Lawyer** for terms, privacy notice and the verification wording: not priced.

## Reading the result

At light and medium use, one member costs well under 3 ₪ a month in money. That makes "free for now" safe for the card, the mini-site and the forum. Video is the one line to watch: a heavy video user costs about 36 ₪ a month at worst-case quality, so video above a monthly allowance is the natural first paid line (see PLAN-HE.md). The existing caps (8 calls per member per day, 40 per day for the whole forum) stay.
