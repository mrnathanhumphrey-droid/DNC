# Pre-Registration v2.9 — DNC 2024 Post-Mortem v2.9 (GenZ-Skip Mechanism)

**Status:** LOCKED. Pre-reg drafted 2026-05-24 BEFORE running any v2.9 outcome × predictor fit.
**Builds on:** result_v2.3 (`d810d63`, CES VV skipper decomposition: GenZ 71% skip-share; MillYoung 49.8% skip-share, only cohort where flipping rivals skipping) + result_v2.0.1 (`68c85b8`, K-S canonical).
**Pivots from:** v2.1–v2.6 (cohort-effect mediator hunt within 2-party voters, 12 mediators ruled out) → v2.9 (within-skip mechanism: predictor of SKIP vs RETAIN within Biden-2020 voters).
**User direction:** *"so next question is why did younger biden coalition skip?"* — "go on C, A, E, D, B" (all 5 hypotheses, ordered).

---

## 0. Why this thread

v2.3 established the decomposition: among Biden-2020 voters who didn't retain Harris in 2024 —
- GenZ 18-27: **71% SKIPPED**, 24% flipped Trump, 7% third party
- MillYoung 28-35: 50% skipped, 39% flipped Trump (only cohort where flipping rivals skipping)
- MillOld 36-43: 56% skipped, ~38% flipped Trump
- Older cohorts: 50-60% skipped

v2.1–v2.6 looked for mediators of the cohort_eff on Harris-vote within 2-party voters and ruled out 12 candidates (ideology, trust, anti-system, Trump-ft×cohort, party-ID-strength, 41-item lasso multivariate, life-stage, mobilization-as-cohort-mediator, mainstream-media diet, financial worry, etc.). σ_cohort sat at 0.40-0.55 across every test.

**v2.9 reframes:** instead of "what mediates the cohort signal on Harris-vote," ask "**among Biden-2020 voters, what predicts SKIP vs RETAIN — and does the predictor pattern differ for GenZ?**" The outcome universe shifts; mediator-hunt was the wrong question for a defection that operates primarily through demobilization (skipping) rather than persuasion (flipping).

---

## 1. Substrate, universe, and outcome

**Substrate:** CES 2024 Common Content with VV (validated voter-file via TargetSmart, file `CCES24_Common_OUTPUT_vv_topost_final.csv`).

**Universe (LOCKED):**
- `vvweight_post > 0` (VV-matched, post-stratification weight valid)
- `presvote20post == 1` (Biden 2020 reported)
- `birthyr` valid (1900-2010)
- `TS_g2024` populated (voter-file status non-missing)
- One of two outcome buckets (below)
- **Universe N expectation:** ~16,000-18,000 after exclusions (v2.3 had N=18,067 before TS_g2024 missingness filter).

**Outcome (LOCKED):** binary `skipped`
- `skipped == 1` if `TS_g2024 == 7` (VV says did not turn out)
- `skipped == 0` if `TS_g2024 ∈ {1,2,3,4,5,6}` (VV says turned out) **AND** `CC24_410 == 1` (self-reported Harris vote)
- **Excluded:** flipped Trump (`CC24_410 == 2`), flipped third (`CC24_410 ∈ {3,4,5,8}`), voted-unknown-choice (`CC24_410` missing despite TS turnout), and `vf_match_missing`.

**Rationale for excluding flippers:** the question is specifically "skip vs retain." Flipping is a separate mechanism handled in v2.4/v2.5/v2.6/v2.7. If we want to test 3-way later (skip/retain/flip), that is a separate model — flagged as v2.10 candidate.

**Sample-size expectation per pre-reg §4:** at universe N ≈ 16-18k and cohort weights from v2.3, GenZ subset N ≈ 1,200-1,500; MillYoung N ≈ 1,400-1,700; this is sufficient for hypothesis-specific coefficient credibility tests but tight for cell-level (cohort × race) interactions in H_SKIP_E. Cell-N tracking documented in result §10.

---

## 2. Hypotheses (LOCKED, ordered C → A → E → D → B per user direction)

