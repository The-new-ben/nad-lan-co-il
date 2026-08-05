# Meier on Rothschild - Chrome source verification

Verification date: 2026-08-05

Browser: the connected Google Chrome session, with Google set to English and Israel for the supplementary protected-source checks. The four localized search-intent runs are recorded separately in `01-live-google-intent-ledger.md`.

## Directly rendered source checks

- S10, Ministry of Justice Land Registry Extract: rendered at the frozen URL with the title `Generation of a Land Registry Extract (Tabu Extract) from the Land Registers | Land Registry and Settlement of Rights`. The visible H1 matched the service name. The page description says that any person can order a Land Registry extract for a fee.
- S11, Israel Tax Authority purchase-tax simulator: rendered at the frozen URL with the title `Simulator – Calculator for calculating property purchase tax | Israel Tax Authority`. The visible H1 matched the calculator name. The page description says that purchasers can calculate the purchase tax legally due when buying a property right.
- S15, Calcalist Menora Allenby report: rendered with the headline `דיירי מגדל מאייר מתנגדים לבניין החדש של מנורה בת"א - "יחסום את האוויר"`, publication time `13:02, 16.03.25`, and a description referring to residents' objections concerning light, view and privacy and to a 45-storey mixed-use proposal.
- S17, Calcalist 2019 transaction report: rendered with the title `מתיו ברונפמן רכש את אחת מדירות הפנטהאוז במגדל מאייר - תמורת 50 מיליון שקל`.
- S18, Calcalist 2013 transaction report: rendered with the title `דירה במגדל "מאייר ברוטשילד" בת"א נמכרה ב-21 מיליון שקל`.
- S19, MeierArchitects official Rothschild Tower record: rendered at the exact source URL with the title `Rothschild Tower | MeierArchitects`. The visible `Facts and Figures` block publishes `33,000 sm`, `42-story` and `158-meter-high`, and classifies the project as residential and commercial.
- S20, Globes report dated 15 May 2019: rendered at the exact source URL with the headline `12 שנים של שיווק: מתיו ברונפמן רכש את הדירה האחרונה במגדל מאייר בת"א`. The visible article text reports the final developer apartment sale and states that the tower contained `42 קומות ו-100 דירות בפועל`, meaning 42 floors and 100 apartments in practice, including six penthouses and duplexes.

## Security-gated sources

- S06, The Skyscraper Center: the direct page stopped at a security-verification screen. A live Google Israel result for the exact frozen URL displayed the result title `Rothschild Tower` and the snippet `154 m / 505 ft`. No fact that depended only on an unread portion of the gated page was added.
- S07, UNESCO: Chrome opened the exact frozen URL and exposed the tab title `White City of Tel-Aviv – the Modern Movement - UNESCO World Heritage Centre`, but the page body did not remain readable through the browser-control layer. The source is retained for the frozen White City context already established in the source ledger.
- S08, NTA Allenby station: the exact frozen URL stopped at a security-verification screen. The page was not represented as fully read during this pass. The source remains in the frozen ledger for the Allenby Red Line station fact established in the earlier research.

## Access interpretation

A browser security gate is an access limitation, not evidence that a source is false or that its URL is broken. The package keeps these URLs because they are the fixed common source set, while limiting article claims to facts supported by the frozen ledger and corroborating accessible sources. The directly rendered S19 and S20 records required the frozen ledger to preserve the public 154-versus-158-metre conflict and the 147-project-versus-100-in-practice apartment-count conflict. No CAPTCHA was bypassed and no protected page was claimed as directly read when it was not.
