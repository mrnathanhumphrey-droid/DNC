# Next Session — Pickup Pointer (DNC Post-Mortem)

**Locked:** 2026-05-23 (commit `469dcd1` on `main`, github.com/mrnathanhumphrey-droid/DNC)
**Last session ended:** result_v1.0_dnc_postmortem.md written + pushed. 8 Model A fits done, H1 NULL on magnitude, INVERTED on vote direction. Attitude-vs-vote gap surfaced as central finding.

---

## Where things stand

| Stage | Status | Commit |
|---|---|---|
| Path map (user-authored) | LOCKED | 45ea69a |
| Pre-reg v1.0 (12 sections + 8 §12 deviations) | LOCKED | 45ea69a + edits through 469dcd1 |
| Operationalization supplement | LOCKED | 45ea69a |
| Substrate downloads (7/7) | LANDED | 1d6d4be |
| Pay-structure imputation v2 (transfer-ready, AUC 0.7851) | DONE, PASS §8 gate | 41b1f02 |
| Model A Stan code (`model_a.stan`, `model_a_issue.stan`) | DONE | 94652cb |
| Batch A (5 fits: ANES vote, gaza_aid_pal, CES vote, GSS science, GSS foreign_aid) | DONE | 2289559 |
| §12 deviation 8 (single_payer V247→V245 + israel→gaza_aid_pal rename + israel_military + gaza_protests added) | FILED | 2289559 |
| Batch B (3 fits: ANES single_payer V245 corrected + israel_military V241401 + gaza_protests V241410) | DONE | 469dcd1 |
| `result_v1.0_dnc_postmortem.md` (200 lines, 9 sections) | WRITTEN + pushed | 469dcd1 |

## Headline findings (per result_v1.0 §1-5)

**Variance decomposition (Model A posterior σ across 8 fits):**
- Gender dominates 6/8 fits.
- Cohort dominates 1/8 (ANES israel_military σ_cohort = 0.324).
- Cohort tied on 1/8 (ANES single_payer 0.284 ≈ gender 0.291).
- **H1 NULL at substrate-aggregate level.**

**Cohort direction:**
- Issue attitudes (Israel-military, single-payer, Gaza-protests): younger cohorts credibly more progressive. **H1 direction CONFIRMED.**
- Vote choice (CES): **Millennial credibly anti-Harris (cohort_eff = -0.311 [-0.57, -0.06])**, controlling for 2020 recall. **H1 direction INVERTED.**
- Mechanism: Biden→Harris retention drops monotonically Silent 98.4% → GenZ 90.8%.

**Decomposition by race × cohort (CES Biden→Harris retention):**
- Millennial Hispanic Biden voters: 82.7% retention (n=349) — lowest cell.
- GenZ Black Biden voters: 86.3% (n=99) — small sample.
- White retention >91% across all cohorts.

**Central frame:** 2024 was attitude-vs-vote gap, not attitudinal realignment. Younger voters held progressive positions but defected from Biden→Trump at 3x the Silent rate.

**Secondary:** race-on-vote (σ=0.39-0.66) vs race-on-issues (σ=0.08-0.23) asymmetry. Race predicts vote much more than issue attitudes, conditional on 2020 recall.

## v2 scope (per result_v1.0 §9)

1. Fit remaining battery items: CES single_payer, CES structural_inequity, ANES race_relations, ANES science_arts compound, ANES foreign_aid. Item maps in operationalization supplement §1.
2. AP VoteCast Model A (vote only, banded cohort approximation). Largest-N cohort test.
3. **Cohort × race hierarchical interaction Stan model** to formalize the cross-tab in result.md §3 as posterior estimates with CIs.
4. Party-ID-as-fundamental probe on ANES race-on-vote (race asymmetry follow-up).
5. Pew VV turnout-vs-choice separation.
6. Model B/C revisit IF restricted-use ANES DUA becomes available.
7. Within-cohort splits (older/younger Millennial 28-35 vs 36-43, older/younger Boomer) per pre-reg §4.

## §12 deviation log (8 entries)

1. GSS 2024 natarts absent → Issue 5 collapses to science-only
2. GSS 2024 no insurance variable → drops from Model B insurance pool
3. ANES 2024 birth year RESTRICTED → use V241458x continuous age top-coded 80
4. Pew W159 F_AGECAT 4-band only
5. Pew W159 actual N=9,609
6. ANES public-file restrictions exceed §2 assumptions; Model B/C deferred (Path C)
7. §8 pay-structure imputation: transfer-ready feature reduction (AUC 0.7851 PASS)
8. ANES outcome miscodings corrected: single_payer V247→V245 + israel→gaza_aid_pal rename + israel_military/gaza_protests added

## Repo state

Branch `main` at `469dcd1`. Pushed to `origin/main`. github.com/mrnathanhumphrey-droid/DNC.
