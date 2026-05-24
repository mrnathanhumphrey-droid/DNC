# Pre-registration v2.4 — DNC 2024 Post-Mortem (6-cohort × race interaction refinement on CES vote)

**Locks BEFORE running v2.4 fits.** Builds on:
- result_v1.1 (HEAD `122fc8c`): cohort × race interaction on CES vote (5-cohort) — Millennial × Hispanic -0.46, Millennial × Asian -0.38, GenZ × Asian +0.44, Boomer × Black +0.55 credible cells.
- result_v2.0 H6 (HEAD `d03e2dd`): 6-cohort recode — MillYoung (28-35) credibly defects -0.302 [-0.545, -0.077]; MillOld (36-43) borderline -0.218; GenZ flips +0.223 borderline-positive.
- result_v2.3 (HEAD `d810d63`): MillYoung Biden-2020 defection is 50% flip / 50% skip — qualitatively distinct from skip-dominated defection in other cohorts.

**Motivation.** v1.1's cohort × race finding (Mill × Hispanic / Mill × Asian credibly negative) used 5-cohort coding that collapses MillOld + MillYoung into one "Millennial" cell. v2.0 H6 + v2.3 now show MillYoung is the qualitatively-distinct defector. v2.4 re-runs the cohort × race interaction at 6-cohort resolution to localize which race × fine-cohort cells drive the defection signal.

This is **refinement** of a v1.1 finding using v2.0 H6's resolution, not new mechanism discovery — appropriate pre-reg target per user direction "keep going with open threads."

---

## 0. What this pre-reg LOCKS

- 4 v2.4 hypotheses (H16-H19), each anchored to a specific cell prediction
- 6-cohort × 6-race interaction Stan specification
- Falsification gates per cell
- Aggregate verdict reading

**What this pre-reg does NOT lock:**
- Cross-substrate replication (CES only)
- Causal interpretation
- Re-fit of other v1.1 outcomes (only vote)

---

## 1. v2.4 Hypotheses (LOCKED)

**Reference baseline:** v1.1 5-cohort interaction cells on CES vote (controlling 2020 recall):
- Millennial × Hispanic = -0.463 [-0.879, -0.103] CREDIBLE
- Millennial × Asian    = -0.379 [-0.822, -0.005] CREDIBLE
- GenZ × Asian          = +0.437 [+0.058, +0.856] CREDIBLE
- Boomer × Black        = +0.547 [+0.165, +0.964] CREDIBLE

### H16 — MillYoung × Hispanic carries more of the v1.1 Mill × Hispanic signal than MillOld × Hispanic

**Prior:** v1.1 found Millennial × Hispanic credibly negative. v2.0 H6 found MillYoung credibly negative + MillOld borderline. v2.3 found MillYoung is the active-flipper cohort. Prediction: MillYoung × Hispanic posterior mean MORE negative than MillOld × Hispanic posterior mean.

**Test:** Pull cohort_race_eff[MillYoung, Hispanic] and cohort_race_eff[MillOld, Hispanic] from 6-cohort × 6-race interaction Stan fit on CES vote.

**Falsification gates:**
- **CONFIRMED:** MillYoung × Hispanic mean ≤ MillOld × Hispanic mean - 0.10 AND MillYoung × Hispanic 95% CI < 0.
- **PARTIAL:** MillYoung × Hispanic mean negative AND ≤ MillOld × Hispanic mean (any margin) but CI crosses zero.
- **REFUTED:** MillYoung × Hispanic mean > MillOld × Hispanic mean (signal more in MillOld than MillYoung) OR MillYoung × Hispanic credibly POSITIVE.

### H17 — MillYoung × Asian carries more of the v1.1 Mill × Asian signal than MillOld × Asian

**Prior:** Same logic as H16 applied to Asian race cell.

**Test:** Pull cohort_race_eff[MillYoung, Asian] and cohort_race_eff[MillOld, Asian].

**Falsification gates:**
- **CONFIRMED:** MillYoung × Asian mean ≤ MillOld × Asian mean - 0.10 AND MillYoung × Asian 95% CI < 0.
- **PARTIAL:** MillYoung × Asian mean negative AND ≤ MillOld × Asian mean (any margin) but CI crosses zero.
- **REFUTED:** MillYoung × Asian mean > MillOld × Asian mean.

### H18 — GenZ × Asian remains credibly positive at 6-cohort resolution

