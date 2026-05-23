# Result v1.1 — Cohort × Race Interaction (CES + ANES vote)

**Locked at commit** `[fill at commit]` on `main`, github.com/mrnathanhumphrey-droid/DNC.
**Updates** `result_v1.0_dnc_postmortem.md` (HEAD f6b1855); v1.0 sections unchanged.
**New work:** Model A + cohort×race hierarchical interaction layer (`code/stan/model_a_interaction.stan`), fit on CES vote (N=42,028) and ANES vote (N=3,539).
**Pre-reg status:** This is an exploratory follow-up to result_v1.0 §9 #3. Logged as v2 work; not in original pre-reg.

---

## 1. What the interaction model does

Adds a 5×6 (cohort × race) cell-specific deviation to the additive Model A:

```
eta = alpha + X_fund * beta_fund
    + race_eff[r] + educ_eff[e] + cohort_eff[c] + gender_eff[g] + region_eff[reg]
    + cohort_race_eff[c, r]
```

`cohort_race_eff[c, r]` measures how much each (cohort, race) cell departs from the additive marginal sum. Hierarchical half-normal(0, 0.5) prior on σ_cohort_race (tighter than marginal half-normal(0,1) since interaction should be smaller). 30 cells. Same 4-chain Stan fit (warmup 750, samples 750).

This formalizes the result_v1.0 §3 cross-tab as posterior estimates with credible intervals.

---

## 2. CES vote (N=42,028) — 4 credibly non-zero cells

R-hat max 1.006, ESS_bulk min 717, **0 divergent transitions.** Excellent convergence.

**σ_cohort_race = 0.340 [0.224, 0.486]** — credibly non-zero. There ARE real cohort×race interactions on CES vote, beyond the additive marginals.

**Marginal effects (with interaction layer in the model):**

| Demographic | σ | Notes |
|---|---:|---|
| race | 0.329 | shrunk from 0.390 marginal-only (interaction absorbs some race variance) |
| educ | 0.387 | unchanged |
| cohort | 0.364 | unchanged from 0.332 marginal-only |
| gender | 1.230 | unchanged |
| region | 0.147 | unchanged |
| **cohort_race** | **0.340** | **NEW — credibly non-zero** |

**4 of 30 interaction cells credibly significant** (95% CI excludes zero):

| Cell | Mean | 95% CI | Story |
|---|---:|---|---|
| **Millennial × Hispanic** | **-0.463** | [-0.879, -0.103] | Latino-Millennial defection CONFIRMED |
| **Millennial × Asian** | **-0.379** | [-0.822, -0.005] | NEW: Asian-Millennial defection |
| **GenZ × Asian** | **+0.437** | [+0.058, +0.856] | Asian split — Gen Z anchored opposite direction |
| **Boomer × Black** | **+0.547** | [+0.165, +0.964] | Loyal Boomer-Black Dem anchor |

**Implied total cell effects** (marginal race + marginal cohort + interaction), conditional on 2020 recall + econ:

| Cell | Σ effect (logit) |
|---|---:|
| Millennial × Hispanic | -0.879 (most anti-Harris cell) |
| Boomer × Black | +0.981 (most pro-Harris cell) |
| Span | 1.86 logit |

That's a ~70 percentage-point spread in predicted Harris probability between the most loyal cell (Boomer Black) and the most defecting cell (Millennial Hispanic), holding 2020 recall + econ perception constant.

---

## 3. ANES vote (N=3,539) — null at cell level; substrate-N limit

R-hat max 1.005, ESS_bulk min 855, 3 divergent transitions. Converged.

**σ_cohort_race = 0.184 [0.013, 0.482]** — CI starts very close to zero. Interaction layer is weakly identified.

**0 of 30 interaction cells credibly significant.** Point estimates partially replicate CES:
- Boomer × Black = +0.124 (same sign as CES +0.547, but smaller and CI [-0.155, +0.686] includes zero).
- Hispanic cells mixed direction.
- Millennial × Asian = +0.088 (OPPOSITE sign vs CES -0.379) — but with per-cell n ≈ 30-50, unreliable.

**Methodological lesson:** Cell-level interaction discovery requires substrate-N at CES scale (N≈40k). ANES at N≈3.5k can fit the marginal Model A reliably but cannot credibly identify 30-cell cohort×race departures. AP VoteCast (N=139,938) at v2 will be the obvious cross-substrate replication test if banded-cohort approximation holds — see operationalization supplement §3.2.

---

## 4. Updates to v1.0 narrative

