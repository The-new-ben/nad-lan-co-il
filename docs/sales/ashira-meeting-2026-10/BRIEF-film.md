# Task: a short English film "How a buyer decides" (reconstruction of a real journey), for a developer meeting on 19.10.2026

You work on Ben's PC. Repo root: C:\Users\777\nad-lan\nad-lan-co-il. Write ONLY inside docs\sales\ashira-meeting-2026-10\film\.
The live site is read-only for you: browse it, never submit a form, never send a WhatsApp message, never log in, never edit any file outside film\.

What happened (real, anonymous): a visitor on the Ashira project page opened the 3D stage, chose an apartment, looked at the view
and the area, wanted more details and pressed the WhatsApp button. Reconstruct THAT kind of journey as a screen film.

Page: https://nad-lan.co.il/projects/ashira-sde-dov-en/ (English). If a control does not exist there, use the Hebrew page
https://nad-lan.co.il/projects/ashira-sde-dov/ for that shot only. Nothing personal appears anywhere.

How (proven pattern in this repo: docs\sales\meital-kit-2026-10\shoot.py and build_film.py):
- Python Playwright, chromium channel "chrome", args ["--use-gl=angle","--use-angle=swiftshader","--enable-unsafe-swiftshader"],
  viewport 1600x900, record_video_dir, slow human pacing (mouse moves, 1.5-3 s pauses, smooth scrolls). Wait for the 3D to render.
- Journey: land on the page (H1 + answer) -> the 3D stage -> choose a floor and an example apartment -> the view from the floor ->
  the area map (switch categories: education, parks, transport, shopping, health) -> the price calculator -> hover the WhatsApp bar
  (do NOT click it). Find selectors yourself by reading the DOM (ids seen: #nlps-stage, #nlps-view, #nlpjx-map, #nlpg, #nlsch).
- Add a 3 s English title card at the start ("A real buyer journey, reconstructed · nad-lan.co.il") and a 4 s end card
  ("From first look to a WhatsApp message: one decision room · nad-lan.co.il"). Cards: background #0E1B24, text #EEF3F2, accent #B3126F,
  font IBM Plex Sans. No music, no voice. Label on the first card in small text: "Reconstruction. No personal data."
- Encode H.264 MP4 1600x900, 60-90 s, with imageio_ffmpeg (installed). Output: film\journey-en.mp4 plus 6 key stills (film\still-*.png).
- Write film\REPORT.md: what was shown, which steps worked, which controls failed or did not exist (exact), file sizes.
Do not stop at the first failure: if the 3D does not render, retry with headless=False. Finish with the report.
