# DNC 2024 Post-Mortem — Pre-Registration v1.0

**Date drafted:** 2026-05-22
**Locked before:** any model fit, any data merge, any data inspection beyond schema-level verification of variables present in codebooks.
**Companion documents:**
- `path_map_dnc_postmortem.md` (substrate inventory, conceptual contribution, stated priors)
- Substrate access verification (2026-05-22 web research; results inline in §2 below)

Once committed (git init + commit), no edits permitted; deviations logged in §12.

---

## 0. What this pre-reg LOCKS

- Hypotheses with falsification thresholds (§1)
- Substrate roles + N + access mechanism (§2)
- Six-issue battery + per-substrate operationalization (§3)
- Three-model architecture A / B / C (§4)
- Variance decomposition method + falsification gates (§5)
- Multiplicity correction via hierarchical shrinkage (§6)
- Stan model skeletons with priors (§7)
- Pay-structure imputation pipeline (§8)
- Verdict decision rules (§9)
- Operational protocol with execution order (§10)
- Explicitly NOT covered (§11)

The pre-reg does NOT lock final per-issue effect-size point estimates, which substrates produce significant findings, or whether the cohort hypothesis survives. Those are the answers; this is the question.

---

## 1. Hypotheses (LOCKED)

**H1 (cohort, the primary stated prior per path_map §5.5):** In Model A with Pew cohort coding (Silent ≤1945, Boomer 1946-1964, Gen X 1965-1980, Millennial 1981-1996, Gen Z 1997-2012), cohort main effects are large relative to other demographic main effects, AND Millennial + Gen Z cohorts cluster attitudinally on the six-issue battery distinct from Gen X + Boomer cohorts.

- **H1 SUPPORTED** if: cohort-effect 95% CI for ≥1 of {Millennial, Gen Z} excludes the Gen X/Boomer cluster on ≥3 of 6 issues, AND cohort effects are within the top quartile of demographic main-effect magnitudes (race, educ, gender, region also estimated).
- **H1 NULL** if: cohort effects are small (bottom half of demographic main-effect magnitudes) OR Millennial/Gen Z do not cluster distinct from Gen X/Boomer on ≥3 of 6 issues.

**H2 (exposure-beyond-cohort):** In Model C with both demographic and exposure-pool hierarchical structures, exposure-cell coefficients have CIs excluding zero in directions consistent with theory on ≥2 of 6 issues, AND demographic effects shrink by ≥30% in magnitude when exposure pools are added.

- **H2 SUPPORTED** if both conditions hold.
- **H2 NULL** if exposure-cell coefficients in Model C shrink to zero (≥4 of 6 with CIs covering zero) AND demographic effects in C are within 10% of A.

**H3 (residual-dominated):** Residual variance after Model C fit exceeds 60% of total variance across all primary substrates (ANES + CES).

- **H3 SUPPORTED** if average residual variance > 60% across ANES + CES on ≥4 of 6 issues.
- This is the path_map §5 "both lose" condition — the most epistemically valuable null and the one the pre-reg leaves room for explicitly.

**Cross-hypothesis joint outcomes** (not new tests, just decision rules for the headline):
- H1 SUPPORTED + H2 NULL: "Properly-coded cohort effects explain most of the 2024 shift; exposure pools add nothing beyond cohort." A Model-A-wins finding.
- H1 NULL + H2 SUPPORTED: "Cohort doesn't pick up much; exposure pools are the carrier." Model-B-wins.
- H1 SUPPORTED + H2 SUPPORTED: "Both cohort AND exposure carry distinct information." Model-C-wins.
- H1 NULL + H2 NULL: "Neither cohort nor exposure adequately explains the shift." Consistent with H3.
- H3 SUPPORTED: Residual dominates regardless of H1 / H2 directions.

All four joint outcomes are reportable and publishable. The pre-reg makes no commitment about which is most likely.

## 2. Substrates (LOCKED — roles assigned from 2026-05-22 access verification)

