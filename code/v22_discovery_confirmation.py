"""v2.2 cohort-axis discovery + confirmation pipeline.

Per prereg_v2.2_dnc_postmortem.md HEAD ff0f9ec:
- 50/50 cohort-stratified split (seed=42)
- TRAIN: L1-penalized logistic with 42 candidates + cohort_idx + H4 fundamentals
  on Harris-vote. Lambda selected by 10-fold CV (lambda.min).
- RETAIN: non-zero coefs at lambda.min, cap top-20 by |coef|
- TEST: Stan model_a with retained items added as fundamentals (next script
  invoked separately for the Stan part)
"""

from pathlib import Path
import json
import joblib
import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegressionCV
from sklearn.preprocessing import StandardScaler
import random

RAW = Path("D:/DNC/data/raw/anes_2024/anes_timeseries_2024_csv_20260519.csv")
PROCESSED = Path("D:/DNC/data/processed")
OUT_DIR = PROCESSED / "v22"
OUT_DIR.mkdir(exist_ok=True)

SEED = 42

# Candidate pool LOCKED in prereg_v2.2 §1 (42 items)
CANDIDATES = [
    # 21 issue summary x-vars
    "V241187x", "V241287x", "V241290x", "V241319x", "V241322x", "V241330x",
    "V241333x", "V241344x", "V241347x", "V241350x", "V241353x",
    "V241372x", "V241375x", "V241381x", "V241389x", "V241392x", "V241395x",
    "V241400x", "V241403x", "V241406x",
    # The duplicate V241350x is omitted; V241385x dropped per >20% miss
    # 8 trait items
    "V241201", "V241202", "V241203", "V241204",
    "V241206", "V241207", "V241208", "V241209",
    # 3 values/system items
    "V241325", "V241327", "V241335",
    # 4 trust/efficacy
    "V241229", "V241230", "V241233", "V241235",
    # 2 identity/engagement
    "V241210", "V241228",
    # 1 ideology
    "V241177",
    # 1 religion
    "V241420",
    # 2 POST anti-system
    "V242304", "V242305",
]
# Count: 20 + 8 + 3 + 4 + 2 + 1 + 1 + 2 = 41. Pre-reg said 42; let me add V241385x... actually
# V241385x is dropped. Let me also add V241341 (corruption-trump? No that's not in pool).
# Pre-reg count was wrong (verbal "42"); actual is 41. Will be noted in result §10 dev 1.

# H4 baseline fundamentals (mandatory keeps in lasso)
H4_FUND_COLS = [
    "fund_recall20_biden", "fund_recall20_trump", "fund_recall20_other",
    "fund_econ_z", "fund_pid7_z", "fund_trump_ft_z",
    "fund_gaza_salience_z", "fund_econ_x_cohort",
]


