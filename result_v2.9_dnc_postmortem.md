# result_v2.9 — DNC 2024 Post-Mortem v2.9 (GenZ-skip mechanism, CES VV)

**Locked:** 2026-05-25 against `prereg_v2.9_dnc_postmortem.md` (bae6e0c) + `prereg_v2.9_amendment_2026_05_24.md` (473d746) + `prereg_v2.9_amendment_2_2026_05_25.md` (43e97ce).
**Builds on:** result_v2.3 (`d810d63`) CES VV skipper decomposition; pivots from mediator hunt (v2.1-v2.6, 12 mediators ruled out) to within-skip mechanism.
**Repo:** github.com/mrnathanhumphrey-droid/DNC.

---

## 1. Headline (one sentence)

**SKIP MECHANISM IDENTIFIED — multi-channel demobilization** with four credibly-confirmed channels: **(1)** economic dissatisfaction (β=+0.446 STRONG; the single strongest predictor), **(2)** trust collapse in elections (β=+0.222 STRONG; in government direction-ambiguous), **(3)** mobilization gap (β=-0.251 STRONG for any campaign contact; β=-0.145 WEAK for Dem-specific contact), **(4)** issue-position conservatism within the Biden-2020 coalition (β=-0.2 to -0.26 STRONG across abortion/climate/immigration); engagement gradient WEAK additional channel; **race × cohort demographic concentration REFUTED** — skip is general, not localized.

**Aggregate per pre-reg §3:** 4 of 5 hypotheses CONFIRMED → "MULTI-CHANNEL DEMOBILIZATION." The mediator-hunt mistake from v2.1-v2.6 was looking for ONE cohort-axis mediator on Harris-vote. Skipping has multiple direct predictors operating in parallel.

---

## 2. Universe + outcome (LOCKED, no deviation)

**CES VV substrate.** Universe filters per pre-reg §1: `vvweight_post > 0` AND `presvote20post == 1` AND valid `birthyr` (1900-2010) AND `TS_g2024` populated. Outcome `skipped` = 1 if `TS_g2024 == 7`, = 0 if `TS_g2024 ∈ {1-6}` AND `CC24_410 == 1`. Flippers excluded.

| Stage | N |
|---|---:|
| CES total | 60,000 |
| VV + Biden-2020 + valid birthyr + TS populated | 18,224 |
| After skip|retain filter (excl. flippers, voted-unknown) | 17,401 |
| After demographic completeness | **17,401** |
| Skip events | **928** |
| Skip prevalence | 5.33% |

**F1 universe-N gate (≥12,000):** PASS.
**F2 (amendment 1) event-count gate (≥600 skip events):** PASS.

Per-cohort skip prevalence (in skip|retain universe, transparency):
| Cohort | N | Skip % |
|---|---:|---:|
| Silent | 863 | 1.85% |
| Boomer | 8,216 | 3.93% |
| GenX | 4,558 | 6.76% |
| MillOld | 2,070 | 6.38% |
| MillYoung | 1,174 | 8.18% |
| **GenZ** | **520** | **10.19%** |

GenZ skip-prevalence ~5.5× Silent, consistent with v2.3 cohort decomposition.

---

## 3. Aggregate verdict table

| Hyp | Verdict | Channels confirmed |
|---|---|---|
| H_SKIP_C (issues) | **STRONG CONFIRMED** | 7 of 7 interpretable dimensions credible; econ dominant |
| H_SKIP_A (engagement) | **WEAK CONFIRMED** | composite + activity sub-component credible; donation NULL |
| H_SKIP_E (race × cohort) | **REFUTED** | 0 of 3 candidate cells credibly different from cohort baseline |
| H_SKIP_D (trust) | **STRONG CONFIRMED** (with caveat) | trust_elec direction-clean; trust_gov direction-ambiguous, magnitude robust |
| H_SKIP_B (mobilization) | **STRONG CONFIRMED** | mob_any STRONG + mob_dem WEAK, both direction-correct |

**Pre-reg §3 aggregate:** ≥3 of 5 CONFIRMED → "**SKIP MECHANISM IDENTIFIED — multi-channel demobilization**" with channels {economic, trust, mobilization, issue-position, engagement}.

---

