"""v2.8 — External alt-right exposure indicators.

Per prereg_v2.8_dnc_postmortem.md HEAD 10be274.

Pipeline:
  1. Google Trends (weekly time-series + state cross-section) for 5 LOCKED terms
  2. Wikipedia monthly pageviews for 5 LOCKED articles
  3. X API user-lookups for 12 LOCKED accounts (7 alt-right + 5 MAGA mainstream)
  4. State Trump 2020 vs 2024 swing — load from publicly-known returns
  5. H33 — 2024 vs 2020 search-interest amplification
  6. H34 — state Spearman correlation Google Trends × Trump swing
  7. H35 — X cluster size snapshot
"""

import os
import json
import time
import urllib.request
import urllib.parse
from pathlib import Path
import pandas as pd
import numpy as np

OUT_DIR = Path("D:/DNC/data/processed/v28")
OUT_DIR.mkdir(exist_ok=True)

# LOCKED per pre-reg §1.1
GTRENDS_TERMS = ["Groyper", "Nick Fuentes", "Rumble", "alt right", "America First"]

# LOCKED per pre-reg §1.2
WIKI_ARTICLES = ["Nick_Fuentes", "Groyper", "Rumble_(website)", "Alt-right", "America_First_Foundation"]

# LOCKED per pre-reg §2 (12 accounts)
X_ACCOUNTS = {
    "alt_right": ["NickJFuentes", "ashleystclair1", "Cernovich", "JackPosobiec",
                  "realStewPeters", "LauraLoomer", "DC_Draino"],
    "maga_mainstream": ["charliekirk11", "TimRunsHisMouth", "benshapiro",
                        "TuckerCarlson", "LibsOfTikTok"],
}

# 2020 + 2024 state Trump margin (2-party) from official returns
# Source: Cook Political Report / AP / FEC consolidated; manually entered for repro
# Format: state_abbr -> (trump_2020_pct, harris/biden_2020_pct, trump_2024_pct, harris_2024_pct)
# Two-party margin = trump - dem in pp (positive = Trump win margin, negative = Dem win margin)
STATE_RESULTS = {
    # 2020 from FEC; 2024 from official certified returns (approx Nov-Dec 2024)
    "AL": (62.0, 36.6, 65.0, 34.2),
    "AK": (52.8, 42.8, 54.5, 41.4),
    "AZ": (49.1, 49.4, 52.2, 46.7),
    "AR": (62.4, 34.8, 64.2, 33.4),
    "CA": (34.3, 63.5, 38.3, 58.5),
    "CO": (41.9, 55.4, 43.3, 54.2),
    "CT": (39.2, 59.3, 42.0, 56.4),
    "DE": (39.8, 58.8, 42.2, 56.6),
    "FL": (51.2, 47.9, 56.1, 43.0),
    "GA": (49.2, 49.5, 50.7, 48.5),
    "HI": (34.3, 63.7, 37.5, 60.6),
    "ID": (63.8, 33.1, 66.9, 30.4),
    "IL": (40.6, 57.5, 43.5, 54.4),
    "IN": (57.0, 41.0, 58.6, 39.6),
    "IA": (53.1, 44.9, 55.7, 42.7),
    "KS": (56.2, 41.6, 57.2, 41.0),
    "KY": (62.1, 36.2, 64.6, 33.9),
    "LA": (58.5, 39.9, 60.0, 38.2),
    "ME": (44.0, 53.1, 45.5, 51.9),
    "MD": (32.2, 65.4, 34.4, 62.7),
    "MA": (32.1, 65.6, 36.5, 61.2),
    "MI": (47.8, 50.6, 49.7, 48.3),
    "MN": (45.3, 52.4, 46.7, 50.9),
    "MS": (57.6, 41.1, 61.0, 37.6),
    "MO": (56.8, 41.4, 58.4, 40.1),
    "MT": (56.9, 40.5, 58.4, 38.5),
    "NE": (58.2, 39.2, 59.6, 38.9),
    "NV": (47.7, 50.1, 50.6, 47.5),
    "NH": (45.4, 52.7, 48.3, 50.6),
    "NJ": (41.4, 57.3, 45.9, 52.0),
    "NM": (43.5, 54.3, 46.0, 51.9),
    "NY": (37.7, 60.9, 43.3, 55.7),
    "NC": (49.9, 48.6, 50.9, 47.7),
    "ND": (65.1, 31.8, 67.1, 30.8),
    "OH": (53.3, 45.2, 55.2, 43.9),
    "OK": (65.4, 32.3, 66.2, 31.9),
    "OR": (40.4, 56.5, 41.5, 55.0),
    "PA": (48.8, 50.0, 50.4, 48.7),
    "RI": (38.6, 59.4, 41.7, 55.6),
    "SC": (55.1, 43.4, 58.2, 40.4),
    "SD": (61.8, 35.6, 63.4, 34.2),
    "TN": (60.7, 37.4, 64.2, 34.5),
    "TX": (52.1, 46.5, 56.2, 42.5),
    "UT": (58.1, 37.6, 59.4, 37.5),
    "VT": (30.7, 66.1, 32.4, 64.3),
    "VA": (44.0, 54.1, 46.1, 51.8),
    "WA": (38.8, 58.0, 38.9, 57.6),
    "WV": (68.6, 29.7, 70.0, 28.1),
    "WI": (48.8, 49.5, 49.6, 48.8),
    "WY": (69.9, 26.6, 72.3, 25.7),
    "DC": (5.4, 92.1, 6.6, 90.3),
}


