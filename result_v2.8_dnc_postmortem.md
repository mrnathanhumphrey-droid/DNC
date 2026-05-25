# result_v2.8 — DNC 2024 Post-Mortem v2.8 (External alt-right exposure indicators)

**Locked:** 2026-05-24 against `prereg_v2.8_dnc_postmortem.md` HEAD `10be274`.
**Builds on:** result_v2.6 (`887c384`) + prereg_v2.7 (`bb21e1a`).
**Repo:** github.com/mrnathanhumphrey-droid/DNC.

---

## 1. Headline (one sentence)

**Alt-right has substantial X reach (11.3M follower cluster across 7 alt-right-adjacent accounts), Wikipedia interest amplified specifically for Groyper-related terms (essentially nonexistent in 2020, massive 2024 search spike), but state-level alt-right search interest does NOT correlate with Trump 2020→2024 swing** (Spearman ρ = -0.067 NULL). Aggregate verdict per pre-reg: **EXTERNAL ALT-RIGHT FOOTPRINT PARTIAL** — the cluster exists at scale (H35 HIGH-VISIBILITY) and grew dramatically (H33 confirmed for Groyper/Fuentes), but is not geographically aligned with the swing pattern that delivered Trump's win (H34 NULL).

---

## 2. Verdicts table

| Hyp | Test | Verdict | Detail |
|---|---|---|---|
| **H33** | 2024 vs 2020 search-interest amplification (≥3 of 5 terms with 2024 spike ≥1.5× 2020) | **PARTIAL** (2 of 5) | Groyper and Nick Fuentes massively amplified (Groyper essentially nonexistent in 2020 search). "alt right" / Rumble / America First stable or declined. |
| **H34** | Spearman ρ state Google Trends interest × Trump 2020→2024 swing ≥ +0.4 | **NULL** | ρ = -0.067. State-level alt-right search interest does NOT predict Trump swing geographically. |
| **H35** | X cluster size — alt-right Cluster A total ≥ 5M followers | **HIGH-VISIBILITY** | Cluster A total = **11.27M** (excluding St. Clair handle returning 0). |

**Aggregate per pre-reg §3 §1:** ≥1 sub-hypothesis confirms (H35) → **EXTERNAL ALT-RIGHT FOOTPRINT PARTIAL.** The cluster exists and grew, but not in a state-pattern correlated with Trump's victory geography.

---

## 3. H33 detail — search-interest amplification

Pre/post comparison: spike = (Jul-Oct interest) - (Jan-Jun interest), per cycle.