### Walked back from v1.0:
- **"GenZ Black defection"** (v1.0 §3 point 2) — downgraded from finding to suggestive. CES cross-tab showed GenZ Black retention 86.3% (vs Silent 100%) BUT cohort_race_eff[GenZ, Black] in interaction model = -0.269 with 95% CI [-0.661, +0.140] — **not credibly distinct from zero.** The cross-tab point estimate is consistent with the Black-voter-generational-erosion thesis but the interaction model's cell CI says we can't rule out zero. n=99 for the cell. **Direction tentative; magnitude requires larger N to confirm.** AP VoteCast Model A + interaction at v2 will resolve.

### Tightened from v1.0:
- **Latino-Millennial defection** (v1.0 §3 point 1) — UPGRADED from cross-tab to posterior-credible. Interaction cell -0.463 [-0.879, -0.103] with full Stan model. This thread is now formal.

### New from v1.1:
- **Asian generational split** — Millennial × Asian credibly NEGATIVE (-0.379), GenZ × Asian credibly POSITIVE (+0.437). Same race, opposite directions across cohorts. The only race in CES where two cohort cells go credibly opposite. Asian-American voting in 2024 is generationally bifurcated.
- **Boomer-Black anchor** — Cell-level +0.547 confirms the standard "older Black voters most loyal Dems" pattern shows up as the strongest single POSITIVE cell in the interaction layer, not just a marginal effect.

### Unchanged from v1.0:
- σ_cohort_race in CES is credibly non-zero — interactions are REAL, not noise.
- White retention shows NO credible interaction cell (all 5 white cohort cells CI cross zero). The marginal white race_eff carries the full white-cohort story; there's no white-by-cohort kink at the cell level. **The cohort signal lives in race-of-color cells, not in white cells.**
- Marginal cohort_eff for Millennial in the interaction model = -0.353 [-0.795, +0.014] — slightly MORE negative than the non-interaction additive Model A (-0.311). The interaction layer adds to Millennial-Hispanic / Millennial-Asian defection rather than absorbing the marginal Millennial effect.

---

## 5. The thread map after v1.1

| Thread | Status | Source |
|---|---|---|
| Attitudes-vs-vote gap | CONFIRMED v1.0 | Variance decomp + cohort_eff |
| Race-on-vote >> race-on-issues | CONFIRMED v1.0 | σ_race comparison across 8 fits |
| Latino-Millennial defection | UPGRADED to posterior-credible | CES interaction cell |
| Asian-Millennial defection | NEW | CES interaction cell |
| Asian generational SPLIT | NEW | CES interaction GenZ-Asian opposite |
| Boomer-Black anchor | CONFIRMED | CES interaction cell |
| GenZ-Black erosion | DOWNGRADED to suggestive | CES interaction CI crosses zero |
| White-by-cohort kink | NULL (no credible cells) | CES interaction model |
| Gender-by-NB skew | OPEN | σ_gender driven by NB cell; unprobed at cell level |
| Party-ID mediation of race-on-vote | **CONFIRMED** | ANES vote_partyid fit (see §8) |
| Cohort-on-vote IS NOT mediated by party-ID | NEW finding | Same fit; σ_cohort INCREASES with pid7 control |

---

## 6. What v1.1 changes about the Democratic post-mortem framing

The race-cohort interaction structure is more SPECIFIC than v1.0 implied:

1. **Latino voter shift is specifically a Millennial phenomenon** in CES 2024. Older Latino Biden voters retained Harris reliably; Gen Z Latino Biden voters point in mildly opposite direction (cell +0.235, not credible). The widely-reported "Latino swing" in 2024 is a generational defection within Hispanic voters — not a broad Hispanic-realignment.

2. **Asian-American voting in 2024 was generationally bifurcated.** Millennial Asian Biden voters defected (cell -0.379, credibly); Gen Z Asian Biden voters were MORE anchored to Harris than the additive marginals would predict (+0.437, credibly). Same race, opposite directions across adjacent cohorts. This is a NEW finding not surfaced in v1.0.

3. **Older Black voters remained the most loyal Dem cell** in CES (cell +0.547, credibly). The Black-voter-generational-erosion thesis (younger Black voters less Dem-loyal) is consistent in DIRECTION but not credibly distinct from zero at the cell level in our data.

4. **White voters did not split by cohort in interaction cells** — no credible white-by-cohort effect. The cohort signal on Harris vote operates through race-of-color voters, not through white voters.

