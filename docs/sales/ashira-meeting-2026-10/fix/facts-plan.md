# Ashira: facts and languages plan (HAD-543, 17.10.2026) - NOT part of the text-removal patch

Rule: no fact is changed until its current primary source is re-read and dated (the August ledger is not current clearance).

| item | where | what we see | source to re-read | proposed handling |
|---|---|---|---|---|
| floors of the two low buildings | facts strip (plugin/data) says 9 "per the design plan"; article says 8 | the design plan (dated 5.2023 on the stage, 5.2024 in the timeline) vs approved composition | TA municipality design plan file for lot 101 + the permit report (3.2026) | state the convention once ("8 floors + technical roof" or as the plan writes it) with its date; same in all 5 languages |
| design-plan date | stage/facts 5.2023 vs timeline 5.2024 | one is wrong | the municipal plan record | one dated value everywhere |
| room mix | HE 2-5 (two paragraphs); EN/FR/RU/AR 2-6 + penthouses | the official sources themselves differ (recorded in the ledger) | developer site ashirabyavisror.com today + latest marketing release | write the range with its source and date, or "2-5 (developer site), with larger units and penthouses in later releases" if that is what the sources say |
| sales figures | only HE (125 of 406 by 7.2026, ~72,000/m2 Q2 2026); foreign pages say no price data | parity gap | the developer's TASE report (company is listed since 8.2026) | same dated figure + source line in all languages |
| penthouse | HE 19.5M deal (8.2024, Globes); foreign 25M asking (old Ynet) | different facts, both may be true | Globes + Ynet items | foreign pages: the dated deal, the old asking price only as "asked at launch" |
| self-neighbour row | EN/FR/RU/AR neighbour table lists ASHIRA at 11 m | plugin: self-exclusion uses the HE post id, foreign posts have their own ids | code | exclude by project key, not post id; separate plugin release via the runner |
| translation slips | "collagen tanning" x4; RU/AR "small tower" for מגדלון | wording | - | wording fix in the four foreign posts |
| French map labels | "Prix a proximite", "Sante", "Cafes" | shared component, likely every French page | code | i18n string fix, separate release |
| generic designer | "Design the apartment" goes to /tour/designer/ (general 4-room example) | not an Ashira plan | - | label it as a general designer; no Ashira-official interior claim |