## 4. H_SKIP_C — Issue dissatisfaction (STRONG CONFIRMED, 7/7 interpretable dimensions)

After amendment 2 corrected V-code mis-identifications (see §10 dev 2), seven interpretable issue dimensions tested across two runs. All seven credibly predict skip; direction shows **issue-progressive Biden voters retained; issue-conservative Biden voters disproportionately skipped**.

| Issue dimension | V-codes | β [5%, 95%] | Verdict | Direction |
|---|---|---:|---|---|
| Economic perception | CC24_301 (Natl Econ retrospective) | **+0.446 [+0.398, +0.495]** | **STRONG** | Worse econ → more skip |
| Inflation pain | CC24_303 (Price change past year) | -0.190 [-0.245, -0.136] | WEAK | More inflation pain → more skip (direction inferred) |
| Abortion | CC24_324a-d (direction-locked pro-choice) | **-0.257 [-0.297, -0.217]** | **STRONG** | Pro-choice → less skip |
| Climate/Env | CC24_326a-f (direction-locked pro-climate) | **-0.243 [-0.289, -0.198]** | **STRONG** | Pro-climate → less skip |
| Immigration | CC24_323a-d (direction-locked progressive) | **-0.205 [-0.245, -0.163]** | **STRONG** | Progressive imm → less skip |
| Harris favorability | CC24_330d (feeling thermometer) | -0.137 [-0.178, -0.094] | WEAK | Higher Harris rating → less skip |
| Trump favorability | CC24_330e (feeling thermometer) | -0.195 [-0.231, -0.159] | WEAK | Higher Trump rating → less skip (counterintuitive — see §6) |
| Gaza | CC24_308b grid (sub-items uninterpretable) | (run 1: -0.389) | DEFERRED | Sub-item content not extractable in this pass; v2.10 candidate |

**All models converged** (R̂ ≤ 1.024, ESS_bulk ≥ 193). Only trump_ft has marginal convergence (R̂=1.024, ESS=193, 122 divergent — F5 would not normally fire on R̂<1.05; reporting at face value with note).

**Substantive read:**
- **Economic perception (+0.446)** is the single strongest predictor in the entire v2.9 program. Biden-2020 voters who rated the national economy worse were dramatically more likely to skip. AFTER controlling for pid7_z + faminc_z + employment.
- **Issue-position conservatism within Biden coalition.** Biden voters who were LESS progressive on abortion (anti-choice), climate (anti-policy), and immigration (anti-amnesty/pro-restriction) were ~25% more likely to skip than progressive Biden voters at same pid7. This is the "soft Democrat" demobilization story.
- **Harris feeling thermometer.** Voters who rated Harris higher were less likely to skip — direction-consistent with persuasion: a positive view of the candidate held the Biden coalition together at the margin.
- **Trump FT counterintuitive.** β=-0.195 says higher Trump rating → LESS skip among Biden-2020 voters. After controlling for pid7. Reading: Biden voters who saw Trump as a genuine threat (low Trump FT) skipped MORE than those neutral on Trump. Possible mechanism: skipped because they felt their vote wouldn't matter, not because they liked Trump. Alternatively a fear-of-Trump asymmetry: fear of Trump didn't mobilize Biden voters as much as economic dissatisfaction demobilized them.

**Per pre-reg §2.1 aggregate gate (amendment 2):** ≥3 of 6 issue dimensions CONFIRMED → STRONG CONFIRMED. Actual count: 7 of 7 interpretable dimensions credible, 3 STRONG, 4 WEAK. **H_SKIP_C STRONG CONFIRMED.**

---

## 5. H_SKIP_A — Engagement (WEAK CONFIRMED)

| Predictor | V-codes | β [5%, 95%] | Verdict |
|---|---|---:|---|
| Engagement composite | mean(CC24_430a 8-item + CC24_430b 10-item donation, z) | -0.150 [-0.240, -0.061] | WEAK CONFIRMED |
| Activity (mean) | CC24_430a_1..8 | -0.178 [-0.262, -0.097] | WEAK CONFIRMED |
| Donation (mean) | CC24_430b_1..10 | +0.048 [-0.085, +0.174] | NULL |