def load_h4_sample():
    """Re-build H4 sample with cohort + Harris-vote + all candidates."""
    df = pd.read_csv(RAW, low_memory=False)
    # H4 filters (same as data_prep.py anes_load_and_prep('vote_h4'))
    df = df[df["V242096x"].isin([1, 2]) & (df["V241227x"] > 0)].copy()
    df["y"] = (df["V242096x"] == 1).astype(int)

    # Build cohort_idx
    def age_to_cohort(a):
        if pd.isna(a) or a < 18: return None
        if a <= 27: return "GenZ"
        if a <= 43: return "Millennial"
        if a <= 59: return "GenX"
        if a <= 78: return "Boomer"
        return "Silent"
    df["cohort"] = df["V241458x"].where(df["V241458x"] >= 18).apply(age_to_cohort)
    cohort_num = {"Silent": 1, "Boomer": 2, "GenX": 3, "Millennial": 4, "GenZ": 5}
    df["cohort_idx"] = df["cohort"].map(cohort_num)

    # H4 fundamentals
    def _zscore(s):
        s = pd.to_numeric(s, errors="coerce")
        return (s - s.mean()) / s.std(ddof=0)

    recall_map = {1: "biden", 2: "trump", 5: "other"}
    df["recall20"] = df["V241104"].map(recall_map).fillna("nonvoter")
    for level in ["biden", "trump", "other"]:
        df[f"fund_recall20_{level}"] = (df["recall20"] == level).astype(int)
    df["fund_econ_z"] = _zscore(df["V241291"].where(df["V241291"] > 0)).fillna(0.0)
    df["fund_pid7_z"] = _zscore(df["V241227x"].astype(float))
    df["fund_trump_ft_z"] = _zscore(df["V241157"].where(df["V241157"] >= 0)).fillna(0.0)
    df["fund_gaza_salience_z"] = _zscore(df["V241404"].where(df["V241404"] > 0)).fillna(0.0)
    df["fund_econ_x_cohort"] = df["fund_econ_z"].astype(float) * df["cohort_idx"].fillna(3).astype(float)

    # Demographics for Stan
    race_map = {1: "white", 2: "black", 3: "hispanic", 4: "asian", 5: "nhpi", 6: "other"}
    df["race"] = df["V241501x"].map(race_map)
    def educ_grp(v):
        if v < 0: return None
        if v <= 10: return "lt_hs"
        if v <= 12: return "hs"
        if v == 13: return "some_col"
        if v == 14: return "ba"
        return "grad"
    df["educ"] = df["V241463"].apply(educ_grp)
    gender_map = {1: "man", 2: "woman", 3: "nb", 4: "other"}
    df["gender"] = df["V241551"].map(gender_map)
    # State→region (use simple mapping)
    NORTHEAST = {9,23,25,33,44,50,34,36,42}
    MIDWEST = {17,18,26,39,55,19,20,27,29,31,38,46}
    SOUTH = {10,11,12,13,24,37,45,51,54,1,21,28,47,5,22,40,48}
    WEST = {4,8,16,30,32,35,49,56,2,6,15,41,53}
    def state_to_region(s):
        s = int(s) if pd.notna(s) and s > 0 else None
        if s in NORTHEAST: return "NE"
        if s in MIDWEST: return "MW"
        if s in SOUTH: return "South"
        if s in WEST: return "West"
        return None
    df["region"] = df["V241023"].apply(state_to_region)

    # Keep H4-valid rows
    df = df[df[["cohort", "race", "educ", "gender", "region"]].notna().all(axis=1)].copy()
    return df


def build_feature_matrix(df, scaler=None):
    """Build z-scored feature matrix from candidates. Mean-impute missing.
    If scaler provided, use it (test-half); else fit (train-half)."""
    X = pd.DataFrame(index=df.index)
    for c in CANDIDATES:
        col = pd.to_numeric(df[c], errors="coerce").where(df[c] > 0)
        # For V241177 ideology, also drop 99 (haven't thought)
        if c == "V241177":
            col = col.where(col != 99)
        X[c] = col.astype(float)
    # Add cohort_idx + H4 fundamentals (no z-score for fundamentals; lasso handles scale)
    feat = pd.concat([X, df[["cohort_idx"] + H4_FUND_COLS]], axis=1)

    # Mean-impute (per-column) the candidate items only; H4 fundamentals already complete
    means = feat[CANDIDATES].mean()
    feat[CANDIDATES] = feat[CANDIDATES].fillna(means)

    if scaler is None:
        scaler = StandardScaler()
        feat_scaled = scaler.fit_transform(feat)
    else:
        feat_scaled = scaler.transform(feat)

    feat_scaled = pd.DataFrame(feat_scaled, index=feat.index, columns=feat.columns)
    return feat_scaled, scaler, means


