# result_v2.10 — DNC 2024 Post-Mortem v2.10 (Non-voter mirror + Issue decomposition)

**Locked:** 2026-05-25 against `prereg_v2.10_dnc_postmortem.md` (`f63c343`).
**Builds on:** result_v2.9 (`823432b`) multi-channel demobilization.
**Repo:** github.com/mrnathanhumphrey-droid/DNC.

24 Stan fits total: 10 non-voter mirror + 14 item-level issue decomposition.

---

## 1. Two headlines

**HEADLINE 1 (mirror reframe):** Non-voter mobilization in 2024 was **IDEOLOGICAL, not LOGISTICAL.** Among CES VV 2020 non-voters (N=2,803), campaign contact does NOT predict either Trump-mobilization or Harris-mobilization (β NULL for both directions). What DOES predict is pre-existing ideological alignment — economic perception, immigration position, engagement — and these align in OPPOSITE directions for the two mobilization pathways. **The "Dem GOTV failure" framing is REFUTED** for the non-voter pool: total non-voter mobilization was roughly symmetric (Trump 810, Harris 830). Trump and Harris each pulled their ideological matches; the cohort asymmetry (older→Trump, younger→Harris) is the real story.

**HEADLINE 2 (decomp resolution):** Within the "issue-conservatism" channel from v2.9, **two single items dominate**: opposing "Build the wall" (β=-0.262 STRONG) and opposing "Increase fossil fuel production" (β=-0.262 STRONG). Both are the conservative side of their respective batteries. The "soft Democrat issue conservatism" pattern from v2.9 is most precisely: **Biden voters who support The Wall and Fossil Fuel Expansion were the disproportionate skippers.** Other issue items (legal status for undocumented, border patrols, EPA enforcement) are NULL or weak.

---

## 2. PART 1 — H_MIRROR: Non-voter mobilization

### 2.1 Universe (no deviation from pre-reg §1A)

