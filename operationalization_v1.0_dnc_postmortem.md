# DNC 2024 Post-Mortem — Operationalization Supplement v1.0

**Companion to:** `prereg_v1.0_dnc_postmortem.md`
**Date drafted:** 2026-05-22
**Status:** Locked alongside the pre-reg.

This document records per-substrate item operationalization, harmonization rules, exposure-pool construction, cohort coding (including the AP VoteCast band-to-cohort approximation), and data dictionary references. It is the supplement the path map §10 step 3 calls for. Any divergence between this document and actual substrate data at implementation time is logged in pre-reg §12 deviation log.

---

## 1. Item-level mapping per substrate

### Issue 1 — Israel/Gaza position

| Substrate | Variable(s) | Question text status | Scale |
|---|---|---|---|
| ANES 2024 | Israel military aid item + Palestinian humanitarian aid item (variable names to confirm at codebook pull) | Confirmed present via release-codebook search 2026-05-22 | 7-pt each (standard ANES policy-scale convention) |
| CES 2024 Common Content | NOT PRESENT | — | — |
| GSS 2024 | NOT PRESENT | — | — |
| AP VoteCast 2024 | `ISRAELAID` | 4-pt favor/oppose (confirmed via PUF codebook 2026-05-22) | 4-pt |
| Pew VV 2024 | NOT PRESENT | — | — |

**Harmonization rule:** Z-standardize within substrate before pooling. Direction sign-aligned across substrates so "more support for Israel military aid" = positive. ANES Palestinian-humanitarian-aid item enters as a separate covariate, NOT folded into Israel-aid; the path map's framing of the Rivera-attributed claim is on the Israel-military-aid item specifically.

### Issue 2 — Single-payer healthcare / government health insurance

| Substrate | Variable(s) | Status | Scale |
|---|---|---|---|
| ANES 2024 | Government health insurance scale | Confirmed (long-running ANES item) | 7-pt |
| CES 2024 Common Content | ACA / single-payer support items | Confirmed | Item-dependent (typically 4-pt or binary support/oppose) |
| GSS 2024 | NOT PRESENT | — | — |
| AP VoteCast 2024 | NOT PRESENT for M4A / single-payer directly; `HEALTHCOV` policy-attitude + `MEDICAID` expansion exist but measure different constructs | DROPPED from Issue 2 analysis | — |
| Pew VV 2024 | NOT PRESENT | — | — |

**Harmonization:** Z-standardize within substrate. ANES 7-pt and CES (often 4-pt) standardized separately; cross-substrate comparison uses z-scores only. CES ACA/M4A items may load on a 1-factor model — pre-reg specifies first principal component if multiple items present, else single-item z-score.

### Issue 3 — Structural / systemic racial inequity

| Substrate | Variable(s) | Status | Scale |
|---|---|---|---|
| ANES 2024 | Racial inequity / structural-racism battery | Confirmed | Battery (typically 4-6 items, 5-pt agree-disagree) |
| CES 2024 Common Content | Racial resentment battery (standard 4-item Henry-Sears battery) | Confirmed | 4 items × 5-pt |
| GSS 2024 | NOT PRESENT (GSS has racial-attitude items but not this specific battery in 2024) | — | — |
| AP VoteCast 2024 | `RACISMUS` 4-pt seriousness (single item, partial) | Partial — single-item proxy | 4-pt |
| Pew VV 2024 | NOT PRESENT | — | — |

**Harmonization:** ANES + CES standardized to first principal component of their respective batteries (reverse-coded as needed so higher = stronger structural-racism endorsement). AP VoteCast single-item `RACISMUS` enters as standardized scalar; flagged in writeup as "partial" because it's a salience/seriousness probe, not a multi-item construct. Cross-substrate comparison uses z-scores; coefficient point estimates are NOT directly comparable across the battery-vs-single-item operationalization.

### Issue 4 — Race relations

