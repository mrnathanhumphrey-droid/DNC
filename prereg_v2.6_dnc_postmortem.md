# Pre-registration v2.6 — DNC 2024 Post-Mortem (Behavioral/structural channel for cohort-bypass mechanism)

**Locks BEFORE running v2.6 fits.** Builds on:
- result_v2.1 (HEAD `27a0093`): 5 attitudinal mediators NOT MEDIATED.
- result_v2.2 (HEAD `e441cbd`): lasso 16-item multivariate AXIS NOT FOUND.
- result_v2.5 (HEAD `74d1a4d`): mainstream-media-diet NOT THIS.

**Motivation.** After 9 ruled-out attitudinal/media mediators with the pattern of LEVEL-SHIFT (not heterogeneous slope) + two HOMOGENEOUS interactions (Trump_ft × cohort, media × cohort), the working read is that **the cohort defection signal is BEHAVIORAL/STRUCTURAL, not ATTITUDINAL**. v2.6 tests the structural-channel hypotheses directly: mobilization (campaign contact) + life-stage (housing tenure / marital status / student-debt / financial anxiety).

Per user framing 2026-05-24: *"oh its B"* (selecting Read B from the v2.5-result follow-up rundown: cohort effect is BEHAVIORAL not ATTITUDINAL — channels to test are mobilization-gap, life-stage economic shock, 2020-event exposure, right-wing-media — pursuing the ANES-2024-testable subset).

---

## 0. What this pre-reg LOCKS

- 3 v2.6 hypotheses (H27/H28/H29) targeting behavioral/structural channels
- ANES item composites + V-codes
- Verdict gates
- Aggregate verdict reading

**What this pre-reg does NOT lock:**
- Right-wing media (blocked, see v2.5 §3)
- 2020-cycle event exposure (no direct ANES items)
- Causal-identification

---

## 1. Hypotheses (LOCKED)

**Reference baseline:** v2.0.1 hardened H4 fit — **σ_cohort = 0.448 [0.047, 1.053]**, K_fund=8, N=3533.

### H27 — Campaign mobilization (party contact + activity participation) mediates cohort

**Prior:** v2.3 H7 + v2.3 found MillYoung is the active-flipper cell while GenZ skips. If MillYoung's flipping AND GenZ's skipping both stem from a campaign-mobilization gap (DNC under-reached younger cohorts; GOP campaign reached MillYoung specifically), σ_cohort should shrink under contact controls.

**Mediator construction:**
- `fund_party_contact_z` = z-score of (V242004 == 1) binary indicator (party contact in 2024 campaign).
- `fund_campaign_activity_z` = z-score of count of (V242011 + V242012 + V242013) all coded 1=yes, 2=no. Convert to 0/1 indicators then sum, then z-score. (Items: online political meetings, in-person rallies/dinners, button/sticker/sign.)

**Test:** Add both `fund_party_contact_z` + `fund_campaign_activity_z` to H4 K_fund=8 baseline. K_fund_new=10.

**Falsification gates (re-use v2.1 thresholds):**
- **MEDIATED:** σ_cohort < 0.15.
- **PARTIAL:** σ_cohort ∈ [0.15, 0.25].
- **NOT MEDIATED:** σ_cohort ≥ 0.25.

### H28 — Life-stage / economic position mediates cohort

**Prior:** MillYoung (28-35 in 2024) was 24-31 during 2020 — peak first-time-homebuyer + service-worker + early-career-debt cohort. If structural economic position (own home / never married / has student debt / financial worry) mediates, the cohort defection is a LIFE-STAGE STRUCTURAL signal masquerading as "generation."

**Mediator construction:**
- `fund_owns_home_z` = z-score of (V241530 == 1) binary indicator (home owned by household member).
- `fund_ever_married_z` = z-score of (V241461x ∈ {1, 2, 3, 4}) — i.e., has-ever-been-in-formal-partnership; vs V241461x == 5 (never married).
- `fund_has_student_debt_z` = z-score of (V241569 > 0) binary indicator.
- `fund_financial_worry_z` = z-score of V241539 reverse-coded (so HIGH = MORE worried; raw 1=extremely worried, 5=not worried).

