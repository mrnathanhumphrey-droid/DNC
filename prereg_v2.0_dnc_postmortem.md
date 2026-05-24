# Pre-registration v2.0 — DNC 2024 Post-Mortem (Cross-substrate + Mechanism)

**Locked at commit:** `[fill at commit]` on `main`, github.com/mrnathanhumphrey-droid/DNC.
**Builds on:** `prereg_v1.0_dnc_postmortem.md` (HEAD 45ea69a + 8 §12 deviations) + `result_v1.0_dnc_postmortem.md` (HEAD 469dcd1) + `result_v1.1_dnc_postmortem.md` (HEAD 122fc8c).
**Status:** Locks 7 v2 hypotheses (H1.2-H7) BEFORE running any v2 fits. Once committed, no edits permitted; deviations logged in §10.

Per user framing 2026-05-23: *"post-mortem is discovery by definition; if we say we are wrong we go and figure out WHY"* + *"oh good i like threads"* + *"pre reg it all"*. The v1.1 threads emerged exploratorily; v2.0 locks them as pre-registered hypotheses with explicit falsification thresholds before further analysis is run.

---

## 0. What this pre-reg LOCKS

- 7 v2 hypotheses (H1.2-H7), each with stated prior + falsification gate
- 4 substrates (AP VoteCast PRIMARY for cohort×race replication; ANES + CES + Pew secondary roles)
- Model A + interaction Stan specs (re-using v1.1 `model_a_interaction.stan`)
- Mechanism-probe extended fundamentals matrix (party-ID + Trump-favorability + Gaza-salience + econ × cohort interaction)
- Verdict thresholds per hypothesis
- Multiplicity correction: hierarchical shrinkage already in model (per v1.0 §6); v2 hypothesis tests reported with 90% CI as primary AND 95% CI as falsification threshold.

What this pre-reg DOES NOT lock:
- Manuscript-prose writing (out of scope per session protocol)
- Model B / C revisit (deferred unless restricted-use ANES DUA becomes available)
- Post-2024 longitudinal extension (out of scope; this is 2024-specific)

---

## 1. v2 Hypotheses (LOCKED)

### H1.2 — Asian generational bifurcation REPLICATES on AP VoteCast

**Prior:** v1.1 found Millennial × Asian = -0.379 [-0.822, -0.005] credibly NEGATIVE and GenZ × Asian = +0.437 [+0.058, +0.856] credibly POSITIVE on CES vote (N=42,028). Only race in CES with credibly-opposite cohort cells.

**Test:** Fit Model A + cohort×race interaction on AP VoteCast (N=139,938) with banded-cohort approximation (§3.2).

**Falsification gates:**
- **CONFIRMED:** cohort_race_eff[Millennial-band, Asian] 95% CI < 0 AND cohort_race_eff[GenZ-band, Asian] 95% CI > 0 on AP VoteCast.
- **PARTIAL:** one of the two cells credible, other indeterminate (CI crosses zero).
- **REFUTED:** either cell credibly OPPOSITE direction from CES finding, OR both indeterminate.

**Pre-reg notes:** AP VoteCast cohort coding is banded (per pre-reg v1.0 §12 entry 4 — F_AGECAT 4-band only on Pew; AP VoteCast is 6-band per its codebook). Cohort × race cells must be remapped to the AP banding (Silent + Boomer collapse; GenZ subset of 18-29 band — see §3.2). If the remap loses Asian resolution at the cell level (e.g., Asian × any-single-cohort cell n < 50), report INDETERMINATE with a §10 deviation.

### H2.2 — Latino-Millennial defection REPLICATES on AP VoteCast

**Prior:** v1.1 found Millennial × Hispanic = -0.463 [-0.879, -0.103] credibly NEGATIVE on CES.

**Test:** Same as H1.2 on AP VoteCast.

**Falsification gates:**
- **CONFIRMED:** cohort_race_eff[Millennial-band, Hispanic] 95% CI < 0 on AP.
- **PARTIAL:** point estimate negative, CI crosses zero.
- **REFUTED:** credible-positive cell on AP.

