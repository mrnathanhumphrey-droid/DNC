"""
DNC post-mortem — Pay-structure imputation pipeline (pre-reg §8, locked 45ea69a).

Trains a logistic regression P(paid_hourly | observables) on CPS basic-monthly ORG
respondents Jan-Dec 2024 (n=125,880), to be applied at predict-time to ANES/CES/
AP-VoteCast political-survey respondents who lack a direct hourly-vs-salary item.

Pre-reg gate (§8): if cross-validated AUC < 0.75, flag exposure-pool analysis as
weakly identified.

Output:
  data/processed/paystructure_model_v1.joblib  - trained pipeline (scaler + logit + col defs)
  data/processed/paystructure_cv_metrics.json  - 5-fold CV AUC, accuracy, coefficient summary
"""

from pathlib import Path
import json
import re
import gzip
import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.model_selection import StratifiedKFold, cross_val_score
from sklearn.metrics import roc_auc_score, accuracy_score
import joblib

RAW = Path("D:/DNC/data/raw/cps_org_2024")
PROCESSED = Path("D:/DNC/data/processed")
DO_FILE = RAW / "cps_00001.do"
DAT_FILE = RAW / "cps_00001.dat"
SEED = 42

AUC_GATE_THRESHOLD = 0.75  # pre-reg §8


def parse_do_specs(do_path):
    """Pull (name, start, end) tuples from the IPUMS Stata .do file's infix block."""
    text = Path(do_path).read_text()
    head = text[: text.find("using")]
    pattern = re.compile(r"^\s+(\w+)\s+(\w+)\s+(\d+)-(\d+)", re.MULTILINE)
    return [(name, int(s) - 1, int(e)) for _, name, s, e in pattern.findall(head)]


def load_cps_org(do_file=DO_FILE, dat_file=DAT_FILE):
    specs = parse_do_specs(do_file)
    names = [n for n, _, _ in specs]
    colspecs = [(s, e) for _, s, e in specs]
    df = pd.read_fwf(dat_file, colspecs=colspecs, names=names, header=None)
    df["earnweek2"] = df["earnweek2"] / 100.0
    df["hourwage2"] = df["hourwage2"] / 100.0
    df["wtfinl"] = df["wtfinl"] / 10000.0
    df["hwtfinl"] = df["hwtfinl"] / 10000.0
    return df


def make_org_subset(df):
    """Filter to ORG-eligible respondents (PAIDHOUR > 0)."""
    org = df[df["paidhour"] > 0].copy()
    org["paid_hourly"] = (org["paidhour"] == 2).astype(int)
    return org