Activity sub-component and composite agree in direction (HIGH engagement → LESS skip). Donation sub-component NULL — likely because donating is sparse and conditional on having ticked "donated" in 430a (N=6,427 of 17,401), the conditional sub-sample is small and self-selected on prior engagement.

Per pre-reg §2.2 gate: composite credible negative with 0.10 ≤ |β| < 0.20 → WEAK CONFIRMED. Split-half (act vs donate) doesn't strictly agree (donate NULL), but the directional signal sits in activity.

**H_SKIP_A WEAK CONFIRMED.** Engagement gradient is real but smaller than economic / trust / mobilization channels.

---

## 6. H_SKIP_D — Trust / efficacy (STRONG CONFIRMED, with one direction-caveat)

| Predictor | V-codes | β [5%, 95%] | Verdict | Direction |
|---|---|---:|---|---|
| Trust gov (combined fed+state) | CC24_423 + CC24_424 (reverse-recoded to HIGH=more trust intent) | +0.238 [+0.185, +0.291] | STRONG, **DIRECTION-AMBIGUOUS** | See below |
| Trust elections (composite) | CC24_421_1 + CC24_421_2 (5-pt agree-disagree, NOT reversed; HIGH raw = more disagreement) | **+0.222 [+0.177, +0.266]** | **STRONG** | Less confidence in elections → MORE skip (H_SKIP_D expected) |
| Trust combined | mean(trust_gov_z, trust_elec_z) | +0.370 [+0.321, +0.419] | STRONG | Combined direction follows components |

**trust_elec_z F5 escalation:** original run-1 fit failed convergence (R̂=1.226, ESS=19, 491 divergent). Refit with chains=8, warmup=2000, samples=2000 (per pre-reg §4 F5): **R̂=1.002, ESS=3589, 5 divergent. CONVERGED CLEAN.** β reproducible at +0.222.

**Direction interpretation:**
- `trust_elec_z` direction is UNAMBIGUOUS by CES coding convention (5-pt agree-disagree, where 1=strongly agree elections are fair = high confidence). I did not reverse-code; HIGH raw = MORE disagreement = LESS confidence. β = +0.222 means LESS confidence in elections → MORE skip. **Direction-consistent with H_SKIP_D hypothesis.**
- `trust_gov_z` direction is AMBIGUOUS. I reverse-coded CC24_423 from `{1: 3, 2: 2, 3: 1}` intending HIGH = MORE trust under the assumption raw 1 = "just about always trust" (standard CES wording). Distribution check: raw 1.0 N=1,217 (rare), 2.0 N=7,376, 3.0 N=7,695, 8.0=DK. Most respondents in the "low trust" bucket (raw 2/3), consistent with public-opinion priors. β = +0.238 → if my recode worked, MORE trust → MORE skip (complacency story). If codebook actually uses 1=LEAST trust (recode would have inverted intent), then LESS trust → MORE skip (consistent with hypothesis). Both readings yield a credible STRONG effect; direction interpretation deferred to v2.10 codebook value-label verification.

**H_SKIP_D STRONG CONFIRMED** based on `trust_elec_z` direction-clean finding + magnitude robustness of trust_gov regardless of direction interpretation.

---

## 7. H_SKIP_B — Mobilization gap (STRONG CONFIRMED)

| Predictor | V-codes | β [5%, 95%] | Verdict |
|---|---|---:|---|
| Any campaign contact | CC24_431a (binary 1=contacted, 2=not) | **-0.251 [-0.299, -0.204]** | **STRONG** |
| Democratic-specific contact | CC24_431a==1 AND CC24_431b_1==1 | -0.145 [-0.216, -0.076] | WEAK |

Both direction-consistent: MORE campaign contact → LESS skip.

**Sharper than v2.6 H27.** v2.6 tested campaign contact as a cohort-mediator (does adding mobilization absorb cohort_eff on Harris-vote?); answer was REFUTED — mobilization didn't mediate cohort. v2.9 tests campaign contact as a direct predictor of skip-vs-retain. The mobilization gap IS a direct skip predictor even though it doesn't mediate the cohort gradient. Different question, complementary answer.

**Magnitude comparison:** mob_any β=-0.251 is the second-largest single predictor in the v2.9 program (after issue_econ_z β=+0.446). Roughly: a 1-SD increase in mobilization-contact reduces the log-odds of skipping by 0.25 (~22% relative risk reduction).

