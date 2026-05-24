"""v2.3 — CES VV cohort-stratified Bidento2024 outcome decomposition (fine cohort cuts).

Per prereg_v2.3 §1. Universe: CES VV-matched Biden-2020 voters with
valid birthyr + TS_g2024 (voter-file match). Buckets: retained_harris /
flipped_trump / flipped_third / skipped, weighted by vvweight_post.
"""

from pathlib import Path
import pandas as pd
import numpy as np

RAW = Path("D:/DNC/data/raw/ces_2024/CCES24_Common_OUTPUT_vv_topost_final.csv")
OUT = Path("D:/DNC/data/processed/fits/h7_ces_decomp.csv")
OUT_DECOMP = Path("D:/DNC/data/processed/fits/h7_ces_decomp_table_b.csv")

COHORT_ORDER = ["Silent", "Boomer", "GenX", "MillOld", "MillYoung", "GenZ"]


def birthyr_to_cohort6(by):
    if pd.isna(by) or by < 1900 or by > 2010:
        return np.nan
    if by >= 1997: return "GenZ"
    if by >= 1989: return "MillYoung"
    if by >= 1981: return "MillOld"
    if by >= 1965: return "GenX"
    if by >= 1946: return "Boomer"
    return "Silent"


def bucket(row):
    ts = row["TS_g2024"]
    cc = row["CC24_410"]
    if pd.isna(ts):
        return "vf_match_missing"
    if ts == 7:
        return "skipped"
    if ts in [1, 2, 3, 4, 5, 6]:
        if pd.isna(cc):
            return "voted_unknown_choice"
        if cc == 1:
            return "retained_harris"
        if cc == 2:
            return "flipped_trump"
        if cc in [3, 4, 5, 8]:
            return "flipped_third"
        return "voted_unknown_choice"
    return "other"


