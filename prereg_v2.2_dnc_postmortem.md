# Pre-registration v2.2 — DNC 2024 Post-Mortem (Cohort-axis discovery + confirmation)

**Locks BEFORE running v2.2 discovery + confirmation.** Builds on:
- result_v2.1 (HEAD `27a0093`): **MECHANISM RESIDUAL** — cohort signal NOT MEDIATED by ideology / trust / anti-system / Trump_ft × cohort / party-ID importance.

**Motivation.** v2.1 ruled out 5 a-priori-plausible mediators. The cohort signal sits in *some* direction in the available ANES covariate space; v2.2 attempts to **discover** that direction via penalized regression on a candidate item pool, then **confirm** the discovered axis via Stan refit on a held-out sample.

**Discovery-vs-confirmation discipline.** v2.2 is explicitly a discovery exercise. The discovery procedure (lasso on training half) will produce candidate mediators; the verdict reads from the CONFIRMATION step (Stan on test half) against pre-reg gates locked here.

Per user framing 2026-05-24: *"yes go the cleanest route"* (Approach 1 sample-split + Approach 2 lasso selection).

---

## 0. What this pre-reg LOCKS

- Candidate item pool (38 ANES items, exact V-codes below)
- 50/50 sample split protocol + seed
- Lasso discovery procedure + retention rule
- Stan confirmation model + verdict gates
- Aggregate verdict reading