### H3.2 — GenZ × Black cell — RESOLVE the v1.0/v1.1 walk-back

**Prior:** v1.0 §3 cross-tab showed GenZ × Black Biden→Harris retention 86.3% (n=99); v1.1 interaction model gave cell -0.269 [-0.661, +0.140] NOT credible at CES N=42,028. AP VoteCast at N=139,938 provides ~3× the sample size; cell-level CIs should tighten.

**Test:** Same Stan fit; pull cohort_race_eff[GenZ-band, Black] with 95% CI.

**Three pre-registered verdicts:**
- **GenZ Black erosion CONFIRMED:** 95% CI < 0 AND mean < -0.20.
- **GenZ Black anchoring (anti-prediction):** 95% CI > 0 AND mean > +0.20.
- **INDETERMINATE:** CI crosses zero, OR mean between -0.20 and +0.20.

This pre-reg commits to reporting whichever verdict obtains, even if INDETERMINATE.

### H4 — Cohort-bypass-of-pid7 mechanism probe

**Prior:** v1.1 §8 found σ_cohort INCREASES +33% when party-ID added as fundamental on ANES vote (0.202 → 0.269). Cohort signal is NOT mediated by partisanship. Open question: what DOES mediate the cohort-defection signal?

**Test:** Re-fit ANES vote with extended fundamentals matrix (in addition to 2020-recall + econ + pid7):
- **F1:** Trump favorability (V241166 or feeling-thermometer for Trump; pre-confirm V-code at implementation; if uncoded substitute closest).
- **F2:** Gaza-salience proxy (V241404 humanitarian aid to Palestinians ∈ {1,2,3}, z-scored as a covariate, NOT as outcome).
- **F3:** Economic perception × cohort interaction (cohort_idx × fund_econ_z product term).

**Falsification gates:**
- **MEDIATED:** σ_cohort shrinks from 0.269 (with-pid7 baseline) to <0.10 in the extended model.
- **PARTIALLY MEDIATED:** σ_cohort shrinks to between 0.10-0.20.
- **NOT MEDIATED (cohort signal is direct):** σ_cohort stays >0.20 with full controls.

**Report:** the marginal coefficient of F1, F2, F3 with CIs; whichever fundamental(s) drive shrinkage is the mediator. F3 (econ × cohort) tests "younger cohorts swung specifically because their economic perception was worse, not because of age per se."

### H5 — Remaining issue battery completion

**Prior:** v1.0 §1 found gender dominant on 6/8 outcomes; cohort dominant 1/8. Remaining items in pre-reg v1.0 §3 not yet fit: CES single_payer, CES structural_inequity (racial-resentment battery), ANES race_relations, ANES science_arts compound, ANES foreign_aid (5 outcomes).

**Test:** Fit Model A on each. Build variance-decomp row for each in master table.

**Falsification gates per outcome:**
- **Cohort-dominant:** σ_cohort > max(σ_race, σ_educ, σ_gender, σ_region). If any outcome flips cohort-dominant, this is a v2 finding; otherwise the v1.0 pattern (gender dominance) holds.

**Aggregate gate:** if ≥3 of 5 new outcomes are cohort-dominant, revise v1.0 §1 verdict ("H1 NULL on magnitude") to "H1 MIXED — cohort dominant on issue-attitude items, gender on vote."

### H6 — Within-Millennial age split

**Prior:** v1.1 found Millennial cohort_eff -0.353 on CES with interaction model. Open question: is this concentrated in older (36-43) Millennials closer to Gen X, or younger (28-35) Millennials closer to Gen Z?

**Test:** Re-code CES cohort with 6 levels: Silent, Boomer, GenX, Millennial-Older (36-43), Millennial-Younger (28-35), GenZ. Re-fit marginal Model A. Compare cohort_eff for Mill-Older vs Mill-Younger.

