# Raw Substrate Data Inventory

**Last updated:** 2026-05-22
**Pre-reg companion:** `../../prereg_v1.0_dnc_postmortem.md` (locked at commit `45ea69a`)

All raw data files (`.csv`, `.dta`, `.zip`, `.sas7bdat`, etc.) are gitignored. Documentation PDFs and this README track. Downloads landed via `curl` from public URLs unless noted as registration-required.

---

## Directly downloaded (✓ in place)

### `ap_votecast_2024/`
- **Source:** https://apnorc.org/wp-content/uploads/2021/05/AP_VOTECAST_2024_GENERAL.zip (95 MB)
- **Files extracted:** `AP_VOTECAST_2024_GENERAL.csv` (367 MB), `AP_VOTECAST_2024_GENERAL.sas` (variable manifest), `AP_VOTECAST_2024_GENERAL_CODEBOOK.pdf` (4.2 MB), `AP_VOTECAST_2024_GENERAL_QUESTIONNAIRE.pdf` (515 KB)
- **Verified shape:** 139,938 respondents × 466 columns
- **Role:** Vote-choice + demographic decomposition + Israel/Gaza single-issue (per pre-reg §2 + 2026-05-22 codebook pull)
- **Note:** Age banded (6 levels) — disclosure-suppressed continuous age. Cohort coding lossy per operationalization supplement §3.2.

### `ces_2024/`
- **Source:** Harvard Dataverse DOI 10.7910/DVN/X11EP6 → file IDs 12050325 (CSV), 12050326 (guide PDF), 11032062 + 11049825 (pre/post questionnaire DOCX)
- **Files in place:** `CCES24_Common_OUTPUT_vv_topost_final.csv` (176 MB), `CES_2024_GUIDE_vv.pdf` (1.2 MB), `CCES24_Common_pre.docx`, `CCES24_Common_post.docx`
- **Verified shape:** 60,000 respondents × 694 columns. `birthyr` continuous (cohort coding feasible), `gender4`, `educ`, `race`, `hispanic`, `inputstate`, `region`, `pid3`, `pid7` all present.
- **Stata file (993 MB) NOT downloaded** — CSV sufficient for our analysis.
- **Role:** Scale-on-subset (3/6 issues: healthcare + structural inequity + race-attitudes battery).

### `cps_asec_2025/`
- **Source:** https://www2.census.gov/programs-surveys/cps/datasets/2025/march/asecpub25csv.zip (141 MB)
- **Files extracted:** `hhpub25.csv` (32 MB), `ffpub25.csv` (14 MB), `pppub25.csv` (266 MB), `asec_csv_repwgt_2025.csv` (283 MB), `asec2025_ddl_pub_full.pdf` (data dictionary)
- **Verified shape:** Person file `pppub25.csv` = 142,125 persons × 844 columns
- **Role:** Pay-structure imputation backbone (per pre-reg §8). ASEC alone does NOT carry direct hourly/salary; the PAIDHRE variable lives in CPS monthly Outgoing Rotation Group (ORG) — see `cps_org_2024/` below for the registration-required IPUMS extract.

### `gss_2024/`
- **Source:** https://www.norc.org/content/dam/gss/get-the-data/documents/stata/2024_stata.zip (5.1 MB)
- **Files extracted:** `2024/GSS2024.dta`, `2024/GSS 2024 Codebook R3.pdf`, `2024/GSS 2024 Release Variables R3.pdf`, `2024/Release Notes 7224 R3.pdf`, `2024/GSS 2024 - Whats New R3.pdf`
- **Verified shape:** 3,986 respondents × 980 columns
- **Variables confirmed:** `natsci` (n=3815 non-null), `nataid` + `nataidy` (split-ballot Y-wording, ~1900 each), `natheal`, `natfare`, `cohort` (continuous), `age`, `race`, `sex`, `educ`, `region`, `partyid`, `pres20`
- **DEVIATIONS LOGGED (pre-reg §12, 2026-05-22):**
  - `natarts` NOT in 2024 wave → Issue 5 collapses to science-only on GSS
  - No insurance-status variable → GSS drops out of Model B insurance-pool analysis
- **`pres24` also absent:** GSS 2024 doesn't have 2024 presidential vote choice; GSS contributes to issue-attitude analysis only, not vote-choice decomposition. (Already implied by pre-reg's Tier 2 framing; noted explicitly here.)

---

## Registration-required (manual steps — user action needed)

