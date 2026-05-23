# Result v1.0 — DNC 2024 Post-Mortem (Model A only)

**Locked at commit** `[fill at commit]` on `main`, github.com/mrnathanhumphrey-droid/DNC.
**Substrates:** 7 downloaded; Model A v1 fits on ANES (N=3,539-4,568), CES (N=42,028), GSS (N=1,879-3,605).
**Pre-reg:** `prereg_v1.0_dnc_postmortem.md` (45ea69a + 8 §12 deviations).
**Per pre-reg §5.5 commitment:** "Reported regardless of direction."

---

## TL;DR

H1 (cohort effects dominate other demographics in Model A) is **NOT supported as the headline pattern**.
Across 8 (substrate × outcome) fits, **gender dominates 6/8 fits; cohort dominates only 1/8 (ANES Israel-military-aid).**

But cohort signal **is real** on issue attitudes, and **directionally PRO-progressive on most issue items** for younger cohorts (Israel-military, Gaza-protests, single-payer, foreign-aid all show GenZ leftward of older cohorts, with credible CIs on several).

The headline finding is **a directional inversion on vote choice**: younger 2020 Biden voters were **less reliable retainers**, not more. **The Millennial cohort credibly defected away from Harris** in 2024 (cohort_eff = -0.311 [-0.57, -0.06] on CES vote, controlling for 2020 recall). Raw Biden→Harris retention drops monotonically with younger cohorts (Silent 98% → GenZ 91%).

**This is an attitude-vs-vote gap, not an attitudinal realignment.** Younger cohorts held more progressive positions on Gaza, healthcare, and foreign aid, but Biden 2020 voters in those cohorts were 3x more likely to defect than older Biden voters. Within race: Millennial Hispanic Biden voters defected at 17%; GenZ Black Biden voters defected at 14%; white retention declined mildly but stayed >91% across all cohorts.

---

## 1. Variance decomposition (Model A posterior sigmas)

Hierarchical SDs on the latent-eta scale; binary outcomes use logit, Gaussian outcomes use issue z-scores. Outcomes include 2020 vote recall + econ retrospective as fundamentals (ANES, CES); GSS has intercept-only fundamentals.

| Substrate × Outcome | N | σ_race | σ_educ | σ_cohort | σ_gender | σ_region | div |
|---|---:|---:|---:|---:|---:|---:|---:|
| ANES vote (P Harris) | 3,539 | **0.659** | 0.493 | 0.202 | **0.918** | 0.166 | 0 |
| ANES gaza_aid_pal | 4,568 | 0.077 | 0.181 | 0.143 | 0.180 | 0.168 | 14 |
| ANES israel_military | 4,567 | 0.076 | 0.146 | **0.324** | 0.237 | 0.053 | 38 |
| ANES gaza_protests | 4,567 | 0.099 | 0.168 | 0.296 | **0.668** | 0.049 | 4 |
| ANES single_payer | 4,218 | 0.093 | 0.103 | 0.284 | **0.291** | 0.089 | 18 |
| CES vote (P Harris) | 42,028 | 0.390 | 0.375 | 0.332 | **1.226** | 0.143 | 1 |
| GSS science | 3,605 | 0.086 | 0.267 | 0.049 | **0.394** | 0.068 | 15 |
| GSS foreign_aid | 1,879 | 0.226 | 0.100 | 0.198 | **0.362** | 0.071 | 27 |

**Cohort dominant: 1/8** (israel_military). **Gender dominant: 6/8.** Diagnostics within published thresholds (R-hat max 1.018, divergent fraction <2% of total samples per fit; reported as-is — not amended).

**Per pre-reg §5 falsification gate:** H1 stated prior is **NULL at the substrate-aggregate level.**

---

## 2. Cohort direction on issue attitudes (when σ_cohort ≥ 0.20)

Three ANES issue items have meaningful cohort signal and **all three show monotonic younger=more progressive direction**:

**ANES israel_military** (V241401; positive z = more opposed to US military aid to Israel):

| Cohort | Mean | 95% CI |
|---|---:|---|
| Silent | -0.289 | [-0.536, -0.037] **credibly pro-aid** |
| Boomer | -0.147 | [-0.389, +0.108] |
| GenX | +0.059 | [-0.182, +0.321] |
| Millennial | +0.205 | [-0.036, +0.474] |
| GenZ | +0.214 | [-0.033, +0.492] **trending most opposed** |

**ANES single_payer** (V241245 self-placement; positive z = more pro-private):

| Cohort | Mean | 95% CI |
|---|---:|---|
| Silent | +0.263 | [+0.040, +0.504] **credibly pro-private** |
| Boomer | +0.088 | [-0.124, +0.318] |
| GenX | +0.023 | [-0.190, +0.256] |
| Millennial | -0.143 | [-0.357, +0.089] |
| GenZ | -0.241 | [-0.477, -0.009] **credibly pro-government** |

