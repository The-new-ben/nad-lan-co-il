# Developer campaign page check (HAD-678)

## Method

Checked on 2026-11-07, Israel local time (UTC+2), by script: `build/campaign_check.py` (pages) and `build/meta_ads.py` plus `build/meta_summarise.py` (Meta Ad Library). Helpers used to find the project URLs: `build/probe_domains.py` and `build/discover_projects.py`. Browser: installed Google Chrome, headless, through Playwright, 1440x900, locale he-IL, desktop Chrome user agent. Analytics and ad requests were blocked in the script's own browser context. There were no logins, no form input and no ad clicks. Each page got a 7 s wait after load, then a slow scroll to the bottom. Where a cookie banner offered a decline button, that button was pressed; consent was never accepted. Lead pop-ups were closed with Escape, except on the Gindi page (`--no-close`, because Escape also closes its content panel). One page per developer was checked. The script chose a project marked "בשיווק", "חדש" or presale. Where the developer's project page linked to a separate project or campaign site, that site was checked instead. The raw evidence for each page is in `campaign-check/<slug>.json`: final URL, HTTP status, redirect chain, title, iframe sources, canvas count, keyword counts with context, candidate 3D, tour or picker links and buttons, forms, videos and PDF links.

Classes:
- **A**: renders/photos (maybe a video, maybe floor-plan images or PDFs, maybe a list of apartment types) + a contact/lead form. No interactive building, no 360 tour.
- **B**: A plus a 360-degree virtual tour of a model/sample apartment (e.g. Matterport, Kuula, 3DVista, panorama iframes) or an interactive 2D plan/apartment picker, but NO 3D building in which the buyer picks a floor or a specific apartment.
- **C**: an interactive 3D building (or an interactive building/facade availability viewer) where the buyer himself picks a floor or a specific apartment (unit-level choice), on the page or one click from it on the same site.

## Results

