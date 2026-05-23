"""
DNC post-mortem - Substrate -> Stan data prep (Model A).

Per pre-reg §4 + §7 + operationalization supplement §3.

Three substrates with substantively different variable layouts:
  - ANES: V-coded; many demos restricted in public file (§12 deviation)
  - CES: human-readable col names; full battery on subset of issues
  - GSS: human-readable; spending-priorities Tier 2 only

Outputs: Stan-ready dict per (substrate, outcome). Persisted via joblib.
"""

from pathlib import Path
import numpy as np
import pandas as pd
import joblib

RAW = Path("D:/DNC/data/raw")
PROCESSED = Path("D:/DNC/data/processed")
PROCESSED.mkdir(parents=True, exist_ok=True)


# --------- Cohort coding (Pew cutoffs, age-derived) ---------

def age_to_cohort(age):
    """Pew cohort cutoffs via age at Nov 2024.

    Silent ≤1945 → age 79+
    Boomer 1946-1964 → age 60-78
    Gen X 1965-1980 → age 44-59
    Millennial 1981-1996 → age 28-43
    Gen Z 1997-2012 → age 18-27 (voting subset)
    """
    if pd.isna(age) or age < 18:
        return np.nan
    if age <= 27:
        return "GenZ"
    elif age <= 43:
        return "Millennial"
    elif age <= 59:
        return "GenX"
    elif age <= 78:
        return "Boomer"
    else:
        return "Silent"  # collapses with Boomer at ANES top-code 80


def birthyr_to_cohort(birthyr):
    """Pew cohort cutoffs from birth year (exact)."""
    if pd.isna(birthyr) or birthyr < 1900 or birthyr > 2010:
        return np.nan
    if birthyr >= 1997:
        return "GenZ"
    elif birthyr >= 1981:
        return "Millennial"
    elif birthyr >= 1965:
        return "GenX"
    elif birthyr >= 1946:
        return "Boomer"
    else:
        return "Silent"


COHORT_LEVELS = ["Silent", "Boomer", "GenX", "Millennial", "GenZ"]

# --------- Substrate-specific harmonization ---------

# Census state FIPS → 4-region (Census regions)
STATE_FIPS_TO_REGION = {
    # Northeast (1, 2)
    9: "NE", 23: "NE", 25: "NE", 33: "NE", 44: "NE", 50: "NE",  # New England
    34: "NE", 36: "NE", 42: "NE",  # Middle Atlantic
    # Midwest (3, 4)
    18: "MW", 17: "MW", 26: "MW", 39: "MW", 55: "MW",  # East North Central
    19: "MW", 20: "MW", 27: "MW", 29: "MW", 31: "MW", 38: "MW", 46: "MW",  # West North Central
    # South (5, 6, 7)
    10: "South", 11: "South", 12: "South", 13: "South", 24: "South", 37: "South",
    45: "South", 51: "South", 54: "South",  # South Atlantic
    1: "South", 21: "South", 28: "South", 47: "South",  # East South Central
    5: "South", 22: "South", 40: "South", 48: "South",  # West South Central
    # West (8, 9)
    4: "West", 8: "West", 16: "West", 30: "West", 32: "West", 35: "West", 49: "West", 56: "West",
    2: "West", 6: "West", 15: "West", 41: "West", 53: "West",  # Pacific
}


