# Apartment designer: scoring rubric and method (HAD-701)

Version: draft 1, 2026-11-10. Parameter table: `features.csv` (78 parameters). Scoring code: `evidence/build_features.py` (Python standard library only; run `python -I build_features.py`). Draft hash of `features.csv` at writing: `sha256 676a9ad2…9b5625d6`. The lead session should re-hash at commit and treat that commit as the frozen pre-registration.

## 1. The claim this rubric must be able to test

Ben's target is "the highest level in the world … above them on every parameter". The engineering form of that claim is:

> For every parameter *p* in the frozen rubric, the nad-lan designer's measured value is **at least equal** to the best value of any benchmark product, and on every parameter with a continuous or ordinal measure it is **strictly better**, under the test protocol below.

Two consequences follow, and they are stated up front so nobody is surprised later.

1. **Strict superiority is impossible on a yes/no item that a competitor already passes.** One example is V04: Coohom's anonymous 360 link already works [LT]. On such items the honest claim is "equal". To claim "above", the item must also carry a continuous quality measure, for example time to open the link on a phone or MB transferred. Section 6 lists these companion measures.
2. **Unknown competitor values are taken at the vendor's word when testing *our* superiority.** If a vendor claims 12K renders, we must beat 12K, even though we could not verify the claim. This is the conservative direction, and it removes the easiest objection a sceptic would raise.

## 2. Products and versions under test

The baseline uses six deep products and one reference product: Planner 5D, Homestyler, Coohom, RoomSketcher, Floorplanner, Higharc Showroom, and GBuilder (reference, vendor evidence only). Every observation is dated 2026-11-10. SaaS products change weekly, so each re-measurement must record the date and, where visible, the build or version string. A comparison is only valid between measurements taken within 14 days of each other.

## 3. Parameter design rules

Every parameter in `features.csv` has six fields.

| Field | Content |
|---|---|
| `measure` | An objective test procedure a third party can repeat without asking us. It names the action, the observation and the pass condition. |
| `unit` | ms, MB, %, count, px, or a declared ordinal level. |
| Transfer function | Embedded in `measure`. It maps the raw value to a score from 0 to 100 and is declared before any product is measured. Continuous items use thresholds. Ordinal items use anchored levels, for example "0 toggle only; 50 minimap; 100 resizable split with live camera marker". |
| `weight_1to5` | Buyer value; see section 4. |
| Product columns | Raw observation, then `{class=…}`, then `(score n)`. |
| `evidence_urls` | One URL per product, dated 2026-11-10. |

**The 12 groups:**

| Group | Parameters | Weight sum | Share of total weight |
|---|---|---|---|
| visualisation | 9 | 27 | 10.2% |
| plan accuracy | 7 | 23 | 8.7% |
| 2D-3D link | 5 | 20 | 7.5% |
| catalogue and pricing | 6 | 23 | 8.7% |
| generation | 4 | 12 | 4.5% |
| collaboration and video | 7 | 28 | 10.6% |
| spec, BOM and cost | 6 | 25 | 9.4% |
| mobile UX | 6 | 22 | 8.3% |
| performance | 7 | 14 | 5.3% |
| accessibility and RTL | 8 | 22 | 8.3% |
| integration with project plans | 7 | 28 | 10.6% |
| trust and honesty labels | 6 | 21 | 7.9% |
| **Total** | **78** | **265** | 100% |

## 4. Weights (buyer value 1–5)

The reference persona is an Israeli buyer of a new-build apartment in a tower, inside the tenant-change window, possibly with a sales rep and an interior designer.

| Weight | Meaning | Example |
|---|---|---|
| 5 | Changes money or a binding decision, or decides whether the buyer can use the tool at all | C03 price on every item, S04 delta against base spec, A01 Hebrew UI, K04 video call, I01 starts from the real unit plan |
| 4 | Materially reduces a mistake or the effort of a decision | L02 synced split view, T04 data consistency, F04 time to canvas |
| 3 | Clear quality-of-life value | V03 render resolution, G01 style apply |
| 2 | Useful to some users | V09 video export, S06 CAD export |
| 1 | Marginal for this persona | V07 VR headset, P07 phone scan (the apartment does not exist yet) |

Sixteen parameters carry weight 5: V01, V02, P06, L01, C03, C04, K04, K05, S02, S03, S04, M01, A01, I01, I03, T01.

