"""v2.10 — Non-voter mirror (H_MIRROR) + Issue decomposition (H_DECOMP).

Per prereg_v2.10_dnc_postmortem.md (LOCKED f63c343).

PART 1 H_MIRROR: CES VV 2020 non-voters (presvote20post==6, 18+ in 2020).
  Outcome 1: trump_mob (1=mobilized for Trump, 0=stayed non-voter)
  Outcome 2: harris_mob (1=mobilized for Harris, 0=stayed non-voter)
  5 channel predictors from v2.9: mob_any, engage_act, issue_econ, issue_imm, trust_elec

PART 2 H_DECOMP: CES VV Biden-2020 skip universe (same as v2.9, N=17,401).
  Outcome: skipped (1=skipped, 0=retained Harris)
  14 item-level predictors: 4 abortion + 6 climate + 4 immigration.

Settings: chains=6, warmup=1000, samples=1000, seed=42.
"""

from pathlib import Path
import json
import os
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
OUT_DIR = Path("D:/DNC/data/processed/v210")
OUT_DIR.mkdir(parents=True, exist_ok=True)

SEED = 42
CHAINS = 6
WARMUP = 1000
SAMPLES = 1000

COHORT_ORDER = ["Silent", "Boomer", "GenX", "MillOld", "MillYoung", "GenZ"]
RACE_ORDER = ["white", "black", "hispanic", "asian", "nhpi", "other"]


def birthyr_to_cohort6(by, max_yr=2010):
    if pd.isna(by) or by < 1900 or by > max_yr:
        return np.nan
    if by >= 1997: return "GenZ"
    if by >= 1989: return "MillYoung"
    if by >= 1981: return "MillOld"
    if by >= 1965: return "GenX"
    if by >= 1946: return "Boomer"
    return "Silent"


def _z(s):
    s = pd.to_numeric(s, errors="coerce")
    if s.std(ddof=0) == 0 or s.notna().sum() == 0:
        return pd.Series(0.0, index=s.index)
    return (s - s.mean()) / s.std(ddof=0)


def _demographics(df):
    """Add race/educ/gender/region from CES coding. Returns df modified in place."""
    race_map = {1: "white", 2: "black", 3: "hispanic", 4: "asian",
                5: "nhpi", 6: "other", 7: "other", 8: "other"}
    df["race"] = df["race"].map(race_map)
    educ_map = {1: "lt_hs", 2: "hs", 3: "some_col", 4: "some_col", 5: "ba", 6: "grad"}
    df["educ"] = df["educ"].map(educ_map)
    gender_map = {1: "man", 2: "woman", 3: "nb", 4: "other"}
    df["gender"] = df["gender4"].map(gender_map)
    region_map = {1: "NE", 2: "MW", 3: "South", 4: "West"}
    df["region"] = df["region"].map(region_map)
    return df


def _baseline_fund(df):
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


def build_mirror_universe(df_full):
    """2020 non-voter universe. Returns df with trump_mob, harris_mob outcomes."""
    mask = (
        df_full["vvweight_post"].notna() & (df_full["vvweight_post"] > 0)
        & (df_full["presvote20post"] == 6)
        & df_full["birthyr"].notna()
        & (df_full["birthyr"] >= 1900) & (df_full["birthyr"] <= 2002)
        & df_full["TS_g2024"].notna()
    )
    nv = df_full[mask].copy()
    print(f"Non-voter universe N = {len(nv)}")

    nv["cohort6"] = nv["birthyr"].apply(birthyr_to_cohort6)
    nv = nv[nv["cohort6"].notna()].copy()
    nv = _demographics(nv)
    nv = nv.dropna(subset=["race", "educ", "gender", "region", "cohort6"]).copy()
    print(f"After demographic completeness: N = {len(nv)}")

    # Outcomes
    voted = nv["TS_g2024"].isin([1, 2, 3, 4, 5, 6])
    still_nv = nv["TS_g2024"] == 7

    nv["trump_2024"] = (voted & (nv["CC24_410"] == 2)).astype(int)
    nv["harris_2024"] = (voted & (nv["CC24_410"] == 1)).astype(int)
    nv["still_nv"] = still_nv.astype(int)

    return nv


