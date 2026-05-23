"""
DNC post-mortem - Substrate -> Stan data prep (Model A) v2.

Per pre-reg §4 + §7 + operationalization supplement §3.

v2 adds:
- ANES sex (V241551), state-derived region (V241023), 2020 vote recall
  (V241104), retrospective econ perception (V241291)
- CES vote-choice (CC24_410), 2020 recall (presvote20post)
- GSS issue-only data prep (no vote; spending priorities)
- Fundamentals matrix: 2020 vote (one-hot), economic perception z-score

Outputs Stan-ready dict per (substrate, outcome). Persisted via joblib.
"""

from pathlib import Path
import numpy as np
import pandas as pd
import joblib

RAW = Path("D:/DNC/data/raw")
PROCESSED = Path("D:/DNC/data/processed")
PROCESSED.mkdir(parents=True, exist_ok=True)


def age_to_cohort(age):
    if pd.isna(age) or age < 18:
        return np.nan
    if age <= 27: return "GenZ"
    elif age <= 43: return "Millennial"
    elif age <= 59: return "GenX"
    elif age <= 78: return "Boomer"
    else: return "Silent"


def birthyr_to_cohort(birthyr):
    if pd.isna(birthyr) or birthyr < 1900 or birthyr > 2010:
        return np.nan
    if birthyr >= 1997: return "GenZ"
    elif birthyr >= 1981: return "Millennial"
    elif birthyr >= 1965: return "GenX"
    elif birthyr >= 1946: return "Boomer"
    else: return "Silent"


COHORT_LEVELS = ["Silent", "Boomer", "GenX", "Millennial", "GenZ"]

# Census state FIPS → 4-region (Census)
STATE_FIPS_TO_REGION = {
    9: "NE", 23: "NE", 25: "NE", 33: "NE", 44: "NE", 50: "NE",
    34: "NE", 36: "NE", 42: "NE",
    18: "MW", 17: "MW", 26: "MW", 39: "MW", 55: "MW",
    19: "MW", 20: "MW", 27: "MW", 29: "MW", 31: "MW", 38: "MW", 46: "MW",
    10: "South", 11: "South", 12: "South", 13: "South", 24: "South", 37: "South",
    45: "South", 51: "South", 54: "South",
    1: "South", 21: "South", 28: "South", 47: "South",
    5: "South", 22: "South", 40: "South", 48: "South",
    4: "West", 8: "West", 16: "West", 30: "West", 32: "West", 35: "West", 49: "West", 56: "West",
    2: "West", 6: "West", 15: "West", 41: "West", 53: "West",
}


def _zscore(x):
    arr = pd.Series(x).astype(float)
    return ((arr - arr.mean()) / arr.std()).values


def _build_data_dict(df_clean, outcome_col, outcome_kind, weight_col=None):
    """Build Stan data dict from cleaned dataframe with cols:
    age, cohort, race, educ, gender, region, y (already coded), and any fund_ cols."""
    race_levels = sorted(df_clean["race"].dropna().unique())
    educ_levels = sorted(df_clean["educ"].dropna().unique())
    cohort_levels = [c for c in COHORT_LEVELS if c in df_clean["cohort"].values]
    if len(cohort_levels) < 2:
        cohort_levels = sorted(df_clean["cohort"].dropna().unique())
    gender_levels = sorted(df_clean["gender"].dropna().unique())
    region_levels = sorted(df_clean["region"].dropna().unique())

    race_idx = pd.Categorical(df_clean["race"], categories=race_levels).codes + 1
    educ_idx = pd.Categorical(df_clean["educ"], categories=educ_levels).codes + 1
    cohort_idx = pd.Categorical(df_clean["cohort"], categories=cohort_levels).codes + 1
    gender_idx = pd.Categorical(df_clean["gender"], categories=gender_levels).codes + 1
    region_idx = pd.Categorical(df_clean["region"], categories=region_levels).codes + 1

    # Fundamentals: pick up any column starting with "fund_"
    fund_cols = [c for c in df_clean.columns if c.startswith("fund_")]
    if fund_cols:
        X_fund = df_clean[fund_cols].values
    else:
        # Fallback: just z-score of age as a placeholder
        X_fund = _zscore(df_clean["age"]).reshape(-1, 1)
        fund_cols = ["age_z"]

    y = df_clean[outcome_col].values
    y = y.astype(int).tolist() if outcome_kind == "binary" else y.astype(float).tolist()

    weights = (df_clean[weight_col].fillna(1.0).values.tolist()
               if weight_col and weight_col in df_clean.columns
               else np.ones(len(df_clean)).tolist())

    data = {
        "N": len(df_clean),
        "K_fund": X_fund.shape[1],
        "X_fund": X_fund,
        "N_race": len(race_levels),
        "N_educ": len(educ_levels),
        "N_cohort": len(cohort_levels),
        "N_gender": len(gender_levels),
        "N_region": len(region_levels),
        "race": race_idx.astype(int).tolist(),
        "educ": educ_idx.astype(int).tolist(),
        "cohort": cohort_idx.astype(int).tolist(),
        "gender": gender_idx.astype(int).tolist(),
        "region": region_idx.astype(int).tolist(),
        "y": y,
        "weight": weights,
    }
    meta = {
        "n_used": len(df_clean),
        "race_levels": race_levels, "educ_levels": educ_levels,
        "cohort_levels": cohort_levels, "gender_levels": gender_levels,
        "region_levels": region_levels, "fund_cols": fund_cols,
    }
    return data, meta