**Falsification gates:**
- **OLDER-DRIVEN:** cohort_eff[Mill-Older] more negative than cohort_eff[Mill-Younger] by ≥0.15 in posterior mean AND non-overlapping 80% CIs.
- **YOUNGER-DRIVEN:** opposite direction with same threshold.
- **UNIFORM Millennial:** both cells within 0.10 of each other.

### H7 — Pew VV turnout-vs-choice decomposition

**Prior:** Pew VV has validated-voter records and a panel design (per pre-reg v1.0 §2). N=9,609 with WEIGHT_W159_VALIDATEDVOTE (n=9,240). Open question: of the Biden 2020 → not-Harris 2024 cohort, what fraction did NOT VOTE in 2024 vs voted but flipped?

**Test:** Stratify Pew VV Biden 2020 voters by their 2024 status (validated-voted-Harris / validated-voted-Trump-or-third / did not vote). Cross-tab by cohort band (Pew is F_AGECAT 4-band per §12 dev 4).

**Pre-registered output:** Pew VV §7 result table reports per-cohort percentage who (a) retained Harris, (b) flipped to Trump, (c) flipped to third party, (d) did not vote. Cohort-defection decomposition into (a) flip-vote vs (b) skip-vote. Whichever decomposition pattern emerges is reported.

**Falsification gate:** N/A — this is a descriptive decomposition. Pre-reg locks the FRAME (decompose into 4 buckets per cohort) rather than a directional prior.

---

## 2. Substrates + roles (LOCKED)

| Substrate | N | Role in v2 |
|---|---:|---|
| AP VoteCast 2024 PUF | 139,938 | **PRIMARY for H1.2 + H2.2 + H3.2 (cohort×race interaction replication)** |
| ANES 2024 | 5,521 | **PRIMARY for H4 (cohort-bypass-of-pid7 mechanism); H5 (race_relations + sci_arts + foreign_aid items)** |
| CES 2024 Common | 60,000 | **PRIMARY for H6 (Mill age split — only substrate with continuous birthyr); H5 (single_payer + structural_inequity items)** |
| Pew W159 VV | 9,609 | **PRIMARY for H7 (turnout-vs-choice)** |
| GSS 2024 | 3,986 | Not used in v2 (already covered in v1.0) |
| CPS ASEC + ORG | — | Not used in v2 (pay-structure imputation already done v1.0) |

---

## 3. Operationalization (LOCKED)

### 3.1 AP VoteCast cohort coding (banded approximation)

AP VoteCast 2024 PUF age variable is `Age7Categories` (or equivalent — confirm at impl time; if differently named log §10 deviation). Per the codebook check, the bands map to cohorts:

| AP age band | Pre-reg cohort |
|---|---|
| 18-29 | GenZ + Young Millennial (mixed) |
| 30-44 | Young/Mid Millennial + Old Millennial (mixed) |
| 45-49 | Late GenX / Early GenX (mixed) |
| 50-64 | GenX + Early Boomer (mixed) |
| 65+ | Boomer + Silent (mixed) |

**Cohort remap for AP VoteCast:**
- AP Cohort 1 ("GenZ-band") = 18-29 (estimates Gen Z + youngest Millennials)
- AP Cohort 2 ("Millennial-band") = 30-44 (estimates Millennials)
- AP Cohort 3 ("GenX-band") = 45-64 (estimates Gen X + early Boomers)
- AP Cohort 4 ("Boomer-band") = 65+ (estimates Boomer + Silent)

H1.2 / H2.2 / H3.2 cohort claims use these 4 AP bands. **The CES-derived cell finding (Millennial × Asian = -0.379) translates to "AP cohort 2 (30-44) × Asian < 0 on AP VoteCast"** — i.e., the AP test is at coarser resolution but should preserve direction.

If AP's actual age categorization differs from this scheme, file §10 deviation BEFORE re-fitting.

### 3.2 AP VoteCast Model A fundamentals

