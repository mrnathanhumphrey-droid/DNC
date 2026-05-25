"""v2.9 — GenZ-skip mechanism on CES VV Biden-2020 universe.

Per prereg_v2.9_dnc_postmortem.md (LOCKED bae6e0c) + prereg_v2.9_amendment_2026_05_24.md.
5 hypotheses C/A/E/D/B with V-codes corrected post-codebook verification.

H_SKIP_C: 6 issue z-scores (econ/inflation/gaza/imm/abor/clim)
H_SKIP_A: engagement composite (CC24_430a + CC24_430b)
H_SKIP_E: cohort x race interaction
H_SKIP_D: trust composite (CC24_423/424 + CC24_421)
H_SKIP_B: mobilization (CC24_431a + CC24_431b)

Settings: chains=6, warmup=1000, samples=1000, seed=42.
"""

from pathlib import Path
import json
import os
import joblib
import numpy as np
import pandas as pd

RTOOLS_PATHS = [
    r"C:\Users\Nate\.cmdstan\RTools40\usr\bin",
    r"C:\Users\Nate\.cmdstan\RTools40\mingw64\bin",
]
for p in RTOOLS_PATHS:
    if p not in os.environ.get("PATH", ""):
        os.environ["PATH"] = p + ";" + os.environ.get("PATH", "")

from cmdstanpy import CmdStanModel

RAW = Path("D:/DNC/data/raw/ces_2024/CCES24_Common_OUTPUT_vv_topost_final.csv")
STAN_DIR = Path("D:/DNC/code/stan")
OUT_DIR = Path("D:/DNC/data/processed/v29")
OUT_DIR.mkdir(parents=True, exist_ok=True)

SEED = 42
CHAINS = 6
WARMUP = 1000
SAMPLES = 1000

COHORT_ORDER = ["Silent", "Boomer", "GenX", "MillOld", "MillYoung", "GenZ"]
RACE_ORDER = ["white", "black", "hispanic", "asian", "nhpi", "other"]


def birthyr_to_cohort6(by):
    if pd.isna(by) or by < 1900 or by > 2010:
        return np.nan
    if by >= 1997: return "GenZ"
    if by >= 1989: return "MillYoung"
    if by >= 1981: return "MillOld"
    if by >= 1965: return "GenX"
    if by >= 1946: return "Boomer"
    return "Silent"


def _z(s):
    s = pd.to_numeric(s, errors="coerce")
    return (s - s.mean()) / s.std(ddof=0)


def build_universe():
    print("=== Loading CES ===")
    df = pd.read_csv(RAW, low_memory=False)
    print(f"  CES total N = {len(df)}")

    mask = (
        df["vvweight_post"].notna() & (df["vvweight_post"] > 0)
        & (df["presvote20post"] == 1)
        & df["birthyr"].notna()
        & (df["birthyr"] >= 1900) & (df["birthyr"] <= 2010)
        & df["TS_g2024"].notna()
    )
    biden = df[mask].copy()
    print(f"  VV + Biden-2020 + valid birthyr + TS populated: N = {len(biden)}")

    biden["cohort6"] = biden["birthyr"].apply(birthyr_to_cohort6)
    biden = biden[biden["cohort6"].notna()].copy()

    def bucket(row):
        ts = row["TS_g2024"]
        cc = row["CC24_410"]
        if pd.isna(ts):
            return None
        if ts == 7:
            return 1
        if ts in [1, 2, 3, 4, 5, 6]:
            if pd.isna(cc):
                return None
            if cc == 1:
                return 0
            return None
        return None

    biden["skipped"] = biden.apply(bucket, axis=1)
    biden = biden[biden["skipped"].notna()].copy()
    biden["skipped"] = biden["skipped"].astype(int)
    print(f"  After outcome filter (skip|retain ONLY): N = {len(biden)}")
    print(f"  Skip prevalence: {biden['skipped'].mean()*100:.2f}%")

    race_map = {1: "white", 2: "black", 3: "hispanic", 4: "asian",
                5: "nhpi", 6: "other", 7: "other", 8: "other"}
    biden["race"] = biden["race"].map(race_map)
    educ_map = {1: "lt_hs", 2: "hs", 3: "some_col", 4: "some_col", 5: "ba", 6: "grad"}
    biden["educ"] = biden["educ"].map(educ_map)
    gender_map = {1: "man", 2: "woman", 3: "nb", 4: "other"}
    biden["gender"] = biden["gender4"].map(gender_map)
    region_map = {1: "NE", 2: "MW", 3: "South", 4: "West"}
    biden["region"] = biden["region"].map(region_map)

    needed = ["race", "educ", "gender", "region", "cohort6"]
    biden = biden.dropna(subset=needed).copy()
    print(f"  After demographic completeness: N = {len(biden)}")

    print("\n  Per-cohort skip prevalence:")
    for c in COHORT_ORDER:
        sub = biden[biden["cohort6"] == c]
        if len(sub) > 0:
            print(f"    {c}: N={len(sub)}, skip%={sub['skipped'].mean()*100:.2f}")

    return biden


