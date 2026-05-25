# Pre-Registration v2.10 — DNC 2024 Post-Mortem v2.10 (Non-voter mirror + Issue decomposition)

**Status:** LOCKED. Pre-reg drafted 2026-05-25 BEFORE running any v2.10 outcome × predictor fit.
**Builds on:** result_v2.9 (`823432b`) — 4/5 hypotheses confirmed (econ+trust+mobilization+issue-conservatism multi-channel demobilization among Biden-2020 voters).
**User direction (2026-05-25):** "non-voter mirror first, then chart-up of issues."

---

## 0. Why this thread

v2.9 characterized **why Biden-2020 voters left** (multi-channel demobilization). Two open questions remain:

1. **Symmetric question:** Who SHOWED UP for Trump in 2024 who didn't vote in 2020? Tests "demobilization" framing against "differential mobilization" framing — different political implications (Dem GOTV failure vs GOP mobilization success). CES VV has 2020 + 2024 turnout for the same respondents; this is a sibling regression.

2. **Headline elevation of v2.9 §4 issue findings:** v2.9 reported pro-choice/pro-climate/pro-immigration as 3 STRONG channels (β=-0.20 to -0.26) but buried them in a long table. Item-level decomposition + headline chart is the move.

---

## 1. Universe(s), outcomes (LOCKED)

### 1A. NON-VOTER MIRROR universe (H_MIRROR)

**Substrate:** CES 2024 Common Content with VV.
**Filters:**
- `vvweight_post > 0`
- `presvote20post == 6` (did NOT vote 2020) **— pre-reg note: smoke-test verified CES coding `6 = did not vote`; earlier v2.9 amendment 1 used wrong code `4`. Documented here at lock**
- `birthyr` valid AND `birthyr ≤ 2002` (18+ in 2020 — exclude post-2020-eligibility cohort)
- `TS_g2024` populated

**Smoke-test universe (filed at pre-reg lock as operationalization fact, not outcome-result):**
- N = 2,803 (2020 non-voters with valid VV match)
- 4-way outcome breakdown (universe sufficient for hierarchical Bayes):
  - trump_mobilized (TS_g2024 ∈ {1-6} AND CC24_410 == 2): **810**
  - harris_mobilized (TS_g2024 ∈ {1-6} AND CC24_410 == 1): **830**
  - third_mobilized (CC24_410 ∈ {3,4,5,8}): 97
  - still_nonvoter (TS_g2024 == 7): **924**
  - unaccounted (voted-unknown): 142

**Outcome definitions (two binary models, parallel structure):**

**Outcome 1 — `trump_mob`:** universe restricted to N_trump = trump_mobilized + still_nonvoter (= 1,734).
- `trump_mob == 1` if mobilized for Trump
- `trump_mob == 0` if stayed non-voter
- Excludes harris-mob, third-mob, voted-unknown (separate outcomes / not the test)

**Outcome 2 — `harris_mob`:** universe restricted to N_harris = harris_mobilized + still_nonvoter (= 1,754).
- `harris_mob == 1` if mobilized for Harris
- `harris_mob == 0` if stayed non-voter

**Rationale for two-binary, not multinomial:** directly comparable to v2.9's binary structure; β coefficients read on the same scale; permits side-by-side comparison of "what predicts Trump mobilization" vs "what predicts Harris mobilization."

### 1B. ISSUE DECOMPOSITION universe (H_DECOMP)

**Substrate:** Same as v2.9 — CES VV Biden-2020 voters, N=17,401 skip|retain universe.
**Outcome:** `skipped` (binary, identical to v2.9 §1).

---

## 2. Hypotheses (LOCKED)

### 2.1 H_MIRROR_A — Differential mobilization at COHORT level

**Hypothesis:** Trump's net mobilization from 2020 non-voters concentrates in OLDER cohorts (Silent/Boomer/GenX); Harris's net mobilization concentrates in YOUNGER cohorts (MillOld/MillYoung/GenZ).

Smoke-test cohort breakdown (transparency, filed at lock):
| Cohort | N | trump_mob | harris_mob | T-H gap |
|---|---:|---:|---:|---:|
| Silent | 37 | 14 | 14 | 0 |
| Boomer | 847 | 277 | 243 | **+34** |
| GenX | 933 | 294 | 263 | **+31** |
| MillOld | 480 | 117 | 142 | -25 |
| MillYoung | 312 | 77 | 94 | -17 |
| GenZ | 194 | 31 | 74 | **-43** |

**Decision rule:**
- Bayesian logistic on `trump_mob` and `harris_mob` separately, hierarchical with cohort random intercept + race/educ/gender/region + pid7_z + faminc_z.
- Compute σ_cohort for both fits.
- **H_MIRROR_A CONFIRMED** if BOTH:
  - σ_cohort ≥ 0.25 in BOTH the Trump-mob and Harris-mob fits (cohort matters as predictor in both directions)
  - Trump-mob cohort_eff is POSITIVE for {Silent, Boomer, GenX} AND Harris-mob cohort_eff is POSITIVE for {MillOld, MillYoung, GenZ} (with at least one credibility-positive in each side)
