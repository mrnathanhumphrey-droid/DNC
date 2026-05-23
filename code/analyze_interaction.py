"""Analyze cohort × race interaction posterior from fit_*_interaction_*.

Pulls the 5x6 = 30 cohort_race_eff cells and reports:
- Means + 90% CI as a (cohort × race) grid
- Most-extreme cells (with significance flag)
- Comparison vs raw weighted Biden→Harris retention cross-tab
"""

from pathlib import Path
import json
import re
import sys
import pandas as pd

FITS = Path("D:/DNC/data/processed/fits")
COHORTS = ["Silent", "Boomer", "GenX", "Millennial", "GenZ"]
RACES = ["asian", "black", "hispanic", "nhpi", "other", "white"]


def analyze(tag):
    diag = json.loads((FITS / f"fit_{tag}_diag.json").read_text())
    df = pd.read_csv(FITS / f"fit_{tag}_summary.csv", index_col=0)

    print(f"\n===== {tag} =====")
    print(f"N={diag['N']}, R-hat max={diag['max_rhat']:.4f}, "
          f"ESS_bulk min={diag['min_neff']:.0f}, divergent={diag['num_divergent']}")
    print(f"Cohort levels: {diag.get('cohort_levels')}; race levels: {diag.get('race_levels')}")

    cohort_levels = diag.get("cohort_levels", COHORTS)
    race_levels = diag.get("race_levels", RACES)

    # Sigmas
    sigma_rows = df.loc[df.index.str.startswith("sigma_")]
    cols_have = [c for c in ["Mean", "StdDev", "5%", "95%"] if c in df.columns]
    print("\n--- Sigmas ---")
    print(sigma_rows[cols_have].round(3))

    # Marginal cohort + race
    for prefix, labels in [("cohort_eff[", cohort_levels), ("race_eff[", race_levels)]:
        rows = df.loc[df.index.str.startswith(prefix)].copy()
        if len(rows) == len(labels):
            rows.index = labels
        print(f"\n--- Marginal {prefix.rstrip('[')} ---")
        print(rows[cols_have].round(3).to_string())

    # Interaction
    ix = df.loc[df.index.str.startswith("cohort_race_eff[")]
    data = []
    for idx, row in ix.iterrows():
        m = re.match(r"cohort_race_eff\[(\d+),(\d+)\]", idx)
        if m:
            c, r = int(m.group(1)), int(m.group(2))
            data.append({
                "cohort": cohort_levels[c - 1], "race": race_levels[r - 1],
                "mean": row["Mean"], "lo": row.get("5%", float("nan")),
                "hi": row.get("95%", float("nan")),
            })
    cr = pd.DataFrame(data)
    cr["signif"] = (cr["hi"] < 0) | (cr["lo"] > 0)

    piv_mean = cr.pivot(index="cohort", columns="race", values="mean").reindex(cohort_levels)
    print("\n--- Interaction cohort_race_eff (Mean) ---")
    print(piv_mean[race_levels].round(3).to_string())

    print(f"\n--- Credible-significant interaction cells ({cr['signif'].sum()}/{len(cr)}) ---")
    sig = cr[cr["signif"]].sort_values("mean")
    print(sig.round(3).to_string(index=False))

    print("\n--- Top 5 most-NEGATIVE cells (defectors) ---")
    print(cr.sort_values("mean").head(5).round(3).to_string(index=False))

    print("\n--- Top 5 most-POSITIVE cells (anchors) ---")
    print(cr.sort_values("mean", ascending=False).head(5).round(3).to_string(index=False))

    cr.to_csv(FITS / f"interaction_cells_{tag}.csv", index=False)
    print(f"\nSaved cell table: {FITS / f'interaction_cells_{tag}.csv'}")


if __name__ == "__main__":
    tag = sys.argv[1] if len(sys.argv) > 1 else "ces_vote_interaction"
    analyze(tag)
