"""
DNC post-mortem — Pay-structure imputation v2 (transfer-ready feature set).

Replaces v1 (paystructure_imputation.py, commit c4e1cb6) which scored AUC 0.8393
but used predictors NOT available on ANES/CES political-survey respondents
(occupation OCC2010, hours UHRSWORKT, weekly earnings EARNWEEK2).

§12 deviation 2026-05-23: reduce predictor set to features ANES+CES actually
carry (AGE, SEX, RACE, HISPAN, EDUC, REGION, IND_MAJOR). Earnings dropped
because CPS records individual earnings while ANES/CES record banded household
income — the household-vs-individual mismatch makes the cross-substrate transfer
unreliable. Cleaner to drop earnings than kludge a crosswalk.

The §8 gate (AUC &gt;= 0.75) is re-tested on this transfer-ready model. PASS → use
for Model B exposure-pool analysis. FAIL → flag exposure-pool analysis as
weakly identified per pre-reg §8.

Outputs:
  data/processed/paystructure_model_v2_transfer.joblib
  data/processed/paystructure_cv_metrics_v2.json
"""

from pathlib import Path
import json
import re
import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.model_selection import StratifiedKFold, cross_val_score
import joblib

RAW = Path("D:/DNC/data/raw/cps_org_2024")
PROCESSED = Path("D:/DNC/data/processed")
DO_FILE = RAW / "cps_00001.do"
DAT_FILE = RAW / "cps_00001.dat"
SEED = 42
N_JOBS = 8  # user-set worker limit

AUC_GATE_THRESHOLD = 0.75


def parse_do_specs(do_path):
    text = Path(do_path).read_text()
    head = text[: text.find("using")]
    pattern = re.compile(r"^\s+(\w+)\s+(\w+)\s+(\d+)-(\d+)", re.MULTILINE)
    return [(name, int(s) - 1, int(e)) for _, name, s, e in pattern.findall(head)]


def load_cps_org(do_file=DO_FILE, dat_file=DAT_FILE):
    specs = parse_do_specs(do_file)
    names = [n for n, _, _ in specs]
    colspecs = [(s, e) for _, s, e in specs]
    df = pd.read_fwf(dat_file, colspecs=colspecs, names=names, header=None)
    return df


def make_org_subset(df):
    org = df[df["paidhour"] > 0].copy()
    org["paid_hourly"] = (org["paidhour"] == 2).astype(int)
    return org


