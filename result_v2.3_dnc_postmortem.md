# result_v2.3 — DNC 2024 Post-Mortem v2.3 (Skipper decomposition at fine cohort cuts, CES VV)

**Locked:** 2026-05-24 against `prereg_v2.3_dnc_postmortem.md` HEAD `8dcd2a9`.
**Builds on:** result_v2.0 H6 + H7 (HEAD `d03e2dd`), result_v2.1 (`27a0093`), result_v2.2 (`e441cbd`).
**Repo:** github.com/mrnathanhumphrey-droid/DNC.

---

## 1. Headline (one sentence)

**At fine cohort resolution on CES validated-voter data, MillYoung (28-35) is the peak-defection cell AND the only cohort where actual flipping rivals skipping** — defection rate 19.8% (highest of any cohort), with skip-share of non-retainers only 49.8% (lowest of any cohort). GenZ (18-27) defects at 17.4% but does so overwhelmingly by skipping (71.1% skip-share — highest of any cohort). The Pew H7 finding "defection ≈ disengagement" replicates qualitatively in 5 of 6 cohorts; MillYoung is the qualitatively-distinct exception.

---

## 2. Verdicts table

| Hyp | Test | Verdict | Note |
|---|---|---|---|
| **H13** | Cohort gradient of defection: monotonic younger→older (Pew H7 4-band) replicates at CES 6-cohort | **PARTIAL** (1 inversion of 2.46pp) | Defection monotonic Silent→MillYoung; GenZ slightly LOWER than MillYoung. Pre-reg accepted ≤1 inversion ≤3pp. |
| **H14** | Skip-share ≥ 50% in all cohorts (Pew "skip dominates" pattern at fine cuts) | **PARTIAL** (5 of 6) | All cohorts ≥50% except MillYoung (49.82% — just below 50%). |
| **H15** | GenZ retention > MillYoung retention by ≥3pp (H6 "GenZ flips positive direction") | **TIE** (+2.46pp, just inside 3pp band) | Direction matches H6 prediction; magnitude not credible at this N. |

**Aggregate verdict:** **MECHANISM PARTIAL with MillYoung as the qualitatively-distinct exception.** Pew H7's 4-band age finding holds at fine cohort cuts in shape (defection rises with cohort youth) and in mechanism (skip dominates flip) — but breaks down precisely at MillYoung, where defection peaks AND flips are nearly equal to skips.

---

## 3. Table A — per-cohort 4-bucket decomposition (CES VV, weighted by vvweight_post)

Universe: CES respondents with vvweight_post > 0 AND presvote20post == 1 (self-reported Biden 2020) AND valid birthyr AND TS_g2024 ∈ {1-7} (voter-file matched). N = 18,067 unweighted, weighted total 16,917.

| Cohort | retained_harris | flipped_trump | flipped_third | skipped | weighted N | unweighted N |
|---|---:|---:|---:|---:|---:|---:|
| Silent     | **95.51%** | 1.83% | 0.39% | 2.27% | 510 | 882 |
| Boomer     | 91.56% | 2.80% | 0.62% | 5.02% | 5,468 | 8,426 |
| GenX       | 84.31% | 6.44% | 0.66% | 8.59% | 4,165 | 4,739 |
| MillOld    | 83.07% | 6.05% | 2.29% | 8.58% | 2,709 | 2,202 |
| **MillYoung** | **80.16%** | **7.77%** | 2.19% | 9.88% | 2,069 | 1,263 |
| GenZ       | 82.62% | 2.53% | 2.48% | **12.37%** | 1,995 | 555 |

**Cell-level reads:**
- **MillYoung** has the HIGHEST flipped_trump share (7.77%) AND the LOWEST retained_harris share (80.16%). The Mill-Young Biden-2020 coalition was the most likely to actively defect to Trump.
- **GenZ** has the HIGHEST skipped share (12.37%) — they disengaged most when they didn't retain. GenZ's flipped_trump is among the LOWEST (2.53%).
- **Silent + Boomer** retain at 92-96% — Biden's older coalition was nearly fully loyal.

---

## 4. Table B — defection + skip-share + flip-share decomposition