| Substrate | Variable(s) | Status | Scale |
|---|---|---|---|
| ANES 2024 | Dedicated race-relations item | Confirmed | Typically 4-pt or 5-pt |
| CES 2024 Common Content | Racial-attitudes battery (no dedicated "race relations" question) | DROPPED for Issue 4 (handled under Issue 3) | — |
| GSS 2024 | NOT PRESENT in 2024 (GSS RACDIF series + racial attitudes exist but coverage varies; verify) | TENTATIVE — confirm at implementation time | — |
| AP VoteCast 2024 | Covered by `RACISMUS` (no separate item) | Folded into Issue 3 | — |
| Pew VV 2024 | NOT PRESENT | — | — |

**Harmonization:** Z-standardize ANES single item. If GSS 2024 carries race-relations attitude items at implementation time, add and z-standardize; otherwise Issue 4 is ANES-only.

### Issue 5 — Science / arts funding (Tier 2)

| Substrate | Variable(s) | Status | Scale |
|---|---|---|---|
| ANES 2024 | Federal spending battery (science + arts items) | Confirmed | Typically 3-pt: too little / about right / too much |
| CES 2024 Common Content | NOT in Common Content (defense / welfare / environment / border are CES spending items, not science/arts) | DROPPED | — |
| GSS 2024 | `NATSCI` + `NATARTS` | Confirmed (core spending module) | 3-pt: too little / about right / too much |
| AP VoteCast 2024 | NOT PRESENT (no spending priorities battery) | DROPPED | — |
| Pew VV 2024 | NOT PRESENT | — | — |

**Harmonization:** GSS NATSCI/NATARTS coded as ordinal [-1, 0, +1] then z-standardized within substrate. ANES analog coded identically. Cross-substrate comparison on z-scores. Composite "science + arts" score = mean of NATSCI + NATARTS z-scores per respondent.

### Issue 6 — USAID / foreign aid (Tier 2)

| Substrate | Variable(s) | Status | Scale |
|---|---|---|---|
| ANES 2024 | Federal foreign aid spending item | Confirmed (USAID-adjacent, generic foreign aid spending) | 3-pt: too little / about right / too much |
| CES 2024 Common Content | NOT PRESENT | DROPPED | — |
| GSS 2024 | `NATAID` | Confirmed (core spending module) | 3-pt |
| AP VoteCast 2024 | NOT generic foreign-aid item; only `UKRAINEAID` + `ISRAELAID` exist (both country-specific) | DROPPED for Issue 6 (Israel-specific item already used in Issue 1; Ukraine-specific is out of scope) | — |
| Pew VV 2024 | NOT PRESENT | — | — |

**Harmonization:** Same as Issue 5. GSS NATAID and ANES foreign-aid spending coded as ordinal [-1, 0, +1] then z-standardized. Composite foreign-aid score = z-standardized single item per substrate.

## 2. Exposure-pool variable construction

### 2.1 Social media platform mix

**Definition (pre-reg §4):** Dominant-platform indicator with intensity = platform with highest frequency × political-content product among confirmed-used platforms; "low-use" if all platforms below threshold; "mixed" if no single platform exceeds 1.5x next-highest.

**Substrate-specific operationalization:**

- **ANES 2024:** Dichotomous platform indicators for FB, X/Twitter, Instagram, Reddit, YouTube, Snapchat, TikTok + frequency/political-posting for FB and X/Twitter. Constructed score: (FB_freq × FB_political) + similar for X. Other platforms enter as binary "ever uses" indicators in the dominance computation. Dominant-platform classification per pre-reg §4.
- **CES 2024 Common Content:** FB / X / YouTube confirmed; TikTok / Instagram coverage variable by 2024 — verify at codebook pull time. Less rich than ANES (no frequency × political-content interaction by default).
- **AP VoteCast 2024:** Only `TIKTOKUSER` available. Drop dominant-platform construction; record TikTok-user binary as substrate-limited proxy. Flagged in writeup.
- **Pew VV W159:** No platform items in this wave. Drop.

