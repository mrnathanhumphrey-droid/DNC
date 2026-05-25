# Pre-registration v2.7 — DNC 2024 Post-Mortem (Alt-right-aligned voter composite — survey-side, ANES)

**Locks BEFORE running v2.7 analyses.** Builds on:
- result_v2.3 (HEAD `d810d63`): MillYoung is the qualitatively-distinct active-flipper cell.
- result_v2.6 (HEAD `887c384`): 12 mediators ruled out; cohort signal residual.

**Motivation.** Per user direction 2026-05-24: "*can we see HOW much of an impact the white supremacists and alt right had FOR trump?*" + "*that should be part of it too even if it wasnt the DNC who did it. it kinda is by alienating them.*" Tests whether the alt-right-aligned voter cluster — identified via canonical proxies (racial resentment + immigration hardlining + alt-right-belief-register) — was (a) a numerically-meaningful slice of Trump's 2024 vote, (b) over-represented among Biden-2020 defectors, especially in MillYoung, and (c) what % of Trump's margin is attributable to that cluster.

**Explicit naming caveat:** "alt-right" is operationalized as a *belief-cluster proxy* in ANES items — racial resentment + immigration restrictionism + Trump-grievance frame + anti-DEI/academic backlash. ANES has NO direct alt-right or white-supremacist self-identification item; the composite captures racial-attitudes-aligned populism, which OVERLAPS with alt-right rhetoric but is NOT a self-identified-alt-right indicator. Verdicts read against the composite explicitly as "alt-right-PROXY" cluster, not "alt-right voters."

---

## 0. What this pre-reg LOCKS

- Item list + directions for the alt-right-proxy composite
- 3 sub-hypotheses (H30 volume, H31 alienation, H32 counterfactual contribution)
- Stratification + reporting format

**What this pre-reg does NOT lock:**
- Cross-substrate replication (ANES only — CES has partial composite via CC24_441 + CC24_321/323 but item-mapping differs)
- Causal interpretation
- External-data-source confirmation (handled in pre-reg v2.8)

---

## 1. Composite construction (LOCKED — items + directions)

All standardized so **HIGHER = MORE ALT-RIGHT-PROXY-ALIGNED**.

### 1.1 Racial resentment sub-composite (4 items, already constructed v2.0.1 canonical direction)

`rr_composite_z` = z-score of mean(rr_workway, rr_genrtns, rr_deserve, rr_tryharder) from V242300-V242303 (Kinder-Sanders, canonical: HIGH = MORE resent).

### 1.2 Immigration restrictionism sub-composite (3 items, summary x-vars)

For each item, verify likert direction at impl time; reverse if needed so HIGH = MORE restrictionist:
- V241389x (favor/oppose ending birthright citizenship) — HIGH on raw = OPPOSE; **REVERSE so HIGH = favor ending birthright = restrictionist**
- V241392x (should children-brought-illegally be sent back or stay) — direction TBV at impl; if HIGH = "allowed to stay", REVERSE; if HIGH = "sent back", KEEP
- V241395x (favor/oppose border wall) — HIGH on raw = OPPOSE wall; **REVERSE so HIGH = favor wall = restrictionist**

`immigration_z` = z-score of mean of the 3 items after direction-alignment.

### 1.3 Trump-grievance sub-composite (3 items)

- V241353x (Trump treated unfairly) — direction TBV; align so HIGH = agree Trump treated unfairly = alt-right-aligned
- V241350x (president immune from prosecution) — align so HIGH = favor immunity
- V241344x (corruption increased under Biden) — align so HIGH = increased

`grievance_z` = z-score of mean of the 3 items after direction-alignment.

### 1.4 Anti-DEI / anti-academic sub-composite (2 items)

- V241290x (DEI approval) — direction TBV; align so HIGH = oppose DEI
- V241287x (colleges run approval) — direction TBV; align so HIGH = oppose how colleges are run

`anti_dei_z` = z-score of mean of the 2 items after direction-alignment.

### 1.5 Top-level composite

`altright_proxy_z` = z-score of mean(rr_composite_z + immigration_z + grievance_z + anti_dei_z) — all four sub-composites equal-weighted at the z-score level, then z-scored.

Missing-data handling: respondent must have at least 2 of the 4 sub-composites non-missing to be included; missing sub-composites mean-imputed to 0 before averaging. Per-item negatives (-9, -8, -1, etc.) treated as missing per sub-composite construction.

**LOCKED interpretation thresholds:**
- HIGH cluster = top quartile (Q4) of `altright_proxy_z`
- LOW cluster = bottom quartile (Q1)

---

## 2. Hypotheses (LOCKED)

### H30 — VOLUME: what fraction of Trump 2024 voters scored HIGH on alt-right-proxy?

**Test:** Among ANES respondents with V242096x ∈ {1, 2} (2-party voters), cross-tab Q4-alt-right-proxy × 2024-vote, weighted appropriately (use V200010c post-weight if available; else unweighted).

**Reporting:**
- % of Trump 2024 voters in Q4 of altright_proxy_z
- % of Harris 2024 voters in Q4
- % of Q4 voters who voted Trump (the conditional)

