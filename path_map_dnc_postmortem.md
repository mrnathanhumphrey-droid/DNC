# Path Map: From DNC 2024 Autopsy Release to Pre-Registered Statistical Post-Mortem

**Date:** May 22, 2026
**Status:** Pre-compute. Pre-registration draft. No data touched yet.
**Form:** Mirrors path_map_nba_to_c745.md. Steps explicit, falsification conditions upfront, what-cannot-be-concluded section at the end.

---

## 0. Why this exists

On May 21, 2026, the DNC released the Rivera-authored 2024 election autopsy with a disclaimer stating the DNC "was not provided with the underlying sourcing, interviews, or supporting data for many of the assertions contained herein and therefore cannot independently verify the claims presented." The released document is a narrative report. The supporting microdata, interview transcripts, and internal voter-file modeling are not public and, per Martin's statement, not held by the DNC either.

This project is not an attempt to "redo" the Rivera report. It is an attempt to construct, from public microdata, a statistically rigorous post-mortem of the 2024 Democratic presidential loss, with the medical-post-mortem discipline: pre-registered hypotheses, decomposition into mechanisms, confidence intervals on each mechanism, and explicit reporting of nulls and indeterminate findings.

The Rivera report is the prompt. It is not the benchmark.

---

## 1. Conceptual contribution

Standard post-mortems decompose vote shifts along demographic axes (race × education × age × gender × region). This project tests whether **exposure-stratified pooling** captures variance that demographic pooling misses, where exposure pools are defined by:

- **Information environment**: social media platform mix and intensity
- **Economic experience**: salary vs hourly pay structure
- **State-contact and material precarity**: insured vs uninsured

These are hypothesized to index *how people encounter politics and what economic precarity feels like to them*, which is closer to mechanism than census categories.

The standard demographic decomposition is fit honestly and reported in full. The exposure-pool decomposition is the proposed contribution. A joint model adjudicates whether exposure adds information beyond demographics.

---

## 2. Three-model architecture

- **Model A (standard, properly coded)**: fundamentals baseline + demographic partial pooling. Race × education × **birth cohort** × gender × region. Cohort coding uses Pew cutoffs (Silent ≤1945, Boomer 1946-1964, Gen X 1965-1980, Millennial 1981-1996, Gen Z 1997-2012) rather than arbitrary age bins. Continuous age included as robustness check. Within-cohort splits (older/younger millennial 1981-1988 vs 1989-1996; older/younger boomer 1946-1954 vs 1955-1964) reported as secondary specification where cell N permits. This raises the bar for Model B by ensuring the demographic baseline is not weakened by miscoded age structure.
- **Model B (exposure)**: fundamentals baseline + exposure-pool partial pooling. Social media × pay-structure × insurance.
- **Model C (joint)**: fundamentals baseline + both pooling structures, with shrinkage allowed on demographic effects.

Variance decomposition across A, B, C is the central methodological output. Each issue coefficient is estimated under all three.

---

## 3. Six-issue battery

Pre-committed before fitting. All six reported regardless of significance. Hierarchical shrinkage prior across issues handles multiplicity.

| Issue | What it probes | Substrate tier |
|---|---|---|
| Israel/Gaza position | Identity-coded foreign policy; salience-vs-position; the Rivera-leaked claim specifically | Tier 1 |
| Single-payer healthcare | Insured/uninsured pool directly; intra-coalition fault line | Tier 1 |
| Structural inequity | Salience-vs-position; high-information cell separation | Tier 1 |
| Race relations | Attitude shift independent of demographic-race shift | Tier 1 |
| Science/arts funding | Within-cell signal (salaried-insured-high-info); low-overall-but-concentrated | Tier 2 (operationalize as spending priorities) |
| USAID / foreign aid | Anti-establishment-spending frame; hourly-uninsured cell behavior | Tier 2 (operationalize as foreign aid; USAID-specific is forward-looking) |

---

## 4. Substrate inventory

- **CES 2024** (Cooperative Election Study, ~60k respondents): primary substrate. Issue items, vote choice, 2020 recall, platform usage, insurance status.
- **AP VoteCast 2024** (~120k respondents): validation. Larger N, validated against returns.
- **Pew Validated Voters 2024**: turnout/choice separation via vote validation against the file.
- **ANES 2024 Time Series**: panel structure for within-person attitude change.
- **GSS**: long-running spending-priorities items for Tier 2 issues.
- **CPS ASEC**: source for hourly/salary imputation via occupation × income × hours crosswalk.