| Substrate | Role | N | Access | Battery coverage |
|---|---|---|---|---|
| **ANES 2024 Time Series** | **PRIMARY** | 5,521 (+ 2,070 panel re-interviews) | Free, https://electionstudies.org/data-center/2024-time-series-study/ | **Full 6-issue battery + exposure pools + cohort. The only substrate with confirmed full coverage.** |
| **CES 2024 Common Content** | **SCALE-on-subset** | ~60,000 | Free, https://dataverse.harvard.edu/dataset.xhtml?persistentId=doi:10.7910/DVN/X11EP6 | Healthcare (single-payer), racial inequity, insurance, social media platforms. **Missing Israel/Gaza, science/arts, USAID in Common Content** — team modules may carry but at ~1k each. CES contributes scale on 3 of 6 issues; flagged as scale-secondary not full primary. |
| **AP VoteCast 2024 PUF** | Vote-choice + demographic decomposition + Issue 1 single-issue contribution | 139,938 | Free PUF, https://apnorc.org/projects/ap-votecast-puf/ | **CONFIRMED via codebook pull 2026-05-22.** 2 of 6 issue items present (Israel/Gaza via `ISRAELAID` 4-pt; structural racism partial via `RACISMUS` 4-pt). Below 3-of-6 threshold → role-locked to vote-choice + demographic decomposition with Israel/Gaza single-issue add-on. Social media = `TIKTOKUSER` only (no FB/X/Instagram). No hourly/salary. No insurance status. **Age banded only** (6 bands: 18-24, 25-29, 30-39, 40-49, 50-64, 65+) — disclosure-suppressed; cohort coding approximate via band-to-cohort mapping (see operationalization supplement). Race × education × gender × state all present. |
| **Pew Validated Voters 2024** | Turnout-vs-choice separation only | 8,942 (7,100 voter-file-validated, 94% match) | Registration-gated free, https://www.pewresearch.org/politics/2025/06/26/behind-trumps-2024-victory-a-more-racially-and-ethnically-diverse-voter-coalition/ | **CONFIRMED via questionnaire PDF pull 2026-05-22.** 0 of 6 issue items in W159 wave instrument (validated voters wave was a narrow turnout-only instrument). 0 of 3 exposure-pool items in W159. Demographics via panel profile (age continuous-grade, race/educ/gender/state). Validation: 7,100 of 8,942 matched (94%) against 3 commercial voter files. Utah excluded by state law (self-report only). **Role locked to turnout-vs-choice separation; no issue-battery contribution.** |
| **GSS 2024** | **Tier 2: spending priorities** | NORC GSS Cross-section, recent annual cadence | Free, https://gssdataexplorer.norc.org/ | NATSCI / NATARTS / NATAID confirmed as core "national spending priorities" module (replicating-core block); contributes Tier 2 items 5 + 6 (science/arts + foreign aid). Insurance module rotating-uneven; verify in 2024 codebook. |
| **CPS ASEC 2025 + CPS ORG** | Pay-structure imputation backbone | ASEC ~180-200k persons; ORG monthly | Free, https://www.census.gov/data/datasets/2025/demo/cps/cps-asec-2025.html + https://cps.ipums.org/ | No political items. Provides (occ × ind × hours × income) for imputing P(hourly) on political-survey respondents. **Hourly/salary direct via PAIDHRE in CPS ORG monthly outgoing rotation group**, not ASEC. Pipeline §8 below. |

**Substrate roles resolved 2026-05-22** (conditional gating rule from draft removed). Per the 2026-05-22 codebook pulls in §10.0, both AP VoteCast and Pew VV failed the ≥3-of-6 threshold. Roles locked above; not re-opened by future codebook discoveries unless filed as a §12 deviation.

## 3. Issue battery — per-substrate operationalization (LOCKED)

The six issues from path_map §3 are operationalized as follows. Each row is locked ex ante; per-substrate item presence is what determines whether each substrate enters the per-issue analysis.

