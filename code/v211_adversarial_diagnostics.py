"""Adversarial diagnostics for v2.11:
1. Crack the 'leftist Biden voters retain more' raw pattern (5 critiques)
2. Test user's NEW hypotheses: Boomer-disaffected + rich-disaffected skip
"""
import sys; sys.path.insert(0, 'code')
from v211_leftist_test import build_leftist_predictors, LEFT_ITEMS
import pandas as pd
import numpy as np

df_full = pd.read_csv('D:/DNC/data/raw/ces_2024/CCES24_Common_OUTPUT_vv_topost_final.csv', low_memory=False)


def by_cohort(b):
    if pd.isna(b): return None
    if b >= 1997: return 'GenZ'
    if b >= 1989: return 'MillYoung'
    if b >= 1981: return 'MillOld'
    if b >= 1965: return 'GenX'
    if b >= 1946: return 'Boomer'
    return 'Silent'


def outcome4(row):
    ts = row['TS_g2024']; cc = row['CC24_410']
    if pd.isna(ts): return None
    if ts == 7: return 'skipped'
    if ts in [1,2,3,4,5,6]:
        if pd.isna(cc): return 'voted_unk'
        if cc == 1: return 'retained_harris'
        if cc == 2: return 'flipped_trump'
        if cc in [3,4,5,8]: return 'flipped_3rd'
        return 'voted_unk'
    return None


# Full Biden universe with 4-way outcome
mask = (df_full['vvweight_post']>0) & (df_full['presvote20post']==1) & df_full['birthyr'].notna() & df_full['TS_g2024'].notna()
biden = df_full[mask].copy()
biden['outcome4'] = biden.apply(outcome4, axis=1)
biden = biden[biden['outcome4'].isin(['skipped','retained_harris','flipped_trump','flipped_3rd'])].copy()
biden = build_leftist_predictors(biden)
biden['cohort6'] = biden['birthyr'].apply(by_cohort)
biden['cq'] = pd.qcut(biden['left_composite_z'], 5, labels=False, duplicates='drop')
biden['pid7'] = pd.to_numeric(biden['pid7'], errors='coerce')
biden['faminc'] = pd.to_numeric(biden['faminc_new'], errors='coerce')
print(f"Biden full universe N={len(biden)}")

# CRITIQUE 1: Outcome by composite quintile (4-way)
print("\n" + "="*70)
print("C1: 3rd-party defection as leftist exit (4-way outcome by composite quintile)")
print("="*70)
ct = pd.crosstab(biden['cq'], biden['outcome4'], normalize='index') * 100
print(ct.round(2).to_string())
print(f"\nN per quintile:")
print(biden['cq'].value_counts().sort_index().to_string())

# Combined leftist-exit
print(f"\nCombined leftist-exit (skip + flip_3rd):")
for q in sorted(biden['cq'].dropna().unique()):
    sub = biden[biden['cq']==q]
    sk = (sub['outcome4']=='skipped').mean()*100
    th = (sub['outcome4']=='flipped_3rd').mean()*100
    tr = (sub['outcome4']=='flipped_trump').mean()*100
    re = (sub['outcome4']=='retained_harris').mean()*100
    print(f"  Q{int(q)} (N={len(sub)}): retain={re:.2f}% skip={sk:.2f}% flip_3rd={th:.2f}% flip_trump={tr:.2f}% | leftist-exit={sk+th:.2f}%")

# RESTRICT to skip|retain for stratified analyses
restricted = biden[biden['outcome4'].isin(['skipped','retained_harris'])].copy()
restricted['skipped'] = (restricted['outcome4']=='skipped').astype(int)

# CRITIQUE 2: Within-pid7
print("\n" + "="*70)
print("C2: Within-pid7 stratified")
print("="*70)
for pid in [1, 2, 3, 4, 5, 6, 7]:
    sub = restricted[restricted['pid7']==pid]
    if len(sub) < 100: continue
    parts = []
    for q in sorted(restricted['cq'].dropna().unique()):
        ssub = sub[sub['cq']==q]
        if len(ssub) > 0:
            parts.append(f"Q{int(q)}={ssub['skipped'].mean()*100:.1f}%(n={len(ssub)})")
    print(f"  pid7={pid} (N={len(sub)}): {' | '.join(parts)}")

# CRITIQUE 3: Within-cohort
print("\n" + "="*70)
print("C3: Within-cohort stratified")
print("="*70)
for c in ['Silent','Boomer','GenX','MillOld','MillYoung','GenZ']:
    sub = restricted[restricted['cohort6']==c]
    if len(sub) < 50: continue
    parts = []
    for q in sorted(restricted['cq'].dropna().unique()):
        ssub = sub[sub['cq']==q]
        if len(ssub) > 0:
            parts.append(f"Q{int(q)}={ssub['skipped'].mean()*100:.1f}%(n={len(ssub)})")
    print(f"  {c} (N={len(sub)}): {' | '.join(parts)}")

# CRITIQUE 4: NaN imputation
print("\n" + "="*70)
print("C4: NaN imputation — does low composite = non-response?")
print("="*70)
recoded_cols = [f"left_{name}" for _, (name, _) in LEFT_ITEMS.items()]
biden['n_answered'] = biden[recoded_cols].notna().sum(axis=1)
print(f"\nN_items_answered distribution:")
print(biden['n_answered'].value_counts().sort_index().to_string())