# ---------------- ANES ----------------

def anes_load_and_prep(outcome="vote"):
    """ANES 2024 Model A data prep."""
    p = RAW / "anes_2024" / "anes_timeseries_2024_csv_20260519.csv"
    df = pd.read_csv(p, low_memory=False)
    n0 = len(df)

    # Demographics
    df["age"] = df["V241458x"].where(df["V241458x"] >= 18)
    df["cohort"] = df["age"].apply(age_to_cohort)
    race_map = {1: "white", 2: "black", 3: "hispanic", 4: "asian", 5: "nhpi", 6: "other"}
    df["race"] = df["V241501x"].map(race_map)
    def educ_grp(v):
        if v < 0: return np.nan
        if v <= 10: return "lt_hs"
        if v <= 12: return "hs"
        if v == 13: return "some_col"
        if v == 14: return "ba"
        return "grad"
    df["educ"] = df["V241463"].apply(educ_grp)
    gender_map = {1: "man", 2: "woman", 3: "nb", 4: "other"}
    df["gender"] = df["V241551"].map(gender_map)
    # State FIPS → region
    df["region"] = df["V241023"].apply(lambda v: STATE_FIPS_TO_REGION.get(int(v), np.nan) if v > 0 else np.nan)

    # Fundamentals
    # V241104 = 2020 recall: 1=Biden, 2=Trump, 5=Other, -1=Inap, -8/-9=DK/RF
    recall_map = {1: "biden", 2: "trump", 5: "other"}
    df["recall20"] = df["V241104"].map(recall_map).fillna("nonvoter")
    # One-hot for recall (drop nonvoter as baseline)
    for level in ["biden", "trump", "other"]:
        df[f"fund_recall20_{level}"] = (df["recall20"] == level).astype(int)
    # V241291: NATIONAL ECONOMY BETTER OR WORSE — 1=much better, 5=much worse (need to verify)
    df["fund_econ_z"] = _zscore(df["V241291"].where(df["V241291"] > 0))
    df["fund_econ_z"] = df["fund_econ_z"].fillna(0.0)

    # Outcome
    outcome_kind = "binary"
    if outcome == "vote":
        df = df[df["V242096x"].isin([1, 2])].copy()
        df["y"] = (df["V242096x"] == 1).astype(int)  # 1 = Harris
    elif outcome == "vote_partyid":
        # v2 probe: ANES vote with party-ID 7pt added as fundamental.
        # Tests whether race-on-vote shrinks when conditioned on partisanship.
        df = df[df["V242096x"].isin([1, 2]) & (df["V241227x"] > 0)].copy()
        df["y"] = (df["V242096x"] == 1).astype(int)
        df["fund_pid7_z"] = _zscore(df["V241227x"].astype(float))
    elif outcome == "gaza_aid_pal":
        # V241404: PRE FAVOR/OPPOSE U.S. GIVING HUMANITARIAN AID TO PALESTINIANS
        # 1=Favor, 2=Oppose, 3=Neither. z>0 = more opposed/neutral relative to favor.
        df = df[df["V241404"].isin([1, 2, 3])].copy()
        df["y"] = _zscore(df["V241404"])
        outcome_kind = "gaussian"
    elif outcome == "israel_military":
        # V241401: PRE FAVOR/OPPOSE U.S. GIVING MILITARY ASSISTANCE TO ISRAEL
        # 1=Favor, 2=Oppose, 3=Neither. z>0 = more opposed.
        df = df[df["V241401"].isin([1, 2, 3])].copy()
        df["y"] = _zscore(df["V241401"])
        outcome_kind = "gaussian"
    elif outcome == "gaza_protests":
        # V241410: PRE APPROVE/DISAPPROVE PROTESTS AGAINST WAR IN GAZA
        # 1=Approve, 2=Disapprove, 3=Neither. z>0 = more disapproving.
        df = df[df["V241410"].isin([1, 2, 3])].copy()
        df["y"] = _zscore(df["V241410"])
        outcome_kind = "gaussian"
    elif outcome == "single_payer":
        # V241245: PRE 7PT SELF-PLACEMENT gov-vs-private medical insurance.
        # 1=Government insurance plan, 7=Private insurance plan, 99=Haven't thought (DROP).
        # z>0 = more pro-private.  CORRECTED FROM V241247 (Trump placement) §12 dev 8.
        df = df[df["V241245"].isin(range(1, 8))].copy()  # keep 1..7, drop 99 + DK/RF/Inap
        df["y"] = _zscore(df["V241245"])
        outcome_kind = "gaussian"
    elif outcome == "race_relations":
        # Need correct V-code; placeholder
        return None
    else:
        return None

    needed = ["age", "cohort", "race", "educ", "gender", "region"]
    df_clean = df.dropna(subset=needed).copy()
    data, sub_meta = _build_data_dict(df_clean, "y", outcome_kind)

    meta = {
        "substrate": "ANES", "outcome": outcome, "outcome_kind": outcome_kind,
        "n0_raw": n0, **sub_meta,
        "fundamentals_note": "v2: 2020 recall one-hot + V241291 econ retrospective z",
    }
    return data, meta


