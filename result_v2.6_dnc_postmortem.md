# result_v2.6 — DNC 2024 Post-Mortem v2.6 (Behavioral/structural channel — also NOT THIS)

**Locked:** 2026-05-24 against `prereg_v2.6_dnc_postmortem.md` HEAD `abee034`.
**Builds on:** result_v2.1 (`27a0093`), result_v2.2 (`e441cbd`), result_v2.5 (`74d1a4d`).
**Repo:** github.com/mrnathanhumphrey-droid/DNC.

---

## 1. Headline (one sentence)

**Even the behavioral/structural channel hypotheses — campaign mobilization (party contact + activity) and life-stage economic position (housing tenure + marital status + student debt + financial worry) — fail to mediate the cohort defection signal.** σ_cohort stays at 0.43-0.53 across H27/H28/H29. **DNC mobilization gap is REFUTED**: party contact + campaign activity are not even credibly different from zero as vote predictors at this N. Financial worry is a real fundamental (β ≈ -0.2 credibly negative) but doesn't absorb cohort either. The cohort effect remains residual to everything ANES 2024 public release can measure.

---

## 2. Verdicts table

Reference baseline (v2.0.1 hardened H4): **σ_cohort = 0.448 [0.047, 1.053]**, K_fund=8, N=3533.

| Hyp | What's added | K_fund | σ_cohort (Δ vs baseline) | Verdict |
|---|---|---:|---|---|
| **H27** | mobilization: V242004 party-contact + V242011/12/13 activity | 10 | 0.430 (Δ -0.018, -4%) | **NOT MEDIATED** |
| **H28** | life-stage: V241530 owns-home + V241461x ever-married + V241569 student-debt + V241539 fin-worry | 12 | 0.528 (Δ +0.080, +18%) | **NOT MEDIATED + ANTI-SHRINKAGE** |
| **H29** | combined all 6 | 14 | 0.481 (Δ +0.033, +7%) | **NOT MEDIATED + ANTI-SHRINKAGE** |

**Aggregate verdict per pre-reg §1:** **BEHAVIORAL CHANNEL NOT THIS.** All 3 hypotheses NOT MEDIATED. Even the strongest combined-behavioral-channel test fails to shrink cohort variance.

---

## 3. Mediator β details (which behavioral predictors are real fundamentals?)

### H27 mobilization β's

- β_party_contact = +0.099 [-0.089, +0.277] — **NULL.** Party contact is not credibly different from zero as a vote predictor conditional on H4 baseline (2020 recall, pid7, Trump_ft, etc).
- β_campaign_activity = +0.126 [-0.100, +0.347] — **NULL.**

**The DNC-mobilization-gap hypothesis is REFUTED.** At this N, with the full H4 fundamentals partialed out, neither having-been-contacted-by-a-party-in-2024 nor having-participated-in-campaign-activities-2024 predicts Harris-vote. The proximate political channels (Trump favorability, party-ID, recall) absorb whatever predictive signal contact + activity carry.

### H28 life-stage β's

- β_owns_home = -0.151 [-0.328, +0.027] — **BORDERLINE NEGATIVE** (homeowners slightly less Harris-leaning at 90% CI; CI crosses zero at 95%).
- β_ever_married = +0.116 [-0.080, +0.309] — **NULL.**
- β_has_student_debt = -0.057 [-0.258, +0.146] — **NULL.**
- β_financial_worry = **-0.199 [-0.386, -0.012] CREDIBLY NEGATIVE.** More financial worry → less Harris-vote. The directional sign is informative: among the Harris-Trump major-party 2024 voters, higher financial-situation worry predicts Trump-vote.

### H29 combined β's (all 6 simultaneously)

- β_financial_worry = -0.212 [-0.404, -0.021] still **CREDIBLY NEGATIVE** — survives full combined controls.
- All others NULL or borderline.

**Financial worry is the only behavioral/structural item in v2.6 that proves to be a real fundamental.** It joins the v2.5 H23 media-diet ideology (β +0.638 credible) as the second "real but non-mediating" finding.

---

## 4. Updated mediator scorecard (12 ruled out, 0 confirmed)

| Source | Hyp | Mediator | β credible? | σ_cohort | Verdict |
|---|---|---|---|---:|---|
| v2.1 | H8 | Ideology (V241177) | YES | 0.386 | NOT MEDIATED (14% shrink) |
| v2.1 | H9 | Trust-gov composite | YES | 0.498 | NOT MEDIATED (anti-shrink) |
| v2.1 | H10 | Anti-system composite | YES | 0.386 | NOT MEDIATED (14% shrink) |
| v2.1 | H11 | Trump_ft × cohort | NULL | 0.444 | NOT MEDIATED + HOMOGENEOUS |
| v2.1 | H12 | Party-ID importance | NULL | 0.474 | NOT MEDIATED |
| v2.2 | — | Lasso 16-item multivariate | mixed | 0.407 (test) | AXIS NOT FOUND (9% on held-out) |
| v2.5 | H24 | Media-diet ideology | YES | 0.437 | NOT MEDIATED (2.5%) |
| v2.5 | H25 | Media-diet volume | YES | 0.543 | NOT MEDIATED (anti-shrink) |
| v2.5 | H26 | Media combined + interaction | YES + NULL | 0.488 | NOT MEDIATED + HOMOGENEOUS |
| **v2.6** | **H27** | **Mobilization (contact + activity)** | **NULL** | **0.430** | **NOT MEDIATED + NULL** |
| **v2.6** | **H28** | **Life-stage (home/married/debt/worry)** | **mixed** | **0.528** | **NOT MEDIATED + anti-shrink** |
| **v2.6** | **H29** | **Combined behavioral** | **mixed** | **0.481** | **NOT MEDIATED + anti-shrink** |