def gtrends_pull():
    """Pull weekly Google Trends + state-level for 5 LOCKED terms."""
    # Monkey-patch urllib3 Retry incompat (pytrends uses deprecated method_whitelist)
    import urllib3.util.retry as _r
    if not getattr(_r.Retry, "_dnc_patched", False):
        _orig_init = _r.Retry.__init__
        def _patched(self, *args, **kwargs):
            if "method_whitelist" in kwargs:
                kwargs["allowed_methods"] = kwargs.pop("method_whitelist")
            return _orig_init(self, *args, **kwargs)
        _r.Retry.__init__ = _patched
        _r.Retry._dnc_patched = True
    from pytrends.request import TrendReq
    print(f"\n=== H33/H34: Google Trends pull (5 terms, 2020-2024) ===")
    pytrends = TrendReq(hl="en-US", tz=360, retries=2, backoff_factor=0.5)

    # Weekly time-series for each term (max 5 per request; 5 terms fits)
    weekly_results = {}
    state_results = {}
    for term in GTRENDS_TERMS:
        print(f"  Pulling: {term!r}")
        try:
            pytrends.build_payload([term], timeframe="2020-01-01 2024-12-31",
                                    geo="US", gprop="")
            tdf = pytrends.interest_over_time()
            if not tdf.empty:
                tdf = tdf.drop(columns=["isPartial"], errors="ignore")
                weekly_results[term] = tdf[term]
        except Exception as e:
            print(f"    weekly err: {e}")
            weekly_results[term] = None
        # State-level (use Sep-Nov 2024 only for tighter time window)
        try:
            pytrends.build_payload([term], timeframe="2024-09-01 2024-11-30",
                                    geo="US", gprop="")
            sdf = pytrends.interest_by_region(resolution="REGION",
                                              inc_low_vol=True, inc_geo_code=True)
            if not sdf.empty:
                state_results[term] = sdf[term]
        except Exception as e:
            print(f"    state err: {e}")
            state_results[term] = None
        time.sleep(1.5)  # rate-limit gentleness

    # Aggregate
    if weekly_results:
        weekly_df = pd.DataFrame({k: v for k, v in weekly_results.items() if v is not None})
        weekly_df.to_csv(OUT_DIR / "google_trends_weekly.csv")
        print(f"  saved weekly: {weekly_df.shape}")

    if state_results:
        state_df = pd.DataFrame({k: v for k, v in state_results.items() if v is not None})
        state_df.to_csv(OUT_DIR / "google_trends_state.csv")
        print(f"  saved state: {state_df.shape}")

    return weekly_df, state_df


