# Next Session — Pickup Pointer (DNC Post-Mortem)

**Locked:** 2026-05-23 (commit `122fc8c` on `main`, github.com/mrnathanhumphrey-droid/DNC)
**Last session ended:** result_v1.1 published. Cohort×race interaction (CES) + party-ID mediation probe (ANES) both complete. 4 credible CES interaction cells; party-ID mediates 61% of race-on-vote but NOT cohort.

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
| `model_a_interaction.stan` + fit + analyze scripts | DONE | 60b4078 |
| CES vote interaction fit (N=42028, 0 div, 4 credible cells) | DONE | 60b4078 |
| ANES vote interaction fit (N=3539, 0 credible cells — substrate-N limit) | DONE | 60b4078 |
| ANES vote_partyid fit (V241227x added as fund; race -61%, cohort +33%) | DONE | 122fc8c |
| `result_v1.1_dnc_postmortem.md` (interaction + party-ID, 188 lines) | WRITTEN + pushed | 122fc8c |

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

## v1.1 headline (post-interaction + party-ID)

**4 credibly non-zero cohort×race cells on CES vote:**
- Millennial × Hispanic -0.463 [-0.879, -0.103]  (Latino-Mill defection UPGRADED to credible)
- Millennial × Asian    -0.379 [-0.822, -0.005]  (NEW: Asian-Mill defection)
- GenZ × Asian          +0.437 [+0.058, +0.856]  (NEW: opposite direction same race)
- Boomer × Black        +0.547 [+0.165, +0.964]  (anchor confirmed)

**Asian-American voting in 2024 is generationally bifurcated** (only race with credibly-opposite cohort cells).

**Walk-backs:** GenZ × Black = -0.269 [-0.661, +0.140] — CI includes zero; downgrade v1.0 "GenZ Black erosion" claim from finding to suggestive at this N.

**Party-ID mediation:** race operates THROUGH pid7 (σ_race -61%); cohort operates AROUND pid7 (σ_cohort +33%). Two distinct mechanisms — Millennial defection survives partisanship control.

## v2 scope (per result_v1.0 §9 + v1.1 §5)

1. Fit remaining battery items: CES single_payer, CES structural_inequity, ANES race_relations, ANES science_arts compound, ANES foreign_aid. Item maps in operationalization supplement §1.
2. **AP VoteCast Model A + interaction** (N=139,938 voters, banded cohort approximation). Cross-substrate replication test of CES interaction cells — especially GenZ × Black (the v1.1 downgraded claim).
3. ~~Cohort × race interaction Stan~~ DONE v1.1.
4. ~~Party-ID-as-fundamental probe~~ DONE v1.1.
5. Pew VV turnout-vs-choice separation.
6. Model B/C revisit IF restricted-use ANES DUA becomes available.
7. Within-cohort splits (older/younger Millennial 28-35 vs 36-43, older/younger Boomer) per pre-reg §4.
8. **NEW v1.2 from v1.1 emergence:** within-Asian race detail — Asian-Mill defection + Asian-GenZ anchor split is the strongest single discovery. Worth disaggregating by ancestry / nativity / region if any substrate carries it.
9. **NEW v1.2:** mechanism of cohort-bypass-of-pid7 — what predicts Millennial Biden defection conditional on party-ID? Issue salience? Trump-specific evaluation? Economic perception × cohort interaction?

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