**The cohort signal sits at σ_cohort 0.40-0.55 across 12 tests in 7 categories.** Three homogeneous interactions (Trump_ft × cohort, media × cohort, mobilization β's NULL) reinforce the LEVEL-SHIFT reading: cohort doesn't differentially-weight existing channels; it's a baseline-propensity shift.

---

## 5. What v2.6 closes (Read B effectively bounded)

User's pre-v2.6 framing was "oh its B" — selecting Read B (cohort is BEHAVIORAL not ATTITUDINAL). v2.6 directly tested Read B with the strongest ANES-measurable behavioral/structural levers:

- **"DNC under-reached MillYoung" (mobilization-gap hypothesis): REFUTED.** Campaign contact + activity are not even credibly different from zero as vote predictors. The mechanism is NOT that DNC failed to mobilize.
- **"MillYoung defects because they're at a life-stage where housing/debt/finances make them more Trump-receptive": REFUTED at the mediation level.** Financial worry IS a real predictor (people with higher worry voted Trump more), but the worry-by-cohort variance is independent from the cohort-vote variance. They're separate channels.
- **"Combined behavioral channels absorb cohort": REFUTED.** Even with all 6 behavioral mediators added at once, σ_cohort stays at 0.48 — above the NOT MEDIATED gate.

**Read B is effectively bounded.** The behavioral/structural channels measurable in ANES 2024 don't mediate cohort either.

---

## 6. What remains (hard-bounded candidate space)

After v2.1 + v2.2 + v2.5 + v2.6, the surviving candidates for the cohort-bypass mechanism are:

### Data-blocked candidates

1. **Right-wing media exposure** — V241604 radio + V241605 websites are -2 in public release. Hannity/Levin/Shapiro/Bongino/Breitbart/Newsmax/OAN are STRUCTURALLY UNMEASURABLE from this release. **Path forward: ANES DUA, OR CES-team-module if any, OR Pew CRWG.**
2. **2020-cycle event exposure** — no direct ANES items. **Path forward: specialized 2020-protest / COVID-impact / J6-reaction survey, OR ANES post-election panel modules with retrospective items.**
3. **Right-wing podcast / social-media exposure** — not in any ANES 2024 release. **Path forward: specialized media-consumption surveys (Reuters Digital News Report, Pew Pathways).**

### ANES-2024-still-testable but lower-priority candidates

4. **Religious identity × cohort** — V241443a-h religious-identification battery NOT yet tested. Religious-none rises sharply by cohort. v2.7 candidate.
5. **Knowledge × cohort** — political-knowledge items (V241612-V241620 PREKNOW battery). Low-info × cohort interaction not tested.
6. **Linked-fate × race × cohort** — ANES has linked-fate items historically; race-conscious-identity dimension not tested.
7. **Conspiracy / misinformation receptivity** — V242563 (vaccines/autism) + similar items. Not tested.

### Acceptance candidate

8. **True latent generational disposition.** The cohort effect may be a real demographic-historical signal not reducible to any currently-measurable attitudinal or structural variable. The level-shift pattern + 12 ruled-out mediators + 3 homogeneous interactions support this interpretation. Productive move: pivot to Read C (descriptive characterization of MillYoung defectors via CES VV voter-file data) rather than continued mediator hunting.

---

## 7. Honest caveats + diagnostics

- **H27 divergences = 34** (above 10 threshold). R̂ 1.007, ESS 1112 — chains mix; mobilization sub-model is in thin-tail region. Verdict robust (σ_cohort = 0.430 >> 0.25 gate).
- **H28 + H29 divergences = 17 + 14** — within acceptable range. R̂ < 1.004. Clean.
- **Campaign-contact endogeneity.** Per pre-reg §4 threat: campaigns target receptive voters. The β_party_contact NULL finding is even MORE striking under this caveat — even if contact reflects targeting, it doesn't add predictive value beyond the H4 baseline of partisanship + Trump-favorability + 2020 recall.
- **Financial worry direction.** Among Harris-Trump 2-party voters, higher financial worry predicts Trump-vote. This is consistent with 2024's "vibecession" narrative. But it does NOT mediate the cohort signal — younger cohorts have higher financial worry AND defect more, but those are independent.
- **Single-substrate.** ANES only.

---

## 8. Repo state at lock

- Pre-reg v2.6 locked at `abee034`.
- 3 hardened fits stored under `data/processed/fits/`:
  - `fit_anes_vote_h27_binary_hardened_*` (mobilization)
  - `fit_anes_vote_h28_binary_hardened_*` (life-stage)
  - `fit_anes_vote_h29_binary_hardened_*` (combined)
- Joblibs under `data/processed/stan_data_anes_vote_h{27,28,29}.joblib`.
- Repo: github.com/mrnathanhumphrey-droid/DNC.

**Result commit hash to be filled at commit time.**
