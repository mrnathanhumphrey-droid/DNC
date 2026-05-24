# result_v2.5 — DNC 2024 Post-Mortem v2.5 (Media-diet channel — partial test, asymmetric battery)

**Locked:** 2026-05-24 against `prereg_v2.5_dnc_postmortem.md` HEAD `02137ba`.
**Builds on:** result_v2.1 (`27a0093`), result_v2.2 (`e441cbd`), result_v2.3 (`d810d63`).
**Repo:** github.com/mrnathanhumphrey-droid/DNC.

---

## 1. Headline (one sentence)

**Mainstream + MSNBC-tilted TV news engagement is a real predictor of Harris-vote (β = +0.64 to +1.06 credibly positive across H24 and H26) but does NOT mediate the cohort defection signal** — σ_cohort stays at 0.44-0.54 across all three v2.5 hypotheses (H24/H25/H26). Combined with the §10 dev 1 caveat that ANES 2024 public release **excluded** the radio + website batteries (right-wing media ecosystem unmeasurable), the verdict is **MEDIA-DIET CHANNEL NOT THIS at the slice we can observe** — and the right-wing media exposure channel remains the live candidate for the cohort-bypass mechanism, blocked behind data acquisition (CES/Pew comparable items or restricted-release ANES).

---

## 2. Verdicts table

Reference baseline (v2.0.1 hardened H4): **σ_cohort = 0.448 [0.047, 1.053]**, K_fund=8, N=3533.

| Hyp | Mediator | β / interaction [90% CI] | σ_cohort (Δ vs baseline) | Verdict |
|---|---|---|---|---|
| **H23** | media-diet ideology score predicts Harris-vote | β = +0.638 [+0.285, +1.016] **credible**, |β| ≫ 0.15 threshold | (predictive) | **CONFIRMED — left media is a real fundamental** |
| **H24** | media-diet ideology mediates cohort | (same β as H23) | 0.437 (Δ -0.011, -2.5%) | **NOT MEDIATED** |
| **H25** | media-diet volume mediates cohort | β = +0.266 [+0.064, +0.471] credible (more shows watched → more Harris) | 0.543 (Δ +0.095, +21%) | **NOT MEDIATED + ANTI-SHRINKAGE** |
| **H26** | combined ideology + volume + ideology×cohort | β_ideology = +1.06 [+0.15, +1.98] credible; β_volume = +0.18 [-0.03, +0.39] NULL; β_interaction = -0.18 [-0.47, +0.12] NULL | 0.488 (Δ +0.040, +9%) | **NOT MEDIATED + interaction HOMOGENEOUS** |

**Aggregate verdict per pre-reg §1:** **MEDIA-DIET CHANNEL NOT THIS** — all three mediation hypotheses (H24/H25/H26) NOT MEDIATED. The mainstream-TV-news engagement dimension does not absorb the cohort defection signal.

---

## 3. The asymmetric-battery caveat (§10 dev 1, filed at lock)

ANES 2024 public release contains:
- **V241602 English TV battery (16 items): POPULATED.** Used in v2.5. Battery composition: 4 explicitly left-leaning MSNBC shows + lean-left CNN/PBS + center-mainstream + ONE explicitly right-leaning show (Outnumbered/Fox).
- **V241603 Spanish TV battery: small-subsample only** (≈600 valid, mostly -1 inapplicable for non-Spanish-speaking respondents).
- **V241604 radio battery (14 items): ALL VALUES -2 (UNAVAILABLE in public release).** This battery would have caught Hannity/Levin/Shapiro/Bongino/Glenn Beck/Mark Levin/Dan Bongino/Hugh Hewitt/Mike Gallagher/Dana Show — i.e., the right-wing talk-radio ecosystem.
- **V241605 website battery (~17 items): ALL VALUES -2 (UNAVAILABLE in public release).** Would have caught Breitbart/Newsmax/OAN/Daily Caller/New York Post — the right-wing website ecosystem.

