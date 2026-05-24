"""v2.2 confirmation step: Stan model_a on TEST half with retained items
added as fundamentals.

Per prereg_v2.2 §4. Reads discovery artifacts, builds test-half Stan dict,
fits hardened (chains=6, warmup=1000, samples=1000), reads σ_cohort.

Also fits TRAIN half with same retained items as overfit-flag.
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

# Reuse data_prep helper for Stan-dict construction
sys.path.insert(0, "code")
from data_prep import _build_data_dict  # noqa: E402

from cmdstanpy import CmdStanModel  # noqa: E402

V22_DIR = Path("D:/DNC/data/processed/v22")
FITS_DIR = Path("D:/DNC/data/processed/fits")
STAN_DIR = Path("D:/DNC/code/stan")

SEED = 42


def build_stan_data_for_half(half_idx, df_full, scaler, imputation_means, retained_items):
    """Build Stan dict for one half of the sample with retained items added
    as fundamentals on top of H4 baseline. Uses training-half mean-imputation
    statistics + training-half z-score statistics (no test-leakage)."""
    import pandas as pd

    sub = df_full.loc[half_idx].copy()
    # Build retained_item z-scored columns using training-half stats
    for item in retained_items:
        col = pd.to_numeric(sub[item], errors="coerce").where(sub[item] > 0)
        if item == "V241177":
            col = col.where(col != 99)
        # Mean-impute using training mean (passed in)
        col = col.fillna(imputation_means[item])
        # Apply z-score from scaler
        scaler_idx = list(scaler.feature_names_in_).index(item)
        mean = scaler.mean_[scaler_idx]
        scale = scaler.scale_[scaler_idx]
        sub[f"fund_{item}_z"] = (col - mean) / scale

    # Augment fundamentals: H4 baseline (8) + retained (N)
    fund_cols = [
        "fund_recall20_biden", "fund_recall20_trump", "fund_recall20_other",
        "fund_econ_z", "fund_pid7_z", "fund_trump_ft_z",
        "fund_gaza_salience_z", "fund_econ_x_cohort",
    ] + [f"fund_{item}_z" for item in retained_items]

    # Build data dict (binary outcome)
    sub_meta = {"_fund_cols_override": fund_cols}
    # Manually construct X_fund + indices
    X_fund = sub[fund_cols].values.astype(float)
    n = len(sub)

    # Build group indices
    race_levels = sorted(sub["race"].dropna().unique().tolist())
    educ_levels = sorted(sub["educ"].dropna().unique().tolist())
    cohort_levels = ["Silent", "Boomer", "GenX", "Millennial", "GenZ"]
    gender_levels = sorted(sub["gender"].dropna().unique().tolist())
    region_levels = sorted(sub["region"].dropna().unique().tolist())

    data = {
        "N": n,
        "K_fund": X_fund.shape[1],
        "X_fund": X_fund.tolist(),
        "N_race": len(race_levels),
        "N_educ": len(educ_levels),
        "N_cohort": len(cohort_levels),
        "N_gender": len(gender_levels),
        "N_region": len(region_levels),
        "race": [race_levels.index(r) + 1 for r in sub["race"]],
        "educ": [educ_levels.index(e) + 1 for e in sub["educ"]],
        "cohort": [cohort_levels.index(c) + 1 for c in sub["cohort"]],
        "gender": [gender_levels.index(g) + 1 for g in sub["gender"]],
        "region": [region_levels.index(r) + 1 for r in sub["region"]],
        "y": sub["y"].astype(int).tolist(),
        "weight": [1.0] * n,
    }
    meta = {
        "substrate": "ANES",
        "outcome": "vote_v22",
        "n_used": n,
        "fund_cols": fund_cols,
        "race_levels": race_levels,
        "educ_levels": educ_levels,
        "cohort_levels": cohort_levels,
        "gender_levels": gender_levels,
        "region_levels": region_levels,
    }
    return data, meta


def fit_half(data, meta, tag):
    print(f"\n=== Fitting {tag} (N={data['N']}, K_fund={data['K_fund']}) ===")
    model = CmdStanModel(stan_file=STAN_DIR / "model_a.stan")
    fit = model.sample(
        data=data,
        chains=6,
        iter_warmup=1000,
        iter_sampling=1000,
        seed=SEED,
        show_progress=True,
        parallel_chains=6,
        refresh=200,
    )
    summary = fit.summary()
    out_csv = FITS_DIR / f"fit_anes_vote_v22_{tag}_summary.csv"
    summary.to_csv(out_csv)

    sigma_rows = summary.loc[summary.index.str.startswith("sigma_")]
    diag = {
        "tag": tag,
        "N": data["N"], "K_fund": data["K_fund"],
        "chains": 6, "warmup": 1000, "samples": 1000,
        "max_rhat": float(summary["R_hat"].max()),
        "min_neff": float(summary["ESS_bulk"].min()) if "ESS_bulk" in summary.columns
                    else float(summary["N_Eff"].min()),
        "num_divergent": int(np.array(fit.method_variables()["divergent__"]).sum()),
        "sigma_means": {idx.replace("sigma_", ""): float(row["Mean"])
                        for idx, row in sigma_rows.iterrows()},
    }
    diag_path = FITS_DIR / f"fit_anes_vote_v22_{tag}_diag.json"
    diag_path.write_text(json.dumps(diag, indent=2))
    print(f"\n{tag}: R-hat max = {diag['max_rhat']:.4f}, ESS_bulk min = {diag['min_neff']:.0f}, "
          f"divergent = {diag['num_divergent']}, sigma_cohort = {diag['sigma_means']['cohort']:.3f}")
    return diag


def main():
    art = joblib.load(V22_DIR / "discovery_artifacts.joblib")
    train_idx = art["train_idx"]
    test_idx = art["test_idx"]
    scaler = art["scaler"]
    imputation_means = art["imputation_means"]
    retained_items = art["retained_items"]
    print(f"Retained items ({len(retained_items)}): {retained_items}")

    # Load full sample (must match the load_h4_sample() output indexing)
    from v22_discovery_confirmation import load_h4_sample
    df = load_h4_sample()

    # TEST fit (primary verdict)
    test_data, test_meta = build_stan_data_for_half(
        test_idx, df, scaler, imputation_means, retained_items)
    test_diag = fit_half(test_data, test_meta, tag="test")

    # TRAIN fit (overfit flag)
    train_data, train_meta = build_stan_data_for_half(
        train_idx, df, scaler, imputation_means, retained_items)
    train_diag = fit_half(train_data, train_meta, tag="train")

    overfit_gap = train_diag["sigma_means"]["cohort"] - test_diag["sigma_means"]["cohort"]
    print(f"\n=== Confirmation summary ===")
    print(f"sigma_cohort TRAIN = {train_diag['sigma_means']['cohort']:.3f}")
    print(f"sigma_cohort TEST  = {test_diag['sigma_means']['cohort']:.3f}")
    print(f"Overfit gap (train < test by) = {-overfit_gap:.3f}")
    print(f"  (positive = train < test = overfit; pre-reg flags >0.10)")

    # Verdict per pre-reg
    sc = test_diag["sigma_means"]["cohort"]
    if sc < 0.15:
        verdict = "AXIS FOUND"
    elif sc < 0.25:
        verdict = "AXIS PARTIAL"
    else:
        verdict = "AXIS NOT FOUND (MECHANISM RESIDUAL replicates)"
    print(f"\nVERDICT: {verdict} (sigma_cohort = {sc:.3f})")

    # Save summary
    out = {
        "train_sigma_cohort": train_diag["sigma_means"]["cohort"],
        "test_sigma_cohort": test_diag["sigma_means"]["cohort"],
        "overfit_gap": -overfit_gap,
        "verdict": verdict,
        "train_diag": train_diag,
        "test_diag": test_diag,
    }
    (V22_DIR / "confirmation_verdict.json").write_text(json.dumps(out, indent=2))
    print(f"\nSaved: {V22_DIR / 'confirmation_verdict.json'}")


if __name__ == "__main__":
    main()