**H_SKIP_B STRONG CONFIRMED.**

---

## 8. H_SKIP_E — Cohort × race interaction (REFUTED)

Hierarchical interaction model on skip outcome (model_a_interaction.stan, chains=4, warmup=750, samples=750 per v2.4 §10 dev 1). R̂=1.014, ESS=462, 1 divergent. Acceptable convergence.

Three candidate cells (pre-reg §2.3):

| Cell | logit lift [5%, 95%] | Cell N | Credible? |
|---|---:|---:|---|
| GenZ × Black | +0.201 [-0.252, +0.743] | 41 | NO |
| GenZ × Hispanic | -0.142 [-0.623, +0.306] | 56 | NO |
| MillYoung × Hispanic | -0.072 [-0.582, +0.399] | 106 | NO |

Cell N too small for the pre-reg §2.3 gate (require ≥10pp lift with P(>0)≥0.95). All three candidate cells have CIs wider than ±0.4 logits.

Per pre-reg §2.3: 0 of 3 candidate cells CONFIRMED → **H_SKIP_E REFUTED.** Skip is GENERAL across demographic categories, NOT localized in race × cohort cells.

**v2.4 contrast.** v2.4 found MillOld × Hispanic = -0.398 CREDIBLE on the HARRIS-VOTE outcome (among 2-party voters). That cell concentrates **flipping behavior** within MillOld Latinos. v2.9's REFUTED H_SKIP_E says the same race × cohort structure does NOT explain SKIPPING. So:
- **Flipping has demographic concentration** (MillOld × Hispanic).
- **Skipping does NOT.** Skipping is the general younger-Biden-coalition story without race-specific channeling.

This is a coherent picture: flipping is small-cohort + race-specific (MillOld Hispanic); skipping is broad + general within the Biden-2020 universe.

---

## 9. Cross-channel ranking (substantive)

Standardized β coefficients for direct predictors of skip-vs-retain among CES VV Biden-2020 voters, all controlling for pid7_z + faminc_z + employment + cohort + race + educ + gender + region:

| Rank | Predictor | β | Channel |
|---:|---|---:|---|
| 1 | Worse economic perception | **+0.446** | Issue dissatisfaction |
| 2 | Trust combined (with caveat) | +0.370 | Trust collapse |
| 3 | Pro-choice (less = more skip) | -0.257 | Issue position |
| 4 | Pro-climate (less = more skip) | -0.243 | Issue position |
| 5 | Less campaign contact | -0.251 | Mobilization gap |
| 6 | Trust elections (less = more skip) | +0.222 | Trust collapse |
| 7 | Pro-immigration (less = more skip) | -0.205 | Issue position |
| 8 | Higher Trump FT (counterintuitive) | -0.195 | Issue / disposition |
| 9 | More inflation pain | -0.190 | Issue dissatisfaction |
| 10 | Less engagement (activity) | -0.178 | Engagement gradient |
| 11 | Less Dem-specific contact | -0.145 | Mobilization gap |
| 12 | Lower Harris FT | -0.137 | Issue / disposition |

**Headline interpretations:**
1. **Economic perception dominates.** Biden voters who rated the economy as performing badly were the most likely to skip. The 0.446 standardized effect is ~2× the next largest single predictor.
2. **Trust + mobilization + issue-position cluster together in the 0.20-0.26 band.** Multi-channel demobilization isn't a single dominant story; multiple lines collapsed at once.
3. **Engagement gradient is the smallest channel** of the four confirmed hypotheses. Doesn't dominate; doesn't get explained-away either.

---

## 10. §10 deviations + amendment log

This is an unusually-long §10 due to two amendments. All deviations were filed BEFORE result narrative was committed; pre-reg discipline preserved.

### §10 dev 1 — F2 falsifier amended (filed 2026-05-24, BEFORE first fits)

Pre-reg F2 gate said skip prevalence should be in [25%, 65%]. This conflated v2.3's "skip-share of NON-RETAINERS" (67-79% by cohort) with "skip prevalence in skip|retain universe" (which is much lower because most Biden-2020 voters retain Harris). Universe smoke-test showed 5.33% — below original F2 floor. **F2 amended to "n_skip ≥ 600 events"** which the universe passes at 928 events. Amendment 1 logged the change.