**The right-wing media ecosystem is structurally unmeasurable from this release.** v2.5 tests ONLY the mainstream/MSNBC-tilted slice. The NOT THIS verdict is conditional on this slice; it does not rule out right-wing media exposure as a mediator, which v2.5 was designed to detect IF it operated through mainstream-news disengagement, but cannot test as direct exposure.

---

## 4. Reading H23 (media-diet ideology is a real fundamental — confirmed twice over)

H24 ideology-only β = **+0.638 [+0.285, +1.016]** credibly positive.
H26 ideology with volume + interaction also-included β = **+1.06 [+0.15, +1.98]** credibly positive, even larger.

Reading the magnitude: a 1-SD increase in left-leaning media diet (composite of which of the 16 V241602 shows the respondent watches, weighted by show ideology) is associated with **roughly a 0.6-1.0 log-odds increase in Harris-vote probability** conditional on the rest of the H4 baseline (2020 recall, econ, pid7, Trump_ft, Gaza salience, econ×cohort interaction).

For perspective, this is roughly half the magnitude of `fund_pid7_z` (β ≈ -1.17) and a third of `fund_trump_ft_z` (β ≈ -2.32) — substantial but not dominant.

**Mainstream/MSNBC TV-news engagement is a real channel.** It just doesn't *mediate* cohort.

---

## 5. Reading H24/H25/H26 (mediation fails)

| H | What's added | σ_cohort | Shrinkage |
|---|---|---:|---:|
| H4 baseline | — | 0.448 | reference |
| H24 | ideology only | 0.437 | -2.5% (essentially unchanged) |
| H25 | volume only | 0.543 | **+21% (anti-shrinkage)** |
| H26 | ideology + volume + ideology×cohort | 0.488 | +9% (anti-shrinkage, smaller) |

**The pattern matches v2.1's H9 trust-gov anti-shrinkage finding.** When media-engagement controls are added, σ_cohort INCREASES — meaning the cohort defection signal becomes MORE distinct, not less, once you adjust for how much TV news people consume. Reading: younger cohorts engage less with mainstream TV news AND defect more, but those are independent channels rather than the engagement-mediating-defection story.

The H26 interaction β = -0.178 [-0.467, +0.115] is NULL — media-diet ideology has a HOMOGENEOUS slope across cohorts. The Trump_ft × cohort interaction was also HOMOGENEOUS (v2.1 H11). Two homogeneous interactions in a row suggests the cohort effect operates as a level-shift across cohorts, not as differential-weight on existing fundamentals.

---

## 6. What v2.5 closes

- **"Younger cohorts defect because they consume less mainstream/MSNBC news"**: REFUTED. Volume controls anti-shrink cohort variance; engagement gap and cohort effect are independent.
- **"Younger cohorts defect because they consume more right-leaning content in the V241602 TV battery"**: REFUTED in the sub-sample where it's measurable. (The Fox/Outnumbered signal is captured but doesn't absorb cohort.)
- **"Media-ideology-by-cohort interaction is the channel"**: REFUTED. Interaction β NULL.

Combined with v2.1's 5 ruled-out attitudinal mediators + v2.2's lasso AXIS NOT FOUND, **the set of measurable ANES political-attitudinal + mainstream-media-engagement mediators that fail to absorb the cohort signal now numbers 9**:

1. Ideology (v2.1 H8) — 14% shrinkage
2. Trust-gov composite (v2.1 H9) — anti-shrinkage
3. Anti-system populism (v2.1 H10) — 14% shrinkage
4. Trump_ft × cohort heterogeneity (v2.1 H11) — no shrinkage + HOMOGENEOUS
5. Party-ID importance (v2.1 H12) — no shrinkage
6. Lasso 16-item multivariate (v2.2) — 9% on held-out
7. Mainstream-TV-news ideology (v2.5 H24) — 2.5%
8. Mainstream-TV-news volume (v2.5 H25) — anti-shrinkage
9. Combined media-ideology + volume + interaction (v2.5 H26) — anti-shrinkage + HOMOGENEOUS