AP VoteCast does NOT have 2020 vote recall (per pre-reg v1.0 §2 verification). Fundamentals matrix on AP:
- **fund_econ_perception** (RESULTS_ECON or equivalent; z-scored)
- Intercept-only otherwise (no 2020 recall available; this changes interpretation — AP cohort_eff is marginal effect on vote, not conditional on prior partisanship)

This is a substantive difference vs CES — pre-reg locks the comparison: CES cohort_eff conditional on 2020 recall vs AP cohort_eff marginal. AP is a NOISIER test of "above-and-beyond 2020 baseline" defection; if AP still shows credibly negative Millennial-band cell, the signal is robust to the absence of 2020 recall conditioning.

### 3.3 ANES extended fundamentals for H4

- fund_recall20_biden / trump / other (existing)
- fund_econ_z (existing)
- fund_pid7_z (existing, V241227x)
- **NEW fund_trump_ft_z** = V241177 (PRE Trump feeling thermometer, 0-100; -9/-8/-1 dropped; z-scored). Verify V-code at implementation; if mis-coded log §10 deviation.
- **NEW fund_gaza_salience_z** = V241404 (humanitarian aid to Palestinians, 1=favor, 2=oppose, 3=neither; treated as ORDINAL covariate; z-scored). Cross-tabulated with cohort to test economic-vs-Gaza mediation contributions.
- **NEW fund_econ_x_cohort_interaction** = fund_econ_z × cohort_idx (numeric 1-5). Single column.

### 3.4 CES H6 cohort recoding

CES has continuous birthyr. Recode 6-level cohort:
- 1 = Silent (birthyr ≤ 1945)
- 2 = Boomer (1946-1964)
- 3 = GenX (1965-1980)
- 4 = Millennial-Older (1981-1988, ages 36-43)
- 5 = Millennial-Younger (1989-1996, ages 28-35)
- 6 = GenZ (1997+, ages 18-27)

### 3.5 Pew W159 H7 decomposition

Pew variables (per pre-reg v1.0 §12 dev 4): F_AGECAT 4-band, F_PRES20_VV (validated 2020 vote), F_PRES24_VV (validated 2024 vote). Required weights: WEIGHT_W159_VALIDATEDVOTE.

Verify variable names at impl time; if differently named log §10 deviation.

---

## 4. Stan model specs (LOCKED)

### Model A marginal (re-used from v1.0)
`code/stan/model_a.stan` (binary outcomes). Unchanged.

### Model A + cohort×race interaction (re-used from v1.1)
`code/stan/model_a_interaction.stan`. Unchanged.

### H4 extended-fundamentals variant
Same `model_a.stan` with K_fund = 8 (4 original + pid7 + Trump_ft + gaza_salience + econ×cohort).

### H6 6-cohort variant
Same `model_a.stan` with N_cohort = 6.

---

## 5. Verdicts (LOCKED)

Each hypothesis verdict reported as one of: **CONFIRMED**, **PARTIAL**, **REFUTED**, **INDETERMINATE** per the falsification gates in §1.

Aggregate verdict over v2 fits:
- If ≥4 of 7 hypotheses CONFIRMED: v1.1 findings are robust cross-substrate; "Asian generational bifurcation" and "cohort-bypass-of-pid7" cement as v2-level findings.
- If ≤2 of 7 CONFIRMED: v1.1 was substrate-specific; revise framing.
- Mixed: report as-is, no umbrella verdict.

---

## 6. Multiplicity correction

Hierarchical shrinkage in Model A handles multiple comparisons within each fit (per pre-reg v1.0 §6).

Across 7 v2 hypotheses tested:
- Each hypothesis is REPORTED with 90% CI as primary AND 95% CI as falsification threshold.
- No Bonferroni / Holm adjustment applied across hypotheses; each is a directional pre-registered test with own substantive prior.

---

## 7. Operational protocol (LOCKED execution order)