def build_predictors_mirror(df):
    """5 channel predictors from v2.9 confirmed channels."""
    df = _baseline_fund(df)

    df["mob_any_z"] = _z(df["CC24_431a"].map({1: 1, 2: 0})).fillna(0.0)
    df["engage_act_raw"] = df[[f"CC24_430a_{i}" for i in range(1, 9)]].apply(
        lambda r: r.map({1: 1, 2: 0}).mean(), axis=1)
    df["engage_act_z"] = _z(df["engage_act_raw"]).fillna(0.0)

    df["issue_econ_z"] = _z(df["CC24_301"].where(df["CC24_301"].between(1, 5))).fillna(0.0)

    # Immigration direction-locked
    df["i_a"] = df["CC24_323a"].map({1: 1, 2: 0})
    df["i_d"] = df["CC24_323d"].map({1: 1, 2: 0})
    df["i_b"] = df["CC24_323b"].map({1: 0, 2: 1})
    df["i_c"] = df["CC24_323c"].map({1: 0, 2: 1})
    df["issue_imm_z"] = _z(df[["i_a", "i_d", "i_b", "i_c"]].mean(axis=1)).fillna(0.0)

    # Trust elections
    df["trust_elec_z"] = _z(
        df[["CC24_421_1", "CC24_421_2"]].apply(
            lambda r: r.where(r.between(1, 5)).mean(), axis=1)
    ).fillna(0.0)

    return df


def build_biden_universe(df_full):
    """v2.9 Biden-2020 skip|retain universe — for issue decomp."""
    mask = (
        df_full["vvweight_post"].notna() & (df_full["vvweight_post"] > 0)
        & (df_full["presvote20post"] == 1)
        & df_full["birthyr"].notna()
        & (df_full["birthyr"] >= 1900) & (df_full["birthyr"] <= 2010)
        & df_full["TS_g2024"].notna()
    )
    bd = df_full[mask].copy()

    bd["cohort6"] = bd["birthyr"].apply(birthyr_to_cohort6)
    bd = bd[bd["cohort6"].notna()].copy()

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

    bd["skipped"] = bd.apply(bucket, axis=1)
    bd = bd[bd["skipped"].notna()].copy()
    bd["skipped"] = bd["skipped"].astype(int)
    bd = _demographics(bd)
    bd = bd.dropna(subset=["race", "educ", "gender", "region", "cohort6"]).copy()
    print(f"Biden universe N = {len(bd)}, skip events = {bd['skipped'].sum()}")

    return bd


def build_predictors_decomp(df):
    """14 item-level issue predictors for H_DECOMP."""
    df = _baseline_fund(df)

    # ABORTION 4 items (CC24_324a-d), direction-locked so HIGH = pro-choice
    df["abor_324a_z"] = _z(df["CC24_324a"].map({1: 1, 2: 0})).fillna(0.0)
    df["abor_324d_z"] = _z(df["CC24_324d"].map({1: 1, 2: 0})).fillna(0.0)
    df["abor_324b_z"] = _z(df["CC24_324b"].map({1: 0, 2: 1})).fillna(0.0)
    df["abor_324c_z"] = _z(df["CC24_324c"].map({1: 0, 2: 1})).fillna(0.0)

    # CLIMATE 6 items, HIGH = pro-climate
    df["clim_326a_z"] = _z(df["CC24_326a"].map({1: 1, 2: 0})).fillna(0.0)
    df["clim_326b_z"] = _z(df["CC24_326b"].map({1: 1, 2: 0})).fillna(0.0)
    df["clim_326c_z"] = _z(df["CC24_326c"].map({1: 1, 2: 0})).fillna(0.0)
    df["clim_326e_z"] = _z(df["CC24_326e"].map({1: 1, 2: 0})).fillna(0.0)
    df["clim_326d_z"] = _z(df["CC24_326d"].map({1: 0, 2: 1})).fillna(0.0)
    df["clim_326f_z"] = _z(df["CC24_326f"].map({1: 0, 2: 1})).fillna(0.0)

    # IMMIGRATION 4 items, HIGH = progressive on that item
    df["imm_323a_z"] = _z(df["CC24_323a"].map({1: 1, 2: 0})).fillna(0.0)
    df["imm_323d_z"] = _z(df["CC24_323d"].map({1: 1, 2: 0})).fillna(0.0)
    df["imm_323b_z"] = _z(df["CC24_323b"].map({1: 0, 2: 1})).fillna(0.0)
    df["imm_323c_z"] = _z(df["CC24_323c"].map({1: 0, 2: 1})).fillna(0.0)

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
    return df