**Weight validation (required before the claim is published).** These weights are the researcher's proposal. Before any public claim, they are replaced or confirmed by a MaxDiff (best-worst scaling) survey of at least 30 recent or active Israeli new-build buyers, run on the 78 parameter names in plain Hebrew. If the Spearman rank correlation between survey utilities and these weights is below 0.7, the survey weights win. The decision is logged, and nothing else changes.

## 5. How the score is computed

For product *j* and parameter *i*:

- *s_ij* ∈ [0, 100] is the transferred score. It is **NA** when the parameter does not apply to the product type; for example, plan upload accuracy does not apply to a developer tool whose plans the builder authors. NA rows leave that product's denominator.
- *e_ij* is the evidence multiplier: live-tested **1.0**, seen-live **0.8**, vendor claim **0.6**, press **0.5**, review **0.5**, unknown **0**.
- *w_i* is the weight.

Three numbers are reported, never just one:

```
Verified score   V_j = Σ_i w_i · s_ij · e_ij  /  Σ_i w_i        (unknown counts as 0)
Claimed score    C_j = Σ_i w_i · s_ij         /  Σ_i w_i        (vendor claims at face value; unknown = 0)
Coverage         K_j = Σ_{i: e_ij = LT} w_i   /  Σ_i w_i        (share of weight we actually measured)
```

**Why unknown counts as 0.** From the buyer's side, a capability hidden behind a sign-up wall, or not documented at all, is not available at the moment they decide. It is not a judgement on engineering quality, which is why *C_j* and *K_j* are always shown next to *V_j*.

**Why the evidence multiplier exists.** Without it, a product with a long marketing feature list beats a product we actually measured. With it, vendor-only products cannot top the table on claims alone. GBuilder shows this: claimed 35.2, verified 22.7.

**Group scores** use the same formulas restricted to one group (`evidence/scores.csv`).

**For our own product, only [LT] evidence counts** (e = 1.0, or 0 if not measured). We do not grant ourselves vendor-claim credit.

## 6. The superiority test, parameter by parameter

| Measure type | Our requirement to count as "above" | Statistical basis |
|---|---|---|
| Continuous (ms, MB, %, px) | 5 runs each, same device, network and day. **Our worst run beats their best run.** | With n = 5 against n = 5, complete separation is the exact one-sided Mann–Whitney result (p ≈ 0.004). No distribution assumption. |
| Ordinal level (0/25/50/75/100) | Two independent raters, blind to brand where possible (screenshots cropped of logos). Weighted Cohen's κ ≥ 0.6 on the full set, and both raters place us strictly higher. | Inter-rater agreement guards against our own rater bias. |
| Binary (yes/no) | Pass on two devices (Android and iPhone), executed by a tester outside the build team. | Equal at best; see companion measures below. |
| Vendor-claimed competitor value | Treated as true. We must beat the claimed number. | Conservative. |
| Unknown competitor value (sign-up wall) | Measure it after a paid or trial sign-up done by Ben's team (we cannot create accounts), or mark the parameter "unresolved". **Do not count it as a win.** | No win by default. |

**Companion continuous measures for binary items that a competitor already passes:**

| Item | Companion measure |
|---|---|
| V04 | 360 share link: time to first frame on a phone, plus MB |
| K01 | Anonymous share: time to render on a phone (Coohom 11 s / 15.7 MB [LT]) |
| A06 | Zoom allowed, plus text still readable at 200% |
| I06 | Embed: added page weight in KB, plus CLS on the host page |
| L01 | 2D → 3D propagation latency in ms |

**Publication rule.** The public claim is generated from the table, not written by hand. It takes the form: "Equal or better than [named products] on N of 78 measured parameters, strictly better on M, measured [date], method [link]". If any parameter is lost or unresolved, the phrase "every parameter" is not used. This matches the owner's honesty rules: no worldwide-superiority claim without evidence.

## 7. Test environment for the decisive run

- **Desktop:** a Windows laptop with an integrated GPU (Intel Iris Xe class), Chrome stable, 1366x900, cold profile.
- **Phones:** one mid-range Android (Galaxy A5x class) and one iPhone 13 class. Real devices, not emulation, for every number that matters (M-group and F-group).
- **Network:** two profiles. "IL-4G" uses the median Israeli 4G throughput and RTT measured on the test day with a speed-test, logged. "Slow 4G" is 1.6 Mbps and 150 ms RTT, Lighthouse-compatible.
- **Runs:** 5 per measure, median reported, raw runs kept. Cold cache for "first" metrics; warm cache only where stated.
- **Tools:** the two zero-dependency CDP scripts used for this baseline, plus WebPageTest or Lighthouse for cross-checks. The scripts are `evidence/tools/probe.mjs` (landing and probe metrics) and `evidence/tools/interact.mjs` (scripted clicks, timings and screenshots), and the job files beside them reproduce every run. Run them with `node probe.mjs <jobs.json> <outDir>`.
- **The 2026-11-10 baseline used headless Chrome with software WebGL (SwiftShader).** Its 3D timings are upper bounds. Higharc's 3D did not finish rendering in that rig, which is the rig's limitation and not necessarily the product's. The decisive run must use a GPU.

