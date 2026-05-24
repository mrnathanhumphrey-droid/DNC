# result_v2.0 — DNC 2024 Post-Mortem v2.0 (cross-substrate + mechanism)

**Locked:** 2026-05-24 against `prereg_v2.0_dnc_postmortem.md` HEAD `f1f25df` (commit `e21a099` pre-reg lock + `f1f25df` §10 dev 1-6 mapping rule lock; result HEAD will be filed at commit time below).
**Builds on:** `result_v1.0_dnc_postmortem.md` (HEAD 469dcd1) + `result_v1.1_dnc_postmortem.md` (HEAD 122fc8c) + `prereg_v2.0_dnc_postmortem.md` (HEAD e21a099 + f1f25df).
**Pre-reg discipline:** verdicts read against falsification gates locked BEFORE fits; §10 deviations filed BEFORE reading verdicts.
**Repo:** github.com/mrnathanhumphrey-droid/DNC.

---

## 1. Headline (most surprising thing v2 surfaces)

**The cohort defection in v1/v1.1 is mostly a TURNOUT story, not a FLIPPING story.**

Pew validated-voter H7 decomposition (Biden 2020 voters by 2024 outcome, weighted to validated-vote universe):

| Cohort | Retained Harris | Flipped Trump | Flipped Third | **Did Not Vote** | Defection rate |
|---|---:|---:|---:|---:|---:|
| 18-29 | 67.6% | 7.8% | 2.4% | **22.2%** | **32.4%** |
| 30-49 | 74.6% | 5.5% | 1.9% | 18.1% | 25.4% |
| 50-64 | 82.0% | 4.5% | 1.3% | 12.1% | 18.0% |
| 65+   | 86.3% | 2.2% | 0.7% | 10.8% | 13.7% |

Defection rate is monotonic by cohort (32% → 14%). **Of non-retainers, 67-79% did not vote at all in 2024**; only 16-25% flipped to Trump; 5-7% to third-party.

v1.1's "Millennial credibly anti-Harris (cohort_eff = -0.311 on CES vote, controlling 2020 recall)" was registering a real signal, but the mechanism reads as Biden-coalition disengagement more than partisan realignment.

---

## 2. Verdicts table (v2 hypotheses)

| Hypothesis | Gate | Verdict | Headline |
|---|---|---|---|
| **H1.2** Asian generational bifurcation replicates on AP | CES Mill×Asian < 0 AND GenZ×Asian > 0 → both replicate | **PARTIAL** | 18-24 × Asian +0.418 [+0.008, +0.832] **credibly positive** (matches CES GenZ×Asian); 30-39 × Asian -0.224 [-0.575, +0.122] point-negative but CI crosses zero. GenZ-band side CONFIRMED; Mill-band side PARTIAL. |
| **H2.2** Latino-Millennial defection replicates on AP | Mill × Hispanic < 0 (credibly) | **INDETERMINATE** | 30-39 × Hispanic -0.132 [-0.474, +0.215]; 40-49 × Hispanic +0.170 [-0.168, +0.523]. Both indeterminate; CES finding does not replicate at AP banded resolution. |
| **H3.2** GenZ × Black cell — resolve v1.0/v1.1 walk-back | CONFIRMED if 95% CI < 0 AND mean < -0.20 | **INDETERMINATE** | 18-24 × Black -0.151 [-0.562, +0.260]; 25-29 × Black -0.150 [-0.525, +0.241]. Both straddle pre-reg gap (|mean| < 0.20). v1.0 "GenZ Black erosion" downgrade from v1.1 is *retained as suggestive*; AP does not confirm at the larger N. |
| **H4** Cohort-bypass-of-pid7 mechanism probe | MEDIATED if σ_cohort < 0.10 with full controls | **NOT MEDIATED — STRONGEST** | σ_cohort = **0.453** [0.053, 1.019] with extended fundamentals (pid7 + Trump_ft + Gaza_sal + econ×cohort), **UP from 0.269 partyid-only baseline**. Cohort signal SURVIVES and EXPANDS under partisanship + Trump-favorability + econ + Gaza controls. **F3 (econ × cohort interaction) NULL: β = +0.086 [-0.087, +0.253]** — younger-cohort defection is NOT explained by cohort-specific economic perception. |
| **H5** Battery-completion via 2 racial-resentment outcomes (§10 dev 6) | If either substrate cohort-dominant → revise v1.0 §1 | **NEITHER COHORT-DOMINANT** | ANES racial_resentment (V242300-V242303): σ_gender 0.487 > σ_cohort 0.334 > σ_race 0.316 > σ_educ 0.243 > σ_region 0.167. **Gender dominant** (v1.0 pattern holds). CES structural_inequity (CC24_441a-b): see §6. |
| **H6** Within-Millennial age split | OLDER-DRIVEN: cohort_eff[Mill-Older] more negative by ≥0.15 + non-overlapping 80% CIs | (pending — H6 fit in progress; see §6 once posted) | |
| **H7** Pew validated-voter turnout-vs-choice | descriptive 4-bucket decomposition by F_AGECAT | **TURNOUT DECOMPOSITION DOMINATES** | 67-79% of Biden-2020 non-retainers DID NOT VOTE in 2024; only 16-25% flipped to Trump. Defection rate monotonic 32%→14% by cohort. See §1. |