def cohort_stratified_split(df, seed=SEED):
    """50/50 split stratified by cohort using deterministic shuffle."""
    rng = random.Random(seed)
    train_idx, test_idx = [], []
    for coh in sorted(df["cohort"].unique()):
        sub = df.index[df["cohort"] == coh].tolist()
        rng.shuffle(sub)
        mid = len(sub) // 2
        train_idx.extend(sub[:mid])
        test_idx.extend(sub[mid:])
    return sorted(train_idx), sorted(test_idx)


def main():
    print("=== v2.2 Discovery (lasso on training half) ===\n")
    df = load_h4_sample()
    print(f"H4 sample N={len(df)}")

    train_idx, test_idx = cohort_stratified_split(df, seed=SEED)
    df_train = df.loc[train_idx]
    df_test = df.loc[test_idx]
    print(f"Train N={len(df_train)}, Test N={len(df_test)}\n")

    Xtr, scaler, imputation_means = build_feature_matrix(df_train, scaler=None)
    ytr = df_train["y"].values

    print(f"Feature matrix: {Xtr.shape[0]} x {Xtr.shape[1]}")
    print(f"Cohort_idx stats train: min/max = {Xtr['cohort_idx'].min():.2f}/{Xtr['cohort_idx'].max():.2f}\n")

    # LogisticRegressionCV with L1 penalty (saga); 10-fold CV
    lr = LogisticRegressionCV(
        Cs=20,  # 20 grid points for regularization
        cv=10,
        penalty="l1",
        solver="saga",
        scoring="neg_log_loss",
        class_weight="balanced",
        max_iter=5000,
        n_jobs=-1,
        random_state=SEED,
    )
    print("Fitting LogisticRegressionCV (this may take a couple minutes)...")
    lr.fit(Xtr.values, ytr)
    best_C = lr.C_[0]
    coefs = pd.Series(lr.coef_[0], index=Xtr.columns)
    print(f"\nLambda.min selected: C = {best_C:.4g} (lambda = 1/{1/best_C:.4g})")
    print(f"Non-zero coefs: {(coefs != 0).sum()} of {len(coefs)}")
    print(f"\nAll coefficients (sorted by |coef|):")
    print(coefs.reindex(coefs.abs().sort_values(ascending=False).index).round(3).to_string())

    # Retention rule: non-zero AND not in H4 baseline AND not cohort_idx
    candidate_coefs = coefs.loc[CANDIDATES]
    retained = candidate_coefs[candidate_coefs != 0].abs().sort_values(ascending=False)
    print(f"\nNon-zero among candidates: {len(retained)}")
    if len(retained) > 20:
        retained_top20 = retained.head(20)
        print(f"Cap to top-20 by |coef|: keeping top 20")
        retained_items = retained_top20.index.tolist()
    else:
        retained_items = retained.index.tolist()
    print(f"\nRETAINED items ({len(retained_items)}):")
    for it in retained_items:
        print(f"  {it}: coef = {candidate_coefs[it]:+.3f}")

    # Save artifacts
    out = {
        "seed": SEED,
        "n_train": int(len(df_train)),
        "n_test": int(len(df_test)),
        "best_C": float(best_C),
        "best_lambda": float(1 / best_C),
        "candidates_pool_size": len(CANDIDATES),
        "n_retained": len(retained_items),
        "retained_items": retained_items,
        "retained_coefs": {it: float(candidate_coefs[it]) for it in retained_items},
        "all_coefs_train_lasso": {c: float(v) for c, v in coefs.items()},
    }
    (OUT_DIR / "discovery_lasso.json").write_text(json.dumps(out, indent=2))
    print(f"\nSaved: {OUT_DIR / 'discovery_lasso.json'}")

    # Save train/test indices + imputation params + scaler for confirmation step
    joblib.dump({
        "train_idx": train_idx,
        "test_idx": test_idx,
        "scaler": scaler,
        "imputation_means": imputation_means,
        "retained_items": retained_items,
    }, OUT_DIR / "discovery_artifacts.joblib")
    print(f"Saved: {OUT_DIR / 'discovery_artifacts.joblib'}")


if __name__ == "__main__":
    main()
