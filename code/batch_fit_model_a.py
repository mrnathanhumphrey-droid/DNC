"""Batch-fit Model A across all prepared (substrate, outcome) combinations.

4-worker user-limit: chains=4 per fit, one fit at a time sequentially.
"""

from pathlib import Path
import os
import sys
import time

# Toolchain PATH (Windows RTools40)
for p in [r"C:\Users\Nate\.cmdstan\RTools40\usr\bin",
          r"C:\Users\Nate\.cmdstan\RTools40\mingw64\bin"]:
    if p not in os.environ.get("PATH", ""):
        os.environ["PATH"] = p + ";" + os.environ.get("PATH", "")

sys.path.insert(0, str(Path(__file__).parent))
from fit_model_a import fit_model_a

PROCESSED = Path("D:/DNC/data/processed")

JOBS = [
    ("stan_data_anes_vote.joblib",          "binary",   "ANES vote"),
    ("stan_data_anes_israel.joblib",        "gaussian", "ANES Israel/Gaza"),
    ("stan_data_anes_single_payer.joblib",  "gaussian", "ANES single-payer"),
    ("stan_data_ces_vote.joblib",           "binary",   "CES vote"),
    ("stan_data_gss_science.joblib",        "gaussian", "GSS science spending"),
    ("stan_data_gss_foreign_aid.joblib",    "gaussian", "GSS foreign aid spending"),
]


def main():
    print("=== Batch Model A fits (4-worker sequential) ===\n")
    summary = []
    for fname, mtype, label in JOBS:
        path = PROCESSED / fname
        if not path.exists():
            print(f"[SKIP] {label}: {path} missing")
            continue
        print(f"\n=== {label} ({mtype}) ===")
        t0 = time.time()
        try:
            fit, summ, diag = fit_model_a(str(path), mtype)
            wall = time.time() - t0
            summary.append({
                "label": label,
                "wall_seconds": round(wall, 1),
                "N": diag["N"],
                "max_rhat": round(diag["max_rhat"], 4),
                "min_neff": int(diag["min_neff"]),
                "num_divergent": diag["num_divergent"],
                "sigmas": diag["sigma_means"],
            })
        except Exception as e:
            print(f"  ERROR: {type(e).__name__}: {e}")
            summary.append({"label": label, "ERROR": f"{type(e).__name__}: {e}"})

    print("\n\n========== BATCH SUMMARY ==========\n")
    for s in summary:
        print(s)


if __name__ == "__main__":
    main()
