# Live proof, 19.11.2026 (HAD-791, release 1.72.706)

Release: 1.72.706 released and verified on the second run (deploy-result-706.json; the first run rolled back cleanly on four
inherited 1.72.602 rows that forbade the tracker outside the stage pages). Health 1.72.706, visit_trail 1.1.0 db 2, dev_report 1.0.1.

## Events arriving from the live site (server rows read back through a temporary admin bridge, removed after each read)
Browser: installed Google Chrome, headless, normal user agent, no webdriver flag; one browser at a time, closed after each run
(the PC was short on memory, the owner's own Chrome window was minimized and could not be photographed).

Desktop 1366x900, Rainbow (/projects/rainbow-tel-aviv/, project 4464, mode full), stored as device "d":
- open
- click deal_floor "קומה 13 במגדל, בבמה" f=13 (the deals table's floor button)
- click tour_btn "להיכנס לדירה · 360°"
- tour o=1 s=25-w (the stage's own event)
- act tour_open src=ga (the module's nadlanGA call, mirrored from dataLayer: no change in the module)
- leave vis=14 s, scroll 100%
Screenshot: shots/e1-desktop-rainbow-after-clicks.png

Phone 390x844, touch, Android user agent, Kikar HaMedina (/projects/hamedina/, project 8113, mode full), stored as device "m":
- open
- click wa "לקבלת פרטים נוספים בוואטסאפ" where=hero (a tap on the WhatsApp button; nothing was sent)
Screenshot: shots/e2-phone-kikar-after-taps.png

Phone, /mortgage-calculator/ (page 121, mode lite, no project):
- act mortgage_check k=tools (a digit typed into the budget calculator; the number itself is not in the row)
Screenshot: shots/e3-phone-mortgage-typed.png

All seven test visits (including one from the owner's Chrome) were then deleted with nadlan_vt_delete_visit, so the developer
counts stay real.

## Found during the proof and fixed in the repo (next release)
- The mortgage page's most visible calculators (fields nlmq-*, nlm-*) are outside the calculator areas the 1.1.0 watcher knew;
  typing there was not counted. trail.js now also counts a numeric field whose id starts nmc-, nlmq-, nlm-, nlmb-, nlck-, nlpg-
  (test_trail_11.js 117/117).
- Correction of my own first finding: the 7.11 tracker WAS on the stage project pages (Rainbow and Ashira have visits from
  19.11 morning, before 1.72.706). What it missed: H Infinity and every other project page without a stage, the language pages
  of non-stage projects, and every tool page (designer, mortgage, basket).

## Real data already in the report (not tests)
Rainbow (4464), 30 days, read 19.11 ~11:45 UTC: 24 visits, 6 chose a floor, 6 opened the view, 1 WhatsApp, measuring since 10.11.2026.