### `anes_2024/` — ✓ DOWNLOADED 2026-05-22 (user via Chrome agent)
**Status:** Files in place.
**Verified shape:** 5,521 × 1,738 columns.
**Variables confirmed (key V-codes):**
- V241458x = continuous age (range 18-80, top-coded at 80, n=5,242)
- V241455 = birth year, **RESTRICTED** in public file (all -3) — §12 deviation
- V241404 = Israel/Palestinian humanitarian aid (confirmed real Israel/Gaza item)
- V242577a-g = social media platform indicators (FB, X, Instagram, Reddit, YouTube, etc.)
- V242350 = pay structure (verify hourly/salary semantics at impl time)
- Many V-codes in V241xxx and V242xxx ranges cover the six-issue battery; exact V-code → item mapping is implementation-time work per operationalization supplement §7
- **Caveat:** Earlier verification "CONFIRMED" status was over-confident on specific V-codes (e.g., V242176 turned out to be abortion-importance, not Israel). Verify each item's actual codebook label before locking it into a Stan dataset variable.
**Steps:**
1. Register a free account at https://electionstudies.org/ (click "Register" in top-right)
2. Verify email
3. Navigate to https://electionstudies.org/data-center/2024-time-series-study/
4. Download the **2024 Time Series Study — Full Release** package (the 2025-08-08 release with the 2025-09-08 codebook). Choose the Stata `.dta` format. Also download:
   - User guide / codebook PDF (`anes_timeseries_2024_userguidecodebook_20250808.pdf`)
   - Questionnaire PDF
5. Save all files into `data/raw/anes_2024/`

**What we need from ANES 2024:**
- Full 6-issue battery (Israel military aid + Palestinian humanitarian aid; government health insurance scale; racial inequity battery; race-relations item; federal spending science + arts; foreign aid spending)
- Exposure pools (platform indicators for FB / X / Instagram / Reddit / YouTube / Snapchat / TikTok + frequency × political-content for FB and X; insurance status; hourly/salary employment item)
- Birth year continuous (cohort coding)
- 2020 vote recall + 2024 vote choice
- Panel re-interview flag (n=2,070 from 2016-2020 ANES Panel)

### `cps_org_2024/` — ✓ DOWNLOADED 2026-05-22 (IPUMS extract #2918366)
**Status:** Files in place. Fixed-width `.dat` decompressed; Stata `.do` reader spec + codebook `.cbk` present.
**Files:**
- `cps_00001.dat.gz` (25 MB compressed) + `cps_00001.dat` (143 MB decompressed)
- `cps_00001.do` (Stata reader: variable positions + scaling factors)
- `cps_00001.cbk` (codebook with variable layout + value labels)
**Verified shape:** 1,187,356 person-month records across Jan-Dec 2024 from CPS basic monthly samples.
**ORG-eligible subset (PAIDHOUR > 0):** 125,880 records — 70,268 paid hourly + 55,612 salaried — this is the P(hourly) imputation training sample.
**Variables (25 total):** YEAR, SERIAL, MONTH, HWTFINL, CPSID, ASECFLAG, REGION, STATEFIP, PERNUM, WTFINL, CPSIDP, CPSIDV, EARNWEEK2, HOURWAGE2, AGE, SEX, RACE, HISPAN, EMPSTAT, LABFORCE, OCC2010, IND, UHRSWORKT, EDUC, PAIDHOUR
**Note:** The extract is full CPS basic-monthly (not pre-filtered to ORG). PAIDHOUR > 0 identifies ORG respondents — the rest are non-ORG and have PAIDHOUR=0. Filter in pipeline.
**Scaling factors (from `.do`):** EARNWEEK2 / 100, HOURWAGE2 / 100, WTFINL / 10000.
**Steps:**
1. Register a free account at https://cps.ipums.org/cps/ (IPUMS-CPS)
2. Build an extract via the IPUMS CPS extract builder:
   - Sample selection: **Monthly Outgoing Rotation Group (ORG)** samples for **all months of 2024** (Jan 2024 — Dec 2024, 12 monthly files)
   - Variables (minimum needed):
     - `PAIDHRE` (paid hourly Y/N — the imputation training label)
     - `OCC2010` (Census 2010 harmonized occupation codes)
     - `IND` (industry)
     - `UHRSWORKT` (usual hours worked)
     - `EARNHRLY` (hourly earnings)
     - `EARNWEEK` (weekly earnings)
     - `AGE`, `SEX`, `RACE`, `HISPAN`, `EDUC`, `EDUCD` (educational attainment)
     - `STATEFIP`, `REGION`
     - `EMPSTAT`, `LABFORCE` (labor force status)
     - `WTFINL` (final weight)
3. Wait for extract email (typically minutes to hours)
4. Download CSV or Stata file + the codebook PDF
5. Save into `data/raw/cps_org_2024/`

**Alternative:** Census direct monthly CPS basic files at https://www.census.gov/data/datasets/time-series/demo/cps/cps-basic.html — but uses non-harmonized variable names across months. IPUMS is preferred.