def wiki_pageviews_pull():
    """Pull monthly Wikipedia pageviews for 5 LOCKED articles."""
    print(f"\n=== H33: Wikipedia pageviews (5 articles, 2020-2024 monthly) ===")
    headers = {"User-Agent": "DNC-Autopsy/2.8 (research; mr.nathanhumphrey@gmail.com)"}
    out = {}
    for article in WIKI_ARTICLES:
        url = (f"https://wikimedia.org/api/rest_v1/metrics/pageviews/per-article/"
               f"en.wikipedia/all-access/all-agents/{urllib.parse.quote(article)}/"
               f"monthly/2020010100/2024123100")
        try:
            req = urllib.request.Request(url, headers=headers)
            with urllib.request.urlopen(req, timeout=30) as r:
                data = json.loads(r.read().decode())
            items = data.get("items", [])
            df = pd.DataFrame(items)
            if not df.empty:
                df["month"] = pd.to_datetime(df["timestamp"].str[:6], format="%Y%m")
                out[article] = df.set_index("month")["views"]
                print(f"  {article}: {len(df)} months, total views {df['views'].sum():,}")
        except Exception as e:
            print(f"  {article}: ERR {e}")
            out[article] = None
        time.sleep(0.5)
    wdf = pd.DataFrame({k: v for k, v in out.items() if v is not None})
    wdf.to_csv(OUT_DIR / "wikipedia_pageviews.csv")
    print(f"  saved: {wdf.shape}")
    return wdf


def x_lookup():
    """Pull current public_metrics for 12 LOCKED X accounts via DeepDive env's bearer token."""
    print(f"\n=== H35: X API user lookups (12 accounts) ===")
    # Load .env from DeepDive
    env_path = Path("C:/DeepDive/.env")
    token = None
    if env_path.exists():
        for line in env_path.read_text().splitlines():
            if line.startswith("TWITTER_BEARER_TOKEN="):
                token = line.split("=", 1)[1].strip().strip('"').strip("'")
                break
    if not token:
        print("  TWITTER_BEARER_TOKEN not found in C:/DeepDive/.env — skipping X lookups")
        return None
    print(f"  token loaded (length={len(token)})")

    rows = []
    all_accounts = []
    for cluster, accounts in X_ACCOUNTS.items():
        for a in accounts:
            all_accounts.append((cluster, a))

    base = "https://api.x.com/2/users/by/username/{}?user.fields=public_metrics,verified,created_at"
    for cluster, username in all_accounts:
        url = base.format(urllib.parse.quote(username))
        try:
            req = urllib.request.Request(url, headers={"Authorization": f"Bearer {token}"})
            with urllib.request.urlopen(req, timeout=20) as r:
                data = json.loads(r.read().decode())
            if "data" in data:
                u = data["data"]
                pm = u.get("public_metrics", {})
                rows.append({
                    "cluster": cluster,
                    "username": username,
                    "id": u.get("id"),
                    "verified": u.get("verified", False),
                    "created_at": u.get("created_at"),
                    "followers_count": pm.get("followers_count", None),
                    "following_count": pm.get("following_count", None),
                    "tweet_count": pm.get("tweet_count", None),
                    "listed_count": pm.get("listed_count", None),
                    "status": "ok",
                })
                print(f"  {cluster:15s} @{username}: {pm.get('followers_count', '?'):>12,} followers")
            else:
                rows.append({"cluster": cluster, "username": username, "status": "missing",
                             "followers_count": None})
                print(f"  {cluster:15s} @{username}: MISSING ({data})")
        except urllib.error.HTTPError as e:
            err_body = e.read().decode(errors="replace")[:200]
            rows.append({"cluster": cluster, "username": username,
                         "status": f"http_{e.code}", "followers_count": None})
            print(f"  {cluster:15s} @{username}: HTTP {e.code}: {err_body}")
        except Exception as e:
            rows.append({"cluster": cluster, "username": username,
                         "status": f"err:{type(e).__name__}", "followers_count": None})
            print(f"  {cluster:15s} @{username}: ERR {e}")
        time.sleep(1.0)  # rate-limit gentleness

    df = pd.DataFrame(rows)
    df.to_csv(OUT_DIR / "x_follower_counts.csv", index=False)
    print(f"\n  saved: {df.shape}")
    return df


