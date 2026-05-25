"""v2.9 RUN 2 — refit issue items with correct V-codes + F5 trust_elec escalation.

Per prereg_v2.9_amendment_2_2026_05_25.md.

Corrected V-codes:
  issue_abor_z   = CC24_324a/b/c/d direction-locked
  issue_clim_z   = CC24_326a-f direction-locked (climate/env)
  issue_imm_z    = CC24_323a-d direction-locked
  issue_harris_ft_z = CC24_330d Harris feeling thermometer
  issue_trump_ft_z  = CC24_330e Trump feeling thermometer

F5 escalation for trust_elec_z: chains=8, warmup=2000, samples=2000.
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
from v29_skip_mechanism import (
    build_universe, build_baseline_fundamentals, make_indices, make_stan_data,
    coef_row, OUT_DIR, STAN_DIR, SEED, RACE_ORDER, COHORT_ORDER,
)


def _z(s):
    s = pd.to_numeric(s, errors="coerce")
    return (s - s.mean()) / s.std(ddof=0)


def build_corrected_issue_predictors(df):
    """Direction-locked issue composites per amendment 2."""

    # ABORTION — CC24_324 (1=support, 2=oppose)
    df["a_pro"] = df["CC24_324a"].map({1: 1, 2: 0})      # always allow = pro-choice
    df["a_d_pro"] = df["CC24_324d"].map({1: 1, 2: 0})    # expand access = pro-choice
    df["a_b_res"] = df["CC24_324b"].map({1: 0, 2: 1})    # rape/incest only = restrict; flip so 1=pro-choice
    df["a_c_res"] = df["CC24_324c"].map({1: 0, 2: 1})    # illegal-always = restrict; flip
    df["issue_abor_raw"] = df[["a_pro", "a_d_pro", "a_b_res", "a_c_res"]].mean(axis=1)
    df["issue_abor_z"] = _z(df["issue_abor_raw"]).fillna(0.0)

    # CLIMATE/ENV — CC24_326a-f
    df["e_a"] = df["CC24_326a"].map({1: 1, 2: 0})  # EPA carbon
    df["e_b"] = df["CC24_326b"].map({1: 1, 2: 0})  # renewable
    df["e_c"] = df["CC24_326c"].map({1: 1, 2: 0})  # EPA enforcement
    df["e_e"] = df["CC24_326e"].map({1: 1, 2: 0})  # halt oil/gas leases
    df["e_d"] = df["CC24_326d"].map({1: 0, 2: 1})  # increase fossil fuel → flip
    df["e_f"] = df["CC24_326f"].map({1: 0, 2: 1})  # prevent gas-stove ban → flip
    df["issue_clim_raw"] = df[["e_a", "e_b", "e_c", "e_e", "e_d", "e_f"]].mean(axis=1)
    df["issue_clim_z"] = _z(df["issue_clim_raw"]).fillna(0.0)

    # IMMIGRATION — CC24_323a-d
    df["i_a"] = df["CC24_323a"].map({1: 1, 2: 0})  # legal status
    df["i_d"] = df["CC24_323d"].map({1: 1, 2: 0})  # Dreamers
    df["i_b"] = df["CC24_323b"].map({1: 0, 2: 1})  # border patrols → flip
    df["i_c"] = df["CC24_323c"].map({1: 0, 2: 1})  # build wall → flip
    df["issue_imm_raw"] = df[["i_a", "i_d", "i_b", "i_c"]].mean(axis=1)
    df["issue_imm_z"] = _z(df["issue_imm_raw"]).fillna(0.0)

    # HARRIS feeling thermometer — CC24_330d (1-7 scale; higher = warmer rating)
    h = df["CC24_330d"].where(df["CC24_330d"].between(1, 7))
    df["issue_harris_ft_z"] = _z(h).fillna(0.0)

    # TRUMP FT — CC24_330e
    t = df["CC24_330e"].where(df["CC24_330e"].between(1, 7))
    df["issue_trump_ft_z"] = _z(t).fillna(0.0)

    # Re-import trust_elec for refit
    for col in ["CC24_421_1", "CC24_421_2"]:
        df[col + "_v"] = df[col].where(df[col].between(1, 5))
    df["trust_elec_raw"] = df[["CC24_421_1_v", "CC24_421_2_v"]].mean(axis=1)
    df["trust_elec_z"] = _z(df["trust_elec_raw"]).fillna(0.0)

    return df


def fit_one(tag, data, model_stan="model_a.stan", chains=6, warmup=1000, samples=1000):
    print(f"\n=== [{tag}] N={data['N']} K_fund={data['K_fund']} chains={chains} warmup={warmup} ===")
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


def main():
    df = build_universe()
    df = build_baseline_fundamentals(df)
    df = build_corrected_issue_predictors(df)
    df, _, _, _, _, _ = make_indices(df)

    BASE_FUND = ["pid7_z", "faminc_z", "emp_employed", "emp_unemployed", "emp_retired"]
    results = {}

    # ============ Refit issues with correct V-codes ============
    print("\n" + "=" * 60); print("RUN 2 — CORRECTED ISSUE V-CODES"); print("=" * 60)
    for issue in ["issue_abor_z", "issue_clim_z", "issue_imm_z",
                   "issue_harris_ft_z", "issue_trump_ft_z"]:
        fund_cols = BASE_FUND + [issue]
        data, _ = make_stan_data(df, fund_cols)
        tag = f"skip_C_{issue}_v2"
        _, summary, diag = fit_one(tag, data)
        beta_idx = len(fund_cols)
        r = coef_row(summary, f"beta_fund[{beta_idx}]")
        if r:
            mean, q5, q95, credible = r
            print(f"  [{issue}] beta = {mean:+.3f} [{q5:+.3f}, {q95:+.3f}] credible={credible}")
            results[tag] = {"mean": mean, "q5": q5, "q95": q95, "credible": credible, "diag": diag}

    # ============ F5 escalated trust_elec refit ============
    print("\n" + "=" * 60); print("F5 ESCALATION — trust_elec_z chains=8 warmup=2000"); print("=" * 60)
    fund_cols = BASE_FUND + ["trust_elec_z"]
    data, _ = make_stan_data(df, fund_cols)
    tag = "skip_D_trust_elec_z_F5"
    _, summary, diag = fit_one(tag, data, chains=8, warmup=2000, samples=2000)
    beta_idx = len(fund_cols)
    r = coef_row(summary, f"beta_fund[{beta_idx}]")
    if r:
        mean, q5, q95, credible = r
        print(f"  [trust_elec_z F5] beta = {mean:+.3f} [{q5:+.3f}, {q95:+.3f}] credible={credible}")
        results[tag] = {"mean": mean, "q5": q5, "q95": q95, "credible": credible, "diag": diag}

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
    sb_df.to_csv(OUT_DIR / "v29_scoreboard_run2.csv", index=False)
    print("\n=== v2.9 RUN 2 SCOREBOARD ===")
    print(sb_df.to_string(index=False))


if __name__ == "__main__":
    main()