**What this pre-reg does NOT lock:**
- The identity of the items retained by lasso (that's the discovery output)
- Causal interpretation (v2.2 is descriptive; cohort-axis characterization is associational)
- Cross-substrate replication (v3)

---

## 1. Candidate item pool (LOCKED — 38 items)

### A. Issue battery summary x-vars (21 items)

V241187x (Biden drop), V241287x (colleges run), V241290x (DEI), V241319x (voter ID), V241322x (felons vote), V241330x (president-bypass-courts), V241333x (restrict journalist), V241344x (corruption-under-Biden), V241347x (Manhattan jury), V241350x (president-immune), V241353x (Trump treated unfairly), V241372x (trans bathroom), V241375x (abortion ban), V241381x (gay-lesbian adopt), V241389x (birthright citz), V241392x (children brought illegally), V241395x (border wall), V241400x (weapons to Ukraine), V241403x (military aid to Israel), V241406x (humanitarian aid Palestinians), V241350x already listed (omit second).

**Drop from issue pool per >20% missingness rule:** V241385x (gay-marry, 53% miss).

### B. Candidate trait items (8 items)

V241201 / V241202 / V241203 / V241204 (Harris: cares / knowledgeable / honest / energetic).
V241206 / V241207 / V241208 / V241209 (Trump: same 4).

### C. Values + system items (3 items)

V241325 (separation of powers important), V241327 (agree-on-facts important), V241335 (media trust).

### D. Trust + efficacy items (4 items)

V241229 (trust govt), V241230 (trust courts), V241233 (corruption-in-govt), V241235 (elections make govt respond).

### E. Identity + engagement (2 items)

V241210 (care who wins), V241228 (party-ID importance).

**Drop per >20% missingness:** V241222 (strong-partisan; conditional on having a partisan ID — 36% miss).

### F. Ideology (1 item)

V241177 (7pt liberal-conservative self-placement; recode 99="haven't thought" as missing).

### G. Religion (1 item)

V241420 (religion importance).

**Drop per >20% missingness:** V241441 (attend services 85% miss).

### Excluded (already in H4 baseline as fundamentals; do NOT add as candidates)

V241104 (2020 recall), V241291 (econ retro), V241227x (pid7), V241157 (Trump_ft), V241404 (Gaza salience — already in H4). These are baseline fundamentals — the lasso retains them as MANDATORY-INCLUDE features, not lasso-selected.

### Excluded (POST items + the 2 already in H10 anti-system composite)

V242304, V242305: these are POST items in the anti-system composite from v2.1 H10. **Whether to include POST items in v2.2 lasso:** included (they're valid covariates; the H10-as-composite test was descriptive). Add to pool: V242304, V242305.

### Excluded (demographic — already in Model A as random-effect groups)

V241501x (race), V241458x (age→cohort), V241463 (educ), V241551 (gender), V241023 (state→region). These are model groups, not candidate mediators.

**FINAL POOL: 38 items** (21 issues + 8 traits + 3 values/system + 4 trust + 2 identity + 1 ideology + 1 religion - 2 POST = 38).

Wait, let me recount: 21 issue (with the duplicate noted out) + 8 traits + 3 values + 4 trust + 2 identity + 1 ideology + 1 religion + 2 POST anti-system = 21+8+3+4+2+1+1+2 = **42 items**. (Verbal "38" above incorrect; corrected here. Final pool LOCKED at 42.)

---

## 2. Sample split protocol (LOCKED)

- **Universe:** Same as v2.0 H4: respondents with valid V242096x ∈ {1, 2}, valid V241227x > 0, valid demographics, valid 2020 recall. (Per v2.0 H4: N=3533.)
- **Split:** 50/50, stratified by cohort (Silent / Boomer / GenX / Millennial / GenZ).
- **Seed:** Python `random.Random(42).shuffle(...)` deterministic shuffle within each cohort stratum, take first half as train, second half as test.
- **Sample sizes:** report N_train + N_test in result_v2.2 §3.

---

## 3. Lasso discovery procedure (LOCKED)

### 3.1 Feature matrix construction

On TRAINING half only:
- Mean-impute missing values per item (after dropping rows where >50% of pool items are missing — the per-item >20%-miss rule already applied at pool-construction time).
- Z-score each item (mean-0 / unit-variance) **using training-half statistics only**.
- Include all 42 candidate items + cohort_idx (1-5 numeric) + H4 baseline fundamentals (8 items) as features. Total: 51 features.
- Outcome: Harris-vote (0/1).

### 3.2 Penalty

L1-penalized logistic regression (sklearn `LogisticRegression(penalty='l1', solver='saga')`).

- Regularization strength: λ selected by 10-fold cross-validation (mean cross-entropy loss) within the training half.
- `class_weight='balanced'` (Harris/Trump are ~equal but tighten any imbalance).

### 3.3 Retention rule

- An item is RETAINED if its z-scored lasso coefficient is non-zero at λ_min.
- Cohort_idx and H4 fundamentals are KEPT regardless (mandatory).
- If >20 items retained, take TOP 20 by |coefficient| (avoid identifiability in Stan with K_fund > 28).

---

## 4. Stan confirmation (LOCKED)

### 4.1 Test-half fit

- On TEST half only: fit `model_a.stan` with K_fund = 8 (H4 baseline) + N_retained (lasso-discovered items).
- Items are mean-imputed using TRAINING-HALF means + z-scored using TRAINING-HALF statistics. **No test-leakage.**
- Settings: chains=6, warmup=1000, samples=1000, seed=42 (hardened, matches v2.0.1 / v2.1).

### 4.2 Verdict gates (re-use v2.1 thresholds)

| Verdict | σ_cohort posterior mean |
|---|---|
| **AXIS FOUND** | < 0.15 |
| **AXIS PARTIAL** | 0.15 ≤ σ_cohort < 0.25 |
| **AXIS NOT FOUND** | ≥ 0.25 |

Report posterior mean + 90% CI; report β + 90% CI for each retained item; report N_retained.

### 4.3 Robustness reads

- **σ_cohort comparison: train vs test.** Also fit Stan on TRAIN-half with retained items + H4 baseline. If σ_cohort_train < σ_cohort_test by >0.10, the discovery overfit the cohort signal; report as overfit-flag.
- **Items retained:** report the labeled list as DISCOVERY OUTPUT (not pre-reg'd). Interpretation: these are the items in the canonical ANES political-attitudes battery that DO load on the cohort signal — the "v3 candidate" enumeration v2.1 §5 anticipated.

---

## 5. Aggregate verdict

- **MECHANISM IDENTIFIED VIA ANES BATTERY:** test-half σ_cohort < 0.15 (AXIS FOUND).
- **MECHANISM PARTIALLY IN ANES BATTERY:** test-half σ_cohort ∈ [0.15, 0.25] (AXIS PARTIAL).
- **MECHANISM TRULY RESIDUAL:** test-half σ_cohort ≥ 0.25 (AXIS NOT FOUND). v2.1's MECHANISM RESIDUAL verdict survives this stronger test — cohort signal is NOT in any linear combination of the available ANES political-attitudes covariate space.

Pre-reg commits to reporting the verdict whichever obtains, including the strongest reading (AXIS NOT FOUND — strongest possible v2.2 reading, doubles down on v2.1).

---

## 6. Threats to validity

- **Lasso instability at λ_min.** Items selected at λ_min can be noisy; the TOP-20 cap and the test-half confirmation step both mitigate.
- **Mean-imputation of missing.** Imputing to training-mean assumes missing-at-random; ~5% per-item missingness is small but may introduce residual bias.
- **Sample-split power.** N_test ≈ 1766 is smaller than full H4 N=3533; the test-half σ_cohort posterior is wider. The verdict gates (0.15 / 0.25) account for this — even with wider CIs, the point estimate against the gate is the verdict.
- **Z-score statistics from training only.** Standard out-of-sample protocol; same items may have somewhat different test-half distributions, slight β bias possible.

---

## 7. v2.2 deviation log

| Date | Deviation | Rationale |
|---|---|---|

(Empty at lock; populated as v2.2 work surfaces discrepancies.)

---

**Locked at commit:** `[fill at commit]` on `main`.
**Repository:** https://github.com/mrnathanhumphrey-droid/DNC.
**Builds on:** result_v2.1 (HEAD 27a0093).