All five hypotheses share:
- **Model:** hierarchical Bayesian logistic regression on `skipped`.
- **Random intercepts:** race (8 levels), educ (5 levels), gender (4 levels), region (4 levels).
- **Fixed effects (baseline controls present in EVERY model):** cohort_idx (6 levels: Silent/Boomer/GenX/MillOld/MillYoung/GenZ), pid7_z (z-scored 7-pt party ID), faminc_z (z-scored 16-pt family income), employ_dummies (8 employment categories, omit modal).
- **Hypothesis-specific predictor(s):** added one model at a time, NOT combined (avoids over-controlling and post-treatment bias from inter-mediator overlap).
- **Settings (LOCKED hardened, per v2.0.1):** chains=6, warmup=1000, samples=1000, seed=42.
- **Convergence acceptance:** R̂ ≤ 1.01 (max), ESS_bulk ≥ 400 (min), divergent transitions <2% of post-warmup samples.

### 2.1 H_SKIP_C — Issue-dissatisfaction mechanism

**Hypothesis (LOCKED):** Biden-2020 voters who skipped 2024 differ from retainers on at least one of {economic perception, immigration policy, climate policy, abortion policy} after controlling for cohort, pid7, demographics. Direction-specific: skippers will show MORE rightward economic perception (econ_z toward "worse") and/or MORE leftward issue position on at least one of {immigration, abortion, climate}.

**V-codes (LOCKED):**
- `CC24_303` — economic retrospective evaluation (5-pt, ∼100% valid in universe). Code reverse-scaled so higher = worse. z-score.
- `CC24_323a` — immigration policy item 1 (binary support/oppose, ∼100% valid). Reverse-code if needed so 1=more progressive.
- `CC24_323b` — immigration policy item 2.
- `CC24_326a` — abortion policy item 1 (binary, ∼100% valid).
- `CC24_326b` — abortion policy item 2.
- `CC24_330a` — climate policy item 1 (8-pt; collapse to binary above-median = pro-climate, ∼100% valid).
- `CC24_330b` — climate policy item 2.

**Operationalization:**
- `issue_econ_z` = z-score of CC24_303 (higher = worse retrospective evaluation).
- `issue_imm_z` = z-score of mean(CC24_323a_progressive, CC24_323b_progressive) where each item is recoded 1=progressive/0=conservative based on codebook direction (locked post-§10 verification).
- `issue_abor_z` = z-score of mean(CC24_326a_pro_choice, CC24_326b_pro_choice).
- `issue_clim_z` = z-score of mean(CC24_330a_pro_climate, CC24_330b_pro_climate) (binary collapsed).
- Four separate model fits, one for each issue z-score (avoids over-fitting; testing whether ANY issue dimension predicts skip after controlling for cohort/pid7).

**Decision rule (LOCKED):**
- Per issue: β credibly non-zero (95% CI excludes zero) AND |β_standardized| ≥ 0.10 → CONFIRMED for that issue.
- Per issue: |β| < 0.05 and CI includes zero → NULL.
- Per issue: 0.05 ≤ |β| < 0.10 or CI marginal → INDETERMINATE.
- **GenZ-subset interaction:** add `issue_X_z × cohort_GenZ_indicator` term. Interaction credibly non-zero with |β_interaction| ≥ 0.10 → "issue dissatisfaction is GenZ-specific."
- **Aggregate H_SKIP_C verdict:**
  - 0 of 4 issues CONFIRMED → H_SKIP_C REFUTED.
  - 1-2 of 4 CONFIRMED → H_SKIP_C PARTIAL.
  - 3-4 of 4 CONFIRMED → H_SKIP_C CONFIRMED.

### 2.2 H_SKIP_A — Engagement / political-interest gradient

**Hypothesis (LOCKED):** Biden-2020 voters who skipped have LOWER baseline political engagement than retainers, controlling for cohort and demographics. Skippers are not necessarily disaffected — they may have been peripheral participants in 2020 who didn't sustain engagement to 2024.

**V-codes (LOCKED):**
- `CC24_310a` — political activity 1 (4-pt: e.g., signed petition; ∼100% valid).
- `CC24_310b` — political activity 2 (4-pt).
- `CC24_310c` — political activity 3 (4-pt).
- `CC24_310d` — political activity 4 (4-pt).
- `CC24_311a` — political talk frequency 1 (5-pt; ∼100% valid).
- `CC24_311b` — political talk frequency 2 (5-pt).
- `CC24_311c` — political talk frequency 3 (5-pt).
- `CC24_311d` — political talk frequency 4 (5-pt).

