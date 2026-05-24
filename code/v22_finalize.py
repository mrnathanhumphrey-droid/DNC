"""Finish v2.2 confirmation: train-half fit (test already saved) + write verdict.

Skips the test fit since fit_anes_vote_v22_test_diag.json already exists.
"""
from pathlib import Path
import os, sys, json, joblib

for p in [r"C:\Users\Nate\.cmdstan\RTools40\usr\bin",
          r"C:\Users\Nate\.cmdstan\RTools40\mingw64\bin"]:
    if p not in os.environ.get("PATH", ""):
        os.environ["PATH"] = p + ";" + os.environ.get("PATH", "")

sys.path.insert(0, "code")
from v22_confirmation_stan import build_stan_data_for_half, fit_half
from v22_discovery_confirmation import load_h4_sample

V22_DIR = Path("D:/DNC/data/processed/v22")
FITS_DIR = Path("D:/DNC/data/processed/fits")


def main():
    test_diag = json.loads((FITS_DIR / "fit_anes_vote_v22_test_diag.json").read_text())
    art = joblib.load(V22_DIR / "discovery_artifacts.joblib")
    df = load_h4_sample()

    train_data, train_meta = build_stan_data_for_half(
        art["train_idx"], df, art["scaler"], art["imputation_means"], art["retained_items"])
    train_diag = fit_half(train_data, train_meta, tag="train")

    overfit_gap = train_diag["sigma_means"]["cohort"] - test_diag["sigma_means"]["cohort"]
    sc = test_diag["sigma_means"]["cohort"]
    if sc < 0.15:
        verdict = "AXIS FOUND"
    elif sc < 0.25:
        verdict = "AXIS PARTIAL"
    else:
        verdict = "AXIS NOT FOUND (MECHANISM RESIDUAL replicates)"

    out = {
        "train_sigma_cohort": train_diag["sigma_means"]["cohort"],
        "test_sigma_cohort": test_diag["sigma_means"]["cohort"],
        "overfit_gap": -overfit_gap,
        "verdict": verdict,
        "train_diag": train_diag,
        "test_diag": test_diag,
    }
    (V22_DIR / "confirmation_verdict.json").write_text(json.dumps(out, indent=2))
    print(f"\n=== Confirmation summary ===")
    print(f"sigma_cohort TRAIN = {train_diag['sigma_means']['cohort']:.3f}")
    print(f"sigma_cohort TEST  = {test_diag['sigma_means']['cohort']:.3f}")
    print(f"Overfit gap = {-overfit_gap:.3f} (pre-reg flags >0.10)")
    print(f"\nVERDICT: {verdict} (sigma_cohort_test = {sc:.3f})")


if __name__ == "__main__":
    main()