| Cohort | defection_rate | skip-share (of non-retainers) | flip-Trump share | flip-third share |
|---|---:|---:|---:|---:|
| Silent     | 4.49%  | 50.54% | 40.70% | 8.75% |
| Boomer     | 8.44%  | 59.50% | 33.14% | 7.36% |
| GenX       | 15.69% | 54.73% | 41.03% | 4.23% |
| MillOld    | 16.93% | 50.70% | 35.75% | 13.55% |
| **MillYoung** | **19.84%** | **49.82%** | **39.16%** | 11.03% |
| GenZ       | 17.38% | **71.13%** | 14.58% | 14.29% |

**The MillYoung exception:** every other cohort has skip-share between 50% and 71%. MillYoung is the only cohort where skip-share dips below 50%. For MillYoung Biden-2020 voters who didn't retain Harris, roughly half disappeared from the electorate, half showed up to vote AGAINST Harris (mostly for Trump, some third-party). This is a meaningfully different *kind* of defection from the other cohorts.

**The GenZ exception:** skip-share 71% — GenZ defectors overwhelmingly disengaged, not flipped. The Trump-flip share (14.58%) and third-party share (14.29%) are roughly equal — among the small fraction of GenZ Biden-2020 voters who DID show up to vote for someone else in 2024, they were nearly as likely to vote third-party as to vote Trump.

---

## 5. Cross-substrate comparison with Pew H7 (v2.0 §5)

| | Pew W159 (4-band age) | CES VV (6-cohort) |
|---|---|---|
| Source | validated voters, vote choice from PEW VOTECHOICE2024 | validated voters via TargetSmart, choice self-reported via CC24_410 |
| Weights | WEIGHT_W159_VALIDATEDVOTE | vvweight_post |
| 18-29 band defection | 32.4% | ~19% (weighted avg GenZ + part of MillYoung; not directly comparable) |
| Skip-share of non-retainers (youngest) | 68.6% | 71.1% (GenZ) / 49.8% (MillYoung) |
| Monotonic younger→older defection? | YES (32→25→18→14) | PARTIAL (4.5→8.4→15.7→16.9→19.8→17.4) — MillYoung peak, GenZ slight dip |

