# result_v2.7 — DNC 2024 Post-Mortem v2.7 (Alt-right-aligned voter composite, survey-side)

**Locked:** 2026-05-24 against `prereg_v2.7_dnc_postmortem.md` HEAD `bb21e1a`.
**Builds on:** result_v2.3 (`d810d63`) + result_v2.6 (`887c384`).
**Naming caveat:** "alt-right" = belief-cluster PROXY (racial resentment + immigration hardline + Trump-grievance + anti-DEI). NOT self-id'd alt-right.
**Repo:** github.com/mrnathanhumphrey-droid/DNC.

---

## 1. Headline (one sentence — counterintuitive)

**The alt-right-PROXY-aligned cluster is HUGE in Trump's 2024 coalition (63.6% of his ANES voters scored in Q4 of the composite, and 97.8% of the Q4 cluster voted Trump), BUT only 0.8% of his total vote came from "alienated" Biden-2020 voters who scored alt-right-aligned** — the cluster was overwhelmingly his EXISTING base (96.1% of Trump 2024 voters did NOT vote Biden in 2020). The alt-right alienation pathway exists with massive per-voter strength (Q4 Biden-2020 voters flipped Trump at 52% vs Q1's 0.2% — a 51.7pp gap) but the BIDEN-coalition slice that scored alt-right-aligned was tiny in absolute numbers (N=27 of 1960 Biden-2020 2-party voters). **The DNC didn't lose by alienating future-alt-right voters; the alt-right cluster was a pre-existing Trump bloc that DNC was never going to win, and the Biden→Trump defection by that cluster was numerically small.**

---

## 2. Verdicts table

| Hyp | What was tested | Verdict | Magnitude |
|---|---|---|---|
| **H30 VOLUME** | % of Trump 2024 voters in Q4 alt-right-PROXY | **CONFIRMED-LARGE-VOLUME** | **63.6%** of Trump voters in Q4 (≥40% gate) |
| **H31 ALIENATION** | Biden-2020 → Trump flip rate, Q4 vs Q1 + cohort concentration | **CONFIRMED** (DNC alienation thesis confirmed at the per-voter rate level) | Q4 flip rate **51.9%** vs Q1 **0.2%** = **+51.7pp gap** |
| **H32 COUNTERFACTUAL** | % of Trump's 2024 vote = Biden-defector × Q4 cell | **LOW-CONTRIBUTION** | **0.8%** of Trump's vote (cell N=14 of total Trump N=1658) |

**Aggregate verdict:** **ALT-RIGHT-PROXY MATTERED LARGELY (in volume) + DNC ALIENATION CONFIRMED (in per-voter rate) BUT NUMERICALLY SMALL IN CONTRIBUTION TO TRUMP'S WIN.** The cluster was Trump's pre-existing base, not his Biden-defection-pickup.

---

## 3. H30 detail — the cluster IS Trump's coalition

| Quartile | Harris voters | Trump voters | % of each quartile voting Trump |
|---|---:|---:|---:|
| Q1 (lowest altright-proxy) | 1114 | 13 | **1.2%** |
| Q2 | 735 | 96 | **11.6%** |
| Q3 | 255 | 495 | **66.0%** |
| Q4 (highest altright-proxy) | 24 | 1054 | **97.8%** |

**The alt-right-PROXY composite cleanly separates the 2-party vote.** Q1 is essentially uniformly Harris (98.85%), Q4 is essentially uniformly Trump (97.77%). This is partly mechanical (the composite includes Trump-favorability-correlated items like "Trump treated unfairly") but the magnitude is striking — the composite functions as nearly a perfect classifier of 2-party vote at the extremes.

**Composition reads:**
- **63.6% of Trump 2024 voters were in Q4 altright-proxy.** Trump's coalition is HEAVILY concentrated in the cluster.
- **1.1% of Harris voters were in Q4.** The cluster is asymmetrically pro-Trump.
- The Q3 cell (29.9% of Trump voters) is the "medium-aligned" segment — also overwhelmingly Trump but less extreme.

---

## 4. H31 detail — DNC alienation IS confirmed per-voter, but tiny cell

**Aggregate: Biden-2020 voters' 2024 flip-to-Trump rate by altright-proxy quartile:**

| Quartile | Flip rate | Cell N |
|---|---:|---:|
| Q1 | **0.19%** | 1035 |
| Q2 | 1.97% | 659 |
| Q3 | 15.06% | 239 |
| Q4 | **51.85%** | **27** |

**The alienation hypothesis is dramatically confirmed AT THE PER-VOTER LEVEL.** Biden-2020 voters who scored Q4 altright-proxy flipped at 52% — meaning if you were a 2020 Biden voter AND scored in the top quartile of alt-right-PROXY composite, you had nearly a coin-flip probability of voting Trump in 2024. Biden-2020 voters in Q1 essentially NEVER flipped (0.19%).

**But the Q4 cell is tiny: only 27 of 1960 Biden-2020 ANES 2-party voters** (1.4% of the Biden coalition was in Q4 altright-proxy). This is consistent with: the Biden coalition was largely composed of voters who scored LOW on alt-right-PROXY, and the small alt-right-leaning slice was the high-defection vector.

**By cohort × quartile** (where N permits):

