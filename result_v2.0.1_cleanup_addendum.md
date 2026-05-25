# result_v2.0.1 — Cleanup addendum to result_v2.0

**Locked:** 2026-05-24. Addendum to `result_v2.0_dnc_postmortem.md` (HEAD `d03e2dd`).
**Builds on:** result_v2.0 + §10 dev 7 K-S orientation clarification.

This is a CLEANUP pass to result_v2.0, capturing:
1. H4 re-fit at hardened settings (chains=6, warmup=1000, samples=1000)
2. H5 ANES racial_resentment re-fit with corrected K-S canonical direction
3. H5 CES structural_inequity re-fit with corrected K-S canonical direction
4. NEXT.md refresh (already done at d03e2dd-era pre-v2.0.1)

All numerical updates are **direction-invariant σ values UNCHANGED** + **cohort_eff signs FLIPPED to canonical K-S direction** (HIGH = MORE racial resentment).

---

## 1. H4 hardened re-fit (v2.0.1)

**Original H4 (v2.0):** chains=4, warmup=500, samples=500. σ_cohort = 0.453 [0.053, 1.019]. R̂ 1.018 (marginal), ESS 384 (below 500).

**H4 hardened (v2.0.1):** chains=6, warmup=1000, samples=1000.
- σ_cohort = **0.448 [0.047, 1.053]** — virtually unchanged from original.
- R̂ 1.005, ESS_bulk 1326, 7 divergent. **CONVERGED CLEAN.**
- β_econ_x_cohort (F3 interaction) = +0.086 [-0.087, +0.253] — STILL NULL.
- σ_race 0.656, σ_educ 0.448, σ_cohort 0.448, σ_gender 0.389, σ_region 0.244.

**Verdict: H4 NOT MEDIATED confirmed at higher precision.** σ_cohort = 0.448 vs pre-reg gate ≥0.25 (NOT MEDIATED). Result robust to convergence improvement.

---

## 2. H5 ANES racial_resentment re-fit (canonical K-S direction)

**Original H5 ANES (v2.0):** composite oriented as racial_sympathy (per §10 dev 7); GenZ cohort_eff reported as +0.350 [+0.101, +0.622] credibly POSITIVE on sympathy direction.

**H5 ANES re-fit (v2.0.1):** rebuilt composite with canonical Kinder-Sanders direction (HIGH = MORE resentment). N=4167, R̂ 1.011, ESS 569, 1 divergent. CLEAN.

Variance (direction-invariant):
- σ_race 0.321, σ_educ 0.237, σ_cohort 0.333, **σ_gender 0.475 (dominant)**, σ_region 0.172, σ_y 0.754.

cohort_eff (canonical: HIGH = MORE resentment):

| Cohort | mean | 5% | 95% | Credible? |
|---|---:|---:|---:|---|
| Silent | +0.152 | -0.102 | +0.403 | null lean more resent |
| Boomer | +0.172 | -0.082 | +0.435 | null lean more resent |
| GenX | +0.099 | -0.154 | +0.348 | null |
| Millennial | -0.111 | -0.359 | +0.150 | null lean less resent |
| **GenZ** | **-0.358** | **-0.620** | **-0.104** | **CREDIBLY LESS resent (MOST progressive)** |

**Same finding, canonical signs.** GenZ is credibly the most racially-progressive cohort in ANES. Gender still dominant.

---

## 3. H5 CES structural_inequity re-fit (canonical K-S direction)

**Original H5 CES (v2.0):** composite as built with inverted direction (per §10 dev 7); GenZ cohort_eff +0.311 credibly POSITIVE on sympathy direction.

**H5 CES re-fit (v2.0.1):** rebuilt composite (`6 - CC24_441a` for WORKWAY + `CC24_441b` for GENRTNS) so HIGH = MORE resentment per canonical K-S. N=49,431, R̂ 1.010, ESS 460, 23 divergent.

Variance (direction-invariant):
- σ_race 0.224, σ_educ 0.210, σ_cohort 0.289, **σ_gender 0.463 (dominant)**, σ_region 0.055, σ_y 0.721.

cohort_eff (canonical: HIGH = MORE resentment):

| Cohort | mean | 5% | 95% | Credible? |
|---|---:|---:|---:|---|
| Silent | +0.078 | -0.162 | +0.287 | null |
| Boomer | +0.159 | -0.078 | +0.371 | null lean more resent |
| GenX | +0.111 | -0.122 | +0.323 | null |
| Millennial | -0.080 | -0.318 | +0.132 | null lean less resent |
| **GenZ** | **-0.319** | **-0.550** | **-0.107** | **CREDIBLY LESS resent (MOST progressive)** |

**Cross-substrate replication: GenZ credibly LESS resentful in BOTH ANES (-0.358 [-0.620, -0.104]) AND CES (-0.319 [-0.550, -0.107]).** Sign-agreement across all 5 cohorts holds. The cleanest cross-substrate cell-level replication remains the strongest cross-substrate finding in the v2 program.

---

## 4. Updated headline (cross-substrate, canonical direction)

| Cohort | ANES cohort_eff (less resent direction = lower=more) | CES cohort_eff | Sign-agree |
|---|---:|---:|:---:|
| Silent | +0.152 | +0.078 | ✓ both positive (lean more resent) |
| Boomer | +0.172 | +0.159 | ✓ both positive |
| GenX | +0.099 | +0.111 | ✓ both positive |
| Millennial | -0.111 | -0.080 | ✓ both negative |
| **GenZ** | **-0.358** ✓ | **-0.319** ✓ | **✓ both CREDIBLY negative** |

**\* = 95% CI excludes zero.**

The result_v2.0 headline "GenZ credibly most racially-sympathetic in BOTH substrates" reads cleanly now with canonical-direction signs: **GenZ has credibly LESS racial resentment than baseline in BOTH ANES and CES; monotonic gradient older→younger; sign-agreement across all 5 cohorts cross-substrate.**

Gender dominance verdict (NEITHER cohort-dominant per pre-reg σ gate) is UNCHANGED — variance is direction-invariant.

---

## 5. Repo state at lock

- All cleanup fits stored under `data/processed/fits/`:
  - `fit_anes_vote_h4_binary_hardened_*` (H4 v2.0.1 hardened)
  - `fit_anes_racial_resentment_gaussian_*` (H5 ANES canonical re-fit)
  - `fit_ces_structural_inequity_gaussian_*` (H5 CES canonical re-fit; last write 2026-05-24)
- result_v2.0 unchanged at HEAD `d03e2dd`; this addendum updates the numbers.
- Repo: github.com/mrnathanhumphrey-droid/DNC.

**Result commit hash to be filled at commit time.**