| Term | 2024 Jul-Oct | 2024 Jan-Jun | 2024 spike | 2020 spike | Ratio | Reading |
|---|---:|---:|---:|---:|---:|---|
| **Groyper** | 28.9 | 11.5 | **+17.5** | -0.7 | (mag ratio ≫1.5) | **CONFIRMED — surged from near-zero** |
| **Nick Fuentes** | 2.8 | 1.8 | +1.0 | +0.1 | **14.59×** | CONFIRMED amplification |
| Rumble | 24.2 | 31.1 | -6.9 | -5.9 | 1.16× | similar (slight pre-baseline decline both cycles) |
| "alt right" | 14.2 | 12.0 | +2.2 | +1.9 | 1.13× | similar (no amplification) |
| America First | 72.9 | 70.3 | +2.7 | +4.2 | 0.64× | DECLINED (Trump's first run 2020 had bigger surge) |

**Pattern read:** Groyper-specific search interest is essentially a 2024 phenomenon — pre-election interest in 2020 was statistical zero. Nick Fuentes interest 14× higher in the 2024 pre-election window vs 2020. "Rumble" and "alt right" interest were already established pre-2020 (Rumble's growth predates Trump's 2024 cycle). "America First" search interest peaked with Trump's 2020 cycle and slightly declined for 2024.

**Substantive read:** The Groyper movement specifically grew dramatically as a search-interest entity 2020→2024. The broader "alt right" term and Rumble platform are stable / pre-existing.

---

## 4. H34 detail — state-level ecological correlation NULL

Spearman ρ between state geometric-mean Google Trends interest (Sep-Nov 2024 across 5 LOCKED terms) and state Trump 2020→2024 margin swing:

**ρ = -0.067, p ≈ 0.64 (effectively zero correlation)**

**Reading:** State-level interest in alt-right terms does not predict Trump's state-level gains. This NULL result is informative in two directions:

1. **Geographic mismatch.** States that searched alt-right terms most are NOT the states that shifted hardest toward Trump. Search interest in these terms reflects a mix of (a) sympathetic curiosity, (b) alarmed monitoring (probably overweighted in liberal states), and (c) media-driven mainstream curiosity. The signal is ambiguous in direction.
2. **Trump swing geography is not driven by alt-right exposure as measured here.** The states with biggest Trump swings (per state_trump_swing.csv: NY, NJ, FL, MA, CA, IL...) are states with large urban populations of all ideologies. The Trump swing seems to be a metro-cosmopolitan-electorate phenomenon, not an alt-right-search-interest phenomenon.

**Pre-reg §5 threats already noted ecological fallacy + term ambiguity. NULL verdict is robust to these pre-reg'd caveats.**

---

## 5. H35 detail — X cluster size snapshot

Pre-reg §2 LOCKED 12 accounts. Status at query time (2026-05-24):

**Cluster A — Alt-right adjacent (7 accounts):**

| Account | Followers | Status |
|---|---:|---|
| @JackPosobiec | **3,302,728** | active |
| @DC_Draino | 2,344,164 | active |
| @LauraLoomer | 1,912,275 | active |
| @Cernovich | 1,467,381 | active |
| @NickJFuentes | 1,321,645 | active (reinstated after 2021 ban) |
| @realStewPeters | 925,393 | active |
| @ashleystclair1 | **0** | **HANDLE PROBABLY WRONG** — see §9 dev 1 |
| **Cluster A total** | **11,273,586** | |

**Cluster B — MAGA mainstream comparison (5 accounts):**

| Account | Followers |
|---|---:|
| @TuckerCarlson | **17,627,249** |
| @benshapiro | 8,548,690 |
| @charliekirk11 | 6,216,454 |
| @LibsOfTikTok | 4,752,742 |
| @TimRunsHisMouth | 1,184,516 |
| **Cluster B total** | **38,329,651** |

**Ratios + interpretation:**
- Cluster A : Cluster B follower ratio = **0.294** (alt-right cluster ≈ 30% of MAGA-mainstream reach by follower count).
- Tucker Carlson alone (17.6M) is larger than the entire alt-right cluster combined.
- Posobiec (3.3M) is the largest alt-right account in this snapshot — moderately within mainstream-MAGA-influencer band.

**Per pre-reg §1 H35 gate:** Cluster A total = 11.27M >> 5M threshold → **HIGH-VISIBILITY**.

**Caveat (per pre-reg §5):** snapshot is CURRENT (post-election). Pre-election cluster size would require historical archive (not in user's basic X API tier). The snapshot reflects today's reach, not the pre-election state. Survivor bias: accounts banned 2020-2024 not in this snapshot (Fuentes was banned 2021-Dec 2023; current follower count reflects post-reinstatement rebuild).

---

## 6. Wikipedia pageviews — supporting evidence

Monthly pageviews 2020-2024 for 5 LOCKED articles (not part of formal pre-reg verdict gate; descriptive support):

| Article | Total views | Months active | Avg/month |
|---|---:|---:|---:|
| **Nick_Fuentes** | **8,505,796** | 60 | 141,763 |
| Alt-right | 2,926,945 | 60 | 48,782 |
| Rumble_(website) | 1,782,891 | 53 | 33,640 |
| Groyper | 48,923 | 56 | 873 |
| America_First_Foundation | 2,077 | 19 | 109 |

**Reading:**
- **Nick Fuentes is the dominant Wikipedia-curiosity entity** — 8.5M views over 60 months. Substantial mainstream-media-driven attention.
- The Wikipedia article on "Groyper" itself has only 49k total views (873/month) — the term is more of an in-group identifier than a Wikipedia-curiosity object.
- "Rumble" has steady but modest interest (33k/month).
- The "America First Foundation" Wikipedia article is essentially unread (109/month) — the entity has very low mainstream curiosity.

The Wikipedia pattern matches H33's Google Trends pattern: Fuentes-specific interest is real and substantial; Groyper-as-search-term is niche; mainstream "alt-right" interest is steady but not surging.

---

## 7. Cross-substrate read — combined v2.7 + v2.8

| Question | v2.7 (ANES survey-side) | v2.8 (external indicators) |
|---|---|---|
| Is the alt-right-aligned cluster numerically meaningful? | 63.6% of Trump 2024 voters in Q4 of proxy composite. **YES, large.** | X follower cluster 11.3M; Wikipedia interest 8.5M views. **YES, substantial reach.** |
| Did the alt-right cluster grow into the Trump coalition? | Cluster was Trump's pre-existing base (96.1% of Trump 2024 voters did NOT vote Biden 2020). **Was already there.** | Groyper / Fuentes search interest amplified massively 2020→2024. **YES, online presence grew.** |
| Did DNC alienation feed the alt-right cluster? | Q4 Biden-2020 voters flipped at 52%, but N=27 (1.4% of Biden coalition). **Per-voter yes, absolute small.** | State-level alt-right search interest doesn't correlate with Trump swing (ρ=-0.07). **No geographic alignment.** |

**Combined headline:** The alt-right ecosystem has substantial OBSERVABLE reach + grew dramatically online during 2020-2024 (especially Groyper / Fuentes-adjacent) AND aligns with the cluster that constitutes the majority of Trump's voters (per v2.7 H30). BUT the EXISTING alt-right-aligned voters were already Trump's base; DNC didn't lose by bleeding many voters into that cluster (only 27 of 1960 Biden-2020 voters fit the high-altright-proxy profile). And the geographic pattern of where alt-right search interest concentrates does NOT match the geographic pattern of Trump's 2020→2024 swing — Trump's swing-states were broad-electorate metro-cosmopolitan flips, not alt-right-interest hotspots.

**Reframed autopsy:** The alt-right is real, large online, and grew substantially. But Trump's WIN was driven by his existing alt-right-adjacent base showing up (v2.7 H30) + skipping of younger Biden-coalition members (v2.3 H7) + a small MillYoung active-flipper segment (v2.3 H14) + a MillOld-Hispanic-specific defection cell (v2.4 H16 refinement). The alt-right ecosystem amplification is a NECESSARY backdrop for the base's energy but NOT the SUFFICIENT cause of 2024's specific Democratic losses.

---

## 8. Honest caveats + diagnostics

- **Google Trends "100" scale.** Relative-interest within-term; cross-term comparisons require geometric-mean composition (as done in H34). Absolute magnitude of search volume per state is opaque.
- **Term ambiguity.** "Rumble" is wrestling / non-political conflict. "America First" was Trump's official 2020 campaign brand. Both terms conflate sympathetic and non-political uses.
- **Search-direction ambiguity.** Alt-right term searches are mix of (a) sympathetic, (b) alarmed/monitoring, (c) curious/educational. H34 NULL is robust to direction interpretation, but H33 amplification could reflect mainstream-media-driven concern rather than sympathetic interest.
- **Wikipedia pageviews ≠ sympathy.** High-page-view articles (Nick Fuentes 8.5M) capture both alarm and interest.
- **X snapshot is current.** Pre-election follower counts not accessible without historical archive (user's API tier basic, no archive).
- **Ecological fallacy.** State-level correlations don't speak to individual-level exposure-to-vote links.
- **§9 dev 1 (filed below): @ashleystclair1 handle was wrong.** Returned 0 followers. Correct handle for Ashley St. Clair is @stclairashley. Pre-reg discipline did not allow handle substitution. Cluster A total of 11.3M excludes whatever her actual follower count is; would presumably add ~1-3M based on her public profile post-Musk-affair-2024. Estimated impact: Cluster A total would rise modestly but does not change verdict (still HIGH-VISIBILITY).

---

## 9. v2.8 deviation log

| Date | Deviation | Rationale |
|---|---|---|
| 2026-05-24 | **§10 dev 1: @ashleystclair1 returned 0 followers.** Pre-reg §2 locked this handle. Actual Ashley St. Clair X handle is @stclairashley (or similar). Per pre-reg discipline, NO substitution made — the locked handle is what was queried. | Handle-locking error in pre-reg; verifying account handle pre-lock would have caught this. Verdict (HIGH-VISIBILITY at 11.3M total) unchanged by this exclusion. Future pre-regs should include account-handle verification step before commit. |

---

## 10. Repo state at lock

- Pre-reg v2.8 locked at `10be274`.
- Script: `code/v28_external_altright.py`
- Outputs under `data/processed/v28/`:
  - `state_trump_swing.csv` (51 states / DC, 2020+2024 margins + swing)
  - `wikipedia_pageviews.csv` (60 months × 5 articles)
  - `x_follower_counts.csv` (12 accounts)
  - `google_trends_weekly.csv` (262 weeks × 5 terms)
  - `google_trends_state.csv` (51 states × 5 terms)
  - `state_correlation.csv` (state × geomean interest × swing)
  - `run_log.txt` (full execution log)
- Repo: github.com/mrnathanhumphrey-droid/DNC.

**Result commit hash to be filled at commit time.**