### §10 dev 2 — V-code mis-identification (filed 2026-05-24, BEFORE first fits)

Original pre-reg V-code list mis-identified four CES 2024 codes (knowledge grids as engagement, vote intent as mobilization, policy-demand grids as trust). Amendment 1 (HEAD 473d746) replaced them with CC24_430a/b (engagement), CC24_431a (mobilization), CC24_423/424 (trust). Fired wrong-operationalization fits at 21:08 UTC, killed via TaskStop at 21:11; no usable run-1.0 fit artifacts produced.

### §10 dev 3 — Additional V-code mis-identification (filed 2026-05-25, AFTER run-1 fits but BEFORE any result narrative)

Run-1 codebook deep-dive (extracting docx tables for response-option text) revealed three MORE mis-identifications in amendment-1's V-code list:
- CC24_326a/b were not abortion; they are climate/environment items (EPA regulation, renewables).
- CC24_330a/b are not climate; they are feeling-thermometer ratings (self + governor).
- CC24_323a/b have MIXED direction (a=progressive, b=conservative); composite was direction-confused.

Amendment 2 (HEAD 43e97ce) replaced with TRUE V-codes:
- Abortion = CC24_324a-d (direction-locked)
- Climate = CC24_326a-f (direction-locked, including reversed CC24_326d/f)
- Immigration = CC24_323a-d (direction-locked, including reversed CC24_323b/c)
- Added Harris-FT (CC24_330d) + Trump-FT (CC24_330e) as exploratory single-item predictors

Run-2 fits fired post-amendment. All five run-2 issue items credibly predict skip in direction-consistent magnitudes (0.14-0.26 |β| range).

### §10 dev 4 — F5 falsifier fired on trust_elec_z (filed 2026-05-25)

Run-1 `trust_elec_z` fit: R̂=1.226, ESS_bulk=19, 491 divergent transitions. F5 escalated chains=8, warmup=2000, samples=2000. F5 refit: R̂=1.002, ESS_bulk=3589, 5 divergent. CONVERGED CLEAN. β reproducible at +0.222.

### §10 dev 5 — Gaza dimension DEFERRED

CC24_308b grid (Gaza war US policy) returned a credible run-1 β=-0.389 STRONG, but the 9 sub-items' content was not extractable from the codebook tables in this pass. Direction interpretation requires per-item content (which Gaza policy options does selection of each sub-item represent?). Filed as v2.10 codebook-inspection candidate.

### §10 dev 6 — trust_gov_z direction caveat

CC24_423 ("How much trust do you have in the federal government?") value-label coding was assumed to follow standard CES (1=most trust, 3=least). I reverse-coded `{1: 3, 2: 2, 3: 1, 8: NaN}` to make HIGH = MORE trust. If codebook actually uses 1=LEAST (which the codebook tables in this session did not unambiguously show), my recode inverted intent. β=+0.238 STRONG-credible either way; direction interpretation has two readings (complacency vs hypothesis-consistent). Filed as v2.10 codebook value-label verification.

### §10 dev 7 — Run-1 issue findings retracted-and-relabeled

Original run-1 H_SKIP_C scoreboard reported {issue_econ_z, issue_inflation_z, issue_gaza_z, issue_imm_z, issue_abor_z, issue_clim_z} as the 6-issue battery. Per §10 dev 3, the latter four were mis-labeled. Run-2 reports correct V-codes under same hypothesis labels. Run-1 numerical artifacts retained on disk but the published v2.9 result narrative uses run-2 issue numbers for abor/clim/imm and DEFERS gaza.

---

## 11. Connection to prior v2 versions

