# Pre-registration v2.8 — DNC 2024 Post-Mortem (External alt-right exposure indicators)

**Locks BEFORE any external-data query.** Builds on:
- result_v2.6 (HEAD `887c384`): 12 mediators ruled out; remaining channels include "right-wing media exposure" (data-blocked in ANES public release).
- pre-reg v2.7 (HEAD `bb21e1a`): ANES-survey-side alt-right-PROXY composite.

**Motivation.** Per user direction 2026-05-24: "*can we find any alt right signals? with rumble or the rise of that groyper fuck? id love to see all 3. but i want data on the alt right and how to measure it. i think SM followers for the groypers or ashley sinclair is an option. media mentions of 'alt right' or 'groyper' or 'rumble' or some other terms??*" PLUS: user has X API access in DeepDive env (`TWITTER_BEARER_TOKEN`, $0.01/user-lookup).

v2.7 measures the SURVEY-SIDE alt-right-aligned voter cluster. v2.8 measures the EXTERNAL alt-right exposure ecosystem via:
1. Google Trends search-interest time-series (state-level)
2. Wikipedia pageviews time-series
3. X/Twitter current follower counts for cluster of alt-right-adjacent accounts (snapshot — historical follower-count growth requires gated archive access not in user's tier)

Tests whether the EXTERNAL alt-right cluster has measurable footprint correlated with the SURVEY-SIDE cluster + with state-level Trump 2020→2024 swing.

---

## 0. What this pre-reg LOCKS

- Term list for Google Trends + Wikipedia (LOCKED §1)
- X account list (LOCKED §2 — MUST be locked before X API call per pre-reg discipline)
- Time window
- 3 sub-hypotheses (H33-H35)
- Verdict gates

**What this pre-reg does NOT lock:**
- Historical X follower-count time-series (requires Pro-tier X API archive access; user has basic tier)
- Rumble user data (no public API)
- Individual-level alt-right-exposure × vote (no public data source)

---

## 1. Term list — Google Trends + Wikipedia (LOCKED)

### 1.1 Google Trends query terms

Time window: **2020-01-01 to 2024-12-31** (covers both election cycles).
Geography: **US, state-level resolution**.

**Terms (LOCKED):**
- `"Groyper"`
- `"Nick Fuentes"`
- `"Rumble"` (will be ambiguous with non-political "rumble" uses — caveat)
- `"alt right"` (with space; common form)
- `"America First"` (Fuentes's political organization brand)

5 query terms. Pull weekly-resolution time-series + state-level overall (Sep-Nov 2024 average).

### 1.2 Wikipedia article pageviews

Articles (Wikipedia titles, LOCKED):
- `Nick_Fuentes`
- `Groyper`
- `Rumble_(website)`
- `Alt-right`
- `America_First_Foundation`

Wikipedia Pageviews API: monthly counts 2020-01 to 2024-12. No state-level granularity.

---

## 2. X account list (LOCKED — MUST be locked before query)

**Cluster A — Alt-right adjacent (Groyper + America-First-adjacent):**
- `@NickJFuentes` (Nick Fuentes — Groyper leader; account variously banned/reinstated)
- `@ashleystclair1` (Ashley St. Clair — late-2024 right-wing pundit)
- `@cernovich` (Mike Cernovich — earlier alt-right wave)
- `@JackPosobiec` (Jack Posobiec — Pizzagate / America First adjacent)
- `@realStewPeters` (Stew Peters — far-right podcaster)
- `@LauraLoomer` (Laura Loomer — anti-Muslim far-right)
- `@DC_Draino` (Rogan O'Handley — MAGA far-right legal commentator)

**Cluster B — MAGA mainstream (control / boundary):**
- `@charliekirk11` (Charlie Kirk — TPUSA, MAGA mainstream)
- `@TimRunsHisMouth` (Tim Pool — populist/contrarian, edge case)
- `@benshapiro` (Ben Shapiro — mainstream conservative)
- `@TuckerCarlson` (Tucker Carlson — populist-right post-Fox)
- `@LibsOfTikTok` (Chaya Raichik — culture-war right)
- `@JackKKnight` ... wait, let me prune to real accounts.

Let me lock 7 alt-right + 5 mainstream-MAGA = 12 accounts.

**FINAL LOCKED LIST (12 accounts):**

Alt-right cluster (7):
1. `NickJFuentes`
2. `ashleystclair1`
3. `Cernovich`
4. `JackPosobiec`
5. `realStewPeters`
6. `LauraLoomer`
7. `DC_Draino`

MAGA mainstream comparison cluster (5):
8. `charliekirk11`
9. `TimRunsHisMouth`
10. `benshapiro`
11. `TuckerCarlson`
12. `LibsOfTikTok`

If any locked account is suspended/banned/non-existent at query time, report as `STATUS=missing` and exclude from cluster aggregates. Pre-reg does NOT allow substitution.

X API query: `users/by/username/{username}` endpoint, `user.fields=public_metrics,verified,created_at`. ~12 × $0.01 = $0.12 budget (well under user's $2 session cap).

---

## 3. Hypotheses (LOCKED)

### H33 — Google Trends interest rose more sharply 2024 vs 2020 for alt-right terms

**Test:** Compute search-interest geometric-mean across the 5 LOCKED terms by month. Compare:
- Pre-election rise: Jul-Oct interest (avg) vs Jan-Jun (avg), 2020 cycle vs 2024 cycle.
- 2024 election-month spike: % change from Jul 2024 to Nov 2024, compared to same window 2020.

**Falsification gates:**
- **CONFIRMED-AMPLIFIED:** 2024 pre-election spike ≥ 1.5× 2020 pre-election spike (across ≥ 3 of 5 terms).
- **PARTIAL:** between 1.0× and 1.5×.
- **REFUTED:** 2024 spike < 2020 spike (alt-right interest is DECLINING).

### H34 — State Google Trends interest correlates with state Trump 2020→2024 swing

**Test:** Compute state-level Trump margin shift 2020→2024 (Trump 2024 margin minus Trump 2020 margin, in percentage points). Compute Spearman correlation with state-level Google Trends interest (Sep-Nov 2024 average across the 5 LOCKED terms, geometric mean).

**Falsification gates:**
- **CONFIRMED:** Spearman ρ ≥ +0.4 (states with higher alt-right search interest shifted MORE toward Trump).
- **PARTIAL:** ρ ∈ [+0.2, +0.4].
- **NULL:** ρ ∈ (-0.2, +0.2).
- **REVERSED:** ρ ≤ -0.2 (states with higher alt-right interest shifted AWAY from Trump).

**Caveat (per pre-reg):** State-level ecological correlation. NOT causal. Ecological-fallacy risk noted.

### H35 — X cluster size (descriptive snapshot)

**Test:** Pull current follower_count for each LOCKED account. Report:
- Sum of follower counts for Cluster A (alt-right).
- Sum for Cluster B (MAGA mainstream).
- Ratio A:B as "alt-right share of MAGA-adjacent reach."
- Most-followed alt-right account vs least-followed.

**Verdict (descriptive, NOT pre-reg gated — magnitudes flagged):**
- **HIGH-VISIBILITY:** Cluster A total ≥ 5M followers (substantial reach).
- **MEDIUM:** 1-5M.
- **NICHE:** <1M.

**Time-series caveat:** Snapshot only. Historical follower-count growth requires Pro-tier X API (not available). The snapshot is post-election, so reflects current cluster size NOT pre-election state.

### Aggregate verdict

- **EXTERNAL ALT-RIGHT FOOTPRINT CONFIRMED:** H33 CONFIRMED-AMPLIFIED + H34 CONFIRMED + H35 HIGH-VISIBILITY.
- **PARTIAL FOOTPRINT:** ≥1 hypothesis confirms.
- **EXTERNAL FOOTPRINT WEAK / DECLINING:** H33 REFUTED + H34 NULL.

---

## 4. Operationalization

### 4.1 Tools

- **Google Trends:** `pytrends` Python library (free, rate-limited). Pull weekly time-series + state-level cross-section.
- **Wikipedia Pageviews:** Wikimedia REST API at `https://wikimedia.org/api/rest_v1/metrics/pageviews/per-article/en.wikipedia/all-access/all-agents/{article}/monthly/2020010100/2024123100` — free, no auth.
- **X API:** existing `TWITTER_BEARER_TOKEN` in `C:/DeepDive/.env`. Endpoint `https://api.x.com/2/users/by/username/{username}?user.fields=public_metrics,verified,created_at`. Budget: 12 × $0.01 = $0.12.
- **State election data:** MIT Election Data + Science Lab or FEC official returns. State-level Trump 2020 + 2024 vote shares.

### 4.2 Outputs

- `data/processed/v28/google_trends.csv` — weekly time-series + state cross-section
- `data/processed/v28/wikipedia_pageviews.csv` — monthly pageviews per article
- `data/processed/v28/x_follower_counts.csv` — current follower counts for 12 accounts
- `data/processed/v28/state_trump_swing.csv` — state-level 2020+2024 margins + ecological correlation
- `result_v2.8_dnc_postmortem.md` — written verdict

### 4.3 Reproducibility

State-level vote data hash + retrieval date recorded in result.

---

## 5. Threats to validity

- **Ecological fallacy.** State-level Google Trends × state Trump swing is a CORRELATION not an INDIVIDUAL exposure-vote link. Individuals in high-search-interest states may not personally be searching alt-right terms.
- **Term ambiguity.** "Rumble" has non-political uses; "America First" used by both Trump campaign and Fuentes. Caveat: term searches conflate.
- **Snapshot vs trajectory.** X follower counts are CURRENT (post-election). Pre-election cluster size would require historical archive (not in user's API tier). Snapshot reports cluster size NOW, not its growth.
- **Banned-account survivor bias.** Accounts banned 2020-2024 (e.g., Fuentes was banned then reinstated) don't appear in this snapshot. Surviving accounts may under-represent total cluster.
- **Google Trends "100" scale.** Relative-interest scale, not absolute volume. Cross-term comparisons need geometric-mean composition.
- **Wikipedia pageviews ≠ alt-right curiosity.** Page views include casual / mainstream-media-driven curiosity, not just sympathetic interest. Direction-of-interest is ambiguous.

---

## 6. v2.8 deviation log

| Date | Deviation | Rationale |
|---|---|---|

(Empty at lock; populated as v2.8 work surfaces discrepancies.)

---

**Locked at commit:** `[fill at commit]` on `main`.
**Repository:** https://github.com/mrnathanhumphrey-droid/DNC.
**Builds on:** result_v2.6 (887c384) + prereg_v2.7 (bb21e1a).
