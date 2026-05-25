"""v2.7 — ANES alt-right-PROXY composite + 3 sub-hypotheses.

Per prereg_v2.7_dnc_postmortem.md HEAD bb21e1a.

Composite (LOCKED) — HIGH = MORE alt-right-PROXY-aligned:
  rr_composite_z   : racial resentment 4-item K-S (V242300-V242303), canonical
  immigration_z    : mean of REVERSED V241389x + REVERSED V241392x + REVERSED V241395x
  grievance_z      : mean of V241353x (keep) + REVERSED V241350x + REVERSED V241344x
  anti_dei_z       : mean of V241290x (keep) + V241287x (keep)
altright_proxy_z = z-score of mean of 4 sub-composites.

Directions verified against codebook 2026-05-24 (commit bb21e1a §10 dev N/A).
"""

from pathlib import Path
import pandas as pd
import numpy as np

RAW = Path("D:/DNC/data/raw/anes_2024/anes_timeseries_2024_csv_20260519.csv")
OUT_DIR = Path("D:/DNC/data/processed/v27")
OUT_DIR.mkdir(exist_ok=True)


def _valid(s, low=1, high=7):
    """Return values in [low, high]; else NaN."""
    return s.where((s >= low) & (s <= high))


def main():
    cols = [
        "V242096x", "V241104",  # 2024 vote + 2020 recall
        # Racial resentment battery
        "V242300", "V242301", "V242302", "V242303",
        # Immigration
        "V241389x", "V241392x", "V241395x",
        # Grievance
        "V241353x", "V241350x", "V241344x",
        # Anti-DEI / anti-academic
        "V241290x", "V241287x",
        # Cohort
        "V241458x",
    ]
    df = pd.read_csv(RAW, usecols=cols, low_memory=False)
    n0 = len(df)
    print(f"Raw N = {n0}")

    # === Cohort ===
    def age_to_cohort(a):
        if pd.isna(a) or a < 18: return None
        if a <= 27: return "GenZ"
        if a <= 35: return "MillYoung"
        if a <= 43: return "MillOld"
        if a <= 59: return "GenX"
        if a <= 78: return "Boomer"
        return "Silent"
    df["age"] = df["V241458x"].where(df["V241458x"] >= 18)
    df["cohort6"] = df["age"].apply(age_to_cohort)
    # Also collapsed 5-cohort to match v1.x
    def to_5(c):
        if c in ("MillYoung", "MillOld"): return "Millennial"
        return c
    df["cohort5"] = df["cohort6"].apply(to_5)

    # === Racial resentment composite (canonical: HIGH = MORE resent) ===
    # V242300 WORKWAY agree=more resent → REVERSE (6-raw); 1-5
    # V242301 GENRTNS agree=less resent → KEEP
    # V242302 DESERVE agree=less resent → KEEP
    # V242303 TRYHARDER agree=more resent → REVERSE
    rr_workway = 6 - _valid(df["V242300"], 1, 5)
    rr_genrtns = _valid(df["V242301"], 1, 5)
    rr_deserve = _valid(df["V242302"], 1, 5)
    rr_tryharder = 6 - _valid(df["V242303"], 1, 5)
    rr_mean = pd.concat([rr_workway, rr_genrtns, rr_deserve, rr_tryharder], axis=1).mean(axis=1)
    df["rr_composite_z"] = (rr_mean - rr_mean.mean()) / rr_mean.std()

    # === Immigration restrictionism (HIGH = more restrictionist) ===
    # V241389x birthright: 1=Favor great deal ending, 7=Oppose great deal → KEEP (1=favor ending = restrictionist)
    # Wait, I want HIGH=restrictionist. raw 1=favor ending = restrictionist. So REVERSE (8-raw) so HIGH=favor ending.
    imm_birthright = 8 - _valid(df["V241389x"], 1, 7)
    # V241392x: 1=send back great deal, 6=allow stay great deal → REVERSE (7-raw) so HIGH=send back=restrictionist
    imm_kids = 7 - _valid(df["V241392x"], 1, 6)
    # V241395x wall: 1=favor great deal, 7=oppose great deal → REVERSE (8-raw) so HIGH=favor wall=restrictionist
    imm_wall = 8 - _valid(df["V241395x"], 1, 7)
    imm_mean = pd.concat([imm_birthright, imm_kids, imm_wall], axis=1).mean(axis=1)
    df["immigration_z"] = (imm_mean - imm_mean.mean()) / imm_mean.std()

    # === Trump-grievance composite (HIGH = more grievance/alt-right-aligned) ===
    # V241353x: 1=fairly very strongly, 6=unfairly very strongly → KEEP (HIGH=agrees Trump treated unfairly)
    griev_trump_unfair = _valid(df["V241353x"], 1, 6)
    # V241350x: 1=approve very strongly immunity, 6=disapprove → REVERSE (7-raw) HIGH=approve immunity
    griev_immune = 7 - _valid(df["V241350x"], 1, 6)
    # V241344x: 1=increased great deal corruption, 7=decreased → REVERSE (8-raw) HIGH=increased
    griev_corrupt = 8 - _valid(df["V241344x"], 1, 7)
    griev_mean = pd.concat([griev_trump_unfair, griev_immune, griev_corrupt], axis=1).mean(axis=1)
    df["grievance_z"] = (griev_mean - griev_mean.mean()) / griev_mean.std()

    # === Anti-DEI / anti-academic (HIGH = more opposition = alt-right-aligned) ===
    # V241290x DEI: 1=favor great deal, 7=oppose great deal → KEEP (HIGH=oppose DEI)
    ad_dei = _valid(df["V241290x"], 1, 7)
    # V241287x colleges run: 1=approve very strongly, 7=disapprove strongly → KEEP (HIGH=disapprove colleges)
    ad_colleges = _valid(df["V241287x"], 1, 7)
    ad_mean = pd.concat([ad_dei, ad_colleges], axis=1).mean(axis=1)
    df["anti_dei_z"] = (ad_mean - ad_mean.mean()) / ad_mean.std()

    # === Top-level composite ===
    sub_z = df[["rr_composite_z", "immigration_z", "grievance_z", "anti_dei_z"]]
    # Per pre-reg: require ≥2 of 4 sub-composites non-missing; missing ones mean-imputed to 0
    sub_nonmiss = sub_z.notna().sum(axis=1)
    df = df[sub_nonmiss >= 2].copy()
    sub_z_imp = sub_z.fillna(0.0).loc[df.index]
    top_mean = sub_z_imp.mean(axis=1)
    df["altright_proxy_z"] = (top_mean - top_mean.mean()) / top_mean.std()
    print(f"After ≥2/4 sub-composite valid: N = {len(df)}")
    print(f"altright_proxy_z stats: mean={df['altright_proxy_z'].mean():.3f} std={df['altright_proxy_z'].std():.3f} min={df['altright_proxy_z'].min():.2f} max={df['altright_proxy_z'].max():.2f}")

    # Quartiles
    q1, q3 = df["altright_proxy_z"].quantile([0.25, 0.75])
    df["quartile"] = pd.cut(df["altright_proxy_z"],
                             bins=[-np.inf, q1, df["altright_proxy_z"].median(), q3, np.inf],
                             labels=["Q1", "Q2", "Q3", "Q4"])
    print(f"Quartile cutoffs: Q1<{q1:.3f}, Q4>{q3:.3f}")

    # === Sample for H30 (2-party voters) ===
    voters = df[df["V242096x"].isin([1, 2])].copy()
    voters["vote_2024"] = voters["V242096x"].map({1: "Harris", 2: "Trump"})
    print(f"\n2-party voter universe: N={len(voters)}")

    # === H30: VOLUME ===
    print("\n" + "="*60)
    print("=== H30 VOLUME: alt-right-PROXY cluster x 2024 vote ===")
    print("="*60)
    h30_table = pd.crosstab(voters["quartile"], voters["vote_2024"], margins=False)
    h30_pct_col = pd.crosstab(voters["quartile"], voters["vote_2024"], normalize="columns") * 100
    h30_pct_row = pd.crosstab(voters["quartile"], voters["vote_2024"], normalize="index") * 100
    print("\nCounts (cohort_quartile x 2024 vote):")
    print(h30_table.to_string())
    print("\nWithin-vote columns (% of Trump / % of Harris voters in each quartile):")
    print(h30_pct_col.round(2).to_string())
    print("\nWithin-quartile rows (% of each quartile that voted Harris/Trump):")
    print(h30_pct_row.round(2).to_string())

    pct_trump_in_q4 = h30_pct_col.loc["Q4", "Trump"]
    pct_q4_voted_trump = h30_pct_row.loc["Q4", "Trump"]
    print(f"\nKEY: % of Trump 2024 voters in Q4 altright_proxy = {pct_trump_in_q4:.1f}%")
    print(f"KEY: % of Q4-cluster voters who voted Trump = {pct_q4_voted_trump:.1f}%")
    if pct_trump_in_q4 >= 40:
        h30_verdict = "CONFIRMED-LARGE-VOLUME"
    elif pct_trump_in_q4 >= 25:
        h30_verdict = "CONFIRMED-MEDIUM"
    else:
        h30_verdict = "LIMITED-VOLUME"
    print(f"H30 VERDICT: {h30_verdict}")

    # === H31: ALIENATION ===
    print("\n" + "="*60)
    print("=== H31 ALIENATION: Biden-2020 voters' 2024 flip rate by quartile + cohort ===")
    print("="*60)
    biden = voters[voters["V241104"] == 1].copy()
    print(f"Biden-2020 voters who voted 2-party 2024: N={len(biden)}")
    biden["flipped_to_trump"] = (biden["V242096x"] == 2).astype(int)
    # By quartile (aggregate)
    q_flip = biden.groupby("quartile", observed=True)["flipped_to_trump"].agg(["mean", "count"]) * pd.Series({"mean": 100, "count": 1})
    q_flip["mean"] = biden.groupby("quartile", observed=True)["flipped_to_trump"].mean() * 100
    q_flip["count"] = biden.groupby("quartile", observed=True).size()
    print("\nFlip-to-Trump rate by altright_proxy quartile:")
    print(q_flip.round(2).to_string())

    flip_q4 = q_flip.loc["Q4", "mean"]
    flip_q1 = q_flip.loc["Q1", "mean"]
    diff_q4q1 = flip_q4 - flip_q1
    print(f"\nKEY: Q4 flip rate = {flip_q4:.1f}%, Q1 flip rate = {flip_q1:.1f}%, gap = {diff_q4q1:+.1f}pp")

    # By cohort × quartile (look for MillYoung/Mill concentration)
    print("\nFlip-rate by cohort × altright_proxy quartile (6-cohort):")
    cq_flip = (biden.groupby(["cohort6", "quartile"], observed=True)["flipped_to_trump"].mean() * 100).unstack()
    cq_n = biden.groupby(["cohort6", "quartile"], observed=True).size().unstack(fill_value=0)
    cohort_order = ["Silent", "Boomer", "GenX", "MillOld", "MillYoung", "GenZ"]
    cq_flip = cq_flip.reindex(cohort_order)
    cq_n = cq_n.reindex(cohort_order)
    print("\nFlip rate (%):")
    print(cq_flip.round(2).to_string())
    print("\nCell N:")
    print(cq_n.to_string())

    # Verdict: Q4 flip rate ≥20pp higher than Q1, and concentrated in Mill/MillYoung
    mill_q4q1 = (cq_flip.loc["MillYoung", "Q4"] if not pd.isna(cq_flip.loc["MillYoung", "Q4"]) else None,
                 cq_flip.loc["MillYoung", "Q1"] if not pd.isna(cq_flip.loc["MillYoung", "Q1"]) else None)
    if diff_q4q1 >= 20 and (mill_q4q1[0] is not None and mill_q4q1[1] is not None and (mill_q4q1[0] - mill_q4q1[1]) >= 20):
        h31_verdict = "CONFIRMED (DNC alienation thesis)"
    elif diff_q4q1 >= 10:
        h31_verdict = "PARTIAL"
    else:
        h31_verdict = "REFUTED"
    print(f"\nH31 VERDICT: {h31_verdict}")

    # === H32: COUNTERFACTUAL CONTRIBUTION ===
    print("\n" + "="*60)
    print("=== H32 COUNTERFACTUAL: Trump 2024 voters decomposition ===")
    print("="*60)
    trump_voters = voters[voters["V242096x"] == 2].copy()
    total_trump = len(trump_voters)
    # A. Always-Republican (recall20 != 1 = not Biden)
    cell_A = trump_voters[trump_voters["V241104"] != 1]
    # B. Biden-2020 defectors × Q4 altright
    cell_B = trump_voters[(trump_voters["V241104"] == 1) & (trump_voters["quartile"] == "Q4")]
    # C. Biden-2020 defectors × non-Q4
    cell_C = trump_voters[(trump_voters["V241104"] == 1) & (trump_voters["quartile"] != "Q4")]
    print(f"Total Trump 2024 voters: {total_trump}")
    print(f"A. Non-Biden-2020 Trump voters (always-Republican / nonvoter / third 2020): N={len(cell_A)} ({100*len(cell_A)/total_trump:.1f}%)")
    print(f"B. Biden-2020 defectors with Q4-altright score: N={len(cell_B)} ({100*len(cell_B)/total_trump:.1f}%)")
    print(f"C. Biden-2020 defectors with non-Q4 altright score: N={len(cell_C)} ({100*len(cell_C)/total_trump:.1f}%)")

    pct_B = 100 * len(cell_B) / total_trump
    if pct_B >= 10:
        h32_verdict = "HIGH-CONTRIBUTION"
    elif pct_B >= 3:
        h32_verdict = "MEDIUM-CONTRIBUTION"
    else:
        h32_verdict = "LOW-CONTRIBUTION"
    print(f"\nH32 VERDICT: {h32_verdict} (cell B = {pct_B:.1f}% of Trump's 2024 ANES vote)")

    # === Aggregate verdict ===
    print("\n" + "="*60)
    print("=== AGGREGATE v2.7 VERDICT ===")
    print("="*60)
    print(f"H30 (volume): {h30_verdict}")
    print(f"H31 (alienation): {h31_verdict}")
    print(f"H32 (counterfactual): {h32_verdict}")

    # Save outputs
    h30_pct_col.to_csv(OUT_DIR / "h30_by_vote.csv")
    h30_pct_row.to_csv(OUT_DIR / "h30_by_quartile.csv")
    q_flip.to_csv(OUT_DIR / "h31_aggregate.csv")
    cq_flip.to_csv(OUT_DIR / "h31_cohort_x_quartile.csv")
    print(f"\nSaved tables under {OUT_DIR}")


if __name__ == "__main__":
    main()