def build_transfer_features(df):
    """Transfer-ready features available on ANES + CES."""
    out = pd.DataFrame(index=df.index)
    out["age"] = df["age"].astype(float)
    out["sex_male"] = (df["sex"] == 1).astype(int)
    race_map = {100: "white", 200: "black", 300: "aian", 651: "asian", 652: "nhpi"}
    out["race_grp"] = df["race"].map(race_map).fillna("other")
    out["hispan_yn"] = (df["hispan"] > 0).astype(int)
    def educ_grp(v):
        if v < 73: return "lt_hs"
        elif v < 81: return "hs"
        elif v < 111: return "some_col"
        elif v < 124: return "ba"
        else: return "grad"
    out["educ_grp"] = df["educ"].apply(educ_grp)
    def region_grp(v):
        if v in (11, 12): return "NE"
        elif v in (21, 22): return "MW"
        elif v in (31, 32, 33): return "South"
        elif v in (41, 42): return "West"
        return "other"
    out["region"] = df["region"].apply(region_grp)
    # Industry 2-digit major (kept — ANES + CES both have industry)
    out["ind_major"] = (df["ind"] // 100).astype(int).astype(str).str.zfill(2)
    return out


def build_pipeline():
    num_cols = ["age"]
    bin_cols = ["sex_male", "hispan_yn"]
    cat_cols = ["race_grp", "educ_grp", "region", "ind_major"]
    pre = ColumnTransformer([
        ("num", StandardScaler(), num_cols),
        ("bin", "passthrough", bin_cols),
        ("cat", OneHotEncoder(handle_unknown="ignore", sparse_output=False), cat_cols),
    ])
    clf = LogisticRegression(max_iter=2000, C=1.0, solver="lbfgs", random_state=SEED)
    return Pipeline([("pre", pre), ("clf", clf)])


def main():
    print("=== DNC pay-structure imputation v2 (transfer-ready features only) ===\n")
    print(f"Worker limit: n_jobs={N_JOBS}\n")

    print("[1/5] Loading CPS basic-monthly Jan-Dec 2024…")
    df = load_cps_org()
    print(f"  Total records: {len(df)}")

    print("\n[2/5] Filtering to ORG-eligible (PAIDHOUR > 0)…")
    org = make_org_subset(df)
    print(f"  ORG sample size: {len(org)}; Paid hourly: {org['paid_hourly'].sum()} ({org['paid_hourly'].mean():.1%})")

    print("\n[3/5] Engineering transfer-ready features…")
    X = build_transfer_features(org)
    y = org["paid_hourly"].values
    print(f"  Features: {list(X.columns)}")
    print(f"  Categorical cardinalities:")
    for c in ["race_grp", "educ_grp", "region", "ind_major"]:
        print(f"    {c}: {X[c].nunique()}")

    print(f"\n[4/5] 5-fold stratified CV (n_jobs={N_JOBS})…")
    pipe = build_pipeline()
    cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=SEED)
    aucs = cross_val_score(pipe, X, y, cv=cv, scoring="roc_auc", n_jobs=N_JOBS)
    accs = cross_val_score(pipe, X, y, cv=cv, scoring="accuracy", n_jobs=N_JOBS)
    print(f"  Per-fold AUC: {[f'{a:.4f}' for a in aucs]}")
    print(f"  Mean AUC:     {aucs.mean():.4f}  (SD {aucs.std():.4f})")
    print(f"  Mean Acc:     {accs.mean():.4f}")
    print(f"  Pre-reg §8 gate: AUC &gt;= {AUC_GATE_THRESHOLD}")
    pass_flag = aucs.mean() >= AUC_GATE_THRESHOLD
    print(f"  Gate verdict: {'PASS' if pass_flag else 'FAIL (exposure-pool flagged as weakly identified)'}")
    print(f"  Comparison to v1 (full features incl occ+hours+earnings): AUC {aucs.mean():.4f} vs 0.8393")

    print(f"\n[5/5] Fitting on full ORG sample + persisting…")
    pipe.fit(X, y)
    PROCESSED.mkdir(parents=True, exist_ok=True)
    joblib.dump({
        "pipeline": pipe,
        "feature_columns": list(X.columns),
        "training_n": len(org),
        "training_positive_rate": float(org["paid_hourly"].mean()),
        "cv_auc_mean": float(aucs.mean()),
        "cv_auc_sd": float(aucs.std()),
        "cv_acc_mean": float(accs.mean()),
        "auc_gate_threshold": AUC_GATE_THRESHOLD,
        "gate_pass": bool(pass_flag),
        "seed": SEED,
        "transfer_features_only": True,
        "v1_full_features_auc": 0.8393,
    }, PROCESSED / "paystructure_model_v2_transfer.joblib")
    print(f"  Saved: {PROCESSED / 'paystructure_model_v2_transfer.joblib'}")

    metrics = {
        "model_version": "v2_transfer",
        "training_n": len(org),
        "training_positive_rate_hourly": float(org["paid_hourly"].mean()),
        "cv_auc_per_fold": [float(a) for a in aucs],
        "cv_auc_mean": float(aucs.mean()),
        "cv_auc_sd": float(aucs.std()),
        "cv_acc_mean": float(accs.mean()),
        "auc_gate_threshold": AUC_GATE_THRESHOLD,
        "gate_pass": bool(pass_flag),
        "feature_columns": list(X.columns),
        "v1_full_features_auc_comparison": 0.8393,
        "v2_v1_auc_delta": float(aucs.mean() - 0.8393),
    }
    (PROCESSED / "paystructure_cv_metrics_v2.json").write_text(json.dumps(metrics, indent=2))
    print(f"  Saved: {PROCESSED / 'paystructure_cv_metrics_v2.json'}")


if __name__ == "__main__":
    main()