def main():
    df = pd.read_csv(RAW, usecols=[
        "TS_g2024", "CC24_410", "presvote20post",
        "vvweight_post", "birthyr",
    ], low_memory=False)
    print(f"CES total N = {len(df)}")

    # Filter: VV-matched + Biden 2020 + valid birthyr
    mask = (df["vvweight_post"].notna() & (df["vvweight_post"] > 0)
            & (df["presvote20post"] == 1)
            & df["birthyr"].notna()
            & (df["birthyr"] >= 1900) & (df["birthyr"] <= 2010))
    biden = df[mask].copy()
    biden["cohort"] = biden["birthyr"].apply(birthyr_to_cohort6)
    biden = biden[biden["cohort"].notna()].copy()
    print(f"VV-matched + Biden 2020 + valid cohort: N = {len(biden)}")

    biden["bucket"] = biden.apply(bucket, axis=1)
    print(f"\nUniverse bucket counts (raw, unweighted):")
    print(biden["bucket"].value_counts())

    # Track vf_match_missing per cohort (transparency check per §4)
    vf_miss = biden[biden["bucket"] == "vf_match_missing"]
    vu = biden[biden["bucket"] == "voted_unknown_choice"]
    print(f"\nvf_match_missing per cohort:")
    print(vf_miss["cohort"].value_counts().reindex(COHORT_ORDER, fill_value=0))
    print(f"\nvoted_unknown_choice per cohort:")
    print(vu["cohort"].value_counts().reindex(COHORT_ORDER, fill_value=0))

    # Restrict to 4 main buckets for Table A
    main_buckets = ["retained_harris", "flipped_trump", "flipped_third", "skipped"]
    decomp = biden[biden["bucket"].isin(main_buckets)].copy()
    print(f"\nMain-buckets universe (excl. vf_match_missing + voted_unknown_choice): N = {len(decomp)}")
    print(f"  per cohort:")
    print(decomp.groupby("cohort").size().reindex(COHORT_ORDER, fill_value=0))

    # === Table A: weighted % per cohort x bucket ===
    grp = (decomp.groupby(["cohort", "bucket"])["vvweight_post"]
                .sum()
                .unstack(fill_value=0.0))
    for b in main_buckets:
        if b not in grp.columns:
            grp[b] = 0.0
    grp = grp[main_buckets]
    row_totals = grp.sum(axis=1)
    pct = grp.div(row_totals, axis=0) * 100
    pct["weighted_N"] = row_totals.round(1)
    pct["unweighted_N"] = decomp.groupby("cohort").size().reindex(pct.index)
    pct = pct.reindex(COHORT_ORDER)
    print("\n=== Table A: weighted % per cohort (Biden-2020 to 2024 outcome) ===")
    print(pct.round(2).to_string())
    pct.to_csv(OUT)
    print(f"\nSaved Table A: {OUT}")

    # === Table B: defection + skip_share + flip_share ===
    tb = pd.DataFrame(index=COHORT_ORDER)
    tb["defection_rate_pct"] = 100 - pct["retained_harris"]
    non_retained = (grp["flipped_trump"] + grp["flipped_third"] + grp["skipped"])
    tb["skip_share_of_non_retained_pct"] = 100 * grp["skipped"] / non_retained
    tb["flip_trump_share_pct"] = 100 * grp["flipped_trump"] / non_retained
    tb["flip_third_share_pct"] = 100 * grp["flipped_third"] / non_retained
    tb = tb.round(2)
    print("\n=== Table B: defection + skip-share + flip-share ===")
    print(tb.to_string())
    tb.to_csv(OUT_DECOMP)
    print(f"\nSaved Table B: {OUT_DECOMP}")

    # === Verdicts ===
    print("\n=== H13 verdict (cohort gradient of defection, MONOTONIC younger to older?) ===")
    def_rates = tb["defection_rate_pct"].values  # Silent..GenZ
    # Per pre-reg: monotonically non-increasing from MillYoung/GenZ to Silent
    # I.e., reversed order: GenZ..MillYoung..MillOld..GenX..Boomer..Silent should be non-increasing
    rev = tb["defection_rate_pct"][::-1].values
    diffs = np.diff(rev)
    inversions = (diffs > 0).sum()
    max_inv = max(diffs) if len(diffs) else 0
    print(f"  Defection rates (GenZ to Silent): {rev.round(2).tolist()}")
    print(f"  Adjacent-pair differences (older - younger): {diffs.round(2).tolist()}")
    print(f"  Inversions (older > younger): {inversions}; max inversion = {max_inv:.2f}pp")
    if inversions == 0:
        h13 = "CONFIRMED (strict monotone)"
    elif inversions <= 1 and max_inv <= 3.0:
        h13 = "PARTIAL (1 small inversion)"
    else:
        h13 = "REFUTED"
    print(f"  H13 verdict: {h13}")

    print("\n=== H14 verdict (skip dominates non-retention?) ===")
    skip_shares = tb["skip_share_of_non_retained_pct"].values
    n_above_50 = (skip_shares >= 50).sum()
    print(f"  Skip-shares per cohort: {dict(zip(COHORT_ORDER, skip_shares.round(2)))}")
    print(f"  Cohorts with skip_share >= 50%: {n_above_50} of 6")
    if n_above_50 == 6:
        h14 = "CONFIRMED (skip dominates in ALL cohorts)"
    elif n_above_50 >= 4:
        h14 = f"PARTIAL ({n_above_50} of 6)"
    else:
        h14 = "REFUTED"
    print(f"  H14 verdict: {h14}")

    print("\n=== H15 verdict (GenZ Biden-coalition more loyal than MillYoung?) ===")
    ret_genz = pct.loc["GenZ", "retained_harris"]
    ret_millyoung = pct.loc["MillYoung", "retained_harris"]
    diff = ret_genz - ret_millyoung
    print(f"  retention_rate(GenZ) = {ret_genz:.2f}%")
    print(f"  retention_rate(MillYoung) = {ret_millyoung:.2f}%")
    print(f"  GenZ - MillYoung = {diff:+.2f}pp")
    if diff >= 3.0:
        h15 = "CONFIRMED (GenZ more loyal by >=3pp)"
    elif diff <= -3.0:
        h15 = "REFUTED (MillYoung more loyal by >=3pp)"
    else:
        h15 = f"TIE ({diff:+.2f}pp, within 3pp)"
    print(f"  H15 verdict: {h15}")

    print("\n=== Aggregate verdict ===")
    confirmed_count = sum(1 for v in [h13, h14] if v.startswith("CONFIRMED"))
    refuted_count = sum(1 for v in [h13, h14] if v == "REFUTED")
    if confirmed_count == 2:
        agg = "TURNOUT-MECHANISM CONFIRMED (H13+H14 both CONFIRMED)"
    elif refuted_count > 0:
        agg = "PEW H7 NOT REPLICATED (H13 or H14 REFUTED)"
    elif confirmed_count >= 1:
        agg = "MECHANISM PARTIAL"
    else:
        agg = "ALL PARTIAL/TIE"
    print(f"  H13/H14: {agg}")
    if h15.startswith("CONFIRMED"):
        print(f"  H15: H6 GENZ-DIRECTION REPLICATED")
    elif h15 == "REFUTED":
        print(f"  H15: H6 GENZ-DIRECTION REFUTED on CES VV")
    else:
        print(f"  H15: TIE — no evidence either way at this N")


if __name__ == "__main__":
    main()