def build_baseline_fundamentals(df):
    pid7 = pd.to_numeric(df.get("pid7"), errors="coerce")
    pid7 = pid7.where((pid7 >= 1) & (pid7 <= 7))
    df["pid7_z"] = ((pid7 - pid7.mean()) / pid7.std(ddof=0)).fillna(0.0)

    faminc = pd.to_numeric(df.get("faminc_new"), errors="coerce")
    faminc = faminc.where((faminc >= 1) & (faminc <= 16))
    df["faminc_z"] = ((faminc - faminc.mean()) / faminc.std(ddof=0)).fillna(0.0)

    emp = pd.to_numeric(df.get("employ"), errors="coerce")
    df["emp_employed"] = emp.isin([1, 2]).astype(int)
    df["emp_unemployed"] = (emp == 4).astype(int)
    df["emp_retired"] = (emp == 5).astype(int)

    return df


def build_predictors(df):
    """V-codes per amendment 2026-05-24."""

    # ---------- H_SKIP_C: ISSUES (6 dimensions) ----------
    # CC24_301 National Economics (1=Excellent..5=Poor, 6=Not sure). Higher = WORSE = more dissatisfaction.
    e = df["CC24_301"].where(df["CC24_301"].between(1, 5))
    df["issue_econ_z"] = _z(e).fillna(0.0)

    # CC24_303 Price change in past year (1-5; higher = bigger increase = more dissatisfaction)
    p = df["CC24_303"].where(df["CC24_303"].between(1, 5))
    df["issue_inflation_z"] = _z(p).fillna(0.0)

    # CC24_308b_1..9 Israel/Gaza grid (binary 1=support/agree, 2=oppose/disagree per row)
    # Treat as composite mean of recoded items (1=support, 0=oppose)
    gaza_cols = [f"CC24_308b_{i}" for i in range(1, 10) if f"CC24_308b_{i}" in df.columns]
    for c in gaza_cols:
        df[c + "_p"] = df[c].map({1: 1, 2: 0})
    df["issue_gaza_raw"] = df[[c + "_p" for c in gaza_cols]].mean(axis=1)
    df["issue_gaza_z"] = _z(df["issue_gaza_raw"]).fillna(0.0)

    # CC24_323a/b immigration (binary; recode 1->1 progressive, 2->0)
    for c in ["CC24_323a", "CC24_323b"]:
        df[c + "_p"] = df[c].map({1: 1, 2: 0})
    df["issue_imm_raw"] = df[["CC24_323a_p", "CC24_323b_p"]].mean(axis=1)
    df["issue_imm_z"] = _z(df["issue_imm_raw"]).fillna(0.0)

    # CC24_326a/b abortion
    for c in ["CC24_326a", "CC24_326b"]:
        df[c + "_p"] = df[c].map({1: 1, 2: 0})
    df["issue_abor_raw"] = df[["CC24_326a_p", "CC24_326b_p"]].mean(axis=1)
    df["issue_abor_z"] = _z(df["issue_abor_raw"]).fillna(0.0)

    # CC24_330a/b climate (8-pt ordinal)
    for c in ["CC24_330a", "CC24_330b"]:
        df[c + "_v"] = df[c].where(df[c].between(1, 8))
    df["issue_clim_raw"] = df[["CC24_330a_v", "CC24_330b_v"]].mean(axis=1)
    df["issue_clim_z"] = _z(df["issue_clim_raw"]).fillna(0.0)

    # ---------- H_SKIP_A: ENGAGEMENT ----------
    # CC24_430a_1..8 — Past year political activity (binary 1=did, 2=didn't)
    act_cols = [f"CC24_430a_{i}" for i in range(1, 9) if f"CC24_430a_{i}" in df.columns]
    for c in act_cols:
        df[c + "_p"] = df[c].map({1: 1, 2: 0})
    df["engage_act_raw"] = df[[c + "_p" for c in act_cols]].mean(axis=1)
    df["engage_act_z"] = _z(df["engage_act_raw"]).fillna(0.0)

    # CC24_430b_1..10 — Donate money (binary 1=donated to this cat, 2=didn't)
    don_cols = [f"CC24_430b_{i}" for i in range(1, 11) if f"CC24_430b_{i}" in df.columns]
    for c in don_cols:
        df[c + "_p"] = df[c].map({1: 1, 2: 0})
    df["engage_donate_raw"] = df[[c + "_p" for c in don_cols]].mean(axis=1)
    df["engage_donate_z"] = _z(df["engage_donate_raw"]).fillna(0.0)

    # Composite
    df["engage_composite_z"] = _z(
        df[["engage_act_z", "engage_donate_z"]].mean(axis=1)
    ).fillna(0.0)

    # ---------- H_SKIP_D: TRUST ----------
    # CC24_423 trustfed (1=most..3=least, 8=DK). Recode: 1->3, 2->2, 3->1, 8->NaN
    # Then HIGHER = MORE trust.
    df["trust_fed_v"] = df["CC24_423"].map({1: 3, 2: 2, 3: 1, 8: np.nan})
    df["trust_state_v"] = df["CC24_424"].map({1: 3, 2: 2, 3: 1, 8: np.nan})
    df["trust_gov_raw"] = df[["trust_fed_v", "trust_state_v"]].mean(axis=1)
    df["trust_gov_z"] = _z(df["trust_gov_raw"]).fillna(0.0)

    # CC24_421_1, CC24_421_2 election fairness (5-pt; verify direction pre-fit, treat as
    # higher = more confidence assumed; verify in §10)
    for c in ["CC24_421_1", "CC24_421_2"]:
        df[c + "_v"] = df[c].where(df[c].between(1, 5))
    df["trust_elec_raw"] = df[["CC24_421_1_v", "CC24_421_2_v"]].mean(axis=1)
    df["trust_elec_z"] = _z(df["trust_elec_raw"]).fillna(0.0)

    df["trust_combined_z"] = _z(
        df[["trust_gov_z", "trust_elec_z"]].mean(axis=1)
    ).fillna(0.0)

    # ---------- H_SKIP_B: MOBILIZATION ----------
    # CC24_431a binary (1=contacted, 2=not) — recode 1->1, 2->0
    df["mob_any_raw"] = df["CC24_431a"].map({1: 1, 2: 0})
    df["mob_any_z"] = _z(df["mob_any_raw"]).fillna(0.0)
    # CC24_431b_1 = contact via Dems (binary 1=yes/2=no, conditional on 431a==1)
    # Build: contacted AND by Dems specifically
    df["mob_dem_raw"] = np.where(
        (df["CC24_431a"] == 1) & (df["CC24_431b_1"] == 1),
        1,
        np.where(df["CC24_431a"] == 2, 0, 0),  # not contacted = 0
    )
    df["mob_dem_z"] = _z(df["mob_dem_raw"]).fillna(0.0)

    return df


