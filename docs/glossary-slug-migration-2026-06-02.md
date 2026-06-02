# Glossary slug migration — 2026-06-02

Migrated all 22 `nadlan_term` slugs from Hebrew sentence-slugs to clean Latin concept
slugs. Done live via REST (owner app password). WordPress `_wp_old_slug` provides the
301 from each old Hebrew URL to the new one automatically (verified: every old URL → 301,
every new URL → 200, Hebrew titles unchanged).

**Why:** Hebrew slugs break reports/analytics/CLIs; several slugs were full
sentences/questions (article-style) rather than glossary concepts. See
`skills/url-namespace-contract.md`.

**Reversibility:** to revert any term, PATCH its slug back; `_wp_old_slug` will 301 the
Latin URL to the restored one. The mapping below is the record.

| id | Hebrew title (unchanged) | OLD slug (now 301s) | NEW slug |
|---|---|---|---|
| 3527 | עסקת קומבינציה | עסקת-קומבינציה | `combination-deal` |
| 3520 | התיישנות במקרקעין | התיישנות-במקרקעין-ההבדל-מהתיישנות-אזרחית | `statute-of-limitations-property` |
| 3512 | חשבון נאמנות בעסקת מקרקעין | חשבון-נאמנות-בעסקת-מקרקעין | `escrow-account` |
| 3505 | הפקעה | הפקעה | `expropriation` |
| 3498 | חכירה לדורות מול בעלות | חכירה-לדורות-מול-בעלות-מה-ההבדל-בפועל | `perpetual-lease` |
| 3490 | זכות קדימה | זכות-קדימה | `right-of-first-refusal` |
| 3482 | איך לקרוא נסח טאבו | איך-לקרוא-נסח-טאבו | `land-registry-extract` |
| 3080 | תשואה על הון עצמי | תשואה-על-הון-עצמי | `return-on-equity` |
| 3079 | רווח תפעולי נטו | רווח-תפעולי-נטו | `net-operating-income` |
| 3078 | שיעור היוון | שיעור-היוון | `cap-rate` |
| 3077 | לוח שפיצר מול לוח קרן שווה | לוח-שפיצר-מול-לוח-קרן-שווה-איך-לבחור | `spitzer-vs-equal-principal` |
| 3076 | לוח קרן שווה | לוח-קרן-שווה | `equal-principal-loan` |
| 1520 | גרייס (משכנתא) | גרייס-משכנתא | `mortgage-grace-period` |
| 1508 | יחס החזר חודשי | יחס-החזר-חודשי | `payment-to-income-ratio` |
| 1498 | יחס הלוואה לשווי | יחס-הלוואה-לשווי | `loan-to-value` |
| 690 | אלמנט מתועש | אלמנט-מתועש | `precast-element` |
| 689 | גשר תרמי | גשר-תרמי | `thermal-bridge` |
| 688 | בלוק תרמי | בלוק-תרמי | `thermal-block` |
| 687 | קורת מעבר | קורת-מעבר | `transfer-beam` |
| 686 | קיר דיפון | קיר-דיפון | `shoring-wall` |
| 685 | רפסודה (יסוד) | רפסודה-יסוד | `raft-foundation` |
| 684 | כלונס קדוח | כלונס-קדוח | `bored-pile` |

**Follow-ups (in BACKLOG):**
- Re-submit the new URLs in Google Search Console / ping the sitemap so Google recrawls.
- `/glossary/` archive still needs the entity-map redesign (Codex audit was right).
- Some `nadlan_project` / `nadlan_professional` pages lack a self canonical — fix via Yoast,
  single-source (do not double up on Yoast's canonical).