| # | Issue | Path-map intent | ANES 2024 | CES 2024 Common Content | GSS 2024 | AP VoteCast 2024 | Pew VV 2024 |
|---|---|---|---|---|---|---|---|
| 1 | **Israel/Gaza position** | Tier 1; identity-coded foreign policy; the Rivera-attributed Israel-net-negative claim | Israel military aid 7-pt + Palestinian humanitarian aid 7-pt | NOT in Common Content (team-module-only) | N/A | **`ISRAELAID` 4-pt favor/oppose** | NOT in W159 |
| 2 | **Single-payer healthcare** | Tier 1; insured/uninsured pool directly | Government health insurance scale | ACA / single-payer support items | N/A | NOT (only `HEALTHCOV` policy-attitude + `MEDICAID` expansion) | NOT in W159 |
| 3 | **Structural inequity** | Tier 1; salience-vs-position; high-information cell separation | Racial inequity / structural-racism battery | Racial resentment battery | N/A | **`RACISMUS` 4-pt seriousness (partial)** | NOT in W159 |
| 4 | **Race relations** | Tier 1; attitude shift independent of demographic-race shift | Dedicated race-relations item | Racial-attitudes battery (no dedicated "race relations") | N/A | Covered by `RACISMUS` (no separate item) | NOT in W159 |
| 5 | **Science / arts funding** | Tier 2; spending priorities | Federal spending battery (science, arts) | NOT in Common Content | **NATSCI + NATARTS** | NOT in PUF | NOT in W159 |
| 6 | **USAID / foreign aid** | Tier 2; anti-establishment-spending; operationalized as foreign aid | Federal foreign aid spending item | NOT in Common Content | **NATAID** | NOT generic (only `UKRAINEAID` + `ISRAELAID`) | NOT in W159 |

**Net per-substrate issue-battery coverage:** ANES 2024 = 6/6 (full); CES 2024 = 3/6 (healthcare + structural inequity + race-attitudes); GSS 2024 = 2/6 (science/arts + foreign aid, Tier 2); AP VoteCast 2024 = 2/6 (Israel + structural-racism partial); Pew VV 2024 = 0/6. **ANES is the only full-battery substrate.** Cross-substrate corroboration patterns for each issue are constrained accordingly.

**Harmonization rules (LOCKED):**
- 7-pt scales standardized to z-scores within substrate before pooling.
- Categorical items (e.g., GSS spending: "too little / about right / too much") converted to ordinal scores [-1, 0, +1] then z-standardized.
- Cross-substrate effect-size comparison uses standardized coefficients only.
- Per-substrate effect-size tables in supplement report raw scales for transparency.

## 4. Three-model architecture (LOCKED — Stan specifications in §7)

**Outcome variable (LOCKED):** Presidential vote choice in 2024 election, coded as four-category multinomial: {Harris, Trump, third-party, abstain}. Primary models predict Harris vs Trump binary among major-party voters; secondary models on the four-category multinomial for completeness.

**Independent variables — fundamentals baseline (LOCKED, common across A/B/C):**
- 2020 presidential vote recall (Biden / Trump / third / abstain)
- State partisanship (Cook PVI 2024 cycle)
- State result margin 2024 (controlled to avoid double-counting state-level shift)
- Personal economic perception (5-pt scale, standardized within substrate)
- Incumbency direction (Democratic Biden→Harris transition; binary marker for transition)

**Model A — Standard, properly-coded demographic pooling:**
- Hierarchical structure: race × education × birth-cohort × gender × region (5-dim cells)
- Cohort coding: Pew cutoffs locked above (Silent / Boomer / Gen X / Millennial / Gen Z)
- Continuous age included as robustness check in supplement (not headline)
- Within-cohort splits (older/younger millennial 1981-1988 vs 1989-1996; older/younger boomer 1946-1954 vs 1955-1964) as secondary specification where cell N ≥ 50

**Model B — Exposure-pool hierarchical structure:**
- Hierarchical structure: social_media × pay_structure × insurance (3-dim cells)
- Social media: dominant-platform indicator with intensity (frequency × political-content) — categorical with levels {Facebook-heavy, Twitter/X-heavy, Instagram-heavy, TikTok-heavy, YouTube-heavy, Reddit-heavy, low-use, mixed}. Per-respondent dominant-platform classification = platform with highest frequency × political-content product among confirmed-used platforms; "low-use" if all platforms below threshold; "mixed" if no single platform exceeds 1.5x next-highest.
- Pay structure: imputed P(hourly | observables) from §8 pipeline; respondent classified as hourly if P(hourly) > 0.6, salaried if < 0.4, mixed/uncertain otherwise; alternative spec uses continuous P(hourly) as covariate
- Insurance: insured-private / insured-public / uninsured (3-level categorical)