## 8. Human-task measures (usability)

Several parameters (M01, M04, M05, K05, S02, T01) need human confirmation beyond the scripted checks.

- **Participants:** 12 Hebrew-speaking buyers or near-buyers of a new-build apartment, recruited without reference to nad-lan. Five find most usability problems; 12 gives a usable paired comparison.
- **Design:** within-subjects. Each participant uses our designer and the top-scoring competitor for that task. Order is counterbalanced.
- **Tasks:**
  1. Open unit 3B from the project page.
  2. Change the living-room floor to option X.
  3. Find the price difference.
  4. Walk to the balcony.
  5. Invite the designer to a call and hand her control.
  6. Export the spec sheet.
- **Metrics:**
  - task success (binary);
  - time on task (s);
  - error count;
  - SEQ (single ease question, 1–7) per task;
  - SUS (System Usability Scale, 0–100) per product.
- **Analysis:** paired Wilcoxon signed-rank on time and SEQ. Report the effect size (r) and the 95% CI of the median difference. Report every task, including those we lose.
- **Ethics and privacy:** recordings stay private. No contact details enter any share link, per the project rule.

## 9. Bias controls a sceptic will ask about

1. **Pre-registration.** The rubric file is committed and hashed before our build is measured. Weight or threshold changes after first measurement are forbidden, except through the MaxDiff rule in section 4, which is itself pre-declared.
2. **The rubric is target-shaped, and we say so.** About half of the weight measures fit to *our* scenario: Israeli catalogue, Hebrew, video co-design, developer integration. General-purpose planners are not designed for it, so they score low there. We therefore also publish a **neutral-subset score**: visualisation, plan accuracy, 2D-3D link, mobile UX, performance, and A04–A08. This shows whether we also lead on generic quality, where the incumbents are strong.
3. **Blind visual rating.** V06 is rated on brand-stripped screenshots by five raters. The current values are a single-rater preliminary and are labelled as such.
4. **Sensitivity.** Rankings are re-computed with equal weights and with ±1 random weight noise (10,000 draws). A ranking that flips under that noise is not reported as a ranking.
5. **Evidence asymmetry.** Our product gets only [LT] credit, while competitors get vendor-claim credit at 0.6. This favours them, deliberately.
6. **No click-bait thresholds.** Thresholds follow external norms where they exist: Core Web Vitals (LCP ≤ 2.5 s, CLS ≤ 0.1), Apple HIG 44 pt touch targets, WCAG 2.2 target size 24 px. Other thresholds are set in round steps declared in the CSV.

## 10. Baseline results (2026-11-10)

Format: **verified / claimed (live-tested share of weight)**, all 78 parameters, buyer weights.