# ---------------- CES ----------------

def ces_load_and_prep(outcome="vote"):
    """CES 2024 Model A data prep."""
    p = RAW / "ces_2024" / "CCES24_Common_OUTPUT_vv_topost_final.csv"
    df = pd.read_csv(p, low_memory=False)
    n0 = len(df)

    df["cohort"] = df["birthyr"].apply(birthyr_to_cohort)
    df["age"] = 2024 - df["birthyr"]
    race_map = {1: "white", 2: "black", 3: "hispanic", 4: "asian",
                5: "nhpi", 6: "other", 7: "other", 8: "other"}
    df["race"] = df["race"].map(race_map)
    educ_map = {1: "lt_hs", 2: "hs", 3: "some_col", 4: "some_col", 5: "ba", 6: "grad"}
    df["educ"] = df["educ"].map(educ_map)
    gender_map = {1: "man", 2: "woman", 3: "nb", 4: "other"}
    df["gender"] = df["gender4"].map(gender_map)
    region_map = {1: "NE", 2: "MW", 3: "South", 4: "West"}
    df["region"] = df["region"].map(region_map)

    # Fundamentals
    # presvote20post: 1=Biden, 2=Trump, 3=other, 4=did-not-vote (CES coding)
    recall_map = {1: "biden", 2: "trump", 3: "other"}
    df["recall20"] = df["presvote20post"].map(recall_map).fillna("nonvoter")
    for level in ["biden", "trump", "other"]:
        df[f"fund_recall20_{level}"] = (df["recall20"] == level).astype(int)
    # Econ perception — CES has CC24_303 or similar. Use a placeholder if missing.
    if "CC24_303" in df.columns:
        df["fund_econ_z"] = _zscore(df["CC24_303"].where(df["CC24_303"] > 0))
        df["fund_econ_z"] = df["fund_econ_z"].fillna(0.0)
    else:
        df["fund_econ_z"] = 0.0

    outcome_kind = "binary"
    if outcome == "vote":
        df = df[df["CC24_410"].isin([1, 2])].copy()
        df["y"] = (df["CC24_410"] == 1).astype(int)  # 1 = Harris
    elif outcome == "single_payer":
        # CES single-payer item; find in v3
        return None
    elif outcome == "structural_inequity":
        # CES racial resentment battery; find in v3
        return None
    else:
        return None

    needed = ["age", "cohort", "race", "educ", "gender", "region"]
    df_clean = df.dropna(subset=needed).copy()
    data, sub_meta = _build_data_dict(df_clean, "y", outcome_kind, weight_col="commonweight")

    meta = {
        "substrate": "CES", "outcome": outcome, "outcome_kind": outcome_kind,
        "n0_raw": n0, **sub_meta,
        "fundamentals_note": "v2: presvote20post one-hot + CC24_303 econ z (if present)",
    }
    return data, meta


# ---------------- GSS ----------------