**Model C — Joint demographic + exposure with shrinkage:**
- Both Model A's and Model B's hierarchical structures included
- Shrinkage prior on demographic main effects allows them to fade if exposure cells absorb explanatory power
- Mediation analysis quantifies path race → platform → vote, education → occupation → pay-structure → vote, etc.

## 5. Variance decomposition + falsification (LOCKED)

**Headline variance decomposition (the main quantitative output):**

For the aggregate 2020→2024 two-party shift Δ:
```
Δ = β_fundamentals + β_demographics + β_exposure + β_residual
```

Each β is a posterior distribution over decomposition contributions, reported with 95% CI. Per-substrate decompositions reported flat in supplement; headline collapses across substrates as robustness column.

**Model comparison thresholds (LOCKED, per Vehtari et al. 2017 ELPD-difference conventions):**
- ΔELPD > 4 with SE(ΔELPD) < ΔELPD/2: "Model X clearly preferred over Model Y."
- 0 < ΔELPD ≤ 4 OR SE(ΔELPD) ≥ ΔELPD/2: "Indistinguishable."
- ΔELPD < 0: "Model Y preferred."

**Falsification gates (per-substrate, primary substrate ANES anchors verdict):**
- **Model B "wins":** ANES ΔELPD(B, A) > 4 AND ≥2 of 6 issues have exposure-cell 95% CIs excluding zero in Model C AND demographic main effects in C shrink ≥30% relative to A on those issues.
- **Model A "wins":** ANES ΔELPD(B, A) < 0 (i.e., A preferred) AND exposure-cell 95% CIs in C cover zero on ≥4 of 6 issues AND demographic effects in C within 10% of A.
- **Model C "wins":** Both Model A AND Model B effects survive jointly in C (≥3 issues with significant demographic main effects in C AND ≥2 with significant exposure-cell effects in C).
- **All lose (residual-dominated, H3 SUPPORTED):** Average residual variance > 60% across ANES + CES on ≥4 of 6 issues.

**CES corroborates (does not override) ANES gate:** CES results on the 3 confirmed-Common-Content issues (healthcare, structural inequity, race relations attitudinal battery) must be directionally consistent with ANES (sign-agreement on ≥2 of 3) for the verdict to stand. If CES disagrees, report mixed verdict and flag substrate disagreement as the headline finding for those issues.

## 6. Multiplicity correction (LOCKED)

**Hierarchical shrinkage prior across the six issues:** Issue-level coefficient SDs share a half-normal hyperprior with scale parameter τ ~ Half-Normal(0, 0.5). This shrinks issue-level coefficients toward zero in absence of strong data, automatically handling multiplicity across 6 issues without ad-hoc Bonferroni.

**Bonferroni as supplementary check (NOT primary):** Per-substrate, per-model, per-issue: report uncorrected p-values, report Bonferroni-corrected α = 0.05 / 6 / 3 = 0.0028, report which findings survive at the corrected threshold. Headline uses the Bayesian credible-interval-excludes-zero criterion, not Bonferroni.

## 7. Stan model skeletons (LOCKED structure; constants finalized at implementation)

### Model A (sketch)

