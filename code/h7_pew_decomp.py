"""H7: Pew W159 turnout-vs-choice decomposition (pre-reg v2.0 §1 H7 + §3.5).

Among VALIDATED Biden 2020 voters, decompose 2024 outcomes by F_AGECAT cohort band:
  (a) Retained Harris (VOTECHOICE2024 == 2)
  (b) Flipped to Trump (VOTECHOICE2024 == 1)
  (c) Flipped to Third party (VOTECHOICE2024 == 3)
  (d) Did not vote 2024 (VOTECHOICE2024 is NaN within validated universe)

Vote coding verified by margin: VOTECHOICE 1 = Republican (Trump 2020, Trump 2024);
2 = Democrat (Biden 2020, Harris 2024); 3 = Third party.

Outputs weighted % within Biden-2020 cohort band.
"""

from pathlib import Path
import pandas as pd
import numpy as np

RAW = Path("D:/DNC/data/raw/pew_vv_2024/W159_Nov24/ATP W159.csv")
OUT = Path("D:/DNC/data/processed/fits/h7_pew_decomp.csv")

# Pew F_AGECAT bands (per Pew convention, verified by Pew W159 codebook conventions)
AGECAT_LABELS = {1: "18-29", 2: "30-49", 3: "50-64", 4: "65+", 99: "Refused"}


def main():
    df = pd.read_csv(RAW, usecols=[
        "F_AGECAT", "F_RACETHNMOD",
        "VOTECHOICE2020", "VOTECHOICE2024",
        "WEIGHT_W159_VALIDATEDVOTE",
    ], low_memory=False)

    # Validated universe
    vv = df[df["WEIGHT_W159_VALIDATEDVOTE"].notna()
            & (df["WEIGHT_W159_VALIDATEDVOTE"] > 0)].copy()
    print(f"Validated voter universe (weight > 0): N={len(vv)}, "
          f"weighted total={vv['WEIGHT_W159_VALIDATEDVOTE'].sum():.1f}")

    # Biden 2020 voters (VOTECHOICE2020 == 2)
    biden = vv[vv["VOTECHOICE2020"] == 2].copy()
    print(f"Biden 2020 voters (validated): N={len(biden)}, "
          f"weighted={biden['WEIGHT_W159_VALIDATEDVOTE'].sum():.1f}")
    print()

    # Bucket VOTECHOICE2024
    def bucket(v):
        if pd.isna(v): return "did_not_vote"
        if v == 2: return "harris_retained"
        if v == 1: return "trump_flip"
        if v == 3: return "third_party"
        return "other"
    biden["bucket_2024"] = biden["VOTECHOICE2024"].apply(bucket)

    # Drop refused-cohort respondents
    biden_c = biden[biden["F_AGECAT"].isin([1, 2, 3, 4])].copy()
    biden_c["cohort_band"] = biden_c["F_AGECAT"].map(AGECAT_LABELS)
    print(f"Biden 2020 with valid F_AGECAT: N={len(biden_c)}")
    print()

    # Compute weighted % per cohort × bucket
    grp = (biden_c.groupby(["cohort_band", "bucket_2024"])["WEIGHT_W159_VALIDATEDVOTE"]
                  .sum()
                  .unstack(fill_value=0.0))
    # Ensure all 4 buckets present
    for b in ["harris_retained", "trump_flip", "third_party", "did_not_vote"]:
        if b not in grp.columns:
            grp[b] = 0.0
    grp = grp[["harris_retained", "trump_flip", "third_party", "did_not_vote"]]
    row_totals = grp.sum(axis=1)
    pct = grp.div(row_totals, axis=0) * 100
    pct["weighted_N"] = row_totals.round(1)
    pct["unweighted_N"] = biden_c.groupby("cohort_band").size()

    cohort_order = ["18-29", "30-49", "50-64", "65+"]
    pct = pct.reindex(cohort_order)
    print("=== H7 decomposition: Biden 2020 voters by 2024 outcome, per Pew F_AGECAT ===")
    print(pct.round(2).to_string())

    pct.to_csv(OUT)
    print(f"\nSaved: {OUT}")

    # Also compute defection rate (1 - retention) for headline
    defection = 100 - pct["harris_retained"]
    print("\n=== Defection rate (1 - Harris retention) by cohort band ===")
    for c in cohort_order:
        print(f"  {c}: {defection[c]:.2f}%  (weighted N={pct.loc[c,'weighted_N']:.0f}, "
              f"unweighted N={int(pct.loc[c,'unweighted_N'])})")

    # Flip-vs-skip decomposition (among defectors)
    print("\n=== Flip-vs-skip decomposition (among Biden-2020 non-retainers) ===")
    for c in cohort_order:
        nonret = grp.loc[c, "trump_flip"] + grp.loc[c, "third_party"] + grp.loc[c, "did_not_vote"]
        if nonret > 0:
            print(f"  {c}: flip-to-Trump {100*grp.loc[c,'trump_flip']/nonret:.1f}% / "
                  f"flip-to-third {100*grp.loc[c,'third_party']/nonret:.1f}% / "
                  f"skip {100*grp.loc[c,'did_not_vote']/nonret:.1f}%")

if __name__ == "__main__":
    main()