def gss_load_and_prep(outcome="science"):
    """GSS 2024 Model A data prep — issue-only (no vote choice in 2024 wave).

    outcome ∈ {"science", "foreign_aid"}
    """
    p = RAW / "gss_2024" / "2024" / "GSS2024.dta"
    df = pd.read_stata(p, convert_categoricals=False)
    n0 = len(df)

    df["age"] = df["age"].where(df["age"] >= 18)
    df["cohort"] = df.get("cohort", pd.Series(index=df.index, dtype=float)).apply(birthyr_to_cohort)
    if df["cohort"].isna().all():
        df["cohort"] = df["age"].apply(age_to_cohort)
    # Race
    race_map = {1: "white", 2: "black", 3: "other"}
    df["race"] = df["race"].map(race_map)
    if "hispanic" in df.columns:
        df["race"] = df.apply(lambda r: "hispanic" if (r.get("hispanic", 0) and r["hispanic"] > 0 and r["hispanic"] != 1) else r["race"], axis=1)
    # Sex (1=Male, 2=Female)
    gender_map = {1: "man", 2: "woman"}
    df["gender"] = df["sex"].map(gender_map)
    # Region (GSS 2024 uses 4-level coding: 1=NE, 2=MW, 3=South, 4=West)
    region_map = {1: "NE", 2: "MW", 3: "South", 4: "West"}
    df["region"] = df["region"].map(region_map)
    # Education collapsed
    def gss_educ_grp(v):
        if pd.isna(v) or v < 0: return np.nan
        if v < 12: return "lt_hs"
        if v == 12: return "hs"
        if v < 16: return "some_col"
        if v == 16: return "ba"
        return "grad"
    df["educ"] = df["educ"].apply(gss_educ_grp)

    # No fundamentals on GSS (no pres24, no 2020 recall, no comparable econ item in core)
    df["fund_intercept"] = 1.0  # passthrough constant; X_fund has at least 1 col

    outcome_kind = "gaussian"
    if outcome == "science":
        # natsci: 1=too little, 2=about right, 3=too much (reverse to higher=more support)
        df = df[df["natsci"].isin([1, 2, 3])].copy()
        df["y_raw"] = -1 * (df["natsci"] - 2)  # +1 too little support, -1 too much
        df["y"] = _zscore(df["y_raw"])
    elif outcome == "foreign_aid":
        df = df[df["nataid"].isin([1, 2, 3])].copy()
        df["y_raw"] = -1 * (df["nataid"] - 2)
        df["y"] = _zscore(df["y_raw"])
    else:
        return None

    needed = ["age", "cohort", "race", "educ", "gender", "region"]
    df_clean = df.dropna(subset=needed).copy()
    data, sub_meta = _build_data_dict(df_clean, "y", outcome_kind, weight_col="wtssps")

    meta = {
        "substrate": "GSS", "outcome": outcome, "outcome_kind": outcome_kind,
        "n0_raw": n0, **sub_meta,
        "fundamentals_note": "v2: GSS has no comparable fundamentals; intercept-only fund",
    }
    return data, meta


# ---------------- Main ----------------

if __name__ == "__main__":
    print("=== Data prep v2 ===\n")
    jobs = [
        ("ANES vote",            lambda: anes_load_and_prep("vote")),
        ("ANES vote_partyid",    lambda: anes_load_and_prep("vote_partyid")),
        ("ANES gaza_aid_pal",    lambda: anes_load_and_prep("gaza_aid_pal")),
        ("ANES israel_military", lambda: anes_load_and_prep("israel_military")),
        ("ANES gaza_protests",   lambda: anes_load_and_prep("gaza_protests")),
        ("ANES single_payer",    lambda: anes_load_and_prep("single_payer")),
        ("CES vote",             lambda: ces_load_and_prep("vote")),
        ("GSS science",          lambda: gss_load_and_prep("science")),
        ("GSS foreign_aid",      lambda: gss_load_and_prep("foreign_aid")),
    ]
    for name, fn in jobs:
        print(f"--- {name} ---")
        try:
            result = fn()
            if result is None:
                print("  (skipped - outcome not yet wired)")
                continue
            data, meta = result
            print(f"  raw {meta['n0_raw']} -> used {meta['n_used']}, K_fund={data['K_fund']}, fund_cols={meta['fund_cols']}")
            print(f"  race {meta['race_levels']}; educ {meta['educ_levels']}; cohort {meta['cohort_levels']}")
            print(f"  gender {meta['gender_levels']}; region {meta['region_levels']}")
            outpath = PROCESSED / f"stan_data_{meta['substrate'].lower()}_{meta['outcome']}.joblib"
            joblib.dump({"data": data, "meta": meta}, outpath)
            print(f"  saved: {outpath}")
        except Exception as e:
            print(f"  ERROR: {type(e).__name__}: {e}")
        print()