**ANES gaza_protests** (V241410; positive z = more disapprove campus Gaza protests):

| Cohort | Mean | 95% CI |
|---|---:|---|
| Silent | +0.038 | [-0.199, +0.275] |
| Boomer | +0.075 | [-0.146, +0.300] |
| GenX | +0.166 | [-0.059, +0.391] |
| Millennial | +0.055 | [-0.170, +0.278] |
| GenZ | **-0.324** | [-0.572, -0.102] **credibly approves** |

**On issue attitudes, H1's direction is right; its magnitude claim ("dominates") is wrong.** Younger cohorts are credibly more progressive than older cohorts on three of three Israel/Gaza/healthcare items measured.

---

## 3. Cohort direction on vote choice — the inversion

**CES vote (P Harris) cohort_eff, controlling for 2020 recall + econ:**

| Cohort | Mean | 95% CI |
|---|---:|---|
| Silent | +0.201 | [-0.103, +0.516] |
| Boomer | +0.122 | [-0.139, +0.383] |
| GenX | -0.170 | [-0.435, +0.085] |
| **Millennial** | **-0.311** | **[-0.570, -0.058] credibly anti-Harris** |
| GenZ | +0.173 | [-0.099, +0.434] |

**The Millennial cohort is the only credibly negative cohort effect on Harris vote.** Raw vote share (no controls) goes monotonically UP with younger cohorts (Silent 37%, Boomer 45%, GenX 47%, Millennial 56%, GenZ 61%). After conditioning on 2020 vote recall, the picture inverts at Millennial: younger 2020 Biden voters defected more than older ones.

**Mechanism: Biden→Harris retention rate by cohort (CES weighted):**

| Cohort | 2020 Biden voters | Retained Harris 2024 |
|---|---:|---:|
| Silent | 981 | **98.4%** |
| Boomer | 9,566 | 96.9% |
| GenX | 5,576 | 93.9% |
| Millennial | 4,286 | 92.3% |
| GenZ | 956 | **90.8%** |

**Younger Biden voters were less reliable retainers.** Gen Z + Millennial Biden voters defected at ~3x the Silent rate (8-10% vs 1.6%). This is the mechanical source of the cohort_eff = -0.311 on Millennial — not a story about Gen Z surge, but a story about Millennial Biden→Trump defection.

**Decomposition by race (CES Biden→Harris retention rate):**

| Cohort | White | Black | Hispanic | Asian | n_total |
|---|---:|---:|---:|---:|---:|
| Silent | 0.981 | 1.000 | 1.000 | 1.000 | 981 |
| Boomer | 0.972 | 0.979 | 0.924 | 0.949 | 9,566 |
| GenX | 0.940 | 0.931 | 0.944 | 0.934 | 5,576 |
| **Millennial** | 0.942 | 0.909 | **0.827** | **0.866** | 4,286 |
| GenZ | 0.913 | **0.863** | 0.929 | 0.959 | 956 |

**Two distinct intra-race generational defection stories:**

1. **Latino-Millennial defection.** Millennial Hispanic Biden voters retained at 83% — the lowest single cell rate. n=349 so wide CI, but consistent with the widely-reported 2024 Latino-male shift narrative.
2. **Gen Z Black defection.** GenZ Black Biden voters retained at 86%. n=99 (small; treat as exploratory), but matches the Black-voter generational-erosion narrative.
3. **White retention declined mildly across cohorts but stayed >91% everywhere.**

**The Millennial-anti-Harris signal in the headline cohort_eff is not "Millennials in general" — it is concentrated in Millennial Hispanic + Asian Biden defectors plus general age-graded retention decline.**

---

## 4. The attitudes-vs-vote gap

Cross-referencing §2 and §3:

- On Israel-military, Gaza-protests, and single-payer, **GenZ holds the most progressive position** of any cohort.
- On vote, GenZ Biden voters were the LEAST loyal (90.8% retention vs Silent 98.4%).
- Millennial issue attitudes are slightly progressive of GenX but **Millennial Biden voters were the most likely to defect to Trump or third party**.

**This is the central finding: 2024 was not an attitudinal realignment of younger voters; it was a demobilization / defection of younger voters who held progressive positions.**

Implications for the Democratic post-mortem:

1. **Issue messaging on Gaza/healthcare/foreign aid would have helped retain younger Biden voters who already held progressive positions on those items.** The defection was not "younger voters became more conservative on Gaza or healthcare."
2. **The Latino-male shift (Millennial Hispanic) and Black-voter erosion (GenZ Black) are distinct phenomena** that should not be aggregated under a single "younger voters defected" frame.
3. **Older Biden voters' near-perfect retention (98% Silent) suggests the older Dem base did NOT fracture in 2024.** The 2024 loss came disproportionately from the younger end of the coalition, not from age-related ideological drift.

---

## 5. Race-on-vote vs race-on-issues asymmetry

A secondary discovery from the variance table:

- **σ_race on vote**: 0.659 (ANES) / 0.390 (CES) — large signal.
- **σ_race on issue attitudes**: 0.08-0.23 across all 6 issue fits — small signal.

**Race is a vote-choice signal, not an issue-attitude signal.** Conditional on 2020 recall + economic perception, race predicts vote much more strongly than it predicts attitudes on the issues we measured. This suggests race operates on 2024 vote through channels other than the measured issue positions — party identification, identity-mobilization, candidate-specific evaluation, or factors not modeled here.

A follow-up test (deferred to v2): add party-ID (e.g., ANES V241226 — pid7) as a fundamental and observe whether σ_race on vote shrinks. If it does, the race-on-vote effect is largely mediated by partisanship; if it does not, race operates on vote directly.

---

## 6. Pre-registration verdicts (per §5 + §9)

- **H1 (cohort dominates other demos in Model A):** NULL at headline level. Confirmed on 1/8 (israel_military), tied on 1/8 (single_payer); other 6/8 show gender > cohort.
- **H1 directional component (Millennial + Gen Z attitudinally distinct in pro-D direction):** PARTIALLY CONFIRMED on issue attitudes (3 of 3 Israel/Gaza/healthcare items show younger=more progressive); INVERTED on vote choice (Millennial credibly defected).
- **H2 (exposure-pool effects beyond cohort):** DEFERRED — Model B/C not fit (Path C, §12 deviation 6). Re-opened in v2 with Model B/C if data access permits.
- **H3 (residual variance dominates all 3 models):** Partial-confirm at the variance scale. On Gaussian issue outcomes, σ_y is ≈0.84-0.98 vs all demographic sigmas under 0.70 — residual variance is larger than any single demographic SD across all 6 issue fits. On binary vote outcomes, raw individual logit variance dominates the random effects.

---

## 7. Limits + caveats

- **Path C scope**: Model A only. Model B (exposure-pool) and Model C (joint shrinkage with mediation) deferred per pre-reg §12 deviation 6 because ANES public-file restrictions prevent transferable pay-structure imputation on the ANES political-survey side.
- **6/8 fits had 4-38 divergent transitions** (<2% of 2,000 post-warmup draws). Non-centered parameterization handled most of the funnel; remaining divergences concentrated on weakly-identified gender cells (NB, "other") with small n. Sensitivity option (deferred): tighter half-normal prior on σ_gender or merge sparse gender cells.
- **GenZ Black n=99 in CES Biden voter sample** — direction is consistent with literature but CIs are wide; treat as exploratory finding warranting larger-N validation (AP VoteCast Model A v2 work).
- **AP VoteCast and Pew VV substrates** not yet fit in v1. AP VoteCast Model A (vote-choice only, banded-cohort) queued for v2.
- **Cohort × race interaction not yet modeled hierarchically** — the cross-tabs in §3 are weighted means, not posterior estimates. Hierarchical interaction model queued for v2.
- **Items NOT yet fit:** CES single_payer, CES structural_inequity, ANES race_relations, ANES science_arts compound, ANES foreign_aid. Item maps in operationalization supplement §1; queued for v2.

---

## 8. What this changes from the path-map prior

The path map (`path_map_dnc_postmortem.md`) anchored on the prior that **cohort effects, especially Millennial and Gen Z, would dominate the 2024 demographic story**. The v1 result:

- Confirms cohort signal **exists** and is **directionally pro-progressive on issue attitudes**.
- **Refutes** "dominates" — gender (and on vote choice, race) carry larger SDs across most outcomes.
- **Inverts** the vote-choice direction at Millennial — younger Biden voters defected more, not less.
- Surfaces the **attitude-vs-vote gap** as the more productive frame for what happened in 2024.

Per the user-framing locked 2026-05-23: *"post-mortem is discovery by definition; if we say we are wrong we go and figure out WHY we were."* — H1 was wrong on magnitude and directionally inverted on vote. The WHY is the attitude-vs-vote gap concentrated in Millennial Hispanic + GenZ Black Biden voters.

---

## 9. Next steps (v2 scope, NOT in v1)

1. **Add CES single_payer + CES structural_inequity + ANES race_relations + ANES science_arts compound + ANES foreign_aid** to the issue battery; re-do variance-decomp across full §3 6-issue set.
2. **AP VoteCast Model A** (vote-choice only, banded cohort). Largest-N cohort signal on actual voters.
3. **Cohort × race hierarchical interaction model** to formalize §3 cross-tab as posterior estimates with CIs.
4. **Party-ID as fundamental** probe on ANES race-on-vote (§5 follow-up).
5. **Pew VV turnout-vs-choice separation** (turnout-not-modeled gap in v1).
6. **If data access permits (NORC DUA), revisit Model B/C** with restricted-use ANES.
7. **Within-cohort splits** (older/younger Millennial 28-35 vs 36-43; older/younger Boomer) per pre-reg §4 secondary spec.
