# SERP Reverse Engineering

Goal:
Build against the actual SERP shape, not against guesses.

Required for each P0 keyword:
- Top 10 organic URLs. `NEEDS_VERIFICATION`
- SERP features: maps, local pack, AI answers, video, People Also Ask, images, calculators. `NEEDS_VERIFICATION`
- Winning page type: listing index, city hub, article, calculator, project page, directory, brand page. `NEEDS_VERIFICATION`
- Title/H1 patterns. `NEEDS_VERIFICATION`
- Content depth and unique data. `NEEDS_VERIFICATION`
- Schema usage. `NEEDS_VERIFICATION`
- Internal-link pattern. `NEEDS_VERIFICATION`
- Conversion surface. `NEEDS_VERIFICATION`

Output format:
| Keyword | Winner type | Top competitors | NadLan target page | Gap | Build/no-build |
|---|---|---|---|---|---|

Build rule:
Do not create a new page unless it has a distinct intent and a defined internal-link relationship to the money page.