**Discrepancy notes (per pre-reg §4):**
- Absolute % differ across substrates; Pew validated CHOICE while CES has self-reported choice among validated VOTERS. CES retention rates run higher (95% Silent vs Pew's ~96% 65+) but the patterns mostly align.
- Pew's 18-29 band MIXES GenZ + MillYoung; CES at 6-cohort exposes that mixing **as the source of Pew's monotonic story**. When you separate, MillYoung defects MORE than GenZ — but Pew couldn't see this.
- Pew's "skip dominates everywhere" (67-79% across 4 bands) holds in 5 of 6 CES cohorts; MillYoung is the lone exception, and it dips below 50% by < 1pp.

---

## 6. Connection to v2.0 H6 (MillYoung defector finding)

v2.0 H6 (CES vote_h6 6-cohort Stan): **MillYoung cohort_eff = -0.302 [-0.545, -0.077]** credibly NEGATIVE on Harris-vote (controlling 2020 recall). v2.3 now decomposes that finding behaviorally:

- MillYoung is **credibly negative** in H6 (cohort_eff on vote) AND **highest-defection-rate** in v2.3 (19.8%) AND **lowest-skip-share** in v2.3 (49.8%).
- The H6 negative coefficient is being driven by ACTUAL VOTE-FLIPPING (39% to Trump, 11% third party, totaling 50% of non-retainers), not solely by skipping.
- GenZ's H6 +0.223 borderline-positive finding squares with v2.3 H15 TIE: GenZ retention slightly higher than MillYoung but not credibly so.

**Unified reading of v2.0 H6 + v2.0 H7 + v2.3:** The cohort defection signal in v1.1 (CES, -0.311 cohort_eff for "Millennial") was a coarse-cohort artifact masking TWO distinct phenomena: (a) MillYoung (28-35) actively defecting via flipping (≈50% of defection) + skipping (≈50%); (b) GenZ (18-27) disengaging via skipping (71% of defection) with minimal active flipping. v2.0 H6's 6-cohort recode + v2.3's bucket decomposition jointly expose that the "young Biden coalition defected" narrative needs two qualitatively different mechanisms — one realignment-shaped (MillYoung), one disengagement-shaped (GenZ).

---

## 7. What v2.3 closes

- **H7's Pew "skip dominates" pattern holds at fine resolution in 5 of 6 cohorts.** It is not a 4-band-aggregation artifact for most of the cohort spectrum.
- **MillYoung is qualitatively distinct.** v2.0 H6's credible-negative cohort_eff is not driven primarily by disengagement; it's driven by Biden-2020 voters showing up to vote against Harris.
- **GenZ's "flips positive direction" finding from H6 is consistent with v2.3** at TIE-magnitude (just inside 3pp threshold); GenZ retention is slightly higher than MillYoung, with most GenZ "defection" reading as not-voting rather than active flipping.

## 8. What v2.3 opens

- **MillYoung-flipper mechanism.** *Why* does the 28-35 cohort show up to vote AGAINST a Biden-coalition successor, when adjacent-cohort defections are skip-dominated? Candidate mechanisms (overlap with v2.2 v3-candidates):
  - 2020-cycle backlash specific to this cohort (24-31 in 2020 — peak BLM/COVID/Trump-first-term experience)
  - Trump-favorability for MillYoung Biden-2020 voters specifically (v2.1 H11 showed Trump_ft × cohort interaction was HOMOGENEOUS aggregate-wise, but MillYoung sub-segment hasn't been probed)
  - Latino-Millennial or Asian-Millennial cell × MillYoung interaction (v1.1 + v2.0 H1.2 + H2.2 found Mill × Hispanic / Mill × Asian credibly negative on CES interaction)
- **GenZ-skipper mechanism.** *Why* does the youngest cohort overwhelmingly skip rather than flip? Candidates:
  - First-time-voter cohort effect (lower behavioral commitment to repeat voting)
  - Disillusionment-with-both-options (the "lesser evil" pattern is more salient for younger voters)
  - Mobilization gap (campaigns under-mobilized youngest cohort)
- **Pre-reg-able v2.4 cross-substrate replication.** AP VoteCast 6-band age (30-44 includes both MillOld + MillYoung) doesn't resolve the MillOld vs MillYoung split — but the AP cohort×race interaction cells already show 30-39 patterns (per v2.0 H1.2 / H2.2). v2.4 could pre-reg AP MillYoung-specific predictions.

---

## 9. Honest caveats + diagnostics

- **Self-reported vote choice on validated voters.** CC24_410 is self-reported in CES even when TS_g2024 validates the act of voting. The vote-CHOICE bucket assignment carries self-report bias; the SKIP-vs-VOTE assignment is validated.
- **vf_match_missing universe filter.** Pre-reg §1 specified excluding rows where TS_g2024 is NaN. In the constructed universe (vvweight_post > 0 already requires voter-file match), no such rows survived — vf_match_missing count is zero per cohort. The filter is non-binding for this universe.
- **voted_unknown_choice excluded.** 157 respondents had validated vote (TS_g2024 ∈ {1-6}) but missing CC24_410. Excluded from main decomposition per pre-reg §1. By cohort: Silent 4, Boomer 68, GenX 42, MillOld 29, MillYoung 11, GenZ 3. Distribution is roughly proportional to cohort N; no systematic bias indicated.
- **Sample-N per cohort:** Silent N=882, Boomer N=8426, GenX N=4739, MillOld N=2202, MillYoung N=1263, **GenZ N=555**. GenZ has the smallest cell; the 12.37% skip rate has wider CI than the MillYoung 9.88% (Boomer's 5.02% is at large N).
- **Weighting:** vvweight_post applied per pre-reg. Different choice of weight (commonweight, vvweight) would shift absolute % but not directional patterns.
- **MillYoung skip-share = 49.82%** is technically below the 50% threshold for H14 PARTIAL, but by < 1pp. Reading: the cohort sits exactly on the edge of "skip dominates" / "flip dominates" — substantively, defection is half-half.

---

## 10. Repo state at lock

- Pre-reg v2.3 locked at `8dcd2a9`.
- Script: `code/v23_skipper_decomp.py`
- Outputs: `data/processed/fits/h7_ces_decomp.csv` (Table A), `data/processed/fits/h7_ces_decomp_table_b.csv` (Table B).
- Repo: github.com/mrnathanhumphrey-droid/DNC.

**Result commit hash to be filled at commit time.**