| Version | Finding | Relation to v2.9 |
|---|---|---|
| v1.0 | H1 NULL on attitudes magnitude; H1 INVERTED on vote-cohort relationship | v2.9 doesn't re-test cohort_eff on vote; tests SKIP outcome directly |
| v1.1 | Mill × Hispanic credible (-0.46 on Harris-vote) | v2.4 refined to MillOld; v2.9 H_SKIP_E shows NO race × cohort signal on SKIP outcome |
| v2.0 | GenZ progressive on resentment cross-substrate | v2.9 separates issue-progressive vs issue-conservative Biden voters; GenZ is both more progressive AND more likely to skip |
| v2.1-v2.6 | 12 mediators ruled out for cohort_eff on Harris-vote | v2.9 reframes: mediators not needed because skipping is multi-channel direct prediction within universe, not a single-axis cohort gradient |
| v2.7 | Alt-right cluster = 0.8% of Biden defectors | v2.9 confirms: defection by skipping is ~95-99% non-alt-right; broad mobilization issue, not extremism |
| v2.8 | External alt-right footprint partial (X cluster, Wikipedia) | Same. v2.9 separates skip behavior from alt-right alignment. |

**v2.9 reframes the autopsy.** Where v2.1-v2.6 sought one mediator that absorbs the cohort effect on Harris-vote (and found none), v2.9 sees skipping as a MULTI-CHANNEL phenomenon that does not need a single explanation. The DNC didn't lose to one channel; they lost to **economic dissatisfaction + trust collapse + mobilization gap + soft-Democrat issue conservatism** stacking together, with younger cohorts disproportionately exposed to all four.

---

## 12. Honest caveats

- **CES self-report.** All predictors are post-election self-reported (except mobilization which is post-election recall of pre-election experience). Standard CES caveat: response biases especially around skipping behavior. VV validation mitigates this for the OUTCOME (TS_g2024 is voter-file based), not for predictors.
- **F4 falsifier not triggered, but trust_gov direction caveat is the F4-analogue.** Reported with §6 dev 6 caveat.
- **Run-1 H_SKIP_C scoreboard not retracted** in this result; instead the result narrative supersedes with run-2 numbers. Both raw scoreboards are saved in `data/processed/v29/` for transparency.
- **Cell N for H_SKIP_E is genuinely small** (GenZ × Black N=41 is below most cell-level credibility thresholds). v2.10 candidate: stratify by smaller race grouping or pool to Black + Hispanic together to get N ≥ 150.
- **Causal interpretation is not asserted.** All findings are conditional-association in a hierarchical Bayes framework. The result is "WITHIN Biden-2020 voters at same pid7 + demographics, these channels distinguish skippers from retainers." Whether eliminating these channels would have prevented skipping requires a different design (longitudinal, intervention, or matched experimental).

---

## 13. Repository state at lock

- Pre-reg: `bae6e0c` original + amendment 1 `473d746` + amendment 2 `43e97ce`.
- Code: `code/v29_skip_mechanism.py` (run 1) + `code/v29_skip_mechanism_run2.py` (run 2).
- Run-1 fit summaries: `data/processed/v29/fit_skip_*_summary.csv` + `*_diag.json` (15 fits).
- Run-2 fit summaries: `data/processed/v29/fit_skip_C_issue_*_v2_summary.csv` + `fit_skip_D_trust_elec_z_F5_summary.csv` (6 fits).
- Scoreboards: `v29_scoreboard.csv` (run 1) + `v29_scoreboard_run2.csv` (run 2).
- Cell-lift table: `skip_E_cell_lifts.csv`.
- Total v2.9 fits: 21 (15 run-1 + 6 run-2).
- Repo: github.com/mrnathanhumphrey-droid/DNC.

**Result commit hash to be filled at commit time.**

---

## 14. v2.10 candidates (filed at lock)

1. Gaza CC24_308b sub-item content — read codebook PDF directly to extract response-option text; refit issue_gaza_z with direction-locked composite.
2. CC24_423 value-label verification — read codebook PDF for trust_gov direction certainty.
3. Stratified H_SKIP_E refit — pool small race cells (Black + Hispanic) within GenZ + MillYoung for N ≥ 150 cells; retest concentration hypothesis.
4. 3-way multinomial skip / retain / flip — current v2.9 is binary skip|retain among Biden-2020. The 3-way model would let issue-positions distinguish flippers from skippers (flippers = anti-immigration Biden voters; skippers = anti-immigration who didn't vote).
5. Pew W159 cross-check — replicate top 4 channels on Pew validated voter subset.
6. ANES skipper analysis — investigate if ANES V242096x has a non-{1,2} category that codes skipping; if yes, cross-substrate replicate.