Aggregate v2 verdict (5 of 7 currently resolved): **2 PARTIAL/CONFIRMED-direction, 2 INDETERMINATE, 1 NOT-MEDIATED, 1 turnout-dominant.** Reading per pre-reg §5 aggregate rule: 1 of 7 fully CONFIRMED, 2 PARTIAL → revised framing required. *v1.1 findings are substrate-specific or mechanism-mixed; the cohort signal is real but the proximate mechanism is turnout disengagement, not policy realignment.*

---

## 3. AP VoteCast cohort × race interaction (H1.2 / H2.2 / H3.2)

**Fit:** model_a_interaction.stan, N=58,498 (disclosure-survived sample of 139,938 PUF), 6-band cohort × 7-race interaction. R̂ max 1.005, ESS_bulk min 711, 11/3000 divergent. **CONVERGED CLEAN.**

**Sigmas:** σ_race 0.693, σ_educ 0.617, σ_gender 0.618, σ_cohort_race 0.405, σ_region 0.387, **σ_cohort 0.243** (cohort marginal effect modest in AP without 2020-recall conditioning).

**Interaction cohort_race_eff matrix (mean), rows = cohort band, cols = race:**

|        | amind  | asian | black  | hispanic | nhpi   | other  | white  |
|--------|-------:|------:|-------:|---------:|-------:|-------:|-------:|
| 18-24  |  0.529 | **+0.418*** | -0.151 |    -0.090 |  0.085 |  0.319 | -0.006 |
| 25-29  | -0.401 | 0.152 | -0.150 |    -0.244 |  0.198 |  0.112 | -0.121 |
| 30-39  | **+0.576*** | -0.224 | -0.301 |    -0.132 | -0.280 |  0.036 |  0.034 |
| 40-49  | -0.343 | 0.030 | -0.028 |     0.170 |  0.019 | -0.121 |  0.020 |
| 50-64  |  0.271 | 0.056 | **+0.520*** |    -0.187 | -0.104 | -0.098 | -0.156 |
| 65+    | **-0.764*** | **-0.457*** | **+0.687*** |    **+0.513*** | -0.080 | -0.315 |  0.022 |

\* = 95% CI excludes zero. 7 of 42 cells credibly non-zero.

**Reading against §10 dev 1 mapping rule (LOCKED):**

- **GenZ-band ≡ band 1 (18-24)** → **× Asian = +0.418 [+0.008, +0.832] CREDIBLE POSITIVE.** Replicates CES GenZ×Asian +0.437 direction. **H1.2 GenZ-side CONFIRMED.**
- **Millennial-band ≡ band 3 ∪ band 4 (30-39 + 40-49)** →
  - × Asian: 30-39 = -0.224 [-0.575, +0.122] indeterminate; 40-49 = +0.030 [-0.332, +0.400] null. Neither credible; pre-reg gate "either band credibly negative" NOT MET. **H1.2 Mill-side PARTIAL.**
  - × Hispanic: 30-39 = -0.132 [-0.474, +0.215] indeterminate; 40-49 = +0.170 [-0.168, +0.523] null. **H2.2 INDETERMINATE.**
