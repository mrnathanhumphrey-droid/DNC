# Next Session — Pickup Pointer (DNC Post-Mortem)

**Locked:** 2026-05-23 (commit `c1a2859` on `main`, github.com/mrnathanhumphrey-droid/DNC)
**Last session ended:** v2 data prep complete; batch fit of 6 Model A targets running in background. Preliminary H1 NULL signal from smoke. User-direction: "post-mortem is discovery by definition; if we say we are wrong we go and figure out WHY."

---

## Where things stand

| Stage | Status | Commit |
|---|---|---|
| Path map (`path_map_dnc_postmortem.md`) | user-authored | 45ea69a |
| Pre-reg v1.0 (`prereg_v1.0_dnc_postmortem.md`) | LOCKED + 6 §12 deviations filed | 45ea69a + edits through c1a2859 |
| Operationalization supplement (`operationalization_v1.0_dnc_postmortem.md`) | LOCKED | 45ea69a |
| Substrate downloads (7/7) | landed + verified | 1d6d4be |
| Pay-structure imputation v1 (full features, AUC 0.8393) | done; NOT transfer-ready | c4e1cb6 |
| Pay-structure imputation v2 (transfer-ready, AUC 0.7851) | PASS §8 gate by 0.035 | 41b1f02 |
| Model A Stan code (`code/stan/model_a.stan`, `model_a_issue.stan`) | written, compiles | 94652cb |
| Model A v1 smoke (ANES vote, no fundamentals): H1 NULL signal | 67 divergent | 94652cb |
| Model A v2 data prep (proper gender/region/fundamentals) | done | c1a2859 |
| Model A v2 smoke (ANES vote): H1 NULL persists, 0 divergent | done | c1a2859 |
| Batch fit 6 Model A (ANES vote, israel, single_payer + CES vote + GSS science, foreign_aid) | **RUNNING in background task `b372l317q`** | — |

## What the batch is producing

`code/batch_fit_model_a.py` is running 6 Stan fits sequentially at 4 chains each (4-worker user-limit):

1. ANES vote (binary, N=3,539)
2. ANES Israel/Gaza (gaussian, N=4,568)
3. ANES single-payer (gaussian, N=4,514)
4. CES vote (binary, N=42,028) — this one will be slow (~5-15 min)
5. GSS science spending (gaussian, N=3,605)
6. GSS foreign-aid spending (gaussian, N=1,879)

Outputs land in `data/processed/fits/`:
- `fit_{substrate}_{outcome}_{type}_summary.csv` — full posterior summary table
- `fit_{substrate}_{outcome}_{type}_diag.json` — diagnostics + sigma means

Total wall clock estimate: ~30-90 min.

## Preliminary H1 signal (v2 smoke, ANES vote only)

```
sigma_race    0.659  [0.29, 1.19]
sigma_educ    0.493  [0.16, 1.02]
sigma_cohort  0.202  [0.01, 0.56]   <-- SMALL relative to others
sigma_gender  0.918  [0.31, 1.84]   <-- LARGEST
sigma_region  0.166  [0.01, 0.51]
```

H1 stated prior (pre-reg §5.5): "cohort effects large relative to other demographics" — **NOT supported** on ANES vote choice. Cohort SD is 3-5× smaller than gender, race, and education SDs. **Gender gap dominates.**

This is provisional; batch results will show whether the pattern holds across CES (larger N) and across issue positions (not just vote choice).

## Next-session pickup order (when batch completes)

1. **Read batch results.** `data/processed/fits/fit_*_diag.json` + `_summary.csv`. Per-fit: R-hat, ESS, divergent transitions, sigma_means dictionary.

2. **Build variance-decomposition table.** Per substrate per outcome: posterior sigma_race / sigma_educ / sigma_cohort / sigma_gender / sigma_region. Show side-by-side. Identify pattern: which demographic dominates which outcome on which substrate?

3. **Discovery posture: figure out WHY H1 was wrong (if it is).** Possible threads:
   - Cohort × race interaction? Maybe Gen Z effects exist but only within race-hispanic, etc.
   - Cohort × education? "Diploma divide" within cohort
   - Per-issue variation: maybe cohort dominates on Israel/Gaza but not vote choice (Gaza generational divide reported widely)
   - Cohort within-splits: older/younger Millennial; older/younger Boomer — per pre-reg §4 secondary spec
   - Are race effects mostly proxying party ID? Try a model with party ID added as fundamental
   - Is gender SD really that big or is it absorbing 2024 abortion / gender-specific issue salience?

4. **Pre-reg §10.1 step 8 (ELPD comparison) is skipped** because we're doing Model A only per Path C (B/C deferred). No ΔELPD vs Model B since B isn't fit.

5. **Per-issue findings table** (§9): per-substrate per-issue effect-size table with cohort × issue / race × issue / gender × issue interaction estimates. Per pre-reg §9: "always reported, regardless of cascade verdict."

6. **Write up `result_v1.0_dnc_postmortem.md`** as the headline result document. Cancer-substrate honest-conditional style.

## §12 deviation log status (6 entries)

1. GSS 2024 natarts absent → Issue 5 collapses to science-only on GSS
2. GSS 2024 no insurance variable → drops from Model B insurance pool
3. ANES 2024 PUF birth year RESTRICTED → use V241458x continuous age top-coded 80
4. Pew W159 F_AGECAT 4-band only → coarser cohort coding than AP VoteCast
5. Pew W159 actual N=9,609 (not 8,942)
6. ANES public-file restrictions exceed pre-reg §2 assumptions (income, industry, detailed race/educ all RESTRICTED); Model B/C deferred per Path C
7. §8 pay-structure imputation v2: predictor set reduced to transfer-ready features (drop occ, hours, earnings). AUC 0.7851 PASS gate by 0.035.

## Discovery threads to potentially follow (post-batch)

- **Israel/Gaza vs vote choice cross-tab.** Path map prompt was the Rivera-attributed claim. ANES Israel item should be the most directly probative.
- **CES racial-resentment battery** (Issue 3): scale large enough to estimate cohort × race interactions, which is what the prior actually predicts.
- **Gender × race interaction** on vote: 2024 reporting widely noted Latino-male shift. Cohort-Latino-male as a cell.
- **Sub-cohort splits within Millennial** (1981-1988 vs 1989-1996): per pre-reg §4 secondary spec.
- **GSS spending priorities × cohort** as a clean test of the "Gen Z attitudinal alignment" prior on a Tier 2 item.

## Things NOT yet done

- Per-issue Stan fits for items not yet wired in data_prep (CES single_payer, CES structural_inequity, ANES race_relations, ANES science_arts compound, ANES foreign_aid). Operationalization supplement §1 has the item maps; need to find the actual CES + ANES item columns.
- AP VoteCast Model A fit (vote-choice only; banded-age cohort approximation per §12).
- Pew VV turnout-vs-choice separation analysis.
- Within-cohort splits (older/younger Millennial, etc.).
- Mediation analysis (race → gender / race → cohort path decomposition).

## Repo state

Branch `main` at `c1a2859`. Pushed to `origin/main` synced. github.com/mrnathanhumphrey-droid/DNC.
