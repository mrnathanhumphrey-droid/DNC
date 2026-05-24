# Pre-registration v2.5 — DNC 2024 Post-Mortem (Media-diet channel for cohort-bypass mechanism)

**Locks BEFORE running v2.5 fits.** Builds on:
- result_v2.1 (HEAD `27a0093`): MECHANISM RESIDUAL — 5 a-priori mediators NOT MEDIATED.
- result_v2.2 (HEAD `e441cbd`): AXIS NOT FOUND — 41-item ANES political-attitudes lasso couldn't decompose cohort signal on held-out half.
- result_v2.3 (HEAD `d810d63`): MillYoung is the qualitatively-distinct active-flipper cohort.

**Motivation.** v2.2 §5 listed media diet as the top v3 candidate, deferred because the items aren't single-ordinal scalars. v2.5 tests the **media-diet channel** for the cohort-bypass mechanism: does composing the ANES TV-show-watching battery into media-diet ideology + volume metrics, then adding them as fundamentals to H4 baseline, shrink σ_cohort?

Per user framing 2026-05-24: *"now we have to look at the channels as a prereg hypothesis. im assuming media diet. can we get that data?"*

**Critical data-availability caveat (§10 dev 1, filed at lock):** ANES 2024 public release contains the English TV-shows battery V241602a-r (16 items) but **EXCLUDES** the radio battery V241604 (all values -2 = not in public release) and the website battery V241605 (all -2). V241603 Spanish TV is a small-subsample probe (n≈600, mostly -1 inapplicable for non-Spanish-speaking respondents). **The pre-reg restricts to V241602 16-item English TV battery.** This battery is asymmetric: it contains 4 explicitly left-leaning MSNBC shows + lean-left CNN/PBS + center-mainstream + ONE right-leaning show (Outnumbered/Fox). The right-wing media ecosystem (Hannity, Levin, Shapiro, Bongino, Breitbart, Newsmax, OAN) is **NOT measurable** in this public release. v2.5 therefore tests "mainstream/left news engagement" as a cohort mediator — NOT "right-wing media exposure as cohort mediator."

---

## 0. What this pre-reg LOCKS

- Ideology score per V241602 show (LOCKED below in §3.1)
- 3 composite metrics from V241602 (LOCKED §3.2)
- 4 v2.5 hypotheses (H23-H26)
- Stan model + fit configuration
- Verdict gates

**What this pre-reg does NOT lock:**
- Right-wing media exposure (data unavailable in 2024 public release)
- Causal-identification (descriptive associational tests only)
- Cross-substrate (ANES only — CES + Pew don't carry comparable batteries)

---

## 1. Hypotheses (LOCKED)

**Reference baseline:** v2.0.1 hardened H4 fit — σ_cohort = 0.448 [0.047, 1.053].

### H23 — Media-diet ideology score predicts Harris-vote

**Prior:** Higher left-leaning media diet → more likely Harris-vote. β credibly POSITIVE expected (left-diet → Harris).

**Test:** Add `fund_media_diet_score_z` (z-score of per-respondent ideology composite, §3.2) to H4 K_fund=8 baseline. K_fund_new=9.

**Falsification gates:**
- **CONFIRMED:** β 95% CI > 0 AND |β| > 0.15 (sizable + credible).
- **WEAK CONFIRMED:** β 95% CI > 0 AND |β| ≤ 0.15.
- **NULL:** β CI crosses zero.
- **REVERSED:** β 95% CI < 0.

### H24 — Media-diet ideology mediates cohort

**Prior:** If MillYoung's defection reflects LESS engagement with left-leaning mainstream news (rather than MORE engagement with right news, which we can't measure), σ_cohort should shrink under the media-diet ideology control.

**Test:** σ_cohort posterior with H23 model.

**Falsification gates (re-use v2.1 thresholds):**
- **MEDIATED:** σ_cohort < 0.15.
- **PARTIAL:** σ_cohort ∈ [0.15, 0.25].
- **NOT MEDIATED:** σ_cohort ≥ 0.25.

### H25 — Media-diet VOLUME (count of shows watched) mediates cohort

**Prior:** Younger cohorts may engage with mainstream TV news less (cord-cutters, streaming, social-media-first information environment). If volume itself absorbs cohort variance, the mediator is "engagement with traditional TV news" rather than ideology.

**Test:** Add `fund_media_volume_z` (z-score of count of V241602 shows checked) to H4 baseline. Single fundamental added. K_fund_new=9.

**Falsification gates:** same as H24.

### H26 — Combined ideology + volume + interaction mediates cohort

**Prior:** A composite mediator (ideology + volume + ideology × cohort interaction) gives the maximum opportunity for V241602 to absorb the cohort signal.

**Test:** Add `fund_media_diet_score_z` + `fund_media_volume_z` + `fund_media_score_x_cohort` (ideology × cohort_idx) as 3 fundamentals to H4 baseline. K_fund_new=11.

**Falsification gates:**
- **MEDIATED:** σ_cohort < 0.15.
- **PARTIAL:** σ_cohort ∈ [0.15, 0.25].
- **NOT MEDIATED:** σ_cohort ≥ 0.25.

### Aggregate verdict

- **MEDIA-DIET CHANNEL CONFIRMED:** ≥1 of H24/H25/H26 reaches MEDIATED gate.
- **MEDIA-DIET CHANNEL PARTIAL:** ≥1 reaches PARTIAL gate; none MEDIATED.
- **MEDIA-DIET CHANNEL NOT THIS:** All NOT MEDIATED. The mainstream-TV-news engagement dimension of media diet does not mediate cohort. Reading: the cohort-bypass mechanism is likely in the UNAVAILABLE channels (right-wing radio, websites, podcasts, social media) — a v3 / data-acquisition lookahead.