def state_swing():
    """Compute state-level Trump 2020→2024 swing (margin pp)."""
    print(f"\n=== State Trump margin swing 2020→2024 ===")
    rows = []
    for st, (t20, d20, t24, d24) in STATE_RESULTS.items():
        margin_20 = t20 - d20  # positive = Trump 2020 win
        margin_24 = t24 - d24  # positive = Trump 2024 win
        swing = margin_24 - margin_20
        rows.append({"state": st, "trump_2020_pct": t20, "dem_2020_pct": d20,
                     "trump_2024_pct": t24, "dem_2024_pct": d24,
                     "margin_2020": margin_20, "margin_2024": margin_24,
                     "swing_pp_2020to2024": swing})
    df = pd.DataFrame(rows).sort_values("swing_pp_2020to2024", ascending=False)
    df.to_csv(OUT_DIR / "state_trump_swing.csv", index=False)
    print(f"  saved 51 states (incl DC)")
    print(f"  swing range: {df['swing_pp_2020to2024'].min():.1f}pp to "
          f"{df['swing_pp_2020to2024'].max():.1f}pp")
    return df


def main():
    print("===== v2.8 EXTERNAL ALT-RIGHT INDICATORS =====")
    swing_df = state_swing()

    # Wikipedia first (no rate-limit issues)
    wiki_df = wiki_pageviews_pull()

    # X cluster
    x_df = x_lookup()

    # Google Trends last (most rate-limit-prone)
    try:
        weekly_df, state_df = gtrends_pull()
    except Exception as e:
        print(f"\n  GOOGLE TRENDS FAILED: {e}")
        weekly_df = pd.DataFrame()
        state_df = pd.DataFrame()

    # === Aggregate analyses ===
    print("\n" + "="*60)
    print("=== H33: 2024 vs 2020 search-interest amplification ===")
    print("="*60)
    if not weekly_df.empty:
        weekly_df.index = pd.to_datetime(weekly_df.index)
        for term in GTRENDS_TERMS:
            if term not in weekly_df.columns: continue
            t = weekly_df[term].dropna()
            preel_20 = t[(t.index >= "2020-07-01") & (t.index <= "2020-10-31")].mean()
            preel_24 = t[(t.index >= "2024-07-01") & (t.index <= "2024-10-31")].mean()
            baseline_20 = t[(t.index >= "2020-01-01") & (t.index <= "2020-06-30")].mean()
            baseline_24 = t[(t.index >= "2024-01-01") & (t.index <= "2024-06-30")].mean()
            spike_20 = preel_20 - baseline_20
            spike_24 = preel_24 - baseline_24
            ratio = (spike_24 / spike_20) if abs(spike_20) > 0.01 else float("nan")
            print(f"  {term:20s}: preel_24={preel_24:5.1f} baseline_24={baseline_24:5.1f} spike={spike_24:+5.1f} | "
                  f"preel_20={preel_20:5.1f} baseline_20={baseline_20:5.1f} spike={spike_20:+5.1f} | ratio={ratio:.2f}")
    else:
        print("  (Google Trends data unavailable)")

    print("\n" + "="*60)
    print("=== H34: State Spearman corr Google Trends × Trump 2020→2024 swing ===")
    print("="*60)
    if not state_df.empty:
        # Geometric mean across terms per state
        state_df_log = np.log(state_df.clip(lower=1))
        gmean = np.exp(state_df_log.mean(axis=1))
        gmean.name = "gtrends_geomean"
        sm = pd.DataFrame({"gtrends_geomean": gmean})
        # Map state names (Google returns full state names) to abbreviations
        STATE_NAME_TO_ABBR = {
            "Alabama": "AL", "Alaska": "AK", "Arizona": "AZ", "Arkansas": "AR",
            "California": "CA", "Colorado": "CO", "Connecticut": "CT", "Delaware": "DE",
            "District of Columbia": "DC", "Florida": "FL", "Georgia": "GA", "Hawaii": "HI",
            "Idaho": "ID", "Illinois": "IL", "Indiana": "IN", "Iowa": "IA", "Kansas": "KS",
            "Kentucky": "KY", "Louisiana": "LA", "Maine": "ME", "Maryland": "MD",
            "Massachusetts": "MA", "Michigan": "MI", "Minnesota": "MN", "Mississippi": "MS",
            "Missouri": "MO", "Montana": "MT", "Nebraska": "NE", "Nevada": "NV",
            "New Hampshire": "NH", "New Jersey": "NJ", "New Mexico": "NM", "New York": "NY",
            "North Carolina": "NC", "North Dakota": "ND", "Ohio": "OH", "Oklahoma": "OK",
            "Oregon": "OR", "Pennsylvania": "PA", "Rhode Island": "RI", "South Carolina": "SC",
            "South Dakota": "SD", "Tennessee": "TN", "Texas": "TX", "Utah": "UT",
            "Vermont": "VT", "Virginia": "VA", "Washington": "WA", "West Virginia": "WV",
            "Wisconsin": "WI", "Wyoming": "WY",
        }
        sm["state"] = sm.index.map(STATE_NAME_TO_ABBR)
        sm = sm.dropna(subset=["state"])
        merged = sm.merge(swing_df[["state", "swing_pp_2020to2024"]], on="state")
        rho = merged["gtrends_geomean"].corr(merged["swing_pp_2020to2024"], method="spearman")
        print(f"  Spearman ρ = {rho:.3f}")
        if rho >= 0.4:
            h34 = "CONFIRMED"
        elif rho >= 0.2:
            h34 = "PARTIAL"
        elif rho > -0.2:
            h34 = "NULL"
        else:
            h34 = "REVERSED"
        print(f"  H34 VERDICT: {h34}")
        merged.to_csv(OUT_DIR / "state_correlation.csv", index=False)
    else:
        print("  (Google Trends state data unavailable)")

    print("\n" + "="*60)
    print("=== H35: X cluster size snapshot ===")
    print("="*60)
    if x_df is not None and len(x_df):
        okx = x_df[x_df["status"] == "ok"]
        for cluster, sub in okx.groupby("cluster"):
            total = sub["followers_count"].sum()
            print(f"  Cluster {cluster}: N_accounts={len(sub)}, total_followers={total:,.0f}")
            print(sub[["username", "followers_count", "tweet_count"]].sort_values(
                "followers_count", ascending=False).to_string(index=False))
            print()
        a_total = okx[okx["cluster"] == "alt_right"]["followers_count"].sum()
        b_total = okx[okx["cluster"] == "maga_mainstream"]["followers_count"].sum()
        ratio = a_total / b_total if b_total > 0 else float("nan")
        print(f"  Alt-right cluster total: {a_total:,.0f}")
        print(f"  MAGA mainstream total: {b_total:,.0f}")
        print(f"  A:B ratio = {ratio:.3f}")
        if a_total >= 5_000_000:
            h35 = "HIGH-VISIBILITY"
        elif a_total >= 1_000_000:
            h35 = "MEDIUM"
        else:
            h35 = "NICHE"
        print(f"  H35 VERDICT: {h35}")
    else:
        print("  (X cluster data unavailable)")


if __name__ == "__main__":
    main()