```
data {
  int<lower=1> N;
  int<lower=1> N_race; int<lower=1> N_educ; int<lower=1> N_cohort;
  int<lower=1> N_gender; int<lower=1> N_region;
  array[N] int<lower=1, upper=N_race> race;
  array[N] int<lower=1, upper=N_educ> educ;
  array[N] int<lower=1, upper=N_cohort> cohort;
  array[N] int<lower=1, upper=N_gender> gender;
  array[N] int<lower=1, upper=N_region> region;
  matrix[N, K_fundamentals] X_fund;
  array[N] int<lower=0, upper=1> y;  // 1 = Harris, 0 = Trump
  // For issue-coefficient secondary models:
  // matrix[N, 6] issue_z;  // 6 issues z-standardized
}
parameters {
  real alpha;
  vector[K_fundamentals] beta_fund;
  vector[N_race] z_race; real<lower=0> sigma_race;
  vector[N_educ] z_educ; real<lower=0> sigma_educ;
  vector[N_cohort] z_cohort; real<lower=0> sigma_cohort;
  vector[N_gender] z_gender; real<lower=0> sigma_gender;
  vector[N_region] z_region; real<lower=0> sigma_region;
}
transformed parameters {
  vector[N_race] race_eff = z_race * sigma_race;
  vector[N_cohort] cohort_eff = z_cohort * sigma_cohort;
  // ... (non-centered parameterization for all)
}
model {
  // Priors
  alpha ~ normal(0, 2);
  beta_fund ~ normal(0, 1);
  sigma_race ~ normal(0, 1);
  sigma_cohort ~ normal(0, 1);
  // ... (all hierarchical SDs half-normal)
  z_race ~ std_normal();
  z_cohort ~ std_normal();
  // Likelihood
  y ~ bernoulli_logit(alpha + X_fund * beta_fund
                      + race_eff[race] + educ_eff[educ]
                      + cohort_eff[cohort] + gender_eff[gender]
                      + region_eff[region]);
}
```

Non-centered parameterization throughout (per [[feedback_non_centered_for_sparse_funnels]]).

### Model B (sketch)

Replace demographic cells with exposure cells:
- social_media (8 levels per §4)
- pay_structure (3 levels: hourly / salaried / mixed)
- insurance (3 levels: private / public / uninsured)
- 8 × 3 × 3 = 72 exposure cells with hierarchical pooling

### Model C (sketch)

Both Model A and Model B structures. Demographic-effect priors widened to allow shrinkage toward zero when exposure cells absorb variance:
```
sigma_race ~ normal(0, 1);  // same as Model A
sigma_cohort ~ normal(0, 1);
// PLUS:
sigma_social ~ normal(0, 1);
sigma_pay ~ normal(0, 1);
sigma_insurance ~ normal(0, 1);
```

Mediation: for race → social_media → vote, fit auxiliary regression P(social_media_level | race) and decompose total race effect into direct (in joint model) + indirect (mediated through social_media).

**Issue-specific Stan models** for the 6-issue battery: replace binary outcome `y` with z-standardized issue position; same hierarchical structure; report posterior over issue × cohort and issue × exposure-cell coefficients.

## 8. Pay-structure imputation pipeline (LOCKED)

**Step 1 — Train P(hourly | X) on CPS monthly Outgoing Rotation Group (ORG):**
- Use CPS ORG earner-study file with PAIDHRE (paid hourly Y/N) as label
- Predictors: occupation (Census 2018 occ codes), industry (Census 2017 ind codes), age, gender, hours worked (UHRSWORKT), weekly earnings, education, region, race
- Logistic regression with interactions; cross-validated AUC reported
- Model coefficients persisted; uncertainty quantified via 50 multiple-imputation draws

**Step 2 — Apply trained model to ANES + CES + AP VoteCast respondents:**
- Each substrate has occ + ind + hours + earnings + demographics → predict P(hourly)
- For each respondent, draw 50 imputations from posterior P(hourly | observables)
- Propagate the 50 imputation sets through Model B and Model C; report posterior averaged over imputations with imputation-uncertainty contribution to total SE

**Step 3 — Sensitivity:**
- Re-run Model B / C with continuous P(hourly) covariate (avoids discrete-thresholding)
- Compare to discrete classification (P > 0.6 = hourly, < 0.4 = salaried, otherwise mixed)
- Report both; primary uses discrete with 50-imputation propagation

**Pay-structure-substrate weakness flag (LOCKED in pre-reg):** This is the substrate-weakest variable in the design per path_map §4. Sensitivity analysis at multiple imputation thresholds + continuous-spec robustness is required. If pay-structure imputation accuracy on CPS ORG cross-validation is below AUC 0.75, flag the exposure-pool analysis as weakly identified and report accordingly. Imputation-driven null results are not interpretable.

## 9. Verdicts (LOCKED)

**Cascade-level verdicts (per §5 falsification gates, ANES + CES corroboration):**

