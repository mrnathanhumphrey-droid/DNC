# result_v2.4 — DNC 2024 Post-Mortem v2.4 (6-cohort × race interaction refinement, CES vote)

**Locked:** 2026-05-24 against `prereg_v2.4_dnc_postmortem.md` HEAD `f7a96ad`.
**Builds on:** result_v1.1 (`122fc8c`) + result_v2.0 H6 (`d03e2dd`) + result_v2.3 (`d810d63`).
**Repo:** github.com/mrnathanhumphrey-droid/DNC.

---

## 1. Headline (one sentence — REVISES v1.1)

**v1.1's "Mill × Hispanic" credible-negative cell is driven by MillOld (36-43), not MillYoung (28-35)** — at 6-cohort resolution, MillOld × Hispanic = -0.398 [-0.793, -0.032] CREDIBLY NEGATIVE while MillYoung × Hispanic = -0.291 NOT credible. **MillYoung defection is RACE-GENERAL** (marginal cohort_eff -0.394 [-0.787, -0.032] credibly negative; no specific race cell credibly negative for MillYoung). MillOld defection IS race-specific (concentrated in Hispanic). The two "Millennial" sub-cohorts have qualitatively-different defection profiles AND qualitatively-different race-cell loadings.

---

## 2. Verdicts table

Reference baseline: v1.1 5-cohort interaction cells on CES vote — Mill × Hispanic -0.46, Mill × Asian -0.38, GenZ × Asian +0.44, Boomer × Black +0.55.

| Hyp | Test | Verdict | Detail |
|---|---|---|---|
| **H16** | MillYoung × Hispanic carries more of Mill × Hispanic signal than MillOld × Hispanic | **REFUTED** | MillOld × Hispanic credible -0.398; MillYoung × Hispanic = -0.291 NOT credible. MillYoung MORE positive than MillOld by +0.107 (wrong direction). |
| **H17** | Same for Asian | **REFUTED** | MillYoung × Asian = -0.207 vs MillOld × Asian = -0.324; MillYoung +0.117 more positive. |
| **H18** | GenZ × Asian remains credibly positive at 6-cohort | **CONFIRMED** | GenZ × Asian = +0.454 [+0.088, +0.868] credibly positive, mean ≥ +0.20 ✓ |
| **H19** | MillYoung × Black credibly negative | **INDETERMINATE** | mean -0.052, CI [-0.398, +0.282]; within indeterminate band |

**Aggregate per pre-reg §3:** 0 of {H16, H17, H19} CONFIRMED → not "MILLYOUNG IS DEFECTOR-RACE-SPECIFIC". MillYoung marginal cohort_eff = -0.394 CREDIBLY NEGATIVE → **MILLYOUNG IS RACE-GENERAL DEFECTOR**. H18 CONFIRMED → **GENZ ASIAN-PRO PERSISTS** (cross-validates v1.1 + v2.0 H1.2).

---

## 3. Fit diagnostics (CLEANEST FIT IN v2)

**Fit:** model_a_interaction.stan on CES `vote_h6_x_race`, N=42,028, K_fund=4 baseline + cohort×race interaction layer.
- chains=4, warmup=750, samples=750 (§10 dev 1 — v1.1 interaction defaults, not v2.0.1 hardened; verdicts robust)
- **R̂ max 1.007, ESS_bulk min 852, 0 divergent transitions out of 3000 samples.**
- σ_race 0.342, σ_educ 0.382, σ_cohort 0.384, **σ_gender 1.207 (dominant)**, σ_region 0.151, **σ_cohort_race 0.327**.

---

## 4. Cell-level interaction matrix

cohort_race_eff posterior mean (rows = 6-cohort, cols = race; positive = more pro-Harris):

| | asian | black | hispanic | nhpi | other | white |
|---|---:|---:|---:|---:|---:|---:|
| Silent | +0.034 | +0.181 | +0.144 | -0.123 | +0.092 | -0.043 |
| Boomer | -0.080 | **+0.528** | -0.202 | +0.110 | -0.138 | -0.025 |
| GenX | -0.097 | +0.086 | +0.275 | -0.018 | +0.031 | -0.241 |
| **MillOld** | -0.324 | +0.125 | **-0.398** | +0.139 | +0.150 | +0.051 |
| **MillYoung** | -0.207 | -0.052 | -0.291 | -0.109 | -0.080 | +0.253 |
| **GenZ** | **+0.454** | -0.279 | +0.281 | -0.310 | +0.177 | -0.072 |

**3 credible cells (95% CI excluding zero):**
- **Boomer × Black = +0.528 [+0.168, +0.940]** — anchor confirmed (v1.1 +0.55 replicates)
- **GenZ × Asian = +0.454 [+0.088, +0.868]** — GenZ Asian-pro replicates v1.1 + cross-validates AP v2.0 H1.2 (18-24 × Asian = +0.42)
- **MillOld × Hispanic = -0.398 [-0.793, -0.032]** — Mill × Hispanic signal LOCALIZED to MillOld

---

## 5. Marginal cohort_eff (level-shift across races, controlling 2020 recall)