| Scope | Planner 5D | Homestyler | Coohom | RoomSketcher | Floorplanner | Higharc | GBuilder (ref) |
|---|---|---|---|---|---|---|---|
| **ALL** | 19.8 / 29.9 (14%) | 20.3 / 30.7 (14%) | **29.9** / **39.5** (46%) | 17.1 / 23.7 (12%) | 19.1 / 20.8 (77%) | 25.7 / 32.8 (52%) | 22.7 / 35.2 (9%) |
| visualisation | 21.1 / 36.1 | 32.8 / 54.6 | **56.1 / 65.7** | 23.3 / 38.9 | 45.4 / 50.9 | 12.1 / 20.2 | 17.3 / 28.8 |
| plan accuracy | 11.1 / 18.5 | 16.3 / 27.2 | 21.5 / 35.9 | 24.8 / 41.3 | 19.5 / 19.5 | **38.9 / 50.0** | 30.0 / 50.0 |
| 2D-3D link | 27.0 / 45.0 | 27.0 / 45.0 | **52.0 / 70.0** | 47.0 / 65.0 | 27.5 / 27.5 | 40.0 / 50.0 | 9.0 / 15.0 |
| catalogue and pricing | 15.7 / 26.1 | 9.1 / 15.2 | 16.5 / 21.7 | 0 / 0 | 0 / 0 | 15.7 / 26.1 | **31.3 / 52.2** |
| generation | 21.2 / 35.4 | **23.3 / 41.7** | 17.5 / 29.2 | 0 / 0 | 20.0 / 25.0 | 12.5 / 12.5 | 15.0 / 25.0 |
| collaboration and video | 23.2 / 33.9 | 17.1 / 28.6 | **27.1 / 35.7** | 17.1 / 28.6 | 18.6 / 21.4 | 15.0 / 17.9 | 12.9 / 21.4 |
| spec, BOM and cost | **27.6 / 46.0** | 20.4 / 34.0 | 26.4 / 44.0 | 2.4 / 4.0 | 1.2 / 2.0 | 26.4 / 44.0 | 24.0 / 40.0 |
| mobile UX | 26.2 / 30.7 | 31.3 / 35.8 | **37.0 / 39.3** | 35.0 / 39.5 | 15.1 / 15.1 | 12.2 / 12.2 | 23.3 / 32.4 |
| performance | 19.6 | 10.7 | 42.9 | 30.4 | **44.6** | 32.1 | 28.6 |
| accessibility and RTL | 15.9 | 17.0 | 15.9 | **22.7** | 20.5 | **22.7** | 18.2 |
| integration with project plans | 22.5 / 37.5 | 22.5 / 37.5 | 27.9 / 46.4 | 4.3 / 7.1 | 17.9 / 22.3 | **65.0 / 82.1** | 45.0 / 75.0 |
| trust and honesty labels | 4.3 / 7.1 | 11.7 / 13.1 | 15.2 / 19.0 | 2.1 / 3.6 | 7.1 / 7.1 | 13.9 / 13.9 | **15.8 / 26.4** |

**Sensitivity** (`evidence/sensitivity.csv`):

| Variant | Ranking (verified score) |
|---|---|
| Buyer weights, all 78 | Coohom 29.9 > Higharc 25.7 > GBuilder 22.7 > Homestyler 20.3 > Planner 5D 19.8 > Floorplanner 19.1 > RoomSketcher 17.1 |
| Equal weights | Coohom 32.7 > Higharc 26.4 > GBuilder 23.6 > Homestyler 22.9 > Planner 5D 21.7 > Floorplanner 21.5 > RoomSketcher 19.5 |
| Neutral subset only | Coohom 41.9 > RoomSketcher 33.3 > Floorplanner 31.6 > Higharc 26.8 > Homestyler 24.5 > Planner 5D 22.3 > GBuilder 22.1 |
| Target-fit subset only | Higharc 24.9 > GBuilder 23.2 > Coohom 20.7 > Planner 5D 17.8 > Homestyler 17.0 > Floorplanner 9.6 > RoomSketcher 4.7 |
| ±1 weight noise, 10,000 draws | Coohom ranks first in 100.0% of draws |

**Reading.**

- **Coohom is the bar on generic quality.** It has path-traced 360 tours, a minimap with a view cone, and a product list.
- **Higharc is the bar on developer integration.** The real plan model drives 3D, options, lot rules and the lead.
- **No product exceeds 40 even on claims.** Each one covers part of the target experience and none covers the whole of it.

The scores are low by construction. The rubric measures *our* target experience, and none of these products was built for it. That is the opening, not an insult to them.

## 11. Limits of this baseline

1. **Sign-up walls.** Four of six editors required an account. Under the brief's rules (no accounts, no terms acceptance, no uploads), we could not measure Planner 5D, Homestyler, Coohom or RoomSketcher editors directly, and their editor values are vendor claims or unknown. Resolving them needs Ben's team to open trial accounts. Then P03 (recognition accuracy), L03 (switch latency) and K02 (co-editing latency) can be measured with the same scripts.
2. **Software WebGL.** 3D timings come from a GPU-less rig. Higharc's 3D never finished within 36 s here, and V06 and F04 should be re-measured on a GPU.
3. **Single-rater visual realism.** V06 needs the five-rater blind panel.
4. **Landing-page metrics** stand in for some mobile measures (M02–M04, A04–A06) because the designers themselves were walled.
5. **GBuilder** is scored entirely from vendor material. Its column is a reference, not a measured competitor.
6. **One snapshot.** Prices, features and payloads change. Re-measure within 14 days of any public claim.
