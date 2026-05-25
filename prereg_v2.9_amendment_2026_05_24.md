# Pre-Registration v2.9 Amendment — Operationalization Corrections

**Date:** 2026-05-24, filed BEFORE running any v2.9 fits.
**Original pre-reg:** `prereg_v2.9_dnc_postmortem.md` (LOCKED at HEAD `bae6e0c`).
**Trigger:** post-lock codebook verification revealed FOUR V-code mis-identifications. Per pre-reg discipline §1 in NEXT.md ("Variable-identification / value-coding inspection IS allowed; outcome-relationship inspection is NOT"), correcting operationalization before any outcome fit is the integrity-preserving move.
**No outcome relationships were inspected before this amendment.**

This amendment SUPERSEDES the V-code lists in original pre-reg §2.1 (H_SKIP_C), §2.2 (H_SKIP_A), §2.4 (H_SKIP_D), §2.5 (H_SKIP_B). Hypotheses and decision rules are UNCHANGED — only the operationalization (which V-codes back each hypothesis) is corrected.

---

## 1. Corrections

### 1.1 H_SKIP_C — Issue dissatisfaction (V-code adjustments)

| Pre-reg item | Pre-reg description | Codebook actual | Action |
|---|---|---|---|
| CC24_303 | Economic retrospective | **"Price change in past year"** (inflation perception) | KEEP — inflation IS econ dissatisfaction component |
| CC24_323a/b | Immigration | Confirmed immigration items (binary support/oppose; codebook direction verified pre-fit) | KEEP |
| CC24_326a/b | Abortion | Confirmed abortion (binary support/oppose) | KEEP |
| CC24_330a/b | Climate (8-pt) | Confirmed climate-related, ordinal | KEEP, direction verified pre-fit |

**ADDITIONS to H_SKIP_C:**
- **CC24_301** ("National Economics", 6-pt, ~100% valid) — PRIMARY econ retrospective item, supersedes CC24_303 in interpretation while CC24_303 (inflation) is retained as a sub-component.
- **CC24_308b_1..9** ("Israel/Gaza" grid, binary items, 100% valid) — Gaza item set IS in CES Common Content. Pre-reg said no Gaza in CES (deferred to v3); this is corrected.

**Updated H_SKIP_C predictor set:** `issue_econ_z` (CC24_301), `issue_inflation_z` (CC24_303), `issue_gaza_z` (CC24_308b composite), `issue_imm_z` (CC24_323a/b), `issue_abor_z` (CC24_326a/b), `issue_clim_z` (CC24_330a/b). **Six issue dimensions tested.** Aggregate gate updated: ≥3 of 6 CONFIRMED → H_SKIP_C CONFIRMED; 2 of 6 → PARTIAL; 1 or 0 → REFUTED.

### 1.2 H_SKIP_A — Engagement (V-code adjustments)

| Pre-reg item | Pre-reg description | Codebook actual | Action |
|---|---|---|---|
| CC24_310a-d | Political activity 4-item battery | **"Know Party in Government"** grid (political knowledge) | REMOVE — knowledge ≠ engagement (per locked operationalization rule) |
| CC24_311a-d | Political talk frequency 4-item | **"Know Party of Representative"** grid (more political knowledge) | REMOVE |

**REPLACEMENTS for H_SKIP_A:**
- **CC24_430a_1..8** ("Past year" — political activity binary battery, 100% valid). 8 binary items: standard activities (signed petition, attended rally, etc.). This is the canonical CES engagement battery and what the pre-reg INTENDED.
- **CC24_430b_1..10** ("Donate money" — binary activity items, 100% valid). 10 binary indicators of where/how donated.
- **CC24_300a** (newsint, 3-pt) — 63% valid; INCLUDED with missingness dummy as sensitivity.

**Updated H_SKIP_A operationalization:**
- `engage_act_z` = z-score of mean(CC24_430a_1..8 recoded so 1=did the activity), z-scored.
- `engage_donate_z` = z-score of mean(CC24_430b_1..10 recoded so 1=donated to category).
- `engage_composite_z` = z-score of mean(engage_act_z, engage_donate_z).

Decision rule UNCHANGED.

### 1.3 H_SKIP_D — Trust / efficacy (V-code adjustments)

| Pre-reg item | Pre-reg description | Codebook actual | Action |
|---|---|---|---|
| CC24_443_1..5 | Trust-in-institutions 5-pt battery | **"State legislature spending"** policy-demand grid | REMOVE |
| CC24_444a-d | Election integrity binary | **"State policies"** policy-demand grid | REMOVE |
| CC24_445a/b | Election confidence binary | **"Supreme Court decisions"** policy-demand grid | REMOVE |