def anes_load_and_prep(outcome="vote"):
    """Load ANES 2024 and produce Stan-ready dict.

    outcome ∈ {"vote", "israel", "single_payer", "structural_inequity",
               "race_relations", "science_arts", "foreign_aid"}
    """
    p = RAW / "anes_2024" / "anes_timeseries_2024_csv_20260519.csv"
    df = pd.read_csv(p, low_memory=False)
    n0 = len(df)

    # ---- Demographics ----
    # Age (top-coded 80) → cohort
    df["age"] = df["V241458x"].where(df["V241458x"] >= 18)
    df["cohort"] = df["age"].apply(age_to_cohort)
    # Race summary (1=White, 2=Black, 3=Hispanic, 4=Asian, 5=NAt Hawaiian / API, 6=Other/multi, -9=DK/RF, -4=Error)
    race_map = {1: "white", 2: "black", 3: "hispanic", 4: "asian", 5: "nhpi", 6: "other"}
    df["race"] = df["V241501x"].map(race_map)
    # Education V241463 ANES codes (rough mapping: 9-10 lt_hs, 11-12 hs, 13 some_col, 14 ba, 15+ grad)
    def educ_grp(v):
        if v < 0: return np.nan
        if v <= 10: return "lt_hs"
        if v <= 12: return "hs"
        if v == 13: return "some_col"
        if v == 14: return "ba"
        return "grad"
    df["educ"] = df["V241463"].apply(educ_grp)
    # Gender — ANES V241454 is sex (verify)
    # Per codebook: V241454 is restricted day-of-birth; V241551 maybe gender; for v1 use a simple PUBLIC search
    # Fall back: assume gender ≈ binary self-id, look for it in next iteration; for smoke, skip gender pooling
    df["gender"] = "unknown"  # placeholder; refine in v2 of this prep
    # Region: V241022 is "registration state matches sample state". We need actual state.
    # PUF often masks state; for smoke skip region pooling.
    df["region"] = "unknown"

    # ---- Outcome ----
    if outcome == "vote":
        # V242096x: 1=Harris, 2=Trump (binarize Harris vs Trump, drop other)
        df = df[df["V242096x"].isin([1, 2])].copy()
        df["y"] = (df["V242096x"] == 1).astype(int)
    elif outcome == "israel":
        # V241404 humanitarian aid Palestinians (placeholder; real Israel-aid V-code may differ)
        df = df[df["V241404"] > 0].copy()
        df["y_raw"] = df["V241404"]
        df["y"] = (df["y_raw"] - df["y_raw"].mean()) / df["y_raw"].std()
    else:
        # other issues — placeholder; resolve per-item at impl time
        return None

    # ---- Filter to complete cases on demographics ----
    needed = ["age", "cohort", "race", "educ"]
    df_clean = df.dropna(subset=needed).copy()

    # ---- Build Stan data ----
    race_levels = sorted(df_clean["race"].unique())
    educ_levels = sorted(df_clean["educ"].unique())
    cohort_levels = [c for c in COHORT_LEVELS if c in df_clean["cohort"].values]
    if len(cohort_levels) < 2:
        cohort_levels = sorted(df_clean["cohort"].unique())
    gender_levels = sorted(df_clean["gender"].unique())
    region_levels = sorted(df_clean["region"].unique())

    race_idx = pd.Categorical(df_clean["race"], categories=race_levels).codes + 1
    educ_idx = pd.Categorical(df_clean["educ"], categories=educ_levels).codes + 1
    cohort_idx = pd.Categorical(df_clean["cohort"], categories=cohort_levels).codes + 1
    gender_idx = pd.Categorical(df_clean["gender"], categories=gender_levels).codes + 1
    region_idx = pd.Categorical(df_clean["region"], categories=region_levels).codes + 1

    # Fundamentals: smoke build uses just continuous age as a placeholder for econ/2020-recall
    # (proper fundamentals join in v2)
    X_fund = np.column_stack([
        (df_clean["age"].values - df_clean["age"].mean()) / df_clean["age"].std(),
    ])

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
        "y": df_clean["y"].astype(int).tolist() if outcome == "vote" else df_clean["y"].astype(float).tolist(),
        "weight": np.ones(len(df_clean)).tolist(),
    }
    meta = {
        "substrate": "ANES",
        "outcome": outcome,
        "n0_raw": n0,
        "n_used": len(df_clean),
        "race_levels": race_levels,
        "educ_levels": educ_levels,
        "cohort_levels": cohort_levels,
        "gender_levels": gender_levels,
        "region_levels": region_levels,
        "fundamentals_note": "v1 smoke: age z-score only; econ/2020-recall in v2",
    }
    return data, meta