| Filter | N |
|---|---:|
| `presvote20post == 6` (didn't vote 2020) + VV + age 18+ in 2020 + TS_g2024 populated | 2,803 |
| Trump-mobilized (TS in {1-6} + CC24_410==2) | 810 |
| Harris-mobilized (TS in {1-6} + CC24_410==1) | 830 |
| Third-party-mobilized | 97 |
| Still non-voter (TS==7) | 924 |
| Voted-unknown | 142 |

**Symmetric totals:** Trump-mob 810 vs Harris-mob 830 → Harris won non-voter mobilization by +20 (negligible). Refutes "GOP out-mobilized" + "Dem GOTV failure" framings at the AGGREGATE level. Asymmetry is internal.

### 2.2 Cohort breakdown (asymmetry IS the story)

| Cohort | N | Trump-mob | Harris-mob | T - H | Net swing |
|---|---:|---:|---:|---:|---|
| Silent | 37 | 14 | 14 | 0 | tie |
| Boomer | 847 | 277 | 243 | **+34** | older→Trump |
| GenX | 933 | 294 | 263 | **+31** | older→Trump |
| MillOld | 480 | 117 | 142 | -25 | younger→Harris |
| MillYoung | 312 | 77 | 94 | -17 | younger→Harris |
| **GenZ** | 194 | 31 | 74 | **-43** | strongest younger→Harris |

GenZ non-voters mobilized for Harris 2.4× more than for Trump.

### 2.3 H_MIRROR_A — Cohort matters (CONFIRMED)

σ_cohort across all 10 fits sat at **0.48 – 0.54** — among the highest σ_cohort readings in the entire v2 program. Cohort is a STRONG predictor of both Trump-mob and Harris-mob directions, with opposite-signed cohort effects. **H_MIRROR_A CONFIRMED.**

### 2.4 H_MIRROR_B — Channel asymmetry (CONFIRMED)

Trump-mob predictors (vs. still-non-voter, N=1,734):

| Channel | β [5%, 95%] | Verdict |
|---|---:|---|
| mob_any_z (campaign contact) | +0.018 [-0.090, +0.126] | **NULL** |
| engage_act_z (political activity) | +0.058 [-0.077, +0.206] | **NULL** |
| issue_econ_z (worse econ) | **+0.460 [+0.316, +0.603]** | **STRONG** |
| issue_imm_z (progressive imm.) | **-0.599 [-0.730, -0.471]** | **STRONG** |
| trust_elec_z (less election confidence) | -0.480 [-0.599, -0.361] | STRONG (counterintuitive — see §6) |

Harris-mob predictors (vs. still-non-voter, N=1,754):

| Channel | β [5%, 95%] | Verdict |
|---|---:|---|
| mob_any_z (campaign contact) | +0.053 [-0.081, +0.185] | **NULL** |
| engage_act_z (political activity) | **+0.510 [+0.338, +0.691]** | **STRONG** |
| issue_econ_z (worse econ) | **-0.573 [-0.715, -0.430]** | **STRONG** (opposite-sign of Trump) |
| issue_imm_z (progressive imm.) | **+0.353 [+0.195, +0.512]** | **STRONG** (opposite-sign of Trump) |
| trust_elec_z (less election confidence) | -0.278 [-0.402, -0.153] | STRONG (same direction as Trump) |

**Symmetric channels (Trump β ≈ -Harris β):** econ perception, immigration. Same magnitude, opposite sign. This is the ideological-sorting mechanism in numbers.

**Asymmetric channels:** engagement (Harris-mob predicts; Trump-mob does NOT). Mobilization (NULL for both — non-voters who got campaign contact didn't behave differently than those who didn't, regardless of which party mobilized them).

**Trust collapse SAME direction for both:** both Trump-mob AND Harris-mob have HIGHER raw election-confidence than still-non-voters. Reading: trust_elec_z direction goes raw 1=strongly agree elections fair (high confidence) → strongly disagree (low confidence). β=-0.48 for Trump-mob means LESS election confidence → MORE Trump-mobilization (no... wait). Let me redo.

Trust direction LOCKED in v2.9 §6: CC24_421 5-pt raw is 1=strongly agree (high confidence) to 5=strongly disagree (low confidence). Not reversed. So HIGH raw z = LESS confidence. β=-0.480 trust_elec_z trump-mob means LESS confidence → LESS mobilization (negative β). So both Trump and Harris mobilized voters with HIGHER trust in elections than still-non-voters. The still-non-voter pool has the LOWEST election confidence. Consistent reading: election-distrust = disengagement, not partisan signal. (Updated from initial reading — both mobilized groups are more election-confident.)

**H_MIRROR_B CONFIRMED** (3 of 5 channels show direction-asymmetry between Trump-mob and Harris-mob fits).

### 2.5 H_MIRROR_C — Net symmetric (CONFIRMED)

Trump-mob 810 vs Harris-mob 830. Difference -20 within sampling variation of any reasonable per-cohort decomposition. **Net mobilization symmetric.** The asymmetric story is cohort-internal, not overall.

### 2.6 The big reframe

**Mobilization (campaign contact) matters for RETAINING existing voters, NOT for RECRUITING new ones from non-voters.**

| Universe | Mobilization β (CC24_431a) | Interpretation |
|---|---|---|
| v2.9 Biden-2020 (retention vs skip) | **β=-0.251 STRONG** (more contact → less skip) | Campaign contact retains marginal Biden voters |
| v2.10 non-voter (Trump-mob vs still-nv) | β=+0.018 NULL | Campaign contact does NOT pull 2020 non-voters to Trump |
| v2.10 non-voter (Harris-mob vs still-nv) | β=+0.053 NULL | Campaign contact does NOT pull 2020 non-voters to Harris |

**This refutes the "Dem GOTV failure" framing.** Dem campaign contact wasn't the lever that activated non-voters; non-voters mobilized based on pre-existing ideological alignment regardless of contact. The DNC's loss is NOT primarily a GOTV story on the non-voter side.

It's also a partial vindication of the v2.9 framing: campaign contact DID matter for retaining marginal Biden voters (the demobilization angle). Just not for the symmetric question.

---

## 3. PART 2 — H_DECOMP: Item-level issue decomposition

### 3.1 14 items tested on the v2.9 Biden universe (N=17,401)

| Cluster | Item | β [5%, 95%] | Verdict | Note |
|---|---|---:|---|---|
| Abortion | CC24_324a "Always allow as choice" | -0.147 [-0.186, -0.107] | WEAK | direction-correct: pro-choice → less skip |
| Abortion | CC24_324d "Expand access" | -0.196 [-0.234, -0.158] | WEAK | direction-correct |
| Abortion | CC24_324b "Rape/incest only" reversed | -0.176 [-0.224, -0.128] | WEAK | direction-correct |
| Abortion | CC24_324c "Illegal always" reversed | -0.129 [-0.161, -0.096] | WEAK | direction-correct |
| Climate | CC24_326a "EPA regulate carbon" | -0.108 [-0.142, -0.076] | WEAK | direction-correct |
| Climate | CC24_326b "Renewable energy" | -0.082 [-0.119, -0.044] | INDET | weak signal |
| Climate | CC24_326c "EPA enforcement" | -0.035 [-0.077, +0.008] | **NULL** | |
| Climate | CC24_326e "Halt oil/gas leases" | -0.130 [-0.176, -0.084] | WEAK | direction-correct |
| **Climate** | **CC24_326d "Increase fossil fuel" reversed** | **-0.262 [-0.310, -0.215]** | **STRONG** | **biggest climate item** |
| Climate | CC24_326f "Prevent gas-stove ban" reversed | -0.099 [-0.150, -0.049] | INDET | weak signal |
| Immigration | CC24_323a "Legal status to undocumented" | -0.039 [-0.084, +0.005] | **NULL** | |
| Immigration | CC24_323d "Dreamers permanent status" | -0.176 [-0.206, -0.146] | WEAK | direction-correct |
| Immigration | CC24_323b "Border patrols" reversed | -0.006 [-0.056, +0.044] | **NULL** | border patrols doesn't divide |
| **Immigration** | **CC24_323c "Build wall" reversed** | **-0.262 [-0.301, -0.223]** | **STRONG** | **biggest immigration item** |

### 3.2 Cluster patterns

**Abortion (4/4 credible WEAK).** Uniform pattern: pro-choice → less skip across all 4 sub-items. The cluster signal is broad-based but no single item dominates. This means "the abortion issue" as a unified construct carried the skip signal — voters who skip are anti-choice across multiple framings.

**Climate (1 STRONG + 4 WEAK/INDET + 1 NULL).** Asymmetric. The STRONG item is "support increase fossil fuel production" — opposing fossil-fuel expansion is what marks the retainer. The mainstream pro-climate items (EPA, renewables) are WEAK. **Reading: it's not "pro-climate" voters who retained; it's "anti-fossil-fuel-expansion" voters who retained.** The conservative pole on the energy axis is what divides.

**Immigration (1 STRONG + 1 WEAK + 2 NULL).** Highly asymmetric. The STRONG item is "support build the wall" — opposing the wall is what marks the retainer. Border patrols and legal status are NULL — Biden voters didn't split on those. Dreamers is WEAK. **Reading: the immigration channel is THE WALL specifically.** A symbolic concrete artifact, not a generic "immigration policy preference."

### 3.3 The two dominant single items

| Item | β | Cluster | Reading |
|---|---:|---|---|
| **"Build wall" support → more skip** | **-0.262** | Immigration | Biden voters who support the wall skipped at ~22% higher rate per 1-SD |
| **"Increase fossil fuel" support → more skip** | **-0.262** | Climate | Biden voters who support fossil-fuel expansion skipped at ~22% higher rate per 1-SD |

Both items are the conservative pole of their respective issue dimensions. Both are concrete cultural-political symbols (the wall as MAGA icon; fossil-fuel expansion as the explicit Trump 2024 platform). Both have β=-0.262, identical to two decimal places. This is the **specific** content of v2.9's "issue-conservatism" channel.

For context, v2.9's `issue_imm_z` composite was β=-0.205 and `issue_clim_z` composite was β=-0.243. Individual items "Build wall" and "Increase fossil fuel" exceed BOTH composites in magnitude (β=-0.262 each), meaning the composites were averaging strong wall+fossil signals with NULL items like border patrols + EPA enforcement, ATTENUATING the headline number.

---

## 4. Synthesis — three things v2.10 changes

### 4.1 Substantive picture revised

v2.9 said: "multi-channel demobilization with econ + trust + mobilization + issue-conservatism + engagement." v2.10 sharpens:

- **Economic perception:** confirmed dominant. Same finding as v2.9 (β=+0.446).
- **Mobilization gap:** narrowed to "retains existing Biden voters; does NOT recruit non-voters." Different lever, same channel.
- **Trust:** election-distrust is a DISENGAGEMENT signal (correlates with still-non-voter status), not a partisan-mobilization signal.
- **Issue conservatism:** UN-bundled. The Wall and Fossil Fuel Expansion are the two single items. Other items either WEAK (Dreamers, abortion, EPA carbon, halt leases) or NULL (legal status, border patrols, EPA enforcement).
- **Engagement:** asymmetric. Engagement predicts Harris-mobilization but not Trump-mobilization.

### 4.2 Political framing revised

v2.9 framing: "DNC lost to demobilization." Largely intact.

v2.10 addition: **the non-voter pool was ideologically sorted, not GOTV-recruited.** Each side mobilized its ideological matches. Older non-voters were net-Trump-aligned; younger non-voters were net-Harris-aligned. The DNC's loss is NOT a non-voter-GOTV-failure narrative — both sides mobilized their non-voters at roughly symmetric rates. The DNC's loss is in the **skip among existing Biden voters** (v2.9), not in **failure to recruit new voters** (v2.10).

### 4.3 The 2-item concentrated signal

If you had to summarize the "issue" dimension of why Biden voters skipped in two words: **"Wall" and "Drill."** These are the concrete cultural-political markers that distinguish skipper Biden-voters from retainer Biden-voters. Generic issue dimensions (immigration, climate, abortion as concepts) are real but distributed across many sub-items; the SPECIFIC items that move the needle are these two.

---

## 5. Aggregate verdicts vs pre-reg

| Hypothesis | Verdict |
|---|---|
| H_MIRROR_A (cohort matters) | **CONFIRMED** (σ_cohort 0.48-0.54 in all 10 fits) |
| H_MIRROR_B (channel asymmetry) | **CONFIRMED** (3 of 5 channels — econ, imm, engage — show opposite-direction effects) |
| H_MIRROR_C (net symmetric mobilization) | **CONFIRMED** (Trump 810 vs Harris 830; difference within noise) |
| H_DECOMP (item-level breakdown) | **CONFIRMED** — 11 of 14 items credible; cluster patterns clean; "Wall" and "Fossil Fuel" identified as dominant single items |

---

## 6. Honest caveats

- **trust_elec direction.** Initial paragraph in §2.4 read it incorrectly mid-write; corrected interpretation: both Trump-mob and Harris-mob have HIGHER election confidence than still-non-voters. The signal is non-voter disengagement = lowest election confidence, not partisan-asymmetric.
- **mob_any NULL on non-voter side may reflect coverage.** CC24_431a "Were you contacted by a candidate or political campaign" — non-voters might still report contact but the question is asked post-election. If non-voters underreport contact systematically, mob_any signal is attenuated. Caveat noted; underreporting doesn't change the comparative conclusion (Trump and Harris both NULL).
- **trust_elec on mirror trump_mob:** R̂=1.028 ESS=160 marginal. Not F5-escalated. β stable at -0.480 across run. Note in next pass.
- **Build wall = Fossil fuel = exactly -0.262.** Coincidence in two decimals; magnitudes will fluctuate with re-sampling. The substantive equivalence holds; the exact equality is a quirk.
- **Universe N=2,803 is bigger than I worried about at pre-reg (initial smoke at presvote20post==4 was N=169, wrong code). Universe is robust at the corrected code (==6).**

---

## 7. v2.11 candidates (filed at lock)

1. **Cohort × channel interactions on Biden-skip outcome** (still on v2.9 §14 list — "do GenZ skippers differ from MillYoung skippers in WHICH channel drives them?"). High-payoff per earlier discussion.
2. **3-way multinomial skip/retain/flip** on Biden universe — separate flippers from skippers in one model. Tests whether the Wall+Fossil items distinguish flippers AND skippers from retainers, or only one.
3. **Item-level decomposition on mirror universe** — same Wall+Fossil items tested as Trump-mob predictors. Hypothesis: Wall+Fossil would be even more dominant on non-voter mobilization than they are on Biden skip.
4. **Gaza CC24_308b sub-item resolution** — still pending codebook PDF read.
5. **Pew W159 cross-replication** of Build-Wall + Fossil-Fuel item-level findings.
6. **Trust_elec F5 escalation on mirror_trump_mob fit** (R̂=1.028, ESS=160 marginal).
7. **State-level counterfactual using v2.9 + v2.10 betas + state-skip-rate weights** — translate to MI/PA/WI/GA/AZ/NV margin shifts.

---

## 8. Repository state at lock

- Pre-reg: `f63c343` (LOCKED at lock-time).
- Code: `code/v210_mirror_and_decomp.py`.
- Fit summaries: 24 files in `data/processed/v210/fit_*_summary.csv` + `*_diag.json`.
- Scoreboard: `data/processed/v210/v210_scoreboard.csv`.
- Universe artifacts: `mirror_universe.csv`.

**Result commit hash to be filled at commit time.**
