"""Batch B - 3 corrected/new ANES Model A fits, post §12 deviation 8.

Fixes:
- single_payer was V241247 (Trump placement) -> now V241245 (self-placement).
- Adds israel_military (V241401) and gaza_protests (V241410) as direct Israel/Gaza items.

4-worker user-limit: chains=4 per fit, one fit at a time sequentially.
"""

from pathlib import Path
import os
import sys
import time

for p in [r"C:\Users\Nate\.cmdstan\RTools40\usr\bin",
          r"C:\Users\Nate\.cmdstan\RTools40\mingw64\bin"]:
    if p not in os.environ.get("PATH", ""):
        os.environ["PATH"] = p + ";" + os.environ.get("PATH", "")

sys.path.insert(0, str(Path(__file__).parent))
from fit_model_a import fit_model_a

PROCESSED = Path("D:/DNC/data/processed")

JOBS = [
    ("stan_data_anes_single_payer.joblib",    "gaussian", "ANES single-payer (V241245 self)"),
    ("stan_data_anes_israel_military.joblib", "gaussian", "ANES Israel military aid (V241401)"),
    ("stan_data_anes_gaza_protests.joblib",   "gaussian", "ANES Gaza protests approval (V241410)"),
]


def main():
    print("=== Batch B - 3 corrected/new ANES fits ===\n")
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

    print("\n\n========== BATCH B SUMMARY ==========\n")
    for s in summary:
        print(s)


if __name__ == "__main__":
    main()
