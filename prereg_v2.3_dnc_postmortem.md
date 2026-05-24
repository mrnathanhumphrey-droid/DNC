# Pre-registration v2.3 — DNC 2024 Post-Mortem (Skipper decomposition at fine cohort cuts, CES VV)

**Locks BEFORE running v2.3 cross-tabs.** Builds on:
- result_v1.1 (HEAD `122fc8c`): cohort × race interaction findings.
- result_v2.0 (HEAD `d03e2dd`): Pew H7 turnout-vs-choice (4-band age) — defection rate monotonic 32% (18-29) → 14% (65+); 67-79% of non-retainers SKIPPED in 2024 (Pew validated voters).
- result_v2.0 H6: CES vote_h6 6-cohort split — MillYoung (28-35) cohort_eff = -0.302 [-0.545, -0.077] CREDIBLY NEGATIVE; GenZ +0.223 borderline positive (opposite direction).
- result_v2.1 + v2.2: cohort signal is MECHANISM RESIDUAL to ANES attitudinal battery + LASSO multi-mediator combination.

**Motivation.** v2.0 H7 (Pew, 4-band age) and v2.0 H6 (CES, 6-cohort vote) point in the same direction but at different resolutions and on different outcomes. CES has both continuous birthyr AND validated voter-file records (TargetSmart TS_g2024). v2.3 unifies the H6 + H7 findings at fine cohort resolution: among Biden-2020 voters, what fraction of each cohort SKIPPED vs FLIPPED-Trump vs FLIPPED-Third vs RETAINED-Harris in 2024?

Per user framing 2026-05-24: *"keep going with open threads."* Thread #5 from result_v2.0 §9 (skipper decomposition).

---

## 0. What this pre-reg LOCKS

- 3 v2.3 hypotheses (H13-H15) with falsification gates
- CES VV universe definition
- Cohort coding (6-level, matches v2.0 H6)
- Validated-vote bucket definitions
- Reporting format

**What this pre-reg does NOT lock:**
- Cross-substrate replication (CES + Pew only; ANES has weaker validation)
- Causal interpretation
- Mechanism-for-skipping (descriptive decomposition only)

---

## 1. v2.3 Hypotheses (LOCKED)

### Bucket definitions

For each respondent in the universe (defined §2), compute 2024 outcome bucket:

| Bucket | Definition |
|---|---|
| **retained_harris** | TS_g2024 ∈ {1, 2, 3, 4, 5, 6} (validated voted) AND CC24_410 == 1 (self-reported Harris) |
| **flipped_trump**   | TS_g2024 ∈ {1, 2, 3, 4, 5, 6} AND CC24_410 == 2 (self-reported Trump) |
| **flipped_third**   | TS_g2024 ∈ {1, 2, 3, 4, 5, 6} AND CC24_410 ∈ {3, 4, 5, 8} (third party / other) |
| **skipped**         | TS_g2024 == 7 (validated non-voter) |
| **voted_unknown_choice** | TS_g2024 ∈ {1-6} BUT CC24_410 is missing (validated voted, didn't tell us who) — REPORTED separately, not in main decomposition |
| **vf_match_missing**     | TS_g2024 is NaN (no voter file match) — EXCLUDED from skip/vote outcomes; reported separately |

### Cohort coding (6-level, matches v2.0 H6 §3.4)

- Silent: birthyr ≤ 1945
- Boomer: 1946-1964
- GenX: 1965-1980
- MillOld: 1981-1988 (ages 36-43 in 2024)
- MillYoung: 1989-1996 (ages 28-35 in 2024)
- GenZ: 1997+ (ages 18-27 in 2024)

### H13 — Cohort gradient of defection (CONFIRMATORY of H7 at fine resolution)

**Prior:** Pew H7 (4-band age) found defection rate monotonic 32% → 14% from 18-29 to 65+ band among Biden-2020 voters.

**Test:** Compute defection rate = 1 - (retained_harris / total_in_4_main_buckets) per CES cohort (using vvweight_post weighting).

**Falsification gates:**
- **CONFIRMED:** defection rate is monotonically non-increasing from MillYoung/GenZ → Silent (older cohorts at most as defective as younger).
- **PARTIAL:** monotonic with at most 1 inversion (any pair of adjacent cohorts where the older has higher defection by ≤ 3 percentage points).
- **REFUTED:** non-monotonic with ≥ 1 inversion >3pp, OR older cohorts more defective than MillYoung.

### H14 — Defection-is-mostly-skipping at fine cohort cuts (CONFIRMATORY of H7 mechanism)

**Prior:** Pew H7 found 67-79% of non-retainers SKIPPED across all 4 age bands; only 16-25% flipped to Trump.

**Test:** For each cohort, compute skip_share = skipped / (skipped + flipped_trump + flipped_third) — i.e., among non-retainers, what fraction skipped vs flipped.

**Falsification gates:**
- **CONFIRMED:** skip_share ≥ 0.50 for ALL 6 cohorts (matching Pew "skip dominates flip" pattern across the cohort spectrum).
- **PARTIAL:** skip_share ≥ 0.50 for ≥ 4 of 6 cohorts.
- **REFUTED:** skip_share < 0.50 for the majority of cohorts (defection is mostly flipping, not skipping — would contradict Pew H7).

### H15 — GenZ Biden-coalition loyalty (CONFIRMATORY of H6 GenZ-positive direction)

**Prior:** Pre-reg v2.0 H6 found CES vote_h6 GenZ cohort_eff = +0.223 (borderline positive) — opposite direction from MillYoung's credibly-negative -0.302. Reading: GenZ Biden-2020 voters were MORE retentive of Harris than MillYoung Biden-2020 voters.

**Test:** Compare retention_rate(GenZ) vs retention_rate(MillYoung) on CES VV.

**Falsification gates:**
- **CONFIRMED:** retention_rate(GenZ) > retention_rate(MillYoung) by ≥ 3 percentage points.
- **TIE:** difference < 3 percentage points either direction.
- **REFUTED:** retention_rate(GenZ) < retention_rate(MillYoung) by ≥ 3 percentage points (GenZ Biden coalition was LESS retentive than MillYoung — contradicts H6).

---

## 2. Universe + sample definition

- **Substrate:** CES 2024 Common Content + VV file (D:/DNC/data/raw/ces_2024/CCES24_Common_OUTPUT_vv_topost_final.csv).
- **Filter:**
  - vvweight_post > 0 AND vvweight_post not NaN (matched to voter file + completed post-election wave)
  - presvote20post == 1 (self-reported Biden 2020)
  - valid birthyr (1900 ≤ birthyr ≤ 2010 for cohort assignment)
  - TS_g2024 not NaN (voter-file match — exclude unmatched per pre-reg §6 "vf_match_missing" definition)
- **Weights:** vvweight_post (CES validated-voter post-election weight)
- **Reported N:** unweighted + weighted total per cohort, both reported.

---

## 3. Reporting format (LOCKED)

Two tables saved to `data/processed/fits/h7_ces_decomp.csv` + reported in result:

### Table A — per-cohort 4-bucket decomposition (weighted %)

| Cohort | retained_harris | flipped_trump | flipped_third | skipped | weighted_N | unweighted_N |
|---|---|---|---|---|---|---|
| Silent | ... | ... | ... | ... | ... | ... |
| Boomer | ... | ... | ... | ... | ... | ... |
| GenX | ... | ... | ... | ... | ... | ... |
| MillOld | ... | ... | ... | ... | ... | ... |
| MillYoung | ... | ... | ... | ... | ... | ... |
| GenZ | ... | ... | ... | ... | ... | ... |

### Table B — defection + skip-share + flip-share decomposition

| Cohort | defection_rate | skip_share (of non-retainers) | flip_trump_share | flip_third_share |
|---|---|---|---|---|

### Side-table — voted_unknown_choice + vf_match_missing counts

Per pre-reg §1 bucket definitions, these excluded categories are reported by N (and as % of Biden-2020 universe) so the reader sees what was filtered.

---

## 4. Threats to validity

- **Bucket assignment uncertainty:** TS_g2024 == 6 ("voted by unknown method") is a validated vote but with unknown method; treated as voted (consistent with §1 bucket definition).
- **CC24_410 self-report bias among validated voters:** social-desirability could push reported choice toward winner; this is a known CES limitation. Reading: directional patterns across cohorts are more reliable than absolute %.
- **Voter-file match rate by cohort:** if younger cohorts (GenZ, MillYoung) are less likely to have voter-file matches (recent moves, less voter file history), the vf_match_missing exclusion could bias toward older cohorts being more validated. Report match rate per cohort as transparency check.
- **Weighting choice:** vvweight_post is post-election validated weight. Pew H7 used WEIGHT_W159_VALIDATEDVOTE. Different weighting → not directly cross-comparable %; the cross-substrate comparison is directional.

---

## 5. Verdicts

Each of H13/H14/H15 reported as CONFIRMED / PARTIAL / TIE / REFUTED per §1 gates.

**Aggregate verdict:**
- **TURNOUT-MECHANISM CONFIRMED** if H13 + H14 both CONFIRMED.
- **MECHANISM PARTIAL** if at least 1 CONFIRMED + 0 REFUTED.
- **PEW H7 NOT REPLICATED** if H13 or H14 REFUTED.
- **H6 GENZ-DIRECTION REPLICATED** if H15 CONFIRMED.

---

## 6. v2.3 deviation log

| Date | Deviation | Rationale |
|---|---|---|

(Empty at lock; populated as v2.3 work surfaces discrepancies.)

---

**Locked at commit:** `[fill at commit]` on `main`.
**Repository:** https://github.com/mrnathanhumphrey-droid/DNC.
**Builds on:** result_v2.0 H6 + H7 (HEAD d03e2dd); result_v2.1 (27a0093); result_v2.2 (e441cbd).
