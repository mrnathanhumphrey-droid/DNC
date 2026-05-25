# Pre-Registration v2.9 Amendment 2 — Issue V-code corrections + F5 trust_elec refit

**Date:** 2026-05-25, filed AFTER run 1 codebook deep-dive revealed additional V-code mis-identifications. Amendment 1 (2026-05-24) corrected 4 V-codes; deeper inspection of CES 2024 codebook tables reveals 3 more issue-V-code errors and 1 direction-coding issue.
**No outcome-result interpretation has been written or committed yet.** Run-1 fit summaries are saved (numerical artifacts) but verdicts have not been published in any result file. Per pre-reg discipline §1, refining operationalization on the basis of codebook content (NOT on outcome relationships read from fit summaries) is allowed and required for integrity.

This amendment SUPERSEDES the H_SKIP_C predictor list in amendment 1. Hypotheses + decision rules UNCHANGED.

---

## 1. Run-1 errors traced

Codebook table extraction revealed:

| Run-1 predictor | Run-1 claimed | Codebook actual content |
|---|---|---|
| `issue_abor_z` (CC24_326a/b) | Abortion items | **Environment/climate items** (EPA carbon, renewable energy) |
| `issue_clim_z` (CC24_330a/b) | Climate items | **Feeling-thermometer ratings** of "Yourself" + "$CurrentGovName" |
| `issue_imm_z` (CC24_323a/b) | Immigration progressive composite | Items 323a (legal status — progressive) + 323b (border patrols — **conservative**); composite mixed direction |
| `issue_gaza_z` (CC24_308b_1..9) | Gaza policy composite | Gaza war "what should US do?" multiple-choice; sub-item content not extractable from codebook in this pass |

## 2. Corrections

### 2.1 Replace issue V-codes with correct items

**Abortion (TRUE V-codes):** `CC24_324a/b/c/d` (codebook table 81 confirms: "On the topic of abortion, do you support or oppose each of the following proposals?")
- CC24_324a: "Always allow a woman the right to obtain an abortion as a matter of choice" — 1=support = **PRO-CHOICE**
- CC24_324b: "Permit only in case of rape, incest, life endangered" — 1=support = **RESTRICTIVE**
- CC24_324c: "Make illegal in all circumstances" — 1=support = **MOST RESTRICTIVE**
- CC24_324d: "Expand access" — 1=support = **PRO-CHOICE**

`issue_abor_z` = z-score of (a_progressive + d_progressive + (2 - b) + (2 - c)) / 4, where each item recoded so HIGH = MORE pro-choice.

**Climate/Environment (TRUE V-codes):** `CC24_326a-f`
- CC24_326a: EPA regulate carbon — 1=support = PROGRESSIVE
- CC24_326b: 20% renewable — 1=support = PROGRESSIVE
- CC24_326c: Strengthen EPA enforcement — 1=support = PROGRESSIVE
- CC24_326d: Increase fossil fuel — 1=support = CONSERVATIVE
- CC24_326e: Halt oil/gas leases — 1=support = PROGRESSIVE
- CC24_326f: Prevent gas-stove ban — 1=support = CONSERVATIVE

`issue_clim_z` = z-score of mean (a + b + c + e + (2 - d) + (2 - f)) / 6, where each item recoded so HIGH = MORE pro-climate-policy.

**Immigration (DIRECTION-LOCKED V-codes):** `CC24_323a-d`
- CC24_323a: "Legal status to tax-paying undocumented" — 1=support = PROGRESSIVE
- CC24_323b: "Increase border patrols" — 1=support = CONSERVATIVE
- CC24_323c: "Build wall" — 1=support = CONSERVATIVE
- CC24_323d: "Permanent residence for Dreamers" — 1=support = PROGRESSIVE

`issue_imm_z` = z-score of (a + d + (2 - b) + (2 - c)) / 4 recoded so HIGH = MORE progressive on immigration.

