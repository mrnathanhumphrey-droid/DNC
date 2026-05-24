# Pre-registration v2.1 — DNC 2024 Post-Mortem (Cohort-bypass mechanism hunt)

**Locks BEFORE running v2.1 fits.** Builds on:
- `prereg_v2.0_dnc_postmortem.md` (HEAD e21a099 + §10 dev 1-7 at d03e2dd)
- `result_v2.0_dnc_postmortem.md` (HEAD d03e2dd)
- Specifically: result_v2.0 §4 H4 finding **σ_cohort = 0.453 [0.053, 1.019] NOT MEDIATED** by extended fundamentals (2020 recall + econ + pid7 + Trump_ft + Gaza salience + econ×cohort).

**Motivation.** v2.0 H4 left the cohort signal unexplained after the strongest fundamental controls in the literature. The pre-registered F3 econ × cohort interaction was NULL, refuting one specific mechanism. v2.1 systematically probes alternative mediators with falsification gates locked BEFORE fits.

Per user framing 2026-05-24: *"pre reg it all"* (from v2.0 lock, reaffirmed for v2.1 by extension).

---

## 0. What this pre-reg LOCKS

- 5 v2.1 hypotheses (H8-H12), each with stated prior + falsification gate
- Mediator variable V-codes for ANES 2024 (PRE + POST items)
- Composite construction rules
- Verdict thresholds per hypothesis + aggregate gate

**What this pre-reg does NOT lock:**
- Manuscript-prose writing (out of scope per session protocol)
- CES/Pew analyses (ANES only — these probes require ANES-specific items not in cross-substrate harmonization)
- Re-fit at hardened convergence (v2.0.1 cleanup already addressed)

---

## 1. v2.1 Hypotheses (LOCKED)

**Reference baseline:** v2.0 H4 (model_a.stan on ANES `vote_h4`, N=3533, K_fund=8): σ_cohort = **0.453 [0.053, 1.019]** with full controls. Each v2.1 hypothesis adds a new mediator and asks: does σ_cohort shrink?

**Common falsification gates (apply per hypothesis):**
- **MEDIATED:** σ_cohort posterior mean shrinks to **< 0.15** with mediator added.
- **PARTIALLY MEDIATED:** σ_cohort ∈ [0.15, 0.25].
- **NOT MEDIATED:** σ_cohort ≥ 0.25 (cohort signal robust to the mediator).

Each hypothesis reports the mediator's β coefficient with 90% CI, AND the σ_cohort posterior in the augmented model.

### H8 — Ideology (liberal-conservative self-placement) × cohort

**Prior:** Ideology is the canonical "summary fundamental" in voting research. If younger cohorts defect because they're more liberal (in self-identification), σ_cohort should shrink substantially when ideology is added.

