# Task: critical PRESS audit of the Ashira project page against Rainbow (read-only), for a developer meeting on 19.10.2026

Repo root: C:\Users\777\nad-lan\nad-lan-co-il. Write ONLY inside docs\sales\ashira-meeting-2026-10\audit\. NEVER change the live
site or any other file (the owner forbids touching the Ashira page: a buyer found it and Google ranks it). No form submits, no WhatsApp sends.

Pages: A = https://nad-lan.co.il/projects/ashira-sde-dov/ , B (the standard) = https://nad-lan.co.il/projects/rainbow-tel-aviv/
Python Playwright, channel "chrome", args ["--use-gl=angle","--use-angle=swiftshader","--enable-unsafe-swiftshader"] (pattern:
docs\sales\meital-kit-2026-10\shoot.py). Two widths: 1440x900 and 390x844 (phone). For each page and width:
1. Order on screen: H1 -> answer paragraph -> CTAs -> 3D stage -> view+map -> facts -> article (house law). Record the y of each.
2. PRESS every control and screenshot the result: floors, towers/buildings, directions, example apartment, rooms/360 tour,
   facilities (pool, gym, spa, lobby...), floor view, area map categories, map pins, price calculator, design styles, basket,
   video call, WhatsApp bar (do not send). For each: works / broken (what happens) / missing (exists on B, not on A).
3. The in-building journey: on B you choose an apartment and then reach the facilities. Can a buyer do the same on A? Steps count.
4. Facts on A vs the ledger docs\content\ashira\00-source-ledger.md (and docs\research\2026-10-15-ashira-meeting\README.md, which already
   lists verified contradictions: 9 vs 8 floors, Ashira listed as its own neighbour at 11 m in EN/FR/RU/AR, sales data only in Hebrew,
   rooms 2-5 vs 2-6). Add any NEW wrong or unsupported fact you find, with the quote and the source line.
5. Console errors and failed network requests on A.
Output: audit\REPORT.md in Hebrew (plain words, short sentences): a table control x page (A/B) with works/broken/missing, the
journey comparison, facts, errors, and a ranked list "what to fix, smallest change first", each item with the exact place on the page.
Screenshots: audit\<page>-<width>-<control>.png. Finish with the report even if some controls fail.