def build_features(df):
    """Engineered feature columns matching what political surveys can carry.

    Continuous: age, log_earnweek (capped + log1p), uhrsworkt (NIU 999 → median imputed)
    Binary: sex (M=1)
    Categorical: race_grp (5 levels), hispan_yn, educ_grp, region, occ_major (2-digit), ind_major (2-digit)
    """
    out = pd.DataFrame(index=df.index)
    out["age"] = df["age"].astype(float)
    # NIU 999 / blank handling on hours
    hr = df["uhrsworkt"].replace({999: np.nan, 997: np.nan})
    hr_med = hr.median()
    out["uhrsworkt"] = hr.fillna(hr_med)
    # Earnings: 9999.99 is topcode; log1p
    ew = df["earnweek2"].clip(lower=0).fillna(0)
    out["log_earnweek"] = np.log1p(ew)
    out["sex_male"] = (df["sex"] == 1).astype(int)
    # Race: 100=White, 200=Black, 300=AIAN, 651=Asian, 652=NHPI, others=mixed
    race_map = {100: "white", 200: "black", 300: "aian", 651: "asian", 652: "nhpi"}
    out["race_grp"] = df["race"].map(race_map).fillna("other")
    out["hispan_yn"] = (df["hispan"] > 0).astype(int)
    # Education: IPUMS EDUC codes; group to <HS / HS / SomeCol / BA / Grad
    def educ_grp(v):
        if v < 73:
            return "lt_hs"
        elif v < 81:
            return "hs"
        elif v < 111:
            return "some_col"
        elif v < 124:
            return "ba"
        else:
            return "grad"
    out["educ_grp"] = df["educ"].apply(educ_grp)
    # Region: 11/12 NE, 21/22 MW, 31/32/33 South, 41/42 West
    def region_grp(v):
        if v in (11, 12):
            return "NE"
        elif v in (21, 22):
            return "MW"
        elif v in (31, 32, 33):
            return "South"
        elif v in (41, 42):
            return "West"
        return "other"
    out["region"] = df["region"].apply(region_grp)
    # Occupation: 4-digit OCC2010 → 2-digit major group (first 2 digits, or 0 if NIU)
    out["occ_major"] = (df["occ2010"] // 100).astype(int).astype(str).str.zfill(2)
    # Industry: similar to OCC, take first 2 digits of IND (NAICS-like)
    out["ind_major"] = (df["ind"] // 100).astype(int).astype(str).str.zfill(2)
    return out


def build_pipeline():
    """Logistic regression pipeline per pre-reg §8."""
    num_cols = ["age", "uhrsworkt", "log_earnweek"]
    bin_cols = ["sex_male", "hispan_yn"]
    cat_cols = ["race_grp", "educ_grp", "region", "occ_major", "ind_major"]
    pre = ColumnTransformer([
        ("num", StandardScaler(), num_cols),
        ("bin", "passthrough", bin_cols),
        ("cat", OneHotEncoder(handle_unknown="ignore", sparse_output=False), cat_cols),
    ])
    clf = LogisticRegression(max_iter=2000, C=1.0, solver="lbfgs", random_state=SEED)
    return Pipeline([("pre", pre), ("clf", clf)])


def main():
    print("=== DNC pay-structure imputation pipeline (pre-reg §8) ===\n")

    print("[1/5] Loading CPS basic-monthly Jan-Dec 2024…")
    df = load_cps_org()
    print(f"  Total person-month records: {len(df)}")

    print("\n[2/5] Filtering to ORG-eligible (PAIDHOUR > 0)…")
    org = make_org_subset(df)
    print(f"  ORG sample size: {len(org)}")
    print(f"  Paid hourly: {org['paid_hourly'].sum()} ({org['paid_hourly'].mean():.1%})")

    print("\n[3/5] Engineering features…")
    X = build_features(org)
    y = org["paid_hourly"].values
    print(f"  Feature columns: {list(X.columns)}")
    print(f"  Categorical cardinalities:")
    for c in ["race_grp", "educ_grp", "region", "occ_major", "ind_major"]:
        print(f"    {c}: {X[c].nunique()}")

    print("\n[4/5] 5-fold stratified CV (logistic regression)…")
    pipe = build_pipeline()
    cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=SEED)
    aucs = cross_val_score(pipe, X, y, cv=cv, scoring="roc_auc", n_jobs=-1)
    accs = cross_val_score(pipe, X, y, cv=cv, scoring="accuracy", n_jobs=-1)
    print(f"  Per-fold AUC: {[f'{a:.4f}' for a in aucs]}")
    print(f"  Mean AUC:     {aucs.mean():.4f}  (SD {aucs.std():.4f})")
    print(f"  Mean Acc:     {accs.mean():.4f}")
    print(f"  Pre-reg §8 gate: AUC >= {AUC_GATE_THRESHOLD}")
    gate = "PASS" if aucs.mean() >= AUC_GATE_THRESHOLD else "FAIL (exposure-pool analysis flagged as weakly identified)"
    print(f"  Gate verdict: {gate}")

    print("\n[5/5] Fitting on full ORG sample + persisting…")
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
        "gate_pass": bool(aucs.mean() >= AUC_GATE_THRESHOLD),
        "seed": SEED,
    }, PROCESSED / "paystructure_model_v1.joblib")
    print(f"  Saved: {PROCESSED / 'paystructure_model_v1.joblib'}")

    metrics = {
        "training_n": len(org),
        "training_positive_rate_hourly": float(org["paid_hourly"].mean()),
        "cv_auc_per_fold": [float(a) for a in aucs],
        "cv_auc_mean": float(aucs.mean()),
        "cv_auc_sd": float(aucs.std()),
        "cv_acc_mean": float(accs.mean()),
        "auc_gate_threshold": AUC_GATE_THRESHOLD,
        "gate_pass": bool(aucs.mean() >= AUC_GATE_THRESHOLD),
        "feature_columns": list(X.columns),
    }
    metrics_path = PROCESSED / "paystructure_cv_metrics.json"
    metrics_path.write_text(json.dumps(metrics, indent=2))
    print(f"  Saved: {metrics_path}")


if __name__ == "__main__":
    main()