**Test:** Add `fund_ideo7_z` = z-score of V241177 (PRE: 7PT SCALE LIBERAL-CONSERVATIVE SELF-PLACEMENT, 1=extreme liberal, 7=extreme conservative, 99=haven't thought DROPPED, -9/-8 DROPPED) to the H4 K_fund=8 baseline. K_fund_new = 9.

**Falsification gates:** as common gates above.

### H9 — Trust-in-government composite × cohort

**Prior:** Younger cohorts plausibly defect due to lower trust in government/courts and higher corruption perception. This composite tests whether trust mediates cohort effect.

**Test:** Add `fund_trust_gov_z` = z-score of equally-weighted mean of:
- V241229 (PRE: HOW OFTEN TRUST GOVT IN WASHINGTON; 1=always, ..., 5=never, where higher = LESS trust)
- V241230 (PRE: HOW OFTEN TRUST COURT SYSTEM; same 1-5)
- V241233 (PRE: HOW MANY IN GOVERNMENT ARE CORRUPT; 1=all, ..., 5=none, where higher = LESS corruption perceived; REVERSE so higher = MORE corruption perceived)
- V241235 (PRE: ELECTIONS MAKE GOVT PAY ATTENTION; 1-5 some direction; higher = LESS efficacy after reverse-coding if needed)

After reverse-coding each so that **HIGHER = LESS political trust / MORE cynicism**, take mean, z-score → `fund_trust_gov_z`. Negatives (-9, -8, -1) dropped per-item. Composite computed only for respondents with ≥3 of 4 items non-missing.

K_fund_new = 9.

**Falsification gates:** common gates above.

### H10 — Anti-system / populist sentiment composite × cohort

**Prior:** "The system is rigged against ordinary people" is a populist register that may correlate with cohort-specific disengagement. Tests whether anti-system sentiment absorbs the cohort signal.

**Test:** Add `fund_antisystem_z` = z-score of equally-weighted mean of:
- V242304 (POST: "Our political system only works for insiders with money and power"; 1=describes very well, ..., 5=does not describe at all; REVERSE so HIGHER = MORE anti-system)
- V242305 (POST: "Because of rich and powerful it's difficult for rest to get ahead"; same scale; REVERSE)

After reverse-coding so HIGHER = MORE anti-system sentiment, take mean, z-score → `fund_antisystem_z`. Negatives dropped. K_fund_new = 9.

**Falsification gates:** common gates above.

### H11 — Trump favorability × cohort INTERACTION (heterogeneous slope)

**Prior:** v2.0 H4 included Trump_ft as a MAIN effect (single β = -2.319). If Trump_ft has DIFFERENT slopes by cohort (e.g., Trump_ft maps to Harris-vote-flip more steeply for some cohorts than others), the cohort-residual signal may be a "heterogeneous Trump-evaluation" story rather than a true generational mechanism.

**Test:** Add `fund_trump_ft_x_cohort` = z-scored Trump_ft × cohort_idx (numeric 1-5 for Silent..GenZ). This is the same construction as v2.0 H4's F3 (econ × cohort) but with Trump_ft replacing econ. K_fund_new = 9.

**Falsification gates:** common gates above, PLUS report the β of the interaction term itself with 90% CI:
- **TRUMP-FT HETEROGENEOUS:** interaction β 95% CI excludes zero AND σ_cohort shrinks ≥ 0.10.
- **TRUMP-FT HOMOGENEOUS:** interaction β CI crosses zero.

### H12 — Party identity importance × cohort

**Prior:** Younger cohorts may have weaker partisan identities and therefore weaker partisan-loyalty defaults. If party-identity-importance mediates cohort effect, this points at "weaker tribal identity → freer defection" mechanism.

**Test:** Add `fund_pid_import_z` = z-score of V241228 (PRE: PARTY IDENTITY IMPORTANCE; 1=extremely important, ..., 5=not at all important; REVERSE so HIGHER = MORE important). Negatives dropped. K_fund_new = 9.

**Falsification gates:** common gates above.

---

## 2. Aggregate verdict (v2.1)

After running all 5 hypotheses individually:

- **MECHANISM IDENTIFIED:** ≥1 hypothesis reaches MEDIATED gate (σ_cohort < 0.15).
- **MECHANISM PARTIAL:** ≥2 hypotheses reach PARTIAL gate (σ_cohort 0.15-0.25), or 1 reaches MEDIATED.
- **MECHANISM RESIDUAL:** ALL 5 hypotheses report NOT MEDIATED (σ_cohort ≥ 0.25). Reading: cohort signal in ANES vote is RESIDUAL to ideology + trust + anti-system + Trump-favorability-heterogeneity + party-identity-importance. This would be the strongest possible reading — the cohort effect is something not measured by the standard ANES political-attitudes battery, pointing at v3 candidates: media diet / generational-political-socialization markers / cohort-specific event exposure.

**Pre-reg commits to reporting the aggregate verdict explicitly, including MECHANISM RESIDUAL if it obtains.**

---

## 3. Operationalization (LOCKED)

### 3.1 Data file

ANES 2024 Time Series CSV (HEAD-verified at `D:/DNC/data/raw/anes_2024/anes_timeseries_2024_csv_20260519.csv`).

### 3.2 Sample frame

Same as v2.0 H4: respondents with valid 2024 PRES vote (V242096x ∈ {1, 2}), valid 7-pt party-ID (V241227x > 0), valid demographics, valid 2020 recall. **Additional per-hypothesis:** drop respondents with missing mediator(s) for the augmented model (per-hypothesis sample-N reported).

### 3.3 Stan model

Same `model_a.stan` (binary logistic, hierarchical demographic + cohort + fundamentals). Each H8-H12 augmented model has K_fund = 9 (vs H4 baseline K_fund = 8).

### 3.4 Fit configuration

**MUST USE hardened settings (per v2.0.1 cleanup):** chains=6, warmup=1000, samples=1000, seed=42. This matches the v2.0.1 H4 hardened re-fit reference baseline.

### 3.5 Reference baseline

σ_cohort posterior mean and 90% CI from `fit_anes_vote_h4_binary_hardened` (v2.0.1 cleanup, commit will be tagged in §6 below).

---

## 4. Verdicts

Each hypothesis verdict reported as one of: **MEDIATED**, **PARTIALLY MEDIATED**, **NOT MEDIATED**, plus the mediator's main β.

Aggregate verdict per §2.

---

## 5. Threats to validity

- **Sample-N attrition.** Each augmented model loses respondents with missing mediator. The σ_cohort comparison vs baseline is only valid if N is roughly comparable; report N per fit and flag if N drops >5% from H4 baseline.
- **Collider bias.** Adding mediator-as-fundamental may induce collider bias if cohort → mediator → vote AND cohort → vote directly. The pre-reg here is descriptive ("does the mediator absorb the cohort variance"), not causal-identification. Reading is associational.
- **Single-substrate (ANES).** All H8-H12 are ANES-only. Cross-substrate replication of MEDIATED mediators is v3.

---

## 6. v2.1 deviation log

| Date | Deviation | Rationale |
|---|---|---|

(Empty at lock; populated as v2.1 work surfaces discrepancies.)

---

**Locked at commit:** `[fill at commit]` on `main`.
**Repository:** https://github.com/mrnathanhumphrey-droid/DNC.
**Builds on:** prereg_v2.0 + result_v2.0 (HEAD d03e2dd).