Hourly/salary is the substrate-weakest variable in the design. Two-stage approach: impute pay-structure probability from CPS, propagate uncertainty through political model. Documented BLS occupation-code methodology exists.

---

## 5. Falsification conditions (pre-committed)

**Model B "wins" (exposure pools add real information):**
- ΔELPD or ΔWAIC vs Model A exceeds threshold (specify before fitting)
- Exposure-cell coefficients have CIs excluding zero in directions consistent with theory
- In Model C, demographic effects shrink substantially when exposure pools are added

**Model A "wins" (exposure pools add nothing beyond demographics):**
- Exposure-cell coefficients in Model C shrink to zero
- Demographic effects in Model C unchanged from Model A
- This is a publishable finding. The standard splits were sufficient.

**Both "lose" (residual variance dominates):**
- Residual variance exceeds threshold T across all three substrates
- Conclusion: issue-based decomposition insufficient; 2024 not well-explained by issue positions exposure-stratified or not
- Recommend identification of candidate omitted constructs (affect, institutional trust, identity)
- **This is the most epistemically valuable outcome and the pre-reg leaves room for it explicitly.**

---

## 5.5 Stated priors and their falsification conditions

The authors enter this analysis with a stated prior: that birth-cohort effects in 2024 are large, that the Millennial-Gen Z bloc has aligned attitudinally in ways the Gen X-Boomer bloc has not, and that exposure-pool stratification will reveal additional within-cohort heterogeneity tracking information environment and economic experience beyond what cohort alone captures.

Naming this prior is itself the rigor move. Pre-committed falsification conditions:

- **Cohort hypothesis falsified if:** cohort effects in Model A are small relative to other demographic effects, or if Millennial and Gen Z cohorts do not cluster attitudinally relative to Gen X and Boomer cohorts on the issue battery.
- **Exposure-beyond-cohort hypothesis falsified if:** in Model C, exposure-cell coefficients shrink to zero when cohort is properly coded and held fixed, and Model B's apparent gains over Model A vanish once Model A's cohort coding is corrected.
- **Reported regardless of direction.** A finding that properly-coded cohort effects explain most of the 2024 shift, with exposure pools adding nothing, is a publishable result and the authors commit to publishing it.

## 6. Decomposition output

The headline result is a variance decomposition:

> "Of the X-point 2020→2024 shift, Y points attributable to fundamentals (incumbency, economy, war/peace), Z points to issue-position shifts within exposure pools, W points to differential turnout across exposure pools, residual U ± SE."

Per-issue coefficient table reports estimates under Models A, B, C across three substrates. Sensitivity bounds (Rosenbaum-style Γ) on unmeasured confounding for each issue.

---

## 7. Mediation discipline

Demographic effects are mechanistically prior to some exposure effects (race shapes platform use; education shapes occupation which shapes pay structure). Model C includes mediation analysis. Honest answer to the anticipated critique "you've hidden demographics inside exposure variables": partially yes, and the question is whether exposure captures something *beyond* the demographic upstream, which the variance decomposition answers directly.

---

## 8. What cannot be concluded from public data

- DNC's internal voter-file modeling and its specific findings (e.g., the Rivera-attributed Israel-net-negative claim as the DNC modeled it). We can test whether the *direction* of the claim replicates in public substrates. We cannot reproduce the internal model.
- Campaign-internal polling, message-testing, and operational decisions.
- Catalist microdata; reports purchasable, microdata not.
- Anything requiring interview transcripts that Rivera may or may not still hold.

A finding in public substrates that does not replicate the DNC's internal claim is **not evidence the DNC was wrong**. It is evidence the claim is not robust to independent substrates. Both interpretations should be reported.

---

## 9. Discipline anchors

- Null-as-finding: pre-committed, reported in full.
- Pre-registration before any data touch.
- Six issues × three models × three substrates reported flat in supplement; headline tables collapse on substrate as robustness column.
- Hierarchical shrinkage prior across issues handles multiplicity.
- Walk-backs documented and visible.
- "Slow is smooth, smooth is fast."

---

## 10. Next steps (no compute yet)

1. Pre-registration document (separate file): hypotheses, model specifications in Stan pseudocode, falsification thresholds with numbers, multiplicity correction approach.
2. Substrate access verification: confirm CES 2024 module includes the platform and insurance items needed; confirm AP VoteCast 2024 microdata access status; identify CPS supplement edition for pay-structure imputation.
3. Operationalization sheet: exact question wording per issue per substrate, harmonization decisions documented.
4. Stan model skeletons: A, B, C with priors specified before any fit.
5. Lock pre-reg. Then touch data.
