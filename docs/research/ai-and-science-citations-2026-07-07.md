# AI-brain + science-layer citation bank (2026-07-07)
All citations verified against primary sources by 5 parallel research agents.
Implemented items are marked SHIPPED with the version.

## Prompting techniques (the AI brain, inc/ai-brain.php, v1.72.61)
- SHIPPED grounding constitution: Lewis et al. 2020, RAG, arXiv:2005.11401 (NeurIPS 2020).
  Hallucination evidence: Shuster et al. 2021, arXiv:2104.07567 - hallucination 68.2% -> 7.9% with retrieval.
- SHIPPED judge: Zheng et al. 2023, MT-Bench, arXiv:2306.05685 - GPT-4 judge >80% agreement with humans
  (position/verbosity/self-enhancement biases documented; we judge with an explicit rubric).
- SHIPPED refine: Madaan et al. 2023, Self-Refine, arXiv:2303.17651 - ~20% avg preference gain.
  Guard honored: Huang et al. ICLR 2024, arXiv:2310.01798 - intrinsic self-correction can degrade;
  our loop uses an external rubric + never-regress gate (length + dash-law re-check, fallback to draft).
- SHIPPED selective vote: Wang et al. 2022, Self-Consistency, arXiv:2203.11171 - GSM8K +17.9% abs;
  we fire it only in the 0.5-0.7 confidence band (cost-aware) and resolve to the conservative tier.
- CoT: Wei et al. 2022, arXiv:2201.11903 (GSM8K 17.9%->56.9% @ PaLM-540B; needs ~100B+ scale).
- Structured output: Willard & Louf 2023 arXiv:2307.09702 (Outlines); Beurer-Kellner 2024 arXiv:2403.06988;
  caution: Tam et al. 2024 arXiv:2408.02442 vs the dottxt rebuttal - schema-described JSON asks are safe (ours are).
- Personas: Zheng et al. 2023 arXiv:2311.10054 - personas do NOT improve factual accuracy (our house rules are
  constraints, not personas); Kong et al. NAACL 2024 arXiv:2308.07702 - role-play helps reasoning as a CoT trigger.
- Exemplars: Liu et al. 2021 arXiv:2101.06804 (KATE); Zhao et al. ICML 2021 arXiv:2102.09690 (calibration);
  Lu et al. ACL 2022 arXiv:2104.08786 (ordering).
- Chaining: Wu et al. CHI 2022, AI Chains, arXiv:2110.01691; Khot et al. ICLR 2023 arXiv:2210.02406 (DecomP).

## Science layer (engine, v1.72.62)
- SHIPPED sun-hours: Michalsky 1988, Solar Energy 40(3):227-235 (approx solar position, max err 0.01 deg);
  NREL SPA: Reda & Andreas 2004, Solar Energy 76(5) (0.0003 deg). Exposure framing: EN 17037:2018 daylight
  standard (direct sun >=1.5h min / 3h medium / 4h high on a reference day). UDI: Nabil & Mardaljevic 2005.
- SHIPPED TOPSIS compare pick: Hwang & Yoon 1981, LNEMS 186 (Springer); AHP: Saaty 1977 JMP 15(3);
  housing application: Ball & Srinivasan 1994, J Real Estate Finance & Economics 9:69-85.

## Armed for future cycles (infra exists, data/GPU gated)
- Honest price intervals: Romano et al. 2019 Conformalized Quantile Regression arXiv:1905.03222;
  spatially weighted conformal AVM: Hjort et al. arXiv:2312.06531; Bastos & Paquette 2025 JPR 42(1).
  (avm-deals.php armed; nadlan.gov.il ToS sign-off = owner decision.)
- Recommenders: Grbovic & Cheng KDD 2018 (Airbnb embeddings, +21% CTR) - needs behavioral data volume.
- NL search->filters: Spider EMNLP 2018 arXiv:1809.08887; Zillow NL search (industrial) - concierge roadmap.
- Floor-plan graphs: Graph2Plan SIGGRAPH 2020 arXiv:2004.13204; House-GAN ECCV 2020 arXiv:2003.06988;
  RPLAN dataset (80K plans) - borrow representations (adjacency graphs), not networks, for the studio.
- Walkability: Walk Score validations Carr 2010/2011 (r=0.74), Duncan 2011; 15-minute city Moreno 2021,
  Bruno et al. Nature Cities 2024 - per-category walking-time scores for project pages.
- Honest scarcity validated: Barton et al. 2022 J Retailing meta-analysis (scarcity raises intent);
  Tuncer 2023 BIT + Luguri & Strahilevitz 2021 JLA (fabricated cues destroy trust);
  Mathur et al. CSCW 2019 (581 sites caught faking low-stock - we compute from real inventory).
