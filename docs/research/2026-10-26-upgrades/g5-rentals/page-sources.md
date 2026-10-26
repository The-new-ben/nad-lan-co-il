# /דירות-להשכרה/ (G5, new page): where every fact on the page comes from (internal, written by write_g5_page.py, 26.10.2026)

| Fact on the page | Source |
|---|---|
| Median rent by city (72), rooms 3/4/5/all, 22 quarters to April to June 2026, the file's yearly change, 945 neighbourhood medians (all sizes, last year) | data.nadlan.gov.il settlement rent files, אתר הנדל״ן הממשלתי, שכר דירה חציוני לפי עיר, חדרים ושכונה, גרסה 20-08-2026, read 25.10.2026 (U2 fetch, raw in _private-research/.../raw/u2/data/nadlan-gov); nadlan.gov.il labels them "מחיר חציוני" |
| Average rent with sampling error, 18 cities + 6 districts + Israel, groups 1-2 / 2.5-3 / 3.5-4 / 4.5+, Q2 2026 and Q2 2025 | CBS price bulletin, table 4.9 (research parse docs/research/2026-10-26-upgrades/u2-investment/data/cbs-rent-table-4-9-2026q2.json); the same figures ynet (8.9.2026) quotes: Israel 5,086 in Q2 |
| Rent index monthly and 12-month change to ספטמבר 2026 | CBS API series 120460 |
| Fair-rental chapter: sections 25א to 25טו, first and second schedules, the 5786 amendment of 25י | Nevo law00/5149 (current to 30.9.2026) and he.wikisource (edited 30.9.2026), raw in raw/g5/gov |
| Guarantee cap rules incl. personal guarantors not counted, relatives excluded | Kol Zchut "הגבלת סכום הערובה שמותר לדרוש משוכר דירה" (raw/g5/comp/c16.html) |
| Tax: ceiling 5,654 (2024 to 2026), 5,471 (2023), 5,196 (2022), partial up to 11,308, 10% due 30.1, offset up to 7,500, 31% / 10% first bracket, payment at the post office voucher | Kol Zchut pages updated 22.2.2026 (raw/g5/gov/g05, g06); the Tax Authority guide (403 to scripts, its AI-overview summary matches) |
| "דירה להשכיר" is the government company for long-term rental tenders | renten.co.il (raw/g5/comp/c06.html) |
| Every computed number (yearly change from CBS Q2 2025, the tax table, the 10% break-even 6,740 ₪, neighbourhood estimates) | this script, from rent.json, cross-checked by tools/instruments/test_rentfair.js |