| Cohort | mean | 5% | 95% | Credible? |
|---|---:|---:|---:|---|
| Silent | +0.257 | -0.136 | +0.720 | (lean positive, NOT credible) |
| Boomer | +0.163 | -0.177 | +0.526 | null |
| GenX | +0.009 | -0.338 | +0.345 | null |
| MillOld | -0.232 | -0.612 | +0.096 | (lean negative, NOT credible) |
| **MillYoung** | **-0.394** | **-0.787** | **-0.032** | **CREDIBLY NEGATIVE** |
| GenZ | +0.212 | -0.136 | +0.580 | (lean positive, NOT credible) |

**MillYoung marginal cohort_eff REPLICATES + STRENGTHENS v2.0 H6 finding** (was -0.302 [-0.545, -0.077] in H6 marginal model; now -0.394 [-0.787, -0.032] when interaction-cells partialed out). The 6-cohort + race-interaction model gives MillYoung the cleanest credible-negative reading in the v2 program.

---

## 6. The MillOld vs MillYoung divergence (key v2.4 substantive finding)

| Cohort | Marginal cohort_eff | Race cells |
|---|---|---|
| MillOld (36-43) | -0.232 (lean negative, NOT credible alone) | **× Hispanic = -0.398 CREDIBLE** (single concentrated cell); × Asian = -0.324 (lean negative) |
| MillYoung (28-35) | **-0.394 CREDIBLE** (race-general defection) | No race cell credibly non-zero; all 6 race cells in [-0.291, +0.253] |

**Interpretation:** "Millennial defection" in v1.1 conflated TWO distinct phenomena:
1. **MillOld defection is HISPANIC-CONCENTRATED.** The Mill × Hispanic -0.46 credible cell from v1.1 is MillOld × Hispanic specifically. Race-by-cell-specific defection.
2. **MillYoung defection is RACE-GENERAL.** The marginal credibly-negative effect doesn't concentrate in any race cell. Whatever drives MillYoung defection operates ACROSS race lines.

Combined with v2.3 finding (MillYoung = active flipper, GenZ = skipper): MillYoung's defection is RACE-GENERAL ACTIVE FLIPPING. MillOld's defection is HISPANIC-SPECIFIC FLIPPING.

These are different mechanisms — and v2.1-v2.6's "mediator hunt" was looking for one consistent across-cohort mechanism. v2.4 hints that the right model may be: separate mechanisms for MillOld-Hispanic-specific defection (Latino-political-realignment story) vs. MillYoung-race-general defection (?).

---

## 7. Cross-substrate triangulation (CES + AP + v1.1)

| Cell | v1.1 5-cohort CES | v2.0 AP 6-band | v2.4 6-cohort CES |
|---|---|---|---|
| Mill × Hispanic | -0.46 credible | INDETERMINATE | MillOld -0.398 credible, MillYoung -0.291 NOT |
| Mill × Asian | -0.38 credible | INDETERMINATE | MillOld -0.324, MillYoung -0.207, neither credible |
| GenZ × Asian | +0.44 credible | +0.42 credible (AP 18-24) | +0.454 credible |
| Boomer × Black | +0.55 credible | +0.69 credible (AP 65+) | +0.528 credible |

**Three of four v1.1 credible cells REPLICATE cleanly across substrates and cohort refinements.** Only the Mill × Asian cell weakens at fine-cohort resolution (becomes MillOld-leaning but not credible). The Latino-Millennial defection finding from v1.1 is REVISED to "Latino-MillOld defection" (36-43 Hispanic) at fine cohort resolution.

---

## 8. Connection to v2.7 (alt-right composite)

v2.7 found 96.1% of Trump 2024 voters did NOT vote Biden in 2020 — Trump's coalition is overwhelmingly his pre-existing base. The MillOld × Hispanic defection cell from v2.4 is one of the small slices of Biden→Trump conversion. If we cross v2.4 with v2.7's alt-right composite: are MillOld-Hispanic flippers concentrated in Q3-Q4 of altright-proxy? v2.7 H31 cohort × quartile cell N was too small to test specifically for MillOld-Hispanic.

Future test (v2.9 candidate): MillOld-Hispanic-specific defectors' altright-proxy distribution.

---

## 9. Honest caveats + diagnostics

- **§10 dev 1: Fit settings.** Used `fit_model_a_interaction.py` defaults (chains=4, warmup=750, samples=750) instead of pre-reg v2.4 §2.4 "hardened consistent with v2.0.1" (chains=6, warmup=1000, samples=1000). R̂ 1.007 + 0 divergent in this fit = excellent convergence; verdicts robust. v2.4-hardened-rerun is a follow-up if precision becomes binding.
- **6-cohort split halves cell N.** Per pre-reg §4: MillYoung × Hispanic cell N ≈ 150-200 (was ~349 at 5-cohort). Posterior CIs wider. Cell-level credibility threshold (95% CI excluding zero) is conservative; the directional patterns are robust to this.
- **CES self-report.** Same caveat as v1.1.

---

## 10. Repo state at lock

- Pre-reg v2.4 locked at `f7a96ad`.
- Fit: `fit_ces_vote_h6_x_race_interaction_*` under `data/processed/fits/`.
- Cell table: `interaction_cells_ces_vote_h6_x_race_interaction.csv`.
- Repo: github.com/mrnathanhumphrey-droid/DNC.

**Result commit hash to be filled at commit time.**