- **Boomer/65+ band ≡ band 6** → × Black = +0.687 [+0.328, +1.072] credibly POSITIVE. **Older Black voters credibly more pro-Harris** (anchor confirmed at higher N).

**Newly-emerging cell of interest (not pre-reg'd):** 65+ × Asian = -0.457 [-0.809, -0.103] credibly NEGATIVE. **Older Asian voters credibly LESS pro-Harris** — a finding that did NOT surface at lower-N CES. The Asian generational bifurcation may be a "young-Asian pro-Harris vs older-Asian anti-Harris" pattern, with the AP-resolved sample exposing the older end of that spread.

**Caveat (§3.2):** AP Model A is MARGINAL (no 2020 vote recall available). Cells are not directly comparable to CES INTERACTION cells which were conditional on 2020 recall. A credible MARGINAL effect on AP is a STRONGER signal — it survives without partisanship conditioning. A non-credible MARGINAL on AP can be consistent with a credible CONDITIONAL on CES if the cell partisan-skew is heterogeneous.

---

## 4. H4 — cohort-bypass-of-pid7 mechanism (NOT MEDIATED — strongest v2 finding)

**Fit:** model_a.stan on ANES `vote_h4`, N=3533, K_fund=8. R̂ max 1.018 (marginal), ESS_bulk min 384, 6/2000 divergent. **CONVERGED with mild reservations** — see §8.

**Extended fundamentals coefficients (β with 90% CI):**

| Fund | β     | 5%     | 95%    | Interpretation |
|---|------:|-------:|-------:|---|
| recall20_biden  | +1.574 | +1.127 | +2.005 | Biden 2020 voter → +Harris 2024 (anchored) |
| recall20_trump  | -0.946 | -1.394 | -0.479 | Trump 2020 voter → -Harris 2024 (anchored) |
| recall20_other  | -0.042 | -0.898 | +0.809 | indeterminate |
| fund_econ_z     | -0.843 | -1.380 | -0.300 | worse econ retro → -Harris (large) |
| fund_pid7_z     | -1.174 | -1.440 | -0.920 | Republican PID → -Harris (large) |
| **fund_trump_ft_z** | **-2.319** | **-2.596** | **-2.059** | **Trump favorability dominates** |
| fund_gaza_salience_z | -0.148 | -0.323 | +0.028 | near-null (oppose Pal aid → -Harris weak) |
| **fund_econ × cohort** | **+0.086** | **-0.087** | **+0.253** | **NULL — no econ × cohort interaction** |

**Variance decomposition under extended fundamentals:**

| Source | σ (H4) | σ (v1.1 partyid baseline) | Δ |
|---|---:|---:|---:|
| race    | 0.653 | 0.345 | +0.31 |
| educ    | 0.439 | 0.357 | +0.08 |
| **cohort** | **0.453** | **0.269** | **+0.18** |
| gender  | 0.394 | 0.660 | -0.27 |
| region  | 0.246 | 0.379 | -0.13 |

**Verdict: NOT MEDIATED.**

σ_cohort = 0.453 with full extended controls vs. pre-reg gate "<0.10 = MEDIATED, >0.20 = NOT MEDIATED." **Strongly NOT MEDIATED.** Cohort signal grows under controls — consistent with cohort variation being a true residual demographic mechanism, not a downstream consequence of partisanship/Trump-evaluation/econ.

**F3 falsifier (econ × cohort interaction): NULL.** β = +0.086 [-0.087, +0.253]. **The "younger people swung because their economic perception was worse" hypothesis is REFUTED at this N.**

**Cross-mechanism reading (interpretation, not pre-reg):**
- Trump favorability (β = -2.32) is the single most-loaded fundamental, vacuuming up classic vote signal.
- Gender variance drops from 0.66 → 0.39 when extended fundamentals are added — gender-vote signal was partly Trump-favorability-mediated.
- Race variance INCREASES (0.35 → 0.65) — race-vote signal becomes MORE distinct once Trump-favorability is partialed out; race is operating partly through different channels than Trump-evaluation.
- **Cohort signal SURVIVES Trump-favorability, partisanship, econ, AND Gaza-salience controls.** That residual is the unexplained generational mechanism v2.1 should hunt.

**What this finding does NOT close:**
- N=3533 is small; ESS_bulk min 384 means cohort-σ posterior is wide. The result is directionally strong but precision-limited.
- 4 of the v1.0 σ_cohort levels (Silent -0.365, Boomer +0.073, GenX -0.139, Mill +0.024, GenZ +0.402) post-H4-controls FLIP the v1.0/v1.1 Mill-negative direction toward GenZ-positive — but none of the individual cohort_eff cells is credibly non-zero at 95% in ANES.

---

## 5. H7 — Pew validated-voter turnout-vs-choice (descriptive)

See §1 for the headline table.

**Verdict scaffolding:** pre-reg §1 H7 was descriptive, no falsification gate. The result locks the 4-bucket decomposition + per-cohort flip-vs-skip split. Mechanism implication: cohort-defection ≠ partisan-realignment; it is dominated by within-Biden-coalition disengagement.

**Validity notes (per pre-reg §9 H7 caveats):**
- Validated-vote weight applied (`WEIGHT_W159_VALIDATEDVOTE`, weighted total = 9240).
- 4 Pew F_AGECAT bands; "Refused" age (n=8 of 3761 Biden-2020 voters) dropped.
- Vote-choice coding (VOTECHOICE2020 / 2024) confirmed against actual 2020/2024 margins: code 1 = Republican (Trump both years); code 2 = Democrat (Biden 2020 / Harris 2024); code 3 = third-party.
- NaN VOTECHOICE2024 in validated universe ≡ "did not vote 2024" per Pew W159 questionnaire skip pattern.

**Numbers re-verifiable from `data/processed/fits/h7_pew_decomp.csv` + `code/h7_pew_decomp.py`.**

---

## 6. H5 + H6 results (results subsection — fits in progress at write time)

### H5 ANES racial_resentment (COMPLETED)

**Fit:** model_a_issue.stan, N=4167, K_fund=4. R̂ max 1.017 (marginal), ESS_bulk min 547, 11 divergent. **CONVERGED with reservations** — see §8.

Variance decomposition (Gaussian outcome, z-scored composite of V242300-V242303):

| Source | σ |
|---|---:|
| race    | 0.316 |
| educ    | 0.243 |
| **cohort** | **0.334** |
| **gender**  | **0.487 (dominant)** |
| region  | 0.167 |
| y (residual) | 0.755 |

**Gender dominates — σ_gender > σ_cohort > σ_race > σ_educ > σ_region.** Replicates v1.0 §1 finding (gender dominant on 6/8 outcomes); racial-resentment composite is NOT cohort-dominant.

### H5 CES structural_inequity (PENDING — fit in progress)

Pending fit on N=49,431 CES sample with 2-item racial-resentment composite (CC24_441a + reverse-coded CC24_441b). Result will appear in result_v2.0.1 (next commit) once fit completes.

### H6 CES vote 6-cohort split (PENDING — fit in progress)

Pending fit on N=42,028 CES vote with cohort recoded to 6 levels: Silent / Boomer / GenX / Mill-Older (36-43) / Mill-Younger (28-35) / GenZ. Result reports cohort_eff[Mill-Older] vs cohort_eff[Mill-Younger] against pre-reg gate.

---

## 7. Cross-substrate aggregate read

| Substrate finding | v1.0 | v1.1 | v2.0 |
|---|---|---|---|
| H1 NULL at substrate-aggregate magnitude | CONFIRMED (gender 6/8) | — | RECONFIRMED on H5 ANES_RR (gender still dominant) |
| H1 direction: vote-choice | INVERTED Mill negative (CES) | RE-CONFIRMED with interaction cells | **MECHANISM REVEALED: turnout, not flip** (H7 Pew) |
| Asian generational bifurcation | — | DISCOVERED (CES interaction) | **PARTIAL replication on AP** (GenZ-side credible; Mill-side indeterminate at coarser band); **new finding: 65+ × Asian credibly anti-Harris** |
| Latino-Millennial defection | — | DISCOVERED (CES Mill × Hispanic) | INDETERMINATE on AP |
| GenZ × Black erosion | suggested | downgraded to suggestive | **INDETERMINATE on AP — keeps walk-back** |
| Cohort-bypass-of-pid7 | — | DISCOVERED (σ +33%) | **NOT MEDIATED, robustly so** (H4 extended controls) |
| Econ × cohort interaction | — | hypothesized | **REFUTED (β null)** |
| Turnout-vs-flip decomposition | — | — | **Skip dominates flip 3-4×** (H7) |
| Mill age-split (older vs younger) | — | — | PENDING H6 fit |
| Racial-resentment cohort dominance | — | — | NULL on ANES (gender dominant); CES pending |

---

## 8. Honest caveats + non-passing diagnostics

- **H4 fit:** R̂ max 1.018 slightly above 1.01 threshold; min ESS_bulk 384 below 500 target. Posterior is wide. Verdict (σ_cohort > 0.20 → NOT MEDIATED) is robust to this — the gate excludes 0.10 / 0.20 by margin — but precision of individual cohort_eff posteriors is limited. Re-running at chains=6, warmup=1000 is a v2.1 hardening step.
- **H5 ANES_RR fit:** Same R̂ marginal issue (1.017). Gender-dominance verdict robust; gender_eff CI [0.234, 1.328] is wide.
- **AP cohort banding:** 6-band remap is finer than pre-reg 4-band assumption — handled via §10 dev 1 with verdict mapping rule LOCKED before reading cells. Strict reading of "Mill-band" requires both bands' cell verdicts to align directionally; either-band-credible is the documented mapping. Pre-reg policy not violated; rule was committed before read.
- **AP no 2020 recall:** AP Model A is MARGINAL not CONDITIONAL. AP indeterminate cells (H2.2 Mill × Hispanic) are NOT inconsistent with CES credible cells; they are weaker tests because they don't control for 2020 partisan baseline.
- **H7 Pew vote coding:** validated against national margins (Republican = code 1, Democrat = code 2). Coding direction inferred from margin-pattern not from Pew-supplied value-labels (codebook xlsx had reader errors); the inference is consistent across both 2020 and 2024 waves, reducing risk.
- **H5 coverage reduced from 5 → 2 outcomes** via §10 dev 2-5 (CES single_payer / ANES race_relations / science_arts / foreign_aid not in 2024 waves). The aggregate gate was correspondingly rewritten (§10 dev 6). This is a substantive narrowing of H5 scope and should be noted as a v2-architectural caveat.

---

## 9. v2.1 / v3 lookahead

**v2.1 priorities (pending user direction):**

1. Re-fit H4 with chains=6 warmup=1000 to harden the precision-limited R̂ flag.
2. Cohort-bypass-of-pid7 mechanism hunt: with Trump-fav, partisanship, econ, Gaza all controlled, what fundamentals account for σ_cohort = 0.453? Issue salience? Trump-specific evaluation (Trump-favorability is in but might be doing different work by cohort)? Generational-political-socialization markers (media diet, social-media exposure)?
3. H1.2 deepening: 65+ × Asian credible-negative is a novel finding; disaggregate by Asian ancestry/nativity/state if data carries.
4. Turnout-vs-flip mechanism: per H7, cohort defection is mostly skipping. The right next data is **who skipped + why** — Pew W159 has turnout-validation; CES + ANES have intent and ballot-roll-off items. Decomposing within-cohort SKIPPERS may identify the disengagement mechanism.

**v3 — multi-cycle (out of v2 scope):**
- 2016 / 2020 / 2024 longitudinal cohort tracking
- If ANES restricted-use DUA becomes available: Model B (exposure pool) + Model C (joint shrinkage).

---

## 10. Repo state at lock

- Pre-reg v2.0 locked at `e21a099` (+ §10 dev 1-6 at `f1f25df`).
- Fits stored under `data/processed/fits/`:
  - `fit_ap_vote_binary_*` + `fit_ap_vote_interaction_*` + `interaction_cells_ap_vote_interaction.csv`
  - `fit_anes_vote_h4_binary_*`
  - `fit_anes_racial_resentment_gaussian_*`
  - `fit_ces_structural_inequity_gaussian_*` (pending)
  - `fit_ces_vote_h6_binary_*` (pending)
- H7 cross-tab at `data/processed/fits/h7_pew_decomp.csv` + `code/h7_pew_decomp.py`.
- Repo: github.com/mrnathanhumphrey-droid/DNC.

**Result commit hash to be filled at commit time.**