- **MODEL A WINS** — properly-coded demographics (especially cohort) explain the 2024 shift; exposure pools add nothing beyond demographics.
- **MODEL B WINS** — exposure pools carry information demographics miss; Rivera-style mechanism-level decomposition validated.
- **MODEL C WINS (joint)** — both cohort AND exposure carry distinct information; integrated framework needed.
- **ALL LOSE (residual-dominated)** — issue-based decomposition insufficient; 2024 not well-explained by issue positions exposure-stratified or not; recommend identifying candidate omitted constructs (affect, institutional trust, identity).
- **INVALID** — primary substrate (ANES 2024) lacks the items as confirmed in §2 (i.e., substrate access verification was wrong), OR pay-structure imputation AUC < 0.75 AND alternative continuous specification also fails, OR all 4 primary substrates (ANES + CES + AP VoteCast + Pew VV) fail to produce convergent Stan fits.

**Per-issue findings (always reported, regardless of cascade verdict):**
- Effect-size point estimate + 95% CI for each of 6 issues under each of {A, B, C} on each of {ANES, CES, GSS Tier 2}
- Cohort × issue interaction estimates (which cohorts move on which issues, vs. baseline)
- Exposure-cell × issue interaction estimates
- Mediation decomposition (race → platform; education → pay → outcome)

## 10. Operational protocol (LOCKED execution order)

**§10.0 — Pre-reg-blocking action items BEFORE lock:**

1. **AP VoteCast 2024 PUF codebook pull.** **COMPLETED 2026-05-22.** Result: 2 of 6 issue items present (Israel/Gaza via `ISRAELAID`; structural racism partial via `RACISMUS`). Role-locked: vote-choice + demographic decomposition + Issue 1 single-issue. §2 + §3 updated with confirmed items.
2. **Pew Validated Voters 2024 questionnaire PDF pull.** **COMPLETED 2026-05-22.** Result: 0 of 6 issue items in W159 wave instrument. Role-locked: turnout-vs-choice separation only. §2 + §3 updated.
3. **CES 2024 team-module index review.** **DEFERRED.** Optional in v1; if pursued, file as §12 deviation with module IDs + per-module N.

All §10.0 blocking items resolved. Pre-reg ready to lock.

**§10.1 — Execution order after pre-reg lock:**

1. **Commit + push this pre-reg.** Lock = commit timestamp.
2. **Substrate downloads.** ANES 2024, CES 2024, GSS 2024, CPS ASEC 2025, CPS ORG (monthly file for 2024 calendar year), AP VoteCast 2024 PUF, Pew VV 2024 (after registration).
3. **Schema verification.** For each substrate, confirm the items in §3 are present at the variable names indicated. If any variable absent, file §12 deviation BEFORE proceeding with that substrate.
4. **Pay-structure imputation pipeline (§8).** Train on CPS ORG. Persist trained model + cross-validation AUC. Apply to political-survey substrates; produce 50-draw imputation sets.
5. **Stan model A fits.** Per substrate: fit Model A on outcome (vote choice) + 6 per-issue models. Convergence diagnostics (R-hat ≤ 1.01, ESS ≥ 400 per parameter, no divergent transitions) required for fits to be reported.
6. **Stan model B fits.** Same per substrate, with imputed pay structure.
7. **Stan model C fits.** Same per substrate.
8. **ELPD + variance decomposition.** Per §5 thresholds.
9. **Apply §9 verdicts.** Write up in `result_v1.0_dnc_postmortem.md`.

**Estimated wall clock:** 3-5 sessions of focused work. Stan fits at ANES n=5521 + CES n=60k will require ~30 min - 2 hours per model per substrate on the 9950X3D + cmdstanpy; total compute manageable locally without cloud.

## 11. Explicitly NOT covered