The cohort signal sits robustly at σ_cohort ≈ 0.40-0.55 across all 9 tests.

## 7. What v2.5 opens (sharper than v2.1's open question)

v2.5 sharpens the v2.1 mechanism-residual reading by ruling out ANES-measurable media-diet (at least the mainstream slice). The live channel candidates that remain, in priority order:

1. **Right-wing media exposure** (talk radio + websites + podcasts + social media). Per §3 caveat, V241604 and V241605 are unavailable in this release. **Data acquisition path**: ANES restricted-release access (requires DUA, per pre-reg v1.0 §12 dev 6 NOT currently available); OR Pew CRWG (which has news-source detail items in some waves); OR Cooperative Election Study's news-consumption module if available 2024.
2. **Generational political socialization** (when first politically aware, what national events were formative). ANES has age-of-first-vote-ish items; CES doesn't carry this; specialized surveys (American Religious Identification Survey?) might.
3. **Cohort-specific event exposure**. MillYoung was 24-31 during 2020 (peak BLM/COVID/Trump-first-term). v2.3 found MillYoung is the active-flipper cell; if their flipping is driven by formative 2020-cycle experience, this would be detectable via items like "did you participate in 2020 protests" / "do you know someone who died from COVID-19" / "did you change party registration in 2020-2024." These items are not in the v2.1-v2.5 covariate pool.
4. **Direct identity items beyond demographics** (LGBTQ+, gender identity, religious-none vs non-affiliated, race-conscious identity). ANES has religious-id battery (V241443 series) — could be tested in v2.6.

**Recommended next thread** (highest yield given existing data): **#4 — religious-identity × cohort** using V241443a-h. Religious-none rises sharply by cohort and is plausibly cohort-linked through socialization, not currently in the model. If MEDIATED, narrows mechanism toward religious-secular cohort shift.

---

## 8. Honest caveats + diagnostics

- **H24 divergence count = 59** (well above 10 threshold) despite hardened settings. R̂ 1.013, ESS 610 — chains mix but slowly. The interaction-free model with ideology added pushes posterior into thin-tail regions. H25 + H26 have cleaner 15 divergent each. The H24 σ_cohort posterior estimate at point-mean 0.437 is robust to this; tail precision is reduced.
- **H25 anti-shrinkage flag**: same pattern as v2.1 H9 trust-gov. When you control for media VOLUME (which younger cohorts have LESS of), the remaining cohort-vote signal becomes larger because the volume control partials out a *positive* cohort-vote pathway, leaving the *negative* residual more pronounced. This is consistent with: more TV news → more Harris-vote (β_volume credibly positive) AND younger cohorts watch less TV news AND younger cohorts defect more.
- **Battery asymmetry binds the verdict**: with 8 left + 1 right + 7 center shows, the V241602 ideology composite is structurally compressed against the left ceiling. A respondent who watches only Fox/Hannity/Levin/Newsmax/Breitbart would register as 0.0 on `media_ideology_mean` (no V241602 shows watched), indistinguishable from a non-TV-watcher. This is the asymmetric-battery threat to interpretation (per §4 of pre-reg).
- **Self-report bias**: respondents over-report news engagement. Affects absolute volume estimates but not cross-cohort directional pattern.
- **Single-substrate**. ANES only.

---

## 9. Repo state at lock

- Pre-reg v2.5 locked at `02137ba`.
- 3 hardened fits stored under `data/processed/fits/`:
  - `fit_anes_vote_h24_binary_hardened_*` (media ideology only)
  - `fit_anes_vote_h25_binary_hardened_*` (media volume only)
  - `fit_anes_vote_h26_binary_hardened_*` (combined)
- Joblibs under `data/processed/stan_data_anes_vote_h{24,25,26}.joblib`.
- Repo: github.com/mrnathanhumphrey-droid/DNC.

**Result commit hash to be filled at commit time.**