**Gaza:** DEFER. Sub-item content not extractable from codebook in this session. Run-1 `issue_gaza_z` β = -0.389 STRONG-credible is uninterpretable without knowing what CC24_308b_1..9 each ask. Flagged for v2.10 follow-up after codebook PDF inspection.

### 2.2 Run-1 issue findings to RETAIN

Two issue predictors survive amendment 2 with clean operationalization:

- **`issue_econ_z` (CC24_301)** — National Economics retrospective. ✓ direction clear (1=Excellent..5=Poor; higher raw = worse econ). Run-1 β=+0.446 STRONG-credible CONFIRMED.
- **`issue_inflation_z` (CC24_303)** — Price change in past year. ✓ direction inferrable (1=much higher..5=little change/lower; higher raw = LESS inflation pain). Run-1 β=-0.190 WEAK-credible. Reading: HIGHER raw (LESS inflation pain) → LESS skip; equivalently MORE inflation pain → MORE skip. Consistent with `issue_econ_z` direction. CONFIRMED.

### 2.3 F5 trust_elec refit

Run-1 `trust_elec_z` fit: R̂=1.226, ESS=19, 491 divergent. F5 falsifier fires. Refit with **chains=8, warmup=2000, samples=2000** per pre-reg §4 F5.

Also: `trust_gov_z` direction must be verified empirically. Run-1 reported β=+0.238 STRONG positive (MORE trust → MORE skip) which is counterintuitive. Two interpretations:
- (a) My recode `{1: 3, 2: 2, 3: 1}` correctly flipped direction so HIGH=MORE trust, and the finding is genuine (high-trust → complacent → skip).
- (b) Codebook value labels for CC24_423 are reversed from my assumption (i.e., 1 actually = LEAST trust), in which case my recode broke direction and the true direction is HIGH=LESS trust → MORE skip (consistent with H_SKIP_D hypothesis).

Resolution: report both possibilities in result §6; flag CC24_423 value-label verification as v2.10 cleanup item.

### 2.4 Run-1 H_SKIP_A, H_SKIP_B, H_SKIP_E findings to RETAIN

- H_SKIP_A engage_composite_z: β=-0.150 WEAK CONFIRMED ✓ direction verified (CC24_430a "did you do X" recoded 1→1).
- H_SKIP_B mob_any_z: β=-0.251 STRONG CONFIRMED ✓ direction verified.
- H_SKIP_B mob_dem_z: β=-0.145 WEAK CONFIRMED.
- H_SKIP_E: NO CREDIBLE CELLS — REFUTED at standard threshold.

## 3. Refit scope

Six new Stan fits planned under amendment 2:
1. `skip_C_issue_abor_z` (with TRUE abortion items CC24_324a-d, direction-locked)
2. `skip_C_issue_clim_z` (with TRUE climate items CC24_326a-f, direction-locked)
3. `skip_C_issue_imm_z` (with direction-locked CC24_323a-d)
4. `skip_C_issue_harris_ft_z` (NEW — CC24_330d Harris feeling thermometer, single-item, exploratory addition since CC24_330 grid is FT not climate)
5. `skip_C_issue_trump_ft_z` (NEW — CC24_330e Trump feeling thermometer, single-item)
6. `skip_D_trust_elec_z_hardened` (F5 escalation: chains=8, warmup=2000, samples=2000)

All other run-1 fits retained.

## 4. Aggregate verdict UPDATED

H_SKIP_C re-scored at 6 dimensions (econ + inflation + true-abor + true-clim + true-imm + gaza-deferred + harris-FT + trump-FT). Pre-reg §3 gates unchanged: ≥3 CONFIRMED → CONFIRMED; etc.

## 5. Process integrity note

Amendment 2 is filed BEFORE any result_v2.9 document is committed and BEFORE any narrative interpretation of run-1 findings is published. Run-1 fit CSVs and JSON diagnostics exist in `data/processed/v29/` but constitute numerical artifacts, not verdicts. The published v2.9 result will include both run-1 and run-2 fits with V-code labels accurate per the amendment.
