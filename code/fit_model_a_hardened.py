"""Hardened fit for H4 re-fit: chains=6, warmup=1000, samples=1000.

Same as fit_model_a.py but with bumped sampling parameters. Per result_v2.0 §8
H4 had R̂ 1.018 / ESS 384 — marginal. Re-fit to tighten precision before
result_v2.1.
"""

from pathlib import Path
import sys
import os
import json
import joblib
import numpy as np

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

SEED = 42
CHAINS = 6
WARMUP = 1000
SAMPLES = 1000


def fit_hardened(data_file, model_type="binary", tag_suffix="_hardened"):
    payload = joblib.load(data_file)
    data, meta = payload["data"], payload["meta"]

    stan_file = STAN_DIR / ("model_a.stan" if model_type == "binary" else "model_a_issue.stan")
    print(f"Compiling {stan_file.name}")
    model = CmdStanModel(stan_file=stan_file)

    print(f"Fitting on substrate={meta['substrate']}, outcome={meta['outcome']}, "
          f"N={data['N']}, chains={CHAINS}, warmup={WARMUP}, samples={SAMPLES}")
    fit = model.sample(
        data=data, chains=CHAINS,
        iter_warmup=WARMUP, iter_sampling=SAMPLES,
        seed=SEED, show_progress=True, refresh=200,
        parallel_chains=CHAINS,
    )

    summary = fit.summary()
    tag = f"{meta['substrate'].lower()}_{meta['outcome']}_{model_type}{tag_suffix}"
    out_csv = FITS_DIR / f"fit_{tag}_summary.csv"
    summary.to_csv(out_csv)

    sigma_rows = summary.loc[summary.index.str.startswith("sigma_")]
    diag = {
        "substrate": meta["substrate"], "outcome": meta["outcome"],
        "model_type": model_type, "tag_suffix": tag_suffix,
        "N": data["N"], "chains": CHAINS,
        "warmup": WARMUP, "samples": SAMPLES,
        "max_rhat": float(summary["R_hat"].max()),
        "min_neff": float(summary["ESS_bulk"].min()) if "ESS_bulk" in summary.columns
                    else float(summary["N_Eff"].min()),
        "num_divergent": int(np.array(fit.method_variables()["divergent__"]).sum()),
        "sigma_means": {idx.replace("sigma_", ""): float(row["Mean"])
                        for idx, row in sigma_rows.iterrows()},
    }
    diag_path = FITS_DIR / f"fit_{tag}_diag.json"
    diag_path.write_text(json.dumps(diag, indent=2))
    print(f"Saved: {out_csv} + {diag_path}")
    print(f"R-hat max = {diag['max_rhat']:.4f}, ESS_bulk min = {diag['min_neff']:.0f}, "
          f"divergent = {diag['num_divergent']}")
    return fit, summary, diag


if __name__ == "__main__":
    data_file = sys.argv[1]
    model_type = sys.argv[2] if len(sys.argv) > 2 else "binary"
    fit_hardened(data_file, model_type)