def make_indices(df):
    educ_levels = ["lt_hs", "hs", "some_col", "ba", "grad"]
    gender_levels = ["man", "woman", "nb", "other"]
    region_levels = ["NE", "MW", "South", "West"]

    df["race_idx"] = df["race"].apply(lambda x: RACE_ORDER.index(x) + 1)
    df["educ_idx"] = df["educ"].apply(lambda x: educ_levels.index(x) + 1)
    df["cohort_idx"] = df["cohort6"].apply(lambda x: COHORT_ORDER.index(x) + 1)
    df["gender_idx"] = df["gender"].apply(lambda x: gender_levels.index(x) + 1)
    df["region_idx"] = df["region"].apply(lambda x: region_levels.index(x) + 1)
    return df, len(RACE_ORDER), len(educ_levels), len(COHORT_ORDER), len(gender_levels), len(region_levels)


def make_stan_data(df, fund_cols):
    df_clean = df.dropna(subset=fund_cols).copy()
    X_fund = df_clean[fund_cols].values.astype(float)
    data = {
        "N": len(df_clean),
        "K_fund": len(fund_cols),
        "X_fund": X_fund,
        "N_race": len(RACE_ORDER),
        "N_educ": 5,
        "N_cohort": 6,
        "N_gender": 4,
        "N_region": 4,
        "race": df_clean["race_idx"].astype(int).values,
        "educ": df_clean["educ_idx"].astype(int).values,
        "cohort": df_clean["cohort_idx"].astype(int).values,
        "gender": df_clean["gender_idx"].astype(int).values,
        "region": df_clean["region_idx"].astype(int).values,
        "y": df_clean["skipped"].astype(int).values,
        "weight": df_clean["vvweight_post"].astype(float).values,
    }
    return data, df_clean


