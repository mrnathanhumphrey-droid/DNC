"""v2.11 — "Blame the leftists" empirical test.

Per prereg_v2.11_dnc_postmortem.md (LOCKED ea9aca3).

11-item leftist composite (direction-locked HIGH = LEFTIST).
Tested on Biden universe (skip outcome) + mirror universe (trump_mob, harris_mob).
Plus 4 single-item Biden-skip fits.

Total: 7 binary logistic Stan fits.
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

import sys
sys.path.insert(0, "code")
from v210_mirror_and_decomp import (
    build_mirror_universe, build_biden_universe, _baseline_fund, _demographics,
    make_indices, make_stan_data, coef_row, fit_one,
    STAN_DIR, SEED, CHAINS, WARMUP, SAMPLES,
    COHORT_ORDER, RACE_ORDER,
)

RAW = Path("D:/DNC/data/raw/ces_2024/CCES24_Common_OUTPUT_vv_topost_final.csv")
OUT_DIR = Path("D:/DNC/data/processed/v211")
OUT_DIR.mkdir(parents=True, exist_ok=True)


def _z(s):
    s = pd.to_numeric(s, errors="coerce")
    if s.std(ddof=0) == 0 or s.notna().sum() == 0:
        return pd.Series(0.0, index=s.index)
    return (s - s.mean()) / s.std(ddof=0)


# Direction-lock per pre-reg §2: 1 if item-support is LEFTIST, 0 if item-support is RIGHT-ist
LEFT_ITEMS = {
    "CC24_323f": ("student_loan", "support"),  # forgive loan: support = left
    "CC24_328a": ("zoning", "support"),
    "CC24_328b": ("housing_subsidy", "support"),
    "CC24_328e": ("medicaid_expand", "support"),
    "CC24_340a": ("contraceptives", "support"),
    "CC24_340c": ("ssm_recognition", "support"),
    "CC24_340d": ("tiktok_ban", "oppose"),  # support=right; oppose=left
    "CC24_340e": ("fisa_renew", "oppose"),
    "CC24_341b": ("corp_tax", "support"),
    "CC24_341c": ("rich_tax", "support"),
    "CC24_341d": ("infra", "support"),
}


def build_leftist_predictors(df):
    """Build left_composite_z + 4 single-item z-scores."""
    df = _baseline_fund(df)

    # Recode each item to 1=leftist, 0=non-leftist
    item_recoded_cols = []
    for vcode, (name, direction) in LEFT_ITEMS.items():
        if vcode not in df.columns:
            print(f"WARN: {vcode} not in df")
            continue
        if direction == "support":
            df[f"left_{name}"] = df[vcode].map({1: 1, 2: 0})
        elif direction == "oppose":
            df[f"left_{name}"] = df[vcode].map({1: 0, 2: 1})
        item_recoded_cols.append(f"left_{name}")

    # Composite: row-mean across items, then z-score
    df["left_composite_raw"] = df[item_recoded_cols].mean(axis=1)
    df["left_composite_z"] = _z(df["left_composite_raw"]).fillna(0.0)

    # Single-item z-scores for decomp
    df["left_student_loan_z"] = _z(df["left_student_loan"]).fillna(0.0)
    df["left_anti_tiktok_z"] = _z(df["left_tiktok_ban"]).fillna(0.0)
    df["left_anti_fisa_z"] = _z(df["left_fisa_renew"]).fillna(0.0)
    df["left_medicaid_z"] = _z(df["left_medicaid_expand"]).fillna(0.0)

    return df


def main():
    print("=== Loading CES ===")
    df_full = pd.read_csv(RAW, low_memory=False)
    print(f"CES total N = {len(df_full)}")

    BASE_FUND = ["pid7_z", "faminc_z", "emp_employed", "emp_unemployed", "emp_retired"]
    all_results = []

    # ============================================================
    # BIDEN universe (primary): skip outcome
    # ============================================================
    print("\n" + "#" * 60); print("BIDEN UNIVERSE — SKIP OUTCOME"); print("#" * 60)
    bd = build_biden_universe(df_full)
    bd = build_leftist_predictors(bd)
    bd = make_indices(bd)

    # F3 sanity: collinearity of left_composite_z with pid7_z
    r = bd[["left_composite_z", "pid7_z"]].corr().iloc[0, 1]
    print(f"\n  Correlation left_composite_z vs pid7_z: r = {r:.3f}")
    print(f"  (F3 gate: |r| < 0.5 — {'PASS' if abs(r) < 0.5 else 'FAIL'})")

    # Per-cohort composite means (transparency)
    print("\n  Per-cohort left_composite mean (Biden universe):")
    for c in COHORT_ORDER:
        sub = bd[bd["cohort6"] == c]
        if len(sub) > 0:
            print(f"    {c}: N={len(sub)}, mean_composite_raw={sub['left_composite_raw'].mean():.3f}, mean_z={sub['left_composite_z'].mean():+.3f}")

    # H_LEFTIST_A: composite x skip  (SKIP if already completed — fit 1 ran on previous attempt)
    import os
    already_done = os.path.exists(OUT_DIR / "fit_v211_skip_composite_summary.csv")
    fund_cols = BASE_FUND + ["left_composite_z"]
    if already_done:
        print("\n  [SKIP] v211_skip_composite already completed; loading existing summary")
        summary = pd.read_csv(OUT_DIR / "fit_v211_skip_composite_summary.csv", index_col=0)
        diag = {"max_rhat": float(summary["R_hat"].max()), "min_ess_bulk": float(summary["ESS_bulk"].min()), "N": 17401}
    else:
        data, _ = make_stan_data(bd, fund_cols, "skipped")
        fit, summary, diag = fit_one("v211_skip_composite", data, model_stan="model_a.stan")
    # Adjust output path
    (Path("D:/DNC/data/processed/v210") / "fit_v211_skip_composite_summary.csv").rename(
        OUT_DIR / "fit_v211_skip_composite_summary.csv") if (Path("D:/DNC/data/processed/v210") / "fit_v211_skip_composite_summary.csv").exists() else None

    beta_idx = len(fund_cols)
    r = coef_row(summary, f"beta_fund[{beta_idx}]")
    if r:
        mean, q5, q95, credible = r
        print(f"\n  ** H_LEFTIST_A composite beta={mean:+.3f} [{q5:+.3f}, {q95:+.3f}] cred={credible} **")
        all_results.append({"hypothesis": "H_LEFTIST_A", "universe": "biden_skip",
                           "predictor": "left_composite_z", "mean": mean, "q5": q5, "q95": q95,
                           "credible": credible, "max_rhat": diag["max_rhat"],
                           "min_ess": diag["min_ess_bulk"], "N": diag["N"]})

    # H_LEFTIST_DECOMP: 4 single-item fits
    print("\n  Single-item Biden-skip decomp:")
    for predictor in ["left_student_loan_z", "left_anti_tiktok_z", "left_anti_fisa_z", "left_medicaid_z"]:
        fund_cols = BASE_FUND + [predictor]
        data, _ = make_stan_data(bd, fund_cols, "skipped")
        fit, summary, diag = fit_one(f"v211_skip_{predictor}", data, model_stan="model_a.stan")
        beta_idx = len(fund_cols)
        r = coef_row(summary, f"beta_fund[{beta_idx}]")
        if r:
            mean, q5, q95, credible = r
            mag = abs(mean)
            verdict = "NULL" if not credible or mag < 0.05 else ("INDET" if mag < 0.10 else ("WEAK" if mag < 0.20 else "STRONG"))
            print(f"  [{predictor}] beta={mean:+.3f} [{q5:+.3f}, {q95:+.3f}] {verdict}")
            all_results.append({"hypothesis": "H_LEFTIST_DECOMP", "universe": "biden_skip",
                               "predictor": predictor, "mean": mean, "q5": q5, "q95": q95,
                               "credible": credible, "verdict": verdict,
                               "max_rhat": diag["max_rhat"], "min_ess": diag["min_ess_bulk"], "N": diag["N"]})

    # ============================================================
    # MIRROR universe: composite × trump_mob, harris_mob
    # ============================================================
    print("\n" + "#" * 60); print("MIRROR UNIVERSE — NON-VOTER MOBILIZATION"); print("#" * 60)
    nv = build_mirror_universe(df_full)
    nv = build_leftist_predictors(nv)
    nv = make_indices(nv)

    voted = nv["TS_g2024"].isin([1, 2, 3, 4, 5, 6])
    still_nv = nv["TS_g2024"] == 7
    nv["trump_2024"] = (voted & (nv["CC24_410"] == 2)).astype(int)
    nv["harris_2024"] = (voted & (nv["CC24_410"] == 1)).astype(int)
    nv["still_nv"] = still_nv.astype(int)

    # H_LEFTIST_B: composite × harris_mob (universe: harris_mob OR still_nv)
    sub_h = nv[(nv["harris_2024"] == 1) | (nv["still_nv"] == 1)].copy()
    sub_h["y_bin"] = sub_h["harris_2024"]
    fund_cols = BASE_FUND + ["left_composite_z"]
    data, _ = make_stan_data(sub_h, fund_cols, "y_bin")
    fit, summary, diag = fit_one("v211_harris_mob_composite", data, model_stan="model_a.stan")
    beta_idx = len(fund_cols)
    r = coef_row(summary, f"beta_fund[{beta_idx}]")
    if r:
        mean, q5, q95, credible = r
        print(f"\n  ** H_LEFTIST_B composite x harris_mob beta={mean:+.3f} [{q5:+.3f}, {q95:+.3f}] cred={credible} **")
        all_results.append({"hypothesis": "H_LEFTIST_B", "universe": "harris_mob",
                           "predictor": "left_composite_z", "mean": mean, "q5": q5, "q95": q95,
                           "credible": credible, "max_rhat": diag["max_rhat"],
                           "min_ess": diag["min_ess_bulk"], "N": diag["N"]})

    # H_LEFTIST_C: composite × trump_mob
    sub_t = nv[(nv["trump_2024"] == 1) | (nv["still_nv"] == 1)].copy()
    sub_t["y_bin"] = sub_t["trump_2024"]
    fund_cols = BASE_FUND + ["left_composite_z"]
    data, _ = make_stan_data(sub_t, fund_cols, "y_bin")
    fit, summary, diag = fit_one("v211_trump_mob_composite", data, model_stan="model_a.stan")
    beta_idx = len(fund_cols)
    r = coef_row(summary, f"beta_fund[{beta_idx}]")
    if r:
        mean, q5, q95, credible = r
        print(f"\n  ** H_LEFTIST_C composite x trump_mob beta={mean:+.3f} [{q5:+.3f}, {q95:+.3f}] cred={credible} **")
        all_results.append({"hypothesis": "H_LEFTIST_C", "universe": "trump_mob",
                           "predictor": "left_composite_z", "mean": mean, "q5": q5, "q95": q95,
                           "credible": credible, "max_rhat": diag["max_rhat"],
                           "min_ess": diag["min_ess_bulk"], "N": diag["N"]})

    # Save scoreboard
    sb_df = pd.DataFrame(all_results)
    sb_df.to_csv(OUT_DIR / "v211_scoreboard.csv", index=False)
    print("\n=== v2.11 SCOREBOARD ===")
    print(sb_df.to_string(index=False))


if __name__ == "__main__":
    main()
