# MortgageMillion

"כמה עולה משכנתא של מיליון שקל, חודש אחר חודש": the monthly figure on /mortgage-calculator/#million (1.72.615, HAD-675, 9.11.2026).
The first payment on 1,000,000 ILS over 25 years, Spitzer, at the average track mix and effective rates of all banks and of each bank
(Bank of Israel TamInt010), for every month in the data file (25 months, 9.2024 to 9.2026 at build). It updates by itself when the
monthly data file is refreshed.

## Why it looks like this (the anti-default line)
The subject is official registers and data tables (Bank of Israel files), not a magazine page. Slate ink `#12202A`, deep teal `#1F4B5C`
for the line and links, survey teal `#2F6F86` for the copy button and the quote rule, grid `#D3DCE2` on white. IBM Plex Sans Hebrew for
text and IBM Plex Mono for numbers and axes, like the rest of the page's data blocks. No cream, gold, terracotta, gradient, emoji or Inter.

## Anatomy
1. H3 and one answer sentence with the month, the year-ago figure, the high and the low.
2. A line chart (inline SVG, time left to right as in Bank of Israel charts), high, low and latest marked, a text label for screen readers.
3. A table of the last 13 months by bank (all banks, Hapoalim, Leumi, Discount, Mizrahi, FIBI) and the change from the previous month.
4. A cite box: the sentence a journalist can quote, the source line, "העתקת הציטוט" (copies sentence + source + link) and
   "הורדת כל החודשים (CSV)" (REST /wp-json/nadlan/v1/mortgage-million, every month and every bank, BOM for Excel).

## Schema
Dataset `#million` with a CSV DataDownload; the market Dataset gains the same CSV; a WebApplication `#calculators` whose featureList is
the tools printed on the page.

## Code
`inc/mortgage-market.php`: nadlan_mm_million_rows / _sentence / _html / _css / _csv, the REST route, the JSON-LD.
Local render: docs/research/2026-11-09-mortgage-proof/build/render_million.php (asserts 5,428 / 5,443 / 5,404 / 5,354 / 5,463 / 5,281 for 9.2026).

## v2 (1.72.616, 9.11.2026)
Found by the press of 1.72.615 at 390 px: the chart scaled to ~336 px, so 12-unit text drew at ~6 px, and the last labels were clipped because the page is RTL. Now: phone text 20-22 units (~11 px), every 6th month on phones, the SVG text forced LTR (time runs left to right), the last value and month anchored inside, a low point within 3 months of the last gets its label under the point. Copy: when the clipboard API refuses, the textarea copy runs.