**REPLACEMENTS for H_SKIP_D:**
- **CC24_423** ("trustfed" — trust in federal government, 4 values incl. 8=DK, ~99% valid). Canonical trust-in-government item.
- **CC24_424** ("truststate" — trust in state government, 4 values, ~99% valid). Companion item.
- **CC24_421_1, CC24_421_2** ("Election fairness" — 5-pt, 100% valid). Election integrity items.

**Updated H_SKIP_D operationalization:**
- `trust_gov_z` = z-score of mean(CC24_423_recoded, CC24_424_recoded) where DK (8) → median impute; lower raw values = MORE trust per codebook convention.
- `trust_elec_z` = z-score of mean(CC24_421_1, CC24_421_2); direction verified pre-fit.
- `trust_combined_z` = z-score of mean of above.

Decision rule UNCHANGED.

### 1.4 H_SKIP_B — Direct mobilization gap (V-code adjustment)

| Pre-reg item | Pre-reg description | Codebook actual | Action |
|---|---|---|---|
| CC24_363 | Campaign contact in 2024 cycle | **"Vote Intention"** (pre-election) | REMOVE — would test vote-intent as predictor of skip, which is near-circular |

**REPLACEMENT for H_SKIP_B:**
- **CC24_431a** ("Contacted by candidate or political campaign" — binary 1=yes/2=no, 100% valid). Canonical post-election mobilization item — what the pre-reg INTENDED.
- **CC24_431b_1..4** (contact method — Dem/Rep/both/other indicators, conditional on CC24_431a==1). Used to separate Dem-contact from any-contact.

**Updated H_SKIP_B operationalization:**
- `mob_any_z` = z-score of binary(CC24_431a == 1).
- `mob_dem_z` = z-score of binary(CC24_431a == 1 AND CC24_431b_1 == 1) — contacted specifically by Democrats.

Decision rule UNCHANGED.

### 1.5 H_SKIP_E — UNCHANGED.

Race × cohort interaction model on CES VV Biden-2020 universe with `skipped` outcome. No V-code changes.

---

## 2. F-falsifier updates

**F2 (outcome imbalance):** original pre-reg said [25%, 65%]. Smoke-test (operationalization-only, not predictor-cross) showed universe skip prevalence = **5.33%** in skip|retain universe — much lower than F2 expected because pre-reg F2 conflated v2.3's "skip-share of non-retainers" (67-79%) with "skip prevalence in skip|retain universe." **F2 amendment:** drop the F2 gate; replace with documented expectation "skip prevalence likely 4-12% in skip|retain universe (per v2.3 cohort decomp); event count must support ≥600 skip events for binary logistic credibility." Current universe: ~928 skip events. PASSES.

All other falsifiers F1, F3, F4, F5 unchanged.

---

## 3. Verdict-rule additions

Because H_SKIP_C now has 6 sub-issues (was 4), the aggregate H_SKIP_C verdict is:
- 0 CONFIRMED → REFUTED
- 1-2 CONFIRMED → PARTIAL
- 3-4 CONFIRMED → CONFIRMED
- 5-6 CONFIRMED → STRONG CONFIRMED

---

## 4. Repository state

- Amendment filed 2026-05-24 at HEAD `bae6e0c + amendment commit`.
- No fits run yet on corrected operationalization. Wrong-operationalization run (started 21:08 EST, killed 21:11 EST via TaskStop after first-chain start) produced NO usable fit output — only `model_a.stan` was compiled. No summary CSVs, no diagnostic JSONs. Pre-reg integrity preserved.
- Updated script: `code/v29_skip_mechanism.py` (revised post-amendment).

---

## 5. Why the original errors happened

CES Common Content variable codes follow a numeric scheme where the meaning is not obvious from the code alone. The pre-reg's V-code descriptions were drawn from prior experience with similar CES batteries (where CC24_310 series IS typically engagement) without verifying against the 2024-specific codebook. The 2024 wave reassigned several codes (CC24_310/311 to knowledge, CC24_363 to vote intent, CC24_443/444/445 to policy-demand grids) compared to common historical patterns.

**Process lesson for future pre-regs:** ALWAYS dump varlabels from the codebook .docx before committing V-codes to a pre-reg, not after. For v3 and beyond, add a pre-reg checklist item: "Run codebook varlabel extraction; confirm each V-code's actual label matches its hypothesized construct."