- **H_MIRROR_A REFUTED** if σ_cohort < 0.10 in either fit (cohort doesn't predict mobilization).
- **PARTIAL** otherwise.

### 2.2 H_MIRROR_B — Channel asymmetry

**Hypothesis:** The 5 channels confirmed in v2.9 (econ, trust, mobilization, issue-conservatism, engagement) operate ASYMMETRICALLY between Trump-mob and Harris-mob universes. Specifically:
- Mobilization (campaign contact) predicts Harris-mob > Trump-mob (Dem GOTV pulled non-voters)
- OR Mobilization predicts Trump-mob > Harris-mob (Rep GOTV pulled non-voters)
- Economic dissatisfaction predicts Trump-mob (worse-econ non-voters showed up for Trump)
- Issue-conservatism predicts Trump-mob > Harris-mob

**V-codes for predictors (5 channels, identical to v2.9 confirmed channels):**
- `mob_any_z` = CC24_431a binary
- `engage_act_z` = CC24_430a_1..8 composite
- `issue_econ_z` = CC24_301 z-score
- `issue_imm_z` = CC24_323a-d direction-locked
- `trust_elec_z` = CC24_421_1+2 mean z

**Decision rule:**
- For each channel × outcome combination, compute β (standardized).
- Channel CONFIRMED ASYMMETRIC if |β_trump| - |β_harris| ≥ 0.10 (substantively different magnitudes) AND signs differ OR sign agrees with hypothesized direction.
- Aggregate H_MIRROR_B verdict: ≥3 of 5 channels show asymmetry → CONFIRMED; 1-2 → PARTIAL; 0 → REFUTED.

### 2.3 H_MIRROR_C — Net mobilization is SYMMETRIC

**Null hypothesis (filed for direct test):** Trump and Harris mobilized comparable numbers of 2020 non-voters; the asymmetric STORY (DNC failure vs GOP success) is mainly internal to each coalition's cohort pattern, not an overall mobilization gap.

**Decision rule:** Smoke-test already shows trump_mob=810, harris_mob=830. Difference = -20 (Harris higher). Per-cohort breakdown shows offsetting patterns (older→Trump, younger→Harris). Formally test:
- 95% CI for log(trump_mob_share) - log(harris_mob_share) crosses zero → H_MIRROR_C CONFIRMED (net symmetric)
- 95% CI excludes zero → H_MIRROR_C REFUTED (one side dominates)

### 2.4 H_DECOMP — Item-level issue dimension breakdown

**Hypothesis:** The v2.9 issue-conservatism finding (abortion β=-0.257, climate β=-0.243, immigration β=-0.205 as composites) is **driven by specific items**, not uniformly across all sub-items.

**V-codes:**
- Abortion: 4 items (CC24_324a Always allow / CC24_324b Rape-incest only / CC24_324c Illegal always / CC24_324d Expand access). Each as separate predictor in own fit; HIGH = support that specific position.
- Climate: 6 items (CC24_326a-f, individual). Each as separate predictor.
- Immigration: 4 items (CC24_323a-d, individual). Each as separate predictor.
- Total: 14 item-level fits.

**Decision rule:**
- For each item: β credibly non-zero (95% CI excludes zero) AND |β| ≥ 0.10 → ITEM-CONFIRMED.
- Cluster verdict per issue:
  - Abortion: how many of 4 items credible? Direction-consistent across items?
  - Climate: how many of 6 items? Direction-consistent?
  - Immigration: how many of 4 items? Direction-consistent?
- **Headline chart:** standardized β bar chart with 14 issue items + 5 v2.9 channels (econ/trust/mob/engage + issue-aggregate) for visual headline.

---

## 3. Hardened fit settings

Per v2.0.1+ pattern:
- chains = 6
- warmup = 1000
- samples = 1000
- seed = 42
- Stan model: `model_a.stan` (binary hierarchical logistic).

---

## 4. Falsifiers

**F1 — Universe N collapse:**
- Trump-mob universe (`trump_mob` outcome) N ≥ 1,000 events combined. Smoke: 810 events of 1,734 — PASS.
- Harris-mob universe N ≥ 1,000. Smoke: 830 of 1,754 — PASS.
- Decomp universe (Biden 2020 skip|retain) N = 17,401 — PASS.

**F2 — pid7_z dominates:**
- If pid7_z absorbs >75% of cohort variance, mobilization predictors may be over-controlled. Run no-pid7 sensitivity.

**F3 — Convergence failure:**
- R̂ > 1.01 OR ESS_bulk < 400 → F5 escalation chains=8, warmup=2000, samples=2000.

**F4 — Codebook orientation:**
- All item-level coding verified pre-fit against codebook tables (already done for abor/clim/imm in v2.9 amendment 2). Trust_elec direction LOCKED per v2.9 result §6 (HIGH raw = less confidence).

**F5 — Mirror-universe selection bias:**
- CES VV match rate among 2020 non-voters is lower than among 2020 voters (smoke: 169 N at strict criteria; 2,803 at broader). Document any VV-selection effects in result §10.

---

## 5. Code artifact

`code/v210_mirror_and_decomp.py` (to build post-pre-reg lock):
- Loads CES, builds non-voter universe per §1A.
- Builds outcomes `trump_mob` and `harris_mob`.
- 5 channel predictors per H_MIRROR_B.
- Reuses Biden-2020 universe from v29 for H_DECOMP.
- 14 item-level issue fits per H_DECOMP.
- Output: `result_v2.10_scoreboard.csv` + headline-chart-data CSV.

---

## 6. Out-of-scope (deferred to v2.11)

- 3-way multinomial skip/retain/flip on Biden universe (already filed in v2.9 §14 as candidate).
- Pew W159 cross-replication.
- Cohort × channel interactions on Biden-skip outcome (filed as v2.11 candidate earlier).
- Late-decider analysis (CES vote-timing items are voter-conditional; would need pre-election proxy).
- Information environment (CES media items are type-coded not ideology-coded).

---

## 7. Repository state at pre-reg lock

- HEAD `823432b` (result_v2.9 LOCKED).
- Branch `main`, pushed to origin.
- Smoke-test universe-N + bucket counts logged in §1A as operationalization facts (not outcome-relationship results).