def make_stan_data(df, fund_cols, outcome_col):
    df_clean = df.dropna(subset=fund_cols + [outcome_col]).copy()
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
        "y": df_clean[outcome_col].astype(int).values,
        "weight": df_clean["vvweight_post"].astype(float).values,
    }
    return data, df_clean


def fit_one(tag, data, model_stan="model_a.stan", chains=CHAINS, warmup=WARMUP, samples=SAMPLES):
    print(f"\n=== [{tag}] N={data['N']} K_fund={data['K_fund']} ===")
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
    return float(row["Mean"]), float(row["5%"]), float(row["95%"]), ((row["5%"]>0) or (row["95%"]<0))


def main():
    print("=== Loading CES ===")
    df_full = pd.read_csv(RAW, low_memory=False)
    print(f"CES total N = {len(df_full)}")

    BASE_FUND = ["pid7_z", "faminc_z", "emp_employed", "emp_unemployed", "emp_retired"]
    all_results = []

    # ============================================================
    # PART 1: H_MIRROR — Non-voter mobilization
    # ============================================================
    print("\n" + "#" * 60); print("PART 1: H_MIRROR — NON-VOTER MOBILIZATION"); print("#" * 60)
    nv = build_mirror_universe(df_full)
    nv = build_predictors_mirror(nv)
    nv = make_indices(nv)
    nv.to_csv(OUT_DIR / "mirror_universe.csv", index=False)

    n_t = (nv["trump_2024"] == 1).sum()
    n_h = (nv["harris_2024"] == 1).sum()
    n_snv = (nv["still_nv"] == 1).sum()
    print(f"  Mirror N = {len(nv)}: trump_2024={n_t}, harris_2024={n_h}, still_nv={n_snv}")

    # Per-cohort retention table
    print(f"\n  Cohort × outcome breakdown:")
    print(f"  {'cohort':>10} {'N':>5} {'trump':>6} {'harris':>6} {'still':>6}")
    for c in COHORT_ORDER:
        sub = nv[nv["cohort6"] == c]
        t = (sub["trump_2024"] == 1).sum()
        h = (sub["harris_2024"] == 1).sum()
        snv = (sub["still_nv"] == 1).sum()
        print(f"  {c:>10} {len(sub):>5} {t:>6} {h:>6} {snv:>6}")

    # === Two binaries: trump_mob vs still_nv, harris_mob vs still_nv ===
    for outcome_label, outcome_indic in [("trump_mob", "trump_2024"), ("harris_mob", "harris_2024")]:
        # Subset universe: only outcome OR still_nv (drop other-vote)
        sub = nv[(nv[outcome_indic] == 1) | (nv["still_nv"] == 1)].copy()
        sub["y_bin"] = sub[outcome_indic]

        for predictor in ["mob_any_z", "engage_act_z", "issue_econ_z", "issue_imm_z", "trust_elec_z"]:
            fund_cols = BASE_FUND + [predictor]
            data, _ = make_stan_data(sub, fund_cols, "y_bin")
            tag = f"mirror_{outcome_label}_{predictor}"
            _, summary, diag = fit_one(tag, data)
            beta_idx = len(fund_cols)
            r = coef_row(summary, f"beta_fund[{beta_idx}]")
            sigma_cohort = float(summary.loc["sigma_cohort"]["Mean"]) if "sigma_cohort" in summary.index else None
            if r:
                mean, q5, q95, credible = r
                print(f"  [{outcome_label}/{predictor}] beta={mean:+.3f} [{q5:+.3f}, {q95:+.3f}] credible={credible}, sigma_cohort={sigma_cohort:.3f}")
                all_results.append({
                    "block": "mirror", "outcome": outcome_label, "predictor": predictor,
                    "mean": mean, "q5": q5, "q95": q95, "credible": credible,
                    "sigma_cohort": sigma_cohort,
                    "max_rhat": diag["max_rhat"], "min_ess": diag["min_ess_bulk"], "N": diag["N"],
                })

    # ============================================================
    # PART 2: H_DECOMP — Item-level issue decomposition
    # ============================================================
    print("\n" + "#" * 60); print("PART 2: H_DECOMP — ITEM-LEVEL ISSUE DECOMPOSITION"); print("#" * 60)
    bd = build_biden_universe(df_full)
    bd = build_predictors_decomp(bd)
    bd = make_indices(bd)

    item_predictors = [
        # Abortion 4
        ("abor_324a_z", "abortion", "Always allow as choice"),
        ("abor_324d_z", "abortion", "Expand access"),
        ("abor_324b_z", "abortion", "Rape/incest only (reversed)"),
        ("abor_324c_z", "abortion", "Illegal always (reversed)"),
        # Climate 6
        ("clim_326a_z", "climate", "EPA regulate carbon"),
        ("clim_326b_z", "climate", "Renewable energy"),
        ("clim_326c_z", "climate", "EPA enforcement"),
        ("clim_326e_z", "climate", "Halt oil/gas leases"),
        ("clim_326d_z", "climate", "Increase fossil fuel (reversed)"),
        ("clim_326f_z", "climate", "Prevent gas-stove ban (reversed)"),
        # Immigration 4
        ("imm_323a_z", "immigration", "Legal status to undocumented"),
        ("imm_323d_z", "immigration", "Dreamers permanent status"),
        ("imm_323b_z", "immigration", "Border patrols (reversed)"),
        ("imm_323c_z", "immigration", "Build wall (reversed)"),
    ]

    for predictor, cluster, label in item_predictors:
        fund_cols = BASE_FUND + [predictor]
        data, _ = make_stan_data(bd, fund_cols, "skipped")
        tag = f"decomp_{predictor}"
        _, summary, diag = fit_one(tag, data)
        beta_idx = len(fund_cols)
        r = coef_row(summary, f"beta_fund[{beta_idx}]")
        if r:
            mean, q5, q95, credible = r
            mag = abs(mean)
            verdict = "NULL" if not credible or mag < 0.05 else ("INDET" if mag < 0.10 else ("WEAK" if mag < 0.20 else "STRONG"))
            print(f"  [{cluster}/{predictor}] {label}: beta={mean:+.3f} [{q5:+.3f}, {q95:+.3f}] cred={credible} {verdict}")
            all_results.append({
                "block": "decomp", "cluster": cluster, "predictor": predictor, "label": label,
                "mean": mean, "q5": q5, "q95": q95, "credible": credible, "verdict": verdict,
                "max_rhat": diag["max_rhat"], "min_ess": diag["min_ess_bulk"], "N": diag["N"],
            })

    # Scoreboard
    sb_df = pd.DataFrame(all_results)
    sb_df.to_csv(OUT_DIR / "v210_scoreboard.csv", index=False)
    print("\n=== v2.10 SCOREBOARD ===")
    print(sb_df.to_string(index=False))


if __name__ == "__main__":
    main()