**Cross-substrate compatibility:** The 8-level dominant-platform variable is constructed at full granularity on ANES; CES uses a reduced version (3-5 platforms depending on what's in Common Content); AP VoteCast uses binary TikTok-user only. Cross-substrate exposure analysis is ANES-anchored.

### 2.2 Pay structure (hourly vs salary)

**Definition (pre-reg §8):** Imputed P(hourly | observables) from CPS ORG model. Logistic regression trained on PAIDHRE (paid hourly Y/N) in CPS ORG, applied to political-survey respondents with 50 multiple-imputation draws.

**Inputs needed per substrate to apply imputation model:**

- ANES 2024: occupation code (Census 2018 occ codes if reported at that granularity; else 2-digit major group), industry, age, gender, hours worked, weekly/annual earnings, education, region, race.
- CES 2024: employment status + industry — occupation depth varies by wave; verify at codebook pull. If only 2-digit major-group occupation, train imputation model at that granularity too (re-fit CPS ORG with reduced predictor set).
- AP VoteCast 2024: NO hourly/salary item AND no occupation codes at sufficient detail for imputation (income band + union HH + govt-worker binary only). Drop pay-structure exposure-pool analysis on AP VoteCast.
- Pew VV W159: no employment items in wave; drop.

**Fallback:** If ANES occupation coding doesn't match CPS coding at the (occ × ind) cell level, build a crosswalk via the Census 2018 OCC → Census 2018 OCC10 manual aggregation. Document crosswalk decisions at implementation time.

### 2.3 Insurance status

| Substrate | Variable | Categories |
|---|---|---|
| ANES 2024 | Confirmed present | Insured-private / insured-public / uninsured |
| CES 2024 Common Content | Confirmed present | Same 3-level categorical |
| GSS 2024 | Health insurance status (rotating; verify in 2024 codebook) | TBD |
| AP VoteCast 2024 | NOT PRESENT (policy-attitude items only) | DROP from Model B on AP VoteCast |
| Pew VV W159 | NOT PRESENT | DROP |

**Harmonization:** Three-level categorical. Public = Medicare or Medicaid (including dual-eligible); Private = employer or marketplace; Uninsured = no coverage. Mixed coverage (private + public, e.g., Medicare Advantage) coded as Public.

## 3. Cohort coding

### 3.1 Pew cohort cutoffs (LOCKED in pre-reg §1)

| Cohort | Birth year range | Age at Nov 2024 |
|---|---|---|
| Silent | ≤ 1945 | 79+ |
| Boomer | 1946-1964 | 60-78 |
| Gen X | 1965-1980 | 44-59 |
| Millennial | 1981-1996 | 28-43 |
| Gen Z | 1997-2012 | 12-27 (voting subset 18-27) |

Within-cohort splits (pre-reg §4): older/younger Millennial 1981-1988 vs 1989-1996; older/younger Boomer 1946-1954 vs 1955-1964. Used as secondary specification where cell N ≥ 50.

### 3.2 Per-substrate cohort coding feasibility

- **ANES 2024:** Birth year continuous → exact cohort coding + within-cohort splits feasible.
- **CES 2024:** Birth year continuous → exact coding feasible.
- **GSS 2024:** Birth year (COHORT variable) continuous → exact coding feasible.
- **AP VoteCast 2024:** Age BANDED (18-24 / 25-29 / 30-39 / 40-49 / 50-64 / 65+) per 2026-05-22 codebook pull. Continuous age / birth year suppressed for disclosure. **Approximate cohort mapping via the bands:**

| AP VoteCast band | Age at Nov 2024 | Pew cohort coverage | Approximation rule |
|---|---|---|---|
| 18-24 | 18-24 | Gen Z (entire band falls in Gen Z 12-27) | Code as Gen Z |
| 25-29 | 25-29 | Gen Z 25-27 (40%) + Millennial 28-29 (60%) | Code as Gen Z/Mill boundary; report sensitivity to alternate coding both ways |
| 30-39 | 30-39 | Millennial entire (28-43 contains 30-39) | Code as Millennial |
| 40-49 | 40-49 | Millennial 40-43 (40%) + Gen X 44-49 (60%) | Code as Mill/Gen X boundary; report sensitivity |
| 50-64 | 50-64 | Gen X 50-59 (~62%) + Boomer 60-64 (~38%) | Code as Gen X/Boomer boundary; report sensitivity |
| 65+ | 65+ | Boomer 65-78 (most) + Silent 79+ (some) | Code as Boomer; Silent under-represented in this band |

**AP VoteCast cohort coding decision rule (LOCKED):** Primary coding uses the modal cohort per band as listed above (e.g., 25-29 → Gen Z, 50-64 → Gen X). Boundary bands (25-29, 40-49, 50-64) get sensitivity re-analysis with the alternate-modal coding. Boundary disagreement reported in supplement as cohort-coding robustness check.

This is lossy; the approximation is documented and the substrate-specific results for AP VoteCast are flagged accordingly. **AP VoteCast is NOT the cohort-hypothesis primary substrate** — ANES + CES + GSS carry that load.

- **Pew VV 2024:** Age "detailed" via panel profile per 2026-05-22 questionnaire pull. Confirm at panel-profile join whether continuous birth year is available; if only banded, apply the same approximation rule.

## 4. Fundamentals baseline (LOCKED across A/B/C; pre-reg §4)

| Variable | Source | Coding |
|---|---|---|
| 2020 presidential vote recall | All political substrates | Biden / Trump / third-party / abstain |
| State partisanship | Cook PVI 2024 cycle | Continuous Cook PVI |
| State result margin 2024 | Federal Election Commission canvass | Continuous, Harris-Trump 2-party margin in % |
| Personal economic perception | All political substrates | 5-pt scale, standardized within substrate (item names vary) |
| Incumbency direction | Constructed | Binary: 1 if Democratic incumbent transition (Biden→Harris) |

State-level controls join via 2-letter state abbreviation + FIPS code (verify in each substrate at implementation time).

## 5. Z-standardization rules

- Within-substrate z-standardization for all issue items + economic-perception covariates BEFORE pooling.
- Cross-substrate effect-size comparison uses z-scores only. Raw scales reported in supplement tables for transparency.
- 7-pt vs 4-pt vs 3-pt vs 5-pt scales standardize differently in tail behavior; report standardized AND raw-scale coefficients in per-substrate effect tables.

## 6. Dataset access references

- **ANES 2024:** https://electionstudies.org/data-center/2024-time-series-study/ (free; full release 2025-08-08; codebook 2025-09-08)
- **CES 2024 Common Content:** https://dataverse.harvard.edu/dataset.xhtml?persistentId=doi:10.7910/DVN/X11EP6 (free public Dataverse)
- **AP VoteCast 2024 PUF:** https://apnorc.org/projects/ap-votecast-puf/ → ZIP `AP_VOTECAST_2024_GENERAL.zip` (99 MB; includes SAS + codebook PDF + questionnaire PDF)
- **Pew Validated Voters 2024:** https://www.pewresearch.org/dataset/ (registration-gated)
- **GSS 2024:** https://gssdataexplorer.norc.org/ (free public)
- **CPS ASEC 2025:** https://www.census.gov/data/datasets/2025/demo/cps/cps-asec-2025.html OR IPUMS-CPS https://cps.ipums.org/ (free)
- **CPS ORG (monthly outgoing rotation group):** Same Census site + IPUMS-CPS, monthly files; pull 2024 calendar year for pay-structure imputation training

## 7. Implementation-time wording verification

The pre-reg locks item PRESENCE (which items are in each substrate per the 2026-05-22 verification round). Exact question WORDING for ANES + CES + GSS items is to be confirmed at implementation time against the actual codebooks (the verification round used release announcements + summary documentation but did not pull every codebook page).

**Procedure at implementation:**
1. Pull each substrate's full codebook before model fitting.
2. Confirm item presence per this supplement's table entries.
3. Confirm exact wording matches the path map's intent for each issue.
4. If item is absent OR wording substantially differs from intent (e.g., the "structural inequity" item is actually a salience probe not an attitude measure), file pre-reg §12 deviation BEFORE proceeding with that substrate-issue combination.

Wording divergences are expected on the order of 1-2 items across the 6-issue × 4-substrate matrix; the pre-reg's hierarchical shrinkage handles modest measurement-construct heterogeneity. Substantial divergences (>2 items per substrate or any item that changes construct entirely) trigger a §12 deviation with explicit decision: drop the item, re-define operationalization, or proceed and flag.

---

**Locked alongside pre-reg v1.0 at the same commit.**