**Note re CC24_300a:** newsint (3-pt) is the obvious news-interest item but only 11,486 / 18,224 valid in universe (63%). EXCLUDED from primary composite to avoid 37% missingness imputation. Available as sensitivity check via missing-indicator dummy (§10 candidate).

**Operationalization:**
- `engage_act_z` = z-score of mean of CC24_310a-d (reverse-coded so HIGH = MORE engagement, per codebook direction locked at impl time).
- `engage_talk_z` = z-score of mean of CC24_311a-d (reverse-coded so HIGH = MORE engagement).
- `engage_composite_z` = z-score of mean(engage_act_z, engage_talk_z) for combined index.
- Primary model: `engage_composite_z` as single predictor.
- Sensitivity: separate fits with engage_act_z and engage_talk_z (split-half reliability check).

**Decision rule (LOCKED):**
- Primary `engage_composite_z` β credibly negative (95% CI excludes zero) AND |β| ≥ 0.20 → STRONG CONFIRMED (engagement strongly predicts skip).
- β credibly negative AND 0.10 ≤ |β| < 0.20 → WEAK CONFIRMED.
- CI includes zero OR |β| < 0.10 → NULL.
- **GenZ-subset interaction:** `engage_composite_z × cohort_GenZ_indicator` credibly more negative for GenZ → "engagement gradient steeper for GenZ skippers."
- Split-half (act vs talk) signs MUST agree for CONFIRMED verdict; sign-disagreement → INDETERMINATE.

### 2.3 H_SKIP_E — Demographic concentration (race × cohort cells)

**Hypothesis (LOCKED):** Biden-2020 skipping is concentrated in specific race × cohort cells beyond what cohort + race main effects predict. Specifically: GenZ × Black, GenZ × Hispanic, MillYoung × Hispanic — three cells highlighted by v1.1, v2.0, v2.4 race-interaction findings.

**V-codes (LOCKED):**
- `birthyr` → cohort6 (Silent/Boomer/GenX/MillOld/MillYoung/GenZ) per v2.4 boundaries.
- `race` (CES native, 8-level: white/black/hispanic/asian/nhpi/other/middle-eastern/2+races). Collapse to 6-level (white/black/hispanic/asian/nhpi/other) for cell-size sufficiency.

**Model:**
- Hierarchical logistic regression with cohort, race main effects + cohort × race interaction.
- Random intercepts for educ, gender, region.
- Baseline controls: pid7_z, faminc_z.
- Predictor matrix: full 6 × 6 cohort × race interaction (mean-centered, soft-summing constraint).

**Operationalization:**
- Cell-level posterior mean of `skip_rate_cell - skip_rate_cohort_marginal`.
- Cell N tracking per pre-reg §1.

**Decision rule (LOCKED):**
- For each candidate cell {GenZ×Black, GenZ×Hispanic, MillYoung×Hispanic}: posterior P(skip_rate_cell - skip_rate_cohort_marginal > 0) ≥ 0.95 AND posterior median lift ≥ +10pp → CELL CONFIRMED.
- For each cell: posterior median lift in [+3pp, +10pp] OR P < 0.95 → INDETERMINATE.
- For each cell: posterior median lift < +3pp OR P(>0) ≤ 0.50 → NULL.
- **Aggregate H_SKIP_E verdict:**
  - 2-3 of 3 candidate cells CONFIRMED → H_SKIP_E CONFIRMED (demographic concentration is real).
  - 1 of 3 CONFIRMED → H_SKIP_E PARTIAL.
  - 0 of 3 CONFIRMED → H_SKIP_E REFUTED.

**Honest caveat:** with N≈18k and 36 cells, cell-N for GenZ × Black ≈ 100-150, GenZ × Hispanic ≈ 80-130, MillYoung × Hispanic ≈ 150-200. Cell-level posteriors will be wide. Per pre-reg §1, the gate is intentionally conservative (require ≥10pp lift, not just credible non-zero).

### 2.4 H_SKIP_D — Trust / efficacy collapse

**Hypothesis (LOCKED):** Biden-2020 voters who skipped report LOWER trust in elections and/or political institutions than retainers, suggesting 2024-specific election-integrity narratives or accumulated efficacy collapse demobilized them.