**Falsification gates (descriptive — no formal gate, but pre-reg expected pattern):**
- EXPECTED: Q4 cluster strongly Trump-favoring; ≥70% of Q4 voted Trump.
- CONFIRMED-LARGE-VOLUME: ≥40% of Trump voters in Q4.
- CONFIRMED-MEDIUM: 25-40% in Q4.
- LIMITED-VOLUME: <25% in Q4 (Trump win was NOT predominantly alt-right-proxy-aligned).

### H31 — ALIENATION: were Biden-2020 high-altright-proxy voters more likely to flip Trump in 2024?

**Subset:** ANES Biden-2020 recall voters (V241104 == 1) AND 2024 2-party voter (V242096x ∈ {1, 2}).

**Test:** Compute flip-to-Trump rate among Biden-2020 voters, stratified by altright_proxy_z quartile + by cohort (5-level Silent/Boomer/GenX/Mill/GenZ).

**Falsification gates:**
- **CONFIRMED (DNC alienation thesis):** Q4-cluster Biden-2020 voters have flip-to-Trump rate ≥ 20pp higher than Q1-cluster, AND effect concentrated in MillYoung/Mill cohort (cohort × quartile interaction in the descriptive cross-tab).
- **PARTIAL:** rate ≥ 10pp higher but no clear cohort concentration.
- **REFUTED:** rate within 10pp.

### H32 — COUNTERFACTUAL CONTRIBUTION: what % of Trump's 2024 ANES vote share is attributable to Biden-defector × high-altright-proxy cell?

**Decomposition (descriptive arithmetic):**
- A. Always-Republican Trump-2024 voters = N where (recall20 != biden AND V242096x == 2).
- B. Biden-2020 defectors to Trump in Q4-altright-proxy = N where (V241104 == 1 AND V242096x == 2 AND altright_proxy_z ≥ Q4-threshold).
- C. Biden-2020 defectors to Trump NOT in Q4 = N where (V241104 == 1 AND V242096x == 2 AND altright_proxy_z < Q4-threshold).
- D. Other Trump voters (non-2020-voter, third-2020, etc.) = remainder.

**Reporting:** weighted % of Trump's 2024 ANES vote share contributed by each cell B, C, D.

**Falsification gates:**
- **HIGH-CONTRIBUTION:** cell B (alt-right-proxy ex-Biden defectors) ≥ 10% of Trump's vote.
- **MEDIUM-CONTRIBUTION:** 3-10%.
- **LOW-CONTRIBUTION:** <3% — alt-right-proxy ex-Biden defectors are a small contributor in raw numbers.

### Aggregate verdict

- **ALT-RIGHT-PROXY MATTERED LARGELY:** H30 CONFIRMED-LARGE + (H31 CONFIRMED OR PARTIAL) + H32 HIGH-or-MEDIUM.
- **ALT-RIGHT-PROXY EXISTS BUT BIDEN-COALITION-PORTION SMALL:** H30 confirms volume but H31 + H32 show defector subset is small.
- **CLUSTER NOT NUMERICALLY DOMINANT:** H30 LIMITED-VOLUME.

---

## 3. Operationalization

### 3.1 Sample frame

ANES 2024, V242096x ∈ {1, 2} for H30. For H31/H32, subset to V241104 valid 2020 recall.

### 3.2 Tools

Pure pandas cross-tabs + arithmetic. NO Stan fit (descriptive analysis only, per pre-reg discipline — formal Stan mediation would be the v2.7-extended Stan version, but the descriptive 3-sub-hypothesis test is sufficient at this stage).

### 3.3 Weighting

V200010c (ANES 2024 post-weight if applicable; else V200010 pre-weight). If neither is the right v2.0-vintage variable, use the weight already used in v2.0 H4 sample construction (unweighted in current data_prep.py).

---

## 4. Threats to validity

- **Proxy ≠ identity.** Composite captures racial-attitudes-aligned populism. Voters scoring HIGH may or may not self-identify as alt-right; composite is a *behavioral-attitudes* signal not a *self-id* signal.
- **Direction-alignment review at impl time.** The pre-reg locks the ITEMS but DIRECTIONS depend on raw value coding. Will be verified pre-construction. §10 dev filed if any direction reversal differs from this lock.
- **Quartile thresholds are sample-specific.** Q4 cutoffs derived from THIS sample's composite distribution. Cross-substrate replication would use different cutoffs.
- **ANES self-report of vote.** V242096x is self-reported, not validated. Some Biden-2020 → Trump-2024 self-reports may be misremembered; rate of misremembering is modest in ANES (~5-10% per validation studies).
- **No causal claim.** Composite cluster correlates with Trump vote; this is associational, not causal.

---

## 5. v2.7 deviation log

| Date | Deviation | Rationale |
|---|---|---|

(Empty at lock; populated as v2.7 work surfaces discrepancies.)

---

**Locked at commit:** `[fill at commit]` on `main`.
**Repository:** https://github.com/mrnathanhumphrey-droid/DNC.
**Builds on:** result_v2.3 (d810d63) + result_v2.6 (887c384).
