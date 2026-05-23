"""Fit Model A + cohort×race interaction layer.

Reuses existing stan_data joblibs (interaction adds no schema change).
Outputs to data/processed/fits/fit_{substrate}_{outcome}_interaction_*.
"""

from pathlib import Path
import os
import sys
import json
import joblib
import numpy as np

for p in [r"C:\Users\Nate\.cmdstan\RTools40\usr\bin",
          r"C:\Users\Nate\.cmdstan\RTools40\mingw64\bin"]:
    if p not in os.environ.get("PATH", ""):
        os.environ["PATH"] = p + ";" + os.environ.get("PATH", "")

from cmdstanpy import CmdStanModel

STAN_DIR = Path("D:/DNC/code/stan")
PROCESSED = Path("D:/DNC/data/processed")
FITS = PROCESSED / "fits"

SEED = 42
CHAINS = 4
WARMUP = 750     # bumped from 500 — interaction needs more warmup
SAMPLES = 750


def fit_interaction(data_file):
    payload = joblib.load(data_file)
    data, meta = payload["data"], payload["meta"]

    print(f"Compiling model_a_interaction.stan…")
    model = CmdStanModel(stan_file=STAN_DIR / "model_a_interaction.stan")

    print(f"Fitting interaction model on substrate={meta['substrate']}, "
          f"outcome={meta['outcome']}, N={data['N']}, "
          f"N_cohort={data['N_cohort']}, N_race={data['N_race']} "
          f"(= {data['N_cohort']*data['N_race']} interaction cells)")
    fit = model.sample(
        data=data,
        chains=CHAINS,
        iter_warmup=WARMUP,
        iter_sampling=SAMPLES,
        seed=SEED,
        show_progress=True,
        refresh=200,
        parallel_chains=CHAINS,
    )

    summary = fit.summary()
    tag = f"{meta['substrate'].lower()}_{meta['outcome']}_interaction"
    out_csv = FITS / f"fit_{tag}_summary.csv"
    summary.to_csv(out_csv)

    sigma_rows = summary.loc[summary.index.str.startswith("sigma_")]
    cohort_race_rows = summary.loc[summary.index.str.startswith("cohort_race_eff[")]
    print("\n=== Sigmas ===")
    print(sigma_rows[[c for c in ["Mean", "StdDev", "5%", "95%"] if c in sigma_rows.columns]].round(3))
    print(f"\n=== cohort_race_eff cells (head 10 of {len(cohort_race_rows)}) ===")
    print(cohort_race_rows[[c for c in ["Mean", "5%", "95%"] if c in cohort_race_rows.columns]].head(10).round(3))

    diag = {
        "substrate": meta["substrate"],
        "outcome": meta["outcome"],
        "model_type": "interaction_cohort_race",
        "N": data["N"],
        "chains": CHAINS,
        "warmup": WARMUP,
        "samples": SAMPLES,
        "max_rhat": float(summary["R_hat"].max()),
        "min_neff": float(summary["ESS_bulk"].min()) if "ESS_bulk" in summary.columns else float(summary["N_Eff"].min()),
        "num_divergent": int(np.array(fit.method_variables()["divergent__"]).sum()),
        "sigma_means": {idx.replace("sigma_", ""): float(row["Mean"]) for idx, row in sigma_rows.iterrows()},
        "race_levels": meta["race_levels"],
        "cohort_levels": meta["cohort_levels"],
    }
    diag_path = FITS / f"fit_{tag}_diag.json"
    diag_path.write_text(json.dumps(diag, indent=2))
    print(f"\nSaved: {out_csv} + {diag_path}")
    print(f"R-hat max = {diag['max_rhat']:.4f}, ESS_bulk min = {diag['min_neff']:.0f}, "
          f"divergent = {diag['num_divergent']}")
    return fit, summary, diag


if __name__ == "__main__":
    data_file = sys.argv[1] if len(sys.argv) > 1 else str(PROCESSED / "stan_data_ces_vote.joblib")
    fit_interaction(data_file)
