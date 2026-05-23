"""
DNC post-mortem - Model A Stan fit harness.

Loads a Stan-ready dict (from data_prep.py outputs) and fits either
model_a.stan (binary outcome) or model_a_issue.stan (Gaussian outcome).

Pre-reg §10.1 step 5. 4-worker limit (user-set).
"""

from pathlib import Path
import sys
import os
import json
import joblib
import numpy as np

# Add RTools to PATH so cmdstanpy can find mingw32-make + gcc
RTOOLS_PATHS = [
    r"C:\Users\Nate\.cmdstan\RTools40\usr\bin",
    r"C:\Users\Nate\.cmdstan\RTools40\mingw64\bin",
]
for p in RTOOLS_PATHS:
    if p not in os.environ.get("PATH", ""):
        os.environ["PATH"] = p + ";" + os.environ.get("PATH", "")

from cmdstanpy import CmdStanModel

STAN_DIR = Path("D:/DNC/code/stan")
PROCESSED = Path("D:/DNC/data/processed")
FITS_DIR = PROCESSED / "fits"
FITS_DIR.mkdir(parents=True, exist_ok=True)

SEED = 42
CHAINS = 4
WARMUP = 500
SAMPLES = 500


def fit_model_a(data_file, model_type="binary", refresh=200):
    """
    data_file: path to joblib dict with keys 'data' (Stan dict) and 'meta'
    model_type: 'binary' uses model_a.stan; 'gaussian' uses model_a_issue.stan
    """
    payload = joblib.load(data_file)
    data, meta = payload["data"], payload["meta"]

    stan_file = STAN_DIR / ("model_a.stan" if model_type == "binary" else "model_a_issue.stan")
    print(f"Compiling {stan_file.name}…")
    model = CmdStanModel(stan_file=stan_file)

    print(f"Fitting on substrate={meta['substrate']}, outcome={meta['outcome']}, N={data['N']}, "
          f"chains={CHAINS}, warmup={WARMUP}, samples={SAMPLES}")
    fit = model.sample(
        data=data,
        chains=CHAINS,
        iter_warmup=WARMUP,
        iter_sampling=SAMPLES,
        seed=SEED,
        show_progress=True,
        refresh=refresh,
        parallel_chains=CHAINS,
    )

    # Diagnostics
    summary = fit.summary()
    sigma_rows = summary.loc[summary.index.str.startswith("sigma_")]
    print("\n=== Hierarchical SDs (sigma_*) ===")
    # Newer cmdstanpy uses ESS_bulk / ESS_tail / R_hat; older used N_Eff
    cols_present = sigma_rows.columns.tolist()
    show_cols = [c for c in ["Mean", "StdDev", "5%", "95%", "ESS_bulk", "ESS_tail", "N_Eff", "R_hat"] if c in cols_present]
    print(sigma_rows[show_cols].round(3))

    # Save outputs
    tag = f"{meta['substrate'].lower()}_{meta['outcome']}_{model_type}"
    out_csv = FITS_DIR / f"fit_{tag}_summary.csv"
    summary.to_csv(out_csv)
    print(f"\nSummary saved: {out_csv}")

    diag = {
        "substrate": meta["substrate"],
        "outcome": meta["outcome"],
        "model_type": model_type,
        "N": data["N"],
        "chains": CHAINS,
        "warmup": WARMUP,
        "samples": SAMPLES,
        "max_rhat": float(summary["R_hat"].max()),
        "min_neff": float(summary["ESS_bulk"].min()) if "ESS_bulk" in summary.columns else float(summary["N_Eff"].min()),
        "num_divergent": int(np.array(fit.method_variables()["divergent__"]).sum()),
        "sigma_means": {idx.replace("sigma_", ""): float(row["Mean"]) for idx, row in sigma_rows.iterrows()},
    }
    diag_path = FITS_DIR / f"fit_{tag}_diag.json"
    diag_path.write_text(json.dumps(diag, indent=2))
    print(f"Diagnostics saved: {diag_path}")
    print(f"\nVerdict: R-hat max = {diag['max_rhat']:.4f}, N_eff min = {diag['min_neff']:.0f}, divergent = {diag['num_divergent']}")
    if diag["max_rhat"] > 1.01 or diag["num_divergent"] > 10:
        print("  WARNING: convergence concerns")
    else:
        print("  CONVERGED")
    return fit, summary, diag


if __name__ == "__main__":
    data_file = sys.argv[1] if len(sys.argv) > 1 else str(PROCESSED / "stan_data_anes_vote.joblib")
    model_type = sys.argv[2] if len(sys.argv) > 2 else "binary"
    fit_model_a(data_file, model_type)
