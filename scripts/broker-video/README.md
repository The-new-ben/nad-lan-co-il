# A broker's listings video

The owner's order, 24.9.2026: every broker gets a video of all their listings. Built for Meital Katzir first (release 1.72.249).

1. Data: `python renderer/tools/build_broker_json.py --slug <slug>` reads the broker's public card, site and listing pages and
   writes `renderer/data/<slug>.json` (photos go to `renderer/img/<slug>/`). Unknown facts are omitted; a price shows only where
   the listing page prints it. Check the JSON before rendering.
2. Render: `python renderer/render.py all --broker <slug>` (8 Mbps, for WhatsApp status and reels), then the web size:
   `python renderer/render.py record --size 1080x1920 --kbps 2500 --suffix _web`, the same for `1920x1080`, and
   `python renderer/render.py poster --sizes 1080x1920,1920x1080 --quality 82`. At 4 seconds a listing, 13 listings fit in 60 s;
   use `--per 3` or `--max N` for more.
3. Upload: `python upload_media.py renderer/out <slug>` (web files and posters, public names without Hebrew; an upload that is
   already in the media library is not repeated).
4. On the site: the professional's meta `nl_video` (JSON: tall, wide, poster_tall, poster_wide, count, secs, date) shows the
   design system's ListingsVideo on the card (see `deploy249.py` for the write and the checks).

The broker's name, "מתווך" or "מתווכת" and the licence number are on every frame (Brokers Regulations, reg. 19(a)).