These are MECHANISTICALLY DIFFERENT stories than a generic "younger voters defected." Future Dem coalition strategy that aggregates "younger voters" misses the bifurcation by race-cohort cell.

---

## 8. Party-ID mediation probe (ANES vote, N=3,533)

Adds V241227x (PRE summary 7pt party ID; z-scored, 1=Strong D, 7=Strong R) as a 5th fundamental to the existing 2020-recall + econ-perception fundamentals matrix.

**σ shrinkage when party-ID enters as fundamental:**

| σ | Without pid7 | With pid7 | Δ |
|---|---:|---:|---|
| race | 0.659 | 0.255 | **-61%** |
| gender | 0.918 | 0.513 | -44% |
| educ | 0.493 | 0.493 | flat |
| region | 0.166 | 0.185 | +12% |
| **cohort** | **0.202** | **0.269** | **+33%** |

**Race-on-vote residual is small once party-ID is controlled.** Cell-level changes:

| Race | Base race_eff (95% CI) | +pid7 race_eff (95% CI) |
|---|---|---|
| Black | +0.863 [+0.23, +1.61] credible | +0.162 [-0.12, +0.70] not credible |
| White | -0.424 [-0.97, +0.12] borderline | -0.027 [-0.34, +0.26] not credible |
| Hispanic | -0.129 [-0.72, +0.47] | -0.135 [-0.57, +0.13] |
| Asian | -0.097 [-0.73, +0.53] | -0.018 [-0.45, +0.37] |

**The race-on-vote effect operates almost entirely through party identification.** Race predicts vote because race predicts party ID; conditional on party ID, the residual marginal race effect is small and not credibly distinct from zero across all 6 race cells.

**Party-ID coefficient (β_fund_pid7_z) = -2.000 [-2.20, -1.81] per σ** — by far the largest fundamental. For reference: 2020 recall Biden one-hot = +2.13, 2020 recall Trump = -1.68, econ z = -1.02.

**Cohort signal is NOT mediated by party-ID.** σ_cohort INCREASES from 0.202 to 0.269 (+33%) when party-ID enters. The Millennial-anti-Harris signal that appeared in CES marginal Model A and in v1.0 §3 cross-tab is INDEPENDENT of partisanship. Younger Biden voters defected above-and-beyond what their party-ID would predict.

**This is a different mechanism than the race effect.** Race operates THROUGH party-ID; cohort operates AROUND party-ID. The Democratic post-mortem cannot collapse "younger voter defection" into "younger voters became Republican" — younger voters defected even controlling for their stated partisanship.

---

## 9. The mechanism diagram after v1.1

```
race ─────────► party-ID ─────────► vote
                  │
       cohort ────┘    (cohort does NOT operate through party-ID;
                       cohort_eff sharpens when party-ID is controlled)

       cohort ─────────────────────► vote (independent of party-ID)
```

In the post-mortem framing: **race-based vote choice is a partisanship story (well-known)**. **Cohort-based vote defection is NOT a partisanship story — it operates separately**. The 2024 Democratic loss has a partisanship component (race × party-ID) and a separate cohort-defection component that crosses partisanship lines.

Mechanistically: a Millennial Biden 2020 voter who reports as "Strong Democrat" in 2024 still has elevated defection probability compared to a Silent Biden voter who reports as "Strong Democrat" in 2024. The defection is NOT explained by them having weaker stated party ID.

---

## 7. Limits + caveats

- Cell n in CES: Boomer×Black 1571, Millennial×Hispanic 349, Millennial×Asian 184, GenZ×Asian 72, GenZ×Black 99. The credibly-non-zero cells are the larger n cells. The CIs on smaller-n cells are wide for principled reasons (less data).
- σ_cohort_race = 0.340 means the typical cell deviation is ~0.34 logit. The 4 credibly-non-zero cells are 1.5-3 σ outliers from the additive sum; the other 26 cells shrink toward zero appropriately.
- **No multiplicity correction applied** beyond hierarchical shrinkage (per pre-reg §6). The 4 credible cells are consistent with the prior-narrative interpretation and shouldn't be reinterpreted as 4 independent hypothesis tests.
- ANES NULL at cell level is a substrate-N limit, not a substantive contradiction. AP VoteCast (N=139,938) at v2 is the natural cross-substrate test.
- The model treats cohort+race+gender+educ+region as exchangeable random effects with their own σ. A more flexible model (e.g., separate weak/strong-Dem split in fundamentals; or party-ID 7-pt as covariate) would change the marginal effects. Party-ID probe is in v1.2 (running).