- **DNC's internal voter-file modeling and Catalist microdata.** Per path_map §8: failure to replicate the Rivera-attributed Israel-net-negative claim in public substrates is NOT evidence the DNC was wrong; it is evidence the claim is not robust to independent substrates. Both interpretations reported.
- **Catalist-specific microdata.** Not purchasable in any reasonable form for this project; aggregate reports cited where relevant.
- **Campaign-internal polling, message-testing, operational decisions.** Out of scope.
- **Rivera interview transcripts.** May or may not exist; not pursued.
- **Causal identification beyond regression adjustment + mediation.** Rosenbaum-Γ sensitivity reported but no instrumental-variable or RD identification claimed.
- **Outcomes other than 2024 presidential vote choice + 6-issue battery.** House / Senate / state-level decompositions out of scope for v1; potential v2 scope.
- **Within-person panel attitude change beyond ANES.** ANES 2024 panel re-interviews (n=2070 from 2016-2020 ANES panel) are reported as a secondary panel-analysis section; no other within-person tracking attempted.

## 12. Pre-registration deviation log

| Date | Deviation | Rationale |
|---|---|---|
| 2026-05-22 | **GSS 2024: `natarts` is NOT in the 2024 wave.** §3 Issue 5 claimed "GSS 2024 \| NATSCI + NATARTS"; reality is NATSCI only. Issue 5 (science/arts funding) **collapses to "science spending only" on GSS**. ANES retains the science + arts compound (per operationalization supplement). | Schema-level discovery on data download 2026-05-22 (commit `304b645` + post-download verification). The 2024 GSS NAT* spending battery includes natsci, nataid, natchld, natcity, natcrime, natdrug, nateduc, natenrgy, natenvir, natfare, natheal, natrace, natroad, natsoc, natspac — but not natarts. Arts-related variables present (aimofart, proudart, notsmart) measure arts-engagement attitudes, not federal spending. Cross-substrate Issue 5 comparison uses science-only on GSS; ANES "science + arts" remains compound. Operationalization supplement updated accordingly. |
| 2026-05-22 | **GSS 2024: no insurance-status variable.** §2 substrate row claimed "Insurance coverage rotating-uneven; verify in 2024 codebook." Verification at schema level 2026-05-22: no insurance / medicare / medicaid coverage variable in the 2024 wave's variable list. GSS **drops out of Model B insurance-pool analysis** (but retains spending-priorities role + cohort-effect role on Tier 2 items). | Schema-level discovery on data download. GSS's HEALTH module rotation did not include insurance coverage in the 2024 wave. Affects Model B only; Models A (demographic) and the issue-attitude analyses on spending priorities are unaffected. |
| 2026-05-22 | **ANES 2024 PUF: birth year (V241455) is RESTRICTED.** Public file shows uniform value -3 across all 5,521 respondents. Continuous age substitute: **V241458x** (range 18-80, top-coded at 80, n=5,242 non-missing). Cohort coding on ANES is via age-to-cohort mapping, NOT birth year. Silent generation (age 79+) collapses into the top-code 80 with oldest Boomers; can't be distinguished in the public file. | Schema-level discovery on ANES public-file extract 2026-05-22. Disclosure-protection by ANES restricts exact birth year. The age-derived cohort mapping is: age 18-27 → Gen Z; 28-43 → Millennial; 44-59 → Gen X; 60-78 → Boomer; 79-80 → Boomer/Silent boundary (top-coded). Silent generation is under-represented at boundary; sensitivity check via Boomer-only vs Boomer+Silent collapsed coding. Within-cohort splits (older/younger Millennial 28-35 vs 36-43; older/younger Boomer 60-69 vs 70-78) feasible via age. |
| 2026-05-22 | **Pew W159 F_AGECAT is 4-band only**, NOT continuous birth year as the methodology language suggested. Banded categories likely 1=18-29, 2=30-49, 3=50-64, 4=65+ (confirm at implementation). Cohort coding via band-to-cohort approximation similar to AP VoteCast (§3.2 of operationalization supplement) but coarser. | Schema-level discovery on Pew W159 microdata 2026-05-22. Pew's "Age (detailed)" from earlier verification refers to weighting-stratum granularity, not microdata variable. Pew W159 contributes to vote-choice validation across cohorts at coarse cohort granularity only; not a cohort-hypothesis-testing substrate. |
| 2026-05-22 | **Pew W159 actual N = 9,609 panel respondents** (not 8,942 as earlier verification reported), with 9,240 carrying WEIGHT_W159_VALIDATEDVOTE (validated-voter weight). The 7,100 figure from the methodology page refers to file-validated voters specifically (validated AND voted); the broader panel + non-voter subsample is larger and usable for turnout-vs-non-turnout analysis. | Schema-level discovery on download. Higher N is favorable; supports both turnout-vs-choice and turnout-vs-non-vote decompositions. |
| 2026-05-23 | **ANES public-file restrictions exceed what pre-reg §2 / §3 / §8 assumed.** Verification at impl time 2026-05-23 found the following ANES variables are RESTRICTED-and-empty (uniformly -3 in the public release): V241455 birth year (already in §12), **V241555 + V241556-558 ALL income variables**, **V241484 industry / kind of business**, **V241500a/b detailed race**, **V241463z detailed education**. Public summary versions available: V241458x continuous age (top-coded 80), V241463 collapsed education, V241501x summary race/ethnicity, V241499 hispanic, V241470-V241478 employment-status battery, V241498a union membership. **No public occupation, no public industry, no public income on ANES.** | Substrate-reality finding, dictated by ANES disclosure-protection on the public-use file. Restricted-use ANES requires institutional Data Use Agreement, which is not available for this project. **Knock-on consequences:** (1) Pre-reg §4 Model B / §5 / §6 / §7 — exposure-pool analysis on ANES — pay-structure imputation requires industry; demographics-only imputation would AUC well below the §8 0.75 gate. Per pre-reg §8, this triggers "weakly identified" flag for ANES Model B. (2) Pre-reg §2 substrate role for ANES partially rescoped: still PRIMARY for Model A (demographic + cohort effects via age-to-cohort mapping); demoted to LIMITED for Model B (no occupation/industry/income, only demographics + employment status). (3) CES Model B remains viable using CES's `industry` (17-level CES-internal categorical, requires crosswalk to CPS IND_MAJOR). (4) **Path-decision 2026-05-23 (user-directed):** v1 of the analysis defers Model B and Model C entirely; focus on Model A only across the 6-issue battery + vote choice. Model B/C revisited in v2 with the v3 demographics-only imputation evaluated against the §8 gate, OR with CES-only Model B. |
| 2026-05-23 | **§8 pay-structure imputation model: reduce predictor set to transfer-ready features only.** Original §8 specified predictors as "occupation (Census 2018 occ codes), industry (Census 2017 ind codes), age, gender, hours worked (UHRSWORKT), weekly earnings, education, region, race." Verification at impl time 2026-05-23: **ANES and CES political-survey respondents do NOT carry occupation codes, do NOT directly report hours worked, and do NOT report weekly earnings** (only banded household income, which is a household-vs-individual mismatch with CPS ORG's individual EARNWEEK2). Continuing with the original predictor set would inflate training-set AUC via CPS-only signal that doesn't transfer to the political surveys. **Amendment:** training-side feature set reduced to AGE, SEX, RACE, HISPAN, EDUC, REGION, IND_MAJOR (industry 2-digit major) — features both CPS ORG and ANES/CES carry. **Result: v2 transfer-ready model CV AUC = 0.7851 ± 0.0033** (per-fold 0.7810-0.7904), PASS at §8 gate (≥0.75) by 0.035 margin. v1 full-feature model (AUC 0.8393, commit c4e1cb6) is retained for reference but NOT used for downstream Model B / C imputation. | **Substrate-reality driven**, not result-driven. The feature reduction is dictated by what ANES + CES actually contain, not by model performance considerations. Filing this BEFORE applying imputation to political surveys — no peeking at downstream Model B / C results. v2 model is in `data/processed/paystructure_model_v2_transfer.joblib`; cross-substrate transfer uses this version. Earnings dropped (rather than kludged via household-vs-individual crosswalk) on principle: a noisy crosswalk would degrade prediction quality on political surveys more than dropping the feature entirely. Sensitivity option for Stan-stage analysis: re-fit Model B with continuous P(hourly) as covariate (avoids discrete-thresholding) per pre-reg §8 Step 3. |

---

**Locked at commit:** `45ea69a` on `main`, pushed to `origin/main` 2026-05-22.
Repository: https://github.com/mrnathanhumphrey-droid/DNC