# CRITIQUE 5: Item-level univariate
print("\n" + "="*70)
print("C5: Item-level skip rate (left=1 vs non-left=0)")
print("="*70)
for vcode, (name, direction) in LEFT_ITEMS.items():
    if f"left_{name}" not in restricted.columns: continue
    skip_left = restricted[restricted[f"left_{name}"]==1]['skipped'].mean()*100
    skip_right = restricted[restricted[f"left_{name}"]==0]['skipped'].mean()*100
    n_left = (restricted[f"left_{name}"]==1).sum()
    n_right = (restricted[f"left_{name}"]==0).sum()
    diff = skip_left - skip_right
    print(f"  {vcode} ({name}, left=={direction}): left N={n_left} sk%={skip_left:.2f} | nonleft N={n_right} sk%={skip_right:.2f} | diff={diff:+.2f}pp")

# USER HYPOTHESIS 1: Boomer-rich disaffection
print("\n" + "="*70)
print("USER H: BOOMER + HIGH-INCOME disaffected skippers")
print("="*70)
print(f"\nSkip rate by cohort:")
for c in ['Silent','Boomer','GenX','MillOld','MillYoung','GenZ']:
    sub = restricted[restricted['cohort6']==c]
    if len(sub) > 0:
        print(f"  {c}: N={len(sub)}, skip%={sub['skipped'].mean()*100:.2f}, skip_count={sub['skipped'].sum()} | share of all skips: {sub['skipped'].sum()/restricted['skipped'].sum()*100:.1f}%")

# Income × cohort grid
print(f"\nSkip rate by cohort × income quintile:")
restricted['inc_q'] = pd.qcut(restricted['faminc'], 5, labels=False, duplicates='drop')
print(f"{'cohort':>10} | " + " | ".join([f"Q{int(q)} skip%" for q in sorted(restricted['inc_q'].dropna().unique())]))
for c in ['Silent','Boomer','GenX','MillOld','MillYoung','GenZ']:
    sub = restricted[restricted['cohort6']==c]
    rates = []
    for iq in sorted(restricted['inc_q'].dropna().unique()):
        ssub = sub[sub['inc_q']==iq]
        if len(ssub) > 0:
            rates.append(f"{ssub['skipped'].mean()*100:>6.2f}% (n={len(ssub)})")
    print(f"{c:>10} | {' | '.join(rates)}")

# BOOMER ZOOM
print(f"\n=== BOOMER-RICH DEEP DIVE ===")
boomers = restricted[restricted['cohort6']=='Boomer'].copy()
print(f"\nBoomer overall: N={len(boomers)}, skip%={boomers['skipped'].mean()*100:.2f}, skip events={boomers['skipped'].sum()}")

# Income detail
print(f"\nBoomer skip rate by faminc level (granular):")
for inc in sorted(boomers['faminc'].dropna().unique()):
    sub = boomers[boomers['faminc']==inc]
    if len(sub) > 30:
        print(f"  faminc={int(inc)}: N={len(sub)}, skip%={sub['skipped'].mean()*100:.2f}")

# Pid7 distribution among high-income boomers
print(f"\nHigh-income Boomer (faminc>=10) pid7 distribution:")
hi_boom = boomers[boomers['faminc']>=10]
print(hi_boom['pid7'].value_counts(dropna=False).sort_index().to_string())
print(f"\nLow-income Boomer (faminc<10) pid7 distribution:")
lo_boom = boomers[boomers['faminc']<10]
print(lo_boom['pid7'].value_counts(dropna=False).sort_index().to_string())

# Skip rate hi vs lo income Boomers
print(f"\nHigh-income Boomers: N={len(hi_boom)}, skip%={hi_boom['skipped'].mean()*100:.2f}%")
print(f"Low-income Boomers: N={len(lo_boom)}, skip%={lo_boom['skipped'].mean()*100:.2f}%")

# Engagement: rich boomers less engaged?
boomers['engaged_count'] = (boomers['CC24_430a_1'].map({1:1,2:0}).fillna(0) +
                              boomers['CC24_430a_2'].map({1:1,2:0}).fillna(0) +
                              boomers['CC24_430a_3'].map({1:1,2:0}).fillna(0))
print(f"\nBoomer engagement count by income quintile:")
print(boomers.groupby('inc_q')['engaged_count'].mean().round(2).to_string())

# WHERE are absolute skip counts? (the user's hypothesis is about ABSOLUTE LOSS)
print(f"\n=== Absolute skip-loss attribution (cohort × income) ===")
print(f"Total Biden-2020 skip events: {restricted['skipped'].sum()}")
print(f"\nTop 10 (cohort, income-quintile) cells by absolute skip count:")
grid = restricted.groupby(['cohort6','inc_q']).agg(N=('skipped','size'), skip_count=('skipped','sum'), skip_pct=('skipped',lambda x: x.mean()*100))
grid = grid.sort_values('skip_count', ascending=False).head(10)
print(grid.to_string())

# Most importantly: which cell has the HIGHEST skip RATE and biggest size?
print(f"\nCells with skip_count >= 30, sorted by skip%:")
big_cells = restricted.groupby(['cohort6','inc_q']).agg(N=('skipped','size'), skip_count=('skipped','sum'), skip_pct=('skipped',lambda x: x.mean()*100))
big_cells = big_cells[big_cells['skip_count'] >= 30].sort_values('skip_pct', ascending=False)
print(big_cells.to_string())