**Prior:** v1.1 GenZ × Asian = +0.437 CREDIBLE. v2.0 H6 GenZ marginal +0.223 borderline-positive. Direct test: does the GenZ × Asian credible-positive cell survive the cohort recode?

**Test:** Pull cohort_race_eff[GenZ, Asian].

**Falsification gates:**
- **CONFIRMED:** 95% CI > 0 AND mean ≥ +0.20.
- **PARTIAL:** mean positive but CI crosses zero, OR mean in [0, 0.20].
- **REFUTED:** 95% CI < 0.

### H19 — MillYoung × Black: NEW prediction (not pre-reg'd previously)

**Prior:** v1.1 5-cohort Mill × Black was -0.27 [-0.66, +0.14] (not credible, downgraded in v1.1). v2.3 shows MillYoung defects at 19.8% rate; if MillYoung-flipping is concentrated by race, MillYoung × Black might surface as credibly negative at 6-cohort resolution.

**Test:** Pull cohort_race_eff[MillYoung, Black].

**Falsification gates:**
- **DEFECTION-CELL CONFIRMED:** 95% CI < 0 AND mean ≤ -0.20.
- **INDETERMINATE:** CI crosses zero OR mean ∈ (-0.20, +0.20).
- **ANCHOR-CELL:** 95% CI > 0 (MillYoung Black more retentive than other Mill cells — would surprise).

---

## 2. Operationalization (LOCKED)

### 2.1 Stan model

Re-use `model_a_interaction.stan` from v1.1 (existing file at `D:/DNC/code/stan/model_a_interaction.stan`). No changes to model spec; the only change is the cohort coding from 5-level to 6-level (driven by data prep).

### 2.2 Data prep

Outcome `vote_h6_x_race` on CES: same as v2.0 H6 (cohort recoded to 6-level Silent/Boomer/GenX/MillOld/MillYoung/GenZ) but using the INTERACTION model `model_a_interaction.stan` instead of marginal `model_a.stan`. New outcome name `vote_h6_x_race` in data_prep.py to keep distinct.

### 2.3 Sample

Same as v2.0 H6: CES Common Content + valid 2020 recall + valid 2024 major-party vote + valid demographics. N expected ≈ 42,028.

### 2.4 Fit configuration

Hardened settings consistent with v2.0.1: chains=6, warmup=1000, samples=1000, seed=42.

### 2.5 Cohort × race cells

6 cohorts × 6 races = 36 cells. Pre-reg focuses on 4 cells (MillYoung × Hispanic / MillYoung × Asian / GenZ × Asian / MillYoung × Black) as the primary verdicts. All 36 cells reported in result_v2.4 §3 table.

---

## 3. Aggregate verdict (v2.4)

- **MILLYOUNG IS DEFECTOR-RACE-SPECIFIC:** if ≥ 2 of {H16, H17, H19} CONFIRMED.
- **MILLYOUNG IS RACE-GENERAL DEFECTOR:** if H16 + H17 + H19 all NOT CONFIRMED but cohort_eff[MillYoung] (marginal) remains credibly negative as in v2.0 H6.
- **V1.1 INTERACTION FINDINGS DISSOLVE:** if H16 + H17 REFUTED.
- **GENZ ASIAN-PRO PERSISTS:** if H18 CONFIRMED (cross-validation of v1.1 + v2.0 H1.2).

---

## 4. Threats to validity

- **6-cohort split halves the MillYoung/MillOld cell N relative to v1.1 5-cohort fits.** Per v1.1: Mill × Hispanic n=349, Mill × Asian n=184. At 6-cohort split: MillYoung × Hispanic ≈ 150-200, MillYoung × Asian ≈ 80-110. Posterior CIs will be wider than v1.1.
- **Cell-level posterior width.** With smaller cell N, σ_cohort_race shrinkage pulls cells toward zero. The credibly-negative gate (95% CI < 0) is conservative; PARTIAL gate accepts directional evidence.
- **CES self-report.** Same caveat as v1.1; cells are conditional on self-reported 2024 vote.

---

## 5. v2.4 deviation log

| Date | Deviation | Rationale |
|---|---|---|

(Empty at lock; populated as v2.4 work surfaces discrepancies.)

---

**Locked at commit:** `[fill at commit]` on `main`.
**Repository:** https://github.com/mrnathanhumphrey-droid/DNC.
**Builds on:** result_v1.1 (HEAD 122fc8c) + result_v2.0 H6 (d03e2dd) + result_v2.3 (d810d63).