**V-codes (LOCKED):**
- `CC24_443_1` — trust battery item 1 (5-pt, 100% valid).
- `CC24_443_2` — trust battery item 2 (5-pt).
- `CC24_443_3` — trust battery item 3 (5-pt).
- `CC24_443_4` — trust battery item 4 (5-pt).
- `CC24_443_5` — trust battery item 5 (5-pt).
- `CC24_444a` — election integrity binary 1 (∼100% valid).
- `CC24_444b` — election integrity binary 2.
- `CC24_444c` — election integrity binary 3.
- `CC24_444d` — election integrity binary 4.
- `CC24_445a` — election confidence binary 1.
- `CC24_445b` — election confidence binary 2.

**Operationalization:**
- `trust_inst_z` = z-score of mean(CC24_443_1..5) reverse-coded so HIGH = MORE trust per codebook (locked pre-fit).
- `trust_elec_z` = z-score of mean(CC24_444a-d, CC24_445a-b) reverse-coded so HIGH = MORE election confidence (binary items → 0/1, mean across 6).
- Two separate model fits (one per composite).
- `trust_combined_z` = z-score of mean(trust_inst_z, trust_elec_z) for combined model.

**Decision rule (LOCKED):**
- Per composite: β credibly negative (95% CI excludes zero) AND |β| ≥ 0.20 → STRONG CONFIRMED for that composite.
- 0.10 ≤ |β| < 0.20 with credibility → WEAK CONFIRMED.
- |β| < 0.10 or CI crosses zero → NULL.
- **Aggregate H_SKIP_D verdict:**
  - Both trust_inst_z AND trust_elec_z STRONG → H_SKIP_D STRONG CONFIRMED.
  - One STRONG and one WEAK → H_SKIP_D WEAK CONFIRMED.
  - Both NULL → H_SKIP_D REFUTED.
  - Other → PARTIAL.
- **GenZ-subset interaction:** trust × GenZ interaction tested; if interaction credibly more negative for GenZ → "trust collapse is GenZ-specific demobilizer."

### 2.5 H_SKIP_B — Direct mobilization gap

**Hypothesis (LOCKED):** Biden-2020 skippers received LESS campaign contact in 2024 than retainers. **Sharper than v2.6 H27 (which tested campaign contact as cohort-mediator and was REFUTED at the cohort-mediator level):** here, contact is tested as DIRECT predictor of skip-vs-retain, NOT as a cohort mediator.

**V-codes (LOCKED):**
- `CC24_363` — campaign contact in 2024 cycle (6-pt, 100% valid in universe). Likely: 1=contacted by Dems only, 2=Reps only, 3=both, 4=neither, 5=other, 6=DK. **Operationalization verified pre-fit; if values don't conform, recode to {any_contact=1, no_contact=0} per codebook §10.**

**Operationalization:**
- `mob_any_z` = binary 1=any campaign contact (CC24_363 ∈ {1,2,3,5}), 0=no contact (CC24_363 ∈ {4,6}). z-scored.
- `mob_dem_z` = binary 1=contacted by Democrats (CC24_363 ∈ {1,3}), 0=not. z-scored. (Sharper test — Democratic ground game directly.)
- Two separate model fits, one for each binary.