def fit_one(tag, data, model_stan="model_a.stan", chains=CHAINS, warmup=WARMUP, samples=SAMPLES):
    print(f"\n=== [{tag}] N={data['N']} K_fund={data['K_fund']} model={model_stan} ===")
    model = CmdStanModel(stan_file=STAN_DIR / model_stan)
    fit = model.sample(
        data=data, chains=chains,
        iter_warmup=warmup, iter_sampling=samples,
        seed=SEED, show_progress=False, refresh=500,
        parallel_chains=chains,
    )
    summary = fit.summary()
    max_rhat = float(summary["R_hat"].max())
    min_ess = float(summary["ESS_bulk"].min()) if "ESS_bulk" in summary.columns else float(summary["N_Eff"].min())
    divergent = int(np.array(fit.method_variables()["divergent__"]).sum())

    out_csv = OUT_DIR / f"fit_{tag}_summary.csv"
    summary.to_csv(out_csv)
    diag = {"tag": tag, "N": int(data["N"]), "K_fund": int(data["K_fund"]),
            "chains": chains, "warmup": warmup, "samples": samples,
            "max_rhat": max_rhat, "min_ess_bulk": min_ess, "divergent": divergent}
    (OUT_DIR / f"fit_{tag}_diag.json").write_text(json.dumps(diag, indent=2))
    print(f"  R-hat={max_rhat:.4f} ESS={min_ess:.0f} div={divergent}")
    return fit, summary, diag


def coef_row(summary, name):
    if name not in summary.index:
        return None
    row = summary.loc[name]
    mean = float(row["Mean"])
    q5 = float(row["5%"])
    q95 = float(row["95%"])
    credible = (q5 > 0) or (q95 < 0)
    return mean, q5, q95, credible