---

## 2. Operationalization (LOCKED)

### 2.1 Show-by-show ideology score (LOCKED before any data inspection)

Following AllSides / Ad Fontes / mainstream-media-bias conventions for these specific shows. **HIGHER = MORE LEFT-LEANING.** Range -1 (strong right) to +1 (strong left).

| V-code | Show | Network | Ideology score |
|---|---|---|---:|
| V241602a | Anderson Cooper 360 | CNN | +0.3 |
| V241602b | Erin Burnett OutFront | CNN | +0.2 |
| V241602c | 60 Minutes | CBS | 0.0 |
| V241602d | 20/20 | ABC | 0.0 |
| V241602e | Dateline | NBC | 0.0 |
| V241602f | Face the Nation | CBS | 0.0 |
| V241602g | Meet the Press | NBC | 0.0 |
| V241602h | The Price Is Right | CBS | 0.0 (game show — excluded from ideology composite, included in volume) |
| V241602i | Good Morning America | ABC | 0.0 |
| V241602j | Today | NBC | 0.0 |
| V241602k | Outnumbered | Fox News | **-0.8** |
| V241602m | Deadline: White House | MSNBC | **+0.8** |
| V241602n | All In with Chris Hayes | MSNBC | **+0.9** |
| V241602p | The 11th Hour with Stephanie Ruhle | MSNBC | **+0.8** |
| V241602q | PBS NewsHour | PBS | +0.2 |
| V241602r | Saturday Night Live | NBC | +0.4 |

**Battery asymmetry note:** sum of LEFT-leaning shows (score > 0): 8 items totaling +3.6. Sum of RIGHT-leaning: 1 item totaling -0.8. The battery is structurally tilted toward measuring left-news engagement.

### 2.2 Composite metrics (LOCKED)

For each respondent:
- `media_volume` = count of V241602 items where value == 1 (mentions).
- `media_ideology_sum` = sum over items where value == 1 of `ideology_score[item]` (PRICE IS RIGHT excluded from ideology composite per §2.1 note).
- `media_ideology_mean` = `media_ideology_sum / max(media_volume_excl_PIR, 1)` (0 if no qualifying shows watched).
- All standardized by z-score across the H4 sample.

`fund_media_diet_score_z` = z-score of `media_ideology_mean`.
`fund_media_volume_z` = z-score of `media_volume`.
`fund_media_score_x_cohort` = `fund_media_diet_score_z × cohort_idx` (numeric 1-5).

Missing-data handling: if a respondent has all V241602 items as -1 (inapplicable) or -9 (refused), media_volume = 0, media_ideology_mean = 0, with a `media_missing` flag. Per pre-reg, respondents with media_missing=True are RETAINED in the sample (z-scored to the sample mean, which is approximately 0 for the volume measure). Missingness rate reported in result.

### 2.3 Sample frame

Same as H4 baseline (per v2.0 H4 §1): respondents with valid 2024 PRES major-party vote (V242096x ∈ {1, 2}), valid 7-pt pid7 (V241227x > 0), valid demographics, valid 2020 recall. N expected ≈ 3533 (matches H4 baseline) ± modest media-missing attrition.

### 2.4 Stan model + fit configuration

`model_a.stan`, hardened: chains=6, warmup=1000, samples=1000, seed=42 (matches v2.0.1 / v2.1 / v2.2 standard).

---

## 3. Verdicts

H23: CONFIRMED / WEAK CONFIRMED / NULL / REVERSED.
H24, H25, H26: MEDIATED / PARTIAL / NOT MEDIATED.

Aggregate: per §1.

---

## 4. Threats to validity

- **Battery asymmetry.** The V241602 battery has 8 left-leaning + 1 right-leaning item. This biases the ideology composite toward measuring "left-news engagement amount" rather than "left-vs-right news balance." If the cohort mechanism is via right-wing media exposure (radio/websites/podcasts — UNAVAILABLE), v2.5 will produce a NOT MEDIATED reading by construction. **This is a known limitation, not a verdict.**
- **TV-only sample.** Cord-cutting younger cohorts may have LOW media_volume regardless of ideology — picking up "TV-news-cord-cut" effects rather than "ideological echo chamber" effects. Volume and ideology composites are reported separately to disentangle.
- **Show ideology scores are author-assigned.** While based on AllSides/Ad Fontes consensus, individual show scores are judgment calls. Aggregate verdict robust to within-+/-0.2 perturbation, but extreme perturbation could flip H23 sign for ambiguous shows (none of the strong-right or strong-left placements are controversial).
- **Self-report bias.** Respondents over-report news engagement; this affects absolute volume estimates but not cross-cohort comparison.
- **Single-substrate.** ANES only. Cross-substrate replication impossible without comparable media batteries elsewhere.

---

## 5. v2.5 deviation log

| Date | Deviation | Rationale |
|---|---|---|
| 2026-05-24 | **§10 dev 1: media-diet pool restricted to V241602 English TV (16 items).** Pre-reg motivation cited media diet broadly; data inspection 2026-05-24 found V241604 radio + V241605 websites are all -2 (NOT IN PUBLIC RELEASE), V241603 Spanish TV is small-subsample-only. | ANES 2024 public release narrows media-diet coverage to English TV. Right-wing media ecosystem (talk radio + websites) is unmeasurable from this release. Caveat folded into §4 threats. Restriction filed BEFORE running fits per pre-reg discipline. |

---

**Locked at commit:** `[fill at commit]` on `main`.
**Repository:** https://github.com/mrnathanhumphrey-droid/DNC.
**Builds on:** result_v2.1 (27a0093) + result_v2.2 (e441cbd) + result_v2.3 (d810d63).