**Test:** Add all 4 to H4 baseline. K_fund_new=12.

**Falsification gates:** same as H27.

### H29 — Combined behavioral + structural

**Prior:** Maximum-power test — both H27 and H28 mediators simultaneously.

**Test:** Add all 6 mediators (party_contact + campaign_activity + owns_home + ever_married + has_student_debt + financial_worry) to H4 baseline. K_fund_new=14.

**Falsification gates:** same as H27.

### Aggregate verdict

- **BEHAVIORAL CHANNEL CONFIRMED:** ≥1 of H27/H28/H29 reaches MEDIATED gate.
- **BEHAVIORAL CHANNEL PARTIAL:** ≥1 reaches PARTIAL gate; none MEDIATED.
- **BEHAVIORAL CHANNEL NOT THIS:** All 3 NOT MEDIATED. Reading: even the structural/behavioral channel (the strongest remaining ANES-testable lever) does NOT mediate cohort. The cohort signal is then RESIDUAL to everything measurable in ANES 2024 public release — pointing to right-wing media (data-acquisition-blocked) or 2020-event-exposure (no items) or true-generational-disposition (latent).

---

## 2. Operationalization (LOCKED)

### 2.1 Sample frame

Same as H4 baseline: respondents with valid 2024 PRES major-party vote (V242096x ∈ {1, 2}), valid 7-pt pid7 (V241227x > 0), valid demographics, valid 2020 recall. N expected ≈ 3533.

### 2.2 Missing-data handling

Per item:
- Party contact / activity items: code -6 (no post interview), -7 (insufficient partial), -9 (refused), -1 (inapplicable) as MISSING. Mean-impute the z-score to 0 (sample mean) with a flag tracked but not added as fundamental.
- Home tenure: -9 (refused), -8 (DK), -4 (error) as MISSING.
- Marital: -2 (DK/RF) as MISSING.
- Student debt amount: -9, -1 as MISSING (effectively zero student debt — the "0" code is preserved).
- Financial worry: -9, -8, -1 as MISSING.

Report missingness rate per mediator in result §6 caveats.

### 2.3 Stan model + fit configuration

`model_a.stan`, hardened: chains=6, warmup=1000, samples=1000, seed=42.

---

## 3. Verdicts

H27, H28, H29: MEDIATED / PARTIAL / NOT MEDIATED per §1 gates.

Aggregate: per §1.

**Additional reporting** (descriptive, not pre-reg-gated):
- Each mediator's β with 90% CI (which behavioral predictors are real fundamentals?).
- σ_cohort posterior + 90% CI per H.

---

## 4. Threats to validity

- **Direction of causality.** Campaign-contact may be ENDOGENOUS to vote choice (campaigns target receptive voters). The descriptive verdict ("does X absorb cohort variance") is associational; if H27 MEDIATES, it could reflect targeting rather than mobilization-causing-vote.
- **Self-report.** All measures are self-reported. Campaign contact recall is noisy.
- **Life-stage proxies are imperfect.** Marital status / housing / debt are correlated cohort markers, but the EFFECT of each on vote is conditional on many unmeasured variables (income, region, employment).
- **K_fund growth.** H29 has K_fund=14; at N=3533, this is 5 fundamentals per ~700 sample → manageable but pushing the binary-logistic limit. Hardened settings should accommodate.
- **Single-substrate.** ANES only. CES has comparable items (CC24_xxx homeownership, marital) for cross-substrate replication in v3.

---

## 5. v2.6 deviation log

| Date | Deviation | Rationale |
|---|---|---|

(Empty at lock; populated as v2.6 work surfaces discrepancies.)

---

**Locked at commit:** `[fill at commit]` on `main`.
**Repository:** https://github.com/mrnathanhumphrey-droid/DNC.
**Builds on:** result_v2.1 (27a0093) + result_v2.2 (e441cbd) + result_v2.5 (74d1a4d).