**Decision rule (LOCKED):**
- `mob_any_z` β credibly negative (95% CI excludes zero) AND |β| ≥ 0.20 → STRONG CONFIRMED (mobilization gap real).
- 0.10 ≤ |β| < 0.20 → WEAK CONFIRMED.
- `mob_dem_z` β STRONGER negative than mob_any_z → "Democratic-side mobilization gap dominates" finding.
- All-NULL → REFUTED (v2.6 finding extends: even at direct level, mobilization isn't the skip story).
- **GenZ-subset interaction:** mob × GenZ interaction credibly different → "GenZ disproportionately under-mobilized" (or over-, depending on sign).

---

## 3. Aggregate v2.9 verdict logic

Build a 5-row scorecard:

| Hyp | Verdict | GenZ-specific? |
|---|---|---|
| H_SKIP_C | CONFIRMED / PARTIAL / NULL / REFUTED | yes/no/INDET |
| H_SKIP_A | STRONG / WEAK / NULL | yes/no/INDET |
| H_SKIP_E | CONFIRMED / PARTIAL / REFUTED | n/a (cell-level) |
| H_SKIP_D | STRONG / WEAK / NULL / REFUTED | yes/no/INDET |
| H_SKIP_B | STRONG / WEAK / NULL / REFUTED | yes/no/INDET |

**Aggregate framing (LOCKED):**
- **≥3 of 5 CONFIRMED (any strength):** "SKIP MECHANISM IDENTIFIED — multi-channel demobilization with channels [list]."
- **2 of 5 CONFIRMED:** "SKIP MECHANISM PARTIAL — channels [list] are the primary demobilizers; others are NOT IT."
- **1 of 5 CONFIRMED:** "Single-channel skip mechanism — [channel]; v3 needs out-of-CES data on remaining mechanisms."
- **0 of 5 CONFIRMED:** "SKIP MECHANISM NOT IN CES BATTERY — youth disengagement is unmeasured in CES public release; v3 needs ANES restricted release, supplementary surveys, or qualitative data."

**Strong null is a valid outcome.** Per the v2.1-v2.6 pattern, the most honest possibility is that the skip mechanism is also not in the standard battery — which would tighten the v3 data-acquisition argument from §5 in NEXT.md.

---

## 4. Falsifiers (LOCKED, fired BEFORE result interpretation)

1. **F1 — Universe N collapse:** if universe N < 12,000 after exclusions, → STOP, document in §10, refit with relaxed universe (drop the strictest filter — likely TS_g2024 non-missing).
2. **F2 — Outcome imbalance:** if skip prevalence in universe is outside [25%, 65%] of universe (way different from v2.3's 50-71% by cohort) → investigate via §10 dev before fit interpretation.
3. **F3 — pid7_z dominates:** if pid7_z (a control) absorbs more than 70% of variance in the skip outcome, hypothesis-specific predictors may be over-controlled; report alongside no-pid7 sensitivity fit.
4. **F4 — Codebook orientation mismatch:** if any composite shows direction opposite expected (e.g., trust_inst_z predicts MORE skip), verify codebook direction at result-writing time and document orientation correction in §10. (Pattern: K-S §10 dev 7 incident in v2.0.1 — DO NOT REPEAT.)
5. **F5 — Convergence failure:** if R̂ > 1.01 OR ESS_bulk < 400 OR divergents > 2%, refit with chains=8, warmup=2000, samples=2000 (escalated), document in §10.

---

## 5. Hardened fit settings

LOCKED per v2.0.1+ pattern:
- chains = 6
- warmup = 1000
- samples = 1000
- seed = 42
- Stan model: `model_a_skip.stan` (new — binary hierarchical logistic, same structure as model_a.stan but on `skipped` outcome). Reuse model_a.stan if shape matches; create model_a_skip_with_interaction.stan only if H_SKIP_E cell model requires custom indexing.

---

## 6. Code artifact

`code/v29_skip_mechanism.py` (TO BUILD post-pre-reg lock):
- Loads CES, builds universe per §1.
- Builds outcome `skipped`, all 5 hypothesis predictors per §2.
- Fits 5 primary models + cohort-interaction sensitivity for A/C/D/B (4 extra) = 9 fits total.
- Outputs `result_v2.9_skip_mechanism.csv` with per-hypothesis verdicts.

---

## 7. Out-of-scope

- 3-way SKIP/RETAIN/FLIP multinomial (deferred to v2.10).
- ANES skipper subset (ANES universe doesn't ID skippers cleanly per NEXT.md §2; deferred).
- Pew W159 cross-check (smaller N, less granular cohort; deferred to v2.10 sensitivity).
- Specific Gaza skip-channel test (no Gaza item in CES public release; would require ANES-PRE V241404 but ANES outcome cannot identify skip vs retain). Filed as v3 data-acquisition gap.

---

## 8. Repository state at pre-reg lock

- HEAD `0b008b8` (NEXT.md compaction handoff).
- Branch `main`, pushed to origin.
- No outstanding fits.
- Memory pointers refreshed.

---

## 9. §10 deviation log (to be populated during impl/fits)

(Empty at lock. All deviations from §2-§5 to be logged with timestamps + rationale before result interpretation.)