**What we need from CPS ORG:**
- Train logistic regression P(hourly | occupation × industry × hours × earnings × demographics) per pre-reg §8 Step 1
- Apply to ANES + CES political-survey respondents (those have occupation + earnings + demographics but no hourly/salary)
- 50-draw multiple-imputation propagation through Model B / C

### `pew_vv_2024/` — ✓ DOWNLOADED 2026-05-22 (user via Chrome agent)
**Status:** Files in place at `pew_vv_2024/W159_Nov24/`.
**Verified shape:** 9,609 × 169 columns (CSV + SPSS .sav both included).
**Variables confirmed:**
- `VOTED2024`, `VOTECHOICE2024`, `VOTESTATUS2024` — vote validation against voter file
- `VOTED2020/2018/2016` + `VOTECHOICE2020/2018/2016` — retrospective validation back to 2016
- `WEIGHT_W159_VALIDATEDVOTE` — validated-vote weight, n=9,240 non-NaN
- `F_AGECAT` — 4-band age categorical (NOT continuous birth year) — §12 deviation
- `F_RACECMB`, `F_GENDER`, `F_EDUCCAT/2`, `F_CREGION`, `F_PARTY_FINAL`, `F_IDEO` — demographic + party
- `DTCONF_ECON/IMMI/ABCN/CRIM/FRGN/CLSR_W159` — Trump-confidence on 6 issue areas (competence ratings, NOT position items; not in our issue battery)
- `THERMTRUMP/HARRIS_W159` — feeling thermometers
**Role:** Turnout-vs-choice separation + 2020 vote validation (confirmed; matches pre-reg §2 role lock).
**Steps:**
1. Register a free Pew account at https://www.pewresearch.org/dataset/ (click "Create an account")
2. Verify email + sign user agreement
3. Search for "Validated Voters 2024" or navigate via the methodology page https://www.pewresearch.org/politics/2025/06/26/validated-voters-2024-methodology/
4. Download the microdata file (SPSS `.sav` and/or `.csv`) for ATP Wave 159 + the validated-voter merge file
5. Also download (these are public, no registration):
   - Topline / questionnaire PDF: https://www.pewresearch.org/wp-content/uploads/sites/20/2025/06/PP-2025.6.26_validated-voters_questionnaire.pdf
   - Full report PDF: https://www.pewresearch.org/wp-content/uploads/sites/20/2025/06/PP-2025.6.26_validated-voters_report.pdf
6. Save into `data/raw/pew_vv_2024/`

**What we need from Pew VV 2024:**
- Validated turnout marker (Y/N from voter-file match against 3 commercial files; 7,100 of 8,942 validated)
- Self-reported vote choice for choice-among-validated-voters analysis
- Demographics (race / education / age / gender / state) via panel profile
- NOTE per 2026-05-22 questionnaire pull: 0 of 6 issue items in this wave; Pew VV does NOT contribute to the issue-battery analysis. Role-locked to turnout-vs-choice separation.

---

## Summary table

| Substrate | Status | Source | N | Issue items | Cohort coding |
|---|---|---|---|---|---|
| ANES 2024 | **REGISTRATION REQUIRED** | electionstudies.org | 5,521 + 2,070 panel | 6/6 (full battery) | Continuous birthyr |
| CES 2024 | ✓ Downloaded | Harvard Dataverse | 60,000 | 3/6 (healthcare + struct-inequity + race) | Continuous `birthyr` |
| AP VoteCast 2024 | ✓ Downloaded | apnorc.org | 139,938 | 2/6 (Israel + struct-racism partial) | Banded (6 levels, lossy) |
| Pew VV 2024 | **REGISTRATION REQUIRED** (PDFs public) | pewresearch.org/dataset | 8,942 (7,100 validated) | 0/6 (turnout substrate only) | Panel-profile continuous |
| GSS 2024 | ✓ Downloaded | norc.org | 3,986 | natsci + nataid only (Tier 2 spending; natarts absent — §12 deviation) | Continuous `cohort` |
| CPS ASEC 2025 | ✓ Downloaded | census.gov | 142,125 persons | n/a (labor-market backbone) | Continuous |
| CPS ORG 2024 | ✓ Downloaded (IPUMS #2918366) | cps.ipums.org | 1,187,356 person-months Jan-Dec 2024; 125,880 ORG-eligible (PAIDHOUR>0) | n/a (PAIDHOUR imputation training) | Continuous AGE |

---

## Disk usage (approximate)

- AP VoteCast: 467 MB (after extract, CSV format)
- CES: 178 MB
- CPS ASEC: 735 MB (after extract, CSV format with replicate weights)
- GSS: 5 MB
- **Total directly downloaded: ~1.4 GB**
- **Pending (ANES + IPUMS-CPS-ORG + Pew VV): another ~0.5-1 GB estimated**