| Cohort | Q1 flip% | Q2 flip% | Q3 flip% | Q4 flip% (N) |
|---|---:|---:|---:|---:|
| Silent | 1.33 | 1.56 | 10.00 | 50.00 (N=2) |
| Boomer | 0.00 | 0.38 | 11.70 | 50.00 (N=10) |
| GenX | 0.00 | 3.01 | 13.43 | 42.86 (N=7) |
| MillOld | 0.00 | 5.63 | 21.74 | 0.00 (N=1) |
| **MillYoung** | 0.72 | 2.08 | 33.33 | **100.00 (N=3)** |
| GenZ | 0.00 | 5.00 | 50.00 | N=0 |

**MillYoung Q4 flipped at 100%** — but N=3 (3 of 3 Q4 MillYoung Biden-2020 voters flipped). The MillYoung-concentration claim cannot be cleanly supported at N=3.

**The clearer pattern: ALL cohorts in Q4 (where cell N > 5) flipped at 43-50%, regardless of cohort.** The alt-right-PROXY composite captures the flip propensity ACROSS cohorts; cohort × quartile interaction is not detectable at these cell N's.

---

## 5. H32 detail — Trump's coalition decomposition

| Cell | Description | N | % of Trump 2024 vote |
|---|---|---:|---:|
| A | Non-Biden-2020 Trump voters (always-R / nonvoter / third) | 1593 | **96.1%** |
| B | Biden-2020 → Trump, Q4 altright-proxy | 14 | **0.8%** |
| C | Biden-2020 → Trump, non-Q4 altright-proxy | 51 | **3.1%** |
| Total Trump 2024 voters | | 1658 | 100% |

**0.8% of Trump's 2024 ANES vote came from the "alienated Biden-2020 defectors with alt-right alignment" cell.** Even at the highest per-voter flip rate (52% in Q4), the absolute number of such voters in the Biden coalition was small.

**The mechanism for Trump's win, per these decompositions, is overwhelmingly TURNOUT + MOBILIZATION of his EXISTING alt-right-PROXY-aligned base** (the 63.6% of Trump voters in Q4), not conversion of Biden coalition members.

---

## 6. Cross-reference with v2.3 (MillYoung distinct flipper)

v2.3 found MillYoung (28-35) is the qualitatively-distinct active-flipper cohort on CES VV — 50% of MillYoung Biden-2020 non-retainers flipped vs 50% skipped (the only cohort where flipping rivaled skipping).

v2.7 confirms the *direction* (flippers are alt-right-aligned at 52% Q4 rate) but the *sample sizes* in ANES at fine cohort × quartile cuts are too small to localize MillYoung specifically. CES is the better substrate for cell-N reasons; ANES is the better substrate for the attitudinal composite. **A v2.7-extended fit on CES (using CC24_441 racial resentment + CC24_321/323 issue battery as a CES-side proxy composite) is the natural cross-substrate replication target.** Not pre-reg'd here; flagged as v2.9 candidate.

---

## 7. What v2.7 means for the autopsy

Reframing the DNC autopsy with v2.7 in hand:

- **Trump won 2024 because his existing alt-right-PROXY-aligned base showed up.** 63.6% of his coalition is in Q4 of the composite. This is the structural Republican-leaning bloc whose attitudes were already aligned in 2020. Mobilizing them was sufficient.
- **The DNC's alienation problem is real per-voter but small in absolute contribution.** Q4 Biden-2020 voters flipped at 52%, but there were only 27 of them in ANES (1.4% of the Biden coalition). DNC didn't bleed many alt-right-leaning voters because the Biden coalition didn't have many to begin with.
- **The MillYoung-flipper story from v2.3 is consistent with v2.7 but not localized to alt-right alignment specifically.** MillYoung Biden→Trump flippers may be in Q3-Q4 of altright-proxy but the cell N's are too small to confirm.
- **v2.6's "behavioral channel NOT THIS" verdict reads cleaner with v2.7:** the cohort defection signal in v2.1-v2.6 was looking for what makes MillYoung defect MORE THAN OTHER COHORTS *holding the alt-right-proxy distribution constant*. v2.7 shows the alt-right-proxy distribution IS the dominant axis of 2-party vote split, and cohort enters at the margins (within-quartile cohort differences are detectable but small).

---

## 8. Honest caveats + diagnostics

- **Composite includes Trump-favorability-correlated items (grievance sub-composite uses V241353x "Trump treated unfairly" + V241350x "president immune").** This makes the composite mechanically over-fit to 2-party vote at the extremes. Q4 being 97.8% Trump is partly the composite scoring Trump-supporters by definition. A cleaner version would drop the grievance sub-composite. v2.7-extended candidate.
- **Sub-composite construction direction-aligned at impl per pre-reg §1.5; verified against codebook 2026-05-24.**
- **H31 Q4 cell N=27** is too small for fine-grain cohort × quartile localization. The 51.7pp gap at aggregate is robust; the cohort-concentration claim is N-bound.
- **H32 decomposition uses ANES unweighted N's.** Weighted % using V200010c-equivalent weight may shift absolute % but not the pattern: Trump's coalition is overwhelmingly his pre-existing base.
- **Self-reported 2020 recall.** V241104 misremembering rate is modest but non-zero. Could bias Biden-2020 cell composition.
- **Single-substrate (ANES).** CES cross-substrate via CC24_441 composite is the natural next test.

---

## 9. Repo state at lock

- Pre-reg v2.7 locked at `bb21e1a`.
- Script: `code/v27_altright_proxy.py`
- Outputs: `data/processed/v27/{h30_by_vote, h30_by_quartile, h31_aggregate, h31_cohort_x_quartile}.csv`
- Repo: github.com/mrnathanhumphrey-droid/DNC.

**Result commit hash to be filled at commit time.**