| Developer | Project | URL (final) | Checked | What the buyer can do | Class | Screenshots |
|---|---|---|---|---|---|---|
| Avisror (אביסרור) | Ashira, Sde Dov, Tel Aviv ("בשיווק") | https://avisror.com/residential/אשירה-בשדה-דב/ | 2026-11-07 15:32 | View a hero render, a render gallery, an embedded YouTube video and a location map; leave details in a form. | A | campaign-check/avisror_top.jpg, campaign-check/avisror_full.jpg |
| Israel Canada (ישראל קנדה) | Vertical City, Ramat Gan ("בשיווק") | https://www.israel-canada.co.il/projects/ramat-gan/vertical-city | 2026-11-07 15:36 | View hero and gallery renders, a background video and project facts; leave details in a pop-up form and a footer form. | A | campaign-check/israel-canada_top.jpg, campaign-check/israel-canada_full.jpg |
| Y.H. Dimri (י.ח. דמרי) | YAMA TLV, Sde Dov, Tel Aviv ("בשיווק") | https://www.dimri.co.il/project/sde-dov | 2026-11-07 16:08 | View exterior, interior and lobby render tabs; open the "סיור ויטואלי" tab (360 panorama of an apartment interior, iframe dreamstours.bmby.com, 90 canvases inside it); watch a Vimeo video; see a Google map; leave details; use a chat widget. No floor or unit picker. | B | campaign-check/dimri_top.jpg, campaign-check/dimri_full.jpg, campaign-check/dimri_viewer.jpg |
| Gindi Holdings (גינדי החזקות) | LOVE Glil Yam, Herzliya ("בשיווק"; project site link from gindih.co.il) | https://mapatz.gindih.co.il/#glilyam (redirect from https://glilyam.gindih.co.il/) | 2026-11-07 15:42 | View a render slider and an interior render; open "לסיור 360° בשכונה", a 360 aerial panorama of the neighbourhood with building labels LOVE 1-13 (krpano tour on in3dreal.net, no apartment or floor actions in its hotspot XML); read a static price table by apartment type and floor; book a meeting or leave details; AI chat avatar. | B (see note) | campaign-check/gindi_top.jpg, campaign-check/gindi_full.jpg, campaign-check/gindi_viewer.jpg |
| Tidhar (תדהר) | Kochav HaTzafon, Ashdod (new project) | https://tidhar.co.il/project/kohav-hatsafon-ashdod/ | 2026-11-07 15:45 | View a hero render with a play button, text sections, a gallery and a neighbourhood map; open an apartment-type accordion (type A, type B...) that shows one floor-plan image per type; leave details. | A | campaign-check/tidhar_top.jpg, campaign-check/tidhar_full.jpg |
| Azorim (אזורים) | Azorim Park HaYam, Bat Yam (first card on the projects page) | https://www.azorim.co.il/projects/פארק-הים-בת-ים/ | 2026-11-07 15:46 | View hero and gallery renders and a location map image; 4 PDF links; contact form. | A | campaign-check/azorim_top.jpg, campaign-check/azorim_full.jpg |
| Electra Residential (אלקטרה מגורים) | SEVEN SEAS, Sde Dov West, Tel Aviv ("בקרוב בפריסייל") | https://electra-megurim.com/portfolio-item/שדה-דב/ | 2026-11-07 16:07 | View hero and building renders, project and district facts, and a static image with tower labels A-D (not clickable); contact form. | A | campaign-check/electra_top.jpg, campaign-check/electra_full.jpg |
| Aura (אאורה) | Aura Ramat HaSharon (project site linked from auraisrael.co.il as "מעבר לאתר הפרוייקט") | https://aura-project.co.il/aura-ha-sharon/ | 2026-11-07 15:50 | View an interior render slider with a price banner, text and a location map image; leave details in a sticky form. | A | campaign-check/aura_top.jpg, campaign-check/aura_full.jpg |
| America Israel (אמריקה ישראל) | MUZA, Tel Aviv ("בשיווק") | https://america-israel.co.il/project/muza/ | 2026-11-07 15:57 | View a hero render, text and a gallery slider with category buttons (map, interior, wellness, apartments); contact form. | A | campaign-check/america-israel_top.jpg, campaign-check/america-israel_full.jpg |
| Prashkovsky (פרשקובסקי) | GLILYAM, Herzliya (listed on the home page) | https://www.prashkovsky.co.il/project/פרשקובסקי-בגליל-ים-הרצליה/ | 2026-11-07 15:58 | View renders, text, an illustrated site plan (static) and a gallery; leave details in a sticky form. | A | campaign-check/prashkovsky_top.jpg, campaign-check/prashkovsky_full.jpg |
| Shikun & Binui Real Estate (שיכון ובינוי נדל"ן) | D-Point, Jaffa - Tel Aviv ("בשיווק") | https://www.shbn.co.il/projects/d-point/ | 2026-11-07 16:00 | View a render slider and text; switch tabs (project, technical spec, project stages); download project documents (PDF); leave details. | A | campaign-check/shikun-binui_top.jpg, campaign-check/shikun-binui_full.jpg |
| Africa Israel Residences (אפריקה ישראל מגורים) | Semel Tzafon, Tel Aviv ("חדש") | https://res.afi-g.com/cities/TelAviv-Jaffa/semel-zafon/Pages/default.aspx | 2026-11-07 16:01 | View a gallery, the technical spec and a list of apartment types, where each type shows one floor-plan image with zoom; see a Google map; leave details in a sticky form. | A | campaign-check/africa-israel_top.jpg, campaign-check/africa-israel_full.jpg |

All 12 pages returned HTTP 200. On every page, none of these words appeared in the rendered text: "בחירת דירה", "בחר דירה", "בחר קומה", "תלת מימד", "3D". The only page canvases were 2 full-screen decorative canvases on the Gindi campaign page (ids "stars" and "sparks"), and the 90 canvases inside the Dimri tour iframe. The single "360" text hit on Tidhar is part of a phone number (3604).

Gindi note: the 360 view is an aerial panorama of the neighbourhood, not of a model apartment. Class A excludes any 360 tour, and the page has no unit-level choice, so B was chosen as the closest class.

Supplementary page (not counted in the totals): the Israel Canada ad landing domain seen in the Ad Library, https://einstein.israel-canada.co.il/ ("Einstein 57-61 Ramat Aviv", checked 16:06). It has one screen with a render, a short text and an RSVP lead form, so it would be class A. Screenshots: campaign-check/israel-canada-einstein-lp_top.jpg and campaign-check/israel-canada-einstein-lp_full.jpg.

## Totals

- Pages checked: 12 (one per developer)
- A: 10 (Avisror, Israel Canada, Tidhar, Azorim, Electra, Aura, America Israel, Prashkovsky, Shikun & Binui, Africa Israel)
- B: 2 (Dimri, Gindi)
- C: 0

## Meta Ad Library

The URL used was `https://www.facebook.com/ads/library/?active_status=active&ad_type=all&country=IL&q=<name>&search_type=keyword_unordered`. All 5 searches opened without login. The server answered HTTP 403, but the full results page rendered. Each page was scrolled about 6 screens and no ad was clicked. The result counts are Meta's own rounded "כ-N תוצאות" figures for the keyword. A keyword search also returns other advertisers whose text contains the word, so the table also gives the advertiser split of the cards that loaded.

| Developer | Query | Checked | Meta result line | Cards loaded / of them by the developer's own page(s) | Landing domains shown on cards | Screenshots |
|---|---|---|---|---|---|---|
| Avisror | אביסרור | 16:03 | כ-110 תוצאות | 67 / 44 "אביסרור- בונים מאהבה" + 2 "Avisror home" (others include Z Sport, Yad2) | AVISROR.COM, AVISRUR.CO.IL, LP.AVISROR-HOME.COM | campaign-check/meta_avisror.jpg, campaign-check/meta_avisror_cards.jpg |
| Israel Canada | ישראל קנדה | 16:03 | כ-190 תוצאות | 62 / 36 "ישראל קנדה - Israel Canada" + 13 "ICR - Israel Canada Reem Residences" | EINSTEIN.ISRAEL-CANADA.CO.IL (others on the page belonged to other advertisers) | campaign-check/meta_israel-canada.jpg, campaign-check/meta_israel-canada_cards.jpg |
| Dimri | דמרי | 16:04 | כ-360 תוצאות | 68 / 44 "י.ח.דמרי - בנייה ופיתוח" (others include Dimri malls, Maccabi) | DIMRI.CO.IL | campaign-check/meta_dimri.jpg, campaign-check/meta_dimri_cards.jpg |
| Gindi | גינדי | 16:04 | כ-380 תוצאות | 65 / 25 "Gindi Holding גינדי החזקות" (others include unrelated people and firms named Gindi) | none shown as a domain; card captions name projects (e.g. "גינדי Space רמת אפעל", "גינדי שדה דב", "המפץ הגדול בגינדי גליל ים") | campaign-check/meta_gindi.jpg, campaign-check/meta_gindi_cards.jpg |
| Azorim | Azorim (the Hebrew "אזורים" is a common word and returned about 1,800 mostly unrelated ads) | 16:05 | כ-190 תוצאות | 74 / 74 "אזורים - Azorim" | LP.AZORIM.CO.IL, VILLE-HERZLIYA.CO.IL | campaign-check/meta_azorim.jpg, campaign-check/meta_azorim_cards.jpg |

What the developers' own creatives show, from the screenshots and the card text in `meta_<slug>.json`:
- Building renders, often with price or presale text on the image (for example Avisror NEXUS TOWERS "מחירי פריסייל", and Dimri cards with prices such as "דירת 3 חד' החל מ 1,700,000"), plus short videos.
- Azorim has several videos of a sample apartment ("נפתחה הדירה לדוגמה בפרויקט סנטרל פארק 17").
- Calls to action are mostly "Learn More" and "Sign Up". Gindi also has "Send WhatsApp Message" cards, but in the loaded set these belong to other advertisers named Gindi.
- The ad copy mentions price, presale, penthouses, garden apartments and payment terms. Where "סיור" appears, it means booking a physical visit: Israel Canada "לתיאום סיור בפרויקט" and Azorim "קביעת סיור בדירה לדוגמה". None of these developers' cards mention 3D, a virtual tour or apartment selection.
- People appear mainly in other advertisers' cards, and in an Israel Canada Rainbow render that shows people at a pool.

Two ad landing domains were opened at their root only, because the exact ad paths are not visible without clicking an ad:
- https://lp.avisror-home.com/ shows a default WordPress "Hello world" page.
- https://ville-herzliya.co.il/ rendered as a blank page in headless Chrome.

Neither was classified. The JSON files are campaign-check/avisror-home-lp.json and campaign-check/azorim-ville-lp.json.

## Could not check / caveats

- **Gindi legacy domain.** gindi.co.il has an invalid HTTPS certificate. Over plain HTTP it redirects to `http://www.ginditowers.com/cgi-sys/defaultwebpage.cgi`, a cPanel "Default Web Site Page". The current site, gindih.co.il, was found through a web search and used instead.
- **Shikun & Binui first pick sold out.** The first project opened, Dream Tower Netanya, is marked "הסתיים השיווק", so D-Point ("בשיווק") was used.
- **America Israel screenshots.** The page is RTL and has about 11,000 px of horizontal overflow. Normal headless screenshots of it come out as an empty dark frame, while the DOM evidence was collected normally. Its screenshots were therefore taken with a CDP beyond-viewport capture, cropped to the right-most 1440 px (`--rtl-wide`).
- **Cookie banners left on screen.** The Dimri banner (its decline button was not matched by the script) and the Azorim and Shikun & Binui cookie bars are visible in some screenshots. No consent was given.
- **Stitched full-page shots.** The `_full.jpg` shots are stitched from 1440x900 viewport slices, so fixed headers and sticky forms repeat in each slice. Shots are capped at 9,000 px tall; the Tidhar page is 11,917 px.
- **Extra developers not needed.** Acro, Rotshtein, Ashtrom Residential, Danya Cebus and Yuval Yizum were not checked, because none of the 12 listed developers failed outright.