def main():
    df = build_universe()
    df = build_baseline_fundamentals(df)
    df = build_predictors(df)
    df, _, _, _, _, _ = make_indices(df)
    df.to_csv(OUT_DIR / "universe.csv", index=False)

    universe_n = len(df)
    skip_pct = df["skipped"].mean() * 100
    n_skip = int(df["skipped"].sum())
    print(f"\n=== Universe ===")
    print(f"  N = {universe_n}, skip% = {skip_pct:.2f}%, n_skip = {n_skip}")
    f1_ok = universe_n >= 12000
    print(f"  F1 (N>=12000): {'PASS' if f1_ok else 'FAIL'}")
    print(f"  Amendment F2 (n_skip >= 600 events): {'PASS' if n_skip >= 600 else 'FAIL'}")

    BASE_FUND = ["pid7_z", "faminc_z", "emp_employed", "emp_unemployed", "emp_retired"]
    results = {}

    # ============ H_SKIP_C: 6 issue fits ============
    print("\n" + "=" * 60); print("H_SKIP_C — ISSUE DISSATISFACTION (6 dimensions)"); print("=" * 60)
    for issue in ["issue_econ_z", "issue_inflation_z", "issue_gaza_z",
                   "issue_imm_z", "issue_abor_z", "issue_clim_z"]:
        fund_cols = BASE_FUND + [issue]
        data, _ = make_stan_data(df, fund_cols)
        tag = f"skip_C_{issue}"
        _, summary, diag = fit_one(tag, data)
        beta_idx = len(fund_cols)
        r = coef_row(summary, f"beta_fund[{beta_idx}]")
        if r:
            mean, q5, q95, credible = r
            print(f"  [{issue}] beta = {mean:+.3f} [{q5:+.3f}, {q95:+.3f}] credible={credible}")
            results[tag] = {"mean": mean, "q5": q5, "q95": q95, "credible": credible, "diag": diag}

    # ============ H_SKIP_A: engagement ============
    print("\n" + "=" * 60); print("H_SKIP_A — ENGAGEMENT"); print("=" * 60)
    for predictor in ["engage_composite_z", "engage_act_z", "engage_donate_z"]:
        fund_cols = BASE_FUND + [predictor]
        data, _ = make_stan_data(df, fund_cols)
        tag = f"skip_A_{predictor}"
        _, summary, diag = fit_one(tag, data)
        beta_idx = len(fund_cols)
        r = coef_row(summary, f"beta_fund[{beta_idx}]")
        if r:
            mean, q5, q95, credible = r
            print(f"  [{predictor}] beta = {mean:+.3f} [{q5:+.3f}, {q95:+.3f}] credible={credible}")
            results[tag] = {"mean": mean, "q5": q5, "q95": q95, "credible": credible, "diag": diag}

    # ============ H_SKIP_D: trust ============
    print("\n" + "=" * 60); print("H_SKIP_D — TRUST"); print("=" * 60)
    for predictor in ["trust_gov_z", "trust_elec_z", "trust_combined_z"]:
        fund_cols = BASE_FUND + [predictor]
        data, _ = make_stan_data(df, fund_cols)
        tag = f"skip_D_{predictor}"
        _, summary, diag = fit_one(tag, data)
        beta_idx = len(fund_cols)
        r = coef_row(summary, f"beta_fund[{beta_idx}]")
        if r:
            mean, q5, q95, credible = r
            print(f"  [{predictor}] beta = {mean:+.3f} [{q5:+.3f}, {q95:+.3f}] credible={credible}")
            results[tag] = {"mean": mean, "q5": q5, "q95": q95, "credible": credible, "diag": diag}

    # ============ H_SKIP_B: mobilization ============
    print("\n" + "=" * 60); print("H_SKIP_B — MOBILIZATION"); print("=" * 60)
    for predictor in ["mob_any_z", "mob_dem_z"]:
        fund_cols = BASE_FUND + [predictor]
        data, _ = make_stan_data(df, fund_cols)
        tag = f"skip_B_{predictor}"
        _, summary, diag = fit_one(tag, data)
        beta_idx = len(fund_cols)
        r = coef_row(summary, f"beta_fund[{beta_idx}]")
        if r:
            mean, q5, q95, credible = r
            print(f"  [{predictor}] beta = {mean:+.3f} [{q5:+.3f}, {q95:+.3f}] credible={credible}")
            results[tag] = {"mean": mean, "q5": q5, "q95": q95, "credible": credible, "diag": diag}

    # ============ H_SKIP_E: cohort x race interaction ============
    print("\n" + "=" * 60); print("H_SKIP_E — COHORT x RACE INTERACTION"); print("=" * 60)
    fund_cols = BASE_FUND
    data, df_e = make_stan_data(df, fund_cols)
    tag = "skip_E_cohort_x_race"
    fit_e, summary_e, diag_e = fit_one(tag, data, model_stan="model_a_interaction.stan",
                                        chains=4, warmup=750, samples=750)

    cell_lifts = []
    for ci, coh in enumerate(COHORT_ORDER, start=1):
        for ri, race in enumerate(RACE_ORDER, start=1):
            name = f"cohort_race_eff[{ci},{ri}]"
            if name in summary_e.index:
                row = summary_e.loc[name]
                cell_lifts.append({
                    "cohort": coh, "race": race,
                    "logit_mean": float(row["Mean"]),
                    "logit_q5": float(row["5%"]), "logit_q95": float(row["95%"]),
                    "cell_n": int(((df_e["cohort_idx"] == ci) & (df_e["race_idx"] == ri)).sum()),
                })
    cell_df = pd.DataFrame(cell_lifts)
    cell_df.to_csv(OUT_DIR / "skip_E_cell_lifts.csv", index=False)
    print(f"  Cell-table saved: {OUT_DIR / 'skip_E_cell_lifts.csv'}")

    print("\n  CANDIDATE CELLS:")
    for coh, race in [("GenZ", "black"), ("GenZ", "hispanic"), ("MillYoung", "hispanic")]:
        row = cell_df[(cell_df["cohort"] == coh) & (cell_df["race"] == race)]
        if len(row):
            r = row.iloc[0]
            credible = (r["logit_q5"] > 0) or (r["logit_q95"] < 0)
            print(f"    {coh} x {race}: logit_lift = {r['logit_mean']:+.3f} "
                  f"[{r['logit_q5']:+.3f}, {r['logit_q95']:+.3f}] N={r['cell_n']} credible={credible}")
    results[tag] = {"diag": diag_e, "cell_table": str(OUT_DIR / "skip_E_cell_lifts.csv")}

    # Scoreboard
    scoreboard = []
    for tag, r in results.items():
        if "mean" in r:
            mag = abs(r["mean"])
            if not r["credible"] or mag < 0.05:
                verdict = "NULL"
            elif mag < 0.10:
                verdict = "INDET"
            elif mag < 0.20:
                verdict = "WEAK"
            else:
                verdict = "STRONG"
            scoreboard.append({"tag": tag, "mean": r["mean"], "q5": r["q5"], "q95": r["q95"],
                              "credible": r["credible"], "verdict": verdict,
                              "max_rhat": r["diag"]["max_rhat"], "min_ess": r["diag"]["min_ess_bulk"]})
    sb_df = pd.DataFrame(scoreboard)
    sb_df.to_csv(OUT_DIR / "v29_scoreboard.csv", index=False)
    print("\n=== v2.9 SCOREBOARD ===")
    print(sb_df.to_string(index=False))


if __name__ == "__main__":
    main()
