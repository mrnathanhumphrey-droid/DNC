# Pre-Registration v2.11 — DNC 2024 Post-Mortem v2.11 ("Blame the Leftists" empirical test)

**Status:** LOCKED. Drafted 2026-05-25 BEFORE running any v2.11 outcome × predictor fit.
**Builds on:** result_v2.10 (`df16116`).
**User direction (2026-05-25):** *"see if the 'blame the leftists' people were right. did the socialists get people to stop voting?"*

---

## 0. The question

The mainstream-Dem post-mortem narrative blames "the left" (socialists, Squad, Gaza protesters, anti-establishment progressives) for demobilizing the 2024 Democratic coalition. This is testable: **do leftist Biden-2020 voters skip MORE or LESS than centrist Biden-2020 voters?**

- **β POSITIVE** (more leftist → more skip): "blame the leftists" CONFIRMED. Leftist positioning drove demobilization.
- **β NEGATIVE** (more leftist → less skip): "blame the leftists" REFUTED. Leftist Biden voters were the most loyal retainers; the skip pattern lives elsewhere.
- **β NULL**: leftism orthogonal to skip; narrative neither supported nor refuted.

v2.10 already identified the RIGHT-flank skip story (Build Wall + Fossil Fuel support → skip, β=-0.262 STRONG each). v2.11 tests the LEFT-flank: did "too progressive for Harris" voters also skip?

---

## 1. Universes (LOCKED)

**Biden-2020 universe** (primary, identical to v2.9 / v2.10 §1):
- N = 17,401 (skip vs retain among VV-matched Biden-2020 voters)
- Outcome: `skipped` binary (1 = TS_g2024 == 7; 0 = TS in {1-6} AND CC24_410 == 1)

**Non-voter mirror universe** (secondary, identical to v2.10 §1A):
- N = 2,803 (CES VV 2020 non-voters, age 18+ in 2020)
- Outcome 1: `trump_mob` (Trump-mobilized vs still-non-voter, N=1,734)
- Outcome 2: `harris_mob` (Harris-mobilized vs still-non-voter, N=1,754)

---

## 2. Composite (LOCKED, V-codes + direction)

`left_composite_z`: z-score of mean across 11 binary items, each recoded so HIGH = leftist position.

| V-code | Item | Direction-lock |
|---|---|---|
| CC24_323f | Forgive $20k student loan | Support → 1 (LEFTIST) |
| CC24_328a | Relax zoning (YIMBY housing) | Support → 1 |
| CC24_328b | Expand affordable housing subsidies | Support → 1 |
| CC24_328e | Expand Medicaid <$25k/$40k | Support → 1 |
| CC24_340a | No gov restrictions on contraceptives | Support → 1 |
| CC24_340c | Recognize same-sex/interracial marriage federally | Support → 1 |
| CC24_340d | Ban TikTok | Support → 0 (OPPOSE = LEFTIST) |
| CC24_340e | Renew FISA surveillance | Support → 0 (OPPOSE = LEFTIST) |
| CC24_341b | Raise corporate tax 21→28% | Support → 1 |
| CC24_341c | Tax >$400k income at 35% | Support → 1 |
| CC24_341d | $150B/yr infrastructure | Support → 1 |

**Construction:** for each item, recode to {1, 0} per direction-lock; take row-mean across items; z-score the row-mean. HIGH = MORE LEFTIST.

**Verification:** all 11 items have ≥99% valid coverage in Biden universe (CES Common Content full sample). Variance ranges: TikTok ban 53/47 (highest variance), FISA renewal 35/65, zoning 59/41, student loan 81/19, others ≥90/10. Item-mean composite will have moderate variance.

---

## 3. Hypotheses (LOCKED)

### 3.1 H_LEFTIST_A — "Blame the leftists" PRIMARY test

**On Biden universe:** β coefficient of `left_composite_z` on `skipped` outcome, controlling for pid7_z + faminc_z + employ + cohort + race + educ + gender + region.

**Decision rule:**
- β credibly POSITIVE (95% CI excludes zero AND mean > 0) AND |β| ≥ 0.10 → **CONFIRMED: leftist Biden voters skipped MORE**
- β credibly NEGATIVE AND |β| ≥ 0.10 → **REFUTED: leftist Biden voters skipped LESS** (i.e., they were the most loyal retainers)
- β CI crosses zero OR |β| < 0.05 → NULL

### 3.2 H_LEFTIST_B — Mirror Harris-mob

**On Harris-mob universe (N=1,754):** β of `left_composite_z` on harris_mob outcome.

**Expected if v2.10 mirror story holds:** β POSITIVE (leftist non-voters mobilized for Harris). This is the Bernie-Squad-loyalty-to-Dem-coalition hypothesis.

### 3.3 H_LEFTIST_C — Mirror Trump-mob

**On Trump-mob universe (N=1,734):** β of `left_composite_z` on trump_mob outcome.

**Expected:** β NEGATIVE (leftist non-voters did NOT mobilize for Trump). Sanity check on direction-lock.

### 3.4 H_LEFTIST_DECOMP — Single-item breakouts

Run 4 single-item fits on the Biden universe to identify which item(s) drive the composite signal (if any):
- `left_student_loan_z` (CC24_323f recoded to HIGH=support)
- `left_anti_tiktok_z` (CC24_340d recoded to HIGH=oppose-ban)
- `left_anti_fisa_z` (CC24_340e recoded to HIGH=oppose-renewal)
- `left_medicaid_z` (CC24_328e recoded to HIGH=support-expand)

These four are the highest-variance / most-diagnostic leftist items.

---

## 4. Falsifiers + settings

**F1:** universe N ≥ 12,000 Biden; ≥ 1,500 mirror. PASS at universe build.

**F2:** convergence per pre-reg v2.9 standard. R̂ ≤ 1.01 OR escalate to chains=8 warmup=2000 samples=2000.

**F3:** if `left_composite_z` collinear with `pid7_z` at |r| ≥ 0.5, run no-pid7 sensitivity. Smoke check at predictor-build time.

**Hardened settings:** chains=6, warmup=1000, samples=1000, seed=42. Stan model: `model_a.stan`.

---

## 5. Code artifact

`code/v211_leftist_test.py`: build composite + 4 single-item z-scores; reuse v2.9/v2.10 universe infrastructure; fit 7 binary logistic models (3 composite outcomes + 4 single-item Biden-skip fits). Total runtime ~1.5–2 hours.

---

## 6. Out-of-scope

- Item-level breakouts on mirror universe (deferred to v2.12 if v2.11 lands).
- Gaza items (CC24_308b sub-content still pending codebook PDF read).
- Continuous left-right scale via PCA on issue items (v2.12 candidate).
- Interaction with cohort (v2.12 candidate).

---

## 7. Repository state at lock

- HEAD `df16116` (result_v2.10 LOCKED).
- Branch `main`, pushed to origin.
- V-codes verified pre-lock against codebook tables (no V-code mis-identifications expected — items are the policy/issue series we already verified in v2.10).
