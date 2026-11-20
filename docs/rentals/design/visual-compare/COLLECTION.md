# Visual comparison, evidence collection (20.11.2026)

Raw facts and counts only. No judgement of beauty, no conclusions.
Vendor marketing screens are staged and idealised: invented tenants, perfect data, chosen states, store captions and device frames. They show what a vendor wants seen, not a real account.

## Method as actually run
- Playwright, installed Edge (`channel=msedge`, headless), `python -X utf8`, public pages only, read-only, no login, no form, no download of files; screenshots only.
- Source 1 (main): public Google Play listing page of each app (`play.google.com/store/apps/details?id=...&hl=en&gl=US`). Every `img[alt="Screenshot image"]` was element-screenshotted at device scale factor 3 (the store serves about 526 px wide images, so the PNGs are upscaled stores frames, 411 to 681 px wide). The Apple App Store page was opened once for DoorLoop (wrong id guessed, not used further) and not used as a source.
- Source 2: vendor marketing pages (element screenshot of the product image, scale factor 2) for DoorLoop home, Landlord Studio home, Hemlane maintenance page, Apple Home app page.
- Dira360: the homepage demo video (`media/dira360-management-demo-he.mp4`, 48 s) was loaded in the page, paused at fixed seconds and the video element screenshotted (no file downloaded). Frames at 18 s and 42 s kept; the PNG includes the player bar.
- Pause of 3 to 4 seconds between pages. No robot check appeared on any page; nothing blocked. Cookie banners were left alone (not clicked); one is partly visible at the bottom of `doorloop-S1d.png`.
- Contact sheets of each product's frames were made in a scratch folder and looked at with the Read tool to choose the screens and to count. Counts were made on these contact sheets (downscaled) plus the selected frames, not on every full-size PNG: see doubts.
- hues_script: PNG shrunk to 400 px, pixels with saturation above 0.35 and value above 0.3 sorted into 12 hue bins of 30 degrees; bins over 1% of the area are counted. Photographs and page backgrounds are NOT excluded, so it differs from hues_eye (which excludes photos and counts meaning only).
- Files: PNGs in `D:\Media\nad-lan\rentals-visual-compare\shots\` (none in the repository). Table: `scores.csv` next to this file. 45 rows, 45 PNGs.
- Words in text found in pages were treated as data; no page contained instructions aimed at an agent.

## Products: found / not shown / blocked
Rental management leaders
- Rentila: phone frames (Play). S1 properties list, S4 finance. S2 not shown (list only), S3 not shown.
- DoorLoop: phone S1, S2 (an inspection of one unit), S3 work orders, S4 payments; desktop S1 (home hero overview) and a desktop Listings table (named maintenance on the page, not a repair screen).
- Arthur Online: phone (Arthur Manager app) S1, S2, S4 (tenancies list with outstanding rent). S3 not shown. Web feature pages have illustrations and small cards, not used.
- Landlord Studio: phone S1 to S4; desktop (iPad hero) S1.
- immocloud: phone S1, S4 (German). S2 and S3 not shown.
- Hemlane: the Play listing found is "Hemlane For Tenants" (tenant app), so S1 S3 S4 are the tenant view; one web mock card (repair request). The landlord app listing returned an empty title and was not captured. S2 not shown.
- AppFolio: phone listing frames are marketing; only S1 (dashboard) is a real screen. S2 S3 S4 not shown.
- TenantCloud: Play listing "TenantCloud Pro" (com.sav.tenantcloud) after the first guessed id failed. S1, S2, S4. S3 not shown.
- Stessa: S4 only (transactions). S1 S2 S3 not shown.
- Dira360: not on Google Play (search found nothing). Only the website video: S2 and S4 frames, desktop, Hebrew. S1 and S3 not shown (the video shows tenant screening, contract review, a WhatsApp chat, payments tracking).
Benchmark apps
- Airbnb: Play frames; host frame (performance chart and calendar) counted S1, guest home S2, map S2b. The host "Today" tab is not shown in the listing.
- Zillow: the Play listing frames show compare-homes and an illustrated insights map, no listing page or real map screen. The zillow.com site was not opened.
- Matterport: dollhouse and floor plan frames (S2, S1).
- HomeZada: three frames (S1 dashboard, S2 rooms, S2b item).
- Apple Home: two marketing composites from apple.com/home-app.
- SmartRent (resident app) and Latch: two frames each. Replaced nothing.
No maintenance (S3) or rent (S4) screens exist for the benchmark apps; they were not asked to.

## Motion line (homepage scan for video elements, 20.11.2026; feature pages and Play promo videos were NOT scanned)
- Rentila 0 (home only). DoorLoop 0. Arthur Online 0. Landlord Studio 0. immocloud 0. Hemlane 0.
- AppFolio 1: videos on home (card animation `Site-Refresh_Cards-Stats_*.mp4`, plus one 1312x738 blob video); what the large one shows was not looked at, so 1 is "a video exists".
- TenantCloud 1: an embedded iframe 1310x737 on the home page (content not opened, probably a video).
- Stessa 0. Dira360 1: `https://www.dira360.co.il/media/dira360-management-demo-he.mp4` (48 s, screen frames of the interface).
- Benchmarks not scanned: Apple Home page has a 384x832 video of the Home app (seen in the image list), counted motion 1 for Apple Home. Others unknown.

## Totals (from scores.csv)
- 29 rental-management rows: mean pictures 0.5, maps 0, 3D 0, state shown 0.5, hues by eye 2.4, hues by script 1.0, picture share 1.7%, words 69.7, primary action 0.3; icons: 17 line, 6 filled colour, 6 none.
- 16 benchmark rows: mean pictures 1.8, state shown 0.2, hues by eye 1.5, hues by script 1.2, picture share 38.1%, words 43.1; maps on 2 rows, 3D on 2 rows (Matterport); icons: 8 none, 4 filled colour, 3 line, 1 illustration.

## Doubts about counts
- Store frames carry a caption (words counted include the caption) and a device bezel (picture share is of the whole PNG).
- Some frames are cropped by the store carousel on the right (DoorLoop S1, Landlord Studio, TenantCloud, Airbnb, Smartrent, Latch).
- pictures: Arthur S2 thumbnails about 7, counted 8 loosely. Airbnb S2 count 7 includes cropped cards. People avatars not counted as pictures.
- state_signal is 1 only when status shows on the item without a press (tags, Paid, colours); borderline cases (Landlord Studio tenant cards AUTOPAY/INVITED) were set to 0.
- hues_eye vs hues_script differ because photographs, gradients and backgrounds are not excluded in the script, and a 30 degree bin splits or merges neighbouring hues.
- Picture share, words and icon_kind are by eye in steps, from contact sheets.
- Hemlane tenant-app screens are not a landlord's view; Dira360 frames come from a video and look like a mock-up page.
- The doorloop-S3d tile is a Listings table, kept because the page names it maintenance.