def ces_load_and_prep(outcome="vote"):
    """Load CES 2024 and produce Stan-ready dict.

    CES columns are human-readable: birthyr, gender4, race, hispanic,
    educ, region, inputstate, faminc_new, presvote24post, etc.
    """
    p = RAW / "ces_2024" / "CCES24_Common_OUTPUT_vv_topost_final.csv"
    df = pd.read_csv(p, low_memory=False)
    n0 = len(df)

    # Cohort from birth year (exact, no top-coding issue)
    df["cohort"] = df["birthyr"].apply(birthyr_to_cohort)
    df["age"] = 2024 - df["birthyr"]

    # Race (1=White, 2=Black, 3=Hispanic, 4=Asian, 5=NAt, 6=Mid East, 7=Mixed, 8=Other)
    race_map = {1: "white", 2: "black", 3: "hispanic", 4: "asian",
                5: "nhpi", 6: "other", 7: "other", 8: "other"}
    df["race"] = df["race"].map(race_map)

    # Education (CES: 1=No HS, 2=HS, 3=Some Col, 4=2yr, 5=4yr BA, 6=Postgrad)
    educ_map = {1: "lt_hs", 2: "hs", 3: "some_col", 4: "some_col", 5: "ba", 6: "grad"}
    df["educ"] = df["educ"].map(educ_map)

    # Gender (1=Man, 2=Woman, 3=NB, 4=Other)
    gender_map = {1: "man", 2: "woman", 3: "nb", 4: "other"}
    df["gender"] = df["gender4"].map(gender_map)

    # Region (1=NE, 2=MW, 3=South, 4=West)
    region_map = {1: "NE", 2: "MW", 3: "South", 4: "West"}
    df["region"] = df["region"].map(region_map)

    if outcome == "vote":
        # presvote24post: 1=Harris, 2=Trump, ...
        if "presvote24post" not in df.columns:
            # Try other CES vote-choice column names
            candidates = [c for c in df.columns if "presvote24" in c.lower() or c.lower() == "voted24"]
            if not candidates:
                raise KeyError(f"CES vote-choice column not found; candidates: {[c for c in df.columns if 'vote' in c.lower() or 'pres' in c.lower()][:10]}")
            df["presvote24post"] = df[candidates[0]]
        df = df[df["presvote24post"].isin([1, 2])].copy()
        df["y"] = (df["presvote24post"] == 1).astype(int)
    elif outcome == "single_payer":
        # CES single-payer / govt insurance item — find in codebook v2
        # For smoke, skip this combo
        return None
    elif outcome == "structural_inequity":
        # CES racial resentment 4-item; find col names v2
        return None
    else:
        return None

    needed = ["age", "cohort", "race", "educ", "gender", "region"]
    df_clean = df.dropna(subset=needed).copy()

    race_levels = sorted(df_clean["race"].unique())
    educ_levels = sorted(df_clean["educ"].unique())
    cohort_levels = [c for c in COHORT_LEVELS if c in df_clean["cohort"].values]
    gender_levels = sorted(df_clean["gender"].unique())
    region_levels = sorted(df_clean["region"].unique())

    race_idx = pd.Categorical(df_clean["race"], categories=race_levels).codes + 1
    educ_idx = pd.Categorical(df_clean["educ"], categories=educ_levels).codes + 1
    cohort_idx = pd.Categorical(df_clean["cohort"], categories=cohort_levels).codes + 1
    gender_idx = pd.Categorical(df_clean["gender"], categories=gender_levels).codes + 1
    region_idx = pd.Categorical(df_clean["region"], categories=region_levels).codes + 1

    X_fund = np.column_stack([
        (df_clean["age"].values - df_clean["age"].mean()) / df_clean["age"].std(),
    ])

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
        "y": df_clean["y"].astype(int).tolist(),
        "weight": (df_clean["commonweight"].fillna(1.0).values).tolist()
                  if "commonweight" in df_clean.columns else np.ones(len(df_clean)).tolist(),
    }
    meta = {
        "substrate": "CES",
        "outcome": outcome,
        "n0_raw": n0,
        "n_used": len(df_clean),
        "race_levels": race_levels,
        "educ_levels": educ_levels,
        "cohort_levels": cohort_levels,
        "gender_levels": gender_levels,
        "region_levels": region_levels,
        "fundamentals_note": "v1 smoke: age z-score only; econ/2020-recall in v2",
    }
    return data, meta


if __name__ == "__main__":
    print("=== Data prep smoke ===\n")

    for name, fn in [("ANES vote", lambda: anes_load_and_prep("vote")),
                     ("CES vote", lambda: ces_load_and_prep("vote"))]:
        print(f"--- {name} ---")
        try:
            result = fn()
            if result is None:
                print("  (not implemented)")
                continue
            data, meta = result
            print(f"  raw N: {meta['n0_raw']}, used N: {meta['n_used']}")
            print(f"  race: {meta['race_levels']}")
            print(f"  educ: {meta['educ_levels']}")
            print(f"  cohort: {meta['cohort_levels']}")
            print(f"  gender: {meta['gender_levels']}")
            print(f"  region: {meta['region_levels']}")
            # Save data dict
            outpath = PROCESSED / f"stan_data_{meta['substrate'].lower()}_{meta['outcome']}.joblib"
            joblib.dump({"data": data, "meta": meta}, outpath)
            print(f"  saved: {outpath}")
        except Exception as e:
            print(f"  ERROR: {type(e).__name__}: {e}")
        print()