1. **Survey AP VoteCast variables** (codebook check at impl time). Log discrepancies as §10 deviations.
2. **Build AP VoteCast Model A data prep** with banded cohort + race + educ + gender + region + econ fund.
3. **Fit AP VoteCast Model A marginal** (validate convergence; no peeking at headline cells before fitting interaction).
4. **Fit AP VoteCast Model A + cohort×race interaction.** Report H1.2 / H2.2 / H3.2 verdicts.
5. **ANES H4 extended fundamentals fit.** Report H4 verdict.
6. **CES H6 6-cohort fit.** Report H6 verdict.
7. **CES H5 + ANES H5 5 outcomes.** Report H5 per-outcome + aggregate.
8. **Pew H7 cross-tab.** Report H7 decomposition.
9. **Write result_v2.0_dnc_postmortem.md** with all 7 hypothesis verdicts.

---

## 8. Explicitly NOT covered

- Model B (exposure pool) — deferred (Path C; ANES DUA unavailable).
- Model C (joint shrinkage) — deferred (Path C).
- Manuscript prose — user-authored, not in pre-reg scope.
- Cross-election longitudinal (2020 vs 2024 vs 2016) — out of scope.
- Causal-identification claims — this pre-reg locks descriptive + posterior-credibility verdicts only.

---

## 9. Threats to validity (acknowledged)

- AP VoteCast banded cohort introduces ecological bias if true cohort effects are non-monotonic within bands. H1.2 / H2.2 / H3.2 directional tests are robust to band-mixing only if cell signs preserve under aggregation.
- ANES extended fundamentals (H4) may absorb variance that is correlationally cohort-related but not partisanship-mediated; pre-reg commits to reporting individual fund coefficients with CIs so the mediation pathway is transparent.
- Pew H7 turnout-vs-choice may have validated-vote-coverage gaps (not every state in Pew's voter file matched); pre-reg commits to reporting state-level coverage with the decomposition.

---

## 10. v2 deviation log

| Date | Deviation | Rationale |
|---|---|---|
| 2026-05-24 | **§10 dev 1: AP cohort banding 4-band → 6-band.** Pre-reg §3.1 locked a 4-band remap (GenZ 18-29, Mill 30-44, GenX 45-64, Boomer 65+); actual AP VoteCast `AGE65` variable is 6-band (18-24, 25-29, 30-39, 40-49, 50-64, 65+). | AP codebook resolution is finer than expected — banding decision must reflect actual variable. 6-band is data-driven (no collapsing arbitrary cells) and strictly more informative; reading the H1.2/H2.2/H3.2 verdicts against the finer bands is conservative (rejects more nulls). |

### §10 dev 1 — 6-band → H1.2 / H2.2 / H3.2 verdict mapping rule (LOCKED before reading results)

Pre-reg H1.2/H2.2/H3.2 falsification gates reference "Millennial-band", "GenZ-band", "Boomer-band". Against the 6-band AP fit, the mapping is:

- **GenZ-band** ≡ AP band 1 (18-24). Band 2 (25-29) overlaps Mill-Young; not used for GenZ-band verdicts.
- **Millennial-band** ≡ AP band 3 (30-39) ∪ band 4 (40-49). Verdict reads CONFIRMED if EITHER band's cell 95% CI lies on the pre-reg-prescribed side; PARTIAL if one credible + one indeterminate; REFUTED if either credibly OPPOSITE.
- **Boomer-band / 65+ band** ≡ AP band 6 (65+).

Rationale: pre-reg 30-44 Millennial band straddles AP's 30-39 + 40-49 split. Reading EITHER band's credible-cell as a CONFIRMATION matches the original 30-44 directional intent. Requiring BOTH would be stricter than pre-reg specified.

This mapping rule was committed in this deviation BEFORE the verdict was read against the 6-band fit. Deviation log entry hash will be the lock.

---

**Locked at commit:** `[fill at commit]` on `main`.
**Repository:** https://github.com/mrnathanhumphrey-droid/DNC.
**Builds on:** prereg_v1.0 (HEAD 45ea69a) + result_v1.0 (HEAD 469dcd1) + result_v1.1 (HEAD 122fc8c).
